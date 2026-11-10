"""Chapter 10, Topic and atlas symbols (stage B round 2, systems designer, November 10, 2026).

Usage:
    python3 -I work/build/scripts/phase-2/stage_b_ch10_build.py            draw the sheets, measure, write everything
    python3 -I work/build/scripts/phase-2/stage_b_ch10_build.py --no-draw  reuse the sheets and figures already written

Writes:
    work/build/guide/chapters/10-symbols.json                  the chapter in the content contract (Stage A brief)
    work/build/guide/specimens/s-10-*.html                     one fragment per specimen
    work/build/guide/specimens/manifest-systems.json           the s-10-* entries, merged; every other chapter's kept
    work/build/guide/specimens/img/20261110_Ch10-Library-*.png the five contact sheets, drawn from civic-line-v6
    work/handoffs/phase-2/20261110_Stage-B-Ch10-Figures.json    every figure the chapter prints, and how

Reads, never edits:
    work/build/assets/civic-line-v6/                            the 124 drawings in use and their inventory (D2-716)
    work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json     the editor's words: every label and meaning (DR-185)
    work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md the rules this chapter carries (the list of 41)
    work/build/assets/civic-line/tiles/                         the rounded tile's superellipse outline (D2-41)
    work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py   System 1's encoding glyphs (DR-36)
    work/extract/atlas-v7-data.json                             the atlas's domains, variables and reform targets
    work/build/scripts/phase-2/icon_likeness_check.js           the engineer's look-alike figure, run as written

Drawings reach the page from the engineer's sprite by <use> (D2-590): Civic Line as #oa-sym-<id>, utility icons as
#oa-sym-u-<name>-24px. The library shows each category as one contact sheet image (D2-591, D2-717), drawn here in
Chromium from the Black files at 128 px a drawing, kept to 16 colors, and shown at 64 px a drawing: each cell of the
library grid draws its own square of the sheet with <use> of one <image>, so the page carries each sheet once while the
words beside each drawing stay live text that wraps on a phone.

The specimen checks are stage_a_systems_build.Ctx.spec(): no heading or landmark element, no dash, no literal color,
no px font size, and every class prefixed sx- so no name meets a shell class.
"""
import argparse
import importlib.util
import io
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent


