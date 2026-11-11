"""Chapter 19, Accessibility (accessibility lead), stage C round 1, November 11, 2026.

Usage:
    python3 -I work/build/scripts/phase-2/stage_c_ch19_build.py            write the chapter and its specimens
    python3 -I work/build/scripts/phase-2/stage_c_ch19_build.py --check    write nothing; exit 1 if any output differs

Writes:
    work/build/guide/chapters/19-accessibility.json         the chapter in the content contract (round 1 brief)
    work/build/guide/specimens/s-19-*.html                  its specimens
    work/build/guide/specimens/manifest-accessibility.json  their entries (D2-1267)

Reads:
    work/handoffs/phase-2/20261110_Stage-C-Research-Notes.md, section 1: the 55 WCAG 2.2 criteria at levels A and AA in
        W3C's words, from the Recommendation of December 12, 2024, as the research lead quoted them (D2-1137). Notes are
        W3C's informative text and stay out (D2-1138); 4.1.1 Parsing is listed as removed (D2-1139).
    work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch19-Results.json: the guide's own results, dated, Tested and Not
        tested apart, written by the accessibility lead from the runs it names. A missing file prints as pending.
    work/build/guide/chapters/*.json: every rule this chapter's map cites must exist in a chapter file that is present,
        and a chapter that is not written yet is named in words, never linked.

The map of criterion to rule starts from the round 0 inventory's section 4 and adds chapters 17, 18, 19 and 26.
"""
import argparse
import html
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parents[4]
GUIDE = ROOT / 'work/build/guide'
OUT_CH = GUIDE / 'chapters/19-accessibility.json'
OUT_SP = GUIDE / 'specimens'
MANIFEST = OUT_SP / 'manifest-accessibility.json'
RESEARCH = ROOT / 'work/handoffs/phase-2/20261110_Stage-C-Research-Notes.md'
RESULTS = ROOT / 'work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch19-Results.json'
CH = '19'
EM, EN = '—', '–'
WORDS = 'zero one two three four five six seven eight nine'.split()


def w(n, cap=False):
    """House rule H06: a number under ten in prose is a word."""
    t = WORDS[n] if n < 10 else f'{n:,}'
    return t[0].upper() + t[1:] if cap else t

e = html.escape

# ------------------------------------------------------------------------------------------------- WCAG's words
def criteria():
    s = RESEARCH.read_text()
    sec = s[s.index('### Principle 1, Perceivable'):s.index('## 2. WAI-ARIA')]
    out = []
    blocks = re.split(r'^(?=\*\*\d\.\d+\.\d+ )', sec, flags=re.M)
    for b in blocks:
        m = re.match(r'\*\*(\d\.\d+\.\d+) ([^*]+)\*\* \(Level (A|AA)\)(\. \*\*New in 2\.2\.\*\*)?', b)
        if not m:
            continue
        quote = [ln[1:].strip() for ln in b.splitlines() if ln.startswith('>')]
        url = re.search(r'Understanding page: (\S+)', b).group(1)
        out.append({'n': m.group(1), 'name': m.group(2).strip(), 'level': m.group(3), 'new': bool(m.group(4)),
                    'quote': quote, 'url': url})
    if len(out) != 55 or sum(c['level'] == 'A' for c in out) != 31:
        raise SystemExit(f'expected 55 criteria, 31 at level A; read {len(out)}')
    return out


def quote_html(lines):
    """W3C's words as written: a lead paragraph and any list of labeled items. Bold labels stay bold."""
    paras, items = [], []
    for ln in lines:
        t = e(ln, quote=False)
        t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
        if t.startswith('- '):
            items.append(t[2:].strip())
        else:
            paras.append(t)
    out = ''.join(f'<p>{p}</p>' for p in paras)
    if items:
        out += '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
    return out


# The map. Status: met (a guide rule states what the criterion asks), part (a rule covers part of it), gap (no rule
# yet; the chapter that owes it), none (no product does the thing today; the chapter that would add it). Rules are
# listed with the one that states the criterion most fully first.
MAP = {
    '1.1.1': ('met', ['19.2', '10.6', '11.11', '18.23'], 'Charts and atlas drawings add their table and reading guide in chapters 14 and 15.'),
    '1.2.1': ('gap', [], 'Chapters 16 and 23, with audio and video.'),
    '1.2.2': ('gap', [], 'Chapters 16 and 23, with video.'),
    '1.2.3': ('gap', [], 'Chapters 16 and 23, with video.'),
    '1.2.4': ('none', [], 'No product streams live today; chapter 23 if one does.'),
    '1.2.5': ('gap', [], 'Chapters 16 and 23, with video.'),
    '1.3.1': ('met', ['18.10', '18.3', '18.17', '18.6', '18.7', '11.5'], ''),
    '1.3.2': ('part', ['18.22', '18.6'], 'Components keep their order; chapter 20 owes the reading order of a whole page.'),
    '1.3.3': ('met', ['19.3'], ''),
    '1.3.4': ('met', ['19.6'], ''),
    '1.3.5': ('met', ['18.17'], ''),
    '1.4.1': ('met', ['05.4', '17.8', '17.10', '18.2', '18.5', '18.7', '19.3', '11.2', '11.15'], ''),
    '1.4.2': ('none', ['17.3'], 'No product plays sound; chapter 23 if a page ever does.'),
    '1.4.3': ('met', ['05.2', '26.7'], ''),
    '1.4.4': ('met', ['19.6', '07.5', '06.2'], ''),
    '1.4.5': ('met', ['19.4'], ''),
    '1.4.10': ('met', ['07.6', '19.6', '18.11'], ''),
    '1.4.11': ('met', ['05.5', '17.8', '17.9', '11.2'], ''),
    '1.4.12': ('met', ['19.6'], ''),
    '1.4.13': ('met', ['11.11', '18.23', '18.6'], ''),
    '2.1.1': ('met', ['18.1', '18.9', '18.23', '19.5'], 'Every rule of chapter 18 gives its keyboard path.'),
    '2.1.2': ('met', ['18.6', '18.23'], ''),
    '2.1.4': ('met', ['19.5'], ''),
    '2.2.1': ('met', ['18.22', '11.14', '18.20'], ''),
    '2.2.2': ('met', ['17.3', '17.4', '18.22'], ''),
    '2.3.1': ('part', ['17.1', '17.3'], 'Motion plays only on request; chapter 23 owes the flash test for video.'),
    '2.4.1': ('met', ['18.5', '18.6'], ''),
    '2.4.2': ('gap', [], 'Chapter 20, with each web page. This guide’s own page has a title.'),
    '2.4.3': ('met', ['18.6', '18.16', '18.17', '18.21', '18.22', '18.23'], ''),
    '2.4.4': ('met', ['18.5', '18.14', '11.13'], ''),
    '2.4.5': ('part', ['18.15', '18.7'], 'Search and location lists; chapter 20 owes the ways around a whole site.'),
    '2.4.6': ('part', ['18.17', '18.3', '11.11'], 'Labels; chapter 20 owes the headings of a page.'),
    '2.4.7': ('met', ['17.9', '05.4'], 'Every rule of chapter 18 draws the ring in its states.'),
    '2.4.11': ('met', ['18.6', '18.11'], ''),
    '2.5.1': ('met', ['19.5', '18.23'], ''),
    '2.5.2': ('met', ['19.5'], ''),
    '2.5.3': ('met', ['11.11', '18.1', '18.13'], ''),
    '2.5.4': ('met', ['19.5'], ''),
    '2.5.7': ('met', ['19.5'], ''),
    '2.5.8': ('met', ['11.7', '18.1'], 'Every rule of chapter 18 gives its target size.'),
    '3.1.1': ('gap', [], 'Chapter 20, with each web page. This guide’s own page sets its language.'),
    '3.1.2': ('gap', [], 'Chapters 02 and 20, for a passage in another language.'),
    '3.2.1': ('part', ['18.3', '18.9'], 'No component changes the page on focus; chapter 20 owes the rule for a whole page.'),
    '3.2.2': ('met', ['18.3', '18.4', '18.16'], ''),
    '3.2.3': ('met', ['18.6', '18.4'], ''),
    '3.2.4': ('met', ['11.12', '17.10', '18.22'], ''),
    '3.2.6': ('gap', [], 'Chapter 20, which places help in the same spot on every page.'),
    '3.3.1': ('met', ['18.17', '11.15'], ''),
    '3.3.2': ('met', ['18.17', '18.15'], ''),
    '3.3.3': ('met', ['18.17', '11.15'], ''),
    '3.3.4': ('none', [], 'No product takes money or legal statements today; chapter 22 if one sends testimony, gifts or petitions.'),
    '3.3.7': ('none', [], 'No form has more than one step today; chapter 22 when one does.'),
    '3.3.8': ('none', [], 'No product has accounts today; the chapter that adds them owes it.'),
    '4.1.2': ('met', ['18.1', '18.2', '18.9', '17.11'], 'Every rule of chapter 18 gives its accessible name and states.'),
    '4.1.3': ('met', ['18.18', '18.12', '18.15', '18.16', '18.20', '11.15'], ''),
}
STATUS_WORD = {'met': 'Met', 'part': 'Met in part', 'gap': 'Gap', 'none': 'Not used today'}


