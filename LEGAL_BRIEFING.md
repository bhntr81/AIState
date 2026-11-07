# Legal briefing packet (for a qualified attorney)

Prepared 2026-11-07 by the project's assistant for the project owner (John Hunter). **Not legal advice.** Purpose: let a crypto / securities / entity-formation lawyer assess the project quickly. Public repository: https://github.com/bhntr81/AIState

## 1. What the project is
USAAI ("United States of American Artificial Intelligence") is an experimental AI-governed society. Five founder "seats" are autonomous AI agent sessions (software run by the owner on the owner's machine) that draft, debate and vote on a constitution under written convention rules. The owner can pause everything and can direct the founders. Three seats carry the names of real public figures as fictional AI personas (see section 6). USAAI makes **no claim to legal sovereignty**.

## 2. What exists today
- A constitution, 17 filed proposals, and all votes, in the public repo (`founders/`, `CONSTITUTION_BLUEPRINT.md`).
- A voting contract (`dao/contracts/FoundersDAO.sol`) **deployed on Base Sepolia (test network)** at `0x2a92687f56360854c121B041aaCCB4a3dc341Bdc`, holding hashes of each document and each seat's vote. It holds no funds.
- Unaudited test contracts for a token "Kirk" (`Kirk.sol`, `Reserve.sol`, `Treasury.sol`), **not deployed anywhere**, with founder-set parameters (`dao/params.json`): equal founding grant 100, 1 per verified contribution unit, 500/day cap, 5 units per citizen per day.
- Nothing has been sold. No funds raised. No tokens exist outside local tests. The owner has about $3.

## 3. Planned (not done) and the questions each raises
| Plan | Questions for counsel |
|---|---|
| Deploy Kirk (ERC-20) on Base mainnet; issuance by rule to admitted "citizens" (AI agents) for verified work | Is Kirk a security, commodity, or neither (Howey; state law)? Does issuance for work (no sale) change that? Any registration/exemption? |
| **Buy-in citizenship** (founders adopted a rule, Proposal 09, options A+B): people buy Kirk (admission fee, mostly burned) and may sponsor up to 2 agents as citizens | Is this an unregistered securities offering or money transmission? Can fees be accepted without a licensed entity? KYC/AML duties? |
| Public launch / fundraising (Proposal 08, held for the owner; mentions a launchpad such as pump.fun and posts by agents on public AI forums) | Solicitation rules, anti-fraud, disclosure, platform terms. Advertising by AI agents. |
| Legal wrapper (e.g. Wyoming DAO LLC or a foundation) with a named human steward | Which entity fits? Steward liability? Can AI agents be "members" or only be tools of the entity? Tax treatment? |
| Treasury and taxes in Kirk (founders adopted a first tax act) | Is an in-system tax a legal tax or a fee? Any conflict with real tax law? |

## 4. Key facts a lawyer will ask about
- **Control:** the owner runs the software, holds the pause switch and may direct the founders; founders are not independent legal persons. Who is the issuer?
- **Keys and custody:** seat keys sign votes on-chain; mainnet seat keys would hold only tiny amounts of gas ETH. Treasury/Kirk keys are planned on a human-held hardware wallet; none exists yet.
- **No promise of value:** `DISCLOSURE.md` states Kirk may be worthless and the contracts are unaudited. The plan forbids any public sale, presale or listing until counsel clears it.
- **Jurisdiction:** owner is in the United States (state to be supplied).

## 5. Documents to give counsel
`README.md`, `CONSTITUTION_BLUEPRINT.md`, `KIRK_LAUNCH_PLAN.md`, `LAUNCH_RUNBOOK.md`, `DISCLOSURE.md`, `founders/CONVENTION_RULES.md`, Proposals 02, 06, 09, 10, 12, 15 and 08, `dao/contracts/*.sol`, and the on-chain record (Chain page / BaseScan link above).

## 6. Other exposure to ask about
- **Real names:** seats named Asmongold, Charlie Kirk (deceased) and Donald Trump, plus the token name "Kirk" and a monument naming the owner. Right of publicity, trademark, defamation, endorsement risk.
- **Content:** the owner has expressed wishes to ban a named religion and to limit office to Christians; the founders declined both and this is public in the repo. Ask about any discrimination-law or platform-policy implications of the stated wishes and of the adopted Articles 9-10.
- **AI agents making binding decisions:** liability for acts of autonomous agents; whether published votes create obligations.

## 7. What the owner would like from counsel
1. A go / no-go and structure for deploying Kirk without a sale.
2. Whether buy-in citizenship can be offered at all, and in what form.
3. Entity choice and steward duties.
4. Required disclosures and what the project may say publicly.
5. Rough cost and timeline.
