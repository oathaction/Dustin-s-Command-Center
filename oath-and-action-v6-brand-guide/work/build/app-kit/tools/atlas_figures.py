"""The atlas pages' figure and data step (chat 11c; chapter 21's plan, section 9.3).

The `atlas-page` renderer (renderers/atlas-page.mjs) runs this file once per page with the page's content file:

    python3 -I work/build/app-kit/tools/atlas_figures.py REQUEST.json      prints the page's view as JSON
    python3 -I work/build/app-kit/tools/atlas_figures.py --self-test

It imports chapter 15's generator (work/build/scripts/phase-3/phase3_ch15_build.py) with importlib, read and never edited,
as chapter 15 imports chapter 13's, so every drawing comes from chapter 15's own kit (its pills, its connections drawn by
System 1's wire_marks with the 28 px lead-in, its loops, its read-aloud line) and every grade, delay and family word from
chapter 13's tables. It reads every value from the atlas model, work/extract/atlas-v7-data.json, and returns:

    model     the model's SHA-256, title, subtitle and snapshot (ISO and in words, house rule H05)
    kinds     Rule 13.9's ten kind words, keyed by where an ID lives in the model
    parts     the home drawing's eight parts in the order effects travel, each with the model's own title
    locator   the parts the page's record sits in (Rule 12.7's locator)
    view      the template's values, read from the record (loop, reform, register, home, loop index, How to read)
    figures   SVG drawings by chapter 15's code, with the style block they need (chapter 15's own rules, by class)
    inputs    every file under the project folder this step read, for the plate's freshness (contract C4)

Nothing here holds a value copied from the plan; a value the plan prints is only ever checked against, in the atlas test.
"""
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MODEL = ROOT / "work/extract/atlas-v7-data.json"
CH15_PATH = ROOT / "work/build/scripts/phase-3/phase3_ch15_build.py"

READ = set()


def _audit(event, args):
    """Every file this step opens under the project folder, chapter 15's and 13's own reads included (contract C4)."""
    if event == "open" and args and isinstance(args[0], (str, Path)):
        p = Path(args[0]).resolve() if not isinstance(args[0], int) else None
        if p and str(p).startswith(str(ROOT) + "/") and "__pycache__" not in p.parts:
            READ.add(str(p.relative_to(ROOT)))


sys.addaudithook(_audit)
sys.dont_write_bytecode = True
# PR-S4: every module this step loads is read from its source, never from a cached .pyc, so the audit hook hears each
# source file opened and a change to any of them stales the plates (a cache outside the project, empty for each run)
import atexit, shutil, tempfile  # noqa: E401,E402
sys.pycache_prefix = tempfile.mkdtemp(prefix="oa-atlas-pyc-")
atexit.register(shutil.rmtree, sys.pycache_prefix, True)

_C15 = None


def c15():
    """Chapter 15's generator, imported once, read and never edited (plan 9.3)."""
    global _C15
    if _C15 is None:
        sp = importlib.util.spec_from_file_location("phase3_ch15_build", CH15_PATH)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        # chapter 15 never read Variable D2 aloud, so its SAY table holds no words for it; read_aloud stops on a variable
        # it has no entry for. The entry is set here, in this process only: no article, singular, as chapter 15 sets for
        # its other policy variables ("presidential action without new legislation rises"). Chapter 15's file is untouched.
        m.SAY.setdefault("D2", ("", False))
        # chapter 15's conn() draws a red target on a solid line only; the data lead's R14 (and the design director's
        # DD-11C-5) set the red target on a patterned line, which this process draws through the same call, so every
        # loop drawing of chapter 15 places it and its words as for a solid target. Chapter 15's file is untouched.
        orig = m.conn

        def conn(pts, grade=None, sign=None, delay=None, authority=False, hollow=False, w=m.LW, target=False):
            # CR-9: a red target's runs are of even width (the 4 px red on its 6 px case), so each coordinate on a half
            # pixel moves half a pixel on, and its vertical runs land whole, as its horizontal runs already do
            if target and not hollow:
                pts = [tuple(c + 0.5 if abs(c - int(c)) == 0.5 else c for c in p_) for p_ in pts]
            if target and not hollow and not authority and m.tex(grade) != "solid":
                return red_patterned(m, pts, grade, sign, delay)
            return orig(pts, grade, sign, delay, authority=authority, hollow=hollow, w=w, target=target)
        m.conn = conn
        _C15 = m
    return _C15


def need(cond, msg):
    if not cond:
        raise SystemExit(f"atlas_figures: {msg}")


def red_patterned(m, pts, grade, sign, delay):
    """Rule 12.5's red target on a patterned connection, by the data lead's R14: the 28 px lead-in solid, red at 4 px on
    the 6 px case, carrying the ticks; then the pattern at 4 px (16 and 8 px dashed), fitted by System 1's fitted() from the
    lead-in's own gap to the 6 px arrowhead's base; the case on the red's rhythm, each case dash 2 px longer, set 1 px
    back; tag, ticks and arrowhead at the 6 px sizes from System 1's wire_marks(lit=True), as chapter 15's solid target."""
    BS = m.BS
    tex = m.tex(grade)
    marks, _, _ = BS.wire_marks(pts, grade, sign if sign in ("+", "-") else None, delay, m.LW, lit=True)
    marks = re.sub(r'<path class="ak-(?:case|mark)"[^>]*/>', "", marks)          # the lines are drawn below
    full = [tuple(x) for x in pts]
    total = BS.path_len(full)
    arr, _ = BS.pattern(tex, 4)
    need(arr is not None and tex != "dotted", f"R14 draws a dashed or dash-dot red target; {tex} waits for a ruling")
    gap = arr[-1]
    s0, end = m.LEAD + gap, total - BS.ARROW[6][0]
    rest = m.cut(full, s0, end)
    run = m.rounded_len(rest, m.BEND)
    need(run >= 20 * 4, f"a red {tex} target runs {run:.0f} px after its lead-in, under 80 px (R14: its grade word goes beside it)")
    need(run >= 2 * sum(arr), f"a red {tex} target holds under two periods ({run:.0f} px); R14 asks the data lead to rule")
    # CD-S10 (specs 15.4): the line runs unbroken from its last corner into the arrowhead's shaft, so the pattern never
    # turns that corner on a gap; the pattern is fitted to the run before the corner, from the lead-in's gap to the bend's
    # start, where there are two periods or more; else the whole run is patterned as before
    c = BS.path_len(full[:-1]) - m.BEND if len(full) >= 3 else None
    tail = None
    if c is not None and c > s0 and m.rounded_len(m.cut(full, s0, c), m.BEND) >= 2 * sum(arr):
        rest, tail = m.cut(full, s0, c), m.cut(full, c, end)
        run = m.rounded_len(rest, m.BEND)
    red_da = [float(x) for x in BS.fitted(tex, 4, run).split()]
    case_da = [x + 2 if i % 2 == 0 else x - 2 for i, x in enumerate(red_da)]
    lead = m.cut(full, 0, m.LEAD)
    F = BS.f
    poly = lambda q: f"M{F(q[0][0])} {F(q[0][1])}" + "".join(f"L{F(x)} {F(y)}" for x, y in q[1:])
    lead_d = poly(lead)
    da = lambda a: " ".join(f"{x:.2f}" for x in a)
    # the case rides the red's own path, its pattern set 1 px back (dashoffset 1), so every corner bends alike; the 1 px
    # before the first dash and after the last, which a path cannot reach behind its ends, are two short straight stubs
    stubs = poly(m.cut(full, s0 - 1, s0)) + poly(m.cut(full, end, end + 1))
    tail_case = f'<path class="ak-case" d="{BS.rounded_d(m.cut(full, c - 1, end), m.BEND)}"/>' if tail else ""
    tail_mark = f'<path class="ak-mark" d="{BS.rounded_d(tail, m.BEND)}" stroke-width="{m.LW}"/>' if tail else ""
    lines = (f'<path class="ak-case" d="{lead_d}"/>'
             f'<path class="ak-case" d="{BS.rounded_d(rest, m.BEND)}" stroke-dasharray="{da(case_da)}" stroke-dashoffset="1"/>'
             f'<path class="ak-case" d="{stubs}"/>{tail_case}'
             f'<path class="ak-mark" d="{lead_d}" stroke-width="{m.LW}"/>'
             f'<path class="ak-mark" d="{BS.rounded_d(rest, m.BEND)}" stroke-width="{m.LW}" stroke-dasharray="{da(red_da)}"/>{tail_mark}')
    marks = lines + marks.replace(' fill="none"', "").replace(' stroke-linecap="butt"', "").replace('class="rail"', 'class="rl"')
    return marks, full


