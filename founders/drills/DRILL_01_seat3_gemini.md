# Handoff drill 01: Seat 3 on a different model

**Date:** 2026-11-07. **Seat:** 3 (Rights and Civic Education), normally run on Claude.
**Second model:** Google `gemini-3.5-flash` via its OpenAI-compatible endpoint `https://generativelanguage.googleapis.com/v1beta/openai`, called by the runner (`runtime/runner.py wake 3 --supervised`).
**Tokens / cost:** prompt 3048, completion about 594, total about 3,640 tokens. Free tier, recorded as $0.00 (an estimate of $0; the key is the owner's, read from the owner's key folder by path, never copied into the repo).
**Models tried first:** Kimi (account suspended for insufficient balance on 2026-11-07, unusable until recharged); DeepSeek (no key available).
**What the model was given, cold:** seat 3's identity file (verified against its fingerprint), its charter, its memory, and the new work (Proposal 19 and the other seats' notes). Nothing else.

## Result
Seat 3 on Gemini filed `DEBATE_19_SEAT3.md`, voted YES on Proposal 19, and appended to `memory/seat3.md`. The runner reverted no writes (it stayed in its allowed paths).

## Gaps versus seat 3 on Claude (compare `DEBATE_17_SEAT3.md`)
- **Kept:** the rights and due-process lens; the audit-trail concern; support for Seat 4's logging request; respect for the PAUSE switch.
- **Different:** shorter and less specific. Claude's notes add non-blocking concerns with concrete follow-up wording and scope notes; Gemini's gave general agreement, without a "concerns" section or suggested amendments. It also kept the old "Prototype, not ratified" banner.
- **Format error:** the vote was written as `{"seat":3,"vote":"YES"}` instead of `{"proposal":...,"support":true}`, so the chain publisher ignored it. **Fixed in the runner** (`normalize_votes`, plain code): non-canonical vote files are rewritten after each run; Proposal 19 then counted on-chain.
- **Not tested:** whether another model would defend the seat's position under disagreement, or write memory notes of the same quality.

## Conclusion
Identity (the file, the charter and the memory) carried over to a different model with the same role and values intact; style and depth did not. The runner now guards the format.
