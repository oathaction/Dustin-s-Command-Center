"""Shared drawing primitives for the Systems Map Directions Board.

One SVG unit is one CSS pixel. Marks keep their absolute size at every scale (line weight, dash, ticks, text),
and only the geometry scales, as in cartographic generalization: a miniature shrinks the card's geometry and keeps
the marks legible. The marks are the Gate 1 vocabulary (M1 to M4): V7's line code with the record square and the
hollow line, delay ticks, the open authority diamond, and red per Rule 05.3 with a Charcoal edge.

Every data mark carries data-* attributes that verify_maps_data.py reads back and checks against Atlas V7.
"""
import html
import math

esc = html.escape

INK = "#121212"        # Charcoal
NEWS = "#DCD9D2"       # Newsprint
WHITE = "#FFFFFF"
STONE = "#5D636D"      # data.context on Newsprint and White
DEEP = "#4E535B"       # derived deepStone: secondary text on Newsprint and White
RED = "#E63946"        # Pillar Red; Rule 05.3, one working red per view
PRUSSIAN = "#1F2D5A"
MINUS = "−"

DASH = {"documented": None, "well-supported": None, "plausible": "9 4", "plausible_contested": "9 3 2 3",
        "contested": "9 3 2 3", "hypothesis": "2 4"}
TICKS = {"S": 1, "M": 2, "L": 3}
FONT_UI = "Inter, 'Helvetica Neue', Arial, sans-serif"
FONT_DISPLAY = "'Inter Tight', Inter, 'Helvetica Neue', Arial, sans-serif"

STYLE = (f"<style>.mt{{font-family:{FONT_UI}}}.md{{font-family:{FONT_DISPLAY};font-weight:800;letter-spacing:-0.01em}}"
         ".mb{font-weight:700}.ms{font-weight:600}.mi{font-style:italic}</style>")


def sign_glyph(p):
    return "+" if p == "+" else (MINUS if p == "-" else "")


def text_w(s, size=13, weight=400, display=False):
    """Approximate advance width of Inter, for layout only. Measured widths are checked in the browser."""
    per = 0.56 if weight < 600 else 0.6
    if display:
        per = 0.55
    narrow = sum(1 for ch in s if ch in "il.,:;'|() ")
    wide = sum(1 for ch in s if ch in "MWmw")
    return size * (per * (len(s) - narrow - wide) + 0.3 * narrow + 0.85 * wide)


def wrap(s, width, size=13, weight=400):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, size, weight) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def T(x, y, s, size=13, weight=400, fill=INK, anchor=None, display=False, italic=False, extra=""):
    cls = "md" if display else "mt"
    if weight >= 700 and not display:
        cls += " mb"
    elif weight >= 600 and not display:
        cls += " ms"
    if italic:
        cls += " mi"
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size}" fill="{fill}"{a}{extra}>{esc(s)}</text>'


def svg_doc(w, h, body, label, view, extra_attrs="", bg=None, desc=None):
    bgr = f'<rect x="0" y="0" width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    d = f"<desc>{esc(desc)}</desc>" if desc else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'role="img" aria-label="{esc(label)}" data-view="{esc(view)}"{extra_attrs}><title>{esc(label)}</title>{d}{STYLE}{bgr}{body}</svg>')


# ------------------------------------------------------------------ polyline geometry

def dist(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def plen(poly):
    return sum(dist(poly[i], poly[i + 1]) for i in range(len(poly) - 1))


def point_at(poly, s):
    """Point and unit tangent at arc length s along a polyline."""
    if s <= 0:
        a, b = poly[0], poly[1]
        d = dist(a, b) or 1
        return a, ((b[0] - a[0]) / d, (b[1] - a[1]) / d)
    acc = 0
    for i in range(len(poly) - 1):
        a, b = poly[i], poly[i + 1]
        d = dist(a, b)
        if acc + d >= s and d > 0:
            t = (s - acc) / d
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ((b[0] - a[0]) / d, (b[1] - a[1]) / d)
        acc += d
    a, b = poly[-2], poly[-1]
    d = dist(a, b) or 1
    return b, ((b[0] - a[0]) / d, (b[1] - a[1]) / d)


def trim(poly, s0, s1):
    """The part of a polyline between arc lengths s0 and (length - s1)."""
    total = plen(poly)
    e = total - s1
    if e <= s0:
        return [point_at(poly, s0)[0], point_at(poly, s0 + 0.01)[0]]
    out = [point_at(poly, s0)[0]]
    acc = 0
    for i in range(len(poly) - 1):
        a, b = poly[i], poly[i + 1]
        acc_b = acc + dist(a, b)
        if s0 < acc_b < e:
            out.append(b)
        acc = acc_b
    out.append(point_at(poly, e)[0])
    return out


def mid(poly):
    return point_at(poly, plen(poly) / 2)


def quad(p0, c, p1, n=48):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]) for t in (i / n for i in range(n + 1))]


