"""Stage B, round 1: the identity designer's drawings for the drawings board (November 9, 2026).

Under work/handoffs/phase-2/20261109_Stage-B-Drawings-Brief.md, "Identity designer". Three items:

  1. The pixel-fit end mark (DR-142, D2-496). Ampersand B drawn on whole pixels for the end mark at 17 px text (the
     14 px master) and at 15 px text (the 12 px master), two fits each. Fit A keeps the master's overshoot above and
     below, so B's tail sits one pixel under the baseline, as today's end mark does (DR-130). Fit B sits B on the
     baseline as a typeface does with its round letters at text sizes, one row shorter. Both keep B's top on the
     capitals' top row. Each drawing is one outline traced from its pixels, so it never parts into stripes.
  2. The lockmark masters rebuilt (DR-145). The 24 and 48 px masters with each node and the lever as one outline traced
     from the pixels today's files draw, so the drawing at each master's own size is the same, pixel for pixel. The 16
     px master already draws each node and the lever as one shape (a circle), so it needs no new file; the script
     measures it from 16 to 23 px to show it stays whole. Prussian White files go in prussian/ (treatment D).
  3. L6 centered. The wordmark and tagline moved down so that the span from the wordmark's cap line to the tagline's
     baseline is centered on the strip, beside L6 as drawn today without its dots (DR-129). Plate only: no master.

It writes new files only: the masters beside today's in work/build/assets/identity/ (ampersand/, lockmark/, prussian/),
and the plate page, its renders and its figures in work/boards/phase-2/stage-b/drawings/identity/. No existing master,
specimen, chapter, board or ledger file is changed. Today's files are read, never written.

Run: python3 work/build/scripts/phase-2/stage_b_identity_drawings.py [--scratch DIR] [--keep]
Needs Node with Playwright's Chromium (stage_a_identity_shots.js) and Pillow.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage_a_identity_lib as LIB  # noqa: E402
from stage_a_identity_lib import (E, ROOT, ID_DIR, LOCK, AMP, WM, svg_file, mark, mark_style, ink, ink2, hair, pal,  # noqa: E402
                                  tv, ty, curl_html, illus)
import stage_a_identity_q_measure as QM  # noqa: E402  (count, seam_free, feed_counts: read only)

# Since the promotion (November 10, 2026, DR-181) the library's LOCK names the rebuilt files. This board compares them
# with the files that stood before, and traces its outlines from those, so "today" here keeps the earlier files.
LOCK = {**LOCK, **LIB.LOCK_RECT}

DATE = "20261109"
OUT = ROOT / "work/boards/phase-2/stage-b/drawings/identity"
SHOTS = HERE / "stage_a_identity_shots.js"
CAP_EM = 0.7275                       # Inter's cap height in em, as the guide's end mark uses it
END_TEXT = ("The board meets again on April 2, and the agenda posts a week before. We will add the vote to the tracker once "
            "the clerk publishes the minutes.")

# ============================================================================================ outlines from pixels
def trace(pixels):
    """Closed outlines around a set of filled pixels (x, y): outer edges run clockwise on screen and holes the other
    way, so the default nonzero fill draws the pixels exactly. Pixels that touch only at a corner stay separate."""
    P = set(pixels)
    edges = {}

    def add(a, b):
        edges.setdefault(a, []).append(b)
    for (x, y) in P:
        if (x, y - 1) not in P:
            add((x, y), (x + 1, y))
        if (x + 1, y) not in P:
            add((x + 1, y), (x + 1, y + 1))
        if (x, y + 1) not in P:
            add((x + 1, y + 1), (x, y + 1))
        if (x - 1, y) not in P:
            add((x, y + 1), (x, y))
    loops = []
    while edges:
        start = min(edges)
        a = start
        b = edges[a].pop(0)
        if not edges[a]:
            del edges[a]
        pts, prev, cur = [a], a, b
        while cur != start:
            opts = edges[cur]
            n = opts[0]
            if len(opts) > 1:                       # a corner touch: turn right, so the two pixels stay apart
                dx, dy = cur[0] - prev[0], cur[1] - prev[1]
                right = (cur[0] - dy, cur[1] + dx)
                n = right if right in opts else opts[0]
            opts.remove(n)
            if not opts:
                del edges[cur]
            pts.append(cur)
            prev, cur = cur, n
        m = len(pts)
        loops.append([pts[i] for i in range(m)
                      if (pts[i][0] - pts[i - 1][0]) * (pts[(i + 1) % m][1] - pts[i][1])
                      - (pts[i][1] - pts[i - 1][1]) * (pts[(i + 1) % m][0] - pts[i][0]) != 0])
    return loops


def path_d(loops):
    out = []
    for L in sorted(loops, key=lambda L: min((p[1], p[0]) for p in L)):
        i = min(range(len(L)), key=lambda k: (L[k][1], L[k][0]))
        L = L[i:] + L[:i]
        d = f"M{L[0][0]:g} {L[0][1]:g}"
        for (x0, y0), (x1, y1) in zip(L, L[1:]):
            d += f"H{x1:g}" if y1 == y0 else f"V{y1:g}"
        out.append(d + "Z")
    return "".join(out)


def pixels_of(rows):
    return {(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == "#"}


def raster(d, w, h):
    """The pixels a path of H and V moves fills, by the nonzero rule at pixel centers: a check that the outline draws
    exactly the pixels it was traced from."""
    segs = []
    for sub in re.findall(r"M[^M]+", d):
        nums = re.findall(r"([MHVZ])\s*([-\d.]*)\s*([-\d.]*)", sub)
        x = y = None
        pts = []
        for cmd, a, b in nums:
            if cmd == "M":
                x, y = float(a), float(b)
                pts.append((x, y))
            elif cmd == "H":
                x = float(a)
                pts.append((x, y))
            elif cmd == "V":
                y = float(a)
                pts.append((x, y))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
            if x0 == x1 and y0 != y1:
                segs.append((x0, y0, y1))
    out = set()
    for py in range(h):
        cy = py + 0.5
        for px in range(w):
            cx = px + 0.5
            wind = sum((1 if y1 > y0 else -1) for (sx, y0, y1) in segs if sx > cx and min(y0, y1) < cy < max(y0, y1))
            if wind:
                out.add((px, py))
    return out


# ============================================================================================ 1. the end mark
# Drawn by hand on the pixel grid from the 16 px master as it renders at 16 px and from the display master reduced to
# each size: the same loop with its counter tapering to the crossing, the diagonal, the bowl, the arm with its serif
# and the tail. '#' is a full pixel. Fit B is Fit A with one row of the lower half taken out (the diagonal's), the
# bottom kept two rows deep.
B14_A = [
    "...####......",
    "..######.....",
    "..##..##.....",
    "..##..##.....",
    "..###.##.....",
    "...##.##.....",
    "...####..###.",
    "...####...##.",
    "..##.####.##.",
    ".##...######.",
    "###....####..",
    "###.....####.",
    ".############",
    "..#####...###",
]
B14_B = B14_A[:10] + B14_A[11:]
B12_A = [
    "...####....",
    "..##..##...",
    "..##..##...",
    "..##.##....",
    "...###.....",
    "...###.###.",
    "..####..##.",
    ".##.######.",
    "##....###..",
    "##.....###.",
    ".##########",
    "..####..###",
]
B12_B = B12_A[:6] + B12_A[7:]

# key: (rows, text px it serves, vertical-align in px, file stem words, one-line description)
END_FITS = {
    "14A": (B14_A, 17, -1, "Amp-B-14px-End-Mark-Fit-A",
            "14 px tall, 13 wide. Its top row sits on the capitals' top row and its tail one row under the baseline, the "
            "master's overshoot kept, as today's end mark sits (DR-130)"),
    "14B": (B14_B, 17, 0, "Amp-B-14px-End-Mark-Fit-B",
            "13 px tall, 13 wide. Its top row sits on the capitals' top row and its bowl and tail on the baseline, as a "
            "typeface sits its round letters at text sizes"),
    "12A": (B12_A, 15, -1, "Amp-B-12px-End-Mark-Fit-A",
            "12 px tall, 11 wide. Its top row sits on the capitals' top row and its tail one row under the baseline, the "
            "master's overshoot kept, as today's end mark sits (DR-130)"),
    "12B": (B12_B, 15, 0, "Amp-B-12px-End-Mark-Fit-B",
            "11 px tall, 11 wide. Its top row sits on the capitals' top row and its bowl and tail on the baseline, as a "
            "typeface sits its round letters at text sizes"),
}


def counters(rows):
    """Enclosed spaces in a drawing: the background regions that do not reach the edge (4-connected)."""
    w, h = len(rows[0]), len(rows)
    bg = {(x, y) for y in range(h) for x in range(w) if rows[y][x] != "#"}
    n = 0
    while bg:
        stack = [bg.pop()]
        comp, edge = set(stack), False
        while stack:
            x, y = stack.pop()
            if x in (0, w - 1) or y in (0, h - 1):
                edge = True
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if q in bg:
                    bg.remove(q)
                    comp.add(q)
                    stack.append(q)
        n += not edge
    return n


def end_files():
    out = {}
    for k, (rows, text_px, va, stem, desc) in END_FITS.items():
        w, h = len(rows[0]), len(rows)
        assert all(len(r) == w for r in rows), k
        assert counters(rows) == 2, f"{k}: B must keep exactly its two counters, the loop's and the bowl's"
        d = path_d(trace(pixels_of(rows)))
        assert raster(d, w, h) == pixels_of(rows), f"{k}: the outline does not draw its pixels"
        title = (f"Ampersand B, pixel-fit end mark for {text_px} px text, fit {k[-1]}: {desc}. Set it with "
                 f"vertical-align {va} px, half an em after the period. Drawn on the pixel grid as one path, its outline and its two counters (DR-142, stage B)")
        color = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><title>{E(title)}</title>'
                 f'<path fill="currentColor" d="{d}"/></svg>\n')
        white = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><title>{E(title)}. Treatment D for Prussian: one color, White</title>'
                 f'<path fill="#FFFFFF" d="{d}"/></svg>\n')
        f1 = ID_DIR / "ampersand" / f"{DATE}_{stem}.svg"
        f2 = ID_DIR / "prussian" / f"{DATE}_{stem}-Prussian-White.svg"
        f1.write_text(color)
        f2.write_text(white)
        out[k] = {"file": LIB.rel(f1), "prussian": LIB.rel(f2), "width_px": w, "height_px": h, "text_px": text_px,
                  "vertical_align_px": va, "ink_px": len(pixels_of(rows)), "subpaths": d.count("M")}
    return out


def end_mark_html(key, surface="newsprint"):
    """B as the end mark: today's (stage_a_identity_s04.end_b) or a pixel fit at its own size."""
    if key in ("T17", "T15"):
        import stage_a_identity_s04 as S04
        return S04.end_b(int(key[1:]), surface)
    rows, text_px, va, stem, _ = END_FITS[key]
    f = ID_DIR / "ampersand" / f"{DATE}_{stem}.svg"
    return svg_file(f, h=len(rows), decorative=True,
                    style=f"color:{ink(surface)};display:inline-block;vertical-align:{va}px;margin-left:0.5em")


