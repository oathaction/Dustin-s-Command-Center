"""Chapter 14's palette specification (Phase 3, round 5, contract R5-3): every data palette Rule 14.5 names, step by step,
written from the token files by script, so a token release rewrites the plate.

Usage (from the project folder):
  python3 -I work/build/scripts/phase-3/palette_spec_build.py            write the plate and its meta file
  python3 -I work/build/scripts/phase-3/palette_spec_build.py --check    exit 1 when either file is not what tokens.json makes now

Reads   work/build/tokens/tokens.json (every name, value, alias and the release)
        work/boards/phase-3/round-0/palettes/build_palette_proofs.py (round 0's measures, imported and run on today's tokens,
        so the plate's numbers equal board 1's, which DR-236 approved: the data lead's ruling b, request E-1)
        work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py (the atlas build's own grade line marks, as
        Rule 13.4 draws them)
Writes  work/build/guide/specimens/s-14-palette-spec.html, the plate's fragment
        work/build/guide/specimens/s-14-palette-spec.meta.json, the shell's plate keys and the draft label and caption that
        phase3_ch14_build.py copies into chapter 14's manifest and chapter file (R5-2a)

Content, by the data lead's ruling b (round 5): the four palettes in Rule 14.5's order (sequential Verdigris, diverging pair
B, the four group inks with Stone hatched, gray magnitude), each step's token, its value on Newsprint and on Charcoal, the
Newsprint value's contrast on White paper, its label ink and that ink's contrast; a grayscale proof through the browser's own
grayscale(1) filter with each step's OKLab lightness; three color-vision proofs (Machado, Oliveira and Fernandes 2009,
severity 1.0, linear RGB) with round 0's neighbor measure and its bar; the grade line code at 2 and 3 px on both grounds; one
line on Prussian. The accessibility lead's section 6 sets how it reads: contrast in words and rounded down, the swatch in the
Step cell, no empty cell, swatches that keep their color in forced colors and print, token names that break only at a dot.
Every color shows through var(--oa-...), so the page draws what tokens.css holds; the color-vision rows apply the
simulation matrices as SVG filters to those same swatches, so no simulated color is written as a value.
"""
import argparse
import html
import importlib.util
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TOKENS_JSON = ROOT / "work/build/tokens/tokens.json"
SPECIMENS = ROOT / "work/build/guide/specimens"
SID = "s-14-palette-spec"
OUT = SPECIMENS / f"{SID}.html"
META = SPECIMENS / f"{SID}.meta.json"
R0_PATH = ROOT / "work/boards/phase-3/round-0/palettes/build_palette_proofs.py"
BS_PATH = ROOT / "work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py"
e = html.escape


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


R0 = load("oa_round0_palette_proofs", R0_PATH)
R0.PROPOSED.clear()      # round 0's proposals are in the release now; the plate reads tokens.json alone
BS = load("oa_atlas_build", BS_PATH)
TOK = json.loads(TOKENS_JSON.read_text())
RELEASE = TOK["$extensions"]["org.oathandaction"]["version"]
FAULTS = []


def need(ok, msg):
    if not ok:
        FAULTS.append(msg)


# ------------------------------------------------------------------------------------------------ tokens
def node(path):
    n = TOK
    for k in path.split("."):
        n = n[k]
    return n


def hex_of(path):
    v = node(path)["$value"]
    return hex_of(v[1:-1]) if isinstance(v, str) and v.startswith("{") else v["hex"].upper()


def alias_name(path):
    """The palette color a label token points to, in words: Charcoal, Newsprint, White."""
    v = node(path)["$value"]
    while isinstance(v, str) and v.startswith("{"):
        p = v[1:-1]
        m = re.fullmatch(r"oa\.color\.palette\.(\w+)", p)
        if m:
            return {"pillarRed": "Pillar Red"}.get(m.group(1), m.group(1).capitalize())
        v = node(p)["$value"]
    return None


def css(path):
    return "--" + re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", path.replace(".", "-")).lower()


def dotted(path):
    """A token name that may break after each dot and nowhere else (the accessibility lead's 6.4)."""
    return ".<wbr>".join(e(x) for x in path.split("."))


def ratio(x):
    """A contrast ratio rounded down to two places, so it never rounds up across a bar (6.2)."""
    return f"{math.floor(x * 100 + 1e-9) / 100:.2f} to 1"


def contrast(a, b):
    return R0.C.contrast(a, b)


def uses(r, kind):
    """What a ratio allows, in words (6.2): text at 4.5 to 1, a mark at 3 to 1."""
    if kind == "label":
        return "text" if r >= 4.5 else ("large text" if r >= 3 else "not for text")
    return "marks" if r >= 3 else "not for marks alone"


