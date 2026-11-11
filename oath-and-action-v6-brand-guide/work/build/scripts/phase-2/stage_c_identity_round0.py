"""Stage C, round 0, November 10, 2026: the identity designer's measurements and proposals for chapter 08's open items
(D2-715) and the check of chapter 09's opener figure (D2-965, D2-1134).

Under work/handoffs/phase-2/20261110_Stage-C-Brief.md, "Round 0 tasks, Identity designer". Figures go to
work/handoffs/phase-2/20261110_Stage-C-Identity-Figures.json, one key per step, so each step can run alone.

  feed DIR     Rule 08.2's feed test (D2-468) on the proofs' link-preview card drawn on Newsprint, White, Charcoal and
               Prussian (stage_a_identity_proofs._social), captured at 1x in Chromium, and the margin studies the
               creative director's "feed margin" note asks for:
                 dark      the light-node version of the test for a dark card (CD-N12): each node keeps a pixel whose every
                           channel clears a floor, measured from the links alone so a link can never pass for a node;
                 filters   Lanczos, bicubic, bilinear and box reductions, and Chromium's own downscale of the card as an
                           <img>, the way a browser draws a feed at 1x;
                 jpeg      the card saved as a JPEG before and after the reduction, at four qualities, with and without
                           chroma subsampling (the color detail a JPEG keeps at half size);
                 widths    every width from 300 to 600 px, so 500 and 360 px are seen against their neighbors;
                 place     every whole-pixel position of the lockmark inside a 60 px square at the card's corner, which
                           holds every phase 500 and 360 px give, to see whether placement alone can widen the margin.
               Writes key "feed".
  proposals    Writes the drawings for board C beside the masters (new files only): the print L3 at the masthead's
               proportion, from the display masters, and its White file. No master is edited. Writes key "proposals".
  plates DIR   Renders the side-by-side comparisons for board C at actual size into work/handoffs/phase-2/stage-c-identity/.
  opener DIR   Measures s-09-opener in the built guide page (run the chain and guide_build.py first) at 1440,
               1024 and 768 px at 1x and 390, 360 and 1440 px at 2x, with the device set to dark. Writes key "opener".
  floor DIR    The floor study alone, printed. feed-dark-key rewrites key "feed_dark" from a saved "feed".

Run: python3 -I work/build/scripts/phase-2/stage_c_identity_round0.py feed DIR | proposals | plates DIR | opener DIR
"""
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage_a_identity_lib as LIB  # noqa: E402
from stage_a_identity_lib import ROOT, ID_DIR, LOCK  # noqa: E402

FIGS = ROOT / "work/handoffs/phase-2/20261110_Stage-C-Identity-Figures.json"
PLATES = ROOT / "work/handoffs/phase-2/stage-c-identity"
CARD = (1200, 630)
LK = (1079, 509)                     # the lockmark's box in the card: 1 px border, 72 px margin, 48 px mark
CENTERS48 = (4.5, 23.5, 42.5)        # the 48 px master's node centers; 7 px nodes, a 9 px lever
FEED_WIDTHS = (500, 360)
MIN_RED = 4                          # Rule 08.2: the lever keeps at least four red pixels
DARK_MAX = 70                        # Rule 08.2: a near-black pixel has every channel under 70
GROUNDS = {"newsprint": (0xDC, 0xD9, 0xD2), "white": (0xFF, 0xFF, 0xFF), "charcoal": (0x12, 0x12, 0x12),
           "prussian": (0x1F, 0x2D, 0x5A)}
LIGHT_GROUNDS = ("newsprint", "white")
NODE_INK = {"charcoal": (0xDC, 0xD9, 0xD2), "prussian": (0xFF, 0xFF, 0xFF)}   # Newsprint nodes on Charcoal, White on Prussian


def save(key, value):
    d = json.loads(FIGS.read_text()) if FIGS.exists() else {}
    d[key] = value
    d["date"] = "2026-11-10"
    FIGS.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


def page(body, css=""):
    import stage_a_identity_q_measure as QM
    return QM.page(body, css)


def node_js(js, *args):
    p = Path(args[0]).parent / "run.js" if args else None
    p.write_text(js)
    r = subprocess.run(["node", str(p), *map(str, args)], check=True, capture_output=True, text=True, cwd=str(ROOT / "work/build"))
    return json.loads(r.stdout.strip().splitlines()[-1])


SHOT_JS = r"""
const { chromium } = require('playwright');
const [out, html, ...ids] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 1 });
  await p.goto('file://' + html, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  const boxes = {};
  for (const id of ids) {
    const el = p.locator('#' + id);
    await el.scrollIntoViewIfNeeded();
    boxes[id] = await el.boundingBox();
    await el.screenshot({ path: out + '/' + id + '.png' });
  }
  console.log(JSON.stringify(boxes));
  await b.close();
})();
"""

# a feed in a browser at 1x: the card as an <img> drawn at a width, captured as the screen shows it
IMG_JS = r"""
const fs = require('fs');
const { chromium } = require('playwright');
const [out, job] = process.argv.slice(2);
const items = JSON.parse(fs.readFileSync(job, 'utf8'));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 700, height: 400 }, deviceScaleFactor: 1 });
  const html = out + '/img-page.html';
  let n = 0;
  for (const it of items) {
    fs.writeFileSync(html, `<!doctype html><html><body style="margin:0;background:#888"><img id="i" src="file://${it.src}" width="${it.w}" style="display:block"></body></html>`);
    await p.goto('file://' + html, { waitUntil: 'load' });
    const ok = await p.evaluate(() => { const i = document.getElementById('i'); return i.complete && i.naturalWidth > 0; });
    if (!ok) throw new Error('image did not load: ' + it.src);
    await p.locator('#i').screenshot({ path: it.out });
    n++;
  }
  console.log(JSON.stringify({ n }));
  await b.close();
})();
"""


# =========================================================================================== counting
def node_boxes(ox, oy, s, w, h):
    """Each node's square in a card reduced by s: the node's 7 px (the lever's 9 px) plus 1 px on every side, as
    Rule 08.2 counts it (stage_a_identity_q_measure.feed_counts)."""
    out = []
    for cy in CENTERS48:
        for cx in CENTERS48:
            lever = (cx, cy) == (CENTERS48[2], CENTERS48[2])
            X, Y = (ox + cx) * s, (oy + cy) * s
            r = (4.5 if lever else 3.5) * s + 1
            pts = [(x, y) for x in range(int(X - r), int(X + r) + 1) for y in range(int(Y - r), int(Y + r) + 1)
                   if 0 <= x < w and 0 <= y < h]
            out.append((lever, pts))
    return out


def is_red(p):
    return p[0] > 170 and p[1] < 120 and p[2] < 120


