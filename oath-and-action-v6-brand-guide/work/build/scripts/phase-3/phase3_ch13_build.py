"""Write chapter 13, Evidence and sourcing: its words, its plates and its manifest.

Oath & Action Edition 06, Phase 3, round 0. Editor (oa-editor), November 11, 2026, with the data lead's evidence rules
in view. The brief is work/handoffs/phase-3/20261111_Phase-3-Round-0-Brief.md; the proposal's section 1.1 lists what
each rule settles; DR-233 adds Rule 13.13.

Usage:
    python3 -I work/build/scripts/phase-3/phase3_ch13_build.py [--check-only]

Reads, by script, every value it prints from:
    work/extract/atlas-v7-data.json                 the atlas model, snapshot of October 15, 2026
    work/build/data/*.meta.json and *.csv           the engineer's data folder (contract C1): the child poverty and
                                                    payroll sidecars and the Census rows
Writes:
    work/build/guide/chapters/13-evidence.json
    work/build/guide/specimens/s-13-*.html and s-13-*.chart.json (contract C7's specs for the kit's charts)
    work/build/guide/specimens/manifest-evidence.json

Then runs the editor's checks and stops on any failure: no em dash, no listed filler or corporate word, no studio
word or decision code in reader text, every rule title at fifteen words or fewer, every failure caption led by
"Fails Rule 13.N.", every failure plate carrying the do-not-publish band and an alt that opens "Failure case: do not
publish.", every rule with Specifications, the opener under 16 KB, every Illustrative-flagged plate labeled, no literal
color, every font size from a token, the locked lines exact where they appear, every atlas ID it prints present in the
model, and Rule 01.9's spread over the chapter's example log.
"""
import csv
import html
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHAPTERS = ROOT / "work/build/guide/chapters"
SPECIMENS = ROOT / "work/build/guide/specimens"
V7_PATH = ROOT / "work/extract/atlas-v7-data.json"
DATA = ROOT / "work/build/data"
MAKER = "evidence"
WRITTEN = "November 11, 2026"

