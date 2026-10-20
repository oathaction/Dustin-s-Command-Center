"""Phase 0 identity geometry audit.

Reads the V5 Polished sprite extracts (work/extract/v5-polished/sprite) and
measures the wordmark, ampersand and lockup symbols from their outlines.
Writes JSON to the path given as the second argument.

Run: python3 -I identity_geometry.py <sprite_dir> <out.json>
"""
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oa_geom import *  # noqa: E402,F403

SPRITE = Path(sys.argv[1])
OUT = Path(sys.argv[2])

def load_symbol(name):
    return (SPRITE / f"{name}.svg").read_text()


res = {}

# ---------- wordmark ----------
wm = strip_defs(load_symbol("wordmark"))
parts = collect_polys(wm)
letters, amp = [], None
for polys, is_amp in parts:
    if is_amp:
        amp = polys
    else:
        letters.extend(polys)
glyphs = group_glyphs(letters)
names = ["O", "A", "T", "H", "A2", "C", "T2", "I", "O2", "N"]
assert len(glyphs) == 10, len(glyphs)
gl = {n: g for n, g in zip(names, glyphs)}
gl_amp = {"box": bbox(amp), "polys": amp}
CAP_TOP, BASE = 4.0, 104.0
CAP = BASE - CAP_TOP
res["wordmark_viewbox"] = viewbox(wm)
res["cap_height_units"] = CAP
res["glyph_boxes"] = {n: [round(v, 2) for v in gl[n]["box"]] for n in names}
res["amp_box_in_wordmark"] = [round(v, 2) for v in gl_amp["box"]]
ab = gl_amp["box"]
res["amp_overshoot"] = {
    "above_cap_units": round(CAP_TOP - ab[1], 2),
    "below_base_units": round(ab[3] - BASE, 2),
    "above_cap_x": round((CAP_TOP - ab[1]) / CAP, 4),
    "below_base_x": round((ab[3] - BASE) / CAP, 4),
    "ink_height_x": round((ab[3] - ab[1]) / CAP, 4),
    "O_overshoot_units": round(CAP_TOP - gl["O"]["box"][1], 2),
}

seq = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]
lookup = dict(gl)
lookup["&"] = gl_amp
pairs = {}
for a, b in zip(seq, seq[1:]):
    pm = pair_metrics(lookup[a]["polys"], lookup[b]["polys"], CAP_TOP, BASE)
    pm["bbox_gap"] = round(lookup[b]["box"][0] - lookup[a]["box"][2], 2)
    pm["min_gap_x"] = round(pm["min_gap"] / CAP, 4)
    pairs[f"{a.rstrip('2')}{b.rstrip('2')}" + ("_action" if a.endswith("2") or b.endswith("2") else "")] = pm
res["pairs"] = pairs


# stem and bar thickness, measured on scanlines through the outlines
def run_at_y(polys, y):
    xs = crossings(polys, y)
    return [round(xs[k + 1] - xs[k], 2) for k in range(0, len(xs) - 1, 2)]


def run_at_x(polys, x):
    ys = vcrossings(polys, x)
    return [round(ys[k + 1] - ys[k], 2) for k in range(0, len(ys) - 1, 2)]


