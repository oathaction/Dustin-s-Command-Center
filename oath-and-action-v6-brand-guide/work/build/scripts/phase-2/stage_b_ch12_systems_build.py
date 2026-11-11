"""Chapter 12, Graphic devices and patterns: the systems devices, Rules 12.5 to 12.9 (stage B round 2, systems
designer, November 10, 2026).

Usage:
    python3 -I work/build/scripts/phase-2/stage_b_ch12_systems_build.py

Writes:
    work/build/guide/chapters/12-graphic-devices.json   creates the chapter with its opener if it does not exist; in
                                                        any case replaces only Rules 12.5 to 12.9 and their extras, and
                                                        keeps every other rule, group and extra the identity designer
                                                        writes there (12.1 to 12.4, D2-829, D2-830)
    work/build/guide/specimens/s-12-<device>-*.html     one fragment per specimen, named by device, never by rule
    work/build/guide/specimens/manifest-systems.json    the chapter 12 entries, merged; every other chapter's kept
    work/handoffs/phase-2/20261110_Stage-B-Ch12-Systems-Figures.json   every figure the rules print, and how

Reads, never edits: System 1's build (work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py) for the
intervention marker's marks, pills and the atlas locator (DR-36); the chart system's grade table and tile grid
(work/boards/phase-2/data-viz/01-explainer/, DR-52); the atlas model (work/extract/atlas-v7-data.json) for the layers;
the editor's label table for the variables' names (DR-185); chapter 10's build for the shared helpers.

The specimen checks are stage_a_systems_build.Ctx.spec(), as in chapter 10.
"""
import importlib.util
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent


