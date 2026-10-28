"""I6, I7 and S9: the hinge diagram V2, the lockmark small masters and the hinge-circle badge.

I6  Hinge diagram V2, display and compact masters, at today's width and at the condensed width:
    OATH and ACTION on a line with four nodes, ampersand B in a circle at the center, two solid
    hairline arcs running clockwise with open chevrons, UNDERSTAND and IMPACT under the words on
    the display master. The words are the display wordmark masters' own letters and spacing. The
    ampersand is B's display drawing at 1.25 cap heights, centered on its ink, so its waist
    crossing sits on the center line with the nodes. Construction is Phase 1's (p1_marks.hinge).
I7  Lockmark 16 and 24 px masters: node centers on whole pixels (2.5, 7.5, 12.5 and 3.5, 11.5,
    19.5), 1 px links centered on pixel rows, the lever one size up. V5's master from 48 px.
S9  Hinge-circle badge: B in the hinge diagram's ring, no words. 16 px: a 1 px pixel ring around
    a 10 by 10 px ampersand area-sampled from B's 16 px master and corrected by hand; 24 px: the
    ring around B's 16 px master itself; display: the V2 ring proportions, ring raised to 4.6 units.

Run: python3 -I p2_marks.py
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402
import p1_marks as M1  # noqa: E402
import p2_amp_b as B2  # noqa: E402
import p2_wordmark as WM  # noqa: E402
import p2_condensed as CD  # noqa: E402

CY = 54.0


def words(width):
    if width == "condensed":
        parts = CD.display()[0]
        return CD.oath_action(parts)
    parts = WM.display_parts()[0]
    oath = o.union(*[parts[n] for n in ("O", "A", "T", "H")])
    action = o.union(*[parts[n] for n in ("A2", "C", "T2", "I", "O2", "N")])
    ab = o.bounds(action)
    return oath, o.tx(action, e=-ab[0]), ab[2] - ab[0]


def amp_in_ring(cx, cy, h=125.0):
    """B's display drawing scaled to h units tall, centered on its ink box at (cx, cy)."""
    q = B2.display_symbol()
    b = o.bounds(q)
    s = h / (b[3] - b[1])
    q = o.tx(q, a=s, d=s, e=cx - (b[0] + b[2]) / 2 * s, f=cy - (b[1] + b[3]) / 2 * s)
    # the waist crossing, carried through the same transform (font units to symbol units first)
    g = B2.glyph()
    gb = o.bounds(g)
    c = B2.crossing(B2.G)
    sx = (c[0] - gb[0]) * B2.K
    sy = (B2.CAP - c[1]) * B2.K
    cross = (cx + (sx - (b[0] + b[2]) / 2) * s, cy + (sy - (b[1] + b[3]) / 2) * s)
    return q, cross


