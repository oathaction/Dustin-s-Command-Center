"""Board 6, section 3: geometry for the stacked lockup variations (identity designer, November 7, 2026).

Reads the approved masters and places them. No letter is redrawn (D2-321): every word is cut from a
wordmark master with its letters at the positions that master gives them, and ampersand B comes from
its own master, moved and, in one option, scaled as a whole.

Spacing follows the wordmark's hinge rule (C-007, Phase 1 option 2b): white between two shapes is
measured as area, slice by slice across the band they share, each slice counted to at most 0.15x past
the nearest point, and averaged over the band. The wordmark holds 0.203x of white on each side of B.
Here every join in a stack holds that same white:
  - beside B (H to B, B to A) the masters' own placement is kept, so the white is the wordmark's;
  - between lines the slices run down columns instead of across rows, and the gap is solved so the
    white matches the hinge. A column where one line has no ink counts as open, to the 0.15x limit.

This module has no outside dependency: a small SVG path reader (absolute M L H V Q C Z, which is all
the masters use), flattening for measurement and an exact re-writer for output.
"""
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
IDENT = ROOT / "work/build/assets/identity"
MASTERS = {
    "wm_display": IDENT / "wordmark/20261028_Wordmark-Display-Master.svg",
    "wm_24": IDENT / "wordmark/20261028_Wordmark-24px-Master.svg",
    "wm_16": IDENT / "wordmark/20261028_Wordmark-16px-Master.svg",
    "b_display": IDENT / "ampersand/20261028_Amp-B-Display-Master.svg",
    "b_24": IDENT / "ampersand/20261028_Amp-B-24px-Master.svg",
    "b_16": IDENT / "ampersand/20261028_Amp-B-16px-Master.svg",
    "l2": IDENT / "lockups/20261028_L2-Stacked-Master.svg",
}
DEPTH_X = 0.15   # slices count to 0.15x past the nearest point (p1_wordmark.DEPTH)
FLOOR_X = 0.07   # no ink nearer than 0.07x (p1_wordmark.FLOOR)
NAMES = ["O", "A", "T", "H", "A2", "C", "T2", "I", "O2", "N"]