meas = {
    "H_stems_at_y30": run_at_y(gl["H"]["polys"], 30),
    "H_bar_at_x315": run_at_x(gl["H"]["polys"], 315),
    "T_bar_at_x190": run_at_x(gl["T"]["polys"], 190),
    "T_stem_at_y60": run_at_y(gl["T"]["polys"], 60),
    "I_stem_at_y60": run_at_y(gl["I"]["polys"], 60),
    "N_at_y20": run_at_y(gl["N"]["polys"], 20),
    "N_at_y54": run_at_y(gl["N"]["polys"], 54),
    "O_sides_at_y54": run_at_y(gl["O"]["polys"], 54),
    "O_top_bottom_at_x47.7": run_at_x(gl["O"]["polys"], 47.72),
    "C_at_y54": run_at_y(gl["C"]["polys"], 54),
    "A_bar_at_x143": run_at_x(gl["A"]["polys"], 143),
    "A_legs_at_y54": run_at_y(gl["A"]["polys"], 54),
}
# ampersand, in wordmark units (glyph transform translate(365.5 104) scale .14)
G = lambda gx: 365.5 + gx * 0.14
GY = lambda gy: 104 - gy * 0.14
meas["amp_upper_loop_sides_at_glyph_y530"] = run_at_y(amp, GY(530))
meas["amp_lower_bowl_at_glyph_y200"] = run_at_y(amp, GY(200))
meas["amp_bowl_bottom_and_loop_top_at_glyph_x283"] = run_at_x(amp, G(283))
meas["amp_arm_at_glyph_y255"] = run_at_y(amp, GY(255))
meas["amp_serif_at_glyph_x560"] = run_at_x(amp, G(560))
meas["amp_tail_at_glyph_x620"] = run_at_x(amp, G(620))
# diagonal: perpendicular distance between its two edges
p1, p2, q1 = (318, 364), (480, 205), (208, 308)
dx, dy = p2[0] - p1[0], p2[1] - p1[1]
L = math.hypot(dx, dy)
nx, ny = -dy / L, dx / L
meas["amp_diagonal_perpendicular_units"] = round(abs((q1[0] - p1[0]) * nx + (q1[1] - p1[1]) * ny) * 0.14, 2)
# notch between diagonal and arm: mouth width and depth
mouth = math.hypot(432 - 346, 331 - 335) * 0.14
depth = math.hypot(480 - (432 + 346) / 2, 205 - (331 + 335) / 2) * 0.14
meas["amp_arm_notch_mouth_units"] = round(mouth, 2)
meas["amp_arm_notch_depth_units"] = round(depth, 2)
meas["amp_upper_counter_w_h_units"] = [round((349 - 216) * 0.14, 2), round((646 - 417) * 0.14, 2)]
res["stroke_measures_units"] = meas

# ---------- clipping: glyph ink against each symbol's own viewBox ----------
clip = {}
for name in ["wordmark", "wordmark-mono", "stacked", "monogram", "amp", "amp-16", "tl-1", "tl-2a", "tl-2b",
             "url-1", "lbl-understand", "lbl-impact", "pw-act", "pw-track", "pw-connect", "pw-explain",
             "word-oath", "word-action", "word-o", "word-a"]:
    s = strip_defs(load_symbol(name))
    vb = viewbox(s)
    polys = [p for pp, _ in collect_polys(s) for p in pp]
    b = bbox(polys)
    sw = re.search(r'stroke-width="(' + NUM + ')"', s)
    pad = 0.0
    if sw and name == "amp-16":
        pad = float(sw.group(1)) * 0.14 / 2
    over = {
        "left": round(vb[0] - (b[0] - pad), 2),
        "top": round(vb[1] - (b[1] - pad), 2),
        "right": round((b[2] + pad) - (vb[0] + vb[2]), 2),
        "bottom": round((b[3] + pad) - (vb[1] + vb[3]), 2),
    }
    clip[name] = {"viewBox": vb, "ink_box": [round(v, 2) for v in b],
                  "overflow_units": {k: v for k, v in over.items() if v > 0.05}}
res["clipping"] = clip

# ---------- amp-16 versus amp ----------
a16 = load_symbol("amp-16")
sw = float(re.search(r'stroke-width="(' + NUM + ')"', a16).group(1))
vb16 = viewbox(a16)
vba = viewbox(load_symbol("amp"))
res["amp16"] = {
    "stroke_width_glyph_units": sw,
    "stroke_width_symbol_units": round(sw * 0.14, 3),
    "added_weight_per_side_px_at_16px_tall": round(sw * 0.14 / 2 * 16 / vb16[3], 3),
    "glyph_scale_vs_amp_at_same_height": round(vba[3] / vb16[3], 4),
    "note": "same outline as amp, stroked with round join, in a padded viewBox",
}

