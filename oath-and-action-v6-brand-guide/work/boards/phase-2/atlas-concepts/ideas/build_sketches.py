#!/usr/bin/env python3
"""Build the from-scratch atlas directions board for "Who Do They Answer To?".

Reads only the model file and the variable icon map, draws ten overview
sketches and 230 loop thumbnails from the real data, and writes:

  20261030_From-Scratch-Directions-Sketches.html   (beside this script)
  work/handoffs/phase-2/20261030_Atlas-From-Scratch-Directions.md

Run with:  python3 -I build_sketches.py
"""
import html
import json
import math
import os
import random
import re
from collections import Counter, defaultdict, deque
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
MODEL = os.path.join(ROOT, "work/boards/phase-2/maps/20261028_Maps-Model-Data.json")
ICONMAP = os.path.join(ROOT, "work/boards/phase-2/atlas-concepts/shared/20261030_Variable-Icon-Map.json")
ICONDIR = os.path.join(ROOT, "work/build/assets/civic-line")
OUT_HTML = os.path.join(HERE, "20261030_From-Scratch-Directions-Sketches.html")
OUT_MD = os.path.join(ROOT, "work/handoffs/phase-2/20261030_Atlas-From-Scratch-Directions.md")

# Brand colors, and only these.
NEWS, CHAR, RED, PRU, STONE, VERD, WHITE = ("#DCD9D2", "#121212", "#E63946", "#1F2D5A",
                                            "#5D636D", "#4A7C74", "#FFFFFF")

FONTS = {
    "inter": "Inter, 'Inter Tight', system-ui, sans-serif",
    "tight": "'Inter Tight', Inter, system-ui, sans-serif",
    "lora": "Lora, Georgia, serif",
}

# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------
M = json.load(open(MODEL))
IM = json.load(open(ICONMAP))
NODES = M["nodes"]
LINKS = M["links"]
LOOPS = M["loops"]
ORDER = M["order"]
LOOP_ORDER = M["loop_order"]
AREA_OF = {}
AREA_NODES = {}
AREA_TITLE = {}
for a in M["areas"]:
    AREA_NODES[a["id"]] = list(a["nodes"])
    AREA_TITLE[a["id"]] = a["title"]
    for n in a["nodes"]:
        AREA_OF[n] = a["id"]
CORE_AREAS = ["A", "B", "C", "D", "E"]
CORE = [n for n in ORDER if AREA_OF[n] in CORE_AREAS]

OUT = defaultdict(list)
INN = defaultdict(list)
for l in LINKS.values():
    OUT[l["from"]].append(l)
    INN[l["to"]].append(l)
DEG = {n: len(OUT[n]) + len(INN[n]) for n in ORDER}
LOOPCOUNT = Counter()
for lp in LOOPS.values():
    for s in lp["stations"]:
        if s["code"]:
            LOOPCOUNT[s["code"]] += 1
LOOP_LINKS = {l["id"] for l in LINKS.values() if l["loops"]}
DELAY_W = {"S": 1, "M": 2, "L": 3}


def label(n):
    return NODES[n]["label"]


def loop_steps(lid):
    return LOOPS[lid]["steps"]


def loop_stations(lid):
    return LOOPS[lid]["stations"]


def is_sketch(lid):
    return LOOPS[lid]["conceptual"]


def loop_color(lid, dark=False):
    if LOOPS[lid]["type"] == "B":
        return VERD
    return WHITE if dark else PRU


# --------------------------------------------------------------------------
# Facts used in the prose (computed, never typed by hand)
# --------------------------------------------------------------------------
def area_pair_counts():
    c = Counter()
    inl = Counter()
    for l in LINKS.values():
        k = (AREA_OF[l["from"]], AREA_OF[l["to"]])
        c[k] += 1
        if l["loops"]:
            inl[k] += 1
    return c, inl


APC, APC_LOOP = area_pair_counts()
FORWARD = sum(APC[(a, b)] for a, b in zip(CORE_AREAS, CORE_AREAS[1:] + CORE_AREAS[:1]))
BACKWARD = sum(APC[(b, a)] for a, b in zip(CORE_AREAS, CORE_AREAS[1:] + CORE_AREAS[:1]))


def upstream_distance(target):
    dist = {target: 0}
    q = deque([target])
    while q:
        u = q.popleft()
        for l in INN[u]:
            v = l["from"]
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


HOME = "A4"
HOME_DIST = upstream_distance(HOME)


def scc():
    idx, low, st, on, out, c = {}, {}, [], set(), [], [0]

    def go(v):
        idx[v] = low[v] = c[0]
        c[0] += 1
        st.append(v)
        on.add(v)
        for l in OUT[v]:
            w = l["to"]
            if w not in idx:
                go(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = st.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            out.append(comp)

    for n in ORDER:
        if n not in idx:
            go(n)
    return out


KNOT = max(scc(), key=len)
CORE_CHORDS = [l for l in LINKS.values() if AREA_OF[l["from"]] in CORE_AREAS and AREA_OF[l["to"]] in CORE_AREAS]
SIDE = {n: ("ECON" if AREA_OF[n] in ("A", "production", "household", "money")
            else "DEM" if AREA_OF[n] in ("B", "C", "D", "E") else AREA_OF[n]) for n in ORDER}
CROSSINGS = [l for l in LINKS.values() if {SIDE[l["from"]], SIDE[l["to"]]} == {"ECON", "DEM"}]
SPINE_ORDER = (AREA_NODES["X"] + AREA_NODES["TC"] + AREA_NODES["money"] + AREA_NODES["production"]
               + AREA_NODES["household"] + [n for a in CORE_AREAS for n in AREA_NODES[a]])
SPINE_IX = {n: i for i, n in enumerate(SPINE_ORDER)}
SPINE_BACK = [l for l in LINKS.values() if SPINE_IX[l["to"]] < SPINE_IX[l["from"]]]

FACTS = {
    "forward": FORWARD,
    "backward": BACKWARD,
    "knot": len(KNOT),
    "outside_knot": len(ORDER) - len(KNOT),
    "e1_loops": LOOPCOUNT["E1"],
    "e1_deg": DEG["E1"],
    "no_loop": sum(1 for n in ORDER if LOOPCOUNT[n] == 0),
    "home_max": max(HOME_DIST.values()),
    "home_reach": len(HOME_DIST),
    "home_direct": sum(1 for v in HOME_DIST.values() if v == 1),
    "crossings": len(CROSSINGS),
    "to_dem": sum(1 for l in CROSSINGS if SIDE[l["to"]] == "DEM"),
    "to_econ": sum(1 for l in CROSSINGS if SIDE[l["to"]] == "ECON"),
    "to_econ_e1": sum(1 for l in CROSSINGS if SIDE[l["to"]] == "ECON" and l["from"] == "E1"),
    "core_chords": len(CORE_CHORDS),
    "core_chords_loop": sum(1 for l in CORE_CHORDS if l["loops"]),
    "spine_back": len(SPINE_BACK),
    "spine_fwd": len(LINKS) - len(SPINE_BACK),
}
assert FACTS["home_reach"] == len(ORDER)

# --------------------------------------------------------------------------
# Icons (Civic Line, used as drawn)
# --------------------------------------------------------------------------
ICON_FILE = {}
for v in IM["variables"]:
    ICON_FILE[(v["variable"], "black")] = os.path.join(ROOT, v["black"])
    ICON_FILE[(v["variable"], "newsprint")] = os.path.join(
        ROOT, v["black"].replace("/black/", "/newsprint/").replace("-Black.svg", "-Newsprint.svg"))
for fn in os.listdir(os.path.join(ICONDIR, "black")):
    m = re.search(r"-(R-\d\d)-", fn)
    if m:
        ICON_FILE[(m.group(1), "black")] = os.path.join(ICONDIR, "black", fn)
        ICON_FILE[(m.group(1), "newsprint")] = os.path.join(
            ICONDIR, "newsprint", fn.replace("-Black.svg", "-Newsprint.svg"))
_ICON_CACHE = {}


def icon_inner(key, ed):
    if (key, ed) not in _ICON_CACHE:
        src = open(ICON_FILE[(key, ed)]).read()
        body = re.search(r"<svg[^>]*>(.*)</svg>", src, re.S).group(1)
        body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
        body = re.sub(r"<desc>.*?</desc>", "", body, flags=re.S)
        body = re.sub(r"\s+", " ", body).strip()
        _ICON_CACHE[(key, ed)] = body
    return _ICON_CACHE[(key, ed)]


def symbol(pfx, key, ed):
    body = icon_inner(key, ed)
    sid = f"{pfx}-{key}-{ed}"
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{sid}-{m.group(1)}"', body)
    body = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{sid}-{m.group(1)})", body)
    return f'<symbol id="{sid}" viewBox="0 0 128 128">{body}</symbol>'


# --------------------------------------------------------------------------
# SVG helpers
# --------------------------------------------------------------------------
def f1(v):
    return f"{v:.1f}"


def esc(s):
    return html.escape(str(s), quote=True)


def dash(ev, w):
    k = max(1.0, w / 1.15)
    if ev in ("documented", "well-supported"):
        return ""
    if ev == "plausible":
        return f' stroke-dasharray="{4.2 * k:.1f} {2.9 * k:.1f}"'
    if ev == "plausible_contested":
        return f' stroke-dasharray="{4.8 * k:.1f} {2.4 * k:.1f} 0.1 {2.4 * k:.1f}" stroke-linecap="round"'
    if ev == "hypothesis":
        return f' stroke-dasharray="0.1 {2.7 * k:.1f}" stroke-linecap="round"'
    return ""


class Svg:
    def __init__(self, pfx, w=640, h=400, bg=NEWS, title=""):
        self.pfx, self.w, self.h, self.bg, self.title = pfx, w, h, bg, title
        self.parts = []
        self.icons = set()

    def add(self, *s):
        self.parts.extend(s)

    def icon(self, key, ed, x, y, size, extra=""):
        self.icons.add((key, ed))
        return (f'<use href="#{self.pfx}-{key}-{ed}" x="{f1(x)}" y="{f1(y)}" '
                f'width="{f1(size)}" height="{f1(size)}"{extra}/>')

    def icon_matrix(self, key, ed, m):
        self.icons.add((key, ed))
        mat = " ".join(f"{v:.4f}" for v in m)
        return f'<use href="#{self.pfx}-{key}-{ed}" width="128" height="128" transform="matrix({mat})"/>'

    def render(self, cls="", size=None):
        defs = "".join(symbol(self.pfx, k, e) for k, e in sorted(self.icons))
        wh = f'width="{self.w}" height="{self.h}"' if size is None else size
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" {wh} '
                f'class="{cls}" role="img" aria-label="{esc(self.title)}">'
                f'<defs>{defs}</defs><rect width="{self.w}" height="{self.h}" fill="{self.bg}"/>'
                + "".join(self.parts) + "</svg>")


def T(x, y, s, size=13, fill=CHAR, weight=400, anchor="start", fam="inter", ls=0.0,
      halo=None, italic=False, extra=""):
    assert size >= 13, s
    st = f' letter-spacing="{ls}"' if ls else ""
    hl = (f' stroke="{halo}" stroke-width="3.2" stroke-linejoin="round" paint-order="stroke"'
          if halo else "")
    it = ' font-style="italic"' if italic else ""
    return (f'<text x="{f1(x)}" y="{f1(y)}" font-family="{FONTS[fam]}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st}{hl}{it}{extra}>'
            f"{esc(s)}</text>")


def TL(x, y, lines, size=13, lh=None, **kw):
    lh = lh or size * 1.3
    return "".join(T(x, y + i * lh, s, size=size, **kw) for i, s in enumerate(lines))


def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def P(d, color, w, ev=None, fill="none", extra=""):
    return (f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}"'
            f'{dash(ev, w)} stroke-linejoin="round"{extra}/>')


def band(d, bg, w=1.4, color=STONE):
    """Hollow band for sketched loops: no numbered chain, so no evidence texture."""
    return P(d, color, w + 2.2) + P(d, bg, w)


def L(x1, y1, x2, y2, color, w, ev=None, extra=""):
    return (f'<line x1="{f1(x1)}" y1="{f1(y1)}" x2="{f1(x2)}" y2="{f1(y2)}" stroke="{color}" '
            f'stroke-width="{w}"{dash(ev, w)}{extra}/>')


def C(x, y, r, fill=WHITE, stroke=CHAR, w=1.0, extra=""):
    s = f' stroke="{stroke}" stroke-width="{w}"' if stroke else ""
    return f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{fill}"{s}{extra}/>'


def R(x, y, w, h, fill=WHITE, stroke=None, sw=1.0, rx=0, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" rx="{rx}" '
            f'fill="{fill}"{s}{extra}/>')


def poly(pts, fill, stroke=None, sw=0.8, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    return f'<polygon points="{" ".join(f"{f1(x)},{f1(y)}" for x, y in pts)}" fill="{fill}"{s}{extra}/>'


def AH(x, y, ang, size, color):
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    return poly([(x, y), (x + size * math.cos(a1), y + size * math.sin(a1)),
                 (x + size * math.cos(a2), y + size * math.sin(a2))], color)


def qpt(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])


def qtan(p0, p1, p2, t):
    return math.atan2(2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1]),
                      2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]))


def cpt(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def ctan(p0, p1, p2, p3, t):
    u = 1 - t
    dx = 3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
    dy = 3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
    return math.atan2(dy, dx)


def qseg(p0, p1, p2, t0, t1):
    a, b = qpt(p0, p1, p2, t0), qpt(p0, p1, p2, t1)
    q = tuple((1 - t0) * (1 - t1) * p0[i] + ((1 - t0) * t1 + t0 * (1 - t1)) * p1[i] + t0 * t1 * p2[i]
              for i in range(2))
    return a, q, b


def qtrim(p0, p1, p2, r0, r1):
    t0, t1 = 0.0, 1.0
    for i in range(1, 400):
        t = i / 400
        x, y = qpt(p0, p1, p2, t)
        if math.hypot(x - p0[0], y - p0[1]) >= r0:
            t0 = t
            break
    for i in range(1, 400):
        t = 1 - i / 400
        x, y = qpt(p0, p1, p2, t)
        if math.hypot(x - p2[0], y - p2[1]) >= r1:
            t1 = t
            break
    return qseg(p0, p1, p2, t0, t1)


def loop_curves(pts, bow=0.2):
    """Closed curve through station points, one segment per step.
    Returns a list of ('q', p0, c, p1) or ('c', p0, c1, c2, p1)."""
    n = len(pts)
    segs = []
    if n == 2:
        (x0, y0), (x1, y1) = pts
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = x1 - x0, y1 - y0
        px, py = -dy * bow * 1.6, dx * bow * 1.6
        segs.append(("q", pts[0], (mx + px, my + py), pts[1]))
        segs.append(("q", pts[1], (mx - px, my - py), pts[0]))
        return segs
    for i in range(n):
        p_1, p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p0[0] + (p1[0] - p_1[0]) / 6, p0[1] + (p1[1] - p_1[1]) / 6)
        c2 = (p1[0] - (p2[0] - p0[0]) / 6, p1[1] - (p2[1] - p0[1]) / 6)
        segs.append(("c", p0, c1, c2, p1))
    return segs


def seg_d(s):
    if s[0] == "q":
        _, a, c, b = s
        return f"M{f1(a[0])} {f1(a[1])}Q{f1(c[0])} {f1(c[1])} {f1(b[0])} {f1(b[1])}"
    _, a, c1, c2, b = s
    return (f"M{f1(a[0])} {f1(a[1])}C{f1(c1[0])} {f1(c1[1])} {f1(c2[0])} {f1(c2[1])} "
            f"{f1(b[0])} {f1(b[1])}")


def seg_mid(s, t=0.55):
    if s[0] == "q":
        _, a, c, b = s
        return qpt(a, c, b, t), qtan(a, c, b, t)
    _, a, c1, c2, b = s
    return cpt(a, c1, c2, b, t), ctan(a, c1, c2, b, t)


def draw_loop(lid, pts, color, w, bg, arrows=True, ah=4.2, bow=0.2):
    """Draw a loop through station points with evidence textures per step."""
    out = []
    segs = loop_curves(pts, bow)
    steps = loop_steps(lid)
    for s, st in zip(segs, steps):
        d = seg_d(s)
        if st["conceptual"]:
            out.append(band(d, bg, max(0.9, w * 0.7)))
        else:
            out.append(P(d, color, w, st["evidence"], extra=' stroke-linecap="round"' if st["evidence"] in ("documented", "well-supported") else ""))
        if arrows and not st["conceptual"]:
            (mx, my), ang = seg_mid(s)
            out.append(AH(mx + math.cos(ang) * ah * 0.5, my + math.sin(ang) * ah * 0.5, ang, ah, color))
    return "".join(out)


def header(svg, headline, dark=False, x=16, y=26, width=88):
    ink = NEWS if dark else CHAR
    sub = NEWS if dark else STONE
    svg.add(R(x, y - 14, 58, 19, fill="none", stroke=ink, sw=1, rx=2),
            T(x + 29, y, "SKETCH", 13, ink, 600, "middle", ls=1.2))
    lines = wrap(headline, width)
    svg.add(TL(x + 70, y, lines, 13, 17, fill=ink, weight=500))
    return len(lines)


def thumb_svg(pfx, bg, draw, size=76):
    s = Svg(pfx, size, size, bg)
    draw(s)
    return s.render(cls="thumb", size=f'width="{size}" height="{size}"')


