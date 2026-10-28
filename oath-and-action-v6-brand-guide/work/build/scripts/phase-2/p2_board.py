"""Build work/boards/20261028_Identity-Masters-Board.html from the renders (p2_render.py), the
measurements and the master specs. Copy follows the CLAUDE.md writing rules.

Run: python3 -I p2_board.py
"""
import html
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402
import p2_amp_b as B2  # noqa: E402
import p2_pairs as PP  # noqa: E402

BOARD = o.ROOT / "work/boards/20261028_Identity-Masters-Board.html"
E = html.escape
CELLS = P.load_json(P.SCRATCH / "manifest2.json")["cells"]
MEAS = P.load_json(P.HANDOFF / f"{P.DATE}_Identity-Masters-Measurements.json")
SIM = P.load_json(P.HANDOFF / f"{P.DATE}_Ampersand-B-Similarity.json")
SPEC = {k: P.load_json(P.SCRATCH / f"specs/{k}.json") for k in ("amp_b", "wordmark", "condensed", "marks", "lockups", "reexport", "print_proof", "minsizes", "prussian")}
SURF = [("newsprint", "Newsprint"), ("white", "White"), ("charcoal", "Charcoal"), ("prussian", "Prussian")]
MODES = [("color", "Color"), ("mono", "One color")]
RULE_053 = ("The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither do the ampersands inside the hinge diagram and the hinge-circle badge, which are identity marks. "
            "The hinge diagram never shares a view with the wordmark and never stands in for the hinge divider. An icon's red accent counts as signature red when the icon stands alone, as an app tile, an avatar or a single feature icon. "
            "In a row or a menu, icons go one color and only the current one keeps its red. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: an error the reader must fix; "
            "the step a reader can take now; the one point the headline names, which in a systems figure is where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline's ampersand uses the view's working red. "
            "The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian.")


def img(cid, alt, zoom=1, lazy=True, cls=""):
    c = CELLS[cid]
    k = ' class="pix"' if zoom > 1 else (f' class="{cls}"' if cls else "")
    ld = ' loading="lazy"' if lazy else ""
    return f'<img src="{c["src"]}" width="{c["w"] * zoom}" height="{c["h"] * zoom}" alt="{E(alt)}"{k}{ld}>'


def size_label(s):
    return "display size" if s == "display" else f"{s} px"


def table(head, rows, cls="", label=None):
    h = "".join(f'<th scope="col">{E(x)}</th>' for x in head)
    b = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    return f'<div class="scroll" tabindex="0" role="region" aria-label="{E(label or head[0])} table"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def P_(*xs):
    return "".join(f"<p>{x}</p>" for x in xs)


def checks_html(checks):
    rows = []
    for name, res, note in checks:
        cls = "pass" if res.startswith("Pass") else ("fail" if res.startswith("Fail") else "na")
        rows.append([E(name), f'<span class="res {cls}">{E(res)}</span>', E(note)])
    return "<h3>Craft checks</h3>" + table(["Craft check", "Result", "What I measured or saw"], rows, "checks")


def m(pid, vk, key, default=None):
    return MEAS["pairs"].get(pid, {}).get(vk, {}).get(key, default)


def fmt(v, nd=2):
    return "n/a" if v is None else f"{v:.{nd}f}"


def pair_block(p):
    pid = p["id"]
    surfaces = p.get("surfaces", [s for s, _ in SURF])
    sl = dict(SURF)
    ml = dict(MODES)
    olab, plab = p["olab"], p["plab"]
    first_m = p.get("modes", ["color", "mono"])[0]
    out = [f'<div class="pair" id="{pid}"><h3>{E(p["label"])}</h3><div class="disp">']
    for vk, lab in (("orig", olab), ("prop", plab)):
        cid = f"{pid}__{vk}__newsprint__{first_m}__display"
        out.append(f'<figure><figcaption>{E(lab)}, display size ({p["display"]} px tall), Newsprint, {ml[first_m].lower()}</figcaption>'
                   f'<div class="scroll" tabindex="0" role="region" aria-label="{E(lab)} at display size">{img(cid, lab + " at display size", lazy=False)}</div></figure>')
    if p.get("overlay"):
        out.append(f'<figure><figcaption>Overlay at display size. <span class="k k-both"></span>both <span class="k k-orig"></span>{E(olab)} only <span class="k k-prop"></span>{E(plab)} only</figcaption>'
                   f'<div class="scroll" tabindex="0" role="region" aria-label="Overlay at display size">{img(f"overlay__{pid}__display", "Overlay at display size", lazy=False)}</div></figure>')
    out.append("</div>")
    out.append('<div class="zoom"><p class="cap">16, 24 and 48 px magnified 4x, nearest neighbor: each square is one screen pixel of the 1x render.</p><div class="zgrid">')
    for s in (16, 24, 48):
        cells = []
        for vk, lab in (("orig", olab), ("prop", plab)):
            cells.append(f'<figure><figcaption>{E(lab)}, {s} px</figcaption>{img(f"{pid}__{vk}__newsprint__{first_m}__{s}", f"{lab} at {s} px, magnified 4x", zoom=4)}</figure>')
        if p.get("overlay") and s != 48:
            cells.append(f'<figure><figcaption>Overlay, {s} px</figcaption>{img(f"overlay__{pid}__{s}", f"Overlay at {s} px, magnified 4x", zoom=4)}</figure>')
        out.append(f'<div class="scroll zrow" tabindex="0" role="region" aria-label="{s} px magnified">{"".join(cells)}</div>')
    out.append("</div></div>")
    rows = []
    for s in surfaces:
        for md in p.get("modes", ["color", "mono"]):
            if s == "prussian" and md == "color":
                continue
            for vk, lab in (("orig", olab), ("prop", plab)):
                cells = "".join(f'<figure class="c"><div class="sw s-{s}">{img(f"{pid}__{vk}__{s}__{md}__{z}", f"{lab} at {z} px on {sl[s]}, {ml[md].lower()}")}</div><figcaption>{z}</figcaption></figure>' for z in PP.SIZES)
                rows.append(f'<div class="mrow"><div class="ml"><b>{E(lab)}</b><span>{sl[s]}, {ml[md].lower()}</span></div><div class="sizes">{cells}</div></div>')
    out.append(f'<details><summary>Every surface at 1x: 16, 24, 48 and 96 px. On Prussian, one color only (Rule 05.3, treatment D)</summary><div class="scroll matrix" tabindex="0" role="region" aria-label="Surface matrix for {E(p["label"])}">{"".join(rows)}</div></details>')
    zr = []
    for s in surfaces:
        for md in p.get("modes", ["color", "mono"]):
            if s == "prussian" and md == "color":
                continue
            cells = []
            for vk, lab in (("orig", olab), ("prop", plab)):
                for z in (16, 24):
                    cells.append(f'<figure><figcaption>{E(lab)}, {z} px</figcaption><div class="sw s-{s}">{img(f"{pid}__{vk}__{s}__{md}__{z}", f"{lab} {z} px on {sl[s]}, magnified", zoom=4)}</div></figure>')
            zr.append(f'<div class="mrow"><div class="ml"><b>{sl[s]}</b><span>{ml[md]}</span></div><div class="sizes">{"".join(cells)}</div></div>')
    out.append(f'<details><summary>Magnified 4x on every surface: 16 and 24 px</summary><div class="scroll matrix" tabindex="0" role="region" aria-label="Magnified renders on every surface">{"".join(zr)}</div></details>')
    dr = []
    for s in surfaces:
        for md in p.get("modes", ["color", "mono"]):
            if s == "prussian" and md == "color":
                continue
            for vk, lab in (("orig", olab), ("prop", plab)):
                dr.append(f'<figure><figcaption>{E(lab)}, {sl[s]}, {ml[md].lower()}</figcaption><div class="scroll" tabindex="0" role="region" aria-label="{E(lab)} at display size on {sl[s]}">{img(f"{pid}__{vk}__{s}__{md}__display", f"{lab} at display size on {sl[s]}, {ml[md].lower()}")}</div></figure>')
    out.append(f'<details><summary>Display size on every surface and in one color</summary><div class="dispall">{"".join(dr)}</div></details>')
    out.append(measure_strip(p))
    out.append("</div>")
    return "".join(out)


