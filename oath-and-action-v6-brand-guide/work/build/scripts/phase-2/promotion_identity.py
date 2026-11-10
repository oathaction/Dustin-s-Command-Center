"""Promotion, November 10, 2026: the identity finals Dustin approved become the ones the guide and the records use.

Under work/handoffs/phase-2/20261110_Promotion-Brief.md, "Who does what", item 3 (identity designer).

  End mark (DR-180)   Ampersand B's pixel masters, fit B, on a 1x screen: the 14 px master in 17 px text and the 12 px
                      master in 15 px text, sitting on the baseline. Every other screen keeps the 16 px master at the
                      text's cap height, switched by screen resolution (the identity notes' question 2, approved with
                      every recommendation, D2-709). stage_a_identity_s04.end_mark draws the pair.
  Lockmark (DR-181)   The rebuilt 24 and 48 px masters, each node and the lever one outline, are the files in use
                      (stage_a_identity_lib.LOCK). The 16 px master stays. L3's masthead master carries the 48 px
                      master's paths, so it gets a new dated file beside the November 8 one, which stays as the record.
  L6 (DR-182)         The wordmark and tagline centered on the strip, 14.72 units of 300 lower, 9.3 px at 884 px
                      (stage_a_identity_s03.l6). The strip, the lockmark and every size stay.

Steps, each run alone:

  masters     Writes lockups/20261110_L3-Horizontal-Master.svg and its Prussian White file, checks that each is the
              November 8 file with only the lockmark's paths and the title changed, and updates the minimum sizes
              record (stage_a_identity_s1.update_minimums). No existing master is written.
  specimens   The identity build (stage_a_identity_build.build): chapters 03, 04 and 08, the proofs, their specimens
              and manifest-identity.json. The letterhead proof in the boards' proofs folder is not written; the build
              draws its letter only to keep the id prefixes a full build gives.
  checks DIR  Builds the guide page into DIR, and a control page from the same chapters with the earlier lockmark and
              L3 files swapped back into the identity specimens. Renders both in Chromium at 1x and 2x and compares
              every 24 and 48 px lockmark and every L3 masthead master pixel for pixel (DR-145); compares the masters
              alone on Newsprint, White, Charcoal and Prussian; runs the feed test (D2-468) on both pages; checks the end
              mark in the page at 1x and 2x beside a capital H; compares L6 with the stage B proposal's render; runs the
              engineer's pixel-fit check on the finals; captures every changed plate at 1440 and 390 px; and writes
              work/handoffs/phase-2/20261110_Promotion-Identity-Figures.json.

Run: python3 -I work/build/scripts/phase-2/promotion_identity.py masters | specimens | checks <scratch dir>
Then specimens again, so the chapters print the figures checks wrote, and checks again on the final page.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage_a_identity_lib as LIB  # noqa: E402
from stage_a_identity_lib import ROOT, ID_DIR, LOCK, LOCK_RECT, L3, WM, AMP_END  # noqa: E402

FIGS = LIB.FIGURES_PROMOTION
STAGE_B = ROOT / "work/boards/phase-2/stage-b/drawings/identity"
STAGE_B_FIGS = STAGE_B / "20261109_Identity-Figures.json"
GUIDE_BUILD = HERE / "guide_build.py"
SPEC_DIR = ROOT / "work/build/guide/specimens"
CHAP_DIR = ROOT / "work/build/guide/chapters"
MINE = ("s-03-", "s-04-", "s-08-", "s-proofs-")

L3_TITLE = ("L3 horizontal lockup, masthead master on the pixel grid: the wordmark's 24 px master (capitals 22 px), 13 px of "
            "space and the lockmark's 48 px master, centered on the wordmark's box. 282 by 48 px, for the site and email "
            "masthead. It carries the rebuilt 48 px lockmark master, each node and the lever one outline, and draws the same "
            "pixels as the November 8 file (DR-181)")

# the earlier files and the files in use, for the control page and the comparisons
SWAP = {
    LOCK[24]: LOCK_RECT[24],
    LOCK[48]: LOCK_RECT[48],
    "prussian/" + Path(LOCK[24]).stem + "-Prussian-White.svg": "prussian/" + Path(LOCK_RECT[24]).stem + "-Prussian-White.svg",
    "prussian/" + Path(LOCK[48]).stem + "-Prussian-White.svg": "prussian/" + Path(LOCK_RECT[48]).stem + "-Prussian-White.svg",
    L3["masthead"]: L3["masthead_rect"],
    "prussian/" + Path(L3["masthead"]).stem + "-Prussian-White.svg": "prussian/" + Path(L3["masthead_rect"]).stem + "-Prussian-White.svg",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git_blob_sha(rel):
    """The file's sha256 as committed at HEAD, or None when it is not in git."""
    r = subprocess.run(["git", "show", f"HEAD:./{rel}"], cwd=ROOT, capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None


def inner(svg):
    """Everything inside a root <svg>, its title removed."""
    body = re.sub(r"<title>.*?</title>", "", svg, count=1, flags=re.S)
    return body[re.match(r"<svg\b[^>]*>", body).end():body.rindex("</svg>")]


# ============================================================================================ masters
def esc(t):
    return t.replace("&", "&amp;").replace("'", "&#x27;")


def l3_masthead():
    """L3's masthead master with the rebuilt 48 px lockmark: the November 8 file with the lockmark's paths and the title
    changed, nothing else."""
    import stage_a_identity_s1 as S1
    old = (ID_DIR / L3["masthead_rect"]).read_text()
    rect48, out48 = (ID_DIR / LOCK_RECT[48]).read_text(), (ID_DIR / LOCK[48]).read_text()
    assert inner(rect48) in old, "the November 8 L3 does not carry the November 8 48 px master's drawing"
    new = old.replace(inner(rect48), inner(out48), 1)
    new = re.sub(r"<title>.*?</title>", f"<title>{esc(L3_TITLE)}</title>", new, count=1, flags=re.S)
    assert inner((ID_DIR / WM[24]).read_text()) in new, "the wordmark's 24 px master is not in the new L3 byte for byte"
    assert inner(out48) in new and inner(rect48) not in new
    assert new.count("<svg") == 2 and 'viewBox="0 -12 282 48"' in new and '<svg x="234" y="-12" width="48" height="48" viewBox="0 0 48 48">' in new
    white = S1.prussian_hooks(new)
    pw_out48 = (ID_DIR / "prussian" / (Path(LOCK[48]).stem + "-Prussian-White.svg")).read_text()
    assert inner(pw_out48) in white, "the new L3's White file does not carry the rebuilt 48 px White file's drawing"
    f1 = ID_DIR / L3["masthead"]
    f2 = ID_DIR / "prussian" / (f1.stem + "-Prussian-White.svg")
    for f in (f1, f2):
        assert f.name.startswith("20261110_"), f            # a new file beside the old; never an existing master
    f1.write_text(new)
    f2.write_text(white)
    old_white = (ID_DIR / "prussian" / (Path(L3["masthead_rect"]).stem + "-Prussian-White.svg")).read_text()
    return {"file": LIB.rel(f1), "prussian": LIB.rel(f2), "from": L3["masthead_rect"],
            "same_as_november_8_but_lockmark_and_title": old.replace(inner(rect48), inner(out48), 1).split("</title>", 1)[1] == new.split("</title>", 1)[1],
            "white_same_as_november_8_but_lockmark_and_title": re.sub(r"<title>.*?</title>", "", old_white).replace(
                inner((ID_DIR / "prussian" / (Path(LOCK_RECT[48]).stem + "-Prussian-White.svg")).read_text()), inner(pw_out48), 1)
                == re.sub(r"<title>.*?</title>", "", white),
            "sha256": sha(f1), "prussian_sha256": sha(f2)}


def masters():
    rec = l3_masthead()
    import stage_a_identity_s1 as S1
    S1.update_minimums()
    print(json.dumps(rec, indent=1))
    print("updated", S1.MIN_FILE.relative_to(ROOT))
    return rec


# ============================================================================================ specimens
def specimens():
    import stage_a_identity_build as B
    import stage_a_identity_proofs as SP

    def no_letterhead(pdf=False):
        LIB.INLINE_ALL[0] = True
        try:
            SP._letter()        # the same two masters inlined as write_letterhead draws, so the id prefixes match
        finally:
            LIB.INLINE_ALL[0] = False
    SP.write_letterhead = no_letterhead
    B.build()


# ============================================================================================ checks
SHOTS_JS = r"""
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const VB = new Set(['0 0 24 24', '0 0 48 48', '0 -12 282 48']);
(async () => {
  const b = await chromium.launch();
  const res = { lockmarks: {}, endmark: {}, l6: {}, plates: {} };
  for (const [name, file] of Object.entries(job.pages)) {
    for (const scale of [1, 2]) {
      const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: scale });
      await p.goto('file://' + file, { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      // every 24 and 48 px lockmark and every L3 masthead master in the identity specimens, in document order
      for (const sid of job.specimens) {
        const svgs = p.locator(`[data-specimen="${sid}"] svg`);
        const n = await svgs.count();
        let k = 0;
        for (let i = 0; i < n; i++) {
          const s = svgs.nth(i);
          const vb = await s.getAttribute('viewBox');
          if (!VB.has(vb)) continue;
          const parentVb = await s.evaluate((e) => e.parentElement && e.parentElement.closest('svg') ? 'nested' : 'root');
          if (parentVb === 'nested') continue;
          const box = await s.boundingBox();
          if (!box || box.width < 1) continue;
          await s.scrollIntoViewIfNeeded();
          const f = path.join(job.out, `lk-${name}-${sid}-${k}@${scale}x.png`);
          await s.screenshot({ path: f });
          (res.lockmarks[`${name}@${scale}x`] ||= []).push({ sid, k, vb, w: box.width, h: box.height, file: f });
          k++;
        }
      }
      if (name === 'after') {
        // the end mark: which drawing shows, its box, and a probe H of the same text beside it for the rows
        const paras = p.locator('[data-specimen="s-04-6-correct"] p:has(.oai-end-fit)');
        const m = await paras.count();
        for (let i = 0; i < m; i++) {
          const info = await paras.nth(i).evaluate((para) => {
            const span = para.querySelector('span[style*="nowrap"]');
            const fit = span.querySelector('.oai-end-fit'), sm = span.querySelector('.oai-end-smooth');
            const cs = (e) => getComputedStyle(e).display;
            const r = (e) => { const q = e.getBoundingClientRect(); return { x: q.x, y: q.y, w: q.width, h: q.height }; };
            const probe = document.createElement('span');
            probe.textContent = 'H';
            probe.setAttribute('data-probe', '1');
            span.insertBefore(probe, fit);
            const shown = cs(fit) !== 'none' ? fit : sm;
            const pr = probe.getBoundingClientRect(), sr = shown.getBoundingClientRect();
            return { font_px: parseFloat(getComputedStyle(para).fontSize), fit_display: cs(fit), smooth_display: cs(sm), fit_box: r(fit), smooth_box: r(sm),
                     shown: shown === fit ? 'fit' : 'smooth', ground: getComputedStyle(para.closest('[class*="oai-s-"]')).backgroundColor,
                     clip: { x: Math.floor(pr.left), y: Math.floor(Math.min(pr.top, sr.top)) - 3, width: Math.ceil(sr.right) - Math.floor(pr.left) + 2,
                             height: Math.ceil(Math.max(pr.bottom, sr.bottom)) - Math.floor(Math.min(pr.top, sr.top)) + 6 } };
          });
          await paras.nth(i).scrollIntoViewIfNeeded();
          const again = await paras.nth(i).evaluate((para) => {
            const pr = para.querySelector('[data-probe]').getBoundingClientRect();
            const sp = para.querySelector('span[style*="nowrap"]');
            const fit = sp.querySelector('.oai-end-fit'), sm = sp.querySelector('.oai-end-smooth');
            const shown = getComputedStyle(fit).display !== 'none' ? fit : sm;
            const sr = shown.getBoundingClientRect();
            return { x: Math.floor(pr.left), y: Math.floor(Math.min(pr.top, sr.top)) - 3, width: Math.ceil(sr.right) - Math.floor(pr.left) + 2,
                     height: Math.ceil(Math.max(pr.bottom, sr.bottom)) - Math.floor(Math.min(pr.top, sr.top)) + 6 };
          });
          const f = path.join(job.out, `em-${i}@${scale}x.png`);
          await p.screenshot({ path: f, clip: again });
          (res.endmark[`${scale}x`] ||= []).push(Object.assign(info, { file: f }));
          await paras.nth(i).evaluate((para) => para.querySelector('[data-probe]').remove());
        }
      }
      // L6's strip
      const strip = p.locator('[data-specimen="s-03-l6"] [aria-label^="Oath & Action, L6"]').first();
      await strip.scrollIntoViewIfNeeded();
      const f6 = path.join(job.out, `l6-${name}@${scale}x.png`);
      await strip.screenshot({ path: f6 });
      res.l6[`${name}@${scale}x`] = { file: f6, box: await strip.boundingBox() };
      await p.close();
    }
  }
  // every changed plate at 1440 and 390 px, as a reader sees it, at 1x
  for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 1000 }, deviceScaleFactor: 1 });
    await p.goto('file://' + job.pages.after, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    for (const sid of job.plates) {
      const fig = p.locator(`#fig-${sid}`);
      if (!(await fig.count())) { res.plates[`${sid}@${w}`] = null; continue; }
      await fig.scrollIntoViewIfNeeded();
      const f = path.join(job.out, `plate-${sid}-${w}.png`);
      await fig.screenshot({ path: f });
      res.plates[`${sid}@${w}`] = f;
    }
    await p.close();
  }
  await b.close();
  fs.writeFileSync(path.join(job.out, 'shots.json'), JSON.stringify(res, null, 1));
})();
"""

MASTERS_JS = r"""
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const [html, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const ids = JSON.parse(fs.readFileSync(html + '.ids.json', 'utf8'));
  for (const scale of [1, 2]) {
    const p = await b.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: scale });
    await p.goto('file://' + html, { waitUntil: 'networkidle' });
    for (const id of ids) await p.locator('#' + id).screenshot({ path: path.join(out, `${id}@${scale}x.png`) });
    await p.close();
  }
  await b.close();
})();
"""

ID_SPECS = ["s-03-4-correct", "s-03-lockups", "s-03-6-correct", "s-03-6-failure", "s-08-1-correct", "s-08-2-correct",
            "s-proofs-masthead", "s-proofs-social", "s-proofs-letterhead"]
PLATES = ["s-03-lockups", "s-03-l6", "s-03-4-correct", "s-03-minimums", "s-03-6-correct", "s-03-6-failure", "s-04-6-correct",
          "s-08-1-correct", "s-08-2-correct", "s-proofs-masthead", "s-proofs-social", "s-proofs-letterhead"]


def build_pages(scratch):
    """The guide as the repository builds it, and a control page: the same chapters and specimens with the earlier
    lockmark and L3 files swapped back into the identity specimens, so the two differ only in those drawings."""
    after = scratch / "guide.html"
    r = subprocess.run(["python3", "-I", str(GUIDE_BUILD), "--strict", "--out", str(after)], capture_output=True, text=True)
    out = {"after": {"exit": r.returncode, "tail": r.stdout.strip().splitlines()[-1:] + r.stderr.strip().splitlines()[-3:]}}
    cs = scratch / "control-specimens"
    if cs.exists():
        shutil.rmtree(cs)
    shutil.copytree(SPEC_DIR, cs)
    swapped = {}
    for f in cs.glob("s-*.html"):
        if not f.stem.startswith(MINE):
            continue
        t = f.read_text()
        n = 0
        for new, old in SWAP.items():
            n += t.count(new)
            t = t.replace(new, old)
        if n:
            f.write_text(t)
            swapped[f.stem] = n
    control = scratch / "control.html"
    r = subprocess.run(["python3", "-I", str(GUIDE_BUILD), "--chapters", str(CHAP_DIR), "--specimens", str(cs), "--out", str(control)],
                       capture_output=True, text=True)
    out["control"] = {"exit": r.returncode, "swapped": swapped}
    return after, control, out


def same(a, b):
    from PIL import Image, ImageChops
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    if A.size != B.size:
        return {"same": False, "size": [A.size, B.size]}
    box = ImageChops.difference(A, B).getbbox()
    if box is None:
        return {"same": True, "size": list(A.size)}
    diff = ImageChops.difference(A, B).convert("L")
    return {"same": False, "size": list(A.size), "diff_box": list(box), "diff_px": sum(1 for v in diff.getdata() if v)}


def masters_alone(scratch):
    """Each rebuilt master and the new L3 against the earlier file at its own size, on each surface, at 1x and 2x. Two
    pages with the same cells, one drawing the files in use and one the earlier files, so each pair sits at the same
    place: Chromium shades a curve's edge pixels a few levels differently at different places on a page."""
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    pairs = [(24, LOCK[24], LOCK_RECT[24]), (48, LOCK[48], LOCK_RECT[48]), ("l3", L3["masthead"], L3["masthead_rect"])]
    d = scratch / "masters"
    d.mkdir(exist_ok=True)
    js = scratch / "masters.js"
    js.write_text(MASTERS_JS)
    for kind in ("new", "old"):
        cells, ids = [], []
        LIB.INLINE_ALL[0] = True
        try:
            for key, new, old in pairs:
                for surface in ("newsprint", "white", "charcoal", "prussian"):
                    i = f"m-{key}-{surface}"
                    ids.append(i)
                    h = 48 if key == "l3" else key
                    m = LIB.mark(new if kind == "new" else old, h=h, surface=surface, label=i)
                    cells.append(f'<div id="{i}" class="oai-s-{surface}" style="display:inline-block;padding:4px;line-height:0;margin:4px">{m}</div>')
        finally:
            LIB.INLINE_ALL[0] = False
        html = scratch / f"masters-{kind}.html"
        html.write_text('<!doctype html><html><head><meta charset="utf-8">'
                        f'<style>{tokens}</style><style>{LIB.CSS}body{{margin:0}}</style></head><body><div class="oai">{"".join(cells)}</div></body></html>')
        Path(str(html) + ".ids.json").write_text(json.dumps(ids))
        (d / kind).mkdir(exist_ok=True)
        subprocess.run(["node", str(js), str(html), str(d / kind)], check=True, cwd=str(ROOT / "work/build"))
    out = {}
    for key, new, old in pairs:
        for surface in ("newsprint", "white", "charcoal", "prussian"):
            for scale in (1, 2):
                out[f"{key}-{surface}-{scale}x"] = same(d / "new" / f"m-{key}-{surface}@{scale}x.png", d / "old" / f"m-{key}-{surface}@{scale}x.png")["same"]
    return out


def rows_of(img, ground):
    """H and B in a crop: the first run of inked columns is H, the rest is B. Each one's first and last inked device
    row, and the share of B's ink pixels drawn at full color."""
    im = img.convert("RGB")
    W, H = im.size
    px = im.load()
    inkc = (0x12, 0x12, 0x12) if sum(ground) > 300 else (0xDC, 0xD9, 0xD2)
    span = max(abs(a - b) for a, b in zip(ground, inkc))
    cov = [[max(abs(a - b) for a, b in zip(px[x, y], ground)) / span for x in range(W)] for y in range(H)]
    cols = [x for x in range(W) if any(cov[y][x] > 0.18 for y in range(H))]
    runs, start, prev = [], cols[0], cols[0]
    for x in cols[1:]:
        if x != prev + 1:
            runs.append((start, prev))
            start = x
        prev = x
    runs.append((start, prev))

    def rows(x0, x1):
        ys = [y for y in range(H) if any(cov[y][x] > 0.18 for x in range(x0, x1 + 1))]
        return ys[0], ys[-1]
    h, b = rows(*runs[0]), rows(runs[1][0], runs[-1][1])
    inked = [cov[y][x] for y in range(H) for x in range(runs[1][0], runs[-1][1] + 1) if cov[y][x] > 0.05]
    return {"h_rows": [h[0], h[1]], "b_rows": [b[0], b[1]], "b_full_share": round(sum(1 for v in inked if v >= 0.95) / len(inked), 3)}


def endmark_check(shots):
    from PIL import Image
    out = {}
    for scale in ("1x", "2x"):
        res = []
        for e in shots["endmark"].get(scale, []):
            g = tuple(int(v) for v in re.findall(r"\d+", e["ground"])[:3])
            r = rows_of(Image.open(e["file"]), g)
            k = 1 if scale == "1x" else 2
            res.append({"font_px": e["font_px"], "shown": e["shown"], "fit_display": e["fit_display"], "smooth_display": e["smooth_display"],
                        "shown_height_px": round((e["fit_box"] if e["shown"] == "fit" else e["smooth_box"])["h"], 2),
                        "b_rows_device": r["b_rows"][1] - r["b_rows"][0] + 1, "h_rows_device": r["h_rows"][1] - r["h_rows"][0] + 1,
                        "top_rows_over_h": r["h_rows"][0] - r["b_rows"][0], "last_rows_under_h": r["b_rows"][1] - r["h_rows"][1],
                        "b_full_share": r["b_full_share"], "scale": k,
                        "ground": "charcoal" if sum(g) < 200 else "newsprint"})
        out[scale] = res
    return out


def l6_check(scratch, shots):
    """L6 as the guide now draws it (stage_a_identity_s03.l6) against the stage B proposal's drawing
    (stage_b_identity_drawings.l6_centered with its 14.72 units): the markup with the masters inlined, the specimen's
    positions, and both rendered at the same place on two pages at 1x and 2x. Also the strip's box in the built page."""
    import stage_a_identity_s03 as S03
    import stage_b_identity_drawings as SB
    figs = json.loads(STAGE_B_FIGS.read_text())["l6"]
    LIB.INLINE_ALL[0] = True
    try:
        guide, proposal = S03.l6(884), SB.l6_centered(884, figs["shift_down_units"])
    finally:
        LIB.INLINE_ALL[0] = False
    strip = lambda h: re.sub(r'aria-label="[^"]*"', "", re.sub(r'oai\d+-', "", h))   # noqa: E731  (names and id prefixes aside)
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    d = scratch / "l6"
    d.mkdir(exist_ok=True)
    js = scratch / "masters.js"
    js.write_text(MASTERS_JS)
    for kind, h in (("guide", guide), ("proposal", proposal)):
        html = scratch / f"l6-{kind}.html"
        html.write_text('<!doctype html><html><head><meta charset="utf-8">'
                        f'<style>{tokens}</style><style>{LIB.CSS}body{{margin:0}}</style></head><body><div class="oai">'
                        f'<div id="l6" style="width:max-content;margin:16px">{h}</div></div></body></html>')
        Path(str(html) + ".ids.json").write_text(json.dumps(["l6"]))
        (d / kind).mkdir(exist_ok=True)
        subprocess.run(["node", str(js), str(html), str(d / kind)], check=True, cwd=str(ROOT / "work/build"))
    spec = (SPEC_DIR / "s-03-l6.html").read_text()
    tops = re.findall(r'position:absolute;left:([\d.]+)px;top:([\d.]+)px', spec)
    return {"shift_units": S03.L6_SHIFT, "stage_b_shift_units": figs["shift_down_units"], "stage_b_shift_px_at_884": figs["shift_down_px_at_884"],
            "markup_same_as_proposal": strip(guide) == strip(proposal),
            "same_pixels_as_proposal_1x": same(d / "guide" / "l6@1x.png", d / "proposal" / "l6@1x.png")["same"],
            "same_pixels_as_proposal_2x": same(d / "guide" / "l6@2x.png", d / "proposal" / "l6@2x.png")["same"],
            "specimen_positions_px": [[float(x), float(y)] for x, y in tops],
            "strip_in_built_page_1x": shots["l6"]["after@1x"]["box"]}


def feed(page):
    """D2-468's feed test, as stage_a_identity_q_measure.feed_test runs it, on a given built page."""
    import stage_a_identity_q_measure as QM
    import tempfile
    got = {}
    keep_guide, keep_save = QM.GUIDE, QM.save
    QM.GUIDE, QM.save = page, (lambda k, v: got.__setitem__(k, v))
    try:
        QM.feed_test(Path(tempfile.mkdtemp(prefix="oai-feed-")))
    finally:
        QM.GUIDE, QM.save = keep_guide, keep_save
    return got["feed"]


def pixel_fit(scratch):
    """The engineer's check on the finals at their own sizes. B's masters run on square copies padded on the right,
    which keeps them on whole pixels (D2-548)."""
    files = []
    for t, (rel, w, h) in AMP_END.items():
        n = max(w, h)
        src = (ID_DIR / rel).read_text()
        sq = scratch / f"{Path(rel).stem}-Square.svg"
        sq.write_text(src.replace(f'viewBox="0 0 {w} {h}"', f'viewBox="0 0 {n} {n}"'))
        files.append((sq, n, rel))
    for s in (24, 48):
        files.append((ID_DIR / LOCK[s], s, LOCK[s]))
    out = {}
    for f, n, name in files:
        j = scratch / f"pfc-{Path(name).stem}.json"
        r = subprocess.run(["python3", "-I", str(HERE / "icon_pixel_fit_check.py"), "--size", str(n), "--json", str(j), "--quiet", str(f)],
                           capture_output=True, text=True)
        try:
            data = json.loads(j.read_text())
        except Exception:
            data = {"error": (r.stderr or r.stdout)[-400:]}
        out[name] = {"size": n, "exit": r.returncode, "result": data}
    return out


def hashes():
    """Each final in use: its sha256 now and at HEAD (unchanged files keep their bytes), and the new files."""
    rels = [AMP_END[17][0], AMP_END[15][0], LOCK[24], LOCK[48], LOCK[16]]
    rels += ["prussian/" + Path(r).stem + "-Prussian-White.svg" for r in (AMP_END[17][0], AMP_END[15][0], LOCK[24], LOCK[48], LOCK[16])]
    rels += [L3["masthead_rect"], "prussian/" + Path(L3["masthead_rect"]).stem + "-Prussian-White.svg", LOCK_RECT[24], LOCK_RECT[48]]
    out = {}
    for r in rels:
        p = ID_DIR / r
        out[r] = {"sha256": sha(p), "same_as_head": sha(p) == git_blob_sha(LIB.rel(p))}
    for r in (L3["masthead"], "prussian/" + Path(L3["masthead"]).stem + "-Prussian-White.svg"):
        out[r] = {"sha256": sha(ID_DIR / r), "same_as_head": None, "new": True}
    return out


def endmark_fit_figures():
    """The pixel masters' figures from the stage B measurement Dustin approved them on (fit B beside a capital H of the
    same text, at eight times and at 1x with the line at four positions between pixels)."""
    d = json.loads(STAGE_B_FIGS.read_text())
    out = {"source": LIB.rel(STAGE_B_FIGS) + ", measure.end_mark, keys 14B-newsprint and 12B-newsprint"}
    for text_px, key in ((17, "14B"), (15, "12B")):
        m = d["measure"]["end_mark"][f"{key}-newsprint"]
        f = d["end_files"][key]
        rows = m["rows_at_1x"]
        out[str(text_px)] = {"file": AMP_END[text_px][0], "b_px": m["b_px"], "b_width_px": f["width_px"], "capitals_px": m["capitals_px"],
                             "top_over_cap_line_px": m["top_over_cap_line_px"], "tail_under_baseline_px": m["tail_under_baseline_px"],
                             "rows_at_1x_four_positions": {"b_rows": sorted({q["b_rows"] for q in rows}),
                                                           "top_rows_over_h": sorted({q["top_rows_over_h"] for q in rows}),
                                                           "tail_rows_under_h": sorted({q["tail_rows_under_h"] for q in rows})},
                             "full_ink_share_at_1x": m["b_full_ink_share_at_1x"]}
    return out


def checks(scratch):
    scratch = Path(scratch).resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    figs = {"date": "2026-11-10", "method": "Chromium through Playwright; masters inlined by guide_build.py; device scale 1 and 2; "
            "pixel comparisons are exact (any channel difference counts)"}
    figs["endmark_fit"] = endmark_fit_figures()
    after, control, figs["pages"] = build_pages(scratch)
    shots_dir = scratch / "shots"
    shots_dir.mkdir(exist_ok=True)
    job = scratch / "job.json"
    job.write_text(json.dumps({"pages": {"after": str(after), "control": str(control)}, "specimens": ID_SPECS, "plates": PLATES, "out": str(shots_dir)}))
    js = scratch / "shots.js"
    js.write_text(SHOTS_JS)
    subprocess.run(["node", str(js), str(job)], check=True, cwd=str(ROOT / "work/build"))
    shots = json.loads((shots_dir / "shots.json").read_text())
    # DR-145 in the page: each lockmark and L3 drawing against the same place drawn with the earlier file
    cmp = {}
    for scale in (1, 2):
        A, C = shots["lockmarks"][f"after@{scale}x"], shots["lockmarks"][f"control@{scale}x"]
        assert [(a["sid"], a["vb"]) for a in A] == [(c["sid"], c["vb"]) for c in C], "the two pages place different drawings"
        for a, c in zip(A, C):
            r = same(a["file"], c["file"])
            cmp[f'{a["sid"]}-{a["k"]}@{scale}x'] = dict(r, viewBox=a["vb"], drawn_px=[round(a["w"], 2), round(a["h"], 2)])
    figs["in_page"] = cmp
    figs["masters_alone"] = masters_alone(scratch)
    figs["endmark_in_page"] = endmark_check(shots)
    figs["l6"] = l6_check(scratch, shots)
    figs["feed"] = feed(after)
    figs["feed_control_page"] = feed(control)
    figs["feed_control_page"]["lockmark_master"] = LOCK_RECT[48]      # the test names the file by its viewBox, which both share
    figs["pixel_fit_check"] = pixel_fit(scratch)
    figs["hashes"] = hashes()
    figs["plates"] = shots["plates"]
    FIGS.write_text(json.dumps(figs, indent=1, ensure_ascii=False) + "\n")
    print("wrote", FIGS.relative_to(ROOT))
    return figs


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what == "masters":
        masters()
    elif what == "specimens":
        specimens()
    elif what == "checks" and len(sys.argv) > 2:
        f = checks(sys.argv[2])
        print(json.dumps({k: f[k] for k in ("pages", "masters_alone", "endmark_in_page", "l6")}, indent=1))
        print("in page, not the same:", {k: v for k, v in f["in_page"].items() if not v["same"]})
        print("feed:", {k: f["feed"][k] for k in ("at_500", "at_360", "lockmark_master")})
        print("feed, control page:", {k: f["feed_control_page"][k] for k in ("at_500", "at_360", "lockmark_master")})
        print("pixel-fit exits:", {k: v["exit"] for k, v in f["pixel_fit_check"].items()})
    else:
        print(__doc__)
        sys.exit(2)
