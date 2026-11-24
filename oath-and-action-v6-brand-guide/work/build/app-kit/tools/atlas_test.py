"""The atlas test (chat 11c; chapter 21's plan, section 8; Rule 21.16).

Reads every atlas page the application kit drew, its standalone working export and each of its plate's frames, together
with the atlas model, and checks that each page says what the model holds and works as the guide's rules require. It
prints one line a check and view, PASS or FAIL; a failure names the page, the frame, the record, the value printed and
the model's value.

Usage:
    python3 -I work/build/app-kit/tools/atlas_test.py OUT_DIR [--plates DIR] [--ids A11 A14 ...] [--json REPORT]
    python3 -I work/build/app-kit/tools/atlas_test.py --self-test OUT_DIR [--plates DIR]

OUT_DIR is the kit's output folder (oa-app.mjs --out): OUT_DIR/<id>/export.html, the working page; OUT_DIR/<id>/facts.json,
what the kit measured in each captured view (every word's size and colors). --plates is the folder of the kit's plates
(work/build/app-kit/plates by default), whose frames are tested as drawn. Exit 1 on any FAIL.

The self-test copies the clean pages, plants one fault for each check in a copy (never in the model), and passes only when
every plant is caught by its own check and the clean pages stay quiet, as the guide check's self-test does (D4-90).

The marks each page carries are contract C9's (the engineer's notes) with the data lead's rulings R1 to R13
(work/handoffs/phase-4/20261122_Chat-11c-Dataviz-Lead-Notes.md): R2's count methods, R4's read-aloud directions, R5's
evidence paths, R8's weakest step and R10's one red. The test reimplements each method from the model itself and never
imports the renderer's figure step, so a fault in the step shows here.
"""
import copy
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[4]
MODEL_PATH = ROOT / "work/extract/atlas-v7-data.json"
PLATES = ROOT / "work/build/app-kit/plates"
V = json.loads(MODEL_PATH.read_text())
N, L, LO, RF, IS = V["nodes"], V["links"], V["loops"], V["reforms"], V["issues"]
CHECKS = [f"T{i}" for i in range(1, 17)]
NAMES = {"T1": "Typed IDs", "T2": "Connection marks", "T3": "Counts", "T4": "Loops", "T5": "Authority", "T6": "Red",
         "T7": "Effects", "T8": "Routes and dates", "T9": "Evidence a step away", "T10": "Grades in words", "T11": "Stepper",
         "T12": "Pressed and lit", "T13": "Colors", "T14": "Type", "T15": "Site frame", "T16": "Words the atlas retired"}

# ---------------------------------------------------------------------------------------------------------------------
# The model, by the plan's written methods (Appendix A; the data lead's R2, R4, R5, R8), read here on their own
# ---------------------------------------------------------------------------------------------------------------------
COLL = {"Variable": set(N), "Connection": set(L), "Loop": set(LO), "Reform": set(RF), "Issue": set(IS), "Claim": set(V["claims"]),
        "Domain": {d["id"] for d in V["domains"]}, "Route": {r["code"] for r in V["routes"]["items"]},
        "Rule change": {r["id"] for r in V["repairLog"]["rows"]}, "Delivery case": {r["id"] for r in V["deliveryLog"]["rows"]}}
ALL_IDS = set().union(*[v for k, v in COLL.items() if k != "Route"])     # route codes are words (SS, LOC): never read as bare
GRADE_WORD = {"documented": "Documented", "well-supported": "Well supported", "well_supported": "Well supported",
              "plausible": "Plausible", "plausible_contested": "Contested", "contested": "Contested", "hypothesis": "Hypothesis"}
GRADE_LINE = {"documented": "solid", "well-supported": "solid", "plausible": "dashed", "plausible_contested": "dashdot", "hypothesis": "dotted"}
ORDER = ["documented", "well-supported", "plausible", "plausible_contested", "hypothesis"]
STORED_SPELLINGS = ["well-supported", "well_supported", "plausible_contested"]
FAMILIES = ["DQ", "GE", "EP", "EQ"]
MINUS = "−"


def _system1():
    """System 1's build_system.py, for its sentences(): the one splitter the kit and this test share (the data lead's R15)."""
    import importlib.util
    sp = importlib.util.spec_from_file_location("oa_atlas_build_t", ROOT / "work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py")
    m = importlib.util.module_from_spec(sp)
    sys.dont_write_bytecode = True
    sp.loader.exec_module(m)
    return m


_S1 = []


def SENTENCES(t):
    if not _S1:
        _S1.append(_system1())
    return _S1[0].sentences(t)


def part(v):
    x = N[v]
    return {"economy": "EC", "technology": "TC"}.get(x["layer"], x["cluster"])


def sheet(v):
    x = N[v]
    return {"economy": "EC", "technology": "TC"}.get(x["layer"]) or x["domain"].split("/")[0]


def numbered(k):
    return not LO[k]["closure"].startswith("conceptual")


def domain(sid):
    return next((d for d in V["domains"] if d["id"] == sid), None)


def count_of(key, page):
    """R2's method for one data-count-of key, or None for a key R2 does not list (a FAIL under T3)."""
    p = key.split(":")
    try:
        if p[0] == "atlas":
            k = p[1]
            if k == "grade":
                return sum(1 for x in L.values() if x["evidence"] == p[2])
            return {"variables": len(N), "connections": len(L), "loops": len(LO), "loops-numbered": sum(1 for k_ in LO if numbered(k_)),
                    "loops-conceptual": sum(1 for x in LO.values() if x["closure"].startswith("conceptual")),
                    "loops-reinforcing": sum(1 for x in LO.values() if x["type"] == "R"), "loops-balancing": sum(1 for x in LO.values() if x["type"] == "B"),
                    "reforms": len(RF), "reforms-active": sum(1 for r in RF.values() if not r.get("rejected")), "issues": len(IS),
                    "issues-retired": sum(1 for x in IS.values() if x.get("retired")), "hubs": len(V["hubs"]), "pathways": len(V["pathways"])}[k]
        if p[0] == "hub":
            return sum(1 for x in V["pathways"] if x["hub"] == p[1])
        if p[0] == "part-variables":
            return sum(1 for v in N if part(v) == p[1])
        if p[0] == "part-inside":
            return sum(1 for x in L.values() if part(x["from"]) == p[1] and part(x["to"]) == p[1])
        if p[0] == "flow":
            a, b = p[1].split(">")
            return sum(1 for x in L.values() if part(x["from"]) == a and part(x["to"]) == b) if a != b else None
        if p[0] == "sheet":
            s, what = p[1], p[2]
            vs = [v for v in N if sheet(v) == s]
            ls = [k for k, x in L.items() if sheet(x["to"]) == s]
            if what == "variables":
                return len(vs)
            if what == "connections":
                return len(ls)
            if what == "loops":
                return sum(1 for k in LO if numbered(k) and any(c[0] in vs for c in LO[k]["chain"]))
            if what == "reforms":
                return sum(1 for r in RF.values() if (set(vs) | set(ls)) & set(r["targets"]) and not r.get("rejected"))
            if what == "issues":
                d = domain(s)
                return len(d["issues"]) if d else 0
            if what == "grade":
                return sum(1 for k in ls if L[k]["evidence"] == p[3])
        if p[0] == "records-shown":
            d = domain(p[1])
            on = page.filter_on()
            return sum(1 for i in d["issues"] if not on or set(IS[i]["nodes"] or []) & on)
        if p[0] == "records-naming":       # the engineer's key, for each filter chip's count (sent to the data lead for R2)
            d = domain(p[1])
            return sum(1 for i in d["issues"] if p[2] in (IS[i]["nodes"] or []))
        if p[0] == "records-grade":
            d = domain(p[1])
            return sum(1 for i in d["issues"] if IS[i]["grade"] == p[2])
        if p[0] == "loop":
            lp = LO[p[1]]
            return {"steps": len(lp["links"]), "minus": sum(1 for x in lp["links"] if L[x]["polarity"] == "-"), "records": len(lp["records"])}[p[2]]
        if p[0] == "question":
            pw = next(x for x in V["pathways"] if x["id"] == p[1])
            return len({part(v) for v in pw["model_refs"]["nodes"]})
    except (KeyError, IndexError, StopIteration, TypeError):
        return None
    return None


def weakest(lid):
    """R8: the connection the loop's evidence summary names as weakest, checked against its least certain grade."""
    lp = LO[lid]
    txt = lp["evidence_summary"] or ""
    for k in lp["links"]:
        txt = txt.replace(f"{k}: {L[k]['name']}", k)
    sent = next((x for x in re.split(r"(?<=[.;])\s+", txt) if re.search(r"\bweake(st|r)\b", x)), None)
    if not sent:
        return None
    m = re.search(r"\bweake(?:st|r)\b(?:\s+step)?\s+is\s+([A-Z]{1,3}\d+[a-z]?)\b", sent)
    k = m.group(1) if m else ([x for x in re.findall(r"\b[A-Z]{1,3}\d+[a-z]?\b", sent[:re.search(r"\bweake(st|r)\b", sent).start()]) if x in L] or [None])[-1]
    return k if k in lp["links"] else None


def directions(lid):
    lp = LO[lid]
    codes = [c for c, _ in lp["chain"]]
    up, out = True, [f"{codes[0]}:rises"]
    for i, k in enumerate(lp["links"]):
        if L[k]["polarity"] == "-":
            up = not up
        out += [k, f"{codes[(i + 1) % len(codes)]}:{'rises' if up else 'falls'}"]
    return " ".join(out)


def words_date(iso):
    y, m, d = iso.split("-")
    return f"{['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][int(m) - 1]} {int(d)}, {y}"


