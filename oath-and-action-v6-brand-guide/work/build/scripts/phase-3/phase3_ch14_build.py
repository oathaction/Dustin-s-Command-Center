"""Chapter 14, Data visualization: the chapter file, its manifest and its example log, assembled from the plan, the
editor's chapter file and entries, and the makers' entries and specs (Phase 3, round 1; the round 1 brief, Engineer 3).

Usage (from the project folder):
  python3 -I work/build/scripts/phase-3/phase3_ch14_build.py [--rounds 1,2]   write the files below; exit 1 on any fault
  python3 -I work/build/scripts/phase-3/phase3_ch14_build.py --check        fail if a file on disk is not what this writes

Reads   work/handoffs/phase-3/20261112_Chapter-14-Plan.json (every number, tier, round, spec and owner; R1)
        work/build/guide/entries/14-chapter.json (the editor's opener, introduction, group lines, related chapters, sources)
        work/build/guide/entries/14-NNN.json (one per rule: the editor's 14.1 to 14.14, the makers' entries; R2)
        work/build/chart-kit/specs/sNN.json (each entry's spec: its alt, its Illustrative label, its domain and states)
Writes  work/build/guide/chapters/14-data-visualization.json
        work/build/guide/specimens/manifest-data-visualization.json (every chapter 14 plate, the opener's and the rules')
        work/build/guide/specimens/s-14-sNN.html (one fragment per entry specimen: the chart placeholder, contract R1-C3)
        work/build/guide/entries/14-example-log.json (Rule 01.12's log for chapter 14, checked against DR-229's limits)

The chapter holds rules 14.1 to 14.14 and every entry of the rounds built (--rounds, default 1,2) whose entry file and
spec or sketch have landed; the plan's other numbers go into "planned_rules", so a citation of a rule not yet built is no
fault and prints unlinked until it is. A sketch entry's caption is the first sentence of its sketch_alt (R2-3). An entry
is a rule with "entry": true: its plate is its specimen, it takes no failure plate (DR-240), and when a spec serves two
entries the second names the first ("specimen_at") instead of drawing it again. Faults (a missing entry for a built round,
a number, tier or specimen that disagrees with the plan, a missing spec or sketch, Rule 01.9's limits passed) are listed
and the script exits 1, after writing what it can, so the makers can see their work in a build.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PLAN = ROOT / "work/handoffs/phase-3/20261112_Chapter-14-Plan.json"
ENTRIES = ROOT / "work/build/guide/entries"
SPECS = ROOT / "work/build/chart-kit/specs"
SPECIMENS = ROOT / "work/build/guide/specimens"
CHAPTER = ROOT / "work/build/guide/chapters/14-data-visualization.json"
MANIFEST = SPECIMENS / "manifest-data-visualization.json"
LOG = ENTRIES / "14-example-log.json"
DOMAIN_SHARE = 1 / 4      # DR-229: no atlas domain supplies more than one example in four in chapter 14
STATE_SHARE = 1 / 5       # and no state more than one in five
ENTRY_DROP = {"use_when", "use_instead", "specimen", "tier", "correct", "failure", "examples", "caption"}
SKETCH_LIMIT = {"reference": 4096, "avoid": 4096}   # R1-C1; D3-486 raises the avoid sketch to 4,096 bytes for its pair
SVG_WIDTH = re.compile(r'<svg\b[^>]*?\swidth="([\d.]+)"')
DESC = re.compile(r"<desc\b[^>]*>(.*?)</desc>", re.S)
# R2-3 (contract R2-C3): a sentence ends at a period, question mark or exclamation mark followed by a space and a capital
# letter, a digit or an opening quotation mark; an abbreviation (U.S., a single capital and its period, e.g.) does not end it
SENTENCE_END = re.compile(r"(?<=[.?!])[\u201d\u2019\"')]?\s+(?=[A-Z0-9\u201c\u2018\"])")
ABBREV = re.compile(r"(?:\b[A-Z]\.|\b(?:e\.g|i\.e|vs|No|St|Mr|Ms|Dr|Jr|Sr)\.)$")


def first_sentence(text):
    """The first sentence of a sketch's words (R2-3): up to the first end that is not an abbreviation's period."""
    t = re.sub(r"\s+", " ", str(text or "")).strip()
    for m in SENTENCE_END.finditer(t):
        head = t[:m.start()].rstrip()
        if ABBREV.search(head.rstrip("\u201d\u2019\"')")):
            continue
        return head
    return t


def unescape(t):
    return re.sub(r"\s+", " ", str(t).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'").replace("&#8217;", "\u2019")).strip()


def sketch_widths(path):
    """The true width of each drawing in a sketch file, in order (one, or an avoid entry's pair)."""
    try:
        return [int(float(w)) if float(w).is_integer() else float(w) for w in SVG_WIDTH.findall(path.read_text())]
    except OSError:
        return []


def same_basis(a, b):
    norm = lambda t: re.sub(r"\s+", " ", str(t or "")).strip().rstrip(".").lower()
    return bool(norm(a)) and norm(a) == norm(b)


def curly(t):
    """The guide's apostrophes and quotation marks (ED-E5): a straight ' or " in plan text becomes its curly form."""
    t = re.sub(r"(^|[\s(\[{])'", lambda m: m.group(1) + "\u2018", str(t))
    t = t.replace("'", "\u2019")
    t = re.sub(r'(^|[\s(\[{])"', lambda m: m.group(1) + "\u201c", t)
    return t.replace('"', "\u201d")
PLATE_META = ("width_px", "illustrative", "notes", "fit_switch", "interactive", "readable", "height_px", "surface", "scale", "check_exempt", "breakout")   # ED-E2: readable and the shell's other keys


def tier_of(t):
    return str(t or "").lower().split(",")[0].strip()


def num_key(rid):
    a, b = rid.split(".")
    return int(a), int(b)


def outputs(rounds):
    faults = []
    plan = json.loads(PLAN.read_text())
    chap = json.loads((ENTRIES / "14-chapter.json").read_text())
    built = [dict(r, kind="rule", tier=None) for r in plan["chapter_rules"] if r.get("round", 1) in rounds]
    built += [dict(f, kind="form") for f in plan["forms"] if f["round"] in rounds]
    planned = sorted({r["rule"] for r in plan["chapter_rules"]} | {f["rule"] for f in plan["forms"]}, key=num_key)
    rules, manifest, fragments, log, placed_spec = [], {}, {}, [], {}
    opener = dict(chap.get("opener") or {})
    if opener.get("specimen"):
        manifest[opener["specimen"]] = {"chapter": "14", "rule": None, "width_px": opener.get("width_px"), "alt": opener.get("alt", ""),
                                        "illustrative": bool(opener.get("illustrative")), "notes": opener.get("notes", "chapter 14's opener"),
                                        **{k: opener[k] for k in PLATE_META if k in opener and k not in ("width_px", "illustrative", "notes")}}
    for p in sorted(built, key=lambda r: num_key(r["rule"])):
        rid = p["rule"]
        ef = ENTRIES / f"14-{int(rid.split('.')[1]):03d}.json"
        if not ef.exists():
            faults.append(f"Rule {rid}: no entry file {ef.relative_to(ROOT)} for a built round")
            continue
        try:
            e = json.loads(ef.read_text())
        except json.JSONDecodeError as ex:
            faults.append(f"Rule {rid}: {ef.name} is not JSON ({ex})")
            continue
        if str(e.get("id")) != rid:
            faults.append(f"Rule {rid}: {ef.name} says id {e.get('id')!r}; the plan fixes {rid}")
        rule = {k: v for k, v in e.items() if k not in ENTRY_DROP}
        rule["id"] = rid
        # BC S18 (ED-E11): the chapter states its basis once; a rule or entry whose basis is that one prints no box of its own
        if chap.get("basis") and isinstance(rule.get("why"), dict) and same_basis(rule["why"].get("basis"), chap["basis"]):
            rule["why"] = {k: v for k, v in rule["why"].items() if k != "basis"}
        # R2 gives "related" as the rule numbers an entry cites; the guide prints related chapters, so the rules' chapters
        # other than 14 go there and the rule numbers stay beside them as "related_rules"
        rel = [str(x) for x in (e.get("related") or [])]
        if any("." in x for x in rel):
            rule["related_rules"] = [x for x in rel if "." in x]
            rule["related"] = sorted({x.split(".")[0].zfill(2) for x in rel if x.split(".")[0].zfill(2) != "14"} | {x for x in rel if "." not in x})
        for ex in e.get("examples") or []:
            log.append(dict(ex, rule=rid, source=ef.name))
        if p["kind"] == "rule":
            for kind in ("correct", "failure"):
                blk = e.get(kind)
                if not blk or not blk.get("specimen"):
                    faults.append(f"Rule {rid}: no {kind} plate (DR-240 gives rules 14.1 to 14.14 both)")
                    continue
                rule[kind] = {"specimen": blk["specimen"], "caption": blk.get("caption", "")}
                manifest[blk["specimen"]] = {"chapter": "14", "rule": rid, "alt": blk.get("alt", ""),
                                             **{k: blk[k] for k in PLATE_META if k in blk}}
                manifest[blk["specimen"]].setdefault("illustrative", False)
                if not (SPECIMENS / f"{blk['specimen']}.html").exists():
                    faults.append(f"Rule {rid}: the {kind} plate {blk['specimen']}.html is not in the specimens folder")
            rules.append(rule)
            continue
        # a form's entry (R2)
        rule["entry"] = True
        rule["use_when"] = e.get("use_when")
        rule["use_instead"] = e.get("use_instead") or []
        if e.get("failure"):
            faults.append(f"Rule {rid}: an entry takes no failure plate (DR-240)")
        if tier_of(e.get("tier")) != tier_of(p["tier"]):
            faults.append(f"Rule {rid}: tier {e.get('tier')!r}; the plan sets {p['tier']!r}")
        want = p.get("spec_id") or p.get("sketch_id")
        if e.get("specimen") != want:
            faults.append(f"Rule {rid}: specimen {e.get('specimen')!r}; the plan sets {want!r}")
        for u in rule["use_instead"]:
            if str(u.get("rule")).startswith("14.") and str(u.get("rule")) not in planned:
                faults.append(f"Rule {rid}: use_instead names Rule {u.get('rule')}, which the plan does not hold")
        # a plate's caption until the editor's words pass gives its own: the reader's question the specimen answers
        # the entry's own caption first (the makers' and editor's words), else the plan's question, curled (ED-E5)
        cap = e.get("caption") or curly(p.get("reader_question") or f"{p['form']}.")
        if p.get("spec_id"):
            sid = p["spec_id"].lower()
            sp = SPECS / f"{sid}.json"
            if not sp.exists():
                # round 2: an entry whose spec has not landed stays out of the chapter, among the planned numbers, so the
                # chapter carries every finished entry while its round is built (a fault all the same)
                faults.append(f"Rule {rid}: no spec {sp.relative_to(ROOT)}")
                continue
            spec = json.loads(sp.read_text())
            if sid in placed_spec:
                rule["specimen_at"] = placed_spec[sid]
                rules.append(rule)
                continue
            placed_spec[sid] = rid
            frag = f"s-14-{sid}"
            fragments[frag] = f'<div data-oa-chart="{frag}"></div>\n'
            rule["correct"] = {"specimen": frag, "caption": cap}
            manifest[frag] = {"chapter": "14", "rule": rid, "width_px": None, "alt": spec.get("alt", ""),
                              "illustrative": bool(spec.get("illustrative")),
                              "notes": f"{p['spec_id']}, {p['form_id']}: the chart kit draws it from {sp.relative_to(ROOT)} (contract R1-C3)"}
            if spec.get("lookup"):
                manifest[frag]["interactive"] = True   # access S3: a lookup is a control besides the table's disclosure
            log.append({"example": spec.get("title", p["spec_id"]), "domain": spec.get("domain"), "states": spec.get("states") or [],
                        "rule": rid, "source": f"{sid}.json"})
        else:
            sk = p["sketch_id"]
            if not (SPECIMENS / f"{sk}.html").exists():
                faults.append(f"Rule {rid}: the sketch {sk}.html is not in the specimens folder")
                continue   # as a missing spec: the entry waits among the planned numbers
            # R-B12: an avoid sketch's plate names the form as misleading and carries the do-not-publish bar; a reference
            # sketch's plate reads as a sketch
            avoid = tier_of(p["tier"]) == "avoid"
            # R2-3 (RS-S2, contract R2-C3): the visible caption is the first sentence of the entry's sketch_alt, and the
            # sketch's first <desc> carries the same sentence; round 1's sketches without sketch_alt take their first
            # <desc>'s first sentence, and the <desc> test starts with round 2's sketches
            descs = [unescape(d) for d in DESC.findall((SPECIMENS / f"{sk}.html").read_text())]
            cap1 = first_sentence(e.get("sketch_alt")) if e.get("sketch_alt") else (first_sentence(descs[0]) if descs else "")
            if p.get("round", 1) >= 2:
                if not e.get("sketch_alt"):
                    faults.append(f"Rule {rid}: a sketch entry carries sketch_alt, whose first sentence prints as its caption (R2-3)")
                elif not descs or first_sentence(descs[0]) != cap1:
                    faults.append(f"Rule {rid}: {sk}.html's first <desc> does not hold sketch_alt's first sentence, \"{cap1}\" (R2-3)")
            rule["correct"] = {"specimen": sk, "caption": cap1 or f"{p['form']}, drawn small with illustrative data.",
                               "kind": "avoid" if avoid else "sketch",
                               "label": f"{p['form']}, a form that misleads" if avoid else f"{p['form']}, a sketch"}
            limit = SKETCH_LIMIT.get(tier_of(p["tier"]), 4096)
            # CD SK-M2, BC S7: one drawing sets its stage at the drawing's true width, so the frame centers it and the
            # do-not-publish bar takes its width; an avoid entry's pair (D3-486) flows, each half at its own width, side by
            # side where the frame holds both and one over the other where it does not
            ws = sketch_widths(SPECIMENS / f"{sk}.html")
            manifest[sk] = {"chapter": "14", "rule": rid, "width_px": ws[0] if len(ws) == 1 else None, "illustrative": True,
                            "alt": e.get("sketch_alt") or f"A sketch of a {p['form'].lower()}, with illustrative data.",
                            "notes": f"{tier_of(p['tier'])} sketch, at most {limit:,} bytes (contract R1-C1, D3-486)"}
            if len(ws) == 1:
                manifest[sk]["fit_switch"] = False
            if len(ws) > 2 or (len(ws) == 2 and not avoid):
                faults.append(f"Rule {rid}: {sk}.html holds {len(ws)} drawings; a sketch holds one, or an avoid entry's pair (D3-486)")
            if (SPECIMENS / f"{sk}.html").exists() and (SPECIMENS / f"{sk}.html").stat().st_size > limit:
                faults.append(f"Rule {rid}: {sk}.html weighs {(SPECIMENS / f'{sk}.html').stat().st_size:,} bytes, over its {limit:,} (R1-C1)")
        rules.append(rule)
    # the groups whose first rule is built
    ids = [r["id"] for r in rules]
    groups = [g for g in chap.get("groups") or [] if str(g.get("before_rule")) in ids]
    chapter = {k: chap[k] for k in ("number", "anchor", "title", "part", "instruction", "basis", "plate_css") if k in chap}
    if opener.get("specimen"):
        chapter["opener"] = {"specimen": opener["specimen"], "caption": opener.get("caption", "")}
    chapter.update({"intro": chap.get("intro") or [], "groups": groups, "rules": rules,
                    "related_chapters": chap.get("related_chapters") or [], "sources": chap.get("sources") or [],
                    "planned_rules": [x for x in planned if x not in ids]})
    # Rule 01.12's log, against DR-229's shares (an atlas-wide table, domain "all", is counted apart)
    n = len(log)
    doms = Counter(x.get("domain") for x in log if x.get("domain") and x.get("domain") != "all")
    sts = Counter(s for x in log for s in (x.get("states") or []))
    for d, k in doms.items():
        if k > n * DOMAIN_SHARE:
            faults.append(f"Rule 01.9: domain {d} supplies {k} of chapter 14's {n} examples, over one in four (DR-229)")
    for s, k in sts.items():
        if k > n * STATE_SHARE:
            faults.append(f"Rule 01.9: {s} supplies {k} of chapter 14's {n} examples, over one in five (DR-229)")
    logdoc = {"chapter": "14", "written_by": "work/build/scripts/phase-3/phase3_ch14_build.py", "rounds": sorted(rounds),
              "examples": n, "by_domain": dict(sorted(doms.items())), "all_domains": sum(1 for x in log if x.get("domain") == "all"),
              "by_state": dict(sorted(sts.items())), "limits": {"domain": "one in four", "state": "one in five"}, "rows": log}
    files = {CHAPTER: json.dumps(chapter, indent=1, ensure_ascii=False) + "\n", MANIFEST: json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
             LOG: json.dumps(logdoc, indent=1, ensure_ascii=False) + "\n"}
    for frag, text in fragments.items():
        files[SPECIMENS / f"{frag}.html"] = text
    return files, faults, {"rules": len(rules), "entries": sum(1 for r in rules if r.get("entry")), "plates": len(fragments),
                           "examples": n, "planned": len(chapter["planned_rules"])}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rounds", default="1,2", help="the rounds built, as a comma list (default 1,2: round 2 is being built)")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    rounds = {int(x) for x in a.rounds.split(",")}
    files, faults, counts = outputs(rounds)
    stale = [p for p, t in files.items() if not p.exists() or p.read_text() != t]
    if a.check:
        for p in stale:
            print(f"phase3_ch14_build --check: {p.relative_to(ROOT)} is not what the script writes")
        print(f"phase3_ch14_build --check: {len(files) - len(stale)} of {len(files)} files current")
        return 1 if stale else 0
    for p in stale:
        p.write_text(files[p])
    for f in faults:
        print(f"  fault: {f}")
    print(f"phase3_ch14_build: {counts['rules']} rules ({counts['entries']} entries, {counts['plates']} chart plates), "
          f"{counts['examples']} examples logged, {counts['planned']} numbers planned for later rounds; {len(files)} files, {len(stale)} written; "
          f"{len(faults)} fault(s)")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