# The grounds: Newsprint and Charcoal hold every chart token (chartGrounds); White measures the Newsprint values as the paper
# of a printed report; Prussian holds none (ruling b)
EXT = TOK["$extensions"]["org.oathandaction"]
need(EXT.get("chartGrounds") == ["newsprint", "charcoal"], f"tokens.json's chartGrounds are {EXT.get('chartGrounds')}; the plate draws Newsprint and Charcoal")
GROUND = {g: hex_of(f"oa.color.palette.{g}") for g in ("newsprint", "white", "charcoal", "prussian")}
for g, h in GROUND.items():
    need(R0.GROUND_HEX[g].upper() == h, f"round 0's {g} ({R0.GROUND_HEX[g]}) is not tokens.json's ({h})")
SURF = {"newsprint": "onNewsprint", "charcoal": "onCharcoal"}
WORD = {"newsprint": "Newsprint", "charcoal": "Charcoal", "white": "White", "prussian": "Prussian"}

# ------------------------------------------------------------------------------------------------ words (drafts, ruling b)
# The jobs' sentences are the data lead's drafts in ruling b; the editor sets the final words (a request to the engineer).
PALS = [
    {"id": "sequential", "name": "Sequential, Verdigris", "steps": 5, "code": "seq", "fill": "oa.chart.color.sequential.fill.step{n}",
     "label": "oa.chart.color.sequential.label.step{n}", "word": "Step",
     "job": "One measure from low to high, such as a rate in each state. Low values sit closest to the ground and high values farthest from it, on Newsprint and on Charcoal.",
     "carry": "Where a step stands under 3 to 1 against the ground, its value prints on or beside it, and a sized circle takes the outline token, {outline}."},
    {"id": "diverging", "name": "Diverging, pair B", "steps": 5, "code": "div", "fill": "oa.chart.color.diverging.fill.step{n}",
     "label": "oa.chart.color.diverging.label.step{n}", "word": "Step",
     "job": "A measure with a middle that means something, such as a change above or below zero. Prussian runs one way and Verdigris the other, and the middle step sits close to the ground. A sign or a boxed arrow says which way each side runs. Never for parties (Rule 14.7).",
     "carry": "Where a step stands under 3 to 1 against the ground, its value prints on or beside it."},
    {"id": "categorical", "name": "Groups, four inks", "steps": 4, "code": "cat", "fill": "oa.chart.color.categorical.fill.group{n}",
     "label": "oa.chart.color.categorical.label.group{n}", "word": "Group",
     "job": "Up to four named groups with no order. Charcoal, Verdigris, Prussian, then Stone with its hatch, always in that order. Each group carries its name on the chart, and each line ends on its own marker. Past four groups, split the chart into small multiples, or show one group in ink and the rest in gray.",
     "carry": ""},
    {"id": "magnitude", "name": "Magnitude, Stone", "steps": 4, "code": "mag", "fill": "oa.chart.color.magnitude.fill.step{n}",
     "label": "oa.chart.color.magnitude.label.step{n}", "word": "Step",
     "job": "Size in ordered steps with no direction, where a hue would add a meaning the data does not hold. The fan chart’s bands, the confidence band and the bullet graph’s ranges use it, and so do phone tile maps that show how far each state moved.",
     "carry": "Where a step stands under 3 to 1 against the ground, its value prints on or beside it, or the band takes a 1 px edge in the context ink."},
]
MARKER = ["circle", "square", "triangle", "diamond"]
SIM = [("grayscale", "In gray", "the browser’s grayscale filter"),
       ("protanopia", "Protanopia", "no red-sensing cones"),
       ("deuteranopia", "Deuteranopia", "no green-sensing cones"),
       ("tritanopia", "Tritanopia", "no blue-sensing cones")]
GRADE_WORDS = {"documented": ("Documented", "on the public record"), "wellSupported": ("Well supported", "strong research evidence"),
               "plausible": ("Plausible", "some evidence"), "contested": ("Contested", "evidence disputed"),
               "hypothesis": ("Hypothesis", "not yet tested")}
GRADE_JOB = ("How sure the evidence is, drawn in the line itself, separate from color: solid for documented and well supported, "
             "dashed for plausible, dash-dot for contested, dotted for a hypothesis.")


def fill_path(p, n, g):
    path = p["fill"].format(n=n) + "." + SURF[g]
    return path


def label_path(p, n, g):
    if p["id"] == "categorical" and n == 4:
        return f"oa.chart.color.categorical.labelBeside.group4.{SURF[g]}"
    return p["label"].format(n=n) + "." + SURF[g]