def measure_strip(p):
    pid = p["id"]
    rows = []
    for vk, lab in (("orig", p["olab"]), ("prop", p["plab"])):
        ol = m(pid, vk, "one_color_max_offline", {})
        rc = m(pid, vk, "red_median_contrast", {})
        rows.append([E(lab), fmt(m(pid, vk, "crisp_16"), 3), fmt(m(pid, vk, "crisp_24"), 3), str(m(pid, vk, "open_counters_16", "n/a")),
                     fmt(max(ol.values()) if ol else None, 1), fmt(rc.get("newsprint 16")), fmt(rc.get("white 16")), fmt(rc.get("charcoal 16")),
                     str(m(pid, vk, "red_pixels_on_prussian", 0))])
    return ('<h4>Measured on the renders</h4>' + table(["Version", "Crisp share, 16 px", "Crisp share, 24 px", "Open counters at 16 px", "One color: largest step off the ink line",
                                                         "Red, Newsprint 16 px", "Red, White 16 px", "Red, Charcoal 16 px", "Red pixels on Prussian"], rows, "nums", label=f"Measurements for {p['label']}")
            + '<p class="cap">Crisp share passes D1-17 at 0.60. The one-color column is the largest distance, in RGB units, of any pixel from the line between surface and ink, over every one-color render: antialiasing keeps it under 8, and a second color would put it in the tens. Red is the median WCAG contrast of the ampersand\u2019s or lever\u2019s pixels, measured with the letters hidden.</p>')


def section(key, title, tag, body, rec=None):
    t = {"defect": '<span class="tag defect">Defect fix</span>', "option": '<span class="tag">Option</span>', "gate2": '<span class="tag">Option for Gate 2</span>'}[tag]
    r = f' <span class="rec">{E(rec)}</span>' if rec else ""
    return f'<section id="{key.lower()}" aria-labelledby="h-{key.lower()}"><p class="eyebrow">{key} {t}{r}</p><h2 id="h-{key.lower()}">{E(title)}</h2>{body}</section>'


def pairs_of(prefix):
    return [p for p in PP.pairs() if p["id"].startswith(prefix)]


# ---------------------------------------------------------------- B construction figure (vector, inline)

