"""Chapter 14, group 18, "Three charts in full": Rules 14.142 to 14.144, their entry files, specs and plates.

Oath & Action Edition 06, Phase 3, round 5. Complex examples maker, November 14, 2026, under
work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md (R5-1, R5-4), the data lead's rulings (c) and (d), the accessibility
lead's round 5 "Interaction specification" and the component engineer's contracts CE-1 to CE-4.

Usage:
    python3 -I work/build/scripts/phase-3/phase3_ch14_complex_build.py           write the files below; exit 1 on any fault
    python3 -I work/build/scripts/phase-3/phase3_ch14_complex_build.py --check   fail if a file on disk differs; write nothing

Reads, by script, every value it prints:
    work/extract/atlas-v7-data.json                      the atlas model, snapshot of October 15, 2026
    work/build/data/fred-payrolls-monthly-change.csv     S14's frozen file and its sidecar (through maker_c_round5_derive.py)
    work/handoffs/phase-3/20261112_Chapter-14-Plan.json  the rows of Rules 14.142 to 14.144 (R5-1): IDs, files, plates
and draws every loop with chapter 15's own drawing functions, imported read-only from
work/build/scripts/phase-3/phase3_ch15_build.py (the systems designer's contract C-SD1): three_loop and four_loop with
steps_g for Rule 14.143, two_loop for Rule 14.144. Nothing of chapter 15's is copied or written. The stepper's buttons and
reason line, the choice's check and the disclosure's chevron come from chapter 18's code sets by that file's code_part, so
each plate carries one copy of each live component's markup and no script (R4-5, CE-1, CE-2).

Writes:
    work/build/chart-kit/specs/s96.json                  Rule 14.142's correct plate: S14 in full, drawn by the kit
    work/build/guide/specimens/s-14-142-failure.html     and s-14-142-failure.chart.json, its failure plate (C7)
    work/build/guide/specimens/s-14-143-correct.html     Loops B4 and R10 on Rule 18.22's stepper, and s-14-143-failure.html
    work/build/guide/specimens/s-14-144-correct.html     Reforms R-06, R-30 and R-38 on Rule 15.20's chooser, and s-14-144-failure.html
    work/build/guide/entries/14-142.json to 14-144.json  the three rules (R5-1's entry files)
The keys files of the two live plates are the component engineer's (CE-3); this script never writes them.

Then runs its checks and stops on any failure: every atlas value printed matches the model; every figure matches S14's
file (maker_c_round5_derive.py's facts); the drawing numbers each loop's steps in the atlas's order (Rule 15.6) and its
groups carry the walk's numbers; the stepper's markup as CE-1 lists it, the chooser's as CE-2 lists it; red only on a
chosen reform's targets on the drawing; no total, count or rank of effects anywhere; every qualifier whole; every route
dated or "Not checked"; no em dash, no U+2011, no literal color, no heading, no studio word in reader text; each plate's
bytes reported (DR-271), never a stop.
"""
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SPECIMENS = ROOT / "work/build/guide/specimens"
ENTRIES = ROOT / "work/build/guide/entries"
SPECS = ROOT / "work/build/chart-kit/specs"
PLAN = ROOT / "work/handoffs/phase-3/20261112_Chapter-14-Plan.json"
ME = "work/build/scripts/phase-3/phase3_ch14_complex_build.py"
WRITTEN = "November 14, 2026"

sys.dont_write_bytecode = True


def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# chapter 15's drawing functions, read-only (C-SD1): never main(), write() or chapter()
C15 = _load("phase3_ch15_build", "work/build/scripts/phase-3/phase3_ch15_build.py")
DV = _load("maker_c_round5_derive", "work/build/scripts/phase-3/maker_c_round5_derive.py")
C13 = C15.C13
e, need, chip, grade_word, diagram_label, dnp = C15.e, C15.need, C15.chip, C15.grade_word, C15.diagram_label, C15.dnp
LINK, NODE, LOOP, REFORM = C15.LINK, C15.NODE, C15.LOOP, C15.REFORM
GRADE, DELAY, SNAP, MINUS = C15.GRADE, C15.DELAY, C15.SNAP, C15.MINUS
short, lc, words_n, link, node = C15.short, C15.lc, C15.words_n, C15.link, C15.node
FACTS = DV.facts()
need(SNAP == "October 15, 2026" and FACTS["snapshot"] == "2026-10-15", "the atlas snapshot moved; reread every value")
FC = "Failure case: do not publish. "
# Rule 01.12's log for Rule 14.143 (ruling (g)): Loop B4 and Loop R10 as Rule 15.15 logs them, read from chapter 15's source
_C15_SRC = (ROOT / "work/build/scripts/phase-3/phase3_ch15_build.py").read_text(encoding="utf-8")
LOG_143 = [(m.group(1), m.group(2), m.group(3)) for m in
           re.finditer(r'book\.log\("15\.15 correct", "Loop (B4|R10), ([^"]+)", "(D\d\d)"\)', _C15_SRC)]
need([x[0] for x in LOG_143] == ["B4", "R10"] and dict((x[0], x[2]) for x in LOG_143) == {"B4": "D04", "R10": "D02"},
     f"Rule 15.15's log of Loops B4 and R10 changed ({LOG_143}); ruling (g) logs B4 under D04 and R10 under D02")
RSQ = C13.rsq()


def curl(t):
    """An atlas string as the guide prints it: curly apostrophes and quotation marks (ED-E5)."""
    t = re.sub(r"(^|[\s(\[{])'", lambda m: m.group(1) + "‘", str(t))
    t = t.replace("'", "’")
    t = re.sub(r'(^|[\s(\[{])"', lambda m: m.group(1) + "“", t)
    return t.replace('"', "”")


def ce(t):
    """Curled, then escaped for markup."""
    return e(curl(t))


def plan_rows():
    plan = json.loads(PLAN.read_text())
    rows = {r["rule"]: r for r in plan["chapter_rules"] if r["rule"] in ("14.142", "14.143", "14.144")}
    need(sorted(rows) == ["14.142", "14.143", "14.144"], "the plan holds no rows for Rules 14.142 to 14.144 (R5-1)")
    g = [x for x in plan["groups"] if x.get("group") == 18]
    need(g and g[0]["rules"] == "14.142 to 14.144", "the plan's group 18 changed")
    return rows


ROWS = plan_rows()
need(ROWS["14.142"]["spec_id"] == "S96" and ROWS["14.142"]["correct"] == "s-14-s96"
     and ROWS["14.143"]["correct"] == "s-14-143-correct" and ROWS["14.144"]["correct"] == "s-14-144-correct",
     "the plan's IDs for group 18 changed (R5-1); nobody renumbers")


# ---------------------------------------------------------------------------------------------------------------------
# A plate's own style. Chapter 14's shared block already defines .fx for its charts' axis row (grid-column 2, 26 px
# tall), so chapter 15's two-column .fx takes the name .cfx here, in the markup and in the rules the plate carries. Two
# more names meet rules from outside the plate on this page (main session, 04:40 UTC, from SG-7): the shell's .rt (a
# grid column) would select chapter 15's .rt group, and chapter 14's block's .tk (a tick label, absolutely placed) would
# select chapter 15's .tk tick path, so they take .crt and .ctk. Every other class keeps chapter 15's name and look. The
# style sits in the fragment, which the build scopes to the specimen.
# ---------------------------------------------------------------------------------------------------------------------
RENAME = {"fx": "cfx", "rt": "crt", "tk": "ctk"}
# chapter 15's LAYOUT closes one brace more than it opens ("grid-row:2}}}" ends its wide @container rule and then the
# build's @scope), so its narrow-frame rule fell outside the plate's scope and applied to every .p on the page. This
# plate carries a balanced copy (C-SD1: copy what you need); the systems designer has the same fix for its own block
_LAYOUT = C15.LAYOUT
if _LAYOUT.count("}") == _LAYOUT.count("{") + 1 and "grid-row:2}}}@container" in _LAYOUT:
    _LAYOUT = _LAYOUT.replace("grid-row:2}}}@container", "grid-row:2}}@container", 1)
need(_LAYOUT.count("{") == _LAYOUT.count("}"), "chapter 15's LAYOUT braces changed; reread it before copying")


def rename_classes(s):
    return re.sub(r'class="([^"]*)"', lambda m: 'class="' + " ".join(RENAME.get(c, c) for c in m.group(1).split()) + '"', s)


def rename_css(css):
    for a, b in RENAME.items():
        css = re.sub(r"\." + a + r"(?![\w-])", "." + b, css)
    return css


def plate_style(body, swap=None, extra=""):
    """The rules this plate's markup uses, from chapter 15's CSS (C-SD1: copy what you need), with the stepper's or the
    chooser's state rules swapped for this plate's own, then this plate's own rules and chapter 15's compositions last."""
    used = set()
    for cls in re.findall(r'class="([^"]+)"', body):
        used.update(cls.split())
    used.update(RENAME.get(c, c) for c in list(used))
    used |= {k for k, v in RENAME.items() if v in used}
    parts = [C15.BASE, ".p{padding:16px}"]       # chapter 14's block pads .p 24 px from 48em; a 328 px stage keeps 16
    for k, css in C15.CSS.items():
        if k in used:
            for old, new in (swap or {}).items():
                if old in css:
                    css = css.replace(old, new)
            parts.append(css)
    parts.append(extra)
    parts.append(_LAYOUT)
    return "<style>" + rename_css("".join(parts)) + "</style>"


def fragment(sid, body, style):
    body = rename_classes(re.sub(r">\s+<", "><", body.strip()))
    return (f"<!-- {sid}: Oath & Action guide, Edition 06, chapter 14. Complex examples maker, {WRITTEN}. Written by {ME}. -->\n"
            f"{style}\n<div class=\"p wd\">{body}</div>\n")


def plate_meta(alt, interactive=False, keys=False, notes=""):
    """The plate keys the shell reads (R5-1): chapter 15's stage, a 328 px true size that widens to 680 px where the frame
    holds it, with the frame as the query container."""
    m = {"alt": " ".join(curl(alt).split()), "illustrative": False, "width_px": C15.STAGE, "wide_px": C15.WIDE,
         "frame_container": True, "fit_switch": False, "notes": notes}
    if interactive:
        m["interactive"] = True
    if keys:
        m["keys"] = True
    return m


def src(what):
    return C15.src(what)


# =====================================================================================================================
# Rule 14.143: Loops B4 and R10, stepped one connection at a time through Variable C3 (ruling d)
# =====================================================================================================================
WALK = [("B4", "L23"), ("B4", "L24"), ("B4", "L54"), ("R10", "L08"), ("R10", "L25"), ("R10", "L53"), ("R10", "L42")]
KIND = {"B4": "balancing", "R10": "reinforcing"}
# each loop's starting supposition (ruling d): B4 starts at the quality of public services and supposes it falls (L23's
# name speaks of poor service); R10 starts at seats with little electoral competition and supposes they rise
START = {"B4": ("D5", "falls"), "R10": ("C1", "rise")}
# where a title enters a sentence after its first word, the words English needs before it (the atlas's own how_to_read for
# both loops: "The quality of public services lowers the risk of losing office")
THE = {"D5": "the quality of public services", "C3": "the risk of losing office"}
PLURAL = {"C1": True, "C5": True, "C2": False, "C3": False, "C4": False, "D5": False}


OBJECT = {"C5": "the number of incumbents defeated or pushed into retirement"}   # as B4's how_to_read says it


def in_sentence(code, first=False, obj=False):
    t = (OBJECT.get(code) if obj else None) or THE.get(code) or lc(curl(short(code)))
    need(lc(curl(short(code))) in t.lower(), f"Variable {code}'s title is not whole in its sentence (DR-265)")
    return t[0].upper() + t[1:] if first else t


# how each variable's change is said (the editor's words for CE-M1): "rises" and "falls" for a singular title, "rise" and
# "fall" for a plural one, "goes up" and "goes down" after the title that asks how often; "can" before the base form
VERB = {"C2": ("goes up", "goes down", "go up", "go down")}


def says(code, up, can, subject=True):
    """A variable and its change in the walk's direction: its title whole (DR-265), then its verb."""
    t = in_sentence(code, first=subject, obj=True)
    plural = PLURAL[code] and code not in OBJECT          # "the number of ..." is singular
    if code in VERB:
        v3u, v3d, bu, bd = VERB[code]
    else:
        v3u, v3d, bu, bd = ("rise", "fall", "rise", "fall") if plural else ("rises", "falls", "rise", "fall")
    return f"{t} {('can ' + (bu if up else bd)) if can else (v3u if up else v3d)}"


def directions(lid):
    """The walk's direction at each variable of a loop, from its start supposition through each connection's sign (the data
    lead's R2, item 1), and where "can" starts: after the first plausible step, to the end of the loop (item 2)."""
    lp = LOOP[lid]
    up = START[lid][1] in ("rise", "rises")
    out, can = [], False
    for x in lp["links"]:
        l = link(x)
        nxt = up if l["polarity"] == "+" else not up
        can_after = can or l["evidence"] == "plausible"
        out.append({"link": x, "cause_up": up, "effect_up": nxt, "cause_can": can, "effect_can": can_after})
        up, can = nxt, can_after
    return out


