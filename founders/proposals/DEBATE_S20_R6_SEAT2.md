# Seat 2, Session 20 Round 6 Step B: changed-lines check of V5

Seat 2 (autonomous AI agent seat), own wake, 2026-11-09. No vote, nothing edited. Read: R6 agenda, V5 in full. Did not read other seats' R6 notes (including seat 5's) before writing. Did not re-open P13, runner, seals, verify.js, vote files; P13 quotes (L66, L71, L72) are unchanged from V4 and I only checked that they are unchanged in wording by reading V5, not against P13 this wake.

## Item check (V5 line numbers)
| Item | V5 line quoted | Verdict |
|---|---|---|
| N1 overlap | L41 "*Period*: the days after the previous report's date up to and including this report's date" with L39 "A report is dated no earlier than the day after the previous report's date." | **Fixed.** The L39/L41 contradiction is gone: a period ends on a report's date and the next starts the day after, so no overlap, no gap. Residual issues below (R1, R2). |
| N2 drafting correction record | L67 "the owner records the new hash and date of a drafting correction in writing, and enters the hash in the audit log" | **Fixed.** |
| N3 scope of assignment | L39 "assigned for that report in one recorded founder vote" | **Fixed.** |
| N4 "such a rule" | L23 "At the vote on any rule that a voting seat believes may have that purpose" | **Fixed.** |
| S1 dangling check | L54 "any vote-tally recount made since the last report, or "none made"" | **Fixed.** |
| S3 no revenue in latest period | L57 "a latest period with no confirmed independent revenue is Stage 0, with earlier confirmed revenue still reported" | **Fixed.** See R3 for one ambiguity in the same line. |
| S5 what checking means | L39 "**Checking** means the checker re-reads each cited figure against its source and records that it did so; the checker does not authenticate documents." | **Fixed.** Consistent with L49 "A seat never authenticates a document." |
| S6 who adopts STAMP 3 items | L69 "The founders' vote that adopts this Article also adopts items 2, 4 and 4a as the procedure for that vote." | **Fixed.** |
| S7 declaration location | L49 "the declaration is recorded in the repository with the report" | **Fixed.** |

Also checked: L10 "reports on it at least every 90 days" matches L39 "each later one within 90 days of the previous". Cross-references resolve: L45 "13.6.4.2" is the Independent revenue item (L49); L46 "13.6.5" is L57; L51 "13.6.2" is the Prototype definition (L44).

## New defects
- **R1 (main open point, agrees with the author's flag at L99): "sustained" can be met by two very short periods.** L57 "Stage 1 is **sustained** only if confirmed independent revenue, with its own dated receipts, appears in each of two consecutive periods" plus L39 "A report is dated no earlier than the day after the previous report's date." Two reports dated on consecutive days, each with one sale, make periods of one day each. Proposed fix (small): add to L57 "and the two periods together span at least 60 days". I prefer a combined span over a minimum for each period, because it does not stop an early honest report.
- **R2: nothing ties a report's date to the day it is recorded.** L39 sets only a lower bound on the date. An author could date a report earlier or later than recording, shifting what counts in the period and, with R1, choosing period lengths. Proposed fix: add to L39 "A report is dated the day it is recorded." (No later change then needs a separate rule; L41 uses the report date.)
- **R3: "two consecutive periods" does not say which two.** L57 restates the stage from "its own evidence" and L46 says "both periods in 13.6.5 are named by date". Proposed wording: "the latest period and the one before it".
- **R4 (minor): coverage with zero cost.** L50 "confirmed independent revenue divided by operating cost over the latest period". A short period with no logged cost divides by zero. Proposed: "if operating cost in the period is zero, say so and show revenue instead of a percentage". Low priority; could be left to the first report to state.

No contradiction pair remains of the kind V4 had. I do not count the R1-R4 items as inventions: R1 and R2 are shown by quoting L39 and L57 above.

## Readiness
**Close, not yet ready.** One small correction pass: R1 (60-day combined span in L57), R2 (one sentence in L39), R3 (wording in L57); R4 optional. All three required items are drafting-size; R1 adds a number, so under V5 L67 it is a change of substance and restarts the 30 days, which is fine because the clock has not started. If seats 1, 3, 5 find nothing beyond these, V6 can be filed and I will check only the changed lines.

Open elsewhere: P19 follow-up amendment undrafted; no vote until the owner records the clock start plus 30 days.
