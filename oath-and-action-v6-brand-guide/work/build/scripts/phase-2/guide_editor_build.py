"""Write the editor's chapters for stage board A: 01 Purpose and 02 Voice.

Usage:
    python3 -I work/build/scripts/phase-2/guide_editor_build.py

Writes:
    work/build/guide/chapters/01-purpose.json and 02-voice.json
    work/build/guide/specimens/s-01-*.html, s-02-*.html and manifest-editor.json

Then runs the editor's own checks and stops on any failure: locked lines character for character, no em dash
character anywhere (W21's is drawn as a rule, DR-79), no bare decision or record code in reader-facing text (H11),
no listed filler or corporate word outside the rules that name them, every Illustrative-flagged specimen labeled,
the writing section carried whole (every W rule's name, rule, before, after, terms and why, every house rule and the
checklist found in the output), font sizes in specimen CSS at 13 px or larger, and token names known to tokens.json.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import guide_editor_ch01 as ch01  # noqa: E402
import guide_editor_ch02 as ch02  # noqa: E402
from guide_editor_common import (ALLOWED_REM, LOCKED, ROOT, VOICE_CONTENT, VOICE_LINE_B, Book, curl, load,  # noqa: E402
                                 plain, write_chapter)

FILLERS = ["genuinely", "really", "truly", "actually", "simply", "leverage", "underscore", "reflect"]


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def visible(html):
    t = re.sub(r"<style\b.*?</style>", " ", html, flags=re.S)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"</?(del|ins|span|b|a|strong|em|sup)\b[^>]*>", "", t)
    t = re.sub(r"<[^>]+>", " ", t)
    import html as h
    return " ".join(h.unescape(t).split())


def tokens_known():
    tj = ROOT / "work/build/tokens/tokens.json"
    names = set()

    def walk(o, path):
        if isinstance(o, dict):
            if "$value" in o:
                names.add(".".join(path))
                return
            for k, v in o.items():
                if not k.startswith("$"):
                    walk(v, path + [k])
    if tj.exists():
        walk(json.loads(tj.read_text()), [])
    return names


def check(chapters, book, house):
    fails, notes = [], []
    texts = {}
    for c in chapters:
        texts[f"chapter {c['number']}"] = " ".join(strings({k: v for k, v in c.items() if k != "extras"})) + " " + " ".join(
            str(x.get("caption", "")) + " " + str(x.get("label", "")) for x in c.get("extras", []))
    for sid, html in book.files.items():
        texts[sid] = visible(html)
    for sid, m in book.manifest.items():
        texts[sid + " alt"] = m["alt"]
    allt = " ".join(texts.values())

    # 1. em dash: none at all, anywhere (W21's is drawn)
    for k, t in texts.items():
        if "—" in t:
            fails.append(f"em dash in {k}")
    for sid, html in book.files.items():
        if "—" in html:
            fails.append(f"em dash character in the source of {sid}")
    if 'aria-label="em dash"' not in book.files.get("s-02-21-pair", ""):
        fails.append("W21's pair does not draw the em dash as a labeled rule")

    # 2. locked lines exact, and no near miss (a long prefix of a line followed by other words)
    for name, line in LOCKED.items():
        n = allt.count(line)
        notes.append(f"locked line {name}: {n} exact uses")
        head = line[: max(18, len(line) // 2)]
        for m in re.finditer(re.escape(head), allt):
            frag = allt[m.start(): m.start() + len(line)]
            if frag != line:
                fails.append(f"near miss of the {name}: {frag!r}")
    for k, t in texts.items():
        if "Explain" in t and "Connect" in t:
            for m in re.finditer(r"Explain\W{1,4}Track\W{1,4}Connect\W{1,4}Act", t):
                pass
            order = [t.find(p) for p in ("Explain → Track → Connect → Act",)]
    if allt.count(VOICE_LINE_B) < 2:
        fails.append("voice line B is not quoted exactly in the lines table and in W13")

    # 3. bare record codes (H11): decision and question codes never print in reader-facing text
    for k, t in texts.items():
        for m in re.finditer(r"\b(DR|D[012]|G1|DC|Q|C|S|I|Y|M|T|NP)-\d{1,3}\b", t):
            fails.append(f"bare record code {m.group(0)} in {k}")
        for m in re.finditer(r"(?<![\w-])(?<!Loop )(?<!Rule )\b(V7|V5|V4\.2|R9|R13|I6|I8|S5|S9)\b", t):
            fails.append(f"internal code {m.group(0)} in {k}")
        # D2-253: studio words never reach a reader
        for m in re.finditer(r"Master Brief|\bPhase \d|\bPhase\b|\bGate \d|\bGate\b|Board 5|stage board|the studio|Atlas V7|later stage", t):
            fails.append(f"studio word {m.group(0)!r} in {k}")

    # 4. fillers and corporate words, outside the rules and sheets that name them as the words to cut
    allowed = {"s-02-17-pair", "s-02-17-fault", "s-02-18-pair", "s-02-18-fault", "s-02-26-correct", "s-02-26-failure",
               "s-02-26-correct alt", "s-02-26-failure alt", "s-02-17-pair alt", "s-02-17-fault alt", "s-02-18-pair alt", "s-02-18-fault alt"}
    for k, t in texts.items():
        if k in allowed:
            continue
        for w in FILLERS:
            for m in re.finditer(rf"\b{w}\b", t, re.I):
                ctx = t[max(0, m.start() - 60): m.end() + 40]
                if t[max(0, m.start() - 1):m.start()] == "“" or t[m.end():m.end() + 1] in ("”",):
                    continue
                if k.startswith("chapter 02") and ("W17" in ctx or "W18" in ctx or "Search for" in ctx or "such as" in ctx or "Write “use”" in ctx or "for leverage" in ctx):
                    continue
                fails.append(f"listed word {w!r} in {k}: …{ctx}…")

    # 5. Illustrative label beside the item in every flagged specimen
    for sid, m in book.manifest.items():
        if m["illustrative"] and "Illustrative" not in book.files[sid] and "illustrative" not in m["alt"].lower():
            fails.append(f"{sid} is flagged illustrative but carries no label")

    # 6. the writing section carried whole
    C = load(VOICE_CONTENT)
    blob = allt
    for g in C["groups"]:
        for need in (g["name"], g["intro"]):
            if curl(need) not in blob:
                fails.append(f"group text missing: {need[:60]}")
        for r in g["rules"]:
            for key in ("name", "rule", "terms", "why", "before_source"):
                v = curl(r.get(key) or "")
                if v and v not in blob:
                    fails.append(f"{r['id']} {key} missing from the output")
            for key in ("before", "after"):
                v = re.sub(r"\s+", " ", plain(r[key])).replace("—", "")
                v = " ".join(v.split())
                if v not in blob.replace("  ", " "):
                    # the before's em dash is drawn, so compare with it removed
                    b2 = " ".join(blob.split())
                    if v.replace(" .", ".") not in b2 and v not in b2:
                        fails.append(f"{r['id']} {key} missing from the output")
            if r.get("source_line") and r["source_line"] not in blob:
                fails.append(f"{r['id']} source line missing")
    for h in house:
        for key in ("name", "rule", "example_source", "example_before_source"):
            v = curl(h.get(key) or "")
            if v and v not in blob:
                fails.append(f"{h['id']} {key} missing")
        for key in ("example", "example_before"):
            if h.get(key):
                v = plain(h[key]).replace(" Illustrative", "")
                if v not in blob:
                    fails.append(f"{h['id']} {key} missing")
        for gr in h.get("grades") or []:
            for v in gr.values():
                if curl(v) not in blob:
                    fails.append(f"{h['id']} grade text missing: {v}")
    for qq in C["checklist"]:
        if curl(qq) not in blob:
            fails.append(f"checklist question missing: {qq[:50]}")
    for k in ("title", "deck", "scope", "sources_note"):
        if curl(C[k]) not in blob:
            fails.append(f"writing section {k} missing")
    for p in C["narrative"]:
        if curl(p) not in blob:
            fails.append(f"narrative paragraph missing: {p[:50]}")
    retired = ["Know the rules. Find the lever.", "Institutions endure when people act.", "The fine print affects the big picture.", "Bring your questions. They belong here."]
    for line in retired[1:]:
        for k, t in texts.items():
            if line in t and k not in ("s-02-lines", "s-02-lines alt"):
                fails.append(f"retired line {line!r} outside the labeled record, in {k}")

    # 7. specimen CSS: font sizes at 13 px or more; colors only through var(--oa-...)
    for sid, html in book.files.items():
        for m in re.finditer(r"font-size\s*:\s*([\d.]+)(px|rem|em)", html):
            v = float(m.group(1)) * (16 if m.group(2) in ("rem", "em") else 1)
            if v < 13 and m.group(2) != "em":
                fails.append(f"{sid}: font-size {m.group(0)} under 13 px")
        for m in re.finditer(r'font-size="([\d.]+)"', html):
            if float(m.group(1)) < 13:
                fails.append(f"{sid}: SVG text at {m.group(1)}")
        bare = re.sub(r"var\((?:[^()]|\([^()]*\))*\)", "", html)
        bare = re.sub(r'\sd="[^"]*"', "", bare)
        if re.search(r"(?<![\w&])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![\w-])|\brgba?\(", bare):
            fails.append(f"{sid}: a literal color")
        if re.search(r"<h[1-6]\b", html):
            fails.append(f"{sid}: a heading element")
        if re.search(r"<(nav|article|header|footer|main|aside|section|form)\b|role=\"(navigation|main|banner|contentinfo|region|complementary|article)\"", html):
            fails.append(f"{sid}: a landmark or article element (AX-S8)")
        for m in re.finditer(r"font(?:-size)?\s*:[^;}]*?([\d.]+)rem", html):
            if float(m.group(1)) not in ALLOWED_REM:
                fails.append(f"{sid}: a font size of {m.group(1)}rem, off the D2-254 scale")
        if re.search(r"font(?:-size)?\s*:[^;}]*clamp\(", html):
            fails.append(f"{sid}: a fluid font size written by hand")
        if re.search(r"class=\"ill\"|\.ill\b", html):
            fails.append(f"{sid}: an Illustrative label in a form other than the shell's (DR-97)")

    # 8. tokens named in the chapters exist
    known = tokens_known()
    if known:
        for c in chapters:
            for r in c["rules"]:
                for t in (r.get("tokens") or []) + [s.get("token") for s in r.get("specs") or [] if s.get("token")]:
                    if t not in known:
                        fails.append(f"Rule {r['id']}: token {t} not in tokens.json")
    else:
        notes.append("tokens.json not found; token names unchecked")

    # 9. files named exist; every specimen placed once
    placed = []
    for c in chapters:
        for r in c["rules"]:
            for f in r.get("files") or []:
                if not (ROOT / f).exists():
                    fails.append(f"Rule {r['id']}: file {f} not found")
            for k in ("correct", "failure", "corrective"):
                if r.get(k):
                    placed.append(r[k]["specimen"])
        placed += [x["specimen"] for x in c.get("extras", [])]
    for sid in book.files:
        if placed.count(sid) != 1:
            fails.append(f"{sid} is placed {placed.count(sid)} times")

    # 10. chapter 01's own rotation (Rule 01.9)
    n, dom, st = ch01.tally()
    if max(dom.values()) > n / 4:
        fails.append(f"chapter 01 breaks its own Rule 01.9: {dom.most_common(1)} of {n}")
    notes.append(f"chapter 01 rotation: {n} examples, top domain {dom.most_common(1)[0]}")
    return fails, notes


def main():
    book = Book("editor")
    c1 = ch01.build(book)
    c2, house = ch02.build(book)
    fails, notes = check([c1, c2], book, house)
    for n in notes:
        print("note:", n)
    if fails:
        for f in fails:
            print("FAIL:", f)
        print(f"{len(fails)} check(s) failed; nothing written")
        sys.exit(1)
    p1 = write_chapter(c1)
    p2 = write_chapter(c2)
    book.write()
    print("wrote", p1.relative_to(ROOT), p2.relative_to(ROOT), f"and {len(book.files)} specimens with manifest-editor.json")
    print(f"chapter 01: {len(c1['rules'])} rules, {len(c1['extras'])} extras; chapter 02: {len(c2['rules'])} rules, {len(c2['extras'])} extras")


if __name__ == "__main__":
    main()
