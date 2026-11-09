"""Pixel-fit pillar icons (DR-133, D2-496, D2-497): CL-019 Explain, CL-020
Track, CL-021 Connect and CL-022 Act at 16 and 24 px.

    python3 -I work/build/scripts/phase-2/civic_line_stage_b_pillar_fit.py [--proof DIR]

Each fit is drawn on its own pixel grid in Civic Line's hand: one line, round
caps and joins, every feature of the master and every red placement, the red
as its own shapes in the accent group. A 1 px line runs on half-pixel
centers and a 2 px line on whole-pixel centers, so every straight run fills
whole pixels; rings take centers and radii that put their four extremes on
whole pixels too. Curves and diagonals still shade at their edges, as any
curve on a pixel grid must.

Fits: at 24 px, A has a 2 px line (the utility set's weight at 24 px) and B a
1 px line (closer to the masters' light line). At 16 px, A has a 1 px line
and B a 2 px line where every feature still holds apart; where it cannot,
the fit is not drawn and the notes say why.

Writes work/build/assets/pillar-pixel-fit/svg/ and png/ (1x and 2x) and a
manifest. The black edition, the one in use under 48 px (D2-497, DR-67's
R10), is the red-black file with Pillar Red swapped for Charcoal.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import civic_line_stage_b_common as C  # noqa: E402

OUT = os.path.join(C.ROOT, "work", "build", "assets", "pillar-pixel-fit")


def n(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def mx(ax, x):
    return 2 * ax - x


# Each fit returns (base, accent): lists of SVG element strings in grid units.
# L: line, PL: polyline, PA: path, CI: circle.
def L(x1, y1, x2, y2):
    return f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}"/>'


def PL(pts):
    return '<polyline points="' + " ".join(f"{n(x)},{n(y)}" for x, y in pts) + '"/>'


def PA(d):
    return f'<path d="{d}"/>'


def CI(cx, cy, r):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}"/>'


# ------------------------------------------------------------------ Explain

def explain(size, w):
    """Open book: two page blocks bowing down to the spine, an outer cover a
    step lower with its doubled lower edge, the spine, and three red rays."""
    if size == 24 and w == 2:
        ax = 12
        pages = lambda s: PA(f"M{ax} 9 C{n(ax + s * 2)} 7 {n(ax + s * 4)} 7 {n(ax + s * 7)} 7 V17 "
                             f"C{n(ax + s * 4)} 17 {n(ax + s * 2)} 17.5 {ax} 19")
        cover = lambda s: PA(f"M{n(ax + s * 7)} 10 H{n(ax + s * 10)} V20 C{n(ax + s * 6)} 20 {n(ax + s * 3)} 20.5 {ax} 22")
        base = [pages(-1), pages(1), cover(-1), cover(1), L(ax, 9, ax, 22)]
        acc = [L(ax, 2, ax, 5), L(7, 3, 8.5, 5), L(17, 3, 15.5, 5)]
    elif size == 24 and w == 1:
        ax = 11.5
        pages = lambda s: PA(f"M{ax} 9.5 C{n(ax + s * 2.5)} 7.5 {n(ax + s * 5)} 7.5 {n(ax + s * 7)} 7.5 V17.5 "
                             f"C{n(ax + s * 4)} 17.5 {n(ax + s * 2)} 18 {ax} 19.5")
        cover = lambda s: PA(f"M{n(ax + s * 7)} 10.5 H{n(ax + s * 10)} V19.5 C{n(ax + s * 6)} 19.5 {n(ax + s * 3)} 20 {ax} 21.5")
        base = [pages(-1), pages(1), cover(-1), cover(1), L(ax, 9.5, ax, 21.5)]
        acc = [L(ax, 2.5, ax, 5.5), L(6.5, 3.5, 8.5, 5.5), L(16.5, 3.5, 14.5, 5.5)]
    elif size == 16 and w == 1:
        ax = 7.5
        pages = lambda s: PA(f"M{ax} 6.5 C{n(ax + s * 1.5)} 5.5 {n(ax + s * 3)} 5.5 {n(ax + s * 5)} 5.5 V11.5 "
                             f"C{n(ax + s * 3)} 11.5 {n(ax + s * 1.5)} 12 {ax} 12.5")
        cover = lambda s: PA(f"M{n(ax + s * 5)} 7.5 H{n(ax + s * 7)} V13.5 C{n(ax + s * 4)} 13.5 {n(ax + s * 2)} 13.8 {ax} 14.5")
        base = [pages(-1), pages(1), cover(-1), cover(1), L(ax, 6.5, ax, 14.5)]
        acc = [L(ax, 1.5, ax, 3.5), L(3.5, 2.5, 4.5, 3.5), L(11.5, 2.5, 10.5, 3.5)]
    else:
        return None
    return base, acc


# ------------------------------------------------------------------ Track

def track(size, w):
    """Route in an S with rounded turns, a hollow red pin over its start, and
    a lens whose red handle runs down to the right."""
    if size == 24 and w == 2:
        base = [PA("M8 9 H11 A2 2 0 0 1 11 13 H5 A2 2 0 0 0 5 17 H13"), CI(17, 14, 3)]
        acc = [PA("M5 7 L3.3 4.6 A2 2 0 1 1 6.7 4.6 Z"), L(19.5, 16.5, 21.5, 18.5)]
    elif size == 24 and w == 1:
        base = [PA("M7.5 9.5 H11 A2 2 0 0 1 11 13.5 H5 A2 2 0 0 0 5 17.5 H13.5"), CI(17.5, 14.5, 3)]
        acc = [PA("M4.5 7.5 L2.9 5.1 A2 2 0 1 1 6.1 5.1 Z"), L(19.8, 16.8, 21.5, 18.5)]
    elif size == 16 and w == 1:
        base = [PA("M5.5 6.5 H7.5 A1.5 1.5 0 0 1 7.5 9.5 H3.5 A1.5 1.5 0 0 0 3.5 12.5 H8.5"), CI(11.5, 10.5, 2)]
        acc = [PA("M3 5 L2 3.4 A1.25 1.25 0 1 1 4 3.4 Z"), L(13, 12, 14.5, 13.5)]
    else:
        return None
    return base, acc


# ------------------------------------------------------------------ Connect

def connect(size, w):
    """Two equal rings; their shared lens is red and the outer arcs black,
    meeting at the two crossings."""
    if size == 24 and w == 2:
        cl, cr, cy, r = 8, 16, 12, 6
    elif size == 24 and w == 1:
        cl, cr, cy, r = 7.5, 16.5, 12.5, 6
    elif size == 16 and w == 1:
        cl, cr, cy, r = 5.5, 10.5, 8.5, 4
    elif size == 16 and w == 2:
        cl, cr, cy, r = 6, 10, 8, 4
    else:
        return None
    xm = (cl + cr) / 2
    h = (r * r - ((cr - cl) / 2) ** 2) ** 0.5
    top, bot = cy - h, cy + h
    base = [PA(f"M{n(xm)} {n(top)} A{r} {r} 0 1 0 {n(xm)} {n(bot)}"),
            PA(f"M{n(xm)} {n(top)} A{r} {r} 0 1 1 {n(xm)} {n(bot)}")]
    acc = [PA(f"M{n(xm)} {n(top)} A{r} {r} 0 0 1 {n(xm)} {n(bot)}"),
           PA(f"M{n(xm)} {n(top)} A{r} {r} 0 0 0 {n(xm)} {n(bot)}")]
    return base, acc


# ------------------------------------------------------------------ Act

def act(size, w):
    """Hand with a raised index finger, three knuckles stepping down, the
    hooked thumb and the open wrist; the red ring around the fingertip, open
    where the finger enters, and three red rays."""
    if size == 24 and w == 2:
        base = [PA("M9 21 V7.5 A1.5 1.5 0 0 1 12 7.5 V13"),
                PA("M12 12 A1.5 1.5 0 0 1 15 12 V14"),
                PA("M15 13 A1.5 1.5 0 0 1 18 13 V14.5"),
                PA("M18 14 A1.5 1.5 0 0 1 21 14 V18 L19 22"),
                PA("M9 17 L7.5 15.3 A1.4 1.4 0 0 0 5.2 16.8 L8 22")]
        acc = [PA("M13.6 11.2 A5 5 0 1 0 6.9 11.2"), L(16.5, 4.5, 18, 3.5), L(17, 7.5, 19.5, 7.5), L(16.5, 10.5, 18, 11.5)]
    elif size == 24 and w == 1:
        base = [PA("M8.5 21.5 V7.5 A1.75 1.75 0 0 1 12 7.5 V13"),
                PA("M12 12 A1.5 1.5 0 0 1 15 12 V14"),
                PA("M15 13 A1.5 1.5 0 0 1 18 13 V14.5"),
                PA("M18 14 A1.5 1.5 0 0 1 21 14 V18 L19 22"),
                PA("M8.5 17 L7 15.3 A1.4 1.4 0 0 0 4.7 16.8 L7.5 22")]
        acc = [PA("M13.9 11.4 A5.4 5.4 0 1 0 6.4 11.4"), L(16.5, 4, 18, 3), L(17.5, 7.5, 19.5, 7.5), L(16.5, 11, 18, 12)]
    elif size == 16 and w == 1:
        base = [PA("M5.5 14.5 V5.5 A1.25 1.25 0 0 1 8 5.5 V9"),
                PA("M8 8.5 A1 1 0 0 1 10 8.5 V9.5"),
                PA("M10 9 A1 1 0 0 1 12 9 V10"),
                PA("M12 9.5 A1 1 0 0 1 14 9.5 V12 L12.5 15"),
                PA("M5.5 11.5 L4.5 10.5 A1 1 0 0 0 3 11.5 L4.8 15")]
        acc = [PA("M9.2 8 A3.6 3.6 0 1 0 4.3 8"), L(11, 2.5, 12, 2), L(11.5, 5, 13, 5), L(11, 7.5, 12, 8)]
    else:
        return None
    return base, acc


ICONS = [("CL-019", "Explain", explain), ("CL-020", "Track", track), ("CL-021", "Connect", connect), ("CL-022", "Act", act)]
FITS = [(24, 2, "A"), (24, 1, "B"), (16, 1, "A"), (16, 2, "B")]


def svg(icon_id, name, size, w, fit, base, acc, black=False):
    red = C.CHARCOAL if black else C.RED
    ed = "black" if black else "red-black"
    rid = f"oa-pillar-fit-{icon_id.lower()}-{size}px-fit-{fit.lower()}-{ed}"
    attrs = f'fill="none" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" id="{rid}" data-id="{icon_id}" width="{size}" height="{size}" '
            f'viewBox="0 0 {size} {size}">\n'
            f'  <title>{name}, {size} px fit {fit}</title>\n'
            f'  <desc>Oath &amp; Action Civic Line {icon_id} {name}, pixel-fit master for {size} px, fit {fit}: a {w} px line on '
            f'the pixel grid, every feature and red placement of the master kept, the red its own shapes in the accent group '
            f'(DR-133, stage B). Use at {size} px only; the black edition is the one in use under 48 px.</desc>\n'
            f'  <g id="{rid}-accent" data-part="accent" stroke="{red}" {attrs}>\n    ' + "\n    ".join(acc) + "\n  </g>\n"
            f'  <g id="{rid}-base" data-part="base" stroke="{C.CHARCOAL}" {attrs}>\n    ' + "\n    ".join(base) + "\n  </g>\n"
            "</svg>\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proof")
    a = ap.parse_args()
    os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "png"), exist_ok=True)
    jobs, recs = [], []
    for icon_id, name, fn in ICONS:
        for size, w, fit in FITS:
            r = fn(size, w)
            if r is None:
                continue
            base, acc = r
            stem = f"{C.DATE}_{icon_id}-{name}-{size}px-Fit-{fit}"
            files = {}
            for ed, black in (("Red-Black", False), ("Black", True)):
                t = svg(icon_id, name, size, w, fit, base, acc, black)
                p = os.path.join(OUT, "svg", f"{stem}-{ed}.svg")
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(t)
                files[ed] = os.path.relpath(p, C.ROOT)
                body = t.split("?>", 1)[1].strip()
                for z, suf in ((1, ""), (2, "-2x")):
                    jobs.append({"svg": body.replace(f'width="{size}" height="{size}"', f'width="{size * z}" height="{size * z}"', 1),
                                 "w": size * z, "h": size * z, "bg": None,
                                 "out": os.path.join(OUT, "png", f"{stem}-{ed}{suf}.png")})
                if a.proof:
                    for z in (1, 4):
                        jobs.append({"svg": body.replace(f'width="{size}" height="{size}"', f'width="{size * z}" height="{size * z}"', 1),
                                     "w": size * z, "h": size * z, "bg": C.NEWSPRINT,
                                     "out": os.path.join(a.proof, f"{stem}-{ed}-x{z}.png")})
            recs.append({"id": icon_id, "name": name, "size_px": size, "line_px": w, "fit": fit, "stem": stem,
                         "svg_red_black": files["Red-Black"], "svg_black": files["Black"]})
    C.render(jobs, os.path.join(a.proof or "/tmp/cl-pillar-fit", "tmp"))
    with open(os.path.join(OUT, f"{C.DATE}_Pillar-Pixel-Fit-Manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"date": C.DATE, "fits": recs}, fh, indent=1)
    if a.proof:
        rows = []
        for icon_id, name, fn in ICONS:
            cells = []
            for size, w, fit in FITS:
                stem = f"{C.DATE}_{icon_id}-{name}-{size}px-Fit-{fit}"
                f1 = os.path.join(a.proof, f"{stem}-Black-x1.png")
                if not os.path.exists(f1):
                    continue
                cells += ["(", f1, "-filter", "point", "-resize", f"{96 // size * 100}%", ")",
                          "(", os.path.join(a.proof, f"{stem}-Red-Black-x1.png"), "-filter", "point", "-resize", f"{96 // size * 100}%", ")",
                          os.path.join(a.proof, f"{stem}-Black-x1.png")]
            out = os.path.join(a.proof, f"{icon_id}-row.png")
            subprocess.run(["convert", *cells, "-bordercolor", "#c8c4bb", "-border", "3", "-background", "#c8c4bb",
                            "-gravity", "center", "+append", out], check=True)
            rows.append(out)
        subprocess.run(["convert", *rows, "-background", "#c8c4bb", "-append", os.path.join(a.proof, "pillar-fits.png")], check=True)
    for r in recs:
        print(r["stem"])


if __name__ == "__main__":
    main()
