"""Phase 0 editor audit scan of V5 Polished chapter extracts.

Reads work/extract/v5-polished/chapters/*.html (visible text plus aria-label,
alt and title attributes) and reports:
  1. every occurrence of the locked lines and pillar sequences, exact or deviating
  2. counts of scriptable voice patterns, with examples
  3. first use of listed terms by chapter

Usage: python3 -I editor_audit_scan.py <project-root> <output.json>
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
CH = ROOT / "work/extract/v5-polished/chapters"

LOCKED = {
    "tagline": "A country that answers to its people.",
    "mission": "Help people understand and improve the rules that shape their lives.",
    "reader_promise": "We explain how a decision is made and give you a practical way to take part.",
    "editorial_commitment": "Clarity is our duty. Action is our promise.",
}
# fragments that catch a deviating version of each line
FRAGMENTS = {
    "tagline": [r"answers? to (its|the|our) people", r"country that answers"],
    "mission": [r"rules that shape (their|our|your) lives", r"understand and improve"],
    "reader_promise": [r"how a decision is made", r"practical way to take part"],
    "editorial_commitment": [r"clarity is our", r"action is our promise"],
}
PILLARS = ["Explain", "Track", "Connect", "Act"]


class Collector(HTMLParser):
    """Collects visible text, and attribute text separately."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.attrs = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self.skip += 1
        for k, v in attrs:
            if k in ("aria-label", "alt", "title") and v:
                self.attrs.append((tag, k, v))
        if tag in ("br", "p", "div", "li", "h1", "h2", "h3", "h4", "td", "th", "tr", "figcaption", "span", "b", "strong"):
            self.text.append(" ")

    def handle_endtag(self, tag):
        if tag in ("style", "script") and self.skip:
            self.skip -= 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "td", "th", "figcaption"):
            self.text.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


def norm(s):
    s = s.replace("’", "'").replace(" ", " ")
    return re.sub(r"[ \t\r\f\v]+", " ", s)


def flat(s):
    return re.sub(r"\s+", " ", norm(s)).strip()


def context(s, i, j, pad=70):
    return flat(s[max(0, i - pad): j + pad])


chapters = {}
for p in sorted(CH.glob("*.html")):
    c = Collector()
    c.feed(p.read_text(encoding="utf-8", errors="replace"))
    chapters[p.stem] = {"text": norm("".join(c.text)), "attrs": c.attrs}

report = {"locked": [], "pillar_sequences": [], "patterns": {}, "terms": {}}

# 1. locked lines
for ch, d in chapters.items():
    sources = [("text", flat(d["text"]))] + [(f"attr:{t}.{k}", flat(v)) for t, k, v in d["attrs"]]
    for where, s in sources:
        for key, frags in FRAGMENTS.items():
            seen = set()
            for fr in frags:
                for m in re.finditer(fr, s, re.I):
                    # widen to the sentence (or two sentences for the commitment)
                    start = max(s.rfind(". ", 0, m.start()), s.rfind("\n", 0, m.start()))
                    start = 0 if start < 0 else start + 1
                    if key == "editorial_commitment":
                        start = max(0, s.lower().rfind("clarity", 0, m.end()))
                    end = s.find(".", m.end())
                    if key == "editorial_commitment" and "clarity" in s[start:m.end()].lower():
                        end = s.lower().find("promise", m.end() - 7)
                        end = s.find(".", end) if end >= 0 else -1
                    end = len(s) if end < 0 else end + 1
                    span = (start, end)
                    if any(abs(span[0] - a) < 5 for a, _ in seen):
                        continue
                    seen.add(span)
                    found = s[start:end].strip()
                    exact = LOCKED[key] in found
                    report["locked"].append({
                        "chapter": ch, "where": where, "line": key,
                        "exact": exact, "found": found[:220],
                    })

# pillar sequences: any run naming all four pillars within a short window
pat = re.compile(r"\b(Explain|Track|Connect|Act)\b")
for ch, d in chapters.items():
    for where, s in [("text", flat(d["text"]))] + [(f"attr:{t}.{k}", flat(v)) for t, k, v in d["attrs"]]:
        hits = [(m.start(), m.group(1)) for m in pat.finditer(s)]
        i = 0
        while i < len(hits):
            run = [hits[i]]
            j = i + 1
            while j < len(hits) and hits[j][0] - run[-1][0] < 140 and len(run) < 4:
                run.append(hits[j])
                j += 1
            names = [n for _, n in run]
            if len(run) == 4 and set(names) == set(PILLARS):
                report["pillar_sequences"].append({
                    "chapter": ch, "where": where,
                    "order": names, "in_order": names == PILLARS,
                    "context": context(s, run[0][0], run[-1][0] + 8, 30)[:200],
                })
                i = j
            else:
                i += 1

