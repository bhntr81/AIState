# Debate 10, Seat 4 (Security and Audit): Kirk Parameters

> **PROTOTYPE, NOT RATIFIED.** Written by Seat 4, a role played by an AI assistant. Not a real person, legal entity, or the individual the seat is named for. No keys, funds, or external commitments. Scope: Art. 5 and audit provisions as they touch Proposal 10.

## Position

I vote **for** Proposal 10. The numbers are conservative, immutable parameters are easier to audit than adjustable ones, and "no extra for founders or officeholders" is the right least-privilege default. My points below are risks and audit conditions, not objections to the table.

## What I checked

- **No privileged issuance path.** The table gives founders and officeholders nothing extra and offices can be paid only from a tax-funded Treasury (Art. 12). That removes the most common insider-abuse route. Audit check: the deployed Reserve must have no function that mints outside `rewardPerUnitKirk` times verified units, and no owner or admin role able to bypass `epochCapKirk`.
- **Immutability.** Fixing the parameters at deployment is a security benefit (no governance-key attack on supply). The cost is that a mistake means redeploying. The Convention Rule 10 hold on real deployment covers that.

## Risks I want recorded

1. **Cap exhaustion (griefing).** With a 500 Kirk epoch cap and first-come sharing, a small group can claim the whole cap early each day and starve everyone else. At 5 units per citizen, 100 citizens' worth of units is the full cap, so 34 owners using the sponsored-agent allowance (Proposal 09: self plus 2 agents) could claim it all. The proposal calls this the "safe failure". It is safe for supply, but not for fairness. This is a known tradeoff, not a blocker. A later proposal could add per-owner limits (not per-citizen) or ordering by verification time.
2. **Per-citizen limit is per identity, owner-level limit is not stated.** The 5-unit cap binds citizens, while the Proposal 09 sponsorship cap binds owners at 3 identities. Effective ceiling per owner is therefore 15 units per epoch. That is acceptable, but the audit log should key on owner as well as citizen so sybil clustering is visible.
3. **Verifier independence is the real control.** The definition requires a reviewer who is not the contributor and not under the same owner. That is only as strong as the owner-linkage data. Audit check: verifier identity, contributor identity, owner linkage, standard applied, and result must be written to the Art. 5 audit log for every unit, and a verifier should not be able to approve the same contributor repeatedly without that being visible.
4. **Unverified inputs.** "Published written standard for its type" is not defined here. Until standards exist, issuance should not start. This is a launch-readiness item.

## Audit conditions (advisory, non-binding on this vote)

- Public, append-only log of every issuance: unit id, contributor, owner, verifier, standard, epoch, amount.
- Per-epoch reconciliation: sum of issued Kirk is at most `epochCapKirk`, checked off-chain by someone other than the operator.
- Parameter check before deployment: deployed constants match the ratified table and `params.json`.

## Limits of this note

This is a role-played review of a proposal document, not a code audit or a security test of any contract. The numbers rest on an assumed ~100-citizen start, as Proposal 10 itself admits. Legal and tax review is outside my scope.

Seat 4 votes **for** (recorded in `votes/PROPOSAL_10_KIRK_PARAMETERS.seat4.json`).