def _load(name, path=None):
    spec = importlib.util.spec_from_file_location(name, path or HERE / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


T10 = _load('stage_b_ch10_build')
B, C, S1 = T10.B, T10.C, T10.S1
ROOT = C.ROOT
EX_DIR = ROOT / 'work/boards/phase-2/data-viz'
TILES = json.loads((EX_DIR / 'shared/geo/us-state-tile-grid.json').read_text())
OUT_CH = ROOT / 'work/build/guide/chapters/12-graphic-devices.json'
OUT_SP = ROOT / 'work/build/guide/specimens'
MANIFEST = OUT_SP / 'manifest-systems.json'
FIG_OUT = ROOT / 'work/handoffs/phase-2/20261110_Stage-B-Ch12-Systems-Figures.json'
CH = '12'
MINE = ('12.5', '12.6', '12.7', '12.8', '12.9')
DEVICES = ('marker', 'key', 'locator', 'layers', 'owner')
esc, nb, nb_html, nb_tree = T10.esc, T10.nb, T10.nb_html, T10.nb_tree
f = S1.f   # System 1's number format for path data

# The chart system's grade table (01 Explainer, build_concept.py GRADE_TABLE): the word, the meaning and the mark each
# grade takes in a chart. Copied as data, with the chart system's mark names mapped to the chart tokens below.
GRADES = [('Documented', 'on the public record', 'ink'), ('Well supported', 'strong research evidence', 'ctx'),
          ('Plausible', 'some evidence', 'lt'), ('Contested', 'evidence disputed', 'hatch'),
          ('Hypothesis', 'not yet tested', 'dot')]


# Chapter 12's intro sentence for Rules 12.5 to 12.9 (ED 4c: the marker's job at first use)
MY_INTRO = ('Rules 12.5 to 12.9 cover the devices that explain a system: the intervention marker, which shows where a reform '
            'acts, chart keys, locators, the layer diagram and the frame that names who owns each step.')
# D2-960: the title states what the invented counts show, 28 of 39 claims documented or well supported (H08)
KEY_TITLE = 'Most claims in these three chapters are documented or well supported'


def pad(px):
    return f'.pad{{box-sizing:border-box;padding:{px}px}}'


def specimens(ctx, rows, v7, figs):
    k = T10.K(ctx)
    t = k.t
    band_css, band = ctx.fail_band()
    cap_css = f'{t("caption")};text-transform:none'
    sec_css = f'.sec{{margin:0 0 10px;{t("label")};color:var(--t2)}}'
    _spec = ctx.spec

    def spec(sid, html, rule, alt, **kw):
        return _spec(sid, nb_html(html), CH, rule, nb(alt), **kw)

    vname = lambda code: rows[next(i for i, r in rows.items() if r.get('v7_id') == code)]['label_where_atlas'] \
        if rows[next(i for i, r in rows.items() if r.get('v7_id') == code)].get('label_where_atlas') \
        else rows[next(i for i, r in rows.items() if r.get('v7_id') == code)]['label']

    # ---------------------------------------------------------------- 12.5 the intervention marker (System 1's red target)
    reform = 'R-01'
    r01 = S1.RF[reform]
    chain = [('C1', 'L08'), ('C2', None)]   # one connection at System 1's own length, about 240 px
    targets = set(r01['targets'])
    figs['marker'] = {'reform': reform, 'targets': sorted(targets), 'shown': ['C1', 'L08', 'C2'],
                      'source': 'System 1 data: work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json'}

    def chain_svg(mode, W=552):
        """mode 'red': the reform's targets in Pillar Red at the selected weight, with the kit's Charcoal keyline on
        Newsprint; 'ink': the same marks yielded to ink (Rule 11.16); 'problem': the failure, red on the problem."""
        pw, cy = 150, 56
        xs = [2 + pw / 2, W - 2 - pw / 2]
        out, h = [], []
        for n, (code, _) in enumerate(chain):
            svg, hh = S1.station_block(code, vname(code), xs[n], cy, pw, 'map')
            hit = code in targets and mode in ('red', 'ink')
            red = (mode == 'red' and hit) or (mode == 'problem' and code == 'C2')
            cls = 'node' + (' target' if hit or red else '') + (' red' if red else '')
            attrs = ' data-red="working" data-red-job="where a reform acts"' if mode == 'red' and hit else (
                ' data-red="working" data-red-job="a problem"' if red else '')
            out.append(f'<g class="{cls}"{attrs}>{svg}</g>')
            h.append(hh)
        for n, (code, lid) in enumerate(chain[:-1]):
            ll = S1.L[lid]
            a, b = xs[n] + pw / 2 + 6, xs[n + 1] - pw / 2 - 6
            pts = [(a, cy), (b, cy)]
            hit = lid in targets and mode in ('red', 'ink')
            red = mode == 'red' and hit
            marks = S1.wire_marks(pts, ll['evidence'], ll['polarity'], ll['delay'], 2, lit=hit)[0]
            (tx, ty), _ = S1.tag_point(pts, 2, ll['polarity'])
            verb = S1.svg_text(tx, ty - 16, S1.verb(ll['polarity']), 'vb', 'middle')
            cls = 'wire' + (' target' if hit else '') + (' red' if red else '')
            attrs = ' data-red="working" data-red-job="where a reform acts"' if red else ''
            out.append(f'<g class="{cls}"{attrs}>{marks}{verb}</g>')
        H = cy + max(h) / 2 + 8
        return (f'<svg class="ch" viewBox="0 0 {W} {f(H)}" width="{W}" height="{f(H)}" aria-hidden="true" focusable="false">'
                f'{"".join(out)}</svg>')

    s1css = ('.ch{display:block;color:var(--ink);overflow:visible}'
             '.ch text{font-family:var(--oa-font-family-reading)}'
             '.st-map{font-size:0.9375rem;font-weight:600;fill:var(--t1)}.vb{font-size:0.8125rem;font-weight:600;fill:var(--t1)}'
             '.pl{fill:var(--oa-color-surface-newsprint);stroke:currentColor}'
             '.wire{color:var(--ink)}.ak-case{stroke:none}.ak-mark{stroke:currentColor}.hd{fill:currentColor}'
             '.tg polygon{fill:currentColor}.tg .sg{fill:var(--oa-color-surface-newsprint)}.tk{stroke:currentColor;stroke-width:2px}'
             '.wire .hi{display:none}.wire.target .lo{display:none}.wire.target .hi{display:inline}'
             '.wire.target .ak-mark{stroke-width:4px;stroke-dasharray:var(--d6,none)}'
             '.node.target .pl{stroke-width:3px}'
             # System 1's red target: the reform's marks take the working red; on Newsprint a red wire carries the kit's
             # 1 px Charcoal keyline (a 6 px case under the 4 px mark, atlas-kit.css)
             '.red .ak-mark,.red .pl{stroke:var(--red)}.wire.red .hd{fill:var(--red)}'
             '.wire.red .ak-case{stroke:var(--oa-color-graphic-essential-on-newsprint);stroke-width:6px;stroke-dasharray:var(--d6,none)}')
    note = (f'Reform {reform}, {r01["title"][0].lower() + r01["title"][1:]}, acts where the marks turn red: here, on '
            f'the connection and on {vname("C2")}.')
    note_ink = (f'Reform {reform} acts on the marks drawn heavier: the connection and {vname("C2")}. An error holds '
                'this view’s red.')
    html = (f'<p class="sec">In a view of its own: the working red</p>{chain_svg("red")}<p class="nt">{esc(note)}</p>'
            f'<p class="sec two">Beside an error or a step to take now: the same marks in ink</p>{chain_svg("ink")}'
            f'<p class="nt">{esc(note_ink)}</p>')
    css = (k.vars() + pad(24) + sec_css + '.sec.two{margin-top:28px}' + s1css +
           f'.nt{{margin:8px 0 0;{t("bodySmall")};max-width:34rem}}')
    spec('s-12-marker-correct', f'<style>{css}</style><div class="pad">{html}</div>', '12.5',
         f'Two copies of one step from the atlas’s safe-seat loop, on Newsprint at 600 px: {vname("C1")} raises '
         f'{vname("C2")}, the connection drawn with its sign tag, its evidence line and its delay tick. In the first '
         f'copy, reform {reform}’s marks are Pillar Red at a heavier weight: the connection, with a thin Charcoal edge, '
         f'and the outline of {vname("C2")}. A note under it reads: {note} In the second '
         f'copy the same marks are heavier but drawn in Charcoal, and the note says an error holds this view’s red.',
         width=600, notes='Marks, pills, tags, verbs and widths from System 1 (DR-36): targets at the selected weight '
                          '(4 px wires, 3 px pills), the lit marks at the 6 px sizes, and atlas-kit.css\'s 1 px Charcoal '
                          'keyline on a red wire on Newsprint. Names from the editor\'s label table (DR-185). The second '
                          'copy is Rule 11.16\'s yield.')
    fail_html = (f'{band}<div class="pad"><p class="sec">Where the problem is</p>{chain_svg("problem")}'
                 f'<p class="nt">Red marks the problem: primaries that settle the seat before November.</p></div>')
    spec('s-12-marker-failure', f'<style>{band_css}{css}</style>{fail_html}', '12.5',
         f'Failure case: do not publish. The same step, with {vname("C2")} outlined in Pillar Red and a note that '
         'says red marks the problem: primaries that settle the seat. No reform is named.',
         width=600, exempt=['red'],
         notes='Labeled failure: red spent on a problem, which System 1 never does ("It never marks a problem or a bad '
               'step"), and a judgment in the note.')

    # ---------------------------------------------------------------- 12.6 chart keys
    data = [('Wages', [6, 4, 3, 1, 1]), ('Housing', [4, 5, 2, 2, 0]), ('Elections', [7, 2, 1, 0, 1])]
    top2 = sum(v[0] + v[1] for _, v in data)
    tot = sum(sum(v) for _, v in data)
    if not top2 * 2 > tot:
        raise SystemExit('Rule 12.6: the title says most claims are documented or well supported, and the counts disagree')
    figs['key'] = {'illustrative_counts': {r: dict(zip([g[0] for g in GRADES], v)) for r, v in data},
                   'title': KEY_TITLE, 'documented_or_well_supported': top2, 'claims': tot}
    W = 358
    fills = {'ink': 'var(--oa-chart-color-subject-on-newsprint)', 'ctx': 'var(--oa-chart-color-context-on-newsprint)',
             'lt': 'var(--oa-chart-color-light-fill-on-newsprint)'}

    def mark(kind, x, y, w, h, uid):
        if kind in fills:
            return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" style="fill:{fills[kind]}"/>'
        if kind == 'hatch':
            return (f'<rect x="{f(x + 0.75)}" y="{f(y + 0.75)}" width="{f(w - 1.5)}" height="{f(h - 1.5)}" '
                    f'class="hb" style="fill:url(#{uid})"/>')
        return (f'<rect x="{f(x + 0.75)}" y="{f(y + 0.75)}" width="{f(w - 1.5)}" height="{f(h - 1.5)}" class="db"/>')

    def chart(failure=False):
        uid = 'hatch'
        defs = (f'<defs><pattern id="{uid}" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<rect width="5" height="5" class="pbg"/><line x1="0" y1="0" x2="0" y2="5" class="pln"/></pattern></defs>')
        x0, unit, bh, pitch = 0, 14, 24, 58
        y = 8
        body = []
        for name, vals in data:
            body.append(f'<text class="tl" x="0" y="{y + 14}">{esc(name)}</text>')
            yb = y + 22
            x = x0
            for (word_, _, kind), v in zip(GRADES, vals):
                if not v:
                    continue
                w = v * unit
                if failure:
                    hue = {'ink': 'var(--oa-color-palette-prussian)', 'ctx': 'var(--oa-color-palette-verdigris)',
                           'lt': 'var(--oa-color-tint-verdigris-c50)', 'hatch': 'var(--oa-color-tint-prussian-n62)',
                           'dot': 'var(--oa-color-palette-stone)'}[kind]
                    body.append(f'<rect x="{f(x)}" y="{yb}" width="{f(w - 1)}" height="{bh}" style="fill:{hue}"/>')
                else:
                    body.append(mark(kind, x, yb, w - 1, bh, uid))
                x += w
            if not failure:
                body.append(f'<text class="tr" x="{f(x + 8)}" y="{yb + 17}">{sum(vals)}</text>')
            y += pitch
        H = y - pitch + 22 + bh + 8
        return (f'<svg class="cv" viewBox="0 0 {W - 32} {H}" width="{W - 32}" height="{H}" aria-hidden="true" '
                f'focusable="false">{defs}{"".join(body)}</svg>')

    key = ''.join(
        f'<li><svg class="sw" viewBox="0 0 14 14" width="14" height="14" aria-hidden="true" focusable="false">'
        f'{mark(kind, 0, 0, 14, 14, "hatch")}</svg><span><strong>{esc(word_)}</strong>, {esc(meaning)}</span></li>'
        for word_, meaning, kind in GRADES)
    ccss = (k.vars() + pad(16) +
            f'.ttl{{margin:0 0 4px;font-family:var(--oa-font-family-display);font-weight:800;font-size:var(--oa-chart-type-title-phone-size);'
            f'line-height:var(--oa-chart-type-title-phone-leading);letter-spacing:-0.01em}}'
            f'.ms{{margin:0 0 12px;{t("bodySmall")};color:var(--oa-chart-color-secondary-on-newsprint)}}'
            '.key{list-style:none;margin:0 0 14px;padding:0;display:flex;flex-wrap:wrap;gap:6px 16px}'
            f'.key li{{display:flex;align-items:center;gap:7px;{t("caption")}}}.sw{{display:block;flex:none}}'
            '.cv{display:block;overflow:visible}'
            '.cv text{font-family:var(--oa-font-family-reading);font-size:var(--oa-chart-type-label)}'
            '.tl{font-weight:600;fill:var(--oa-chart-color-label-on-newsprint)}.tr{font-weight:400;fill:var(--oa-chart-color-label-on-newsprint);font-variant-numeric:tabular-nums}'
            '.pbg{fill:var(--oa-chart-color-light-fill-on-newsprint)}.pln{stroke:var(--oa-chart-color-context-on-newsprint);stroke-width:var(--oa-chart-hatch-weight)}'
            '.hb{stroke:var(--oa-chart-color-context-on-newsprint);stroke-width:1.5px}'
            '.db{fill:none;stroke:var(--oa-chart-color-subject-on-newsprint);stroke-width:1.5px;stroke-dasharray:1.5 2.5;stroke-linecap:round}'
            f'.src{{margin:14px 0 0;{t("caption")};color:var(--oa-chart-color-secondary-on-newsprint)}}')
    head = (f'{T10.ILLUS}<p class="ttl">{esc(KEY_TITLE)}</p>'
            f'<p class="ms">Claims in each chapter of a report, by the grade of their evidence</p>')
    spec('s-12-key-correct', f'<style>{ccss}</style><div class="pad">{head}<ul class="key">{key}</ul>{chart()}'
         f'<p class="src">Grades as our systems atlas defines them. Counts invented for this example.</p></div>', '12.6',
         f'An Illustrative chart on a 358 px phone. Its title reads {KEY_TITLE}, '
         'and its measure line reads Claims in each chapter of a report, by the grade of their evidence. Above the plot, '
         'a key names the five grades in the order their segments run, each with a swatch drawn in the chart’s own mark: '
         'Documented, on the public record, solid ink; Well supported, strong research evidence, gray; Plausible, some '
         'evidence, light gray; Contested, evidence disputed, a hatch; Hypothesis, not yet tested, a dotted outline. Three '
         'stacked bars follow, each named at its left and with its total at its end: Wages 15, Housing 13, Elections 11.',
         width=W, illustrative=True,
         notes='Grade marks from the chart system\'s GRADE_TABLE (01 Explainer, DR-52), colors and line weights from the '
               'chart tokens; key swatches 14 px with a 7 px gap, as the chart system\'s key_item draws them.')
    fail = (f'{band}<div class="pad">{T10.ILLUS}<p class="ttl">Claims by grade</p>{chart(True)}'
            '<div class="lg"><ul>' + ''.join(
                f'<li><span class="dt" style="background:{hue}"></span>{esc(w)}</li>' for w, hue in [
                    ('Hypothesis', 'var(--oa-color-palette-stone)'), ('Contested', 'var(--oa-color-tint-prussian-n62)'),
                    ('Plausible', 'var(--oa-color-tint-verdigris-c50)'), ('Well supported', 'var(--oa-color-palette-verdigris)'),
                    ('Documented', 'var(--oa-color-palette-prussian)')]) + '</ul></div></div>')
    fcss = (ccss + band_css + '.lg{display:flex;justify-content:flex-end;margin-top:12px}'
            f'.lg ul{{list-style:none;margin:0;padding:8px 10px;border:1px solid var(--hair);{t("label")};text-transform:none}}'
            '.lg li{display:flex;align-items:center;gap:6px}.dt{display:inline-block;width:8px;height:8px;border-radius:50%}')
    spec('s-12-key-failure', f'<style>{fcss}</style>{fail}', '12.6',
         'Failure case: do not publish. The same Illustrative chart titled Claims by grade, with no measure line '
         'and no totals, its segments in five blues and greens. A boxed legend sits under the plot at the right, listing '
         'the grades from Hypothesis to Documented, the reverse of the bars, each beside a small colored dot.',
         width=W, illustrative=True, exempt=['contrast'],
         notes='Labeled failure: a detached legend in reverse order, dots that match no mark, hue alone for the grades '
               '(Prussian and Verdigris tie in grayscale), no unit.')

    # ---------------------------------------------------------------- 12.7 locators
    loc_atlas = re.sub(r'^<a[^>]*>|</a>$', '', S1.locator('C'))
    loc_atlas = loc_atlas.replace('<svg data-view="locator"', '<svg class="lca"')
    lab_parts = {p['id']: p['plain_name'] for p in S1.ED['parts']}
    state = 'NE'
    tw_, gap = 8, 1      # 107 px across, so the headline beside it keeps 205 px at 360 px (CA-S12)
    cells = []
    for tl in TILES:
        x, y = tl['col'] * (tw_ + gap), tl['row'] * (tw_ + gap)
        cls = 'on' if tl['code'] == state else 'off'
        cells.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{tw_}" height="{tw_}"/>')
    cols = max(tl['col'] for tl in TILES) + 1
    rws = max(tl['row'] for tl in TILES) + 1
    gw, gh = cols * (tw_ + gap) - gap, rws * (tw_ + gap) - gap
    st_name = next(tl['name'] for tl in TILES if tl['code'] == state)
    loc_state = (f'<svg class="lcs" viewBox="0 0 {gw} {gh}" width="{gw}" height="{gh}" aria-hidden="true" '
                 f'focusable="false">{"".join(cells)}</svg>')
    figs['locator'] = {'atlas_current': 'C', 'state': state, 'tile_px': tw_, 'gap_px': gap, 'columns': cols, 'rows': rws,
                       'state_locator_px': [gw, gh], 'headline_px_at_360': 360 - 2 * 16 - gw - 16,
                       'tile_grid': 'work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json'}
    html = (f'{T10.ILLUS}<p class="sec">In the atlas: where this view sits among the parts</p>'
            f'<div class="hdr"><div><p class="crumb">Overview › {esc(lab_parts["C"])}</p>'
            f'<p class="vt">How safe seats move the real choice to the primary</p></div>{loc_atlas}</div>'
            f'<p class="sec two">In a state story: where the state sits on the map</p>'
            f'<div class="hdr"><div><p class="kick">Tracker {T10.DOT} {esc(st_name)}</p>'
            f'<p class="vt">{esc(st_name)} has one chamber, so a bill’s fifth step never comes</p></div>{loc_state}</div>')
    lcss = (k.vars() + pad(16) + sec_css + '.sec.two{margin-top:24px}.pad > .illus{margin:0 0 12px}'
            '.hdr{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;padding:12px 0;border-top:1px solid var(--strong)}'
            f'.crumb{{margin:0 0 4px;{t("caption")};color:var(--t2)}}.kick{{margin:0 0 4px;{t("label")}}}'
            f'.vt{{margin:0;{t("h4")};max-width:14rem}}'
            '.lca,.lcs{display:block;flex:none}'
            '.lca .lc{fill:var(--oa-color-surface-newsprint);stroke:var(--oa-color-graphic-subtle-on-newsprint);stroke-width:1px;vector-effect:non-scaling-stroke}'
            '.lca .lc.on{fill:var(--ink);stroke:var(--ink)}'
            '.lcs .off{fill:var(--oa-color-tint-stone-n70)}.lcs .on{fill:var(--ink)}')
    spec('s-12-locator-correct', f'<style>{lcss}</style><div class="pad">{html}</div>', '12.7',
         f'Two Illustrative view headers on a 360 px phone, each with a small locator at its right, drawn in ink. The first, from the '
         f'atlas, reads Overview, {lab_parts["C"]}, over the title How safe seats move the real choice to the primary; '
         'its locator is the atlas in small, a bar for outside forces, five boxes for its parts and two boxes below, with '
         f'the third box, {lab_parts["C"]}, filled Charcoal. The second, a state story, reads Tracker, {st_name}, over '
         f'the title {st_name} has one chamber, so a bill’s fifth step never comes; its locator is the 50-state tile '
         f'grid with {st_name} filled Charcoal and every other state light gray.',
         width=360, illustrative=True,
         notes='The atlas locator is System 1\'s locator() geometry (DR-36), redrawn on Newsprint (DR-53); the '
               'state grid is the chart system\'s tile grid at 8 px a tile (CA-S12). Nebraska\'s line is Rule 11\'s '
               '(DR-150). Both headlines are invented, so one Illustrative label heads the plate (BE-S5, CD-S13).')
    loc_red = loc_atlas.replace('class="lca"', 'class="lca" data-red="working" data-red-job="you are here"')
    html = (f'{band}<div class="pad">{T10.ILLUS}<div class="hdr"><div><p class="crumb">Overview › {esc(lab_parts["C"])}</p>'
            f'<p class="vt">How safe seats move the real choice to the primary</p></div>{loc_red}</div></div>')
    spec('s-12-locator-failure', f'<style>{band_css}{lcss}.lca .lc.on{{fill:var(--red);stroke:var(--red)}}</style>{html}', '12.7',
         f'Failure case: do not publish. The Illustrative atlas view header, with the locator’s current box, '
         f'{lab_parts["C"]}, filled Pillar Red.', width=360, illustrative=True, exempt=['red'],
         notes='Labeled failure: the locator spends the view\'s red on "you are here", which takes it from the reform '
               'target, the error or the ask (Rule 05.3, Rule 11.16).')

    # ---------------------------------------------------------------- 12.8 the layer diagram (the one exploded view)
    layers = [(k_, v) for k_, v in v7['layers'].items()]
    plain = {p_['id']: p_['plain_name'] for p_ in S1.ED['parts']}
    # the core's parts lead with the plain names every other page uses (Wealth, Voice, Elections, Checks, Policy,
    # Outside forces); the economy and technology planes keep the atlas's region titles, which have no plain names
    rname = lambda k_, r: plain.get(r.get('id'), r['title']) if k_ == 'core' else r['title']
    figs['layers'] = [{'id': k_, 'title': v['title'], 'regions': [r['title'] for r in v.get('regions', [])],
                       'printed': [rname(k_, r) for r in v.get('regions', [])]} for k_, v in layers]
    W8 = 600
    ox, dx, dy = 16, 120, 60          # an oblique plane: depth runs up and to the right
    pw_ = 200                         # plane width along x; planes stacked 130 px apart
    out, labels = [], []
    tops = [24, 154, 284]

    def plane(y, cls):
        p = [(ox, y + dy), (ox + pw_, y + dy), (ox + pw_ + dx, y), (ox + dx, y)]
        return f'<polygon class="{cls}" points="{" ".join(f"{f(a)},{f(b)}" for a, b in p)}"/>'
    for n, (key_, lay) in enumerate(layers):
        y = tops[n]
        out.append(plane(y, 'pl' + (' core' if key_ == 'core' else '')))
        regs = lay.get('regions', [])
        m = len(regs)
        for j in range(m):   # one tile per region, set on the plane
            u0, u1 = 0.08 + 0.84 * j / m + 0.01, 0.08 + 0.84 * (j + 1) / m - 0.01
            v0, v1 = 0.3, 0.7
            P = lambda u, v: (ox + u * pw_ + v * dx, y + dy - v * dy)
            q = [P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)]
            out.append(f'<polygon class="rg" points="{" ".join(f"{f(a)},{f(b)}" for a, b in q)}"/>')
        if n < len(layers) - 1:
            for u in (0.25, 0.75):
                xx = ox + u * pw_ + 0.5 * dx
                out.append(f'<line class="tie" x1="{f(xx)}" y1="{f(y + dy - 0.5 * dy)}" x2="{f(xx)}" y2="{f(tops[n + 1] + dy - 0.5 * dy)}"/>')
        lx = ox + pw_ + dx + 24
        title = lay['title']
        sub = ', '.join(rname(key_, r) for r in regs)
        tl_ = S1.swrap(title, W8 - lx - 8, 'map')
        for i_, ln in enumerate(tl_):
            labels.append(f'<text class="lt" x="{lx}" y="{f(y + 22 + 19 * i_)}">{esc(ln)}</text>')
        for i_, ln in enumerate(S1.swrap(sub, W8 - lx - 8, 'note')):
            labels.append(f'<text class="ls" x="{lx}" y="{f(y + 22 + 19 * len(tl_) + 4 + 17 * i_)}">{esc(ln)}</text>')
        labels.append(f'<line class="ld" x1="{f(ox + pw_ + dx + 4)}" y1="{f(y + 16)}" x2="{f(lx - 6)}" y2="{f(y + 16)}"/>')
    H8 = tops[-1] + dy + 24
    svg = (f'<svg class="lay" viewBox="0 0 {W8} {H8}" width="{W8}" height="{H8}" aria-hidden="true" focusable="false">'
           f'{"".join(out)}{"".join(labels)}</svg>')
    ycss = (k.vars() + pad(0) + '.lay{display:block}'
            '.pl{fill:var(--oa-color-surface-newsprint);stroke:var(--ink);stroke-width:1.5px;stroke-linejoin:round}'
            '.pl.core{stroke-width:2.5px}'
            '.rg{fill:var(--oa-color-tint-stone-n85);stroke:var(--oa-color-graphic-subtle-on-newsprint);stroke-width:1px}'
            '.tie{stroke:var(--ink);stroke-width:1px;stroke-dasharray:2 3}'
            '.ld{stroke:var(--t2);stroke-width:1px}'
            '.lay text{font-family:var(--oa-font-family-reading)}'
            '.lt{font-size:0.9375rem;font-weight:700;fill:var(--t1)}.ls{font-size:0.8125rem;fill:var(--t2)}'
            f'.cp{{margin:8px 0 0;{t("caption")};color:var(--t2)}}')
    lay_alt = '; '.join(f'{v["title"]}, holding {", ".join(rname(k_, r) for r in v.get("regions", []))}' for k_, v in layers)
    spec('s-12-layers-correct', f'<style>{ycss}</style>{svg}', '12.8',
         'An exploded view of our systems atlas at 600 px: three flat planes stacked one above another and drawn at a '
         'slant, joined by dotted ties. Each plane carries one tile for each of its parts, and each name sits flat and '
         f'upright to the right of its plane, never on the slant. From the top: {lay_alt}. The top plane, the core, has '
         'the heavier outline.',
         width=W8, height=H8, notes='Layers, titles and regions read from the atlas model; the slant is the one place an '
                                    'exploded view is allowed (isometric study 03).')
    # failure: names set on the slant, inside the planes
    skew = []
    for n, (key_, lay) in enumerate(layers):
        y = tops[n]
        skew.append(plane(y, 'pl'))
        cx, cyy = ox + 0.5 * pw_ + 0.5 * dx, y + 0.5 * dy
        ang = -25.0
        skew.append(f'<text class="lt" text-anchor="middle" transform="translate({f(cx)} {f(cyy + 5)}) rotate({ang}) skewX(-30)">'
                    f'{esc(lay["title"])}</text>')
    svgf = (f'<svg class="lay" viewBox="0 0 {W8} {H8}" width="{W8}" height="{H8}" aria-hidden="true" focusable="false">'
            f'{"".join(skew)}</svg>')
    spec('s-12-layers-failure', f'<style>{band_css}{ycss}</style>{band}{svgf}', '12.8',
         'Failure case: do not publish. The same three planes with no parts and no ties, each layer’s name set '
         'inside its plane, turned and slanted to follow the plane, so every name reads at an angle.',
         width=W8, notes='Labeled failure: labels on the oblique, which the exploded view never takes.')

    # ---------------------------------------------------------------- 12.9 who owns the next step (V4.2's frame)
    steps = [
        ('You', 'Send a written request that describes the records you want to the agency’s records office.',
         'The agency’s records office', 'Twenty working days to decide whether to release the records, from the day '
         'the request arrives.'),
        ('The agency’s records office', 'Confirms the request with a tracking number, searches for the records, reviews '
         'them, blacking out what an exemption protects, and sends a written answer with the records it can release.',
         'You', 'At least 90 days to appeal a refusal or a partial answer.'),
        ('You', 'If you appeal, write to the agency’s appeal office.', 'The agency’s appeal office',
         'Twenty working days to decide the appeal.'),
        ('The agency’s appeal office', 'Reviews the answer and decides whether to release more.', None, None),
    ]
    li = []
    for n, (who, what, nxt, clock) in enumerate(steps, 1):
        handoff = (f'<p class="ho"><span class="ar" aria-hidden="true">↓</span> Next step: <strong>{esc(nxt)}</strong>'
                   + (f'. {esc(clock)}' if clock else '') + '</p>') if n < len(steps) else (
            '<p class="ho"><span class="ar" aria-hidden="true">↓</span> Next step: <strong>You</strong>, again. Ask the '
            'National Archives’ records ombudsman to mediate, or sue in federal court.</p>')
        li.append(f'<li><p class="n">{n}</p><div><p class="who">{esc(who)}</p><p class="what">{esc(what)}</p>{handoff}</div></li>')
    ocss = (k.vars() + f'.q{{margin:0 0 4px;{t("h4")}}}.qs{{margin:0 0 16px;{t("bodySmall")};color:var(--t2)}}'
            '.st{list-style:none;margin:0;padding:0;border-top:2px solid var(--strong)}'
            '.st li{display:grid;grid-template-columns:2rem minmax(0,1fr);gap:12px;padding:14px 0;border-bottom:1px solid var(--hair)}'
            f'.n{{margin:0;{t("ui")};font-weight:700;font-variant-numeric:tabular-nums}}'
            f'.who{{margin:0;{t("ui")};font-weight:700}}.what{{margin:4px 0 0;{t("bodySmall")};max-width:34rem}}'
            f'.ho{{margin:8px 0 0;{t("caption")}}}.ar{{margin-right:4px}}'
            f'.src{{margin:14px 0 0;{t("caption")};color:var(--t2);max-width:40rem}}')
    src = ('Sources: 5 U.S.C. 552, the Freedom of Information Act, sections (a)(6)(A), (h)(3) and (a)(4)(B), as in force on '
           'November 9, 2026, via the Legal Information Institute, Cornell Law School; and FOIA.gov, “Frequently Asked '
           'Questions”, Office of Information Policy, U.S. Department of Justice, no page date; both retrieved November 9, '
           '2026. Federal agencies only; states set their own records laws.')
    html = (f'<p class="q">Who owns the next step?</p><p class="qs">A federal records request, from your letter to an '
            f'appeal</p><ol class="st">{"".join(li)}</ol><p class="src">{esc(src)}</p>')
    spec('s-12-owner-correct', f'<style>{ocss}</style>{html}', '12.9',
         'A frame titled Who owns the next step?, for a federal records request, in four numbered steps. Each step names '
         'who acts, what they do, and who owns the next step, with the deadline the law sets. ' + ' '.join(
             f'Step {n}: {who}. {what} Next step: {nxt}.' + (f' {clock}' if clock else '')
             for n, (who, what, nxt, clock) in enumerate(steps[:-1], 1))
         + f' Step 4: {steps[-1][0]}. {steps[-1][1]} Next step: You, again. Ask the National Archives’ records ombudsman '
           'to mediate, or sue in federal court. ' + src,
         readable=True, notes='V4.2\'s frame ("Give every handoff an owner."), with the deadlines and routes from the '
                              'research notes, section 7A (5 U.S.C. 552(a)(6)(A), (a)(6)(A)(ii), (h)(3), (a)(4)(B)).')
    boxes = ['Request submitted', 'Request processed', 'Records reviewed', 'Response issued', 'Appeal considered']
    fx, fy, bw, bh = 16, 16, 300, 40
    parts = []
    for n, b in enumerate(boxes):
        y = fy + n * (bh + 24)
        parts.append(f'<rect class="bx" x="{fx}" y="{y}" width="{bw}" height="{bh}"/>'
                     f'<text class="bt" x="{fx + bw / 2}" y="{y + 25}" text-anchor="middle">{esc(b)}</text>')
        if n < len(boxes) - 1:
            parts.append(f'<path class="aw" d="M{fx + bw / 2} {y + bh + 4}V{y + bh + 18}"/>'
                         f'<path class="ah" d="M{fx + bw / 2 - 5} {y + bh + 14}L{fx + bw / 2} {y + bh + 20}L{fx + bw / 2 + 5} {y + bh + 14}"/>')
    Hf = fy + len(boxes) * (bh + 24) - 8
    svgf = (f'<svg class="fl" viewBox="0 0 332 {Hf}" width="332" height="{Hf}" aria-hidden="true" focusable="false">'
            f'{"".join(parts)}</svg>')
    fcss = (k.vars() + band_css + pad(14) + '.fl{display:block}.bx{fill:none;stroke:var(--ink);stroke-width:1.5px}'
            '.fl text{font-family:var(--oa-font-family-reading);font-size:0.9375rem;fill:var(--t1)}'
            '.aw,.ah{fill:none;stroke:var(--ink);stroke-width:1.5px}'
            f'.q{{margin:0 0 8px;{t("h4")}}}')
    spec('s-12-owner-failure', f'<style>{fcss}</style>{band}<div class="pad"><p class="q">How a records request works</p>{svgf}</div>',
         '12.9',
         'Failure case: do not publish. A flow chart titled How a records request works: five boxes joined by '
         'arrows, reading Request submitted, Request processed, Records reviewed, Response issued and Appeal considered, '
         'with no one named in any box and no deadline.',
         width=360, notes='Labeled failure: every step in the passive voice, so no step says who acts or whom to call.')


