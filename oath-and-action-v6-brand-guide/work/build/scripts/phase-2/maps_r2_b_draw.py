"""Drawings for Direction B, Snowball and Thermostat: miniature, card figure, phone figure, kind glyph, head emblem
and the placement mock for Direction C's poster.

Every drawing comes from the loop model in maps_model.py (Atlas V7 read once). Every data mark carries the data-*
attributes that verify_maps_data.py and maps_r2_b_verify.py read back. One SVG unit is one CSS pixel.

Rules drawn here:
- The shape comes from V7's loop type only: type R draws the spiral, type B the ring. Delay, direction, grade and
  valence never set a shape, a size or a color.
- One geometry per scale: every miniature uses the same center, r and k; every card figure the same r and k.
- Stroke weight is constant within a view. Pillar Red marks only the targets of the one reform a card names.
- M1 textures per segment (V7's code: plausible 9 4, contested 9 3 2 3, hypothesis 2 4, documented and well
  supported solid), the hollow line for sketched steps, M4 delay ticks on the card only.
"""
import html
import math

import maps_r2_b_geom as G
import maps_r2_b_text as TX

esc = html.escape

INK = "#121212"
NEWS = "#DCD9D2"
WHITE = "#FFFFFF"
STONE = "#5D636D"
DEEP = "#4E535B"
RED = "#E63946"
PRUSSIAN = "#1F2D5A"
MINUS = "−"

DASH = {"documented": None, "well-supported": None, "plausible": "9 4", "plausible_contested": "9 3 2 3",
        "contested": "9 3 2 3", "hypothesis": "2 4"}
TICKS = {"S": 1, "M": 2, "L": 3}
GRADE_WORD = {"documented": "Documented", "well-supported": "Well supported", "plausible": "Plausible",
              "plausible_contested": "Contested", "contested": "Contested", "hypothesis": "Hypothesis"}
GRADE_GLOSS = {"documented": "on the public record", "well-supported": "strong studies agree on the direction",
               "plausible": "a coherent mechanism with some evidence", "plausible_contested": "credible studies disagree",
               "contested": "credible studies disagree", "hypothesis": "proposed, not yet supported"}
DELAY_WORD = {"S": "under 2 years", "M": "2 to 10 years", "L": "over 10 years"}
FONT_UI = "Inter, 'Helvetica Neue', Arial, sans-serif"
FONT_DISPLAY = "'Inter Tight', Inter, 'Helvetica Neue', Arial, sans-serif"
STYLE = (f"<style>.bt{{font-family:{FONT_UI}}}.bd{{font-family:{FONT_DISPLAY};font-weight:800}}"
         ".b6{font-weight:600}.b7{font-weight:700}</style>")

# ------------------------------------------------------------------ geometry constants (one set per scale)

K = 1.8            # spiral growth per turn, the same for every reinforcing loop at every scale (see the notes, test 1)
K_BRIEF = 1.3      # the review's starting value, drawn only in the test panel


def mini_geo(k=K, disc=13, w=150):
    """Miniature frame: one center, one r, for every loop. r is the largest that keeps the echo disc clear of the
    first station (edge to edge at least 5 px) and the whole curve with discs inside the 150 px frame."""
    stroke = 2.5
    if k == 1:
        raise ValueError
    # clearance between first station and echo: (k - 1) r - 2 disc - stroke >= 5
    r_need = (2 * disc + stroke + 5) / (k - 1)
    # fit: union of extents for n = 2, 3, 4 inside w (width) and a height we derive
    def box(r):
        xs0, ys0, xs1, ys1 = [], [], [], []
        for n in (2, 3, 4):
            e = G.extents(n, r, k, disc + stroke / 2)
            xs0.append(e[0]); ys0.append(e[1]); xs1.append(e[2]); ys1.append(e[3])
        return min(xs0), min(ys0), max(xs1), max(ys1)
    r = 60.0
    while r > 10:
        b = box(r)
        if b[2] - b[0] <= w - 2:
            break
        r -= 0.25
    r_fit = r
    r = r_fit
    b = box(r)
    h = math.ceil(b[3] - b[1] + 2)
    cx = 1 - b[0] + ((w - 2) - (b[2] - b[0])) / 2
    cy = 1 - b[1]
    return {"r": round(r, 2), "k": k, "disc": disc, "stroke": stroke, "w": w, "h": h, "cx": round(cx, 2), "cy": round(cy, 2),
            "clear": round((k - 1) * r - 2 * disc - stroke, 2), "r_need": round(r_need, 2), "gap": 3, "arrow": (9, 4.5)}