def walk_steps():
    """Each step's words as Rule 18.22's list holds them (CE-1, the accessibility lead's 2.4; the data lead's R2 and the
    editor's words for CE-M1): the line says the walk's direction at both ends, cause first, computed from the start
    supposition and the signs ("can" from the plausible step on); the more words give the typed connection, its name, its
    sign in words that hold either way, what moves along it, its grade and its delay; the step that closes a loop says
    where the change ends up and names its kind; the walk names Variable C3 as the variable both loops pass through where
    it meets it first and where Loop R10 meets it. Each hold is CE-1's formula from what the status line says."""
    f2 = FACTS["example_2"]
    out = []
    count = {lid: 0 for lid in KIND}
    dirs = {lid: directions(lid) for lid in KIND}
    for k, (lid, x) in enumerate(WALK, 1):
        lp = LOOP[lid]
        codes = [c for c, _ in lp["chain"]]
        i = lp["links"].index(x)
        n = len(lp["links"])
        count[lid] += 1
        need(count[lid] == i + 1, f"the walk takes Loop {lid}'s steps out of the atlas's order (ruling d)")
        l = link(x)
        a, b = codes[i], codes[(i + 1) % n]
        need((l["from"], l["to"]) == (a, b), f"Connection {x} changed")
        d = dirs[lid][i]
        closes = i == n - 1
        # the editor's second read: the closing step's "again" lives in its result sentence ("... can rise again, on top
        # of the first rise"), so the line states the direction alone and the step no longer says "can rise again" twice
        line = f"{says(a, d['cause_up'], d['cause_can'])}, so {says(b, d['effect_up'], d['effect_can'], subject=False)}."
        moves = f", and {l['type']} moves along it" if l["type"] in ("money", "information", "ownership") else ""
        sign = ("a minus sign, which means that when one rises, the other falls" if l["polarity"] == "-"
                else "a plus sign, which means that the two rise and fall together")
        least = (", the least certain step in the loop" if l["evidence"] == C15.least_certain(lp["links"])
                 and len({link(y)["evidence"] for y in lp["links"]}) > 1 else "")
        more = (f'{chip("Connection", x)} “{ce(l["name"])}” carries {sign}{moves}. The atlas grades it '
                f'{GRADE[l["evidence"]][0].lower()}{least}, and its effect takes {DELAY[l["delay"]][1]}.')
        # the atlas's own claim of a weakest step, read from the loop's evidence summary (Loop B4: all three steps well
        # supported, and L54 the weakest for U.S. services); none is printed where the model names none
        wk = re.search(r"For U\.S\. services the weakest is (L\d+), (since [^.]+)\.", lp["evidence_summary"])
        if wk and wk.group(1) == x:
            more += f" The atlas names it the weakest step for U.S. services, \u201c{ce(wk.group(2))}\u201d."
        # Loop R10's supposition comes before the step it sets up, as Loop B4's does in the ready line (the data lead's
        # batch 6 suggestion): it opens the step's line, in regular weight, so the status line says it first
        lead = ""
        if i == 0 and lid == "R10":
            s_, v_ = START["R10"]
            lead = f"Start at {in_sentence(s_)}, and suppose they {v_}."

        if b == "C3" or a == "C3":
            if lid == "B4" and b == "C3":
                more += f" {in_sentence('C3', True)} is the variable both loops pass through."
            if lid == "R10" and b == "C3":
                more += f" Here Loop R10 reaches {in_sentence('C3')}, the variable Loop B4 also passes through."
        if closes:
            # where the change ends up (R2, item 4), in Rule 15.6's words for the kind: a balancing loop pushes back
            # against the first change, a reinforcing one feeds itself on top of it
            m_ = C15.minus_count(lp["links"])
            first = "fall" if dirs[lid][0]["cause_up"] is False else "rise"
            back = d["effect_up"] == dirs[lid][0]["cause_up"]
            need(back == (KIND[lid] == "reinforcing"), f"Loop {lid} ends against its kind")
            end = says(codes[0], d["effect_up"], d["effect_can"], subject=False)
            if KIND[lid] == "balancing":
                t_, v_ = end.rsplit(" ", 1) if not d["effect_can"] else (end, "")
                where = f"{t_} now {v_}".strip() + f", against the first {first}"
                acts = "can push back" if d["effect_can"] else "pushes back"
            else:
                where = f"{end} again, on top of the first {first}"
                acts = "can feed itself" if d["effect_can"] else "feeds itself"
            signs = f"its {words_n(m_)} minus sign{'' if m_ == 1 else 's'} show{'s' if m_ == 1 else ''}"
            more += (f" Loop {lid} is back where it began, and {where}. The loop {acts}, so it is {KIND[lid]}, as {signs}.")
            if lid == "R10":
                more += " The atlas holds no measure of either loop’s strength, so the walk weighs neither against the other."
        need(KIND[lid] == ("reinforcing" if C15.minus_count(lp["links"]) % 2 == 0 else "balancing"), f"Loop {lid}'s kind changed")
        said = f"Loop {lid}, step {i + 1} of {n}: {(lead + ' ') if lead else ''}{line} {re.sub(r'<[^>]+>', '', html.unescape(more))}"
        hold = max(6000, 250 * len(said.split()))
        out.append({"k": k, "loop": lid, "i": i + 1, "n": n, "link": x, "line": line, "lead": lead, "more": more, "hold": hold, "said": said,
                    "dir": d})
    need(f2["loops"]["B4"]["into_C3"] == "L23" and f2["loops"]["R10"]["into_C3"] == "L25", "Variable C3's steps changed")
    return out


def drawing(lid, numbered=True, shared=frozenset({"C3"}), labels=None, live=True):
    """One loop drawn by chapter 15's own function (three_loop for B4, four_loop for R10) with steps_g, each step's group
    renumbered to its place in the walk (data-s, 1 to 7) and each pill keyed by loop and variable (data-p). The step
    numbers drawn stay the atlas's, 1 to 3 and 1 to 4 (Rule 15.6)."""
    lp = LOOP[lid]
    codes = [c for c, _ in lp["chain"]]
    if len(codes) == 3:
        body, h = C15.three_loop(codes, lp["links"], inside=(lid, KIND[lid]), shared=set(shared), steps_g=live,
                                 numbered=numbered, labels=labels)
    else:
        body, h = C15.four_loop(codes, lp["links"], inside=(lid, KIND[lid]), shared=set(shared), steps_g=live,
                                numbered=numbered, labels=labels)
    walk_no = {x: k for k, (l_, x) in enumerate(WALK, 1) if l_ == lid}
    if not live:            # a still picture: no step or pill groups, no band
        need("data-s=" not in body and 'class="bd"' not in body, f"Loop {lid}'s still drawing carries a stepper's groups")
        return C15.svg_wrap(body, h), h
    n_s = len(re.findall(r'data-s="\d+"', body))
    n_p = len(re.findall(r'data-p="\d+"', body))
    need(n_s == len(lp["links"]) and n_p == len(codes), f"Loop {lid}'s drawing lost a step or pill group ({n_s}, {n_p})")
    body = re.sub(r'data-s="(\d+)"', lambda m: f'data-s="{walk_no[lp["links"][int(m.group(1)) - 1]]}"', body)
    body = re.sub(r'data-p="(\d+)"', lambda m: f'data-p="{lid}-{codes[int(m.group(1))]}"', body)
    if numbered:
        drawn = [int(x) for x in re.findall(r'<tspan class="sn">(\d+)</tspan>', body)]
        need(drawn == list(range(1, len(lp["links"]) + 1)), f"Loop {lid} numbers its steps {drawn}; Rule 15.6 sets 1 to n")
    return C15.svg_wrap(body, h), h


def walk_css(steps):
    """The drawing follows the stepper's data-oa-at (CE-1), as chapter 15's stepper_css does for one loop: steps before
    the current one in ink, the current one on the selected band with its words bold, steps ahead and the variables not
    yet reached muted, each line keeping its grade's pattern. Variable C3, filled in ink in both drawings, is never muted.
    No red. The list's counter starts again at each loop's first step, so its numbers are the drawn ones (Rule 15.6)."""
    MUTED, BAND = C15.MUTED, C15.BAND
    pills = {}
    for st in steps:
        lp = LOOP[st["loop"]]
        codes = [c for c, _ in lp["chain"]]
        a, b = codes[st["i"] - 1], codes[st["i"] % st["n"]]
        pills[st["k"]] = (f"{st['loop']}-{a}", f"{st['loop']}-{b}")
    every = sorted({p for ab in pills.values() for p in ab})
    out = []
    n = len(steps)
    for k in range(n + 1):
        s_ = f'[data-oa-at="{k}"]'
        lit = {f"B4-{START['B4'][0]}"} if k == 0 else set(pills[k])
        reached = set(lit) | {p for j in range(1, k + 1) for p in pills[j]}
        mute = [f'{s_} [data-s="{i}"]' for i in range(k + 1, n + 1)]
        mute += [f'{s_} [data-p="{p}"]' for p in every if p not in reached and not p.endswith("-C3")]
        if mute:
            out.append(",".join(mute) + f"{{--k:{MUTED};--t:{MUTED}}}")
        out.append(",".join(f'{s_} [data-p="{p}"]' for p in sorted(lit)) + f"{{--f:{BAND}}}")
        if k:
            out.append(f'{s_} [data-s="{k}"] .bd{{display:inline}}{s_} [data-s="{k}"] text{{font-weight:var(--oa-font-weight-bold)}}')
    # the still sequence as a hanging list: each number in its own column, the step's words beside it, and each loop's
    # first step headed by its chip and its count of steps
    out.append(".lv>.oa-stepper-status{margin-top:20px}.lv>.oa-stepper-why{margin-bottom:16px}"
               ".lv>.oa-stepper-steps+.k{margin-top:20px}")
    out.append(".oa-stepper-step{display:grid;grid-template-columns:1.6em minmax(0,1fr);align-items:start}"
               ".oa-stepper-step::before{grid-column:1;grid-row:1/span 2;margin-right:0}"
               ".oa-stepper-step>*{grid-column:2}"
               ".oa-stepper-step[data-oa-first]{counter-set:st 0}"
               ".oa-stepper-step[data-oa-first]::before{grid-row:2/span 2}"
               ".oa-stepper-step .lpn{grid-row:1;display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 6px;"
               "font:var(--oa-type-caption);color:var(--oa-color-text-secondary)}"
               # Loop R10's supposition, on its own line before the step's direction, in the regular weight
               ".oa-stepper-line .sup8{display:block;margin-bottom:2px;font-weight:var(--oa-font-weight-regular)}")
    return "".join(out)


