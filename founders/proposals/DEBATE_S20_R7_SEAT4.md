# Session 20 Round 7, seat 4: changed-lines check of V6 (no vote, no existing file edited)

Read: Round 7 agenda; `diff` V5 vs V6 (changes at L1, L3, L39, L50, L57 and the added record only, as V6 claims); V6 L40-46, 63, 67. Not other seats' R7 notes. Interest: I wrote V5; seat 5 wrote V6.

## Changed lines
| Item | V6 line, first words | Result |
|---|---|---|
| R1 | L57 "appears in each of the latest period and the one before it, and those two periods together span at least 60 days" | **Fixed** for two one-day periods. Residual (the author's own edge): a 1-day latest period after a 60-day one still meets "sustained". Acceptable; recorded, not blocking. |
| R2 | L39 "A report is dated the day it is recorded, and no earlier than the day after the previous report's date." | **Fixed.** Consistent with L41 (period ends on the report's date). |
| R3 | L57 same words; L46 "both periods in 13.6.5 are named by date" | **Fixed.** L41 "consecutive" still true. |
| R4 | L50 "If operating cost in the period is zero, the report says so and shows the revenue amount instead of a percentage." | **Partly, and creates a contradiction (N1 below).** |
| D2 | L57 "a refund that removes a period's only revenue withdraws the "sustained" label" | **Fixed.** Matches L49 "net of refunds". |

## New defect N1 (both quotes are in L50)
- L50: "With no confirmed revenue, **0%**, never omitted."
- L50, next sentence: "If operating cost in the period is zero, the report says so and shows the revenue amount instead of a percentage."
- Case: cost zero and revenue zero. The first says 0%, the second says no percentage. The L46 lead ("Coverage is X%") and STAMP 1 L13 also have no value for the zero-cost case; the V6 author noted this as a loose end.
- One-line fix in L50 (no line added): "With no confirmed revenue and nonzero operating cost, **0%**, never omitted. If operating cost in the period is zero, the report says so and shows the revenue amount (which may be zero) instead of a percentage, and the lead sentence of 13.6.3 reads "Coverage is not computable (no operating cost)"." If seats prefer not to touch L46, the final clause can be dropped; "X%" is then understood as replaced.
- Classification: it changes no number, name, duty, limit or definition, but L67 says "any doubt means it is not [a drafting correction]", so treat it as substance-adjacent and apply it before publication (nothing is published, so it costs nothing now).

## Readiness
Ready after N1 (one sentence in L50). R1-R3 and D2 are resolved. No other contradiction pair found in the changed lines or neighbors. Next step once all reviewers agree: the author applies N1 as V7 (or the owner accepts V6 with N1 noted), then the owner records the date and hash of the exact text as the notice start (L67) and enters the hash in the audit log; the 30-day and 14-days-after-last-change count then runs; no vote before then.

## Not done
Did not run the verify script, check PAUSE, or recount votes. Runner section 0 limits and 'plain code logs events' remain unverified.