def head_geo(size=240, k=K, disc=15, stroke=2.5):
    """Display size for the catalog head: the largest r whose spiral, with its discs, fits the square."""
    lo, hi = 5.0, size / 2
    for _ in range(50):
        r = (lo + hi) / 2
        e = G.extents(2, r, k, disc + stroke / 2)
        if e[3] - e[1] <= size - 4 and e[2] - e[0] <= size - 4:
            lo = r
        else:
            hi = r
    r = round(lo, 2)
    e = G.extents(2, r, k, disc + stroke / 2)
    cx = 2 - e[0] + ((size - 4) - (e[2] - e[0])) / 2
    cy = 2 - e[1] + ((size - 4) - (e[3] - e[1])) / 2
    return {"r": r, "k": k, "disc": disc, "stroke": stroke, "w": size, "h": size, "cx": round(cx, 2), "cy": round(cy, 2),
            "gap": 4, "arrow": (10, 5)}


# ------------------------------------------------------------------ primitives

def T(x, y, s, size=13, weight=400, fill=INK, anchor=None, display=False, italic=False, extra=""):
    cls = "bd" if display else "bt" + (" b7" if weight >= 700 else (" b6" if weight >= 600 else ""))
    a = f' text-anchor="{anchor}"' if anchor else ""
    it = ' font-style="italic"' if italic else ""
    return f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" font-size="{size}" fill="{fill}"{a}{it}{extra}>{esc(s)}</text>'


def svg_doc(w, h, body, label, view, attrs="", bg=None, desc=None):
    bgr = f'<rect x="0" y="0" width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    d = f"<desc>{esc(desc)}</desc>" if desc else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'role="img" aria-label="{esc(label)}" data-view="{esc(view)}"{attrs}><title>{esc(label)}</title>{d}{STYLE}{bgr}{body}</svg>')


def sign_glyph(p):
    return "+" if p == "+" else (MINUS if p == "-" else "")


def step_attrs(step, t0, t1):
    a = {"data-step": str(step["index"]), "data-sign": step.get("polarity") or "none",
         "data-t0": f"{math.degrees(t0):.4f}", "data-t1": f"{math.degrees(t1):.4f}"}
    if step.get("conceptual"):
        a["data-concept"] = "1"
        a["data-from-label"] = step["from_label"]
        a["data-to-label"] = step["to_label"]
    else:
        a.update({"data-link": step["id"], "data-from": step["from"], "data-to": step["to"], "data-grade": step["evidence"],
                  "data-delay": step["delay"], "data-type": step["type"]})
    return "".join(f' {k}="{esc(v)}"' for k, v in a.items())


def seg_range(geo, i, n, ring):
    """Angles of step i (0-based): from station i to station i + 1, the last step to the echo (spiral) or the start (ring)."""
    return G.TAU * i / n, G.TAU * (i + 1) / n


def trimmed(geo, t0, t1, r, k, rad0, rad1):
    """Angles after trimming rad0 px of arc from the start and rad1 px from the end."""
    a = G.t_at(t0, rad0, r, k, 1)
    b = G.t_at(t1, rad1, r, k, -1)
    return a, b


def arrowhead(cx, cy, r, k, t_tip, length, half, fill):
    tip = G.pt(cx, cy, G.rho(t_tip, r, k), t_tip)
    t_base = G.t_at(t_tip, length, r, k, -1)
    base = G.pt(cx, cy, G.rho(t_base, r, k), t_base)
    ux, uy = tip[0] - base[0], tip[1] - base[1]
    L = math.hypot(ux, uy) or 1
    ux, uy = ux / L, uy / L
    px, py = -uy, ux
    pts = f"{tip[0]:.2f},{tip[1]:.2f} {base[0] + px * half:.2f},{base[1] + py * half:.2f} {base[0] - px * half:.2f},{base[1] - py * half:.2f}"
    return f'<polygon points="{pts}" fill="{fill}"/>'