def end_line(key, text_px, surface="newsprint", width=520, head_id=None):
    head, last = END_TEXT.rsplit(" ", 1)
    hid = f' id="{head_id}"' if head_id else ""
    return (f'<p{hid} style="{ty("body", size=text_px)};width:{width}px;margin:0;color:{ink(surface)}">{E(head)} '
            f'<span style="white-space:nowrap">{E(last)}{end_mark_html(key, surface)}</span></p>')


# ============================================================================================ 2. the lockmark
def rects_by_group(svg_text):
    """The rect pixels of each fill group of a pixel master: links, nodes (currentColor) and lever."""
    groups = {}
    for m in re.finditer(r'<g fill="([^"]+)">(.*?)</g>', svg_text, flags=re.S):
        px = set()
        for r in re.finditer(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"/>', m.group(2)):
            x, y, w, h = (float(v) for v in r.groups())
            if x.is_integer() and y.is_integer() and w.is_integer() and h.is_integer():
                px |= {(int(x) + i, int(y) + j) for i in range(int(w)) for j in range(int(h))}
        groups[m.group(1)] = (m.group(0), px)
    return groups


def components(px):
    px, out = set(px), []
    while px:
        stack = [px.pop()]
        comp = set(stack)
        while stack:
            x, y = stack.pop()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in px:
                    px.remove(n)
                    comp.add(n)
                    stack.append(n)
        out.append(comp)
    return sorted(out, key=lambda c: (min(p[1] for p in c), min(p[0] for p in c)))


LOCK_NEW = {24: f"lockmark/{DATE}_Lockmark-24px-Master-Outline.svg", 48: f"lockmark/{DATE}_Lockmark-48px-Master-Outline.svg"}


def lockmark_files():
    """Rebuild the 24 and 48 px masters: the links stay as today's rects, byte for byte; each node and the lever become
    one outline traced from today's pixel rows. Asserts that each outline draws exactly the pixels it replaces."""
    out = {}
    for size in (24, 48):
        src = (ID_DIR / LOCK[size]).read_text()
        g = rects_by_group(src)
        link_xml, _ = g["var(--link,#5D636D)"]
        _, node_px = g["currentColor"]
        _, lever_px = g["var(--lever,#E63946)"]
        nodes = components(node_px)
        levers = components(lever_px)
        assert len(nodes) == 8 and len(levers) == 1, (size, len(nodes), len(levers))
        node_d = [path_d(trace(c)) for c in nodes]
        lever_d = path_d(trace(levers[0]))
        for d, c in zip(node_d + [lever_d], nodes + levers):
            assert d.count("M") == 1, "each node and the lever must be one outline"
            assert raster(d, size, size) == c, "an outline does not draw the pixels it replaces"
        if size == 24:
            title = ("Lockmark, 24 px master on the pixel grid, rebuilt (DR-145): each node and the lever one outline, the same "
                     "pixels as the October master at 24 px. For 24 to 47 px. Centers at 3.5, 11.5 and 19.5 px, 5 px nodes, a 7 px lever, 1 px links")
        else:
            title = ("Lockmark, 48 px master on the pixel grid, rebuilt (DR-145): each node and the lever one outline, the same "
                     "pixels as the November 8 master at 48 px. The masthead and the sign-off. Centers at 4.5, 23.5 and 42.5 px, 7 px nodes, a 9 px lever, 1 px links")
        nodes_xml = "".join(f'<path d="{d}"/>' for d in node_d)
        body = (f'{link_xml}<g fill="currentColor">{nodes_xml}</g><path fill="var(--lever,#E63946)" d="{lever_d}"/>')
        color = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"><title>{E(title)}</title>{body}</svg>\n'
        wbody = (link_xml.replace('fill="var(--link,#5D636D)"', 'fill="#FFFFFF"') + f'<g fill="#FFFFFF">{nodes_xml}</g>'
                 f'<path fill="#FFFFFF" d="{lever_d}"/>')
        white = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"><title>{E(title)}. Treatment D for Prussian: '
                 f'one color, White</title>{wbody}</svg>\n')
        f1 = ID_DIR / LOCK_NEW[size]
        f2 = ID_DIR / "prussian" / (Path(LOCK_NEW[size]).stem + "-Prussian-White.svg")
        f1.write_text(color)
        f2.write_text(white)
        assert re.findall(r"#[0-9A-Fa-f]{6}", white) and set(re.findall(r"#[0-9A-Fa-f]{6}", white)) == {"#FFFFFF"}
        out[size] = {"file": LIB.rel(f1), "prussian": LIB.rel(f2), "today": LOCK[size], "links_unchanged": link_xml in src,
                     "node_outlines": len(node_d), "lever_outlines": 1,
                     "rects_today": src.count("<rect"), "rects_rebuilt": color.count("<rect"), "paths_rebuilt": color.count("<path")}
    return out


