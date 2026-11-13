"""Write chapter 15, Systems graphics: its words, its plates and its manifest.

Oath & Action Edition 06, Phase 3, rounds 1 and 2. Systems designer, November 12, 2026. The briefs are
work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md and 20261112_Phase-3-Round-2-Brief.md (systems designer); the
rule list the main session fixed (R7) is in work/handoffs/phase-3/20261112_Round-1-Systems-Designer-Notes.md, section
"Rule list". Round 1 built the grammar, Rules 15.1 to 15.10, and worked examples 1 and 2, Rules 15.13 (Loop R1) and
15.14 (Loop R8), with the opener. Round 2 (DR-244) builds the reforms on the drawing, Rules 15.11 and 15.12, and worked
examples 3 to 6, Rules 15.15 to 15.18. Round 4 (November 13, 2026; work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md)
gives every variable its own title in every drawing (DR-265) and builds group 4, Interaction: Rules 15.19 (the loop
stepper on Rule 18.22's code), 15.20 (the reform chooser on Rules 18.3 and 18.8) and 15.21 (no control for a strength).
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
against the 0.60 MB it reports (DR-271: a reported figure, not a stop).
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
         "15.14", "15.15", "15.16", "15.17", "15.18", "15.19", "15.20", "15.21"]
PLANNED = {"15.22": "Draw a route to change as its whole workflow, through to reversal.",
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


DR265_TITLES = {NODE[c]["title"] for c, lab in LOOP_NAME.items() if lab != NODE[c]["title"]}


def short(code):
    """A variable's name on every plate and in every line of the chapter: its own title (nodes[].title), never the
    chain label a loop's record gives it (DR-265, November 13, 2026). LOOP_NAME stays only for the check that no chain
    label prints (check(), DR-265)."""
    return node(code)["title"]


# The data lead's RF-16 and RF-16a (BC S4, D3-893) gave these four core variables their own titles outside a loop; DR-265
# (November 13, 2026) gives every variable its own title in every drawing, a loop's included, so TWO_NAMES stays only to
# hold the atlas's two names for them, which the V7.1 list asks the atlas to make one.
TWO_NAMES = {"D1", "D2", "D4", "D6"}
need(all(LOOP_NAME.get(c) and LOOP_NAME[c] != node(c)["title"] for c in TWO_NAMES), "the atlas no longer names D1, D2, D4 and D6 two ways")


def own(code):
    """A variable's label in a drawing outside any loop: its own title (RF-16, then DR-265 for every variable)."""
    return node(code)["title"] if code in TWO_NAMES else short(code)


def tie(s):
    """Hold a label's last two words on one line, so no word stands alone at the end of it (BC S16)."""
    head, _, last = s.rpartition(" ")
    return f"{head} {last}" if head else s


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
    """A connection's typed chip with its grade word, the record square before Documented (Rule 13.4, SD-1), held on one
    line: a no-break space alone does not hold across the chip's inline box (round 2)."""
    return f'<span class="nw2">{chip("Connection", lid)}&#160;{grade_word(link(lid)["evidence"], gloss=False)}</span>'


def vt(code):
    """A variable's typed chip with its title in quotation marks, as a connection's chip takes its name. Words follow a
    chip and punctuation never touches it, since the chip's padding and edge would set a comma or a period apart (BC S16)."""
    return f'{chip("Variable", code)} “{e(node(code)["title"])}”'


def step_lines(lids, skip=(), head="Each step", extra=None):
    """A loop's steps, numbered in the atlas's order, each connection's chip with its grade word (Rule 13.4, the data
    lead's SD-7): every connection a drawing shows prints its grade somewhere on the plate. A step with words added after
    its grade ends the grade word with a period first (CD CH15-S1)."""
    ex = extra or {}
    rows = [f'<p class="nt"><b>{i}</b>&#160;{gl(x)}{"." + ex[x] if x in ex else ""}</p>'
            for i, x in enumerate(lids, 1) if x not in skip]
    return f'<p class="k">{e(head)}</p>' + "".join(rows) if rows else ""


def ticks_line(lids):
    """What a line's ticks count, for the delay classes the drawn connections hold, in the words Rule 15.13's key uses
    (the atlas's glossary for a delay and chapter 13's classes, Rule 13.5)."""
    dg = GLOSS["Delay"].split(".")[0]
    need(dg == "The time between a change and its effect", "the atlas's definition of a delay changed")
    held = [k for k in ("S", "M", "L") if any(link(x)["delay"] == k for x in lids)]
    need(held, "a key for ticks on a drawing whose connections hold no delay")
    cls = [f"{words_n(DELAY[k][0])} for {DELAY[k][1]}" for k in held]
    lst = cls[0] if len(cls) == 1 else ", ".join(cls[:-1]) + " and " + cls[-1]
    return f"{e(dg[0].lower() + dg[1:])}: {lst} (Rule 13.5)"


def reading_key(lids, layers=None):
    """A short key for a plate a reader may reach by a link (AX S10): the step words the drawn connections print, the
    ticks their delays draw, and the layers a boundary names. Every word comes from the connections' own records."""
    words = []
    for x in lids:
        w_ = " ".join(step_words(0, x))
        if w_ not in words:
            words.append(w_)
    verbs = {BS.verb(link(x)["polarity"]) for x in lids}
    typed = all(link(x)["type"] in ("money", "information", "ownership") for x in lids)
    need(typed and verbs <= {"raises", "lowers"}, "the key's step words cover typed, signed connections only")
    ways = {"lowers": "the opposite way for lowers", "raises": "the same way for raises"}
    names = " and ".join(f"<b>{e(w_)}</b>" for w_ in words)
    items = [f"{names}: the first word says what moves along the connection (Rule 15.4), and the second which way the next "
             f"variable moves, {' and '.join(ways[v] for v in ('lowers', 'raises') if v in verbs)} (Rule 15.3).",
             f"<b>Ticks</b> near a line’s start count its delay, {ticks_line(lids)}."]
    if layers:
        need(len(V7["layers"]) == 3, "the atlas's model no longer holds three layers")
        items.append(f"<b>{e(layers[0])}</b> and <b>{e(layers[1])}</b> name two of the three layers our systems atlas divides "
                     "its model into, and the rule between them marks where the chain crosses (Rule 15.9).")
    return kw(items)


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
LOOP_HI = 140             # DR-265: a loop's pill may widen to 140 px where that saves a row of its title; two side by
TOP_HI = 170              # side still leave 12 px between them, and a three-variable loop's top pill, alone in its row,
                          # may take 170
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


def pill_w(label, pw=PW, hi=None):
    """A pill's width: the base, or wide enough for the label's longest word with PAD at each end. With hi, the pill may
    widen up to hi where that saves a row, and takes the narrowest width that holds the fewest rows (DR-265: a title
    runs longer than the chain label it replaces)."""
    base = max(pw, math.ceil(max(tw(w_, 600) for w_ in label.split()) + 2 * PAD + 2))
    if not hi or hi <= base:
        return base
    fewest = len(wrap(label, hi - 2 * PAD))
    return next(w_ for w_ in range(base, hi + 1) if len(wrap(label, w_ - 2 * PAD)) == fewest)


ROW_ROOM = W - 4 - 12      # two pills side by side in one row: 2 px from each edge and 12 px between them
ROW_ROOM3 = W - 4 - 6      # a three-variable loop's lower row, where nothing runs between its two pills
MAX_ROWS = 3               # the data lead's ruling (e): a title wraps onto three rows at most in a pill that can grow
STACK_HI = 250             # a two-variable loop drawn one pill above the other: its pills' widest


def _rows_n(label, w_):
    k = (label, w_)
    if k not in _ROWS_N:
        _ROWS_N[k] = len(wrap(label, w_ - 2 * PAD))
    return _ROWS_N[k]


_ROWS_N = {}


def pair_w(la, lb, lo=PW, room=ROW_ROOM):
    """Two pills that share a row (a two-variable loop, a row of a four- or three-variable one): the widths that set both
    titles in the fewest rows, then the fewest rows in all, then the narrowest, inside room together (DR-265). Each pill
    keeps the 130 px base where that still holds both titles in three rows or fewer, the data lead's ruling (e), and may
    narrow to its longest word where it does not."""
    best = None
    for lo_ in (lo, 0):
        ba, bb = pill_w(la, lo_), pill_w(lb, lo_)
        best = None
        for wa in range(ba, room - bb + 1):
            for wb in range(bb, room - wa + 1):
                ra, rb = _rows_n(la, wa), _rows_n(lb, wb)
                if not (pill_shape(wa, ra) and pill_shape(wb, rb)):
                    continue
                k = (max(ra, rb), ra + rb, wa + wb, abs(wa - wb))
                if best is None or k < best[0]:
                    best = (k, wa, wb)
        if best and best[0][0] <= MAX_ROWS:
            break
    if best is None:            # no pair of pill shapes fits the row: the caller re-lays the drawing (ruling (e), step 2)
        return pill_w(la), pill_w(lb), 99
    return best[1], best[2], best[0][0]


def pill_shape(w_, rows):
    """A pill stays a pill: at least half again as wide as it is tall, so a short title on three rows never draws a disc."""
    return w_ >= 1.5 * max(rows * LH + 22, 44)


def stack_w(labels, scale=None):
    """One width for the pills of a loop drawn one above the other: the narrowest that sets every title in its fewest rows
    up to STACK_HI, two rows where that fits; scale widens a failure plate's pill on purpose."""
    w_ = max(next(x for x in range(pill_w(lb, PW), STACK_HI + 1) if _rows_n(lb, x) == min(_rows_n(lb, STACK_HI), MAX_ROWS)
                  or x == STACK_HI) for lb in labels)
    return [min(W - 4, round(w_ * sc)) for sc in (scale or [1] * len(labels))]


def rows_of(label, width):
    """A label's rows at a width: as many as the greedy wrap takes, set as evenly as the words allow, so no short word
    stands alone on a row of its own while the row above runs full (DR-265's longer titles)."""
    rows = wrap(label, width)
    if len(rows) < 2:
        return rows
    words = label.split()
    runs = sorted({tw(" ".join(words[i:j]), 600) for i in range(len(words)) for j in range(i + 1, len(words) + 1)})
    for c in runs:
        if c > width:
            break
        r = wrap(label, c + 0.01)
        if len(r) == len(rows):
            return r
    return rows


class Pill:
    """A variable as a pill with its own title inside (System 1's station_block, DR-36), or a thin pill for a station
    that is no numbered variable (a conceptual loop's)."""

    def __init__(self, label, cx, cy, pw=PW, thin=False, cls="", red=False, shared=False):
        pw = pill_w(label, pw)
        self.rows = rows_of(label, pw - 2 * PAD)
        need(len(self.rows) <= MAX_ROWS or label not in DR265_TITLES,
             f"the title {label!r} takes {len(self.rows)} rows in a {pw:.0f} px pill; ruling (e) holds a pill to {MAX_ROWS}")
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
    wa, wb, most = pair_w(*labels)
    if most > MAX_ROWS:
        return stacked_loop(codes, lids, labels, numbered, weakest, inside, thin, grades, widths, hollow, scale, top,
                            targets, shared)
    pw = [wa, wb] if not scale else [pill_w(lb, PW * sc) for lb, sc in zip(labels, scale)]
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


def stacked_loop(codes, lids, labels, numbered, weakest, inside, thin, grades, widths, hollow, scale, top, targets, shared):
    """A loop of two variables whose titles cannot share one row in three rows each (the data lead's ruling (e), step 2:
    re-lay the drawing): one pill above the other at one width, step 1 straight down the right and step 2 straight up the
    left, each on both pills' flat edges, its words outside the loop and the loop's ID between them above the tags, as a
    four-variable loop draws its side steps. Returns (body, h, pills)."""
    sw = stack_w(labels, scale)
    hs = [max(len(wrap(lb, w_ - 2 * PAD)) * LH + 22, 44) for lb, w_ in zip(labels, sw)]
    kw_ = [dict(red=c in targets, shared=c in shared) for c in codes]
    a = Pill(labels[0], W / 2, top + 2 + hs[0] / 2, sw[0], thin, **kw_[0])
    b = Pill(labels[1], W / 2, a.bot + GAP4 + hs[1] / 2, sw[1], thin, **kw_[1])
    lo_, hi_ = max(a.left + a.h / 2, b.left + b.h / 2), min(a.right - a.h / 2, b.right - b.h / 2)

    def span(i):
        lid = lids[i]
        if not lid:
            return 0
        ws = step_words(i + 1 if numbered else 0, lid, ("weakest step",) if weakest == i else ())
        return max(tw(w_, 600 if re.match(r"\d+ ", w_) else 400) for w_ in ws) + (3 if lid in targets else 0)
    # each step on both pills' flat edges, pulled in from the ends where its words need the room outside it
    xr = min(hi_ - INNER, W - 2 - 15 - span(0))
    xl = max(lo_ + INNER, 2 + 15 + span(1))
    need(lo_ <= xl and xr <= hi_, "a stacked loop's steps miss their pills' flat edges")
    need(xr - xl >= 80, "a stacked loop's two steps sit too close for its ID between them")
    paths = [([(xr, a.bot + 2), (xr, b.top - 2)], "right"), ([(xl, b.top - 2), (xl, a.bot + 2)], "left")]
    out, tag_tops = [], []
    for i, ((pts, side), lid) in enumerate(zip(paths, lids)):
        l = link(lid) if lid else {"polarity": None, "evidence": None, "delay": None}
        g = (grades or {}).get(i, l["evidence"])
        w = (widths or {}).get(i, LW)
        tg = bool(lid) and lid in targets
        m, _ = conn(pts, g, l["polarity"], l["delay"], hollow=hollow, w=w, target=tg)
        out.append(wr(m, tg))
        if lid:
            extra = ("weakest step",) if weakest == i else ()
            words = step_words(i + 1 if numbered else 0, lid, extra)
            out.append(verb_at(pts, l["polarity"], words, side, big=tg))
            x, ty, _, _ = anchor_at(pts, l["polarity"])
            tag_tops.append(ty - (TAG_HALF + 3 if tg else TAG_HALF) - (len(words) - 1) * LH / 2)
            span = max(tw(w_, 600 if re.match(r"\d+ ", w_) else 400) for w_ in words) + (3 if tg else 0)
            need((x - 15 - span >= 2) if side == "left" else (x + 15 + span <= W - 2),
                 f"step {i + 1}'s words of a stacked loop leave the {W} px artboard")
    out.append(a.svg() + b.svg())
    if inside:
        ceil_, floor_ = a.bot, min(tag_tops)
        y = (ceil_ + floor_ - ID_DOWN + ID_UP) / 2
        need(y - ID_UP >= ceil_ + 4 and y + ID_DOWN <= floor_ - 4,
             f"a stacked loop's ID has no room above its steps' tags ({floor_ - ceil_:.0f} px)")
        need(max(tw(f"Loop {inside[0]}", 700), tw(inside[1])) <= xr - xl - 24, "a stacked loop's ID crowds its steps")
        out.append(loop_id((xl + xr) / 2, y, *inside, two=True))
    return "".join(out), b.bot + 4, (a, b)


def three_loop(codes, lids, numbered=True, weakest=None, grades=None, inside=None, hollow=False, labels=None, thin=False,
               targets=(), shared=(), top=0, steps_g=False, lit=(), for_=None, only=None):
    """A loop of three variables: the first centered at the top, the second below it to the right and the third to the
    left. Steps 1 and 3 run straight between overlapping pills; step 2 arches under the bottom row. targets and shared
    as two_loop takes them. Round 4: steps_g wraps each step (its band, marks and words) in data-s and each pill in
    data-p, so Rule 15.19's plate can light the current step from the stepper's data-oa-at; lit draws a connection with
    Rule 12.5's red marks ready though not shown (the red shows for those in targets), and for_ names the reforms each
    target belongs to (data-oa-for), so Rule 15.20's plate lights the chosen reform's; only draws those steps alone (a
    failure plate's). Returns (body, h)."""
    labels = labels or [short(c) for c in codes]
    w3, w2, _ = pair_w(labels[2], labels[1], room=ROW_ROOM3)
    pw = [pill_w(labels[0], PW, TOP_HI), w2, w3]
    hs = [max(len(wrap(lb, p - 2 * PAD)) * LH + 22, 44) for lb, p in zip(labels, pw)]
    y1 = top + 4 + hs[0] / 2
    gap = 108
    y2 = y1 + hs[0] / 2 + gap + max(hs[1], hs[2]) / 2
    kw_ = [dict(red=c in targets, shared=c in shared) for c in codes]
    p1 = Pill(labels[0], W / 2, y1, pw[0], thin, **kw_[0])
    p2 = Pill(labels[1], W - 2 - pw[1] / 2, y2, pw[1], thin, **kw_[1])
    p3 = Pill(labels[2], 2 + pw[2] / 2, y2, pw[2], thin, **kw_[2])
    def mid(p, q):
        """An upright step's place: the middle of the two pills' shared flat edge, or of their overlap where the flat
        edges share none (DR-265's wider pills)."""
        lo_, hi_ = max(p.left + p.h / 2, q.left + q.h / 2), min(p.right - p.h / 2, q.right - q.h / 2)
        if hi_ - lo_ >= 8:
            return (lo_ + hi_) / 2
        return (max(p.left, q.left) + min(p.right, q.right)) / 2
    xr, xl = mid(p1, p2), mid(p1, p3)
    # the loop's ID sits on one line under the lower row, between the lower arch's two upright ends with 12 px to spare
    # each side; where DR-265's wider pills bring those ends too close, it takes two rows and the arch drops 18 px more
    two_rows = bool(inside) and (tw(f"Loop {inside[0]} ", 700) + tw(inside[1]) > p2.cx - p3.cx - 24)
    id_x = (p2.cx + p3.cx) / 2      # the ID's middle: the lower arch's middle, so 12 px stay clear at each upright end
    bot_y = max(p2.bot, p3.bot) + RISE + (LH if two_rows else 0)
    paths = [([(xr, p1.bot + 2), (xr, p2.top - 2)], "right"),
             ([(p2.cx, p2.bot + 2), (p2.cx, bot_y), (p3.cx, bot_y), (p3.cx, p3.bot + 2)], "below"),
             ([(xl, p3.top - 2), (xl, p1.bot + 2)], "left")]
    out = []
    fa = lambda k: f' data-oa-for="{for_[k]}"' if for_ and k in for_ else ""
    for i, ((pts, side), lid) in enumerate(zip(paths, lids)):
        if only is not None and i not in only:
            continue
        l = link(lid) if lid else {"polarity": None, "evidence": None, "delay": None}
        g = (grades or {}).get(i, l["evidence"])
        tg = bool(lid) and lid in targets
        lt = tg or (bool(lid) and lid in lit)
        m, _ = conn(pts, g, l["polarity"], l["delay"], hollow=hollow, target=lt)
        part = (wr(m, tg) if not lt or tg else f'<g class="wr"{RED}>{m}</g>')
        if fa(lid):
            part = part.replace("<g ", f"<g{fa(lid)} ", 1)
        if lid:
            extra = ("weakest step",) if weakest == i else ()
            part += verb_at(pts, l["polarity"], step_words(i + 1 if numbered else 0, lid, extra), side, big=lt)
        if steps_g:
            part = f'<g data-s="{i + 1}"><path class="bd" d="{BS.rounded_d(pts, BEND)}"/>{part}</g>'
        out.append(part)
    for j, p_ in enumerate((p1, p2, p3)):
        out.append(f'<g data-p="{j}"{fa(codes[j])}>{p_.svg()}</g>' if steps_g or fa(codes[j]) else p_.svg())
    if inside and two_rows:
        need(max(tw(f"Loop {inside[0]}", 700), tw(inside[1])) <= p2.cx - p3.cx - 24, "the loop's ID crowds its lower arch")
        out.append(loop_id(id_x, max(p2.bot, p3.bot) + 28, *inside, two=True))
    elif inside:
        out.append(loop_id(id_x, max(p2.bot, p3.bot) + 28, *inside))
    n2 = len(step_words(2, lids[1], ("weakest step",) if weakest == 1 else ())) if lids[1] else 1
    h = bot_y + 34 + (n2 - 1) * LH
    return "".join(out), h


