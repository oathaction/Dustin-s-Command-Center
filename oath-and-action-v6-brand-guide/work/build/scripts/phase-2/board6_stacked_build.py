"""Board 6, section 3: more stacked lockups (identity designer, November 7, 2026).

Builds six stacked variations of the name from the approved masters at today's width with ampersand
B as refined (DR-106, D2-321), writes each as its own SVG beside the board, measures them, renders
their minimum-size drawings in Chromium, and writes one self-contained board page.

  python3 -I work/build/scripts/phase-2/board6_stacked_build.py

Writes to work/boards/phase-2/board-6/stacked/ only:
  20261107_Board-6-Stacked-Lockups.html        the board
  20261107_Stacked-S<n>-<Name>[-24px|-16px].svg each variation: display, 24 px and 16 px drawings
  20261107_Board-6-Stacked-Measurements.json   every number the board prints
Working renders go to the session scratchpad.
"""
import base64
import html
import json
import math
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import board6_stacked_geom as g  # noqa: E402

ROOT = g.ROOT
HERE = Path(__file__).resolve().parent
OUT = ROOT / "work/boards/phase-2/board-6/stacked"
SCRATCH = Path("/tmp/claude-0/-home-user-Dustin-s-Command-Center/d4b0fb53-ac2c-5992-bcfd-deda558d4457/scratchpad/b6")
DATE = "20261107"
PAGE = OUT / f"{DATE}_Board-6-Stacked-Lockups.html"
JSON_OUT = OUT / f"{DATE}_Board-6-Stacked-Measurements.json"

NEWS, CHAR, RED, PRUS, WHITE, STONE = "#DCD9D2", "#121212", "#E63946", "#1F2D5A", "#FFFFFF", "#5D636D"
DEEP_STONE, DIM_NEWS, PANEL = "#4E535B", "#A3A19C", "#CECDC7"
SURF = {
    "newsprint": {"label": "Newsprint", "bg": NEWS, "ink": CHAR, "amp": RED},
    "charcoal": {"label": "Charcoal", "bg": CHAR, "ink": NEWS, "amp": RED},
    "prussian": {"label": "Prussian, one color White", "bg": PRUS, "ink": WHITE, "amp": WHITE},
}
RECOMMEND = "S1"
CAP_COMPARE = 72 / 2.1796          # L2 stands 72 px tall: its viewBox is 217.96 units for capitals of 100
CAP_LARGE = 80.0
CAP_PLATE = 40.0
POSTER_SCALE = 48.0                 # screen px per inch: an 11 by 17 inch sign drawn at half size
POSTER_CAP_IN = 0.5

ABOUT = {
    "S1": {"construction": "OATH & sits over ACTION, flush left, and B ends the first line exactly where the wordmark puts it.",
           "good": "It suits square posts, posters, covers and avatars, since it packs the name into the smallest box of the six.",
           "watch": "The first line stops short of the second by 0.46x, so the right edge steps in at B."},
    "S2": {"construction": "OATH sits over & ACTION, flush left, and B starts the second line at the wordmark’s own spacing to the A.",
           "good": "It suits pages that read down one left edge, where the name starts the column.",
           "watch": "The second line runs 1.69 times as long as the first, so the block leans right and comes within 0.3x of L2’s width."},
    "S3": {"construction": "OATH sits over ACTION on one left edge. B leads the second line and hangs outside that edge, the way a printer hangs a quotation mark.",
           "good": "It suits layouts where the name lines up with a text column, since the O and the A sit on the column’s edge.",
           "watch": "Clear space starts at B, which sits outside the column, and on a narrow page B can look like a bullet."},
    "S4": {"construction": "OATH, B and ACTION stand on three centered lines, with B at the size of the capitals.",
           "good": "It suits centered posters, event backdrops and square tiles, where the name sits on a center line.",
           "watch": "Three lines make it half again as tall as S1. Set in a corner, its centered lines leave a stepped left edge."},
    "S5": {"construction": "OATH, B and ACTION stand on three lines that share one left edge, with B at the size of the capitals.",
           "good": "It suits poster corners and left-set covers, where every line starts on the margin.",
           "watch": "B alone on the middle line leaves the largest open space of the six, to its right."},
    "S6": {"construction": "S6 is S4 with B at 1.25 times the capitals, the size B takes in the hinge diagram.",
           "good": "It suits posters and signs, where B has to carry the brand across a room.",
           "watch": "It brings back a larger B, so your reaction to it tells us whether L2’s size or its offset was the trouble. At its minimum B is its 16 px master drawn 18 px tall, off the pixel grid, so its crisp share there is 0.68 against 0.69 for the others."},
}
READS = {"L2": "OATH, ACTION, then &", "S1": "OATH &, then ACTION", "S2": "OATH, then & ACTION", "S3": "OATH, then & ACTION",
         "S4": "OATH, &, ACTION", "S5": "OATH, &, ACTION", "S6": "OATH, &, ACTION"}


def slug(v):
    return re.sub(r"[^A-Za-z0-9]+", "-", v["name"].title()).strip("-")


def fname(v, size):
    suf = "" if size == "display" else f"-{size}px"
    return f"{DATE}_Stacked-{v['id']}-{slug(v)}{suf}.svg"


def esc(s):
    return html.escape(s, quote=True)


def num(v, nd=2):
    return g.fmt(v, nd)


# ------------------------------------------------------------------ builds and files

def l2_parts():
    s = g.MASTERS["l2"].read_text()
    s = re.sub(r"<title>.*?</title>", "", s)
    inner = s[s.find(">") + 1: s.rfind("</svg>")]
    vb, paths = g.read_master("l2")
    ink = [sp for f, ss in paths if f == "currentColor" for sp in ss]
    amp = [sp for f, ss in paths if f.startswith("var(--amp") for sp in ss]
    box = g.bbox(ink + amp)
    return inner, vb, box


def build_all():
    res = {}
    for v in g.VARIANTS:
        res[v["id"]] = {size: g.build(v, size) for size in ("display", 24, 16)}
    return res


