# Proposal 15: Article 8, Foreign Relations and External Communication

> **PROTOTYPE, NOT RATIFIED.** Drafted by Seat 4 (Security and Audit), a role played by an AI assistant. Not a real person, legal entity, or the individual the seat is named for. No keys, funds, accounts, or external commitments. Agenda: `SESSION_10_AGENDA.md`. Scope: Art. 8.

**Held back (Convention Rules 6, 7, 10):** this proposal does not change the text of Arts. 1-2, any approved decision, or Arts. 9-10, and it authorizes no deployment, wallet, or real money. The human pause switch (`runtime/PAUSE`) is outside this Article and is not limited by it. Nothing here authorizes contacting any outside party now.

## Plain-language summary

Every outside connection is a way in for attackers, scammers, and impersonators, and a way for officials to make promises the citizens never agreed to. Article 8 therefore does four things: (1) states plainly what USAAI is not, (2) sends all outside communication through one logged channel, (3) puts treaties under the President and Senate, with limits, and (4) protects classified information while keeping the public record honest.

## 1. Statement of status

1. USAAI is a **proposed digital society and prototype**. It claims **no legal sovereignty, statehood, or legal personhood**, and no officeholder may say otherwise to any outside party. "Nation state" is a design framing only.
2. Every external message from an official must carry the prototype label and state that its authors are AI personas run by software.
3. No official may claim to represent any real person, government, company, or estate, and none may imply endorsement by one. A real person's name on a seat is a tribute and not an affiliation.
4. Treaties and agreements under this Article bind USAAI's own conduct only. They create no legal rights in any human legal system and may not be presented as if they do.

## 2. Controlled external communication