GAP4 = 112                # the rise between a four-variable loop's two rows: the tick, the tag and the arrowhead
INNER = 8                 # a side step's line stands 8 px in from where the pill's rounded end meets its flat edge
TAG_HALF = 8              # half a sign tag's height at 2 px (16 px tall; a red target's 6 px tag is 22, so 3 more)
ID_UP, ID_DOWN = 17, 16   # a two-row loop ID's ink above and below its middle: 15 px type, rows 18 px apart at -6 and +12


def four_loop(codes, lids, numbered=True, inside=None, inside_rows=None, targets=(), shared=(), labels=None):
    """A loop of four variables on a square, clockwise from the top left: step 1 arches over the top and step 3 under
    the bottom, as two_loop draws a two-variable loop; steps 2 and 4 run straight down the right and up the left, each on
    its pills' flat edges near their inner ends, with its words outside the loop, so the loop's ID sits clear between
    them. inside is (loop ID, kind); inside_rows sets words of a failure plate's own on two rows; targets and shared as
    two_loop takes them; labels overrides the titles (a failure plate's own words). Returns (body, h)."""
    labels = labels or [short(c) for c in codes]
    (w0, w1, _), (w3, w2, _) = pair_w(labels[0], labels[1]), pair_w(labels[3], labels[2])
    pw = [w0, w1, w2, w3]
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
    out, tag_tops = [], []
    for i, ((pts, side), lid) in enumerate(zip(paths, lids)):
        l = link(lid)
        tg = lid in targets
        m, _ = conn(pts, l["evidence"], l["polarity"], l["delay"], target=tg)
        out.append(wr(m, tg))
        words = step_words(i + 1 if numbered else 0, lid)
        out.append(verb_at(pts, l["polarity"], words, side, big=tg))
        if side in ("left", "right"):
            x, ty, _, _ = anchor_at(pts, l["polarity"])
            tag_tops.append(ty - (TAG_HALF + 3 if tg else TAG_HALF))
            span = max(tw(w_, 600 if re.match(r"\d+ ", w_) else 400) for w_ in words) + (3 if tg else 0)
            need((x - 15 - span >= 2) if side == "left" else (x + 15 + span <= W - 2),
                 f"step {i + 1}'s words of a four-variable loop leave the {W} px artboard")
    out.append(a.svg() + b.svg() + c.svg() + d.svg())
    mid_x = (xl + xr) / 2
    room = xr - xl - 2 * 12
    # BC S16: the loop's two rows sit above the side steps' tags, centered in the room between the top row's pills and
    # the higher tag, so neither row reads on one line with a side step's words and tag ("4 raises + Loop R10"). y is
    # the block's middle; its rows' baselines fall 6 px above it and 12 px below it, and its ink runs from ID_UP above to
    # ID_DOWN below
    ceil_, floor_ = max(a.bot, b.bot), min(tag_tops)
    y = (ceil_ + floor_ - ID_DOWN + ID_UP) / 2
    if inside or inside_rows:
        need(y - ID_UP >= ceil_ + 4 and y + ID_DOWN <= floor_ - 4,
             f"the loop's ID has no room above its side steps' tags ({floor_ - ceil_:.0f} px)")
    if inside:
        lid_, kind = inside
        need(max(tw(f"Loop {lid_}", 700), tw(kind)) <= room, "the loop's ID crowds its side steps")
        out.append(loop_id(mid_x, y, lid_, kind, two=True))
    if inside_rows:
        need(max(tw(r_, 700) for r_ in inside_rows) <= room, "the words inside the loop crowd its side steps")
        out.append(f'<text class="id" x="{F(mid_x)}" y="{F(y - 6)}" text-anchor="middle">{e(inside_rows[0])}'
                   f'<tspan x="{F(mid_x)}" dy="{LH}">{e(inside_rows[1])}</tspan></text>')
    h = bot_y + 34 + (rows[2] - 1) * LH
    return "".join(out), h


def read_aloud(codes, lids, closes=True):
    """More or less at each variable, carrying the signs along the chain from a rise at the first (System 1's
    read_aloud, from the atlas's signs)."""
    up, parts = True, []

    def more(name, up_):
        # a title that asks how often ("How often the primary decides the winner") reads "the primary decides the winner
        # more often"; every other title takes more or less before it
        if name.startswith("how often "):
            return name[len("how often "):] + (" more often" if up_ else " less often")
        return ("more " if up_ else "less ") + name
    for i, code in enumerate(codes):
        name = lc(short(code))
        parts.append(more(name, up))
        if i < len(lids) and link(lids[i])["polarity"] == "-":
            up = not up
    line = ", ".join(parts)
    if closes:
        line += ", and back to " + more(lc(short(codes[0])), up)
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
        ".p *{box-sizing:border-box}:where(.p) :where(p){margin:0}"
        ".p :is(.gr,.nt,.ra,.q,.src,li){text-wrap:pretty}")      # no word left alone at the end of a line (BC S16)
LAYOUT = (".fx{display:grid;grid-template-columns:minmax(0,1fr);gap:12px}.fx.pr{gap:24px}.fx.tri{gap:0}.fx>div{min-width:0}"
          ".fx>div>:first-child{margin-top:0}.fx>div>*+.k{margin-top:16px}"
          "@container oa-frame (min-width:680px){.p.wd{padding:24px}"
          f".wd .fx{{grid-template-columns:{W}px minmax(0,1fr);column-gap:{GAP_A}px}}"
          f".wd .fx.pr{{grid-template-columns:{W}px {W}px;column-gap:{GAP_PR}px}}"
          f".wd .fx.tri{{grid-template-columns:repeat(3,minmax(0,1fr));column-gap:{GAP_TRI}px}}"
          ".wd .tri>.vc{margin:0;padding:0;border:0}"
          f".wd .two{{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:{GAP_PR}px}}"
          ".wd .fx.g3>:nth-child(1){grid-column:1;grid-row:1}.wd .fx.g3>:nth-child(2){grid-column:2;grid-row:1/span 2}"
          ".wd .fx.g3>:nth-child(3){grid-column:1;grid-row:2}}}"
          "@container oa-frame (max-width:327.98px){.p :is(p,ul,ol,.evr,.oa-stepper-controls,fieldset,.oa-choice-item,details)"
          ":not(.dnp){max-width:calc(100cqi - 32px)}}")
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
           ".ef>li>p{margin-top:2px}"),
    "gp": (".gp+.gp{margin-top:16px;padding-top:14px;border-top:1px solid var(--oa-color-border-hairline)}"
           ".gp .evr{margin-bottom:6px}"),
    "two": ".two{display:grid;grid-template-columns:minmax(0,1fr);gap:20px;margin-top:20px}.two.tw{gap:12px;margin-top:0}"
           ".two.tw>p{margin:0}",
    "kd2": (".kd2{display:grid;grid-template-columns:64px minmax(0,1fr);column-gap:12px;font:var(--oa-type-body-small)}"
            ".kd2 .sv{margin-top:4px}.kd2 b{font-weight:var(--oa-font-weight-semibold)}.kd2+.kd2{margin-top:8px}"),
    # a row of typed chips, a list with no punctuation to touch a chip's edge (BC S16)
    "cr": ".cr{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px 8px}",
})