# ---------------------------------------------------------------------------------------------------------------------
# The model, by the methods chapter 21's plan writes down (sections 3.2 and 3.4; its Appendix A)
# ---------------------------------------------------------------------------------------------------------------------
def model():
    return c15().V7


def sha():
    return hashlib.sha256(MODEL.read_bytes()).hexdigest()


# Rule 13.9's ten kind words, by the collection an ID lives in (never by its letters: B4 is a variable and a loop)
KIND = {"nodes": "Variable", "links": "Connection", "loops": "Loop", "reforms": "Reform", "issues": "Issue",
        "claims": "Claim", "domains": "Domain", "routes": "Route", "repairLog": "Rule change", "deliveryLog": "Delivery case"}


def ids_of(coll):
    V = model()
    if coll == "domains":
        return {d["id"] for d in V["domains"]}
    if coll == "routes":
        return {r["code"] for r in V["routes"]["items"]}
    if coll in ("repairLog", "deliveryLog"):
        return {r["id"] for r in V[coll]["rows"]}
    return set(V[coll])


def kinds_index():
    """Every ID in the model with the kind word (or words, for a code two collections share) of where it lives."""
    out = {}
    for coll, word in KIND.items():
        for i in ids_of(coll):
            out.setdefault(i, []).append(word)
    return out


def part(code):
    """The home drawing's part: the economy and technology layers, else the core region (plan 3.2, Appendix A)."""
    n = model()["nodes"][code]
    return {"economy": "EC", "technology": "TC"}.get(n["layer"], n["cluster"])


def sheet(code):
    """The Register's sheet: EC and TC for the two lower layers, else the variable's first domain (plan 3.4)."""
    n = model()["nodes"][code]
    return {"economy": "EC", "technology": "TC"}.get(n["layer"]) or n["domain"].split("/")[0]


# the order effects travel (plan 3.2): Outside forces, Wealth, Voice, Elections, Checks, Policy, Your household, Technology
PART_ORDER = ["X", "A", "B", "C", "D", "E", "EC", "TC"]
MAIN_CIRCUIT = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")]


def parts():
    V = model()
    regions = {r["id"]: r for r in V["layers"]["core"]["regions"]}
    out = []
    for p in PART_ORDER:
        title = V["layers"]["economy"]["title"] if p == "EC" else V["layers"]["technology"]["title"] if p == "TC" else regions[p]["title"]
        vs = [k for k in V["nodes"] if part(k) == p]
        out.append({"id": p, "title": title, "variables": vs,
                    "inside": sum(1 for x in V["links"].values() if part(x["from"]) == p and part(x["to"]) == p)})
    return out


def flows():
    """Every directed pair of parts with the count of connections it carries (plan 3.2)."""
    c = Counter()
    for x in model()["links"].values():
        a, b = part(x["from"]), part(x["to"])
        if a != b:
            c[(a, b)] += 1
    return [{"from": a, "to": b, "count": n, "main": (a, b) in MAIN_CIRCUIT} for (a, b), n in sorted(c.items(), key=lambda kv: (PART_ORDER.index(kv[0][0]), PART_ORDER.index(kv[0][1])))]


def words_date(iso):
    return c15().C13.words_date(iso)


def grade(g):
    word, gloss, line = c15().C13.GRADE[g]
    return {"key": g, "word": word, "gloss": gloss, "line": line}


def delay(d):
    n, words = c15().C13.DELAY[d]
    return {"key": d, "ticks": n, "words": words}


def link_rec(lid):
    V = model()
    x = V["links"][lid]
    N = V["nodes"]
    return {"id": lid, "from": x["from"], "to": x["to"], "from_title": N[x["from"]]["title"], "to_title": N[x["to"]]["title"],
            "sign": x["polarity"] or "none", "verb": c15().BS.verb(x["polarity"]) if x["polarity"] else ("decides" if x["type"] == "authority" else None),
            "type": x["type"], "delay": delay(x["delay"]), "grade": grade(x["evidence"]), "name": x["name"], "plain": x["plain"],
            "citation": x["citation"], "sheet": sheet(x["to"]), "loops": x["loops"]}


def var_rec(code):
    n = model()["nodes"][code]
    return {"id": code, "title": n["title"], "increase_means": n["increase_means"], "part": part(code), "sheet": sheet(code),
            "layer": n["layer"]}


def id_index():
    """Every ID of the ten kinds with what a page needs to chip it: its kind word(s) and, for a variable or a connection,
    the sheet its Register line sits on (R5)."""
    V = model()
    out = {}
    for i, ks in kinds_index().items():
        out[i] = {"kinds": ks, "names": {k: name_of(k, i) for k in ks if name_of(k, i)}}
        if i in V["nodes"]:
            out[i]["sheet"] = sheet(i)
        if i in V["links"]:
            out[i]["sheet"] = sheet(V["links"][i]["to"])
    return out


def name_of(kind, i):
    """The data lead's R22: the stored name that follows a chip of each kind, as stored (a claim takes none)."""
    V = model()
    f = {"Variable": lambda: V["nodes"][i]["title"], "Connection": lambda: V["links"][i]["name"], "Loop": lambda: V["loops"][i]["title"],
         "Reform": lambda: V["reforms"][i]["title"], "Issue": lambda: V["issues"][i]["title"],
         "Domain": lambda: next(d["title"] for d in V["domains"] if d["id"] == i),
         "Route": lambda: next(r["name"] for r in V["routes"]["items"] if r["code"] == i),
         "Rule change": lambda: next(r["rule"] for r in V["repairLog"]["rows"] if r["id"] == i),
         "Delivery case": lambda: next(r["what_was_done"] for r in V["deliveryLog"]["rows"] if r["id"] == i)}.get(kind)
    try:
        return f() if f else None
    except (KeyError, StopIteration):
        return None


