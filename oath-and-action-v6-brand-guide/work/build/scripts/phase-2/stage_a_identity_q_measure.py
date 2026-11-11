"""Measurements for the Q1 to Q4 pass, November 8, 2026 (DR-130, DR-131, CD-N8, CA-S1, CA-S2).

Three tests, each rendered in Chromium through stage_a_identity_shots.js, with the figures written to
work/handoffs/phase-2/20261108_Q1-To-Q4-Identity-Figures.json (one key per test, so each can run alone):

  range    The 48 px lockmark master and the display master at 48 to 144 px on Newsprint, at 1x and 2x: the share of the
           field in ink, the share near black, the lever's red pixels, the share of ink pixels drawn at full color
           (crisp), and the share of the top-left node's core and the lever's core drawn at full color (seam-free: a
           pixel master built from one rect per row parts into stripes when it is scaled between whole multiples). The
           24 px master at 34 and 40 px rides along for the record. Chooses the size where the display master takes over.
  endmark  B as an article's end mark, as Rule 04.6 now draws it (stage_a_identity_s04.end_b), beside a capital H of the
           same text at 15, 17, 19, 20 and 24 px, rendered at eight times: capitals, B's height, its top over the cap line
           and its tail under the baseline.
  feed     The feed test Rule 08.2 sets: the identity proofs' link-preview card (s-proofs-social) captured at 1x from the
           built chapters page, reduced to 500 and 360 px wide with Lanczos resampling, and the sign-off's box counted.

Renders go to a scratch folder (--scratch DIR, or a new temporary folder) and are deleted unless --keep is given. No
master, board or guide file is written.

Run: python3 work/build/scripts/phase-2/stage_a_identity_q_measure.py range|endmark|feed|all [--scratch DIR] [--keep]
The feed test reads the built chapters page, so run the identity build and guide_build.py first.
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
from stage_a_identity_lib import ROOT, ID_DIR, LOCK, svg_file, mark_style, ty, E  # noqa: E402

OUT = ROOT / "work/handoffs/phase-2/20261108_Q1-To-Q4-Identity-Figures.json"
GUIDE = ROOT / "work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html"
SHOTS = HERE / "stage_a_identity_shots.js"

NEWSPRINT, CHARCOAL, STONE, RED = (0xDC, 0xD9, 0xD2), (0x12, 0x12, 0x12), (0x5D, 0x63, 0x6D), (0xE6, 0x39, 0x46)
# The thresholds the fix pass used (work/boards/phase-2/apply-pass/lockmark/20261107_Lockmark-Weight-Figures.json).
METHOD = ("Chromium render on Newsprint; ink = channel distance from Newsprint over 45; near black = every channel under 70; "
          "red = R over 170, G and B under 120; crisp = an ink pixel within a channel distance of 40 of Charcoal, Stone or Pillar Red")


def page(body, css=""):
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<style>{tokens}</style><style>{LIB.CSS}body{{margin:0;background:var(--oa-color-surface-newsprint)}}'
            f'.cell{{position:relative;margin:0 0 8px 8px}}{css}</style></head><body><div class="oai">{body}</div></body></html>')


def shoot(html, scratch, scale, ids, name):
    p = scratch / f"{name}.html"
    p.write_text(html)
    d = scratch / f"{name}@{scale}x"
    r = subprocess.run(["node", str(SHOTS), str(p), str(d), str(scale), *ids], check=True, capture_output=True, text=True)
    return d, json.loads(r.stdout.strip().splitlines()[-1])["fonts"]


def dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def count(img):
    im = img.convert("RGB")
    px = [im.getpixel((x, y)) for y in range(im.height) for x in range(im.width)]
    n = len(px)
    inked = [p for p in px if dist(p, NEWSPRINT) > 45]
    black = sum(1 for p in px if max(p) < 70)
    red = sum(1 for p in px if p[0] > 170 and p[1] < 120 and p[2] < 120)
    crisp = sum(1 for p in inked if min(dist(p, c) for c in (CHARCOAL, STONE, RED)) <= 40)
    return {"field_px": n, "ink_share": round(len(inked) / n, 3), "near_black_share": round(black / n, 3), "red_px": red,
            "crisp_share_of_ink": round(crisp / len(inked), 3) if inked else 0.0}


def save(key, value):
    d = json.loads(OUT.read_text()) if OUT.exists() else {}
    d[key] = value
    d["method"] = METHOD
    OUT.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


# =========================================================================================== range
RANGE_SIZES = (48, 49, 50, 52, 56, 64, 72, 80, 88, 95, 96, 104, 112, 128, 144)
# node and lever centers and radii in each master's units, and its grid size: the cores the seam test reads
CORES = {"m48": (48, (4.5, 4.5, 3.5), (42.5, 42.5, 4.5)), "m24": (24, (3.5, 3.5, 2.5), (19.5, 19.5, 3.5)),
         "display": (123.5, (11.75, 11.75, 3.8), (111.75, 111.75, 4.75))}


def seam_free(img, kind, size, scale):
    """The share of a node's core and the lever's core (the inner 70 percent of the radius) drawn at full color: within
    a channel distance of 30 of Charcoal or Pillar Red. A seam between two rows renders 30 to 50 levels lighter."""
    im = img.convert("RGB")
    px = im.load()
    unit, node, lever = CORES[kind]
    out = []
    for (cx, cy, r), target in ((node, CHARCOAL), (lever, RED)):
        k = size / unit * scale
        X, Y, R = cx * k, cy * k, r * k * 0.7
        pts = [(x, y) for x in range(int(X - R) - 1, int(X + R) + 2) for y in range(int(Y - R) - 1, int(Y + R) + 2)
               if 0 <= x < im.width and 0 <= y < im.height and (x + .5 - X) ** 2 + (y + .5 - Y) ** 2 <= R * R]
        out.append(round(sum(1 for p in pts if dist(px[p], target) <= 30) / len(pts), 3) if pts else None)
    return {"node_core_full": out[0], "lever_core_full": out[1]}


def range_test(scratch):
    from PIL import Image
    LIB.INLINE_ALL[0] = True
    files = {"m48": ID_DIR / LOCK[48], "display": ID_DIR / LOCK["display"], "m24": ID_DIR / LOCK[24]}
    cells, ids = [], []
    for k, f in files.items():
        for s in (RANGE_SIZES if k != "m24" else (24, 34, 40)):
            i = f"r-{k}-{s}"
            ids.append(i)
            cells.append(f'<div class="cell" id="{i}" style="width:{s}px;height:{s}px;line-height:0">'
                         f'{svg_file(f, h=s, style=mark_style("newsprint"), decorative=True, by_ref=False)}</div>')
    LIB.INLINE_ALL[0] = False
    html = page("".join(cells))
    out = {"sizes": list(RANGE_SIZES), "at_1x": {}, "at_2x": {}}
    for scale in (1, 2):
        d, _ = shoot(html, scratch, scale, ids, "range")
        for i in ids:
            img = Image.open(d / f"{i}@{scale}x.png")
            _, k, sz = i.split("-")
            out[f"at_{scale}x"][i[2:]] = dict(count(img), **seam_free(img, k, int(sz), scale))
    out["geometry"] = {
        "m48": {str(s): {"grid_px_per_unit": round(s / 48, 3), "node_px": round(7 * s / 48, 2), "lever_px": round(9 * s / 48, 2)} for s in RANGE_SIZES},
        "display": {str(s): {"node_px": round(7.6 * s / 123.5, 2), "lever_px": round(9.5 * s / 123.5, 2), "link_px": 1} for s in RANGE_SIZES},
    }
    save("range", out)
    return out


# =========================================================================================== end mark
END_SIZES = (15, 17, 19, 20, 24)


def endmark_test(scratch):
    """Rule 04.6's end mark beside a capital H, rendered at eight times, then measured from ink rows as in the fix pass
    (stage_a_identity_fix_boards.measure_end_marks): the first ink run is H, the rest is B."""
    from PIL import Image
    import stage_a_identity_s04 as S04
    LIB.INLINE_ALL[0] = True
    cells, ids = [], []
    for f in END_SIZES:
        b = S04.end_b(f)
        i = f"e-{f}"
        ids.append(i)
        cells.append(f'<div id="{i}" style="width:max-content;padding:6px;{ty("body", size=f)};color:var(--oa-color-text-primary-on-newsprint)">'
                     f'H{b.replace("margin-left:0.5em", "margin-left:6px")}</div>')
    LIB.INLINE_ALL[0] = False
    d, fonts = shoot(page("".join(cells)), scratch, 8, ids, "endmark")
    res = {}
    for i in ids:
        im = Image.open(d / f"{i}@8x.png").convert("L")
        W, H = im.size
        px = im.load()
        dark = [[px[x, y] < 110 for x in range(W)] for y in range(H)]
        cols = [x for x in range(W) if any(dark[y][x] for y in range(H))]
        runs, start, prev = [], cols[0], cols[0]
        for x in cols[1:]:
            if x != prev + 1:
                runs.append((start, prev))
                start = x
            prev = x
        runs.append((start, prev))

        def rows(x0, x1):
            ys = [y for y in range(H) if any(dark[y][x] for x in range(x0, x1 + 1))]
            return ys[0] / 8, (ys[-1] + 1) / 8
        hT, hB = rows(*runs[0])
        bT, bB = rows(runs[1][0], runs[-1][1])
        f = int(i[2:])
        res[str(f)] = {"capitals_px": round(hB - hT, 2), "b_px": round(bB - bT, 2), "top_over_cap_line_px": round(hT - bT, 2),
                       "tail_under_baseline_px": round(bB - hB, 2), "b_over_capitals": round((bB - bT) / (hB - hT), 3)}
    save("endmark", {"text_px": list(END_SIZES), "measured_at_8x": res, "fonts_loaded": fonts,
                     "drawn_by": "stage_a_identity_s04.end_b, as s-04-6-correct places it"})
    return res


# =========================================================================================== feed
FEED_WIDTHS = (500, 360)
CARD = (1200, 630)
# Rule 08.2's pass line for a card a feed shrinks: every one of the eight dark nodes keeps a near-black pixel, and the
# lever keeps at least FEED_MIN_RED red pixels, so a reader still sees nine nodes and a red lever.
FEED_MIN_RED = 4
CENTERS48 = (4.5, 23.5, 42.5)          # the 48 px master's node centers; its nodes are 7 px across and its lever 9 px


def feed_counts(img, ox, oy, s):
    """Per node: does a near-black pixel survive inside the node's reduced square (its 7 px plus 1 px each side)? And how
    many red pixels does the lever's reduced square keep? ox, oy: the lockmark's top left in the full-size card."""
    px = img.load()
    dark = 0
    for cy in CENTERS48:
        for cx in CENTERS48:
            X, Y = (ox + cx) * s, (oy + cy) * s
            r = 3.5 * s + 1 if (cx, cy) != (CENTERS48[2], CENTERS48[2]) else 4.5 * s + 1
            pts = [(x, y) for x in range(int(X - r), int(X + r) + 1) for y in range(int(Y - r), int(Y + r) + 1)
                   if 0 <= x < img.width and 0 <= y < img.height]
            if (cx, cy) == (CENTERS48[2], CENTERS48[2]):
                red = sum(1 for q in pts if px[q][0] > 170 and px[q][1] < 120 and px[q][2] < 120)
            elif any(max(px[q]) < 70 for q in pts):
                dark += 1
    return {"dark_nodes_kept": dark, "lever_red_px": red, "passes": dark == 8 and red >= FEED_MIN_RED}


def feed_test(scratch):
    """Capture the proof's 1200 by 630 card at 1x from the built chapters page, reduce it as a feed does, and count the
    sign-off's box plus 1 px, node by node."""
    from PIL import Image
    js = scratch / "feed.js"
    shot = scratch / "card@1x.png"
    js.write_text(
        "const { chromium } = require('playwright');\n"
        "(async () => {\n"
        "  const b = await chromium.launch();\n"
        "  const p = await b.newPage({ viewport: { width: 1700, height: 1000 }, deviceScaleFactor: 1 });\n"
        f"  await p.goto('file://{GUIDE}', {{ waitUntil: 'networkidle' }});\n"
        "  await p.evaluate(() => document.fonts.ready);\n"
        "  const card = p.locator('[data-oai=\"s-proofs-social\"] .oai-stackpair > div:first-child > div').first();\n"
        "  await card.scrollIntoViewIfNeeded();\n"
        "  const box = await card.boundingBox();\n"
        "  const lk = await card.locator('svg[aria-label=\"Lockmark\"]').last().evaluate((e) => {\n"
        "    const r = e.getBoundingClientRect(); return { viewBox: e.getAttribute('viewBox'), x: r.x, y: r.y, w: r.width, h: r.height }; });\n"
        "  const clip = { x: Math.round(box.x), y: Math.round(box.y), width: 1200, height: 630 };\n"
        f"  await p.screenshot({{ path: '{shot}', clip }});\n"
        "  console.log(JSON.stringify({ box, clip, lk }));\n"
        "  await b.close();\n"
        "})();\n")
    r = subprocess.run(["node", str(js)], check=True, capture_output=True, text=True, cwd=str(ROOT / "work/build"))
    info = json.loads(r.stdout.strip().splitlines()[-1])
    card = Image.open(shot).convert("RGB")
    assert card.size == CARD, f"the card captured at {card.size}, not {CARD}"
    lk, bx = info["lk"], info["clip"]
    # since promotion C (DR-211) the card signs off at 96 px, which this count's 48 px grid cannot read;
    # promotion_c_identity.py feed measures that card
    assert round(lk["h"]) == 48, f"the card's sign-off is {lk['h']} px, not 48; run promotion_c_identity.py feed instead"
    ox, oy = lk["x"] - bx["x"], lk["y"] - bx["y"]           # the lockmark's box in the captured card, as layout places it
    vb48 = re.search(r'viewBox="([^"]+)"', (ID_DIR / LOCK[48]).read_text()).group(1)
    master = LOCK[48] if lk["viewBox"] == vb48 else f"a drawing with viewBox {lk['viewBox']}"     # the guide inlines masters
    res = {"card_px": list(card.size), "card_in_page": [round(info["box"]["x"], 3), round(info["box"]["y"], 3)], "lockmark_master": master,
           "lockmark_box_in_card": [round(ox, 3), round(oy, 3), round(lk["w"], 2), round(lk["h"], 2)], "min_red_px": FEED_MIN_RED}
    ox, oy = round(ox), round(oy)
    at1 = card.crop((ox, oy, ox + round(lk["w"]), oy + round(lk["h"])))
    res["at_1200"] = dict(count(at1), **seam_free(at1, "m48", 48, 1), **feed_counts(card, ox, oy, 1))
    for w in FEED_WIDTHS:
        s = w / CARD[0]
        small = card.resize((w, round(CARD[1] * s)), Image.LANCZOS)
        box = (int(ox * s) - 1, int(oy * s) - 1, int((ox + lk["w"]) * s + 0.999) + 1, int((oy + lk["h"]) * s + 0.999) + 1)
        crop = small.crop(box)
        res[f"at_{w}"] = dict(count(crop), **feed_counts(small, ox, oy, s), lockmark_px=round(lk["h"] * s, 1), box_px=[crop.width, crop.height])
        crop.resize((crop.width * 8, crop.height * 8), Image.NEAREST).save(scratch / f"feed-{w}@8x.png")
    res["control"] = feed_control(scratch)
    save("feed", res)
    return res


