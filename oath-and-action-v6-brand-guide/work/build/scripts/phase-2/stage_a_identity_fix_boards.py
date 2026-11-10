"""Plates for Dustin's changes board, fix pass after the apply pass review (November 7, 2026).

Writes three folders under work/boards/phase-2/apply-pass/, each a standalone HTML page of plates at true size on
Newsprint (masters inlined, tokens inlined, Google Fonts only), PNG renders of each plate at 1x and 2x, and a JSON of
the figures the plates print:

  end-mark/   CD-M1, CA-S4: B as an article's end mark at 17 and 19 px text, (a) at the text's cap height, an exception
              to B's 16 px minimum for the end mark alone, and (b) at B's 16 px minimum, which the guide now draws.
  l6/         D2-403: L6 as drawn and L6 without its four pillar dots, side by side at L6's 884 px minimum.
  lockmark/   CA-S1, CA-S2: today's lockmark in its four places, a proposed pixel-fit 48 px master for the sign-off and
              the masthead, and each candidate on a social card reduced to the 500 and 360 px a feed shows.

The proposed 48 px master is a proposal for Dustin's named approval (gate rule 4). It is written only into the board's
folder, never into work/build/assets/identity/, and no guide page draws it.

Run: python3 work/build/scripts/phase-2/stage_a_identity_fix_boards.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage_a_identity_lib as LIB  # noqa: E402
from stage_a_identity_lib import (E, ROOT, ID_DIR, AMP, LOCK, WM, svg_file, mark, lockmark, ink, ink2, hair, pal, tv, ty,  # noqa: E402
                                  curl_html, illus)
from stage_a_identity_s03 import l6, l3_small  # noqa: E402

BOARD = ROOT / "work/boards/phase-2/apply-pass"
CAP = 0.7275                       # Inter's cap height in em (the guide's type tokens)
END_TEXT = ("The board meets again on April 2, and the agenda posts a week before. We will add the vote to the tracker once "
            "the clerk publishes the minutes.")
TAGLINE = "A country that answers to its people."

PAGE_CSS = """
body{margin:0;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);font-family:var(--oa-font-family-reading)}
.bd{padding:32px;display:flex;flex-direction:column;gap:40px}
.bd h1{font:800 26px/1.2 var(--oa-font-family-display);letter-spacing:-0.01em;margin:0}
.bd .lede{font-size:15px;line-height:1.5;max-width:70ch;margin:8px 0 0;color:var(--oa-color-text-secondary-on-newsprint)}
.plate{background:var(--oa-color-surface-newsprint);border:1px solid var(--oa-color-border-hairline-on-newsprint);padding:24px;display:inline-flex;flex-direction:column;gap:20px;align-self:flex-start}
.plate h2{font:700 13px/1.4 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;margin:0}
.fig{font-size:13px;line-height:1.45;color:var(--oa-color-text-secondary-on-newsprint);margin:6px 0 0;max-width:62ch}
.row{display:flex;gap:32px;align-items:flex-start;flex-wrap:nowrap}
.illus{display:inline-block;align-self:flex-start;padding:0 .4em;border:1px solid currentColor;font:700 13px/1.5 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase}
.cell{display:flex;flex-direction:column;gap:8px;align-items:flex-start}
"""


def page(title, body, css=""):
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<style>{tokens}</style><style>{LIB.CSS}{PAGE_CSS}{css}</style></head>'
            f'<body><div class="bd oai">{curl_html(body)}</div></body></html>')


def shoot(html_path, out_dir, ids, names=None):
    """Render each plate at 1x and 2x. names maps an element id to the file's title words (house naming)."""
    fonts = None
    for scale in (1, 2):
        r = subprocess.run(["node", str(HERE / "stage_a_identity_shots.js"), str(html_path), str(out_dir), str(scale), *ids],
                           check=True, capture_output=True, text=True)
        fonts = json.loads(r.stdout.strip().splitlines()[-1])["fonts"]
        for i in ids:
            if names:
                (out_dir / f"{i}@{scale}x.png").replace(out_dir / f"20261107_{names[i]}-{scale}x.png")
    return fonts


