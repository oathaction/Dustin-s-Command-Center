"""Direction C, Loop Lines: the composed views. Poster on Prussian, working map on Newsprint, reform view on White,
and the poster band that heads the catalog page. One Layout (maps_r2_c_geom.Layout) feeds all four, so every
station sits in the same place on every view (Harvard Growth Lab rule, research 4.8)."""
import math

import maps_r2_c_draw as D
import maps_r2_c_geom as G

M, LOOPS = G.M, G.LOOPS
T, esc = D.T, D.esc
W, H = 1440, 960
FRAME = 44
CELL = 36
OX, OY = 506, 452

# Line bullets: where each loop's chip sits, in cells from its first station (layout data, like the station table)
BULLETS = {
    "R1": (-3.0, 4.0), "R1b": (5.0, 2.6), "R2": (1.6, -1.3), "R3": (-1.0, -1.0), "R4a": (-1.4, 1.25),
    "R4b": (5.0, -3.6), "R5": (-1.6, -0.7), "R6": (2.4, 2.2), "R7": (3.2, -1.2), "R8": (0.0, 1.2),
    "R10": (-1.6, 1.4), "R11": (-1.4, 1.3), "R12": (-3.0, -1.5), "R13": (-2.8, 1.4), "R15": (2.1, -3.0),
    "R16": (-1.2, -1.6), "R18": (1.6, 0.0), "B1a": (3.2, 1.0), "B4": (1.3, 1.5), "B5": (3.0, 1.6),
}
DISTRICT_NAME_AT = {  # cells: the district letter's left baseline
    "A": (-12.3, -2.6), "B": (4.5, -9.6), "C": (18.9, 1.4), "D": (18.9, 11.3), "E": (6.0, 10.35),
}
DISTRICT_WRAP = {"A": False, "B": False, "C": True, "D": True, "E": False}
DISTRICT_TITLE = {"A": "Economic structure", "B": "Political inputs", "C": "Electoral competition",
                  "D": "Governing institutions", "E": "Legitimacy"}


def label_keepout(L, pad=10):
    """Grid points under each station name (and a pad), closed to routed corridors."""
    th = D.Theme("prussian")
    cells = set()
    for sid in G.STATIONS:
        _, box = D.station_shape(L, sid, th)
        _, lb = D.station_label(L, sid, th, box)
        if not lb:
            continue
        c0 = math.floor((lb[0] - pad - L.ox) / L.cell)
        c1 = math.ceil((lb[2] + pad - L.ox) / L.cell)
        r0 = math.floor((lb[1] - pad - L.oy) / L.cell)
        r1 = math.ceil((lb[3] + pad - L.oy) / L.cell)
        for c in range(c0, c1 + 1):
            for r in range(r0, r1 + 1):
                x, y = L.px((c, r))
                if lb[0] - pad <= x <= lb[2] + pad and lb[1] - pad <= y <= lb[3] + pad:
                    cells.add((c, r))
    return cells


def layout(cell=CELL, ox=OX, oy=OY):
    return G.Layout(cell, ox, oy, keepout_fn=label_keepout)


