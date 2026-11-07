#!/usr/bin/env bash
# One scheduled round: each founder seat runs once, in turn. Guarded by the PAUSE file and the daily cap.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for s in 1 2 3 4 5; do "$ROOT/runtime/run_founder.sh" "$s" >> "$ROOT/runtime/tick.log" 2>&1; done
python3 "$ROOT/gui/build.py" >/dev/null 2>&1; python3 "$ROOT/gui/capitol.py" >/dev/null 2>&1
