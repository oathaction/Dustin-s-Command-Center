"""Chapter 19, Accessibility (accessibility lead), stage C round 1, November 11, 2026; round 2's fix pass the same day.

Usage:
    python3 -I work/build/scripts/phase-2/stage_c_ch19_build.py            write the chapter and its specimens
    python3 -I work/build/scripts/phase-2/stage_c_ch19_build.py --check    write nothing; exit 1 if any output differs
    python3 -I work/build/scripts/phase-2/stage_c_ch19_build.py --read-wcag <wcag22.html> --read-on "November 11, 2026"
                                                                         rewrite the stored copy of WCAG 2.2's criteria
                                                                         from a copy of the Recommendation fetched from
                                                                         https://www.w3.org/TR/WCAG22/, then stop

Writes:
    work/build/guide/chapters/19-accessibility.json         the chapter in the content contract (round 1 brief)
    work/build/guide/specimens/s-19-*.html                  its specimens
    work/build/guide/specimens/manifest-accessibility.json  their entries (D2-1267)

Reads:
    work/handoffs/phase-2/20261111_WCAG22-Criteria-Text.json: the 55 WCAG 2.2 criteria at levels A and AA in W3C's
        words and in the Recommendation's document order, read from w3.org on November 11, 2026 by --read-wcag (the
        Recommendation of December 12, 2024; the file names its address and the SHA-256 of the copy read). Notes,
        examples and definitions are W3C's informative text and stay out (D2-1138); 4.1.1 Parsing is listed as removed
        (D2-1139). Rule 19.1's list prints each criterion's parts in that order, and the build stops when the words it
        printed, read back from its own HTML, differ from the stored copy (round 2, BE-M2).
    work/handoffs/phase-2/20261111_Gate-2-Ch19-Results.json: the guide's own results on the Gate 2 preview after the fix
        pass, dated, Tested and Not tested apart, written by the accessibility lead from the main session's final runs, which
        it names. Round 1's and round 2's files stay as the record. A missing file prints as pending. The build stops on a
        studio role in the printed lines, and on the icon set's name in any case but "Civic Line" (DT-S12).
    work/build/guide/chapters/*.json: every rule this chapter's map cites must exist in a chapter file that is present,
        and a chapter that is not written yet is named in words, never linked.

The map of criterion to rule starts from the round 0 inventory's section 4 and adds chapters 17, 18, 19 and 26. A
criterion reads Met only where a rule states what it asks (round 2, D2-1553).
"""
import argparse
import hashlib
import html
import html.parser
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
WCAG = ROOT / 'work/handoffs/phase-2/20261111_WCAG22-Criteria-Text.json'
RESULTS = ROOT / 'work/handoffs/phase-2/20261111_Gate-2-Ch19-Results.json'   # Gate 2's call 12; round 1's and round 2's files stay as the record
CH = '19'
EM, EN = '—', '–'
WORDS = 'zero one two three four five six seven eight nine'.split()


def w(n, cap=False):
    """House rule H06: a number under ten in prose is a word."""
    t = WORDS[n] if n < 10 else f'{n:,}'
    return t[0].upper() + t[1:] if cap else t

e = html.escape

# ------------------------------------------------------------------------------------------------- WCAG's words
def norm(t):
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()