def cubic(p0, c0, c1, p1, n=64):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * c0[0] + 3 * u * t * t * c1[0] + t ** 3 * p1[0],
                    u ** 3 * p0[1] + 3 * u * u * t * c0[1] + 3 * u * t * t * c1[1] + t ** 3 * p1[1]))
    return out


def arc_through(p0, p1, sagitta, n=64):
    """Circular arc from p0 to p1 bulging to the left of the direction p0 to p1 by sagitta (negative bulges right)."""
    c = dist(p0, p1)
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    ux, uy = (p1[0] - p0[0]) / c, (p1[1] - p0[1]) / c
    nx, ny = uy, -ux  # left normal in screen coordinates (y down) is (uy, -ux)
    if abs(sagitta) < 0.5:
        return [(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t) for t in (i / n for i in range(n + 1))]
    h = sagitta
    r = (c * c / 4 + h * h) / (2 * abs(h))
    # centre lies on the normal, on the side opposite the bulge
    sgn = 1 if h > 0 else -1
    cx, cy = mx - nx * sgn * (r - abs(h)), my - ny * sgn * (r - abs(h))
    a0 = math.atan2(p0[1] - cy, p0[0] - cx)
    a1 = math.atan2(p1[1] - cy, p1[0] - cx)
    # choose the sweep that passes through the apex
    apex = (mx + nx * h, my + ny * h)
    aa = math.atan2(apex[1] - cy, apex[0] - cx)

    def norm(a):
        while a < 0:
            a += 2 * math.pi
        while a >= 2 * math.pi:
            a -= 2 * math.pi
        return a
    d1 = norm(a1 - a0)
    da = norm(aa - a0)
    if da > d1:
        d1 = d1 - 2 * math.pi
    return [(cx + r * math.cos(a0 + d1 * t), cy + r * math.sin(a0 + d1 * t)) for t in (i / n for i in range(n + 1))]


def path_d(poly):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly)


# ------------------------------------------------------------------ end marks, ticks, labels

def arrow_at(poly, length=9, half=4.5, fill=INK, edge=None):
    p, (ux, uy) = point_at(poly, plen(poly))
    bx, by = p[0] - ux * length, p[1] - uy * length
    px, py = -uy, ux
    pts = f"{p[0]:.1f},{p[1]:.1f} {bx + px * half:.1f},{by + py * half:.1f} {bx - px * half:.1f},{by - py * half:.1f}"
    st = f' stroke="{edge}" stroke-width="1" stroke-linejoin="miter"' if edge else ""
    return f'<polygon points="{pts}" fill="{fill}"{st}/>'


def diamond_at(poly, length=12, half=4.5, bg=NEWS, ink=INK):
    p, (ux, uy) = point_at(poly, plen(poly))
    mx, my = p[0] - ux * length / 2, p[1] - uy * length / 2
    bx, by = p[0] - ux * length, p[1] - uy * length
    px, py = -uy, ux
    pts = (f"{p[0]:.1f},{p[1]:.1f} {mx + px * half:.1f},{my + py * half:.1f} {bx:.1f},{by:.1f} "
           f"{mx - px * half:.1f},{my - py * half:.1f}")
    return f'<polygon points="{pts}" fill="{bg}" stroke="{ink}" stroke-width="1.5" stroke-linejoin="miter"/>'


def ticks_on(poly, n, start=7, step=5, length=10, color=INK, width=1.5):
    out = []
    for i in range(n):
        p, (ux, uy) = point_at(poly, start + i * step)
        px, py = -uy, ux
        out.append(f'<line x1="{p[0] + px * length / 2:.1f}" y1="{p[1] + py * length / 2:.1f}" '
                   f'x2="{p[0] - px * length / 2:.1f}" y2="{p[1] - py * length / 2:.1f}" stroke="{color}" stroke-width="{width}"/>')
    return f'<g class="ticks" data-ticks="{n}">' + "".join(out) + "</g>"


def stroke(poly, grade, conceptual=False, width=2, color=INK, bg=NEWS, red=False):
    """The line itself, in V7's texture (M1). A red line carries a Charcoal edge (Rule 05.3, contrast on Newsprint)."""
    d = path_d(poly)
    if conceptual:
        return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="5" data-texture="hollow"/>'
                f'<path d="{d}" fill="none" stroke="{bg}" stroke-width="2"/>')
    dash = DASH.get(grade)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    tex = dash or "solid"
    if red:
        return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width + 3}"{da} data-texture="{tex}"/>'
                f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="{width + 0.5}"{da}/>')
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} data-texture="{tex}"/>'


def connection(poly, step, *, start_gap=0, end_gap=0, width=2, color=INK, bg=NEWS, red=False, ticks=True,
               head=True, kind=None):
    """A drawn connection: line in its grade texture, arrowhead (or authority diamond), delay ticks."""
    base = trim(poly, start_gap, end_gap) if (start_gap or end_gap) else poly
    kind = kind or step.get("type")
    end = ""
    line_poly = base
    if head:
        L = 12 if kind == "authority" else 9
        line_poly = trim(base, 0, L - 0.5)
        if kind == "authority":
            end = diamond_at(base, bg=bg, ink=color)
        else:
            end = arrow_at(base, fill=RED if red else color, edge=INK if red else None)
    out = stroke(line_poly, step.get("evidence"), step.get("conceptual"), width, color, bg, red)
    if ticks and step.get("delay"):
        out += ticks_on(base, TICKS[step["delay"]], color=color)
    return out + end


