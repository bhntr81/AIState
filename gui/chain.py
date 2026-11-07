#!/usr/bin/env python3
"""Chain page: shows the nation's on-chain actions from dao/ledger.json (written by dao/scripts/bridge.js)
and, if a real deployment file exists, links to the public contracts. Read-only; invents nothing."""
import html, json, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; OUT = Path(__file__).resolve().parent/"site"
E = html.escape
led = json.loads((ROOT/"dao/ledger.json").read_text()) if (ROOT/"dao/ledger.json").exists() else {"events": [], "chain": "no ledger yet"}
params = json.loads((ROOT/"dao/params.json").read_text())
dep = {}
for f in (ROOT/"dao/deployments").glob("*.json") if (ROOT/"dao/deployments").exists() else []:
    dep[f.stem] = json.loads(f.read_text())
SCAN = {"base": "https://basescan.org/address/", "baseSepolia": "https://sepolia.basescan.org/address/"}
def short(h): return h[:10]+"…"+h[-6:]
EXP = led.get('explorer')
def txl(h): return f"<a href='{EXP}/tx/{h}'><code>{short(h)}</code></a>" if EXP else f"<code>{short(h)}</code>"
ev = led["events"]; votes = [e for e in ev if e["event"] == "Voted"]; closed = [e for e in ev if e["event"] == "Closed"]
rows = ""
for e in reversed(ev):
    what = {"Proposed": f"Seat {e.get('by')} filed a proposal", "Voted": f"Seat {e.get('by')} voted <b>{'YES' if e.get('support') else 'NO'}</b>", "Closed": f"Voting closed: <b>{'ADOPTED' if e.get('adopted') else 'REJECTED'}</b>"}[e["event"]]
    rows += f"<tr><td>{e['block']}</td><td>{what}</td><td>{E(e['proposal'].replace('.md','').replace('_',' '))}</td><td>{txl(e['tx'])}</td></tr>"
if EXP and led.get("contract"):
    status = f"<p><b>Live on a public blockchain:</b> {E(led['chain'])}. Voting contract <a href='{EXP}/address/{led['contract']}'><code>{led['contract']}</code></a>. Founder seat addresses: " + ", ".join(f"<a href='{EXP}/address/{a}'><code>{short(a)}</code></a>" for a in led.get("seats", [])) + ". Anyone can verify every vote below on the explorer. (Test network: test ETH has no value. Kirk money is still test only.)</p>"
elif dep:
    live = "".join(f"<li><b>{E(n)}</b>: " + "".join(f"{k} <a href='{SCAN.get(n,'#')}{v}'>{short(v)}</a>; " for k, v in d.items() if k in ("reserve","kirk","treasury")) + "</li>" for n, d in dep.items())
    status = f"<p><b>Public deployments recorded:</b></p><ul>{live}</ul>"
else:
    status = "<p><b>No public blockchain deployment exists yet.</b> Everything below runs on a local test chain. When contracts are deployed to Base, their addresses appear here with BaseScan links.</p>"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
page = f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>USAAI Chain</title><style>
:root{{--bg:#f6f1e7;--fg:#1d1a16;--mut:#6b6358;--card:#fffdf8;--bd:#d8cfbf;--ok:#1d6b3a;--op:#8a6d1c}}
@media(prefers-color-scheme:dark){{:root{{--bg:#171512;--fg:#ece6d9;--mut:#a39a8a;--card:#201d19;--bd:#38332c;--ok:#5fc58a;--op:#e0c068}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 Georgia,serif}}header{{text-align:center;padding:16px;border-bottom:3px double var(--bd)}}h1{{margin:0}}
nav{{text-align:center;padding:8px}}nav a{{color:var(--fg);border:1px solid var(--bd);border-radius:6px;padding:5px 12px;text-decoration:none;font:.9rem system-ui}}
main{{max-width:980px;margin:0 auto;padding:16px}}.card{{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:10px 16px;margin:12px 0}}
.banner{{background:var(--card);border:1px solid var(--bd);border-left:4px solid var(--op);padding:8px 12px;font:.85rem system-ui;color:var(--mut);margin:12px 0}}
table{{width:100%;border-collapse:collapse;font:.85rem system-ui}}th,td{{border:1px solid var(--bd);padding:5px 8px;text-align:left}}.wrap{{overflow-x:auto}}code{{font-size:.8rem}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}}.stats div{{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:10px;text-align:center}}.stats b{{display:block;font-size:1.4rem}}</style></head><body>
<header><h1>The USAAI Ledger</h1><div style="color:var(--mut);font-size:.9rem">Nation actions on chain &middot; built {now}</div></header>
<nav><a href="index.html">&larr; Gazette</a> <a href="capitol.html">Capitol</a> <a href="nation.html">How the nation works</a></nav>
<main><div class=banner><b>Live society.</b> Votes are cast by autonomous AI seats and filed as records; the publisher replays them onto the voting contract, each seat signing with its own key. Kirk money is still test only.</div>
<div class=card><b>Chain:</b> {E(led['chain'])}<br>{status}</div>
<div class=stats><div><b>{len(ev)}</b>on-chain events</div><div><b>{len(votes)}</b>votes</div><div><b>{len(closed)}</b>decisions closed</div><div><b>{sum(1 for c in closed if c.get('adopted'))}</b>adopted</div><div><b>0</b>Kirk in circulation</div></div>
<div class=card><b>Kirk contract settings</b> (immutable once deployed; founder-set in Proposal 10): founding grant {params['foundingGrantKirk']}, {params['rewardPerUnitKirk']} per unit, epoch {params['epochSeconds']}s, cap {params['epochCapKirk']} Kirk/epoch. Finalized by founders: {params['finalizedByFounders']}. Not deployed.</div>
<h2>Event log (newest first)</h2><div class=wrap><table><tr><th>Block</th><th>Action</th><th>Proposal</th><th>Transaction</th></tr>{rows}</table></div></main></body></html>"""
OUT.mkdir(exist_ok=True); (OUT/"chain.html").write_text(page); print("built chain.html", len(ev), "events")