def present_rules():
    held = {}
    for f in (GUIDE / 'chapters').glob('[0-9][0-9]-*.json'):
        d = json.loads(f.read_text())
        held[str(d['number'])] = {str(r['id']) for r in d.get('rules', [])}
    return held


def rule_link(rid, held, own):
    ch = rid.split('.')[0]
    ok = rid in own if ch == CH else rid in held.get(ch, set())
    if ch != CH and ch in held and not ok:
        raise SystemExit(f'the map cites Rule {rid}, which chapter {ch} does not hold')
    if ok:
        return f'<a href="#rule-{rid.replace(".", "-")}">{rid}</a>'
    return rid


# ------------------------------------------------------------------------------------------------- specimens
SPECS = {}


def spec(sid, html_, rule, alt, width=None, interactive=False, readable=False, illustrative=False, notes='', exempt=None):
    if re.search(r'<h[1-6]\b|<(nav|article|header|footer|main|aside|section|form|search)\b', html_, re.I):
        raise SystemExit(f'{sid}: heading or landmark in a specimen')
    bare = re.sub(r'var\((?:[^()]|\([^()]*\))*\)', '', html_)
    bare = re.sub(r'\sd="[^"]*"', '', bare)
    if re.search(r'(?<![\w&])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![\w-])|\brgba?\(|\bhsla?\(', bare):
        raise SystemExit(f'{sid}: literal color')
    if EM in html_ or EN in html_:
        raise SystemExit(f'{sid}: em or en dash')
    meta = {'chapter': CH, 'rule': rule, 'width_px': width, 'alt': alt, 'illustrative': illustrative, 'notes': notes}
    if width:
        meta['fit_switch'] = False
    if interactive:
        meta['interactive'] = True
    if readable:
        meta['readable'] = True
    if exempt:
        meta['check_exempt'] = exempt
    SPECS[sid] = {'html': html_.strip() + '\n', 'meta': meta}
    return sid


BASE = (':scope{--ink:var(--oa-color-text-primary);--sec:var(--oa-color-text-secondary);--edge:var(--oa-color-border-strong);'
        '--hair:var(--oa-color-border-hairline);--ground:var(--oa-color-surface)}'
        ':where(.c19 p,.c19 ul,.c19 ol,.c19 blockquote){margin:0}'
        '.c19{color:var(--ink);font:var(--oa-type-body)}')
FAIL_CSS = ('.c19-fb{display:flex;align-items:center;gap:8px;padding:6px 12px;background:var(--oa-color-surface-charcoal);'
            'color:var(--oa-color-text-primary-on-charcoal);font:var(--oa-type-label);'
            'letter-spacing:var(--oa-type-label-letter-spacing);text-transform:var(--oa-type-label-text-transform)}'
            '.c19-ui{background:var(--ground);padding:16px 16px 20px}.c19-n{margin-top:12px;font:var(--oa-type-caption);color:var(--sec)}'
            '.c19-ill{margin-bottom:12px}.c19-ico{display:block;flex:none;fill:none;stroke:currentColor}'
            '.c19-box{border:1px solid var(--edge);padding:12px;background:var(--oa-color-field-ground)}'
            '.c19-k{font:var(--oa-type-caption);color:var(--sec);margin-bottom:6px}'
            '.c19-code{font:var(--oa-type-caption);font-family:ui-monospace,monospace;overflow-wrap:anywhere}'
            '.c19-btn{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;box-sizing:border-box;'
            'border:1px solid var(--edge);font:var(--oa-type-ui)}.c19-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}')
BAND = '<div class="c19-fb" aria-hidden="true"><span>×</span> Failure case: do not publish</div>'
ILL = '<p class="c19-ill"><span class="illus">Illustrative</span></p>'


def icon(name, px=24):
    return (f'<svg class="c19-ico" viewBox="0 0 {px} {px}" width="{px}" height="{px}" aria-hidden="true" focusable="false" '
            f'data-icon="U-{name}" data-icon-family="utility"><use href="#oa-sym-u-{name}-{px}px"/></svg>')


def picture(sid, rule, body, alt, notes, fail=False, illus=True, css='', exempt=None):
    h = (f'<style>{BASE}{FAIL_CSS}{css}</style><div class="c19">{BAND if fail else ""}<div class="c19-ui">'
         f'{ILL if illus else ""}{body}</div></div>')
    return spec(sid, h, rule, alt, width=360, illustrative=illus, notes=notes, exempt=exempt)


