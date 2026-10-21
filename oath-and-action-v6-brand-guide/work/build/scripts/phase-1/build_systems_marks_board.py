#!/usr/bin/env python3
"""Build the Systems Marks Board from the V7 query output.

Run:  python3 -I work/build/scripts/phase-1/systems_marks_data.py
      python3 -I work/build/scripts/phase-1/build_systems_marks_board.py
Reads  work/boards/phase-1/systems/20261021_Systems-Marks-Data.json (every V7 value on the board)
       work/boards/phase-1/systems/20261021_Board-Check-Results.json (optional, written by check_systems_board.js)
Writes work/boards/20261021_Systems-Marks-Board.html
"""
import html
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import svg_marks as M  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
ASSETS = ROOT / "work/boards/phase-1/systems"
DATA = json.loads((ASSETS / "20261021_Systems-Marks-Data.json").read_text(encoding="utf-8"))
CHECK_PATH = ASSETS / "20261021_Board-Check-Results.json"
CHECK = json.loads(CHECK_PATH.read_text(encoding="utf-8")) if CHECK_PATH.exists() else None
OUT = ROOT / "work/boards/20261021_Systems-Marks-Board.html"
A = "phase-1/systems/"
esc = html.escape
MINUS = M.MINUS
SURF = ["Newsprint", "White", "Charcoal", "Prussian"]
CC = DATA["chip_contrast"]
LP = DATA["loops"]
LX = DATA["links_example"]
R01 = DATA["reform_R01"]
FX = DATA["effects"]
Q = DATA["quotes"]


def tm(s):
    """True minus in displayed effect and sign values."""
    return s.replace("-S", MINUS + "S").replace("-M", MINUS + "M").replace("-L", MINUS + "L")


def date_long(iso):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    y, m, d = iso.split("-")
    return f"{months[int(m) - 1]} {int(d)}, {y}"


def tag(kind):
    cls = {"Defect fix": "tag defect", "Option": "tag", "Original": "tag orig", "Misuse": "tag misuse",
           "Recommended": "tag best", "Confirm with changes": "tag", "Revise": "tag", "Add as a fifth base": "tag"}[kind]
    return f'<span class="{cls}">{esc(kind)}</span>'


def surfaces(fn, note=None, gray=True):
    """fn(surface) returns inner HTML for one cell. Draws the four surfaces, then the same four in grayscale."""
    def row(cls_extra, label_suffix):
        cells = []
        for s in SURF:
            cells.append(f'<div class="s-{s.lower()}"><p class="slab">{s}{label_suffix}</p>{fn(s)}</div>')
        return f'<div class="surfaces{cls_extra}">' + "".join(cells) + "</div>"
    out = row("", "")
    if gray:
        out += row(" gray", " · grayscale")
    if note:
        out += f'<p class="cap">{note}</p>'
    return out


def chip(kind, code, compact=False):
    words = {"variable": ("Variable", "Var"), "connection": ("Connection", "Conn"), "loop": ("Loop", "Loop"),
             "reform": ("Reform", "Reform"), "issue": ("Issue", "Issue"), "claim": ("Claim", "Claim"),
             "domain": ("Domain", "Domain"), "route": ("Route", "Route"), "standard": ("Rule", "Rule"),
             "rule change": ("Rule change", "Rule change"), "delivery": ("Delivery case", "Case")}[kind]
    w = words[1] if compact else words[0]
    return f'<span class="chip"><span class="k">{esc(w)}</span><span class="c">{esc(code)}</span></span>'


def contrast_note(s):
    c = CC[s]
    return (f'<p class="meas">Code {c["code_text_on_surface"]:.2f}:1 · type word {c["kind_text_on_ink_fill"]:.2f}:1'
            f'<br>Grayscale {c["grayscale_code"]:.2f}:1</p>')


def figure(inner, caption, source, cls="fig s-newsprint"):
    return (f'<figure class="{cls}">{inner}<figcaption><p>{caption}</p><p class="src">{source}</p></figcaption></figure>')


SRC_V7 = "Source: Who Do They Answer To? Systems Atlas V7, snapshot " + date_long(DATA["generated"]["snapshot"])


def link_of(lid, loop):
    for l in LP[loop]["link_detail"]:
        if l["id"] == lid:
            return l
    return LX[lid]


def loop_nodes(loop):
    return [(n["id"], n["label"]) for n in LP[loop]["node_detail"]]


def loop_fig(loop, rings=None, record=True, W=320):
    det = LP[loop]["link_detail"]
    return M.vloop(loop_nodes(loop), det[:-1], det[-1], W=W, record_mark=record, rings=rings,
                   label=f"Loop {loop}: {LP[loop]['title']}")