def _load(name, path=None):
    spec = importlib.util.spec_from_file_location(name, path or HERE / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


B = _load('stage_a_systems_build')
C = sys.modules['stage_a_systems_core']
ROOT = C.ROOT
S1 = _load('s1_times_explainer', ROOT / 'work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py')

CL6 = ROOT / 'work/build/assets/civic-line-v6'
INV_PATH = CL6 / '20261110_Civic-Line-V6-Inventory.json'
LABELS_PATH = ROOT / 'work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json'
CONSTRUCTION = ROOT / 'work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md'
TILE_ROUNDED = (ROOT / 'work/build/assets/civic-line/tiles/rounded-charcoal/svg/'
                '20261029_Oath-And-Action-Civic-Line-CL-031-Local-Government-Tile-Rounded-Charcoal-Two-Color.svg')
V7 = ROOT / 'work/extract/atlas-v7-data.json'
V7_COMMITTED = ROOT / 'work/research/atlas-v7-docs/20261015_Atlas-V7-Model.json'
LIKENESS = ROOT / 'work/build/scripts/phase-2/icon_likeness_check.js'
OUT_CH = ROOT / 'work/build/guide/chapters/10-symbols.json'
OUT_SP = ROOT / 'work/build/guide/specimens'
IMG = OUT_SP / 'img'
MANIFEST = OUT_SP / 'manifest-systems.json'
FIG_OUT = ROOT / 'work/handoffs/phase-2/20261110_Stage-B-Ch10-Figures.json'
CH = '10'
ILLUS = B.ILLUS
NB = ' '
DOT = '·'
SHOWN = 64          # a library drawing's size on the page; the sheet holds it at twice that (D2-591)
CELL = 2 * SHOWN

PILLARS = ('CL-019', 'CL-020', 'CL-021', 'CL-022')
CATEGORIES = [   # the five October sheets, as the inventory in use files each drawing (D2-714 puts CL-073, CL-074 in 01)
    ('01', 'Participation', 'Participation'),
    ('02', 'Government-Tech', 'Government and technology'),
    ('03', 'Economy-Issues', 'Economy and issues'),
    ('04', 'Reforms-01-25', 'Reforms R-01 to R-25'),
    ('05', 'Reforms-26-50', 'Reforms R-26 to R-50'),
]
LOOKALIKES = [   # the round 2 brief's side by side checks, with what tells each group apart (my words; the editor edits)
    (('CL-073', 'CL-005'), 'Testify seats three officials on a raised dais above one witness at a microphone. Public '
                           'meeting stands one speaker at a lectern, facing the people in the room.'),
    (('CL-074', 'CL-061'), 'Contact an official joins a person to an official at a desk, with a speech mark on the '
                           'line. Household income sends an envelope from a person along an arrow.'),
    (('CL-025', 'CL-014'), 'Congress shows the chamber in session under its three-tier rostrum. Entrenched majority '
                           'control fences the chamber, and a ballot’s arrow stops at the fence.'),
    (('CL-053', 'CL-054', 'CL-063'), 'All three hold a house. Housing scarcity counts too few homes, Owner home equity '
                                     'adds a rising chart, and Cost of essentials sets the house among other bills.'),
    (('CL-027', 'CL-031'), 'Both stand on a building’s front. Court alignment holds the scales, and Local government '
                           'is a hall with a door.'),
    (('CL-048', 'CL-023'), 'Both hold a page. Public records files it in an open drawer, and Evidence checks it '
                           'under a magnifier.'),
]


# ------------------------------------------------------------------------------------------------ inputs
def load_inputs():
    inv = json.loads(INV_PATH.read_text())
    icons = inv['icons']
    if len(icons) != 124:
        raise SystemExit(f'{INV_PATH.name}: {len(icons)} drawings, expected 124')
    black = {}
    for p in sorted((CL6 / 'black').glob('*-Black.svg')):
        m = re.search(r'\sdata-id="([^"]+)"', p.read_text())
        if m:
            black[m.group(1)] = p
    missing = [i['id'] for i in icons if i['id'] not in black]
    if missing:
        raise SystemExit(f'civic-line-v6/black lacks {missing}')
    lab = json.loads(LABELS_PATH.read_text())
    rows = {r['id']: r for r in lab['rows']}
    if set(rows) != {i['id'] for i in icons}:
        raise SystemExit('the label table and the inventory in use name different drawings')
    text = CONSTRUCTION.read_text()
    m = re.search(r'\*\*The list, by ID\*\*.*?\n\n(.*?)\n', text, re.S)
    reads24 = re.findall(r'(?:CL|R)-\d+', m.group(1))
    if len(reads24) != 41 or len(set(reads24)) != 41:
        raise SystemExit(f'the construction file lists {len(reads24)} drawings for 24 px, expected 41')
    v7 = json.loads((V7 if V7.exists() else V7_COMMITTED).read_text())
    return icons, black, rows, reads24, v7


def family(row, atlas=False):
    k = row['class']
    if k == 'pillar':
        return 'pillar'
    if k == 'topic':
        return 'topic'
    if k == 'topic and atlas variable':
        return 'atlas' if atlas else 'topic'
    return 'atlas'


def word(row, atlas=False):
    if atlas and row.get('label_where_atlas'):
        return row['label_where_atlas']
    return row['label']


# ------------------------------------------------------------------------------------------------ drawing in Chromium
SHEET_JS = r"""
const { chromium } = require('playwright');
const fs = require('fs');
const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 1 });
  for (const s of job.sheets) {
    const cells = s.files.map((f) => fs.readFileSync(f, 'utf8').replace(/<\?xml[^>]*>\s*/, '')
      .replace(/<svg\b([^>]*)>/, (m, a) => '<svg' + a.replace(/\s(width|height)="[^"]*"/g, '') + ` width="${job.cell}" height="${job.cell}" style="display:block">`));
    await p.setContent(`<!doctype html><body style="margin:0;background:${job.ground}"><div id="g" style="display:grid;` +
      `grid-template-columns:repeat(${s.cols},${job.cell}px);width:${s.cols * job.cell}px">${cells.join('')}</div></body>`);
    await (await p.$('#g')).screenshot({ path: s.out });
  }
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
"""


def draw_sheets(icons, black, tmp):
    """One contact sheet per category: every drawing's Black file at 128 px, in inventory order, on Newsprint."""
    from PIL import Image
    IMG.mkdir(parents=True, exist_ok=True)
    jobs, meta = [], {}
    for num, slug, name in CATEGORIES:
        ids = [i['id'] for i in icons if i['sheet'] == num]
        cols = 8
        raw = tmp / f'sheet-{num}.png'
        jobs.append({'out': str(raw), 'cols': cols, 'files': [str(black[i]) for i in ids]})
        meta[num] = {'ids': ids, 'cols': cols, 'raw': raw, 'file': IMG / f'20261110_Ch10-Library-{num}-{slug}.png'}
    job = {'sheets': jobs, 'cell': CELL, 'ground': '#DCD9D2'}
    (tmp / 'job.json').write_text(json.dumps(job))
    (tmp / 'sheets.js').write_text(SHEET_JS)
    subprocess.run(['node', str(tmp / 'sheets.js'), str(tmp / 'job.json')], check=True, cwd=tmp)
    out = {}
    for num, m in meta.items():
        im = Image.open(m['raw']).convert('RGB')
        buf = io.BytesIO()
        im.quantize(colors=16, method=Image.Quantize.MEDIANCUT).save(buf, 'PNG', optimize=True)
        m['file'].write_bytes(buf.getvalue())
        out[num] = {'file': str(m['file'].relative_to(ROOT)), 'ids': m['ids'], 'cols': m['cols'],
                    'width': im.width, 'height': im.height, 'bytes': len(buf.getvalue())}
    return out


def measure_likeness(black, tmp):
    """The engineer's look-alike figure for each pair in LOOKALIKES, drawn from the set in use. Every file goes in as a
    new drawing, so each pair is computed between the drawings in use (the check's masters are the October files)."""
    ids = sorted({i for grp, _ in LOOKALIKES for i in grp})
    d = tmp / 'likeness'
    d.mkdir(exist_ok=True)
    for i in ids:
        shutil.copy(black[i], d / black[i].name)
    out = tmp / 'likeness.json'
    subprocess.run(['node', str(LIKENESS), str(d), '--watch', '1', '--flag', '99', '--json', str(out), '--quiet'],
                   cwd=ROOT, stdout=subprocess.DEVNULL)
    r = json.loads(out.read_text())
    idof = lambda n: re.search(r'(?:CL|R)-\d+', n).group(0)
    pairs = {}
    for row in r['flagged'] + r['watch']:
        if row.get('against') == 'new':
            pairs[tuple(sorted((idof(row['a']), idof(row['b']))))] = {'likeness': row['likeness'], 'percentile': row['percentile']}
    res = {}
    for grp, _ in LOOKALIKES:
        for a in range(len(grp)):
            for b in range(a + 1, len(grp)):
                k = tuple(sorted((grp[a], grp[b])))
                if k not in pairs:
                    raise SystemExit(f'no likeness figure for {k}')
                res['|'.join(k)] = pairs[k]
    return {'pairs': res, 'thresholds': r['thresholds'], 'distribution': r['distribution'], 'renderer': r['renderer'],
            'method': r['method'], 'run': r['run']}


# ------------------------------------------------------------------------------------------------ markup helpers
def sym(i, px, surface='newsprint', two=False, fam='topic', cls='sym', vb='0 0 128 128', ink=None, accent=None):
    """A Civic Line drawing from the sprite. Two-color sets the accent from the surface's token (DR-66, R11)."""
    col = ink or f'var(--oa-component-icon-ink-on-{surface})'
    st = f'color:{col}'
    if two:
        st += f';--oa-icon-accent:{accent or f"var(--oa-component-icon-accent-on-{surface})"}'
    return (f'<svg class="{cls}" viewBox="{vb}" width="{px:g}" height="{px:g}" aria-hidden="true" focusable="false" '
            f'data-icon="{i}" data-icon-family="{fam}" style="{st}"><use href="#oa-sym-{i.lower()}"/></svg>')


def util(name, px=24, cls='ug'):
    return (f'<svg class="{cls}" viewBox="0 0 {px} {px}" width="{px}" height="{px}" aria-hidden="true" focusable="false" '
            f'data-icon="U-{name}" data-icon-family="utility"><use href="#oa-sym-u-{name}-{px}px"/></svg>')


def esc(s):
    return C.esc(s)


def px2(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.') if abs(v - round(v)) > 1e-9 else f'{v:.0f}'


def line_px(units, size):
    return units / 128 * size


class K:
    """Shorthands for the token CSS every specimen uses."""

    def __init__(self, ctx):
        self.ctx = ctx

    def vars(self, s='newsprint'):
        return (f':scope{{--t1:var(--oa-color-text-primary-on-{s});--t2:var(--oa-color-text-secondary-on-{s});'
                f'--hair:var(--oa-color-border-hairline-on-{s});--strong:var(--oa-color-border-strong-on-{s});'
                f'--ink:var(--oa-component-icon-ink-on-{s});--sub:var(--oa-color-graphic-subtle-on-{s});'
                f'--focus:var(--oa-color-focus-ring-on-{s});--red:var(--oa-color-palette-pillar-red);'
                f'color:var(--t1)}}')

    def t(self, name):
        return self.ctx.ty(name)


# ------------------------------------------------------------------------------------------------ the specimens
def specimens(ctx, icons, rows, reads24, v7, sheets, like, figs):
    k = K(ctx)
    inv = {i['id']: i for i in icons}
    band_css, band = ctx.fail_band()
    t = k.t
    chip_css = (f'.chip{{display:inline-block;{t("label")};line-height:1.2;padding:3px 6px;border:1px solid var(--strong);'
                f'white-space:nowrap;color:var(--t1)}}')

    # ---------------------------------------------------------------- 10.1 classes
    track, loc, ent = rows['CL-020'], rows['CL-031'], rows['CL-014']
    tag_svg = ('<svg class="enc" viewBox="0 0 64 28" width="64" height="28" aria-hidden="true" focusable="false" '
               'data-icon="E-sign-same" data-icon-family="encoding"><g class="wire">'
               + S1.wire_marks([(2, 14), (62, 14)], 'documented', '+', None, 2, lit=False)[0] + '</g></svg>')
    status_svg = ('<svg class="st" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" '
                  'data-icon="S-now" data-icon-family="status"><circle class="st-ring" cx="12" cy="12" r="10.5"/>'
                  '<text class="st-n" x="12" y="16.6" font-size="13">2</text></svg>')
    classes = [
        ('Pillar icon', sym('CL-020', 48, fam='pillar'), track['label'],
         'Marks which of our four pillars a piece serves, in the order Explain, Track, Connect, Act.', 'Chapter 09'),
        ('Topic symbol', sym('CL-031', 48, fam='topic'), loc['label'],
         'Names the subject of a piece.', 'Chapter 10'),
        ('Atlas symbol', sym('CL-014', 48, fam='atlas'), f'{ent["label"]}<br><span class="chip">{esc(ent["v7_chip"])}</span>',
         'Names a variable or a reform in our systems atlas.', 'Chapter 10'),
        ('Status mark', status_svg, 'Step 2 of 6: Hearing',
         'Says where a bill, a records request or an agency rule stands.', 'Chapter 11'),
        ('Utility icon', util('search'), 'Search',
         'Names an action a reader takes, always beside its word.', 'Chapter 11'),
        ('Encoding glyph', tag_svg, 'raises',
         'Carries the atlas’s grammar of sign, authority, evidence and delay.', 'Shown here, taught in chapter 15'),
    ]
    li = ''.join(
        f'<li class="row"><div class="ex">{g}<span class="w">{w}</span></div><div class="tx"><p class="cn">{esc(n)}</p>'
        f'<p class="job">{esc(j)}</p><p class="ch">{esc(c)}</p></div></li>' for n, g, w, j, c in classes)
    css = (k.vars() + chip_css +
           '.list{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}'
           '.row{display:grid;grid-template-columns:136px minmax(0,1fr);gap:16px;padding:16px 0;border-bottom:1px solid var(--hair);align-items:center}'
           '.ex{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center}'
           f'.w{{{t("caption")};color:var(--t1)}}'
           f'.cn{{margin:0;{t("ui")};font-weight:700}}.job{{margin:4px 0 0;{t("bodySmall")}}}'
           f'.ch{{margin:6px 0 0;{t("label")};color:var(--t2)}}'
           '.sym,.ug,.enc,.st{display:block;color:var(--ink)}'
           '.st-ring{fill:var(--oa-color-surface-newsprint);stroke:var(--ink);stroke-width:var(--oa-component-mark-ring-now)}'
           '.st-n{fill:var(--t1);font-family:var(--oa-font-family-reading);font-weight:700;text-anchor:middle;font-variant-numeric:tabular-nums}'
           + S1_CSS)
    ctx.spec('s-10-1-correct', f'<style>{css}</style><ul class="list">{li}</ul>', CH, '10.1',
             'The six kinds of symbol, one to a row, each with an example at the size it is used. Pillar icon: Track at '
             '48 px, which marks which of our four pillars a piece serves; chapter 09. Topic symbol: Local government at '
             '48 px, which names the subject of a piece; chapter 10. Atlas symbol: Entrenched majority control, Variable '
             'D7, at 48 px, which names a variable or a reform in our systems atlas; chapter 10. Status mark: a step ring '
             'with the number 2, for Step 2 of 6: Hearing, which says where a bill or a record stands; chapter 11. Utility '
             'icon: the search magnifier at 24 px beside the word Search; chapter 11. Encoding glyph: a line with a tag '
             'holding a plus sign, read as raises; shown here and taught in chapter 15.',
             width=600, readable=True, notes='D2-515; readable list (D2-255). Status ring drawn at the tracker\'s 24 px size '
             'with the ring.now token; encoding tag drawn by System 1\'s wire_marks (DR-36).')

    rec = rows['CL-048']
    fail = (f'{band}<div class="page"><p class="ttl">Brand files</p><p class="lede">Every logo, icon and font file, sorted '
            f'by size and surface.</p><span class="btn">{sym("CL-048", 24, fam="topic")}<span>Downloads</span></span></div>')
    css = (k.vars() + band_css + '.page{padding:16px;border:1px solid var(--hair)}'
           f'.ttl{{margin:0;{t("h4")}}}.lede{{margin:6px 0 16px;{t("bodySmall")};color:var(--t2)}}'
           f'.btn{{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border:2px solid var(--strong);{t("ui")};font-weight:600}}'
           '.sym{display:block}')
    ctx.spec('s-10-1-failure', f'<style>{css}</style>{fail}', CH, '10.1',
             'Labeled Failure case: do not publish. A Brand files page at 360 px whose Downloads button carries the '
             f'{rec["label"]} drawing, an open drawer of files, at 24 px in place of the download icon.',
             width=360, notes='Topic drawing standing for an interface action (D2-515). CL-048 is on the list of 41, so '
             'the size is allowed; the class is the fault.')

    # ---------------------------------------------------------------- library extras (after 10.1)
    for num, slug, name in CATEGORIES:
        sh = sheets[num]
        cells, dl = [], []
        for n, i in enumerate(sh['ids']):
            r = rows[i]
            c, rr = n % sh['cols'], n // sh['cols']
            fam = family(r)
            sub = [i]
            if r['class'] == 'pillar':
                sub.append('Pillar icon')
            elif r.get('v7_chip') and not i.startswith('R-'):
                sub.append(r['v7_chip'])
            tag = ('<span class="t24">Also at 24 px</span>' if i in reads24 and r['class'] != 'pillar' else '')
            cells.append(f'<li class="cell"><svg class="ls" viewBox="{c * CELL} {rr * CELL} {CELL} {CELL}" width="{SHOWN}" '
                         f'height="{SHOWN}" aria-hidden="true" focusable="false" data-icon="{i}" data-icon-family="{fam}">'
                         f'<use href="#sheet"/></svg><span class="w">{esc(word(r))}</span>'
                         f'<span class="id">{esc(f" {DOT} ".join(sub))}</span>{tag}</li>')
            extra = ''
            if r.get('label_where_atlas'):
                extra = (f'<dd class="m2"><span class="chip">{esc(r["v7_chip"])}</span> {esc(r["label_where_atlas"])}. '
                         f'{esc(r["meaning_where_atlas"])}</dd>')
            elif r.get('v7_chip') and not i.startswith('R-'):
                extra = f'<dd class="m2"><span class="chip">{esc(r["v7_chip"])}</span></dd>'
            size = ('24 px and up on 1x and 2x screens from chapter 09’s drawings' if r['class'] == 'pillar'
                    else '24 px and up' if i in reads24 else '48 px and up')
            dl.append(f'<div class="it"><dt><span class="di">{esc(i)}</span> {esc(word(r))}</dt><dd>{esc(r["meaning"])}</dd>'
                      f'{extra}<dd class="sz">Smallest size: {size}</dd></div>')
        n_ids = len(sh['ids'])
        first, last = sh['ids'][0], sh['ids'][-1]
        span = f'{first} to {last}' if num != '01' else 'CL-001 to CL-024, CL-073 and CL-074'
        html = (f'<p class="hd">{esc(name)}: {n_ids} drawings, {span}</p>'
                f'<svg class="defs" width="0" height="0" aria-hidden="true" focusable="false"><defs><image id="sheet" '
                f'href="{sh["file"]}" width="{sh["width"]}" height="{sh["height"]}"/></defs></svg>'
                f'<ul class="grid">{"".join(cells)}</ul>'
                f'<details class="more"><summary>{util("chevron", cls="chev")}<span>Meanings and smallest sizes of the '
                f'{n_ids} drawings</span></summary><dl class="dl">{"".join(dl)}</dl></details>')
        css = (k.vars() + chip_css +
               f'.hd{{margin:0 0 12px;{t("label")};color:var(--t2)}}'
               '.defs{position:absolute;width:0;height:0;overflow:hidden}'
               '.grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));'
               'border-top:1px solid var(--hair);border-left:1px solid var(--hair)}'
               '.cell{display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;padding:14px 6px 12px;'
               'border-right:1px solid var(--hair);border-bottom:1px solid var(--hair)}'
               '.ls{display:block;margin:0 0 4px}'
               f'.w{{{t("caption")};font-weight:600;text-wrap:balance;overflow-wrap:anywhere}}'
               f'.id{{{t("label")};color:var(--t2);font-variant-numeric:tabular-nums}}'
               f'.t24{{{t("label")};color:var(--t1);border-bottom:2px solid var(--ink)}}'
               '.more{margin:16px 0 0}'
               f'summary{{display:flex;align-items:center;gap:8px;min-height:44px;cursor:pointer;list-style:none;{t("ui")};font-weight:600}}'
               'summary::-webkit-details-marker{display:none}'
               'summary:focus-visible{outline:var(--oa-border-width-focus-ring) solid var(--focus);outline-offset:2px}'
               '.chev{display:block;flex:none;color:var(--ink)}'
               '.more[open] .chev{transform:rotate(180deg)}'
               '.dl{margin:8px 0 0;border-top:1px solid var(--hair)}'
               '.it{padding:12px 0;border-bottom:1px solid var(--hair)}'
               f'dt{{{t("ui")};font-weight:700}}.di{{font-weight:400;color:var(--t2);font-variant-numeric:tabular-nums}}'
               f'dd{{margin:4px 0 0;{t("bodySmall")}}}.m2{{color:var(--t1)}}'
               f'.sz{{{t("caption")};color:var(--t2)}}')
        ids_txt = ', '.join(f'{i} {word(rows[i])}' for i in sh['ids'])
        ctx.spec(f's-10-lib-{num}', f'<style>{css}</style>{html}', CH, None,
                 f'Contact sheet: {name}, {n_ids} Civic Line drawings in one color at 64 px, each with its word and ID: '
                 f'{ids_txt}. A closed list below the sheet gives each drawing’s meaning and smallest size.',
                 width=600, interactive=True,
                 notes=f'D2-591, D2-717: one contact sheet image, {sh["file"]}, {sh["width"]} by {sh["height"]} px, 16 colors, '
                       f'drawn from civic-line-v6/black at 128 px a drawing and shown at 64 px. Each cell draws its square '
                       f'with <use> of the one <image>. Words and meanings from the editor\'s label table (DR-185).')

    # ---------------------------------------------------------------- 10.2 construction
    u_cap = 3.3508
    S3 = 3          # the big drawing at three times its 128 px master
    X0, Y0 = 16, 24
    big = 128 * S3
    grid = ''.join(f'<line class="gl" x1="{X0 + g * S3}" y1="{Y0}" x2="{X0 + g * S3}" y2="{Y0 + big}"/>'
                   f'<line class="gl" x1="{X0}" y1="{Y0 + g * S3}" x2="{X0 + big}" y2="{Y0 + g * S3}"/>' for g in range(16, 128, 16))
    fz = f'<rect class="fz" x="{X0 + 6 * S3}" y="{Y0 + 6 * S3}" width="{116 * S3}" height="{116 * S3}"/>'
    ctr = (f'<line class="cx" x1="{X0 + 64 * S3}" y1="{Y0 + 56 * S3}" x2="{X0 + 64 * S3}" y2="{Y0 + 72 * S3}"/>'
           f'<line class="cx" x1="{X0 + 56 * S3}" y1="{Y0 + 64 * S3}" x2="{X0 + 72 * S3}" y2="{Y0 + 64 * S3}"/>')
    drawing = (f'<svg x="{X0}" y="{Y0}" width="{big}" height="{big}" viewBox="0 0 128 128" data-icon="CL-031" '
               f'data-icon-family="topic" style="color:var(--ink);--oa-icon-accent:var(--oa-component-icon-accent-on-newsprint)">'
               f'<use href="#oa-sym-cl-031"/></svg>')
    AX = X0 + big + 24   # notes column
    notes = [  # (text lines, target x,y in units, label y)
        (['128-unit box'], (128, 0), 30),
        (['116 units: the most', 'a drawing fills'], (122, 20), 92),
        (['Line 3.35 units, with', 'round ends and corners'], (82.39, 72), 186),
        (['One red part: the door'], (70.74, 88), 282),
        (['Ink centered on 64, 64'], (72, 64), 338),
    ]
    lead = []
    labels = []
    for lines, (ux, uy), ly in notes:
        tx, ty = X0 + ux * S3, Y0 + uy * S3
        lead.append(f'<path class="ld" d="M{AX - 6} {ly - 5}H{AX - 14}L{tx + 3:.1f} {ty:.1f}"/><circle class="dt" cx="{tx:.1f}" cy="{ty:.1f}" r="2.5"/>')
        labels.append(''.join(f'<text class="nt" x="{AX}" y="{ly + 18 * n}">{esc(s)}</text>' for n, s in enumerate(lines)))
    row_y = Y0 + big + 36
    sizes = [(128, 'Master, 128 px'), (64, '64 px'), (48, '48 px')]
    xx, row = X0, []
    for s, lab in sizes:
        row.append(f'<svg x="{xx}" y="{row_y + 128 - s}" width="{s}" height="{s}" viewBox="0 0 128 128" data-icon="CL-031" '
                   f'data-icon-family="topic" style="color:var(--ink);--oa-icon-accent:var(--oa-component-icon-accent-on-newsprint)">'
                   f'<use href="#oa-sym-cl-031"/></svg>'
                   f'<text class="nt" x="{xx}" y="{row_y + 128 + 22}">{esc(lab)}</text>'
                   f'<text class="nt2" x="{xx}" y="{row_y + 128 + 40}">line {px2(line_px(u_cap, s))} px</text>')
        xx += s + 56
    H = row_y + 128 + 52
    svg = (f'<svg class="con" viewBox="0 0 600 {H}" width="600" height="{H}" aria-hidden="true" focusable="false">'
           f'<rect class="bx" x="{X0}" y="{Y0}" width="{big}" height="{big}"/>{grid}{fz}{ctr}{drawing}{"".join(lead)}'
           f'{"".join(labels)}{"".join(row)}</svg>')
    css = (k.vars() + '.con{display:block}'
           '.bx{fill:none;stroke:var(--strong);stroke-width:1}.gl{stroke:var(--hair);stroke-width:1}'
           '.fz{fill:none;stroke:var(--strong);stroke-width:1;stroke-dasharray:4 4}'
           '.cx{stroke:var(--strong);stroke-width:1}'
           '.ld{fill:none;stroke:var(--t1);stroke-width:1}.dt{fill:var(--t1)}'
           '.nt{fill:var(--t1);font-family:var(--oa-font-family-reading);font-size:0.8125rem;font-weight:600}'
           '.nt2{fill:var(--t2);font-family:var(--oa-font-family-reading);font-size:0.8125rem;font-weight:400}')
    figs['construction line px'] = {s: round(line_px(u_cap, s), 2) for s in (24, 48, 64, 96, 128)}
    ctx.spec('s-10-2-correct', f'<style>{css}</style>{svg}', CH, '10.2',
             'Local government drawn at three times its 128 px master on its 128-unit box, with a grid every 16 units. A '
             'dashed square marks the 116 units a drawing may fill, and a small cross marks the center at 64, 64. Notes '
             'point to the box, to the dashed square, to the left wall, whose line is 3.35 units wide with round ends and '
             'corners, and to the door, the one red part. Below, the same drawing at true size: 128 px with a 3.35 px '
             'line, 64 px with a 1.68 px line and 48 px with a 1.26 px line.',
             width=600, height=H, notes='The drawing is CL-031 from the sprite (D2-590); keylines from the construction file.')

    stock = ('<svg class="stk" viewBox="0 0 24 24" width="64" height="64" aria-hidden="true" focusable="false">'
             '<path fill-rule="evenodd" d="M4 1H15L20 6V23H4ZM7 10H17V12H7ZM7 14H17V16H7ZM7 18H13V20H7Z"/>'
             '<path class="fold" d="M15 1V6H20"/></svg>')
    items = [(sym('CL-048', 64), rows['CL-048']['label']), (sym('CL-071', 64), rows['CL-071']['label']),
             (stock, 'Bill'), (sym('CL-004', 64), rows['CL-004']['label'])]
    ul = ''.join(f'<li>{g}<span>{esc(w)}</span></li>' for g, w in items)
    css = (k.vars() + band_css + '.r{list-style:none;margin:0;padding:8px 0;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}'
           f'.r li{{display:flex;flex-direction:column;align-items:center;gap:8px;{t("ui")};font-weight:600;text-align:center}}'
           '.sym,.stk{display:block}.stk path{fill:var(--ink)}.stk .fold{fill:none;stroke:var(--oa-color-surface-newsprint);stroke-width:1.5}')
    ctx.spec('s-10-2-failure', f'<style>{css}</style>{band}<ul class="r">{ul}</ul>', CH, '10.2',
             'Labeled Failure case: do not publish. A row of four symbols at 64 px with their words: Public records, Policy, '
             'Bill and Petition. Bill is a filled stock document icon with square corners, solid black among three Civic '
             'Line line drawings.', width=480,
             notes='The stock glyph is drawn for this failure only, on a 24-unit grid; Bill has no Civic Line drawing (DR-137).')

    # ---------------------------------------------------------------- 10.3 capped fit
    trio = ['CL-067', 'CL-031', 'R-44']
    def cells3(trim):
        out = []
        for i in trio:
            e = inv[i]['extent_units']
            u = inv[i]['stroke_units']
            vb = f'{64 - e / 2:.3f} {64 - e / 2:.3f} {e:.3f} {e:.3f}' if trim else '0 0 128 128'
            lw = u * (128 / e if trim else 1) / 128 * 96
            out.append(f'<li><span class="bx">{sym(i, 96, vb=vb)}</span><span class="w">{esc(word(rows[i]))}</span>'
                       f'<span class="m">line {px2(round(lw, 2))} px</span></li>')
            figs.setdefault('fit', {})[f'{i} {"trimmed" if trim else "box"}'] = {'extent_units': e, 'stroke_units': u,
                                                                                  'line_px_at_96': round(lw, 2)}
        return ''.join(out)
    css3 = (k.vars() + '.r{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:24px}'
            '.r li{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center}'
            '.bx{display:block;outline:1px dashed var(--strong);outline-offset:0}.sym{display:block}'
            f'.w{{{t("ui")};font-weight:600;margin-top:6px}}.m{{{t("label")};color:var(--t2)}}')
    ctx.spec('s-10-3-correct', f'<style>{css3}</style><ul class="r">{cells3(False)}</ul>', CH, '10.3',
             f'Three drawings in 96 px boxes, each box outlined with a dashed line: {word(rows["CL-067"])}, compact, with '
             f'room around it and a 2.51 px line; {word(rows["CL-031"])}, with a 2.51 px line; and '
             f'{word(rows["R-44"])}, which fills the box across with a 2.01 px line. The lines look alike.',
             width=600, notes='Each box is the file\'s own 128-unit box (DR-08). Line widths from the inventory in use, '
                              'stroke_units times 96/128.')
    ctx.spec('s-10-3-failure', f'<style>{band_css}{css3}</style>{band}<ul class="r">{cells3(True)}</ul>', CH, '10.3',
             f'Labeled Failure case: do not publish. The same three drawings, each with its box trimmed to its ink and set '
             f'at 96 px. {word(rows["CL-067"])} grows to fill its box and its line thickens to 3.83 px; '
             f'{word(rows["CL-031"])} to 2.89 px; {word(rows["R-44"])} to 2.22 px. The three no longer match.',
             width=600, notes='The trim is a viewBox cut to each drawing\'s ink extent from the inventory in use '
                              '(extent_units, centered on 64, 64).')

    # ---------------------------------------------------------------- 10.4 sizes
    def ladder(i, sizes, gap24=False):
        out = []
        for s in sizes:
            out.append(f'<li><span class="hold">{sym(i, s)}</span><span class="m">{s} px</span>'
                       f'<span class="m2">line {px2(round(line_px(inv[i]["stroke_units"], s), 2))} px</span></li>')
        if gap24:
            out.append('<li><span class="hold"><span class="no"></span></span><span class="m">24 px</span>'
                       '<span class="m2">not on the list</span></li>')
        return ''.join(out)
    kick = (f'<div class="card"><p class="kick"><span>Explainer</span><span aria-hidden="true">{DOT}</span>'
            f'<span class="ki">{sym("CL-048", 24)}<span>{esc(rows["CL-048"]["label"])}</span></span></p>'
            f'<p class="hl">How to ask your town for its meeting minutes</p></div>')
    html = (f'<p class="sec">On the list of 41: {esc(rows["CL-048"]["label"])}</p><ul class="lad">{ladder("CL-048", (128, 96, 64, 48, 24))}</ul>'
            f'<p class="sec">Not on the list: {esc(rows["CL-025"]["label"])}</p><ul class="lad">{ladder("CL-025", (128, 96, 64, 48), True)}</ul>'
            f'<p class="sec">In a kicker, 24 px, one color, 8 px before its word</p>{kick}')
    css = (k.vars() + f'.sec{{margin:0 0 12px;{t("label")};color:var(--t2)}}.sec+.lad{{margin-bottom:28px}}'
           '.lad{list-style:none;margin:0 0 28px;padding:0;display:flex;align-items:flex-end;gap:28px;flex-wrap:wrap}'
           '.lad li{display:flex;flex-direction:column;align-items:flex-start;gap:4px}'
           '.hold{display:flex;align-items:flex-end;height:128px}.sym{display:block}'
           '.no{display:block;width:24px;height:24px;outline:1px dashed var(--strong)}'
           f'.m{{{t("label")};font-variant-numeric:tabular-nums}}.m2{{{t("label")};color:var(--t2);font-variant-numeric:tabular-nums}}'
           '.card{padding:16px;border:1px solid var(--hair);max-width:360px;box-sizing:border-box}'
           f'.kick{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 8px;{t("label")};text-transform:uppercase}}'
           '.ki{display:inline-flex;align-items:center;gap:8px}'
           f'.hl{{margin:0;{t("h4")}}}')
    ctx.spec('s-10-4-correct', f'<style>{css}</style>{html}', CH, '10.4',
             f'Two size ladders and a kicker at true size. {rows["CL-048"]["label"]}, which is on the list of 41, at 128, '
             f'96, 64, 48 and 24 px, with lines of 3.35, 2.51, 1.68, 1.26 and 0.63 px. {rows["CL-025"]["label"]}, which is '
             f'not on the list, at 128, 96, 64 and 48 px, and an empty dashed square where 24 px would be. Below, a story '
             f'card whose kicker reads Explainer, then the {rows["CL-048"]["label"]} drawing at 24 px directly before the '
             f'words {rows["CL-048"]["label"]}, over the headline How to ask your town for its meeting minutes.',
             width=600, illustrative=False,
             notes='Ladder sizes on whole pixels; CL-048 is on the list of 41 (construction file, section 10). The '
                   'headline is a service line, not an invented fact.')
    menu = ['CL-001', 'CL-005', 'CL-031', 'CL-067', 'CL-068', 'CL-069']
    li = ''.join(f'<li>{sym(i, 16)}<span>{esc(rows[i]["label"])}</span></li>' for i in menu)
    css = (k.vars() + band_css + f'.mn{{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}}'
           f'.mn li{{display:flex;align-items:center;gap:8px;min-height:44px;border-bottom:1px solid var(--hair);{t("ui")}}}'
           '.sym{display:block;flex:none}' f'.tt{{margin:0 0 8px;{t("label")};color:var(--t2);text-transform:uppercase}}')
    ctx.spec('s-10-4-failure', f'<style>{css}</style>{band}<p class="tt">Topics</p><ul class="mn">{li}</ul>', CH, '10.4',
             'Labeled Failure case: do not publish. A topics menu at 360 px with a Civic Line drawing at 16 px before each '
             f'word: {", ".join(rows[i]["label"] for i in menu)}. At 16 px each drawing is a gray smudge, and no two can '
             'be told apart.', width=360, notes='Topic symbols at 16 px, which no topic or atlas symbol takes (DR-136).')

    # extra after 10.4: the 41
    topics41 = [i for i in reads24 if i not in PILLARS]
    li = ''.join(f'<li>{sym(i, 24, fam=family(rows[i]))}<span class="w">{esc(word(rows[i]))}</span><span class="id">{esc(i)}</span></li>'
                 for i in topics41)
    pil = ', '.join(f'{i} {rows[i]["label"]}' for i in PILLARS)
    html = (f'<ul class="l41">{li}</ul><p class="nt">The other four on the list are the pillar icons, {esc(pil)}. At '
            f'24 px they take chapter 09’s own drawings.</p>')
    css = (k.vars() + '.l41{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(176px,1fr));gap:0 16px}'
           f'.l41 li{{display:grid;grid-template-columns:24px minmax(0,1fr) auto;align-items:center;gap:8px;min-height:44px;'
           f'border-bottom:1px solid var(--hair)}}.sym{{display:block}}'
           f'.w{{{t("bodySmall")}}}.id{{{t("label")};color:var(--t2);font-variant-numeric:tabular-nums}}'
           f'.nt{{margin:16px 0 0;{t("bodySmall")};color:var(--t1)}}')
    ctx.spec('s-10-list-41', f'<style>{css}</style>{html}', CH, None,
             'The 37 topic and atlas drawings that may be set at 24 px, each at 24 px in one color with its word and ID: '
             + '; '.join(f'{word(rows[i])}, {i}' for i in topics41)
             + f'. The other four on the list are the pillar icons, {pil}, which take chapter 09’s own drawings at 24 px.',
             width=600, readable=True, notes='The list of 41 from the construction file, section 10 (DR-136, D2-587).')

    # ---------------------------------------------------------------- 10.5 editions and tiles
    eds = [('newsprint', 'Red-Black', True, 'On Newsprint'), ('white', 'Black', False, 'On White'),
           ('charcoal', 'Red-Newsprint', True, 'On Charcoal'), ('prussian', 'Newsprint', False, 'On Prussian')]
    panels = ''.join(
        f'<li class="pn" style="background:var(--oa-color-surface-{s});color:var(--oa-color-text-primary-on-{s})">'
        f'{sym("CL-031", 96, surface=s, two=two)}<span class="w">{esc(ed)}</span>'
        f'<span class="m" style="color:var(--oa-color-text-secondary-on-{s})">{esc(on)}</span></li>' for s, ed, two, on in eds)
    rounded = re.search(r'data-part="tile" d="([^"]+)"', TILE_ROUNDED.read_text()).group(1)
    shapes = [('square', 'Square', 0.68, f'<rect width="128" height="128"/>', 72),
              ('rounded', 'Rounded square', 0.66, f'<path d="{rounded}"/>', 76),
              ('circle', 'Circle', 0.62, '<circle cx="64" cy="64" r="64"/>', 80)]
    tiles = []
    for ground, ink_s in (('charcoal', 'charcoal'), ('newsprint', 'newsprint')):
        for key, name, f, shape, mn in shapes:
            o = 64 * (1 - f)
            tiles.append(
                f'<li><svg class="tile" viewBox="0 0 128 128" width="80" height="80" aria-hidden="true" focusable="false" '
                f'data-icon="CL-031" data-icon-family="topic"><g style="fill:var(--oa-color-surface-{ground})">{shape}</g>'
                f'<use href="#oa-sym-cl-031" width="128" height="128" transform="matrix({f} 0 0 {f} {o:.2f} {o:.2f})" '
                f'style="color:var(--oa-component-icon-ink-on-{ink_s});--oa-icon-accent:var(--oa-component-icon-accent-on-{ink_s})"/>'
                f'</svg><span class="w">{esc(name)}, {ground.capitalize()}</span><span class="m">two-color from {mn} px</span></li>')
    html = (f'<p class="sec">Four editions, one drawing</p><ul class="eds">{panels}</ul>'
            f'<p class="sec">Six tiles, two-color, at 80 px</p><ul class="tl">{"".join(tiles)}</ul>'
            f'<p class="nt">Charcoal is the default tile for the app icon and avatars.</p>')
    css = (k.vars() + f'.sec{{margin:0 0 12px;{t("label")};color:var(--t2)}}'
           '.eds{list-style:none;margin:0 0 28px;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}'
           '.pn{display:flex;flex-direction:column;align-items:center;gap:4px;padding:16px 8px 14px;box-shadow:inset 0 0 0 1px var(--hair)}'
           '.sym,.tile{display:block}'
           f'.w{{{t("caption")};font-weight:600;text-align:center}}.m{{{t("label")};color:var(--t2);text-align:center}}'
           '.tl{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:20px 16px}'
           '.tl li{display:flex;flex-direction:column;align-items:center;gap:4px}'
           f'.nt{{margin:16px 0 0;{t("bodySmall")}}}')
    ctx.spec('s-10-5-correct', f'<style>{css}</style>{html}', CH, '10.5',
             f'{word(rows["CL-031"])} in its four editions at 96 px, each on its own surface: Red-Black on Newsprint, with '
             'the door in red; Black on White; Red-Newsprint on Charcoal, with Newsprint lines and a red door; Newsprint '
             'alone on Prussian, with no red. Below, the six tiles at 80 px, all two-color: square, rounded square and '
             'circle on Charcoal with Newsprint lines, then the same three on Newsprint with Charcoal lines, each with its '
             'two-color minimum of 72, 76 or 80 px. A note says Charcoal is the default tile for the app icon and avatars.',
             width=600, notes='Tile factors 0.68, 0.66 and 0.62 (D2-40); CL-031 takes optical scale 1.0 and no offset '
                              '(inventory in use). The rounded outline is read from the October tile file (D2-41).')
    css = (k.vars() + band_css + '.pn{display:flex;align-items:center;gap:16px;padding:16px;background:var(--oa-color-surface-prussian);'
           'color:var(--oa-color-text-primary-on-prussian)}.sym{display:block}'
           f'.w{{{t("ui")};font-weight:600}}')
    ctx.spec('s-10-5-failure', f'<style>{css}</style>{band}<div class="pn">'
             f'{sym("CL-031", 96, surface="prussian", two=True, accent="var(--oa-color-palette-pillar-red)")}'
             f'<span class="w">{esc(word(rows["CL-031"]))}</span></div>', CH, '10.5',
             f'Labeled Failure case: do not publish. {word(rows["CL-031"])} in its Red-Newsprint edition on a Prussian '
             'panel at 96 px, with Newsprint lines and a Pillar Red door.',
             width=360, exempt=['red'], notes='Labeled failure: red on Prussian, which Rule 05.3 never allows.')

    # ---------------------------------------------------------------- 10.6 words
    pairs6 = [
        ('CL-025', False, 'As a topic, in a story’s subject line'),
        ('CL-025', True, 'In the atlas, where it stands for the variable'),
        ('R-13', False, 'A reform, in its short form'),
        ('CL-056', False, 'An atlas variable, under the atlas’s full name'),
        ('R-36', False, 'A reform with a similar subject, kept apart by its own name'),
        ('R-35', False, 'The rejected option keeps the word Rejected'),
    ]
    li = []
    for i, atl, where in pairs6:
        r = rows[i]
        chip = f'<span class="chip">{esc(r["v7_chip"])}</span>' if (atl or i.startswith('R-') or r['class'] == 'atlas variable') and r.get('v7_chip') else ''
        li.append(f'<li>{sym(i, 64, fam=family(r, atl))}<div><p class="w">{esc(word(r, atl))}</p>{chip}'
                  f'<p class="m">{esc(where)}</p></div></li>')
    css = (k.vars() + chip_css + '.l{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(272px,1fr));gap:0 24px}'
           '.l li{display:grid;grid-template-columns:64px minmax(0,1fr);gap:16px;align-items:center;padding:14px 0;border-bottom:1px solid var(--hair)}'
           f'.sym{{display:block}}.w{{margin:0 0 4px;{t("ui")};font-weight:700}}.m{{margin:6px 0 0;{t("caption")};color:var(--t2)}}')
    ctx.spec('s-10-6-correct', f'<style>{css}</style><ul class="l">{"".join(li)}</ul>', CH, '10.6',
             'Six symbols at 64 px, each with its word and, for an atlas element, its typed chip. '
             + ' '.join(f'{word(rows[i], a)}{", " + rows[i]["v7_chip"] if ((a or i.startswith("R-") or rows[i]["class"] == "atlas variable") and rows[i].get("v7_chip")) else ""}: {w}.'
                        for i, a, w in pairs6),
             width=600, readable=True, notes='Every word from the editor\'s label table (DR-185).')
    four = ['CL-053', 'CL-054', 'CL-063', 'CL-061']
    css = (k.vars() + band_css + '.r{list-style:none;margin:0;padding:8px 0;display:flex;justify-content:space-between}.sym{display:block}')
    ctx.spec('s-10-6-failure', f'<style>{css}</style>{band}<ul class="r">'
             + ''.join(f'<li>{sym(i, 64, fam=family(rows[i]))}</li>' for i in four) + '</ul>', CH, '10.6',
             'Labeled Failure case: do not publish. Four Civic Line drawings at 64 px in a row with no words: three '
             'houses with different marks and a person sending an envelope along an arrow.', width=360,
             notes=f'The drawings are {", ".join(four)}.')

    # ---------------------------------------------------------------- 10.7 red
    act = ['CL-001', 'CL-004', 'CL-005', 'CL-073', 'CL-074']
    cur = 'CL-073'
    def menu7(all_red):
        out = []
        for i in act:
            on = i == cur
            out.append(f'<li class="{"on" if on else ""}">{sym(i, 48, two=(on or all_red))}'
                       f'<span class="w">{esc(rows[i]["label"])}</span></li>')
        return f'<ul class="mn">{"".join(out)}</ul>'
    css7 = (k.vars() + '.mn{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,1fr);gap:8px}'
            '.mn li{display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center;padding:8px 0}'
            f'.w{{{t("caption")}}}.on .w{{font-weight:700;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}}'
            '.sym{display:block}' f'.sec{{margin:0 0 12px;{t("label")};color:var(--t2)}}'
            '.solo{display:flex;align-items:center;gap:24px;margin:0;padding:16px 0 0;border-top:1px solid var(--hair)}'
            f'.solo p{{margin:0;{t("h4")}}}')
    html = (f'<p class="sec">In a menu: one color, the current item in red</p>{menu7(False)}'
            f'<p class="sec" style="margin-top:28px">Standing alone at 128 px: red, bare on Newsprint</p>'
            f'<div class="solo">{sym(cur, 128, two=True)}<p>{esc(rows[cur]["label"])}</p></div>')
    ctx.spec('s-10-7-correct', f'<style>{css7}</style>{html}', CH, '10.7',
             'A menu of five symbols at 48 px with their words: ' + ', '.join(rows[i]['label'] for i in act)
             + f'. All are one color except {rows[cur]["label"]}, the current item, whose microphone is red and whose word '
             f'is bold and underlined. Below, {rows[cur]["label"]} alone at 128 px with its red microphone, bare on '
             'Newsprint, beside its word.', width=600, notes='Rule 05.3 as DR-66 words it; R11.')
    ctx.spec('s-10-7-failure', f'<style>{band_css}{css7}</style>{band}{menu7(True)}', CH, '10.7',
             'Labeled Failure case: do not publish. The same menu with every drawing keeping its red part: the ballot, the '
             'pen, the speaker, the microphone and the speech mark all in red, so the current item, '
             f'{rows[cur]["label"]}, no longer stands out.', width=600,
             notes='Labeled failure: five red accents in one row.')

    # ---------------------------------------------------------------- 10.8 atlas scope
    dom = next(d for d in v7['domains'] if d['id'] == 'D02')
    dvars = [k_ for k_, v in v7['nodes'].items() if v['domain'] == 'D02']
    var_icon = {r['v7_id']: i for i, r in rows.items() if r['class'] in ('atlas variable', 'topic and atlas variable')}
    reforms = [rid for rid, r in v7['reforms'].items() if set(r.get('targets', [])) & set(dvars)][:2]
    li = []
    for v in dvars:
        i = var_icon[v]
        li.append(f'<li>{sym(i, 48, fam="atlas")}<div><span class="chip">{esc(rows[i]["v7_chip"])}</span>'
                  f'<p class="w">{esc(word(rows[i], True))}</p></div></li>')
    lr = [f'<li>{sym(rid, 48, fam="atlas")}<div><span class="chip">{esc(rows[rid]["v7_chip"])}</span>'
          f'<p class="w">{esc(rows[rid]["label"])}</p></div></li>' for rid in reforms]
    figs['atlas domain D02'] = {'variables': dvars, 'reforms_acting': reforms}
    html = (f'<div class="dm"><span class="chip">Domain {dom["id"]}</span><p class="dn">{esc(dom["title"])}</p></div>'
            f'<p class="sec">Variables in this domain</p><ul class="vl">{"".join(li)}</ul>'
            f'<p class="sec">Reforms that act on them</p><ul class="vl">{"".join(lr)}</ul>')
    css8 = (k.vars() + chip_css + '.dm{padding:0 0 16px;margin:0 0 16px;border-bottom:2px solid var(--strong)}'
            f'.dn{{margin:8px 0 0;{t("h4")}}}' f'.sec{{margin:0 0 4px;{t("label")};color:var(--t2)}}'
            '.vl{list-style:none;margin:0 0 20px;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(272px,1fr));gap:0 24px}'
            '.vl li{display:grid;grid-template-columns:48px minmax(0,1fr);gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid var(--hair)}'
            f'.sym{{display:block}}.w{{margin:4px 0 0;{t("bodySmall")};font-weight:600}}')
    ctx.spec('s-10-8-correct', f'<style>{css8}</style>{html}', CH, '10.8',
             f'An atlas list for Domain {dom["id"]}, {dom["title"]}, shown as a typed chip and its name in words, with no '
             'drawing. Under it, the domain’s variables, each with its drawing at 48 px, its chip and its name: '
             + '; '.join(f'{rows[var_icon[v]]["v7_chip"]}, {word(rows[var_icon[v]], True)}' for v in dvars)
             + '. Then the reforms that act on them: ' + '; '.join(f'{rows[r]["v7_chip"]}, {rows[r]["label"]}' for r in reforms) + '.',
             width=600, readable=True,
             notes='Domain membership and reform targets read from the atlas model (work/extract/atlas-v7-data.json).')
    borrowed = [('D02', 'CL-001'), ('D03', 'CL-015'), ('D04', 'CL-025')]
    li = []
    for did, i in borrowed:
        d = next(x for x in v7['domains'] if x['id'] == did)
        li.append(f'<li>{sym(i, 48, fam="topic")}<div><span class="chip">Domain {did}</span><p class="w">{esc(d["title"])}</p></div></li>')
    ctx.spec('s-10-8-failure', f'<style>{band_css}{css8}</style>{band}<ul class="vl">{"".join(li)}</ul>', CH, '10.8',
             'Labeled Failure case: do not publish. A list of three atlas domains, each given a borrowed topic drawing at '
             '48 px: ' + '; '.join(f'Domain {did}, {next(x for x in v7["domains"] if x["id"] == did)["title"]}, with the '
                                   f'{rows[i]["label"]} drawing' for did, i in borrowed) + '.',
             width=360, notes='Domains stay words and typed chips (round 2 brief).')

    # ---------------------------------------------------------------- 10.9 look-alikes
    groups = []
    for grp, look in LOOKALIKES:
        figs_g = []
        for a in range(len(grp)):
            for b in range(a + 1, len(grp)):
                key = '|'.join(sorted((grp[a], grp[b])))
                v = like['pairs'][key]['likeness']
                figs_g.append(f'{word(rows[grp[a]])} and {word(rows[grp[b]])}: {v:.2f}')
        cells = ''.join(f'<div class="c">{sym(i, 64, fam=family(rows[i]))}<span class="w">{esc(word(rows[i]))}</span>'
                        f'<span class="id">{esc(i)}</span></div>' for i in grp)
        groups.append(f'<li><div class="cs">{cells}</div><div class="tx"><p class="lk">{esc(look)}</p>'
                      f'<p class="fg">Likeness at 24 px: {esc("; ".join(figs_g))}</p></div></li>')
    css = (k.vars() + '.l{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}'
           '.l li{display:grid;grid-template-columns:minmax(0,1fr);gap:10px;padding:16px 0;border-bottom:1px solid var(--hair)}'
           '.cs{display:flex;gap:16px;flex-wrap:wrap}.c{display:flex;flex-direction:column;align-items:center;gap:4px;width:120px;text-align:center}'
           f'.sym{{display:block}}.w{{{t("caption")};font-weight:600}}.id{{{t("label")};color:var(--t2)}}'
           f'.lk{{margin:0;{t("bodySmall")}}}.fg{{margin:4px 0 0;{t("caption")};color:var(--t2);font-variant-numeric:tabular-nums}}')
    ctx.spec('s-10-9-correct', f'<style>{css}</style><ul class="l">{"".join(groups)}</ul>', CH, '10.9',
             'Six groups of look-alike symbols, each at 64 px with its word and ID, then what tells them apart and their '
             'likeness at 24 px. ' + ' '.join(
                 f'{" and ".join(word(rows[i]) for i in grp)}: {look}' for grp, look in LOOKALIKES),
             width=600, readable=True,
             notes=f'Likeness from the engineer\'s icon_likeness_check.js, run on the civic-line-v6 Black files as new '
                   f'drawings (flag {like["thresholds"]["flag"]["likeness"]}, watch {like["thresholds"]["watch"]["likeness"]}).')
    card = (f'{band}<div class="card">{ILLUS}<p class="kick">Act</p><div class="hd">{sym("CL-005", 64)}'
            f'<span class="w">{esc(rows["CL-005"]["label"])}</span></div>'
            f'<p class="hl">Testify on the library budget at the March 10 hearing</p>'
            f'<p class="tx">Sign up at the clerk’s table by 6:30 p.m. Each speaker gets three minutes before the '
            f'council’s budget committee.</p></div>')
    css = (k.vars() + band_css + '.card{padding:16px;border:1px solid var(--hair)}'
           f'.kick{{margin:8px 0;{t("label")};text-transform:uppercase}}'
           '.hd{display:flex;align-items:center;gap:12px;margin:0 0 8px}.sym{display:block}'
           f'.w{{{t("ui")};font-weight:600}}.hl{{margin:0 0 8px;{t("h4")}}}.tx{{margin:0;{t("bodySmall")}}}')
    ctx.spec('s-10-9-failure', f'<style>{css}</style>{card}', CH, '10.9',
             'Labeled Failure case: do not publish. An Illustrative Act card at 360 px headed Testify on the library budget '
             f'at the March 10 hearing, with the {rows["CL-005"]["label"]} drawing at 64 px and its word: one speaker at a '
             'lectern facing an audience. The card asks readers to sign up to speak to the council’s budget committee.',
             width=360, illustrative=True, notes='Illustrative: the hearing, its date and its committee are invented.')

    # ---------------------------------------------------------------- 10.10 encoding glyphs
    def line(grade='documented', sign=None, delay=None, authority=False, W=176, target=False):
        marks = S1.wire_marks([(4, 16), (W - 4, 16)], grade, sign, delay, 2, lit=target, authority=authority)[0]
        cls = 'wire target' if target else 'wire'
        red = ' data-red="working" data-red-job="where a reform acts"' if target else ''
        return (f'<svg class="gx" viewBox="0 0 {W} 32" width="{W}" height="32" aria-hidden="true" focusable="false" '
                f'data-icon="E-{grade}-{sign or ("authority" if authority else "none")}{"-" + delay if delay else ""}'
                f'{"-target" if target else ""}" data-icon-family="encoding"><g class="{cls}"{red}>{marks}</g></svg>')
    G = S1.acc.GRADES
    rows10 = [
        ('Sign', line(sign='+'), 'raises', 'The two conditions move the same way. A plus sign does not mean the change is good.'),
        ('Sign', line(sign='-'), 'lowers', 'They move opposite ways.'),
        ('Authority', line(authority=True), 'decides', 'A line of authority ends in an open diamond and carries no sign.'),
    ] + [('Evidence', line(grade=g), G[g][0], f'{G[g][1][0].upper() + G[g][1][1:]}.') for g in
         ('documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis')] + [
        ('Delay', line(delay=d), S1.acc.DELAYS[d], f'{n} tick{"s" if n > 1 else ""} after the tail.')
        for d, n in (('S', 1), ('M', 2), ('L', 3))] + [
        ('Where a reform acts', line(sign='+', target=True), 'Reform acts here',
         'The line and its head turn Pillar Red at a heavier weight, on the loop and reform pages only.'),
    ]
    li = ''.join(f'<li><p class="k">{esc(a)}</p>{g}<div><p class="w">{esc(w)}</p><p class="m">{esc(m)}</p></div></li>'
                 for a, g, w, m in rows10)
    css = (k.vars('white') + '.l{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}'
           '.l li{display:grid;grid-template-columns:96px 176px minmax(0,1fr);gap:16px;align-items:center;padding:10px 0;'
           'border-bottom:1px solid var(--hair)}'
           f'.k{{margin:0;{t("label")};color:var(--t2)}}.w{{margin:0;{t("ui")};font-weight:700}}.m{{margin:2px 0 0;{t("caption")}}}'
           '.gx{display:block;color:var(--oa-component-icon-ink-on-white)}'
           f'.nt{{margin:14px 0 0;{t("bodySmall")}}}'
           '@media (max-width:47.99em){.l li{grid-template-columns:minmax(0,1fr)}}' + S1_CSS +
           '.target .lo{display:none}.target .hi{display:inline}'
           '.target .ak-mark{stroke:var(--red);stroke-width:4px;stroke-dasharray:var(--d6,none)}.target .hd{fill:var(--red)}')
    html = (f'<ul class="l">{li}</ul><p class="nt">Loops carry their type in their ID and in words: loop R10 feeds '
            f'itself, and loop B4 pushes back.</p>')
    ctx.spec('s-10-10-correct', f'<style>{css}</style>{html}', CH, '10.10',
             'The atlas’s encoding glyphs on White, each drawn on a short line with its words. Sign: a tag with a plus '
             'sign, raises, the two move the same way; a tag with a minus sign, lowers. Authority: an open diamond at the '
             'tip, decides, with no sign. Evidence: Documented and Well supported as solid lines, Plausible dashed, '
             'Contested dash and dot, Hypothesis dotted. Delay: one tick for under 2 years, two for 2 to 10 years, three '
             'for over 10 years. Where a reform acts: the line and its arrowhead in Pillar Red at a heavier weight. A '
             'note says loops carry their type in their ID and in words.',
             width=600, readable=True, surface='white',
             notes='Drawn with System 1\'s own wire_marks, ARROW, TAG, BEND and textures (DR-36), on White as System 1 is; '
                   'red on White measures 4.17 to 1 and takes no keyline there.')
    fail = (f'{band}<p class="t">Effects in this loop</p><svg class="gx" viewBox="0 0 360 120" width="360" height="120" '
            f'aria-hidden="true" focusable="false"><path class="up" d="M8 30H340"/><path class="dn" d="M8 90H340"/>'
            f'<path class="hu" d="M340 24L352 30L340 36Z"/><path class="hdn" d="M340 84L352 90L340 96Z"/></svg>')
    css = (k.vars('white') + band_css + f'.t{{margin:0 0 8px;{t("label")};color:var(--t2)}}.gx{{display:block}}'
           '.up{stroke:var(--oa-color-palette-verdigris);stroke-width:4}.dn{stroke:var(--red);stroke-width:4}'
           '.hu{fill:var(--oa-color-palette-verdigris)}.hdn{fill:var(--red)}')
    ctx.spec('s-10-10-failure', f'<style>{css}</style>{fail}', CH, '10.10',
             'Labeled Failure case: do not publish. Two connections drawn on White with no tags and no words: a green line '
             'for raises and a red line for lowers. The sign lives in color alone, and red means something it never means '
             'in the atlas.', width=360, surface='white', exempt=['red'],
             notes='Labeled failure: polarity by hue, with red spent on a sign.')


# System 1's own rules for the marks wire_marks draws (build_system.py CSS, lines for .wire), with its White replaced by
# the White token
S1_CSS = ('.wire{color:var(--oa-component-icon-ink-on-white)}.wire .ak-case{stroke:none}'
          '.wire .ak-mark{stroke:var(--ak-hi,currentColor)}.wire .hd{fill:var(--ak-hi,currentColor)}'
          '.wire .tg polygon{fill:currentColor}.wire .tg .sg{fill:var(--oa-color-surface-white)}'
          '.wire .tk{stroke:currentColor;stroke-width:2px}'
          '.wire .dm{fill:var(--oa-color-surface-white);stroke:var(--ak-hi,currentColor);stroke-width:2px}'
          '.wire .hi{display:none}')


# ------------------------------------------------------------------------------------------------ the chapter
def chapter(rows, reads24, like, sheets, figs):
    from stage_b_ch10_copy import build_chapter
    return build_chapter(rows, reads24, like, sheets, figs, CATEGORIES, LOOKALIKES, PILLARS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-draw', action='store_true', help='reuse the sheets and the likeness figures already written')
    a = ap.parse_args()
    icons, black, rows, reads24, v7 = load_inputs()
    T = C.Tokens(C.TOKENS_JSON, C.TOKENS_CSS)
    ctx = B.Ctx(T, {}, 'final')
    figs = {}
    if a.no_draw and FIG_OUT.exists():
        old = json.loads(FIG_OUT.read_text())
        sheets, like = old['sheets'], old['likeness']
    else:
        with tempfile.TemporaryDirectory() as td:
            tmp = pathlib.Path(td)
            sheets = draw_sheets(icons, black, tmp)
            like = measure_likeness(black, tmp)
    specimens(ctx, icons, rows, reads24, v7, sheets, like, figs)
    ch = chapter(rows, reads24, like, sheets, figs)
    B.check_chapter(ch)
    used = set()
    for r in ch['rules']:
        for kk in ('correct', 'failure', 'corrective'):
            if r.get(kk):
                used.add(r[kk]['specimen'])
    for x in ch.get('extras', []):
        used.add(x['specimen'])
    missing, unused = used - set(ctx.specs), set(ctx.specs) - used
    if missing or unused:
        raise SystemExit(f'specimens missing {sorted(missing)} unused {sorted(unused)}')
    OUT_CH.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + '\n')
    for old in OUT_SP.glob('s-10-*.html'):
        if old.stem not in ctx.specs:
            old.unlink()
    for sid, s in ctx.specs.items():
        (OUT_SP / f'{sid}.html').write_text(s['html'])
    man = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    man = {kk: v for kk, v in man.items() if str(v.get('chapter')) != CH}
    man.update({sid: s['meta'] for sid, s in ctx.specs.items()})
    MANIFEST.write_text(json.dumps(dict(sorted(man.items())), indent=1, ensure_ascii=False) + '\n')
    FIG_OUT.write_text(json.dumps({
        'about': 'Every figure chapter 10 prints, with how it was measured. Contrast is WCAG 2.x relative luminance on the '
                 'token values in tokens.json; line widths are each file\'s stroke_units in the inventory in use times the '
                 'size over 128; likeness is the engineer\'s icon_likeness_check.js run on the Black files in use.',
        'built': '2026-11-10', 'sheets': sheets, 'likeness': like, 'figures': {**figs, **ctx.figures},
    }, indent=1, ensure_ascii=False, default=str) + '\n')
    print(f'chapter 10: {len(ch["rules"])} rules, {len(ctx.specs)} specimens, {len(sheets)} sheets '
          f'({sum(s["bytes"] for s in sheets.values()):,} bytes)')


if __name__ == '__main__':
    main()
