"""Check every V7 item an atlas concept page draws against the model export (D2-50).

Usage:
    python3 -I work/build/scripts/phase-2/atlas_concepts_verify.py <concept.html>
    python3 -I work/build/scripts/phase-2/atlas_concepts_verify.py --selftest <concept.html>

Reads the data attributes set out in brief section 8:
  data-node (+ data-name, the exact printed label), data-link (+ data-sign, data-grade, data-delay, data-from,
  data-to), data-loop (+ data-steps), data-reform (+ data-targets), data-count (+ the number as text),
  data-strip="loops" (must hold all 23 loops).
Also requires the like-for-like subjects (DR-13): R10 with its four steps, and area C's five variables when the
page has an area-c view. Fails on any em dash in the page text (CLAUDE.md writing rules).
--selftest plants six errors in a copy of the page and confirms the verifier catches each one.
Writes <page stem>-Verify-Results.json beside the page. Exit code 1 on any failure.
"""
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[4]
MODEL = json.loads((ROOT / 'work/boards/phase-2/maps/20261028_Maps-Model-Data.json').read_text())
NODES, LINKS, LOOPS, REFORMS = MODEL['nodes'], MODEL['links'], MODEL['loops'], MODEL['reforms']
AREA_OF = {k: v['area'] for k, v in NODES.items()}
for a in MODEL['areas']:
    for n in a['nodes']:
        AREA_OF[n] = a['id']


def counts():
    c = dict(MODEL['generated']['counts'])
    cross = [l for l in LINKS.values() if AREA_OF[l['from']] != AREA_OF[l['to']]]
    c.update({
        'loops_reinforcing': sum(1 for l in LOOPS.values() if l['type'] == 'R'),
        'loops_balancing': sum(1 for l in LOOPS.values() if l['type'] == 'B'),
        'loops_sketched': sum(1 for l in LOOPS.values() if l['conceptual']),
        'connections_cross_area': len(cross),
        'connections_within_area': len(LINKS) - len(cross),
        'areas': len(MODEL['areas']),
        'authority_connections': sum(1 for l in LINKS.values() if l['type'] == 'authority'),
    })
    for a in MODEL['areas']:
        c[f'variables_{a["id"]}'] = len(a['nodes'])
    for g in MODEL['groups']:
        c[f'loops_{g["id"]}'] = len(g['loops'])
    return c


COUNTS = counts()


