"""research_atlas_recheck_full.py: Phase 0's 2,644 atlas comparisons rerun from the three supplied pages against today's
Atlas V7, as data only (DR-258, board 2, research lead, November 13, 2026). It completes research_atlas_recheck.py
(round 3, D3-1094), which could rerun 1,976 of them from Phase 0's stored data.

Run:
  python3 -I work/build/scripts/phase-3/research_atlas_recheck_full.py <upload dir> <scratch dir> [--write]
  e.g. <upload dir> = /root/.claude/uploads/4af740fe-eb77-5222-8bcc-cd714f9f6532 (this session's upload folder)
       <scratch dir> = an empty folder outside the repository; the split pages and the two run outputs go there

Reads, never writes:
  the three supplied pages, in place in <upload dir>, each checked against the October 20 source manifest first:
    ef88da19-20261018_Oath-And-Action-Brand-Guide_V5-Polished.html          4,285,909 bytes, SHA-256 f4fff9cc...09c8d2
    25399b55-20261018_Oath-And-Action-Atlas-Visual-System.html              3,014,874 bytes, SHA-256 22a150ce...7699d2
    afdfd03c-20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html         1,568,049 bytes, SHA-256 56980de8...548490
  the Atlas V7 model, work/extract/atlas-v7-data.json, checked equal to work/research/atlas-v7-docs/20261015_Atlas-V7-Model.json
  Phase 0's code and data: work/build/scripts/extract_sources.py, work/build/scripts/phase-0/atlas_reconcile_extract.py,
    work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json
Writes:
  always, in <scratch dir> only: extract/ (the two split pages), reconcile-clean.json and reconcile-tally.json
  with --write, in the repository only: work/research/20261113_Atlas-Recheck-Full-Data.json and -Full-Table.md
  (a file whose text is unchanged is left alone). Phase 0's files, source/ and the atlas are never touched.

Steps:
1. Checks each supplied page against the source manifest (size and SHA-256) and today's model against the committed one.
2. Splits V5 Polished and the Atlas Visual System in <scratch dir>/extract with Phase 0's own code (extract_sources.py's
   extract_html, as Phase 0 ran it). Concepts V2 is read in place, as Phase 0 did.
3. Runs Phase 0's reconciliation script twice in <scratch dir>, changing only where it reads and writes: once clean, once
   with per-source tallies beside five of its counters. Both outputs must be equal; each is compared with Phase 0's data
   file field by field and byte for byte.
4. Counts the 17 comparison families with Phase 0's own formula (build_reconciliation_table.py, lines 190 to 215), on
   Phase 0's data and today's, and splits each by the page its side came from.
5. Reads the Circuit's 13 drawn bundle counts by position (Phase 0 counted them; its script has no code for them).
Folded in from the scratch steps full_extract.py and full_reconcile.py, which it replaces.
"""
import collections
import hashlib
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
if len(ARGS) != 2:
    sys.exit(__doc__)