def counts(arr, ox, oy, s, ground, floor=None):
    """Rule 08.2's counts on a reduced card (a numpy array, H x W x 3).

    Light ground: each of the eight dark nodes keeps a pixel with every channel under 70; the lever keeps red pixels.
    Dark ground: each light node keeps a pixel with every channel over the floor; on Charcoal the lever counts red
    pixels as on a light ground, and on Prussian, where the lever is White, it is the ninth light node.
    best: per node, the darkest pixel's highest channel (light ground) or the brightest pixel's lowest channel (dark
    ground), so a margin can be read against the threshold."""
    h, w = arr.shape[:2]
    kept, best, red = 0, [], 0
    for lever, pts in node_boxes(ox, oy, s, w, h):
        px = [tuple(int(c) for c in arr[y, x]) for x, y in pts]
        if lever and ground != "prussian":
            red = sum(1 for p in px if is_red(p))
            continue
        if ground in LIGHT_GROUNDS:
            b = min(max(p) for p in px)
            best.append(b)
            kept += b < DARK_MAX
        else:
            b = max(min(p) for p in px)
            best.append(b)
            kept += floor is not None and b > floor
    need = 8 if ground != "prussian" else 9
    out = {"nodes_kept": kept, "of": need, "best_per_node": best}
    if ground != "prussian":
        out["lever_red_px"] = red
    if ground in LIGHT_GROUNDS or floor is not None:
        out["passes"] = kept == need and (ground == "prussian" or red >= MIN_RED)
    return out


def reduce(img, w, flt):
    from PIL import Image
    return img.resize((w, round(CARD[1] * w / CARD[0])), flt)


def jpeg(img, q, sub):
    from PIL import Image
    b = io.BytesIO()
    img.save(b, format="JPEG", quality=q, subsampling=sub)
    b.seek(0)
    return Image.open(b).convert("RGB")