def construction_svg():
    g = B2.glyph()
    import p1_amp_b as B1
    g1 = B1.glyph()

    def yd(p):
        return o.tx(p, d=-1, f=720)
    d2, d1 = o.d_from_path(yd(g)), o.d_from_path(yd(g1))
    nodes, handles = [], []
    cur = None
    for verb, pts in yd(g).segments:
        if verb in ("moveTo", "lineTo"):
            cur = pts[-1]
            nodes.append(cur)
        elif verb == "curveTo":
            handles.append((cur, pts[0]))
            handles.append((pts[2], pts[1]))
            cur = pts[2]
            nodes.append(cur)
    hs = "".join(f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}" stroke="#4A7C74" stroke-width="1.2"/><circle cx="{b[0]:.1f}" cy="{b[1]:.1f}" r="3" fill="#4A7C74"/>' for a, b in handles)
    ns = "".join(f'<rect x="{x - 4:.1f}" y="{y - 4:.1f}" width="8" height="8" fill="#121212"/>' for x, y in nodes)
    c = B2.crossing(B2.G)
    cy = 720 - c[1]
    st = []
    geom = P.to_shapely(g)
    from shapely.geometry import LineString
    for name, (pt, ang, kind) in B2.stations(B2.G).items():
        if pt is None:
            a_, b_ = B2.crossing(B2.G), B2.arm_crossing(B2.G)
            pt = ((a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)
            ang = math.degrees(math.atan2(b_[1] - a_[1], b_[0] - a_[0]))
        aa = math.radians(ang + 90)
        line = LineString([(pt[0] - 400 * math.cos(aa), pt[1] - 400 * math.sin(aa)), (pt[0] + 400 * math.cos(aa), pt[1] + 400 * math.sin(aa))])
        inter = geom.intersection(line)
        segs = [inter] if inter.geom_type == "LineString" else list(getattr(inter, "geoms", []))
        from shapely.geometry import Point
        for sgm in segs:
            if sgm.geom_type == "LineString" and sgm.distance(Point(pt)) < 1e-6:
                (x0, y0), (x1, y1) = sgm.coords[0], sgm.coords[-1]
                col = "#121212" if kind == "thick" else ("#FFFFFF" if kind == "thin" else "#DCD9D2")
                st.append(f'<path d="M{x0:.1f} {720 - y0:.1f}L{x1:.1f} {720 - y1:.1f}" stroke="{col}" stroke-width="5"/>')
    lines = (f'<path d="M-20 {720 - 350:.1f}H700" stroke="#121212" stroke-width="2"/>'
             f'<path d="M-20 720H700M-20 20H700" stroke="#5D636D" stroke-width="1"/>')
    return (f'<svg viewBox="-30 0 730 740" role="img" aria-label="Ampersand B refined at twice its display size, with its nodes, handles, the measured stroke widths, the glyph center line and the Phase 1 outline" class="constr">'
            f'{lines}<path d="{d2}" fill="#E63946" fill-opacity="0.9"/><path d="{d1}" fill="none" stroke="#121212" stroke-width="2"/>{"".join(st)}{hs}{ns}'
            f'<circle cx="{c[0]:.1f}" cy="{cy:.1f}" r="12" fill="none" stroke="#FFFFFF" stroke-width="4"/></svg>')


# ---------------------------------------------------------------- sections

def s_i1():
    R = SPEC["reexport"]
    rows = [[f"<code>#{E(k)}</code>", " ".join(f"{x:g}" for x in v["v5_viewBox"]), E(", ".join(f"{a} {b:g}" for a, b in v["ink_outside_v5_box_units"].items())),
             " ".join(f"{x:g}" for x in v["viewBox"]), f'<code>{E(Path(v["file"]).name)}</code>'] for k, v in R.items()]
    off = max(max(m(p["id"], "prop", "one_color_max_offline", {"x": 0}).values()) for p in pairs_of("i1"))
    b = P_("Six V5 symbols cut off their own ink because each viewBox ends before the outline does. The tagline rendered without its descenders and the master ampersand lost the top of its loop. "
           "Each re-export keeps V5's outlines and origins and widens the viewBox to the exact ink, measured on the curves and rounded outward to 0.01 unit. Nothing moves on the page; placements that address these symbols keep their scale.",
           "The masters are in <code>work/build/assets/identity/reexport/</code>. The ampersand and the stacked lockup are V5's Lora drawings: they stay as the record and as the base for option A, the fallback. The taglines and the web address are the live masters for L4, L5 and L6.")
    b += table(["Symbol", "V5 viewBox", "Ink outside it (units)", "Re-exported viewBox", "File"], rows)
    b += "".join(pair_block(p) for p in pairs_of("i1"))
    b += checks_html([
        ("1 Silhouette at 16 px", "Pass", "The loop top, the tail tip and every descender render; open counters at 16 px match V5's on every symbol"),
        ("2 Pixel fit", "Not applicable", "Outlines unchanged; the small masters are items I3, I4 and I7"),
        ("3 Consistency", "Pass", "Same outlines, scale and origins as V5"),
        ("4 Overshoot", "Pass", "Unchanged; the re-export only stops the cut"),
        ("5 Similarity", "Not applicable", "No new shapes"),
        ("6 One color per surface", "Pass", f"One-color renders on all four surfaces stay within {off:.1f} RGB units of the ink line"),
        ("7 Red follows Rule 05.3", "Pass", "Red on the ampersand only; none on Prussian"),
        ("8 Contrast on four surfaces", "Fail, inherited (logotype)", "Pillar Red on Newsprint measures 2.96:1 at best; WCAG exempts logotypes. Ink measures 13.28:1 or more by token"),
        ("9 Type", "Pass", "The descenders of y, p and g are whole again"),
    ])
    return section("I1", "Re-exported outlines for the six clipped symbols", "defect", b, "Applied")


def s_i2():
    W = SPEC["wordmark"]
    v5, v2b, d = W["v5"], W["v5_glyph_2b"], W["display"]
    rows = []
    for lab, r in (("V5 as shipped", v5), ("V5 glyph with 2b (Phase 1 record)", v2b), ("Phase 2 master, ampersand B", d)):
        rows.append([E(lab), f'{r["H&"]["nearest_x"]:.3f}x', f'{r["&A"]["nearest_x"]:.3f}x', f'{r["H&"]["area_x"]:.3f}x', f'{r["&A"]["area_x"]:.3f}x',
                     f'{r["&A"]["area_x"] / r["H&"]["area_x"]:.2f}', f'{r["width_units"]:.2f}'])
    b = P_("V5 sets the ampersand 0.10x from each neighbor, ink to ink, where x is one cap height, 100 units. The wedge of white above the A's diagonal makes the right gap read wider, so the ampersand leans toward OATH. "
           "Option 2b, approved at Gate 1, sets the gaps by area: the white between the ampersand and each neighbor, counted row by row across the cap band to 0.15x past the nearest point, measures the same on both sides, and no ink sits closer than 0.07x.",
           f"Applied with ampersand B, both sides hold {d['H&']['area_x']:.3f}x of white. The nearest ink measures {d['H&']['nearest_x']:.3f}x on the left and {d['&A']['nearest_x']:.3f}x on the right, at the floor. "
           f"The display master is {d['width_units']:.2f} units wide: V5's 970.71 plus the Phase 1 pair adjustments approved with I3 (T to H and T to I open 1.4 units, I to O and O to N 2.4).")
    b += table(["Spacing", "Nearest, left", "Nearest, right", "Area, left", "Area, right", "Right over left", "Width, units"], rows)
    b += "".join(pair_block(p) for p in pairs_of("i2"))
    b += checks_html([
        ("1 Silhouette at 16 px", "Pass", "Six open counters at 16 px, as V5"),
        ("2 Pixel fit", "Not applicable", "Spacing only; the 16 and 24 px masters are item I3"),
        ("3 Consistency", "Pass", "One spacing model for the wordmark, the condensed wordmark and L8"),
        ("4 Optical balance", "Pass", f"White area {d['H&']['area_x']:.3f}x on the left and {d['&A']['area_x']:.3f}x on the right"),
        ("5 Similarity", "Not applicable", "No new shapes"),
        ("6 One color per surface", "Pass", "Within 0.8 RGB units of the ink line on all four surfaces"),
        ("7 Red follows Rule 05.3", "Pass", "Red on the ampersand only; none on Prussian"),
        ("8 Contrast on four surfaces", "Fail, inherited (logotype)", "Pillar Red on Newsprint 2.96:1; ink 13.28:1 or more by token"),
        ("9 Type", "Pass", "Nearest ink 0.070x on the right, at the floor"),
    ])
    return section("I2", "Hinge gaps by equal white area (2b)", "defect", b, "Applied")


def s_i4():
    A = SPEC["amp_b"]
    p1, p2, pn = A["phase1_first_drawing"], A["phase2_refined"], A["phase2_narrow"]
    st1, st2 = p1["stations_font_units"], p2["stations_font_units"]
    order = ["bowl stem", "diagonal", "loop left", "loop right", "waist upstroke", "loop top", "bowl bottom", "arm"]
    kinds = {"thick": "thick", "thin": "hairline", "mid": "middle"}
    rows = [[E(n), kinds[st2[n]["kind"]], f'{st1[n]["width_units"]:.1f}', f'{st2[n]["width_units"]:.1f}', f'{st2[n]["width_units"] / 7:.1f}'] for n in order]
    rows.append(["<b>Thick over thin</b>", "thickest over thinnest", f'{p1["contrast_max_over_min"]:.2f}', f'<b>{p2["contrast_max_over_min"]:.2f}</b>', ""])
    rows.append(["<b>Thick over thin, means</b>", "mean over mean", f'{p1["contrast_mean"]:.2f}', f'{p2["contrast_mean"]:.2f}', ""])
    rows.append(["Bowl stem over wordmark stem", "", f'{p1["bowl_stem_over_wordmark_stem"]:.3f}', f'{p2["bowl_stem_over_wordmark_stem"]:.3f}', ""])
    rows.append(["Waist crossing above the ink center", "", f'{p1["waist_crossing_minus_ink_center_units"]:.1f}', f'{p2["waist_crossing_minus_ink_center_units"]:.1f}', ""])
    hm = SPEC["marks"]["hinge_regular_display"]
    vr = SIM["verdict_B_refined"]
    res = SIM["results"]["B refined (Phase 2)"]
    res1 = SIM["results"]["B first drawing (Phase 1)"]
    top = sorted(res.items(), key=lambda kv: -kv[1]["silhouette_overlap_200px"])[:10]
    simrows = [[E(n), f'{r["silhouette_overlap_200px"]:.3f}', f'{res1[n]["silhouette_overlap_200px"]:.3f}', f'{r["score_16px"]:.3f}', f'{r["score_24px"]:.3f}'] for n, r in top]
    sheet = P.load_json(P.SCRATCH / "similarity_sheet.json")
    inv = {v: k for k, v in sheet.items()}
    pick = ["B refined (Phase 2)", "Lora Bold (V5 master source)", "Liberation Mono Bold", "Courier 10 Pitch Bold", "FreeMono Bold", "Bitstream Charter Bold",
            "FreeSerif Bold", "DejaVu Serif Bold", "Caladea Bold", "Liberation Serif Bold"]
    figs = "".join(f'<figure><img src="phase-2/identity/04-amp-b/similarity/{inv[n]}.png" width="{"120" if True else ""}" height="96" alt="{E(n)} ampersand, 96 px tall" loading="lazy" class="fixh"><figcaption>{E(n)}</figcaption></figure>' for n in pick)
    pp = SPEC["print_proof"]
    mk = MEAS["pairs"]
    b = P_("Every lockup carries the ampersand, so B's refinement pass came first. Gate 1 set four tests for it: raise its stroke contrast from about 1.5 to 1 toward 1.7 to 1, set its crossing on the hinge diagram's center line, refine it at twice size, and check it in print and against other serif ampersands. If B failed any of them, option A would take its place.",
           "<b>Result: B passes all four, so option A stays the unused fallback.</b> The drawing is redrawn by hand as clean cubic contours, 27 nodes against the first drawing's 41, on the same broad-nib axis.")
    b += "<h3>What changed</h3>" + P_(
        f"<b>Contrast.</b> The bowl stem rises to {p2['bowl_stem_over_wordmark_stem']:.2f} of the wordmark's stem and the hairlines fall to {p2['thin_min']:.1f} to {st2['arm']['width_units']:.1f} font units. "
        f"Thick over thin now measures {p2['contrast_max_over_min']:.2f} to 1 (the first drawing, by the same stations, {p1['contrast_max_over_min']:.2f}). Measured as means of the thick and hairline stations, it is {p2['contrast_mean']:.2f} to 1 ({p1['contrast_mean']:.2f} before).",
        f"<b>Crossing.</b> B's pen path crosses itself twice. The waist crossing, between the loop and the bowl, is its pivot, and it moves down {p1['waist_crossing'][1] - p2['waist_crossing'][1]:.1f} font units to the glyph's vertical ink center. In the hinge diagram, where the ampersand is centered on its ink, the crossing now sits {abs(hm['waist_crossing_offset_from_center_line_units']):.1f} diagram units from the center line that joins the four nodes. "
        "The arm crossing stays low: lifting it to the center line would need a new skeleton.",
        "<b>Balance.</b> The lower crossing makes the loop taller, so the loop is 13 units narrower than in the first drawing and the bowl reaches 8 units further left, which keeps the visual weight in the bowl. The serif drops 7 units and the beak gives up 4, so the beak keeps 54 units of clear space to the loop (the first drawing had 64).",
        "<b>Overshoot.</b> The loop top and the bowl bottom overshoot by 9.4 font units, 1.34 wordmark units, the same as the wordmark's O. The first drawing overshot by 1.43 and 1.71.")
    b += table(["Station", "Kind", "Phase 1, font units", "Phase 2, font units", "Phase 2, wordmark units"], rows, "nums", label="Stroke widths")
    b += '<p class="cap">Widths are chords measured square to the stroke at each station, on the outline. Font units: cap height 700; 7 font units make 1 wordmark unit. The wordmark stem is 168.6 font units.</p>'
    b += ('<h3>Refined at twice size</h3><p>The outline drawn at twice its 280 px display size. Black squares are nodes, green dots are handles. '
          'The black chords are the thick stations, white the hairlines, light the middle strokes. The black horizontal line is the glyph center line and the white ring marks the waist crossing. The thin black outline is the Phase 1 drawing.</p>'
          f'<div class="scroll" tabindex="0" role="region" aria-label="Construction drawing">{construction_svg()}</div>')
    b += "<h3>The pixel masters</h3>" + P_(
        "B now has four masters drawn on the pixel grid, each over the display drawing at its size: 16 px (14 by 16), 24 px (21 by 24), and for the condensed wordmark a narrow 16 px (12 by 16) and a narrow 24 px (18 by 24). "
        "Every horizontal and vertical edge sits on a whole pixel and the waist crossing sits on the box's middle line. Hairlines are 2 px at 16 px and 3 px at 24 px; the bowl stem 3 and 5 px. Pixel arithmetic caps the 16 px contrast at 1.5 to 1.",
        f"Crisp share, one color on Newsprint (D1-17 passes at 0.60): 16 px {fmt(mk['i4-amp']['prop']['crisp_16'], 3)}, 24 px {fmt(mk['i4-amp']['prop']['crisp_24'], 3)}, narrow 16 px {fmt(mk['i4-narrow']['prop']['crisp_16'], 3)}, narrow 24 px {fmt(mk['i4-narrow']['prop']['crisp_24'], 3)}. "
        f"V5's 16 px drawing measures {fmt(mk['i4-amp']['orig']['crisp_16'], 3)}. The narrow 16 px master drops the beak: at 12 px wide it would close the notch under the arm.")
    b += "".join(pair_block(p) for p in pairs_of("i4"))
    b += "<h3>Silhouette against every serif ampersand on this machine</h3>" + P_(
        f"I checked B against {vr['faces_checked']} faces: every style of the eight serif families installed here ({', '.join(f for f in vr['families_checked'] if f != 'Lora')}) and the three Lora files from V5. "
        "Each glyph is scaled to the same ink height, centered on its ink box, rendered at 200 px, and compared by silhouette overlap (1.0 is identical). Two rules were set before the run. "
        "Recognition: B overlaps the V5 glyph, Lora Bold, at 0.70 or more, so a reader still knows it. Distinctness: B overlaps no other face as closely as one face's Regular overlaps its own Bold (the median of eight families), the point at which two ampersands count as one design.",
        f"<b>Recognition passes</b> at {vr['recognition']['value']:.3f}. <b>Distinctness passes</b>: the nearest face is {E(vr['distinctness']['nearest_face'])} at {vr['distinctness']['value']:.3f}, under the {vr['distinctness']['threshold']:.3f} line. "
        "The margin is narrow, and the nearest faces are typewriter slabs, whose resemblance is mass more than form. The first drawing would have failed: it overlapped Courier 10 Pitch Bold at 0.713. "
        "At 16 px every ampersand looks alike, so the small-size scores in the table are for the record only. Commercial faces are not on this machine and were not checked.")
    b += table(["Face", "Overlap with B refined", "Overlap with B, Phase 1", "Score at 16 px", "Score at 24 px"], simrows, "nums", label="Nearest ampersands")
    b += f'<p class="cap">The ten nearest of {vr["faces_checked"]}. Every row is in <code>work/handoffs/phase-2/20261028_Ampersand-B-Similarity.json</code>.</p>'
    b += f'<div class="sheet scroll" tabindex="0" role="region" aria-label="Ampersand contact sheet">{figs}</div>'
    pages = "".join(f'<figure><img src="phase-2/identity/04-amp-b/proof-page-{n}.png" width="510" height="660" alt="Print proof page {n} of {pp["pages"]}, reduced" loading="lazy" class="fit"><figcaption>Page {n}, reduced to 60 dpi</figcaption></figure>' for n in range(1, pp["pages"] + 1))
    b += "<h3>Print proof</h3>" + P_(
        f'<a href="phase-2/identity/04-amp-b/20261028_Ampersand-B-Print-Proof.pdf">Open the print proof (PDF, {pp["pages"]} pages, US Letter)</a>. It sets B from 3 to 70 mm tall in Pillar Red and in Charcoal, on paper and on a Newsprint field; the wordmark at both widths from its 1.20 in print minimum to 5 in; the main lockups, badge, lockmark and hinge diagram at their print minimums; V5, the first drawing and the refinement side by side; and a calibration item.',
        f"<b>It has not been printed on paper.</b> I generated it as a true-size PDF and checked its scale on a 300 dpi render: the 100 mm bar measures {pp['bar_mm']:.2f} mm and the 50 mm calibration ampersand {pp['calibration_amp_height_mm']:.2f} mm. Press gain, paper color and ink density need a real print. At 3 mm both counters stay open in the 300 dpi render, checked by eye.")
    b += f'<div class="three">{pages}</div>'
    b += checks_html([
        ("1 Silhouette at 16 px", "Pass", f"Two open counters at 16 px in the 16 px master, three in V5's stroked drawing (its notch closes); the narrow 16 px master keeps {mk['i4-narrow']['prop']['open_counters_16']} with the beak dropped"),
        ("2 Pixel fit (D1-17)", "Pass", f"Crisp share {fmt(mk['i4-amp']['prop']['crisp_16'], 3)} at 16 px and {fmt(mk['i4-amp']['prop']['crisp_24'], 3)} at 24 px; narrow {fmt(mk['i4-narrow']['prop']['crisp_16'], 3)} and {fmt(mk['i4-narrow']['prop']['crisp_24'], 3)}"),
        ("3 Consistent weights", "Pass", f"Bowl stem {p2['bowl_stem_over_wordmark_stem']:.2f} of the wordmark stem; hairlines within 3 font units of each other; the narrow drawing keeps the same stems ({pn['contrast_max_over_min']:.2f} to 1)"),
        ("4 Overshoot", "Pass", "9.4 font units top and bottom, 1.34 wordmark units, as the O"),
        ("5 Similarity", "Pass, narrow margin", f"Lora Bold {vr['recognition']['value']:.3f}; nearest other face {vr['distinctness']['value']:.3f} against a {vr['distinctness']['threshold']:.3f} line"),
        ("6 One color per surface", "Pass", "Within 0.8 RGB units of the ink line on all four surfaces"),
        ("7 Red follows Rule 05.3", "Pass", "Signature red on Newsprint, White and Charcoal; White on Prussian; 0 red pixels on Prussian"),
        ("8 Contrast on four surfaces", "Fail on Newsprint (logotype)", f"Red median at 16 px: Newsprint {fmt(mk['i4-amp']['prop']['red_median_contrast']['newsprint 16'])}, White {fmt(mk['i4-amp']['prop']['red_median_contrast']['white 16'])}, Charcoal {fmt(mk['i4-amp']['prop']['red_median_contrast']['charcoal 16'])}; White on Prussian 13.28. V5's 16 px drawing: {fmt(mk['i4-amp']['orig']['red_median_contrast']['newsprint 16'])} on Newsprint"),
        ("9 Type", "Not applicable", "No type"),
    ])
    return section("I4", "Ampersand B, refined", "option", b, "Approved at Gate 1; B as refined goes to Gate 2")


def s_i3():
    W = SPEC["wordmark"]
    mk = MEAS["pairs"]["i3-wordmark"]
    rows = []
    for size in ("16", "24"):
        pr = W[size]["pairs"]
        rows.append([f"{size} px"] + [f'{pr[k]["nearest_px"]:.1f}' for k in ("OA", "AT", "TH", "H&", "&A", "AC", "CT", "TI", "IO", "ON")])
    b = P_("V5 draws one wordmark and scales it, so at 16 px T to H and T to I clog and I, O and N run dark. Three masters now carry ampersand B, as approved:",
           f"<b>Display</b>, from 40 px tall: the equal-area hinge (I2) and the Phase 1 pair adjustments, {W['display']['width_units']:.2f} units wide. "
           f"<b>24 px</b>, from 20 to 39 px: 22 px capitals, 5 px stems and 4 px bars on whole pixels, tracking opened 2.5 units a pair, T arms trimmed 1.5 units, {W['24']['viewBox'][2]} px wide. "
           f"<b>16 px</b>, from 16 to 19 px: 14 px capitals, 3 px stems and bars, tracking opened 5 units, T arms trimmed 4 units, {W['16']['viewBox'][2]} px wide.",
           "At 16 and 24 px the ampersand is B's own pixel master at full box height, 1.14 and 1.09 times the cap height, so the red keeps its weight beside the Charcoal capitals. Gate 1 approved this change to V5's rule.")
    b += table(["Nearest ink, px", "O A", "A T", "T H", "H &", "& A", "A C", "C T", "T I", "I O", "O N"], rows, "nums", label="Letter gaps at small sizes")
    b += "".join(pair_block(p) for p in pairs_of("i3"))
    b += checks_html([
        ("1 Silhouette at 16 px", "Pass", f"{mk['prop']['open_counters_16']} open counters at 16 px, as V5; every letter gap at least 2 px"),
        ("2 Pixel fit (D1-17)", "Pass", f"Crisp share {fmt(mk['prop']['crisp_16'], 3)} at 16 px and {fmt(mk['prop']['crisp_24'], 3)} at 24 px (V5: {fmt(mk['orig']['crisp_16'], 3)} and {fmt(mk['orig']['crisp_24'], 3)})"),
        ("3 Consistent weights", "Pass", "Stems 3 px at 16 px and 5 px at 24 px in every letter; the ampersand's stem 3 and 5 px"),
        ("4 Overshoot", "Pass", "Display: O, C and the ampersand overshoot 1.34 units; small masters hold the cap line and baseline on whole pixels"),
        ("5 Similarity", "Not applicable", "Same letters"),
        ("6 One color per surface", "Pass", "Within 0.8 RGB units of the ink line on all four surfaces"),
        ("7 Red follows Rule 05.3", "Pass", "Red on the ampersand only; none on Prussian"),
        ("8 Contrast on four surfaces", "Fail on Newsprint (logotype)", f"Red at 16 px: Newsprint {fmt(mk['prop']['red_median_contrast']['newsprint 16'])} (V5 {fmt(mk['orig']['red_median_contrast']['newsprint 16'])}), White {fmt(mk['prop']['red_median_contrast']['white 16'])}, Charcoal {fmt(mk['prop']['red_median_contrast']['charcoal 16'])}"),
        ("9 Type", "Pass", f"At 16 px the nearest ink between neighbors is {min(v['nearest_px'] for v in W['16']['pairs'].values()):.2f} px or more; T to H {W['16']['pairs']['TH']['nearest_px']:.2f} px and T to I {W['16']['pairs']['TI']['nearest_px']:.2f} px"),
    ])
    return section("I3", "Wordmark masters at display, 24 and 16 px", "option", b, "Applied")


def s_i5():
    C = SPEC["condensed"]
    d = C["display"]
    L = SPEC["lockups"]
    mk = MEAS["pairs"]
    lw = d["letter_widths"]
    A_ = d["letters"]["A"]
    N_ = d["letters"]["N"]
    b = P_("Gate 1 approved one drawing pass on a condensed wordmark at 7.5 to 1, with today's width in force until Gate 2, where Dustin chooses. "
           "Phase 1 narrowed every capital with one scale. That works for straight letters, so T, H and I keep it. It fails for round and diagonal ones, and four letters are redrawn at weight on the same metrics:",
           f"<b>O</b> (and the C cut from it): straight sides between quarter arcs, sides 22.6 units, top and bottom 19, the counter 28.8 units wide where the squeezed O had a slot. "
           f"<b>C</b>: the same curve, horizontal terminal cuts at y 40 and 68, an aperture of 28 units, 4 px at 16 px. "
           f"<b>A</b>: a flat apex 26 units wide, legs 21.5 thick at {A_['leg_angle_deg']:.1f} degrees, the bar 16.5 thick and set at y 69, so the counter above it is {A_['counter_height_above_bar']:.1f} units tall and {A_['counter_width_at_bar']:.1f} wide at the bar. "
           f"<b>N</b>: stems 22, the diagonal 18.5 thick, 0.84 of the stem as in Inter Tight, with parallel edges and notch tips blunted 0.8 units, as Inter Tight does.",
           f"The ampersand is the narrow B. Spacing follows the area model; the hinge is equal white on both sides ({d['H&']['area_x']:.3f}x). Width over ink height measures {d['ratio_width_to_ink_height']:.2f} to 1, "
           f"{d['width_units']:.2f} units against today's {SPEC['wordmark']['display']['width_units']:.2f}. The 24 and 16 px masters are pixel-fit, {C['24']['viewBox'][2]} and {C['16']['viewBox'][2]} px wide, with the bar of the A held at 3 and 2 px so its counter stays open.",
           "<b>Main lockups.</b> I count four: L1 the wordmark, L2 stacked, L3 horizontal with the lockmark, and L8 the monogram. V5's color matrix names L1, L2 and L8 as its primary lockups, and L3 is the site and email masthead, the placement readers see most. Each is drawn at both widths below, with B. L4 to L7 follow in a later step from whichever width Dustin picks.",
           "<b>A finding for Gate 2.</b> In the condensed L8, the narrow O beside the ampersand reads close to a zero: 0&amp;A. If Dustin chooses the condensed width, I recommend L8 keep today's width.")
    lrows = [["L1 wordmark", f"{SPEC['wordmark']['display']['width_units']:.2f}", f"{d['width_units']:.2f}", "Wordmark masters, display, 24 and 16 px"]]
    for lk, nm in (("L2", "stacked"), ("L3", "horizontal"), ("L8", "monogram")):
        lrows.append([f"{lk} {nm}", f'{L[f"{lk}_regular"]["width_units"]:.2f}', f'{L[f"{lk}_condensed"]["width_units"]:.2f}', f'<code>{E(Path(L[f"{lk}_regular"]["file"]).name)}</code> and the condensed file'])
    b += table(["Main lockup", "Today's width, units", "Condensed, units", "Masters"], lrows, "nums", label="Main lockups")
    sw = "".join(f'<figure><figcaption>{E(lab)}, {w} px wide</figcaption><div class="scroll" tabindex="0" role="region" aria-label="{E(lab)} {w} px wide">{img(f"sw__{k}__{w}", f"{lab} at {w} px wide")}</div></figure>' for w in (360, 180) for k, lab in (("today", "Today's width"), ("condensed", "Condensed")))
    sh = "".join(f'<figure><figcaption>{E(lab)}, 40 px tall</figcaption><div class="scroll" tabindex="0" role="region" aria-label="{E(lab)} 40 px tall">{img(f"sh__{k}__40", f"{lab} at 40 px tall")}</div></figure>' for k, lab in (("today", "Today's width"), ("condensed", "Condensed")))
    b += f'<h3>Same width, and same height</h3><p>At the same width the condensed wordmark stands 1.27 times taller. At the same height it takes 79 percent of the width.</p><div class="sizes">{sw}</div><div class="dispall">{sh}</div>'
    b += "".join(pair_block(p) for p in pairs_of("i5"))
    b += checks_html([
        ("1 Silhouette at 16 px", "Pass, with one finding", f"The condensed 16 px master keeps every counter open: {mk['i5-l1']['prop']['open_counters_16']} enclosed counters against today's {mk['i5-l1']['orig']['open_counters_16']}. In L8 the condensed O reads close to a zero"),
        ("2 Pixel fit (D1-17)", "Pass", f"Crisp share {fmt(mk['i5-l1']['prop']['crisp_16'], 3)} at 16 px and {fmt(mk['i5-l1']['prop']['crisp_24'], 3)} at 24 px (Phase 1 condensed: {fmt(mk['i5-p1']['orig']['crisp_16'], 3)} and {fmt(mk['i5-p1']['orig']['crisp_24'], 3)})"),
        ("3 Consistent weights", "Pass", "Stems 22 and round sides 22.6 units in every letter; bars 16.5 to 17.5; 3 px stems at 16 px"),
        ("4 Overshoot", "Pass", "O, C and the ampersand overshoot 1.34 units, as at today's width"),
        ("5 Similarity", "Open", "Heavy condensed capitals are common on campaign signs, as the creative director noted at Gate 1; the drawing pass removes the squeeze but not the genre"),
        ("6 One color per surface", "Pass", "Within 1.6 RGB units of the ink line on all four surfaces, lockups included"),
        ("7 Red follows Rule 05.3", "Pass", "Red on the ampersand and the lockmark's lever only; none on Prussian"),
        ("8 Contrast on four surfaces", "Fail on Newsprint (logotype)", f"Red at 16 px on Newsprint {fmt(mk['i5-l1']['prop']['red_median_contrast']['newsprint 16'])}; ink 13.28:1 or more by token"),
        ("9 Type", "Pass", f"Letter widths: O {lw['O']:.0f}, A {lw['A']:.0f}, T {lw['T']:.1f}, H {lw['H']:.1f}, C {lw['C']:.1f}, I {lw['I']:.1f}, N {lw['N']:.0f} units"),
    ])
    return section("I5", "The condensed drawing pass at 7.5 to 1", "gate2", b, "Width chosen at Gate 2")


def s_i6():
    M = SPEC["marks"]
    hd, hc, cdp, ccp = M["hinge_regular_display"], M["hinge_regular_compact"], M["hinge_condensed_display"], M["hinge_condensed_compact"]
    b = P_("Hinge diagram V2, approved at Gate 1, redrawn with ampersand B: OATH and ACTION on a line with four nodes, B in a circle at the center, two solid hairline arcs running clockwise with open chevrons, and UNDERSTAND and IMPACT under the words on the display master. "
           "The words are the display wordmark masters' own letters and spacing, at today's width and condensed. B is set at 1.25 cap heights and centered on its ink, so its waist crossing sits on the line through the nodes, "
           f"{abs(hd['waist_crossing_offset_from_center_line_units']):.1f} units off it. No line is dotted or dashed: Atlas V7 gives those to evidence grades.",
           f"Minimum widths: the display master from {hd['min_width_px']} px, where the labels reach 13 px, and the compact master from {hc['min_width_px']} px, where lines reach 1 px. Condensed: {cdp['min_width_px']} and {ccp['min_width_px']} px. "
           f"Lines are {hd['line_units']:g} units and arcs {hd['arc_units']:g} on the display master; {hc['line_units']:g} on the compact. Under Rule 05.3 the diagram is an identity mark: its ampersand is signature red, and it never shares a view with the wordmark or stands in for the hinge divider. On this board they appear together as specimens.")
    b += "".join(pair_block(p) for p in pairs_of("i6"))
    b += checks_html([
        ("1 Silhouette at 16 px", "Not applicable", "The diagram starts at 213 px wide; the 16 to 96 px cells show the compact master by height for the record"),
        ("2 Pixel fit", "Not applicable", "No small master; lines reach 1 px at each minimum width"),
        ("3 Consistent weights", "Pass", "Lines and circle share one weight; arcs and chevrons a hairline at 0.8 of it; four nodes of one size"),
        ("4 Optical balance", "Pass", f"B's crossing {abs(hd['waist_crossing_offset_from_center_line_units']):.1f} units from the center line; labels under the optical centers of their words"),
        ("5 Similarity", "Pass", "Solid arcs keep the diagram apart from V7's dotted and dashed evidence lines"),
        ("6 One color per surface", "Pass", "Within 1.7 RGB units of the ink line on all four surfaces"),
        ("7 Red follows Rule 05.3", "Pass", "Red on the ampersand only, as an identity mark; none on Prussian"),
        ("8 Contrast on four surfaces", "Pass for lines, fail for red on Newsprint", "Stone lines measure 4.29:1 on Newsprint and 6.05:1 on White by token; the red ampersand 2.96:1 on Newsprint"),
        ("9 Type", "Pass", "Labels are Inter 600 outlines at 13 px or more from each minimum width"),
    ])
    return section("I6", "Hinge diagram V2, display and compact masters", "option", b, "Applied")


def s_i7():
    mk = MEAS["pairs"]["i7-lockmark"]
    b = P_("Two small masters on the pixel grid, as approved. 16 px: node centers at 2.5, 7.5 and 12.5 px, 3 px nodes and a 5 px lever, 1 px links on whole pixel rows. "
           "24 px: centers at 3.5, 11.5 and 19.5 px, 5 px nodes and a 7 px lever. V5's master serves from 48 px. The lever stays one size up so it reads in one color.",
           f"One change from the Phase 1 drawing. Its 24 px vector discs measured {0.599:.3f} crisp, a hair under D1-17's 0.60, so the 24 px master now draws its nodes and lever as whole-pixel discs. It measures {fmt(mk['prop']['crisp_24'], 3)}. The 16 px master keeps vector discs at {fmt(mk['prop']['crisp_16'], 3)}.")
    b += "".join(pair_block(p) for p in pairs_of("i7"))
    b += checks_html([
        ("1 Silhouette at 16 px", "Pass", "Nine dots on a frame and a cross, the lever larger; 4 open squares at 16 px"),
        ("2 Pixel fit (D1-17)", "Pass", f"Crisp share {fmt(mk['prop']['crisp_16'], 3)} at 16 px and {fmt(mk['prop']['crisp_24'], 3)} at 24 px (V5: {fmt(mk['orig']['crisp_16'], 3)} and {fmt(mk['orig']['crisp_24'], 3)})"),
        ("3 Consistent weights", "Pass", "One link weight, one node size and one lever size per master"),
        ("4 Optical balance", "Pass", "The live area sits 1 px inside the box on every side"),
        ("5 Similarity", "Pass", "The Signal Grid states keep their differences: Empty has no lever, Active a Verdigris one"),
        ("6 One color per surface", "Pass", "Within 1.7 RGB units of the ink line; the lever reads by size"),
        ("7 Red follows Rule 05.3", "Pass", "Red on the lever only; none on Prussian"),
        ("8 Contrast on four surfaces", "Fail on Newsprint (logotype)", f"Red lever at 16 px: Newsprint {fmt(mk['prop']['red_median_contrast']['newsprint 16'])}, White {fmt(mk['prop']['red_median_contrast']['white 16'])}, Charcoal {fmt(mk['prop']['red_median_contrast']['charcoal 16'])}"),
        ("9 Type", "Not applicable", "No type"),
    ])
    return section("I7", "Lockmark masters at 16 and 24 px", "defect", b, "Applied")


def s_i8():
    ms = SPEC["minsizes"]
    rows = [[E(r["lockup"]), E(r["v5"]), E(r["screen"]), E(r["print"]), E(r["below"])] for r in ms["rows"]]
    from p2_render import MIN_ITEMS
    rows9 = []
    for mid, lab, _, _ in MIN_ITEMS:
        cells = []
        for vk, vl in (("orig", "V5 at its minimum"), ("prop", "Phase 2 at its minimum")):
            for s, sl_ in SURF:
                for md, mdl in MODES:
                    if s == "prussian" and md == "color":
                        continue
                    cells.append(f'<figure class="c"><div class="sw s-{s}">{img(f"min__{mid}__{vk}__{s}__{md}", f"{lab}, {vl}, {sl_}, {mdl}")}</div><figcaption>{("Phase 1" if mid == "BADGE" else "V5") if vk == "orig" else "Phase 2"}, {sl_}, {mdl.lower()}</figcaption></figure>')
        rows9.append(f'<div class="mrow"><div class="ml"><b>{E(lab)}</b><span>1x</span></div><div class="sizes">{"".join(cells)}</div></div>')
    b = P_("V5's minimum sizes leave gaps and contradict each other: L1's 120 px minimum is 13.4 px tall, L2 at 72 px has smaller capitals than L1, and L8 is both a 48 px lockup and a favicon. One rule replaces them:",
           f"<b>{E(ms['rule'])}</b>",
           "The table follows from the rule and the Phase 2 masters. Inter's capitals are 0.727 of its size, so a 13 px tagline has 9.45 px capitals. L4 to L7 are not redrawn in this pass: their rows come from V5's layouts with the re-exported taglines. "
           "The table is also a file the guide and the engineer can read: <code>work/build/assets/identity/20261028_Identity-Minimum-Sizes.json</code>.")
    b += table(["Lockup", "V5 minimum", "Screen minimum", "Print minimum", "Below the minimum"], rows, label="Minimum sizes")
    b += f'<h3>Each mark at its minimum, V5 against Phase 2, at 1x</h3><div class="scroll matrix" tabindex="0" role="region" aria-label="Minimum sizes">{"".join(rows9)}</div>'
    b += checks_html([
        ("1 Silhouette at the minimum", "Pass", f"Enclosed counters at each minimum, one color on Newsprint: the Phase 2 L1 keeps {MEAS['minimums']['L1 prop']['open_counters']} and the ampersand {MEAS['minimums']['AMP prop']['open_counters']}, as at display size. V5's L1 and ampersand close a notch at their minimums ({MEAS['minimums']['L1 orig']['open_counters']} and {MEAS['minimums']['AMP orig']['open_counters']})"),
        ("2 Pixel fit (D1-17)", "Pass for pixel masters", "The 16 px masters used at each minimum pass; L2, L3, L8 and the hinge are display masters, 0.55 to 0.60 crisp, for the record"),
        ("3 Consistency", "Pass", "One rule for every lockup; no size range without a named mark"),
        ("6 One color per surface", "Pass", "Every minimum shown in one color on all four surfaces"),
        ("8 Contrast", "Pass for taglines", "Taglines at 13 px or more on screen and 7 pt or more in print"),
        ("9 Type", "Pass", "No capitals under 14 px on screen or 3 mm in print"),
    ])
    return section("I8", "One minimum-size rule", "defect", b, "Applied")


def s_i9():
    pr = MEAS["prussian"]
    from p2_render import PRUSSIAN_ITEMS
    cells = "".join(f'<figure><div class="scroll" tabindex="0" role="region" aria-label="{E(lab)} on Prussian"><div class="sw s-prussian">{img(f"pru__{k}", f"{lab} in White on Prussian")}</div></div><figcaption>{E(lab)}</figcaption></figure>' for k, lab, _, _ in PRUSSIAN_ITEMS)
    rows = [[E(v["label"]), str(v["red_px"]), f'{v["one_color_max_offline"]:.1f}', f'{v["median_contrast"]:.2f}'] for k, v in pr.items() if "label" in v]
    v5 = "".join(f'<figure data-redspecimen="1"><div class="scroll" tabindex="0" role="region" aria-label="V5 today on Prussian, {h} px"><div class="sw s-prussian">{img(f"pru__v5today__{h}", f"V5 today: red ampersand on Prussian at {h} px, ruled out by Rule 05.3")}</div></div><figcaption>V5 today, {h} px. Pillar Red on Prussian measures 3.19:1 by token. Ruled out by Rule 05.3</figcaption></figure>' for h in (16, 96))
    n = len(SPEC["prussian"])
    b = P_("Treatment D, approved at Gate 1: on Prussian every identity mark is one color, White, ampersand and lever included. White measures 13.28:1 on Prussian. Rule 05.3 closes with “Red never sits on Prussian.”",
           f"Each master has an explicit-color White file in <code>work/build/assets/identity/prussian/</code>, {n} in all, so a producer can place it on Prussian without CSS. Every file holds one color, #FFFFFF, by a scan of its markup, and every render on Prussian has 0 red pixels.",
           "The two V5 cells below are the only red on Prussian on this board. They are labeled specimens of what the rule rules out.")
    b += f'<div class="sizes prus">{cells}</div>'
    b += table(["Mark on Prussian", "Red pixels", "One color: largest step off the ink line", "Median contrast"], rows, "nums", label="Prussian renders")
    b += '<p class="cap">Median contrast falls under 13.28 only where the mark is mostly thin antialiased line, as the lockmark\u2019s 1 px links and the badge\u2019s ring at 48 px.</p>'
    b += f'<h3>V5 today, for the record</h3><div class="sizes">{v5}</div>'
    b += "<h3>Rule 05.3, word for word (decision D2-01)</h3><blockquote>" + E(RULE_053) + "</blockquote>"
    b += checks_html([
        ("6 One color per surface", "Pass", f"{n} files, one color each; renders within 1.2 RGB units of the ink line"),
        ("7 Red follows Rule 05.3", "Pass", "0 red pixels on Prussian outside the two labeled V5 cells"),
        ("8 Contrast on Prussian", "Pass", "White 13.28:1"),
    ])
    return section("I9", "Treatment D on Prussian: one color, White", "option", b, "Applied")


def s_s9():
    M = SPEC["marks"]
    mk = MEAS["pairs"]["s9-badge"]
    b = P_("The hinge-circle badge, approved at Gate 1 with three conditions: ampersand B in the hinge diagram's ring, with no words. This is a new mark, so the comparison below sets it beside its Phase 1 drawing; V5 has no badge.",
           "<b>Condition 1, Rule 05.3 names it.</b> Met: decision D2-01 puts the badge's ampersand among the signature reds, so it does not spend a view's working red. It is signature red on Newsprint, White and Charcoal and White on Prussian.",
           "<b>Condition 2, it keeps to its jobs.</b> An article's end mark, a report's back cover and events. It never serves as an avatar or favicon, never appears near a candidate or a ballot, and never sits beside the wordmark or the hinge diagram. It never carries words or a date. These lines belong beside the mark in the guide's identity chapter.",
           f"<b>Condition 3, its 16 px master is redrawn from B's own 16 px master.</b> Met. I sampled B's 16 px master onto the badge's 10 by 10 px inner field by area, then corrected the pixels by hand: the loop keeps its three-row counter, the crossing sits on the badge's center line, and the tail's foot stays on the baseline, clear of the ring. "
           f"The ink's center of mass sits {abs(M['badge_16']['amp_centroid_offset_px'][0]):.2f} px from the center across and {M['badge_16']['amp_centroid_offset_px'][1]:.2f} px below it. The arm has no beak at this size, as in the Phase 1 drawing. "
           "The 24 px master is B's 16 px master inside a 1 px ring, and the display master is B's display drawing in the V2 ring, the ring raised to 4.6 units so it reaches 1 px at 48 px.")
    b += "".join(pair_block(p) for p in pairs_of("s9"))
    b += checks_html([
        ("1 Silhouette at 16 px", "Pass", f"{mk['prop']['open_counters_16']} enclosed regions at 16 px: the ring's inside and both counters"),
        ("2 Pixel fit (D1-17)", "Pass", f"Crisp share {fmt(mk['prop']['crisp_16'], 3)} at 16 px and {fmt(mk['prop']['crisp_24'], 3)} at 24 px"),
        ("3 Consistency", "Pass", "The 16 px ampersand comes from B's 16 px master; the 24 px master is that master unchanged"),
        ("4 Optical balance", "Pass", f"Center of mass {abs(M['badge_16']['amp_centroid_offset_px'][0]):.2f} px across and {M['badge_16']['amp_centroid_offset_px'][1]:.2f} px below the center at 16 px, the bowl's weight"),
        ("5 Similarity", "Open", "Phase 1 scored it 0.584 against a generated seal at 16 px and 0.608 at 24 px. No reader has tested whether people take it for a seal (Q-13)"),
        ("6 One color per surface", "Pass", "Within 0.8 RGB units of the ink line on all four surfaces"),
        ("7 Red follows Rule 05.3", "Pass", "Signature red, named in the rule; White on Prussian"),
        ("8 Contrast on four surfaces", "Fail on Newsprint (logotype)", "Red 2.96:1 on Newsprint, 4.17 on White, 4.49 on Charcoal; White 13.28 on Prussian"),
        ("9 Type", "Not applicable", "No words, by condition 2"),
    ])
    return section("S9", "The hinge-circle badge", "option", b, "Applied, with its three conditions")


def summary():
    rows = [
        ["I1", "Re-export the six clipped symbols", "<code>reexport/</code>, 6 files", "Applied; outlines unchanged"],
        ["I2", "Hinge gaps by equal white area", "In every wordmark and L8 master", "0.203x of white on each side"],
        ["I4", "Ampersand B as the direction, A the fallback", "<code>ampersand/</code>, 6 files", "B passes all four tests; A not needed"],
        ["I3", "Wordmark masters at display, 24 and 16 px", "<code>wordmark/</code>, 3 files", f"Crisp share {MEAS['pairs']['i3-wordmark']['prop']['crisp_16']:.3f} at 16 px, {MEAS['pairs']['i3-wordmark']['prop']['crisp_24']:.3f} at 24"],
        ["I5", "The condensed drawing pass at 7.5 to 1", "<code>wordmark-condensed/</code>, 3 files; <code>lockups/</code>, 6 files", "Ready for the Gate 2 choice"],
        ["I6", "Hinge diagram V2, display and compact", "<code>hinge/</code>, 4 files", "Crossing on the center line"],
        ["I7", "Lockmark masters at 16 and 24 px", "<code>lockmark/</code>, 3 files", f"Crisp share {MEAS['pairs']['i7-lockmark']['prop']['crisp_16']:.3f} at 16 px, {MEAS['pairs']['i7-lockmark']['prop']['crisp_24']:.3f} at 24"],
        ["I8", "One minimum-size rule", "<code>20261028_Identity-Minimum-Sizes.json</code>", "A table for every mark"],
        ["I9", "Treatment D on Prussian", f"<code>prussian/</code>, {len(SPEC['prussian'])} files", "One color each; 0 red on Prussian"],
        ["S9", "The hinge-circle badge, three conditions", "<code>badge/</code>, 3 files", "All three conditions met"],
    ]
    return ('<section id="summary" aria-labelledby="h-sum"><h2 id="h-sum">The ten approved changes, as masters</h2>'
            + table(["Item", "Approved at Gate 1", "Masters in work/build/assets/identity/", "Result"], [[f'<a href="#{r[0].lower()}">{r[0]}</a>'] + r[1:] for r in rows], label="Summary") + '</section>')


def decisions():
    rows = [
        ("Ampersand B as refined", "Approve B as refined, or return it for another pass, or move to A", "Approve. It passes the contrast, crossing, print-scale and silhouette tests, and its pixel masters pass D1-17."),
        ("The wordmark's width", "Today's width, or the condensed drawing at 7.5 to 1", "Today's width. The condensed drawing passes the craft checks, but it gains only height, it sits close to campaign-sign lettering, and its monogram reads as 0&A."),
        ("L8 if the condensed width is chosen", "Condensed L8, or L8 at today's width", "Today's width, so the O cannot read as a zero."),
    ]
    tr = "".join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in rows)
    return ('<section id="decisions" aria-labelledby="h-dec"><div class="decision"><p class="eyebrow">Decisions for Gate 2</p><h2 id="h-dec">What Dustin decides next</h2>'
            '<p>Until Gate 2, today’s width stays in force and B goes forward as refined. My recommendation follows each item.</p>'
            f'<div class="scroll" tabindex="0" role="region" aria-label="Decisions table"><table><thead><tr><th scope="col">Decision</th><th scope="col">Options</th><th scope="col">Recommendation</th></tr></thead><tbody>{tr}</tbody></table></div></div></section>')