# ------------------------------------------------------------------------------------------------ measures (round 0's)
def measures(p):
    """Round 0's measure_set on today's tokens, for each ground, with the plate's own reading of the same tokens checked
    against it value for value."""
    out = {}
    for g in ("newsprint", "charcoal", "white"):
        m = R0.measure_set(p["id"], g)
        tg = "newsprint" if g == "white" else g
        for i, row in enumerate(m["rows"]):
            need(row["fill_hex"] == hex_of(fill_path(p, i + 1, tg)), f"{p['id']} {row['name']} on {g}: round 0 read {row['fill_hex']}")
            need(row["label_hex"] == hex_of(label_path(p, i + 1, tg)), f"{p['id']} {row['name']} label on {g}: round 0 read {row['label_hex']}")
        out[g] = m
    return out


# ------------------------------------------------------------------------------------------------ the plate
def swatch(path, label_path=None, numeral=None, hatch=False, halo=False):
    """One swatch, drawn as an SVG rectangle so it prints, in its token through var(); its numeral in its label ink."""
    fill = f"var({css(path)})"
    body = f'<rect width="40" height="28" style="fill:{fill}"/>'
    if hatch:
        body = (f'<rect width="40" height="28" style="fill:var(--ps-ground)"/>'
                f'<rect width="40" height="28" style="fill:url(#ps-hatch-{path.rsplit(".", 1)[1]})"/>')
    if numeral is not None and label_path:
        if halo:
            body += (f'<rect x="12" y="6" width="16" height="16" style="fill:var(--ps-ground)"/>'
                     f'<text x="20" y="19" text-anchor="middle" style="fill:var({css(label_path)})">{numeral}</text>')
        else:
            body += f'<text x="20" y="19" text-anchor="middle" style="fill:var({css(label_path)})">{numeral}</text>'
    return (f'<svg class="ps-sw" viewBox="0 0 40 28" width="40" height="28" aria-hidden="true" focusable="false">'
            f'<rect class="ps-edge" x=".5" y=".5" width="39" height="27"/>{body}</svg>')


def strip(p, g, sim=None):
    """A palette's swatches in one row on its ground, as drawn or through one proof's filter."""
    n = p["steps"]
    w = 40 * n
    flt = "" if sim is None else (' style="filter:grayscale(1)"' if sim == "grayscale" else f' style="filter:url(#ps-{sim})"')
    rects = []
    for i in range(n):
        path = fill_path(p, i + 1, g)
        if p["id"] == "categorical" and i == 3:
            rects.append(f'<rect x="{40 * i}" width="40" height="20" style="fill:url(#ps-hatch-{SURF[g]})"/>')
        else:
            rects.append(f'<rect x="{40 * i}" width="40" height="20" style="fill:var({css(path)})"/>')
    return (f'<svg class="ps-strip" viewBox="0 0 {w} 20" width="{w}" height="20" preserveAspectRatio="none" aria-hidden="true" '
            f'focusable="false"><g{flt}>{"".join(rects)}</g></svg>')


def ground_panel(p, g, m):
    n = p["steps"]
    word = p["word"]
    rows = m[g]["rows"]
    sw = []
    for i in range(n):
        path = fill_path(p, i + 1, g)
        cat4 = p["id"] == "categorical" and i == 3
        sw.append(f'<li>{swatch(path, label_path(p, i + 1, g), i + 1, hatch=cat4, halo=cat4)}'
                  + (f'<span class="ps-mk">{e(MARKER[i])}</span>' if p["id"] == "categorical" else "") + "</li>")
    proofs = []
    for sim, lab, _ in SIM:
        under = ""
        if sim == "grayscale":
            under = ('<ol class="ps-ls" role="list">' + "".join(f'<li>{r["oklab_L"]:.3f}</li>' for r in rows) + "</ol>")
        proofs.append(f'<div class="ps-pr"><p class="ps-prk">{e(lab)}</p><div class="ps-prs">{strip(p, g, sim)}{under}</div></div>')
    name = (f'{p["name"]} on {WORD[g]}: the {n} {word.lower()}s with their numbers in their label inks, then the same {word.lower()}s '
            f'in gray, with each one’s lightness, and as readers with protanopia, deuteranopia and tritanopia see them.')
    return (f'<div class="ps-g oa-surface-{g}" role="img" aria-label="{e(name)}">'
            f'<p class="ps-gn">On {WORD[g]}</p><ol class="ps-sws" role="list">{"".join(sw)}</ol>{"".join(proofs)}</div>')