def oklch_mix(c1, c2, t):
    """Mix two sRGB hex colors in OKLab (the token method in Master Brief section 10)."""
    def to_lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    def to_srgb(c):
        c = max(0.0, min(1.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

    def lab(hexs):
        r, g, b = (to_lin(int(hexs[i:i + 2], 16)) for i in (1, 3, 5))
        l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
        m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
        s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
        l, m, s = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
        return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)

    a, b = lab(c1), lab(c2)
    L_, A_, B_ = (a[i] + (b[i] - a[i]) * t for i in range(3))
    l = (L_ + 0.3963377774 * A_ + 0.2158037573 * B_) ** 3
    m = (L_ - 0.1055613458 * A_ - 0.0638541728 * B_) ** 3
    s = (L_ - 0.0894841775 * A_ - 1.2914855480 * B_) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return "#" + "".join(f"{round(to_srgb(x) * 255):02X}" for x in (r, g, bb))


FIELD_ON_PRUSSIAN = oklch_mix(D.PRUSSIAN, D.NEWS, 0.085)
FIELD_ON_NEWS = oklch_mix(D.NEWS, D.WHITE, 0.45)
FIELD_ON_WHITE = oklch_mix(D.WHITE, D.NEWS, 0.32)


def core_rect():
    return (FRAME, FRAME, W - FRAME, H - FRAME)


FIELDS_TABLE = G.ASSETS / "20261028_Loop-Lines-District-Fields.csv"


def read_fields(path=FIELDS_TABLE):
    import csv
    out = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            verts = [tuple(float(v) for v in pair.split()) for pair in r["vertices"].split(";")]
            out.append({"district": r["district"], "part": r["part"], "cells": verts, "why": r["why"], "island": r.get("island") == "yes"})
    return out


def inside(pt, poly):
    x, y = pt
    c = False
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c


def district_fields(L, rect, gap=8.0, round_r=14.0):
    """Fields A to E, drawn from the field table on the same grid as the stations, clipped to the core, inset by
    half the gap and rounded by a same-colour stroke."""
    x0, y0, x1, y1 = rect
    parts = []
    for f in read_fields():
        pts = [L.px(c) for c in f["cells"]]
        pts = [(min(max(x, x0), x1), min(max(y, y0), y1)) for x, y in pts]
        parts.append(dict(f, px=pts))
    return {"parts": parts, "gap": gap, "round": round_r, "rect": rect}


def _inset(poly, d):
    """Inset a simple orthogonal or octilinear polygon by d (positive shrinks), keeping its edge directions."""
    sa = G.signed_area(poly)
    sgn = 1 if sa > 0 else -1
    return G.offset_poly(poly + [poly[0], poly[1]], sgn * d)[1:-1]


def field_svg(fields, color, bg):
    out = []
    r = fields["round"]
    for f in sorted(fields["parts"], key=lambda f: f["island"]):
        if f["island"]:
            moat = _inset(f["px"], -fields["gap"] / 2 + r)
            dm = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in moat) + " Z"
            out.append(f'<path d="{dm}" fill="{bg}" stroke="{bg}" stroke-width="{2 * r:.0f}" stroke-linejoin="round"/>')
        poly = _inset(f["px"], fields["gap"] / 2 + r)
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly) + " Z"
        out.append(f'<path class="field" data-district="{f["district"]}" data-part="{f["part"]}" d="{d}" fill="{color}" '
                   f'stroke="{color}" stroke-width="{2 * r:.0f}" stroke-linejoin="round"/>')
    return "".join(out)


def field_contacts(fields, rect):
    """Where each district's field meets each edge of the core: {(district, side): (lo, hi)} along that edge."""
    x0, y0, x1, y1 = rect
    res = {}
    for f in fields["parts"]:
        p = f["px"]
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            for side, test, coord in (("top", lambda q: abs(q[1] - y0) < 0.5, 0), ("bottom", lambda q: abs(q[1] - y1) < 0.5, 0),
                                      ("right", lambda q: abs(q[0] - x1) < 0.5, 1), ("left", lambda q: abs(q[0] - x0) < 0.5, 1)):
                if test(a) and test(b):
                    lo, hi = sorted((a[coord], b[coord]))
                    if hi - lo >= 1:
                        k = (f["district"], side)
                        if k not in res or hi - lo > res[k][1] - res[k][0]:
                            res[k] = (lo, hi)
    return res


def frame_counts():
    """Connections between each frame group (outside drivers, economy, technology) and each core district."""
    N = M["nodes"]

    def grp(k):
        n = N[k]
        if n["layer"] == "economy":
            return "EC"
        if n["layer"] == "technology":
            return "TC"
        return n["area"]

    c = {}
    for k, l in M["links"].items():
        a, b = grp(l["from"]), grp(l["to"])
        for f, d in ((a, b), (b, a)):
            if f in ("EC", "TC", "X") and d in "ABCDE":
                c.setdefault(f, {}).setdefault(d, []).append(k)
    return c


def legend_line(x, y, grade, w=46, ink=D.NEWS, weight=4.0):
    dash, code = D.dash_for(grade, weight)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x:.1f} {y:.1f} L{x + w:.1f} {y:.1f}" stroke="{ink}" stroke-width="{weight}" fill="none"{da} data-texture="{code}" data-legend="{grade}"/>'