def reform_rec(rid):
    V = model()
    r = V["reforms"][rid]
    C13 = c15().C13
    fam = C13.FAMILY
    routes = {x["code"]: x["name"] for x in V["routes"]["items"]}
    return {"id": rid, "title": r["title"], "summary": r["summary"], "band": r["band"],
            "band_words": V["leverage"]["bands"].get(r["band"]), "targets": r["targets"], "loops": r["loops"],
            "rejected": bool(r.get("rejected")),
            "problem": {"grade": grade(r["problem_evidence"]["grade"]), "text": r["problem_evidence"]["text"]},
            "remedy": {"grade": grade(r["remedy_evidence"]["grade"]), "text": r["remedy_evidence"]["text"],
                       # the data lead's R15: one sentence splitter for the kit and the test, System 1's sentences()
                       "sentences": c15().BS.sentences(r["remedy_evidence"]["text"])},
            "effects": [{"family": k, "name": fam[k], "code": r["effects"][k], "pips": pips(r["effects"][k])} for k in ("DQ", "GE", "EP", "EQ")],
            "effects_confidence": r["effects_confidence"],
            "routes": [{"code": x["route"], "name": routes.get(x["route"]), "who": x["who"], "feasibility": x["feasibility"],
                        "note": x["note"], "checked": x["checked"], "checked_words": words_date(x["checked"]) if x["checked"] else None}
                       for x in r["routes"]],
            "status": {"text": r["status"]["text"], "checked": r["status"]["checked"], "checked_words": words_date(r["status"]["checked"])},
            "complements": r["complements"], "sources": r["sources"], "tradeoffs": r.get("tradeoffs")}


GRADE_ORDER = ["documented", "well-supported", "plausible", "plausible_contested", "hypothesis"]   # Rule 13.3's order


def weakest_step(lid):
    """The weakest step by the data lead's ruling R8: the connection the loop's own evidence summary names as weakest, its
    grade the least certain among the loop's steps (ties allowed; a step that fails the check stops the build); None when
    the sentence names no ID."""
    V = model()
    lp = V["loops"][lid]
    txt = lp["evidence_summary"] or ""
    for k in lp["links"]:                       # 1. "<ID>: <connection name>" becomes the bare ID
        txt = txt.replace(f"{k}: {V['links'][k]['name']}", k)
    sent = next((x for x in re.split(r"(?<=[.;])\s+", txt) if re.search(r"\bweake(st|r)\b", x)), None)   # 2.
    if not sent:
        return None
    ids = r"\b(?:[A-Z]{1,3}\d+[a-z]?)\b"
    m = re.search(r"\bweake(?:st|r)\b(?:\s+step)?\s+is\s+(" + ids + ")", sent)                     # 3.
    if m:
        k = m.group(1)
    else:
        before = sent[:re.search(r"\bweake(st|r)\b", sent).start()]
        found = [x for x in re.findall(ids, before) if x in V["links"]]
        k = found[-1] if found else None
    if k is None or k not in V["links"]:
        return None                              # 5. no ID: no step marked
    lo = max(GRADE_ORDER.index(V["links"][x]["evidence"]) for x in lp["links"])
    need(k in lp["links"] and GRADE_ORDER.index(V["links"][k]["evidence"]) == lo,
         f"Loop {lid}'s evidence summary names {k} its weakest step, which is not its least certain step (R8)")    # 4.
    return k


def reads(lid):
    """The read-aloud line's marks by the data lead's R4: the first variable rises, and each connection turns the next
    variable at a minus only: "D2:rises L14 D4:falls L15 D2:rises"."""
    V = model()
    lp = V["loops"][lid]
    codes = [c for c, _ in lp["chain"]]
    up, out = True, [f"{codes[0]}:rises"]
    for i, k in enumerate(lp["links"]):
        if V["links"][k]["polarity"] == "-":
            up = not up
        out += [k, f"{codes[(i + 1) % len(codes)]}:{'rises' if up else 'falls'}"]
    need((out[-1].endswith(":rises")) == (lp["type"] == "R"), f"Loop {lid}'s signs and its kind disagree (R4)")
    return " ".join(out)


# ---------------------------------------------------------------------------------------------------------------------
# Figures, by chapter 15's own drawing code
# ---------------------------------------------------------------------------------------------------------------------
FIG_CSS_KEYS = ("sv", "id", "sn", "dm", "rt", "rp", "sh", "pp")
C13_CSS_KEYS = ("ln", "rs", "tgt")   # tgt: a red target sample's style (the data lead's request 23)


def fig_css():
    """Chapter 15's rules for its drawings and chapter 13's for its line samples and record square (their CSS tables, by
    key), with nothing of either chapter's plate layout."""
    C = c15()
    return "".join(C.CSS[k] for k in FIG_CSS_KEYS if k in C.CSS) + "".join(C.C13.CSS[k] for k in C13_CSS_KEYS if k in C.C13.CSS)


def pips(code):
    """Rule 13.5's pips for an effect code, by chapter 13's pips_svg; a range ("0 to -S at high bite") draws both ends on
    the same scale, joined by a 1 px line in the same ink (the data lead's R12), since pips_svg draws one end only."""
    C13 = c15().C13
    ends = re.split(r"\s+to\s+", code)
    if len(ends) == 1:
        return C13.pips_svg(code)
    a, b = (C13.pips_svg(x.strip()) for x in ends[:2])
    inner = lambda svg: re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    xs = [float(x) for x in re.findall(r'cx="([\d.]+)"', a + b)] + [44.0]
    join = f'<line class="j" x1="{min(xs):g}" y1="11" x2="{max(xs):g}" y2="11" stroke-width="1"/>'
    body = inner(a) + "".join(x for x in re.findall(r"<(?:circle|rect)[^>]*/>", inner(b)) if x not in inner(a))
    return re.sub(r"(<svg[^>]*>).*(</svg>)", lambda m: m.group(1) + join + body + m.group(2), a, flags=re.S)


def grade_sample(g):
    """A grade's key sample (Rule 13.4; the data lead's R3), by chapter 13's line_svg at chapter 13's key width, whose
    pattern runs the shortest run, 40 px on a 2 px line, before the arrowhead (oa.chart.grade.minRun)."""
    C13 = c15().C13
    return C13.line_svg(g, w=C13.KEY_W)


def sign_samples():
    """Rule 15.3's sign tag at 2 px for a table cell, by System 1's tag_shape, and authority's open diamond (Rule 15.5)."""
    BS = c15().BS
    out = {}
    for sg in ("+", "-"):
        out[sg] = (f'<svg class="ln wa-tagm" viewBox="0 0 22 16" width="22" height="16" aria-hidden="true" focusable="false">'
                   + BS.tag_shape(11, 8, 1, 0, sg, 2) + "</svg>")
    out["none"] = ('<svg class="ln wa-tagm" viewBox="0 0 22 16" width="22" height="16" aria-hidden="true" focusable="false">'
                   + BS.diamond_shape(18, 8, 1, 0) + "</svg>")
    return out


def tick_samples():
    """Rule 13.5's delay ticks at 2 px for a table cell, by System 1's tick_marks."""
    BS = c15().BS
    return {k: (f'<svg class="ln wa-tickm" viewBox="0 0 28 16" width="28" height="16" aria-hidden="true" focusable="false">'
                + BS.tick_marks(-8, 8, 1, 0, n, 2) + "</svg>") for k, n in (("S", 1), ("M", 2), ("L", 3))}


def record_square():
    return c15().C13.rsq()