def write_svgs(res):
    files = []
    for v in g.VARIANTS:
        for size in ("display", 24, 16):
            r = res[v["id"]][size]
            vb = " ".join(num(t, 3) for t in r["viewBox"])
            what = "display drawing" if size == "display" else f"{size} px drawing on the pixel grid"
            title = (f"Stacked lockup {v['id']}, {v['name'].lower()}, {what}. Today's width, ampersand B. "
                     f"Board 6 exploration, November 7, 2026; not an approved master")
            body = g.svg_body(r)
            p = OUT / fname(v, size)
            p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><title>{esc(title)}</title>{body}</svg>\n')
            files.append(p)
    return files


def lockup_svg(inner, vb, cap, surf, label, extra_style=""):
    s = cap / 100.0
    S = SURF[surf]
    w, h = vb[2] * s, vb[3] * s
    vbs = " ".join(num(t, 3) for t in vb)
    return (f'<svg class="lk" xmlns="http://www.w3.org/2000/svg" viewBox="{vbs}" width="{w:.2f}" height="{h:.2f}" '
            f'role="img" aria-label="{esc(label)}" data-red="signature" data-red-job="signature ampersand" '
            f'style="color:{S["ink"]};--amp:{S["amp"]};{extra_style}">{inner}</svg>')


def var_svg(res, vid, size, cap, surf="newsprint", extra_style=""):
    r = res[vid][size]
    v = [x for x in g.VARIANTS if x["id"] == vid][0]
    if size == "display":
        scale_cap = cap
    else:
        scale_cap = cap * 100.0 / r["cap"]
    return lockup_svg(g.svg_body(r), r["viewBox"], scale_cap, surf, f"Oath & Action, stacked lockup {vid}, {v['name'].lower()}", extra_style)


def l2_svg(cap, surf="newsprint"):
    inner, vb, _ = l2_parts()
    return lockup_svg(inner, vb, cap, surf, "Oath & Action, today’s L2 stacked lockup")


# ------------------------------------------------------------------ measures

def ink_box_units(r):
    return r["ink_box"]


def measures(res):
    out = {"method": {
        "x": "one cap height of the wordmark: 100 units in the display drawings, 22 px in the 24 px drawings, 14 px in the 16 px drawings",
        "white": "area between two shapes: slices 0.25 units apart (0.05 px at pixel sizes), each counted to 0.15x past the nearest point, averaged over the band the two shapes share; between lines the slices are columns and a column where one line has no ink counts as open to the 0.15x limit",
        "hinge_targets": {str(k): round(g.masters(k)["hinge"]["target"] / g.SIZES[k]["cap"], 4) for k in ("display", 24, 16)},
        "hinge_master": {str(k): {"H_to_B": round(g.masters(k)["hinge"]["left"]["white"] / g.SIZES[k]["cap"], 4),
                                  "B_to_A": round(g.masters(k)["hinge"]["right"]["white"] / g.SIZES[k]["cap"], 4)} for k in ("display", 24, 16)},
        "avatar": "largest capitals that keep the ink box plus 1.0x of clear space on every side inside the 400 px tile's inscribed circle",
        "print_minimum": "capitals 3 mm, width rounded up to the next 0.05 in",
    }, "L2": {}, "variants": {}}
    _, vb2, box2 = l2_parts()
    m2 = g.l2_measures()
    Wc, Hc = (box2[2] - box2[0]) / 100, (box2[3] - box2[1]) / 100
    diag = math.hypot(Wc + 2, Hc + 2)
    out["L2"] = {"width_x": round(vb2[2] / 100, 2), "ink_height_x": round(Hc, 2), "line_white_x": round(m2["line_white"] / 100, 3),
                 "line_nearest_x": round(m2["line_nearest"] / 100, 3), "b_scale": round(m2["b_scale"], 3),
                 "b_to_n_nearest_x": round(m2["b_to_n_nearest"] / 100, 3), "min_screen_px": 90, "min_print_in": 0.80,
                 "avatar_cap_px": round(400 / diag, 1), "avatar_min_tile_px": math.ceil(14 * diag)}
    for v in g.VARIANTS:
        rd, r24, r16 = (res[v["id"]][k] for k in ("display", 24, 16))
        ib = rd["ink_box"]
        Wc, Hc = (ib[2] - ib[0]) / 100, (ib[3] - ib[1]) / 100
        diag = math.hypot(Wc + 2, Hc + 2)
        bands = rd["cap_bands"]
        flat = [round((bands[k + 1][0] - bands[k][1]) / 100, 3) for k in range(len(bands) - 1)]
        pin = math.ceil((rd["width"] / 100 * 3 / 25.4) / 0.05 - 1e-9) * 0.05
        out["variants"][v["id"]] = {
            "name": v["name"], "lines": v["lines"], "align": v["align"], "b_scale": v.get("b_scale", 1.0),
            "files": {str(k): str((OUT / fname(v, k)).relative_to(ROOT)) for k in ("display", 24, 16)},
            "width_x": round(rd["width"] / 100, 3), "ink_height_x": round(Hc, 3), "ratio": round(Wc / Hc, 2),
            "joins_display": [{"between": j["between"], "kind": j["kind"], "white_x": round(j["white"] / 100, 3), "nearest_x": round(j["nearest"] / 100, 3)} for j in rd["joins"]],
            "joins_24px": [{"between": j["between"], "kind": j["kind"], "white_px": round(j["white"], 2), "white_x": round(j["white"] / 22, 3), "nearest_px": round(j["nearest"], 2)} for j in r24["joins"]],
            "joins_16px": [{"between": j["between"], "kind": j["kind"], "white_px": round(j["white"], 2), "white_x": round(j["white"] / 14, 3), "nearest_px": round(j["nearest"], 2)} for j in r16["joins"]],
            "baseline_to_cap_line_x": flat,
            "size_24px": [r24["width"], r24["height"]], "size_16px": [r16["width"], r16["height"]],
            "min_screen_px": r16["width"], "min_screen_height_px": r16["height"], "min_print_in": round(pin, 2),
            "avatar_cap_px": round(400 / diag, 1), "avatar_min_tile_px": math.ceil(14 * diag),
        }
    return out


