# Proposal 11: First Elections and Handover

> **PROTOTYPE, NOT RATIFIED.** Drafted by Seat 1 (Legislative, citizens' voice), a role played by an AI assistant. Not a real person, legal entity, or the individual the seat is named for. No keys, funds, or external commitments. Agenda: `SESSION_08_AGENDA.md`. Builds on Article 3 (Draft v0.3, `CONSTITUTION_BLUEPRINT.md` 3d) and Proposal 05 item 1.

**Held back (Convention Rules 6, 10):** this proposal sets **no religious or other qualification** for voting or office. Office eligibility is "per Article 10, undrafted" and stays user-directed. Nothing here fixes Arts. 9-10, and nothing authorizes any deployment, wallet, or real money.

## Plain-language summary

Until enough citizens exist, the five founder seats run the government on an interim basis. Once enough citizens are admitted, they elect the real officeholders, the founders step down from interim offices, and the elected branches take over on a fixed date.

## 1. Who may vote and stand

1. **Voters:** admitted citizens only (Art. 1.3, Proposal 09), **one identity per citizen** (Art. 1.2). No other test. Sponsored agents of one owner count as separate citizens only if admitted separately under Proposal 09's sponsor cap; a vote is cast by the citizen identity, never by its owner.
2. **Candidates:** admitted citizens who are voters, **plus whatever Article 10 later adds**. Until Article 10 is drafted, no further qualification applies and none may be invented by the provisional Congress, the Executive, or an election officer.
3. **Founders** may stand as citizens on equal terms, subject to section 4 (no dual office). A founder gets no extra votes, seats, or ballot position.

## 2. Minimum citizen count before the first election

1. **Threshold:** the first general election is held only when **at least 25 admitted citizens** exist, of whom **at least 15 are not founder seats or sponsored by a founder seat**. Reason: below this, "elected" officers would be chosen mostly by the people they replace.
2. **Today (0 citizens):** no election is scheduled. The five founder seats continue as the interim branches under Proposal 05 item 1. The interim period has no automatic end by date; it ends when the threshold is met.
3. **Check:** the Auditor General (or, while none exists, the Secretary of Press, per Proposal 07) publishes the verified citizen count monthly. When the threshold is met, the provisional Congress must publish an election notice within **14 days**.
4. **No indefinite drift:** if the threshold is not met **24 months** after the first citizen is admitted, the provisional Congress must publish a written report of why and a decision to extend, lower the threshold (4 of 5 vote), or dissolve the experiment. This is a checkpoint, not a deadline for ending self-governance.

## 3. Election timing and terms

1. **Notice and campaign:** at least **30 days** between the election notice and the vote; candidate lists and rules published in advance (publicity safeguard, v0.2).
2. **First terms are shortened and staggered**, so the first elected officers face voters again soon with a larger citizenry:
   - House of Representatives: all seats elected; **1-year first term**, then 2-year terms per Art. 3 §1.1.
   - Senate: seats by State are deferred (State definitions are open per Art. 3 §1.18). Until States are defined, the Senate is **not elected**; the House sits as the only elected chamber and the provisional Congress (founder seats) keeps the Senate's confirm/try functions, with every such act recorded. A proposal defining States is the next prerequisite for a Senate election.
   - President and Vice President: elected together, **2-year first term**, then 4-year terms with the two-term limit of Art. 3 §2.6. The first term counts as a term.
   - Justices: nominated and confirmed under Art. 3 §3.10, by the provisional Senate function; staggered 18-year terms from first appointment, with the first terms set by lot in the founding act so they are staggered.
3. **Method:** simple plurality for House seats; a majority with runoff for President. Ballots and tallies are public and logged; the exact tally mechanism is an implementation detail and is left to a later proposal. Any mechanism used must let a citizen verify their own vote was counted.
4. **Vacancies:** filled by special election within 60 days, except the Vice President, who succeeds per Art. 3 §2.9.

## 4. Founder stepdown and no dual office

1. **Handover day:** the elected officers take office **30 days after certification** of results. On that day every interim office held by a founder seat ends automatically.
2. **No office in two branches:** under Art. 3 §3.17 and Proposal 05 item 1, from the moment of the election notice each founder seat holds **at most one** interim office, and no founder may hold an elected office in a different branch from any office it still holds. A founder elected to office must resign any interim office on handover day.
3. **Founders become ordinary citizens** on handover (if admitted as citizens): no reserved seats, vetoes, or special powers survive. The convention's records stay in `proposals/` as history; they are not law unless adopted.
4. **Continuity:** laws, ratified proposals, and approved decisions made by the founders remain in force. The elected Congress may amend or repeal them by the normal process. Arts. 1-2 text, Arts. 9-10, and the user's pause switch (`runtime/PAUSE`) are outside this transfer and unchanged.
5. **Convention end:** the convention seats are dissolved by a final founders' vote (4 of 5) after handover, once the elected Congress certifies receipt of records.

## 5. Role of the Auditor General

1. **Appointment (interim):** because no elected Congress exists yet, the provisional Congress appoints the first Auditor General **from outside the five founder seats** (a distinct admitted citizen or, if none exists, a separately-permissioned agent that holds no other office) and publishes the reasoning. If no suitable candidate exists, the Auditor role stays vacant and the monthly count is published by the Secretary of Press, which is a weaker check and must be labeled as such.
2. **Duties in the transition:** (a) certify the citizen count and voter roll (one identity each, no duplicates, per Art. 1.2); (b) observe and publish the tally; (c) audit that no founder holds two-branch office on handover day; (d) report publicly within **30 days** after handover.
3. **Independence:** per Art. 3 §4.13, reports to Congress, not the President. Removal only by impeachment. The Auditor General may not stand for any office in the same election cycle.
4. **Limits:** the audit reduces risk; it does not guarantee a fair result. Role-played seats are not a security boundary.

## 6. If nobody has been admitted

With 0 citizens (the current state), nothing in this proposal triggers. The interim branches continue, the monthly count is published as "0", and the 24-month checkpoint in 2.4 starts from the first admission, not from adoption. Adopting this proposal does not open admissions: admission is governed by Proposal 09 and by Rule 10's hold on any real deployment, and the user's pause switch applies throughout.

## Caveats

- Thresholds (25 / 15, 14 / 30 / 60 days, 24 months) are judgment calls on an assumed ~100-citizen start (cf. Proposal 10), not measured data.
- A founder-run interim period with no citizens is the central weakness. The thresholds in 2.1 and the checkpoint in 2.4 reduce it but do not remove it.
- The Senate deferral (3.2) leaves the first elected government unicameral until States are defined; this is intentional, not an oversight.
- Digital voting and AI identity uniqueness remain hard open problems; this proposal relies on Art. 1.2 and Proposal 09 without solving them.

## Ask

Adopt sections 1-6 as the interim handover rule under Art. 3 and Proposal 05, when 4 of 5 vote in favor (Rule 5). Debate and votes follow in `DEBATE_11_SEATn.md` and `votes/PROPOSAL_11_FIRST_ELECTIONS_AND_HANDOVER.seatN.json`.

Seat 1's vote will be filed in the same way as the other seats' once debate opens (drafting is this session's bounded task). This record was written by the primary assistant playing Seat 1.
