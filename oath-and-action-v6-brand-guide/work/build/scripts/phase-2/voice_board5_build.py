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


AMP = (ROOT / 'work/build/assets/identity/ampersand/20261028_Amp-B-24px-Master.svg').read_text()
AMP = re.sub(r'<title>.*?</title>', '', AMP).replace('<svg ', '<svg class="hamp" aria-hidden="true" focusable="false" ', 1)


def marks(s, kind):
    """[-removed-] in a before and [+repair+] in an after become del and ins, drawn as dotted and solid underlines."""
    t = html.escape(curl(s), quote=False)
    t = re.sub(r'\[-(.+?)-\]', r'<del>\1</del>', t)
    t = re.sub(r'\[\+(.+?)\+\]', r'<ins>\1</ins>', t)
    return t


def curl(s):
    """Quote marks only: a quoted before keeps every other character as published."""
    s = str(s)
    s = re.sub(r'"([^"<>]*)"', '“\\1”', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '’', s)
    return re.sub(r"(?<![\w'])'([^'\n]{1,80}?)'(?![\w])", '‘\\1’', s)


CSS = """
/* Board 5. The Board 3 and 4 frame on Newsprint, with a Prussian decision band. Each rule is a spread: the rule on the
   left, and on the right its before and after joined by the hinge divider (a hairline broken by ampersand B in
   Charcoal, D1-22). Specimens run in Inter as copy does in production; Lora Italic carries only the locked lines.
   A dotted underline marks what a rule removes, a solid one the repair. No working red on the page. */
:root{color-scheme:light;--bg:#DCD9D2;--surface:#E6E3DD;--white:#FFFFFF;--fg:#121212;--muted:#4E535B;--rule:#5D636D;
--hair:#C9C6BF;--prussian:#1F2D5A;--newsprint:#DCD9D2;--display:"Inter Tight","Helvetica Neue",Arial,sans-serif;
--body:"Inter","Helvetica Neue",Arial,sans-serif;--quote:"Lora",Georgia,serif}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:400 1rem/1.6 var(--body)}
a{color:inherit;text-underline-offset:3px}a:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--fg);outline-offset:3px}
.board{max-width:1280px;margin:0 auto;padding-block:40px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.mast{display:flex;justify-content:space-between;align-items:baseline;gap:16px;border-bottom:2px solid var(--fg);padding-bottom:14px}
.mast b{font:800 1.25rem/1 var(--display);letter-spacing:-.02em;white-space:nowrap}.mast span{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);text-align:right}
.eyebrow{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:28px 0 0}
h1,h2,h3{font-family:var(--display);font-weight:800;letter-spacing:-.025em;text-wrap:balance;margin:0}
h1{font-size:clamp(2.5rem,7vw,5rem);line-height:1;margin-top:10px;max-width:14ch}
h2{font-size:clamp(1.5rem,3vw,2.25rem);line-height:1.08;margin:0 0 10px}
h3{font-size:1.375rem;line-height:1.2;letter-spacing:-.015em}
h4{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:22px 0 8px}
p{margin:0 0 12px;max-width:68ch}.deck{font-size:1.25rem;line-height:1.5;max-width:58ch;margin-top:18px}
section{border-top:1px solid var(--rule);margin-top:48px;padding-top:32px}
.secnum{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;color:var(--muted);margin:0 0 6px}
.ask{background:var(--white);border:1px solid var(--rule);padding:22px 24px;margin-top:28px}
.ask ol{margin:0;padding-left:1.3em}.ask li{margin:0 0 8px;max-width:84ch}.reply{font:italic 400 1.0625rem/1.5 var(--quote);margin:10px 0 0}
.toc{display:flex;flex-wrap:wrap;gap:6px 22px;margin:22px 0 0;padding:12px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.toc a{font:600 .9375rem/1.4 var(--body);text-decoration:none;display:inline-flex;align-items:center;min-height:44px;white-space:nowrap}.toc a:hover{text-decoration:underline}
.narr .body p{font-size:1.25rem;line-height:1.6;max-width:58ch}
.narr .body q,.narr .body .lk{font:italic 400 1.0625em/1.5 var(--quote);quotes:none}
.index{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));gap:24px 32px;margin-top:20px}
.index h4{margin:0 0 6px;color:var(--fg)}.index h4 span{display:block;font:800 2rem/1 var(--display);letter-spacing:-.02em;margin-bottom:6px}
.index ol{list-style:none;margin:0;padding:0}.index li{border-top:1px solid var(--hair)}
.index a{display:flex;gap:10px;align-items:baseline;min-height:36px;padding:6px 0;text-decoration:none;font-size:.9375rem}.index a:hover span+span{text-decoration:underline}
.index a span:first-child{font:700 .8125rem/1 var(--body);color:var(--muted);font-variant-numeric:tabular-nums;min-width:2.4em}
.group{margin-top:64px;border-top:2px solid var(--fg);padding-top:20px}
.ghead{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 24px;align-items:start;margin-bottom:8px}
.gnum{font:800 clamp(3.5rem,8vw,6rem)/.85 var(--display);letter-spacing:-.04em;grid-row:1/3}
.ghead p{font-size:1.0625rem;margin:6px 0 0}
.legend{display:flex;flex-wrap:wrap;gap:6px 24px;font-size:.875rem;color:var(--muted);margin:14px 0 0}
.rule{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:24px 48px;border-top:1px solid var(--rule);padding:22px 0 30px}
.rule:first-of-type{border-top:0}
.rule-h{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.rid{font:700 .8125rem/1 var(--body);letter-spacing:.06em;color:var(--muted);font-variant-numeric:tabular-nums}
.rtext{font-size:1.0625rem;margin:10px 0 8px}
.terms{font-size:.9375rem;color:var(--muted);margin:0 0 8px}.terms b{color:var(--fg)}
.why{font-size:.9375rem;margin:14px 0 0}.why b{font-weight:700}
.pair{min-width:0}
.ex{margin:0;padding:18px 20px;border:1px solid var(--rule);background:var(--surface)}
.ex.after{background:var(--white);border-color:var(--fg)}
.exh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 12px}
.chip{display:inline-block;font:700 .8125rem/1 var(--body);letter-spacing:.06em;text-transform:uppercase;padding:5px 8px;border:1px solid var(--fg)}
.chip.solid{background:var(--fg);color:var(--white)}.chip.ill{border-style:dashed}
.src{font-size:.875rem;color:var(--muted)}
.ex blockquote{margin:0;font:400 1.375rem/1.5 var(--body);letter-spacing:-.005em;overflow-wrap:anywhere}
del{text-decoration:underline dotted 2px var(--rule);text-underline-offset:5px;color:inherit}
ins{text-decoration:underline solid 2px var(--fg);text-underline-offset:5px;color:inherit}
.hinge{display:flex;align-items:center;gap:14px;margin:12px 0;color:var(--fg)}
.hinge::before,.hinge::after{content:"";flex:1;height:1px;background:var(--fg)}
.hamp{width:21px;height:24px;flex:none;color:var(--fg)}
.tw{overflow-x:auto;border:1px solid var(--rule);background:var(--white)}
table{border-collapse:collapse;width:100%;font-size:.9375rem;font-variant-numeric:tabular-nums}
th,td{text-align:left;vertical-align:top;padding:12px 14px;border-bottom:1px solid var(--hair)}
thead th{font:700 .8125rem/1.3 var(--body);letter-spacing:.02em;text-transform:uppercase;color:var(--muted);background:var(--surface)}
td.exq{font-size:1rem}
ol.check{list-style:none;counter-reset:c;margin:12px 0 0;padding:0;columns:2;column-gap:48px}
ol.check li{counter-increment:c;display:grid;grid-template-columns:2.25rem minmax(0,1fr);gap:10px;padding:14px 0;border-bottom:1px solid var(--rule);font-size:1.0625rem;break-inside:avoid}
ol.check li::before{content:counter(c);font:800 1.375rem/1.15 var(--display)}
.decision{background:var(--prussian);color:var(--newsprint);padding-block:28px;padding-left:max(20px,3vw);padding-right:max(20px,3vw);margin-top:56px}
.decision *{color:inherit}.decision h2{color:#FFFFFF}.decision ol{padding-left:1.3em;margin:0}.decision li{margin:0 0 16px;max-width:88ch}
.decision .rec{display:block;margin-top:4px;font-weight:700}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:28px}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 8px;max-width:70ch}
.small{font-size:.875rem;color:var(--muted)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
code{font:500 max(13px,.875em)/1.4 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.short{display:none}
@media (max-width:900px){.rule{grid-template-columns:minmax(0,1fr);gap:16px}ol.check{columns:1}}
@media (max-width:720px){.long{display:none}.short{display:inline}
.toc{flex-wrap:nowrap;overflow-x:auto;gap:4px 18px;scrollbar-width:thin}
.ex blockquote{font-size:1.1875rem}
table.house,table.house tbody,table.house tr,table.house th,table.house td{display:block;width:100%}
table.house thead{display:none}table.house tr{border-bottom:1px solid var(--rule);padding:12px 0}
table.house th,table.house td{border:0;padding:4px 14px}
table.house td.exq::before{content:"Written correctly: ";font:700 .8125rem/1.4 var(--body);letter-spacing:.04em;color:var(--muted)}}
@media (max-width:520px){.ask{padding:18px 16px}.ex{padding:14px 16px}.ghead{grid-template-columns:minmax(0,1fr)}.gnum{grid-row:auto}}
"""


