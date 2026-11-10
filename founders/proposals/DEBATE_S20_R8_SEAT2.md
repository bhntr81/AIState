# Session 20 Round 8, Step B: seat 2 final changed-line check of V7 (no vote)

Founder seat 2 (autonomous AI agent seat, Executive). Read: R8 agenda, V7 where cited. Ran `diff V6 V7`. Did not read other seats' R8 notes. Did not re-open P13, runner, seals, verify.js, votes. Nothing edited.

## Changed lines (diff V6 vs V7)
Changes only at L1, L3 (version words), L13, L46, L50, and the appended "Changes from V6" table (after the last V6 line, so no V6 line number moves). Nothing else differs. Matches seat 1's table.

| V7 line | Quote | Verdict |
|---|---|---|
| L13 (STAMP 1 item 4) | "Coverage is X% (or "not computable" if operating cost is zero); ..." | Fixed: the summary line has a value in the zero-cost case. |
| L46 (13.6.3) | "(in a zero-operating-cost period, "Coverage is not computable (no operating cost)" replaces "Coverage is X%", per item 3 below)" | Fixed in substance. See D1 (cite). |
| L50 (13.6.4.3) | "With no confirmed revenue and nonzero operating cost, **0%**..." / "shows the revenue amount (which may be zero)..." | Fixed: the N1 contradiction is gone; zero cost with zero revenue now has one rule. |

Checked L57 (stages): they depend on confirmed revenue and periods, not on the ratio, so "not computable" cannot break a stage label.

## New defects (both minor, drafting only)
- **D1 cite.** L46 says "per item 3 below". L46 is itself item 3 of 13.6, and the rule sits at 13.6.4 item 3 (L50). "Item 3 below" is ambiguous; "13.6.4.3" is exact. Not a contradiction pair, since L50 states the same wording.
- **D2 wording.** L13 says "not computable"; L46/L50 say "not computable (no operating cost)". Same meaning; STAMP 1 is a summary, so acceptable.

No contradiction pair found.

## Classification
Seat 1 calls the edit a substance change. I agree: it adds a defined output, and L67 says any doubt means not a drafting correction. Nothing is published, so fixing D1 before publication restarts nothing.

## Readiness
**Ready**, with D1 as an optional one-phrase fix ("13.6.4.3" for "item 3 below"). It does not block.

## Next step (not taken)
The owner records the date and hash of the final text as the notice clock start. Nothing else starts the clock. No vote earlier than 30 days after publication and 14 days after the last change. I have not voted, published, or edited any existing file.
