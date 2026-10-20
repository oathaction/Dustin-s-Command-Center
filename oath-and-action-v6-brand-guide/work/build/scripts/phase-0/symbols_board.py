"""Phase 0 symbol audit: pillar marks and the twenty topic icons from the V5 Polished sprite.

Parses every ic-* master (48, 24, 16), tabulates stroke widths, caps, joins, corner
radii and accent use, checks 16 and 24 px coordinates against the pixel grid for
their stroke width, renders everything with Chromium at device scale 1, measures
crispness and similarity, and writes a diagnostic board.

Run: python3 -I symbols_board.py <ROOT> <SCRATCH> [--skip-render]
"""
import base64
import io
import json
import math
import re
import subprocess
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image  # noqa: E402

ROOT = Path(sys.argv[1])
SCRATCH = Path(sys.argv[2])
SPRITE = ROOT / "work/extract/v5-polished/sprite"
HERE = Path(__file__).resolve().parent
OUT_HTML = ROOT / "work/boards/phase-0/20261020_Symbol-Pixel-Fit-And-Similarity-Diagnostic.html"
RDIR = SCRATCH / "symbol-renders"
RED, CHAR, NEWS, PRUS, STONE, WHITE, VERD = "#E63946", "#121212", "#DCD9D2", "#1F2D5A", "#5D636D", "#FFFFFF", "#4A7C74"
SURFACES = [("newsprint", "Newsprint", NEWS, CHAR), ("white", "White", WHITE, CHAR),
            ("charcoal", "Charcoal", CHAR, NEWS), ("prussian", "Prussian", PRUS, WHITE)]
TOPICS = ["ballot", "ranked-ballot", "open-primary", "district-map", "state-house", "bill", "committee-hearing",
          "roll-call-vote", "court", "campaign-money", "local-government", "public-records", "housing",
          "work-and-wages", "taxes-and-budget", "health-care", "cost-of-living", "contact-an-official", "testify", "organize"]
PILLARS = ["explain", "track", "connect", "act"]
PAIRS = [("bill", "public-records"), ("court", "state-house"), ("testify", "contact-an-official"),
         ("housing", "cost-of-living"), ("ballot", "ranked-ballot"), ("ballot", "open-primary"), ("ranked-ballot", "open-primary")]
NUM = r"-?\d*\.?\d+"


def attrs(tag):
    return dict(re.findall(r'([\w:-]+)="([^"]*)"', tag))


def path_segments(d):
    toks = re.findall(r"[MLHVACQZ]|" + NUM, d)
    segs, i, cmd = [], 0, None
    x = y = sx = sy = 0.0
    while i < len(toks):
        t = toks[i]
        if re.match("[A-Z]", t):
            cmd = t
            i += 1
            if cmd == "Z":
                if (x, y) != (sx, sy):
                    segs.append(("L", (x, y), (sx, sy)))
                x, y = sx, sy
            continue
        f = lambda k: float(toks[i + k])
        if cmd == "M":
            x, y = f(0), f(1); sx, sy = x, y; i += 2; cmd = "L"
        elif cmd == "L":
            segs.append(("L", (x, y), (f(0), f(1)))); x, y = f(0), f(1); i += 2
        elif cmd == "H":
            segs.append(("L", (x, y), (f(0), y))); x = f(0); i += 1
        elif cmd == "V":
            segs.append(("L", (x, y), (x, f(0)))); y = f(0); i += 1
        elif cmd == "A":
            segs.append(("A", (x, y), (f(5), f(6)), (f(0), f(1)))); x, y = f(5), f(6); i += 7
        elif cmd == "Q":
            segs.append(("Q", (x, y), (f(2), f(3)))); x, y = f(2), f(3); i += 4
        elif cmd == "C":
            segs.append(("C", (x, y), (f(4), f(5)))); x, y = f(4), f(5); i += 6
        else:
            i += 1
    return segs


def is_int(v, tol=0.02):
    return abs(v - round(v)) < tol


