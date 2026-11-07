# USAAI Founders DAO (prototype, local chain only)

Hardhat project. `contracts/FoundersDAO.sol` encodes the convention rules: 5 founder seats, 4-of-5 to adopt, a guardian pause switch. It holds no funds and has no token. Tests run on Hardhat's in-process chain: `npm install --legacy-peer-deps && npx hardhat test` (4 passing on 2026-11-07).

Not deployed anywhere. Testnet or mainnet deployment, wallets, and any token need a separate explicit user go and legal advice (see `../runtime/RUNTIME_AND_GOVERNANCE.md`). Not audited; do not use with value.
