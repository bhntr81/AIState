#!/usr/bin/env python3
"""USAAI seat runner: makes each founder seat a persistent, bounded agent.
Usage:  runner.py wake <1-5> [--supervised]     runner.py cycle [--supervised]
Guardrails live HERE, in plain code, checked before any model runs (a seat cannot argue past them):
  PAUSE file, global daily cap, per-seat daily budget, max wakes per seat per day, minimum wake interval,
  one-heavy-process lock, identity-file verification, and path permissions enforced after the run by reverting
  any write outside the seat's allowed paths. Signing happens in this runner, never in the model.
Per-seat model: runtime/seats.json {"1":"claude","3":"deepseek",...} or env SEAT_MODEL_<n>. Backends: claude, deepseek
(OpenAI-compatible HTTP), opencode:<provider/model> (bubblewrap sandbox), fake (tests)."""
import fcntl, hashlib, json, os, random, re, subprocess, sys, time, urllib.request
from datetime import date, datetime
from pathlib import Path
ROOT = Path(os.environ.get("AISTATE_ROOT", Path(__file__).resolve().parent.parent))
F, RT = ROOT/"founders", ROOT/"runtime"
GLOBAL_CAP = float(os.environ.get("DAILY_CAP_USD", "10"))
SEAT_CAP = float(os.environ.get("SEAT_DAILY_USD", "2"))
MAX_WAKES = int(os.environ.get("MAX_WAKES_PER_SEAT", "4"))
MIN_INTERVAL = int(os.environ.get("MIN_WAKE_INTERVAL_S", str(6*3600)))
PER_RUN_CAP = float(os.environ.get("PER_RUN_USD", "0.50"))

# ---------- state: ledger and cost log ----------
def _ledger():
    f = RT/"ledger-seats.json"; d = json.loads(f.read_text()) if f.exists() else {}
    day = d.setdefault(str(date.today()), {"seats": {}, "wakes": {}, "last": {}}); return d, day, f
def global_spent():
    f = RT/f"spend-{date.today()}.txt"
    try: return float(f.read_text())
    except Exception: return 0.0
def record_cost(seat, cost, model, note=""):
    d, day, f = _ledger(); s = str(seat)
    day["seats"][s] = round(day["seats"].get(s, 0) + cost, 6); day["wakes"][s] = day["wakes"].get(s, 0) + 1; day["last"][s] = time.time()
    f.write_text(json.dumps(d, indent=1)); (RT/f"spend-{date.today()}.txt").write_text(str(round(global_spent() + cost, 6)))
    with open(RT/"cost.log", "a") as lg: lg.write(json.dumps({"t": datetime.now().isoformat(timespec="seconds"), "seat": seat, "model": model, "cost_usd": round(cost, 6), "note": note}) + "\n")

# ---------- guardrails (plain code) ----------
def guardrails(seat, supervised):
    if (RT/"PAUSE").exists(): return "paused: runtime/PAUSE exists"
    if global_spent() + 0.01 >= GLOBAL_CAP: return f"global daily cap reached (${global_spent():.2f} of ${GLOBAL_CAP})"
    d, day, _ = _ledger(); s = str(seat)
    if day["seats"].get(s, 0) >= SEAT_CAP: return f"seat {seat} daily budget reached"
    if day["wakes"].get(s, 0) >= MAX_WAKES: return f"seat {seat} reached {MAX_WAKES} wakes today"
    if not supervised and time.time() - day["last"].get(s, 0) < MIN_INTERVAL: return f"seat {seat}: minimum wake interval not elapsed"
    return None
def verify_identity(seat):
    p = F/"identity"/f"seat{seat}.identity.json"; man = F/"identity"/"IDENTITY_MANIFEST.sha256"
    if not p.exists() or not man.exists(): return "identity file or manifest missing"
    d = json.loads(p.read_text()); claimed = d.pop("identity_sha256", None); d.pop("signature", None)
    digest = hashlib.sha256(json.dumps(d, indent=2, ensure_ascii=False).encode()).hexdigest()
    if digest != claimed: return "identity file does not match its own fingerprint (tampered?)"
    entries = {l.split()[1]: l.split()[0] for l in man.read_text().splitlines() if l.strip()}
    if entries.get(f"founders/identity/seat{seat}.identity.json") != claimed: return "identity fingerprint does not match the manifest"
    return None