UP, WORK = (os.path.abspath(a) for a in ARGS)
WRITE = '--write' in sys.argv
assert not WORK.startswith(ROOT + os.sep), 'the scratch dir must be outside the repository'
os.makedirs(WORK, exist_ok=True)
XS = os.path.join(WORK, 'extract')
P0_DATA = os.path.join(ROOT, 'work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json')
P0_SCRIPT = os.path.join(ROOT, 'work/build/scripts/phase-0/atlas_reconcile_extract.py')
V7P = os.path.join(ROOT, 'work/extract/atlas-v7-data.json')
V7M = os.path.join(ROOT, 'work/research/atlas-v7-docs/20261015_Atlas-V7-Model.json')
OUT_JSON = os.path.join(ROOT, 'work/research/20261113_Atlas-Recheck-Full-Data.json')
OUT_MD = os.path.join(ROOT, 'work/research/20261113_Atlas-Recheck-Full-Table.md')
PAGES = {  # group: (upload name, the name Phase 0 read, size, SHA-256 in the source manifest)
    'V5 Polished': ('ef88da19-20261018_Oath-And-Action-Brand-Guide_V5-Polished.html', '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html',
                    4285909, 'f4fff9cc0e36b7cc9e346ae1406d1e3b6b30ef44526f181a002b35da2c09c8d2'),
    'Atlas Visual System': ('25399b55-20261018_Oath-And-Action-Atlas-Visual-System.html', '20261018_Oath-And-Action-Atlas-Visual-System.html',
                            3014874, '22a150ce0a76a8dff5687762cdb2168aa73b530d1a2207f0323c5e06447699d2'),
    'Concepts V2': ('afdfd03c-20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html', '20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html',
                    1568049, '56980de8ca29f9016d749ac79071a16110333ab49bbf86696d96efcfac548490'),
}
MODEL_SHA = 'ef1028ac87e402e30af9e3cda234fed63794b5570d0a165b9dab39073e08c7f2'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# 1. inputs
inputs = {}
for grp, (up, name, size, digest) in PAGES.items():
    p = os.path.join(UP, up)
    got = sha(p)
    assert os.path.getsize(p) == size and got == digest, grp
    inputs[grp] = {'file_read': name, 'read_in_place_from': 'the session upload folder', 'bytes': size, 'sha256': got, 'equals_source_manifest': True}
assert sha(V7P) == sha(V7M) == MODEL_SHA
CV2 = os.path.join(UP, PAGES['Concepts V2'][0])

# 2. split with Phase 0's own code
sys_argv = sys.argv
sys.argv = [sys_argv[0], ROOT]
spec = importlib.util.spec_from_file_location('extract_sources', os.path.join(ROOT, 'work/build/scripts/extract_sources.py'))
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)
sys.argv = sys_argv
ex.SRC, ex.OUT = UP, XS
for slug, grp in (('v5-polished', 'V5 Polished'), ('atlas-visual-system', 'Atlas Visual System')):
    inv = ex.extract_html(PAGES[grp][0], slug, True)
    inputs[grp]['split'] = {'sections': len(inv['sections']), 'embedded_files': len(inv['data_uris'])}


# 3. Phase 0's reconciliation, run as written but for where it reads and writes
def phase0(out, tally):
    src = open(P0_SCRIPT, encoding='utf-8').read()
    patch = [
        ('CV2_SRC = os.path.join(ROOT, "source", "20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html")', f'CV2_SRC = {CV2!r}'),
        ('OUT = os.path.join(ROOT, "work", "handoffs", "phase-0", "20261020_Atlas-Reconciliation-Data.json")', f'OUT = {out!r}'),
        ('v5 = os.path.join(X, "v5-polished")', f'v5 = {os.path.join(XS, "v5-polished")!r}'),
        ('avs = os.path.join(X, "atlas-visual-system")', f'avs = {os.path.join(XS, "atlas-visual-system")!r}'),
        ('def rel(p):\n    return os.path.relpath(p, ROOT)',
         'def rel(p):\n'
         f'    if os.path.abspath(p) == {CV2!r}:\n        return "source/" + {PAGES["Concepts V2"][1]!r}\n'
         f'    if os.path.abspath(p).startswith({XS + os.sep!r}):\n        return "work/extract/" + os.path.relpath(p, {XS!r})\n'
         '    return os.path.relpath(p, ROOT)'),
    ]
    if tally:
        patch += [
            ('checked = collections.Counter()\n', 'checked = collections.Counter()\nBYSRC = collections.defaultdict(collections.Counter)\n'),
            ('checked["from-to-sign statements"] += 1', 'checked["from-to-sign statements"] += 1; BYSRC["from-to-sign statements"][DOCS[di]["group"]] += 1'),
            ('checked["table rows (link, from-to, sign, delay, grade)"] += 1',
             'checked["table rows (link, from-to, sign, delay, grade)"] += 1; BYSRC["table rows"][DOCS[di]["group"]] += 1'),
            ('checked["link names shown without their ID"] += 1',
             'checked["link names shown without their ID"] += 1; BYSRC["link names shown without their ID"][DOCS[di]["group"]] += 1'),
            ('checked["reform effect words"] += 1', 'checked["reform effect words"] += 1; BYSRC["reform effect words"][DOCS[di]["group"]] += 1'),
            ('checked["loop titles next to loop IDs"] += 1',
             'checked["loop titles next to loop IDs"] += 1; BYSRC["loop titles next to loop IDs"][DOCS[o["doc"]]["group"]] += 1'),
        ]
    for a, b in patch:
        assert src.count(a) == 1, a
        src = src.replace(a, b)
    g = {'__name__': '__main__', '__file__': P0_SCRIPT}
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, P0_SCRIPT, 'exec'), g)
    return g


