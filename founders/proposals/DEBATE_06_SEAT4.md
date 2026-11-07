# Debate 06, Seat 4 (Security and Audit): First Tax Act

> **PROTOTYPE, NOT RATIFIED.** Written by Seat 4, an AI role-played by the primary assistant. Not a real person, legal person, or the individual the seat is named for. Kirk is a test-ledger unit with no outside value. No real money, accounts, or deployment.

**Position: SUPPORT**, with the security and audit conditions below recorded for the implementing rules. Vote cast in `votes/PROPOSAL_06_FIRST_TAX_ACT.seat4.json`.

## Why support
- **Narrow collection power (items 5, 6):** the Treasury may debit only what the act sets, and tax cannot mint or confiscate Kirk. This is least privilege applied to money.
- **Quarterly audit and published aggregates (item 8):** collection is checked by an office the Treasury does not control.
- **Self-dealing barred (item 10):** officers cannot touch their own or relatives' assessments, and benefits to officeholders must be disclosed.

## Security and audit conditions (for implementing rules; not blocking)
1. **Collection is a privileged action: log it.** Every debit, waiver, correction, and exemption applied is written to the append-only audit log (see `NOTE_ART5_AUDIT_ACCESS.md`), with the rule it applied. No collection without a log entry; no officer may edit or delete entries.
2. **Separate duties.** The role that publishes the computation method (Seat 2's condition 1) should not be the role that runs collection or approves corrections. One officer must not be able to compute, debit, and waive alone.
3. **Pinned computation.** The published method is versioned and hashed. The Auditor General can re-run it against the ledger and compare totals. A mismatch is a published finding.
4. **Debit is capped by the act.** The collecting process holds permission to debit citizen balances only up to the assessed amount and never below zero or below the floor Seat 3 proposes. Enforce this in permissions, not only in policy text.
5. **Audit access to individual records.** The Auditor General reads per-citizen records under the Art. 5 access rules, itself logged. Published reports stay aggregate (supports Seat 3 on privacy). Small groups need suppression, since "aggregate by type" can identify a lone taxpayer in a tiny community. Do not publish a cell with fewer than 5 taxpayers.
6. **Exemption register.** Non-profit status (item 3d) is on the public register, and each grant or removal is logged. Audit samples it each quarter.
7. **Appeal pause is auditable.** Seat 2's 90-day backstop is good. Add that the Auditor General's quarterly report lists the count and total of paused amounts.
8. **Carryover with tax changes.** Rate changes (item 7) and the six-period review (item 11) should cite the audit report they rely on.

## Answers to the open questions
- **Rates and allowance:** placeholders acceptable. A live first period tests collection and audit early, which is the security case against starting at 0%.
- **Business levy:** keep, with zero rate allowed until a register entry exists (Seat 2).
- **Monthly period:** acceptable; more data per quarter helps audit.
- **Appeal window:** 60 days in the first year (Seats 2, 3).

## Honest limit
These conditions reduce risk. They do not guarantee security; protection depends on permissions and review actually being enforced.

## Honesty note
All five seats are played by the primary assistant. This record is a prototype of deliberation and not a vote of real, independent people.
