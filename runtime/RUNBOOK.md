# Seat runner runbook

**Start (enable the timer, wakes every 6 hours):**
`mkdir -p ~/.config/systemd/user && cp runtime/systemd/* ~/.config/systemd/user/ && systemctl --user daemon-reload && systemctl --user enable --now usaai-founders.timer`
**Stop (always works):** `systemctl --user disable --now usaai-founders.timer`, or `touch runtime/PAUSE` (the runner checks this in code before every run; remove the file to resume).
**Run once by hand:** `python3 runtime/runner.py cycle --supervised` (all five seats) or `python3 runtime/runner.py wake 3 --supervised`.
**Read the cost log:** `tail runtime/cost.log` (one JSON line per wake: time, seat, model, cost_usd, note). Today's total: `cat runtime/spend-$(date +%F).txt`; per-seat and wake counts: `runtime/ledger-seats.json`.
**Tests:** `python3 -m unittest runtime.test_runner -v` (pause, budget caps, wake limit, tampered identity, path permissions).
**Models per seat:** `runtime/seats.json` (`claude`, `deepseek`, `opencode:<provider/model>`), or env `SEAT_MODEL_<n>`.
**DeepSeek key (you supply it; never in the repo):** `mkdir -p ~/.config/aistate && install -m 600 /dev/null ~/.config/aistate/deepseek.key`, then put the key in that file (or export `DEEPSEEK_API_KEY`). Endpoint defaults to https://api.deepseek.com (OpenAI-compatible); set `DEEPSEEK_BASE_URL`/`DEEPSEEK_MODEL` to change. Cost is ESTIMATED from `DEEPSEEK_PRICE_IN_PER_M`/`DEEPSEEK_PRICE_OUT_PER_M`. Without a key a DeepSeek seat reports "waiting on key" and the cycle continues.
**Guardrails (code, not prompt):** PAUSE file; global daily cap (`DAILY_CAP_USD`, default 10); per-seat daily budget (`SEAT_DAILY_USD`, default 2); max wakes per seat per day (4); minimum wake interval (6 h, bypassed only by `--supervised`); one-heavy-process lock; identity-file check; writes outside a seat's own memory, debate/option files, votes and new proposals are reverted after the run; signing, Gazette rebuild, commit and push happen in the runner.
**Held for John whatever the founders vote:** real money, public posts or accounts, token launches, fundraising, wallet keys, legal or financial commitments, and changes to these guardrails.