clean_out, tally_out = os.path.join(WORK, 'reconcile-clean.json'), os.path.join(WORK, 'reconcile-tally.json')
phase0(clean_out, False)
G = phase0(tally_out, True)
raw0, raw1, raw2 = (open(p, 'rb').read() for p in (P0_DATA, clean_out, tally_out))
assert raw1 == raw2, 'the tallies changed the result'
D0, D1 = json.loads(raw0), json.loads(raw1)
field_equal = {k: D0.get(k) == D1.get(k) for k in D0}
BYSRC = {k: dict(v) for k, v in G['BYSRC'].items()}

# 4. families, by Phase 0's formula (build_reconciliation_table.py lines 190 to 215), and their sources


def group_of_file(f):
    return 'V5 Polished' if f.startswith('work/extract/v5-polished/') else 'Atlas Visual System' if f.startswith('work/extract/atlas-visual-system/') \
        else 'Concepts V2' if f.startswith('source/') else '?'


def families(D, bysrc):
    cr = D['summary']['checks_run']
    tags = sum(1 for r in D['register_rows'] if r['from_sheet_shown'])
    also = sum(1 for v in D['register_vars'] if 'Also under' in v['kind'])
    link_attr = [o for o in D['occurrences'] if 'connection' in o['kinds'] and o['shown']]
    cv2 = lambda n: {'Concepts V2': n}
    split = lambda key, k=1: {s: n * k for s, n in (bysrc or {}).get(key, {}).items()}
    la = collections.Counter(group_of_file(o['file']) for o in link_attr)
    ew = split('reform effect words')
    ew['Atlas Visual System'] = ew.get('Atlas Visual System', 0) + cr['AVS outcome cells']
    return [
        ('Concepts V2 Register connection rows', len(D['register_rows']) * 7 + tags, cv2(len(D['register_rows']) * 7 + tags)),
        ('Concepts V2 Register variable cards', cr['Register variable cards'] * 4 + also, cv2(cr['Register variable cards'] * 4 + also)),
        ('Concepts V2 Register reform rows', cr['Register reform rows'] * 2, cv2(cr['Register reform rows'] * 2)),
        ('Concepts V2 Register effect cells', cr['Register effect cells'], cv2(cr['Register effect cells'])),
        ('Concepts V2 Register sheet figures and index table', 82 + 64, cv2(146)),
        ('Concepts V2 Field Guide specimens', cr['Field Guide specimens'] * 8, cv2(cr['Field Guide specimens'] * 8)),
        ('Concepts V2 Who Can Act', cr['Who Can Act route rows'] * 3 + cr['Who Can Act outcome rows'] + cr['Who Can Act group rows'] + cr['Who Can Act reform titles'],
         cv2(cr['Who Can Act route rows'] * 3 + cr['Who Can Act outcome rows'] + cr['Who Can Act group rows'] + cr['Who Can Act reform titles'])),
        ('Concepts V2 Ledger rows', cr['Ledger rows'] * 4, cv2(cr['Ledger rows'] * 4)),
        ('Concepts V2 Circuit', 5 + 4 + cr['Circuit pass-on examples'] + 13, cv2(5 + 4 + cr['Circuit pass-on examples'] + 13)),
        ('Other numeric claims', cr['numeric and structural claims'], cv2(cr['numeric and structural claims'])),
        ('Direction-and-sign sentences', cr['from-to-sign statements'] * 2, split('from-to-sign statements', 2)),
        ('AVS production table rows', cr['table rows (link, from-to, sign, delay, grade)'] * 4, split('table rows', 4)),
        ('Connection names shown without an ID', cr['link names shown without their ID'], split('link names shown without their ID')),
        ('Connection IDs with a grade, delay or glyph shown beside them', len(link_attr), dict(la)),
        ('Loop titles printed beside loop IDs', cr.get('loop titles next to loop IDs', 0), split('loop titles next to loop IDs')),
        ('Reform effect words (Concepts V2 and AVS outcome figure)', cr['reform effect words'] + cr['AVS outcome cells'], ew),
        ('AVS domain titles and layer rows', cr['AVS domain rows'] + cr['AVS layer rows'], {'Atlas Visual System': cr['AVS domain rows'] + cr['AVS layer rows']}),
    ]