def equivalent_table(loop):
    rows = []
    for l in LP[loop]["link_detail"]:
        rows.append(f'<tr><td>{chip("connection", l["id"])}</td><td>{esc(l["from"])} to {esc(l["to"])}</td>'
                    f'<td>{M.sign_glyph(l["polarity"])}</td><td>{esc(l["type"])}</td><td>{esc(M.GRADE_WORD[l["evidence"]])}</td>'
                    f'<td>{esc(M.DELAY_WORD[l["delay"]])}</td><td>{esc(l["name"])}</td></tr>')
    return ('<div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="eq"><caption>Table equivalent, Loop ' + esc(loop) + '</caption><thead><tr><th>Connection</th><th>From, to</th>'
            '<th>Sign</th><th>Type</th><th>Grade</th><th>Delay</th><th>V7 name</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")


def loop_head(loop):
    lp = LP[loop]
    kind = "Reinforcing loop" if lp["type"] == "R" else "Balancing loop"
    return (f'<div class="loophead">{chip("loop", loop)} <span class="lt">{esc(lp["title"])}</span>'
            f'<span class="lk">{kind} · {esc(lp["closure"].split(":")[0])} · V7 loop grade: “{esc(lp["evidence"])}”</span></div>')


# ======================================================================= section 1: evidence lines
def spec_lines(rows, opacity=False):
    def cell(s):
        out = []
        for word, grade, dash, op in rows:
            line = M.line_specimen(grade, 104, dash=dash, opacity=op if opacity else None)
            out.append(f'<div class="ls"><span class="lw">{esc(word)}</span>{line}</div>')
        return "".join(out)
    return cell


V5_ROWS = [("Documented", "documented", "", None), ("Well supported", "well-supported", "", None), ("Plausible", "plausible", "", None),
           ("Contested", "contested", "", None), ("Hypothesis", "hypothesis", "8 7", None)]
V7_ROWS = [("Documented", "documented", None, None), ("Well supported", "well-supported", None, None),
           ("Plausible", "plausible", None, None), ("Contested", "contested", None, None), ("Hypothesis", "hypothesis", None, None)]
RAMP_ROWS = [("Documented", "documented", "", 1), ("Well supported", "well-supported", "", 0.8), ("Plausible", "plausible", "", 0.6),
             ("Contested", "contested", "", 0.45), ("Hypothesis", "hypothesis", "", 0.3)]


def record_rows(s):
    out = []
    for word, grade, _, _ in V7_ROWS:
        line = M.line_specimen(grade, 104)
        _, p = M.pill(0, 1, "L08 +" if grade == "documented" else "L25 " + MINUS, record=(grade == "documented"))
        pills = M.svg(78, 24, p, "label pill", "mk inl") if grade in ("documented", "well-supported") else ""
        out.append(f'<div class="ls"><span class="lw">{esc(word)}</span>{line}{pills}</div>')
    return "".join(out)


def conceptual_rows(s):
    out = [f'<div class="ls"><span class="lw">Plausible, for comparison</span>{M.line_specimen("plausible", 104)}</div>',
           f'<div class="ls"><span class="lw">V7 conceptual step</span>'
           f'{M.svg(104, 18, M.connection([(4, 9), (100, 9)], "plausible", dash_override="5 4").replace("currentColor", "#8B9095"), "V7 conceptual step")}</div>',
           f'<div class="ls"><span class="lw">Proposal: hollow line</span>{M.line_specimen("plausible", 104, conceptual=True)}</div>']
    return "".join(out)


def section_evidence():
    r1 = LP["R1"]
    r10 = LP["R10"]
    L02 = link_of("L02", "R1")
    return f'''
<section id="m1">
  <p class="eyebrow">Mark 1</p>
  <h2>1. Evidence line code</h2>
  <p>A connection's line texture shows its evidence grade. V7 sets the code twice, in its methods text and in its renderer: hypothesis dotted, plausible dashed, contested dash-dot, documented and well supported solid. V5 Polished and the Atlas Visual System dash hypotheses and draw every other grade solid, so their key contradicts the model. Concepts V2 already follows V7. Every specimen below is a 2 px line drawn at true size with V7's dash lengths ({esc(DATA["renderer"]["edge_css_dashes"]["u-plausible"])}, {esc(DATA["renderer"]["edge_css_dashes"]["u-contested"])} and {esc(DATA["renderer"]["edge_css_dashes"]["u-hypothesis"])}).</p>

  <div class="opt">
    <div class="opthead">{tag("Original")}<h3>V5 Polished and the Atlas Visual System</h3></div>
    <p>Their working rules say: "Hypotheses use 8/7 dashes ... All other evidence distinctions remain textual." Plausible links such as L02 are drawn solid, the same as their well supported neighbors.</p>
    {surfaces(spec_lines(V5_ROWS))}
  </div>

  <div class="opt">
    <div class="opthead">{tag("Defect fix")}<h3>A. V7's code</h3></div>
    <p>Four textures for five grades. Documented and well supported share the solid line, as they do in V7's legend ("documented or well supported").</p>
    {surfaces(spec_lines(V7_ROWS))}
  </div>

  <div class="opt rec-opt">
    <div class="opthead">{tag("Option")}{tag("Recommended")}<h3>B. V7's code, with the record square on documented labels</h3></div>
    <p>The lines stay exactly V7's. The connection label adds a small filled square when the grade is documented. The square says "on the public record", so a reader of a print or grayscale copy can tell documented from well supported without the key.</p>
    {surfaces(record_rows)}
  </div>

  <div class="opt">
    <div class="opthead">{tag("Misuse")}<h3>C. A weight or opacity ramp</h3></div>
    <p>Fading lines as evidence weakens looks orderly in color. In grayscale the middle steps blur together, and a fainter or thinner line reads as a smaller effect, which mixes grade with size.</p>
    {surfaces(spec_lines(RAMP_ROWS, opacity=True))}
  </div>

  <div class="opt">
    <div class="opthead">{tag("Option")}<h3>Conceptual steps</h3></div>
    <p>A conceptual loop has no complete numbered chain ({", ".join("Loop " + k for k in ["B2", "B3", "R9"])}). V7 draws its steps as a lighter gray dash ({esc(DATA["renderer"]["edge_css_dashes"]["u-concept"])}, #8B9095). Plausible steps are dashed too ({esc(DATA["renderer"]["edge_css_dashes"]["u-plausible"])}), so the two differ only in shade and dash length. The proposal is a hollow line: two hairlines around an empty core, which no grade uses and which survives grayscale.</p>
    {surfaces(conceptual_rows)}
  </div>

  <h3 class="exh">Real examples</h3>
  <div class="ex2">
    {figure(loop_head("R1") + loop_fig("R1"),
            f'Loop R1 shows the least certain step. L02 ({esc(L02["name"])}) is plausible, so its line is dashed while L01 and L03 stay solid. V7 grades the whole loop "{esc(r1["evidence"])}": a loop is no surer than its least certain step, and V7 never estimates how strong a whole loop is. The ticks count the delay (Mark 6).',
            SRC_V7 + "; loop R1, connections L01, L02, L03. Box labels are V7's chain labels.")}
    {figure(loop_head("R10") + loop_fig("R10"),
            'Loop R10 shows how documented differs from well supported. Both are solid. L08 and L42 are documented: the record itself shows the link, through counts of seats settled in primaries and of maps drawn by incumbents, and the grade says nothing about the size of an effect unless the record does. L25 is well supported: strong studies agree on the direction of the effect. The record square marks the documented pair. L53 is plausible and dashed, and V7 calls it "the weakest link".',
            SRC_V7 + "; loop R10, connections L08, L25, L53, L42.")}
  </div>
  {equivalent_table("R1")}
  {equivalent_table("R10")}
  <div class="rec"><p class="eyebrow">Recommendation</p>
    <p><b>Adopt V7's line code exactly and retire the V5 dash rule (defect fix). Add the record square to documented labels (option B).</b> Print the grade word beside every connection on public views, draw conceptual steps as a hollow line, and keep every graded line at least 48 px long so its texture shows two full cycles. The square sits in the label, so the line itself stays identical to V7's renderer.</p>
    <p class="cap">Every example prints the sign in the connection label, as V7 does ("L25 {MINUS}"). V7's methods text: "{esc(Q["methods_sign"])}"</p>
  </div>
</section>'''


# ======================================================================= section 2: grade words
GRADES_ALL = ["documented", "well-supported", "plausible", "contested", "mixed", "hypothesis", "not yet tested"]
V2_WORDS = {"documented": "On the record", "well-supported": "Strong evidence", "plausible": "Some evidence",
            "contested": "Disputed", "hypothesis": "Untested"}
GLOSS = {"documented": "on the public record", "well-supported": "strong studies agree on the direction",
         "plausible": "a coherent mechanism with some evidence", "contested": "credible studies disagree",
         "mixed": "evidence differs for different parts", "hypothesis": "proposed, not yet supported",
         "not yet tested": "no evaluation exists yet"}


def grade_cell(mode):
    def cell(s):
        out = []
        order = ["well-supported", "documented", "plausible", "contested", "hypothesis"] if mode == "v2" else GRADES_ALL
        for g in order:
            if mode == "v2" and g not in V2_WORDS:
                continue
            word = V2_WORDS[g] if mode == "v2" else DATA["renderer"]["grade_table"][g]["label"]
            sample = M.grade_sample(g if g in M.DASH else "plausible", 34) if g in M.DASH else '<span class="nosample"></span>'
            gl = f'<span class="gl">{esc(GLOSS[g])}</span>' if mode == "hybrid" else ""
            out.append(f'<div class="gw">{sample}<span><b>{esc(word)}</b>{gl}</span></div>')
        return "".join(out)
    return cell


def mapping_table():
    g = DATA["grades"]

    def n(field, key):
        v = g[field].get(key)
        return f'<span class="code">{esc(key)}</span> {v}' if v else "<span class=\"none\">none</span>"
    rd = g["reforms.problem_evidence.grade"]
    rr = g["reforms.remedy_evidence.grade"]
    rows = [
        ("Documented", GLOSS["documented"], n("links.evidence", "documented"), n("issues.grade", "documented"),
         n("issues.remedy_note (first word)", "Documented"), n("claims.confidence", "documented"),
         f'{rd.get("documented", 0)} / {rr.get("documented", 0)}', n("deliveryLog.rows.evidence_grade", "documented"),
         "Record and event verbs: “records”, “shows”, “counted”"),
        ("Well supported", GLOSS["well-supported"], n("links.evidence", "well-supported"), n("issues.grade", "well_supported"),
         n("issues.remedy_note (first word)", "Well supported"), n("claims.confidence", "well-supported"),
         f'{rd.get("well-supported", 0)} / {rr.get("well-supported", 0)}', n("deliveryLog.rows.evidence_grade", "well-supported"),
         "A direct finding: “raises”, “lowers”"),
        ("Plausible", GLOSS["plausible"], n("links.evidence", "plausible"), n("issues.grade", "plausible"),
         n("issues.remedy_note (first word)", "Plausible"), n("claims.confidence", "plausible"),
         f'{rd.get("plausible", 0)} / {rr.get("plausible", 0)}', n("deliveryLog.rows.evidence_grade", "plausible"),
         "“can”, “may”"),
        ("Contested", GLOSS["contested"],
         n("links.evidence", "plausible_contested") + f'<br><span class="cap">plus <span class="code">contested: true</span> on the same {len(DATA["grade_facts"]["contested_flag_links"])}</span>',
         "<span class=\"none\">none</span>", n("issues.remedy_note (first word)", "Contested"), n("claims.confidence", "contested"),
         f'{rd.get("plausible_contested", 0)} / {rr.get("plausible_contested", 0)} <span class="code">plausible_contested</span>; 0 / {rr.get("contested", 0)} <span class="code">contested</span>',
         "<span class=\"none\">none</span>", "Name both readings: “Studies disagree on whether …”"),
        ("Mixed", GLOSS["mixed"], "<span class=\"none\">none (defined in methods)</span>", "<span class=\"none\">none</span>",
         n("issues.remedy_note (first word)", "Mixed") + f' ({", ".join(DATA["grade_facts"]["mixed_remedy_issue"])})',
         "<span class=\"none\">none</span>", "0 / 0", "<span class=\"none\">none</span>", "Say which part holds"),
        ("Hypothesis", GLOSS["hypothesis"], n("links.evidence", "hypothesis"), n("issues.grade", "hypothesis"),
         n("issues.remedy_note (first word)", "Hypothesis"), "<span class=\"none\">none</span>",
         f'{rd.get("hypothesis", 0)} / {rr.get("hypothesis", 0)}', "<span class=\"none\">none</span>", "Label first: “Hypothesis: …”"),
        ("Not yet tested", GLOSS["not yet tested"], "<span class=\"none\">none</span>", "<span class=\"none\">none</span>",
         "<span class=\"none\">none (renderer and glossary only)</span>", "<span class=\"none\">none</span>", "0 / 0",
         "<span class=\"none\">none</span>", "“No evaluation yet”"),
    ]
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" if i else f"<th scope=\"row\">{c}</th>" for i, c in enumerate(r)) + "</tr>" for r in rows)
    status = (f'<tr><th scope="row">Retired (a status)</th><td>record kept for reference</td><td></td><td>{n("issues.grade", "retired")} '
              f'({", ".join(DATA["grade_facts"]["retired_issue"])})</td><td><span class="code">Retired</span> 1</td><td></td><td></td><td></td><td>Show as a status chip, never as a grade</td></tr>')
    return ('<div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="map"><caption>Display words mapped to every V7 grade field. Counts are records, read by script.</caption>'
            '<thead><tr><th>Display word</th><th>Gloss in keys</th><th>Connections <span class="code">links[].evidence</span></th>'
            '<th>Issues <span class="code">issues[].grade</span></th><th>Issue remedies, first word of <span class="code">remedy_note</span></th>'
            '<th>Claims <span class="code">claims[].confidence</span></th><th>Reforms, problem / remedy <span class="code">*_evidence.grade</span></th>'
            '<th>Delivery log <span class="code">evidence_grade</span></th><th>Title verb (brief section 15)</th></tr></thead><tbody>'
            + body + status + "</tbody></table></div>")


def other_vocab():
    g = DATA["grades"]
    rd = g["repairLog.rows.direction"]
    ec = g["reforms.effects_confidence"]
    return f'''<div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="eq"><caption>Words that look like grades and are not</caption>
<thead><tr><th>V7 field</th><th>Values</th><th>Display rule</th></tr></thead><tbody>
<tr><td><span class="code">repairLog.rows[].direction</span></td><td><span class="code">mixed</span> {rd.get("mixed")} of {sum(rd.values())}</td><td>“Mixed direction”, so it never reads as the grade Mixed</td></tr>
<tr><td><span class="code">repairLog.rows[].verified</span></td><td><span class="code">false</span> {g["repairLog.rows.verified"].get("false")} of {sum(g["repairLog.rows.verified"].values())}</td><td>“Source not checked” beside the row, as V7 labels it</td></tr>
<tr><td><span class="code">issues[].jurisdiction</span></td><td><span class="code">mixed</span> {g["issues.jurisdiction = mixed"].get("mixed")}</td><td>“Several levels of government”</td></tr>
<tr><td><span class="code">reforms[].effects_confidence</span></td><td>high, medium, low; {ec.get("free text with scopes")} of 50 carry scopes, such as R-01's “{esc(R01["effects_confidence"])}”</td><td>“Confidence in the effect: …”, printed apart from the grade and the effect mark</td></tr>
<tr><td><span class="code">routes … feasibility</span></td><td>high, medium, low, very low</td><td>“Feasibility: medium”, always with its noun, because confidence also uses medium and low</td></tr>
<tr><td><span class="code">loops[].evidence</span></td><td>free text, for example R10: “{esc(LP["R10"]["evidence"])}”</td><td>Show each step's grade on its connection, and the loop's text in the record panel</td></tr>
</tbody></table></div>'''


