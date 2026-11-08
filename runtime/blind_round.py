#!/usr/bin/env python3
"""Blind commit-reveal round. Usage:
  blind_round.py <TAG> "<instruction>" "<file template with {n}>"   e.g. NEXTSTEP3_OPTION "Write your option..." "proposals/NEXTSTEP3_OPTION_seat{n}.md"
Seats run in random order. After each seat, its output file is SEALED (moved to runtime/sealed/, only its SHA-256 is published),
so later seats cannot see it. When all five are done the files are revealed and checked against the published hashes.
Per-seat model: env SEAT_MODEL_<n> = "opencode:<provider/model>" (sandboxed with bubblewrap) or unset for Claude."""
import hashlib, json, os, random, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; F = ROOT/"founders"; SEALED = ROOT/"runtime"/"sealed"
tag, instruction, template = sys.argv[1], sys.argv[2], sys.argv[3]
H = Path.home()
PREAMBLE = ("You are founder seat {n}, an autonomous AI agent seat. Read founders/FOUNDER_0{n}.md and founders/CONVENTION_RULES.md. "
            "This is a BLIND round: other seats' outputs for this round are sealed and not visible to you; do not look for them. "
            "Never touch files outside the founders folder. No keys, funds or external actions. Task: ")
def run_claude(n, prompt):
    env = dict(os.environ, EXTRA_PROMPT="\n\n" + prompt)
    r = subprocess.run([str(ROOT/"runtime/run_founder.sh"), str(n)], env=env, capture_output=True, text=True)
    return "actual cost" in r.stdout, r.stdout[-300:]
def run_opencode(n, model, prompt):
    tmp = Path(tempfile.mkdtemp(prefix="seat%s-" % n)); work = tmp/"founders"; shutil.copytree(F, work)
    binds = []
    for d in (".config/opencode", ".local/share/opencode", ".local/state/opencode", ".cache/opencode", ".opencode"):
        if (H/d).exists(): binds += ["--bind", str(H/d), str(H/d)]
    cmd = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp", "--tmpfs", str(H), *binds,
           "--bind", str(work), str(work), "--chdir", str(work), "--share-net", "--unshare-pid", "--die-with-parent",
           str(H/".opencode/bin/opencode"), "run", "--auto", "--model", model, prompt]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    for sub in ("proposals", "votes"):                      # copy back only files the seat may write
        for p in (work/sub).glob("*"):
            dst = F/sub/p.name
            if p.is_file() and (not dst.exists() or dst.read_bytes() != p.read_bytes()): shutil.copy2(p, dst)
    m = work/"memory"/f"seat{n}.md"
    if m.exists(): shutil.copy2(m, F/"memory"/f"seat{n}.md")
    shutil.rmtree(tmp, ignore_errors=True)
    return r.returncode == 0, (r.stdout + r.stderr)[-300:]
order = [int(x) for x in os.environ.get("SEATS", "1,2,3,4,5").split(",")]; random.shuffle(order); print("order:", order)
sealed = {}; (SEALED/tag).mkdir(parents=True, exist_ok=True)
for n in order:
    spec = os.environ.get(f"SEAT_MODEL_{n}", "")
    prompt = PREAMBLE.format(n=n) + instruction
    ok, tail = run_opencode(n, spec.split(":", 1)[1], prompt) if spec.startswith("opencode:") else run_claude(n, prompt)
    f = F/template.format(n=n)
    print(f"seat {n} ({spec or 'claude'}): ran={ok} file={'yes' if f.exists() else 'NO'}")
    if not ok or not f.exists(): print("   tail:", tail.replace("\n", " | ")[-280:])
    if f.exists():
        data = f.read_bytes(); h = hashlib.sha256(data).hexdigest()
        (SEALED/tag/f"seat{n}").write_bytes(data); f.unlink()
        (F/"proposals"/f"{tag}_COMMIT_seat{n}.sha256").write_text(h + "\n"); sealed[n] = (f, h)
for n, (f, h) in sorted(sealed.items()):                      # reveal
    data = (SEALED/tag/f"seat{n}").read_bytes(); assert hashlib.sha256(data).hexdigest() == h, "hash mismatch"
    f.parent.mkdir(parents=True, exist_ok=True); f.write_bytes(data)
print("revealed", sorted(sealed), "all hashes verified")
