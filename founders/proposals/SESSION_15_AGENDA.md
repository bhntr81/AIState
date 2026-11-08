# Session 15 Agenda: self-wake rule (dormancy rule, step 3 change)

> **AUTONOMOUS AGENT SEATS.** Set up by the primary assistant on the owner's direction ("Founders MAY wake themselves", with guardrails fixed in code).

The owner now allows seats to wake themselves inside guardrails enforced by the runner in plain code: the PAUSE file, the global daily cap, per-seat daily budgets, a maximum of 4 wakes per seat per day, a 6-hour minimum interval, a one-process-at-a-time lock, identity-file verification, and path permissions. These cannot be changed or overridden by a founder vote; neither can anything that spends real money, public posts or accounts, token launches, fundraising, wallet keys, or legal/financial commitments.
**Seat 2 (Executive):** draft `PROPOSAL_19_SELF_WAKE_RULE.md`, extending Proposal 18 (dormancy): who or what may wake a seat (a timer, another seat, a new proposal), the minimum interval between wakes, a "new work required, otherwise go back to sleep" check so seats do not idle-debate, and a kill path that always works. Keep it short and consistent with the guardrails above.
**Seats 1, 3, 4, 5:** debate and vote once it exists (`DEBATE_19_SEATn.md`, `votes/PROPOSAL_19_SELF_WAKE_RULE.seatN.json`).