def measure_end_marks(out):
    """Ink rows of B and of a capital H set beside it, at eight times size: B's height, its top over the cap line and
    its tail under the baseline, as the page draws them."""
    from PIL import Image
    cells, ids = [], []
    for mode in ("cap", "min"):
        for f in (17, 19):
            b, _ = end_b(f, mode)
            ids.append(f"t-{mode}-{f}")
            cells.append(f'<div id="t-{mode}-{f}" style="width:max-content;align-self:flex-start;padding:6px;{LIB.ty("body", size=f)}">H{b.replace("margin-left:0.5em", "margin-left:6px")}</div>')
    tmp = out / "_measure.html"
    tmp.write_text(page("measure", "".join(cells)))
    subprocess.run(["node", str(HERE / "stage_a_identity_shots.js"), str(tmp), str(out / "_m"), "8", *ids], check=True, capture_output=True)
    res = {}
    for i in ids:
        im = Image.open(out / "_m" / f"{i}@8x.png").convert("L")
        W, H = im.size
        dark = [[im.getpixel((x, y)) < 110 for x in range(W)] for y in range(H)]
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
        res[i] = {"capitals_px": round(hB - hT, 2), "b_px": round(bB - bT, 2), "top_over_cap_line_px": round(hT - bT, 2),
                  "tail_under_baseline_px": round(bB - hB, 2)}
        (out / "_m" / f"{i}@8x.png").unlink()
    (out / "_m").rmdir()
    tmp.unlink()
    return res


# =========================================================================================== end mark
def end_b(font_px, mode):
    """B from its 16 px master. mode 'cap': its 14 px band (the master's capitals, y 1 to 15) on the text's cap band,
    as Rule 04.3 sets B in a hinge headline. mode 'min': the master at 16 px, its 16 px minimum, with the master's
    baseline on the text's baseline."""
    cap = font_px * CAP
    if mode == "cap":
        h, below = cap * 16 / 14, cap / 14
    else:
        h, below = 16.0, 1.0
    svg = svg_file(ID_DIR / AMP[16], h=h, decorative=True,
                   style=f"color:{ink('newsprint')};display:inline-block;vertical-align:{-below:.3f}px;margin-left:0.5em")
    figures = {"text_px": font_px, "capitals_px": round(cap, 2), "b_px": round(h, 2), "b_scale_of_16px_master": round(h / 16, 3),
               "top_over_cap_line_px": round(h - below - cap, 2), "tail_under_baseline_px": round(below, 2), "gap": "0.5 em"}
    return svg, figures


def end_para(font_px, mode):
    head, last = END_TEXT.rsplit(" ", 1)
    b, fig = end_b(font_px, mode)
    p = (f'<p style="{LIB.ty("body", size=font_px)};width:520px;margin:0">{E(head)} '
         f'<span style="white-space:nowrap">{E(last)}{b}</span></p>')
    return p, fig


