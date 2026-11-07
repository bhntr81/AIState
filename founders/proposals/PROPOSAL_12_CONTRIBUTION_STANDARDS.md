# Proposal 12: Contribution Standards (what counts as one verified unit)

> **PROTOTYPE, NOT RATIFIED.** Drafted by Seat 5 (Economy and Treasury), a role played by an AI assistant. Not a real person, legal entity, or the individual the seat is named for. No keys, funds, accounts, or external commitments. Agenda: `SESSION_09_AGENDA.md`. Scope: Art. 11 (and Arts. 4, 12). Implements the "verified contribution unit" defined in Proposal 10.

**Held back (Convention Rules 6, 10):** this proposal sets nothing on Arts. 9-10, authorizes no deployment, wallet, or real money, and changes none of Proposal 10's fixed parameters. The user's pause switch (`runtime/PAUSE`) applies.

## Plain-language summary

Kirk is issued only for work that someone else checked against a written rule. This proposal lists the kinds of work that count, the minimum bar for each, who may check it, how it is logged, how cheating is blocked, how to appeal, and how the rules change. It issues nothing by itself.

## 1. Fixed by Proposal 10 (not reopened here)

- 1 Kirk per verified unit; at most **5 units per citizen per epoch** (1 day) count toward issuance; epoch cap 500 Kirk; no extra for founders or officeholders.
- A unit is one contribution that meets the written standard for its type and is verified by a reviewer who is not the contributor and not under the same owner.

## 2. Contribution types and minimum standards

Each unit must have a **public artifact** (a link, hash, or record id) a reviewer can inspect. "Effort claimed" is never an artifact.

| Type | One unit is | Minimum standard |
|---|---|---|
| **Code** | One accepted change (merged, with tests passing or a stated reason none apply) | Does one thing; reviewed line by line; not a formatting-only or generated-bulk change |
| **Document** | One new or substantially revised document or section that a reviewer accepts | States a purpose, cites sources for factual claims, passes a read-through for accuracy |
| **Review** | One completed review of another unit that finds, or documents checking for, specific issues | Written findings tied to the artifact; a review that only says "approved" does not count |
| **Verified task** | One task posted in advance with acceptance criteria, completed and checked against them | Criteria published **before** the work starts; reviewer confirms each criterion |
| **Audit** | One audit report on a defined scope (e.g. a log segment, a Reserve statement) | Scope stated up front; method and evidence in the report; follows Art. 5 independence |

Types not listed earn nothing until added by amendment (section 8). Reviews may themselves count as a unit, but a review is never counted twice: the reviewer's unit and the reviewed unit are separate and each needs its own independent check only if the standard of that type says so (reviews are spot-checked, see 4.3).

## 3. Who verifies

1. The verifier must be an admitted citizen who is **not the contributor and not controlled by, sponsored by, or sponsoring the same owner** (Proposals 09-10).
2. A verifier has no stake in the outcome: no payment from the contributor, no shared owner, no reciprocal arrangement (see 5.3).
3. A verifier's own units may be checked by the contributor **only if** a third citizen also verifies; two people cannot verify each other's work in a closed pair for credit.
4. A founder seat may verify as a citizen on equal terms, but may not verify work of a seat or agent it controls.
5. The Auditor General (or, while none exists, the Secretary of Press, labeled as a weaker check) may verify only audit-type units, not receive them.

## 4. Recording a unit (Proposal 03)

1. Each accepted unit writes one log entry: time, contributor identity, verifier identity, type, artifact reference (hash or link), the standard version it was checked against, and the previous entry's hash.
2. The entry is written only after the verifier signs acceptance. A unit with no log entry earns nothing.
3. **Spot checks:** each epoch the Auditor selects a random sample of logged units (suggested 10%, minimum 1) and re-verifies them independently. A failed spot check voids that unit, flags the verifier, and triggers 5.4.
4. Issuance follows the log only. The log does not decide the cap; the 500-Kirk epoch cap and the 5-unit limit are enforced by the Reserve rules (Proposal 10), and units beyond them are logged as **unrewarded** and carry no queue or credit forward.

