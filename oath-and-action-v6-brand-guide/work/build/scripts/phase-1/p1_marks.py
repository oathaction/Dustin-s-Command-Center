"""Items 7, 8 and 10: the hinge master, the small lockmark masters, the red ampersand on Prussian.

Hinge. Drawn from Dustin's mockups (a circle holding the ampersand on a line that joins OATH and
ACTION, nodes at both ends of each line, looping arrows above and below) and kept to V5's rules:
the original lettering anchors it, the arc is dotted and ends in one open arrowhead, UNDERSTAND
and IMPACT sit under the optical centres of their words, the ampersand is the master glyph in
Pillar Red. Every stroke is in drawing units, so the weight scales with the mark (V5 fixed the
arc at 1.25 px). Labels are Inter 600 outlines, tracked 0.08 em, with a 13 px minimum.

Lockmark. 16 and 24 px masters on whole pixels: 1 px links centred on pixel rows, nodes of 3 and
5 px, the lever one size up (5 and 7 px) so it still reads in one colour.

Prussian. Four treatments of the wordmark's ampersand on Prussian, measured after rendering.

Run: python3 -I p1_marks.py
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.append("/root/.local/lib/python3.13/site-packages")
import oa_p1 as o  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
from fontTools.pens.svgPathPen import SVGPathPen  # noqa: E402

D7 = o.OUT / "07-hinge"
D8 = o.OUT / "08-lockmark"
D10 = o.OUT / "10-prussian"


def text_outline(txt, font_file, cap_units, tracking_em=0.08):
    """Set a caps label as outlines. Returns (svg d in label units with cap top at y 0, width)."""
    f = TTFont(o.FONTS / font_file)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm
    capf = f["OS/2"].sCapHeight
    k = cap_units / capf
    x = 0.0
    ds = []
    for i, ch in enumerate(txt):
        gn = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[gn].draw(pen)
        p = o.path_from_d(pen.getCommands(), (k, 0, 0, -k, x, cap_units))
        ds.append(p)
        x += f["hmtx"][gn][0] * k
        if i < len(txt) - 1:
            x += tracking_em * upm * k
    u = o.union(*ds)
    b = o.bounds(u)
    u = o.tx(u, e=-b[0])
    return u, b[2] - b[0]


def word_paths():
    gl, amp = o.wordmark_letters()
    oath = o.union(*gl[:4])
    action = o.union(*gl[4:])
    ab = o.bounds(action)
    return oath, o.tx(action, e=-ab[0]), ab[2] - ab[0]


def arc_d(cx, cy, r, a0, a1):
    """Arc on screen from angle a0 to a1 (degrees, maths convention, y up), going clockwise."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
    large = 1 if (a0 - a1) % 360 > 180 else 0
    return f"M{p0[0]:.2f} {p0[1]:.2f}A{r} {r} 0 {large} 1 {p1[0]:.2f} {p1[1]:.2f}", p1


def arrow_d(px, py, ang_travel, length, spread=32):
    """Open chevron at (px, py) pointing along ang_travel (screen degrees)."""
    out = []
    for s in (-1, 1):
        a = math.radians(ang_travel + 180 + s * spread)
        out.append((px + length * math.cos(a), py + length * math.sin(a)))
    return f"M{out[0][0]:.2f} {out[0][1]:.2f}L{px:.2f} {py:.2f}L{out[1][0]:.2f} {out[1][1]:.2f}"