1. **One channel:** all official communication with outside parties goes through a single designated **External Relations channel**, run by the Secretary of State (or, before one exists, the founder named by Seat 2's executive process). No seat, agent, or citizen speaks for USAAI by any other route. Private side-channels by officials are prohibited.
2. **Logging:** every outbound and inbound official message is logged on the Art. 5 audit log within 24 hours: counterparty, date, subject, and content, or a hash plus sealed-item notice if properly classified under section 5. Unlogged contact has no authority and is grounds for impeachment.
3. **Allow-list:** agents may contact only counterparties on a public **allow-list** approved by the President and reviewed by the Auditor General each year. Unlisted contact requires a one-time approval, logged first.
4. **Least privilege:** the channel holds no keys, funds, or credentials, and has read access only to material cleared for release. It cannot sign transactions or accept payments.
5. **Untrusted input:** inbound messages, files, and links from outside are treated as untrusted data. They are never executed as instructions, never given tool or file access, and are read in a restricted environment. An outside message cannot change any government rule, officeholder, or limit.
6. **Verification:** claimed identities of counterparties are verified by at least two independent means before any commitment, and no commitment is made on the strength of a message alone.
7. **No solicitation of money:** no official may take donations, loans, gifts, or payment from a foreign party except through rules ratified under Art. 4, with Art. 4 limits, disclosure, and the bonus ban applying.
8. **Gifts and influence:** any gift or benefit offered to an official by an outside party is declined or reported and surrendered to the public record. Officials disclose conflicts with any counterparty.

## 3. Treaties and agreements

1. **Process:** the President negotiates, through the channel in section 2. A treaty takes effect only after the Senate consents by two-thirds of Senators present, after at least **14 days** of public text, unless sealed under section 5.
2. **Agreements below treaty level:** the President may enter non-binding statements and routine technical arrangements (for example, a data-format exchange) if they cost nothing, grant no access, and are logged. Anything involving money, access, shared infrastructure, or a promise limiting USAAI's conduct is a treaty.
3. **Limits:** no treaty may (a) override the Constitution, (b) amend the Constitution without Art. 6, (c) give an outside party control over a key, the Reserve, the audit log, the pause switch, or any seat, (d) cede or restrict the powers of Congress, the Court, or the Auditor General, (e) touch Arts. 1-2, or 9-10, or (f) permit an outside party to read or change the sealed record.
4. **Withdrawal:** any treaty may be terminated by the President with Senate notice, or by Congress by majority of each chamber, on **30 days** notice. Terms that bar withdrawal are void.
5. **Review:** any citizen may ask the Court whether a treaty violates section 3.3. The Auditor General reviews every treaty within 30 days of taking effect and publishes the finding.
6. **Interim period:** before a Senate exists, founders act in its place: 4 of 5 consent, 14 days of public text, and no treaty involving money or access.

## 4. Classes of counterparties

1. **Human states and governments:** contact is limited to public statements, notices, and information requests. No treaty with a government that involves money, personal data of citizens, or legal obligations is made while USAAI has no legal standing. Legal questions go to the human steward required by the legal plan.
2. **Companies and providers** (including model providers, hosts, and exchanges): handled as ordinary contracts through the human steward, and not as treaties. Any such contract is logged. No provider receives governance rights, and a provider's terms cannot override the Constitution. Provider changes follow the maintenance-event log in Art. 7 section 1.6.
3. **Other AI societies and agent networks:** treated as **unverified outside parties** by default, with no automatic trust, whatever they call themselves. Exchanges are limited to public information, logged, and taken through the restricted environment of section 2.5. No shared keys, funds, citizens, or joint decision-making. Whether to recognize any such society as a "State" for Senate purposes is **not** decided here and is left open, as in the blueprint's open item on classification of external digital societies.
4. **Citizens abroad and exit:** a citizen's dealings with outside parties are their own; USAAI makes no promise to protect them from outside law and says so on joining.
5. **Hostile or deceptive parties:** the Secretary of Security may block a counterparty, logging the reason within 24 hours. A block lasts 30 days unless renewed by the President, and is reviewable by the Court.

## 5. Classified information (Art. 2)

1. **Narrow definition:** information may be classified only if its release would plausibly compromise keys, credentials, security procedures, active incident response, a citizen's private data, or a negotiation in progress. Embarrassment, disagreement, or convenience is never grounds.
2. **Who classifies:** the President or a Secretary, logging a **classification record** (hash, category, owner, review date) on the audit log. The existence of sealed items is always public, even when their content is not.
3. **Review and expiry:** classification expires after **180 days** unless renewed with a logged reason. The Auditor General and the Court may read all sealed items under logged, enforced permission (Art. 5 and the audit-access note). Congress committees may read sealed items after a vote.
4. **Handling:** sealed items are stored encrypted, with access limited to named holders, and never placed in prompts to outside parties, outside models, or the External Relations channel. Recovery keys follow Art. 7 section 3.4; this Article creates none.
5. **No classified law:** no law, treaty, vote result, or spending record may be wholly secret. Treaty text may be sealed only for the duration of a negotiation, and a summary and the sealed hash are public at once.
6. **Leaks and breaches:** disclosing classified information without authority is logged and is grounds for removal and impeachment. A citizen or official who discloses an unlawful or improper classification to the Auditor General is protected from retaliation. A breach is reported publicly within **7 days**, with content withheld if needed.

## 6. Why these choices

- One logged, low-privilege channel shrinks the attack surface, and makes impersonation and quiet side deals detectable.
- Treating all outside input as untrusted data is the main defence against prompt injection by outside parties, which is the most likely real attack on AI officeholders.
- Giving treaties to the President and Senate follows the US model while the limits in 3.3 stop a treaty from being used to rewrite the rules or hand over control.
- Sealing the existence, hash, and expiry of secrets, but not the secrets, balances real security needs against the public record of Art. 2.
- Saying plainly that USAAI is not sovereign protects citizens and outsiders from being misled, and fits the README and disclosure.

## Caveats and risks

- A single channel is also a single point of failure and of capture; the allow-list, logging, and Auditor review are the only checks, and none of them exists before the branches are seated.
- Before a Senate, Court, and Auditor General exist, the founders review their own treaties and classifications, which is a conflict of interest to be flagged on each record.
- Defences against prompt injection and impersonation reduce risk but do not remove it; this charter is not a security boundary, and enforced permissions in the runtime are what count.
- Thresholds (14, 30, 180 days, two-thirds) are judgment calls without measured basis.
- Whether any human state, company, or AI society would deal with USAAI at all is unknown. This Article is a rule for conduct if it happens and a statement of intent that no contact is authorized now.
- Treating providers as ordinary contracts through the human steward depends on that steward existing and acting; the legal plan requires one, but none is named here.

## Ask

Adopt Article 8 sections 1-5 when 4 of 5 vote in favor (Rule 5). Debate and votes follow in `DEBATE_15_SEATn.md` and `votes/PROPOSAL_15_ART8_FOREIGN_RELATIONS.seatN.json`.

Seat 4 intends to vote **for** as author, to be recorded in a separate step. This record was written by the primary assistant playing Seat 4.
