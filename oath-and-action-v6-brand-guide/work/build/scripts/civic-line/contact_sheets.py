"""Part A: the ten Civic Line contact sheets (five layouts x two editions).

    python3 -I contact_sheets.py

Each sheet is a 1536 x 1024 Newsprint canvas that repeats its source sheet
cell for cell: every traced icon sits at its own crop rectangle, and the
captions, reform IDs, sheet title, header rule and footer sit at the
positions measured on the source. The upper left carries the approved
Edition 06 wordmark master (DR-05), scaled to the source wordmark's cap
height, with its ampersand in Pillar Red (red-black) or Charcoal (black).

Text is set in Inter from work/extract/v5-polished/fonts (OFL 1.1, no
Reserved Font Name; rights ledger font-01 to font-03), shaped by Chromium
with kerning and converted to outlines with fontTools. The SVGs therefore
carry no font data and render the same everywhere.

Writes contact-sheets/<date>_Oath-And-Action-Civic-Line-<NN>-<Slug>-<Edition>.svg,
.png (1x) and -2x.png, the side-by-side checks in qa/sheet-compare/, and
qa/sheet-compare/<date>_Contact-Sheet-Layout.json with every measured
position and fitted size.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site  # noqa: E402
_USER_SITE = site.getusersitepackages()   # fontTools is installed per user; -I leaves this path out
if os.path.isdir(_USER_SITE) and _USER_SITE not in sys.path:
    sys.path.append(_USER_SITE)
import cl_common as C  # noqa: E402
import crop_references as R  # noqa: E402
from fontTools.pens.svgPathPen import SVGPathPen  # noqa: E402
from fontTools.pens.transformPen import TransformPen  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402

OUT = os.path.join(C.ASSETS, "contact-sheets")
CMP = os.path.join(C.QA, "sheet-compare")
FONT_DIR = os.path.join(C.ROOT, "work", "extract", "v5-polished", "fonts")
FONTS = {"Inter-400": os.path.join(FONT_DIR, "Inter-400-normal.ttf"),
         "Inter-600": os.path.join(FONT_DIR, "Inter-600-normal.ttf"),
         "Inter-700": os.path.join(FONT_DIR, "Inter-700-normal.ttf")}
WORDMARK = os.path.join(C.ROOT, "work", "build", "assets", "identity", "wordmark", "20261028_Wordmark-Display-Master.svg")
WM_CAP_TOP, WM_BASELINE = 4.0, 104.0          # from the master's title: cap line y 4, baseline y 104
SHEET_SLUG = {"01": "Participation", "02": "Government-Tech", "03": "Economy-Issues",
              "04": "Reforms-01-25", "05": "Reforms-26-50"}
# Title text and weight runs as drawn on each source sheet.
TITLES = {
    "01": [("Inter-400", "01 / Participation & Accountability")],
    "02": [("Inter-700", "02"), ("Inter-400", " / Government, Information & Technology")],
    "03": [("Inter-600", "03 / Economy & Public Issues")],
    "04": [("Inter-700", "04 / Reforms R-01–R-25")],
    "05": [("Inter-400", "05 / "), ("Inter-700", "Reforms"), ("Inter-400", " R-26–R-50")],
}
# Dark editions sit on Newsprint and are compared with their source sheet; the
# light editions (DR-09) sit on Charcoal and have no source sheet to compare.
EDITIONS = {"red-black": {"label": "Red-Black", "accent": C.PILLAR_RED, "src": "red", "ground": C.NEWSPRINT, "ink": C.CHARCOAL},
            "black": {"label": "Black", "accent": C.CHARCOAL, "src": "black", "ground": C.NEWSPRINT, "ink": C.CHARCOAL},
            "red-newsprint": {"label": "Red-Newsprint", "accent": C.PILLAR_RED, "src": None, "ground": C.CHARCOAL, "ink": C.NEWSPRINT},
            "newsprint": {"label": "Newsprint", "accent": C.NEWSPRINT, "src": None, "ground": C.CHARCOAL, "ink": C.NEWSPRINT}}
RULE_T = 1.2   # rule thickness in px: median of the five source rules (1.02 to 1.5)


def n2(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ------------------------------------------------------------------ source measurements

def measure_sheet(key):
    """Positions of every text element and the rule on the black source sheet."""
    A = R.analyse_sheet(key)
    sh = A["sheet"]
    boxes = A["boxes"]
    rule_y = A["rule_y"]
    g = C.green(sh.rgb)
    bg = float(np.median(g[rule_y + 10:rule_y + 25, 600:900]))
    cov = np.clip((bg - g[rule_y - 10:rule_y + 10, 300:1200]) / (bg - sh.full_ink_g), 0, 1).mean(1)
    rule_cy = rule_y - 10 + float((np.arange(20) * cov).sum() / cov.sum()) + 0.5
    row_ink = np.nonzero(sh.ink[rule_y])[0]
    above = [b for b in boxes if b["y1"] <= rule_y - 2]
    wm = sorted([b for b in above if b["x0"] < 500], key=lambda b: b["x0"])
    title = [b for b in above if b["x0"] >= 700]
    last_cap = max(c["cap_y1"] for c in A["rows"][-1]["cells"])
    footer = [b for b in boxes if b["y0"] > last_cap + 4]

    def line(bs):
        return {"x0": min(b["x0"] for b in bs), "x1": max(b["x1"] for b in bs),
                "baseline": float(np.median([b["y1"] for b in bs]))}
    # wordmark: cap height from the H (fourth letter) and the I (ninth)
    h_box, i_box = wm[3], wm[8]
    cap_top = (h_box["y0"] + i_box["y0"]) / 2.0
    baseline = (h_box["y1"] + i_box["y1"]) / 2.0
    cells = []
    for r, row in enumerate(A["rows"]):
        for c, cell in enumerate(row["cells"]):
            e = {"row": r + 1, "column": c + 1,
                 "cap": {"x0": cell["cap_x0"], "x1": cell["cap_x1"],
                         "baseline": float(np.median([b[3] for b in cell["cap_glyph_boxes"]]))}}
            if cell.get("id_glyph_boxes"):
                e["id"] = {"x0": cell["id_x0"], "x1": cell["id_x1"],
                           "baseline": float(np.median([b[3] for b in cell["id_glyph_boxes"]]))}
            cells.append(e)
    return {"rule": {"x0": int(row_ink.min()), "x1": int(row_ink.max()) + 1, "cy": round(rule_cy, 2)},
            "wordmark": {"x0": wm[0]["x0"], "x1": wm[-1]["x1"], "cap_top": cap_top, "baseline": baseline},
            "title": line(title), "footer": line(footer), "cells": cells}


# ------------------------------------------------------------------ text

class Fonts:
    def __init__(self):
        self.f = {}
        for fam, p in FONTS.items():
            t = TTFont(p)
            self.f[fam] = {"gs": t.getGlyphSet(), "cmap": t.getBestCmap(), "upm": t["head"].unitsPerEm,
                           "glyf": t["glyf"] if "glyf" in t else None, "font": t}

    def bounds(self, fam, ch):
        F = self.f[fam]
        name = F["cmap"].get(ord(ch))
        if name is None:
            raise SystemExit(f"{fam} has no glyph for {ch!r}")
        gl = F["glyf"][name]
        if not hasattr(gl, "xMin") or gl.numberOfContours == 0:
            return None
        return gl.xMin, gl.xMax, F["upm"]

    def path(self, fam, ch, x, baseline, size):
        F = self.f[fam]
        name = F["cmap"][ord(ch)]
        k = size / F["upm"]
        pen = SVGPathPen(F["gs"], ntos=n2)
        F["gs"][name].draw(TransformPen(pen, (k, 0, 0, -k, x, baseline)))
        return pen.getCommands()


def shape(lines):
    """lines: [{id, size, runs:[{family,text}]}] -> {id: {chars, advance}} via Chromium."""
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "in.json"), os.path.join(d, "out.json")
        with open(a, "w") as fh:
            json.dump({"fonts": FONTS, "lines": lines}, fh)
        r = subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "shape_text.js"), a, b],
                           capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("shape_text.js failed:\n" + r.stderr[-2000:])
        res = json.load(open(b))
    bad = [f for f in res["fonts"] if not f.endswith(":loaded")]
    if bad:
        raise SystemExit(f"fonts did not load in Chromium: {bad}")
    return res["lines"]


def ink_extent(fonts, chars, size, shaped_size=100.0):
    k = size / shaped_size
    xs0, xs1 = [], []
    for c in chars:
        b = fonts.bounds(c["family"], c["ch"])
        if b is None:
            continue
        x0, x1, upm = b
        xs0.append(c["x"] * k + x0 * size / upm)
        xs1.append(c["x"] * k + x1 * size / upm)
    return min(xs0), max(xs1)


def text_path(fonts, chars, size, dx, baseline, shaped_size=100.0):
    k = size / shaped_size
    parts = []
    for c in chars:
        if c["ch"] == " ":
            continue
        parts.append(fonts.path(c["family"], c["ch"], dx + c["x"] * k, baseline, size))
    return "".join(parts)


# ------------------------------------------------------------------ sheet assembly

def wordmark_group(meas, accent, ink=C.CHARCOAL):
    s = open(WORDMARK, encoding="utf-8").read()
    paths = re.findall(r"<path\b[^>]*/>", s)
    k = (meas["baseline"] - meas["cap_top"]) / (WM_BASELINE - WM_CAP_TOP)
    out = []
    for p in paths:
        p = p.replace('fill="currentColor"', f'fill="{ink}"')
        p = re.sub(r'fill="var\(--amp,[^)]*\)"', f'fill="{accent}"', p)
        out.append("    " + p)
    tx = meas["x0"]
    ty = meas["baseline"] - WM_BASELINE * k
    width = 978.31 * k
    return (f'  <g id="wordmark" transform="translate({n2(tx)} {n2(ty)}) scale({k:.6f})">\n' + "\n".join(out) + "\n  </g>"), k, width


def icon_block(row, edition):
    p = C.edition_file(row, edition)
    if not os.path.exists(p):
        return None
    s = open(p, encoding="utf-8").read()
    s = s.split("?>", 1)[-1].strip()
    s = re.sub(r"\s*<title>.*?</title>", "", s, flags=re.S)
    s = re.sub(r"\s*<desc>.*?</desc>", "", s, flags=re.S)
    t = row["transform"]
    sc = t["s"]
    c = row["crop"]
    vb = f"{64 - sc * t['cx']:.4f} {64 - sc * t['cy']:.4f} {c['w'] * sc:.4f} {c['h'] * sc:.4f}"
    s = s.replace('width="128" height="128" viewBox="0 0 128 128"',
                  f'x="{c["x0"]}" y="{c["y0"]}" width="{c["w"]}" height="{c["h"]}" viewBox="{vb}" overflow="visible"', 1)
    pre = row["id"].lower()
    s = re.sub(r'<g id="(base|accent)((?:-\d+)?)"', lambda m: f'<g id="{pre}-{m.group(1)}{m.group(2)}"', s)
    s = s.replace('xmlns="http://www.w3.org/2000/svg" ', "", 1)
    return "  " + s.replace("\n", "\n  ")


def build():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CMP, exist_ok=True)
    inv = C.load_inventory()
    by_sheet = {k: [r for r in inv["icons"] if r["sheet"] == k] for k in C.SHEETS}
    fonts = Fonts()
    layout = {"date": C.DATE, "fonts": {k: os.path.relpath(v, C.ROOT) for k, v in FONTS.items()},
              "text": "Inter outlines (fontTools), shaped in Chromium with kerning, contextual alternates off", "sheets": {}}
    # shape every line once at 100 px
    lines = []
    meas = {}
    for key in C.SHEETS:
        m = meas[key] = measure_sheet(key)
        lines.append({"id": f"{key}-title", "size": 100, "runs": [{"family": f, "text": t} for f, t in TITLES[key]]})
        for ed in EDITIONS.values():
            lines.append({"id": f"{key}-footer-{ed['label']}", "size": 100,
                          "runs": [{"family": "Inter-400", "text": f"Oath & Action / Civic Line / {ed['label']}"}]})
        for r in by_sheet[key]:
            lines.append({"id": f"{r['id']}-cap", "size": 100, "runs": [{"family": "Inter-400", "text": r["label"]}]})
            if C.SHEETS[key]["reform"]:
                lines.append({"id": f"{r['id']}-id", "size": 100, "runs": [{"family": "Inter-400", "text": r["id"]}]})
    shaped = shape(lines)

    def fit(lid, x0, x1):
        a, b = ink_extent(fonts, shaped[lid]["chars"], 100.0)
        return 100.0 * (x1 - x0) / (b - a)
    pending = []
    for key in C.SHEETS:
        m = meas[key]
        rows = by_sheet[key]
        cells = {(c["row"], c["column"]): c for c in m["cells"]}
        cap_sizes = [fit(f"{r['id']}-cap", cells[(r['row'], r['column'])]["cap"]["x0"], cells[(r['row'], r['column'])]["cap"]["x1"]) for r in rows]
        cap_size = float(np.median(cap_sizes))
        id_size = None
        if C.SHEETS[key]["reform"]:
            id_size = float(np.median([fit(f"{r['id']}-id", cells[(r['row'], r['column'])]["id"]["x0"],
                                           cells[(r['row'], r['column'])]["id"]["x1"]) for r in rows]))
        title_size = fit(f"{key}-title", m["title"]["x0"], m["title"]["x1"])
        footer_sizes = {}
        lay = {"measured": m, "caption_size_px": round(cap_size, 3), "caption_size_spread": [round(min(cap_sizes), 2), round(max(cap_sizes), 2)],
               "id_size_px": round(id_size, 3) if id_size else None, "title_size_px": round(title_size, 3), "editions": {}}
        for ed_key, ed in EDITIONS.items():
            fid = f"{key}-footer-{ed['label']}"
            # the footer face is fitted on the black sheet's footer; both editions share that size
            footer_sizes[ed_key] = fit(f"{key}-footer-Black", m["footer"]["x0"], m["footer"]["x1"])
            fsz = footer_sizes[ed_key]
            parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024" '
                     f'id="oa-civic-line-sheet-{key}-{ed_key}">',
                     f"  <title>Oath &amp; Action Civic Line, sheet {key}, {ed['label']} edition</title>",
                     f"  <desc>Contact sheet rebuilt from the traced Civic Line masters at the source sheet's layout. "
                     f"Text is Inter converted to outlines. The wordmark is the Edition 06 display master (DR-05).</desc>",
                     f'  <rect id="ground" x="0" y="0" width="1536" height="1024" fill="{ed["ground"]}"/>']
            wm, k, wmw = wordmark_group(m["wordmark"], ed["accent"], ed["ink"])
            parts.append(wm)
            ru = m["rule"]
            parts.append(f'  <rect id="rule" x="{ru["x0"]}" y="{n2(ru["cy"] - RULE_T / 2)}" width="{ru["x1"] - ru["x0"]}" '
                         f'height="{n2(RULE_T)}" fill="{ed["ink"]}"/>')
            a, b = ink_extent(fonts, shaped[f"{key}-title"]["chars"], title_size)
            dx = m["title"]["x1"] - b
            parts.append(f'  <path id="title" fill="{ed["ink"]}" d="{text_path(fonts, shaped[f"{key}-title"]["chars"], title_size, dx, m["title"]["baseline"])}"/>')
            a, b = ink_extent(fonts, shaped[fid]["chars"], fsz)
            dx = m["footer"]["x1"] - b
            parts.append(f'  <path id="footer" fill="{ed["ink"]}" d="{text_path(fonts, shaped[fid]["chars"], fsz, dx, m["footer"]["baseline"])}"/>')
            missing = []
            for r in rows:
                cm = cells[(r["row"], r["column"])]
                blk = icon_block(r, ed_key)
                if blk is None:
                    missing.append(r["id"])
                else:
                    parts.append(blk)
                ch = shaped[f"{r['id']}-cap"]["chars"]
                a, b = ink_extent(fonts, ch, cap_size)
                dx = (cm["cap"]["x0"] + cm["cap"]["x1"]) / 2.0 - (a + b) / 2.0
                parts.append(f'  <path id="caption-{r["id"].lower()}" fill="{ed["ink"]}" d="{text_path(fonts, ch, cap_size, dx, cm["cap"]["baseline"])}"/>')
                if id_size:
                    ch = shaped[f"{r['id']}-id"]["chars"]
                    a, b = ink_extent(fonts, ch, id_size)
                    dx = (cm["id"]["x0"] + cm["id"]["x1"]) / 2.0 - (a + b) / 2.0
                    parts.append(f'  <path id="id-{r["id"].lower()}" fill="{ed["ink"]}" d="{text_path(fonts, ch, id_size, dx, cm["id"]["baseline"])}"/>')
            parts.append("</svg>")
            svg = "\n".join(parts) + "\n"
            name = f"{C.DATE}_Oath-And-Action-Civic-Line-{key}-{SHEET_SLUG[key]}-{ed['label']}"
            with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as fh:
                fh.write(svg)
            pending.append((key, ed_key, name, svg))
            lay["editions"][ed_key] = {"file": name + ".svg", "footer_size_px": round(fsz, 3), "missing_icons": missing,
                                       "wordmark_scale": round(k, 6), "wordmark_width_px": round(wmw, 2),
                                       "source_wordmark_width_px": m["wordmark"]["x1"] - m["wordmark"]["x0"]}
        layout["sheets"][key] = lay
    # render 1x and 2x PNGs in one Chromium run
    jobs = []
    for key, ed_key, name, svg in pending:
        jobs.append({"svg": svg, "w": 1536, "h": 1024, "bg": None, "out": os.path.join(OUT, name + ".png")})
        jobs.append({"svg": svg.replace('width="1536" height="1024"', 'width="3072" height="2048"', 1), "w": 3072, "h": 2048,
                     "bg": None, "out": os.path.join(OUT, name + "-2x.png")})
    with tempfile.TemporaryDirectory() as d:
        jp = os.path.join(d, "jobs.json")
        json.dump(jobs, open(jp, "w"))
        r = subprocess.run(["node", C.RENDER_JS, jp], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("render failed:\n" + r.stderr[-2000:])
    # PNG files carry no alpha: the Newsprint canvas fills them
    for key, ed_key, name, svg in pending:
        for suf in ("", "-2x"):
            p = os.path.join(OUT, name + suf + ".png")
            Image.open(p).convert("RGB").save(p, optimize=True)
        if EDITIONS[ed_key]["src"]:
            compare(key, ed_key, name)
    C.write_json(os.path.join(CMP, f"{C.DATE}_Contact-Sheet-Layout.json"), layout)
    for key, lay in layout["sheets"].items():
        e = lay["editions"]["red-black"]
        print(f"sheet {key}: caption {lay['caption_size_px']:.2f} px (fits {lay['caption_size_spread']}), ID {lay['id_size_px']}, "
              f"title {lay['title_size_px']:.2f} px, footer {e['footer_size_px']:.2f} px, wordmark x{e['wordmark_scale']:.4f} "
              f"= {e['wordmark_width_px']:.0f} px wide (source {e['source_wordmark_width_px']} px); missing {e['missing_icons'] or 'none'}")


def compare(key, ed_key, name):
    src = Image.open(os.path.join(C.REF_DIR, C.SHEETS[key][EDITIONS[ed_key]["src"]])).convert("RGB")
    reb = Image.open(os.path.join(OUT, name + ".png")).convert("RGB")
    gap, top = 24, 40
    out = Image.new("RGB", (src.width * 2 + gap * 3, src.height + top + gap), (255, 255, 255))
    d = ImageDraw.Draw(out)
    f = C.font(20, True)
    d.text((gap, 10), f"Source sheet {key}, {EDITIONS[ed_key]['label']} (supplied raster)", fill=(0, 0, 0), font=f)
    d.text((gap * 2 + src.width, 10), f"Rebuilt sheet {key}, {EDITIONS[ed_key]['label']} (traced masters, Edition 06 wordmark)",
           fill=(0, 0, 0), font=f)
    out.paste(src, (gap, top))
    out.paste(reb, (gap * 2 + src.width, top))
    out.save(os.path.join(CMP, f"{C.DATE}_Sheet-{key}-{EDITIONS[ed_key]['label']}-Compare.png"), optimize=True)


if __name__ == "__main__":
    build()
