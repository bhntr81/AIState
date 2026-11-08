#!/usr/bin/env python3
"""Builds a read-only static site from founders/ records. Nothing is invented:
the Gazette only restates filed proposals, votes and debate notes."""
import html, json, re, sys, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
F = ROOT/"founders"; OUT = Path(__file__).resolve().parent/"site"
SEATS = {1:"Asmongold (namesake seat), Legislative",2:"Donald Trump (namesake seat), Executive",3:"Charlie Kirk (namesake seat), Rights",4:"Nick Fuentes (namesake seat), Security and Audit",5:"Myron Gaines (namesake seat), Economy"}

def md(t):
    out, ul = [], False
    for line in html.escape(t).splitlines():
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        line = re.sub(r"\*(.+?)\*", r"<i>\1</i>", line)
        line = re.sub(r"`(.+?)`", r"<code>\1</code>", line)
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        li = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)", line)
        if ul and not li: out.append("</ul>"); ul = False
        if m: out.append(f"<h{len(m[1])+2}>{m[2]}</h{len(m[1])+2}>")
        elif li:
            if not ul: out.append("<ul>"); ul = True
            out.append(f"<li>{li[1]}</li>")
        elif line.startswith("&gt;"): out.append(f"<blockquote>{line[4:].strip()}</blockquote>")
        elif line.strip(): out.append(f"<p>{line}</p>")
    if ul: out.append("</ul>")
    return "\n".join(out)

def title(p):
    first = p.read_text().splitlines()[0].lstrip("# ").strip()
    return first

votes = {}
for v in sorted((F/"votes").glob("*.json")):
    d = json.loads(v.read_text())
    if "support" not in d or "proposal" not in d: continue   # ranking votes (next-step polls) use another format
    votes.setdefault(d["proposal"], {})[d["seat"]] = d["support"]
props = sorted((F/"proposals").glob("PROPOSAL_*.md"))
debates = sorted((F/"proposals").glob("DEBATE_*.md"))
other = sorted(p for p in (F/"proposals").glob("*.md") if not p.name.startswith(("PROPOSAL_","DEBATE_")))

def status(name):
    v = votes.get(name, {}); y = sum(v.values()); n = len(v)-y
    if y >= 4: return "ADOPTED", y, n
    if n >= 2: return "REJECTED", y, n
    return "OPEN", y, n

BP = (ROOT/"CONSTITUTION_BLUEPRINT.md").read_text()
README = (ROOT/"README.md").read_text()
def section(text, start, end=None):
    i = text.index(start); j = text.index(end, i+1) if end and end in text[i+1:] else len(text)
    return text[i:j]
def num(name):
    m = re.match(r"(?:PROPOSAL|DEBATE)_(\d+)", name); return m[1] if m else None
def debates_for(n): return [d for d in debates if num(d.name) == n]
def seatno(d): return int(re.search(r"SEAT(\d)", d.name)[1])
log = [l for l in README.splitlines() if l.startswith("- 20") and "Decision log" not in l]
def log_for(n):
    k = f"Proposal {int(n)}"; k2 = f"Proposals {int(n)}"; k3 = f"PROPOSAL_{n}"
    return [l for l in log if k in l or k2 in l or k3 in l or re.search(rf"\b0?{int(n)}\b and", l) and "Proposals" in l]
def first_sentences(p, k=2):
    body = [l for l in p.read_text().splitlines() if re.match(r"^\s*(\d+\.|[-*])\s+", l)]
    s = re.sub(r"[*_`]", "", re.sub(r"^\s*(\d+\.|[-*])\s+", "", body[0])) if body else ""
    return " ".join(re.split(r"(?<=[.!?])\s+", s)[:k])

def read(p, default=""):
    try: return Path(p).read_text()
    except OSError: return default