def parse_icon(name):
    s = (SPRITE / f"{name}.svg").read_text()
    size = int(name.rsplit("-", 1)[1]) if name.startswith("ic-") else 100
    scale = 0.5 if 'transform="scale(.5)"' in s else 1.0
    if 'scale(1.235)' in s:
        scale = 1.235
    els = []
    for m in re.finditer(r"<(path|rect|circle|line)\b([^>]*)/?>", s):
        kind, a = m.group(1), attrs(m.group(2))
        stroke = a.get("stroke", "none")
        fill = a.get("fill", "#000" if kind != "line" else "none")
        sw = float(a.get("stroke-width", "1")) * scale if stroke != "none" else 0.0
        els.append({"kind": kind, "a": a, "stroked": stroke != "none", "filled": fill not in ("none",),
                    "sw": sw, "accent": "var(--dot" in (stroke + fill) or "var(--pc" in (stroke + fill)})
    return s, size, scale, els


def grid_check(els, scale):
    """Axis-aligned edges on whole pixels for the element's stroke width (px units)."""
    total = ok = 0
    off = []
    curves = curves_ok = 0
    for e in els:
        a = e["a"]
        if e["kind"] == "path":
            for seg in path_segments(a["d"]):
                (x1, y1), (x2, y2) = seg[1], seg[2]
                x1, y1, x2, y2 = x1 * scale, y1 * scale, x2 * scale, y2 * scale
                if seg[0] != "L":
                    continue
                if abs(y1 - y2) < 1e-6 or abs(x1 - x2) < 1e-6:
                    c = y1 if abs(y1 - y2) < 1e-6 else x1
                    if e["stroked"]:
                        edges = (c - e["sw"] / 2, c + e["sw"] / 2)
                    else:
                        edges = (c,)
                    total += 1
                    good = all(is_int(v) for v in edges)
                    ok += good
                    if not good:
                        off.append(f'{"H" if abs(y1 - y2) < 1e-6 else "V"} edge at {c:g}, w {e["sw"]:g}')
        elif e["kind"] == "rect":
            x, y, w, h = (float(a[k]) * scale for k in ("x", "y", "width", "height"))
            edges = [x, x + w, y, y + h]
            if e["stroked"]:
                edges = [v + d for v in edges for d in (-e["sw"] / 2, e["sw"] / 2)]
            for v in edges:
                total += 1
                ok += is_int(v)
            if not all(is_int(v) for v in edges):
                off.append(f"rect {x:g},{y:g} {w:g}x{h:g}")
        elif e["kind"] == "circle":
            cx, cy, r = (float(a[k]) * scale for k in ("cx", "cy", "r"))
            ext = [cx - r, cx + r, cy - r, cy + r]
            if e["stroked"]:
                ext = [v + d for v in ext for d in (-e["sw"] / 2, e["sw"] / 2)]
            curves += 1
            curves_ok += all(is_int(v, 0.05) for v in ext)
        elif e["kind"] == "line":
            x1, y1, x2, y2 = (float(a[k]) * scale for k in ("x1", "y1", "x2", "y2"))
            if abs(y1 - y2) < 1e-6 or abs(x1 - x2) < 1e-6:
                c = y1 if abs(y1 - y2) < 1e-6 else x1
                edges = (c - e["sw"] / 2, c + e["sw"] / 2)
                total += 1
                good = all(is_int(v) for v in edges)
                ok += good
                if not good:
                    off.append(f"line at {c:g}, w {e['sw']:g}")
    return {"axis_edges": total, "on_grid": ok, "share": round(ok / total, 2) if total else None,
            "circles": curves, "circles_on_grid": curves_ok, "off_examples": off[:4]}


def radii(els, scale):
    out = set()
    for e in els:
        a = e["a"]
        if e["kind"] == "rect" and float(a.get("rx", "0")) > 0:
            out.add(round(float(a["rx"]) * scale, 2))
        if e["kind"] == "path":
            for seg in path_segments(a["d"]):
                if seg[0] == "A":
                    out.add(round(seg[3][0] * scale, 2))
        if e["kind"] == "circle":
            out.add(f"circle r{round(float(a['r']) * scale, 2)}")
    return sorted(out, key=str)