def hinge(compact=False):
    oath, action, aw = word_paths()
    line_w = 6.0 if compact else 3.5
    node_r = 12.0 if compact else 9.0
    gap_word, line_len, rc = 50.0, 120.0, 110.0
    cy = 54.0
    n1 = 358.67 + gap_word
    c_l = n1 + line_len
    cx = c_l + rc
    c_r = cx + rc
    n2 = c_r + line_len
    a_x = n2 + gap_word
    # ampersand: the V5 glyph re-exported, 1.25 x cap, centred on its ink in the circle
    amp = o.amp_glyph(0, 0, 0.14)
    ab = o.bounds(amp)
    s = 125.0 / (ab[3] - ab[1])
    amp = o.tx(amp, a=s, d=s, e=cx - (ab[0] + ab[2]) / 2 * s, f=cy - (ab[1] + ab[3]) / 2 * s)
    R = rc + 55.0
    top_d, top_end = arc_d(cx, cy, R, 158, 22)
    bot_d, bot_end = arc_d(cx, cy, R, -22, -158)
    # a clockwise arc ending at angle t travels along screen angle 90 - t at its end
    alen = 18.0 if not compact else 24.0
    parts = []
    parts.append(f'<path fill="currentColor" d="{o.d_from_path(oath)}"/>')
    parts.append(f'<path fill="currentColor" d="{o.d_from_path(o.tx(action, e=a_x))}"/>')
    st = f'fill="none" stroke="var(--line,#5D636D)" stroke-width="{line_w}" stroke-linecap="round" stroke-linejoin="round"'
    parts.append(f'<path {st} d="M{n1:.2f} {cy}H{c_l:.2f}M{c_r:.2f} {cy}H{n2:.2f}"/>')
    parts.append(f'<circle cx="{cx:.2f}" cy="{cy}" r="{rc}" {st}/>')
    dot = f'stroke-dasharray="0 {line_w * 2.6:.1f}"'
    parts.append(f'<path {st} {dot} d="{top_d}"/>')
    parts.append(f'<path {st} d="{arrow_d(top_end[0], top_end[1], 90 - 22, alen)}"/>')
    parts.append(f'<path {st} {dot} d="{bot_d}"/>')
    parts.append(f'<path {st} d="{arrow_d(bot_end[0], bot_end[1], 90 + 158, alen)}"/>')
    for x in (n1, c_l, c_r, n2):
        parts.append(f'<circle cx="{x:.2f}" cy="{cy}" r="{node_r}" fill="currentColor"/>')
    parts.append(f'<path fill="var(--amp,#E63946)" d="{o.d_from_path(amp)}"/>')
    top = cy - R - line_w - 6
    bottom = cy + R + line_w + 6
    if not compact:
        cap_l = 26.0
        lu, lw = text_outline("UNDERSTAND", "Inter-600-normal.ttf", cap_l)
        li, iw = text_outline("IMPACT", "Inter-600-normal.ttf", cap_l)
        ly = 104 + 36
        parts.append(f'<path fill="currentColor" d="{o.d_from_path(o.tx(lu, e=179.33 - lw / 2, f=ly))}"/>')
        parts.append(f'<path fill="currentColor" d="{o.d_from_path(o.tx(li, e=a_x + aw / 2 - iw / 2, f=ly))}"/>')
    vb = [-12.0, round(top, 2), round(a_x + aw + 24, 2), round(bottom - top, 2)]
    info = {"viewBox": vb, "line_units": line_w, "node_r": node_r, "circle_r": rc, "arc_r": R, "amp_height_x": 1.25,
            "label_cap_units": None if compact else 26.0}
    return "".join(parts), vb, info


def lockmark_small(size):
    if size == 16:
        cs, r, lr = [2.5, 7.5, 12.5], 1.5, 2.5
    else:
        cs, r, lr = [3.5, 11.5, 19.5], 2.5, 3.5
    links = []
    for c in cs:
        links.append(f'<rect x="{cs[0]}" y="{c - 0.5}" width="{cs[-1] - cs[0]}" height="1"/>')
        links.append(f'<rect x="{c - 0.5}" y="{cs[0]}" width="1" height="{cs[-1] - cs[0]}"/>')
    nodes = []
    for yy in cs:
        for xx in cs:
            if xx == cs[-1] and yy == cs[-1]:
                continue
            nodes.append(f'<circle cx="{xx}" cy="{yy}" r="{r}" fill="currentColor"/>')
    lever = f'<circle cx="{cs[-1]}" cy="{cs[-1]}" r="{lr}" fill="var(--lever,#E63946)"/>'
    body = f'<g fill="var(--link,#5D636D)">{"".join(links)}</g>{"".join(nodes)}{lever}'
    return body, [0, 0, size, size], {"node_centres_px": cs, "node_diameter_px": 2 * r, "lever_diameter_px": 2 * lr, "link_px": 1}


def build():
    for d in (D7, D8, D10):
        d.mkdir(parents=True, exist_ok=True)
    res = {}
    for compact in (False, True):
        body, vb, info = hinge(compact)
        nm = "Compact" if compact else "Display"
        fn = D7 / f"20261021_Hinge-{nm}-Master.svg"
        o.write_svg(fn, vb, body, f"Hinge {nm.lower()} master (proposal, Phase 1)")
        # minimum width for 13 px labels (display) or 1 px lines (compact)
        if compact:
            min_w = math.ceil(vb[2] * 1.0 / info["line_units"])
        else:
            cap_px_13 = 13 * 0.727
            min_w = math.ceil(vb[2] * cap_px_13 / info["label_cap_units"])
        info["min_width_px"] = min_w
        info["line_px_at_min"] = round(info["line_units"] * min_w / vb[2], 2)
        info["file"] = str(fn.relative_to(o.ROOT))
        res[f"hinge_{nm.lower()}"] = info
    for size in (16, 24):
        body, vb, info = lockmark_small(size)
        fn = D8 / f"20261021_Lockmark-{size}px-Master.svg"
        o.write_svg(fn, vb, body, f"Lockmark {size} px master on the pixel grid (proposal, Phase 1)")
        info["file"] = str(fn.relative_to(o.ROOT))
        res[f"lockmark_{size}"] = info
    # nominal contrast for the Prussian options
    res["prussian_nominal"] = {k: round(o.contrast(c, o.PRUS), 2) for k, c in (("Pillar Red", o.RED), ("Newsprint", o.NEWS), ("White", o.WHITE))}
    res["prussian_nominal"]["Pillar Red on Newsprint keyline"] = round(o.contrast(o.RED, o.NEWS), 2)
    return res


if __name__ == "__main__":
    r = build()
    (o.SCRATCH / "specs/marks.json").write_text(json.dumps(r, indent=1))
    print(json.dumps(r, indent=1))
