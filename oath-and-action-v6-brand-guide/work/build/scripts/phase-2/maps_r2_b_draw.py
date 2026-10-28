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
    stroke = 2
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
            "clear": round((k - 1) * r - 2 * disc - stroke, 2), "r_need": round(r_need, 2), "gap": 3, "arrow": (8, 4)}


def head_geo(size=240, k=K, disc=15, stroke=2.5):
    r = 70.0
    while True:
        e = G.extents(2, r, k, disc + stroke / 2)
        if e[3] - e[1] <= size - 2 and e[2] - e[0] <= size - 2:
            r += 0.25
            continue
        r -= 0.25
        break
    e = G.extents(2, r, k, disc + stroke / 2)
    cx = 1 - e[0] + ((size - 2) - (e[2] - e[0])) / 2
    cy = 1 - e[1] + ((size - 2) - (e[3] - e[1])) / 2
    return {"r": round(r, 2), "k": k, "disc": disc, "stroke": stroke, "w": size, "h": size, "cx": round(cx, 2), "cy": round(cy, 2),
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
    """The loop-kind mark at 24 px (proposal, pending Dustin's approval). Same construction as the miniature: start
    disc at twelve o'clock, clockwise; the spiral ends on the outer lap above its start, the ring closes on it."""
    s = size / 24
    sw = 2 * s
    if kind == "R":
        k = K
        r = 5.0 * s
        # center the spiral's box: extents of the curve with the start dot
        e = G.extents(1, r, k, 0)
        cx = size / 2 - (e[0] + e[2]) / 2
        cy = size / 2 - (e[1] + e[3]) / 2
        cx, cy = round(cx * 2) / 2, round(cy * 2) / 2
        t_end = G.TAU
        d = G.bezier_d(0, t_end, r, k, cx, cy, max_deg=6)
        x0, y0 = G.pt(cx, cy, r, 0)
        body = (f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round"/>'
                f'<circle cx="{x0:.2f}" cy="{y0:.2f}" r="{2.75 * s:.2f}" fill="{ink}"/>')
    else:
        r = 7.5 * s
        cx = cy = size / 2
        body = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ink}" stroke-width="{sw}"/>'
                f'<circle cx="{cx}" cy="{cy - r:.2f}" r="{2.75 * s:.2f}" fill="{ink}"/>')
    bg = f'<rect x="0" y="0" width="{size}" height="{size}" fill="{ground}"/>' if ground else ""
    lab = "Snowball loop mark" if kind == "R" else "Thermostat loop mark"
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


def place_block(placer, lines, anchor_pt, direction, gap=14, slide=True):
    """Try to put a label block outward of anchor_pt along direction (unit vector), sliding outward until clear.
    Returns (x0, y0, x1, y1, text_anchor) or None."""
    w, h, _ = block_size(lines)
    ux, uy = direction
    ax, ay = anchor_pt
    for extra in range(0, 260, 4) if slide else (0,):
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

def card_geo(k=K, r=150.0, disc=27, stroke=2.5):
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
    w = max(24, tw + 14 + (11 if doc else 0))
    out = [f'<rect x="{x:.2f}" y="{y - h / 2:.2f}" width="{w:.2f}" height="{h}" rx="{h / 2}" fill="{ground}" stroke="{ink}" stroke-width="1.5"/>']
    if doc:
        out.append(f'<rect x="{x + 8:.2f}" y="{y - 3.5:.2f}" width="7" height="7" fill="{ink}" data-record="1"/>')
        tx = x + 8 + 7 + 3.5 + tw / 2
    else:
        tx = x + w / 2
    out.append(T(tx, y + size * 0.36, g, size, 700, ink, "middle", extra=' data-sign-glyph="1"'))
    return f'<g class="pill" data-for="{esc(step["id"])}">' + "".join(out) + "</g>", w


def _station_lines(s, echo=False, rule_w=210, compact=False):
    if echo:
        return [(f'{s["label"]}, one turn later', 16, 600, "inter", INK)]
    lines = [(s["label"], 16, 600, "inter", INK)]
    if not compact and s.get("increase_means"):
        for ln in TX.wrap(higher_rule(s["increase_means"]), rule_w, 14, 400):
            lines.append((ln, 14, 400, "inter", DEEP))
    return lines


def _step_lines(step, loop, reform_id, red, name_w=230):
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