def tabulate():
    rows = {}
    for t in TOPICS:
        for sz in (48, 24, 16):
            name = f"ic-{t}-{sz}"
            s, size, scale, els = parse_icon(name)
            sws = sorted({round(e["sw"], 2) for e in els if e["stroked"]})
            caps = sorted({e["a"].get("stroke-linecap", "butt") for e in els if e["stroked"]})
            joins = sorted({e["a"].get("stroke-linejoin", "miter") for e in els if e["stroked"]})
            acc = [e for e in els if e["accent"]]
            acc_desc = ", ".join(f'{e["kind"]} {"stroke " + format(e["sw"], "g") if e["stroked"] else "fill"}' for e in acc)
            row = {"strokes_px": sws, "caps": caps, "joins": joins, "radii_px": radii(els, scale),
                   "filled": sum(e["filled"] and not e["stroked"] for e in els), "stroked": sum(e["stroked"] for e in els),
                   "accent": acc_desc, "accent_count": len(acc), "scaled_from_48": scale == 0.5}
            if sz in (16, 24):
                row["grid"] = grid_check(els, scale)
            rows[name] = row
    return rows


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def symbol_markup(name, w, h, css):
    s = (SPRITE / f"{name}.svg").read_text()
    s = re.sub(r"<title>.*?</title>", "", s)
    return re.sub(r'<svg ([^>]*?)style="color:#121212"', lambda m: f'<svg {m.group(1)}width="{w}" height="{h}" style="color:inherit;{css}"', s, count=1)


def jobs():
    out = []
    for t in TOPICS:
        for sz in (48, 24, 16):
            for surf in SURFACES:
                for mode in ("plain", "act"):
                    css = f"--dot:{RED};" if mode == "act" else ""
                    out.append({"id": f"ic-{t}-{sz}__{surf[0]}__{mode}", "w": sz, "h": sz, "bg": surf[2], "fg": surf[3],
                                "html": symbol_markup(f"ic-{t}-{sz}", sz, sz, css)})
    for p in PILLARS:
        for var in ("", "-s"):
            for sz in (16, 18, 24, 28, 32, 48, 96):
                for surf in SURFACES:
                    for mode in ("color", "mono"):
                        dark = surf[0] in ("charcoal", "prussian")
                        if mode == "mono":
                            css = "--pc:currentColor;"
                        else:
                            css = "--pc:currentColor;" if (dark and p != "act") else ""
                            if p == "act" and dark:
                                css = f"--pc:{RED};"
                        out.append({"id": f"pm-{p}{var}-{sz}__{surf[0]}__{mode}", "w": sz, "h": sz, "bg": surf[2], "fg": surf[3],
                                    "html": symbol_markup(f"pm-{p}{var}", sz, sz, css)})
    for u in ("menu", "close", "search", "arrow", "download", "external"):
        for sz in (16, 24):
            out.append({"id": f"ui-{u}-{sz}__newsprint__plain", "w": sz, "h": sz, "bg": NEWS, "fg": CHAR,
                        "html": symbol_markup(f"ui-{u}", sz, sz, "")})
    return out


def cov(img, bg, fg):
    b, f = hexrgb(bg), hexrgb(fg)
    d = [f[i] - b[i] for i in range(3)]
    dd = sum(v * v for v in d)
    px = img.load()
    return [[max(0.0, min(1.0, sum((px[x, y][i] - b[i]) * d[i] for i in range(3)) / dd)) for x in range(img.width)] for y in range(img.height)]


def load(id_):
    return Image.open(RDIR / f"{id_}.png").convert("RGB")


def crisp(c):
    ink = [v for row in c for v in row if v > 0.1]
    return round(sum(v > 0.9 for v in ink) / len(ink), 2) if ink else None, round(sum(map(sum, c)) / (len(c) * len(c[0])), 3)