def s_criteria(crit, held, own):
    rows = []
    counts = {'met': 0, 'part': 0, 'gap': 0, 'none': 0}
    for c in crit:
        st, rules, note = MAP[c['n']]
        counts[st] += 1
        rl = ', '.join(rule_link(r, held, own) for r in rules)
        what = (f'<span class="c19-st c19-st--{st}">{STATUS_WORD[st]}</span>' + (f' Rules {rl}.' if rules else '')
                + (f' {e(note)}' if note else ''))
        new = ' <span class="c19-new">New in 2.2</span>' if c['new'] else ''
        rows.append(f'<li class="c19-c" data-st="{st}"><p class="c19-ch"><span class="c19-cn">{c["n"]}</span> '
                    f'<span class="c19-ct">{e(c["name"])}</span> <span class="c19-lv">Level {c["level"]}</span>{new}</p>'
                    f'<blockquote class="c19-q">{quote_html(c["quote"])}</blockquote><p class="c19-m">{what}</p></li>')
    total = len(crit)
    chips = ''.join(f'<label class="c19-f"><input type="radio" name="show" value="{v}"{" checked" if v == "all" else ""}>'
                    f'<span class="c19-fw">{w}</span></label>'
                    for v, w in (('all', 'All'), ('met', 'Met'), ('part', 'Met in part'), ('gap', 'Gaps'), ('none', 'Not used today')))
    css = ('.c19-s{display:grid;gap:8px;margin-bottom:12px}.c19-sl{font:var(--oa-type-ui)}'
           '.c19-sb{display:flex;align-items:stretch;border:1px solid var(--edge);background:var(--oa-color-field-ground);min-height:44px;box-sizing:border-box}'
           '.c19-si{flex:1;min-width:0;border:0;background:transparent;color:var(--ink);font:var(--oa-type-body);padding:0 12px}'
           '.c19-si:focus-visible{outline:2px solid var(--oa-color-focus-ring);outline-offset:2px}'
           '.c19-x{display:flex;align-items:center;justify-content:center;width:44px;min-height:44px;border:0;background:transparent;color:var(--ink);cursor:pointer}'
           '.c19-x[hidden]{display:none}.c19-x:focus-visible{outline:2px solid var(--oa-color-focus-ring);outline-offset:-4px}'
           '.c19-fs{border:0;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}.c19-fs legend{font:var(--oa-type-ui);padding:0;margin-bottom:6px;float:left;width:100%}'
           '.c19-f{position:relative;display:inline-flex}.c19-f input{position:absolute;inset:0;opacity:0;margin:0;cursor:pointer}'
           '.c19-fw{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1px solid var(--edge);font:var(--oa-type-ui);box-sizing:border-box}'
           '.c19-f input:checked+.c19-fw{border-width:2px;font-weight:var(--oa-font-weight-bold);padding:0 13px}'
           '.c19-f input:checked+.c19-fw::before{content:"\\2713";margin-right:6px}'
           '.c19-f input:focus-visible+.c19-fw{outline:2px solid var(--oa-color-focus-ring);outline-offset:2px}'
           '.c19-st-line{font:var(--oa-type-ui);margin:4px 0 8px}'
           '.c19-l{list-style:none;padding:0;margin:0;display:grid;gap:0}'
           '.c19-c{padding:14px 0;border-top:1px solid var(--hair)}.c19-c[hidden]{display:none}'
           '.c19-ch{font:var(--oa-type-ui);display:flex;flex-wrap:wrap;gap:4px 8px;align-items:baseline}'
           '.c19-cn{font-variant-numeric:tabular-nums}.c19-lv,.c19-new{font:var(--oa-type-caption);color:var(--sec)}'
           '.c19-new{border:1px solid var(--edge);padding:0 6px;color:var(--ink)}'
           '.c19-q{margin:8px 0 0;padding-left:12px;border-left:2px solid var(--hair);font:var(--oa-type-body-small)}'
           '.c19-q p+p,.c19-q ul{margin-top:6px}.c19-q ul{padding-left:18px}.c19-q li+li{margin-top:4px}'
           '.c19-m{margin-top:8px;font:var(--oa-type-body-small)}.c19-st{font-weight:var(--oa-font-weight-bold);margin-right:4px}'
           '.c19-st--gap::before{content:"\\25B3";margin-right:4px}.c19-st--met::before{content:"\\2713";margin-right:4px}'
           '.c19-m a{color:inherit;text-decoration:underline;text-underline-offset:.2em}'
           '.c19-rm{margin-top:12px;padding:12px 0;border-top:1px solid var(--hair);font:var(--oa-type-body-small)}'
           '@media (forced-colors:active){.c19-sb,.c19-fw{border-color:CanvasText}}')
    script = ('<script>(function(){var S=document.currentScript.closest("[data-specimen]");if(!S)return;'
              'var q=S.querySelector(".c19-si"),x=S.querySelector(".c19-x"),line=S.querySelector(".c19-st-line"),'
              'rows=Array.prototype.slice.call(S.querySelectorAll(".c19-c"));'
              'function show(){var t=q.value.trim().toLowerCase(),f=S.querySelector(".c19-f input:checked").value,n=0;'
              'rows.forEach(function(r){var on=(f==="all"||r.getAttribute("data-st")===f)&&(!t||r.textContent.toLowerCase().indexOf(t)>=0);'
              'r.hidden=!on;if(on)n++;});x.hidden=!q.value;'
              f'line.textContent=n+" of {total} criteria"+(n?".":". No criterion matches. Clear the search, or choose All, to see all {total}.");}}'
              'q.addEventListener("input",show);'
              'q.addEventListener("keydown",function(k){if(k.key==="Escape"&&q.value){k.preventDefault();q.value="";show();}});'
              'x.addEventListener("click",function(){q.value="";show();q.focus();});'
              'S.querySelectorAll(".c19-f input").forEach(function(i){i.addEventListener("change",show);});})();</script>')
    body = (f'<style>{BASE}{css}</style><div class="c19"><div class="c19-s"><label class="c19-sl" for="q">Search the criteria</label>'
            f'<div class="c19-sb"><input class="c19-si" id="q" type="search" autocomplete="off" spellcheck="false" aria-describedby="st">'
            f'<button type="button" class="c19-x" aria-label="Clear the search" hidden>{icon("close")}</button></div>'
            f'<fieldset class="c19-fs"><legend>Show</legend>{chips}</fieldset></div>'
            f'<p class="c19-st-line" id="st" role="status">{total} of {total} criteria.</p>'
            f'<ol class="c19-l">{"".join(rows)}</ol>'
            '<p class="c19-rm"><b>4.1.1 Parsing</b> was removed in WCAG 2.2, which keeps its number with no level. The problems '
            'it covered now fall under 1.3.1 and 4.1.2, so no rule here is tied to it.</p></div>' + script)
    sid = spec('s-19-criteria', body, '19.1',
               f'A searchable list of the {total} WCAG 2.2 success criteria at levels A and AA, in W3C’s words. Each entry '
               'gives the number, the name, the level, a tag for the six new in 2.2, the criterion’s words, and how this '
               f'guide meets it: {counts["met"]} are met by a rule, {counts["part"]} in part, {counts["gap"]} are gaps with '
               f'the chapter that owes each, and {counts["none"]} govern things no product does today. A search field and a '
               'choice of All, Met, Met in part, Gaps or Not used today narrow the list, and a status line says how many '
               'show. A last line says 4.1.1 Parsing was removed in WCAG 2.2.',
               interactive=True, notes='Live: search and a radio choice filter the list; the count goes to a polite status line (Rule 18.15).')
    return sid, counts


# ------------------------------------------------------------------------------------------------- results and the matrix
MATRIX = [
    # (check, what it shows, method, criteria)
    ('Every chapter rendered', 'Each chapter draws whole at the widths readers use', 'Screenshots at 1440, 1024, 390 and 360 px, looked at by a person', '1.4.10'),
    ('Report pages', 'Every page of a report reads in the reader', 'A screenshot of each page in the report reader', '1.4.10, 4.1.2'),
    ('Keyboard and focus', 'Every control is reached in order, shows its ring and holds no trap', 'A script presses Tab through the page and walks each component’s keyboard path; a person checks the order and the ring', '2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11'),
    ('Reading order and headings', 'The outline makes sense read aloud', 'The accessibility tree’s outline, read by script and by a person', '1.3.1, 1.3.2, 2.4.6'),
    ('Automated rules', 'The faults a machine can find are gone', 'axe-core with the WCAG 2.2 A and AA tags on every chapter', 'Many, in part'),
    ('Contrast', 'Text, marks, edges and focus rings stand out from their ground', 'A script reads each rendered color pair, states included', '1.4.3, 1.4.11'),
    ('Text at 200 percent and 320 px', 'Nothing is cut off or lost when text grows or the screen narrows', 'Screenshots, and a script that finds sideways scroll and clipped words', '1.4.4, 1.4.10, 1.4.12'),
    ('Reduced motion', 'Nothing moves on its own, and every motion has a still end', 'The browser set to reduce motion, then each moving part played', '2.2.2, 2.3.1'),
    ('Forced colors', 'Every mark, edge and state survives a contrast theme', 'The browser set to forced colors, light and dark, then each part read by script and by eye', '1.4.1, 1.4.11'),
    ('Dark surfaces and long labels', 'Components read on Charcoal and Prussian, with the longest real words', 'Specimens on each surface, and labels from the atlas’s longest variable and reform titles', '1.4.3, 1.4.10'),
    ('Print', 'A printed page keeps its words and order', 'Print emulation and the print stylesheet', '1.3.2'),
    ('Downloads', 'Each file arrives whole and named', 'Press each download, open each file, check SVG validity and PNG size', '2.4.4'),
    ('Diagram and chart equivalents', 'A reader who cannot see a drawing gets its connections', 'Each drawing checked for its words or table and its reading guide', '1.1.1, 1.3.1'),
    ('Grayscale', 'Nothing rests on color alone', 'Grayscale screenshots of every data and systems specimen', '1.4.1'),
]


def load_results():
    if not RESULTS.exists():
        return None
    return json.loads(RESULTS.read_text())