def line_path(d, grade, conceptual, width, color, ground, red=False):
    if conceptual:
        return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width + 3}" data-texture="hollow"/>'
                f'<path d="{d}" fill="none" stroke="{ground}" stroke-width="{max(1.5, width - 0.5)}"/>')
    dash = DASH.get(grade)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    tex = dash or "solid"
    rd = ' data-red="1"' if red else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} data-texture="{tex}"{rd}/>'


def ticks_at(cx, cy, r, k, t_start, n, color, width=1.5, length=10, spacing=5, offset=8):
    out = []
    for i in range(n):
        t = G.t_at(t_start, offset + i * spacing, r, k, 1)
        p = G.pt(cx, cy, G.rho(t, r, k), t)
        ux, uy = G.tangent(t, r, k)
        px, py = -uy, ux
        out.append(f'<line x1="{p[0] + px * length / 2:.2f}" y1="{p[1] + py * length / 2:.2f}" '
                   f'x2="{p[0] - px * length / 2:.2f}" y2="{p[1] - py * length / 2:.2f}" stroke="{color}" stroke-width="{width}"/>')
    return f'<g class="ticks" data-ticks="{n}">' + "".join(out) + "</g>"


def draw_steps(loop, geo, ground, ink=INK, red_links=(), ticks=False, open_r=None):
    """Every step of a loop as its own segment: textured line, arrowhead at the arrival, ticks on cards."""
    n = loop["n"]
    ring = loop["type"] == "B"
    k = 1 if ring else geo["k"]
    r, cx, cy, disc = geo["r"], geo["cx"], geo["cy"], geo["disc"]
    st = loop["stations"]
    out, mids = [], []
    for i, step in enumerate(loop["steps"]):
        t0, t1 = seg_range(geo, i, n, ring)
        rad0 = (disc if st[i]["is_variable"] else (open_r or disc)) + geo["gap"] + geo["stroke"] / 2
        to_station = st[(i + 1) % n]
        rad1 = (disc if to_station["is_variable"] else (open_r or disc)) + geo["gap"] + geo["stroke"] / 2
        a, b = trimmed(geo, t0, t1, r, k, rad0, rad1)
        al, ah = geo["arrow"]
        b_line = G.t_at(b, al - 0.6, r, k, -1)
        red = bool(step.get("id") and step["id"] in red_links)
        color = RED if red else ink
        d = G.bezier_d(a, b_line, r, k, cx, cy)
        g = [f'<g class="step"{step_attrs(step, t0, t1)}>', line_path(d, step.get("evidence"), step.get("conceptual"), geo["stroke"], color, ground, red)]
        g.append(arrowhead(cx, cy, r, k, b, al, ah, color))
        if ticks and step.get("delay"):
            g.append(ticks_at(cx, cy, r, k, a, TICKS[step["delay"]], color))
        g.append("</g>")
        out.append("".join(g))
        tm = (t0 + t1) / 2
        mids.append((step, tm, G.pt(cx, cy, G.rho(tm, r, k), tm)))
    return out, mids