# ============================================================================================ 3. L6 centered
# L6 on the fifth edition's layout, 1400 by 300 units (stage_a_identity_s03.l6). The wordmark's cap line and baseline
# are its master's y 4 and 104 in a 108-unit box; the tagline's are y 4 and 104 in a box from y -0.77, 133.36 tall.
L6_WM_TOP, L6_WM_H = 82.5, 50.8
L6_TL_TOP, L6_TL_W, L6_TL_VB = 170.46, 363.34, (2422.29, -0.77, 133.36)
L6_LK_LEFT, L6_LK_TOP, L6_LK = 1170.5, 74.9, 148


def l6_geometry():
    k_wm = L6_WM_H / 108
    k_tl = L6_TL_W / L6_TL_VB[0]
    cap = L6_WM_TOP + 4 * k_wm
    base = L6_TL_TOP + (104 - L6_TL_VB[1]) * k_tl
    desc = L6_TL_TOP + L6_TL_VB[2] * k_tl
    k_lk = L6_LK / 123.5
    lk_top, lk_bot = L6_LK_TOP + (11.75 - 3.8) * k_lk, L6_LK_TOP + (111.75 + 4.75) * k_lk
    shift = 150 - (cap + base) / 2
    return {"units": "L6's 1400 by 300 units; 884 px wide is 0.6314 px per unit",
            "wordmark_cap_line": round(cap, 2), "tagline_baseline": round(base, 2), "tagline_descender_bottom": round(desc, 2),
            "group_middle_today": round((cap + base) / 2, 2), "strip_middle": 150.0,
            "lockmark_ink_top": round(lk_top, 2), "lockmark_ink_bottom": round(lk_bot, 2), "lockmark_ink_middle": round((lk_top + lk_bot) / 2, 2),
            "shift_down_units": round(shift, 2), "shift_down_px_at_884": round(shift * 884 / 1400, 2),
            "middle_with_descenders_today": round((cap + desc) / 2, 2),
            "shift_if_descenders_counted_units": round(150 - (cap + desc) / 2, 2),
            "centered_cap_line": round(cap + shift, 2), "centered_baseline": round(base + shift, 2)}


def l6_centered(width_px, shift_units):
    """L6 without its dots, with the wordmark and tagline moved down by shift_units; the lockmark, the strip and every
    size stay as stage_a_identity_s03.l6 draws them."""
    k = width_px / 1400
    wh = pal("white")
    wm = mark(WM["display"], h=L6_WM_H * k, surface="prussian", decorative=True)
    t1 = svg_file(ID_DIR / LIB.TL1, w=L6_TL_W * k, style=f"color:{wh}", decorative=True)
    lk = LIB.lockmark(L6_LK * k, surface="prussian", decorative=True)
    return (f'<span role="img" aria-label="Oath &amp; Action, L6 editorial signature on Prussian, all in White, with the wordmark and the '
            f'tagline centered on the strip: the wordmark, the tagline and the lockmark." '
            f'style="position:relative;display:block;width:{width_px:.1f}px;height:{300 * k:.1f}px;background:{tv("color-surface-prussian")}">'
            f'<span style="position:absolute;left:{80 * k:.1f}px;top:{(L6_WM_TOP + shift_units) * k:.1f}px">{wm}</span>'
            f'<span style="position:absolute;left:{80 * k:.1f}px;top:{(L6_TL_TOP + shift_units) * k:.1f}px">{t1}</span>'
            f'<span style="position:absolute;left:{L6_LK_LEFT * k:.1f}px;top:{L6_LK_TOP * k:.1f}px">{lk}</span></span>')


# ============================================================================================ rendering and counting
def page(title, body, css=""):
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<style>{tokens}</style><style>{LIB.CSS}{PAGE_CSS}{css}</style></head>'
            f'<body><div class="bd oai">{curl_html(body)}</div></body></html>')