PILL_INDENT = 34


def card_figure(loop, model, reform_id=None, geo=None, w=900, h=None, view="b-card", compact=False, ground=WHITE):
    """The loop card's drawing at full size. Station names and their Higher rules sit horizontal outside the curve;
    step names sit outside each segment with the sign, grade word and delay ticks; red marks the targets of the one
    reform the card names (Rule 05.3). Labels are placed by measured size and tested against the curve and discs."""
    geo = dict(geo or card_geo())
    ring = loop["type"] == "B"
    k = 1 if ring else geo["k"]
    r, disc = geo["r"], geo["disc"]
    # frame: the spiral (or ring) box, plus room for labels on each side
    e = G.extents(4, r, geo["k"], disc)  # one frame for every loop of this kind at this scale
    side = (w - (e[2] - e[0])) / 2
    top_room = 64 if not compact else 40
    geo["cx"] = side - e[0]
    geo["cy"] = top_room - e[1]
    h = h or math.ceil(e[3] - e[1] + top_room + 72)
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    red_links = {s["id"] for s in loop["steps"] if s["id"] in red_targets}
    red_nodes = {s["code"] for s in loop["stations"] if s["code"] in red_targets}
    steps, mids = draw_steps(loop, geo, ground, red_links=red_links, ticks=not compact)
    stations, centers, echo = draw_stations(loop, geo, ground, id_size=20, red_nodes=red_nodes, reform_id=reform_id,
                                            id_display=True)
    poly = _curve_poly(loop, geo)
    discs = [(c, disc + 2) for _, _, c in centers] + ([(echo[2], disc + 2)] if echo else [])
    P = Placer([poly], discs, w, h, margin=10)
    labels = []
    failed = []
    # echo first (its spot is fixed above the outer lap), then stations, then steps
    order = []
    if echo:
        order.append(("echo", echo))
    order += [("station", c) for c in centers]
    for kind_, (s, t, c) in order:
        lines = _station_lines(s, echo=(kind_ == "echo"), compact=compact)
        out_dir = G.outward(t)
        cands = [out_dir]
        if kind_ == "station" and t == 0 and not ring:
            # the echo sits outward of the first station: try beside it, then inside the turn
            cands = [(-1, 0), (0, 1), (1, 0)]
        rect = None
        for dvec in cands:
            rect = place_block(P, lines, c, dvec, gap=disc + 10)
            if rect:
                break
        if rect is None:
            failed.append(s["label"])
            continue
        al = align_for(dvec)
        labels.append(render_block(rect, lines, al, f' data-for="{esc(s["code"] or s["label"])}" data-kind="{kind_}"'))
    for step, tm, c in mids:
        if step.get("conceptual"):
            continue
        red = step["id"] in red_links
        lines = _step_lines(step, loop, reform_id, red, name_w=200 if compact else 230)
        # reserve the pill's width on the first line
        lines_m = [(lines[0][0] + "   ", *lines[0][1:])] + lines[1:]
        dvec = G.outward(tm)
        rect = place_block(P, lines_m, c, dvec, gap=16)
        if rect is None:
            failed.append(step["id"])
            continue
        al = align_for(dvec)
        x0, y0, x1, y1 = rect
        _, _, base = block_size(lines_m)
        pill_w = TX.width(sign_glyph(step["polarity"]), 14, 700) + 14 + (11 if step["evidence"] == "documented" else 0)
        pill_w = max(24, pill_w)
        head_w = TX.width(lines[0][0], 13, 700)
        if al == "end":
            hx_end = x1
            px = x1 - head_w - 8 - pill_w
        elif al == "middle":
            tot = pill_w + 8 + head_w
            px = (x0 + x1) / 2 - tot / 2
            hx_end = px + tot
        else:
            px = x0
            hx_end = x0 + pill_w + 8 + head_w
        pill, _ = pill_svg(px, y0 + base[0] - 4.5, step, ground=ground)
        body = [pill, T(hx_end, y0 + base[0], lines[0][0], 13, 700, INK, "end")]
        for (text, size, weight, fam, color), b in zip(lines[1:], base[1:]):
            if al == "end":
                body.append(T(x1, y0 + b, text, size, weight, color, "end"))
            elif al == "middle":
                body.append(T((x0 + x1) / 2, y0 + b, text, size, weight, color, "middle"))
            else:
                body.append(T(x0, y0 + b, text, size, weight, color))
        labels.append(f'<g class="lbl steplabel" data-for="{esc(step["id"])}" data-kind="step">' + "".join(body) + "</g>")
    kind_word = "Snowball loop: it feeds itself" if not ring else "Thermostat loop: it pushes back"
    label = f'Loop {loop["id"]} drawn as a {"spiral" if not ring else "ring"}. {kind_word}. {loop["how_to_read"]}'
    extra = f' data-reform="{esc(reform_id)}"' if reform_id else ""
    extra += f' data-label-failures="{esc("|".join(failed))}"' if failed else ""
    svg = svg_doc(w, h, "".join(steps) + "".join(stations) + "".join(labels), label, view, root_attrs(loop, geo, extra), bg=ground)
    return svg, failed