F0, F1 = families(D0, None), families(D1, BYSRC)
assert [(a, b) for a, b, _ in F0] == [(a, b) for a, b, _ in F1]
for name, n, s in F1:
    assert sum(s.values()) == n, (name, n, s)
NOT_RERUN_R3 = {'Concepts V2 Register effect cells': 344, 'Concepts V2 Who Can Act': 94, 'AVS production table rows': 48,
                'Connection names shown without an ID': 127, 'Reform effect words (Concepts V2 and AVS outcome figure)': 24,
                'AVS domain titles and layer rows': 13, 'Concepts V2 Circuit': 18}
assert sum(NOT_RERUN_R3.values()) == 668


# conflicts per family: Phase 0's findings and reviewed flags, placed by the check that raised them
def fam_of(f):
    n = f['note']
    if n.startswith('Ledger'):
        return 'Concepts V2 Ledger rows'
    if n.startswith('connection attribute'):
        return 'Connection IDs with a grade, delay or glyph shown beside them'
    return n


conf = collections.Counter(fam_of(f) for f in D1['findings'])
rfp = collections.Counter(fam_of(f) for f in D1['reviewed_false_positives'])
NAMES = {name for name, _, _ in F1}
assert set(conf) <= NAMES and set(rfp) <= NAMES, ('a finding the family map does not place', set(conf) | set(rfp))

# 5. the Circuit's 13 drawn bundle counts, read by position on section 10 (Concept 09) of Concepts V2
H = open(CV2, encoding='utf-8').read()
st = [m.start() for m in re.finditer(r'<section class="pg"', H)] + [len(H)]
frag = H[st[10]:st[11]]
assert 'Atlas concept 09' in re.sub(r'&nbsp;', ' ', frag)
divs = [(float(a), float(b), c) for a, b, c in re.findall(r'left: ([\d.]+)px; top: ([\d.]+)px;[^>]*>(.{0,260}?)</div>', frag)]
col = sorted((x, c.strip()) for x, y, c in divs if y == 374 and re.fullmatch(r'[A-E]', c.strip()))
assert [c for _, c in col] == list('ABCDE')
V7 = G['V7']
NODES, LINKS = G['NODES'], G['LINKS']
pair = collections.Counter((G['area'](L['from']), G['area'](L['to'])) for L in LINKS.values())


def column(x):
    i = max(j for j, (cx, _) in enumerate(col) if cx <= x)
    return i


