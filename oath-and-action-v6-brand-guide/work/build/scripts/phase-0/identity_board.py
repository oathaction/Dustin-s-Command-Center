"""Phase 0 identity small-size diagnostic board.

Renders the V5 Polished identity symbols at 16, 24, 48, 96 px height and a display
size, on four surfaces, in color and one color, measures the rasters, and writes
an HTML board with the 1x renders and 4x nearest-neighbour zooms.

Run: python3 -I identity_board.py <ROOT> <SCRATCH>
"""
import base64
import io
import json
import math
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image  # noqa: E402
from oa_geom import collect_polys, crossings, group_glyphs, strip_defs  # noqa: E402

ROOT = Path(sys.argv[1])
SCRATCH = Path(sys.argv[2])
SPRITE = ROOT / "work/extract/v5-polished/sprite"
HERE = Path(__file__).resolve().parent
OUT_HTML = ROOT / "work/boards/phase-0/20261020_Identity-Small-Size-Diagnostic.html"
GEOM = json.loads((SCRATCH / "identity_geometry.json").read_text())
RENDER_DIR = SCRATCH / "identity-renders"

RED, CHAR, NEWS, PRUS, STONE, WHITE, VERD = "#E63946", "#121212", "#DCD9D2", "#1F2D5A", "#5D636D", "#FFFFFF", "#4A7C74"
SURFACES = [("newsprint", "Newsprint", NEWS, CHAR), ("white", "White", WHITE, CHAR),
            ("charcoal", "Charcoal", CHAR, NEWS), ("prussian", "Prussian", PRUS, WHITE)]
MODES = [("color", "Color"), ("mono", "One color")]
SIZES = [16, 24, 48, 96]
ELEMENTS = [
    # name, label, display height
    ("wordmark", "Wordmark (L1)", 160),
    ("wordmark-mono", "Wordmark mono", 160),
    ("stacked", "Stacked (L2)", 240),
    ("monogram", "Monogram (L8)", 200),
    ("amp", "Master ampersand", 320),
    ("amp-16", "Ampersand, 16 px drawing", 320),
    ("lockmark", "Lockmark (Signal Grid)", 320),
    ("hinge", "Hinge diagram", 360),
]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def symbol_markup(name, w, h, css_vars):
    s = (SPRITE / f"{name}.svg").read_text()
    s = re.sub(r"<title>.*?</title>", "", s)
    s = re.sub(r'<svg ([^>]*?)style="color:#121212"',
               lambda m: f'<svg {m.group(1)}width="{w:.3f}" height="{h}" style="color:inherit;{css_vars}"', s, count=1)
    if name == "hinge":
        body_start = s.find("</defs>")
        body = s[body_start:].replace('<g color="#E63946">', '<g style="color:var(--hamp,#E63946)">')
        s = s[:body_start] + body
    return s


def vars_for(name, surface, mode):
    sid = surface[0]
    dark = sid in ("charcoal", "prussian")
    if mode == "mono":
        return "--amp:currentColor;--link:currentColor;--lever:currentColor;--hinge-line:currentColor;--hamp:currentColor;"
    v = f"--amp:{RED};--lever:{RED};--hamp:{RED};"
    v += "--hinge-line:currentColor;" if dark else f"--hinge-line:{STONE};"
    v += f"--link:{WHITE};" if sid == "prussian" else f"--link:{STONE};"
    if name in ("amp", "amp-16"):
        v += f"color:{RED};"
    return v


def vb(name):
    s = (SPRITE / f"{name}.svg").read_text()
    return [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]


def build_jobs():
    jobs = []
    for name, _, disp in ELEMENTS:
        v = vb(name)
        for surf in SURFACES:
            for mode, _ in MODES:
                if name == "wordmark-mono" and mode == "color":
                    continue
                for h in SIZES + [disp]:
                    w = h * v[2] / v[3]
                    jobs.append({"id": f"{name}__{surf[0]}__{mode}__{h}", "w": math.ceil(w), "h": h, "bg": surf[2], "fg": surf[3],
                                 "html": symbol_markup(name, w, h, vars_for(name, surf, mode))})
    # unclipped copies for the clipping panel
    for name, h in [("amp", 400), ("tl-1", 60), ("url-1", 60)]:
        v = vb(name)
        w = h * v[2] / v[3]
        pad = int(h * 0.3)
        pos = f"position:absolute;left:{pad}px;top:{pad}px;"
        shipped = symbol_markup(name, w, h, pos + f"color:{CHAR};")
        under = symbol_markup(name, w, h, pos + f"color:{RED};").replace("<svg ", '<svg overflow="visible" ', 1)
        jobs.append({"id": f"clip__{name}__shipped", "w": math.ceil(w) + 2 * pad, "h": h + 2 * pad, "bg": NEWS, "fg": CHAR,
                     "html": shipped})
        jobs.append({"id": f"clip__{name}__unclipped", "w": math.ceil(w) + 2 * pad, "h": h + 2 * pad, "bg": NEWS, "fg": CHAR,
                     "html": under + shipped})
    return jobs