PAGE_CSS = """
body{margin:0;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);font-family:var(--oa-font-family-reading)}
.bd{padding:32px;display:flex;flex-direction:column;gap:40px}
.bd h1{font:800 26px/1.2 var(--oa-font-family-display);letter-spacing:-0.01em;margin:0}
.bd .lede{font-size:15px;line-height:1.5;max-width:72ch;margin:8px 0 0;color:var(--oa-color-text-secondary-on-newsprint)}
.plate{background:var(--oa-color-surface-newsprint);border:1px solid var(--oa-color-border-hairline-on-newsprint);padding:24px;display:inline-flex;flex-direction:column;gap:20px;align-self:flex-start}
.plate h2{font:700 13px/1.4 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;margin:0}
.plate h3{font:700 15px/1.4 var(--oa-font-family-reading);margin:0}
.fig{font-size:13px;line-height:1.45;color:var(--oa-color-text-secondary-on-newsprint);margin:4px 0 0;max-width:66ch}
.row{display:flex;gap:32px;align-items:flex-start;flex-wrap:nowrap}
.illus{display:inline-block;align-self:flex-start;padding:0 .4em;border:1px solid currentColor;font:700 13px/1.5 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase}
.cell{display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.opt{font:700 13px/1.4 var(--oa-font-family-reading);letter-spacing:.04em;text-transform:uppercase;color:var(--oa-color-text-primary-on-newsprint)}
.grid{display:grid;gap:16px 28px;align-items:end}
.grid .h{font:600 13px/1.4 var(--oa-font-family-reading);color:var(--oa-color-text-secondary-on-newsprint)}
.px{image-rendering:pixelated;display:block}
.strip{padding:12px 16px}
"""


def shoot(html_path, out_dir, ids, scale):
    r = subprocess.run(["node", str(SHOTS), str(html_path), str(out_dir), str(scale), *ids], check=True, capture_output=True, text=True)
    return json.loads(r.stdout.strip().splitlines()[-1])["fonts"]


def enlarge(img, k, path):
    from PIL import Image
    img.resize((img.width * k, img.height * k), Image.NEAREST).save(path)


# ----------------------------------------------------------------------------- measurement page and tests
LK_CELLS = [("today", 16, s) for s in (16, 17, 18, 20, 23)] + [("today", 24, s) for s in (24, 34, 40, 47)] + \
           [("today", 48, s) for s in (48, 49, 56, 72, 96)] + [("new", 24, s) for s in (24, 34, 40, 47)] + \
           [("new", 48, s) for s in (48, 49, 56, 72, 96)]
QM.CORES.setdefault("m16", (16, (2.5, 2.5, 1.5), (12.5, 12.5, 2.5)))


def lk_file(kind, master):
    return ID_DIR / (LOCK[master] if kind == "today" else LOCK_NEW[master])


def lk_html(kind, master, size, surface="newsprint", label=None):
    if surface == "prussian":
        f = ID_DIR / "prussian" / (lk_file(kind, master).stem + "-Prussian-White.svg")
        return svg_file(f, h=size, label=label or f"Lockmark at {size} px", style="")
    return svg_file(lk_file(kind, master), h=size, label=label or f"Lockmark at {size} px", style=mark_style(surface))


EM_OFFSETS = (0, 0.25, 0.5, 0.75)


def _runs(img, surface, unit, trim):
    """H and B in one cell: the first ink run of columns is H, the rest is B. Returns each one's top and bottom edges
    in CSS px (device rows divided by unit) and the share of B's ink pixels at full color. trim drops the cell's edge,
    where the page's ground can show."""
    im = img.convert("RGB")
    im = im.crop((trim, trim, im.width - trim, im.height - trim))
    W, H = im.size
    px = im.load()
    ground = (0xDC, 0xD9, 0xD2) if surface == "newsprint" else (0x12, 0x12, 0x12)
    inkc = (0x12, 0x12, 0x12) if surface == "newsprint" else (0xDC, 0xD9, 0xD2)
    span = max(abs(a - b) for a, b in zip(ground, inkc))
    cov = [[max(abs(a - b) for a, b in zip(px[x, y], ground)) / span for x in range(W)] for y in range(H)]
    thresh = 0.43 if unit == 8 else 0.18              # at 8x the fix pass's threshold; at 1x any visible ink
    cols = [x for x in range(W) if any(cov[y][x] > thresh for y in range(H))]
    runs, start, prev = [], cols[0], cols[0]
    for x in cols[1:]:
        if x != prev + 1:
            runs.append((start, prev))
            start = x
        prev = x
    runs.append((start, prev))

    def rows(x0, x1):
        ys = [y for y in range(H) if any(cov[y][x] > thresh for x in range(x0, x1 + 1))]
        return ys[0] / unit, (ys[-1] + 1) / unit
    b0, b1 = runs[1][0], runs[-1][1]
    inked = [cov[y][x] for y in range(H) for x in range(b0, b1 + 1) if cov[y][x] > 0.05]
    full = sum(1 for v in inked if v >= 0.95)
    return {"h": rows(*runs[0]), "b": rows(b0, b1), "full": round(full / len(inked), 3) if inked else None}


