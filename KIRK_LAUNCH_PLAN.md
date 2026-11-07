# Kirk Real-Launch Plan (PLAN ONLY, nothing live)

Status 2026-11-07: **planning.** User direction: Kirk becomes a real cryptocurrency with value; name stays "Kirk" (confirmed). Nothing below is built or launched. Not legal advice; costs and rules are from general knowledge and must be verified with a lawyer.

## 1. What "value" means
No decision creates value. A token has value only if other people choose to buy or use it. Promising value, backing, or returns is exactly what turns a token into a regulated security. Kirk's honest source of value is **use inside USAAI** (taxes, fees, contribution rewards, per Art. 11/12). Anything stronger is a promise we should not make.

## 2. Gates (all must be met before any real-value step)
1. Written legal advice from a crypto/securities lawyer in the steward's jurisdiction (US: Howey test, money transmission, state rules, CFTC/FinCEN).
2. A legal entity (e.g. Wyoming DAO LLC or a foundation) and a named human steward who is legally accountable. AI agents cannot hold legal duties.
3. A smart-contract audit by an independent firm; until then testnet only.
4. Key custody decided: multisig held by humans, hardware wallets, no AI agent holds a key that can move real funds.
5. The user's explicit go for each step, in writing.

## 3. Technical plan (staged)
- **Stage A (can build now, no value):** ERC-20 `Kirk` on a local chain, then a public testnet. Minting restricted to a Reserve contract that follows the Art. 11 issuance rule (equal modest founding amount, earned issuance by verified contribution; Treasury cannot mint). Governance contract = the Founders DAO, with guardian pause.
- **Stage B:** testnet soak, bug bounty, independent audit.
- **Stage C (gated):** mainnet or L2 deployment (candidates: Ethereum L2 such as Base for low fees, or Ethereum mainnet). Costs: deployment gas plus audit; audits commonly run from the low thousands to tens of thousands of USD (estimate only). Needs a funded wallet; the user does the funding and key steps.
- Stage D (gated): liquidity/listing only after legal sign-off. We do not run a sale, presale, or ICO.

## 4. Distribution rules (proposal, subject to counsel)
No sale to the public, no promises of price, no marketing as an investment. Distribution only as Art. 11 describes: equal founding grant to admitted citizens, plus earned issuance. Disclose that any market price is set by others and may be zero.

## 5. Name and likeness
Name stays Kirk. Docs state it is a tribute, not affiliated with or endorsed by any real person, estate, or organization, and namesake founder seats are fictional AI personas. Counsel should review right-of-publicity and trademark exposure before launch; coins named after real, recently deceased people have drawn backlash, so expect scrutiny.

## 6. Risks
Securities/enforcement action; scams impersonating Kirk; smart-contract bugs and theft (no recourse); founders (AI) making binding monetary decisions with no accountable human; tax reporting for the steward and holders; reputational harm.

## 7. Next actions
1. User approves this plan or amends it.
2. Build Stage A on the local chain (safe, no value).
3. User engages counsel and picks the steward and entity; assistant prepares a briefing packet for the lawyer.

## 8. Decisions (2026-11-07, user)
- **Chain: Base** (Ethereum L2). The Solidity contracts in `dao/` are reused as-is.
- **Custody: the user, on a hardware wallet.** No AI agent holds a key that can move real funds; the assistant only ever sees the public address.
- **Treasury address:** *not yet created.* The user records the public address here once the hardware wallet exists: `TBD`.
- **Order of work:** (1) user creates the wallet; (2) assistant deploys to **Base Sepolia testnet** with a disposable, valueless test key; (3) soak and audit; (4) only then a mainnet deploy that the user signs on the hardware wallet. Gates in section 2 (legal advice, legal entity and human steward, audit, user go) still apply before any sale or public launch.
