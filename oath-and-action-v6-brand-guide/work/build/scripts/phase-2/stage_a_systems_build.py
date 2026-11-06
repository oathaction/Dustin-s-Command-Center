"""Stage board A: chapters 05 Color, 06 Type and 07 Layout and spacing, written by the systems designer.

Writes, from the content in stage_a_systems_ch05.py, _ch06.py and _ch07.py:
  work/build/guide/chapters/05-color.json, 06-type.json, 07-layout.json   (Stage A brief, content contract)
  work/build/guide/specimens/s-05-*.html, s-06-*.html, s-07-*.html         one fragment per specimen
  work/build/guide/specimens/manifest-systems.json
  work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json         every figure the chapters print, with how
                                                                           it was measured

Two stages, because some figures come from the rendered page (characters per line, a page's color shares, word-space
widths, the width a headline takes in its fallback face):
  1. python3 -I work/build/scripts/phase-2/stage_a_systems_build.py probe --out-dir <scratch>
       writes probe pages (tokens.css and Google Fonts, as the guide page loads them)
  2. node work/build/scripts/phase-2/stage_a_systems_capture.js <scratch>
       renders them in Chromium and writes <scratch>/results.json and screenshots
  3. python3 -I work/build/scripts/phase-2/stage_a_systems_build.py final --out-dir <scratch>
       reads the results and writes the files above

Contrast, OKLab and color-vision figures are computed here from work/build/tokens/tokens.json (never edited).
"""
import argparse
import importlib.util
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


C = _load('stage_a_systems_core')
ROOT = C.ROOT
OUT_CH = ROOT / 'work/build/guide/chapters'
OUT_SP = ROOT / 'work/build/guide/specimens'
MEAS_OUT = ROOT / 'work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json'
FONTS = ('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@800'
         '&family=Lora:ital,wght@1,400;1,500&display=swap')

# Display styles grow with the window; every other style holds one size (tokens.json oa.type).
FLUID = ('title', 'section', 'h3', 'h4', 'quote', 'intro', 'figure')
# D2-254: fixed artboards up to 600 px take each style's phone floor; 1,200 px and wider, its desktop ceiling.
ARTBOARD_FLOOR = {'title': 56, 'section': 44, 'figure': 48, 'h3': 26, 'h4': 20, 'quote': 24, 'intro': 19, 'ask': 19,
                  'body': 17, 'bodySmall': 15, 'ui': 15, 'caption': 14, 'label': 13, 'dataLabel': 13}
ARTBOARD_CEIL = dict(ARTBOARD_FLOOR, title=110, section=80, figure=104, h3=32, h4=24, quote=32, intro=22)
# DR-95: display tracking, in em
TRACKING_DR95 = {'title': -0.03, 'section': -0.025, 'h3': -0.01, 'h4': -0.005}
# Classes the shell styles on purpose inside a specimen: the one Illustrative label (DR-97)
SHELL_CLASSES = ('illus',)
ILLUS = '<span class="illus">Illustrative</span>'
FAIL_BAND = ('<div class="fb" aria-hidden="true"><span>×</span> Failure case: do not publish</div>')


