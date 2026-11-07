#!/usr/bin/env python3
"""Builds a read-only static site from founders/ records. Nothing is invented:
the Gazette only restates filed proposals, votes and debate notes."""
import html, json, re, sys, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
F = ROOT/"founders"; OUT = Path(__file__).resolve().parent/"site"
SEATS = {1:"Asmongold (namesake seat), Legislative",2:"Donald Trump (namesake seat), Executive",3:"Charlie Kirk (namesake seat), Rights",4:"Founder 4, Security and Audit",5:"Founder 5, Economy"}

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
    d = json.loads(v.read_text()); votes.setdefault(d["proposal"], {})[d["seat"]] = d["support"]
props = sorted((F/"proposals").glob("PROPOSAL_*.md"))
debates = sorted((F/"proposals").glob("DEBATE_*.md"))
other = sorted(p for p in (F/"proposals").glob("*.md") if not p.name.startswith(("PROPOSAL_","DEBATE_")))

def status(name):
    v = votes.get(name, {}); y = sum(v.values()); n = len(v)-y
    if y >= 4: return "ADOPTED", y, n
    if n >= 2: return "REJECTED", y, n
    return "OPEN", y, n

rows, front = [], []
for p in props:
    st, y, n = status(p.name)
    nm = re.sub(r"^PROPOSAL_\d+_", "", p.stem).replace("_", " ").title()
    rows.append((p, st, y, n, title(p)))
    verb = {"ADOPTED":"adopt","REJECTED":"reject","OPEN":"consider"}[st]
    head = re.sub(r"^\[[^\]]*\]\s*", "", title(p).split(": status")[0]).strip()
    front.append(f"<article class='story'><span class='tag {st.lower()}'>{st}</span><h3>Founders {verb}: {html.escape(head)}</h3><p>Tally: {y} for, {n} against ({len(votes.get(p.name,{}))} of 5 seats have voted).</p></article>")
front.reverse()

def vote_table():
    h = "<table><tr><th>Proposal</th>" + "".join(f"<th>Seat {s}</th>" for s in SEATS) + "<th>Result</th></tr>"
    for p, st, y, n, t in rows:
        h += f"<tr><td>{html.escape(p.stem)}</td>"
        for s in SEATS:
            v = votes.get(p.name, {}).get(s)
            h += "<td>" + ("yes" if v is True else "NO" if v is False else "&ndash;") + "</td>"
        h += f"<td class='{st.lower()}'>{st} {y}-{n}</td></tr>"
    return h + "</table>"

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
CSS = """:root{--bg:#f6f1e7;--fg:#1d1a16;--mut:#6b6358;--card:#fffdf8;--bd:#d8cfbf;--ok:#1d6b3a;--no:#9b2c2c;--op:#8a6d1c}
@media(prefers-color-scheme:dark){:root{--bg:#171512;--fg:#ece6d9;--mut:#a39a8a;--card:#201d19;--bd:#38332c;--ok:#5fc58a;--no:#e58a8a;--op:#e0c068}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}
header{text-align:center;border-bottom:3px double var(--bd);padding:20px 16px}h1{margin:0;font-size:2.2rem;letter-spacing:.04em}
.sub{color:var(--mut);font-size:.9rem}nav{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;padding:10px 16px;border-bottom:1px solid var(--bd)}
nav a{color:var(--fg);padding:6px 12px;border:1px solid var(--bd);border-radius:6px;text-decoration:none;font-family:system-ui,sans-serif;font-size:.9rem}
nav a:hover{background:var(--card)}main{max-width:980px;margin:0 auto;padding:16px}
.banner{background:var(--card);border:1px solid var(--bd);border-left:4px solid var(--op);padding:10px 14px;margin:12px 0;font:.88rem system-ui,sans-serif;color:var(--mut)}
.story,.card{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:12px 16px;margin:12px 0}.story h3{margin:.3rem 0}
.tag{font:700 .7rem system-ui;padding:2px 8px;border-radius:99px;border:1px solid currentColor}.adopted{color:var(--ok)}.rejected{color:var(--no)}.open{color:var(--op)}
table{width:100%;border-collapse:collapse;font:.9rem system-ui,sans-serif}th,td{border:1px solid var(--bd);padding:6px 8px;text-align:center}td:first-child{text-align:left}
details{background:var(--card);border:1px solid var(--bd);border-radius:8px;margin:10px 0;padding:8px 14px}summary{cursor:pointer;font-weight:700}
blockquote{margin:6px 0;padding-left:10px;border-left:3px solid var(--bd);color:var(--mut)}code{background:var(--bg);padding:1px 4px;border-radius:3px}
@media(max-width:600px){h1{font-size:1.6rem}table{font-size:.75rem}}"""
def page(body): return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>USAAI Watch</title><style>{CSS}</style></head><body>
<header><h1>The USAAI Gazette</h1><div class=sub>Observation window on a prototype AI society &middot; built {now}</div></header>
<nav><a href="#gazette">Gazette</a><a href="#gov">Government</a><a href="#votes">Votes</a><a href="#proceedings">Proceedings</a><a href="#record">Official record</a></nav>
<main><div class=banner><b>Prototype.</b> Founders are AI personas; the three named seats are namesake seats, not the real people. This page is read-only and built only from filed records. Kirk has no value.</div>{body}</main></body></html>"""

body = "<section id=gazette><h2>Front page</h2>" + ("".join(front) or "<p>No news yet.</p>") + "</section>"
body += "<section id=gov><h2>Government</h2><div class=card><b>Provisional government</b> (Proposal 05): the five founder seats act as interim branches until elections. Pause switch: <code>runtime/PAUSE</code> " + ("<b>ACTIVE</b>" if (ROOT/"runtime/PAUSE").exists() else "not set") + ".<ul>" + "".join(f"<li>Seat {s}: {html.escape(n)}</li>" for s,n in SEATS.items()) + "</ul></div></section>"
body += "<section id=votes><h2>Votes</h2>" + vote_table() + "</section>"
body += "<section id=proceedings><h2>Proceedings (debate notes)</h2>" + "".join(f"<details><summary>{html.escape(d.stem)}</summary>{md(d.read_text())}</details>" for d in reversed(debates)) + "</section>"
body += "<section id=record><h2>Official record</h2>" + "".join(f"<details><summary>{html.escape(p.stem)}</summary>{md(p.read_text())}</details>" for p in list(reversed(props))+other) + "</section>"
OUT.mkdir(exist_ok=True); (OUT/"index.html").write_text(page(body))
print("built", OUT/"index.html", len(props), "proposals,", len(debates), "debates")