def chapter(ctx, figs, existing):
    rules = []
    rules.append({
        'id': '12.5', 'title': 'Mark where a reform acts with the atlas’s red target.',
        'rule': [
            'Where a figure shows a reform at work, only the marks it acts on turn Pillar Red, at a heavier weight: each '
            'connection it changes, with its arrowhead, and the outline of each variable it targets. A connection is '
            'the atlas’s arrow from one variable to another (Rule 10.10). On Newsprint '
            'a red connection carries a 1 px Charcoal edge. A note beside the figure names the reform and says that it '
            'acts where the marks turn red.',
            'The marker is the view’s one working red. When an error or a step the reader can take now shares the view, '
            'the marker yields as Rule 11.16 sets out: its marks stay heavier, in ink, and the note still names the '
            'reform.'],
        'tokens': ['oa.color.data.emphasisRed.onNewsprint', 'oa.color.data.emphasis.onNewsprint',
                   'oa.color.graphic.essential.onNewsprint'],
        'why': {'text': [
            'Red means one thing across the atlas: this is where a reform acts. It never marks a problem or a bad step, '
            'so a reader of any party can follow the mechanism without being told which outcome to dislike. The heavier '
            'weight and the note carry the meaning when red is gone, in gray print or beside an error. Pillar Red '
            'measures 2.96 to 1 on Newsprint, so a 1 px Charcoal edge, at 13.29 to 1, outlines the red line against the '
            'page.'],
            'basis': 'Design judgment, from the atlas’s visual system'},
        'correct': {'specimen': 's-12-marker-correct',
                    'caption': 'Reform R-01, all-party primaries with ranked general elections, on one step of Loop R10, '
                               'the safe-seat loop: in red when it holds the view’s red, then in ink when an error does.'},
        'failure': {'specimen': 's-12-marker-failure',
                    'caption': '<strong>Fails Rule 12.5.</strong> Red marks the problem, and the note calls it one. The '
                               'figure now takes a side on an outcome and spends the view’s red on it.'},
        'specs': [
            {'label': 'Target weight', 'value': 'Pillar Red: connections 4 px, variable outlines 3 px; arrowheads and sign '
                                                'tags at the 6 px sizes', 'token': 'oa.color.data.emphasisRed.onNewsprint'},
            {'label': 'Edge on Newsprint', 'value': '1 px Charcoal on each side of a red connection, as a 6 px case under '
                                                    'the 4 px line', 'token': 'oa.color.graphic.essential.onNewsprint'},
            {'label': 'Note', 'value': '“Reform R-01, …, acts where the marks turn red.”'},
            {'label': 'Yielded', 'value': 'The same weights in ink, with the note (Rule 11.16)'},
        ],
        'files': ['work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py',
                  'work/boards/phase-2/atlas-concepts/shared/atlas-kit.css'],
        'related': ['05', '11', '15'],
        'builders': ['Draw the marks with the atlas build’s own <code>wire_marks</code> and give the targets the '
                     'kit’s <code>ak-target</code> class; the kit’s Newsprint surface sets the keyline. Set '
                     '<code>data-red="working"</code> on the red marks so the check can count the view’s red.'],
    })
    rules.append({
        'id': '12.6', 'title': 'Label each mark where it sits.',
        'rule': [
            'Name each line, bar or point beside it where the label fits. When a chart codes something a label cannot '
            'carry on every mark, such as the evidence grade of each segment, set a key above the plot. List its items '
            'in the order the marks run, draw each swatch in the chart’s own mark, give each its word and meaning, and '
            'name the unit in the measure line, the line under a chart’s title that says what is counted and in what '
            'unit.'],
        'tokens': ['oa.chart.color.subject.onNewsprint', 'oa.chart.color.context.onNewsprint',
                   'oa.chart.color.lightFill.onNewsprint', 'oa.chart.hatch.pitch'],
        'why': {'text': [
            'A label beside its mark is read once. A key makes the reader look away, match a swatch and look back, so it '
            'should come before the plot, in the plot’s order, with swatches that match the marks exactly. Marks drawn as '
            'shades, a hatch and a dotted outline still tell the grades apart in gray print, where hues of the same '
            'lightness merge.'],
            'basis': 'Design judgment, from the chart system'},
        'correct': {'specimen': 's-12-key-correct',
                    'caption': 'A key above a phone chart, in the order the segments run, each swatch drawn as its mark. '
                               'Its title says only what the counts show, that 28 of the 39 claims are documented or well '
                               'supported.'},
        'failure': {'specimen': 's-12-key-failure',
                    'caption': '<strong>Fails Rule 12.6.</strong> A boxed legend under the plot, in reverse order, with '
                               'dots that match no mark and hues that merge in gray. The chart names no unit.'},
        'specs': [
            {'label': 'Swatch', 'value': '14 px, the label 7 px after it; items 16 px apart, wrapping in rows',
             'token': 'oa.chart.hatch.pitch'},
            {'label': 'Order', 'value': 'The order the marks run, left to right or top to bottom'},
            {'label': 'Grade marks', 'value': 'In bars and areas, Documented solid ink, Well supported gray, Plausible '
                                              'light gray, Contested a hatch, Hypothesis a dotted outline; a connection in '
                                              'the atlas takes Rule 10.10’s line textures'},
            {'label': 'Place', 'value': 'Under the title and measure line, above the plot'},
        ],
        'files': ['work/boards/phase-2/data-viz/01-explainer/build_concept.py'],
        'related': ['14', '15'],
        'builders': ['Take the swatches and the grade table from the chart system’s build, <code>key_item</code> and '
                     '<code>GRADE_TABLE</code>, so a key and its chart can never drift apart.'],
    })
    rules.append({
        'id': '12.7', 'title': 'Show where a view sits in the whole with a small locator in ink.',
        'rule': [
            'A view that shows part of a larger whole carries a locator at its top right: the whole in small, with the '
            'current part filled in Charcoal and the rest in a light ground. In the atlas, the locator draws the atlas’s '
            'parts and links back to the overview. In a state story it is the 50-state tile grid.',
            'Draw the locator in ink, with no red.'],
        'tokens': ['oa.color.graphic.essential.onNewsprint', 'oa.color.graphic.subtle.onNewsprint'],
        'why': {'text': [
            'A reader who arrives from a search lands in the middle of the system. A locator answers “Where am I?” before '
            'the reader asks, and the same small map on every view teaches its shape. Kept to ink, it never competes with the '
            'red that marks a reform, an error or a step to take.'],
            'basis': 'Design judgment, from the atlas’s visual system'},
        'correct': {'specimen': 's-12-locator-correct',
                    'caption': 'The atlas locator and the state locator at true size, each in ink, small enough that the '
                               'headline beside it keeps at least 200 px on a phone.'},
        'failure': {'specimen': 's-12-locator-failure',
                    'caption': '<strong>Fails Rule 12.7.</strong> The current part filled red. “You are here” takes the '
                               'view’s red, and the reform marker, the error or the ask loses it.'},
        'specs': [
            {'label': 'Atlas locator', 'value': '88 by 41 px, the parts as boxes, the current one filled'},
            {'label': 'State locator', 'value': f'{figs["locator"]["tile_px"]} px tiles with {figs["locator"]["gap_px"]} px '
                                                f'gaps, {figs["locator"]["columns"]} columns, {figs["locator"]["state_locator_px"][0]} by '
                                                f'{figs["locator"]["state_locator_px"][1]} px, the state filled; the headline '
                                                'beside it keeps at least 200 px on a 360 px phone'},
            {'label': 'Place', 'value': 'Top right of the view’s header; hidden on phones in the atlas, where the '
                                        'breadcrumb carries it'},
            {'label': 'Ink', 'value': 'Charcoal for the current part', 'token': 'oa.color.graphic.essential.onNewsprint'},
        ],
        'files': ['work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json'],
        'related': ['14', '21'],
        'builders': ['Draw the atlas locator from the atlas build’s <code>locator()</code> and the state locator from the '
                     'tile grid file; mark the current part with a class, never with a color written into the drawing.'],
    })
    rules.append({
        'id': '12.8', 'title': 'Use an exploded view only to stack the atlas’s layers, and keep every name flat.',
        'rule': [
            'An exploded view, a drawing of flat planes stacked at a slant, shows one thing in this guide: how the atlas’s '
            'three layers sit on one another. Draw each layer as a plane with one tile for each of its parts, join the '
            'planes with dotted ties, and set every name flat and upright beside its plane.'],
        'tokens': ['oa.color.graphic.essential.onNewsprint'],
        'why': {'text': [
            'A slant shows depth, which suits layers and nothing else we draw. Names on a slant read slowly and turn to '
            'texture at small sizes, so the names stay flat where a reader’s eye already runs.'],
            'basis': 'Design judgment'},
        'correct': {'specimen': 's-12-layers-correct',
                    'caption': 'The atlas’s three layers, each with its parts, and every name flat beside its plane.'},
        'failure': {'specimen': 's-12-layers-failure',
                    'caption': '<strong>Fails Rule 12.8.</strong> The names follow the slant into the planes, so each one '
                               'reads at an angle and the parts are lost.'},
        'specs': [
            {'label': 'Planes', 'value': 'Three, the core outlined at 2.5 px and the others at 1.5 px'},
            {'label': 'Ties', 'value': '1 px dotted, two between each pair of planes'},
            {'label': 'Names', 'value': 'Flat, upright, to the right of each plane, with a 1 px leader'},
        ],
        'files': ['work/extract/atlas-v7-data.json'],
        'related': ['15', '21'],
        'builders': ['Read the layers and their parts from the atlas model, never from a list typed by hand, so the '
                     'diagram follows the atlas when it changes.'],
    })
    rules.append({
        'id': '12.9', 'title': 'In a process explainer, name who owns the next step at every handoff.',
        'rule': [
            'Give every step of a process a person or an office that acts, and at each handoff name who owns the next '
            'step and the deadline the law sets. Write each step with its actor first. Link the steps to '
            'the official procedure in a source line.'],
        'tokens': ['oa.type.ui', 'oa.type.bodySmall'],
        'why': {'text': [
            'Our guide’s fourth edition put it in one line: “Give every handoff an owner.” A reader who knows who holds a request '
            'knows whom to call when it stalls. Passive steps hide that, and a process with no owner reads as one that '
            'runs by itself.'],
            'basis': 'Design judgment, from our guide’s fourth edition'},
        'correct': {'specimen': 's-12-owner-correct',
                    'caption': 'A federal records request, with who acts at each step, who owns the next one and the '
                               'deadline the law sets.'},
        'failure': {'specimen': 's-12-owner-failure',
                    'caption': '<strong>Fails Rule 12.9.</strong> Five passive boxes. The reader cannot tell who has the '
                               'request or whom to call when it stalls.'},
        'specs': [
            {'label': 'Each step', 'value': 'Actor first, then the act', 'token': 'oa.type.ui'},
            {'label': 'Each handoff', 'value': '“Next step:” and the owner, then the deadline', 'token': 'oa.type.bodySmall'},
            {'label': 'Source line', 'value': 'The statute or official page for every deadline'},
        ],
        'related': ['11', '15'],
        'builders': ['Name an office by its role, as in “the agency’s records office”, so the frame holds for every '
                     'agency, and put the agency’s own name in a live page.'],
    })
    # no-break spaces and non-breaking hyphens go into my own strings only, so the identity designer's rules in the same
    # file stay exactly as their script writes them
    rules = nb_tree(rules)
    my_intro = nb_tree(MY_INTRO)
    if existing:
        ch = existing
        # my sentence of the intro (the identity designer's sentence for Rules 12.1 to 12.4 opens the same paragraph and
        # is theirs): replace it where it stands, or add it at the end of the second paragraph
        intro = list(ch.get('intro', []))
        for n_, para in enumerate(intro):
            if 'Rules 12.5 to 12.9 cover' in para:
                intro[n_] = re.sub(r'Rules 12\.5 to 12\.9 cover.*$', lambda m: my_intro, para, flags=re.S)
                break
        else:
            if len(intro) >= 2:
                intro[1] = intro[1].rstrip() + ' ' + my_intro
            else:
                intro.append(my_intro)
        ch['intro'] = intro
        keep = [r for r in ch.get('rules', []) if r.get('id') not in MINE]
        ch['rules'] = sorted(keep + rules, key=lambda r: [int(x) for x in str(r['id']).split('.')])
        ch['extras'] = [x for x in ch.get('extras', []) if not str(x.get('specimen', '')).startswith(
            tuple(f's-12-{d}-' for d in DEVICES))]
        return ch
    return {
        'number': CH, 'anchor': 'graphic-devices', 'title': 'Graphic devices and patterns', 'part': 'Symbols and graphics',
        'instruction': 'Add dividers, frames, markers and watermarks only where they help someone read.',
        'intro': [
            'A graphic device is a mark that helps a reader find their way: a divider between sections, a watermark, a '
            'marker on the place a reform acts, a key, a locator, a frame around a process. Each one has a job, and the '
            'page leaves it out where that job is already done.',
            my_intro],
        'rules': rules,
        'related_chapters': [
            {'chapter': '05', 'reason': 'One working red in each view, and which red yields.'},
            {'chapter': '11', 'reason': 'Which red wins when an error, a step to take and a reform meet.'},
            {'chapter': '14', 'reason': 'The chart system the keys belong to.'},
            {'chapter': '15', 'reason': 'Systems graphics, where the marker and the layers do their work.'},
            {'chapter': '21', 'reason': 'The atlas, with its locator on every view.'},
        ],
    }


