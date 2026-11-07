# Kirk Launch Runbook (Base mainnet): READ BEFORE ANY REAL MONEY

**State 2026-11-07: prepared, NOT launched.** Nothing below has been run on a real network. This is a *contract deployment* runbook. It does **not** include any sale, listing, or fundraising. Not legal advice.

## What the user must have before launching
| Item | Why | Status |
|---|---|---|
| Hardware wallet (about $70+) set up, 24 words on paper | Holds the keys; signs the deployment | [ ] |
| About $20 of ETH on **Base** in that wallet | Gas for 3 contracts (Reserve, Kirk, Treasury) | [ ] |
| Founders' final amounts in `dao/params.json` (`finalizedByFounders: true`) | Amounts are immutable after deploy | [ ] placeholders now |
| Independent contract audit | Contracts are unaudited; a bug can lose funds permanently | [ ] |
| Legal advice + entity + named human steward | Securities / money-transmission exposure | [ ] |
| `KIRK_LAUNCH_PLAN.md` section 2 gates met | Written go from the user | [ ] |

**Do not send real value to these contracts until the audit and legal items are done.** Deploying the contracts alone (no sale) is the lowest-risk step; it still costs real gas and puts the name Kirk on a public chain.

## Steps (run on your own machine, from `dao/`)
1. **Rehearse on the free testnet first** (Base Sepolia): get test ETH from a Base Sepolia faucet, then
   `LEDGER_ADDRESS=0xYOURADDR npx hardhat run scripts/deploy.js --network baseSepolia`
2. **Mainnet**, with the Ledger plugged in, unlocked, Ethereum app open:
   `CONFIRM_MAINNET=I_HAVE_READ_KIRK_LAUNCH_PLAN LEDGER_ADDRESS=0xYOURADDR GOVERNANCE_ADDRESS=0xYOURADDR GUARDIAN_ADDRESS=0xYOURADDR npx hardhat run scripts/deploy.js --network base`

| Part | Meaning |
|---|---|
| `CONFIRM_MAINNET=...` | A deliberate typed switch; the script refuses mainnet without it |
| `LEDGER_ADDRESS` | Your hardware-wallet address; Hardhat asks the device to sign, so the key never leaves it |
| `GOVERNANCE_ADDRESS` | Who may admit citizens and reward contribution (use a multisig later) |
| `GUARDIAN_ADDRESS` | Who can pause issuance (the human kill switch); best a *different* address from governance |
| `npx hardhat run scripts/deploy.js` | Runs the deploy script with the project's Hardhat |
| `--network base` | Targets Base mainnet (chain id 8453); `baseSepolia` is the test network |

3. The script writes `dao/deployments/base.json` (addresses). Verify the contracts on BaseScan and record the addresses in the README.
4. Confirm on-chain: supply is 0, `governance` and `guardian` are your addresses, params match `params.json`.

## Built-in safeguards
- Mainnet is blocked unless the confirm switch, finalized params, and both addresses are set.
- Only the Reserve can mint; the Treasury cannot. Issuance is rate-capped per epoch; the guardian can pause.
- No AI agent holds a key. Agents only vote in files; nothing they do moves funds.

## Not covered (needs the user or professionals)
Audit, legal review, entity formation, any token sale or exchange listing, marketing text (use `DISCLOSURE.md` wording only), tax reporting.
