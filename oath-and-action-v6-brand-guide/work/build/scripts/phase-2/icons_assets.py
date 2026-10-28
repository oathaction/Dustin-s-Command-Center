"""Write the icon concept masters, variants, holders, construction drawings and pixel renders.

Run: python3 -I icons_assets.py   (then icons_measure.py, then icons_board_build.py)

Masters, in work/boards/phase-2/icons/:
  20261028_Concept-A-Explain-16px.svg      16 px master, ink hinted to whole pixels
  20261028_Concept-A-Explain-24px.svg      24 px master, ink hinted to whole pixels
  20261028_Concept-A-Explain-Display.svg   display master for 48 px and up, unhinted 24-unit drawing
Concept C carries its cut in the name: 20261028_Concept-C-Line-Explain-24px.svg. Its line cut has
no 16 px master; 16 px uses the flat cut.
Each master has three paths: ink (Charcoal), seat (no fill; the 1 px ring that takes a Charcoal
keyline in a row on Newsprint) and node (Pillar Red).
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_common as C  # noqa: E402
import icons_draw as D  # noqa: E402
import icons_geom as g  # noqa: E402

KINDS = ("16px", "24px", "Display")


def kinds_for(c, cut):
    out = [f"{s}px" for s in C.sizes(c, cut)]
    return out + ["Display"]


def lay_kind(c, cut, n, kind):
    if kind == "Display":
        return D.display(c, cut, n), 24
    s = int(kind[:-2])
    return D.master(c, cut, n, s), s


def file_stem(c, cut, n, kind):
    cc = f"Concept-{c}" + (f"-{cut.title()}" if c == "C" else "")
    return f"{C.DATE}_{cc}-{D.FILE_NAME[n]}-{kind}"


def master_file(c, cut, n, kind):
    return C.OUT / f"{file_stem(c, cut, n, kind)}.svg"


def variant_file(c, cut, n, kind, colorway):
    if colorway == "Ink-Charcoal-Red":
        return master_file(c, cut, n, kind)
    return C.VARIANTS / f"{file_stem(c, cut, n, kind)}-{colorway}.svg"


def title_for(c, cut, n, kind):
    cutname = {"line": "line", "flat": "flat"}[cut]
    k = "display master" if kind == "Display" else f"{kind[:-2]} px master"
    return f"{D.LABELS[n]}, Concept {c} {cutname}, {k}. Oath &amp; Action icon concept, October 28, 2026. Proposal only."


def write_icons():
    C.OUT.mkdir(parents=True, exist_ok=True)
    C.VARIANTS.mkdir(parents=True, exist_ok=True)
    count = 0
    for (c, cut) in C.DRAWINGS:
        for n in D.ICONS:
            for kind in kinds_for(c, cut):
                lay, s = lay_kind(c, cut, n, kind)
                master_file(c, cut, n, kind).write_text(C.svg_doc(lay, s, "Ink-Charcoal-Red", title=title_for(c, cut, n, kind), master=True))
                count += 1
                for cw in C.COLORWAYS:
                    if cw == "Ink-Charcoal-Red":
                        continue
                    variant_file(c, cut, n, kind, cw).write_text(C.svg_doc(lay, s, cw))
                    count += 1
    return count


# ---------------------------------------------------------------- holders

def write_holders():
    C.HOLDERS.mkdir(parents=True, exist_ok=True)
    for shape in C.HOLDER_SHAPES:
        p = C.holder_path(shape, 100)
        for color, (fill, _) in C.HOLDER_COLORS.items():
            C.holder_file(shape, color).write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'
                f'<title>{shape.replace("-", " ")} holder, {color}</title><path d="{g.d_of(p)}" fill="{fill}"/></svg>')
    # construction drawing: the three holders with the field and live area, the smoothed corner
    # against a plain rounded corner, and their curvature
    W, H = 760, 300 + 20
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter, Arial, sans-serif">',
             "<title>Holder construction: field, live area and the smoothed corner</title>"]
    S = 200
    for i, shape in enumerate(C.HOLDER_SHAPES):
        x0 = 10 + i * 250
        hp = g.transform(C.holder_path(shape, S), 1, x0, 10)
        parts.append(f'<path d="{g.d_of(hp)}" fill="#E6E3DD" stroke="#121212" stroke-width="1.5"/>')
        f = C.FIELD_FRACTION * S
        l = C.LIVE_FRACTION * S
        parts.append(f'<rect x="{x0 + (S - f) / 2}" y="{10 + (S - f) / 2}" width="{f}" height="{f}" fill="none" stroke="#4A7C74" stroke-width="1.2"/>')
        parts.append(f'<rect x="{x0 + (S - l) / 2}" y="{10 + (S - l) / 2}" width="{l}" height="{l}" fill="none" stroke="#1F2D5A" stroke-width="1.2"/>')
        if shape == "Circle":
            parts.append(f'<circle cx="{x0 + S / 2}" cy="{10 + S / 2}" r="{C.CIRCLE_SAFE * S}" fill="none" stroke="#1F2D5A" stroke-width="1.2"/>')
        lab = {"Square": "Square", "Rounded-Square": "Rounded square, superellipse", "Circle": "Circle"}[shape]
        parts.append(f'<text x="{x0}" y="{10 + S + 26}" font-size="14" font-weight="600" fill="#121212">{lab}</text>')
    parts.append(f'<text x="10" y="{10 + S + 50}" font-size="13" fill="#45494F">Green: the 24-unit icon field, 60 percent of the side. Blue: the 20-unit live area, 50 percent of the side.</text>')
    parts.append(f'<text x="10" y="{10 + S + 68}" font-size="13" fill="#45494F">In the circle, ink also stays inside the blue circle, 80 percent of the diameter.</text>')
    parts.append("</svg>")
    (C.HOLDERS / f"{C.DATE}_Holder-Construction.svg").write_text("".join(parts))
    # corner comparison and curvature plot
    S2 = 240
    se = C.holder_path("Rounded-Square", S2)
    pl = g.plain_rounded(0, 0, S2, C.CORNER_RADIUS)
    W2, H2 = 760, 330
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" font-family="Inter, Arial, sans-serif">',
             "<title>Superellipse corner against a plain rounded corner, with curvature along one quarter</title>"]
    z = 2.2
    corner = lambda p: g.transform(p, z, -(S2 - 110) * z + 10, 10)  # noqa: E731
    parts.append('<clipPath id="cc"><rect x="10" y="10" width="242" height="242"/></clipPath>')
    parts.append(f'<g clip-path="url(#cc)"><path d="{g.d_of(corner(pl))}" fill="none" stroke="#8A8F96" stroke-width="2"/>'
                 f'<path d="{g.d_of(corner(se))}" fill="none" stroke="#121212" stroke-width="2.5"/></g>')
    parts.append('<text x="10" y="280" font-size="13" fill="#45494F">Top right corner at 2.2x. Black: the superellipse.</text>')
    parts.append('<text x="10" y="298" font-size="13" fill="#45494F">Gray: a plain border radius, 22.37 percent of the side.</text>')
    px0, py0, pw, ph = 300, 20, 430, 200
    parts.append(f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="none" stroke="#5D636D" stroke-width="1"/>')
    for pts, col, wdt in ((g.plain_corner_curvature(S2, C.CORNER_RADIUS), "#8A8F96", 2), (g.superellipse_curvature(S2, C.SUPERELLIPSE_N), "#121212", 2.5)):
        smax = pts[-1][0] or 1
        kmax = 1.6 / (C.CORNER_RADIUS * S2)
        d = " ".join(f"{'M' if i == 0 else 'L'}{px0 + p[0] / smax * pw:.1f} {py0 + ph - min(p[1], kmax) / kmax * (ph - 10):.1f}" for i, p in enumerate(pts))
        parts.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wdt}"/>')
    parts.append(f'<text x="{px0}" y="{py0 + ph + 22}" font-size="13" fill="#45494F">Curvature from the middle of the top edge to the middle of the right edge.</text>')
    parts.append(f'<text x="{px0}" y="{py0 + ph + 40}" font-size="13" fill="#45494F">Gray steps from straight to full curve. Black changes without a step.</text>')
    parts.append("</svg>")
    (C.HOLDERS / f"{C.DATE}_Holder-Superellipse-Corner.svg").write_text("".join(parts))


# ---------------------------------------------------------------- grid construction drawings

def write_grid():
    C.CONTEXT.mkdir(parents=True, exist_ok=True)
    U = 12  # px per unit
    for (c, cut), n in ((("A", "line"), "ballot"), (("B", "flat"), "ballot"), (("C", "line"), "ballot"), (("C", "flat"), "ballot")):
        lay = D.display(c, cut, n)
        W = 24 * U + 2
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="-1 -1 {W} {W}">',
                 f"<title>{D.LABELS[n]} on the 24-unit grid, Concept {c} {cut}</title>"]
        parts.append(f'<rect x="0" y="0" width="{24 * U}" height="{24 * U}" fill="#F1EFEA"/>')
        for i in range(25):
            parts.append(f'<line x1="{i * U}" y1="0" x2="{i * U}" y2="{24 * U}" stroke="#C9C5BC" stroke-width="1"/>')
            parts.append(f'<line x1="0" y1="{i * U}" x2="{24 * U}" y2="{i * U}" stroke="#C9C5BC" stroke-width="1"/>')
        parts.append(f'<rect x="{2 * U}" y="{2 * U}" width="{20 * U}" height="{20 * U}" fill="none" stroke="#4A7C74" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{12 * U}" cy="{12 * U}" r="{10 * U}" fill="none" stroke="#4A7C74" stroke-width="1"/>')
        parts.append(f'<rect x="{3 * U}" y="{3 * U}" width="{18 * U}" height="{18 * U}" fill="none" stroke="#4A7C74" stroke-width="1"/>')
        parts.append(f'<rect x="{4 * U}" y="{2 * U}" width="{16 * U}" height="{20 * U}" fill="none" stroke="#4A7C74" stroke-width="1"/>')
        parts.append(f'<rect x="{2 * U}" y="{4 * U}" width="{20 * U}" height="{16 * U}" fill="none" stroke="#4A7C74" stroke-width="1"/>')
        parts.append(f'<line x1="0" y1="{12 * U}" x2="{24 * U}" y2="{12 * U}" stroke="#1F2D5A" stroke-width="1"/>')
        parts.append(f'<line x1="{12 * U}" y1="0" x2="{12 * U}" y2="{24 * U}" stroke="#1F2D5A" stroke-width="1"/>')
        ink = g.transform(lay["ink"], U)
        node = g.transform(lay["node"], U)
        seat = g.transform(lay["seat"], U)
        parts.append(f'<path d="{g.d_of(ink)}" fill="#121212" fill-opacity="0.86"/>')
        parts.append(f'<path d="{g.d_of(seat)}" fill="none" stroke="#1F2D5A" stroke-width="1.2"/>')
        parts.append(f'<path d="{g.d_of(node)}" fill="#E63946"/>')
        parts.append("</svg>")
        cc = f"Concept-{c}" + (f"-{cut.title()}" if c == "C" else "")
        (C.CONTEXT / f"{C.DATE}_{cc}-Ballot-On-Grid.svg").write_text("".join(parts))
    # the bare grid with keylines and the 16 px grid
    for size, pad in ((24, 2), (16, 1)):
        U2 = 12 if size == 24 else 18
        W = size * U2 + 2
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="-1 -1 {W} {W}"><title>{size}-unit grid and keylines</title>',
                 f'<rect width="{size * U2}" height="{size * U2}" fill="#F1EFEA"/>']
        for i in range(size + 1):
            parts.append(f'<line x1="{i * U2}" y1="0" x2="{i * U2}" y2="{size * U2}" stroke="#C9C5BC"/>')
            parts.append(f'<line x1="0" y1="{i * U2}" x2="{size * U2}" y2="{i * U2}" stroke="#C9C5BC"/>')
        live = size - 2 * pad
        parts.append(f'<rect x="{pad * U2}" y="{pad * U2}" width="{live * U2}" height="{live * U2}" fill="none" stroke="#4A7C74" stroke-width="2"/>')
        if size == 24:
            parts.append(f'<circle cx="{12 * U2}" cy="{12 * U2}" r="{10 * U2}" fill="none" stroke="#4A7C74" stroke-width="1.2"/>')
            parts.append(f'<rect x="{3 * U2}" y="{3 * U2}" width="{18 * U2}" height="{18 * U2}" fill="none" stroke="#4A7C74" stroke-width="1.2"/>')
            parts.append(f'<rect x="{4 * U2}" y="{2 * U2}" width="{16 * U2}" height="{20 * U2}" fill="none" stroke="#4A7C74" stroke-width="1.2"/>')
            parts.append(f'<rect x="{2 * U2}" y="{4 * U2}" width="{20 * U2}" height="{16 * U2}" fill="none" stroke="#4A7C74" stroke-width="1.2"/>')
            parts.append(f'<circle cx="{12 * U2}" cy="{12 * U2}" r="{2 * U2}" fill="#E63946"/><circle cx="{12 * U2}" cy="{12 * U2}" r="{3 * U2}" fill="none" stroke="#1F2D5A" stroke-width="1.2"/>')
        else:
            parts.append(f'<circle cx="{7.5 * U2}" cy="{7.5 * U2}" r="{6.5 * U2}" fill="none" stroke="#4A7C74" stroke-width="1.2"/>')
            parts.append(f'<circle cx="{7.5 * U2}" cy="{7.5 * U2}" r="{1.5 * U2}" fill="#E63946"/><circle cx="{7.5 * U2}" cy="{7.5 * U2}" r="{2.5 * U2}" fill="none" stroke="#1F2D5A" stroke-width="1.2"/>')
        parts.append(f'<line x1="0" y1="{size / 2 * U2}" x2="{size * U2}" y2="{size / 2 * U2}" stroke="#1F2D5A"/><line x1="{size / 2 * U2}" y1="0" x2="{size / 2 * U2}" y2="{size * U2}" stroke="#1F2D5A"/>')
        parts.append("</svg>")
        (C.CONTEXT / f"{C.DATE}_Grid-{size}px-Keylines.svg").write_text("".join(parts))


# ---------------------------------------------------------------- baseline: V5 today and Direction A

def write_baseline():
    C.BASELINE.mkdir(parents=True, exist_ok=True)
    v5 = {"explain": "pm-explain", "track": "pm-track", "connect": "pm-connect", "act": "pm-act",
          "ballot": "ic-ballot-48", "money": "ic-campaign-money-48", "search": "ui-search"}
    names = {}
    for n, sym in v5.items():
        src = (C.SPRITE / f"{sym}.svg").read_text()
        src = re.sub(r"<title>.*?</title>", f"<title>V5 {D.LABELS[n]} ({sym}), today. Copied from the V5 Polished sprite for comparison.</title>", src, count=1)
        f = C.BASELINE / f"{C.DATE}_V5-{D.FILE_NAME[n]}.svg"
        f.write_text(src)
        names[f"v5|{n}"] = f.name
    lock = (C.SPRITE / "lockmark.svg").read_text()
    (C.BASELINE / f"{C.DATE}_V5-Lockmark.svg").write_text(lock)
    names["v5|lockmark"] = f"{C.DATE}_V5-Lockmark.svg"
    sprite = (C.P1_SYMBOLS / "20261021_Pillar-Sketches-Direction-A.svg").read_text()
    topics = (C.P1_SYMBOLS / "20261021_Topic-Sketches-Direction-A.svg").read_text()
    for n, sid, src in (("explain", "oa-sketch-a-filled-explain-24", sprite), ("track", "oa-sketch-a-filled-track-24", sprite),
                        ("connect", "oa-sketch-a-filled-connect-24", sprite), ("act", "oa-sketch-a-filled-act-24", sprite),
                        ("ballot", "oa-sketch-topic-ballot-24", topics), ("money", "oa-sketch-topic-campaign-money-24", topics)):
        m = re.search(rf'<symbol id="{sid}" viewBox="([^"]+)">(.*?)</symbol>', src, re.S)
        body = re.sub(r"<title>.*?</title>", "", m.group(2))
        body = body.replace('fill="currentColor"', 'fill="#121212"').replace('fill="var(--seat,none)"', 'fill="none"').replace('fill="var(--node,currentColor)"', 'fill="#121212"')
        f = C.BASELINE / f"{C.DATE}_Direction-A-{D.FILE_NAME[n]}.svg"
        f.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="{m.group(1)}"><title>Direction A {D.LABELS[n]}, approved at Gate 1, 24 px sketch from Phase 1</title>{body}</svg>')
        names[f"a|{n}"] = f.name
    (C.BASELINE / "manifest.json").write_text(json.dumps(names, indent=1))


# ---------------------------------------------------------------- pixel renders for the magnified views

def write_px():
    C.PX.mkdir(parents=True, exist_ok=True)
    jobs = []
    for (c, cut) in C.DRAWINGS:
        for n in D.ICONS:
            for s in C.sizes(c, cut):
                lay = D.master(c, cut, n, s)
                kind = f"{s}px"
                stem = file_stem(c, cut, n, kind)
                jobs.append({"id": f"{stem}-Newsprint", "w": s, "h": s, "bg": C.NEWS, "html": C.svg_doc(lay, s, "Ink-Charcoal-Red")})
                jobs.append({"id": f"{stem}-Charcoal", "w": s, "h": s, "bg": C.CHAR, "html": C.svg_doc(lay, s, "Ink-Newsprint-Red")})
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    jp = C.SCRATCH / "px-jobs.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(C.RENDER_JS), str(jp), str(C.PX)], check=True)
    return len(jobs)


APP_TILE = [("A", "line"), ("B", "flat"), ("C", "flat")]


def app_tile_file(c, cut):
    cc = f"Concept-{c}" + (f"-{cut.title()}" if c == "C" else "")
    return C.CONTEXT / f"{C.DATE}_{cc}-App-Tile-1024.svg"


def write_app_tiles():
    """A 1024 px app tile per concept: the superellipse holder in Charcoal with the Act display
    master in Newsprint and its red node, the icon's live area at half the side."""
    S = 1024
    off = S * (1 - C.FIELD_FRACTION) / 2
    sc = S * C.FIELD_FRACTION / 24
    for c, cut in APP_TILE:
        lay = D.display(c, cut, "act")
        hp = C.holder_path("Rounded-Square", S)
        app_tile_file(c, cut).write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">'
            f"<title>Act as a 1024 px app tile, Concept {c} {cut}. Superellipse holder, exponent 5. Proposal only.</title>"
            f'<path d="{g.d_of(hp)}" fill="{C.CHAR}"/>'
            f'<path d="{g.d_of(g.transform(lay["ink"], sc, off, off))}" fill="{C.NEWS}"/>'
            f'<path d="{g.d_of(g.transform(lay["node"], sc, off, off))}" fill="{C.RED}"/></svg>')


def main():
    if C.VARIANTS.exists():
        shutil.rmtree(C.VARIANTS)
    for f in C.OUT.glob(f"{C.DATE}_Concept-*.svg"):
        f.unlink()
    n = write_icons()
    write_holders()
    write_grid()
    write_baseline()
    write_app_tiles()
    p = write_px()
    print("icons", n, "px", p)


if __name__ == "__main__":
    main()
