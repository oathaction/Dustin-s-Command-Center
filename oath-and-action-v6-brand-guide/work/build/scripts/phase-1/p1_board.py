"""Build work/boards/20261021_Identity-Refinement-Board.html from the rendered cells
(p1_render.py) and the measurements. Text follows the CLAUDE.md writing rules.

Run: python3 -I p1_board.py
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p1 as o  # noqa: E402
import p1_pairs as PP  # noqa: E402

BOARD = o.ROOT / "work/boards/20261021_Identity-Refinement-Board.html"
MAN = json.loads((o.SCRATCH / "manifest.json").read_text())
CELLS = MAN["cells"]
MEAS = MAN["measures"]
SPEC = {k: json.loads((o.SCRATCH / f"specs/{k}.json").read_text()) for k in ("p01", "wordmark", "wordmark_amp", "condensed", "marks")}
SIM = json.loads((o.ROOT / "work/handoffs/phase-1/20261021_Ampersand-Similarity.json").read_text())["results"]
SURF = [("newsprint", "Newsprint"), ("white", "White"), ("charcoal", "Charcoal"), ("prussian", "Prussian")]
MODES = [("color", "Color"), ("mono", "One color")]
E = html.escape


def img(cid, alt, zoom=1, cls="", lazy=True):
    c = CELLS[cid]
    w, h = c["w"] * zoom, c["h"] * zoom
    k = ' class="pix' + (" " + cls if cls else "") + '"' if zoom > 1 else (f' class="{cls}"' if cls else "")
    ld = ' loading="lazy"' if lazy else ""
    return f'<img src="{c["src"]}" width="{w}" height="{h}" alt="{E(alt)}"{k}{ld}>'


def size_label(s):
    return "display size" if s == "display" else f"{s} px"


def pair_block(p):
    pid = p["id"]
    surfaces = p.get("surfaces", [s for s, _ in SURF])
    modes = p.get("modes", ["color", "mono"]) if p["panel"] != 10 else ["color"]
    sl = dict(SURF)
    ml = dict(MODES)
    first_s, first_m = surfaces[0], modes[0]
    out = [f'<div class="pair" id="{pid}"><h3>{E(p["label"])}</h3>']
    # display size, first surface
    out.append('<div class="disp">')
    for vk, lab in (("orig", "Original, V5"), ("prop", "Proposal")):
        cid = f"{pid}__{vk}__{first_s}__{first_m}__display"
        out.append(f'<figure><figcaption>{lab}, {size_label("display")} ({p["display"]} px tall), {sl[first_s]}, {ml[first_m].lower()}</figcaption>'
                   f'<div class="scroll" tabindex="0" role="region" aria-label="{lab} at display size">{img(cid, lab + " at display size", lazy=False)}</div></figure>')
    if p.get("overlay"):
        cid = f"overlay__{pid}__display"
        out.append(f'<figure><figcaption>Overlay at display size. <span class="k k-both"></span>both <span class="k k-orig"></span>original only <span class="k k-prop"></span>proposal only</figcaption>'
                   f'<div class="scroll" tabindex="0" role="region" aria-label="Overlay at display size">{img(cid, "Overlay of original and proposal at display size", lazy=False)}</div></figure>')
    out.append("</div>")
    # magnified small sizes on the first surface
    zs = [16, 24] + ([48] if p["panel"] in (1, 4, 5, 8) and pid not in ("p01-tl-1", "p01-tl-2a", "p01-tl-2b", "p01-url-1") else [])
    out.append('<div class="zoom"><p class="cap">Magnified 4x, nearest neighbor: each square is one screen pixel of the 1x render.</p><div class="zgrid">')
    for s in zs:
        cells = []
        for vk, lab in (("orig", "Original"), ("prop", "Proposal")):
            cid = f"{pid}__{vk}__{first_s}__{first_m}__{s}"
            cells.append(f'<figure><figcaption>{lab}, {s} px</figcaption>{img(cid, f"{lab} at {s} px, magnified 4x", zoom=4)}</figure>')
        if p.get("overlay"):
            cells.append(f'<figure><figcaption>Overlay, {s} px</figcaption>{img(f"overlay__{pid}__{s}", f"Overlay at {s} px, magnified 4x", zoom=4)}</figure>')
        out.append(f'<div class="scroll zrow" tabindex="0" role="region" aria-label="{s} px magnified">{"".join(cells)}</div>')
    out.append("</div></div>")
    # matrix at 1x
    rows = []
    for s in surfaces:
        for m in modes:
            for vk, lab in (("orig", "Original"), ("prop", "Proposal")):
                cells = "".join(f'<figure class="c"><div class="sw s-{s}">{img(f"{pid}__{vk}__{s}__{m}__{z}", f"{lab} at {z} px on {sl[s]}, {ml[m].lower()}")}</div><figcaption>{z}</figcaption></figure>' for z in PP.SIZES)
                rows.append(f'<div class="mrow"><div class="ml"><b>{lab}</b><span>{sl[s]}, {ml[m].lower()}</span></div><div class="sizes">{cells}</div></div>')
    out.append(f'<details><summary>Every surface and color mode at 1x: 16, 24, 48 and 96 px</summary><div class="scroll matrix" tabindex="0" role="region" aria-label="Surface matrix for {E(p["label"])}">{"".join(rows)}</div></details>')
    # magnified on every surface
    zr = []
    for s in surfaces:
        for m in modes:
            cells = []
            for vk, lab in (("orig", "Original"), ("prop", "Proposal")):
                for z in (16, 24):
                    cells.append(f'<figure><figcaption>{lab}, {z} px</figcaption><div class="sw s-{s}">{img(f"{pid}__{vk}__{s}__{m}__{z}", f"{lab} {z} px on {sl[s]}, magnified", zoom=4)}</div></figure>')
            zr.append(f'<div class="mrow"><div class="ml"><b>{sl[s]}</b><span>{ml[m]}</span></div><div class="sizes">{"".join(cells)}</div></div>')
    out.append(f'<details><summary>Magnified 4x on every surface: 16 and 24 px</summary><div class="scroll matrix" tabindex="0" role="region" aria-label="Magnified renders, every surface">{"".join(zr)}</div></details>')
    # display on every surface
    dr = []
    for s in surfaces:
        for m in modes:
            for vk, lab in (("orig", "Original"), ("prop", "Proposal")):
                dr.append(f'<figure><figcaption>{lab}, {sl[s]}, {ml[m].lower()}</figcaption><div class="scroll" tabindex="0" role="region" aria-label="{lab} display size on {sl[s]}">{img(f"{pid}__{vk}__{s}__{m}__display", f"{lab} at display size on {sl[s]}, {ml[m].lower()}")}</div></figure>')
    out.append(f'<details><summary>Display size on every surface and in one color</summary><div class="dispall">{"".join(dr)}</div></details>')
    out.append("</div>")
    return "".join(out)


def table(head, rows, cls=""):
    h = "".join(f"<th scope=\"col\">{E(x)}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    return f'<div class="scroll" tabindex="0" role="region" aria-label="{E(head[0])} table"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def checks_html(checks):
    rows = []
    for name, res, note in checks:
        cls = {"Pass": "pass", "Fail": "fail"}.get(res, "na")
        rows.append([E(name), f'<span class="res {cls}">{E(res)}</span>', E(note)])
    return table(["Craft check", "Result", "What I measured or saw"], rows, "checks")


def scores_html(sc, why):
    crit = ["Craft", "Clarity", "Brand fidelity", "Usefulness", "Evidence honesty", "Accessibility"]
    cells = [f'<span class="score{" low" if sc[i] < 4 else ""}">{sc[i]}</span>' for i in range(6)]
    return table(["Rubric (Master Brief V2, section 6)"] + crit[1:] if False else crit, [cells]) + f'<p class="cap">{E(why)}</p>'


def red_row(pid, vk, size):
    m = MEAS.get(pid, {}).get("red", {})
    vals = []
    for s, lab in SURF:
        r = m.get(f"{vk} {s} {size}")
        vals.append(f'{r["median_contrast"]:.2f}' if r and "median_contrast" in r else "n/a")
    return vals


def red_table(pid, sizes=(16, 24), label="Median contrast of the ampersand's pixels against the surface"):
    rows = []
    for vk, lab in (("orig", "Original"), ("prop", "Proposal")):
        for s in sizes:
            rows.append([f"{lab}, {s} px"] + red_row(pid, vk, s))
    return f'<p class="cap">{E(label)}. Nominal values: 2.96 on Newsprint, 4.17 on White, 4.49 on Charcoal, 3.19 on Prussian.</p>' + table(["Render"] + [s for _, s in SURF], rows)


def solid_row(pid):
    m = MEAS.get(pid, {}).get("solid_share_mono_newsprint", {})
    return m


def section(n, title, tag, rec, body):
    t = '<span class="tag defect">Defect fix</span>' if tag == "defect" else '<span class="tag">Option</span>'
    r = f' <span class="rec">{E(rec)}</span>' if rec else ""
    return f'<section id="item-{n}" aria-labelledby="h-{n}"><p class="eyebrow">Item {n} {t}{r}</p><h2 id="h-{n}">{E(title)}</h2>{body}</section>'


def P(*xs):
    return "".join(f"<p>{x}</p>" for x in xs)


def pairs_of(panel):
    return [p for p in PP.pairs() if p["panel"] == panel]


def m(pid, key):
    return MEAS.get(pid, {}).get(key, {})


def joins_text(pid):
    j = m(pid, "joins_openness")
    rows = []
    for k in ("orig 16", "prop 16", "orig 24", "prop 24"):
        if k in j:
            rows.append([("Original, " if k.startswith("orig") else "Proposal, ") + k.split()[1] + " px"] + [f'{j[k].get(x, "n/a")}' for x in ("T-H", "T-I", "I-O", "O-N")])
    return table(["Render, one color on Newsprint", "T to H", "T to I", "I to O", "O to N"], rows) if rows else ""


def build():
    W = SPEC["wordmark"]
    WA = SPEC["wordmark_amp"]
    CD = SPEC["condensed"]
    MK = SPEC["marks"]
    R1 = SPEC["p01"]
    parts = []
    # ------------------------------------------------------------ 1
    rows = []
    for k, v in R1["measures"].items():
        ov = ", ".join(f"{a} {b}" for a, b in v["overflow_units"].items())
        rows.append([f"<code>#{E(k)}</code>", " ".join(f"{x:g}" for x in v["old_viewBox"]), E(ov), " ".join(f"{x:g}" for x in v["new_viewBox"]),
                     f'<code>{E(Path(v["file"]).name)}</code>'])
    lp = []
    for lk, us in R1["lockup_placements"].items():
        for u in us:
            lp.append([lk.upper(), f"<code>#{u['symbol']}</code>", f'y {u["old"]["y"]:g}, height {u["old"]["height"]:g}', f'y {u["new"]["y"]:g}, height {u["new"]["height"]:g}'])
    hp = R1["hinge_amp_placement"]
    lp.append(["Hinge", "<code>#amp</code>", f'y {hp["old"]["y"]:g}, {hp["old"]["width"]:g} by {hp["old"]["height"]:g}', f'y {hp["new"]["y"]:g}, {hp["new"]["width"]:g} by {hp["new"]["height"]:g}'])
    am = m("p01-amp", "overlay_96")
    b1 = P("Six symbols in the V5 sprite cut off their own ink because each viewBox ends before the outline does. The tagline renders as “A countrv that answers to its peoole.” and the web address as “.orq”. The master ampersand loses the top of its loop and the tip of its tail wherever V5 uses it.",
           "The fix leaves every outline as it is. Each symbol keeps its own origin and gets a viewBox that holds its full ink, measured on the curves themselves and rounded outward to 0.01 unit. Lockups that place these symbols get matching placements, listed below, so nothing moves on the page.")
    b1 += table(["Symbol", "V5 viewBox", "Ink outside it (units)", "Re-exported viewBox", "File"], rows)
    b1 += "<h3>Placements that change with the new viewBoxes</h3>" + table(["Lockup", "Symbol", "V5 use element", "New use element"], lp)
    b1 += f'<p class="cap">Overlay legend for every panel: Charcoal where both versions have ink, light gray where only the original has ink, Verdigris where only the proposal has ink. For the re-exports the Verdigris pixels are the ink V5 cut away ({am.get("proposal_only_px", 0):g} px of coverage on the ampersand at 96 px).</p>'
    b1 += "".join(pair_block(p) for p in pairs_of(1))
    b1 += "<h3>Craft checks</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Pass", "The loop top, tail tip and every descender now render; the symbols' shapes are V5's"),
        ("2 Pixel fit", "Not applicable", "Outlines unchanged. Pixel fit at 16 px is items 3, 4, 5 and 8"),
        ("3 Consistency", "Pass", "Same outlines, same scale (0.14) and origins as V5"),
        ("4 Optical balance", "Pass", "No change to overshoot; the re-export only stops the cut"),
        ("5 Similarity", "Not applicable", "No new shapes"),
        ("6 Monochrome", "Pass", "Checked in one color on all four surfaces below"),
        ("7 Red discipline", "Pass", "Red stays on the ampersand only"),
        ("8 Contrast", "Fail, inherited", "The ampersand is still Pillar Red, so on Newsprint it measures below 3:1 (items 4, 5 and 10)"),
        ("9 Type", "Pass", "Descenders restored: y, p and g read correctly at every size"),
    ]) + "<h3>Rubric</h3>" + scores_html([5, 5, 5, 5, 5, 4], "Accessibility stays at 4: the taglines are still drawn too small inside L4, L5 and L6, which item 9 resolves.")
    parts.append(section(1, "Re-export the six clipped symbols", "defect", "Recommended", b1))
    # ------------------------------------------------------------ 2
    hl, ho = W["hinge_literal"], W["hinge_optical"]
    v5 = W["v5"]
    rows = [["V5 as shipped", f'{v5["H&"]["nearest_x"]:.3f}x', f'{v5["&A"]["nearest_x"]:.3f}x', f'{v5["H&"]["area_x"]:.3f}x', f'{v5["&A"]["area_x"]:.3f}x', f'{v5["&A"]["area_x"] / v5["H&"]["area_x"]:.2f}', "970.71"],
            ["2a. 0.10x nearest ink, as V5 states", f'{hl["H&"]["nearest_x"]:.3f}x', f'{hl["&A"]["nearest_x"]:.3f}x', f'{hl["H&"]["area_x"]:.3f}x', f'{hl["&A"]["area_x"]:.3f}x', f'{hl["&A"]["area_x"] / hl["H&"]["area_x"]:.2f}', f'{hl["width_units"]}'],
            ["2b. Equal white area (recommended)", f'{ho["H&"]["nearest_x"]:.3f}x', f'{ho["&A"]["nearest_x"]:.3f}x', f'{ho["H&"]["area_x"]:.3f}x', f'{ho["&A"]["area_x"]:.3f}x', f'{ho["&A"]["area_x"] / ho["H&"]["area_x"]:.2f}', f'{ho["width_units"]}']]
    b2 = P("V5 states a hinge gap of 0.10x on each side of the ampersand, measured ink to ink. Here x is one cap height of the wordmark, 100 units. The right gap measures 0.083x, and it still reads wider than the left, because the wedge of white above the A's diagonal adds to it. So the ampersand leans toward OATH.",
           f"Two fixes are drawn. Option 2a applies the stated rule: ACTION moves {hl['action_shift']:g} units right so both nearest gaps measure 0.10x. The white on the right then grows further, to {hl['&A']['area_x'] / hl['H&']['area_x']:.2f} times the left. Option 2b sets the gaps by area, which is how the eye judges space: the white between the ampersand and each neighbor, row by row across the cap band, each row counted up to 0.15x deeper than the nearest point. The ampersand moves {ho['amp_shift']:g} units toward ACTION, the wordmark keeps its width to within 0.1 unit, and both sides measure {ho['H&']['area_x']:.3f}x.",
           "I recommend 2b, with the V6 rule written as: equal white on both sides of the ampersand, measured as area across the cap band to a depth of 0.15x, with no ink closer than 0.07x.")
    b2 += table(["Spacing", "Nearest, left", "Nearest, right", "Area, left", "Area, right", "Right over left", "Width, units"], rows)
    b2 += "".join(pair_block(p) for p in pairs_of(2))
    b2 += "<h3>Craft checks, option 2b</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Pass", "Same letters and glyph; the hinge white looks even at 16 px in the magnified render"),
        ("2 Pixel fit", "Not applicable", "Spacing only; the 16 and 24 px masters in item 3 carry the pixel fit"),
        ("3 Consistency", "Pass", "One spacing model for every pair in items 2, 3 and 6"),
        ("4 Optical balance", "Pass", f"Area left {ho['H&']['area_x']:.3f}x, right {ho['&A']['area_x']:.3f}x"),
        ("5 Similarity", "Not applicable", "No new shapes"),
        ("6 Monochrome", "Pass", "Checked in one color on all four surfaces"),
        ("7 Red discipline", "Pass", "Red on the ampersand only"),
        ("8 Contrast", "Fail, inherited", "Pillar Red on Newsprint, 2.96:1 nominal; item 10 and the edge rule apply"),
        ("9 Type", "Pass", f"Nearest ink on the right is {ho['&A']['nearest_x']:.3f}x, above the 0.07x floor"),
    ]) + "<h3>Rubric</h3>" + scores_html([4, 4, 5, 4, 5, 4], "Craft is 4: at 16 px the tail and the A's foot sit 1 px apart in the unhinted master, which the 16 px master in item 3 widens to 2 px.")
    parts.append(section(2, "Equal hinge gaps around the ampersand", "defect", "Recommended: 2b", b2))
    # ------------------------------------------------------------ 3
    m16, m24, dm = W["master_16"], W["master_24"], W["display_master"]
    sol = m("p03-masters", "solid_share_mono_newsprint")
    b3 = P("V5 draws one wordmark and scales it, so the 16 px logo carries display spacing: T to H and T to I clog, I to O to N runs dark, and no stem lands on a whole pixel. This proposal draws three masters from the same letters.",
           f"The display master is option 2b plus two spacing changes: I to O and O to N open by 2.4 units (their white area rises from 0.140x to {dm['IO']['area_x']:.3f}x), and the T joins open by 1.4 units. It is {dm['width_units']:g} units wide against V5's 970.71.",
           f"The 24 px master ({m24['viewBox'][2]} by 24 px) has a 22 px cap height, 5 px stems and 4 px bars, all on whole pixels; each letter pair gets the same white area, the T arms are 1.5 units shorter and nothing comes closer than 2 px. The 16 px master ({m16['viewBox'][2]} by 16 px) has a 14 px cap height, 3 px stems and bars, T arms 4 units shorter, and the option A 16 px ampersand. At 16 and 24 px the ampersand fills the full box height, 1.14 and 1.09 times the cap height, so the red keeps its weight beside Charcoal capitals. That is an optical-size change to V5's rule that the glyph matches the cap height, and it needs Dustin's approval with the rest.",
           f"Solid share of ink pixels, one color on Newsprint: original {sol.get('orig 16', 'n/a')} at 16 px and {sol.get('orig 24', 'n/a')} at 24 px; proposal {sol.get('prop 16', 'n/a')} and {sol.get('prop 24', 'n/a')}.")
    b3 += "<h3>Joins at small sizes</h3><p class=\"cap\">The lightest column between two letters in the top fifth of the cap band (T joins) or across the band (I, O, N), as a share of full background. 1.00 means a clear column.</p>" + joins_text("p03-masters")
    b3 += "".join(pair_block(p) for p in pairs_of(3))
    b3 += "<h3>Craft checks</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Pass", "Every letter separates; the T joins show a clear column (table above)"),
        ("2 Pixel fit", "Pass", "Stems, bars and the cap band sit on whole pixels at 16 and 24 px by construction; diagonals of A and N antialias, as they must"),
        ("3 Consistency", "Pass", "Same stem and bar weights in every letter of a master"),
        ("4 Optical balance", "Pass", "Overshoots suppressed at 16 and 24 px, where they would be a blurred half pixel; kept at display"),
        ("5 Similarity", "Not applicable", "Same letters"),
        ("6 Monochrome", "Pass", "One color checked on all four surfaces"),
        ("7 Red discipline", "Pass", "Red on the ampersand only"),
        ("8 Contrast", "Fail, inherited", "Red on Newsprint stays under 3:1; the larger 16 px glyph makes more of its pixels solid (item 4)"),
        ("9 Type", "Pass", "Tracking opens as size falls: +2.5 units per pair at 24 px, +5 at 16 px, then each pair evened by area"),
    ]) + "<h3>Rubric</h3>" + scores_html([4, 4, 4, 5, 5, 4], "Brand fidelity is 4: the larger ampersand at 16 and 24 px changes a stated V5 measure, so it needs a named approval.")
    parts.append(section(3, "Wordmark masters for display, 24 px and 16 px", "option", "Recommended", b3))
    # ------------------------------------------------------------ 4
    b4 = P("Option A keeps the Lora-derived glyph Dustin knows and tunes it.",
           "The display tune grows the outline with an elliptical pen, 7.5 font units up and down and 3 across, so the thin horizontals gain more than the stems: hairlines go from 70 to 85 font units and the contrast between thick and thin falls from 1.9 to about 1.7. A vertical warp then sets the overshoot to the wordmark's own, 1.34 units above the cap line and below the baseline, and keeps the tail flat on the baseline. V5 measured 0.24 units above and 2.24 below.",
           "The 16 px master is a separate drawing, 15 by 16 px, made over the tuned outline on the pixel grid. Hairlines are 2 px (V5: 1.45 px), the bowl stem 3 px, the diagonal 2.6 px measured square to its direction, and the upper counter 3 px wide. Every horizontal and vertical edge sits on a whole pixel, so the red pixels come out solid.")
    b4 += red_table("p04-amp")
    s4 = m("p04-amp", "solid_share_mono_newsprint")
    b4 += f'<p class="cap">Solid share of ink pixels at 16 px, one color on Newsprint: V5 {s4.get("orig 16", "n/a")}, option A {s4.get("prop 16", "n/a")}. At 24 px: V5 {s4.get("orig 24", "n/a")}, option A {s4.get("prop 24", "n/a")}.</p>'
    b4 += "".join(pair_block(p) for p in pairs_of(4))
    b4 += "<h3>Craft checks</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Pass", "Both counters and the arm notch show background at 16 px (V5: upper counter 0.66 filled at its base, arm notch 0.23)"),
        ("2 Pixel fit", "Pass", "The 16 px master is drawn on whole pixels"),
        ("3 Consistency", "Pass", "Hairlines 2 px and stems 3 px, matching the 16 px wordmark's 3 px stems"),
        ("4 Optical balance", "Pass", "Overshoot now 1.34 units on both sides, as the O"),
        ("5 Similarity", "Pass", f"Overlap with the V5 glyph {SIM['V5 master (Lora Bold)']['IoU with option A']}: it stays the same ampersand"),
        ("6 Monochrome", "Pass", "One color on all four surfaces"),
        ("7 Red discipline", "Pass", "One ampersand moment"),
        ("8 Contrast", "Fail on Newsprint", "Solid pixels reach the nominal 2.96:1 and no higher; the 1 px Charcoal edge rule stays for informative use. Logotypes are exempt from WCAG contrast"),
        ("9 Type", "Not applicable", "A glyph"),
    ]) + "<h3>Rubric</h3>" + scores_html([4, 4, 5, 4, 5, 4], "The tune is low-risk and fixes the small sizes. It does not make the glyph proprietary: anyone can still set Lora Bold.")
    parts.append(section(4, "Ampersand option A: an optical tune and a true small master", "option", "Fallback if B is declined", b4))
    # ------------------------------------------------------------ 5
    sim_rows = [[E(k), f'{v["IoU with option B"]:.3f}', f'{v["IoU with option A"]:.3f}'] for k, v in SIM.items()]
    b5 = P("Option B is a drawn ampersand. It keeps the silhouette a reader knows (a loop over a bowl, a diagonal that crosses to a tail, an arm with a serif) and makes four decisions of its own.",
           "Contrast: one broad-nib axis, the bowl stem at 0.85 of the wordmark's stem (Lora's thick strokes reach 0.67 to 0.78) and hairlines of 13.7 to 14.9 units (Lora's: 9.8 to 10.2), so thick to thin is about 1.5 to 1 against Lora's 1.9. The red now carries weight beside the Charcoal capitals. Terminals: the arm ends in a flat cut with a beak serif that reaches only toward the loop, and the tail sweeps out flat and stops with a vertical cut, its foot on the baseline like the letters' feet. Crossing: the diagonal meets the arm close to square, and both strokes narrow where they cross, so the corners of the counters stay open. Counters: a taller loop counter and a fuller bowl than Lora's.",
           "I drew it first as one pen path that crosses itself twice, the way an ampersand is written, then redrew the outline by hand as three contours of cubic Beziers with nodes on extrema, added weight with an elliptical pen and refitted it (41 nodes). A 16 px master, 14 by 16 px, is drawn on the pixel grid with the same rules as option A's.")
    b5 += f'<figure class="constr"><figcaption>Construction. Red fill: option B. Dashed line: the V5 glyph (Lora Bold) at the same cap height. Gray: the pen path B was drawn from.</figcaption>{construction_svg()}</figure>'
    b5 += "<h3>Similarity to other serif ampersands</h3><p class=\"cap\">Silhouette overlap (intersection over union) after scaling each glyph to the same ink height and centring it. 1.000 is identical. Fonts installed on this machine; a wider check against commercial serif ampersands needs page access.</p>" + table(["Glyph", "Overlap with B", "Overlap with A"], sim_rows)
    b5 += red_table("p05-amp")
    s5 = m("p05-amp", "solid_share_mono_newsprint")
    b5 += f'<p class="cap">Solid share of ink pixels at 16 px, one color on Newsprint: V5 {s5.get("orig 16", "n/a")}, option B {s5.get("prop 16", "n/a")}.</p>'
    b5 += "".join(pair_block(p) for p in pairs_of(5))
    b5 += "<h3>Craft checks</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Pass", "Loop, bowl, beak and tail all read at 16 px; both counters open"),
        ("2 Pixel fit", "Pass", "The 16 px master is drawn on whole pixels"),
        ("3 Consistency", "Pass", "Stem and hairline weights sit with the wordmark's 800 capitals; one contrast axis throughout"),
        ("4 Optical balance", "Pass", "Overshoot 1.43 units above the cap line, 1.71 below the baseline; the tail's foot sits on the baseline"),
        ("5 Similarity", "Pass", f"Overlap with Lora {SIM['V5 master (Lora Bold)']['IoU with option B']:.3f}: recognizably the same kind of glyph, and its own. With the other serifs 0.47 to 0.60"),
        ("6 Monochrome", "Pass", "One color on all four surfaces"),
        ("7 Red discipline", "Pass", "One ampersand moment"),
        ("8 Contrast", "Fail on Newsprint", "As option A: 2.96:1 at best on Newsprint"),
        ("9 Type", "Not applicable", "A glyph"),
    ]) + "<h3>Rubric</h3>" + scores_html([4, 4, 4, 4, 5, 4], "Craft is 4 for a first drawing. Before it ships it needs a refinement pass at 2x and a print proof, and a check against commercial serif ampersands.")
    parts.append(section(5, "Ampersand option B: a drawn ampersand of Oath & Action's own", "option", "Recommended direction", b5))
    # ------------------------------------------------------------ 6
    c75, c60 = CD["7.5"], CD["6.0"]
    cur_w = W["display_master"]["width_units"]
    gain75 = cur_w / (c75["viewBox"][2])
    gain60 = cur_w / (c60["viewBox"][2])
    sw = "".join(f'<figure><figcaption>{lab}, 360 px wide</figcaption>{img(f"sw__{k}__360", lab + " at 360 px wide", lazy=False)}</figure>' for k, lab in (("current", "Current proportions"), ("condensed", "Condensed 7.5 to 1"), ("condensed60", "Condensed 6 to 1")))
    sw2 = "".join(f'<figure><figcaption>{lab}, 180 px wide</figcaption>{img(f"sw__{k}__180", lab + " at 180 px wide", zoom=2, lazy=False)}</figure>' for k, lab in (("current", "Current proportions"), ("condensed", "Condensed 7.5 to 1")))
    b6 = P("Dustin's references set the wordmark in condensed heavy capitals with the serif red ampersand. The creative director measured them at 5.7 to 6.3 times as wide as their ink is tall; V5's wordmark is 9.5 times.",
           f"I drew the condensed letters from Inter Tight 800's own capitals, the outlines V5 already uses. Each letter is narrowed (to 0.74 of its width, the A to 0.81 so its counter stays open), its stems get back the weight the narrowing took, its bars thin by 2.2 units so stems and bars keep Inter Tight's 1.2 to 1, and the cap band is restored. The A's flat apex, the C's horizontal cuts and the N's joins stay Inter Tight's. Spacing uses the same area model as item 2. The ampersand is option B narrowed to 0.85, since the Lora glyph is 0.89 as wide as it is tall and sits wide among condensed capitals.",
           f"Two widths were tested. At 7.5 to 1 (by ink height; {c75['ratio_width_to_cap']} cap heights wide) the A's counter stays {c75['counter_openness_at_16px']['A']:.2f} open at 16 px. At 6 to 1 ({c60['ratio_width_to_cap']} cap heights) it closes to {c60['counter_openness_at_16px']['A']:.2f}. The 16 px test chooses 7.5 to 1, and only that width gets 24 and 16 px masters. In the same width as the current wordmark, the 7.5 to 1 version has {gain75:.2f} times the cap height; the 6 to 1 version would give {gain60:.2f} times.",
           "Effect on the type system: Inter Tight stays the headline face, set in sentence case, and Inter and Lora Italic keep their roles. Condensed capitals live in the wordmark only; no condensed headline style is added. Because the letters come from Inter Tight, the wordmark and the headlines share terminals and apertures. Tokens change only for masthead sizes.",
           "Font record: base family Inter Tight 800, Copyright 2022 The Inter Project Authors, SIL Open Font License 1.1, as its name table states. No OFL condensed family was used; the research ledger's list (Archivo, Barlow Condensed, Oswald, Anton and others) served as comparison only. The wordmark is artwork made from the outlines, which the OFL does not govern (research ledger, Part 4). Changed: width, stem compensation, bar weight, the A's width, spacing.")
    b6 += f'<h3>Same width, more height</h3><div class="disp">{sw}</div><div class="zgrid"><div class="scroll zrow" tabindex="0" role="region" aria-label="Same width at 180 px, magnified 2x">{sw2}</div></div>'
    b6 += ('<h3>Beside an Inter Tight headline</h3><div class="spec s-newsprint"><img src="' + CELLS["sw__condensed__360"]["src"] + '" width="360" height="' + str(CELLS["sw__condensed__360"]["h"]) + '" alt="Condensed wordmark">'
           '<p class="hl">Who decides when the bus comes?</p><p class="cap">Headline set live in Inter Tight 800, sentence case, 40 px, beside the condensed wordmark at 360 px. Illustrative headline.</p></div>')
    b6 += "".join(pair_block(p) for p in pairs_of(6))
    b6 += "<h3>Craft checks, 7.5 to 1</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Pass", f"O, A and C counters open at 16 px ({c75['counter_openness_at_16px']['O']:.2f}, {c75['counter_openness_at_16px']['A']:.2f}, {c75['counter_openness_at_16px']['C']:.2f})"),
        ("2 Pixel fit", "Fail", "Letters are pixel-fit at 16 and 24 px, but the narrowed ampersand is scaled, not drawn, so its edges blur. A drawn 16 px narrow master is Phase 2 work if Dustin approves the direction"),
        ("3 Consistency", "Pass", "One stem (22 units), one bar weight, Inter Tight terminals"),
        ("4 Optical balance", "Pass", "Overshoots unchanged at 1.34 units; hinge areas equal"),
        ("5 Similarity", "Fail, risk", "Heavy condensed capitals are common on campaign signs. The serif ampersand and Newsprint keep it editorial, but the risk is real"),
        ("6 Monochrome", "Pass", "One color on all four surfaces"),
        ("7 Red discipline", "Pass", "Red on the ampersand only"),
        ("8 Contrast", "Fail, inherited", "Red on Newsprint under 3:1"),
        ("9 Type", "Pass", "Headlines stay Inter Tight; no new face"),
    ]) + "<h3>Rubric</h3>" + scores_html([3, 4, 3, 4, 5, 4], "Craft 3: the letters are derived by a measured transform and want a drawing pass (the C's terminals and the N's joins at display size, a drawn narrow ampersand at 16 px). Brand fidelity 3: it changes the locked wordmark's proportions, which is Dustin's call.")
    parts.append(section(6, "Wordmark width: a condensed exploration", "option", "For Dustin's named decision", b6))
    # ------------------------------------------------------------ 7
    hd, hc = MK["hinge_display"], MK["hinge_compact"]
    b7 = P("V5's hinge diagram sets the wordmark under a dotted arc that ends in an open arrowhead, with UNDERSTAND and IMPACT beneath. Its arc keeps a fixed 1.25 px weight at every size (a non-scaling stroke), so it is heavy when small and faint when large, and its labels fall under 13 px below 516 px wide.",
           "The proposal is drawn from Dustin's mockups: the ampersand sits in a circle on a line that joins OATH and ACTION, with a node at each end of each line, and two dotted arcs loop around it. The upper arc runs from OATH to ACTION, the promise then the act, and the lower arc returns, so the figure reads as a cycle. Each arc ends in one open arrowhead. It keeps V5's rules: the original lettering anchors it, the labels sit under the optical centers of their words, and the ampersand is the master glyph in Pillar Red, here at 1.25 times the cap height in a circle 2.2 times the cap height.",
           f"Every stroke is drawn in units, so line weight scales with the mark. The display master (lines 3.5 units, labels with a 26-unit cap height) holds 13 px labels from {hd['min_width_px']} px wide, where its lines measure {hd['line_px_at_min']} px. Below that, the compact master drops the labels and draws lines at 6 units, which stay at 1 px or more down to {hc['min_width_px']} px wide. Labels are Charcoal on light surfaces: Stone measures 4.29:1 on Newsprint, under the 4.5:1 that 13 px text needs.")
    b7 += "".join(pair_block(p) for p in pairs_of(7))
    b7 += "<h3>Craft checks</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Not applicable", "The hinge has a minimum of 241 px wide; the 16, 24 and 48 px rows show both versions below their minimum, for the record"),
        ("2 Pixel fit", "Not applicable", "A diagram that scales; line weight is held at 1 px or more by the two masters"),
        ("3 Consistency", "Pass", "Lines, circle, arcs and arrowheads share one weight; nodes share one size"),
        ("4 Optical balance", "Pass", "The ampersand is centered on its ink in the circle; arcs are concentric with it"),
        ("5 Similarity", "Pass", "Distinct from the lockmark and the Signal Grid: no 3 by 3 field"),
        ("6 Monochrome", "Pass", "One color on all four surfaces"),
        ("7 Red discipline", "Pass", "Red on the ampersand only; lines Stone or Newsprint"),
        ("8 Contrast", "Pass", "Stone lines on Newsprint 4.29:1, Newsprint lines on Charcoal 13.29:1, on Prussian 9.42:1, all above 3:1"),
        ("9 Type", "Pass", f"Labels 13 px or larger at the display master's minimum ({hd['min_width_px']} px)"),
    ]) + "<h3>Rubric</h3>" + scores_html([4, 4, 4, 4, 5, 4], "Brand fidelity is 4 because the circle and the return arc are new to V5's hinge; both come from Dustin's references.")
    parts.append(section(7, "The hinge mark", "option", "Recommended", b7))
    # ------------------------------------------------------------ 8
    l16, l24 = MK["lockmark_16"], MK["lockmark_24"]
    b8 = P("V5 draws the lockmark's links as 1 px non-scaling strokes on a 123.5-unit field. At 16 px a node is 0.98 px across, the width of a link, and the lever is one pink pixel. The middle links land on a pixel boundary at 16, 24 and 48 px, so the center cross splits into two gray rows inside a dark frame.",
           f"The 16 px master puts node centers at {', '.join(str(c) for c in l16['node_centres_px'])} px, so every 1 px link fills a whole pixel row or column. Nodes are {l16['node_diameter_px']:g} px and the lever {l16['lever_diameter_px']:g} px. The 24 px master uses centers {', '.join(str(c) for c in l24['node_centres_px'])}, nodes {l24['node_diameter_px']:g} px and the lever {l24['lever_diameter_px']:g} px. The lever stays one size larger than the nodes, so it still reads in one color; V5 made it match the nodes below 32 px. From 48 px up the V5 master stays.")
    s8 = m("p08-lockmark", "solid_share_mono_newsprint")
    b8 += f'<p class="cap">Solid share of ink pixels, one color on Newsprint: V5 {s8.get("orig 16", "n/a")} at 16 px and {s8.get("orig 24", "n/a")} at 24 px; proposal {s8.get("prop 16", "n/a")} and {s8.get("prop 24", "n/a")}.</p>'
    b8 += "".join(pair_block(p) for p in pairs_of(8))
    b8 += "<h3>Craft checks</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Pass", "Nine dots on a frame and a cross, with the lever larger"),
        ("2 Pixel fit", "Pass", "Links fill whole pixel rows; nodes center on pixel centers"),
        ("3 Consistency", "Pass", "One link weight, one node size, one lever size per master"),
        ("4 Optical balance", "Pass", "The live area sits 1 px inside the box on every side"),
        ("5 Similarity", "Pass", "Compared with the Signal Grid states: Empty has no lever, Active a Verdigris lever; the masters keep those differences"),
        ("6 Monochrome", "Pass", "The lever reads by size in one color"),
        ("7 Red discipline", "Pass", "Red on the lever only"),
        ("8 Contrast", "Fail on Newsprint", "A red lever on Newsprint is 2.96:1. Its size, not its color, carries the meaning, so it is decorative there"),
        ("9 Type", "Not applicable", "No type"),
    ]) + "<h3>Rubric</h3>" + scores_html([5, 4, 4, 5, 5, 4], "Brand fidelity is 4: a larger lever at 16 px reverses V5's rule for small sizes.")
    parts.append(section(8, "A lockmark master for small sizes", "defect", "Recommended", b8))
    # ------------------------------------------------------------ 9
    mins = [
        ["L1 wordmark", "120 px wide (13.4 px tall, cap 12.4 px)", f"16 px tall with the 16 px master ({W['master_16']['viewBox'][2]} px wide); 24 px master from 20 to 40 px tall; display master above", "1.25 in", "Below 16 px tall, use L8"],
        ["L2 stacked", "72 px wide (cap 11.5 px, smaller than L1's)", "88 px wide (cap 14 px)", "0.75 in", "Below 88 px, use L8"],
        ["L3 horizontal with lockmark", "192 px wide", "200 px wide (wordmark 16 px tall, lockmark 34 px)", "1.5 in", "Below 200 px, use L1"],
        ["L4 box and tagline", "144 px wide (tagline cap 4.5 px)", "304 px wide (tagline at 13 px)", "2.3 in (tagline at 7 pt)", "Below 304 px, use L8 and set the tagline as live text"],
        ["L5 wordmark and tagline", "240 px wide (tagline cap 5.9 px)", "384 px wide (tagline at 13 px)", "2.85 in (tagline at 7 pt)", "Below 384 px, use L1 and set the tagline as live text"],
        ["L6 editorial signature", "288 px wide (tagline cap 3.1 px)", "880 px wide (tagline at 13 px)", "6.6 in (tagline at 7 pt)", "Below 880 px, use L3 with the tagline as live text"],
        ["L7 section masthead", "168 px wide", "250 px wide (pillar word at 13 px)", "1.9 in (pillar word at 7 pt)", "Pillar word drawn in Inter 600 caps"],
        ["L8 monogram", "48 px wide, also used for favicons", "48 px wide; never a favicon", "0.5 in", "Favicons use the ampersand, below"],
        ["Ampersand, freestanding", "16 px with the optical drawing; 24 px master", "16 px master from 16 to 23 px; display master from 24 px", "0.25 in", "Favicon: the 16 px master on a clear ground at 16 px, the S2 tile from 32 px"],
        ["Lockmark", "16 px, one color", "16 and 24 px masters; V5 master from 32 px", "0.25 in", "The lever stays one size up at 16 and 24 px"],
        ["Hinge", "None set", "Display master from 526 px wide; compact from 241 px", "4 in (display)", "Below 241 px, use a hinge headline"],
    ]
    b9 = P("V5's minimums leave a gap and contradict each other. L1's 120 px minimum is 13.4 px tall, and the rule that the monogram replaces the wordmark below 80 px leaves 80 to 120 px undefined. L2 at 72 px has a smaller cap height than L1 at its minimum. L8 has a 48 px minimum but is listed for favicons. Clear space allows no type, yet the taglines in L5 and L6 sit 0.39x and 0.79x below the baseline, inside it.",
           "The proposal uses one principle: on screen no identity mark draws its capitals under 14 px, and no tagline inside a lockup draws under 13 px. Each lockup's minimum follows from that, and each has a named replacement below it, so no size is undefined. Clear space (1.0x) surrounds the whole lockup; the tagline's offset inside L5 and L6 is part of the lockup's drawing, fixed by its master, and nothing else enters. Print floors keep V5's inch values where they hold a 3 mm cap height, and set the tagline at 7 pt or larger.")
    b9 += table(["Lockup", "V5 minimum", "Proposed screen minimum", "Print", "Below the minimum"], mins)
    rows9 = []
    for mid, lab, _, _ in [(a, b, c, d) for a, b, c, d in __import__("p1_render").MIN_ITEMS]:
        cells = []
        for vk, vl in (("orig", "V5 at its minimum"), ("prop", "Proposal at its minimum")):
            for s, sl_ in SURF:
                for md, mdl in MODES:
                    cid = f"min__{mid}__{vk}__{s}__{md}"
                    cells.append(f'<figure class="c"><div class="sw s-{s}">{img(cid, f"{lab}, {vl}, {sl_}, {mdl}")}</div><figcaption>{vl.split(" at")[0]}, {sl_}, {mdl.lower()}</figcaption></figure>')
        rows9.append(f'<div class="mrow"><div class="ml"><b>{E(lab)}</b><span>1x</span></div><div class="sizes">{"".join(cells)}</div></div>')
    b9 += f'<h3>Each mark at its minimum, V5 against the proposal, at 1x</h3><div class="scroll matrix" tabindex="0" role="region" aria-label="Minimum sizes">{"".join(rows9)}</div>'
    zrows = []
    for mid, lab in (("L1", "L1 wordmark"), ("AMP", "Freestanding ampersand"), ("LOCK", "Lockmark")):
        zrows.append("".join(f'<figure><figcaption>{E(lab)}, {vl}</figcaption>{img(f"min__{mid}__{vk}__newsprint__color", lab + " magnified", zoom=4)}</figure>' for vk, vl in (("orig", "V5 minimum"), ("prop", "proposed minimum"))))
    b9 += '<div class="zgrid">' + "".join(f'<div class="scroll zrow" tabindex="0" role="region" aria-label="Magnified minimums">{z}</div>' for z in zrows) + "</div>"
    b9 += "<h3>Craft checks</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Pass", "Every mark at its minimum uses a master drawn for that size"),
        ("2 Pixel fit", "Pass", "Minimums land where the 16 and 24 px masters apply"),
        ("3 Consistency", "Pass", "One rule (14 px capitals, 13 px taglines) produces every number"),
        ("4 Optical balance", "Not applicable", "A rule set"),
        ("5 Similarity", "Not applicable", "A rule set"),
        ("6 Monochrome", "Pass", "Minimums hold in one color; checked on all surfaces"),
        ("7 Red discipline", "Pass", "No change"),
        ("8 Contrast", "Pass", "Taglines at 13 px in Charcoal or Newsprint clear 4.5:1 on every approved surface"),
        ("9 Type", "Pass", "No tagline under the 13 px floor"),
    ]) + "<h3>Rubric</h3>" + scores_html([4, 4, 5, 5, 5, 4], "L4, L5 and L6 grow a lot. If Dustin wants them smaller, the taglines inside them have to grow relative to the wordmark, which redraws those lockups.")
    parts.append(section(9, "One set of minimum sizes", "defect", "Recommended", b9))
    # ------------------------------------------------------------ 10
    rows10 = []
    labels = {"p10-display-only": "A. Red at display size only", "p10-newsprint": "B. Newsprint ampersand", "p10-keyline": "C. Red with a Newsprint keyline", "p10-mono": "D. One color, all White"}
    for pid, lab in labels.items():
        rs = m(pid, "red")
        vals = []
        for size in (16, 24, 48, 96):
            r = rs.get(f"prop prussian {size}")
            vals.append(f'{r["median_contrast"]:.2f} ({int(round(r["share_at_or_above_3"] * 100))}%)' if r and "median_contrast" in r else "n/a")
        rows10.append([lab] + vals)
    r0 = m("p10-mono", "red")
    vals0 = []
    for size in (16, 24, 48, 96):
        r = r0.get(f"orig prussian {size}")
        vals0.append(f'{r["median_contrast"]:.2f} ({int(round(r["share_at_or_above_3"] * 100))}%)' if r and "median_contrast" in r else "n/a")
    rows10.insert(0, ["V5: red at every size"] + vals0)
    nom = MK["prussian_nominal"]
    b10 = P(f"V5 sets White letters and a red ampersand on Prussian, and its own text says red there “stays at display size or goes mono”, while its color matrix shows small red ampersands. Pillar Red measures {nom['Pillar Red']}:1 on Prussian, just above the 3:1 that graphics need, and antialiasing pulls the small sizes below it. V5's Voice chapter also says “Never red against blue”, because red on blue reads as a party pairing.",
            f"Four treatments are drawn and measured. Nominal contrast on Prussian: Pillar Red {nom['Pillar Red']}, Newsprint {nom['Newsprint']}, White {nom['White']}. The keyline in option C is Newsprint, and Pillar Red against Newsprint is {nom['Pillar Red on Newsprint keyline']}:1, so the keyline carries the edge while the red reads as a fill.")
    b10 += '<p class="cap">Median contrast of the ampersand’s pixels against Prussian, after rendering, with the share of its pixels at 3:1 or more in brackets.</p>' + table(["Treatment", "16 px", "24 px", "48 px", "96 px"], rows10)
    b10 += "".join(pair_block(p) for p in pairs_of(10))
    b10 += "<h3>Craft checks, option D</h3>" + checks_html([
        ("1 Silhouette at 16 px", "Pass", "Same mark"),
        ("2 Pixel fit", "Not applicable", "Color only"),
        ("3 Consistency", "Pass", "One rule on Prussian at every size"),
        ("4 Optical balance", "Pass", "No change"),
        ("5 Similarity", "Not applicable", "Color only"),
        ("6 Monochrome", "Pass", "It is the one-color version"),
        ("7 Red discipline", "Pass", "No red on blue"),
        ("8 Contrast", "Pass", f"White on Prussian {nom['White']}:1"),
        ("9 Type", "Not applicable", "Color only"),
    ]) + "<h3>Rubric</h3>" + scores_html([4, 4, 4, 4, 5, 5], "Brand fidelity is 4: Dustin's Prussian banner reference uses the red ampersand, and option D gives that up on Prussian.")
    parts.append(section(10, "The red ampersand on Prussian", "option", "A decision for Dustin", b10))
    return parts


def construction_svg():
    import p1_amp_b as B
    s = (o.OUT / "05-amp-b/20261021_Amp-B-Drawn-Master.svg").read_text()
    d = re.search(r' d="([^"]+)"', s).group(1)
    vb = o.viewbox(s)
    cons = json.loads((o.OUT / "05-amp-b/construction.json").read_text())
    lora = o.amp_glyph(0, 100, 0.14)
    lb = o.bounds(lora)
    lora_d = o.d_from_path(o.tx(lora, e=-lb[0]))
    off = cons["offset_x_units"]
    k = 1 / 7
    return (f'<svg viewBox="-6 {vb[1] - 6:.1f} {vb[2] + 12:.1f} {vb[3] + 12:.1f}" width="420" role="img" aria-label="Option B over the V5 glyph, with the pen path it was drawn from">'
            f'<line x1="-6" y1="0" x2="{vb[2] + 6:.1f}" y2="0" stroke="#4A7C74" stroke-width="0.25"/><line x1="-6" y1="100" x2="{vb[2] + 6:.1f}" y2="100" stroke="#4A7C74" stroke-width="0.25"/>'
            f'<path d="{d}" fill="#E63946" fill-opacity="0.85"/>'
            f'<path d="{cons["centreline_font_units_y_up"]}" fill="none" stroke="#45494F" stroke-width="0.35" transform="matrix({k} 0 0 {-k} {-off * k:.3f} 100)"/>'
            f'<path d="{lora_d}" fill="none" stroke="#121212" stroke-width="0.45" stroke-dasharray="1.2 1"/></svg>')


def decisions():
    rows = [
        ("1. Re-export six clipped symbols", "Accept or decline", "Accept. It restores ink V5 cuts away and changes no outline."),
        ("2. Hinge gaps", "2a: 0.10x nearest ink. 2b: equal white area. Keep V5", "2b. It centers the ampersand by the white the eye sees and keeps the wordmark's width."),
        ("3. Wordmark masters for display, 24 and 16 px", "Accept, accept without the larger small-size ampersand, or decline", "Accept all three, with the ampersand at full box height at 16 and 24 px. The 16 px logo stops clogging."),
        ("4 and 5. The ampersand", "A: tune the Lora glyph. B: the drawn ampersand. Keep V5", "B as the direction, refined in Phase 2, with A as the fallback. B makes the hinge Oath & Action's own and holds at 16 px; A fixes the small sizes but stays a stock glyph."),
        ("6. Wordmark width", "Condensed at 7.5 to 1, or the current proportions", "Your call. I lean to the condensed 7.5 to 1 as a direction: it matches your references and gains 1.26 times the height at the same width. It is not finished; it needs a drawing pass and a narrow 16 px ampersand."),
        ("7. The hinge mark", "Accept, accept without the return arc, or keep V5", "Accept. It follows your mockups, keeps V5's rules and scales its lines."),
        ("8. Lockmark small masters", "Accept or decline", "Accept. Nodes read at 16 and 24 px and the cross fills whole pixels."),
        ("9. Minimum sizes", "Accept, or keep V5's", "Accept. One rule, no undefined range, no tagline under 13 px."),
        ("10. Red ampersand on Prussian", "A: red at display size only. B: Newsprint ampersand. C: red with a keyline. D: one color", "D. It follows V5's “Never red against blue” and passes at every size. If you want the red from your banner, A is the fallback."),
    ]
    tr = "".join(f"<tr><th scope=\"row\">{E(a)}</th><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in rows)
    return ('<section id="decisions" aria-labelledby="h-dec"><div class="decision"><p class="eyebrow">Decisions for Gate 1</p><h2 id="h-dec">What I need you to decide</h2>'
            '<p>Each change to identity geometry needs your approval by name. Until then the V5 masters stay in force. My recommendation follows each item.</p>'
            f'<div class="scroll" tabindex="0" role="region" aria-label="Decisions table"><table><thead><tr><th scope="col">Item</th><th scope="col">Options</th><th scope="col">Recommendation</th></tr></thead><tbody>{tr}</tbody></table></div></div></section>')


CSS = """
.board{max-width:1280px}
.intro{display:grid;gap:12px}
.toc{columns:2 280px;padding-left:20px;margin:8px 0 0}
.toc a{color:var(--fg)}
.tag{margin-left:6px}
.rec{font:600 .8125rem/1.4 var(--body);margin-left:6px;color:var(--fg)}
.pair{margin:28px 0;padding:16px;border:1px solid var(--rule);background:var(--surface);min-width:0}
.pair h3{margin-bottom:12px}
.disp{display:grid;gap:12px;margin-bottom:12px}
.disp figure,.dispall figure,.zgrid figure{margin:0}
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
.c{margin:0}
.c figcaption{margin:2px 0 0}
.sw{padding:6px;display:inline-block}
.dispall{display:grid;gap:10px}
.s-newsprint{background:#DCD9D2}.s-white{background:#FFFFFF}.s-charcoal{background:#121212}.s-prussian{background:#1F2D5A}
.k{display:inline-block;width:12px;height:12px;vertical-align:-1px;margin:0 3px 0 8px;border:1px solid var(--rule)}
.k-both{background:#121212}.k-orig{background:#A8ACB2}.k-prop{background:#4A7C74}
table.checks td:nth-child(2){white-space:nowrap}
.res{font-weight:700}.res.pass{color:#1E4F47}.res.fail{color:#9E1B26}.res.na{color:var(--muted)}
.score{font:800 1.25rem/1 var(--display)}.score.low{color:#9E1B26}
.constr{margin:16px 0}
.constr svg{max-width:100%;height:auto;background:#fff;border:1px solid var(--rule)}
.spec{padding:20px;display:grid;gap:12px;justify-items:start}
.spec img{max-width:100%;height:auto}
.hl{font:800 2.5rem/1.05 var(--display);letter-spacing:-0.02em;margin:0;text-wrap:balance}
.decision table th,.decision table td{border-bottom-color:rgba(220,217,210,.45);color:var(--newsprint)}
.decision table th{text-transform:none;letter-spacing:0;font-size:.875rem}
.decision h2{color:var(--newsprint)}
.decision .eyebrow{color:var(--newsprint)}
.tested{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
code{font-size:.85em}
@media (max-width:760px){.mrow{grid-template-columns:1fr}.hl{font-size:1.75rem}}
"""


def page(parts):
    intro = ('<header class="intro"><p class="eyebrow">Oath &amp; Action Brand Guide, Edition 06. Phase 1, October 21, 2026</p>'
             '<h1>Identity refinement</h1>'
             '<p>Ten proposals for the wordmark, the ampersand, the hinge and the lockmark, each beside the V5 master it would change. Every proposal is a drawing on this board only. The V5 masters stay in force until Dustin approves a change by name.</p>'
             '<p>Each pair shows the original, the proposal and an overlay at 16, 24, 48 and 96 px tall and at display size, on Newsprint, White, Charcoal and Prussian, in color and in one color. Small sizes are also shown magnified 4x with nearest-neighbor scaling, so each square is one screen pixel. Every image is a Chromium render at device scale 1. The surface matrix and the other surfaces sit in the expandable rows under each pair.</p>'
             '<p>Tags: <span class="tag defect">Defect fix</span> repairs something V5 gets wrong. <span class="tag">Option</span> is a choice. In the text, x means one cap height of the wordmark, 100 units.</p>'
             '<nav aria-label="Items on this board"><ol class="toc">'
             + "".join(f'<li><a href="#item-{n}">{E(t)}</a></li>' for n, t in [(1, "Re-export the six clipped symbols"), (2, "Equal hinge gaps"), (3, "Wordmark masters for display, 24 and 16 px"),
                                                                             (4, "Ampersand option A"), (5, "Ampersand option B"), (6, "Wordmark width, condensed"), (7, "The hinge mark"),
                                                                             (8, "Lockmark for small sizes"), (9, "One set of minimum sizes"), (10, "Red ampersand on Prussian")])
             + '<li><a href="#decisions">Decisions for Gate 1</a></li><li><a href="#tested">What I checked</a></li></ol></nav></header>')
    tested = ('<section id="tested" aria-labelledby="h-t"><h2 id="h-t">What I checked and what I could not</h2><div class="tested"><div><h3>Checked</h3><ul>'
              '<li>Every cell rendered in Chromium 141 on Linux at device scale 1, from the SVG files in <code>work/boards/phase-1/identity/</code>.</li>'
              '<li>Ink bounds of all six re-exported symbols from their curves (fontTools BoundsPen).</li>'
              '<li>Spacing by nearest ink and depth-limited area for every letter pair, from outlines.</li>'
              '<li>Red pixel contrast, solid share and join openness from the renders; numbers in <code>work/handoffs/phase-1/20261021_Identity-Refinement-Measurements.json</code>.</li>'
              '<li>Silhouette overlap of option B against Lora Bold and four serif fonts on this machine.</li>'
              '<li>This board at 1440 and 390 px wide: no horizontal page scroll, every image loads.</li></ul></div>'
              '<div><h3>Not checked</h3><ul><li>Windows, macOS and high-density screens: pixel fit holds for 1x Chromium on Linux.</li><li>Firefox and Safari.</li><li>Print: no proofs; print minimums are calculated.</li>'
              '<li>Commercial serif ampersands, for similarity to option B: no page access.</li><li>Reader tests: optical spacing comes from a model and my eye.</li>'
              '<li>Screen readers on this board.</li></ul></div></div></section>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Identity Refinement Board</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="board-base.css"><style>{CSS}</style></head><body><main class="board">{intro}{"".join(parts)}{decisions()}{tested}</main></body></html>')


if __name__ == "__main__":
    BOARD.write_text(page(build()))
    print(BOARD, BOARD.stat().st_size)