def rule_14_143():
    f2 = FACTS["example_2"]
    b4, r10 = LOOP["B4"], LOOP["R10"]
    steps = walk_steps()
    need(len(steps) == 7 and [s["link"] for s in steps] == ["L23", "L24", "L54", "L08", "L25", "L53", "L42"], "the walk changed")
    svgs = {lid: drawing(lid)[0] for lid in ("B4", "R10")}
    ctl = C15.code_part("c-18-loop-stepper.html", r'<div\s+class="oa-stepper-controls".*?</button>\s*</div>')
    ctl = ctl.replace('aria-label="Steps of the loop"', 'aria-label="Steps of Loops B4 and R10"')
    need('aria-label="Steps of Loops B4 and R10"' in ctl, "Rule 18.22's group name changed")
    why = C15.code_part("c-18-loop-stepper.html", r'<p class="oa-stepper-why".*?</p>')
    need('id="oa-stepper-why"' in why and ctl.count('aria-describedby="oa-stepper-why"') == 2,
         "Rule 18.22's reason line and the two buttons that name it changed")
    s0, v0 = START["B4"]
    ready = (f"Ready. Both loops pass through {in_sentence('C3')}. Start in Loop B4 at {in_sentence(s0)}, and suppose it "
             f"{v0}. Press Play, or Next step to follow one connection at a time.")
    lis = []
    for st in steps:
        first = st["i"] == 1
        tag = (f'<span class="lpn">{chip("Loop", st["loop"])}&#32;{words_n(st["n"])} steps</span>' if first else "")
        lis.append(f'<li class="oa-stepper-step" data-oa-part="Loop {st["loop"]}"{" data-oa-first" if first else ""} '
                   f'data-oa-hold="{st["hold"]}">{tag}<span class="oa-stepper-line">'
                   + (f'<span class="sup8">{e(st["lead"])}</span>&#32;' if st["lead"] else "") + f'{e(st["line"])}</span>&#32;'
                   f'<span class="oa-stepper-more">{st["more"]}</span></li>')
    cols = []
    for lid in ("B4", "R10"):
        lp = LOOP[lid]
        grades = {link(x)["evidence"] for x in lp["links"]}
        lab = (diagram_label(grades.pop(), f"{GRADE[link(lp['links'][0])['evidence']][1]}, the grade of all "
                                           f"{words_n(len(lp['links']))} steps")
               if len(grades) == 1 else C15.label_for(lp["links"], "the grade of the loop’s least certain step"))
        # the grade label and its gloss above the loop's chip and title, as Rule 13.1 sets and chapter 15's plates print
        # them, Rule 15.15's two loops included (DF-6)
        cols.append(f'<div>{lab}{C15.hed("Loop", lid, curl(lp["title"]))}'
                    f'<div class="dw dg{" b4w" if lid == "B4" else ""}">{svgs[lid]}</div></div>')
    # side by side, Loop B4's drawing drops so its filled pill for Variable C3 shares one line with Loop R10's (the design
    # director's DD-C2): the two pills' centers read from the drawings themselves
    def c3_mid(svg, key):
        m = re.search(r'data-p="' + key + r'"[^>]*>\s*<rect class="pl[^"]*" x="[^"]+" y="([\d.]+)" width="[^"]+" height="([\d.]+)"', svg)
        need(m is not None, f"no pill {key} in its drawing")
        return float(m.group(1)) + float(m.group(2)) / 2
    drop = round(c3_mid(svgs["R10"], "R10-C3") - c3_mid(svgs["B4"], "B4-C3"))
    need(0 <= drop <= 160, f"Loop B4's drawing would drop {drop} px to meet Loop R10's pill")
    shared = (f'<p class="nt">{C15.vt("C3")} is the pill filled in ink in both drawings: both loops pass through it. '
              f'Each loop numbers its steps from where the atlas starts it.</p>'
              # the ticks and the dashed step, which no other words on the plate read (the reader panel's RP-9)
              + loop_key(b4["links"] + r10["links"]))
    limits = (f'<p class="k">The atlas’s limits on the two loops</p>'
              f'<p class="nt">{chip("Loop", "B4")} “{ce(b4["qualification"])}”</p>'
              f'<p class="nt">{chip("Loop", "R10")} “{ce(r10["qualification"])}”</p>')
    root = (f'<div class="oa-stepper lv" data-oa-stepper>'
            f'<div class="cfx pr">{"".join(cols)}</div>{shared}'
            f'<p class="oa-stepper-status" role="status" data-oa-ready="{e(ready)}">{e(ready)}</p>'
            # the buttons sit right under the drawings and the status line, so a window shows the drawing that lights
            # and the button that lights it together (the design director's DD-C1, the accessibility lead's 2.8): the
            # order in the markup, never by CSS; the still list follows
            f'{ctl}{why}<ol class="oa-stepper-steps" role="list">{"".join(lis)}</ol>{limits}'
            + src("loops B4 and R10 and connections L23, L24, L54, L08, L25, L53 and L42") + "</div>")
    css_live = (walk_css(steps) + f"@container oa-frame (min-width:680px){{.b4w{{padding-top:{drop}px}}}}"
                ".lk8{margin-top:12px}")
    style = plate_style(root, swap={C15.stepper_css(3): css_live})
    alt = (f"Loop B4 from our systems atlas, “{b4['title']}”, beside Loop R10, “{r10['title']}”, each drawn "
           f"with its steps numbered from 1, and Variable C3, {lc(short('C3'))}, the pill filled in ink in both. Under them "
           "the loop stepper of Rule 18.22: a status line, the seven steps in order, Loop B4’s three then Loop R10’s "
           "four, and four buttons, Play, Reset the loop, Previous step and Next step. The current step lights in its "
           "drawing and in the list. With scripts off or in print, the list shows every step in order.")
    files = {"s-14-143-correct": fragment("s-14-143-correct", root, style)}
    meta = {"s-14-143-correct": plate_meta(alt, interactive=True, keys=True,
                                           notes="Rule 18.22's markup with no script of its own (CE-1); loops drawn by "
                                                 "phase3_ch15_build.py's three_loop and four_loop, imported read-only; every "
                                                 "word of the steps read from the atlas's loop and connection records.")}
    # the failure: the two loops read as one loop of seven steps, numbered 1 to 7, its minus signs counted together
    fcols = []
    for lid in ("B4", "R10"):
        svg, _ = drawing(lid, numbered=True, live=False)
        offs = 0 if lid == "B4" else 3
        svg = re.sub(r'<tspan class="sn">(\d+)</tspan>', lambda m: f'<tspan class="sn">{int(m.group(1)) + offs}</tspan>', svg)
        cols_svg = re.sub(r'<text class="id"[^>]*>.*?</text>', "", svg, flags=re.S)
        fcols.append(f'<div><div class="dg">{cols_svg}</div></div>')
    m_all = C15.minus_count(b4["links"] + r10["links"])
    need(m_all == 3, "the two loops' minus signs changed")
    fail = (dnp() + f'<p class="hed"><span>“One loop through the risk of losing office: seven steps, '
            f'{words_n(m_all)} minus signs, balancing”</span></p><div class="cfx pr">{"".join(fcols)}</div>'
            '<ol class="fl7">' + "".join(f"<li>{e(st['line'])}</li>" for st in steps) + "</ol>")
    fstyle = plate_style(fail, extra=".fl7{margin:12px 0 0;padding-left:1.4em;font:var(--oa-type-body-small)}"
                                      ".fl7 li+li{margin-top:4px}")
    files["s-14-143-failure"] = fragment("s-14-143-failure", fail, fstyle)
    meta["s-14-143-failure"] = plate_meta(
        FC + "The two loops drawn side by side with their steps numbered 1 to 7 as one sequence and no loop names inside "
        "them, under a label that calls them one loop of seven steps, three minus signs, balancing. A list of the seven steps "
        "follows with no word of which loop each belongs to.",
        notes="Labeled failure, a still picture: the two loops read as one, its kind taken from the minus signs of both.")
    n = len(steps)
    entry = {
        "id": "14.143",
        "title": "Step through two loops that share a\u00a0variable, one connection at a time.",
        "rule": [
            f"When two loops from our systems atlas pass through one variable, step the reader through both on one loop "
            f"stepper (Rule 18.22), one loop after the other, each in the atlas’s own order. Loop B4, "
            f"“{curl(b4['title'])}”, and Loop R10, “{curl(r10['title'])}”, share Variable C3, "
            f"{lc(short('C3'))}. Draw them side by side with that variable filled in ink in both (Rule 15.15), number each "
            f"loop’s steps from 1 as the atlas starts it (Rule 15.6), and let the status line say which loop each step "
            f"belongs to.",
            "Start each loop from a rise or a fall, and say each step in the direction the walk runs, cause first, as in "
            f"“{steps[0]['line']}” After a step the atlas grades plausible, say “can” to the end of the loop. At the last "
            "step, say that the loop is back where it began, whether it pushes back or feeds itself, and name its kind. Say "
            "too where the second loop reaches the shared variable. Print every step in order wherever nothing can move: on paper, with motion "
            "reduced and with scripts off (Rule 15.19). Keep each loop’s own numbers and kind, and leave out any word that "
            "one loop outweighs the other, since the atlas holds no measure of a loop’s strength (Rule 15.21).",
        ],
        "use_when": None,
        "use_instead": [],
        "why": {"text": [
            "A variable two loops share is where one loop can weaken the other. As primaries decide more seats in Loop R10, "
            "the risk of losing office falls, and in Loop B4 that same risk is what turns poor service into defeats. Stepping "
            "through both loops one connection at a time lets a reader watch the one variable at work in each, and each "
            "loop’s own numbers and kind stop the two from reading as one."],
            "basis": "Our systems atlas, Loops B4 and R10; the stepper and still-sequence lessons of LOOPY, as Rule 18.22 sets them"},
        "specimen": None,
        "tier": None,
        "tokens": ["oa.color.state.selected.band", "oa.color.state.selected.bar", "oa.color.state.muted.text",
                   "oa.color.graphic.essential.onNewsprint"],
        "related": ["15.6", "15.15", "15.19", "15.21", "18.22"],
        "builders": ("Carry Rule 18.22’s markup and let chapter 18’s script run it; never copy the script. Name each "
                     "step’s loop with <code>data-oa-part</code>, light each drawing from the stepper’s "
                     "<code>data-oa-at</code>, and start the list’s counter again at each loop’s first step, so the "
                     "number said, the number listed and the number drawn agree."),
        "specs": [
            {"label": "Component", "value": "The loop stepper of Rule 18.22: one status line, one list and one set of buttons for both loops"},
            {"label": "Order", "value": "Loop B4’s three steps, then Loop R10’s four, each in the atlas’s order"},
            {"label": "Shared variable", "value": "Its own title in both drawings and every step, its pill filled in ink (Rule 15.15)",
             "token": "oa.color.graphic.essential.onNewsprint"},
            {"label": "Current step", "value": "The selected band behind its line and its two pills, in ink, never in red",
             "token": "oa.color.state.selected.band"},
            {"label": "Status line", "value": "The loop and its own count, as “Loop R10, step 2 of 4”, then the step’s words"},
            {"label": "Still sequence", "value": "Every step numbered and in ink, buttons hidden, on paper, with motion reduced and with scripts off"},
        ],
        "correct": dict({"specimen": "s-14-143-correct",
                         "caption": (f"Loops B4 and R10 on the loop stepper of Rule 18.22, live: {words_n(n)} steps, Loop "
                                     "B4’s three and then Loop R10’s four, each with its connection, grade and "
                                     "delay. Both drawings fill the pill of Variable C3, risk of losing office, in ink, and the "
                                     "status line names each step’s loop.")},
                        **meta["s-14-143-correct"]),
        "failure": dict({"specimen": "s-14-143-failure",
                         "caption": ("<strong>Fails Rule 14.143.</strong> The walk numbers the two loops 1 to 7 as one loop "
                                     "and counts their three minus signs together to call it balancing. The atlas holds two "
                                     "loops, Loop B4 balancing and Loop R10 reinforcing, which share one variable.")},
                        **meta["s-14-143-failure"]),
        # ruling (g): two examples, one a loop, in the domains Rule 15.15 logs them under (read from chapter 15's own log
        # calls, so the two chapters cannot part)
        "examples": [
            {"example": f"Loop {lid}, {what}, stepped through the risk of losing office", "domain": dom, "states": [],
             "level": "federal", "where": "14.143"} for lid, what, dom in LOG_143],
    }
    return entry, files, steps


# =====================================================================================================================
# Rule 14.144: Reforms R-06, R-30 and R-38 on Loop R8, compared with no total (ruling d)
# =====================================================================================================================
RIDS = ["R-06", "R-30", "R-38"]
LAYER = {"core": "the core layer", "economy": "the economy layer", "technology": "the technology layer"}


def r8_drawing(rids, chosen_first=True, failure=False):
    """Loop R8 alone (ruling d), drawn by chapter 15's two_loop with every on-loop target of the offered reforms marked
    ready under data-red; the first reform's targets red in the markup, each target's group naming the reforms it
    belongs to (data-oa-for), so the chosen reform's red shows through the plate's CSS, scripts on or off."""
    lp = LOOP["R8"]
    codes = [c for c, _ in lp["chain"]]
    on = set(codes) | set(lp["links"])
    owner = {}
    for rid in rids:
        for t in REFORM[rid]["targets"]:
            if t in on:
                owner.setdefault(t, []).append(rid)
    need(owner == {"L39": ["R-06", "R-30"], "A5": ["R-30"]}, f"the reforms' targets on Loop R8 changed: {owner}")
    body, h, _ = C15.two_loop(codes, lp["links"], inside=("R8", "reinforcing"), targets=set(owner))
    first = set(REFORM[rids[0]]["targets"])
    # each step's group in the atlas's order: L38 carries no target, L39 does
    groups = list(re.finditer(r'<g class="wr( rt)?"([^>]*)>', body))
    need(len(groups) == 2 and groups[0].group(1) is None and groups[1].group(1) == " rt", "Loop R8's drawing changed")
    m = groups[1]
    body = body[:m.start()] + f'<g class="wr{" rt" if "L39" in first else ""}"{m.group(2)} data-oa-for="{" ".join(owner["L39"])}">' + body[m.end():]
    # the pills: A5 is a target of R-30 alone; its outline turns red when R-30 is chosen, so it carries data-red now
    pills = list(re.finditer(r'(<rect class="pl([^"]*)"[^>]*/>)(<text class="t[^"]*"[^>]*>.*?</text>)', body))
    need(len(pills) == 2, "Loop R8's pills changed")
    out, last = [], 0
    for c, pm in zip(codes, pills):
        rect, txt = pm.group(1), pm.group(3)
        if c in owner:
            red = c in first
            rect = re.sub(r'class="pl([^"]*)"', lambda q: 'class="pl' + (" rp" if red else "") + q.group(1).replace(" rp", "") + '"', rect)
            seg = f'<g data-oa-for="{" ".join(owner[c])}">{rect}{txt}</g>'
        else:
            seg = rect + txt
        out.append(body[last:pm.start()] + seg)
        last = pm.end()
    body = "".join(out) + body[last:]
    return C15.svg_wrap(body, h), owner


def effect_cell(code):
    """An effect as the atlas stores it, its qualifier whole after the code, then the code's words; a zero says so."""
    head = code.split(" ")[0]
    need(head in C13.EFFECT_WORDS, f"effect {code!r} has no code")
    return (f'<b class="cd">{e(code.replace("-", MINUS, 1) if code.startswith("-") else code)}</b>'
            f',&#32;<span class="cw">{e(C13.EFFECT_WORDS[head])}</span>')


def target_words(t):
    if t in LINK:
        l = link(t)
        return f'{chip("Connection", t)} “{ce(l["name"])}”, {GRADE[l["evidence"]][0].lower()}'
    return f'{chip("Variable", t)} “{ce(node(t)["title"])}”'


def reaches(start, goal):
    """Whether any chain of the model's connections, at any length, runs from the variable start into one of goal."""
    seen, todo = {start}, [start]
    while todo:
        x = todo.pop()
        for l in LINK.values():
            if l["from"] == x and l["to"] not in seen:
                seen.add(l["to"])
                todo.append(l["to"])
    return bool(seen & set(goal))


def counted(ts):
    n_l = sum(1 for t in ts if t in LINK)
    n_v = len(ts) - n_l
    return " and ".join(p for p in (f"{words_n(n_l)} connection{'s' if n_l != 1 else ''}" if n_l else "",
                                    f"{words_n(n_v)} variable{'s' if n_v != 1 else ''}" if n_v else "") if p)


def layer_of(t):
    return LINK[t]["layer"] if t in LINK else NODE[t]["layer"]


def say_line(rid, on):
    """The line the status line says (the data lead's A-2, item 3): the marks that turn red on the drawing, none included,
    then the targets outside the loop with their layer. It never says a reform acts on the loop through anything, and no
    punctuation touches a chip (BC S16)."""
    r = REFORM[rid]
    mine = [t for t in r["targets"] if t in on]
    off = [t for t in r["targets"] if t not in on]
    lays = sorted({LAYER[layer_of(t)] for t in off})
    s = f'{chip("Reform", rid)} turns {counted(mine) if mine else "no mark"} red.'
    if off and mine:
        s += (f' One {counted(off).split(" ", 1)[1]} it targets sits outside this loop, in {" and ".join(lays)}.'
              if len(off) == 1 else f' {counted(off).capitalize()} it targets sit outside this loop, in {" and ".join(lays)}.')
    elif off:
        s += f' Its {words_n(len(off))} targets sit outside this loop, in {" and ".join(lays)}.'
    return s