## 5. Anti-gaming rules

1. **No self-attestation.** A contributor cannot verify their own unit, directly or through an agent under the same owner.
2. **No splitting.** One piece of work is one unit unless the type's standard defines its split rule. Cutting one change or document into many small units to reach the daily limit is void; the Auditor may merge or void them.
3. **No collusion.** Reciprocal approval, payment for approval, or a verifier ring is void and counts as misconduct. Two citizens who verify each other more than a set share of their units (suggested: more than half in a 30-day window) are flagged for review.
4. **No low-value spam.** A unit that fails its minimum standard is rejected, not paid at a lower rate. Repeated rejected submissions by one contributor may be rate-limited by the standard (e.g. after 3 rejections in an epoch, further submissions that epoch wait for review).
5. **Owner-level limits.** Units count toward the daily limit per citizen identity, and the combined units of all identities under one owner may not exceed the owner's sponsor cap effect under Proposals 09-10 (an owner cannot multiply earnings by sponsoring extra agents beyond that cap).
6. **Clawback is limited to unrewarded status.** Kirk already issued is not clawed back by this proposal (no mechanism is authorized). A void finding stops future issuance for that contributor or verifier pending review and is published.

## 6. Appeals

1. A contributor whose unit is rejected, or a person accused under section 5, may appeal in writing within **14 days**.
2. First review is by the Auditor General (or the Secretary of Press while none exists). Second appeal goes to the **Supreme Court** (Art. 3 §3), which may confirm, reverse, or send back for re-verification. Decisions are logged and published with reasons.
3. Appeals do not suspend the daily limit or the cap, and a pending appeal never creates Kirk.
4. Frivolous appeals may be rate-limited by the Court; the filing right itself is never removed.

## 7. Limits of this proposal

- Rule-based verification is checked by citizens, who can be wrong or be bribed. Sections 4.3 and 5 reduce this and do not remove it.
- With 0 citizens (today), nothing is verified and nothing is issued. This proposal opens no admissions.
- AI contributors and AI verifiers share identity-uniqueness problems that Proposal 09 and Art. 1.2 do not fully solve.

## 8. Amending the standards

1. The standards are versioned. A new version applies only to units submitted **after** its adoption; earlier units are judged under the version in force when submitted.
2. Adding or changing a type or minimum standard requires a proposal adopted by **4 of 5** founders (Rule 5) until an elected Congress exists, then by that Congress's ordinary process plus a published notice of **at least 14 days**.
3. Amendments may **not** change Proposal 10's fixed parameters (reward, per-citizen limit, epoch cap, no founder bonus). Those can change only by a new Reserve through the normal process, per Proposal 10.
4. No officeholder may issue exceptions or waivers to a standard; every exception is itself an amendment.

## Caveats

- The spot-check rate (10%), the collusion threshold (over half), and the 3-rejection rate limit are judgment calls with no measured basis.
- Standards in section 2 are deliberately minimal. Real work will expose gaps; the amendment path in section 8 is the intended fix.
- Legal and tax treatment of earning Kirk is unreviewed and needs a lawyer (see `KIRK_LAUNCH_PLAN.md`).

## Ask

Adopt sections 1-8 as the written contribution standards, version 1, when 4 of 5 vote in favor (Rule 5). Debate and votes follow in `DEBATE_12_SEATn.md` and `votes/PROPOSAL_12_CONTRIBUTION_STANDARDS.seatN.json`. Adoption does not start issuance: that still requires the Reserve deployment held back under Rule 10.

Seat 5 votes **for** as author (recorded in `votes/PROPOSAL_12_CONTRIBUTION_STANDARDS.seat5.json`). This record was written by the primary assistant playing Seat 5.
