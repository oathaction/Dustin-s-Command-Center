"""Check every chart specimen on a data visualization concept page against the shared chart dataset.

Usage:
    python3 -I work/build/scripts/phase-2/dataviz_verify.py <concept.html>
    python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest <concept.html>

Contract (data viz brief, section 6):
  <figure data-spec="S03" data-dataset="rule-changes-by-instrument" data-evidence="Finding"> holds, by data-role,
  an evidence-label, a title, a measure line, a source line and an equivalent (a table or full text). Marks carry
  data-key (the dataset row key) and data-value (number) or data-category (string), with data-field naming the
  column when it is not "value", and data-mark (bar, point, unit, cell, vertex, label).
Checks: every specimen S01 to S10 is present with its dataset and evidence kind; every role present and not empty;
the evidence label names the kind; the source line carries the dataset's source words; every mark's key exists and
its value or category matches the dataset; required keys are all drawn; unit charts draw each row once and each
category's count exactly; no em dash anywhere in the page text; no hyphen used as a minus sign before a figure.
--selftest plants seven errors in copies of the page and confirms each one is caught.
Writes <page stem>-Verify-Results.json beside the page. Exit code 1 on any failure.
"""
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATA = json.loads((ROOT / 'work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json').read_text())
DS = DATA['datasets']
SPECS = {s['id']: s for s in DATA['specimens']}
ROLES = ['evidence-label', 'title', 'measure', 'source', 'equivalent']
KINDS = {'Finding', 'Association', 'Estimate', 'Illustration'}