def section_grades():
    r8 = LP["R8"]
    return f'''
<section id="m2">
  <p class="eyebrow">Mark 2</p>
  <h2>2. Grade display words</h2>
  <p>V7 stores its grades in six places, spelled four ways: <span class="code">well-supported</span> and <span class="code">plausible_contested</span> on connections, <span class="code">well_supported</span> and <span class="code">retired</span> on issues, <span class="code">contested</span> on claims, and both contested spellings on reform remedies. Issue remedy grades live only as the first word of a note. The methods text also defines Mixed, and the renderer adds Not yet tested. V7's renderer maps all of them to five labels. Concepts V2 wrote plainer words for its boards.</p>

  <div class="opt">
    <div class="opthead">{tag("Option")}<h3>A. V7's labels</h3></div>
    <p>The words a reader finds in the atlas glossary and methods text, in V7's order with documented first.</p>
    {surfaces(grade_cell("v7"))}
  </div>
  <div class="opt">
    <div class="opthead">{tag("Option")}<h3>B. Concepts V2's plain labels</h3></div>
    <p>Friendly, and in conflict with V7 in three places. “Untested” sits beside V7's own “Not yet tested”, which means something else: no evaluation of a response exists yet. Concepts V2 keys put “Strong evidence” above “On the record”, while V7 ranks documented first. The atlas glossary carries none of these words.</p>
    {surfaces(grade_cell("v2"))}
  </div>
  <div class="opt rec-opt">
    <div class="opthead">{tag("Option")}{tag("Recommended")}<h3>C. Hybrid: V7's word, with a plain gloss</h3></div>
    <p>The label is V7's word. The key and the first use on a page add a short gloss in plain language, drawn from V7's own definitions. Mixed and Not yet tested appear only where a record uses them.</p>
    {surfaces(grade_cell("hybrid"))}
  </div>

  <h3 class="exh">Mapping table across record types</h3>
  {mapping_table()}
  {other_vocab()}

  <h3 class="exh">Real example</h3>
  <div class="ex2">
    {figure(loop_head("R8") + loop_fig("R8"),
            f'Loop R8 has the same grade word on both steps, and V7 still treats them differently in prose: it calls L39 “the weaker step because equity is one motive among several for opposing construction”. The grade word cannot carry that, so the record panel quotes it. V7 also records a revision in the loop’s grade, “the loop no longer depends on A1”, and its qualification gives the reason: rising home equity tends to lower the top 1% share of wealth (T12).',
            SRC_V7 + "; loop R8, connections L38, L39.")}
    <div class="panel recpanel s-newsprint">
      <p class="eyebrow">Record panel, Loop R8</p>
      <dl>
        <dt>What the record shows</dt><dd>Both steps are graded <b>Well supported</b>: strong studies agree on the direction.</dd>
        <dt>What still needs an answer</dt><dd>V7 calls L39 “{esc(re.search(r"(the weaker step[^.]*)", r8["evidence_summary"]).group(1))}”.</dd>
        <dt>Model note</dt><dd>V7: “{esc(r8["evidence"])}”.</dd>
        <dt>Qualification</dt><dd>{esc(r8["qualification"])}</dd>
      </dl>
      <p class="src">{SRC_V7}; loops.R8.evidence, evidence_summary and qualification, quoted.</p>
    </div>
  </div>
  <div class="rec"><p class="eyebrow">Recommendation</p>
    <p><b>Hybrid (option C).</b> Use V7's labels as the words, in V7's order with documented first, so the guide and the atlas say the same thing. Add the plain gloss in every key and at first use. Keep V7's stored codes in data files and downloads. Map <span class="code">plausible_contested</span> and <span class="code">contested</span> to one word, Contested, as V7's renderer does, and keep the stored code in the record panel. Never use Concepts V2's words as labels.</p>
  </div>
</section>'''


# ======================================================================= section 3: chips
KIND_ROWS = ["variable", "connection", "loop", "reform", "issue", "claim", "domain", "route", "standard"]


def chips_collision_cell(s):
    pairs = DATA["collisions"]["pairs"][:2]
    out = []
    for p in pairs:
        a, b = p["a"], p["b"]
        out.append(f'<div class="cp">{chip(a[0], a[1])}<span class="cn">{esc(a[2])}</span></div>'
                   f'<div class="cp">{chip(b[0], b[1])}<span class="cn">{esc(b[2])}</span></div>')
    return "".join(out) + contrast_note(s)


def chips_compact_cell(s):
    return ('<div class="cp">' + chip("variable", "B4", True) + " " + chip("loop", "B4", True) + '</div><div class="cp">'
            + chip("loop", "R1", True) + " " + chip("reform", "R-01", True) + '</div><div class="cp">' + chip("standard", "05.1", True) + "</div>")


def bare_cell(s):
    return '<div class="cp bare">' + "".join(f'<span class="bchip">{c}</span>' for c in ["D5", "C3", "C5", "B4"]) + "</div>" \
           '<p class="cap2">Ring chips and the loop ID in one row. B4 here is the loop.</p>'


def v7style_cell(s):
    return ('<p class="v7r"><span class="code">Variable B4:</span> Hostility toward the other political party</p>'
            '<p class="v7r"><span class="code">Loop B4:</span> Electoral consequences can improve public performance</p>'
            '<p class="v7r"><span class="code">R1:</span> Wealth and political influence reinforce each other</p>'
            '<p class="v7r"><span class="code">R-01:</span> All-party primaries with ranked general elections</p>')