def table(p, m):
    n = p["steps"]
    word = p["word"]
    cap = f'{p["name"]}, {n} {word.lower()}s: {p["job"].split(".")[0].lower()}'
    head = ('<thead><tr><th scope="col">' + e(word) + '</th><th scope="col">Token</th>'
            + "".join(f'<th scope="col">On {WORD[g]}</th>' for g in ("newsprint", "charcoal"))
            + '<th scope="col">On White paper</th></tr></thead>')
    body = []
    for i in range(n):
        k = i + 1
        base = p["fill"].format(n=k)
        cat4 = p["id"] == "categorical" and i == 3
        hdr = (f'<th scope="row">{swatch(fill_path(p, k, "newsprint"), hatch=cat4)}<span class="ps-st">{e(word)} {k}</span>'
               f'<span class="ps-cd">{p["code"]}-{k}</span>' + ('<span class="ps-hn">Stone, hatched</span>' if cat4 else "") + "</th>")
        cells = [f'<td><code class="ps-tk">{dotted(base)}</code></td>']
        for g in ("newsprint", "charcoal"):
            r = m[g]["rows"][i]
            fr = contrast(r["fill_hex"], GROUND[g])
            lr = r["label_on_fill"]
            lab_on = "on a halo of the ground" if cat4 else "on the step"
            carry = ""
            cells.append(
                f'<td><span class="ps-v">{e(r["fill_hex"]).replace("#", "&#35;")}</span>'
                f'<span class="ps-l">{ratio(fr)} against {WORD[g]}, {uses(fr, "fill")}</span>'
                f'<span class="ps-l">Label {e(alias_name(label_path(p, k, g)) or "")} {lab_on}, {ratio(lr)}, {uses(lr, "label")}</span>'
                f'<span class="ps-l">Lightness {r["oklab_L"]:.3f}</span>{carry}</td>')
        rw = m["white"]["rows"][i]
        wr = contrast(rw["fill_hex"], GROUND["white"])
        cells.append(f'<td><span class="ps-l">{ratio(wr)} against White, {uses(wr, "fill")}</span>'
                     f'<span class="ps-l">The Newsprint value</span></td>')
        body.append(f"<tr>{hdr}{''.join(cells)}</tr>")
    return (f'<div class="ps-tw"><table class="ps-t"><caption>{e(cap)}</caption>{head}<tbody>{"".join(body)}</tbody></table></div>')


def three(x):
    return f"{x:.3f}"


def measures_words(p, m):
    """The proofs' results in words beside them (6.5), each against its bar (ruling b, round 0's thresholds)."""
    out = []
    word = p["word"].lower()
    for g in ("newsprint", "charcoal"):
        mm = m[g]
        if p["id"] == "categorical":
            under = [x for x in mm["pairs_under_margin"]]
            gray = (f"On {WORD[g]}, in gray, every two groups stand 0.10 or more apart in lightness"
                    + (", except " + "; ".join(f'{x["between"][0].lower()} and {x["between"][1].lower()}, {three(x["delta_L"])} apart, told apart by Stone’s hatch and the direct label'
                                                for x in under) if under else "") + ".")
            need(all("Group 4" in x["between"] for x in under), f"categorical on {g}: a pair under 0.10 without the hatched group")
        elif p["id"] == "diverging":
            ep = mm["end_pair"]
            gray = (f"On {WORD[g]}, in gray, the nearest neighbors stand {three(mm['smallest_lightness_gap'])} apart in lightness "
                    f"(the bar is 0.08), and the two ends sit {three(ep['delta_L'])} apart, so a printed sign or a boxed arrow says "
                    f"which way each end runs.")
            need(mm["smallest_lightness_gap"] >= 0.08, f"diverging on {g}: neighbors under 0.08 in lightness")
        else:
            gray = (f"On {WORD[g]}, in gray, the nearest neighbors stand {three(mm['smallest_lightness_gap'])} apart in lightness "
                    f"(the bar is 0.08), and the {word}s keep their order"
                    + ("" if mm.get("grayscale_order_holds") else ", which fails") + ".")
            need(mm["smallest_lightness_gap"] >= 0.08 and mm.get("grayscale_order_holds"), f"{p['id']} on {g}: gray order or 0.08 fails")
        cv = mm["closest"]
        pairs = "every two groups" if p["id"] == "categorical" else f"neighboring {word}s"
        worst = min(cv[k]["delta_e_ok"] for k in ("protanopia", "deuteranopia", "tritanopia"))
        sims = "; ".join(f'{k}, {three(cv[k]["delta_e_ok"])}, {cv[k]["between"][0].lower()} and {cv[k]["between"][1].lower()}'
                         for k in ("protanopia", "deuteranopia", "tritanopia"))
        bar = "" if p["id"] == "categorical" else " (the bar is 0.05)"
        held = ("" if p["id"] == "categorical" else (" All stay apart." if worst >= 0.05 else " Some come closer than the bar."))
        cvw = f"Closest {pairs} under each simulation, as a color distance{bar}: {sims}.{held}"
        out.append(f'<li><p class="ps-mg">{e(gray)}</p><p class="ps-mg">{e(cvw)}</p></li>')
    return '<ul class="ps-ms" role="list">' + "".join(out) + "</ul>"