def poster(L=None, theme_name="prussian", lit_loop=None, reform=None, view="c-poster", label=None, band=False):
    L = L or layout()
    th = D.Theme(theme_name)
    rect = core_rect()
    body = []
    field_fill = {"prussian": FIELD_ON_PRUSSIAN, "newsprint": FIELD_ON_NEWS, "white": FIELD_ON_WHITE}[theme_name]
    fields = district_fields(L, rect)
    body.append(field_svg(fields, field_fill, th.bg))
    ink_text = th.label
    soft = D.NEWS if theme_name == "prussian" else D.DEEP
    # district names on the map
    for dct, (cx, cy) in DISTRICT_NAME_AT.items():
        x, y = L.px((cx, cy))
        letter_w = D.text_w(dct, 40, 800, True)
        name = DISTRICT_TITLE[dct]
        body.append(T(x, y, dct, 40, 800, soft, "start", "d", extra=f' data-district-name="{dct}"'))
        if DISTRICT_WRAP[dct]:
            l1, l2 = D.wrap2(name, 19, 800)
            body.append(T(x + letter_w + 8, y - 22, l1, 19, 800, soft, "start", "d"))
            body.append(T(x + letter_w + 8, y - 1, l2, 19, 800, soft, "start", "d"))
        else:
            body.append(T(x + letter_w + 8, y - 3, name, 19, 800, soft, "start", "d"))
    net, boxes = D.network(L, th, lit_loop=lit_loop, reform=reform)
    body.append(net)
    body.append(frame(L, th, fields, rect, theme_name))
    body.append(title_block(th, theme_name, lit_loop, reform))
    body.append(legend(th, theme_name, L))
    body.append(sketched_box(th, theme_name))
    lab = label or "Loop Lines poster: the 20 numbered loops of Atlas V7 drawn as closed lines through 25 shared variables"
    extra = f' data-reform="{reform}"' if reform else ""
    extra += f' data-lit="{lit_loop}"' if lit_loop else ""
    extra += f' data-cell="{L.cell}" data-ox="{L.ox}" data-oy="{L.oy}"'
    svg = D.svg_doc(W, H, "".join(body), lab, view, th.bg, extra=extra)
    return svg, L, boxes, fields