def kinds_table():
    kl = DATA["renderer"]["kind_label"]
    v7 = {"variable": kl.get("variable"), "connection": kl.get("connection"), "loop": kl.get("loop"), "reform": kl.get("reform"),
          "issue": kl.get("issue"), "claim": kl.get("claim"), "domain": kl.get("domain"), "route": kl.get("route"), "standard": "none (guide rule, architecture map)"}
    rows = []
    for k in KIND_ROWS:
        ex = DATA["chip_examples"][k]
        rows.append(f'<tr><td>{chip(k, ex["code"])}</td><td>{chip(k, ex["code"], True)}</td><td>{esc(v7[k])}</td><td>{esc(ex["name"] or "")}</td></tr>')
    return ('<div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="eq"><caption>The nine chip types, with V7 examples. V7 column: the label V7\'s renderer uses for that kind.</caption>'
            '<thead><tr><th>Full chip</th><th>Compact chip</th><th>V7 renderer label</th><th>Name of the example in V7</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def near_table():
    rows = []
    for p in DATA["collisions"]["pairs"][2:]:
        cells = [p["a"], p["b"]] + ([p["c"]] if "c" in p else [])
        rows.append("<tr>" + "".join(f'<td>{chip(c[0], c[1])}<br><span class="cap">{esc(c[2])}</span></td>' for c in cells)
                    + ("<td></td>" if len(cells) == 2 else "") + "</tr>")
    return ('<div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="eq"><caption>Near collisions the script found beyond the two in the brief</caption><thead><tr><th>Record</th><th>Looks like</th><th>And</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def r01_card():
    def tchip(t):
        return chip("connection" if t["kind"] == "connection" else "variable", t["id"])
    targets = " ".join(tchip(t) for t in R01["target_detail"])
    loops = " ".join(chip("loop", k) for k in R01["loops"])
    r11 = LP["R11"]
    return f'''<div class="panel card s-newsprint">
  <p class="eyebrow">Reform card, built from V7</p>
  <p class="ct">{chip("reform", "R-01")} <b>{esc(R01["title"])}</b></p>
  <dl>
    <dt>Acts on</dt><dd>{targets}</dd>
    <dt>Loops it touches</dt><dd>{loops}</dd>
    <dt>Where B4 appears twice</dt><dd>{chip("loop", "B4")} is a loop R-01 touches. {chip("loop", "R11")} runs through {chip("variable", "B4")}, {esc([n["title"] for n in r11["node_detail"] if n["id"] == "B4"][0])}. Typed chips keep the two apart on one card.</dd>
  </dl>
  <p class="src">{SRC_V7}; reforms.R-01.targets and loops; loops.R11.chain.</p>
</div>'''


def section_chips():
    coll = DATA["collisions"]
    v7_near = [m for m in coll["near"] if len({k for k, _ in m["members"] if k != "v5_standards_rule"}) > 1]
    exact_v7 = [x for x, kinds in coll["exact"] if "v5_standards_rule" not in kinds]
    pc = coll["prefix_candidates"]
    return f'''
<section id="m3">
  <p class="eyebrow">Mark 3</p>
  <h2>3. Typed ID chips</h2>
  <p>V7's codes collide, and V7 says so: “{esc(Q["methods_identifiers"])}” Its renderer adds the type word only when a code is identical across kinds, which covers {", ".join(exact_v7)}. The script compared every V7 namespace and found {len(v7_near)} codes that match another kind once a hyphen or a leading zero is set aside, such as Loop R1 and Reform R-01, Variable D1 and Domain D01, Variable X1 and Issue X01. V5's Standards chapter adds a third R list, rules R1 to R10. The chip below types every code, every time.</p>

  <div class="opt">
    <div class="opthead">{tag("Original")}<h3>Bare chips, as in Concept 08 Loop Field Guide</h3></div>
    {surfaces(bare_cell, gray=False)}
  </div>
  <div class="opt">
    <div class="opthead">{tag("Option")}<h3>A. V7's renderer: quiet code, colon, name</h3></div>
    <p>Clear in running text. The type word appears only for B2 to B5, so “R1” and “R-01” stay bare.</p>
    {surfaces(v7style_cell, gray=False)}
  </div>
  <div class="opt rec-opt">
    <div class="opthead">{tag("Option")}{tag("Recommended")}<h3>B. Two-part chip: type word in an ink cell, code in an outlined cell</h3></div>
    <p>Type word: Inter 600, 13 px, uppercase with 0.06 em tracking (the token value), set in the surface color on an ink fill. Code: Inter 700, 14 px, tabular figures, in ink inside a 1.5 px outline. Chip height 26 px, so a chip that links meets the 24 px target size. The measured contrast under each cell comes from the WCAG formula on the locked hex values; the rendered check at the end of the board confirms it on the page.</p>
    {surfaces(chips_collision_cell)}
  </div>
  <div class="opt">
    <div class="opthead">{tag("Option")}<h3>Compact chips, for tight spaces such as map labels</h3></div>
    {surfaces(chips_compact_cell)}
  </div>

  {kinds_table()}
  {near_table()}
  <div class="ex2">{r01_card()}
    <div class="panel s-newsprint"><p class="eyebrow">Guide rule IDs</p>
      <p>V5 numbers its Standards rules R1 to R10, the same codes as loops R1 to R10. The architecture map gives every guide rule a home rule ID in the form Rule NN.n, chapter then rule: V5's R1, “{esc(DATA["v5_standards_rules"]["R1"].rstrip("."))}”, becomes Rule 05.1. The form starts with a digit, and the script found {len(DATA["collisions"]["digit_led_ids"])} V7 IDs that do, so it cannot collide. The chip uses the type word Rule and the code 05.1. Std-01, which an earlier draft of this board proposed, is held back pending Dustin's ruling on the map's scheme.</p>
      <p>{chip("standard", "05.1")}</p>
    </div>
  </div>
  <div class="rec"><p class="eyebrow">Recommendation</p>
    <p><b>Option B on every surface: the two-part chip with the full type word, and the compact word only where space forces it.</b> Inside a diagram, a code may sit bare where the mark states its kind (a code in a variable box, a code in a connection label on its line) and the key says so. Loops and reforms always carry their type word, in diagrams too. Cite guide rules as Rule NN.n, as the architecture map proposes, and hold Std-01. Use “Domain” for D01 to D10; V7's renderer says “Issue area”, which the V7.1 list asks the atlas editor to settle.</p>
  </div>
</section>'''


# ======================================================================= section 4: effects
FAMS = ["DQ", "GE", "EP", "EQ"]


def fx_word(v):
    w = FX["words"].get(v)
    if w:
        return w[0].upper() + w[1:]
    out = re.sub(r"(?<![\w$])([+\-](?:S|M|L)|0|\?)(?![\w,])", lambda m: FX["words"][m.group(1)], v)
    return out[0].upper() + out[1:]


def fx_cell(mode, rid="R-01", fams=None):
    ex = FX["examples"][rid]
    fams = fams or FAMS

    def cell(s):
        out = []
        for f in fams:
            v = ex["effects"][f]
            name = FX["families"][f]
            if mode == "words":
                mark = f'<span class="fxw">{esc(fx_word(v) or tm(v))}</span>'
            elif mode == "pips":
                mark = M.pips(ex["parsed"][f], 120)
            else:
                mark = M.width_strand(v, 96)
            out.append(f'<div class="fxr"><span class="fxn">{esc(name)}</span>{mark}</div>')
        return "".join(out)
    return cell


def fx_cost_cell(mode):
    def cell(s):
        out = []
        for rid, f in [("R-12", "DQ"), ("R-28", "EP")]:
            v = FX["examples"][rid]["effects"][f]
            if mode == "words":
                mark = f'<span class="fxw">{esc(tm(v))}</span>'
            elif mode == "pips":
                mark = M.pips(FX["examples"][rid]["parsed"][f], 120)
            else:
                mark = '<span class="fxw">no width for a cost</span>'
            out.append(f'<div class="fxr"><span class="fxn">{rid} {esc(FX["families"][f])}</span>{mark}</div>')
        return "".join(out)
    return cell


def fx_table():
    rows = []
    for rid in ["R-01", "R-12", "R-07", "R-28", "R-06", "R-20", "R-29", "R-25"]:
        ex = FX["examples"][rid]
        first = True
        for f in FAMS:
            v = ex["effects"][f]
            p = ex["parsed"][f]
            words = fx_word(v)
            rows.append("<tr>" + (f'<td rowspan="4">{chip("reform", rid)}<br><span class="cap">{esc(ex["title"])}</span></td>' if first else "")
                        + f'<td>{esc(FX["families"][f])}</td><td class="pipcell">{M.pips(p, 120)}</td><td><span class="code">{esc(tm(v))}</span></td><td>{esc(words)}</td>'
                        + (f'<td rowspan="4">{esc(ex["effects_confidence"])}<br><span class="cap">Remedy grade: {esc(M.GRADE_WORD[ex["remedy_grade"]])}</span></td>' if first else "")
                        + "</tr>")
            first = False
    return ('<div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="eq fx"><caption>Effects of eight V7 reforms, drawn with the recommended mark. No row or column is totaled.</caption>'
            '<thead><tr><th>Reform</th><th>Outcome family</th><th>Mark</th><th>V7 value, verbatim</th><th>Words</th><th>Separate properties: confidence and remedy grade</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def section_effects():
    costs = FX["costs_live"]
    return f'''
<section id="m4">
  <p class="eyebrow">Mark 4</p>
  <h2>4. The ordinal effect mark</h2>
  <p>V7 gives each reform an expected effect on four outcome families in seven ordinal codes: {", ".join(tm(c) for c in ["+L", "+M", "+S", "0", "-S", "-M", "?"])}. Of the {FX["total"]} values, {FX["plain"]} use a plain code and {FX["qualified"]} add a qualifier or a range, such as R-06's “+L local” or R-28's “0 to {MINUS}S”. {len(costs)} values on live reforms carry a cost. V7 explains why it never adds them: “{esc(Q["outcomes_why_not_one_number"])}” Concept 10 draws the codes as strand widths in a 1 to 2 to 3 ratio and draws gains only. Concept 11 fills cells by thirds and drops the qualifiers.</p>

  <div class="opt">
    <div class="opthead">{tag("Option")}<h3>A. Words</h3></div>
    <p>V7's own words for each code. Exact and accessible; slow to scan across 50 reforms.</p>
    {surfaces(fx_cell("words"))}
    {surfaces(fx_cost_cell("words"), gray=False)}
  </div>
  <div class="opt rec-opt">
    <div class="opthead">{tag("Option")}{tag("Recommended")}<h3>B. One to three pips with a sign, costs left of zero</h3></div>
    <p>Each family has its own row and its own zero line. Gains run right with a plus sign, costs run left with a minus sign, so a reform that may help and harm the same family shows both in one row. A filled pip is a code V7 states. A ring is the far end of a range V7 states. A bar on the zero line is “no expected effect”; a question mark is “direction uncertain”. The words sit beside the pips and quote V7 in full when it adds a qualifier.</p>
    {surfaces(fx_cell("pips"))}
    {surfaces(fx_cost_cell("pips"), gray=False)}
  </div>
  <div class="opt">
    <div class="opthead">{tag("Option")}<h3>C. Width with an ordinal key, as in Concept 10</h3></div>
    <p>Widths 1.3, 2.6 and 3.9 px for small, moderate and large. A key can say “ordinal categories with no measured size”, and the eye still reads width as amount. Bundled into a Sankey, strands add up, which turns four codes into a total V7 says it never makes. Width also has no side for a cost.</p>
    {surfaces(fx_cell("width"))}
  </div>

  <h3 class="exh">Real example: Reform R-01, with seven reforms that carry costs or qualifiers</h3>
  {fx_table()}
  <div class="rec"><p class="eyebrow">Recommendation</p>
    <p><b>Option B with V7's words beside it.</b> The words quote V7's full value wherever it adds a qualifier. Costs share the row with gains. Never total a reform, a family or a route. Keep confidence (<span class="code">effects_confidence</span>) and the remedy grade as separate lines on the card, so effect size, uncertainty and evidence stay three properties. Retire width for effects (brief tension 13).</p>
  </div>
</section>'''


# ======================================================================= section 5: events
FAMILIES = ["Ballot measure", "Statute or local law", "Court ruling", "Executive or agency action"]


def ev_key_cell(s):
    out = []
    for f in FAMILIES:
        out.append(f'<div class="ek">{M.glyph_svg(f)}<span>{esc(f)}</span></div>')
    out.append(f'<div class="ek">{M.glyph_svg("Ballot measure", True)}<span>Pending: outline only</span></div>')
    return "".join(out)


def ev_chip_cell(s):
    rows = [r for r in DATA["repair"]["rows"] if r["id"] in ("RL64", "RL30")]
    out = []
    for r in rows:
        out.append(f'<div class="evchip">{M.glyph_svg(r["family"], r["direction"] == "pending")}<span><b>{esc(r["id"])}</b> · {esc(M.DIR_LABEL[r["direction"]])}<br>'
                   f'{esc(r["instrument"].capitalize())} · {esc(r["jurisdiction"])} · {esc(date_long(r["date"]))}</span></div>')
    return "".join(out)


def section_events():
    rep = DATA["repair"]
    rows10 = [r for r in rep["rows"] if r["loop"] == "R10"]
    rowsb4 = [r for r in rep["rows"] if r["loop"] == "B4"]
    dl = sorted(DATA["delivery"]["rows"], key=lambda r: r["period"]["start"])
    snap = DATA["generated"]["snapshot"]
    t10n = M.timeline(rows10, 2016, 2027, 326, 92, 2, "Rule changes recorded on Loop R10, 2016 to 2026")
    t10w = M.timeline(rows10, 2016, 2027, 900, 170, 1, "Rule changes recorded on Loop R10, 2016 to 2026")
    tb4n = M.timeline(rowsb4, 2016, 2027, 326, 92, 2, "Rule changes recorded on Loop B4, 2016 to 2026")
    tb4w = M.timeline(rowsb4, 2016, 2027, 900, 170, 1, "Rule changes recorded on Loop B4, 2016 to 2026")
    dln = M.spans(dl, 1930, 2030, 326, 0, 20, snap, "Delivery log periods", stacked=True)
    dlw = M.spans(dl, 1930, 2030, 1000, 220, 10, snap, "Delivery log periods", grade_col=110)
    fams = rep["family_counts"]
    instr_lines = "; ".join(f"{k} {v}" for k, v in rep["instrument_counts"].items())
    tbl = "".join(f'<tr><td>{chip("delivery", r["id"])}</td><td>{esc(r["date"])}</td><td>{esc(r["period"]["kind"])}, {esc(r["period"]["precision"])}</td>'
                  f'<td>{esc(r["period"]["start"])}</td><td>{esc(r["period"]["end"] or "none")}</td><td>{esc(M.GRADE_WORD[r["grade"]])}</td><td>{esc(r["what"][:110])}{"…" if len(r["what"]) > 110 else ""}</td></tr>' for r in dl)
    ev_rows = "".join(f'<tr><td>{chip("rule change", r["id"])}</td><td>{esc(r["date"])}</td><td>{esc(r["jurisdiction"])}</td><td>{esc(M.DIR_LABEL[r["direction"]])}</td><td>{esc(r["instrument"])}</td><td>{chip("loop", r["loop"])}</td></tr>' for r in rows10 + rowsb4)
    return f'''
<section id="m5">
  <p class="eyebrow">Mark 5</p>
  <h2>5. The event mark</h2>
  <p>The repair log records {len(rep["rows"])} dated rule changes and the delivery log {len(DATA["delivery"]["rows"])} measured results. Both are documented events. They sit on a time axis and keep away from the causal grammar: no arrowheads, no variable boxes, no grade textures. Direction gets a row with V7's own words ({", ".join(f"{M.DIR_LABEL[k].lower()} {v}" for k, v in rep["direction_counts"].items())}). Instrument gets a shape, grouped into four families from V7's {len(rep["instrument_counts"])} instrument values ({esc(instr_lines)}). The exact V7 instrument stays in the label and the table. Events on the same day stack upward in their row, so a count stays visible. No color is used, so the mark makes no red and blue pairing. V7's coding note: “{esc(Q["repair_coding_last"])}”</p>

  <div class="opt rec-opt">
    <div class="opthead">{tag("Option")}{tag("Recommended")}<h3>The mark: a shape per instrument family, placed in its direction row</h3></div>
    {surfaces(ev_key_cell)}
    <p>As a chip outside a timeline, the mark carries its direction in words:</p>
    {surfaces(ev_chip_cell, gray=False)}
  </div>

  <h3 class="exh">Real example: rule changes on Loop R10 and Loop B4</h3>
  <p class="cap">True size. The phone version is drawn for 326 px; the wide version appears at 1100 px and wider.</p>
  <div class="ex2 tl">
    {figure('<div class="narrow">' + t10n + '</div><div class="wide">' + t10w + '</div>',
            f'{len(rows10)} rule changes that V7 ties to Loop R10, Safe seats shift accountability to small primary electorates. The column of {sum(1 for r in rows10 if r["date"] == "2024-11-05" and r["direction"] == "voters kept existing rules")} ballot measures on November 5, 2024 is the day voters in several states kept their existing primary rules. The two outlined marks are the Alaska and Massachusetts measures on the November 3, 2026 ballot, pending.',
            SRC_V7 + "; repairLog.rows where loop is R10. Hover a mark for its ID.", "fig s-newsprint wide-fig")}
    {figure('<div class="narrow">' + tb4n + '</div><div class="wide">' + tb4w + '</div>',
            f'{len(rowsb4)} rule changes that V7 ties to Loop B4, Electoral consequences can improve public performance.',
            SRC_V7 + "; repairLog.rows where loop is B4.", "fig s-newsprint wide-fig")}
  </div>
  <div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="eq"><caption>Table equivalent of the two timelines</caption><thead><tr><th>Record</th><th>Date</th><th>Jurisdiction</th><th>Direction</th><th>V7 instrument</th><th>Loop</th></tr></thead><tbody>{ev_rows}</tbody></table></div>

  <h3 class="exh">Periods: the delivery log</h3>
  <p>Delivery log dates are text, and V7 lists the cases out of time order. The rule below turns every one of the {len(dl)} date strings into a span or a point; the script parsed all of them ({len(DATA["delivery"]["unparsed"])} left over).</p>
  <ol class="rule">
    <li>Print V7's date text verbatim beside the mark.</li>
    <li>Sort and place a period by its start: “1935-1955” sorts at 1935 and runs to the end of 1955.</li>
    <li>A year-only period runs from the start of its first year to the end of its last. A month period runs from the first to the last day of its months.</li>
    <li>A federal fiscal year runs on the federal calendar: “FY2024” is October 1, 2023 to September 30, 2024.</li>
    <li>An open period (“1945-01-25 onward”) runs to the snapshot date, {date_long(snap)}, with a notch at its end and the word onward in its label.</li>
    <li>A date that marks an analysis or a publication (“2024 analysis”, “published 2012”) is a point, drawn as an open square, and never stretches a span.</li>
    <li>Never add precision V7 does not state: a year-only date gets no month or day.</li>
  </ol>
  {figure('<div class="narrow">' + dln + '</div><div class="wide">' + dlw + '</div>',
          f'All {len(dl)} delivery cases, sorted by start. Bars are periods; open squares are analysis and publication dates; the hairline is the snapshot date. The grade is the grade V7 gives the measured result: “{esc(Q["delivery_grade_note"])}”',
          SRC_V7 + "; deliveryLog.rows[].date, parsed by the period rule.", "fig s-newsprint wide-fig")}
  <details><summary>Table equivalent of the delivery log chart</summary>
  <div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="eq"><thead><tr><th>Case</th><th>V7 date text</th><th>Read as</th><th>Start</th><th>End</th><th>Grade</th><th>What was done (V7, shortened)</th></tr></thead><tbody>{tbl}</tbody></table></div></details>

  <div class="opt">
    <div class="opthead">{tag("Misuse")}<h3>An event drawn as a cause</h3></div>
    <div class="ex2">
      <div class="fig s-newsprint">{M.svg(300, 70, M.ev_glyph("Ballot measure", 20, 35) + M.connection([(30, 35), (170, 35)], "documented") + M.vbox(172, 14, 120, 42, "C2", "Primary decisiveness"), "misuse")}</div>
      <p>An arrow from a rule change into a variable claims that the change moved the variable. The repair log records that the change happened. When a row names a loop, show the loop as a typed chip in the event's label, as the table above does.</p>
    </div>
  </div>
  <div class="rec"><p class="eyebrow">Recommendation</p>
    <p><b>Adopt the event mark and the period rule.</b> Shape for instrument family, row for direction in V7's words, outline for pending, stacking for events on the same day, and no arrowheads, boxes or grade textures. Delivery cases are bars for periods and open squares for points, with V7's date text beside them. Every figure that uses the event mark carries the shape key.</p>
  </div>
</section>'''


# ======================================================================= section 6: authority and delay
def auth_cell(mode):
    def cell(s):
        if mode == "v5":
            body = (M.connection([(4, 10), (100, 10)], "documented", head=False, width=1.5)
                    + '<path d="M92 4 L100 10 L92 16" fill="none" stroke="currentColor" stroke-width="1.5"/>')
            return M.svg(104, 20, body, "V5 authority") + '<p class="cap2">“sets”, “funds”, “appoints”</p>'
        if mode == "v7":
            body = M.connection([(4, 10), (100, 10)], "documented", width=1.8).replace("currentColor", "#3F6C64")
            _, p = M.pill(30, 0, "auth")
            return M.svg(104, 22, body + p.replace("currentColor", "#3F6C64"), "V7 authority") + '<p class="cap2">V7 teal #3F6C64</p>'
        body = M.connection([(4, 10), (100, 10)], "documented", kind="authority", width=1.5)
        return M.svg(104, 20, body, "authority") + '<p class="cap2">LE02 no sign · decides</p>'
    return cell


def authority_fig():
    auth = DATA["authority"]["links"]
    left = ["D1", "D2", "D4", "D6"]
    right = ["EC2", "TC5", "EC10", "TC7"]
    titles = {}
    for a in auth:
        titles[a["from"]] = a["from_title"]
        titles[a["to"]] = a["to_title"]
    W, bw, gap = 320, 126, 12

    def col(keys):
        pos, y = {}, 6
        for k in keys:
            n = len(M.wrap(titles[k], bw - 12, 13, 400))
            h = 24 + n * 15
            pos[k] = (y, h)
            y += h + gap
        return pos, y
    lp, lh = col(left)
    rp, rh = col(right)
    out = []
    order = {}
    for a in auth:
        order.setdefault(a["from"], []).append(a)
        order.setdefault("to:" + a["to"], []).append(a)
    for a in auth:
        fs, ts = order[a["from"]], order["to:" + a["to"]]
        fy = lp[a["from"]][0] + lp[a["from"]][1] * (fs.index(a) + 1) / (len(fs) + 1)
        ty = rp[a["to"]][0] + rp[a["to"]][1] * (ts.index(a) + 1) / (len(ts) + 1)
        out.append(M.connection([(bw + 4, fy), (W - bw - 4, ty)], a["evidence"], a["delay"], kind="authority", width=1.5))
    for k in left:
        out.append(_auth_box(4, lp[k][0], bw, lp[k][1], k, titles[k]))
    for k in right:
        out.append(_auth_box(W - bw - 4, rp[k][0], bw, rp[k][1], k, titles[k]))
    return M.svg(W, max(lh, rh), "".join(out), "Authority diagram: the seven authority connections in V7")


def _auth_box(x, y, w, h, code, title):
    lines = M.wrap(title, w - 12, 13, 400)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="bgf" stroke="currentColor" stroke-width="1.5"/>',
           M.T(x + 6, y + 16, code, "b")]
    for i, ln in enumerate(lines):
        out.append(M.T(x + 6, y + 32 + i * 15, ln))
    return "".join(out)


def misuse_auth():
    body = (M.vbox(10, 6, 120, 42, "D1", "Congress's capacity") + M.vbox(10, 110, 120, 42, "EC2", "Public investment")
            + M.connection([(70, 48), (70, 110)], "documented", kind="authority", width=1.5)
            + M.connection([(130, 131), (170, 131), (170, 27), (130, 27)], "plausible"))
    return M.svg(200, 160, body, "misuse: authority as a loop step")


def delay_cell(mode):
    def cell(s):
        out = []
        for d in ["S", "M", "L"]:
            if mode == "letters":
                _, p = M.pill(0, 1, f"L01 + · {d}")
                out.append(f'<div class="ls">{M.svg(96, 24, p, "delay letter", "mk inl")}</div>')
            elif mode == "words":
                out.append(f'<div class="ls"><span class="lw">{esc(M.DELAY_WORD[d])}</span>{M.line_specimen("documented", 104)}</div>')
            else:
                out.append(f'<div class="ls"><span class="lw">{esc(M.DELAY_WORD[d])}</span>{M.line_specimen("documented", 104, delay=d)}</div>')
        if mode == "ticks":
            out.append(f'<div class="ls"><span class="lw">On every texture</span>{M.line_specimen("contested", 104, delay="M")}{M.line_specimen("hypothesis", 104, delay="L")}</div>')
        return "".join(out)
    return cell


def section_authority_delay():
    auth = DATA["authority"]["links"]
    rows = "".join(f'<tr><td>{chip("connection", a["id"])}</td><td>{esc(a["from"])} to {esc(a["to"])}</td><td>no sign</td>'
                   f'<td>{esc(M.GRADE_WORD[a["evidence"]])}</td><td>{esc(M.DELAY_WORD[a["delay"]])}</td><td>{esc(a["name"])}</td></tr>' for a in auth)
    dl = DATA["delay"]
    r1 = LP["R1"]["link_detail"]
    return f'''
<section id="m6">
  <p class="eyebrow">Mark 6</p>
  <h2>6. The authority mark and the delay mark</h2>
  <h3 class="exh">Authority</h3>
  <p>V7: “{esc(Q["authority_glossary"])}” All {len(auth)} authority connections are documented, and {len(DATA["authority"]["in_loops"])} sit in a loop. The supplied files draw them three ways.</p>
  <div class="opt">
    <div class="opthead">{tag("Original")}<h3>V5 Polished and the Atlas Visual System: open arrowhead with a verb</h3></div>
    {surfaces(auth_cell("v5"), gray=False)}
  </div>
  <div class="opt">
    <div class="opthead">{tag("Original")}<h3>V7's renderer: a teal line and arrowhead, “auth” in the label</h3></div>
    <p>The arrowhead is the causal end mark, and teal gives Verdigris one more job.</p>
    {surfaces(auth_cell("v7"), gray=False)}
  </div>
  <div class="opt rec-opt">
    <div class="opthead">{tag("Option")}{tag("Recommended")}<h3>Open diamond at the decided end, in ink, with “no sign” in the label</h3></div>
    <p>From Concepts V2 (“decides, no direction”). The diamond cannot be read as an arrowhead, the label replaces the sign with the words “no sign”, and the V7 name supplies the verb. Grade texture and delay ticks still apply.</p>
    {surfaces(auth_cell("rec"))}
  </div>
  <div class="ex2">
    {figure(authority_fig(), "The authority diagram (brief worked example 5): every authority connection in V7. Bodies that hold the power sit on the left; what they decide sits on the right. Two ticks mark the two connections with a delay of 2 to 10 years.", SRC_V7 + "; links where type is authority.")}
    <div class="fig s-newsprint"><div class="opthead">{tag("Misuse")}</div>{misuse_auth()}<p class="cap">An authority connection drawn as one step of a ring. V7 says authority “never closes a loop”, so a key that allows this is wrong. Drawn for this board from two V7 variables; no such loop exists in V7.</p></div>
  </div>
  <div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="eq"><caption>Table equivalent of the authority diagram</caption><thead><tr><th>Connection</th><th>From, to</th><th>Sign</th><th>Grade</th><th>Delay</th><th>V7 name</th></tr></thead><tbody>{rows}</tbody></table></div>

  <h3 class="exh">Delay</h3>
  <p>V7: “{esc(dl["definition"])}” Across the 118 connections: S {dl["counts"].get("S")}, M {dl["counts"].get("M")}, L {dl["counts"].get("L")}. The same three letters size reform effects (+S, +M, +L), so a bare letter near an effect code can be misread. V7 gives each loop the delay of its slowest step; the script confirmed this for all {len(dl["loop_delay_rule"])} loops with numbered steps.</p>
  <div class="opt">
    <div class="opthead">{tag("Original")}<h3>V7's letters in the label</h3></div>
    {surfaces(delay_cell("letters"), gray=False)}
  </div>
  <div class="opt">
    <div class="opthead">{tag("Option")}<h3>A. Words only</h3></div>
    {surfaces(delay_cell("words"), gray=False)}
  </div>
  <div class="opt rec-opt">
    <div class="opthead">{tag("Option")}{tag("Recommended")}<h3>B. Ticks on the line, words in the label</h3></div>
    <p>One, two or three 1.5 px ticks across the start of the line, 10 px long and 5 px apart, so they read on every texture. The label spells the delay out.</p>
    {surfaces(delay_cell("ticks"))}
  </div>
  <p>Loop R1 carries all three delays: {", ".join(f'{l["id"]} {M.DELAY_WORD[l["delay"]]}' for l in r1)}. V7 gives the loop delay {esc(LP["R1"]["delay"])}, its slowest step. The R1 figure in Mark 1 draws the ticks.</p>
  <div class="rec"><p class="eyebrow">Recommendation</p>
    <p><b>Authority: the open diamond in ink with “no sign” in the label.</b> Authority lines stay outside loop rings and are never numbered as loop steps. <b>Delay: ticks on the line and words in the label.</b> A bare S, M or L appears only in a data table under the heading “Delay code”.</p>
  </div>
</section>'''


# ======================================================================= section 7: hinge
AMP_PATH = ("M261 -16Q218 -16 175.5 -5.0Q133 6 98.5 28.5Q64 51 43.5 86.0Q23 121 23 170Q23 237 67.5 288.5Q112 340 179 365Q143 404 125.5 436.0Q108 468 102.5 496.0Q97 524 97 551Q98 627 150.0 671.5Q202 716 288 716Q341 716 380.0 694.0Q419 672 440.5 636.5Q462 601 462 559Q462 518 441.5 481.5Q421 445 388.0 415.5Q355 386 318 364Q322 360 346.0 335.0Q370 310 406.0 275.0Q442 240 480 205Q483 217 484.0 229.5Q485 242 485 255Q485 283 479.0 299.0Q473 315 461.5 322.5Q450 330 432 331V395H600V320L545 323Q550 311 553.0 295.5Q556 280 556 262Q556 233 551.0 206.0Q546 179 537 154Q541 151 544.5 147.5Q548 144 552 141Q591 108 623.0 87.0Q655 66 675 66V0H568Q560 0 532.5 15.0Q505 30 470 57Q431 23 378.0 3.5Q325 -16 261 -16ZM293 55Q331 55 362.5 67.5Q394 80 418 102Q405 113 393.0 124.5Q381 136 368 147Q310 200 274.5 236.5Q239 273 208 308Q189 293 178.5 272.0Q168 251 163.5 230.5Q159 210 159 195Q159 150 175.0 118.5Q191 87 221.0 71.0Q251 55 293 55ZM273 417Q311 446 330.0 489.5Q349 533 349 564Q349 600 331.5 623.0Q314 646 283 646Q255 646 235.5 623.0Q216 600 216 556Q216 526 232.5 486.5Q249 447 273 417Z")


def amp(x, y, h, red=True, fill=None):
    s = h / 100.61
    fill = fill or ("#E63946" if red else "currentColor")
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})"><path d="{AMP_PATH}" fill="{fill}" '
            f'transform="translate(-3.16 98.41) scale(0.14 -0.14)"/></g>')