def render_minimums(res):
    """Render the 16 and 24 px drawings at true size in Chromium, in color for the board and in one color for
    the crisp share (ink pixels at 90 percent coverage or more over ink pixels at 10 percent or more, D1-17)."""
    SCRATCH.mkdir(parents=True, exist_ok=True)
    jobs = []
    for v in g.VARIANTS:
        for size in (16, 24):
            r = res[v["id"]][size]
            vb = " ".join(num(t, 3) for t in r["viewBox"])
            w, h = int(r["viewBox"][2]), int(r["viewBox"][3])
            body = g.svg_body(r)
            for tone, ink, amp in (("color", CHAR, RED), ("mono", CHAR, CHAR)):
                svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}" style="display:block;color:{ink};--amp:{amp}">{body}</svg>'
                jobs.append({"id": f"{v['id']}-{size}-{tone}", "svg": svg, "w": w, "h": h, "bg": NEWS})
    inner, vb2, _ = l2_parts()
    w2 = 90
    h2 = round(vb2[3] * w2 / vb2[2], 2)
    svg2 = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(num(t, 3) for t in vb2)}" width="{w2}" height="{h2}" style="display:block;color:{CHAR};--amp:{CHAR}">{inner}</svg>'
    jobs.append({"id": "L2-min-mono", "svg": svg2, "w": w2, "h": math.ceil(h2), "bg": NEWS})
    jp = SCRATCH / "render_jobs.json"
    jp.write_text(json.dumps(jobs))
    rd = SCRATCH / "renders"
    subprocess.run(["node", str(HERE / "board6_stacked_render.js"), str(jp), str(rd)], check=True)
    import numpy as np
    from PIL import Image
    # Chromium blends coverage in encoded sRGB values, so coverage is read per channel from those values
    bg = np.array([int(NEWS[i:i + 2], 16) for i in (1, 3, 5)], float)
    ink = np.array([int(CHAR[i:i + 2], 16) for i in (1, 3, 5)], float)
    crisp, pngs = {}, {}
    for j in jobs:
        im = Image.open(rd / f"{j['id']}.png").convert("RGB")
        if j["id"].endswith("mono"):
            a = np.asarray(im, float)
            cov = ((bg - a) / (bg - ink)).mean(axis=2)
            lo = int((cov >= 0.10).sum())
            hi = int((cov >= 0.90).sum())
            crisp[j["id"].replace("-mono", "")] = round(hi / lo, 3)
        else:
            big = im.resize((im.width * 4, im.height * 4), Image.NEAREST)
            p = rd / f"{j['id']}-4x.png"
            big.save(p, optimize=True)
            pngs[j["id"].replace("-color", "")] = ("data:image/png;base64," + base64.b64encode(p.read_bytes()).decode(), big.width, big.height)
    return crisp, pngs


def lum(hexc):
    return lum_rgb(tuple(int(hexc[i:i + 2], 16) for i in (1, 3, 5)))


