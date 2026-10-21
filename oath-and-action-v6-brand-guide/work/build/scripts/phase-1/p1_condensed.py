"""Item 6. A condensed wordmark exploration, drawn from Inter Tight 800's own letters.

Method: each capital of the V5 wordmark (Inter Tight 800 outlines, SIL OFL 1.1) is narrowed
by a horizontal scale s, then the stems get back the weight the scale took (a horizontal-only
embolden), the horizontal bars are thinned so stems and bars keep Inter Tight's 1.2 to 1 ratio,
and the cap band is restored. Terminals, the A's flat apex and the C's horizontal cuts stay
Inter Tight's. No OFL condensed family is used. The ampersand is option B narrowed to 0.85.

Two widths are drawn, about 7.5 and 6.5 cap heights wide, and judged by the 16 px test (do the
O, A and C counters stay open, do stems land on whole pixels). The chosen width gets display,
24 px and 16 px masters, each spaced for its size, with equal hinge gaps.

Run: python3 -I p1_condensed.py
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o  # noqa: E402
import p1_amp_a as A  # noqa: E402
import p1_amp_b as B  # noqa: E402
import p1_wordmark as W  # noqa: E402

DIR = o.OUT / "06-condensed"
VARIANTS = {
    "7.5": {"s": 0.63, "stem": 21.0, "bar_thin": 2.4, "target_area": 13.0},
    "6.5": {"s": 0.52, "stem": 19.5, "bar_thin": 2.8, "target_area": 11.5},
}
SIGN_Y = {"cap": 1, "base": -1, "o_in_top": -1, "o_in_bot": 1, "t_bar_bot": -1, "h_bar_top": 1, "h_bar_bot": -1,
          "a_bar_top": 1, "a_bar_bot": -1, "c_term_top": -1, "c_term_bot": 1}
SIGN_X = {"O": [-1, 1, -1, 1], "A": [-1, 1, -1, 1, -1, 1], "T": [-1, -1, 1, 1], "H": [-1, 1, -1, 1],
          "C": [-1, 1, 1], "I": [-1, 1], "N": [-1, 1, -1, 1]}
GROW_Y = 0.3   # the elliptical pen needs a little height; the bar thinning takes it back


def condense(g, name, v):
    """Return the condensed glyph (left ink at 0) and its edge spec for pixel fitting."""
    base = W.SAME.get(name, (name, 0.0))
    spec = W.EDGES[base[0]]
    off = base[1]
    b = o.bounds(g)
    s = v["s"]
    stem0 = 24.1
    dx = (v["stem"] - stem0 * s) / 2
    q = o.tx(g, a=s, e=-b[0] * s)
    q = A.ell_embolden(q, dx, GROW_Y)
    t2 = v["bar_thin"] / 2
    q = A.shrink(o.simplify(q), 0.05, t2)
    # restore the cap band 4..104 (and the overshoot band with it)
    r = 100.0 / (100.0 + 2 * (GROW_Y - t2))
    q = o.tx(q, d=r, f=54 - 54 * r)
    qb = o.bounds(q)
    q = o.tx(q, e=-qb[0])
    # edges
    xs = [(x + off - b[0]) * s + sg * dx + (dx - 0) for x, sg in zip(spec["x"], SIGN_X[base[0]])]
    xs = [x - (xs[0]) for x in xs]
    ys = {}
    for yu, zone in spec["y"].items():
        ys[54 + (yu + SIGN_Y[zone] * (t2 - GROW_Y) - 54) * r] = zone
    sp = {"x": xs, "stems": spec["stems"], "y": ys}
    return o.simplify(q), sp


def build_variant(key, v, amp_scale=0.85):
    G, _ = W.glyphs()
    cg, specs = {}, {}
    for n in W.NAMES:
        cg[n], specs[n] = condense(G[n], n, v)
    # ampersand: option B narrowed, at the letters' cap height (ink = cap plus overshoot)
    bg = B.narrow(B.glyph(), amp_scale)
    bb = o.bounds(bg)
    amp = B.to_symbol(bg, bb[0])
    amp = o.tx(amp, f=4.0)  # cap line at y = 4, as the wordmark
    # spacing: area model, each pair to the variant's target, nearest no closer than 0.05x
    seq = ["O", "A", "T", "H", "&", "A2", "C", "T2", "I", "O2", "N"]
    placed, prof, x = {}, {}, 0.0
    prev = None
    for n in seq:
        g = amp if n == "&" else cg[n]
        gb = o.bounds(g)
        g0 = o.tx(g, e=-gb[0])
        prof[n] = o.Profile(g0)
        if prev is None:
            placed[n], pos = g0, {n: 0.0}
            prev = n
            continue
        target = v["target_area"] if "&" not in (prev, n) else 15.0
        lo, hi = pos[prev] - 40, pos[prev] + 160
        for _ in range(40):
            mid = (lo + hi) / 2
            gp = o.gap_profiles(prof[prev], prof[n], mid - pos[prev], W.DEPTH)
            if gp["area"] < target:
                lo = mid
            else:
                hi = mid
        x = (lo + hi) / 2
        gp = o.gap_profiles(prof[prev], prof[n], x - pos[prev], W.DEPTH)
        if gp["min"] < 5.0:
            x += 5.0 - gp["min"]
        pos[n] = x
        placed[n] = o.tx(g0, e=x)
        prev = n
    # hinge: equal areas
    d, e, lg, rg = W.solve_hinge(placed["H"], placed["&"], placed["A2"])
    placed["&"] = o.tx(placed["&"], e=d)
    for n in ["A2", "C", "T2", "I", "O2", "N"]:
        placed[n] = o.tx(placed[n], e=e)
    return placed, specs


def measures(parts):
    m = W.measures(parts)
    bx = o.bounds(o.union(*parts.values()))
    m["ratio_width_to_cap"] = round((bx[2] - bx[0]) / 100, 2)
    m["ratio_width_to_ink_height"] = round((bx[2] - bx[0]) / (bx[3] - bx[1]), 2)
    return m


def pixel_master(parts, specs, size, v):
    yp = W.YPX[size]
    k = yp["cap_px"] / 100.0
    stem_px = max(2, round(v["stem"] * k))
    out = {}
    for n in ["O", "A", "T", "H", "A2", "C", "T2", "I", "O2", "N"]:
        g = parts[n]
        b = o.bounds(g)
        sp = specs[n]
        left_px = round(b[0] * k)
        tgt = {}
        xs = [x + b[0] for x in sp["x"]]
        for i, x in enumerate(xs):
            tgt[i] = left_px + round((x - xs[0]) * k)
        for a_, b_ in sp["stems"]:
            tgt[b_] = tgt[a_] + stem_px
        pairs, last = [], -1e9
        for i, x in enumerate(xs):
            t = max(tgt[i], last + 1)
            pairs.append((x * k, t))
            last = t
        q = o.tx(g, a=k, d=k)
        q = A.xwarp(q, pairs)
        ypairs = []
        for yu, zone in sorted(sp["y"].items()):
            t = yp["top"] if zone == "cap" else (yp["top"] + yp["cap_px"] if zone == "base" else yp[zone])
            ypairs.append((yu * k, t))
        out[n] = A.ywarp(q, ypairs)
    ab = o.bounds(parts["&"])
    s = size / (ab[3] - ab[1])
    q = o.tx(parts["&"], a=s, d=s)
    qb = o.bounds(q)
    cx = (ab[0] + ab[2]) / 2 * k
    out["&"] = o.tx(q, e=round(cx - (qb[2] - qb[0]) / 2) - qb[0], f=-qb[1])
    W.space_px(out, size)
    W.solve_hinge_px(out, size, 1.5 if size == 16 else 2.0)
    return out


def sixteen_test(parts, specs, v, key):
    """Render the variant at 16 px tall (unhinted, as a browser would) and measure the counters."""
    bx = o.bounds(o.union(*parts.values()))
    vb = [0, 0, round(bx[2], 2), 108]
    body = W.to_svg(parts, vb)
    h = 16
    w = h * vb[2] / vb[3]
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(map(str, vb))}" width="{w:.3f}" height="{h}" style="left:0;top:0;color:#121212;--amp:#121212">{body}</svg>'
    od = o.SCRATCH / "condensed16"
    o.render([{"id": key, "w": math.ceil(w), "h": h, "bg": o.NEWS, "html": svg}], od, "c16" + key)
    from PIL import Image
    img = Image.open(od / f"{key}.png").convert("RGB")
    cov = o.coverage(img, o.NEWS, o.CHAR)
    sc = h / 108
    res = {}
    for n in ("O", "A", "C", "O2", "H"):
        b = o.bounds(parts[n])
        cx = (b[0] + b[2]) / 2 * sc
        y0, y1 = (30 * sc, 78 * sc) if n != "A" else (40 * sc, 60 * sc)
        col = int(cx)
        vals = [cov[y][col] for y in range(int(y0), int(y1)) if 0 <= y < img.height]
        res[n] = round(1 - sum(vals) / len(vals), 2) if vals else None
    return {"counter_openness_at_16px": res, "width_px_at_16px_tall": round(w, 1)}


def build():
    DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    built = {}
    for key, v in VARIANTS.items():
        parts, specs = build_variant(key, v)
        built[key] = (parts, specs)
        bx = o.bounds(o.union(*parts.values()))
        vb = [0, 0, round(bx[2], 2), 108]
        fn = DIR / f"20261021_Wordmark-Condensed-{key.replace('.', '-')}-To-1-Display.svg"
        o.write_svg(fn, vb, W.to_svg(parts, vb), f"Condensed wordmark exploration, {key} to 1 (proposal, Phase 1)")
        out[key] = {"params": v, "viewBox": vb, "file": str(fn.relative_to(o.ROOT)), **measures(parts), **sixteen_test(parts, specs, v, key.replace('.', '_'))}
    # choose by the 16 px test: the variant whose worst counter is most open
    choice = max(out, key=lambda k: min(v for v in out[k]["counter_openness_at_16px"].values() if v is not None))
    out["chosen"] = choice
    parts, specs = built[choice]
    for size in (24, 16):
        px = pixel_master(parts, specs, size, VARIANTS[choice])
        bx = o.bounds(o.union(*px.values()))
        vb = [0, 0, math.ceil(bx[2]), size]
        fn = DIR / f"20261021_Wordmark-Condensed-{choice.replace('.', '-')}-To-1-{size}px.svg"
        o.write_svg(fn, vb, W.to_svg(px, vb, nd=3), f"Condensed wordmark, {size} px master (proposal, Phase 1)")
        out[f"master_{size}"] = {"viewBox": vb, "file": str(fn.relative_to(o.ROOT))}
    return out


if __name__ == "__main__":
    r = build()
    (o.SCRATCH / "specs/condensed.json").write_text(json.dumps(r, indent=1))
    print(json.dumps({k: (v if k == "chosen" else {kk: vv for kk, vv in v.items() if kk in ("viewBox", "ratio_width_to_cap", "ratio_width_to_ink_height", "counter_openness_at_16px", "width_px_at_16px_tall", "H&", "&A")}) for k, v in r.items()}, indent=1))