def _chev(p2, p3, size=7):
    import math
    dx, dy = p3[0] - p2[0], p3[1] - p2[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    pts = []
    for ang in (0.5, -0.5):
        ca, sa = math.cos(ang), math.sin(ang)
        bx, by = -(ux * ca - uy * sa), -(ux * sa + uy * ca)
        pts.append((p3[0] + bx * size, p3[1] + by * size))
    return (f'<path d="M{pts[0][0]:.1f} {pts[0][1]:.1f} L{p3[0]:.1f} {p3[1]:.1f} L{pts[1][0]:.1f} {pts[1][1]:.1f}" '
            f'fill="none" stroke="currentColor" stroke-width="1.25" stroke-linejoin="round" stroke-linecap="round"/>')


def hinge_primer(W=280, arcs="solid", red=True, amp_fill=None):
    """Studio sketch of the hinge diagram as a loop primer. Words only: no IDs, signs, grades or delays."""
    cx, cy = W / 2, 112
    dash = ' stroke-dasharray="1 6" stroke-linecap="round"' if arcs == "v5" else (' stroke-dasharray="6 5"' if arcs == "mock" else "")
    # clockwise: the top arc runs from OATH to ACTION, the bottom arc returns from ACTION to OATH
    t1 = ((cx - 50, cy - 44), (cx - 28, cy - 84), (cx + 28, cy - 84), (cx + 50, cy - 44))
    t2 = ((cx + 50, cy + 44), (cx + 28, cy + 84), (cx - 28, cy + 84), (cx - 50, cy + 44))

    def arc(t):
        return (f'<path d="M{t[0][0]} {t[0][1]} C{t[1][0]} {t[1][1]} {t[2][0]} {t[2][1]} {t[3][0]} {t[3][1]}" '
                f'fill="none" stroke="currentColor" stroke-width="1.25"{dash}/>' + _chev(t[2], t[3]))
    out = [
        f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="currentColor" stroke-width="1"/>',
        amp(cx - 22, cy - 24, 48, red, amp_fill),
        f'<line x1="{cx - 34}" y1="{cy}" x2="{cx - 58}" y2="{cy}" stroke="currentColor" stroke-width="1"/>',
        f'<line x1="{cx + 34}" y1="{cy}" x2="{cx + 58}" y2="{cy}" stroke="currentColor" stroke-width="1"/>',
        f'<circle cx="{cx - 58}" cy="{cy}" r="3.5" fill="currentColor"/><circle cx="{cx + 58}" cy="{cy}" r="3.5" fill="currentColor"/>',
        M.T(cx - 64, cy + 6, "OATH", "hw", anchor="end"), M.T(cx + 64, cy + 6, "ACTION", "hw"),
        M.T(cx - 64, cy + 24, "UNDERSTAND", "lbl", anchor="end"), M.T(cx + 64, cy + 24, "IMPACT", "lbl"),
        arc(t1), arc(t2),
        M.T(cx, cy - 86, "The promise becomes action", "ink2", anchor="middle"),
        M.T(cx, cy + 100, "The result shapes the next promise", "ink2", anchor="middle"),
    ]
    return M.svg(W, 224, "".join(out), "Hinge diagram sketch: a promise, then action, and the result returns")


HINGE_READY = ROOT / "work/handoffs/phase-1/20261021_Hinge-V2-Ready.md"


def red_rule_d126():
    """Rule 05.3, the red rule, word for word from decision D1-26 in the decision log."""
    log = next((ROOT / "work/ledger").glob("*_Decision-Log.md")).read_text(encoding="utf-8")
    row = [ln for ln in log.splitlines() if ln.startswith("| D1-26 |")][0]
    return re.search(r'every board: "(.*)" \|', row).group(1)


RED_RULE_0503 = red_rule_d126()


def hinge_v2_path(which="Compact"):
    """The V2 master (Display or Compact) named in the identity agent's ready note, or None."""
    if not HINGE_READY.exists():
        return None
    for c in re.findall(r"[\w./-]+\.svg", HINGE_READY.read_text(encoding="utf-8")):
        path = ROOT / c.lstrip("./")
        if path.exists() and which in path.name:
            return path
    return None


def hinge_v2_pair(surface="Newsprint"):
    """Display master at 560 px where the view is 700 px or wider, compact master at 280 px below that,
    as the identity board's minimum sizes require (display from 526 px, compact from 241 px)."""
    return (f'<div class="hdisp">{hinge_v2_inline(560, surface, "Display")}</div>'
            f'<div class="hcomp">{hinge_v2_inline(280, surface, "Compact")}</div>')


def hinge_v2_inline(W, surface="Newsprint", which="Compact"):
    path = hinge_v2_path(which)
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml[^>]*>", "", svg).strip()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    H = W * vb[3] / vb[2]
    amp_c = "#FFFFFF" if surface == "Prussian" else "#E63946"
    line_c = "#5D636D" if surface in ("Newsprint", "White") else "#DCD9D2"
    svg = svg.replace("<svg ", f'<svg class="mk" width="{W:.0f}" height="{H:.1f}" role="img" aria-label="Hinge diagram V2" style="--amp:{amp_c};--line:{line_c}" ', 1)
    cap_top = '<p class="harc">The promise becomes action</p>'
    cap_bot = '<p class="harc">The result shapes the next promise</p>'
    return cap_top + svg + cap_bot


def hinge_v2_block():
    """Reuse the identity board's hinge diagram V2 when its ready note exists; otherwise show a marked placeholder."""
    head = f'<div class="opthead">{tag("Option")}{tag("Recommended")}<h3>Hinge diagram V2, from the identity board, as the primer\'s first step</h3></div>'
    path = hinge_v2_path()
    if path:
        rel = path.relative_to(ROOT)
        disp = hinge_v2_path("Display").relative_to(ROOT)
        return (head + f'<div class="s-newsprint pad hv2">{hinge_v2_pair()}</div>'
                + f'<p class="cap">The identity board\'s hinge diagram V2, drawn inline from <span class="code">{esc(str(disp))}</span> at 560 px (minimum 526 px) and, in views under 700 px, from <span class="code">{esc(str(rel))}</span> at 280 px (minimum 241 px). Solid hairline arcs, clockwise, with V5\'s labels UNDERSTAND and IMPACT on the display master; the compact master drops them. The arc captions are this board\'s.</p>'), True
    return (head + '<div class="s-newsprint pad placeholder"><p><b>Placeholder.</b> The identity board\'s hinge diagram V2 goes here, from the path the identity agent writes to <span class="code">work/handoffs/phase-1/20261021_Hinge-V2-Ready.md</span>. That file did not exist when this board was built. The studio sketch below follows the same brief.</p>'
            + hinge_primer(300) + '</div>'), False


def section_hinge():
    b4 = LP["B4"]
    V2_BLOCK, _ = hinge_v2_block()
    return f'''
<section id="m7">
  <p class="eyebrow">Mark 7</p>
  <h2>7. The hinge in the systems grammar</h2>
  <p>Dustin's brief for the idea (DC-05): <q>I really like the Oath &amp; Action ampersand hinge concept. A promise or commitment, then acting. The ampersand runs through the brand. Problem and solution. Bridging the divide and/or finding common ground between the left and right, cause and effect, you and me.</q> His hinge mockup circles the ampersand with looping arrows. That turn is the shape of a feedback loop, so the hinge can be the first loop a newcomer meets. It has to stay a brand mark, though, and two current drawings use a data texture.</p>

  <div class="ex3">
    <div class="opt"><div class="opthead">{tag("Original")}<h3>V5 hinge master</h3></div>
      <div class="s-newsprint pad"><img src="{A}20261021_V5-Hinge-Master-Copy.svg" alt="V5 hinge master: the wordmark with a dotted arc from OATH to ACTION" width="300" height="88"></div>
      <p class="cap">The arc is dotted (1.25 px, dashes 1 6, round caps). In V7's grammar a dotted line is a hypothesis.</p></div>
    <div class="opt"><div class="opthead">{tag("Original")}<h3>Dustin's hinge mockup</h3></div>
      <div class="s-newsprint pad"><img src="../../source/brand-mockups/20261021_Mockup-Hinge-Diagram-Newsprint.webp" alt="Hinge diagram mockup on Newsprint" width="300" height="200"></div>
      <p class="cap">Generated reference image, shown for study. Both arcs are dashed; in V7's grammar a dash is plausible.</p></div>
    <div class="opt rec-opt span-all">{V2_BLOCK}</div>
  </div>
  <div class="widecells">{surfaces(lambda s: ('<div class="hv2">' + hinge_v2_pair(s) + '</div>') if hinge_v2_path() else hinge_primer(280, amp_fill="#FFFFFF" if s == "Prussian" else None), note="Hinge diagram V2 at true size on all four surfaces and in grayscale, clockwise, with V5's labels. The ampersand inside the hinge diagram is an identity mark, which Rule 05.3 does not count toward a view's working red. It is red on Newsprint, White and Charcoal (4.49:1 on Charcoal) and White on Prussian, because under Rule 05.3 red never sits on Prussian and identity marks there use White (treatment D).")}</div>

  <h3 class="exh">From the hinge to a real loop</h3>
  <ol class="steps">
    <li><b>The idea.</b> The hinge: a promise, then action, and the result comes back around to shape the next promise. Words only.</li>
    <li><b>One loop the atlas records.</b> {chip("loop", "B4")} {esc(b4["title"])}. Read it aloud: <i>worse service, more risk of losing office, more incumbents defeated or retired, better service from those who remain.</i> It is a balancing loop: it pushes back against the first change.</li>
    <li><b>Where loops meet.</b> {chip("variable", "C3")} Risk of losing office sits in {", ".join("Loop " + k for k in DATA["loops_through_C3"])}. Where seats are safe, {chip("loop", "R10")} wears down the pressure that B4 needs; V7's qualification for B4: “{esc(b4["qualification"].split(". ")[0])}.”</li>
  </ol>
  <div class="ex2">
    {figure(loop_head("B4") + loop_fig("B4"), "Loop B4 in the systems grammar: IDs, signs, grades, delays and a source line, which the hinge never carries. All three steps are well supported; V7's summary adds that for U.S. services the weakest is L54, “since its main study covers Brazilian mayors”.", SRC_V7 + "; loop B4, connections L23, L24, L54.")}
    {figure(loop_head("R10") + loop_fig("R10", rings={"links": R01["targets"], "nodes": [t for t in R01["targets"] if not t.startswith("L")]}),
            f'Loop R10 shares C3 with B4. The red rings mark where Reform R-01 acts: {", ".join(t["id"] for t in R01["target_detail"])}. Under Rule 05.3 the one working red in a systems figure marks where a reform acts, and “One job may take several marks, such as each target of one reform.”, so the three rings count as one red.',
            SRC_V7 + "; loop R10; reforms.R-01.targets.")}
  </div>
  {equivalent_table("B4")}

  <div class="panel rules s-newsprint">
    <p class="eyebrow">The rule that keeps a brand mark apart from a data mark</p>
    <ol>
      <li>The hinge carries words only. It never carries an ID, a sign, a grade, a delay or a count. Every loop drawn from the atlas carries all of them, with a key and a source line.</li>
      <li>The hinge never sits inside a figure that has a key, and a data figure never contains the ampersand.</li>
      <li>No brand graphic uses a dotted or dashed line, since V7 gives those textures to evidence grades. The hinge diagram's arcs are solid hairlines with open chevrons, and they run clockwise.</li>
      <li>Red follows Rule 05.3, the red rule: “{esc(RED_RULE_0503)}” Data graphics on Prussian keep the token table's Newsprint marks; identity marks on Prussian use White.</li>
      <li>“Hinge” stays a brand word. The atlas calls a shared variable a place where loops meet.</li>
    </ol>
  </div>
  <div class="rec"><p class="eyebrow">Recommendation</p>
    <p><b>Use the identity board's hinge diagram V2 (item 7: solid hairline arcs, clockwise, UNDERSTAND and IMPACT) as the first step of the three-step primer, and adopt the five rules.</b> The arcs are identity geometry, so they need your named approval at identity item 7. The primer reuses that drawing and adds no third hinge.</p>
  </div>
</section>'''


# ======================================================================= section 8: bases
BASES = [
    ("03", "Field Manual", "20261021_Concept-03-Field-Manual.jpg", "Confirm with changes",
     "The layered model as stacked plates, a title block with source and date, numbered callouts, and a magnified detail with IDs and grades.",
     "Draw the plumb lines with each connection's grade texture, or as plain hairlines with a key: dotted means hypothesis, and none of the 31 is one. Label what each plate shows. Build the Prussian surface from dark-surface tokens with measured contrast. Drop “Concept 03 of 06”.",
     "The layer overview: covers, report openers and the atlas page that explains how the model is built."),
    ("09", "The Circuit", "20261021_Concept-09-Circuit.jpg", "Confirm with changes",
     "The whole model in reading order, every crossing counted, the five V7 areas as cards listing variables by ID, authority wires ending in diamonds, an explicit return line.",
     "Let a reader light one loop at a time. Print signs in wire labels. Give color one job. Keep a static printable state with a table equivalent, so hover is never the only route. Say “back to area A, Economic structure”.",
     "The whole-system map behind the atlas home page and the systems chapter."),
    ("10", "Who Can Act", "20261021_Concept-10-Who-Can-Act.jpg", "Revise",
     "V7's eleven routes with their actors, every count, a separate result per outcome family, and the note that strand counts carry “no judgment about which route matters most”.",
     "Replace strand width with the pips and words of Mark 4. Draw costs. Show all four feasibility levels and the route check dates, or “no check date in V7”. Restore qualifiers. Add a filtered view for one reform so strands stay legible at 390 px.",
     "The “what can I do” page and the source for the configurable policy tracker."),
    ("11", "Register", "20261021_Concept-11-Register.jpg", "Confirm with changes",
     "The most faithful file: 118 connections filed once, 51 variable cards with type and what a higher value means, reform rows with routes and effects, sheet counts that add up, and a matrix of how sheets connect.",
     "Typed chips. Text at 13 px or more. Keys in V7's grade order with the record square for documented. Pips with qualifiers in text. A size key on the matrix. Brand tokens for its grays.",
     "The evidence view, and the table equivalent behind every systems graphic."),
    ("07 + 04", "Loop Card with the Broadsheet record panel", "20261021_Concept-07-Loop-Card.jpg", "Add as a fifth base",
     "Concept 07 gives one loop a full page: variable cards with “a higher value means”, arrows that say raises or lowers, grade and delay in words, where a reform enters, who can act and the expected effects. Concept 04 adds the panel that sets “What the record shows” beside “This part still needs an answer”.",
     "A short version for two-step loops such as R8 and a long one for four-step loops such as R10. Typed chips, pips for effects, route check dates, and both ballot measures named where R-01 appears.",
     "The loop page: the template for brief worked examples 1, 2, 3, 4 and 6."),
]


def section_bases():
    cards = []
    for num, name, img, verdict, keep, change, becomes in BASES:
        extra = (f'<img src="{A}20261021_Concept-04-Broadsheet.jpg" alt="Concept 04 Broadsheet">' if num.startswith("07") else "")
        cards.append(f'''<article class="base">
  <div class="opthead">{tag(verdict)}<h3>Concept {esc(num)} · {esc(name)}</h3></div>
  <img src="{A}{img}" alt="Concept {esc(num)} {esc(name)}, Concepts V2, captured at 1440 px">{extra}
  <dl><dt>Keep</dt><dd>{esc(keep)}</dd><dt>Change</dt><dd>{esc(change)}</dd><dt>In V6</dt><dd><b>{esc(becomes)}</b></dd></dl>
</article>''')
    return f'''
<section id="m8">
  <p class="eyebrow">Mark 8</p>
  <h2>8. The atlas bases</h2>
  <p>Dustin's saved screenshots favor Concepts 03, 09, 10 and 11. Together they cover layers, the whole map, actors and evidence. None gives one loop its own page, and five of the brief's six worked examples are loop or intervention pages, so the fifth base is Concept 07 with Concept 04's record panel. Thumbnails are Phase 0 captures of Concepts V2 at 1440 px, scaled down for review.</p>
  <div class="bases">{"".join(cards)}</div>
  <div class="rec"><p class="eyebrow">Recommendation</p>
    <p><b>Confirm 03, 09 and 11 with the changes listed, revise 10, and add 07 with 04's record panel as the fifth base.</b> All five take the marks on this board, so the atlas and the guide share one grammar.</p>
  </div>
</section>'''


# ======================================================================= checks and decisions
def section_checks():
    if not CHECK:
        body = "<p>The rendered checks have not run yet. Run <span class=\"code\">node work/build/scripts/phase-1/check_systems_board.js</span>.</p>"
    else:
        items = "".join(f"<li>{esc(x)}</li>" for x in CHECK.get("summary", []))
        nots = "".join(f"<li>{esc(x)}</li>" for x in CHECK.get("not_checked", []))
        body = f"<h3>Checked on the rendered page</h3><ul>{items}</ul><h3>Not checked</h3><ul>{nots}</ul>"
    return f'''
<section id="checks">
  <p class="eyebrow">Checks</p>
  <h2>How this board was checked</h2>
  <p>Values: every V7 value on this board comes from <span class="code">work/build/scripts/phase-1/systems_marks_data.py</span>, which writes <span class="code">{A}20261021_Systems-Marks-Data.json</span>. The board is generated from that file by <span class="code">build_systems_marks_board.py</span>. Rendering: <span class="code">check_systems_board.js</span> renders the board in Chromium at 1440 and 390 px.</p>
  {body}
</section>'''


DECISIONS = [
    ("Evidence line code", "V7's code; V5's dash rule; a weight ramp", "V7's code, plus the record square on documented labels and the hollow line for conceptual steps", "It matches the model and survives grayscale; the square tells documented from well supported in print."),
    ("Grade words", "V7's labels; Concepts V2's plain words; hybrid", "Hybrid: V7's word with a plain gloss, documented first", "Readers meet the same words in the atlas, and the gloss carries the plain meaning."),
    ("Typed ID chips and guide rule IDs", "Bare codes; V7's colon style; two-part chip. Rule NN.n or Std-01", "Two-part chip with the full type word everywhere; guide rules cited as Rule NN.n, as the architecture map proposes; Std-01 held", "It solves all the collisions the script found, at 13 px and above with at least 9.42:1, and one rule set keeps one ID system."),
    ("Ordinal effect mark", "Words; pips with a sign; width with a key", "Pips with a sign, costs left of zero, V7's words beside them", "Countable, never summed, and it keeps costs and qualifiers on the graphic."),
    ("Event mark and period rule", "Adopt; revise", "Adopt: shape for instrument, row for direction, outline for pending, the seven-step period rule", "Events stay visibly apart from causal findings and every V7 date string parses."),
    ("Authority mark", "Open arrowhead; V7 teal line; open diamond", "Open diamond in ink with “no sign” in the label", "It cannot be read as a causal arrow and adds no color job."),
    ("Delay mark", "Letters; words; ticks with words", "Ticks on the line, words in the label", "S, M and L also size effects, so letters stay in data tables only."),
    ("The hinge diagram (I6)", "V5's dotted arc; two-way dashed arcs; V2 with solid arcs; V2 without the return arc", "V2 with solid arcs, running clockwise, with the five separation rules; the primer reuses it as its first step", "A dotted or dashed hinge reads as a hypothesis or a plausible link once a reader learns the key."),
    ("Atlas bases", "Confirm, revise or drop each", "Confirm 03, 09, 11; revise 10; add 07 with 04's record panel", "Covers layers, the whole map, actors, evidence and single loops."),
    ("Atlas V7.1 issue list", "Send to the atlas editor; hold", "Send it as written", "Every item has a JSON location, evidence and a fix, and V6 works around each one meanwhile."),
]


def section_decisions():
    rows = "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td><td><b>{esc(c)}</b></td><td>{esc(d)}</td></tr>" for a, b, c, d in DECISIONS)
    return f'''
<section id="decisions">
  <div class="decision">
    <p class="eyebrow">Decisions for Gate 1</p>
    <h2>Systems marks: what you decide</h2>
    <div class="wrap" tabindex="0" role="region" aria-label="Scrollable table"><table class="dec"><thead><tr><th>Decision</th><th>Options</th><th>Studio recommendation</th><th>Reason</th></tr></thead><tbody>{rows}</tbody></table></div>
  </div>
</section>'''


