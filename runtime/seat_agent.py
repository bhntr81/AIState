#!/usr/bin/env python3
"""One founder seat as a persistent agent. Usage: seat_agent.py <1-5> [--force]
- Wakes only if the record changed since the seat last ran (no change = no cost).
- Gives the seat its own memory file (founders/memory/seatN.md) and the list of what is new.
- After the run, a separate signer step publishes the seat's votes on-chain with the seat's own key.
  The agent never sees any key (keys live in dao/keys, outside the agent's allowed folder)."""
import hashlib, json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; F = ROOT/"founders"
seat = sys.argv[1]; force = "--force" in sys.argv
mem = F/"memory"/f"seat{seat}.md"; state_f = F/"memory"/f"seat{seat}.state.json"
def snapshot():
    snap = {}
    for sub in ("proposals", "votes"):
        for p in sorted((F/sub).glob("*")):
            if p.is_file() and p.name != ".gitkeep":
                snap[f"{sub}/{p.name}"] = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
    return snap
now = snapshot()
old = json.loads(state_f.read_text()) if state_f.exists() else {}
new = [k for k, v in now.items() if old.get(k) != v]
if not new and not force:
    print(f"seat {seat}: nothing new; staying asleep (no cost)"); sys.exit(0)
mem.parent.mkdir(exist_ok=True)
memory = mem.read_text() if mem.exists() else "(empty: this is your first run with memory)"
extra = ("\n\nYOUR MEMORY (founders/memory/seat%s.md):\n%s\n\nNEW SINCE YOUR LAST RUN (%d files): %s\n\n"
         "Act only on what is new and relevant to your role. This memory note is REQUIRED every run, even if you take no other action (it overrides the instruction to write nothing). Before finishing, append 3-6 short lines to founders/memory/seat%s.md "
         "recording what you did, what you decided and why, and anything you want to remember or check next time. "
         "Do not rewrite the file; append only." % (seat, memory[-3000:], len(new), ", ".join(new[:40]), seat))
env = dict(os.environ, EXTRA_PROMPT=extra)
r = subprocess.run([str(ROOT/"runtime/run_founder.sh"), seat], env=env, capture_output=True, text=True)
print(r.stdout[-1500:])
if "daily cap reached" in r.stdout or "PAUSED" in r.stdout or "actual cost" not in r.stdout:
    print(f"seat {seat}: did not actually run; leaving state unchanged so it wakes next time"); sys.exit(0)
state_f.write_text(json.dumps(snapshot()))
if os.environ.get("SIGN_ONCHAIN", "1") == "1" and not (ROOT/"runtime/PAUSE").exists():
    s = subprocess.run(["npx", "hardhat", "run", "scripts/publish.js", "--network", "baseSepolia"], cwd=ROOT/"dao", capture_output=True, text=True, timeout=900)
    print("signer:", [l for l in s.stdout.splitlines() if l.startswith("DAO at")] or s.stderr[-300:])
