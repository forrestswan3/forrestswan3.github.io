#!/usr/bin/env python3
"""Render the portfolio from portfolio.json, the single source of truth. Stdlib only.

Outputs
  site/index.html            landing page, published at https://forrestswan3.github.io/
  site/assets/*              brand marks and demo previews
  pages/<repo>/index.html    project page; copy it to the root of that repo, where
                             GitHub Pages serves it at https://forrestswan3.github.io/<repo>/
  PROFILE_README.md          copy into the forrestswan3/forrestswan3 profile repo

Usage:  python scripts/build.py
"""
import html, json, pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((ROOT / 'portfolio.json').read_text(encoding='utf-8'))
owner, author = data['owner'], data['author']
SITE = data.get('site', f'https://{owner}.github.io/')
ORDER = {'In production': 0, 'Shipped': 1, 'In progress': 2}
projects = sorted(data['projects'], key=lambda p: (ORDER.get(p['status'], 9), -int((p['shipped'] or '0').replace('-', '')), p['title']))
public = [p for p in projects if p.get('visibility') == 'public']

# ---- Brand -------------------------------------------------------------------
# SystemSerenity brand palette (brand sheet, 2026-09-22)
BRAND = dict(name='SystemSerenity', tagline='Operational clarity at scale.',
             navy='#0B1F33', steel='#3A6EA5', teal='#2C9C95', sage='#8FB996',
             platinum='#E5E7EB', offwhite='#F7F4ED')
ROLE = 'Agency Operations & Systems Manager'
MARK = f'{SITE}assets/ss-mark.png'
MARK_DARK = f'{SITE}assets/ss-mark-dark.png'

e = html.escape