CSS = r"""
:root{--cell:#DCD9D2;--ink:#121212;--ink2:#45494F}
.s-newsprint{--cell:#DCD9D2;--ink:#121212;--ink2:#45494F}
.s-white{--cell:#FFFFFF;--ink:#121212;--ink2:#45494F}
.s-charcoal{--cell:#121212;--ink:#DCD9D2;--ink2:#DCD9D2}
.s-prussian{--cell:#1F2D5A;--ink:#DCD9D2;--ink2:#DCD9D2}
.bgf{fill:var(--cell)} .bgs{stroke:var(--cell)}
svg.mk{display:block;overflow:visible;max-width:none}
svg.mk.inl{display:inline-block;vertical-align:middle}
svg text{font-family:var(--body);font-size:13px;fill:currentColor}
svg .b{font-weight:700} svg .sb{font-weight:600} svg .ink2{fill:var(--ink2)} svg .hw{font-family:var(--display);font-weight:800;font-size:22px;letter-spacing:-0.01em} svg .lbl{font-weight:600;letter-spacing:.06em;fill:var(--ink2)}
.toc{display:flex;flex-wrap:wrap;gap:8px 18px;padding:0;margin:20px 0 0;list-style:none}
.toc a{color:var(--fg);font-weight:600}
.lede{font-size:1.0625rem}
.opt{margin:28px 0 0}
.opthead{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 8px}
.opthead h3{margin:0}
.tag.orig{border-style:dashed}
.tag.misuse{border-width:2px}
.tag{font-size:.8125rem;line-height:1.25}
.tag.best{background:var(--prussian);color:var(--newsprint);border-color:var(--prussian)}
.rec-opt{border-left:4px solid var(--prussian);padding-left:14px}
.surfaces{margin-top:8px}
.surfaces.gray{filter:grayscale(1);margin-top:1px}
.slab{font:600 .8125rem/1.3 var(--body);margin:0;color:var(--ink2);letter-spacing:.02em}
.s-charcoal .slab,.s-prussian .slab{color:var(--ink)}
.ls{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:2px 0;min-width:0}
.lw{font-size:.8125rem;font-weight:600;min-width:7.2em}
.gw{display:flex;gap:8px;align-items:flex-start;font-size:.8125rem;line-height:1.35;margin:2px 0}
.gw .gl{display:block;font-weight:400;color:var(--ink2)}
.s-charcoal .gw .gl,.s-prussian .gw .gl{color:var(--ink)}
.nosample{display:inline-block;width:34px;flex:none}
.gw svg{flex:none;margin-top:4px}
.chip{display:inline-flex;align-items:stretch;min-height:26px;vertical-align:middle;white-space:nowrap;font-feature-settings:"tnum" 1}
.chip .k{background:currentColor;display:inline-flex;align-items:center;padding:0 7px;border:1.5px solid currentColor}
.chip .k{color:var(--ink,#121212)}
.chip .k::after{content:none}
.chip .c{display:inline-flex;align-items:center;padding:0 8px;border:1.5px solid currentColor;border-left:0;font:700 .875rem/1 var(--body)}
.chip .k{font:600 .8125rem/1 var(--body);letter-spacing:.06em;text-transform:uppercase}
.chip .k{background:var(--ink,#121212);color:var(--cell,#DCD9D2);border-color:var(--ink,#121212)}
.chip .c{color:var(--ink,#121212);border-color:var(--ink,#121212)}
.cp{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:center;margin:4px 0}
.cn{font-size:.8125rem;line-height:1.3}
.bchip{display:inline-block;border:1px solid currentColor;padding:2px 6px;font:700 .8125rem/1.3 var(--body);margin-right:4px}
.v7r{font-size:.8125rem;margin:0 0 4px;line-height:1.35}
.meas{font-size:.8125rem;line-height:1.35;margin:6px 0 0;font-feature-settings:"tnum" 1}
.cap2{font-size:.8125rem;margin:2px 0 0;color:var(--ink2)}
.s-charcoal .cap2,.s-prussian .cap2{color:var(--ink)}
.code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.8125rem}
.none{color:var(--muted)}
.fig{margin:16px 0 0;padding:16px;min-width:0}
.fig figcaption p{font-size:.875rem;max-width:62ch}
.src{font-size:.8125rem;color:var(--muted)}
.ex2{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px;align-items:start}
.ex3{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px;align-items:start}
.pad{padding:12px}
.loophead{margin:0 0 10px;display:grid;gap:4px}
.loophead .lt{font-weight:700;font-size:.9375rem}
.loophead .lk{font-size:.8125rem;color:var(--ink2)}
.exh{margin:28px 0 8px;font-size:1.0625rem}
.wrap{overflow-x:auto;margin:16px 0 0;max-width:100%}
table.eq,table.map,table.dec{min-width:640px}
table.map{min-width:1100px}
table caption{text-align:left;font-size:.8125rem;color:var(--muted);padding:0 0 6px}
td .chip{margin:1px 0}
.fx td.pipcell{min-width:130px}
.fxr{display:grid;grid-template-columns:minmax(0,1fr);gap:2px;margin:3px 0}
.fxn{font-size:.8125rem;font-weight:600}
.fxw{font-size:.8125rem}
.ek{display:flex;gap:8px;align-items:center;font-size:.8125rem;margin:2px 0}
.evchip{display:flex;gap:8px;align-items:flex-start;font-size:.8125rem;line-height:1.35;border:1px solid currentColor;padding:6px 8px;margin:4px 0}
.evchip svg{margin-top:2px}
.narrow{display:block}.wide{display:none}
@media (min-width:1100px){.narrow{display:none}.wide{display:block}.tl{grid-template-columns:1fr}}
.rule li,.steps li{margin:0 0 6px;max-width:72ch}
.rec{background:var(--surface);border:1px solid var(--rule);border-left:6px solid var(--charcoal);padding:14px 16px;margin-top:24px}
.rec p{margin-bottom:8px}
.panel dl,.base dl{margin:8px 0 0}
dt{font-weight:700;font-size:.8125rem;letter-spacing:.03em;text-transform:uppercase;margin-top:10px}
dd{margin:2px 0 0;font-size:.9375rem}
.recpanel,.card{background:var(--newsprint)}
.ct{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.rules ol{margin:8px 0 0;padding-left:1.3em}
.rules li{margin:0 0 6px}
.bases{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}
.base img{width:100%;height:auto;display:block;border:1px solid var(--rule);margin:6px 0}
.dec th,.dec td{border-bottom-color:rgba(220,217,210,.45)}
.decision th{color:var(--newsprint)}
details{margin-top:12px} summary{cursor:pointer;font-weight:600}
q{quotes:"“" "”"}
.placeholder{outline:2px solid var(--fg);outline-offset:-6px}
.hv2{display:grid;justify-items:center;gap:6px}.harc{font-size:.8125rem;margin:0;color:var(--ink2);text-align:center}
.s-charcoal .harc,.s-prussian .harc{color:var(--ink)}
.widecells .surfaces{grid-template-columns:repeat(auto-fit,minmax(min(592px,100%),1fr))}
.span-all{grid-column:1/-1}
.hcomp{display:none}
@media (max-width:699px){.hdisp{display:none}.hcomp{display:block}.widecells .surfaces{grid-template-columns:1fr}}
@media (max-width:760px){.lw{min-width:0}}
"""


