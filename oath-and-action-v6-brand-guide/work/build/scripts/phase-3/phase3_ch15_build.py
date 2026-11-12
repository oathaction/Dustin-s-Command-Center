"""Write chapter 15, Systems graphics: its words, its plates and its manifest.

Oath & Action Edition 06, Phase 3, rounds 1 and 2. Systems designer, November 12, 2026. The briefs are
work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md and 20261112_Phase-3-Round-2-Brief.md (systems designer); the
rule list the main session fixed (R7) is in work/handoffs/phase-3/20261112_Round-1-Systems-Designer-Notes.md, section
"Rule list". Round 1 built the grammar, Rules 15.1 to 15.10, and worked examples 1 and 2, Rules 15.13 (Loop R1) and
15.14 (Loop R8), with the opener. Round 2 (DR-244) builds the reforms on the drawing, Rules 15.11 and 15.12, and worked
examples 3 to 6, Rules 15.15 to 15.18. The rules of later rounds are listed in PLANNED and join as each round builds them.

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

The review fix pass (D3-480, D3-485): every plate is a 328 px true-size stage whose frame is the query container
oa-frame (manifest "frame_container"); a plate with words to set beside its drawing, or drawings to set side by side,
also takes a 680 px stage where its frame holds it (manifest "wide_px") and composes for it with @container oa-frame,
never a media query. No drawing scales. Every plate rule sits in one block, the chapter file's "plate_css", which the
shell prints once; no plate carries a style of its own.

Then runs its checks and stops on any failure: chapter 13's word checks (no em dash, no listed filler or corporate
word, no studio word or decision code in reader text, titles of fifteen words or fewer, failure captions led by
"Fails Rule 15.N.", failure plates with the do-not-publish band), no literal color, every font size from a token,
every atlas ID in a chip present in the model, every value the words print matched to the model, loop kind against
the count of minus signs on every numbered loop, no authority connection in any loop, Rule 01.9 over the example log,
red only on a reform's own targets, no effect total, every route dated or "Not checked", and the chapter's bytes
against its 0.60 MB ceiling.
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
ROUND_STOP = 600_000          # chapter 15's ceiling, 0.60 MB (guide_charts.MB is 1,000,000); the generator's own count of
                              # its fragments and chapter file stays under it, and the strict build reports the placed bytes

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
_SHELL = (ROOT / "work/build/scripts/phase-2/guide_build.py").read_text()
need(all(k in _SHELL for k in ('"plate_css"', '"wide_px"', '"frame_container"')),
     "the guide build no longer reads plate_css, wide_px or frame_container (D3-480), which these plates depend on")
FC = "Failure case: do not publish. "

# ---------------------------------------------------------------------------------------------------------------
# The rule list the main session fixed (R7). Rounds 1 and 2 build BUILT; the rest wait for their rounds.
# ---------------------------------------------------------------------------------------------------------------
BUILT = ["15.1", "15.2", "15.3", "15.4", "15.5", "15.6", "15.7", "15.8", "15.9", "15.10", "15.11", "15.12", "15.13",
         "15.14", "15.15", "15.16", "15.17", "15.18"]
PLANNED = {"15.19": "Let a reader step through a loop one connection at a time, with a still sequence.",
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


KIND_OF_TYPE = {"stock": "Stock", "flow": "Flow", "auxiliary": "Condition", "driver": "Outside driver"}


def kind_word(code):
    """The kind in words, from the atlas's kind_plain, cut at its first sentence, where it agrees with the atlas's type.
    Where they disagree (Variable D6, item 8 of the atlas V7.1 issue list) the page prints no kind (SD-4): None."""
    n = node(code)
    k = n["kind_plain"].split(".")[0]
    if not k.startswith(KIND_OF_TYPE[n["type"]]):
        return None
    return {"Condition (auxiliary)": "Condition, which the atlas calls auxiliary"}.get(k, k)


def gl(lid):
    """A connection's typed chip with its grade word, the record square before Documented (Rule 13.4, SD-1)."""
    return f'{chip("Connection", lid)}&#160;{grade_word(link(lid)["evidence"], gloss=False)}'


def label_for(ids, what="the grade of the least certain connection shown"):
    """The evidence label over a plate that draws atlas connections: the grade of its least certain one (Rule 13.1)."""
    g = least_certain(ids)
    low = [i for i in ids if link(i)["evidence"] == g]
    return diagram_label(g, f"{GRADE[g][1]}, {what}, Connection {low[0]}")


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


RED = ' data-red="working" data-red-job="where a reform acts"'   # Rule 12.5's marker, counted by the guide check


