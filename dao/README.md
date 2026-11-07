# USAAI Founders DAO (prototype, local chain only)

Hardhat project. `contracts/FoundersDAO.sol` encodes the convention rules: 5 founder seats, 4-of-5 to adopt, a guardian pause switch. It holds no funds and has no token. Tests run on Hardhat's in-process chain: `npm install --legacy-peer-deps && npx hardhat test` (4 passing on 2026-11-07).

Not deployed anywhere. Testnet or mainnet deployment, wallets, and any token need a separate explicit user go and legal advice (see `../runtime/RUNTIME_AND_GOVERNANCE.md`). Not audited; do not use with value.

## Founder bridge
Founder agents vote by writing `founders/votes/<proposal>.seat<N>.json`. `npx hardhat run scripts/bridge.js` replays all proposals and vote files onto a fresh local chain and prints each result. The files are the source of truth; the chain is a deterministic replay (local chains reset on restart). Votes arriving after a proposal closes are shown as not counted.

## Stage A: Kirk token (local chain, no value)
`Kirk.sol` (minimal ERC-20, only the Reserve can mint), `Reserve.sol` (Art. 11 issuance rule: equal founding grant per citizen, earned issuance, per-epoch cap, guardian pause), `Treasury.sol` (holds tax Kirk, no mint power). Amounts are placeholders. Tests: `npx hardhat test` (10 passing). Not audited, not deployed. Governance is a single address here; wiring it to FoundersDAO execution is a later step. See `../KIRK_LAUNCH_PLAN.md`.