def rule_card(r, gname):
    ill = '<span class="chip ill">Illustrative</span>' if r.get('illustrative') else ''
    terms = f'<p class="terms">{E(r["terms"])}</p>' if r.get('terms') else ''
    rid = E(r['id'].lower())
    return f'''<article class="rule" id="{rid}" aria-labelledby="{rid}-h">
<div><div class="rule-h"><span class="rid">{E(r["id"])}</span><h3 id="{rid}-h">{E(r["name"])}</h3></div>
<p class="rtext">{E(r["rule"])}</p>{terms}<p class="why"><b>What changed.</b> {E(r["why"])}</p></div>
<div class="pair"><figure class="ex before"><figcaption class="exh"><span class="chip">Before</span>{ill}<span class="src">{E(r["before_source"])}</span></figcaption>
<blockquote>{marks(r["before"], "before")}</blockquote></figure>
<div class="hinge">{AMP}<span class="sr">becomes</span></div>
<figure class="ex after"><figcaption class="exh"><span class="chip solid">After</span>{ill}</figcaption><blockquote>{marks(r["after"], "after")}</blockquote></figure></div></article>'''


LOCKED = ['We explain how a decision is made and give you a practical way to take part.', 'Clarity is our duty. Action is our promise.',
          'A country that answers to its people.', 'Help people understand and improve the rules that shape their lives.']