def silhouette(mask):
    h, w = len(mask), len(mask[0])
    seen = [[False] * w for _ in range(h)]
    stack = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    while stack:
        x, y = stack.pop()
        if 0 <= x < w and 0 <= y < h and not seen[y][x] and not mask[y][x]:
            seen[y][x] = True
            stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [[mask[y][x] or not seen[y][x] for x in range(w)] for y in range(h)]


def iou(a, b):
    inter = sum(1 for y in range(len(a)) for x in range(len(a[0])) if a[y][x] and b[y][x])
    uni = sum(1 for y in range(len(a)) for x in range(len(a[0])) if a[y][x] or b[y][x])
    return inter / uni if uni else 0


def blur(c):
    h, w = len(c), len(c[0])
    return [[sum(c[yy][xx] for yy in range(max(0, y - 1), min(h, y + 2)) for xx in range(max(0, x - 1), min(w, x + 2))) / 9 for x in range(w)] for y in range(h)]


def corr(a, b):
    fa = [v for r in a for v in r]
    fb = [v for r in b for v in r]
    ma, mb = sum(fa) / len(fa), sum(fb) / len(fb)
    num = sum((x - ma) * (y - mb) for x, y in zip(fa, fb))
    den = math.sqrt(sum((x - ma) ** 2 for x in fa) * sum((y - mb) ** 2 for y in fb))
    return num / den if den else 0


def analyse():
    res = {"crisp": {}, "similarity": {}, "pillars": {}, "utility": {}}
    covs = {}
    for t in TOPICS:
        for sz in (16, 24, 48):
            c = cov(load(f"ic-{t}-{sz}__white__plain"), WHITE, CHAR)
            covs[(t, sz)] = c
            res["crisp"][f"{t} {sz}"] = crisp(c)
    for sz in (16, 24):
        scores = []
        for a, b in combinations(TOPICS, 2):
            ca, cb = covs[(a, sz)], covs[(b, sz)]
            ma = [[v > 0.5 for v in r] for r in ca]
            mb = [[v > 0.5 for v in r] for r in cb]
            s_iou = iou(silhouette(ma), silhouette(mb))
            b_corr = corr(blur(ca), blur(cb))
            scores.append({"a": a, "b": b, "silhouette_iou": round(s_iou, 2), "blurred_corr": round(b_corr, 2),
                           "score": round((s_iou + b_corr) / 2, 3)})
        scores.sort(key=lambda r: -r["score"])
        for k, r in enumerate(scores):
            r["rank"] = k + 1
        res["similarity"][sz] = {"top": scores[:12],
                                 "pairs": [next(r for r in scores if {r["a"], r["b"]} == set(p)) for p in PAIRS],
                                 "n": len(scores)}
    for p in PILLARS:
        for var in ("", "-s"):
            for sz in (16, 24, 32, 48, 96):
                c = cov(load(f"pm-{p}{var}-{sz}__white__mono"), WHITE, CHAR)
                cr, density = crisp(c)
                ys = [y for y in range(len(c)) for x in range(len(c[0])) if c[y][x] > 0.5]
                xs = [x for y in range(len(c)) for x in range(len(c[0])) if c[y][x] > 0.5]
                tot = sum(map(sum, c))
                cx = sum(c[y][x] * x for y in range(len(c)) for x in range(len(c[0]))) / tot
                cy = sum(c[y][x] * y for y in range(len(c)) for x in range(len(c[0]))) / tot
                res["pillars"][f"{p}{var} {sz}"] = {
                    "crisp": cr, "ink_density": density,
                    "bbox_share": [round(min(xs) / sz, 2), round(min(ys) / sz, 2), round((max(xs) + 1) / sz, 2), round((max(ys) + 1) / sz, 2)] if xs else None,
                    "centroid_offset": [round(cx / sz - 0.5 + 0.5 / sz, 3), round(cy / sz - 0.5 + 0.5 / sz, 3)]}
    for u in ("menu", "close", "search", "arrow", "download", "external"):
        for sz in (16, 24):
            res["utility"][f"{u} {sz}"] = crisp(cov(load(f"ui-{u}-{sz}__newsprint__plain"), NEWS, CHAR))
    # pillar silhouettes compared with each other at 16 px, and with nearby glyphs
    sil = {}
    for p in PILLARS:
        c = cov(load(f"pm-{p}-s-16__white__mono"), WHITE, CHAR)
        sil[p] = c
    pp = []
    for a, b in combinations(PILLARS, 2):
        pp.append({"a": a, "b": b, "blurred_corr": round(corr(blur(sil[a]), blur(sil[b])), 2),
                   "silhouette_iou": round(iou(silhouette([[v > 0.5 for v in r] for r in sil[a]]), silhouette([[v > 0.5 for v in r] for r in sil[b]])), 2)})
    res["pillar_pairs_16"] = pp
    return res