def loop_figure(lid, targets=()):
    """A numbered loop drawn by chapter 15's kit, its weakest step named and its ID and kind inside. targets are the chosen
    reform's: chapter 15 draws a red target on a solid connection and on a pill; a patterned connection it cannot draw red
    (conn(): "a patterned one needs its lead-in at 6 px"), so such a target is returned in `not_red`, for the page to name in
    words and for the atlas test to read."""
    C = c15()
    lp = C.LOOP[lid]
    codes = [c for c, _ in lp["chain"]]
    lids = lp["links"]
    wk = weakest_step(lid)                       # the data lead's R8
    weakest = lids.index(wk) if wk else None
    kind = "reinforcing" if lp["type"] == "R" else "balancing"
    # every target of the chosen reform turns red: a pill, a solid connection by chapter 15's conn(), a patterned one by
    # R14's red_patterned() through the same call; a target that is not on this drawing is named in words by the page
    drawable = {t for t in targets if t in C.NODE or (t in C.LINK and C.tex(C.link(t)["evidence"]) in ("solid", "dashed", "dash-dot"))}
    not_red = [t for t in targets if t not in drawable]
    if len(codes) == 2:
        body, h, _ = C.two_loop(codes, lids, weakest=weakest, inside=(lid, kind), top=4, targets=drawable)
    elif len(codes) == 3:
        body, h = C.three_loop(codes, lids, weakest=weakest, inside=(lid, kind), targets=drawable)
    else:
        need(False, f"Loop {lid} has {len(codes)} variables; the figure step draws two and three today")
    svg = mark_svg(C.svg_wrap(body, h), codes, lids, wk)
    return {"svg": svg, "w": C.W, "h": h, "variables": codes, "connections": lids, "weakest": wk,
            "red": sorted(drawable & set(codes + lids)), "not_red": not_red, "kind": kind,
            "read_aloud": C.read_aloud(codes, lids), "reads": reads(lid), "minus": C.minus_count(lids)}


def mark_svg(svg, codes, lids, weakest=None):
    """The marks the atlas test reads (contract C9, the data lead's R1), set on chapter 15's drawing as it comes: each
    connection's group, in the loop's order, takes its ID, sign, type, delay and grade, and the weakest step data-weakest;
    each pill, in the chain's order, its variable's ID. Chapter 15 draws the connections first, then the pills."""
    V = model()
    groups = [m.start() for m in re.finditer(r'<g class="wr', svg)]
    need(len(groups) == len(lids), f"the drawing holds {len(groups)} connection groups for {len(lids)} connections")
    for i in reversed(range(len(lids))):
        x = V["links"][lids[i]]
        at = groups[i] + len('<g')
        a = (f' data-atlas-kind="Connection" data-atlas-id="{lids[i]}" data-sign="{x["polarity"] or "none"}" data-type="{x["type"]}"'
             f' data-delay="{x["delay"]}" data-grade="{x["evidence"]}"' + (' data-weakest="true"' if lids[i] == weakest else ""))
        svg = svg[:at] + a + svg[at:]
    pills = [m.start() for m in re.finditer(r'<rect class="pl', svg)]
    need(len(pills) == len(codes), f"the drawing holds {len(pills)} pills for {len(codes)} variables")
    for i in reversed(range(len(codes))):
        at = pills[i] + len('<rect')
        svg = svg[:at] + f' data-atlas-kind="Variable" data-atlas-id="{codes[i]}"' + svg[at:]
    return svg


def target_figure(a_code, b_code, lid, targets=()):
    """One connection between two variables, drawn downward as chapter 15's card, its pills red where they are targets."""
    C = c15()
    body, h, x = C.card(a_code, b_code, lid)
    red = [t for t in (a_code, b_code) if t in targets]
    # the card draws its first pill, then its second (card(): a.svg() + b.svg()); a target pill takes chapter 15's red
    # outline class and Rule 12.5's marker, as Pill.svg() writes them for a red pill
    pills = [m.start() for m in re.finditer(r'<rect class="pl"', body)]
    need(len(pills) == 2, "chapter 15's card no longer draws two pills")
    for i in sorted((j for j, c in enumerate((a_code, b_code)) if c in red), reverse=True):
        at = pills[i]
        end = body.index("/>", at)
        body = body[:at] + body[at:end].replace('class="pl"', 'class="pl rp"', 1) + C.RED + body[end:]
    return {"svg": mark_svg(C.svg_wrap(body, h, w=C.card_width(a_code, b_code, lid)), [a_code, b_code], [lid]), "h": h, "variables": [a_code, b_code],
            "connections": [lid], "red": red}


# ---------------------------------------------------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------------------------------------------------
def view_loop(spec):
    V = model()
    C = c15()
    lid = spec["record"]
    need(lid in V["loops"], f"no Loop {lid} in the model")
    lp = V["loops"][lid]
    chosen = spec.get("chosen_reform")
    offered = [k for k, r in V["reforms"].items() if lid in r["loops"]]      # the reforms whose own records name the loop
    need(not chosen or chosen in offered, f"Reform {chosen}'s record does not name Loop {lid}")
    tg = V["reforms"][chosen]["targets"] if chosen else []
    fig = loop_figure(lid, tg)
    steps = [link_rec(x) for x in lp["links"]]
    others = {}
    for t in set(sum((V["reforms"][k]["targets"] for k in offered), [])):
        others[t] = [k for k in offered if k != chosen and t in V["reforms"][k]["targets"]]
    gl = [{"grade": grade(m.group(1).replace(" ", "-")), "from": m.group(2), "to": m.group(3)}
          for m in re.finditer(r"([a-z][a-z_ -]*?) for ([A-Z]{1,3}\d+[a-z]?) to ([A-Z]{1,3}\d+[a-z]?)", lp["evidence"])]
    need(gl and all(x["from"] in V["nodes"] and x["to"] in V["nodes"] for x in gl), f"Loop {lid}'s grade text no longer reads 'grade for X to Y' (R11)")
    # the data lead's R22, item 4: each "X to Y" span names the one connection among the loop's own that runs from X to Y,
    # whose own grade gives the span's word; none, more than one, or another word stops the build
    for x in gl:
        cs = [k for k in lp["links"] if V["links"][k]["from"] == x["from"] and V["links"][k]["to"] == x["to"]]
        need(len(cs) == 1, f"Loop {lid}'s grade span {x['from']} to {x['to']} maps to {len(cs)} of its connections (R22)")
        need(grade(V["links"][cs[0]]["evidence"])["word"] == x["grade"]["word"], f"Loop {lid}'s span {x['from']} to {x['to']} reads {x['grade']['word']}, Connection {cs[0]} is {V['links'][cs[0]]['evidence']} (R22)")
        x["conn"] = cs[0]
    return {"grade_line": gl, "loop": {"id": lid, "kind": fig["kind"], "type": lp["type"], "title": lp["title"], "summary": lp["summary"],
                     "case": lp["case"], "qualification": lp["qualification"], "adaptation": lp["adaptation"],
                     "closure": lp["closure"], "evidence": lp["evidence"], "evidence_summary": lp["evidence_summary"],
                     "delay": delay(lp["delay"]) if lp.get("delay") in ("S", "M", "L") else lp.get("delay"),
                     "records": lp["records"], "reforms_listed": lp["reforms"]},
            "variables": [var_rec(c) for c, _ in lp["chain"]], "steps": steps, "minus": fig["minus"],
            "weakest": fig["weakest"], "read_aloud": fig["read_aloud"], "reads": fig["reads"],
            "offered": [reform_rec(k) for k in offered], "chosen": chosen, "tags": others,
            "figure": {k: fig[k] for k in ("svg", "w", "h", "red", "not_red")},
            # E11c-2: the drawing for each reform the chooser offers, so choosing one moves the red to its own targets
            "figures": {k: loop_figure(lid, V["reforms"][k]["targets"])["svg"] for k in offered}}