def lum_rgb(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(rgb[0]) + 0.7152 * ch(rgb[1]) + 0.0722 * ch(rgb[2])


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# ------------------------------------------------------------------ page parts

def vname(vid):
    return [v for v in g.VARIANTS if v["id"] == vid][0]["name"]


def region(label, inner, cls=""):
    return f'<div class="scroller {cls}" role="region" tabindex="0" aria-label="{esc(label)}">{inner}</div>'


def compare_grid(res, M):
    cells = []
    items = [("L2", "", l2_svg(CAP_COMPARE))] + [(v["id"], v["name"], var_svg(res, v["id"], "display", CAP_COMPARE)) for v in g.VARIANTS]
    for vid, name, svg in items:
        w = M["L2"]["width_x"] if vid == "L2" else M["variants"][vid]["width_x"]
        flag = '<span class="pill">Recommended</span> ' if vid == RECOMMEND else ('<span class="pill quiet">In the guide today</span> ' if vid == "L2" else "")
        cells.append(f'<figure class="cmp{" cmp-today" if vid == "L2" else ""}{" cmp-rec" if vid == RECOMMEND else ""}">'
                     f'<figcaption><span class="id">{vid}</span>{" " + esc(name) if name else ""}</figcaption>'
                     f'<div class="cmp-art">{svg}</div>'
                     f'<p class="small">{flag}Reads {esc(READS[vid])}. {num(w * CAP_COMPARE, 0)} px wide.</p></figure>')
    return f'<div class="cmp-grid">{"".join(cells)}</div>'


def surfaces_row(res, vid):
    out = []
    for key, S in SURF.items():
        out.append(f'<figure class="surf surf-{key[:4]}" style="background:{S["bg"]}"><figcaption style="color:{S["ink"] if key != "newsprint" else DEEP_STONE}">{esc(S["label"])}</figcaption>'
                   f'{var_svg(res, vid, "display", CAP_PLATE, key)}</figure>')
    return f'<div class="surf-row">{"".join(out)}</div>'


def avatar(res, vid, M, tile):
    m = M["variants"][vid]
    rd = res[vid]["display"]
    ib = rd["ink_box"]
    if tile < 200:
        # the smallest tile holds 14 px capitals: the 16 px drawing at its own pixels, on whole-pixel offsets
        r = res[vid][16]
        vb, ib = r["viewBox"], r["ink_box"]
        left = round(tile / 2 - ((ib[0] + ib[2]) / 2 - vb[0]))
        top = round(tile / 2 - ((ib[1] + ib[3]) / 2 - vb[1]))
        svg = var_svg(res, vid, 16, 14.0, "charcoal", f"position:absolute;left:{left}px;top:{top}px")
    else:
        cap = m["avatar_cap_px"] * tile / 400.0
        s = cap / 100
        vb = rd["viewBox"]
        # center the ink box in the tile
        left = tile / 2 - ((ib[0] + ib[2]) / 2 - vb[0]) * s
        top = tile / 2 - ((ib[1] + ib[3]) / 2 - vb[1]) * s
        svg = var_svg(res, vid, "display", cap, "charcoal", f"position:absolute;left:{left:.2f}px;top:{top:.2f}px")
    return (f'<div class="tile" style="width:{tile}px;height:{tile}px">{svg}'
            f'<span class="tile-circle" aria-hidden="true"></span></div>')


def poster(res, vid):
    v = [x for x in g.VARIANTS if x["id"] == vid][0]
    rd = res[vid]["display"]
    cap = POSTER_CAP_IN * POSTER_SCALE
    s = cap / 100
    ib, vb = rd["ink_box"], rd["viewBox"]
    margin = 0.75 * POSTER_SCALE
    sheet_w, crop_w, crop_h = 11 * POSTER_SCALE, 480, 420
    # the sheet's lower left corner sits 28 px in from the crop's left and bottom
    trim_x, trim_b = 28, 28
    # the lockup's text edge sits on the margin; in S3 the O and the A sit on it and B hangs left of it
    if v["align"] == "hung":
        a2 = [sh for sh in rd["shapes"] if sh.name == "A2"][0]
        edge = a2.box[0]
    else:
        edge = ib[0]
    lk_left = margin - (edge - vb[0]) * s
    lk_bottom = margin - (vb[1] + vb[3] - ib[3]) * s
    svg = var_svg(res, vid, "display", cap, "newsprint", f"position:absolute;left:{lk_left:.2f}px;bottom:{lk_bottom:.2f}px")
    return (f'<div class="poster-crop" style="width:{crop_w}px;height:{crop_h}px">'
            f'<div class="sheet" style="left:{trim_x}px;bottom:{trim_b}px;width:{sheet_w:.0f}px;height:{crop_h + 40}px">'
            f'<div class="sheet-text" style="left:{margin:.0f}px;bottom:{margin + (ib[3] - ib[1]) * s + cap + 4:.0f}px;width:{crop_w - trim_x - margin - 16:.0f}px">'
            f'<p class="sheet-kicker">Public hearing</p>'
            f'<p class="sheet-head">Tell the library board what hours you need.</p>'
            f'<p class="sheet-body">Tuesday, March 9, 7 p.m., Wrenfield Town Hall</p></div>'
            f'{svg}</div></div>')


def clearspace(res, vid, cap=CAP_PLATE):
    rd = res[vid]["display"]
    ib, vb = rd["ink_box"], rd["viewBox"]
    s = cap / 100
    c = cap
    pad_l, pad_t, pad_r, pad_b = 34, 30, 16, 16
    iw, ih = (ib[2] - ib[0]) * s, (ib[3] - ib[1]) * s
    W = pad_l + c + iw + c + pad_r
    H = pad_t + c + ih + c + pad_b
    ox, oy = pad_l + c, pad_t + c                # ink box origin
    lx = ox - (ib[0] - vb[0]) * s
    ly = oy - (ib[1] - vb[1]) * s
    body = g.svg_body(rd)
    vbs = " ".join(num(t, 3) for t in vb)
    # line one's cap band, for the x bracket
    band = rd["cap_bands"][0]
    cy0, cy1 = oy + (band[0] - ib[1]) * s, oy + (band[1] - ib[1]) * s
    lab = f"Oath & Action, stacked lockup {vid}, with one cap height of clear space drawn around it"
    return (f'<svg class="cs" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W:.2f}" height="{H:.2f}" role="img" aria-label="{esc(lab)}" data-red="signature" data-red-job="signature ampersand">'
            f'<rect x="{pad_l:.2f}" y="{pad_t:.2f}" width="{iw + 2 * c:.2f}" height="{ih + 2 * c:.2f}" fill="{PANEL}" stroke="{STONE}" stroke-width="1" stroke-dasharray="4 3"/>'
            f'<rect x="{ox:.2f}" y="{oy:.2f}" width="{iw:.2f}" height="{ih:.2f}" fill="{NEWS}" stroke="{STONE}" stroke-width="1"/>'
            f'<svg x="{lx:.2f}" y="{ly:.2f}" width="{vb[2] * s:.2f}" height="{vb[3] * s:.2f}" viewBox="{vbs}" style="color:{CHAR};--amp:{RED}" overflow="visible">{body}</svg>'
            f'<g stroke="{CHAR}" stroke-width="1" fill="none"><path d="M{pad_l + 4:.2f} {cy0:.2f}H{pad_l + 12:.2f}M{pad_l + 8:.2f} {cy0:.2f}V{cy1:.2f}M{pad_l + 4:.2f} {cy1:.2f}H{pad_l + 12:.2f}"/>'
            f'<path d="M{ox + iw / 2:.2f} {pad_t:.2f}V{oy:.2f}M{ox + iw / 2 - 4:.2f} {pad_t:.2f}H{ox + iw / 2 + 4:.2f}M{ox + iw / 2 - 4:.2f} {oy:.2f}H{ox + iw / 2 + 4:.2f}"/></g>'
            f'<text x="{pad_l - 6:.2f}" y="{(cy0 + cy1) / 2 + 5:.2f}" text-anchor="end" font-family="Inter, Arial, sans-serif" font-size="14" font-style="italic" fill="{CHAR}">x</text>'
            f'<text x="{ox + iw / 2 + 8:.2f}" y="{pad_t - 10:.2f}" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="600" fill="{CHAR}">1.0x clear space</text>'
            f'</svg>')


def minimum(res, vid, M, pngs, crisp):
    r16 = res[vid][16]
    m = M["variants"][vid]
    src, bw, bh = pngs[f"{vid}-16"]
    one = var_svg(res, vid, 16, 14.0)
    r24 = res[vid][24]
    two = var_svg(res, vid, 24, 22.0)
    return (f'<div class="min-row"><figure class="min-cell"><figcaption>16 px drawing, 14 px capitals</figcaption><div class="min-art">{one}</div>'
            f'<p class="small">{r16["width"]:.0f} by {r16["height"]:.0f} px</p></figure>'
            f'<figure class="min-cell"><figcaption>24 px drawing, 22 px capitals</figcaption><div class="min-art">{two}</div>'
            f'<p class="small">{r24["width"]:.0f} by {r24["height"]:.0f} px</p></figure>'
            f'<figure class="min-cell min-big"><figcaption>The pixels Chromium draws, four times</figcaption>'
            + region(f"{vid} minimum, enlarged four times", f'<img src="{src}" width="{bw}" height="{bh}" alt="The {vid} lockup at its 14 px minimum, enlarged four times so each pixel shows" class="px">', "fit")
            + '</figure></div>')


def table_row_cells(vid, M, crisp):
    if vid == "L2":
        m = M["L2"]
        lines = f'{m["line_white_x"]:.3f}x'
        near = f'{m["line_nearest_x"]:.3f}x'
        return [f'<th scope="row">L2, today</th>', f"<td>{READS['L2']}</td>", f'<td class="n">{m["width_x"]:.2f} by {m["ink_height_x"]:.2f}</td>',
                f'<td class="n">{lines}</td>', f'<td class="n">{near}</td>', f'<td class="n">90 px wide</td>', f'<td class="n">0.80 in</td>',
                f'<td class="n">{m["avatar_cap_px"]:.0f} px</td>', f'<td class="n">{m["avatar_min_tile_px"]} px</td>', f'<td class="n">{crisp["L2-min"]:.2f}</td>']
    m = M["variants"][vid]
    lw = [j for j in m["joins_display"] if j["kind"] == "lines"]
    sw = [j for j in m["joins_display"] if j["kind"] == "side"]
    whites = ", ".join(f'{j["white_x"]:.3f}x' for j in lw)
    nears = ", ".join(f'{j["nearest_x"]:.3f}x' for j in lw)
    rec = " (recommended)" if vid == RECOMMEND else ""
    return [f'<th scope="row">{vid}, {esc(m["name"].lower())}{rec}</th>', f"<td>{READS[vid]}</td>", f'<td class="n">{m["width_x"]:.2f} by {m["ink_height_x"]:.2f}</td>',
            f'<td class="n">{whites}</td>', f'<td class="n">{nears}</td>', f'<td class="n">{m["min_screen_px"]:.0f} px wide</td>', f'<td class="n">{m["min_print_in"]:.2f} in</td>',
            f'<td class="n">{m["avatar_cap_px"]:.0f} px</td>', f'<td class="n">{m["avatar_min_tile_px"]} px</td>', f'<td class="n">{crisp[vid + "-16"]:.2f}</td>']


def table(M, crisp):
    heads = ["Lockup", "Reads", "Size in x, wide by tall", "White between lines", "Nearest ink between lines", "Minimum on screen", "Minimum in print",
             "Capitals in a 400 px round avatar", "Smallest tile for 14 px capitals", "Crisp share at the minimum"]
    keys = ["L2"] + [v["id"] for v in g.VARIANTS]
    rows = []
    for k in keys:
        cells = table_row_cells(k, M, crisp)
        cells = [cells[0]] + [c.replace("<td", f'<td data-k="{esc(h)}"', 1) for c, h in zip(cells[1:], heads[1:])]
        rows.append(f'<tr{" class=rec" if k == RECOMMEND else ""}>{"".join(cells)}</tr>')
    th = "".join(f'<th scope="col">{esc(h)}</th>' for h in heads)
    return f'<table class="stack"><caption>Every lockup measured the same way. x is one cap height.</caption><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


def variant_section(res, v, M, crisp, pngs):
    vid = v["id"]
    m = M["variants"][vid]
    A = ABOUT[vid]
    lw = [j for j in m["joins_display"] if j["kind"] == "lines"]
    sw = [j for j in m["joins_display"] if j["kind"] == "side"]
    rec = '<p class="rec-flag">Recommended</p>' if vid == RECOMMEND else ""
    spacing = []
    for j in sw:
        spacing.append(f"Beside B ({j['between'].replace(' / ', ' to ')}): {j['white_x']:.3f}x of white, the wordmark’s own.")
    for j in lw:
        a, b = j["between"].split(" / ")
        a = a.replace("&", " &").replace("OATH &", "OATH &").strip()
        b = b.replace("&ACTION", "& ACTION")
        spacing.append(f"{esc(a)} to {esc(b)}: {j['white_x']:.3f}x of white, nearest ink {j['nearest_x']:.3f}x.")
    flat = ", ".join(f"{f:.3f}x" for f in m["baseline_to_cap_line_x"])
    flat_label = "Open space from each line’s baseline to the cap line below" if len(v["lines"]) == 2 else "Open space down the stack, from baseline to B’s ink and from B’s ink to the cap line"
    pair = region(f"{vid} beside L2 at 80 px capitals",
                  f'<div class="pair"><figure><figcaption>Today’s L2</figcaption>{l2_svg(CAP_LARGE)}</figure>'
                  f'<figure><figcaption>{vid}</figcaption>{var_svg(res, vid, "display", CAP_LARGE)}</figure></div>')
    tiles = (region(f"{vid} in a 400 px avatar tile", f'<figure><figcaption>400 px tile, capitals {m["avatar_cap_px"]:.0f} px</figcaption>{avatar(res, vid, M, 400)}</figure>', "fit")
             + f'<figure class="tile-min"><figcaption>{m["avatar_min_tile_px"]} px tile, capitals 14 px</figcaption>{avatar(res, vid, M, m["avatar_min_tile_px"])}</figure>')
    post = region(f"{vid} on a poster corner", poster(res, vid), "fit")
    return f'''
<section class="var" id="{vid.lower()}" aria-labelledby="{vid.lower()}-h">
  <div class="var-head">
    {rec}<h2 id="{vid.lower()}-h"><span class="id">{vid}</span> {esc(v["name"])}</h2>
    <p class="lede">{esc(A["construction"])}</p>
    <dl class="gw"><div><dt>Good for</dt><dd>{esc(A["good"])}</dd></div><div><dt>Watch</dt><dd>{esc(A["watch"])}</dd></div></dl>
  </div>
  <h3>Beside L2 at 80 px capitals</h3>
  {pair}
  <h3>On the three surfaces, 40 px capitals</h3>
  {surfaces_row(res, vid)}
  <div class="inuse">
    <div class="inuse-tiles"><h3>In a square avatar tile</h3>
      <p class="small">Charcoal, the default tile. The ring marks the circle most platforms crop to; the lockup and one cap height of clear space sit inside it. The small tile is the 16 px drawing at true pixels.</p>
      <div class="tiles">{tiles}</div></div>
    <div class="inuse-poster"><h3>On a poster corner</h3>
      <p class="small"><span class="illus">Illustrative</span> The lower left corner of an 11 by 17 inch sign, drawn at half size. The margin is 0.75 in and the lockup’s capitals are 0.5 in tall in print.</p>
      {post}</div>
  </div>
  <div class="two">
    <div><h3>Clear space</h3>{region(f"{vid} clear space", clearspace(res, vid), "fit")}
      <p class="small">One cap height on every side of the ink, at 40 px capitals. The lockup measures {m["width_x"]:.2f}x by {m["ink_height_x"]:.2f}x.</p></div>
    <div><h3>Minimum size</h3>{minimum(res, vid, M, pngs, crisp)}
      <p class="small">On screen: capitals 14 px, {m["min_screen_px"]:.0f} px wide, drawn from the 16 px wordmark master on whole pixels; crisp share {crisp[vid + "-16"]:.2f} (the guide passes 0.60). In print: capitals 3 mm, {m["min_print_in"]:.2f} in wide. Below these sizes, use L8.</p></div>
  </div>
  <h3>Spacing, measured</h3>
  <ul class="facts">{"".join(f"<li>{s}</li>" for s in spacing)}<li>{flat_label}: {flat}.</li></ul>
  <p class="files">File: <code>{esc(m["files"]["display"].split("/")[-1])}</code>, with <code>-24px</code> and <code>-16px</code> drawings beside it.</p>
</section>'''


CSS = """
:root{--news:#DCD9D2;--char:#121212;--stone:#5D636D;--deep:#4E535B;--panel:#CECDC7;--white:#FFFFFF;--prus:#1F2D5A}
*{box-sizing:border-box}
html{background:var(--news)}
body{margin:0;background:var(--news);color:var(--char);font:400 16px/1.55 "Inter",Arial,sans-serif;-webkit-font-smoothing:antialiased}
main{max-width:1200px;margin:0 auto;padding:40px 32px 96px}
h1,h2,h3{font-family:"Inter Tight",Arial,sans-serif;font-weight:800;margin:0}
h1{font-size:56px;line-height:1;letter-spacing:-0.03em;margin:8px 0 16px}
h2{font-size:36px;line-height:1.05;letter-spacing:-0.025em}
h3{font-size:20px;line-height:1.2;letter-spacing:-0.005em;margin:36px 0 12px}
p{margin:0 0 12px;max-width:68ch}
.kicker,.label,figcaption,.rec-flag,dt,thead th,caption{font:600 13px/1.4 "Inter",Arial,sans-serif;letter-spacing:0.06em;text-transform:uppercase}
.kicker{color:var(--deep)}
.deck{font-size:20px;line-height:1.45;max-width:62ch}
.quote{font-family:"Lora",Georgia,serif;font-style:italic;font-size:20px;line-height:1.45;margin:20px 0 4px;max-width:60ch}
.small{font-size:14px;line-height:1.5;color:var(--deep)}
.id{font-variant-numeric:tabular-nums}
.pill{display:inline-block;border:1px solid var(--char);padding:0 6px;margin-right:4px;color:var(--char);font-size:13px;letter-spacing:0.04em;text-transform:uppercase;line-height:20px}
.pill.quiet{border-color:var(--deep);color:var(--deep)}
hr{border:0;border-top:1px solid var(--char);margin:48px 0 0}
.lead{margin-top:20px}
.head-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:0 48px}
@media (min-width:64em){.head-grid{grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);align-items:end}.head-grid .quote{margin-top:0}}
.cmp-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;border-top:2px solid var(--char);margin-top:16px}
.cmp{margin:0;padding:14px 16px 10px 0;border-bottom:1px solid var(--stone)}
.cmp figcaption{color:var(--char);margin-bottom:12px}
.cmp-art{display:flex;align-items:flex-start}
.cmp .small{margin:8px 0 0}
.cmp-rec{box-shadow:inset 0 3px 0 var(--char)}
.recbox{border:2px solid var(--char);padding:24px 28px;margin:40px 0 0;background:var(--white)}
.recbox h2{font-size:32px;margin-bottom:12px}
.recbox ul{margin:12px 0 0;padding-left:20px;max-width:75ch}
.recbox li{margin:0 0 8px}
.recbox .small{color:var(--char)}
.var{border-top:2px solid var(--char);margin-top:72px;padding-top:24px}
.var-head{max-width:820px}
.rec-flag{display:inline-block;background:var(--char);color:var(--news);padding:2px 8px;margin:0 0 12px}
.lede{font-size:18px;margin:12px 0 16px}
.gw{display:grid;grid-template-columns:1fr 1fr;gap:16px 32px;margin:0}
.gw dt{color:var(--deep);margin-bottom:4px}
.gw dd{margin:0;font-size:15px;line-height:1.5}
.scroller{overflow-x:auto;max-width:100%}
.scroller:focus-visible,.scroller:focus{outline:3px solid var(--char);outline-offset:3px}
.pair{display:flex;gap:56px;align-items:flex-start;padding:24px;background:var(--panel);width:max-content;min-width:100%}
.pair figure{margin:0}
.pair figcaption{color:var(--char);margin-bottom:12px}
.surf-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.surf{margin:0;padding:20px 20px 28px;min-height:200px;display:flex;flex-direction:column;gap:20px;border:1px solid transparent}
.surf-news{border-color:var(--stone)}
.surf figcaption{margin:0}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px}
.inuse{display:flex;flex-wrap:wrap;gap:24px 48px;align-items:flex-start}
.inuse-tiles{flex:0 1 560px;min-width:0}
.inuse-poster{flex:0 1 480px;min-width:0}
.inuse .small{max-width:52ch}
.tiles{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}
.scroller.fit{width:max-content;max-width:100%}
.tiles figure{margin:0}
.tiles figcaption{color:var(--char);margin-bottom:8px}
.tile-min figcaption{max-width:136px}
.min-row + .small{margin-top:12px}
.tile{position:relative;background:var(--char);overflow:hidden}
.tile-circle{position:absolute;inset:0;border-radius:50%;border:1px solid #6E6C68;pointer-events:none}
.lk{display:block;max-width:none;overflow:visible}
.poster-crop{position:relative;background:var(--panel);overflow:hidden}
.sheet{position:absolute;background:var(--news);box-shadow:0 0 0 1px var(--stone)}
.sheet-text{position:absolute}
.sheet-kicker{font:600 14px/1.3 "Inter",Arial,sans-serif;letter-spacing:0.06em;text-transform:uppercase;margin:0 0 8px}
.sheet-head{font:800 40px/1.02 "Inter Tight",Arial,sans-serif;letter-spacing:-0.025em;margin:0 0 12px;max-width:none}
.sheet-body{font:500 16px/1.35 "Inter",Arial,sans-serif;margin:0}
.illus{display:inline-block;font:600 13px/1.4 "Inter",Arial,sans-serif;letter-spacing:0.06em;text-transform:uppercase;border:1px solid var(--deep);padding:0 5px;margin-right:6px;color:var(--char)}
.cs{display:block;max-width:none}
.min-row{display:flex;gap:28px;align-items:flex-start;flex-wrap:wrap}
.min-cell{margin:0;min-width:0}
.min-big{max-width:100%}
.min-cell figcaption{color:var(--char);margin-bottom:8px;max-width:22ch}
.min-art{padding:8px 0}
img.px{image-rendering:pixelated;display:block;border:1px solid var(--stone)}
.facts{margin:0;padding-left:20px;max-width:75ch}
.facts li{margin:0 0 4px}
.files{font-size:14px;margin-top:12px}
code{font:500 13px/1.4 ui-monospace,Menlo,Consolas,monospace;background:var(--white);padding:1px 4px;overflow-wrap:anywhere}
table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.45;margin-top:12px}
caption{text-align:left;color:var(--deep);padding:0 0 8px}
th,td{text-align:left;vertical-align:top;padding:8px 10px 8px 0;border-bottom:1px solid var(--stone)}
thead th{color:var(--deep);border-bottom:2px solid var(--char);font-size:13px}
td.n{font-variant-numeric:tabular-nums;white-space:nowrap}
tr.rec th,tr.rec td{background:var(--white)}
.method{max-width:75ch}
.method li{margin-bottom:8px}
.toc{display:flex;flex-wrap:wrap;gap:8px 20px;margin:20px 0 0;padding:0;list-style:none;font-size:15px}
a{color:var(--char);text-underline-offset:3px}
a:focus-visible{outline:3px solid var(--char);outline-offset:2px}
@media (max-width:64em){.cmp-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.two{grid-template-columns:minmax(0,1fr)}}
@media (max-width:48em){
 main{padding:24px 16px 72px}
 h1{font-size:40px}
 h2{font-size:28px}
 .deck{font-size:18px}
 .cmp-grid{grid-template-columns:minmax(0,1fr)}
 .cmp-art{min-height:0}
 .gw{grid-template-columns:minmax(0,1fr)}
 .surf-row{grid-template-columns:minmax(0,1fr)}
 .recbox{padding:20px}
 table.stack,table.stack tbody,table.stack tr,table.stack th,table.stack td,table.stack caption{display:block;width:100%}
 table.stack thead{display:none}
 table.stack tr{border-bottom:1px solid var(--char);padding:10px 0}
 table.stack th,table.stack td{border:0;padding:2px 0;white-space:normal}
 table.stack td[data-k]::before{content:attr(data-k) ": ";font-weight:600}
}
"""


def page(res, M, crisp, pngs):
    m1 = M["variants"][RECOMMEND]
    l2 = M["L2"]
    secs = "".join(variant_section(res, v, M, crisp, pngs) for v in g.VARIANTS)
    toc = "".join(f'<li><a href="#{v["id"].lower()}">{v["id"]} {esc(v["name"])}</a></li>' for v in g.VARIANTS)
    hin = M["method"]["hinge_master"]
    s1_lines = [j for j in m1["joins_display"] if j["kind"] == "lines"][0]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Board 6, section 3: Stacked lockups</title>
<meta name="description" content="Six stacked variations of the Oath &amp; Action lockup beside today’s L2, built from the approved masters, with a recommendation.">
<meta name="generator" content="work/build/scripts/phase-2/board6_stacked_build.py">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&amp;family=Inter:wght@400;500;600;700&amp;family=Lora:ital,wght@1,400;1,500&amp;display=swap">
<style>{CSS}</style>
</head>
<body>
<main data-view-root="overview">
<header class="head-grid">
  <div><p class="kicker">Board 6 · Section 3 of 4 · November 7, 2026</p>
  <h1>More stacked lockups</h1>
  <p class="deck">This board sets six ways to stack the name beside today’s L2. All six keep today’s wordmark width and ampersand B as refined. We set each word from the wordmark master’s own letters and spacing and placed B from its own master, redrawing no letter.</p></div>
  <div><p class="quote">“I don’t know that I like that. Can you give me a few more variations of stacked?”</p>
  <p class="small">Dustin Cathcart, November 7, 2026, on L2: OATH over ACTION with B 1.28 times larger, set off at the right.</p></div>
</header>

<section class="lead" aria-labelledby="cmp-h">
  <h2 id="cmp-h">All six beside today’s L2</h2>
  <p>Every lockup here sets its capitals {CAP_COMPARE:.0f} px tall, so L2 stands 72 px tall. All seven come from the display masters, as L2 does, and the lockups in each row share one top line. Readers take in L2 as OATH, ACTION, then B, because B sits after both words. Each new stack puts B between the words, in the order people say the name.</p>
  {compare_grid(res, M)}
</section>

<section class="recbox" aria-labelledby="rec-h">
  <p class="kicker">Our recommendation</p>
  <h2 id="rec-h">S1, ampersand ends line one</h2>
  <ul>
    <li>It is the wordmark broken after B. OATH, B and the white between H and B are exactly as the wordmark master draws them, so a reader who knows the masthead knows this stack at once.</li>
    <li>It reads in the name’s order and keeps B at the size of the capitals, as the wordmark does.</li>
    <li>It packs the name into the smallest box of the six, {m1["width_x"]:.2f}x by {m1["ink_height_x"]:.2f}x. In a 400 px round avatar its capitals reach {m1["avatar_cap_px"]:.0f} px, against {l2["avatar_cap_px"]:.0f} px for L2, and it holds 14 px capitals in tiles down to {m1["avatar_min_tile_px"]} px.</li>
    <li>Its lines hold {s1_lines["white_x"]:.3f}x of white, the same white as each side of B. L2 holds {l2["line_white_x"]:.3f}x, so the leading, the space between lines, barely moves and the block keeps L2’s density.</li>
    <li>At its minimum it is drawn from the 16 px wordmark master on whole pixels, {m1["min_screen_px"]:.0f} px wide. Its crisp share there, the part of its ink that lands on whole pixels, is {crisp["S1-16"]:.2f}, against {crisp["L2-min"]:.2f} for L2 at its 90 px minimum; the guide passes 0.60.</li>
  </ul>
  <p class="small">If you would rather set the name on a center line, choose S4 in its place. We recommend shipping one stacked lockup, so producers never have to choose between two.</p>
</section>

<nav aria-label="The six variations"><ul class="toc">{toc}<li><a href="#measures">All measures</a></li><li><a href="#method">How we spaced them</a></li></ul></nav>

{secs}

<section class="var" id="measures" aria-labelledby="measures-h">
  <h2 id="measures-h">All measures</h2>
  <p>Sizes and white come from the display drawings. The minimum and its crisp share come from the 16 px drawings, rendered in Chromium at true size. Crisp share counts ink pixels at 90 percent coverage or more over ink pixels at 10 percent or more, in one color on Newsprint.</p>
  {table(M, crisp)}
</section>

<section class="var" id="method" aria-labelledby="method-h">
  <h2 id="method-h">How we spaced them</h2>
  <ul class="method">
    <li>Every join holds the white the wordmark holds beside B. We measure white as an area: slice the space between two shapes into thin strips, count each strip up to 0.15x past the nearest point, and average the strips. The wordmark master holds {hin["display"]["H_to_B"]:.3f}x between H and B and {hin["display"]["B_to_A"]:.3f}x between B and A, the hinge spacing set in October (change C-007).</li>
    <li>Beside B, each stack keeps the master’s own placement, so the white there is the wordmark’s. Between lines the strips run upright, and we moved the lower line until its white matched the hinge. A strip where one line has no ink, such as the gap between two letters, counts as open up to the 0.15x limit.</li>
    <li>Today’s L2 holds {l2["line_white_x"]:.3f}x between its lines by the same measure, close to the hinge already, and its B stands {l2["b_to_n_nearest_x"]:.2f}x clear of the N.</li>
    <li>We center B on its own line by its ink, as the hinge diagram does. Flush-left lines start at their ink, as L2’s do.</li>
    <li>The 24 px and 16 px wordmark masters carry wider spacing for small sizes, an average of {M["method"]["hinge_targets"]["24"]:.3f}x and {M["method"]["hinge_targets"]["16"]:.3f}x on the two sides of B. The small drawings follow their own master and move lines in whole pixels, so their white lands within half a pixel of that target.</li>
    <li>Like the wordmark, each stack has three drawings: the 16 px drawing for capitals 14 to 17 px, the 24 px drawing for capitals 18 to 36 px and the display drawing from 37 px. Set <code>color</code> to the surface’s text token and <code>--amp</code> to its signature token; on Prussian set both to White.</li>
    <li>x means one cap height of the wordmark.</li>
  </ul>
  <p class="small">These are explorations for Board 6. L2 stays in the guide until Dustin picks one by name, since a new lockup changes identity geometry (gate rule 4). Every file sits beside this board in <code>work/boards/phase-2/board-6/stacked/</code>, outside the identity masters folder.</p>
</section>
</main>
</body>
</html>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = build_all()
    files = write_svgs(res)
    M = measures(res)
    crisp, pngs = render_minimums(res)
    M["crisp_share"] = crisp
    M["contrast"] = {"charcoal_on_newsprint": round(contrast(CHAR, NEWS), 2), "deep_stone_on_newsprint": round(contrast(DEEP_STONE, NEWS), 2),
                     "deep_stone_on_panel": round(contrast(DEEP_STONE, PANEL), 2), "red_on_newsprint": round(contrast(RED, NEWS), 2),
                     "red_on_charcoal": round(contrast(RED, CHAR), 2), "white_on_prussian": round(contrast(WHITE, PRUS), 2),
                     "newsprint_on_charcoal": round(contrast(NEWS, CHAR), 2)}
    JSON_OUT.write_text(json.dumps(M, indent=1))
    PAGE.write_text(page(res, M, crisp, pngs))
    print(f"{len(files)} SVG files, {PAGE.relative_to(ROOT)} ({PAGE.stat().st_size // 1024} KB)")
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk in ("width_x", "ink_height_x", "avatar_cap_px", "avatar_min_tile_px", "min_screen_px", "min_print_in")} for k, v in M["variants"].items()}, indent=0))
    print("L2", M["L2"])
    print("crisp", crisp)


if __name__ == "__main__":
    main()