def palette_block(p):
    m = measures(p)
    extra = ""
    if p["id"] == "sequential":
        extra = (f'<p class="ps-note">Outline of a sized circle on a sequential map: <code class="ps-tk">{dotted("oa.chart.color.sequential.outline")}</code>, '
                 f'{e(hex_of("oa.chart.color.sequential.outline.onNewsprint")).replace("#", "&#35;")} on Newsprint and '
                 f'{e(hex_of("oa.chart.color.sequential.outline.onCharcoal")).replace("#", "&#35;")} on Charcoal.</p>')
    if p["id"] == "categorical":
        pitch = node("oa.chart.hatch.pitch")["$value"]["value"]
        weight = node("oa.chart.hatch.weight")["$value"]["value"]
        extra = (f'<p class="ps-note">Stone’s hatch: <code class="ps-tk">{dotted("oa.chart.hatch.pitch")}</code>, {pitch:g} px apart, and '
                 f'<code class="ps-tk">{dotted("oa.chart.hatch.weight")}</code>, {weight:g} px lines in Stone. Group 4’s label sits beside '
                 f'the hatch, in <code class="ps-tk">{dotted("oa.chart.color.categorical.labelBeside.group4")}</code>. Markers, in order: '
                 f'{", ".join(MARKER)}.</p>')
    carry = p["carry"].format(outline="oa.chart.color.sequential.outline") if p["carry"] else ""
    tok = (f'<p class="ps-note">Tokens: <code class="ps-tk">{dotted(p["fill"].format(n=1))}</code> to {p["word"].lower()} {p["steps"]}, each with '
           f'<code class="ps-tk">.<wbr>onNewsprint</code> and <code class="ps-tk">.<wbr>onCharcoal</code>; label inks '
           f'<code class="ps-tk">{dotted(p["label"].format(n=1))}</code> and on. In a form, name the role: '
           f'<code class="ps-tk">{p["code"]}-1</code> to <code class="ps-tk">{p["code"]}-{p["steps"]}</code>.'
           + (f" {e(carry)}" if carry else "") + "</p>")
    return (f'<div class="ps-pal" id="ps-{p["id"]}"><p class="ps-name">{e(p["name"])}</p><p class="ps-job">{e(p["job"])}</p>'
            f'{table(p, m)}{tok}{extra}<div class="ps-gs">{ground_panel(p, "newsprint", m)}{ground_panel(p, "charcoal", m)}</div>'
            f'{measures_words(p, m)}</div>')


def grade_line(key, w):
    """One grade's line at width w, by the atlas build's own marks (Rule 13.4), checked against the token's pattern."""
    tok = node(f"oa.chart.grade.{key}")["$value"]
    tex = {"documented": "solid", "wellSupported": "solid", "plausible": "dashed", "contested": "dash-dot", "hypothesis": "dotted"}[key]
    arr, cap = BS.pattern(tex, w)
    if isinstance(tok, dict):
        want = [x["value"] * w for x in tok["dashArray"]]
        need(arr is not None and [round(x, 6) for x in arr] == [round(x, 6) for x in want] and cap == tok["lineCap"],
             f"oa.chart.grade.{key} at {w} px: the token gives {want} {tok['lineCap']}, the atlas build {arr} {cap}")
    else:
        need(tok == "solid" and arr is None, f"oa.chart.grade.{key}: the token is {tok!r}, the atlas build draws {tex}")
    marks, _, _ = BS.wire_marks([(1, 8), (119, 8)], key, None, None, w, lit=False)
    marks = re.sub(r'<path class="ak-case"[^>]*/>', "", marks).replace(' fill="none"', "").replace(' stroke-linecap="butt"', "")
    marks = re.sub(r'\sstyle="[^"]*"', "", marks)
    return (f'<svg class="ps-ln" viewBox="0 0 120 16" width="120" height="16" aria-hidden="true" focusable="false">{marks}</svg>')