def measure(scratch):
    """Render every test cell at 1x and 2x and count it. Returns the figures and the folder of renders."""
    from PIL import Image, ImageChops
    cells, ids = [], []
    for kind, m, s in LK_CELLS:
        i = f"lk-{kind}-{m}-{s}"
        ids.append(i)
        cells.append(f'<div class="cell2" id="{i}" style="width:{s}px;height:{s}px;line-height:0">{lk_html(kind, m, s)}</div>')
    for kind in ("today", "new"):
        for s in (24, 48):
            i = f"lkc-{kind}-{s}"            # on Charcoal, to compare the files on a dark ground too
            ids.append(i)
            cells.append(f'<div class="cell2" id="{i}" style="width:{s}px;height:{s}px;line-height:0;background:{tv("color-surface-charcoal")}">{lk_html(kind, s, s, "charcoal")}</div>')
            i = f"lkp-{kind}-{s}"
            ids.append(i)
            cells.append(f'<div class="cell2" id="{i}" style="width:{s}px;height:{s}px;line-height:0;background:{tv("color-surface-prussian")}">{lk_html(kind, s, s, "prussian")}</div>')
    for key in ("T17", "14A", "14B", "T15", "12A", "12B"):
        f = 17 if key in ("T17", "14A", "14B") else 15
        for surface in ("newsprint", "charcoal"):
            for o in EM_OFFSETS:
                i = f"em-{key}-{surface}-{int(o * 100)}"
                ids.append(i)
                bg = tv(f"color-surface-{surface}")
                # a fixed 48 px cell; the line starts o px lower, so the baseline falls between pixels as it does in a page
                cells.append(f'<div class="cell2" id="{i}" style="width:max-content;height:48px;padding:{8 + o}px 8px 0;background:{bg};{ty("body", size=f)};'
                             f'line-height:28px;color:{ink(surface)}">H{end_mark_html(key, surface).replace("margin-left:0.5em", "margin-left:6px")}</div>')
    html = page("measure", "".join(cells), ".cell2{position:relative;margin:0 0 8px 8px;flex:none}.bd{gap:0;flex-direction:row;flex-wrap:wrap;align-items:flex-start}")
    p = scratch / "measure.html"
    p.write_text(html)
    fonts = None
    for scale in (1, 2, 8):
        sel = ids if scale != 8 else [i for i in ids if i.startswith("em-") and i.endswith("-0")]
        fonts = shoot(p, scratch / f"m{scale}", sel, scale)
    res = {"fonts_loaded": fonts, "lockmark": {"at_1x": {}, "at_2x": {}}, "identical_at_own_size": {}, "end_mark": {}}
    for scale in (1, 2):
        for kind, m, s in LK_CELLS:
            img = Image.open(scratch / f"m{scale}" / f"lk-{kind}-{m}-{s}@{scale}x.png")
            kk = "m16" if m == 16 else ("m24" if m == 24 else "m48")
            res["lockmark"][f"at_{scale}x"][f"{kind}-{m}-at-{s}"] = dict(QM.count(img), **QM.seam_free(img, kk, s, scale))
    for m in (24, 48):
        for scale in (1, 2):
            for pre in ("lk", "lkc", "lkp"):
                a = Image.open(scratch / f"m{scale}" / (f"lk-today-{m}-{m}@{scale}x.png" if pre == "lk" else f"{pre}-today-{m}@{scale}x.png")).convert("RGB")
                b = Image.open(scratch / f"m{scale}" / (f"lk-new-{m}-{m}@{scale}x.png" if pre == "lk" else f"{pre}-new-{m}@{scale}x.png")).convert("RGB")
                diff = ImageChops.difference(a, b).getbbox()
                ground = {"lk": "newsprint", "lkc": "charcoal", "lkp": "prussian"}[pre]
                res["identical_at_own_size"][f"{m}px-{ground}-{scale}x"] = (a.size == b.size and diff is None)
    # the end mark. At eight times, offset 0: B's height, its top over the cap line and its tail under the baseline,
    # as stage_a_identity_q_measure.endmark_test measures them. At 1x and 2x, every offset: which device rows H and B
    # cover, and the share of B's ink pixels drawn at full color.
    for key in ("T17", "14A", "14B", "T15", "12A", "12B"):
        for surface in ("newsprint", "charcoal"):
            rec = {"text_px": 17 if key in ("T17", "14A", "14B") else 15}
            m8 = _runs(Image.open(scratch / "m8" / f"em-{key}-{surface}-0@8x.png"), surface, 8, trim=16)
            rec.update({"capitals_px": round(m8["h"][1] - m8["h"][0], 2), "b_px": round(m8["b"][1] - m8["b"][0], 2),
                        "top_over_cap_line_px": round(m8["h"][0] - m8["b"][0], 2), "tail_under_baseline_px": round(m8["b"][1] - m8["h"][1], 2)})
            for scale in (1, 2):
                per = []
                for o in EM_OFFSETS:
                    im = Image.open(scratch / f"m{scale}" / f"em-{key}-{surface}-{int(o * 100)}@{scale}x.png")
                    r = _runs(im, surface, 1, trim=2 * scale)
                    per.append({"offset_px": o, "b_rows": r["b"][1] - r["b"][0], "top_rows_over_h": r["h"][0] - r["b"][0],
                                "tail_rows_under_h": r["b"][1] - r["h"][1], "b_full_ink_share": r["full"]})
                rec[f"rows_at_{scale}x"] = per
            rec["b_full_ink_share_at_1x"] = min(q["b_full_ink_share"] for q in rec["rows_at_1x"])
            res["end_mark"][f"{key}-{surface}"] = rec
    return res


def feed(scratch):
    """D2-468's feed test on the proofs' 1200 by 630 card drawn standalone, as stage_a_identity_q_measure.feed_control
    draws it, with today's 48 px master and with the rebuilt one in the sign-off."""
    from PIL import Image
    import stage_a_identity_proofs as SP
    keep = SP.lockmark
    cards = {}
    try:
        for k in ("today", "new"):
            SP.lockmark = (lambda kk: (lambda s, **kw: svg_file(lk_file(kk, 48), h=s, label="Lockmark", style=mark_style("newsprint"))))(k)
            cards[k] = f'<div id="card-{k}" style="width:1200px">{SP._social()}</div>'
    finally:
        SP.lockmark = keep
    p = scratch / "feed.html"
    p.write_text(page("feed", "".join(cards.values()), ".bd{padding:0;gap:0}"))
    shoot(p, scratch / "feed", [f"card-{k}" for k in cards], 1)
    out = {"card_px": [1200, 630], "lockmark_box_in_card": [1079, 509, 48, 48], "min_red_px": QM.FEED_MIN_RED, "filter": "Lanczos"}
    crops = {}
    for k in cards:
        card = Image.open(scratch / "feed" / f"card-{k}@1x.png").convert("RGB")
        assert card.size == (1202, 632) or card.size == (1200, 630), card.size
        out[k] = {}
        for w in QM.FEED_WIDTHS:
            s = w / 1200
            small = card.resize((round(card.width * s), round(card.height * s)), Image.LANCZOS)
            out[k][f"at_{w}"] = QM.feed_counts(small, 1079, 509, s)
            box = (int(1079 * s) - 1, int(509 * s) - 1, int(1127 * s + 0.999) + 1, int(557 * s + 0.999) + 1)
            crops[f"{k}-{w}"] = small.crop(box)
    a = Image.open(scratch / "feed" / "card-today@1x.png").convert("RGB").crop((1071, 501, 1135, 565))
    b = Image.open(scratch / "feed" / "card-new@1x.png").convert("RGB").crop((1071, 501, 1135, 565))
    out["same_pixels_in_sign_off"] = a.tobytes() == b.tobytes()     # the lockmark's box plus 8 px, in the 1200 px card
    return out, crops


