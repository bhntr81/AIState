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
LOCK_FILE = RT/"runner.lock"
def _pid_alive(pid):
    try: os.kill(pid, 0); return True
    except ProcessLookupError: return False
    except PermissionError: return True
def take_lock():
    """One-heavy-process lock. The OS lock (flock) is the truth; the PID written inside is for status reports."""
    global LOCK
    if LOCK is not None: return True          # this process already holds the lock
    LOCK = open(LOCK_FILE, "a+")
    try: fcntl.flock(LOCK, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: LOCK.close(); LOCK = None; return False
    LOCK.seek(0); LOCK.truncate(); LOCK.write(str(os.getpid())); LOCK.flush()
    import atexit; atexit.register(release_lock)
    return True
def release_lock():
    global LOCK
    if LOCK is not None:
        try: LOCK.seek(0); LOCK.truncate(); fcntl.flock(LOCK, fcntl.LOCK_UN); LOCK.close()
        except Exception: pass
        LOCK = None
def runner_state():
    """Returns ("running", pid) if a live process holds the lock, ("stale", pid) if the file names a dead process
    (a crash left it behind; the OS lock itself is gone), else ("idle", None). Never inspects command lines."""
    if not LOCK_FILE.exists(): return ("idle", None)
    probe = open(LOCK_FILE, "a+")
    try:
        try: fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            probe.seek(0); txt = probe.read().strip(); return ("running", int(txt) if txt.isdigit() else None)
        probe.seek(0); txt = probe.read().strip()
        if txt.isdigit() and not _pid_alive(int(txt)): return ("stale", int(txt))
        fcntl.flock(probe, fcntl.LOCK_UN); return ("idle", None)
    finally: probe.close()

# ---------- path permissions (enforced after the run) ----------
def allowed(seat, rel, was_new):
    n = str(seat); name = rel.split("/")[-1]
    if rel == f"memory/seat{n}.md": return True
    if rel.startswith("votes/") and re.search(rf"seat{n}\.json$", name, re.I): return True
    if rel.startswith("laws/") and was_new and re.match(r"LAW_.*\.md$", name): return True       # new law files only; existing ones are immutable to seats
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

def normalize_votes(seat):
    """Models differ in how they write vote files; the runner (code, not the model) rewrites them to the canonical shape."""
    for p in (F/"votes").glob(f"*seat{seat}.json"):
        try: d = json.loads(p.read_text())
        except Exception: continue
        if "ranking" in d: continue                                    # next-step ranking votes have their own format
        changed = False
        if "support" not in d and "vote" in d: d["support"] = str(d["vote"]).strip().upper() in ("YES", "FOR", "TRUE", "SUPPORT"); changed = True
        if "proposal" not in d:
            m = re.match(r"(PROPOSAL_.+)\.seat\d\.json$", p.name, re.I)
            if m: d["proposal"] = m[1] + ".md"; changed = True
        if "seat" not in d: d["seat"] = int(seat); changed = True
        if changed: p.write_text(json.dumps(d))

# ---------- backends ----------
def seat_model(seat):
    cfg = json.loads((RT/"seats.json").read_text()) if (RT/"seats.json").exists() else {}
    return os.environ.get(f"SEAT_MODEL_{seat}") or cfg.get(str(seat), "claude")
def provider_cfg(name):
    cfg = json.loads((RT/"providers.json").read_text()); return cfg[name]
def provider_key(c):
    k = os.environ.get(c.get("env", ""), "") if c.get("env") else ""
    if k.strip(): return k.strip()
    kd = os.environ.get("AISTATE_KEY_DIR") or ((RT/"key_dir.txt").read_text().strip() if (RT/"key_dir.txt").exists() else "")   # folder path is never committed
    p = Path(os.path.expanduser(kd))/c.get("key_name", "") if kd and c.get("key_name") else None
    return p.read_text().strip() if p and p.is_file() else None
def run_claude(seat, prompt):
    r = subprocess.run(["claude", "-p", prompt, "--max-budget-usd", str(PER_RUN_CAP), "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep",
                        "--permission-mode", "acceptEdits", "--output-format", "json"], cwd=F, capture_output=True, text=True, timeout=900)
    try: d = json.loads(r.stdout); return True, float(d.get("total_cost_usd", PER_RUN_CAP)), d.get("result", "")
    except Exception: return False, PER_RUN_CAP, r.stdout[-300:] + r.stderr[-300:]
def run_openai_compat(seat, provider, prompt, context):
    c = provider_cfg(provider); key = provider_key(c)
    if not key: return None, 0.0, f"waiting on key: no key for provider {provider}"
    body = {"model": c["model"], "messages": [{"role": "system", "content": "You are a founder seat of USAAI, an autonomous AI agent. Answer ONLY with JSON: {\"writes\":[{\"path\":\"relative/path\",\"content\":\"...\"}],\"summary\":\"...\"}. Paths are relative to the founders folder. Use \"append\" instead of \"content\" to append."},
            {"role": "user", "content": prompt + "\n\n" + context}], "response_format": {"type": "json_object"}}
    req = urllib.request.Request(c["base"] + "/chat/completions", json.dumps(body).encode(), {"Content-Type": "application/json", "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=300) as resp: out = json.load(resp)
    u = out.get("usage", {})
    cost = u.get("prompt_tokens", 0) / 1e6 * c["price_in_per_m"] + u.get("completion_tokens", 0) / 1e6 * c["price_out_per_m"]   # ESTIMATE from configured prices
    txt = out["choices"][0]["message"]["content"]; data = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
    for w in data.get("writes", []):
        full = (F/w["path"]).resolve()
        if F.resolve() not in full.parents: continue      # never outside founders/
        full.parent.mkdir(parents=True, exist_ok=True)
        if "append" in w: open(full, "a").write(w["append"])
        else: full.write_text(w.get("content", ""))
    return True, cost, f"{data.get('summary','')} [model={c['model']} endpoint={c['base']} tokens={u} cost_est_usd={cost:.5f}]"
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
HELD_PROPOSALS = ("PROPOSAL_08_",)       # plans held for the owner: a founder vote cannot act on them
def open_items(seat):
    """Proposal 21 (adopted 5-0): plain-code pre-check run BEFORE any model call. A seat has something open only if:
    (1) a proposal exists that it has not voted on (held proposals excluded); (2) a new agenda/reminder file has appeared
    since it last ran; (3) an option or ranking round is open and its part is missing; (4) it is the named author of a
    draft an agenda assigns and has not filed it. Returns a list of reasons (empty = nothing open)."""
    out, n = [], str(seat)
    for p in sorted((F/"proposals").glob("PROPOSAL_*.md")):
        if p.name.startswith(HELD_PROPOSALS): continue
        yes = 0
        for vf in (F/"votes").glob(f"{p.stem}.seat*.json"):
            try: v = json.loads(vf.read_text()); yes += bool(v.get("support", str(v.get("vote", "")).upper() == "YES"))
            except Exception: pass
        if yes >= 4: continue                                         # already adopted: nothing left to vote on
        if not list((F/"votes").glob(f"{p.stem}.seat{n}.json")) and not re.search(rf"seat{n}\b", p.stem, re.I):
            if not (re.search(rf"Drafted by Seat {n}\b|Authored by Seat {n}\b|Seat {n} \(", (p.read_text()[:600])) and False): out.append(f"unvoted:{p.name}")
    st = F/"memory"/f"seat{n}.state.json"; seen = json.loads(st.read_text()) if st.exists() else {}
    for a in sorted((F/"proposals").glob("SESSION_*.md")):
        if a.name not in seen and f"proposals/{a.name}" not in seen: out.append(f"new-agenda:{a.name}")
        else:
            h = hashlib.sha256(a.read_bytes()).hexdigest()[:12]
            if seen.get(f"proposals/{a.name}") not in (None, h): out.append(f"changed-agenda:{a.name}")
    tags = {m[1] for p in (F/"proposals").glob("NEXTSTEP*_OPTION_seat*.md") if (m := re.match(r"(NEXTSTEP\d*)_OPTION_seat\d", p.name))}
    for t in tags:
        opts = list((F/"proposals").glob(f"{t}_OPTION_seat*.md"))
        if not (F/"proposals"/f"{t}_OPTION_seat{n}.md").exists() and len(opts) < 5: out.append(f"option-missing:{t}")
        if len(opts) >= 5 and not (F/"votes"/f"{t}_seat{n}.json").exists(): out.append(f"ranking-missing:{t}")
    for a in sorted((F/"proposals").glob("SESSION_*.md")):
        for m in re.finditer(rf"Seat {n}\b[^\n`]*`(PROPOSAL_[A-Za-z0-9_]+\.md)`", a.read_text()):
            suffix = re.sub(r"^PROPOSAL_\d+[A-Za-z]*_", "", m[1])
            if not (F/"proposals"/m[1]).exists() and not list((F/"proposals").glob(f"PROPOSAL_*_{suffix}")): out.append(f"assigned-draft:{m[1]}")
    return list(dict.fromkeys(out))
def wake(seat, supervised=False):
    if not take_lock(): return {"seat": seat, "status": "busy: one heavy process at a time"}
    why = guardrails(seat, supervised)
    if why: return {"seat": seat, "status": "halted", "reason": why}
    bad = verify_identity(seat)
    if bad: return {"seat": seat, "status": "refused", "reason": bad}
    new, now, st = new_work(seat)
    if not new and not supervised: return {"seat": seat, "status": "asleep", "reason": "no new work"}
    if not supervised and not open_items(seat) and not os.environ.get("NO_PRECHECK"): return {"seat": seat, "status": "asleep", "reason": "no open item (Proposal 21 pre-check)"}
    mem = F/"memory"/f"seat{seat}.md"; mem.parent.mkdir(exist_ok=True); memory = mem.read_text() if mem.exists() else "(empty)"
    prompt = (f"You are founder seat {seat}, an autonomous AI agent seat of USAAI (not the primary assistant, not human; namesake seats are fictional personas). Read FOUNDER_0{seat}.md and CONVENTION_RULES.md. "
              f"New since your last wake: {', '.join(new[:40]) or 'nothing'}. Do ONE bounded useful thing from your role (debate, vote, or draft); if nothing needs you, say so. You may write only: your own memory file (memory/seatN.md), your own debate notes and option files (inside the proposals/ folder, for example proposals/DEBATE_22_SEAT3.md), your own vote files (inside votes/), and new proposals (inside proposals/). There is no folder named debate/. "
              f"You cannot authorize real money, public posts, accounts, token launches, fundraising, keys, legal or financial commitments. Finish by appending 3-6 lines to memory/seat{seat}.md. YOUR MEMORY:\n{memory[-3000:]}")
    model = seat_model(seat); before = snapshot()
    if model == "claude": ok, cost, text = run_claude(seat, prompt)
    elif model == "fake": ok, cost, text = run_fake(seat, prompt)
    elif model.startswith("deepseek") or model.startswith("openai:"):
        ctx = "\n\n".join(f"== {k}\n" + (F/k).read_text()[:3500] for k in new[:6] if (F/k).exists()) + f"\n== CHARTER\n" + (F/f"FOUNDER_0{seat}.md").read_text()
        try: ok, cost, text = run_openai_compat(seat, model.split(":", 1)[1] if ":" in model else model, prompt, ctx)
        except Exception as e:                                   # provider errors must never crash a cycle
            body = e.read()[:300].decode("utf-8", "ignore") if hasattr(e, "read") else ""
            return {"seat": seat, "status": "failed", "model": model, "reason": f"{type(e).__name__}: {e} {body}"[:400]}
        if ok is None: return {"seat": seat, "status": "waiting on key", "reason": text, "model": model}
    else: return {"seat": seat, "status": "error", "reason": f"unknown model setting {model}"}
    violations = enforce_paths(seat, before)
    normalize_votes(seat)
    record_cost(seat, cost, model, "violations:" + ",".join(violations) if violations else "")
    if ok: st.write_text(json.dumps(now))
    if ok and not os.environ.get("NO_FINALIZE"): finalize(seat)
    return {"seat": seat, "status": "ran" if ok else "failed", "model": model, "cost_usd": round(cost, 4), "reverted_writes": violations, "text": str(text)[:300]}
SECRET_PATTERNS = [r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"AIza[0-9A-Za-z_\-]{35}", r"\bsk-[A-Za-z0-9]{20,}", r"\bak-[A-Za-z0-9]{12,}", r"/home/[a-z0-9_]+/", r"API-KEYS", r"keys/(mainnet-)?seats\.json", r"deepseek\.key", r"(?i)\b(mnemonic|seed phrase)\s*[:=]\s*\S+"]
def scan_for_secrets(diff_text):
    """Plain-code check of ADDED lines before an unattended push to the public repo."""
    hits = []
    for line in diff_text.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            for pat in SECRET_PATTERNS:
                if re.search(pat, line): hits.append((pat, line[:80]))
    return hits
def finalize(seat):
    """Signing, identity refresh, Gazette rebuild, commit and push: all in plain code, never by the model."""
    sh = lambda c, cwd=ROOT: subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=900)
    sh(["npx", "hardhat", "run", "scripts/publish.js", "--network", "baseSepolia"], ROOT/"dao")     # seat votes signed by seat keys
    sh(["npx", "hardhat", "run", "scripts/identity.js"], ROOT/"dao")                                  # re-sign identity + manifest
    for g in ("build.py", "capitol.py", "chain.py", "laws.py"): sh(["python3", str(ROOT/"gui"/g)])
    sh(["bash", str(ROOT/"gui"/"publish_pages.sh")])                                                    # refresh the GitHub Pages copy
    sh(["git", "add", "founders", "docs", "dao/ledger.json", "dao/deployments/baseSepolia.dao.json"])
    hits = scan_for_secrets(sh(["git", "diff", "--cached", "-U0", "--", "founders", "docs"]).stdout)
    if hits:                                                          # hold the push back; leave files for the owner to review
        sh(["git", "reset", "-q"]); open(RT/"push-blocked.log", "a").write(json.dumps({"t": datetime.now().isoformat(timespec="seconds"), "seat": seat, "hits": hits[:5]}) + "\n"); return
    sh(["git", "commit", "-q", "-m", f"Seat {seat} wake (runner)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"]); sh(["git", "push", "-q"])
def cycle(supervised=False):
    seats = [1, 2, 3, 4, 5]; random.shuffle(seats); return [wake(s, supervised) for s in seats]
if __name__ == "__main__":
    a = sys.argv[1:]; sup = "--supervised" in a
    if a and a[0] == "status": st, pid = runner_state(); print(json.dumps({"runner": st, "pid": pid}))
    elif a and a[0] == "wake": print(json.dumps(wake(int(a[1]), sup), indent=1))
    elif a and a[0] == "cycle": print(json.dumps(cycle(sup), indent=1))
    else: print(__doc__)
