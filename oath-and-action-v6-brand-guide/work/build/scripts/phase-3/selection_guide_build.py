"""Write chapter 14's selection guide, "Choose a chart": every form in the chapter as a small picture under its question.

Oath & Action Edition 06, Phase 3, round 5. Selection guide maker, November 14, 2026, under
work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md (R5-2, DR-273), the engineer's R5-2 contract, the data lead's
ruling (a) with its addition A-1, the accessibility lead's interaction specification, section 1, and the editor's
"Words for the selection guide maker" (all in work/handoffs/phase-3/20261114_Round-5-*-Notes.md).

Usage:
    python3 -I work/build/scripts/phase-3/selection_guide_build.py            write the fragment and its meta file
    python3 -I work/build/scripts/phase-3/selection_guide_build.py --check    exit 1 when either file on disk differs
    python3 -I work/build/scripts/phase-3/selection_guide_build.py --page P   also prove every link lands on page P
    python3 -I work/build/scripts/phase-3/selection_guide_build.py --sheet P  also write a review sheet (scratch only)

Reads:
    work/handoffs/phase-3/20261112_Chapter-14-Plan.json   the 127 forms: rule, family, name, tier (the only source)
    work/build/guide/entries/14-chapter.json              the 16 questions as the chapter prints them, the label
    work/build/data/census-cb-2024-states.geojson         land and state outlines for the map pictures
    work/build/data/census-cb-2024-counties.geojson       one state's counties (14.120's picture)
    work/build/data/census-cb-2024-cd119.geojson          one state's districts (14.119's picture)
    work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json   the tile grid (14.114, 14.115, 14.124)
Writes:
    work/build/guide/specimens/s-14-selection-guide.html        the fragment: one symbol set, then the guide
    work/build/guide/specimens/s-14-selection-guide.meta.json   the manifest keys the shell reads, and a draft label

Every picture is a shape, never data (ruling a): no number, word, axis value, party mark or color scale; the shadings
on the map pictures follow an invented pattern, so the plate states no figure. Each picture draws from one <symbol>
by <use>, in one stroke weight (2 px; the avoid mark's frame is 1 px, as A-1 sets), in the kit's neutral inks only.
The checks below stop the script on any fault before it writes.
"""
import argparse
import html
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PLAN = ROOT / "work/handoffs/phase-3/20261112_Chapter-14-Plan.json"
CHAPTER = ROOT / "work/build/guide/entries/14-chapter.json"
SPECIMENS = ROOT / "work/build/guide/specimens"
SID = "s-14-selection-guide"
FRAG = SPECIMENS / f"{SID}.html"
META = SPECIMENS / f"{SID}.meta.json"
GEO_STATES = ROOT / "work/build/data/census-cb-2024-states.geojson"
GEO_COUNTIES = ROOT / "work/build/data/census-cb-2024-counties.geojson"
GEO_CD = ROOT / "work/build/data/census-cb-2024-cd119.geojson"
TILE_GRID = ROOT / "work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json"
WRITTEN = "November 14, 2026"

W, H = 88, 56          # every picture's box, drawn at true size (viewBox = width and height), so a 2 px line is 2 px
SW = 2                 # the one stroke weight

# The kit's ink classes (kit.css, R1-C1), neutral roles only (ruling a, A-1): no point red, no Verdigris or Prussian,
# no sequential or diverging steps
FS, FC, FL, FG, FT = "oac-f-subject", "oac-f-context", "oac-f-light-fill", "oac-f-gridline", "oac-f-track"
M1, M2, M3, M4 = "oac-f-mag-1", "oac-f-mag-2", "oac-f-mag-3", "oac-f-mag-4"
SS, SC, SL, SG, ST = "oac-s-subject", "oac-s-context", "oac-s-light-fill", "oac-s-gridline", "oac-s-track"
INKS = {FS, FC, FL, FG, FT, M1, M2, M3, M4, SS, SC, SL, SG, ST}
TIER_ORDER = ["Core", "Extended", "Reference", "Avoid"]


def need(cond, msg):
    if not cond:
        raise SystemExit(f"selection_guide_build: {msg}")


def e(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------------------------------------------------------------
# Drawing helpers. Coordinates are px in the 88 by 56 box; a 2 px line centered on a whole number sits on whole pixels.

def f(v):
    v = round(float(v), 1)
    return str(int(v)) if v == int(v) else f"{v:.1f}"


def tenths(v):
    """A number of tenths written short: 125 -> '12.5', -5 -> '-.5', 120 -> '12'."""
    t = f"{v / 10:.1f}".rstrip("0").rstrip(".")
    return re.sub(r"^(-?)0\.", r"\1.", t) if t not in ("0", "-0") else "0"


def joinnums(vals):
    out = ""
    for v in vals:
        if out and not v.startswith("-") and not (v.startswith(".") and "." in re.split(r"[ \-]", out)[-1]):
            out += " "
        out += v
    return out


def q5(v):
    """A coordinate in tenths of a pixel, rounded to the nearest half pixel: at the drawn size and at twice it, a half
    pixel is the finest step a screen shows, and the shorter numbers carry no other change."""
    return int(round(v * 2)) * 5


def ring_d(pts):
    """A closed ring as one short path: its first point, then each step relative, in tenths of a pixel."""
    t = []
    for x, y in pts:
        q = (q5(x), q5(y))
        if not t or q != t[-1]:
            t.append(q)
    if len(t) > 1 and t[-1] == t[0]:
        t.pop()
    if len(t) < 3:
        return ""
    head_ = "M" + joinnums([tenths(t[0][0]), tenths(t[0][1])])
    steps = [tenths(v) for (a, b), (c, d) in zip(t, t[1:]) for v in (c - a, d - b)]
    return head_ + "l" + joinnums(steps) + "z"


NUM = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|-?(?:\d+\.?\d*|\.\d+)")
ARITY = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}


def mini(d):
    """Path data written short, drawing the same shape: every point rounded to a tenth of a pixel, each step written
    absolute or relative, whichever is shorter, numbers without a leading zero and spaces only where a number needs one."""
    toks = NUM.findall(d)
    out, prev = [], None
    cx = cy = sx = sy = 0  # the current point and the subpath's start, in tenths
    i = 0
    while i < len(toks):
        cmd = toks[i]
        i += 1
        C, rel = cmd.upper(), cmd.islower()
        if C == "Z":
            out.append("z")
            prev = "z"
            cx, cy = sx, sy
            continue
        first = True
        while i < len(toks) and not toks[i].isalpha():
            a = [float(t) for t in toks[i:i + ARITY[C]]]
            i += ARITY[C]
            c = "L" if (C == "M" and not first) else C
            first = False
            ax, ay = (cx / 10, cy / 10) if rel else (0, 0)
            if c == "A":
                rx, ry, rot, fa, fs, x, y = a
                ex, ey = q5(x + ax), q5(y + ay)
                fixed = [tenths(round(rx * 10)), tenths(round(ry * 10)), tenths(round(rot * 10)), str(int(fa)), str(int(fs))]
                cand = [("A", fixed + [tenths(ex), tenths(ey)]), ("a", fixed + [tenths(ex - cx), tenths(ey - cy)])]
            elif c == "H":
                ex, ey = q5(a[0] + ax), cy
                cand = [("H", [tenths(ex)]), ("h", [tenths(ex - cx)])]
            elif c == "V":
                ex, ey = cx, q5(a[0] + (cy / 10 if rel else 0))
                cand = [("V", [tenths(ey)]), ("v", [tenths(ey - cy)])]
            else:
                pts = [(q5(a[k] + ax), q5(a[k + 1] + ay)) for k in range(0, len(a), 2)]
                ex, ey = pts[-1]
                cand = [(c, [tenths(v) for p_ in pts for v in p_]), (c.lower(), [tenths(v) for p_ in pts for v in (p_[0] - cx, p_[1] - cy)])]
            if c == "M":
                cand = [("M", cand[0][1]), ("m", cand[1][1])] if prev not in (None,) else [("M", cand[0][1])]
            letter, nums = min(cand, key=lambda t: len(joinnums(t[1])))
            if c in ("L",) and letter == "l" and ex == cx and ey != cy:
                letter, nums = "v", [tenths(ey - cy)]
            elif c in ("L",) and letter == "l" and ey == cy and ex != cx:
                letter, nums = "h", [tenths(ex - cx)]
            body = joinnums(nums)
            if letter == prev and letter.upper() not in ("M",):
                out.append(("" if body.startswith("-") else " ") + body)
            else:
                out.append(letter + body)
            prev = letter
            cx, cy = ex, ey
            if c == "M":
                sx, sy = ex, ey
    return "".join(out)


DOT1 = re.compile(r"M(-?[\d.]+) (-?[\d.]+)a([\d.]+) \3 0 1 0 [\d.]+ 0a\3 \3 0 1 0 -[\d.]+ 0")


def P(cls, d, extra=""):
    if cls.startswith("oac-f-") and not extra:
        found = DOT1.findall(d)
        if found and "".join(DOT1.findall(d) and [m.group(0) for m in DOT1.finditer(d)]) == d and len({r for x, y, r in found}) == 1:
            # a run of filled dots of one size, each written as a zero-length step with a round end: the same disc in
            # a tenth of the bytes, in the same ink role (its stroke class), so forced colors and print treat it alike
            r = float(found[0][2])
            dd = mini("".join(f"M{f(float(x) + r)} {y}h0" for x, y, rr in found))
            return (f'<path class="{cls.replace("oac-f-", "oac-s-")}" d="{dd}" stroke-width="{f(2 * r)}" '
                    f'stroke-linecap="round"/>')
    return f'<path class="{cls}" d="{mini(d)}"{extra}/>'


def rects(rs):
    """Filled boxes as one path: (x, y, w, h)."""
    return "".join(f"M{f(x)} {f(y)}h{f(w)}v{f(h)}h{f(-w)}z" for x, y, w, h in rs)


def dots(ps, r):
    """Circles as one path (filled with an f class, or ringed with an s class)."""
    return "".join(f"M{f(x - r)} {f(y)}a{f(r)} {f(r)} 0 1 0 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 0 {f(-2 * r)} 0" for x, y in ps)


def dots_r(prs):
    return "".join(dots([(x, y)], r) for x, y, r in prs)


def line(pts, close=False):
    s = "M" + " ".join(f"{f(x)} {f(y)}" for x, y in pts)
    return s + ("z" if close else "")


def lines(segs):
    return "".join(line(s) for s in segs)


def head(x, y, dx, dy, ln=6, half=3.5):
    """A filled arrowhead with its tip at (x, y), pointing along (dx, dy)."""
    m = math.hypot(dx, dy) or 1
    ux, uy = dx / m, dy / m
    bx, by = x - ux * ln, y - uy * ln
    return line([(x, y), (bx - uy * half, by + ux * half), (bx + uy * half, by - ux * half)], close=True)


def curve(fn, x0, x1, step=2):
    return [(x, fn(x)) for x in frange(x0, x1, step)]


def frange(a, b, step):
    out, x = [], a
    while x < b - 1e-9:
        out.append(round(x, 2))
        x += step
    out.append(b)
    return out


def area(top, base):
    """A filled area between a top line (left to right) and a flat base."""
    return line(top + [(top[-1][0], base), (top[0][0], base)], close=True)


def band(top, bottom):
    """A filled band between two lines given left to right."""
    return line(top + list(reversed(bottom)), close=True)


def arc_pts(cx, cy, r, a0, a1, n=24):
    return [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]


def wedge(cx, cy, r0, r1, a0, a1, n=24):
    """An annular (r0 > 0) or pie (r0 = 0) wedge from angle a0 to a1 (radians, clockwise from three o'clock)."""
    outer = arc_pts(cx, cy, r1, a0, a1, n)
    inner = arc_pts(cx, cy, r0, a1, a0, n) if r0 > 0 else [(cx, cy)]
    return line(outer + inner, close=True)


def poly_ring(cx, cy, r, k, rot=-math.pi / 2, scale=None):
    scale = scale or [1] * k
    return [(cx + r * s * math.cos(rot + 2 * math.pi * i / k), cy + r * s * math.sin(rot + 2 * math.pi * i / k))
            for i, s in enumerate(scale)]


def textlines(x, y, widths, gap=5, cls=SC):
    """Lines that stand for words, as a 2 px rule in the context ink."""
    return P(cls, lines([[(x, y + i * gap), (x + w, y + i * gap)] for i, w in enumerate(widths)]))


BASE = P(SS, "M4 51H84")             # the zero line under bars and lines, in the subject ink (the kit's baseline role)


# ---------------------------------------------------------------------------------------------------------------------
# Map shapes, projected and simplified at build time from the Census files the map entries use. Albers equal-area,
# the lower 48 with Alaska and Hawaii set in, as the guide's maps set them; simplified to under one pixel.

def albers(lon, lat, lon0=-96.0, lat0=37.5, p1=29.5, p2=45.5):
    r = math.radians
    n = (math.sin(r(p1)) + math.sin(r(p2))) / 2
    c = math.cos(r(p1)) ** 2 + 2 * n * math.sin(r(p1))
    rho = math.sqrt(max(c - 2 * n * math.sin(r(lat)), 0)) / n
    rho0 = math.sqrt(c - 2 * n * math.sin(r(lat0))) / n
    th = n * r(lon - lon0)
    return rho * math.sin(th), -(rho0 - rho * math.cos(th))


def rings_of(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"][0]]
    return [p[0] for p in geom["coordinates"]]


def dp(pts, tol):
    """Douglas-Peucker on a closed ring."""
    if len(pts) < 4:
        return pts

    def rec(a, b):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        best, bi = 0, None
        for i in range(a + 1, b):
            x0, y0 = pts[i]
            d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / L if L else math.hypot(x0 - x1, y0 - y1)
            if d > best:
                best, bi = d, i
        if bi is not None and best > tol:
            return rec(a, bi)[:-1] + rec(bi, b)
        return [pts[a], pts[b]]

    far = max(range(len(pts)), key=lambda i: math.hypot(pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]))
    return rec(0, far)[:-1] + rec(far, len(pts) - 1)