class _Parts(html.parser.HTMLParser):
    """Read a criterion's normative parts in document order: a paragraph, or a list whose items may carry a label (a
    definition list in the Recommendation). Notes, examples, definition pop-ups, the level and the "New" mark stay out.
    The same reader reads back the HTML this script prints, so both sides of the check are read one way."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip, self.buf, self.mode, self.label = [], 0, None, None, None

    def handle_starttag(self, tag, attrs):
        cls = (dict(attrs).get('class') or '').split()
        if self.skip:
            if tag in ('div', 'p', 'span'):
                self.skip += 1
            return
        if (tag == 'div' and {'note', 'doclinks', 'example'} & set(cls)) or (tag == 'p' and {'conformance-level', 'change'} & set(cls)) \
                or (tag == 'span' and 'dfn-panel' in cls):
            self.skip = 1
        elif tag in ('ul', 'ol', 'dl') and self.mode is None:
            self.mode = tag
            self.parts.append({'list': []})
        elif (self.mode in ('ul', 'ol') and tag == 'li') or (self.mode == 'dl' and tag in ('dt', 'dd')) or (self.mode is None and tag == 'p'):
            self.buf = []

    def handle_endtag(self, tag):
        if self.skip:
            if tag in ('div', 'p', 'span'):
                self.skip -= 1
            return
        if self.mode and tag == self.mode:
            self.mode = None
        elif self.mode in ('ul', 'ol') and tag == 'li':
            self.parts[-1]['list'].append({'text': norm(''.join(self.buf))})
            self.buf = None
        elif self.mode == 'dl' and tag == 'dt':
            self.label, self.buf = norm(''.join(self.buf)), None
        elif self.mode == 'dl' and tag == 'dd':
            self.parts[-1]['list'].append({'label': self.label, 'text': norm(''.join(self.buf))})
            self.buf, self.label = None, None
        elif self.mode is None and tag == 'p' and self.buf is not None:
            self.parts.append({'p': norm(''.join(self.buf))})
            self.buf = None

    def handle_data(self, d):
        if not self.skip and self.buf is not None:
            self.buf.append(d)


def parts_of(fragment):
    r = _Parts()
    r.feed(fragment)
    r.close()
    return r.parts


def read_wcag(src, read_on):
    """Write the stored copy from a copy of the Recommendation fetched from w3.org (BE-M2)."""
    raw = pathlib.Path(src).read_bytes()
    doc = raw.decode('utf-8')
    crit, removed = [], []
    for m in re.finditer(r'<section id="([^"]+)" class="guideline"><div class="header-wrapper"><h4 id="[^"]+">'
                         r'<bdi class="secno">Success Criterion (\d\.\d+\.\d+) </bdi>(.*?)</h4>(.*?)</section>', doc, re.S):
        sid, n, name, body = m.groups()
        name = norm(re.sub(r'<[^>]+>', '', name))
        lv = re.search(r'<p class="conformance-level">\(Level (A{1,3})\)</p>', body)
        und = re.search(r'<a href="(https://www\.w3\.org/WAI/WCAG22/Understanding/[^"]+)">', body)
        if not lv:
            removed.append({'n': n, 'name': name, 'id': sid})
        elif lv.group(1) != 'AAA':
            crit.append({'n': n, 'name': name, 'level': lv.group(1), 'new': '<p class="change">New</p>' in body, 'id': sid,
                         'understanding': und.group(1) if und else None, 'parts': parts_of(body)})
    status = re.search(r'W3C Recommendation \d{1,2} \w+ \d{4}', doc)
    this = re.search(r'https://www\.w3\.org/TR/\d{4}/REC-WCAG22-\d{8}/', doc)
    out = {
        'about': ('The 55 success criteria of WCAG 2.2 at levels A and AA, in the Recommendation’s own words and in its '
                  'document order, read from w3.org by stage_c_ch19_build.py --read-wcag. Each criterion’s parts run as the '
                  'Recommendation prints them: a paragraph, or a list whose items may carry a label. Notes, examples and '
                  'definitions are informative and stay out. Rule 19.1 prints its list from this file, and the build stops '
                  'when the words it prints differ from it.'),
        'title': 'Web Content Accessibility Guidelines (WCAG) 2.2',
        'status': status.group(0) if status else None,
        'url': 'https://www.w3.org/TR/WCAG22/',
        'this_version': this.group(0) if this else None,
        'read': read_on,
        'sha256': hashlib.sha256(raw).hexdigest(),
        'bytes': len(raw),
        'count': {'A': sum(c['level'] == 'A' for c in crit), 'AA': sum(c['level'] == 'AA' for c in crit),
                  'all': len(crit), 'new': sum(c['new'] for c in crit)},
        'removed': removed,
        'criteria': crit,
    }
    if out['count'] != {'A': 31, 'AA': 24, 'all': 55, 'new': 6} or [r['n'] for r in removed] != ['4.1.1']:
        raise SystemExit(f'the copy read does not hold WCAG 2.2’s 55 criteria and 4.1.1: {out["count"]}, {removed}')
    WCAG.write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    print(f'{WCAG.relative_to(ROOT)}: {len(crit)} criteria, {out["status"]}, SHA-256 {out["sha256"][:16]}…')


def criteria():
    d = json.loads(WCAG.read_text())
    out = d['criteria']
    if len(out) != 55 or sum(c['level'] == 'A' for c in out) != 31 or sum(c['new'] for c in out) != 6:
        raise SystemExit(f'expected 55 criteria, 31 at level A and 6 new; the stored copy holds {len(out)}')
    for c in out:
        if not c['parts'] or any(not (p.get('p') or p.get('list')) for p in c['parts']):
            raise SystemExit(f'{c["n"]}: an empty part in the stored copy')
    return out


def quote_html(parts):
    """W3C's words in the Recommendation's order: each paragraph, then each list where it stands; a labeled item keeps
    its label as a term, as the Recommendation sets it."""
    out = []
    for p in parts:
        if 'p' in p:
            out.append(f'<p>{e(p["p"], quote=False)}</p>')
        elif any(i.get('label') for i in p['list']):
            out.append('<dl>' + ''.join(f'<dt>{e(i["label"], quote=False)}</dt><dd>{e(i["text"], quote=False)}</dd>'
                                        for i in p['list']) + '</dl>')
        else:
            out.append('<ul>' + ''.join(f'<li>{e(i["text"], quote=False)}</li>' for i in p['list']) + '</ul>')
    return ''.join(out)


def check_printed(printed):
    """Read back every criterion the list printed, in order, and stop on any difference from the stored copy, read
    afresh from its file (BE-M2)."""
    crit = json.loads(WCAG.read_text())['criteria']
    items = re.findall(r'<li class="c19-c" data-st="\w+"><p class="c19-ch"><span class="c19-cn">([\d.]+)</span> '
                       r'<span class="c19-ct">(.*?)</span> <span class="c19-lv">Level (A{1,2})</span>.*?</p>'
                       r'<blockquote class="c19-q">(.*?)</blockquote>', printed, re.S)
    if [i[0] for i in items] != [c['n'] for c in crit]:
        raise SystemExit('Rule 19.1’s list prints the criteria out of the Recommendation’s order, or drops one')
    for (n, name, level, quote), c in zip(items, crit):
        got = parts_of(quote)
        want = [p if 'p' in p else {'list': [{k: v for k, v in i.items() if v is not None} for i in p['list']]} for p in c['parts']]
        if norm(name) != c['name'] or level != c['level'] or got != want:
            first = next((f'part {k + 1}: printed {g!r}, stored {w!r}' for k, (g, w) in enumerate(zip(got, want)) if g != w),
                         f'{len(got)} parts printed, {len(want)} stored')
            raise SystemExit(f'{n} {c["name"]}: the printed text differs from the stored copy of the Recommendation; {first}')


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
    '1.3.1': ('part', ['18.10', '18.3', '18.17', '18.6', '18.7', '11.5'], 'Tables, forms, lists, landmarks and the current place keep their structure in markup; chapter 20 owes the headings of a whole page.'),
    '1.3.2': ('part', ['18.22', '18.6'], 'Components keep their order; chapter 20 owes the reading order of a whole page.'),
    '1.3.3': ('met', ['19.3'], ''),
    '1.3.4': ('met', ['19.6'], ''),
    '1.3.5': ('met', ['18.17'], ''),
    '1.4.1': ('met', ['05.4', '17.8', '17.10', '18.2', '18.5', '18.7', '19.3', '11.2', '11.15', '12.6'], ''),
    '1.4.2': ('none', ['17.3'], 'No product plays sound; chapter 23 if a page ever does.'),
    '1.4.3': ('met', ['05.2', '26.7'], ''),
    '1.4.4': ('met', ['19.6', '07.5', '06.2'], ''),
    '1.4.5': ('met', ['19.4'], ''),
    '1.4.10': ('met', ['07.6', '19.6', '18.11'], ''),
    '1.4.11': ('met', ['05.5', '17.8', '17.9', '11.2'], ''),
    '1.4.12': ('met', ['19.6'], ''),
    '1.4.13': ('part', ['18.23', '18.6', '11.11'], 'A drawing’s readout stays in its own line and covers nothing, and menus open on a press; no rule yet sets the three conditions for words that show on hover or focus, such as a tooltip, which chapter 18 owes if a product adds one.'),
    '2.1.1': ('met', ['18.1', '18.9', '18.23', '19.5'], 'Every rule of chapter 18 gives its keyboard path.'),
    '2.1.2': ('met', ['18.6', '18.23'], ''),
    '2.1.4': ('met', ['19.5'], ''),
    '2.2.1': ('none', [], 'No product sets a time limit today; the chapter that adds one owes it. A loop a reader plays holds each step at least six seconds, and Pause stops it (Rule 18.22).'),
    '2.2.2': ('met', ['17.3', '17.4', '18.22'], ''),
    '2.3.1': ('part', ['17.1', '17.3'], 'Motion plays only on request; chapter 23 owes the flash test for video.'),
    '2.4.1': ('met', ['18.5', '18.6'], ''),
    '2.4.2': ('gap', [], 'Chapter 20, with each web page. This guide’s own page has a title.'),
    '2.4.3': ('part', ['18.6', '18.16', '18.17', '18.21', '18.22', '18.23'], 'Each component says where focus goes; chapter 20 owes the focus order of a whole page.'),
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
    '3.3.4': ('gap', [], 'Chapter 18 owes a rule that lets a reader check, confirm or undo a send that reaches a legislature, such as testimony, and a delete of saved items.'),
    '3.3.7': ('none', [], 'No form has more than one step today; chapter 18 when one does.'),
    '3.3.8': ('none', [], 'No product has accounts today; the chapter that adds them owes it.'),
    '4.1.2': ('met', ['18.1', '18.2', '18.9', '17.11'], 'Every rule of chapter 18 gives its accessible name and states.'),
    '4.1.3': ('met', ['18.18', '18.12', '18.15', '18.16', '18.20', '11.15'], ''),
}
STATUS_WORD = {'met': 'Met', 'part': 'Met in part', 'gap': 'Gap', 'none': 'Not used today'}
# The chapters that owe each gap, and what no product does today, for Rule 19.1's specifications
GAP_OWNERS = {'1.2.1': ['16', '23'], '1.2.2': ['16', '23'], '1.2.3': ['16', '23'], '1.2.5': ['16', '23'], '2.4.2': ['20'],
              '3.1.1': ['20'], '3.1.2': ['02', '20'], '3.2.6': ['20'], '3.3.4': ['18']}
NONE_WHAT = {'1.2.4': 'live captions', '1.4.2': 'sound that plays itself', '2.2.1': 'time limits',
             '3.3.7': 'forms of more than one step', '3.3.8': 'sign-in'}


def sort_key(n):
    return tuple(int(x) for x in n.split('.'))


def and_list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


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


def spec(sid, html_, rule, alt, width=None, interactive=False, readable=False, illustrative=False, notes='', exempt=None,
         scale=None):
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
    if scale:
        meta['scale'] = scale
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


def picture(sid, rule, body, alt, notes, fail=False, illus=True, css='', exempt=None, width=360, scale=None, root=''):
    h = (f'<style>{BASE}{FAIL_CSS}{css}</style><div class="c19{root}">{BAND if fail else ""}<div class="c19-ui">'
         f'{ILL if illus else ""}{body}</div></div>')
    return spec(sid, h, rule, alt, width=width, illustrative=illus, notes=notes, exempt=exempt, scale=scale)


def s_criteria(crit, held, own):
    rows = []
    counts = {'met': 0, 'part': 0, 'gap': 0, 'none': 0}
    for c in crit:
        st, rules, note = MAP[c['n']]
        counts[st] += 1
        order = sorted(rules, key=lambda r: (int(r.split('.')[0]), int(r.split('.')[1])))   # in the page's order
        links = [rule_link(r, held, own) for r in order]
        rl = links[0] if len(links) == 1 else ', '.join(links[:-1]) + ' and ' + links[-1] if links else ''
        what = (f'<span class="c19-st c19-st--{st}">{STATUS_WORD[st]}</span>'
                + ((f' Rule {rl}.' if len(links) == 1 else f' Rules {rl}.') if links else '')
                + (f' {e(note)}' if note else ''))
        new = ' <span class="c19-new">New in 2.2</span>' if c['new'] else ''
        rows.append(f'<li class="c19-c" data-st="{st}"><p class="c19-ch"><span class="c19-cn">{c["n"]}</span> '
                    f'<span class="c19-ct">{e(c["name"])}</span> <span class="c19-lv">Level {c["level"]}</span>{new}</p>'
                    f'<blockquote class="c19-q">{quote_html(c["parts"])}</blockquote><p class="c19-m">{what}</p></li>')
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
           '.c19-q>*+*{margin-top:6px}.c19-q ul{padding-left:18px}.c19-q li+li,.c19-q dd+dt{margin-top:4px}'
           '.c19-q dt{font-weight:var(--oa-font-weight-bold)}.c19-q dd{margin:0}'
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
            '<p class="c19-rm"><b>4.1.1 Parsing</b> was removed in WCAG 2.2, which keeps its number with no level. W3C’s '
            'Understanding page says many of the problems it covered now fail 1.3.1 or 4.1.2, so no rule here is tied to '
            'it.</p></div>' + script)
    check_printed(body)
    sid = spec('s-19-criteria', body, '19.1',
               f'A searchable list of the {total} WCAG 2.2 success criteria at levels A and AA, in W3C’s words. Each entry '
               'gives the number, the name, the level, a tag for the six new in 2.2, the criterion’s words, and how this '
               f'guide meets it: {counts["met"]} are met by a rule, {counts["part"]} in part, {counts["gap"]} are gaps with '
               f'the chapter that owes each, and {counts["none"]} govern things no product does today. A search field and a '
               'choice of All, Met, Met in part, Gaps or Not used today narrow the list, and a status line says how many '
               'show. A last line says 4.1.1 Parsing was removed in WCAG 2.2.',
               interactive=True, notes='Live: search and a radio choice filter the list; the count goes to a polite status line (Rule 18.15).')
    return sid, counts


# ------------------------------------------------------------------------------------------------- the opener
def s_opener(counts, n):
    """Chapter 19's opener (CD-S18, D2-1550): the status counts as a picture that flows with the column."""
    tiles = (('met', 'Met', 'a rule states what it asks'), ('part', 'Met in part', 'a rule covers some of it'),
             ('gap', 'Gaps', 'each with the chapter that owes it'), ('none', 'Not used today', 'no product does what it covers yet'))
    css = ('.c19-ot{font:var(--oa-type-caption);color:var(--sec);margin-bottom:8px}'
           '.c19-og{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(9rem,1fr));gap:8px}'
           '.c19-oc{border:1px solid var(--edge);padding:12px;display:grid;gap:2px;align-content:start}'
           '.c19-on{font:var(--oa-type-h3);font-variant-numeric:tabular-nums}.c19-ow{font:var(--oa-type-ui)}'
           '.c19-ow--met::before{content:"\\2713";margin-right:4px}.c19-ow--gap::before{content:"\\25B3";margin-right:4px}'
           '.c19-ox{font:var(--oa-type-caption);color:var(--sec)}')
    body = (f'<style>{BASE}{css}</style><div class="c19"><p class="c19-ot">WCAG 2.2’s {n} criteria at levels A and AA, as this '
            'guide meets them today</p><ul class="c19-og">'
            + ''.join(f'<li class="c19-oc"><span class="c19-on">{counts[k]}</span><span class="c19-ow c19-ow--{k}">{e(word)}</span>'
                      f'<span class="c19-ox">{e(why)}</span></li>' for k, word, why in tiles) + '</ul></div>')
    return spec('s-19-opener', body, None,
                f'Where this guide stands on WCAG 2.2’s {n} criteria at levels A and AA: {counts["met"]} met, where a rule '
                f'states what the criterion asks; {counts["part"]} met in part; {counts["gap"]} gaps, each with the chapter '
                f'that owes it; and {counts["none"]} not used today, since no product does what they cover yet.',
                notes='Chapter 19’s opener (CD-S18, D2-1550): the counts from Rule 19.1’s map, as a picture that flows with '
                      'the column at true size.')


