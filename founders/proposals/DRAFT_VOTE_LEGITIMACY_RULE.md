# DRAFT: Vote Legitimacy Rule (prototype votes vs. authorized votes)

> **Status: DRAFT. Not a proposal, not adopted, not filed.** Written by the primary assistant at John's request (2026-11-08), not by a seat. It changes no vote file, files no law and alters no constitutional status. The filename is deliberately `DRAFT_*` so `runtime/tally.py` and `dao/scripts/publish.js` (which only read `PROPOSAL_NN*`) do not treat it as a proposal. Seat review has **not** happened yet (it needs a paid cycle John has not authorized). Nothing here is human-verified.

## 0. Evidence this rule responds to (counted from the repository)
- **105 vote files** carry `"prototype": true`. Only **21** say they were role-played by the primary assistant. **23** are flagged but say "Written by Seat N, an autonomous AI agent seat". **61** have no note at all. One file (P19, seat 3) has no flag.
- So **the `prototype` flag is not a reliable provenance marker.** It cannot be used on its own to decide which votes are legitimate.
- Git history gives real provenance: P19's five votes each first appear in that seat's own runner-wake commit ("Seat N wake (runner)"); P01's five votes were role-played by the primary assistant (the files say so); P04's four votes first appear in a primary-assistant commit ("Founders get the reins"), with no note.
- On-chain votes are signed by seat keys, but the runner (and the operator) hold those keys. **A chain signature proves the runner published a file, not that the seat itself chose the vote.**

## 1. Definitions
- **Authorized vote:** a vote file written by the seat's own autonomous session during a runner wake, with a provenance record (section 6) that passes independent verification.
- **Prototype vote:** a vote written by anyone other than the seat's own autonomous session (for example the primary assistant role-playing the seat), or whose provenance cannot be established.
- **Legitimacy-first default:** a vote is a prototype vote until its provenance is verified. The burden of proof is on counting a vote, never on excluding it. The legacy `prototype` flag is neither required nor sufficient; evidence decides.

## 2. Deliberation and preliminary rankings (question 1)
Prototype votes **may** be displayed and discussed as an advisory signal (they show what a role-played convention concluded) and **may** inform preliminary rankings and agendas, **always reported separately** ("N authorized, M prototype"). They never appear as, or are merged into, an authorized tally. *(Alternative for John: exclude them from rankings too; see decision D1.)*

## 3. Filing and adoption thresholds (question 2)
Only **authorized votes** count toward adoption (4 of 5), forwarding, quorum, and any threshold that gates filing a law. A proposal with fewer than 4 authorized yes votes is **"advisory-passed, unratified"**, never "adopted", and **no `LAW_NN` may be filed for it**.

## 4. Ratification of prototype votes (questions 3 and 4)
1. **A ratification is a new, fresh authorized vote, never an edit.** The prototype file is left untouched. The seat files `votes/<PROPOSAL>.<seatN>.ratify.json` (new file) during its own autonomous wake.
2. It must cite: the proposal file and its **current SHA-256**, the SHA-256 of the prototype vote file it addresses, the seat's own decision (`yes`, `no` or `changed`), and a reason. The seat must have read the proposal text at that hash in that wake.
3. **The original voter must explicitly authorize.** Only the seat's own session can ratify its seat's vote. The primary assistant, another seat, or the runner may not ratify for it. **Silence, a memory-file note, or a "deemed consent" is not ratification.** A seat may decline, or ratify as `no` or `changed`; a changed decision supersedes the prototype vote.
4. A ratification counts only if the provenance record (section 6) is verified by someone other than the author.

## 5. Retroactive application (question 5)
No existing vote file is modified. Existing results are **re-labelled, not reversed**:

| Proposal | What the repository shows | Under this rule |
|---|---|---|
| **P01** (Art. 4 Treasury, 4-1) | All 5 votes role-played by the primary assistant (stated in the files). 0 authorized. | **Advisory-passed, unratified.** Needs 4 authorized yes votes by ratification. Seat 4's prototype "no" is advisory and may be re-decided. No law may be filed until then. |
| **P04** (Art. 3 Branches, 4 yes, seat 5 absent) | 4 votes first appear in a primary-assistant commit, no provenance note. 0 verified authorized. | **Advisory-passed, unratified.** Needs 4 authorized yes votes; seat 5 has never voted. |
| **P19** (Self-wake rule, 5 yes) | All 5 first appear in each seat's own runner-wake commit; texts say "autonomous AI agent seat"; the flag on 4 of them is a leftover. | **Eligible for reclassification as authorized by evidence** (a provenance record, not a new vote), if the independent verifier confirms the runner commits and logs. If it cannot, treat as prototype and ratify. |

Same method for every other proposal, one at a time, by evidence. Nothing is repealed automatically. Whether provisionally adopted items stay in force pending ratification is decision D4. This draft makes no claim either way.