V7 = json.loads(V7_PATH.read_text())
LINK, NODE, LOOP, REFORM = V7["links"], V7["nodes"], V7["loops"], V7["reforms"]
GLOSS = {g["term"]: g["definition"] for g in V7["glossary"]}
ROUTE_NAME = {r["code"]: r["name"] for r in V7["routes"]["items"]}
SNAP_ISO = V7["meta"]["snapshot"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
def e(s):
    """Escape for HTML, with curly apostrophes (Rule 06's typography; the atlas's words stay as written)."""
    return html.escape(str(s).replace("'", "’"), quote=True)


MINUS = "−"


def need(cond, msg):
    if not cond:
        raise SystemExit(f"phase3_ch13_build: {msg}")


def words_date(iso):
    """2026-10-15 -> October 15, 2026 (house rule H05)."""
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {int(d)}, {y}"


SNAP = words_date(SNAP_ISO)
need(SNAP == "October 15, 2026", f"the atlas snapshot moved to {SNAP}; reread every value before printing")
ATLAS = "Oath & Action’s systems atlas, Who Do They Answer To?"


def sidecar(name):
    return json.loads((DATA / f"{name}.meta.json").read_text())


def rows(name):
    with open(DATA / f"{name}.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------------------------------------------
# The grade table (Rule 13.3). Display words and key glosses as Rule 12.6's key prints them (the chart system's
# GRADE_TABLE, DR-52); the line each one draws as Rule 10.10 measures it (V7's renderer, Gate 1's M1).
# ---------------------------------------------------------------------------------------------------------------
GRADE = {
    "documented": ("Documented", "on the public record", "solid"),
    "well-supported": ("Well supported", "strong research evidence", "solid"),
    "well_supported": ("Well supported", "strong research evidence", "solid"),
    "plausible": ("Plausible", "some evidence", "dashed"),
    "plausible_contested": ("Contested", "evidence disputed", "dashdot"),
    "contested": ("Contested", "evidence disputed", "dashdot"),
    "hypothesis": ("Hypothesis", "not yet tested", "dotted"),
}
DELAY = {"S": (1, "under 2 years"), "M": (2, "2 to 10 years"), "L": (3, "over 10 years")}
for k in ("S", "M", "L"):
    need(DELAY[k][1].replace("under ", "").replace("over ", "") in GLOSS["Delay"], f"delay {k} words differ from the atlas glossary")
FAMILY = {"DQ": "Quality of democracy", "GE": "Government efficacy", "EP": "Economic performance",
          "EQ": "Income and wealth equality"}   # DR-39: DQ prints as Quality of democracy
EFFECT_WORDS = V7["outcomes"]["effect_codes"]

# Instrument families for the event mark (Gate 1, M4): V7's ten instrument values in four shapes
INSTR = {"ballot initiative": "ballot", "referendum": "ballot", "federal statute": "statute", "state statute": "statute",
         "municipal ordinance (local law)": "statute", "council funding vote": "statute", "court ruling": "court",
         "agency rule": "exec", "executive action": "exec", "executive order": "exec"}
need(set(r["instrument"] for r in V7["repairLog"]["rows"]) <= set(INSTR), "the repair log holds an instrument the event mark lacks")
FAMILY_WORD = {"ballot": "Ballot measure", "statute": "Statute or local law", "court": "Court ruling",
               "exec": "Executive or agency action"}


# ---------------------------------------------------------------------------------------------------------------
# Marks. Every drawing reads its ink from the stage's surface through short token names, and every mark is hidden
# from assistive technology: the words beside it carry its meaning.
# ---------------------------------------------------------------------------------------------------------------
PATTERN_KEY = {"documented": "documented", "well-supported": "wellSupported", "well_supported": "wellSupported",
               "plausible": "plausible", "plausible_contested": "contested", "contested": "contested",
               "hypothesis": "hypothesis"}
PROPOSAL = ROOT / "work/handoffs/phase-3/20261111_Palette-Proposal.json"
TOKEN_LAG = []   # values the data lead set (D3-84) that tokens.json does not hold yet


def grade_values():
    """D3-84: the line code has one source, the atlas build's own constants, which the data lead read by script into the
    palette proposal's line_code_source and the oa.chart.grade tokens take. Read both, check them against the build, and
    note any token the engineer's release has not taken yet."""
    src = json.loads(PROPOSAL.read_text())["line_code_source"]
    read = src["read"]
    per = read["patterns_per_line_width"]
    for word, tex in (("Plausible", "dashed"), ("Contested", "dash-dot"), ("Hypothesis", "dotted")):
        need([x / 2 for x in BS.pattern(tex, 2)[0]] == per[word], f"{word}'s pattern differs from the atlas build (D3-84)")
    set_here = dict(x["value"].split(" = ", 1) for x in src["set_here_because_the_build_defines_none"] if " = " in x["value"])
    v = {"plausible": per["Plausible"], "contested": per["Contested"], "hypothesis": per["Hypothesis"],
         "widths": read["line_widths_px"], "clearance": read["dotted_head_clearance_line_widths"],
         "min_run": int(set_here["oa.chart.grade.minRun"].split()[0]),
         "square": int(set_here["oa.chart.grade.recordSquare"].split()[0]), "rail": 1, "gap": 1}
    need(v["widths"] == sorted(BS.ARROW) and BS.ARROW[2] == (10, 8) and BS.TAG[2] == (14, 6, 16, 8, 2),
         "the atlas build's marks changed; reread Rule 10.10")
    t = json.loads((ROOT / "work/build/tokens/tokens.json").read_text())["oa"]["chart"]["grade"]
    held = {"minRun": t.get("minRun", {}).get("$value"), "recordSquare": (t.get("recordSquare", {}).get("$value") or {}).get("value"),
            "conceptual.rail": (t.get("conceptual", {}).get("rail", {}).get("$value") or {}).get("value"),
            "conceptual.gap": t.get("conceptual", {}).get("gap", {}).get("$value"),
            "headClearance": t.get("headClearance", {}).get("$value")}
    want = {"minRun": v["min_run"], "recordSquare": v["square"], "conceptual.rail": v["rail"], "conceptual.gap": v["gap"],
            "headClearance": v["clearance"]}
    for k, x in want.items():
        if held[k] != x:
            TOKEN_LAG.append(f"oa.chart.grade.{k}: tokens.json holds {held[k]!r}, D3-84 sets {x!r}")
    v["tokens"] = {k: k in t or k.split(".")[0] in t for k in ("documented", "wellSupported", "plausible", "contested", "hypothesis",
                                                              "conceptual.rail", "minRun", "recordSquare", "headClearance")}
    v["tokens"]["headClearance"] = "headClearance" in t
    return v


# The atlas build's own drawing (Rule 10.10's builders line): wire_marks, pattern and tag_shape, imported, never retyped
_bs = importlib.util.spec_from_file_location("oa_atlas_build", ROOT / "work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py")
BS = importlib.util.module_from_spec(_bs)
_bs.loader.exec_module(BS)
GV = grade_values()
LW = 2                                    # the line width every plate draws at
MIN_RUN = GV["min_run"] * LW              # the shortest textured run, oa.chart.grade.minRun: 40 px at 2 px
KEY_W = MIN_RUN + 15                      # a key sample: the run, the 10 px arrowhead, the ends and the dots' clearance
STEP_W = 88                               # a step's line in a list of steps


def line_svg(grade=None, w=STEP_W, delay=None, sign=None, hollow=False, target=False):
    """A connection drawn left to right by the atlas build's wire_marks: the line in its grade's pattern (or hollow), delay
    ticks after the tail, the sign tag, the arrowhead. target=True draws Rule 12.5's red target at the 6 px sizes."""
    h = 24 if target else 16
    y = h // 2
    tex = "solid" if hollow or not grade else GRADE[grade][2]
    run = w - 12 - (GV["clearance"] * LW if tex == "dotted" else 0)
    need(hollow or run >= MIN_RUN, f"a {w} px line carries {run} px of pattern, under the shortest run, {MIN_RUN} px")
    marks, _, _ = BS.wire_marks([(1, y), (w - 1, y)], PATTERN_KEY.get(grade or "documented"), sign if sign in ("+", "-") else None,
                                delay, LW, lit=target, sketch=hollow)
    if not target:
        # the case under a line shows only on a red target; the rest are defaults the stylesheet sets once
        marks = re.sub(r'<path class="ak-case"[^>]*/>', "", marks)
        marks = marks.replace(' fill="none"', "").replace(' stroke-linecap="butt"', "")
    # the guide's page shell hides its own .rail (the chapter list) on phones, so the hollow line's rails take another class
    marks = marks.replace('class="rail"', 'class="rl"')
    red = ' data-red="working" data-red-job="where a reform acts"' if target else ""
    return (f'<svg class="ln{" tgt" if target else ""}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true" '
            f'focusable="false"{red}>{marks}</svg>')


def rsq():
    """The record square (Gate 1, M1): 7 px, filled, before the word Documented in a connection's label."""
    q = GV["square"]
    return f'<svg class="rs" viewBox="0 0 {q} {q}" width="{q}" height="{q}" aria-hidden="true" focusable="false"><rect width="{q}" height="{q}"/></svg>'


def grade_word(grade, gloss=True):
    word, g, _ = GRADE[grade]
    lead = rsq() + " " if grade == "documented" else ""
    return f'<span class="gw"><span class="w">{lead}<b>{e(word)}</b></span>{", " + e(g) if gloss else ""}</span>'


def event_svg(fam, pending=False):
    """The event mark (Gate 1, M4): a shape for the instrument, an outline when pending."""
    shape = {"ballot": '<rect x="4" y="4" width="8" height="8"/>', "statute": '<rect x="2" y="5" width="12" height="6"/>',
             "court": '<rect x="5" y="2" width="6" height="12"/>'}
    if fam == "exec":
        body = '<rect class="ol" x="4.25" y="4.25" width="7.5" height="7.5"/><rect x="6.5" y="6.5" width="3" height="3"/>'
    else:
        body = shape[fam]
        if pending:
            body = body.replace("<rect ", '<rect class="ol" ')
    return f'<svg class="ev-m" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false">{body}</svg>'


def pips_svg(code):
    """The ordinal effect mark (Gate 1, M4): one to three pips right of the zero line for a gain, left for a cost, a bar
    on the zero line for no expected effect."""
    out = ['<line class="z" x1="44" y1="2" x2="44" y2="20"/>']
    m = re.match(r"([+\-−])([SML])", code)
    if code.startswith("0"):
        out.append('<rect x="42" y="4" width="4" height="14"/>')
    elif m:
        n = {"S": 1, "M": 2, "L": 3}[m.group(2)]
        side = 1 if m.group(1) == "+" else -1
        for i in range(n):
            out.append(f'<circle cx="{44 + side * (11 + 12 * i)}" cy="11" r="4.5"/>')
    return (f'<svg class="pp" viewBox="0 0 88 22" width="88" height="22" aria-hidden="true" focusable="false">'
            + "".join(out) + "</svg>")


def chip(kind, rid, after=""):
    """A typed chip (Rule 18.24, house rule H11): the kind word and the ID in one outlined label. Punctuation that follows
    the chip stays on its line with it."""
    c = f'<span class="chip">{e(kind)} <span class="id">{e(rid)}</span></span>'
    return f'<span class="nw2">{c}{e(after)}</span>' if after else c


def mk(n):
    """A numeral that ties a part of the opener's record to its line in the list beside it."""
    return f'<span class="mk" aria-hidden="true">{n}</span>'


GL_CENSUS = "Documented: a Census Bureau survey"          # D3-83: an official statistic takes Documented, its source after
GL_BLS = "Documented: a Bureau of Labor Statistics survey of employers, as copied by FRED"


def least_certain(link_ids):
    """The grade of a diagram's least certain step: the word an atlas diagram prints in the label's place (Rule 13.1)."""
    order = ["hypothesis", "plausible_contested", "contested", "plausible", "well-supported", "documented"]
    return min((LINK[i]["evidence"] for i in link_ids), key=order.index)


def diagram_label(grade, what):
    """The dark chip of an atlas diagram: its least certain grade word, then what that grade belongs to."""
    return f'<div class="evr"><span class="ev">{e(GRADE[grade][0])}</span><span class="gr">{e(what)}</span></div>'


def dnp():
    """The do-not-publish band (CD-S2, D2-1801)."""
    return '<p class="dnp"><span aria-hidden="true">×</span>Failure case: do not publish</p>'


def ill(words="Illustrative"):
    return f'<span class="illus">{e(words)}</span>'


# ---------------------------------------------------------------------------------------------------------------
# Styles. Each plate carries only the rules its own markup uses, so a plate stays light (D2-1732). Every size comes
# from a type token or a chart type token; every color from a short token name the stage's surface class sets.
# ---------------------------------------------------------------------------------------------------------------
LBL = ("font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);"
       "text-transform:var(--oa-type-label-text-transform)")
CAP = "font:var(--oa-type-caption)"
BASE = (":scope{color:var(--oa-color-text-primary)}"
        ".p{box-sizing:border-box;padding:16px;font:var(--oa-type-body);max-width:100%}"
        ".p *{box-sizing:border-box}:where(.p) :where(p){margin:0}@media (min-width:48em){.p{padding:24px}}")
CSS = {
    "dnp": f".dnp{{display:flex;align-items:center;gap:8px;margin:0 0 16px;padding:6px 10px;background:var(--oa-color-surface-charcoal);"
           f"color:var(--oa-color-text-primary-on-charcoal);{LBL}}}",
    "evr": ".evr{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;margin:0 0 10px}",
    "ev": f".ev{{display:inline-flex;align-items:center;min-height:24px;padding:3px 8px;background:var(--oa-chart-color-chip-fill);"
          f"color:var(--oa-chart-color-chip-label);{LBL}}}",
    "gr": f".gr{{{CAP};color:var(--oa-color-text-secondary)}}",
    "ct": (".ct{font:var(--oa-font-weight-extrabold) var(--oa-chart-type-title-phone-size)/var(--oa-chart-type-title-phone-leading) "
           "var(--oa-font-family-display);letter-spacing:-0.01em;margin:0 0 6px;max-width:34em;text-wrap:balance}"
           "@media (min-width:48em){.ct{font-size:var(--oa-chart-type-title-size);line-height:var(--oa-chart-type-title-leading)}}"),
    "ms": (".ms{font:400 var(--oa-chart-type-measure-size)/var(--oa-chart-type-measure-leading) var(--oa-font-family-reading);"
           "color:var(--oa-color-text-secondary);max-width:40em}.sub+.ms{margin-top:8px}"),
    "nt": f".nt{{{CAP};margin-top:10px;max-width:40em}}",
    "src": f".src{{{CAP};color:var(--oa-color-text-secondary);margin-top:12px;max-width:44em}}",
    "chip": (".chip{display:inline-flex;align-items:center;gap:.3em;padding:1px 8px;border:1px solid var(--oa-color-border-strong);"
             "font:var(--oa-type-data-label);white-space:nowrap;vertical-align:baseline}.chip .id{font-variant-numeric:tabular-nums}"),
    "k": f".k{{{LBL};color:var(--oa-color-text-secondary);margin:0 0 6px}}",
    "ln": (".ln{display:block;flex:none;overflow:visible}.ln path{fill:none}.ln .ak-case{stroke:none}.ln .ak-mark{stroke:var(--oa-color-graphic-essential)}"
           ".ln .hd,.ln .tg polygon{fill:var(--oa-color-graphic-essential)}.ln .tg .sg{fill:var(--oa-color-surface)}"
           ".ln .tk{stroke:var(--oa-color-graphic-essential);stroke-width:2px}.ln .rl{stroke:var(--oa-color-graphic-essential)}"
           ),
    "tgt": (".ln .hi{display:none}.ln.tgt .lo{display:none}.ln.tgt .hi{display:inline}"
            ".ln.tgt .ak-mark{stroke:var(--oa-color-data-emphasis-red);stroke-width:4px;stroke-dasharray:var(--d6,none)}"
            ".ln.tgt .ak-case{stroke:var(--oa-color-graphic-essential);stroke-width:6px;stroke-dasharray:var(--d6,none)}"
            ".ln.tgt .hd{fill:var(--oa-color-data-emphasis-red)}"),
    "rs": ".rs{display:inline-block;fill:var(--oa-color-graphic-essential);vertical-align:.08em;margin-right:5px}",
    "gw": ".gw b{font-weight:var(--oa-font-weight-bold)}.gw .w{white-space:nowrap}",
    "ev-m": (".ev-m{display:block;flex:none;fill:var(--oa-color-graphic-essential)}"
             ".ev-m .ol{fill:none;stroke:var(--oa-color-graphic-essential);stroke-width:1.5}"),
    "pp": ".pp{display:block;flex:none;fill:var(--oa-color-graphic-essential)}.pp .z{stroke:var(--oa-color-graphic-essential);stroke-width:1}",
    "tb": (f".tb{{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}}"
           f".tb th,.tb td{{text-align:left;vertical-align:top;padding:9px 12px 9px 0;border-bottom:1px solid var(--oa-color-border-hairline)}}"
           f".tb thead th{{{LBL};color:var(--oa-color-text-secondary);border-bottom:2px solid var(--oa-color-border-strong)}}"
           f".tb caption{{{CAP};color:var(--oa-color-text-secondary);text-align:left;margin:0 0 8px}}"
           f".tb .num{{font-variant-numeric:tabular-nums}}.tb tbody th{{font-weight:var(--oa-font-weight-regular)}}"
           f".tb .ttl{{font-family:var(--oa-font-family-display);font-weight:var(--oa-font-weight-extrabold)}}.tb .ttl p+p{{margin-top:6px}}"
           f".tb .cl{{display:inline-flex;flex-direction:column;align-items:flex-start;gap:4px}}"
           f"@media (max-width:47.99em){{.tb .cl{{display:flex;margin-top:4px}}}}"),
    "stack": (".stack td[data-k]::before{content:none}@media (max-width:47.99em){.stack,.stack tbody,.stack tr,.stack th,.stack td{display:block;width:100%}"
              ".stack caption{display:block;width:auto}.stack thead{display:none}.stack tr{border-bottom:1px solid var(--oa-color-border-strong);padding:8px 0}"
              ".stack th,.stack td{border:0;padding:3px 0}.stack td[data-k]::before{content:attr(data-k) \": \";font-weight:var(--oa-font-weight-bold)}}"),
    "p0": ".p.p0{padding:16px}",  # a true-size stage keeps the phone gutter inside its 360 px
    "card": (".card{max-width:360px;border-top:4px solid var(--oa-color-border-strong);padding:14px 0 0}"
             ".card .hl{font:var(--oa-type-h4-font-weight) 1.25rem/var(--oa-type-h4-line-height) var(--oa-type-h4-font-family);"
             "letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 10px;text-wrap:balance}"
             ".card p+p{margin-top:10px}.card.nb{border-top:0;padding-top:0}"
             # an article's headline stays larger than the chart title the kit prints inside it (22 px in a narrow column)
             ".card .hl.art{font-size:1.625rem;line-height:var(--oa-type-h3-line-height)}"),
    "q": (".q{font:var(--oa-type-quote);letter-spacing:var(--oa-type-quote-letter-spacing);margin:0;text-indent:-.42em;max-width:30em}"),
    "qs": f".qs{{font:italic 400 var(--oa-type-body-font-size)/1.6 var(--oa-font-family-quote);margin:0}}",
    "by": f".by{{{CAP};color:var(--oa-color-text-secondary);margin-top:8px}}",
    "fx": ".fx{display:grid;grid-template-columns:minmax(0,1fr);gap:24px}@media (min-width:48em){.fx.two{grid-template-columns:repeat(2,minmax(0,1fr))}}",
    "rw": ".rw{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px}",
    "lp": ".lp+.lp{margin-top:20px;padding-top:16px;border-top:1px solid var(--oa-color-border-hairline)}.lp .k{margin-bottom:10px}",
    "wt": ".st.wt{grid-template-columns:148px minmax(0,1fr)}@media (max-width:30em){.st.wt{grid-template-columns:minmax(0,1fr)}}",
    "st": ".st{display:grid;grid-template-columns:88px minmax(0,1fr);gap:4px 12px;align-items:start;margin-top:10px}.st .ln{margin-top:5px}"
          "@media (max-width:30em){.st{grid-template-columns:minmax(0,1fr);gap:2px}.st .ln{margin-top:0}}",
    "hed": f".hed{{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 10px;margin:0 0 4px;font:var(--oa-type-body-small)}}",
    "sub": f".sub{{{CAP};color:var(--oa-color-text-secondary)}}",
    "fxr": ".fxr{display:grid;grid-template-columns:minmax(0,11rem) 88px minmax(0,1fr);gap:4px 12px;align-items:center;padding:6px 0;border-bottom:1px solid var(--oa-color-border-hairline);font:var(--oa-type-body-small)}"
           "@media (max-width:30em){.fxr{grid-template-columns:88px minmax(0,1fr)}.fxr .fn{grid-column:1/-1}}",
    "blk": ".blk{margin-top:16px}",
    "ol": f".ol{{margin:8px 0 0;padding:0 0 0 1.4em;font:var(--oa-type-body-small)}}.ol li+li{{margin-top:4px}}",
    "evl": ".evl{list-style:none;margin:0;padding:0}.evl li{display:grid;grid-template-columns:16px minmax(0,1fr);gap:2px 10px;padding:8px 0;border-bottom:1px solid var(--oa-color-border-hairline);font:var(--oa-type-body-small)}.evl .ev-m{margin-top:4px}",
    "dt": ".dt{font-weight:var(--oa-font-weight-semibold);font-variant-numeric:tabular-nums}",
    "flag": f".flag{{{LBL};color:var(--oa-color-text-secondary)}}",
    "cn": (f".cn{{border-top:4px solid var(--oa-color-graphic-essential);padding:10px 0 12px;margin:0 0 14px;{CAP}}}"
           ".cn b{font-weight:var(--oa-font-weight-bold)}"),
    "bc": (".bc{display:block;overflow:visible;margin-top:8px}.bc .b{fill:var(--oa-chart-color-subject)}"
           ".bc .bl{stroke:var(--oa-chart-color-baseline);stroke-width:var(--oa-chart-line-baseline)}"
           ".bc text{font-family:var(--oa-font-family-reading);font-size:var(--oa-chart-type-label);fill:var(--oa-chart-color-label)}"
           ".bc .n{font-weight:var(--oa-font-weight-semibold)}.bc .v{font-weight:var(--oa-font-weight-bold);font-variant-numeric:tabular-nums}"),
    "foot": f".foot{{{CAP};color:var(--oa-color-text-secondary);margin-top:14px;padding-top:8px;border-top:1px solid var(--oa-color-border-hairline)}}",
    "dek": ".dek{font:var(--oa-type-body-small);margin:0 0 12px}",
    "box": ".box{display:inline-flex;align-items:center;padding:6px 10px;border:1.5px solid var(--oa-color-border-strong);font:var(--oa-type-body-small)}",
    "arrowrow": ".arrowrow{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px}",
    "tag": f".tag{{{LBL}}}",
    "kys": ".kys{display:flex;flex-wrap:wrap;gap:8px 24px;font:var(--oa-type-body-small)}",
    "ky": ".ky{display:inline-flex;align-items:center;gap:6px}",
    "mk": (f".mk{{display:inline-flex;align-items:center;justify-content:center;min-width:20px;height:20px;padding:0 4px;"
           f"border-radius:10px;background:var(--oa-chart-color-chip-fill);color:var(--oa-chart-color-chip-label);{LBL};"
           f"letter-spacing:0;vertical-align:.15em;margin:0 1px 0 3px}}"),
    "nw2": ".nw2{white-space:nowrap}",
    "kl": ".kl{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:6px;font:var(--oa-type-body-small)}",
    "thick": ".ln .thick{fill:none;stroke:var(--oa-color-graphic-essential);stroke-width:12}",
}


def styled(body):
    used = set()
    for cls in re.findall(r'class="([^"]+)"', body):
        used.update(cls.split())
    rules = [BASE] + [css for k, css in CSS.items() if k in used]
    return "<style>" + "".join(rules) + "</style>"


# ---------------------------------------------------------------------------------------------------------------
# The book of plates
# ---------------------------------------------------------------------------------------------------------------
class Book:
    def __init__(self):
        self.files, self.manifest, self.examples = {}, {}, []

    def add(self, sid, body, *, rule, alt, illustrative=False, readable=False, notes="", width=None):
        """A plate. With width, the piece is drawn at that true width, edge to edge, and the frame says so (brand S7)."""
        need(sid not in self.files, f"duplicate specimen {sid}")
        body = re.sub(r">\s+<", "><", body.strip())
        self.files[sid] = (f"<!-- {sid}: Oath & Action guide, Edition 06, chapter 13. Editor, {WRITTEN}. Written by "
                           f"work/build/scripts/phase-3/phase3_ch13_build.py. -->\n" + styled(body + (' class="p0"' if width else ""))
                           + f'\n<div class="p{" p0" if width else ""}">{body}</div>\n')
        m = {"chapter": "13", "rule": rule, "width_px": width, "alt": " ".join(alt.replace("'", "’").split()), "illustrative": bool(illustrative),
             "notes": notes}
        if readable:
            m["readable"] = True
        if width and width <= 360:
            m["fit_switch"] = False      # a phone piece at true size, as chapter 11's 360 px plates are set
        self.manifest[sid] = m

    def log(self, where, example, domain, states=(), level="federal"):
        """Rule 01.12's example log, counted for Rule 01.9 (DR-229)."""
        self.examples.append({"where": where, "example": example, "domain": domain, "states": list(states), "level": level})


# ---------------------------------------------------------------------------------------------------------------
# Atlas facts read once, with the checks that hold them to the model
# ---------------------------------------------------------------------------------------------------------------
def link(i):
    need(i in LINK, f"connection {i} is not in the atlas")
    return LINK[i]


def node_title(i):
    need(i in NODE, f"variable {i} is not in the atlas")
    return NODE[i]["title"]


def chart_head(label, grade_line, title, measure, notes=(), source=None, illus=None):
    out = [f'<div class="evr"><span class="ev">{e(label)}</span><span class="gr">{e(grade_line)}</span>{ill(illus) if illus else ""}</div>',
           f'<p class="ct">{e(title)}</p>', f'<p class="ms">{e(measure)}</p>']
    out += [f'<p class="nt">{e(n)}</p>' for n in notes]
    if source:
        out.append(f'<p class="src">{e(source)}</p>')
    return "".join(out)


FC = "Failure case: do not publish. "


# ===============================================================================================================
# The opener: one record from the atlas with the evidence it carries
# ===============================================================================================================
def opener(book):
    l02 = link("L02")
    need((l02["evidence"], l02["delay"], l02["polarity"], l02["from"], l02["to"]) == ("plausible", "M", "+", "B1", "E1"),
         "Connection L02 changed in the atlas")
    name = l02["name"]
    need(" can " in f" {name} ", "L02's name no longer carries “can”")
    head, tail = name.split(" can ", 1)
    parts = [("“Can”, the verb a plausible grade allows", "13.2"),
             ("The grade word and its plain gloss, in the label", "13.3"),
             ("The dashed line of a plausible connection", "13.4"),
             ("The delay in ticks, kept apart from the grade", "13.5"),
             ("The typed chip for every atlas ID", "13.9"),
             ("The snapshot date, since the record can change", "13.10")]
    body = (f'<div class="fx two"><div>'
            f'<div class="evr"><span class="ev">{e(GRADE["plausible"][0])}</span>{mk(2)}<span class="gr">some evidence, the '
            f'atlas’s grade for this connection</span></div>'
            f'<p class="hed">{chip("Connection", "L02")}{mk(5)}<span class="sub">in {chip("Loop", "R1")}</span></p>'
            f'<p class="ct">“{e(head)} can{mk(1)} {e(tail)}”</p>'
            f'<p class="ms">From {chip("Variable", "B1", ",")} {e(lc(node_title("B1")))}, to {chip("Variable", "E1", ",")} '
            f'{e(lc(node_title("E1")))}</p>'
            f'<div class="rw blk">{line_svg("plausible", 168, delay="M", sign="+")}{mk(3)}</div>'
            f'<p>{grade_word("plausible")}. Sign +, the two move the same way. Delay M, {DELAY["M"][1]}, two ticks{mk(4)}</p>'
            f'<p class="src">Source: {e(ATLAS)}, connection L02, snapshot of {SNAP}{mk(6)}, United States.</p></div>'
            f'<div><p class="k">What each part carries</p><ol class="ol">'
            + "".join(f"<li>{e(w)}, Rule {r}</li>" for w, r in parts) + "</ol></div></div>")
    book.add("s-13-opener", body, rule=None, readable=True,
             alt=(f"One record from our systems atlas with the evidence it carries, each part numbered. A dark label reads "
                  f"Plausible, some evidence. Connection L02, in Loop R1, is named “{name}”, and runs from Variable B1, "
                  f"{lc(node_title('B1'))}, to Variable E1, {lc(node_title('E1'))}. A dashed line carries a plus sign tag and two "
                  f"delay ticks. Its words read Plausible, some evidence; sign plus, the two move the same way; delay M, "
                  f"{DELAY['M'][1]}. The source line names the atlas and the snapshot of {SNAP}. A list beside it names the "
                  "six numbered parts and their rules: the verb can, Rule 13.2; the grade word and gloss, Rule 13.3; the dashed "
                  "line, Rule 13.4; the delay apart from the grade, Rule 13.5; the typed chip, Rule 13.9; the snapshot date, "
                  "Rule 13.10."),
             notes="Chapter 13's opener (D2-1708, D2-1732): a light drawing the chapter's rules use, with only the styles it "
                   "needs. The line is the atlas build's own wire_marks; the numerals tie each part to the list (brand S1).")
    book.log("opener", "Connection L02", "D03")
    return {"specimen": "s-13-opener",
            "caption": "Connection L02 as our systems atlas records it. Each numeral marks a part that carries its evidence, "
                       "and the list names the rule that sets it."}


# ===============================================================================================================
# Rule 13.1, the four kinds
# ===============================================================================================================
def cp_source(kind="children"):
    """The child poverty source line from the sidecar (never retyped). Statistics M3 and CD M4: until the research lead's
    sidecar carries the corrected qualification and a line for both groups, the plate prints the sidecar's line with
    the qualification the reviewers' fix gives and, for the pair of charts, both groups named."""
    sc = sidecar("census-spm-child-poverty")
    var = sc.get("source_line_variants") or {}
    if kind == "both" and var.get("source_line_children_and_all_people"):
        return var["source_line_children_and_all_people"], "sidecar"
    line = sc["printed_source_line"]
    old_q = ("Figures for 2019 to 2024 include the Bureau’s August 2026 revision and differ by up to 0.4 points from those "
             "first published.")
    new_q = ("Figures for 2019 to 2024 include the Bureau’s August 2026 correction to the poverty thresholds, and 2024 also "
             "takes new population weights; they differ by up to 0.4 points from the earlier release.")
    how = "sidecar"
    if old_q in line:
        line, how = line.replace(old_q, new_q), "sidecar, qualification as statistics M3 gives it"
    if kind == "both":
        need("children under 18, 2009 to 2025" in line, "the child poverty source line changed")
        line, how = line.replace("children under 18, 2009 to 2025", "children under 18 and all people, 2009 to 2025"), how + ", both groups named"
    return line, how


def rule_13_1(book):
    cp = {(r["year"], r["age_group"], r["vintage"]): r for r in rows("census-spm-child-poverty")
          if r["measure"] == "spm" and r["series_variant"] in ("standard",)}
    c25 = cp[("2025", "under_18", "p60-290")]
    need((c25["percent"], c25["moe_pct"]) == ("13.4", "0.6"), "the 2025 child poverty row changed")
    cl = V7["claims"]["CL1507"]
    need("17% lower posted wages" in cl["supports"] and "8,000" in cl["supports"] and cl["confidence"] == "well-supported"
         and cl["period"] == "2010 to 2013 postings", "claim CL1507 changed")
    dl = next(r for r in V7["deliveryLog"]["rows"] if r["id"] == "DL06")
    need("613,501 lives saved" in dl["outcome"] and "a hypothetical estimate" in dl["qualification"]
         and "begins in 1975" in dl["qualification"] and dl["evidence_grade"] == "well-supported"
         and "1960 to 2012" in dl["source_title"], "delivery log DL06 changed")
    need(GLOSS["Association"].startswith("Two measures that move together without an established causal path."),
         "the atlas's definition of an association changed")
    need(GLOSS["Supplemental Poverty Measure"].startswith("A Census Bureau poverty measure that counts taxes, tax credits and benefits"),
         "the atlas's definition of the Supplemental Poverty Measure changed")
    src_cp, how = cp_source()
    assoc_src = ("Source: José Azar, Ioana Marinescu and Marshall I. Steinbaum, “Labor Market Concentration,” Journal of "
                 f"Human Resources, 2022, online job postings, 2010 to 2013, United States, as recorded in {ATLAS}, claim "
                 f"CL1507, snapshot of {SNAP}. Online postings leave out some jobs.")
    assoc_gl = "Well supported, as our systems atlas grades the research on employer concentration"
    finding = chart_head("Finding", GL_CENSUS,
                         "Child poverty stood at 13.4 percent in 2025 under the Supplemental Poverty Measure",
                         "Children under 18 below the poverty line, Supplemental Poverty Measure, percent, United States, 2009 to 2025",
                         notes=["The Supplemental Poverty Measure counts taxes, tax credits and benefits such as food aid, and "
                                "subtracts costs such as medical expenses. The survey’s margin of error for 2025 is 0.6 points "
                                "at 90 percent confidence."],
                         source=src_cp)
    assoc = chart_head("Association", assoc_gl,
                       "Job postings offered 17 percent lower wages where a few employers did more of the hiring",
                       "Posted wages in a local job market at the 75th percentile of employer concentration against one at the 25th, "
                       "United States, 2010 to 2013",
                       notes=["The study measured a pattern across markets. It does not show that concentration caused the lower wages."],
                       source=assoc_src)
    estimate = chart_head("Estimate", "Well supported, as our systems atlas grades this delivery case",
                          "Vehicle safety technologies saved an estimated 614,000 lives from 1960 to 2012",
                          "Lives saved by vehicle safety technologies and the federal safety standards behind them, United States, "
                          "1960 to 2012",
                          notes=["Method: the National Highway Traffic Safety Administration removes each technology from its crash "
                                 "records, using that technology’s measured effect, and counts the deaths that would have followed. "
                                 "The agency’s figure is 613,501, and it calls the result “a hypothetical estimate.” Its crash "
                                 "records begin in 1975, so the agency extrapolates the earlier years."],
                          source=("Source: National Highway Traffic Safety Administration, Lives Saved by Vehicle Safety Technologies "
                                  "and Associated Federal Motor Vehicle Safety Standards, 1960 to 2012 (DOT HS 812 069), United States, "
                                  f"as recorded in our systems atlas’s delivery log, delivery case DL06, snapshot of {SNAP}. The "
                                  "estimate assumes each technology’s effect held steady for five decades."))
    illus = chart_head("Illustration", "Invented values that show how a ranked bar works",
                       "A ranked bar puts the town with the most library hours first",
                       "Hours a week the main library is open, five invented towns",
                       source="Values invented for this example.", illus="Illustrative data")
    body = "".join(f'<div class="lp">{x}</div>' for x in (finding, assoc, estimate, illus))
    book.add("s-13-1-correct", body, rule="13.1", readable=True, illustrative=True,
             alt=("Four chart heads, one of each kind of evidence, each with a dark label, a grade line, a title, a measure line "
                  "and a source. Finding, Documented: a Census Bureau survey: Child poverty stood at 13.4 percent in 2025 under "
                  "the Supplemental Poverty Measure, with a note that defines the measure and gives the margin of error. "
                  "Association, Well supported: Job postings offered 17 percent lower wages where a few employers did more of "
                  "the hiring, with a note that the pattern does not show cause. Estimate, Well supported: Vehicle safety "
                  "technologies saved an estimated 614,000 lives from 1960 to 2012, with a note on the agency’s method and its "
                  "figure, 613,501. Illustration: A ranked bar puts the town with the most library hours first, labeled "
                  "Illustrative data."),
             notes=f"Evidence label and grade line as the approved chart system draws them (DR-52), with D3-83's grade rule for "
                   f"an official statistic. Child poverty from the engineer's census-spm-child-poverty file; its source line from "
                   f"the {how}. CL1507 and DL06 read from the atlas.")
    book.log("13.1 correct", "Child poverty, 2025 (Census P60-290)", "D08")
    book.log("13.1 correct", "Claim CL1507, employer concentration and posted wages", "D07")
    book.log("13.1 correct", "Delivery case DL06, lives saved by vehicle safety standards", "D04")
    book.log("13.1 correct", "Five towns' library hours", "invented", level="invented")
    fail = dnp() + chart_head("Finding", assoc_gl, "Concentrated hiring cuts wages by 17 percent",
                              "Posted wages and employer concentration, local job markets, United States, 2010 to 2013",
                              source=assoc_src)
    book.add("s-13-1-failure", fail, rule="13.1",
             alt=(FC + "A chart head labeled Finding over the same study of job postings, titled Concentrated hiring cuts wages "
                  "by 17 percent, with no note that the study measured a pattern."),
             notes="Labeled failure: a causal verb and the Finding label over an association; grade line and source as the correct plate.")
    return {
        "id": "13.1",
        "title": "Title each chart or diagram as a finding, an association, an estimate or an illustration.",
        "rule": [
            "An evidence label, a chip in the chart chip colors, sits above every chart title and names the kind of evidence in "
            "one of four words. A finding is a measured result with a source and a period, such as a count or a survey figure. "
            "An association is what our systems atlas defines as “" + GLOSS["Association"].split(". ")[0] + ".” An estimate "
            "rests on a model’s assumptions, such as a projection. An illustration shows how a design works with invented values.",
            "The grade follows the label in words: the atlas’s grade for a figure from the atlas (Rule 13.2), and Documented for "
            "an official statistic or a public record, with its source after the colon. A diagram of atlas connections prints "
            "the grade word of its least certain step in the label’s place.",
        ],
        "tokens": ["oa.chart.color.chip.fill.onNewsprint", "oa.chart.color.chip.label.onNewsprint",
                   "oa.chart.color.chip.fill.onCharcoal", "oa.chart.color.chip.label.onCharcoal"],
        "why": {"text": ["A reader decides how far to trust a chart before reading it closely. The label names what they are "
                         "looking at: something measured, a pattern, a projection or a demonstration. A title that states a "
                         "cause over a chart of a pattern misleads with true numbers, and the label puts that difference in the "
                         "first word on the figure."],
                "basis": "Design judgment, from the chart system our founder and editor approved in November 2026"},
        "correct": {"specimen": "s-13-1-correct",
                    "caption": "Four chart heads, one of each kind, with the charts under them left out. The finding gives its "
                               "margin of error, the association’s note says the pattern does not show cause, and the estimate’s "
                               "note gives the method behind its number."},
        "failure": {"specimen": "s-13-1-failure",
                    "caption": "<strong>Fails Rule 13.1.</strong> The label says Finding and the title says concentrated hiring "
                               "“cuts” wages, over a study that measured a pattern across job markets, so a reader takes the "
                               "pattern for a cause."},
        "specs": [
            {"label": "Evidence label", "value": "Finding, Association, Estimate or Illustration, in the label style on the chart chip fill, which turns with the theme",
             "token": "oa.chart.color.chip.fill.onNewsprint"},
            {"label": "Grade line", "value": "After the label: the atlas’s grade for an atlas figure; Documented for an official statistic or a public record, then its source, as in “Documented: a Census Bureau survey”", "token": "oa.type.caption"},
            {"label": "A finding", "value": "A count or a survey tabulation, with the publisher’s margin of error where one exists, at its stated confidence"},
            {"label": "An estimate", "value": "A figure that rests on a model’s assumptions, such as a projection, a small-area model or a with-and-without calculation, with its range or method"},
            {"label": "An association", "value": "Words such as “went with” at any grade, and a note that the pattern does not show cause"},
            {"label": "An illustration", "value": "Invented values only, with “Illustrative data” beside the chart (Rule 13.8)"},
            {"label": "An atlas diagram", "value": "The grade word of its least certain step in the label’s place, and what that grade belongs to after it"},
            {"label": "Measure line", "value": "The line under the title that says what is counted, in what unit, where and when"},
        ],
        "related": ["02", "14", "15"],
        "builders": ["Store the kind in the chart’s spec as its evidence field and print the label from that field, so the "
                     "label and the title come from one record.",
                     "Take an atlas claim’s kind from its own words: a claim the atlas writes as “associated with” is an "
                     "association, whatever its grade."],
    }


def lc(title):
    """A record's name in running text: the first letter lowered unless the first word is a name."""
    first = title.split(" ")[0]
    if first in ("Congress", "Congress's", "Congress’s", "Medicare", "Social", "U.S."):
        return title
    return title[0].lower() + title[1:]


# ===============================================================================================================
# Rule 13.2, the verb each grade allows
# ===============================================================================================================
def rule_13_2(book):
    le02, l26, l20, l47, l18 = (link(i) for i in ("LE02", "L26", "L20", "L47", "L18"))
    need(le02["evidence"] == "documented" and "as of July 31, 2026" in le02["qualification"]
         and "46.6% spent" in le02["qualification"] and "Department of Transportation" in le02["qualification"],
         "Connection LE02 changed")
    need(l26["evidence"] == "well-supported" and l20["evidence"] == "plausible" and l18["evidence"] == "hypothesis",
         "a ladder connection changed grade")
    need(l47["evidence"] == "plausible_contested" and l47["contested"], "Connection L47 changed")
    need("null effects on partisan hostility" in l47["qualification"] and "2024 reranking test on X" in l47["qualification"]
         and "four weeks off Facebook in 2018" in l47["qualification"], "Connection L47's readings changed")
    read_a = "Large randomized feed experiments in 2020 and 2023 found effects near zero on partisan hostility."
    read_b = "A 2024 test on X and a break from Facebook found small drops in polarization."
    need(len(read_a.split()) == len(read_b.split()), "the two contested readings differ in length (Rule 01.16)")
    ladder = [
        ("documented", "The Transportation Department had spent 46.6 percent of the infrastructure law’s transportation "
                       "funds by July 31, 2026", "LE02", le02),
        ("well-supported", "Local reporting raises incumbents’ risk of losing office", "L26", l26),
        ("plausible", "Better public services can build earned trust in government", "L20", l20),
        ("plausible_contested", None, "L47", l47),
        ("hypothesis", "Untested: more expert congressional staff may reduce insider influence", "L18", l18),
    ]
    trs = []
    for g, title, cid, rec in ladder:
        t = (f'<p>{e(read_a)}</p><p>{e(read_b)}</p>' if title is None else f"<p>{e(title)}</p>")
        trs.append(f'<tr><th scope="row">{grade_word(g)}</th><td data-k="Our title" class="ttl">{t}</td>'
                   f'<td data-k="The atlas record">{chip("Connection", cid)} “{e(rec["name"])}”</td></tr>')
    body = ('<table class="tb stack"><caption>Five connections in our systems atlas, one at each grade, with the title its '
            'grade allows</caption><thead><tr><th scope="col">Grade</th><th scope="col">Our title</th>'
            f'<th scope="col">The atlas record</th></tr></thead><tbody>{"".join(trs)}</tbody></table>'
            f'<p class="src">Source: {e(ATLAS)}, connections LE02, L26, L20, L47 and L18, snapshot of {SNAP}, United States. '
            'Connection LE02’s record cites the Department of Transportation’s count as of July 31, 2026.</p>')
    book.add("s-13-2-correct", body, rule="13.2", readable=True,
             alt=("A table of five connections from our systems atlas, one at each grade, with the title its grade allows and the "
                  "atlas record beside it, each name in quotation marks. Documented: The Transportation Department had spent "
                  "46.6 percent of the infrastructure law’s transportation funds by July 31, 2026. Well supported: Local "
                  "reporting raises incumbents’ risk of losing office. Plausible: Better public services can build earned trust "
                  "in government, beside the atlas name Better public services build earned trust. Contested: two readings of "
                  "15 words each, one finding effects near zero and one finding small drops. Hypothesis: Untested: more expert "
                  "congressional staff may reduce insider influence."),
             notes="Every grade and every reading from the atlas's connection records. The two contested readings run 15 words "
                   "each (Rule 01.16). The Documented row is a count on the public record in LE02's own record, in record words "
                   "(statistics S1, CD S5).")
    book.log("13.2 correct", "Connection LE02, infrastructure law spending", "D04")
    book.log("13.2 correct", "Connection L26, local reporting", "D01")
    book.log("13.2 correct", "Connection L20, public services and trust", "D04")
    book.log("13.2 correct", "Connection L47, hostile content", "D10")
    book.log("13.2 correct", "Connection L18, congressional expertise", "D04")
    fail = (dnp() + diagram_label("plausible", "some evidence, the atlas’s grade for Connection L20")
            + f'<p class="ct">{e(l20["name"])}</p>'
            + '<p class="ms">How the quality of public services and earned trust in government move together, United States</p>'
            + f'<p class="src">Source: {e(ATLAS)}, connection L20, snapshot of {SNAP}, United States.</p>')
    book.add("s-13-2-failure", fail, rule="13.2",
             alt=(FC + f"A diagram head whose label reads Plausible, some evidence, titled {l20['name']}, with the direct verb "
                  "build and no can or may."),
             notes="Labeled failure: the atlas's name for L20 used as a title; the label is right (CD M3), so it fails on the verb alone.")
    return {
        "id": "13.2",
        "title": "Give the title the verb its evidence grade allows.",
        "rule": [
            "House rule H08 in chapter 02 gives each evidence grade its verb: record words such as “passed” or “stood at” for "
            "documented, a direct verb such as “raises” for well supported, “can” or “may” for plausible, both readings at the "
            "same length for contested, and a label that marks a hypothesis as untested. A title takes the grade of the claim "
            "it states, read from the atlas record or set by Rule 13.1 for a figure from outside the atlas.",
            "The atlas names each connection, a claimed causal link from one of its variables to another, and some names keep a "
            "direct verb at a lower grade, such as “" + l20["name"] + "”, graded plausible. We print such a name in quotation "
            "marks after its typed chip, as the atlas writes it, and write our own title in the verb the grade allows.",
        ],
        "why": {"text": ["The verb carries most of a title’s claim. “Raises” tells a reader that strong studies agree, while “can "
                         "raise” says some evidence points that way, so a verb sized to the grade keeps the claim honest in the "
                         "sentence a reader repeats. Rule 02.16 asks for the same verbs inside a sentence."],
                "basis": "Chapter 02, house rule H08"},
        "correct": {"specimen": "s-13-2-correct",
                    "caption": "Five connections from our systems atlas, one at each grade, each titled with the verb its grade "
                               "allows beside the record it states. The contested link takes both readings at 15 words each."},
        "failure": {"specimen": "s-13-2-failure",
                    "caption": "<strong>Fails Rule 13.2.</strong> The label says plausible, and the title states the link with the "
                               "direct verb “build”, which only well-supported evidence allows."},
        "specs": [
            {"label": "Documented", "value": "Record words: passed, ruled, stood at, reported, had spent"},
            {"label": "Well supported", "value": "A direct verb: raises, lowers"},
            {"label": "Plausible", "value": "“Can” or “may”, once, with no other softener"},
            {"label": "Contested", "value": "Both readings at the same length (Rule 01.16)"},
            {"label": "Hypothesis", "value": "“Untested” in the title’s first words"},
            {"label": "An atlas name", "value": "In quotation marks after its chip, as the atlas writes it"},
            {"label": "Where the grade comes from", "value": "The atlas record the title states, read by script, or Rule 13.1 for an outside figure"},
        ],
        "related": ["01", "02", "14", "15"],
        "builders": ["Read the grade from the record the title states and check the verb against H08’s table before the chart "
                     "ships. A title about a whole loop takes the grade of its least certain step, read from the grades of its "
                     "connections."],
    }


# ===============================================================================================================
# Rule 13.3, one table of grade words
# ===============================================================================================================
GRADE_FIELDS = [
    ("links", "evidence", "connections"),
    ("issues", "grade", "issue records"),
    ("claims", "confidence", "claims"),
    ("reforms.problem", "grade", "evidence of the problem"),
    ("reforms.remedy", "grade", "evidence the remedy works"),
    ("deliveryLog", "evidence_grade", "delivery log cases"),
]


def grade_counts():
    out = Counter()
    for k, l in LINK.items():
        out[("connections", l["evidence"])] += 1
    for k, i in V7["issues"].items():
        out[("issue records", i["grade"])] += 1
    for k, c in V7["claims"].items():
        out[("claims", c["confidence"])] += 1
    for k, r in REFORM.items():
        out[("evidence of the problem", r["problem_evidence"]["grade"])] += 1
        out[("evidence the remedy works", r["remedy_evidence"]["grade"])] += 1
    for r in V7["deliveryLog"]["rows"]:
        out[("delivery log cases", r["evidence_grade"])] += 1
    return out


def rule_13_3(book):
    counts = grade_counts()
    values = {v for (_, v) in counts}
    need(values <= set(GRADE) | {"retired"}, f"the atlas holds a grade value the table lacks: {sorted(values - set(GRADE) - {'retired'})}")
    flagged = sorted(k for k, l in LINK.items() if l["contested"])
    need(flagged == sorted(k for k, l in LINK.items() if l["evidence"] == "plausible_contested"),
         "the contested flag no longer matches plausible_contested")
    mixed = [k for k, i in V7["issues"].items() if (i.get("remedy_note") or "").startswith("Mixed")]
    retired = [k for k, i in V7["issues"].items() if i["grade"] == "retired"]
    need(mixed == ["X16"] and retired == ["I128"], "the Mixed or retired records changed")
    need(not any("not yet tested" in str(x).lower() for (_, x) in counts), "a record now carries “not yet tested”")
    order = [("documented", "Documented", "solid line, record square"), ("well-supported", "Well supported", "solid line"),
             ("plausible", "Plausible", "dashed line"), ("contested", "Contested", "dash and dot"),
             ("hypothesis", "Hypothesis", "dots")]
    keys = {"documented": ["documented"], "well-supported": ["well-supported", "well_supported"], "plausible": ["plausible"],
            "contested": ["plausible_contested", "contested"], "hypothesis": ["hypothesis"]}
    trs = []
    for g, word, drawn in order:
        held = []
        for v in keys[g]:
            per = [(f, counts[(f, v)]) for _, _, f in GRADE_FIELDS if counts.get((f, v))]
            if per:
                held.append(f"<code>{e(v)}</code>: " + ", ".join(f"{n} {f}" for f, n in per))
        if g == "contested":
            held.append(f"the contested flag, on the same {len(flagged)} connections")
        line = line_svg(g, KEY_W) if g != "documented" else rsq() + line_svg(g, KEY_W)
        trs.append(f'<tr><th scope="row"><b>{e(word)}</b></th><td data-k="Key gloss">{e(GRADE[keys[g][0]][1])}</td>'
                   f'<td data-k="Values the atlas holds">{"; ".join(held)}</td>'
                   f'<td data-k="On a connection"><span class="cl"><span class="rw">{line}</span><span>{e(drawn)}</span></span></td></tr>')
    trs.append(f'<tr><th scope="row"><b>Mixed</b></th><td data-k="Key gloss">parts point different ways</td>'
               f'<td data-k="Values the atlas holds">The first word of one remedy note, on {chip("Issue", mixed[0])}</td>'
               f'<td data-k="On a connection">None; printed beside its record</td></tr>')
    trs.append(f'<tr><th scope="row"><b>Retired</b></th><td data-k="Key gloss">a record status, kept out of keys</td>'
               f'<td data-k="Values the atlas holds"><code>retired</code>: 1 issue record, {chip("Issue", retired[0])}</td>'
               f'<td data-k="On a connection">None</td></tr>')
    body = ('<table class="tb stack"><caption>Every grade value our systems atlas holds, with the word a page prints</caption>'
            '<thead><tr><th scope="col">Display word</th><th scope="col">Key gloss</th><th scope="col">Values the atlas holds</th>'
            f'<th scope="col">On a connection</th></tr></thead><tbody>{"".join(trs)}</tbody></table>'
            '<p class="nt">The atlas also defines “not yet tested” for a response no one has evaluated. No record carries it on '
            f'{SNAP}, and it joins this table as its own row before any page prints it.</p>'
            f'<p class="src">Source: {e(ATLAS)}, grade fields of its connections, issue records, claims, reforms and delivery '
            f'log, snapshot of {SNAP}, United States. Counts by script.</p>')
    book.add("s-13-3-correct", body, rule="13.3", readable=True,
             alt=("The mapping table. Each row gives a display word, its gloss for a key, the grade values our systems atlas "
                  "stores with their counts, and how a connection draws it. Documented, on the public record: a solid line with "
                  "the record square. Well supported, strong research evidence, which the atlas spells two ways: a solid line. "
                  "Plausible, some evidence: a dashed line. Contested, evidence disputed, which covers plausible_contested, "
                  "contested and the contested flag: dash and dot. Hypothesis, not yet tested: dots. Mixed, on one issue record, "
                  "and Retired, a record status kept out of keys, draw no line."),
             notes="Every count read from the atlas by script. Key glosses as Rule 12.6's key prints them (the chart system's "
                   "GRADE_TABLE); the line names as Rule 10.10 draws them; plausible_contested as Contested, as the atlas "
                   "concepts mapped it. Tension 8 asked for this table.")
    book.log("13.3 correct", "The atlas's grade fields", "all", level="atlas-wide")
    fail_key = [("well_supported", "solid"), ("well-supported", "solid"), ("plausible_contested", "dashdot"),
                ("Strong", "solid"), ("hypothesis", "dotted")]
    lis = "".join(f'<li><span class="rw">{line_svg({"solid": "documented", "dashdot": "contested", "dotted": "hypothesis"}[t], KEY_W)}'
                  f"<span>{e(w)}</span></span></li>" for w, t in fail_key)
    fail = (dnp() + diagram_label("hypothesis", "not yet tested, the grade of the least certain step")
            + '<p class="ct">How sure each step of the loop is</p><p class="ms">Connections in one loop, by grade</p>'
            + f'<ul class="kl">{lis}</ul>')
    book.add("s-13-3-failure", fail, rule="13.3",
             alt=(FC + "A chart key that lists well_supported and well-supported as two entries, plausible_contested as the "
                  "atlas stores it, a made-up grade called Strong, and hypothesis in lower case, each beside a line sample."),
             notes="Labeled failure: the atlas's stored values printed raw, one grade spelled two ways, a homemade grade word.")
    return {
        "id": "13.3",
        "title": "Print the atlas’s grade words with a plain gloss, from one table.",
        "rule": [
            "Our systems atlas stores its grades in several fields and spells some of them two ways: well-supported on a "
            "connection and well_supported on an issue record, plausible_contested on a connection and contested on a claim. "
            "Every page prints one display word for each grade, from the table in this rule, with a short gloss in a chart key "
            "and the atlas’s own definition the first time a page uses the word. A gloss is a plain phrase that says what the "
            "word means, such as “some evidence” for Plausible.",
            "Two more words sit in the table. Mixed, for a claim whose parts point different ways, prints as the atlas words it, "
            "beside the record it describes. Retired marks an issue record the atlas no longer uses, which is a status, so it "
            "stays out of every grade key.",
        ],
        "why": {"text": ["A reader who meets Well supported in a key and well_supported in a table has to wonder whether they "
                         "mean the same thing. One table gives every page the same word for the same grade, and the gloss hands "
                         "a newcomer the meaning without a trip to the atlas’s methods."],
                "basis": "Our systems atlas’s methods and glossary; the display words and glosses are design judgment"},
        "correct": {"specimen": "s-13-3-correct",
                    "caption": "The mapping table: every grade value our systems atlas holds on " + SNAP + ", with its count, "
                               "the word a page prints, the gloss a key prints and the line a connection draws."},
        "failure": {"specimen": "s-13-3-failure",
                    "caption": "<strong>Fails Rule 13.3.</strong> The key prints the atlas’s stored values, gives one grade two "
                               "spellings and adds Strong, a word that matches no grade."},
        "specs": [
            {"label": "Display words", "value": "Documented, Well supported, Plausible, Contested, Hypothesis, in that order"},
            {"label": "Key glosses", "value": "On the public record; strong research evidence; some evidence; evidence disputed; not yet tested, as Rule 12.6’s key prints them"},
            {"label": "First use", "value": "The atlas glossary’s definition, quoted"},
            {"label": "Contested", "value": "The atlas’s plausible_contested and contested values, and its contested flag"},
            {"label": "Outside the keys", "value": "Mixed beside its record; Retired as a record status"},
        ],
        "related": ["02", "12", "14", "15"],
        "builders": ["Map every grade through one function that reads this table, and stop the build on any value the table "
                     "does not hold, so a new value in the atlas waits until the table names it."],
    }


# ===============================================================================================================
# Rule 13.4, the line code
# ===============================================================================================================
WEAKEST = {"R10": "L53", "R16": "T01", "R3": "L47"}


def loop_block(lid, conceptual=False, words=True):
    """One loop as a list of its steps, each drawn by wire_marks in its grade's line with its sign tag, the atlas's name in
    quotation marks after its chip (Rule 13.2), and the diagram's label: its least certain grade (Rule 13.1)."""
    L = LOOP[lid]
    weak = WEAKEST.get(lid)
    if weak:
        need(weak in L["evidence_summary"] and "weakest" in L["evidence_summary"], f"Loop {lid} no longer names {weak} its weakest step")
    out = ['<div class="lp">']
    if conceptual:
        need(L["closure"].startswith("conceptual"), f"Loop {lid} is no longer conceptual")
        g = L["evidence"].split(";")[0].strip()
        if words:
            out.append(diagram_label(g, "the atlas’s grade for the mechanism, which has no numbered connection"))
        out.append(f'<p class="hed">{chip("Loop", lid)}<span>“{e(L["title"])}”</span></p>')
        out.append(f'<div class="st">{line_svg(None, STEP_W, hollow=True)}<p>Each step, drawn hollow: the atlas gives this '
                   f'loop no numbered connection.</p></div>')
    else:
        g = least_certain(L["links"])
        if words:
            low = [c for c in L["links"] if LINK[c]["evidence"] == g]
            out.append(diagram_label(g, f"{GRADE[g][1]}, the grade of the loop’s least certain step, Connection {low[0]}"))
        out.append(f'<p class="hed">{chip("Loop", lid)}<span>“{e(L["title"])}”</span></p>')
        for cid in L["links"]:
            c = link(cid)
            if words:
                tail = " The atlas names it the loop’s weakest step." if cid == weak else ""
                text = f'{chip("Connection", cid)} “{e(c["name"])}”. {grade_word(c["evidence"])}.{tail}'
            else:
                text = f'{chip("Connection", cid)} “{e(c["name"])}”'
            out.append(f'<div class="st">{line_svg(c["evidence"] if words else "documented", STEP_W, sign=c["polarity"])}<p>{text}</p></div>')
    return "".join(out) + "</div>"


def rule_13_4(book):
    need([LINK[c]["evidence"] for c in LOOP["R10"]["links"]] == ["documented", "well-supported", "plausible", "documented"],
         "Loop R10's grades changed")
    need("weakest" in LOOP["R10"]["evidence"] and "L53" in LOOP["R10"]["evidence_summary"], "Loop R10 no longer names L53 its weakest")
    need([LINK[c]["evidence"] for c in LOOP["R16"]["links"]] == ["well-supported", "hypothesis"], "Loop R16 changed")
    need([LINK[c]["evidence"] for c in LOOP["R3"]["links"]] == ["plausible", "plausible_contested"], "Loop R3 changed")
    need(LOOP["B2"]["closure"] == "conceptual: no complete numbered chain", "Loop B2 changed")
    v = GV
    pl, ct, hy = v["plausible"], v["contested"], v["hypothesis"]
    num = lambda xs: ", ".join(f"{x:g}" for x in xs[:-1]) + f" and {xs[-1]:g}"
    px = lambda xs: ", ".join(f"{x * LW:g}" for x in xs[:-1]) + f" and {xs[-1] * LW:g}"
    body = "".join(loop_block(x) for x in ("R10", "R16", "R3")) + loop_block("B2", conceptual=True)
    body += (f'<p class="src">Source: {e(ATLAS)}, loops R10, R16, R3 and B2 and their connections, snapshot of {SNAP}, '
             'United States. Lines drawn by the atlas build’s own function at 2 px.</p>')
    book.add("s-13-4-correct", body, rule="13.4", readable=True,
             alt=("Four loops from our systems atlas, each with a dark label giving the grade of its least certain step, and each "
                  "step drawn as a short arrow in the line of its grade, with a sign tag, its typed chip, its name in quotation "
                  "marks and its grade word. Loop R10, labeled Plausible: two documented steps, each with the record square, one "
                  "well supported, all solid, and one plausible step, dashed, the loop's weakest. Loop R16, labeled Hypothesis: "
                  "a well-supported solid step and an untested step in dots. Loop R3, labeled Contested: a plausible dashed step "
                  "and a contested step in dash and dot. Loop B2, labeled Well supported: one hollow line, since the atlas gives "
                  "the loop no numbered connection."),
             notes="Every line is the atlas build's wire_marks at 2 px (Rule 10.10's builders line), with the oa.chart.grade "
                   "values the data lead read from it (D3-84); the record square and the hollow line as Gate 1's M1 approved them.")
    book.log("13.4 correct", "Loop R10, safe seats", "D02")
    book.log("13.4 correct", "Loop R16, local news", "D01")
    book.log("13.4 correct", "Loop R3, hostile content", "D10")
    book.log("13.4 correct", "Loop B2, automatic benefits", "D08")
    fail = dnp() + loop_block("R10", words=False)
    book.add("s-13-4-failure", fail, rule="13.4",
             alt=(FC + "Loop R10's four steps, each drawn as a solid arrow with its chip and name, with no label, no grade word "
                  "and no record square, so the plausible step looks as firm as the documented ones."),
             notes="Labeled failure: one solid line for every grade and no grade words.")
    toks = [k for k in ("documented", "wellSupported", "plausible", "contested", "hypothesis", "conceptual.rail", "minRun",
                        "recordSquare") if v["tokens"].get(k)]
    tok = lambda k: f"oa.chart.grade.{k}" if v["tokens"].get(k) else None
    clear = f", stopping {v['clearance']:g} line widths short of the arrowhead"
    specs = [
        {"label": "Documented and Well supported", "value": "Solid", "token": tok("documented")},
        {"label": "Plausible", "value": f"Dashed, {num(pl)} line widths, butt caps: {px(pl)} px on a 2 px line", "token": tok("plausible")},
        {"label": "Contested", "value": f"Dash and dot, {num(ct)} line widths: {px(ct)} px on a 2 px line", "token": tok("contested")},
        {"label": "Hypothesis", "value": f"Round dots {hy[1]:g} line widths apart, {hy[1] * LW:g} px on a 2 px line{clear}", "token": tok("hypothesis")},
        {"label": "Widths and fit", "value": f"Lines at {', '.join(str(x) for x in v['widths'][:-1])} or {v['widths'][-1]} px; each pattern stretched to start and end on ink"},
        {"label": "Hollow line", "value": f"Two {v['rail']} px rails, {v['gap']} line width apart: {2 * v['rail'] + v['gap'] * LW} px across on a 2 px line", "token": tok("conceptual.rail")},
        {"label": "Shortest run", "value": f"{v['min_run']} line widths, {MIN_RUN} px on a 2 px line, key samples included; a shorter step prints its grade in words beside it", "token": tok("minRun")},
        {"label": "Record square", "value": f"{v['square']} px, filled in the label’s ink, inline before the word Documented and nowhere else", "token": tok("recordSquare")},
        {"label": "Beside the event mark", "value": "An event’s shape sits only at the head of an event row, with the figure’s key (Rule 13.11)"},
    ]
    return {
        "id": "13.4",
        "title": "Draw a connection’s grade in the atlas’s line code.",
        "rule": [
            "A connection, the arrow from one variable to another in our systems atlas, takes the line of its own grade, drawn "
            "by the atlas build’s own function as Rule 10.10 sets out: solid for documented and well supported, dashed for "
            "plausible, dash and dot for contested, and dots for a hypothesis. Its grade word prints beside it, and a documented "
            "connection’s label starts with the record square, a filled square that says the public record itself shows the link.",
            "A loop, a chain of connections that returns to where it started, draws each step in its own line, so its least "
            "certain step stands out, and each step of a conceptual loop, one with no complete chain of numbered connections, "
            "draws as a hollow line. The oa.chart.grade tokens hold every number, listed in the Specifications.",
        ],
        "tokens": [f"oa.chart.grade.{k}" for k in toks] + ["oa.color.graphic.essential.onNewsprint"],
        "why": {"text": ["Documented and well supported share the solid line, and the record square tells them apart in gray "
                         "print or on a photocopy, where a key is easy to miss. Drawing each step at its own grade shows a reader "
                         "where a loop is weakest before they read its record."],
                "basis": "Our systems atlas’s line code, with the record square and the hollow line our founder and editor approved in October 2026"},
        "correct": {"specimen": "s-13-4-correct",
                    "caption": "Four loops from our systems atlas, each step in the line of its grade with its word, under a label "
                               "that gives the loop’s least certain grade. The record square marks Loop R10’s two documented steps, "
                               "Loop R16 closes on an untested step, and Loop B2’s step is hollow because the atlas gives it no "
                               "numbered connection."},
        "failure": {"specimen": "s-13-4-failure",
                    "caption": "<strong>Fails Rule 13.4.</strong> Every step of Loop R10 is solid and none carries its grade, so "
                               "the plausible step the atlas calls its weakest looks as firm as the documented ones."},
        "specs": [s if s.get("token") else {k: x for k, x in s.items() if k != "token"} for s in specs],
        "related": ["10", "15", "21"],
        "builders": ["Take each step’s grade from its own connection record and draw the line with the atlas build’s "
                     "<code>wire_marks</code>, so the pattern fits the line’s length and starts and ends on ink. Read every "
                     "number from the oa.chart.grade tokens."],
    }


# ===============================================================================================================
# Rule 13.5, four properties apart
# ===============================================================================================================
def rule_13_5(book):
    r = REFORM["R-30"]
    need(r["effects"] == {"DQ": "+S delayed", "GE": "0", "EP": "+M", "EQ": "+M renter-owner"}, "Reform R-30's effects changed")
    need(r["effects_confidence"] == "high where binding; medium for US statutes", "Reform R-30's confidence changed")
    need(r["remedy_evidence"]["grade"] == "plausible" and r["targets"] == ["L39", "A5", "LE17"], "Reform R-30's grade or targets changed")
    l39, le17 = link("L39"), link("LE17")
    need((l39["evidence"], l39["delay"], le17["evidence"], le17["delay"]) == ("well-supported", "L", "well-supported", "M"),
         "Connection L39 or LE17 changed")
    why_one = V7["outcomes"]["why_not_one_number"]
    q2 = ("The four outcome families use different units. A reform can improve one while imposing a cost on another, and the "
          "evidence behind each estimate differs in quality.")
    need(why_one.startswith(q2), "the atlas's reason for no single score changed")
    rowsx = []
    for fam in ("DQ", "GE", "EP", "EQ"):
        v = r["effects"][fam]
        code = v.split(" ")[0]
        qual = v[len(code):].strip()
        words = EFFECT_WORDS[code] + (f", {qual}" if qual else "")
        rowsx.append(f'<div class="fxr"><span class="fn">{e(FAMILY[fam])}</span>{pips_svg(code)}'
                     f'<span><b>{e(code)}</b> {e(words)}</span></div>')
    targets = "".join(
        f'<div class="st wt">{line_svg(c["evidence"], 148, delay=c["delay"], sign=c["polarity"], target=True)}'
        f'<p>{chip("Connection", cid)} “{e(c["name"])}”. Delay {c["delay"]}, {DELAY[c["delay"]][1]}.</p></div>'
        for cid, c in (("L39", l39), ("LE17", le17)))
    body = (diagram_label("plausible", "some evidence, the grade of the evidence that the reform works")
            + f'<p class="hed">{chip("Reform", "R-30")}<span>“{e(r["title"])}”</span></p>'
            f'<div class="blk"><p class="k">Effect size, by outcome family</p>{"".join(rowsx)}</div>'
            f'<div class="blk"><p class="k">Uncertainty: how sure the atlas is of those sizes</p><p>“{e(r["effects_confidence"])}”</p></div>'
            f'<div class="blk"><p class="k">Delay, at each connection it targets</p>{targets}'
            f'<p class="nt">Reform R-30 acts where the marks turn red. Its third target is {chip("Variable", "A5", ",")} '
            f'{e(lc(node_title("A5")))}.</p></div>'
            f'<p class="src">Source: {e(ATLAS)}, reform R-30 and connections L39 and LE17, snapshot of {SNAP}, United States. '
            'The atlas adds no effects into one score.</p>')
    book.add("s-13-5-correct", body, rule="13.5", readable=True,
             alt=(f"Reform R-30, {r['title']}, with four properties in four places. Its label reads Plausible, the grade of the "
                  "evidence that it works. Effect size: one row for each outcome family, with pips beside a zero line and the "
                  "atlas's code and words: Quality of democracy +S, small positive, delayed; Government efficacy 0, no expected "
                  "effect, drawn as a bar on the zero line; Economic performance +M, moderate positive; Income and wealth "
                  "equality +M, moderate positive, renter-owner. Uncertainty, in the atlas's words: high where binding; medium "
                  f"for US statutes. Delay: the two connections it targets drawn in red, Connection L39, {l39['name']}, with "
                  f"three ticks for over 10 years, and Connection LE17, {le17['name']}, with two ticks for 2 to 10 years. A note "
                  "says the reform acts where the marks turn red and names its third target, Variable A5, housing scarcity."),
             notes="Pips and the zero bar as Gate 1's M4 effect mark draws them; qualifiers kept as the atlas writes them; no total. "
                   "The targets take Rule 12.5's red target, the plate's one working red, drawn by wire_marks at the 6 px sizes "
                   "with a 4 px red line on a 6 px Charcoal case (brand S4, statistics S11).")
    book.log("13.5 correct", "Reform R-30, homes allowed by right", "D09")
    fail = (dnp() + f'<p class="hed">{chip("Reform", "R-30")}<span>“{e(r["title"])}”</span></p>'
            '<div class="blk"><p class="k">Impact score</p><p class="ct">+5</p>'
            '<p class="ms">Four outcome families added together</p></div>'
            '<div class="blk"><p class="k">Strength of evidence</p><svg class="ln" viewBox="0 0 200 16" width="200" height="16" '
            'aria-hidden="true" focusable="false"><path class="thick" d="M1 8H199"/></svg></div>')
    book.add("s-13-5-failure", fail, rule="13.5",
             alt=(FC + "Reform R-30 with an impact score of +5, the four outcome families added together, and a thick bar for the "
                  "strength of its evidence. No delay appears."),
             notes="Labeled failure: a total across outcome families, a bar's thickness for a grade, delay left out.")
    return {
        "id": "13.5",
        "title": "Keep grade, effect size, uncertainty and delay apart, each with its own mark.",
        "rule": [
            "Four properties of a claim keep their own marks and words. The evidence grade takes the line of Rule 13.4 or the "
            "grade word. A reform’s effect size prints as the atlas’s ordinal code, a rank of small, moderate or large with no "
            "measured amount, in one row for each outcome family, one of the four groups of results the atlas judges reforms by. "
            "Uncertainty prints in the atlas’s own words, or for a survey figure as its margin of error, the range around the "
            "figure that sampling allows. Delay, the time an effect takes, draws as ticks on the connection.",
            "No mark carries two properties, and the four outcome families never add into one score. Our systems atlas gives the "
            "reason: “" + q2 + "”",
        ],
        "tokens": ["oa.color.graphic.essential.onNewsprint", "oa.color.data.emphasisRed.onNewsprint"],
        "why": {"text": ["Each property answers its own question: how strong the evidence is, how large the change, how sure the "
                         "atlas is of that size, and how soon it comes. A mark that carries two at once, such as a thicker line "
                         "for stronger evidence, lets a large effect on thin evidence pass for a small one on strong evidence."],
                "basis": "Our systems atlas’s methods and outcomes, with the effect and delay marks our founder and editor approved in October 2026"},
        "correct": {"specimen": "s-13-5-correct",
                    "caption": "Reform R-30 with each property in its own place: the grade of the evidence that it works in the "
                               "label, its effect on each outcome family with the atlas’s qualifiers kept, the atlas’s confidence in "
                               "its own words, and the delay of each connection it targets, marked in Rule 12.5’s red."},
        "failure": {"specimen": "s-13-5-failure",
                    "caption": "<strong>Fails Rule 13.5.</strong> The card adds four codes into one score of +5, draws the grade "
                               "as a bar’s thickness and leaves the delay out."},
        "specs": [
            {"label": "Grade", "value": "The line of Rule 13.4, or the grade word"},
            {"label": "Effect size", "value": "The atlas’s code and words, one row per outcome family: one to three pips right of the zero line for a gain, left for a cost, and a bar on the zero line for no expected effect"},
            {"label": "Uncertainty", "value": "The atlas’s words, quoted; for a survey figure, its margin of error at the publisher’s stated confidence, 90 percent for the Census Bureau and the Bureau of Labor Statistics, drawn as an interval"},
            {"label": "A gap between two survey figures", "value": "Counts only where it passes the margin of error of the gap itself; chapter 14 sets when a chart may rank survey figures"},
            {"label": "Delay", "value": "One, two or three ticks for under 2 years, 2 to 10 years and over 10 years, with the words"},
            {"label": "Where a reform acts", "value": "Its target connections in Rule 12.5’s red, at 4 px on a 1 px Charcoal edge and never at 2 px, with a note that names the reform",
             "token": "oa.color.data.emphasisRed.onNewsprint"},
            {"label": "Never", "value": "A total across families, or a width or darkness for a grade"},
        ],
        "related": ["12", "14", "15", "21"],
        "builders": ["Print each family’s code from the reform’s effects record with its qualifier, such as “+S delayed”, and "
                     "write the families as Quality of democracy, Government efficacy, Economic performance, and Income and "
                     "wealth equality."],
    }


# ===============================================================================================================
# Rule 13.6, the six parts of a source line
# ===============================================================================================================
def rule_13_6(book):
    sc = sidecar("fred-payrolls-monthly-change")
    line = sc["printed_source_line"]
    parts = [
        ("Publisher", "U.S. Bureau of Labor Statistics"),
        ("Title or table", "Current Employment Statistics, all nonfarm employees, monthly change, seasonally adjusted"),
        ("Observation period", "January 2022 to September 2026"),
        ("Geography", "United States"),
        ("The copy we read", "via FRED, Federal Reserve Bank of St. Louis"),
        ("Date retrieved", "Retrieved November 6, 2026."),
        ("Qualification", "August and September 2026 are preliminary and will be revised."),
    ]
    pos = -1
    for _, words in parts:
        i = line.find(words)
        need(i > pos, f"the payroll source line no longer holds “{words}” in H04's order")
        pos = i
    data = rows("fred-payrolls-monthly-change")
    last = data[-1]
    need((last["month"], last["status"]) == ("2026-09", "preliminary") and round(float(last["avg3_thousands"])) == 51,
         "the payroll file's last month changed")
    title = "The three-month average of monthly job change stood at 51,000 in September 2026, a preliminary figure"
    trs = "".join(f'<tr><th scope="row">{e(k)}</th><td data-k="Words in this line">{e(w)}</td></tr>' for k, w in parts)
    atlas_line = (f"Source: {ATLAS}, connection L02, political spending and policy toward donors, snapshot of {SNAP}, United "
                  "States. Retrieved November 11, 2026. Graded plausible on a 2016 field experiment in which congressional "
                  "offices granted meetings more often to people identified as donors.")
    need("2016 field experiment" in link("L02")["qualification"] and "donors" in link("L02")["qualification"], "L02's qualification changed")
    body = (chart_head("Finding", GL_BLS, title,
                       "Monthly change in jobs, thousands, seasonally adjusted, United States, January 2022 to September 2026",
                       notes=["Seasonally adjusted: with the swings that repeat every year, such as holiday hiring, taken out."],
                       source=line)
            + '<table class="tb stack blk"><caption>The same line, part by part, in H04’s order</caption><thead><tr>'
              f'<th scope="col">Part</th><th scope="col">Words in this line</th></tr></thead><tbody>{trs}</tbody></table>'
            + f'<div class="blk"><p class="k">A value from our systems atlas, in the same order</p><p class="src">{e(atlas_line)}</p></div>')
    book.add("s-13-6-correct", body, rule="13.6", readable=True,
             alt=(f"A jobs chart's head and foot: the grade line {GL_BLS}, the title {title}, its measure line, a note that says "
                  f"what seasonally adjusted means, and the source line, {line} A table then takes the line apart: publisher, "
                  "title or table, observation period, geography, the copy we read, date retrieved and qualification. Under it, "
                  "a source line for a value from our systems atlas follows the same order."),
             notes="The source line is the engineer's sidecar printed_source_line for fred-payrolls-monthly-change, read by "
                   "script, never retyped. The title is level and counts no drops (D3-87, statistics M4); the three-month "
                   "average, 50.7 thousand, is read from the same file.")
    book.log("13.6 correct", "Monthly payroll change (BLS via FRED)", "D07")
    fail = dnp() + chart_head("Finding", GL_BLS, title, "Monthly change in jobs, thousands", source="Source: FRED data.")
    book.add("s-13-6-failure", fail, rule="13.6",
             alt=FC + f"The same jobs chart's head, titled {title}, with a short measure line and the source line Source: FRED data.",
             notes="Labeled failure: a copy named in place of the publisher; no table, period, geography, date or qualification. "
                   "The grade line is right, so the plate fails on its source line alone.")
    return {
        "id": "13.6",
        "title": "Write the source line in its six parts, in order.",
        "rule": [
            "House rule H04 in chapter 02 sets the source line’s six parts and their order: the publisher, the title or table, "
            "the observation period, the geography, the date retrieved, and the qualification, the one caveat a reader most "
            "needs. The observation period is the time the numbers describe, and the date retrieved is the day we read the file. "
            "A chart prints the line under its notes, starting “Source:”, and a chart with two sources gives each its six parts.",
            "A copy, a secondary source, an advocacy group and a value from our systems atlas each add a few words, which the "
            "Specifications set out.",
        ],
        "tokens": ["oa.type.caption"],
        "why": {"text": ["A reader who doubts a number should be able to find it in a minute. The six parts in a fixed order tell "
                         "them whose table to open, which rows, which years and places, and what the publisher says to watch for."],
                "basis": "Chapter 02, house rule H04"},
        "correct": {"specimen": "s-13-6-correct",
                    "caption": "A jobs chart’s source line, taken apart into its parts, with the copy we read named after the "
                               "geography. A line for a value from our systems atlas follows in the same order."},
        "failure": {"specimen": "s-13-6-failure",
                    "caption": "<strong>Fails Rule 13.6.</strong> The line names the database that copies the numbers and drops "
                               "the publisher, the period, the date we read them and the warning that the last two months will change."},
        "specs": [
            {"label": "Order", "value": "Publisher, title or table, observation period, geography, date retrieved, qualification"},
            {"label": "A copy", "value": "The publisher first, then “via” and the copy’s name after the geography, such as FRED, the St. Louis Fed’s database"},
            {"label": "A secondary source", "value": "One that compiles other people’s records, with “a secondary source” after its name"},
            {"label": "An advocacy group", "value": "Named as one, as in “Unite America, an advocacy group”"},
            {"label": "An atlas value", "value": "Oath & Action’s systems atlas, Who Do They Answer To?, the record, snapshot of " + SNAP},
            {"label": "Place", "value": "Under the chart’s notes, in the caption style, starting “Source:”", "token": "oa.type.caption"},
        ],
        "related": ["02", "14"],
        "builders": ["Print the line from the dataset’s own record, its printed source line, and never retype it, so the chart "
                     "check can compare the two word for word."],
    }


# ===============================================================================================================
# Rule 13.7, period, vintage and one window
# ===============================================================================================================
KIT_SPECS = {}   # chart specs this chapter's plates name (contract C7), written beside the fragments


def cp_spec(cid, group, title, alt, years=None):
    """A small line chart of the Supplemental Poverty Measure for one group, drawn by the kit's line-event-notes form in the
    guide (contract C7). Both charts in a set share the window and the 0 to 25 percent scale."""
    sc = sidecar("census-spm-child-poverty")
    where = {"measure": "spm", "age_group": group, "vintage": "p60-290"}
    if years:
        where["year"] = years
    KIT_SPECS[cid] = {
        "kit": 1, "id": cid, "form": "line-event-notes", "family": "change-over-time", "tier": "core",
        "dataset": "census-spm-child-poverty", "where": where, "sort": [{"field": "year", "order": "asc"}],
        "reader_question": "How has poverty under the Supplemental Poverty Measure changed since 2009?",
        "evidence": "finding", "evidence_label": "Finding", "grade_line": GL_CENSUS, "title": title,
        "measure_line": f"{'Children under 18' if group == 'under_18' else 'All people'} in poverty, Supplemental Poverty Measure, "
                        f"percent, United States, {years[0] if years else 2009} to 2025",
        "source_line": sc["printed_source_line"], "illustrative": False, "alt": alt,
        "table": {"caption": "Percent in poverty, Supplemental Poverty Measure", "columns": [
            {"field": "year", "label": "Year", "format": "year", "row_header": True},
            {"field": "series_variant", "label": "Estimate", "format": "text", "words": {
                "standard": "One estimate", "redesigned_income_questions": "Redesigned income questions",
                "traditional_income_questions": "Traditional income questions", "legacy_processing": "Earlier processing system",
                "updated_processing": "Updated processing system", "corrected_2026_method": "Method used from 2019 on",
                "original_2011_method": "Original 2011 method"}},
            {"field": "percent", "label": "Percent", "format": "number:1"},
            {"field": "moe_pct", "label": "Margin of error, points (90%)", "format": "number:1"}]},
        "chart_notes": ["The line breaks in 2013, 2017 and 2019, where the Census Bureau changed its survey or method."],
        "phone": "same", "domain": "D08", "states": [],
        "encode": {"x": "year", "y": "percent", "break": "comparable_with"},
        "labels": {"break_end": "earlier", "break_start": "later", "y_max": 25},
        "show": ["evidence", "title", "measure", "chart"],
        "notes_internal": "Chapter 13, Rule 13.7 (CD S3, brand S5): one of a pair drawn in one window on one scale.",
    }
    return f'<div data-oa-chart="{cid}"></div>'


def rule_13_7(book):
    sc = sidecar("census-spm-child-poverty")
    cp = {(r["year"], r["age_group"], r["vintage"]): r["percent"] for r in rows("census-spm-child-poverty")
          if r["measure"] == "spm" and r["series_variant"] == "standard"}
    yrs = sorted({r["year"] for r in rows("census-spm-child-poverty") if r["measure"] == "spm" and r["vintage"] == "p60-290"})
    need((yrs[0], yrs[-1]) == ("2009", "2025"), "the SPM table no longer runs 2009 to 2025")
    need("released September 15, 2026" in sc["vintage"] and "released September 9, 2025" in sc["vintage"], "release dates changed")
    pair = [(y, cp[(y, "under_18", "p60-287")], cp[(y, "under_18", "p60-290")]) for y in ("2020", "2021", "2024")]
    need(pair == [("2020", "9.7", "9.6"), ("2021", "5.2", "5.1"), ("2024", "13.4", "13.5")], "the revision values changed")
    all25 = cp[("2025", "all_ages", "p60-290")]
    need(all25 == "13.1", "the all-ages 2025 rate changed")
    both_line, how = cp_source("both")
    before_line = sc["source_line_variants"]["source_line_first_published"]
    old_b = "Rates as first published; the Bureau revised 2019 to 2024 in August 2026."
    if old_b in before_line:
        before_line = before_line.replace(old_b, "Rates before the Bureau’s August 2026 correction to the poverty thresholds.")
    ch_title, all_title = "Child poverty stood at 13.4 percent in 2025", f"Poverty among all people stood at {all25} percent in 2025"
    # the kit prints each chart's head from its spec (label, grade line, title, measure line), so its drawing is named by the
    # title above it; a head written here beside a chart-only figure left the drawing's label pointing at nothing
    a = cp_spec("s-13-7-children", "under_18", ch_title,
                 "Line chart of child poverty under the Supplemental Poverty Measure, 2009 to 2025, on a scale that starts at 0, "
                 "breaking where the Census Bureau changed its method; it stood at 13.4 percent in 2025.")
    b = cp_spec("s-13-7-all", "all_ages", all_title,
                 f"Line chart of poverty among all people under the Supplemental Poverty Measure, 2009 to 2025, on the same scale "
                 f"and window, breaking where the method changed; it stood at {all25} percent in 2025.")
    trs = "".join(f'<tr><th scope="row">{y}</th><td class="num" data-k="Before the revision: P60-287, September 9, 2025">{p}</td>'
                  f'<td class="num" data-k="Current release: P60-290, September 15, 2026">{c}</td></tr>' for y, p, c in pair)
    body = (f'<div class="fx two"><div>{a}</div><div>{b}</div></div>'
            '<p class="nt">Both charts run 2009 to 2025, every year in the Census Bureau’s table of this measure, on one scale. '
            'The figures show how much poverty changed. Tying a change to a policy takes a study of its own.</p>'
            f'<p class="src">{e(both_line)}</p>'
            '<table class="tb stack blk"><caption>Children in poverty, percent, in the two releases</caption><thead><tr>'
            '<th scope="col">Year</th><th scope="col">Before the revision: P60-287, September 9, 2025</th>'
            f'<th scope="col">Current release: P60-290, September 15, 2026</th></tr></thead><tbody>{trs}</tbody></table>'
            f'<p class="src">{e(before_line)}</p>')
    book.add("s-13-7-correct", body, rule="13.7", readable=True,
             alt=(f"Two charts shown together, each a chart head over a small line chart in one window, 2009 to 2025, on one scale: "
                  f"{ch_title}, and {all_title}. A note gives the shared window and its reason and says that tying a change to a "
                  "policy takes a study of its own. The source line names children under 18 and all people and the current "
                  "release. A table sets the two releases side by side for children: 2020, 9.7 before the revision and 9.6 now; "
                  "2021, 5.2 and 5.1; 2024, 13.4 and 13.5."),
             notes=f"Rows from the engineer's census-spm-child-poverty file; the pair's source line from the {how}; the earlier "
                   "release's line from the sidecar's variant, its qualification as statistics M3 gives it. The two charts are "
                   "the kit's line-event-notes form through the guide hook (contract C7).")
    book.log("13.7 correct", "Child poverty releases (Census P60-287 and P60-290)", "D08")
    fb = chart_head("Finding", GL_CENSUS,
                    f"Child poverty fell from {pair[0][1]} percent in 2020 to {pair[1][1]} percent in 2021, then rose to {pair[2][2]} percent in 2024",
                    "Children in poverty, percent")
    fc = cp_spec("s-13-7-fail-all", "all_ages", all_title,
                  "Line chart of poverty among all people under the Supplemental Poverty Measure, 2017 to 2025.",
                  years=[str(y) for y in range(2017, 2026)])
    fail = dnp() + f'<div class="fx two"><div>{fb}</div><div>{fc}</div></div>'
    book.add("s-13-7-failure", fail, rule="13.7",
             alt=(FC + f"Two charts side by side. The first is titled Child poverty fell from {pair[0][1]} percent in 2020 to "
                  f"{pair[1][1]} percent in 2021, then rose to {pair[2][2]} percent in 2024, with no period or release named. "
                  "The second, beside it, draws a line that starts in 2017."),
             notes="Labeled failure: 2020 and 2021 from the earlier release beside 2024 from the current one, with no release "
                   "named, and two windows in one set.")
    return {
        "id": "13.7",
        "title": "Print the period and the vintage, and give charts shown together one window.",
        "rule": [
            "The measure line names the observation period, such as 2009 to 2025. Where a publisher revises its figures, the "
            "chart also names the vintage, the release its figures come from, and marks any figure the publisher calls "
            "preliminary. The Census Bureau’s release of September 15, 2026 carries corrected poverty thresholds for 2019 to 2024 "
            "and new weights for 2024, so a chart of those years names that release.",
            "Charts shown together share one time window, printed once with its reason, and house rule H09 holds: “No chart or "
            "sentence splits a period at an inauguration date.” When a publisher revises a figure a published chart shows, the "
            "chart takes the new release and a dated update line that names it; a correction note (Rule 13.13) is for our own errors.",
        ],
        "why": {"text": ["A reader who compares our chart with an older report may find another number for the same year and "
                         "decide one of us made a mistake. The release named on the chart answers that before they ask, and one "
                         "window lets a reader compare charts set side by side."],
                "basis": "Chapter 02, house rule H09, and the Census Bureau’s own revision notes"},
        "correct": {"specimen": "s-13-7-correct",
                    "caption": "Two charts shown together in one window and on one scale, with the reason and the release named "
                               "under them. The table shows the revision that makes the release matter."},
        "failure": {"specimen": "s-13-7-failure",
                    "caption": "<strong>Fails Rule 13.7.</strong> The title takes 2020 and 2021 from the earlier release and 2024 "
                               "from the current one without naming either, and the chart beside it starts in another year."},
        "specs": [
            {"label": "Period", "value": "In the measure line, with months in words"},
            {"label": "Vintage", "value": "The release’s name and date, where the publisher revises its figures"},
            {"label": "Preliminary figures", "value": "Named in the qualification and marked on the chart"},
            {"label": "One window", "value": "The same first and last period and the same scale on every chart in a set, with its reason, printed once"},
            {"label": "A publisher’s revision", "value": "The new release, and an update line with its date and the release’s name"},
            {"label": "Inauguration dates", "value": "No chart or sentence splits a period at one (H09)"},
        ],
        "related": ["02", "14"],
        "builders": ["Freeze each dataset with its release and the date we read it, and print both from that record. When a "
                     "publisher revises, rebuild every chart in the set from the new release on one day, and name that release "
                     "on each chart."],
    }


# ===============================================================================================================
# Rule 13.8, the Illustrative label beside the item
# ===============================================================================================================
def rule_13_8(book):
    n = V7["numbers"][2]
    need(n["figure"] == "$35" and "Medicare Part D" in n["caption"] and "since January 2023" in n["caption"]
         and "Inflation Reduction Act" in n["caption"] and n["verified_status"] == f"checked {SNAP}", "the atlas's insulin figure changed")
    src = (f"Source: {ATLAS}, headline figure on the Medicare insulin cap, in force since January 2023, United States. "
           f"Checked {SNAP}. The cap covers people with Medicare Part D drug coverage.")
    who = "Ruth Okafor, 71, Alder County"
    quote = "“I check each fall that my insulin is still on my plan’s list.”"
    card = lambda label: (f'<div class="card"><p class="hl">Medicare caps what Part\u00a0D enrollees pay for each covered insulin at $35 a month</p>'
                          '<p>The cap has applied since January 2023, under the Inflation Reduction Act.</p>'
                          f'<div class="blk"><p class="qs">{e(quote)}</p><p class="by">{e(who)} {label}</p></div>'
                          f'<p class="src">{e(src)}</p>')
    body = card(ill()) + "</div>"
    book.add("s-13-8-correct", body, rule="13.8", readable=True, illustrative=True, width=360,
             alt=("A story card. Its headline, Medicare caps what Part D enrollees pay for each covered insulin at $35 a month, "
                  "and the line under it report a real rule, with its source line. An invented reader, Ruth Okafor, 71, of Alder "
                  "County, says she checks each fall that her insulin is still on her plan’s list, with the Illustrative label "
                  "beside her name."),
             notes="The rule and its dates from the atlas's headline figures (checked October 15, 2026); the reader, her words "
                   "and Alder County are invented. Lora Italic for her words (DR-47).")
    book.log("13.8 correct", "The Medicare insulin cap", "D09")
    fail = dnp() + card("") + '<p class="foot">Some people and quotes in our pieces are illustrative.</p></div>'
    book.add("s-13-8-failure", fail, rule="13.8", width=360,
             alt=(FC + "The same story card with the invented reader and her words unlabeled, and a note at the foot that says "
                  "some people and quotes in our pieces are illustrative."),
             notes="Labeled failure: one general note at the foot in place of a label beside the invented reader. The caption "
                   "names her as invented, so the plate itself carries no label (the failure it shows).")
    return {
        "id": "13.8",
        "title": "Label an invented item Illustrative, beside the item.",
        "rule": [
            "House rule H03 puts the word Illustrative beside every invented person, quote, place or figure a reader could take "
            "for real. A chart drawn from invented numbers carries “Illustrative data” beside its top edge, where a reader sees "
            "it before the numbers. When a piece mixes real and invented items, each invented item carries its own label and the "
            "real ones keep their sources. When every item in a piece is invented, one label at its head covers them all.",
            "An invented bill takes a number from the ranges Rule 11.1 sets, from H.99001 and S.99002 up, which no legislature "
            "assigns, and an invented place takes a name we keep for examples, such as Alder County.",
        ],
        "why": {"text": ["Many of our pieces set real and invented items side by side. A label beside each invented item tells "
                         "a reader which is which at the moment they read it, while a note at the foot of a page arrives after "
                         "they have believed what came before it."],
                "basis": "Chapter 02, house rule H03"},
        "correct": {"specimen": "s-13-8-correct",
                    "caption": "A story card that mixes a real rule with an invented reader. The rule keeps its source, and the "
                               "label sits beside the invented reader and her words."},
        "failure": {"specimen": "s-13-8-failure",
                    "caption": "<strong>Fails Rule 13.8.</strong> One note at the foot covers the card, so Ruth Okafor, an invented "
                               "reader, and her words sit beside a real rule with nothing to set them apart."},
        "specs": [
            {"label": "Beside the item", "value": "Illustrative, in the label style, right after the invented name, quote, place or figure", "token": "oa.type.label"},
            {"label": "A chart", "value": "“Illustrative data” beside its top edge"},
            {"label": "Everything invented", "value": "One label at the head of the piece"},
            {"label": "Invented bills", "value": "Numbers from Rule 11.1’s ranges"},
            {"label": "Invented places", "value": "Names kept for examples, such as Alder County"},
        ],
        "related": ["02", "11", "16"],
        "builders": ["Keep a flag on every invented item in a piece’s data and print the label from that flag, so a label cannot "
                     "drift away from its item when the layout changes."],
    }


# ===============================================================================================================
# Rule 13.9, typed chips
# ===============================================================================================================
def rule_13_9(book):
    both = sorted(set(NODE) & set(LOOP))
    need(both == ["B2", "B3", "B4", "B5"], f"the IDs shared by variables and loops changed: {both}")
    need("R1" in LOOP and "R-01" in REFORM, "Loop R1 or Reform R-01 is missing")
    l46 = link("L46")
    need((l46["from"], l46["to"]) == ("B4", "B6"), "Connection L46 changed")
    need("C3" in [x for pair in LOOP["B4"]["chain"] for x in pair[:1]], "Loop B4 no longer runs through Variable C3")
    need(l46["evidence"] == "plausible", "Connection L46's grade changed; its verb must follow (Rule 13.2)")
    s1 = (f'<p>{chip("Variable", "B4")}, {e(lc(node_title("B4")))}, can raise {chip("Variable", "B6")}, {e(lc(node_title("B6")))}, '
          f'through {chip("Connection", "L46")}.</p>')
    s2 = (f'<p class="blk">{chip("Loop", "B4")}, {e(lc(LOOP["B4"]["title"]))}, runs through {chip("Variable", "C3")}, '
          f'{e(lc(node_title("C3")))}.</p>')
    s3 = (f'<p class="blk">{chip("Loop", "R1")}, {e(lc(LOOP["R1"]["title"]))}, and {chip("Reform", "R-01")}, '
          f'{e(lc(REFORM["R-01"]["title"]))}, are separate records.</p>')
    body = s1 + s2 + s3 + f'<p class="src">Source: {e(ATLAS)}, the records named, snapshot of {SNAP}.</p>'
    book.add("s-13-9-correct", body, rule="13.9", readable=True,
             alt=(f"Three sentences, each atlas ID in its typed chip with the record's name after it. Variable B4, "
                  f"{lc(node_title('B4'))}, can raise Variable B6, {lc(node_title('B6'))}, through Connection L46. Loop B4, "
                  f"{lc(LOOP['B4']['title'])}, runs through Variable C3, {lc(node_title('C3'))}. Loop R1, "
                  f"{lc(LOOP['R1']['title'])}, and Reform R-01, {lc(REFORM['R-01']['title'])}, are separate records."),
             notes="Chips as Rule 18.24 builds them (c-18-id-chip); every ID and name read from the atlas; B2 to B5 are the "
                   "IDs variables and loops share.")
    book.log("13.9 correct", "IDs the atlas shares across kinds", "all", level="atlas-wide")
    fail = dnp() + '<p>When B4 rises, B6 can rise with it. B4 runs through C3, and R1 explains why R-01 matters.</p>'
    book.add("s-13-9-failure", fail, rule="13.9",
             alt=FC + "A sentence of bare codes: When B4 rises, B6 can rise with it. B4 runs through C3, and R1 explains why R-01 matters.",
             notes="Labeled failure: bare atlas IDs, two of them the same code for different kinds of record.")
    return {
        "id": "13.9",
        "title": "Name every atlas ID in its typed chip.",
        "rule": [
            "Our systems atlas gives each record a short ID, and some IDs repeat across kinds of record. The code B4 names both "
            "Variable B4 and Loop B4, B2, B3 and B5 repeat the same way, and Loop R1 sits one hyphen from Reform R-01. Every "
            "atlas ID we "
            "print sits in a typed chip, the outlined label that holds the kind of record and its ID together, such as Variable "
            "B4 or Loop B4, built as Rule 18.24 sets out. The first time a page names a record, its name follows the chip, as "
            "house rule H11 asks.",
            "The kind word comes from the record’s place in the atlas, and the build checks every chip’s ID against the atlas "
            "before a page ships. In a source line, the kind word in plain text does the chip’s job, as in “connection L02”.",
        ],
        "tokens": ["oa.type.dataLabel", "oa.color.border.strong.onNewsprint"],
        "why": {"text": ["A bare B4 could mean hostility toward the other party or the loop in which electoral consequences can "
                         "improve public performance, and the reader cannot tell which. The kind word settles it, and the chip keeps the word and the ID "
                         "on one line."],
                "basis": "Chapter 02, house rule H11, and Rule 18.24"},
        "correct": {"specimen": "s-13-9-correct",
                    "caption": "Three sentences that name records whose IDs collide, each ID in its chip with the record’s name "
                               "after it."},
        "failure": {"specimen": "s-13-9-failure",
                    "caption": "<strong>Fails Rule 13.9.</strong> Bare codes leave the reader to guess that the first B4 is a "
                               "variable and the second a loop, and that R1 and R-01 are different records."},
        "specs": [
            {"label": "Chip", "value": "The kind word and the ID in one outlined label, as Rule 18.24 builds it", "token": "oa.type.dataLabel"},
            {"label": "Kind words", "value": "Variable, Connection, Loop, Reform, Issue, Claim, Domain, Route, Rule change and Delivery case"},
            {"label": "In a source line", "value": "The kind word in plain text before the ID, as in “connection L02” or “delivery case DL06”"},
            {"label": "First use", "value": "The record’s name after the chip"},
            {"label": "The ID", "value": "As the atlas writes it, with an ASCII hyphen, held on one line"},
            {"label": "Check", "value": "Every ID matched against the atlas before the page ships"},
        ],
        "related": ["02", "18", "10", "21"],
        "builders": ["Write each chip from the record’s kind in the atlas, and let the build’s atlas check fail any chip whose "
                     "ID the atlas does not hold."],
    }


# ===============================================================================================================
# Rule 13.10, dates on what can change
# ===============================================================================================================
def route_counts():
    entries = [x for r in REFORM.values() for x in r["routes"]]
    return len(entries), sum(1 for x in entries if x.get("checked"))


def rule_13_10(book):
    total, dated = route_counts()
    need((total, dated) == (126, 13), f"route entries changed: {total} with {dated} dated")
    r = REFORM["R-19"]
    need([(x["route"], x["feasibility"], x["checked"]) for x in r["routes"]]
         == [("ENF", "medium", None), ("FS", "high", SNAP_ISO), ("SS", "high", None)], "Reform R-19's routes changed")
    need(r["status"]["text"].startswith(f"Partly in place as of {SNAP}.") and r["status"]["checked"] == SNAP_ISO,
         "Reform R-19's status changed")
    need(GLOSS["Snapshot"].startswith(f"The dated state of the research behind the Atlas, most recently {SNAP}."), "the snapshot definition changed")
    order = ["FS", "ENF", "SS"]
    by = {x["route"]: x for x in r["routes"]}
    trs = "".join(f'<tr><th scope="row">{chip("Route", c)} {e(ROUTE_NAME[c])}</th><td data-k="Feasibility">{e(by[c]["feasibility"].capitalize())}</td>'
                  f'<td data-k="Date">{"Checked " + words_date(by[c]["checked"]) if by[c]["checked"] else "Not checked"}</td></tr>'
                  for c in order)
    pbm = "pharmacy benefit managers, the companies that run drug benefits for insurers and employers"
    need(pbm in r["status"]["text"], "Reform R-19's status no longer defines pharmacy benefit managers")
    body = (f'<p class="hed">{chip("Reform", "R-19")}<span>“{e(r["title"])}”</span></p>'
            f'<p class="sub">PBMs are {e(pbm)}.</p>'
            f'<p class="ms">Status, as of {SNAP}: partly in place.</p>'
            '<table class="tb stack blk"><caption>Routes to change, with the date each was last checked</caption><thead><tr>'
            '<th scope="col">Route</th><th scope="col">Feasibility</th><th scope="col">Date</th></tr></thead>'
            f'<tbody>{trs}</tbody></table>'
            f'<p class="src">Source: {e(ATLAS)}, reform R-19, its status and routes, snapshot of {SNAP}, United States. '
            f'Of the atlas’s {total} route entries, {dated} carry a check date.</p>')
    book.add("s-13-10-correct", body, rule="13.10", readable=True,
             alt=(f"Reform R-19, {r['title']}, with its status dated as of {SNAP}: partly in place. A table lists three routes "
                  f"to change. Route FS, Federal statute, feasibility high, checked {SNAP}. Route ENF, Enforcement and litigation, "
                  "feasibility medium, not checked. Route SS, State statute, feasibility high, not checked."),
             notes=f"Routes, ratings and check dates read from the atlas; {dated} of its {total} route entries carry a date.")
    book.log("13.10 correct", "Reform R-19, drug-pricing middlemen", "D06")
    trs_f = "".join(f'<tr><th scope="row">{chip("Route", c)} {e(ROUTE_NAME[c])}</th><td data-k="Feasibility">{e(by[c]["feasibility"].capitalize())}</td></tr>'
                    for c in order)
    fail = (dnp() + f'<p class="hed">{chip("Reform", "R-19")}<span>“{e(r["title"])}”</span></p>'
            f'<p class="sub">PBMs are {e(pbm)}.</p>'
            '<p class="ms">Where it stands now: partly in place.</p>'
            '<table class="tb stack blk"><caption>Routes to change</caption><thead><tr><th scope="col">Route</th>'
            f'<th scope="col">Feasibility</th></tr></thead><tbody>{trs_f}</tbody></table>')
    book.add("s-13-10-failure", fail, rule="13.10",
             alt=(FC + "Reform R-19 under the heading Where it stands now, with its three routes and their feasibility and no "
                  "date on the status or on any route."),
             notes="Labeled failure: an undated status and routes that read as checked.")
    return {
        "id": "13.10",
        "title": "Date what can change, and print an undated route as not checked.",
        "rule": [
            "A status, a count or a rule that can change after we publish carries the date it was last checked, in words, as in "
            f"“as of {SNAP}”. Our systems atlas dates its research as a snapshot, and its glossary defines one as “"
            + GLOSS["Snapshot"].split(". ")[0] + ".” Each fact the atlas rechecked also carries a date of its own. A page prints "
            "a fact’s own check date where it has one, and the snapshot date where it does not.",
            "A route, one of the paths a reform can take to become law or practice, carries its check date when the atlas gives "
            f"one and the words “Not checked” when it does not. Of the atlas’s {total} route entries, {dated} carry a date. When "
            "something the record names has happened since its date, such as an election, the page keeps the dated words and "
            "adds what happened, with its own source and date.",
        ],
        "why": {"text": ["A rating with no date reads as current, and a reader may act on it. “Not checked” tells them to look "
                         "for themselves before they rely on the rating."],
                "basis": "Our systems atlas’s glossary entry “Snapshot” and its route records"},
        "correct": {"specimen": "s-13-10-correct",
                    "caption": f"Reform R-19’s three routes, each with its date: the atlas checked the federal route on {SNAP} "
                               "and prints the other two as not checked. The status carries its own date."},
        "failure": {"specimen": "s-13-10-failure",
                    "caption": "<strong>Fails Rule 13.10.</strong> The heading says now and no route carries a date, so all three "
                               "read as checked, though the atlas checked only one."},
        "specs": [
            {"label": "A checked route", "value": "“Checked” and the date, from the route’s own record"},
            {"label": "An undated route", "value": "“Not checked”, in the same type and place"},
            {"label": "A status", "value": "“As of” and the date, before the status words"},
            {"label": "An atlas value", "value": f"“Snapshot of {SNAP}” where it has no check date of its own"},
            {"label": "Dates", "value": "In words, as house rule H05 sets"},
        ],
        "related": ["11", "15", "21"],
        "builders": ["Print the check date from each route’s own record and “Not checked” where that field is empty, so a "
                     "rating never borrows the reform’s status date."],
    }


# ===============================================================================================================
# Rule 13.11, events apart from findings
# ===============================================================================================================
SHORT = {
    "RL02": "Local Law 8 created the Campaign Finance Board and public matching funds for small contributions.",
    "RL12": "Charter Question 1 raised the public match to 8 to 1 and lowered contribution limits for city offices.",
    "RL37": "Proposition 1 renewed for ten years the levy that funds Democracy Vouchers.",
    "RL59": "Ballot Measure 1 reinstated state limits on contributions to candidates.",
    "RL03": "Citizens United v. FEC held that limits on independent spending by corporations and unions violate the First Amendment.",
    "RL05": "McCutcheon v. FEC struck down limits on the total one donor may give to all federal candidates and parties.",
    "RL58": "NRSC v. FEC struck down federal limits on spending that parties coordinate with their candidates.",
}


def rule_13_11(book):
    log = [r for r in V7["repairLog"]["rows"] if r["loop"].startswith("Loop R1:")]
    need(sorted(r["id"] for r in log) == sorted(SHORT), "Loop R1's repair log rows changed")
    need(len(V7["repairLog"]["rows"]) == 64 and len(V7["deliveryLog"]["rows"]) == 24, "the logs' sizes changed")
    unverified = [r["id"] for r in log if not r["verified"]]
    need(unverified == ["RL02"], "the unchecked row on Loop R1 changed")
    note = V7["repairLog"]["coding_note"]
    tail = "A row's direction describes the rule's effect on who officials answer to and carries no judgment of the people or parties involved."
    need(note.endswith(tail), "the repair log's coding note changed")
    for k, words in SHORT.items():
        row = next(r for r in log if r["id"] == k)
        for w in re.findall(r"Citizens United|McCutcheon|NRSC|Charter Question 1|Proposition 1|Ballot Measure 1|Local Law 8", words):
            need(w in row["rule"], f"{k} no longer names {w}")
    groups = []
    for direction in ("toward voters", "away from voters"):
        items = sorted((r for r in log if r["direction"] == direction), key=lambda r: r["date"])
        lis = "".join(
            f'<li>{event_svg(INSTR[r["instrument"]])}<span><span class="dt">{words_date(r["date"])}</span>, {e(r["jurisdiction"])}, '
            f'{e(FAMILY_WORD[INSTR[r["instrument"]]].lower())}. {e(SHORT[r["id"]])} {chip("Rule change", r["id"])}'
            + (' <span class="flag">Source not checked</span>' if not r["verified"] else "") + "</span></li>"
            for r in items)
        groups.append(f'<div class="blk"><p class="k">The atlas codes these rows {e(direction)}</p><ul class="evl">{lis}</ul></div>')
    conns = "".join(f'<div class="st">{line_svg(LINK[c]["evidence"], STEP_W, delay=LINK[c]["delay"], sign=LINK[c]["polarity"])}'
                    f'<p>{chip("Connection", c)} “{e(LINK[c]["name"])}”. {grade_word(LINK[c]["evidence"])}.</p></div>'
                    for c in LOOP["R1"]["links"])
    key = "".join(f'<span class="ky">{event_svg(f)}<span>{e(w)}</span></span>' for f, w in FAMILY_WORD.items())
    low = least_certain(LOOP["R1"]["links"])
    weak = [c for c in LOOP["R1"]["links"] if LINK[c]["evidence"] == low][0]
    body = (f'<p class="hed">{chip("Loop", "R1")}<span>“{e(LOOP["R1"]["title"])}”</span></p>'
            f'<p class="nt">The atlas’s coding note: “{e(tail)}”</p>'
            f'<div class="blk"><div class="evr"><span class="ev">Finding</span><span class="gr">Documented: the atlas’s repair log</span></div>'
            f'<p class="k">Events, with the shape for each instrument</p><div class="kys">{key}</div></div>'
            + "".join(groups)
            + f'<div class="blk">{diagram_label(low, f"{GRADE[low][1]}, the grade of the loop’s least certain step, Connection {weak}")}'
              f'<p class="k">Causal claims: the loop’s connections</p>{conns}</div>'
            + f'<p class="src">Source: {e(ATLAS)}, repair log rows on loop R1 and connections L01, L02 and L03, snapshot of {SNAP}, '
              'United States. One row rests on a source the atlas has not checked, and it is marked.</p>')
    book.add("s-13-11-correct", body, rule="13.11", readable=True,
             alt=("Loop R1, wealth and political influence reinforce each other, in two parts. The atlas’s coding note opens the "
                  "plate: a row’s direction describes the rule’s effect on who officials answer to and carries no judgment of the "
                  "people or parties involved. Events: the atlas’s seven repair log rows on the loop, labeled Finding, "
                  "Documented, each a filled shape for its instrument with its date, place and what it did, under headings that "
                  "say how the atlas codes them. The atlas codes these rows toward voters: New York City’s Local Law 8 in 1988, "
                  "marked source not checked; New York City’s Charter Question 1 in 2018; Seattle’s Proposition 1 in 2025; "
                  "Alaska’s Ballot Measure 1 in 2026. The atlas codes these rows away from voters: the court rulings in "
                  "Citizens United in 2010, McCutcheon in 2014 and NRSC in 2026. None has an arrow. Causal claims, labeled "
                  "Plausible: the loop’s three connections, drawn as arrows in the line of their grades with sign tags and "
                  "delay ticks: L01 well supported, L02 plausible, L03 well supported."),
             notes="Event shapes as Gate 1's M4 approved them: ballot measure a square, statute or local law a wide bar, court "
                   "ruling a tall bar, executive or agency action a framed square. Each row's words are a short form of the "
                   "atlas's own. The coding note opens the plate and each heading names the atlas (D3-85, brand M1); all seven "
                   "rows stay, in date order (D3-86).")
    book.log("13.11 correct", "Loop R1's repair log rows and connections", "D03", states=("NY", "WA", "AK"))
    r3 = next(r for r in log if r["id"] == "RL03")
    fail = (dnp() + '<div class="arrowrow">'
            f'<span class="box">Citizens United v. FEC, {words_date(r3["date"])}</span>'
            f'{line_svg("documented", 96, sign="+")}'
            f'<span class="box">{e(node_title("B1"))}</span></div>'
            f'<p class="nt">{grade_word("documented", gloss=False)}</p>')
    book.add("s-13-11-failure", fail, rule="13.11",
             alt=(FC + f"A box for the Citizens United ruling of {words_date(r3['date'])} joined by a solid arrow with a plus sign "
                  f"tag to a box for {lc(node_title('B1'))}, graded Documented with the record square."),
             notes="Labeled failure: a dated event drawn with the causal grammar of a connection.")
    return {
        "id": "13.11",
        "title": "Draw documented events apart from causal claims.",
        "rule": [
            f"Our systems atlas keeps two logs of dated events. The repair log records {len(V7['repairLog']['rows'])} changes to "
            "the rules that decide who officials answer to, and the delivery log records "
            f"{len(V7['deliveryLog']['rows'])} times government did something hard at scale with a measured result. An event "
            "records what happened on a date. A causal claim says that one thing moves another, and the atlas grades it.",
            "On a chart or diagram, an event takes a mark of its own, a shape for its instrument with an outline for one still "
            "pending, and no arrowhead, line pattern or sign. Where the atlas codes an event’s direction, such as toward voters, "
            "the page prints the atlas’s words as the atlas’s assessment, with the atlas named, apart from the event’s date, "
            "place and text. A causal claim keeps the arrow, the sign and the line of Rule 13.4.",
        ],
        "tokens": ["oa.color.graphic.essential.onNewsprint"],
        "why": {"text": ["A ruling drawn as an arrow into a variable claims that the ruling moved the variable by an amount someone "
                         "measured. The log records that the ruling happened and what it changed in the rules, and a mark of its "
                         "own keeps a reader from taking it for more."],
                "basis": "Design judgment, from the atlas’s event mark our founder and editor approved in October 2026"},
        "correct": {"specimen": "s-13-11-correct",
                    "caption": "Loop R1’s seven entries in the repair log, under the atlas’s own coding note, each a dated shape "
                               "under a heading that says how the atlas codes it, then the loop’s three connections drawn as causal "
                               "claims with their grades."},
        "failure": {"specimen": "s-13-11-failure",
                    "caption": "<strong>Fails Rule 13.11.</strong> A ruling drawn as a solid arrow with a plus sign reads as a "
                               "measured effect on political spending, though the log records only that the ruling happened."},
        "specs": [
            {"label": "Event shapes", "value": "Ballot measure, a filled square; statute or local law, a wide bar; court ruling, a tall bar; executive or agency action, a framed square"},
            {"label": "Pending", "value": "The shape in outline"},
            {"label": "Direction", "value": "The atlas’s words, under a heading that names the atlas, such as “The atlas codes these rows toward voters”, with its coding note above the rows"},
            {"label": "Left off", "value": "Arrowheads, line patterns, signs and grade words on each event"},
            {"label": "Label", "value": "The date in words, the place and what the rule did, with the row’s ID in its chip"},
            {"label": "Placement", "value": "An event’s shape sits only at the head of its row, with the figure’s key, 6 px from its word; the record square sits only before the word Documented (Rule 13.4)"},
        ],
        "related": ["14", "15", "21"],
        "builders": ["Draw events from the logs’ rows and connections from the connection records, each with its own drawing "
                     "function, so an event cannot pick up an arrowhead by a wrong flag."],
    }


# ===============================================================================================================
# Rule 13.12, quotes
# ===============================================================================================================
BRANDEIS = ("It is one of the happy incidents of the federal system that a single courageous State may, if its citizens choose, "
            "serve as a laboratory; and try novel social and economic experiments without risk to the rest of the country.")
LOC_URL = "https://tile.loc.gov/storage-services/service/ll/usrep/usrep285/usrep285262/usrep285262.pdf"


def rule_13_12(book):
    need(node_title("D6") == "State and local testing of reforms", "Variable D6 changed")
    attribution = ("Louis D. Brandeis, associate justice of the Supreme Court, dissenting in New State Ice Co. v. Liebmann, an "
                   "Oklahoma case the Court decided on March 21, 1932")
    src = ("Source: New State Ice Co. v. Liebmann, 285 U.S. 262, 311 (1932), Brandeis, J., dissenting, United States "
           "Reports, via the Library of Congress. Retrieved November 11, 2026.")
    body = (f'<p class="sub">Set beside {chip("Variable", "D6")}, {e(lc(node_title("D6")))}, in our systems atlas</p>'
            f'<p class="q">“{e(BRANDEIS)}”</p><p class="by">{e(attribution)}</p><p class="src">{e(src)}</p>')
    book.add("s-13-12-correct", body, rule="13.12", readable=True,
             alt=(f"A quotation set beside Variable D6, state and local testing of reforms, in our systems atlas. In Lora Italic: "
                  f"“{BRANDEIS}” Under it: {attribution}. The source line names the case in the United States Reports, page 311, "
                  "via the Library of Congress, retrieved November 11, 2026."),
             notes=f"The words copied from the United States Reports scan at {LOC_URL}, page 311, read November 11, 2026, with "
                   "the decision date (March 21, 1932) and the dissent's running head. The Reports print “State”, as the quote "
                   "does (statistics S10). The opinion holds neither “laboratories” nor “democracy”, which the failure plate's "
                   "paraphrase uses (checked by script in the scan's text).")
    book.log("13.12 correct", "Justice Brandeis on states as laboratories", "D05", states=("OK",))
    fail = dnp() + '<p class="q">“States are the laboratories of democracy.”</p><p class="by">Louis Brandeis</p>'
    book.add("s-13-12-failure", fail, rule="13.12",
             alt=FC + "A pull quote in Lora Italic, “States are the laboratories of democracy.”, credited to Louis Brandeis with no role, date, place or source.",
             notes="Labeled failure: a later paraphrase in quotation marks; the opinion's text holds neither word it turns on.")
    return {
        "id": "13.12",
        "title": "Quote a person exactly, with who, when and where.",
        "rule": [
            "A quotation prints a person’s words exactly as the record holds them, set in Lora Italic as Rule 06.1 sets, and then "
            "says who said them, the role they held at the time, when, and where: the hearing, the ruling, the speech or the "
            "interview. A source line gives the record a reader can open. Words we add for sense sit in square brackets, and an "
            "ellipsis marks a cut only where the meaning stays the same.",
            "In a chart or diagram, a quote sits beside the mark it speaks to as a note with its attribution, and the title stays "
            "our sentence about the evidence (Rule 13.1). An Act piece quotes each side at the same length (Rule 01.22), and an "
            "invented quote carries the Illustrative label beside it (Rule 13.8).",
        ],
        "tokens": ["oa.font.family.quote"],
        "why": {"text": ["A quotation is the one place we print someone else’s words as theirs. The exact words with who, when "
                         "and where let a reader check them, and they keep a famous paraphrase from passing for the original."],
                "basis": "Editorial judgment"},
        "correct": {"specimen": "s-13-12-correct",
                    "caption": "Justice Brandeis’s words as the Court’s opinion prints them, with his role, the case, the date and "
                               "the record, set beside the atlas variable they speak to."},
        "failure": {"specimen": "s-13-12-failure",
                    "caption": "<strong>Fails Rule 13.12.</strong> The words in quotation marks appear nowhere in the opinion, and "
                               "the line gives no role, date or place, so a reader cannot check them."},
        "specs": [
            {"label": "The words", "value": "Exactly as the record holds them, in Lora Italic, the opening mark hung (Rule 06.7)", "token": "oa.font.family.quote"},
            {"label": "Who", "value": "The name, and the role held at the time"},
            {"label": "When and where", "value": "The date in words, and the hearing, ruling, speech or interview"},
            {"label": "Source", "value": "A source line for the record a reader can open"},
            {"label": "In a chart", "value": "Beside the mark it speaks to, with its attribution, under a title that stays ours"},
            {"label": "Added words", "value": "In square brackets; a cut takes an ellipsis only where the meaning holds"},
        ],
        "related": ["06", "01", "14"],
        "builders": ["Copy a quotation from the record itself, never from an article that quotes it, and keep the record’s link "
                     "in the piece’s notes."],
    }


# ===============================================================================================================
# Rule 13.13, corrections (DR-233)
# ===============================================================================================================
LIB = [("Main Library", 52), ("Riverside", 44), ("Elm Street", 36)]
LIB_WRONG = 58


def bars_svg(data, w=312):
    """The piece's ranked bar, drawn in the chart tokens. Contract C7's spec for the kit sits beside the fragment
    (s-13-13-correct.chart.json); the kit's figure replaces this drawing once the guide hook lands."""
    label_w, row, bh, top = 104, 34, 20, 4
    vmax = 60
    plot = w - label_w - 36
    h = top + row * len(data)
    out = [f'<line class="bl" x1="{label_w}" y1="0" x2="{label_w}" y2="{h}"/>']
    for i, (name, v) in enumerate(data):
        y = top + i * row
        bw = plot * v / vmax
        out.append(f'<text class="n" x="0" y="{y + 15}">{e(name)}</text><rect class="b" x="{label_w}" y="{y}" width="{bw:.1f}" height="{bh}"/>'
                   f'<text class="v" x="{label_w + bw + 6:.1f}" y="{y + 15}">{v}</text>')
    return (f'<svg class="bc" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true" focusable="false">'
            + "".join(out) + "</svg>")


GUIDE_BUILD = ROOT / "work/build/scripts/phase-2/guide_build.py"


def kit_hook():
    """Contract C7: once guide_build.py expands <div data-oa-chart="..."> and the engineer's notes say GUIDE HOOK READY,
    the plate names its spec and the kit draws the chart in the guide. Until then the plate carries a static drawing in the
    chart tokens. --static-chart forces the drawing."""
    if "--static-chart" in sys.argv:
        return False
    notes = ROOT / "work/handoffs/phase-3/20261111_Round-0-Engineer-Notes.md"
    return (GUIDE_BUILD.exists() and "data-oa-chart" in GUIDE_BUILD.read_text()
            and notes.exists() and "GUIDE HOOK READY" in notes.read_text())


LIB_TITLE = "The Main Library will be open the most hours of the three branches"
LIB_MEASURE = "Hours open each week from January 4, Alder County’s three library branches"


def rule_13_13(book):
    head = "Alder County’s libraries add Sunday hours from January"
    hook = kit_hook()
    src = ("Source: Alder County Board, adopted library schedule, hours from January 4, Alder County’s three branches. "
           "Retrieved November 2, 2026. Values invented for this example.")
    figure = '<div data-oa-chart="s-13-13-correct"></div>' if hook else bars_svg(LIB)
    figure_f = '<div data-oa-chart="s-13-13-fail-chart"></div>' if hook else bars_svg(LIB)
    def chead(cid):
        # the kit prints the chart's title and measure line from its spec, so the drawing is named by the title above it
        return ('<div class="evr"><span class="ev">Finding</span><span class="gr">Documented: the county’s adopted schedule</span></div>'
                + ("" if hook else f'<p class="ct">{e(LIB_TITLE)}</p><p class="ms">{e(LIB_MEASURE)}</p>'))
    note = (f"<b>Corrected November 4, 2026.</b> An earlier version of this article and its chart gave the Main Library’s "
            f"weekly hours as {LIB_WRONG}. The county’s adopted schedule gives {LIB[0][1]}. We replaced the chart and fixed the "
            "second paragraph.")
    piece = (f'<div class="card nb">{ill()}<p class="cn">{note}</p><p class="hl art">{e(head)}</p>'
             '<p>The county board approved Sunday hours at all three branches from January 4.</p>'
             f'<p>The Main Library will open {LIB[0][1]} hours a week, the most of the three.</p>'
             f'<div class="blk">{chead("s-13-13-correct")}{figure}</div><p class="src">{e(src)}</p></div>')
    page = (f'<div class="card nb">{ill()}<p class="hl">Corrections</p><p class="sub">Every correction we have made, newest first.</p>'
            '<div class="blk lp"><p class="dt">November 4, 2026</p>'
            f'<p><b>{e(head)}</b>, first published November 2, 2026.</p>'
            f'<p>An earlier version of this article and its chart gave the Main Library’s weekly hours as {LIB_WRONG}. The '
            f'county’s adopted schedule gives {LIB[0][1]}. We replaced the chart and fixed the second paragraph.</p></div></div>')
    body = f'<div class="fx two"><div>{piece}</div><div>{page}</div></div>'
    book.add("s-13-13-correct", body, rule="13.13", readable=True, illustrative=True,
             alt=(f"An invented article and its corrections page entry, each labeled Illustrative. Above the headline, {head}, a "
                  "note with a dark bar reads: Corrected November 4, 2026. An earlier version of this article and its chart gave "
                  f"the Main Library’s weekly hours as {LIB_WRONG}. The county’s adopted schedule gives {LIB[0][1]}. We replaced "
                  "the chart and fixed the second paragraph. The fixed chart follows, ranking weekly hours: Main Library "
                  f"{LIB[0][1]}, Riverside {LIB[1][1]}, Elm Street {LIB[2][1]}. The corrections page lists the same note under "
                  "its date, with the headline and the date the article first ran."),
             notes="Invented throughout, one label at the head of each piece (DR-97). The note's tokens follow Rule 26.3's example "
                   "for a correction notice: primary text and a 4 px bar in the essential graphic color. "
                   + ("The chart is the kit's figure from s-13-13-correct.chart.json (contract C7)." if hook else
                      "The chart is a static drawing in the chart tokens until the kit's guide hook lands; its kit spec, "
                      "s-13-13-correct.chart.json, passes the kit's checks (oa-chart.mjs build, 0 faults)."))
    book.log("13.13 correct", "Alder County library hours", "invented", level="invented")
    fail = (dnp() + f'<div class="card">{ill()}<p class="hl art">{e(head)}</p>'
            '<p>The county board approved Sunday hours at all three branches from January 4.</p>'
            f'<p>The Main Library will open {LIB[0][1]} hours a week, the most of the three.</p>'
            f'<div class="blk">{chead("s-13-13-fail-chart")}{figure_f}</div><p class="src">{e(src)}</p>'
            '<p class="foot">Updated</p></div>')
    book.add("s-13-13-failure", fail, rule="13.13", illustrative=True, width=360,
             alt=(FC + f"The same invented article, labeled Illustrative, with the chart already showing {LIB[0][1]} hours and one "
                  "word at its foot, Updated, with no date and no account of what was wrong."),
             notes="Labeled failure: a silent fix with an undated Updated line at the foot.")
    spec = {
        "kit": 1, "id": "s-13-13-correct", "form": "ranked-bar", "family": "comparison", "tier": "core",
        "data": {"columns": {"branch": {"type": "text"}, "hours": {"type": "integer", "unit": "hours a week"}},
                 "rows": [{"branch": b, "hours": h} for b, h in LIB]},
        "reader_question": "Which branch will be open the most hours a week?",
        "evidence": "illustration", "evidence_label": "Illustration",
        "title": LIB_TITLE,
        "measure_line": LIB_MEASURE,
        "source_line": src,
        "illustrative": "Illustrative data",
        "alt": "A ranked bar of weekly hours at three invented library branches: Main Library 52, Riverside 44, Elm Street 36.",
        "table": {"caption": "Hours open each week, from January 4", "columns": [
            {"field": "branch", "label": "Branch", "format": "text", "row_header": True},
            {"field": "hours", "label": "Hours a week", "format": "integer"}]},
        "phone": "same", "domain": "all", "states": [], "encode": {"category": "branch", "value": "hours"},
        "show": ["title", "measure", "chart"],
        "notes_internal": "Chapter 13's one chart (Rule 13.13's correct plate), in contract C7's format. Invented values. "
                          "domain is all because the example is invented and counts toward no atlas domain.",
    }
    KIT_SPECS["s-13-13-correct"] = spec
    KIT_SPECS["s-13-13-fail-chart"] = dict(spec, id="s-13-13-fail-chart",
                                          notes_internal="The failure plate's chart: the same invented data, already fixed.")
    return spec, {
        "id": "13.13",
        "title": "Correct in the open, with a dated note at the top.",
        "rule": [
            "When a piece we published gets a fact, a figure or a chart wrong, we fix it and say so at its top. A correction note "
            "sits above the headline with the date of the fix and says what was wrong and what changed, in plain sentences. The "
            "fixed chart replaces the old one in the piece, so every reader and every share meets the right figures, and the note "
            "says what the old chart showed.",
            "The same note goes on our corrections page, newest first, with the piece’s headline, a link to it and the date it "
            "first ran, and both stay as long as the piece is published. A correction takes no red: its words take the primary "
            "text color and its 4 px bar the essential graphic color, as Rule 26.3’s example sets out.",
        ],
        "tokens": ["oa.color.graphic.essential.onNewsprint", "oa.border.width.bar"],
        "why": {"text": ["A note that says what was wrong lets a reader who saw the first version learn of the change, and anyone "
                         "who shared the old figure can find out why it moved. Over months, the corrections page shows readers how "
                         "often we get things wrong and how we fix it."],
                "basis": "Our founder and editor’s policy on corrections, November 11, 2026"},
        "correct": {"specimen": "s-13-13-correct",
                    "caption": "An invented article with its correction note above the headline and the fixed chart in place, "
                               "beside the entry for the same correction on the corrections page."},
        "failure": {"specimen": "s-13-13-failure",
                    "caption": f"<strong>Fails Rule 13.13.</strong> The chart changed and the foot says only “Updated”, so a reader "
                               f"who saw {LIB_WRONG} hours cannot learn it was wrong."},
        "specs": [
            {"label": "Place", "value": "Above the headline, before any other words"},
            {"label": "Words", "value": "“Corrected” and the date, what was wrong, what changed"},
            {"label": "The chart", "value": "The fixed chart in place of the old one, and the note says what the old one showed"},
            {"label": "Corrections page", "value": "Every note, newest first, with the headline, a link and the date the piece first ran"},
            {"label": "Look", "value": "Primary text and a 4 px bar in the essential graphic color, with no red", "token": "oa.border.width.bar"},
            {"label": "How long", "value": "The note stays as long as the piece is published"},
        ],
        "related": ["26", "05", "20", "24"],
        "builders": ["Store each correction as a record with the piece’s ID, the date and the words, and build both the note and "
                     "the corrections page from it, so the two always match."],
    }


# ===============================================================================================================
# The chapter
# ===============================================================================================================
def chapter(book):
    op = opener(book)
    rules = [rule_13_1(book), rule_13_2(book), rule_13_3(book), rule_13_4(book), rule_13_5(book), rule_13_6(book),
             rule_13_7(book), rule_13_8(book), rule_13_9(book), rule_13_10(book), rule_13_11(book), rule_13_12(book)]
    spec, r13 = rule_13_13(book)
    rules.append(r13)
    cps = sidecar("census-spm-child-poverty")
    pay = sidecar("fred-payrolls-monthly-change")
    data = {
        "number": "13",
        "anchor": "evidence",
        "title": "Evidence and sourcing",
        "part": "Evidence and media",
        "instruction": "Name the kind of evidence behind each claim, with its source and any label beside it.",
        "opener": op,
        "intro": [
            "Every chart, diagram and claim we publish carries its evidence: what kind it is, how strong, who published it and "
            "when. Our systems atlas, Who Do They Answer To?, grades each claim it holds from documented to hypothesis, and that "
            "evidence grade sets the words and lines a page may use.",
            "Where chapter 01 or chapter 02 already states a rule, the rules here cite it and show how a figure keeps it.",
        ],
        "groups": [
            {"before_rule": "13.1", "number": 1, "title": "Kinds of evidence and their grades",
             "line": "A title says what kind of evidence it rests on, and every word, line and mark about that evidence follows "
                     "the grade our systems atlas gives it."},
            {"before_rule": "13.6", "number": 2, "title": "Sources, dates and labels",
             "line": "A reader can trace every number to its publisher and its date, and can tell what we invented from what "
                     "we found."},
            {"before_rule": "13.11", "number": 3, "title": "Records, quotes and corrections",
             "line": "Dated events, quoted words and our own corrections each take a form a reader can check against the record."},
        ],
        "rules": rules,
        "extras": [],
        "related_chapters": [
            {"chapter": "01", "reason": "The nonpartisan rules, among them Rules 01.9, 01.11, 01.16, 01.22 and 01.23, which this chapter cites."},
            {"chapter": "02", "reason": "House rules H03, H04, H08, H09 and H11, which these rules carry into charts and the atlas."},
            {"chapter": "10", "reason": "Rule 10.10, the atlas’s encoding glyphs and their measurements."},
            {"chapter": "12", "reason": "Rule 12.6, keys that print the grade words in the order the marks run."},
            {"chapter": "14", "reason": "Every chart, held to these rules."},
            {"chapter": "15", "reason": "Every systems drawing and the atlas’s worked examples, held to these rules."},
            {"chapter": "18", "reason": "Rule 18.24, the typed ID chip as a component."},
            {"chapter": "26", "reason": "Rule 26.3, the tokens a correction note takes."},
        ],
        "sources": [
            cp_source("both")[0],
            cps["source_line_variants"]["source_line_first_published"].replace(
                "Rates as first published; the Bureau revised 2019 to 2024 in August 2026.",
                "Rates before the Bureau’s August 2026 correction to the poverty thresholds."),
            pay["printed_source_line"],
            (f"Source: {ATLAS}, the records each rule names (connections, loops, reforms, claims, the repair log, the delivery "
             f"log, the headline figures and the glossary), snapshot of {SNAP}, United States. Retrieved November 11, 2026. "
             "Facts the atlas rechecked carry their own check dates; inclusion in the snapshot alone does not mean a fact was "
             "rechecked on that date."),
            ("Source: José Azar, Ioana Marinescu and Marshall I. Steinbaum, “Labor Market Concentration,” Journal of Human "
             f"Resources, 2022, online job postings, 2010 to 2013, United States, as recorded in our systems atlas, claim CL1507, "
             f"snapshot of {SNAP}. Online postings leave out some jobs, behind Rule 13.1."),
            ("Source: National Highway Traffic Safety Administration, Lives Saved by Vehicle Safety Technologies and Associated "
             "Federal Motor Vehicle Safety Standards, 1960 to 2012 (DOT HS 812 069), United States, as recorded in our systems "
             f"atlas’s delivery log, delivery case DL06, snapshot of {SNAP}. The agency calls its figure “a hypothetical estimate”, "
             "behind Rule 13.1."),
            ("Source: New State Ice Co. v. Liebmann, 285 U.S. 262, 311 (1932), Brandeis, J., dissenting, decided March 21, 1932, "
             "United States Reports, via the Library of Congress. Retrieved November 11, 2026. The quotation behind Rule 13.12."),
        ],
    }
    return data, spec


# ===============================================================================================================
# Checks
# ===============================================================================================================
FILLERS = ["genuinely", "really", "truly", "actually", "simply", "just", "leverage", "underscore", "underscores", "reflect",
           "reflects", "crucial", "robust", "seamless", "powerful", "stunning", "vital", "key insight"]
STUDIO = r"Master Brief|\bPhase\b|\bGates?\b|\b[Bb]oards? \d|stage board|the studio|\bV5\b|\bV4\.2\b|Atlas V7|\bV7\b|\bDR-\d|\bD[12]-\d|\bG1-|\bT-\d"
LOCKED = {"tagline": "A country that answers to its people.",
          "mission": "Help people understand and improve the rules that shape their lives.",
          "promise": "We explain how a decision is made and give you a practical way to take part.",
          "commitment": "Clarity is our duty. Action is our promise."}


def strings(o, skip=("notes",)):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in skip:
                yield from strings(v, skip)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, skip)


def visible(fragment):
    t = re.sub(r"<style\b.*?</style>|<!--.*?-->", " ", fragment, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return " ".join(html.unescape(t).split())


def check(data, book, spec):
    fails = []
    texts = {"chapter": " ".join(strings({k: v for k, v in data.items() if k not in ("sources",)}))}
    for sid, frag in book.files.items():
        texts[sid] = visible(frag)
        texts[sid + " alt"] = book.manifest[sid]["alt"]
    allt = " ".join(texts.values())
    for k, t in texts.items():
        if "—" in t or "‑" in t:
            fails.append(f"em dash or U+2011 in {k}")
        for w in FILLERS:
            for m in re.finditer(rf"\b{w}\b", t, re.I):
                fails.append(f"listed word {w!r} in {k}: …{t[max(0, m.start() - 50): m.end() + 30]}…")
        for m in re.finditer(STUDIO, t):
            fails.append(f"studio word or code {m.group(0)!r} in {k}")
        if re.search(r"\bnot only\b|\bnot just\b|, not [a-z]+ [a-z]+,", t):
            fails.append(f"a corrective-negation shape in {k}")
    for name, line in LOCKED.items():
        head = line[: max(18, len(line) // 2)]
        for m in re.finditer(re.escape(head), allt):
            if allt[m.start(): m.start() + len(line)] != line:
                fails.append(f"near miss of the {name}")
    for r in data["rules"]:
        rid = r["id"]
        n = len(re.sub(r"[“”.,]", "", r["title"]).split())
        if n > 15:
            fails.append(f"Rule {rid}: title runs {n} words (D2-1709, D2-1739)")
        if not r["failure"]["caption"].startswith(f"<strong>Fails Rule {rid}.</strong> "):
            fails.append(f"Rule {rid}: failure caption without its lead")
        if not r.get("specs"):
            fails.append(f"Rule {rid}: no Specifications")
        fsid = r["failure"]["specimen"]
        if 'class="dnp"' not in book.files[fsid]:
            fails.append(f"{fsid}: no do-not-publish band")
        if not book.manifest[fsid]["alt"].startswith("Failure case: do not publish."):
            fails.append(f"{fsid}: alt does not open with the band's words")
        for k in ("rule", "why", "correct", "failure", "builders", "related"):
            if not r.get(k):
                fails.append(f"Rule {rid}: no {k}")
    for sid, frag in book.files.items():
        m = book.manifest[sid]
        if m["illustrative"] and "Illustrative" not in frag:
            fails.append(f"{sid} is flagged Illustrative and carries no label")
        bare = re.sub(r"var\((?:[^()]|\([^()]*\))*\)", "", frag)
        bare = re.sub(r'\sd="[^"]*"', "", bare)
        if re.search(r"(?<![\w&])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![\w-])|\brgba?\(|\bhsla?\(", bare):
            fails.append(f"{sid}: a literal color")
        for px in re.findall(r"font(?:-size)?:[^;}\"]*?\b(\d+(?:\.\d+)?)px", frag):
            fails.append(f"{sid}: a font size in px ({px}) outside the tokens")
        if re.search(r"<h[1-6]\b", frag):
            fails.append(f"{sid}: a heading element")
    op = book.files[data["opener"]["specimen"]]
    if len(op.encode()) > 12 * 1024:
        fails.append(f"the opener's fragment weighs {len(op.encode()):,} bytes; it must stay well under 16 KB as placed")
    # every atlas ID in a chip exists in the model
    kinds = {"Variable": NODE, "Connection": LINK, "Loop": LOOP, "Reform": REFORM, "Issue": V7["issues"],
             "Claim": V7["claims"], "Route": ROUTE_NAME, "Rule change": {r["id"]: r for r in V7["repairLog"]["rows"]}}
    for sid, frag in book.files.items():
        for kind, rid in re.findall(r'<span class="chip">([A-Za-z ]+) <span class="id">([^<]+)</span>', frag):
            if rid not in kinds.get(kind, {}):
                fails.append(f"{sid}: {kind} {rid} is not in the atlas")
    # Rule 01.9 over the chapter's example log
    ex = [x for x in book.examples if x["domain"] not in ("all", "invented")]
    dom = Counter()
    for x in ex:
        dom[x["domain"]] += 1
    st = Counter(s for x in book.examples for s in x["states"])
    for d, n in dom.items():
        if n * 4 > len(ex):
            fails.append(f"Rule 01.9: domain {d} supplies {n} of {len(ex)} examples, over one in four")
    for s, n in st.items():
        if n * 5 > len(book.examples):
            fails.append(f"Rule 01.9: state {s} supplies {n} of {len(book.examples)} examples, over one in five")
    if spec.get("illustrative") != "Illustrative data":
        fails.append("the chart spec's illustrative label is missing")
    return fails, dom, st


def write(data, book, spec):
    SPECIMENS.mkdir(parents=True, exist_ok=True)
    for old in SPECIMENS.glob("s-13-*.html"):
        if old.stem not in book.files:
            old.unlink()
    for sid, txt in book.files.items():
        (SPECIMENS / f"{sid}.html").write_text(txt)
    (SPECIMENS / f"manifest-{MAKER}.json").write_text(json.dumps(book.manifest, indent=1, ensure_ascii=False) + "\n")
    for old in SPECIMENS.glob("s-13-*.chart.json"):
        if old.name[: -len(".chart.json")] not in KIT_SPECS:
            old.unlink()
    for cid, sp in KIT_SPECS.items():
        (SPECIMENS / f"{cid}.chart.json").write_text(json.dumps(sp, indent=1, ensure_ascii=False) + "\n")
    p = CHAPTERS / "13-evidence.json"
    p.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    return p


def main():
    book = Book()
    data, spec = chapter(book)
    fails, dom, st = check(data, book, spec)
    total = sum(len(x.encode()) for x in book.files.values())
    print(f"chapter 13: {len(data['rules'])} rules, {len(book.files)} plates, {total:,} bytes of fragments")
    for lag in TOKEN_LAG:
        print("token not yet in the release:", lag)
    print("examples by domain:", dict(sorted(dom.items())), "| states:", dict(st), "| all examples:", len(book.examples))
    for sid, frag in sorted(book.files.items(), key=lambda x: -len(x[1].encode()))[:6]:
        print(f"  {sid}: {len(frag.encode()):,} bytes")
    if fails:
        print("\n".join("FAIL " + f for f in fails))
        raise SystemExit(1)
    if "--check-only" not in sys.argv:
        p = write(data, book, spec)
        print(f"wrote {p.relative_to(ROOT)}, {len(book.files)} specimens and manifest-{MAKER}.json")


if __name__ == "__main__":
    main()