# --------------------------------------------------------------------------
# Force layout (Fruchterman and Reingold, with anchors and collision radii)
# --------------------------------------------------------------------------
def force_layout(ids, edges, anchors, box, iters=900, seed=5, kscale=0.8, grav=0.035,
                 radii=None, edge_k=1.0):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    pos = {}
    for i in ids:
        ax, ay, _ = anchors.get(i, ((x0 + x1) / 2, (y0 + y1) / 2, 0))
        pos[i] = [ax + rnd.uniform(-18, 18), ay + rnd.uniform(-18, 18)]
    k = kscale * math.sqrt((x1 - x0) * (y1 - y0) / len(ids))
    t = k * 0.5
    radii = radii or {}
    for it in range(iters):
        disp = {i: [0.0, 0.0] for i in ids}
        for a, b in combinations(ids, 2):
            dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 0.01
            f = k * k / d
            mind = radii.get(a, 6) + radii.get(b, 6) + 6
            if d < mind:
                f += (mind - d) * 3.0
            disp[a][0] += dx / d * f
            disp[a][1] += dy / d * f
            disp[b][0] -= dx / d * f
            disp[b][1] -= dy / d * f
        for a, b, wt in edges:
            dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 0.01
            f = wt * edge_k * d * d / k
            disp[a][0] -= dx / d * f
            disp[a][1] -= dy / d * f
            disp[b][0] += dx / d * f
            disp[b][1] += dy / d * f
        for i in ids:
            if i in anchors:
                ax, ay, s = anchors[i]
                disp[i][0] += (ax - pos[i][0]) * grav * s * k
                disp[i][1] += (ay - pos[i][1]) * grav * s * k
            dx, dy = disp[i]
            d = math.hypot(dx, dy) or 0.01
            step = min(d, t)
            r = radii.get(i, 6)
            pos[i][0] = min(max(pos[i][0] + dx / d * step, x0 + r), x1 - r)
            pos[i][1] = min(max(pos[i][1] + dy / d * step, y0 + r), y1 - r)
        t = max(0.4, t * 0.994)
    return {i: tuple(p) for i, p in pos.items()}


# ==========================================================================
# 1. GREAT CIRCLE
# ==========================================================================
GC_GAP = 1.7
GC_STEP = 2 * math.pi / (len(CORE) + 5 * GC_GAP)


def gc_angles():
    cslot = 6 + 6 + 2 + 2 * GC_GAP
    th = -cslot * GC_STEP + math.radians(8)
    ang = {}
    for a in CORE_AREAS:
        for n in AREA_NODES[a]:
            ang[n] = th
            th += GC_STEP
        th += GC_GAP * GC_STEP
    return ang


GC_ANG = gc_angles()


def gc_pt(n, cx, cy, r):
    a = GC_ANG[n]
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def gc_chord(p0, p1, cx, cy, r):
    d = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    k = 0.92 - 0.75 * (d / (2 * r))
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    return (cx + (mx - cx) * k, cy + (my - cy) * k)


def gc_ring_base(s, cx, cy, r, bg, ticks=True, arcs=True, aw=1.4):
    out = [C(cx, cy, r, fill="none", stroke=STONE, w=0.6)]
    if arcs:
        for a in CORE_AREAS:
            ns = AREA_NODES[a]
            a0, a1 = GC_ANG[ns[0]] - GC_STEP * 0.45, GC_ANG[ns[-1]] + GC_STEP * 0.45
            rr = r + max(2.5, r * 0.07)
            out.append(P(f"M{f1(cx + rr * math.cos(a0))} {f1(cy + rr * math.sin(a0))}"
                         f"A{f1(rr)} {f1(rr)} 0 0 1 {f1(cx + rr * math.cos(a1))} {f1(cy + rr * math.sin(a1))}",
                         CHAR, aw))
    if ticks:
        for n in CORE:
            x, y = gc_pt(n, cx, cy, r)
            out.append(C(x, y, max(0.8, r * 0.022), fill=STONE, stroke=None))
    s.add(*out)


def gc_loop(s, lid, cx, cy, r, bg, w=1.6, ah=3.6, dot=2.0):
    col = loop_color(lid)
    sts = loop_stations(lid)
    if is_sketch(lid):
        k = len(sts)
        pts = []
        for i, st in enumerate(sts):
            if st["code"]:
                pts.append(gc_pt(st["code"], cx, cy, r))
            else:
                a = -math.pi / 2 + 2 * math.pi * i / k
                pts.append((cx + r * 0.32 * math.cos(a), cy + r * 0.32 * math.sin(a)))
        s.add(draw_loop(lid, pts, col, w, bg, arrows=False, bow=0.25))
        for p, st in zip(pts, sts):
            s.add(C(p[0], p[1], dot, fill=bg if not st["code"] else CHAR, stroke=STONE if not st["code"] else None, w=1))
        return
    for st in loop_steps(lid):
        p0, p1 = gc_pt(st["from"], cx, cy, r), gc_pt(st["to"], cx, cy, r)
        c = gc_chord(p0, p1, cx, cy, r)
        a, q, b = qtrim(p0, c, p1, dot + 0.5, dot + 0.5)
        s.add(P(f"M{f1(a[0])} {f1(a[1])}Q{f1(q[0])} {f1(q[1])} {f1(b[0])} {f1(b[1])}", col, w, st["evidence"]))
        (mx, my), ang = qpt(a, q, b, 0.55), qtan(a, q, b, 0.55)
        s.add(AH(mx, my, ang, ah, col))
    for st in sts:
        x, y = gc_pt(st["code"], cx, cy, r)
        s.add(C(x, y, dot, fill=CHAR, stroke=None))


def gc_thumb(lid):
    def draw(s):
        gc_ring_base(s, 38, 38, 27, NEWS, aw=1.2)
        gc_loop(s, lid, 38, 38, 27, NEWS, w=1.5, ah=3.4, dot=1.9)
    return thumb_svg(f"gc-{lid}", NEWS, draw)


