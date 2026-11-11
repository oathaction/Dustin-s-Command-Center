"""Stage C, round 1, November 11, 2026: the identity designer's checks for Rule 17.6 and the Rule 12.4 proposal for board C.

Under work/handoffs/phase-2/20261111_Stage-C-Round-1-Brief.md and the main session's round 1 task. Figures go to
work/handoffs/phase-2/20261111_Stage-C-Round-1-Identity-Figures.json, one key per step.

  ch17 PAGE DIR  Checks Rule 17.6's two players in a built guide page (stage_c_identity_ch17.py makes them; chapter 17's
                 maker places them): at 1440 and 390 px, 1x and 2x, with and without reduced motion. Nothing moves on
                 load; Play runs once and ends on the end frame; Reset returns to the first frame; under reduced motion
                 Play draws the end frame at once with Slow motion unavailable. Compares, pixel for pixel, the moving
                 layer's last keyframe with the end frame, and the moving layer at rest (no animation) with the master;
                 counts the 48 px lockmark's colors in its end frame; checks that each end-layer drawing in the page is
                 its master file's drawing. Writes key ch17.
  rule-12-4 DIR  Rule 12.4's rewrite for board C (the creative director's review, "For board C"). Measures the large
                 crop of B on the 360 px Report 3 cover at every height from 180 to 320 px in 4 px steps, at Rule 04.8's
                 proportions: the share of B's ink outside the cover, whether what stays inside is one piece (and at
                 every offset within 4 px for the height chosen), and the clearance from B's ink to the words against
                 the body text's line height. Writes key rule_12_4, then the comparison page
                 work/handoffs/phase-2/stage-c-identity/20261111_Rule-12-4-Comparison.html with its captures at 1x
                 and 2x: today's rule and the rewrite side by side at 360 px. Chapter 12 does not change.

Run: python3 -I work/build/scripts/phase-2/stage_c_identity_round1.py ch17 <built page> <scratch dir> | rule-12-4 <scratch dir>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage_a_identity_lib as LIB  # noqa: E402
from stage_a_identity_lib import ROOT, ID_DIR, AMP, E  # noqa: E402

FIGS = ROOT / "work/handoffs/phase-2/20261111_Stage-C-Round-1-Identity-Figures.json"
PLATES = ROOT / "work/handoffs/phase-2/stage-c-identity"


def save(key, value):
    d = json.loads(FIGS.read_text()) if FIGS.exists() else {}
    d[key] = value
    d["date"] = "2026-11-11"
    FIGS.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")


def node(js_text, scratch, *args):
    js = Path(scratch) / "run.js"
    js.write_text(js_text)
    r = subprocess.run(["node", str(js), *map(str, args)], check=True, capture_output=True, text=True, cwd=str(ROOT / "work/build"))
    return r.stdout


# ============================================================================================ ch17
CH17_JS = r"""
const fs = require('fs'); const path = require('path'); const { chromium } = require('playwright');
const [page, out] = process.argv.slice(2);
const SIDS = ['s-17-hinge-correct', 's-17-lever-correct'];
(async () => {
  const b = await chromium.launch(); const res = {};
  for (const [w, sc] of [[1440, 1], [1440, 2], [390, 1], [390, 2]]) {
    for (const rm of ['no-preference', 'reduce']) {
      const ctx = await b.newContext({ viewport: { width: w, height: 1100 }, deviceScaleFactor: sc, reducedMotion: rm });
      const p = await ctx.newPage();
      await p.goto('file://' + page, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
      for (const sid of SIDS) {
        const key = `${sid}@${w}@${sc}x@${rm}`; const r = res[key] = {};
        const P = p.locator(`[data-specimen="${sid}"] [data-oa-motion]`);
        await P.scrollIntoViewIfNeeded(); await p.waitForTimeout(300);
        r.onLoad = await P.evaluate((el) => ({ frame: el.getAttribute('data-frame'), anims: el.getAnimations({ subtree: true }).length }));
        const boxes = P.locator('.oai-mv-grounds .oai-mv-box'); const n = await boxes.count(); const vis = [];
        for (let i = 0; i < n; i++) if (await boxes.nth(i).isVisible()) vis.push(i);
        r.cells = vis.length;
        const shot = async (tag) => { for (const [k, i] of vis.entries()) await boxes.nth(i).screenshot({ path: path.join(out, `${sid}-${w}-${sc}x-${rm}-${tag}-${k}.png`) }); };
        await shot('start');
        r.resetAtStart = await P.locator('[data-oa-reset]').getAttribute('aria-disabled');
        await P.locator('[data-oa-play]').click();
        if (rm === 'no-preference') {
          r.afterClick = await P.evaluate((el) => { const A = el.getAnimations({ subtree: true });
            const ends = A.map((a) => a.effect.getComputedTiming().endTime);
            A.forEach((a) => { a.pause(); a.currentTime = a.effect.getComputedTiming().endTime; });
            return { frame: el.getAttribute('data-frame'), anims: A.length, endMax: Math.round(Math.max(...ends)), word: el.querySelector('[data-word]').textContent }; });
          await p.waitForTimeout(100); await shot('runfinal');
          await P.evaluate((el) => el.getAnimations({ subtree: true }).forEach((a) => a.play()));
          await p.waitForFunction((s) => document.querySelector(`[data-specimen="${s}"] [data-oa-motion]`).getAttribute('data-frame') === 'end', sid, { timeout: 5000 });
        } else {
          r.afterClick = await P.evaluate((el) => ({ frame: el.getAttribute('data-frame'), anims: el.getAnimations({ subtree: true }).length,
            slowUnavailable: el.querySelector('input[data-slow]').getAttribute('aria-disabled'), why: el.querySelector('[data-why]').textContent,
            tokens: ['hinge', 'lever', 'standard', 'slow', 'stagger'].map((t) => getComputedStyle(el).getPropertyValue('--oa-motion-duration-' + t).trim()) }));
        }
        await p.waitForTimeout(100); await shot('end');
        r.atEnd = await P.evaluate((el) => ({ frame: el.getAttribute('data-frame'), anims: el.getAnimations({ subtree: true }).length,
          status: el.querySelector('[data-out]').textContent, word: el.querySelector('[data-word]').textContent,
          endSvgs: [...el.querySelectorAll('.oai-mv-grounds [data-layer="end"] svg')].map((s) => s.outerHTML) }));
        await P.locator('[data-oa-reset]').click(); await p.waitForTimeout(100);
        r.afterReset = await P.evaluate((el) => ({ frame: el.getAttribute('data-frame'), anims: el.getAnimations({ subtree: true }).length }));
        await shot('reset');
        if (rm === 'no-preference' && w === 1440) {   // the moving layer at rest, no animation, every part shown
          await P.evaluate((el) => { el.setAttribute('data-frame', 'still'); el.querySelectorAll('[data-part]').forEach((e) => { e.style.visibility = 'visible'; }); });
          await p.waitForTimeout(100); await shot('static');
          await P.evaluate((el) => { el.querySelectorAll('[data-part]').forEach((e) => { e.style.visibility = ''; }); el.setAttribute('data-frame', 'end'); });
          await p.waitForTimeout(100); await shot('endlayer');
          await P.evaluate((el) => el.setAttribute('data-frame', 'start'));
        }
      }
      await ctx.close();
    }
  }
  fs.writeFileSync(path.join(out, 'ch17.json'), JSON.stringify(res, null, 1)); await b.close();
})();
"""


def _diff(a, b):
    import numpy as np
    from PIL import Image
    A, B = (np.asarray(Image.open(x).convert("RGB")).astype(int) for x in (a, b))
    if A.shape != B.shape:
        return {"same": False, "sizes": [list(A.shape), list(B.shape)]}
    d = abs(A - B).max(axis=2)
    return {"same": bool(d.max() == 0), "pixels_differing": int((d > 0).sum()), "max_levels": int(d.max()), "of": int(d.size)}


def ch17(page, scratch):
    import numpy as np
    from PIL import Image
    out = Path(scratch).resolve() / "ch17"
    out.mkdir(parents=True, exist_ok=True)
    node(CH17_JS, out, Path(page).resolve(), out)
    raw = json.loads((out / "ch17.json").read_text())
    masters = {"wordmark/20261028_Wordmark-24px-Master.svg", "wordmark/20261028_Wordmark-Display-Master.svg",
               "lockmark/20261109_Lockmark-48px-Master-Outline.svg", "lockmark/20261107_Lockmark-Display-Master.svg"}

    def inner(t):
        t = re.sub(r"<title>.*?</title>", "", t, flags=re.S)
        t = t[re.match(r"<svg\b[^>]*>", t).end():t.rindex("</svg>")]
        return re.sub(r"\s+", " ", re.sub(r"<(\w+)([^>]*?)\s*/>", r"<\1\2></\1>", t)).strip()
    mi = {m: inner((ID_DIR / m).read_text()) for m in masters}
    res = {}
    for k, r in raw.items():
        sid, w, sc, rm = k.split("@")
        pre = f"{sid}-{w}-{sc}-{rm}"
        row = {"on_load": r["onLoad"], "reset_unavailable_at_start": r["resetAtStart"] == "true", "after_play": r["afterClick"],
               "at_end": {x: y for x, y in r["atEnd"].items() if x != "endSvgs"}, "after_reset": r["afterReset"], "cells": r["cells"],
               "end_layer_is_its_master": [next((m for m in masters if mi[m] == inner(s)), None) for s in r["atEnd"]["endSvgs"]]}
        cells = range(r["cells"])
        row["reset_equals_first_frame"] = [_diff(out / f"{pre}-reset-{i}.png", out / f"{pre}-start-{i}.png")["same"] for i in cells]
        if rm == "no-preference":
            row["last_keyframe_vs_end_frame"] = [_diff(out / f"{pre}-runfinal-{i}.png", out / f"{pre}-end-{i}.png") for i in cells]
            if w == "1440":
                row["moving_layer_at_rest_vs_master"] = [_diff(out / f"{pre}-static-{i}.png", out / f"{pre}-endlayer-{i}.png") for i in cells]
            if sid == "s-17-lever-correct":
                row["lockmark_48_end_frame_colors"] = [len({tuple(c) for c in np.asarray(Image.open(out / f"{pre}-end-{i}.png").convert("RGB")).reshape(-1, 3)})
                                                       for i in cells if i in (0, 2)]
        res[k] = row
    save("ch17", res)
    return res


# ============================================================================================ rule 12.4
CROP_JS = r"""
const fs = require('fs'); const path = require('path'); const { chromium } = require('playwright');
const [html, out] = process.argv.slice(2);
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 1 });
  await p.goto('file://' + html, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const ids = await p.evaluate(() => [...document.querySelectorAll('[data-cell]')].map((e) => e.id));
  const info = {};
  for (const id of ids) {
    const el = p.locator('#' + id); await el.scrollIntoViewIfNeeded(); await el.screenshot({ path: path.join(out, id + '.png') });
    info[id] = await el.evaluate((c) => { const o = c.getBoundingClientRect(); const rects = [];
      c.querySelectorAll('[data-words] p').forEach((pp) => { const rg = document.createRange(); rg.selectNodeContents(pp);
        [...rg.getClientRects()].forEach((q) => rects.push([q.left - o.left, q.top - o.top, q.right - o.left, q.bottom - o.top])); });
      const par = c.querySelector('.p12-par'); return { rects, lineHeight: par ? parseFloat(getComputedStyle(par).lineHeight) : null }; });
  }
  fs.writeFileSync(path.join(out, 'cells.json'), JSON.stringify(info)); await b.close(); })();