# ---------------------------------------------------------------------------------------------------------------------
# A page: a working export or a plate's frame
# ---------------------------------------------------------------------------------------------------------------------
def text(el):
    return re.sub(r"\s+", " ", el.get_text(" ") if isinstance(el, Tag) else str(el)).strip()


class Page:
    def __init__(self, app, key, html, kind, facts=None, title=None, full=True):
        self.app, self.key, self.kind, self.facts, self.full = app, key, kind, facts, full
        self.soup = BeautifulSoup(html, "lxml")
        self.root = self.soup.select_one("[data-atlas-view]")
        self.view = self.root.get("data-atlas-view") if self.root else None
        self.record = self.root.get("data-atlas-record") if self.root else None
        t = self.soup.find("title")
        self.title = text(t) if t else title
        self.html = html
        self.theme = "light"
        self.contrast = None

    @property
    def where(self):
        return f"{self.app} {self.key}"

    def all(self, sel):
        return self.root.select(sel) if self.root else []

    def filter_on(self):
        return {b.get("data-atlas-filter") for b in self.all('[data-atlas-filter][aria-pressed="true"]')}

    def chosen(self):
        if self.view == "reform":
            return self.record
        c = self.all("input.oa-choice-input[checked]")
        return c[0].get("value") if c else self.root.get("data-atlas-chosen")


def in_any(el, names):
    """True when el sits inside an element of one of the given tag names or classes (".class")."""
    for p in el.parents:
        if not isinstance(p, Tag):
            continue
        for n in names:
            if (n.startswith(".") and n[1:] in (p.get("class") or [])) or (n.startswith("[") and p.has_attr(n[1:-1])) or p.name == n:
                return True
    return False


# ---------------------------------------------------------------------------------------------------------------------
# The checks. Each returns a list of faults (strings), and a count of what it read; a check that finds nothing of its
# kind on a full page of a view that must hold it fails ("found nothing to check").
# ---------------------------------------------------------------------------------------------------------------------
EXPECT = {"T2": {"loop", "reform", "register"}, "T3": {"home", "register", "loop"}, "T4": {"loop"}, "T6": {"reform", "loop", "how-to-read"},
          "T7": {"reform", "loop"}, "T8": {"reform", "loop"}, "T9": {"home", "reform", "register", "loop"}, "T11": {"loop"}, "T12": {"home"}}
ID_RE = re.compile(r"(?<![\w/#-])([A-Z]{1,3}-?\d+[a-z]?)(?![\w-])")


def t1(pg):
    faults, n = [], 0
    for el in pg.all("[data-atlas-kind]"):
        n += 1
        k, i = el.get("data-atlas-kind"), el.get("data-atlas-id")
        if k not in COLL:
            faults.append(f"{k} {i}: the kind word {k!r} is not one of Rule 13.9's ten")
        elif i not in COLL[k]:
            faults.append(f"{k} {i}: printed as a {k.lower()}, and the model files no {k.lower()} {i} (it files {i} as {', '.join(x for x, s in COLL.items() if i in s) or 'nothing'})")
        if "oa-chip" in (el.get("class") or []) and text(el) != f"{k} {i}":
            faults.append(f"{k} {i}: the chip reads {text(el)!r}")
        if el.has_attr("data-part"):
            faults.append(f"part {el.get('data-part')}: a part's box carries a kind ({k}); a part is no typed record (R1)")
    # a row's head (its chip and title) shown at every width: a table drawn as cards opens each card with it (specs 10;
    # the data lead's request 15). Read from the kit's measure of each row head in the captured view
    for rh in (pg.facts or {}).get("rowheads", []):
        n += 1
        if not rh.get("shown"):
            faults.append(f"the row head {rh.get('text', '')[:40]!r} is hidden at {pg.facts.get('width')} px; each card opens with its row's head (specs 10)")
    for s in pg.root.find_all(string=True) if pg.root else []:
        if isinstance(s, NavigableString) and not in_any(s, [".oa-chip", "svg", "script", "style", "title"]):
            for m in ID_RE.finditer(str(s)):
                if m.group(1) in ALL_IDS:
                    faults.append(f"{m.group(1)}: a bare code in the page's words, {str(s).strip()[:60]!r} (house rule H11)")
    for t in pg.all("svg text"):
        tx = text(t)
        for m in ID_RE.finditer(tx):
            if m.group(1) in ALL_IDS and not re.search(r"(Variable|Connection|Loop|Reform|Issue|Claim|Domain)\s+" + re.escape(m.group(1)), tx):
                faults.append(f"{m.group(1)}: a code in a drawing with no kind word before it")
    # CE1 (the data lead's R22, item 6): the first chip of each record in main, in document order, is followed by the
    # record's stored name, or sits in a row or heading whose text prints it, or takes it as its link's description
    if pg.full:
        for k, i, why in unnamed_first(pg):
            n += 1
            faults.append(f"{k} {i}: first named on the page with no name after its chip ({why}); Rule 21.6 and R22 ask its stored name")
    return faults, n


def name_of(kind, i):
    """R22's table: the stored name that follows a chip of each kind (Claim: none)."""
    if kind == "Variable":
        return (N.get(i) or {}).get("title")
    if kind == "Connection":
        return (L.get(i) or {}).get("name")
    if kind == "Loop":
        return (LO.get(i) or {}).get("title")
    if kind == "Reform":
        return (RF.get(i) or {}).get("title")
    if kind == "Issue":
        return (IS.get(i) or {}).get("title")
    if kind == "Domain":
        return next((d["title"] for d in V["domains"] if d["id"] == i), None)
    if kind == "Route":
        return next((r["name"] for r in V["routes"]["items"] if r["code"] == i), None)
    if kind == "Rule change":
        return next((r["rule"] for r in V["repairLog"]["rows"] if r["id"] == i), None)
    if kind == "Delivery case":
        return next((r["what_was_done"] for r in V["deliveryLog"]["rows"] if r["id"] == i), None)
    return None


def norm(s):
    """Whitespace collapsed; quotation marks and apostrophes read as one straight form, for comparing names (R22)."""
    s = re.sub(r"[‘’′]", "'", re.sub(r"[“”]", '"', str(s)))
    return re.sub(r"\s+", " ", s).strip()


def unkind(s):
    """Stored text compared with its page's words: a chip's kind word before an ID dropped on both sides (R11 sets each
    bare ID in its typed chip, taking a kind word the stored text gives)."""
    return re.sub(r"\b(variable|connection|loop|reform|issue|claim|domain)\s+(?=[A-Z]{1,3}-?\d)", "", norm(s), flags=re.I)


def unnamed_first(pg):
    """The first chip of each record in main that R22's item 6 finds unnamed: (kind, id, what follows it)."""
    main = pg.root.select_one("main") if pg.root else None
    if main is None:
        return []
    h1 = norm(text(pg.root.select_one("main h1") or ""))
    seen, out = set(), []
    for el in main.select(".oa-chip[data-atlas-kind]"):
        k, i = el.get("data-atlas-kind"), el.get("data-atlas-id")
        if (k, i) in seen or k == "Claim":
            continue
        seen.add((k, i))
        nm = name_of(k, i)
        if not nm:
            continue
        nm_ = norm(nm).strip('"')
        # the page's own record, its name the page's h1
        if i == pg.record and nm_ in h1:
            continue
        # its link's accessible description
        d = el.get("aria-describedby")
        if d and any(nm_ == norm(text(t)).strip('"') for t in pg.soup.select(f"#{d}")):
            continue
        # a frame is a picture and drops the page's hidden list of names; its working page carries them, read above
        if d and pg.kind == "frame" and not pg.soup.select(f"#{d}"):
            continue
        # a row or heading whose own text prints the name
        hold = el.find_parent(["tr", "li", "h1", "h2", "h3", "h4", "label", "summary"])
        if hold is not None and nm_ in norm(text(hold)):
            continue
        # the name right after the chip, in the same run, past nothing but a space or a comma
        after, node = "", el
        while node is not None:
            for sib in node.next_siblings:
                after += text(sib) if isinstance(sib, Tag) else str(sib)
                if len(after) > len(nm) + 8:
                    break
            # CD-R3: a chip held to its marks sits in a ws-nb span, and the run reads on past the span
            par = node.parent
            if len(after) <= len(nm) + 8 and par is not None and par.name == "span" and "ws-nb" in (par.get("class") or []):
                node = par
                continue
            break
        a = norm(after)
        if re.match(r'^[\s,]*"?' + re.escape(nm_), a):
            continue
        out.append((k, i, repr(a[:30])))
    return out


def line_of(g):
    """The texture of a drawn connection's mark (System 1's pattern(): dashed 4w 2w, dash-dot 4w 1.5w w 1.5w, dotted 0 2.5w)."""
    dash = [p.get("stroke-dasharray") for p in g.select("path.ak-mark") if p.get("stroke-dasharray")]
    if not dash:
        return "solid"
    nums = [float(x) for x in re.split(r"[\s,]+", dash[0].strip()) if x]
    if nums and nums[0] == 0:
        return "dotted"
    return "dashdot" if len(nums) >= 4 else "dashed"


def square_first(el, word):
    """True when the record square (svg.rs) stands right before the word in el."""
    for sq in el.select("svg.rs"):
        nxt = sq.next_sibling
        while isinstance(nxt, NavigableString) and not str(nxt).strip():
            nxt = nxt.next_sibling
        if nxt is not None and text(nxt).lower().startswith(word.lower()):
            return True
    return False