# ------------------------------------------------------------------------------------------------- results and the matrix
MATRIX = [
    # (check, what it shows, method, criteria, how to run it: HTML with the code in <code>, or '' where a person runs it)
    ('Every page rendered', 'Each page draws whole at the widths readers use', 'Screenshots at 1440, 1024, 390 and 360 px, looked at by a person', '1.4.10', ''),
    ('Report pages', 'Every page of a report reads in the reader', 'A screenshot of each page in the report reader', '1.4.10, 4.1.2', ''),
    ('Keyboard and focus', 'Every control is reached in order, shows its ring, holds no trap and is big enough to press',
     'A script presses Tab through the page, walks each component’s keyboard path and measures each control’s size; a person checks the order and the ring',
     '2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11, 2.5.8',
     'To list each control under 24 by 24 px, paste this into the browser’s console: <code>document.querySelectorAll(\'a, button, input, select, '
     'summary, [tabindex]\').forEach(el =&gt; { const r = el.getBoundingClientRect(); if (r.width &amp;&amp; (r.width &lt; 24 || r.height &lt; 24)) '
     'console.log(el, Math.round(r.width), Math.round(r.height)); })</code>. A link inside a sentence may be smaller.'),
    ('Reading order and headings', 'The outline makes sense read aloud', 'The accessibility tree’s outline, read by script and by a person', '1.3.1, 1.3.2, 2.4.6',
     'In Chrome’s developer tools, open the Elements panel’s Accessibility pane and turn on the full-page accessibility tree.'),
    ('Forms and messages', 'A reader can find and fix every field, then send the form', 'Send each form empty, then with a mistake, by keyboard: focus lands on '
     'the first field to fix, its description holds the message, and the status line holds the result', '1.3.5, 3.3.1, 3.3.2, 3.3.3, 4.1.3', ''),
    ('Automated rules', 'The faults a machine can find are gone', 'axe-core with the tags wcag2a, wcag2aa, wcag21a, wcag21aa and wcag22aa on every page',
     'Parts of many, such as 1.1.1, 1.3.1, 1.4.3, 2.4.2, 2.4.4, 3.1.1 and 4.1.2',
     '<code>npx @axe-core/cli https://example.org/your-page --tags wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa --exit</code>, which needs Chrome '
     'and stops with an error when a rule fails.'),
    ('Contrast', 'Text, marks, edges and focus rings stand out from their ground',
     'A script reads each rendered color pair, states included; a person measures marks, edges and rings against 3 to 1', '1.4.3, 1.4.11',
     'For text: <code>npx @axe-core/cli https://example.org/your-page --rules color-contrast</code>. For marks and edges, a color picker and '
     'the ratios in chapter 26’s token table.'),
    ('Text at 200 percent and 320 px', 'Nothing is cut off, lost or broken in the middle of a word when text grows, spacing opens or the screen narrows',
     'Text doubled, the page at 320 px, then line height 1.5, paragraph spacing 2 times the size, letter spacing 0.12 and word spacing 0.16 '
     'times the size, all at once. A script finds sideways scroll and clipped boxes, and a person reads for words broken in the middle',
     '1.4.4, 1.4.10, 1.4.12',
     'To double the text, paste <code>document.documentElement.style.fontSize = \'200%\'</code> into the console; then '
     '<code>document.documentElement.scrollWidth &gt; innerWidth</code> reads true where the page scrolls sideways. For the spacing, add '
     '<code>* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important } p { margin-bottom: 2em '
     '!important }</code>.'),
    ('Reduced motion', 'Nothing moves on its own, and every motion has a still end', 'The browser set to reduce motion, then each moving part played', '2.2.2, 2.3.1',
     'In Chrome’s developer tools, open Rendering and set “Emulate CSS media feature prefers-reduced-motion” to reduce.'),
    ('Forced colors', 'Every mark, edge and state survives a contrast theme', 'The browser set to forced colors, light and dark, then each part read by script and by eye', '1.4.1, 1.4.11',
     'In Rendering, set “Emulate CSS media feature forced-colors” to active, with prefers-color-scheme set to light, then to dark.'),
    ('Dark surfaces and long labels', 'Each part reads on every surface it uses, with the longest real words',
     'Each part on Newsprint, Charcoal and any other surface it uses, filled with the longest real words it will hold, such as the longest title in its data',
     '1.4.3, 1.4.10', ''),
    ('Print', 'A printed page keeps its words and order', 'Print emulation and the print stylesheet: every word prints, in reading order, and nothing is cut at a page’s edge', '1.3.2',
     'In Rendering, set “Emulate CSS media type” to print.'),
    ('Downloads', 'Each file arrives whole and named', 'Press each download, open each file, check SVG validity and PNG size', '2.4.4', ''),
    ('Diagram and chart equivalents', 'A reader who cannot see a drawing gets its connections', 'Each drawing checked for its words or table and its reading guide', '1.1.1, 1.3.1', ''),
    ('Grayscale', 'Nothing rests on color alone', 'Grayscale screenshots of every page, with each state shown', '1.4.1',
     'Paste <code>document.documentElement.style.filter = \'grayscale(1)\'</code> into the console.'),
]


