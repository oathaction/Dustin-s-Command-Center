"""The V7 check, grown for Phase 3 round 0 (proposal section 7, first row), from atlas_concepts_verify.py and
dataviz_verify.py: every Atlas V7 ID and value that chapters 13 to 15 and the chart kit print, against the model.

Usage:
    python3 -I work/build/scripts/phase-3/v7_check.py --page PAGE.html [--out RESULTS.json]
    python3 -I work/build/scripts/phase-3/v7_check.py --self-test

Reads work/extract/atlas-v7-data.json (snapshot of October 15, 2026; never edited), the built guide page, the chart kit's
specs (work/build/chart-kit/specs/, the chapter 13 plates' .chart.json) and its data folder (work/build/data/).

In chapters 13, 14 and 15 of the page it checks, outside failure plates, which show faults on purpose:
  ids        every ID chip (<span class="id"> or <span class="oa-id">) names an atlas ID or one of V7's route codes
  typed      a chip for a variable, connection, loop, reform or issue carries its type word (H11)
  bare       no atlas ID prints bare in reader text: its sentence names its type before it (H11)
  grade      a block (p, li, tr, figcaption) that names one connection and a grade word gives V7's grade for it
  sign       a block that names one connection and a sign gives V7's sign; an authority connection carries no sign or loop
  route      a block that names a reform and one route code prints that route's check date when V7 dates it, and never
             calls an undated route checked
  tally      no effect total, tally or sum of a reform's effects
  disclosure no copy of the retired disclosure (DR-100, D2-1756)
And in the kit: every v7-*.json data file is what the model gives today (every V7 value S01 to S16 draw), and the kit's
own check passes on every spec (IDs, grades and the verbs a grade allows, typed chips). --self-test plants each fault.
"""
import argparse
import html
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
V7P = ROOT / "work/extract/atlas-v7-data.json"
KIT = ROOT / "work/build/chart-kit"
DATA = ROOT / "work/build/data"
CHAPTERS = {"evidence": "13", "data-visualization": "14", "systems-graphics": "15"}
GRADE_WORDS = {"documented": "documented", "well supported": "well-supported", "well-supported": "well-supported",
               "plausible": "plausible", "contested": "contested", "hypothesis": "hypothesis"}
DISCLOSURE = re.compile(r"Yes on 3|Veterans for All Voters|Ranked Choice Melrose|\bDisclosure:", re.I)
TALLY = re.compile(r"\b(total effect|net effect|effects? (?:add|adds|added|sum|sums|summed) up|sum of (?:its |the )?effects|effect score|tally of (?:its |the )?effects)\b", re.I)
TYPE_WORD = {"node": "Variable", "link": "Connection", "loop": "Loop", "reform": "Reform", "issue": "Issue"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


class Kinds(set):
    """The kinds of record one ID names; == compares with one kind, as most IDs name one."""
    def __eq__(self, other):
        return other in self if isinstance(other, str) else set.__eq__(self, other)
    __hash__ = None


def model():
    d = json.loads(V7P.read_text())
    ids = {}
    add = lambda k, kind: ids.setdefault(k, Kinds()).add(kind)
    for k in d["nodes"]: add(k, "node")
    for k in d["links"]: add(k, "link")
    for k in d["loops"]: add(k, "loop")
    for k in d["reforms"]: add(k, "reform")
    for k in d["issues"]: add(k, "issue")
    for p in d["pathways"]: add(p["id"], "pathway")
    for r in d["repairLog"]["rows"]: add(r["id"], "repair")
    for k in d["deliveryLog"]: add(k, "delivery")
    for x in d["domains"]: add(x["id"], "domain")
    for x in d["overlays"]: add(x["id"], "overlay")
    routes = set()
    for r in d["reforms"].values():
        for x in r.get("routes") or []:
            routes.add(x["route"])
    return d, ids, routes


def words_date(iso):
    y, m, dd = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {int(dd)}, {y}"


def chapter_slices(page):
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'<section class="chapter[^"]*" id="([^"]+)"', page)]
    out = {}
    for (s, a), nxt in zip(marks, [m[0] for m in marks[1:]] + [len(page)]):
        if a in CHAPTERS:
            out[CHAPTERS[a]] = page[s:nxt]
    return out