def pixel_fit_check(scratch):
    """The engineer's check (icon_pixel_fit_check.js) on every new master at its own size. The check sets a square box,
    so B's masters run on square copies padded on the right, which keeps them on whole pixels."""
    files = []
    for k, (rows, *_rest) in END_FITS.items():
        w, h = len(rows[0]), len(rows)
        n = max(w, h)
        src = (ID_DIR / "ampersand" / f"{DATE}_{END_FITS[k][3]}.svg").read_text()
        sq = src.replace(f'viewBox="0 0 {w} {h}"', f'viewBox="0 0 {n} {n}"')
        f = scratch / f"{DATE}_{END_FITS[k][3]}-Square.svg"
        f.write_text(sq)
        files.append((f, n, f"ampersand/{DATE}_{END_FITS[k][3]}.svg"))
    for s in (24, 48):
        files.append((ID_DIR / LOCK_NEW[s], s, LOCK_NEW[s]))
        files.append((ID_DIR / LOCK[s], s, LOCK[s] + " (today, for comparison)"))
    files.append((ID_DIR / LOCK[16], 16, LOCK[16] + " (today, unchanged)"))
    res = {}
    for f, n, name in files:
        j = scratch / f"pfc-{f.stem}-{n}.json"
        r = subprocess.run(["python3", "-I", str(HERE / "icon_pixel_fit_check.py"), "--size", str(n), "--json", str(j), "--quiet", str(f)],
                           capture_output=True, text=True)
        try:
            data = json.loads(j.read_text())
        except Exception:
            data = {"error": (r.stderr or r.stdout)[-400:]}
        res[name] = {"size": n, "exit": r.returncode, "result": data}
    return res


# ============================================================================================ the plate page
def figure_line(m):
    """Measured at eight times, then at 1x with the line set at four positions between pixels."""
    r = m["rows_at_1x"]

    def span(key):
        lo, hi = min(q[key] for q in r), max(q[key] for q in r)
        return (lo, hi)
    top, tail, rows = span("top_rows_over_h"), span("tail_rows_under_h"), span("b_rows")
    word = {0: "no rows", 1: "one row", 2: "two rows"}
    t_top = "its top row on the capital H\'s top row" if top == (0, 0) else (
        f"its top {word[top[0]]} over H\'s" if top[0] == top[1] else f"its top {top[0]:.0f} to {top[1]:.0f} rows over H\'s")
    t_tail = "its last row on H\'s last row" if tail == (0, 0) else (
        f"its last row {word[tail[0]]} under H\'s" if tail[0] == tail[1] else f"its last row {tail[0]:.0f} to {tail[1]:.0f} rows under H\'s, by where the line falls")
    t_rows = f"{rows[0]:.0f} rows" if rows[0] == rows[1] else f"{rows[0]:.0f} to {rows[1]:.0f} rows"
    under = ("its bowl and tail on the baseline" if m["tail_under_baseline_px"] == 0
             else f'its tail {m["tail_under_baseline_px"]:.1f} px under the baseline')
    return (f'Capitals {m["capitals_px"]:.1f} px; B {m["b_px"]:.1f} px tall, its top {m["top_over_cap_line_px"]:.1f} px over the cap line and {under}. '
            f'At 1x, with the line at four positions between pixels, B covers {t_rows}, {t_top} and {t_tail}; '
            f'{m["b_full_ink_share_at_1x"] * 100:.0f} percent of its ink pixels are full Charcoal.')


