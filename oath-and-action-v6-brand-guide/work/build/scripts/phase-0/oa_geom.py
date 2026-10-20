"""Shared outline helpers for the Phase 0 geometry scripts."""
import math
import re
from pathlib import Path

NUM = r"-?\d*\.?\d+(?:e-?\d+)?"


def parse_path(d, steps=24):
    """Absolute M L H V Q C A Z only (the sprite uses no relative commands).
    Returns a list of closed polylines."""
    toks = re.findall(r"[MLHVQCAZ]|" + NUM, d)
    subs, cur, x, y, sx, sy = [], [], 0.0, 0.0, 0.0, 0.0
    i, cmd = 0, None
    while i < len(toks):
        t = toks[i]
        if re.match("[A-Z]", t):
            cmd = t
            i += 1
            if cmd == "Z":
                if cur:
                    subs.append(cur)
                cur = []
                x, y = sx, sy
            continue
        v = lambda k: float(toks[i + k])
        if cmd == "M":
            if cur:
                subs.append(cur)
            x, y = v(0), v(1)
            sx, sy = x, y
            cur = [(x, y)]
            i += 2
            cmd = "L"
        elif cmd == "L":
            x, y = v(0), v(1)
            cur.append((x, y))
            i += 2
        elif cmd == "H":
            x = v(0)
            cur.append((x, y))
            i += 1
        elif cmd == "V":
            y = v(0)
            cur.append((x, y))
            i += 1
        elif cmd == "Q":
            cx, cy, ex, ey = v(0), v(1), v(2), v(3)
            for s in range(1, steps + 1):
                tt = s / steps
                px = (1 - tt) ** 2 * x + 2 * (1 - tt) * tt * cx + tt * tt * ex
                py = (1 - tt) ** 2 * y + 2 * (1 - tt) * tt * cy + tt * tt * ey
                cur.append((px, py))
            x, y = ex, ey
            i += 4
        elif cmd == "C":
            c1x, c1y, c2x, c2y, ex, ey = [v(k) for k in range(6)]
            for s in range(1, steps + 1):
                tt = s / steps
                mt = 1 - tt
                px = mt**3 * x + 3 * mt * mt * tt * c1x + 3 * mt * tt * tt * c2x + tt**3 * ex
                py = mt**3 * y + 3 * mt * mt * tt * c1y + 3 * mt * tt * tt * c2y + tt**3 * ey
                cur.append((px, py))
            x, y = ex, ey
            i += 6
        elif cmd == "A":
            # endpoints only are enough for bbox work on these glyph files
            x, y = v(5), v(6)
            cur.append((x, y))
            i += 7
        else:
            i += 1
    if cur:
        subs.append(cur)
    return [s for s in subs if len(s) > 2]


def xform(poly, tx=0.0, ty=0.0, s=1.0, sy=None):
    sy = s if sy is None else sy
    return [(tx + px * s, ty + py * sy) for px, py in poly]


def bbox(polys):
    xs = [p[0] for poly in polys for p in poly]
    ys = [p[1] for poly in polys for p in poly]
    return [min(xs), min(ys), max(xs), max(ys)]


def group_glyphs(polys):
    """Group sub-paths whose bbox sits inside another sub-path's bbox."""
    boxes = [bbox([p]) for p in polys]
    order = sorted(range(len(polys)), key=lambda k: -(boxes[k][2] - boxes[k][0]) * (boxes[k][3] - boxes[k][1]))
    groups = []
    for k in order:
        b = boxes[k]
        for g in groups:
            gb = g["box"]
            if b[0] >= gb[0] - 0.01 and b[2] <= gb[2] + 0.01 and b[1] >= gb[1] - 0.01 and b[3] <= gb[3] + 0.01:
                g["polys"].append(polys[k])
                break
        else:
            groups.append({"box": b, "polys": [polys[k]]})
    groups.sort(key=lambda g: g["box"][0])
    return groups


def crossings(polys, y):
    xs = []
    for poly in polys:
        n = len(poly)
        for j in range(n):
            (x1, y1), (x2, y2) = poly[j], poly[(j + 1) % n]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    return sorted(xs)


def vcrossings(polys, x):
    ys = []
    for poly in polys:
        n = len(poly)
        for j in range(n):
            (x1, y1), (x2, y2) = poly[j], poly[(j + 1) % n]
            if (x1 <= x < x2) or (x2 <= x < x1):
                ys.append(y1 + (x - x1) * (y2 - y1) / (x2 - x1))
    return sorted(ys)


def profiles(polys, y0, y1, step=0.25):
    rows = []
    y = y0 + step / 2
    while y < y1:
        xs = crossings(polys, y)
        rows.append((y, (xs[0], xs[-1]) if xs else None))
        y += step
    return rows


def pair_metrics(ga, gb, cap_top, base, step=0.25, depth_caps=(10, 20, 30)):
    pa = profiles(ga, cap_top, base, step)
    pb = profiles(gb, cap_top, base, step)
    gaps = []
    for (y, ra), (_, rb) in zip(pa, pb):
        if ra and rb:
            gaps.append((y, rb[0] - ra[1]))
    gmin = min(g for _, g in gaps)
    ymin = [y for y, g in gaps if abs(g - gmin) < 1e-6][0]
    mid = min(gaps, key=lambda t: abs(t[0] - (cap_top + base) / 2))[1]
    out = {"min_gap": round(gmin, 2), "min_gap_at_y": round(ymin, 2), "gap_at_mid": round(mid, 2)}
    band = base - cap_top
    for dc in depth_caps:
        area = sum(min(g, gmin + dc) for _, g in gaps) * step
        out[f"mean_gap_depthcap_{dc}"] = round(area / band, 2)
    return out


def strip_defs(s):
    if "<defs>" in s:
        s = s[: s.find("<defs>")] + s[s.find("</defs>") + 7 :]
    return s


def viewbox(s):
    return [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]


def collect_polys(svg):
    """Return list of (polys, is_amp) for every <path> in the symbol body,
    applying translate/scale transforms written on the path."""
    out = []
    for m in re.finditer(r"<path([^>]*)/>", svg):
        attrs = m.group(1)
        d = re.search(r' d="([^"]+)"', attrs)
        if not d:
            continue
        polys = parse_path(d.group(1))
        t = re.search(r'transform="translate\((' + NUM + r") (" + NUM + r")\) scale\((" + NUM + r") (" + NUM + r")\)", attrs)
        is_amp = False
        if t:
            tx, ty, s1, s2 = [float(t.group(k)) for k in range(1, 5)]
            polys = [xform(p, tx, ty, s1, s2) for p in polys]
            is_amp = True
        out.append((polys, is_amp))
    return out