def grade_block():
    sq = node("oa.chart.grade.recordSquare")["$value"]["value"]
    rows = []
    for g in ("newsprint", "charcoal"):
        items = []
        for key in ("documented", "wellSupported", "plausible", "contested", "hypothesis"):
            word, gloss = GRADE_WORDS[key]
            lead = (f'<svg class="ps-rs" viewBox="0 0 {sq:g} {sq:g}" width="{sq:g}" height="{sq:g}" aria-hidden="true" focusable="false">'
                    f'<rect width="{sq:g}" height="{sq:g}"/></svg> ') if key == "documented" else ""
            items.append(f'<li><span class="ps-lns">{grade_line(key, 2)}{grade_line(key, 3)}</span>'
                         f'<span class="ps-gw">{lead}<b>{e(word)}</b>, {e(gloss)}</span></li>')
        rows.append(f'<div class="ps-g ps-gl oa-surface-{g}"><p class="ps-gn">On {WORD[g]}, at 2 and 3 px</p>'
                    f'<ul class="ps-gls" role="list">{"".join(items)}</ul></div>')
    pats = []
    for key in ("plausible", "contested", "hypothesis"):
        tok = node(f"oa.chart.grade.{key}")["$value"]
        pats.append(f'{GRADE_WORDS[key][0]}, {" and ".join(f"{x["value"]:g}" for x in tok["dashArray"])} for each pixel of the line’s width, '
                    f'{"round" if tok["lineCap"] == "round" else "square"} ends')
    tokens = ", ".join(f'<code class="ps-tk">{dotted("oa.chart.grade." + k)}</code>' for k in GRADE_WORDS)
    return (f'<div class="ps-pal" id="ps-grade"><p class="ps-name">The grade line code</p><p class="ps-job">{e(GRADE_JOB)}</p>'
            f'<div class="ps-gs">{"".join(rows)}</div>'
            f'<p class="ps-note">Tokens: {tokens}. Patterns: {e("; ".join(pats))}; each pattern stretches so the line starts and ends '
            f'on ink. The record square before Documented is {sq:g} px, <code class="ps-tk">{dotted("oa.chart.grade.recordSquare")}</code>.</p></div>')


def prussian_line():
    inks = [("Charcoal", "charcoal"), ("Verdigris", "verdigris"), ("Prussian", "prussian"), ("Stone", "stone")]
    rs = [contrast(hex_of(f"oa.color.palette.{k}"), GROUND["prussian"]) for _, k in inks]
    need(max(rs) < 3, "a group ink reaches 3 to 1 on Prussian; reread ruling b's Prussian line")
    lo, hi = min(rs), max(rs)
    return (f'<p class="ps-note ps-pru">On Prussian: no chart draws on it. A chart in a Prussian panel sits on its own Newsprint '
            f'or Charcoal plate, since the four group inks measure {ratio(lo).replace(" to 1", "")} to {ratio(hi)} on Prussian, under the 3 to 1 a mark '
            f'needs, and red never sits on Prussian (Rule 05.3).</p>')


def filters():
    out = []
    for sim in ("protanopia", "deuteranopia", "tritanopia"):
        mx = R0.CVD[sim]
        vals = " ".join(" ".join(f"{x:g}" for x in row) + " 0 0" for row in mx) + " 0 0 0 1 0"
        out.append(f'<filter id="ps-{sim}" color-interpolation-filters="linearRGB"><feColorMatrix type="matrix" values="{vals}"/></filter>')
    pitch = node("oa.chart.hatch.pitch")["$value"]["value"]
    weight = node("oa.chart.hatch.weight")["$value"]["value"]
    for g in ("newsprint", "charcoal"):
        out.append(f'<pattern id="ps-hatch-{SURF[g]}" width="{pitch:g}" height="{pitch:g}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                   f'<rect width="{pitch:g}" height="{pitch:g}" style="fill:var({css("oa.color.palette." + g)})"/>'
                   f'<line x1="0" y1="0" x2="0" y2="{pitch:g}" stroke-width="{weight:g}" style="stroke:var({css(fill_path(PALS[2], 4, g))})"/></pattern>')
    return f'<svg class="ps-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>{"".join(out)}</defs></svg>'