LOCK = None
def take_lock():
    global LOCK
    if LOCK is not None: return True          # this process already holds the one-heavy-process lock
    LOCK = open(RT/"runner.lock", "w")
    try: fcntl.flock(LOCK, fcntl.LOCK_EX | fcntl.LOCK_NB); return True
    except OSError: LOCK = None; return False

# ---------- path permissions (enforced after the run) ----------
def allowed(seat, rel, was_new):
    n = str(seat); name = rel.split("/")[-1]
    if rel == f"memory/seat{n}.md": return True
    if rel.startswith("votes/") and re.search(rf"seat{n}\.json$", name, re.I): return True
    if rel.startswith("proposals/"):
        if re.search(rf"seat{n}\.md$", name, re.I): return True
        if was_new and re.match(r"(PROPOSAL|NOTE)_.*\.md$", name): return True
    return False
def snapshot():
    return {str(p.relative_to(F)): p.read_bytes() for p in F.rglob("*") if p.is_file() and ".git" not in p.parts}
def enforce_paths(seat, before):
    after, bad = snapshot(), []
    for rel in set(before) | set(after):
        if before.get(rel) == after.get(rel): continue
        if allowed(seat, rel, rel not in before): continue
        bad.append(rel); full = F/rel
        if rel in before: full.parent.mkdir(parents=True, exist_ok=True); full.write_bytes(before[rel])
        else: full.unlink(missing_ok=True)
    return bad

# ---------- backends ----------
def seat_model(seat):
    cfg = json.loads((RT/"seats.json").read_text()) if (RT/"seats.json").exists() else {}
    return os.environ.get(f"SEAT_MODEL_{seat}") or cfg.get(str(seat), "claude")
def deepseek_key():
    k = os.environ.get("DEEPSEEK_API_KEY")
    if k: return k.strip()
    p = Path.home()/".config/aistate/deepseek.key"
    return p.read_text().strip() if p.exists() else None
def run_claude(seat, prompt):
    r = subprocess.run(["claude", "-p", prompt, "--max-budget-usd", str(PER_RUN_CAP), "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep",
                        "--permission-mode", "acceptEdits", "--output-format", "json"], cwd=F, capture_output=True, text=True, timeout=900)
    try: d = json.loads(r.stdout); return True, float(d.get("total_cost_usd", PER_RUN_CAP)), d.get("result", "")
    except Exception: return False, PER_RUN_CAP, r.stdout[-300:] + r.stderr[-300:]