def hinge(width="regular", compact=False):
    oath, action, aw = words(width)
    ob = o.bounds(oath)
    line_w = 6.0 if compact else 3.5
    node_r = 12.0 if compact else 9.0
    gap_word, line_len, rc = 50.0, 120.0, 110.0
    cy = CY
    n1 = ob[2] + gap_word
    c_l = n1 + line_len
    cx = c_l + rc
    c_r = cx + rc
    n2 = c_r + line_len
    a_x = n2 + gap_word
    amp, cross = amp_in_ring(cx, cy)
    R = rc + 55.0
    top_d, top_end = M1.arc_d(cx, cy, R, 158, 22)
    bot_d, bot_end = M1.arc_d(cx, cy, R, -22, -158)
    alen = 24.0 if compact else 18.0
    st = f'fill="none" stroke="var(--line,#5D636D)" stroke-width="{line_w:g}" stroke-linecap="round" stroke-linejoin="round"'
    arc_w = line_w * (1.0 if compact else 0.8)
    sa = f'fill="none" stroke="var(--line,#5D636D)" stroke-width="{arc_w:g}" stroke-linecap="round" stroke-linejoin="round"'
    parts = [f'<path fill="currentColor" d="{o.d_from_path(oath)}"/>',
             f'<path fill="currentColor" d="{o.d_from_path(o.tx(action, e=a_x))}"/>',
             f'<path {st} d="M{n1:.2f} {cy}H{c_l:.2f}M{c_r:.2f} {cy}H{n2:.2f}"/>',
             f'<circle cx="{cx:.2f}" cy="{cy}" r="{rc:g}" {st}/>',
             f'<path {sa} d="{top_d}"/>', f'<path {sa} d="{M1.arrow_d(top_end[0], top_end[1], 90 - 22, alen)}"/>',
             f'<path {sa} d="{bot_d}"/>', f'<path {sa} d="{M1.arrow_d(bot_end[0], bot_end[1], 90 + 158, alen)}"/>']
    parts += [f'<circle cx="{x:.2f}" cy="{cy}" r="{node_r:g}" fill="currentColor"/>' for x in (n1, c_l, c_r, n2)]
    parts.append(f'<path fill="var(--amp,#E63946)" d="{o.d_from_path(amp)}"/>')
    top, bottom = cy - R - line_w - 6, cy + R + line_w + 6
    label = None
    if not compact:
        cap_l = 26.0
        lu, lw = M1.text_outline("UNDERSTAND", "Inter-600-normal.ttf", cap_l)
        li, iw = M1.text_outline("IMPACT", "Inter-600-normal.ttf", cap_l)
        ly = 104 + 36
        oc = (ob[0] + ob[2]) / 2
        parts.append(f'<path fill="currentColor" d="{o.d_from_path(o.tx(lu, e=oc - lw / 2, f=ly))}"/>')
        parts.append(f'<path fill="currentColor" d="{o.d_from_path(o.tx(li, e=a_x + aw / 2 - iw / 2, f=ly))}"/>')
        label = cap_l
        left = min(0.0, oc - lw / 2)
    else:
        left = 0.0
    vb = [round(left - 12, 2), round(top, 2), round(a_x + aw + 24 - (left - 12), 2), round(bottom - top, 2)]
    if compact:
        min_w = math.ceil(vb[2] / min(line_w, arc_w))
    else:
        min_w = math.ceil(vb[2] * 13 * 0.727 / label)       # Inter's cap height is 0.727 em: 13 px labels
    info = {"viewBox": vb, "line_units": line_w, "arc_units": arc_w, "node_r": node_r, "circle_r": rc, "arc_r": R, "amp_height_x": 1.25,
            "label_cap_units": label, "min_width_px": min_w, "line_px_at_min": round(line_w * min_w / vb[2], 2), "arc_px_at_min": round(arc_w * min_w / vb[2], 2),
            "waist_crossing_offset_from_center_line_units": round(cross[1] - cy, 2), "words_width": "condensed 7.5 to 1" if width == "condensed" else "today's width"}
    return "".join(parts), vb, info


# ---------------------------------------------------------------- lockmark

def pixel_disc(cx, cy, d):
    """A disc d px across, drawn in whole pixels, centered on the pixel at (cx, cy)."""
    rows = {5: [1, 2, 2, 2, 1], 7: [1, 2, 3, 3, 3, 2, 1]}[d]
    x0, y0 = int(cx - 0.5), int(cy - 0.5)
    h = len(rows) // 2
    rects = "".join(f'<rect x="{x0 - r}" y="{y0 - h + i}" width="{2 * r + 1}" height="1"/>' for i, r in enumerate(rows))
    return rects


def lockmark(size):
    """16 px: Phase 1's master (vector discs, 0.6 crisp). 24 px: the same layout with the nodes and the
    lever drawn as whole-pixel discs, so every ink pixel is solid."""
    if size == 16:
        return M1.lockmark_small(16)
    cs, nd, ld = [3.5, 11.5, 19.5], 5, 7
    links = []
    for c in cs:
        links.append(f'<rect x="{cs[0]}" y="{c - 0.5}" width="{cs[-1] - cs[0]}" height="1"/>')
        links.append(f'<rect x="{c - 0.5}" y="{cs[0]}" width="1" height="{cs[-1] - cs[0]}"/>')
    nodes = "".join(pixel_disc(x, y, nd) for y in cs for x in cs if not (x == cs[-1] and y == cs[-1]))
    lever = pixel_disc(cs[-1], cs[-1], ld)
    body = f'<g fill="var(--link,#5D636D)">{"".join(links)}</g><g fill="currentColor">{nodes}</g><g fill="var(--lever,#E63946)">{lever}</g>'
    return body, [0, 0, 24, 24], {"node_centres_px": cs, "node_diameter_px": nd, "lever_diameter_px": ld, "link_px": 1, "nodes": "whole-pixel discs"}


# ---------------------------------------------------------------- badge