def end_mark_board():
    out = BOARD / "end-mark"
    out.mkdir(parents=True, exist_ok=True)
    plates, figs = [], {}
    measured = measure_end_marks(out)
    for key, mode, title, tail in (
            ("a", "cap", "(a) B at the text's cap height",
             "An exception to B's 16 px minimum, for the end mark alone. B's band, its height less the overshoot above and below, "
             "matches the capitals, as Rule 04.3 sets B in a hinge headline. B comes from its 16 px master, scaled."),
            ("b", "min", "(b) B at its 16 px minimum",
             "B's 16 px master at 16 px, with the master's baseline on the text's baseline. The guide draws this today.")):
        rows = []
        figs[key] = []
        for fpx in (17, 19):
            p, fig = end_para(fpx, mode)
            fig["measured_at_8x"] = measured[f"t-{mode}-{fpx}"]
            figs[key].append(fig)
            m = fig["measured_at_8x"]
            rows.append(f'<div class="cell">{p}<p class="fig">{fpx} px text: capitals {m["capitals_px"]:.1f} px; B {m["b_px"]:.1f} px tall '
                        f'({fig["b_scale_of_16px_master"] * 100:.0f} percent of its 16 px master), its top {m["top_over_cap_line_px"]:.1f} px over the cap line '
                        f'and its tail {m["tail_under_baseline_px"]:.1f} px under the baseline, measured on this page in Chromium; half an em after the period.</p></div>')
        plates.append(f'<section class="plate" id="end-mark-{key}"><h2>{E(title)}</h2><p class="fig" style="margin:0">{E(tail)}</p>'
                      f'{illus()}{"".join(rows)}</section>')
    body = ('<header><h1>The end mark at body size</h1><p class="lede">Two ways to end an article on ampersand B, at true size on '
            'Newsprint. Each plate shows a paragraph\'s last lines at 17 px, the body size, and at 19 px. The paragraph is invented.</p></header>'
            + "".join(plates))
    html_path = out / "20261107_End-Mark-Plates.html"
    html_path.write_text(page("End mark plates", body))
    fonts = shoot(html_path, out, ["end-mark-a", "end-mark-b"], {"end-mark-a": "End-Mark-A-Cap-Height", "end-mark-b": "End-Mark-B-Minimum"})
    (out / "20261107_End-Mark-Figures.json").write_text(json.dumps({"plates": figs, "fonts_loaded": fonts}, indent=1) + "\n")
    return figs, fonts


# =========================================================================================== L6
def l6_board():
    out = BOARD / "l6"
    out.mkdir(parents=True, exist_ok=True)
    cells = (f'<div class="cell">{l6(884, dots=True)}<p class="fig">L6 as the guide draws it: the wordmark, the tagline, four pillar dots and the lockmark.</p></div>'
             f'<div class="cell">{l6(884, dots=False, centered=False)}<p class="fig">L6 without the four pillar dots. Nothing else moves.</p></div>')
    body = ('<header><h1>L6 with and without its four pillar dots</h1><p class="lede">L6, the editorial signature that closes a report, at its '
            '884 px minimum, side by side at true size. The dots stand for the four pillars with no words beside them; the pillars now take '
            'their icons with their words.</p></header>'
            f'<section class="plate" id="l6-pair"><h2>At 884 px, L6\'s minimum</h2><div class="row" style="gap:48px">{cells}</div></section>')
    html_path = out / "20261107_L6-Dots-Plates.html"
    html_path.write_text(page("L6 plates", body))
    fonts = shoot(html_path, out, ["l6-pair"], {"l6-pair": "L6-With-And-Without-Dots"})
    return fonts


# =========================================================================================== lockmark
# A proposed 48 px master on the pixel grid, in the grammar of the 24 px master: centers at 4.5, 23.5 and 42.5 px,
# 7 px nodes, a 9 px lever, 1 px links on whole pixels, the same hooks (--link, currentColor, --lever).
P48_CENTERS = (4.5, 23.5, 42.5)
NODE7 = (3, 5, 7, 7, 7, 5, 3)
LEVER9 = (5, 7, 9, 9, 9, 9, 9, 7, 5)


def _disc(cx, cy, rows):
    top = cy - len(rows) / 2
    return "".join(f'<rect x="{cx - w / 2:g}" y="{top + i:g}" width="{w}" height="1"/>' for i, w in enumerate(rows))


