"""Items 2 and 3. The wordmark at its current proportions: equal hinge gaps, and masters for
display, 24 px and 16 px with optical tracking per size and opened T joins.

Spacing model (Phase 0 method): for two neighbours, the nearest ink gap and the white area
between them across the cap band, each row capped at nearest + depth (depth 0.15x here),
divided by the band height. "Equal hinge" means equal area on both sides of the ampersand with
no ink closer than 0.07x. The literal V5 rule (0.10x nearest ink on both sides) is built too, so
Dustin can compare.

Small masters are pixel-fit: each glyph's stems and bars move to whole pixels with a
piecewise-linear warp (the method hinting uses), overshoots are suppressed, and the ampersand
fills the full box height at 16 and 24 px so the red keeps its weight beside Charcoal capitals.

Run: python3 -I p1_wordmark.py
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o  # noqa: E402
import p1_amp_a as A  # noqa: E402

NAMES = ["O", "A", "T", "H", "A2", "C", "T2", "I", "O2", "N"]
DEPTH = 15.0
FLOOR = 7.0
DIR2 = o.OUT / "02-hinge-gaps"
DIR3 = o.OUT / "03-wordmark-masters"

# Edges of each glyph in V5 wordmark units (absolute x), with stem pairs, for pixel fitting.
EDGES = {
    "O": {"x": [0.0, 24.63, 70.74, 95.37], "stems": [(0, 1), (2, 3)], "y": {2.66: "cap", 23.8: "o_in_top", 84.2: "o_in_bot", 105.34: "base"}},
    "A": {"x": [93.16, 119.13, 126.99, 159.07, 166.92, 192.83], "stems": [], "y": {4.0: "cap", 64.6: "a_bar_top", 82.99: "a_bar_bot", 104.0: "base"}},
    "T": {"x": [181.28, 211.62, 235.38, 265.71], "stems": [(1, 2)], "y": {4.0: "cap", 23.66: "t_bar_bot", 104.0: "base"}},
    "H": {"x": [271.02, 295.11, 334.58, 358.67], "stems": [(0, 1), (2, 3)], "y": {4.0: "cap", 44.13: "h_bar_top", 63.8: "h_bar_bot", 104.0: "base"}},
    "C": {"x": [565.8, 590.43, 657.61], "stems": [(0, 1)], "y": {2.66: "cap", 23.8: "o_in_top", 40.31: "c_term_top", 68.83: "c_term_bot", 84.2: "o_in_bot", 105.34: "base"}},
    "I": {"x": [751.31, 775.4], "stems": [(0, 1)], "y": {4.0: "cap", 104.0: "base"}},
    "N": {"x": [885.67, 909.77, 946.61, 970.71], "stems": [(0, 1), (2, 3)], "y": {4.0: "cap", 104.0: "base"}},
}
SAME = {"A2": ("A", 468.28 - 93.16), "T2": ("T", 661.57 - 181.28), "O2": ("O", 782.85 - 0.0)}

# y targets in pixels for each size: (cap px, row of the cap line, then named zones)
YPX = {
    16: {"cap_px": 14, "top": 1, "o_in_top": 4, "o_in_bot": 12, "t_bar_bot": 4, "h_bar_top": 6, "h_bar_bot": 9,
         "a_bar_top": 9, "a_bar_bot": 12, "c_term_top": 6, "c_term_bot": 10, "stem": 3},
    24: {"cap_px": 22, "top": 1, "o_in_top": 5, "o_in_bot": 19, "t_bar_bot": 5, "h_bar_top": 10, "h_bar_bot": 14,
         "a_bar_top": 14, "a_bar_bot": 18, "c_term_top": 9, "c_term_bot": 15, "stem": 5},
}
# optical tracking per size, in wordmark units added to every letter pair, and T arm trim
TRACK = {"display": 0.0, 24: 2.5, 16: 5.0}
T_TRIM = {"display": 0.0, 24: 1.5, 16: 4.0}


def glyphs():
    gl, amp = o.wordmark_letters()
    return dict(zip(NAMES, gl)), amp


def gap(a, b):
    return o.pair_gap(a, b, depth=DEPTH)


def solve_hinge(H, amp, A2, keep_total=True):
    """Shift the ampersand (d) and ACTION (e) so the depth-limited white areas match, with no
    ink nearer than FLOOR. Returns d, e and the resulting gaps."""
    pH, pa, pA = o.Profile(H), o.Profile(amp), o.Profile(A2)
    for e10 in range(0, 241):
        e = e10 / 10
        lo, hi = -20.0, 20.0
        for _ in range(40):
            d = (lo + hi) / 2
            l = o.gap_profiles(pH, pa, d, DEPTH)
            r = o.gap_profiles(pa, pA, e - d, DEPTH)
            if l["area"] < r["area"]:
                lo = d
            else:
                hi = d
        l = o.gap_profiles(pH, pa, d, DEPTH)
        r = o.gap_profiles(pa, pA, e - d, DEPTH)
        if min(l["min"], r["min"]) >= FLOOR - 1e-6:
            return round(d, 2), e, l, r
    return round(d, 2), e, l, r


def spacing_display(G, amp, ampkind="V5"):
    """Display master spacing: optical hinge plus the two densest pairs (I O, O N) and the
    T joins opened toward the median area of the other pairs."""
    xs = {n: 0.0 for n in NAMES}
    # pair adjustments in units, applied cumulatively from the left
    adj = {("T", "H"): 1.4, ("T2", "I"): 1.4, ("I", "O2"): 2.4, ("O2", "N"): 2.4}
    return adj


def place(G, amp, adj, hinge_d, hinge_e, track=0.0, t_trim=0.0):
    """Return dict of positioned glyph paths and the ampersand, in units."""
    seq = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]
    shift = 0.0
    out = {}
    prev = None
    for n in seq:
        if prev is not None:
            shift += track
            shift += adj.get((prev, n), 0.0)
        if n == "&":
            shift_amp = shift + hinge_d
            out["&"] = o.tx(amp, e=shift_amp)
        else:
            if n == "A2":
                shift += hinge_e
            g = G[n]
            if t_trim and n in ("T", "T2"):
                g = trim_t(g, n, t_trim)
            out[n] = o.tx(g, e=shift)
        prev = n
    return out


def trim_t(g, n, t):
    """Shorten both arms of a T by t units (its bar ends move in, the stem stays)."""
    x0 = 181.28 if n == "T" else 661.57
    x1 = 265.71 if n == "T" else 746.0
    return A.xwarp(g, [(x0, x0 + t), (x0 + 30.34, x0 + 30.34), (x1 - 30.33, x1 - 30.33), (x1, x1 - t)])


def to_svg(parts, vb, amp_fill="var(--amp,#E63946)", nd=2, title="wordmark"):
    letters = o.union(*[parts[n] for n in parts if n != "&"])
    body = (f'<path fill="currentColor" d="{o.d_from_path(o.simplify(letters), nd)}"/>'
            f'<path fill="{amp_fill}" d="{o.d_from_path(parts["&"], nd)}"/>')
    return body


def measures(parts):
    seq = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]
    out = {}
    for a, b in zip(seq, seq[1:]):
        g = gap(parts[a], parts[b])
        out[f"{a.rstrip('2')}{b.rstrip('2')}"] = {"nearest_x": round(g["min"] / 100, 3), "area_x": round(g["area"] / 100, 3)}
    bx = o.bounds(o.union(*parts.values()))
    out["width_units"] = round(bx[2] - bx[0], 2)
    return out


# ---------------------------------------------------------------- pixel fitting

def fit_glyph(g, name, x0_units, k, size, left_px):
    """Snap one glyph. g is in units with its own position; x0_units is its left ink edge.
    Returns the glyph in pixel units (y down, box top at 0)."""
    base = SAME.get(name, (name, 0.0))
    spec = EDGES[base[0]]
    off = base[1]
    yp = YPX[size]
    stem = yp["stem"]
    xs = [x + off for x in spec["x"]]
    # target px for each x edge, relative rounding from the glyph's own left edge
    tgt = {}
    for i, x in enumerate(xs):
        tgt[i] = left_px + round((x - xs[0]) * k)
    for a, b in spec["stems"]:
        tgt[b] = tgt[a] + stem
    # keep order strictly increasing
    pairs = []
    last = -1e9
    for i, x in enumerate(xs):
        t = max(tgt[i], last + 1)
        pairs.append((x, t))
        last = t
    # map units to px: first a uniform scale, then the warp from scaled edge to target
    q = o.tx(g, a=k, d=k, e=0, f=0)
    pairs_px = [(x * k, t) for x, t in pairs]
    if len(pairs_px) >= 2:
        q = A.xwarp(q, pairs_px)
    else:
        q = o.tx(q, e=pairs_px[0][1] - pairs_px[0][0])
    # y: units to px with the cap line at row 'top'
    cap_px = yp["cap_px"]
    ypairs = []
    for yu, zone in sorted(spec["y"].items()):
        y_scaled = yu * k
        if zone == "cap":
            t = yp["top"]
        elif zone == "base":
            t = yp["top"] + cap_px
        else:
            t = yp[zone]
        ypairs.append((y_scaled, t))
    q = A.ywarp(q, ypairs)
    return q


def pixel_master(parts, size, amp_px_path=None):
    """parts: positioned glyphs in units (display coordinates). Returns pixel-unit parts."""
    yp = YPX[size]
    k = yp["cap_px"] / 100.0
    seq = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]
    out = {}
    for n in seq:
        if n == "&":
            continue
        b = o.bounds(parts[n])
        left_px = round(b[0] * k)
        out[n] = fit_glyph(parts[n], n, b[0], k, size, left_px)
    # ampersand: full box height (0..size px), placed so its centre keeps the display hinge position
    ab = o.bounds(parts["&"])
    if amp_px_path is not None:
        q = amp_px_path
        qb = o.bounds(q)
        cx = (ab[0] + ab[2]) / 2 * k
        q = o.tx(q, e=round(cx - (qb[2] - qb[0]) / 2) - qb[0])
    else:
        hh = size
        s = hh / (ab[3] - ab[1])
        q = o.tx(parts["&"], a=s, d=s, e=0, f=0)
        qb = o.bounds(q)
        cx = (ab[0] + ab[2]) / 2 * k
        q = o.tx(q, e=round(cx - (qb[2] - qb[0]) / 2) - qb[0], f=-qb[1])
    out["&"] = q
    return out


def space_px(px, size, floor_px=2.0):
    """Small-size spacing: every letter pair gets the same depth-limited white area (the mean of
    O A and A C, the two pairs that need no help), in whole-pixel steps, never nearer than
    floor_px. The two hinge pairs are left to solve_hinge_px."""
    cap = YPX[size]["cap_px"]
    top, base = YPX[size]["top"], YPX[size]["top"] + cap
    depth = DEPTH * cap / 100
    seq = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]

    def g(a, b):
        return o.pair_gap(px[a], px[b], cap_top=top, base=base, step=0.05, depth=depth)
    target = (g("O", "A")["area"] + g("A2", "C")["area"]) / 2
    log = {}
    for a, b in zip(seq, seq[1:]):
        if "&" in (a, b):
            continue
        cur = g(a, b)
        best = None
        for dx in range(-6, 7):
            if cur["min"] + dx < floor_px - 1e-6:
                continue
            sc = abs(cur["area"] + dx - target)
            if best is None or sc < best[0]:
                best = (sc, dx)
        dx = best[1] if best else 0
        if dx:
            for n in seq[seq.index(b):]:
                px[n] = o.tx(px[n], e=dx)
        log[f"{a.rstrip('2')}{b.rstrip('2')}"] = dx
    return round(target, 2), log


def solve_hinge_px(px, size, floor_px):
    """Move the ampersand by whole pixels so the white on its two sides matches best, keeping
    floor_px of clear space on each side; then move ACTION if the right side needs room."""
    cap = YPX[size]["cap_px"]
    top, base = YPX[size]["top"], YPX[size]["top"] + cap
    depth = DEPTH * cap / 100
    best = None
    for dx in range(-8, 9):
        a = o.tx(px["&"], e=dx)
        l = o.pair_gap(px["H"], a, cap_top=top, base=base, step=0.05, depth=depth)
        r = o.pair_gap(a, px["A2"], cap_top=top, base=base, step=0.05, depth=depth)
        if l["min"] < floor_px:
            continue
        need = max(0, math.ceil(floor_px - r["min"] - 1e-6))
        score = abs(l["area"] - (r["area"] + need)) + need * 0.25
        if best is None or score < best[0]:
            best = (score, dx, need)
    _, dx, need = best
    px["&"] = o.tx(px["&"], e=dx)
    seq = ["A2", "C", "T2", "I", "O2", "N"]
    for n in seq:
        px[n] = o.tx(px[n], e=need)
    return dx, need


def enforce_gaps(px_parts, min_px, size):
    """Push glyphs right so that every neighbour gap (nearest ink, in px) is at least min_px[pair]."""
    seq = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]
    total = 0
    for a, b in zip(seq, seq[1:]):
        need = min_px.get((a, b), min_px.get("*", 1.0))
        g = o.pair_gap(px_parts[a], px_parts[b], cap_top=0.5, base=size - 0.5, step=0.05, depth=3)
        if g["min"] < need:
            dx = math.ceil(need - g["min"] - 1e-6)
            idx = seq.index(b)
            for n in seq[idx:]:
                px_parts[n] = o.tx(px_parts[n], e=dx)
            total += dx
    return total


def build():
    DIR2.mkdir(parents=True, exist_ok=True)
    DIR3.mkdir(parents=True, exist_ok=True)
    G, amp = glyphs()
    res = {"model": {"depth_x": DEPTH / 100, "floor_x": FLOOR / 100}}
    v5 = place(G, amp, {}, 0.0, 0.0)
    res["v5"] = measures(v5)
    # item 2a: literal 0.10x nearest ink on both sides
    l = gap(G["H"], amp)
    r = gap(amp, G["A2"])
    e_lit = round(10.0 - r["min"], 2)
    d_lit = round(10.0 - l["min"], 2)
    lit = place(G, amp, {}, d_lit, e_lit + d_lit)
    res["hinge_literal"] = {"amp_shift": d_lit, "action_shift": round(e_lit + d_lit, 2), **measures(lit)}
    # item 2b: optical
    d, e, lg, rg = solve_hinge(G["H"], amp, G["A2"])
    opt = place(G, amp, {}, d, e)
    res["hinge_optical"] = {"amp_shift": d, "action_shift": e, **measures(opt)}
    W = 970.71
    for nm, parts, extra in (("Literal-0.10x", lit, e_lit + d_lit), ("Optical", opt, e)):
        vb = [0, 0, round(W + extra, 2), 108]
        o.write_svg(DIR2 / f"20261021_Wordmark-Hinge-{nm}.svg", vb, to_svg(parts, vb), f"Wordmark, hinge gaps {nm.lower()} (proposal, Phase 1)")
    res["files_item2"] = [str((DIR2 / f"20261021_Wordmark-Hinge-{nm}.svg").relative_to(o.ROOT)) for nm in ("Literal-0.10x", "Optical")]
    # item 3: display master = optical hinge + pair adjustments
    adj = spacing_display(G, amp)
    disp = place(G, amp, adj, d, e)
    res["display_master"] = {"pair_adjustments_units": {f"{a}{b}".replace("2", ""): v for (a, b), v in adj.items()}, **measures(disp)}
    bx = o.bounds(o.union(*disp.values()))
    vb = [0, 0, round(bx[2], 2), 108]
    o.write_svg(DIR3 / "20261021_Wordmark-Display-Master.svg", vb, to_svg(disp, vb), "Wordmark, display master (proposal, Phase 1)")
    res["display_master"]["viewBox"] = vb
    # small masters
    amp16 = A.a16()                    # 15 x 16 px, already on the pixel grid
    for size in (24, 16):
        parts = place(G, amp, adj, d, e, track=TRACK[size], t_trim=T_TRIM[size])
        a_px = amp16 if size == 16 else None
        px = pixel_master(parts, size, a_px if size == 16 else None)
        if size == 24:
            # display tune ampersand scaled to the 24 px box
            tune = A.a_display()
            tb = o.bounds(tune)
            s = 24 / (tb[3] - tb[1])
            q = o.tx(tune, a=s, d=-s, e=-tb[0] * s, f=tb[3] * s)
            ab = o.bounds(parts["&"])
            cx = (ab[0] + ab[2]) / 2 * YPX[24]["cap_px"] / 100
            qb = o.bounds(q)
            px["&"] = o.tx(q, e=round(cx - (qb[2] - qb[0]) / 2))
        minimum = {"*": 1.0 if size == 24 else 1.0, ("T", "H"): 2.0, ("T2", "I"): 2.0, ("H", "&"): 2.0, ("&", "A2"): 1.0}
        spacing_px = space_px(px, size)
        hinge_px = solve_hinge_px(px, size, 1.5 if size == 16 else 2.0)
        pushed = enforce_gaps(px, minimum, size)
        bx = o.bounds(o.union(*px.values()))
        vb = [0, 0, math.ceil(bx[2]), size]
        o.write_svg(DIR3 / f"20261021_Wordmark-{size}px-Master.svg", vb, to_svg(px, vb, nd=3), f"Wordmark, {size} px master on the pixel grid (proposal, Phase 1)")
        m = {}
        seq = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]
        for a_, b_ in zip(seq, seq[1:]):
            g = o.pair_gap(px[a_], px[b_], cap_top=1, base=1 + YPX[size]["cap_px"], step=0.05, depth=DEPTH * YPX[size]["cap_px"] / 100)
            m[f"{a_.rstrip('2')}{b_.rstrip('2')}"] = {"nearest_px": round(g["min"], 2), "area_px": round(g["area"], 2)}
        res[f"master_{size}"] = {"viewBox": vb, "track_units": TRACK[size], "t_arm_trim_units": T_TRIM[size], "pushed_px": pushed, "hinge_px_shift": hinge_px, "area_target_px_and_shifts": spacing_px, "pairs": m}
    return res


if __name__ == "__main__":
    r = build()
    (o.SCRATCH / "specs").mkdir(parents=True, exist_ok=True)
    (o.SCRATCH / "specs/wordmark.json").write_text(json.dumps(r, indent=1))
    print(json.dumps(r, indent=1)[:4000])