def strip_failures(h):
    # a failure plate shows a fault on purpose; its figure is left out of every check here
    return re.sub(r'<figure class="plate plate--failure".*?</figure>', " ", h, flags=re.S)


def visible(h):
    h = re.sub(r"<(script|style|svg|code|pre)\b.*?</\1>", " ", h, flags=re.S | re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", h))


def check_html(h, d, ids, routes, where):
    f = []
    h = strip_failures(h)
    chip_re = re.compile(r'<span class="(?:id|oa-id)"(?: data-oa-id="[^"]*")?>([^<]+)</span>')
    for m in chip_re.finditer(h):
        raw = html.unescape(m.group(1)).strip()
        code = raw.split(" ")[-1]
        if code not in ids and code not in routes:
            f.append(f"{where}: ids: chip {raw!r} names no atlas ID or route code")
            continue
        kinds = [k for k in ids.get(code, ()) if k in TYPE_WORD]
        if kinds:
            before = (visible(h[max(0, m.start() - 160):m.start()]) + " " + raw)[-(len(raw) + 24):].lower()
            if not any(TYPE_WORD[k].lower() in before for k in kinds):
                f.append(f"{where}: typed: {code} prints without its type word ({' or '.join(TYPE_WORD[k] for k in kinds)} {code}, H11)")
    # bare IDs: atlas IDs in reader text outside any chip
    text = visible(chip_re.sub(" ", h))
    # an ID is bare when its sentence, up to the ID, never names its type ("Loop R10", "Loops R1 and R10", "Connections L01 to L03")
    for m in re.finditer(r"(?<![\w-])((?:RL|PW|DL)\d{2}|R-\d{2}|L[ETR]?\d{2}|LX\d{1,2}|T\d{2}|I\d{3}|[A-E]\d{1,2}|[RB]\d{1,2}[ab]?)(?![\w-])", text):
        code = m.group(1)
        kinds = [k for k in ids.get(code, ()) if k in TYPE_WORD]
        if kinds:
            sentence = re.split(r"[.;!?]\s", text[max(0, m.start() - 160):m.start()])[-1].lower()
            # "the code B4" names the code itself, as Rule 13.9's plates do when they explain chips
            if not any(TYPE_WORD[k].lower() in sentence for k in kinds) and not re.search(r"\b(?:the |a )?(?:code|id|bare)\s*$", sentence):
                f.append(f"{where}: bare: {code} prints with no type word before it (H11)")
    # block by block: grades, signs, routes
    for b in re.finditer(r"<(p|li|tr|figcaption)\b[^>]*>(.*?)</\1>", h, flags=re.S):
        blk = b.group(2)
        codes = [html.unescape(x).split(" ")[-1] for x in chip_re.findall(blk)]
        links = [c for c in codes if ids.get(c) == "link"]
        reforms = [c for c in codes if ids.get(c) == "reform"]
        rts = [c for c in codes if c in routes and c not in ids]
        txt = visible(blk).lower()
        if len(set(links)) == 1:
            L = d["links"][links[0]]
            gw = [GRADE_WORDS[w] for w in GRADE_WORDS if re.search(r"\b" + re.escape(w) + r"\b", txt)]
            # a compound V7 grade such as plausible_contested prints as either of its words (the guide's mapping table)
            if gw and L.get("evidence") and L["evidence"] not in gw and not any(g in L["evidence"].split("_") for g in gw):
                f.append(f"{where}: grade: {links[0]} printed as {', '.join(sorted(set(gw)))}; V7 grades it {L['evidence']}")
            if L.get("type") == "authority":
                if re.search(r"(?:^|\s)[+−−-](?:\s|$)|\bpositive\b|\bnegative\b|\bloop\b", txt):
                    f.append(f"{where}: sign: authority connection {links[0]} is given a sign or a loop")
            else:
                signs = set(re.findall(r"(?:^|\s)([+−])(?=\s|$)", txt))
                want = "+" if L.get("polarity") == "+" else "−"
                if signs and signs != {want}:
                    f.append(f"{where}: sign: {links[0]} printed {''.join(sorted(signs))}; V7's sign is {L.get('polarity')}")
        if len(set(reforms)) == 1 and len(set(rts)) == 1:
            entry = next((x for x in d["reforms"][reforms[0]].get("routes") or [] if x["route"] == rts[0]), None)
            if entry is None:
                f.append(f"{where}: route: {reforms[0]} has no route {rts[0]} in V7")
            elif entry.get("checked"):
                if words_date(entry["checked"]).lower() not in txt and entry["checked"] not in txt and "not checked" in txt:
                    f.append(f"{where}: route: {reforms[0]} {rts[0]} is dated {entry['checked']} in V7, printed as not checked")
            elif re.search(r"\bchecked (?:on )?(?:" + "|".join(MONTHS).lower() + r")", txt) and "not checked" not in txt:
                f.append(f"{where}: route: {reforms[0]} {rts[0]} has no check date in V7, printed as checked")
    if TALLY.search(text):
        f.append(f"{where}: tally: {TALLY.search(text).group(0)!r}; a reform's effects are never added or tallied")
    if DISCLOSURE.search(visible(h)):
        f.append(f"{where}: disclosure: the retired disclosure prints (DR-100)")
    return f


def check_kit_data():
    """Every v7-*.json is what the model gives today: rebuild them in memory with the data script's own code."""
    f = []
    spec = importlib.util.spec_from_file_location("data_round0_build", ROOT / "work/build/scripts/phase-3/data_round0_build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        mod.OUT = Path(td)
        mod.v7_tables()
        for p in sorted(Path(td).glob("v7-*.json")):
            if p.name.endswith(".meta.json"):
                continue
            have = DATA / p.name
            if not have.exists():
                f.append(f"kit data: {p.name} is missing from work/build/data/")
            elif json.loads(have.read_text()) != json.loads(p.read_text()):
                f.append(f"kit data: {p.name} differs from what Atlas V7 gives today")
    for p in sorted(DATA.glob("*.json")) + sorted(DATA.glob("*.csv")):
        if DISCLOSURE.search(p.read_text()):
            f.append(f"kit data: {p.name} carries the retired disclosure")
    return f


def check_kit_specs(spec_paths):
    f = []
    if not spec_paths:
        return f
    r = subprocess.run(["node", str(KIT / "oa-chart.mjs"), "check"] + [str(p) for p in spec_paths], capture_output=True, text=True, cwd=str(ROOT))
    cur = None
    for line in r.stdout.splitlines():
        if line.startswith(("PASS", "FAIL")):
            cur = line.split()[1]
        elif line.startswith("  - ") and cur and re.search(r"\b(v7|words|source)\b:", line):
            f.append(f"kit spec {cur}: {line[4:]}")
    if r.returncode not in (0, 1):
        f.append(f"kit: the check did not run: {r.stderr[:300]}")
    return f


def run(page_path):
    d, ids, routes = model()
    page = Path(page_path).read_text()
    res = {"page": str(page_path), "snapshot": d["meta"]["snapshot"], "chapters": {}, "failures": []}
    for n, h in sorted(chapter_slices(page).items()):
        fl = check_html(h, d, ids, routes, f"chapter {n}")
        res["chapters"][n] = {"chips": len(re.findall(r'<span class="(?:id|oa-id)"', strip_failures(h))), "failures": len(fl)}
        res["failures"] += fl
    res["failures"] += check_kit_data()
    specs = sorted((KIT / "specs").glob("s*.json")) + sorted((ROOT / "work/build/guide/specimens").glob("*.chart.json"))
    res["kit_specs"] = len(specs)
    res["failures"] += check_kit_specs(specs)
    return res


def self_test():
    d, ids, routes = model()
    L25 = d["links"]["L25"]
    auth = next(k for k, v in d["links"].items() if v.get("type") == "authority")
    undated = next((r, x["route"]) for r, v in d["reforms"].items() for x in v.get("routes") or [] if not x.get("checked"))
    dated = next((r, x["route"], x["checked"]) for r, v in d["reforms"].items() for x in v.get("routes") or [] if x.get("checked"))
    other = "plausible" if L25["evidence"] != "plausible" else "documented"
    sign_bad = "−" if L25["polarity"] == "+" else "+"
    chip = lambda c, t: f'<span class="chip">{t} <span class="id">{c}</span></span>'
    sec = lambda body: f'<section class="chapter" id="evidence">{body}</section>'
    cases = [
        ("a chip that names no atlas ID", f"<p>{chip('L99x', 'Connection')}</p>", "ids:"),
        ("a chip without its type word", '<p><span class="id">R10</span> is a loop.</p>', "typed:"),
        ("a bare atlas ID", "<p>R10 shifts accountability.</p>", "bare:"),
        # the systems designer's request (round 1): connections whose IDs start with T or LX
        ("a bare T connection", "<p>T12 carries the delay.</p>", "bare:"),
        ("a bare LX connection", "<p>LX4 closes the loop.</p>", "bare:"),
        ("a connection given the wrong grade", f"<p>{chip('L25', 'Connection')} <b>{other.capitalize()}</b>.</p>", "grade:"),
        ("a connection given the wrong sign", f"<p>{chip('L25', 'Connection')} {sign_bad} </p>", "sign:"),
        ("an authority connection given a sign", f"<p>{chip(auth, 'Connection')} + </p>", "sign:"),
        ("an undated route printed as checked", f"<p>{chip(undated[0], 'Reform')} {chip(undated[1], 'Route')} checked October 15, 2026.</p>", "route:"),
        ("a dated route printed as not checked", f"<p>{chip(dated[0], 'Reform')} {chip(dated[1], 'Route')} not checked.</p>", "route:"),
        ("an effect total", "<p>The reform's total effect is +3.</p>", "tally:"),
        ("the retired disclosure", "<p>Disclosure: the editor works with the Yes on 3 campaign.</p>", "disclosure:"),
    ]
    bad = 0
    for name, body, want in cases:
        fl = check_html(sec(body), d, ids, routes, "self-test")
        ok = any(want in x for x in fl)
        print(f"{'caught' if ok else 'MISSED'} {name}" + ("" if ok else f": {fl}"))
        bad += not ok
    clean = f"<p>{chip('L25', 'Connection')} <b>{L25['evidence'].replace('-', ' ').capitalize()}</b>.</p>"
    fl = check_html(sec(clean), d, ids, routes, "self-test")
    print(f"{'pass' if not fl else 'FAIL'} a correct connection passes" + ("" if not fl else f": {fl}"))
    bad += bool(fl)
    fl = check_html(sec(f'<figure class="plate plate--failure"><p>Loop R10 bare on purpose.</p></figure>'), d, ids, routes, "self-test")
    print(f"{'pass' if not fl else 'FAIL'} a failure plate's planted fault is left out")
    bad += bool(fl)
    print("v7_check self-test: " + ("every planted fault caught" if not bad else f"{bad} failed"))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page")
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(1 if self_test() else 0)
    res = run(a.page)
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False))
    for n, c in res["chapters"].items():
        print(f"chapter {n}: {c['chips']} chips, {c['failures']} failures")
    print(f"kit: {res['kit_specs']} specs and the data folder")
    for x in res["failures"][:60]:
        print("  FAIL", x)
    print(f"{'PASS' if not res['failures'] else 'FAIL'} v7 check: {len(res['failures'])} failures")
    sys.exit(1 if res["failures"] else 0)


if __name__ == "__main__":
    main()
