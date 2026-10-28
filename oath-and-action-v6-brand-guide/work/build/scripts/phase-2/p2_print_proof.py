"""I4 print proof: ampersand B and the identity masters at real print sizes, as a PDF.

Builds a five-page US Letter HTML proof from the Phase 2 masters (every size in mm or inches,
computed from each viewBox), prints it to PDF with Chromium (p2_print_pdf.js), then renders page 5
at 300 dpi and measures the 50 mm calibration ampersand to confirm the PDF holds true size.

The proof was generated, not printed on paper. Colors are the screen values without a press profile.

Run: python3 -I p2_print_proof.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402

OUT = P.BOARD_DIR / "04-amp-b" / f"{P.DATE}_Ampersand-B-Print-Proof.pdf"
HTML = P.SCRATCH / "print_proof.html"
A = P.ASSETS
FONT = o.FONTS


def svg(path, h_mm=None, w_mm=None, color="#121212", amp="#E63946", extra=""):
    inner, vb = P.svg_parts(path)
    if h_mm is not None:
        w_mm = h_mm * vb[2] / vb[3]
    else:
        h_mm = w_mm * vb[3] / vb[2]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(f"{v:g}" for v in vb)}" style="width:{w_mm:.3f}mm;height:{h_mm:.3f}mm;color:{color};'
            f'--amp:{amp};--lever:{amp};--line:#5D636D;--link:#5D636D;{extra}">{inner}</svg>')


def cell(content, label):
    return f'<figure>{content}<figcaption>{label}</figcaption></figure>'


def page(title, body, n):
    return (f'<section class="page"><header><p class="k">Oath &amp; Action, identity masters, print proof, page {n} of 5</p><h1>{title}</h1></header>{body}'
            '<footer>Generated on October 28, 2026 as a true-size PDF from the Phase 2 masters. This proof has not been printed on paper: '
            'press gain, paper color and ink density are untested. Colors are screen values (#E63946, #121212, #DCD9D2) with no press profile.</footer></section>')


def build_html():
    amp = A / "ampersand/20261028_Amp-B-Display-Master.svg"
    v5amp = A / "reexport/20261028_Amp-V5-Lora-Master-Reexported.svg"
    p1amp = o.OUT / "05-amp-b/20261021_Amp-B-Drawn-Master.svg"
    wm = A / "wordmark/20261028_Wordmark-Display-Master.svg"
    wmc = A / "wordmark-condensed/20261028_Wordmark-Condensed-Display-Master.svg"
    v5wm = o.SPRITE / "wordmark.svg"
    # page 1: the ampersand
    heights = [3, 4, 5, 6, 8, 10, 15, 25]
    r1 = "".join(cell(svg(amp, h, color="#E63946"), f"{h} mm") for h in heights)
    r2 = "".join(cell(svg(amp, h), f"{h} mm") for h in heights)
    r3 = "".join(cell(svg(amp, h, color="#E63946"), f"{h} mm") for h in heights)
    big = cell(svg(amp, 70, color="#E63946"), "70 mm tall: the drawing at large size, for the curves")
    p1 = (f'<h2>Pillar Red on paper</h2><div class="row">{r1}</div><h2>Charcoal, one color</h2><div class="row">{r2}</div>'
          f'<h2>Pillar Red on a Newsprint field</h2><div class="row field">{r3}</div><div class="row">{big}</div>')
    # page 2: the wordmark at both widths
    widths_in = [1.2, 1.5, 2.0, 3.0, 5.0]
    rows = ""
    for w in widths_in:
        cap_mm = w * 25.4 * 100 / 978.31
        rows += f'<div class="row wide">{cell(svg(wm, w_mm=w * 25.4), f"Today" + chr(39) + f"s width, {w:.2f} in wide, capitals {cap_mm:.1f} mm")}</div>'
        hcond = (w * 25.4) * 108 / 978.31
        rows += f'<div class="row wide">{cell(svg(wmc, h_mm=hcond), f"Condensed, same capitals ({cap_mm:.1f} mm), {hcond * 770.07 / 108 / 25.4:.2f} in wide")}</div>'
    rows += f'<div class="row wide field">{cell(svg(wm, w_mm=3 * 25.4), "On a Newsprint field, 3 in wide")}{cell(svg(wm, w_mm=3 * 25.4, amp="#121212"), "One color, Charcoal, 3 in wide")}</div>'
    p2 = rows
    # page 3: lockups and marks
    L = A / "lockups"
    p3 = '<h2>Main lockups at their print minimums and at twice that</h2>'
    for nm, f, fc, wmin, wminc in (("L2 stacked", L / "20261028_L2-Stacked-Master.svg", L / "20261028_L2-Stacked-Condensed-Master.svg", 0.80, 0.65),
                                   ("L3 horizontal", L / "20261028_L3-Horizontal-Master.svg", L / "20261028_L3-Horizontal-Condensed-Master.svg", 1.55, 1.30),
                                   ("L8 monogram", L / "20261028_L8-Monogram-Master.svg", L / "20261028_L8-Monogram-Condensed-Master.svg", 0.50, 0.50)):
        p3 += (f'<div class="row">{cell(svg(f, w_mm=wmin * 25.4), f"{nm}, {wmin:.2f} in")}{cell(svg(f, w_mm=2 * wmin * 25.4), f"{nm}, {2 * wmin:.2f} in")}'
               f'{cell(svg(fc, w_mm=wminc * 25.4), f"{nm}, condensed, {wminc:.2f} in")}{cell(svg(fc, w_mm=2 * wminc * 25.4), f"condensed, {2 * wminc:.2f} in")}</div>')
    bd = A / "badge/20261028_Hinge-Badge-Display-Master.svg"
    p3b = '<h2>Hinge-circle badge and lockmark</h2><div class="row">' + "".join(cell(svg(bd, h, color="#E63946"), f"Badge, {h / 25.4:.2f} in") for h in (6.35, 12.7, 25.4, 50.8))
    lm = A / "lockmark/20261028_Lockmark-Master-V5.svg"
    p3b += "".join(cell(svg(lm, h), f"Lockmark, {h / 25.4:.2f} in") for h in (6.35, 12.7, 25.4)) + '</div>'
    hd = A / "hinge/20261028_Hinge-Diagram-V2-Display-Master.svg"
    p3b += f'<h2>Hinge diagram V2, display master</h2><div class="row wide">{cell(svg(hd, w_mm=4 * 25.4), "4 in wide, its print minimum (labels at 7 pt)")}</div>'
    p3b += f'<div class="row wide">{cell(svg(hd, w_mm=6.5 * 25.4), "6.5 in wide")}</div>'
    # page 4: before and after, and the calibration item
    p4 = ('<h2>V5, the Phase 1 drawing and the refined B, each 12 mm and 40 mm tall</h2><div class="row">'
          + cell(svg(v5amp, 12, color="#E63946"), "V5, Lora Bold, 12 mm") + cell(svg(p1amp, 12, color="#E63946"), "B, Phase 1, 12 mm") + cell(svg(amp, 12, color="#E63946"), "B, refined, 12 mm")
          + cell(svg(v5amp, 40, color="#E63946"), "V5, 40 mm") + cell(svg(p1amp, 40, color="#E63946"), "B, Phase 1, 40 mm") + cell(svg(amp, 40, color="#E63946"), "B, refined, 40 mm") + '</div>'
          f'<h2>V5 wordmark and the Phase 2 display master, 2 in wide</h2><div class="row wide">{cell(svg(v5wm, w_mm=50.8), "V5")}{cell(svg(wm, w_mm=50.8), "Phase 2, ampersand B")}</div>'
          '<h2>Calibration</h2><div class="calib"><div class="ruler"></div>'
          f'<div class="cal">{svg(amp, 50, color="#121212")}</div><p class="cap">The ampersand at left is 50 mm tall, ink top to ink bottom. The bar is 100 mm long. '
          'Measure both on paper to check that the printer held 100 percent scale.</p></div>')
    css = f"""