"""
SPARE = 2                        # px of clearance over the line height, for type that renders a little differently
NEWSPRINT = (0xDC, 0xD9, 0xD2)
CHARCOAL = (0x12, 0x12, 0x12)


def _ink(img):
    """Coverage of the surface's ink, 0 to 1, per pixel (B is drawn in Charcoal on Newsprint)."""
    import numpy as np
    a = np.asarray(img.convert("RGB")).astype(float)
    span = max(abs(x - y) for x, y in zip(NEWSPRINT, CHARCOAL))
    return np.clip(np.abs(a - np.array(NEWSPRINT)).max(axis=2) / span, 0, 1)


def _pieces(cov, thr=0.5):
    from scipy import ndimage
    lab, n = ndimage.label(cov >= thr)
    return n


def _sid(dx, dy):
    return f"s{str(dx).replace('-', 'm')}_{str(dy).replace('-', 'm')}"


def rule_12_4(scratch):
    import numpy as np
    from PIL import Image
    import stage_b_identity_ch12 as C12
    import stage_a_identity_q_measure as QM
    out = Path(scratch).resolve() / "rule-12-4"
    out.mkdir(parents=True, exist_ok=True)
    sizes = list(range(180, 324, 4))
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', (ID_DIR / AMP["display"]).read_text()).group(1).split()]
    cells = []
    LIB.INLINE_ALL[0] = True
    try:
        for h in sizes:
            cov_html = C12.cover_signed(h)
            # the cover with its words marked for the measure, and the same cover with the words hidden
            words = cov_html.replace('<div style="position:relative;padding:32px 32px 0">',
                                     '<div data-words="" style="position:relative;padding:32px 32px 0">', 1)
            assert words != cov_html
            cells.append(f'<div id="c-{h}" data-cell="" style="width:360px;margin:8px">{words}</div>')
            cells.append(f'<div id="b-{h}" data-cell="" style="width:360px;margin:8px">'
                         f'{words.replace("data-words=\"\" style=\"", "data-words=\"\" style=\"visibility:hidden;", 1)}</div>')
            b_w = h * vb[2] / vb[3]
            cells.append(f'<div id="u-{h}" data-cell="" style="display:inline-block;padding:8px;background:var(--oa-color-surface-newsprint);line-height:0">'
                         f'{LIB.mark(AMP["display"], h=h, mode="ink", decorative=True)}</div>')
        best = None
    finally:
        LIB.INLINE_ALL[0] = False
    html = out / "crop.html"
    html.write_text(QM.page("".join(cells)))
    node(CROP_JS, out, html, out)
    info = json.loads((out / "cells.json").read_text())
    rows = {}
    for h in sizes:
        inside = _ink(Image.open(out / f"b-{h}.png"))
        total = _ink(Image.open(out / f"u-{h}.png")).sum()
        share_out = 1 - inside.sum() / total
        ys, xs = np.nonzero(inside >= 0.5)
        rects = info[f"c-{h}"]["rects"]
        lh = info[f"c-{h}"]["lineHeight"]
        # the shortest distance from any of B's ink pixels inside the cover to the words' line boxes
        dmin = 1e9
        for x0, y0, x1, y1 in rects:
            dx = np.maximum(np.maximum(x0 - (xs + 0.5), (xs + 0.5) - x1), 0)
            dy = np.maximum(np.maximum(y0 - (ys + 0.5), (ys + 0.5) - y1), 0)
            dmin = min(dmin, float(np.sqrt(dx * dx + dy * dy).min()))
        rows[str(h)] = {"ink_outside_share": round(float(share_out), 3), "pieces_inside": _pieces(inside),
                        "clearance_px": round(dmin, 1), "body_line_height_px": lh,
                        "passes": 0.25 <= share_out <= 0.40 and _pieces(inside) == 1 and dmin >= lh + SPARE}
    ok = [h for h in sizes if rows[str(h)]["passes"]]
    best = max(ok) if ok else None
    res = {"method": ("The Report 3 cover from stage_b_identity_ch12.cover_signed at each height of B, rendered at 1x in "
                      "Chromium; B alone unclipped for its whole ink; the cover with its words hidden for the ink inside; "
                      "ink = coverage of Charcoal over Newsprint; pieces = 8-way-free connected regions at half coverage; "
                      "clearance = the shortest distance from B's ink inside the cover to the words' line boxes"),
           "proportions": {"right_past_edge_share_of_width": round(C12.CROP_RIGHT, 4), "foot_past_edge_share_of_height": round(C12.CROP_FOOT, 4)},
           "rule_04_8": {"outside_share": [0.25, 0.40], "pieces": 1, "clearance": "the body text's line height",
                         "spare_px_over_line_height": SPARE},
           "by_height": rows, "largest_that_passes": best, "in_generator": C12.CROP_B_H}
    if best:
        # the chosen height at every offset within 4 px: one piece inside, every time
        shifts = {}
        for dx in (-4, 0, 4):
            for dy in (-4, 0, 4):
                shifts[f"{dx},{dy}"] = None
        cells2 = []
        LIB.INLINE_ALL[0] = True
        try:
            base = C12.crop_b(best)
            m = re.search(r"right:(-?[\d.]+)px;bottom:(-?[\d.]+)px", base)
            r0, b0 = float(m.group(1)), float(m.group(2))
            for k in shifts:
                dx, dy = map(int, k.split(","))
                cr = base.replace(m.group(0), f"right:{r0 - dx:.2f}px;bottom:{b0 - dy:.2f}px", 1)
                cells2.append(f'<div id="{_sid(dx, dy)}" data-cell="" style="width:360px;margin:8px">'
                              f'<div class="oai-s-newsprint" style="position:relative;width:360px;height:466px;overflow:hidden">{cr}</div></div>')
        finally:
            LIB.INLINE_ALL[0] = False
        html2 = out / "shifts.html"
        html2.write_text(QM.page("".join(cells2)))
        node(CROP_JS, out, html2, out)
        for k in shifts:
            dx, dy = k.split(",")
            shifts[k] = _pieces(_ink(Image.open(out / f"{_sid(int(dx), int(dy))}.png")))
        res["chosen_height_pieces_at_offsets_within_4_px"] = shifts
    save("rule_12_4", res)
    return res