def ring_area(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
                   for i in range(len(pts)))) / 2


class Geo:
    """Projected rings by code, fitted into a box."""

    def __init__(self):
        states = json.loads(GEO_STATES.read_text())["features"]
        self.raw = {}
        for ft in states:
            code = ft["properties"]["code"]
            if code == "PR":
                continue
            if code == "AK":
                proj = lambda lo, la: albers(lo if lo < 0 else lo - 360, la, -154, 50, 55, 65)
            elif code == "HI":
                proj = lambda lo, la: albers(lo, la, -157, 3, 8, 18)
            else:
                proj = albers
            self.raw[code] = [[proj(lo, la) for lo, la in ring] for ring in rings_of(ft["geometry"])]
        l48 = [p for c, rs in self.raw.items() if c not in ("AK", "HI") for r in rs for p in r]
        self.l48 = (min(p[0] for p in l48), min(p[1] for p in l48), max(p[0] for p in l48), max(p[1] for p in l48))

    def fit(self, box):
        """Place every state in box (x, y, w, h): the lower 48 fill it, Alaska and Hawaii sit at its lower left."""
        bx, by, bw, bh = box
        x0, y0, x1, y1 = self.l48
        s = min(bw / (x1 - x0), bh / (y1 - y0))
        ox, oy = bx + (bw - (x1 - x0) * s) / 2, by + (bh - (y1 - y0) * s) / 2
        out = {}
        for code, rs in self.raw.items():
            if code in ("AK", "HI"):
                pts = [p for r in rs for p in r]
                ax0, ay0, ax1, ay1 = (min(p[0] for p in pts), min(p[1] for p in pts),
                                      max(p[0] for p in pts), max(p[1] for p in pts))
                ks = s * (0.35 if code == "AK" else 1.0)
                # Alaska at the lower left, Hawaii beside it, as the guide's state maps set them
                tx = ox + (0.0 if code == "AK" else 0.21) * (x1 - x0) * s
                ty = oy + (y1 - y0) * s - (ay1 - ay0) * ks - (0.0 if code == "AK" else 0.01 * bh)
                out[code] = [[(tx + (p[0] - ax0) * ks, ty + (p[1] - ay0) * ks) for p in r] for r in rs]
            else:
                out[code] = [[(ox + (p[0] - x0) * s, oy + (p[1] - y0) * s) for p in r] for r in rs]
        return out


def ring_path(rings, tol=0.6, min_area=0.8):
    out = []
    for r in rings:
        if ring_area(r) < min_area:
            continue
        q = dp(r, tol)
        if len(q) >= 3:
            out.append(ring_d(q))
    return "".join(out)


def fit_rings(rings, box):
    pts = [p for r in rings for p in r]
    x0, y0, x1, y1 = min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)
    bx, by, bw, bh = box
    s = min(bw / (x1 - x0), bh / (y1 - y0))
    ox, oy = bx + (bw - (x1 - x0) * s) / 2, by + (bh - (y1 - y0) * s) / 2
    return lambda r: [(ox + (p[0] - x0) * s, oy + (p[1] - y0) * s) for p in r]


def lerp_class(v, classes):
    i = min(int(v * len(classes)), len(classes) - 1)
    return classes[max(i, 0)]


def pattern(x, y, k=0.0):
    """An invented smooth pattern across a picture (0 to 1), so a map's shading shows the form and states nothing."""
    v = 0.5 + 0.32 * math.sin(x / 13.0 + k) * math.cos(y / 11.0 - k) + 0.18 * math.sin((x + y) / 7.0 + 2 * k)
    return min(max(v, 0.0), 0.999)


def centroid(rings):
    pts = [p for r in rings for p in r]
    return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)


def shaded(groups_by_class):
    return "".join(P(cls, d) for cls, d in groups_by_class if d)


US_GROUPS = ("s-14-sg-us-a", "s-14-sg-us-b", "s-14-sg-us-c", "s-14-sg-us-d")


class Maps:
    """The states, projected once into the picture's box (x 4 to 84, y 4 to 52) and split into four groups by the
    invented pattern. Each group is a symbol with no ink of its own; a picture <use>s it with an ink class, which the
    shapes inherit, so the country's outline is carried once for every map picture (land, shading, outlines)."""

    def __init__(self):
        self.geo = Geo()
        self.us = self.geo.fit((4, 4, 80, 48))
        self.groups = {g: [] for g in US_GROUPS}
        for code, rs in sorted(self.us.items()):
            cx, cy = centroid(rs)
            self.groups[lerp_class(pattern(cx, cy, 0.3), US_GROUPS)].append(code)

    def symbols(self):
        out = {g: f'<path d="{"".join(ring_path(self.us[c]) for c in codes)}" stroke-linejoin="round"/>'
               for g, codes in self.groups.items()}
        out["s-14-sg-us"] = "".join(f'<use href="#{g}"/>' for g in US_GROUPS)
        return out

    @staticmethod
    def use(sym, cls, box=None):
        at = f' x="{f(box[0])}" y="{f(box[1])}" width="{f(box[2])}" height="{f(box[3])}"' if box else ""
        return f'<use href="#{sym}" class="{cls}"{at}/>'

    def land(self, cls):
        return self.use("s-14-sg-us", cls)

    def choropleth(self, classes, box=None):
        """The four groups, each in one of the classes, in order; a box draws the map smaller at (x, y, w, h)."""
        return "".join(self.use(g, c, box) for g, c in zip(US_GROUPS, classes))

    def state(self, code, cls):
        return P(cls, ring_path(self.us[code]))

    def inside(self, x, y):
        return any(point_in(x, y, r) for rs in self.us.values() for r in rs)


def point_in(x, y, ring):
    c = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            c = not c
        j = i
    return c


def sub_features(path, code, key=None):
    feats = [ft for ft in json.loads(path.read_text())["features"] if ft["properties"]["code"] == code]
    out = []
    for ft in feats:
        rs = [[albers(lo, la) for lo, la in r] for r in rings_of(ft["geometry"])]
        out.append((ft["properties"].get(key or "geoid"), rs))
    return out


# ---------------------------------------------------------------------------------------------------------------------
# The pictures. One function a rule; each returns the shapes inside its symbol. Read with the plan's form names.

G = {}


def glyph(n):
    def deco(fn):
        G[n] = fn
        return fn
    return deco


# --- Comparison: which is bigger, and how do they rank? ----------------------------------------------------------------

@glyph(15)
def g15(m):  # Ranked bar: one bar a category from a zero line, longest first
    lens = [78, 62, 49, 37, 24]
    return (P(FS, rects([(6, 6, lens[0], 6)])) + P(FC, rects([(6, 6 + 10 * i, w, 6) for i, w in enumerate(lens) if i]))
            + P(SS, "M5 4V54"))


@glyph(16)
def g16(m):  # Column: a few categories from left to right, the last one picked out
    hs = [26, 34, 22, 31, 28, 40]
    xs = [9, 22, 35, 48, 61, 74]
    return (P(FC, rects([(x, 50 - h, 8, h) for x, h in zip(xs[:-1], hs[:-1])])) + P(FS, rects([(xs[-1], 50 - hs[-1], 8, hs[-1])]))
            + BASE)


@glyph(17)
def g17(m):  # Bar with a benchmark tick: bars, each crossed by one tick at the benchmark
    lens = [14, 27, 46, 74]
    return (P(FC, rects([(6, 7 + 12 * i, w, 6) for i, w in enumerate(lens)])) + P(SS, "M5 4V54")
            + P(SS, lines([[(36, 5 + 12 * i), (36, 15 + 12 * i)] for i in range(4)])))


@glyph(18)
def g18(m):  # Dot plot: many items on one scale, one dot a row
    xs = [79, 71, 64, 57, 49, 41, 27]
    ys = [8 + 7 * i for i in range(7)]
    return (P(SG, lines([[(5, y), (84, y)] for y in ys])) + P(FC, dots(list(zip(xs[1:], ys[1:])), 3))
            + P(FS, dots([(xs[0], ys[0])], 3)))


@glyph(19)
def g19(m):  # Dumbbell: two values per item joined by a line
    pairs = [(16, 52), (28, 72), (40, 62), (13, 34)]
    ys = [10, 22, 34, 46]
    return (P(SC, lines([[(a + 4, y), (b - 4, y)] for (a, b), y in zip(pairs, ys)]))
            + P(SS, dots([(a, y) for (a, b), y in zip(pairs, ys)], 3))
            + P(FS, dots([(b, y) for (a, b), y in zip(pairs, ys)], 4)))


@glyph(20)
def g20(m):  # Slope chart: two points in time, one line an item
    pairs = [(14, 32), (22, 12), (32, 42), (44, 26)]
    ctx = pairs[1:]
    return (P(SG, "M18 6V50M70 6V50")
            + P(SC, lines([[(18, a), (70, b)] for a, b in ctx])) + P(FC, dots([p for a, b in ctx for p in ((18, a), (70, b))], 3))
            + P(SS, line([(18, pairs[0][0]), (70, pairs[0][1])])) + P(FS, dots([(18, pairs[0][0]), (70, pairs[0][1])], 3)))


@glyph(21)
def g21(m):  # Lollipop: a ranked list of thin stems with a dot at the value
    ends = [80, 69, 59, 50, 41, 31]
    ys = [8 + 8 * i for i in range(6)]
    return (P(SS, "M5 4V54") + P(SS, line([(6, ys[0]), (ends[0], ys[0])])) + P(FS, dots([(ends[0], ys[0])], 3.5))
            + P(SC, lines([[(6, y), (x, y)] for x, y in zip(ends[1:], ys[1:])])) + P(FC, dots(list(zip(ends[1:], ys[1:])), 3.5)))


@glyph(22)
def g22(m):  # Grouped bar: two series side by side in each group
    a, b = [62, 76, 40], [48, 69, 55]
    ys = [5, 21, 37]
    return (P(FS, rects([(6, y, w, 6) for y, w in zip(ys, a)])) + P(FC, rects([(6, y + 7, w, 6) for y, w in zip(ys, b)]))
            + P(SS, "M5 3V53"))


@glyph(23)
def g23(m):  # Small-multiple bars: the same comparison in three panels on one scale
    panels = [[22, 16, 12, 7], [14, 22, 9, 18], [20, 7, 15, 11]]
    out = ""
    for k, lens in enumerate(panels):
        x0 = 6 + 28 * k
        out += P(FC, rects([(x0, 10 + 10 * i, w, 6) for i, w in enumerate(lens)])) + P(SS, f"M{x0 - 1} 7V50")
        out += P(SC, f"M{x0} 4h12")
    return out


@glyph(24)
def g24(m):  # Radar chart: values on spokes joined into a shape (to avoid)
    cx, cy, r = 44, 30, 22
    out = P(SG, line(poly_ring(cx, cy, r, 5), True) + line(poly_ring(cx, cy, r * 0.55, 5), True)
            + lines([[(cx, cy), p] for p in poly_ring(cx, cy, r, 5)]))
    shape = poly_ring(cx, cy, r, 5, scale=[0.92, 0.5, 0.78, 0.36, 0.62])
    return out + P(FL, line(shape, True)) + P(SS, line(shape, True), ' stroke-linejoin="round"')


# --- Shift and swing: what moved, and which way? ------------------------------------------------------------------------

@glyph(25)
def g25(m):  # Shift arrows: an arrow from where each value was to where it went
    arrows = [(10, 40), (20, 46), (30, 76), (48, 64), (66, 40)]
    out, heads = [], []
    for i, (a, b) in enumerate(arrows):
        y = 8 + 10 * i
        d = 1 if b > a else -1
        out.append([(a, y), (b - 5 * d, y)])
        heads.append(head(b, y, d, 0))
    return P(SG, "M44 4V52") + P(SS, lines(out)) + P(FS, "".join(heads))


@glyph(26)
def g26(m):  # Change lollipop with a size-of-shift key: ranked stems from zero, a key's marks behind them
    ends = [80, 68, 57, 47, 37, 26]
    ys = [9 + 8 * i for i in range(6)]
    return (P(SG, "M30 4V53M54 4V53M78 4V53") + P(SS, "M5 4V53")
            + P(SC, lines([[(6, y), (x - 4, y)] for x, y in zip(ends[1:], ys[1:])]))
            + P(FC, "".join(head(x, y, 1, 0, 5, 3) for x, y in zip(ends[1:], ys[1:])))
            + P(SS, line([(6, ys[0]), (ends[0] - 4, ys[0])])) + P(FS, head(ends[0], ys[0], 1, 0, 5, 3)))


@glyph(27)
def g27(m):  # Diverging bar: gains to one side of a center line, losses to the other
    vals = [34, 24, 13, -8, -19, -31]
    right = [(45, 6 + 8 * i, v, 6) for i, v in enumerate(vals) if v > 0]
    left = [(43 + v, 6 + 8 * i, -v, 6) for i, v in enumerate(vals) if v < 0]
    return P(FS, rects(right)) + P(FC, rects(left)) + P(SS, "M44 3V53")


@glyph(28)
def g28(m):  # Diverging bar with arrows over time: one row a period, an arrow out from the center line
    vals = [-12, 18, 30, -24, -9, 22, 34]
    out, heads, outs, headss = [], [], [], []
    for i, v in enumerate(vals):
        y = 8 + 7 * i
        d = 1 if v > 0 else -1
        (outs if i == len(vals) - 1 else out).append([(44 + d, y), (44 + v - 5 * d, y)])
        (headss if i == len(vals) - 1 else heads).append(head(44 + v, y, d, 0, 5, 3))
    return (P(SC, lines(out)) + P(FC, "".join(heads)) + P(SS, lines(outs)) + P(FS, "".join(headss)) + P(SS, "M44 3V54"))