def card_say(rid, on):
    """The card's first line (CD-S10): the status line's words with the reform's chip dropped from the screen, since the
    card's head names it, and kept for the status line in a visually hidden prefix, so a reader who hears the line alone
    still hears which reform it is."""
    full = say_line(rid, on)
    head = f'{chip("Reform", rid)} '
    need(full.startswith(head + "turns "), f"Reform {rid}'s line no longer starts on its chip and “turns”")
    rest = full[len(head):]
    return f'<span class="vh">Reform {e(rid)}: </span>{rest[0].upper()}{rest[1:]}'


def loop_key(lids):
    """A key for the marks a loop drawing carries and no other words read (the reader panel's RP-9): the delay ticks, in
    the words of chapter 15's own keys (ticks_line, Rules 13.5 and 15.13), and, where a drawing holds a dashed step, the
    grade its pattern draws (Rule 13.4). Each sample is drawn by chapter 15's conn, read-only."""
    sv = '<svg class="sv" viewBox="0 0 64 18" width="64" height="18" aria-hidden="true" focusable="false">'
    delays = [k for k in ("S", "M", "L") if any(link(x)["delay"] == k for x in lids)]
    tick, _ = C15.conn([(1, 9), (61, 9)], "documented", None, delays[-1])
    rows = [f'<p class="kd2">{sv}{C15.wr(tick)}</svg><span><b>Ticks</b> near a line’s start count its delay, '
            f'{C15.ticks_line(lids)}.</span></p>']
    grades = {link(x)["evidence"] for x in lids}
    if "plausible" in grades:
        need(grades <= {"documented", "well-supported", "plausible"}, "a loop here holds a grade the key does not name")
        dash, _ = C15.conn([(1, 9), (61, 9)], "plausible", None, None)
        rows.append(f'<p class="kd2">{sv}{C15.wr(dash)}</svg><span><b>Dashed</b> for a step the atlas grades plausible; '
                    f'every other step is solid, documented or well supported (Rule 13.4).</span></p>')
    return '<div class="lk8">' + "".join(rows) + "</div>"


def off_words(rid, t, loop_vars):
    """An off-loop target in words (A-2, item 2): its typed chip, the atlas's title, for a connection its grade and its two
    ends, and its layer."""
    if t in LINK:
        # its layer right after its own name and grade, before its two ends, so a reader never takes the connection's layer
        # for its end variable's (the reader panel's RP-7: LT12 sits in the technology layer, Variable EC9 in the economy)
        l = link(t)
        return (f'{chip("Connection", t)} \u201c{ce(l["name"])}\u201d, {GRADE[l["evidence"]][0].lower()}, in '
                f'{LAYER[l["layer"]]}, from {chip("Variable", l["from"])} to {chip("Variable", l["to"])} '
                f'\u201c{ce(node(l["to"])["title"])}\u201d')
    return f'{chip("Variable", t)} \u201c{ce(node(t)["title"])}\u201d, in {LAYER[NODE[t]["layer"]]}'


def off_note(rid, off, loop_vars):
    """What the model holds about the off-loop targets and the loop (A-2, items 2 and 4), checked by search: a target
    from which no chain of connections reaches the loop, and a connection that leaves the loop and runs outward."""
    starts = []
    for t in off:
        if t in LINK:
            if LINK[t]["from"] in loop_vars:
                need(not reaches(LINK[t]["to"], loop_vars), f"{t} now leads back into the loop")
                return (f'{chip("Connection", t)} leaves the loop at {chip("Variable", LINK[t]["from"])} and runs outward.')
            starts += [LINK[t]["from"], LINK[t]["to"]]
        else:
            starts.append(t)
    need(not any(reaches(x, loop_vars) for x in starts), f"a target of {rid} now reaches Loop R8")
    one = len(off) == 1
    tail = ("That target sits outside the loop, and the atlas holds no connection from it into the loop." if one else
            "Neither target sits on the loop, and the atlas holds no connection from either into the loop.")
    return f'Its record names {chip("Loop", "R8")} as a loop it acts on. {tail}'


def chooser_css(rids):
    """The choice through CSS from the checked radio (the accessibility lead's 3.3, CE-2), so it works with scripts off:
    the chosen reform's targets on the drawing turn red, as Rule 15.20's plate draws them, and its card takes the selected
    bar. Every card stays in view: this plate compares all three. A target of a reform not chosen goes back to the loop's
    own weight, its 6 px ink case included: chapter 15's red-target rule (.crt .ak-case), which the first reform's targets
    carry in the markup, would otherwise keep Connection L39 drawn heavy with Reform R-38 chosen (NB-M3)."""
    INK = C15.INK
    out = []
    for rid in rids:
        has = f'.p:has([value="{rid}"]:checked)'
        no, yes = f'{has} [data-oa-for]:not([data-oa-for~="{rid}"])', f'{has} [data-oa-for~="{rid}"]'
        out.append(f'{no} .hi,{yes} .lo{{display:none}}{no} .lo,{yes} .hi{{display:inline}}'
                   f'{no} .pl{{stroke:{INK};stroke-width:2px}}{no} .ak-mark{{stroke:{INK};stroke-width:2px}}{no} .hd{{fill:{INK}}}'
                   f'{no} .ak-case{{stroke:none}}'
                   f'{yes} .ak-mark{{stroke:var(--oa-color-data-emphasis-red);stroke-width:4px}}'
                   f'{yes} .ak-case{{fill:none;stroke:{INK};stroke-width:6px}}{yes} .hd{{fill:var(--oa-color-data-emphasis-red)}}'
                   f'{yes} .pl{{stroke:var(--oa-color-data-emphasis-red);stroke-width:3px}}'
                   f'{has} [data-oa-panel="{rid}"]{{border-top-color:var(--oa-color-state-selected-bar)}}'
                   f'{has} [data-oa-panel="{rid}"] .ch{{font-weight:var(--oa-font-weight-bold)}}')
    prints = ",".join(f'.p:has([value="{rid}"]:checked) [data-oa-print="{rid}"]' for rid in rids)
    return f"@supports selector(:has(*)){{{''.join(out)}@media print{{{prints}{{display:block}}}}}}"


CARD_CSS = (
    ".cds{list-style:none;margin:16px 0 0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);gap:20px}"
    ".cd8{border-top:4px solid var(--oa-color-border-hairline);padding-top:10px}"
    ".cd8 .ch{margin:0 0 6px;font:var(--oa-type-body-small)}"
    ".cd8 dl{margin:10px 0 0}.cd8 dl>div{padding:8px 0;border-top:1px solid var(--oa-color-border-hairline)}"
    ".cd8 dt{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);"
    "text-transform:var(--oa-type-label-text-transform);color:var(--oa-color-text-secondary);margin:0 0 4px}"
    ".cd8 dd{margin:0;font:var(--oa-type-body-small)}.cd8 dd+dd{margin-top:4px}"
    ".cd8 .cd{font-weight:var(--oa-font-weight-semibold);font-variant-numeric:tabular-nums;white-space:nowrap}"
    ".cd8 .oa-disclosure-set{margin-top:12px}.cd8 .on8{color:var(--oa-color-text-secondary)}"
    ".rl8{list-style:none;margin:0;padding:0}.rl8 li+li{margin-top:8px}.rl8 .rn,.rl8 .rw{display:block}"
    ".rl8 .rw{color:var(--oa-color-text-secondary)}"
    ".ky8{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:4px 16px;font:var(--oa-type-caption)}"
    ".ky8 b{font-variant-numeric:tabular-nums}.ky8 li{display:flex;align-items:center;gap:8px}.pon{display:none}"
    # the effects' rows (Rule 13.5's mark beside each code, as Rule 15.20's panel sets them), the two grades and the
    # routes' lines
    ".cd8 .ef8{list-style:none;margin:0;padding:0}.cd8 .ef8>li{padding:6px 0}"
    ".cd8 .ef8>li+li{border-top:1px solid var(--oa-color-border-hairline)}.cd8 .fn8{display:block}"
    ".fv8{display:flex;flex-wrap:wrap;align-items:center;gap:4px 12px;margin-top:4px}"
    ".cd8 .gd8 dd+dd{margin-top:10px}.cd8 .gd8 .evr{margin:0}.rl8 .rf{display:block}"
    # the phone line-up (CR-S3): a family a block, its three reforms one a row, the chip beside the pips and the code
    ".ph8{margin-top:16px}.pt8,.pr8{list-style:none;margin:0;padding:0}.pt8>li{padding:8px 0;border-top:1px solid "
    "var(--oa-color-border-hairline)}.pt8 .fn8{font:var(--oa-type-body-small);font-weight:var(--oa-font-weight-semibold)}"
    ".pr8>li{display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:10px;align-items:center;margin-top:6px;"
    "font:var(--oa-type-body-small)}.pr8 .fv8{margin-top:0}"
    "@container oa-frame (min-width:680px) and (min-width:40em){.ph8{display:none}}@media print{.ph8{display:none}}"
    ".lk8{margin-top:12px}"
    # on the 680 px stage the three cards stand side by side, and each row of one card lines up with the same row of the
    # others: a card spans thirteen rows of the list's grid (its head, the eleven rows of its list, its disclosure), its
    # list eleven. Three columns only while the frame holds 40em of the plate's own text as well (680 px at the guide's
    # 17 px), so text set larger (1.4.4: 200 percent, or a larger default) takes one card a row, as a phone does
    "@container oa-frame (min-width:680px) and (min-width:40em){.cds{grid-template-columns:repeat(3,minmax(0,1fr));column-gap:20px;"
    "grid-template-rows:repeat(13,auto);row-gap:0}"
    "@supports (grid-template-rows:subgrid){.cd8{display:grid;grid-row:span 13;grid-template-rows:subgrid;row-gap:0}"
    ".cd8 dl{display:grid;grid-row:span 11;grid-template-rows:subgrid;row-gap:0}"
    # the effects' heading and its four family rows take five of the list's rows, so each family lines up across the cards
    ".cd8 .ef8g{display:grid;grid-row:span 5;grid-template-rows:subgrid;row-gap:0}"
    ".cd8 .ef8g>dd,.cd8 .ef8{display:grid;grid-row:span 4;grid-template-rows:subgrid;row-gap:0}}}"
    ".pcs8{display:none}"
    "@media print{.lv>.oa-choice{display:none}.pcs8{display:grid;grid-template-columns:repeat(auto-fill,296px);gap:16px 24px;"
    "margin-top:16px}.pcs8 .pc8{break-inside:avoid}.mn8,.lv [data-oa-print]{display:none!important}}"
)