def s_matrix():
    rows = ''.join(f'<li class="c19-r"><p class="c19-rt">{e(c)}</p><dl class="c19-dl"><div><dt>What it shows</dt><dd>{e(w)}</dd></div>'
                   f'<div><dt>Method</dt><dd>{e(m)}</dd></div><div><dt>Criteria</dt><dd>{e(k)}</dd></div></dl></li>'
                   for c, w, m, k in MATRIX)
    css = ('.c19-ml{list-style:none;padding:0;margin:0}.c19-r{padding:12px 0;border-top:1px solid var(--hair)}'
           '.c19-rt{font:var(--oa-type-ui)}.c19-dl{margin:6px 0 0;display:grid;gap:4px;font:var(--oa-type-body-small)}'
           '.c19-dl div{display:grid;grid-template-columns:minmax(6rem,9rem) 1fr;gap:8px}.c19-dl dt{color:var(--sec)}.c19-dl dd{margin:0}'
           '@media (max-width:30em){.c19-dl div{grid-template-columns:1fr;gap:0}}')
    return spec('s-19-matrix', f'<style>{BASE}{css}</style><div class="c19"><ol class="c19-ml">{rows}</ol></div>', '19.7',
                f'The verification matrix: {len(MATRIX)} checks, each with what it shows, its method and the WCAG 2.2 '
                'criteria it serves. ' + ' '.join(f'{c}: {m}.' for c, _, m, _ in MATRIX), readable=True,
                notes='Readable: the checks and methods of the verification matrix, with what each shows.')


def s_results(res):
    css = ('.c19-h{font:var(--oa-type-ui);margin:0 0 6px}.c19-h+.c19-rl{margin-bottom:16px}'
           '.c19-rl{padding-left:20px;font:var(--oa-type-body-small)}.c19-rl li+li{margin-top:6px}'
           '.c19-meta{font:var(--oa-type-caption);color:var(--sec);margin-bottom:12px}')
    if not res:
        body = '<p class="c19-meta">The results file is not written yet.</p>'
        alt = 'The guide’s own results: pending.'
    else:
        t = ''.join(f'<li><b>{e(x["check"])}.</b> {e(x["result"])}</li>' for x in res['tested'])
        n = ''.join(f'<li><b>{e(x["check"])}.</b> {e(x["why"])}</li>' for x in res['not_tested'])
        body = (f'<p class="c19-meta">{e(res["build"])}</p><p class="c19-h">Tested on {e(res["date"])}</p><ul class="c19-rl">{t}</ul>'
                f'<p class="c19-h">Not tested</p><ul class="c19-rl">{n}</ul>')
        alt = (f'The guide’s own results, {res["date"]}. {res["build"]} Tested: '
               + ' '.join(f'{x["check"]}: {x["result"]}' for x in res['tested']) + ' Not tested: '
               + ' '.join(f'{x["check"]}: {x["why"]}' for x in res['not_tested']))
    return spec('s-19-results', f'<style>{BASE}{css}</style><div class="c19">{body}</div>', '19.8', alt, readable=True,
                notes='Readable: printed from 20261111_Stage-C-Round-1-Ch19-Results.json, which names the runs behind each line.')


# ------------------------------------------------------------------------------------------------- the device script
LOOK = [
    'The page’s title is read as the page opens.',
    'The first stop is “Skip to main content”.',
    'Headings come in order: the chapter, then each rule.',
    'Each control says its words and what kind of control it is, and a pressed, checked or current one says so.',
    'A button that waits says it is unavailable and why.',
    'The phone menu takes you inside when it opens, and Close the menu, or Escape on a keyboard, brings you back to Menu.',
    'Typing in a search field, you hear how many results there are, and the cursor stays in the field.',
    'Pressing Copy, you hear what was copied.',
    'Sending a form with a mistake takes you to the field to fix, and you hear the error.',
    'Nothing you cannot see is read, and nothing you cannot see takes focus.',
]
DEVICES = [
    ('iPhone with VoiceOver', [
        'Open Settings, then Accessibility, then Accessibility Shortcut, and choose VoiceOver. From now on, pressing the side '
        'button three times turns VoiceOver on and off.',
        'Open the page in Safari, then press the side button three times. VoiceOver says “VoiceOver on”.',
        'Swipe right with one finger to move to the next item, and left to go back. Each item is read aloud.',
        'Double-tap anywhere to press the item VoiceOver is on. To type, double-tap a field, type, then swipe on.',
        'Go through the ten things to listen for below, and write Pass or Fail beside each with what you heard.',
        'Press the side button three times to turn VoiceOver off.']),
    ('Android phone with TalkBack', [
        'Open Settings, then Accessibility, then TalkBack, and turn on the TalkBack shortcut. Makers name these menus '
        'differently; the shortcut is usually holding both volume keys for three seconds.',
        'Open the page in Chrome, then hold both volume keys for three seconds. TalkBack says it is on.',
        'Swipe right with one finger to move to the next item, and left to go back. Scroll with two fingers.',
        'Double-tap anywhere to press the item TalkBack is on. To type, double-tap a field, type, then swipe on.',
        'Go through the ten things to listen for below, and write Pass or Fail beside each with what you heard. Gestures '
        'differ between TalkBack versions; Google’s TalkBack help lists the ones on your phone.',
        'Hold both volume keys for three seconds to turn TalkBack off.']),
    ('Windows PC with NVDA and a contrast theme', [
        'Download NVDA, a free screen reader, from nvaccess.org and install it. Start it from the Start menu; it says '
        '“NVDA started”.',
        'Open the page in Chrome, Edge or Firefox. Press Tab to move from control to control, and Shift and Tab to go back. '
        'Press Enter or Space to press a control. Press Control to stop the speech.',
        'Press H to jump from heading to heading, and D from landmark to landmark.',
        'Go through the ten things to listen for below, and write Pass or Fail beside each with what you heard. Press '
        'Insert and Q to quit NVDA.',
        'Now turn on a contrast theme: on Windows 11, open Settings, then Accessibility, then Contrast themes, choose Night '
        'sky and press Apply. On Windows 10, open Settings, then Ease of Access, then High contrast.',
        'Reload the page and look: every button keeps an edge, the focus ring shows on each Tab stop, a pressed chip keeps '
        'its check, an error keeps its bar, and the warning and success marks stay visible. Write down any that vanish, '
        'then set the theme back to None.']),
    ('Mac with VoiceOver', [
        'In Safari, open Settings, then Advanced, and turn on “Press Tab to highlight each item on a webpage”.',
        'Press Command and F5 to turn VoiceOver on. It says “VoiceOver on Safari”.',
        'Press Tab to move from control to control, and Shift and Tab to go back. Press Control, Option and the Right Arrow '
        'to read the next item, and Control, Option and Space to press it.',
        'Press Control, Option and U to open the rotor, a list of the page’s headings, links and landmarks. The Left and '
        'Right Arrows switch lists, the Up and Down Arrows choose, and Return goes there.',
        'Go through the ten things to listen for below, and write Pass or Fail beside each with what you heard.',
        'Press Command and F5 to turn VoiceOver off.']),
]


def s_devices():
    blocks = ''.join(f'<li class="c19-d"><p class="c19-dt">{e(name)}</p><ol class="c19-ds">'
                     + ''.join(f'<li>{e(s)}</li>' for s in steps) + '</ol></li>' for name, steps in DEVICES)
    css = ('.c19-dl0{list-style:none;padding:0;margin:0}.c19-d{padding:12px 0;border-top:1px solid var(--hair)}'
           '.c19-dt{font:var(--oa-type-ui)}.c19-ds{margin-top:6px;padding-left:22px;font:var(--oa-type-body-small)}'
           '.c19-ds li+li{margin-top:6px}.c19-lk{margin-top:16px;padding-top:12px;border-top:2px solid var(--edge)}'
           '.c19-lk p{font:var(--oa-type-ui)}.c19-lk ol{margin-top:6px;padding-left:22px;font:var(--oa-type-body-small)}'
           '.c19-lk li+li{margin-top:4px}.c19-rec{margin-top:12px;font:var(--oa-type-body-small)}')
    look = ''.join(f'<li>{e(x)}</li>' for x in LOOK)
    body = (f'<style>{BASE}{css}</style><div class="c19"><ol class="c19-dl0">{blocks}</ol>'
            f'<div class="c19-lk"><p>Ten things to listen for: a pass sounds like this</p><ol>{look}</ol>'
            '<p class="c19-rec">Write down the device, its system version, the browser and its version, the screen reader’s '
            'version, the date, and each step’s result with what you heard. A fail with its words is as useful as a pass.</p></div></div>')
    alt = ('The device script, in four parts. ' + ' '.join(f'{n}: ' + ' '.join(f'{i + 1}. {s}' for i, s in enumerate(st))
                                                         for n, st in DEVICES)
           + ' Ten things to listen for: ' + ' '.join(f'{i + 1}. {x}' for i, x in enumerate(LOOK)))
    return spec('s-19-devices', body, '19.9', alt, readable=True,
                notes='Readable: the device script of DR-213, four devices, each step numbered, with what a pass sounds like.')