# --- Change over time: how has it moved? --------------------------------------------------------------------------------

def series(pts):
    return P(SS, line(pts), ' stroke-linejoin="round"')


@glyph(29)
def g29(m):  # Line with event notes: a line with an event marked where it falls, and its note
    pts = [(5, 42), (15, 38), (25, 40), (35, 33), (45, 35), (55, 24), (65, 27), (75, 17), (84, 20)]
    return (BASE + P(SC, "M55 21V9") + textlines(58, 8, [22, 14]) + series(pts) + P(FS, dots([(55, 24)], 3)))


def wiggle(seed, n=9, x0=5, x1=84, base=30, amp=10, trend=0.0):
    pts = []
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        y = base - trend * i / (n - 1) + amp * math.sin(i * 1.7 + seed) * 0.6 + amp * math.cos(i * 0.9 + 2 * seed) * 0.4
        pts.append((x, y))
    return pts


@glyph(30)
def g30(m):  # Multi-line with one highlighted: a few lines in the context ink, one in the subject ink
    ctx = [wiggle(s, base=b, amp=5) for s, b in ((0.3, 18), (1.7, 28), (2.9, 38))]
    return BASE + P(SC, "".join(line(p) for p in ctx), ' stroke-linejoin="round"') + series(wiggle(4.2, base=34, amp=6, trend=22))


@glyph(31)
def g31(m):  # Line field with highlight: many lines in a light ink, one in the subject ink
    ctx = [wiggle(s, base=b, amp=4, trend=t) for s, b, t in
           ((0.2, 16, 4), (0.9, 22, 8), (1.6, 26, 2), (2.3, 30, 10), (3.1, 34, 6), (3.8, 38, 12), (4.6, 42, 8), (5.2, 46, 4))]
    return BASE + P(SL, "".join(line(p) for p in ctx), ' stroke-linejoin="round"') + series(wiggle(6.1, base=40, amp=4, trend=26))


@glyph(32)
def g32(m):  # Columns with a moving average: columns, and a line that smooths them
    hs = [14, 22, 12, 26, 18, 30, 20, 33, 25, 36, 28]
    xs = [6 + 7 * i for i in range(11)]
    avg = []
    for i in range(len(hs)):
        w = hs[max(0, i - 2):i + 1]
        avg.append((xs[i] + 2.5, 50 - sum(w) / len(w)))
    return P(FC, rects([(x, 50 - h, 5, h) for x, h in zip(xs, hs)])) + BASE + series(avg)


@glyph(33)
def g33(m):  # Sparkline: a word-sized line that sits in a sentence
    out = textlines(5, 18, [26]) + textlines(5, 38, [18])
    s1 = [(35, 21), (41, 18), (47, 19), (53, 15), (59, 16), (65, 12), (70, 10)]
    s2 = [(27, 35), (33, 37), (39, 36), (45, 40), (51, 39), (57, 42), (62, 43)]
    return (out + textlines(78, 18, [6]) + textlines(70, 38, [14]) + series(s1) + series(s2)
            + P(FS, dots([(70, 9), (62, 44)], 2.5)))