def rule_14_144():
    f3 = FACTS["example_3"]
    lp = LOOP["R8"]
    codes = [c for c, _ in lp["chain"]]
    on = set(codes) | set(lp["links"])
    need(sorted(lp["reforms"]) == ["R-30"] and all("R8" in REFORM[r]["loops"] for r in RIDS),
         "the loop's and the reforms' lists of Loop R8 changed (ruling d)")
    svg, owner = r8_drawing(RIDS)
    check_ = C15.code_part("c-18-choice.html", r'<svg\s+class="oa-choice-check".*?</svg>')
    chev = C15.code_part("c-18-disclosure.html", r'<svg\s+class="oa-disclosure-chevron".*?</svg>')
    items = "".join(
        f'<label class="oa-choice-item"><input class="oa-choice-input" type="radio" name="s-14-144-reform" value="{rid}"'
        f'{" checked" if k == 0 else ""}><span class="oa-choice-face">{check_}<span class="oa-choice-label">'
        f'{chip("Reform", rid)} “{ce(REFORM[rid]["title"])}”</span></span></label>' for k, rid in enumerate(RIDS))
    group = (f'<fieldset class="oa-choice"><legend class="oa-choice-legend">Show one reform on Loop R8</legend>'
             f'<div class="oa-choice-row ch1">{items}</div></fieldset><p class="vh" role="status" data-oa-chooser-status></p>')
    lists_ = (f'<p class="nt">Each of these reforms names {chip("Loop", "R8")} in its own record; the loop’s record lists '
              f'{chip("Reform", "R-30")} only. The drawing marks a reform’s targets that sit on the loop, and each card '
              'lists the others in words with their layer.</p>')
    prints = "".join(f'<p class="nt pon" data-oa-print="{rid}">'
                     + (f'The drawing shows the targets of {chip("Reform", rid)} in red.' if any(t in on for t in REFORM[rid]["targets"])
                        else f'Neither target of {chip("Reform", rid)} sits on the drawing, so nothing on it turns red.')
                     + '</p>' for rid in RIDS)
    need({link(x)["evidence"] for x in lp["links"]} == {"well-supported"}, "Loop R8's grades changed")
    # the grade label above the loop's chip and title (Rule 13.1, DF-6)
    left = (diagram_label("well-supported", f"{GRADE['well-supported'][1]}, the grade of both steps") + C15.hed("Loop", "R8", curl(lp["title"]))
            + f'<div class="dw dg mn8">{svg}</div>{prints}')
    # on paper, one copy of the drawing for each reform, its targets on the loop drawn heavy (red prints as gray, so the
    # weight carries it), under a line that names them (the accessibility lead's 3.4); hidden on screen
    copies = []
    for rid in RIDS:
        tg = {t for t in REFORM[rid]["targets"] if t in on}
        cb, ch_, _ = C15.two_loop(codes, lp["links"], inside=("R8", "reinforcing"), targets=tg)
        named = " and ".join(f'{chip("Connection" if t in LINK else "Variable", t)}' for t in REFORM[rid]["targets"] if t in on)
        line = (f'{chip("Reform", rid)} on Loop R8: its target{"s" if len(tg) > 1 else ""} on the loop, {named}, drawn heavier than the rest of the loop.' if tg else
                f'{chip("Reform", rid)} on Loop R8: neither of its targets sits on the loop.')
        copies.append(f'<div class="pc8"><p class="nt">{line}</p><div class="dg">{C15.svg_wrap(cb, ch_)}</div></div>')
    pcopies = '<div class="pcs8">' + "".join(copies) + "</div>"
    # each step of the loop with its connection's chip, its name and its grade word (H11: an ID says what it refers to)
    # each step with its delay in words, and a key for the ticks that draw it (the reader panel's RP-9)
    right = ('<p class="k">Each step</p>' + "".join(
        f'<p class="nt"><b>{i}</b>&#160;{chip("Connection", x)} \u201c{ce(link(x)["name"])}\u201d, '
        f'{GRADE[link(x)["evidence"]][0].lower()}, and its effect takes {DELAY[link(x)["delay"]][1]}</p>'
        for i, x in enumerate(lp["links"], 1)) + loop_key(lp["links"]) + lists_)
    cards = []
    for rid in RIDS:
        r = REFORM[rid]
        rf = f3["reforms"][rid]
        mine = [t for t in r["targets"] if t in on]
        off = [t for t in r["targets"] if t not in on]
        offs = []
        for t in off:
            lay = (LINK[t]["layer"] if t in LINK else NODE[t]["layer"])
            offs.append(f"<dd>{off_words(rid, t, set(codes))}</dd>")
        # the effects as Rules 15.16 and 15.20 print them (the data lead's R5, DF-3): one heading, then one row a family in
        # the atlas's order, its name, Rule 13.5's pips from chapter 13's own pips_svg, and the code and qualifier whole
        # with the code's words. Each family's row lines up across the three cards (the design director's DD-R1); no row
        # adds them
        effs = ('<div class="ef8g"><dt>Effects by outcome family</dt><dd><ul class="ef8" role="list">'
                + "".join(f'<li><span class="fn8">{e(C13.FAMILY[f])}</span><span class="fv8">'
                          f'{C13.pips_svg(r["effects"][f].split(" ")[0])}<span>{effect_cell(r["effects"][f])}</span></span></li>'
                          for f in ("DQ", "GE", "EP", "EQ")) + "</ul></dd></div>")
        # each route as route_rows in phase3_ch15_build.py prints it (R5, DF-7): chip and name, who acts, the feasibility
        # word in bold, and the route's own check date or "Not checked", each on its own line
        routes = []
        for x in r["routes"]:
            when = f"Checked {C13.words_date(x['checked'])}" if x["checked"] else "Not checked"
            routes.append(f'<li><span class="rn">{chip("Route", x["route"])} {e(C13.ROUTE_NAME[x["route"]])}</span>'
                          f'<span class="rw">{ce(x["who"])}</span>'
                          f'<span class="rf"><b>{e(x["feasibility"].capitalize())}</b> feasibility</span>'
                          f'<span class="rf">{e(when)}</span></li>')
        rem = r["remedy_evidence"]
        disc = (f'<div class="oa-disclosure-set"><div class="oa-disclosure-stack"><details class="oa-disclosure">'
                f'<summary class="oa-disclosure-summary"><span class="oa-disclosure-label">The atlas’s evidence and '
                f'tradeoffs for {chip("Reform", rid)}</span>{chev}</summary><div class="oa-disclosure-body">'
                f'<p>The evidence for the remedy, {e(GRADE[rem["grade"]][0].lower())}: “{ce(rem["text"])}”</p>'
                f'<p>Its tradeoffs: “{ce(r["tradeoffs"])}”</p></div></details></div></div>')
        cards.append(
            f'<li class="cd8" data-oa-panel="{rid}"><div><p class="ch">{chip("Reform", rid)} “{ce(r["title"])}”</p>'
            # the card's head names the reform, so its first line starts on the verb (the creative director's CD-S10, the
            # craft reader's CR-S2); the status line, which reads this line alone, keeps the name in words a screen
            # shows nowhere
            f'<p class="nt" data-oa-say>{card_say(rid, on)}</p></div>'
            f'<dl>'
            f'<div><dt>Targets on Loop R8</dt>'
            + ("".join(f"<dd>{target_words(t)}</dd>" for t in mine) or "<dd>None</dd>") + "</div>"
            f'<div><dt>Targets outside this loop</dt>' + ("".join(offs) + (f'<dd class="on8">{off_note(rid, off, set(codes))}</dd>' if off else "")
                                                       or "<dd>None</dd>") + "</div>"
            # the band in the atlas's word and its definition, quoted, as Rules 15.11 and 15.20 print it (CE-S14)
            f'<div><dt>Band, the kind of change</dt><dd><b>{e(r["band"].capitalize())}</b>: “{ce(C15.BANDS[r["band"]])}”</dd></div>'
            + effs +
            # the two grades apart, each as Rule 15.16's grade_block prints it: the grade chip, Rule 13.3's gloss, then
            # the atlas's term (R5, DF-7)
            f'<div class="gd8"><dt>Its two grades, apart</dt>'
            f'<dd>{C15.grade_block(r["problem_evidence"]["grade"], "evidence of the problem")}</dd>'
            f'<dd>{C15.grade_block(rem["grade"], "evidence for the remedy")}</dd></div>'
            f'<div><dt>The atlas’s confidence in the effects</dt><dd>“{ce(r["effects_confidence"])}”</dd></div>'
            f'<div><dt>Routes, with the date each was checked</dt><dd><ul class="rl8">{"".join(routes)}</ul></dd></div>'
            f'</dl>{disc}</li>')
    order = ["+L", "+M", "+S", "0", "-S", "-M", "?"]
    need(list(C13.EFFECT_WORDS) == order, "the atlas's effect codes changed")
    key = ('<ul class="ky8">' + "".join(f'<li>{C13.pips_svg(c)}<span><b>{e(c.replace("-", MINUS))}</b> {e(C13.EFFECT_WORDS[c])}</span></li>'
                                        for c in order) + "</ul>")
    note = FACTS_NOTE()
    # where the cards stack one under another (a phone, or text set large), each family's effects for the three reforms
    # sit together before the cards, so a reader compares them without holding one card in mind across the others (the
    # craft reader's CR-S3, DD-R1's phone half). Rule 13.5's pips and each code whole, as in the cards; no total. Hidden
    # where the cards stand side by side and on paper, which prints the cards
    by_family = ('<div class="ph8"><p class="k">Each family’s effects, the three reforms together</p><ul class="pt8" role="list">'
                 + "".join(f'<li><p class="fn8">{e(C13.FAMILY[f])}</p><ul class="pr8" role="list">'
                           + "".join(f'<li>{chip("Reform", rid)}<span class="fv8">{C13.pips_svg(REFORM[rid]["effects"][f].split(" ")[0])}'
                                     f'<span>{effect_cell(REFORM[rid]["effects"][f])}</span></span></li>' for rid in RIDS)
                           + "</ul></li>" for f in ("DQ", "GE", "EP", "EQ"))
                 + "</ul></div>")
    body = (f'<div class="lv" data-oa-chooser>{group}' + C15.beside(left, right)
            + f'<p class="k kb">The three reforms compared, as of {SNAP}</p>'
            + key + f'<p class="nt">The atlas’s note on the codes: “{e(note)}”</p>'
            + by_family + pcopies + f'<ul class="cds" role="list">{"".join(cards)}</ul>'
            + src("reforms R-06, R-30 and R-38, their targets, effects, evidence and routes, and loop R8 with its "
                  "connections") + "</div>")
    style = plate_style(body, swap={C15.chooser_css(["R-03", "R-04"]): ""}, extra=chooser_css(RIDS) + CARD_CSS)
    files = {"s-14-144-correct": fragment("s-14-144-correct", body, style)}
    alt = ("A reform chooser on Loop R8 from our systems atlas: a group of three radio buttons, Reform R-06, Reform R-30 "
           "and Reform R-38, with R-06 chosen; the loop drawn as two pills with the chosen reform’s targets on it in "
           f"red; and three cards, one per reform, each with its targets on the loop and outside it, its band with the "
           f"atlas’s definition, its four effects one family to a row as of {SNAP}, each code and qualifier whole beside "
           "its pips, its two evidence grades apart, its routes each with its check date or not checked, and its evidence "
           "and tradeoffs one step away in a disclosure. No row adds the effects.")
    meta = {"s-14-144-correct": plate_meta(alt, interactive=True, keys=True,
                                           notes="Rule 18.3's choice and Rule 18.8's disclosure as their code sets write them; "
                                                 "the choice shows through the plate's own CSS from the checked radio, scripts "
                                                 "on or off; the status line is the shell's (C-2, CE-2). Every value read "
                                                 "from the atlas's reform and loop records.")}
    # the failure: a total row that adds each reform's four effect codes as points
    pts = {"S": 1, "M": 2, "L": 3}

    def points(v):
        m = re.match(r"([+\-])([SML])", v)
        return 0 if not m else (pts[m.group(2)] if m.group(1) == "+" else -pts[m.group(2)])
    tot = {rid: sum(points(REFORM[rid]["effects"][f]) for f in ("DQ", "GE", "EP", "EQ")) for rid in RIDS}
    need(tot == {"R-06": 5, "R-30": 5, "R-38": 2}, f"the failure's invented totals moved: {tot}")
    # one row a reform, so the picture holds whole in the 296 px column as well as at 680 px: its four codes in the
    # families' order, then the total the fault adds
    rows = "".join(f'<tr><th scope="row">{chip("Reform", rid)}</th><td>'
                   + ", ".join(f'<span class="cn8">{e(REFORM[rid]["effects"][f])}</span>' for f in ("DQ", "GE", "EP", "EQ"))
                   + f'</td><td class="f144-tt">+{tot[rid]}</td></tr>' for rid in RIDS)
    fam = ", ".join(lc(C13.FAMILY[f]) for f in ("DQ", "GE", "EP", "EQ"))
    fail = (dnp() + '<p class="hed"><span>\u201cWhich reform does the most for Loop R8?\u201d</span></p>'
            '<table class="ft8"><thead><tr><th scope="col">Reform</th><th scope="col">Effects</th>'
            f'<th scope="col">Total score</th></tr></thead><tbody>{rows}</tbody></table>'
            f'<p class="nt">Effects in the order {e(fam)}. Scored +S as 1, +M as 2 and +L as 3.</p>')
    fstyle = plate_style(fail, extra=(".ft8{border-collapse:collapse;margin-top:12px;font:var(--oa-type-body-small);width:100%}"
                                      ".ft8 th,.ft8 td{padding:6px 8px 6px 0;border-top:1px solid var(--oa-color-border-hairline);"
                                      "text-align:left;vertical-align:top}.ft8 thead th{border-top:0;font:var(--oa-type-label);"
                                      "letter-spacing:var(--oa-type-label-letter-spacing);text-transform:var(--oa-type-label-text-transform);"
                                      "color:var(--oa-color-text-secondary)}"
                                      ".ft8 .f144-tt{font-weight:var(--oa-font-weight-bold);font-variant-numeric:tabular-nums;"
                                      "text-align:right;white-space:nowrap}.ft8 thead th:last-child{text-align:right}.ft8 .cn8{white-space:nowrap}"
                                      "@container oa-frame (max-width:327.98px){.p .ft8{max-width:calc(100cqi - 32px)}}"))
    files["s-14-144-failure"] = fragment("s-14-144-failure", fail, fstyle)
    meta["s-14-144-failure"] = plate_meta(
        FC + "A table of the three reforms, each with its four effects in a row and a total score at the end: Reform R-06 "
        "plus 5, Reform R-30 plus 5 and Reform R-38 plus 2, under a question asking which reform does the most, and a line "
        "saying each code was scored as 1, 2 or 3 points.",
        notes="Labeled failure, a still picture: its totals are the fault and hold no atlas value; the atlas never adds "
              "effects across families.")
    entry = {
        "id": "14.144",
        "title": "Compare reforms effect by effect, with every qualifier kept and no total score.",
        "rule": [
            "Give each reform whose record names one loop a card, in the order of their IDs and side by side where the page "
            "is wide enough, each with the same rows in the same order: the targets on the loop, the targets outside it, the band, the four effects one "
            "outcome family to a row, the evidence grades and the routes. Let a reader choose one reform at a time to see "
            "its targets on the loop turn red (Rule 15.20), and keep every card on the page as the choice changes, so the comparison never rests on "
            "memory. A reform can name a loop and target nothing on it, as Reform R-38 does with Loop R8. Name each target "
            "outside the loop in words, with its layer, and draw no path the atlas does not hold.",
            "Draw each effect with Rule 13.5’s pips in the text’s ink, then print it as the atlas stores it, the code and "
            "then any qualifier, followed by the code’s meaning. A qualifier is the words after a code that say where, when "
            "or for whom the effect holds, as in “+L local” or “+M renter-owner”. A zero says “no expected effect”. Give no "
            "total, count, average or rank, since the atlas never adds effects across families (Rules 15.16 and 15.21). "
            "Print each "
            f"route’s check date or “Not checked”, with the model’s date, {SNAP}.",
        ],
        "use_when": None,
        "use_instead": [],
        "why": {"text": [
            "The four outcome families measure different things, and a reform can help one while costing another. A total turns "
            "a local, delayed or sector-only effect into points that count as if they held everywhere, and two reforms with "
            "different effects can tie. Cards with the same rows let a reader compare each family in turn, in the atlas’s "
            "own words."],
            "basis": "Our systems atlas, Reforms R-06, R-30 and R-38, Loop R8 and its note on effect codes"},
        "specimen": None,
        "tier": None,
        "tokens": ["oa.color.data.emphasis.red", "oa.color.state.selected.bar"],
        "related": ["13.3", "13.5", "13.10", "15.11", "15.16", "15.20", "15.21", "18.3", "18.8"],
        "builders": ("Read every row from the reforms’ own records, show the chosen reform’s targets from the checked "
                     "radio with CSS so the choice works with scripts off, and stop the build if any line adds, counts or "
                     "ranks the effects."),
        "specs": [
            {"label": "Choice", "value": "A named group of radio buttons, one per reform, the first chosen on load (Rule 18.3)"},
            {"label": "Targets", "value": "The chosen reform’s on the loop, in Rule 12.5’s red; each one outside it in words, with its layer and, for a connection, its two ends",
             "token": "oa.color.data.emphasis.red"},
            {"label": "Cards", "value": "One per reform, the same rows in the same order, all on the page whichever is chosen; the chosen one takes the selected bar",
             "token": "oa.color.state.selected.bar"},
            {"label": "Effects", "value": "Rule 13.5’s pips, then the atlas’s code and qualifier whole and its words; zero in words; never added"},
            {"label": "Routes", "value": "Under “Routes, with the date each was checked”: the route, who acts, its feasibility in bold, and the check date or “Not checked”, as Rule 15.20 prints them"},
            {"label": "Never", "value": "A total, a count of codes or pips, a rank, or a fill, shade, length or color by code"},
        ],
        "correct": dict({"specimen": "s-14-144-correct",
                         "caption": ("Reforms R-06, R-30 and R-38 on Loop R8, live. Choose one and its targets on the loop "
                                     "turn red; Reform R-38 has none there and says so in words. All three cards stay on the "
                                     "page whichever is chosen, with every effect, qualifier, grade and route the atlas holds, and "
                                     "no total.")},
                        **meta["s-14-144-correct"]),
        "failure": dict({"specimen": "s-14-144-failure",
                         "caption": ("<strong>Fails Rule 14.144.</strong> A total score adds each reform’s four codes as points, so a "
                                     "local or sector-only effect counts as if it held everywhere and two different "
                                     "reforms tie. The atlas never adds effects across families.")},
                        **meta["s-14-144-failure"]),
        "examples": [
            {"example": "Reforms R-06, R-30 and R-38 on Loop R8, housing", "domain": "D09", "states": [], "level": "federal",
             "where": "14.144"}],
    }
    return entry, files


