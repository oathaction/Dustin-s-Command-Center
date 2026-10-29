"""DR-10 tiles: 12 per icon, 1,464 SVGs, and PNGs at 256 and 512 px.

    python3 -I build_tiles.py [--no-png]

For every icon, shape (square, rounded, circle), tile colour (charcoal,
newsprint) and colour mode (two-color, one-color): the tile shape comes first,
then the icon's bare export of the matching edition, copied verbatim inside one
group with one uniform transform (the shape's factor about the centre). A
Charcoal tile carries the light editions (red-newsprint, newsprint); a
Newsprint tile the dark ones (red-black, black). Writes
tiles/<shape>-<tile>/svg/, png-256/ and png-512/, and qa/<date>_Civic-Line-Tile-Margins.json
with every icon's smallest ink-to-edge margin per shape.
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
import cl_tiles as T  # noqa: E402

MARGINS = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Tile-Margins.json")


def sized(svg, px):
    body = svg.split("?>", 1)[-1].lstrip()
    return body.replace('width="128" height="128" viewBox="0 0 128 128"', f'width="{px}" height="{px}" viewBox="0 0 128 128"', 1)


def main():
    build(png="--no-png" not in sys.argv)


def build(ids=None, png=True):
    no_png = not png
    inv = [r for r in C.load_inventory()["icons"] if ids is None or r["id"] in ids]
    jobs = []
    margins = {sh: {} for sh in C.TILE_SHAPES}
    n_svg = 0
    for r in inv:
        bare = {ed: open(C.edition_file(r, ed), encoding="utf-8").read() for ed in C.EDITIONS}
        for sh in C.TILE_SHAPES:
            f = C.TILE_FACTORS[sh]
            margins[sh][r["id"]] = round(T.icon_margin(bare["red-black"], sh, f), 3)
            for tl in C.TILE_COLOURS:
                for md in C.TILE_MODES:
                    svg = T.tile_svg(bare[C.TILE_EDITION[(tl, md)]], r["id"], r["label"], sh, tl, md, f)
                    p = C.tile_file(r, sh, tl, md)
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    with open(p, "w", encoding="utf-8") as fh:
                        fh.write(svg)
                    n_svg += 1
                    for px in (256, 512):
                        out = C.tile_file(r, sh, tl, md, "png", px)
                        os.makedirs(os.path.dirname(out), exist_ok=True)
                        jobs.append({"svg": sized(svg, px), "w": px, "h": px, "bg": None, "out": out})
    if not no_png:
        for k in range(0, len(jobs), 600):
            with tempfile.TemporaryDirectory() as d:
                jp = os.path.join(d, "jobs.json")
                json.dump(jobs[k:k + 600], open(jp, "w"))
                rr = subprocess.run(["node", C.RENDER_JS, jp], capture_output=True, text=True)
                if rr.returncode:
                    raise SystemExit("render failed:\n" + rr.stderr[-2000:])
        for j in jobs:   # one mode for every tile PNG (RGBA), recompressed: tiles are flat colour
            Image.open(j["out"]).convert("RGBA").save(j["out"], optimize=True)
    report = {"factors": C.TILE_FACTORS, "safe_margin_units": C.TILE_SAFE_MARGIN, "shapes": {}}
    for sh, m in margins.items():
        worst = sorted(m.items(), key=lambda kv: kv[1])[:5]
        report["shapes"][sh] = {"factor": C.TILE_FACTORS[sh], "min_margin": worst[0][1], "min_margin_id": worst[0][0],
                                "five_smallest": worst, "all_clear": all(v >= C.TILE_SAFE_MARGIN for v in m.values()),
                                "per_icon": m}
    report["rounded_outline"] = T.curvature_report(T.ROUNDED_D)
    report["rounded_outline"]["max_deviation_from_exact_units"] = T.deviation_from_exact(T.ROUNDED_D)
    C.write_json(os.path.join(C.QA, os.path.basename(MARGINS)), report)
    print(f"wrote {n_svg} tile SVGs" + ("" if no_png else f" and {len(jobs)} PNGs"))
    for sh, v in report["shapes"].items():
        print(f"  {sh:8s} factor {v['factor']:.2f}: smallest margin {v['min_margin']:.2f} units ({v['min_margin_id']}); all clear of {C.TILE_SAFE_MARGIN}: {v['all_clear']}")
    return report


if __name__ == "__main__":
    main()