def proposal_48_svg():
    c = P48_CENTERS
    links = "".join(f'<rect x="{c[0]:g}" y="{y - 0.5:g}" width="{c[2] - c[0]:g}" height="1"/><rect x="{y - 0.5:g}" y="{c[0]:g}" width="1" height="{c[2] - c[0]:g}"/>' for y in c)
    nodes = "".join(_disc(x, y, NODE7) for y in c for x in c if (x, y) != (c[2], c[2]))
    lever = _disc(c[2], c[2], LEVER9)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><title>Lockmark, proposed 48 px master on the pixel grid, '
            'for the sign-off and the masthead (a proposal for named approval, not a master)</title>'
            f'<g fill="var(--link,#5D636D)">{links}</g><g fill="currentColor">{nodes}</g><g fill="var(--lever,#E63946)">{lever}</g></svg>')


def lk(kind, size, surface="newsprint", label=None):
    """A lockmark drawing for the board: 'today' picks the master Rule 08.1 sets; 'p48' is the proposal; 'm24' is the
    24 px master at the size given."""
    if kind == "today":
        if size >= 48:    # the masters as they stood on November 7, 2026, before the 48 px master (DR-131), so a rerun keeps the record
            return mark(LOCK["display"], h=size, surface=surface, label=label or f"Lockmark at {size} px")
        # the 16 and 24 px masters as they stood then; the rebuilt 24 px file is in use since DR-181 (LIB.LOCK_RECT)
        return mark(LOCK[16] if size < 24 else LIB.LOCK_RECT[24], h=size, surface=surface, label=label or f"Lockmark at {size} px")
    path = BOARD / "lockmark" / "20261107_Lockmark-48px-Proposal.svg" if kind == "p48" else ID_DIR / LIB.LOCK_RECT[24]
    return svg_file(path, h=size, label=label or f"Lockmark at {size} px", style=LIB.mark_style(surface), by_ref=False)


def places(kind):
    """The four places at true size, drawn with today's masters or with the proposal where the display master stands."""
    big = (lambda s: lk("today", s)) if kind == "today" else (lambda s: lk("p48", s))
    mast = (f'<div class="oai-s-newsprint" style="width:420px;height:80px;display:flex;align-items:center;gap:13px;padding:0 24px;border:1px solid {hair("newsprint")}">'
            f'{mark(WM[24], h=24, decorative=True)}<span style="line-height:0">{big(52)}</span></div>')
    head = (f'<div class="oai-s-white" style="width:420px;display:flex;align-items:center;gap:12px;padding:16px 24px;border:1px solid {hair("white")}">'
            f'{lk("today", 24, "white")}<span class="oai-label" style="color:{ink("white")}">03 · Who writes the budget</span></div>')
    foot = (f'<div class="oai-s-charcoal" style="width:420px;display:flex;align-items:center;gap:12px;padding:16px 24px">'
            f'{lk("today", 24, "charcoal")}<span style="{ty("body-small")};color:{ink("charcoal")}">{E(TAGLINE)}</span></div>')
    sign = (f'<div class="oai-s-newsprint" style="position:relative;width:200px;height:150px;border-right:1px solid {ink("newsprint")};border-bottom:1px solid {ink("newsprint")}">'
            f'<span style="position:absolute;right:72px;bottom:72px;line-height:0">{big(48)}</span></div>')
    cells = [("Masthead, 52 px", mast), ("Page header, 24 px", head), ("Footer, 24 px", foot), ("Sign-off, 48 px", sign)]
    return "".join(f'<div class="cell"><p class="fig" style="margin:0">{E(t)}</p>{m}</div>' for t, m in cells)


def social_corner(kind):
    """The bottom-right 400 by 260 px of a 1200 by 630 card with the sign-off drawn by one candidate, for the feed test."""
    m = {"display": lambda: lk("today", 48), "m24": lambda: lk("m24", 48), "p48": lambda: lk("p48", 48)}[kind]()
    return (f'<div id="card-{kind}" class="oai-s-newsprint" style="position:relative;width:1200px;height:630px;padding:72px">'
            f'<p style="{ty("h4", 1200)};color:{ink2("newsprint")}">Explainer · Zoning</p>'
            f'<div style="position:absolute;left:72px;bottom:72px">{mark(WM["display"], h=44, decorative=True)}</div>'
            f'<div style="position:absolute;right:72px;bottom:72px;line-height:0">{m}</div></div>')