# =========================================================================================== feed
def feed(scratch):
    import numpy as np
    from PIL import Image
    import stage_a_identity_proofs as SP
    scratch = Path(scratch).resolve()
    d = scratch / "feed"
    d.mkdir(parents=True, exist_ok=True)
    LIB.INLINE_ALL[0] = True
    try:
        cards = {s: f'<div id="card-{s}" style="width:1200px">{SP._social(s, sign=48)}</div>' for s in GROUNDS}
        # the 48 px master alone on each ground, whole and with its links only, for the floor (no node, no lever)
        tiles = {}
        for s in GROUNDS:
            m = LIB.lockmark(48, surface=s, label="Lockmark")
            links = re.sub(r'(<g fill="(?:currentColor|#FFFFFF)">)(?=<path)(.*?)</g>', "", m, count=1, flags=re.S)
            links = re.sub(r'<path fill="(?:var\(--lever[^"]*|#FFFFFF)"[^>]*/>(?=</svg>)', "", links, flags=re.S)
            assert links.count("<path") == 0, f"the links-only tile on {s} still draws a node"
            tiles[s] = m
            tiles[s + "-links"] = links
    finally:
        LIB.INLINE_ALL[0] = False
    body = "".join(cards.values()) + "".join(
        f'<div id="tile-{k}" class="oai-s-{k.split("-")[0]}" style="width:48px;height:48px;line-height:0;margin:8px">{v}</div>'
        for k, v in tiles.items())
    html = d / "cards.html"
    html.write_text(page(body))
    ids = [f"card-{s}" for s in GROUNDS] + [f"tile-{k}" for k in tiles]
    js = d / "shot.js"
    js.write_text(SHOT_JS)
    r = subprocess.run(["node", str(js), str(d), str(html), *ids], check=True, capture_output=True, text=True, cwd=str(ROOT / "work/build"))
    boxes = json.loads(r.stdout.strip().splitlines()[-1])
    res = {"method": ("The proofs' link-preview card (stage_a_identity_proofs._social) drawn on each ground with every master "
                      "inlined, captured at 1x in Chromium through Playwright; reduced with Pillow 12 or drawn by Chromium "
                      "as an <img>; counted node by node in each node's square plus 1 px, as Rule 08.2 counts it"),
           "lockmark_master": LOCK[48], "lockmark_box_in_card": list(LK), "card_px": list(CARD)}
    imgs = {s: Image.open(d / f"card-{s}.png").convert("RGB") for s in GROUNDS}
    for s, im in imgs.items():
        assert im.size == CARD, f"card on {s} captured at {im.size}"
    # the lockmark sits where the rule's counter expects it, on whole pixels, on each ground
    tile = {k: np.asarray(Image.open(d / f"tile-{k}.png").convert("RGB")) for k in tiles}
    for s in GROUNDS:
        a = np.asarray(imgs[s])[LK[1]:LK[1] + 48, LK[0]:LK[0] + 48]
        assert (a == tile[s]).all(), f"the card on {s} does not draw the lockmark tile at {LK}"
    res["lockmark_in_card_same_as_tile"] = True

    flts = {"lanczos": Image.LANCZOS, "bicubic": Image.BICUBIC, "bilinear": Image.BILINEAR, "box": Image.BOX}

    def flat_card(s, t):
        """A flat card of the ground with a tile pasted at the lockmark's place: the same pixels the card draws there,
        so studies that move the lockmark or swap its drawing need no new capture."""
        a = np.empty((CARD[1], CARD[0], 3), dtype=np.uint8)
        a[:] = GROUNDS[s]
        a[LK[1]:LK[1] + 48, LK[0]:LK[0] + 48] = t
        return a

    # ------------------------------------------------------------------ the floor for light nodes, from the links alone
    # On a dark card the links take the nodes' own ink (Newsprint on Charcoal, White on Prussian), so a link crossing a
    # node's square can leave a light pixel too. The floor sits halfway between the brightest pixel the links alone
    # leave in any node's square and the weakest node's brightest pixel, at the rule's two widths under four filters,
    # rounded down to a multiple of 5. The band from 300 to 600 px is recorded beside it.
    floor_study, floors = {}, {}
    for s in ("charcoal", "prussian"):
        links = Image.fromarray(flat_card(s, tile[s + "-links"]))
        whole = Image.fromarray(flat_card(s, tile[s]))
        row = {"at_rule_widths": {}, "band_300_to_600": {"links_alone_max": 0, "weakest_node_min": 255,
                                                          "widths_where_a_node_falls_to_the_links": []}}
        lk_r, nd_r = 0, 255
        for w in range(300, 601):
            lk = max(max(counts(np.asarray(reduce(links, w, f)), *LK, w / CARD[0], s, floor=255)["best_per_node"]) for f in flts.values())
            nd = min(min(counts(np.asarray(reduce(whole, w, f)), *LK, w / CARD[0], s, floor=0)["best_per_node"]) for f in flts.values())
            bnd = row["band_300_to_600"]
            bnd["links_alone_max"] = max(bnd["links_alone_max"], lk)
            bnd["weakest_node_min"] = min(bnd["weakest_node_min"], nd)
            if nd <= lk:
                bnd["widths_where_a_node_falls_to_the_links"].append(w)
            if w in FEED_WIDTHS:
                row["at_rule_widths"][str(w)] = {"links_alone_max": lk, "weakest_node_min": nd}
                lk_r, nd_r = max(lk_r, lk), min(nd_r, nd)
        floors[s] = int((lk_r + nd_r) / 2 // 5 * 5)
        row["floor"] = floors[s]
        row["floor_share_of_the_way_from_ground_to_node"] = round((floors[s] - min(GROUNDS[s])) / (min(NODE_INK[s]) - min(GROUNDS[s])), 3)
        floor_study[s] = row
    # the same check for the light test's 70: the links alone never leave a pixel under it on a light ground
    for s in LIGHT_GROUNDS:
        links = Image.fromarray(flat_card(s, tile[s + "-links"]))
        low = 255
        for w in range(300, 601):
            for name, f in flts.items():
                arr = np.asarray(reduce(links, w, f))
                low = min(low, min(counts(arr, *LK, w / CARD[0], s)["best_per_node"]))
        floor_study[s] = {"links_alone_darkest_high_channel_300_to_600": low, "under_70": low < DARK_MAX}
    res["floor_study"] = floor_study
    res["light_floor"] = floors
    return res, imgs, tile, flts, flat_card, d


def feed_run(scratch):
    import numpy as np
    from PIL import Image
    res, imgs, tile, flts, flat_card, d = feed(scratch)
    floors = res["light_floor"]

    def counts_(arr, ox, oy, s_, ground):
        return counts(arr, ox, oy, s_, ground, floor=floors.get(ground))

    out = {}
    # ------------------------------------------------------------------ the rule's widths on the captured cards
    for s, im in imgs.items():
        out[s] = {}
        for w in FEED_WIDTHS:
            for name, f in flts.items():
                arr = np.asarray(reduce(im, w, f))
                out[s].setdefault(f"at_{w}", {})[name] = counts_(arr, *LK, w / CARD[0], s)
            sm = reduce(im, w, Image.LANCZOS)
            sc = w / CARD[0]
            box = (int(LK[0] * sc) - 1, int(LK[1] * sc) - 1, int((LK[0] + 48) * sc + 0.999) + 1, int((LK[1] + 48) * sc + 0.999) + 1)
            sm.crop(box).resize(((box[2] - box[0]) * 8, (box[3] - box[1]) * 8), Image.NEAREST).save(d / f"feed-{s}-{w}@8x.png")
    res["at_rule_widths"] = out

    # ------------------------------------------------------------------ Chromium's own downscale of the card as an <img>
    job, items = d / "img-job.json", []
    for s in GROUNDS:
        for w in FEED_WIDTHS:
            items.append({"src": str(d / f"card-{s}.png"), "w": w, "out": str(d / f"img-{s}-{w}.png")})
    for q, sub in ((80, 2),):
        for s in GROUNDS:
            p = d / f"card-{s}-q{q}-s{sub}.jpg"
            imgs[s].save(p, format="JPEG", quality=q, subsampling=sub)
            for w in FEED_WIDTHS:
                items.append({"src": str(p), "w": w, "out": str(d / f"img-{s}-q{q}-s{sub}-{w}.png")})
    job.write_text(json.dumps(items))
    js = d / "img.js"
    js.write_text(IMG_JS)
    subprocess.run(["node", str(js), str(d), str(job)], check=True, capture_output=True, text=True, cwd=str(ROOT / "work/build"))
    chrome = {}
    for it in items:
        name = Path(it["out"]).stem[4:]
        s = name.split("-")[0]
        arr = np.asarray(Image.open(it["out"]).convert("RGB"))
        chrome[name] = counts_(arr, *LK, it["w"] / CARD[0], s)
        chrome[name]["drawn_px"] = list(arr.shape[1::-1])
    res["chromium_img_downscale"] = chrome

    # ------------------------------------------------------------------ JPEG before and after the reduction
    jp = {}
    for s in GROUNDS:
        for q in (60, 75, 85, 95):
            for sub, sname in ((2, "4:2:0"), (0, "4:4:4")):
                k = f"{s} q{q} {sname}"
                big = jpeg(imgs[s], q, sub)
                for w in FEED_WIDTHS:
                    a = counts_(np.asarray(reduce(big, w, Image.LANCZOS)), *LK, w / CARD[0], s)
                    b = counts_(np.asarray(jpeg(reduce(imgs[s], w, Image.LANCZOS), q, sub)), *LK, w / CARD[0], s)
                    jp.setdefault(k, {})[f"jpeg_then_{w}"] = {x: a[x] for x in a if x != "best_per_node"}
                    jp[k][f"{w}_then_jpeg"] = {x: b[x] for x in b if x != "best_per_node"}
    res["jpeg"] = jp

    # ------------------------------------------------------------------ every width from 300 to 600 px, Lanczos
    widths = {}
    for s in GROUNDS:
        rows = []
        for w in range(300, 601):
            c = counts_(np.asarray(reduce(imgs[s], w, Image.LANCZOS)), *LK, w / CARD[0], s)
            rows.append((w, c["nodes_kept"], c.get("lever_red_px"), c.get("passes")))
        fails = [r[0] for r in rows if not r[3]]
        reds = [r[2] for r in rows if r[2] is not None]
        widths[s] = {"widths": "300 to 600", "fail_widths": fails, "fail_count": len(fails),
                     "lever_red_min": min(reds) if reds else None, "lever_red_max": max(reds) if reds else None,
                     "lever_red_by_width": {str(r[0]): r[2] for r in rows} if reds else None,
                     "nodes_min": min(r[1] for r in rows)}
        if reds:
            near = [r for r in rows if 340 <= r[0] <= 380]
            widths[s]["lever_red_340_to_380"] = {str(r[0]): r[2] for r in near}
    res["widths"] = widths

    # ------------------------------------------------------------------ placement: every phase 500 and 360 px give
    place = {}
    for s in ("newsprint", "charcoal"):
        grid = {}
        for dy in range(60):
            for dx in range(60):
                a = np.empty((CARD[1], CARD[0], 3), dtype=np.uint8)
                a[:] = GROUNDS[s]
                x, y = LK[0] - dx, LK[1] - dy
                a[y:y + 48, x:x + 48] = tile[s]
                im = Image.fromarray(a)
                r = tuple(counts_(np.asarray(reduce(im, w, Image.LANCZOS)), x, y, w / CARD[0], s)["lever_red_px"]
                          for w in FEED_WIDTHS)
                grid[(dx, dy)] = r
        at = grid[(0, 0)]
        best360 = max(v[1] for v in grid.values())
        both = max(min(v) for v in grid.values())
        place[s] = {"today_500_360": list(at), "best_at_360": best360, "worst_at_360": min(v[1] for v in grid.values()),
                    "share_of_positions_at_360": {str(n): round(sum(1 for v in grid.values() if v[1] == n) / len(grid), 3)
                                                  for n in sorted({v[1] for v in grid.values()})},
                    "best_min_of_both_widths": both}
    res["placement"] = place
    save("feed", res)
    feed_dark_key(res)
    return res


def feed_dark_key(res=None):
    """The figures chapter 08 prints (stage_a_identity_lib.figures("feed_dark")): the test at 500 and 360 px with Lanczos
    on the card drawn on each ground, and the floors, from the full study above."""
    if res is None:
        res = json.loads(FIGS.read_text())["feed"]
    out = {"source": "work/build/scripts/phase-2/stage_c_identity_round0.py feed, key feed",
           "lockmark_master": res["lockmark_master"], "floors": res["light_floor"], "filter": "lanczos"}
    for s, v in res["at_rule_widths"].items():
        out[s] = {w: {k: c["lanczos"][k] for k in ("nodes_kept", "of", "lever_red_px", "passes") if k in c["lanczos"]}
                  for w, c in v.items()}
    save("feed_dark", out)
    return out


# =========================================================================================== proposals
# The print L3 at the masthead's proportion (D2-482, D2-483, CD-S10): the October master with only its lockmark resized,
# from 2.4 cap heights to 48 over 22, as DR-131 and D2-477 resized it in the masthead. The wordmark, the 0.60 cap height
# of space, the lockmark's display drawing and its centering on the capitals stay. Capitals run from y 4 to 104.
PRINT_L3 = {"src": "lockups/20261028_L3-Horizontal-Master.svg", "dst": "lockups/20261110_L3-Horizontal-Print-Master.svg",
            "src_white": "prussian/20261028_L3-Horizontal-Master-Prussian-White.svg",
            "dst_white": "prussian/20261110_L3-Horizontal-Print-Master-Prussian-White.svg"}
CAP_TOP, CAP_H = 4, 100
LOCK_CAPS = 48 / 22                  # the masthead's lockmark over its capitals (DR-131, D2-477)
PRINT_L3_TITLE = ("L3 horizontal lockup, print master at the masthead's proportion: the wordmark's display master, 0.60 "
                  "cap height of space and the lockmark's display master at 48/22 cap heights, as in the 282 px masthead, "
                  "centered on the capitals. For print and for widths other than the masthead's 282 px. Proposed for "
                  "board C; the October master stays in use until approved")


def print_l3_svg(src_text, white=False):
    m = re.search(r'<svg x="([\d.]+)" y="(-?[\d.]+)" width="([\d.]+)" height="([\d.]+)" viewBox="0 0 123.5 123.5"', src_text)
    x, y, w, h = map(float, m.groups())
    assert (y, w, h) == (-66.0, 240.0, 240.0), "the October master is not the file this step was written for"
    size = round(CAP_H * LOCK_CAPS, 2)                       # 218.18
    top = round(CAP_TOP + CAP_H / 2 - size / 2, 2)           # -55.09: centered on the capitals, as before
    width = round(x + size, 2)
    out = src_text.replace(m.group(0), f'<svg x="{m.group(1)}" y="{top:g}" width="{size:g}" height="{size:g}" viewBox="0 0 123.5 123.5"', 1)
    out = out.replace('viewBox="0 -66 1278.31 240"', f'viewBox="0 {top:g} {width:g} {size:g}"', 1)
    title = PRINT_L3_TITLE + (". Treatment D for Prussian: one color, White" if white else "")
    out = re.sub(r"<title>.*?</title>", f"<title>{LIB.E(title).replace(chr(39), '&#x27;')}</title>", out, count=1)
    # nothing else moves: undo the three changes and the file is the October master again
    back = re.sub(r"<title>.*?</title>", re.search(r"<title>.*?</title>", src_text).group(0), out, count=1)
    back = back.replace(f'viewBox="0 {top:g} {width:g} {size:g}"', 'viewBox="0 -66 1278.31 240"', 1)
    back = back.replace(f'<svg x="{m.group(1)}" y="{top:g}" width="{size:g}" height="{size:g}"', m.group(0)[:m.group(0).index(' viewBox')], 1)
    assert back == src_text, "the print L3 differs from the October master in more than the lockmark's size, the view box and the title"
    return out, {"lockmark_units": size, "lockmark_top": top, "width_units": width, "gap_units": round(x - 978.31, 2),
                 "lockmark_over_capitals": round(size / CAP_H, 4), "width_over_capitals": round(width / CAP_H, 4)}


def proposals():
    rec = {}
    for k_src, k_dst, white in (("src", "dst", False), ("src_white", "dst_white", True)):
        src = ID_DIR / PRINT_L3[k_src]
        dst = ID_DIR / PRINT_L3[k_dst]
        text, geo = print_l3_svg(src.read_text(), white)
        if dst.exists() and dst.read_text() != text:
            raise SystemExit(f"{dst.name} exists with other content; a proposal file is written once")
        dst.write_text(text)
        rec[PRINT_L3[k_dst]] = dict(geo, source=PRINT_L3[k_src])
    october = {"lockmark_units": 240, "width_units": 1278.31, "gap_units": 60, "lockmark_over_capitals": 2.4,
               "width_over_capitals": 12.7831}
    rec["october_master"] = october
    # at L3's print minimum, 1.55 in wide (Rule 03.4), the capitals and the lockmark in each drawing
    for name, g in (("october_at_1.55_in", october), ("proposal_at_1.55_in", rec[PRINT_L3["dst"]])):
        caps_in = 1.55 / g["width_over_capitals"]
        rec[name] = {"capitals_mm": round(caps_in * 25.4, 2), "lockmark_in": round(caps_in * g["lockmark_over_capitals"], 3)}
    rec["masthead_master"] = {"file": LIB.L3["masthead"], "capitals_px": 22, "gap_px": 13, "lockmark_px": 48,
                              "lockmark_over_capitals": round(48 / 22, 4), "gap_over_capitals": round(13 / 22, 4)}
    save("proposals", {"print_l3": rec})
    return rec


# =========================================================================================== plates
# Comparison pages for board C, each at actual size (CLAUDE.md gate rule 4; Master Brief section 3, change control, and
# section 9, step 4: original, proposal and an overlay). They are handoff files for the board builder; no board is
# written here. Masters are inlined from their files, unchanged, with only width, height and style on the root.
PLATE_CSS = """
body{margin:0;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);
 font-family:Inter,system-ui,sans-serif;font-size:17px;line-height:1.55}
main{padding:40px 40px 64px;max-width:1300px}
h1{font:800 32px/1.15 "Inter Tight",Inter,sans-serif;margin:0 0 12px;max-width:30em}
h2{font:700 20px/1.3 Inter,sans-serif;margin:48px 0 8px;padding-top:16px;border-top:1px solid var(--oa-color-border-hairline-on-newsprint)}
main>p,.note{margin:0 0 12px;max-width:44em}
.tag{display:block;font-size:13px;line-height:1.4;color:var(--oa-color-text-secondary-on-newsprint);margin:8px 0 0}
.row{display:flex;flex-wrap:wrap;gap:32px 48px;align-items:flex-start;margin:16px 0 0}
.stack{display:flex;flex-direction:column;gap:20px;margin:16px 0 0}
.cell{display:flex;flex-direction:column;align-items:flex-start}
.ground{padding:24px;line-height:0}
.s-newsprint{background:var(--oa-color-surface-newsprint)}.s-white{background:var(--oa-color-surface-white)}
.s-charcoal{background:var(--oa-color-surface-charcoal)}.s-prussian{background:var(--oa-color-surface-prussian)}
.s-newsprint.ground{border:1px solid var(--oa-color-border-hairline-on-newsprint)}
.s-white.ground{border:1px solid var(--oa-color-border-hairline-on-white)}
.s-charcoal .tag{color:var(--oa-color-text-secondary-on-charcoal)}.s-prussian .tag{color:var(--oa-color-text-secondary-on-prussian)}
table{border-collapse:collapse;font-size:15px;margin:12px 0 0;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:6px 16px 6px 0;border-top:1px solid var(--oa-color-border-hairline-on-newsprint);vertical-align:top}
th{font-weight:700}
.px{image-rendering:pixelated}
.cell>svg,.stack svg{display:block}
"""


def plate_page(title, body, css=""):
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{LIB.E(title)}</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<style>{tokens}</style><style>:root{{color-scheme:light}}{PLATE_CSS}{css}</style></head><body><main>{body}</main></body></html>')


def svg_at(rel, *, h=None, w=None, surface="newsprint", mode="color", label=""):
    """A master inlined from its file at a size, its hooks set for a surface (stage_a_identity_lib.mark_style). On
    Prussian in color, the White file beside it."""
    path = ID_DIR / rel
    style = LIB.mark_style(surface, mode)
    if surface == "prussian" and mode == "color":
        alt = ID_DIR / "prussian" / (Path(rel).stem + "-Prussian-White.svg")
        if alt.exists():
            path, style = alt, ""
    text = path.read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', text).group(1).split()]
    if h is None:
        h = w * vb[3] / vb[2]
    if w is None:
        w = h * vb[2] / vb[3]
    root = re.match(r"<svg\b[^>]*>", text).group(0)
    new_root = root[:-1] + f' width="{w:.2f}" height="{h:.2f}" role="img" aria-label="{LIB.E(label or path.stem)}" style="{style}">'
    return text.replace(root, new_root, 1), (w, h)


def l3_pair(caps, surface="newsprint", mode="color", tags=True):
    """The October L3 master over the proposal, at one cap height, left edges together so the wordmarks align."""
    out = []
    for rel, name in ((PRINT_L3["src"], "In use for print: the October L3 master, its lockmark at 2.4 cap heights"),
                      (PRINT_L3["dst"], "Proposal: the print L3, its lockmark at 2.18 cap heights, as in the masthead")):
        vbh = 240 if rel == PRINT_L3["src"] else CAP_H * LOCK_CAPS
        s, (w, h) = svg_at(rel, h=caps * vbh / CAP_H, surface=surface, mode=mode, label=name)
        tag = f'<span class="tag">{LIB.E(name)}; capitals {caps:g} px, {w:.0f} by {h:.0f} px</span>' if tags else ""
        out.append(f'<div class="cell">{s}{tag}</div>')
    return '<div class="stack">' + "".join(out) + "</div>"


def overlay(caps):
    """The two L3 drawings on one wordmark: the October master in Stone, the proposal over it in Charcoal and red."""
    k = caps / CAP_H
    a, (wa, ha) = svg_at(PRINT_L3["src"], h=240 * k, mode="mono", surface="newsprint", label="October L3 master")
    a = a.replace('style="', 'style="position:absolute;left:0;top:0;opacity:1;', 1)
    a = re.sub(r'(color:)var\(--oa-color-text-primary-on-newsprint\)', r"\1var(--oa-color-palette-stone)", a)
    a = a.replace("--amp:var(--oa-color-text-primary-on-newsprint)", "--amp:var(--oa-color-palette-stone)")
    a = re.sub(r"--(lever|link|line):var\(--oa-color-text-primary-on-newsprint\)", r"--\1:var(--oa-color-palette-stone)", a)
    b, (wb, hb) = svg_at(PRINT_L3["dst"], h=CAP_H * LOCK_CAPS * k, label="Print L3 proposal")
    top = (-55.09 - -66) * k
    b = b.replace('style="', f'style="position:absolute;left:0;top:{top:.2f}px;', 1)
    return (f'<div style="position:relative;width:{wa:.0f}px;height:{ha:.0f}px">{a}{b}</div>'
            f'<span class="tag">Capitals {caps:g} px. The October master in Stone; the proposal over it, in Charcoal with its red, '
            'shares the wordmark, the space before the lockmark and the lockmark’s vertical center, and its lockmark is 9.1 '
            'percent smaller.</span>')


def plates(scratch):
    import numpy as np
    from PIL import Image
    import stage_a_identity_proofs as SP
    scratch = Path(scratch).resolve()
    d = scratch / "plates"
    d.mkdir(parents=True, exist_ok=True)
    PLATES.mkdir(parents=True, exist_ok=True)
    prop = json.loads(FIGS.read_text())["proposals"]["print_l3"]
    F = json.loads(FIGS.read_text())["feed"]
    floors = F["light_floor"]
    out_files = []

    # -------------------------------------------------------------------------------- 1. the print L3
    ms, _ = svg_at(LIB.L3["masthead"], h=48, label="L3 masthead master")
    oc, (ow, oh) = svg_at(PRINT_L3["src"], w=282, label="October L3 master at 282 px")
    pr, (pw, ph) = svg_at(PRINT_L3["dst"], w=282, label="Print L3 proposal at 282 px")
    o155, p155 = prop["october_at_1.55_in"], prop["proposal_at_1.55_in"]
    body = (
        '<h1>A print L3 at the masthead’s proportion</h1>'
        '<p>Proposed for board C, for approval by name (gate rule 4). Since November 8 the masthead sets L3’s lockmark at 48 px '
        'beside 22 px capitals, 2.18 cap heights (DR-131). Print and every width but the 282 px masthead still take the October '
        'master, whose lockmark stands 2.4 cap heights (D2-482), so L3 prints at one proportion and shows on screen at another. '
        'The proposal is the October master with one change: its lockmark drawn at 2.18 cap heights, centered on the capitals as '
        'before. The wordmark, the 0.60 cap height of space, both display drawings and the colors stay.</p>'
        '<p>Files: <code>lockups/20261110_L3-Horizontal-Print-Master.svg</code> and its White file in <code>prussian/</code>, '
        'new files beside the masters. The guide keeps naming the October master until Dustin approves.</p>'
        '<h2>At the masthead’s width, 282 px</h2>'
        '<p>The masthead master is drawn on the pixel grid and serves 282 px on screen alone. At the same width the October '
        'master sets a larger lockmark and smaller capitals; the proposal matches the masthead’s proportion.</p>'
        f'<div class="row"><div class="cell ground s-newsprint">{ms}<span class="tag">In use on screen: the masthead master, 282 by 48 px, capitals 22 px</span></div>'
        f'<div class="cell ground s-newsprint">{oc}<span class="tag">October master, 282 by {oh:.1f} px, capitals {282 / 12.7831:.1f} px</span></div>'
        f'<div class="cell ground s-newsprint">{pr}<span class="tag">Proposal, 282 by {ph:.1f} px, capitals {282 / prop[PRINT_L3["dst"]]["width_over_capitals"]:.1f} px</span></div></div>'
        '<h2>At 16, 24, 48 and 96 px capitals</h2>'
        '<p>Each pair shares its capitals and its left edge. Under 37 px capitals a page draws L3 from the pixel masters, which '
        'this proposal leaves alone, so the 16 and 24 px rows compare the two drawings’ proportions only.</p>'
        + "".join(f'<div class="ground s-newsprint" style="margin-top:16px;line-height:1.4">{l3_pair(c)}</div>' for c in (16, 24, 48, 96))
        + '<h2>Display size, with the overlay</h2>'
        f'<div class="ground s-newsprint" style="margin-top:16px;line-height:1.4">{overlay(100)}</div>'
        '<h2>On the four approved surfaces, at 40 px capitals</h2>'
        + "".join(f'<div class="ground s-{s}" style="margin-top:16px;line-height:1.4">{l3_pair(40, s)}</div>' for s in ("newsprint", "white", "charcoal", "prussian"))
        + '<h2>In one color</h2>'
        f'<div class="ground s-newsprint" style="margin-top:16px;line-height:1.4">{l3_pair(40, "newsprint", "mono-dark")}</div>'
        f'<div class="ground s-charcoal" style="margin-top:16px;line-height:1.4">{l3_pair(40, "charcoal", "mono-light")}</div>'
        '<h2>In print</h2>'
        f'<p>L3’s print minimum is 1.55 in wide (Rule 03.4). There the October master sets {o155["capitals_mm"]} mm capitals and a '
        f'{o155["lockmark_in"]} in lockmark; the proposal, {p155["capitals_mm"]} mm capitals and a {p155["lockmark_in"]} in lockmark, '
        'over the 3 mm capitals and the 0.25 in lockmark that Rules 03.4 and 08.1 set as print minimums. The PDF beside this page '
        'prints both at 1.55, 2.5 and 4 in wide.</p>'
        + "".join(f'<div class="ground s-white" style="margin-top:16px;line-height:1.4"><div class="stack">'
                  f'<div class="cell">{svg_at(PRINT_L3["src"], w=96 * x, surface="white")[0]}<span class="tag">October master, {x:g} in wide</span></div>'
                  f'<div class="cell">{svg_at(PRINT_L3["dst"], w=96 * x, surface="white")[0]}<span class="tag">Proposal, {x:g} in wide</span></div></div></div>'
                  for x in (1.55, 2.5))
    )
    l3_html = PLATES / "20261110_Print-L3-Comparison.html"
    l3_html.write_text(plate_page("Print L3 comparison", body))
    out_files.append(l3_html)
    pbody = ('<h1 style="font-size:16pt">A print L3 at the masthead’s proportion: print proof</h1>'
             '<p style="font-size:10pt">Each pair at true size on US Letter. Above, the October master in use for print; below, the '
             'proposal. Proposed for board C; not in use.</p>'
             + "".join(f'<div style="margin:18pt 0 0;line-height:1.4"><div class="stack" style="gap:10pt">'
                       f'<div class="cell">{svg_at(PRINT_L3["src"], w=96 * x, surface="white")[0]}<span class="tag" style="font-size:9pt">October master, {x:g} in wide</span></div>'
                       f'<div class="cell">{svg_at(PRINT_L3["dst"], w=96 * x, surface="white")[0]}<span class="tag" style="font-size:9pt">Proposal, {x:g} in wide</span></div></div></div>'
                       for x in (1.55, 2.5, 4)))
    l3_print = PLATES / "20261110_Print-L3-Comparison-Print.html"
    l3_print.write_text(plate_page("Print L3 print proof", pbody, css="html,body{background:#fff!important}main{padding:0}@page{size:letter;margin:0.75in}"))
    out_files.append(l3_print)

    # -------------------------------------------------------------------------------- 2. the social sign-off at 96 px
    LIB.INLINE_ALL[0] = True
    try:
        cards = {}
        for s in ("newsprint", "charcoal"):
            today = SP._social(s, sign=48)
            m48 = LIB.lockmark(48, surface=s, label="Lockmark")
            assert today.count(m48) == 1, "the card's sign-off is not where the plate expects it"
            cards[f"{s}-48"] = today
            cards[f"{s}-96"] = today.replace(m48, LIB.mark(LOCK[48], h=96, surface=s, label="Lockmark"), 1)
    finally:
        LIB.INLINE_ALL[0] = False
    cap_html = d / "cards.html"
    cap_html.write_text(page("".join(f'<div id="c-{k}" style="width:1200px">{v}</div>' for k, v in cards.items())))
    js = d / "shot.js"
    js.write_text(SHOT_JS)
    subprocess.run(["node", str(js), str(d), str(cap_html), *[f"c-{k}" for k in cards]], check=True, capture_output=True, text=True,
                   cwd=str(ROOT / "work/build"))
    sign = {"method": "The proofs' card drawn by stage_a_identity_proofs._social, its sign-off swapped for the 48 px master at "
                      "96 px, captured at 1x; counted as Rule 08.2 counts, with each node's square scaled by 2"}
    imgs_html = {}

    def counts_k(arr, ox, oy, sc, ground, k):
        h, w = arr.shape[:2]
        kept, red = 0, 0
        for cy in CENTERS48:
            for cx in CENTERS48:
                lever = (cx, cy) == (CENTERS48[2], CENTERS48[2])
                X, Y = (ox + cx * k) * sc, (oy + cy * k) * sc
                r = (4.5 if lever else 3.5) * k * sc + 1
                px = [tuple(int(c) for c in arr[y, x]) for x in range(int(X - r), int(X + r) + 1)
                      for y in range(int(Y - r), int(Y + r) + 1) if 0 <= x < w and 0 <= y < h]
                if lever:
                    red = sum(1 for p in px if is_red(p))
                elif ground in LIGHT_GROUNDS:
                    kept += min(max(p) for p in px) < DARK_MAX
                else:
                    kept += max(min(p) for p in px) > floors[ground]
        return {"nodes_kept": kept, "lever_red_px": red, "passes": kept == 8 and red >= MIN_RED}

    for key in cards:
        s, size = key.split("-")
        k = int(size) // 48
        L = 48 * k
        ox, oy = CARD[0] - 1 - 72 - L, CARD[1] - 1 - 72 - L
        im = Image.open(d / f"c-{key}.png").convert("RGB")
        assert im.size == CARD
        row = {}
        for w in FEED_WIDTHS:
            sc = w / CARD[0]
            sm = reduce(im, w, Image.LANCZOS)
            row[f"at_{w}"] = counts_k(np.asarray(sm), ox, oy, sc, s, k)
            th = jpeg(sm, 75, 2)
            row[f"at_{w}_then_jpeg_q75_420"] = counts_k(np.asarray(th), ox, oy, sc, s, k)
            box = (int(ox * sc) - 2, int(oy * sc) - 2, int((ox + L) * sc + 0.999) + 2, int((oy + L) * sc + 0.999) + 2)
            for tag, src in (("", sm), ("-jpeg", th)):
                f = PLATES / f"20261110_Sign-Off-{s.title()}-{size}px-At-{w}{'-Thumbnail-Jpeg' if tag else ''}-8x.png"
                src.crop(box).resize(((box[2] - box[0]) * 8, (box[3] - box[1]) * 8), Image.NEAREST).save(f)
                imgs_html[(key, w, tag)] = f.name
                out_files.append(f)
            f = PLATES / f"20261110_Social-Card-{s.title()}-{size}px-At-{w}.png"
            sm.save(f)
            imgs_html[(key, w, "card")] = f.name
            out_files.append(f)
        fails = []
        jfails = []
        for w in range(300, 601):
            sc = w / CARD[0]
            sm = reduce(im, w, Image.LANCZOS)
            if not counts_k(np.asarray(sm), ox, oy, sc, s, k)["passes"]:
                fails.append(w)
            if w % 4 == 0 and not counts_k(np.asarray(jpeg(sm, 75, 2)), ox, oy, sc, s, k)["passes"]:
                jfails.append(w)
        row["lanczos_fail_widths_300_to_600"] = fails
        row["thumbnail_jpeg_q75_420_fail_widths_every_4th_300_to_600"] = {"fails": len(jfails), "of": len(range(300, 601, 4))}
        row["lockmark_px_at"] = {str(w): round(L * w / CARD[0], 1) for w in FEED_WIDTHS}
        sign[key] = row
    wm_caps = 44 * 100 / 108
    sign["card_wordmark_capitals_px"] = round(wm_caps, 2)
    sign["lockmark_over_wordmark_capitals"] = {"48": round(48 / wm_caps, 3), "96": round(96 / wm_caps, 3)}
    d_all = json.loads(FIGS.read_text())
    d_all["proposals"]["social_sign_off_96"] = sign
    FIGS.write_text(json.dumps(d_all, indent=1, ensure_ascii=False) + "\n")

    def fig_row(s):
        cells = []
        for size in ("48", "96"):
            key = f"{s}-{size}"
            r = sign[key]
            cells.append(
                f'<div class="cell"><p style="margin:0 0 8px"><b>{"Today, 48 px" if size == "48" else "Proposal, 96 px"}</b></p>'
                + "".join(f'<img src="{imgs_html[(key, w, "card")]}" width="{w}" alt="The card reduced to {w} px wide" style="display:block;margin:0 0 6px">'
                          f'<span class="tag" style="margin:0 0 12px">At {w} px wide, as a feed draws it: {r[f"at_{w}"]["nodes_kept"]} of 8 nodes, {r[f"at_{w}"]["lever_red_px"]} red pixels; the lockmark {r["lockmark_px_at"][str(w)]} px</span>'
                          for w in FEED_WIDTHS)
                + '<div class="row" style="gap:16px">'
                + "".join(f'<div class="cell"><img class="px" src="{imgs_html[(key, w, "")]}" alt="The sign-off at {w} px, enlarged eight times">'
                          f'<span class="tag">{w} px, enlarged 8x</span></div>' for w in FEED_WIDTHS)
                + f'<div class="cell"><img class="px" src="{imgs_html[(key, 360, "-jpeg")]}" alt="The sign-off at 360 px saved as a JPEG, enlarged eight times">'
                  f'<span class="tag">360 px, then a JPEG at quality 75 with chroma at half size: {r["at_360_then_jpeg_q75_420"]["lever_red_px"]} red pixels</span></div>'
                + '</div></div>')
        return '<div class="row">' + "".join(cells) + "</div>"

    n48, n96, c48, c96 = sign["newsprint-48"], sign["newsprint-96"], sign["charcoal-48"], sign["charcoal-96"]
    sbody = (
        '<h1>The social card’s sign-off at 96 px</h1>'
        '<p>Proposed for board C, for approval by name (gate rule 4). Today a social card signs off with the lockmark at 48 px from '
        'its 48 px master (DR-131). A feed that shows the card 360 px wide draws that lockmark at 14.4 px, under its own 16 px '
        'floor, and its lever 2.7 px across. Rule 08.2’s test still passes there, with 5 red pixels against a floor of 4. '
        'The proposal draws the same 48 px master at exactly twice its size, 96 px, on social cards only, so every node and the '
        'lever still land on whole pixels. Covers, posters and the masthead keep 48 px. No new drawing is made.</p>'
        f'<p>On the card the 96 px lockmark stands {sign["lockmark_over_wordmark_capitals"]["96"]:.2f} times the wordmark’s '
        f'{sign["card_wordmark_capitals_px"]:.1f} px capitals, between the masthead’s 2.18 and the October L3’s 2.4, so the two '
        'corners keep L3’s own proportion.</p>'
        '<h2>What the feed test finds</h2>'
        '<table><tr><th>Card</th><th>500 px</th><th>360 px</th><th>360 px, then a JPEG at quality 75, chroma at half size</th>'
        '<th>Widths 300 to 600 px that fail</th></tr>'
        + "".join(f'<tr><td>{lab}</td><td>{r["at_500"]["nodes_kept"]} of 8 nodes, {r["at_500"]["lever_red_px"]} red</td>'
                  f'<td>{r["at_360"]["nodes_kept"]} of 8 nodes, {r["at_360"]["lever_red_px"]} red</td>'
                  f'<td>{r["at_360_then_jpeg_q75_420"]["lever_red_px"]} red</td><td>{len(r["lanczos_fail_widths_300_to_600"])} of 301</td></tr>'
                  for lab, r in (("Newsprint, 48 px today", n48), ("Newsprint, 96 px proposal", n96),
                                 ("Charcoal, 48 px today", c48), ("Charcoal, 96 px proposal", c96)))
        + '</table>'
        '<p class="note" style="margin-top:12px">A JPEG saved from the full 1,200 px card leaves today’s counts as they are at every quality we '
        'tried. A JPEG saved after the card is shrunk, with its color kept at half size, as many image services store a '
        'thumbnail, takes every red pixel from today’s lever at 360 px. We have not tested a real feed.</p>'
        '<h2>Today’s card, actual size, 1200 by 630 px</h2>'
        f'<div class="oai" style="margin-top:16px">{cards["newsprint-48"]}</div>'
        '<h2>The proposal, actual size, 1200 by 630 px</h2>'
        f'<div class="oai" style="margin-top:16px">{cards["newsprint-96"]}</div>'
        '<h2>In a feed, on Newsprint</h2>' + fig_row("newsprint")
        + '<h2>In a feed, on Charcoal</h2>' + fig_row("charcoal")
        + '<h2>The proposal on Charcoal, actual size</h2>'
        f'<div class="oai" style="margin-top:16px">{cards["charcoal-96"]}</div>'
        '<h2>The mark alone</h2>'
        '<div class="row">'
        + "".join(f'<div class="cell ground s-{s}">{svg_at(LOCK[48], h=h, surface=s, label="Lockmark")[0]}'
                  f'<span class="tag">48 px master at {h} px{", today" if h == 48 else ", proposal"}</span></div>'
                  for s in ("newsprint", "charcoal") for h in (48, 96))
        + f'<div class="cell ground s-newsprint">{svg_at(LOCK["display"], h=96, label="Lockmark display master")[0]}'
          '<span class="tag">Display master at 96 px, for comparison: its lever is 7.4 px</span></div>'
        + '</div>'
    )
    so_html = PLATES / "20261110_Social-Sign-Off-Comparison.html"
    so_html.write_text(plate_page("Social sign-off comparison", sbody, css=LIB.CSS))
    out_files.append(so_html)

    # -------------------------------------------------------------------------------- captures and the print PDF
    job = d / "pages.json"
    job.write_text(json.dumps([str(l3_html), str(so_html), str(l3_print)]))
    js = d / "pages.js"
    js.write_text(PAGES_JS)
    r = subprocess.run(["node", str(js), str(job)], check=True, capture_output=True, text=True, cwd=str(ROOT / "work/build"))
    made = json.loads(r.stdout.strip().splitlines()[-1])
    out_files += [Path(p) for p in made["files"]]
    d_all = json.loads(FIGS.read_text())
    d_all["plates"] = {"files": [LIB.rel(p) for p in out_files], "fonts": made["fonts"]}
    FIGS.write_text(json.dumps(d_all, indent=1, ensure_ascii=False) + "\n")
    return d_all["plates"], sign


PAGES_JS = r"""
const fs = require('fs');
const { chromium } = require('playwright');
const [job] = process.argv.slice(2);
const pages = JSON.parse(fs.readFileSync(job, 'utf8'));
(async () => {
  const b = await chromium.launch();
  const files = []; let fonts = [];
  for (const html of pages) {
    const isPrint = html.endsWith('-Print.html');
    for (const scale of isPrint ? [] : [1, 2]) {
      const p = await b.newPage({ viewport: { width: 1380, height: 1000 }, deviceScaleFactor: scale });
      await p.goto('file://' + html, { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      fonts = fonts.concat(await p.evaluate(() => [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family + ' ' + f.weight)));
      const out = html.replace(/\.html$/, `-${scale}x.png`);
      await p.screenshot({ path: out, fullPage: true });
      files.push(out);
      await p.close();
    }
    if (isPrint) {
      const p = await b.newPage();
      await p.goto('file://' + html, { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      const out = html.replace(/\.html$/, '.pdf');
      await p.pdf({ path: out, format: 'Letter', preferCSSPageSize: true, printBackground: true });
      files.push(out);
      await p.close();
    }
  }
  console.log(JSON.stringify({ files, fonts: [...new Set(fonts)] }));
  await b.close();
})();
"""


# =========================================================================================== opener
GUIDE_PAGE = ROOT / "work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html"
OPENER_JS = r"""
const { chromium } = require('playwright');
const [page, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const res = {};
  for (const [w, scale] of [[1440, 1], [1024, 1], [768, 1], [390, 2], [360, 2], [1440, 2]]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: scale, colorScheme: 'dark' });
    await p.goto('file://' + page, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const fig = p.locator('#fig-s-09-opener');
    await fig.scrollIntoViewIfNeeded();
    const r = await fig.evaluate((f) => {
      const box = (e) => { const q = e.getBoundingClientRect(); return [Math.round(q.left * 10) / 10, Math.round(q.top * 10) / 10, Math.round(q.width * 10) / 10, Math.round(q.height * 10) / 10]; };
      const ch = f.closest('section.chapter');
      const intro = ch.querySelector('.intro, p.intro') || null;
      const scroll = f.querySelector('.plate-scroll');
      const stage = f.querySelector('.plate-stage');
      const items = [...f.querySelectorAll('.p9-pi')].map((li) => box(li));
      const icons = [...f.querySelectorAll('svg[data-icon-family="pillar"]')].map((s) => ({ icon: s.getAttribute('data-icon'), box: box(s), color: getComputedStyle(s).color }));
      const words = [...f.querySelectorAll('.p9-w')].map((s) => ({ text: s.textContent, size: getComputedStyle(s).fontSize, weight: getComputedStyle(s).fontWeight }));
      const prev = f.previousElementSibling;
      const next = f.nextElementSibling;
      return {
        figure: box(f), stage: box(stage), scroll_overflows: scroll.scrollWidth > scroll.clientWidth + 0.5,
        scroll_w: [scroll.scrollWidth, scroll.clientWidth], page_overflows: document.documentElement.scrollWidth > innerWidth,
        rows: new Set(items.map((i) => Math.round(i[1]))).size, items, icons, words,
        stage_role: stage.getAttribute('role'), stage_label: stage.getAttribute('aria-label'),
        hint_shown: !f.querySelector('.plate-hint').hidden, fit_switch: !!f.querySelector('.fit-switch'),
        before: prev ? prev.className || prev.tagName : null, after: next ? next.className || next.tagName : null,
        theme: document.documentElement.getAttribute('data-oa-theme'), bg: getComputedStyle(stage).backgroundColor,
      };
    });
    await fig.screenshot({ path: `${out}/opener-${w}@${scale}x.png` });
    res[`${w}@${scale}x`] = r;
    await p.close();
  }
  console.log(JSON.stringify(res));
  await b.close();
})();
"""


def opener(scratch):
    scratch = Path(scratch).resolve()
    d = scratch / "opener"
    d.mkdir(parents=True, exist_ok=True)
    js = d / "opener.js"
    js.write_text(OPENER_JS)
    r = subprocess.run(["node", str(js), str(GUIDE_PAGE), str(d)], check=True, capture_output=True, text=True, cwd=str(ROOT / "work/build"))
    res = json.loads(r.stdout.strip().splitlines()[-1])
    save("opener", {"page": LIB.rel(GUIDE_PAGE), "method": "Chromium through Playwright, device set to dark (the guide forces light), "
                    "the figure scrolled into view at each width", "widths": res})
    return res


# =========================================================================================== main
if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what == "floor" and len(sys.argv) > 2:
        r = feed(sys.argv[2])[0]
        print(json.dumps(r["floor_study"], indent=1))
    elif what == "feed" and len(sys.argv) > 2:
        r = feed_run(sys.argv[2])
        print(json.dumps({k: r[k] for k in ("floor_study", "light_floor")}, indent=1))
        for s, v in r["at_rule_widths"].items():
            print(s, {w: {f: (c["nodes_kept"], c.get("lever_red_px"), c.get("passes")) for f, c in x.items()} for w, x in v.items()})
        print("chromium", {k: (v["nodes_kept"], v.get("lever_red_px"), v.get("passes")) for k, v in r["chromium_img_downscale"].items()})
        print("widths", {s: {k: v[k] for k in ("fail_count", "lever_red_min", "lever_red_max", "nodes_min")} for s, v in r["widths"].items()})
        print("placement", json.dumps(r["placement"]))
    elif what == "feed-dark-key":
        print(json.dumps(feed_dark_key(), indent=1))
    elif what == "proposals":
        print(json.dumps(proposals(), indent=1))
    elif what == "opener" and len(sys.argv) > 2:
        for k, v in opener(sys.argv[2]).items():
            print(k, {x: v[x] for x in ("figure", "stage", "scroll_overflows", "page_overflows", "rows", "hint_shown", "before", "after", "theme", "bg")})
            print("   words", [(w["text"], w["size"], w["weight"]) for w in v["words"]], "icons", [(i["icon"], i["box"][2]) for i in v["icons"]])
    elif what == "plates" and len(sys.argv) > 2:
        pl, sign = plates(sys.argv[2])
        print(json.dumps(pl, indent=1))
        print(json.dumps({k: {x: v[x] for x in v if not x.startswith("lanczos")} if isinstance(v, dict) else v for k, v in sign.items() if k != "method"}, indent=1))
    else:
        print(__doc__)
        sys.exit(2)