ROLE_WORDS = re.compile(r'\b(?:engineer|designer|lead|owner|editor|creative director|main session|studio|red team)s?\b', re.I)


def load_results():
    if not RESULTS.exists():
        return None
    return json.loads(RESULTS.read_text())


def s_matrix():
    rows = ''.join(f'<li class="c19-r"><p class="c19-rt">{e(c)}</p><dl class="c19-dl"><div><dt>What it shows</dt><dd>{e(w)}</dd></div>'
                   f'<div><dt>Method</dt><dd>{e(m)}</dd></div><div><dt>Criteria</dt><dd>{e(k)}</dd></div>'
                   + (f'<div><dt>To run it</dt><dd>{run}</dd></div>' if run else '') + '</dl></li>'
                   for c, w, m, k, run in MATRIX)
    css = ('.c19-ml{list-style:none;padding:0;margin:0}.c19-r{padding:12px 0;border-top:1px solid var(--hair)}'
           '.c19-rt{font:var(--oa-type-ui)}.c19-dl{margin:6px 0 0;display:grid;gap:4px;font:var(--oa-type-body-small)}'
           '.c19-dl div{display:grid;grid-template-columns:minmax(6rem,9rem) 1fr;gap:8px}.c19-dl dt{color:var(--sec)}.c19-dl dd{margin:0;min-width:0}'
           '.c19-dl code{font-family:ui-monospace,monospace;font-size:0.875em;overflow-wrap:anywhere}'
           '@media (max-width:30em){.c19-dl div{grid-template-columns:1fr;gap:0}}')
    return spec('s-19-matrix', f'<style>{BASE}{css}</style><div class="c19"><ol class="c19-ml">{rows}</ol></div>', '19.7',
                f'The verification matrix: {len(MATRIX)} checks, each with what it shows, its method, the WCAG 2.2 '
                'criteria it serves and, where a tool runs it, how. ' + ' '.join(f'{c}: {m}.' for c, _, m, _, _ in MATRIX), readable=True,
                notes='Readable: the checks and methods of the verification matrix, with what each shows.')