def conn(pts, grade=None, sign=None, delay=None, authority=False, hollow=False, w=LW, target=False):
    """One connection along pts, tail to tip, drawn by the atlas build's wire_marks: the line in its grade's pattern or
    hollow, delay ticks after the tail, the sign tag, the arrowhead or the authority diamond. A patterned line with ticks
    runs solid for LEAD px, then leaves its pattern's own gap and starts the fitted pattern on ink (D3-105).
    target=True draws Rule 12.5's red target: wire_marks' lit marks, a 4 px red line on a 6 px ink case with the 6 px
    tag, ticks and arrowhead, which the chapter's block shows only inside a group of class rt (round 2)."""
    t = "solid" if hollow else tex(grade)
    if target:
        need(t == "solid" and not authority, "a red target here draws a solid connection; a patterned one needs its lead-in at 6 px")
    marks, body, _ = BS.wire_marks(pts, grade or "documented", sign if sign in ("+", "-") else None, delay, w,
                                   lit=target, sketch=hollow, authority=authority)
    if not target:
        marks = re.sub(r'<path class="ak-case"[^>]*/>', "", marks).replace('<g class="lo">', "<g>")
    marks = (marks.replace(' fill="none"', "").replace(' stroke-linecap="butt"', "")
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


def loop_id(x, y, lid, kind, two=False):
    """The loop's typed ID in bold and its kind, inside the loop: "Loop R13" then "reinforcing" (house rule H11). Two
    lines inside a two-variable loop, where one would crowd the arch. A failure plate's own words pass with lid None."""
    if lid is None:
        return f'<text class="id" x="{F(x)}" y="{F(y)}" text-anchor="middle">{e(kind)}</text>'
    if two:
        return (f'<text class="id" x="{F(x)}" y="{F(y - 6)}" text-anchor="middle">Loop {e(lid)}'
                f'<tspan class="kd" x="{F(x)}" dy="{LH}">{e(kind)}</tspan></text>')
    return (f'<text class="id" x="{F(x)}" y="{F(y)}" text-anchor="middle">Loop {e(lid)}'
            f'<tspan class="kd"> {e(kind)}</tspan></text>')


def verb_at(pts, sign, words, side, big=False):
    """A connection's words beside its tag: above or below a level run, left or right of an upright one. big leaves room
    for a red target's 6 px tag, 22 px tall where the 2 px tag is 16."""
    x, y, ux, uy = anchor_at(pts, sign)
    k = 3 if big else 0
    if side == "above":
        return lines(x, y - 15 - k - (len(words) - 1) * LH, words, "v")
    if side == "below":
        return lines(x, y + 26 + k, words, "v")
    if side == "right":
        return lines(x + 15 + k, y + 5 - (len(words) - 1) * LH / 2, words, "v", "start")
    return lines(x - 15 - k, y + 5 - (len(words) - 1) * LH / 2, words, "v", "end")


def pill_w(label, pw=PW):
    """A pill's width: the base, or wide enough for the label's longest word with PAD at each end."""
    return max(pw, math.ceil(max(tw(w_, 600) for w_ in label.split()) + 2 * PAD + 2))


class Pill:
    """A variable as a pill with its short name inside (System 1's station_block, DR-36), or a thin pill for a station
    that is no numbered variable (a conceptual loop's)."""

    def __init__(self, label, cx, cy, pw=PW, thin=False, cls="", red=False, shared=False):
        pw = pill_w(label, pw)
        self.rows = wrap(label, pw - 2 * PAD)
        self.h = max(len(self.rows) * LH + 22, 44)
        self.cx, self.cy, self.pw, self.thin, self.cls = cx, cy, pw, thin, cls
        self.red, self.shared = red, shared

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
        """A red target pill (Rule 12.5) takes a 3 px red outline under data-red; a shared variable (Rule 15.15) is
        filled in ink with its name in the surface color, the one fill a pill takes."""
        c = ("pl" + (" th" if self.thin else "") + (" rp" if self.red else "") + (" sh" if self.shared else "")
             + (" " + self.cls if self.cls else ""))
        ty = self.cy - (len(self.rows) - 1) * LH / 2 + 15 * 0.35
        return (f'<rect class="{c}" x="{F(self.left)}" y="{F(self.top)}" width="{F(self.pw)}" height="{F(self.h)}" '
                f'rx="{F(self.h / 2)}"{RED if self.red else ""}/>' + lines(self.cx, ty, self.rows, "t ts" if self.shared else "t"))


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


def wr(m, target=False):
    """A connection's group: a red target's carries Rule 12.5's data-red and the class the chapter's block shows it by."""
    return f'<g class="wr rt"{RED}>{m}</g>' if target else f'<g class="wr">{m}</g>'


def two_loop(codes, lids, numbered=True, weakest=None, inside=None, labels=None, thin=False, grades=None, widths=None,
             hollow=False, scale=None, a_in=0, top=0, targets=(), shared=()):
    """A loop of two variables, side by side, its first step arching over the top and its second under the bottom
    (System 1's n == 2 cycle, drawn for the 296 px artboard). inside is (loop ID, kind word), set on one line inside the
    loop; a_in moves the second step's arrival along the first pill, to free room under it. targets names the
    connections and variables a reform acts on (Rule 12.5's red); shared names a variable another loop holds too
    (Rule 15.15). Returns (body, h, pills)."""
    labels = labels or [short(c) for c in codes]
    pw = [pill_w(lb, PW if not scale else PW * sc) for lb, sc in zip(labels, scale or [1, 1])]
    rows_h = [max(len(wrap(lb, p - 2 * PAD)) * LH + 22, 44) for lb, p in zip(labels, pw)]
    wrows = [len(step_words(1, x, ("weakest step",) if weakest == i else ())) if x else 1 for i, x in enumerate(lids)]
    run_y = top + 30 + (wrows[0] - 1) * LH + (3 if lids[0] in targets else 0)
    cy = run_y + RISE + max(rows_h) / 2
    a = Pill(labels[0], 2 + pw[0] / 2, cy, pw[0], thin, red=codes[0] in targets, shared=codes[0] in shared)
    b = Pill(labels[1], W - 2 - pw[1] / 2, cy, pw[1], thin, red=codes[1] in targets, shared=codes[1] in shared)
    out = []
    bot_y = max(a.bot, b.bot) + RISE
    p1 = [(a.cx, a.top - 2), (a.cx, run_y), (b.cx, run_y), (b.cx, b.top - 2)]
    p2 = [(b.cx, b.bot + 2), (b.cx, bot_y), (a.cx + a_in, bot_y), (a.cx + a_in, a.bot + 2)]
    for i, (pts, lid, side) in enumerate(((p1, lids[0], "above"), (p2, lids[1], "below"))):
        l = link(lid) if lid else {"polarity": None, "evidence": None, "delay": None}
        g = (grades or {}).get(i, l["evidence"])
        w = (widths or {}).get(i, LW)
        tg = bool(lid) and lid in targets
        m, _ = conn(pts, g, l["polarity"], l["delay"], hollow=hollow, w=w, target=tg)
        out.append(wr(m, tg))
        if lid:
            extra = ("weakest step",) if weakest == i else ()
            out.append(verb_at(pts, l["polarity"], step_words(i + 1 if numbered else 0, lid, extra), side, big=tg))
    out.append(a.svg() + b.svg())
    if inside:
        out.append(loop_id(W / 2, run_y + 28, *inside, two=True))
    h = bot_y + 34 + (wrows[1] - 1) * LH
    return "".join(out), h, (a, b)


def three_loop(codes, lids, numbered=True, weakest=None, grades=None, inside=None, hollow=False, labels=None, thin=False,
               targets=(), shared=(), top=0):
    """A loop of three variables: the first centered at the top, the second below it to the right and the third to the
    left. Steps 1 and 3 run straight between overlapping pills; step 2 arches under the bottom row. targets and shared
    as two_loop takes them. Returns (body, h)."""
    labels = labels or [short(c) for c in codes]
    hs = [max(len(wrap(lb, pill_w(lb) - 2 * PAD)) * LH + 22, 44) for lb in labels]
    y1 = top + 4 + hs[0] / 2
    gap = 108
    y2 = y1 + hs[0] / 2 + gap + max(hs[1], hs[2]) / 2
    kw_ = [dict(red=c in targets, shared=c in shared) for c in codes]
    p1 = Pill(labels[0], W / 2, y1, PW, thin, **kw_[0])
    p2 = Pill(labels[1], W - 2 - pill_w(labels[1]) / 2, y2, PW, thin, **kw_[1])
    p3 = Pill(labels[2], 2 + pill_w(labels[2]) / 2, y2, PW, thin, **kw_[2])
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
        tg = bool(lid) and lid in targets
        m, _ = conn(pts, g, l["polarity"], l["delay"], hollow=hollow, target=tg)
        out.append(wr(m, tg))
        if lid:
            extra = ("weakest step",) if weakest == i else ()
            out.append(verb_at(pts, l["polarity"], step_words(i + 1 if numbered else 0, lid, extra), side, big=tg))
    out.append(p1.svg() + p2.svg() + p3.svg())
    if inside:
        out.append(loop_id(W / 2, max(p2.bot, p3.bot) + 28, *inside))
    n2 = len(step_words(2, lids[1], ("weakest step",) if weakest == 1 else ())) if lids[1] else 1
    h = bot_y + 34 + (n2 - 1) * LH
    return "".join(out), h


GAP4 = 112                # the rise between a four-variable loop's two rows: the tick, the tag and the arrowhead
INNER = 8                 # a side step's line stands 8 px in from where the pill's rounded end meets its flat edge


def four_loop(codes, lids, numbered=True, inside=None, inside_rows=None, targets=(), shared=(), labels=None):
    """A loop of four variables on a square, clockwise from the top left: step 1 arches over the top and step 3 under
    the bottom, as two_loop draws a two-variable loop; steps 2 and 4 run straight down the right and up the left, each on
    its pills' flat edges near their inner ends, with its words outside the loop, so the loop's ID sits clear between
    them. inside is (loop ID, kind); inside_rows sets words of a failure plate's own on two rows; targets and shared as
    two_loop takes them; labels overrides the short names (a failure plate's own words). Returns (body, h)."""
    labels = labels or [short(c) for c in codes]
    pw = [pill_w(lb) for lb in labels]
    rows = [len(step_words(1, x)) if x else 1 for x in lids]
    run_y = 30 + (rows[0] - 1) * LH + (3 if lids[0] in targets else 0)
    hs = [max(len(wrap(lb, p - 2 * PAD)) * LH + 22, 44) for lb, p in zip(labels, pw)]
    h1, h2 = max(hs[0], hs[1]), max(hs[2], hs[3])
    cy1 = run_y + RISE + h1 / 2
    cy2 = cy1 + h1 / 2 + GAP4 + h2 / 2
    kw_ = [dict(red=c_ in targets, shared=c_ in shared) for c_ in codes]
    a = Pill(labels[0], 2 + pw[0] / 2, cy1, pw[0], **kw_[0])
    b = Pill(labels[1], W - 2 - pw[1] / 2, cy1, pw[1], **kw_[1])
    c = Pill(labels[2], W - 2 - pw[2] / 2, cy2, pw[2], **kw_[2])
    d = Pill(labels[3], 2 + pw[3] / 2, cy2, pw[3], **kw_[3])
    xr = max(b.left + b.h / 2, c.left + c.h / 2) + INNER
    xl = min(a.right - a.h / 2, d.right - d.h / 2) - INNER
    need(xr <= min(b.right - b.h / 2, c.right - c.h / 2) and xl >= max(a.left + a.h / 2, d.left + d.h / 2),
         "a four-variable loop's side step misses its pills' flat edges")
    bot_y = max(c.bot, d.bot) + RISE
    paths = [([(a.cx, a.top - 2), (a.cx, run_y), (b.cx, run_y), (b.cx, b.top - 2)], "above"),
             ([(xr, b.bot + 2), (xr, c.top - 2)], "right"),
             ([(c.cx, c.bot + 2), (c.cx, bot_y), (d.cx, bot_y), (d.cx, d.bot + 2)], "below"),
             ([(xl, d.top - 2), (xl, a.bot + 2)], "left")]
    out = []
    for i, ((pts, side), lid) in enumerate(zip(paths, lids)):
        l = link(lid)
        tg = lid in targets
        m, _ = conn(pts, l["evidence"], l["polarity"], l["delay"], target=tg)
        out.append(wr(m, tg))
        words = step_words(i + 1 if numbered else 0, lid)
        out.append(verb_at(pts, l["polarity"], words, side, big=tg))
        if side in ("left", "right"):
            x, _, _, _ = anchor_at(pts, l["polarity"])
            span = max(tw(w_, 600 if re.match(r"\d+ ", w_) else 400) for w_ in words) + (3 if tg else 0)
            need((x - 15 - span >= 2) if side == "left" else (x + 15 + span <= W - 2),
                 f"step {i + 1}'s words of a four-variable loop leave the {W} px artboard")
    out.append(a.svg() + b.svg() + c.svg() + d.svg())
    mid_x, mid_y = (xl + xr) / 2, (max(a.bot, b.bot) + min(c.top, d.top)) / 2
    room = xr - xl - 2 * 12
    if inside:
        lid_, kind = inside
        need(max(tw(f"Loop {lid_}", 700), tw(kind)) <= room, "the loop's ID crowds its side steps")
        out.append(loop_id(mid_x, mid_y - 3, lid_, kind, two=True))
    if inside_rows:
        need(max(tw(r_, 700) for r_ in inside_rows) <= room, "the words inside the loop crowd its side steps")
        out.append(f'<text class="id" x="{F(mid_x)}" y="{F(mid_y - 9)}" text-anchor="middle">{e(inside_rows[0])}'
                   f'<tspan x="{F(mid_x)}" dy="{LH}">{e(inside_rows[1])}</tspan></text>')
    h = bot_y + 34 + (rows[2] - 1) * LH
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
# Styles (D3-480, the review fix pass). The plates share one block, printed once at the head of the chapter as its
# "plate_css" (the shell wraps it in @scope (#systems-graphics [data-specimen]), so :scope is each stage); no plate
# carries a style of its own. Every size comes from a type token or a chart type token, every color from a theme
# token. The plate composes by its frame's width with @container oa-frame and never by a media query: under 680 px one
# 328 px column, the drawing over its words; at 680 px or wider (the frame's content box, which the shell also reads
# to widen the stage) a 680 px stage with the drawing at left and its words beside it, or two drawings side by side;
# under 328 px the prose follows the frame's visible width, so only the 296 px drawing reaches past it (AX S5).
# ---------------------------------------------------------------------------------------------------------------
CSS = {k: C13.CSS[k] for k in ("dnp", "evr", "ev", "gr", "chip", "k", "rs", "gw", "nw2", "src", "nt", "hed", "sub", "mk")}
STAGE = W + 2 * 16          # 328 px: the opener's limit on a 360 px screen, and every plate's narrow true width
WIDE = 680                  # the wide true width, where the frame's content box holds it (D3-480; the shell's switch)
GAP_A, GAP_PR, GAP_TRI = 32, 40, 16       # the column gaps of the wide compositions, inside 24 px gutters
TRI = (WIDE - 48 - 2 * GAP_TRI) // 3      # 200 px: a column of a three-across plate
INK = "var(--oa-color-graphic-essential)"
BASE = (":scope{color:var(--oa-color-text-primary)}.p{box-sizing:border-box;padding:16px;font:var(--oa-type-body);max-width:100%}"
        ".p *{box-sizing:border-box}:where(.p) :where(p){margin:0}")
LAYOUT = (".fx{display:grid;grid-template-columns:minmax(0,1fr);gap:12px}.fx.pr{gap:24px}.fx.tri{gap:0}.fx>div{min-width:0}"
          ".fx>div>:first-child{margin-top:0}.fx>div>*+.k{margin-top:16px}"
          "@container oa-frame (min-width:680px){.p.wd{padding:24px}"
          f".wd .fx{{grid-template-columns:{W}px minmax(0,1fr);column-gap:{GAP_A}px}}"
          f".wd .fx.pr{{grid-template-columns:{W}px {W}px;column-gap:{GAP_PR}px}}"
          f".wd .fx.tri{{grid-template-columns:repeat(3,minmax(0,1fr));column-gap:{GAP_TRI}px}}"
          ".wd .tri>.vc{margin:0;padding:0;border:0}"
          f".wd .two{{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:{GAP_PR}px}}}}"
          "@container oa-frame (max-width:327.98px){.p :is(p,ul,ol,.evr):not(.dnp){max-width:calc(100cqi - 32px)}}")
CSS.update({
    "sv": (".sv{display:block;overflow:visible}"
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
    "pk": (".sv .pk{stroke:var(--oa-color-palette-prussian)}.sv .gk{stroke:var(--oa-color-palette-verdigris)}"
           ".sv .sk{stroke:var(--oa-color-palette-stone)}.sv .pkf{fill:var(--oa-color-palette-prussian)}"
           ".sv .gkf{fill:var(--oa-color-palette-verdigris)}.sv .skf{fill:var(--oa-color-palette-stone)}"),
    "kb": ".kb{margin-top:16px}",
    "hg": ".hg li{display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:6px;align-items:baseline}.hg .mk{margin:0}",
    "sw": (".sw{display:inline-block;width:14px;height:14px;vertical-align:-2px;margin-right:6px}"
           ".sw.gkf{background:var(--oa-color-palette-verdigris)}.sw.pkf{background:var(--oa-color-palette-prussian)}"
           ".sw.skf{background:var(--oa-color-palette-stone)}"),
    # round 2. Rule 12.5's red target, as chapter 13's plates and the atlas build draw it: a 4 px red line on a 6 px ink
    # case with the 6 px tag, ticks and arrowhead; a target variable's outline in red at 3 px
    "rt": (".sv .hi{display:none}.sv .rt .lo{display:none}.sv .rt .hi{display:inline}"
           ".sv .rt .ak-mark{stroke:var(--oa-color-data-emphasis-red);stroke-width:4px}"
           f".sv .rt .ak-case{{fill:none;stroke:{INK};stroke-width:6px}}.sv .rt .hd{{fill:var(--oa-color-data-emphasis-red)}}"),
    "rp": ".sv .pl.rp{stroke:var(--oa-color-data-emphasis-red);stroke-width:3px}",
    # Rule 15.15's shared variable: the pill filled in ink and its name in the surface color
    "sh": f".sv .pl.sh{{fill:{INK}}}.sv .ts{{fill:var(--oa-color-surface)}}",
    "pp": C13.CSS["pp"],
    # a list of rows under a small head: a reform's effects by family and its routes (Rules 15.16, 13.5, 13.10)
    "ef": (".ef{list-style:none;margin:0;padding:0;font:var(--oa-type-body-small)}"
           ".ef>li{padding:8px 0;border-top:1px solid var(--oa-color-border-hairline)}.ef>li:last-child{border-bottom:1px solid var(--oa-color-border-hairline)}"
           ".ef .fv{display:flex;flex-wrap:wrap;align-items:center;gap:4px 12px;margin-top:4px}"
           ".ef .fv b{font-weight:var(--oa-font-weight-bold);font-variant-numeric:tabular-nums}"
           ".ef .rd{display:flex;flex-wrap:wrap;gap:2px 16px;margin-top:2px}"),
    "gp": (".gp+.gp{margin-top:16px;padding-top:14px;border-top:1px solid var(--oa-color-border-hairline)}"
           ".gp .evr{margin-bottom:6px}"),
    "two": ".two{display:grid;grid-template-columns:minmax(0,1fr);gap:20px;margin-top:20px}",
})


CSS["nt"] = CSS["nt"] + ".nt+.nt{margin-top:4px}"


def plate_css(files):
    """The chapter's one block: the base, every rule some plate's markup uses, then the compositions, last, so the
    container rules win over the rules they reset."""
    used = set()
    for body in files.values():
        for cls in re.findall(r'class="([^"]+)"', body):
            used.update(cls.split())
    return BASE + "".join(css for k, css in CSS.items() if k in used) + LAYOUT


# ---------------------------------------------------------------------------------------------------------------
# The book of plates
# ---------------------------------------------------------------------------------------------------------------
class Book:
    def __init__(self):
        self.files, self.manifest, self.examples = {}, {}, []

    def add(self, sid, body, *, rule, alt, illustrative=False, readable=False, notes="", wide=False):
        """A plate at true size, never scaled (fix pass 2, D3-480). Every plate is a 328 px stage, the 296 px drawing with
        a 16 px gutter each side, whose frame is the query container oa-frame. A plate with words to set beside its
        drawing, or two or three drawings to set side by side, is wide: where its frame's content box holds 680 px, the
        shell widens its stage to 680 px and the plate composes for that width. Styles come from the chapter's block."""
        need(sid not in self.files, f"duplicate specimen {sid}")
        body = re.sub(r">\s+<", "><", body.strip())
        self.files[sid] = (f"<!-- {sid}: Oath & Action guide, Edition 06, chapter 15. Systems designer, {WRITTEN}. Written by "
                           f"work/build/scripts/phase-3/phase3_ch15_build.py. -->\n"
                           f'<div class="p{" wd" if wide else ""}">{body}</div>\n')
        m = {"chapter": "15", "rule": rule, "width_px": STAGE, "fit_switch": False, "frame_container": True,
             "alt": " ".join(alt.replace("'", "’").split()), "illustrative": bool(illustrative), "notes": notes}
        if wide:
            m["wide_px"] = WIDE
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


def ra_p(t):
    """The read-aloud sentence as the first of the words beside a drawing."""
    return f'<p class="ra">{e(t)}</p>'


def beside(left, right):
    """A drawing and its words: one column under 680 px, the drawing at left and its words at right from 680 px."""
    return f'<div class="fx"><div>{left}</div><div>{right}</div></div>'


def least_certain(ids):
    return C13.least_certain(ids)


# ===============================================================================================================
# The opener: one loop, one authority line and one boundary, each part numbered to the rule that sets it
# ===============================================================================================================
LETTERS = "ABCDEF"           # the opener's callouts take letters, since its loop's steps take numbers (CD CH15-S1, BC S1)


def numeral(n, x, y):
    return f'<g class="nm"><circle cx="{F(x)}" cy="{F(y)}" r="11"/>{text(x, y + 5, LETTERS[n - 1], "")}</g>'


def opener(book):
    """Loop R13 with authority connection LE02, which leaves the loop's first variable for the economy layer (SD-6: the
    data lead's choice; Rule 15.6 then drew Loop R18, and draws Loop R10 since the review fix pass)."""
    lid = "R13"
    lp = LOOP[lid]
    need(lp["links"] == ["L11", "L12"] and lp["type"] == "R" and minus_count(lp["links"]) == 2, "Loop R13 changed")
    need([link(x)["evidence"] for x in lp["links"]] == ["well-supported", "plausible"], "Loop R13's grades changed")
    codes = [c for c, _ in lp["chain"]]
    need(codes == ["D1", "D2"], "Loop R13's variables changed")
    le = link("LE02")
    need((le["type"], le["from"], le["to"], le["polarity"], le["evidence"], le["loops"]) == ("authority", "D1", "EC2", None, "documented", []),
         "connection LE02 changed")
    need(node("EC2")["layer"] == "economy" and node("D1")["layer"] == "core", "the layers of D1 or EC2 changed")
    body, h, (a, b) = two_loop(codes, lp["links"], inside=(lid, "reinforcing"), a_in=22, top=4)
    # the economy layer under the core: a 1 px rule with each layer's name, broken where the authority line crosses it
    xa = a.left + 38
    run2 = a.bot + RISE
    fy = run2 + 52
    ec = Pill(short("EC2"), 0, 0, 196)
    ec.cx, ec.cy = 2 + ec.pw / 2, fy + 22 + ec.h / 2
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
    lst = "".join(f"<li>{C13.mk(LETTERS[n - 1])} {e(w)}, Rule {r}</li>" for n, (w, r) in enumerate(parts, 1))
    steps = "".join(f'<p class="nt">{gl(x)}</p>' for x in (*lp["links"], "LE02"))
    body = (label_for(lp["links"], "the grade of the loop’s least certain step")
            + beside(hed("Loop", lid, lp["title"]) + fig(svg),
                     f'{steps}<p class="k">What each lettered part says</p><ol class="kw hg">{lst}</ol>'
                     + src("loop R13 and connections L11, L12 and LE02")))
    book.add("s-15-opener", body, rule=None, readable=True, wide=True,
             alt=(f"Loop R13 from our systems atlas, “{lp['title']}”, drawn as two pills, Congressional capacity and Executive "
                  "unilateralism, with an arrow over the top marked minus, lowers, and one under the bottom marked minus, lowers, "
                  "drawn dashed. The loop’s name and the word reinforcing sit inside it. A line with an open diamond and the word "
                  "decides runs from Congressional capacity down across a rule into the economy layer, to Public investment in "
                  "research and infrastructure. Six letters, A to F, tie the parts to a list: a variable, Rule 15.2; a sign tag "
                  "and its word, Rule 15.3; the loop’s number and kind, Rule 15.6; authority with no sign, Rule 15.5; a boundary "
                  "between layers, Rule 15.9; a dashed line for a plausible step, Rule 13.4."),
             notes="Chapter 15's opener: one loop, one authority line and the core and economy layers, from the atlas's records "
                   "read by script; lines by the atlas build's wire_marks with the 28 px lead-in. Its callouts are letters, "
                   "since the loop's steps carry numbers.")
    book.log("opener", "Loop R13 and connection LE02, Congress and public investment", "D04")
    return {"specimen": "s-15-opener",
            "caption": "Loop R13 from our systems atlas, with the authority line that leaves it and the layer it reaches. "
                       "Each letter marks one part of the grammar, and the list names the rule that sets it."}


# ---------------------------------------------------------------------------------------------------------------
# More of the kit: one connection as a card, a boundary rule, a frame, a loop of drawn steps
# ---------------------------------------------------------------------------------------------------------------
CARD_PW = 170
CARD_RUN = 116


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
    pw = max(pill_w(la, pw), pill_w(lb, pw))
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


def card_width(a_code, b_code, lid, words=None, pw=CARD_PW):
    """The width a card's drawing takes, for an artboard sized to it: the wider pill, or the line's words to its right,
    with the sign tag between (card() sets the words 15 px right of the line)."""
    la, lb = short(a_code), short(b_code)
    pw = max(pill_w(la, pw), pill_w(lb, pw))
    words = words or step_words(0, lid)
    return math.ceil(max(2 + pw, 2 + pw / 2 + 15 + max(tw(w_) for w_ in words)) + 2)


def drawn_loop(n, stations, steps, numbered=True, weakest=None, inside=None, thin=False):
    """A loop drawn from explicit steps, for a mechanism with no numbered connections (a conceptual loop) or a loop drawn
    against the record in a failure plate. stations are labels; steps are dicts of sign, grade, delay, hollow. Two
    stations sit side by side as two_loop sets them (round 2, Loop B2); three as three_loop sets them."""
    if n == 2:
        hs = [max(len(wrap(lb, pill_w(lb) - 2 * PAD)) * LH + 22, 44) for lb in stations]
        run_y = 30
        cy = run_y + RISE + max(hs) / 2
        a = Pill(stations[0], 2 + pill_w(stations[0]) / 2, cy, PW, thin)
        b = Pill(stations[1], W - 2 - pill_w(stations[1]) / 2, cy, PW, thin)
        bot_y = max(a.bot, b.bot) + RISE
        paths = [([(a.cx, a.top - 2), (a.cx, run_y), (b.cx, run_y), (b.cx, b.top - 2)], "above"),
                 ([(b.cx, b.bot + 2), (b.cx, bot_y), (a.cx, bot_y), (a.cx, a.bot + 2)], "below")]
        pills = [a, b]
        need(a.right + 12 <= b.left, "a two-station loop's stations touch")
        mid = (W / 2, run_y + 28)
        out = []
        for i, ((pts, side), st) in enumerate(zip(paths, steps)):
            m, _ = conn(pts, st.get("grade"), st["sign"], st.get("delay"), hollow=st.get("hollow", False))
            out.append(f'<g class="wr">{m}</g>')
            word = BS.verb(st["sign"])
            out.append(verb_at(pts, st["sign"], [f"{i + 1} {word}" if numbered else word], side))
        out.append(a.svg() + b.svg())
        if inside:
            out.append(loop_id(*mid, *inside, two=True))
        return "".join(out), bot_y + 34
    if n == 3:
        hs = [max(len(wrap(lb, pill_w(lb) - 2 * PAD)) * LH + 22, 44) for lb in stations]
        y1 = 4 + hs[0] / 2
        y2 = y1 + hs[0] / 2 + 108 + max(hs[1], hs[2]) / 2
        p1 = Pill(stations[0], W / 2, y1, PW, thin)
        p2 = Pill(stations[1], W - 2 - pill_w(stations[1]) / 2, y2, PW, thin)
        p3 = Pill(stations[2], 2 + pill_w(stations[2]) / 2, y2, PW, thin)
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
            + beside(hed("Loop", "B1a", lp["title"]) + fig(svg),
                     ra_p(read_aloud(["E1", "D4"], lp["links"])) + f'<p class="k">What the drawing holds</p>{words}'
                     + src("loop B1a and connections L17 and L16")))
    book.add("s-15-1-correct", body, rule="15.1", readable=True, wide=True,
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
        "title": "Draw mechanisms at one weight, and let width or size measure only with a key.",
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
        need(node(c)["type"] == k and kind_word(c), f"variable {c} is no longer a {k}, or its kind and type disagree")
    split = sorted(c for c in NODE if kind_word(c) is None)
    need(split == ["D6"], f"the variables whose type and plain kind disagree changed: {split}")
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
    need(174 <= TRI, "a variable's card is wider than a column of three")
    body = f'<div class="fx tri">{"".join(cards)}</div>' + src("variables B3, B1 and C3")
    book.add("s-15-2-correct", body, rule="15.2", readable=True, wide=True,
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
            f"Of its {len(NODE)} variables, {kinds['stock']} are stocks, amounts built up over time, and "
            f"{words_n(kinds['flow'])} are flows, amounts per period. {words_n(kinds['auxiliary']).capitalize()} are conditions "
            f"the atlas calls auxiliary, worked out from other variables. The other {words_n(kinds['driver'])} are outside "
            "drivers, forces whose causes lie outside the model, and Rule 15.9 sets where they go.",
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
            {"label": "Kind", "value": "Stock, flow, condition or outside driver, in words, from the variable’s type and its plain description; "
                                       "where the two disagree, as for Variable D6, no kind, since the atlas lists the question for its next version"},
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
        cols.append(f'<div>{fig(svg_wrap(b, h))}<p class="hed">{gl(lid)}</p><p class="nt">{e(l["sign_meaning"])}</p></div>')
    key = kw([f"<b>+ raises</b>: the two move the same way.", f"<b>{MINUS} lowers</b>: they move in opposite directions.",
              "“A positive sign does not mean a benefit.”"])
    body = (label_for(["L46", "L16"]) + f'<div class="fx pr">{"".join(cols)}</div><div class="kb"><p class="k">Key</p>{key}</div>'
            + src("connections L46 and L16, and the glossary entry for a positive sign"))
    book.add("s-15-3-correct", body, rule="15.3", readable=True, wide=True,
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
    fail = dnp() + f'<div class="fx pr">{"".join(fcols)}</div><div class="kb"><p class="k">Key</p>{fkey}</div>'
    book.add("s-15-3-failure", fail, rule="15.3", wide=True,
             alt=(FC + "The same two connections over a key that reads plus, positive effect, and minus, negative effect."),
             notes="Labeled failure: the key reads a sign as good or bad news.")
    return {
        "id": "15.3",
        "title": "Read a plus or minus as the way two variables move together.",
        "rule": [
            "Each causal connection joins two variables, the quantities or conditions that can rise or fall, and carries a "
            "sign tag. A plus means the two tend to move the same way, and a minus means they move in opposite directions, "
            "with the model’s other conditions held steady. The word beside the tag says it again: raises for a plus, lowers "
            "for a minus.",
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
        cw = card_width(l["from"], l["to"], lid)
        need(cw <= TRI, f"connection {lid}'s card needs {cw} px, over a column of three ({TRI} px)")
        cols.append(f'<div class="vc">{fig(svg_wrap(b, h, w=cw))}<p class="nt">{say_link(lid)}</p></div>')
    body = (label_for([x for x, _ in picks]) + f'<div class="fx tri">{"".join(cols)}</div>'
            + src("connections L28, L26 and T12"))
    book.add("s-15-4-correct", body, rule="15.4", readable=True, wide=True,
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
        cw = card_width(l["from"], l["to"], lid, words=[BS.verb(l["polarity"])])
        fcols.append(f'<div class="vc">{fig(svg_wrap(b, h, w=cw))}</div>')
    legend = kw([f'<span class="sw gkf"></span> Money', f'<span class="sw pkf"></span> Information', f'<span class="sw skf"></span> Ownership'])
    fail = dnp() + f'<div class="fx tri">{"".join(fcols)}</div><div class="kb"><p class="k">Key</p>{legend}</div>'
    book.add("s-15-4-failure", fail, rule="15.4", wide=True,
             alt=(FC + "The same three connections with no type words, their lines in three colors, green for money, blue for "
                  "information and gray for ownership, keyed by colored squares."),
             notes="Labeled failure: color alone for a connection's type, which gray print and low color vision lose.")
    return {
        "id": "15.4",
        "title": "Say in words when a connection carries money, information or ownership.",
        "rule": [
            "Our systems atlas gives each connection a type. Most are causal: a change in one variable changes another. "
            f"Others name what moves along the line: money on {types['money']} of them, such as contributions or advertising "
            f"revenue; information on {words_n(types['information'])}, such as news coverage or a feed; and ownership on "
            f"{words_n(types['ownership'])}, where one quantity is held inside another. Print the type in words before the verb, "
            "as in “money, lowers”, and in the key.",
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
                    "caption": "<strong>Fails Rule 15.4.</strong> Color alone tells the three types apart. In gray print the "
                               "money and ownership lines match, and the key cannot say which is which."},
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
    gls = GLOSS["Authority connection"]
    q = "It says who decides, without saying which way the decision goes, so it has no sign and never closes a loop."
    need(q in gls, "the atlas's definition of an authority connection changed")
    l13, l14 = link("LT13"), link("LT14")
    need((l13["from"], l13["to"], l14["from"], l14["to"]) == ("D4", "TC7", "D6", "TC7"), "connection LT13 or LT14 changed")
    need(node("TC7")["layer"] == "technology" and node("D4")["layer"] == node("D6")["layer"] == "core", "the layers changed")
    # two bodies, one decision: two authority lines into one variable across the core and technology boundary
    a = Pill(short("D4"), 0, 0, 140)
    b = Pill(short("D6"), 0, 0, 140)
    a.cx, b.cx = 2 + a.pw / 2, W - 2 - b.pw / 2
    top = max(a.h, b.h)
    a.cy = b.cy = top / 2 + 2
    t = Pill(short("TC7"), W / 2, 0, 172)
    t.cy = top + 4 + 128 + t.h / 2
    lo = [max(a.left, t.left) + 29, min(a.right, t.right) - 29]
    hi = [max(b.left, t.left) + 29, min(b.right, t.right) - 29]
    need(lo[0] <= lo[1] and hi[0] <= hi[1], "the authority lines cannot meet both pills on their flat edges")
    xs = [(lo[0] + lo[1]) / 2, hi[0] + 6]
    out = []
    for x, src_p, lid in ((xs[0], a, "LT13"), (xs[1], b, "LT14")):
        m, _ = conn([(x, src_p.bot + 2), (x, t.top - 2)], "documented", None, link(lid)["delay"], authority=True)
        out.append(f'<g class="wr">{m}</g>')
    out.append(text(xs[0] - 12, a.bot + 46, "decides", "v", "end") + text(xs[1] + 12, b.bot + 46, "decides", "v", "start"))
    out.append(boundary(t.top - 48, xs, "Core layer", None) + lines(W, t.top - 26, ["Technology", "layer"], "fl", "end"))
    need(W - tw("Technology") - 8 > xs[1], "the layer's name would touch the authority line")
    out.append(a.svg() + b.svg() + t.svg())
    svg = svg_wrap("".join(out), t.bot + 4)
    words = kw([say_link("LT13"), say_link("LT14"), f"“{e(l13['sign_meaning'])}”"])
    body = (label_for(["LT13", "LT14"])
            + beside(fig(svg), f'<p class="k">Two bodies, one decision</p>{words}' + src("connections LT13 and LT14")))
    book.add("s-15-5-correct", body, rule="15.5", readable=True, wide=True,
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
            f"Keep it out of every loop drawing, even where it touches a variable the loop holds. All {words_n(len(auth))} of the "
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
    # Loop R10 sits outside executive power and reads the same from either side, and its signs run plus, minus, minus,
    # plus, so a reader counts two minus signs among plus signs to find its kind (the data lead's ruling on BC S2)
    picks = [("R10", "reinforcing", 2, 4), ("B5", "balancing", 1, 2)]
    r10 = LOOP["R10"]
    need([c for c, _ in r10["chain"]] == ["C1", "C2", "C3", "C4"] and r10["links"] == ["L08", "L25", "L53", "L42"]
         and [link(x)["polarity"] for x in r10["links"]] == ["+", "-", "-", "+"] and r10["closure"].startswith("closed"),
         "Loop R10 changed")
    need(all(node(c)["layer"] == "core" for c, _ in r10["chain"]), "Loop R10 left the core layer")
    cols = []
    for lid, kind, n, k in picks:
        lp = LOOP[lid]
        need(minus_count(lp["links"]) == n and len(lp["links"]) == k and lp["type"] == kind[0].upper(), f"Loop {lid} changed")
        codes = [c for c, _ in lp["chain"]]
        if k == 4:
            b, h = four_loop(codes, lp["links"], inside=(lid, kind))
        else:
            b, h, _ = two_loop(codes, lp["links"], inside=(lid, kind))
        steps = "".join(f'<p class="nt"><b>{i}</b>&#160;{gl(x)}</p>' for i, x in enumerate(lp["links"], 1))
        cols.append(f'<div>{label_for(lp["links"], "the grade of the loop’s least certain step")}{hed("Loop", lid, lp["title"])}'
                    f'{fig(svg_wrap(b, h), read_aloud(codes, lp["links"]))}{steps}'
                    f'<p class="nt"><b>{words_n(n).capitalize()} minus sign{"s" if n != 1 else ""}</b>: {kind}.</p></div>')
    body = f'<div class="fx pr">{"".join(cols)}</div>' + src("loops R10 and B5 and their connections")
    book.add("s-15-6-correct", body, rule="15.6", readable=True, wide=True,
             alt=("Two loops from our systems atlas, each with its steps numbered in order, its number and kind inside it, a "
                  "sentence that reads it aloud and its count of minus signs. Loop R10 draws four variables on a square, its "
                  "steps marked plus, minus, minus and plus; Loop B5 draws two. "
                  + " ".join(f"Loop {lid}, “{LOOP[lid]['title']}”: {read_aloud([c for c, _ in LOOP[lid]['chain']], LOOP[lid]['links'])} "
                             f"{words_n(n).capitalize()} minus sign{'s' if n != 1 else ''}, {kind}." for lid, kind, n, _ in picks)),
             notes="Kinds checked against the count of minus signs on every numbered loop; read-aloud lines carry the signs "
                   "around. Loop R10 replaces Loop R18, so the chapter's first plates draw executive power once, in the opener.")
    book.log("15.6 correct", "Loop R10, safe seats", "D02")
    book.log("15.6 correct", "Loop B5, state experiments", "D03")
    codes = [c for c, _ in r10["chain"]]
    b, h = four_loop(codes, r10["links"], numbered=False, inside_rows=("A vicious", "cycle"))
    fail = dnp() + fig(svg_wrap(b, h))
    book.add("s-15-6-failure", fail, rule="15.6",
             alt=(FC + "Loop R10 drawn without its step numbers, chip and kind, and the words “A vicious cycle” inside it."),
             notes="Labeled failure: a judgment for a kind, and no numbers to read the loop in order.")
    return {
        "id": "15.6",
        "title": "Number a loop’s steps in order, and name it reinforcing or balancing.",
        "rule": [
            "A loop is “a chain of causes that returns to its starting variable”, in our systems atlas’s words. Number its steps "
            "from the variable the atlas starts it at, in the atlas’s order. Give the loop its typed chip and name beside the "
            "drawing, and set its ID and its kind inside it: "
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
                    "caption": "<strong>Fails Rule 15.6.</strong> Loop R10 lacks its step numbers, chip and kind, and the "
                               "words inside it judge the loop. Its two minus signs make it reinforcing."},
        "specs": [
            {"label": "Step number", "value": "Bold, before the verb, from the atlas’s first connection: 1 raises"},
            {"label": "Inside the loop", "value": "The loop’s typed ID in bold, such as Loop R10, then reinforcing or balancing"},
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
    body = f'<div class="fx pr"><div>{col1}</div><div>{col2}</div></div>' + src("loops R16 and B3")
    book.add("s-15-7-correct", body, rule="15.7", readable=True, wide=True,
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
            f"Of the atlas’s {len(LOOP)} loops, {closed} close through numbered connections, {words_n(len(hyp))} close "
            f"through a hypothesis and {words_n(len(con))} are conceptual.",
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
            {"label": "Counts", "value": f"{closed} closed, {words_n(len(hyp))} through a hypothesis, {words_n(len(con))} conceptual, as of the snapshot"},
        ],
        "related": ["10", "13"],
        "builders": ["Read the closure from the loop’s record, and draw a conceptual loop’s steps from its own list of stations "
                     "and signs, since it lists no connections."],
    }


def chain_plate(summary_sign, summary_lid=None):
    """The open chain E1 to EC6 to A4, down the left, through the economy layer's frame, with a summary arrow on the
    right from its first variable to its last: the core map's own connection L37, or (in the failure) one drawn with the
    last step's sign."""
    pw, x = 170, 44
    e1 = Pill(short("E1"), 2 + pw / 2, 0, pw)
    e1.cy = e1.h / 2 + 2
    fy = e1.bot + 60
    ec = Pill(short("EC6"), 2 + pw / 2, 0, pw)
    ec.cy = fy + 34 + ec.h / 2
    fb = ec.bot + 12
    a4 = Pill(short("A4"), 2 + pw / 2, 0, pw)
    a4.cy = fb + 62 + a4.h / 2
    out = [frame(0, fy, pw + 16, fb - fy, "Economy layer", gaps_top=[x], gaps_bot=[x])]
    for (p, q), lid in (((e1, ec), "LE12"), ((ec, a4), "LE14")):
        pts = [(x, p.bot + 2), (x, q.top - 2)]
        m, _ = conn(pts, link(lid)["evidence"], link(lid)["polarity"], link(lid)["delay"])
        out.append(f'<g class="wr">{m}</g>' + verb_at(pts, link(lid)["polarity"], step_words(0, lid), "right"))
    xr = 262
    pts = [(e1.right + 2, e1.cy), (xr, e1.cy), (xr, a4.cy), (a4.right + 2, a4.cy)]
    if summary_lid:
        l = link(summary_lid)
        m, _ = conn(pts, l["evidence"], l["polarity"], l["delay"])
        words = step_words(0, summary_lid)
    else:
        m, _ = conn(pts, "well-supported", summary_sign, None)
        words = [BS.verb(summary_sign)]
    out.append(f'<g class="wr">{m}</g>' + verb_at(pts, summary_sign, words, "left"))
    out.append(e1.svg() + ec.svg() + a4.svg() + text(W, 14, "Core layer", "fl", "end"))
    return svg_wrap("".join(out), a4.bot + 4)


def rule_15_8(book):
    conv = V7["methods"]["model_conventions"]
    q = ("Where the core map draws one arrow for a longer chain, the economy and technology layers show the steps, and their "
         "combined sign agrees with the core arrow.")
    need(q in conv, "the atlas's convention on chains changed")
    le12, le14, l37 = link("LE12"), link("LE14"), link("L37")
    need((le12["from"], le12["to"], le12["polarity"], le14["from"], le14["to"], le14["polarity"]) == ("E1", "EC6", "-", "EC6", "A4", "+"),
         "the chain E1 to EC6 to A4 changed")
    need((l37["from"], l37["to"], l37["polarity"]) == ("E1", "A4", "-"), "connection L37 changed")
    n = minus_count(["LE12", "LE14"])
    need(("-" if n % 2 else "+") == l37["polarity"], "the chain's combined sign no longer agrees with connection L37")
    need(node("EC6")["layer"] == "economy" and node("E1")["layer"] == node("A4")["layer"] == "core", "the chain's layers changed")
    svg = chain_plate("-", "L37")
    ra = read_aloud(["E1", "EC6", "A4"], ["LE12", "LE14"], closes=False)
    words = kw([f"{gl('LE12')} and {gl('LE14')}: the chain carries {words_n(n)} minus sign, so the end moves opposite to the start.",
                f"{gl('L37')}: the core map’s one arrow for the same path carries a minus.",
                f"The atlas: “{e(q)}”"])
    body = (label_for(["LE12", "LE14", "L37"])
            + beside(fig(svg), ra_p(ra) + f'<p class="k">Carry the sign along</p>{words}'
                     + src("connections LE12, LE14 and L37, and the atlas’s model conventions")))
    book.add("s-15-8-correct", body, rule="15.8", readable=True, wide=True,
             alt=(f"An open chain from our systems atlas, drawn downward: Policy tilt to insiders, a minus tag and the words money, "
                  f"lowers, into Net support from taxes and public benefits, framed as the economy layer, then a plus tag and the "
                  f"words money, raises, into Household security. On the right, connection L37 runs from Policy tilt to insiders "
                  f"straight to Household security with a minus tag and the words money, lowers. The chain reads: {ra} Beside it, "
                  "notes say the chain carries one minus sign, so the end moves opposite to the start, and the core map’s arrow agrees."),
             notes="Signs carried along the chain by script and checked against connection L37 (the atlas's convention).")
    book.log("15.8 correct", "Connections LE12, LE14 and L37, taxes and benefits", "D08")
    fail = dnp() + fig(chain_plate("+"))
    book.add("s-15-8-failure", fail, rule="15.8",
             alt=(FC + "The same chain with a summary arrow on the right from Policy tilt to insiders to Household security "
                  "drawn with a plus tag and the word raises, the sign of the chain’s last step."),
             notes="Labeled failure: the chain's answer read from its last step.")
    return {
        "id": "15.8",
        "title": "Draw an open chain from start to end, and carry its sign along.",
        "rule": [
            "An open chain is a run of connections that does not return to its start, such as the steps a layer draws behind "
            "one arrow on the core map. Draw it in one direction, from its first variable to its last, and read it the way a loop "
            "is read: each minus sign turns the direction. An even count of minus signs means the end moves with the start, and "
            "an odd count means it moves the other way.",
            f"Our systems atlas holds its chains to this: “{q}” Where a page shows a chain and the core arrow it stands behind, "
            "draw the core arrow beside the chain.",
        ],
        "tokens": [TOKEN_LINE],
        "why": {"text": ["A reader who takes the last step’s sign as the chain’s answer will often get it backward. Here the "
                         "last step raises household security, and the chain as a whole lowers it, as the core arrow says."],
                "basis": "Our systems atlas’s model conventions"},
        "correct": {"specimen": "s-15-8-correct",
                    "caption": "An open chain from our systems atlas through its economy layer, read with its signs carried "
                               "along, beside connection L37, the core map’s one arrow for the same path."},
        "failure": {"specimen": "s-15-8-failure",
                    "caption": "<strong>Fails Rule 15.8.</strong> The summary arrow takes the last step’s plus, so the chain reads "
                               "as raising household security. One minus sign along the way turns it, as connection L37 says."},
        "specs": [
            {"label": "Direction", "value": "One way, first variable to last; an open chain never bends back into a loop"},
            {"label": "Combined sign", "value": "An even count of minus signs for the same direction, odd for the opposite"},
            {"label": "Core arrow", "value": "Beside the chain where the page shows both, with its own sign"},
            {"label": "Read aloud", "value": "More or less at each variable, carrying the signs, as Rule 15.6 reads a loop"},
        ],
        "related": ["13"],
        "builders": ["Work out the combined sign by script from each connection’s record, and stop the build if it disagrees "
                     "with the core arrow."],
    }


def layers_plate(failure=False):
    pw, x = 196, 60
    top = 40 if failure else 0
    x4 = Pill(short("X4"), 2 + pw / 2, 0, pw)
    x4.cy = top + x4.h / 2 + 2
    cy0 = x4.bot + 84
    b6 = Pill(short("B6"), 2 + pw / 2, 0, pw)
    b6.cy = cy0 + 34 + b6.h / 2
    cy1 = b6.bot + 12
    ty0 = cy1 + 92
    tc = Pill(short("TC1"), 2 + pw / 2, 0, pw)
    tc.cy = ty0 + 34 + tc.h / 2
    ty1 = tc.bot + 12
    out = []
    if failure:
        out.append(frame(0, 0, W, ty1 + 4, "The model"))
    else:
        cl = next(r["title"] for r in V7["layers"]["core"]["regions"] if "B6" in r["nodes"])
        out.append(frame(0, cy0, W, cy1 - cy0, f"Core layer, {cl}", gaps_top=[x], gaps_bot=[x]))
        out.append(frame(0, ty0, W, ty1 - ty0, "Technology layer", gaps_top=[x]))
        out.append(lines(W, x4.cy - 4, ["Outside", "driver"], "fl", "end"))
    for p, q, lid, up in ((x4, b6, "LX4", False), (tc, b6, "LT01", True)):
        pts = [(x, p.top - 2), (x, q.bot + 2)] if up else [(x, p.bot + 2), (x, q.top - 2)]
        l = link(lid)
        m, _ = conn(pts, l["evidence"], l["polarity"], l["delay"])
        out.append(f'<g class="wr">{m}</g>' + verb_at(pts, l["polarity"], step_words(0, lid), "right"))
    out.append(x4.svg() + b6.svg() + tc.svg())
    return svg_wrap("".join(out), ty1 + (6 if failure else 2))


def rule_15_9(book):
    lay = {k: sum(1 for n in NODE.values() if n["layer"] == k) for k in ("core", "economy", "technology")}
    need(lay == {"core": 31, "economy": 12, "technology": 8}, f"the layers changed: {lay}")
    regions = V7["layers"]["core"]["regions"]
    clusters = [r for r in regions if r["id"] != "X"]
    drivers = next(r for r in regions if r["id"] == "X")["nodes"]
    need(len(clusters) == 5 and drivers == ["X1", "X2", "X3", "X4", "X5"], "the core's clusters or drivers changed")
    gls = GLOSS["Outside driver"]
    q = "A force that affects the model but whose own causes lie outside its boundary"
    need(gls.startswith(q), "the atlas's outside driver entry changed")
    bnd = V7["methods"]["boundary"]
    need("Five outside drivers are treated as given over that period" in bnd and "between 2026 and 2036" in bnd, "the atlas's boundary changed")
    lx4, lt01 = link("LX4"), link("LT01")
    need((lx4["from"], lx4["to"], lt01["from"], lt01["to"]) == ("X4", "B6", "TC1", "B6"), "connection LX4 or LT01 changed")
    svg = layers_plate()
    words = kw([f"{chip('Variable', 'X4')} sits outside every frame: the atlas treats its five outside drivers as given from "
                "2026 to 2036.", f"{chip('Variable', 'B6')} sits in the core layer’s cluster B.",
                f"{chip('Variable', 'TC1')} sits in the technology layer.",
                f"Each frame breaks where a connection crosses it: {gl('LX4')}, {gl('LT01')}."])
    body = (label_for(["LX4", "LT01"])
            + beside(fig(svg), f'<p class="k">Inside and outside</p>{words}'
                     + src("variables X4, B6 and TC1, connections LX4 and LT01, the layers and the model’s boundary")))
    book.add("s-15-9-correct", body, rule="15.9", readable=True, wide=True,
             alt=("A drawing from our systems atlas in three bands. At the top, outside every frame, Foreign interference, marked "
                  "outside driver. A line marked information, raises crosses into a frame named Core layer, Political inputs, "
                  "holding Hostile-content exposure. Below it a frame named Technology layer holds How platforms rank feeds and "
                  "seek attention, and a line marked information, raises runs up from it across both frames into Hostile-content "
                  "exposure. Each frame breaks where a line crosses it."),
             notes="Frames 1 px in the strong border color, broken 7 px each side of a crossing; layers and clusters from the atlas's layers record.")
    book.log("15.9 correct", "Variables X4, B6 and TC1, hostile content", "D01")
    fail = dnp() + fig(layers_plate(failure=True))
    book.add("s-15-9-failure", fail, rule="15.9",
             alt=(FC + "The same three variables and two connections inside one frame named The model, with Foreign "
                  "interference drawn as one more variable and no layers."),
             notes="Labeled failure: an outside driver inside the model's frame, and the layers left out.")
    return {
        "id": "15.9",
        "title": "Frame the atlas’s layers and clusters, and set outside drivers beyond the frames.",
        "rule": [
            f"Our systems atlas sorts its {len(NODE)} variables into three layers: the core, “{V7['layers']['core']['title']}”, "
            f"with {lay['core']} variables, five of them outside drivers and the rest in {words_n(len(clusters))} clusters; the "
            f"economy layer, with {lay['economy']}; and the technology layer, with {words_n(lay['technology'])}. Where a drawing "
            "shows variables from more than one layer, name each layer and mark its edge with a 1 px rule: a frame around each, "
            "one rule between two layers that stack, with both names, or a box around a layer that sits inside a drawing of "
            "another. Name the cluster of a core variable where the drawing frames it.",
            f"An outside driver is “{q.lower()[0] + q[1:]}”, in the atlas’s words. Set it outside every frame, with its kind in "
            "words. Where a connection crosses a frame, break the frame around the line, so a reader sees where the effect comes in.",
        ],
        "tokens": ["oa.color.border.strong"],
        "why": {"text": ["The frames tell a reader what the model explains and what it takes as given. A driver drawn inside a "
                         "cluster reads as one more thing the model accounts for, and the atlas treats its five drivers as given "
                         "from 2026 to 2036."],
                "basis": "Our systems atlas’s layers, boundary and glossary"},
        "correct": {"specimen": "s-15-9-correct",
                    "caption": "Foreign interference outside every frame, Hostile-content exposure in the core layer’s cluster B, "
                               "and feed ranking in the technology layer, with each frame broken where a connection crosses it."},
        "failure": {"specimen": "s-15-9-failure",
                    "caption": "<strong>Fails Rule 15.9.</strong> Foreign interference sits inside the model’s frame as one more "
                               "variable, and feed ranking loses its layer, so a reader cannot tell what the model explains."},
        "specs": [
            {"label": "Frame", "value": "1 px in the strong border color, its name at top right inside, 15 px", "token": "oa.color.border.strong"},
            {"label": "Two layers", "value": "One 1 px rule between them with both names at its right end, or a box around the smaller"},
            {"label": "Crossing", "value": "The frame breaks 7 px each side of the line"},
            {"label": "Outside driver", "value": "Outside every frame, marked Outside driver; the atlas’s glossary draws it as a rounded pill"},
            {"label": "Layers", "value": f"Core {lay['core']}, economy {lay['economy']}, technology {lay['technology']}; core clusters A to E"},
        ],
        "related": ["12", "13"],
        "builders": ["Read each variable’s layer and cluster from the atlas’s layers record, and break a frame wherever a "
                     "connection’s line crosses it."],
    }


def rule_15_10(book):
    rej = V7["rejectedLinks"]
    need(len(rej) == 3 and all(r["status"] == "reviewed and not drawn" for r in rej), "the atlas's rejected connections changed")
    need(len(V7["omissions"]) == 9, "the atlas's omissions changed")
    r1 = next(r for r in rej if r["id"] == "LTR1")
    need(r1["from"].startswith("TC1:") and r1["to"].startswith("B4:"), "rejected connection LTR1 changed")
    reason = C13_sentences(r1["reason"])
    need(reason[0] == "Feed ranking changes what people see (LT01).", "LTR1's reason changed")
    quote = reason[1] + " " + reason[2]
    need(quote.startswith("In the largest experiments, changing the feed did not measurably change hostility")
         and reason[2].startswith("Smaller effects appear in a 2024 reranking test") and len(reason) == 4, "LTR1's reason changed")
    a1, a2 = "Any effect runs through exposure to hostile content", "and is small."
    need(reason[3].startswith(a1 + ", from B6: ") and reason[3].endswith("(connection L47), " + a2), "LTR1's last sentence changed")
    need(link("L47")["from"] == "B6" and link("L47")["to"] == "B4", "connection L47 changed")
    tail = (f'The atlas adds that any effect “{e(a1[len("Any effect "):])}”, from {chip("Variable", "B6")} to '
            f'{chip("Variable", "B4")} along {gl("L47")}, “{e(a2)}”')
    tail_txt = (f"The atlas adds that any effect “{a1[len('Any effect '):]}”, from Variable B6 to Variable B4 along connection "
                f"L47, graded {GRADE[link('L47')['evidence']][0]}, “{a2}”")
    lead = (f'Its reason opens on the drawn connection, {chip("Connection", "LT01", ":")} feed ranking “changes what people see”.')
    need(reason[0].startswith("Feed ranking changes what people see"), "LTR1's first sentence changed")
    gls = GLOSS["Rejected connection"]
    need(gls.startswith("A relationship that was reviewed against the evidence and left off the map"), "the atlas's rejected connection entry changed")
    b, h, _ = card("TC1", "B6", "LT01", layers=("Technology layer", "Core layer"))
    panel = (f'<p class="k">Reviewed and not drawn</p><p class="hed"><span>From {chip("Variable", "TC1")} to '
             f'{chip("Variable", "B4", ",")} {e(lc(node("B4")["title"]))}</span></p><p class="nt">{lead}</p>'
             f'<p class="q">“{e(quote)}”</p><p class="nt">{tail}</p>'
             f'<p class="nt">The atlas keeps {words_n(len(rej))} connections it reviewed and left off its map, each with its reason.</p>')
    body = (label_for(["LT01"], "the grade of the connection drawn")
            + beside(hed("Connection", "LT01", link("LT01")["name"]) + fig(svg_wrap(b, h)) + f'<p class="nt">{gl("LT01")}</p>',
                     panel + src("connection LT01, rejected connection LTR1 and connection L47")))
    book.add("s-15-10-correct", body, rule="15.10", readable=True, wide=True,
             alt=(f"Connection LT01 from our systems atlas, “{link('LT01')['name']}”, drawn from How platforms rank feeds and seek "
                  "attention, in the technology layer, down to Hostile-content exposure, in the core layer, with the words "
                  f"information, raises. Beside it, under the heading Reviewed and not drawn, the claim from feed ranking to "
                  f"hostility toward the other party, with the atlas’s reason: feed ranking changes what people see; then, quoted, "
                  f"{quote} {tail_txt}"),
             notes="The rejected connection in words only, from the atlas's rejectedLinks record; no line drawn for it.")
    book.log("15.10 correct", "Connection LT01 and rejected LTR1, feeds and hostility", "D10")
    fb, fh, _ = card("TC1", "B4", None, layers=("Technology layer", "Core layer"), sign="+", authority=False,
                     grade="plausible", words=["information,", "raises"])
    fail = dnp() + fig(svg_wrap(fb, fh))
    book.add("s-15-10-failure", fail, rule="15.10",
             alt=(FC + "A dashed line marked information, raises, from How platforms rank feeds and seek attention down to "
                  "Affective polarization, a connection the atlas reviewed and left off its map."),
             notes="Labeled failure: a line drawn for a rejected connection, in the plausible pattern.")
    return {
        "id": "15.10",
        "title": "Show what the model leaves out beside what it draws.",
        "rule": [
            f"Our systems atlas keeps a record of what it left off its map: {words_n(len(rej))} connections it reviewed against "
            f"the evidence and did not draw, {words_n(len(V7['omissions']))} subjects it names as omitted, and a boundary that lists what the "
            "model does not cover. Where a drawing shows a mechanism next to one of those connections, print the connection "
            "beside it in words, with the atlas’s reason, under the heading Reviewed and not drawn.",
            "Draw no line for a connection the atlas reviewed and left out, in any pattern.",
        ],
        "tokens": [],
        "why": {"text": ["A reader who sees feed ranking raise hostile content will ask whether feed ranking raises hostility "
                         "itself. The atlas reviewed that claim and left it off its map, and its reason answers the question "
                         "with the evidence."],
                "basis": "Our systems atlas’s rejected connections, omissions and limits"},
        "correct": {"specimen": "s-15-10-correct",
                    "caption": "Connection LT01 from our systems atlas, with the connection the atlas reviewed and left off its "
                               "map printed beside it in words, with the atlas’s reason."},
        "failure": {"specimen": "s-15-10-failure",
                    "caption": "<strong>Fails Rule 15.10.</strong> A dashed line runs from feed ranking to hostility toward the "
                               "other party, a connection the atlas reviewed and left off its map, so the drawing claims some "
                               "evidence where the largest experiments found no measurable change."},
        "specs": [
            {"label": "Heading", "value": "Reviewed and not drawn"},
            {"label": "Words", "value": "From and to, with typed chips, and the atlas’s reason quoted"},
            {"label": "Line", "value": "None, in any pattern"},
            {"label": "Records", "value": f"{words_n(len(rej)).capitalize()} rejected connections and {words_n(len(V7['omissions']))} omissions, as of the snapshot"},
        ],
        "related": ["13"],
        "builders": ["Look up the atlas’s rejected connections for every pair of variables a drawing shows, and print any match "
                     "in words beside the drawing."],
    }


def C13_sentences(t):
    return [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"])", t.strip()) if x]


# ===============================================================================================================
# Group 2. Reforms on the drawing (round 2, DR-244)
# ===============================================================================================================
BANDS = V7["leverage"]["bands"]
BAND_ORDER = ["parameter", "feedback", "information", "rules", "power to change the rules", "goals"]
need(list(BANDS) == BAND_ORDER, "the atlas's leverage bands changed")
need("Donella Meadows' ordering of leverage points" in V7["leverage"]["intro"], "the atlas's leverage ranking no longer names its source")


def reform(rid, targets, loops, band, problem=None, remedy=None):
    """A reform's record, held to the values a plate prints."""
    need(rid in REFORM, f"reform {rid} is not in the atlas")
    r = REFORM[rid]
    need(r["targets"] == targets and r["loops"] == loops and r["band"] == band and not r.get("rejected"),
         f"reform {rid}'s targets, loops or band changed")
    if problem:
        need(r["problem_evidence"]["grade"] == problem and r["remedy_evidence"]["grade"] == remedy,
             f"reform {rid}'s problem or remedy grade changed")
    return r


def target_items(r, drawn):
    """Each target in its typed chip, in the atlas's order: a connection with its name and grade word, a variable with
    its title. drawn is the set the drawing holds; the build stops if any target is missing from it."""
    need(set(r["targets"]) <= drawn, f"reform {r['id']}'s drawing misses a target")
    out = []
    for t in r["targets"]:
        if t in LINK:
            out.append(f'{chip("Connection", t)} “{e(link(t)["name"])}”.&#160;{grade_word(link(t)["evidence"], gloss=False)}')
        else:
            out.append(f'{chip("Variable", t, ",")} {e(lc(node(t)["title"]))}')
    return out


def acts_note(rid, r):
    n_l = sum(1 for t in r["targets"] if t in LINK)
    n_v = len(r["targets"]) - n_l
    parts = [f"{words_n(n_l)} connection{'s' if n_l != 1 else ''}" if n_l else "",
             f"{words_n(n_v)} variable{'s' if n_v != 1 else ''}" if n_v else ""]
    return (f'<p class="nt">{chip("Reform", rid)} acts where the marks turn red: on '
            f'{" and ".join(p for p in parts if p)}.</p>')


def band_p(r):
    b = r["band"]
    return f'<p class="nt"><b>{e(b.capitalize())}</b>: “{e(BANDS[b])}”</p>'


def loops_p(r, shown):
    """The loops a reform sits on, in typed chips, and the one the drawing shows."""
    need(shown in r["loops"], f"reform {r['id']} does not sit on Loop {shown}")
    cs = [chip("Loop", k) for k in r["loops"]]
    lst = cs[0] if len(cs) == 1 else ", ".join(cs[:-1]) + " and " + cs[-1]
    return f'<p class="nt">{lst}. The drawing shows {chip("Loop", shown, ",")} which holds every target.</p>'


def rule_15_11(book):
    r = reform("R-03", ["L42", "C1", "D7"], ["R4a", "R10", "R12"], "rules", "documented", "plausible")
    lp = LOOP["R4a"]
    codes = [c for c, _ in lp["chain"]]
    need(codes == ["C4", "C1", "D7"] and lp["links"] == ["L42", "L55", "L56"] and lp["type"] == "R"
         and minus_count(lp["links"]) == 0, "Loop R4a changed")
    need([link(x)["evidence"] for x in lp["links"]] == ["documented", "plausible", "documented"], "Loop R4a's grades changed")
    clus = {c: node(c)["cluster"] for c in codes}
    need(clus == {"C4": "C", "C1": "C", "D7": "D"}, "Loop R4a's clusters changed")
    cname = next(x["title"] for x in V7["layers"]["core"]["regions"] if x["id"] == "C")
    need(cname == "Electoral competition", "the core's cluster C changed its name")
    bands = Counter(x["band"] for x in REFORM.values())
    need(bands == Counter({"rules": 26, "parameter": 11, "feedback": 5, "information": 4, "power to change the rules": 3, "goals": 1}),
         f"the reforms' bands changed: {dict(bands)}")
    tg = set(r["targets"])
    b, h = three_loop(codes, lp["links"], inside=("R4a", "reinforcing"), targets=tg)
    svg = svg_wrap(b, h)
    items = kw(target_items(r, set(codes) | set(lp["links"]))
               + [f'{chip("Variable", "C4")} shares {chip("Variable", "C1", "’s")} cluster, {e(cname.lower())}, and stays in ink.'])
    words = (hed("Reform", "R-03", r["title"]) + acts_note("R-03", r)
             + f'<p class="k">Its targets, from the atlas</p>{items}'
             + f'<p class="k">Its band</p>{band_p(r)}'
             + f'<p class="k">Its loops</p>{loops_p(r, "R4a")}'
             + src("reform R-03, loop R4a, connections L42, L55 and L56, and the leverage bands"))
    body = (label_for(lp["links"], "the grade of the loop’s least certain step")
            + beside(hed("Loop", "R4a", lp["title"]) + fig(svg), words))
    book.add("s-15-11-correct", body, rule="15.11", readable=True, wide=True,
             alt=(f"Reform R-03 from our systems atlas, “{r['title']}”, on Loop R4a, “{lp['title']}”. Three pills: "
                  "Incumbent control of election rules at the top, Safe seats below right, Entrenched majority control below "
                  "left. Step 1, from the top to Safe seats, is drawn heavy in red, and the outlines of Safe seats and "
                  "Entrenched majority control are red; step 2, dashed, and step 3 stay in ink, as does Incumbent control of "
                  "election rules. Beside it: the reform acts where the marks turn red, on one connection and two variables: "
                  f"Connection L42, {link('L42')['name']}, documented; Variable C1, {lc(node('C1')['title'])}; Variable D7, "
                  f"{lc(node('D7')['title'])}. Variable C4 shares Variable C1’s cluster, electoral competition, and stays in "
                  f"ink. Its band, rules: {BANDS['rules']} Its loops: Loop R4a, Loop R10 and Loop R12; the drawing shows Loop "
                  "R4a, which holds every target."),
             notes="Targets read from the reform's record and drawn in Rule 12.5's red by wire_marks at the 6 px sizes; the band "
                   "quoted from the atlas's leverage bands.")
    book.log("15.11 correct", "Reform R-03 on Loop R4a, district maps", "D02")
    fb, fh = three_loop(codes, lp["links"], inside=("R4a", "reinforcing"), targets={"C4", "C1", "L42"})
    fail = (dnp() + hed("Reform", "R-03", r["title"]) + fig(svg_wrap(fb, fh))
            + f'<p class="nt">Reform R-03 acts on {e(cname.lower())}.</p>')
    book.add("s-15-11-failure", fail, rule="15.11",
             alt=(FC + "Loop R4a with every mark of the electoral competition cluster in red: Incumbent control of election "
                  "rules, Safe seats and the step between them. Entrenched majority control stays in ink. A note reads: Reform "
                  "R-03 acts on electoral competition."),
             notes="Labeled failure: the red set by the cluster, so a variable the reform does not target turns red and one "
                   "it does target stays in ink.")
    return {
        "id": "15.11",
        "title": "Place a reform on the exact connections and variables it targets, with its band.",
        "rule": [
            f"Each of our systems atlas’s {len(REFORM)} reforms lists its targets, the exact connections and variables it acts "
            "on, and the loops it sits on. Draw the reform on a drawing that holds its targets, and turn only those marks red, "
            "as Rule 12.5 sets: each target connection with its arrowhead, and the outline of each target variable. Beside "
            "the drawing, name the reform, say that it acts where the marks turn red, and list each target in its typed chip.",
            "Mark the targets one by one, even where they fill a cluster, and never turn a frame, a cluster or a whole loop "
            "red in their place. Print the reform’s band beside it in the atlas’s words. The band names the kind of change, "
            "on Donella Meadows’ ordering of leverage points, from changing a number to changing what a system aims for. Of the "
            f"{len(REFORM)} reforms, {bands['rules']} change rules, {bands['parameter']} change a parameter, "
            f"{words_n(bands['feedback'])} feedback, {words_n(bands['information'])} information, "
            f"{words_n(bands['power to change the rules'])} the power to change the rules and {words_n(bands['goals'])} goals.",
        ],
        "tokens": ["oa.color.data.emphasisRed.onNewsprint", TOKEN_LINE],
        "why": {"text": ["A reform moves a few marks, and the rest of the mechanism has to follow on its own. Red on the exact "
                         "targets shows a reader what the reform changes and what it leaves to the loop, before any claim about "
                         "results. Red on a whole cluster claims changes the atlas never lists."],
                "basis": "Our systems atlas’s reform profiles and leverage bands; Rule 12.5"},
        "correct": {"specimen": "s-15-11-correct",
                    "caption": "Reform R-03 on Loop R4a, with red on its one connection and two variables and nothing else, "
                               "its targets listed in typed chips and its band in the atlas’s words."},
        "failure": {"specimen": "s-15-11-failure",
                    "caption": "<strong>Fails Rule 15.11.</strong> The red follows the electoral competition cluster, so "
                               "Variable C4 reads as a target and Variable D7, which the atlas lists, stays in ink."},
        "specs": [
            {"label": "Targets", "value": "Only the connections and variables the reform’s record lists, in Rule 12.5’s red: a "
                                          "connection at 4 px on its ink edge, with its arrowhead; a variable’s outline at 3 px",
             "token": "oa.color.data.emphasisRed.onNewsprint"},
            {"label": "Never red", "value": "A frame, a cluster or a whole loop in place of the targets"},
            {"label": "Note", "value": "The reform’s chip and the words “acts where the marks turn red”, with the count of each kind"},
            {"label": "Band", "value": "The atlas’s word and its definition, quoted: parameter, feedback, information, rules, "
                                       "power to change the rules or goals"},
            {"label": "Loops", "value": "Each loop the reform sits on, in its typed chip; the drawing shows one that holds every target"},
        ],
        "related": ["12", "13"],
        "builders": ["Read the targets, loops and band from the reform’s own record, set the red only on marks whose IDs the "
                     "record lists, and stop the build if a red mark carries any other ID."],
    }


def chain_down(codes, lids, pw=196, x=56, layers=None, targets=(), run=CARD_RUN):
    """An open chain drawn downward, one pill under the next, each connection's words to the right of its line (Rule
    15.8's one direction). layers is (index of the first pill below a boundary, name above, name below). Returns (svg, h)."""
    pills, out, y = [], [], 2
    for i, c in enumerate(codes):
        if i:
            y += run + (24 if layers and layers[0] == i else 0)
        p = Pill(short(c), 2 + pw / 2, 0, pw, red=c in targets)
        p.cy = y + p.h / 2
        y = p.bot
        pills.append(p)
    for i, lid in enumerate(lids):
        a, b = pills[i], pills[i + 1]
        need(a.left + a.h / 2 <= x <= a.right - a.h / 2, "a chain's line misses its pill's flat edge")
        pts = [(x, a.bot + 2), (x, b.top - 2)]
        l = link(lid)
        tg = lid in targets
        m, _ = conn(pts, l["evidence"], l["polarity"], l["delay"], target=tg)
        out.append(wr(m, tg) + verb_at(pts, l["polarity"], step_words(0, lid), "right", big=tg))
        if layers and layers[0] == i + 1:
            out.append(boundary(b.top - 26, [x], layers[1], None) + text(W, b.top - 6, layers[2], "fl", "end"))
    out.append("".join(p.svg() for p in pills))
    return svg_wrap("".join(out), pills[-1].bot + 4), pills


def grade_block(grade, what, quote_html):
    """One of a reform's two grades, as its own label with Rule 13.3's word and gloss, and the atlas's words under it."""
    return (f'<div class="gp">{diagram_label(grade, f"{GRADE[grade][1]}, {what}")}'
            f'<p class="nt">{quote_html}</p></div>')


def rule_15_12(book):
    r = reform("R-32", ["B2", "L26", "LT03"], ["R16", "B1a"], "information", "well-supported", "hypothesis")
    lt03, l26 = link("LT03"), link("L26")
    need((lt03["from"], lt03["to"], lt03["polarity"], lt03["type"], lt03["evidence"]) == ("TC2", "B2", "-", "money", "well-supported")
         and (l26["from"], l26["to"], l26["polarity"], l26["type"], l26["evidence"]) == ("B2", "C3", "+", "information", "well-supported"),
         "connection LT03 or L26 changed")
    need(node("TC2")["layer"] == "technology" and node("B2")["layer"] == node("C3")["layer"] == "core", "the chain's layers changed")
    pg, rg = GLOSS["Problem evidence"], GLOSS["Remedy evidence"]
    need(pg.startswith("Evidence that the condition or mechanism a reform addresses exists.")
         and rg.startswith("Evidence that an intervention changes the condition it targets"), "the atlas's glossary on problem and remedy evidence changed")
    pt = C13_sentences(r["problem_evidence"]["text"])
    need(pt[0] == ("Northwestern University's Medill Local News Initiative counted 213 U.S. counties with no local news source in "
                   "2025, with about 50 million people having limited or no access to local news."), "Reform R-32's problem evidence changed")
    rt_ = r["remedy_evidence"]["text"]
    need(rt_ == ("Funding models exist. Main limitation: no evaluation has yet shown that these funds improve coverage or "
                 "accountability, so their effect remains a hypothesis."), "Reform R-32's remedy evidence changed")
    disp = lambda g: GRADE[g][0]
    two = sum(1 for x in REFORM.values() if disp(x["problem_evidence"]["grade"]) != disp(x["remedy_evidence"]["grade"]))
    rank = ["Documented", "Well supported", "Plausible", "Contested", "Hypothesis"]     # Rule 13.3's order
    lower = sum(1 for x in REFORM.values()
                if rank.index(disp(x["remedy_evidence"]["grade"])) > rank.index(disp(x["problem_evidence"]["grade"])))
    need((two, lower) == (49, 48), f"the count of reforms with two different grades changed: {two}, {lower} with the remedy lower")
    tg = set(r["targets"])
    svg, _ = chain_down(["TC2", "B2", "C3"], ["LT03", "L26"], layers=(1, "Technology layer", "Core layer"), targets=tg)
    blocks = (grade_block(r["problem_evidence"]["grade"], "evidence of the problem",
                          f"The atlas: “{e(pt[0])}”")
              + grade_block(r["remedy_evidence"]["grade"], "evidence for the remedy", f"The atlas: “{e(rt_)}”"))
    words = (hed("Reform", "R-32", r["title"]) + acts_note("R-32", r)
             + f'<p class="k">Two grades, apart</p>{blocks}'
             + src("reform R-32, its problem and remedy evidence, and connections LT03 and L26"))
    body = (label_for(["LT03", "L26"], "the grade of both connections drawn")
            + beside(fig(svg) + f'<p class="nt">{gl("LT03")}</p><p class="nt">{gl("L26")}</p>', words))
    book.add("s-15-12-correct", body, rule="15.12", readable=True, wide=True,
             alt=(f"Reform R-32 from our systems atlas, “{r['title']}”, on a chain of three pills drawn downward: Concentration "
                  "of platforms and digital advertising, in the technology layer, then across a rule into the core layer, Local "
                  "news supply and Electoral pressure. Both connections and the outline of Local news supply are red: money, "
                  "lowers, then information, raises. A label over the drawing reads Well supported, the grade of both "
                  "connections. Beside it, two more labels: Well supported, strong research evidence, for the evidence of the "
                  f"problem, with the atlas’s words: {pt[0]} Hypothesis, not yet tested, for the evidence for the remedy, with "
                  f"the atlas’s words: {rt_}"),
             notes="Both grades and their words read from the reform's problem_evidence and remedy_evidence; the connections' "
                   "grades from their own records.")
    book.log("15.12 correct", "Reform R-32, local news", "D01")
    fsvg, _ = chain_down(["TC2", "B2", "C3"], ["LT03", "L26"], layers=(1, "Technology layer", "Core layer"), targets=tg)
    fail = (dnp() + diagram_label("well-supported", "strong research evidence") + hed("Reform", "R-32", r["title"]) + fig(fsvg))
    book.add("s-15-12-failure", fail, rule="15.12",
             alt=(FC + "Reform R-32 on the same chain under one label for the whole reform: Well supported, strong research "
                  "evidence. No grade is given for the remedy."),
             notes="Labeled failure: one grade over the reform, borrowed from the problem and the connections.")
    return {
        "id": "15.12",
        "title": "Grade the evidence for the problem and for the remedy apart.",
        "rule": [
            "Our systems atlas grades each reform twice. Evidence of the problem is, in its glossary’s words, “"
            + pg.split(". ")[0][0].lower() + pg.split(". ")[0][1:] + "”. Evidence for the remedy is “"
            + rg.split(", with")[0][0].lower() + rg.split(", with")[0][1:] + "”. Print each as its own label with Rule "
            "13.3’s word and gloss, and quote the atlas’s words under it.",
            "A drawing of the reform carries a third grade, the line code on each connection (Rule 13.4), which says how sure "
            f"the atlas is of the mechanism. Keep all three apart. Of the atlas’s {len(REFORM)} reforms, {two} carry two "
            f"different grades, and in {lower} of them the remedy’s grade is the lower.",
        ],
        "tokens": ["oa.chart.grade.documented", "oa.chart.grade.hypothesis"],
        "why": {"text": ["A problem on the record says nothing yet about whether a fix works. A reader shown one grade carries the "
                         "stronger to both, and a well-documented harm then reads as proof of a remedy no one has tested."],
                "basis": "Our systems atlas’s glossary and reform profiles; Rule 13.3"},
        "correct": {"specimen": "s-15-12-correct",
                    "caption": "Reform R-32 with its two grades apart: the evidence of the problem well supported, and the "
                               "evidence for the remedy a hypothesis, each in the atlas’s words, beside the grade of the "
                               "connections drawn."},
        "failure": {"specimen": "s-15-12-failure",
                    "caption": "<strong>Fails Rule 15.12.</strong> One label, Well supported, covers the reform, so the loss of "
                               "local news reads as proof that funding would restore it. The atlas grades that remedy a hypothesis."},
        "specs": [
            {"label": "Problem", "value": "Its own label: Rule 13.3’s word and gloss, then “evidence of the problem”, and the atlas’s words quoted"},
            {"label": "Remedy", "value": "Its own label the same way, “evidence for the remedy”"},
            {"label": "Connections", "value": "Their own line code (Rule 13.4), and the drawing’s label from the least certain (Rule 13.1)"},
            {"label": "Never", "value": "One grade for the whole reform"},
            {"label": "Counts", "value": f"{two} of {len(REFORM)} reforms carry two different grades, as of the snapshot"},
        ],
        "related": ["13"],
        "builders": ["Read the two grades from <code>problem_evidence</code> and <code>remedy_evidence</code>, print each through "
                     "Rule 13.3’s table, and never fall back from one to the other."],
    }


# ===============================================================================================================
# Group 2. Worked examples from the atlas
# ===============================================================================================================
def rule_15_13(book):
    lp = LOOP["R1"]
    need(lp["links"] == ["L01", "L02", "L03"] and lp["type"] == "R" and lp["evidence"] == "plausible" and lp["delay"] == "L",
         "Loop R1 changed")
    g = [(link(x)["evidence"], link(x)["polarity"], link(x)["type"], link(x)["delay"]) for x in lp["links"]]
    need(g == [("well-supported", "+", "money", "S"), ("plausible", "+", "money", "M"), ("well-supported", "+", "money", "L")],
         "Loop R1's connections changed")
    es = lp["evidence_summary"]
    q = "The middle step, L02: Political spending can tilt policy toward donors, is plausible and the weakest."
    need(q in es, "Loop R1's evidence summary no longer names L02 its weakest step")
    need(least_certain(lp["links"]) == "plausible", "Loop R1's least certain grade changed")
    frag = "is plausible and the weakest."
    need(q.endswith(frag), "the atlas's words on Loop R1's weakest step changed")
    said = (f'In the atlas’s evidence summary, the middle step, {chip("Connection", "L02", ",")} “{e(frag)}”')
    said_alt = f"In the atlas’s evidence summary, the middle step, connection L02, “{frag}”"
    codes = ["A1", "B1", "E1"]
    b, h = three_loop(codes, lp["links"], weakest=1, inside=("R1", "reinforcing"))
    svg = svg_wrap(b, h)
    steps = kw([f"<b>{i}</b>&#160;{say_link(x)}" + (" The atlas names it the weakest step." if x == "L02" else "")
                for i, x in enumerate(lp["links"], 1)])
    # AX S9: a reader who lands here by a link meets "money, raises" and the ticks with no gloss, so the plate says what
    # each means, in the delay classes chapter 13 reads from the atlas (one tick per class, short to long, all three here)
    need([DELAY[link(x)["delay"]][0] for x in lp["links"]] == [1, 2, 3], "Loop R1's steps no longer show one, two and three ticks")
    ticks = ", ".join(f"{words_n(DELAY[k][0])} for {DELAY[k][1]}" for k in ("S", "M", "L"))
    dg = GLOSS["Delay"].split(".")[0]
    need(dg == "The time between a change and its effect", "the atlas's definition of a delay changed")
    gloss = kw(["<b>money, raises</b>: money is what moves along the connection (Rule 15.4), and raises says the next "
                "variable moves the same way as the one before it (Rule 15.3).",
                f"<b>Ticks</b> near a line’s start count its delay, {e(dg[0].lower() + dg[1:])}: {ticks} (Rule 13.5)."])
    body = (diagram_label("plausible", "some evidence, the grade of the loop’s least certain step, Connection L02")
            + beside(hed("Loop", "R1", lp["title"]) + fig(svg) + f'<p class="k">Reading a step</p>{gloss}',
                     ra_p(read_aloud(codes, lp["links"])) + f'<p class="k">Each step, and the weakest</p>{steps}'
                     f'<p class="nt">{said}</p>' + src("loop R1 and connections L01, L02 and L03")))
    book.add("s-15-13-correct", body, rule="15.13", readable=True, wide=True,
             alt=(f"Loop R1 from our systems atlas, “{lp['title']}”, under a label reading Plausible, the grade of its least "
                  "certain step. Three pills: Wealth concentration at the top, Money in politics below right, Policy tilt to "
                  "insiders below left. Step 1, solid, money, raises; step 2, dashed, money, raises, marked weakest step; step 3, "
                  f"solid, money, raises. The loop reads: {read_aloud(codes, lp['links'])} Beside it, each step with its grade. "
                  f"{said_alt} A key says money is what moves along each connection and raises says the next variable moves "
                  f"the same way, and that ticks count a step’s delay, {dg[0].lower() + dg[1:]}: {ticks}."),
             notes="Grades, signs, types and delays from each connection's record; the weakest step from the loop's evidence summary.")
    book.log("15.13 correct", "Loop R1, wealth and influence", "D03")
    fb, fh = three_loop(codes, lp["links"], grades={1: "well-supported"})
    fail = dnp() + diagram_label("well-supported", "strong research evidence") + hed("Loop", "R1", lp["title"]) + fig(svg_wrap(fb, fh))
    book.add("s-15-13-failure", fail, rule="15.13",
             alt=(FC + "Loop R1 drawn with all three steps solid under a label reading Well supported, with no weakest step marked."),
             notes="Labeled failure: the loop given its strongest step's grade, and the plausible step drawn solid.")
    return {
        "id": "15.13",
        "title": "Let the least certain step set how far a reader trusts a loop.",
        "rule": [
            f"Loop R1, “{lp['title']}”, runs through three connections that carry money. Two are well supported. The middle "
            f"one, connection L02, “{link('L02')['name']}”, is plausible, and our systems atlas names it the weakest step. The "
            "loop as a whole takes that grade: the atlas grades Loop R1 plausible.",
            "Draw each step in its own line, mark the weakest in words, and give the diagram’s label the grade of the least "
            "certain step (Rule 13.1). The loop stepper of Rule 18.22 runs the same loop live, one connection at a time, in "
            "Rule 11.14’s plate.",
        ],
        "tokens": ["oa.chart.grade.plausible"],
        "why": {"text": ["A loop runs only when each of its steps runs, so its least certain step limits the whole. A reader who "
                         "sees two solid lines and one dashed line can say how far the loop holds before reading its record."],
                "basis": "Our systems atlas, Loop R1’s record and evidence summary"},
        "correct": {"specimen": "s-15-13-correct",
                    "caption": "Loop R1 from our systems atlas, with its middle step dashed and marked as the weakest, under a "
                               "label that gives the whole loop that step’s grade."},
        "failure": {"specimen": "s-15-13-failure",
                    "caption": "<strong>Fails Rule 15.13.</strong> Every step is solid and the label reads Well supported, so "
                               "the loop borrows the grade of its strongest steps and hides the one the atlas calls weakest."},
        "specs": [
            {"label": "Each step", "value": "Its own line, by its own grade (Rule 13.4)"},
            {"label": "Weakest step", "value": "“Weakest step” under its words, where the atlas’s evidence summary names it"},
            {"label": "The loop’s label", "value": "The least certain step’s grade (Rule 13.1)"},
            {"label": "Live", "value": "The loop stepper of Rule 18.22 runs Loop R1 in Rule 11.14’s plate"},
        ],
        "related": ["11", "13", "18"],
        "builders": ["Take the weakest step from the loop’s evidence summary and the label from the least certain connection, "
                     "and stop the build if the two disagree."],
    }


def rule_15_14(book):
    lp = LOOP["R8"]
    need(lp["links"] == ["L38", "L39"] and lp["type"] == "R" and lp["delay"] == "L", "Loop R8 changed")
    rev = "the loop no longer depends on A1"
    need(lp["evidence"] == "well-supported for both links; " + rev, "Loop R8's evidence note changed")
    qual = lp["qualification"]
    tq = ("Rising home equity tends to lower the top 1% share of wealth (T12: Rising home equity lowers the top wealth share), "
          "so this loop does not explain that share.")
    need(tq in qual, "Loop R8's qualification changed")
    t12 = link("T12")
    need((t12["from"], t12["to"], t12["polarity"]) == ("A6", "A1", "-"), "connection T12 changed")
    r1, r2 = "tends to lower the top 1% share of wealth", "so this loop does not explain that share."
    need(tq == f"Rising home equity {r1} (T12: {t12['name']}), {r2}", "Loop R8's qualification changed")
    why_html = (f'Its reason, from the atlas’s qualification: rising home equity “{e(r1)}”, as {chip("Connection", "T12")} '
                f'“{e(t12["name"])}” records, “{e(r2)}”')
    why_txt = (f"Its reason, from the atlas’s qualification: rising home equity “{r1}”, as connection T12, “{t12['name']}”, "
               f"records, “{r2}”")
    need([link(x)["evidence"] for x in lp["links"]] == ["well-supported", "well-supported"], "Loop R8's grades changed")
    f1, f2 = "well-supported for both links", "no longer depends on"
    need(lp["evidence"] == f"{f1}; the loop {f2} A1", "Loop R8's evidence note changed")
    rev_html = (f'Its evidence note reads “{e(f1)}”, and says the loop “{e(f2)}” {chip("Variable", "A1", ",")} '
                f'{e(lc(node("A1")["title"]))}.')
    rev_txt = (f"Its evidence note reads “{f1}”, and says the loop “{f2}” Variable A1, {lc(node('A1')['title'])}.")
    codes = ["A5", "A6"]
    b, h, _ = two_loop(codes, lp["links"], inside=("R8", "reinforcing"))
    panel = (f'<p class="k">The atlas’s revision, as of {SNAP}</p><p class="nt">{rev_html}</p>'
             f'<p class="nt">{why_html}</p>')
    body = (diagram_label("well-supported", "strong research evidence, the grade of both steps")
            + beside(hed("Loop", "R8", lp["title"]) + fig(svg_wrap(b, h)),
                     ra_p(read_aloud(codes, lp["links"])) + panel
                     + src("loop R8, its evidence note and qualification, and connection T12")))
    book.add("s-15-14-correct", body, rule="15.14", readable=True, wide=True,
             alt=(f"Loop R8 from our systems atlas, “{lp['title']}”, under a label reading Well supported. Two pills, Housing "
                  "scarcity and Owner home equity, with step 1 over the top, plus, raises, and step 2 under the bottom, plus, "
                  f"raises, both solid with three delay ticks. The loop reads: {read_aloud(codes, lp['links'])} Beside it, the "
                  f"atlas’s revision as of {SNAP}. {rev_txt} {why_txt}"),
             notes="The revision and its reason quoted from the loop's evidence and qualification fields, with the snapshot date.")
    book.log("15.14 correct", "Loop R8, housing scarcity", "D09")
    stations = [short("A5"), short("A6"), short("A1")]
    fb, fh = drawn_loop(3, stations, [{"sign": "+", "grade": "well-supported", "delay": "L"}] * 3, inside=("R8", "reinforcing"))
    fail = dnp() + hed("Loop", "R8", lp["title"]) + fig(svg_wrap(fb, fh))
    book.add("s-15-14-failure", fail, rule="15.14",
             alt=(FC + "Loop R8 drawn through three pills, Housing scarcity, Owner home equity and Wealth concentration, with "
                  "plus signs on every step and no date."),
             notes="Labeled failure: the loop routed through A1 with plus signs, against the atlas's revision and connection T12's minus.")
    return {
        "id": "15.14",
        "title": "Show a change to the model in the atlas’s own words, with its date.",
        "rule": [
            "Our systems atlas revises its model as the evidence changes, and it records some revisions in its own text. Loop R8, "
            f"“{lp['title']}”, carries one: its evidence note reads “{f1}”, and says the loop “{f2}” Variable A1, "
            f"{lc(node('A1')['title'])}. Quote a revision as the atlas writes it, with the snapshot date, and draw the loop as "
            "it stands now.",
            "A drawing made before the revision is a record of what we drew. It is never evidence for the model, and a page "
            "that published one corrects it as Rule 13.13 sets out.",
        ],
        "tokens": [],
        "why": {"text": ["A revision in the atlas’s own words lets a reader check it against the atlas, and the date tells them "
                         "which version they read. This one changes what the loop explains: the atlas records that rising home "
                         "equity tends to lower the top wealth share, so the loop no longer accounts for wealth at the top."],
                "basis": "Our systems atlas, Loop R8’s record and connection T12"},
        "correct": {"specimen": "s-15-14-correct",
                    "caption": "Loop R8 as our systems atlas holds it, with the atlas’s revision and its reason quoted beside "
                               f"the drawing, as of {SNAP}."},
        "failure": {"specimen": "s-15-14-failure",
                    "caption": "<strong>Fails Rule 15.14.</strong> The drawing routes Loop R8 through wealth concentration with "
                               "plus signs and prints no date. The atlas says the loop no longer depends on Variable A1, and its "
                               "connection T12 runs from home equity to the top wealth share with a minus."},
        "specs": [
            {"label": "Revision", "value": "The atlas’s words, quoted, from the record that carries them"},
            {"label": "Date", "value": f"“As of” and the snapshot date, {SNAP} (Rule 13.10)"},
            {"label": "Drawing", "value": "The loop as the atlas holds it now"},
            {"label": "An earlier drawing", "value": "A record, never evidence; a published one is corrected under Rule 13.13"},
        ],
        "related": ["13"],
        "builders": ["Quote the revision from the loop’s own fields, and stop the build when those fields change, so the "
                     "quotation never drifts from the atlas."],
    }


def rule_15_15(book):
    """Worked example 3: Loop B4 beside Loop R10, through Variable C3, which both hold (Master Brief section 14)."""
    b4, r10 = LOOP["B4"], LOOP["R10"]
    need([c for c, _ in b4["chain"]] == ["D5", "C3", "C5"] and b4["links"] == ["L23", "L24", "L54"] and b4["type"] == "B"
         and [link(x)["polarity"] for x in b4["links"]] == ["-", "+", "+"], "Loop B4 changed")
    need([c for c, _ in r10["chain"]] == ["C1", "C2", "C3", "C4"] and r10["links"] == ["L08", "L25", "L53", "L42"]
         and r10["type"] == "R", "Loop R10 changed")
    both = sorted(set(c for c, _ in b4["chain"]) & set(c for c, _ in r10["chain"]))
    need(both == ["C3"], f"Loops B4 and R10 share {both}, where the example follows Variable C3 alone")
    need([link(x)["evidence"] for x in b4["links"]] == ["well-supported"] * 3, "Loop B4's grades changed")
    need(r10["evidence"].endswith("plausible for C3 to C4 (the weakest link)"), "Loop R10's weakest link changed")
    c3 = node("C3")
    need(short("C3") == "Electoral pressure" and c3["title"] == "Risk of losing office", "Variable C3's names changed")
    ep = GLOSS["Electoral pressure"]
    need(ep == "The credible chance that an official will lose office. It can change behavior before any election removes anyone.",
         "the atlas's entry for electoral pressure changed")
    qual = "The loop works only where seats are competitive."
    need(b4["qualification"].startswith(qual), "Loop B4's qualification changed")
    val = b4["valence"]
    need("Its strength depends on C1: Seats with little electoral competition, C2: How often the primary decides the winner," in val,
         "Loop B4's valence changed")
    # in and out of Variable C3 in each loop: the connection that arrives and the one that leaves
    ins = {"B4": ("L23", "L24"), "R10": ("L25", "L53")}
    for k, (a, b_) in ins.items():
        need(link(a)["to"] == "C3" and link(b_)["from"] == "C3" and a in LOOP[k]["links"] and b_ in LOOP[k]["links"],
             f"Variable C3's steps in Loop {k} changed")
    cols = []
    specs_ = (("B4", "balancing", 3), ("R10", "reinforcing", 4))
    for lid, kind, n in specs_:
        lp = LOOP[lid]
        codes = [c for c, _ in lp["chain"]]
        if n == 3:
            b, h = three_loop(codes, lp["links"], inside=(lid, kind), shared={"C3"})
        else:
            b, h = four_loop(codes, lp["links"], inside=(lid, kind), shared={"C3"})
        a, b_ = ins[lid]
        steps = (f'<p class="k">Variable C3 in this loop</p>'
                 + kw([f'<b>In</b>&#160;{gl(a)}: “{e(link(a)["sign_meaning"])}”',
                       f'<b>Out</b>&#160;{gl(b_)}: “{e(link(b_)["sign_meaning"])}”']))
        cols.append(f'<div>{label_for(lp["links"], "the grade of the loop’s least certain step")}{hed("Loop", lid, lp["title"])}'
                    f'{fig(svg_wrap(b, h), read_aloud(codes, lp["links"]))}{steps}</div>')
    meet = (f'<p class="k">Where the two loops meet</p>'
            f'<p class="nt">{chip("Variable", "C3", ",")} {e(lc(c3["title"]))}, is the pill filled in ink in both drawings. '
            f'The atlas calls it electoral pressure: “{e(ep)}”</p>'
            f'<p class="nt">Loop B4, in the atlas’s words, “{e(qual[len("The loop "):])}” Its strength depends on '
            f'{chip("Variable", "C1")} and {chip("Variable", "C2", ",")} which Loop R10’s first step joins.</p>')
    body = (f'<div class="fx pr">{"".join(cols)}</div><div class="kb">{meet}</div>'
            + src("loops B4 and R10, their connections, and the glossary entry for electoral pressure"))
    book.add("s-15-15-correct", body, rule="15.15", readable=True, wide=True,
             alt=(f"Loop B4, “{b4['title']}”, beside Loop R10, “{r10['title']}”, from our systems atlas. Both pass through "
                  "Electoral pressure, the pill filled in ink in each drawing. Loop B4 draws three pills, Public service "
                  "quality, Electoral pressure and Sanction applied, its steps marked minus, plus and plus, balancing. Loop R10 "
                  "draws four on a square, Safe seats, Primary decisiveness, Electoral pressure and Incumbent control of election "
                  "rules, its steps marked plus, minus, minus and plus, reinforcing. Under each, the connection into Electoral "
                  f"pressure and the one out of it, with the atlas’s sentences. In Loop B4: {link('L23')['sign_meaning']} "
                  f"{link('L24')['sign_meaning']} In Loop R10: {link('L25')['sign_meaning']} {link('L53')['sign_meaning']} "
                  f"A note says Variable C3, risk of losing office, is the shared variable, which the atlas defines: {ep} Loop "
                  "B4 works only where seats are competitive, and its strength depends on Variable C1 and Variable C2, which "
                  "Loop R10’s first step joins."),
             notes="Both loops read by script; the shared variable found as the intersection of their chains; the in and out "
                   "connections of Variable C3 checked against each loop.")
    book.log("15.15 correct", "Loop B4, public services", "D04")
    book.log("15.15 correct", "Loop R10, safe seats", "D02")
    fcols = []
    for lid, kind, n in specs_:
        lp = LOOP[lid]
        codes = [c for c, _ in lp["chain"]]
        labels = [short(c) if c != "C3" or lid == "B4" else c3["title"] for c in codes]
        if n == 3:
            b, h = three_loop(codes, lp["links"], inside=(lid, kind), labels=labels)
        else:
            b, h = four_loop(codes, lp["links"], inside=(lid, kind), labels=labels)
        fcols.append(f'<div>{hed("Loop", lid, lp["title"])}{fig(svg_wrap(b, h))}</div>')
    fail = dnp() + f'<div class="fx pr">{"".join(fcols)}</div>'
    book.add("s-15-15-failure", fail, rule="15.15", wide=True,
             alt=(FC + "The same two loops side by side, with the shared variable named Electoral pressure in Loop B4 and Risk "
                  "of losing office in Loop R10, in plain pills, with no chip and no word that the two are one variable."),
             notes="Labeled failure: the shared variable under two names and no mark, so the loops read as unrelated.")
    return {
        "id": "15.15",
        "title": "Follow a variable two loops share through each loop in turn.",
        "rule": [
            f"Loop B4, “{b4['title']}”, and Loop R10, “{r10['title']}”, both pass through Variable C3, "
            f"{lc(c3['title'])}. Draw the two loops side by side, give the shared variable the same short name in both, and "
            "fill its pill in ink in each drawing, the one place a pill takes a fill. Under each loop, print the connection "
            "that brings a change into the shared variable and the one that carries it on, with the atlas’s sentence on each sign.",
            "Then say where the loops meet, in the atlas’s words. Loop R10 lowers the risk of losing office as primaries "
            "decide more seats, and Loop B4 turns that same risk into defeats that improve public services. The atlas says "
            f"Loop B4 “{qual[len('The loop '):][:-1]}”.",
        ],
        "tokens": [TOKEN_LINE],
        "why": {"text": ["Two loops drawn apart look like two separate stories. A variable they share is where one can weaken or "
                         "strengthen the other, and a reader can find it only if it carries one name and one mark in both."],
                "basis": "Our systems atlas, Loops B4 and R10 and the glossary entry “Electoral pressure”"},
        "correct": {"specimen": "s-15-15-correct",
                    "caption": "Loop B4 beside Loop R10, with Variable C3 filled in ink in both, the connections in and out of it "
                               "in each loop, and the atlas’s words on where the two meet."},
        "failure": {"specimen": "s-15-15-failure",
                    "caption": "<strong>Fails Rule 15.15.</strong> The shared variable takes a different name in each loop and "
                               "no mark, so the loops read as unrelated. Both pass through Variable C3, the risk of losing office."},
        "specs": [
            {"label": "Order", "value": "The two loops side by side from 680 px, one under the other below it"},
            {"label": "Shared variable", "value": "One short name in both drawings, its pill filled in ink with its name in the surface color",
             "token": "oa.color.graphic.essential.onNewsprint"},
            {"label": "In and out", "value": "Under each loop, the connection into the shared variable and the one out of it, with "
                                             "their chips, grade words and the atlas’s sentences on their signs"},
            {"label": "Where they meet", "value": "The atlas’s words, quoted, with the shared variable’s chip"},
        ],
        "related": ["13"],
        "builders": ["Find the shared variable as the overlap of the two loops’ chains, by script, and stop the build if the "
                     "loops share none or more than the one the page follows."],
    }


def effect_rows(r):
    """One row for each outcome family: its name, then the pips, the atlas's code and its words (Rule 13.5's mark). The
    families keep the atlas's order and no row adds them."""
    out = []
    for fam in ("DQ", "GE", "EP", "EQ"):
        v = r["effects"][fam]
        code = v.split(" ")[0]
        need(code in EFFECT_WORDS, f"reform {r['id']}'s effect {v!r} has no code")
        qual = v[len(code):].strip()
        words = EFFECT_WORDS[code] + (f", {qual}" if qual else "")
        out.append(f'<li><span>{e(FAMILY[fam])}</span><span class="fv">{C13.pips_svg(code)}'
                   f'<span><b>{e(code.replace("-", MINUS))}</b> {e(words)}</span></span></li>')
    return '<ul class="ef">' + "".join(out) + "</ul>"


def route_rows(r, dated=True):
    """One row for each route: its chip and name, who acts, the feasibility word, and the route's own check date or
    "Not checked" in the same type and place (Rule 13.10). dated=False is a failure plate's: every route under one date."""
    out = []
    for x in r["routes"]:
        when = (f"Checked {C13.words_date(x['checked'])}" if x["checked"] else "Not checked") if dated else f"Checked {SNAP}"
        out.append(f'<li><span>{chip("Route", x["route"])} {e(C13.ROUTE_NAME[x["route"]])}</span>'
                   f'<p class="sub">{e(x["who"])}</p>'
                   f'<span class="rd"><span><b>{e(x["feasibility"].capitalize())}</b> feasibility</span><span>{e(when)}</span></span></li>')
    return '<ul class="ef">' + "".join(out) + "</ul>"


FAMILY, EFFECT_WORDS = C13.FAMILY, C13.EFFECT_WORDS


def rule_15_16(book):
    """Worked example 4: Reform R-01 at its actual targets, its effects with no total and its routes with their dates.
    R-01 is drawn as every other reform is (DR-223), and the page carries no disclosure (DR-100)."""
    r = reform("R-01", ["L25", "L08", "C2"], ["R10", "B4", "R11"], "rules", "plausible", "plausible_contested")
    need(r["effects"] == {"DQ": "+M", "GE": "+S", "EP": "0", "EQ": "0"}, "Reform R-01's effects changed")
    need(r["effects_confidence"] == "medium (participation); low (moderation)", "Reform R-01's confidence changed")
    rts = [(x["route"], x["feasibility"], x["checked"]) for x in r["routes"]]
    need(rts == [("BI", "medium", "2026-10-15"), ("SS", "low", None), ("LOC", "medium", "2026-10-15"), ("FS", "very low", None)],
         f"Reform R-01's routes changed: {rts}")
    note = V7["outcomes"]["effect_codes_note"]
    q_note = "The codes are conditional on the reform working as described, and codes for different families are never added together."
    need(q_note in note, "the atlas's note on effect codes changed")
    feas = GLOSS["Feasibility"]
    need(feas.endswith("The Atlas rates it high, medium, low or very low for 2026 to 2030."), "the atlas's entry for feasibility changed")
    lp = LOOP["R10"]
    codes = [c for c, _ in lp["chain"]]
    tg = set(r["targets"])
    b, h = four_loop(codes, lp["links"], inside=("R10", "reinforcing"), targets=tg)
    svg = svg_wrap(b, h)
    pe, re_ = r["problem_evidence"]["grade"], r["remedy_evidence"]["grade"]
    words = (hed("Reform", "R-01", r["title"]) + acts_note("R-01", r)
             + f'<p class="k">Its targets</p>{kw(target_items(r, set(codes) | set(lp["links"])))}'
             + f'<p class="k">Its loops</p>{loops_p(r, "R10")}'
             + f'<p class="k">Its evidence</p>'
             + f'<p class="nt">Of the problem: {grade_word(pe)}. For the remedy: {grade_word(re_)}.</p>')
    fx = (f'<div><p class="k">Effects by outcome family, as of {SNAP}</p>{effect_rows(r)}'
          f'<p class="nt">The atlas: “{e(q_note)}” Its confidence in these sizes: “{e(r["effects_confidence"])}”.</p></div>'
          f'<div><p class="k">Routes, with the date each was checked</p>{route_rows(r)}'
          f'<p class="nt">Feasibility is the atlas’s judgment for 2026 to 2030.</p></div>')
    body = (label_for(lp["links"], "the grade of the loop’s least certain step")
            + beside(hed("Loop", "R10", lp["title"]) + fig(svg), words)
            + f'<div class="two">{fx}</div>'
            + src("reform R-01, its targets, effects and routes, and loop R10 with its connections"))
    fam_alt = "; ".join(f"{FAMILY[k]}, {r['effects'][k]}, {EFFECT_WORDS[r['effects'][k]]}" for k in ("DQ", "GE", "EP", "EQ"))
    rt_alt = "; ".join(f"Route {x['route']}, {C13.ROUTE_NAME[x['route']]}, {x['who']}, {x['feasibility']} feasibility, "
                       + (f"checked {C13.words_date(x['checked'])}" if x["checked"] else "not checked") for x in r["routes"])
    book.add("s-15-16-correct", body, rule="15.16", readable=True, wide=True,
             alt=(f"Reform R-01 from our systems atlas, “{r['title']}”, on Loop R10, “{lp['title']}”, drawn on a square: "
                  "Safe seats, Primary decisiveness, Electoral pressure and Incumbent control of election rules. Step 1, from "
                  "Safe seats to Primary decisiveness, and step 2, from Primary decisiveness to Electoral pressure, are drawn "
                  "heavy in red, and the outline of Primary decisiveness is red; the other two steps and pills stay in ink. "
                  f"Beside it: Connection L08, {link('L08')['name']}, documented; Connection L25, {link('L25')['name']}, well "
                  f"supported; Variable C2, {lc(node('C2')['title'])}. Its loops: Loop R10, Loop B4 and Loop R11. Evidence of "
                  f"the problem, plausible; for the remedy, contested. Effects by outcome family, as of {SNAP}, one row each: "
                  f"{fam_alt}. {q_note} Routes: {rt_alt}."),
             notes="Targets, effects, confidence and routes read from the reform's record; each route's own check date or Not "
                   "checked; no row adds the families. No disclosure prints (DR-100).")
    book.log("15.16 correct", "Reform R-01, primaries", "D02")
    fail = (dnp() + hed("Reform", "R-01", r["title"])
            + f'<p class="k">Overall effect</p><ul class="ef"><li><span>All four families</span><span class="fv">'
              f'{C13.pips_svg("+L")}<span><b>+L</b> large positive</span></span></li></ul>'
            + f'<p class="k">Routes</p>{route_rows(r, dated=False)}')
    book.add("s-15-16-failure", fail, rule="15.16",
             alt=(FC + "Reform R-01 with one overall effect for all four families, three pips and +L, large positive, and its "
                  f"four routes each marked checked {SNAP}."),
             notes="Labeled failure: the families added into one score, and every route given the reform's snapshot date.")
    return {
        "id": "15.16",
        "title": "Show a reform’s four effects side by side, with each route’s check date.",
        "rule": [
            f"Reform R-01, “{r['title']}”, targets two connections and one variable on Loop R10, and sits on Loops R10, B4 "
            "and R11. Draw it where it acts (Rule 15.11), then print its effects one outcome family to a row, each with the "
            "atlas’s code, its words and the pips of Rule 13.5, and no row that adds them. Its routes follow, each with who "
            "acts there, its feasibility and its own check date, or “Not checked” where the atlas gives none (Rule 13.10).",
            f"As of {SNAP}, the atlas codes a moderate gain for the quality of democracy, a small one for government "
            "efficacy and no expected effect on the other two. It checked the state ballot and local routes on that date, "
            "and the state statute and federal statute routes carry no date.",
        ],
        "tokens": ["oa.color.data.emphasisRed.onNewsprint", TOKEN_LINE],
        "why": {"text": ["A single score would hide what the atlas keeps apart: the families use different units, and a reform "
                         "can help one while it costs another. A route rated without a date reads as current, and a reader "
                         "deciding where to act needs to know which ratings the atlas checked."],
                "basis": "Our systems atlas, Reform R-01’s profile and its note on effect codes; Rules 13.5 and 13.10"},
        "correct": {"specimen": "s-15-16-correct",
                    "caption": f"Reform R-01 at its targets on Loop R10, with its four effects one family to a row and its "
                               f"four routes each dated or marked not checked, as of {SNAP}."},
        "failure": {"specimen": "s-15-16-failure",
                    "caption": "<strong>Fails Rule 15.16.</strong> The card adds two gains into one large positive score and "
                               f"dates all four routes {SNAP}. The atlas adds no families, and it checked only the ballot and "
                               "local routes."},
        "specs": [
            {"label": "Where it acts", "value": "Its targets in Rule 12.5’s red, as Rule 15.11 sets"},
            {"label": "Effects", "value": "One row per outcome family, in the atlas’s order, with the pips, the code and its words; "
                                          "the atlas’s note that codes are never added, quoted"},
            {"label": "Routes", "value": "Chip and name, who acts, feasibility, and “Checked” with the route’s own date, or “Not checked”"},
            {"label": "Date", "value": f"“As of {SNAP}” over the effects, the snapshot date"},
            {"label": "Never", "value": "A total, an overall score, or a route dated from the reform’s status"},
        ],
        "related": ["12", "13"],
        "builders": ["Print each family from the reform’s <code>effects</code> record and each route from its <code>routes</code> "
                     "list, and stop the build if any row sums or a route without a <code>checked</code> date prints one."],
    }


# ===============================================================================================================
# The chapter
# ===============================================================================================================
def chapter(book):
    op = opener(book)
    rules = [rule_15_1(book), rule_15_2(book), rule_15_3(book), rule_15_4(book), rule_15_5(book), rule_15_6(book),
             rule_15_7(book), rule_15_8(book), rule_15_9(book), rule_15_10(book), rule_15_13(book), rule_15_14(book)]
    need([r["id"] for r in rules] == BUILT, "the chapter's rules differ from the round's list")
    need(not set(BUILT) & set(PLANNED), "a rule is both built and planned")
    data = {
        "number": "15",
        "anchor": "systems-graphics",
        "title": "Systems graphics",
        "part": "Evidence and media",
        "instruction": "Draw our systems atlas’s mechanisms so a reader can follow them one connection at a time.",
        "opener": op,
        "intro": [
            "A systems graphic draws a mechanism: what moves what, which way, and how sure our systems atlas, Who Do They "
            "Answer To?, is of each step. It uses the atlas’s own parts. Variables are the quantities or conditions that can "
            "rise or fall, connections are the arrows between them, and loops are chains of connections that come back to "
            "where they started.",
            "Chapter 13 sets how a connection carries its grade, its delay and its source. The rules here show how to read and "
            "combine those marks, then work through mechanisms from the atlas as it records them.",
        ],
        "groups": [
            {"before_rule": "15.1", "number": 1, "title": "Reading a systems drawing",
             "line": "Each mark in a systems drawing answers one question about the mechanism, and a reader can name every "
                     "answer without color."},
            {"before_rule": "15.13", "number": 2, "title": "Worked examples from the atlas",
             "line": "Each example draws one mechanism from our systems atlas as the atlas records it, and shows what a reader "
                     "can take from it."},
        ],
        "rules": rules,
        "plate_css": plate_css(book.files),
        "extras": [],
        "related_chapters": [
            {"chapter": "10", "reason": "Rule 10.10, the atlas’s encoding glyphs and their measurements."},
            {"chapter": "11", "reason": "Rule 11.14’s plate, where the loop stepper of Rule 18.22 runs Loop R1 live."},
            {"chapter": "12", "reason": "Rule 12.5, the red target where a reform acts, and Rule 12.8, the stacked layers."},
            {"chapter": "13", "reason": "The grade words, the line code, delay, typed chips and dates every drawing here keeps."},
            {"chapter": "14", "reason": "Charts, where widths and areas carry measured amounts."},
            {"chapter": "18", "reason": "Rule 18.22, the loop stepper as a component, and Rule 18.24, the typed ID chip."},
        ],
        "sources": [
            (f"Source: {ATLAS}, the records each rule names (variables, connections, loops, the layers, the rejected "
             f"connections, the model’s conventions, boundary and limits, and the glossary), snapshot of {SNAP}, United States. "
             "Retrieved November 12, 2026. Facts the atlas rechecked carry their own check dates; inclusion in the snapshot "
             "alone does not mean a fact was rechecked on that date."),
        ],
    }
    return data


# ===============================================================================================================
# Checks
# ===============================================================================================================
def curly(o, skip=("specimen", "id", "before_rule", "chapter", "related", "token", "tokens", "anchor", "plate_css")):
    """Atlas titles carry straight apostrophes; the chapter prints curly ones (chapter 06), as e() does in the plates."""
    if isinstance(o, str):
        return o.replace("'", "’")
    if isinstance(o, list):
        return [curly(x) for x in o]
    if isinstance(o, dict):
        return {k: (v if k in skip else curly(v)) for k, v in o.items()}
    return o


def check(data, book):
    fails = []
    texts = {"chapter": " ".join(C13.strings({k: v for k, v in data.items() if k not in ("sources", "plate_css")}))}
    for sid, frag in book.files.items():
        texts[sid] = C13.visible(frag)
        texts[sid + " alt"] = book.manifest[sid]["alt"]
    allt = " ".join(texts.values())
    for k, t in texts.items():
        if "—" in t or "‑" in t:
            fails.append(f"em dash or U+2011 in {k}")
        for w in C13.FILLERS:
            for m in re.finditer(rf"\b{w}\b", t, re.I):
                fails.append(f"listed word {w!r} in {k}: …{t[max(0, m.start() - 50): m.end() + 30]}…")
        for m in re.finditer(C13.STUDIO, t):
            fails.append(f"studio word or code {m.group(0)!r} in {k}")
        if re.search(r"\bnot only\b|\bnot just\b", t):
            fails.append(f"a corrective-negation shape in {k}")
        for m in re.finditer(r"\bRules? (15\.\d+)", t):
            if m.group(1) not in BUILT:
                fails.append(f"{k} cites Rule {m.group(1)}, which this round does not build")
    for name, line in C13.LOCKED.items():
        head = line[: max(18, len(line) // 2)]
        for m in re.finditer(re.escape(head), allt):
            if allt[m.start(): m.start() + len(line)] != line:
                fails.append(f"near miss of the {name}")
    for r in data["rules"]:
        rid = r["id"]
        n = len(re.sub(r"[“”.,]", "", r["title"]).split())
        if n > 15:
            fails.append(f"Rule {rid}: title runs {n} words")
        if not r["failure"]["caption"].startswith(f"<strong>Fails Rule {rid}.</strong> "):
            fails.append(f"Rule {rid}: failure caption without its lead")
        fsid = r["failure"]["specimen"]
        if 'class="dnp"' not in book.files[fsid]:
            fails.append(f"{fsid}: no do-not-publish band")
        if not book.manifest[fsid]["alt"].startswith("Failure case: do not publish."):
            fails.append(f"{fsid}: alt does not open with the band's words")
        for k in ("rule", "why", "correct", "failure", "builders", "related", "specs"):
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
        if re.search(r'class="sv"[^>]*viewBox="0 0 (\d+)', frag) and any(int(w_) > W for w_ in re.findall(r'class="sv" viewBox="0 0 (\d+)', frag)):
            fails.append(f"{sid}: a drawing wider than the {W} px artboard")
    for sid, m_ in book.manifest.items():
        if m_["width_px"] != STAGE:
            fails.append(f"{sid}: a stage of {m_['width_px']} px, where every plate is {STAGE} px")
        if m_.get("wide_px") not in (None, WIDE) or m_.get("frame_container") is not True:
            fails.append(f"{sid}: its frame must be the query container, and a wide stage is {WIDE} px")
        if bool(m_.get("wide_px")) != ('class="p wd"' in book.files[sid]):
            fails.append(f"{sid}: its manifest and its markup disagree on the wide composition")
        frag = book.files[sid]
        if "<style" in frag:
            fails.append(f"{sid}: a style of its own; the chapter's block holds every plate rule (D3-480)")
    # D3-480: every plate that has words or a second drawing to set beside its drawing takes the wide stage, and the
    # plates that hold one drawing alone keep one true size
    wide = sorted(k for k, m_ in book.manifest.items() if m_.get("wide_px"))
    want = sorted([data["opener"]["specimen"]] + [r["correct"]["specimen"] for r in data["rules"]]
                  + ["s-15-3-failure", "s-15-4-failure"])
    if wide != want:
        fails.append(f"the wide plates are {wide}, where D3-480 wants {want}")
    css = data["plate_css"]
    if re.search(r"@media\b", css):
        fails.append("plate_css: a media query; the plates compose by their frame's container only (D3-480)")
    for m in re.finditer(r"@container\s+(\S+)", css):
        if m.group(1) != "oa-frame":
            fails.append(f"plate_css: a container query on {m.group(1)}, where the shell's container is oa-frame")
    if "—" in css or "‑" in css:
        fails.append("plate_css: an em dash or U+2011")
    bare_css = re.sub(r"var\((?:[^()]|\([^()]*\))*\)", "", css)
    if re.search(r"(?<![\w&])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![\w-])|\brgba?\(|\bhsla?\(", bare_css):
        fails.append("plate_css: a literal color")
    for px in re.findall(r"font(?:-size)?:[^;}\"]*?\b(\d+(?:\.\d+)?)px", css):
        fails.append(f"plate_css: a font size in px ({px}) outside the tokens")
    op = book.files[data["opener"]["specimen"]]
    if len(op.encode()) > 12 * 1024:
        fails.append(f"the opener's fragment weighs {len(op.encode()):,} bytes; it must stay well under 16 KB as placed")
    kinds = {"Variable": NODE, "Connection": LINK, "Loop": LOOP, "Reform": REFORM,
             "Route": {r["code"] for r in V7["routes"]["items"]}}
    for sid, frag in book.files.items():
        for kind, rid in re.findall(r'<span class="chip">([A-Za-z ]+) <span class="id">([^<]+)</span>', frag):
            if rid not in kinds.get(kind, {}):
                fails.append(f"{sid}: {kind} {rid} is not in the atlas")
    # the model's own consistency, which every rule here leans on
    for k, p in LOOP.items():
        if p["links"] and ("R" if minus_count(p["links"]) % 2 == 0 else "B") != p["type"]:
            fails.append(f"Loop {k}: its kind disagrees with its count of minus signs")
        for lid in p["links"]:
            if link(lid)["type"] == "authority":
                fails.append(f"Loop {k} lists authority connection {lid}")
    # Rule 01.9 over the chapter's example log
    ex = [x for x in book.examples if x["domain"] not in ("all", "invented")]
    dom = Counter(x["domain"] for x in ex)
    st = Counter(s for x in book.examples for s in x["states"])
    for d, n in dom.items():
        if n * 4 > len(ex):
            fails.append(f"Rule 01.9: domain {d} supplies {n} of {len(ex)} examples, over one in four")
    for s_, n in st.items():
        if n * 5 > len(book.examples):
            fails.append(f"Rule 01.9: state {s_} supplies {n} of {len(book.examples)} examples, over one in five")
    return fails, dom


def write(data, book):
    SPECIMENS.mkdir(parents=True, exist_ok=True)
    for old in SPECIMENS.glob("s-15-*.html"):
        if old.stem not in book.files:
            old.unlink()
    for sid, txt in book.files.items():
        (SPECIMENS / f"{sid}.html").write_text(txt)
    (SPECIMENS / f"manifest-{MAKER}.json").write_text(json.dumps(book.manifest, indent=1, ensure_ascii=False) + "\n")
    p = CHAPTERS / "15-systems-graphics.json"
    p.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    return p


def main():
    book = Book()
    data = curly(chapter(book))
    fails, dom = check(data, book)
    frag = sum(len(x.encode()) for x in book.files.values())
    js = len(json.dumps(data, indent=1, ensure_ascii=False).encode())
    print(f"chapter 15: {len(data['rules'])} rules, {len(book.files)} plates, {frag:,} bytes of fragments, {js:,} bytes of chapter file")
    print("examples by domain:", dict(sorted(dom.items())), "| all examples:", len(book.examples))
    for sid, f_ in sorted(book.files.items(), key=lambda x: -len(x[1].encode()))[:6]:
        print(f"  {sid}: {len(f_.encode()):,} bytes")
    if fails:
        print("\n".join("FAIL " + f for f in fails))
        raise SystemExit(1)
    if "--check-only" not in sys.argv:
        p = write(data, book)
        print(f"wrote {p.relative_to(ROOT)}, {len(book.files)} specimens and manifest-{MAKER}.json")


if __name__ == "__main__":
    main()