def t2(pg):
    faults, n = [], 0
    for el in pg.all('[data-atlas-kind="Connection"][data-sign]'):
        n += 1
        i = el.get("data-atlas-id")
        x = L.get(i)
        if not x:
            continue
        for a, want in (("data-sign", x["polarity"] or "none"), ("data-type", x["type"]), ("data-delay", x["delay"]), ("data-grade", x["evidence"])):
            if el.get(a) != want:
                faults.append(f"Connection {i}: {a} printed {el.get(a)!r}, model {want!r}")
        if el.name == "g":
            got, want = line_of(el), GRADE_LINE[x["evidence"]]
            if got != want:
                faults.append(f"Connection {i}: drawn {got}, its grade {GRADE_WORD[x['evidence']]} takes a {want} line (Rule 13.4)")
        elif not el.find_parent("svg"):
            tx = text(el)
            gw = GRADE_WORD[x["evidence"]]
            for g, w in GRADE_WORD.items():
                if re.search(r"\b" + w + r"\b", tx) and w != gw:
                    faults.append(f"Connection {i}: printed {w}, model {gw}")
                    break
            if not re.search(r"\b" + gw + r"\b", tx, re.I):
                faults.append(f"Connection {i}: its grade {gw} does not print in words (Rule 13.3)")
            elif x["evidence"] == "documented" and re.search(r"\b" + gw + r"\b", tx) and not square_first(el, gw):
                # the label's display word (a row, a key); a sentence that says "documented" in its own words takes none
                faults.append(f"Connection {i}: no record square right before the word {gw} (Rule 13.4, R3)")
            sw = atlas_words().get("signs", {})
            own = sw.get(x["polarity"] or "none")
            other = sw.get({"+": "-", "-": "+"}.get(x["polarity"] or "none", ""), None)
            if own and x["polarity"] and not re.search(r"\b" + re.escape(own) + r"\b", tx) and other and re.search(r"\b" + re.escape(other) + r"\b", tx):
                faults.append(f"Connection {i}: printed {other!r}, its sign {x['polarity']} reads {own!r}")
    # a connection chip followed by a grade word (a loop's grade line): the word is the connection's
    for ch in pg.all('.oa-chip[data-atlas-kind="Connection"]'):
        nxt = ch.next_sibling
        tx = str(nxt).strip() if isinstance(nxt, NavigableString) else ""
        word = next((w for w in sorted(set(GRADE_WORD.values()), key=len, reverse=True) if tx.startswith(w)), None)
        i = ch.get("data-atlas-id")
        if word and i in L:
            n += 1
            if word != GRADE_WORD[L[i]["evidence"]]:
                faults.append(f"Connection {i}: printed {word} after its chip, model {GRADE_WORD[L[i]['evidence']]}")
    return faults, n


