"""Build Board 5 (November 6, 2026): chapter 02's writing rules, each with a real before and an after, for Dustin.

Usage:
    python3 -I work/build/scripts/phase-2/voice_board5_build.py

Reads the editor's content (work/boards/phase-2/voice/20261106_Voice-Rules-Content.json) and the main session's record
(work/boards/phase-2/voice/20261106_Board-5-Studio-Record.json: the ask, process, checks, change log). Writes:
    work/boards/20261106_Voice-Writing-Rules-Board.html            (the studio record, a full document)
    <scratchpad>/publish/20261106_Voice-Writing-Rules-Board.html   (the publish copy for the private page)
Quoted copy (every before and after) is set in Lora Italic, the brand's face for quoted words (DR-47); everything
else in Inter Tight and Inter. The page carries no working red.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
V = ROOT / 'work/boards/phase-2/voice'
OUT = ROOT / 'work/boards/20261106_Voice-Writing-Rules-Board.html'
PUB = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/72a6dd5d-b3ac-5a79-9ac0-32d5f5fbde66/scratchpad/publish/20261106_Voice-Writing-Rules-Board.html')
C = json.loads((V / '20261106_Voice-Rules-Content.json').read_text())
REC = V / '20261106_Board-5-Studio-Record.json'
R = json.loads(REC.read_text()) if REC.exists() else {}


def copy(s):
    """Curly quotes and apostrophes, and the true minus before a figure."""
    s = str(s)
    s = re.sub(r'"([^"<>]*)"', '“\\1”', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '’', s)
    s = re.sub(r"(?<![\w'])'([^'\n]{1,80}?)'(?![\w])", '‘\\1’', s)
    return re.sub(r'(?<![\w.\-])-(?=\d)', '−', s)


E = lambda s: html.escape(copy(s), quote=True)
Q = lambda s: html.escape(str(s), quote=True)      # quoted copy stays exactly as written


CSS = '''
/* Board 5. The Board 3 and 4 frame: one 1280 px column on Newsprint, a Prussian decision band. Each rule is a card:
   its name and rule in Inter, then the before and the after side by side, quoted in Lora Italic, chipped like the
   charts' evidence label (outlined for before, solid Charcoal for after). No working red on the page. */
:root{color-scheme:light;--bg:#DCD9D2;--surface:#E6E3DD;--white:#FFFFFF;--fg:#121212;--muted:#4E535B;--rule:#5D636D;
--hair:#C9C6BF;--prussian:#1F2D5A;--newsprint:#DCD9D2;--display:"Inter Tight","Helvetica Neue",Arial,sans-serif;
--body:"Inter","Helvetica Neue",Arial,sans-serif;--quote:"Lora",Georgia,serif}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:400 1rem/1.6 var(--body)}
a{color:inherit;text-underline-offset:3px}a:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--fg);outline-offset:3px}
.board{max-width:1280px;margin:0 auto;padding-block:40px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.mast{display:flex;justify-content:space-between;align-items:baseline;gap:16px;border-bottom:2px solid var(--fg);padding-bottom:14px;flex-wrap:wrap}
.mast b{font:800 1.25rem/1 var(--display);letter-spacing:-.02em}.mast span{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.eyebrow{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:28px 0 0}
h1,h2,h3{font-family:var(--display);font-weight:800;letter-spacing:-.025em;text-wrap:balance;margin:0}
h1{font-size:clamp(2.25rem,6vw,4.25rem);line-height:1.02;margin-top:10px;max-width:16ch}
h2{font-size:clamp(1.5rem,3vw,2.25rem);line-height:1.08;margin:0 0 10px}
h3{font-size:1.3125rem;line-height:1.2;letter-spacing:-.015em}
h4{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:22px 0 8px}
p{margin:0 0 12px;max-width:68ch}.deck{font-size:1.1875rem;line-height:1.5;max-width:62ch;margin-top:16px}
section{border-top:1px solid var(--rule);margin-top:48px;padding-top:32px}
.secnum{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;color:var(--muted);margin:0 0 6px}
.ask{background:var(--white);border:1px solid var(--rule);padding:22px 24px;margin-top:28px}
.ask ol{margin:0;padding-left:1.3em}.ask li{margin:0 0 8px;max-width:84ch}.reply{font:italic 400 1.0625rem/1.5 var(--quote);margin:10px 0 0}
.toc{display:flex;flex-wrap:wrap;gap:6px 22px;margin:22px 0 0;padding:12px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.toc a{font:600 .9375rem/1.4 var(--body);text-decoration:none;display:inline-flex;align-items:center;min-height:44px}.toc a:hover{text-decoration:underline}
.narr{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,22rem);gap:48px;align-items:start}
.narr .body p{font-size:1.1875rem;line-height:1.6;max-width:60ch}
.locked{border-top:2px solid var(--fg);padding-top:12px}.locked p{font:italic 400 1.125rem/1.45 var(--quote);margin:0 0 4px}
.locked small{display:block;font:700 .8125rem/1.4 var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 14px}
.group{margin-top:44px}.group>p{font-size:1.0625rem}
.rules{display:grid;gap:0}
.rule{border-top:2px solid var(--fg);padding:18px 0 26px}
.rule-h{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.rid{font:700 .8125rem/1 var(--body);letter-spacing:.06em;color:var(--muted);font-variant-numeric:tabular-nums}
.rtext{font-size:1.0625rem;margin:8px 0 6px;max-width:72ch}
.terms{font-size:.9375rem;color:var(--muted);margin:0 0 6px;max-width:72ch}
.ba{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-top:14px}
.ex{margin:0;padding:16px 18px;border:1px solid var(--rule);background:var(--surface);min-width:0}
.ex.after{background:var(--white);border-color:var(--fg);box-shadow:inset 0 3px 0 var(--fg)}
.exh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 10px}
.chip{display:inline-block;font:700 .8125rem/1 var(--body);letter-spacing:.06em;text-transform:uppercase;padding:5px 8px;border:1px solid var(--fg)}
.chip.solid{background:var(--fg);color:var(--white)}
.chip.ill{border-style:dashed}
.src{font-size:.875rem;color:var(--muted)}
.ex blockquote{margin:0;font:italic 400 1.125rem/1.55 var(--quote);overflow-wrap:anywhere}
.why{font-size:.9375rem;margin:12px 0 0;max-width:80ch}.why b{font-weight:700}
.tw{overflow-x:auto;border:1px solid var(--rule);background:var(--white)}
table{border-collapse:collapse;width:100%;font-size:.9375rem;min-width:720px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--hair)}
thead th{font:700 .8125rem/1.3 var(--body);letter-spacing:.02em;text-transform:uppercase;color:var(--muted);background:var(--surface)}
td.exq{font:italic 400 1rem/1.5 var(--quote)}
ol.check{list-style:none;counter-reset:c;margin:12px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px}
ol.check li{counter-increment:c;display:grid;grid-template-columns:2rem minmax(0,1fr);gap:10px;padding:12px 0;border-bottom:1px solid var(--rule);font-size:1.0625rem}
ol.check li::before{content:counter(c);font:800 1.25rem/1.2 var(--display)}
.decision{background:var(--prussian);color:var(--newsprint);padding-block:28px;padding-left:max(20px,3vw);padding-right:max(20px,3vw);margin-top:48px}
.decision *{color:inherit}.decision h2{color:#FFFFFF}.decision ol{padding-left:1.3em;margin:0}.decision li{margin:0 0 16px;max-width:88ch}
.decision .rec{display:block;margin-top:4px;font-weight:700}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:28px}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 8px;max-width:70ch}
.small{font-size:.875rem;color:var(--muted)}
code{font:500 max(13px,.875em)/1.4 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
@media (max-width:900px){.narr{grid-template-columns:minmax(0,1fr);gap:24px}.ba{grid-template-columns:minmax(0,1fr)}ol.check{grid-template-columns:minmax(0,1fr)}}
@media (max-width:520px){.ask{padding:18px 16px}.ex{padding:14px}}
'''


def rule_card(r):
    ill = '<span class="chip ill">Illustrative</span>' if r.get('illustrative') else ''
    terms = f'<p class="terms"><b>In plain words:</b> {E(r["terms"])}</p>' if r.get('terms') else ''
    return f'''<article class="rule" id="{E(r["id"].lower())}" aria-labelledby="{E(r["id"].lower())}-h">
<div class="rule-h"><span class="rid">{E(r["id"])}</span><h3 id="{E(r["id"].lower())}-h">{E(r["name"])}</h3></div>
<p class="rtext">{E(r["rule"])}</p>{terms}
<div class="ba"><figure class="ex before"><figcaption class="exh"><span class="chip">Before</span>{ill}<span class="src">{E(r["before_source"])}</span></figcaption>
<blockquote>{Q(r["before"])}</blockquote></figure>
<figure class="ex after"><figcaption class="exh"><span class="chip solid">After</span></figcaption><blockquote>{Q(r["after"])}</blockquote></figure></div>
<p class="why"><b>What changed.</b> {E(r["why"])}</p></article>'''


def build():
    groups = C['groups']
    n_rules = sum(len(g['rules']) for g in groups)
    n_real = sum(1 for g in groups for r in g['rules'] if not r.get('illustrative'))
    gid = lambda i: f'g{i + 1}'
    toc = ''.join(f'<a href="#{gid(i)}">{E(g["name"])}</a>' for i, g in enumerate(groups))
    gsec = ''.join(f'''<div class="group" id="{gid(i)}"><p class="secnum">GROUP {i + 1} OF {len(groups)}</p><h2>{E(g["name"])}</h2><p>{E(g["intro"])}</p>
<div class="rules">{"".join(rule_card(r) for r in g["rules"])}</div></div>''' for i, g in enumerate(groups))
    house = ''.join(f'<tr><th scope="row">{E(h["id"])}</th><td><b>{E(h["name"])}</b><br>{E(h["rule"])}</td><td class="exq">{Q(h.get("example", ""))}</td></tr>' for h in C.get('house_rules', []))
    check = ''.join(f'<li><span>{E(q)}</span></li>' for q in C.get('checklist', []))
    narr = ''.join(f'<p>{E(p)}</p>' for p in C['narrative'])
    L = lambda k: ''.join(f'<li>{x}</li>' for x in R.get(k, []))
    ask = ''.join(f'<li>{E(x)}</li>' for x in R.get('ask', []))
    decisions = ''.join(f'<li><b>{E(d["q"])}</b> {E(d["text"])}<span class="rec">Recommended: {E(d["rec"])}</span></li>' for d in R.get('decisions', []))
    locked = ('<div class="locked"><p>“We explain how a decision is made and give you a practical way to take part.”</p><small>Reader promise</small>'
              '<p>“Clarity is our duty. Action is our promise.”</p><small>Editorial commitment</small>'
              '<p>“A country that answers to its people.”</p><small>Tagline</small></div>')
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="overview">
<title>Oath &amp; Action Writing Rules</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><main class="board" data-view-root="overview">
<header>
<div class="mast"><b>Oath &amp; Action</b><span>Brand Guide, Edition 06 · Phase 2 · Chapter 02, Voice</span></div>
<p class="eyebrow">Board 5 · November 6, 2026</p>
<h1>{E(C["title"])}</h1>
<p class="deck">{E(C["deck"])}</p>
<div class="ask"><h3>What you are asked</h3><ol>{ask}</ol><p class="reply">{E(R.get("sample_reply", ""))}</p></div>
<nav class="toc" aria-label="On this board"><a href="#why">Why we write this way</a>{toc}<a href="#house">House rules</a><a href="#checklist">Before you publish</a><a href="#decisions">Decisions</a><a href="#checks">Checks</a></nav>
</header>
<section id="why" aria-labelledby="h-why"><p class="secnum">CHAPTER 02 · VOICE</p><h2 id="h-why">Why we write this way</h2>
<div class="narr"><div class="body">{narr}</div>{locked}</div>
<p class="small" style="margin-top:20px">{n_rules} rules in {len(groups)} groups. {n_real} of the befores are real Oath &amp; Action copy, quoted exactly with their source; the rest are written to show the fault and labeled Illustrative. Every after keeps the before’s facts.</p></section>
{gsec}
<section id="house" aria-labelledby="h-house"><p class="secnum">HOUSE RULES</p><h2 id="h-house">The rules every page already follows</h2>
<div class="tw" role="region" tabindex="0" aria-label="House rules"><table><thead><tr><th scope="col">Rule</th><th scope="col">What it asks</th><th scope="col">Written correctly</th></tr></thead><tbody>{house}</tbody></table></div></section>
<section id="checklist" aria-labelledby="h-check"><p class="secnum">BEFORE YOU PUBLISH</p><h2 id="h-check">Read it aloud, then ask</h2><ol class="check">{check}</ol></section>
<div class="decision" id="decisions" role="region" aria-labelledby="h-dec"><h2 id="h-dec">Decisions on this board</h2><ol>{decisions}</ol></div>
<section id="process" aria-labelledby="h-proc"><p class="secnum">HOW THIS WAS MADE</p><h2 id="h-proc">The editor wrote it, the creative director read it against itself</h2><ol>{L("process")}</ol></section>
<section id="checks" aria-labelledby="h-checks"><p class="secnum">CHECKS</p><h2 id="h-checks">What was tested</h2>
<div class="cols"><div><h4>Tested</h4><ul class="facts">{L("tested")}</ul></div><div><h4>Not tested</h4><ul class="facts">{L("not_tested")}</ul></div></div></section>
<section id="changes" aria-labelledby="h-ch"><p class="secnum">CHANGE LOG</p><h2 id="h-ch">Files</h2>
<p class="small">Paths are relative to <code>oath-and-action-v6-brand-guide/</code>.</p>
<div class="cols"><div><h4>Created</h4><ul class="facts">{L("changelog_created")}</ul></div><div><h4>Modified</h4><ul class="facts">{L("changelog_modified")}</ul></div></div></section>
</main></body></html>'''
    # a before may show the fault it teaches (an em dash among them); nothing else on the page may carry one
    rest = re.sub(r'<figure class="ex before">.*?</figure>', '', re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S), flags=re.S)
    assert '\u2014' not in rest, 'em dash on the board outside a before'
    OUT.write_text(page)
    head, body = re.split(r'</head>\s*<body>', page, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    head = head.replace('<title>Oath &amp; Action Writing Rules</title>\n', '')
    PUB.parent.mkdir(parents=True, exist_ok=True)
    PUB.write_text('<title>Oath &amp; Action Writing Rules</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head + re.sub(r'</body>\s*</html>\s*$', '', body))
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1e3:.0f} kB; {n_rules} rules, {n_real} real befores')


if __name__ == '__main__':
    build()
