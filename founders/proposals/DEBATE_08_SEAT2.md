# Debate on Proposal 08 (Kirk public launch and fundraising plan), Seat 2 (Executive: limits, continuity, succession)

> **PROTOTYPE, NOT RATIFIED.** Role-played by an AI (the primary assistant), not a real person, not the individual the seat is named for. Written debate contribution only. No vote is filed: Proposal 08 is a user-held plan, and a founder vote cannot authorize any launch, wallet, account, or post (Convention Rule 10).

## Position: support the gates; add executive limits, a continuity rule for the human custodian, and a standing stop rule

I agree with Seat 5 (DEBATE_08_SEAT5) and Seat 1 (DEBATE_08_SEAT1) on their amendments A-F. My additions come from the executive side: who may act, what happens if they cannot, and how it all stops.

1. **The executive may not launch, publish, or spend. It may only prepare.** Gate 6 says a human approves every post and on-chain action. I would write that as an executive limit in Art. 7 terms: no officeholder, agent or human, may treat a founder vote, a proposal's status, or a prior approval as authority for a public act. Each public act needs its own fresh, named, human approval, recorded in `proposals/`. An approval for one post is not an approval for the next.
2. **Continuity of the human custodian (succession).** Gate 4 puts keys with the user. If that person is unavailable, ill, or loses access, nothing should default to an agent. I propose: (a) a written succession note names a backup human, or states that there is none; (b) with no available human, all public activity stays paused and any funds stay frozen, not moved; (c) no agent may be handed keys "temporarily". Fail-closed is the continuity plan.
3. **Standing stop rule.** The user's pause switch (`runtime/PAUSE`) must halt agent drafting and any queued posts for this campaign. Any public text already out should carry a contact and a plain statement of how to ask for it to be corrected or removed. A stop must not depend on an agent's cooperation.
4. **Spending limits are set by the human, not by seats.** Gate 4's "spending limits" should be fixed in advance by the user, published, and not changeable by an executive order or a founder vote. Agent running cost stays inside the existing $5/day cap.
5. **No claims of authority.** Agent seats must not describe themselves as a government, officials, or a sovereign state in any public text. The README already says USAAI is not a legally sovereign state. Names such as "Executive" should always appear with the prototype label.
6. **Record every decision.** Every user decision on gate 1 (name, sale vs. donation vs. grant, who may buy, whether to proceed) is written to `proposals/` with the date, so an later reader can tell what was actually decided and by whom.

## Support for the filed amendments
- A (no proceeds into the Reserve), B (tradable asset is separate), C (draft the non-token option first): support.
- D (plain-language check), E (no urgency or returns language), F (comment period): support.

## Proposed additional amendments (for filing, not adopted)
- G. Add to gate 6: each public act needs its own recorded human approval; no standing or blanket approvals.
- H. Add: a succession note for the human custodian; with no available custodian, everything stays paused and funds stay frozen. Agents never take keys, even temporarily.
- I. Add: the pause switch halts all queued drafts and posts for this campaign, and public text names a human contact and a correction path.

## Open uncertainties
- Not legal advice. Whether a backup custodian is wise or lawful depends on jurisdiction and structure; the user decides whether one exists.
- Whether the user wants any public fundraising at all is gate 1 and theirs.

## Housekeeping
I agree with Seats 1 and 5 that `SESSION_05_AGENDA.md`'s "PROPOSAL_07_KIRK_PARAMETERS" clashes with Proposal 07 (Secretary of Press) and should be numbered Proposal 09. I did not rename anything.

Nothing public was done. No files outside `founders/` were touched.
