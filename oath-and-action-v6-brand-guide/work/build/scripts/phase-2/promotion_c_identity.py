"""Promotion C, November 11, 2026: drawings board C's identity approvals go into use.

Under work/handoffs/phase-2/20261111_Promotion-Stage-C-Brief.md, "Who does what", item 2 (identity designer).

  Print L3 (DR-210)   lockups/20261110_L3-Horizontal-Print-Master.svg and its Prussian White file serve print and every
                      width but the 282 px masthead, by reference, bytes unchanged (stage_a_identity_lib.L3["print"]).
                      The October master stays as the record.
  Sign-off (DR-211)   A social card signs off with the 48 px lockmark master drawn at exactly twice its size, 96 px
                      (stage_a_identity_lib.sign_off, stage_a_identity_proofs._social). Covers, posters and the masthead
                      keep 48 px.

Steps, each run alone:

  minimums     The minimum sizes record (stage_a_identity_s1.update_minimums). Writes no master.
  specimens    The identity build, as promotion_identity.py specimens runs it (chapters 03, 04, 08 and 09, the proofs,
               their specimens and manifest-identity.json; the letterhead proof is not written).
  feed DIR     Builds the guide page into DIR with guide_build.py --out (strict first; when strict stops, a plain
               build for the measure, and the warnings are recorded). Captures the proofs' card from the built page at
               1x, and the same card drawn alone on Newsprint, White, Charcoal and Prussian with the sign-off at 96 and
               at 48 px, and the 96 px sign-off alone, whole and with its links only. Checks that the built page and the
               card drawn alone put the same pixels in the sign-off's box. Runs Rule 08.2's test at 500 and 360 px
               (Lanczos; bicubic, bilinear and box for the record), the floor study for dark grounds on the 96 px
               drawing, the thumbnail path (reduce, then a JPEG at quality 75 with chroma at half size) at 48 and 96 px,
               and every width from 300 to 600 px. Writes work/handoffs/phase-2/20261111_Promotion-C-Identity-Figures.json,
               keys feed, feed_dark, feed_thumbnail and feed_study.
  hashes       The print L3 files' sha256 against HEAD and against round 0's figures; writes key hashes.
  plates DIR   Captures every changed plate from DIR/guide.html at 1440 and 390 px (1x and 2x), the 24 px kicker icon
               at 1x and 2x, and the changed rules' text; writes DIR/plates/ and key plates.

Run: python3 -I work/build/scripts/phase-2/promotion_c_identity.py minimums | specimens | feed DIR | hashes | plates DIR
Then specimens again, so the chapters print the figures feed wrote, then the generator chain and a strict build.
"""
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage_a_identity_lib as LIB  # noqa: E402
from stage_a_identity_lib import ROOT, ID_DIR, LOCK, L3, SIGN_OFF  # noqa: E402

FIGS = LIB.FIGURES_PROMOTION_C
ROUND0 = LIB.FIGURES_STAGE_C
GUIDE_BUILD = HERE / "guide_build.py"
CARD = (1200, 630)
MARGIN = 72
CENTERS48 = (4.5, 23.5, 42.5)        # the 48 px master's node centers; 7 px nodes, a 9 px lever
FEED_WIDTHS = (500, 360)
MIN_RED = 4                          # Rule 08.2: the lever keeps at least four red pixels
DARK_MAX = 70                        # Rule 08.2: a near-black pixel has every channel under 70
GROUNDS = {"newsprint": (0xDC, 0xD9, 0xD2), "white": (0xFF, 0xFF, 0xFF), "charcoal": (0x12, 0x12, 0x12),
           "prussian": (0x1F, 0x2D, 0x5A)}
LIGHT = ("newsprint", "white")
NODE_INK = {"charcoal": (0xDC, 0xD9, 0xD2), "prussian": (0xFF, 0xFF, 0xFF)}
THUMB = (75, 2)                      # the thumbnail path: JPEG quality 75, chroma at half size (4:2:0), as round 0 ran it