BADGE_AMP_16 = [      # rows 3 to 12 of the 16 px field, columns 0 to 15; '#' is ink
    "......###.......",   # loop top
    ".....##.##......",   # loop counter, three rows: the loop stays the taller part, as in B
    ".....##.##......",
    ".....##.##......",
    "......###..##...",   # the pinch above the crossing, and the arm's top
    ".....####.##....",   # the crossing: the line between rows 7 and 8 is the badge's center line
    "....##..###.....",   # bowl, lower counter, diagonal meeting the arm
    "....##...##.....",
    "....##...###....",
    ".....#######....",   # bowl bottom and the tail, foot on the baseline, clear of the ring
]


def pixmap(rows, ox, oy):
    p = None
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "#":
                r = o.rect(x + ox, y + oy, x + ox + 1, y + oy + 1)
                p = r if p is None else o.union(p, r)
    return o.simplify(p)


def pixring(n, r_out, r_in):
    c = n / 2
    p = None
    for y in range(n):
        for x in range(n):
            k = sum(r_in <= math.hypot(x + (sx + .5) / 4 - c, y + (sy + .5) / 4 - c) <= r_out for sy in range(4) for sx in range(4))
            if k >= 8:
                r = o.rect(x, y, x + 1, y + 1)
                p = r if p is None else o.union(p, r)
    return o.simplify(p)


def badge(key):
    if key == 16:
        ring, amp = pixring(16, 8, 7), pixmap(BADGE_AMP_16, 0, 3)
        return ring, amp, 16
    if key == 24:
        ring = pixring(24, 12, 11)
        amp = o.tx(B2.b16(), e=5, f=4)
        return ring, amp, 24
    ring = o.ring(120, 120, 112.3, 107.7)
    amp, _ = amp_in_ring(120, 120)
    return ring, amp, 240


def centroid_x(p, n):
    """Ink centroid of a pixel drawing, as offset from the field center in px."""
    import numpy as np
    g = P.to_shapely(p)
    c = g.centroid
    return round(c.x - n / 2, 2), round(c.y - n / 2, 2)


def export():
    out = {}
    for width in ("regular", "condensed"):
        for compact in (False, True):
            body, vb, info = hinge(width, compact)
            nm = ("Compact" if compact else "Display") + ("-Condensed" if width == "condensed" else "")
            f = P.write_svg(P.asset("hinge", f"{P.DATE}_Hinge-Diagram-V2-{nm}-Master.svg"), vb, body,
                            f"Hinge diagram V2, {'compact' if compact else 'display'} master, {info['words_width']}, ampersand B (Phase 2)")
            info["file"] = P.rel(f)
            out[f"hinge_{width}_{'compact' if compact else 'display'}"] = info
    for size in (16, 24):
        body, vb, info = lockmark(size)
        f = P.write_svg(P.asset("lockmark", f"{P.DATE}_Lockmark-{size}px-Master.svg"), vb, body, f"Lockmark {size} px master on the pixel grid (I7, Phase 2)")
        info["file"] = P.rel(f)
        info["use_range_px"] = "16 to 23" if size == 16 else "24 to 47"
        out[f"lockmark_{size}"] = info
    lm, lvb = P.svg_parts(o.SPRITE / "lockmark.svg")
    f = P.write_svg(P.asset("lockmark", f"{P.DATE}_Lockmark-Master-V5.svg"), lvb, lm, "Lockmark master, V5 geometry unchanged, for 48 px and up (I7)")
    out["lockmark_master"] = {"file": P.rel(f), "viewBox": lvb, "use_range_px": "48 and up"}
    for key in (16, 24, "display"):
        ring, amp, n = badge(key)
        body = f'<path fill="currentColor" d="{o.d_from_path(o.union(ring, amp), 3)}"/>'
        f = P.write_svg(P.asset("badge", f"{P.DATE}_Hinge-Badge-{key if key != 'display' else 'Display'}{'px' if key != 'display' else ''}-Master.svg"),
                        [0, 0, n, n], body, f"Hinge-circle badge, {key if key != 'display' else 'display'}{' px' if key != 'display' else ''} master, ampersand B (S9, Phase 2)")
        info = {"file": P.rel(f), "viewBox": [0, 0, n, n]}
        if key != "display":
            info["amp_centroid_offset_px"] = centroid_x(amp, n)
        out[f"badge_{key}"] = info
    P.save_json(P.SCRATCH / "specs/marks.json", out)
    return out


if __name__ == "__main__":
    print(json.dumps(export(), indent=1))