def s_results(res):
    css = ('.c19-h{font:var(--oa-type-ui);margin:0 0 6px}.c19-h+.c19-rl{margin-bottom:16px}'
           '.c19-rl{padding-left:20px;font:var(--oa-type-body-small)}.c19-rl li+li{margin-top:6px}'
           '.c19-meta{font:var(--oa-type-caption);color:var(--sec);margin-bottom:12px}')
    if not res:
        body = '<p class="c19-meta">The results file is not written yet.</p>'
        alt = 'The guide’s own results: pending.'
    else:
        # BE-S7: an open item reads "Open, to fix before launch.", and no line names a studio role
        for x in res['tested']:
            x['result'] = x['result'].rstrip() + (' Open, to fix before launch.' if x.get('open') else '')
        for x in res['tested'] + res['not_tested'] + [{'check': 'build', 'build': res['build']}]:
            words = ' '.join(str(v) for v in x.values())
            m = ROLE_WORDS.search(words)
            if m:
                raise SystemExit(f'the results name a role, “{m.group(0)}”, in “{x["check"]}”; write an open item as open, to fix before launch')
            # DT-S12: one name for the icon set, as every other chapter writes it
            m = re.search(r'\b(?!Civic Line\b)[Cc]ivic [Ll]ine\b', words)
            if m:
                raise SystemExit(f'the results write “{m.group(0)}” in “{x["check"]}”; the set is “Civic Line”')
        t = ''.join(f'<li><b>{e(x["check"])}.</b> {e(x["result"])}</li>' for x in res['tested'])
        n = ''.join(f'<li><b>{e(x["check"])}.</b> {e(x["why"])}</li>' for x in res['not_tested'])
        body = (f'<p class="c19-meta">{e(res["build"])}</p><p class="c19-h">Tested on {e(res["date"])}</p><ul class="c19-rl">{t}</ul>'
                f'<p class="c19-h">Not tested</p><ul class="c19-rl">{n}</ul>')
        alt = (f'The guide’s own results, {res["date"]}. {res["build"]} Tested: '
               + ' '.join(f'{x["check"]}: {x["result"]}' for x in res['tested']) + ' Not tested: '
               + ' '.join(f'{x["check"]}: {x["why"]}' for x in res['not_tested']))
    return spec('s-19-results', f'<style>{BASE}{css}</style><div class="c19">{body}</div>', '19.8', alt, readable=True,
                notes=f'Readable: printed from {RESULTS.name}, which names the runs behind each line.')