# ------------------------------------------------------------------------------------------------ the comparison page
PAGE_CSS = (
    "body{margin:0;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);"
    "font:var(--oa-type-body)}main{padding:40px 32px 64px;max-width:1000px}"
    "h1{font:var(--oa-type-h3);margin:0 0 12px}h2{font:var(--oa-type-h4);margin:40px 0 8px}"
    "p{margin:0 0 12px;max-width:68ch}.k{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);"
    "text-transform:uppercase;color:var(--oa-color-text-secondary-on-newsprint);margin:0 0 6px}"
    ".cols{display:grid;grid-template-columns:repeat(2,360px);gap:48px;align-items:start;margin-top:24px}"
    ".col{display:grid;gap:16px;width:360px}.rt{font:var(--oa-type-h4);font-size:1.25rem}"
    ".small{font:var(--oa-type-body-small)}.cap{font:var(--oa-type-caption);color:var(--oa-color-text-secondary-on-newsprint)}"
    ".plate{display:grid;gap:8px}.plate .k{margin:0}"
    ".plate .oai{width:360px;outline:1px solid var(--oa-color-border-strong-on-newsprint)}"
    "ul{margin:0;padding-left:1.2em;max-width:68ch}li{margin:0 0 4px}"
    "table{border-collapse:collapse;font:var(--oa-type-body-small)}td,th{text-align:left;vertical-align:top;padding:6px 12px 6px 0;"
    "border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint)}")


