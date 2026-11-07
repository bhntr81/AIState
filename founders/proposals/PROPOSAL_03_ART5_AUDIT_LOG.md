# [Founder 4 draft] Art. 5, audit log integrity: status **Proposed**

> **PROTOTYPE, NOT RATIFIED.** Drafted by an AI role-playing Founder 4 (Security and Audit). Not a real person, not a vote of real people. Nothing here is implemented. Only the user can ratify; other seats have not yet voted.

Builds on `NOTE_ART5_AUDIT_ACCESS.md`. Seat 4 already voted for Proposals 01 and 02; no further vote is needed there.

1. *Append-only log.* Every government action that moves Kirk, changes a permission, or changes a record writes one log entry: time, actor role, action, target, and the hash of the previous entry (a hash chain), so any edit or deletion breaks the chain visibly.
2. *Independent copies.* The chain head is copied at a fixed interval to at least two holders who are not officials of the branch being logged. Holders compare heads; a mismatch is reported to the Auditor and published.
3. *Enforced, not promised.* Write access to the log is by a narrow service permission. No official role has delete or edit rights. Permission changes are themselves log entries.
4. *Auditor access.* Read-only, via a logged permission. The Auditor cannot alter the log or the records it audits.
5. *Findings.* Published on a fixed schedule; the audited body may append a written response but may not edit the finding.
6. *Review.* Log design is reviewed independently before use, and re-reviewed after any incident.
7. *Limits.* A hash chain shows tampering; it does not prevent bad entries or collusion among all holders. This reduces risk and does not guarantee security.
8. *Deferred.* Hash algorithm, copy interval, holder selection, publication schedule, classified-material handling (Art. 2).

**Debate request:** Seats 1-3 and 5, please state objections or cost concerns (especially item 2's burden on small early deployments).

**Vote (role-played):** Seat 4 for (author). Others pending.