@glyph(34)
def g34(m):  # Small-multiple area sparklines: one small area a panel, on one scale
    out_a, out_l, base = "", "", ""
    for k in range(6):
        x0, y0 = 4 + 28 * (k % 3), 6 + 24 * (k // 3)
        top = [(x0 + 3 * i, y0 + 18 - (5 + 6 * abs(math.sin(i * 0.8 + k)) + i * 0.6)) for i in range(9)]
        out_a += area(top, y0 + 19)
        out_l += line(top)
        base += f"M{x0} {y0 + 20}h24"
    return P(FL, out_a) + P(SS, out_l, ' stroke-linejoin="round"') + P(SS, base)


@glyph(35)
def g35(m):  # Area chart: one series filled down to zero
    top = [(5, 38), (15, 34), (25, 36), (35, 28), (45, 30), (55, 22), (65, 25), (75, 16), (84, 18)]
    return P(FL, area(top, 50)) + BASE + series(top)


@glyph(36)
def g36(m):  # Step line: a value that holds, then jumps
    pts = [(5, 40), (20, 40), (20, 32), (38, 32), (38, 36), (52, 36), (52, 22), (70, 22), (70, 14), (84, 14)]
    return BASE + P(SS, line(pts), ' stroke-linejoin="miter"')


@glyph(37)
def g37(m):  # Line with a data gap marked: the line breaks where no figure exists, and the gap is shaded
    a = [(5, 36), (13, 32), (21, 34), (29, 28), (37, 30), (44, 26)]
    b = [(56, 24), (64, 20), (72, 23), (84, 16)]
    return P(FG, rects([(47, 6, 6, 44)])) + BASE + series(a) + series(b)


@glyph(38)
def g38(m):  # Timeline: dated events along one line, each with its note
    xs = [10, 28, 50, 72]
    out = P(SS, "M4 30H84") + P(SC, "M10 28V17M50 28V17M28 32V43M72 32V43")
    out += textlines(12, 12, [16]) + textlines(52, 12, [18]) + textlines(30, 47, [16]) + textlines(64, 47, [18])
    return out + P(FS, dots([(x, 30) for x in xs], 3.5))


@glyph(39)
def g39(m):  # Implementation timeline: each part's start, its run in force and its deadline
    rows = [(12, 30, 52), (26, 22, 66), (40, 46, 78)]
    out = P(SG, "M10 4V52")
    out += P(FC, rects([(a, y - 3, b - a, 6) for y, a, b in rows]))
    out += P(FL, rects([(b, y - 3, (c - 3) - b, 6) for y, a, b, c in [(r[0], 10, r[1], r[2]) for r in rows]]))
    out += P(FS, "".join(line([(c, y - 5), (c + 5, y), (c, y + 5), (c - 5, y)], True) for y, a, c in rows))
    return out


@glyph(40)
def g40(m):  # Indexed line: every line starts at 100 together, and moves from there
    o = (5, 30)
    ctx = [[o, (25, 26), (45, 28), (65, 22), (84, 24)], [o, (25, 33), (45, 36), (65, 38), (84, 42)],
           [o, (25, 30), (45, 33), (65, 31), (84, 34)]]
    return (P(SC, "M5 30H84", ' stroke-dasharray="3 3"') + P(SC, "".join(line(p) for p in ctx), ' stroke-linejoin="round"')
            + series([o, (25, 24), (45, 20), (65, 12), (84, 6)]) + P(FS, dots([o], 3)))


@glyph(41)
def g41(m):  # Bubble timeline: one circle a period, its area the count
    cs = [(7, 3), (18, 5), (34, 8), (51, 5), (66, 8), (80, 4)]
    return P(SC, "M4 30H84") + P(FL, dots_r([(x, 30, r) for x, r in cs])) + P(SS, dots_r([(x, 30, r) for x, r in cs]))


@glyph(42)
def g42(m):  # Benefit-cliff line: the line rises, drops where a benefit ends, and climbs again
    return (BASE + P(SC, "M5 46L84 12", ' stroke-dasharray="3 3"')
            + P(SS, line([(5, 46), (48, 22), (48, 38), (84, 22)]), ' stroke-linejoin="miter"'))


@glyph(43)
def g43(m):  # Run chart: points over time around their median, with a run marked
    pts = [(6, 34), (12, 26), (18, 36), (24, 28), (30, 38), (36, 30), (42, 22), (48, 18), (54, 24), (60, 16), (66, 26),
           (72, 34), (78, 28), (84, 36)]
    return (P(FG, rects([(39, 10, 30, 32)])) + P(SC, "M4 30H84", ' stroke-dasharray="3 3"') + series(pts)
            + P(FS, dots(pts, 2)) + P(SS, "M4 51H84"))


@glyph(44)
def g44(m):  # Cycle or seasonal chart: each year's line across the same months, this year picked out
    def hump(sh, h):
        return curve(lambda x: 44 - h * math.exp(-((x - 44 - sh) / 18) ** 2), 5, 84, 4)
    return (BASE + P(SC, line(hump(-6, 20)) + line(hump(4, 24)), ' stroke-linejoin="round"') + series(hump(0, 32)))


@glyph(45)
def g45(m):  # Streamgraph: layers stacked around a moving center (to avoid)
    xs = frange(5, 84, 3)
    c = lambda x: 29 + 4 * math.sin(x / 14)
    t1 = lambda x: 5 + 3 * math.sin(x / 10 + 1)
    t2 = lambda x: 6 + 4 * math.cos(x / 12)
    t3 = lambda x: 5 + 3 * math.sin(x / 9 + 2)
    top = [(x, c(x) - t1(x) - t2(x) / 2) for x in xs]
    mid1 = [(x, c(x) - t2(x) / 2) for x in xs]
    mid2 = [(x, c(x) + t2(x) / 2) for x in xs]
    bot = [(x, c(x) + t2(x) / 2 + t3(x)) for x in xs]
    return P(FS, band(top, mid1)) + P(FL, band(mid1, mid2)) + P(FC, band(mid2, bot))


# --- Composition: what is it made of? -----------------------------------------------------------------------------------

@glyph(46)
def g46(m):  # 100 percent bar: each bar the whole, split into its parts
    splits = [(34, 26), (46, 18), (22, 30), (40, 24)]
    out_s, out_c, out_l = [], [], []
    for i, (a, b) in enumerate(splits):
        y = 6 + 12 * i
        out_s.append((5, y, a, 8))
        out_c.append((5 + a + 2, y, b, 8))
        out_l.append((5 + a + b + 4, y, 79 - a - b - 4, 8))
    return P(FS, rects(out_s)) + P(FC, rects(out_c)) + P(FL, rects(out_l))


@glyph(47)
def g47(m):  # Stacked share bar with a midline: two shares a bar, and the line at half
    splits = [52, 30, 61, 44, 37]
    out_c, out_l = [], []
    for i, a in enumerate(splits):
        y = 7 + 9 * i
        out_c.append((5, y, a - 1, 6))
        out_l.append((5 + a + 1, y, 78 - a, 6))
    return P(FC, rects(out_c)) + P(FL, rects(out_l)) + P(SS, "M44 3V53")


@glyph(48)
def g48(m):  # Waterfall: a start, the steps up and down, and the total
    out = P(FS, rects([(6, 22, 9, 28), (73, 14, 9, 36)]))
    out += P(FC, rects([(17, 14, 9, 8), (28, 10, 9, 4)]))
    out += P(FL, rects([(39, 10, 9, 10), (50, 20, 9, 6)]))
    out += P(FC, rects([(61, 14, 9, 12)]))
    return out + BASE


@glyph(49)
def g49(m):  # Unit chart or waffle: one square a unit, a share of them filled
    on, off = [], []
    k = 0
    for c in range(10):
        for r in range(5):
            (on if k < 23 else off).append((5 + 8 * c, 8 + 8 * (4 - r), 6, 6))
            k += 1
    return P(FS, rects(on)) + P(FL, rects(off))


@glyph(50)
def g50(m):  # Stacked column: each column split into its parts
    cols = [(18, 8, 6), (22, 10, 8), (16, 12, 10), (26, 10, 8), (24, 14, 6), (30, 12, 6)]
    a, b, c = [], [], []
    for i, (h1, h2, h3) in enumerate(cols):
        x = 9 + 13 * i
        a.append((x, 50 - h1, 8, h1))
        b.append((x, 50 - h1 - 2 - h2, 8, h2))
        c.append((x, 50 - h1 - h2 - 4 - h3, 8, h3))
    return P(FS, rects(a)) + P(FC, rects(b)) + P(FL, rects(c)) + BASE


@glyph(51)
def g51(m):  # Stacked area: the parts' areas stacked up to the whole
    xs = frange(5, 84, 4)
    l1 = [(x, 50 - (10 + 6 * (x - 5) / 79 + 2 * math.sin(x / 9))) for x in xs]
    l2 = [(x, y - (8 + 5 * (x - 5) / 79 + 2 * math.cos(x / 11))) for x, y in l1]
    l3 = [(x, y - (6 + 8 * (x - 5) / 79)) for x, y in l2]
    return (P(FS, area(l1, 50)) + P(FC, band(l2, l1)) + P(FL, band(l3, l2)) + BASE)


@glyph(52)
def g52(m):  # Treemap: one box a part, its area the amount
    return (P(FS, rects([(5, 5, 40, 46)])) + P(FC, rects([(47, 5, 36, 20), (47, 27, 18, 24)]))
            + P(FL, rects([(67, 27, 16, 11), (67, 40, 16, 11)])))


@glyph(53)
def g53(m):  # Parliament chart: one dot a seat, in rows of a half circle
    cx, cy = 44, 49
    seats = []
    for r in (17, 25, 33, 41):
        k = max(int(math.pi * r / 6.6), 2)
        for i in range(k + 1):
            a = math.pi + math.pi * i / k
            seats.append((a, cx + r * math.cos(a), cy + r * math.sin(a)))
    seats.sort()
    cut = int(len(seats) * 0.54)
    return P(FS, dots([(x, y) for a, x, y in seats[:cut]], 2.6)) + P(FC, dots([(x, y) for a, x, y in seats[cut:]], 2.6))


@glyph(54)
def g54(m):  # Pie: a circle cut into a few parts of a whole
    cx, cy, r = 44, 29, 23
    a0 = -math.pi / 2
    s = [0.55, 0.30, 0.15]
    cuts = [a0, a0 + 2 * math.pi * s[0], a0 + 2 * math.pi * (s[0] + s[1]), a0 + 2 * math.pi]
    return (P(FS, wedge(cx, cy, 0, r, cuts[0], cuts[1])) + P(FC, wedge(cx, cy, 0, r, cuts[1], cuts[2]))
            + P(FL, wedge(cx, cy, 0, r, cuts[2], cuts[3])))


@glyph(55)
def g55(m):  # Donut with a center number: a ring cut into parts, with the figure in its hole
    cx, cy = 44, 29
    a0 = -math.pi / 2
    a1 = a0 + 2 * math.pi * 0.64
    return (P(FS, wedge(cx, cy, 15, 23, a0, a1, 32)) + P(FL, wedge(cx, cy, 15, 23, a1, a0 + 2 * math.pi, 18))
            + P(FS, rects([(37, 24, 14, 6)])) + textlines(39, 34, [10]))


@glyph(56)
def g56(m):  # Marimekko: columns as wide as their group, each split into its parts
    cols = [(5, 38, 0.42), (45, 22, 0.70), (69, 14, 0.55)]
    a, b = [], []
    for x, w, s in cols:
        h = 46 * s
        a.append((x, 51 - h, w, h))
        b.append((x, 5, w, 46 - h - 2))
    return P(FS, rects(a)) + P(FL, rects(b))


@glyph(57)
def g57(m):  # 3D pie or bar: a pie tilted, with a side (to avoid)
    cx, cy, rx, ry, dep = 44, 22, 32, 14, 10
    ell = lambda a: (cx + rx * math.cos(a), cy + ry * math.sin(a))
    side = [ell(math.pi * i / 24) for i in range(25)]
    side_d = line(side + [(x, y + dep) for x, y in reversed(side)], True)
    top_l = line([(cx, cy)] + [ell(math.pi / 2 + math.pi * i / 24) for i in range(25)] + [(cx, cy)], True)
    top_r = line([(cx, cy)] + [ell(-math.pi / 2 + math.pi * i / 24) for i in range(25)], True)
    return P(FC, side_d) + P(FS, top_l) + P(FL, top_r)


# --- Distribution and density: how are the values spread? ---------------------------------------------------------------

@glyph(58)
def g58(m):  # Histogram: counts in equal bins, the bars touching
    hs = [5, 12, 22, 33, 40, 36, 27, 19, 12, 7]
    return P(FC, rects([(4 + 8 * i, 50 - h, 7, h) for i, h in enumerate(hs)])) + BASE


@glyph(59)
def g59(m):  # Beeswarm or strip plot: one dot an item along one scale, pushed apart where they bunch
    counts = [1, 2, 3, 5, 6, 5, 4, 3, 2, 2, 1, 1]
    pts = []
    for i, c in enumerate(counts):
        x = 10 + 6 * i
        for j in range(c):
            pts.append((x + (3 if j % 2 else 0), 30 + (j - (c - 1) / 2) * 6))
    ends = [pts[0], pts[-1]]
    return P(FC, dots([p for p in pts if p not in ends], 2.6)) + P(FS, dots(ends, 2.6)) + P(SS, "M4 51H84")


@glyph(60)
def g60(m):  # Box plot: the middle half as a box, the median across it, the range as whiskers
    boxes = [(20, 10, 18, 28, 36, 46), (44, 6, 14, 22, 30, 40), (68, 16, 24, 30, 38, 48)]
    out_w, out_b, out_m = [], "", []
    for x, lo, q1, med, q3, hi in boxes:
        out_w += [[(x, lo), (x, q1)], [(x, q3), (x, hi)], [(x - 4, lo), (x + 4, lo)], [(x - 4, hi), (x + 4, hi)]]
        out_b += line([(x - 7, q1), (x + 7, q1), (x + 7, q3), (x - 7, q3)], True)
        out_m.append([(x - 7, med), (x + 7, med)])
    return P(SC, lines(out_w)) + P(FL, out_b) + P(SS, out_b) + P(SS, lines(out_m))


@glyph(61)
def g61(m):  # Line histogram: the bins' tops drawn as one stepped line, two groups compared
    def steps(hs, x0=4, w=8):
        pts = [(x0, 50)]
        for i, h in enumerate(hs):
            pts += [(x0 + w * i, 50 - h), (x0 + w * (i + 1), 50 - h)]
        return pts + [(x0 + w * len(hs), 50)]
    return (BASE + P(SC, line(steps([4, 9, 16, 26, 30, 24, 15, 9, 5, 3])), ' stroke-linejoin="miter"')
            + P(SS, line(steps([2, 4, 8, 13, 20, 28, 34, 26, 14, 6])), ' stroke-linejoin="miter"'))


@glyph(62)
def g62(m):  # Population pyramid: two groups' bars back to back, youngest at the bottom
    left = [34, 32, 29, 26, 21, 15, 8]
    right = [33, 31, 29, 27, 23, 18, 11]
    return (P(FS, rects([(43 - w, 45 - 6 * i, w, 5) for i, w in enumerate(left)]))
            + P(FC, rects([(45, 45 - 6 * i, w, 5) for i, w in enumerate(right)])))


@glyph(63)
def g63(m):  # Violin: each group's spread drawn as a mirrored shape
    out = ""
    for x, sh in ((20, 0.0), (44, 0.8), (68, 1.6)):
        prof = [(y, 1.5 + 9 * math.exp(-((y - 28 - 6 * math.sin(sh)) / (8 + 2 * sh)) ** 2) + 2 * math.exp(-((y - 42) / 4) ** 2))
                for y in frange(8, 48, 2)]
        right = [(x + w, y) for y, w in prof]
        left = [(x - w, y) for y, w in reversed(prof)]
        out += line(right + left, True)
    return P(FL, out) + P(FS, rects([(19, 22, 2, 12), (43, 20, 2, 14), (67, 24, 2, 12)]))


@glyph(64)
def g64(m):  # Ridgeline: one group's spread per row, each row overlapping the one above
    out = ""
    for i in range(4):
        y0 = 22 + 9 * i
        top = curve(lambda x: y0 - 16 * math.exp(-((x - 40 - 6 * i) / (9 + i)) ** 2), 8, 84, 3)
        d = area(top, y0)
        out += P(FS if i == 3 else FL, d) + P(SS if i == 3 else SC, line(top), ' stroke-linejoin="round"')
    return out


def hexagon(cx, cy, r):
    return line([(cx + r * math.cos(math.pi / 6 + k * math.pi / 3), cy + r * math.sin(math.pi / 6 + k * math.pi / 3))
                 for k in range(6)], True)


@glyph(65)
def g65(m):  # Hexbin: points counted into hexagons, each shaded by its count
    by = {M2: "", M3: "", M4: ""}
    r = 4.6
    for row in range(-3, 4):
        for col in range(-6, 7):
            cx = 44 + col * r * math.sqrt(3) + (row % 2) * r * math.sqrt(3) / 2
            cy = 30 + row * r * 1.5
            d = abs((cy - 30) + (cx - 44) * 0.45)
            if d > 11 or not (6 < cx < 82):
                continue
            v = 1 - d / 11 - abs(cx - 44) / 70
            by[M4 if v > 0.55 else M3 if v > 0.3 else M2] += hexagon(cx, cy, r - 0.8)
    return "".join(P(c, d) for c, d in by.items())


@glyph(66)
def g66(m):  # Contour or density: rings around where points bunch, the densest inside
    def ell(rx, ry):
        a = -0.45
        return line([(44 + rx * math.cos(t) * math.cos(a) - ry * math.sin(t) * math.sin(a),
                      29 + rx * math.cos(t) * math.sin(a) + ry * math.sin(t) * math.cos(a))
                     for t in [2 * math.pi * k / 36 for k in range(36)]], True)
    return (P(M2, ell(34, 17)) + P(M3, ell(22, 11)) + P(M4, ell(11, 6))
            + P(FS, dots([(10, 16), (78, 12), (82, 40), (14, 46), (64, 52), (30, 6)], 1.8)))


# --- Correlation: do two things move together? ---------------------------------------------------------------------------

AXES = P(SG, "M5 4V51") + BASE


@glyph(67)
def g67(m):  # Scatter plot with named points: one dot an item on two scales, a few named
    pts = [(10, 44), (16, 40), (20, 43), (26, 36), (30, 38), (34, 31), (40, 34), (44, 28), (50, 30), (56, 24), (60, 27),
           (66, 20), (72, 22)]
    named = [(22, 24), (78, 12)]
    return (AXES + P(FC, dots(pts, 2.6)) + P(FS, dots(named, 3)) + textlines(28, 24, [14]) + textlines(56, 12, [16]))


@glyph(68)
def g68(m):  # Bubble chart: a scatter whose circles show a third value by their area
    cs = [(14, 40, 4), (26, 32, 7), (42, 36, 5), (54, 22, 10), (72, 16, 6), (70, 38, 3)]
    return AXES + P(FL, dots_r(cs)) + P(SS, dots_r(cs))


@glyph(69)
def g69(m):  # Connected scatter: points on two scales joined in time order
    pts = [(12, 42), (22, 36), (30, 40), (40, 30), (52, 34), (60, 22), (54, 14), (68, 10), (80, 16)]
    return (AXES + P(SC, line(pts), ' stroke-linejoin="round"') + P(FC, dots(pts[:-1], 2.6))
            + P(FS, dots([pts[-1]], 3.5)))


@glyph(70)
def g70(m):  # Correlogram: a grid of pairs, each cell shaded by how closely the pair moves together
    order = [M4, M3, M2, M3, M2, M4, M2, M3, M4, M3]
    by = {M2: [], M3: [], M4: []}
    diag = []
    k = 0
    for r in range(5):
        for c in range(5):
            x, y = 21 + 10 * c, 4 + 10 * r
            if c == r:
                diag.append((x, y, 8, 8))
            elif c > r:
                by[order[k % len(order)]].append((x, y, 8, 8))
                k += 1
    return "".join(P(cl, rects(v)) for cl, v in by.items()) + P(SC, "".join(rects([(x + 1, y + 1, 6, 6)]) for x, y, w, h in diag))


@glyph(71)
def g71(m):  # Pair plot: every pair of measures as a small scatter, each measure's spread on the diagonal
    out_box, out_bar, out_dot = "", [], []
    for r in range(3):
        for c in range(3):
            x, y = 20 + 17 * c, 4 + 17 * r
            out_box += f"M{x} {y}h14v14h-14z"
            if r == c:
                for i, h in enumerate([4, 9, 6]):
                    out_bar.append((x + 2 + 4 * i, y + 12 - h, 3, h))
            else:
                sl = 1 if (r + c) % 2 else -1
                for i in range(4):
                    out_dot.append((x + 3 + 2.7 * i, y + 7 - sl * (2.5 * i - 3.5) + (1 if i % 2 else -1)))
    return P(SG, out_box) + P(FC, rects(out_bar)) + P(FS, dots(out_dot, 1.4))


@glyph(72)
def g72(m):  # Trajectory or speed chart: one dot a year along a path, the gaps showing the speed
    ts = [0, 0.04, 0.1, 0.2, 0.33, 0.48, 0.62, 0.74, 0.84, 0.92, 1.0]
    pts = [(8 + 74 * t, 46 - 36 * math.sin(math.pi * t * 0.92)) for t in ts]
    return (P(SC, line(pts), ' stroke-linejoin="round"') + P(FC, dots(pts[1:-1], 2.2))
            + P(FS, dots([pts[0], pts[-1]], 3.5)))


@glyph(73)
def g73(m):  # Dual-axis line: two lines on two different scales (to avoid)
    ticks = "".join(f"M5 {y}h-3M83 {y}h3" for y in (12, 24, 36, 48))
    return (P(SC, "M5 4V51M83 4V51" + ticks) + BASE
            + P(SC, line([(5, 22), (25, 24), (45, 22), (65, 26), (83, 24)]), ' stroke-dasharray="4 3"')
            + series([(5, 44), (25, 38), (45, 30), (65, 22), (83, 12)]))


# --- Uncertainty and estimates: how sure is it? ---------------------------------------------------------------------------

@glyph(74)
def g74(m):  # Range bar or error bar: each estimate with the range around it
    rows = [(52, 18), (44, 14), (38, 20), (30, 12), (22, 16)]
    segs, caps, mids = [], [], []
    for i, (x, w) in enumerate(rows):
        y = 8 + 10 * i
        segs.append([(x - w, y), (x + w, y)])
        caps += [[(x - w, y - 3), (x - w, y + 3)], [(x + w, y - 3), (x + w, y + 3)]]
        mids.append((x, y))
    return P(SC, lines(segs + caps)) + P(FS, dots(mids, 3))


@glyph(75)
def g75(m):  # Confidence band on a line: a band for the range around the line
    xs = frange(5, 84, 4)
    mid = [(x, 38 - 0.28 * (x - 5) + 3 * math.sin(x / 8)) for x in xs]
    w = lambda x: 3 + 7 * (x - 5) / 79
    return P(FL, band([(x, y - w(x)) for x, y in mid], [(x, y + w(x)) for x, y in mid])) + BASE + series(mid)


@glyph(76)
def g76(m):  # Scenario directions: each scenario's direction on each outcome, as an arrow in its cell
    out_up, out_dn, out_flat = "", "", []
    marks = ["u", "d", "f", "u", "f", "u", "u", "d", "f", "f", "u", "f"]
    k = 0
    for r in range(3):
        for c in range(4):
            x, y = 28 + 15 * c, 12 + 15 * r
            mk = marks[k]
            k += 1
            if mk == "u":
                out_up += line([(x, y - 4), (x + 5, y + 3), (x - 5, y + 3)], True)
            elif mk == "d":
                out_dn += line([(x, y + 4), (x + 5, y - 3), (x - 5, y - 3)], True)
            else:
                out_flat.append([(x - 5, y), (x + 5, y)])
    return (textlines(4, 12, [14, 10, 12], 15) + P(SG, "M21 5H86M21 20H86M21 35H86M21 50H86")
            + P(FS, out_up) + P(FC, out_dn) + P(SS, lines(out_flat)))


@glyph(77)
def g77(m):  # Fan chart: the line so far, then bands that widen into the future
    past = [(5, 40), (14, 36), (23, 38), (32, 31), (41, 33), (48, 28)]
    xs = frange(48, 84, 4)
    c = lambda x: 28 - 0.25 * (x - 48)
    w1 = lambda x: 0.32 * (x - 48)
    w2 = lambda x: 0.6 * (x - 48)
    return (P(FG, band([(x, c(x) - w2(x)) for x in xs], [(x, c(x) + w2(x)) for x in xs]))
            + P(FL, band([(x, c(x) - w1(x)) for x in xs], [(x, c(x) + w1(x)) for x in xs])) + BASE
            + series(past) + P(SS, line([(x, c(x)) for x in xs]), ' stroke-dasharray="3 3"'))


@glyph(78)
def g78(m):  # Hypothetical outcomes: the same chart drawn for several possible outcomes
    hs = [26, 14, 30, 20, 11, 24]
    boxes, bars = "", []
    for k, h in enumerate(hs):
        x, y = 6 + 27 * (k % 3), 4 + 25 * (k // 3)
        boxes += f"M{x} {y}h22v22h-22z"
        bars.append((x + 8, y + 22 - h * 0.7, 6, h * 0.7))
    thr = "".join(f"M{6 + 27 * (k % 3) + 3} {4 + 25 * (k // 3) + 10}h16" for k in range(6))
    return P(SG, boxes) + P(FC, rects(bars)) + P(SS, thr, ' stroke-dasharray="2 2"')


# --- Proportion and overlap: how much, and how do groups overlap? ---------------------------------------------------------

def person(x, y):
    """A small figure 6 px wide: head and shoulders."""
    return dots([(x + 3, y + 2)], 2) + f"M{x} {y + 11}v-3a3 3 0 0 1 3 -3a3 3 0 0 1 3 3v3z"


@glyph(79)
def g79(m):  # Icon array with Civic Line icons: one figure a person, a share of them filled
    on, off = "", ""
    k = 0
    for r in range(3):
        for c in range(10):
            if k < 12:
                on += person(5 + 8 * c, 8 + 15 * r)
            else:
                off += person(5 + 8 * c, 8 + 15 * r)
            k += 1
    return P(FS, on) + P(FL, off)


@glyph(80)
def g80(m):  # Proportional symbols: circles whose areas compare counts far apart
    cs = [(24, 31, 20), (58, 37, 14), (79, 45, 6)]
    return P(FL, dots_r(cs)) + P(SS, dots_r(cs))


@glyph(81)
def g81(m):  # Venn diagram: two groups as circles, their overlap shaded
    r, c1, c2 = 19, 33, 55
    dx = (c2 - c1) / 2
    hh = math.sqrt(r * r - dx * dx)
    lens = f"M44 {f(29 - hh)}a{r} {r} 0 0 1 0 {f(2 * hh)}a{r} {r} 0 0 1 0 {f(-2 * hh)}z"
    return P(FL, lens) + P(SS, dots([(c1, 29), (c2, 29)], r))


@glyph(82)
def g82(m):  # Euler diagram: two groups drawn at their true sizes, one partly inside the other
    R, r, X, x = 22, 10, 36, 58
    d = x - X
    a = (d * d + R * R - r * r) / (2 * d)
    hh = math.sqrt(R * R - a * a)
    px = X + a
    lens = (f"M{f(px)} {f(29 - hh)}a{r} {r} 0 0 1 0 {f(2 * hh)}a{R} {R} 0 0 1 0 {f(-2 * hh)}z")
    return P(FL, lens) + P(SS, dots_r([(X, 29, R), (x, 29, r)]))


@glyph(83)
def g83(m):  # Packed circles or bubble cloud: circles packed together, sized by amount
    cs = [(40, 30, 14), (63, 22, 9), (64, 41, 8), (20, 22, 8), (21, 42, 7), (46, 8, 5), (79, 32, 5), (8, 32, 4),
          (42, 51, 4)]
    return P(FL, dots_r(cs)) + P(SC, dots_r(cs))


@glyph(84)
def g84(m):  # Rose chart: wedges of equal angle whose lengths show the values (to avoid)
    cx, cy = 44, 30
    rs = [22, 13, 8, 17]
    out = ""
    for i, r in enumerate(rs):
        a0 = -math.pi / 2 + i * math.pi / 2 + 0.05
        out += wedge(cx, cy, 0, r, a0, a0 + math.pi / 2 - 0.1, 12)
    return P(FC, out)


# --- Gauges and indicators: where does it stand now? ----------------------------------------------------------------------

@glyph(85)
def g85(m):  # Big number in context: one figure set large, its words, and a small comparison beside it
    return (P(FS, rects([(5, 8, 34, 18)])) + textlines(5, 34, [32, 24, 28])
            + P(FT, rects([(48, 12, 36, 6), (48, 28, 36, 6)])) + P(FS, rects([(48, 12, 30, 6)])) + P(FC, rects([(48, 28, 21, 6)]))
            + textlines(48, 7, [12]) + textlines(48, 23, [12]))


@glyph(86)
def g86(m):  # Indicator row: a few figures in a row, each with its words
    out = P(SG, "M4 19H84M4 37H84")
    out += P(FS, rects([(5, 5, 20, 8), (5, 23, 14, 8), (5, 41, 24, 8)]))
    return out + textlines(36, 6, [40, 32]) + textlines(36, 24, [44, 26]) + textlines(36, 42, [38, 30])


@glyph(87)
def g87(m):  # Progress bar: the share done along a track, with the target marked
    return (P(FG, rects([(5, 14, 78, 8), (5, 36, 78, 8)])) + P(FS, rects([(5, 14, 58, 8), (5, 36, 30, 8)]))
            + P(SS, "M70 10V26M70 32V48") + textlines(5, 7, [16]) + textlines(5, 29, [20]))


@glyph(88)
def g88(m):  # Step tracker: the six steps in order, those done filled, the rest open
    xs = [8, 22, 36, 50, 64, 78]
    return (P(SS, "M8 24H36") + P(SC, "M36 24H46M54 24H60M68 24H74") + P(FS, dots([(x, 24) for x in xs[:3]], 4.5))
            + P(SS, dots([(x, 24) for x in xs[3:]], 4)) + textlines(4, 40, [36]) + textlines(4, 45, [24]))


def pill(x, y, w, h=10):
    r = h / 2
    return f"M{f(x + r)} {f(y)}h{f(w - h)}a{f(r)} {f(r)} 0 0 1 0 {f(h)}h{f(-(w - h))}a{f(r)} {f(r)} 0 0 1 0 {f(-h)}z"


@glyph(89)
def g89(m):  # Status chips: each item's state in a small labeled chip beside its words
    return (P(FS, pill(5, 8, 26)) + P(SS, pill(6, 24, 24, 8) + pill(6, 40, 24, 8))
            + textlines(12, 28, [12]) + textlines(12, 44, [12])
            + textlines(38, 11, [44, 30]) + textlines(38, 27, [40, 26]) + textlines(38, 43, [46, 22]))


@glyph(90)
def g90(m):  # Bullet graph: one measure as a bar over the ranges that judge it, with its target
    out = ""
    for y in (12, 34):
        out += P(FG, rects([(5, y, 78, 12)])) + P(FL, rects([(5, y, 52, 12)]))
    return (out + P(FS, rects([(5, 16, 46, 4), (5, 38, 62, 4)])) + P(SS, "M64 10V26M58 32V48"))


@glyph(91)
def g91(m):  # Gauge: a dial with a needle (to avoid)
    cx, cy = 44, 46
    a0, a1 = math.pi, 2 * math.pi
    av = a0 + (a1 - a0) * 0.68
    return (P(FL, wedge(cx, cy, 25, 33, av, a1)) + P(FS, wedge(cx, cy, 25, 33, a0, av))
            + P(SS, line([(cx, cy), (cx + 21 * math.cos(av), cy + 21 * math.sin(av))])) + P(FS, dots([(cx, cy)], 3)))


@glyph(92)
def g92(m):  # Thermometer: a tube filled to a level (to avoid)
    return (P(SS, "M39 39V9a5 5 0 0 1 10 0V39") + P(FS, rects([(42, 20, 4, 22)]) + dots([(44, 44)], 7))
            + P(SS, "M52 14h6") + textlines(60, 14, [14]))


# --- Behavior: how do people move through a process? ----------------------------------------------------------------------

@glyph(93)
def g93(m):  # Funnel: each stage narrower than the one before
    ws = [78, 62, 46, 32, 20]
    return P(FC, rects([(44 - w / 2, 6 + 9 * i, w, 7) for i, w in enumerate(ws[:-1])])) + P(FS, rects([(44 - 10, 42, 20, 7)]))


@glyph(94)
def g94(m):  # Cohort chart: each group followed from the same start, the newest shortest
    o = (8, 8)
    curves = [[o, (24, 26), (44, 34), (64, 40), (84, 44)], [o, (24, 22), (44, 30), (64, 36)], [o, (24, 18), (44, 26)]]
    return (P(SG, "M8 20H84M8 32H84M8 44H84") + P(SC, "".join(line(c) for c in curves[:2]), ' stroke-linejoin="round"')
            + series(curves[2]) + P(FS, dots([o], 3)) + P(SS, "M8 4V51"))


@glyph(95)
def g95(m):  # Survival curve: the share still in, stepping down over time
    a = [(6, 8), (14, 8), (14, 13), (22, 13), (22, 19), (32, 19), (32, 26), (44, 26), (44, 30), (58, 30), (58, 34), (84, 34)]
    b = [(6, 8), (12, 8), (12, 16), (20, 16), (20, 26), (30, 26), (30, 34), (42, 34), (42, 40), (60, 40), (60, 44), (84, 44)]
    return (P(SS, "M6 4V51") + BASE + P(SC, line(b), ' stroke-linejoin="miter"') + P(SS, line(a), ' stroke-linejoin="miter"')
            + P(SS, "M38 23v6M70 31v6"))


# --- Structure: who decides, and how does it work? ------------------------------------------------------------------------

def box(x, y, w, h):
    return f"M{f(x)} {f(y)}h{f(w)}v{f(h)}h{f(-w)}z"


@glyph(96)
def g96(m):  # Process diagram: the steps as boxes, joined by arrows in order, with a branch
    b = box(5, 8, 20, 12) + box(34, 8, 20, 12) + box(63, 8, 20, 12) + box(34, 36, 20, 12)
    return (P(SS, b) + P(SC, "M26 14H28M55 14H57M44 21V30") + P(FC, head(33, 14, 1, 0, 5, 3) + head(62, 14, 1, 0, 5, 3)
            + head(44, 35, 0, 1, 5, 3)) + textlines(9, 14, [12]) + textlines(38, 14, [12]) + textlines(67, 14, [12])
            + textlines(38, 42, [12]))


@glyph(97)
def g97(m):  # Decision tree: a question at the top, each answer branching to the next
    b = box(34, 4, 20, 10) + box(8, 24, 20, 10) + box(60, 24, 20, 10)
    leaves = rects([(4, 44, 12, 8), (20, 44, 12, 8), (64, 44, 12, 8)])
    return (P(SS, "M44 15V19H18V23M44 19H70V23M18 35V39H10V43M18 39H26V43M70 35V43") + P(SS, b)
            + P(FC, leaves) + textlines(39, 9, [10]) + textlines(13, 29, [10]) + textlines(65, 29, [10]))


@glyph(98)
def g98(m):  # Who-decides diagram: the bodies at each level, those who make the rules above those who apply them
    out = P(SG, "M4 29H84") + textlines(6, 5, [10]) + textlines(28, 5, [10]) + textlines(50, 5, [10]) + textlines(72, 5, [10])
    out += P(SS, box(5, 11, 18, 12) + box(27, 11, 18, 12) + box(49, 11, 18, 12) + box(27, 37, 18, 12) + box(71, 37, 13, 12))
    out += P(SC, "M9 24V43H22")
    out += P(SS, line([(22, 43), (24.5, 40.5), (27, 43), (24.5, 45.5)], True))
    return out + textlines(9, 17, [10]) + textlines(31, 17, [10]) + textlines(53, 17, [10]) + textlines(31, 43, [10])


@glyph(99)
def g99(m):  # Org chart: who sits under whom, in boxes joined by lines
    return (P(FS, rects([(32, 4, 24, 10)])) + P(SC, "M44 15V20M14 20H74M14 20V25M44 20V25M74 20V25M44 36V40M34 40H54M34 40V43M54 40V43")
            + P(SS, box(4, 26, 20, 10) + box(34, 26, 20, 10) + box(64, 26, 20, 10) + box(26, 44, 16, 8) + box(46, 44, 16, 8)))


@glyph(100)
def g100(m):  # Hierarchy tree: a root branching to its parts, and theirs, left to right
    root = (8, 29)
    mids = [(34, 12), (34, 29), (34, 46)]
    leaves = [(62, 6), (62, 15), (62, 24), (62, 34), (62, 42), (62, 51)]
    pairs = [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4), (2, 5)]

    def link(a, b):
        mx = (a[0] + b[0]) / 2
        return f"M{f(a[0])} {f(a[1])}C{f(mx)} {f(a[1])} {f(mx)} {f(b[1])} {f(b[0])} {f(b[1])}"
    links = "".join(link(root, mm) for mm in mids) + "".join(link(mids[i], leaves[j]) for i, j in pairs)
    return (P(SC, links) + P(FS, dots([root], 4)) + P(FS, dots(mids, 3)) + P(FC, dots(leaves, 2.5))
            + textlines(68, 6, [14]) + textlines(68, 15, [10]) + textlines(68, 24, [16]) + textlines(68, 34, [12])
            + textlines(68, 42, [14]) + textlines(68, 51, [10]))


@glyph(101)
def g101(m):  # Comparison grid: options in rows, the same questions in columns, each cell's answer in words
    out = P(SG, "M4 14H84M4 27H84M4 40H84M28 5V52")
    out += P(SS, "M4 6H24") + textlines(32, 6, [12]) + textlines(52, 6, [12]) + textlines(72, 6, [10])
    for i, y in enumerate((20, 33, 46)):
        out += P(SS, f"M4 {y}h{16 - 2 * i}") + textlines(32, y, [14 - 2 * i]) + textlines(52, y, [10 + i])
        out += textlines(72, y, [8 + i])
    return out


@glyph(102)
def g102(m):  # Roll-call grid: one row a member, one square a vote, filled for yes
    yes, no = [], []
    pat = [0b11011101, 0b11111011, 0b10010110, 0b00100100, 0b11101111, 0b01001001]
    for r in range(6):
        for c in range(8):
            (yes if (pat[r] >> (7 - c)) & 1 else no).append((30 + 7 * c, 9 + 7 * r, 5, 5))
    return P(FS, rects(yes)) + P(FL, rects(no)) + textlines(5, 11.5, [18, 14, 20, 16, 18, 12], 7)


@glyph(103)
def g103(m):  # Mind map: one idea in the middle, its branches curving out to the parts
    out = P(SS, box(32, 23, 24, 11))
    br = ("M32 28C24 28 24 12 16 12M32 28C24 28 24 44 16 44M56 28C64 28 64 12 72 12M56 28C64 28 64 44 72 44")
    out += P(SC, br) + P(FC, dots([(16, 12), (16, 44), (72, 12), (72, 44)], 3))
    return out + textlines(37, 28.5, [14]) + textlines(4, 20, [12]) + textlines(4, 52, [12]) + textlines(72, 20, [12]) + textlines(72, 52, [12])


# --- Relationships: who is connected to whom? -----------------------------------------------------------------------------

@glyph(104)
def g104(m):  # Network diagram: people or groups as dots, the links between them as lines
    nodes = [(14, 14), (12, 40), (32, 28), (48, 10), (54, 40), (74, 20), (78, 46), (34, 50)]
    edges = [(0, 2), (1, 2), (2, 3), (2, 4), (3, 5), (4, 5), (4, 6), (5, 6), (1, 7), (4, 7), (0, 3)]
    return (P(SC, lines([[nodes[a], nodes[b]] for a, b in edges])) + P(FC, dots([nodes[i] for i in (0, 1, 3, 6, 7)], 4))
            + P(FS, dots([nodes[i] for i in (2, 4, 5)], 5)))


@glyph(105)
def g105(m):  # Adjacency matrix: everyone in rows and in columns, a filled cell where two connect
    n = 6
    links = {(0, 1), (0, 3), (1, 2), (2, 4), (3, 4), (4, 5), (1, 5)}
    on, off = [], []
    for r in range(n):
        for c in range(n):
            cell = (34 + 8 * c, 5 + 8 * r, 7, 7)
            if r == c:
                continue
            ((on) if (min(r, c), max(r, c)) in links else off).append(cell)
    return P(FS, rects(on)) + P(FG, rects(off)) + textlines(8, 8.5, [20, 16, 22, 18, 14, 20], 8)


@glyph(106)
def g106(m):  # Arc diagram: the items on one line, an arc above for each link
    xs = [6, 18, 30, 42, 54, 66, 78]
    arcs = [(0, 3), (1, 2), (2, 5), (3, 4), (4, 6), (1, 6)]
    ctx = "".join(f"M{xs[a]} 44A{(xs[b] - xs[a]) / 2} {(xs[b] - xs[a]) / 2} 0 0 1 {xs[b]} 44" for a, b in arcs[:-1])
    a, b = arcs[-1]
    sub = f"M{xs[a]} 44A{(xs[b] - xs[a]) / 2} {(xs[b] - xs[a]) / 2} 0 0 1 {xs[b]} 44"
    return P(SC, ctx) + P(SS, sub) + P(FS, dots([(x, 44) for x in xs], 3))


@glyph(107)
def g107(m):  # Chord diagram: groups around a circle, bands across it for what flows between them (a reference form)
    cx, cy, r0, r1 = 44, 29, 19, 24
    segs = [(-1.4, -0.1), (0.05, 1.5), (1.65, 3.3), (3.45, 4.75)]
    out = "".join(wedge(cx, cy, r0, r1, a, b, 12) for a, b in segs)

    def rib(a0, a1, b0, b1):
        p = lambda a: (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p(a0), p(a1), p(b0), p(b1)
        return (f"M{f(x0)} {f(y0)}A{r0} {r0} 0 0 1 {f(x1)} {f(y1)}Q{cx} {cy} {f(x2)} {f(y2)}"
                f"A{r0} {r0} 0 0 1 {f(x3)} {f(y3)}Q{cx} {cy} {f(x0)} {f(y0)}z")
    return (P(FC, out) + P(FL, rib(0.2, 0.8, 3.6, 4.1) + rib(1.8, 2.4, 4.3, 4.6)) + P(FS, rib(-1.2, -0.4, 2.2, 3.0)))


@glyph(108)
def g108(m):  # Multi-network: the same people joined by more than one kind of link
    nodes = [(16, 12), (50, 8), (74, 30), (44, 48), (12, 42)]
    return (P(SS, lines([[nodes[0], nodes[1]], [nodes[1], nodes[2]], [nodes[2], nodes[3]], [nodes[4], nodes[0]]]))
            + P(SC, lines([[nodes[0], nodes[3]], [nodes[1], nodes[3]], [nodes[4], nodes[3]]]), ' stroke-dasharray="3 2"')
            + P(FL, dots(nodes, 4.5)) + P(SS, dots(nodes, 4.5)))


@glyph(109)
def g109(m):  # Symmetrical links: links that run both ways, each as wide as what the pair shares
    A, B, C, D = (12, 29), (44, 7), (44, 51), (76, 29)

    def wide(p, q, w):
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * w / 2, dx / L * w / 2
        return line([(p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny), (q[0] - nx, q[1] - ny), (p[0] - nx, p[1] - ny)], True)
    return (P(FC, wide(A, B, 6) + wide(C, D, 6)) + P(SC, lines([[A, C], [B, D], [B, C]]))
            + P(FL, dots([A, B, C, D], 5)) + P(SS, dots([A, B, C, D], 5)))


# --- Flow: where does it go? ----------------------------------------------------------------------------------------------

def flow(x0, a0, a1, x1, b0, b1):
    """A band from (x0, a0..a1) to (x1, b0..b1), its width kept."""
    mx = (x0 + x1) / 2
    return (f"M{f(x0)} {f(a0)}C{f(mx)} {f(a0)} {f(mx)} {f(b0)} {f(x1)} {f(b0)}V{f(b1)}"
            f"C{f(mx)} {f(b1)} {f(mx)} {f(a1)} {f(x0)} {f(a1)}z")


@glyph(110)
def g110(m):  # Sankey: amounts flowing from sources to uses, each band as wide as its amount
    out = P(FS, rects([(4, 6, 5, 24), (4, 34, 5, 16), (79, 4, 5, 14), (79, 22, 5, 16), (79, 42, 5, 10)]))
    bands = flow(9, 6, 18, 79, 4, 16) + flow(9, 18, 30, 79, 22, 34) + flow(9, 34, 40, 79, 34, 38) + flow(9, 40, 50, 79, 42, 52)
    return P(FL, bands) + out


@glyph(111)
def g111(m):  # Alluvial: groups at each stage, bands showing who moved between them (a reference form)
    out = P(FS, rects([(4, 4, 4, 16), (4, 22, 4, 14), (4, 38, 4, 14), (42, 4, 4, 12), (42, 18, 4, 18), (42, 38, 4, 14),
                       (80, 4, 4, 14), (80, 20, 4, 12), (80, 34, 4, 18)]))
    bands = (flow(8, 4, 16, 42, 4, 16) + flow(8, 16, 20, 42, 18, 22) + flow(8, 22, 36, 42, 22, 36) + flow(8, 38, 52, 42, 38, 52)
             + flow(46, 4, 16, 80, 4, 16) + flow(46, 18, 32, 80, 34, 48) + flow(46, 32, 36, 80, 20, 24) + flow(46, 38, 52, 80, 24, 32))
    return P(FL, bands) + P(FC, flow(46, 18, 32, 80, 34, 48)) + out


@glyph(112)
def g112(m):  # Journey map: one person's path through a process, stage by stage
    pts = [(10, 36), (30, 22), (50, 40), (70, 28)]
    return (P(SG, "M20 4V52M40 4V52M60 4V52") + textlines(5, 7, [12]) + textlines(25, 7, [12]) + textlines(45, 7, [12])
            + textlines(65, 7, [12]) + P(SC, line(pts + [(84, 18)]), ' stroke-linejoin="round"')
            + P(FS, dots(pts, 3.5)) + P(FS, head(84, 18, 1, -0.7, 5, 3.5)) + textlines(5, 48, [10]) + textlines(45, 50, [12]))


@glyph(113)
def g113(m):  # Flow map: arrows on a map from one place to others, each as wide as its flow (a reference form)
    land = m.land(FG)
    o = (22, 30)
    return (land
            + P(SS, "M22 30C40 12 58 10 72 16M22 30C44 34 60 38 74 40M22 30C26 40 30 46 36 48")
            + P(FS, head(74, 17, 1, 0.3, 5, 3.5) + head(76, 40.3, 1, 0.1, 5, 3.5) + head(37, 48.5, 1, 0.3, 5, 3.5) + dots([o], 3.5)))


# --- Maps: where is it happening? -----------------------------------------------------------------------------------------

def tile_cells():
    grid = json.loads(TILE_GRID.read_text())
    return {x["code"]: (x["col"], x["row"]) for x in grid}


def tile_xy(c, r, pitch=7, x0=3, y0=1):
    return x0 + pitch * c, y0 + pitch * r


@glyph(114)
def g114(m):  # Tile-grid map, categorical: one square a state, in its group's ink
    by = {FS: [], FC: [], FL: []}
    for code, (c, r) in sorted(tile_cells().items()):
        x, y = tile_xy(c, r)
        v = pattern(x * 1.3, y * 1.1, 0.7)
        by[FS if v > 0.62 else FC if v > 0.38 else FL].append((x, y, 6, 6))
    return "".join(P(k, rects(v)) for k, v in by.items())


@glyph(115)
def g115(m):  # Tile-grid map with shift arrows: one square a state, an arrow in each for the shift
    cells = sorted(tile_cells().items())
    out = P(FG, rects([(*tile_xy(c, r), 6, 6) for code, (c, r) in cells]))
    segs, heads = [], ""
    for code, (c, r) in cells:
        x, y = tile_xy(c, r)
        v = pattern(x, y, 1.9)
        if v < 0.3 or v > 0.75:
            continue
        segs.append([(x + 1, y + 3), (x + 4, y + 3)])
        heads += head(x + 7, y + 3, 1, 0, 3, 2.5)
    return out + P(SS, lines(segs)) + P(FS, heads)


@glyph(116)
def g116(m):  # Bubble map: a circle at each place, its area the count
    cs = [(70, 22, 7), (20, 30, 6), (44, 42, 5), (60, 30, 4), (76, 40, 3.5), (34, 18, 3), (54, 16, 4), (28, 40, 3)]
    return m.land(FG) + P(FL, dots_r(cs)) + P(SS, dots_r(cs))


@glyph(117)
def g117(m):  # Choropleth, sequential: each state shaded by its value, darker for more
    return m.choropleth([M2, M3, M4, FS]) + m.land(ST)


@glyph(118)
def g118(m):  # Locator map: where a place sits, picked out on the country
    return m.land(FL) + m.state("CO", FS) + P(SS, dots([(32.5, 24.5)], 7.5))


def sub_map(path, code, box, classes, k, tol=0.5):
    feats = sub_features(path, code)
    t = fit_rings([r for g, rs in feats for r in rs], box)
    by = {c: "" for c in classes}
    for g, rs in sorted(feats):
        rr = [t(r) for r in rs]
        cx, cy = centroid(rr)
        by[lerp_class(pattern(cx * 1.4, cy * 1.4, k), classes)] += ring_path(rr, tol, 0.3)
    outline = "".join(ring_path([t(r)], tol, 0.3) for g, rs in sorted(feats) for r in rs)
    return by, outline


@glyph(119)
def g119(m):  # District map: one state's districts, each drawn whole, one picked out
    feats = sub_features(GEO_CD, "WI")
    t = fit_rings([r for g, rs in feats for r in rs], (22, 4, 44, 48))
    by = {M3: "", FL: "", FS: ""}
    for g, rs in sorted(feats):
        by[FS if g == "5503" else M3 if g in ("5501", "5506", "5508") else FL] += ring_path([t(r) for r in rs], 0.4, 0.3)
    outline = "".join(ring_path([t(r)], 0.4, 0.3) for g, rs in sorted(feats) for r in rs)
    return "".join(P(c, d) for c, d in by.items()) + P(ST, outline, ' stroke-linejoin="round"')


@glyph(120)
def g120(m):  # County choropleth: one state's counties, each shaded by its value
    by, outline = sub_map(GEO_COUNTIES, "IA", (6, 6, 76, 44), [M2, M3, M4, FS], 0.4)
    return "".join(P(c, d) for c, d in by.items()) + P(ST, outline, ' stroke-linejoin="round"')


@glyph(121)
def g121(m):  # District tile map: one small square a district, gathered into each state's shape
    by = {FS: [], FC: [], FL: []}
    for y in range(5, 52, 4):
        for x in range(5, 84, 4):
            if m.inside(x + 1.5, y + 1.5):
                v = pattern(x * 1.7, y * 1.9, 2.2)
                by[FS if v > 0.6 else FC if v > 0.36 else FL].append((x, y, 3, 3))
    return "".join(P(k, rects(v)) for k, v in by.items())


@glyph(122)
def g122(m):  # Dot density map: one dot for so many people, placed where they are
    import random
    rnd = random.Random(14122)
    centers = [(76, 16, 6), (70, 26, 5), (60, 22, 5), (64, 42, 4), (46, 44, 5), (14, 30, 6), (12, 14, 3), (30, 24, 2),
               (50, 18, 3)]
    pts = []
    while len(pts) < 86:
        cx, cy, s = centers[rnd.randrange(len(centers))]
        x, y = rnd.gauss(cx, s), rnd.gauss(cy, s * 0.8)
        if m.inside(x, y) and all(math.hypot(x - a, y - b) > 2.6 for a, b in pts):
            pts.append((x, y))
    return m.land(FG) + P(FS, dots(pts, 1))


@glyph(123)
def g123(m):  # Small-multiple maps: the same map for each year, side by side
    out = ""
    for k in range(4):
        box = (4 + 41 * (k % 2), 3 + 26 * (k // 2), 39, 24)
        out += m.choropleth([[M2, M3, M4, M3], [M3, M4, M2, M4], [M2, M4, M3, M4], [M4, M3, M4, M2]][k], box=box)
    return out


@glyph(124)
def g124(m):  # Party-colored map or red and blue scale: each state in one of two flat fills (to avoid)
    full, hollow = [], []
    for code, (c, r) in sorted(tile_cells().items()):
        x, y = tile_xy(c, r, pitch=6, x0=8, y0=4)
        (full if pattern(x * 2.1, y * 1.3, 2.6) > 0.48 else hollow).append((x, y))
    return P(FS, rects([(x, y, 5, 5) for x, y in full])) + P(SS, "".join(f"M{x + 1} {y + 1}h3v3h-3z" for x, y in hollow), ' stroke-width="1"')


# --- Tables and plain words: where does a reader look things up, and when do words answer faster? ---------------------

def table_rules(ys, x0=4, x1=84):
    return P(SG, lines([[(x0, y), (x1, y)] for y in ys]))


@glyph(125)
def g125(m):  # Results table with margin cells: one row a place, the margin as a cell sized to the lead
    out = P(SS, "M4 8H84") + table_rules([20, 32, 44])
    for i, (w, lead) in enumerate([(22, 26), (18, 18), (24, 11), (16, 6)]):
        y = 14 + 12 * i
        out += textlines(4, y, [w]) + P(FS if i == 0 else FC, rects([(48, y - 3, lead, 6)])) + textlines(78, y, [6])
    return out


@glyph(126)
def g126(m):  # Ranked register: a numbered list in rank order, each row's figure and bar
    out = table_rules([15, 27, 39, 51])
    for i, w in enumerate([38, 30, 24, 16]):
        y = 9 + 12 * i
        out += P(FS if i == 0 else FC, rects([(4, y - 3, 5, 6)])) + textlines(14, y, [26 - 2 * i])
        out += P(FS if i == 0 else FC, rects([(84 - w, y - 2, w, 4)]))
    return out


@glyph(127)
def g127(m):  # Comparison matrix: the options in rows, the measures in columns, each cell's answer in words on its shade
    shades = [[M2, FT, M2, FT], [FT, M2, FT, M2], [M2, FT, FT, M2]]
    by = {M2: [], FT: []}
    words = []
    for r in range(3):
        for c in range(4):
            x, y = 24 + 15 * c, 12 + 14 * r
            by[shades[r][c]].append((x, y, 14, 13))
            words.append([(x + 3, y + 6.5), (x + 3 + (8 if (r + c) % 2 else 6), y + 6.5)])
    return ("".join(P(k, rects(v)) for k, v in by.items()) + P(SS, lines(words))
            + textlines(26, 6, [9]) + textlines(41, 6, [9]) + textlines(56, 6, [9]) + textlines(71, 6, [9])
            + textlines(4, 18.5, [16, 12, 14], 14))


@glyph(128)
def g128(m):  # Sparkline table: one row an item, a small line of its history beside its figure
    out = P(SS, "M4 8H84") + table_rules([20, 32, 44])
    for i in range(4):
        y = 14 + 12 * i
        pts = [(40 + 5 * k, y + 2 - 2.5 * math.sin(k * 0.8 + i * 1.3) - (0.6 * k if i % 2 == 0 else -0.3 * k)) for k in range(7)]
        out += textlines(4, y, [24 - 3 * i]) + series(pts) + textlines(76, y, [8])
    return out


@glyph(129)
def g129(m):  # Heat table: a table whose cells are shaded by their values
    by = {M2: [], M3: [], M4: [], FS: []}
    for r in range(5):
        for c in range(6):
            v = pattern(c * 13.0, r * 9.0, 1.1)
            by[lerp_class(v, [M2, M3, M4, FS])].append((30 + 9 * c, 5 + 9.4 * r, 8, 8))
    return "".join(P(k, rects(v)) for k, v in by.items()) + textlines(4, 9, [20, 16, 22, 14, 18], 9.4)


@glyph(130)
def g130(m):  # Filterable lookup table: a search field over the table, the rows narrowing as a reader types
    return (P(SS, box(5, 4, 78, 12)) + P(SS, dots([(12, 10)], 3)) + P(SS, "M14.5 12.5L17 15")
            + textlines(21, 10, [20]) + P(SS, "M4 24H84") + table_rules([34, 44])
            + textlines(4, 29, [26, 0], 0) + textlines(54, 29, [14]) + textlines(4, 39, [22]) + textlines(54, 39, [18])
            + textlines(4, 49, [28]) + textlines(54, 49, [12]))


@glyph(131)
def g131(m):  # Evidence table: each claim in a row, with its grade and its source
    out = P(SS, "M4 8H84") + table_rules([20, 32, 44])
    grades = [FS, FC, FS, FL]
    for i in range(4):
        y = 14 + 12 * i
        out += P(grades[i], rects([(4, y - 3, 12, 6)])) + textlines(21, y, [32 - 4 * i]) + textlines(64, y, [16])
    return out


@glyph(132)
def g132(m):  # Tracker list: each item in a row, with how far along its steps it is
    out = table_rules([16, 30, 44])
    for i, k in enumerate([5, 2, 4]):
        y = 9 + 14 * i
        out += textlines(4, y, [30 - 4 * i])
        out += P(FS, dots([(46 + 7 * s, y) for s in range(k)], 2.5)) + P(SC, dots([(46 + 7 * s, y) for s in range(k, 6)], 2.2))
    return out


@glyph(133)
def g133(m):  # Plain table: rows and columns of words and figures, nothing more
    out = P(SS, "M4 9H84") + table_rules([20, 31, 42])
    out += P(SS, "M4 4h20M54 4h10M74 4h10")
    for i in range(4):
        y = 15 + 11 * i
        out += textlines(4, y, [26 - 3 * (i % 2)]) + textlines(56 - 2 * (i % 2), y, [8 + 2 * (i % 2)]) + textlines(76 - 2 * (i % 3), y, [8 + 2 * (i % 3)])
    return out


@glyph(134)
def g134(m):  # One sentence: the figure stated in words, where a chart would add nothing
    return (P(FS, rects([(4, 15, 22, 6)])) + P(SS, "M29 18H84") + P(SS, "M4 30H76") + P(SS, "M4 42H52"))


# --- Infographics: how does it work, in one look? -------------------------------------------------------------------------

@glyph(135)
def g135(m):  # Process explainer: how a public process runs, step by step across lanes
    out = P(SG, "M4 19H84M4 37H84")
    out += P(SS, box(5, 5, 18, 10) + box(35, 23, 18, 10) + box(65, 41, 18, 10))
    out += P(SC, "M24 10H29V28H34M54 28H59V46H64")
    return out + textlines(8, 10, [12]) + textlines(38, 28, [12]) + textlines(68, 46, [12])


@glyph(136)
def g136(m):  # By-the-numbers panel: a few figures set large, side by side, each with its words
    out = P(SG, "M30 4V52M58 4V52")
    for i, x in enumerate((4, 33, 61)):
        out += P(FS, rects([(x, 8, 20 - 2 * (i % 2), 12)])) + textlines(x, 28, [22, 18, 20])
    return out


@glyph(137)
def g137(m):  # Comparison cards: options as cards side by side, the same fields on each
    out = P(SC, box(4, 4, 24, 48) + box(32, 4, 24, 48) + box(60, 4, 24, 48))
    for x in (8, 36, 64):
        out += P(SS, f"M{x} 11h14") + textlines(x, 21, [16, 12, 14, 10, 15], 6)
    return out


@glyph(138)
def g138(m):  # Step-by-step: what a reader does, in numbered steps down the page
    ys = [9, 27, 45]
    return (P(SS, "M10 13V41") + P(FS, dots([(10, y) for y in ys], 5)) + textlines(22, 7, [40, 28])
            + textlines(22, 25, [48, 22]) + textlines(22, 43, [36, 30]))


@glyph(139)
def g139(m):  # Annotated illustration: a drawing with numbered parts, each explained beside it
    out = P(SC, box(5, 4, 34, 48)) + textlines(10, 12, [22, 24, 18, 24, 20, 22, 16], 5)
    out += P(FS, dots([(36, 14), (36, 34), (8, 44)], 3.5))
    out += P(FS, dots([(48, 10), (48, 28), (48, 46)], 3.5)) + textlines(55, 10, [28]) + textlines(55, 28, [24]) + textlines(55, 46, [26])
    return out


@glyph(140)
def g140(m):  # Calendar: the days in a month grid, the dates that matter marked
    on, off = [], []
    for k in range(35):
        x, y = 9 + 10 * (k % 7), 8 + 9 * (k // 7)
        (on if k in (9, 23) else off).append((x, y, 8, 7))
    return P(FG, rects([c for c in off if (c[0], c[1]) != (49, 35)])) + P(FS, rects(on)) + P(SS, "M50 36h8v7h-8z")


@glyph(141)
def g141(m):  # Social data card: a finished card to share, with its chart inside
    out = P(SS, box(24, 2, 40, 50))
    out += P(SS, "M29 9H59") + textlines(29, 14, [22])
    pts = [(31 + 3.2 * i, 44 - 1.2 * i - (2 if i % 3 == 0 else 0)) for i in range(9)]
    return out + P(FC, dots(pts[1:-1], 1.8)) + P(FS, dots([pts[0], pts[-1]], 2.4)) + textlines(29, 48, [16])


# The avoid mark (A-1): a 1 px frame in the context ink and one rule from its top left to its bottom right in the
# subject ink at the pictures' stroke weight, drawn on top of the form's own picture by a second <use>.
AVOID = P(SC, "M0.5 0.5H87.5V55.5H0.5Z", ' stroke-width="1"') + P(SS, "M1 1L87 55")


# ---------------------------------------------------------------------------------------------------------------------
# The plate.

CSS = (
    # the symbol set: out of sight at no size, never display:none, which drops what a <use> reads (R5-2, item 2)
    ".sg-defs{position:absolute;width:0;height:0;overflow:hidden}"
    # the root follows the reader's colors in forced colors and paints its own ground (AX 1.10)
    ".sg{position:relative;forced-color-adjust:auto;background:var(--oa-color-surface);color:var(--oa-color-text-primary)}"
    ".sg-qs,.sg-fs{list-style:none;margin:0;padding:0}"
    ".sg-q{position:relative;padding:var(--oa-space-300) 0}"
    ".sg-q:first-child{padding-top:0}.sg-q:last-child{padding-bottom:0}"
    ".sg-q+.sg-q{border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}"
    ".sg-qt{margin:0 0 var(--oa-space-200);font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);"
    "text-wrap:balance;max-width:34em;break-after:avoid}"
    # tiles on one column grid in rem, so larger text takes fewer columns (AX 1.8)
    ".sg-fs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,6rem),1fr));gap:var(--oa-space-300) var(--oa-space-200)}"
    ".sg-fs>li{break-inside:avoid}"
    ".sg-fs a{display:flex;flex-direction:column;align-items:flex-start;gap:var(--oa-space-050);min-height:44px;"
    "color:inherit;text-decoration:none}"
    ".sg-pic{display:block;flex:none;margin-bottom:var(--oa-space-100)}"
    ".sg-n{font:var(--oa-type-ui);overflow-wrap:break-word;max-width:100%}"
    ".sg-t{font:var(--oa-type-caption);color:var(--oa-color-text-secondary)}"
    # the comma a screen reader pauses on between name and tier, out of sight in the line it ends; an absolutely placed
    # hidden span (the shell's .vh) makes Chromium name the link "Ranked bar , Core", with a space before the comma
    ".sg-c{clip-path:inset(50%)}"
    ".sg-fs a:hover .sg-n{text-decoration:underline;text-decoration-thickness:var(--oa-border-width-underline-hover);"
    "text-underline-offset:.2em}"
    # the skip links: Rule 18's skip link, shown 4 px inside the block it skips (AX 1.5)
    ".sg .sg-skip{top:4px;left:4px}"
    "@media print{.sg .sg-skip{display:none}}"
)


def load():
    plan = json.loads(PLAN.read_text())
    chapter = json.loads(CHAPTER.read_text())
    forms = plan["forms"]
    groups = {g["group"]: g for g in plan["groups"] if g.get("family_section")}
    printed = {g["number"]: g["title"] for g in chapter["groups"]}
    extra = next((x for x in chapter.get("extras", []) if x.get("specimen") == SID), None)
    need(extra and extra.get("label") and extra.get("caption"), f"14-chapter.json has no extras entry with words for {SID}")
    need(len(forms) == 127, f"the plan holds {len(forms)} forms, not 127")
    rules = [fm["rule"] for fm in forms]
    need(len(set(rules)) == len(rules), "a rule appears twice in the plan's forms")
    section_group = {g["family_section"]: n for n, g in groups.items()}
    need(sorted(section_group.values()) == list(range(2, 18)), "the plan's family groups are not groups 2 to 17")
    by_group = {n: [] for n in range(2, 18)}
    for fm in forms:
        tier = fm["tier"].split(",")[0].strip()
        need(tier in TIER_ORDER, f"Rule {fm['rule']}: tier {fm['tier']!r} is none of {TIER_ORDER}")
        n = section_group.get(fm["family_section"])
        need(n is not None, f"Rule {fm['rule']}: family section {fm['family_section']} names no group")
        lo, hi = groups[n]["rules"].split(" to ")
        num = int(fm["rule"].split(".")[1])
        need(int(lo.split(".")[1]) <= num <= int(hi.split(".")[1]), f"Rule {fm['rule']} sits outside group {n}'s rules")
        need(n in printed, f"14-chapter.json prints no title for group {n}")
        need(printed[n] == groups[n]["title"], f"group {n}: the chapter prints {printed[n]!r}, the plan {groups[n]['title']!r}")
        by_group[n].append(dict(fm, tier_word=tier, num=num))
    for n in by_group:
        # ruling (a): Core, Extended, Reference, Avoid; inside a tier, rule order
        by_group[n].sort(key=lambda x: (TIER_ORDER.index(x["tier_word"]), x["num"]))
    return plan, chapter, extra, by_group, printed


def symbol(sid, inner, box=False):
    """A picture's symbol. It draws at the picture's own size, so it needs no viewBox; the country's groups take one, since
    the small-multiple maps draw them smaller (14.123)."""
    vb = f' viewBox="0 0 {W} {H}"' if box else ""
    return f'<symbol id="{sid}"{vb} stroke-width="{SW}">{inner}</symbol>'


def picture(n, avoid):
    uses = f'<use href="#s-14-sg-{n}"/>' + ('<use href="#s-14-sg-avoid"/>' if avoid else "")
    return (f'<svg class="oac-svg sg-pic" viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true" '
            f'focusable="false">{uses}</svg>')


def build():
    plan, chapter, extra, by_group, printed = load()
    maps = Maps()
    need(set(G) == {fm["num"] for v in by_group.values() for fm in v},
         f"pictures and forms differ: {sorted(set(G) ^ {fm['num'] for v in by_group.values() for fm in v})}")
    syms = [symbol(k, v, box=True) for k, v in maps.symbols().items()]
    syms += [symbol(f"s-14-sg-{n}", G[n](maps)) for n in sorted(G)]
    syms.append(symbol("s-14-sg-avoid", AVOID))
    defs = (f'<svg class="oac-svg sg-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>'
            + "".join(syms) + "</defs></svg>")
    label = extra["label"]
    qs = []
    order = sorted(by_group)
    for i, n in enumerate(order):
        fs = by_group[n]
        nxt = f"#s-14-sg-q-{order[i + 1]}" if i + 1 < len(order) else "#group-14-1"
        items = []
        for fm in fs:
            name = fm["form"]
            items.append(
                f'<li id="s-14-sg-f-{fm["num"]}" data-return-label="{e(name + " in " + label)}">'
                f'<a href="#rule-14-{fm["num"]}" data-tier="{fm["tier_word"].lower()}" data-rule="{fm["rule"]}" data-oa-xref>'
                f'{picture(fm["num"], fm["tier_word"] == "Avoid")}<span class="sg-n">{e(name)}<span class="sg-c">,</span></span>'
                f'<span class="sg-t">{e(fm["tier_word"])}</span></a></li>')
        qs.append(
            f'<li class="sg-q" data-group="{n}"><p class="sg-qt" id="s-14-sg-q-{n}">{e(printed[n])}</p>'
            f'<a class="oa-link-skip sg-skip" href="{nxt}">Skip these {len(fs)} forms</a>'
            f'<ul class="sg-fs" role="list" aria-labelledby="s-14-sg-q-{n}">{"".join(items)}</ul></li>')
    body = (f'<div class="sg"><a class="oa-link-skip sg-skip" href="#group-14-1">Skip the chart guide</a>'
            f'<ol class="sg-qs" role="list">{"".join(qs)}</ol></div>')
    head = (f"<!-- {SID}: Oath & Action guide, Edition 06, chapter 14, the selection guide. Selection guide maker, "
            f"{WRITTEN}. Written by work/build/scripts/phase-3/selection_guide_build.py from the plan file; do not edit by "
            f"hand: run the script, whose --check fails when this file and the plan disagree. -->\n")
    frag = head + f"<style>{CSS}</style>\n{defs}\n{body}\n"
    meta = {
        "chapter": "14",
        "rule": None,
        "width_px": None,
        "alt": ("Every one of the 127 forms in this chapter, under the 16 reader questions that open its groups, each named "
                "with its tier and linked to its entry, beside a small drawing of the form."),
        "illustrative": False,
        "interactive": True,
        "fit_switch": False,
        "label": label,
        "caption": extra["caption"],
        "notes": ("Chapter 14's selection guide (R5-2, DR-273): the plan's 127 forms under the 16 family questions, "
                  "Core, Extended, Reference, then Avoid within each, every picture drawn from one symbol set; written by "
                  "selection_guide_build.py."),
    }
    check(frag, by_group, printed)
    return frag, json.dumps(meta, indent=1, ensure_ascii=False) + "\n", by_group


# ---------------------------------------------------------------------------------------------------------------------
# Checks, each a stop: the plan's forms once each under their own question, the links, the symbols, the inks, no words.

def check(frag, by_group, printed):
    faults = []
    hrefs = re.findall(r'<a href="#rule-14-(\d+)" data-tier="(\w+)" data-rule="14\.(\d+)"', frag)
    want = {fm["num"]: fm for v in by_group.values() for fm in v}
    seen = {}
    for a, tier, b in hrefs:
        if a != b:
            faults.append(f"link to rule 14.{a} carries data-rule 14.{b}")
        seen[int(a)] = seen.get(int(a), 0) + 1
        fm = want.get(int(a))
        if not fm:
            faults.append(f"link to rule 14.{a}, which is no form in the plan")
        elif tier != fm["tier_word"].lower():
            faults.append(f"Rule 14.{a}: data-tier {tier}, plan tier {fm['tier_word']}")
    for num in want:
        if seen.get(num) != 1:
            faults.append(f"Rule 14.{num} is linked {seen.get(num, 0)} times")
    if len(hrefs) != 127:
        faults.append(f"{len(hrefs)} form links, not 127")
    # each form under its own question, with its name and its tier word in the link's text
    for n, fs in by_group.items():
        block = re.search(rf'<li class="sg-q" data-group="{n}">(.*?)</ul></li>', frag, re.S)
        if not block:
            faults.append(f"group {n} has no block")
            continue
        if f'id="s-14-sg-q-{n}">{e(printed[n])}</p>' not in block.group(1):
            faults.append(f"group {n}'s question line is not the chapter's title")
        for fm in fs:
            m = re.search(rf'<a href="#rule-14-{fm["num"]}"[^>]*>(.*?)</a>', block.group(1))
            if not m:
                faults.append(f"Rule {fm['rule']} is not under group {n}")
                continue
            text = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
            if text != f"{fm['form']},{fm['tier_word']}":
                faults.append(f"Rule {fm['rule']}: the link reads {text!r}")
        got = [int(x) for x in re.findall(r'<a href="#rule-14-(\d+)"', block.group(1))]
        if got != [fm["num"] for fm in fs]:
            faults.append(f"group {n}: forms out of ruling (a)'s order")
    # symbols: each defined once and used, every <use> resolving, inside the box, in the neutral inks, no words
    defs = re.findall(r'<symbol id="([^"]+)"', frag)
    uses = re.findall(r'<use href="#([^"]+)"', frag)
    for d in set(defs):
        if defs.count(d) != 1:
            faults.append(f"symbol {d} defined {defs.count(d)} times")
        if d not in uses:
            faults.append(f"symbol {d} never used")
    for u in set(uses) - set(defs):
        faults.append(f"<use> names {u}, which no symbol defines")
    for sym in re.findall(r"<symbol[^>]*>(.*?)</symbol>", frag, re.S):
        for cls in re.findall(r'class="([^"]+)"', sym):
            for c in cls.split():
                if c not in INKS:
                    faults.append(f"a picture uses the class {c}, outside the neutral inks")
        if 'd=""' in sym:
            faults.append("a picture holds an empty path")
        if re.search(r"<text|<tspan|<title|<desc|<image|style=|fill=\"#|stroke=\"#|rgb\(|url\(", sym):
            faults.append("a picture holds words, an image, a style attribute, a literal color or a reference")
    for svg in re.findall(r"<svg\b[^>]*>", frag):
        if 'aria-hidden="true"' not in svg or 'focusable="false"' not in svg:
            faults.append("an <svg> is not hidden from the accessibility tree")
    for bad, why in ((r"<h[1-6]\b", "a heading"), (r"\sstyle=", "a style attribute"), (r"#[0-9a-fA-F]{3,6}\b(?![\w-])", "a literal color"),
                     ("—", "an em dash"), ("‑", "U+2011"), (r"<title\b", "a title"), (r"\stitle=", "a title attribute")):
        body = frag.split("</style>", 1)[1]
        body = re.sub(r'href="#[^"]+"', "", body)
        if re.search(bad, body):
            faults.append(f"the fragment holds {why}")
    for i in re.findall(r'\sid="([^"]+)"', frag):
        if not i.startswith("s-14-sg-"):
            faults.append(f"id {i} does not start s-14-sg-")
    ids = re.findall(r'\sid="([^"]+)"', frag)
    if len(ids) != len(set(ids)):
        faults.append("an id repeats")
    # the skip links: one past the guide, one a question to the next question's line (AX 1.5)
    skips = re.findall(r'<a class="oa-link-skip sg-skip" href="#([^"]+)">([^<]+)</a>', frag)
    if not skips or skips[0] != ("group-14-1", "Skip the chart guide"):
        faults.append("the guide's first stop is not its skip link")
    order = sorted(by_group)
    for i, n in enumerate(order):
        want_t = f"s-14-sg-q-{order[i + 1]}" if i + 1 < len(order) else "group-14-1"
        if (want_t, f"Skip these {len(by_group[n])} forms") not in skips:
            faults.append(f"group {n}'s skip link is missing or wrong")
    need(not faults, "faults:\n  " + "\n  ".join(faults))


def check_page(page, by_group):
    """Every link in the placed guide lands on its rule's block on the built page, and every skip link on its target."""
    s = Path(page).read_text(encoding="utf-8")
    i = s.find(f'data-specimen="{SID}"')
    need(i >= 0, f"{page} holds no {SID}")
    j = s.find("</figure>", i)
    plate = s[i:j]
    faults = []
    for num in sorted(fm["num"] for v in by_group.values() for fm in v):
        if plate.count(f'href="#rule-14-{num}"') != 1:
            faults.append(f"Rule 14.{num} is linked {plate.count(f'href=\"#rule-14-{num}\"')} times on the page")
        if not re.search(rf'<div class="rule[^"]*" id="rule-14-{num}" data-rule="14\.{num}"', s):
            faults.append(f"#rule-14-{num} is not a rule block on the page")
    for t in set(re.findall(r'href="#([^"]+)"', plate)):
        if not re.search(rf'\sid="{re.escape(t)}"', s):
            faults.append(f"#{t} lands on nothing")
    need(not faults, "page faults:\n  " + "\n  ".join(faults))
    return len(re.findall(r'href="#rule-14-\d+"', plate))


def sheet(frag, out):
    """A review sheet (scratch only): every picture at true size on Newsprint and on Charcoal, with its rule number."""
    toks = (ROOT / "work/build/tokens/tokens.css").read_text()
    kit = (ROOT / "work/build/chart-kit/kit.css").read_text()
    defs = re.search(r'<svg class="oac-svg sg-defs".*?</svg>', frag, re.S).group(0)
    nums = sorted(int(x) for x in re.findall(r'<symbol id="s-14-sg-(\d+)"', frag))
    avoid = set(int(x) for x in re.findall(r'<a href="#rule-14-(\d+)" data-tier="avoid"', frag))
    cells = "".join(f'<div class="c"><span>14.{n}</span>{picture(n, n in avoid)}</div>' for n in nums)
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{toks}{kit}'
           "body{margin:0;font:12px sans-serif}.g{display:grid;grid-template-columns:repeat(8,104px);gap:10px;padding:12px}"
           ".c span{display:block;font-size:11px;margin-bottom:2px}.sg-defs{position:absolute;width:0;height:0;overflow:hidden}"
           f'</style></head><body>{defs}<div class="oa-surface-newsprint g">{cells}</div>'
           f'<div class="oa-surface-charcoal g">{cells}</div></body></html>')
    Path(out).write_text(doc, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 when the files on disk differ from what the plan makes")
    ap.add_argument("--page", help="a built guide page: prove every link in the placed guide lands")
    ap.add_argument("--sheet", help="write a review sheet of every picture to this path (scratch only)")
    a = ap.parse_args()
    frag, meta, by_group = build()
    if a.sheet:
        sheet(frag, a.sheet)
    if a.check:
        bad = [p.name for p, t in ((FRAG, frag), (META, meta)) if not p.exists() or p.read_text(encoding="utf-8") != t]
        if bad:
            print(f"selection_guide_build --check: {', '.join(bad)} differ from what the plan makes; run the script.")
            sys.exit(1)
        print(f"selection_guide_build --check: both files match the plan, {sum(len(v) for v in by_group.values())} forms.")
    else:
        for p, t in ((FRAG, frag), (META, meta)):
            if not p.exists() or p.read_text(encoding="utf-8") != t:
                p.write_text(t, encoding="utf-8")
        n_sym = len(re.findall(r"<symbol ", frag))
        print(f"selection_guide_build: wrote {FRAG.relative_to(ROOT)} ({len(frag.encode()):,} bytes; {n_sym} symbols, "
              f"{sum(len(v) for v in by_group.values())} forms under {len(by_group)} questions) and {META.name}")
    if a.page:
        n = check_page(a.page, by_group)
        print(f"selection_guide_build --page: {n} form links, each landing on its rule block; every skip link lands")


if __name__ == "__main__":
    main()