NUM_WORDS = {"no": 0, "none": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def t3(pg):
    faults, n = [], 0
    for el in pg.all("[data-count]"):
        n += 1
        key, got = el.get("data-count-of"), el.get("data-count")
        want = count_of(key or "", pg)
        if want is None:
            faults.append(f"count {got} under {key!r}: no method in the data lead's R2 counts it")
            continue
        if str(want) != got:
            faults.append(f"count {key}: printed {got}, model {want}")
        tx = text(el).replace(",", "")
        nums = [int(x) for x in re.findall(r"\b\d+\b", tx)] + [v for w_, v in NUM_WORDS.items() if re.search(r"\b" + w_ + r"\b", tx.lower())]
        if int(got) not in nums:
            faults.append(f"count {key}: the words {tx[:50]!r} do not print {got}")
    return faults, n


def t4(pg):
    faults, n = [], 0
    for el in pg.all("[data-atlas-reads]"):
        n += 1
        toks = el.get("data-atlas-reads").split()
        lids = [t for t in toks if ":" not in t]
        lid = next((k for k, lp in LO.items() if lp["links"] == lids), None)
        if not lid:
            faults.append(f"the read-aloud line reads {' '.join(lids)}, which is no loop's chain")
            continue
        if el.get("data-atlas-reads") != directions(lid):
            faults.append(f"Loop {lid}: the read-aloud line reads {el.get('data-atlas-reads')!r}, the signs give {directions(lid)!r} (R4)")
        tx = text(el)
        if tx.count("falls") + tx.count("fall") < 1 and any(t.endswith(":falls") for t in toks):
            faults.append(f"Loop {lid}: the line's words never say a variable falls")
    lids_on = {el.get("data-atlas-id") for el in pg.all('svg [data-atlas-kind="Connection"]')}
    for lid, lp in LO.items():
        if not numbered(lid) or not set(lp["links"]) <= lids_on or not lids_on <= set(lp["links"]):
            continue
        n += 1
        wk = weakest(lid)
        marked = {el.get("data-atlas-id") for el in pg.all('[data-weakest="true"]')}
        if wk and marked != {wk}:
            faults.append(f"Loop {lid}: the weakest step marked {sorted(marked) or 'none'}, its evidence summary names {wk} (R8)")
        m_ = sum(1 for x in lp["links"] if L[x]["polarity"] == "-")
        kind = "reinforcing" if lp["type"] == "R" else "balancing"
        if (m_ % 2 == 0) != (lp["type"] == "R"):
            faults.append(f"Loop {lid}: {m_} minus signs and the kind {kind} disagree in the model itself")
        if pg.full and kind not in text(pg.root):
            faults.append(f"Loop {lid}: the page never names its kind, {kind}")
    return faults, n


def t5(pg):
    faults, n = [], 0
    for el in pg.all('[data-type="authority"]'):
        n += 1
        if el.get("data-sign") not in (None, "none"):
            faults.append(f"Connection {el.get('data-atlas-id')}: authority printed with a sign, {el.get('data-sign')} (Rule 15.5)")
        if el.find_parent("svg") and any(el.get("data-atlas-id") in lp["links"] for lp in LO.values()):
            faults.append(f"Connection {el.get('data-atlas-id')}: authority drawn in a loop")
    for k, x in L.items():
        if x["type"] == "authority" and (x["polarity"] or x["loops"]):
            faults.append(f"Connection {k}: the model gives an authority connection a sign or a loop")
    return faults, n


def t6(pg):
    faults, n = [], 0
    # How to read's key sample of the red target names no reform (specs 11.2): it is read for its target style
    if pg.view == "how-to-read":
        smp = pg.all(".wa-marks svg.tgt")
        css = "".join("".join(str(x) for x in st.contents) for st in pg.soup.find_all("style"))
        n += len(smp)
        if not smp and pg.full:
            faults.append("How to read draws no red target sample (svg class tgt) (Rule 12.5's key)")
        elif not re.search(r"\.tgt\s+\.ak-mark\{[^}]*stroke:var\(--oa-color-data-emphasis-red", css):
            faults.append("How to read's red target sample takes no red: no rule strokes .tgt .ak-mark in the red token (request 23)")
        for el in pg.all('[data-red="working"]'):
            if not in_any(el, [".wa-marks"]):
                faults.append(f"{el.get('data-atlas-kind')} {el.get('data-atlas-id')}: red on a how-to-read page outside its key (R10)")
        return faults, n
    # E11c-2: a loop page carries one drawing, note and tag set a reform it offers; every state is read, as a reader
    # choosing each reform sees it (the data lead's request 17)
    states = sorted({a.get("data-atlas-for") for a in pg.all("[data-atlas-for]")}) if pg.view == "loop" else []
    for chosen in states or [pg.chosen()]:
        mine = lambda el: all(a.get("data-atlas-for") == chosen for a in el.find_parents(attrs={"data-atlas-for": True})) \
            and (el.get("data-atlas-for") in (None, chosen))
        reds = [el for el in pg.all('[data-red="working"]') if mine(el)]
        tg = set(RF[chosen]["targets"]) if chosen in RF else set()
        jobs = {el.get("data-red-job") for el in reds}
        if len(jobs) > 1:
            faults.append(f"Reform {chosen} chosen: {len(jobs)} working reds of different jobs in one view: {sorted(j or '' for j in jobs)} (Rule 05.3)")
        for el in reds:
            n += 1
            i = el.get("data-atlas-id")
            if pg.view not in ("reform", "loop"):
                faults.append(f"{el.get('data-atlas-kind')} {i}: red on a {pg.view} page, which takes none (R10)")
            elif i not in tg:
                faults.append(f"{el.get('data-atlas-kind')} {i}: red with Reform {chosen} chosen, and Reform {chosen} does not target it (Rule 12.5)")
            if "oa-chip" in (el.get("class") or []) or in_any(el, [".wa-tag", ".oa-chip", "button", "h1", "h2"]):
                faults.append(f"{i}: red on a chip, tag, button or heading (R10)")
        drawn = {el.get("data-atlas-id") for el in pg.all("svg [data-atlas-id]") if mine(el)}
        for t in sorted(tg & drawn):
            n += 1
            if not any(el.get("data-atlas-id") == t for el in reds):
                faults.append(f"{t}: Reform {chosen}'s target, drawn and not red with Reform {chosen} chosen (Rule 12.5, R10)")
        if states:
            # the tags under the drawing name the other reforms, never the chosen one (Rule 21.5); the note names the
            # chosen reform and each target the drawing turns red (Rule 12.5; the data lead's request 18)
            box = next((a for a in pg.all(f'.wa-tagsets [data-atlas-for="{chosen}"]')), None)
            # a crop to the drawing alone ("art", specs 15.2) carries no note; its page's frames and export read it
            if box is None and not pg.full and not pg.all(".wa-tagsets"):
                continue
            if box is None:
                faults.append(f"Reform {chosen} chosen: no note or tags for it beside the drawing (Rule 12.5)")
                continue
            for ch in box.select('.wa-tag .oa-chip[data-atlas-kind="Reform"]'):
                n += 1
                if ch.get("data-atlas-id") == chosen:
                    faults.append(f"Reform {chosen} chosen: its own chip among the other reforms' tags (Rule 21.5)")
            named = {c.get("data-atlas-id") for c in box.select(".wa-acts .oa-chip")}
            if chosen not in named:
                faults.append(f"Reform {chosen} chosen: the note beside the drawing does not name it (Rule 12.5)")
            for t in sorted(tg & drawn):
                n += 1
                if t not in named:
                    faults.append(f"Reform {chosen} chosen: the note does not name {t}, a target the drawing turns red (Rule 12.5)")
    return faults, n


def code_words(c):
    return c.replace("-", MINUS)


def t7(pg):
    faults, n = [], 0
    by = {}
    for el in pg.all("[data-effect-family]"):
        by.setdefault(el.get("data-atlas-reform"), []).append(el)
    for rid, rows in by.items():
        n += len(rows)
        if rid not in RF:
            faults.append(f"effect rows for {rid!r}, no reform in the model")
            continue
        fams = [r.get("data-effect-family") for r in rows]
        if fams != FAMILIES:
            faults.append(f"Reform {rid}: effect rows {fams}, Rule 15.16 asks four in the order {FAMILIES}")
        for r in rows:
            f = r.get("data-effect-family")
            want = RF[rid]["effects"].get(f)
            if r.get("data-effect-code") != want:
                faults.append(f"Reform {rid} {f}: code {r.get('data-effect-code')!r}, model {want!r}")
            if want and code_words(want) not in text(r):
                faults.append(f"Reform {rid} {f}: the row does not print {code_words(want)!r} whole, with a true minus")
    # ST-1 (the data lead's R21): the atlas's confidence in a reform's effects, quoted as stored, once a reform; on a loop
    # page each panel's line after its fourth row and Rule 15.20's disclosure under it, closed on load, holding the remedy's
    # evidence whole with its grade word and the stored tradeoffs whole
    for rid in by:
        if rid not in RF:
            continue
        r = RF[rid]
        lines = pg.all(f'[data-effects-confidence="{rid}"]')
        if len(lines) != 1 or unkind(r["effects_confidence"]) not in unkind(text(lines[0])):
            faults.append(f"Reform {rid}: {len(lines)} confidence line(s); R12 and R21 ask one, quoting {r['effects_confidence']!r}")
        if pg.view != "loop":
            continue
        panel = pg.root.select_one(f'[data-oa-panel="{rid}"]')
        if panel is None:
            continue
        last = panel.select("[data-effect-family]")[-1:]
        if lines and last and lines[0] not in [x for x in last[0].find_all_next() if isinstance(x, Tag)]:
            faults.append(f"Reform {rid}: the confidence line does not follow the fourth effect row (R21)")
        q = panel.select("details.wa-qual")
        if len(q) != 1:
            faults.append(f"Reform {rid}: {len(q)} disclosure(s) under the panel; Rule 15.20 asks one")
            continue
        if pg.kind == "frame":
            continue                         # a frame draws a closed disclosure's summary alone (D4-152); its body is read on the working page
        qt = unkind(text(q[0]))
        g = GRADE_WORD.get(r["remedy_evidence"]["grade"], "").lower()
        if q[0].has_attr("open") and pg.kind == "export":
            faults.append(f"Reform {rid}: its disclosure opens on load (Rule 15.20)")
        for what, want in (("the remedy's evidence", r["remedy_evidence"]["text"]), ("its tradeoffs", r.get("tradeoffs") or ""), ("the remedy's grade", g)):
            if unkind(want) not in qt:
                faults.append(f"Reform {rid}: the disclosure does not hold {what} whole ({norm(want)[:40]!r}; R21)")
    for el in pg.all("[data-effect-family]"):
        if re.search(r"\b(total|average|score|sum)\b", text(el.parent), re.I):
            faults.append(f"Reform {el.get('data-atlas-reform')}: the effects carry a total, average or score (Rule 15.16)")
            break
    return faults, n


def t8(pg):
    faults, n = [], 0
    for el in pg.all("[data-route]"):
        n += 1
        rid, code = el.get("data-atlas-reform"), el.get("data-route")
        rr = next((x for x in RF.get(rid, {}).get("routes", []) if x["route"] == code), None)
        if not rr:
            faults.append(f"Reform {rid}: route {code}, not in the reform's record")
            continue
        want = rr["checked"] or "none"
        if el.get("data-checked") != want:
            faults.append(f"Reform {rid} route {code}: dated {el.get('data-checked')!r}, model {want!r} (never the status date)")
        tx = text(el)
        if want == "none" and "Not checked" not in tx:
            faults.append(f"Reform {rid} route {code}: no check date and no words Not checked")
        if want != "none" and words_date(want) not in tx:
            faults.append(f"Reform {rid} route {code}: its date {words_date(want)} does not print")
    for el in pg.all("[data-status-date]"):
        n += 1
        rid = el.get("data-atlas-reform")
        want = (RF[rid]["status"]["checked"] or "none") if rid in RF else V["meta"]["snapshot"]
        if el.get("data-status-date") != want:
            faults.append(f"{'Reform ' + rid if rid else 'the snapshot'}: dated {el.get('data-status-date')!r}, model {want!r}")
        if want == "none":
            if "Not checked" not in text(el):
                faults.append(f"Reform {rid}: its status has no check date and the panel does not say Not checked (Rule 13.10)")
        elif words_date(want) not in text(el):
            faults.append(f"{'Reform ' + rid if rid else 'the snapshot'}: the date {words_date(want)} does not print in words")
    # a frame carries only what its width shows (D4-152), so the title bar's date is read on the working page
    if not pg.all(".wa-bar [data-status-date]") and pg.kind == "export":
        faults.append("the title bar prints no snapshot date (Rule 13.10)")
    return faults, n


PATH_RE = re.compile(r"^/atlas/(register/(?P<sheet>[a-z0-9]+)|loops/(?P<loop>[a-z0-9]+)|reforms/(?P<reform>r-\d+)|routes/(?P<route>[a-z]+))(?:#(?P<anchor>[a-z0-9-]+))?$")


def target_ok(pg, href):
    if href.startswith("#"):
        return pg.soup.find(id=href[1:]) is not None or pg.kind == "frame"
    m = PATH_RE.match(href)
    if not m:
        return False
    if m.group("loop"):
        return next((k for k in LO if k.lower() == m.group("loop")), None) is not None
    if m.group("reform"):
        return m.group("reform").upper() in RF
    if m.group("route"):
        return m.group("route").upper() in COLL["Route"]
    s = m.group("sheet").upper()
    a = m.group("anchor") or ""
    if a.startswith("register-"):
        k = next((x for x in L if x.lower() == a[9:]), None)
        return bool(k) and sheet(L[k]["to"]) == s
    if a.startswith("variable-"):
        k = next((x for x in N if x.lower() == a[9:]), None)
        return bool(k) and sheet(k) == s
    if a.startswith("issue-"):
        k = next((x for x in IS if x.lower() == a[6:]), None)
        return bool(k) and IS[k]["domain"] == s
    return s in {d["id"] for d in V["domains"]} | {"EC", "TC"}


def t9(pg):
    faults, n = [], 0
    for el in pg.all("[data-evidence-href]"):
        n += 1
        h = el.get("data-evidence-href")
        if not target_ok(pg, h):
            faults.append(f"{el.get('data-atlas-kind', '')} {el.get('data-atlas-id', '')}: its evidence link {h!r} reaches no record (R5)")
        if el.name == "a" and el.get("href") != h:
            faults.append(f"{el.get('data-atlas-id')}: links to {el.get('href')!r}, its evidence is {h!r}")
    for ch in pg.all('.oa-chip[data-atlas-kind="Connection"]'):
        if not ch.has_attr("data-evidence-href") and not in_any(ch, ["[data-evidence-href]"]):
            n += 1
            faults.append(f"Connection {ch.get('data-atlas-id')}: a chip with no link to its line in the Register (Rule 21.7)")
    if pg.full:
        drawn = {el.get("data-atlas-id") for el in pg.all('svg [data-atlas-kind="Connection"]')}
        named = {el.get("data-atlas-id") for el in pg.all('.oa-chip[data-atlas-kind="Connection"]') if not el.find_parent("svg")}
        for i in sorted(drawn):
            n += 1
            if i not in named:
                faults.append(f"Connection {i}: drawn, and no chip on the page names it or links to its line (Rule 21.7)")
    return faults, n


def t10(pg):
    faults, n = [], 0
    for s in pg.root.find_all(string=True) if pg.root else []:
        if in_any(s, ["script", "style", "[data-atlas-field]"]):
            continue
        for w in STORED_SPELLINGS:
            if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", str(s)):
                faults.append(f"the stored spelling {w!r} prints in place of its display word (Rule 13.3)")
    for el in pg.all("[data-grade]"):
        n += 1
    # the data lead's R18: each loop's grade line composed from its stored field, every grade token in its display word
    # (capitalized at the start and after a semicolon, lowercase elsewhere), every bare variable code its chip
    for el in pg.all("[data-grade-text]"):
        n += 1
        want = r18(el.get("data-grade-text"))
        if re.sub(r"\s+([;,.:])", r"\1", text(el)) != want:
            faults.append(f"the grade line {text(el)[:60]!r}, R18 composes {want[:60]!r} from the stored {el.get('data-grade-text')[:40]!r}")
    # the data lead's R15: a contested remedy's two blocks rejoin to the stored text whole and in order, split at the
    # sentence remedy_split names by the one splitter the kit uses, side by side at 1440 px, both open, the same type;
    # each block's words and lines are reported, and length never fails
    pair = pg.all("[data-reading]")
    if pair:
        n += 1
        rid = pair[0].get("data-atlas-reform")
        rec = RF.get(rid, {}).get("remedy_evidence", {})
        norm = lambda t: re.sub(r"\s+", " ", t.replace("’", "'")).strip()

        def words_of(b):
            c = copy.copy(b)
            for x in c.select(".wa-srcl"):
                x.decompose()
            return text(c)
        blocks = [words_of(b) for b in pair]
        contested = rec.get("grade") in ("plausible_contested", "contested")
        if len(pair) == 1 and (not contested or rid in WHOLE):
            # PR-M2 and R29: a remedy the atlas does not grade contested, or a contested one on the data lead's list, prints
            # whole, its text the stored text whole
            if norm(words_of(pair[0])) != norm(rec.get("text", "")):
                faults.append(f"Reform {rid}: the remedy printed whole does not equal the stored text (R29)")
            return faults, n
        if len(pair) == 1:
            faults.append(f"Reform {rid}: a contested remedy printed whole, and R29 lists only {sorted(WHOLE)} to print whole; the data lead reads it first")
            return faults, n
        if len(pair) != 2:
            faults.append(f"Reform {rid}: the remedy prints in {len(pair)} blocks, two asked (R15)")
        elif norm(" ".join(blocks)) != norm(rec.get("text", "")):
            faults.append(f"Reform {rid}: the two blocks do not rejoin to the stored remedy text whole and in order (R15)")
        else:
            k = int(pair[0].get("data-split") or 0)
            sents = SENTENCES(rec["text"])
            if not 1 < k <= len(sents) or norm(" ".join(sents[:k - 1])) != norm(blocks[0]):
                faults.append(f"Reform {rid}: the split falls elsewhere than sentence {k} of {len(sents)} by the shared splitter (R15)")
            if any(in_any(b, ["details", "[hidden]"]) for b in pair) or len({tuple(b.get("class") or []) for b in pair}) != 1:
                faults.append(f"Reform {rid}: the two blocks do not stand alike, open and in one type (R15)")
            # RP1 (R23): Rule 01.16's matching labels, one over each block, outside it, in order and in one type
            labs = [b.find_previous_sibling(attrs={"data-reading-label": True}) for b in pair]
            if any(x is None for x in labs) or [x.get("data-reading-label") for x in labs] != ["1", "2"] \
                    or len({tuple(x.get("class") or []) for x in labs}) != 1 or any(not text(x) or "⟦" in text(x) for x in labs):
                faults.append(f"Reform {rid}: the two readings do not carry matching labels over them, in order (Rule 01.16, R23)")
            rd = (pg.facts or {}).get("readings") or []
            if pg.key.endswith("1440-light") and len(rd) == 2 and rd[0]["top"] != rd[1]["top"]:
                faults.append(f"Reform {rid}: at 1440 px the two blocks do not sit side by side, tops at {rd[0]['top']} and {rd[1]['top']} (R15)")
            pg.report = (f"remedy contested, two blocks, {len(blocks[0].split())} and {len(blocks[1].split())} words"
                         + (f", {rd[0]['lines']} and {rd[1]['lines']} lines" if len(rd) == 2 else ""))
    return faults, n


# R29: the contested remedies the data lead rules print whole (no sentence boundary separates two readings)
WHOLE = {"R-01", "R-22"}


def r18(stored):
    def word(m):
        w = GRADE_WORD[m.group(1)]
        return w if m.start() == 0 or re.search(r";\s*$", stored[:m.start()]) else w.lower()
    out = re.sub(r"(?<![\w-])(documented|well-supported|plausible_contested|plausible|hypothesis)(?![\w-])", word, stored)
    out = re.sub(r"\b([A-Z]{1,2}\d+[a-z]?)\b", lambda m: f"Variable {m.group(1)}" if m.group(1) in N else m.group(1), out)
    return re.sub(r"\s+", " ", out).strip()


STEP_ORDER = [("oa-stepper-play", "Play"), ("oa-stepper-reset", "Reset the loop"), ("oa-stepper-prev", "Previous step"), ("oa-stepper-next", "Next step")]


def script_said(box, steps, s, i):
    """The status line chapter 18's stepper script writes for step i (c-18-loop-stepper.js, show() and count()), read the
    way the script reads it (AX-1): the nearest data-oa-part at or above the step, when it sits inside the stepper's root or
    is the root itself, names a loop in a two-loop walk and the line counts within it; else "Step i of n: "."""
    def part_of(el):
        for e in [el] + [p for p in el.parents if isinstance(p, Tag)]:
            if e.has_attr("data-oa-part"):
                return e.get("data-oa-part") if (e is box or any(p is box for p in e.parents)) else None
        return None
    name = part_of(s)
    if name is None:
        pre = f"Step {i} of {len(steps)}: "
    else:
        own = [x for x in steps if part_of(x) == name]
        pre = f"{name}, step {own.index(s) + 1} of {len(own)}: "
    return re.sub(r"\s+", " ", pre + text(s.select_one(".oa-stepper-line") or "") + " " + text(s.select_one(".oa-stepper-more") or "")).strip()


def t11(pg):
    faults, n = [], 0
    for box in pg.all("[data-oa-stepper]"):
        n += 1
        btns = box.select(".oa-stepper-controls button")
        got = [(next((c for c in (b.get("class") or []) if c.startswith("oa-stepper-") and c != "oa-stepper-button"), ""), text(b)) for b in btns]
        if [g[0] for g in got] != [c for c, _ in STEP_ORDER] or [g[1] for g in got] != [w for _, w in STEP_ORDER]:
            faults.append(f"the stepper's buttons read {[g[1] for g in got]}, AL-22 asks {[w for _, w in STEP_ORDER]}")
        steps = box.select(".oa-stepper-step")
        for i, s in enumerate(steps, 1):
            # AX-1: the hold counts the words the script writes in the status line, not the kit's own words
            said = script_said(box, steps, s, i)
            if not said.startswith(f"Step {i} of {len(steps)}: "):
                faults.append(f"step {i}: the script would say {said[:40]!r}…, the plate prints 'Step {i} of {len(steps)}:' (Rule 21.13; AX-1)")
            want = max(6000, 250 * len(said.split()))
            if s.get("data-oa-hold") != str(want):
                faults.append(f"step {i}: holds {s.get('data-oa-hold')} ms, the {len(said.split())} words the status line says take {want} (AL-24)")
            if not s.select(".oa-stepper-more"):
                faults.append(f"step {i}: no more words for the status line to read (chapter 18's stepper reads line and more)")
        # a drawn state (A19): the status line the frame prints is the one the script writes at that step
        at = int(box.get("data-oa-at") or 0)
        st = box.select_one(".oa-stepper-status")
        if at and st is not None and text(st) != script_said(box, steps, steps[at - 1], at):
            faults.append(f"step {at}: the drawn status line reads {text(st)[:50]!r}…, the script writes {script_said(box, steps, steps[at - 1], at)[:50]!r}…")
    return faults, n


def t12(pg):
    faults, n = [], 0
    qs = pg.all("[data-pathway]")
    pressed = [q for q in qs if q.get("aria-pressed") == "true"]
    for q in qs:
        n += 1
        if q.get("aria-pressed") not in ("true", "false"):
            faults.append(f"question {q.get('data-pathway')}: no aria-pressed")
    if len(pressed) > 1:
        faults.append(f"{len(pressed)} questions pressed at once")
    # CD-R1 (R19, item 2): with no question pressed, as the working page loads and as a load-state frame draws it, no part
    # is lit and the status line is empty; and a home page's first screen draws that state, since its window never holds
    # the questions, so a lit drawing there would answer a question the reader cannot see pressed
    if pg.view == "home" and qs and not pressed:
        lit0 = sorted({b.get("data-part") for b in pg.all('[data-part][data-lit="true"]')})
        if lit0:
            faults.append(f"no question pressed, and {', '.join(lit0)} lit (R19, CD-R1)")
        st0 = pg.all(".wa-status")
        if st0 and text(st0[0]):
            faults.append(f"no question pressed, and the status line reads {text(st0[0])[:40]!r} (R19, CD-R1)")
    if pg.view == "home" and pg.kind == "frame" and pg.key.endswith("-screen") and pressed:
        faults.append(f"a first screen drawn with {pressed[0].get('data-pathway')} pressed, its question out of the window (CD-R1)")
    for q in pressed:
        if not q.select("svg use[href*='selected-check'], svg.oa-toggle-check"):
            faults.append(f"question {q.get('data-pathway')}: pressed with no check (AL-21)")
        pw = next((x for x in V["pathways"] if x["id"] == q.get("data-pathway")), None)
        want = {part(v) for v in pw["model_refs"]["nodes"]} if pw else set()
        lit = {b.get("data-part") for b in pg.all('[data-part][data-lit="true"]')}
        if pg.full and lit != want:
            faults.append(f"question {q.get('data-pathway')}: lit parts {sorted(lit)}, its variables sit in {sorted(want)}")
    # R19 (CD-M2, AX-4): each question names its own answer region, which holds its own stored answer under a heading that
    # names it; the working page loads with none pressed and no answer shown; a frame shows the pressed question's alone
    if pg.view == "home" and qs:
        if pg.kind == "export" and pressed:
            faults.append(f"the working page loads with {pressed[0].get('data-pathway')} pressed; R19 asks none")
        regions = pg.all("[data-pathway-answer]")
        shown = [r for r in regions if not r.has_attr("hidden")]
        want_shown = [q.get("data-pathway") for q in pressed]
        if pg.full and [r.get("data-pathway-answer") for r in shown] != want_shown:
            faults.append(f"answers shown {[r.get('data-pathway-answer') for r in shown]}, the pressed question asks {want_shown} (R19)")
        for q in qs:
            pid_ = q.get("data-pathway")
            pw = next((x for x in V["pathways"] if x["id"] == pid_), None)
            if not pw:
                faults.append(f"question {pid_}: no pathway in the model")
                continue
            parts_ = set((q.get("data-parts") or "").split())
            if parts_ != {part(v) for v in pw["model_refs"]["nodes"]}:
                faults.append(f"question {pid_}: lights {sorted(parts_)}, its variables sit in {sorted({part(v) for v in pw['model_refs']['nodes']})} (R6)")
            if pg.kind == "frame":
                continue                     # a frame draws the pressed question's answer alone
            tgt = pg.soup.find(id=q.get("aria-controls")) if q.get("aria-controls") else None
            if tgt is None or tgt.get("data-pathway-answer") != pid_:
                faults.append(f"question {pid_}: names no answer region of its own (aria-controls {q.get('aria-controls')!r}; R19)")
                continue
            body = copy.copy(tgt.select_one('[data-atlas-field="short_answer"]'))
            got = ""
            if body is not None:
                body = BeautifulSoup(str(body), "lxml")
                for c in body.select(".oa-chip"):
                    c.decompose()
                got = norm(text(body)).replace(" .", ".").replace(" ?", "?")
            if got != norm(pw["short_answer"]):
                faults.append(f"question {pid_}: its answer region reads {got[:50]!r}…, the stored answer {norm(pw['short_answer'])[:50]!r}… (R19)")
            h = tgt.select_one("h3")
            if h is None or norm(pw["question"]) not in norm(text(h)):
                faults.append(f"question {pid_}: its answer's heading does not name the question (AX-4)")
    return faults, n


def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def rgb(s):
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", s or "")
    return tuple(int(x) for x in m.groups()) if m else None


LITERAL = re.compile(r"(?<![\w-])(#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\()")


def t13(pg):
    faults, n = [], 0
    for st in pg.soup.find_all("style"):
        css = "".join(str(x) for x in st.contents)
        if "@font-face" in css or "--oa-color-palette-newsprint:" in css:
            continue    # the fonts and tokens.css, the one source of colors
        for m in LITERAL.finditer(css):
            faults.append(f"a literal color {css[m.start():m.start() + 12]!r} in the page's style; every color from a token (AL-23)")
            break
    if pg.theme == "dark":
        for st in pg.soup.find_all("style"):
            css = "".join(str(x) for x in st.contents)
            if "@font-face" in css or "--oa-color-palette-newsprint:" in css:
                continue
            if re.search(r"(muted-mark|selected-bar)[^;{}]*:[^;{}]*(palette-stone|palette-white)", css):
                faults.append("a dark muted mark or selected bar in Stone or White (AL-23)")
    for w in (pg.facts or {}).get("words", []):
        n += 1
        fg, bg = rgb(w.get("color")), rgb(w.get("bg"))
        if not fg or not bg:
            continue
        r = (max(lum(fg), lum(bg)) + 0.05) / (min(lum(fg), lum(bg)) + 0.05)
        big = w["size"] >= 24 or (w["size"] >= 18.66 and int(w.get("weight", 400)) >= 700)
        if r < (3 if big else 4.5) - 0.005:
            faults.append(f"{w['text'][:30]!r}: {r:.2f} to 1 on its ground, under {3 if big else 4.5}")
    # the marks, on the frame's pixels (Rule 21.15): text 4.5 to 1; muted marks and secondary words 3; the red target 3 on
    # Charcoal, where it takes no edge (on Newsprint it carries DR-305's Charcoal case, read by T6 and R14)
    for row, least in (("text", 4.5), ("secondary", 3), ("red", 3 if pg.theme == "dark" else None)):
        c = (pg.contrast or {}).get(row)
        if not c or c.get("ratio") is None or least is None:
            continue
        n += 1
        if c["ratio"] < least - 0.005:
            faults.append(f"{row} ({c.get('token')}): {c['ratio']} to 1 measured on the frame's pixels, under {least} (Rule 21.15)")
    return faults, n


SIGN_VERBS = {"raises", "lowers", "decides"}     # chapter 15's typed step: "1 money," then "lowers" (approved, ED-F9)


def t14(pg):
    faults, n = [], 0
    for w in (pg.facts or {}).get("words", []):
        n += 1
        if w["size"] < 13 - 0.01:
            faults.append(f"{w['text'][:30]!r}: {w['size']} px, under 13 (ED-F9)")
    for t in pg.all("svg text"):
        spans = t.find_all("tspan", recursive=False)
        # chapter 15's typed step ("1 money," then "lowers"), and its card's typed label with no number ("money," then
        # "raises"), approved under ED-F9
        typed_step = (re.match(r"^\d", text(spans[0])) or text(spans[0]).endswith(",")) if spans else False
        last = text(spans[-1]) if spans else ""
        if len(spans) > 1 and len(last.split()) == 1 and len(text(t).split()) > 1 and not (typed_step and last in SIGN_VERBS):
            n += 1
            faults.append(f"the label {text(t)!r} ends its last line on one word (ED-F9)")
    return faults, n


SITE = {}
AW = {}


def atlas_words():
    """Chapter 21's atlas words (signs, delays, grades, the title bar's name), from the generator, as the kit reads them."""
    if not AW:
        import subprocess
        r = subprocess.run(["python3", "-I", str(ROOT / "work/build/scripts/phase-4/phase4_ch21_build.py"), "--page-words", "all"],
                           capture_output=True, text=True, cwd=str(ROOT))
        AW.update(json.loads(r.stdout)["A11"]["atlas"] if r.returncode == 0 else {})
    return AW


def site_words():
    if not SITE:
        import subprocess
        r = subprocess.run(["python3", "-I", str(ROOT / "work/build/scripts/phase-4/phase4_ch20_build.py"), "--page-words", "A06"],
                           capture_output=True, text=True, cwd=str(ROOT))
        SITE.update(json.loads(r.stdout)["site"] if r.returncode == 0 else {})
    return SITE


def t15(pg):
    faults, n = [], 1
    # CD-R5 (PR-S8): a frame's page names the theme its view draws, so the guide's own theme never reaches into it
    if pg.kind == "frame" and pg.root is not None and pg.root.get("data-oa-theme") != pg.theme:
        faults.append(f"the frame's page names the theme {pg.root.get('data-oa-theme')!r} and its view draws {pg.theme!r}, so the guide's theme reaches it (PR-S8, CD-R5)")
    head = pg.root.select_one("header.oa-masthead") if pg.root else None
    if not head and pg.kind == "frame" and not pg.full:
        return faults, 1                   # a crop to a part carries its part alone (DD11C-Q6); the shell is read elsewhere
    if not head:
        return ["no site masthead"], n
    part_ = next((a for a in head.select(".oa-masthead-part, .oa-masthead-row-link") if text(a) == V["meta"]["title"]), None)
    want = "page" if pg.view == "home" else "true"
    # a phone frame shows the masthead's parts only in its closed menu, which the frame does not carry (D4-152)
    shown = pg.kind == "export" or head.select(".oa-masthead-part, .oa-masthead-row-link")
    if shown and (not part_ or part_.get("aria-current") != want):
        faults.append(f"the masthead's atlas part takes aria-current={part_.get('aria-current') if part_ else None!r}, DR-316 asks {want!r}")
    if len(pg.all("header.oa-masthead")) != 1:
        faults.append("more than one masthead (AL-17)")
    nav = pg.root.select("nav.wa-bar[aria-label]")
    if not nav:
        faults.append("no title bar navigation named for the atlas's views")
    elif atlas_words().get("views_label") and nav[0].get("aria-label") != atlas_words()["views_label"]:
        faults.append(f"the title bar is named {nav[0].get('aria-label')!r}, the atlas words {atlas_words()['views_label']!r} (R17)")
    bc = pg.all('nav.wa-crumbs[aria-label]')
    if pg.view != "home" and not bc:
        faults.append("no breadcrumb below the home (AL-09)")
    if pg.view == "home" and bc:
        faults.append("a breadcrumb on the home page")
    foot = pg.root.select_one("footer.ws-foot")
    sw = site_words()
    if not foot and pg.full:
        faults.append("no site footer")
    elif foot and sw:
        heads = [text(h) for h in foot.select("h2")]
        if heads != [g[0] for g in sw["footer"]["groups"]]:
            faults.append(f"the footer's lists read {heads}, the website's {[g[0] for g in sw['footer']['groups']]} (3.2.6)")
    # CR-21: on a working page every <use> draws a symbol the page holds
    if pg.kind == "export":
        ids = {e.get("id") for e in pg.soup.select("[id]")}
        for u in pg.soup.select("use"):
            h = u.get("href") or u.get("xlink:href") or ""
            if h.startswith("#") and h[1:] not in ids:
                faults.append(f"a <use> draws {h}, a symbol the page does not hold (CR-21)")
                break
    if pg.full and len(pg.all("main h1")) != 1:
        faults.append(f"{len(pg.all('main h1'))} h1 in main, one asked (AL-10)")
    if pg.title is not None:
        p = pg.title.split(" | ")
        # a sheet's page names its sheet before "The Register" (specs 15.6), so the view may take two parts
        if len(p) not in (3, 4) or p[-2] != V["meta"]["title"] or p[-1] != "Oath & Action" or (len(p) == 4 and pg.view != "register"):
            faults.append(f"the page title {pg.title!r} is not '[view] | {V['meta']['title']} | Oath & Action' (AL-01)")
        # PR-S9: a record's page names its own record first, its chip's words and its stored title
        kind = {"loop": "Loop", "reform": "Reform"}.get(pg.view)
        if kind and pg.record:
            rec = (LO if kind == "Loop" else RF).get(pg.record, {})
            want = norm(f"{kind} {pg.record}, {rec.get('title', '')}")
            if norm(p[0]).replace('"', '') != want.replace('"', ''):
                faults.append(f"the page title opens {p[0]!r}; the page's own record reads {want!r} (AL-01, 2.4.2; PR-S9)")
    return faults, n


RETIRED = ["Times Explainer", "Economist Register", "Yes on 3", "Veterans for All Voters", "Ranked Choice Melrose", "Oath & Action's editor works with",
           "Oath & Action’s editor works with"]


def t16(pg):
    faults, n = [], 1
    tx = text(pg.root) if pg.root else ""
    if "⟦" in tx or "⟦" in str(pg.soup):
        faults.append(f"a word the generator does not print yet: {sorted(set(re.findall(r'⟦([^⟧]+)⟧', str(pg.soup))))[:6]} (contract C9)")
    for w in RETIRED:
        if w in tx or (pg.title and w in pg.title):
            faults.append(f"{w!r} prints: a newspaper's name (ED-F8) or the editor's disclosure (DR-100)")
    for t in [pg.title or ""] + [text(h) for h in pg.all("h1")]:
        for m in ID_RE.finditer(t):
            if m.group(1) in set(LO) | set(RF) and not re.search(r"(Loop|Reform)\s+" + re.escape(m.group(1)), t):
                faults.append(f"{m.group(1)}: a bare loop or reform code in a title, {t!r}")
    return faults, n


FNS = {f"T{i}": f for i, f in enumerate([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16], 1)}


def line_name(c):
    """A check's name inside its line, in lower case after the code, an initialism keeping its capitals (CE16: "typed IDs")."""
    return " ".join(w if re.match(r"^[A-Z]{2,}", w) else w.lower() for w in NAMES[c].split(" "))


def run_page(pg, only=None):
    """One line a check for the page: (check, ok, line)."""
    out = []
    for c in only or CHECKS:
        faults, n = FNS[c](pg)
        # PR-M2: a reform page with no drawing (its targets are a shape chapter 15's kit does not draw) holds no
        # connection mark and no red, and says so in words (where_none)
        no_art = pg.view == "reform" and c in ("T2", "T6") and not pg.all("figure.wa-fig")
        if not faults and not n and pg.full and pg.view in EXPECT.get(c, set()) and not no_art:
            faults = [f"found nothing to check on a {pg.view} page, which must hold it"]
        if faults:
            out += [(c, False, f"FAIL {c} {pg.where}: {f}") for f in faults]
        else:
            extra = getattr(pg, "report", None) if c == "T10" else None
            out.append((c, True, f"PASS {c} {pg.where}: {line_name(c)}, {n} read" + (f"; {extra}" if extra else "")))
    return out


# ---------------------------------------------------------------------------------------------------------------------
# Loading the kit's output
# ---------------------------------------------------------------------------------------------------------------------
def pages(out_dir, plates_dir=PLATES, ids=None):
    out_dir = Path(out_dir)
    res = []
    for d in sorted(p for p in out_dir.iterdir() if p.is_dir()):
        app = d.name.upper()
        if ids and app not in ids:
            continue
        facts = json.loads((d / "facts.json").read_text()) if (d / "facts.json").exists() else {}
        if facts.get("type") != "atlas-page":
            continue
        fv = {f"{v.get('width')}-{v.get('theme')}": v for v in facts.get("views", []) if v.get("width")}
        for f in sorted(d.glob("export-*-*.html")):
            k = f.stem[len("export-"):]
            pg = Page(app, f"export {k}", f.read_text(), "export", fv.get(k))
            pg.theme = k.split("-")[1]
            res.append(pg)
        pj = Path(plates_dir) / f"{d.name}.json"
        if pj.exists():
            pdata = json.loads(pj.read_text())
            for v in pdata["views"]:
                inner = re.search(r'<div xmlns="http://www.w3.org/1999/xhtml" class="oa-app-art"[^>]*>(.*)</div></foreignObject>', v["html"], re.S)
                parts = v["key"].split("-")
                pg = Page(app, f"frame {v['key']}", frame_html(inner.group(1) if inner else v["html"], pdata, plates_dir), "frame", fv.get(f"{parts[0]}-{parts[1]}"),
                          title=pdata.get("title"), full=len(parts) == 2)
                pg.theme = v["theme"]
                pg.contrast = v.get("contrast")
                res.append(pg)
    return res


USE_RE = re.compile(r'<use href="#(oa-app-wa-[0-9a-f]+)"[^>]*/>')


def unuse(html, symbols):
    """A frame's drawings read whole: each <use> of an atlas symbol (weight step c) replaced by the symbol's content."""
    def one(m):
        sym = (symbols or {}).get(m.group(1), "")
        inner = re.match(r"<symbol\b[^>]*>(.*)</symbol>$", sym, re.S)
        return inner.group(1) if inner else m.group(0)
    return USE_RE.sub(one, html)


def frame_html(inner, pdata, plates_dir):
    """A frame's page as the guide shows it: its markup, with the kit's styles its plate stands on (contract C4)."""
    inner = unuse(inner, pdata.get("symbols"))
    css = "".join((Path(plates_dir) / f"{t}.css").read_text() for t in [pdata.get("type")] + (pdata.get("styles") or [])
                  if (Path(plates_dir) / f"{t}.css").exists())
    return f"<html><head><style>{css}</style></head><body>{inner}</body></html>"


def plate_pages(plates_dir=PLATES, ids=None):
    """The plates' frames alone, for a run with no kit output folder (the strict guide build's)."""
    res = []
    for pj in sorted(Path(plates_dir).glob("a*.json")):
        pdata = json.loads(pj.read_text())
        if pdata.get("type") != "atlas-page" or (ids and pdata["id"] not in ids):
            continue
        for v in pdata["views"]:
            inner = re.search(r'<div xmlns="http://www.w3.org/1999/xhtml" class="oa-app-art"[^>]*>(.*)</div></foreignObject>', v["html"], re.S)
            parts = v["key"].split("-")
            pg = Page(pdata["id"], f"frame {v['key']}", frame_html(inner.group(1) if inner else v["html"], pdata, plates_dir), "frame", None, title=pdata.get("title"), full=len(parts) == 2)
            pg.theme = v["theme"]
            pg.contrast = v.get("contrast")
            res.append(pg)
    return res


def run(out_dir, plates_dir=PLATES, ids=None, quiet=False):
    lines = []
    for pg in pages(out_dir, plates_dir, ids):
        if not pg.root:
            lines.append(("T15", False, f"FAIL T15 {pg.where}: no atlas page root (data-atlas-view)"))
            continue
        lines += run_page(pg)
    if not quiet:
        for _, _, ln in lines:
            print(ln)
    return lines


# ---------------------------------------------------------------------------------------------------------------------
# The self-test: one planted fault a check, each in a copy of a clean page
# ---------------------------------------------------------------------------------------------------------------------
def _sub(pg, sel, fn):
    """A copy of the page with fn applied to the first element matching sel; None when nothing matches."""
    q = copy.copy(pg)
    q.soup = BeautifulSoup(str(pg.soup), "lxml")
    q.root = q.soup.select_one("[data-atlas-view]")
    # a selector led by "@" reads the whole document (the head's style), any other the page's own root
    el = (q.soup.select_one(sel[1:]) if sel.startswith("@") else q.root.select_one(sel)) if q.root else None
    if el is None:
        return None
    fn(el, q)
    return q


def _set(**kv):
    def f(el, q):
        for k, v in kv.items():
            el[k] = v
    return f


def _text(new):
    def f(el, q):
        el.string = new
    return f


def _chips_only(el):
    """A plant: the element keeps its chips alone, its names and words gone."""
    chips = [copy.copy(c) for c in el.select(".oa-chip")]
    el.clear()
    for c in chips:
        el.append(c)
        el.append(NavigableString(" "))


PLANTS = [
    # (check, view the plant needs, selector, change, what it plants)
    ("T1", "reform", ".wa-tag", lambda el, q: _chips_only(el), "a chip whose record the page never names (CE1, R22)"),
    ("T1", "loop", '.oa-chip[data-atlas-kind="Connection"]', lambda el, q: (el.__setitem__("data-atlas-kind", "Variable"), el.contents.__setitem__(0, NavigableString("Variable "))), "a connection's chip under the kind Variable"),
    ("T2", "loop", '[data-atlas-kind="Connection"][data-atlas-id="L15"][data-grade]', _set(**{"data-grade": "documented"}), "Connection L15 printed as documented [Q09]"),
    ("T3", "loop", "[data-count]", lambda el, q: (el.__setitem__("data-count", str(int(el["data-count"]) + 1))), "a count one higher than the model's"),
    ("T4", "loop", "[data-atlas-reads]", lambda el, q: el.__setitem__("data-atlas-reads", el["data-atlas-reads"].replace("falls", "rises", 1)), "the read-aloud line that turns at no minus"),
    ("T5", "loop", 'svg [data-atlas-kind="Connection"]', _set(**{"data-type": "authority"}), "a loop's step drawn as authority with its sign"),
    ("T6", "loop", ".wa-tag .oa-chip", _set(**{"data-red": "working", "data-red-job": "where a reform acts"}), "another reform's tag in red"),
    ("T7", "loop", "[data-effect-family]", lambda el, q: el.__setitem__("data-effect-code", "+L"), "an effect code the record does not hold"),
    ("T7", "loop", "[data-effects-confidence]", lambda el, q: el.decompose(), "a loop panel with no confidence line (ST-1, R21)"),
    ("T8", "loop", "[data-route]", lambda el, q: el.__setitem__("data-checked", RF[el["data-atlas-reform"]]["status"]["checked"]), "a route dated from its reform's status"),
    ("T9", "loop", "[data-evidence-href]", lambda el, q: (el.__setitem__("data-evidence-href", "/atlas/register/d01#register-l14"), el.__setitem__("href", "/atlas/register/d01#register-l14") if el.name == "a" else None), "a step's evidence linked to the wrong sheet"),
    ("T10", "loop", ".wa-gl", lambda el, q: el.append(NavigableString(" well-supported")), "a grade in its stored spelling"),
    ("T10", "reform", '[data-reading="2"] .ws-p', lambda el, q: el.append(NavigableString(" An added sentence.")), "a remedy block that no longer rejoins to the stored text"),
    ("T10", "reform", '[data-reading-label="2"]', lambda el, q: el.decompose(), "the second reading with no label (RP1, R23)"),
    ("T11", "loop", ".oa-stepper-step", lambda el, q: el.__setitem__("data-oa-hold", "3200"), "a step held 3,200 ms (registers F-8, F-15)"),
    ("T11", "loop", "[data-oa-stepper]", _set(**{"data-oa-part": "stepper"}), "a part name on the stepper's root, which the script says before each step (AX-1)"),
    ("T12", "home", "[data-pathway][aria-pressed=\"true\"] || [data-pathway]", lambda el, q: (el.__setitem__("aria-pressed", "true"), [x.decompose() for x in el.select("svg")]), "a pressed question with no check"),
    ("T12", "home", '[data-pathway-answer="PW01"] [data-atlas-field="short_answer"] || [data-pathway-answer]:not([hidden])',
     lambda el, q: el.__setitem__("data-pathway-answer", "PW01") if el.has_attr("data-pathway-answer") else setattr(el, "string", V["pathways"][5]["short_answer"]),
     "a question's answer region holding another question's answer (R19, CD-M2)"),
    ("T12", "home", '.wa-box[data-part]:not([data-lit]) || [data-part][data-lit="false"]', _set(**{"data-lit": "true"}),
     "a part lit with no question pressed (R19, CD-R1)"),
    ("T12", "home", "[data-pathway]", lambda el, q: (setattr(q, "key", "frame 1440-light-screen"), setattr(q, "kind", "frame"), setattr(q, "full", False),
                                                     [x.__setitem__("aria-pressed", "false") for x in q.all("[data-pathway]")], el.__setitem__("aria-pressed", "true")),
     "a first screen drawn with a question pressed out of its window (CD-R1)"),
    ("T13", "loop", "@style:-soup-contains('.ws ')", lambda el, q: el.append(NavigableString(".x{color:#ffffff}")), "a literal White in the page's style"),
    ("T14", "loop", "main", lambda el, q: setattr(q, "facts", {"words": [{"text": "small words", "size": 12, "color": "rgb(18, 18, 18)", "bg": "rgb(250, 247, 240)", "weight": "400"}]}), "words at 12 px"),
    ("T15", "loop", ".oa-masthead-part[aria-current]", lambda el, q: el.attrs.pop("aria-current"), "no current part in the site's masthead"),
    ("T15", "reform", "main", lambda el, q: setattr(q, "title", "Reform R-01, " + RF["R-01"]["title"] + " | " + V["meta"]["title"] + " | Oath & Action"), "a reform page whose tab title names another record (PR-S9)"),
    ("T15", "home", "main", lambda el, q: (setattr(q, "kind", "frame"), setattr(q, "full", False), setattr(q, "theme", "light"), q.root.attrs.pop("data-oa-theme", None)),
     "a light frame whose page names no theme, so the guide's dark reaches it (PR-S8, CD-R5)"),
    ("T16", "loop", "main", lambda el, q: el.append(BeautifulSoup("<p>Who Do They Answer To? Times Explainer</p>", "lxml").p), "a newspaper's name"),
    # the data lead's batch 1, job 4: the gaps, one plant each
    ("T1", "register", "main", lambda el, q: setattr(q, "facts", {**(q.facts or {}), "width": 390, "rowheads": [{"text": "Connection L10", "shown": False}]}), "a row's head hidden on a phone (request 15)"),
    ("T2", "loop", 'svg g[data-atlas-id="L15"]', lambda el, q: [p.__setitem__("stroke-dasharray", "0 6") for p in el.select("path.ak-mark")], "a plausible step drawn dotted"),
    ("T2", "register", 'tr[data-sign="-"]', lambda el, q: [s.replace_with(str(s).replace("lowers", "raises")) for s in el.find_all(string=re.compile("lowers"))], "a minus row whose word reads raises"),
    ("T2", "register", 'tr[data-grade="documented"]', lambda el, q: [x.decompose() for x in el.select("svg.rs")], "a Documented row with no record square (request 13)"),
    ("T6", "loop", '[data-atlas-for]:not(.wa-fv--on) svg [data-atlas-kind="Variable"] || [data-atlas-for] svg [data-atlas-kind="Variable"][data-atlas-id="D2"]', _set(**{"data-red": "working", "data-red-job": "where a reform acts"}), "red on a variable the second chooser state's reform does not target (request 17)"),
    ("T6", "how-to-read", ".wa-marks svg.tgt", lambda el, q: el.__setitem__("class", ["ln"]), "How to read's red target sample drawn in ink (request 23)"),
    ("T9", "reform", '.wa-note [data-atlas-kind="Connection"]', lambda el, q: el.decompose(), "a drawn connection named nowhere (request 8)"),
    ("T10", "loop-index", "[data-grade-text]", lambda el, q: el.append(NavigableString(" plausible_contested")), "a stored spelling in a loop index grade cell (request 21)"),
    ("T13", "loop", "main", lambda el, q: setattr(q, "contrast", {"secondary": {"token": "oa.color.state.muted.mark", "ratio": 2.8}}), "a muted mark at 2.8 to 1"),
    ("T14", "loop", "svg text", lambda el, q: (el.clear(), el.append(q.soup.new_tag("tspan")), el.append(q.soup.new_tag("tspan")),
                                               el.contents[0].append("2 lowers the"), el.contents[1].append("rules")), "a two-line step label ending on one word"),
]


def self_test(out_dir, plates_dir=PLATES):
    allp = [p for p in pages(out_dir, plates_dir) if p.root] if out_dir else [p for p in plate_pages(plates_dir) if p.root]
    pgs = [p for p in allp if p.kind == "export"] or [p for p in allp if p.full]
    bad, report = 0, []

    def say(ok, msg):
        nonlocal bad
        print(("pass " if ok else "FAIL ") + msg)
        report.append(("pass " if ok else "FAIL ") + msg)
        bad += not ok
    if not pgs:
        say(False, "no atlas page to test in " + str(out_dir))
        return bad, report
    clean = [ln for pg in pgs for ln in run_page(pg) if not ln[1]]
    say(not clean, f"the clean pages stay quiet: {len(pgs)} page(s), {len(clean)} FAIL line(s)" + (f", first: {clean[0][2]}" if clean else ""))
    for c, view, sels, fn, what in PLANTS:
        # a plant may name a second place, " || " apart, for a run on the plates alone: a frame holds the one state it shows
        # (the chooser's other drawings are not in a frame), so there the plant goes on the shown drawing
        base, sel = None, None
        for sel in sels.split(" || "):
            base = next((p for p in pgs if p.view == view and (p.soup.select_one(sel[1:]) if sel.startswith("@") else p.root.select_one(sel))), None)
            if base:
                break
        if not base:
            say(False, f"{c}: not planted, no {view} page holds {sels!r} ({what})")
            continue
        q = _sub(base, sel, fn)
        got = [ln for ln in run_page(q, [c]) if not ln[1]]
        say(bool(got), f"{c} catches {what} in {base.where}" + (f": {got[0][2]}" if got else ": not caught"))
    return bad, report


if __name__ == "__main__":
    a = sys.argv[1:]
    plates = Path(a[a.index("--plates") + 1]) if "--plates" in a else PLATES
    ids = None
    if "--ids" in a:
        ids = [x for x in a[a.index("--ids") + 1:] if re.match(r"^A\d+$", x)]
    if "--self-test" in a:
        rest = [x for x in a if not x.startswith("--") and x not in (str(plates),) and not re.match(r"^A\d+$", x)]
        b, _ = self_test(rest[0] if rest else None, plates)
        print(f"self-test: {'PASS' if not b else 'FAIL'}, {len(PLANTS)} plants, {b} miss(es)")
        sys.exit(1 if b else 0)
    if not a or a[0].startswith("--"):
        print(__doc__)
        sys.exit(2)
    res = run(a[0], plates, ids)
    js = a[a.index("--json") + 1] if "--json" in a else None
    fails = [ln for ln in res if not ln[1]]
    print(f"atlas test: {sum(1 for x in res if x[1])} PASS, {len(fails)} FAIL")
    if js:
        Path(js).write_text(json.dumps({"model_sha256": __import__("hashlib").sha256(MODEL_PATH.read_bytes()).hexdigest(),
                                        "lines": [ln for _, _, ln in res]}, indent=1, ensure_ascii=False))
    sys.exit(1 if fails else 0)