def view_reform(spec):
    V = model()
    rid = spec["record"]
    need(rid in V["reforms"], f"no Reform {rid} in the model")
    r = reform_rec(rid)
    tv = [t for t in r["targets"] if t in V["nodes"]]
    between = [k for k, x in V["links"].items() if {x["from"], x["to"]} == set(tv)] if len(tv) == 2 else []
    fig = target_figure(V["links"][between[0]]["from"], V["links"][between[0]]["to"], between[0], tv) if between else None
    shared = {t: [k for k, v in V["reforms"].items() if t in v["targets"] and k != rid] for t in r["targets"]}
    drawn = set(tv) | set(between)
    return {"reform": r, "targets": [var_rec(t) if t in V["nodes"] else link_rec(t) for t in r["targets"]],
            "between": [link_rec(k) for k in between], "tags": shared,
            "loops_named": [{"id": k, "drawn": bool({c for c, _ in V["loops"][k]["chain"]} & drawn)} for k in r["loops"]],
            "complements": [{"id": k, "title": V["reforms"][k]["title"]} for k in r["complements"]],
            "sources": [{"id": s, **{f: V["sources"][s].get(f) for f in ("publisher", "title", "year", "url", "kind")}} for s in r["sources"]],
            "figure": fig and {k: fig[k] for k in ("svg", "h", "red")}}


def sheet_ids():
    return [d["id"] for d in model()["domains"]] + ["EC", "TC"]


def view_register(spec):
    """The Register (plan 3.4; specs 10): the index by R2's methods, and the open sheet's variables, connections, rejected
    option, connections reviewed and not drawn, and issue records with their filters."""
    V = model()
    N, L, LO, RF, IS = V["nodes"], V["links"], V["loops"], V["reforms"], V["issues"]
    num = [k for k, x in LO.items() if not x["closure"].startswith("conceptual")]
    rows = []
    for sh in sheet_ids():
        d = next((x for x in V["domains"] if x["id"] == sh), None)
        vs = [n for n in N if sheet(n) == sh]
        ls = [k for k, x in L.items() if sheet(x["to"]) == sh]
        rows.append({"id": sh, "domain": bool(d), "title": d["title"] if d else V["layers"]["economy" if sh == "EC" else "technology"]["title"],
                     "variables": len(vs), "connections": len(ls),
                     "loops": sum(1 for k in num if any(c[0] in vs for c in LO[k]["chain"])),
                     "reforms": sum(1 for r in RF.values() if (set(vs) | set(ls)) & set(r["targets"]) and not r.get("rejected")),
                     "issues": len(d["issues"]) if d else None,
                     "grades": {g: sum(1 for k in ls if L[k]["evidence"] == g) for g in GRADE_ORDER}})
    whole = {"variables": len(N), "connections": len(L), "loops": len(num), "reforms": sum(1 for r in RF.values() if not r.get("rejected")),
             "loops_all": len(V["loops"]), "loops_conceptual": sum(1 for x in V["loops"].values() if x["closure"].startswith("conceptual")),
             "issues": len(IS), "retired": sum(1 for x in IS.values() if x.get("retired")),
             "grades": {g: sum(1 for x in L.values() if x["evidence"] == g) for g in GRADE_ORDER}}
    sh = spec.get("open_sheet")
    need(sh in sheet_ids(), f"no sheet {sh}")
    d = next((x for x in V["domains"] if x["id"] == sh), None)
    vs = [n for n in N if sheet(n) == sh]
    ls = [k for k, x in L.items() if sheet(x["to"]) == sh]
    rej = [reform_rec(k) for k, r in RF.items() if r.get("rejected") and (set(vs) | set(ls)) & set(r["targets"])]
    reviewed = []
    for x in V["rejectedLinks"]:
        a, b = x["from"].split(":")[0], x["to"].split(":")[0]
        if b in N and sheet(b) == sh:
            reviewed.append({"id": x["id"], "from": a, "to": b, "from_title": N[a]["title"] if a in N else x["from"],
                             "to_title": N[b]["title"], "reason": x["reason"], "status": x["status"]})
    on = [v for v in (spec.get("filter") or []) if v in vs]
    issues = d["issues"] if d else []
    recs = [{"id": i, "title": IS[i]["title"], "grade": grade(IS[i]["grade"].replace("_", "-")), "nodes": [n for n in (IS[i]["nodes"] or []) if n in vs],
             "shown": not on or bool(set(IS[i]["nodes"] or []) & set(on))} for i in issues]
    return {"rows": rows, "whole": whole, "sheet": {"id": sh, "domain": bool(d), "title": rows[sheet_ids().index(sh)]["title"],
            "question": d["everyday_question"] if d else None, "variables": [var_rec(n) for n in vs],
            "connections": [link_rec(k) for k in ls], "rejected": rej, "reviewed": reviewed, "records": recs,
            "filter": on, "filter_counts": {v: sum(1 for r in recs if v in r["nodes"]) for v in vs},
            "shown": sum(1 for r in recs if r["shown"])}}


def view_loop_index(spec):
    """The loop index (Rule 21.14; specs 11.1): every loop, reinforcing then balancing, in the atlas's order."""
    V = model()
    out = {"R": [], "B": []}
    for k, lp in V["loops"].items():
        conc = lp["closure"].startswith("conceptual")
        out[lp["type"]].append({"id": k, "title": lp["title"], "closure": lp["closure"], "evidence": lp["evidence"], "conceptual": conc,
                                "steps": None if conc else len(lp["links"]),
                                "minus": None if conc else sum(1 for x in lp["links"] if V["links"][x]["polarity"] == "-")})
    return {"groups": [{"type": t, "loops": out[t]} for t in ("R", "B")]}


def view_how_to_read(spec):
    """How to read (specs 11.2): each mark drawn by chapter 13's and 15's code at its true size."""
    C = c15()
    C13 = C.C13
    marks = {
        "sign_up": C13.line_svg("documented", w=C13.STEP_W, sign="+"), "sign_down": C13.line_svg("documented", w=C13.STEP_W, sign="-"),
        "authority": re.sub(r"<g class=\"wr\">|</g>$", "", ""),
        "grades": {g: grade_sample(g) for g in GRADE_ORDER}, "record_square": record_square(),
        "ticks": {k: C13.line_svg("documented", w=C13.STEP_W, delay=k) for k in ("S", "M", "L")},
        "hollow": C13.line_svg(None, w=C13.STEP_W, hollow=True),
        "red": C13.line_svg("documented", w=112, sign="+", target=True),
    }
    # authority's open diamond, drawn by System 1's wire_marks on a short line (Rule 15.5)
    m, _, _ = C.BS.wire_marks([(1, 8), (C13.STEP_W - 1, 8)], "documented", None, None, 2, lit=False, authority=True)
    marks["authority"] = (f'<svg class="ln" viewBox="0 0 {C13.STEP_W} 16" width="{C13.STEP_W}" height="16" aria-hidden="true" focusable="false">'
                          + re.sub(r'<path class="ak-case"[^>]*/>', "", m).replace(' fill="none"', "") + "</svg>")
    # Rule 15.3: a key that shows a sign quotes the atlas's own sentence on what a positive sign means, read from its
    # glossary entry for the positive sign, the sentence that says what the sign does not mean
    g = next((x["definition"] for x in model()["glossary"] if x["term"].startswith("Positive sign")), "")
    note = next((x for x in c15().BS.sentences(g) if "does not mean" in x), None)
    need(note, "the atlas's glossary no longer says what a positive sign does not mean (Rule 15.3)")
    return {"marks": marks, "sign_note": note}


def pill_h(C, rows, half_w=85, edge=3, ink=7, room=5):
    """A pill's height on the page (the data lead's request 31; ED-F9): chapter 15's own (its rows at 18 px leading, 22 px
    more, 44 at least), grown 2 px at a time until each row's ink, its words' measured width at the row's height, sits
    inside the pill's rounded ends: half_w is half the narrowest pill (the open box's 170 px), edge the outline and a
    pixel, ink half a row's glyphs."""
    h = max(len(rows) * C.LH + 22, 44)
    widths = [C.tw(r, 600) for r in rows]

    def clear(h):
        R = h / 2
        for k, w in enumerate(widths):
            dy = abs((k - (len(rows) - 1) / 2) * C.LH) + ink
            dx = max(0.0, w / 2 - (half_w - R))
            if dx * dx + dy * dy > (R - edge - room) ** 2:   # CR-10: each line's ink at least 8 px inside the curve
                return False
        return True
    while not clear(h) and h < 160:
        h += 2
    return h