def frame(L, th, fields, rect, theme_name):
    """Outside drivers on top, technology on the right, the economy along the bottom. Each draws an entry tick and
    a count where its connections reach a district's field; a district its band does not touch is named in the
    band's note."""
    x0, y0, x1, y1 = rect
    ink = D.NEWS if theme_name == "prussian" else D.CHARCOAL
    sub = D.NEWS if theme_name == "prussian" else D.DEEP
    counts = frame_counts()
    contacts = field_contacts(fields, rect)
    out = [f'<path d="M{x0} {y0} L{x1} {y0} L{x1} {y1} L{x0} {y1}" fill="none" stroke="{ink}" stroke-width="1"/>']
    bands = [("X", "Outside drivers", "top"), ("TC", "Technology layer", "right"), ("EC", "Economy layer", "bottom")]
    for gid, name, side in bands:
        per = counts[gid]
        total = sum(len(v) for v in per.values())
        nvars = len([k for k, n in M["nodes"].items() if (n["area"] == "X" if gid == "X" else n["layer"] == ("economy" if gid == "EC" else "technology"))])
        placed, unplaced = [], []
        for dct in "ABCDE":
            if dct not in per:
                continue
            seg = contacts.get((dct, side))
            if not seg or seg[1] - seg[0] < 60:
                unplaced.append(dct)
                continue
            placed.append((dct, (seg[0] + seg[1]) / 2))
        for dct, mid in placed:
            n = len(per[dct])
            ids = " ".join(sorted(per[dct]))
            head = f'<g class="entry" data-frame="{gid}" data-district="{dct}" data-count="{n}" data-links="{ids}">'
            if side == "top":
                out.append(head + f'<line x1="{mid:.1f}" y1="{y0 - 12}" x2="{mid:.1f}" y2="{y0 + 12}" stroke="{ink}" stroke-width="2.5"/>'
                           + T(mid + 7, y0 - 15, f"{n} to {dct}", 13, 700, ink, "start") + "</g>")
            elif side == "bottom":
                out.append(head + f'<line x1="{mid:.1f}" y1="{y1 - 12}" x2="{mid:.1f}" y2="{y1 + 12}" stroke="{ink}" stroke-width="2.5"/>'
                           + T(mid + 7, y1 + 28, f"{n} to {dct}", 13, 700, ink, "start") + "</g>")
            else:
                cx = x1 + 22
                out.append(head + f'<line x1="{x1 - 12}" y1="{mid:.1f}" x2="{x1 + 12}" y2="{mid:.1f}" stroke="{ink}" stroke-width="2.5"/>'
                           + f'<text x="{cx:.1f}" y="{mid + 9:.1f}" class="t b" font-size="13" fill="{ink}" transform="rotate(90 {cx:.1f} {mid + 9:.1f})">{n} to {dct}</text></g>')
        rest = ""
        if unplaced:
            parts = [f"{len(per[d])} to {d}" for d in unplaced]
            rest = " Away from a tick: " + (", ".join(parts[:-1]) + " and " + parts[-1] if len(parts) > 1 else parts[0]) + "."
        note = f"{nvars} variables. {total} connections reach the core.{rest}"
        label_attr = f' data-frame-note="{gid}" data-total="{total}" data-unplaced="{" ".join(unplaced)}"'
        line1, line2 = f"{nvars} variables", f"{total} connections reach the core." + rest
        nm_w = D.text_w(name.upper(), 13, 700) + 1.2 * len(name)
        need = max(nm_w + 16 + D.text_w(line1, 13, 400), D.text_w(line2, 13, 400)) + 8
        if side in ("top", "bottom"):
            ticks = sorted(m for _, m in placed)
            spans = [(x0, ticks[0] - 8)] if ticks else [(x0, x1)]
            for i, t in enumerate(ticks):
                spans.append((t + 70, (ticks[i + 1] - 8) if i + 1 < len(ticks) else x1))
            fit = [sp for sp in spans if sp[1] - sp[0] >= need]
            sp = fit[0] if fit else max(spans, key=lambda sp: sp[1] - sp[0])
            y_a, y_b = (19, 36) if side == "top" else (H - 26, H - 9)
            xs = sp[0] + 4
            out.append(T(xs, y_a, name.upper(), 13, 700, ink, "start", extra=' letter-spacing="1.2"'))
            out.append(T(xs + nm_w + 16, y_a, line1, 13, 400, sub, "start"))
            out.append(T(xs, y_b, line2, 13, 400, sub, "start", extra=label_attr))
        else:
            ticks = sorted(m for _, m in placed)
            ys = ticks[0] + 70 if ticks else y0 + 8
            for i, (txt, cls, attr, col) in enumerate(((name.upper() + "   " + line1, "t b", ' letter-spacing="1"', ink), (line2, "t", label_attr, sub))):
                cx = x1 + 12 + i * 17
                out.append(f'<text x="{cx}" y="{ys:.1f}" class="{cls}" font-size="13" fill="{col}"{attr} transform="rotate(90 {cx} {ys:.1f})">{esc(txt)}</text>')
    return '<g class="frame">' + "".join(out) + "</g>"


def title_block(th, theme_name, lit_loop, reform):
    ink = th.label
    sub = D.NEWS if theme_name == "prussian" else D.DEEP
    x, y = 72, 108
    out = [T(x, y, "Twenty loop lines", 44, 800, ink, "start", "d")]
    if reform:
        r = M["reforms"][reform]
        deck = f"Where Reform {reform} acts: {r['title'].lower()}."
    elif lit_loop:
        deck = f"Working map with Loop {lit_loop} lit."
    else:
        deck = "Each loop is a line that comes back to where it starts."
    out.append(T(x, y + 30, deck, 16, 400, sub, "start"))
    return '<g class="title">' + "".join(out) + "</g>"


