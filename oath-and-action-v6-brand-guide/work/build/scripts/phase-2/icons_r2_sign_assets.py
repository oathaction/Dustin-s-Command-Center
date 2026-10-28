"""Concept 3, Public sign, stage 2: write every asset the board and the checks use.

Run: python3 -I icons_r2_sign_assets.py
Writes in work/boards/phase-2/icons-r2/public-sign/:
  20261028_Public-Sign-<Name>-16px.svg      16 px master, fitted to whole pixels
  20261028_Public-Sign-<Name>-24px.svg      24 px master, fitted to whole pixels
  20261028_Public-Sign-<Name>-Display.svg   display master for 48 px and up
     each with two paths: "ink" (Charcoal) and "accent" (Pillar Red)
  variants/   the same masters in every colorway of icons_r2_sign_common.COLORWAYS
  holders/    every icon in the sign panel, the superellipse and the circle, in Charcoal, Newsprint
              and Prussian, at 28 px (16 px master), 40 px (24 px master) and 96 px (display);
              plus the holder construction drawing
  context/    the 1024 px app tile at three glyph scales, the 400 px avatar, the 1080 by 1350
              social card, and the scale study renders
  px/         1x Chromium renders of the 16 and 24 px masters, for the magnified views
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_sign_common as C  # noqa: E402
from icons_r2_sign_common import CHAR, D, G, NEWS, PRUS, RED, WHITE  # noqa: E402


def title(name, kind):
    k = "display master, 48 px and up" if kind == "Display" else f"{kind[:-2]} px master, fitted to whole pixels"
    return f"{D.LABELS[name]}, Concept 3 Public sign, {k}. Oath &amp; Action icon concept, October 28, 2026. Proposal only."


def write_masters():
    n = 0
    for name in D.ICONS:
        for kind in C.KINDS:
            C.master_file(name, kind).write_text(C.svg(name, kind, "Charcoal-Red", title=title(name, kind), ids=True))
            n += 1
            for cw in C.COLORWAYS:
                if cw != "Charcoal-Red":
                    C.variant_file(name, kind, cw).write_text(C.svg(name, kind, cw))
                    n += 1
    return n


def write_holders():
    n = 0
    for name in D.ICONS:
        for shape in C.HOLDER_SHAPES:
            for color in C.HOLDER_COLORS:
                for size in (28, 40, 96):
                    s, *_ = C.tile_svg(name, shape, color, size, title=f"{D.LABELS[name]} in the {C.HOLDER_LABEL[shape].lower()}, {color} tile, {size} px")
                    C.tile_file(name, shape, color, size).write_text(s)
                    n += 1
    # construction: the sign panel at 240 px with its field, live area, circle safe zone and corner radius
    S = 240
    f, live = S * C.FIELD_FRACTION, S * C.LIVE_FRACTION
    lay = D.display("act")
    sc, off = f / 24, (S - f) / 2
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{S + 20}" height="{S + 20}" viewBox="-10 -10 {S + 20} {S + 20}">',
             "<title>The square sign panel: field, live area, circle safe zone and the 2-unit corner radius</title>",
             f'<path d="{G.d_of(C.holder_path("Sign-Panel", S))}" fill="{CHAR}"/>',
             f'<rect x="{(S - f) / 2}" y="{(S - f) / 2}" width="{f}" height="{f}" fill="none" stroke="#4A7C74" stroke-width="1.5"/>',
             f'<rect x="{(S - live) / 2}" y="{(S - live) / 2}" width="{live}" height="{live}" fill="none" stroke="#DCD9D2" stroke-width="1" stroke-dasharray="0"/>',
             f'<circle cx="{S / 2}" cy="{S / 2}" r="{C.CIRCLE_SAFE * S}" fill="none" stroke="#7E9CC0" stroke-width="1"/>',
             f'<path d="{G.d_of(G.g.transform(lay["ink"], sc, off, off))}" fill="{NEWS}" fill-opacity="0.9"/>',
             f'<path d="{G.d_of(G.g.transform(lay["accent"], sc, off, off))}" fill="{RED}"/>',
             "</svg>"]
    (C.HOLDERS / f"{C.DATE}_Public-Sign-Holder-Construction.svg").write_text("".join(parts))
    return n


APP_GLYPH = "act"
APP_SCALES = (56, 62, 66)          # the icon's 20-unit live area as a share of the tile side
APP_CHOICE = 62


def app_tile_svg(scale, size=1024, color="Charcoal", name=APP_GLYPH):
    fill, cw = C.HOLDER_COLORS[color]
    ink_c = C.COLORWAYS[cw][0]
    lay = D.display(name)
    sc = size * scale / 100 / 20
    off = size / 2 - 12 * sc
    hp = G.g.superellipse(0, 0, size, 5.0)
    acc = f'<path d="{G.d_of(G.g.transform(lay["accent"], sc, off, off))}" fill="{RED}"/>' if color != "Prussian" else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f"<title>{D.LABELS[name]} as a {size} px app tile, live area {scale} percent of the side. Superellipse, exponent 5. Proposal only.</title>"
            f'<path d="{G.d_of(hp)}" fill="{fill}"/>'
            f'<path d="{G.d_of(G.g.transform(lay["ink"], sc, off, off))}" fill="{ink_c}"/>{acc}</svg>')


def write_context():
    for sc in APP_SCALES:
        for color in ("Charcoal", "Newsprint"):
            (C.CONTEXT / f"{C.DATE}_Public-Sign-App-Tile-1024-{color}-{sc}.svg").write_text(app_tile_svg(sc, 1024, color))
    (C.CONTEXT / f"{C.DATE}_Public-Sign-App-Tile-1024.svg").write_text(app_tile_svg(APP_CHOICE, 1024, "Charcoal"))
    # avatar, 400 px, the circle holder in Charcoal with Track
    s, *_ = C.tile_svg("track", "Circle", "Charcoal", 400, title="Track as a 400 px social avatar, circle holder, Charcoal")
    (C.CONTEXT / f"{C.DATE}_Public-Sign-Avatar-400.svg").write_text(s)


def write_px():
    jobs = []
    for name in D.ICONS:
        for kind in ("16px", "24px"):
            for cw, bg in (("Charcoal-Red", NEWS), ("Newsprint-Red", CHAR), ("White-Idle", PRUS), ("Charcoal-Idle", NEWS)):
                s = int(kind[:-2])
                jobs.append({"id": f"{C.stem(name, kind)}-{cw}", "w": s, "h": s, "bg": bg, "html": C.svg(name, kind, cw)})
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    jp = C.SCRATCH / "px-jobs.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(C.RENDER_JS), str(jp), str(C.PX)], check=True)
    return len(jobs)


def main():
    for d in (C.VARIANTS, C.HOLDERS, C.CONTEXT, C.PX):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
    for f in C.OUT.glob(f"{C.DATE}_Public-Sign-*-*px.svg"):
        f.unlink()
    n = write_masters()
    h = write_holders()
    write_context()
    p = write_px()
    print("masters and variants", n, "tiles", h, "px renders", p)


if __name__ == "__main__":
    main()
