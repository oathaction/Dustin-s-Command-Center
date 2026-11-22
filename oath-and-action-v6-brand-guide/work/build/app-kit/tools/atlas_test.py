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

    @property
    def where(self):
        return f"{self.app} {self.key}"

    def all(self, sel):
        return self.root.select(sel) if self.root else []

    def filter_on(self):
        return {i.get("value") for i in self.all('input[type="checkbox"][data-atlas-filter]') if i.has_attr("checked")}

    def chosen(self):
        if self.view == "reform":
            return self.record
        c = self.all("input.oa-choice-input[checked]")
        return c[0].get("value") if c else None


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
EXPECT = {"T2": {"loop", "reform", "register"}, "T3": {"home", "register", "loop"}, "T4": {"loop"}, "T6": {"reform", "loop"},
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
    return faults, n


def line_of(g):
    dash = [p.get("stroke-dasharray") for p in g.select("path.ak-mark") if p.get("stroke-dasharray")]
    return "solid" if not dash else "patterned"


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
            got, want = line_of(el), "solid" if GRADE_LINE[x["evidence"]] == "solid" else "patterned"
            if got != want:
                faults.append(f"Connection {i}: drawn {got}, its grade {GRADE_WORD[x['evidence']]} takes a {GRADE_LINE[x['evidence']]} line (Rule 13.4)")
        else:
            tx = text(el)
            for g, w in GRADE_WORD.items():
                if re.search(r"\b" + w + r"\b", tx) and w != GRADE_WORD[x["evidence"]]:
                    faults.append(f"Connection {i}: printed {w}, model {GRADE_WORD[x['evidence']]}")
                    break
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
    reds = pg.all('[data-red="working"]')
    chosen = pg.chosen()
    tg = set(RF[chosen]["targets"]) if chosen in RF else set()
    jobs = {el.get("data-red-job") for el in reds}
    if len(jobs) > 1:
        faults.append(f"{len(jobs)} working reds of different jobs in one view: {sorted(j or '' for j in jobs)} (Rule 05.3)")
    for el in reds:
        n += 1
        i = el.get("data-atlas-id")
        if pg.view not in ("reform", "loop"):
            faults.append(f"{el.get('data-atlas-kind')} {i}: red on a {pg.view} page, which takes none (R10)")
        elif i not in tg:
            faults.append(f"{el.get('data-atlas-kind')} {i}: red, and Reform {chosen} does not target it (Rule 12.5)")
        if "oa-chip" in (el.get("class") or []) or in_any(el, [".wa-tag", ".oa-chip", "button", "h1", "h2"]):
            faults.append(f"{i}: red on a chip, tag, button or heading (R10)")
    drawn = {el.get("data-atlas-id") for el in pg.all("svg [data-atlas-id]")}
    for t in sorted(tg & drawn):
        n += 1
        if not any(el.get("data-atlas-id") == t for el in reds):
            faults.append(f"{t}: Reform {chosen}'s target, drawn and not red (Rule 12.5, R10)")
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
        want = RF[rid]["status"]["checked"] if rid in RF else V["meta"]["snapshot"]
        if el.get("data-status-date") != want:
            faults.append(f"{'Reform ' + rid if rid else 'the snapshot'}: dated {el.get('data-status-date')!r}, model {want!r}")
        if words_date(want) not in text(el):
            faults.append(f"{'Reform ' + rid if rid else 'the snapshot'}: the date {words_date(want)} does not print in words")
    # a frame carries only what its width shows (D4-152), so the title bar's date is read on the working page
    if not pg.all(".wa-tb [data-status-date]") and pg.kind == "export":
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
    pair = pg.all("[data-reading]")
    if pair:
        n += 1
        ls = [len(text(x)) for x in pair]
        if len(ls) != 2 or max(ls) - min(ls) > 75:
            faults.append(f"a contested remedy prints {len(ls)} readings of {ls} characters; two within a line's length (H08)")
    return faults, n


STEP_ORDER = [("oa-stepper-play", "Play"), ("oa-stepper-reset", "Reset the loop"), ("oa-stepper-prev", "Previous step"), ("oa-stepper-next", "Next step")]


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
            said = f"Step {i} of {len(steps)}: " + " ".join(text(x) for x in s.select(".oa-stepper-line, .oa-stepper-more"))
            want = max(6000, 250 * len(said.split()))
            if s.get("data-oa-hold") != str(want):
                faults.append(f"step {i}: holds {s.get('data-oa-hold')} ms, its {len(said.split())} words take {want} (AL-24)")
            if not s.select(".oa-stepper-more"):
                faults.append(f"step {i}: no more words for the status line to read (chapter 18's stepper reads line and more)")
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
    for q in pressed:
        if not q.select("svg use[href*='selected-check'], svg.oa-toggle-check"):
            faults.append(f"question {q.get('data-pathway')}: pressed with no check (AL-21)")
        pw = next((x for x in V["pathways"] if x["id"] == q.get("data-pathway")), None)
        want = {part(v) for v in pw["model_refs"]["nodes"]} if pw else set()
        lit = {b.get("data-part") for b in pg.all('[data-part][data-lit="true"]')}
        if pg.full and lit != want:
            faults.append(f"question {q.get('data-pathway')}: lit parts {sorted(lit)}, its variables sit in {sorted(want)}")
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
        css = st.get_text()
        if "@font-face" in css or "--oa-color-palette-newsprint:" in css:
            continue    # the fonts and tokens.css, the one source of colors
        for m in LITERAL.finditer(css):
            faults.append(f"a literal color {css[m.start():m.start() + 12]!r} in the page's style; every color from a token (AL-23)")
            break
    if pg.theme == "dark":
        for st in pg.soup.find_all("style"):
            css = st.get_text()
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
    return faults, n


def t14(pg):
    faults, n = [], 0
    for w in (pg.facts or {}).get("words", []):
        n += 1
        if w["size"] < 13 - 0.01:
            faults.append(f"{w['text'][:30]!r}: {w['size']} px, under 13 (ED-F9)")
    for t in pg.all("svg text"):
        spans = t.find_all("tspan", recursive=False)
        if len(spans) > 1 and len(text(spans[-1]).split()) == 1 and len(text(t).split()) > 1 and not re.match(r"^\d", text(spans[0])):
            n += 1
            faults.append(f"the label {text(t)!r} ends its last line on one word (ED-F9)")
    return faults, n


SITE = {}


def site_words():
    if not SITE:
        import subprocess
        r = subprocess.run(["python3", "-I", str(ROOT / "work/build/scripts/phase-4/phase4_ch20_build.py"), "--page-words", "A06"],
                           capture_output=True, text=True, cwd=str(ROOT))
        SITE.update(json.loads(r.stdout)["site"] if r.returncode == 0 else {})
    return SITE


def t15(pg):
    faults, n = [], 1
    head = pg.root.select_one("header.oa-masthead") if pg.root else None
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
    nav = pg.all(".wa-tb nav[aria-label]")
    if not nav and (pg.kind == "export" or not pg.all(".wa-tb-toggle")):
        faults.append("no title bar navigation named for the atlas's views")
    bc = pg.all('nav.wa-bc[aria-label]')
    if pg.view != "home" and not bc:
        faults.append("no breadcrumb below the home (AL-09)")
    if pg.view == "home" and bc:
        faults.append("a breadcrumb on the home page")
    foot = pg.root.select_one("footer.ws-foot")
    sw = site_words()
    if not foot:
        faults.append("no site footer")
    elif sw:
        heads = [text(h) for h in foot.select("h2")]
        if heads != [g[0] for g in sw["footer"]["groups"]]:
            faults.append(f"the footer's lists read {heads}, the website's {[g[0] for g in sw['footer']['groups']]} (3.2.6)")
    if pg.full and len(pg.all("main h1")) != 1:
        faults.append(f"{len(pg.all('main h1'))} h1 in main, one asked (AL-10)")
    if pg.title is not None:
        p = pg.title.split(" | ")
        if len(p) != 3 or p[1] != V["meta"]["title"] or p[2] != "Oath & Action":
            faults.append(f"the page title {pg.title!r} is not '[view] | {V['meta']['title']} | Oath & Action' (AL-01)")
    return faults, n


RETIRED = ["Times Explainer", "Yes on 3", "Veterans for All Voters", "Ranked Choice Melrose", "Oath & Action's editor works with",
           "Oath & Action’s editor works with"]


def t16(pg):
    faults, n = [], 1
    tx = text(pg.root) if pg.root else ""
    for w in RETIRED:
        if w in tx or (pg.title and w in pg.title):
            faults.append(f"{w!r} prints: a newspaper's name (ED-F8) or the editor's disclosure (DR-100)")
    for t in [pg.title or ""] + [text(h) for h in pg.all("h1")]:
        for m in ID_RE.finditer(t):
            if m.group(1) in set(LO) | set(RF) and not re.search(r"(Loop|Reform)\s+" + re.escape(m.group(1)), t):
                faults.append(f"{m.group(1)}: a bare loop or reform code in a title, {t!r}")
    return faults, n


FNS = {f"T{i}": f for i, f in enumerate([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16], 1)}


def run_page(pg, only=None):
    """One line a check for the page: (check, ok, line)."""
    out = []
    for c in only or CHECKS:
        faults, n = FNS[c](pg)
        if not faults and not n and pg.full and pg.view in EXPECT.get(c, set()):
            faults = [f"found nothing to check on a {pg.view} page, which must hold it"]
        if faults:
            out += [(c, False, f"FAIL {c} {pg.where}: {f}") for f in faults]
        else:
            out.append((c, True, f"PASS {c} {pg.where}: {NAMES[c].lower()}, {n} read"))
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
                res.append(pg)
    return res


def frame_html(inner, pdata, plates_dir):
    """A frame's page as the guide shows it: its markup, with the kit's styles its plate stands on (contract C4)."""
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


PLANTS = [
    # (check, view the plant needs, selector, change, what it plants)
    ("T1", "loop", '.oa-chip[data-atlas-kind="Connection"]', lambda el, q: (el.__setitem__("data-atlas-kind", "Variable"), el.contents.__setitem__(0, NavigableString("Variable "))), "a connection's chip under the kind Variable"),
    ("T2", "loop", '[data-atlas-kind="Connection"][data-atlas-id="L15"][data-grade]', _set(**{"data-grade": "documented"}), "Connection L15 printed as documented [Q09]"),
    ("T3", "loop", "[data-count]", lambda el, q: (el.__setitem__("data-count", str(int(el["data-count"]) + 1))), "a count one higher than the model's"),
    ("T4", "loop", "[data-atlas-reads]", lambda el, q: el.__setitem__("data-atlas-reads", el["data-atlas-reads"].replace("falls", "rises", 1)), "the read-aloud line that turns at no minus"),
    ("T5", "loop", 'svg [data-atlas-kind="Connection"]', _set(**{"data-type": "authority"}), "a loop's step drawn as authority with its sign"),
    ("T6", "loop", ".wa-tag .oa-chip", _set(**{"data-red": "working", "data-red-job": "where a reform acts"}), "another reform's tag in red"),
    ("T7", "loop", "[data-effect-family]", lambda el, q: el.__setitem__("data-effect-code", "+L"), "an effect code the record does not hold"),
    ("T8", "loop", "[data-route]", lambda el, q: el.__setitem__("data-checked", RF[el["data-atlas-reform"]]["status"]["checked"]), "a route dated from its reform's status"),
    ("T9", "loop", "[data-evidence-href]", lambda el, q: (el.__setitem__("data-evidence-href", "/atlas/register/d01#register-l14"), el.__setitem__("href", "/atlas/register/d01#register-l14") if el.name == "a" else None), "a step's evidence linked to the wrong sheet"),
    ("T10", "loop", ".wa-grades", lambda el, q: el.append(NavigableString(" well-supported")), "a grade in its stored spelling"),
    ("T11", "loop", ".oa-stepper-step", lambda el, q: el.__setitem__("data-oa-hold", "3200"), "a step held 3,200 ms (registers F-8, F-15)"),
    ("T12", "home", "[data-pathway][aria-pressed=\"true\"]", lambda el, q: [x.decompose() for x in el.select("svg")], "a pressed question with no check"),
    ("T13", "loop", "@style:-soup-contains('.ws ')", lambda el, q: el.append(NavigableString(".x{color:#ffffff}")), "a literal White in the page's style"),
    ("T14", "loop", "main", lambda el, q: setattr(q, "facts", {"words": [{"text": "small words", "size": 12, "color": "rgb(18, 18, 18)", "bg": "rgb(250, 247, 240)", "weight": "400"}]}), "words at 12 px"),
    ("T15", "loop", ".oa-masthead-part[aria-current]", lambda el, q: el.attrs.pop("aria-current"), "no current part in the site's masthead"),
    ("T16", "loop", "main", lambda el, q: el.append(BeautifulSoup("<p>Who Do They Answer To? Times Explainer</p>", "lxml").p), "a newspaper's name"),
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
    for c, view, sel, fn, what in PLANTS:
        base = next((p for p in pgs if p.view == view and (p.soup.select_one(sel[1:]) if sel.startswith("@") else p.root.select_one(sel))), None)
        if not base:
            say(False, f"{c}: not planted, no {view} page holds {sel!r} ({what})")
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
