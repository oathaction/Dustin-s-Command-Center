"""Working view for drawing: render SVG files at several heights and stitch a contact image with
8x nearest-neighbour zooms of the small sizes. Output goes to the scratch folder only.

Run: python3 -I p1_peek.py <out_name> <height list, comma separated> <svg> [<svg> ...]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402


def main():
    name, sizes = sys.argv[1], [int(v) for v in sys.argv[2].split(",")]
    files = [Path(f) for f in sys.argv[3:]]
    jobs = []
    for i, f in enumerate(files):
        s = f.read_text()
        vb = o.viewbox(s)
        inner = s[s.find(">") + 1: s.rfind("</svg>")]
        for h in sizes:
            w = h * vb[2] / vb[3]
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(map(str, vb))}" width="{w:.3f}" height="{h}" '
                   f'style="left:0;top:0;color:{o.RED};--amp:{o.RED}">{inner}</svg>')
            jobs.append({"id": f"{i}_{h}", "w": int(w) + 1, "h": h, "bg": o.NEWS, "html": svg})
    outdir = o.SCRATCH / "peek" / name
    o.render(jobs, outdir, "peek_" + name)
    rows = []
    for i, f in enumerate(files):
        ims = [Image.open(outdir / f"{i}_{h}.png").convert("RGB") for h in sizes]
        zooms = [im.resize((im.width * 8, im.height * 8), Image.NEAREST) for im, h in zip(ims, sizes) if h <= 48]
        parts = ims + zooms
        W = sum(p.width for p in parts) + 20 * len(parts)
        H = max(p.height for p in parts) + 10
        row = Image.new("RGB", (W, H), (200, 200, 200))
        x = 0
        for p in parts:
            row.paste(p, (x, 0))
            x += p.width + 20
        rows.append(row)
    W = max(r.width for r in rows)
    H = sum(r.height for r in rows)
    sheet = Image.new("RGB", (W, H), (200, 200, 200))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height
    out = o.SCRATCH / "peek" / f"{name}.png"
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