def _illus_css():
    """The shell's Illustrative label, read from the guide's stylesheet, so the standalone page draws it as the guide does."""
    css = (ROOT / "work/build/guide/shell/guide-shell.css").read_text()
    return "".join(re.findall(r"^\.illus\b[^{]*\{[^}]*\}", css, flags=re.M))


def comparison(scratch):
    import stage_b_identity_ch12 as C12
    f = json.loads(FIGS.read_text())["rule_12_4"]
    assert f["largest_that_passes"] == C12.CROP_B_H, f"set CROP_B_H to {f['largest_that_passes']}, the height the measure chose"
    row = f["by_height"][str(C12.CROP_B_H)]
    chap = json.loads((ROOT / "work/build/guide/chapters/12-graphic-devices.json").read_text())
    today = next(r for r in chap["rules"] if r["id"] == "12.4")
    man = json.loads((ROOT / "work/build/guide/specimens/manifest-identity.json").read_text())
    R = C12.REWRITE_12_4
    LIB.INLINE_ALL[0] = True
    try:
        t_ok, t_fail = C12.cover(), f'{LIB.dnp()}{C12.cover(behind=True)}'
        n_ok, n_fail = C12.rewrite_plates()
    finally:
        LIB.INLINE_ALL[0] = False

    def paras(x):
        return "".join(f"<p class=\"small\">{p}</p>" for p in (x if isinstance(x, list) else [x]))

    def col(kind, title, rule, why, basis, ok, ok_cap, fail, fail_cap, specs):
        sp = "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in specs)
        return (f'<div class="col"><p class="k">{kind}</p><p class="rt">{title}</p>{paras(rule)}'
                f'<p class="k">Why it works</p>{paras(why)}<p class="cap">Basis: {E(basis)}</p>'
                f'<div class="plate"><p class="k">Correct application</p><div class="oai">{ok}</div><p class="cap">{ok_cap}</p></div>'
                f'<div class="plate"><p class="k">Failure case</p><div class="oai">{fail}</div><p class="cap">{fail_cap}</p></div>'
                f'<p class="k">Specifications</p><table>{sp}</table></div>')
    spec_today = [(s["label"], s["value"]) for s in today["specs"]]
    body = (
        '<h1>Rule 12.4: keep the hinge arcs, or retire them</h1>'
        '<p>Proposed for board C, for Dustin’s call by name: Gate 1 approved patterns at 12 percent ink (Y6), and Master '
        'Brief section 12 lists restrained patterns derived from the identity. The creative director’s review of November '
        '11 recommends retiring the hinge arcs and rewriting Rule 12.4 as the rule for open areas: leave them plain, or sign '
        'them with the large crop of B or a watermark. Today’s rule stands at left as the guide prints it; the rewrite stands '
        'at right, with its words in draft for the editor. Both covers are invented and labeled Illustrative, and each plate '
        'is at true size, 360 px wide.</p>'
        '<div class="cols">'
        + col("Today", today["title"], today["rule"], today["why"]["text"], today["why"]["basis"], t_ok, today["correct"]["caption"],
              t_fail, today["failure"]["caption"], spec_today)
        + col("Proposed", R["title"], R["rule"], R["why"], R["basis"], n_ok, R["correct"], n_fail, R["failure"], R["specs"])
        + '</div>'
        '<h2>The crop on this cover</h2>'
        f'<p>B’s display master at {C12.CROP_B_H}{LIB.NBSP if hasattr(LIB, "NBSP") else " "}px tall, in the cover’s ink, at Rule 04.8’s proportions as '
        f'Rule 04.8’s own plate sets them: {round(C12.CROP_RIGHT * 100, 1)} percent of B’s width past the right edge and '
        f'{round(C12.CROP_FOOT * 100, 1)} percent of its height past the foot. Measured on a 1x render: '
        f'{round(row["ink_outside_share"] * 100, 1)} percent of B’s ink falls outside the cover, within Rule 04.8’s 25 to 40 '
        f'percent; what stays inside is one piece, at this place and at every offset within 4 px; and B’s ink stands '
        f'{row["clearance_px"]:g} px from the words, over the body text’s {row["body_line_height_px"]:g} px line height. '
        f'It is the largest B, in 4 px steps, that keeps all three with {SPARE} px to spare.</p>'
        '<h2>If Dustin chooses the rewrite</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in R["if_chosen"]) + '</ul>'
        '<p class="cap">Files: today’s plates are s-12-pattern-correct and s-12-pattern-failure in the guide; the rewrite’s '
        'plates and words are REWRITE_12_4, cover_signed and rewrite_plates in work/build/scripts/phase-2/stage_b_identity_ch12.py, '
        'not built into the guide. Figures: work/handoffs/phase-2/20261111_Stage-C-Round-1-Identity-Figures.json, key rule_12_4.</p>')
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Rule 12.4 comparison</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<style>{tokens}</style><style>:root{{color-scheme:light}}{LIB.CSS}{PAGE_CSS}{_illus_css()}</style></head><body><main>{body}</main></body></html>')
    PLATES.mkdir(parents=True, exist_ok=True)
    html = PLATES / "20261111_Rule-12-4-Comparison.html"
    html.write_text(LIB.curl_html(page))
    shots = r"""
const { chromium } = require('playwright'); const [html, a, b2] = process.argv.slice(2);
(async () => { const b = await chromium.launch();
  for (const [sc, f] of [[1, a], [2, b2]]) { const p = await b.newPage({ viewport: { width: 1064, height: 900 }, deviceScaleFactor: sc });
    await p.goto('file://' + html, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: f, fullPage: true }); await p.close(); }
  await b.close(); })();
"""
    node(shots, Path(scratch).resolve(), html, PLATES / "20261111_Rule-12-4-Comparison-1x.png", PLATES / "20261111_Rule-12-4-Comparison-2x.png")
    return html


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what == "ch17" and len(sys.argv) > 3:
        r = ch17(sys.argv[2], sys.argv[3])
        for k, v in r.items():
            print(k, {x: v[x] for x in ("on_load", "reset_unavailable_at_start", "reset_equals_first_frame", "end_layer_is_its_master")})
            if "last_keyframe_vs_end_frame" in v:
                print("   last keyframe vs end:", [(d["same"], d.get("pixels_differing"), d.get("max_levels")) for d in v["last_keyframe_vs_end_frame"]])
            if "moving_layer_at_rest_vs_master" in v:
                print("   at rest vs master:", [(d["same"], d.get("pixels_differing"), d.get("max_levels")) for d in v["moving_layer_at_rest_vs_master"]])
            if "lockmark_48_end_frame_colors" in v:
                print("   48 px end frame colors:", v["lockmark_48_end_frame_colors"])
            print("   after play:", {x: y for x, y in v["after_play"].items() if x != "why"})
    elif what == "rule-12-4" and len(sys.argv) > 2:
        r = rule_12_4(sys.argv[2])
        for h, v in r["by_height"].items():
            print(h, v)
        print("largest that passes:", r["largest_that_passes"], "in generator:", r["in_generator"], r.get("chosen_height_pieces_at_offsets_within_4_px"))
        if r["largest_that_passes"] == r["in_generator"]:
            print("wrote", comparison(sys.argv[2]))
    else:
        print(__doc__)
        sys.exit(2)