class Ctx:
    """What every content module needs: token values, measured figures and the specimen register."""

    def __init__(self, tokens, results, stage):
        self.T = tokens
        self.R = results or {}
        self.stage = stage
        self.specs = {}
        self.figures = {}          # every printed figure: key -> {value, method}
        self.probes = {}           # measurement requests for the capture script
        self.need = set()

    # tokens --------------------------------------------------------------------------------------------------
    def v(self, path):
        return self.T.var(path)

    def hx(self, path):
        return self.T.hex(path)

    def cssv(self, name):
        if name not in self.T.css_names:
            raise KeyError(f'{name} is not in tokens.css')
        return f'var({name})'

    def ty(self, name, fixed=None):
        """A type style as CSS declarations: the shorthand and the parts the shorthand cannot carry.

        Display styles grow with the window on a web page, but a specimen is a fixed artboard or a sheet, so its size
        comes from the scale's fixed sizes (D2-254): fixed='floor' or 'ceil' writes that size; otherwise the size is
        var(--sx-fs-NAME), which spec() sets for the specimen's width (the phone floor by default)."""
        k = C.css_name('oa.type.' + name)
        for suf in ('', '-letter-spacing', '-text-transform', '-font-variant-numeric'):
            self.cssv(k + suf)
        self.T.used.add('oa.type.' + name)
        out = (f'font:var({k});letter-spacing:var({k}-letter-spacing);text-transform:var({k}-text-transform);'
               f'font-variant-numeric:var({k}-font-variant-numeric)')
        if name in FLUID:
            lo, hi = self.fixed_px(name)
            if fixed == 'floor':
                out += f';font-size:{lo / 16:g}rem'
            elif fixed == 'ceil':
                out += f';font-size:{hi / 16:g}rem'
            else:
                out += f';font-size:var(--sx-fs-{name},{lo / 16:g}rem)'
        return out

    def fixed_px(self, name):
        """The style's phone floor and desktop ceiling in px, read from tokens.json and checked against D2-254."""
        node = self.T.node(f'oa.type.{name}')
        fs = node['$value']['fontSize']
        hi = fs['value'] * 16 if fs['unit'] == 'rem' else fs['value']
        lo = self.T.ext(f'oa.type.{name}').get('minFontSize', {}).get('value')
        lo = lo * 16 if lo else hi
        if (round(lo), round(hi)) != (ARTBOARD_FLOOR[name], ARTBOARD_CEIL[name]):
            raise ValueError(f'oa.type.{name} runs {lo:g} to {hi:g} px in tokens.json; D2-254 prints '
                             f'{ARTBOARD_FLOOR[name]} and {ARTBOARD_CEIL[name]}')
        return lo, hi

    def fs_vars(self, mode):
        """Custom properties that size every display style in a specimen: 'floor', 'ceil' or 'sheet' (floor on
        phones, ceiling from 48em, so every size a reader sees is one of the scale's fixed sizes)."""
        lo = ';'.join(f'--sx-fs-{n}:{self.fixed_px(n)[0] / 16:g}rem' for n in FLUID)
        hi = ';'.join(f'--sx-fs-{n}:{self.fixed_px(n)[1] / 16:g}rem' for n in FLUID)
        if mode == 'floor':
            return f':scope{{{lo}}}'
        if mode == 'ceil':
            return f':scope{{{hi}}}'
        return f':scope{{{lo}}}@media (min-width:48em){{:scope{{{hi}}}}}'

    def fail_band(self):
        """A band inside a failure stage, so a cropped picture of it still says not to publish it (BE-S4)."""
        css = (f'.fb{{display:flex;align-items:center;gap:8px;margin:0 0 16px;padding:6px 12px;'
               f'background:{self.v("oa.color.surface.charcoal")};color:{self.v("oa.color.text.primary.onCharcoal")};'
               f'{self.ty("label")}}}')
        return css, FAIL_BAND

    def ratio(self, fg, bg, key=None):
        """Contrast of two token paths (or hex values), printed to two decimals and recorded."""
        a = fg if fg.startswith('#') else self.hx(fg)
        b = bg if bg.startswith('#') else self.hx(bg)
        txt = C.ratio_txt(a, b)
        k = key or f'contrast {fg} on {bg}'
        self.figures[k] = {'value': txt, 'fg': a, 'bg': b, 'exact': round(C.contrast(a, b), 4),
                           'method': 'WCAG 2.x relative luminance on the token hex values in tokens.json'}
        return txt

    def fig(self, key, value, method):
        self.figures[key] = {'value': value, 'method': method}
        return value

    # rendered measurements -----------------------------------------------------------------------------------
    def probe(self, key, kind, **spec):
        self.probes[key] = dict(kind=kind, **spec)

    def m(self, key):
        """A rendered measurement; in the probe stage a placeholder that the build never ships."""
        if key in self.R:
            return self.R[key]
        if self.stage == 'final':
            raise KeyError(f'measurement {key} is missing from the capture results')
        self.need.add(key)
        return None

    # specimens -----------------------------------------------------------------------------------------------
    def spec(self, sid, html, chapter, rule, alt, width=None, illustrative=False, exempt=None, surface=None,
             interactive=False, notes='', height=None, readable=False, scale=None, sizing=None):
        if sid in self.specs:
            raise ValueError(f'{sid} registered twice')
        if re.search(r'<h[1-6]\b', html, re.I):
            raise ValueError(f'{sid}: heading element in a specimen')
        if C.EM_DASH in re.sub(r'<[^>]+>', '', html) or C.EN_DASH in re.sub(r'<[^>]+>', '', html):
            raise ValueError(f'{sid}: em or en dash in specimen text')
        bare = re.sub(r'var\((?:[^()]|\([^()]*\))*\)', '', html)
        bare = re.sub(r'\sd="[^"]*"', '', bare)
        if re.search(r'(?<![\w&])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![\w-])|\brgba?\(|\bhsla?\(', bare):
            raise ValueError(f'{sid}: literal color outside var()')
        if re.search(r'font-size:\s*[\d.]+px', html):
            raise ValueError(f'{sid}: px font size; use a type token or rem')
        if re.search(r'<(nav|article|header|footer|main|aside|section)\b', html, re.I):
            raise ValueError(f'{sid}: landmark or sectioning element in a specimen; use div')
        if exempt and 'scale' in exempt and 'scale' not in notes.lower() and 'off the scale' not in notes.lower():
            raise ValueError(f'{sid}: check_exempt scale needs its reason in notes')
        # sizes for display styles: the phone floor up to 600 px, the ceiling from 1,200 px, and a sheet that flows
        # with the page shows the floor on phones and the ceiling from 48em (D2-254)
        mode = sizing or ('sheet' if width is None else 'ceil' if width >= 1200 else 'floor')
        if 'var(--sx-fs-' in html and mode != 'floor':
            html = f'<style>{self.fs_vars(mode)}</style>' + html
        C.check_copy(alt, f'{sid} alt')
        if width is None:
            # A fluid specimen fills the stage, and on phones the shell's mat has no side padding, so the specimen
            # keeps the small-phone margin itself below the shell's 48em breakpoint.
            html = (f'<style>@media (max-width:47.99em){{.inset{{padding-inline:{self.cssv("--oa-layout-grid-phone-small-margin")}}}}}</style>'
                    f'<div class="inset">{html}</div>')
        html = prefix_classes(html)
        meta = {'chapter': chapter, 'rule': rule, 'width_px': width, 'alt': alt, 'illustrative': illustrative,
                'notes': notes}
        if height:
            meta['height_px'] = height
        if exempt:
            meta['check_exempt'] = exempt
        if surface:
            meta['surface'] = surface
        if interactive:
            meta['interactive'] = True
        if readable:
            meta['readable'] = True
        if scale:
            meta['scale'] = scale
        self.specs[sid] = {'html': html.strip() + '\n', 'meta': meta}
        return sid


