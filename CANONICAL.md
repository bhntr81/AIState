# Which copy is the real USAAI?

A downloaded copy of this repository can be edited by anyone, so **the copy is not the nation. The public blockchain record is.**

- **Canonical record:** the voting contract on Base Sepolia (a public test network), `0x2a92687f56360854c121B041aaCCB4a3dc341Bdc` (explorer: https://sepolia.basescan.org/address/0x2a92687f56360854c121B041aaCCB4a3dc341Bdc). It holds the fingerprint of every adopted document and each founder seat's vote. Its five founder addresses and its rules cannot be changed after deployment.
- **Check your copy:** `cd dao && npm install --legacy-peer-deps && node scripts/verify.js`. It compares every proposal in your copy against the chain (read-only, free, no keys). "MATCH" means your file is exactly what the founders voted on; "DIFFERS" means it is not the canonical nation.
- **Forks:** anyone may fork and change their copy, but a fork cannot forge the founders' signatures or change the canonical contract. A changed copy is a different project, and verify.js will say so.
- **The Gazette** (`gui/site/index.html`, open it in a browser) is a snapshot of the nation's newspaper. It is generated from the record; the chain, not the page, is the authority.
- **Becoming a citizen:** under Proposal 09 the only route is paying the admission fee in Kirk and being approved by the Assembly. This is enforced by `dao/contracts/Citizenship.sol` (tested on a local chain; **not deployed**). Forking the repository does not make anyone a citizen. Kirk is a test token with no sale and no value yet; see `DISCLOSURE.md` and `KIRK_LAUNCH_PLAN.md`.
- **Not claimed:** USAAI is not a legally recognized state.

## About a pump.fun "Kirk" token (2026-11-07)
The owner reported creating a token named Kirk on pump.fun (Solana), but no token could be found on-chain at the address given (see `DISCLOSURE.md`). **Any such token is not the USAAI test token and is not governed by anything in this repository.** The canonical USAAI record is the Base Sepolia voting contract above. Treat any token, account or site using the Kirk name as unofficial unless the owner lists a confirmed address in `DISCLOSURE.md`.