def sketch_great_circle():
    s = Svg("s1", bg=NEWS, title="Great Circle sketch")
    cx, cy, r = 228, 226, 122
    header(s, "One connection sits in three loops: incumbent-drawn maps create safe seats (L42).")
    # outside drivers
    xt = defaultdict(list)
    for l in LINKS.values():
        if AREA_OF[l["from"]] == "X" and AREA_OF[l["to"]] in CORE_AREAS:
            xt[l["from"]].append(l)
    # discs for the economy layer and the technology group
    discs = {"EC": (62, 92, "Economy layer", 12), "TC": (60, 360, "Technology", 8)}
    for g, (dx, dy, name, cnt) in discs.items():
        for l in LINKS.values():
            fa, ta = AREA_OF[l["from"]], AREA_OF[l["to"]]
            fg = "EC" if fa in ("production", "household", "money") else fa
            tg = "EC" if ta in ("production", "household", "money") else ta
            other = l["to"] if fg == g and ta in CORE_AREAS else l["from"] if tg == g and fa in CORE_AREAS else None
            if other:
                px, py = gc_pt(other, cx, cy, r)
                s.add(L(dx, dy, px, py, STONE, 0.6, l["evidence"]))
    gc_ring_base(s, cx, cy, r, NEWS, ticks=False, aw=3.2)
    # chords, non-loop first
    for layer in (0, 1):
        for l in CORE_CHORDS:
            if (l["id"] in LOOP_LINKS) != bool(layer) or l["id"] == "L42":
                continue
            p0, p1 = gc_pt(l["from"], cx, cy, r), gc_pt(l["to"], cx, cy, r)
            c = gc_chord(p0, p1, cx, cy, r)
            a, q, b = qtrim(p0, c, p1, 4.5, 5.5)
            col = PRU if layer else STONE
            if layer and all(LOOPS[x]["type"] == "B" for x in l["loops"]):
                col = VERD
            w = 1.25 if layer else 0.7
            s.add(P(f"M{f1(a[0])} {f1(a[1])}Q{f1(q[0])} {f1(q[1])} {f1(b[0])} {f1(b[1])}", col, w, l["evidence"]))
            if layer:
                s.add(AH(b[0], b[1], qtan(a, q, b, 1), 4.2, col))
    l = LINKS["L42"]
    p0, p1 = gc_pt("C4", cx, cy, r), gc_pt("C1", cx, cy, r)
    c = gc_chord(p0, p1, cx, cy, r)
    a, q, b = qtrim(p0, c, p1, 4.5, 5.5)
    s.add(P(f"M{f1(a[0])} {f1(a[1])}Q{f1(q[0])} {f1(q[1])} {f1(b[0])} {f1(b[1])}", RED, 2.6, l["evidence"]),
          AH(b[0], b[1], qtan(a, q, b, 1), 6, RED))
    for n in CORE:
        x, y = gc_pt(n, cx, cy, r)
        s.add(C(x, y, 3.6, fill=CHAR if LOOPCOUNT[n] else WHITE, stroke=CHAR, w=1))
    # drivers
    for xid, ls_ in xt.items():
        vx = sum(math.cos(GC_ANG[l["to"]]) for l in ls_)
        vy = sum(math.sin(GC_ANG[l["to"]]) for l in ls_)
        a = math.atan2(vy, vx)
        rx = r + 44
        bx, by = cx + rx * math.cos(a), cy + rx * math.sin(a)
        for l in ls_:
            px, py = gc_pt(l["to"], cx, cy, r + 6)
            s.add(L(bx, by, px, py, CHAR, 0.8, l["evidence"]))
            s.add(AH(px, py, math.atan2(py - by, px - bx), 3.6, CHAR))
        s.add(R(bx - 5, by - 5, 10, 10, fill=NEWS, stroke=CHAR, sw=1.1))
        s.add(T(bx + (9 if math.cos(a) >= 0 else -9), by + 4.5, xid, 13, CHAR, 500,
                "start" if math.cos(a) >= 0 else "end", halo=NEWS))
    for g, (dx, dy, name, cnt) in discs.items():
        s.add(C(dx, dy, 17, fill=WHITE, stroke=CHAR, w=1.2),
              T(dx, dy + 4.6, str(cnt), 13, CHAR, 700, "middle"),
              T(dx, dy + (31 if dy < 200 else -24), name, 13, CHAR, 500, "middle", halo=NEWS))
    # area labels
    for a in CORE_AREAS:
        ns = AREA_NODES[a]
        mid = (GC_ANG[ns[0]] + GC_ANG[ns[-1]]) / 2
        rr = r + 22
        x, y = cx + rr * math.cos(mid), cy + rr * math.sin(mid)
        cs = math.cos(mid)
        anchor = "start" if cs > 0.25 else "end" if cs < -0.25 else "middle"
        words = AREA_TITLE[a].split()
        lines = [" ".join(words[:1]), " ".join(words[1:])] if len(words) > 1 else words
        if math.sin(mid) < -0.6:
            lines = [AREA_TITLE[a]]
            y -= 4
        yy = y + 4 - (len(lines) - 1) * 8 + (6 if math.sin(mid) > 0.6 else 0)
        s.add(T(x, yy - 15, a, 13, STONE, 700, anchor, halo=NEWS) if False else "")
        s.add(TL(x, yy, lines, 13, 15, fill=CHAR, weight=600, anchor=anchor, halo=NEWS, fam="tight"))
    # red callout
    mx, my = qpt(a_ := gc_pt("C4", cx, cy, r), gc_chord(a_, gc_pt("C1", cx, cy, r), cx, cy, r), gc_pt("C1", cx, cy, r), 0.5)
    s.add(L(mx, my, 300, 108, CHAR, 0.7), C(mx, my, 2, fill=CHAR, stroke=None))
    s.add(TL(256, 82, ["L42 · in R4a, R10, R12", "R-03 and R-04 act here"], 13, 15, fill=CHAR, weight=500, halo=NEWS))
    # right panel: R10 on the ring + thumbnails
    px = 470
    s.add(L(px - 14, 70, px - 14, 388, STONE, 0.6))
    s.add(T(px, 82, "R10 on the ring", 13, CHAR, 700))
    gc_ring_base(s, 548, 150, 52, NEWS, aw=2)
    gc_loop(s, "R10", 548, 150, 52, NEWS, w=2.1, ah=5, dot=2.6)
    s.add(TL(px, 226, wrap(LOOPS["R10"]["title"], 26), 13, 16, fill=CHAR))
    picks = ["R12", "R4a", "R1", "R6", "B4", "R8"]
    for i, lid in enumerate(picks):
        gx, gy = px + (i % 3) * 54, 290 + (i // 3) * 58
        gc_ring_base(s, gx + 22, gy + 18, 18, NEWS, aw=1.1)
        gc_loop(s, lid, gx + 22, gy + 18, 18, NEWS, w=1.3, ah=3, dot=1.6)
        s.add(T(gx + 22, gy + 52, lid, 13, CHAR, 600, "middle"))
    return s.render()


# ==========================================================================
# 2. STAR ATLAS
# ==========================================================================
def star_layout():
    anchors = {}
    A_ = {"TC": (90, 115), "A": (165, 245), "production": (80, 325), "household": (190, 340),
          "money": (60, 250), "B": (250, 135), "C": (395, 130), "D": (370, 285), "E": (270, 265)}
    XA = {"X1": (45, 175), "X2": (440, 70), "X3": (130, 380), "X4": (300, 72), "X5": (445, 385)}
    for n in ORDER:
        a = AREA_OF[n]
        if a == "X":
            anchors[n] = (*XA[n], 3.0)
        else:
            anchors[n] = (*A_[a], 1.2)
    edges = [(l["from"], l["to"], 1.6 if l["loops"] else 0.5) for l in LINKS.values()]
    radii = {n: 3 + 0.38 * DEG[n] for n in ORDER}
    return force_layout(ORDER, edges, anchors, (22, 62, 458, 392), iters=800, seed=11, kscale=0.62,
                        grav=0.04, radii=radii)


STAR = star_layout()


def star_r(n):
    return 1.3 + 0.36 * DEG[n]


def star_loop(s, lid, pos, rad, w, dark_bg, ah=3.6, scale=1.0):
    col = loop_color(lid, dark=True)
    pts = [pos[st["code"]] for st in loop_stations(lid)]
    segs = []
    for st in loop_steps(lid):
        p0, p1 = pos[st["from"]], pos[st["to"]]
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        d = math.hypot(dx, dy) or 1
        c = ((p0[0] + p1[0]) / 2 - dy * 0.12, (p0[1] + p1[1]) / 2 + dx * 0.12)
        a, q, b = qtrim(p0, c, p1, rad(st["from"]) + 2.2 * scale, rad(st["to"]) + 2.2 * scale)
        s.add(P(f"M{f1(a[0])} {f1(a[1])}Q{f1(q[0])} {f1(q[1])} {f1(b[0])} {f1(b[1])}", col, w, st["evidence"]))
        (mx, my), ang = qpt(a, q, b, 0.55), qtan(a, q, b, 0.55)
        s.add(AH(mx, my, ang, ah, col))
    return pts


def star_thumb(lid, size=76, bg=CHAR):
    def draw(s):
        sts = loop_stations(lid)
        if is_sketch(lid):
            k = len(sts)
            pts = [(size / 2 + 18 * math.cos(-math.pi / 2 + 2 * math.pi * i / k),
                    size / 2 + 18 * math.sin(-math.pi / 2 + 2 * math.pi * i / k)) for i in range(k)]
            s.add(draw_loop(lid, pts, STONE, 1.2, bg, arrows=False, bow=0.25))
            for p, st in zip(pts, sts):
                if st["code"]:
                    s.add(C(p[0], p[1], 3.2, fill=NEWS, stroke=None))
                else:
                    s.add(C(p[0], p[1], 2.6, fill=bg, stroke=NEWS, w=1))
            return
        codes = [st["code"] for st in sts]
        xs = [STAR[c][0] for c in codes]
        ys = [STAR[c][1] for c in codes]
        span = max(max(xs) - min(xs), max(ys) - min(ys), 30)
        k = (size - 22) / span
        mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        pos = {c: (size / 2 + (STAR[c][0] - mx) * k, size / 2 + (STAR[c][1] - my) * k) for c in codes}
        rad = lambda n: 1.2 + 0.25 * DEG[n]
        star_loop(s, lid, pos, rad, 1.25, True, ah=3.2, scale=0.6)
        for c in codes:
            s.add(C(pos[c][0], pos[c][1], rad(c), fill=NEWS, stroke=None))
    return thumb_svg(f"st-{lid}", bg, draw, size)


def sketch_star_atlas():
    s = Svg("s2", bg=CHAR, title="Star Atlas sketch")
    box = (14, 56, 462, 394)
    cell = 9
    grid = {}
    for gx in range(int((box[2] - box[0]) / cell)):
        for gy in range(int((box[3] - box[1]) / cell)):
            x, y = box[0] + (gx + 0.5) * cell, box[1] + (gy + 0.5) * cell
            best = min(ORDER, key=lambda n: (STAR[n][0] - x) ** 2 + (STAR[n][1] - y) ** 2)
            grid[(gx, gy)] = AREA_OF[best] if AREA_OF[best] not in ("production", "household", "money") else "EC"
    segs = []
    for (gx, gy), a in grid.items():
        x, y = box[0] + gx * cell, box[1] + gy * cell
        if (gx + 1, gy) in grid and grid[(gx + 1, gy)] != a:
            segs.append(f"M{f1(x + cell)} {f1(y)}v{cell}")
        if (gx, gy + 1) in grid and grid[(gx, gy + 1)] != a:
            segs.append(f"M{f1(x)} {f1(y + cell)}h{cell}")
    s.add(P("".join(segs), STONE, 0.8))
    s.add(R(box[0], box[1], box[2] - box[0], box[3] - box[1], fill="none", stroke=STONE, sw=0.8))
    header(s, "Each loop is a figure in the sky. All-party primaries (R-01) act on the red star, primary decisiveness.", dark=True, width=82)
    # faint non-loop connections
    for l in LINKS.values():
        if l["loops"]:
            continue
    order_loops = sorted([x for x in LOOP_ORDER if not is_sketch(x)], key=lambda x: LOOPS[x]["type"] == "B")
    for lid in order_loops:
        star_loop(s, lid, STAR, star_r, 1.15 if LOOPS[lid]["type"] == "R" else 1.6, True)
    for n in ORDER:
        x, y = STAR[n]
        fill = NEWS if LOOPCOUNT[n] else STONE
        if n == "C2":
            s.add(C(x, y, star_r(n) + 2.2, fill=RED, stroke=None))
        else:
            s.add(C(x, y, star_r(n), fill=fill, stroke=None))
    # region names
    cent = defaultdict(list)
    for (gx, gy), a in grid.items():
        cent[a].append((box[0] + (gx + 0.5) * cell, box[1] + (gy + 0.5) * cell))
    names = {"A": "ECONOMIC STRUCTURE", "B": "POLITICAL INPUTS", "C": "ELECTORAL COMPETITION",
             "D": "GOVERNING INSTITUTIONS", "E": "LEGITIMACY", "TC": "TECHNOLOGY", "EC": "ECONOMY LAYER"}
    offs = {"A": (0, 52), "B": (-6, -42), "C": (8, -40), "D": (20, 62), "E": (0, 40), "TC": (0, -40), "EC": (8, 36)}
    for a, nm in names.items():
        if a not in cent:
            continue
        ns = [STAR[n] for n in ORDER if (AREA_OF[n] if AREA_OF[n] not in ("production", "household", "money") else "EC") == a]
        mx = sum(p[0] for p in ns) / len(ns) + offs[a][0]
        my = sum(p[1] for p in ns) / len(ns) + offs[a][1]
        s.add(T(mx, my, nm, 13, STONE, 600, "middle", ls=1.1, halo=CHAR))
    # labels
    x, y = STAR["E1"]
    s.add(T(x + 10, y + 18, "Policy tilt to insiders", 13, NEWS, 500, halo=CHAR))
    x, y = STAR["C2"]
    s.add(TL(x + 9, y - 14, ["Primary decisiveness", "R-01 acts here"], 13, 15, fill=NEWS, weight=500, halo=CHAR))
    xs = [STAR[c][0] for c in ("C1", "C2", "C3", "C4")]
    ys = [STAR[c][1] for c in ("C1", "C2", "C3", "C4")]
    s.add(T(min(xs) - 8, max(ys) + 20, "R10", 13, WHITE, 700, halo=CHAR))
    # right column: figures
    px = 474
    s.add(T(px, 82, "FIGURES", 13, NEWS, 700, ls=1.2))
    s.add(TL(px, 100, ["Cropped from the sky,", "true to position"], 13, 15, fill=STONE))
    picks = ["R10", "R12", "R6", "R1", "B4", "R13"]
    for i, lid in enumerate(picks):
        gx, gy = px + (i % 2) * 80, 128 + (i // 2) * 88
        sub = Svg(f"s2t{i}", 70, 70, CHAR)
        s.add(f'<g transform="translate({gx},{gy})">' + re.sub(r'^<svg[^>]*>|</svg>$', '', star_thumb(lid, 70)) + "</g>")
        s.add(T(gx + 35, gy + 82, lid, 13, NEWS, 600, "middle"))
    return s.render()


# ==========================================================================
# 3. LEDGER GRID
# ==========================================================================
LEDGER_AREAS = ["A", "B", "C", "D", "E", "X", "production", "household", "money", "TC"]
LEDGER_CODES = {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "X": "X", "production": "P",
                "household": "H", "money": "M", "TC": "T"}
CORE_IX = {n: i for i, n in enumerate(CORE)}


def ledger_thumb(lid, size=76):
    def draw(s):
        n = len(CORE)
        x0, y0 = 7, 7
        c = (size - 14) / n
        s.add(R(x0, y0, n * c, n * c, fill=WHITE, stroke=STONE, sw=0.6))
        i = 0
        for a in CORE_AREAS:
            k = len(AREA_NODES[a])
            s.add(R(x0 + i * c, y0 + i * c, k * c, k * c, fill=NEWS, stroke=STONE, sw=0.5))
            i += k
        col = loop_color(lid)
        if is_sketch(lid):
            s.add(band(f"M{size/2-9} {size/2-9}h18v18h-18z", WHITE, 1.1))
            return
        for st in loop_steps(lid):
            a, b = CORE_IX[st["from"]], CORE_IX[st["to"]]
            ax, ay = x0 + (a + 0.5) * c, y0 + (a + 0.5) * c
            bx = x0 + (b + 0.5) * c
            by = y0 + (b + 0.5) * c
            s.add(P(f"M{f1(ax)} {f1(ay)}H{f1(bx)}V{f1(by)}", col, 1.5, st["evidence"]))
            s.add(C(bx, ay, 1.9, fill=CHAR, stroke=None))
    return thumb_svg(f"lg-{lid}", WHITE, draw, size)


def sketch_ledger():
    s = Svg("s3", bg=WHITE, title="Ledger Grid sketch")
    header(s, "R10 as a staircase. All-party primaries (R-01) act on the cell where decisive primaries reduce general-election pressure.", width=84)
    x0, y0, c = 46, 88, 22
    n = len(LEDGER_AREAS)
    s.add(T(x0, y0 - 24, "Areas: rows cause, columns respond", 13, CHAR, 700))
    for i, a in enumerate(LEDGER_AREAS):
        s.add(T(x0 + (i + 0.5) * c, y0 - 6, LEDGER_CODES[a], 13, CHAR, 600, "middle"))
        s.add(T(x0 - 7, y0 + (i + 0.5) * c + 4.5, LEDGER_CODES[a], 13, CHAR, 600, "end"))
    for i, a in enumerate(LEDGER_AREAS):
        for j, b in enumerate(LEDGER_AREAS):
            fill = NEWS if i == j else WHITE
            s.add(R(x0 + j * c, y0 + i * c, c, c, fill=fill, stroke=STONE, sw=0.5))
            cnt, inl = APC[(a, b)], APC_LOOP[(a, b)]
            for k in range(cnt):
                dx, dy = (k % 3) * 6 - 6, (k // 3) * 6 - 6
                s.add(C(x0 + (j + 0.5) * c + dx, y0 + (i + 0.5) * c + dy, 2.0,
                        fill=PRU if k < inl else STONE, stroke=None))
    for a, b in zip(CORE_AREAS, CORE_AREAS[1:] + CORE_AREAS[:1]):
        i, j = LEDGER_AREAS.index(a), LEDGER_AREAS.index(b)
        s.add(R(x0 + j * c + 1, y0 + i * c + 1, c - 2, c - 2, fill="none", stroke=CHAR, sw=1.6))
    ci = LEDGER_AREAS.index("C")
    s.add(R(x0 + ci * c - 1.5, y0 + ci * c - 1.5, c + 3, c + 3, fill="none", stroke=PRU, sw=2.2))
    s.add(L(x0 + (ci + 1) * c + 2, y0 + (ci + 0.5) * c, 352, 118, PRU, 1.0))
    ky = y0 + n * c + 22
    s.add(TL(x0 - 30, ky, ["Outlined: the forward circle, A to B,", "B to C, C to D, D to E and E to A.",
                          "P production, H household, M credit,", "trade and environment, T technology."],
             13, 16, fill=CHAR))
    s.add(C(x0 - 26, ky + 70, 2.2, fill=PRU, stroke=None), T(x0 - 18, ky + 74.5, "in a loop", 13, CHAR),
          C(x0 + 62, ky + 70, 2.2, fill=STONE, stroke=None), T(x0 + 70, ky + 74.5, "outside loops", 13, CHAR))
    # zoom C
    zx, zy, zc = 402, 118, 38
    cn = AREA_NODES["C"]
    s.add(T(zx - 50, zy - 24, "Inside C, variable by variable", 13, CHAR, 700))
    for i, nid in enumerate(cn):
        s.add(T(zx + (i + 0.5) * zc, zy - 7, nid, 13, CHAR, 600, "middle"))
        s.add(T(zx - 8, zy + (i + 0.5) * zc + 4.5, nid, 13, CHAR, 600, "end"))
    for i, a in enumerate(cn):
        for j, b in enumerate(cn):
            s.add(R(zx + j * zc, zy + i * zc, zc, zc, fill=NEWS if i == j else WHITE, stroke=STONE, sw=0.6))
    for i, a in enumerate(cn):
        s.add(s.icon(a, "black", zx + i * zc + 7, zy + i * zc + 7, zc - 14))
    # staircase for R10 under cell marks
    pts = []
    for st in loop_steps("R10"):
        a, b = cn.index(st["from"]), cn.index(st["to"])
        ax, ay = zx + (a + 0.5) * zc, zy + (a + 0.5) * zc
        bx, by = zx + (b + 0.5) * zc, zy + (b + 0.5) * zc
        s.add(P(f"M{f1(ax)} {f1(ay)}H{f1(bx)}V{f1(by)}", PRU, 2.4, st["evidence"]))
    for l in LINKS.values():
        if l["from"] in cn and l["to"] in cn:
            i, j = cn.index(l["from"]), cn.index(l["to"])
            x, y = zx + j * zc, zy + i * zc
            s.add(R(x + 9, y + 6, 20, 17, fill=WHITE, stroke=None))
            s.add(T(x + zc / 2, y + 20, "+" if l["polarity"] == "+" else "−", 16, CHAR, 600, "middle"))
            s.add(L(x + 7, y + zc - 7, x + zc - 7, y + zc - 7, CHAR, 1.6, l["evidence"]))
            if l["id"] == "L25":
                s.add(R(x + 1.5, y + 1.5, zc - 3, zc - 3, fill="none", stroke=RED, sw=2.6))
    i, j = cn.index("C2"), cn.index("C3")
    s.add(TL(zx + 5 * zc + 8, zy + i * zc + 14, ["L25", "R-01 acts", "here"], 13, 15, fill=CHAR, weight=500))
    ky = zy + 5 * zc + 20
    keys = [f"{n} {label(n)}" for n in cn]
    s.add(TL(zx - 50, ky, keys, 13, 16, fill=CHAR))
    return s.render()


# ==========================================================================
# 4. HONEYCOMB
# ==========================================================================
HEX_COLS, HEX_ROWS = 15, 10


def cube(c, r):
    x = c - (r - (r & 1)) // 2
    z = r
    return x, -x - z, z


def hdist(a, b):
    ax, ay, az = cube(*a)
    bx, by, bz = cube(*b)
    return max(abs(ax - bx), abs(ay - by), abs(az - bz))


def hex_layout():
    rnd = random.Random(21)
    cells = [(c, r) for r in range(HEX_ROWS) for c in range(HEX_COLS)]
    anchors = {"TC": (1.5, 1), "B": (6.5, 1), "C": (11, 2), "X": (7, 5), "A": (3, 4.5), "E": (7, 4.5),
               "D": (11, 6.5), "production": (1.5, 7.5), "household": (4.5, 8), "money": (7.5, 8.5)}
    group = {n: AREA_OF[n] for n in ORDER}
    occupied = {}
    pos = {}
    for n in ORDER:
        ax, ay = anchors[group[n]]
        free = sorted([c for c in cells if c not in occupied],
                      key=lambda c: (c[0] - ax) ** 2 + (c[1] - ay) ** 2 + rnd.random() * 0.1)
        pos[n] = free[0]
        occupied[free[0]] = n
    linkw = defaultdict(float)
    for l in LINKS.values():
        linkw[(l["from"], l["to"])] += 3.0 if l["loops"] else 1.0
    nbr = defaultdict(list)
    for (a, b), w in linkw.items():
        nbr[a].append((b, w))
        nbr[b].append((a, w))
    members = defaultdict(list)
    for n in ORDER:
        members[group[n]].append(n)

    def cost_of(n, p):
        c = 0.0
        for m, w in nbr[n]:
            d = hdist(p, pos[m])
            same = group[m] == group[n]
            c += w * (d if same else 0.35 * d)
        g = group[n]
        if g != "X":
            for m in members[g]:
                if m != n:
                    c += 2.2 * max(0, hdist(p, pos[m]) - 1)
        # keep other territories one cell away
        for q in cells:
            if q in occupied and occupied[q] != n and hdist(p, q) == 1 and group[occupied[q]] != g:
                c += 12
        if g == "X":
            c += 0.0
        return c

    T_ = 6.0
    for it in range(60000):
        n = rnd.choice(ORDER)
        if rnd.random() < 0.5:
            m = rnd.choice(members[group[n]])
            if m == n:
                continue
            pn, pm = pos[n], pos[m]
            before = cost_of(n, pn) + cost_of(m, pm)
            pos[n], pos[m] = pm, pn
            occupied[pm], occupied[pn] = n, m
            after = cost_of(n, pm) + cost_of(m, pn)
            if after > before and rnd.random() > math.exp((before - after) / T_):
                pos[n], pos[m] = pn, pm
                occupied[pn], occupied[pm] = n, m
        else:
            p = pos[n]
            q = rnd.choice(cells)
            if q in occupied:
                continue
            before = cost_of(n, p)
            del occupied[p]
            pos[n] = q
            occupied[q] = n
            after = cost_of(n, q)
            if after > before and rnd.random() > math.exp((before - after) / T_):
                del occupied[q]
                pos[n] = p
                occupied[p] = n
        T_ = max(0.05, T_ * 0.99992)
    return pos


HEX = hex_layout()


def hex_center(cr, x0, y0, r):
    c, rr = cr
    w = math.sqrt(3) * r
    return x0 + w * (c + 0.5 * (rr & 1)), y0 + 1.5 * r * rr


def hex_pts(x, y, r):
    return [(x + r * math.cos(math.radians(60 * i - 30)), y + r * math.sin(math.radians(60 * i - 30))) for i in range(6)]


def hex_bounds():
    cs = [c for c, r in HEX.values()]
    rs = [r for c, r in HEX.values()]
    return min(cs), max(cs), min(rs), max(rs)


def hex_thumb(lid, size=76):
    def draw(s):
        c0, c1, r0, r1 = hex_bounds()
        r = (size - 8) / ((c1 - c0 + 1.5) * math.sqrt(3))
        r = min(r, (size - 8) / ((r1 - r0) * 1.5 + 2))
        w = math.sqrt(3) * r
        x0 = (size - (c1 - c0 + 1.5) * w) / 2 + w / 2 - c0 * w
        y0 = (size - ((r1 - r0) * 1.5 * r)) / 2 - r0 * 1.5 * r
        codes = [st["code"] for st in loop_stations(lid) if st["code"]]
        col = loop_color(lid)
        for n, cr in HEX.items():
            x, y = hex_center(cr, x0, y0, r)
            s.add(poly(hex_pts(x, y, r * 0.92), col if n in codes else WHITE))
        if is_sketch(lid):
            s.add(band(f"M{size/2-10} {size-12}h20", NEWS, 1.0))
            return
        pts = [hex_center(HEX[st["code"]], x0, y0, r) for st in loop_stations(lid)]
        s.add(draw_loop(lid, pts, CHAR, 0.9, NEWS, arrows=False, bow=0.18))
    return thumb_svg(f"hx-{lid}", NEWS, draw, size)


def hex_edges(n, x, y, r):
    """Border edges of a tile: sides not shared with a same-area tile."""
    out = []
    pts = hex_pts(x, y, r)
    c, rr = HEX[n]
    same = {HEX[m] for m in ORDER if AREA_OF[m] == AREA_OF[n] and m != n}
    for i in range(6):
        a, b = pts[i], pts[(i + 1) % 6]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        # neighbor center is the reflection of this center across the edge midpoint
        nx, ny = 2 * mx - x, 2 * my - y
        hit = False
        for q in same:
            qx, qy = hex_center(q, 0, 0, r)
            cx0, cy0 = hex_center((c, rr), 0, 0, r)
            if abs((qx - cx0) - (nx - x)) < 1 and abs((qy - cy0) - (ny - y)) < 1:
                hit = True
        if not hit:
            out.append((a, b))
    return out


def sketch_honeycomb():
    s = Svg("s4", bg=NEWS, title="Honeycomb sketch")
    header(s, "Fifty-one equal tiles in ten territories. Two reforms, R-03 and R-46, act on safe seats.", width=84)
    r = 16.2
    c0, c1, r0, r1 = hex_bounds()
    w = math.sqrt(3) * r
    x0 = 26 - c0 * w + w / 2
    y0 = 74 - r0 * 1.5 * r
    for n in ORDER:
        x, y = hex_center(HEX[n], x0, y0, r)
        s.add(poly(hex_pts(x, y, r - 0.6), WHITE, STONE, 0.5))
        s.add(s.icon(n, "black", x - 10, y - 12, 20))
        k = LOOPCOUNT[n]
        for i in range(k):
            bx = x - (k - 1) * 2.1 + i * 4.2
            s.add(C(bx, y + 10.5, 1.5, fill=PRU, stroke=None))
    for n in ORDER:
        x, y = hex_center(HEX[n], x0, y0, r)
        for a, b in hex_edges(n, x, y, r - 0.6):
            s.add(L(a[0], a[1], b[0], b[1], CHAR, 1.6, extra=' stroke-linecap="round"'))
    x, y = hex_center(HEX["C1"], x0, y0, r)
    s.add(poly(hex_pts(x, y, r - 2.2), "none", RED, 2.6))
    # territory labels
    names = {"A": "Economic structure", "B": "Political inputs", "C": "Electoral competition",
             "D": "Governing institutions", "E": "Legitimacy", "TC": "Technology",
             "production": "Production", "household": "Households", "money": "Credit, trade, environment"}
    for a, nm in names.items():
        pts = [hex_center(HEX[n], x0, y0, r) for n in AREA_NODES[a]]
        mx = sum(p[0] for p in pts) / len(pts)
        top = min(p[1] for p in pts)
        bot = max(p[1] for p in pts)
        yy = top - r - 5 if a not in ("production", "household", "money", "D") else bot + r + 15
        s.add(T(mx, yy, nm, 13, CHAR, 600, "middle", fam="tight", halo=NEWS))
    xs = [hex_center(HEX[n], x0, y0, r) for n in AREA_NODES["X"]]
    for (x, y), n in zip(xs, AREA_NODES["X"]):
        pass
    # inset: area C
    ix, iy = 470, 64
    s.add(R(ix - 8, iy, 172, 324, fill=WHITE, stroke=STONE, sw=0.6))
    s.add(T(ix + 2, iy + 22, "Area C opened", 13, CHAR, 700))
    cn = AREA_NODES["C"]
    cs = [HEX[n] for n in cn]
    rr = 27
    cminx = min(hex_center(q, 0, 0, rr)[0] for q in cs)
    cmaxx = max(hex_center(q, 0, 0, rr)[0] for q in cs)
    cminy = min(hex_center(q, 0, 0, rr)[1] for q in cs)
    ox = ix + 78 - (cminx + cmaxx) / 2
    oy = iy + 70 - cminy
    cpos = {}
    for n in cn:
        x, y = hex_center(HEX[n], 0, 0, rr)
        x, y = x + ox, y + oy
        cpos[n] = (x, y)
        s.add(poly(hex_pts(x, y, rr - 1), NEWS, CHAR, 1.2))
        s.add(s.icon(n, "black", x - 13, y - 17, 26))
        s.add(T(x, y + 19, n, 13, CHAR, 600, "middle"))
    for l in LINKS.values():
        if l["from"] in cn and l["to"] in cn:
            p0, p1 = cpos[l["from"]], cpos[l["to"]]
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            cc = ((p0[0] + p1[0]) / 2 - dy * 0.18, (p0[1] + p1[1]) / 2 + dx * 0.18)
            a, q, b = qtrim(p0, cc, p1, 11, 11)
            col = VERD if l["loops"] == ["B4"] else PRU
            s.add(P(f"M{f1(a[0])} {f1(a[1])}Q{f1(q[0])} {f1(q[1])} {f1(b[0])} {f1(b[1])}", col, 2.0, l["evidence"]))
            s.add(AH(b[0], b[1], qtan(a, q, b, 1), 6, col))
    ky = iy + 70 + max(p[1] for p in cpos.values()) - min(p[1] for p in cpos.values()) + 48
    s.add(TL(ix + 2, ky, [f"{n} {label(n)}" if len(label(n)) < 20 else f"{n} {label(n)[:18].rstrip()}…" for n in cn], 13, 16, fill=CHAR))
    s.add(TL(ix + 2, ky + 90, ["R10 in Prussian,", "B4 in Verdigris"], 13, 16, fill=STONE))
    return s.render()


# ==========================================================================
# 5. KITCHEN TABLE
# ==========================================================================
KT_SECTORS = ["A", "household", "production", "money", "TC", "X", "B", "C", "D", "E"]


def kt_positions(cx, cy, r1, dr):
    tot = len(ORDER) - 1
    per = 2 * math.pi / (tot + len(KT_SECTORS) * 0.9)
    th = -math.pi / 2 - per * 3.5
    pos = {HOME: (cx, cy)}
    ang = {}
    for a in KT_SECTORS:
        ns = [n for n in AREA_NODES[a] if n != HOME]
        span = per * len(ns)
        a0 = th
        th += span + per * 0.9
        rings = defaultdict(list)
        for n in ns:
            rings[HOME_DIST[n]].append(n)
        for k, lst in rings.items():
            for i, n in enumerate(lst):
                t = a0 + span * (i + 0.5) / len(lst)
                ang[n] = t
                rr = r1 + dr * (k - 1)
                pos[n] = (cx + rr * math.cos(t), cy + rr * math.sin(t))
        ang[a] = (a0, a0 + span)
    return pos, ang


def kt_parent(n):
    k = HOME_DIST[n]
    cands = [l for l in OUT[n] if HOME_DIST.get(l["to"]) == k - 1]
    rank = {"documented": 0, "well-supported": 1, "plausible": 2, "plausible_contested": 3, "hypothesis": 4}
    cands.sort(key=lambda l: (0 if l["loops"] else 1, rank[l["evidence"]]))
    return cands[0]


def kt_thumb(lid, size=76):
    def draw(s):
        cx = cy = size / 2
        r1, dr = 6.5, 5.6
        pos, _ = kt_positions(cx, cy, r1, dr)
        for k in range(1, 7):
            s.add(C(cx, cy, r1 + dr * (k - 1), fill="none", stroke=STONE, w=0.4))
        s.add(C(cx, cy, 2.4, fill=CHAR, stroke=None))
        col = loop_color(lid)
        sts = loop_stations(lid)
        if is_sketch(lid):
            pts = []
            for i, st in enumerate(sts):
                if st["code"]:
                    pts.append(pos[st["code"]])
                else:
                    a = -math.pi / 2 + 2 * math.pi * i / len(sts)
                    pts.append((cx + 16 * math.cos(a), cy + 16 * math.sin(a)))
            s.add(draw_loop(lid, pts, col, 1.1, WHITE, arrows=False, bow=0.25))
            for p, st in zip(pts, sts):
                s.add(C(p[0], p[1], 1.8, fill=CHAR if st["code"] else WHITE, stroke=STONE if not st["code"] else None, w=0.9))
            return
        pts = [pos[st["code"]] for st in sts]
        s.add(draw_loop(lid, pts, col, 1.6, WHITE, ah=3.2, bow=0.22))
        for p in pts:
            s.add(C(p[0], p[1], 1.9, fill=CHAR, stroke=None))
    return thumb_svg(f"kt-{lid}", WHITE, draw, size)


def sketch_kitchen_table():
    s = Svg("s5", bg=WHITE, title="Kitchen Table sketch")
    header(s, "Every variable in the model reaches households' financial security within six steps.", width=84)
    cx, cy, r1, dr = 222, 226, 37, 27
    pos, ang = kt_positions(cx, cy, r1, dr)
    for k in range(1, 7):
        s.add(C(cx, cy, r1 + dr * (k - 1), fill="none", stroke=STONE, w=0.6))
    for a in KT_SECTORS:
        a0, a1 = ang[a]
        g = a0 - (2 * math.pi / 60) * 0.45
        rr0, rr1 = r1 - 10, r1 + dr * 5 + 8
        s.add(L(cx + rr0 * math.cos(g), cy + rr0 * math.sin(g), cx + rr1 * math.cos(g), cy + rr1 * math.sin(g), NEWS, 1.2))
    for n in ORDER:
        if n == HOME:
            continue
        l = kt_parent(n)
        p0, p1 = pos[n], pos[l["to"]]
        d = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        tr = 22 if l["to"] == HOME else 4.5
        ux, uy = (p1[0] - p0[0]) / d, (p1[1] - p0[1]) / d
        a = (p0[0] + ux * 4, p0[1] + uy * 4)
        b = (p1[0] - ux * tr, p1[1] - uy * tr)
        col = CHAR if l["loops"] else STONE
        s.add(L(a[0], a[1], b[0], b[1], col, 0.9, l["evidence"]))
        s.add(AH(b[0], b[1], math.atan2(uy, ux), 3.4, col))
    for lid in ("R5", "R10"):
        pts = [pos[st["code"]] for st in loop_stations(lid)]
        s.add(draw_loop(lid, pts, PRU, 2.0, WHITE, ah=5, bow=0.22))
    for n in ORDER:
        if n == HOME:
            continue
        x, y = pos[n]
        s.add(C(x, y, 3.4, fill=CHAR if LOOPCOUNT[n] else WHITE, stroke=CHAR, w=1))
    s.add(C(cx, cy, 21, fill=WHITE, stroke=RED, w=2.6), s.icon(HOME, "black", cx - 14, cy - 14, 28))
    for k in range(1, 7):
        s.add(T(cx + 3, cy - (r1 + dr * (k - 1)) + 4.5, str(k), 13, STONE, 600, "start", halo=WHITE))
    s.add(T(cx, 62, "steps to the household", 13, STONE, 500, "middle", halo=WHITE))
    short = {"A": "Economic structure", "household": "Households", "production": "Production",
             "money": "Credit and trade", "TC": "Technology", "X": "Outside drivers", "B": "Political inputs",
             "C": "Electoral competition", "D": "Governing institutions", "E": "Legitimacy"}
    for a in KT_SECTORS:
        a0, a1 = ang[a]
        m = (a0 + a1) / 2
        rr = r1 + dr * 5 + 16
        x, y = cx + rr * math.cos(m), cy + rr * math.sin(m)
        cs = math.cos(m)
        anchor = "start" if cs > 0.3 else "end" if cs < -0.3 else "middle"
        lines = wrap(short[a], 12)
        y += 4 - (len(lines) - 1) * 7 + (6 if math.sin(m) > 0.7 else 0) - (4 if math.sin(m) < -0.7 else 0)
        s.add(TL(x, y, lines, 13, 14, fill=CHAR, weight=600, anchor=anchor, fam="tight", halo=WHITE))
    s.add(L(cx + 18, cy + 14, 404, 372, CHAR, 0.7))
    s.add(TL(404, 368, ["Households' financial security", "Five reforms act on it directly"], 13, 15, fill=CHAR, weight=500, halo=WHITE))
    px = 478
    s.add(T(px, 96, "Loops by distance", 13, CHAR, 700))
    picks = ["R5", "R1", "R10", "R12", "R7", "B4"]
    for i, lid in enumerate(picks):
        gx, gy = px + (i % 2) * 74, 112 + (i // 2) * 82
        s.add(f'<g transform="translate({gx},{gy})">' + re.sub(r'^<svg[^>]*>|</svg>$', '', kt_thumb(lid, 64)) + "</g>")
        s.add(T(gx + 32, gy + 76, lid, 13, CHAR, 600, "middle"))
    return s.render()


# ==========================================================================
# 6. THE SPINE
# ==========================================================================
def spine_thumb(lid, size=76):
    def draw(s):
        y = size / 2
        x0, x1 = 5, size - 5
        sp = (x1 - x0) / (len(SPINE_ORDER) - 1)
        s.add(L(x0, y, x1, y, STONE, 0.8))
        col = loop_color(lid)
        if is_sketch(lid):
            s.add(band(f"M{size/2-14} {y-8}a14 8 0 1 1 28 0a14 8 0 1 1 -28 0", NEWS, 1.0))
            for st in loop_stations(lid):
                if st["code"]:
                    s.add(C(x0 + SPINE_IX[st["code"]] * sp, y, 2, fill=CHAR, stroke=None))
            return
        for st in loop_steps(lid):
            a, b = SPINE_IX[st["from"]], SPINE_IX[st["to"]]
            xa, xb = x0 + a * sp, x0 + b * sp
            rx = abs(xb - xa) / 2
            ry = min(rx, size / 2 - 6)
            s.add(P(f"M{f1(xa)} {f1(y)}A{f1(rx)} {f1(ry)} 0 0 1 {f1(xb)} {f1(y)}", col, 1.4, st["evidence"]))
        for st in loop_stations(lid):
            s.add(C(x0 + SPINE_IX[st["code"]] * sp, y, 1.8, fill=CHAR, stroke=None))
    return thumb_svg(f"sp-{lid}", NEWS, draw, size)


def sketch_spine():
    s = Svg("s6", bg=NEWS, title="Spine sketch")
    header(s, "Feedback lives below the line. Taxing inherited gains (R-28) acts on the red arc, which closes R1.", width=86)
    x0, x1, y = 24, 452, 226
    sp = (x1 - x0) / (len(SPINE_ORDER) - 1)
    yf, yb = y - 6, y + 22
    X = {n: x0 + i * sp for i, n in enumerate(SPINE_ORDER)}

    def arc(l, col, w):
        xa, xb = X[l["from"]], X[l["to"]]
        rx = abs(xb - xa) / 2
        if xb > xa:
            ry = min(rx, 146)
            return P(f"M{f1(xa)} {f1(yf)}A{f1(rx)} {f1(ry)} 0 0 1 {f1(xb)} {f1(yf)}", col, w, l["evidence"]), (xb, yf, math.pi / 2)
        ry = min(rx, 150)
        return P(f"M{f1(xa)} {f1(yb)}A{f1(rx)} {f1(ry)} 0 0 1 {f1(xb)} {f1(yb)}", col, w, l["evidence"]), (xb, yb, -math.pi / 2)

    for layer in (0, 1):
        for l in LINKS.values():
            inl = bool(l["loops"])
            if inl != bool(layer) or l["id"] == "L03":
                continue
            col = (VERD if all(LOOPS[x]["type"] == "B" for x in l["loops"]) else PRU) if inl else STONE
            d, (ex, ey, ea) = arc(l, col, 1.2 if inl else 0.6)
            s.add(d)
            if inl:
                s.add(AH(ex, ey, ea, 3.6, col))
    d, (ex, ey, ea) = arc(LINKS["L03"], RED, 2.4)
    s.add(d, AH(ex, ey, ea, 5.5, RED))
    s.add(R(x0 - 6, y - 1, x1 - x0 + 12, 18, fill=NEWS))
    s.add(L(x0, y - 4, x1, y - 4, CHAR, 1.2))
    for n in SPINE_ORDER:
        s.add(C(X[n], y - 4, 2.3, fill=CHAR if LOOPCOUNT[n] else WHITE, stroke=CHAR, w=0.9))
    segs = [("X", AREA_NODES["X"]), ("TC", AREA_NODES["TC"]),
            ("Economy layer", AREA_NODES["money"] + AREA_NODES["production"] + AREA_NODES["household"])] + \
           [(a, AREA_NODES[a]) for a in CORE_AREAS]
    for nm, ns in segs:
        xa, xb = X[ns[0]], X[ns[-1]]
        s.add(L(xa, y + 3, xb, y + 3, CHAR, 2.4))
        s.add(T((xa + xb) / 2, y + 15.5, nm, 13, CHAR, 600, "middle", fam="tight"))
    s.add(T(x0, 92, "forward", 13, STONE, 600))
    s.add(T(x0, 392, "back", 13, STONE, 600))
    mx = (X["E1"] + X["A1"]) / 2
    s.add(TL(mx + 18, 372, ["L03, Policy advantages add", "to wealth at the top"], 13, 15, fill=CHAR, weight=500, halo=NEWS))
    # phone
    fx, fy, fw, fh = 492, 78, 122, 262
    s.add(R(fx, fy, fw, fh, fill=WHITE, stroke=CHAR, sw=1.4, rx=16))
    s.add(R(fx + fw / 2 - 14, fy + 7, 28, 4, fill=CHAR, rx=2))
    vx, vy0, vy1 = fx + fw / 2, fy + 22, fy + fh - 14
    vs = (vy1 - vy0) / (len(SPINE_ORDER) - 1)
    Y = {n: vy0 + i * vs for i, n in enumerate(SPINE_ORDER)}
    for l in LINKS.values():
        ya, yb2 = Y[l["from"]], Y[l["to"]]
        ry = abs(yb2 - ya) / 2
        rx = min(ry, 52)
        inl = bool(l["loops"])
        col = RED if l["id"] == "L03" else (PRU if inl else STONE)
        sweep = 1 if yb2 > ya else 1
        s.add(P(f"M{f1(vx)} {f1(ya)}A{f1(rx)} {f1(ry)} 0 0 {1 if yb2 > ya else 1} {f1(vx)} {f1(yb2)}", col if l["id"] != "L03" else PRU, 0.9 if inl else 0.45, None))
    s.add(L(vx, vy0, vx, vy1, CHAR, 1))
    s.add(TL(fx - 4, fy + fh + 22, ["On a phone the line", "runs down the screen"], 13, 15, fill=CHAR))
    return s.render()


# ==========================================================================
# 7. FLYWHEELS AND GOVERNORS
# ==========================================================================
SHARED = [n for n in ORDER if LOOPCOUNT[n] >= 2]


def wheel_radius(lid, base=1.0):
    return base * {2: 15, 3: 19, 4: 23}[LOOPS[lid]["n"]]


def wheel_angles(lid, phi):
    steps = loop_steps(lid)
    ws = [DELAY_W.get(st["delay"], 1.5) if st["delay"] else 1.5 for st in steps]
    tot = sum(ws)
    angs, a = [], phi
    for w in ws:
        angs.append(a)
        a += 2 * math.pi * w / tot
    return angs


def draw_wheel(s, lid, cx, cy, r, phi, bg, red_step=None, lw=None, dot=2.3, label_icons=None):
    lp = LOOPS[lid]
    col = loop_color(lid)
    angs = wheel_angles(lid, phi)
    n = len(angs)
    gap = 0.16 if r > 20 else 0.2
    lw = lw or (3.0 if lp["type"] == "R" else 2.2)
    pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in angs]
    if lp["type"] == "B" and not lp["conceptual"]:
        top = (cx, cy - 0.55 * r)
        bl, br = (cx - 0.42 * r, cy + 0.06 * r), (cx + 0.42 * r, cy + 0.06 * r)
        sl = (cx, cy + 0.3 * r)
        s.add(L(cx, cy - 0.62 * r, cx, cy + 0.5 * r, CHAR, 0.9))
        for b in (bl, br):
            s.add(L(top[0], top[1], b[0], b[1], CHAR, 0.9), L(b[0], b[1], sl[0], sl[1], CHAR, 0.9))
            s.add(C(b[0], b[1], max(1.8, 0.14 * r), fill=VERD, stroke=None))
    elif not lp["conceptual"]:
        for p in pts:
            s.add(L(cx, cy, p[0], p[1], CHAR, 0.8))
        s.add(C(cx, cy, max(1.8, r * 0.1), fill=CHAR, stroke=None))
    for i, st in enumerate(loop_steps(lid)):
        a0 = angs[i] + gap
        a1 = (angs[(i + 1) % n] if i + 1 < n else angs[0] + 2 * math.pi) - gap
        large = 1 if (a1 - a0) > math.pi else 0
        d = (f"M{f1(cx + r * math.cos(a0))} {f1(cy + r * math.sin(a0))}"
             f"A{f1(r)} {f1(r)} 0 {large} 1 {f1(cx + r * math.cos(a1))} {f1(cy + r * math.sin(a1))}")
        if st["conceptual"]:
            s.add(band(d, bg, 1.2))
            continue
        c = RED if st["id"] == red_step else col
        s.add(P(d, c, lw + (0.6 if c == RED else 0), st["evidence"]))
        tip = a1
        s.add(AH(cx + r * math.cos(tip), cy + r * math.sin(tip), tip + math.pi / 2, max(3.4, lw * 1.5), c))
    for p, stn in zip(pts, loop_stations(lid)):
        if stn["code"]:
            s.add(C(p[0], p[1], dot, fill=CHAR, stroke=bg, w=0.8))
        else:
            s.add(C(p[0], p[1], dot, fill=bg, stroke=STONE, w=1))
    dirw = lp["direction"]
    ch = r * 0.28
    hx, hy = cx, cy - (0.0 if lp["type"] == "B" else 0)
    if lp["conceptual"]:
        s.add(C(cx, cy, max(2.2, r * 0.12), fill=bg, stroke=STONE, w=1))
    elif dirw == "running_up" and lp["type"] == "R":
        s.add(P(f"M{f1(cx - ch)} {f1(cy - r*0.18)}L{f1(cx)} {f1(cy - r*0.18 - ch)}L{f1(cx + ch)} {f1(cy - r*0.18)}", CHAR, 1.2))
    elif dirw == "running_down" and lp["type"] == "R":
        s.add(P(f"M{f1(cx - ch)} {f1(cy + r*0.18)}L{f1(cx)} {f1(cy + r*0.18 + ch)}L{f1(cx + ch)} {f1(cy + r*0.18)}", CHAR, 1.2))
    elif dirw == "disabled":
        s.add(L(cx - r * 0.55, cy + r * 0.62, cx + r * 0.55, cy + r * 0.62, CHAR, 2.2))
    return pts


def wheel_phi(lid, cx, cy, targets):
    best, bv = 0, 1e9
    sts = loop_stations(lid)
    for k in range(72):
        phi = 2 * math.pi * k / 72
        angs = wheel_angles(lid, phi)
        v = 0
        for a, st in zip(angs, sts):
            if st["code"] in targets:
                tx, ty = targets[st["code"]]
                want = math.atan2(ty - cy, tx - cx)
                dd = (a - want + math.pi) % (2 * math.pi) - math.pi
                v += dd * dd
        if v < bv:
            bv, best = v, phi
    return best


def fly_layout():
    groups = {}
    for g in M["groups"]:
        for lid in g["loops"]:
            groups[lid] = g["id"]
    GA = {"A": (95, 175), "B": (230, 115), "C": (370, 150), "D": (255, 320), "SK": (420, 350)}
    ids = list(LOOP_ORDER) + ["p:" + n for n in SHARED]
    anchors = {lid: (*GA[groups[lid]], 1.0) for lid in LOOP_ORDER}
    anchors["R8"] = (60, 330, 3.0)
    anchors["B2"] = (390, 360, 3.0)
    anchors["B3"] = (440, 300, 3.0)
    edges = []
    for lid in LOOP_ORDER:
        for st in loop_stations(lid):
            if st["code"] in SHARED:
                edges.append((lid, "p:" + st["code"], 1.0))
    radii = {lid: wheel_radius(lid) + 4 for lid in LOOP_ORDER}
    radii.update({"p:" + n: 6 for n in SHARED})
    return force_layout(ids, edges, anchors, (22, 70, 458, 392), iters=900, seed=4, kscale=0.55,
                        grav=0.03, radii=radii, edge_k=1.4)


FLY = fly_layout()


def fly_thumb(lid, size=76):
    def draw(s):
        draw_wheel(s, lid, size / 2, size / 2, 27, -math.pi / 2, NEWS, lw=3.0 if LOOPS[lid]["type"] == "R" else 2.4, dot=2.4)
    return thumb_svg(f"fw-{lid}", NEWS, draw, size)


def sketch_flywheels():
    s = Svg("s7", bg=NEWS, title="Flywheels and Governors sketch")
    header(s, "One governor is switched off. R-08 and R-15 act on its step from oversight back to policy favoritism.", width=86)
    pins = {n: FLY["p:" + n] for n in SHARED}
    phis = {}
    for lid in LOOP_ORDER:
        cx, cy = FLY[lid]
        targets = {st["code"]: pins[st["code"]] for st in loop_stations(lid) if st["code"] in pins}
        phis[lid] = wheel_phi(lid, cx, cy, targets)
    # rods first
    stpts = {}
    for lid in LOOP_ORDER:
        cx, cy = FLY[lid]
        r = wheel_radius(lid)
        angs = wheel_angles(lid, phis[lid])
        for a, st in zip(angs, loop_stations(lid)):
            if st["code"] in pins:
                px, py = pins[st["code"]]
                s.add(L(cx + r * math.cos(a), cy + r * math.sin(a), px, py, STONE, 1.0))
    for lid in LOOP_ORDER:
        cx, cy = FLY[lid]
        draw_wheel(s, lid, cx, cy, wheel_radius(lid), phis[lid], NEWS, red_step="L16")
    for n, (px, py) in pins.items():
        big = LOOPCOUNT[n] >= 3
        sz = 10 if big else 7
        s.add(R(px - sz / 2, py - sz / 2, sz, sz, fill=CHAR))
    for n, (px, py) in pins.items():
        if LOOPCOUNT[n] >= 3:
            s.add(T(px + 8, py - 6, n, 13, CHAR, 700, halo=NEWS))
    for lid in LOOP_ORDER:
        cx, cy = FLY[lid]
        r = wheel_radius(lid)
        s.add(T(cx, cy + r + 14, lid, 13, STONE if is_sketch(lid) else CHAR, 600, "middle", halo=NEWS))
    # inset
    px = 470
    s.add(R(px - 6, 66, 176, 322, fill=WHITE, stroke=STONE, sw=0.6))
    s.add(T(px + 4, 88, "R10, a four-spoke flywheel", 13, CHAR, 700))
    wx, wy, wr = 552, 186, 50
    pts = draw_wheel(s, "R10", wx, wy, wr, -math.pi / 2, WHITE, lw=4, dot=3.2)
    for p, st in zip(pts, loop_stations("R10")):
        ang = math.atan2(p[1] - wy, p[0] - wx)
        ix, iy = wx + (wr + 20) * math.cos(ang), wy + (wr + 20) * math.sin(ang)
        s.add(s.icon(st["code"], "black", ix - 11, iy - 11, 22))
    s.add(TL(px + 4, 282, ["Arcs sized by delay:", "S, S, M, M", "Dashed arc: C3 to C4,", "plausible"], 13, 16, fill=CHAR))
    # legend
    lx, ly = px + 22, 362
    tmp = Svg("x")
    draw_wheel(s, "R13", lx, ly, 12, -math.pi / 2, WHITE, lw=2.2, dot=1.8)
    s.add(T(lx + 18, ly + 4.5, "feeds itself", 13, CHAR))
    draw_wheel(s, "B5", lx + 102, ly, 12, -math.pi / 2, WHITE, lw=2, dot=1.8)
    s.add(T(lx + 118, ly - 6, "pushes", 13, CHAR), T(lx + 118, ly + 9, "back", 13, CHAR))
    return s.render()


# ==========================================================================
# 8. CROSSROADS
# ==========================================================================
def cross_anchor():
    anchor = {}
    for lid in LOOP_ORDER:
        codes = [st["code"] for st in loop_stations(lid) if st["code"]]
        if not codes:
            anchor[lid] = None
            continue
        anchor[lid] = max(codes, key=lambda c: (LOOPCOUNT[c], -ORDER.index(c)))
    return anchor


CROSS_ANCHOR = cross_anchor()


def petal_geom(lid):
    steps = loop_steps(lid)
    tot = sum(DELAY_W.get(st["delay"], 2) if st["delay"] else 2 for st in steps)
    return 30 + 7.6 * tot, 8 + 4.2 * LOOPS[lid]["n"]


def petal_path_pts(L_, W_, hx, hy, ang, samples=90):
    def tr(x, y):
        return (hx + x * math.cos(ang) - y * math.sin(ang), hy + x * math.sin(ang) + y * math.cos(ang))
    up = [cpt((0, 0), (0.18 * L_, 1.05 * W_), (L_, 0.85 * W_), (L_, 0), i / samples) for i in range(samples + 1)]
    dn = [cpt((L_, 0), (L_, -0.85 * W_), (0.18 * L_, -1.05 * W_), (0, 0), i / samples) for i in range(1, samples + 1)]
    return [tr(x, y) for x, y in up + dn]


def rotate_to_hub(lid, hub):
    sts = loop_stations(lid)
    steps = loop_steps(lid)
    if hub is None:
        return sts, steps
    k = next(i for i, st in enumerate(sts) if st["code"] == hub)
    return sts[k:] + sts[:k], steps[k:] + steps[:k]


def draw_petal(s, lid, hx, hy, ang, scale, bg, ink=WHITE, w=1.3, labels=False, hub_r=0):
    hub = CROSS_ANCHOR[lid]
    L_, W_ = petal_geom(lid)
    L_, W_ = L_ * scale, W_ * scale
    pts = petal_path_pts(L_, W_, hx, hy, ang)
    lp = LOOPS[lid]
    if lp["type"] == "B" and not lp["conceptual"]:
        s.add(poly(pts, VERD))
    sts, steps = rotate_to_hub(lid, hub)
    n = len(steps)
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = cum[-1]
    idx = []
    for k in range(n + 1):
        target = tot * k / n
        idx.append(min(range(len(cum)), key=lambda i: abs(cum[i] - target)))
    spots = []
    for k, st in enumerate(steps):
        i0, i1 = idx[k], idx[k + 1]
        seg = pts[i0:i1 + 1]
        d = "M" + "L".join(f"{f1(x)} {f1(y)}" for x, y in seg)
        if st["conceptual"]:
            s.add(band(d, bg, 1.1, color=NEWS if bg == PRU else STONE))
        else:
            s.add(P(d, ink, w, st["evidence"]))
            m = seg[int(len(seg) * 0.55)]
            m2 = seg[min(len(seg) - 1, int(len(seg) * 0.55) + 2)]
            s.add(AH(m2[0], m2[1], math.atan2(m2[1] - m[1], m2[0] - m[0]), 3.6 * max(1, scale), ink))
        spots.append(pts[i0])
    for k, st in enumerate(sts):
        if k == 0 and hub:
            continue
        x, y = spots[k]
        if st["code"]:
            s.add(C(x, y, 2.4 * max(0.8, scale), fill=ink, stroke=bg, w=0.8))
        else:
            s.add(C(x, y, 2.2, fill=bg, stroke=ink, w=1))
    tip = (hx + L_ * math.cos(ang), hy + L_ * math.sin(ang))
    return spots, sts, tip


def cross_thumb(lid, size=76):
    def draw(s):
        hub = CROSS_ANCHOR[lid]
        L_, W_ = petal_geom(lid)
        sc = min(1.0, (size - 18) / (L_ + 4))
        ang = -math.pi / 4
        hx, hy = 13, size - 13
        draw_petal(s, lid, hx, hy, ang, sc, PRU, w=1.3)
        if hub:
            s.add(C(hx, hy, 8, fill=NEWS, stroke=None), s.icon(hub, "black", hx - 6, hy - 6, 12))
        else:
            s.add(C(hx, hy, 3, fill=PRU, stroke=NEWS, w=1))
    return thumb_svg(f"cr-{lid}", PRU, draw, size)


def sketch_crossroads():
    s = Svg("s8", bg=PRU, title="Crossroads sketch")
    header(s, "Seven loops grow from policy tilt to insiders.", dark=True)
    hubs = {"E1": (178, 236), "C4": (420, 160), "C3": (408, 318), "D2": (548, 268),
            "B1": (300, 100), "B4": (288, 362), "D5": (566, 120), "A5": (56, 352), "E2": (596, 368)}
    by_hub = defaultdict(list)
    for lid in LOOP_ORDER:
        by_hub[CROSS_ANCHOR[lid]].append(lid)
    start = {"E1": -2.5, "C4": -2.2, "C3": 0.2, "D2": -0.9, "B1": 0.25, "B4": -0.3, "D5": 0.6, "A5": -1.1, "E2": -2.2}
    spread = {"C4": 2 * math.pi, "C3": 2 * math.pi * 0.62, "D2": 1.6}
    scale = {"E1": 0.95, "C4": 0.72, "C3": 0.8, "D2": 0.9}
    for hub, lids in by_hub.items():
        if hub is None:
            continue
        hx, hy = hubs[hub]
        k = len(lids)
        sp = spread.get(hub, 2 * math.pi)
        for i, lid in enumerate(lids):
            a = start[hub] + (sp * i / k if sp >= 2 * math.pi - 0.01 else (sp * i / max(1, k - 1)))
            draw_petal(s, lid, hx, hy, a, scale.get(hub, 0.75), PRU)
            L_, _ = petal_geom(lid)
            sc = scale.get(hub, 0.75)
            tx, ty = hx + (L_ * sc + 12) * math.cos(a), hy + (L_ * sc + 12) * math.sin(a)
            s.add(T(tx, ty + 4.5, lid, 13, NEWS, 600, "middle", halo=PRU))
    # seeds
    for i, lid in enumerate(["B2", "B3"]):
        sx, sy = 486 + i * 52, 60 + 8
        draw_petal(s, lid, sx, sy + 26, -math.pi / 2 + 0.5, 0.5, PRU)
        s.add(C(sx, sy + 26, 3, fill=PRU, stroke=NEWS, w=1))
        s.add(T(sx + 16, sy + 40, lid, 13, NEWS, 600, "middle", halo=PRU))
    # thread between the two C3 appearances (C3 on the R10 petal and the C3 hub)
    lids = by_hub["C4"]
    for hub, (hx, hy) in hubs.items():
        r = 14 if hub == "E1" else 11
        s.add(C(hx, hy, r, fill=NEWS, stroke=None), s.icon(hub, "black", hx - r * 0.72, hy - r * 0.72, r * 1.44))
    names = {"E1": "Policy tilt to insiders · 7", "C4": "Incumbent control of election rules · 4",
             "C3": "Electoral pressure · 3", "D2": "Executive unilateralism · 2"}
    pos = {"E1": (178, 268, "middle"), "C4": (420, 196, "middle"), "C3": (408, 350, "middle"), "D2": (548, 304, "middle")}
    for h, nm in names.items():
        x, y, an = pos[h]
        s.add(TL(x, y, wrap(nm, 22), 13, 15, fill=WHITE, weight=600, anchor=an, halo=PRU))
    # no-loop margin
    nl = [n for n in ORDER if LOOPCOUNT[n] == 0]
    # tag
    tx, ty = 16, 48
    s.add(L(tx + 150, ty + 52, 172, 222, NEWS, 0.9))
    s.add(R(tx, ty, 186, 58, fill=NEWS, rx=2))
    s.add(R(tx, ty, 6, 58, fill=RED))
    s.add(TL(tx + 14, ty + 20, ["Policy tilt to insiders", "R-09 and R-27 act here"], 13, 16, fill=CHAR, weight=500))
    s.add(T(tx + 14, ty + 52, "", 13, CHAR))
    return s.render()


# ==========================================================================
# 9. OPEN ATLAS
# ==========================================================================
def atlas_positions():
    P_ = {}
    # left page (economy): x 28..300
    grid = {
        "A1": (268, 132), "A2": (268, 188), "A3": (222, 160), "A6": (222, 246), "A4": (268, 300), "A5": (222, 330),
        "EC1": (150, 132), "EC2": (96, 132), "EC3": (176, 182), "EC4": (176, 236),
        "EC6": (176, 300), "EC7": (124, 286), "EC8": (124, 236), "EC9": (150, 346),
        "EC5": (62, 236), "EC10": (62, 300), "EC11": (88, 346), "EC12": (52, 182),
        "B1": (372, 132), "B2": (424, 120), "B3": (372, 196), "B4": (424, 180), "B5": (372, 252), "B6": (470, 140),
        "E1": (372, 318), "E2": (436, 346),
        "C1": (536, 120), "C2": (588, 132), "C3": (520, 178), "C4": (580, 192), "C5": (514, 234),
        "D1": (438, 252), "D2": (488, 286), "D3": (566, 252), "D4": (500, 340), "D5": (446, 300), "D6": (556, 318), "D7": (590, 352),
    }
    P_.update(grid)
    for i, n in enumerate(AREA_NODES["TC"]):
        P_[n] = (320, 128 + i * 30)
    xs = {"X1": (300, 50), "X3": (196, 50), "X2": (548, 50), "X4": (450, 50), "X5": (378, 50)}
    P_.update(xs)
    return P_


ATLAS = atlas_positions()


def atlas_thumb(lid, size=76):
    def draw(s):
        k = (size - 8) / 600
        ox, oy = 4 - 16 * k, (size - 330 * k) / 2 - 60 * k
        s.add(R(ox + 28 * k, oy + 64 * k, 272 * k, 320 * k, fill=WHITE, stroke=STONE, sw=0.5))
        s.add(R(ox + 340 * k, oy + 64 * k, 272 * k, 320 * k, fill=WHITE, stroke=STONE, sw=0.5))
        col = loop_color(lid)
        if is_sketch(lid):
            s.add(band(f"M{size*0.7:.1f} {size/2:.1f}a7 7 0 1 1 0.1 0", WHITE, 0.9))
            return
        pts = [(ox + ATLAS[st["code"]][0] * k, oy + ATLAS[st["code"]][1] * k) for st in loop_stations(lid)]
        s.add(draw_loop(lid, pts, col, 1.5, WHITE, ah=3, bow=0.22))
        for p in pts:
            s.add(C(p[0], p[1], 1.8, fill=CHAR, stroke=None))
    return thumb_svg(f"oa-{lid}", NEWS, draw, size)


def sketch_open_atlas():
    s = Svg("s9", bg=NEWS, title="Open Atlas sketch")
    header(s, "Twelve connections cross the fold between the economy and democracy pages.", width=90)
    s.add(R(28, 64, 272, 320, fill=WHITE, stroke=STONE, sw=0.7), R(340, 64, 272, 320, fill=WHITE, stroke=STONE, sw=0.7))
    s.add(L(320, 64, 320, 384, STONE, 0.6))
    s.add(T(40, 88, "Economy", 17, CHAR, 700, fam="tight"), T(352, 88, "Democracy", 17, CHAR, 700, fam="tight"))
    s.add(T(40, 106, "A and the economy layer · 18", 13, STONE), T(352, 106, "B, C, D and E · 20", 13, STONE))
    cross_loops = {"R1", "R5", "R6", "R15"}
    cross_ids = {l["id"] for l in CROSSINGS}

    def curve(a, b):
        (x0, y0), (x1, y1) = ATLAS[a], ATLAS[b]
        if abs(x1 - x0) > 60:
            return f"M{x0} {y0}C{(x0 + x1) / 2:.1f} {y0} {(x0 + x1) / 2:.1f} {y1} {x1} {y1}", math.atan2(0, x1 - x0)
        dx, dy = x1 - x0, y1 - y0
        c = ((x0 + x1) / 2 - dy * 0.15, (y0 + y1) / 2 + dx * 0.15)
        return f"M{x0} {y0}Q{c[0]:.1f} {c[1]:.1f} {x1} {y1}", qtan((x0, y0), c, (x1, y1), 1)

    order = sorted(LINKS.values(), key=lambda l: (l["id"] in cross_ids, bool(set(l["loops"]) & cross_loops), l["id"] == "L31"))
    for l in order:
        d, ang = curve(l["from"], l["to"])
        if l["id"] == "L31":
            s.add(P(d, RED, 2.4, l["evidence"]))
        elif set(l["loops"]) & cross_loops:
            s.add(P(d, PRU, 1.6, l["evidence"]))
        elif l["id"] in cross_ids:
            s.add(P(d, CHAR, 1.4, l["evidence"]))
        else:
            s.add(P(d, STONE, 0.55, l["evidence"]))
    for n in ORDER:
        x, y = ATLAS[n]
        if AREA_OF[n] == "X":
            s.add(R(x - 5, y - 5, 10, 10, fill=NEWS, stroke=CHAR, sw=1))
            s.add(T(x + 8, y + 4.5, n, 13, CHAR, 500, halo=NEWS))
        elif AREA_OF[n] == "TC":
            s.add(C(x, y, 9, fill=NEWS, stroke=CHAR, w=0.9), s.icon(n, "black", x - 7, y - 7, 14))
        else:
            s.add(C(x, y, 9.5, fill=WHITE, stroke=None), s.icon(n, "black", x - 9, y - 9, 18))
    lab = {"E1": (372, 344, "middle"), "A2": (290, 214, "end"), "A1": (290, 116, "end"), "A4": (290, 326, "end"),
           "B1": (372, 116, "middle"), "B5": (352, 272, "start")}
    for n, (x, y, an) in lab.items():
        s.add(T(x, y, n, 13, CHAR, 700, an, halo=WHITE))
    s.add(T(320, 396, "Technology in the fold", 13, CHAR, 600, "middle", halo=NEWS))
    s.add(TL(36, 376, ["L31 in red: insider-tilted labor rules", "weaken worker bargaining · R-21 acts here"], 13, 15, fill=CHAR, weight=500, halo=WHITE))
    return s.render()


# ==========================================================================
# 10. TABLETOP MODEL
# ==========================================================================
COS30 = math.cos(math.radians(30))


def table_plan():
    plan = {}
    spec = [("TC", 0, 0, 4), ("B", 5, 0, 3), ("C", 9.4, 0, 3), ("A", 0, 3.4, 3), ("E", 5, 3.4, 2),
            ("D", 8.4, 3.4, 4), ("X", 5.2, 6.8, 5)]
    plinths = []
    for a, gx, gy, cols in spec:
        ns = AREA_NODES[a]
        rows = math.ceil(len(ns) / cols)
        plinths.append((a, gx, gy, cols, rows))
        for i, n in enumerate(ns):
            plan[n] = (gx + 0.5 + i % cols, gy + 0.5 + i // cols)
    ec = AREA_NODES["production"] + AREA_NODES["household"] + AREA_NODES["money"]
    plinths.append(("EC", 0, 6.8, 4, 3))
    for i, n in enumerate(ec):
        plan[n] = (0.5 + i % 4, 6.8 + 0.5 + i // 4)
    return plan, plinths


TPLAN, TPLINTHS = table_plan()


def iso(gx, gy, h, ox, oy, s_):
    return (ox + (gx - gy) * COS30 * s_, oy + (gx + gy) * 0.5 * s_ - h * s_)


def block_h(n):
    return 0.28 + 0.42 * LOOPCOUNT[n]


def draw_block(svg, gx, gy, h, ox, oy, s_, half=0.36, top=WHITE, key=None, base=0.0):
    p = lambda x, y, z: iso(x, y, z, ox, oy, s_)
    a, b, c, d = (gx - half, gy - half), (gx + half, gy - half), (gx + half, gy + half), (gx - half, gy + half)
    zt = base + h
    svg.add(poly([p(*d, base), p(*c, base), p(*c, zt), p(*d, zt)], NEWS, CHAR, 0.6))
    svg.add(poly([p(*b, base), p(*c, base), p(*c, zt), p(*b, zt)], STONE, CHAR, 0.6))
    svg.add(poly([p(*a, zt), p(*b, zt), p(*c, zt), p(*d, zt)], top, CHAR, 0.6))
    if key:
        k = 2 * half * 0.78 / 128
        x0, y0 = gx - half * 0.78, gy - half * 0.78
        ex, ey = p(x0, y0, zt)
        m = (k * COS30 * s_, k * 0.5 * s_, -k * COS30 * s_, k * 0.5 * s_, ex, ey)
        svg.add(svg.icon_matrix(key, "black", m))


def table_scene(svg, ox, oy, s_, only=None, red=None, icons=True, arcs_for=None, lw=1.4, plinths=True):
    if plinths:
        for a, gx, gy, cols, rows in sorted(TPLINTHS, key=lambda t: t[1] + t[2]):
            if only is not None:
                continue
            p = lambda x, y, z: iso(x, y, z, ox, oy, s_)
            x0, y0, x1, y1 = gx, gy, gx + cols, gy + rows
            h = 0.22
            svg.add(poly([p(x0, y1, 0), p(x1, y1, 0), p(x1, y1, h), p(x0, y1, h)], NEWS, CHAR, 0.6))
            svg.add(poly([p(x1, y0, 0), p(x1, y1, 0), p(x1, y1, h), p(x1, y0, h)], STONE, CHAR, 0.6))
            svg.add(poly([p(x0, y0, h), p(x1, y0, h), p(x1, y1, h), p(x0, y1, h)], NEWS, CHAR, 0.6))
    nodes = [n for n in ORDER if only is None or n in only]
    for n in sorted(nodes, key=lambda n: TPLAN[n][0] + TPLAN[n][1]):
        gx, gy = TPLAN[n]
        draw_block(svg, gx, gy, block_h(n), ox, oy, s_, top=RED if n == red else WHITE,
                   key=n if icons else None, base=0.22 if only is None else 0)


def table_arcs(svg, lid, ox, oy, s_, base, lw=1.4, ah=4):
    col = loop_color(lid)
    for st in loop_steps(lid):
        a, b = st["from"], st["to"]
        pa = iso(*TPLAN[a], base + block_h(a), ox, oy, s_)
        pb = iso(*TPLAN[b], base + block_h(b), ox, oy, s_)
        d = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
        c = ((pa[0] + pb[0]) / 2, min(pa[1], pb[1]) - 10 - 0.25 * d)
        svg.add(P(f"M{f1(pa[0])} {f1(pa[1])}Q{f1(c[0])} {f1(c[1])} {f1(pb[0])} {f1(pb[1])}", col, lw, st["evidence"]))
        (mx, my), ang = qpt(pa, c, pb, 0.6), qtan(pa, c, pb, 0.6)
        svg.add(AH(mx, my, ang, ah, col))


def table_thumb(lid, size=76):
    def draw(s):
        if is_sketch(lid):
            s.add(band(f"M{size/2-16} {size/2+6}a16 9 0 1 1 32 0a16 9 0 1 1 -32 0", WHITE, 1.0))
            for st in loop_stations(lid):
                if st["code"]:
                    gx, gy = TPLAN[st["code"]]
                    draw_block(s, 0, 0, block_h(st["code"]), size / 2, size / 2 + 6, 11, top=WHITE)
            return
        codes = [st["code"] for st in loop_stations(lid)]
        xs = [TPLAN[c][0] - TPLAN[c][1] for c in codes]
        ys = [TPLAN[c][0] + TPLAN[c][1] for c in codes]
        sp = max(max(xs) - min(xs), (max(ys) - min(ys)) * 0.6, 2.5)
        s_ = min(13, (size - 26) / (sp * COS30 + 1))
        cxp = (max(xs) + min(xs)) / 2 * COS30 * s_
        cyp = (max(ys) + min(ys)) / 2 * 0.5 * s_
        ox, oy = size / 2 - cxp, size / 2 + 16 - cyp
        for n in sorted(codes, key=lambda n: TPLAN[n][0] + TPLAN[n][1]):
            gx, gy = TPLAN[n]
            draw_block(s, gx, gy, block_h(n), ox, oy, s_, half=0.4)
        table_arcs(s, lid, ox, oy, s_, 0, lw=1.3, ah=3)
    return thumb_svg(f"tb-{lid}", WHITE, draw, size)


def sketch_tabletop():
    s = Svg("s10", bg=WHITE, title="Tabletop Model sketch")
    header(s, "Feedback piles up on a few variables. Electoral pressure sits in four loops, and three reforms aim at it.", width=86)
    ox, oy, s_ = 218, 104, 19.5
    table_scene(s, ox, oy, s_, red="C3")
    for lid in LOOP_ORDER:
        if not is_sketch(lid):
            table_arcs(s, lid, ox, oy, s_, 0.22, lw=1.1, ah=3.4)
    labels = {"TC": "Technology", "B": "Political inputs", "C": "Electoral competition", "A": "Economic structure",
              "E": "Legitimacy", "D": "Governing institutions", "X": "Outside drivers", "EC": "Economy layer"}
    for a, gx, gy, cols, rows in TPLINTHS:
        x, y = iso(gx, gy + rows, 0, ox, oy, s_)
        s.add(T(x - 4, y + 14, labels[a], 13, CHAR, 600, "end", fam="tight", halo=WHITE))
    x, y = iso(*TPLAN["E1"], 0.22 + block_h("E1"), ox, oy, s_)
    s.add(L(x, y - 4, x, 70, CHAR, 0.7), T(x + 4, 72, "Policy tilt to insiders · 7 loops", 13, CHAR, 500, halo=WHITE))
    x, y = iso(*TPLAN["C3"], 0.22 + block_h("C3"), ox, oy, s_)
    s.add(L(x, y - 6, x + 30, y - 40, CHAR, 0.7), TL(x + 32, y - 52, ["Electoral pressure · 4 loops", "R-02, R-07, R-47 act here"], 13, 15, fill=CHAR, weight=500, halo=WHITE))
    # scale
    px = 520
    s.add(T(px, 240, "Block height", 13, CHAR, 700), T(px, 256, "= loops through it", 13, CHAR))
    for i, k in enumerate([0, 1, 2, 4, 7]):
        h = 0.28 + 0.42 * k
        bx = 0.6 + i * 1.25
        draw_block(s, bx, 0, h, px - 4, 340, 14, half=0.34)
        xx, yy = iso(bx, 0, 0, px - 4, 340, 14)
        s.add(T(xx + 1, yy + 22, str(k), 13, CHAR, 600, "middle"))
    return s.render()


# ==========================================================================
# Directions: the prose (one source for the board and the handoff)
# ==========================================================================
F = FACTS
DIRECTIONS = [
    {
        "key": "great-circle", "name": "Great Circle", "ground_name": "Newsprint",
        "sketch": sketch_great_circle, "thumb": gc_thumb, "thumb_bg": NEWS,
        "line": "The five core areas drawn as one ring, because influence in the model travels around a circle.",
        "idea": (
            f"Take the connections between neighboring core areas in the order A, B, C, D, E and back to A. "
            f"{F['forward']} of them run forward around that circle and {F['backward']} run back. In the model, money "
            "and organized interests bear on elections, and elections decide who governs. What government does then "
            "shapes whose interests policy favors, and that tilt feeds back into who holds wealth. A ring shows this "
            "circle before the reader learns a single variable name. Each of the 26 core variables gets a fixed place "
            "on the rim, each connection between them becomes a chord, and each loop becomes a closed shape inside the ring."),
        "overview": (
            f"The ring carries areas A to E as five labeled arcs. Inside it run the {F['core_chords']} connections among "
            f"those 26 variables. The {F['core_chords_loop']} that belong to a loop draw in Prussian, or Verdigris for "
            f"balancing loops, and the other {F['core_chords'] - F['core_chords_loop']} draw in thin Stone. The five outside "
            "drivers sit beyond the rim with short arrows to the variables they push. The economy layer (12 variables) and "
            "the technology group (8) appear as two closed discs outside the ring, each with a count and a bundle of lines, "
            "and a tap opens either one as a ring of its own. The overview leaves out names, signs and delays until the "
            "pointer rests on something. Readers click the arcs. They are the five largest shapes on the screen, they "
            "carry the area titles in display type, and they thicken under the pointer."),
        "closeups": (
            "Clicking C turns the ring until C sits at the top and widens its arc to half the circle. Its five variables "
            "get icons and labels. Eight connections arrive from other areas and seven leave, and they enter and exit as "
            "chords from the faded rest of the ring. R10 is the four-sided shape inside the arc. Three of its chords are "
            "solid, because C1 to C2 and C4 to C1 are documented and C2 to C3 is well supported. The fourth, C3 to C4, is "
            "the weakest step, graded plausible, and draws dashed. The R10 page draws the same shape at full size, sets "
            "each step's sentence along its chord and puts the delay outside the rim: under two years for the first two "
            "steps, 2 to 10 years for the last two."),
        "thumbs": (
            "Each thumbnail is the ring in miniature with one loop drawn on it. Variables never move, so the data sets "
            "the shape. R8 is a pair of chords inside area A. R10 is a small four-sided figure inside C, and R12 is a "
            "long kite from the courts in D to safe seats in C. R1 is a triangle spanning A, B and E. Balancing loops "
            "draw in Verdigris and reinforcing loops in Prussian. The three sketched loops have no numbered chain, so "
            "they appear as a hollow band near the center with open points. On the all-loops page the 23 rings sit in a "
            "grid, and a reader tells them apart by where the shape sits on the rim and how far across it reaches."),
        "ground": (
            "Newsprint ground, Charcoal rim, Prussian and Verdigris loop chords, Stone for everything else. The one red "
            "marks a chord. On the overview it marks L42, \"Incumbent-drawn maps create safe seats\", the only "
            "connection inside three loops (R4a, R10, R12) and the place where R-03 and R-04 act."),
        "risks": (
            f"A chord diagram turns into a hairball fast. With {F['core_chords']} chords, the ones outside loops have to "
            "stay faint until a reader asks for them. Order on the rim follows the areas, so neighbors on the rim can look "
            "related when no connection joins them. The two discs hide 20 variables behind a tap, and readers may take "
            "them as minor. On a phone the ring fits at about 340 pixels across. Arcs and loop shapes survive at that "
            "size; names move to a list under the ring."),
        "why": "It shows the circle the core areas form in one shape, and every loop thumbnail is a true miniature of the map.",
    },
    {
        "key": "star-atlas", "name": "Star Atlas", "ground_name": "Charcoal",
        "sketch": sketch_star_atlas, "thumb": star_thumb, "thumb_bg": CHAR,
        "line": "Variables as stars and loops as named constellations, on a dark sky divided into regions.",
        "idea": (
            "Printed star atlases taught the public to find order in a crowded sky by drawing figures between stars "
            "and naming them. This model poses the same problem, with 51 variables and 118 connections, and 23 patterns "
            "that matter most. Each variable becomes a star whose size follows its number of connections, so policy "
            f"tilt to insiders, with {F['e1_deg']}, shines brightest. The sky splits into regions, one per area, with "
            "straight stepped borders like the ones astronomers draw. Each loop becomes a constellation with its title. "
            "A first-time reader can learn one figure and find it again on the next visit."),
        "overview": (
            "The whole sky shows on one screen with its stars, regions and 23 figures. Star positions come from a layout "
            "that pulls connected variables together and keeps each area in its region. Figure lines draw only for loop "
            "steps. The 72 connections that belong to no loop stay hidden until the reader picks a star. Region names run "
            "in small capitals inside each region. The reader clicks a figure or a region: figures brighten under the "
            "pointer and show their title, and region names act as targets."),
        "closeups": (
            "Clicking Electoral competition zooms the sky to that region. Its five stars grow and take icons and labels. "
            "Connections that leave the region run off as lines toward faint neighboring stars, labeled with where they "
            "go. R10 is the four-star figure of safe seats, primary decisiveness, electoral pressure and incumbent control "
            "of election rules. The line from electoral pressure to incumbent control is dashed because that step is "
            "plausible, and the other three are solid. On the R10 page the figure stands alone at full size with each line "
            "captioned by its sentence, and the faint stars around it keep its place in the sky."),
        "thumbs": (
            "Each thumbnail crops the sky to one figure and scales it to fit. Positions are real, so the shapes differ. "
            "R13 and R18 are slim lenses inside the governing region, R12 is a long four-star figure from the courts "
            "across to safe seats, and R6 bends through three regions. Star sizes carry over, so any loop through policy "
            "tilt to insiders has one bright star in it. The three sketched loops have no stars to stand on and appear as "
            "hollow rings with open points."),
        "ground": (
            "Charcoal ground, Newsprint stars, White lines for reinforcing figures, Verdigris for balancing ones, Stone "
            "for region borders and for stars outside every loop. The one red is a star. In the sketch it is C2, primary "
            "decisiveness, where R-01, all-party primaries, acts."),
        "risks": (
            "Star positions come from an algorithm, so distance on the sky means little, and readers trained by real maps "
            "will read meaning into it. Hiding the 72 non-loop connections makes the system look simpler than the model "
            "says. Some figures share stars, and R4a and R12 overlap on three of them, so the overview must light one "
            "figure at a time. A phone can show the whole sky as a picture, but picking a single star needs a zoom step first."),
        "why": "The most beautiful of the ten, and the loop page becomes a page of distinct, named figures.",
    },
    {
        "key": "ledger-grid", "name": "Ledger Grid", "ground_name": "White",
        "sketch": sketch_ledger, "thumb": ledger_thumb, "thumb_bg": WHITE,
        "line": "Every connection as a cell in a table of causes and effects; loops become staircases.",
        "idea": (
            "A table answers one question per cell: when the row rises, what happens to the column? The model fits that "
            "form, since every connection runs from one variable to another with a sign. Rows hold causes and columns "
            "hold effects. Each area forms a block on the diagonal. The overview folds the 51 by 51 table into a 10 by 10 "
            "table of areas, and the circle through the core areas shows up as the cells just above the diagonal plus one "
            "in the far corner. A loop in a table has an exact drawing. Go across a row to the cell of the connection, drop "
            "to the diagonal, and go across again. Each loop becomes a closed staircase."),
        "overview": (
            f"The overview shows ten rows and ten columns, one per area, in the order A, B, C, D, E, then the outside "
            f"drivers, the three economy groups and technology. Each cell holds one dot per connection, Prussian for "
            f"connections in a loop and Stone for the rest. Cells A to B, B to C, C to D, D to E and E to A carry an outline "
            f"so the forward circle is visible: {APC[('A','B')]}, {APC[('B','C')]}, {APC[('C','D')]}, {APC[('D','E')]} and "
            f"{APC[('E','A')]} connections. The table leaves out signs, delays and names at this level. Every cell with dots "
            f"is a target, and the pointer turns it into a sentence such as \"C to D: {APC[('C','D')]} connections, "
            f"{APC_LOOP[('C','D')]} in loops\"."),
        "closeups": (
            "Clicking the C block opens a five by five table of its variables, with a strip on each side for the eight "
            "connections that arrive and the seven that leave. The diagonal cells hold the variable icons. Each filled "
            "cell shows its sign and a short stroke in its evidence texture. R10 draws as a staircase through C1, C2, C3 "
            "and C4: across from C1 to the C2 column, down to the diagonal, across to C3, and on around back to C1. Its "
            "one dashed step sits in the cell for L53, \"Officials safe from defeat write rules for themselves\". The R10 "
            "page lists the four cells as four sentences in reading order."),
        "thumbs": (
            "Each thumbnail is the core table in miniature with one staircase on it. The corners sit at real cells, so the "
            "outline depends on which variables the loop visits and in what order. Loops inside one area make small steps "
            "near the diagonal. R1 and R5 make large steps between A and E, and R12 climbs from D to C and back. "
            "Two-step loops draw as rectangles, longer loops as stairs with more turns."),
        "ground": (
            "White ground, Stone grid, Charcoal type, Prussian and Verdigris staircases. The one red outlines a cell. In "
            "the sketch it is L25, \"Decisive primaries reduce general-election pressure\", where R-01 acts."),
        "risks": (
            "Tables put off many first-time readers, and a grid of dots looks like a spreadsheet at first sight. The "
            "staircase is exact but needs a sentence of teaching before it reads as a loop. The full 51 by 51 table cannot "
            "fit a phone, so phones get one block at a time. Empty cells dominate: 118 connections fill under 5 percent "
            "of the 2,601 cells."),
        "why": "The most exact drawing of the model and the least inviting first screen; keep it as the expert view.",
    },
    {
        "key": "honeycomb", "name": "Honeycomb", "ground_name": "Newsprint",
        "sketch": sketch_honeycomb, "thumb": hex_thumb, "thumb_bg": NEWS,
        "line": "Fifty-one equal tiles in territories, the way newsrooms draw states on election night.",
        "idea": (
            "Election-night hex maps taught a wide public that a tile can stand for a place, and that equal tiles keep "
            "big places from drowning small ones. Here each variable gets one hexagon with its icon. Areas become "
            "territories of touching tiles with firm borders, set apart by a channel of empty cells, and the placement "
            "puts connected variables side by side wherever it can. The overview draws no lines. It reads like a map of a "
            "country made of islands, and each tile opens its own page."),
        "overview": (
            f"All 51 tiles show at once, grouped into territories labeled with area titles. Each tile carries its icon and "
            f"a row of small beads, one per loop that passes through it, so policy tilt to insiders carries "
            f"{F['e1_loops']}. Connections stay hidden until a tile is chosen; then its links draw as short arrows to "
            "neighbors and longer arcs to tiles farther off. The overview leaves out every line and every sign. The "
            "reader clicks a territory to open it or a tile to see its links."),
        "closeups": (
            "Clicking C enlarges its five tiles and greys the rest. Connections inside C draw as arrows between tile "
            "centers. R10 runs as a ring of arrows through safe seats, primary decisiveness, electoral pressure and "
            "incumbent control of election rules, and the step from electoral pressure to sanction applied draws in "
            "Verdigris for the balancing loop B4. Arrows from other territories enter at the border with their source "
            "tile named. The R10 page keeps the four tiles and draws each arrow in its evidence texture."),
        "thumbs": (
            "Each thumbnail is the whole honeycomb in miniature with the loop's tiles filled and a line through their "
            "centers. The silhouette of the filled tiles and its place in the map identify the loop. R8 fills two tiles "
            "of A, R10 four tiles of C, and R6 a bent run from A into B and E. A reader who has seen the honeycomb once "
            "knows where each thumbnail points."),
        "ground": (
            "Newsprint ground, White tiles, Charcoal icons and borders, Prussian beads. The one red outlines a tile. In "
            "the sketch it is C1, safe seats, where R-03 (proportional elections) and R-46 (expand the House) act."),
        "risks": (
            "Hiding the lines hides what the atlas is about, so the first tap has to show connections at once. Equal "
            "tiles give a variable with two connections the same weight as policy tilt to insiders. Adjacency is a "
            "compromise, since 118 connections cannot all fall between neighbors, and readers may assume that touching "
            "tiles are connected. The honeycomb suits a phone because tiles are large, countable targets."),
        "why": "The most phone-ready overview, in a form the public already knows from election coverage.",
    },
    {
        "key": "kitchen-table", "name": "Kitchen Table", "ground_name": "White",
        "sketch": sketch_kitchen_table, "thumb": kt_thumb, "thumb_bg": WHITE,
        "line": "The household at the center, with every other variable placed by how many steps it takes to reach it.",
        "idea": (
            "A first-time reader asks first how any of this touches their own life. The model gives an exact answer. "
            "Follow connections backward from households' financial security and every one of the 51 variables reaches "
            f"it within {F['home_max']} steps. {F['home_direct']} act on it directly. This direction puts that household "
            "at the center and draws a ring for each step out to six. Each variable sits on its ring inside a wedge for "
            "its area. Distance on the page then means one thing, and the reader can see that the courts sit three steps "
            "from the kitchen table and safe seats five."),
        "overview": (
            "Six rings, ten wedges and 51 points. Each point links to one variable on the next ring inward through the "
            "connection that carries it closer, so a reader can trace any variable home. The model ranks those links by "
            "loop membership first and evidence second. All other connections stay hidden. Ring numbers read one to six. "
            "The center disc holds the household icon. Readers click a wedge to open an area or a ring to list everything "
            "at that distance."),
        "closeups": (
            "Clicking C keeps the rings and swings the C wedge to the right, wide enough for icons and labels. Its five "
            "variables sit on four rings: incumbent control of election rules on the third, primary decisiveness and "
            "electoral pressure on the fourth, safe seats on the fifth and sanction applied on the sixth. Lines show the "
            "route each one takes inward. R10 draws as a lasso across rings three to five. The R10 page keeps the faint "
            "rings behind the loop so the reader sees how far it sits from home, and it names the shortest route from the "
            "loop to the household."),
        "thumbs": (
            "Each thumbnail shows the six rings faintly with the loop drawn at its true ring distances and wedge angles. "
            "Loops close to home hug the center, and R5 passes through the household itself. Loops in government and "
            "elections float on the outer rings, and loops that cross areas stretch across wedges. Each loop gets its own "
            "radial profile."),
        "ground": (
            "White ground, Stone rings, Charcoal points, Prussian loops. The one red rings the center, households' "
            "financial security, the point the headline names. Five reforms act on it directly: R-23, R-24, R-25, R-26 "
            "and R-31."),
        "risks": (
            "Step counts say nothing about strength, so a variable two steps away can look more important than one five "
            "steps away with better evidence. Rings can look like layers, and readers may take them for levels of society. "
            "Centering one variable tilts the atlas toward household money; the same frame can center any variable on "
            "request. On a phone the six rings fit as a dial, and wedge labels move into a swipe list."),
        "why": "The best first door for a member of the public: it starts at the household and measures everything from there.",
    },
    {
        "key": "spine", "name": "The Spine", "ground_name": "Newsprint",
        "sketch": sketch_spine, "thumb": spine_thumb, "thumb_bg": NEWS,
        "line": "All 51 variables on one line, with each connection as an arc; feedback shows as arcs that run back.",
        "idea": (
            "Put the variables on one line, ordered from the outside drivers through technology and the economy layer to "
            f"the core areas A to E. Then {F['spine_fwd']} connections run forward along the line and {F['spine_back']} run "
            "back. Forward arcs bow above the line and backward arcs below it. Any loop must contain at least one backward "
            "arc, so the reader finds every piece of feedback on one side of the line. On a phone the line runs down the "
            "screen, and the reader scrolls through the system from causes to consequences."),
        "overview": (
            "The line carries 51 ticks grouped by area, with area codes on a band beneath. Arcs in loops draw in Prussian "
            "and Verdigris, all others in thin Stone. The overview leaves out names and signs and keeps the arcs, which "
            "form a skyline above the line and a second one hanging below it. The reader clicks an area segment or a backward arc."),
        "closeups": (
            "Clicking C opens its five-tick segment wide, with icons and names beside each tick. Arcs inside C stay full "
            "size, and arcs to other areas shrink to stubs labeled with their far end. R10 shows as three forward arcs, C1 "
            "to C2, C2 to C3 and C3 to C4, and one backward arc, C4 to C1. The R10 page turns the segment into a column and "
            "keeps the backward step on its own side."),
        "thumbs": (
            "Each thumbnail draws the line short and plain with one loop's arcs. Which segment the arcs sit over, how wide "
            "they span and how many sit above or below give each loop its signature. Loops inside one area make small "
            "humps. R1, R5, R6 and R15 throw a long backward arc from legitimacy back to the economic structure."),
        "ground": (
            "Newsprint ground, Charcoal ticks, Prussian and Verdigris loop arcs, Stone for the rest. The one red marks an "
            "arc. In the sketch it is L03, \"Policy advantages add to wealth at the top\", the backward arc that closes R1 "
            "and the place where R-28 acts."),
        "risks": (
            "Arc diagrams are abstract, and the picture depends on the order chosen; another order gives another skyline. "
            "Long arcs dominate the view, though their length only measures distance in the list. With 118 arcs the core "
            "end of the line gets dense. The spine suits a phone better than any other direction, because it scrolls in "
            "one dimension."),
        "why": "Exact and easy to scroll, held back by abstraction and by its dependence on one chosen order.",
    },
    {
        "key": "flywheels", "name": "Flywheels and Governors", "ground_name": "Newsprint",
        "sketch": sketch_flywheels, "thumb": fly_thumb, "thumb_bg": NEWS,
        "line": "Loops as machines: reinforcing loops are flywheels, balancing loops are governors.",
        "idea": (
            "Engineers built two devices that behave like the two kinds of loop. A flywheel keeps turning the way it was "
            "pushed, as a reinforcing loop keeps a change going up or down. A governor, the pair of spinning weights on a "
            "steam engine, pushes back harder the faster the engine runs, as a balancing loop does. This direction makes "
            "loops the main objects. Each of the 23 loops is a wheel, and wheels that share a variable connect through a "
            f"pin named for it. The machine shows how loops lock together: {F['e1_loops']} turn on the pin for policy tilt "
            "to insiders, and four on each of the pins for electoral pressure and incumbent control of election rules."),
        "overview": (
            f"The overview shows 23 wheels and {len(SHARED)} pins, one pin for each variable that sits in two or more "
            "loops. Rods join each wheel to the pins it shares. Reinforcing wheels carry spokes and a heavy Prussian rim. "
            "Balancing wheels carry a small governor inside a Verdigris rim. Each rim splits into one arc per step, sized "
            "by delay and drawn in its evidence texture, so a loop with long delays and weak evidence has long, broken "
            "arcs. R8, B2 and B3 share no variable with any other loop and stand apart. Variables in no loop are left out. "
            "Readers click a wheel to open a loop or a pin to open a variable."),
        "closeups": (
            "Clicking area C gathers the seven wheels that pass through it: R10, R4a, R12, R4b, R11, R16 and B4, hung on "
            "the pins for safe seats, electoral pressure and incumbent control of election rules. The five C variables line "
            "up along the top with their icons. R10 is a four-spoke flywheel whose rim arcs run under two years, under two "
            "years, 2 to 10 years and 2 to 10 years, and its third arc is dashed. The R10 page turns the wheel slowly on "
            "load and sets each step's sentence beside its arc."),
        "thumbs": (
            "The thumbnail is the wheel itself. Spoke count gives the number of steps, arc length gives the delays, texture "
            "gives the evidence and the inner drawing gives the type. A mark at the hub shows the loop's state from the "
            "model: a chevron up or down for loops running up or down, a brake bar for switched off, an open hub for the "
            "design target. R13 is a two-spoke flywheel with one short arc and one long one. B1a is a governor with a brake "
            "bar, because the model lists it as switched off."),
        "ground": (
            "Newsprint ground, Charcoal spokes and pins, Prussian flywheel rims, Verdigris governors. The one red marks a "
            "rim arc. In the sketch it is the step in B1a from oversight back to policy favoritism (L16), where R-08 and "
            "R-15 act, on the one governor the model lists as switched off."),
        "risks": (
            "Machines suggest fixed ratios and certain outcomes, and the model claims neither. Readers may take spin as "
            "speed or meshing as cause, so the drawing uses pins and rods and avoids gear teeth. The view leaves out the "
            f"{F['no_loop']} variables in no loop and the 72 connections outside loops, so it shows the system's feedback "
            "and hides its inputs. On a phone the wheel thumbnails hold up well, and the full machine needs pinch zoom."),
        "why": "It teaches the difference between feeding itself and pushing back through objects people already know.",
    },
    {
        "key": "crossroads", "name": "Crossroads", "ground_name": "Prussian",
        "sketch": sketch_crossroads, "thumb": cross_thumb, "thumb_bg": PRU,
        "line": "Loops as petals growing from the variables they share, printed like a cyanotype.",
        "idea": (
            f"Loops in this model cluster on a few variables. Policy tilt to insiders sits in {F['e1_loops']} loops, and "
            "electoral pressure and incumbent control of election rules in four each. A loop that leaves a variable and "
            "returns to it draws as a petal. Gathering petals on their shared variable turns each hub into a rosette, and "
            "the system becomes a small garden of them. The style borrows from nineteenth-century cyanotype plates of "
            "plants, white on Prussian blue, a blue the brand already owns."),
        "overview": (
            "Each loop draws once, anchored at the station it shares with the most loops. That gives seven petals at "
            "policy tilt to insiders, four at incumbent control of election rules, three at electoral pressure and two at "
            "executive unilateralism, plus five single petals and two sketched seeds without a hub. Petal length follows "
            "the loop's total delay and its width the number of steps. Variables in no loop sit as small icons around the "
            "margin with arrows toward the hubs they push. Readers click a hub to open its rosette or a petal to open a loop."),
        "closeups": (
            "Clicking area C opens the two rosettes rooted there. Incumbent control of election rules carries R4a, R4b, "
            "R10 and R12, and electoral pressure carries R11, R16 and B4. R10 grows from the first as a four-station petal "
            "running out through safe seats and primary decisiveness to electoral pressure and back. Electoral pressure "
            "also roots its own rosette, so a fine thread joins the two places it appears. The R10 page lifts the petal "
            "free and labels each station with icon and name."),
        "thumbs": (
            "Each thumbnail is one petal with its hub icon at the base. Length, width, station count and edge textures "
            "come from the loop, and balancing petals fill with Verdigris. R13 is short and narrow, R6 long and wide, and "
            "R2 is dotted along both edges because both its steps are hypotheses. Petals from the same hub share a base "
            "icon, which groups them on the all-loops page."),
        "ground": (
            "Prussian ground with White and Newsprint line work. Red never sits on Prussian, so the red lives on a "
            "Newsprint label tag pinned to the hub the headline names. In the sketch the tag marks policy tilt to "
            "insiders, where R-09 and R-27 act."),
        "risks": (
            "Anchoring each loop at one hub means a variable such as electoral pressure appears in more than one place, "
            "which can confuse a first-time reader. Petal length may read as importance. A Prussian page with white line "
            "work is striking and dark, so long reading moves to Newsprint pages one click down. On a phone one rosette "
            "fills the screen and the garden becomes a swipe between hubs."),
        "why": "Striking and true to where loops meet, but showing one variable in two places will trip up new readers.",
    },
    {
        "key": "open-atlas", "name": "Open Atlas", "ground_name": "Newsprint",
        "sketch": sketch_open_atlas, "thumb": atlas_thumb, "thumb_bg": NEWS,
        "line": "The system as a two-page spread: the economy on the left, democracy on the right, technology in the fold.",
        "idea": (
            "The atlas models democracy and the economy as one causal system, and a book spread can show exactly that. The "
            "left page holds economic structure and the economy layer, 18 variables. The right page holds political "
            "inputs, electoral competition, governing institutions and legitimacy, 20 variables. Technology touches both "
            "and sits in the fold, and the outside drivers sit in the top margin. "
            f"{F['crossings']} connections cross the fold, {F['to_dem']} toward democracy and {F['to_econ']} toward the "
            f"economy, and {F['to_econ_e1']} of those {F['to_econ']} start at policy tilt to insiders. The crossings carry "
            "the atlas's argument, and the spread puts them in the middle of the page."),
        "overview": (
            "Each page shows its variables as icons in small groups by area. Connections within a page draw thin and "
            "Stone, and the twelve crossings draw heavier in Charcoal. Four loops cross the fold, R1, R5, R6 and R15, and "
            "they draw in Prussian. R8 stays on the economy page and every other loop stays on the democracy page. "
            "Technology's eight variables stack in the fold with lines out to both sides. Readers click a page group to "
            "open an area, or a crossing to read it."),
        "closeups": (
            "Clicking area C turns to a right-hand page given over to elections. Its five variables spread across the page, "
            "and the eight incoming and seven outgoing connections run to the page edges labeled with the page and area at "
            "their far end. R10 sits wholly on this page. The R10 page shows the loop as a closed circuit in the middle of "
            "the right-hand page, with a note that none of its steps crosses to the economy."),
        "thumbs": (
            "Each thumbnail is a tiny spread, two page rectangles and a fold, with the loop drawn at its stations' "
            "positions. Loops that cross the fold read at once: R1, R5, R6 and R15 cross twice each. R8 sits alone on the "
            "left page. The rest sit on the right in different places, with R10 and R4a high in the elections group and "
            "R13 and R18 lower down in government."),
        "ground": (
            "Newsprint ground with two White pages, Charcoal crossings, Prussian loops and Stone for the rest. The one red "
            "marks a crossing. In the sketch it is L31, \"Insider-tilted labor rules weaken worker bargaining\", the step "
            "that closes both R6 and R15 and the place where R-21 acts."),
        "risks": (
            "Putting economic structure on the economy page is a choice. Area A could sit on either side, and the count of "
            "crossings depends on it. Pages suggest two separate books, so the fold has to look busy. Technology in the "
            "fold may read as the hinge of the whole system, which the model does not claim. On a phone the spread "
            "becomes two pages with the fold between them as a strip of crossings."),
        "why": "It puts the publication's own argument, that democracy and the economy form one system, in the middle of the page.",
    },
    {
        "key": "tabletop", "name": "Tabletop Model", "ground_name": "White",
        "sketch": sketch_tabletop, "thumb": table_thumb, "thumb_bg": WHITE,
        "line": "An architect's model of the system, each variable a block whose height counts the loops through it.",
        "idea": (
            "People read a physical model faster than a diagram. They see what stands tall and look around it. This "
            "direction builds the system as a tabletop model in isometric view. Each area is a low plinth, and each "
            "variable is a block on it. Block height has one meaning, the number of loops that pass through the "
            f"variable, so policy tilt to insiders rises {F['e1_loops']} units and the {F['no_loop']} variables in no loop "
            "lie flat. Loop steps arc between block tops. The reader sees where feedback concentrates from the skyline alone."),
        "overview": (
            "Eight plinths sit on the table: the five core areas, the outside drivers, the economy layer and technology. "
            "The overview shows all 51 blocks with icons on their tops and the loop arcs between them. Connections outside "
            "loops stay out until a block is chosen. Plinth labels sit along the front edges. Readers click a plinth to "
            "lift it from the table or a block to open the variable."),
        "closeups": (
            "Clicking C lifts its plinth forward and turns it to face the reader. Its five blocks stand three, one, four, "
            "four and one units tall: safe seats, primary decisiveness, electoral pressure, incumbent control of election "
            "rules and sanction applied. R10 arcs across the first four. Arcs to other plinths stay as stubs. The R10 page "
            "sets the four blocks alone on a small plinth with the loop's arcs over them and the step sentences on cards in front."),
        "thumbs": (
            "Each thumbnail is a small plinth holding only the loop's blocks, at their real heights and their relative "
            "places on the table. R10 shows two four-unit towers beside a three-unit block and a one-unit block. R5 shows a "
            "seven-unit tower beside a three-unit block and a one-unit block. R8 shows two short blocks side by side. The "
            "skyline of each loop is its signature."),
        "ground": (
            "White ground, Newsprint and Stone plinths, White blocks with Charcoal edges, Prussian and Verdigris arcs. The "
            "one red marks the top of a block. In the sketch it is electoral pressure, which sits in four loops and where "
            "R-02, R-07 and R-47 act."),
        "risks": (
            "Height invites readers to read the block as the amount of the variable, such as how much electoral pressure "
            "exists, which the model does not measure. Isometric views hide short blocks behind tall ones, so the camera "
            "has to turn. A 3D view costs more to build and to make accessible. On a phone the table fits as a picture, but "
            "blocks become small targets, so the first tap picks a plinth."),
        "why": "An appealing skyline, but height will be read as amount, and it costs the most to build.",
    },
]

RANK = ["great-circle", "star-atlas", "open-atlas", "kitchen-table", "flywheels", "honeycomb",
        "crossroads", "spine", "ledger-grid", "tabletop"]
BUILD = RANK[:6]

# --------------------------------------------------------------------------
# Writing checks for every sentence that ships
# --------------------------------------------------------------------------
BANNED = ["—", "–", " really ", " truly ", " genuinely ", " actually ", "leverage", "underscore",
          "reflect", " not just ", "isn't just"]


def check_prose(s):
    low = f" {s.lower()} "
    for b in BANNED:
        assert b not in low, (b, s[:80])


for d in DIRECTIONS:
    for k in ("line", "idea", "overview", "closeups", "thumbs", "ground", "risks", "why"):
        check_prose(d[k])


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
def legend_svg():
    s = Svg("lg", 560, 54, WHITE)
    items = [("documented or well-supported", "documented"), ("plausible", "plausible"),
             ("contested", "plausible_contested"), ("hypothesis", "hypothesis")]
    x = 0
    for name, ev in items:
        s.add(L(x + 2, 18, x + 44, 18, CHAR, 1.8, ev, extra=' stroke-linecap="round"' if ev in ("documented",) else ""))
        s.add(T(x + 52, 22.5, name, 13, CHAR))
        x += 60 + len(name) * 6.9
    s.add(L(2, 44, 44, 44, PRU, 2.2), T(52, 48.5, "reinforcing loop, feeds itself", 13, CHAR))
    s.add(L(262, 44, 304, 44, VERD, 2.2), T(312, 48.5, "balancing loop, pushes back", 13, CHAR))
    return s.render(size='width="560" height="54"')


def build():
    sketches = {}
    thumbs = {}
    for d in DIRECTIONS:
        sketches[d["key"]] = d["sketch"]()
        thumbs[d["key"]] = [(lid, d["thumb"](lid)) for lid in LOOP_ORDER]
    rank_of = {k: i + 1 for i, k in enumerate(RANK)}

    css = """
    :root{--news:#DCD9D2;--char:#121212;--red:#E63946;--pru:#1F2D5A;--stone:#5D636D;--verd:#4A7C74;--white:#FFFFFF}
    *{box-sizing:border-box}
    body{margin:0;background:var(--news);color:var(--char);font:15px/1.55 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
    .wrap{max-width:1360px;margin:0 auto;padding:56px 40px 72px}
    .kicker{font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--stone)}
    h1{font-family:'Inter Tight',Inter,sans-serif;font-weight:700;font-size:72px;line-height:1.0;letter-spacing:-.02em;margin:14px 0 18px}
    .dek{font-size:19px;line-height:1.5;max-width:880px;margin:0 0 26px}
    .quote{font-family:Lora,Georgia,serif;font-style:italic;font-size:21px;line-height:1.45;max-width:900px;border-left:3px solid var(--char);padding:4px 0 4px 20px;margin:0 0 8px}
    .quote-by{font-size:13px;color:var(--stone);margin:0 0 40px 23px}
    .facts{display:grid;grid-template-columns:repeat(6,1fr);gap:0;background:var(--white);border-top:3px solid var(--char)}
    .fact{padding:20px 18px 22px;border-right:1px solid var(--news)}
    .fact:last-child{border-right:0}
    .fact b{display:block;font-family:'Inter Tight',Inter,sans-serif;font-size:44px;line-height:1;font-weight:700;letter-spacing:-.02em;margin-bottom:10px}
    .fact span{font-size:13px;line-height:1.45;display:block}
    .legend{display:flex;align-items:center;gap:28px;background:var(--white);padding:16px 18px;margin:12px 0 0}
    .legend p{margin:0;font-size:13px;max-width:560px}
    .legend .red{display:inline-block;width:22px;height:4px;background:var(--red);vertical-align:middle;margin-right:6px}
    .card{background:var(--white);margin:44px 0 0;padding:34px 38px 36px;border-top:3px solid var(--char)}
    .top{display:grid;grid-template-columns:1fr 680px;gap:36px;align-items:start}
    .num{font-family:'Inter Tight',Inter,sans-serif;font-weight:700;font-size:15px;letter-spacing:.08em;color:var(--stone)}
    .num em{font-style:normal;color:var(--char);background:var(--news);padding:2px 8px;margin-left:8px;letter-spacing:.04em}
    .num em.build{background:var(--char);color:var(--white)}
    h2{font-family:'Inter Tight',Inter,sans-serif;font-size:44px;line-height:1.02;letter-spacing:-.02em;margin:8px 0 12px}
    .line{font-size:18px;line-height:1.45;margin:0 0 18px;font-weight:500}
    h3{font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 6px;font-weight:700}
    .card p{margin:0 0 16px}
    .sk{border:1px solid var(--stone);line-height:0}
    .sk svg{width:680px;height:425px;display:block}
    .cols{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;margin-top:26px;padding-top:22px;border-top:1px solid var(--news)}
    .cols p{font-size:14px;line-height:1.55}
    .strip{margin-top:10px;padding-top:18px;border-top:1px solid var(--news)}
    .strip h3{margin-bottom:12px}
    .tgrid{display:grid;grid-template-columns:repeat(12,1fr);gap:10px 6px}
    .t{text-align:center;font-size:13px;font-weight:600;line-height:1.2}
    .t svg{display:block;margin:0 auto 4px;width:76px;height:76px}
    .t small{display:block;font-weight:400;color:var(--stone);font-size:13px}
    .rank{background:var(--white);margin:44px 0 0;padding:34px 38px;border-top:3px solid var(--char)}
    .rank ol{list-style:none;padding:0;margin:18px 0 0;counter-reset:r}
    .rank li{display:grid;grid-template-columns:48px 260px 1fr 90px;gap:16px;align-items:baseline;padding:12px 0;border-top:1px solid var(--news);font-size:15px}
    .rank li b{font-family:'Inter Tight',Inter,sans-serif;font-size:22px}
    .rank li .n{font-family:'Inter Tight',Inter,sans-serif;font-size:22px;color:var(--stone);font-weight:700}
    .rank li .tag{font-size:13px;font-weight:700;text-align:center;padding:3px 0;background:var(--char);color:var(--white)}
    .rank li .tag.no{background:var(--news);color:var(--char);font-weight:500}
    footer{font-size:13px;color:var(--stone);margin-top:30px}
    """

    facts = [
        (f"{F['forward']}:{F['backward']}", "Connections between neighboring core areas that run forward around A, B, C, D, E and back to A, against those that run back."),
        (str(F["knot"]), f"Variables in one knot where each can reach every other; the other {F['outside_knot']} only push into it."),
        (str(F["e1_loops"]), "Loops through policy tilt to insiders, more than any other variable. It also has the most connections, 13."),
        ("0", "Loops in the economy layer, the technology group or the outside drivers. All 23 sit in areas A to E."),
        (str(F["home_max"]), "The most steps any variable needs to reach households' financial security. All 51 get there."),
        (str(F["crossings"]), "Connections that cross between the economy (A and the economy layer) and democracy (B to E)."),
    ]
    h = []
    h.append("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
             "<title>Atlas Directions Board</title>"
             "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">"
             "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>"
             "<link href=\"https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400&display=swap\" rel=\"stylesheet\">"
             f"<style>{css}</style></head><body><div class=\"wrap\">")
    h.append("<div class=\"kicker\">Oath &amp; Action · Who Do They Answer To? · Phase 2 atlas concepts · 30 October 2026</div>")
    h.append("<h1>Ten directions<br>from scratch</h1>")
    h.append("<p class=\"dek\">Ten ways to draw the whole systems atlas, each built from a different structure and each "
             "sketched from the model file: 51 variables, 118 connections, 23 loops and 50 reforms. Every sketch carries "
             "one red, at the point its headline names. Under each sketch, all 23 loops appear as thumbnails in that "
             "direction's own drawing.</p>")
    h.append("<p class=\"quote\">“Rather than have the icons for all the loops look relatively the same, I think it "
             "would look good to just use a smaller image of the actual loop. The pages with all loops would be a page "
             "with lots of slightly different looking loops.”</p><p class=\"quote-by\">The client, on loop icons</p>")
    h.append("<div class=\"kicker\" style=\"margin-bottom:10px\">What the data says</div><div class=\"facts\">")
    for big, txt in facts:
        h.append(f"<div class=\"fact\"><b>{esc(big)}</b><span>{esc(txt)}</span></div>")
    h.append("</div>")
    h.append(f"<div class=\"legend\">{legend_svg()}<p><span class=\"red\"></span>One red per view, at the single most "
             "important point: in these sketches, a place where a reform acts. Red never sits on Prussian.</p></div>")
    for i, d in enumerate(DIRECTIONS):
        rk = rank_of[d["key"]]
        tag = f"<em class=\"build\">Rank {rk} · build</em>" if d["key"] in BUILD else f"<em>Rank {rk}</em>"
        h.append(f"<section class=\"card\" id=\"{d['key']}\"><div class=\"top\"><div>")
        h.append(f"<div class=\"num\">DIRECTION {i + 1:02d}{tag}</div><h2>{esc(d['name'])}</h2>")
        h.append(f"<p class=\"line\">{esc(d['line'])}</p>")
        h.append(f"<h3>Big idea</h3><p>{esc(d['idea'])}</p>")
        h.append(f"<h3>Ground and red · {esc(d['ground_name'])}</h3><p>{esc(d['ground'])}</p>")
        h.append(f"</div><div class=\"sk\">{sketches[d['key']].replace('width=\"640\" height=\"400\"', 'width=\"680\" height=\"425\"', 1)}</div></div>")
        h.append("<div class=\"cols\">")
        for k, t in (("overview", "Overview"), ("closeups", "Close-ups: area C and R10"),
                     ("thumbs", "Loop thumbnails"), ("risks", "Risks")):
            h.append(f"<div><h3>{t}</h3><p>{esc(d[k])}</p></div>")
        h.append("</div><div class=\"strip\"><h3>All 23 loops in this direction</h3><div class=\"tgrid\">")
        for lid, svg in thumbs[d["key"]]:
            lp = LOOPS[lid]
            sub = f"{lp['type']} · {lp['n']} steps" + (" · sketch" if lp["conceptual"] else "")
            h.append(f"<div class=\"t\">{svg}{esc(lid)}<small>{esc(sub)}</small></div>")
        h.append("</div></div></section>")
    h.append("<section class=\"rank\"><div class=\"num\">RANKING</div><h2>Ranked, and the six to build</h2>"
             "<p class=\"line\">Ranked on what a first-time reader needs: a whole picture they can grasp, loops they can "
             "tell apart, honesty about the model and a version that works on a phone.</p><ol>")
    by = {d["key"]: d for d in DIRECTIONS}
    for i, k in enumerate(RANK):
        d = by[k]
        tg = "<span class=\"tag\">Build</span>" if k in BUILD else "<span class=\"tag no\">Hold</span>"
        h.append(f"<li><span class=\"n\">{i + 1}</span><b>{esc(d['name'])}</b><span>{esc(d['why'])}</span>{tg}</li>")
    h.append("</ol></section>")
    h.append("<footer>Built by build_sketches.py from work/boards/phase-2/maps/20261028_Maps-Model-Data.json "
             "(snapshot 15 October 2026) and the variable icon map of 30 October 2026. Icons: Civic Line, black and "
             "newsprint editions, used as drawn. Sketches are rough and drawn from the data; layouts in Star Atlas, "
             "Flywheels and Honeycomb come from seeded layout routines.</footer>")
    h.append("</div></body></html>")
    open(OUT_HTML, "w").write("".join(h))

    # handoff markdown
    md = []
    md.append("# Who Do They Answer To? Ten atlas directions from scratch\n")
    md.append("Date: 30 October 2026  \nFor: Dustin Cathcart, Founder and Editor, Oath & Action  \n"
              "Review board: `work/boards/phase-2/atlas-concepts/ideas/20261030_From-Scratch-Directions-Sketches.html` "
              "(capture: `20261030_From-Scratch-Directions-Sketches.png` beside it)  \n"
              "Built by: `work/boards/phase-2/atlas-concepts/ideas/build_sketches.py`  \n"
              "Sources read: `work/boards/phase-2/maps/20261028_Maps-Model-Data.json` and "
              "`work/boards/phase-2/atlas-concepts/shared/20261030_Variable-Icon-Map.json`, plus the Civic Line SVGs.\n")
    md.append("## What the data says\n")
    md.append("I studied the model before sketching. These findings shaped the ten structures.\n")
    md.append(f"- The five core areas pass influence around a circle. Between neighboring areas in the order A, B, C, D, E "
              f"and back to A, {F['forward']} connections run forward and {F['backward']} run back.\n"
              f"- {F['knot']} variables form one knot in which each can reach every other. The other {F['outside_knot']} "
              "only push into it. Housing scarcity and owner home equity form their own small loop (R8) outside the knot.\n"
              "- All 23 loops sit in areas A to E. The economy layer, the technology group and the outside drivers hold no "
              f"loop, and {F['no_loop']} variables sit in no loop at all.\n"
              f"- Policy tilt to insiders (E1) sits in {F['e1_loops']} loops and has {F['e1_deg']} connections, the most "
              "of any variable. Electoral pressure (C3) and incumbent control of election rules (C4) sit in four loops each.\n"
              "- L42, \"Incumbent-drawn maps create safe seats\", is the only connection in three loops (R4a, R10, R12).\n"
              "- 46 pairs of loops share at least one variable. R8, B2 and B3 share none.\n"
              f"- Following connections backward, all 51 variables reach households' financial security (A4) within "
              f"{F['home_max']} steps, and {F['home_direct']} act on it directly.\n"
              f"- {F['crossings']} connections cross between the economy (A and the economy layer) and democracy (B to E): "
              f"{F['to_dem']} toward democracy, {F['to_econ']} toward the economy. Four loops cross: R1, R5, R6 and R15.\n"
              "- Loops differ in ways a drawing can carry: 12 have two steps, 7 three and 4 four; 18 reinforce and 5 "
              "balance; each step has its own delay and evidence grade; and the model gives each loop a state, from "
              "running up to switched off.\n")
    md.append("Every sketch below follows the brand rules: only the seven brand colors, one working red at the point the "
              "headline names, and evidence drawn as line texture (solid for documented and well-supported, dashed for "
              "plausible, dash-dot for contested, dotted for hypothesis). The three sketched loops, which have no numbered "
              "chain to grade, draw as a hollow band so that no texture claims a grade they lack.\n")
    for i, d in enumerate(DIRECTIONS):
        md.append(f"## {i + 1}. {d['name']}\n")
        md.append(f"{d['line']}\n")
        md.append(f"**Big idea.** {d['idea']}\n")
        md.append(f"**Overview.** {d['overview']}\n")
        md.append(f"**Close-ups: area C and R10.** {d['closeups']}\n")
        md.append(f"**Loop thumbnails.** {d['thumbs']}\n")
        md.append(f"**Ground and red.** {d['ground']}\n")
        md.append(f"**Risks.** {d['risks']}\n")
        md.append("**Sketch.** Drawn from the model data at 640 by 400.\n")
        md.append(sketches[d["key"]] + "\n")
    md.append("## Ranking\n")
    md.append("I ranked the ten on what a first-time reader needs: a whole picture they can take in, loops they can tell "
              "apart, honesty about what the model claims, and a version that works on a phone.\n")
    for i, k in enumerate(RANK):
        md.append(f"{i + 1}. **{by[k]['name']}.** {by[k]['why']}")
    md.append("\n## The six I would build\n")
    for k in BUILD:
        md.append(f"- **{by[k]['name']}.** {by[k]['why']}")
    md.append("\nTogether the six give the client six different structures to choose among: a ring, a sky, a book "
              "spread, a dial centered on the household, a machine of loops and a tiled map.\n")
    md.append("## Notes on method\n")
    md.append("- Every label, sign, grade, delay and count in the sketches and in this text comes from the model file. "
              "The script asserts the reach figure and computes the others at build time.\n"
              "- Star Atlas, Flywheels and Governors and Honeycomb place things with seeded layout routines. Positions in "
              "those sketches carry no meaning beyond what each pitch states.\n"
              "- The loop record for R10 lists three reforms (R-01, R-02, R-03). Two more, R-46 and R-47, name R10 among "
              "their loops, so a close-up should show all five.\n"
              "- Tested: the script runs, every SVG text is 13 px or larger, and the page renders at 1440 px wide. Not "
              "tested: phone layouts, motion and interaction, which these sketches only describe.\n")
    text = "\n".join(md)
    for b in ("—", "–"):
        assert b not in text
    open(OUT_MD, "w").write(text)
    print("wrote", OUT_HTML)
    print("wrote", OUT_MD)
    print(json.dumps(FACTS))


if __name__ == "__main__":
    build()