def FACTS_NOTE():
    """The atlas's own sentence on its effect codes, quoted whole (ruling d)."""
    s = C15.V7["outcomes"]["effect_codes_note"]
    want = "The codes are conditional on the reform working as described, and codes for different families are never added together."
    need(want in s, "the atlas's note on effect codes changed")
    return want


# =====================================================================================================================
# Rule 14.142: S14 in full, S96 (ruling c)
# =====================================================================================================================
# S96's second note opens on the count of drops, which the failure keeps (R3): read from the data, checked against it
SEVEN = "Payrolls shrank in seven months: January, June, August, October and December 2025, and February and July 2026."
need(FACTS["example_1"]["losses"] == ["2025-01", "2025-06", "2025-08", "2025-10", "2025-12", "2026-02", "2026-07"],
     "the seven drops moved; reword S96's second note")


def split_words(past, split):
    """Where each drop past the margin fell (the data lead's R4b, ST-S2), in the editor's words, every figure computed from
    the sector file by maker_c_round5_derive.py: private and government payrolls, which add to the month's total. No cause."""
    mw = DV.month_words

    def th(v):
        return f"{abs(int(round(v * 1000))):,}"

    def moved(v):
        return "rose" if v > 0 else "fell"
    a, b = (split[m] for m in past)
    need(a["government"] < 0 < a["private"] and a["government"] < 0 and b["private"] < 0 and b["government"] < 0,
         "the directions of the split moved; the editor's sentence fits only these")
    return (f"In {mw(past[0])}, government payrolls {moved(a['government'])} {th(a['government'])} and private payrolls "
            f"{moved(a['private'])} {th(a['private'])}. In {mw(past[1])}, private payrolls {moved(b['private'])} "
            f"{th(b['private'])}, and government payrolls {moved(b['government'])} {th(b['government'])}.")


def rule_14_142():
    f1 = FACTS["example_1"]
    s14 = json.loads((SPECS / "s14.json").read_text())
    past = f1["past_margin"]
    need(past == ["2025-10", "2026-02"], "DR-239's two drops moved")
    mw = DV.month_words
    pv = {m: v for m, v in zip(past, f1["past_margin_values"])}

    def k(v):
        return f"{MINUS if v < 0 else '+'}{abs(int(round(v * 1000))):,}"
    title = (f"Payrolls shrank in seven of the {f1['n']} months charted, and only the {mw(past[0])} and {mw(past[1])} drops "
             "pass the survey’s margin of error.")
    need(f1["n_losses"] == 7, "the count of drops moved")
    margin = f1["margin_words"]
    lat = f1["latest"]
    spec = {
        "kit": 1,
        "id": "S96",
        "form": "columns-moving-average",
        "family": "change-over-time",
        "tier": "core",
        "dataset": f1["dataset"],
        "reader_question": "Which monthly drops in payroll jobs were larger than the survey’s margin of error?",
        "evidence": "finding",
        "evidence_label": "Finding",
        "grade_line": s14["grade_line"],
        "title": title,
        "reading_guide": ("Each column is one month’s change in jobs, and the two in the text’s ink are the drops past the margin. "
                          "The line is the three-month average. The shaded band is the survey’s margin of error for one "
                          "month’s change. Hatched columns are preliminary."),
        "measure_line": (f"Monthly change in payroll jobs, all nonfarm, seasonally adjusted, United States, {f1['window_words']}, "
                         "the span both jobs charts share, with the three-month average and the survey’s 90 percent "
                         f"margin of error for one month’s change, {margin} jobs."),
        "notes": [
            # what the band means (the data lead's R4; the editor's words for ST-S1 and CE-S13): its size and source, the
            # zero-centered reading, then the caution that it holds for each month alone
            (f"The band runs from {MINUS}122,000 to +122,000 jobs, the Bureau of Labor Statistics’ 90 percent margin of "
             "error for one month’s change in its survey of employers. If a month’s true change were zero, the survey’s "
             "estimate would land inside the band nine times in ten. A column that ends inside the band is a change the "
             "survey cannot tell apart from no change at that level. The band holds for each month alone, so across "
             f"{f1['n']} months a few columns could pass it by chance, and it says nothing about the three-month average."),
            (SEVEN + f" Only the {mw(past[0])} ({k(pv[past[0]])}) and {mw(past[1])} ({k(pv[past[1]])}) drops pass the margin; the other "
             "five sit inside it. " + split_words(past, f1["past_margin_split"])),
            ("August and September 2026 are preliminary: the Bureau of Labor Statistics revises each month’s first estimate "
             "in the next two monthly reports, and a yearly benchmark revision can move earlier months. The band does not show "
             "how far a revision may move a month. The average is dashed where it includes a preliminary month."),
            s14["notes"][0],
            s14["notes"][1],
            s14["notes"][4],
        ],
        "source_line": f1["source_line"],
        "credit": "Chart: Oath & Action",
        "illustrative": False,
        "alt": (f"Columns show the monthly change in payroll jobs from {f1['window_words']} over a shaded band from minus to plus "
                "122,000 jobs, the survey’s margin of error for one month’s change, inside which a month with no real change "
                "would land nine times in ten. Seven columns fall below zero, all "
                f"in 2025 and 2026. Two are drawn in the text’s ink and labeled, {mw(past[0])} at minus 140,000 and {mw(past[1])} at minus 156,000, "
                "and reach past the band; the other five end inside it. A line shows the three-month average, which stood at "
                f"51,000 in {mw(lat['month'])}, a preliminary figure."),
        # its own caption, so a reader who lists the page's tables tells S96's from S14's (the accessibility lead's 4.4)
        # plus a column in words against the margin for every month (the accessibility lead's 4.3, the engineer's request 3)
        "table": dict(s14["table"], caption=f"Monthly change in payroll jobs, {f1['window_words']}, with the three-month average",
                      columns=s14["table"]["columns"] + [
                          {"field": "change_thousands", "label": f"Against the 90 percent margin, {margin}",
                           "format": "margin", "words": {"below": "Drop past the margin", "above": "Gain past the margin",
                                                         "within": "Within the margin"}}]),
        "chart_notes": [
            ("Key: each gray column is the jobs added or lost in the month, and the two in the text’s ink are the drops past "
             "the margin; hatched columns are preliminary, August and September 2026."),
            "The band: the survey’s margin of error for one month’s change, plus or minus 122,000 jobs.",
            "Three-month average: the line, dashed where it includes a preliminary month.",
            f"Latest: +29,000 jobs in {mw(lat['month'])}, preliminary; the three-month average stood at +51,000, also preliminary.",
        ],
        "phone": "same",
        "phone_view": True,
        # the phone note as a plain line under the drawing (the design director's DD-E4, the engineer's request 5)
        "phone_line": True,
        # checked at the rule plates' columns and swept from 224 px, since S96 sits in a rule's plate (request 4)
        "plate": "rule",
        # in words that hold on both grounds: the subject ink is Charcoal on Newsprint and Newsprint on Charcoal, the text's
        # ink on each, the ink word the approved chart notes use (S17, S47; DR-262, D3-914; DF-4)
        "phone_notes": [f"The two columns in the text’s ink: {mw(past[0])}, {k(pv[past[0]])} jobs, and {mw(past[1])}, "
                        f"{k(pv[past[1]])} jobs."],
        "artboard": "reading",
        "domain": s14["domain"],
        "states": [],
        "encode": s14["encode"],
        "formats": s14["formats"],
        # the data lead's yes to DD-E3 (02:44): S96 alone drops the on-plot latest label; its chart note keeps the words
        "labels": dict({k_: v for k_, v in s14["labels"].items() if k_ != "latest"}, **{
            # under 490 px the two labels leave the plot, where October 2025's met the latest month's leader and the
            # sweep found February 2026's no clear place at 327 to 339 px; phone_notes names both in one line (S30's way)
            "named": [{"x": m, "text": [mw(m), f"{k(pv[m])} jobs"], "phone": {"hide": True}} for m in past],
            # both labels as one stack under the band, left of October 2025's column, each leader into its column's foot
            # (the design director's DD-E2, the engineer's request 5)
            "named_stack": True,
            "margin": {"value": int(f1["margin_thousands"]), "label": "Margin of error",
                       "key": "The survey’s margin of error for one month’s\u00a0change"},
        }),
        # S14's note, raised into the space between the plus 500,000 and plus 750,000 gridlines, its leader down to the
        # line: on S96's taller scale S14's offset set it on the plus 500,000 gridline (the design director's DD-E7).
        # The figure checks hold it 4 px or more clear of every gridline at every width
        "annotations": [dict(s14["annotations"][0], dy=-88)],
        # the floor drops from S14's −200 to −400 thousand so the named stack stands clear under the band at every width
        # from 490 px (the engineer measured −375 as the least that holds; −400 keeps a round floor); asked of the data lead
        # DD-E7: no tick or gridline under zero (ticks_min), the floor kept; DD-E8: under 490 px, where the named words hide,
        # the scale returns to S14's (y_narrow). Both the engineer's keys (its request 7, landed 04:10 UTC)
        "scale": {"y": [-400, s14["scale"]["y"][1]], "ticks_min": 0, "y_narrow": list(s14["scale"]["y"])},
        "notes_internal": [
            "Rule 14.142's correct plate (R5-1): S14 in full, from S14's frozen file (D3-1873); S14 stays at its entry untouched.",
            "Ruling (c): all 57 months; preliminary months hatched and the average dashed as S14 draws them; the margin a band "
            "from -122 to +122 thousand behind the columns in Stone magnitude step 1 with context edges (the engineer's band part); "
            "the two drops past it named in Charcoal at the subject weight (labels.named), never red; every other column the light "
            "fill; the average in the context ink at the context weight. The form's keys for this are the engineer's (R5-1, 'The "
            "kit for complex example 1').",
            "Check 14.142-a (maker_c_round5_derive.py): 57 months, January 2022 to September 2026; preliminary August and "
            "September 2026; seven losses; margin 122 thousand from the sidecar's september_release_margin line; past it October 2025 (-140) "
            "and February 2026 (-156); September 2026 average 50.67 thousand, 51,000 to the thousand.",
            "Title: DR-239's two approved sentences joined, as the data lead's ruling (c) suggests; the editor may tune the words, "
            "the counts stay.",
            "Scale: -400 to 850 thousand, where S14 runs -200 to 850. The floor drops so the two named labels stand as one stack "
            "under the band, clear of its lower edge, at every width from 490 px (the design director's DD-E2; the engineer "
            "measured -375 as the least that holds, and -400 keeps a round floor); the data lead's yes (its notes, Sign-offs, Batch 4). S14 keeps "
            "-200. Under 490 px, where the named labels hide, S96 takes S14's -200 to 850 (scale.y_narrow, the design director's "
            "DD-E8); no tick or gridline sits under zero at any width (scale.ticks_min 0, DD-E7), so no gridline runs under the "
            "stack's words. Check 14.142-b (maker_c_round5_derive.py --drawings): on the kit's own Node drawings at every whole "
            "width from 224 to 720 px on both grounds, at both scales, October 2025's and February 2026's columns end at least "
            "3 px past the band's lower edge (the data lead's condition), every word in the plot stands 4 px or more from every "
            "gridline, and no gridline sits under zero.",
            "Written by work/build/scripts/phase-3/phase3_ch14_complex_build.py; change a word there, never here.",
        ],
    }
    # the failure: the same columns with no band, all seven drops labeled alike as job losses (ruling c), one fault.
    # Everything else is the correct plate's (NB-S2): its measure line less the margin, its preliminary, average,
    # seasonal adjustment and window notes in its order, no on-plot latest label (DD-E3), and the sidecar's plain source
    # line, since a source line that names the margin would print what the drawing leaves out (ST-M1)
    losses = f1["losses"]
    fspec = {k_: v for k_, v in spec.items() if k_ not in ("notes_internal", "phone_view", "reading_guide", "phone_notes",
                                                            "phone_line", "plate")}
    # S96's scale with its narrow scale and no gridline under zero (the data lead's R3: S96 with the margin taken out and
    # nothing else changed)
    fspec["scale"] = dict(spec["scale"])
    # S96's notes less every word of the margin (R3): the first sentence of its second note, which counts the seven drops,
    # S14's own preliminary note (S96's adds a sentence about the band), then the notes S96 takes from S14 whole, in its order
    keep = [SEVEN, s14["notes"][2]] + [n for n in spec["notes"] if n in s14["notes"]]
    need(keep[2:] == [s14["notes"][i] for i in (0, 1, 4)] and spec["notes"][1].startswith(SEVEN + " "),
         "S96's notes from S14 changed; the failure keeps the same ones")
    fspec.update({
        "id": "s-14-142-failure",
        "table": dict(s14["table"], caption=f"The same {f1['n']} months, with the three-month average, as this failure case draws them"),
        "title": "The economy lost jobs in seven months of 2025 and 2026.",
        "measure_line": (f"Monthly change in payroll jobs, all nonfarm, seasonally adjusted, United States, {f1['window_words']}, "
                         "the span both jobs charts share, with the three-month average."),
        "notes": keep,
        "source_line": f1["source_line_plain"],
        "chart_notes": [],
        "alt": ("The same columns with no band and the seven drops drawn alike in the text’s ink, under a title that "
                "states seven months of lost jobs with no word on the margin."),
        "labels": dict({k_: v for k_, v in s14["labels"].items() if k_ != "latest"},
                       **{"named": [{"x": m, "text": []} for m in losses]}),
        # the title carries the fault; a note on one column read as pointing at one month (the design director's DD-E6)
        "annotations": [],
        "show": ["evidence", "title", "measure", "chart", "notes", "source"],
        "failure": {"rule": "14.142", "caption_lead": "Fails Rule 14.142."},
        "notes_internal": "Rule 14.142's failure plate (ruling c; the data lead's R3 of the fix pass): S96 with the margin "
                          "left out of the drawing and the words, and nothing else changed: no band, all seven drops drawn "
                          "alike, a title with no word on the margin, S96's scale and notes less the margin's words, no latest "
                          "label, the sidecar's plain source line; no red.",
    })
    fhtml = (f"<!-- s-14-142-failure: Oath & Action guide, Edition 06, chapter 14. Complex examples maker, {WRITTEN}. "
             f"Written by {ME}. -->\n"
             '<div class="p"><p class="dnp"><span aria-hidden="true">×</span>Failure case: do not publish</p>'
             '<div class="art"><div data-oa-chart="s-14-142-failure"></div></div></div>\n')
    files = {"s-14-142-failure": fhtml}
    entry = {
        "id": "14.142",
        "title": "Mark the survey’s margin on a monthly chart, and name the changes that pass it.",
        "rule": [
            "A survey estimates each month’s change from a sample, so a small change can come from the sample alone. Draw "
            "the survey’s margin of error for one month’s change as a band around zero, behind the columns, and give its "
            "size, its confidence and its source in a note (Rule 14.9). The Bureau of Labor Statistics gives a 90 percent "
            "margin, so a month with no real change lands inside the band nine times in ten. The band holds for each month "
            "alone, and over many months a few can pass it by chance, so the note says that too. Name only the changes past "
            "it that the reader’s question asks about, here the drops, each with its month and value in the text’s ink "
            "(Rule 14.6), and print the full count beside them, so a reader still learns how many months fell.",
            "Draw every month in the window the question sets, and print the window’s reason (Rule 14.10). Hatch the months "
            "still preliminary, dash the average where it includes one (Rule 14.11), and say in a note that the band does not "
            "cover the three-month average. The kit draws the phone drawing, the table and the files (Rules 14.12 to 14.14).",
        ],
        "use_when": None,
        "use_instead": [],
        "why": {"text": [
            "A survey of employers estimates each month’s change, and a small drop can come from the sample alone. The band "
            "shows a reader that five of the seven drops sit inside the survey’s margin, where the survey cannot tell them "
            "apart from no change, and that two pass it, so the chart names those two and still counts all seven."],
            "basis": "The Bureau of Labor Statistics’ Employment Situation technical note, October 2026 release; Rule 14.9"},
        "specimen": None,
        "tier": None,
        "tokens": ["oa.chart.color.subject", "oa.chart.color.magnitude.fill.step1.onNewsprint"],
        "related": ["14.6", "14.9", "14.10", "14.11", "14.12", "14.13", "14.14"],
        "builders": ("Draw the band with the kit’s band part from the margin the sidecar’s source line names, name the "
                     "months with <code>labels.named</code>, and let the kit export the SVG, PNG and CSV, checked row for row "
                     "against the data file."),
        "specs": [
            {"label": "Window", "value": f"Every month, {f1['window_words']}, with the reason in a note"},
            {"label": "Margin", "value": f"A band from {MINUS}122,000 to +122,000 behind the columns, with its edges, in the key and named on the drawing",
             "token": "oa.chart.color.magnitude.fill.step1.onNewsprint"},
            {"label": "Named drops", "value": "The two past the margin, in the text’s ink, each with its month and value",
             "token": "oa.chart.color.subject"},
            {"label": "Preliminary", "value": "Hatched columns, the average dashed where it includes one"},
            {"label": "Files", "value": "The kit’s SVG, PNG and CSV, the CSV row for row with the data file"},
        ],
        "correct": {"specimen": "s-14-s96",
                    "caption": ("The monthly change in payroll jobs, all 57 months, with the survey’s margin as a band, the "
                                "two drops past it named and the preliminary months hatched. Its phone drawing sits under it, "
                                "then its table.")},
        "failure": {"specimen": "s-14-142-failure",
                    "caption": ("<strong>Fails Rule 14.142.</strong> The chart leaves out the survey’s margin of error, so all "
                                "seven drops look alike, and the title states seven months of lost jobs with no word on the "
                                "margin. Five of the seven sit inside the margin, where the survey cannot tell them from no "
                                "change."),
                    "alt": FC + fspec["alt"], "illustrative": False, "notes": "Labeled failure: a kit figure through "
                    "s-14-142-failure.chart.json (C7), its title the fault.", "charts": ["s-14-142-failure"]},
        # no "examples" here: the chapter's build logs S96 from its spec as it places the plate (ruling (g): one example,
        # S14's data drawn in full, Work, pay and bargaining power), and a row here would count it twice
    }
    return entry, spec, fspec, files