def tested():
    return ('<section id="tested" aria-labelledby="h-t"><h2 id="h-t">What I checked and what I could not</h2><div class="tested"><div><h3>Checked</h3><ul>'
            '<li>Every cell rendered in Chromium on Linux at device scale 1 from the masters in <code>work/build/assets/identity/</code>.</li>'
            '<li>Stroke widths of B as chords on the outline; its crossings from its corners; overshoot from the curves.</li>'
            '<li>Crisp share, open counters, one-color purity and contrast from the renders; numbers in <code>work/handoffs/phase-2/20261028_Identity-Masters-Measurements.json</code>.</li>'
            '<li>B against 33 ampersands: every serif face installed here and the V5 Lora files.</li>'
            '<li>The print proof’s scale on a 300 dpi render of the PDF.</li>'
            '<li>Every treatment D file scanned for colors other than White.</li>'
            '<li>This board at 1440 and 390 px wide, panels closed and open: page width, text size, images loaded, red pixels on Prussian.</li></ul></div>'
            '<div><h3>Not checked</h3><ul><li>Paper: the proof has not been printed, so press gain and paper color are untested.</li>'
            '<li>Windows, macOS, Firefox, Safari and high-density screens: pixel fit holds for 1x Chromium on Linux.</li>'
            '<li>Commercial serif ampersands: none are installed, and this session cannot download them.</li>'
            '<li>Readers: the similarity, pixel-fit and optical judgments are studio thresholds that no reader has tested (Q-13).</li>'
            '<li>Trademark clearance of B or the badge (Q-12).</li><li>Screen readers on this board.</li></ul></div></div></section>')


