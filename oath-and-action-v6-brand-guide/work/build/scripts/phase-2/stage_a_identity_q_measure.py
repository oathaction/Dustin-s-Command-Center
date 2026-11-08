"""Measurements for the Q1 to Q4 pass, November 8, 2026 (DR-130, DR-131, CD-N8, CA-S1, CA-S2).

Three tests, each rendered in Chromium through stage_a_identity_shots.js, with the figures written to
work/handoffs/phase-2/20261108_Q1-To-Q4-Identity-Figures.json (one key per test, so each can run alone):

  range    The 48 px lockmark master and the display master at 48 to 144 px on Newsprint, at 1x and 2x: the share of the
           field in ink, the share near black, the lever's red pixels, and the share of ink pixels drawn at full color
           (crisp). Chooses the size where the display master takes over from the 48 px master.
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
    px = list(im.getdata())
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
RANGE_SIZES = (48, 56, 64, 72, 80, 88, 95, 96, 104, 112, 128, 144)


def range_test(scratch):
    from PIL import Image
    LIB.INLINE_ALL[0] = True
    files = {"m48": ID_DIR / LOCK[48], "display": ID_DIR / LOCK["display"]}
    cells, ids = [], []
    for k, f in files.items():
        for s in RANGE_SIZES:
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
            out[f"at_{scale}x"][i[2:]] = count(Image.open(d / f"{i}@{scale}x.png"))
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
SIGN = {"size": 48, "margin": 72}           # Rule 08.2's sign-off on a card: 48 px, 72 px in from the right and bottom


def feed_test(scratch):
    """Capture the proof's 1200 by 630 card at 1x from the built chapters page, reduce it as a feed does and count the
    sign-off's box plus 1 px."""
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
        "  const lk = await card.locator('[data-master*=\"lockmark/\"], img[src*=\"lockmark/\"], svg').last().evaluate((e) => {\n"
        "    const r = e.getBoundingClientRect(); return { master: e.getAttribute('data-master') || e.getAttribute('src'), w: r.width, h: r.height }; });\n"
        f"  await card.screenshot({{ path: '{shot}' }});\n"
        "  console.log(JSON.stringify({ box, lk }));\n"
        "  await b.close();\n"
        "})();\n")
    r = subprocess.run(["node", str(js)], check=True, capture_output=True, text=True, cwd=str(ROOT / "work/build"))
    info = json.loads(r.stdout.strip().splitlines()[-1])
    card = Image.open(shot).convert("RGB")
    assert card.size == CARD, f"the card captured at {card.size}, not {CARD}"
    res = {"card_px": list(card.size), "lockmark_master": info["lk"]["master"], "lockmark_drawn_px": [round(info["lk"]["w"], 2), round(info["lk"]["h"], 2)]}
    full = card.crop((CARD[0] - SIGN["margin"] - SIGN["size"], CARD[1] - SIGN["margin"] - SIGN["size"],
                      CARD[0] - SIGN["margin"], CARD[1] - SIGN["margin"]))
    res["at_1200"] = count(full)
    for w in FEED_WIDTHS:
        s = w / CARD[0]
        small = card.resize((w, round(CARD[1] * s)), Image.LANCZOS)
        box = (round((CARD[0] - SIGN["margin"] - SIGN["size"]) * s) - 1, round((CARD[1] - SIGN["margin"] - SIGN["size"]) * s) - 1,
               round((CARD[0] - SIGN["margin"]) * s) + 1, round((CARD[1] - SIGN["margin"]) * s) + 1)
        crop = small.crop(box)
        res[f"at_{w}"] = dict(count(crop), lockmark_px=round(SIGN["size"] * s, 1), box_px=[crop.width, crop.height])
        crop.resize((crop.width * 8, crop.height * 8), Image.NEAREST).save(scratch / f"feed-{w}@8x.png")
    save("feed", res)
    return res


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