def plates(figs, imgs):
    em = figs["measure"]["end_mark"]
    lk = figs["measure"]["lockmark"]
    fd = figs["feed"]
    g6 = figs["l6"]
    pct = lambda v: f"{v * 100:.0f} percent"   # noqa: E731

    # ---- the end mark
    groups = []
    for text_px, keys in ((17, ("T17", "14A", "14B")), (15, ("T15", "12A", "12B"))):
        rows = []
        for key in keys:
            m = em[f"{key}-newsprint"]
            if key.startswith("T"):
                name = "Today"
                what = "B from its 16 px master, scaled to 16/14 of the cap height (DR-130, D2-470)."
            else:
                rows_, _, va, stem, desc = END_FITS[key]
                name = f"Fit {key[-1]}"
                what = desc[0].upper() + desc[1:] + "."
            rows.append(f'<div class="cell" id="em-{key}"><p class="opt">{E(name)}</p>{end_line(key, text_px)}'
                        f'<div class="row" style="gap:20px;align-items:flex-end">'
                        f'<div class="cell"><img class="px" src="{imgs[f"em-{key}-1x"]}" alt="" width="{imgs[f"em-{key}-1x-w"]}"><p class="fig" style="margin:0">At 1x, eight times, beside a capital H of the same text</p></div>'
                        f'<div class="cell"><img class="px" src="{imgs[f"em-{key}-2x"]}" alt="" width="{imgs[f"em-{key}-2x-w"]}"><p class="fig" style="margin:0">On a 2x screen, four times</p></div>'
                        f'</div><p class="fig">{E(what)} {E(figure_line(m))}</p></div>')
        dark = "".join(f'<div class="cell"><p class="fig" style="margin:0;color:{ink2("charcoal")}">{E("Today" if k.startswith("T") else "Fit " + k[-1])}</p>'
                       f'{end_line(k, text_px, "charcoal", width=420)}</div>' for k in keys)
        groups.append(f'<div class="cell" style="gap:24px"><h3>B at {text_px - 3} px: the end mark in {text_px} px text</h3>{"".join(rows)}'
                      f'<div class="oai-s-charcoal strip" style="display:flex;flex-direction:column;gap:12px">{dark}</div></div>')
    end_plate = (f'<section class="plate" id="card-end-mark"><h2>End mark: ampersand B at 14 and 12 px</h2>'
                 f'<p class="fig" style="margin:0">Each line ends a paragraph at true size. The paragraph is invented. Each fit is one drawing on whole pixels; '
                 f'today\'s end mark is the 16 px master scaled, so its edges soften at 1x.</p>{illus()}'
                 f'<div class="row" style="gap:56px">{"".join(groups)}</div></section>')

    # ---- the lockmark masters
    sizes = (16, 24, 34, 40, 48)

    def master_for(s):
        return 16 if s < 24 else (24 if s < 48 else 48)
    head = "".join(f'<p class="h">{s} px</p>' for s in sizes)
    row_today = "".join(f'<div class="cell">{lk_html("today", master_for(s), s, label=f"Today, {s} px")}</div>' for s in sizes)
    row_new = "".join(f'<div class="cell">{lk_html("new" if master_for(s) != 16 else "today", master_for(s), s, label=f"Rebuilt, {s} px")}</div>' for s in sizes)

    def core(kind, s):
        if s == 16:
            return "one circle per node"
        m = master_for(s)
        kind = kind if m != 16 else "today"
        v = lk["at_1x"].get(f"{kind}-{m}-at-{s}")
        return f'nodes whole {pct(v["node_core_full"])}' if v else ""
    row_core_t = "".join(f'<p class="fig" style="margin:0">{core("today", s)}</p>' for s in sizes)
    row_core_n = "".join(f'<p class="fig" style="margin:0">{core("new", s)}</p>' for s in sizes)
    enl_t = "".join(f'<img class="px" src="{imgs[f"lk-today-{s}"]}" alt="" width="{imgs[f"lk-today-{s}-w"]}">' for s in sizes)
    enl_n = "".join(f'<img class="px" src="{imgs[f"lk-new-{s}"]}" alt="" width="{imgs[f"lk-new-{s}-w"]}">' for s in sizes)
    files_line = ("Files: 16 px, today's file, unchanged (its nodes and lever are already one shape each). 24 px, "
                  f"{Path(LOCK_NEW[24]).name}. 48 px, {Path(LOCK_NEW[48]).name}. Each Prussian White file sits in prussian/.")
    surf = "".join(
        f'<div class="cell"><div class="oai-s-{s} strip" style="display:flex;gap:20px;align-items:flex-end">'
        + "".join(lk_html("new", m, m, s, label=f"Rebuilt {m} px on {s.title()}") for m in (24, 48))
        + f'</div><p class="fig" style="margin:0">Rebuilt 24 and 48 px on {s.title()}</p></div>' for s in ("charcoal", "prussian"))
    two_x = (f'<div class="row" style="gap:32px;align-items:flex-end">'
             f'<div class="cell"><img class="px" src="{imgs["lk2x-today-48"]}" alt="" width="{imgs["lk2x-today-48-w"]}"><p class="fig" style="margin:0">Today\'s 48 px master on a 2x screen, four times</p></div>'
             f'<div class="cell"><img class="px" src="{imgs["lk2x-new-48"]}" alt="" width="{imgs["lk2x-new-48-w"]}"><p class="fig" style="margin:0">Rebuilt 48 px master on a 2x screen, four times</p></div>'
             f'<div class="cell"><img class="px" src="{imgs["lk2x-disp-96"]}" alt="" width="{imgs["lk2x-disp-96-w"]}"><p class="fig" style="margin:0">For comparison: the display master at 48 px on a 2x screen, four times</p></div></div>')
    feed_rows = "".join(
        f'<div class="cell"><p class="opt">{E(n)}</p><div class="row" style="gap:16px;align-items:flex-end">'
        + "".join(f'<div class="cell"><img class="px" src="{imgs[f"feed-{k}-{w}"]}" alt="" width="{imgs[f"feed-{k}-{w}-w"]}">'
                  f'<p class="fig" style="margin:0">Card at {w} px: {fd[k][f"at_{w}"]["dark_nodes_kept"]} of 8 nodes, '
                  f'{fd[k][f"at_{w}"]["lever_red_px"]} red pixels</p></div>' for w in (500, 360))
        + '</div></div>' for k, n in (("today", "Today's 48 px master"), ("new", "Rebuilt 48 px master")))
    lock_plate = (f'<section class="plate" id="card-lockmark"><h2>Lockmark masters rebuilt: today and rebuilt at 16, 24, 34, 40 and 48 px</h2>'
                  f'<p class="fig" style="margin:0">Each size draws the master its range names: 16 px from the 16 px master, 24 to 40 px from the 24 px master, 48 px from the 48 px master. '
                  f'At 24 and 48 px the rebuilt files draw the same pixels as today\'s. Between those sizes, today\'s rows part into light stripes and the rebuilt nodes stay whole.</p>'
                  f'<div class="grid" style="grid-template-columns:96px repeat(5,max-content)">'
                  f'<span></span>{head}<p class="opt">Today</p>{row_today}<span></span>{row_core_t}'
                  f'<p class="opt">Rebuilt</p>{row_new}<span></span>{row_core_n}</div>'
                  f'<p class="fig" style="margin:0">{E(files_line)}</p>'
                  f'<h3>At 1x, six times</h3><div class="grid" style="grid-template-columns:96px repeat(5,max-content);align-items:start">'
                  f'<p class="opt">Today</p>{enl_t}<p class="opt">Rebuilt</p>{enl_n}</div>'
                  f'<h3>The 48 px master on a 2x screen</h3>{two_x}'
                  f'<p class="fig" style="margin:0">On a 2x screen the rebuilt master draws the same stepped nodes as today\'s: each 7 px node doubles into a 14 px shape with 2 px steps.</p>'
                  f'<h3>On Charcoal and Prussian</h3><div class="row" style="gap:24px">{surf}</div>'
                  f'<h3>The sign-off when a feed shrinks the card, eight times (D2-468)</h3><div class="row" style="gap:40px">{feed_rows}</div>'
                  f'<p class="fig" style="margin:0">The rebuilt master draws the sign-off on the 1200 px card pixel for pixel as today\'s does, so a feed that shrinks the card gets the same result: '
                  f'{fd["new"]["at_360"]["lever_red_px"]} red pixels at 360 px against a floor of {fd["min_red_px"]}.</p></section>')

    # ---- L6 centered
    l6_plate = (f'<section class="plate" id="card-l6"><h2>L6 centered: the wordmark and tagline on the strip\'s middle</h2>'
                f'<div class="cell"><p class="opt">Today, without its dots (DR-129)</p>{L6_TODAY}'
                f'<p class="fig">The wordmark\'s cap line meets the top of the lockmark\'s nodes. The span from the cap line to the tagline\'s baseline has its middle '
                f'{g6["strip_middle"] - g6["group_middle_today"]:.1f} units over the strip\'s middle, {(g6["strip_middle"] - g6["group_middle_today"]) * 884 / 1400:.1f} px at 884 px.</p></div>'
                f'<div class="cell"><p class="opt">Proposal: centered</p>{L6_CENTERED}'
                f'<p class="fig">The wordmark and tagline move down {g6["shift_down_units"]:.1f} units, {g6["shift_down_px_at_884"]:.1f} px at 884 px, so the span from the cap line to the '
                f'tagline\'s baseline is centered on the strip, as the lockmark is. The wordmark\'s cap line now stands {g6["centered_cap_line"] - g6["lockmark_ink_top"]:.1f} units '
                f'under the lockmark\'s top nodes and the tagline\'s baseline {g6["lockmark_ink_bottom"] - g6["centered_baseline"]:.1f} units over its bottom nodes. Nothing else moves.</p></div>'
                f'<p class="fig" style="margin:0">Both at 884 px, L6\'s minimum on screen, on Prussian in White.</p></section>')

    body = ('<header><h1>Identity drawings for the drawings board</h1><p class="lede">Three cards, each at true size on Newsprint: the end mark drawn on whole '
            'pixels at 14 and 12 px, two fits each; the lockmark\'s 24 and 48 px masters rebuilt with each node and the lever as one outline; and L6 with '
            'its wordmark and tagline centered on the strip. Enlarged views are labeled with their magnification.</p></header>'
            + end_plate + lock_plate + l6_plate)
    return body


L6_TODAY = L6_CENTERED = ""


WORD = {"today": "Today", "new": "Rebuilt"}


