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
        _C15 = m
    return _C15


def need(cond, msg):
    if not cond:
        raise SystemExit(f"atlas_figures: {msg}")


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
            "remedy": {"grade": grade(r["remedy_evidence"]["grade"]), "text": r["remedy_evidence"]["text"]},
            "effects": [{"family": k, "name": fam[k], "code": r["effects"][k]} for k in ("DQ", "GE", "EP", "EQ")],
            "effects_confidence": r["effects_confidence"],
            "routes": [{"code": x["route"], "name": routes.get(x["route"]), "who": x["who"], "feasibility": x["feasibility"],
                        "note": x["note"], "checked": x["checked"], "checked_words": words_date(x["checked"]) if x["checked"] else None}
                       for x in r["routes"]],
            "status": {"text": r["status"]["text"], "checked": r["status"]["checked"], "checked_words": words_date(r["status"]["checked"])},
            "complements": r["complements"], "sources": r["sources"], "tradeoffs": r.get("tradeoffs")}


# ---------------------------------------------------------------------------------------------------------------------
# Figures, by chapter 15's own drawing code
# ---------------------------------------------------------------------------------------------------------------------
FIG_CSS_KEYS = ("sv", "id", "sn", "dm", "rt", "rp", "sh", "pp")


def fig_css():
    """Chapter 15's rules for its drawings (its CSS table, by key), with nothing of its plate layout."""
    C = c15()
    return "".join(C.CSS[k] for k in FIG_CSS_KEYS if k in C.CSS)


def loop_figure(lid, targets=()):
    """A numbered loop drawn by chapter 15's kit, its weakest step named and its ID and kind inside. targets are the chosen
    reform's: chapter 15 draws a red target on a solid connection and on a pill; a patterned connection it cannot draw red
    (conn(): "a patterned one needs its lead-in at 6 px"), so such a target is returned in `not_red`, for the page to name in
    words and for the atlas test to read."""
    C = c15()
    lp = C.LOOP[lid]
    codes = [c for c, _ in lp["chain"]]
    lids = lp["links"]
    weak_g = C.least_certain(lids)
    weak = [i for i, x in enumerate(lids) if C.link(x)["evidence"] == weak_g]
    weakest = weak[0] if len({C.link(x)["evidence"] for x in lids}) > 1 and len(weak) == 1 else None
    kind = "reinforcing" if lp["type"] == "R" else "balancing"
    drawable = {t for t in targets if t in C.NODE or (t in C.LINK and C.tex(C.link(t)["evidence"]) == "solid")}
    not_red = [t for t in targets if t not in drawable]
    if len(codes) == 2:
        body, h, _ = C.two_loop(codes, lids, weakest=weakest, inside=(lid, kind), top=4, targets=drawable)
    elif len(codes) == 3:
        body, h = C.three_loop(codes, lids, weakest=weakest, inside=(lid, kind), targets=drawable)
    else:
        need(False, f"Loop {lid} has {len(codes)} variables; the figure step draws two and three today")
    svg = C.svg_wrap(body, h)
    return {"svg": svg, "w": C.W, "h": h, "variables": codes, "connections": lids, "weakest": lids[weakest] if weakest is not None else None,
            "red": sorted(drawable & set(codes + lids)), "not_red": not_red, "kind": kind,
            "read_aloud": C.read_aloud(codes, lids), "minus": C.minus_count(lids)}


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
    return {"svg": C.svg_wrap(body, h, w=C.card_width(a_code, b_code, lid)), "h": h, "variables": [a_code, b_code],
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
    return {"loop": {"id": lid, "kind": fig["kind"], "type": lp["type"], "title": lp["title"], "summary": lp["summary"],
                     "case": lp["case"], "qualification": lp["qualification"], "adaptation": lp["adaptation"],
                     "closure": lp["closure"], "evidence": lp["evidence"], "evidence_summary": lp["evidence_summary"],
                     "delay": delay(lp["delay"]) if lp.get("delay") in ("S", "M", "L") else lp.get("delay"),
                     "records": lp["records"], "reforms_listed": lp["reforms"]},
            "variables": [var_rec(c) for c, _ in lp["chain"]], "steps": steps, "minus": fig["minus"],
            "weakest": fig["weakest"], "read_aloud": fig["read_aloud"],
            "offered": [reform_rec(k) for k in offered], "chosen": chosen, "tags": others,
            "figure": {k: fig[k] for k in ("svg", "w", "h", "red", "not_red")}}


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


VIEWS = {"loop": view_loop, "reform": view_reform}


def build(spec):
    V = model()
    rec = spec.get("record")
    out = {"model": {"sha256": sha(), "title": V["meta"]["title"], "subtitle": V["meta"]["subtitle"],
                     "snapshot": V["meta"]["snapshot"], "snapshot_words": words_date(V["meta"]["snapshot"])},
           "parts": parts(), "kind_words": list(KIND.values())}
    fn = VIEWS.get(spec["view"])
    out["view"] = fn(spec) if fn else {}
    # the locator (Rule 12.7): the parts the page's record sits in
    v = out["view"]
    codes = [x["id"] for x in v.get("variables", [])] or [t["id"] for t in v.get("targets", []) if "part" in t]
    out["locator"] = sorted({part(c) for c in codes}, key=PART_ORDER.index)
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