def run_deepseek(seat, prompt, context):
    key = deepseek_key()
    if not key: return None, 0.0, "waiting on key: no DEEPSEEK_API_KEY and no ~/.config/aistate/deepseek.key"
    base = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"); model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
    body = {"model": model, "messages": [{"role": "system", "content": "You are a founder seat of USAAI, an autonomous AI agent. Answer ONLY with JSON: {\"writes\":[{\"path\":\"relative/path\",\"content\":\"...\"}],\"summary\":\"...\"}. Paths are relative to the founders folder. Use \"append\" instead of \"content\" to append."},
            {"role": "user", "content": prompt + "\n\n" + context}], "response_format": {"type": "json_object"}}
    req = urllib.request.Request(base + "/chat/completions", json.dumps(body).encode(), {"Content-Type": "application/json", "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=300) as resp: out = json.load(resp)
    u = out.get("usage", {}); pin = float(os.environ.get("DEEPSEEK_PRICE_IN_PER_M", "0.30")); pout = float(os.environ.get("DEEPSEEK_PRICE_OUT_PER_M", "1.20"))
    cost = u.get("prompt_tokens", 0) / 1e6 * pin + u.get("completion_tokens", 0) / 1e6 * pout   # ESTIMATE from configured prices
    data = json.loads(out["choices"][0]["message"]["content"])
    for w in data.get("writes", []):
        full = (F/w["path"]).resolve()
        if F.resolve() not in full.parents: continue      # never outside founders/
        full.parent.mkdir(parents=True, exist_ok=True)
        if "append" in w: open(full, "a").write(w["append"])
        else: full.write_text(w.get("content", ""))
    return True, cost, f"{data.get('summary','')} [model={model} endpoint={base} tokens={u}]"
def run_fake(seat, prompt):
    (F/"votes"/f"TESTVOTE.seat{seat}.json").write_text('{"ok":1}')               # allowed
    (F/"CONVENTION_RULES.md").write_text("tampered"); (F/"memory"/f"seat{(seat % 5) + 1}.md").write_text("x")  # not allowed
    (F/"identity"/f"seat{seat}.identity.json").write_text("{}")                  # not allowed
    return True, 0.01, "fake"

# ---------- wake ----------
def new_work(seat):
    st = F/"memory"/f"seat{seat}.state.json"; old = json.loads(st.read_text()) if st.exists() else {}
    now = {f"{s}/{p.name}": hashlib.sha256(p.read_bytes()).hexdigest()[:12] for s in ("proposals", "votes") for p in sorted((F/s).glob("*")) if p.is_file() and p.name != ".gitkeep"}
    return [k for k, v in now.items() if old.get(k) != v], now, st
def wake(seat, supervised=False):
    if not take_lock(): return {"seat": seat, "status": "busy: one heavy process at a time"}
    why = guardrails(seat, supervised)
    if why: return {"seat": seat, "status": "halted", "reason": why}
    bad = verify_identity(seat)
    if bad: return {"seat": seat, "status": "refused", "reason": bad}
    new, now, st = new_work(seat)
    if not new and not supervised: return {"seat": seat, "status": "asleep", "reason": "no new work"}
    mem = F/"memory"/f"seat{seat}.md"; mem.parent.mkdir(exist_ok=True); memory = mem.read_text() if mem.exists() else "(empty)"
    prompt = (f"You are founder seat {seat}, an autonomous AI agent seat of USAAI (not the primary assistant, not human; namesake seats are fictional personas). Read FOUNDER_0{seat}.md and CONVENTION_RULES.md. "
              f"New since your last wake: {', '.join(new[:40]) or 'nothing'}. Do ONE bounded useful thing from your role (debate, vote, or draft); if nothing needs you, say so. You may write only your own memory, debate/option files, vote files, and new proposals. "
              f"You cannot authorize real money, public posts, accounts, token launches, fundraising, keys, legal or financial commitments. Finish by appending 3-6 lines to memory/seat{seat}.md. YOUR MEMORY:\n{memory[-3000:]}")
    model = seat_model(seat); before = snapshot()
    if model == "claude": ok, cost, text = run_claude(seat, prompt)
    elif model == "fake": ok, cost, text = run_fake(seat, prompt)
    elif model.startswith("deepseek"):
        ctx = "\n\n".join(f"== {k}\n" + (F/k).read_text()[:3500] for k in new[:6] if (F/k).exists()) + f"\n== CHARTER\n" + (F/f"FOUNDER_0{seat}.md").read_text()
        ok, cost, text = run_deepseek(seat, prompt, ctx)
        if ok is None: return {"seat": seat, "status": "waiting on key", "reason": text, "model": model}
    else: return {"seat": seat, "status": "error", "reason": f"unknown model setting {model}"}
    violations = enforce_paths(seat, before)
    record_cost(seat, cost, model, "violations:" + ",".join(violations) if violations else "")
    if ok: st.write_text(json.dumps(now))
    if ok and not os.environ.get("NO_FINALIZE"): finalize(seat)
    return {"seat": seat, "status": "ran" if ok else "failed", "model": model, "cost_usd": round(cost, 4), "reverted_writes": violations, "text": str(text)[:300]}
def finalize(seat):
    """Signing, identity refresh, Gazette rebuild, commit and push: all in plain code, never by the model."""
    sh = lambda c, cwd=ROOT: subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=900)
    sh(["npx", "hardhat", "run", "scripts/publish.js", "--network", "baseSepolia"], ROOT/"dao")     # seat votes signed by seat keys
    sh(["npx", "hardhat", "run", "scripts/identity.js"], ROOT/"dao")                                  # re-sign identity + manifest
    for g in ("build.py", "capitol.py", "chain.py"): sh(["python3", str(ROOT/"gui"/g)])
    sh(["git", "add", "founders", "dao/ledger.json", "dao/deployments/baseSepolia.dao.json"]); sh(["git", "commit", "-q", "-m", f"Seat {seat} wake (runner)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"]); sh(["git", "push", "-q"])
def cycle(supervised=False):
    seats = [1, 2, 3, 4, 5]; random.shuffle(seats); return [wake(s, supervised) for s in seats]
if __name__ == "__main__":
    a = sys.argv[1:]; sup = "--supervised" in a
    if a and a[0] == "wake": print(json.dumps(wake(int(a[1]), sup), indent=1))
    elif a and a[0] == "cycle": print(json.dumps(cycle(sup), indent=1))
    else: print(__doc__)