def view_home(spec):
    """The atlas home (plan 3.2; specs 12): the parts, the flows by R2's methods, the hubs and their questions, the pressed
    question's parts (R6) and its answer's figure, linked to the claim that holds it (R5)."""
    V = model()
    ps = parts()
    fl = flows()
    pw = None
    if spec.get("pressed_question"):
        pw = next((x for x in V["pathways"] if x["id"] == spec["pressed_question"]), None)
        need(pw, f"no pathway {spec['pressed_question']}")
    lit = sorted({part(v) for v in pw["model_refs"]["nodes"]}, key=PART_ORDER.index) if pw else []
    hubs = [{"id": h["id"], "title": h["title"], "questions": [{"id": x["id"], "question": x["question"],
                                                                "parts": sorted({part(n) for n in x["model_refs"]["nodes"]}, key=PART_ORDER.index)}
                                                               for x in V["pathways"] if x["hub"] == h["id"]]}
            for h in V["hubs"]]
    # R19: every question's own stored answer, each with its claim chips by R20; the content file's pressed question sets
    # the plates' state only (the working page loads with none pressed)
    answers = [answer_of(x) for x in V["pathways"]]
    answer = next((a for a in answers if pw and a["id"] == pw["id"]), None)
    pills = {}
    if False:
        C = c15()
        for p_ in ps:
            for v in p_["variables"]:
                # chapter 15's pill at the box's inner width, its title wrapped by rows_of; chapter 15's own Pill()
                # refuses a title past three rows (ruling (e)), so the rows are read here and a longer title reported
                t = N_title(v)
                rows = C.rows_of(t, 172 - 2 * C.PAD)       # specs 14.4: the open box's pill, 172 px
                pills[v] = {"title": t, "h": max(len(rows) * C.LH + 22, 44), "rows": rows, "over_three_rows": len(rows) > C.MAX_ROWS}
    if not pills:                          # the switch on the working page opens every box, so the pills are always drawn
        C = c15()
        for p_ in ps:
            for v in p_["variables"]:
                t = N_title(v)
                rows = C.rows_of(t, 172 - 2 * C.PAD)       # specs 14.4: the open box's pill, 172 px
                pills[v] = {"title": t, "h": pill_h(C, rows), "rows": rows, "over_three_rows": len(rows) > C.MAX_ROWS}
    closed = home_drawing(fl, False, pills, ps, spec.get("box_need"))
    opened = home_drawing(fl, True, pills, ps, spec.get("box_need"))
    return {"parts": ps, "flows": fl, "lit": lit, "hubs": hubs, "pressed": spec.get("pressed_question"), "answer": answer, "answers": answers,
            "every_variable": bool(spec.get("every_variable")), "pills": pills, "drawing": closed, "drawing_open": opened,
            "claim_open": bool(spec.get("claim_open"))}


# R20 (the data lead's, chat 12): R5's figure method made exact. A figure is a dollar amount, a number with % or "percent",
# or a number with million, billion or trillion; a claim holds it whole (no digit, point, comma or dollar sign touching
# its start, no digit after it); the first year after it in its sentence must be in the claim too; a tie goes to the claim
# holding most of the sentence's figures; still tied, or none, no chip. One chip a claim a sentence, at the sentence's end
FIG = re.compile(r"(?<![\d.,$])(?:\$\d[\d,]*(?:\.\d+)?(?: (?:million|billion|trillion))?|\d[\d,]*(?:\.\d+)?(?:%| percent\b| (?:million|billion|trillion)\b))")
YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
# R20's six figures the method cannot link, as a known list: the build stops on any other unlinked figure, and on any of
# these that starts to link, so the list stays true when the model changes (the six go to atlas V7.1, the data lead's notes)
UNLINKED = {("PW01", "29%"), ("PW01", "$1,240"), ("PW01", "$2,420"), ("PW09", "2.1%"), ("PW10", "7.65%"), ("PW14", "83%")}


def holds(text, f):
    return re.search(r"(?<![\d.,$])" + re.escape(f) + r"(?![\d])", text) is not None


def answer_of(pw):
    """One question's short answer (R19), as stored, split into System 1's sentences, each with the claims its figures
    link to (R20) and each claim's record for its disclosure (R5)."""
    V = model()
    C = V["claims"]
    sents, recs = [], {}
    for snt in c15().BS.sentences(pw["short_answer"] or ""):
        figs = [m.group(0) for m in FIG.finditer(snt)]
        cl = []
        for m in FIG.finditer(snt):
            f = m.group(0)
            y = YEAR.search(snt[m.end():])
            y = y.group(0) if y else None
            hits = [c for c in pw["claim_ids"] if holds(C[c]["claim"], f) and (not y or y in C[c]["claim"])]
            if len(hits) > 1:
                best = max(sum(holds(C[c]["claim"], g) for g in figs) for c in hits)
                hits = [c for c in hits if sum(holds(C[c]["claim"], g) for g in figs) == best]
            known = (pw["id"], f) in UNLINKED
            need(len(hits) == 1 or known, f"the figure {f} in {pw['id']}'s answer links to {len(hits)} claims and is not on R20's list")
            need(not (len(hits) == 1 and known), f"the figure {f} in {pw['id']}'s answer now links to {hits[:1]}; take it off R20's list")
            if len(hits) == 1 and hits[0] not in cl:
                cl.append(hits[0])
        for c in cl:
            if c not in recs:
                x = C[c]
                recs[c] = {"claim": c, "record": {**{k: x[k] for k in ("claim", "population", "jurisdiction", "period", "limitation")},
                           "grade": grade(x["confidence"]), "sources": [{"id": s_, **{f: V["sources"][s_].get(f) for f in ("publisher", "title", "year", "url")}} for s_ in x["sources"]]}}
        sents.append({"text": snt, "claims": cl})
    return {"id": pw["id"], "question": pw["question"], "text": pw["short_answer"], "sentences": sents, "claims": list(recs.values()),
            "sources": len(pw["source_ids"])}