CSS["nt"] = CSS["nt"] + ".nt+.nt{margin-top:4px}"
CSS["hed"] = CSS["hed"] + ".p>.hed+.evr{margin-top:12px}"     # a reform's chip and title at the head of its plate (round 2)


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
        self.files, self.manifest, self.examples, self.keys = {}, {}, [], {}

    def add(self, sid, body, *, rule, alt, illustrative=False, readable=False, notes="", wide=False, interactive=False):
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
        if interactive:               # round 4: a live plate, a group the shell names, never an image (AX section 1)
            m["interactive"] = True
        if sid in self.keys:          # round 4: its keyboard path, walked by the guide check from <sid>.keys.json
            m["keys"] = True
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
    # C marks the loop's number and kind, so it sits just left of "Loop R13" (DR-265's wider pills leave no room between
    # the two pills, where it stood before)
    run_y = a.top - RISE
    need(xa < W / 2 - tw(f"Loop {lid}", 700) / 2 - 24, "the opener's letter C crowds the authority line")
    nums = (numeral(1, a.left + 6, a.top - 1) + numeral(2, W / 2 + 46, 15)
            + numeral(3, W / 2 - tw(f"Loop {lid}", 700) / 2 - 17, run_y + 22 - 5)
            + numeral(4, xa - 20, a.bot + 30) + numeral(5, W / 2 - 4, fy) + numeral(6, W / 2 + 64, run2 + 20))
    total = ec.bot + 4
    svg = svg_wrap(body + f'<g class="wr">{m}</g>' + lab + fr + ec.svg() + nums, total)
    parts = [("A variable, by its own title", "15.2"), ("A sign tag and the word for which way", "15.3"),
             ("The loop’s number and kind", "15.6"), ("Authority, with no sign", "15.5"),
             ("A boundary between layers", "15.9"), ("A dashed line for a plausible step", "13.4")]
    lst = "".join(f"<li>{C13.mk(LETTERS[n - 1])} {e(w)}, Rule {r}</li>" for n, (w, r) in enumerate(parts, 1))
    steps = "".join(f'<p class="nt">{gl(x)}</p>' for x in (*lp["links"], "LE02"))
    body = (label_for(lp["links"], "the grade of the loop’s least certain step")
            + beside(hed("Loop", lid, lp["title"]) + fig(svg),
                     f'{steps}<p class="k">What each lettered part says</p><ol class="kw hg">{lst}</ol>'
                     + src("loop R13 and connections L11, L12 and LE02")))
    book.add("s-15-opener", body, rule=None, readable=True, wide=True,
             alt=(f"Loop R13 from our systems atlas, “{lp['title']}”, drawn as two pills, {short('D1')} and "
                  f"{lc(short('D2'))}, with an arrow over the top marked minus, lowers, and one under the bottom marked minus, lowers, "
                  "drawn dashed. The loop’s name and the word reinforcing sit inside it. A line with an open diamond and the word "
                  f"decides runs from {lc(short('D1'))} down across a rule into the economy layer, to Public investment in "
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
    la, lb = labels or (own(a_code), own(b_code))
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
    la, lb = own(a_code), own(b_code)
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
        two_rows = bool(inside) and (tw(f"Loop {inside[0]} ", 700) + tw(inside[1]) > p2.cx - p3.cx - 24)
        if two_rows:
            bot_y += LH
            paths[1] = ([(p2.cx, p2.bot + 2), (p2.cx, bot_y), (p3.cx, bot_y), (p3.cx, p3.bot + 2)], "below")
            need(max(tw(f"Loop {inside[0]}", 700), tw(inside[1])) <= p2.cx - p3.cx - 24, "the loop's ID crowds its lower arch")
        mid = ((p2.cx + p3.cx) / 2, max(p2.bot, p3.bot) + 28)
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
        out.append(loop_id(*mid, *inside, two=two_rows))
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
    body, h, (pa, pb) = two_loop(["E1", "D4"], lp["links"], inside=("B1a", "balancing"))
    need(pa.cx == pb.cx and pa.pw == pb.pw, "Loop B1a no longer draws one pill above the other at one width, as its alt says")
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
             alt=(f"Loop B1a from our systems atlas, “{lp['title']}”, drawn as two pills of one size, one above the other: "
                  f"{short('E1')} at the top and {lc(short('D4'))} below. Step 1, dashed, runs down the right with a plus tag "
                  "and the word raises; step 2, solid, runs up the left with a minus tag and the word lowers. Both lines are 2 px. Beside it, three notes "
                  "say every connection draws at 2 px, both variables take the same pill, and nothing in the drawing measures."),
             notes="Lines by the atlas build's wire_marks at 2 px with the 28 px lead-in; pills sized only by their labels.")
    book.log("15.1 correct", "Loop B1a, oversight", "D05")
    fb, fh, _ = two_loop(["E1", "D4"], lp["links"], inside=("B1a", "balancing"), widths={1: 6}, scale=[1.2, 1.0])
    fail = dnp() + hed("Loop", "B1a", lp["title"]) + fig(svg_wrap(fb, fh))
    book.add("s-15-1-failure", fail, rule="15.1",
             alt=(FC + "Loop B1a with its second step drawn 6 px thick, three times the first, and the pill for "
                  f"{lc(short('E1'))} drawn larger than the other, with no key to say what the width or the size measures."),
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
            {"label": "Pill", "value": f"{PW} px wide on a {W} px drawing, wider where the variable’s title would take more than "
                                       f"{words_n(MAX_ROWS)} rows, with {PAD} px inside each end; 44 px tall, or the title’s rows at "
                                       f"{LH} px plus 22; a 2 px outline"},
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
    need(GLOSS["Variable"].startswith("A quantity or condition in the model that can rise or fall."), "the atlas's definition of a variable changed")
    cards = []
    for c, _ in picks:
        p = Pill(short(c), 2 + 85, 0, 170)
        p.cy = p.h / 2 + 2
        svg = svg_wrap(p.svg(), p.h + 4, w=174)
        n = node(c)
        cards.append(f'<div class="vc">{svg}<p class="hed">{chip("Variable", c)}</p>'
                     f'<p class="sub">{e(kind_word(c))}</p><p class="nt">{e(n["increase_means"])}</p></div>')
    need(174 <= TRI, "a variable's card is wider than a column of three")
    body = f'<div class="fx tri">{"".join(cards)}</div>' + src("variables B3, B1 and C3")
    book.add("s-15-2-correct", body, rule="15.2", readable=True, wide=True,
             alt=("Three variables from our systems atlas, each drawn as a pill with its own title, then its typed chip, "
                  "its kind and the atlas’s sentence on a higher value. "
                  + " ".join(f"Variable {c}, {short(c)}: {kind_word(c)}. {node(c)['increase_means']}" for c, _ in picks)),
             notes="Names are each variable's own title (DR-265); kinds and sentences from each variable's own record.")
    for c, d in (("B3", "D10"), ("B1", "D03"), ("C3", "D02")):
        book.log("15.2 correct", f"Variable {c}", d)
    l44 = link("L44")
    need((l44["from"], l44["to"], l44["polarity"]) == ("C4", "B5", "-"), "connection L44 changed")
    need(node("B5")["increase_means"] == "A higher value means turnout is more similar across income groups.", "variable B5's sentence changed")
    fb, fh, _ = card("C4", "B5", "L44", labels=(short("C4"), "Turnout"))
    fail = dnp() + fig(svg_wrap(fb, fh))
    book.add("s-15-2-failure", fail, rule="15.2",
             alt=(FC + f"A connection from {lc(short('C4'))}, with a minus tag and the word lowers, into a pill "
                  "labeled Turnout, with no chip, no kind and no sentence on what a higher value means."),
             notes="Labeled failure: B5's pill cut to one word, so its minus sign reads as fewer voters.")
    return {
        "id": "15.2",
        "title": "Name each variable, its kind and what a higher value means.",
        "rule": [
            f"Our systems atlas defines a variable as “{GLOSS['Variable'].split('.')[0].lower()}”. Draw each one as a pill "
            "holding its own title, the name on its record, in every drawing, a loop’s among them, so it carries one name "
            "wherever it appears. The first time a reader meets it, give its typed chip, its kind in words and the atlas’s own "
            "sentence on what a higher value means.",
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
                               f"so its minus sign reads as fewer voters. The atlas’s variable is {lc(short('B5'))}, and the sign "
                               "says the gap between income groups widens."},
        "specs": [
            {"label": "Name", "value": f"The variable’s own title, for all {len(NODE)}, never the shorter label a loop’s record lists for a step"},
            {"label": "Label", "value": f"15 px, semibold, wrapped inside the pill with {PAD} px at each end", "token": "oa.chart.type.label"},
            {"label": "Kind", "value": "Stock, flow, condition or outside driver, in words, from the variable’s type and its plain description; "
                                       "where the two disagree, as for Variable D6, no kind, since the atlas lists the question for its next version"},
            {"label": "Higher value", "value": "The atlas’s sentence, quoted, where the reader meets the variable first"},
            {"label": "Chip", "value": "Variable and the ID, as Rule 13.9 sets"},
        ],
        "related": ["10", "13", "18"],
        "builders": ["Read the name, the kind and the higher-value sentence from the variable’s own record, and stop the build "
                     "if a drawing prints the shorter label a loop’s record lists for it. Print the sentence as the atlas writes it."],
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
                  f"{l46['sign_meaning']} Connection L16 runs from {own('D4')} to {lc(short('E1'))}, with a "
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
    # RF-16a: the variables' own titles; 148 and 132 px set each in three rows with no word alone, 12 px apart
    a = Pill(own("D4"), 0, 0, 148)
    b = Pill(own("D6"), 0, 0, 132)
    need(len(a.rows) == len(b.rows) == 3 and a.pw + b.pw + 12 + 4 <= W, "15.5's two pills no longer sit side by side in three rows")
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
             alt=(f"Two authority connections from our systems atlas. Lines from {own('D4')} and from {own('D6')} "
                  f"run down across the boundary between the core and technology layers into Use of pricing "
                  f"algorithms. Each is solid, ends in an open diamond, carries the word decides and no sign. Beside them: "
                  f"Connection LT13, {l13['name']}, documented; Connection LT14, {l14['name']}, documented; and the atlas’s "
                  f"words, {l13['sign_meaning']}"),
             notes="Both lines by wire_marks with authority=True: the open diamond, no tag, delay ticks; the boundary per Rule 15.9.")
    book.log("15.5 correct", "Connections LT13 and LT14, pricing software", "D06")
    fb, fh, _ = card("D4", "TC7", "LT13", layers=("Core layer", "Technology layer"), sign="-", authority=False, words=["lowers"])
    fail = dnp() + fig(svg_wrap(fb, fh))
    book.add("s-15-5-failure", fail, rule="15.5",
             alt=(FC + f"The line from {own('D4')} to Use of pricing algorithms drawn as a causal arrow, with an "
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
            {"label": "Word", "value": "Decides, where a causal line prints its verb, or once in a key where every line in the drawing is an authority connection (Rule 15.17)"},
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
                  f"labeled Hypothesis: a solid step from {lc(short('B2'))} to {lc(short('C3'))}, and a dotted step back that "
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
             alt=(f"An open chain from our systems atlas, drawn downward: {short('E1')}, a minus tag and the words money, "
                  f"lowers, into {short('EC6')}, framed as the economy layer, then a plus tag and the "
                  f"words money, raises, into {lc(short('A4'))}. On the right, connection L37 runs from {lc(short('E1'))} "
                  f"straight to {lc(short('A4'))} with a minus tag and the words money, lowers. The chain reads: {ra} Beside it, "
                  "notes say the chain carries one minus sign, so the end moves opposite to the start, and the core map’s arrow agrees."),
             notes="Signs carried along the chain by script and checked against connection L37 (the atlas's convention).")
    book.log("15.8 correct", "Connections LE12, LE14 and L37, taxes and benefits", "D08")
    fail = dnp() + fig(chain_plate("+"))
    book.add("s-15-8-failure", fail, rule="15.8",
             alt=(FC + f"The same chain with a summary arrow on the right from {lc(short('E1'))} to {lc(short('A4'))} "
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
                         f"last step raises {lc(short('A4'))}, and the chain as a whole lowers it, as the core arrow says."],
                "basis": "Our systems atlas’s model conventions"},
        "correct": {"specimen": "s-15-8-correct",
                    "caption": "An open chain from our systems atlas through its economy layer, read with its signs carried "
                               "along, beside connection L37, the core map’s one arrow for the same path."},
        "failure": {"specimen": "s-15-8-failure",
                    "caption": "<strong>Fails Rule 15.8.</strong> The summary arrow takes the last step’s plus, so the chain reads "
                               f"as raising {lc(short('A4'))}. One minus sign along the way turns it, as connection L37 says."},
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
                  f"holding {short('B6')}. Below it a frame named Technology layer holds How platforms rank feeds and "
                  f"seek attention, and a line marked information, raises runs up from it across both frames into "
                  f"{lc(short('B6'))}. Each frame breaks where a line crosses it."),
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
                    "caption": f"Foreign interference outside every frame, {lc(short('B6'))} in the core layer’s cluster B, "
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
    lead = (f'Its reason opens on the drawn connection: feed ranking “changes what people see”, as {chip("Connection", "LT01")} '
            f'records.')
    need(reason[0].startswith("Feed ranking changes what people see"), "LTR1's first sentence changed")
    gls = GLOSS["Rejected connection"]
    need(gls.startswith("A relationship that was reviewed against the evidence and left off the map"), "the atlas's rejected connection entry changed")
    b, h, _ = card("TC1", "B6", "LT01", layers=("Technology layer", "Core layer"))
    panel = (f'<p class="k">Reviewed and not drawn</p><p class="hed"><span>From {vt("TC1")} to '
             f'{vt("B4")}</span></p><p class="nt">{lead}</p>'
             f'<p class="q">“{e(quote)}”</p><p class="nt">{tail}</p>'
             f'<p class="nt">The atlas keeps {words_n(len(rej))} connections it reviewed and left off its map, each with its reason.</p>')
    body = (label_for(["LT01"], "the grade of the connection drawn")
            + beside(hed("Connection", "LT01", link("LT01")["name"]) + fig(svg_wrap(b, h)) + f'<p class="nt">{gl("LT01")}</p>',
                     panel + src("connection LT01, rejected connection LTR1 and connection L47")))
    book.add("s-15-10-correct", body, rule="15.10", readable=True, wide=True,
             alt=(f"Connection LT01 from our systems atlas, “{link('LT01')['name']}”, drawn from How platforms rank feeds and seek "
                  f"attention, in the technology layer, down to {lc(short('B6'))}, in the core layer, with the words "
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
                  f"{lc(short('B4'))}, a connection the atlas reviewed and left off its map."),
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
            out.append(vt(t))
    return out


def acts_note(rid, r):
    n_l = sum(1 for t in r["targets"] if t in LINK)
    n_v = len(r["targets"]) - n_l
    parts = [f"{words_n(n_l)} connection{'s' if n_l != 1 else ''}" if n_l else "",
             f"{words_n(n_v)} variable{'s' if n_v != 1 else ''}" if n_v else ""]
    return (f'<p class="nt">It acts where the marks turn red: on {" and ".join(p for p in parts if p)}.</p>')


def band_p(r):
    b = r["band"]
    return f'<p class="nt"><b>{e(b.capitalize())}</b>: “{e(BANDS[b])}”</p>'


def loops_p(r, shown):
    """The loops a reform sits on, as a row of typed chips (a list, so no comma or period touches a chip, BC S16), and the
    one the drawing shows."""
    need(shown in r["loops"], f"reform {r['id']} does not sit on Loop {shown}")
    row = "".join(f"<li>{chip('Loop', k)}</li>" for k in r["loops"])
    return (f'<ul class="cr">{row}</ul>'
            f'<p class="nt">The drawing shows {chip("Loop", shown)} because it holds every target.</p>')


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
    items = kw(target_items(r, set(codes) | set(lp["links"])))
    words = (acts_note("R-03", r)
             + f'<p class="k">Its targets, from the atlas</p>{items}'
             + f'<p class="k">Its band</p>{band_p(r)}'
             + src("reform R-03, loop R4a, connections L42, L55 and L56, and the bands of change"))
    under = (step_lines(lp["links"]) + f'<p class="nt">{vt("C4")}, the pill at the top, sits in the {e(cname.lower())} '
             f'cluster with {chip("Variable", "C1")} and stays in ink.</p><p class="k">Its loops</p>{loops_p(r, "R4a")}')
    body = (hed("Reform", "R-03", r["title"]) + label_for(lp["links"], "the grade of the loop’s least certain step")
            + beside(hed("Loop", "R4a", lp["title"]) + fig(svg) + under, words))
    book.add("s-15-11-correct", body, rule="15.11", readable=True, wide=True,
             alt=(f"Reform R-03 from our systems atlas, “{r['title']}”, on Loop R4a, “{lp['title']}”. Three pills: "
                  f"{short('C4')} at the top, {lc(short('C1'))} below right, {lc(short('D7'))} below "
                  f"left. Step 1, from the top to {lc(short('C1'))}, is drawn heavy in red, and the outlines of {lc(short('C1'))} "
                  f"and {lc(short('D7'))} are red; step 2, dashed, and step 3 stay in ink, as does {lc(short('C4'))}. "
                  "Beside it: the reform acts where the marks turn red, on one connection and two variables: "
                  f"Connection L42, {link('L42')['name']}, documented; Variable C1, {lc(node('C1')['title'])}; Variable D7, "
                  f"{lc(node('D7')['title'])}. Its band, rules: {BANDS['rules']} Under the drawing: Variable C4, "
                  f"{lc(node('C4')['title'])}, the pill at the top, sits in the electoral competition cluster with Variable C1 "
                  "and stays in ink; its loops are Loop R4a, Loop R10 and "
                  "Loop R12, and the drawing shows Loop R4a because it holds every target. Each step with its grade: "
                  + "; ".join(f"step {i}, Connection {x}, {GRADE[link(x)['evidence']][0].lower()}" for i, x in enumerate(lp["links"], 1))
                  + "."),
             notes="Targets read from the reform's record and drawn in Rule 12.5's red by wire_marks at the 6 px sizes; the band "
                   "quoted from the atlas's bands of change.")
    book.log("15.11 correct", "Reform R-03 on Loop R4a, district maps", "D02")
    fb, fh = three_loop(codes, lp["links"], inside=("R4a", "reinforcing"), targets={"C4", "C1", "L42"})
    fail = (dnp() + hed("Reform", "R-03", r["title"]) + fig(svg_wrap(fb, fh))
            + f'<p class="nt">Reform R-03 acts on {e(cname.lower())}.</p>')
    book.add("s-15-11-failure", fail, rule="15.11",
             alt=(FC + f"Loop R4a with every mark of the electoral competition cluster in red: {lc(short('C4'))}, "
                  f"{lc(short('C1'))} and the step between them. {short('D7')} stays in ink. A note reads: Reform "
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
            "red in their place. Print the reform’s band, the kind of change it makes, beside it in the atlas’s words. The "
            "bands follow Donella Meadows’ ordering of places to intervene in a system, from changing a number to changing "
            "what the system aims for. Of the "
            f"{len(REFORM)} reforms, {bands['rules']} change rules, {bands['parameter']} change a parameter, "
            f"{words_n(bands['feedback'])} feedback, {words_n(bands['information'])} information, "
            f"{words_n(bands['power to change the rules'])} the power to change the rules and {words_n(bands['goals'])} goals.",
        ],
        "tokens": ["oa.color.data.emphasisRed.onNewsprint", TOKEN_LINE],
        "why": {"text": ["A reform acts on a few connections and variables, and the rest of the mechanism has to respond on its "
                         "own. Red on the exact targets shows a reader where the reform acts, before any claim about results. "
                         "Red on a whole cluster says it acts on variables the atlas never lists."],
                "basis": "Our systems atlas’s reform profiles and its bands of change; Rule 12.5"},
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


def grade_block(grade, what, quote_html=None):
    """One of a reform's two grades, as its own label with Rule 13.3's word and gloss, and the atlas's words under it."""
    return (f'<div class="gp">{diagram_label(grade, f"{GRADE[grade][1]}, {what}")}'
            + (f'<p class="nt">{quote_html}</p>' if quote_html else "") + '</div>')


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
    # BC S15 under the data lead's RF-21: the plate leads with the two grades the rule teaches, so its first label is the
    # problem's and its second the remedy's; the connections' grades sit in the step list under the drawing, beside the
    # connections they grade, as SD-7's lists do, and the drawing takes no label of its own above it. AX S10: a reader who
    # arrives by a link meets the step words, the ticks and the layers in a short key on this plate
    chain = ["LT03", "L26"]
    steps = (f'<p class="k">Each step</p>'
             + "".join(f'<p class="nt"><b>{i}</b>&#160;{chip("Connection", x)} “{e(link(x)["name"])}”.&#160;'
                       f'{grade_word(link(x)["evidence"], gloss=False)}</p>' for i, x in enumerate(chain, 1)))
    words = f'<p class="k">Two grades, apart</p>{blocks}'
    key = reading_key(chain, layers=("Technology layer", "Core layer"))
    # SD-9: in the page's order (one column, and for a screen reader at every width) the two grades come before the
    # step list; at 680 px the steps still sit under the drawing, with the grades in the right column across both rows
    body = (hed("Reform", "R-32", r["title"])
            + f'<div class="fx g3"><div>{fig(svg)}{acts_note("R-32", r)}</div><div>{words}</div><div>{steps}</div></div>'
            + f'<div class="kb"><p class="k">Reading a step</p>{key}</div>'
            + src("reform R-32, its problem and remedy evidence, and connections LT03 and L26"))
    need(body.index("Two grades, apart") < body.index("Each step") and body.index('class="ev"') > body.index("Two grades, apart"),
         "Rule 15.12's plate must lead with its two grades in the page's order (RF-21, SD-9)")
    book.add("s-15-12-correct", body, rule="15.12", readable=True, wide=True,
             alt=(f"Reform R-32 from our systems atlas, “{r['title']}”, on a chain of three pills drawn downward: Concentration "
                  f"of platforms and digital advertising, in the technology layer, then across a rule into the core layer, "
                  f"{lc(short('B2'))} and {lc(short('C3'))}. Both connections and the outline of {lc(short('B2'))} are red: money, "
                  "lowers, then information, raises. Beside it, two labels: Well supported, strong research evidence, for the "
                  f"evidence of the problem, with the atlas’s words: {pt[0]} Hypothesis, not yet tested, for the evidence for "
                  f"the remedy, with the atlas’s words: {rt_} Under the drawing, each step with its grade: "
                  + "; ".join(f"step {i}, Connection {x}, {link(x)['name']}, {GRADE[link(x)['evidence']][0].lower()}"
                              for i, x in enumerate(chain, 1))
                  + f". A key says that money, lowers and information, raises name what moves along each "
                  f"connection and which way the next variable moves; that ticks count a step’s delay, {ticks_line(chain)}; and "
                  "that the technology layer and the core layer are two of the three layers of the atlas’s model."),
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
            "Our systems atlas grades each reform twice. In its glossary’s words, evidence of the problem is “"
            + pg.split(". ")[0][0].lower() + pg.split(". ")[0][1:] + "”, and evidence for the remedy is “"
            + rg.split(", with")[0][0].lower() + rg.split(", with")[0][1:] + "”. Print each as its own label with Rule "
            "13.3’s word and gloss, and quote the atlas’s words under it.",
            "A drawing of the reform carries a third grade, how sure the atlas is of the mechanism. Each connection shows it "
            "in its line code, the solid, dashed or dotted line Rule 13.4 sets by grade. Print each connection’s grade "
            "word in the list of steps under the drawing, and keep all three grades apart. Of the atlas’s "
            f"{len(REFORM)} reforms, {two} carry two different grades, and in {lower} of them the remedy’s grade is the lower.",
        ],
        "tokens": ["oa.chart.grade.documented", "oa.chart.grade.hypothesis"],
        "why": {"text": ["A problem on the record says nothing yet about whether a fix works. A reader shown one grade carries the "
                         "stronger to both, and a well-documented harm then reads as proof of an untested remedy."],
                "basis": "Our systems atlas’s glossary and reform profiles; Rule 13.3"},
        "correct": {"specimen": "s-15-12-correct",
                    "caption": "Reform R-32 with its two grades apart: the evidence of the problem well supported, and the "
                               "evidence for the remedy a hypothesis, each in the atlas’s words, with each connection’s grade "
                               "in the list of steps under the drawing."},
        "failure": {"specimen": "s-15-12-failure",
                    "caption": "<strong>Fails Rule 15.12.</strong> One label, Well supported, covers the reform, so the loss of "
                               "local news reads as proof that funding would restore it. The atlas grades that remedy a hypothesis."},
        "specs": [
            {"label": "Problem", "value": "Its own label: Rule 13.3’s word and gloss, then “evidence of the problem”, and the atlas’s words quoted"},
            {"label": "Remedy", "value": "Its own label the same way, “evidence for the remedy”"},
            {"label": "Order", "value": "The problem’s label first and the remedy’s second, as the first two labels on the plate"},
            {"label": "Connections", "value": "Their own line code (Rule 13.4), and each one’s grade word in the list of steps under the drawing"},
            {"label": "Never", "value": "One grade for the whole reform"},
            {"label": "Counts", "value": f"{two} of {len(REFORM)} reforms carry two different grades, as of the snapshot"},
        ],
        "related": ["13"],
        "builders": ["Read the two grades from <code>problem_evidence</code> and <code>remedy_evidence</code>, print each through "
                     "Rule 13.3’s table, and never fall back from one to the other."],
    }


# ===============================================================================================================
# Group 3. Worked examples from the atlas
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
    said = f'The atlas’s evidence summary names {chip("Connection", "L02")} as the middle step, which “{e(frag)}”'
    said_alt = f"The atlas’s evidence summary names connection L02 as the middle step, which “{frag}”"
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
                  f"certain step. Three pills: {short('A1')} at the top, {lc(short('B1'))} below right, "
                  f"{lc(short('E1'))} below left. Step 1, solid, money, raises; step 2, dashed, money, raises, marked weakest step; step 3, "
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
                "basis": "Our systems atlas, the record and evidence summary of Loop R1"},
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
    rev_html = f'Its evidence note reads “{e(f1)}”, and says the loop “{e(f2)}” {vt("A1")}.'
    rev_txt = (f"Its evidence note reads “{f1}”, and says the loop “{f2}” Variable A1, “{node('A1')['title']}”.")
    codes = ["A5", "A6"]
    b, h, _ = two_loop(codes, lp["links"], inside=("R8", "reinforcing"))
    panel = (f'<p class="k">The atlas’s revision, as of {SNAP}</p><p class="nt">{rev_html}</p>'
             f'<p class="nt">{why_html}</p>')
    body = (diagram_label("well-supported", "strong research evidence, the grade of both steps")
            + beside(hed("Loop", "R8", lp["title"]) + fig(svg_wrap(b, h)),
                     ra_p(read_aloud(codes, lp["links"])) + panel
                     + src("loop R8, its evidence note and qualification, and connection T12")))
    book.add("s-15-14-correct", body, rule="15.14", readable=True, wide=True,
             alt=(f"Loop R8 from our systems atlas, “{lp['title']}”, under a label reading Well supported. Two pills, {short('A5')} "
                  f"and {lc(short('A6'))}, with step 1 over the top, plus, raises, and step 2 under the bottom, plus, "
                  f"raises, both solid with three delay ticks. The loop reads: {read_aloud(codes, lp['links'])} Beside it, the "
                  f"atlas’s revision as of {SNAP}. {rev_txt} {why_txt}"),
             notes="The revision and its reason quoted from the loop's evidence and qualification fields, with the snapshot date.")
    book.log("15.14 correct", "Loop R8, housing scarcity", "D09")
    stations = [short("A5"), short("A6"), short("A1")]
    fb, fh = drawn_loop(3, stations, [{"sign": "+", "grade": "well-supported", "delay": "L"}] * 3, inside=("R8", "reinforcing"))
    fail = dnp() + hed("Loop", "R8", lp["title"]) + fig(svg_wrap(fb, fh))
    book.add("s-15-14-failure", fail, rule="15.14",
             alt=(FC + f"Loop R8 drawn through three pills, {short('A5')}, {lc(short('A6'))} and {lc(short('A1'))}, with "
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
                "basis": "Our systems atlas, the record of Loop R8 and Connection T12"},
        "correct": {"specimen": "s-15-14-correct",
                    "caption": "Loop R8 as our systems atlas holds it, with the atlas’s revision and its reason quoted beside "
                               f"the drawing, as of {SNAP}."},
        "failure": {"specimen": "s-15-14-failure",
                    "caption": f"<strong>Fails Rule 15.14.</strong> The drawing routes Loop R8 through {lc(short('A1'))} with "
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
    need(LOOP_NAME["C3"] == "Electoral pressure" and c3["title"] == "Risk of losing office", "Variable C3's names changed")
    ep = GLOSS["Electoral pressure"]
    need(ep == "The credible chance that an official will lose office. It can change behavior before any election removes anyone.",
         "the atlas's entry for electoral pressure changed")
    qual = "The loop works only where seats are competitive."
    need(b4["qualification"].startswith(qual), "Loop B4's qualification changed")
    val = b4["valence"]
    need("Its strength depends on C1: Seats with little electoral competition, C2: How often the primary decides the winner," in val,
         "Loop B4's valence changed")
    weak54 = "since its main study covers Brazilian mayors"
    need(b4["evidence_summary"].endswith(f"For U.S. services the weakest is L54, {weak54}."), "Loop B4's weakest step changed")
    deps = re.findall(r"\b([A-E]\d): ", val.split("Its strength depends on ")[1].split(". ")[0])
    need(deps == ["C1", "C2", "B2", "B4"], f"Loop B4's strength no longer depends on four variables: {deps}")
    need((link("L08")["from"], link("L08")["to"]) == ("C1", "C2") and r10["links"][0] == "L08", "Loop R10's first step changed")
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
                 + kw([f'<b>Into it</b>&#160;{gl(a)}. “{e(link(a)["sign_meaning"])}”',
                       f'<b>Out of it</b>&#160;{gl(b_)}. “{e(link(b_)["sign_meaning"])}”']))
        steps += step_lines(lp["links"], skip=(a, b_), head="The loop’s other steps",
                            extra={"L54": f' The atlas calls it the weakest for U.S. services, “{e(weak54)}”.'})
        grades = {link(x)["evidence"] for x in lp["links"]}
        lab = (diagram_label(grades.pop(), f"{GRADE[link(lp['links'][0])['evidence']][1]}, the grade of all "
                                           f"{words_n(len(lp['links']))} steps")
               if len(grades) == 1 else label_for(lp["links"], "the grade of the loop’s least certain step"))
        cols.append(f'<div>{lab}{hed("Loop", lid, lp["title"])}'
                    f'{fig(svg_wrap(b, h), read_aloud(codes, lp["links"]))}{steps}</div>')
    meet = (f'<p class="k">Where the two loops meet</p>'
            f'<p class="nt">{vt("C3")} is the pill filled in ink in both drawings. '
            f'The atlas’s glossary defines it as electoral pressure: “{e(ep)}”</p>'
            f'<p class="nt">Loop B4, in the atlas’s words, “{e(qual[len("The loop "):])}” Of the {words_n(len(deps))} '
            f'variables the atlas says its strength depends on, {chip("Variable", "C1")} and {chip("Variable", "C2")} sit at '
            f'the two ends of Loop R10’s first step.</p>')
    body = (f'<div class="fx pr">{"".join(cols)}</div><div class="kb">{meet}</div>'
            + src("loops B4 and R10, their connections, and the glossary entry for electoral pressure"))
    book.add("s-15-15-correct", body, rule="15.15", readable=True, wide=True,
             alt=(f"Loop B4, “{b4['title']}”, beside Loop R10, “{r10['title']}”, from our systems atlas. Both pass through "
                  f"{short('C3')}, the pill filled in ink in each drawing. Loop B4 draws three pills, {short('D5')}, "
                  f"{short('C3')} and {short('C5')}, its steps marked minus, plus and plus, balancing. Loop R10 "
                  f"draws four on a square, {short('C1')}, {short('C2')}, {short('C3')} and {short('C4')}, its steps "
                  f"marked plus, minus, minus and plus, reinforcing. Under each, the connection into {lc(short('C3'))} "
                  f"and the one out of it, with the atlas’s sentences. In Loop B4: {link('L23')['sign_meaning']} "
                  f"{link('L24')['sign_meaning']} In Loop R10: {link('L25')['sign_meaning']} {link('L53')['sign_meaning']} "
                  f"A note says Variable C3, {lc(short('C3'))}, is the shared variable, which the atlas’s glossary defines as "
                  f"electoral pressure: {ep} Loop "
                  "B4 works only where seats are competitive, and of the four variables the atlas says its strength depends "
                  "on, Variable C1 and Variable C2 sit at the two ends of Loop R10’s first step. Loop B4’s label reads Well "
                  "supported, the grade of all three steps, and under each loop its other steps print with their grades; the "
                  "atlas calls Connection L54 the weakest for U.S. services, since its main study covers Brazilian mayors."),
             notes="Both loops read by script; the shared variable found as the intersection of their chains; the in and out "
                   "connections of Variable C3 checked against each loop.")
    book.log("15.15 correct", "Loop B4, public services", "D04")
    book.log("15.15 correct", "Loop R10, safe seats", "D02")
    fcols = []
    for lid, kind, n in specs_:
        lp = LOOP[lid]
        codes = [c for c, _ in lp["chain"]]
        # the fault: Loop B4 calls Variable C3 by its chain label there, Loop R10 by its title (DR-265's one name)
        labels = [LOOP_NAME["C3"] if c == "C3" and lid == "B4" else short(c) for c in codes]
        if n == 3:
            b, h = three_loop(codes, lp["links"], inside=(lid, kind), labels=labels)
        else:
            b, h = four_loop(codes, lp["links"], inside=(lid, kind), labels=labels)
        fcols.append(f'<div>{hed("Loop", lid, lp["title"])}{fig(svg_wrap(b, h))}</div>')
    fail = dnp() + f'<div class="fx pr">{"".join(fcols)}</div>'
    book.add("s-15-15-failure", fail, rule="15.15", wide=True,
             alt=(FC + f"The same two loops side by side, with the shared variable named {LOOP_NAME['C3']} in Loop B4 and "
                  f"{short('C3')} in Loop R10, in plain pills, with no chip and no word that the two are one variable."),
             notes="Labeled failure: the shared variable under two names and no mark, so the loops read as unrelated.")
    return {
        "id": "15.15",
        "title": "Follow a variable two loops share through each loop in turn.",
        "rule": [
            f"Loop B4, “{b4['title']}”, and Loop R10, “{r10['title']}”, both pass through Variable C3, "
            f"{lc(c3['title'])}. Draw the two loops side by side, give the shared variable its own title in both, and "
            "fill its pill in ink in each drawing, the one place a pill takes a fill. Under each loop, print the connection "
            "that brings a change into the shared variable and the one that carries it on, with the atlas’s sentence on each sign.",
            "Then say where the loops meet, in the atlas’s words. As primaries decide more seats in Loop R10, the risk of "
            "losing office falls, and in Loop B4 that same risk turns poor service into defeats that improve it. The atlas says "
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
            {"label": "Shared variable", "value": "Its own title in both drawings, its pill filled in ink with its name in the surface color",
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
                   f'<p><b>{e(x["feasibility"].capitalize())}</b> feasibility</p><p>{e(when)}</p></li>')
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
    words = (acts_note("R-01", r)
             + f'<p class="k">Its targets</p>{kw(target_items(r, set(codes) | set(lp["links"])))}'
             + f'<p class="k">Its two grades, apart (Rule 15.12)</p>'
             + grade_block(pe, "evidence of the problem") + grade_block(re_, "evidence for the remedy"))
    fx = (f'<div><p class="k">Effects by outcome family, as of {SNAP}</p>{effect_rows(r)}'
          f'<p class="nt">The atlas: “{e(q_note)}” Its confidence in these sizes: “{e(r["effects_confidence"])}”.</p></div>'
          f'<div><p class="k">Routes, with the date each was checked</p>{route_rows(r)}'
          f'<p class="nt">Feasibility is the atlas’s judgment for 2026 to 2030.</p></div>')
    body = (hed("Reform", "R-01", r["title"]) + label_for(lp["links"], "the grade of the loop’s least certain step")
            + beside(hed("Loop", "R10", lp["title"]) + fig(svg) + step_lines(lp["links"])
                     + f'<p class="k">Its loops</p>{loops_p(r, "R10")}', words)
            + f'<div class="two">{fx}</div>'
            + src("reform R-01, its targets, effects and routes, and loop R10 with its connections"))
    fam_alt = "; ".join(f"{FAMILY[k]}, {r['effects'][k]}, {EFFECT_WORDS[r['effects'][k]]}" for k in ("DQ", "GE", "EP", "EQ"))
    rt_alt = "; ".join(f"Route {x['route']}, {C13.ROUTE_NAME[x['route']]}, {x['who']}, {x['feasibility']} feasibility, "
                       + (f"checked {C13.words_date(x['checked'])}" if x["checked"] else "not checked") for x in r["routes"])
    book.add("s-15-16-correct", body, rule="15.16", readable=True, wide=True,
             alt=(f"Reform R-01 from our systems atlas, “{r['title']}”, on Loop R10, “{lp['title']}”, drawn on a square: "
                  f"{short('C1')}, {lc(short('C2'))}, {lc(short('C3'))} and {lc(short('C4'))}. Step 1, from "
                  f"{lc(short('C1'))} to {lc(short('C2'))}, and step 2, from {lc(short('C2'))} to {lc(short('C3'))}, are drawn "
                  f"heavy in red, and the outline of {lc(short('C2'))} is red; the other two steps and pills stay in ink. "
                  f"Beside it: Connection L08, {link('L08')['name']}, documented; Connection L25, {link('L25')['name']}, well "
                  f"supported; Variable C2, {lc(node('C2')['title'])}. Its loops: Loop R10, Loop B4 and Loop R11. Evidence of "
                  f"the problem, plausible, some evidence; for the remedy, contested, evidence disputed, each as its own label. "
                  f"Effects by outcome family, as of {SNAP}, one row each: "
                  f"{fam_alt}. {q_note} Routes: {rt_alt}. Under the drawing, each step of the loop with its grade: "
                  + "; ".join(f"step {i}, Connection {x}, {GRADE[link(x)['evidence']][0].lower()}" for i, x in enumerate(lp["links"], 1))
                  + "."),
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
        "title": "Show a reform’s four effects apart, with each route’s check date.",
        "rule": [
            f"Reform R-01, “{r['title']}”, targets two connections and one variable on Loop R10, and sits on Loops R10, B4 "
            "and R11. Draw it where it acts (Rule 15.11), then print its effects one outcome family to a row, each with the "
            "atlas’s code, its words and the pips of Rule 13.5, and no row that adds them. Its routes follow, each with who "
            "acts there, its feasibility and its own check date, or “Not checked” where the atlas gives none (Rule 13.10).",
            f"As of {SNAP}, the atlas codes its effect on the quality of democracy {EFFECT_WORDS['+M']}, on government "
            f"efficacy {EFFECT_WORDS['+S']}, and on the other two families {EFFECT_WORDS['0']}. It checked the state ballot "
            "and local routes on that date, and the state statute and federal statute routes carry no date.",
        ],
        "tokens": ["oa.color.data.emphasisRed.onNewsprint", TOKEN_LINE],
        "why": {"text": ["A single score would hide what the atlas keeps apart: the families use different units, and a reform "
                         "can help one while it costs another. A route rated without a date reads as current, and a reader "
                         "deciding where to act needs to know which ratings the atlas checked."],
                "basis": "Our systems atlas, the profile of Reform R-01 and the note on effect codes; Rules 13.5 and 13.10"},
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


AUTH = ["LE02", "LE03", "LE19", "LT13", "LT14", "LT16", "LT17"]
BODY = {"D1": "Congress", "D2": "The executive", "D4": "Antitrust enforcers", "D6": "States and cities"}   # from V7's own
#                                                     connection names, checked in Rule 15.17 (AX S10)


LADDER_PW = 156             # every pill of the authority diagram: one width, so their ends line up in a column
LANE = 12                  # the space between two lanes beside the column


def end_x(p, off, side):
    """Where a horizontal line at a vertical offset from a pill's middle meets its rounded end, 2 px clear of it."""
    r = p.h / 2
    inset = r - math.sqrt(max(r * r - off * off, 0))
    return p.left + inset - 2 if side == "left" else p.right - inset + 2


def authority_plate(failure=False):
    """The seven authority connections in one drawing, as a ladder: one column of pills in three bands, the economy
    layer at the top, the four deciding bodies in the core layer and the technology layer at the bottom, each band set
    off by a 1 px rule with its name (Rule 15.9). Lines into the economy layer run in lanes on the right and lines into
    the technology layer in lanes on the left, nested so that no two cross; each leaves its body's pill end level, runs
    in its lane and enters the decided variable's end with the open diamond. failure folds the four bodies into one pill
    (Rule 15.17's failure). Returns (svg, rows, edges)."""
    econ, tech = ["EC2", "EC10"], ["TC7", "TC5"]
    core = ["GOV"] if failure else ["D2", "D1", "D4", "D6"]
    if failure:
        edges = [("GOV", "EC2", "right", 0), ("GOV", "EC10", "right", 1), ("GOV", "TC5", "left", 0), ("GOV", "TC7", "left", 1)]
    else:
        # lane 0 is outermost: the nesting the column's order allows (EC2, EC10, D2, D1, D4, D6, TC7, TC5)
        edges = [("D1", "EC2", "right", 0, "LE02"), ("D2", "EC2", "right", 1, "LE03"), ("D2", "EC10", "right", 2, "LE19"),
                 ("D2", "TC5", "left", 0, "LT16"), ("D1", "TC5", "left", 1, "LT17"), ("D4", "TC7", "left", 2, "LT13"),
                 ("D6", "TC7", "left", 3, "LT14")]
    n_left = 1 + max(x[3] for x in edges if x[2] == "left")
    n_right = 1 + max(x[3] for x in edges if x[2] == "right")
    lane_x = {"left": [8 + LANE * i for i in range(n_left)], "right": [W - 8 - LANE * i for i in range(n_right)]}
    cx = 70 + LADDER_PW / 2                       # the column: 26 px clear of the inner left lane, 38 of the inner right
    pills, y, out = {}, 2, []
    bands = [("Economy layer", econ), ("Core layer", core), ("Technology layer", tech)]
    divs = []
    for bi, (name, codes) in enumerate(bands):
        if bi:
            divs.append(y + 26)
            y += 52
        for i, c in enumerate(codes):
            if i:
                y += 14
            lab = "The government" if c == "GOV" else own(c)
            p = Pill(lab, cx, 0, LADDER_PW)
            need(p.pw == LADDER_PW, f"{lab!r} does not fit a {LADDER_PW} px pill")
            p.cy = y + p.h / 2
            y = p.bot
            pills[c] = p
    # offsets where two lines share a pill end: the outer lane's line takes the side away from its travel
    ends = {}
    for ed in edges:
        a, b, side, lane = ed[:4]
        ends.setdefault((a, side), []).append((lane, "out", ed))
        ends.setdefault((b, side), []).append((lane, "in", ed))
    off = {}
    for (c, side), lst in ends.items():
        if len(lst) == 1:
            off[(c, side, lst[0][2])] = 0
            continue
        need(len(lst) == 2, f"three lines share one end of {c}")
        lst.sort(key=lambda t: t[0])                 # outer lane first
        outer, inner = lst
        up = pills[outer[2][1]].cy < pills[outer[2][0]].cy   # the outer line travels up (into the economy layer)
        role = outer[1]
        # departing up or arriving from above: the outer takes the lower offset; departing down or arriving from below: upper
        lower = (role == "out" and up) or (role == "in" and not up)
        off[(c, side, outer[2])] = 8 if lower else -8
        off[(c, side, inner[2])] = -8 if lower else 8
    xs_used = []
    for ed in edges:
        a, b, side, lane = ed[:4]
        lid = ed[4] if len(ed) > 4 else None
        pa, pb = pills[a], pills[b]
        ya, yb = pa.cy + off[(a, side, ed)], pb.cy + off[(b, side, ed)]
        lx = lane_x[side][lane]
        xa, xb = end_x(pa, ya - pa.cy, side), end_x(pb, yb - pb.cy, side)
        first = abs(lx - xa)
        delay = link(lid)["delay"] if lid else None
        need(first >= 12 + 5 * ({"S": 0, "M": 1, "L": 2}.get(delay, 0)) + BEND + 4,
             f"the line into {b} leaves {a} with {first:.0f} px before its lane, short of its ticks")
        if lid:
            l = link(lid)
            need((l["from"], l["to"], l["type"]) == (a, b, "authority"), f"connection {lid} no longer runs from {a} to {b}")
        m, _ = conn([(xa, ya), (lx, ya), (lx, yb), (xb, yb)], "documented", None, delay, authority=True)
        out.append(wr(m))
        xs_used.append(lx)
    need(min(lane_x["right"]) - max(p.right for p in pills.values()) >= 26 and
         min(p.left for p in pills.values()) - max(lane_x["left"]) >= 26, "a lane runs too close to the column")
    # the bands' rules, across the column only, so no lane crosses them; each name at the rule's right end
    x0, x1 = cx - LADDER_PW / 2, cx + LADDER_PW / 2
    for yd, (above, below) in zip(divs, [("Economy layer", "Core layer"), ("Core layer", "Technology layer")]):
        out.append(f'<path class="fr" d="M{F(x0)} {F(yd)}H{F(x1)}"/>' + text(x1, yd - 8, above, "fl", "end")
                   + text(x1, yd + 20, below, "fl", "end"))
    out.append("".join(p.svg() for p in pills.values()))
    return svg_wrap("".join(out), y + 4), pills, edges


def key_decides(lids):
    """The diagram's key: one short authority line, with its open diamond, and the word it stands for; then the same
    line with two ticks, and what the ticks count, for the delay classes the drawn connections hold (AX S10)."""
    m, _ = conn([(1, 9), (61, 9)], "documented", None, None, authority=True)
    mt, _ = conn([(1, 9), (61, 9)], "documented", None, "M", authority=True)
    sv = '<svg class="sv" viewBox="0 0 64 18" width="64" height="18" aria-hidden="true" focusable="false">'
    return (f'<p class="kd2">{sv}{wr(m)}</svg><span><b>decides</b>: the body where the line starts holds the power over '
            f'the variable at its diamond</span></p>'
            f'<p class="kd2">{sv}{wr(mt)}</svg><span><b>Ticks</b> near a line’s start count its delay, '
            f'{ticks_line(lids)}</span></p>')


def rule_15_17(book):
    """Worked example 5: the atlas's seven authority connections in one drawing (Master Brief section 14)."""
    auth = sorted(k for k, l in LINK.items() if l["type"] == "authority")
    need(auth == sorted(AUTH), f"the authority connections changed: {auth}")
    want = {"LE02": ("D1", "EC2"), "LE03": ("D2", "EC2"), "LE19": ("D2", "EC10"), "LT13": ("D4", "TC7"),
            "LT14": ("D6", "TC7"), "LT16": ("D2", "TC5"), "LT17": ("D1", "TC5")}
    for k, (a, b) in want.items():
        l = link(k)
        need((l["from"], l["to"], l["polarity"], l["evidence"], l["loops"]) == (a, b, None, "documented", []),
             f"authority connection {k} changed")
    need(all(node(a)["layer"] == "core" for a, _ in want.values()), "a deciding body left the core layer")
    lay = {b: node(b)["layer"] for _, b in want.values()}
    need(lay == {"EC2": "economy", "EC10": "economy", "TC7": "technology", "TC5": "technology"}, "a decided variable changed layer")
    sm = {link(k)["sign_meaning"] for k in AUTH}
    need(sm == {"This line shows who has the power to decide. It does not say which way they will decide."},
         "the atlas's sentence on authority lines changed")
    by_target = Counter(b for _, b in want.values())
    two = sorted(b for b, n in by_target.items() if n == 2)
    need(two == ["EC2", "TC5", "TC7"] and by_target["EC10"] == 1, "the count of bodies over each variable changed")
    reach = {a: {lay_ for k_, (a_, b_) in want.items() if a_ == a for lay_ in [node(b_)["layer"]]} for a, _ in want.values()}
    need(sorted(a for a, s_ in reach.items() if len(s_) == 2) == ["D1", "D2"], "the bodies that reach both layers changed")
    svg, pills, edges = authority_plate()
    titles = {c: node(c)["title"] for c in ("EC2", "EC10", "TC5", "TC7")}
    need(titles == {"EC2": "Public investment in research and infrastructure", "EC10": "Costs of tariffs and trade rules",
                    "TC5": "Government's ability to build and run digital services", "TC7": "Use of pricing algorithms"},
         "the titles of the decided variables changed")
    need(sorted(ed[4] for ed in edges) == sorted(AUTH), "the diagram leaves out an authority connection")

    def li(k):
        l = link(k)
        return f'{chip("Connection", k)} “{e(l["name"])}”.&#160;{grade_word(l["evidence"], gloss=False)}'

    econ = [k for k in AUTH if lay[want[k][1]] == "economy"]
    tech = [k for k in AUTH if lay[want[k][1]] == "technology"]
    # AX S10 with RF-16: each pill prints the variable's own title, and the list under the drawing names the body whose
    # power it holds, as the atlas's own connection names give it ("Congress decides public investment levels")
    for c, who in BODY.items():
        frm = [k for k in AUTH if link(k)["from"] == c]
        need(frm and all(link(k)["name"].startswith(who + " ") for k in frm), f"the atlas's connections from {c} no longer name {who}")
    bodies = kw([f"<b>{e(who)}</b>: {vt(c)}" for c, who in BODY.items()])
    words = (f'<p class="k">Key</p>{key_decides(AUTH)}'
             f'<p class="k">Into the economy layer</p>{kw([li(k) for k in econ])}'
             f'<p class="k">Into the technology layer</p>{kw([li(k) for k in tech])}'
             f'<p class="nt">Two bodies decide each of {vt("EC2")}, {vt("TC5")} and {vt("TC7")}; one decides {vt("EC10")}. '
             f'Of each line, the atlas says: “{e(next(iter(sm)))}”</p>'
             + src("its seven authority connections and the variables they reach"))
    body = (diagram_label("documented", "on the public record, the grade of all seven connections")
            + beside(fig(svg) + f'<p class="k">The four bodies, as the atlas’s connections name them</p>{bodies}', words))
    book.add("s-15-17-correct", body, rule="15.17", readable=True, wide=True,
             alt=("The seven authority connections in our systems atlas, in one drawing of three layers. At the top, the "
                  "economy layer: Public investment in research and infrastructure, and Costs of tariffs and trade rules. In the "
                  "core layer, four variables that hold the deciding bodies’ powers: "
                  + ", ".join(own(c) for c in ("D2", "D1", "D4")) + f" and {own('D6')}. "
                  "At the bottom, the technology layer: Government’s ability to "
                  "build and run digital services, and Use of pricing algorithms. Seven solid lines with no sign run from the "
                  "core variables to what they decide, in lanes beside the column, those into the economy layer on the right and "
                  "those into the technology layer on the left, and none crosses another. Each ends in an open diamond, which a "
                  "key beside the drawing reads as decides, and carries one or two ticks near its start, which the key reads as "
                  f"its delay, {ticks_line(AUTH)}. Under the drawing, the four bodies, each with its variable: "
                  + "; ".join(f"{who}, Variable {c}, {node(c)['title']}" for c, who in BODY.items())
                  + ". Beside it, each connection with its name, all documented: "
                  + "; ".join(f"Connection {k}, {link(k)['name']}" for k in AUTH)
                  + ". Two bodies decide each of three variables, and one decides tariff costs. Of each line the atlas says: "
                  + next(iter(sm))),
             notes="All seven authority connections read by script, with their ends, layers, grades and delays; drawn by "
                   "wire_marks with its authority switch in nested lanes, so no two lines cross.")
    book.log("15.17 correct", "Seven authority connections, who decides", "D05")
    fsvg, _, _ = authority_plate(failure=True)
    fail = dnp() + fig(fsvg)
    book.add("s-15-17-failure", fail, rule="15.17",
             alt=(FC + "One pill named The government, in place of the four bodies, with four lines that end in open "
                  "diamonds at the four variables the atlas’s authority connections reach, in the economy and technology layers."),
             notes="Labeled failure: the four deciding bodies folded into one, so the drawing cannot show who decides what.")
    return {
        "id": "15.17",
        "title": "Draw who holds power over each layer in one authority diagram.",
        "rule": [
            f"Our systems atlas records {words_n(len(AUTH))} authority connections. Each runs from a variable in the core layer "
            "that holds a body’s power, such as Congress’s ability to write and check policy, to a variable in the economy or "
            "technology layer that the body has the legal power to set. Draw all seven in one diagram: the layers stacked with "
            "a rule between each and its name, one pill for each variable, carrying the variable’s own title, and every line in "
            "the authority mark of Rule 15.5. Name each body beside the diagram as the atlas’s connections name it. Every "
            "line in it means the same verb, decides, so print the word once, in a key beside the diagram.",
            "Run the lines into each layer in lanes on one side of the column, nested so that none crosses another, and list "
            "each connection beside the diagram with its name. Then "
            f"a reader sees what no single line shows: {words_n(len(two))} of the four variables each answer to two bodies, "
            "and Congress and the executive each reach both layers.",
        ],
        "tokens": [TOKEN_LINE, "oa.color.border.strong"],
        "why": {"text": ["Power in the atlas is shared. Congress appropriates public investment and the executive administers it; "
                         "antitrust enforcers set rules for pricing software, and so do states and cities. One diagram keeps every "
                         "body apart and shows where their powers meet."],
                "basis": "Our systems atlas’s authority connections and model conventions"},
        "correct": {"specimen": "s-15-17-correct",
                    "caption": "The atlas’s seven authority connections in one diagram, from the powers of four bodies in the "
                               "core layer to four variables in the economy and technology layers, with each body and each "
                               "connection named beside it."},
        "failure": {"specimen": "s-15-17-failure",
                    "caption": "<strong>Fails Rule 15.17.</strong> One pill for the government stands in for four bodies, so the "
                               "drawing cannot say who decides what. The atlas records four apart: Congress, the executive, "
                               "antitrust enforcers, and state and local governments."},
        "specs": [
            {"label": "Layers", "value": "Stacked, with one 1 px rule between each two and both names beside it (Rule 15.9)"},
            {"label": "Bodies", "value": "One pill for the variable that holds each body’s power, in the core layer, carrying "
                                         "the variable’s own title; the body’s plain name beside the diagram, as the atlas’s "
                                         "connections give it"},
            {"label": "Lines", "value": "The authority mark of Rule 15.5: solid, an open diamond, no sign, with its delay ticks"},
            {"label": "Key", "value": "Two entries: decides, printed once because every line in the diagram means the same, "
                                      "and the delay ticks (Rule 13.5); each connection’s name beside the diagram says who "
                                      "decides what"},
            {"label": "Lanes", "value": f"Lines into the economy layer on the right and into the technology layer on the left, {LANE} px apart, nested so none crosses"},
            {"label": "Beside it", "value": "Each connection’s chip, name and grade word, grouped by the layer it reaches"},
        ],
        "related": ["13"],
        "builders": ["Read every authority connection from the atlas, check that each runs from the core layer and sits in no "
                     "loop, and stop the build if the count or any end changes."],
    }


def rule_15_18(book):
    """Worked example 6: Loop B2, a conceptual loop, with its missing chain printed beside its grade, and the atlas's
    other two conceptual loops named beside it (Master Brief section 14)."""
    b2, b3, r9 = LOOP["B2"], LOOP["B3"], LOOP["R9"]
    con = sorted(k for k, p in LOOP.items() if p["closure"].startswith("conceptual"))
    need(con == ["B2", "B3", "R9"], f"the atlas's conceptual loops changed: {con}")
    need(b2["closure"] == "conceptual: no complete numbered chain" and not b2["links"] and b2["type"] == "B"
         and b2["evidence"] == "well-supported", "Loop B2 changed")
    st = [lab for lab, _ in b2["chain_labels"]]
    sg = [s_ for _, s_ in b2["chain"]]
    need(st == ["Household hardship", "Automatic support (UI, credits)"] and sg == ["+", "-"], "Loop B2's stations changed")
    es = C13_sentences(b2["evidence_summary"])
    need(es == ["The model grades the mechanism well supported.",
                "Neither step is a numbered connection with its own citation, so the evidence cannot be inspected step by "
                "step, and that missing chain is the weakest point."], "Loop B2's evidence summary changed")
    how = b2["how_to_read"]
    rev = "the reverse of households' financial security"
    need(rev in how and how.endswith("neither arrow is a numbered connection."), "Loop B2's reading changed")
    need(node("A4")["title"] == "Households' financial security", "Variable A4 changed its title")
    others = {"B3": ("well-supported where entry is possible", "Its three variables sit outside the model's numbered variables "
                     "and none of its steps is a numbered connection, so the weakest point is the missing chain."),
              "R9": ("hypothesis", "The complete loop is a design hypothesis.")}
    for k, (g, s_) in others.items():
        need(LOOP[k]["evidence"] == g and s_ in LOOP[k]["evidence_summary"], f"Loop {k}'s grade or summary changed")
    b, h = drawn_loop(2, st, [{"sign": x, "hollow": True} for x in sg], numbered=False, inside=("B2", "balancing"), thin=True)
    miss = es[1]
    lab_ = (f'<div class="evr"><span class="ev">{e(GRADE["well-supported"][0])}</span><span class="gr">'
            f'{e(tie("the atlas’s grade for the mechanism; no numbered chain, which the atlas calls the weakest point"))}'
            f'</span></div>')
    # BC S16: the pill's "UI", spelled out in the atlas's own summary of the loop
    ui = ("benefits written into law", "expand without a new vote")
    need(b2["summary"].startswith(f"When a recession cuts earnings, {ui[0]}, such as unemployment insurance, {ui[1]}."),
         "Loop B2's summary no longer names unemployment insurance")
    o_items = [f'{chip("Loop", "B3")} “{e(b3["title"])}”. {grade_word("well-supported")}, where entry is possible. '
               f'No numbered chain: “{e(others["B3"][1])}”',
               f'{chip("Loop", "R9")} “{e(r9["title"])}”. {grade_word("hypothesis")}. “{e(others["R9"][1])}”']
    up, parts = True, []
    for lab, s_ in zip(st, sg):
        parts.append(("more " if up else "less ") + lab.split(" (")[0].lower())
        up = up if s_ == "+" else not up
    ra = ", ".join(parts) + ", and back to " + ("more " if up else "less ") + st[0].lower() + "."
    ra = ra[0].upper() + ra[1:]
    need(ra == "More household hardship, more automatic support, and back to less household hardship.", f"Loop B2 reads {ra!r}")
    words = (ra_p(ra)
             + f'<p class="k">The missing chain</p><p class="nt">The atlas: “{e(es[0])} {e(miss)}”</p>'
             + f'<p class="nt">Household hardship is “{e(rev)}”, which is {chip("Variable", "A4")} in the atlas’s model.</p>'
             + f'<p class="nt">In the pill, UI is unemployment insurance, which the atlas gives as its example of “{e(ui[0])}” '
               f'that “{e(ui[1])}”.</p>'
             )
    others_html = (f'<p class="k">The atlas’s other conceptual loops</p>'
                   f'<div class="two tw">{"".join(f"<p class={chr(34)}nt{chr(34)}>{x}</p>" for x in o_items)}</div>')
    body = (lab_ + beside(hed("Loop", "B2", b2["title"]) + fig(svg_wrap(b, h)), words)
            + f'<div class="kb">{others_html}</div>' + src("loop B2, loop B3 and loop R9"))
    book.add("s-15-18-correct", body, rule="15.18", readable=True, wide=True,
             alt=(f"Loop B2 from our systems atlas, “{b2['title']}”, under a label reading Well supported, the atlas’s grade "
                  "for the mechanism; no numbered chain, which the atlas calls the weakest point. Two thin pills, Household "
                  "hardship and Automatic support (UI, credits), joined by hollow lines: plus, raises, over the top, and minus, "
                  "lowers, under the bottom, with no step numbers. The loop reads: more household hardship, more automatic "
                  f"support, and back to less household hardship. Beside it, the atlas’s words: {es[0]} {miss} Household "
                  f"hardship is {rev}, which is Variable A4 in the atlas’s model. In the pill, UI is unemployment insurance, "
                  f"the atlas’s example of {ui[0]} that {ui[1]}. Then the atlas’s other conceptual loops: Loop B3, "
                  f"{b3['title']}, well supported where entry is possible, with no numbered chain; Loop R9, {r9['title']}, "
                  f"hypothesis: {others['R9'][1]}"),
             notes="Stations, signs, grade and the missing chain read from the loop's record; hollow lines and thin pills as "
                   "Rules 13.4 and 15.7 set.")
    book.log("15.18 correct", "Loop B2, automatic benefits", "D08")
    fail = (dnp() + diagram_label("well-supported", "strong research evidence") + hed("Loop", "B2", b2["title"])
            + fig(svg_wrap(b, h)))
    book.add("s-15-18-failure", fail, rule="15.18",
             alt=(FC + "Loop B2 drawn as before, hollow and thin, under a label that reads only Well supported, strong research "
                  "evidence, with no word that the loop has no numbered chain."),
             notes="Labeled failure: the grade printed alone, so it reads as the grade of steps that were never numbered.")
    return {
        "id": "15.18",
        "title": "Print a conceptual loop’s missing chain beside its grade.",
        "rule": [
            f"Loop B2, “{b2['title']}”, is one of our systems atlas’s {words_n(len(con))} conceptual loops. The atlas grades "
            "its mechanism well supported, and none of its steps is a numbered connection. Draw it as Rule 15.7 sets, with "
            "hollow lines between thin pills, and print in the label, right after the grade, that the loop has no numbered "
            "chain and that the atlas calls this its weakest point.",
            "Quote the atlas’s words on the missing chain beside the drawing, tie each station to a numbered variable where "
            "the atlas does, and name the atlas’s other conceptual loops, Loop B3 and Loop R9, with their grades.",
        ],
        "tokens": ["oa.chart.grade.conceptual.rail"],
        "why": {"text": ["A grade printed alone reads as the grade of each step. For a conceptual loop it belongs to the mechanism "
                         "as a whole, and no step carries a citation of its own, so a reader cannot check the loop one step "
                         "at a time."],
                "basis": "Our systems atlas, the record and evidence summary of Loop B2"},
        "correct": {"specimen": "s-15-18-correct",
                    "caption": "Loop B2 with its missing chain in the label beside its grade, the atlas’s words on it, and the "
                               "atlas’s other two conceptual loops named with their grades."},
        "failure": {"specimen": "s-15-18-failure",
                    "caption": "<strong>Fails Rule 15.18.</strong> The label gives the grade alone, so Well supported reads as "
                               "a checked chain of steps. The atlas grades the mechanism and calls the missing chain its "
                               "weakest point."},
        "specs": [
            {"label": "Label", "value": "The grade word, then “no numbered chain”, in one line"},
            {"label": "Drawing", "value": "Hollow lines with their signs, 1 px pills, no step numbers (Rule 15.7)"},
            {"label": "Beside it", "value": "The atlas’s words on the missing chain, quoted; a station tied to a numbered variable in its chip"},
            {"label": "The others", "value": f"Each conceptual loop named in its chip with its grade; {words_n(len(con))} as of the snapshot"},
        ],
        "related": ["13"],
        "builders": ["Read the closure and the evidence summary from the loop’s record, and stop the build if a conceptual "
                     "loop gains numbered connections or the summary changes."],
    }


# ===============================================================================================================
# The chapter
# ===============================================================================================================
# ===============================================================================================================
# Group 4. Interaction (round 4, November 13, 2026): Rules 15.19 to 15.21 under contracts R4-5 and R4-6, the data lead's
# ruling (f) (15.19 steps Loop R1, 15.20 offers Reforms R-03 and R-04 on Loop R4a, 15.21 draws Connection L55), the
# accessibility lead's "Interaction specification" and the component engineer's C-1 to C-3. 15.19 carries Rule 18.22's
# markup and no script: chapter 18's code plate wires every [data-oa-stepper] on the page and writes data-oa-live and
# data-oa-at on its root (C-1). 15.20's status line is the shell's (C-2), and the shell opens every closed details at
# print (C-3). 15.21 holds no control at all. Every failure plate is a still picture.
# ===============================================================================================================
CODE = ROOT / "work/build/guide/code"
BAND = "var(--oa-color-state-selected-band)"
MUTED = "var(--oa-color-state-muted-text)"
SHELL_CHOOSER_BYTES = 873     # the shell's status-line listener for 15.20 (C-2), counted toward R4-6's 75,000
R4_6 = 75_000
INTERACTION_BYTES = []       # filled by check(): fragments, rule entries, styles, the shell's listener, the sum
INTERACTION = ("15.19", "15.20", "15.21")


def code_part(name, pattern):
    """A piece of a chapter 18 code set, as its file writes it, whitespace closed up (C-1: 15.19 carries 18.22's markup)."""
    src = (CODE / name).read_text()
    m = re.search(pattern, src, re.S)
    need(m is not None, f"{name} no longer holds {pattern[:40]!r}")
    return sprite(re.sub(r"\s+", " ", m.group(0)).replace("> <", "><"))


def sprite(s):
    """A utility icon the page's sprite holds is drawn by <use>, so the page carries it once (the guide build's rule);
    the code set's own classes and data-icon stay on the svg, and a mirrored arrow keeps its transform on the use."""
    def one(m):
        tag, inner = m.group(1), m.group(2)
        ic = re.search(r'data-icon="U-([a-z-]+)"', tag)
        if not ic:
            return m.group(0)
        tr = re.search(r'transform="([^"]+)"', inner)
        use = f'<use href="#oa-sym-u-{ic.group(1)}-24px"{f" transform={chr(34)}{tr.group(1)}{chr(34)}" if tr else ""}/>'
        return f"{tag}{use}</svg>"
    return re.sub(r"(<svg\b[^>]*>)(.*?)</svg>", one, s, flags=re.S)


def plural(t):
    """Whether a title takes a plural verb: its head noun, the last word before a preposition, ends in a single s."""
    head = re.split(r"\s(?:in|to|of|for|on|from|with|over|toward|across|without)\s", t)[0].split()[-1].lower()
    return head.endswith("s") and not head.endswith("ss")


def stepper_steps(lid):
    """Each step of a loop as Rule 18.22's list holds it: the line (the variables' titles, the sign's verb, "can" for a
    plausible step), then every fact the drawing shows for that step (the accessibility lead's section 2): the typed
    connection and its name, what moves along it, its grade in Rule 13.3's word and its delay; the last step says the
    loop is back where it began and names its kind. The hold is 250 ms a word of what the status line says, never under
    6,000 ms (Rule 18.22, C-1)."""
    lp = LOOP[lid]
    codes = [c for c, _ in lp["chain"]]
    n = len(codes)
    out = []
    for i, x in enumerate(lp["links"]):
        l = link(x)
        need((l["from"], l["to"]) == (codes[i], codes[(i + 1) % n]), f"Loop {lid}'s step {i + 1} changed")
        a, b = short(codes[i]), short(codes[(i + 1) % n])
        up = l["polarity"] == "+"
        if l["evidence"] == "plausible":
            verb = "can raise" if up else "can lower"
        else:
            verb = ("raise" if up else "lower") if plural(a) else ("raises" if up else "lowers")
        line = f"{a} {verb} {lc(b)}."
        moves = f"{l['type']} moves along it, " if l["type"] in ("money", "information", "ownership") else ""
        least = ", the least certain step in the loop" if l["evidence"] == least_certain(lp["links"]) and len(
            {link(y)["evidence"] for y in lp["links"]}) > 1 else ""
        more = (f'{chip("Connection", x)} “{e(l["name"])}”: {moves}the atlas grades it '
                f'{GRADE[l["evidence"]][0].lower()}{least}, and its effect takes {DELAY[l["delay"]][1]}.')
        if i == n - 1:
            m_ = minus_count(lp["links"])
            signs = "no minus sign on any step" if m_ == 0 else f"{words_n(m_)} minus sign{'' if m_ == 1 else 's'} on its steps"
            more += f" The loop is back where it began, and with {signs} it is {'reinforcing' if m_ % 2 == 0 else 'balancing'}."
        said = f"Step {i + 1} of {n}: {line} {re.sub(r'<[^>]+>', '', more)}"
        hold = max(6000, 250 * len(said.split()))
        out.append((line, more, hold))
    return out


def stepper_keys(lid, n_steps):
    """Rule 15.19's keyboard path in oa-keys/1, as the accessibility lead's "Interaction specification" writes it (section
    2), with the loop's ID and step count; the guide check walks it in the stage at 1440 and 390 px."""
    n = n_steps
    sl = ".oa-stepper-status"
    return {"format": "oa-keys/1", "set": "s-15-19-correct", "rule": "15.19", "component": "Loop stepper on a systems drawing",
            "paths": [
                {"name": "Step by hand; the line says each step, the drawing follows, and no button moves focus",
                 "steps": [
                     {"key": "Tab", "focus": ".oa-stepper-play"},
                     {"key": "Tab", "focus": ".oa-stepper-reset", "states": [{"el": ".oa-stepper-reset", "attr": "aria-disabled", "is": "true"}]},
                     {"key": "Tab", "focus": ".oa-stepper-prev", "states": [{"el": ".oa-stepper-prev", "attr": "aria-disabled", "is": "true"}]},
                     {"key": "Tab", "focus": ".oa-stepper-next"},
                     {"key": "Enter", "focus": ".oa-stepper-next", "states": [{"el": ".oa-stepper-step:nth-child(1)", "attr": "aria-current", "is": "step"},
                                                                              {"el": "[data-oa-stepper]", "attr": "data-oa-at", "is": "1"}],
                      "status_has": f"Step 1 of {n}:", "status_el": sl},
                     {"key": "Enter", "focus": ".oa-stepper-next", "status_has": f"Step 2 of {n}:", "status_el": sl},
                     {"key": "Shift+Tab", "focus": ".oa-stepper-prev", "states": [{"el": ".oa-stepper-prev", "attr": "aria-disabled", "is": None}]},
                     {"key": "Enter", "focus": ".oa-stepper-prev", "status_has": f"Step 1 of {n}:", "status_el": sl},
                     {"key": "Shift+Tab", "focus": ".oa-stepper-reset"},
                     {"key": "Enter", "focus": ".oa-stepper-reset", "states": [{"el": ".oa-stepper-reset", "attr": "aria-disabled", "is": "true"},
                                                                               {"el": "[data-oa-stepper]", "attr": "data-oa-at", "is": "0"}],
                      "status_has": "Ready.", "status_el": sl},
                     {"key": "Tab", "focus": ".oa-stepper-prev"},
                     {"key": "Tab", "focus": ".oa-stepper-next"},
                     {"key": "Tab", "focus": "outside"}]},
                {"name": "Play becomes Pause and back, with focus on it, under reduced motion too",
                 "setup": {"reducedMotion": True},
                 "steps": [
                     {"key": "Tab", "focus": ".oa-stepper-play", "states": [{"el": ".oa-stepper-word", "text": "Play"}]},
                     {"key": "Enter", "focus": ".oa-stepper-play", "states": [{"el": ".oa-stepper-word", "text": "Pause"}],
                      "status_has": f"Step 1 of {n}:", "status_el": sl},
                     {"key": "Enter", "focus": ".oa-stepper-play", "states": [{"el": ".oa-stepper-word", "text": "Play"}]}]}]}


def chooser_keys(rids):
    """Rule 15.20's keyboard path in oa-keys/1, the accessibility lead's section 3 with the ruled reforms: Tab enters at
    the checked reform, the arrow keys choose and wrap, the panel and the status line follow, focus stays, the chosen
    panel's disclosure keeps its own state."""
    a, b_ = rids[0], rids[1]
    inp = lambda r: f'.oa-choice-input[value="{r}"]'
    pan = lambda r: f'[data-oa-panel="{r}"]'
    say = lambda r: f"Reform {r} acts where the marks turn red"
    wrap_ = rids[2] if len(rids) > 2 else a      # with two reforms, ArrowDown from the second wraps to the first
    return {"format": "oa-keys/1", "set": "s-15-20-correct", "rule": "15.20", "component": "Reform chooser on a systems drawing",
            "paths": [
                {"name": "Enter at the checked reform; the arrow keys choose, the panel and the line follow, and focus stays",
                 "steps": [
                     {"key": "Tab", "focus": inp(a), "states": [{"el": inp(a), "prop": "checked", "is": True},
                                                                {"el": pan(a), "visible": True}, {"el": pan(b_), "visible": False}]},
                     {"key": "ArrowDown", "focus": inp(b_), "states": [{"el": inp(b_), "prop": "checked", "is": True},
                                                                       {"el": pan(b_), "visible": True}, {"el": pan(a), "visible": False}],
                      "status_has": say(b_)},
                     {"key": "ArrowDown", "focus": inp(wrap_), "status_has": say(wrap_)},
                     {"key": "ArrowUp", "focus": inp(b_), "status_has": say(b_)},
                     {"key": "Tab", "focus": f"{pan(b_)} summary", "states": [{"el": f"{pan(b_)} details", "prop": "open", "is": False}]},
                     {"key": "Enter", "focus": f"{pan(b_)} summary", "states": [{"el": f"{pan(b_)} details", "prop": "open", "is": True}]},
                     {"key": "Shift+Tab", "focus": inp(b_)},
                     {"key": "ArrowUp", "focus": inp(a), "states": [{"el": f"{pan(b_)} details", "prop": "open", "is": True}]},
                     {"key": "Tab", "focus": f"{pan(a)} summary"},
                     {"key": "Tab", "focus": "outside"}]}]}


def rule_15_19(book):
    """Rule 15.19: the loop stepper on Loop R1 (ruling (f)), built on Rule 18.22's component and code, never a second copy."""
    lid = "R1"
    lp = LOOP[lid]
    codes = [c for c, _ in lp["chain"]]
    need(codes == ["A1", "B1", "E1"] and lp["links"] == ["L01", "L02", "L03"] and lp["type"] == "R"
         and lp["evidence"] == "plausible", "Loop R1 changed")
    need([link(x)["evidence"] for x in lp["links"]] == ["well-supported", "plausible", "well-supported"]
         and [link(x)["delay"] for x in lp["links"]] == ["S", "M", "L"], "Loop R1's grades or delays changed")
    qual = lp["qualification"]
    need(qual.startswith("The loop runs on issues where wealthy donors"), "Loop R1's qualification changed")
    steps = stepper_steps(lid)
    # C-1: the controls and the reason line as the code set writes them; the group names this loop
    ctl = code_part("c-18-loop-stepper.html", r'<div\s+class="oa-stepper-controls".*?</button>\s*</div>')
    ctl = ctl.replace('aria-label="Steps of the loop"', f'aria-label="Steps of Loop {lid}"')
    why = code_part("c-18-loop-stepper.html", r'<p class="oa-stepper-why".*?</p>')
    need('id="oa-stepper-why"' in why and ctl.count('aria-describedby="oa-stepper-why"') == 2,
         "Rule 18.22's reason line and the two buttons that name it changed")
    ready = (f"Ready. Start at {lc(short(codes[0]))}, and suppose it rises. Press Play, or Next step to follow one "
             "connection at a time.")
    body, h = three_loop(codes, lp["links"], weakest=1, inside=(lid, "reinforcing"), steps_g=True)
    # &#32; keeps the space between the line and its more words, which the plate minifier would close up
    lis = "".join(f'<li class="oa-stepper-step" data-oa-hold="{hd}"><span class="oa-stepper-line">{e(ln)}</span>&#32;'
                  f'<span class="oa-stepper-more">{mo}</span></li>' for ln, mo, hd in steps)
    right = (f'<p class="oa-stepper-status" role="status" data-oa-ready="{e(ready)}">{e(ready)}</p>'
             f'<ol class="oa-stepper-steps" role="list">{lis}</ol>{ctl}{why}'
             f'<p class="nt">The atlas’s limit on the loop: “{e(qual)}”</p>'
             + src("loop R1 and connections L01, L02 and L03"))
    root = (f'<div class="oa-stepper lv" data-oa-stepper>'
            + label_for(lp["links"], "the grade of the loop’s least certain step")
            + beside(hed("Loop", lid, lp["title"]) + f'<div class="dw">{svg_wrap(body, h)}</div>', right) + "</div>")
    book.keys["s-15-19-correct"] = stepper_keys(lid, n_steps=len(steps))
    book.add("s-15-19-correct", root, rule="15.19", wide=True, interactive=True,
             alt=(f"Loop R1 from our systems atlas, “{lp['title']}”, drawn as three pills with its steps numbered 1 to 3, "
                  "beside the loop stepper of Rule 18.22: a status line, the three steps in order, and four buttons, Play, "
                  "Reset the loop, Previous step and Next step. The current step lights in the drawing and in the list. "
                  "With scripts off or in print, the list shows every step in order."),
             notes="Rule 18.22's markup with no script of its own (C-1); its controls and reason line read from "
                   "work/build/guide/code/c-18-loop-stepper.html; the drawing follows data-oa-at through the chapter's "
                   "block; every word of the steps read from the atlas's loop and connection records.")
    book.log("15.19 correct", "Loop R1, wealth and political influence", "D03")
    # the failure: a still picture of a player that shows one step at a time and nothing else
    fb, fh = three_loop(codes, lp["links"], numbered=False, only={1})
    play = code_part("c-18-loop-stepper.html", r'<svg\s+class="oa-stepper-icon oa-stepper-icon--play".*?</svg>')
    play = re.sub(r'\sclass="[^"]*"', ' class="pi"', play, count=1)
    fail = (dnp() + hed("Loop", lid, lp["title"]) + fig(svg_wrap(fb, fh))
            + f'<div class="pb"><span class="ib">{play}</span><p class="nt">Playing. A play button with no word on it, '
              'and nothing else: the step list, the numbers and Pause are missing.</p></div>')
    book.add("s-15-19-failure", fail, rule="15.19",
             alt=(FC + "A picture of a player on Loop R1 that draws one step at a time: only the middle step shows, with no "
                  "number, and the pills it does not join stand alone. Under it, a square button with a play icon and no "
                  "word, and the word Playing. There is no step list, no Pause and no Reset."),
             notes="Labeled failure, drawn as a still picture: no control, no script.")
    n = len(steps)
    return {
        "id": "15.19",
        "title": "Step a reader through a loop one connection at a time, with a still sequence.",
        "rule": [
            "Let a reader move through a loop one connection at a time, in the loop’s own order, with Play, Pause, Reset the "
            "loop, Previous step and Next step, since a loop read all at once asks a reader to hold every step in mind. "
            "Use the loop stepper of Rule 18.22, its markup and its code, and set the drawing beside it so the current step "
            "lights in both.",
            "Each step’s words say everything the drawing shows for it: the two variables by their own titles, which way the "
            "change runs, what moves along the connection, its grade and its delay. Number every step, and print the whole "
            "sequence in order wherever nothing can move: on paper, with motion reduced and with scripts off.",
        ],
        "tokens": ["oa.color.state.selected.band", "oa.color.state.selected.bar", "oa.color.state.muted.text"],
        "why": {"text": ["A stepper adds the loop’s order to the shape its drawing shows. When a reader takes the loop one "
                         "connection at a time, the weakest step stands out where it falls, and the reader sees why the "
                         "loop’s grade is that step’s grade (Rule 15.13). The still sequence keeps the same reading for a reader who "
                         "cannot or will not run it."],
                "basis": "Our systems atlas, Loop R1; the stepper and still-sequence lessons of LOOPY, as Rule 18.22 sets them"},
        "correct": {"specimen": "s-15-19-correct",
                    "caption": f"Loop R1, where {lc(lp['title'])}, on the loop stepper of Rule 18.22, live: {words_n(n)} numbered "
                               "steps, each with its connection, grade and delay. The current step lights in the drawing "
                               "and in the list; on paper and with scripts off the list shows every step in order."},
        "failure": {"specimen": "s-15-19-failure",
                    "caption": "<strong>Fails Rule 15.19.</strong> The player shows one step at a time and nothing else: no "
                               "numbers, no list and no way to pause, so on paper, with motion reduced or with scripts off "
                               "a reader sees one connection of three."},
        "specs": [
            {"label": "Component", "value": "The loop stepper of Rule 18.22: its markup, its styles and its script, once on the page"},
            {"label": "Current step", "value": "The selected band behind its line and its two pills, the list’s band and bar beside it, in ink, never in red",
             "token": "oa.color.state.selected.band"},
            {"label": "Steps ahead", "value": "Muted, each line keeping its grade’s pattern", "token": "oa.color.state.muted.text"},
            {"label": "Step words", "value": "The variables’ titles and the sign’s verb, then the connection, what moves along it, its grade and its delay"},
            {"label": "Still sequence", "value": "Every step numbered and in ink, buttons hidden, on paper, with motion reduced and with scripts off"},
        ],
        "related": ["13", "17", "18"],
        "builders": ["Carry Rule 18.22’s markup and let chapter 18’s script run it; never copy the script. Light the drawing "
                     "from the stepper’s <code>data-oa-at</code>, and number the steps with a CSS counter, never inside the "
                     "line the status reads."],
    }


def chooser_targets(rids, lp):
    """Each offered reform's targets, held to Loop R4a and to the atlas's two lists (ruling (f)): every target a variable or
    connection of the loop, and the loop and the reform naming each other."""
    codes = {c for c, _ in lp["chain"]} | set(lp["links"])
    for rid in rids:
        need(set(REFORM[rid]["targets"]) <= codes and rid in lp["reforms"] and lp["id"] in REFORM[rid]["loops"],
             f"reform {rid} no longer acts wholly on Loop {lp['id']}, or the two lists disagree")
    need(sorted(lp["reforms"]) == sorted(rids), f"Loop {lp['id']} lists other reforms: {lp['reforms']}")
    owner = {}
    for rid in rids:
        for t_ in REFORM[rid]["targets"]:
            owner.setdefault(t_, []).append(rid)
    return {k: " ".join(v) for k, v in owner.items()}


def chooser_css(rids):
    """15.20's choice through CSS from the checked radio (the accessibility lead's section 3), so it works with scripts
    off: the chosen reform's panel shows and its targets turn red; the first reform's are red in the markup."""
    out = []
    for rid in rids[1:]:
        has = f'.p:has([value="{rid}"]:checked)'
        no, yes = f'{has} [data-oa-for]:not([data-oa-for~="{rid}"])', f'{has} [data-oa-for~="{rid}"]'
        # the chosen reform's targets take Rule 12.5's red (the lit marks, a 4 px red line on a 6 px ink case, red head,
        # a 3 px red outline), as the class rt and rp draw the first reform's in the markup; the others go back to ink
        out.append(f'{no} .hi,{yes} .lo{{display:none}}{no} .lo,{yes} .hi{{display:inline}}'
                   f'{no} .pl{{stroke:{INK};stroke-width:2px}}{no} .ak-mark{{stroke:{INK};stroke-width:2px}}{no} .hd{{fill:{INK}}}'
                   f'{yes} .ak-mark{{stroke:var(--oa-color-data-emphasis-red);stroke-width:4px}}'
                   f'{yes} .ak-case{{fill:none;stroke:{INK};stroke-width:6px}}{yes} .hd{{fill:var(--oa-color-data-emphasis-red)}}'
                   f'{yes} .pl{{stroke:var(--oa-color-data-emphasis-red);stroke-width:3px}}')
    # the chosen panel alone shows, with no rule or space above it where another panel stood before it
    shows = "".join(f'.p:has([value="{rid}"]:checked) [data-oa-panel]:not([data-oa-panel="{rid}"]){{display:none}}'
                    f'.p:has([value="{rid}"]:checked) [data-oa-panel="{rid}"]{{margin:0;padding:0;border:0}}' for rid in rids)
    prints = "".join(f'.p:has([value="{rid}"]:checked) [data-oa-print="{rid}"]' + ("," if k < len(rids) - 1 else "")
                     for k, rid in enumerate(rids))
    return (f"@supports selector(:has(*)){{{''.join(out)}@media screen{{{shows}}}"
            f"@media print{{{prints}{{display:block}}}}}}")


def rule_15_20(book):
    """Rule 15.20: the reform chooser on Loop R4a with Reforms R-03 and R-04, the only loop where every reform the atlas
    places on it acts wholly on it and both its lists agree (ruling (f))."""
    rids = ["R-03", "R-04"]
    lp = LOOP["R4a"]
    codes = [c for c, _ in lp["chain"]]
    need(codes == ["C4", "C1", "D7"] and lp["links"] == ["L42", "L55", "L56"], "Loop R4a changed")
    rs = [reform("R-03", ["L42", "C1", "D7"], ["R4a", "R10", "R12"], "rules", "documented", "plausible"),
          reform("R-04", ["L42", "L56"], ["R4a"], "power to change the rules", "documented", "plausible")]
    need([r_["effects"] for r_ in rs] == [{"DQ": "+L", "GE": "?", "EP": "0", "EQ": "+S"},
                                         {"DQ": "+M", "GE": "0", "EP": "0", "EQ": "0"}], "the reforms' effects changed")
    need(all(not x["checked"] for r_ in rs for x in r_["routes"]), "a route of R-03 or R-04 now carries a check date")
    owner = chooser_targets(rids, lp)
    need(REFORM["R-04"]["title"] == "Independent citizen commissions draw election maps", "R-04's title changed; reread the caption")
    check_ = code_part("c-18-choice.html", r'<svg\s+class="oa-choice-check".*?</svg>')
    chev = code_part("c-18-disclosure.html", r'<svg\s+class="oa-disclosure-chevron".*?</svg>')
    items = "".join(
        f'<label class="oa-choice-item"><input class="oa-choice-input" type="radio" name="s-15-20-reform" value="{rid}"'
        f'{" checked" if k == 0 else ""}><span class="oa-choice-face">{check_}<span class="oa-choice-label">'
        f'{chip("Reform", rid)} “{e(REFORM[rid]["title"])}”</span></span></label>' for k, rid in enumerate(rids))
    group = (f'<fieldset class="oa-choice"><legend class="oa-choice-legend">Show one reform on Loop R4a</legend>'
             f'<div class="oa-choice-row ch1">{items}</div></fieldset><p class="vh" role="status" data-oa-chooser-status></p>')
    tg = set(rs[0]["targets"])
    lit = {t_ for r_ in rs for t_ in r_["targets"] if t_ in LINK}
    b, h = three_loop(codes, lp["links"], inside=("R4a", "reinforcing"), targets=tg, lit=lit, for_=owner)
    drawn = set(codes) | set(lp["links"])
    panels = []
    for r_ in rs:
        rid = r_["id"]
        n_l = sum(1 for t_ in r_["targets"] if t_ in LINK)
        n_v = len(r_["targets"]) - n_l
        parts = [f"{words_n(n_l)} connection{'s' if n_l != 1 else ''}" if n_l else "",
                 f"{words_n(n_v)} variable{'s' if n_v != 1 else ''}" if n_v else ""]
        rem = r_["remedy_evidence"]
        disc = (f'<div class="oa-disclosure-set"><div class="oa-disclosure-stack"><details class="oa-disclosure">'
                f'<summary class="oa-disclosure-summary"><span class="oa-disclosure-label">The atlas’s qualifications and '
                f'assumptions for {chip("Reform", rid)}</span>{chev}</summary><div class="oa-disclosure-body">'
                f'<p>Its confidence in the effects: “{e(r_["effects_confidence"])}”.</p>'
                f'<p>The evidence for the remedy, {e(GRADE[rem["grade"]][0].lower())}: “{e(rem["text"])}”</p>'
                f'<p>Its tradeoffs: “{e(r_["tradeoffs"])}”</p></div></details></div></div>')
        panels.append(
            f'<div class="pn" data-oa-panel="{rid}"><p class="nt" data-oa-say>{chip("Reform", rid)} acts where the marks '
            f'turn red: on {" and ".join(p_ for p_ in parts if p_)}.</p>'
            f'<p class="k">Its targets</p>{kw(target_items(r_, drawn))}<p class="k">Its band</p>{band_p(r_)}'
            f'<p class="k">Effects by outcome family, as of {SNAP}</p>{effect_rows(r_)}'
            f'<p class="k">Routes, with the date each was checked</p>{route_rows(r_)}{disc}</div>')
    prints = "".join(f'<p class="nt pon" data-oa-print="{rid}">The drawing shows {chip("Reform", rid)} in red.</p>' for rid in rids)
    left = hed("Loop", "R4a", lp["title"]) + f'<div class="dw">{svg_wrap(b, h)}</div>{prints}' + step_lines(lp["links"])
    root = (f'<div class="lv" data-oa-chooser>{group}' + label_for(lp["links"], "the grade of the loop’s least certain step")
            + beside(left, "".join(panels)) + src("reforms R-03 and R-04, their targets, effects, routes and evidence, and "
                                                   "loop R4a with its connections") + "</div>")
    book.keys["s-15-20-correct"] = chooser_keys(rids)
    book.add("s-15-20-correct", root, rule="15.20", wide=True, interactive=True,
             alt=("A reform chooser on Loop R4a from our systems atlas: a group of two radio buttons, Reform R-03 and Reform "
                  "R-04, with R-03 chosen; the loop drawn as three pills with the chosen reform’s targets in red; and the "
                  "chosen reform’s panel with its targets, its band, its four effects one family to a row as of "
                  f"{SNAP}, its routes, each not checked, and its qualifications and assumptions one step away in a "
                  "disclosure."),
             notes="Rule 18.3's choice and Rule 18.8's disclosure as their code sets write them; the choice shows through "
                   "the chapter's block from the checked radio, scripts on or off; the status line is the shell's (C-2). "
                   "Every value read from the atlas's reform and loop records.")
    book.log("15.20 correct", "Reforms R-03 and R-04 on Loop R4a, district maps", "D02")
    # the failure: both reforms lit at once, their effects added into one score, the qualifications gone
    fb, fh = three_loop(codes, lp["links"], inside=("R4a", "reinforcing"), targets=set(owner))
    boxes = "".join(f'<li><span class="xb" aria-hidden="true">{check_.replace("oa-choice-check", "ck")}</span>'
                    f'{chip("Reform", rid)} “{e(REFORM[rid]["title"])}”</li>' for rid in rids)
    fail = (dnp() + f'<ul class="kw xk">{boxes}</ul>' + hed("Loop", "R4a", lp["title"]) + fig(svg_wrap(fb, fh))
            + '<p class="nt"><b>Combined effect on democracy: +L</b></p>')
    book.add("s-15-20-failure", fail, rule="15.20",
             alt=(FC + "A picture of a chooser with two boxes, Reform R-03 and Reform R-04, both checked, over Loop R4a "
                  "with every target of both in red, so no mark says whose it is. Under it a line reads Combined effect "
                  "on democracy: +L. No qualification or assumption appears."),
             notes="Labeled failure, drawn as a still picture: no control. Its combined score is the fault and holds no "
                   "atlas value: the atlas never adds reform effects.")
    return {
        "id": "15.20",
        "title": "Let a reader choose a reform and see its targets, effects and assumptions.",
        "rule": [
            "Offer the reforms that act on one drawing as a named group of radio buttons (Rule 18.3), so a reader chooses "
            "one at a time. The chosen reform’s exact targets turn red on the drawing (Rule 15.11), and its panel lists its "
            "targets, its band, its four effects apart in the atlas’s codes with their date (Rule 15.16) and its routes, "
            "each with its check date or “Not checked”.",
            "Keep the atlas’s qualifications and assumptions one step away, in a disclosure under the panel (Rule 18.8), "
            "and never light two reforms at once or add their effects. Offer only reforms whose every target sits on the "
            "drawing, so nothing lights for a reform that does not act there.",
        ],
        "tokens": ["oa.color.data.emphasis.red"],
        "why": {"text": ["A reader comparing reforms wants to see where each one acts and what the atlas expects of it. One "
                         "choice at a time keeps each reform’s red its own, and the effects stay the atlas’s four ordinal "
                         "codes. The assumptions sit one step away, where a reader who asks finds "
                         "them whole."],
                "basis": "Our systems atlas, Reforms R-03 and R-04 on Loop R4a; the choice lessons of En-ROADS, as Rules 18.3 and 18.8 set them"},
        "correct": {"specimen": "s-15-20-correct",
                    "caption": f"Reform R-03, {lc(REFORM['R-03']['title'])}, and Reform R-04, independent citizen commissions "
                               f"that draw election maps, on Loop R4a, where {lc(lp['title'])}, live: choose one and its targets turn red, with its "
                               "effects and routes beside the drawing and its qualifications one step away."},
        "failure": {"specimen": "s-15-20-failure",
                    "caption": "<strong>Fails Rule 15.20.</strong> Both reforms light at once, so no red says whose target it "
                               "is, and a combined score adds effects our systems atlas never adds. The qualifications are gone."},
        "specs": [
            {"label": "Choice", "value": "A named group of radio buttons, two to five reforms, the first chosen on load (Rule 18.3)"},
            {"label": "Targets", "value": "The chosen reform’s alone, in Rule 12.5’s red, with each named in a typed chip",
             "token": "oa.color.data.emphasis.red"},
            {"label": "Effects", "value": "Four rows, one outcome family each, in the atlas’s codes with their date; never added"},
            {"label": "Assumptions", "value": "In a disclosure under the panel, closed on load, open on paper (Rule 18.8)"},
            {"label": "Status line", "value": "One sentence on each change, hidden from sight, never on load"},
        ],
        "related": ["13", "18"],
        "builders": ["Show the chosen panel and light its targets from the checked radio with CSS, so the choice works with "
                     "scripts off; let the shell’s listener write the status line from the panel’s first line."],
    }


def rule_15_21(book):
    """Rule 15.21: Connection L55 with what the model holds for it, against a still picture of a slider for a strength the
    model does not hold (ruling (f)'s recommendation; R4-5: no control in either plate)."""
    l = link("L55")
    need((l["from"], l["to"], l["polarity"], l["evidence"], l["delay"], l["contested"]) == ("C1", "D7", "+", "plausible", "M", False),
         "connection L55 changed")
    num = [k for k, v in l.items() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    need(not num, f"connection L55 now holds a number: {num}")
    q = l["qualification"]
    need(q.endswith("relies on seats-votes analysis with no single estimate in this model."), "L55's qualification changed")
    limits = V7["methods"]["limits"]
    lq = "no whole loop has a measured strength."
    need(lq in limits and "the size of any effect comes from the studies attached to each connection" in limits,
         "the atlas's limits no longer say an effect's size comes from the studies and no loop has a measured strength")
    fb, fh, _ = card("C1", "D7", "L55")
    ladder = lambda opts, on: ('<ol class="ld">' + "".join(
        f'<li{" class=\"on\"" if o == on else ""}>{e(o)}</li>' for o in opts) + "</ol>")
    grades = [GRADE[g][0] for g in ("documented", "well-supported", "plausible", "plausible_contested", "hypothesis")]
    delays = [DELAY[k][1].capitalize() for k in ("S", "M", "L")]
    words = (f'<p class="nt">{gl("L55")}</p><p class="k">Sign</p><p class="nt"><b>Plus, raises</b>: “{e(l["sign_meaning"])}”</p>'
             f'<p class="k">Grade, on the atlas’s ladder</p>{ladder(grades, GRADE["plausible"][0])}'
             f'<p class="k">Delay, in the atlas’s three classes</p>{ladder(delays, DELAY["M"][1].capitalize())}'
             f'<p class="k">Strength</p><p class="nt">None in the model. The atlas’s record for the connection: “{e(q)}”</p>'
             + src("connection L55 and the model’s limits"))
    body = (label_for(["L55"], "the grade of the connection drawn")
            + beside(fig(svg_wrap(fb, fh)), words))
    book.add("s-15-21-correct", body, rule="15.21", readable=True, wide=True,
             alt=(f"Connection L55 from our systems atlas, “{l['name']}”, drawn from {lc(short('C1'))} down to "
                  f"{lc(short('D7'))}, dashed for plausible, with two delay ticks, a plus tag and the word raises. Beside it, "
                  "what the model holds for it, each on the atlas’s own steps: its sign, plus, with the atlas’s sentence; its "
                  "grade, plausible, marked on the ladder of five grades; its delay, 2 to 10 years, marked among three "
                  f"classes; and its strength, none in the model, with the atlas’s words: {q}"),
             notes="Every value read from the connection's record; the build stops if the record ever holds a number.")
    book.log("15.21 correct", "Connection L55, safe seats and entrenched control", "D02")
    # the failure: a still picture of a slider for a strength the atlas does not hold; its value is the picture's own
    sl = ('<svg class="sv" viewBox="0 0 296 74" width="296" height="74" aria-hidden="true" focusable="false">'
          '<text class="t" x="0" y="14">Strength of this connection</text>'
          '<path class="ak-mark" d="M8 40H288" stroke-width="2"/><path class="ak-mark" d="M8 40H204" stroke-width="6"/>'
          '<circle class="pl" cx="204" cy="40" r="10"/><text class="v" x="8" y="68">0</text>'
          '<text class="v" x="288" y="68" text-anchor="end">100</text><text class="t" x="204" y="68" text-anchor="middle">70</text></svg>')
    fail = (dnp() + fig(svg_wrap(fb, fh)) + f'<div class="dg">{sl}</div>'
            + '<p class="nt">The value 70 is this picture’s own; the atlas holds no such figure.</p>')
    book.add("s-15-21-failure", fail, rule="15.21",
             alt=(FC + "Connection L55 drawn as on the correct plate, and under it a picture of a slider labeled Strength of "
                  "this connection, running from 0 to 100, its handle set at 70. A note says the value 70 is the picture’s "
                  "own and the atlas holds no such figure. It is a picture, not a control."),
             notes="Labeled failure, drawn in SVG as a still picture: no input, no slider role, no Tab stop.")
    return {
        "id": "15.21",
        "title": "Give every control the model’s own steps, and no slider for a strength.",
        "rule": [
            "A control may offer only what the model holds: its loops and their steps, its reforms, Rule 13.3’s grade words, "
            "the three delay classes and the four ordinal effect codes. Each is a set of named steps, so build it from the "
            "stepper, the radio group or the disclosure.",
            "Leave totals, odds, amounts and strengths out of every control, and with them sliders, dials and fields for a "
            "number, because our systems atlas leaves the size of any effect to the studies behind each connection and says "
            f"that “{lq}” A slider set between 0 and 100 would hand a reader a figure no study supports.",
        ],
        "tokens": [TOKEN_LINE],
        "why": {"text": ["A slider promises that any value along it means something and that moving it changes the outcome "
                         "by that much. The atlas grades its connections in words and codes its effects in ordinal steps, so "
                         "the honest control offers those steps alone."],
                "basis": "Our systems atlas, Connection L55 and the model’s limits"},
        "correct": {"specimen": "s-15-21-correct",
                    "caption": f"Connection L55, “{l['name']}”, with what our systems atlas holds for it, each on the model’s own steps: its "
                               "sign, its grade on the ladder, its delay class, and no strength."},
        "failure": {"specimen": "s-15-21-failure",
                    "caption": "<strong>Fails Rule 15.21.</strong> A slider sets the connection’s strength at 70 of 100, a "
                               "figure our systems atlas does not hold. A line under the slider says the picture made the value up."},
        "specs": [
            {"label": "Steps a control may offer", "value": "Loops and their steps, reforms, grade words, delay classes and ordinal effect codes"},
            {"label": "Never offered", "value": "A total, odds, an amount or a strength, whether by slider, dial or number field"},
            {"label": "A picture of a control", "value": "Drawn, not built, with its alt saying it is a picture"},
        ],
        "related": ["13", "18"],
        "builders": ["Stop the build if a plate or a control prints a number the model’s record does not hold."],
    }


def stepper_css(n):
    """Rule 15.19's drawing follows the stepper's data-oa-at (C-1): the steps before the current one in ink, the current
    one on the selected band with its words bold, the steps ahead and the variables not yet reached muted, each line
    keeping its grade's pattern; at the start, the first variable on the band. No red (ruling (f))."""
    out = []
    for k in range(n + 1):
        s_ = f'[data-oa-at="{k}"]'
        lit = {0} if k == 0 else {k - 1, k % n}
        mute = [f'{s_} [data-s="{i}"]' for i in range(k + 1, n + 1)] + [f'{s_} [data-p="{j}"]' for j in range(n) if j > k and j not in lit]
        if mute:
            out.append(",".join(mute) + f"{{--k:{MUTED};--t:{MUTED}}}")
        out.append(",".join(f'{s_} [data-p="{j}"]' for j in sorted(lit)) + f"{{--f:{BAND}}}")
        if k:
            out.append(f'{s_} [data-s="{k}"] .bd{{display:inline}}{s_} [data-s="{k}"] text{{font-weight:var(--oa-font-weight-bold)}}')
    return "".join(out)


CSS.update({
    # AX section 1: a live plate's words and controls take the reader's forced colors on a ground of their own, and the
    # drawing keeps its own colors on its own ground
    "lv": (".lv{forced-color-adjust:auto;background:var(--oa-color-surface)}"
           # the effect pips and the record square sit in a live plate's words: with forced colors they keep their shape
           # and take the reader's text color through currentColor, as the words beside them do
           ".lv :is(.pp,.rs){forced-color-adjust:none;fill:currentColor}.lv .pp .z{stroke:currentColor}"
           ".dw{forced-color-adjust:none;background:var(--oa-color-surface)}.lv>.oa-choice{margin:0 0 16px}"),
    "dw": (f".dw{{--k:{INK};--t:var(--oa-color-text-primary);--f:var(--oa-color-surface)}}"
           ".dw .ak-mark,.dw .tk{stroke:var(--k)}.dw .hd,.dw .tg polygon{fill:var(--k)}.dw text{fill:var(--t)}"
           ".dw .pl{stroke:var(--k);fill:var(--f)}.dw .ak-case{fill:none;stroke:none}"
           f".dw .bd{{display:none;fill:none;stroke:{BAND};stroke-width:14px;stroke-linecap:round}}" + stepper_css(3)
           # C-1: scripts off, the buttons and the two lines that speak of them stay hidden; the still sequence shows
           + "[data-oa-stepper]:not([data-oa-live]) :is(.oa-stepper-controls,.oa-stepper-status,.oa-stepper-why){display:none}"
           ".oa-stepper-steps{counter-reset:st}.oa-stepper-step::before{counter-increment:st;content:counter(st);"
           "margin-right:8px;font-weight:var(--oa-font-weight-bold)}"
           # AX section 2, print: the still sequence, whatever state the reader left
           "@media print{.p .oa-stepper :is(.oa-stepper-controls,.oa-stepper-status,.oa-stepper-why){display:none}"
           ".p .oa-stepper .oa-stepper-step{background:none;border-left-color:transparent;color:inherit}"
           f".p .oa-stepper .dw :is([data-s],[data-p]){{--k:{INK};--t:var(--oa-color-text-primary);--f:var(--oa-color-surface)}}"
           ".p .oa-stepper .dw .bd{display:none}.p .oa-stepper .dw [data-s] text{font-weight:var(--oa-font-weight-regular)}}"),
    "ch1": ".ch1{flex-direction:column;align-items:flex-start}" + chooser_css(["R-03", "R-04"]),
    "pn": (".pn+.pn{margin-top:24px;padding-top:16px;border-top:1px solid var(--oa-color-border-hairline)}.pn>*+.k{margin-top:16px}"
           ".pn .oa-disclosure-set{margin-top:16px}@media print{.lv>.oa-choice{display:none}}"),
    "pon": ".pon{display:none}",
    "ld": (".ld{list-style:none;margin:4px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:4px 14px;font:var(--oa-type-body-small);"
           "color:var(--oa-color-text-secondary)}.ld .on{color:var(--oa-color-text-primary);font-weight:var(--oa-font-weight-bold);"
           "border-bottom:2px solid var(--oa-color-border-strong)}"),
    "pb": (".pb{display:flex;gap:12px;align-items:center;margin-top:12px}"
           ".ib{display:inline-grid;place-items:center;flex:none;width:44px;height:44px;border:1px solid var(--oa-color-border-strong)}"
           ".ib svg,.xb svg{fill:none;stroke:currentColor;stroke-width:var(--oa-component-icon-utility-line-medium);"
           "stroke-linecap:round;stroke-linejoin:round}"),
    "xk": (".xk{margin-bottom:12px}.xk li{display:flex;gap:8px;align-items:center}.xb{display:inline-grid;place-items:center;"
           "flex:none;width:24px;height:24px;border:2px solid var(--oa-color-border-strong)}.xb svg{width:20px;height:20px}"),
})


def chapter(book):
    op = opener(book)
    rules = [rule_15_1(book), rule_15_2(book), rule_15_3(book), rule_15_4(book), rule_15_5(book), rule_15_6(book),
             rule_15_7(book), rule_15_8(book), rule_15_9(book), rule_15_10(book), rule_15_11(book), rule_15_12(book),
             rule_15_13(book), rule_15_14(book), rule_15_15(book), rule_15_16(book), rule_15_17(book), rule_15_18(book),
             rule_15_19(book), rule_15_20(book), rule_15_21(book)]
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
            "combine those marks and how to place a reform on them, then work through mechanisms from the atlas as it "
            "records them.",
        ],
        "groups": [
            {"before_rule": "15.1", "number": 1, "title": "Reading a systems drawing",
             "line": "Each mark in a systems drawing answers one question about the mechanism, and a reader can name every "
                     "answer without color."},
            {"before_rule": "15.11", "number": 2, "title": "Reforms on the drawing",
             "line": "A reform turns red only where the atlas says it acts, and its two grades stay apart."},
            {"before_rule": "15.13", "number": 3, "title": "Worked examples from the atlas",
             "line": "Each example draws one mechanism from our systems atlas as the atlas records it, and shows what a reader "
                     "can take from it."},
            {"before_rule": "15.19", "number": 4, "title": "Interaction",
             "line": "A control lets a reader move through what the atlas holds, one step or one reform at a time, and "
                     "offers nothing the atlas does not hold."},
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
            {"chapter": "17", "reason": "Motion and states, where the stepper’s current step and reduced motion are set."},
            {"chapter": "18", "reason": "Rules 18.3, 18.8 and 18.22, the choice, the disclosure and the loop stepper that "
                                         "Rules 15.19 and 15.20 are built on, and Rule 18.24, the typed ID chip."},
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


# DR-265's check: the atlas's own strings, masked before a chain label is looked for, longest first, and the places a chain
# label may print on purpose: Rule 15.15's failure names Variable C3 by its chain label in Loop B4 (the fault), and its
# correct plate quotes the glossary's term for the same idea
def _strings(x, key=""):
    if isinstance(x, dict):
        for k, v in x.items():
            if k != "chain_labels":
                yield from _strings(v, k)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v, key)
    elif isinstance(x, str) and len(x) > 20:
        yield " ".join(x.replace("’", "'").split())


_LABELS = set(LOOP_NAME.values())
ATLAS_STRINGS = sorted({s_ for part in (LOOP, LINK, REFORM) for s_ in _strings(part) if s_ not in _LABELS}, key=len, reverse=True)
DR265_FAULT = {"s-15-15-failure": "Electoral pressure"}   # the plate draws it exactly once, in Loop B4's pill
DR265_ALLOW = {"s-15-15-failure": ("named Electoral pressure in Loop B4",),
               "s-15-15-correct": ("glossary defines it as electoral pressure", "glossary defines as electoral pressure",
                                   "glossary entry for electoral pressure"),
               "chapter": ("glossary entry \"Electoral pressure\"", "glossary entry “Electoral pressure”")}


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
        # the guide check's codes test reads R9 and R13 as decision codes unless "Loop " stands right before them
        for m in re.finditer(r"(?<![Ll]oop )\b(?:R9|R13)\b", re.sub(r"\s+", " ", t)):
            fails.append(f"{k}: a bare {m.group(0)}, which the guide check reads as a decision code; write Loop {m.group(0)}")
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
                  + ["s-15-3-failure", "s-15-4-failure", "s-15-15-failure"])   # 15.19 to 15.21's correct plates among them
    if wide != want:
        fails.append(f"the wide plates are {wide}, where D3-480 wants {want}")
    css = data["plate_css"]
    # round 4: print and screen are the only media a plate rule may name (Rules 15.19 and 15.20's still sequence on
    # paper, AX section 2); the plates still compose by their frame's container only (D3-480)
    for m in re.finditer(r"@media\s*([^{]*)\{", css):
        if m.group(1).strip() not in ("print", "screen"):
            fails.append(f"plate_css: a media query on {m.group(1).strip()!r}; the plates compose by their frame's container only (D3-480)")
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
    # BC S16: punctuation never touches a typed chip, whose padding and edge would set it apart ("Variable C1 , seats")
    for sid, frag in book.files.items():
        for m in re.finditer(r'<span class="chip">([^<]*)<span class="id">([^<]*)</span></span>([,.;:!?)])', frag):
            fails.append(f"{sid}: {m.group(1)}{m.group(2)} is followed by {m.group(3)!r}; let words follow a chip")
    # CD CH15-S1: a grade word that words follow ends with a period ("Well supported. The atlas calls it")
    for sid, frag in book.files.items():
        for m in re.finditer(r"<b>([A-Za-z ]+)</b></span></span></span> ([A-Z]\w*)", frag):
            fails.append(f"{sid}: the grade word {m.group(1)!r} runs on into {m.group(2)!r} with no period")
    # DR-265 (with RF-16 and RF-16a before it): no plate, alt or line of the chapter prints a loop's chain label for a
    # variable whose own title differs. The atlas's own strings (loop titles, connection names and sentences, reform
    # titles) are masked first, since "Safe seats" sits inside Loop R10's title; DR265_ALLOW holds the one fault a
    # failure plate draws on purpose and the glossary's own term
    for k, t_ in texts.items():
        flat = " ".join(re.sub(r"<[^>]+>", " ", t_).replace("’", "'").split())
        for phrase in DR265_ALLOW.get(k.replace(" alt", ""), ()):
            flat = flat.replace(phrase, " ")
        if k in DR265_FAULT:
            n_ = flat.count(DR265_FAULT[k])
            if n_ != 1:
                fails.append(f"{k}: the fault prints {DR265_FAULT[k]!r} {n_} times, where it draws it once")
            flat = flat.replace(DR265_FAULT[k], " ")
        for s_ in ATLAS_STRINGS:
            if s_ in flat:
                flat = flat.replace(s_, " ")
        for c, lab in LOOP_NAME.items():
            if lab != node(c)["title"]:
                for m in re.finditer(rf"(?<![\w-]){re.escape(lab)}(?![\w-])", flat, re.I):
                    fails.append(f"{k}: Variable {c} printed as its chain label {lab!r}, where DR-265 prints its title "
                                 f"{node(c)['title']!r}: …{flat[max(0, m.start() - 40): m.end() + 30]}…")
    kinds = {"Variable": NODE, "Connection": LINK, "Loop": LOOP, "Reform": REFORM,
             "Route": {r["code"] for r in V7["routes"]["items"]}}
    for sid, frag in book.files.items():
        for kind, rid in re.findall(r'<span class="chip">([A-Za-z ]+) <span class="id">([^<]+)</span>', frag):
            if rid not in kinds.get(kind, {}):
                fails.append(f"{sid}: {kind} {rid} is not in the atlas")
    # round 2: Rule 12.5's red sits on a reform's own targets and nowhere else on a correct plate; no correct plate or
    # rule text adds effects; every route a correct plate prints carries its own check date or "Not checked" (Rule 13.10)
    reform_of = {"s-15-11-correct": "R-03", "s-15-12-correct": "R-32", "s-15-16-correct": "R-01"}
    offered = {"s-15-20-correct": ("R-03", "R-04")}      # round 4: every target of every reform a chooser offers
    for r in data["rules"]:
        sid = r["correct"]["specimen"]
        n_red = book.files[sid].count('data-red="working"')
        want_red = (len(REFORM[reform_of[sid]]["targets"]) if sid in reform_of else
                    len({t_ for x in offered[sid] for t_ in REFORM[x]["targets"]}) if sid in offered else 0)
        if n_red != want_red:
            fails.append(f"{sid}: {n_red} red marks, where its reform's targets call for {want_red}")
    tally = re.compile(r"\b(?:overall|total|net effect|sum of|adds? up|added up)\b", re.I)
    for k, t in texts.items():
        if "failure" in k:
            continue
        for m in tally.finditer(t):
            # a word that names the fault in order to forbid it ("Never: A total, an overall score") is the rule itself
            if not re.search(r"\b(?:Never|never added)\b", t[max(0, m.start() - 40): m.end() + 40]):
                fails.append(f"{k}: {m.group(0)!r}, a word that adds a reform's effects")
    for sid, frag in book.files.items():
        if "failure" in sid:
            continue
        for seg in re.split(r'(?=data-oa-panel=")', frag):
          pm = re.match(r'data-oa-panel="([^"]+)"', seg)
          for li in re.findall(r"<li>(.*?)</li>", seg):
            mm = re.search(r'<span class="chip">Route <span class="id">([A-Z]+)</span>', li)
            if not mm:
                continue
            rid = pm.group(1) if pm else reform_of.get(sid)
            entry = next(x for x in REFORM[rid]["routes"] if x["route"] == mm.group(1))
            want = f"Checked {C13.words_date(entry['checked'])}" if entry["checked"] else "Not checked"
            if want not in li or (not entry["checked"] and re.search(r"\bChecked\b", li)):
                fails.append(f"{sid}: route {mm.group(1)} does not print {want!r}")
    # round 4 (R4-5, R4-6): no plate carries a script; 15.19 is Rule 18.22's markup; 15.20's radios are one named group;
    # every failure plate and both of 15.21's plates hold no control; 15.19 to 15.21 weigh 75,000 bytes or less together,
    # the shell's listener for 15.20 included
    live = re.compile(r"<(?:button|input|select|textarea|script)\b|role=\"slider\"|tabindex=|contenteditable", re.I)
    for sid, frag in book.files.items():
        if "<script" in frag:
            fails.append(f"{sid}: a script; chapter 18's code plate and the shell carry every script a plate needs (R4-5)")
        if ("failure" in sid or sid.startswith("s-15-21-")) and live.search(frag):
            fails.append(f"{sid}: a working control, where this plate is a still picture (R4-5)")
    if "s-15-19-correct" in book.files:
        f19 = book.files["s-15-19-correct"]
        if not all(k in f19 for k in ("data-oa-stepper", 'class="oa-stepper-status" role="status" data-oa-ready=',
                                      'class="oa-stepper-steps" role="list"', "oa-stepper-play", "oa-stepper-why")):
            fails.append("s-15-19-correct: Rule 18.22's markup is incomplete (C-1)")
        if f19.count('class="oa-stepper-step"') != len(LOOP["R1"]["links"]):
            fails.append("s-15-19-correct: the steps differ from Loop R1's connections")
    if "s-15-20-correct" in book.files:
        f20 = book.files["s-15-20-correct"]
        radios = re.findall(r'<input class="oa-choice-input" type="radio" name="s-15-20-reform" value="([^"]+)"', f20)
        if radios != list(offered["s-15-20-correct"]) or len(re.findall(r'" checked>', f20)) != 1 or not 2 <= len(radios) <= 5:
            fails.append(f"s-15-20-correct: the radios are {radios}, where ruling (f) offers R-03 and R-04 in one group, one checked")
        for rid in radios:
            if f20.count(f'data-oa-panel="{rid}"') != 1 or "data-oa-say" not in f20.split(f'data-oa-panel="{rid}"')[1][:400]:
                fails.append(f"s-15-20-correct: reform {rid} lacks its panel or the line the status reads (C-2)")
        if "data-oa-chooser-status" not in f20 or "data-oa-chooser" not in f20:
            fails.append("s-15-20-correct: the shell's hooks are missing (C-2)")
    if all(r_ in BUILT for r_ in INTERACTION):
        ours = [k for k in book.files if k.startswith(("s-15-19-", "s-15-20-", "s-15-21-"))]
        frag_b = sum(len(book.files[k].encode()) for k in ours)
        rules_b = sum(len(json.dumps(r_, ensure_ascii=False, indent=1).encode()) for r_ in data["rules"] if r_["id"] in INTERACTION)
        css_b = sum(len(CSS[k].encode()) for k in ("lv", "dw", "ch1", "pn", "pon", "ld", "pb", "xk"))
        tot = frag_b + rules_b + css_b + SHELL_CHOOSER_BYTES
        INTERACTION_BYTES[:] = [frag_b, rules_b, css_b, SHELL_CHOOSER_BYTES, tot]
        # DR-271 (November 13, 2026): R4-6's 75,000 bytes is a figure the build reports, not a stop (main() prints it)
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
    for old in SPECIMENS.glob("s-15-*.keys.json"):
        if old.name[: -len(".keys.json")] not in book.keys:
            old.unlink()
    for sid, k in book.keys.items():
        (SPECIMENS / f"{sid}.keys.json").write_text(json.dumps(k, indent=1, ensure_ascii=False) + "\n")
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
    if frag + js > ROUND_STOP:     # DR-271: chapter 15's 600,000 bytes is reported, not a stop
        print(f"  note: chapter 15's fragments and file weigh {frag + js:,} bytes, past the {ROUND_STOP:,} the round reports against")
    print("examples by domain:", dict(sorted(dom.items())), "| all examples:", len(book.examples))
    if INTERACTION_BYTES:
        f_, r_, c_, s_, tot = INTERACTION_BYTES
        print(f"Rules 15.19 to 15.21: {tot:,} bytes of {R4_6:,} (plates {f_:,}, rule entries {r_:,}, styles {c_:,}, "
              f"the shell's listener {s_:,})")
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