def phone_figure(loop, model, reform_id=None, w=358):
    """The card drawing at 390 px: the same geometry at a smaller r, station names only, step IDs with their sign.
    Step names, grades and Higher rules move to the lists under the figure."""
    geo = card_geo(r=62.0, disc=20, stroke=2.5)
    geo["arrow"] = (9, 4.5)
    geo["gap"] = 4
    ring = loop["type"] == "B"
    k = 1 if ring else geo["k"]
    r, disc = geo["r"], geo["disc"]
    e = G.extents(4, r, geo["k"], disc)
    geo["cx"] = (w - (e[2] - e[0])) / 2 - e[0]
    geo["cy"] = 46 - e[1]
    h = math.ceil(e[3] - e[1] + 46 + 52)
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    red_links = {s["id"] for s in loop["steps"] if s["id"] in red_targets}
    red_nodes = {s["code"] for s in loop["stations"] if s["code"] in red_targets}
    steps, mids = draw_steps(loop, geo, WHITE, red_links=red_links, ticks=True)
    stations, centers, echo = draw_stations(loop, geo, WHITE, id_size=15, red_nodes=red_nodes, reform_id=reform_id, id_display=True)
    poly = _curve_poly(loop, geo)
    discs = [(c, disc + 2) for _, _, c in centers] + ([(echo[2], disc + 2)] if echo else [])
    P = Placer([poly], discs, w, h, margin=7)
    labels, failed = [], []
    order = ([("echo", echo)] if echo else []) + [("station", c) for c in centers]
    for kind_, (s, t, c) in order:
        txt = f'{s["label"]}, one turn later' if kind_ == "echo" else s["label"]
        cands = [G.outward(t)]
        if kind_ == "station" and t == 0 and not ring:
            cands = [(0, 1), (-1, 0)]
        rect = None
        for wrap_w in (300, 120, 96):
            lines = [(ln, 15, 600, "inter", INK) for ln in TX.wrap(txt, wrap_w, 15, 600)]
            for dvec in cands:
                rect = place_block(P, lines, c, dvec, gap=disc + 7)
                if rect:
                    break
            if rect:
                break
        if rect is None:
            failed.append(s["label"])
            continue
        labels.append(render_block(rect, lines, align_for(dvec), f' data-for="{esc(s["code"] or s["label"])}" data-kind="{kind_}"'))
    for step, tm, c in mids:
        if step.get("conceptual"):
            continue
        lines = [(step["id"] + "  ", 13, 700, "inter", INK)]
        dvec = G.outward(tm)
        rect = place_block(P, lines, c, dvec, gap=12)
        if rect is None:
            failed.append(step["id"])
            continue
        x0, y0, x1, y1 = rect
        _, _, base = block_size(lines)
        pill, pw = pill_svg(x0, y0 + base[0] - 4.5, step)
        labels.append(f'<g class="lbl steplabel" data-for="{esc(step["id"])}" data-kind="step">{pill}'
                      + T(x0 + pw + 6, y0 + base[0], step["id"], 13, 700, INK) + "</g>")
    label = f'Loop {loop["id"]} drawn as a {"spiral" if not ring else "ring"}. {loop["how_to_read"]}'
    extra = f' data-reform="{esc(reform_id)}"' if reform_id else ""
    extra += f' data-label-failures="{esc("|".join(failed))}"' if failed else ""
    svg = svg_doc(w, h, "".join(steps) + "".join(stations) + "".join(labels), label, "b-card-phone", root_attrs(loop, geo, extra), bg=WHITE)
    return svg, failed