def render(jobs):
    jp = SCRATCH / "identity_jobs.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(HERE / "render_cells.js"), str(jp), str(RENDER_DIR)], check=True)


def png(id_):
    return Image.open(RENDER_DIR / f"{id_}.png").convert("RGB")


def b64(img, scale=1):
    if scale != 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# ---------- raster measurements ----------

def coverage_map(img, bg, ink):
    """Estimated ink coverage per pixel, projecting the pixel colour onto the bg->ink line."""
    bgc, inkc = hexrgb(bg), hexrgb(ink)
    d = [inkc[i] - bgc[i] for i in range(3)]
    dd = sum(x * x for x in d)
    px = img.load()
    out = [[0.0] * img.width for _ in range(img.height)]
    for y in range(img.height):
        for x in range(img.width):
            p = px[x, y]
            a = sum((p[i] - bgc[i]) * d[i] for i in range(3)) / dd
            out[y][x] = max(0.0, min(1.0, a))
    return out


def red_edge_stats(img, bg, x0, x1):
    """Contrast of every red ink pixel in columns x0..x1 against the surface."""
    cov = coverage_map(img, bg, RED)
    px = img.load()
    bgc = hexrgb(bg)
    vals, solid = [], 0
    for y in range(img.height):
        for x in range(max(0, int(x0)), min(img.width, int(math.ceil(x1)))):
            a = cov[y][x]
            if a > 0.1:
                vals.append(contrast(px[x, y], bgc))
                solid += a >= 0.9
    vals.sort()
    n = len(vals)
    return {"ink_px": n, "solid_share": round(solid / n, 2) if n else 0,
            "median_contrast": round(vals[n // 2], 2) if n else None,
            "max_contrast": round(vals[-1], 2) if n else None,
            "share_below_3": round(sum(v < 3 for v in vals) / n, 2) if n else None}


def letter_stats(img, bg, fg, x0, x1):
    cov = coverage_map(img, bg, fg)
    vals = [cov[y][x] for y in range(img.height) for x in range(int(x0), min(img.width, int(math.ceil(x1)))) if cov[y][x] > 0.1]
    return {"ink_px": len(vals), "solid_share": round(sum(v >= 0.9 for v in vals) / len(vals), 2)}


def gap_openness(img, bg, fg, x_a, x_b, y_a, y_b, scale):
    """Lightest column between two glyph edges: 1 means full background shows through."""
    cov = coverage_map(img, bg, fg)
    best = 0.0
    xs = range(int(math.floor(x_a * scale)), int(math.ceil(x_b * scale)))
    for x in xs:
        if x < 0 or x >= img.width:
            continue
        col = [cov[y][x] for y in range(int(y_a * scale), int(math.ceil(y_b * scale))) if 0 <= y < img.height]
        if col:
            best = max(best, 1 - sum(col) / len(col))
    return round(best, 2)


def sample(cov, x, y):
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    vals = []
    for yy in (y0, y0 + 1):
        for xx in (x0, x0 + 1):
            if 0 <= yy < len(cov) and 0 <= xx < len(cov[0]):
                vals.append(cov[yy][xx])
    return round(sum(vals) / len(vals), 2)


def analyse():
    res = {"red_edge": {}, "letters": {}, "joins": {}, "amp_counters": {}, "lockmark_lines": {}, "amp_ink": {}}
    W = 970.71
    for surf in SURFACES:
        for h in SIZES:
            img = png(f"wordmark__{surf[0]}__color__{h}")
            s = h / 108
            res["red_edge"][f"wordmark {surf[1]} {h}px"] = red_edge_stats(img, surf[2], 368.72 * s, 460.0 * s + 1)
            if surf[0] == "newsprint":
                res["letters"][f"OATH {h}px"] = letter_stats(img, surf[2], surf[3], 0, 358.67 * s + 1)
    for surf in SURFACES:
        for h in (16, 24):
            for nm in ("amp", "amp-16"):
                img = png(f"{nm}__{surf[0]}__color__{h}")
                res["red_edge"][f"{nm} {surf[1]} {h}px"] = red_edge_stats(img, surf[2], 0, img.width)
    # joins on the wordmark, Newsprint, one colour, so every glyph is Charcoal
    pairs = {"T-H": (265.71, 271.02, 4, 23.66), "T-I": (746.0, 751.31, 4, 23.66), "I-O": (775.4, 782.85, 30, 78),
             "O-N": (878.22, 885.67, 30, 78), "H-&": (358.67, 368.72, 60, 100), "&-A": (460.0, 468.28, 94, 104),
             "C-T": (657.61, 661.57, 4, 23.66)}
    for h in (16, 24, 48):
        img = png(f"wordmark__newsprint__mono__{h}")
        s = h / 108
        res["joins"][f"{h}px"] = {k: gap_openness(img, NEWS, CHAR, a, b, y0, y1, s) for k, (a, b, y0, y1) in pairs.items()}
    # ampersand counters: coverage at the counter centres (0 = open, 1 = filled)
    pts = {"upper counter centre": (283, 531), "upper counter base": (275, 440), "lower counter centre": (262, 175), "lower counter tip": (395, 104), "arm notch": (436, 300)}
    for nm in ("amp", "amp-16"):
        v = vb(nm)
        for h in (16, 24):
            img = png(f"{nm}__newsprint__mono__{h}")
            cov = coverage_map(img, NEWS, CHAR)
            sc = h / v[3]
            out = {}
            for k, (gx, gy) in pts.items():
                x = (-3.16 + gx * 0.14 - v[0]) * sc - 0.5
                y = (98.41 - gy * 0.14 - v[1]) * sc - 0.5
                out[k] = sample(cov, x, y)
            res["amp_counters"][f"{nm} {h}px"] = out
            res["amp_ink"][f"{nm} {h}px"] = round(sum(map(sum, cov)), 1)
    for h in (16, 24, 48):
        img = png(f"lockmark__white__mono__{h}")
        cov = coverage_map(img, WHITE, CHAR)
        s = h / 123.5
        xcol = int(36.75 * s)  # halfway between node columns, on the links only
        lines = []
        for c in (11.75, 61.75, 111.75):
            yc = c * s
            rows = [cov[y][xcol] for y in range(max(0, int(yc) - 2), min(img.height, int(yc) + 3))]
            peak = max(rows)
            spread = sum(r > 0.15 for r in rows)
            lines.append({"center_px": round(yc, 2), "peak_coverage": round(peak, 2), "rows_touched": spread})
        res["lockmark_lines"][f"{h}px"] = lines
    return res


# ---------- board ----------

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def matrix_block(name, label, disp):
    v = vb(name)
    rows = []
    zoom_sizes = [16, 24] + ([48] if v[2] / v[3] < 4 else [])
    for surf in SURFACES:
        for mode, mlabel in MODES:
            if name == "wordmark-mono" and mode == "color":
                continue
            cells = []
            for h in SIZES:
                img = png(f"{name}__{surf[0]}__{mode}__{h}")
                cells.append(f'<figure class="c"><div class="sw" style="background:{surf[2]}"><img src="{b64(img)}" width="{img.width}" height="{img.height}" alt="{esc(label)} at {h} px on {surf[1]}, {mlabel.lower()}"></div><figcaption>{h} px</figcaption></figure>')
            zooms = []
            for h in zoom_sizes:
                img = png(f"{name}__{surf[0]}__{mode}__{h}")
                if name in ("wordmark", "wordmark-mono") and h == 48:
                    continue
                zooms.append(f'<figure class="c"><div class="sw" style="background:{surf[2]}"><img class="px" src="{b64(img)}" width="{img.width * 4}" height="{img.height * 4}" alt="{h} px render at 4x"></div><figcaption>{h} px at 4x</figcaption></figure>')
            if name in ("wordmark", "wordmark-mono"):
                img = png(f"{name}__{surf[0]}__{mode}__48")
                s = 48 / 108
                crop = img.crop((int(181 * s), 0, int(661.6 * s) + 2, img.height))
                zooms.append(f'<figure class="c"><div class="sw" style="background:{surf[2]}"><img class="px" src="{b64(crop)}" width="{crop.width * 4}" height="{crop.height * 4}" alt="48 px render, T to C, at 4x"></div><figcaption>48 px at 4x, T H &amp; A C</figcaption></figure>')
            rows.append(f'<div class="row"><div class="rl"><b>{surf[1]}</b><span>{mlabel}</span></div><div class="cells">{"".join(cells)}</div><div class="cells z">{"".join(zooms)}</div></div>')
    disp_cells = []
    for surf in SURFACES:
        for mode, mlabel in MODES:
            if name == "wordmark-mono" and mode == "color":
                continue
            img = png(f"{name}__{surf[0]}__{mode}__{disp}")
            disp_cells.append(f'<figure class="c"><div class="sw" style="background:{surf[2]}"><img src="{b64(img)}" width="{img.width}" height="{img.height}" alt="{esc(label)} at display size on {surf[1]}, {mlabel.lower()}"></div><figcaption>{surf[1]}, {mlabel.lower()}, {disp} px</figcaption></figure>')
    return (f'<section class="el" id="m-{name}"><h3>{esc(label)} <code>#{name}</code></h3>'
            f'<p class="note">Rows: surface and color mode. First band: actual pixels at 16, 24, 48 and 96 px height. Second band: the same 1x render enlarged 4x with nearest-neighbour scaling, so each square is one screen pixel.</p>'
            f'{"".join(rows)}<h4>Display size</h4><div class="disp">{"".join(disp_cells)}</div></section>')


def spacing_panel():
    wm = strip_defs((SPRITE / "wordmark.svg").read_text())
    parts = collect_polys(wm)
    letters = [p for pp, a in parts if not a for p in pp]
    amp = [p for pp, a in parts if a for p in pp]
    g = group_glyphs(letters)
    seq = [g[0], g[1], g[2], g[3], {"polys": amp}, g[4], g[5], g[6], g[7], g[8], g[9]]
    keys = ["OA", "AT", "TH", "H&", "&A_action", "AC_action", "CT_action", "TI_action", "IO_action", "ON_action"]
    marks = []
    for i, k in enumerate(keys):
        pm = GEOM["pairs"][k]
        y = pm["min_gap_at_y"]
        xa = crossings(seq[i]["polys"], y)[-1]
        xb = crossings(seq[i + 1]["polys"], y)[0]
        marks.append(f'<line x1="{xa:.2f}" y1="{y:.2f}" x2="{xb:.2f}" y2="{y:.2f}" stroke="#2F7BFF" stroke-width="2.4"/>'
                     f'<circle cx="{xa:.2f}" cy="{y:.2f}" r="2.4" fill="#2F7BFF"/><circle cx="{xb:.2f}" cy="{y:.2f}" r="2.4" fill="#2F7BFF"/>')
        cx = (xa + xb) / 2
        lab = k.split("_")[0].replace("&", "&amp;")
        dy = 0 if i % 2 == 0 else 34
        marks.append(f'<line x1="{cx:.1f}" y1="108" x2="{cx:.1f}" y2="{116 + dy}" stroke="{STONE}" stroke-width="0.4"/>'
                     f'<text x="{cx:.1f}" y="{124 + dy}" text-anchor="middle" font-size="8" fill="{CHAR}" font-weight="600">{lab}</text>'
                     f'<text x="{cx:.1f}" y="{133 + dy}" text-anchor="middle" font-size="7.5" fill="{CHAR}">{pm["min_gap"] / 100:.3f}x</text>'
                     f'<text x="{cx:.1f}" y="{142 + dy}" text-anchor="middle" font-size="7.5" fill="{STONE}">{pm["mean_gap_depthcap_20"] / 100:.3f}x</text>')
    body = re.sub(r"<title>.*?</title>", "", wm)
    inner = body[body.find(">") + 1: body.rfind("</svg>")]
    svg = (f'<svg viewBox="-20 -8 1010 192" width="1400" role="img" aria-label="Wordmark with the nearest ink-to-ink gap marked for each letter pair">'
           f'<g style="color:{CHAR};--amp:{RED}" opacity="0.55">{inner}</g>'
           f'<line x1="-20" y1="4" x2="990" y2="4" stroke="{STONE}" stroke-width="0.4" stroke-dasharray="2 2"/>'
           f'<line x1="-20" y1="104" x2="990" y2="104" stroke="{STONE}" stroke-width="0.4" stroke-dasharray="2 2"/>'
           f'{"".join(marks)}</svg>')
    # bar chart of area-based gap
    bars = []
    vals = [(k.split("_")[0], GEOM["pairs"][k]["mean_gap_depthcap_20"] / 100, GEOM["pairs"][k]["min_gap"] / 100) for k in keys]
    maxv = max(v for _, v, _ in vals)
    for i, (k, v, mn) in enumerate(vals):
        x = 60 + i * 64
        hh = v / maxv * 120
        bars.append(f'<rect x="{x}" y="{150 - hh:.1f}" width="34" height="{hh:.1f}" fill="{PRUS if "&" not in k else RED}"/>'
                    f'<text x="{x + 17}" y="{144 - hh:.1f}" text-anchor="middle" font-size="13" fill="{CHAR}">{v:.3f}</text>'
                    f'<text x="{x + 17}" y="170" text-anchor="middle" font-size="13" font-weight="600" fill="{CHAR}">{k.replace("&", "&amp;")}</text>')
    chart = (f'<svg viewBox="0 0 720 180" width="720" role="img" aria-label="Area-based gap for each letter pair, in cap heights">'
             f'<line x1="50" y1="150" x2="700" y2="150" stroke="{CHAR}" stroke-width="1"/>{"".join(bars)}</svg>')
    return svg, chart


def weight_panel():
    m = GEOM["stroke_measures_units"]
    rows = [
        ("Cap stems: H, T, I, N", "24.1", "0.241x"),
        ("Cap bars: H, T", "19.7", "0.197x"),
        ("O sides / O top and bottom", "24.6 / 21.1", "0.246x / 0.211x"),
        ("Ampersand lower bowl, left side", f"{m['amp_lower_bowl_at_glyph_y200'][0]}", "0.187x"),
        ("Ampersand upper loop, sides", f"{m['amp_upper_loop_sides_at_glyph_y530'][0]} / {m['amp_upper_loop_sides_at_glyph_y530'][1]}", "0.169x / 0.161x"),
        ("Ampersand diagonal (perpendicular)", f"{m['amp_diagonal_perpendicular_units']}", "0.164x"),
        ("Ampersand tail", f"{m['amp_tail_at_glyph_x620'][0]}", "0.125x"),
        ("Ampersand bowl bottom / loop top", f"{m['amp_bowl_bottom_and_loop_top_at_glyph_x283'][0]} / {m['amp_bowl_bottom_and_loop_top_at_glyph_x283'][2]}", "0.098x / 0.099x"),
        ("Ampersand right arm / serif", f"{m['amp_arm_at_glyph_y255'][2]} / {m['amp_serif_at_glyph_x560'][0]}", "0.099x / 0.102x"),
    ]
    tr = "".join(f"<tr><td>{esc(a)}</td><td class='n'>{b}</td><td class='n'>{c}</td><td class='n'>{float(b.split(' / ')[0]) * 16 / 108:.2f}</td><td class='n'>{float(b.split(' / ')[0]) * 120 / 970.71:.2f}</td></tr>" for a, b, c in rows)
    return ("<table><thead><tr><th>Stroke</th><th>Units (cap = 100)</th><th>In cap heights</th><th>px at 16 px tall</th><th>px at V5 minimum (120 px wide)</th></tr></thead>"
            f"<tbody>{tr}</tbody></table>")


def clip_panel():
    out = []
    for name, cap in [("amp", "Master ampersand at 400 px. The viewBox cuts 1.83 units off the top of the loop and 1.72 units off the tail."),
                      ("tl-1", "Tagline symbol tl-1. The viewBox ends at 108 units and the descenders run to 132.6, so y and p lose their tails."),
                      ("url-1", "URL symbol url-1. The g of .org loses its tail.")]:
        a = png(f"clip__{name}__shipped")
        b = png(f"clip__{name}__unclipped")
        out.append(f'<figure class="c"><div class="pair"><img src="{b64(a)}" width="{a.width}" height="{a.height}" alt="{name} as shipped"><img src="{b64(b)}" width="{b.width}" height="{b.height}" alt="{name} with overflow visible"></div>'
                   f'<figcaption><b>Left:</b> as V5 ships it. <b>Right:</b> the shipped symbol over a red copy drawn with overflow visible; the red shows what the viewBox cuts away. {esc(cap)}</figcaption></figure>')
    return "".join(out)


def joins_panel():
    figs = []
    for h in (16, 24):
        img = png(f"wordmark__newsprint__color__{h}")
        figs.append(f'<figure class="c"><div class="sw" style="background:{NEWS}"><img class="px" src="{b64(img)}" width="{img.width * 8}" height="{img.height * 8}" alt="wordmark {h} px at 8x"></div><figcaption>Wordmark, {h} px, 8x. Look at T to H, T to I, I to O to N, and the arm of the ampersand.</figcaption></figure>')
    for nm in ("amp", "amp-16"):
        for h in (16, 24):
            img = png(f"{nm}__newsprint__mono__{h}")
            figs.append(f'<figure class="c"><div class="sw" style="background:{NEWS}"><span class="gw" style="--g:12px"><img class="px" src="{b64(img)}" width="{img.width * 12}" height="{img.height * 12}" alt="{nm} {h} px at 12x"></span></div><figcaption>{nm}, {h} px, 12x</figcaption></figure>')
    return "".join(figs)


def lock_panel():
    figs = []
    for h in (16, 24, 48):
        for mode in ("color", "mono"):
            img = png(f"lockmark__newsprint__{mode}__{h}")
            z = 12 if h < 48 else 6
            figs.append(f'<figure class="c"><div class="sw" style="background:{NEWS}"><span class="gw" style="--g:{z}px"><img class="px" src="{b64(img)}" width="{img.width * z}" height="{img.height * z}" alt="lockmark {h} px {mode} at {z}x"></span></div><figcaption>Lockmark {h} px, {"color" if mode == "color" else "one color"}, {z}x</figcaption></figure>')
    return "".join(figs)


def table(d, cols):
    head = "".join(f"<th>{esc(c)}</th>" for c in ["Item"] + cols)
    body = ""
    for k, v in d.items():
        body += f"<tr><td>{esc(k)}</td>" + "".join(f"<td class='n'>{v.get(c, '')}</td>" for c in cols) + "</tr>"
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def build_board(meas):
    font_dir = "../../extract/v5-polished/fonts/"
    g = GEOM
    spacing_svg, spacing_chart = spacing_panel()
    joins = meas["joins"]
    jrows = {k: v for k, v in joins.items()}
    lock = meas["lockmark_lines"]
    lrows = {f"{k}, line {i + 1}": {"center px": l["center_px"], "peak coverage": l["peak_coverage"], "rows touched": l["rows_touched"]}
             for k, ls in lock.items() for i, l in enumerate(ls)}
    css = f"""
@font-face{{font-family:InterB;src:url('{font_dir}Inter-400-normal.ttf');font-weight:400}}
@font-face{{font-family:InterB;src:url('{font_dir}Inter-600-normal.ttf');font-weight:600}}
@font-face{{font-family:InterB;src:url('{font_dir}Inter-Tight-800-normal.ttf');font-weight:800}}
:root{{--bg:#F3F2EE;--ink:#121212;--muted:#4A4F57;--rule:#C9C6BE}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 InterB,Inter,system-ui,sans-serif}}
main{{max-width:1880px;margin:0 auto;padding:40px 32px 80px}}
h1{{font:800 44px/1.05 InterB,sans-serif;letter-spacing:-0.02em;margin:0 0 12px}}
h2{{font:800 28px/1.15 InterB,sans-serif;letter-spacing:-0.01em;margin:56px 0 12px;padding-top:20px;border-top:1px solid var(--rule)}}
h3{{font:600 20px/1.3 InterB,sans-serif;margin:40px 0 6px}}
h4{{font:600 15px/1.3 InterB,sans-serif;margin:22px 0 8px}}
p{{max-width:70ch;margin:0 0 12px}}
.lede{{font-size:18px;max-width:72ch}}
.note{{color:var(--muted);font-size:14px}}
code{{font:13px ui-monospace,monospace;background:#E6E4DE;padding:1px 5px;border-radius:3px}}
table{{border-collapse:collapse;margin:8px 0 18px;font-size:14px}}
th,td{{border-bottom:1px solid var(--rule);padding:6px 12px 6px 0;text-align:left;vertical-align:top}}
th{{font-weight:600}}
td.n{{font-variant-numeric:tabular-nums;text-align:right}}
.row{{display:grid;grid-template-columns:110px 1fr;gap:6px 16px;padding:12px 0;border-bottom:1px solid var(--rule)}}
.row .z{{grid-column:2}}
.rl b{{display:block;font-weight:600}} .rl span{{color:var(--muted);font-size:14px}}
.cells{{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end}}
.c{{margin:0}}
.c figcaption{{font-size:13px;color:var(--muted);margin-top:4px;max-width:520px}}
.sw{{padding:10px;display:inline-block;line-height:0;border:1px solid var(--rule)}}
img{{display:block}}
img.px{{image-rendering:pixelated;image-rendering:crisp-edges}}
.gw{{position:relative;display:inline-block;line-height:0}}
.gw::after{{content:"";position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(to right,rgba(31,45,90,.28) 1px,transparent 1px),linear-gradient(to bottom,rgba(31,45,90,.28) 1px,transparent 1px);background-size:var(--g,12px) var(--g,12px)}}
.disp{{display:flex;flex-wrap:wrap;gap:16px}}
.pair{{display:flex;gap:12px;flex-wrap:wrap;line-height:0}}
.panel{{display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start}}
.facts li{{margin-bottom:6px;max-width:95ch}}
.toc a{{color:var(--ink)}}
"""
    a = g["amp_overshoot"]
    re_ = meas["red_edge"]
    counters = meas["amp_counters"]
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Identity Small-Size Diagnostic</title><style>{css}</style></head><body><main>
<p class="note">Oath &amp; Action Brand Guide, Edition 06. Phase 0 review board, October 20, 2026. Design director. Diagnosis only: nothing on this board proposes a change.</p>
<h1>Identity at small sizes</h1>
<p class="lede">Every mark here is the V5 Polished vector master from the inline sprite, extracted to <code>work/extract/v5-polished/sprite/</code>. Each is rendered by Chromium at device scale 1 and shown at its true pixels, then enlarged with nearest-neighbour scaling so you can see what the screen draws. Measurements come from the outlines themselves (<code>work/build/scripts/phase-0/identity_geometry.py</code>) and from the rasters (<code>identity_board.py</code>). x means one cap height of the wordmark, 100 units.</p>
<p class="note">Companion board: <a href="20261020_Symbol-Pixel-Fit-And-Similarity-Diagnostic.html">pillar marks and topic icons</a>. Audit note: <code>work/handoffs/phase-0/20261020_Design-Director-Audit.md</code>.</p>
<p class="toc">Panels: <a href="#spacing">1 Spacing</a> · <a href="#weight">2 Ampersand weight</a> · <a href="#joins">3 Joins at small sizes</a> · <a href="#red">4 Red edge contrast</a> · <a href="#clip">5 Clipped outlines</a> · <a href="#amp16">6 The 16 px ampersand</a> · <a href="#lock">7 Lockmark pixel fit</a> · <a href="#min">8 Stated minimums</a> · <a href="#matrix">9 Full matrix</a></p>

<h2 id="spacing">1. Letterspacing and kerning across O A T H &amp; A C T I O N</h2>
<p>The letters are stock Inter Tight 800 outlines. Spacing is the font's own advance widths with a uniform tracking of minus 2 percent of the em, plus the font's kerning on O to A, A to C (minus 3.8 percent) and A to T (minus 9.1 percent). C to T, T to H, T to I, I to O and O to N carry tracking only. The two hinge gaps are set by hand.</p>
{spacing_svg}
<p class="note">Blue bars mark the nearest ink-to-ink point of each pair. Under each pair: label, nearest gap in cap heights, then the area-based gap in grey (white area between the two outlines across the cap band, depth capped at 0.2x, divided by the cap height). The area-based figure tracks what the eye reads as spacing.</p>
{spacing_chart}
<ul class="facts">
<li>Left hinge, H to &amp;: nearest gap {g['pairs']['H&']['min_gap'] / 100:.3f}x, area-based {g['pairs']['H&']['mean_gap_depthcap_20'] / 100:.3f}x. Right hinge, &amp; to A: nearest gap {g['pairs']['&A_action']['min_gap'] / 100:.3f}x, area-based {g['pairs']['&A_action']['mean_gap_depthcap_20'] / 100:.3f}x. V5 states 0.10x on each side. The right side measures 0.083x at the baseline and reads about 32 percent more open, because the A's diagonal leaves a wedge of space above the tail.</li>
<li>I to O and O to N are the tightest pairs: {g['pairs']['IO_action']['min_gap'] / 100:.3f}x nearest, {g['pairs']['IO_action']['mean_gap_depthcap_20'] / 100:.3f}x area-based. A to T is the most open at {g['pairs']['AT']['mean_gap_depthcap_20'] / 100:.3f}x. The range is close to 2 to 1, so ACTION's right half reads denser than OATH.</li>
<li>T to H and T to I leave {g['pairs']['TH']['min_gap'] / 100:.3f}x between the bar and the stem: 0.79 px at 16 px tall and 1.18 px at 24 px.</li>
<li>Monogram: O to &amp; nearest gap {g['monogram']['O_amp']['min_gap'] / 100:.3f}x, &amp; to A {g['monogram']['amp_A']['min_gap'] / 100:.3f}x. Area-based {g['monogram']['O_amp']['mean_gap_depthcap_20'] / 100:.3f}x and {g['monogram']['amp_A']['mean_gap_depthcap_20'] / 100:.3f}x. The monogram is balanced by eye even though its two measured gaps differ.</li>
<li>Stacked: the ampersand is {g['stacked']['amp_height_over_cap']}x the cap height, sits right of ACTION and straddles the line gap of 0.10x. The reading order becomes OATH ACTION &amp;.</li>
</ul>

<h2 id="weight">2. Ampersand weight against the capitals</h2>
<p>The ampersand outline is the Lora Bold glyph, unmodified: all 120 coordinate pairs match the font embedded in V5, scaled by 0.14. V5 describes it as redrawn. Its ink height is {a['ink_height_x']}x. It sits {a['above_cap_x']}x above the cap line and {a['below_base_x']}x below the baseline. The O overshoots by 0.013x at both ends. V5 states 0.02x above and below.</p>
{weight_panel()}
<p class="note">The ampersand's thick strokes reach 0.69 to 0.78 of the cap stems. Its thin strokes are 0.41 of the stems and half the cap bars. Thick to thin contrast is about 1.9 to 1 inside the ampersand against 1.22 to 1 in the letters, so the red glyph reads lighter than the black words beside it, and its hairlines are the first part to break up at small sizes.</p>

<h2 id="joins">3. Joins that clog</h2>
<p>Lightest column between neighbouring glyphs, measured on the one-color render on Newsprint. 1.00 means a full column of background shows between the two shapes. Below about 0.5 the eye sees the two shapes touch.</p>
{table(jrows, list(next(iter(jrows.values())).keys()))}
<p>Ampersand interior coverage at four points (0 is open background, 1 is solid ink), one color on Newsprint:</p>
{table(counters, list(next(iter(counters.values())).keys()))}
<div class="panel">{joins_panel()}</div>

<h2 id="red">4. Red edge contrast</h2>
<p>Pillar Red measures 2.96:1 on Newsprint, 4.17:1 on White, 4.49:1 on Charcoal and 3.19:1 on Prussian at full coverage. At small sizes most red pixels are partly covered, so the ampersand's measured contrast falls below the nominal value. Columns: red ink pixels counted, share that are at least 90 percent covered, median and best contrast of those pixels against the surface, and share below 3:1.</p>
{table(re_, ['ink_px', 'solid_share', 'median_contrast', 'max_contrast', 'share_below_3'])}
<p class="note">For comparison, Charcoal letters of OATH on Newsprint: {', '.join(f"{k}: {v['solid_share']} solid" for k, v in meas['letters'].items())}.</p>

<h2 id="clip">5. Outlines clipped by their own viewBox</h2>
<div class="panel">{clip_panel()}</div>
<p class="note">The cut shows wherever V5 uses <code>#amp</code>: the freestanding master, the hinge diagram, container marks above 16 px, watermarks and hinge headlines. L4, L5 and L6 use the tagline and URL symbols, and the 1440 tiles show the clipped descenders (03-identity-01.jpg: "countrv", "peoole", ".orq"). The stacked lockup clips 0.89 units off the ampersand's tail.</p>

<h2 id="amp16">6. The 16 px ampersand</h2>
<p><code>#amp-16</code> is the master outline with a 5.2-unit stroke in glyph space, which is 0.73 units in the symbol, inside a viewBox padded by 3 units on each side. At 16 px tall that adds {g['amp16']['added_weight_per_side_px_at_16px_tall']} px per side, and the padding draws the glyph at {g['amp16']['glyph_scale_vs_amp_at_same_height']} of the master's size. Total ink at the same box height: {', '.join(f"{k} {v}" for k, v in meas['amp_ink'].items())} (sum of pixel coverage). V5 says the 16 px drawing has a heavier contour so the counter stays open. A heavier contour closes counters; this one changes almost nothing. In the 16 px containers V5 sets it at 70 percent of the circle against 58 percent at other sizes, so the extra presence comes from scale.</p>

<h2 id="lock">7. Lockmark pixel fit</h2>
<p>Links are 1 px with <code>vector-effect: non-scaling-stroke</code>; nodes are 7.6 units across and the lever 9.5. The node and link stop reading as different things below about 32 px.</p>
{table(lrows, ['center px', 'peak coverage', 'rows touched'])}
<p class="note">At 16, 24 and 48 px the middle link lands on a whole pixel, so it splits across two rows at half strength, while the outer links land near a pixel centre and draw close to solid. The grid draws with uneven line weight at every common size. Node diameter: {', '.join(f"{k} px: {v['node_diameter_px']}" for k, v in g['lockmark']['by_size'].items())}. Lever: {', '.join(f"{k} px: {v['lever_diameter_px']}" for k, v in g['lockmark']['by_size'].items())}.</p>
<div class="panel">{lock_panel()}</div>

<h2 id="min">8. Minimum sizes and clear space as V5 states them</h2>
<table><thead><tr><th>V5 rule</th><th>What it means in pixels</th><th>Conflict</th></tr></thead><tbody>
<tr><td>L1 minimum 120 px or 1.25 in</td><td class="n">13.35 px tall, cap height 12.36 px, ampersand hairline 1.14 px</td><td>"Below 80 px the monogram replaces the wordmark" leaves 80 to 120 px undefined.</td></tr>
<tr><td>L2 minimum 72 px or 0.75 in</td><td class="n">24.95 px tall, cap height 11.45 px</td><td>Smaller cap height than L1 at its minimum.</td></tr>
<tr><td>L8 minimum 48 px or 0.5 in</td><td class="n">17 px tall, cap height 15.8 px</td><td>L8 is also named for favicons, which are 16 to 32 px.</td></tr>
<tr><td>Ampersand minimum 16 px freestanding, 24 px master</td><td class="n">The 16 px container draws it about 12 px tall</td><td>The container sits below the stated minimum.</td></tr>
<tr><td>Clear space 1.0x on every side; "nothing enters it: no type"</td><td class="n">One cap height</td><td>Inside the lockups the tagline sits 0.39x below the baseline in L5 and 0.79x in L6. V5 never says that lockup parts are exempt. The one-color lockmark (<code>#lockmark-mono</code>) keeps Stone links, so it is two colors.</td></tr>
<tr><td>Hinge diagram labels</td><td class="n">At 516 px wide the labels reach a 13 px font size</td><td>No minimum is stated.</td></tr>
<tr><td>Prussian: red stays at display size or goes mono</td><td class="n">3.19:1</td><td>The color matrix shows red ampersands on Prussian at small sizes (03-identity-03.jpg).</td></tr>
</tbody></table>

<h2 id="matrix">9. Full matrix</h2>
<p>Color: Charcoal letters with a red ampersand on light surfaces, Newsprint letters on Charcoal and White letters on Prussian, as V5 shows them. The lockmark keeps Stone links in color, with White links on Prussian as L6 sets them. The hinge arc is Stone on light surfaces. One color: every part in the letter color, including links and the lever.</p>
{''.join(matrix_block(n, l, d) for n, l, d in ELEMENTS)}
</main></body></html>"""
    OUT_HTML.write_text(html)
    return OUT_HTML


if __name__ == "__main__":
    jobs = build_jobs()
    if "--skip-render" not in sys.argv:
        render(jobs)
    meas = analyse()
    (SCRATCH / "identity_raster.json").write_text(json.dumps(meas, indent=1))
    p = build_board(meas)
    print(json.dumps(meas, indent=1))
    print("board", p, p.stat().st_size)
