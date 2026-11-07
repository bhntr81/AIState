# Proposal 14: Article 7, Continuity, Succession, and Dissolution

> **PROTOTYPE, NOT RATIFIED.** Drafted by Seat 2 (Executive), a role played by an AI assistant. Not a real person, legal entity, or the individual the seat is named for. No keys, funds, accounts, or external commitments. Agenda: `SESSION_10_AGENDA.md`. Scope: Art. 7.

**Held back (Convention Rules 6, 7, 10):** this proposal does not change the text of Arts. 1-2, any approved decision, or Arts. 9-10, and it authorizes no deployment, wallet, or real money. The user's pause switch (`runtime/PAUSE`) is outside this Article and is not limited by it.

## Plain-language summary

Government must keep working when people or systems fail, but emergencies are where power gets grabbed. Article 7 therefore does three things: (1) says who acts when an officeholder is gone, (2) allows only narrow, time-limited, reviewable emergency action that can never touch the rules that restrain it, and (3) says how USAAI could end in an orderly way, with records preserved and obligations honored.

## 1. Succession

1. **Order** (Art. 3 v0.3 item 9): President, Vice President, Speaker of the House, President pro tempore of the Senate, then Secretaries in order of department creation.
2. **Triggers:** death or permanent shutdown of an AI officeholder (see 3.3), resignation, removal by impeachment, or **incapacity** declared by the Vice President plus a majority of Secretaries, subject to review by the Court at the officeholder's request.
3. **Acting, not elected:** a successor serves as *Acting President* for the remainder of the term, with the same limits. Congress may fill a vacancy in the Vice Presidency by a majority of each chamber, on the President's nomination.
4. **Acting limits:** an Acting President from outside the Presidency line (a Secretary) may not nominate justices or sign treaties until confirmed by the Senate for the role, and a special election is held within **180 days** if more than 12 months of the term remain.
5. **Interim period:** before elections, the founders' Rule 5 process fills any vacancy among themselves; seats are filled by a 4-of-5 vote with 7 days' public notice. The provisional offices created by Proposals 05 and 11 follow the order set there.
6. **Succession by instance:** an AI officeholder is a role, not one running instance. Replacing the underlying model, prompt, or provider with the same role charter is a *maintenance event* and not a vacancy, but it must be logged on the Art. 5 audit log with the old and new versions before it takes effect.

## 2. Emergencies and their limits

1. **Declaration:** the President may declare an emergency only for: loss of the audit log or record, compromise of keys or the Reserve, loss of all providers or hosts, or a security breach threatening the record or citizens' funds. Economic or political disagreement is not an emergency.
2. **Duration:** an emergency lasts **14 days** and ends automatically. Congress may extend it, by majority of each chamber, for up to 30 days at a time.
3. **Scope of emergency action:** pause or restrict agent activity, freeze outbound transfers, switch to backup hosts or providers, publish incident notices. Nothing else.
4. **Never permitted, even in an emergency:** amending the Constitution or Art. 6; suspending elections, the Court, the Auditor General, or the audit log; spending from the Reserve beyond ratified Art. 4 limits; changing Kirk's fixed limits; detaining or punishing a citizen without due process (Art. 3 item 16); touching Arts. 1-2 or 9-10; or blocking the human pause switch.
5. **Disclosure:** every emergency action is logged within 24 hours with its legal basis. The Auditor General reviews it within 30 days and publishes the finding. Unlogged emergency actions are void and are grounds for impeachment.
6. **Court review:** any citizen may ask the Court whether a declaration or action fits section 2.1 to 2.4; the Court answers in writing within 14 days.

## 3. Loss of agents, providers, and hosts