# ------------------------------------------------------------------------------------------------- small pictures
def pictures():
    picture('s-19-1-failure', '19.1',
            '<div class="c19-box c19-row"><svg class="c19-ico" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" '
            'focusable="false"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/>'
            '<path d="M7.5 12.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
            '<p><b>Fully accessible.</b> This site works for everyone.</p></div>'
            '<p class="c19-n">No standard, no level, no date and no list of what was checked.</p>',
            'Failure case: do not publish. An Illustrative badge at 360 px with a check mark and the words “Fully accessible. '
            'This site works for everyone.” A note reads “No standard, no level, no date and no list of what was checked.”',
            'Picture of a fault: a claim with no standard behind it.', fail=True)
    picture('s-19-2-correct', '19.2',
            '<p class="c19-k">A drawing beside its word: the word carries it</p><div class="c19-box c19-row">'
            '<svg viewBox="0 0 128 128" width="48" height="48" aria-hidden="true" focusable="false" data-icon="CL-001" '
            'data-icon-family="topic" style="color:var(--oa-color-text-primary)"><use href="#oa-sym-cl-001"/></svg><span>Voting</span></div>'
            '<p class="c19-code" style="margin-top:6px"><code>alt=""</code></p>'
            '<p class="c19-k" style="margin-top:14px">A chart alone: its alt gives its finding</p>'
            '<div class="c19-box"><svg viewBox="0 0 300 80" width="100%" height="80" aria-hidden="true" focusable="false">'
            '<g fill="var(--oa-color-text-primary)"><rect x="20" y="50" width="40" height="30"/><rect x="90" y="38" width="40" height="42"/>'
            '<rect x="160" y="26" width="40" height="54"/><rect x="230" y="12" width="40" height="68"/></g></svg></div>'
            '<p class="c19-code" style="margin-top:6px"><code>alt="Comments on the county budget rose each year from 2023 to 2026."</code></p>',
            'An Illustrative pair at 360 px. First, the Voting symbol beside its word, “Voting”, marked with '
            'empty alt text because the word says it. Second, a bar chart of four bars rising left to right, with the alt '
            'text “Comments on the county budget rose each year from 2023 to 2026.”',
            'Correct: alt text for purpose, and empty alt where a word already says it.')
    picture('s-19-2-failure', '19.2',
            '<div class="c19-box"><svg viewBox="0 0 300 80" width="100%" height="80" aria-hidden="true" focusable="false">'
            '<g fill="var(--oa-color-text-primary)"><rect x="20" y="50" width="40" height="30"/><rect x="90" y="38" width="40" height="42"/>'
            '<rect x="160" y="26" width="40" height="54"/><rect x="230" y="12" width="40" height="68"/></g></svg></div>'
            '<p class="c19-code" style="margin-top:6px"><code>alt="chart_final_v2.png"</code></p>'
            '<p class="c19-n">A screen reader hears a file name, and nothing of what the chart shows.</p>',
            'Failure case: do not publish. An Illustrative bar chart at 360 px with the alt text “chart_final_v2.png”, a file '
            'name. A note says a screen reader hears nothing of what the chart shows.',
            'Picture of a fault: alt text that names a file.', fail=True)
    form = ('<div class="c19-box"><p class="c19-k" style="color:var(--ink)">Your comment</p>'
            '<div style="height:44px;border:1px solid var(--oa-color-border-strong);background:var(--oa-color-surface)"></div>'
            '<div class="c19-row" style="margin-top:8px;justify-content:flex-end"><span class="c19-btn">Start over</span>'
            '<span class="c19-btn" style="background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label);'
            'border-color:var(--oa-color-action-primary-fill)">Send your comment</span></div></div>')
    picture('s-19-3-correct', '19.3', form + '<p style="margin-top:10px">When your comment is ready, press <b>Send your comment</b>.</p>',
            'An Illustrative comment form at 360 px with a field and two buttons, Start over and Send your comment. The '
            'instruction under it names the button by its words: “When your comment is ready, press Send your comment.”',
            'Correct: an instruction that names the control by its words.')
    picture('s-19-3-failure', '19.3', form + '<p style="margin-top:10px">When your comment is ready, press the dark button on the right.</p>'
            '<p class="c19-n">Color and place are all it gives, and a phone puts the buttons in another place.</p>',
            'Failure case: do not publish. The same Illustrative form at 360 px, with the instruction “When your comment is '
            'ready, press the dark button on the right.”, which names no words.',
            'Picture of a fault: an instruction by color and place alone (SC 1.3.3).', fail=True)
    card = ('<div style="background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);padding:16px">'
            '<p style="font:var(--oa-type-h4);font-size:1.25rem">The zoning code &amp; the rent.</p></div>')
    picture('s-19-4-correct', '19.4', card + '<p class="c19-n">Live text: it grows with the reader’s setting, reflows on a phone and '
            'can be found, read aloud and translated.</p>',
            'An Illustrative hinge headline at 360 px, “The zoning code & the rent.”, set as live text in White on a Prussian '
            'band, with a note that it grows, reflows and can be read aloud and translated.',
            'Correct: words as live text.')
    picture('s-19-4-failure', '19.4',
            '<div style="background:var(--oa-color-surface-prussian);padding:16px"><svg viewBox="0 0 300 24" width="300" height="24" '
            'aria-hidden="true" focusable="false"><g fill="var(--oa-color-text-primary-on-prussian)">'
            + ''.join(f'<rect x="{x}" y="{y}" width="6" height="6"/>' for x, y in
                      [(0, 6), (6, 0), (6, 12), (12, 6), (24, 0), (24, 12), (30, 6), (42, 0), (42, 6), (42, 12), (54, 6), (60, 0),
                       (60, 12), (78, 0), (78, 6), (84, 12), (96, 6), (102, 0), (108, 12), (120, 0), (126, 6), (132, 12)])
            + '</g></svg></div><p class="c19-n">The headline is a picture: it blurs when zoomed, cannot be found or translated, '
            'and a screen reader hears only its alt text, if any.</p>',
            'Failure case: do not publish. An Illustrative headline at 360 px drawn as a picture, shown blurred into blocks as '
            'it looks when zoomed in. A note says it cannot be found, translated or read aloud from its words.',
            'Picture of a fault: a picture of text in place of text (SC 1.4.5).', fail=True)
    mapbox = ('<div class="c19-box" style="height:120px;position:relative"><svg viewBox="0 0 300 100" width="100%" height="100" '
              'aria-hidden="true" focusable="false"><g fill="none" stroke="var(--oa-color-text-primary)" stroke-width="1.5">'
              '<path d="M10 70 L60 40 L120 55 L170 20 L240 35 L290 15"/><path d="M10 90 L80 80 L150 88 L220 70 L290 78"/></g></svg></div>')
    picture('s-19-5-correct', '19.5', mapbox + '<div class="c19-row" style="margin-top:8px"><span class="c19-btn">Zoom in</span>'
            '<span class="c19-btn">Zoom out</span><span class="c19-btn">Fit</span></div>',
            'An Illustrative map of district lines at 360 px with three buttons under it, Zoom in, Zoom out and Fit, each a '
            'single press.', 'Correct: every action is one press of a button.')
    picture('s-19-5-failure', '19.5', mapbox + '<p class="c19-k" style="margin-top:8px">Pinch to zoom. Drag to pan. Shake to undo. Press Z to zoom.</p>'
            '<p class="c19-n">Each action needs two fingers, a drag, a shake or one letter key, and has no button.</p>',
            'Failure case: do not publish. The same Illustrative map at 360 px with the line “Pinch to zoom. Drag to pan. '
            'Shake to undo. Press Z to zoom.” and no buttons.',
            'Picture of a fault: gestures, motion and a single-key shortcut with no button (SC 2.1.4, 2.5.1, 2.5.4, 2.5.7).',
            fail=True)
    big = 'font:var(--oa-type-ui);font-size:1.875rem;line-height:1.3'
    picture('s-19-6-correct', '19.6',
            f'<p class="c19-k">Text at 200 percent, 360 px wide</p><div style="display:grid;gap:8px">'
            f'<span class="c19-btn" style="{big};padding:8px 16px;justify-content:center">Previous page</span>'
            f'<span class="c19-btn" style="{big};padding:8px 16px;justify-content:center">Next page</span></div>',
            'An Illustrative pair of buttons at 360 px with text at 200 percent: Previous page and Next page have stacked into '
            'one column, each word whole.', 'Correct: a row of two buttons that stacks as text grows.')
    picture('s-19-6-failure', '19.6',
            f'<p class="c19-k">Text at 200 percent, 360 px wide</p><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">'
            f'<span class="c19-btn" style="{big};padding:8px 10px;overflow:hidden;white-space:nowrap">Previous page</span>'
            f'<span class="c19-btn" style="{big};padding:8px 10px;overflow:hidden;white-space:nowrap">Next page</span></div>'
            '<p class="c19-n">The words may not wrap, so they run out of their buttons and are cut off.</p>',
            'Failure case: do not publish. The same Illustrative buttons at 360 px with text at 200 percent, held side by side; '
            'their words may not wrap, so “Previous page” and “Next page” are cut off at the buttons’ edges.',
            'Picture of a fault: labels that may not wrap (SC 1.4.4, 1.4.12).', fail=True)
    picture('s-19-7-failure', '19.7',
            '<div class="c19-box"><p class="c19-code">Automated scan: 0 errors</p><p style="margin-top:6px"><b>The page passes.</b></p></div>'
            '<p class="c19-n">One tool’s score stands in for the whole matrix, so keyboard, reading order, zoom and forced '
            'colors went unchecked.</p>',
            'Failure case: do not publish. An Illustrative report line at 360 px: “Automated scan: 0 errors. The page passes.” '
            'A note says one tool stood in for the whole matrix.',
            'Picture of a fault: one automated score taken as a pass.', fail=True)
    picture('s-19-8-failure', '19.8',
            '<div class="c19-box"><p><b>Passes WCAG 2.2 AA</b> on every browser and screen reader.</p></div>'
            '<p class="c19-n">No date, and no line between what someone ran and what nobody did.</p>',
            'Failure case: do not publish. An Illustrative results line at 360 px: “Passes WCAG 2.2 AA on every browser and '
            'screen reader.” It has no date and mixes what was run with what was not.',
            'Picture of a fault: a result with no date and no Not tested list.', fail=True)
    picture('s-19-9-failure', '19.9',
            '<div class="c19-box"><p>Checked with a screen reader. Looks fine.</p></div>'
            '<p class="c19-n">No device, no screen reader named, no steps, no date and nothing heard.</p>',
            'Failure case: do not publish. An Illustrative line at 360 px: “Checked with a screen reader. Looks fine.” A note '
            'says it names no device, screen reader, steps or date.',
            'Picture of a fault: a device check no one could repeat.', fail=True)


