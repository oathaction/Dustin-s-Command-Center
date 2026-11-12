"""Write chapter 15, Systems graphics: its words, its plates and its manifest.

Oath & Action Edition 06, Phase 3, round 1. Systems designer, November 12, 2026. The brief is
work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md (systems designer); the rule list the main session fixed (R7)
is in work/handoffs/phase-3/20261112_Round-1-Systems-Designer-Notes.md, section "Rule list". Round 1 builds the
grammar, Rules 15.1 to 15.10, and worked examples 1 and 2, Rules 15.13 (Loop R1) and 15.14 (Loop R8), with the opener.
The rules of later rounds are listed in PLANNED and join as each round builds them.

Usage:
    python3 -I work/build/scripts/phase-3/phase3_ch15_build.py [--check-only]

Reads, by script, every atlas value it prints from:
    work/extract/atlas-v7-data.json        the atlas model, snapshot of October 15, 2026 (printed beside anything that
                                           could have moved since)
and draws every connection with the atlas build's own wire_marks (work/boards/phase-2/atlas-editorial/
01-times-explainer/build_system.py, DR-36), with the 28 px lead-in from oa.chart.grade.leadIn (D3-105, D3-165). Chapter
13's generator lends its grade table, chips, grade words, do-not-publish band and checks, read and never edited, so
the two chapters print one table.

Writes:
    work/build/guide/chapters/15-systems-graphics.json
    work/build/guide/specimens/s-15-*.html
    work/build/guide/specimens/manifest-systems-graphics.json

Then runs its checks and stops on any failure: chapter 13's word checks (no em dash, no listed filler or corporate
word, no studio word or decision code in reader text, titles of fifteen words or fewer, failure captions led by
"Fails Rule 15.N.", failure plates with the do-not-publish band), no literal color, every font size from a token,
every atlas ID in a chip present in the model, every value the words print matched to the model, loop kind against
the count of minus signs on every numbered loop, no authority connection in any loop, Rule 01.9 over the example log,
and the chapter's bytes against round 1's 0.25 MB.
"""
import html
import importlib.util
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHAPTERS = ROOT / "work/build/guide/chapters"
SPECIMENS = ROOT / "work/build/guide/specimens"
MAKER = "systems-graphics"
WRITTEN = "November 12, 2026"
ROUND_STOP = 250_000          # the brief: chapter 15 under 0.25 MB at round 1's end (guide_charts.MB is 1,000,000)

sys.dont_write_bytecode = True
_c13 = importlib.util.spec_from_file_location("phase3_ch13_build", ROOT / "work/build/scripts/phase-3/phase3_ch13_build.py")
C13 = importlib.util.module_from_spec(_c13)
_c13.loader.exec_module(C13)
BS, GV, V7 = C13.BS, C13.GV, C13.V7
LINK, NODE, LOOP, REFORM = V7["links"], V7["nodes"], V7["loops"], V7["reforms"]
GLOSS = {g["term"]: g["definition"] for g in V7["glossary"]}
e, need, chip, grade_word, dnp, diagram_label = C13.e, C13.need, C13.chip, C13.grade_word, C13.dnp, C13.diagram_label
GRADE, DELAY, SNAP, ATLAS, MINUS = C13.GRADE, C13.DELAY, C13.SNAP, C13.ATLAS, C13.MINUS
need(SNAP == "October 15, 2026", "the atlas snapshot moved; reread every value before printing")
FC = "Failure case: do not publish. "

# ---------------------------------------------------------------------------------------------------------------
# The rule list the main session fixed (R7). Round 1 builds BUILT; the rest wait for their rounds.
# ---------------------------------------------------------------------------------------------------------------
BUILT = ["15.1", "15.2", "15.3", "15.4", "15.5", "15.6", "15.7", "15.8", "15.9", "15.10", "15.13", "15.14"]
PLANNED = {"15.11": "Place a reform on the exact connections and variables it targets, with its band.",
           "15.12": "Grade the evidence for the problem and for the remedy apart.",
           "15.15": "Follow a variable two loops share through each loop in turn.",
           "15.16": "Show a reform’s four effects side by side, with each route’s check date.",
           "15.17": "Draw who holds power over each level in one authority diagram.",
           "15.18": "Print a conceptual loop’s missing chain beside its grade.",
           "15.19": "Let a reader step through a loop one connection at a time, with a still sequence.",
           "15.20": "Let a reader choose a reform and see its targets, effects and assumptions.",
           "15.21": "Give every control the model’s own steps, and no slider for a strength.",
           "15.22": "Draw a route to change as its whole workflow, through to reversal.",
           "15.23": "Show which stages sit behind each of a tracker’s six steps.",
           "15.24": "Use the workflow for the reform’s route, with its official source and check date.",
           "15.25": "Reconcile every earlier atlas drawing to the model, and cite none as evidence."}

# ---------------------------------------------------------------------------------------------------------------
# Atlas facts, read once and held to the model
# ---------------------------------------------------------------------------------------------------------------
def link(i):
    need(i in LINK, f"connection {i} is not in the atlas")
    return LINK[i]


def node(i):
    need(i in NODE, f"variable {i} is not in the atlas")
    return NODE[i]


LOOP_NAME = {}
for _k, _p in LOOP.items():
    for (_code, _), (_lab, _) in zip(_p["chain"], _p["chain_labels"]):
        if _code in NODE:
            LOOP_NAME.setdefault(_code, _lab)


def short(code):
    """DR-185's label rule: the name the atlas gives the variable on its loops, where it holds one; else its title."""
    return LOOP_NAME.get(code) or node(code)["title"]


def minus_count(ids):
    return sum(1 for i in ids if link(i)["polarity"] == "-")


def lc(t):
    return C13.lc(t)


def kind_word(code):
    """The kind in words, from the atlas's own kind_plain, cut at its first sentence."""
    k = node(code)["kind_plain"].split(".")[0]
    return {"Condition (auxiliary)": "Condition, which the atlas calls auxiliary"}.get(k, k)


def words_n(n):
    return ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"][n] if n < 10 else str(n)


# ---------------------------------------------------------------------------------------------------------------
# The drawing kit. One artboard 296 px wide, the width of a 360 px phone's plate, with nothing under 15 px, so a
# 320 px phone that shrinks it still sets every word at 13 px (System 1's phone rule). Lines, tags, ticks and heads come
# from the atlas build's wire_marks; the lead-in, the fitted pattern and the classes are set here.
# ---------------------------------------------------------------------------------------------------------------
W = 296
PW = 130                  # a pill: 12 px inside each end, so "Congressional" (105 px at 15/600) sits whole
PAD = 12
LH = 18                   # a pill label's leading
LW = 2
LEAD = GV["lead_in"]
MIN_RUN = GV["min_run"] * LW
BEND = BS.BEND[LW]
RISE = 48                 # a loop's arrows leave a pill straight for 48 px, room for the lead-in and the gap after it
F = BS.f


def tex(grade):
    return BS.tex_of(grade) if grade else "solid"


def wrap(text, width, weight=600):
    return BS.wrap(text, width, 15, weight)


def tw(text, weight=400):
    return BS.tw(text, 15, weight)