CSS = """
.board{max-width:1280px}
.intro{display:grid;gap:12px}
.toc{columns:2 280px;padding-left:20px;margin:8px 0 0}
.toc a,.board a{color:var(--fg)}
.tag{margin-left:6px}
.rec{font:600 .8125rem/1.4 var(--body);margin-left:6px;color:var(--fg)}
.pair{margin:28px 0;padding:16px;border:1px solid var(--rule);background:var(--surface);min-width:0}
.pair h3{margin-bottom:12px}
h4{font:600 .9375rem/1.4 var(--body);margin:16px 0 8px}
.disp{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:flex-start;margin-bottom:12px}.disp figure{min-width:0;max-width:100%}
figure{margin:0}
figcaption{font-size:.8125rem;line-height:1.4;color:var(--muted);margin-bottom:4px}
.scroll{overflow-x:auto;max-width:100%}
.scroll:focus-visible{outline:3px solid var(--prussian);outline-offset:2px}
.scroll img{max-width:none;display:block}
.disp .scroll img,.dispall .scroll img{max-width:100%;height:auto}
.zoom{margin:12px 0}
.zgrid{display:grid;gap:12px}
.zrow{display:flex;gap:16px;align-items:flex-start;padding-bottom:4px}
.zrow figure{flex:0 0 auto}
.pix{image-rendering:pixelated;image-rendering:crisp-edges}
details{margin-top:10px;border-top:1px solid var(--rule);padding-top:8px}
summary{cursor:pointer;font:600 .9375rem/1.4 var(--body);padding:6px 0}
summary:focus-visible{outline:3px solid var(--prussian);outline-offset:2px}
.matrix{display:grid;gap:6px;padding:8px 0}
.mrow{display:grid;grid-template-columns:150px 1fr;gap:10px;align-items:start}
.ml{display:grid;font-size:.8125rem;line-height:1.35}
.ml span{color:var(--muted)}
.sizes{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end}
.c{margin:0}.c figcaption{margin:2px 0 0}
.sw{padding:6px;display:inline-block}
.dispall{display:grid;gap:10px}
.s-newsprint{background:#DCD9D2}.s-white{background:#FFFFFF}.s-charcoal{background:#121212}.s-prussian{background:#1F2D5A}
.k{display:inline-block;width:12px;height:12px;vertical-align:-1px;margin:0 3px 0 8px;border:1px solid var(--rule)}
.k-both{background:#121212}.k-orig{background:#A8ACB2}.k-prop{background:#4A7C74}
table.checks td:nth-child(2){white-space:nowrap}
table.nums td{font-variant-numeric:tabular-nums}
.res{font-weight:700}.res.pass{color:#1E4F47}.res.fail{color:#9E1B26}.res.na{color:var(--muted)}
.three{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}.three figure{margin:0}.three img.fit{width:100%;height:auto;max-width:100%;border:1px solid var(--rule);background:#fff}
.constr{width:100%;max-width:730px;min-width:300px;height:auto;background:#fff;border:1px solid var(--rule);display:block}
.sheet{display:flex;gap:10px;padding:8px 0}.sheet figure{flex:0 0 auto;width:120px}.sheet img.fixh{height:96px;width:auto;max-width:none;display:block}
.prus{background:transparent}.sizes>figure{max-width:100%;min-width:0}
blockquote{margin:12px 0;padding:12px 16px;border-left:4px solid var(--prussian);background:var(--surface);max-width:80ch}
.decision table th,.decision table td{border-bottom-color:rgba(220,217,210,.45);color:var(--newsprint)}
.decision table th{text-transform:none;letter-spacing:0;font-size:.875rem}
.decision h2,.decision .eyebrow{color:var(--newsprint)}
.tested{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
code{font-size:.8125rem;overflow-wrap:anywhere}
.scroll>table{min-width:640px}.scroll>table.nums{min-width:720px}
p code{overflow-wrap:anywhere}
@media (max-width:760px){.mrow{grid-template-columns:1fr}}
"""