def sign_pill(cx, cy, step, record=True, size=13, bg=NEWS, ink=INK, ring=None, ring_red=False, extra=""):
    """The step's label at its smallest: the sign, with the record square when the grade is documented (M1)."""
    g = sign_glyph(step["polarity"]) if step.get("polarity") else ""
    if step.get("type") == "authority":
        g = "no sign"
    doc = record and step.get("evidence") == "documented"
    tw = text_w(g, size, 700) if len(g) > 1 else size * 0.62
    w = max(20, tw + 12 + (11 if doc else 0))
    h = 20
    x0 = cx - w / 2
    out = [f'<rect x="{x0:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{bg}" stroke="{ink}" stroke-width="1.25"/>']
    if doc:
        out.append(f'<rect x="{x0 + 7:.1f}" y="{cy - 3.25:.1f}" width="6.5" height="6.5" fill="{ink}" data-record="1"/>')
        tx = x0 + 7 + 6.5 + 4 + tw / 2
    else:
        tx = cx
    out.append(T(tx, cy + size * 0.36, g, size, 700, ink, "middle", extra=' data-sign-glyph="1"'))
    if ring:
        out.append(target_ring_rect(x0 - 4, cy - h / 2 - 4, w + 8, h + 8, red=ring_red, ids=ring))
    return f'<g class="pill"{extra}>' + "".join(out) + "</g>", w


def target_ring_rect(x, y, w, h, red=False, ids=()):
    r = h / 2
    tag = f' data-target="{esc(" ".join(ids))}"' if ids else ""
    if red:
        return (f'<g class="tg"{tag} data-red="1"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="none" stroke="{INK}" stroke-width="5"/>'
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="none" stroke="{RED}" stroke-width="2.75"/></g>')
    return f'<rect class="tg"{tag} x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="none" stroke="{INK}" stroke-width="1.5"/>'


def target_ring_circle(cx, cy, r, red=False, ids=()):
    tag = f' data-target="{esc(" ".join(ids))}"' if ids else ""
    if red:
        return (f'<g class="tg"{tag} data-red="1"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{INK}" stroke-width="5"/>'
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{RED}" stroke-width="2.75"/></g>')
    return f'<circle class="tg"{tag} cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{INK}" stroke-width="1.5"/>'


def step_attrs(step):
    """data-* attributes for one drawn step, read back by the verification script."""
    a = {"data-step": str(step["index"]), "data-sign": step.get("polarity") or "none"}
    if step.get("conceptual"):
        a["data-concept"] = "1"
        a["data-from-label"] = step["from_label"]
        a["data-to-label"] = step["to_label"]
    else:
        a.update({"data-link": step["id"], "data-from": step["from"], "data-to": step["to"], "data-grade": step["evidence"],
                  "data-delay": step["delay"], "data-type": step["type"]})
    return "".join(f' {k}="{esc(v)}"' for k, v in a.items())


def link_attrs(l):
    a = {"data-link": l["id"], "data-from": l["from"], "data-to": l["to"], "data-sign": l["polarity"] or "none",
         "data-grade": l["evidence"], "data-delay": l["delay"], "data-type": l["type"]}
    return "".join(f' {k}="{esc(v)}"' for k, v in a.items())


def node_attrs(code, label=None):
    a = {"data-node": code}
    if label:
        a["data-label"] = label
    return "".join(f' {k}="{esc(v)}"' for k, v in a.items())


# ------------------------------------------------------------------ loop kind marks (new, flagged as an option)

def kind_mark(cx, cy, kind, r=11, ink=INK):
    """Reinforcing: an opening spiral (each turn adds to the last). Balancing: a ring held at a set point.
    Drawn in ink only, never red. Studio addition beside M1 to M4, flagged for Dustin."""
    if kind == "R":
        pts = []
        for i in range(0, 61):
            t = i / 60
            a = -math.pi / 2 + t * 2 * math.pi * 1.25
            rr = r * (0.28 + 0.72 * t)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        body = f'<path d="{path_d(pts)}" fill="none" stroke="{ink}" stroke-width="1.75" stroke-linecap="round"/>'
        body += arrow_at(pts, 6, 3.2, ink)
    else:
        body = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{ink}" stroke-width="1.75"/>'
                f'<line x1="{cx - r - 4:.1f}" y1="{cy:.1f}" x2="{cx + r + 4:.1f}" y2="{cy:.1f}" stroke="{ink}" stroke-width="1.75"/>'
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.6" fill="{ink}"/>')
    return f'<g class="kind" data-kind="{kind}">{body}</g>'