def home_drawing(flows_, every=False, pills=None, parts_=None, box_need=None):
    """The home drawing's wide form (specs 12.2): eight boxes and one orthogonal arrow a directed pair, routed by the design
    director's table, each count at its place, the main circuit in the essential ink and the rest in the subtle ink, every
    crossing a break in the line that yields (a main line runs on; else the lower count breaks; on a tie, the vertical).
    Boxes are returned as rectangles for the page to draw in HTML; the arrows as one SVG. Stops on a pair with no route."""
    BS = c15().BS
    F = BS.f
    pills = pills or {}
    PW_GAP = 8
    X0 = {"A": 48, "B": 303, "C": 558, "D": 813, "E": 1068}
    W = 196
    vs = {p_["id"]: p_["variables"] for p_ in parts_}
    ph = lambda v: pills[v]["h"] if every and v in pills else 0

    def stack(ids):                       # one pill a row
        return sum(ph(v) + PW_GAP for v in ids) if every else 0

    def grid(ids, cols):                  # pills in columns, each row as tall as its tallest
        if not every:
            return 0
        rows = [ids[i:i + cols] for i in range(0, len(ids), cols)]
        return sum(max(ph(v) for v in r) + PW_GAP for r in rows)
    # the data lead's requests 4 and 27: each row grows to the tallest box's words, as the kit measures them at 1440 px
    # with each box's height freed (box_need, whole pixels); the specs' heights stay the floor
    floor = (box_need or {}).get("open" if every else "closed", {})
    # specs 15.1 (CD-S1, chat 12): the rows 44, 44, 204, 96, 92 and 44 in place of 56, 56, 184, 112, 104 and 56, so the
    # whole circuit and its key end above 880 px at 1440 by 900; the kit's measure stays each row's floor
    band_h = max(44 + (max((ph(v) for v in vs["X"]), default=0) + PW_GAP if every else 0), floor.get("X", 0))
    yb = band_h
    yc = yb + 44
    hc = max([204 + max(stack(vs[k]) for k in X0)] + [floor.get(k, 0) for k in X0])
    ycb = yc + hc
    yl = ycb + 96
    hl = max(92 + max(grid(vs["EC"], 3), grid(vs["TC"], 2)), floor.get("EC", 0), floor.get("TC", 0))
    ylb = yl + hl
    H = ylb + 44
    boxes = {"X": (48, 0, 1216, band_h), **{k: (x, yc, W, hc) for k, x in X0.items()}, "EC": (48, yl, 706, hl), "TC": (813, yl, 451, hl)}
    A, B, C, D, E = (X0[k] for k in "ABCDE")
    R = {   # pair: (points, count place (x, y, anchor))
        ("X", "A"): ([(A + 24, yb), (A + 24, yc)], (A + 30, yc - 8, "start")),
        ("X", "B"): ([(B + 24, yb), (B + 24, yc)], (B + 30, yc - 8, "start")),
        ("X", "C"): ([(C + 98, yb), (C + 98, yc)], (C + 104, yc - 8, "start")),
        ("X", "D"): ([(D + 172, yb), (D + 172, yc)], (D + 178, yc - 8, "start")),
        ("X", "E"): ([(E + 172, yb), (E + 172, yc)], (E + 178, yc - 8, "start")),
        ("X", "EC"): ([(48, yb / 2), (36, yb / 2), (36, yl + 46), (48, yl + 46)], (42, yl - 10, "start")),
        ("X", "TC"): ([(1264, yb / 2), (1276, yb / 2), (1276, yl + 46), (1264, yl + 46)], (1270, yl - 10, "end")),
        ("B", "E"): ([(B + 120, yc), (B + 120, yb + 18), (E + 40, yb + 18), (E + 40, yc)], ((B + 120 + E + 40) / 2, yb + 15, "middle")),
        ("A", "B"): ([(A + W, yc + 40), (B, yc + 40)], ((A + W + B) / 2, yc + 34, "middle")),
        ("B", "C"): ([(B + W, yc + 40), (C, yc + 40)], ((B + W + C) / 2, yc + 34, "middle")),
        ("C", "D"): ([(C + W, yc + 40), (D, yc + 40)], ((C + W + D) / 2, yc + 34, "middle")),
        ("D", "E"): ([(D + W, yc + 40), (E, yc + 40)], ((D + W + E) / 2, yc + 34, "middle")),
        ("C", "B"): ([(C, yc + 88), (B + W, yc + 88)], ((B + W + C) / 2, yc + 104, "middle")),
        ("D", "C"): ([(D, yc + 88), (C + W, yc + 88)], ((C + W + D) / 2, yc + 104, "middle")),
        ("E", "D"): ([(E, yc + 88), (D + W, yc + 88)], ((D + W + E) / 2, yc + 104, "middle")),
        ("E", "A"): ([(E + W, yc + 120), (1300, yc + 120), (1300, ylb + 38), (12, ylb + 38), (12, yc + 120), (A, yc + 120)], (656, ylb + 35, "middle")),
        ("E", "EC"): ([(E + W, yc + 152), (1288, yc + 152), (1288, ylb + 18), (700, ylb + 18), (700, ylb)], (994, ylb + 15, "middle")),
        ("D", "B"): ([(D + 16, ycb), (D + 16, ycb + 18), (B + 180, ycb + 18), (B + 180, ycb)], ((D + 16 + B + 180) / 2, ycb + 15, "middle")),
        ("B", "D"): ([(B + 156, ycb), (B + 156, ycb + 36), (D + 40, ycb + 36), (D + 40, ycb)], ((B + 156 + D + 40) / 2, ycb + 33, "middle")),
        ("D", "EC"): ([(D + 100, ycb), (D + 100, ycb + 54), (784, ycb + 54), (784, yl + 28), (754, yl + 28)], ((D + 100 + 784) / 2, ycb + 51, "middle")),
        ("TC", "B"): ([(D + 72, yl), (D + 72, ycb + 72), (B + 120, ycb + 72), (B + 120, ycb)], ((D + 72 + B + 120) / 2, ycb + 69, "middle")),
        ("TC", "A"): ([(D + 48, yl), (D + 48, ycb + 90), (A + 150, ycb + 90), (A + 150, ycb)], ((D + 48 + A + 150) / 2, ycb + 87, "middle")),
        ("A", "EC"): ([(A + 60, ycb), (A + 60, yl)], (A + 66, (ycb + yl) / 2 + 5, "start")),
        ("EC", "A"): ([(A + 100, yl), (A + 100, ycb)], (A + 106, (ycb + yl) / 2 + 5, "start")),
        ("D", "TC"): ([(D + 130, ycb), (D + 130, yl)], (D + 136, (ycb + yl) / 2 + 5, "start")),
        ("TC", "D"): ([(D + 170, yl), (D + 170, ycb)], (D + 176, (ycb + yl) / 2 + 5, "start")),
        ("TC", "EC"): ([(813, yl + 64), (754, yl + 64)], ((813 + 754) / 2, yl + 58, "middle")),
    }
    by = {(f_["from"], f_["to"]): f_ for f_ in flows_}
    need(set(by) <= set(R), f"pairs with no route in the specs' table: {sorted(set(by) - set(R))} (specs 12.2, ED-F10)")
    segs = {k: list(zip(R[k][0], R[k][0][1:])) for k in by}

    def cross(s1, s2):
        (a, b), (c, d) = s1, s2
        if (a[0] == b[0]) == (c[0] == d[0]):
            return None                    # parallel orthogonal runs never cross here
        v, h = (s1, s2) if a[0] == b[0] else (s2, s1)
        x, y = v[0][0], h[0][1]
        if min(h[0][0], h[1][0]) < x < max(h[0][0], h[1][0]) and min(v[0][1], v[1][1]) < y < max(v[0][1], v[1][1]):
            return (x, y, v is s1)
        return None
    keys = sorted(by)
    crossings = []
    for i, k1 in enumerate(keys):
        for k2 in keys[i + 1:]:
            for s1 in segs[k1]:
                for s2 in segs[k2]:
                    c = cross(s1, s2)
                    if c:
                        x, y, k1_vertical = c
                        m1, m2 = by[k1]["main"], by[k2]["main"]
                        if m1 != m2:
                            brk = k2 if m1 else k1
                        elif by[k1]["count"] != by[k2]["count"]:
                            brk = k1 if by[k1]["count"] < by[k2]["count"] else k2
                        else:
                            brk = k1 if k1_vertical else k2
                        on = k2 if brk == k1 else k1
                        crossings.append({"at": (x, y), "breaks": brk, "runs_on": on, "vertical_breaks": (brk == k1) == k1_vertical})
    out = []
    covers = []
    for k in keys:
        pts = R[k][0]
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        ux, uy = BS.unit(x2 - x1, y2 - y1)
        body = pts[:-1] + [(x2 - ux * BS.ARROW[2][0], y2 - uy * BS.ARROW[2][0])]
        cls = "mc" if by[k]["main"] else "of"
        d = "M" + "L".join(f"{F(x)} {F(y)}" for x, y in body)
        out.append((cls, f'<g class="{cls}" data-flow="{k[0]}>{k[1]}"><path class="ln" d="{d}"/>{BS.head_shape(x2, y2, ux, uy, 2)}</g>'))
    for c in crossings:
        x, y = c["at"]
        # the yielding line stops 6 px either side of the line that runs on: a 14 by 4 px cut of the ground over it,
        # then the line that runs on drawn again through the cut
        w_, h_ = (4, 14) if c["vertical_breaks"] else (14, 4)
        covers.append(f'<rect class="cut" x="{F(x - w_ / 2)}" y="{F(y - h_ / 2)}" width="{w_}" height="{h_}"/>')
        on = R[c["runs_on"]][0]
        cls = "mc" if by[c["runs_on"]]["main"] else "of"
        seg = [(x - 8, y), (x + 8, y)] if c["vertical_breaks"] else [(x, y - 8), (x, y + 8)]
        covers.append(f'<path class="ln {cls}" d="M{F(seg[0][0])} {F(seg[0][1])}L{F(seg[1][0])} {F(seg[1][1])}"/>')
    labels = [f'<text class="n{" b" if by[k]["main"] else ""}" x="{F(R[k][1][0])}" y="{F(R[k][1][1])}"'
              + (f' text-anchor="{R[k][1][2]}"' if R[k][1][2] != "start" else "")
              + f' data-count="{by[k]["count"]}" data-count-of="flow:{k[0]}>{k[1]}">{by[k]["count"]}</text>' for k in keys]
    svg = (f'<svg class="wa-flows" viewBox="0 0 1312 {F(H)}" width="1312" height="{F(H)}" aria-hidden="true" focusable="false">'
           + "".join(x for c_, x in out if c_ == "of") + "".join(x for c_, x in out if c_ == "mc") + "".join(covers) + "".join(labels) + "</svg>")
    return {"w": 1312, "h": H, "svg": svg, "boxes": {k: {"x": v[0], "y": v[1], "w": v[2], "h": v[3]} for k, v in boxes.items()},
            "crossings": len(crossings), "crossing_list": [f"{c['breaks'][0]}>{c['breaks'][1]} breaks at {c['runs_on'][0]}>{c['runs_on'][1]}" for c in crossings]}


