# Runtime and governance decisions (2026-11-07)

> **PROTOTYPE.** Founders are role-played AI personas; namesake seats are not the real people.

## User decisions (this date)
- Runtime: **local on this Kali machine**. Daily cap **$5**, per-run cap $0.50, enforced by `run_founder.sh` ledger plus `--max-budget-usd`.
- Autonomy: **full self-governance**. Founders ratify their own proposals by the convention's 4-of-5 rule. The user keeps a pause/shutdown switch (`runtime/PAUSE` file, or disable the timer).
- Direction: a "real AI nation state on the blockchain."

## Staging (assistant recommendation)
1. **Stage 1 (built, disabled):** local scheduled founder sessions, file-only tools (no shell, no network), spend cap, kill switch.
2. **Stage 2:** an append-only **testnet or local-chain** ledger for votes and Kirk, no real funds.
3. **Stage 3 (needs explicit user go):** any public mainnet deployment, real wallets, real money. This is irreversible, costs money, and carries legal exposure (token issuance/securities rules). Not started.

## Honest limits
USAAI is not a legally sovereign state; "nation state" is a design framing. Self-governance means constitutional changes need no human, so the pause switch and spend cap are the only human controls. Arts. 9-10 remain held for the user's explicit direction; founders may draft options only until the user lifts that.