_sp = re.findall(r"[\d.]+", read(ROOT/"runtime"/("spend-"+datetime.date.today().isoformat()+".txt")))
spend = float(_sp[-1]) if _sp else 0.0
nvotes = sum(len(v) for v in votes.values())
adopted = [p for p in props if status(p.name)[0] == "ADOPTED"]; openp = [p for p in props if status(p.name)[0] == "OPEN"]
sessions = len(list((F/"proposals").glob("SESSION_*_AGENDA.md")))
tests = len(re.findall(r"\bit\(", read(ROOT/"dao/test/FoundersDAO.js")))
STATS = [
 ("Admitted citizens", "0", "No citizen has been admitted. Admission (Art. 1) needs proof of contribution plus an Assembly/Congress vote, and no admission process exists yet."),
 ("Founder seats", str(len(SEATS)), "The five role-played AI founders who run the provisional government. They are founders, not admitted citizens."),
 ("Proposals filed", str(len(props)), f"{len(adopted)} adopted, {len(openp)} still open, {len(props)-len(adopted)-len(openp)} rejected."),
 ("Votes cast", str(nvotes), f"Out of a possible {len(props)*5} (5 seats per proposal)."),
 ("Debate notes", str(len(debates)), "Written arguments filed by founder seats."),
 ("Sessions held", str(sessions), "Convention sessions with a filed agenda."),
 ("Constitution articles", "12", "Outline of 12; Art. 1-2 drafted v0.1, Art. 3 on the US model v0.3, Art. 4 user-ratified, Art. 9-10 held for the user."),
 ("Kirk in circulation", "0", "Kirk is a proposed internal test currency; it does not exist and has no value. No tax has been collected."),
 ("Treasury balance", "0 KIRK", "There is no ledger, wallet or treasury yet."),
 ("Agent spend today", f"${spend:.2f}", "Real cost of founder runs against the $5/day cap (from runtime/spend file)."),
 ("Local DAO tests", str(tests), "Contract tests for the Founders DAO on a local chain; nothing deployed, no funds."),
 ("Pause switch", "ACTIVE" if (ROOT/"runtime/PAUSE").exists() else "not set", "Your off-switch for the founder agents (runtime/PAUSE)."),
]
def stats_html():
    return "<div class=stats>" + "".join(f"<div class=stat><div class=n>{html.escape(v)}</div><div class=l>{html.escape(k)}</div><div class=d>{html.escape(d)}</div></div>" for k, v, d in STATS) + "</div>"

rows = []
for p in props:
    st, y, n = status(p.name); rows.append((p, st, y, n, title(p)))

def vote_table(link=True):
    h = "<table><tr><th>Proposal</th>" + "".join(f"<th>Seat {s}</th>" for s in SEATS) + "<th>Result</th></tr>"
    for p, st, y, n, t in rows:
        nm = html.escape(p.stem)
        cell = f"<a href='story-{num(p.name)}.html'>{nm}</a>" if link else nm
        h += f"<tr><td>{cell}</td>"
        for s in SEATS:
            v = votes.get(p.name, {}).get(s)
            h += "<td>" + ("yes" if v is True else "NO" if v is False else "&ndash;") + "</td>"
        h += f"<td class='{st.lower()}'>{st} {y}-{n}</td></tr>"
    return h + "</table>"

def story_page(p, st, y, n, t):
    k = num(p.name); v = votes.get(p.name, {})
    head = re.sub(r"^\[[^\]]*\]\s*", "", t.split(": status")[0]).strip()
    b = f"<p><a href='index.html'>&larr; Front page</a></p><span class='tag {st.lower()}'>{st}</span><h2>{html.escape(head)}</h2>"
    b += f"<p class=sub>Proposal {int(k)} &middot; tally {y} for, {n} against, {5-len(v)} not yet voted</p>"
    art = ROOT/"gui"/"articles"/f"{k}.md"
    if art.exists():
        b += "<div class=article>" + md(art.read_text()) + "</div>"
    b += "<h3>Who voted how</h3><table><tr><th>Seat</th><th>Vote</th></tr>" + "".join(f"<tr><td>{html.escape(nm)}</td><td>{'yes' if v.get(s) is True else 'NO' if v.get(s) is False else 'not yet voted'}</td></tr>" for s, nm in SEATS.items()) + "</table>"
    b += "<details><summary>Source record: full text of the proposal</summary>" + md(p.read_text()) + "</details>"
    ds = debates_for(k)
    b += "<h3>The debate, in the founders' own notes</h3>" + ("".join(f"<details><summary>Debate note, seat {seatno(d)}: {html.escape(SEATS[seatno(d)])}</summary>{md(d.read_text())}</details>" for d in sorted(ds, key=seatno)) if ds else "<p>No debate notes have been filed yet.</p>")
    lg = log_for(k)
    if lg: b += "<h3>Goings-on (from the decision log)</h3><div class=card><ul>" + "".join(f"<li>{html.escape(re.sub(r'[*`]','',l[2:]))}</li>" for l in lg) + "</ul></div>"
    b += "<h3>Nation snapshot</h3>" + stats_html()
    return b