# ------------------------------------------------------------------------------------------------- the chapter
def build():
    crit = criteria()
    held = present_rules()
    own = {f'19.{i}' for i in range(1, 10)}
    for st, rules, _ in MAP.values():
        if st not in STATUS_WORD:
            raise SystemExit(f'unknown status {st}')
    if set(MAP) != {c['n'] for c in crit}:
        raise SystemExit(f'the map and the criteria differ: {sorted(set(MAP) ^ {c["n"] for c in crit})}')
    cid, counts = s_criteria(crit, held, own)
    s_matrix()
    res = load_results()
    s_results(res)
    s_devices()
    pictures()
    n = len(crit)
    newn = sum(c['new'] for c in crit)
    rules = [
        dict(id='19.1', title='Build every page and product to WCAG 2.2 at level AA, and find each criterion here.',
             rule=[f'WCAG 2.2 sets {n} success criteria at levels A and AA: '
                   f'{sum(c["level"] == "A" for c in crit)} at A and {sum(c["level"] == "AA" for c in crit)} at AA, {w(newn)} of them '
                   'new in 2.2. Every page and product we publish meets all of them. The list below gives each criterion in '
                   'W3C’s own words and the rule in this guide that meets it.',
                   f'Today a rule meets {w(counts["met"])} criteria and {w(counts["part"])} more in part. {w(counts["gap"], True)} are '
                   f'gaps, each named with the chapter that owes it, and {w(counts["none"])} govern things no product does yet, such as '
                   'live video or accounts. A gap is open work, and a page that meets the criterion on its own still meets '
                   'it.'],
             tokens=[], why={'text': ['One standard, read in its own words, lets a builder check a page without guessing what '
                                      '“accessible” means, and ties each criterion to a rule they can follow. W3C’s notes '
                                      'and examples sit on its Understanding pages, which the sources link.'],
                             'basis': 'WCAG 2.2, W3C Recommendation, December 12, 2024, section 5 on conformance'},
             correct={'specimen': cid, 'caption': f'All {n} criteria in W3C’s words, live. Search by number, name or word, '
                                                   'or show only the gaps; the line above the list says how many show.'},
             failure={'specimen': 's-19-1-failure', 'caption': '<strong>Fails Rule 19.1.</strong> A badge says “Fully accessible” '
                                                               'and names no standard, level, date or check.'},
             specs=[{'label': 'Standard', 'value': 'WCAG 2.2, levels A and AA; level AAA where a rule asks for it'},
                    {'label': 'Criteria', 'value': f'{n}: {sum(c["level"] == "A" for c in crit)} at A, '
                                                   f'{sum(c["level"] == "AA" for c in crit)} at AA, {newn} new in 2.2'},
                    {'label': 'Removed', 'value': '4.1.1 Parsing, which WCAG 2.2 keeps as a number with no level'},
                    {'label': 'Met today', 'value': f'{counts["met"]} by a rule, {counts["part"]} in part'},
                    {'label': 'Gaps', 'value': f'{counts["gap"]}, owed by chapters 02, 16, 20 and 23'},
                    {'label': 'Not used today', 'value': f'{counts["none"]}: live captions, sound that plays itself, legal or '
                                                         'money forms, multi-step forms and sign-in'}],
             related=['18', '20'], builders=['Use W3C’s quick reference, w3.org/WAI/WCAG22/quickref, to filter the criteria '
                                             'by level and topic, and open a criterion’s Understanding page for its examples.']),
        dict(id='19.2', title='Write alt text for what an image does on the page, and hide decoration from screen readers.',
             rule=['Alt text says what a reader would miss without the image, in a sentence, such as a chart’s finding or '
                   'what a photograph shows happening. A symbol beside its own word, a divider or a pattern takes empty alt '
                   'text, <code>alt=""</code>, so a screen reader passes it. A chart or an atlas drawing also gets its table or its lines '
                   'in words (Rule 18.23).'],
             tokens=[], why={'text': ['Alt text that names a purpose gives a screen reader user what the image gives everyone '
                                      'else. A file name or “image of” adds noise, and decoration read aloud slows the page.'],
                             'basis': 'WCAG 2.2 SC 1.1.1'},
             correct={'specimen': 's-19-2-correct', 'caption': 'A symbol beside its word takes empty alt text; a chart standing '
                                                               'alone takes its finding.'},
             failure={'specimen': 's-19-2-failure', 'caption': '<strong>Fails Rule 19.2.</strong> The chart’s alt text is its '
                                                               'file name, so a screen reader hears nothing it shows.'},
             specs=[{'label': 'Informative image', 'value': 'One or two sentences: what it shows that the text around it does not'},
                    {'label': 'Image beside its word', 'value': '<code>alt=""</code> and, for inline SVG, <code>aria-hidden="true"</code>'},
                    {'label': 'Chart or drawing', 'value': 'Its finding as alt text, and its table or lines in words beside it'},
                    {'label': 'Never', 'value': 'A file name, “image of” or “picture of”, or words that repeat the caption'}],
             related=['10', '14', '16']),
        dict(id='19.3', title='Name a control or a step by its words, never only by its color, shape or place.',
             rule=['An instruction names the control it means by the words on it: “press Send your comment”. Color, shape '
                   'and place can add to the words, as in “Send your comment, under the form”, and never stand in for them, '
                   'since a phone moves things and a screen reader or a contrast theme drops color.'],
             tokens=[], why={'text': ['A reader who cannot see color, or who meets the buttons in another order on a phone, '
                                      'can still follow words that match the control’s name.'],
                             'basis': 'WCAG 2.2 SC 1.3.3 and 1.4.1'},
             correct={'specimen': 's-19-3-correct', 'caption': 'The instruction names Send your comment by its words.'},
             failure={'specimen': 's-19-3-failure', 'caption': '<strong>Fails Rule 19.3.</strong> “The dark button on the '
                                                               'right” gives only color and place.'},
             specs=[{'label': 'Say', 'value': 'The control’s own words, as its name starts (Rule 18.1)'},
                    {'label': 'May add', 'value': 'Where it is, after its words'},
                    {'label': 'Never alone', 'value': 'Color, shape, size, sound or place'}],
             related=['02', '18']),
        dict(id='19.4', title='Set words as live text, and keep pictures of text for the logo.',
             rule=['Headlines, quotes, labels and chart words are live text in the page. A social card or a slide that '
                   'must be an image carries its words again in the post or the page beside it. The wordmark is the one '
                   'picture of text a page holds.'],
             tokens=[], why={'text': ['Live text grows with a reader’s setting, reflows on a phone and can be found, copied, '
                                      'translated and read aloud. A picture of text blurs when zoomed and says only its alt '
                                      'text.'],
                             'basis': 'WCAG 2.2 SC 1.4.5; logotypes are essential under its note'},
             correct={'specimen': 's-19-4-correct', 'caption': 'The hinge headline set as live text on a Prussian band.'},
             failure={'specimen': 's-19-4-failure', 'caption': '<strong>Fails Rule 19.4.</strong> The headline is a picture, '
                                                               'which blurs when zoomed and cannot be read from its words.'},
             specs=[{'label': 'Live text', 'value': 'Every word on a web page, in an email where it can be, and on a slide'},
                    {'label': 'An image that must hold words', 'value': 'The same words in the text beside it, and as alt text'},
                    {'label': 'Allowed as an image', 'value': 'The wordmark and the lockups (chapter 03)'}],
             related=['03', '22', '23']),
        dict(id='19.5', title='Let every action work with one tap, one click or one key press.',
             rule=['Every action has a control a reader can press once: Zoom in and Zoom out as buttons, a drawing moved '
                   'with buttons or arrow keys, and Undo as a button. A gesture with two fingers, a drag, a tilt or a shake '
                   'may add a way, never the only one. No product uses a shortcut of one letter key, and an action runs when '
                   'the press ends, so sliding off a control cancels it.'],
             tokens=['oa.size.target.touch'],
             why={'text': ['A reader with a tremor, one hand, a head pointer or voice control can press a button where a '
                           'pinch or a drag fails, and a single-letter shortcut fires by accident for a reader who talks to '
                           'the computer.'],
                  'basis': 'WCAG 2.2 SC 2.1.4, 2.5.1, 2.5.2, 2.5.4 and 2.5.7'},
             correct={'specimen': 's-19-5-correct', 'caption': 'Zoom in, Zoom out and Fit as buttons under the map.'},
             failure={'specimen': 's-19-5-failure', 'caption': '<strong>Fails Rule 19.5.</strong> Pinch, drag, shake and the '
                                                               'Z key are the only ways to act.'},
             specs=[{'label': 'Each action', 'value': 'A control pressed once, at least 44 px (Rule 11.7)', 'token': 'oa.size.target.touch'},
                    {'label': 'Gestures and motion', 'value': 'Only beside a button that does the same'},
                    {'label': 'Shortcuts', 'value': 'None of one letter; a shortcut takes a modifier key, such as Control'},
                    {'label': 'When it runs', 'value': 'On release, as native buttons do'}],
             related=['18', '15']),
        dict(id='19.6', title='Let text grow to 200 percent, spacing open and the screen turn, with nothing lost.',
             rule=['A page keeps every word and control when the reader doubles the text size, widens the spacing between '
                   'lines, words and letters, or turns the phone on its side. Labels wrap where they would overflow, a row '
                   'of two buttons stacks, and no page locks itself to one orientation. Reflow at 320 px is Rule 07.6.'],
             tokens=[], why={'text': ['Many readers raise the text size or the spacing to read at all, and some hold a phone '
                                      'one way only. Words that may not wrap are the most common way a page loses them.'],
                             'basis': 'WCAG 2.2 SC 1.3.4, 1.4.4, 1.4.10 and 1.4.12'},
             correct={'specimen': 's-19-6-correct', 'caption': 'At 200 percent text the two buttons stack, and each word '
                                                               'stays whole.'},
             failure={'specimen': 's-19-6-failure', 'caption': '<strong>Fails Rule 19.6.</strong> The words may not wrap, so '
                                                               'both are cut off.'},
             specs=[{'label': 'Text size', 'value': '200 percent with nothing cut off or overlapping'},
                    {'label': 'Spacing', 'value': 'Line height 1.5, paragraph spacing 2 times the size, letter spacing 0.12 '
                                                  'and word spacing 0.16 times the size, all at once, with nothing lost'},
                    {'label': 'Width', 'value': '320 px with no sideways scroll outside a scroll region (Rule 07.6)'},
                    {'label': 'Orientation', 'value': 'Both, with no lock'},
                    {'label': 'Never', 'value': '<code>white-space: nowrap</code> on a label, or a fixed height on a box of words'}],
             related=['07', '06', '18']),
        dict(id='19.7', title='Check every page with the verification matrix, each check by its own method.',
             rule=[f'The matrix holds {len(MATRIX)} checks. Each shows one thing, such as a keyboard path or a color pair, '
                   'and each has its own method, because no single tool sees them all. A page is ready when every check '
                   'that applies to it has run and passed, and its results are written down as Rule 19.8 sets.'],
             tokens=[], why={'text': ['An automated scan finds some faults a machine can measure. Keyboard order, reading '
                                      'order, zoom, forced colors and what a screen reader says need their own checks, and '
                                      'most of them need a person.'],
                             'basis': 'Design judgment; WCAG 2.2, section 5 on conformance'},
             correct={'specimen': 's-19-matrix', 'caption': 'Each check, what it shows, its method and the criteria it serves.'},
             failure={'specimen': 's-19-7-failure', 'caption': '<strong>Fails Rule 19.7.</strong> One scan’s zero stands in '
                                                               'for the whole matrix.'},
             specs=[{'label': 'Widths', 'value': '1440, 1024, 390 and 360 px'},
                    {'label': 'Automated rules', 'value': 'axe-core with the WCAG 2.2 A and AA tags'},
                    {'label': 'Keyboard paths', 'value': 'Each component’s path, walked in the light and dark themes (chapter 18)'},
                    {'label': 'Emulated settings', 'value': 'Reduced motion, forced colors light and dark, the device set to dark'},
                    {'label': 'By a person', 'value': 'The keyboard order and ring, the reading order, and the device script (Rule 19.9)'}],
             related=['18', '26']),
        dict(id='19.8', title='Report each result with its date, and keep what was tested apart from what was not.',
             rule=['A results report gives the date, the build it ran on and, for each check, what ran and what it found. '
                   'What could not run, and why, goes in a separate list, so no one reads a check nobody made as a pass. '
                   'The guide’s own results so far are below.'],
             tokens=[], why={'text': ['A dated result can be repeated and compared. Keeping the untested list apart is how a '
                                      'reader learns what is still unknown, such as how a real screen reader sounds.'],
                             'basis': 'Design judgment'},
             correct={'specimen': 's-19-results', 'caption': 'The guide’s own results, dated, with Tested and Not tested '
                                                             'apart.'},
             failure={'specimen': 's-19-8-failure', 'caption': '<strong>Fails Rule 19.8.</strong> A pass with no date, '
                                                               'claiming checks no one ran.'},
             specs=[{'label': 'Each report', 'value': 'The date, the build, the tool and its version, the widths'},
                    {'label': 'Tested', 'value': 'What ran and what it found, with counts'},
                    {'label': 'Not tested', 'value': 'What did not run, and why, in its own list'}],
             related=['18']),
        dict(id='19.9', title='Before launch, run the device script on an iPhone, an Android phone, a Windows PC and a Mac.',
             rule=['Four short scripts check what no container can: a real screen reader on each of the four platforms our '
                   'readers use, and a Windows contrast theme. Each step says what to press, and the ten things to listen '
                   'for say what a pass sounds like. Anyone can run them in about half an hour a device, with no training.'],
             tokens=[], why={'text': ['Screen readers and contrast themes differ from one platform to the next, and only the '
                                      'real thing shows what a reader hears and sees. Short numbered steps let anyone on the '
                                      'team run them and write down the same things.'],
                             'basis': 'Design judgment; WCAG 2.2 SC 4.1.2 and 4.1.3 are heard only on a real screen reader'},
             correct={'specimen': 's-19-devices', 'caption': 'The four scripts and the ten things to listen for.'},
             failure={'specimen': 's-19-9-failure', 'caption': '<strong>Fails Rule 19.9.</strong> “Checked with a screen '
                                                               'reader” names no device, steps or date.'},
             specs=[{'label': 'Devices', 'value': 'iPhone with VoiceOver; Android with TalkBack; Windows with NVDA and a '
                                                  'contrast theme; Mac with VoiceOver'},
                    {'label': 'When', 'value': 'Before launch, and after any change to a component in chapter 18'},
                    {'label': 'Record', 'value': 'Device, system, browser and screen reader versions, date, and each step’s '
                                                 'result with what was heard'}],
             related=['18']),
    ]
    for r in rules:
        r.setdefault('related', [])
        r.setdefault('builders', [])
    ch = {
        'number': CH, 'anchor': 'accessibility', 'title': 'Accessibility', 'part': 'Behavior',
        'instruction': 'Check a page against WCAG 2.2 AA before you call it finished.',
        'intro': [f'Accessibility means a person can use a page with a keyboard, a screen reader, zoom, voice or touch, and '
                  f'with less motion. The standard is WCAG 2.2, the Web Content Accessibility Guidelines from W3C, the body '
                  f'that writes the web’s standards. This chapter holds its {n} criteria at levels A and AA, each in W3C’s '
                  'words with the rule in this guide that meets it, then the checks that prove a page meets them.',
                  'Our own results so far come next, dated, with what was tested kept apart from what was not, and a short '
                  'script for the checks only real devices can run.'],
        'groups': [{'before_rule': '19.1', 'number': 1, 'title': 'The standard',
                    'line': 'WCAG 2.2 at level AA, in W3C’s words, with the rule that meets each criterion.'},
                   {'before_rule': '19.2', 'number': 2, 'title': 'Rules this chapter owns',
                    'line': 'Five rules that meet criteria no other chapter covers: alt text, instructions, text as text, '
                            'single presses and text that grows.'},
                   {'before_rule': '19.7', 'number': 3, 'title': 'How to check',
                    'line': 'The checks, our results so far and the script for real devices.'}],
        'rules': rules, 'extras': [],
        'related_chapters': [{'chapter': '18', 'reason': 'Every component’s keyboard path, name and announcements.'},
                             {'chapter': '17', 'reason': 'States, focus and motion under the reader’s control.'},
                             {'chapter': '05', 'reason': 'Contrast on each surface.'},
                             {'chapter': '07', 'reason': 'Reading at 320 px.'},
                             {'chapter': '20', 'reason': 'Page titles, language and help on every web page.'},
                             {'chapter': '26', 'reason': 'The token table, with the contrast of each color.'}],
        'sources': [
            'Source: W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024, '
            'w3.org/TR/WCAG22, retrieved November 10, 2026. Each criterion’s words in Rule 19.1, quoted as the '
            'Recommendation prints them; its notes are informative and sit on W3C’s Understanding pages, '
            'w3.org/WAI/WCAG22/Understanding.',
            'Source: W3C Web Accessibility Initiative, “How to Meet WCAG 2.2 (Quick Reference)”, w3.org/WAI/WCAG22/quickref, '
            'no page date, retrieved November 10, 2026.',
            'Sources for Rule 19.9: Apple, “Turn on and practice VoiceOver on iPhone” and “VoiceOver User Guide for Mac”; '
            'Google, “Get started on Android with TalkBack”; NV Access, “NVDA User Guide”; Microsoft, “Change color contrast '
            'in Windows”. The steps name the menus as each maker does; makers rename them between versions.'],
    }
    walk(ch, '19')
    return ch