def inline(s):
    """Minimal inline Markdown: `code`, **bold**, *italic*, [text](url)."""
    s = e(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s


def plain(s):
    return re.sub(r'[`*]', '', s)


def fmt_date(d):
    if not d:
        return 'In progress'
    y, m, dd = d.split('-')
    return f"{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m)-1]} {int(dd)}, {y}"


def status_class(s):
    return {'In production': 'prod', 'Shipped': 'ship', 'In progress': 'wip'}.get(s, 'wip')


def test_count():
    n = 0
    for p in projects:
        for h in p.get('detail', {}).get('highlights', []):
            m = re.search(r'(\d+) automated tests pass', h)
            if m:
                n += int(m.group(1))
    return n


# ---- Icons (inline SVG, stroke = currentColor) --------------------------------
def icon(name, size=20):
    paths = {
        'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'ext': '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
        'back': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
        'code': '<path d="M9 8l-5 4 5 4M15 8l5 4-5 4"/>',
        'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
        'app': '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 8h18M8 21h8M12 18v3"/>',
        'flow': '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.5 6H15a3 3 0 0 1 3 3v6.5M6 8.5V15a3 3 0 0 0 3 3h6.5"/>',
        'shield': '<path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
        'learn': '<path d="M3 8l9-4 9 4-9 4z"/><path d="M7 10v5c0 1.5 2.2 3 5 3s5-1.5 5-3v-5"/>',
        'play': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 9.5v5l4.5-2.5z"/>',
        'doc': '<path d="M7 3h7l5 5v12a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
        'github': '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
    }
    return (f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


# ---- Shared page chrome ---------------------------------------------------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">')

b = BRAND
CSS = f"""
:root{{--navy:{b['navy']};--steel:{b['steel']};--teal:{b['teal']};--sage:{b['sage']};--platinum:{b['platinum']};--offwhite:{b['offwhite']};
--bg:{b['offwhite']};--surface:#FFFFFF;--surface-2:#FBFAF6;--ink:{b['navy']};--ink-2:#34475B;--muted:#5B6B7C;--line:#E3E0D7;--line-2:{b['platinum']};
--link:#2F5F93;--accent:{b['teal']};--accent-ink:#1D6F6A;--accent-tint:#E4F2F0;--steel-tint:#E8EFF7;--sage-tint:#EDF4EA;--sage-ink:#3F6B3A;
--btn:{b['navy']};--btn-ink:#FFFFFF;--shadow:0 1px 2px rgba(11,31,51,.04),0 8px 24px -12px rgba(11,31,51,.18);
--sans:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--display:"Inter Tight",Inter,system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
@media (prefers-color-scheme:dark){{:root{{--bg:#081726;--surface:#0E2236;--surface-2:#0B1D2F;--ink:#ECF0F4;--ink-2:#C7D2DD;--muted:#94A5B6;--line:#1C3450;--line-2:#1C3450;
--link:#8DB6E2;--accent:#3FB3AB;--accent-ink:#7FD3CC;--accent-tint:rgba(44,156,149,.16);--steel-tint:rgba(58,110,165,.2);--sage-tint:rgba(143,185,150,.16);--sage-ink:#A9D1A6;
--btn:#ECF0F4;--btn-ink:{b['navy']};--shadow:0 1px 2px rgba(0,0,0,.3),0 12px 28px -14px rgba(0,0,0,.6)}}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}
body{{margin:0;font:16px/1.65 var(--sans);color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}}
a{{color:var(--link);text-decoration:none}}a:hover{{text-decoration:underline;text-underline-offset:3px}}
code{{font:.86em var(--mono);background:var(--steel-tint);padding:.1em .4em;border-radius:5px;color:var(--ink)}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 24px}}
.ic{{flex:none;vertical-align:middle}}
/* nav */
.nav{{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:saturate(1.4) blur(10px);-webkit-backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}}
.nav .wrap{{display:flex;align-items:center;justify-content:space-between;height:64px;gap:16px}}
.brand{{display:flex;align-items:center;gap:10px;color:var(--ink);font:600 17px/1 var(--display);letter-spacing:-.01em}}.brand:hover{{text-decoration:none}}
.brand img{{width:30px;height:auto;display:block}}.brand .wm span{{color:var(--accent-ink)}}
.links{{display:flex;gap:26px;align-items:center;font-size:14.5px;font-weight:500}}.links a{{color:var(--ink-2)}}.links a:hover{{color:var(--ink)}}
.links .gh{{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:7px 14px;background:var(--surface)}}
@media (max-width:760px){{.links .hide-sm{{display:none}}}}
/* type */
.eyebrow{{font:500 12.5px/1.2 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent-ink)}}
h1,h2,h3{{font-family:var(--display);color:var(--ink);letter-spacing:-.02em;margin:0}}
h2{{font-size:clamp(26px,3.4vw,34px);line-height:1.15;font-weight:600}}
h3{{font-size:19px;line-height:1.3;font-weight:600;letter-spacing:-.01em}}
.lede{{font-size:clamp(17px,1.9vw,19.5px);line-height:1.6;color:var(--ink-2);max-width:62ch}}
.muted{{color:var(--muted)}}
section{{padding:88px 0}}section+section{{border-top:1px solid var(--line)}}
.sec-head{{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:36px;flex-wrap:wrap}}
.sec-head p{{margin:10px 0 0;max-width:58ch;color:var(--muted)}}
/* buttons */
.btn{{display:inline-flex;align-items:center;gap:8px;font:600 15px/1 var(--sans);padding:13px 20px;border-radius:10px;border:1px solid transparent;transition:transform .15s ease,box-shadow .15s ease,background .15s}}
.btn:hover{{text-decoration:none;transform:translateY(-1px)}}
.btn-primary{{background:var(--btn);color:var(--btn-ink);box-shadow:var(--shadow)}}
.btn-ghost{{background:var(--surface);color:var(--ink);border-color:var(--line)}}.btn-ghost:hover{{border-color:var(--ink-2)}}
/* pills */
.pill{{display:inline-flex;align-items:center;gap:6px;font:500 12px/1 var(--sans);padding:6px 10px;border-radius:999px;white-space:nowrap}}
.pill::before{{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}}
.pill.prod{{background:var(--accent-tint);color:var(--accent-ink)}}.pill.ship{{background:var(--steel-tint);color:var(--link)}}.pill.wip{{background:var(--sage-tint);color:var(--sage-ink)}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}
.chip{{font:500 11.5px/1 var(--mono);color:var(--ink-2);background:var(--surface-2);border:1px solid var(--line);border-radius:6px;padding:6px 8px}}
/* footer */
footer{{border-top:1px solid var(--line);padding:40px 0 56px;color:var(--muted);font-size:14px}}
footer .wrap{{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;align-items:center}}
footer .brand{{font-size:15px}}footer .brand img{{width:24px}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:3px;border-radius:6px}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;scroll-behavior:auto!important}}}}
"""


def head(title, desc, url, extra_css=''):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="author" content="{e(author)}">
<link rel="canonical" href="{e(url)}"><link rel="icon" type="image/png" href="{MARK}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}"><meta property="og:image" content="{MARK}">
<meta name="twitter:card" content="summary"><meta name="theme-color" content="{b['offwhite']}" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#081726" media="(prefers-color-scheme: dark)">
{FONTS}<style>{CSS}{extra_css}</style></head>"""


def mark(size_attr=''):
    return f'<picture><source srcset="{MARK_DARK}" media="(prefers-color-scheme: dark)"><img src="{MARK}" alt="" {size_attr}></picture>'


def nav(links_html):
    return f"""<header class="nav"><div class="wrap"><a class="brand" href="{SITE}" aria-label="SystemSerenity home">{mark()}<span class="wm">System<span>Serenity</span></span></a>
<nav class="links" aria-label="Primary">{links_html}<a class="gh" href="https://github.com/{owner}">{icon('github',16)}GitHub</a></nav></div></header>"""


def footer():
    return f"""<footer><div class="wrap"><a class="brand" href="{SITE}">{mark()}<span class="wm">System<span>Serenity</span></span></a>
<div>© {data['updated'][:4]} {e(author)} · {e(BRAND['tagline'])}</div>
<div>Updated {fmt_date(data['updated'])}</div></div></footer>"""


# ---- Landing page -----------------------------------------------------------------
HOME_CSS = """
.hero{padding:96px 0 88px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;inset:auto -10% -40% 45%;height:520px;background:radial-gradient(closest-side,color-mix(in srgb,var(--teal) 16%,transparent),transparent);pointer-events:none}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:56px;align-items:center;position:relative;z-index:1}
.hero h1{font-size:clamp(40px,6.2vw,68px);line-height:1.02;font-weight:700;letter-spacing:-.035em;margin:18px 0 22px}
.hero h1 em{font-style:normal;background:linear-gradient(90deg,var(--steel),var(--teal));-webkit-background-clip:text;background-clip:text;color:transparent}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:32px}
.who{display:flex;align-items:center;gap:10px;margin-top:28px;font-size:14.5px;color:var(--muted)}
.who b{color:var(--ink);font-weight:600}
.stats{background:var(--surface);border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);display:grid;grid-template-columns:1fr 1fr}
.stat{padding:26px 26px 24px}.stat:nth-child(odd){border-right:1px solid var(--line)}.stat:nth-child(-n+2){border-bottom:1px solid var(--line)}
.stat .n{font:700 44px/1 var(--display);letter-spacing:-.03em;color:var(--ink)}.stat .l{margin-top:8px;font-size:13.5px;color:var(--muted)}
.stat .n small{font-size:20px;color:var(--accent-ink);margin-left:2px}
.caps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:18px;overflow:hidden}
.cap{background:var(--surface);padding:28px 24px}.cap .ic{color:var(--accent-ink);margin-bottom:16px}.cap h3{font-size:16.5px;margin-bottom:6px}.cap p{margin:0;font-size:14.5px;color:var(--muted);line-height:1.55}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:24px;display:flex;flex-direction:column;gap:14px;transition:border-color .15s,box-shadow .2s,transform .2s}
.card:hover{border-color:color-mix(in srgb,var(--steel) 45%,var(--line));box-shadow:var(--shadow);transform:translateY(-2px)}
.card .top{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:12.5px;color:var(--muted)}
.card p{margin:0;font-size:15px;color:var(--ink-2);line-height:1.55}
.card .prob{font-size:14px;color:var(--muted);border-left:2px solid var(--line);padding-left:12px}
.card .foot{margin-top:auto;padding-top:14px;border-top:1px solid var(--line);display:flex;gap:6px 16px;flex-wrap:wrap;font-size:13.5px;font-weight:600}
.card .foot a{white-space:nowrap}
.card .foot a{display:inline-flex;align-items:center;gap:5px}
.demos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.demo{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:16px;overflow:hidden;color:var(--ink);transition:box-shadow .2s,transform .2s}
.demo:hover{text-decoration:none;box-shadow:var(--shadow);transform:translateY(-2px)}
.shot{aspect-ratio:16/10;background:var(--surface-2);border-bottom:1px solid var(--line);overflow:hidden;position:relative}
.shot img{width:100%;height:100%;object-fit:cover;object-position:top left;display:block}
.demo .body{padding:20px 22px 22px;display:flex;flex-direction:column;gap:8px}.demo .body p{margin:0;font-size:14.5px;color:var(--muted)}
.demo .go{display:inline-flex;align-items:center;gap:6px;font-weight:600;font-size:14px;color:var(--link);margin-top:4px}
.cases{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;counter-reset:c}
.case{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:26px;display:flex;flex-direction:column;gap:12px}
.case .num{font:500 12.5px/1 var(--mono);color:var(--accent-ink)}.case p{margin:0;font-size:15px;color:var(--ink-2);line-height:1.6}.case .meta{margin-top:auto;font-size:13px;color:var(--muted)}
.approach{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:56px;align-items:start}
.principles{display:grid;gap:14px;margin:0;padding:0;list-style:none}
.principles li{display:grid;grid-template-columns:28px 1fr;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.principles .ic{color:var(--accent-ink);margin-top:2px}.principles b{display:block;font-family:var(--display);font-size:16px;margin-bottom:2px}.principles span{color:var(--muted);font-size:14.5px}
.contact{background:var(--navy);color:#E9EEF3;border-radius:22px;padding:48px;display:flex;justify-content:space-between;align-items:center;gap:28px;flex-wrap:wrap}
.contact h2{color:#fff}.contact p{margin:10px 0 0;color:#B9C6D3;max-width:52ch}
.contact .btn-primary{background:#fff;color:var(--navy)}
@media (max-width:980px){.hero-grid,.approach{grid-template-columns:1fr;gap:40px}.caps{grid-template-columns:repeat(2,minmax(0,1fr))}.grid,.demos,.cases{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){section{padding:64px 0}.hero{padding:64px 0}.caps,.grid,.demos,.cases{grid-template-columns:1fr}.contact{padding:32px}.stat .n{font-size:36px}}
"""


def site():
    n_prod = sum(p['status'] == 'In production' for p in projects)
    cases = data.get('case_studies', [])
    stats = [(len(projects), '', 'Projects built and documented'), (n_prod, '', 'Systems in daily production use'),
             (test_count(), '', 'Automated tests passing'), (len(cases), '', 'Documentation case studies')]
    stats_html = ''.join(f'<div class="stat"><div class="n">{n}<small>{s}</small></div><div class="l">{e(l)}</div></div>' for n, s, l in stats)

    caps = [('app', 'Desktop applications', 'Offline Python apps for locked-down, carrier-managed Windows workstations.'),
            ('flow', 'Workflow automation', 'Apps Script, Zapier, n8n and Slack wired into one reliable operating rhythm.'),
            ('shield', 'Compliance tooling', 'Data-policy rules encoded as data, audited continuously, fixed reversibly.'),
            ('learn', 'Training systems', 'Narrated video, quiz engines and remediation gates that onboard staff faster.')]
    caps_html = ''.join(f'<div class="cap">{icon(i,24)}<h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in caps)

    cards = []
    for p in projects:
        url = p['repo'] if p.get('visibility') == 'public' else None
        d = p.get('detail', {})
        prob = d.get('problem', '')
        foot = []
        if p.get('page'):
            foot.append(f'<a href="{e(p["page"])}">Details {icon("arrow",15)}</a>')
        if p.get('demo'):
            foot.append(f'<a href="{e(p["demo"]["url"])}">{"Live demo" if p["demo"]["kind"] == "live" else "Interface"} {icon("ext",14)}</a>')
        foot.append(f'<a href="{e(url)}">Source {icon("ext",14)}</a>' if url else '<span class="muted">Source available on request</span>')
        tags = ''.join(f'<span class="chip">{e(t)}</span>' for t in p['topics'][:5])
        cards.append(f"""<article class="card"><div class="top"><span class="pill {status_class(p['status'])}">{e(p['status'])}</span><span>{e(p['lang'])}</span></div>
<h3>{e(p['title'])}</h3><p>{e(p['tagline'])}</p>{f'<p class="prob">{inline(prob)}</p>' if prob else ''}
<div class="chips">{tags}</div><div class="foot">{''.join(foot)}</div></article>""")

    demos = []
    for p in projects:
        if p.get('demo') and p.get('preview'):
            dm = p['demo']
            demos.append(f"""<a class="demo" href="{e(dm['url'])}"><div class="shot"><img src="assets/previews/{e(p['name'])}.png" alt="Screenshot of {e(p['title'])}" loading="lazy" width="1440" height="900"></div>
<div class="body"><span class="eyebrow">{'Live' if dm['kind'] == 'live' else 'Interface preview'}</span><h3>{e(p['title'])}</h3><p>{e(dm.get('note') or p['tagline'])}</p><span class="go">{e(dm['label'])} {icon('ext',14)}</span></div></a>""")

    case_html = ''.join(f"""<article class="case"><span class="num">Case {i:02d}</span><h3>{e(c['title'])}</h3><p>{e(c['summary'])}</p>
<div class="meta">{e(c['status'])} · {fmt_date(c['date'])}</div></article>""" for i, c in enumerate(cases, 1))

    principles = [('Policy as data', 'Rules, blueprints and rubrics live in versioned JSON or YAML, so they change without a rebuild.'),
                  ('Reversible by default', 'Every automated change is journaled with a one-click undo, and baselines are locked before anything is scored.'),
                  ('Built for real constraints', 'Locked-down workstations, blocked add-ins and carrier portals with no API are treated as design inputs, not blockers.'),
                  ('Verified before shipped', 'Automated tests, deploy records and documented acceptance checks come with every release.')]
    pr_html = ''.join(f'<li>{icon("check",20)}<div><b>{e(t)}</b><span>{e(d)}</span></div></li>' for t, d in principles)

    desc = f'{author}: internal software, workflow automation, compliance tooling and training systems for insurance agency operations.'
    links = '<a class="hide-sm" href="#work">Work</a><a class="hide-sm" href="#demos">Demos</a><a class="hide-sm" href="#cases">Case studies</a><a class="hide-sm" href="#approach">Approach</a>'
    return f"""{head(f'{author} · SystemSerenity', desc, SITE, HOME_CSS)}<body>
{nav(links)}
<main>
<section class="hero"><div class="wrap hero-grid"><div>
<span class="eyebrow">{e(ROLE)}</span>
<h1>Operational clarity <em>at scale.</em></h1>
<p class="lede">I design and ship the internal software that runs a Florida insurance agency: compliance auditors on the file server, AI-assisted underwriting triage, offline desktop apps and training systems that onboard new staff.</p>
<div class="cta"><a class="btn btn-primary" href="#work">View selected work {icon('arrow',17)}</a><a class="btn btn-ghost" href="https://github.com/{owner}">{icon('github',17)} GitHub profile</a></div>
<div class="who"><b>{e(author)}</b><span>·</span><span>Central Florida</span></div>
</div><div class="stats" role="list" aria-label="At a glance">{stats_html}</div></div></section>

<section id="capabilities"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Capabilities</span><h2 style="margin-top:10px">What I build</h2>
<p>Four kinds of tools, all running inside the limits of a carrier-managed agency environment.</p></div></div>
<div class="caps">{caps_html}</div></div></section>

<section id="work"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Selected work</span><h2 style="margin-top:10px">Projects</h2>
<p>Each repository is a sanitized portfolio copy. Staff names, IDs and network details were replaced before publishing, and no client data is included.</p></div></div>
<div class="grid">{''.join(cards)}</div></div></section>

<section id="demos"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Try it</span><h2 style="margin-top:10px">Live demos</h2>
<p>Browser-based pieces you can open right now. The desktop applications run on Windows; their source and run instructions are in each repository.</p></div></div>
<div class="demos">{''.join(demos)}</div></div></section>

<section id="cases"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Documentation</span><h2 style="margin-top:10px">Case studies</h2>
<p>Operations work delivered as SOPs, training and monitoring programs rather than code.</p></div></div>
<div class="cases">{case_html}</div></div></section>

<section id="approach"><div class="wrap approach"><div><span class="eyebrow">Approach</span><h2 style="margin-top:10px">How the work gets done</h2>
<p class="lede" style="margin-top:16px">Small agencies can't afford fragile software. Each system here is built to be understood, audited and handed off, and to keep working when its author is out of the office.</p></div>
<ul class="principles">{pr_html}</ul></div></section>

<section style="padding-top:0;border-top:0"><div class="wrap"><div class="contact"><div><h2>See the code</h2><p>Every public project links to its full source, architecture diagram and run instructions.</p></div>
<a class="btn btn-primary" href="https://github.com/{owner}?tab=repositories">Browse repositories {icon('arrow',17)}</a></div></div></section>
</main>
{footer()}
</body></html>
"""


# ---- Project pages -------------------------------------------------------------------
PAGE_CSS = """
.crumbs{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--muted);padding-top:40px}
.crumbs a{display:inline-flex;align-items:center;gap:6px;color:var(--ink-2);font-weight:500}
.phero{padding:28px 0 56px}
.phero h1{font-size:clamp(36px,5.4vw,56px);line-height:1.05;font-weight:700;letter-spacing:-.035em;margin:18px 0 18px;max-width:20ch}
.meta{display:flex;flex-wrap:wrap;gap:10px 22px;align-items:center;margin-top:26px;font-size:14px;color:var(--muted)}
.meta b{color:var(--ink);font-weight:600}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.note-inline{display:flex;gap:10px;align-items:flex-start;margin-top:22px;font-size:14px;color:var(--muted);max-width:70ch}
.frame{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--surface);box-shadow:var(--shadow)}
.frame .bar{display:flex;align-items:center;gap:7px;padding:11px 14px;border-bottom:1px solid var(--line);background:var(--surface-2)}
.frame .bar i{width:10px;height:10px;border-radius:50%;background:var(--line)}
.frame .bar span{margin-left:10px;font:12px var(--mono);color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.frame img{display:block;width:100%;height:auto}
.caption{font-size:13.5px;color:var(--muted);margin-top:12px}
.ps{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:28px}
.panel .eyebrow{display:block;margin-bottom:12px}.panel p{margin:0;font-size:16px;color:var(--ink-2)}
.panel.sol{border-top:3px solid var(--accent)}.panel.prob{border-top:3px solid var(--steel)}
.hl{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:14px}
.hl li{display:grid;grid-template-columns:24px 1fr;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 20px;font-size:15px;color:var(--ink-2)}
.hl .ic{color:var(--accent-ink);margin-top:2px}
.diagram{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:32px;overflow-x:auto}
.diagram pre.mermaid{margin:0;display:flex;justify-content:center;font:13px var(--mono);color:var(--muted)}
.diagram svg{max-width:100%;height:auto}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px}
.notes{margin:0;padding-left:18px;color:var(--ink-2)}.notes li{margin:6px 0}
.disclaimer{background:var(--steel-tint);border-radius:14px;padding:18px 20px;font-size:14px;color:var(--ink-2);margin-top:22px}
.next{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.next a{flex:1 1 260px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 20px;color:var(--ink)}
.next a:hover{text-decoration:none;border-color:var(--ink-2)}.next small{display:block;color:var(--muted);font-size:12.5px;margin-bottom:4px}.next b{font-family:var(--display);font-size:17px}
.next a.r{text-align:right}
@media (max-width:820px){.ps,.hl,.two{grid-template-columns:1fr}}
@media (max-width:640px){section{padding:56px 0}.panel,.diagram{padding:22px}}
"""

MERMAID = """<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
const dark = matchMedia('(prefers-color-scheme: dark)').matches;
mermaid.initialize({startOnLoad:true,securityLevel:'strict',theme:'base',fontFamily:'Inter, system-ui, sans-serif',
 flowchart:{curve:'basis',padding:14,htmlLabels:true},
 themeVariables: dark ? {background:'#0E2236',primaryColor:'#12304A',primaryBorderColor:'#3A6EA5',primaryTextColor:'#ECF0F4',lineColor:'#6F8BA8',secondaryColor:'#113A3A',tertiaryColor:'#0E2236',fontSize:'14px'}
                      : {background:'#FFFFFF',primaryColor:'#EEF3F9',primaryBorderColor:'#3A6EA5',primaryTextColor:'#0B1F33',lineColor:'#7C8FA3',secondaryColor:'#E4F2F0',tertiaryColor:'#FFFFFF',fontSize:'14px'}});
</script>"""


def project_page(p, prev_p, next_p):
    d = p['detail']
    url = p['page']
    dm = p.get('demo')
    btns = []
    if dm:
        btns.append(f'<a class="btn btn-primary" href="{e(dm["url"])}">{icon("play",17)} {e(dm["label"])}</a>')
    btns.append(f'<a class="btn {"btn-ghost" if dm else "btn-primary"}" href="{e(p["repo"])}">{icon("code",17)} View source on GitHub</a>')
    kind = ('Runs in the browser' if dm and dm['kind'] == 'live' else
            'Windows desktop application' if 'desktop-app' in p['topics'] else
            'Script pipeline + HTML player' if dm else 'Source project')
    note = ''
    if dm and dm.get('note'):
        note = f'<p class="note-inline">{icon("doc",18)}<span>{e(dm["note"])}</span></p>'
    elif not dm and 'desktop-app' in p['topics']:
        note = f'<p class="note-inline">{icon("app",18)}<span>This is an offline Windows desktop app, so there is no hosted demo. The repository has setup steps, the test suite and full technical notes.</span></p>'

    shot = ''
    if p.get('preview') and dm:
        shot = f"""<section style="padding-top:0;border-top:0"><div class="wrap"><div class="frame"><div class="bar"><i></i><i></i><i></i><span>{e(dm['url'].replace('https://',''))}</span></div>
<a href="{e(dm['url'])}"><img src="{e(p['preview'])}" alt="Screenshot of {e(p['title'])}" width="1440" height="900"></a></div>
<p class="caption">{e(p['title'])}, sanitized portfolio build. Logos are neutral placeholders.</p></div></section>"""

    hl = ''.join(f'<li>{icon("check",20)}<span>{inline(h)}</span></li>' for h in d['highlights'])
    stack = ''.join(f'<span class="chip">{e(s)}</span>' for s in d.get('stack', []))
    notes = ''.join(f'<li>{inline(n)}</li>' for n in d.get('notes', []))
    diagram = ''
    if d.get('diagram'):
        diagram = f"""<section><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Architecture</span><h2 style="margin-top:10px">How it fits together</h2></div></div>
<div class="diagram"><pre class="mermaid">{e(d['diagram'])}</pre></div></div></section>"""

    nxt = f"""<section><div class="wrap next">
<a href="{e(prev_p['page'])}"><small>← Previous project</small><b>{e(prev_p['title'])}</b></a>
<a class="r" href="{e(next_p['page'])}"><small>Next project →</small><b>{e(next_p['title'])}</b></a></div></section>"""

    links = f'<a class="hide-sm" href="{SITE}#work">Work</a><a class="hide-sm" href="{SITE}#demos">Demos</a><a class="hide-sm" href="{SITE}#cases">Case studies</a>'
    return f"""{head(f"{p['title']} · {author}", p['tagline'], url, PAGE_CSS)}<body>
{nav(links)}
<main>
<div class="wrap crumbs"><a href="{SITE}#work">{icon('back',16)} All work</a><span>/</span><span>{e(p['title'])}</span></div>
<section class="phero" style="border-top:0"><div class="wrap">
<span class="pill {status_class(p['status'])}">{e(p['status'])}</span>
<h1>{e(p['title'])}</h1>
<p class="lede">{e(p['tagline'])}</p>
<div class="meta"><span><b>Shipped</b> {fmt_date(p['shipped'])}</span><span><b>Language</b> {e(p['lang'])}</span><span><b>Format</b> {e(kind)}</span></div>
<div class="cta">{''.join(btns)}</div>{note}
</div></section>
{shot}
<section><div class="wrap"><div class="ps">
<div class="panel prob"><span class="eyebrow">The problem</span><p>{inline(d['problem'])}</p></div>
<div class="panel sol"><span class="eyebrow">The solution</span><p>{inline(d['solution'])}</p></div></div></div></section>
<section><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Highlights</span><h2 style="margin-top:10px">What it does well</h2></div></div>
<ul class="hl">{hl}</ul></div></section>
{diagram}
<section><div class="wrap two"><div><span class="eyebrow">Stack</span><h2 style="margin:10px 0 18px">Built with</h2><div class="chips">{stack}</div></div>
<div><span class="eyebrow">Notes</span><h2 style="margin:10px 0 14px">Good to know</h2><ul class="notes">{notes}</ul>
<div class="disclaimer">Portfolio copy. Built for an Allstate-affiliated insurance agency in Florida. Staff names, emails, network addresses, service IDs and brand logos were replaced with fictional or placeholder values before publishing. No client data is included.</div></div></div></section>
{nxt}
</main>
{footer()}
{MERMAID if d.get('diagram') else ''}
</body></html>
"""


# ---- Profile README -------------------------------------------------------------------
def profile_readme():
    rows = []
    for p in projects:
        url = p['repo'] if p.get('visibility') == 'public' else None
        name = f"**[{p['title']}]({p['page']})**" if p.get('page') else (f"**[{p['title']}]({url})**" if url else f"**{p['title']}** *(private)*")
        extra = []
        if p.get('demo'):
            extra.append(f"[{'Live demo' if p['demo']['kind'] == 'live' else 'Interface'}]({p['demo']['url']})")
        if url:
            extra.append(f"[Source]({url})")
        rows.append(f"| {name} | {p['status']} | {fmt_date(p['shipped']) if p['shipped'] else '—'} | {p['tagline']} | {' · '.join(extra)} |")
    cs = '\n'.join(f"- **{c['title']}** · {c['status']}, {fmt_date(c['date'])}  \n  {c['summary']}" for c in data.get('case_studies', []))
    return f"""<picture><source media="(prefers-color-scheme: dark)" srcset="assets/ss-mark-dark.png"><img src="assets/ss-mark.png" width="56" alt="SystemSerenity"></picture>

# {author}

**{ROLE}** · *SystemSerenity: {BRAND['tagline']}*

I design and ship the internal software that runs a Florida insurance agency: compliance auditors on the file server, AI-assisted underwriting triage, offline desktop apps and training systems that onboard new staff.

**[View the portfolio site →]({SITE})**

**Focus:** Python desktop apps · Google Apps Script · workflow automation (Zapier, n8n, Slack) · data-policy compliance · training systems

## Projects

| Project | Status | Last shipped | What it does | Links |
|---|---|---|---|---|
{chr(10).join(rows)}

## Case studies

{cs}

<sub>Repositories are sanitized portfolio copies: staff names, IDs and network details replaced; no client data. Generated from `portfolio.json` · updated {fmt_date(data['updated'])}.</sub>
"""


# ---- Write outputs -----------------------------------------------------------------------
(ROOT / 'PROFILE_README.md').write_text(profile_readme(), encoding='utf-8')
site_dir = ROOT / 'site'
(site_dir / 'assets' / 'previews').mkdir(parents=True, exist_ok=True)
(site_dir / 'index.html').write_text(site(), encoding='utf-8')
(site_dir / '.nojekyll').write_text('', encoding='utf-8')
for f in ('ss-mark.png', 'ss-mark-dark.png'):
    shutil.copy(ROOT / 'assets' / f, site_dir / 'assets' / f)
for f in (ROOT / 'assets' / 'previews').glob('*.png'):
    shutil.copy(f, site_dir / 'assets' / 'previews' / f.name)

paged = [p for p in projects if p.get('page')]
for i, p in enumerate(paged):
    out = ROOT / 'pages' / p['name']
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(project_page(p, paged[i - 1], paged[(i + 1) % len(paged)]), encoding='utf-8')
print(f'built site ({len(projects)} projects) + {len(paged)} project pages')