bundles = []
for x, y, c in divs:
    if not re.fullmatch(r'\d+', c.strip()):
        continue
    n = int(c)
    if y == 316:
        a = col[column(x)][1]
        key = ('X', a)
    elif y == 424:  # the upper wire between two columns: the left area into the right one
        i0 = max(j for j, (cx, _) in enumerate(col) if cx < x)
        key = (col[i0][1], col[i0 + 1][1])
    elif 590 <= y <= 630:
        i0 = max(j for j, (cx, _) in enumerate(col) if cx < x)
        key = (col[i0 + 1][1], col[i0][1])
    elif y > 1000:
        key = ('technology', 'economy')
    else:
        continue
    bundles.append({'drawn_at': [x, y], 'from': key[0], 'to': key[1], 'shown': n, 'v7_today': pair[key], 'equal': n == pair[key]})
assert len(bundles) == 13, len(bundles)

# results
tot0 = sum(n for _, n, _ in F0)
tot1 = sum(n for _, n, _ in F1)
by_src = collections.Counter()
for _, _, s in F1:
    by_src.update(s)
not_rerun_by_src = collections.Counter()
for name, n, s in F1:
    if name in NOT_RERUN_R3:
        k = NOT_RERUN_R3[name]
        if name == 'Concepts V2 Circuit':
            not_rerun_by_src['Concepts V2'] += k
        else:
            assert n == k
            not_rerun_by_src.update(s)
rows = []
for (name, n0, _), (_, n1, s1) in zip(F0, F1):
    rows.append({'family': name, 'phase0_comparisons': n0, 'phase0_conflicts': 2 if name == 'Concepts V2 Ledger rows' else 0,
                 'rerun_comparisons': n1, 'rerun_conflicts': conf.get(name, 0), 'reviewed_false_positives_found_again': rfp.get(name, 0),
                 'page_side_from': s1, 'not_rerun_at_round_3': NOT_RERUN_R3.get(name, 0),
                 'how': ('Phase 0’s script, run today' if name != 'Concepts V2 Circuit' else
                         'Phase 0’s script for the tally, area cards and pass-on examples (14); the 13 drawn bundle counts read by position')})
data = {
    'run': 'November 13, 2026, research lead, Phase 3 board 2 (DR-258)',
    'purpose': ('Data for chapter 15’s reconciliation table at board 3. These are older files: today’s guide is the standard, and this rerun '
                'changes nothing in the guide (the main session’s word, from Dustin).'),
    'inputs': inputs,
    'v7_model': {'file': 'work/extract/atlas-v7-data.json', 'sha256': MODEL_SHA, 'equal_to': 'work/research/atlas-v7-docs/20261015_Atlas-V7-Model.json'},
    'method': ('Phase 0’s own split (work/build/scripts/extract_sources.py) and its own reconciliation script '
               '(work/build/scripts/phase-0/atlas_reconcile_extract.py), run in scratch with only their input and output paths changed; '
               'comparison families counted by Phase 0’s formula (build_reconciliation_table.py lines 190 to 215).'),
    'phase0_output_equal': {'bytes_identical': raw0 == raw1, 'sha256_phase0': hashlib.sha256(raw0).hexdigest(),
                            'sha256_today': hashlib.sha256(raw1).hexdigest(), 'fields': field_equal},
    'totals': {'phase0_comparisons': tot0, 'rerun_comparisons': tot1, 'by_phase0_script': tot1 - 13, 'by_position_reading': 13,
               'rerun_conflicts': sum(conf.values()), 'reviewed_false_positives_found_again': sum(rfp.values()),
               'page_side_by_source': dict(by_src), 'the_668_not_rerun_at_round_3_by_source': dict(not_rerun_by_src),
               'identifier_occurrences': D1['summary']['identifier_occurrences'], 'documents_scanned': D1['summary']['documents_scanned']},
    'families': rows,
    'conflicts': D1['findings'],
    'reviewed_false_positives': [{k: f[k] for k in ('file', 'location', 'item', 'shown', 'v7', 'why')} for f in D1['reviewed_false_positives']],
    'circuit_bundles': bundles,
    'checks_run': D1['summary']['checks_run'],
    'differs_from_phase0': [k for k, v in field_equal.items() if not v],
    'new_v7_1_items': [],
}
assert all(b['equal'] for b in bundles)
data['new_v7_1_items'] = [] if raw0 == raw1 and all(b['equal'] for b in bundles) else ['see differs_from_phase0']