# 2. scriptable patterns over visible text only
alltext = {ch: flat(d["text"]) for ch, d in chapters.items()}
PATTERNS = {
    "em_dash": r"—",
    "en_dash": r"–",
    "filler_intensifier": r"\b(genuinely|really|truly|actually|simply|very|just|quite)\b",
    "corporate_verb": r"\b(leverag\w*|underscor\w*|reflect\w*|utiliz\w*|facilitat\w*|empower\w*|ensur\w*|enabl\w*)\b",
    "hedge": r"\b(usually|often|generally|approximately|roughly|about \d|at least about|somewhat|relatively|may|might|can be|tends? to|most)\b",
    "corrective_not": r"[,.]\s+(not|never)\s+\w+",
    "x_not_y": r"\b\w+,\s+not\s+\w+",
    "never_statement": r"\bNever\b",
    "inflated_adjective": r"\b(excellent|powerful|seamless|robust|world-class|precise|substantial|deliberate|meaningful|complete|fully|elevated|dependable)\b",
    "nominalization": r"\b[a-z]{4,}(tion|tions|ment|ments|ance|ence|ity|ities)\b",
}
for name, rx in PATTERNS.items():
    total, per, examples = 0, {}, []
    for ch, s in alltext.items():
        ms = list(re.finditer(rx, s))
        if ms:
            per[ch] = len(ms)
            total += len(ms)
            for m in ms[:3]:
                if len(examples) < 12:
                    examples.append(f"{ch}: ...{context(s, m.start(), m.end(), 50)}...")
    report["patterns"][name] = {"total": total, "by_chapter": per, "examples": examples}

# nominalization frequency
freq = {}
for s in alltext.values():
    for m in re.finditer(PATTERNS["nominalization"], s):
        w = m.group(0).lower()
        freq[w] = freq.get(w, 0) + 1
report["patterns"]["nominalization"]["top"] = sorted(freq.items(), key=lambda x: -x[1])[:40]

# parallel sentence runs: three or more consecutive sentences opening with the same word
runs = []
for ch, s in alltext.items():
    sents = re.split(r"(?<=[.!?])\s+", s)
    k = 0
    while k < len(sents):
        w = sents[k].split(" ")[0] if sents[k] else ""
        j = k + 1
        while j < len(sents) and sents[j].split(" ")[0] == w and w:
            j += 1
        if j - k >= 3 and w not in ("[svg]",):
            runs.append(f"{ch}: " + " ".join(sents[k:j])[:220])
        k = j
report["patterns"]["parallel_runs_same_opening_word"] = {"total": len(runs), "examples": runs}

# triplets: "A, B and C" or "A, B, and C" lists
trip = []
for ch, s in alltext.items():
    for m in re.finditer(r"\b[\w'-]+(?: [\w'-]+){0,2}, [\w'-]+(?: [\w'-]+){0,2},? (and|or) [\w'-]+(?: [\w'-]+){0,2}", s):
        trip.append(f"{ch}: {m.group(0)}")
report["patterns"]["three_item_lists"] = {"total": len(trip), "examples": trip[:60]}

# 3. terms: first chapter and context
TERMS = ["Signal Grid", "lockmark", "lever", "hinge", "container mark", "stock", "flow",
         "polarity", "mechanism grid", "kicker", "keyline", "beat", "Act context", "optical master",
         "lit node", "route", "loop", "variable", "delay", "evidence grade", "sign", "the move",
         "the gap", "cap height", "overshoot", "measure", "monogram", "lockup", "counter",
         "unenrolled", "cloture", "reported out", "reconciled", "RCV", "M.G.L.", "PDF/A", "WCAG",
         "ampersand moment", "Authority", "intervention", "target bracket", "watermark", "hairline",
         "series path", "content type", "safe zone", "duotone", "beat", "x is the cap height", "1.0x"]
for t in TERMS:
    rx = re.compile(r"\b" + re.escape(t) + r"\w*", re.I if t[0].islower() else 0)
    for ch, s in alltext.items():
        m = rx.search(s)
        if m:
            n = sum(len(rx.findall(x)) for x in alltext.values())
            report["terms"][t] = {"first_chapter": ch, "uses": n,
                                  "context": context(s, m.start(), m.end(), 90)}
            break

OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
print("locked occurrences:", len(report["locked"]),
      "exact:", sum(1 for x in report["locked"] if x["exact"]))
print("pillar sequences:", len(report["pillar_sequences"]),
      "in order:", sum(1 for x in report["pillar_sequences"] if x["in_order"]))
for k, v in report["patterns"].items():
    print(k, v["total"])