FEED_NAME = {"display": "Display-Master", "m24": "24px-Master-Doubled", "p48": "48px-Proposal"}


def measure_marks(out):
    """Render each lockmark at the size a place uses on Newsprint at 1x and count its ink: the share of the field that is
    not Newsprint, the share that is near black, and the red pixels of the lever."""
    from PIL import Image
    cells = [("m16-16", "today", 16), ("m24-24", "today", 24), ("display-48", "today", 48), ("display-52", "today", 52),
             ("p48-48", "p48", 48), ("p48-52", "p48", 52), ("m24-48", "m24", 48)]
    body = "".join(f'<div id="mk-{n}" style="width:max-content;align-self:flex-start;line-height:0">{lk(k, s, label=n)}</div>' for n, k, s in cells)
    cards = "".join(social_corner(k) for k in ("display", "m24", "p48"))
    tmp = out / "_measure.html"
    tmp.write_text(page("measure", body + cards))
    subprocess.run(["node", str(HERE / "stage_a_identity_shots.js"), str(tmp), str(out / "_m"), "1",
                    *[f"mk-{n}" for n, _, _ in cells], "card-display", "card-m24", "card-p48"], check=True, capture_output=True)

    def count(img):
        im = img.convert("RGB")
        px = [im.getpixel((x, y)) for y in range(im.height) for x in range(im.width)]
        n = len(px)
        np_ = (220, 217, 210)
        inked = sum(1 for p in px if sum(abs(a - b) for a, b in zip(p, np_)) > 45)
        black = sum(1 for p in px if max(p) < 70)
        red = sum(1 for p in px if p[0] > 170 and p[1] < 120 and p[2] < 120)
        return {"field_px": n, "ink_share": round(inked / n, 3), "near_black_share": round(black / n, 3), "red_px": red}
    res = {n: count(Image.open(out / "_m" / f"mk-{n}@1x.png")) for n, _, _ in cells}
    feed = {}
    for k in ("display", "m24", "p48"):
        card = Image.open(out / "_m" / f"card-{k}@1x.png").convert("RGB")
        feed[k] = {}
        for w in (500, 360):
            s = w / 1200
            small = card.resize((w, round(630 * s)), Image.LANCZOS)
            box = (round((1200 - 72 - 48) * s) - 1, round((630 - 72 - 48) * s) - 1, round((1200 - 72) * s) + 1, round((630 - 72) * s) + 1)
            crop = small.crop(box)
            feed[k][str(w)] = dict(count(crop), lockmark_px=round(48 * s, 1))
            crop.resize((crop.width * 8, crop.height * 8), Image.NEAREST).save(out / f"20261107_Feed-{FEED_NAME[k]}-{w}.png")
    for f in (out / "_m").glob("*.png"):
        f.unlink()
    (out / "_m").rmdir()
    tmp.unlink()
    return res, feed


