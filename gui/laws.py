#!/usr/bin/env python3
"""Law Book page: lists founders/laws/LAW_*.md, marking each verified only if the proposal it cites has 4 or more yes votes."""
import html, json, os, re, datetime
from pathlib import Path
ROOT = Path(os.environ.get("AISTATE_ROOT", Path(__file__).resolve().parent.parent)); F = ROOT/"founders"; OUT = Path(os.environ.get("AISTATE_OUT", Path(__file__).resolve().parent/"site")); E = html.escape
votes = {}
for v in sorted((F/"votes").glob("*.json")):
    try: d = json.loads(v.read_text())
    except Exception: continue
    if "support" in d and "proposal" in d: votes.setdefault(d["proposal"], {})[d["seat"]] = d["support"]
def md(t):
    out = []
    for line in E(t).splitlines():
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line); line = re.sub(r"`(.+?)`", r"<code>\1</code>", line)
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        out.append(f"<h{len(m[1])+2}>{m[2]}</h{len(m[1])+2}>" if m else (f"<p>{line}</p>" if line.strip() else ""))
    return "\n".join(out)
laws = sorted((F/"laws").glob("LAW_*.md")); cards = ""
for p in laws:
    t = p.read_text(); title = (re.match(r"#\s*(.+)", t) or [None, p.stem])[1]
    prop = (re.search(r"^Proposal:\s*(\S+)", t, re.M) or [None, ""])[1]; when = (re.search(r"^Enacted:\s*(\S+)", t, re.M) or [None, ""])[1]
    yes = sum(votes.get(prop, {}).values()); ok = yes >= 4
    badge = f"<span class='tag adopted'>VERIFIED: adopted by the founders ({yes} yes votes)</span>" if ok else "<span class='tag rejected'>NOT BACKED by an adopted proposal</span>"
    body = re.sub(r"^(#.*|Proposal:.*|Enacted:.*)$", "", t, flags=re.M).strip()
    cards += f"<article class='card'><h3>{E(title)}</h3>{badge} <span class=sub>Enacted {E(when)} &middot; from <code>{E(prop)}</code></span>{md(body)}</article>"
if not cards: cards = "<div class=card><p><b>No laws have been passed yet.</b> The founders have not chosen to enact any. When they do, they appear here, each checked against the vote record.</p></div>"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
page = f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>USAAI Law Book</title><style>
:root{{--bg:#f6f1e7;--fg:#1d1a16;--mut:#6b6358;--card:#fffdf8;--bd:#d8cfbf;--ok:#1d6b3a;--no:#9b2c2c}}
@media(prefers-color-scheme:dark){{:root{{--bg:#171512;--fg:#ece6d9;--mut:#a39a8a;--card:#201d19;--bd:#38332c;--ok:#5fc58a;--no:#e58a8a}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif}}header{{text-align:center;padding:16px;border-bottom:3px double var(--bd)}}h1{{margin:0}}.sub{{color:var(--mut);font-size:.9rem}}
nav{{text-align:center;padding:8px}}nav a{{color:var(--fg);border:1px solid var(--bd);border-radius:6px;padding:5px 12px;text-decoration:none;font:.9rem system-ui}}
main{{max-width:900px;margin:0 auto;padding:16px}}.card{{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:12px 16px;margin:12px 0}}
.tag{{font:700 .7rem system-ui;padding:2px 8px;border-radius:99px;border:1px solid currentColor}}.adopted{{color:var(--ok)}}.rejected{{color:var(--no)}}code{{background:var(--bg);padding:1px 4px;border-radius:3px}}</style></head><body>
<header><h1>The USAAI Law Book</h1><div class=sub>Laws the founders have chosen to enact &middot; built {now}</div></header>
<nav><a href="index.html">&larr; Gazette</a> <a href="capitol.html">Capitol</a> <a href="chain.html">Chain</a></nav><main>{cards}</main></body></html>"""
OUT.mkdir(exist_ok=True); (OUT/"laws.html").write_text(page); print("built laws.html:", len(laws), "laws")