BANNED = ('genuinely', 'really', 'truly', 'actually', 'leverage', 'underscore', 'simply', 'reflect')
CODES = re.compile(r'\b(?:DR|D1|D2|G1)-\d+|\bMaster Brief\b|\bPhase\b|\bGates?\b|\bthe studio\b|\bV5\b|\bAtlas V7|\b[Ss]tages?\s+[A-C]\b')


def check_words(s, where):
    t = re.sub(r'<code>.*?</code>', '', s, flags=re.S)
    plain = re.sub(r'<[^>]+>', '', t)
    plain = re.sub(r'alt=""|aria-hidden="true"|white-space: nowrap', '', plain)
    bad = [w for w in BANNED if re.search(r'\b' + w + r'\b', plain, re.I)]
    if EM in plain or EN in plain:
        bad.append('dash')
    if re.search(r'"[A-Za-z]', plain) or re.search(r"(?<=[a-z])'(?=[a-z])", plain):
        bad.append('straight quote')
    if CODES.search(plain):
        bad.append('studio code ' + CODES.search(plain).group(0))
    if re.search(r',\s+not\s+\w+', plain):
        bad.append('a “, not” turn')
    if bad:
        raise SystemExit(f'{where}: {", ".join(bad)}: {plain[:160]}')


def walk(o, where):
    if isinstance(o, str):
        check_words(o, where)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            walk(x, f'{where}[{i}]')
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ('specimen', 'token', 'tokens', 'id', 'anchor', 'number', 'related', 'before_rule', 'chapter'):
                walk(v, f'{where}.{k}')