def N_title(v):
    return model()["nodes"][v]["title"]


VIEWS = {"loop": view_loop, "reform": view_reform, "register": view_register, "loop-index": view_loop_index,
         "how-to-read": view_how_to_read, "home": view_home}


def build(spec):
    V = model()
    rec = spec.get("record")
    out = {"model": {"sha256": sha(), "title": V["meta"]["title"], "subtitle": V["meta"]["subtitle"],
                     "snapshot": V["meta"]["snapshot"], "snapshot_words": words_date(V["meta"]["snapshot"])},
           "parts": parts(), "kind_words": list(KIND.values()),
           "effect_words": V["outcomes"]["effect_codes"],
           "grade_samples": {g: grade_sample(g) for g in GRADE_ORDER}, "record_square": record_square(), "ids": id_index(),
           "sign_samples": sign_samples(), "tick_samples": tick_samples(),
           "counts": {"variables": len(V["nodes"]), "connections": len(V["links"]), "loops": len(V["loops"]), "reforms": len(V["reforms"]),
                      "issues": len(V["issues"])}}
    fn = VIEWS.get(spec["view"])
    out["view"] = fn(spec) if fn else {}
    # the locator (Rule 12.7): the parts the page's record sits in
    v = out["view"]
    codes = ([x["id"] for x in v.get("variables", [])] or [t["id"] if "part" in t else t["to"] for t in v.get("targets", [])]
             or [x["id"] for x in (v.get("sheet") or {}).get("variables", [])])
    out["locator"] = sorted({part(c) for c in codes}, key=PART_ORDER.index)
    # the record's own title, for the page's tab title (AL-01, 2.4.2): {title} in the generator's title words
    rec = spec.get("record")
    out["record_title"] = (V["loops"].get(rec) or V["reforms"].get(rec) or {}).get("title") if rec else None
    out["figure_css"] = fig_css()
    # a module loaded from its cached bytecode opens no source file, so each loaded module's source counts as read too
    C = c15()
    for m in [*sys.modules.values(), C, C.C13, C.BS]:
        f = getattr(m, "__file__", None)
        if f and str(Path(f).resolve()).startswith(str(ROOT) + "/"):
            READ.add(str(Path(f).resolve().relative_to(ROOT)))
    READ.discard("work/build/app-kit/tools/atlas_figures.py")   # the kit's own code is an input already
    # chapter 15 reads the guide build's source at import only to check that the shell still reads its plate keys
    # (D3-480); it draws nothing from it, and the guide build is the engineer's to change, so it is no input of a plate
    READ.discard("work/build/scripts/phase-2/guide_build.py")
    out["inputs"] = sorted(READ)
    return out


def self_test():
    bad = 0

    def check(name, ok):
        nonlocal bad
        print(f"{'pass' if ok else 'FAIL'} {name}")
        bad += not ok
    V = model()
    check("Rule 13.9's ten kind words, one a collection", len(KIND) == 10 and len(set(KIND.values())) == 10)
    ki = kinds_index()
    check("a code two collections share takes both kind words (Variable B4 and Loop B4)", sorted(ki.get("B4", [])) == ["Loop", "Variable"])
    ps = parts()
    check("eight parts, every variable in one", len(ps) == 8 and sum(len(p["variables"]) for p in ps) == len(V["nodes"]))
    fl = flows()
    check("the flows and the insides count every connection once", sum(f["count"] for f in fl) + sum(p["inside"] for p in ps) == len(V["links"]))
    v = view_loop({"record": "R18", "chosen_reform": "R-11"})
    check("Loop R18 draws by chapter 15's two-variable loop, its weakest step the least certain", v["figure"]["svg"].startswith('<svg class="sv"')
          and V["links"][v["weakest"]]["evidence"] == c15().least_certain(V["loops"]["R18"]["links"]))
    check("a red target is drawn only where chapter 15 can draw it; the rest are named", set(v["figure"]["red"]) | set(v["figure"]["not_red"]) == set(V["reforms"]["R-11"]["targets"]))
    check("the read-aloud line comes back where it began, rising, on a reinforcing loop", v["loop"]["type"] == "R" and v["read_aloud"].endswith(" rises."))
    check("its marks carry each variable's direction (R4): D2 rises, L14, D4 falls, L15, D2 rises", v["reads"] == "D2:rises L14 D4:falls L15 D2:rises")
    got = {k: weakest_step(k) for k, lp in V["loops"].items() if not lp["closure"].startswith("conceptual")}
    check("R8's weakest steps on every numbered loop: R18 L15, R1 L02, R10 L53, R7 and R8 none",
          got["R18"] == "L15" and got["R1"] == "L02" and got["R10"] == "L53" and got["R7"] is None and got["R8"] is None and got["R16"] == "T01")
    r = view_reform({"record": "R-23"})
    check("Reform R-23's page reads four effect rows, one a family", [e_["family"] for e_ in r["reform"]["effects"]] == ["DQ", "GE", "EP", "EQ"])
    check("every file this step read sits under the project folder and the model is one of them", "work/extract/atlas-v7-data.json" in READ)
    return bad


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(1 if self_test() else 0)
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    spec = json.loads(Path(sys.argv[1]).read_text())
    print(json.dumps(build(spec), ensure_ascii=False))