STYLE = """
.ps { font: var(--oa-type-body-small); color: var(--oa-color-text-primary); container-type: inline-size; --ps-ground: var(--oa-color-surface) }
.ps p { margin: 0 }
.ps-defs { position: absolute; width: 0; height: 0; overflow: hidden }
.ps-rel { font: var(--oa-type-caption); color: var(--oa-color-text-secondary); margin: 0 0 var(--oa-space-300) }
.ps-pal + .ps-pal { margin-top: var(--oa-space-600); padding-top: var(--oa-space-400); border-top: var(--oa-border-width-hairline) solid var(--oa-color-border-strong) }
.ps-name { font: var(--oa-type-ui); font-weight: var(--oa-font-weight-bold) }
.ps-job { margin-top: var(--oa-space-100); max-width: 42em; text-wrap: pretty }
.ps-note { margin-top: var(--oa-space-200); font: var(--oa-type-caption); color: var(--oa-color-text-secondary); max-width: 52em; text-wrap: pretty }
.ps-tk { overflow-wrap: normal; word-break: normal; hyphens: manual }
.ps-tw { margin-top: var(--oa-space-300) }
.ps-t { border-collapse: collapse; width: 100%; table-layout: fixed }
.ps-t caption { text-align: left; font: var(--oa-type-caption); color: var(--oa-color-text-secondary); padding-bottom: var(--oa-space-100) }
.ps-t thead th { font: var(--oa-type-label); letter-spacing: var(--oa-type-label-letter-spacing); text-transform: uppercase; text-align: left;
  padding: var(--oa-space-100) var(--oa-space-200) var(--oa-space-100) 0; border-bottom: var(--oa-border-width-hairline) solid var(--oa-color-border-strong) }
.ps-t tbody th, .ps-t td { text-align: left; vertical-align: top; padding: var(--oa-space-150) var(--oa-space-200) var(--oa-space-150) 0;
  border-bottom: var(--oa-border-width-hairline) solid var(--oa-color-border-hairline); font: var(--oa-type-caption); font-weight: var(--oa-font-weight-regular) }
.ps-t tbody tr:last-child > * { border-bottom: 0 }
.ps-t th[scope="row"] .ps-sw { display: block; margin-bottom: var(--oa-space-100) }
.ps-st { display: block; font: var(--oa-type-caption); font-weight: var(--oa-font-weight-bold) }
.ps-cd, .ps-hn { display: block }
.ps-v { display: block; font-variant-numeric: tabular-nums; font-weight: var(--oa-font-weight-semibold); white-space: nowrap }
.ps-l { display: block; font-variant-numeric: tabular-nums }
.ps-sw, .ps-strip, .ps-ln, .ps-rs { forced-color-adjust: none; print-color-adjust: exact; -webkit-print-color-adjust: exact }
.ps-sw text { font-family: var(--oa-font-family-reading); font-size: var(--oa-chart-type-tick); font-weight: var(--oa-font-weight-semibold); font-variant-numeric: tabular-nums }
.ps-edge { fill: none; stroke: var(--oa-color-border-strong); stroke-width: 1px }
.ps-gs { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--oa-space-300); margin-top: var(--oa-space-300) }
@container (min-width: 40rem) { .ps-gs { grid-template-columns: repeat(2, minmax(0, 1fr)) } }
.ps-g { padding: var(--oa-space-300); background: var(--oa-color-surface); color: var(--oa-color-text-primary); --ps-ground: var(--oa-color-surface);
  box-shadow: inset 0 0 0 var(--oa-border-width-hairline) var(--oa-color-border-strong) }
.ps-gn { font: var(--oa-type-caption); font-weight: var(--oa-font-weight-bold); margin-bottom: var(--oa-space-200) }
.ps-sws { display: flex; flex-wrap: wrap; gap: var(--oa-space-100); margin: 0; padding: 0; list-style: none }
.ps-sws li { display: flex; flex-direction: column; align-items: center; gap: var(--oa-space-050); font: var(--oa-type-caption) }
.ps-mk { color: var(--oa-color-text-secondary) }
.ps-pr { display: grid; grid-template-columns: 7.5rem minmax(0, 1fr); gap: var(--oa-space-200); align-items: start; margin-top: var(--oa-space-150) }
.ps-prk { font: var(--oa-type-caption); color: var(--oa-color-text-secondary) }
.ps-strip { display: block; width: 100%; max-width: 15rem; height: 20px }
.ps-ls { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); max-width: 15rem; margin: var(--oa-space-050) 0 0; padding: 0; list-style: none;
  font: var(--oa-type-caption); font-variant-numeric: tabular-nums; color: var(--oa-color-text-secondary); text-align: center }
.ps-ms { margin: var(--oa-space-300) 0 0; padding: 0; list-style: none; display: grid; gap: var(--oa-space-150) }
.ps-mg { font: var(--oa-type-caption); max-width: 52em; text-wrap: pretty }
.ps-mg + .ps-mg { margin-top: var(--oa-space-050) }
.ps-gls { margin: 0; padding: 0; list-style: none; display: grid; gap: var(--oa-space-150) }
.ps-gls li { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: var(--oa-space-200); align-items: center; font: var(--oa-type-caption) }
.ps-lns { display: grid; gap: var(--oa-space-050) }
.ps-ln { display: block }
.ps-ln path { fill: none }
.ps-ln .ak-mark { stroke: var(--oa-color-graphic-essential) }
.ps-ln .hd { fill: var(--oa-color-graphic-essential) }
.ps-rs { display: inline-block; fill: var(--oa-color-graphic-essential); vertical-align: .08em; margin-right: 2px }
.ps-gw b { font-weight: var(--oa-font-weight-bold) }
/* under 40rem each table row stands as a block: the step, then each value under its column's word (6.6, as chapter 26's table) */
@container (max-width: 39.99rem) {
  .ps-t thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%) }
  .ps-t, .ps-t tbody { display: block }
  .ps-t tr { display: block; padding: var(--oa-space-150) 0; border-bottom: var(--oa-border-width-hairline) solid var(--oa-color-border-hairline) }
  .ps-t tbody tr:last-child { border-bottom: 0 }
  .ps-t tbody th, .ps-t td { display: block; border: 0; padding: var(--oa-space-050) 0 }
  .ps-t td::before { display: block; font: var(--oa-type-label); letter-spacing: var(--oa-type-label-letter-spacing); text-transform: uppercase; color: var(--oa-color-text-secondary) }
  .ps-t td:nth-child(2)::before { content: "Token" }
  .ps-t td:nth-child(3)::before { content: "On Newsprint" }
  .ps-t td:nth-child(4)::before { content: "On Charcoal" }
  .ps-t td:nth-child(5)::before { content: "On White paper" }
}
@media print { .ps-pal { break-inside: auto } .ps-g, .ps-t tr { break-inside: avoid } }
"""