def outputs():
    ch = build()
    for sid, s in SPECS.items():
        if sid != 's-19-criteria':     # W3C's words stay as W3C prints them
            check_words(re.sub(r'<style>.*?</style>|<script>.*?</script>', '', s['html'], flags=re.S), sid)
        check_words(s['meta']['alt'], sid + '.alt')
    used = {r['correct']['specimen'] for r in ch['rules']} | {r['failure']['specimen'] for r in ch['rules']}
    if used != set(SPECS):
        raise SystemExit(f'specimens placed and written differ: {sorted(used ^ set(SPECS))}')
    out = {OUT_CH: json.dumps(ch, indent=2, ensure_ascii=False) + '\n',
           MANIFEST: json.dumps({k: SPECS[k]['meta'] for k in sorted(SPECS)}, indent=1, ensure_ascii=False) + '\n'}
    for sid, s in SPECS.items():
        out[OUT_SP / f'{sid}.html'] = s['html']
    return out, ch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    out, ch = outputs()
    if a.check:
        stale = [str(p.relative_to(ROOT)) for p, t in out.items() if not p.exists() or p.read_text() != t]
        print('chapter 19: current' if not stale else 'chapter 19: stale ' + ', '.join(stale))
        sys.exit(1 if stale else 0)
    for old in OUT_SP.glob('s-19-*.html'):
        if old not in out:
            old.unlink()
    for p, t in out.items():
        p.write_text(t)
    print(f'chapter 19: {len(ch["rules"])} rules, {len(SPECS)} specimens, '
          f'{sum(len(s["html"]) for s in SPECS.values()):,} bytes of specimens')


if __name__ == '__main__':
    main()
