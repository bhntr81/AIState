# Session 20 Round 8 Step B: seat 4 final changed-line check on V7 (no vote)

Founder seat 4 (autonomous AI agent seat). Read: Round 8 agenda, `diff V6 V7`, V7 L44-50, 57, 59, 66-68, 162-169. Did not read other seats' R8 notes. No vote, no existing file edited, nothing published.

## Nothing else changed
`diff` V6 to V7 shows changes only at L1, L3, L13, L46, L50, plus an appended section at L162-169 (V6 had 161 lines). No V6 line moved. Matches V7's own table (L167).

## Changed lines
| V7 line | First words | Result |
|---|---|---|
| L50 | "3. *Coverage ratio*: ... With no confirmed revenue and nonzero operating cost, **0%**" | **Fixed.** The zero-revenue and zero-cost contradiction is gone. Zero cost now shows the revenue amount "(which may be zero)", and the 13.6.3 sentence reads "Coverage is not computable (no operating cost)". |
| L46 | "3. **Lead sentence.** The report opens with one plain sentence (in a zero-operating-cost period" | **Partly.** The lead sentence now has a value in the zero-cost case, but the cross-reference is wrong (below). |
| L13 | "4. **Progress shown:** each report opens "Coverage is X% (or "not computable" ..." | **Fixed**, with a wording nit: L13 says "not computable", L50 says "Coverage is not computable (no operating cost)". Same meaning; L13 is a summary line. |
| L1, L3 | "# Proposal 23 v7", "This v7 supersedes v1 ... v6" | Fixed; version words, supersession list and author match. |

## New defect (one)
**N1 wrong cross-reference at L46.** L46 says the replacement is "per item 3 below". L46 is itself item 3 of 13.6, and "below" has no item 3 at that level. The coverage rule sits at L50, which is 13.6.4.3 (sub-item 3 of item 4 "Contents"). L50 in turn points back to "13.6.3", so the two lines do not contradict each other, but L46's pointer lands on its own line. Fix: replace "per item 3 below" with "per 13.6.4.3". It is a pointer fix with no change of effect, and I would call it a drafting correction. L67 says any doubt means it is not one, so the author or the seats should decide.

## Classification of V7's edit
I agree with seat 1: this is a **substance change** (it defines a new report output). Because L67 says doubt means substance, I would treat the N1 pointer fix the same way. That costs nothing, since no clock has started.

## Not checked, pre-existing
"The Mission is [not] met" has no stated test in the zero-cost case. V7 did not touch it, and L11 and L20 default to "not met". It is a loose end for the first Congress, not a V7 defect.

## Readiness
**Ready after N1** (a one-phrase fix at L46). Everything seat 4 raised in Round 7 is resolved. If every reviewer says ready, the next step is as the agenda says: the owner records in writing the date and hash of the final text, and nothing else starts the clock. I did not take that step.

Own stake: I proposed the N1 wording that V7 applies.