@font-face{{font-family:Inter;src:url('file://{FONT}/Inter-400-normal.ttf');font-weight:400}}
@font-face{{font-family:Inter;src:url('file://{FONT}/Inter-600-normal.ttf');font-weight:600}}
@font-face{{font-family:'Inter Tight';src:url('file://{FONT}/Inter-Tight-800-normal.ttf');font-weight:800}}
@page{{size:8.5in 11in;margin:0}}
*{{box-sizing:border-box}} html,body{{margin:0;padding:0;background:#fff}}
.page{{width:8.5in;height:11in;padding:0.6in 0.6in 0.5in;position:relative;page-break-after:always;font-family:Inter;color:#121212;overflow:hidden}}
.k{{font:600 8pt/1.3 Inter;letter-spacing:.06em;text-transform:uppercase;margin:0 0 4pt}}
h1{{font:800 20pt/1.1 'Inter Tight';margin:0 0 10pt;letter-spacing:-.01em}}
h2{{font:600 10pt/1.3 Inter;margin:12pt 0 6pt}}
.row{{display:flex;flex-wrap:wrap;gap:6mm;align-items:flex-end;margin-bottom:4mm}}
.row.wide{{gap:10mm}}
.field{{background:#DCD9D2;padding:5mm}}
figure{{margin:0;display:flex;flex-direction:column;align-items:flex-start;gap:2mm}}
figcaption,.cap{{font:400 7.5pt/1.3 Inter;color:#45494F}}
footer{{position:absolute;left:0.6in;right:0.6in;bottom:0.35in;font:400 7pt/1.35 Inter;color:#45494F}}
.calib{{position:relative;height:70mm}}
.ruler{{position:absolute;left:0;top:0;width:100mm;height:1mm;background:#121212}}
.cal{{position:absolute;left:0;top:8mm}}
.calib .cap{{position:absolute;left:60mm;top:20mm;width:90mm}}
svg{{display:block;overflow:visible}}
"""
    pages = [page("Ampersand B, refined, at true size", p1, 1), page("The wordmark at both widths", p2, 2),
             page("Main lockups at both widths", p3, 3), page("The badge, the lockmark and the hinge diagram", p3b, 4),
             page("Before and after, and a calibration item", p4, 5)]
    HTML.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Identity Print Proof</title><style>{css}</style></head><body>{"".join(pages)}</body></html>')


def measure_calibration():
    """Render page 4 at 300 dpi and measure the calibration ampersand and bar."""
    import numpy as np
    from PIL import Image
    tmp = P.SCRATCH / "proof_p5"
    subprocess.run(["pdftoppm", "-f", "5", "-l", "5", "-r", "300", "-png", str(OUT), str(tmp)], check=True)
    png = next(P.SCRATCH.glob("proof_p5*.png"))
    a = np.asarray(Image.open(png).convert("L"))
    # the calibration block is the lowest content above the footer: find the 100 mm bar (a long dark row)
    dark = a < 60
    rows = dark.sum(axis=1)
    bar_rows = [y for y in range(a.shape[0]) if rows[y] > 1000]
    bar_y = max(bar_rows) if bar_rows else None
    out = {"dpi": 300}
    if bar_y:
        ys = [y for y in bar_rows if y > bar_y - 40]
        xs = np.where(dark[bar_y])[0]
        out["bar_mm"] = round((xs.max() - xs.min() + 1) / 300 * 25.4, 2)
        region = dark[bar_y + 5: bar_y + 5 + int(60 / 25.4 * 300), xs.min(): xs.min() + int(55 / 25.4 * 300)]
        yy, xx = np.where(region)
        out["calibration_amp_height_mm"] = round((yy.max() - yy.min() + 1) / 300 * 25.4, 2)
    png.unlink()
    return out


def run():
    build_html()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["node", str(P.HERE / "p2_print_pdf.js"), str(HTML), str(OUT)], check=True)
    info = subprocess.run(["pdfinfo", str(OUT)], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    size = re.search(r"Page size:\s+([^\n]+)", info).group(1)
    res = {"file": P.rel(OUT), "pages": pages, "page_size": size, **measure_calibration(), "printed_on_paper": False}
    # page previews for the board
    for n in range(1, pages + 1):
        subprocess.run(["pdftoppm", "-f", str(n), "-l", str(n), "-r", "60", "-png", "-singlefile", str(OUT), str(P.BOARD_DIR / "04-amp-b" / f"proof-page-{n}")], check=True)
    P.save_json(P.SCRATCH / "specs/print_proof.json", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), indent=1))