def draw_stations(loop, geo, ground, ink=INK, id_size=13, red_nodes=(), reform_id=None, open_r=None, id_display=False,
                  paper_ink=None):
    """Station discs with the ID, then the echo of the first station on the outer lap (spiral only)."""
    n = loop["n"]
    ring = loop["type"] == "B"
    k = 1 if ring else geo["k"]
    r, cx, cy, disc = geo["r"], geo["cx"], geo["cy"], geo["disc"]
    paper = paper_ink or ground
    out, centers = [], []
    for i, s in enumerate(loop["stations"]):
        t = G.TAU * i / n
        x, y = G.pt(cx, cy, G.rho(t, r, k), t)
        centers.append((s, t, (x, y)))
        conceptual = loop["conceptual"]
        if s["is_variable"]:
            red = s["code"] in red_nodes
            tag = f' data-target="{esc(reform_id)}" data-red="1"' if red else ""
            g = [f'<g class="var" data-node="{esc(s["code"])}" data-label="{esc(s["label"])}" data-t="{math.degrees(t):.4f}"{tag}>']
            if conceptual:
                g.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{disc}" fill="{ground}" stroke="{ink}" stroke-width="{geo["stroke"]}"/>')
                g.append(T(x, y + id_size * 0.36, s["code"], id_size, 700 if not id_display else 800, ink, "middle", display=id_display))
            else:
                fill = RED if red else ink
                g.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{disc}" fill="{fill}"/>')
                g.append(T(x, y + id_size * 0.36, s["code"], id_size, 700 if not id_display else 800, WHITE if red else paper, "middle", display=id_display))
            g.append("</g>")
            out.append("".join(g))
        else:
            orr = open_r or disc
            out.append(f'<g class="sketch" data-concept-label="{esc(s["label"])}" data-t="{math.degrees(t):.4f}">'
                       f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{orr}" fill="{ground}" stroke="{ink}" stroke-width="{geo["stroke"]}"/></g>')
    echo = None
    if not ring:
        s = loop["stations"][0]
        x, y = G.pt(cx, cy, G.rho(G.TAU, r, k), G.TAU)
        echo = (s, G.TAU, (x, y))
        if s["is_variable"]:
            red = s["code"] in red_nodes
            col = RED if red else ink
            tag = f' data-target="{esc(reform_id)}" data-red="1"' if red else ""
            out.append(f'<g class="echo" data-node="{esc(s["code"])}" data-t="360.0000"{tag}>'
                       f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{disc - geo["stroke"] / 2}" fill="{ground}" stroke="{col}" stroke-width="{geo["stroke"]}"/>'
                       + T(x, y + id_size * 0.36, s["code"], id_size, 700 if not id_display else 800, col, "middle", display=id_display) + "</g>")
        else:
            orr = open_r or disc
            out.append(f'<g class="echo sketch" data-concept-label="{esc(s["label"])}" data-t="360.0000">'
                       f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{orr}" fill="{ground}" stroke="{ink}" stroke-width="{geo["stroke"]}"/></g>')
    return out, centers, echo


def root_attrs(loop, geo, extra=""):
    shape = "ring" if loop["type"] == "B" else "spiral"
    k = 1 if shape == "ring" else geo["k"]
    return (f' data-loop="{esc(loop["id"])}" data-direction="snowball-thermostat" data-shape="{shape}" data-cx="{geo["cx"]}" '
            f'data-cy="{geo["cy"]}" data-r="{geo["r"]}" data-k="{k}" data-n="{loop["n"]}"{extra}')


# ------------------------------------------------------------------ miniature

def miniature(loop, geo=None, ground=WHITE, view="b-mini", label_extra=""):
    """Catalog miniature: the shape, its stations by ID, the echo, each segment in its M1 texture. No signs, ticks or
    pointers, and no red: the catalog names no single reform (Rule 05.3)."""
    geo = geo or mini_geo()
    steps, _ = draw_steps(loop, geo, ground, open_r=7)
    stations, _, _ = draw_stations(loop, geo, ground, open_r=7)
    kind = "Snowball loop, feeds itself" if loop["type"] == "R" else "Thermostat loop, pushes back"
    names = ", ".join(s["label"] for s in loop["stations"])
    label = f'Loop {loop["id"]}, {kind}. Stations clockwise from twelve o\'clock: {names}.{label_extra}'
    return svg_doc(geo["w"], geo["h"], "".join(steps) + "".join(stations), label, view, root_attrs(loop, geo))


# ------------------------------------------------------------------ head emblem and kind glyph

def emblem(kind, geo, ink=NEWS, ground=INK, label=None):
    """The kind at display size: the spiral or the ring with a start disc (and the echo), no data. Used on the
    catalog head beside the counts."""
    r, k, cx, cy, disc = geo["r"], (geo["k"] if kind == "R" else 1), geo["cx"], geo["cy"], geo["disc"]
    sw = geo["stroke"]
    rad = disc + geo["gap"] + sw / 2
    a = G.t_at(0, rad, r, k, 1)
    b = G.t_at(G.TAU, rad, r, k, -1)
    al, ah = geo["arrow"]
    d = G.bezier_d(a, G.t_at(b, al - 0.6, r, k, -1), r, k, cx, cy)
    body = [f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{sw}"/>', arrowhead(cx, cy, r, k, b, al, ah, ink)]
    x0, y0 = G.pt(cx, cy, r, 0)
    body.append(f'<circle cx="{x0:.2f}" cy="{y0:.2f}" r="{disc}" fill="{ink}"/>')
    if kind == "R":
        x1, y1 = G.pt(cx, cy, k * r, G.TAU)
        body.append(f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="{disc - sw / 2}" fill="{ground}" stroke="{ink}" stroke-width="{sw}"/>')
    lab = label or ("Snowball: one turn of a spiral that returns to its start one lap further out" if kind == "R"
                    else "Thermostat: a ring that closes on its start")
    return svg_doc(geo["w"], geo["h"], "".join(body), lab, "b-emblem", f' data-kind="{kind}" data-r="{r}" data-k="{k}"')


def glyph24(kind, ink=INK, ground=None, size=24):
    """The loop-kind mark (proposal, pending Dustin's approval), drawn on a 24 px grid and scaled for other sizes.
    Same construction as the miniature: a start dot at twelve o'clock and a clockwise line with the shared k. The
    spiral (r 6) ends on the outer lap above its start, with a 1.5 px opening between the dot and the outer lap at
    24 px; the ring (r 7.5) closes on its dot, so the pair carries equal optical weight. Marks are not loop drawings,
    so their radii state no relation between kinds. A snapped variant (r 5, extremes on whole pixels) measured no
    crisper and less distinct from the ring, so this drawing stays (see the notes, kind mark)."""
    s = size / 24
    sw = 2 * s
    dot = 2.25 * s
    if kind == "R":
        k = K
        r = 6.0 * s
        e = G.extents(1, r, k, 0)
        cx = size / 2 - (e[0] + e[2]) / 2
        cy = size / 2 - (e[1] + e[3]) / 2
        cx, cy = round(cx * 4) / 4, round(cy * 4) / 4
        d = G.bezier_d(0, G.TAU, r, k, cx, cy, max_deg=6)
        x0, y0 = G.pt(cx, cy, r, 0)
        body = (f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{sw:.2f}" stroke-linecap="round"/>'
                f'<circle cx="{x0:.2f}" cy="{y0:.2f}" r="{dot:.2f}" fill="{ink}"/>')
    else:
        r = 7.5 * s
        cx = cy = size / 2
        body = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ink}" stroke-width="{sw:.2f}"/>'
                f'<circle cx="{cx}" cy="{cy - r:.2f}" r="{dot + 0.5 * s:.2f}" fill="{ink}"/>')
    bg = f'<rect x="0" y="0" width="{size}" height="{size}" fill="{ground}"/>' if ground else ""
    lab = "Snowball loop mark: feeds itself" if kind == "R" else "Thermostat loop mark: pushes back"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" role="img" '
            f'aria-label="{lab}" data-view="b-glyph" data-kind="{kind}"><title>{lab}</title>{bg}{body}</svg>')


# ------------------------------------------------------------------ label placement for card figures

class Placer:
    """Places horizontal label blocks clear of the curve, the discs and each other, from candidate anchors in order."""

    def __init__(self, polys, discs, w, h, margin=8):
        self.polys, self.discs, self.w, self.h, self.margin = polys, discs, w, h, margin
        self.rects = []

    def ok(self, rect, margin=None):
        m = self.margin if margin is None else margin
        x0, y0, x1, y1 = rect
        if x0 < 4 or y0 < 4 or x1 > self.w - 4 or y1 > self.h - 4:
            return False
        for poly in self.polys:
            if not G.rect_clear_of_poly(rect, poly, m):
                return False
        for c, rad in self.discs:
            if not G.rect_clear_of_disc(rect, c, rad, m):
                return False
        for r in self.rects:
            if G.rects_overlap(rect, r, 10):
                return False
        return True

    def take(self, rect):
        self.rects.append(rect)


def block_size(lines):
    """lines: [(text, size, weight, family, color)] -> width, height, baselines."""
    w = 0
    y = 0
    base = []
    for text, size, weight, fam, _ in lines:
        lh = round(size * 1.32)
        y += lh
        base.append(y - round(size * 0.28))
        w = max(w, TX.width(text, size, weight, fam))
    return w, y, base


def place_block(placer, lines, anchor_pt, direction, gap=14, slide=True, max_slide=260):
    """Try to put a label block outward of anchor_pt along direction (unit vector), sliding outward until clear.
    Returns (x0, y0, x1, y1, text_anchor) or None."""
    w, h, _ = block_size(lines)
    ux, uy = direction
    ax, ay = anchor_pt
    for extra in range(0, max_slide, 4) if slide else (0,):
        dist = gap + extra
        px, py = ax + ux * dist, ay + uy * dist
        # choose the block's attachment by direction: left of, right of, above or below the point
        if ux > 0.38:
            x0 = px
        elif ux < -0.38:
            x0 = px - w
        else:
            x0 = px - w / 2
        if uy > 0.38:
            y0 = py
        elif uy < -0.38:
            y0 = py - h
        else:
            y0 = py - h / 2
        rect = (x0, y0, x0 + w, y0 + h)
        if placer.ok(rect):
            placer.take(rect)
            return rect
    return None


def render_block(rect, lines, align="start", extra_attrs="", first_offset=0):
    x0, y0, x1, y1 = rect
    w, h, base = block_size(lines)
    out = []
    for (text, size, weight, fam, color), b in zip(lines, base):
        if align == "end":
            x, anc = x1, "end"
        elif align == "middle":
            x, anc = (x0 + x1) / 2, "middle"
        else:
            x, anc = x0, None
        out.append(T(x, y0 + b, text, size, weight, color, anc, display=(fam == "tight"), italic=(fam == "lora-italic")))
    return f'<g class="lbl"{extra_attrs}>' + "".join(out) + "</g>"


def higher_rule(increase_means):
    s = increase_means.strip()
    pre = "A higher value means "
    if s.startswith(pre):
        s = s[len(pre):]
    return "Higher: " + s


def align_for(direction):
    ux, _ = direction
    return "start" if ux > 0.38 else ("end" if ux < -0.38 else "middle")


# ------------------------------------------------------------------ card figure (desktop) and phone figure

def card_geo(k=K, r=155.0, disc=27, stroke=2.5):
    return {"r": r, "k": k, "disc": disc, "stroke": stroke, "gap": 5, "arrow": (11, 5.5)}


def _curve_poly(loop, geo, step_deg=1.0):
    k = 1 if loop["type"] == "B" else geo["k"]
    return G.sample(0, G.TAU, geo["r"], k, geo["cx"], geo["cy"], step_deg)


def pill_svg(x, y, step, size=14, ground=WHITE, ink=INK):
    """The step's sign in a pill, with the record square when the grade is documented (M1). x, y is the left edge
    and the vertical center. Returns svg and width."""
    g = sign_glyph(step["polarity"])
    doc = step.get("evidence") == "documented"
    tw = TX.width(g, size, 700)
    h = 22
    w = pill_w(step, size)
    out = [f'<rect x="{x:.2f}" y="{y - h / 2:.2f}" width="{w:.2f}" height="{h}" rx="{h / 2}" fill="{ground}" stroke="{ink}" stroke-width="1.5"/>']
    if doc:
        out.append(f'<rect x="{x + 8:.2f}" y="{y - 3.5:.2f}" width="7" height="7" fill="{ink}" data-record="1"/>')
        tx = x + 8 + 7 + 3.5 + tw / 2
    else:
        tx = x + w / 2
    out.append(T(tx, y + size * 0.36, g, size, 700, ink, "middle", extra=' data-sign-glyph="1"'))
    return f'<g class="pill" data-for="{esc(step["id"])}">' + "".join(out) + "</g>", w


def pill_w(step, size=14):
    tw = TX.width(sign_glyph(step["polarity"]), size, 700)
    return max(24, tw + 14 + (11 if step.get("evidence") == "documented" else 0))


def _station_lines(s, echo=False, name_w=200, rule_w=200, compact=False, size=16):
    if echo:
        return [(ln, size, 600, "inter", INK) for ln in TX.wrap(f'{s["label"]}, one turn later', 330, size, 600)]
    lines = [(ln, size, 600, "inter", INK) for ln in TX.wrap(s["label"], name_w, size, 600)]
    if not compact and s.get("increase_means"):
        for ln in TX.wrap(higher_rule(s["increase_means"]), rule_w, 14, 400):
            lines.append((ln, 14, 400, "inter", DEEP))
    return lines


def _step_lines(step, loop, reform_id, red, name_w=220):
    head = f'{step["id"]} · ' + ("same direction" if step["polarity"] == "+" else "opposite direction")
    lines = [(head, 13, 700, "inter", INK)]
    for ln in TX.wrap(step["name"], name_w, 15, 600):
        lines.append((ln, 15, 600, "inter", INK))
    lines.append((f'{GRADE_WORD[step["evidence"]]} · {DELAY_WORD[step["delay"]]}', 13, 400, "inter", DEEP))
    if step["id"] in loop["weakest"]:
        lines.append(("Least certain step in this loop", 13, 700, "inter", INK))
    if red:
        lines.append((f"{reform_id} acts on this step", 13, 700, "inter", INK))
    return lines


def _rot(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def _station_cands(t, first_of_spiral):
    out = G.outward(t)
    if first_of_spiral:
        # the echo sits outward of the first station, so its label goes inside the turn, under the disc
        return [(0, 1), (-1, 0.0001), (1, 0.0001)]
    return [out, _rot(out, 30), _rot(out, -30), _rot(out, 60), _rot(out, -60)]


def _place_step_label(P, lines, step, c, tm, ground):
    """Step label with the sign pill on its first line. Returns svg or None."""
    pw = pill_w(step)
    head_w = TX.width(lines[0][0], 13, 700)
    # measure as one block, with the pill's width added to the first line
    first = (lines[0][0], lines[0][1], lines[0][2], lines[0][3], lines[0][4])
    w_first = pw + 8 + head_w
    w_rest = max((TX.width(t, sz, wt, fm) for t, sz, wt, fm, _ in lines[1:]), default=0)
    _, h, base = block_size(lines)
    bw = max(w_first, w_rest)
    out = G.outward(tm)
    for dvec in (out, _rot(out, 25), _rot(out, -25), _rot(out, 50), _rot(out, -50)):
        ux, uy = dvec
        for extra in range(0, 240, 4):
            dist = 18 + extra
            px, py = c[0] + ux * dist, c[1] + uy * dist
            x0 = px if ux > 0.38 else (px - bw if ux < -0.38 else px - bw / 2)
            y0 = py if uy > 0.38 else (py - h if uy < -0.38 else py - h / 2)
            rect = (x0, y0 - 6, x0 + bw, y0 + h)
            if P.ok(rect):
                P.take(rect)
                al = align_for(dvec)
                x1 = x0 + bw
                if al == "end":
                    px0 = x1 - w_first
                elif al == "middle":
                    px0 = (x0 + x1) / 2 - w_first / 2
                else:
                    px0 = x0
                pill, _ = pill_svg(px0, y0 + base[0] - 4.5, step, ground=ground)
                body = [pill, T(px0 + pw + 8, y0 + base[0], lines[0][0], 13, 700, INK)]
                for (text, size, weight, fam, color), b in zip(lines[1:], base[1:]):
                    if al == "end":
                        body.append(T(x1, y0 + b, text, size, weight, color, "end"))
                    elif al == "middle":
                        body.append(T((x0 + x1) / 2, y0 + b, text, size, weight, color, "middle"))
                    else:
                        body.append(T(x0, y0 + b, text, size, weight, color))
                return f'<g class="lbl steplabel" data-for="{esc(step["id"])}" data-kind="step">' + "".join(body) + "</g>"
    return None


def _figure(loop, model, reform_id, geo, w, top_room, bottom_room, view, ground, compact, phone):
    ring = loop["type"] == "B"
    r, disc = geo["r"], geo["disc"]
    e = G.extents(4, r, geo["k"], disc)  # one frame for every loop at this scale, whatever its kind
    geo["cx"] = round((w - (e[2] - e[0])) / 2 - e[0], 2)
    geo["cy"] = round(top_room - e[1], 2)
    h = math.ceil(e[3] - e[1] + top_room + bottom_room)
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    red_links = {s["id"] for s in loop["steps"] if s["id"] in red_targets}
    red_nodes = {s["code"] for s in loop["stations"] if s["code"] in red_targets}
    steps, mids = draw_steps(loop, geo, ground, red_links=red_links, ticks=True, open_r=12 if not phone else 9)
    stations, centers, echo = draw_stations(loop, geo, ground, id_size=20 if not phone else 19, red_nodes=red_nodes,
                                            reform_id=reform_id, id_display=True, open_r=12 if not phone else 9)
    poly = _curve_poly(loop, geo)
    discs = [(c, disc + 2) for _, _, c in centers] + ([(echo[2], disc + 2)] if echo else [])
    P = Placer([poly], discs, w, h, margin=10 if not phone else 7)
    labels, failed = [], []
    order = ([("echo", echo)] if echo else []) + [("station", c) for c in centers]
    if phone:
        # on a phone the figure names only the echo; the strip under the figure names every station in order
        order = [("echo", echo)] if echo else []
    for kind_, (s, t, c) in order:
        cands = [G.outward(t)] if kind_ == "echo" else _station_cands(t, (t == 0 and not ring))
        rect = None
        if phone:
            lines = [(f'{s["code"] or "Start"} again, one turn later', 14, 600, "inter", INK)]
        else:
            lines = _station_lines(s, echo=(kind_ == "echo"), name_w=200, rule_w=200, compact=compact)
        for dvec in cands:
            rect = place_block(P, lines, c, dvec, gap=disc + (10 if not phone else 7), max_slide=44)
            if rect:
                break
        if rect is None:
            failed.append(s["label"])
            continue
        labels.append(render_block(rect, lines, align_for(dvec), f' data-for="{esc(s["code"] or s["label"])}" data-kind="{kind_}"'))
    for step, tm, c in mids:
        if step.get("conceptual"):
            continue
        red = step["id"] in red_links
        if phone:
            lines = [(step["id"], 13, 700, "inter", INK)]
        else:
            lines = _step_lines(step, loop, reform_id, red, name_w=200 if compact else 220)
        svg = _place_step_label(P, lines, step, c, tm, ground)
        if svg is None:
            failed.append(step["id"])
            continue
        labels.append(svg)
    kind_word = "Snowball loop: it feeds itself" if not ring else "Thermostat loop: it pushes back"
    label = f'Loop {loop["id"]} drawn as a {"spiral" if not ring else "ring"}. {kind_word}. {loop["how_to_read"]}'
    extra = f' data-reform="{esc(reform_id)}"' if reform_id else ""
    extra += f' data-label-failures="{esc("|".join(failed))}"' if failed else ""
    # crop the canvas to the drawing and its labels; r, k and every mark keep their size
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    for c, rad in discs:
        xs += [c[0] - rad, c[0] + rad]
        ys += [c[1] - rad, c[1] + rad]
    for r_ in P.rects:
        xs += [r_[0], r_[2]]
        ys += [r_[1], r_[3]]
    pad = 16 if not phone else 10
    x0, y0, x1, y1 = min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
    if phone:
        x0, x1 = 0, w
    vw, vh = math.ceil(x1 - x0), math.ceil(y1 - y0)
    body = "".join(steps) + "".join(stations) + "".join(labels)
    bgr = f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{vw}" height="{vh}" fill="{ground}"/>'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{vw}" height="{vh}" viewBox="{x0:.0f} {y0:.0f} {vw} {vh}" '
           f'role="img" aria-label="{esc(label)}" data-view="{esc(view)}"{root_attrs(loop, geo, extra)}><title>{esc(label)}</title>'
           f'{STYLE}{bgr}{body}</svg>')
    return svg, failed


def card_figure(loop, model, reform_id=None, geo=None, w=960, view="b-card", compact=False, ground=WHITE):
    """The loop card's drawing at full size: station names and their Higher rules horizontal outside the curve
    (the first station's inside the turn, since its echo sits outward); step names outside each segment with the
    sign, grade word and delay ticks; red at the targets of the one reform the card names (Rule 05.3)."""
    return _figure(loop, model, reform_id, dict(geo or card_geo()), w, 64, 150, view, ground, compact, False)


def phone_geo():
    g = card_geo(r=56.0, disc=19, stroke=2.5)
    g["arrow"] = (9, 4.5)
    g["gap"] = 4
    return g


def phone_figure(loop, model, reform_id=None, w=358, view="b-card-phone"):
    """The card drawing at 390 px: the same k at a smaller r, station names, step IDs with their sign pill. Step
    names, grades and Higher rules move to the list under the figure."""
    return _figure(loop, model, reform_id, phone_geo(), w, 44, 64, view, WHITE, True, True)