def ink_box(img, surface="newsprint", pad=2, trim=2):
    """The box around a cell's ink at 1x, with pad px around it, inside the cell's trimmed edge."""
    im = img.convert("RGB")
    ground = (0xDC, 0xD9, 0xD2) if surface == "newsprint" else (0x12, 0x12, 0x12)
    px = im.load()
    pts = [(x, y) for y in range(trim, im.height - trim) for x in range(trim, im.width - trim)
           if max(abs(a - b) for a, b in zip(px[x, y], ground)) > 12]
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
    x1, y1 = max(p[0] for p in pts), max(p[1] for p in pts)
    return (max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + 1 + pad), min(im.height, y1 + 1 + pad))


def images(scratch, figs, crops):
    """Enlarged views for the plates, written beside the plate page as PNG files."""
    from PIL import Image
    imgs = {}

    def save(key, img, k, name):
        path = OUT / f"{DATE}_Identity-{name}.png"
        enlarge(img, k, path)
        imgs[key] = path.name
        imgs[key + "-w"] = img.width * k
    for key in ("T17", "14A", "14B", "T15", "12A", "12B"):
        one = Image.open(scratch / "m1" / f"em-{key}-newsprint-0@1x.png").convert("RGB")
        box = ink_box(one)
        for scale, k in ((1, 8), (2, 4)):
            im = Image.open(scratch / f"m{scale}" / f"em-{key}-newsprint-0@{scale}x.png").convert("RGB")
            im = im.crop(tuple(v * scale for v in box))
            name = {"T17": "Today-17", "T15": "Today-15"}.get(key, f"Fit-{key[-1]}-{key[:2]}")
            save(f"em-{key}-{scale}x", im, k, f"End-Mark-{name}-{scale}x-Enlarged")
    for s in (16, 24, 34, 40, 48):
        m = 16 if s < 24 else (24 if s < 48 else 48)
        for kind in ("today", "new"):
            kk = kind if m != 16 else "today"
            im = Image.open(scratch / "m1" / f"lk-{kk}-{m}-{s}@1x.png").convert("RGB")
            save(f"lk-{kind}-{s}", im, 6, f"Lockmark-{WORD[kind]}-{s}px-1x-Enlarged")
    for kind in ("today", "new"):
        im = Image.open(scratch / "m2" / f"lk-{kind}-48-48@2x.png").convert("RGB")
        save(f"lk2x-{kind}-48", im, 4, f"Lockmark-{WORD[kind]}-48px-2x-Enlarged")
    # the display master at 48 px on a 2x screen, for comparison
    im = Image.open(scratch / "disp2x" / "disp-48@2x.png").convert("RGB")
    save("lk2x-disp-96", im, 4, "Lockmark-Display-48px-2x-Enlarged")
    for key, img in crops.items():
        save(f"feed-{key}", img, 8, f"Feed-{WORD[key.split('-')[0]]}-{key.split('-')[1]}-Enlarged")
    return imgs


def main(scratch, keep):
    LIB.INLINE_ALL[0] = True
    OUT.mkdir(parents=True, exist_ok=True)
    figs = {"date": "2026-11-09", "method": QM.METHOD}
    figs["end_files"] = end_files()
    figs["lockmark_files"] = lockmark_files()
    figs["l6"] = l6_geometry()
    figs["measure"] = measure(scratch)
    figs["feed"], crops = feed(scratch)
    # the display master at 48 px on a 2x screen, for the 2x comparison
    dp = scratch / "disp.html"
    dp.write_text(page("disp", f'<div id="disp-48" style="width:48px;height:48px;line-height:0">{svg_file(ID_DIR / LOCK["display"], h=48, label="Display master", style=mark_style("newsprint"))}</div>'))
    shoot(dp, scratch / "disp2x", ["disp-48"], 2)
    figs["pixel_fit_check"] = pixel_fit_check(scratch)
    imgs = images(scratch, figs, crops)
    global L6_TODAY, L6_CENTERED
    from stage_a_identity_s03 import l6
    L6_TODAY = l6(884, dots=False, centered=False)
    L6_CENTERED = l6_centered(884, figs["l6"]["shift_down_units"])
    html_path = OUT / f"{DATE}_Identity-Plates.html"
    html_path.write_text(page("Identity drawings: plates", plates(figs, imgs)))
    names = {"card-end-mark": "End-Mark", "card-lockmark": "Lockmark-Masters", "card-l6": "L6-Centered"}
    for scale in (1, 2):
        figs[f"plate_fonts_{scale}x"] = shoot(html_path, scratch / f"plates{scale}", list(names), scale)
        for i, n in names.items():
            shutil.copy(scratch / f"plates{scale}" / f"{i}@{scale}x.png", OUT / f"{DATE}_Identity-{n}-Plate-{scale}x.png")
    # L6 alone at true size and 2x, for the board builder
    lp = scratch / "l6.html"
    lp.write_text(page("L6", f'<div id="l6-today" style="width:max-content">{L6_TODAY}</div><div id="l6-centered" style="width:max-content">{L6_CENTERED}</div>', ".bd{gap:24px}"))
    for scale in (1, 2):
        shoot(lp, scratch / f"l6{scale}", ["l6-today", "l6-centered"], scale)
        shutil.copy(scratch / f"l6{scale}" / f"l6-today@{scale}x.png", OUT / f"{DATE}_Identity-L6-Today-No-Dots-{scale}x.png")
        shutil.copy(scratch / f"l6{scale}" / f"l6-centered@{scale}x.png", OUT / f"{DATE}_Identity-L6-Centered-{scale}x.png")
    (OUT / f"{DATE}_Identity-Figures.json").write_text(json.dumps(figs, indent=1, ensure_ascii=False) + "\n")
    LIB.INLINE_ALL[0] = False
    return figs


if __name__ == "__main__":
    keep = "--keep" in sys.argv
    if "--scratch" in sys.argv:
        scratch = Path(sys.argv[sys.argv.index("--scratch") + 1])
        scratch.mkdir(parents=True, exist_ok=True)
    else:
        scratch = Path(tempfile.mkdtemp(prefix="oai-b-"))
    try:
        f = main(scratch, keep)
        print(json.dumps({k: f[k] for k in ("end_files", "lockmark_files", "l6", "feed")}, indent=1))
        print("identical at own size:", f["measure"]["identical_at_own_size"])
        print("end mark:", json.dumps(f["measure"]["end_mark"], indent=1))
        print("pixel-fit check exits:", {k: v["exit"] for k, v in f["pixel_fit_check"].items()})
    finally:
        if not keep:
            shutil.rmtree(scratch, ignore_errors=True)
    print("wrote", OUT.relative_to(ROOT))