NUM = re.compile(r"[A-Za-z]|-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


# ------------------------------------------------------------------ paths

def parse_d(d):
    """Absolute SVG path data to subpaths: each a list of ('M', p), ('L', p), ('Q', c, p), ('C', c1, c2, p)."""
    toks = NUM.findall(d)
    subs, cur, i, cmd, pos, start = [], None, 0, None, (0.0, 0.0), (0.0, 0.0)

    def nums(n):
        nonlocal i
        v = [float(t) for t in toks[i:i + n]]
        i += n
        return v
    while i < len(toks):
        t = toks[i]
        if re.match(r"[A-Za-z]", t):
            cmd = t
            i += 1
            if cmd in "Zz":
                if cur:
                    subs.append(cur)
                cur = None
                pos = start
                continue
        if cmd is None or cmd.islower():
            raise ValueError(f"unsupported path command {cmd!r}")
        if cmd == "M":
            x, y = nums(2)
            if cur:
                subs.append(cur)
            cur = [("M", (x, y))]
            pos = start = (x, y)
            cmd = "L"          # implicit lineto after a moveto
        elif cmd == "L":
            x, y = nums(2)
            cur.append(("L", (x, y)))
            pos = (x, y)
        elif cmd == "H":
            (x,) = nums(1)
            pos = (x, pos[1])
            cur.append(("L", pos))
        elif cmd == "V":
            (y,) = nums(1)
            pos = (pos[0], y)
            cur.append(("L", pos))
        elif cmd == "Q":
            cx, cy, x, y = nums(4)
            cur.append(("Q", (cx, cy), (x, y)))
            pos = (x, y)
        elif cmd == "C":
            a, b, c, d_, x, y = nums(6)
            cur.append(("C", (a, b), (c, d_), (x, y)))
            pos = (x, y)
        else:
            raise ValueError(f"unsupported path command {cmd!r}")
    if cur:
        subs.append(cur)
    return subs


def xform(subs, s=1.0, dx=0.0, dy=0.0):
    f = lambda p: (p[0] * s + dx, p[1] * s + dy)
    return [[(seg[0], *[f(p) for p in seg[1:]]) for seg in sp] for sp in subs]


def fmt(v, nd):
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def to_d(subs, nd=2):
    out = []
    for sp in subs:
        for seg in sp:
            out.append(seg[0] + " ".join(f"{fmt(p[0], nd)} {fmt(p[1], nd)}" for p in seg[1:]))
        out.append("Z")
    return "".join(out)


def flatten(sp, steps=24):
    pts, last = [], None
    for seg in sp:
        k = seg[0]
        if k == "M":
            pts.append(seg[1]); last = seg[1]
        elif k == "L":
            pts.append(seg[1]); last = seg[1]
        elif k == "Q":
            c, e = seg[1], seg[2]
            for j in range(1, steps + 1):
                t = j / steps; mt = 1 - t
                pts.append((mt * mt * last[0] + 2 * mt * t * c[0] + t * t * e[0], mt * mt * last[1] + 2 * mt * t * c[1] + t * t * e[1]))
            last = e
        elif k == "C":
            c1, c2, e = seg[1], seg[2], seg[3]
            for j in range(1, steps + 1):
                t = j / steps; mt = 1 - t
                pts.append((mt ** 3 * last[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * e[0],
                            mt ** 3 * last[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * e[1]))
            last = e
    return pts


def bbox(subs):
    xs, ys = [], []
    for sp in subs:
        for x, y in flatten(sp, 48):
            xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys))


def read_master(key):
    s = MASTERS[key].read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    paths = re.findall(r'<path fill="([^"]+)" d="([^"]+)"', s)
    return vb, [(fill, parse_d(d)) for fill, d in paths]


def split_glyphs(subs):
    """Group contours into glyphs: a contour whose box sits inside a larger one's box joins it (counters)."""
    boxes = [bbox([sp]) for sp in subs]
    order = sorted(range(len(subs)), key=lambda k: -(boxes[k][2] - boxes[k][0]) * (boxes[k][3] - boxes[k][1]))
    groups = []
    for k in order:
        b = boxes[k]
        for g in groups:
            gb = g["box"]
            if b[0] >= gb[0] - 0.01 and b[2] <= gb[2] + 0.01 and b[1] >= gb[1] - 0.01 and b[3] <= gb[3] + 0.01:
                g["subs"].append((k, subs[k]))
                break
        else:
            groups.append({"box": b, "subs": [(k, subs[k])]})
    out = []
    for g in groups:
        g["subs"].sort()                       # keep the master's own contour order
        out.append([sp for _, sp in g["subs"]])
    out.sort(key=lambda gl: bbox(gl)[0])
    return out


# ------------------------------------------------------------------ masters as parts

class Shape:
    """A placed part: contours plus its paint role ('ink' for letters, 'amp' for B)."""

    def __init__(self, subs, role, name):
        self.subs, self.role, self.name = subs, role, name
        self._box = None
        self._polys = None

    @property
    def box(self):
        if self._box is None:
            self._box = bbox(self.subs)
        return self._box

    def polys(self):
        if self._polys is None:
            self._polys = [flatten(sp, 24) for sp in self.subs]
        return self._polys

    def moved(self, dx=0.0, dy=0.0, s=1.0):
        return Shape(xform(self.subs, s, dx, dy), self.role, self.name)


def letters(key):
    """The ten capitals of a wordmark master, at the master's own positions, and its B."""
    vb, paths = read_master(key)
    ink = [sub for fill, subs in paths if fill == "currentColor" for sub in subs]
    amp = [sub for fill, subs in paths if fill.startswith("var(--amp") for sub in subs]
    gl = split_glyphs(ink)
    assert len(gl) == 10, f"{key}: expected 10 capitals, found {len(gl)}"
    G = {n: Shape(g, "ink", n) for n, g in zip(NAMES, gl)}
    return vb, G, Shape(amp, "amp", "&")


def b_master(key):
    vb, paths = read_master(key)
    return vb, Shape(paths[0][1], "amp", "&")


def word(G, names):
    return [G[n] for n in names]


def group_box(shapes):
    bs = [s.box for s in shapes]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def move_all(shapes, dx=0.0, dy=0.0, s=1.0):
    return [sh.moved(dx, dy, s) for sh in shapes]


# ------------------------------------------------------------------ white area

def _crossings(polys, coord, axis):
    """Sorted crossings of all contours with the line x = coord (axis 'v') or y = coord (axis 'h')."""
    out = []
    for pl in polys:
        n = len(pl)
        for j in range(n):
            (x1, y1), (x2, y2) = pl[j], pl[(j + 1) % n]
            if axis == "h":
                if (y1 <= coord < y2) or (y2 <= coord < y1):
                    out.append(x1 + (coord - y1) * (x2 - x1) / (y2 - y1))
            else:
                if (x1 <= coord < x2) or (x2 <= coord < x1):
                    out.append(y1 + (coord - x1) * (y2 - y1) / (x2 - x1))
    return sorted(out)


def _polys(shapes):
    ps = []
    for sh in shapes:
        ps.extend(sh.polys())
    return ps


def row_profile(shapes, y0, y1, step):
    ps = _polys(shapes)
    rows, y = [], y0 + step / 2
    while y < y1:
        xs = _crossings(ps, y, "h")
        rows.append((xs[0], xs[-1]) if xs else None)
        y += step
    return rows


def col_profile(shapes, x0, x1, step):
    ps = _polys(shapes)
    cols, x = [], x0 + step / 2
    while x < x1:
        ys = _crossings(ps, x, "v")
        cols.append((ys[0], ys[-1]) if ys else None)
        x += step
    return cols


def side_white(left, right, y0, y1, cap, step=0.25):
    """White between two parts side by side, as the wordmark's hinge is measured: rows across the
    band y0..y1, rows where either part has no ink skipped, each row counted to 0.15x past the nearest."""
    depth = DEPTH_X * cap
    a, b = row_profile(left, y0, y1, step), row_profile(right, y0, y1, step)
    gaps = [rb[0] - ra[1] for ra, rb in zip(a, b) if ra and rb]
    gmin = min(gaps)
    area = sum(min(g, gmin + depth) for g in gaps) / len(gaps)
    return {"nearest": gmin, "white": area}


def line_white(top, bottom, x0, x1, cap, step=0.25, prof=None):
    """White between two lines: columns across x0..x1, each from the upper line's lowest ink to the
    lower line's highest ink, counted to 0.15x past the nearest. A column where either line has no ink
    is open and counts at that limit."""
    depth = DEPTH_X * cap
    a = prof[0] if prof else col_profile(top, x0, x1, step)
    b = prof[1] if prof else col_profile(bottom, x0, x1, step)
    both = [(cb[0] - ca[1]) for ca, cb in zip(a, b) if ca and cb]
    gmin = min(both)
    vals = [min(cb[0] - ca[1], gmin + depth) if (ca and cb) else gmin + depth for ca, cb in zip(a, b)]
    return {"nearest": gmin, "white": sum(vals) / len(vals), "open_share": 1 - len(both) / len(vals)}


def solve_drop(top, bottom, x0, x1, cap, target, step=0.25):
    """Vertical shift for the lower line so the white between the lines equals target. Profiles are
    measured once; a shift only adds to the lower line's column tops."""
    a = col_profile(top, x0, x1, step)
    b0 = col_profile(bottom, x0, x1, step)

    def at(dy):
        b = [(c[0] + dy, c[1] + dy) if c else None for c in b0]
        return line_white(None, None, x0, x1, cap, step, prof=(a, b))
    lo, hi = -400.0, 400.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if at(mid)["white"] < target:
            lo = mid
        else:
            hi = mid
    dy = (lo + hi) / 2
    return dy, at(dy)


def drop_px(top, bottom, x0, x1, cap, target, floor):
    """Whole-pixel version: the integer shift whose white is nearest the target, nearest ink at or over floor."""
    step = 0.05
    a = col_profile(top, x0, x1, step)
    b0 = col_profile(bottom, x0, x1, step)
    best = None
    for dy in range(-60, 120):
        b = [(c[0] + dy, c[1] + dy) if c else None for c in b0]
        if not any(cb for cb in b):
            continue
        both = [ca and cb for ca, cb in zip(a, b)]
        if not any(both):
            continue
        r = line_white(None, None, x0, x1, cap, step, prof=(a, b))
        if r["nearest"] < floor - 1e-6:
            continue
        key = abs(r["white"] - target)
        if best is None or key < best[0] - 1e-9:
            best = (key, dy, r)
    return best[1], best[2]


# ------------------------------------------------------------------ the six variations

VARIANTS = [
    {"id": "S1", "name": "Ampersand ends line one", "lines": ["OATH&", "ACTION"], "align": "left"},
    {"id": "S2", "name": "Ampersand opens line two", "lines": ["OATH", "&ACTION"], "align": "left"},
    {"id": "S3", "name": "Hung ampersand", "lines": ["OATH", "&ACTION"], "align": "hung"},
    {"id": "S4", "name": "Ampersand line, centered", "lines": ["OATH", "&", "ACTION"], "align": "center"},
    {"id": "S5", "name": "Ampersand line, flush left", "lines": ["OATH", "&", "ACTION"], "align": "left"},
    {"id": "S6", "name": "Large ampersand, centered", "lines": ["OATH", "&", "ACTION"], "align": "center", "b_scale": 1.25},
]
SIZES = {
    # cap height, cap line of line one, master keys, the line floor (nearest ink) and decimals in output
    "display": {"cap": 100.0, "cap_top": 4.0, "wm": "wm_display", "b": "b_display", "floor": 7.0, "nd": 2, "pad": 4.0},
    24: {"cap": 22.0, "cap_top": 1.0, "wm": "wm_24", "b": "b_24", "floor": 2.0, "nd": 3, "pad": 1.0},
    16: {"cap": 14.0, "cap_top": 1.0, "wm": "wm_16", "b": "b_16", "floor": 1.5, "nd": 3, "pad": 1.0},
}
_CACHE = {}


def masters(size):
    if size not in _CACHE:
        S = SIZES[size]
        vb, G, B = letters(S["wm"])
        _, BM = b_master(S["b"])
        cap, top = S["cap"], S["cap_top"]
        l = side_white([G["H"]], [B], top, top + cap, cap, 0.25 if size == "display" else 0.05)
        r = side_white([B], [G["A2"]], top, top + cap, cap, 0.25 if size == "display" else 0.05)
        _CACHE[size] = {"G": G, "B": B, "BM": BM, "hinge": {"left": l, "right": r, "target": (l["white"] + r["white"]) / 2}}
    return _CACHE[size]


def groups(size, b_scale=1.0):
    """The parts each line can hold, at the master's own spacing. Moves are whole units at pixel sizes."""
    M = masters(size)
    G, B, BM = M["G"], M["B"], M["BM"]
    S = SIZES[size]
    oath = word(G, ["O", "A", "T", "H"])
    action = word(G, ["A2", "C", "T2", "I", "O2", "N"])
    pix = size != "display"
    sh = lambda v: float(round(v)) if pix else v
    amp_alone = BM.moved(0, B.box[1] - BM.box[1])           # B's master, standing where the wordmark stands it
    if b_scale != 1.0:
        bx = amp_alone.box
        if pix:
            # B's box grows to the nearest whole pixel of 1.25 times its share of the cap height (Rule 04.1 ranges)
            h_new = round((bx[3] - bx[1]) * (1.0 if size == "display" else 1.0) * b_scale * (1.0269 * S["cap"]) / (bx[3] - bx[1]))
            s = h_new / (bx[3] - bx[1])
        else:
            s = b_scale
        cy = S["cap_top"] + S["cap"] / 2
        amp_alone = amp_alone.moved(0, 0, s)
        nb = amp_alone.box
        amp_alone = amp_alone.moved(sh(-nb[0]), sh(cy - (nb[1] + nb[3]) / 2))
    return {
        "OATH": oath,
        "OATH&": oath + [B],
        "ACTION": move_all(action, sh(-G["A2"].box[0])),
        "&ACTION": move_all([B] + action, sh(-B.box[0])),
        "&": [amp_alone.moved(sh(-amp_alone.box[0]), 0)],
    }


def build(v, size):
    S = SIZES[size]
    M = masters(size)
    cap, pix = S["cap"], size != "display"
    sh = lambda val: float(round(val)) if pix else val
    P = groups(size, v.get("b_scale", 1.0))
    lines = [list(P[k]) for k in v["lines"]]
    # horizontal placement
    if v["align"] == "center":
        widths = [group_box(l)[2] - group_box(l)[0] for l in lines]
        axis = max(widths) / 2
        lines = [move_all(l, sh(axis - (group_box(l)[0] + group_box(l)[2]) / 2)) for l in lines]
    elif v["align"] == "hung":
        # O and A share the left edge; B leads line two and hangs outside it, at the wordmark's hinge
        a2 = [s for s in lines[1] if s.name == "A2"][0]
        lines[1] = move_all(lines[1], sh(-a2.box[0]))
    # vertical placement, line by line, white between lines equal to the master's own hinge white
    joins = []
    for k in range(1, len(lines)):
        up, lo = lines[k - 1], lines[k]
        bu, bl = group_box(up), group_box(lo)
        x0, x1 = max(bu[0], bl[0]), min(bu[2], bl[2])
        if pix:
            dy, r = drop_px(up, lo, x0, x1, cap, M["hinge"]["target"], S["floor"])
        else:
            dy, r = solve_drop(up, lo, x0, x1, cap, M["hinge"]["target"])
        lines[k] = move_all(lo, 0, dy)
        joins.append({"kind": "lines", "between": f"{v['lines'][k - 1]} / {v['lines'][k]}", "white": r["white"], "nearest": r["nearest"],
                      "open_share": r["open_share"], "band": [x0, x1]})
    shapes = [s for l in lines for s in l]
    # beside B in a line: the master's own hinge, measured again in place
    names = [s.name for s in shapes]
    for l, key in zip(lines, v["lines"]):
        if key == "OATH&":
            H, B_ = [s for s in l if s.name == "H"][0], [s for s in l if s.name == "&"][0]
            r = side_white([H], [B_], B_.box[1] if pix else H.box[1], H.box[3], cap, 0.25 if not pix else 0.05)
            joins.insert(0, {"kind": "side", "between": "H / B", "white": r["white"], "nearest": r["nearest"]})
        if key == "&ACTION":
            B_, A2 = [s for s in l if s.name == "&"][0], [s for s in l if s.name == "A2"][0]
            r = side_white([B_], [A2], A2.box[1], A2.box[3], cap, 0.25 if not pix else 0.05)
            joins.insert(0, {"kind": "side", "between": "B / A", "white": r["white"], "nearest": r["nearest"]})
    # frame: x from the leftmost ink, y from line one's cap line less the pad, to the last baseline plus the pad
    bx = group_box(shapes)
    x_shift = -bx[0] if not pix else -math.floor(bx[0])
    shapes = move_all(shapes, x_shift)
    bx = group_box(shapes)
    top = S["cap_top"] - S["pad"]
    base_last = max(s.box[3] for s in shapes if s.role == "ink" and s.name in ("A2", "T2", "I", "N", "A", "T", "H"))
    bottom = max(base_last + S["pad"], bx[3])
    top = min(top, bx[1])
    W = bx[2] if not pix else math.ceil(bx[2] - 1e-6)
    H = bottom - top
    vb = [0.0, top, round(W, 2), round(H, 2)]
    caps_tops = []
    for l in lines:
        # a line of letters runs from its cap line to its baseline (flat capitals, no overshoot);
        # B alone on a line runs from its ink top to its ink bottom
        ink = [s for s in l if s.role == "ink" and s.name in ("A", "T", "H", "A2", "T2", "I", "N")]
        if ink:
            caps_tops.append((min(s.box[1] for s in ink), max(s.box[3] for s in ink)))
        else:
            caps_tops.append((min(s.box[1] for s in l), max(s.box[3] for s in l)))
    return {"id": v["id"], "size": size, "shapes": shapes, "lines": lines, "viewBox": vb, "joins": joins,
            "cap": cap, "width": vb[2], "height": vb[3], "ink_box": [round(t, 2) for t in group_box(shapes)],
            "cap_bands": caps_tops, "hinge_target": M["hinge"]["target"]}


def svg_body(res, amp_fill="var(--amp,#E63946)"):
    nd = SIZES[res["size"]]["nd"]
    ink = [sp for s in res["shapes"] if s.role == "ink" for sp in s.subs]
    amp = [sp for s in res["shapes"] if s.role == "amp" for sp in s.subs]
    return f'<path fill="currentColor" d="{to_d(ink, nd)}"/><path fill="{amp_fill}" d="{to_d(amp, nd)}"/>'


def l2_measures():
    """Today's L2, read from its master: the white between its lines and B's distance to the N."""
    vb, paths = read_master("l2")
    ink = [s for f, ss in paths if f == "currentColor" for s in ss]
    amp = [s for f, ss in paths if f.startswith("var(--amp") for s in ss]
    gl = [Shape(g, "ink", "g") for g in split_glyphs(ink)]
    B = Shape(amp, "amp", "&")
    top = [g for g in gl if g.box[3] < 110]
    low = [g for g in gl if g.box[1] > 110]
    bt, bl = group_box(top), group_box(low)
    lw = line_white(top, low, max(bt[0], bl[0]), min(bt[2], bl[2]), 100.0)
    n = max(low, key=lambda g: g.box[2])
    sw = side_white([n], [B], n.box[1], n.box[3], 100.0)
    bb = B.box
    return {"viewBox": vb, "line_white": lw["white"], "line_nearest": lw["nearest"], "flat_gap": bl[1] - 104.0,
            "b_to_n_nearest": sw["nearest"], "b_to_n_white": sw["white"], "b_scale": (bb[3] - bb[1]) / 102.68,
            "b_box": [round(t, 2) for t in bb]}


def verify_no_redraw(res):
    """Every placed letter is its master glyph moved; B is its master moved, or moved and scaled as a whole.
    Compares every point of every contour after removing the move (and the scale for B)."""
    worst, checked = 0.0, 0
    M = masters(res["size"])
    for sh in res["shapes"]:
        src = M["G"][sh.name] if sh.role == "ink" else M["BM"]
        pa = [p for sp in src.subs for seg in sp for p in seg[1:]]
        pb = [p for sp in sh.subs for seg in sp for p in seg[1:]]
        assert len(pa) == len(pb), f"{res['id']} {res['size']} {sh.name}: point count differs"
        ba, bb = src.box, sh.box
        s = (bb[3] - bb[1]) / (ba[3] - ba[1])
        if sh.role == "ink":
            assert abs(s - 1) < 1e-9, f"{sh.name} scaled"
        for (x0, y0), (x1, y1) in zip(pa, pb):
            ex = abs((x1 - bb[0]) - (x0 - ba[0]) * s)
            ey = abs((y1 - bb[1]) - (y0 - ba[1]) * s)
            worst = max(worst, ex, ey)
            checked += 1
    return {"points": checked, "worst_offset": worst}