# ---------- stacked, monogram, lockmark, hinge ----------
st = strip_defs(load_symbol("stacked"))
sp = collect_polys(st)
st_amp = [p for pp, a in sp if a for p in pp]
st_letters = [p for pp, a in sp if not a for p in pp]
sab = bbox(st_amp)
res["stacked"] = {
    "viewBox": viewbox(st),
    "amp_box": [round(v, 2) for v in sab],
    "amp_height_over_cap": round((sab[3] - sab[1]) / CAP, 3),
    "line_gap_units": round(113.96 - 104.0, 2),
    "amp_gap_to_N": round(sab[0] - 502.43, 2),
}
mg = strip_defs(load_symbol("monogram"))
mp = collect_polys(mg)
m_amp = [p for pp, a in mp if a for p in pp]
m_let = group_glyphs([p for pp, a in mp if not a for p in pp])
res["monogram"] = {
    "O_amp": pair_metrics(m_let[0]["polys"], m_amp, CAP_TOP, BASE),
    "amp_A": pair_metrics(m_amp, m_let[1]["polys"], CAP_TOP, BASE),
}

lm = load_symbol("lockmark")
nodes = [(float(a), float(b), float(c)) for a, b, c in re.findall(r'<circle cx="(' + NUM + ')" cy="(' + NUM + ')" r="(' + NUM + ')"', lm)]
lines = sorted({float(v) for v in re.findall(r'x1="(' + NUM + ')"', lm)})
lk = {"viewBox": viewbox(lm), "line_positions": lines, "node_r": nodes[0][2], "lever_r": nodes[-1][2],
      "link_stroke": "1 px, vector-effect non-scaling-stroke", "by_size": {}}
for px in [16, 24, 32, 48, 96, 240]:
    s = px / 123.5
    lk["by_size"][px] = {
        "line_centers_px": [round(v * s, 2) for v in lines],
        "node_diameter_px": round(nodes[0][2] * 2 * s, 2),
        "lever_diameter_px": round(nodes[-1][2] * 2 * s, 2),
        "pitch_px": round(50 * s, 2),
        "link_to_node_ratio": round(1 / (nodes[0][2] * 2 * s), 2),
    }
res["lockmark"] = lk

hg = load_symbol("hinge")
body = hg[hg.find("</defs>"):]
res["hinge"] = {
    "viewBox": viewbox(hg),
    "arc": re.search(r'<path d="(M[^"]+)"[^>]*stroke-dasharray="([^"]+)"', body).groups(),
    "label_height_units": 20,
    "label_cap_height_units": round(20 * (105.54 - 2.66) / 108, 2),
    "min_width_for_13px_label_font": None,
}
# Inter cap height is about 0.727 em; a 13 px label has a cap height near 9.45 px
cap_units = 20 * 100 / 108
scale_needed = 9.45 / cap_units
res["hinge"]["min_width_for_13px_label_font"] = round(1010.71 * scale_needed)
res["hinge"]["min_height_for_13px_label_font"] = round(298 * scale_needed)

# stated V5 minima translated into cap height
res["v5_minimum_translations"] = {
    "L1_120px_wide": {"height_px": round(120 * 108 / 970.71, 2), "cap_px": round(120 * 100 / 970.71, 2),
                       "amp_thinnest_stroke_px": round(120 / 970.71 * 9.24, 2)},
    "L2_72px_wide": {"height_px": round(72 * 217.96 / 628.93, 2), "cap_px": round(72 * 100 / 628.93, 2)},
    "L8_48px_wide": {"height_px": round(48 * 108 / 304.65, 2), "cap_px": round(48 * 100 / 304.65, 2)},
}

OUT.write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