class Collect(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items, self.stack, self.text, self.skip = [], [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        rec = {'tag': tag, 'attrs': a, 'text': [], 'children_loops': []}
        if tag in ('script', 'style'):
            self.skip += 1
        if tag in self.VOID:
            if any(k in a for k in ('data-node', 'data-link', 'data-loop', 'data-reform')):
                self.items.append(rec)
            return
        self.stack.append(rec)
        if any(k in a for k in ('data-node', 'data-link', 'data-loop', 'data-reform', 'data-count', 'data-strip', 'data-name')):
            self.items.append(rec)
        if 'data-loop' in a:
            for r in self.stack[:-1]:
                if r['attrs'].get('data-strip') == 'loops':
                    r['children_loops'].append(a['data-loop'])

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        rec = {'tag': tag, 'attrs': a, 'text': [], 'children_loops': []}
        if any(k in a for k in ('data-node', 'data-link', 'data-loop', 'data-reform')):
            self.items.append(rec)
        if 'data-loop' in a:
            for r in self.stack:
                if r['attrs'].get('data-strip') == 'loops':
                    r['children_loops'].append(a['data-loop'])

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.skip:
            return
        self.text.append(data)
        for r in self.stack:
            r['text'].append(data)


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def verify(html):
    p = Collect()
    p.feed(html)
    errs, seen = [], {'node': set(), 'link': set(), 'loop': set(), 'reform': set()}
    stats = {'nodes': 0, 'links': 0, 'loops': 0, 'reforms': 0, 'names': 0, 'counts': 0, 'strips': 0}
    for it in p.items:
        a, text = it['attrs'], norm(' '.join(it['text']))
        if 'data-node' in a:
            v = a['data-node']
            if v not in NODES:
                errs.append(f'unknown variable {v}')
            else:
                seen['node'].add(v); stats['nodes'] += 1
        if 'data-name' in a:
            stats['names'] += 1
            v = a.get('data-node') or a.get('data-loop') or a.get('data-reform') or a.get('data-link')
            name = a['data-name']
            ok = set()
            if v in NODES:
                n = NODES[v]; ok = {n['label'], n['title']} | ({n['short']} if n.get('short') else set())
            elif v in LOOPS:
                ok = {LOOPS[v]['title']}
            elif v in REFORMS:
                ok = {REFORMS[v]['title']}
            elif v in LINKS:
                ok = {LINKS[v]['name']}
            if name not in ok:
                errs.append(f'{v}: data-name "{name}" is not a V7 name ({sorted(ok)})')
            if text and name not in text:
                errs.append(f'{v}: printed text "{text[:60]}" does not carry its data-name "{name}"')
        if 'data-link' in a:
            k = a['data-link']
            if k not in LINKS:
                errs.append(f'unknown connection {k}')
            else:
                L = LINKS[k]; seen['link'].add(k); stats['links'] += 1
                want_sign = L['polarity'] if L['polarity'] in ('+', '-') else 'none'
                if 'data-sign' in a and a['data-sign'] != want_sign:
                    errs.append(f'{k}: sign {a["data-sign"]} should be {want_sign}')
                if 'data-sign' not in a:
                    errs.append(f'{k}: no data-sign')
                if a.get('data-grade', L['evidence']) != L['evidence']:
                    errs.append(f'{k}: grade {a["data-grade"]} should be {L["evidence"]}')
                if 'data-grade' not in a:
                    errs.append(f'{k}: no data-grade')
                if 'data-delay' in a and a['data-delay'] != L['delay']:
                    errs.append(f'{k}: delay {a["data-delay"]} should be {L["delay"]}')
                for end in ('from', 'to'):
                    if f'data-{end}' in a and a[f'data-{end}'] != L[end]:
                        errs.append(f'{k}: {end} {a["data-" + end]} should be {L[end]}')
        if 'data-loop' in a:
            k = a['data-loop']
            if k not in LOOPS:
                errs.append(f'unknown loop {k}')
            else:
                seen['loop'].add(k); stats['loops'] += 1
                if 'data-steps' in a:
                    # the three sketched loops (B2, B3, R9) have no numbered chain and carry data-steps="sketch"
                    want = 'sketch' if LOOPS[k]['conceptual'] else ' '.join(s['id'] for s in LOOPS[k]['steps'])
                    if ' '.join(a['data-steps'].split()) != want:
                        errs.append(f'{k}: steps "{a["data-steps"]}" should be "{want}"')
        if 'data-reform' in a:
            k = a['data-reform']
            if k not in REFORMS:
                errs.append(f'unknown reform {k}')
            else:
                seen['reform'].add(k); stats['reforms'] += 1
                if 'data-targets' in a and sorted(a['data-targets'].split()) != sorted(REFORMS[k]['targets']):
                    errs.append(f'{k}: targets "{a["data-targets"]}" should be {REFORMS[k]["targets"]}')
        if 'data-count' in a:
            key = a['data-count']; stats['counts'] += 1
            num = re.sub(r'[^0-9]', '', text)
            if key.startswith('custom:'):
                pass
            elif key not in COUNTS:
                errs.append(f'unknown count key {key}')
            elif not num or int(num) != COUNTS[key]:
                errs.append(f'count {key}: printed "{text}" should be {COUNTS[key]}')
        if a.get('data-strip') == 'loops':
            stats['strips'] += 1
            missing = sorted(set(LOOPS) - set(it['children_loops']))
            if missing:
                errs.append(f'loop strip is missing {missing}')
    # like-for-like subjects (DR-13)
    if 'R10' not in seen['loop']:
        errs.append('R10 is not drawn (DR-13)')
    for k in ('L08', 'L25', 'L53', 'L42'):
        if k not in seen['link']:
            errs.append(f'R10 step {k} is not drawn with data-link (DR-13)')
    views = re.search(r'<meta\s+name="atlas-views"\s+content="([^"]+)"', html)
    if views and 'area-c' in views.group(1).split():
        for v in ('C1', 'C2', 'C3', 'C4', 'C5'):
            if v not in seen['node']:
                errs.append(f'area C view: {v} is not drawn (DR-13)')
    if stats['strips'] == 0:
        errs.append('no data-strip="loops" element (DR-12: a strip of all 23 loops)')
    body = re.sub(r'<(script|style)\b.*?</\1>', '', html, flags=re.S | re.I)
    if '—' in body or '&mdash;' in body:
        errs.append('em dash in the page text (CLAUDE.md writing rules)')
    return errs, stats, {k: len(v) for k, v in seen.items()}


def selftest(html):
    """Plant one error of each kind and confirm each is caught."""
    plants = []
    plants.append(('flip a minus sign', html.replace('data-sign="-"', 'data-sign="+"', 1)))
    plants.append(('L53 grade to documented', re.sub(r'(data-link="L53"[^>]*?data-grade=")plausible"', r'\1documented"', html, count=1)))
    first_name = re.search(r'data-name="([^"]+)"', html)
    plants.append(('rename a label', html.replace(f'data-name="{first_name.group(1)}"', 'data-name="Housing supply"', 1) if first_name else None))
    plants.append(('drop R8 from the strip', re.sub(r'data-loop="R8"', 'data-loop="R8x"', html, count=1)))
    plants.append(('reorder R10 steps', html.replace('data-steps="L08 L25 L53 L42"', 'data-steps="L25 L08 L53 L42"', 1)))
    plants.append(('em dash', html.replace('</body>', '<p>A — B</p></body>', 1)))
    base = len(verify(html)[0])
    out = []
    for name, h in plants:
        if h is None or h == html:
            out.append((name, 'not planted (pattern absent)'))
            continue
        out.append((name, 'caught' if len(verify(h)[0]) > base else 'MISSED'))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    page = pathlib.Path(args[0]).resolve()
    html = page.read_text()
    errs, stats, seen = verify(html)
    res = {'file': str(page.relative_to(ROOT)) if page.is_relative_to(ROOT) else str(page), 'model': 'work/boards/phase-2/maps/20261028_Maps-Model-Data.json',
           'items_checked': stats, 'distinct_ids': seen, 'errors': errs, 'pass': not errs}
    if '--selftest' in sys.argv:
        res['selftest'] = selftest(html)
    out = page.with_name(page.stem + '-Verify-Results.json')
    out.write_text(json.dumps(res, indent=1))
    print(('PASS' if not errs else 'FAIL'), res['file'], stats, seen)
    for e in errs[:40]:
        print('  -', e)
    if '--selftest' in sys.argv:
        for name, r in res['selftest']:
            print(f'  selftest {name}: {r}')
    sys.exit(0 if not errs else 1)


if __name__ == '__main__':
    main()
