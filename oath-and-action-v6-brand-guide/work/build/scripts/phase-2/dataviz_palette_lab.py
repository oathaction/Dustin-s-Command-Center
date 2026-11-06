"""Palette lab for the data visualization round (November 6, 2026).

Usage:
    python3 -I work/build/scripts/phase-2/dataviz_palette_lab.py

Derives candidate data palettes from the locked palette by mixing in OKLab (D1-04), then measures each swatch on
White, Newsprint and Charcoal: WCAG contrast against the ground, OKLab lightness (the grayscale proof), and the
smallest OKLab distance between neighbors under simulated protanopia, deuteranopia and tritanopia
(Machado, Oliveira and Fernandes 2009, severity 1.0, applied in linear sRGB). Writes
work/boards/phase-2/data-viz/shared/20261106_Palette-Lab.json and a swatch sheet, 20261106_Palette-Lab.html.
These are starting candidates for the makers. Section 13 sends the diverging pair to Gate 2.
"""
import importlib.util
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location('oa_color', ROOT / 'work/build/scripts/phase-1/oa_color.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
P = C.PALETTE
DEEP_STONE = '#4E535B'
DIM_NEWSPRINT = '#A3A19C'
OUT = ROOT / 'work/boards/phase-2/data-viz/shared'
GROUNDS = {'white': P['white'], 'newsprint': P['newsprint'], 'charcoal': P['charcoal']}

# Machado et al. 2009, severity 1.0, linear RGB
CVD = {
    'protanopia': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    'deuteranopia': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    'tritanopia': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def simulate(h, kind):
    r, g, b = (C.lin(c) for c in C.hex_to_rgb(h))
    m = CVD[kind]
    out = [m[i][0] * r + m[i][1] * g + m[i][2] * b for i in range(3)]
    return C.rgb_to_hex(tuple(C.delin(min(1, max(0, v))) for v in out))


def mix(a, b, t):
    return C.mix_oklab(a, b, t)[0]


def L(h):
    return round(C.to_oklab(h)[0], 3)


def measure(name, swatches, ground, kind):
    g = GROUNDS[ground]
    rows = [{'label': lab, 'hex': hx, 'contrast_on_ground': round(C.contrast(hx, g), 2), 'oklab_L': L(hx),
             **{f'sim_{k}': simulate(hx, k) for k in CVD}} for lab, hx in swatches]
    pairs = list(zip(rows, rows[1:])) if kind in ('sequential', 'diverging', 'ramp') else [(a, b) for i, a in enumerate(rows) for b in rows[i + 1:]]
    worst = {}
    for k in ['normal'] + list(CVD):
        key = 'hex' if k == 'normal' else f'sim_{k}'
        ds = [(round(C.delta_e_ok(a[key], b[key]), 3), a['label'], b['label']) for a, b in pairs]
        worst[k] = min(ds) if ds else None
    lsteps = [round(abs(a['oklab_L'] - b['oklab_L']), 3) for a, b in zip(rows, rows[1:])]
    return {'name': name, 'ground': ground, 'kind': kind, 'swatches': rows, 'min_neighbor_delta_e': worst,
            'lightness_steps': lsteps, 'min_lightness_step': min(lsteps) if lsteps else None,
            'grayscale_monotonic': all(x > y for x, y in zip([r['oklab_L'] for r in rows], [r['oklab_L'] for r in rows][1:])) or
                                   all(x < y for x, y in zip([r['oklab_L'] for r in rows], [r['oklab_L'] for r in rows][1:]))}


def ramp(base, ground, steps, light_end=0.82, dark_end=0.0):
    """Light to dark: from base mixed `light_end` toward the ground, to base, then toward Charcoal by dark_end."""
    out = []
    n = steps - 1
    for i in range(steps):
        t = i / n
        if dark_end > 0:
            # first part to the base, last step past it toward Charcoal
            pos = t * (light_end + dark_end)
            hx = mix(base, GROUNDS[ground], light_end - pos) if pos <= light_end else mix(base, P['charcoal'], pos - light_end)
        else:
            hx = mix(base, GROUNDS[ground], light_end * (1 - t))
        out.append(hx)
    return out


sets = []
for ground in ('white', 'newsprint'):
    g = GROUNDS[ground]
    sets.append(measure('Roles', [('Emphasis: the named series (Charcoal)', P['charcoal']), ('Context (Stone)', P['stone']),
                                  ('Secondary text (Deep Stone)', DEEP_STONE), ('Gridline (Stone 70% toward ground)', mix(P['stone'], g, 0.70)),
                                  ('Baseline (Charcoal)', P['charcoal'])], ground, 'roles'))
    sets.append(measure('Categorical, four inks', [('Prussian', P['prussian']), ('Verdigris', P['verdigris']), ('Stone', P['stone']),
                                                   ('Verdigris tint 55%', mix(P['verdigris'], g, 0.55))], ground, 'categorical'))
    sets.append(measure('Sequential Verdigris, five steps', [(f'Step {i + 1}', h) for i, h in enumerate(ramp(P['verdigris'], ground, 5, 0.82, 0.35))], ground, 'sequential'))
    sets.append(measure('Sequential Prussian, five steps', [(f'Step {i + 1}', h) for i, h in enumerate(ramp(P['prussian'], ground, 5, 0.86, 0.0))], ground, 'sequential'))
    neutral = mix(P['stone'], g, 0.86)
    sets.append(measure('Diverging A, one-sided: Stone, neutral, Verdigris', [
        ('Stone, strong', P['stone']), ('Stone, light', mix(P['stone'], g, 0.55)), ('Neutral midpoint', neutral),
        ('Verdigris, light', mix(P['verdigris'], g, 0.55)), ('Verdigris, strong', mix(P['verdigris'], P['charcoal'], 0.25))], ground, 'diverging'))
    sets.append(measure('Diverging B, two-sided: Prussian, ground, Verdigris', [
        ('Prussian, strong', P['prussian']), ('Prussian, light', mix(P['prussian'], g, 0.62)), ('Midpoint (ground tint)', mix(P['stone'], g, 0.90)),
        ('Verdigris, light', mix(P['verdigris'], g, 0.55)), ('Verdigris, strong', mix(P['verdigris'], P['charcoal'], 0.25))], ground, 'diverging'))
    sets.append(measure('Evidence grade ramp (single ink, add texture for contested)', [
        ('Documented', P['charcoal']), ('Well supported', mix(P['charcoal'], g, 0.38)), ('Plausible', mix(P['charcoal'], g, 0.64)),
        ('Contested (pair with hatching)', mix(P['charcoal'], g, 0.84))], ground, 'ramp'))
    sets.append(measure('Pillar Red as the one point (needs a Charcoal keyline under 3:1)', [('Pillar Red', P['pillarRed'])], ground, 'roles'))

dark = 'charcoal'
gd = GROUNDS[dark]
sets.append(measure('Roles', [('Emphasis: the named series (Newsprint)', P['newsprint']), ('Context (Dim Newsprint)', DIM_NEWSPRINT),
                              ('Context, quieter (Stone 35% toward Newsprint)', mix(P['stone'], P['newsprint'], 0.35)),
                              ('Gridline (Stone 45% toward Charcoal)', mix(P['stone'], gd, 0.45))], dark, 'roles'))
sets.append(measure('Categorical, four inks (lifted for Charcoal)', [('Prussian lifted 55% toward Newsprint', mix(P['prussian'], P['newsprint'], 0.55)),
                                                                     ('Verdigris lifted 30% toward Newsprint', mix(P['verdigris'], P['newsprint'], 0.30)),
                                                                     ('Dim Newsprint', DIM_NEWSPRINT), ('Newsprint', P['newsprint'])], dark, 'categorical'))
sets.append(measure('Sequential Verdigris on Charcoal, five steps', [(f'Step {i + 1}', mix(P['verdigris'], gd, t)) if t >= 0 else (f'Step {i + 1}', mix(P['verdigris'], P['newsprint'], -t))
                                                                     for i, t in enumerate([0.75, 0.5, 0.2, -0.25, -0.55])], dark, 'sequential'))
sets.append(measure('Pillar Red as the one point', [('Pillar Red', P['pillarRed'])], dark, 'roles'))

out = {'built': '2026-11-06', 'about': __doc__.strip().splitlines()[0], 'method': 'OKLab mixing (D1-04); Machado 2009 CVD simulation; WCAG 2.x contrast',
       'thresholds': {'graphic_contrast': 3.0, 'text_contrast': 4.5,
                      'note': 'Essential marks need 3:1 against the ground (WCAG 1.4.11). Fills inside a scale may fall under 3:1 when every value is printed or the table equivalent carries it; that is a design judgment and must be labeled so.'},
       'sets': sets}
(OUT / '20261106_Palette-Lab.json').write_text(json.dumps(out, indent=1))

# swatch sheet
bg = {'white': '#FFFFFF', 'newsprint': '#DCD9D2', 'charcoal': '#121212'}
fg = {'white': '#121212', 'newsprint': '#121212', 'charcoal': '#DCD9D2'}
html = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
        '<title>Palette Lab</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Inter+Tight:wght@800&display=swap">',
        '<style>body{margin:0;font:15px/1.45 Inter,sans-serif;background:#fff;color:#121212}main{max-width:1180px;margin:0 auto;padding:32px 20px}h1{font:800 34px/1.1 "Inter Tight",sans-serif;margin:0 0 6px}'
        'section{padding:18px 20px;margin:14px 0}h2{font:600 15px/1.3 Inter,sans-serif;margin:0 0 10px}.row{display:flex;flex-wrap:wrap;gap:8px}.sw{width:132px;font:13px/1.3 Inter,sans-serif;font-variant-numeric:tabular-nums}'
        '.chip{height:44px;border-radius:2px}.sim{display:flex;gap:2px;margin-top:3px}.sim span{flex:1;height:12px}.meta{font-size:13px;margin-top:8px}</style></head><body><main>',
        '<h1>Palette lab</h1><p>Candidate data palettes from the locked palette, mixed in OKLab. Under each chip: hex, contrast on the ground, OKLab lightness, then strips simulating protanopia, deuteranopia and tritanopia.</p>']
for s in sets:
    gnd = s['ground']
    html.append(f'<section style="background:{bg[gnd]};color:{fg[gnd]}"><h2>{s["name"]} on {gnd.capitalize()}</h2><div class="row">')
    for w in s['swatches']:
        html.append(f'<div class="sw"><div class="chip" style="background:{w["hex"]}"></div><div class="sim">' +
                    ''.join(f'<span style="background:{w["sim_" + k]}" title="{k}"></span>' for k in CVD) +
                    f'</div><div>{w["label"]}</div><div>{w["hex"]} · {w["contrast_on_ground"]}:1 · L {w["oklab_L"]}</div></div>')
    m = s['min_neighbor_delta_e']
    html.append('</div><div class="meta">Smallest OKLab distance between ' + ('neighbors' if s['kind'] in ('sequential', 'diverging', 'ramp') else 'any two') + ': ' +
                ', '.join(f'{k} {v[0]}' for k, v in m.items() if v) + (f'. Smallest lightness step {s["min_lightness_step"]}; grayscale order holds: {"yes" if s["grayscale_monotonic"] else "no"}.' if s['min_lightness_step'] is not None else '') +
                '</div></section>')
html.append('</main></body></html>')
(OUT / '20261106_Palette-Lab.html').write_text('\n'.join(html))
for s in sets:
    m = s['min_neighbor_delta_e']
    print(f'{s["ground"]:9s} {s["name"][:46]:46s} contrast {[w["contrast_on_ground"] for w in s["swatches"]]} '
          f'dE min {[(k[:4], v[0]) for k, v in m.items() if v]} Lsteps {s["lightness_steps"]}')