def legend(th, theme_name, L, x=72, y=730):
    """How to read the map: line textures with V7's grade words (M1, M2), the sign tag, the two station shapes, the
    kind glyphs on the line bullets, and the spacing rule."""
    ink = th.label
    sub = D.NEWS if theme_name == "prussian" else D.DEEP
    line_ink = th.line if theme_name != "newsprint" else D.CHARCOAL
    c2 = 258
    out = [T(x, y, "HOW TO READ IT", 13, 700, ink, "start", extra=' letter-spacing="1.2"')]
    rows = [[("documented", "Documented or well supported"), ("plausible", "Plausible")],
            [("plausible_contested", "Contested"), ("hypothesis", "Hypothesis")]]
    yy = y + 24
    for row in rows:
        for i, (g, word) in enumerate(row):
            cx = x + i * c2
            out.append(legend_line(cx, yy - 4, g, 40, line_ink))
            out.append(T(cx + 50, yy + 1, word, 13, 400, sub, "start"))
        yy += 21
    out.append(D.sign_tag((x + 14, yy - 4), (1, 0), "+", th, 4))
    out.append(T(x + 42, yy + 1, "Both move the same way", 13, 400, sub, "start"))
    out.append(D.sign_tag((x + c2 + 14, yy - 4), (1, 0), "-", th, 4))
    out.append(T(x + c2 + 42, yy + 1, "They move opposite ways", 13, 400, sub, "start"))
    yy += 19
    out.append(T(x, yy + 1, "Each tag points the way its step runs.", 13, 400, sub, "start"))
    yy += 23
    out.append(f'<circle cx="{x + 12}" cy="{yy - 4}" r="11" fill="{th.fill}" stroke="{th.ring}" stroke-width="2.5"/>')
    out.append(T(x + 32, yy + 1, "A variable on one loop", 13, 400, sub, "start"))
    out.append(f'<rect x="{x + c2}" y="{yy - 15}" width="38" height="22" rx="11" fill="{th.fill}" stroke="{th.ring}" stroke-width="2.5"/>')
    out.append(T(x + c2 + 46, yy + 1, "Shared by several loops", 13, 400, sub, "start"))
    yy += 23
    out.append(D.kind_glyph(x + 12, yy - 4, "R", 16, line_ink, 1.8))
    out.append(T(x + 32, yy + 1, "Loop that feeds itself", 13, 400, sub, "start"))
    out.append(D.kind_glyph(x + c2 + 12, yy - 4, "B", 16, line_ink, 1.8))
    out.append(T(x + c2 + 32, yy + 1, "Loop that pushes back", 13, 400, sub, "start"))
    yy += 21
    out.append(T(x, yy + 1, "Stations sit on an even grid. Distance and line length carry no meaning.", 13, 400, sub, "start", extra=' data-note="spacing"'))
    return '<g class="legend">' + "".join(out) + "</g>"


def sketched_box(th, theme_name, x=1012, y=62, w=362):
    """The note in the frame, and the three sketched loops listed in words (they have no stations to draw)."""
    ink = th.label
    sub = D.NEWS if theme_name == "prussian" else D.DEEP
    note = ("This map draws the 20 numbered loops: 25 variables and 46 connections. "
            "The register lists all 51 variables and 118 connections.")
    sk = ("Sketched loops, with no numbered chain and so no stations: "
          + "; ".join(f"{lid}, {LOOPS[lid]['title'][0].lower() + LOOPS[lid]['title'][1:]}" for lid in G.SKETCHED) + ".")
    lines_a = D.wrap_to(note, w - 28, 13, 400)
    lines_b = D.wrap_to(sk, w - 28, 13, 400)
    h = 30 + 17 * (len(lines_a) + len(lines_b)) + 14
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{sub}" stroke-width="1"/>']
    yy = y + 22
    for ln in lines_a:
        out.append(T(x + 14, yy, ln, 13, 400, ink, "start", extra=' data-note="register"'))
        yy += 17
    yy += 6
    for ln in lines_b:
        out.append(T(x + 14, yy, ln, 13, 400, sub, "start"))
        yy += 17
    return '<g class="sketched" data-sketched="' + " ".join(G.SKETCHED) + '">' + "".join(out) + "</g>"