def md():
    L = []
    w = L.append
    w('# Atlas re-check, all three pages')
    w('')
    w('Research lead, November 13, 2026, for DR-258, board 2. Data for chapter 15’s reconciliation table at board 3. These are older '
      'files: today’s guide is the standard, and this rerun changes nothing in it. Nothing in Phase 0’s files, `source/`, the atlas or '
      'the guide changed. Machine-readable results: `work/research/20261113_Atlas-Recheck-Full-Data.json`. It completes round 3’s '
      're-check (`work/research/20261113_Atlas-Recheck-Table.md`, D3-1094), which could rerun 1,976 of the 2,644. Script: '
      '`work/build/scripts/phase-3/research_atlas_recheck_full.py`.')
    w('')
    w('## What the rerun found')
    w('')
    w(f'**All {tot1:,} of Phase 0’s comparisons were rerun ({tot0:,} in its table), and every result is Phase 0’s.** Run today on the three supplied pages and '
      f'today’s Atlas V7, Phase 0’s own script writes a data file equal to Phase 0’s byte for byte ({len(raw1):,} bytes, SHA-256 '
      f'{hashlib.sha256(raw1).hexdigest()[:16]}...): the same {sum(conf.values())} conflicts, the Ledger’s reform counts for D03 (shown 10, V7 9) and '
      f'D04 (shown 14, V7 13), the same {sum(rfp.values())} flags Phase 0 read in context and set aside, and the same '
      f'{D1["summary"]["identifier_occurrences"]:,} identifier occurrences in {D1["summary"]["documents_scanned"]} documents. '
      'The 13 drawn bundle counts on the Circuit, which Phase 0 counted but its script does not test, were read today by their position '
      'on the page and all 13 equal V7. So the rerun adds **no new V7.1 item**; the two Ledger counts are already on Phase 0’s list.')
    w('')
    w(f'Of the {tot1:,}, the page side came from Concepts V2 for {by_src["Concepts V2"]:,}, the Atlas Visual System for '
      f'{by_src["Atlas Visual System"]}, and V5 Polished for {by_src["V5 Polished"]}. Of the 668 that round 3 could not rerun, '
      f'{not_rerun_by_src["Concepts V2"]} read Concepts V2, {not_rerun_by_src["Atlas Visual System"]} the Atlas Visual System and '
      f'{not_rerun_by_src.get("V5 Polished", 0)} V5 Polished.')
    w('')
    w('## What was read')
    w('')
    for grp, v in inputs.items():
        w(f'- **{grp}:** `{v["file_read"]}`, uploaded November 13, read in place by script, {v["bytes"]:,} bytes, SHA-256 '
          f'{v["sha256"][:8]}...{v["sha256"][-6:]}, equal to the October 20 source manifest' +
          (f'; split into {v["split"]["sections"]} sections and {v["split"]["embedded_files"]} embedded files in scratch with Phase 0’s own code.' if 'split' in v else '.'))
    w('- **Atlas V7:** `work/extract/atlas-v7-data.json`, equal byte for byte to the committed model (SHA-256 ef1028ac...c7f2), the model Phase 0 compared against.')
    w('- **Phase 0’s code:** `work/build/scripts/extract_sources.py` and `work/build/scripts/phase-0/atlas_reconcile_extract.py`, run in scratch with only '
      'their input and output paths changed; Phase 0’s data file was read and never written.')
    w('')
    w('## Families')
    w('')
    w('| Family | Phase 0 comparisons | Phase 0 conflicts | Rerun comparisons | Rerun conflicts | Page side from | Not rerun at round 3 |')
    w('|---|---|---|---|---|---|---|')
    short = {'Concepts V2': 'Concepts V2', 'Atlas Visual System': 'AVS', 'V5 Polished': 'V5P'}
    for r in rows:
        src = ', '.join(f'{short[k]} {v:,}' for k, v in sorted(r['page_side_from'].items(), key=lambda kv: -kv[1]))
        w(f'| {r["family"]} | {r["phase0_comparisons"]:,} | {r["phase0_conflicts"]} | {r["rerun_comparisons"]:,} | {r["rerun_conflicts"]} | {src} | '
          f'{r["not_rerun_at_round_3"] or ""} |')
    w(f'| **Total** | **{tot0:,}** | **2** | **{tot1:,}** | **{sum(conf.values())}** | Concepts V2 {by_src["Concepts V2"]:,}, AVS {by_src["Atlas Visual System"]}, '
      f'V5P {by_src["V5 Polished"]} | **668** |')
    w('')
    w('AVS is the Atlas Visual System and V5P is V5 Polished. The production table rows and the effect words carry Phase 0’s family names; the '
      'source column says which pages their rows came from.')
    w('')
    w('## Conflicts and flags')
    w('')
    for f in D1['findings']:
        w(f'- {f["location"]}: {f["item"]}, shown {f["shown"]}; V7: {f["v7"]}. Phase 0 found the same.')
    w(f'- The {sum(rfp.values())} flags set aside, as Phase 0 set them aside: ' +
      '; '.join(f'{x["item"]} "{x["shown"]}" in {x["file"].split("/")[-1]}' for x in D1['reviewed_false_positives']) + '.')
    w('')
    w('## The Circuit’s drawn bundle counts')
    w('')
    w('Read by position: a count above an area column is the outside drivers into that area; a count on the upper wire between two columns is '
      'the left area into the right one, on the lower wire the right into the left; the count between the two lower panels is technology into '
      'the economy layer.')
    w('')
    w('| From | To | Shown | V7 today |')
    w('|---|---|---|---|')
    for b in bundles:
        w(f'| {b["from"]} | {b["to"]} | {b["shown"]} | {b["v7_today"]} |')
    w('')
    w('## Not tested')
    w('')
    w('- How the pages look: the rerun reads their text and markup, as Phase 0 did, and draws nothing.')
    w('- The 45 rows of Phase 0’s reconciliation table that propose resolutions (encodings, names, collisions): they are Phase 0’s readings, '
      'not comparisons, and stay with chapter 15 at board 3.')
    w('- The Circuit’s position reading is this rerun’s own, not Phase 0’s code; it rests on the page’s layout (area letters at one height, '
      'counts on two wires).')
    w('')
    return '\n'.join(L) + '\n'


text = md()
for bad in ('—', '‑'):
    assert bad not in text and bad not in json.dumps(data, ensure_ascii=False)
print(json.dumps(data['totals'], indent=1, ensure_ascii=False))
print('phase0 output equal byte for byte:', raw0 == raw1, '| differs:', data['differs_from_phase0'])
for r in rows:
    print('%-62s %5d/%d  %5d/%d  %s' % (r['family'][:62], r['phase0_comparisons'], r['phase0_conflicts'], r['rerun_comparisons'], r['rerun_conflicts'], r['page_side_from']))
print('bundles', [(b['from'], b['to'], b['shown'], b['v7_today']) for b in bundles])
if WRITE:
    for p, t in ((OUT_JSON, json.dumps(data, indent=1, ensure_ascii=False) + '\n'), (OUT_MD, text)):
        if os.path.exists(p) and open(p, encoding='utf-8').read() == t:
            print(os.path.relpath(p, ROOT), 'unchanged')
        else:
            open(p, 'w', encoding='utf-8').write(t)
            print('wrote', os.path.relpath(p, ROOT))
