"""Shared paths and helpers for the Phase 2 identity masters (design director, October 28, 2026).

Phase 2 builds on the Phase 1 geometry library (oa_p1, oa_stroke) and the Phase 1 drawing
modules, loaded from work/build/scripts/phase-1 by explicit path because python3 -I drops the
script folder from sys.path. Masters are written to work/build/assets/identity/, board renders to
work/boards/phase-2/identity/, and working files to the session scratchpad.

Run every Phase 2 script with python3 -I.
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P1 = HERE.parent / "phase-1"
for _p in (str(P1), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
if "/root/.local/lib/python3.13/site-packages" not in sys.path:
    sys.path.append("/root/.local/lib/python3.13/site-packages")

import oa_p1 as o  # noqa: E402
import pathops  # noqa: E402

ROOT = o.ROOT
ASSETS = ROOT / "work/build/assets/identity"
BOARD_DIR = ROOT / "work/boards/phase-2/identity"
HANDOFF = ROOT / "work/handoffs/phase-2"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/p2")
DATE = "20261028"

RED, CHAR, NEWS, PRUS, STONE, WHITE, VERD = o.RED, o.CHAR, o.NEWS, o.PRUS, o.STONE, o.WHITE, o.VERD
SURFACES = o.SURFACES  # (id, label, background, ink)


def asset(*parts):
    p = ASSETS.joinpath(*parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def write_svg(path, vb, body, title, extra=""):
    """Write a master. Fills use currentColor and the CSS hooks --amp, --lever, --link and --line,
    so one file serves every surface; explicit-color variants are written separately."""
    path.parent.mkdir(parents=True, exist_ok=True)
    vbs = " ".join(o._fmt(v, 3) for v in vb)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vbs}"{extra}><title>{title}</title>{body}</svg>\n')
    return path


def svg_parts(path):
    s = Path(path).read_text()
    vb = o.viewbox(s)
    s = re.sub(r"<title>.*?</title>", "", s)
    inner = s[s.find(">") + 1: s.rfind("</svg>")]
    inner = inner.replace('<g color="#E63946">', '<g style="color:var(--amp,#E63946)">')
    return inner, vb


def rel(p):
    return str(Path(p).relative_to(ROOT))


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1))


def load_json(path):
    return json.loads(Path(path).read_text())


def render(jobs, outdir, tag):
    """Chromium at device scale 1, through the Phase 1 renderer (absolute file paths only)."""
    SCRATCH.mkdir(parents=True, exist_ok=True)
    jp = SCRATCH / f"jobs_{tag}.json"
    jp.write_text(json.dumps(jobs))
    Path(outdir).mkdir(parents=True, exist_ok=True)
    subprocess.run(["node", str(P1 / "render_cells_p1.js"), str(jp), str(outdir)], check=True)


def path_d(d):
    return o.path_from_d(d)


def contours(p):
    out = []
    for c in p.contours:
        q = pathops.Path()
        c.draw(q.getPen())
        out.append(q)
    return out


def node_count(p):
    n = 0
    for verb, pts in p.segments:
        if verb in ("lineTo", "curveTo", "qCurveTo"):
            n += 1
    return n


def to_shapely(p, steps=64):
    """pathops path to a shapely (Multi)Polygon with holes, by even-odd nesting."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    rings = [Polygon(r) for r in o.polyline(p, steps=steps)]
    rings = [r if r.is_valid else r.buffer(0) for r in rings]
    rings.sort(key=lambda g: -g.area)
    depth = []
    for i, r in enumerate(rings):
        d = sum(1 for j in range(i) if rings[j].contains(r.representative_point()))
        depth.append(d)
    geom = None
    for r, d in zip(rings, depth):
        geom = r if geom is None else (geom.union(r) if d % 2 == 0 else geom.difference(r))
    return geom


def chord(geom, pt, ang_deg):
    """Stroke width at pt: the chord perpendicular to the travel direction ang_deg, through pt,
    clipped to the ink, keeping the piece that contains pt."""
    from shapely.geometry import LineString, Point
    a = math.radians(ang_deg + 90)
    L = 2000
    line = LineString([(pt[0] - L * math.cos(a), pt[1] - L * math.sin(a)), (pt[0] + L * math.cos(a), pt[1] + L * math.sin(a))])
    inter = geom.intersection(line)
    parts = [inter] if inter.geom_type == "LineString" else list(getattr(inter, "geoms", []))
    P = Point(pt)
    best = None
    for s in parts:
        if s.geom_type != "LineString":
            continue
        if s.distance(P) < 1e-6:
            best = s
            break
    return round(best.length, 1) if best is not None else None


def seg_intersect(p1, p2, p3, p4):
    """Intersection of lines p1-p2 and p3-p4."""
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-12:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def coverage_np(img, bg, ink):
    import numpy as np
    a = np.asarray(img.convert("RGB"), dtype=float)
    bgc = np.array(o.hexrgb(bg), dtype=float)
    inkc = np.array(o.hexrgb(ink), dtype=float)
    d = inkc - bgc
    c = ((a - bgc) @ d) / max(1e-9, float(d @ d))
    return np.clip(c, 0, 1)


def crisp_share(img, bg, ink):
    """D1-17: share of ink pixels (coverage over 0.1) that are crisp (coverage over 0.9)."""
    c = coverage_np(img, bg, ink)
    m = c > 0.1
    n = int(m.sum())
    return round(float((c[m] > 0.9).sum()) / n, 3) if n else None
