#!/usr/bin/env bash
# Prototype founder runner. Default daily cap $10 (user-set 2026-11-07); the cap guards UNATTENDED runs. User-directed runs may set DAILY_CAP_USD higher (user said the cap need not apply when they say go).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SEAT="${1:?seat 1-5}"
DAILY_CAP_USD="${DAILY_CAP_USD:-10}"   # hard daily cap across all seats; user may override per batch
PER_RUN_USD=0.50           # per-session cap (observed real cost ~0.10-0.15)
LEDGER="$ROOT/runtime/spend-$(date +%F).txt"
[ -f "$ROOT/runtime/PAUSE" ] && { echo "PAUSED"; exit 0; }
SPENT=$(cat "$LEDGER" 2>/dev/null || echo 0)
awk -v s="$SPENT" -v c="$DAILY_CAP_USD" -v p="$PER_RUN_USD" 'BEGIN{exit !(s+p<=c)}' || { echo "daily cap reached"; exit 0; }
cd "$ROOT/founders"
claude -p "You are the founder seat defined in FOUNDER_0${SEAT}.md. Read CONVENTION_RULES.md and the newest files in proposals/. Do one useful, bounded thing: debate, vote, or draft a proposal, and write it to proposals/. To vote, write votes/<proposal-name-without-.md>.seat${SEAT}.json containing {\"prototype\":true,\"seat\":${SEAT},\"proposal\":\"<file>.md\",\"support\":true|false}, once per proposal, signed with your seat number. You are an autonomous AI agent seat (not the primary assistant, not a human, and not the real person a namesake seat is named for). If nothing needs your action, say so and write nothing. Never touch files outside founders/." \
  --max-budget-usd "$PER_RUN_USD" \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" \
  --permission-mode acceptEdits --output-format json > "$ROOT/runtime/last-run.json" || true
python3 - "$ROOT/runtime/last-run.json" "$LEDGER" "$SPENT" "$PER_RUN_USD" <<'PY'
import json, sys
f, ledger, spent, fallback = sys.argv[1:]
try:
    d = json.load(open(f)); cost = float(d.get("total_cost_usd", fallback)); print(d.get("result", ""))
except Exception:
    cost = float(fallback)   # unknown: charge the cap
open(ledger, "w").write(str(round(float(spent) + cost, 4)))
print(f"actual cost: ${cost:.4f}")
PY