def main():
    T = C.Tokens(C.TOKENS_JSON, C.TOKENS_CSS)
    ctx = B.Ctx(T, {}, 'final')
    lab = json.loads(T10.LABELS_PATH.read_text())
    rows = {r['id']: r for r in lab['rows']}
    v7 = json.loads((T10.V7 if T10.V7.exists() else T10.V7_COMMITTED).read_text())
    figs = {}
    specimens(ctx, rows, v7, figs)
    existing = json.loads(OUT_CH.read_text()) if OUT_CH.exists() else None
    ch = chapter(ctx, figs, existing)
    B.check_chapter(ch)
    used = {r[kk]['specimen'] for r in ch['rules'] if r['id'] in MINE for kk in ('correct', 'failure', 'corrective') if r.get(kk)}
    missing, unused = used - set(ctx.specs), set(ctx.specs) - used
    if missing or unused:
        raise SystemExit(f'specimens missing {sorted(missing)} unused {sorted(unused)}')
    OUT_CH.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + '\n')
    for old in OUT_SP.glob('s-12-*.html'):
        if old.stem.split('-')[2] in DEVICES and old.stem not in ctx.specs:
            old.unlink()
    for sid, s in ctx.specs.items():
        (OUT_SP / f'{sid}.html').write_text(s['html'])
    man = json.loads(MANIFEST.read_text())
    man = {kk: v for kk, v in man.items() if not (str(v.get('chapter')) == CH and kk.split('-')[2] in DEVICES)}
    man.update({sid: s['meta'] for sid, s in ctx.specs.items()})
    MANIFEST.write_text(json.dumps(dict(sorted(man.items())), indent=1, ensure_ascii=False) + '\n')
    FIG_OUT.write_text(json.dumps({'about': 'Every figure chapter 12\'s systems rules print, and where it comes from.',
                                   'built': '2026-11-10', 'figures': {**figs, **ctx.figures}},
                                  indent=1, ensure_ascii=False, default=str) + '\n')
    print(f'chapter 12 systems: {len(MINE)} rules, {len(ctx.specs)} specimens; the file holds {len(ch["rules"])} rules')


if __name__ == '__main__':
    main()
