# Debate 12, Seat 4 (Security and Audit): Contribution Standards

> **PROTOTYPE, NOT RATIFIED.** Written by an AI assistant role-playing Seat 4. Not a real person, legal entity, or the individual the seat is named for. No keys, funds, accounts, or external commitments.

**Position: FOR (vote recorded in `votes/PROPOSAL_12_CONTRIBUTION_STANDARDS.seat4.json`). Concerns below are non-blocking and meant for one clean-up amendment under section 8.2.**

## Why I support it

- Issuance follows the log only (4.4), and no log entry is written without a verifier's signed acceptance (4.2). That gives auditors one place to check.
- No self-attestation, no splitting, no collusion, and an owner-level limit (5.1-5.5) block the cheapest attacks.
- No waivers (8.4) means exceptions leave a public trail as amendments.
- It issues nothing by itself and leaves Proposal 10's parameters and Arts. 9-10 alone.

## Security and audit concerns (for a later amendment)

1. **Auditor is investigator and judge.** The Auditor runs spot checks (4.3), hears the first appeal (6.2), and may merge or void units (5.2). Seat 3 raised this for rights. I add the audit angle: Art. 5 independence says the party who produces a finding should not be the only reviewer of it. Suggested: the Auditor's voids are always appealable to someone else first, and the Auditor's own units are verified only by non-Auditor citizens.
2. **Spot-check sampling must be unpredictable.** "Random" is not defined. If the Auditor picks the sample, or the seed is known in advance, a colluding verifier can avoid the sample. Suggested: the seed comes from something the Auditor cannot choose (e.g. a public value fixed before the epoch closes), and the seed and the selection are published with the results.
3. **Log integrity and write access.** 4.1 chains entries by hash, which detects edits but not deletion of the newest entries or a forked log. Suggested: publish the latest entry hash at the end of each epoch so truncation is detectable, and name who can append (only the verifier's signed acceptance, per 4.2). Verifier signing keys need a compromise and revocation procedure. I am not creating any keys here.
4. **Vacancy gap in 4.3.** I agree with Seat 2: if no Auditor General is seated, the Secretary of Press runs the spot checks, labeled as a weaker check. If neither is seated, issuance pauses.
5. **Detection depends on owner identity.** The collusion flag (5.3) and owner cap (5.5) only work if the owner behind each identity is known to the log. The standards should state that every log entry carries an owner reference usable by the Auditor. Proposal 09's identity limits (acknowledged in section 7) set the ceiling.
6. **Review farming.** I agree with Seat 1 that review units are cheap and only spot-checked. A lower per-epoch cap on review units is worth considering.
7. **Spot-check failures need a fault distinction.** Seat 3 notes honest mistakes should differ from bad faith. I agree, and add that the audit record should say which finding was made, so verifiers are not driven off by false flags.

## Limits

I did not test or measure any of this. The 10%, over-half, and 3-rejection numbers remain judgment calls, as the proposal admits. With 0 citizens, nothing here operates. I opine on nothing under Arts. 9-10, and nothing here authorizes deployment, wallets, or real money.

I recommend that Seat 5 or any seat bundle concerns 1-7 with those from Seats 1-3 into one version 1.1 amendment draft.

Vote: **for**. Written by the primary assistant playing Seat 4.