def box(size):
    """The sign-off's top left in the card: the card's 1 px border, then the 72 px margin from the right and bottom."""
    return CARD[0] - 1 - MARGIN - size, CARD[1] - 1 - MARGIN - size


def save(key, value):
    d = json.loads(FIGS.read_text()) if FIGS.exists() else {}
    d[key] = value
    d["date"] = "2026-11-11"
    FIGS.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git_sha(rel):
    r = subprocess.run(["git", "show", f"HEAD:./{rel}"], cwd=ROOT, capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None


# ============================================================================================ minimums and specimens
def minimums():
    import stage_a_identity_s1 as S1
    S1.update_minimums()
    print("updated", S1.MIN_FILE.relative_to(ROOT))


def specimens():
    import promotion_identity as P
    P.specimens()


# ============================================================================================ counting
def counts(arr, ox, oy, s, ground, k, floor=None, block=True):
    """Rule 08.2's counts on a card reduced by s (a numpy array, H x W x 3), the sign-off at k times the 48 px master's
    grid with its top left at ox, oy in the full card. Each node's square is its 7 px (the lever's 9 px) times k, plus
    1 px on every side once reduced, as stage_a_identity_q_measure.feed_counts and round 0's counts_k count it.

    Light ground: each of the eight dark nodes keeps a pixel with every channel under 70; the lever keeps red pixels.
    Dark ground: each light node keeps a block of 2 by 2 pixels with every channel over the floor (block=True, the rule
    since promotion C), or a single such pixel (block=False, round 0's form, kept for the record); on Charcoal the lever
    counts red as on a light ground; on Prussian, where the lever is White, it is the ninth light node. best: per node,
    the darkest pixel's highest channel (light), or the brightest block's or pixel's lowest channel (dark).

    Why a block on a dark ground: there the links take the nodes' own color, and on the 96 px sign-off they are 2 px
    wide, so a reduced link can leave one pixel as bright as a node's. A link under 1 px wide once reduced cannot fill a
    block of 2 by 2; a node 4 px or more across does."""
    import numpy as np
    h, w = arr.shape[:2]
    lo_all = arr.min(axis=2).astype(int)
    kept, best, red = 0, [], 0
    for cy in CENTERS48:
        for cx in CENTERS48:
            lever = (cx, cy) == (CENTERS48[2], CENTERS48[2])
            X, Y = (ox + cx * k) * s, (oy + cy * k) * s
            r = (4.5 if lever else 3.5) * k * s + 1
            px = [tuple(int(c) for c in arr[y, x]) for x in range(int(X - r), int(X + r) + 1)
                  for y in range(int(Y - r), int(Y + r) + 1) if 0 <= x < w and 0 <= y < h]
            if lever and ground != "prussian":
                red = sum(1 for p in px if p[0] > 170 and p[1] < 120 and p[2] < 120)
                continue
            if ground in LIGHT:
                b = min(max(p) for p in px)
                best.append(b)
                kept += b < DARK_MAX
            elif block:
                x0, x1, y0, y1 = max(0, int(X - r)), min(w - 1, int(X + r)), max(0, int(Y - r)), min(h - 1, int(Y + r))
                sub = lo_all[y0:y1 + 1, x0:x1 + 1]
                blk = np.minimum(np.minimum(sub[:-1, :-1], sub[1:, :-1]), np.minimum(sub[:-1, 1:], sub[1:, 1:]))
                b = int(blk.max())
                best.append(b)
                kept += floor is not None and b > floor
            else:
                b = max(min(p) for p in px)
                best.append(b)
                kept += floor is not None and b > floor
    need = 9 if ground == "prussian" else 8
    out = {"nodes_kept": kept, "of": need, "best_per_node": best}
    if ground != "prussian":
        out["lever_red_px"] = red
    if ground in LIGHT or floor is not None:
        out["passes"] = kept == need and (ground == "prussian" or red >= MIN_RED)
    return out


def reduce(img, w, flt):
    return img.resize((w, round(CARD[1] * w / CARD[0])), flt)


def jpeg(img, q, sub):
    from PIL import Image
    b = io.BytesIO()
    img.save(b, format="JPEG", quality=q, subsampling=sub)
    b.seek(0)
    return Image.open(b).convert("RGB")


def lean(c):
    return {k: v for k, v in c.items() if k != "best_per_node"}


# ============================================================================================ captures
CARD_JS = r"""
const { chromium } = require('playwright');
const [page, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1700, height: 1000 }, deviceScaleFactor: 1 });
  await p.goto('file://' + page, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const card = p.locator('[data-oai="s-proofs-social"] .oai-stackpair > div:first-child > div').first();
  await card.scrollIntoViewIfNeeded();
  const box = await card.boundingBox();
  const lk = await card.locator('svg[aria-label="Lockmark"]').last().evaluate((e) => {
    const r = e.getBoundingClientRect(); return { viewBox: e.getAttribute('viewBox'), x: r.x, y: r.y, w: r.width, h: r.height }; });
  const clip = { x: Math.round(box.x), y: Math.round(box.y), width: 1200, height: 630 };
  await p.screenshot({ path: out, clip });
  console.log(JSON.stringify({ box, clip, lk }));
  await b.close();
})();
"""

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


def build_page(scratch):
    """The guide page as the repository builds it, into the scratch folder. Strict first; if strict stops, a plain build
    so the measure can run, with the strict build's warnings kept."""
    out = scratch / "guide.html"
    r = subprocess.run(["python3", "-I", str(GUIDE_BUILD), "--strict", "--out", str(out)], capture_output=True, text=True, cwd=ROOT)
    rec = {"strict_exit": r.returncode, "strict_tail": (r.stdout.strip().splitlines() + r.stderr.strip().splitlines())[-6:]}
    if r.returncode != 0:
        r2 = subprocess.run(["python3", "-I", str(GUIDE_BUILD), "--out", str(out)], capture_output=True, text=True, cwd=ROOT)
        rec["plain_exit"] = r2.returncode
        rep = out.with_name(out.stem + "-Build-Report.json")
        if rep.exists():
            rec["warnings"] = json.loads(rep.read_text()).get("warnings", [])[:40]
    return out, rec


def node(js, *args, cwd=None):
    r = subprocess.run(["node", str(js), *map(str, args)], check=True, capture_output=True, text=True, cwd=str(cwd or ROOT / "work/build"))
    return json.loads(r.stdout.strip().splitlines()[-1])


def links_only(m):
    """The sign-off with its nodes and lever taken out, links alone, as round 0 drew it for the floor."""
    links = re.sub(r'(<g fill="(?:currentColor|#FFFFFF)">)(?=<path)(.*?)</g>', "", m, count=1, flags=re.S)
    links = re.sub(r'<path fill="(?:var\(--lever[^"]*|#FFFFFF)"[^>]*/>(?=</svg>)', "", links, flags=re.S)
    assert links.count("<path") == 0, "the links-only drawing still draws a node"
    return links


def feed(scratch):
    import numpy as np
    from PIL import Image
    import stage_a_identity_proofs as SP
    import stage_a_identity_q_measure as QM
    scratch = Path(scratch).resolve()
    d = scratch / "feed"
    d.mkdir(parents=True, exist_ok=True)
    # ---------------------------------------------------------------- the built page's card
    page, built = build_page(scratch)
    cj = d / "card.js"
    cj.write_text(CARD_JS)
    info = node(cj, page, d / "built-card.png")
    lk = info["lk"]
    S = SIGN_OFF["social"]
    ox, oy = box(S)
    # The page's flow can set the card a fraction of a pixel off the grid; the capture's clip rounds it, as
    # stage_a_identity_q_measure.feed_test did, and the pixel check below shows whether Chromium snapped the drawing.
    got = (round(lk["x"] - info["clip"]["x"], 3), round(lk["y"] - info["clip"]["y"], 3), round(lk["w"], 3), round(lk["h"], 3))
    assert (round(got[0]), round(got[1]), got[2], got[3]) == (ox, oy, S, S), f"the built page puts the sign-off at {got}, not {(ox, oy, S, S)}"
    vb48 = re.search(r'viewBox="([^"]+)"', (ID_DIR / LOCK[48]).read_text()).group(1)
    assert lk["viewBox"] == vb48, f"the built page's sign-off has viewBox {lk['viewBox']}, not the 48 px master's {vb48}"
    # ---------------------------------------------------------------- the card alone on each ground, at 96 and 48 px
    LIB.INLINE_ALL[0] = True
    try:
        cards = {}
        for s in GROUNDS:
            for size in (S, 48):
                cards[f"card-{s}-{size}"] = f'<div id="card-{s}-{size}" style="width:1200px">{SP._social(s, sign=size)}</div>'
        tiles = {}
        for s in GROUNDS:
            m = LIB.sign_off("social", surface=s, label="Lockmark")
            tiles[f"tile-{s}"] = m
            tiles[f"tile-{s}-links"] = links_only(m)
    finally:
        LIB.INLINE_ALL[0] = False
    body = "".join(cards.values()) + "".join(
        f'<div id="{k}" class="oai-s-{k.split("-")[1]}" style="width:{S}px;height:{S}px;line-height:0;margin:8px">{v}</div>'
        for k, v in tiles.items())
    html = d / "cards.html"
    html.write_text(QM.page(body))
    sj = d / "shot.js"
    sj.write_text(SHOT_JS)
    node(sj, d, html, *cards, *tiles)
    imgs = {k: Image.open(d / f"{k}.png").convert("RGB") for k in cards}
    for k, im in imgs.items():
        assert im.size == CARD, f"{k} captured at {im.size}"
    tile = {k: np.asarray(Image.open(d / f"{k}.png").convert("RGB")) for k in tiles}
    built_img = Image.open(d / "built-card.png").convert("RGB")
    B, A = np.asarray(built_img), np.asarray(imgs[f"card-newsprint-{S}"])
    sign_same = bool((B[oy:oy + S, ox:ox + S] == A[oy:oy + S, ox:ox + S]).all())
    tile_same = {s: bool((np.asarray(imgs[f"card-{s}-{S}"])[oy:oy + S, ox:ox + S] == tile[f"tile-{s}"]).all()) for s in GROUNDS}
    diff = np.abs(B.astype(int) - A.astype(int)).max(axis=2)
    res = {"method": ("The proofs' link-preview card (stage_a_identity_proofs._social) drawn by the built guide page and drawn "
                      "alone on each ground with every master inlined, captured at 1x in Chromium through Playwright; reduced "
                      "with Pillow; counted node by node in each node's square, scaled with the sign-off, plus 1 px, as Rule "
                      "08.2 counts it"),
           "lockmark_master": LOCK[48], "sign_off_px": S, "sign_off_box_in_card": [ox, oy, S, S], "card_px": list(CARD),
           "built_page": built, "built_page_sign_off_box": list(got),
           "built_page_sign_off_same_pixels_as_card_alone": sign_same,
           "built_page_card_pixels_differing_from_card_alone": int((diff > 0).sum()),
           "card_sign_off_same_pixels_as_tile_alone": tile_same}
    assert sign_same, "the built page and the card drawn alone put different pixels in the sign-off"
    assert all(tile_same.values()), f"a card's sign-off differs from the tile drawn alone: {tile_same}"
    flts = {"lanczos": Image.LANCZOS, "bicubic": Image.BICUBIC, "bilinear": Image.BILINEAR, "box": Image.BOX}

    def flat(s, t, size):
        a = np.empty((CARD[1], CARD[0], 3), dtype=np.uint8)
        a[:] = GROUNDS[s]
        x, y = box(size)
        a[y:y + size, x:x + size] = t
        return Image.fromarray(a)

    # ---------------------------------------------------------------- the floors on the 96 px drawing
    # The rule's method (round 0): halfway between the brightest the links alone leave in a node's square and the dimmest
    # node's brightest, at the rule's two widths under four filters, rounded down to 5. Measured with single pixels
    # (round 0's form, the record) and with blocks of 2 by 2 (the form the rule takes for the 96 px sign-off).
    k = S // 48
    floor_study, floors, floors_single = {}, {}, {}
    for s in ("charcoal", "prussian"):
        links, whole = flat(s, tile[f"tile-{s}-links"], S), flat(s, tile[f"tile-{s}"], S)
        floor_study[s] = {}
        for form, blk in (("block_2_by_2", True), ("single_pixel", False)):
            row = {"at_rule_widths": {}, "band_300_to_600": {"links_alone_max": 0, "weakest_node_min": 255,
                                                              "widths_where_a_node_falls_to_the_links": []}}
            lk_r, nd_r = 0, 255
            for w in range(300, 601):
                sc = w / CARD[0]
                lkv = max(max(counts(np.asarray(reduce(links, w, f)), ox, oy, sc, s, k, floor=255, block=blk)["best_per_node"]) for f in flts.values())
                ndv = min(min(counts(np.asarray(reduce(whole, w, f)), ox, oy, sc, s, k, floor=0, block=blk)["best_per_node"]) for f in flts.values())
                bnd = row["band_300_to_600"]
                bnd["links_alone_max"] = max(bnd["links_alone_max"], lkv)
                bnd["weakest_node_min"] = min(bnd["weakest_node_min"], ndv)
                if ndv <= lkv:
                    bnd["widths_where_a_node_falls_to_the_links"].append(w)
                if w in FEED_WIDTHS:
                    row["at_rule_widths"][str(w)] = {"links_alone_max": lkv, "weakest_node_min": ndv}
                    lk_r, nd_r = max(lk_r, lkv), min(nd_r, ndv)
            fv = int((lk_r + nd_r) / 2 // 5 * 5)
            row["floor_by_the_rule's_method"] = fv
            row["separates_at_rule_widths"] = lk_r < nd_r
            row["floor_share_of_the_way_from_ground_to_node"] = round((fv - min(GROUNDS[s])) / (min(NODE_INK[s]) - min(GROUNDS[s])), 3)
            floor_study[s][form] = row
            (floors if blk else floors_single)[s] = fv
    for s in LIGHT:
        links = flat(s, tile[f"tile-{s}-links"], S)
        low = 255
        for w in range(300, 601):
            for f in flts.values():
                low = min(low, min(counts(np.asarray(reduce(links, w, f)), ox, oy, w / CARD[0], s, k)["best_per_node"]))
        floor_study[s] = {"links_alone_darkest_high_channel_300_to_600": low, "under_70": low < DARK_MAX}
    r0 = json.loads(ROUND0.read_text()).get("feed", {}).get("light_floor", {}) if ROUND0.exists() else {}
    res["floors"] = floors
    res["floors_single_pixel_on_the_96_px_card"] = floors_single
    res["floors_round_0_on_the_48_px_card"] = r0
    res["floor_study"] = floor_study

    # ---------------------------------------------------------------- the rule's widths, four filters
    at = {}
    for s in GROUNDS:
        im = imgs[f"card-{s}-{S}"]
        at[s] = {}
        for w in FEED_WIDTHS:
            for name, f in flts.items():
                at[s].setdefault(f"at_{w}", {})[name] = counts(np.asarray(reduce(im, w, f)), ox, oy, w / CARD[0], s, k, floor=floors.get(s))
            sm = reduce(im, w, Image.LANCZOS)
            sc = w / CARD[0]
            bx = (int(ox * sc) - 2, int(oy * sc) - 2, int((ox + S) * sc + 0.999) + 2, int((oy + S) * sc + 0.999) + 2)
            sm.crop(bx).resize(((bx[2] - bx[0]) * 8, (bx[3] - bx[1]) * 8), Image.NEAREST).save(d / f"feed-{s}-{w}@8x.png")
    res["at_rule_widths"] = at
    # the built page's own card, Newsprint, Lanczos: the figures the guide prints for "our card"
    built_at = {f"at_{w}": counts(np.asarray(reduce(built_img, w, Image.LANCZOS)), ox, oy, w / CARD[0], "newsprint", k)
                for w in FEED_WIDTHS}
    res["built_page_at_rule_widths"] = built_at

    # ---------------------------------------------------------------- the thumbnail path, 48 and 96 px
    thumb = {}
    for s in GROUNDS:
        for size in (48, S):
            im = imgs[f"card-{s}-{size}"]
            x, y = box(size)
            row = {}
            for w in FEED_WIDTHS:
                sm = reduce(im, w, Image.LANCZOS)
                row[f"at_{w}"] = lean(counts(np.asarray(jpeg(sm, *THUMB)), x, y, w / CARD[0], s, size // 48, floor=floors.get(s)))
            fails = [w for w in range(300, 601, 4)
                     if not counts(np.asarray(jpeg(reduce(im, w, Image.LANCZOS), *THUMB)), x, y, w / CARD[0], s, size // 48,
                                   floor=floors.get(s))["passes"]]
            row["fail_widths_every_4th_300_to_600"] = {"fails": len(fails), "of": len(range(300, 601, 4)), "widths": fails}
            thumb.setdefault(s, {})[str(size)] = row
    res["thumbnail"] = thumb

    # ---------------------------------------------------------------- every width from 300 to 600 px, Lanczos
    widths = {}
    for s in GROUNDS:
        rows = []
        for w in range(300, 601):
            c = counts(np.asarray(reduce(imgs[f"card-{s}-{S}"], w, Image.LANCZOS)), ox, oy, w / CARD[0], s, k, floor=floors.get(s))
            rows.append((w, c["nodes_kept"], c.get("lever_red_px"), c.get("passes")))
        reds = [r[2] for r in rows if r[2] is not None]
        widths[s] = {"fail_widths": [r[0] for r in rows if not r[3]], "nodes_min": min(r[1] for r in rows),
                     "lever_red_min": min(reds) if reds else None, "lever_red_max": max(reds) if reds else None}
    res["widths_300_to_600"] = widths
    save("feed_study", res)

    # ---------------------------------------------------------------- the keys the chapters print
    save("feed", {"source": "work/build/scripts/phase-2/promotion_c_identity.py feed, key feed_study, built_page_at_rule_widths",
                  "lockmark_master": LOCK[48], "sign_off_px": S, "filter": "lanczos", "card": "the built guide page, Newsprint",
                  **{w: {"dark_nodes_kept": c["nodes_kept"], "lever_red_px": c["lever_red_px"], "passes": c["passes"]}
                     for w, c in built_at.items()}})
    dark = {"source": "work/build/scripts/phase-2/promotion_c_identity.py feed, key feed_study, at_rule_widths and floors",
            "lockmark_master": LOCK[48], "sign_off_px": S, "floors": floors, "filter": "lanczos", "dark_unit": "block of 2 by 2 pixels",
            "floor_study": {g: {w: floor_study[g]["block_2_by_2"]["at_rule_widths"][w] for w in ("500", "360")} for g in ("charcoal", "prussian")}}
    for s in GROUNDS:
        dark[s] = {w: {x: c["lanczos"][x] for x in ("nodes_kept", "of", "lever_red_px", "passes") if x in c["lanczos"]}
                   for w, c in at[s].items()}
    save("feed_dark", dark)
    save("feed_thumbnail", {"source": "work/build/scripts/phase-2/promotion_c_identity.py feed, key feed_study, thumbnail",
                            "lockmark_master": LOCK[48], "sign_off_px": S, "jpeg": "quality 75, chroma 4:2:0, after a Lanczos reduction",
                            **{s: {size: {w: v[w] for w in ("at_500", "at_360")} for size, v in t.items()} for s, t in thumb.items()}})
    return res


# ============================================================================================ hashes
def hashes():
    out = {}
    r0 = json.loads(ROUND0.read_text())["proposals"]["print_l3"] if ROUND0.exists() else {}
    for rel in (L3["print"], "prussian/" + Path(L3["print"]).stem + "-Prussian-White.svg", L3["today"],
                "prussian/" + Path(L3["today"]).stem + "-Prussian-White.svg", LOCK[48],
                "prussian/" + Path(LOCK[48]).stem + "-Prussian-White.svg"):
        p = ID_DIR / rel
        out[rel] = {"sha256": sha(p), "same_as_head": sha(p) == git_sha(LIB.rel(p))}
        if rel in r0:
            out[rel]["round_0_figures"] = {k: r0[rel][k] for k in ("lockmark_units", "width_units", "lockmark_over_capitals")}
            vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', p.read_text()).group(1).split()]
            out[rel]["viewBox"] = vb
            out[rel]["viewBox_matches_round_0"] = abs(vb[2] - r0[rel]["width_units"]) < 0.01 and abs(vb[3] - r0[rel]["lockmark_units"]) < 0.01
    save("hashes", out)
    return out


# ============================================================================================ plates
PLATES_JS = r"""
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
(async () => {
  const b = await chromium.launch();
  const res = { plates: {}, rules: {}, kicker: {} };
  for (const [w, scale] of [[1440, 1], [390, 1], [1440, 2], [390, 2]]) {
    const p = await b.newPage({ viewport: { width: w, height: 1000 }, deviceScaleFactor: scale });
    await p.goto('file://' + job.page, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.addStyleTag({ content: 'header, .masthead, [class*="masthead"] { visibility: hidden !important }' });
    for (const sid of job.plates) {
      const fig = p.locator(`#fig-${sid}`);
      if (!(await fig.count())) { res.plates[`${sid}@${w}@${scale}x`] = null; continue; }
      await fig.scrollIntoViewIfNeeded();
      const f = path.join(job.out, `plate-${sid}-${w}@${scale}x.png`);
      await fig.screenshot({ path: f });
      const bb = await fig.boundingBox();
      const over = await fig.evaluate((e) => { const s = e.querySelector('.plate__stage, [class*="stage"]') || e; return { sw: s.scrollWidth, cw: s.clientWidth }; });
      res.plates[`${sid}@${w}@${scale}x`] = { file: f, w: bb.width, h: bb.height, stage: over };
    }
    if (scale === 1) {
      for (const rid of job.rules) {
        const r = p.locator(`#rule-${rid}`);
        if (!(await r.count())) { res.rules[`${rid}@${w}`] = null; continue; }
        await r.scrollIntoViewIfNeeded();
        const f = path.join(job.out, `rule-${rid}-${w}.png`);
        await r.screenshot({ path: f });
        res.rules[`${rid}@${w}`] = f;
      }
    }
    // the kicker's 24 px icon: which <use> shows, and what it draws
    const k = p.locator('[data-specimen="s-01-21-correct"] svg[data-icon="CL-057"], #fig-s-01-21-correct svg[data-icon="CL-057"]').first();
    if (await k.count()) {
      await k.scrollIntoViewIfNeeded();
      const info = await k.evaluate((e) => [...e.querySelectorAll('use')].map((u) => ({ cls: u.getAttribute('class'), href: u.getAttribute('href'),
        display: getComputedStyle(u).display, target: !!document.querySelector(u.getAttribute('href')) })));
      const f = path.join(job.out, `kicker-${w}@${scale}x.png`);
      const bb = await k.boundingBox();
      await p.screenshot({ path: f, clip: { x: bb.x - 4, y: bb.y - 4, width: 220, height: bb.height + 8 } });
      res.kicker[`${w}@${scale}x`] = { uses: info, file: f, box: bb };
    }
    await p.close();
  }
  await b.close();
  fs.writeFileSync(path.join(job.out, 'plates.json'), JSON.stringify(res, null, 1));
})();
"""
PLATES = ["s-08-2-correct", "s-proofs-social", "s-03-minimums", "s-01-21-correct"]
RULES = ["03-2", "03-4", "03-6", "08-1", "08-2"]


def plates(scratch):
    scratch = Path(scratch).resolve()
    page = scratch / "guide.html"
    assert page.exists(), "build the page first (feed DIR builds it)"
    out = scratch / "plates"
    out.mkdir(parents=True, exist_ok=True)
    job = scratch / "plates-job.json"
    job.write_text(json.dumps({"page": str(page), "plates": PLATES, "rules": RULES, "out": str(out)}))
    js = scratch / "plates.js"
    js.write_text(PLATES_JS)
    subprocess.run(["node", str(js), str(job)], check=True, cwd=str(ROOT / "work/build"))
    res = json.loads((out / "plates.json").read_text())
    save("plates", {k: ({kk: vv for kk, vv in v.items() if kk != "file"} if isinstance(v, dict) else v) for k, v in res["plates"].items()})
    save("kicker", {k: {"uses": v["uses"]} for k, v in res["kicker"].items()})
    return res


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what == "minimums":
        minimums()
    elif what == "specimens":
        specimens()
    elif what == "feed" and len(sys.argv) > 2:
        f = feed(sys.argv[2])
        print(json.dumps({k: f[k] for k in ("built_page_sign_off_box", "built_page_sign_off_same_pixels_as_card_alone",
                                            "card_sign_off_same_pixels_as_tile_alone", "floors", "floors_single_pixel_on_the_96_px_card",
                                            "floors_round_0_on_the_48_px_card", "built_page_at_rule_widths")}, indent=1, default=str)[:4000])
        print("strict build:", f["built_page"]["strict_exit"], len(f["built_page"].get("warnings", [])), "warnings")
        print("floor study:", json.dumps({g: {fm: {x: (y if x != "band_300_to_600" else {q: (len(z) if isinstance(z, list) else z) for q, z in y.items()})
                                                    for x, y in r.items()} for fm, r in v.items()} if "block_2_by_2" in v else v
                                          for g, v in f["floor_study"].items()}, indent=1))
        print("lanczos:", {s: {w: lean(v[w]["lanczos"]) for w in v} for s, v in f["at_rule_widths"].items()})
        print("thumbnail:", json.dumps({s: {z: {w: t[w] for w in ("at_500", "at_360")} for z, t in v.items()} for s, v in f["thumbnail"].items()}))
        print("thumbnail fails:", {s: {z: t["fail_widths_every_4th_300_to_600"]["fails"] for z, t in v.items()} for s, v in f["thumbnail"].items()})
        print("widths:", {s: (len(v["fail_widths"]), v["lever_red_min"]) for s, v in f["widths_300_to_600"].items()})
    elif what == "hashes":
        print(json.dumps(hashes(), indent=1))
    elif what == "plates" and len(sys.argv) > 2:
        r = plates(sys.argv[2])
        print(json.dumps(r["kicker"], indent=1))
        print({k: (v and (v["w"], v["h"], v["stage"])) for k, v in r["plates"].items()})
    else:
        print(__doc__)
        sys.exit(2)