def page(parts):
    toc = [("summary", "The ten changes"), ("i1", "I1 Re-exported outlines"), ("i2", "I2 Equal hinge gaps"), ("i4", "I4 Ampersand B, refined"), ("i3", "I3 Wordmark masters"),
           ("i5", "I5 The condensed drawing"), ("i6", "I6 Hinge diagram V2"), ("i7", "I7 Lockmark masters"), ("i8", "I8 Minimum sizes"), ("i9", "I9 Treatment D on Prussian"),
           ("s9", "S9 The hinge-circle badge"), ("decisions", "Decisions for Gate 2"), ("tested", "What I checked")]
    intro = ('<header class="intro"><p class="eyebrow">Oath &amp; Action Brand Guide, Edition 06. Phase 2, October 28, 2026</p>'
             '<h1>Identity masters</h1>'
             '<p>Dustin approved ten identity changes at Gate 1 (decisions G1-01 and G1-02). This board shows each one applied as a master in <code>work/build/assets/identity/</code>, beside the V5 master it replaces. V5’s masters stay in <code>work/extract/</code> as the record.</p>'
             '<p>Each pair shows V5 and the new master at 16, 24, 48 and 96 px tall and at display size. Small sizes also appear magnified 4x with nearest-neighbor scaling, so each square is one screen pixel. The other surfaces and the one-color versions sit in the panels under each pair. Every image is a Chromium render at device scale 1.</p>'
             '<p>Two choices wait for Gate 2: ampersand B as refined, and the wordmark’s width. Item I5 sets the condensed drawing beside today’s width for each main lockup.</p>'
             '<p>Tags: <span class="tag defect">Defect fix</span> repairs something V5 gets wrong. <span class="tag">Option</span> was a choice, now approved. In the text, x means one cap height of the wordmark, 100 units.</p>'
             '<nav aria-label="Items on this board"><ol class="toc">' + "".join(f'<li><a href="#{a}">{E(t)}</a></li>' for a, t in toc) + '</ol></nav></header>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Identity Masters Board</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="board-base.css"><style>{CSS}</style></head><body><main class="board">{intro}{"".join(parts)}{decisions()}{tested()}</main></body></html>')


if __name__ == "__main__":
    parts = [summary(), s_i1(), s_i2(), s_i4(), s_i3(), s_i5(), s_i6(), s_i7(), s_i8(), s_i9(), s_s9()]
    BOARD.write_text(page(parts))
    print(BOARD, BOARD.stat().st_size)