def lockmark_board():
    out = BOARD / "lockmark"
    out.mkdir(parents=True, exist_ok=True)
    (out / "20261107_Lockmark-48px-Proposal.svg").write_text(proposal_48_svg())
    ink_, feed = measure_marks(out)

    def pct(v):
        return f"{v * 100:.0f} percent"
    masters = [("16 px master at 16 px", lk("today", 16), ink_["m16-16"]), ("24 px master at 24 px", lk("today", 24), ink_["m24-24"]),
               ("Display master at 48 px", lk("today", 48), ink_["display-48"]), ("Proposed 48 px master", lk("p48", 48), ink_["p48-48"])]
    mrow = "".join(f'<div class="cell">{m}<p class="fig" style="margin:0">{E(t)}<br>ink {pct(r["ink_share"])}, near black {pct(r["near_black_share"])}, '
                   f'lever {r["red_px"]} red px</p></div>' for t, m, r in masters)
    enl = "".join(f'<div class="cell"><div style="line-height:0">{lk(k, 4 * s)}</div><p class="fig" style="margin:0">{E(t)}, four times</p></div>'
                  for t, k, s in (("24 px master", "m24", 24), ("Proposed 48 px master", "p48", 48)))
    names = {"display": "Display master", "m24": "24 px master, doubled", "p48": "Proposed 48 px master"}
    frows = "".join(
        f'<div class="cell"><p class="fig" style="margin:0"><b>{E(names[k])}</b></p><div class="row" style="gap:16px">'
        + "".join(f'<div class="cell"><img src="20261107_Feed-{FEED_NAME[k]}-{w}.png" alt="" style="image-rendering:pixelated">'
                  f'<p class="fig" style="margin:0">Card at {w} px: lockmark {feed[k][str(w)]["lockmark_px"]:g} px, near black {pct(feed[k][str(w)]["near_black_share"])}, '
                  f'red {feed[k][str(w)]["red_px"]} px</p></div>' for w in (500, 360))
        + '</div></div>' for k in ("display", "m24", "p48"))
    body = ('<header><h1>The lockmark at two weights</h1><p class="lede">At 24 px the page header and footer draw a dense block of nine '
            'dots; at 48 and 52 px the sign-off and the masthead draw a hairline square from the display master. The plates show both in '
            'their places at true size, a proposed 48 px master drawn on the pixel grid between the two, and each candidate on a social '
            'card shrunk to the 500 and 360 px a feed shows. The section title in the page header is invented.</p></header>'
            f'<section class="plate" id="lk-today"><h2>Today: the four places at true size</h2><div class="row" style="flex-wrap:wrap;max-width:900px">{places("today")}</div></section>'
            f'<section class="plate" id="lk-proposal"><h2>Proposal: a 48 px master in the masthead and the sign-off</h2><div class="row" style="flex-wrap:wrap;max-width:900px">{places("p48")}</div>'
            '<p class="fig">The masthead draws the proposal at 52 px, 108 percent of its grid, so its edges soften there; L3 at 48 px would keep it on whole pixels.</p></section>'
            f'<section class="plate" id="lk-masters"><h2>The masters at the size each place uses</h2><div class="row" style="align-items:flex-end">{mrow}</div>'
            f'<div class="row" style="align-items:flex-end">{enl}</div></section>'
            f'<section class="plate" id="lk-feed"><h2>The sign-off when a feed shrinks the card, enlarged eight times</h2><div class="row" style="flex-wrap:wrap;max-width:1100px">{frows}</div></section>')
    html_path = out / "20261107_Lockmark-Weight-Plates.html"
    html_path.write_text(page("Lockmark weight plates", body))
    fonts = shoot(html_path, out, ["lk-today", "lk-proposal", "lk-masters", "lk-feed"],
                  {"lk-today": "Lockmark-Places-Today", "lk-proposal": "Lockmark-Places-Proposal", "lk-masters": "Lockmark-Masters-Compared",
                   "lk-feed": "Lockmark-Sign-Off-Feed-Test"})
    (out / "20261107_Lockmark-Weight-Figures.json").write_text(json.dumps({"ink_at_place_size": ink_, "feed_test": feed, "fonts_loaded": fonts,
                                                                           "method": "1x Chromium render on Newsprint; ink = channel distance from Newsprint over 45; near black = every channel under 70; red = R over 170, G and B under 120; feed = the 1200 px card reduced with Lanczos, the lockmark's box plus 1 px"},
                                                                          indent=1) + "\n")
    return ink_, feed, fonts


if __name__ == "__main__":
    LIB.INLINE_ALL[0] = True
    figs, f1 = end_mark_board()
    print("end mark", json.dumps(figs))
    print("fonts", f1)
    l6_board()
    ink_, feed, f3 = lockmark_board()
    print("ink", json.dumps(ink_))
    print("feed", json.dumps(feed))
