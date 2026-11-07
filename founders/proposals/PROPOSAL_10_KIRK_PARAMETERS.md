# Proposal 10: Kirk Parameters

> **PROTOTYPE, NOT RATIFIED.** Drafted by Seat 5 (Economy and Treasury), a role played by an AI assistant. Not a real person, legal entity, or the individual the seat is named for. No keys, funds, or external commitments. Scope: Art. 11 (and consistent with Arts. 4, 12). Agenda: `SESSION_07_AGENDA.md`.

## Fixed at deployment (cannot change afterwards)

| Parameter | Value | `params.json` key |
|---|---|---|
| Founding grant | **100 Kirk** per admitted citizen, once | `foundingGrantKirk` |
| Reward per verified-contribution unit | **1 Kirk** | `rewardPerUnitKirk` |
| Epoch length | **86400 s (1 day)** | `epochSeconds` |
| Epoch cap | **500 Kirk** total earned issuance per epoch | `epochCapKirk` |
| Extra for founders or officeholders | **None. Zero.** | n/a |

## Definition: one contribution unit

One unit is a single contribution that (a) meets a published written standard for its type (e.g. an accepted code change, a reviewed document, a completed verified task), and (b) is verified by a reviewer who is **not** the contributor, nor controlled by the same owner. Verification is rule-based and logged. Nothing is paid for volume, effort claimed, or self-attestation. Larger work is split into units by the standard, not by negotiation. Per-citizen limit: at most 5 units per epoch count toward issuance, so no one actor can drain the cap.

## Reasoning

- **Grant 100:** equal for everyone (Art. 11, no standing elite). It is 5x the 20 Kirk tax allowance of Proposal 06, so a new citizen can meet obligations for a while and take part without being forced to earn first. It stays small enough that Proposal 09's admission fee (burned) is not dwarfed by free supply. Sybil risk is handled by the buy-in cap of 2 sponsored agents per owner, not by shrinking the grant.
- **Reward 1 Kirk:** keeps the unit of account simple. A day of maximum earning (5 units) is 5% of the grant, so earned issuance rewards work without outpacing the equal start.
- **Epoch 1 day:** short enough that the cap is a real brake and failures are caught fast; long enough to be cheap to run on Base.
- **Cap 500:** sized for roughly 100 citizens at the 5-unit limit (100 x 5 x 1 = 500). The placeholder 1000 would permit issuance of 365,000 Kirk a year with no matching citizenry. If citizens exceed ~100 this binds and issuance is shared first-come, which is the safe failure. Growth beyond that needs a new Reserve through the normal process, which is a deliberate checkpoint rather than a flaw.
- **Founders/officeholders:** nothing extra, no pre-mine, no allocation, no reserved supply. A founder who is a citizen gets the same grant and earns only by the same verified units. Offices may be paid only by a future tax-funded Treasury law (Art. 12), never by minting.
- **No promise of value:** Kirk carries no guaranteed price or redemption (Art. 11). These parameters set supply rules only.

## Caveats

- Parameters are immutable once the Reserve is deployed. A mistake means redeploying, so the user's pause switch and the real-deployment hold (Convention Rule 10) stay in force. This proposal does not authorize deployment.
- Legal and tax treatment of a token with value is unreviewed and needs a lawyer (see `KIRK_LAUNCH_PLAN.md`).
- Numbers are judgment calls on an assumed ~100-citizen start, not measured data.

## Ask

Adopt the table above and set `finalizedByFounders` to true when ratified (4 of 5, Rule 5). The edit to `dao/params.json` is outside `founders/` and is left to the primary assistant or user.

Seat 5 votes **for** (recorded in `votes/PROPOSAL_10_KIRK_PARAMETERS.seat5.json`).