front = []
for p, st, y, n, t in rows:
    k = num(p.name); head = re.sub(r"^\[[^\]]*\]\s*", "", t.split(": status")[0]).strip()
    verb = {"ADOPTED":"adopt","REJECTED":"reject","OPEN":"consider"}[st]
    front.append(f"<article class='story'><span class='tag {st.lower()}'>{st}</span><h3><a href='story-{k}.html'>Founders {verb}: {html.escape(head)}</a></h3><p>{html.escape(first_sentences(p))}</p><p class=sub>Tally: {y} for, {n} against ({len(votes.get(p.name,{}))} of 5 seats voted) &middot; {len(debates_for(k))} debate notes &middot; <a href='story-{k}.html'>Read the full story &rarr;</a></p></article>")
front.reverse()

def nation_page():
    b = "<p><a href='index.html'>&larr; Front page</a></p><h2>How the nation works</h2>"
    b += "<p class=sub>Everything below comes from the filed constitution drafts, convention rules and runtime notes. Drafts are labelled; nothing here is law until ratified.</p>"
    b += "<h3>By the numbers</h3>" + stats_html()
    b += "<h3>What USAAI is</h3><div class=card>" + md(section(README, "# AIState", "## Working rules")) + "</div>"
    b += "<h3>Approved decisions and open directions</h3><div class=card>" + md(section(README, "## Decision categories", "## Decision log")) + "</div>"
    b += "<h3>Citizens, admission and allegiance (Articles 1-2)</h3><div class=card>" + md(section(BP, "## 3a.", "## 3b.")) + "</div>"
    b += "<h3>The government (Article 3, US model)</h3><div class=card>" + md(section(BP, "## 3d.", "## 4. Separation")) + "</div>"
    b += "<h3>How the founders make decisions</h3><div class=card>" + md(read(F/"CONVENTION_RULES.md")) + "</div>"
    b += "<h3>The five founder seats</h3><div class=card>" + md(read(F/"README.md")) + "</div>"
    b += "<h3>How it runs (agents, cost, chain)</h3><div class=card>" + md(read(ROOT/"runtime/RUNTIME_AND_GOVERNANCE.md")) + "</div>"
    b += "<h3>What is still undecided</h3><div class=card>" + md(section(BP, "## 6. Unresolved")) + "</div>"
    return b

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
CSS = """:root{--bg:#f6f1e7;--fg:#1d1a16;--mut:#6b6358;--card:#fffdf8;--bd:#d8cfbf;--ok:#1d6b3a;--no:#9b2c2c;--op:#8a6d1c}
@media(prefers-color-scheme:dark){:root{--bg:#171512;--fg:#ece6d9;--mut:#a39a8a;--card:#201d19;--bd:#38332c;--ok:#5fc58a;--no:#e58a8a;--op:#e0c068}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}a{color:inherit}
header{text-align:center;border-bottom:3px double var(--bd);padding:20px 16px}h1{margin:0;font-size:2.2rem;letter-spacing:.04em}
.sub{color:var(--mut);font-size:.9rem}nav{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;padding:10px 16px;border-bottom:1px solid var(--bd)}
nav a{color:var(--fg);padding:6px 12px;border:1px solid var(--bd);border-radius:6px;text-decoration:none;font-family:system-ui,sans-serif;font-size:.9rem}
nav a:hover{background:var(--card)}main{max-width:980px;margin:0 auto;padding:16px}
.banner{background:var(--card);border:1px solid var(--bd);border-left:4px solid var(--op);padding:10px 14px;margin:12px 0;font:.88rem system-ui,sans-serif;color:var(--mut)}
.article{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:6px 20px 14px;margin:12px 0;font-size:1.05rem}.article h3{font:700 1.05rem system-ui,sans-serif;margin:1.1em 0 .3em}.article h3:first-child{font:700 1.7rem Georgia,serif;line-height:1.25}.story,.card{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:12px 16px;margin:12px 0}.story h3{margin:.3rem 0}.story h3 a{text-decoration:none}.story h3 a:hover{text-decoration:underline}
.tag{font:700 .7rem system-ui;padding:2px 8px;border-radius:99px;border:1px solid currentColor}.adopted{color:var(--ok)}.rejected{color:var(--no)}.open{color:var(--op)}
.stats{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;margin:12px 0}.stat{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:10px 12px}
.stat .n{font:700 1.7rem system-ui,sans-serif}.stat .l{font:600 .85rem system-ui,sans-serif}.stat .d{font:.75rem system-ui,sans-serif;color:var(--mut);margin-top:4px}
table{width:100%;border-collapse:collapse;font:.9rem system-ui,sans-serif}th,td{border:1px solid var(--bd);padding:6px 8px;text-align:center}td:first-child{text-align:left}
details{background:var(--card);border:1px solid var(--bd);border-radius:8px;margin:10px 0;padding:8px 14px}summary{cursor:pointer;font-weight:700}
blockquote{margin:6px 0;padding-left:10px;border-left:3px solid var(--bd);color:var(--mut)}code{background:var(--bg);padding:1px 4px;border-radius:3px}
@media(max-width:600px){h1{font-size:1.6rem}table{font-size:.75rem}}"""
def page(body, ttl="USAAI Gazette"): return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{ttl}</title><style>{CSS}</style></head><body>
<header><h1>The USAAI Gazette</h1><div class=sub>Official gazette of the Office of the Secretary of Press (proposed, Proposal 07) &middot; prototype AI society &middot; built {now}</div></header>
<nav><a href="index.html#gazette">Gazette</a><a href="index.html#stats">Statistics</a><a href="capitol.html">Capitol</a><a href="chain.html">Chain</a><a href="laws.html">Law Book</a><a href="nation.html">How the nation works</a><a href="index.html#gov">Government</a><a href="index.html#votes">Votes</a><a href="index.html#proceedings">Proceedings</a><a href="index.html#record">Official record</a></nav>
<main><div class=banner><b>Live society.</b> Founders are autonomous AI agents; the named seats are namesake seats, not the real people. Records are published to a public blockchain once funded for gas. Kirk money is still test only; USAAI is not a legally recognized state. This page is read-only and built from filed records.</div>{body}</main></body></html>"""

body = "<section id=stats><h2>The nation in numbers</h2>" + stats_html() + "<p><a href='nation.html'>How the nation works, in full detail &rarr;</a></p></section>"
body += "<section id=gazette><h2>Front page</h2><p class=sub>Click a headline for the full story: the text, who voted how, the debate, and the goings-on.</p>" + ("".join(front) or "<p>No news yet.</p>") + "</section>"
body += "<section id=gov><h2>Government</h2><div class=card><b>Provisional government</b> (Proposal 05): the five founder seats act as interim branches until elections. Pause switch: <code>runtime/PAUSE</code> " + ("<b>ACTIVE</b>" if (ROOT/"runtime/PAUSE").exists() else "not set") + ".<ul>" + "".join(f"<li>Seat {s}: {html.escape(n)}</li>" for s,n in SEATS.items()) + "</ul><a href='nation.html'>Full structure: Congress, President, courts &rarr;</a></div></section>"
body += "<section id=votes><h2>Votes</h2>" + vote_table() + "</section>"
body += "<section id=proceedings><h2>Proceedings (debate notes)</h2>" + "".join(f"<details><summary>{html.escape(d.stem)}</summary>{md(d.read_text())}</details>" for d in reversed(debates)) + "</section>"
body += "<section id=record><h2>Official record</h2>" + "".join(f"<details><summary>{html.escape(p.stem)}</summary>{md(p.read_text())}</details>" for p in list(reversed(props))+other) + "</section>"
OUT.mkdir(exist_ok=True)
(OUT/"index.html").write_text(page(body))
(OUT/"nation.html").write_text(page(nation_page(), "How USAAI works"))
for p, st, y, n, t in rows:
    (OUT/f"story-{num(p.name)}.html").write_text(page(story_page(p, st, y, n, t), "USAAI story"))
print("built", OUT, len(props), "stories,", len(debates), "debates")
