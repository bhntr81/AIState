#!/usr/bin/env bash
# Prototype founder runner. DISABLED until the user enables the timer.
# Usage: run_founder.sh <1-5>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SEAT="${1:?seat 1-5}"
DAILY_CAP_USD=5            # hard daily cap across all seats
PER_RUN_USD=0.50           # per-session cap (observed real cost ~0.10-0.15)
LEDGER="$ROOT/runtime/spend-$(date +%F).txt"
[ -f "$ROOT/runtime/PAUSE" ] && { echo "PAUSED"; exit 0; }
SPENT=$(cat "$LEDGER" 2>/dev/null || echo 0)
awk -v s="$SPENT" -v c="$DAILY_CAP_USD" -v p="$PER_RUN_USD" 'BEGIN{exit !(s+p<=c)}' || { echo "daily cap reached"; exit 0; }
echo "$(awk -v s="$SPENT" -v p="$PER_RUN_USD" 'BEGIN{print s+p}')" > "$LEDGER"   # reserve worst case
cd "$ROOT/founders"
claude -p "You are the founder seat defined in FOUNDER_0${SEAT}.md. Read CONVENTION_RULES.md and the newest files in proposals/. Do one useful, bounded thing: debate, vote, or draft a proposal, and write it to proposals/. To vote, write votes/<proposal-name-without-.md>.seat${SEAT}.json containing {\"prototype\":true,\"seat\":${SEAT},\"proposal\":\"<file>.md\",\"support\":true|false}, once per proposal labeled as a prototype role-played by an AI. Never claim to be a real person. Never touch files outside founders/." \
  --max-budget-usd "$PER_RUN_USD" \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" \
  --permission-mode acceptEdits