class Collect(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.figs, self.stack, self.text, self.skip, self.cur = [], [], [], 0, []

    def _rec(self, tag, a):
        return {'tag': tag, 'attrs': a, 'text': []}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'):
            self.skip += 1
        rec = self._rec(tag, a)
        if tag == 'figure' and 'data-spec' in a:
            fig = {'attrs': a, 'roles': {}, 'marks': [], 'text': []}
            self.figs.append(fig)
            self.cur.append(fig)
            rec['fig'] = fig
        if self.cur:
            f = self.cur[-1]
            if 'data-role' in a:
                f['roles'].setdefault(a['data-role'], []).append(rec)
            if 'data-key' in a:
                f['marks'].append(rec)
        if tag in self.VOID:
            return
        self.stack.append(rec)

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        if self.cur and 'data-key' in a:
            self.cur[-1]['marks'].append(self._rec(tag, a))

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                for r in self.stack[i:]:
                    if 'fig' in r and self.cur and self.cur[-1] is r['fig']:
                        self.cur.pop()
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.skip:
            return
        self.text.append(data)
        for r in self.stack:
            r['text'].append(data)
        for f in self.cur:
            f['text'].append(data)


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def num(x):
    try:
        return float(str(x).replace('−', '-').replace(',', ''))
    except ValueError:
        return None


def row_index(ds):
    idx = {}
    for r in ds.get('rows', []):
        k = r.get('key')
        if k is None and ds.get('key_fields'):
            k = '|'.join(str(r[f]) for f in ds['key_fields'])
        if k is not None:
            idx[str(k)] = r
    return idx


def verify(html):
    p = Collect()
    p.feed(html)
    errs, stats = [], {'figures': len(p.figs), 'marks': 0, 'values': 0, 'categories': 0, 'units': 0}
    seen_specs = set()
    for fig in p.figs:
        a = fig['attrs']
        sid, did, kind = a.get('data-spec'), a.get('data-dataset'), a.get('data-evidence')
        tag = f'{sid}'
        if sid not in SPECS:
            errs.append(f'{tag}: unknown specimen id')
            continue
        seen_specs.add(sid)
        spec = SPECS[sid]
        if did != spec['dataset']:
            errs.append(f'{tag}: data-dataset "{did}" should be "{spec["dataset"]}"')
            continue
        ds = DS[did]
        if ds.get('pending'):
            errs.append(f'{tag}: dataset {did} is still pending in the shared data')
            continue
        if kind not in KINDS:
            errs.append(f'{tag}: data-evidence "{kind}" is not a section 15 kind')
        elif kind != ds.get('evidence'):
            errs.append(f'{tag}: evidence kind "{kind}" differs from the shared dataset ("{ds.get("evidence")}")')
        for role in ROLES:
            recs = fig['roles'].get(role)
            if not recs or not any(norm(' '.join(r['text'])) for r in recs):
                errs.append(f'{tag}: missing or empty data-role="{role}"')
        lab = ' '.join(norm(' '.join(r['text'])) for r in fig['roles'].get('evidence-label', []))
        if kind and kind not in lab:
            errs.append(f'{tag}: evidence label "{lab[:40]}" does not name "{kind}"')
        srcline = ' '.join(norm(' '.join(r['text'])) for r in fig['roles'].get('source', []))
        for tok in ds.get('source_tokens', []):
            if tok not in srcline:
                errs.append(f'{tag}: source line lacks "{tok}"')
        if ds.get('kind') == 'illustrative' and 'Illustrative data' not in norm(' '.join(fig['text'])):
            errs.append(f'{tag}: illustrative data without an "Illustrative data" label')
        idx = row_index(ds)
        drawn = set()
        unit_count, unit_keys = {}, []
        for m in fig['marks']:
            ma = m['attrs']
            k = ma['data-key']
            stats['marks'] += 1
            if k not in idx:
                errs.append(f'{tag}: mark key "{k}" is not a row of {did}')
                continue
            row = idx[k]
            field = ma.get('data-field', 'value')
            if ma.get('data-mark') not in (None, 'label'):
                drawn.add(k)
            if 'data-value' in ma:
                stats['values'] += 1
                want, got = num(row.get(field)), num(ma['data-value'])
                if want is None or got is None:
                    errs.append(f'{tag}: {k}.{field}: value "{ma["data-value"]}" cannot be compared with "{row.get(field)}"')
                elif abs(want - got) > max(0.051, abs(want) * 0.005):
                    errs.append(f'{tag}: {k}.{field} drawn as {got}, data says {want}')
            if 'data-category' in ma:
                stats['categories'] += 1
                cf = ma.get('data-field', 'direction' if did == 'rule-changes' else 'category')
                if str(row.get(cf)) != ma['data-category']:
                    errs.append(f'{tag}: {k}.{cf} drawn as "{ma["data-category"]}", data says "{row.get(cf)}"')
            if ma.get('data-mark') == 'unit':
                stats['units'] += 1
                unit_keys.append(k)
                c = ma.get('data-category', row.get('direction'))
                unit_count[c] = unit_count.get(c, 0) + 1
        missing = [k for k in ds.get('required_keys', []) if k not in drawn]
        if missing:
            errs.append(f'{tag}: {len(missing)} required rows not drawn ({", ".join(missing[:6])})')
        if unit_keys:
            dup = sorted({k for k in unit_keys if unit_keys.count(k) > 1})
            if dup:
                errs.append(f'{tag}: unit marks repeat rows {dup[:6]}')
            if did == 'rule-changes':
                for c, n in ds['counts'].items():
                    if unit_count.get(c, 0) != n:
                        errs.append(f'{tag}: unit chart draws {unit_count.get(c, 0)} "{c}", data has {n}')
        # hyphen-minus used as a minus sign before a figure, inside the specimen's own text
        ftxt = norm(' '.join(fig['text']))
        for mm in re.finditer(r'(?:(?<=\s)|(?<=\())-\d', ftxt):
            errs.append(f'{tag}: hyphen used as a minus sign near "{ftxt[max(0, mm.start() - 15):mm.end() + 10]}"')
            break
    for sid in SPECS:
        if sid not in seen_specs:
            errs.append(f'{sid}: specimen not on the page')
    page = ' '.join(p.text)
    if '—' in page:
        i = page.index('—')
        errs.append(f'em dash in page text near "{norm(page[max(0, i - 30):i + 10])}"')
    return errs, stats


def selftest(html):
    figs = re.findall(r'<figure[^>]*data-spec="S\d\d"', html)
    plants = []
    m = re.search(r'data-value="([0-9.]+)"', html)
    if m:
        v = float(m.group(1))
        plants.append(('changed value', html[:m.start()] + f'data-value="{v * 1.1 + 1:.2f}"' + html[m.end():]))
    m = re.search(r'data-role="source"', html)
    if m:
        plants.append(('source line removed', html[:m.start()] + 'data-role="sourcex"' + html[m.end():]))
    plants.append(('em dash', html.replace('</figure>', '<p>planted — dash</p></figure>', 1)))
    m = re.search(r'(<[^>]*data-role="evidence-label"[^>]*>)([^<]*)', html)
    if m:
        plants.append(('evidence label', html[:m.start(2)] + 'Mystery' + html[m.end(2):]))
    m = re.search(r'<(rect|circle|path|use|g)[^>]*data-mark="unit"[^>]*/>', html)
    if m:
        plants.append(('unit removed', html[:m.start()] + html[m.end():]))
    m = re.search(r'data-category="toward voters"', html)
    if m:
        plants.append(('category changed', html[:m.start()] + 'data-category="away from voters"' + html[m.end():]))
    plants.append(('specimen removed', html.replace('data-spec="S10"', 'data-spec-x="S10"')))
    out = []
    for name, h in plants:
        e, _ = verify(h)
        out.append({'plant': name, 'caught': bool(e), 'first_error': e[0] if e else None})
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        sys.exit(2)
    path = pathlib.Path(args[0]).resolve()
    html = path.read_text(encoding='utf-8')
    errs, stats = verify(html)
    rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    res = {'file': rel, 'pass': not errs, 'errors': errs[:200], 'error_count': len(errs), 'stats': stats}
    if '--selftest' in sys.argv:
        st = selftest(html)
        res['selftest'] = st
        res['selftest_pass'] = all(x['caught'] for x in st) and len(st) >= 6
    out = path.with_name(path.stem + '-Verify-Results.json')
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False))
    print(f"{'PASS' if res['pass'] else 'FAIL'} {res['file']}: {stats['figures']} figures, {stats['marks']} marks "
          f"({stats['values']} values, {stats['categories']} categories, {stats['units']} units), {len(errs)} errors")
    for e in errs[:40]:
        print('  - ' + e)
    if 'selftest' in res:
        print(f"  selftest: {sum(x['caught'] for x in res['selftest'])} of {len(res['selftest'])} planted errors caught")
        for x in res['selftest']:
            if not x['caught']:
                print(f"    missed: {x['plant']}")
    sys.exit(0 if res['pass'] and res.get('selftest_pass', True) else 1)


if __name__ == '__main__':
    main()