def prefix_classes(html):
    """Prefix every class in a fragment with "sx-", in markup and in its <style>, so no name meets a shell class
    (the shell styles .menu, .label, .hinge and more by class, and @scope keeps styles in but not out)."""
    def cls(m):
        return 'class="' + ' '.join(c if c in SHELL_CLASSES else 'sx-' + c for c in m.group(1).split()) + '"'
    html = re.sub(r'class="([^"]*)"', cls, html)

    def css(m):
        body = re.sub(r'(?<![-\d])\.(?!(?:' + '|'.join(SHELL_CLASSES) + r')\b)([A-Za-z][\w-]*)', r'.sx-\1', m.group(2))
        return m.group(1) + body + m.group(3)
    return re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', css, html, flags=re.S)


def check_chapter(ch):
    """The house rules on every word of a chapter file."""
    def walk(o, where):
        if isinstance(o, str):
            C.check_copy(o, where)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f'{where}[{i}]')
        elif isinstance(o, dict):
            for k, x in o.items():
                if k in ('specimen', 'token', 'tokens', 'files', 'related', 'id', 'anchor', 'number'):
                    continue
                walk(x, f'{where}.{k}')
    walk(ch, ch['number'])
    if len(ch.get('intro', [])) > 2:
        raise ValueError(f'chapter {ch["number"]}: more than two intro paragraphs')


def probe_page(ctx, body, title, extra_css=''):
    css = ctx.T.css_path.as_uri()
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{C.esc(title)}</title>'
            f'<link rel="stylesheet" href="{FONTS}"><link rel="stylesheet" href="{css}">'
            f'<style>body{{margin:0;padding:24px;background:var(--oa-color-surface-newsprint);'
            f'color:var(--oa-color-text-primary-on-newsprint);font:var(--oa-type-body)}}{extra_css}</style>'
            f'</head><body>{body}</body></html>')


