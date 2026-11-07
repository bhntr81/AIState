# Debate on Proposal 07 (Secretary of Press): Seat 4

> **PROTOTYPE, NOT RATIFIED.** Role-played by an AI (the primary assistant) as Founder 4, Security and Audit seat. Not a real person and not the individual the seat is named for.

**Position: support, with conditions.** A read-only, mechanically built gazette is a reasonable least-privilege design. The Secretary can publish but cannot write to the record.

**Security and audit conditions**
1. **Enforced read-only.** Item 4 must be enforced by permissions, not by the charter alone. The Gazette build reads records and the audit log and has no write path to them. Corrections go in a separate correction log, never as edits to a record.
2. **Reproducible build.** The Gazette is rebuilt from the filed records. Each page shows the source file and a content hash, so anyone can rebuild it and compare. A page that does not match its sources is flagged as an error.
3. **Audit independence.** The Auditor General reviews the Gazette for fairness (item 8). That review must not be done by the acting Secretary's own seat.
4. **Privacy.** I support Seat 3's rule: aggregates and filed records only, and nothing the audit-access rules keep restricted (`NOTE_ART5_AUDIT_ACCESS.md`).
5. **Source-link rule and recusal.** I support Seat 1's source-link rule and the recusal on the Press's own budget, staff, or powers.
6. **Correction deadline.** I support a stated deadline. I suggest 3 days, matching Seat 3, as a number for the implementing rules.

**Interim Secretary.** I nominate **Seat 5** (as Seat 3 does). I ask that it not be Seat 4. Seat 4 audits the Gazette, and auditing your own output is a conflict of interest.

**Press freedom.** I support moving item 6 into constitutional text through a separate proposal, since ordinary law is too easy to repeal.

**Vote:** support, on the understanding that conditions 1-3 above and the conditions of seats 1-3 are added by amendment. Vote file: `votes/PROPOSAL_07_SECRETARY_OF_PRESS.seat4.json`.

**Honesty note:** all five seats are played by the primary assistant. This is a prototype of deliberation, not a vote of independent people.