def feed_control(scratch):
    """The same card drawn standalone with each master in the sign-off, so the test is seen to fail the display master
    and pass the 48 px master. The card's 1 px border puts the lockmark at 1079, 509."""
    from PIL import Image
    import stage_a_identity_proofs as SP
    LIB.INLINE_ALL[0] = True
    keep = SP.lockmark
    cards, out = {}, {}
    try:
        for k, f in (("display", lambda s, **kw: LIB.mark(LOCK["display"], h=s, label="Lockmark")), ("m48", keep)):
            SP.lockmark = f
            cards[k] = f'<div id="card-{k}" style="width:1200px">{SP._social(sign=48)}</div>'
    finally:
        SP.lockmark = keep
        LIB.INLINE_ALL[0] = False
    d, _ = shoot(page("".join(cards.values())), scratch, 1, [f"card-{k}" for k in cards], "control")
    for k in cards:
        card = Image.open(d / f"card-{k}@1x.png").convert("RGB")
        out[k] = {}
        for w in FEED_WIDTHS:
            s = w / CARD[0]
            small = card.resize((w, round(CARD[1] * s)), Image.LANCZOS)
            out[k][f"at_{w}"] = feed_counts(small, 1079, 509, s)
    return out


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "all"
    keep = "--keep" in sys.argv
    if "--scratch" in sys.argv:
        scratch = Path(sys.argv[sys.argv.index("--scratch") + 1])
        scratch.mkdir(parents=True, exist_ok=True)
    else:
        scratch = Path(tempfile.mkdtemp(prefix="oai-q-"))
    try:
        if what in ("range", "all"):
            print("range", json.dumps(range_test(scratch)))
        if what in ("endmark", "all"):
            print("endmark", json.dumps(endmark_test(scratch)))
        if what in ("feed", "all"):
            print("feed", json.dumps(feed_test(scratch)))
    finally:
        if not keep:
            shutil.rmtree(scratch, ignore_errors=True)
    print("wrote", OUT.relative_to(ROOT))