def build():
    method = ("Contrast is WCAG 2.2’s ratio, rounded down to two places, so no value rounds up across a bar: 4.5 to 1 for text and "
              "3 to 1 for a mark. Lightness is OKLab’s, from 0 for black to 1 for white. The gray row runs each swatch through the "
              "browser’s grayscale filter. The color-vision rows simulate protanopia (no red-sensing cones), deuteranopia (no "
              "green-sensing cones) and tritanopia (no blue-sensing cones) by Machado, Oliveira and Fernandes (2009) at full strength, "
              "which models full color blindness only; a color distance is the OKLab distance between two colors.")
    body = (f'<div class="ps"><p class="ps-rel">Tokens {e(RELEASE)}. Every value, ratio and lightness below is read from the token files by script.</p>'
            f'{filters()}{"".join(palette_block(p) for p in PALS)}{grade_block()}{prussian_line()}'
            f'<p class="ps-note">{e(method)}</p></div>')
    frag = (f"<!-- {SID}: Oath & Action guide, Edition 06, chapter 14 (R5-3). Written by work/build/scripts/phase-3/palette_spec_build.py "
            f"from tokens {RELEASE}; never edit by hand. -->\n<style>{re.sub(r'[ ]*\\n[ ]*', ' ', STYLE.strip())}</style>\n{body}\n")
    meta = {"alt": ("The four data palettes, step by step, on Newsprint and Charcoal: each step’s token, value and contrast in a table, "
                    "its swatch with its label ink, and proofs in gray and for three kinds of color blindness, then the grade line code."),
            "readable": True, "fit_switch": False,
            "notes": f"Written by palette_spec_build.py from tokens {RELEASE} (R5-3); round 0's measures on today's tokens",
            "label": "The data palettes, specified",
            "caption": ("Each data palette Rule 14.5 names, step by step: its tokens, its values on Newsprint and Charcoal, each value’s "
                        "contrast, and proofs in gray and for three kinds of color blindness. A script writes this plate from the token files.")}
    return frag, json.dumps(meta, indent=1, ensure_ascii=False) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    frag, meta = build()
    for f in FAULTS:
        print(f"  fault: {f}")
    files = {OUT: frag, META: meta}
    stale = [p for p, t in files.items() if not p.exists() or p.read_text() != t]
    if a.check:
        for p in stale:
            print(f"palette_spec_build --check: {p.relative_to(ROOT)} is not what tokens {RELEASE} makes; run the script")
        print(f"palette_spec_build --check: {len(files) - len(stale)} of {len(files)} files current, tokens {RELEASE}")
        return 1 if stale or FAULTS else 0
    for p in stale:
        p.write_text(files[p])
    print(f"palette_spec_build: tokens {RELEASE}; {OUT.relative_to(ROOT)} {len(frag.encode()):,} bytes; {len(stale)} file(s) written; "
          f"{len(FAULTS)} fault(s)")
    return 1 if FAULTS else 0


if __name__ == "__main__":
    sys.exit(main())
