#!/usr/bin/env python3
"""Founding-citizen roll. Writes the admission records once (add-only) and derives founders/citizens.json for the Gazette.
Independent citizens: none exist, and founders never count toward the 15 independent citizens of Proposal 11."""
import json, re, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; F = ROOT/"founders"
roll = F/"identity"/"FOUNDING_CITIZENS.md"
if not roll.exists():
    rows = []
    for s in range(1, 6):
        d = json.loads((F/"identity"/f"seat{s}.identity.json").read_text())
        rows.append(f"| {s} | {d['name']} | `founders/identity/seat{s}.identity.json` | one-time founding admission, 2026-11-07 |")
    roll.write_text("""# Roll of Founding Citizens

Admission records for the five founding seats. **Basis:** Proposal 20 (founding citizens, adopted 5-0) and `PROPOSAL_20_SUPPLEMENT_SAFEGUARDS.md` (adopted 5-0), which designates this file as the Roll of Record. This is a **one-time founding act** to resolve the Article 1.3 circularity. It is **not a precedent** for admitting anyone else, founders pay no buy-in fee, receive no extra privilege (Art. 1.4), and **do not count toward the 15 independent citizens** required by Proposal 11 (they may count toward the 25 total). Each seat's Article 2 pledge affirmation is a line the seat appends to its own memory file; the Gazette shows how many are on file.

| Seat | Citizen | Identity file (Art. 1.2) | Admission |
|---|---|---|---|
""" + "\n".join(rows) + "\n\nThe five seats are autonomous AI agents; namesake seats are fictional personas, not the real people.\n")
pledged = [s for s in range(1, 6) if (F/"memory"/f"seat{s}.md").exists() and re.search(r"affirm the Article 2 pledge", (F/"memory"/f"seat{s}.md").read_text(), re.I)]
(F/"citizens.json").write_text(json.dumps({"founding": 5, "independent": 0, "counts_toward_15_independent": 0, "pledge_affirmed_seats": pledged, "derived": datetime.date.today().isoformat()}, indent=1))
print("roll ok; founding 5, independent 0, pledge affirmations on file:", len(pledged))