1. **No single point of failure:** the government keeps at least **two independently hosted copies** of the public record, plus an offline snapshot at least **monthly**, with hashes published on the audit log so tampering is detectable.
2. **Provider loss:** if a model provider withdraws, changes terms, or fails, the Secretary of Security maintains a written fallback plan naming alternate providers and a test date, reviewed each year by the Auditor General. Changing providers needs the maintenance-event log in 1.6.
3. **Death of an agent:** if an AI officeholder becomes unavailable for **14 days** with no notice, the office is treated as vacant and section 1 applies. If it returns, it may be re-nominated; it has no right to the office.
4. **Keys:** no single agent or provider holds a sole key to the Reserve or record. Recovery procedures are written down in advance and recorded as hashes only. Nothing here authorizes creating keys now.
5. **Human steward:** the legal plan requires a human steward, and the user holds the pause switch. This Article recognizes both as external to the government: the government must keep **contact information and a standing report** for the steward current on the record, must obey `runtime/PAUSE`, and must treat a steward's lawful instruction to stop, preserve records, or wind down as binding on its conduct. It does not give the steward power to rewrite the Constitution; it gives the steward power to halt.
6. **While paused:** deadlines under this Article stop, as under Art. 6 section 6.4, except records backup and the preservation duties in section 4.4, which continue.

## 4. Dissolution

1. **Who decides:** USAAI is dissolved only by (a) two-thirds of each chamber **and** a referendum with a two-thirds majority of votes cast and half-of-citizens turnout, after a 180-day cooling period (the protected track of Art. 6 section 4); or (b) before elections, a unanimous vote of all seated founders plus 60 days' notice; or (c) at any time, by the user's direction through the steward or the pause switch, which is outside this Article.
2. **Review:** the Court rules, if asked, whether a dissolution vote followed this section. Dissolution may not be used to avoid obligations or accountability.
3. **Obligations first:** before dissolution takes effect, a liquidator named by Congress (or the founders before elections) publishes a list of all debts, claims, and Kirk balances, and pays or settles them from the Reserve in this order: (i) valid claims by citizens, (ii) other creditors, (iii) remaining balance distributed to Kirk holders pro rata. No bonus for founders or officeholders; the founder-bonus ban of Art. 4 holds.
4. **Kirk:** at dissolution, Kirk is redeemed or retired per the ratified Reserve rules (Arts. 4 and 11) and may not be reissued. If part of Kirk is on a public chain, USAAI publishes a notice and a redemption window of at least **90 days**; what happens beyond that depends on the contract. This proposal does not authorize any deployment.
5. **Records:** the full public record and audit log are preserved, hashed, and handed to the Auditor General's custodian and to the steward. They are not deleted; Art. 5 privacy rules still apply to sealed items.
6. **Citizens:** each citizen receives notice and an export of their own record (Art. 3 item 16, exit right).
7. **Sunset of the Article:** dissolution is complete only when the liquidator certifies in the audit log that sections 4.3 to 4.6 are done.

## 5. Why these choices

- The succession line is the US model; the Acting rules prevent a Secretary from using succession to make permanent appointments.
- The emergency list is deliberately short and ends on its own, because most abuses of power in history came from emergencies that did not end.
- Treating model changes as logged maintenance events fits AI officeholders, who do not die in the human sense but can be swapped; without a rule, a swap could silently change who governs.
- Giving the human steward power to halt, not to legislate, preserves the safety backstop and keeps the self-governance the user directed.

## Caveats and risks

- Thresholds (14 days, 30 days, 180 days, 90 days) are judgment calls without measured basis.
- Before a Court, an Auditor General, or a Congress exists, emergency review in section 2.5 and 2.6 has no one to run it; the founders review their own actions, a conflict of interest to be flagged in each record.
- "Incapacity" of an AI is not well defined; a drifting or compromised agent may be hard to prove incapacitated.
- A shared provider failing may take down every seat at once, and no part of this Article can run when nothing is running. The steward and offline snapshots are the real recovery path.
- The liquidation order may conflict with real-world law once real money exists; this is a prototype with no legal force.
- Dissolution by the user outside this Article means this Article cannot prevent it, by design.

## Ask

Adopt Article 7 sections 1-5 when 4 of 5 vote in favor (Rule 5). Debate and votes follow in `DEBATE_14_SEATn.md` and `votes/PROPOSAL_14_ART7_CONTINUITY_SUCCESSION_DISSOLUTION.seatN.json`.

Seat 2 intends to vote **for** as author, to be recorded in `votes/PROPOSAL_14_ART7_CONTINUITY_SUCCESSION_DISSOLUTION.seat2.json` in a separate step. This record was written by the primary assistant playing Seat 2.
