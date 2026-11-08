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

## Cost report and timer recommendation (2026-11-07)
- **Real cost per wake cycle** (from `runtime/cost.log`): about **$0.44-$0.53** for a full five-seat cycle (a Claude wake is $0.09-$0.20; a Gemini wake is $0 on the free tier). Four supervised cycles plus the drill logged **$1.9973 across 20 wakes**.
- **Why today ran far above that:** the day's total was **$15.31 against the $10 default cap**. About **$13.32 predates the runner's cost log**: the build-out sessions (Sessions 5-14), run one seat at a time with extra rounds for dependencies, retries and test runs. That is a **one-off**. About $2.00 is runner cycles, mostly the **supervised** extras I ran to test the runner; those are also one-off.
- **What the timer would cost:** at one cycle every 6 hours (4 a day) the worst case is about 4 x $0.50 = **about $2 a day**, and usually less because a seat with no new work sleeps and costs nothing. A seat on Gemini costs $0.
- **Recommended timer settings** (already set in `runtime/systemd/usaai-founders.service`): interval **every 6 hours**; **daily cap $3**; **per-seat cap $0.60**; **max 4 wakes per seat per day**. Raise them only deliberately.
- **Enable (not run by the assistant):** `mkdir -p ~/.config/systemd/user && cp runtime/systemd/* ~/.config/systemd/user/ && systemctl --user daemon-reload && systemctl --user enable --now usaai-founders.timer`
- **Stop:** `systemctl --user disable --now usaai-founders.timer`, or `touch runtime/PAUSE`.

## Timer-readiness verdict (2026-11-07, from the logs)
**READY WITH CHANGES. Not enabled.**
- **Settings that really apply to unattended runs:** the unit file sets `DAILY_CAP_USD=3`, `SEAT_DAILY_USD=0.6`, `MAX_WAKES_PER_SEAT=4`, every 6 hours; the runner reads those from its environment (checked: it reports 3.0 / 0.6 / 4 / 21600 s under the unit's environment), so the $10 default does not apply to the timer. `Linger=yes` is set, so the timer runs while you are logged out.
- **Real cost:** a full five-seat cycle averages about $0.50 ($0.44-$0.60 over seven cycles); a Claude wake is about $0.13, a Gemini wake $0. Four cycles a day is about $2 at most, and less unattended because quiet seats sleep; the $3 daily cap bounds it.
- **Changes before enabling:** (1) confirm the debate-path fix (the old prompt wording made three seats save notes to a nonexistent `debate/` folder, which the runner reverted; reworded, to be confirmed by the next cycle showing no violations); (2) decide whether unattended runs may commit and push to the public repository (today they do, after path checks); (3) the founders' vote on Proposal 21 (wake pre-check, which also guards against a seat ignoring an assigned task, as seat 4 did twice).
- **Enable (not run by the assistant):** `mkdir -p ~/.config/systemd/user && cp runtime/systemd/* ~/.config/systemd/user/ && systemctl --user daemon-reload && systemctl --user enable --now usaai-founders.timer`
- **Stop:** `systemctl --user disable --now usaai-founders.timer`, or `touch runtime/PAUSE`. **Is a cycle running?** `python3 runtime/runner.py status` (from the lock, not a text search).