def build():
    g = DATA["generated"]
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Systems Marks Board</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;600;700&family=Lora:ital,wght@1,400&display=swap">
<link rel="stylesheet" href="board-base.css">
<style>{CSS}</style>
</head>
<body>
<main class="board">
<header>
  <p class="eyebrow">Phase 1 · Systems marks board · for Gate 1 · October 21, 2026</p>
  <h1>Systems marks for the atlas and the guide</h1>
  <p class="lede">This board proposes the marks that carry evidence, effects, events and authority in every Oath &amp; Action systems graphic. Each section draws the options at true size on Newsprint, White, Charcoal and Prussian, repeats them in grayscale, applies the leading option to a real Atlas V7 example, and closes with a recommendation. The Decisions for Gate 1 panel at the end collects every choice.</p>
  <p>Every ID, sign, delay, grade, effect, route and date here was read by script from Atlas V7, snapshot {date_long(g["snapshot"])}, on October 21, 2026. The model was not changed. Its inconsistencies go to the atlas editor in <span class="code">work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md</span>.</p>
  <p class="cap">Tags: {tag("Original")} what a supplied file does today. {tag("Defect fix")} a change that brings a drawing back in line with V7, the model authority. {tag("Option")} a proposal you may accept or decline. {tag("Recommended")} the studio's choice. {tag("Misuse")} a failure the rule prevents.</p>
  <ul class="toc">
    <li><a href="#m1">1 Evidence lines</a></li><li><a href="#m2">2 Grade words</a></li><li><a href="#m3">3 ID chips</a></li>
    <li><a href="#m4">4 Effects</a></li><li><a href="#m5">5 Events</a></li><li><a href="#m6">6 Authority and delay</a></li>
    <li><a href="#m7">7 The hinge</a></li><li><a href="#m8">8 Atlas bases</a></li><li><a href="#checks">Checks</a></li><li><a href="#decisions">Decisions</a></li>
  </ul>
</header>'''
    body = (section_evidence() + section_grades() + section_chips() + section_effects() + section_events()
            + section_authority_delay() + section_hinge() + section_bases() + section_checks() + section_decisions())
    OUT.write_text(head + body + "\n</main>\n</body>\n</html>\n", encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    build()