def rounded_len(pts, r):
    """The length of rounded_d's path: straight runs plus each quadratic corner, measured, so a pattern fits the drawn
    line and starts and ends on ink."""
    if len(pts) == 2 or r <= 0:
        return BS.path_len(pts)
    total, cur = 0.0, pts[0]
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
        u0 = BS.unit(p1[0] - p0[0], p1[1] - p0[1])
        u1 = BS.unit(p2[0] - p1[0], p2[1] - p1[1])
        rr = min(r, math.dist(p0, p1) / 2, math.dist(p1, p2) / 2)
        a = (p1[0] - u0[0] * rr, p1[1] - u0[1] * rr)
        b = (p1[0] + u1[0] * rr, p1[1] + u1[1] * rr)
        total += math.dist(cur, a)
        q, prev = 0.0, a
        for k in range(1, 65):
            t = k / 64
            pt = ((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * p1[0] + t * t * b[0],
                  (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * p1[1] + t * t * b[1])
            q += math.dist(prev, pt)
            prev = pt
        total += q
        cur = b
    return total + math.dist(cur, pts[-1])


def cut(pts, s0, s1):
    """The part of a polyline between distances s0 and s1 from its start."""
    out, acc = [], 0.0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        d = math.dist(a, b)
        lo, hi = max(s0, acc), min(s1, acc + d)
        if hi > lo or (d == 0 and s0 <= acc <= s1):
            t0, t1 = (lo - acc) / d if d else 0, (hi - acc) / d if d else 0
            p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if not out:
                out.append(p0)
            out.append(p1)
        acc += d
    return out


MARK_RE = re.compile(r'<path class="ak-mark" d="([^"]*)"[^>]*/>')


def conn(pts, grade=None, sign=None, delay=None, authority=False, hollow=False, w=LW):
    """One connection along pts, tail to tip, drawn by the atlas build's wire_marks: the line in its grade's pattern or
    hollow, delay ticks after the tail, the sign tag, the arrowhead or the authority diamond. A patterned line with ticks
    runs solid for LEAD px, then leaves its pattern's own gap and starts the fitted pattern on ink (D3-105)."""
    t = "solid" if hollow else tex(grade)
    marks, body, _ = BS.wire_marks(pts, grade or "documented", sign if sign in ("+", "-") else None, delay, w,
                                   lit=False, sketch=hollow, authority=authority)
    marks = re.sub(r'<path class="ak-case"[^>]*/>', "", marks)
    marks = (marks.replace(' fill="none"', "").replace(' stroke-linecap="butt"', "").replace('<g class="lo">', "<g>")
             .replace('class="rail"', 'class="rl"').replace(' stroke-width="1"', ""))
    if not hollow and t != "solid":
        arr, cap = BS.pattern(t, w)
        rnd = ' stroke-linecap="round"' if cap == "round" else ""
        if delay:
            first = math.dist(body[0], body[1])
            gap = arr[-1]
            need(first >= LEAD + gap + 1, f"a patterned line's first run is {first:.0f} px, short of its lead-in ({LEAD} px) and gap")
            lead = cut(body, 0, LEAD)
            rest = cut(body, LEAD + gap, BS.path_len(body))
            run = rounded_len(rest, BEND)
            need(run >= MIN_RUN, f"a patterned line keeps {run:.0f} px after its lead-in, under the shortest run, {MIN_RUN} px")
            new = (f'<path class="ak-mark" d="M{F(lead[0][0])} {F(lead[0][1])}L{F(lead[-1][0])} {F(lead[-1][1])}" stroke-width="{w}"/>'
                   f'<path class="ak-mark" d="{BS.rounded_d(rest, BEND)}" stroke-width="{w}"{rnd} '
                   f'stroke-dasharray="{BS.fitted(t, w, run)}"/>')
        else:
            run = rounded_len(body, BEND)
            need(run >= MIN_RUN, f"a patterned line runs {run:.0f} px, under the shortest run, {MIN_RUN} px")
            new = (f'<path class="ak-mark" d="{BS.rounded_d(body, BEND)}" stroke-width="{w}"{rnd} '
                   f'stroke-dasharray="{BS.fitted(t, w, run)}"/>')
        marks = MARK_RE.sub(lambda m: new, marks, count=1)
    return marks, body


def anchor_at(pts, sign):
    """Where a connection's tag sits: the middle of its longest straight run (wire_marks' own place)."""
    (x, y), (ux, uy) = BS.tag_point(pts, LW, sign)
    return x, y, ux, uy


def text(x, y, s, cls, anchor="middle"):
    a = "" if anchor == "start" else f' text-anchor="{anchor}"'
    return f'<text class="{cls}" x="{F(x)}" y="{F(y)}"{a}>{e(s)}</text>'


def lines(x, y, rows, cls, anchor="middle", lh=LH):
    """Rows of text; a row that opens with a step number sets the number bold."""
    a = "" if anchor == "start" else f' text-anchor="{anchor}"'

    def row(r):
        m = re.match(r"(\d+) (.*)", r)
        return f'<tspan class="sn">{m.group(1)}</tspan> {e(m.group(2))}' if m and cls == "v" else e(r)

    if len(rows) == 1:
        return f'<text class="{cls}" x="{F(x)}" y="{F(y)}"{a}>{row(rows[0])}</text>'
    spans = "".join(f'<tspan x="{F(x)}"{"" if i == 0 else f" dy={chr(34)}{lh}{chr(34)}"}>{row(r)}</tspan>' for i, r in enumerate(rows))
    return f'<text class="{cls}" x="{F(x)}" y="{F(y)}"{a}>{spans}</text>'


def loop_id(x, y, lid, kind):
    """The loop's number in bold and its kind, on one line, inside the loop."""
    return (f'<text class="id" x="{F(x)}" y="{F(y)}" text-anchor="middle">{e(lid)}'
            f'<tspan class="kd"> {e(kind)}</tspan></text>')


def verb_at(pts, sign, words, side):
    """A connection's words beside its tag: above or below a level run, left or right of an upright one."""
    x, y, ux, uy = anchor_at(pts, sign)
    if side == "above":
        return lines(x, y - 15 - (len(words) - 1) * LH, words, "v")
    if side == "below":
        return lines(x, y + 26, words, "v")
    if side == "right":
        return lines(x + 15, y + 5 - (len(words) - 1) * LH / 2, words, "v", "start")
    return lines(x - 15, y + 5 - (len(words) - 1) * LH / 2, words, "v", "end")


class Pill:
    """A variable as a pill with its short name inside (System 1's station_block, DR-36), or a thin pill for a station
    that is no numbered variable (a conceptual loop's)."""

    def __init__(self, label, cx, cy, pw=PW, thin=False, cls=""):
        self.rows = wrap(label, pw - 2 * PAD)
        self.h = max(len(self.rows) * LH + 22, 44)
        self.cx, self.cy, self.pw, self.thin, self.cls = cx, cy, pw, thin, cls

    @property
    def top(self):
        return self.cy - self.h / 2

    @property
    def bot(self):
        return self.cy + self.h / 2

    @property
    def left(self):
        return self.cx - self.pw / 2

    @property
    def right(self):
        return self.cx + self.pw / 2

    def svg(self):
        c = "pl" + (" th" if self.thin else "") + (" " + self.cls if self.cls else "")
        ty = self.cy - (len(self.rows) - 1) * LH / 2 + 15 * 0.35
        return (f'<rect class="{c}" x="{F(self.left)}" y="{F(self.top)}" width="{F(self.pw)}" height="{F(self.h)}" rx="{F(self.h / 2)}"/>'
                + lines(self.cx, ty, self.rows, "t"))


def svg_wrap(body, h, label=None, w=W):
    return (f'<svg class="sv" viewBox="0 0 {w} {F(h)}" width="{w}" height="{F(h)}" aria-hidden="true" focusable="false">'
            f'{body}</svg>')


def step_words(n, lid, extra=()):
    """A connection's words: the step number in bold, then the type for money, information or ownership (Rule 15.4),
    then the verb its sign gives, or decides for authority. A typed step takes two rows."""
    l = link(lid)
    word = "decides" if l["type"] == "authority" else BS.verb(l["polarity"])
    lead = f"{n} " if n else ""
    if l["type"] in ("money", "information", "ownership"):
        return [f"{lead}{l['type']},", word, *extra]
    return [f"{lead}{word}", *extra]


def two_loop(codes, lids, numbered=True, weakest=None, inside=None, labels=None, thin=False, grades=None, widths=None,
             hollow=False, scale=None, a_in=0, top=0):
    """A loop of two variables, side by side, its first step arching over the top and its second under the bottom
    (System 1's n == 2 cycle, drawn for the 296 px artboard). inside is (loop ID, kind word), set on one line inside the
    loop; a_in moves the second step's arrival along the first pill, to free room under it. Returns (body, h, pills)."""
    labels = labels or [short(c) for c in codes]
    pw = [PW, PW] if not scale else [PW * s for s in scale]
    rows_h = [max(len(wrap(lb, p - 2 * PAD)) * LH + 22, 44) for lb, p in zip(labels, pw)]
    run_y = top + 28 + (LH if weakest == 0 else 0)
    cy = run_y + RISE + max(rows_h) / 2
    a = Pill(labels[0], 2 + pw[0] / 2, cy, pw[0], thin)
    b = Pill(labels[1], W - 2 - pw[1] / 2, cy, pw[1], thin)
    out = []
    bot_y = max(a.bot, b.bot) + RISE
    p1 = [(a.cx, a.top - 2), (a.cx, run_y), (b.cx, run_y), (b.cx, b.top - 2)]
    p2 = [(b.cx, b.bot + 2), (b.cx, bot_y), (a.cx + a_in, bot_y), (a.cx + a_in, a.bot + 2)]
    for i, (pts, lid, side) in enumerate(((p1, lids[0], "above"), (p2, lids[1], "below"))):
        l = link(lid) if lid else {"polarity": None, "evidence": None, "delay": None}
        g = (grades or {}).get(i, l["evidence"])
        w = (widths or {}).get(i, LW)
        m, _ = conn(pts, g, l["polarity"], l["delay"], hollow=hollow, w=w)
        out.append(f'<g class="wr">{m}</g>')
        if lid:
            extra = ("weakest step",) if weakest == i else ()
            out.append(verb_at(pts, l["polarity"], step_words(i + 1 if numbered else 0, lid, extra), side))
    out.append(a.svg() + b.svg())
    if inside:
        out.append(loop_id(W / 2, run_y + 28, *inside))
    h = bot_y + 34 + (LH if weakest == 1 else 0)
    return "".join(out), h, (a, b)


def three_loop(codes, lids, numbered=True, weakest=None, grades=None, inside=None, hollow=False, labels=None, thin=False):
    """A loop of three variables: the first centered at the top, the second below it to the right and the third to the
    left. Steps 1 and 3 run straight between overlapping pills; step 2 arches under the bottom row. Returns (body, h)."""
    labels = labels or [short(c) for c in codes]
    hs = [max(len(wrap(lb, PW - 2 * PAD)) * LH + 22, 44) for lb in labels]
    y1 = 4 + hs[0] / 2
    gap = 92
    y2 = y1 + hs[0] / 2 + gap + max(hs[1], hs[2]) / 2
    p1 = Pill(labels[0], W / 2, y1, PW, thin)
    p2 = Pill(labels[1], W - 2 - PW / 2, y2, PW, thin)
    p3 = Pill(labels[2], 2 + PW / 2, y2, PW, thin)
    xr = (max(p1.left, p2.left) + min(p1.right, p2.right)) / 2
    xl = (max(p1.left, p3.left) + min(p1.right, p3.right)) / 2
    bot_y = max(p2.bot, p3.bot) + RISE
    paths = [([(xr, p1.bot + 2), (xr, p2.top - 2)], "right"),
             ([(p2.cx, p2.bot + 2), (p2.cx, bot_y), (p3.cx, bot_y), (p3.cx, p3.bot + 2)], "below"),
             ([(xl, p3.top - 2), (xl, p1.bot + 2)], "left")]
    out = []
    for i, ((pts, side), lid) in enumerate(zip(paths, lids)):
        l = link(lid) if lid else {"polarity": None, "evidence": None, "delay": None}
        g = (grades or {}).get(i, l["evidence"])
        m, _ = conn(pts, g, l["polarity"], l["delay"], hollow=hollow)
        out.append(f'<g class="wr">{m}</g>')
        if lid:
            extra = ("weakest step",) if weakest == i else ()
            out.append(verb_at(pts, l["polarity"], step_words(i + 1 if numbered else 0, lid, extra), side))
    out.append(p1.svg() + p2.svg() + p3.svg())
    if inside:
        out.append(loop_id(W / 2, max(p2.bot, p3.bot) + 28, *inside))
    h = bot_y + 34 + (LH if weakest == 1 else 0)
    return "".join(out), h


def read_aloud(codes, lids, closes=True):
    """More or less at each variable, carrying the signs along the chain from a rise at the first (System 1's
    read_aloud, from the atlas's signs)."""
    up, parts = True, []
    for i, code in enumerate(codes):
        name = lc(short(code))
        parts.append(("more " if up else "less ") + name)
        if i < len(lids) and link(lids[i])["polarity"] == "-":
            up = not up
    line = ", ".join(parts)
    if closes:
        line += ", and back to " + ("more " if up else "less ") + lc(short(codes[0]))
    return line[0].upper() + line[1:] + "."


# ---------------------------------------------------------------------------------------------------------------
# Styles. Each plate carries only the rules its own markup uses (chapter 13's way, D2-1732). Every size comes from a
# type token or a chart type token, every color from a theme token.
# ---------------------------------------------------------------------------------------------------------------
CSS = {k: C13.CSS[k] for k in ("dnp", "evr", "ev", "gr", "chip", "k", "rs", "gw", "nw2", "fx", "src", "nt", "hed", "sub", "mk")}
INK = "var(--oa-color-graphic-essential)"
CSS.update({
    "sv": (".sv{display:block;max-width:100%;height:auto;overflow:visible}"
           ".sv text{font-family:var(--oa-font-family-reading);font-size:var(--oa-chart-type-label);fill:var(--oa-color-text-primary)}"
           f".sv .t{{font-weight:var(--oa-font-weight-semibold)}}.sv .v{{font-weight:var(--oa-font-weight-regular)}}"
           f".sv .pl{{fill:var(--oa-color-surface);stroke:{INK};stroke-width:2px}}.sv .pl.th{{stroke-width:1px}}"
           f".sv .ak-mark{{fill:none;stroke:{INK}}}.sv .hd,.sv .tg polygon{{fill:{INK}}}.sv .tg .sg{{fill:var(--oa-color-surface)}}"
           f".sv .tk{{stroke:{INK};stroke-width:2px}}.sv .rl{{fill:none;stroke:{INK};stroke-width:1px}}"),
    "id": ".sv .id{font-weight:var(--oa-font-weight-bold)}.sv .kd{font-weight:var(--oa-font-weight-regular)}",
    "sn": ".sv .sn{font-weight:var(--oa-font-weight-bold)}",
    "dm": f".sv .dm{{fill:var(--oa-color-surface);stroke:{INK};stroke-width:2px}}",
    "fr": (".sv .fr{fill:none;stroke:var(--oa-color-border-strong);stroke-width:1px}"
           ".sv .fl{fill:var(--oa-color-text-secondary)}"),
    "nm": (".sv .nm circle{fill:var(--oa-chart-color-chip-fill)}.sv .nm text{fill:var(--oa-chart-color-chip-label);"
           "font-weight:var(--oa-font-weight-bold);font-variant-numeric:tabular-nums}"),
    "dg": ".dg{margin:4px 0 0}.dg+.ra{margin-top:10px}",
    "ra": f".ra{{{C13.CAP};color:var(--oa-color-text-secondary);max-width:30em}}",
    "kw": (f".kw{{list-style:none;margin:0;padding:0;font:var(--oa-type-body-small)}}"
           ".kw li{padding:8px 0;border-top:1px solid var(--oa-color-border-hairline)}.kw li:first-child{border-top:0;padding-top:0}"
           ".kw b{font-weight:var(--oa-font-weight-semibold)}"),
    "q": (".q{font:italic 400 var(--oa-type-body-small-font-size)/1.6 var(--oa-font-family-quote);margin:0}"),
    "vc": ".vc+.vc{margin-top:18px;padding-top:14px;border-top:1px solid var(--oa-color-border-hairline)}.vc .sv{margin:2px 0 8px}",
    "two": ".fx>div{min-width:0}",
    "pk": (".sv .pk{stroke:var(--oa-color-palette-prussian)}.sv .gk{stroke:var(--oa-color-palette-verdigris)}"
           ".sv .sk{stroke:var(--oa-color-palette-stone)}.sv .pkf{fill:var(--oa-color-palette-prussian)}"
           ".sv .gkf{fill:var(--oa-color-palette-verdigris)}.sv .skf{fill:var(--oa-color-palette-stone)}"),
    "kb": ".kb{margin-top:16px}",
    "sw": (".sw{display:inline-block;width:14px;height:14px;vertical-align:-2px;margin-right:6px}"
           ".sw.gkf{background:var(--oa-color-palette-verdigris)}.sw.pkf{background:var(--oa-color-palette-prussian)}"
           ".sw.skf{background:var(--oa-color-palette-stone)}"),
})


def styled(body):
    used = set()
    for cls in re.findall(r'class="([^"]+)"', body):
        used.update(cls.split())
    if "fx" in used:
        used.add("two")
    rules = [C13.BASE] + [css for k, css in CSS.items() if k in used]
    return "<style>" + "".join(rules) + "</style>"


# ---------------------------------------------------------------------------------------------------------------
# The book of plates
# ---------------------------------------------------------------------------------------------------------------
class Book:
    def __init__(self):
        self.files, self.manifest, self.examples = {}, {}, []

    def add(self, sid, body, *, rule, alt, illustrative=False, readable=False, notes=""):
        need(sid not in self.files, f"duplicate specimen {sid}")
        body = re.sub(r">\s+<", "><", body.strip())
        self.files[sid] = (f"<!-- {sid}: Oath & Action guide, Edition 06, chapter 15. Systems designer, {WRITTEN}. Written by "
                           f"work/build/scripts/phase-3/phase3_ch15_build.py. -->\n" + styled(body) + f'\n<div class="p">{body}</div>\n')
        m = {"chapter": "15", "rule": rule, "width_px": None, "alt": " ".join(alt.replace("'", "’").split()),
             "illustrative": bool(illustrative), "notes": notes}
        if readable:
            m["readable"] = True
        self.manifest[sid] = m

    def log(self, where, example, domain, states=(), level="federal"):
        """Rule 01.12's example log, counted for Rule 01.9 (DR-229)."""
        self.examples.append({"where": where, "example": example, "domain": domain, "states": list(states), "level": level})


def src(what):
    return f'<p class="src">Source: {e(ATLAS)}, {e(what)}, snapshot of {SNAP}, United States.</p>'


def fig(svg, ra=None):
    return f'<div class="dg">{svg}</div>' + (f'<p class="ra">{e(ra)}</p>' if ra else "")


def hed(kind, rid, title=None):
    t = f'<span>“{e(title)}”</span>' if title else ""
    return f'<p class="hed">{chip(kind, rid)}{t}</p>'


def least_certain(ids):
    return C13.least_certain(ids)


# ===============================================================================================================
# The opener: one loop, one authority line and one boundary, each part numbered to the rule that sets it
# ===============================================================================================================
def numeral(n, x, y):
    return f'<g class="nm"><circle cx="{F(x)}" cy="{F(y)}" r="11"/>{text(x, y + 5, str(n), "")}</g>'


def opener(book):
    lp = LOOP["R13"]
    need(lp["links"] == ["L11", "L12"] and lp["type"] == "R" and minus_count(lp["links"]) == 2, "Loop R13 changed")
    le = link("LE02")
    need((le["type"], le["from"], le["to"], le["polarity"], le["evidence"], le["loops"]) == ("authority", "D1", "EC2", None, "documented", []),
         "connection LE02 changed")
    need(node("EC2")["layer"] == "economy" and node("D1")["layer"] == "core", "the layers of D1 or EC2 changed")
    body, h, (a, b) = two_loop(["D1", "D2"], ["L11", "L12"], inside=("R13", "reinforcing"), a_in=22, top=4)
    # the economy layer under the core: a 1 px rule with each layer's name, broken where the authority line crosses it
    xa = a.left + 38
    run2 = a.bot + RISE
    fy = run2 + 52
    ec = Pill(short("EC2"), 0, 0, 196)
    ec.cx, ec.cy = 2 + 98, fy + 22 + ec.h / 2
    pts = [(xa, a.bot + 2), (xa, ec.top - 2)]
    m, _ = conn(pts, "documented", None, le["delay"], authority=True)
    fr = (f'<path class="fr" d="M0 {F(fy)}H{F(xa - 7)}M{F(xa + 7)} {F(fy)}H{W}"/>'
          + text(W, fy - 8, "Core layer", "fl", "end") + text(W, fy + 20, "Economy layer", "fl", "end"))
    lab = text(xa + 10, run2 + 24, "decides", "v", "start")
    nums = (numeral(1, a.left + 6, a.top - 1) + numeral(2, W / 2 + 46, 15) + numeral(3, W / 2, a.cy)
            + numeral(4, xa - 20, a.bot + 30) + numeral(5, W / 2 - 4, fy) + numeral(6, W / 2 + 64, run2 + 20))
    total = ec.bot + 4
    svg = svg_wrap(body + f'<g class="wr">{m}</g>' + lab + fr + ec.svg() + nums, total)
    parts = [("A variable, by its short name", "15.2"), ("A sign tag and the word for which way", "15.3"),
             ("The loop’s number and kind", "15.6"), ("Authority, with no sign", "15.5"),
             ("A boundary between layers", "15.9"), ("A dashed line for a plausible step", "13.4")]
    lst = "".join(f"<li>{C13.mk(n)} {e(w)}, Rule {r}</li>" for n, (w, r) in enumerate(parts, 1))
    body = (f'<div class="fx two"><div>{hed("Loop", "R13", lp["title"])}{fig(svg)}</div>'
            f'<div><p class="k">What each numbered part says</p><ol class="kw">{lst}</ol></div></div>'
            + src("loop R13 and connections L11, L12 and LE02"))
    book.add("s-15-opener", body, rule=None, readable=True,
             alt=(f"Loop R13 from our systems atlas, “{lp['title']}”, drawn as two pills, Congressional capacity and Executive "
                  "unilateralism, with an arrow over the top marked minus, lowers, and one under the bottom marked minus, lowers, "
                  "drawn dashed. The loop’s number and the word Reinforcing sit inside it. A line with an open diamond and the word "
                  "decides runs from Congressional capacity down across a rule into the economy layer, to Public investment in "
                  "research and infrastructure. Six numerals tie the parts to a list: a variable, Rule 15.2; a sign tag and its "
                  "word, Rule 15.3; the loop’s number and kind, Rule 15.6; authority with no sign, Rule 15.5; a boundary between "
                  "layers, Rule 15.9; a dashed line for a plausible step, Rule 13.4."),
             notes="Chapter 15's opener: one loop, one authority line and the core and economy layers, from the atlas's records "
                   "read by script; lines by the atlas build's wire_marks with the 28 px lead-in.")
    book.log("opener", "Loop R13, Congress and the president", "D04")
    return {"specimen": "s-15-opener",
            "caption": "Loop R13 from our systems atlas, with the authority line that leaves it and the layer it reaches. "
                       "Each numeral marks one part of the grammar, and the list names the rule that sets it."}


# ---------------------------------------------------------------------------------------------------------------
# More of the kit: one connection as a card, a boundary rule, a frame, a loop of drawn steps
# ---------------------------------------------------------------------------------------------------------------
CARD_PW = 170
CARD_RUN = 92


def boundary(y, gaps, above=None, below=None, x0=0, x1=W):
    """A boundary between layers: a 1 px rule broken 7 px each side of every line that crosses it, with each layer's
    name at its right end (Rule 15.9)."""
    d, x = [], x0
    for g in sorted(gaps):
        d.append(f"M{F(x)} {F(y)}H{F(g - 7)}")
        x = g + 7
    d.append(f"M{F(x)} {F(y)}H{F(x1)}")
    out = f'<path class="fr" d="{"".join(d)}"/>'
    if above:
        out += text(x1, y - 8, above, "fl", "end")
    if below:
        out += text(x1, y + 20, below, "fl", "end")
    return out


def frame(x, y, w, h, name, gaps_top=(), gaps_bot=()):
    """A layer or cluster frame: a 1 px rectangle, its name inside at top left, broken where a line crosses it."""
    def edge(yy, gaps):
        d, cur = [], x
        for g in sorted(gaps):
            d.append(f"M{F(cur)} {F(yy)}H{F(g - 7)}")
            cur = g + 7
        d.append(f"M{F(cur)} {F(yy)}H{F(x + w)}")
        return "".join(d)
    d = edge(y, gaps_top) + edge(y + h, gaps_bot) + f"M{F(x)} {F(y)}V{F(y + h)}M{F(x + w)} {F(y)}V{F(y + h)}"
    return f'<path class="fr" d="{d}"/>' + text(x + w - 10, y + 22, name, "fl", "end")


def card(a_code, b_code, lid, layers=None, words=None, sign=None, authority=None, grade=None, labels=None, pw=CARD_PW,
         head=0):
    """One connection, drawn downward from one pill to the next, its words to the right of the line. layers names the
    layers above and below a boundary the line crosses. Returns (body, h, x of the line)."""
    l = link(lid) if lid else {}
    sign = l.get("polarity") if sign is None else (sign or None)
    authority = (l.get("type") == "authority") if authority is None else authority
    la, lb = labels or (short(a_code), short(b_code))
    a = Pill(la, 2 + pw / 2, 0, pw)
    a.cy = head + a.h / 2 + 2
    run = CARD_RUN + (24 if layers else 0)
    b = Pill(lb, 2 + pw / 2, 0, pw)
    b.cy = a.bot + run + b.h / 2
    x = a.cx
    pts = [(x, a.bot + 2), (x, b.top - 2)]
    m, _ = conn(pts, grade or l.get("evidence"), sign, l.get("delay"), authority=authority)
    if words is None:
        words = ["decides"] if authority else step_words(0, lid)
    lab = (lines(x + 15, (a.bot + b.top) / 2 + 5, words, "v", "start") if authority
           else verb_at(pts, sign, words, "right"))
    out = [f'<g class="wr">{m}</g>', lab]
    if layers:
        out.append(boundary(b.top - 26, [x], layers[0], None) + text(W, b.top - 6, layers[1], "fl", "end"))
    out.append(a.svg() + b.svg())
    return "".join(out), b.bot + 2, x


def drawn_loop(n, stations, steps, numbered=True, weakest=None, inside=None, thin=False):
    """A loop drawn from explicit steps, for a mechanism with no numbered connections (a conceptual loop) or a loop drawn
    against the record in a failure plate. stations are labels; steps are dicts of sign, grade, delay, hollow."""
    if n == 3:
        hs = [max(len(wrap(lb, PW - 2 * PAD)) * LH + 22, 44) for lb in stations]
        y1 = 4 + hs[0] / 2
        y2 = y1 + hs[0] / 2 + 92 + max(hs[1], hs[2]) / 2
        p1, p2, p3 = Pill(stations[0], W / 2, y1, PW, thin), Pill(stations[1], W - 2 - PW / 2, y2, PW, thin), Pill(stations[2], 2 + PW / 2, y2, PW, thin)
        xr = (max(p1.left, p2.left) + min(p1.right, p2.right)) / 2
        xl = (max(p1.left, p3.left) + min(p1.right, p3.right)) / 2
        bot_y = max(p2.bot, p3.bot) + RISE
        paths = [([(xr, p1.bot + 2), (xr, p2.top - 2)], "right"),
                 ([(p2.cx, p2.bot + 2), (p2.cx, bot_y), (p3.cx, bot_y), (p3.cx, p3.bot + 2)], "below"),
                 ([(xl, p3.top - 2), (xl, p1.bot + 2)], "left")]
        pills = [p1, p2, p3]
        mid = (W / 2, max(p2.bot, p3.bot) + 28)
    else:
        raise SystemExit("drawn_loop draws three stations")
    out = []
    for i, ((pts, side), st) in enumerate(zip(paths, steps)):
        m, _ = conn(pts, st.get("grade"), st["sign"], st.get("delay"), hollow=st.get("hollow", False))
        out.append(f'<g class="wr">{m}</g>')
        word = BS.verb(st["sign"])
        rows = [f"{i + 1} {word}" if numbered else word] + (["weakest step"] if weakest == i else [])
        out.append(verb_at(pts, st["sign"], rows, side))
    out.append("".join(p.svg() for p in pills))
    if inside:
        out.append(loop_id(*mid, *inside))
    return "".join(out), bot_y + 34 + (LH if weakest == 1 else 0)


def kw(items):
    return '<ul class="kw">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def say_link(lid):
    """A connection's typed chip and its name in quotation marks, with its grade word (Rules 13.2, 13.3, 13.9)."""
    l = link(lid)
    return f'{chip("Connection", lid)} “{e(l["name"])}”. {grade_word(l["evidence"])}.'


TOKEN_LINE = "oa.color.graphic.essential.onNewsprint"


# ===============================================================================================================
# Group 1. Reading a systems drawing
# ===============================================================================================================
def rule_15_1(book):
    lp = LOOP["B1a"]
    need(lp["links"] == ["L17", "L16"] and lp["type"] == "B", "Loop B1a changed")
    need([link(x)["evidence"] for x in lp["links"]] == ["plausible", "well-supported"], "Loop B1a's grades changed")
    limits = V7["methods"]["limits"]
    q = "Loops show structure: the size of any effect comes from the studies attached to each connection, and no whole loop has a measured strength."
    need(q in limits, "the atlas's limits no longer say no loop has a measured strength")
    g = least_certain(lp["links"])
    body, h, _ = two_loop(["E1", "D4"], lp["links"], inside=("B1a", "balancing"))
    svg = svg_wrap(body, h)
    words = kw([f"Every connection draws at 2 px. The dashed line says {chip('Connection', 'L17')} is plausible; the solid "
                f"line says {chip('Connection', 'L16')} is well supported.",
                "Both variables take the same pill, sized only by its label.",
                "Nothing in the drawing measures, so it carries no key for size."])
    body = (diagram_label(g, f"{GRADE[g][1]}, the grade of the loop’s least certain step")
            + f'<div class="fx two"><div>{hed("Loop", "B1a", lp["title"])}{fig(svg, read_aloud(["E1", "D4"], lp["links"]))}</div>'
            f'<div><p class="k">What the drawing holds</p>{words}</div></div>' + src("loop B1a and connections L17 and L16"))
    book.add("s-15-1-correct", body, rule="15.1", readable=True,
             alt=(f"Loop B1a from our systems atlas, “{lp['title']}”, drawn as two pills of one size, Policy tilt to insiders "
                  "and Oversight and enforcement. Step 1, dashed, runs over the top with a plus tag and the word raises; step 2, "
                  "solid, runs under the bottom with a minus tag and the word lowers. Both lines are 2 px. Beside it, three notes "
                  "say every connection draws at 2 px, both variables take the same pill, and nothing in the drawing measures."),
             notes="Lines by the atlas build's wire_marks at 2 px with the 28 px lead-in; pills sized only by their labels.")
    book.log("15.1 correct", "Loop B1a, oversight", "D05")
    fb, fh, _ = two_loop(["E1", "D4"], lp["links"], inside=("B1a", "balancing"), widths={1: 6}, scale=[1.2, 1.0])
    fail = dnp() + hed("Loop", "B1a", lp["title"]) + fig(svg_wrap(fb, fh))
    book.add("s-15-1-failure", fail, rule="15.1",
             alt=(FC + "Loop B1a with its second step drawn 6 px thick, three times the first, and the pill for Policy tilt "
                  "to insiders drawn larger than the other, with no key to say what the width or the size measures."),
             notes="Labeled failure: width and size used as if they measured strength, with no measure behind them and no key.")
    return {
        "id": "15.1",
        "title": "Draw a mechanism as a systems graphic, and give width or size a measure only with a key.",
        "rule": [
            "A systems graphic draws how one change leads to another. Its variables, the quantities or conditions that can "
            "rise or fall, sit in labeled pills, and its connections run between them as arrows. It carries no axis and no "
            "scale. Every connection in a drawing takes one width, 2 px in a figure, and every variable takes one pill, sized "
            "only by its label, so neither can pass for an amount.",
            "Give a line’s width or a shape’s area a quantity only when a defined measure stands behind it, and print the key "
            "beside the drawing. A drawing whose widths carry measured flows, such as dollars moving between budgets, is a chart, "
            "and chapter 14 sets its rules.",
        ],
        "tokens": [TOKEN_LINE],
        "why": {"text": ["Our systems atlas records the direction and the evidence of each connection and gives no loop a size: "
                         f"“{q}” A thicker line or a larger pill would claim a strength the atlas never measured, and a reader "
                         "would take it at its word."],
                "basis": "Our systems atlas’s methods, its limits; design judgment"},
        "correct": {"specimen": "s-15-1-correct",
                    "caption": f"Loop B1a from our systems atlas, “{lp['title']}”, with both connections at 2 px and both "
                               "variables in pills of one size. The line patterns carry the grades, and nothing in the drawing measures."},
        "failure": {"specimen": "s-15-1-failure",
                    "caption": "<strong>Fails Rule 15.1.</strong> The second step is three times as thick and one pill is "
                               "larger, with no key, so the drawing claims sizes our systems atlas never measured."},
        "specs": [
            {"label": "Line width", "value": "One width in a drawing: 2 px in a figure, 3 px in a large drawing; only Rule 12.5’s red target draws heavier", "token": TOKEN_LINE},
            {"label": "Pill", "value": f"{PW} px wide on a {W} px drawing, with {PAD} px inside each end; 44 px tall, or the label’s rows at {LH} px plus 22; a 2 px outline"},
            {"label": "Width or area as a quantity", "value": "Only with a defined measure and a key beside the drawing"},
            {"label": "Measured flows", "value": "A chart, under chapter 14’s rules"},
        ],
        "related": ["10", "13", "14"],
        "builders": ["Draw every connection with the atlas build’s <code>wire_marks</code> at one width, and size each pill from "
                     "its wrapped label, so a pill grows only to hold its words."],
    }


def rule_15_2(book):
    picks = [("B3", "stock"), ("B1", "flow"), ("C3", "auxiliary")]
    for c, k in picks:
        need(node(c)["type"] == k, f"variable {c} is no longer a {k}")
    kinds = Counter(n["type"] for n in NODE.values())
    need(kinds == Counter({"stock": 31, "flow": 9, "auxiliary": 6, "driver": 5}), f"the atlas's kinds changed: {dict(kinds)}")
    from_loops = sum(1 for c in NODE if c in LOOP_NAME)
    need(GLOSS["Variable"].startswith("A quantity or condition in the model that can rise or fall."), "the atlas's definition of a variable changed")
    cards = []
    for c, _ in picks:
        p = Pill(short(c), 2 + 85, 0, 170)
        p.cy = p.h / 2 + 2
        svg = svg_wrap(p.svg(), p.h + 4, w=174)
        n = node(c)
        cards.append(f'<div class="vc">{svg}<p class="hed">{chip("Variable", c)}<span>{e(n["title"])}</span></p>'
                     f'<p class="sub">{e(kind_word(c))}</p><p class="nt">{e(n["increase_means"])}</p></div>')
    body = (f'<div class="fx two"><div>{"".join(cards[:2])}</div><div>{cards[2]}</div></div>'
            + src("variables B3, B1 and C3"))
    book.add("s-15-2-correct", body, rule="15.2", readable=True,
             alt=("Three variables from our systems atlas, each drawn as a pill with its short name, then its typed chip and "
                  "title, its kind and the atlas’s sentence on a higher value. "
                  + " ".join(f"Variable {c}, {node(c)['title']}, short name {short(c)}: {kind_word(c)}. {node(c)['increase_means']}"
                             for c, _ in picks)),
             notes="Short names by DR-185's rule, read from the loops that hold each variable; kinds and sentences from each "
                   "variable's own record.")
    for c, d in (("B3", "D10"), ("B1", "D03"), ("C3", "D02")):
        book.log("15.2 correct", f"Variable {c}", d)
    l44 = link("L44")
    need((l44["from"], l44["to"], l44["polarity"]) == ("C4", "B5", "-"), "connection L44 changed")
    need(node("B5")["increase_means"] == "A higher value means turnout is more similar across income groups.", "variable B5's sentence changed")
    fb, fh, _ = card("C4", "B5", "L44", labels=(short("C4"), "Turnout"))
    fail = dnp() + fig(svg_wrap(fb, fh))
    book.add("s-15-2-failure", fail, rule="15.2",
             alt=(FC + "A connection from Incumbent control of election rules, with a minus tag and the word lowers, into a pill "
                  "labeled Turnout, with no chip, no kind and no sentence on what a higher value means."),
             notes="Labeled failure: B5's pill cut to one word, so its minus sign reads as fewer voters.")
    return {
        "id": "15.2",
        "title": "Name each variable, its kind and what a higher value means.",
        "rule": [
            f"Our systems atlas defines a variable as “{GLOSS['Variable'].split('.')[0].lower()}”. Draw each one as a pill "
            "holding its short name, the name the atlas gives it on its loops, or its title where it sits in no loop. The first "
            "time a reader meets it, give its typed chip, its kind in words and the atlas’s own sentence on what a higher value means.",
            f"The atlas uses four kinds. A stock is an amount built up over time ({kinds['stock']} variables). A flow is an "
            f"amount per period ({kinds['flow']}). A condition, which the atlas calls auxiliary, is worked out from other "
            f"variables ({kinds['auxiliary']}). An outside driver is a force whose causes lie outside the model ({kinds['driver']}), "
            "and Rule 15.9 sets where it goes.",
        ],
        "tokens": ["oa.chart.type.label"],
        "why": {"text": ["A name alone leaves the direction open. Turnout could mean more voters or a smaller gap between "
                         "groups, and only the atlas’s sentence settles it for Variable B5: “" + node("B5")["increase_means"]
                         + "” Once a reader knows which way is up, the sign on every connection into the variable can be read."],
                "basis": "Our systems atlas’s glossary and model conventions; house rule H02"},
        "correct": {"specimen": "s-15-2-correct",
                    "caption": "A stock, a flow and a condition from our systems atlas, each with its pill, its typed chip, its "
                               "kind and the atlas’s sentence on what a higher value means."},
        "failure": {"specimen": "s-15-2-failure",
                    "caption": "<strong>Fails Rule 15.2.</strong> Variable B5 is cut to Turnout, with no kind and no sentence, "
                               "so its minus sign reads as fewer voters. The atlas’s variable is turnout equality, and the sign "
                               "says the gap between income groups widens."},
        "specs": [
            {"label": "Short name", "value": f"The atlas’s name on the loops that hold the variable ({from_loops} of {len(NODE)}), or its title ({len(NODE) - from_loops})"},
            {"label": "Label", "value": f"15 px, semibold, wrapped inside the pill with {PAD} px at each end", "token": "oa.chart.type.label"},
            {"label": "Kind", "value": "Stock, flow, condition or outside driver, in words, from the variable’s record"},
            {"label": "Higher value", "value": "The atlas’s sentence, quoted, where the reader meets the variable first"},
            {"label": "Chip", "value": "Variable and the ID, as Rule 13.9 sets"},
        ],
        "related": ["10", "13", "18"],
        "builders": ["Read the short name from the loops that hold the variable, and its kind and its higher-value sentence from "
                     "its own record. Print the sentence as the atlas writes it."],
    }


def rule_15_3(book):
    l46, l16 = link("L46"), link("L16")
    need((l46["polarity"], l46["from"], l46["to"]) == ("+", "B4", "B6") and (l16["polarity"], l16["from"], l16["to"]) == ("-", "D4", "E1"),
         "connection L46 or L16 changed")
    pos = GLOSS["Positive sign (+)"]
    need(pos.endswith("A positive sign does not mean a benefit."), "the atlas's positive sign entry changed")
    conv = V7["methods"]["model_conventions"]
    need("The sign on a connection gives direction only." in conv, "the atlas's sign convention changed")
    cols = []
    for lid in ("L46", "L16"):
        l = link(lid)
        b, h, _ = card(l["from"], l["to"], lid)
        cols.append(f'<div>{fig(svg_wrap(b, h))}<p class="hed">{chip("Connection", lid)}</p><p class="nt">{e(l["sign_meaning"])}</p></div>')
    key = kw([f"<b>+ raises</b>: the two move the same way.", f"<b>{MINUS} lowers</b>: they move in opposite directions.",
              "“A positive sign does not mean a benefit.”"])
    body = (f'<div class="fx two">{"".join(cols)}</div><div class="blk"><p class="k">Key</p>{key}</div>'
            + src("connections L46 and L16, and the glossary entry for a positive sign"))
    body = body.replace('class="blk"', 'class="kb"')
    book.add("s-15-3-correct", body, rule="15.3", readable=True,
             alt=(f"Two connections from our systems atlas. Connection L46 runs from Hostility toward the other party to Exposure "
                  f"to hostile political content, with a plus tag and the words information, raises; its sentence reads: "
                  f"{l46['sign_meaning']} Connection L16 runs from Oversight and enforcement to Policy tilt to insiders, with a "
                  f"minus tag and the word lowers; its sentence reads: {l16['sign_meaning']} A key says plus raises, the two move "
                  "the same way; minus lowers, they move in opposite directions; and quotes the atlas: a positive sign does not mean a benefit."),
             notes="Sentences on each sign from the connections' own records; the key's last line from the atlas glossary.")
    book.log("15.3 correct", "Connection L46, hostile content", "D10")
    book.log("15.3 correct", "Connection L16, watchdogs", "D05")
    fcols = []
    for lid in ("L46", "L16"):
        l = link(lid)
        b, h, _ = card(l["from"], l["to"], lid)
        fcols.append(f"<div>{fig(svg_wrap(b, h))}</div>")
    fkey = kw(["<b>+</b> Positive effect", f"<b>{MINUS}</b> Negative effect"])
    fail = dnp() + f'<div class="fx two">{"".join(fcols)}</div><div class="kb"><p class="k">Key</p>{fkey}</div>'
    book.add("s-15-3-failure", fail, rule="15.3",
             alt=(FC + "The same two connections over a key that reads plus, positive effect, and minus, negative effect."),
             notes="Labeled failure: the key reads a sign as good or bad news.")
    return {
        "id": "15.3",
        "title": "Read a plus or minus as the way two variables move together.",
        "rule": [
            "Each causal connection carries a sign tag. A plus means the two variables tend to move the same way, and a "
            "minus means they move in opposite directions, with the model’s other conditions held steady. The word beside the "
            "tag says it again: raises for a plus, lowers for a minus.",
            "Our systems atlas states the rule in its conventions: “The sign on a connection gives direction only.” Print the "
            "atlas’s sentence “A positive sign does not mean a benefit.” in every key that shows a sign.",
        ],
        "tokens": [TOKEN_LINE],
        "why": {"text": ["Readers bring the plus and minus of a ledger, where plus means gain. In the atlas a plus sits on "
                         "harmful changes too: when hostility toward the other party rises, exposure to hostile content tends to "
                         "rise, and that connection carries a plus."],
                "basis": "Our systems atlas’s glossary and model conventions"},
        "correct": {"specimen": "s-15-3-correct",
                    "caption": "Two connections from our systems atlas, each with its sign tag, its word and the atlas’s sentence "
                               "on what its sign means, over a key that quotes the atlas on a positive sign."},
        "failure": {"specimen": "s-15-3-failure",
                    "caption": "<strong>Fails Rule 15.3.</strong> The key calls a plus a positive effect, so more exposure to "
                               "hostile content reads as good news and stronger oversight reads as harm."},
        "specs": [
            {"label": "Sign tag", "value": "14 px body and 6 px point, 16 px tall, with an 8 by 2 px sign, on a 2 px line (Rule 10.10)"},
            {"label": "Word", "value": "Raises for a plus, lowers for a minus, 15 px beside the tag"},
            {"label": "Minus", "value": f"A true minus sign, {MINUS}, wherever the sign prints as text"},
            {"label": "Key", "value": "“A positive sign does not mean a benefit.”, quoted from the atlas"},
            {"label": "Authority", "value": "No tag (Rule 15.5)"},
        ],
        "related": ["10", "13"],
        "builders": ["Take the word from the sign alone, and print the connection’s own sentence on its sign where a reader needs "
                     "the reading in full."],
    }


def rule_15_4(book):
    types = Counter(l["type"] for l in LINK.values())
    need(types == Counter({"causal": 80, "money": 17, "information": 9, "authority": 7, "ownership": 5}), f"the connection types changed: {dict(types)}")
    picks = [("L28", "money"), ("L26", "information"), ("T12", "ownership")]
    for lid, t in picks:
        need(link(lid)["type"] == t, f"connection {lid} is no longer {t}")
    cols = []
    for lid, _ in picks:
        l = link(lid)
        b, h, _ = card(l["from"], l["to"], lid)
        cols.append(f'<div class="vc">{fig(svg_wrap(b, h))}<p class="nt">{say_link(lid)}</p></div>')
    body = (f'<div class="fx two"><div>{cols[0]}{cols[1]}</div><div>{cols[2]}</div></div>'
            + src("connections L28, L26 and T12"))
    book.add("s-15-4-correct", body, rule="15.4", readable=True,
             alt=("Three connections from our systems atlas, each with its type in words before its verb. "
                  + " ".join(f"Connection {lid} runs from {short(link(lid)['from'])} to {short(link(lid)['to'])}: "
                             f"{link(lid)['type']}, {BS.verb(link(lid)['polarity'])}, solid for {GRADE[link(lid)['evidence']][0].lower()}."
                             for lid, _ in picks)),
             notes="Types from each connection's record, printed before the verb; lines in their grade's pattern only.")
    book.log("15.4 correct", "Connection L28, local news", "D06")
    book.log("15.4 correct", "Connection L26, local reporting", "D01")
    book.log("15.4 correct", "Connection T12, home equity", "D08")
    fcols = []
    for (lid, _), cls in zip(picks, ("gk", "pk", "sk")):
        l = link(lid)
        b, h, _ = card(l["from"], l["to"], lid, words=[BS.verb(l["polarity"])])
        b = b.replace('<g class="wr">', f'<g class="wr {cls}">', 1).replace('class="ak-mark"', f'class="ak-mark {cls}"')
        fcols.append(f'<div class="vc">{fig(svg_wrap(b, h))}</div>')
    legend = kw([f'<span class="sw gkf"></span> Money', f'<span class="sw pkf"></span> Information', f'<span class="sw skf"></span> Ownership'])
    fail = dnp() + f'<div class="fx two"><div>{fcols[0]}{fcols[1]}</div><div>{fcols[2]}<p class="k">Key</p>{legend}</div></div>'
    book.add("s-15-4-failure", fail, rule="15.4",
             alt=(FC + "The same three connections with no type words, their lines in three colors, green for money, blue for "
                  "information and gray for ownership, keyed by colored squares."),
             notes="Labeled failure: color alone for a connection's type, which gray print and low color vision lose.")
    return {
        "id": "15.4",
        "title": "Say in words when a connection carries money, information or ownership.",
        "rule": [
            "Our systems atlas gives each connection a type. Most are causal: a change in one variable changes another. "
            f"Others name what moves along the line: money ({types['money']} connections), such as contributions or advertising "
            f"revenue; information ({types['information']}), such as news coverage or a feed; or ownership ({types['ownership']}), "
            "where one quantity is held inside another. Print the type in words before the verb, as in “money, lowers”, and in the key.",
            "Line patterns carry the evidence grade (Rule 13.4), so a type takes no pattern, width or color of its own. "
            "Authority, the fifth type, takes its own mark (Rule 15.5).",
        ],
        "tokens": [TOKEN_LINE],
        "why": {"text": ["Gray print and low color vision take away color first, and the patterns already have a job. A word "
                         "survives both, and it tells a reader what a connection is about before they open its record."],
                "basis": "Our systems atlas’s glossary; WCAG 2.2 SC 1.4.1"},
        "correct": {"specimen": "s-15-4-correct",
                    "caption": "Three connections from our systems atlas, one of each type that names what moves, each with its "
                               "type in words before its verb and its line in its grade’s pattern."},
        "failure": {"specimen": "s-15-4-failure",
                    "caption": "<strong>Fails Rule 15.4.</strong> Color alone tells the three types apart, so a reader with gray "
                               "print or low color vision cannot tell money from information."},
        "specs": [
            {"label": "Type word", "value": "Money, information or ownership, before the verb and a comma: money, lowers"},
            {"label": "Causal", "value": "No type word; the verb alone"},
            {"label": "Never", "value": "A color, a width or a pattern for a type"},
            {"label": "Authority", "value": "Its own mark and word (Rule 15.5)"},
        ],
        "related": ["05", "10", "13"],
        "builders": ["Print the type from the connection’s record, and leave the word out for a causal connection."],
    }


def rule_15_5(book):
    auth = [k for k, l in LINK.items() if l["type"] == "authority"]
    need(len(auth) == 7 and all(LINK[k]["polarity"] is None and LINK[k]["evidence"] == "documented" and not LINK[k]["loops"] for k in auth),
         "the authority connections changed: each must be documented, unsigned and in no loop")
    need(not any(k in lp["links"] for lp in LOOP.values() for k in auth), "a loop lists an authority connection")
    gl = GLOSS["Authority connection"]
    q = "It says who decides, without saying which way the decision goes, so it has no sign and never closes a loop."
    need(q in gl, "the atlas's definition of an authority connection changed")
    l13, l14 = link("LT13"), link("LT14")
    need((l13["from"], l13["to"], l14["from"], l14["to"]) == ("D4", "TC7", "D6", "TC7"), "connection LT13 or LT14 changed")
    need(node("TC7")["layer"] == "technology" and node("D4")["layer"] == node("D6")["layer"] == "core", "the layers changed")
    # two bodies, one decision: two authority lines into one variable across the core and technology boundary
    pw = 140
    a = Pill(short("D4"), 2 + pw / 2, 0, pw)
    b = Pill(short("D6"), W - 2 - pw / 2, 0, pw)
    top = max(a.h, b.h)
    a.cy = b.cy = top / 2 + 2
    t = Pill(short("TC7"), W / 2, 0, 172)
    t.cy = top + 4 + 120 + t.h / 2
    xs = [t.left + 32, t.right - 32]
    need(a.left + 29 < xs[0] < a.right - 6 and b.left + 6 < xs[1] < b.right - 29, "the authority lines miss their pills")
    out = []
    for x, src_p, lid in ((xs[0], a, "LT13"), (xs[1], b, "LT14")):
        m, _ = conn([(x, src_p.bot + 2), (x, t.top - 2)], "documented", None, link(lid)["delay"], authority=True)
        out.append(f'<g class="wr">{m}</g>')
    out.append(text(xs[0] - 12, a.bot + 54, "decides", "v", "end") + text(xs[1] + 12, b.bot + 54, "decides", "v", "start"))
    out.append(boundary(t.top - 30, xs, "Core layer", None) + text(W, t.top - 8, "Technology layer", "fl", "end"))
    out.append(a.svg() + b.svg() + t.svg())
    svg = svg_wrap("".join(out), t.bot + 4)
    words = kw([say_link("LT13"), say_link("LT14"), f"“{e(l13['sign_meaning'])}”"])
    body = (f'<div class="fx two"><div>{fig(svg)}</div><div><p class="k">Two bodies, one decision</p>{words}</div></div>'
            + src("connections LT13 and LT14"))
    book.add("s-15-5-correct", body, rule="15.5", readable=True,
             alt=(f"Two authority connections from our systems atlas. Lines from Oversight and enforcement and from State and local "
                  f"experimentation run down across the boundary between the core and technology layers into Use of pricing "
                  f"algorithms. Each is solid, ends in an open diamond, carries the word decides and no sign. Beside them: "
                  f"Connection LT13, {l13['name']}, documented; Connection LT14, {l14['name']}, documented; and the atlas’s "
                  f"words, {l13['sign_meaning']}"),
             notes="Both lines by wire_marks with authority=True: the open diamond, no tag, delay ticks; the boundary per Rule 15.9.")
    book.log("15.5 correct", "Connections LT13 and LT14, pricing software", "D06")
    fb, fh, _ = card("D4", "TC7", "LT13", layers=("Core layer", "Technology layer"), sign="-", authority=False, words=["lowers"])
    fail = dnp() + fig(svg_wrap(fb, fh))
    book.add("s-15-5-failure", fail, rule="15.5",
             alt=(FC + "The line from Oversight and enforcement to Use of pricing algorithms drawn as a causal arrow, with an "
                  "arrowhead, a minus tag and the word lowers."),
             notes="Labeled failure: an authority connection given a sign and an arrowhead, as if the atlas knew which way the enforcers will decide.")
    return {
        "id": "15.5",
        "title": "Draw authority with its open diamond and no sign, outside every loop.",
        "rule": [
            "An authority connection shows that one body holds legal power over something: it appoints, appropriates, preempts, "
            f"enforces or sets a rate. In our systems atlas’s words, “{q}” Draw it solid, end it in an open diamond, and print "
            "decides where a causal line prints its verb.",
            f"Keep it out of every loop drawing, even where it touches a variable the loop holds. All {len(auth)} of the "
            "atlas’s authority connections are documented, and none sits in a loop.",
        ],
        "tokens": [TOKEN_LINE],
        "why": {"text": ["A sign would claim to know how an enforcer or a legislature will use its power. The atlas records the "
                         "power and leaves the choice open, and a reader who met a diamond inside a loop would count a decision "
                         "as one more step that runs by itself."],
                "basis": "Our systems atlas’s glossary and model conventions"},
        "correct": {"specimen": "s-15-5-correct",
                    "caption": "Two authority connections from our systems atlas into one variable, each with its open diamond and "
                               "the word decides, crossing from the core layer to the technology layer."},
        "failure": {"specimen": "s-15-5-failure",
                    "caption": "<strong>Fails Rule 15.5.</strong> The enforcers’ line takes an arrowhead, a minus and lowers, so "
                               "it claims they will cut the use of pricing software. The atlas records only that they decide."},
        "specs": [
            {"label": "End", "value": "An open diamond, 14 by 11 px, in place of the arrowhead (Rule 10.10)"},
            {"label": "Line", "value": "Solid; every authority connection is documented"},
            {"label": "Word", "value": "Decides, where a causal line prints its verb"},
            {"label": "Sign", "value": "None"},
            {"label": "Loops", "value": "None; the build stops if any loop lists an authority connection"},
        ],
        "related": ["10", "13"],
        "builders": ["Draw it with <code>wire_marks</code> and its authority switch, which sets the diamond and leaves the tag off."],
    }


def rule_15_6(book):
    numbered = {k: p for k, p in LOOP.items() if p["links"]}
    bad = [k for k, p in numbered.items() if ("R" if minus_count(p["links"]) % 2 == 0 else "B") != p["type"]]
    need(not bad and len(numbered) == V7["meta"]["counts"]["loops_numbered"], f"loop kind and sign count disagree: {bad}")
    rg, bg = GLOSS["Reinforcing loop (R)"], GLOSS["Balancing loop (B)"]
    fb_ = GLOSS["Feedback loop"]
    need(fb_.endswith("either kind can produce good or harmful results."), "the atlas's feedback loop entry changed")
    picks = [("R18", "reinforcing", 2), ("B5", "balancing", 1)]
    cols = []
    for lid, kind, n in picks:
        lp = LOOP[lid]
        need(minus_count(lp["links"]) == n and len(lp["links"]) == 2, f"Loop {lid} changed")
        codes = [c for c, _ in lp["chain"]]
        b, h, _ = two_loop(codes, lp["links"], inside=(lid, kind))
        cols.append(f'<div>{hed("Loop", lid, lp["title"])}{fig(svg_wrap(b, h), read_aloud(codes, lp["links"]))}'
                    f'<p class="nt"><b>{words_n(n).capitalize()} minus sign{"s" if n != 1 else ""}</b>: {kind}.</p></div>')
    body = f'<div class="fx two">{"".join(cols)}</div>' + src("loops R18 and B5 and their connections")
    book.add("s-15-6-correct", body, rule="15.6", readable=True,
             alt=("Two loops from our systems atlas, each with its steps numbered 1 and 2, its number and kind inside it, a sentence "
                  "that reads it aloud and its count of minus signs. "
                  + " ".join(f"Loop {lid}, {LOOP[lid]['title']}: {read_aloud([c for c, _ in LOOP[lid]['chain']], LOOP[lid]['links'])} "
                             f"{words_n(n).capitalize()} minus sign{'s' if n != 1 else ''}, {kind}." for lid, kind, n in picks)),
             notes="Kinds checked against the count of minus signs on every numbered loop; read-aloud lines carry the signs around.")
    book.log("15.6 correct", "Loop R18, watchdogs", "D05")
    book.log("15.6 correct", "Loop B5, state experiments", "D03")
    lp = LOOP["R18"]
    codes = [c for c, _ in lp["chain"]]
    b, h, _ = two_loop(codes, lp["links"], numbered=False, inside=("A vicious", "cycle"))
    fail = dnp() + fig(svg_wrap(b, h))
    book.add("s-15-6-failure", fail, rule="15.6",
             alt=(FC + "Loop R18 drawn with no step numbers, no chip and no kind, and the words A vicious cycle inside it."),
             notes="Labeled failure: a judgment for a kind, and no numbers to read the loop in order.")
    return {
        "id": "15.6",
        "title": "Number a loop’s steps in order, and name it reinforcing or balancing.",
        "rule": [
            "A loop is “a chain of causes that returns to its starting variable”, in our systems atlas’s words. Number its steps "
            "from the variable the atlas starts it at, in the atlas’s order, and print its typed chip and its kind inside it: "
            "reinforcing, coded R, where the returning effect amplifies the first change, or balancing, coded B, where it pushes back.",
            "The minus signs give the kind. An even count, zero included, makes a loop reinforcing, and an odd count makes it "
            f"balancing, as on all {len(numbered)} of the atlas’s loops with numbered steps. Either kind can help or harm, "
            "depending on which way it runs.",
        ],
        "tokens": [TOKEN_LINE],
        "why": {"text": ["Numbers let a reader follow a loop in the atlas’s order, aloud or one step at a time on a stepper "
                         "(Rule 18.22). The count lets anyone check the kind from the drawing alone, and it shows how two minus "
                         "signs make a loop that feeds itself."],
                "basis": "Our systems atlas’s glossary and loop records; design judgment"},
        "correct": {"specimen": "s-15-6-correct",
                    "caption": "Two loops from our systems atlas, each with numbered steps, its number and kind inside it, a "
                               "sentence that reads it aloud and its count of minus signs."},
        "failure": {"specimen": "s-15-6-failure",
                    "caption": "<strong>Fails Rule 15.6.</strong> Loop R18 has no step numbers, no chip and no kind, and the "
                               "words inside it judge the loop. Its two minus signs make it reinforcing."},
        "specs": [
            {"label": "Step number", "value": "Bold, before the verb, from the atlas’s first connection: 1 raises"},
            {"label": "Inside the loop", "value": "The loop’s ID in bold, then reinforcing or balancing"},
            {"label": "Kind check", "value": "An even count of minus signs for reinforcing, odd for balancing; the build checks every numbered loop"},
            {"label": "Read aloud", "value": "One sentence that carries more or less around the loop and back to the start"},
        ],
        "related": ["11", "13", "18"],
        "builders": ["Number steps in the order of the loop’s own list of connections, and stop the build if a loop’s kind and "
                     "its count of minus signs disagree."],
    }


def rule_15_7(book):
    clos = Counter(p["closure"].split(":")[0].split(" with")[0] for p in LOOP.values())
    hyp = sorted(k for k, p in LOOP.items() if p["closure"] == "closed with a hypothesized step")
    con = sorted(k for k, p in LOOP.items() if p["closure"].startswith("conceptual"))
    need(hyp == ["R16", "R2"] and con == ["B2", "B3", "R9"] and len(LOOP) == 23, "the atlas's loop closures changed")
    closed = len(LOOP) - len(hyp) - len(con)
    lc_ = GLOSS["Loop closure"]
    q = "If any closing step is only a hypothesis, the whole loop stays uncertain."
    need(q in lc_, "the atlas's loop closure entry changed")
    r16, b3 = LOOP["R16"], LOOP["B3"]
    need([link(x)["evidence"] for x in r16["links"]] == ["well-supported", "hypothesis"], "Loop R16 changed")
    need(b3["evidence"] == "well-supported where entry is possible" and not b3["links"], "Loop B3 changed")
    b1, h1, _ = two_loop(["B2", "C3"], r16["links"], inside=("R16", "reinforcing"))
    st = [lab for lab, _ in b3["chain_labels"]]
    sg = [s_ for _, s_ in b3["chain"]]
    need(sg == ["+", "+", "-"], "Loop B3's signs changed")
    b2, h2 = drawn_loop(3, st, [{"sign": x, "hollow": True} for x in sg], numbered=False, inside=("B3", "balancing"), thin=True)
    col1 = (diagram_label("hypothesis", "not yet tested, the grade of the step that closes it")
            + hed("Loop", "R16", r16["title"]) + fig(svg_wrap(b1, h1)) + '<p class="nt"><b>Closes through a hypothesis</b>.</p>')
    col2 = (diagram_label("well-supported", "the atlas’s grade for the mechanism, where entry is possible")
            + hed("Loop", "B3", b3["title"]) + fig(svg_wrap(b2, h2)) + '<p class="nt"><b>No numbered chain</b>. Its three '
            'stations sit outside the atlas’s numbered variables.</p>')
    body = f'<div class="fx two"><div>{col1}</div><div>{col2}</div></div>' + src("loops R16 and B3")
    book.add("s-15-7-correct", body, rule="15.7", readable=True,
             alt=(f"Two loops from our systems atlas with their closure in words beside their grade. Loop R16, “{r16['title']}”, "
                  "labeled Hypothesis: a solid step from Local news supply to Electoral pressure, and a dotted step back that "
                  f"closes it; the words read Closes through a hypothesis. Loop B3, “{b3['title']}”, labeled Well supported: "
                  "three thin pills, Excess profits, Entry and Competitive pressure, joined by hollow lines with their signs; the "
                  "words read No numbered chain, its three stations sit outside the atlas’s numbered variables."),
             notes="R16's dotted closing step by wire_marks with the lead-in; B3's hollow lines and thin pills as Rule 13.4 sets.")
    book.log("15.7 correct", "Loop R16, local news", "D01")
    book.log("15.7 correct", "Loop B3, new competitors", "D06")
    fb, fh = drawn_loop(3, st, [{"sign": x, "grade": "well-supported"} for x in sg], numbered=True, inside=("B3", "balancing"))
    fail = dnp() + diagram_label("well-supported", "strong research evidence") + hed("Loop", "B3", b3["title"]) + fig(svg_wrap(fb, fh))
    book.add("s-15-7-failure", fail, rule="15.7",
             alt=(FC + "Loop B3 drawn with three full pills, solid lines and numbered steps under a Well supported label, with no "
                  "word on how it closes."),
             notes="Labeled failure: a conceptual loop drawn as a closed chain of numbered connections.")
    return {
        "id": "15.7",
        "title": "Say how a loop closes, apart from how strong its evidence is.",
        "rule": [
            "Our systems atlas records how each loop closes, in one of three ways: every step a numbered connection; closed "
            "through a step graded hypothesis; or conceptual, a mechanism with no complete chain of numbered connections. Print "
            "the closure in words beside the loop’s grade. Draw a hypothesized step in dots, and each step of a conceptual loop "
            "as the hollow line of Rule 13.4, between thin pills, since its stations are not the atlas’s numbered variables.",
            f"Of the atlas’s {len(LOOP)} loops, {closed} close through numbered connections, {len(hyp)} close through a "
            f"hypothesis and {len(con)} are conceptual.",
        ],
        "tokens": ["oa.chart.grade.hypothesis", "oa.chart.grade.conceptual.rail"],
        "why": {"text": ["Closure and grade answer different questions. A conceptual loop can rest on strong research and still "
                         "lack a chain a reader can trace, and a loop that closes through a hypothesis stays uncertain as a whole, "
                         f"as the atlas defines closure: “{q}”"],
                "basis": "Our systems atlas’s glossary and loop records"},
        "correct": {"specimen": "s-15-7-correct",
                    "caption": "Loop R16, which closes through a hypothesis, and Loop B3, a conceptual loop, each with its "
                               "closure in words beside its grade."},
        "failure": {"specimen": "s-15-7-failure",
                    "caption": "<strong>Fails Rule 15.7.</strong> Loop B3 is drawn with solid numbered steps, so it passes for a "
                               "chain of connections. The atlas grades the mechanism well supported and gives it no numbered connection."},
        "specs": [
            {"label": "Every step numbered", "value": "The loop as Rule 15.6 draws it"},
            {"label": "Closes through a hypothesis", "value": "The closing step in dots, with these words beside the grade", "token": "oa.chart.grade.hypothesis"},
            {"label": "Conceptual", "value": "Hollow lines with their signs, 1 px pills, no step numbers or chips; “No numbered chain” beside the grade", "token": "oa.chart.grade.conceptual.rail"},
            {"label": "Counts", "value": f"{closed} closed, {len(hyp)} through a hypothesis, {len(con)} conceptual, as of the snapshot"},
        ],
        "related": ["10", "13"],
        "builders": ["Read the closure from the loop’s record, and draw a conceptual loop’s steps from its own list of stations "
                     "and signs, since it lists no connections."],
    }
