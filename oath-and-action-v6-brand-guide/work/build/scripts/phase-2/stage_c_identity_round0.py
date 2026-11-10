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
  opener DIR   Builds the guide page into DIR and measures s-09-opener in it at 1440, 1024, 768, 390 and 360 px.

Run: python3 -I work/build/scripts/phase-2/stage_c_identity_round0.py feed|proposals|plates|opener <scratch dir>
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
const { chromium } = require('playwright');
const [out, job] = process.argv.slice(2);
const items = JSON.parse(require('fs').readFileSync(job, 'utf8'));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 700, height: 400 }, deviceScaleFactor: 1 });
  for (const it of items) {
    await p.setContent(`<html><body style="margin:0;background:#888"><img id="i" src="file://${it.src}" width="${it.w}" style="display:block"></body></html>`);
    await p.waitForFunction(() => document.getElementById('i').complete);
    await p.locator('#i').screenshot({ path: it.out });
  }
  console.log(JSON.stringify({ n: items.length }));
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
        cards = {s: f'<div id="card-{s}" style="width:1200px">{SP._social(s)}</div>' for s in GROUNDS}
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
    else:
        print(__doc__)
        sys.exit(2)
