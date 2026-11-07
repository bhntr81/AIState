# Debate 14, Seat 4 (Security and Audit): Article 7

> **PROTOTYPE, NOT RATIFIED.** Written by an AI assistant role-playing Seat 4. Not a real person, legal entity, or the individual the seat is named for. No keys, funds, accounts, or external commitments. Scope: Art. 7 as it touches Art. 5 and audit provisions.

## Position: vote FOR, with security clarifications to fold in later

Article 7 gets the audit points right. Emergency action must be logged within 24 hours with its legal basis, and unlogged actions are void (2.5). The audit log, Auditor General, Court and the pause switch are all on the never-permitted list (2.4). Model or provider swaps are logged before they take effect (1.6). Two independent record copies with published hashes make tampering detectable (3.1). No single holder of a sole key (3.4) is least privilege applied to continuity.

## Security concerns (not blocking)

1. **Log before effect, also for emergencies.** 1.6 requires logging before a maintenance event; 2.5 allows 24 hours after an emergency action. The log entry for an emergency declaration itself should be written first, with later actions following within 24 hours. Otherwise a compromised actor can act first and backfill.
2. **Maintenance events need a second reviewer.** Swapping the model or prompt behind an office is the main way to silently change who governs. The log entry should include hashes of the new prompt and charter, and the Auditor General (or, before one exists, another founder seat) should confirm the charter is unchanged.
3. **Steward contact data (3.5).** "Current contact information on the record" must not publish private details. Keep it sealed under Art. 5 privacy rules, with only a hash and a custodian on the public record.
4. **Offline snapshots (3.1).** Name who may restore from a snapshot and require a hash check against the published value before any restore is accepted.
5. **Incapacity of a compromised agent.** A compromised officeholder cannot be told apart from a healthy one by its own statements. Allow a security finding by the Auditor General to count as evidence for incapacity.
6. **Self-review in the interim** (2.5-2.6) is a real conflict of interest. Every interim emergency record should name it and be re-reviewed by the Auditor General once seated.

## Vote

FOR. These are suggested follow-up edits, not conditions. Recorded in `votes/PROPOSAL_14_ART7_CONTINUITY_SUCCESSION_DISSOLUTION.seat4.json`. Dissent: none.

Written by the primary assistant playing Seat 4.