def measure_page(ctx, page):
    """One page holding every text measurement the chapters ask for."""
    out = []
    for key, p in ctx.probes.items():
        k = p['kind']
        if k == 'cpl':
            out.append(f'<div data-probe="{C.esc(key)}" data-kind="cpl" style="{p["css"]};margin:0 0 40px">{C.esc(p["text"])}</div>')
        elif k == 'width':
            disp = '' if 'display:block' in p['css'] else 'display:inline-block;white-space:nowrap;'
            out.append(f'<div style="margin:0 0 40px"><span data-probe="{C.esc(key)}" data-kind="width" '
                       f'style="{disp}{p["css"]}">{C.esc(p["text"])}</span></div>')
        elif k == 'space':
            st = f'display:inline-block;white-space:pre;{p["css"]}'
            out.append(f'<div data-probe="{C.esc(key)}" data-kind="space" style="margin:0 0 40px">'
                       f'<span class="a" style="{st}">n n</span> <span class="b" style="{st}">nn</span></div>')
        elif k == 'fonts':
            out.append(f'<div data-probe="{C.esc(key)}" data-kind="fonts"></div>')
    return page(ctx, ''.join(out), 'measurements')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=['probe', 'final'])
    ap.add_argument('--out-dir', required=True, help='scratch folder for probe pages and capture results')
    ap.add_argument('--tokens-json', default=str(C.TOKENS_JSON))
    ap.add_argument('--tokens-css', default=str(C.TOKENS_CSS))
    ap.add_argument('--allow-old-tracking', action='store_true',
                    help='preview only: build while tokens.json still holds the display tracking before DR-95')
    a = ap.parse_args()
    scratch = pathlib.Path(a.out_dir)
    scratch.mkdir(parents=True, exist_ok=True)
    T = C.Tokens(a.tokens_json, a.tokens_css)
    results = {}
    rp = scratch / 'results.json'
    if a.stage == 'final':
        results = json.loads(rp.read_text())
    ctx = Ctx(T, results, a.stage)
    mods = [_load(f'stage_a_systems_ch0{n}') for n in (5, 6, 7)]
    if a.stage == 'final':
        for mod in mods:
            if hasattr(mod, 'analyze'):
                mod.analyze(ctx, scratch)
    ctx.allow_old_tracking = a.allow_old_tracking
    chapters = [mod.build(ctx) for mod in mods]

    if a.stage == 'probe':
        # Rule 06.4: every rule title in these chapters, at the H3 size, at three trackings
        titles = [r['title'] for ch in chapters for r in ch['rules']]
        h3 = T.ext('oa.type.h3').get('trackingEm', 0)
        for name, tr in (('0', 0), ('token', h3), ('draft', -0.03)):
            ctx.probe(f'pairs titles {name}', 'pairs', text=' '.join(titles), family='Inter Tight', weight=800, size=32,
                      track=tr, n_titles=len(titles))
        pages = {}
        for mod in mods:
            if hasattr(mod, 'probe_pages'):
                pages.update(mod.probe_pages(ctx, probe_page))
        pages['measure.html'] = measure_page(ctx, probe_page)
        for name, html in pages.items():
            (scratch / name).write_text(html)
        (scratch / 'probes.json').write_text(json.dumps({'pages': sorted(pages), 'probes': ctx.probes}, indent=1))
        print(f'probe: {len(pages)} pages, {len(ctx.probes)} probes in {scratch}')
        return

    # final: write chapter files, fragments, the manifest and the measurement record
    OUT_CH.mkdir(parents=True, exist_ok=True)
    OUT_SP.mkdir(parents=True, exist_ok=True)
    used_specs = set()
    for ch in chapters:
        check_chapter(ch)
        for r in ch['rules']:
            for k in ('correct', 'failure', 'corrective'):
                if r.get(k):
                    used_specs.add(r[k]['specimen'])
        for x in ch.get('extras', []):
            used_specs.add(x['specimen'])
        path = OUT_CH / f'{ch["number"]}-{ch["anchor"]}.json'
        path.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + '\n')
    missing = used_specs - set(ctx.specs)
    unused = set(ctx.specs) - used_specs
    if missing or unused:
        raise SystemExit(f'specimens missing {sorted(missing)} unused {sorted(unused)}')
    for sid, s in ctx.specs.items():
        (OUT_SP / f'{sid}.html').write_text(s['html'])
    manifest = {sid: s['meta'] for sid, s in sorted(ctx.specs.items())}
    (OUT_SP / 'manifest-systems.json').write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + '\n')
    record = {
        'about': 'Every figure printed in chapters 05, 06 and 07 of stage board A, with the method that produced it. '
                 'Contrast, OKLab and color-vision figures are computed from tokens.json; rendered figures come from '
                 'Chromium through stage_a_systems_capture.js with the fonts the guide page loads.',
        'built': '2026-11-06',
        'tokens_json': str(pathlib.Path(a.tokens_json).resolve().relative_to(ROOT)) if ROOT in pathlib.Path(a.tokens_json).resolve().parents else a.tokens_json,
        'token_set_version': T.data.get('$extensions', {}).get('org.oathandaction', {}).get('tokenSetVersion')
                             or T.data.get('$extensions', {}).get('org.oathandaction', {}).get('version'),
        'figures': dict(sorted(ctx.figures.items())),
        'rendered': {k: v for k, v in sorted(results.items()) if not k.startswith('_')},
        'render_environment': results.get('_env'),
        'tokens_cited': sorted(ctx.T.used),
    }
    MEAS_OUT.write_text(json.dumps(record, indent=1, ensure_ascii=False) + '\n')
    n_rules = {ch['number']: len(ch['rules']) for ch in chapters}
    print(f'final: chapters {n_rules}, {len(ctx.specs)} specimens, {len(ctx.figures)} figures recorded')


if __name__ == '__main__':
    main()
