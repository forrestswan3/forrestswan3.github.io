#!/usr/bin/env python3
"""Render the portfolio site (site/index.html) and the profile README (PROFILE_README.md)
from portfolio.json — the single source of truth. Stdlib only.

Usage:  python scripts/build.py
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((ROOT / 'portfolio.json').read_text(encoding='utf-8'))
owner, author = data['owner'], data['author']
ORDER = {'In production': 0, 'Shipped': 1, 'In progress': 2}
projects = sorted(data['projects'], key=lambda p: (ORDER.get(p['status'], 9), p['title']))

# ---- Brand tokens ------------------------------------------------------------
# SystemSerenity brand palette (brand sheet, 2026-09-22)
BRAND = dict(name='SystemSerenity', tagline='Operational clarity at scale.',
             navy='#0B1F33', steel='#3A6EA5', teal='#2C9C95', sage='#8FB996',
             platinum='#E5E7EB', offwhite='#F7F4ED')


def link(p):
    return p['repo'] if p.get('visibility') == 'public' else None


def profile_readme():
    rows = []
    for p in projects:
        url = link(p)
        name = f"[{p['title']}]({url})" if url else f"{p['title']} *(private)*"
        rows.append(f"| {name} | {p['status']} | {p['shipped'] or '—'} | {p['tagline']} |")
    cs = '\n'.join(f"- **{c['title']}** ({c['status']}, {c['date']}): {c['summary']}" for c in data.get('case_studies', []))
    return f"""<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ss-mark-dark.png"><img src="assets/ss-mark.png" width="56" alt="SystemSerenity"></picture> **SystemSerenity** — *{BRAND['tagline']}*

# Hi, I'm {author.split()[0]} 👋

Agency operations & systems manager. I build the internal tools that keep an insurance agency running:
desktop apps, Google Apps Script automations, compliance tooling, and training content.

**Focus:** Python desktop apps · Google Apps Script · workflow automation (Zapier, n8n, Slack) · data-policy compliance · training systems

## Projects

| Project | Status | Last shipped | What it does |
|---|---|---|---|
{chr(10).join(rows)}

## Case studies (documentation work)

{cs}

<sub>Generated from `portfolio.json` in the portfolio repo · last updated {data['updated']} · Private repositories are listed without links.</sub>
"""


def site():
    cards = []
    for p in projects:
        url = link(p)
        tags = ''.join(f'<span class="tag">{html.escape(t)}</span>' for t in p['topics'][:6])
        a = f'<a href="{html.escape(url)}">View repository →</a>' if url else '<span class="muted">Repository private — available on request</span>'
        cards.append(f"""<article class="card"><div class="row"><h3>{html.escape(p['title'])}</h3>
<span class="status s-{p['status'].split()[0].lower()}">{html.escape(p['status'])}</span></div>
<p>{html.escape(p['tagline'])}</p><div class="tags">{tags}</div><p class="meta">{html.escape(p['lang'])} · {html.escape(p['shipped'] or 'in progress')}</p>{a}</article>""")
    cs = ''.join(f"<li><strong>{html.escape(c['title'])}</strong> — {html.escape(c['summary'])} <span class='muted'>({html.escape(c['status'])}, {c['date']})</span></li>" for c in data.get('case_studies', []))
    b = BRAND
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(author)} — Portfolio</title><link rel="icon" href="assets/ss-mark.png"><meta name="description" content="Internal tools, automations and training systems built by {html.escape(author)}.">
<style>
:root{{--ink:{b['navy']};--accent:{b['teal']};--link:{b['steel']};--sage:{b['sage']};--bg:{b['offwhite']};--line:{b['platinum']};--card:#fff;--muted:#4f5d6d}}
@media (prefers-color-scheme:dark){{:root{{--ink:#EEF1F4;--bg:{b['navy']};--line:#22384F;--card:#10283F;--muted:#A9B6C4;--link:#8FB5DD}} .s-shipped{{color:#8FB996}}}}
*{{box-sizing:border-box}}body{{margin:0;font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}}
header,main,footer{{max-width:1080px;margin:0 auto;padding:24px 16px}}
.brandbar{{display:flex;align-items:center;gap:14px}}.brandbar img{{width:56px;height:auto}}
.wordmark{{font-weight:700;font-size:22px;letter-spacing:-.01em}}.wordmark span{{color:var(--accent)}}
.eyebrow{{color:var(--link);font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:12px}}
header h1{{margin:.6em 0 0;font-size:clamp(28px,5vw,42px)}}
.rule{{display:flex;align-items:center;gap:8px;margin:14px 0}}.rule i{{height:2px;width:64px;background:var(--accent)}}.rule b{{width:7px;height:7px;border-radius:50%;background:var(--accent)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.card{{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--accent);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:6px}}
.card h3{{margin:0;font-size:18px}}.card p{{margin:0}}.row{{display:flex;justify-content:space-between;gap:8px;align-items:start}}
.status{{font-size:12px;padding:2px 10px;border-radius:999px;border:1px solid var(--line);white-space:nowrap}}
.s-in{{color:var(--link)}}.s-shipped{{color:#1F7A74}}.tags{{display:flex;flex-wrap:wrap;gap:6px}}
.tag{{font-size:12px;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:0 6px}}
.meta,.muted{{color:var(--muted);font-size:14px}}a{{color:var(--link);font-weight:600;text-decoration:none}}a:hover{{text-decoration:underline}}
</style></head><body>
<header><div class="brandbar"><picture><source srcset="assets/ss-mark-dark.png" media="(prefers-color-scheme: dark)"><img src="assets/ss-mark.png" alt=""></picture><div><div class="wordmark">System<span>Serenity</span></div><div class="eyebrow">{html.escape(b['tagline'])}</div></div></div>
<h1>{html.escape(author)}</h1><div class="rule"><i></i><b></b><i></i></div>
<p>Agency operations &amp; systems — internal tools, automation and training systems.</p></header>
<main><h2>Projects</h2><section class="grid">{''.join(cards)}</section>
<h2>Case studies</h2><ul>{cs}</ul></main>
<footer class="muted">Built from portfolio.json · updated {data['updated']}</footer></body></html>"""


(ROOT / 'PROFILE_README.md').write_text(profile_readme(), encoding='utf-8')
(ROOT / 'site').mkdir(exist_ok=True)
(ROOT / 'site' / 'index.html').write_text(site(), encoding='utf-8')
import shutil
(ROOT / 'site' / 'assets').mkdir(exist_ok=True)
for f in ('ss-mark.png', 'ss-mark-dark.png'):
    shutil.copy(ROOT / 'assets' / f, ROOT / 'site' / 'assets' / f)
print(f'built {len(projects)} projects')