def b64(img, scale=1):
    if scale != 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tile(id_, label, z=1, grid=False):
    img = load(id_)
    w, h = img.width * z, img.height * z
    im = f'<img class="px" src="{b64(img)}" width="{w}" height="{h}" alt="{esc(label)}">'
    if grid:
        im = f'<span class="gw" style="--g:{z}px">{im}</span>'
    return f'<figure class="c"><div class="sw">{im}</div><figcaption>{esc(label)}</figcaption></figure>'


def board(table_rows, meas):
    font_dir = "../../extract/v5-polished/fonts/"
    css = f"""
@font-face{{font-family:InterB;src:url('{font_dir}Inter-400-normal.ttf');font-weight:400}}
@font-face{{font-family:InterB;src:url('{font_dir}Inter-600-normal.ttf');font-weight:600}}
@font-face{{font-family:InterB;src:url('{font_dir}Inter-Tight-800-normal.ttf');font-weight:800}}
*{{box-sizing:border-box}} body{{margin:0;background:#F3F2EE;color:#121212;font:15px/1.5 InterB,Inter,system-ui,sans-serif}}
main{{max-width:1880px;margin:0 auto;padding:40px 32px 80px}}
h1{{font:800 44px/1.05 InterB,sans-serif;letter-spacing:-0.02em;margin:0 0 12px}}
h2{{font:800 28px/1.15 InterB,sans-serif;margin:56px 0 12px;padding-top:20px;border-top:1px solid #C9C6BE}}
h3{{font:600 18px/1.3 InterB,sans-serif;margin:28px 0 6px}}
p{{max-width:72ch;margin:0 0 12px}} .note{{color:#4A4F57;font-size:14px}}
code{{font:13px ui-monospace,monospace;background:#E6E4DE;padding:1px 5px;border-radius:3px}}
table{{border-collapse:collapse;margin:8px 0 18px;font-size:13.5px}}
th,td{{border-bottom:1px solid #C9C6BE;padding:5px 10px 5px 0;text-align:left;vertical-align:top}}
th{{font-weight:600}} td.n{{font-variant-numeric:tabular-nums;text-align:right}}
.cells{{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;margin:6px 0 14px}}
.c{{margin:0}} .c figcaption{{font-size:13px;color:#4A4F57;margin-top:3px;max-width:260px}}
.sw{{display:inline-block;line-height:0;border:1px solid #C9C6BE}}
img{{display:block}} img.px{{image-rendering:pixelated}}
.gw{{position:relative;display:inline-block;line-height:0}}
.gw::after{{content:"";position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(to right,rgba(31,45,90,.3) 1px,transparent 1px),linear-gradient(to bottom,rgba(31,45,90,.3) 1px,transparent 1px);background-size:var(--g) var(--g)}}
.row{{display:grid;grid-template-columns:170px 1fr;gap:12px;border-bottom:1px solid #C9C6BE;padding:10px 0}}
.bad{{color:#A3121F;font-weight:600}}
"""
    h = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Symbol Pixel-Fit Diagnostic</title><style>{css}</style></head><body><main>"]
    h.append("<p class='note'>Oath &amp; Action Brand Guide, Edition 06. Phase 0 review board, October 20, 2026. Design director. Diagnosis only.</p>")
    h.append("<h1>Pillar marks and topic icons</h1><p>V5 Polished sprite masters, rendered by Chromium at device scale 1. Zooms use nearest-neighbour scaling with a one-pixel grid drawn over them. Scripts: <code>work/build/scripts/phase-0/symbols_board.py</code>.</p>")
    # pillars
    h.append("<h2>1. Pillar marks</h2><p>Standard masters (<code>pm-*</code>) and simplified masters (<code>pm-*-s</code>, V5 uses them below 32 px). 1x at 16, 18, 24, 28, 32, 48 and 96 px; 16 and 24 px again at 8x.</p>")
    for surf in SURFACES:
        for mode in ("color", "mono"):
            cells = []
            for p in PILLARS:
                for var in ("-s", ""):
                    for sz in (16, 18, 24, 28, 32, 48, 96):
                        cells.append(tile(f"pm-{p}{var}-{sz}__{surf[0]}__{mode}", f"{p}{var} {sz}"))
            h.append(f"<div class='row'><div><b>{surf[1]}</b><br><span class='note'>{'color' if mode == 'color' else 'one color'}</span></div><div class='cells'>{''.join(cells)}</div></div>")
    cells = []
    for p in PILLARS:
        for var in ("-s", ""):
            for sz in (16, 24):
                cells.append(tile(f"pm-{p}{var}-{sz}__newsprint__color", f"{p}{var} {sz} px at 8x", 8, True))
    h.append(f"<h3>16 and 24 px at 8x, Newsprint, color</h3><div class='cells'>{''.join(cells)}</div>")
    pr = meas["pillars"]
    trs = "".join(f"<tr><td>{esc(k)}</td><td class='n'>{v['crisp']}</td><td class='n'>{v['ink_density']}</td><td class='n'>{v['bbox_share']}</td><td class='n'>{v['centroid_offset']}</td></tr>" for k, v in pr.items() if k.endswith((" 16", " 24", " 96")))
    h.append(f"<table><thead><tr><th>Mark, size</th><th>Crisp share</th><th>Ink density</th><th>Ink box (share of field)</th><th>Centroid offset from centre</th></tr></thead><tbody>{trs}</tbody></table>")
    trs = "".join(f"<tr><td>{r['a']} / {r['b']}</td><td class='n'>{r['blurred_corr']}</td><td class='n'>{r['silhouette_iou']}</td></tr>" for r in meas["pillar_pairs_16"])
    h.append(f"<h3>Pillar pairs at 16 px (simplified masters)</h3><table><thead><tr><th>Pair</th><th>Blurred correlation</th><th>Silhouette overlap</th></tr></thead><tbody>{trs}</tbody></table>")
    # icon table
    h.append("<h2>2. Topic icons: construction table</h2><p>Stroke widths are in screen pixels at the master's own size. The 24 px masters are the 48-unit drawings scaled by 0.5. Grid: axis-aligned edges that land on whole pixels for their stroke width, then circles whose extremes land on whole pixels.</p>")
    trs = ""
    for name, r in table_rows.items():
        g = r.get("grid")
        gtxt = f"{g['on_grid']}/{g['axis_edges']} ({g['share']}); circles {g['circles_on_grid']}/{g['circles']}" if g else ""
        bad = " class='bad'" if g and g["share"] is not None and g["share"] < 1 else ""
        trs += (f"<tr><td>{name}</td><td class='n'>{', '.join(format(v, 'g') for v in r['strokes_px'])}</td><td>{'/'.join(r['caps'])}</td><td>{'/'.join(r['joins'])}</td>"
                f"<td>{esc(', '.join(map(str, r['radii_px'])))}</td><td class='n'>{r['filled']}/{r['stroked']}</td><td>{esc(r['accent'])}</td><td{bad}>{gtxt}</td><td>{esc('; '.join(g['off_examples'])) if g else ''}</td></tr>")
    h.append(f"<table><thead><tr><th>Icon</th><th>Strokes px</th><th>Caps</th><th>Joins</th><th>Radii px</th><th>Filled/stroked</th><th>Accent</th><th>Pixel grid</th><th>Off-grid examples</th></tr></thead><tbody>{trs}</tbody></table>")
    # icon tiles
    h.append("<h2>3. Topic icons at 48, 24 and 16 px</h2><p>Each row: 48, 24 and 16 px at 1x on Newsprint and Charcoal with the Act accent in red, then 24 and 16 px at 8x on Newsprint with the pixel grid.</p>")
    for t in TOPICS:
        cells = []
        for surf in ("newsprint", "charcoal", "prussian", "white"):
            for sz in (48, 24, 16):
                cells.append(tile(f"ic-{t}-{sz}__{surf}__act", f"{sz} {surf}"))
        for sz in (24, 16):
            cells.append(tile(f"ic-{t}-{sz}__newsprint__plain", f"{sz} at 8x", 8, True))
        h.append(f"<div class='row'><div><b>{t}</b><br><span class='note'>crisp share 16: {meas['crisp'][t + ' 16'][0]}, 24: {meas['crisp'][t + ' 24'][0]}</span></div><div class='cells'>{''.join(cells)}</div></div>")
    # similarity
    h.append("<h2>4. Similarity</h2><p>Score is the mean of two measures on the one-color renders: overlap of the filled silhouettes (counters filled in) and correlation after a 3 by 3 blur, which approximates a glance. Rank is out of 190 pairs; rank 1 is the most alike.</p>")
    for sz in (16, 24):
        sim = meas["similarity"][sz]
        trs = "".join(f"<tr><td>{r['a']} / {r['b']}</td><td class='n'>{r['silhouette_iou']}</td><td class='n'>{r['blurred_corr']}</td><td class='n'>{r['score']}</td><td class='n'>{r['rank']}</td></tr>" for r in sim["pairs"])
        h.append(f"<h3>Named pairs at {sz} px</h3><table><thead><tr><th>Pair</th><th>Silhouette overlap</th><th>Blurred correlation</th><th>Score</th><th>Rank of 190</th></tr></thead><tbody>{trs}</tbody></table>")
        trs = "".join(f"<tr><td>{r['a']} / {r['b']}</td><td class='n'>{r['silhouette_iou']}</td><td class='n'>{r['blurred_corr']}</td><td class='n'>{r['score']}</td></tr>" for r in sim["top"])
        h.append(f"<h3>Twelve most alike at {sz} px</h3><table><thead><tr><th>Pair</th><th>Silhouette overlap</th><th>Blurred correlation</th><th>Score</th></tr></thead><tbody>{trs}</tbody></table>")
    cells = []
    for a, b in PAIRS + [(r["a"], r["b"]) for r in meas["similarity"][16]["top"][:5]]:
        for sz in (16, 24):
            cells.append(tile(f"ic-{a}-{sz}__newsprint__plain", f"{a} {sz}", 6, True))
            cells.append(tile(f"ic-{b}-{sz}__newsprint__plain", f"{b} {sz}", 6, True))
        cells.append("<div style='flex-basis:100%;height:0'></div>")
    h.append(f"<h3>Side by side at 6x</h3><div class='cells'>{''.join(cells)}</div>")
    # utility
    cells = [tile(f"ui-{u}-{sz}__newsprint__plain", f"ui-{u} {sz}", 8, True) for u in ("menu", "close", "search", "arrow", "download", "external") for sz in (16, 24)]
    h.append(f"<h2>5. Utility glyphs</h2><p>Six glyphs on a 24-unit field with a 2-unit stroke. At 16 px the stroke becomes 1.33 px.</p><div class='cells'>{''.join(cells)}</div>")
    h.append("</main></body></html>")
    OUT_HTML.write_text("".join(h))
    return OUT_HTML


if __name__ == "__main__":
    rows = tabulate()
    if "--skip-render" not in sys.argv:
        jp = SCRATCH / "symbol_jobs.json"
        jp.write_text(json.dumps(jobs()))
        subprocess.run(["node", str(HERE / "render_cells.js"), str(jp), str(RDIR)], check=True)
    meas = analyse()
    (SCRATCH / "symbols_audit.json").write_text(json.dumps({"table": rows, "measures": meas}, indent=1, default=str))
    p = board(rows, meas)
    print("board", p, p.stat().st_size)