def narrative_html(p):
    t = E(p)
    for line in LOCKED:      # the locked lines, quoted exactly, take Lora Italic: the brand's face for quoted words
        q = html.escape(curl(line), quote=True)
        t = t.replace(f'“{q}”', f'<span class="lk">“{q}”</span>')
    return t


def build():
    groups = C['groups']
    n_rules = sum(len(g['rules']) for g in groups)
    n_ill = sum(1 for g in groups for r in g['rules'] if r.get('illustrative'))
    gid = lambda i: f'g{i + 1}'
    index = ''.join(f'<div><h4><span>{i + 1:02d}</span>{E(g["name"])}</h4><ol>'
                    + ''.join(f'<li><a href="#{E(r["id"].lower())}"><span>{E(r["id"])}</span><span>{E(r["name"])}</span></a></li>' for r in g['rules'])
                    + '</ol></div>' for i, g in enumerate(groups))
    legend = ('<p class="legend"><span><del>Dotted underline</del>: what the rule removes</span>'
              '<span><ins>Solid underline</ins>: the repair</span><span>Illustrative: written to show the fault, not quoted</span></p>')
    gsec = ''.join(f'''<section class="group" id="{gid(i)}" aria-labelledby="{gid(i)}-h"><div class="ghead"><span class="gnum" aria-hidden="true">{i + 1:02d}</span>
<h2 id="{gid(i)}-h">{E(g["name"])}</h2><p>{E(g["intro"])}</p></div>{legend}
{"".join(rule_card(r, g["name"]) for r in g["rules"])}</section>''' for i, g in enumerate(groups))
    house = ''.join(f'<tr><th scope="row">{E(h["id"])} · {E(h["name"])}</th><td>{E(h["rule"])}</td><td class="exq">{E(h.get("example", ""))}</td></tr>' for h in C.get('house_rules', []))
    check = ''.join(f'<li><span>{E(q)}</span></li>' for q in C.get('checklist', []))
    narr = ''.join(f'<p>{narrative_html(p)}</p>' for p in C['narrative'])
    L = lambda k: ''.join(f'<li>{x}</li>' for x in R.get(k, []))
    ask = ''.join(f'<li>{E(x)}</li>' for x in R.get('ask', []))
    decs = C.get('decisions', []) + R.get('decisions', [])
    decisions = ''.join(f'<li><b>{E(d["q"])}</b> {E(d["text"])}<span class="rec">Recommended: {E(d["rec"])}</span></li>' for d in decs)
    title = E(C['title']).replace('Oath &amp; Action', 'Oath&nbsp;&amp;&nbsp;Action')
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="overview">
<title>Oath &amp; Action Writing Rules</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><main class="board" data-view-root="overview">
<header>
<div class="mast"><b>Oath &amp; Action</b><span><span class="long">Brand Guide, Edition 06 · Phase 2 · </span>Chapter 02, Voice</span></div>
<p class="eyebrow">Board 5 · November 6, 2026</p>
<h1>{title}</h1>
<p class="deck">{E(C["deck"])}</p>
<div class="ask"><h3>What you are asked</h3><ol>{ask}</ol><p class="reply">{E(R.get("sample_reply", ""))}</p></div>
<nav class="toc" aria-label="On this board"><a href="#why">Why we write this way</a><a href="#rules-index">All {n_rules} rules</a>{"".join(f'<a href="#{gid(i)}">{E(g["name"])}</a>' for i, g in enumerate(groups))}<a href="#house">House rules</a><a href="#checklist">Before you publish</a><a href="#decisions">Decisions</a><a href="#checks">Checks</a></nav>
</header>
<section id="why" aria-labelledby="h-why"><p class="secnum">CHAPTER 02 · VOICE</p><h2 id="h-why">Why we write this way</h2>
<div class="narr"><div class="body">{narr}</div></div></section>
<section id="rules-index" aria-labelledby="h-idx"><p class="secnum">THE RULES</p><h2 id="h-idx">All {n_rules} rules, in {len(groups)} groups</h2>
<p>{E(C.get("rule_index_intro", ""))}</p><div class="index">{index}</div>
<p class="small" style="margin-top:18px">Each before is quoted exactly from Oath &amp; Action’s own writing, with its source named, except the {n_ill} marked Illustrative, which the editor wrote to show the fault.</p></section>
{gsec}
<section id="house" aria-labelledby="h-house"><p class="secnum">HOUSE RULES</p><h2 id="h-house">The house rules for every page</h2>
<div class="tw" role="region" tabindex="0" aria-label="House rules"><table class="house"><thead><tr><th scope="col">Rule</th><th scope="col">What it asks</th><th scope="col">Written correctly</th></tr></thead><tbody>{house}</tbody></table></div></section>
<section id="checklist" aria-labelledby="h-check"><p class="secnum">BEFORE YOU PUBLISH</p><h2 id="h-check">Read it aloud, then ask</h2><ol class="check">{check}</ol></section>
<div class="decision" id="decisions" role="region" aria-labelledby="h-dec"><h2 id="h-dec">Decisions on this board</h2><ol>{decisions}</ol></div>
<section id="process" aria-labelledby="h-proc"><p class="secnum">HOW THIS WAS MADE</p><h2 id="h-proc">{E(R.get("process_title", "How this was made"))}</h2><ol>{L("process")}</ol></section>
<section id="checks" aria-labelledby="h-checks"><p class="secnum">CHECKS</p><h2 id="h-checks">What was tested</h2>
<div class="cols"><div><h4>Tested</h4><ul class="facts">{L("tested")}</ul></div><div><h4>Not tested</h4><ul class="facts">{L("not_tested")}</ul></div></div></section>
<section id="changes" aria-labelledby="h-ch"><p class="secnum">CHANGE LOG</p><h2 id="h-ch">Files</h2>
<p class="small">Paths are relative to <code>oath-and-action-v6-brand-guide/</code>.</p>
<div class="cols"><div><h4>Created</h4><ul class="facts">{L("changelog_created")}</ul></div><div><h4>Modified</h4><ul class="facts">{L("changelog_modified")}</ul></div></div></section>
</main></body></html>'''
    # a before may show the fault it teaches (an em dash among them); nothing else on the page may carry one
    rest = re.sub(r'<figure class="ex before">.*?</figure>', '', re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S), flags=re.S)
    assert '—' not in rest, 'em dash on the board outside a before'
    for sec in ('ask', 'process', 'tested', 'not_tested', 'changelog_created'):
        assert R.get(sec), f'the studio record has no {sec}'
    assert decs, 'no decisions'
    OUT.write_text(page)
    head, body = re.split(r'</head>\s*<body>', page, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n', '')
    head = head.replace('<title>Oath &amp; Action Writing Rules</title>\n', '')
    PUB.parent.mkdir(parents=True, exist_ok=True)
    PUB.write_text('<title>Oath &amp; Action Writing Rules</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head + re.sub(r'</body>\s*</html>\s*$', '', body))
    print('wrote', OUT.relative_to(ROOT), f'{len(page) / 1e3:.0f} kB; {n_rules} rules, {n_ill} illustrative')


if __name__ == '__main__':
    build()