# ------------------------------------------------------------------------------------------------- the device script
LOOK = [
    'The page’s title is read as the page opens.',
    'The first stop is “Skip to main content”.',
    'Headings come in order: the page’s title first, then each part under it.',
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
        'button three times, or the Home button on an iPhone that has one, turns VoiceOver on and off.',
        'Open the page in Safari, then press that button three times. VoiceOver says “VoiceOver on”.',
        'Swipe right with one finger to move to the next item, and left to go back. Each item is read aloud.',
        'Double-tap anywhere to press the item VoiceOver is on. To type, double-tap a field, type, then swipe right to move on.',
        'Go through the ten things to listen for below, and write Pass or Fail beside each with what you heard.',
        'Press that button three times to turn VoiceOver off.']),
    ('Android phone with TalkBack', [
        'Open Settings, then Accessibility, then TalkBack, and turn on the TalkBack shortcut. Makers name these menus '
        'differently; the shortcut is usually holding both volume keys for three seconds.',
        'Open the page in Chrome, then hold both volume keys for three seconds. TalkBack says it is on.',
        'Swipe right with one finger to move to the next item, and left to go back. Scroll with two fingers.',
        'Double-tap anywhere to press the item TalkBack is on. To type, double-tap a field, type, then swipe right to move on.',
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
        'Insert and Q, then Enter, to quit NVDA.',
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
            'version, the date, and each step’s result with what you heard. Write a fail down with the words you heard, so the builder can find what broke.</p></div></div>')
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
    # 19.2's chart (CD-S13): a title, each bar's count and year, and a source line, as chapter 12's rules set; HTML bars, so
    # every word stays at its size (D2-1498). Invented counts, under the plate's Illustrative chip.
    chart_css = ('.c19-cht{font:var(--oa-type-ui);margin-bottom:8px}.c19-bars{display:flex;align-items:flex-end;gap:12px;'
                 'height:104px;border-bottom:1px solid var(--edge)}.c19-bar{flex:1;display:flex;flex-direction:column;'
                 'justify-content:flex-end;align-items:center;gap:2px;font:var(--oa-type-caption);height:100%}'
                 '.c19-bar i{display:block;width:100%;background:var(--ink)}.c19-yrs{display:flex;gap:12px;margin-top:4px;'
                 'font:var(--oa-type-caption);color:var(--sec)}.c19-yrs span{flex:1;text-align:center}'
                 '.c19-src{margin-top:8px;font:var(--oa-type-caption);color:var(--sec)}')
    counts = ((2023, 120), (2024, 180), (2025, 240), (2026, 310))
    chart = ('<div class="c19-box"><p class="c19-cht">Comments on the county budget, 2023 to 2026</p><div class="c19-bars">'
             + ''.join(f'<span class="c19-bar">{v}<i style="height:{round(v / 310 * 80)}px"></i></span>' for _, v in counts)
             + '</div><p class="c19-yrs">' + ''.join(f'<span>{y}</span>' for y, _ in counts) + '</p>'
             '<p class="c19-src">Source: Alder County clerk’s comment log, 2023 to 2026.</p></div>')
    chart_words = ('a bar chart titled “Comments on the county budget, 2023 to 2026”, its four bars rising from 120 comments in '
                   '2023 through 180 and 240 to 310 in 2026, each with its count above it and its year below, and a source line')
    picture('s-19-2-correct', '19.2',
            '<p class="c19-k">A drawing beside its word: the word carries it</p><div class="c19-box c19-row">'
            '<svg viewBox="0 0 128 128" width="48" height="48" aria-hidden="true" focusable="false" data-icon="CL-001" '
            'data-icon-family="topic" style="color:var(--oa-color-text-primary)"><use href="#oa-sym-cl-001"/></svg><span>Voting</span></div>'
            '<p class="c19-code" style="margin-top:6px"><code>alt=""</code></p>'
            '<p class="c19-k" style="margin-top:14px">A chart alone: its alt gives its finding</p>' + chart +
            '<p class="c19-code" style="margin-top:6px"><code>alt="Comments on the county budget rose each year, from 120 in 2023 to 310 in 2026."</code></p>',
            'An Illustrative pair at 360 px. First, the Voting symbol beside its word, “Voting”, marked with empty alt text '
            f'because the word says it. Second, {chart_words}, with the alt text “Comments on the county budget rose each year, '
            'from 120 in 2023 to 310 in 2026.”',
            'Correct: alt text for purpose, and empty alt where a word already says it. Invented counts.', css=chart_css)
    picture('s-19-2-failure', '19.2', chart +
            '<p class="c19-code" style="margin-top:6px"><code>alt="chart_final_v2.png"</code></p>'
            '<p class="c19-n">A screen reader hears a file name, and nothing of what the chart shows.</p>',
            f'Failure case: do not publish. The same Illustrative chart at 360 px, {chart_words}, with the alt text '
            '“chart_final_v2.png”, a file name. A note says a screen reader hears nothing of what the chart shows.',
            'Picture of a fault: alt text that names a file. Invented counts.', fail=True, css=chart_css)
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
    # 19.4's failure (CD-S13): the headline as a picture, soft at true size, and a drawing of "Th" enlarged until its
    # pixels show; the drawing stands for the pixels and claims no exact scale
    pix = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (8, 3), (9, 3), (10, 4), (10, 5), (10, 6)]
    soft = [(10, 3), (8, 4)]
    crop = ('<svg viewBox="0 0 66 42" width="198" height="126" aria-hidden="true" focusable="false" shape-rendering="crispEdges">'
            '<g fill="var(--oa-color-text-primary-on-prussian)">' + ''.join(f'<rect x="{x * 6}" y="{y * 6}" width="6" height="6"/>' for x, y in pix)
            + '</g><g fill="var(--oa-color-text-primary-on-prussian)" fill-opacity="0.45">'
            + ''.join(f'<rect x="{x * 6}" y="{y * 6}" width="6" height="6"/>' for x, y in soft) + '</g></svg>')
    picture('s-19-4-failure', '19.4',
            '<div style="background:var(--oa-color-surface-prussian);padding:16px">'
            '<p class="c19-soft">The zoning code &amp; the rent.</p></div>'
            '<p class="c19-k" style="margin-top:12px">Its first two letters, enlarged until each pixel shows</p>'
            '<div style="background:var(--oa-color-surface-prussian);padding:12px;display:inline-block">' + crop + '</div>'
            '<p class="c19-n">The headline is a picture: it goes soft on a sharp screen, breaks into squares when zoomed, cannot be '
            'found or translated, and a screen reader hears only its alt text, if any.</p>',
            'Failure case: do not publish. The Illustrative hinge headline “The zoning code & the rent.” at 360 px, set as a '
            'picture on a Prussian band, its letters soft at the edges. Under it, its first two letters, T and h, enlarged '
            'until each pixel shows as a square. A note says it cannot be found, translated or read aloud from its words.',
            'Picture of a fault: a picture of text in place of text (SC 1.4.5).', fail=True,
            css='.c19-soft{font:var(--oa-type-h4);font-size:1.25rem;color:var(--oa-color-text-primary-on-prussian);filter:blur(0.7px)}')
    # 19.5's chart (the creative director's R2): a title, each line named at its end, the first and last years and a
    # source line, as 19.2's chart has; the words are HTML, so each stays at its size. Invented counts.
    years = list(range(2019, 2027))
    series = (('Comments', (40, 65, 55, 90, 85, 120, 110, 150)), ('Speakers', (20, 25, 22, 30, 28, 35, 34, 40)))
    def ly(v):
        return round(100 - v / 160 * 90 - 5, 1)
    lines = ''.join('<polyline points="' + ' '.join(f'{round(4 + i * 192 / 7, 1)},{ly(v)}' for i, v in enumerate(vals)) + '"/>'
                    for _, vals in series)
    line_css = ('.c19-cht{font:var(--oa-type-ui);margin-bottom:8px}.c19-lc{display:grid;grid-template-columns:200px auto;gap:8px}'
                '.c19-lc svg{display:block}.c19-ends{position:relative;font:var(--oa-type-caption)}'
                '.c19-ends span{position:absolute;left:0;transform:translateY(-50%);white-space:nowrap}'
                '.c19-yr2{display:flex;justify-content:space-between;width:200px;margin-top:4px;font:var(--oa-type-caption);color:var(--sec)}'
                '.c19-src{margin-top:8px;font:var(--oa-type-caption);color:var(--sec)}')
    linebox = ('<div class="c19-box"><p class="c19-cht">Written comments and speakers at the county’s budget hearing, '
               f'{years[0]} to {years[-1]}</p><div class="c19-lc"><svg viewBox="0 0 200 100" width="200" height="100" '
               'aria-hidden="true" focusable="false"><g fill="none" stroke="var(--oa-color-text-primary)" stroke-width="1.5" '
               f'stroke-linejoin="round">{lines}</g></svg><div class="c19-ends">'
               + ''.join(f'<span style="top:{ly(vals[-1])}px">{name}, {vals[-1]}</span>' for name, vals in series)
               + f'</div></div><p class="c19-yr2"><span>{years[0]}</span><span>{years[-1]}</span></p>'
               f'<p class="c19-src">Source: Alder County clerk’s hearing records, {years[0]} to {years[-1]}.</p></div>')
    line_words = (f'titled “Written comments and speakers at the county’s budget hearing, {years[0]} to {years[-1]}”, its two '
                  f'lines rising from {series[0][1][0]} to {series[0][1][-1]} comments and from {series[1][1][0]} to '
                  f'{series[1][1][-1]} speakers, each named with its last count at its end, the years {years[0]} and '
                  f'{years[-1]} under it, and a source line')
    picture('s-19-5-correct', '19.5', linebox + '<div class="c19-row" style="margin-top:8px"><span class="c19-btn">Zoom in</span>'
            '<span class="c19-btn">Zoom out</span><span class="c19-btn">Fit</span></div>',
            f'An Illustrative line chart at 360 px, {line_words}. Under it, three buttons, Zoom in, Zoom out and Fit, each a '
            'single press.', 'Correct: every action is one press of a button. Invented counts.', css=line_css)
    picture('s-19-5-failure', '19.5', linebox + '<p class="c19-k" style="margin-top:8px">Pinch to zoom. Drag to pan. Shake to undo. Press Z to zoom.</p>'
            '<p class="c19-n">Each action needs two fingers, a drag, a shake or one letter key, and has no button.</p>',
            f'Failure case: do not publish. The same Illustrative line chart at 360 px, {line_words}, with the line “Pinch to '
            'zoom. Drag to pan. Shake to undo. Press Z to zoom.” and no buttons.',
            'Picture of a fault: gestures, motion and a single-key shortcut with no button (SC 2.1.4, 2.5.1, 2.5.4, 2.5.7). '
            'Invented counts.', fail=True, css=line_css)
    # 19.6: a 360 px screen zoomed to 200 percent lays out like 180 px; the plate draws that layout at exactly twice
    # its sizes, 360 px wide, and says so (scale 2), so every size divided by 2 is one the type scale holds
    X2 = ('.c19-x2 .c19-ui{padding:32px 32px 40px}.c19-x2 .c19-k{font:var(--oa-type-caption);font-size:1.75rem;margin-bottom:12px}'
          '.c19-x2 .c19-btn{min-height:88px;padding:0 32px;border-width:2px;font:var(--oa-type-ui);font-size:1.875rem;gap:16px}'
          '.c19-x2 .c19-g{display:grid;gap:12px}'
          '.c19-x2 .c19-g2{grid-template-columns:1fr 1fr}.c19-x2 .c19-g2 .c19-btn{padding:0 12px;overflow:hidden;white-space:nowrap}')
    picture('s-19-6-correct', '19.6',
            '<p class="c19-k">360 px, zoomed to 200 percent</p><div class="c19-g">'
            '<span class="c19-btn" style="justify-content:center">Previous page</span>'
            '<span class="c19-btn" style="justify-content:center">Next page</span></div>',
            'A pair of buttons on a 360 px screen zoomed to 200 percent, drawn at twice true size: Previous '
            'page and Next page have stacked into one column, each word whole.',
            'Correct: a row of two buttons that stacks as text grows. The 180 px layout a 360 px screen gives at 200 percent, '
            'drawn at exactly twice its sizes (scale 2).', illus=False, css=X2, root=' c19-x2', scale=2)
    picture('s-19-6-failure', '19.6',
            '<p class="c19-k">360 px, zoomed to 200 percent</p><div class="c19-g c19-g2">'
            '<span class="c19-btn">Previous page</span><span class="c19-btn">Next page</span></div>',
            'Failure case: do not publish. The same buttons on a 360 px screen zoomed to 200 percent, drawn at twice true '
            'size and held side by side; their words may not wrap, so “Previous page” and “Next page” are cut off at the '
            'buttons’ edges.',
            'Picture of a fault: labels that may not wrap (SC 1.4.4, 1.4.12). The 180 px layout a 360 px screen gives at '
            '200 percent, drawn at exactly twice its sizes (scale 2).', fail=True, illus=False, css=X2, root=' c19-x2', scale=2)
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
    meta = json.loads(WCAG.read_text())
    held = present_rules()
    own = {f'19.{i}' for i in range(1, 10)}
    for st, rules, _ in MAP.values():
        if st not in STATUS_WORD:
            raise SystemExit(f'unknown status {st}')
    if set(MAP) != {c['n'] for c in crit}:
        raise SystemExit(f'the map and the criteria differ: {sorted(set(MAP) ^ {c["n"] for c in crit})}')
    if {k for k, v in MAP.items() if v[0] == 'gap'} != set(GAP_OWNERS) or {k for k, v in MAP.items() if v[0] == 'none'} != set(NONE_WHAT):
        raise SystemExit('every gap needs its owing chapters and every criterion not used today its words')
    owers = sorted({c for v in GAP_OWNERS.values() for c in v})
    cid, counts = s_criteria(crit, held, own)
    opener = s_opener(counts, len(crit))
    s_matrix()
    res = load_results()
    s_results(res)
    s_devices()
    pictures()
    n = len(crit)
    newn = sum(c['new'] for c in crit)
    rules = [
        dict(id='19.1', title='Build every page and product to WCAG 2.2 at level AA.',
             rule=[f'WCAG 2.2 sets {n} success criteria at levels A and AA: '
                   f'{sum(c["level"] == "A" for c in crit)} at A and {sum(c["level"] == "AA" for c in crit)} at AA, {w(newn)} of them '
                   'new in 2.2. Build every page and product we publish to meet all of them. The list below gives each criterion in '
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
                    {'label': 'Gaps', 'value': f'{counts["gap"]}, owed by chapters {and_list(owers)}'},
                    {'label': 'Not used today', 'value': f'{counts["none"]}: ' + and_list([NONE_WHAT[k] for k in sorted(NONE_WHAT, key=sort_key)])}],
             related=['18', '20'], builders=['Use W3C’s quick reference, w3.org/WAI/WCAG22/quickref, to filter the criteria '
                                             'by level and topic, and open a criterion’s Understanding page for its examples.']),
        dict(id='19.2', title='Write alt text for what an image does on the page.',
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
             related=['10', '14', '16'],
             builders=['An inline svg beside its word takes <code>aria-hidden="true"</code> and <code>focusable="false"</code>, and an '
                       'img beside its word takes <code>alt=""</code>. A chart that stands alone takes its finding as its alt, or '
                       '<code>role="img"</code> with an <code>aria-label</code> where it is an svg, and its table or its lines in words '
                       'sit beside it.']),
        dict(id='19.3', title='Name a control or a step by its words.',
             rule=['An instruction names the control it means by the words on it: “press Send your comment”. Color, shape '
                   'and place can follow the words, as in “Send your comment, under the form”, since a phone moves things, and '
                   'a screen reader or a contrast theme loses color.'],
             tokens=[], why={'text': ['A reader who cannot see color, or who meets the buttons in another order on a phone, '
                                      'can still follow words that match the control’s name.'],
                             'basis': 'WCAG 2.2 SC 1.3.3 and 1.4.1'},
             correct={'specimen': 's-19-3-correct', 'caption': 'The instruction names Send your comment by its words.'},
             failure={'specimen': 's-19-3-failure', 'caption': '<strong>Fails Rule 19.3.</strong> “The dark button on the '
                                                               'right” gives only color and place.'},
             specs=[{'label': 'Say', 'value': 'The control’s own words, as its name starts (Rule 18.1)'},
                    {'label': 'May add', 'value': 'Where it is, after its words'},
                    {'label': 'Never alone', 'value': 'Color, shape, size, sound or place'}],
             related=['02', '18'],
             builders=['Copy the control’s words into the instruction exactly as the control shows them, as in “Press Send '
                       'your comment”, so a reader using voice control can say the words they read.']),
        dict(id='19.4', title='Set every word as live text except the logo.',
             rule=['Headlines, quotes, labels and chart words are live text in the page. A social card or a slide that '
                   'must be an image carries its words again in the post or the page beside it. The wordmark and its lockups are '
                   'the only pictures of text a page holds.'],
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
             related=['03', '22', '23'],
             builders=['Set a headline that sits over a photograph as HTML text layered on the image, so the image file holds '
                       'no words. A social card that must be one image repeats its words in the post and in its alt text.']),
        dict(id='19.5', title='Let every action work with one tap, one click or one key press.',
             rule=['Every action has a control a reader can press once: Zoom in and Zoom out as buttons, a drawing moved '
                   'with buttons or arrow keys, and Undo as a button. A gesture with two fingers, a drag, a tilt or a shake '
                   'may add a second way beside that control. Where a product answers a tilt or a shake, a setting lets the reader '
                   'turn that response off, so moving the device by accident changes nothing. No product uses a shortcut of one '
                   'letter key, and an action runs when the press ends, so sliding off a control cancels it.'],
             tokens=['oa.size.target.touch'],
             why={'text': ['A reader with a tremor, one hand, a head pointer or voice control can press a button where a '
                           'pinch or a drag fails, and a single-letter shortcut fires by accident for a reader who talks to '
                           'the computer.'],
                  'basis': 'WCAG 2.2 SC 2.1.4, 2.5.1, 2.5.2, 2.5.4 and 2.5.7'},
             correct={'specimen': 's-19-5-correct', 'caption': 'Zoom in, Zoom out and Fit as buttons under the chart.'},
             failure={'specimen': 's-19-5-failure', 'caption': '<strong>Fails Rule 19.5.</strong> Pinch, drag, shake and the '
                                                               'Z key are the only ways to act.'},
             specs=[{'label': 'Each action', 'value': 'A control pressed once, at least 44 px (Rule 11.7)', 'token': 'oa.size.target.touch'},
                    {'label': 'Gestures and motion', 'value': 'Only beside a button that does the same; a setting turns off the '
                                                              'response to a tilt or a shake'},
                    {'label': 'Shortcuts', 'value': 'None of one letter; a shortcut takes a modifier key, such as Control'},
                    {'label': 'When it runs', 'value': 'On release, as native buttons do'}],
             related=['18', '15'],
             builders=['Run an action on the <code>click</code> event, which fires when the press ends, and never on '
                       '<code>pointerdown</code> or <code>touchstart</code>. Give a drag or a pinch a button that does the same, and '
                       'give every keyboard shortcut a modifier key, as in Control and K.']),
        dict(id='19.6', title='Keep every word and control when text grows, spacing opens or the screen turns.',
             rule=['A page keeps every word and control when the reader doubles the text size, widens the spacing between '
                   'lines, words and letters, or turns the phone on its side. Labels wrap where they would overflow, a row '
                   'of two buttons stacks, and no page locks itself to one orientation. Reflow at 320 px is Rule 07.6.'],
             tokens=[], why={'text': ['Many readers raise the text size or the spacing to read at all, and some hold a phone '
                                      'one way only. A label that may not wrap is how this guide’s own pages lost words when we first tested '
                                      'them at 200 percent.'],
                             'basis': 'WCAG 2.2 SC 1.3.4, 1.4.4, 1.4.10 and 1.4.12'},
             correct={'specimen': 's-19-6-correct', 'caption': 'Zoomed to 200 percent, the two buttons stack, and each word '
                                                               'stays whole.'},
             failure={'specimen': 's-19-6-failure', 'caption': '<strong>Fails Rule 19.6.</strong> The words may not wrap, so '
                                                               'both are cut off.'},
             specs=[{'label': 'Text size', 'value': '200 percent with nothing cut off or overlapping'},
                    {'label': 'Spacing', 'value': 'Line height 1.5, paragraph spacing 2 times the size, letter spacing 0.12 '
                                                  'and word spacing 0.16 times the size, all at once, with nothing lost'},
                    {'label': 'Width', 'value': '320 px with no sideways scroll outside a scroll region (Rule 07.6)'},
                    {'label': 'Orientation', 'value': 'Both, with no lock'},
                    {'label': 'Never', 'value': '<code>white-space: nowrap</code> on a label, or a fixed height on a box of words'}],
             related=['07', '06', '18'],
             builders=['Size type in rem, let a box of words take its height from them, and let words wrap with '
                       '<code>overflow-wrap: break-word</code>. Leave the orientation out of the web app manifest, and never call '
                       '<code>screen.orientation.lock()</code>.']),
        dict(id='19.7', title='Check every page against the verification matrix.',
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
                    {'label': 'Automated rules', 'value': 'axe-core with the tags wcag2a, wcag2aa, wcag21a, wcag21aa and wcag22aa; '
                                                          'axe-core has no wcag22a tag'},
                    {'label': 'Keyboard paths', 'value': 'Each component’s path, walked in the light and dark themes (chapter 18)'},
                    {'label': 'Emulated settings', 'value': 'Reduced motion, forced colors light and dark, the device set to dark'},
                    {'label': 'By a person', 'value': 'The keyboard order and ring, the reading order, and the device script (Rule 19.9)'}],
             related=['18', '26'],
             builders=['Run the checks a tool can run with the commands in the matrix, on every page and in each theme, and log the '
                       'tool’s version with each result. The rest need a person: the Tab order and the focus ring, the reading '
                       'order, words broken in the middle, and the device script.']),
        dict(id='19.8', title='Report each result with its date and build.',
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
             related=['18'],
             builders=['Keep the results in a dated file that names the build, the tool and its version, and print the page’s '
                       'results from that file, so the page and the file never disagree.']),
        dict(id='19.9', title='Before launch, run the device script on real devices.',
             rule=['Four short scripts check what no automated test can: a real screen reader on each of four common platforms, '
                   'and a Windows contrast theme. Each step says what to press, and the ten things to listen for say what a '
                   'pass sounds like, so anyone can run them with no training.'],
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
             related=['18'],
             builders=['Run each script on the device’s current system and in the browser the script names, and write both '
                       'versions down with the results, as the script asks at its end.']),
    ]
    for r in rules:
        r.setdefault('related', [])
        r.setdefault('builders', [])
    ch = {
        'number': CH, 'anchor': 'accessibility', 'title': 'Accessibility', 'part': 'Behavior',
        'instruction': 'Check a page against WCAG 2.2 AA before you call it finished.',
        'opener': opener,
        'intro': [f'Accessibility means a person can use a page with a keyboard, a screen reader, zoom, voice or touch, and '
                  f'with less motion. The standard is WCAG 2.2, the Web Content Accessibility Guidelines from the World Wide Web '
                  f'Consortium, W3C, which writes many of the web’s standards. Each of its success criteria is one requirement a page '
                  f'can be tested against. Level A holds the most basic ones, and level AA adds more, such as the contrast of '
                  f'text. This chapter holds the {n} criteria at levels A and AA, each in W3C’s words with the rule in this guide that '
                  'meets it, then the checks that prove a page meets them.',
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
            f'Source: W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024, '
            f'w3.org/TR/WCAG22, retrieved {meta["read"]}. Each criterion’s words in Rule 19.1, quoted as the '
            'Recommendation prints them and in its order; its notes are informative and sit on W3C’s Understanding pages, '
            'w3.org/WAI/WCAG22/Understanding.',
            'Source: W3C Web Accessibility Initiative, “Understanding Success Criterion 4.1.1: Parsing (Obsolete and removed)”, '
            'w3.org/WAI/WCAG22/Understanding/parsing.html, no page date, retrieved November 11, 2026. Behind the line on '
            '4.1.1 under Rule 19.1’s list.',
            'Source: W3C Web Accessibility Initiative, “How to Meet WCAG 2.2 (Quick Reference)”, w3.org/WAI/WCAG22/quickref, '
            'no page date, retrieved November 10, 2026.',
            'Source: Deque Systems, axe-core’s command line, the package @axe-core/cli 4.14.0 on npmjs.com, published October '
            '15, 2026, retrieved November 11, 2026. Its <code>--tags</code>, <code>--rules</code> and <code>--exit</code> '
            'options are behind the commands in Rule 19.7’s matrix.',
            'Further reading for Rule 19.9, each maker’s own guide, each retrieved November 11, 2026: Apple, “Turn on and '
            'practice VoiceOver on iPhone”, support.apple.com/guide/iphone/turn-on-and-practice-voiceover-iph3e2e415f/ios; '
            'Apple, “VoiceOver User Guide for Mac”, support.apple.com/guide/voiceover/welcome/mac; Google, “Get started on '
            'Android with TalkBack”, support.google.com/accessibility/android/answer/6283677; NV Access, “NVDA 2026.3.1 User '
            'Guide”, download.nvaccess.org/documentation/userGuide.html; Microsoft, “Change color contrast in Windows”, '
            'support.microsoft.com/en-us/accessibility/windows/change-color-contrast-in-windows. We wrote the steps from '
            'these makers’ menus as we know them and did not check them on a device; makers rename menus between versions.'],
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
    used = {r['correct']['specimen'] for r in ch['rules']} | {r['failure']['specimen'] for r in ch['rules']} | {ch['opener']}
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
    ap.add_argument('--read-wcag', metavar='HTML', help='a copy of https://www.w3.org/TR/WCAG22/ to store the criteria from')
    ap.add_argument('--read-on', metavar='DATE', help='the date the copy was fetched, in words, such as "November 11, 2026"')
    a = ap.parse_args()
    if a.read_wcag:
        if not a.read_on:
            raise SystemExit('--read-wcag needs --read-on, the date the copy was fetched')
        read_wcag(a.read_wcag, a.read_on)
        return
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