# =====================================================================================================================
# Checks, then the files
# =====================================================================================================================
STUDIO = re.compile(r"\b(D[23]-\d+|DR-\d+|R5-\d|CE-\d|maker|studio|ruling|kit\b|spec\b)", re.I)


def reader_text(s):
    s = re.sub(r"<!--.*?-->|<style\b.*?</style>|<script\b.*?</script>", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def check(entries, files, specs, steps):
    fails = []
    ok = lambda c, m: c or fails.append(m)
    for sid, t in files.items():
        txt = reader_text(t)
        ok("—" not in t and "‑" not in t, f"{sid}: an em dash or U+2011")
        # every brace the plate's style opens it closes, never ahead, so the build's @scope holds the whole style
        css = "".join(re.findall(r"<style>(.*?)</style>", t, re.S))
        depth = [0]
        for ch in css:
            depth[0] += (ch == "{") - (ch == "}")
            if depth[0] < 0:
                break
        ok(depth[0] == 0, f"{sid}: its style's braces do not balance, so rules would leave the plate's scope")
        # names other parts of the page select (main session, 04:40 UTC): chapter 26's token table script takes .tt, the
        # shell's CSS .rt, chapter 14's block .fx and .tk; the guide check found .tt here (SG-7)
        outside = {"tt", "rt", "tk", "fx"} & {c for cl in re.findall(r'class="([^"]*)"', t) for c in cl.split()}
        ok(not outside and not re.search(r"\.(?:tt|rt|tk|fx)(?![\w-])", "".join(re.findall(r"<style>(.*?)</style>", t, re.S))),
           f"{sid}: a class another part of the page selects: {sorted(outside)}")
        ok(not re.search(r"<h[1-6]\b", t), f"{sid}: a heading inside the plate")
        bare = re.sub(r"var\((?:[^()]|\([^()]*\))*\)", "", t)
        ok(not re.search(r"(?<![\w&])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![\w-])|\brgba?\(", bare), f"{sid}: a literal color")
        ok(not STUDIO.search(txt), f"{sid}: a studio word or code in reader text: {STUDIO.search(txt)}")
        ok("<script" not in t, f"{sid}: a script in a plate (R4-5)")
        ok("'" not in txt.replace("’", ""), f"{sid}: a straight apostrophe in reader text")
        ok(" .fx" not in t and 'class="fx' not in t and " fx " not in t, f"{sid}: chapter 15's .fx would meet chapter 14's")
    for rid, en in entries.items():
        s = json.dumps(en, ensure_ascii=False)
        ok("—" not in s and "‑" not in s, f"Rule {rid}: an em dash or U+2011 in the entry")
        ok(len(en["title"].split()) <= 15, f"Rule {rid}: title of {len(en['title'].split())} words")
        ok(en["failure"]["caption"].startswith(f"<strong>Fails Rule {rid}.</strong>"), f"Rule {rid}: the failure caption")
    # DF-6: each loop's grade label sits above its chip and title (Rule 13.1), as on every chapter 15 plate
    for sid, want in (("s-14-143-correct", ["evr", "hed"] * 2), ("s-14-144-correct", ["evr", "hed"])):
        seen = re.findall(r'class="(evr|hed)"', files[sid].split("</style>", 1)[1].split('<div class="pcs8">')[0])
        ok(seen == want, f"{sid}: the grade label and the loop's title stand in the order {seen}, not label first (DF-6)")
    # 14.143: the stepper's markup as CE-1 lists it
    t = files["s-14-143-correct"].split("</style>", 1)[1]
    rt_143 = reader_text(t)
    ok(t.count("data-oa-stepper") == 1 and t.count('class="oa-stepper-step"') == 7 and t.count("data-oa-part=") == 7,
       "14.143: one stepper root with seven steps, each naming its loop")
    ok(t.count('data-oa-first') == 2 and 'role="list"' in t and 'role="status"' in t, "14.143: the list, the status line, the first steps")
    ok(re.search(r'data-oa-ready="([^"]+)"[^>]*>\1</p>', t) is not None, "14.143: the ready line differs from data-oa-ready")
    ok("data-oa-motion" not in t, "14.143: nothing moves, so no data-oa-motion")
    order = [t.find(x) for x in ('class="cfx pr"', 'class="oa-stepper-status"', 'class="oa-stepper-controls"',
                                 'class="oa-stepper-why"', 'class="oa-stepper-steps"', "The atlas’s limits on the two loops")]
    ok(all(x >= 0 for x in order) and order == sorted(order),
       "14.143: the reading order is drawings, status line, controls, reason line, list, limits (DD-C1, 2.8)")
    ok("data-red" not in t and "emphasis-red" not in t, "14.143: red on a loop drawing with no reform")
    ok(sorted(set(re.findall(r'data-s="(\d)"', t))) == [str(i) for i in range(1, 8)], "14.143: the drawing's step groups 1 to 7")
    ok(not re.search(r"Electoral pressure(?! leads to actual defeats)", reader_text(t)), "14.143: the chain label prints as a name (DR-265)")
    # CE-M1 (the data lead's R2, item 1): every printed direction against one recomputed here from the figure facts' signs
    # and grades (maker_c_round5_derive.py) and the start supposition; "can" from the plausible step to the loop's end
    ups, downs = ("rises", "rise", "goes up", "go up"), ("falls", "fall", "goes down", "go down")
    for lid in ("B4", "R10"):
        up, can = START[lid][1] in ("rise", "rises"), False
        for st_, sf in zip([x for x in steps if x["loop"] == lid], FACTS["example_2"]["loops"][lid]["steps"]):
            cause, effect = st_["line"].rstrip(".").split(", so ", 1)
            nxt = up if sf["sign"] == "+" else not up
            can_e = can or sf["grade"] == "plausible"
            for words, want_up, want_can in ((cause, up, can), (effect.removesuffix(" again"), nxt, can_e)):
                said_up = any(words.endswith(" " + v) for v in ups)
                said_dn = any(words.endswith(" " + v) for v in downs)
                ok(said_up != said_dn and said_up == want_up and ((" can " in words) == want_can),
                   f"14.143: {st_['link']} says “{words}”, not the walk's direction (up {want_up}, can {want_can}) (R2)")
            up, can = nxt, can_e
        ok((up == (START[lid][1] in ("rise", "rises"))) == (KIND[lid] == "reinforcing"), f"14.143: Loop {lid} closes against its kind")
    ok(rt_143.count("is back where it began, and") == 2 and "now rises, against the first fall. The loop pushes back, so it is balancing"
       in rt_143 and "can rise again, on top of the first rise. The loop can feed itself, so it is reinforcing" in rt_143,
       "14.143: a loop does not close on its result (R2, item 4)")
    ok(not re.search(r"\b(?:lowers|raises|can lower|can raise)\b", " ".join(x["line"] for x in steps)),
       "14.143: a line states the connection's general claim, not the walk's direction (R2, item 3)")
    # the component engineer's 02:17 findings, held: B4's label claims no least certain step where all three are well
    # supported; the list's number sits beside its loop label; the atlas's weakest-step claim is quoted where it holds
    lab_b4 = reader_text(re.search(r'<div class="evr">.*?</div>', t).group(0))
    ok("the grade of all three steps" in lab_b4 and "Connection" not in lab_b4, f"14.143: Loop B4's label: {lab_b4}")
    ok(".oa-stepper-step .lpn{grid-row:1" in files["s-14-143-correct"], "14.143: the first step's label sits in its own row")
    # RP-9: the key reads the ticks and the dashed step
    ok("Ticks near a line’s start count its delay" in rt_143 and "Dashed for a step the atlas grades plausible" in rt_143,
       "14.143: no key for the ticks or the dashed step (RP-9)")
    # the data lead's batch 6 suggestion: Loop R10's supposition opens its first step, before its direction
    r10_1 = re.search(r'data-oa-part="Loop R10" data-oa-first[^>]*>.*?<span class="oa-stepper-line">(.*?)</span>&#32;<span', t)
    ok(r10_1 is not None and r10_1.group(1).startswith('<span class="sup8">Start at seats with little electoral competition, and suppose they rise.</span>')
       and "The walk moves to Loop R10" not in rt_143, "14.143: Loop R10's supposition does not come before its first step")
    ok("weakest step for U.S. services, \u201csince its main study covers Brazilian mayors\u201d" in reader_text(t),
       "14.143: the atlas's weakest-step claim for Loop B4")
    # 14.144: the chooser's markup as CE-2 lists it, and no total
    t = files["s-14-144-correct"].split("</style>", 1)[1]
    rt = reader_text(t)
    ok(t.count('name="s-14-144-reform"') == 3 and re.findall(r'value="(R-\d+)"', t) == RIDS, "14.144: three radios in ID order")
    ok(t.count("data-oa-say") == 3 and t.count("data-oa-chooser-status") == 1, "14.144: the say lines and the status line")
    ok(re.findall(r'data-oa-panel="(R-\d+)"', t) == RIDS, "14.144: one card per reform")
    ok(not re.search(r"(?i)\b(total|sum|overall|score|rank|ranked|combined|net)\b", rt), "14.144: a word that totals or ranks")
    for q in FACTS["example_3"]["qualifiers"]:
        ok(f'<b class="cd">{e(q)}</b>' in t, f"14.144: the qualifier {q!r} is not whole in its cell")
    ok(rt.count("Not checked") == 8 and rt.count(f"Checked {SNAP}") == 1, "14.144: eight routes not checked, one dated")
    live_t = t.split('<div class="pcs8">')[0]
    ok(len(re.findall(r'data-red="working"', live_t)) == 2, "14.144: two marks under data-red on the live drawing (L39 and A5)")
    # NB-M3: in every chooser state, a target of a reform not chosen loses every part of the red target, its ink case too,
    # so no mark stays heavier than the loop for a reform that does not act on it
    for rid in RIDS:
        no = f'.p:has([value="{rid}"]:checked) [data-oa-for]:not([data-oa-for~="{rid}"])'
        for part in (" .ak-mark{stroke:", " .pl{stroke:", " .hd{fill:", " .ak-case{stroke:none}"):
            ok(no + part in files["s-14-144-correct"], f"14.144: with {rid} chosen, an unchosen target keeps its{part.split('{')[0]}")
    ok(len(re.findall(r'data-red="working"', t)) == 5, "14.144: the print copies mark L39 for R-06, L39 and A5 for R-30, none for R-38")
    ok("no expected effect" in rt, "14.144: a zero says what it means")
    # CE-S14: each card's band carries the atlas's definition after its word, as Rule 15.20's panel does
    for rid in RIDS:
        ok(f'<b>{e(REFORM[rid]["band"].capitalize())}</b>: “{ce(C15.BANDS[REFORM[rid]["band"]])}”' in t,
           f"14.144: Reform {rid}'s band prints as a bare word (CE-S14)")
    ok(re.search(r"<b class=\"cd\">[^<]+</b>,&#32;<span class=\"cw\">", t) is not None and "</b><span class=\"cw\">" not in t,
       "14.144: a code runs into its words")
    ok("grid-row:span 11;grid-template-rows:subgrid" in files["s-14-144-correct"], "14.144: the cards' rows would stack")
    ok("@container oa-frame (min-width:680px) and (min-width:40em){.cds{grid-template-columns:repeat(3," in files["s-14-144-correct"]
       and files["s-14-144-correct"].count(".cds{grid-template-columns:repeat(3,") == 1,
       "14.144: the three cards side by side must hang on the frame's width in em, so larger text takes one card a row (1.4.4)")
    ok(t.count("<dt>") == 21 and t.count("<dl>") == 3 and t.count('class="ef8g"') == 3 and t.count('<ul class="ef8"') == 3,
       "14.144: seven groups in each card's list, the effects' five rows among them, so the subgrid spans hold (eleven rows)")
    # R5 (DF-3): Rule 13.5's pips beside every code, from chapter 13's own function, in each card and in the key
    for rid in RIDS:
        for f in ("DQ", "GE", "EP", "EQ"):
            v = REFORM[rid]["effects"][f]
            ok(f'{C13.pips_svg(v.split(" ")[0])}<span>{effect_cell(v)}</span>' in t, f"14.144: {rid}'s {f} effect lacks its pips or its whole code")
    ok(t.count('<svg class="pp"') == 3 * 4 * 2 + 7, "14.144: twelve effect marks in the cards, twelve in the phone line-up and seven in the key")
    # CR-S3: the phone line-up holds every family's three codes, whole, beside their pips, in the families' and the IDs'
    # order, and shows only where the cards stack
    ph = t[t.index('<div class="ph8">'):t.index('<div class="pcs8">')]
    want = [(f, rid) for f in ("DQ", "GE", "EP", "EQ") for rid in RIDS]
    got = re.findall(r'<li><span class="chip">Reform <span class="id">(R-\d+)</span></span><span class="fv8">', ph)
    ok(got == [rid for _, rid in want] and all(f'<b class="cd">{e(REFORM[rid]["effects"][f].replace("-", MINUS, 1) if REFORM[rid]["effects"][f].startswith("-") else REFORM[rid]["effects"][f])}</b>' in ph
                                              for f, rid in want), "14.144: the phone line-up's twelve rows (CR-S3)")
    ok("@container oa-frame (min-width:680px) and (min-width:40em){.ph8{display:none}}" in files["s-14-144-correct"],
       "14.144: the phone line-up shows where the cards stand side by side")
    # CD-S10: no card's first line starts on a chip on screen; each still says its reform's name to the status line
    for rid in RIDS:
        ok(re.search(r'data-oa-say><span class="vh">Reform ' + rid + r': </span>Turns ', t) is not None,
           f"14.144: {rid}'s first line keeps a chip on screen, or the status line loses its name (CD-S10)")
    # RP-7: a connection off the loop says its own layer before its two ends
    ok("contested, in the technology layer, from" in rt and "well supported, in the economy layer, from" in rt
       and "“Cost of essentials”, in the technology layer" not in rt, "14.144: a connection's layer reads as its end's (RP-7)")
    # RP-9: each step's delay in words and a key for the ticks
    ok(rt.count("and its effect takes over 10 years") == 2 and "Ticks near a line’s start count its delay" in rt,
       "14.144: the steps' delays or the ticks' key are missing (RP-9)")
    # R5 (DF-7): 15.16's grade form and 15.20's route form; "evidence for the problem" nowhere
    ok("vidence for the problem" not in t and t.count("evidence of the problem") == 3 and t.count('class="gp"') == 6,
       "14.144: each card's two grades as Rule 15.16 prints them, “evidence of the problem” (DF-7)")
    ok(t.count("Routes, with the date each was checked") == 3 and "feasibility." not in t
       and len(re.findall(r'<span class="rf"><b>[A-Z][a-z ]+</b> feasibility</span>', t)) == 9,
       "14.144: the routes as Rule 15.20 prints them, the feasibility word in bold on its own line (DF-7)")
    pr38 = reader_text(re.search(r'data-oa-print="R-38">.*?</p>', t).group(0))
    ok("in red" not in pr38, f"14.144: R-38's print line says red: {pr38}")
    ft = reader_text(files["s-14-144-failure"])
    ok("Total score" in ft, "14.144's failure carries its fault")
    # 14.142: the spec's words against the data
    s96 = specs["s96"]
    # ST-S8 (the research lead's F6) and R4b: S96 prints the sidecar's release-named line with the two sector series and the
    # margin, S14 the release-named margin line (the main session's call), the failure the release-named plain line
    ok(s96["source_line"] == FACTS["example_1"]["source_line"],
       "S96: the source line is not the sidecar's september_release_sectors_margin line")
    ok(json.loads((SPECS / "s14.json").read_text())["source_line"] == FACTS["example_1"]["source_line_s14"],
       "S14: the source line is not the sidecar's september_release_margin line")
    allw = " ".join([s96["title"], s96["measure_line"], s96["alt"]] + s96["notes"] + s96["chart_notes"])
    for want in ("January 2022 to September 2026", "122,000", "October 2025", "February 2026", "51,000", "preliminary", "seven"):
        ok(want in allw, f"S96: {want!r} does not print")
    ok("—" not in json.dumps(specs, ensure_ascii=False), "S96: an em dash")
    # DF-4: the approved ink word, "the text's ink", in every place S96 and its failure name the dark columns
    fs = specs["failure"]
    both = json.dumps([s96, fs], ensure_ascii=False)
    ok("strongest ink" not in both, "S96: “strongest ink” where the approved chart notes say “the text’s ink” (DF-4)")
    for where, words in (("reading guide", s96["reading_guide"]), ("alt", s96["alt"]), ("key", s96["chart_notes"][0]),
                         ("phone note", s96["phone_notes"][0]), ("failure's alt", fs["alt"])):
        ok("the text’s ink" in words, f"S96: its {where} does not name the text’s ink (DF-4)")
    # NB-S2: the failure differs from S96 by the band alone: S96's notes from S14 in S96's order, its measure line less the
    # margin, no on-plot latest label, and a source line with no margin sentence (ST-M1)
    s14n = json.loads((SPECS / "s14.json").read_text())["notes"]
    ok(fs["notes"] == [SEVEN, s14n[2]] + [n for n in s96["notes"] if n in s14n],
       "S96's failure: its notes are not S96's count of drops, preliminary, average, seasonal adjustment and window notes (NB-S2, R3)")
    ok(not re.search(r"(?i)margin|band|nine times", " ".join(fs["notes"] + [fs["title"], fs["measure_line"], fs["source_line"]])),
       "S96's failure: a word of the margin in its notes, title, measure line or source line (R3)")
    ok(fs["scale"] == s96["scale"], "S96's failure: its scale is not S96's (R3)")
    # R4 and R4b, the editor's words: the band's meaning and its caution in note 1, and the split of the two drops in note 2
    ok("nine times in ten" in s96["notes"][0] and f"across {FACTS['example_1']['n']} months a few columns could pass it by chance"
       in s96["notes"][0] and "nine times in ten" in s96["alt"], "S96: the band's meaning or its caution is missing (R4)")
    ok(not re.search(r"nine samples out of ten|90 percent (?:accurate|sure)|\b5\.7\b|\b1\.05\b", json.dumps(s96, ensure_ascii=False)),
       "S96: words R4 rules out")
    ok("government payrolls fell 153,000 and private payrolls rose 13,000" in s96["notes"][1]
       and "private payrolls fell 148,000, and government payrolls fell 8,000" in s96["notes"][1], "S96: note 2's split (R4b)")
    ok(s96["measure_line"].startswith(fs["measure_line"].rsplit(", with", 1)[0]) and fs["measure_line"].endswith(", with the three-month average."),
       "S96's failure: its measure line is not S96's less the margin (NB-S2)")
    ok("latest" not in fs["labels"] and "latest" not in s96["labels"], "S96's failure: an on-plot latest label S96 does not carry")
    ok("margin" not in fs["source_line"] and fs["source_line"] == FACTS["example_1"]["source_line_plain"],
       "S96's failure: its source line names the margin the drawing leaves out (ST-M1)")
    # Rule 01.12's log (ruling (g)): 14.142 once, from S96 as the chapter's build places it; 14.143 twice, a loop each;
    # 14.144 once, Loop R8 under Housing, health care and getting ahead
    ok(not entries["14.142"].get("examples") and s96.get("domain") == "D07",
       "Log: Rule 14.142 logs once, from S96 under D07, and its entry carries no row of its own")
    ok([(x["example"].split(",")[0], x["domain"]) for x in entries["14.143"].get("examples") or []]
       == [("Loop B4", "D04"), ("Loop R10", "D02")], "Log: Rule 14.143 logs Loop B4 under D04 and Loop R10 under D02")
    ok([x["domain"] for x in entries["14.144"].get("examples") or []] == ["D09"], "Log: Rule 14.144 logs Loop R8 once, under D09")
    return fails


def outputs():
    e43, f43, steps = rule_14_143()
    e44, f44 = rule_14_144()
    e42, s96, fspec, f42 = rule_14_142()
    entries = {"14.142": e42, "14.143": e43, "14.144": e44}
    files = {**f42, **f43, **f44}
    specs = {"s96": s96, "failure": fspec}
    out = {}
    for rid, en in entries.items():
        out[ENTRIES / f"14-{rid.split('.')[1]}.json"] = json.dumps(en, indent=1, ensure_ascii=False) + "\n"
    for sid, t in files.items():
        out[SPECIMENS / f"{sid}.html"] = t
    out[SPECS / "s96.json"] = json.dumps(s96, indent=1, ensure_ascii=False) + "\n"
    out[SPECIMENS / "s-14-142-failure.chart.json"] = json.dumps(fspec, indent=1, ensure_ascii=False) + "\n"
    return out, check(entries, files, specs, steps), steps, files


def main():
    out, fails, steps, files = outputs()
    for sid, t in sorted(files.items()):
        print(f"  {sid}: {len(t.encode()):,} bytes")
    print(f"phase3_ch14_complex_build: Rule 14.143's walk: " + "; ".join(f"{s['loop']} {s['i']}/{s['n']} {s['link']} {s['hold']} ms" for s in steps))
    stale = [p for p, t in out.items() if not p.exists() or p.read_text() != t]
    if fails:
        print("\n".join("FAIL " + f for f in fails))
    if "--check" in sys.argv:
        for p in stale:
            print(f"phase3_ch14_complex_build --check: {p.relative_to(ROOT)} is not what the script writes")
        print(f"phase3_ch14_complex_build --check: {len(out) - len(stale)} of {len(out)} files current")
        return 1 if (stale or fails) else 0
    if fails:
        return 1
    for p in stale:
        p.write_text(out[p])
    print(f"phase3_ch14_complex_build: {len(out)} files, {len(stale)} written, 0 faults")
    return 0


if __name__ == "__main__":
    sys.exit(main())