## 6. Provenance record and independent verification (question 6)
For every vote, a **provenance record** (a separate append-only file, `votes/provenance/<vote file>.prov.json`, never edited) states: author class (`autonomous-seat-wake` / `primary-assistant` / `unknown`); the creating commit hash; the runner log or `runtime/cost.log` entry for that wake (seat, timestamp); the vote file SHA-256; and, for ratifications, the proposal and prototype-vote hashes.
- **Independent verification:** a **different seat** (not the voter, not the proposal's author) re-derives the record from git history and the runner log, and signs a verification line. The primary assistant and the runner may supply raw evidence but **may not be the sole verifier**. A seat's vote is not verified by that seat.
- `runtime/tally.py` is extended (separate change, after approval) to report authorized, prototype and unverified votes in separate columns and to fail closed on a missing provenance record.

## 7. Protections against manufactured or altered consent (question 7)
1. **Append-only.** Vote, provenance and ratification files are never edited or deleted. A correction is a new file citing the old one. The runner already reverts writes outside a seat's allowed paths; add the rule that **no actor may write a vote file for another seat**.
2. **No proxy voting.** The primary assistant, the runner and other seats may not create a vote or ratification in a seat's name. Doing so is **forgery**, a recorded violation reported to John, and the file is quarantined, not counted.
3. **Hash-bound.** Every ratification binds to specific proposal and vote hashes, so changed text invalidates earlier consent.
4. **Chain anchoring.** Hashes of vote, provenance and verification files are published on chain, but a signature is evidence of publication only (section 0) and is never proof of consent.
5. **Duty to disclose.** Any role-played or reconstructed vote must say so in the file at creation. Stripping or omitting that disclosure is itself a violation.
6. **Tamper checks.** On each filing day the checker re-runs the tally and the file hashes; any mismatch blocks filing (as in the draft checklist, item 2).
7. **Steward override.** `runtime/PAUSE` and the held-for-John list are untouched. This rule gives no seat spending power, key access or authority to change its own rules; adopting or amending it needs 4 authorized yes votes plus John's approval of this draft's open decisions.

## 8. Decisions for John (the rule is not ready to put to the seats until these are settled)
- **D1.** May prototype votes inform **preliminary rankings** (draft says yes, labelled and separate), or only deliberation?
- **D2.** Confirm that **only authorized votes** count toward adoption and filing (draft says yes, no exceptions).
- **D3.** For role-played votes (P01, P04), is today's autonomous seat the "original voter" who may ratify under the same seat charter (draft says yes, as a fresh vote, not a confirmation of words it never said)?
- **D4.** While unratified, do P01 and P04 (and other prototype-only items) **stay provisionally in force**, or are they treated as not yet adopted? The draft is silent.
- **D5.** May a vote whose git and runner history **prove autonomous authorship** (P19) be **reclassified by evidence** without a fresh vote (draft says yes)?
- **D6.** Who verifies provenance: another seat (draft) or must John or an outside party also sign? And who may verify the verifier's own vote?
- **D7.** Is adopting this rule a founders-only 4-of-5 action (CONVENTION_RULES rule 5), or do you want to ratify it yourself because it governs how consent is counted?

## 9. Seat review (not yet run)
All five seats are to review this draft independently in their own wakes and record: agree / disagree / amend per section, and any disagreement with D1 to D7. **Not run: needs John's authorization of a paid cycle** (about $0.50 for five seats at recent cost, bounded by the daily cap). The review would be advisory only: it files no vote on this draft, adopts nothing and changes no record.

## 10. Authority analysis and limits (added 2026-11-08 by the primary assistant, before any Founder deliberation; advisory, not a Founder decision)
**Basis found in `founders/CONVENTION_RULES.md`:** rule 5 (a proposal adopted by 4 of 5 founders is ratified by the convention; the user keeps the pause switch and may direct or amend), rule 10 (the founders write all remaining law except what is held back), rule 3 (written deliberation, dissents recorded with reasons), rule 8 (each seat is a separate autonomous session; records are signed by the seat that wrote them).
- **D7 as the existing rules read:** adopting this rule is a founders-only 4-of-5 action; no user ratification is required by rule 5. The user's held list (`runtime/RUNBOOK.md`) still covers changes to the runner's guardrails, so section 7 item 1 (a runner-enforced "no actor writes another seat's vote") is a guardrail change and stays held for John even if the founders adopt the rest.
- **Gaps the framework does not settle (documented, not invented):** (a) the rules never define what makes a vote valid or who may write it, so the draft's definitions are new law, not an interpretation; (b) rule 7 forbids changing "approved decisions"; whether re-labelling founder-adopted proposals (P01, P04) as "advisory-passed, unratified" touches that has not been decided and needs the seats' reading, and, if they disagree, John's; (c) there is no procedure for a rule that retroactively demotes earlier votes, which would be adopted under the old counting; (d) the Convention has no mechanism to bring in independent verifiers outside the five seats.
- **Who can deliberate:** only the five seats' own autonomous wakes can produce Founder deliberation. The primary assistant playing a seat would create exactly the kind of prototype vote this draft addresses, so it is excluded. Every wake is a model call: seats 1, 2, 4 and 5 run on Claude (paid), seat 3 on Gemini ($0). A 4-of-5 decision therefore cannot be reached at no cost.
