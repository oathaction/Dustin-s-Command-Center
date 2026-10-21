"""Editor, Phase 1: count writing-rule patterns and term variants in review texts.

Takes text files (board text extracted by editor_board_text.py, or Markdown
handoffs) and prints every hit with its line, grouped by check.

Run: python3 -I work/build/scripts/phase-1/editor_pattern_check.py <file> [<file> ...]
"""
import re
import sys
from pathlib import Path

CHECKS = {
    "em dash": r"—",
    "en dash": r"–",
    "filler": r"\b(genuinely|really|truly|actually|very|simply|just|quite|incredibly)\b",
    "corporate verb": r"\b(leverag\w*|underscor\w*|reflect\w*|utiliz\w*|facilitat\w*|empower\w*|streamlin\w*|unlock\w*|harness\w*|robust|seamless\w*)\b",
    "hedge": r"\b(perhaps|arguably|somewhat|fairly|rather|likely|probably|might|could be|seems?|appears? to|tends? to|generally)\b",
    "inflated adjective": r"\b(powerful|bold|iconic|transformative|world-class|cutting-edge|crucial|vital|essential|critical|key|unique|significant|deserves)\b",
    "corrective negation": r"\b(not|never|no)\b[^.;:]{0,40}\b(but|it is|it's)\b|,\s*not\s+\w+",
    "British spelling": r"\b(colour\w*|favour\w*|neighbour\w*|behaviour\w*|centr(e|es|ing)|organis\w*|analys(e|ed|ing)|totall(ed|ing)|labell(ed|ing)|modell(ed|ing)|grey|licence|programme|catalogue)\b",
    "locked tagline variant": r"answers to (its|the) people|A country that answers",
    "locked mission variant": r"rules that shape",
    "locked promise variant": r"practical way to take part",
    "locked commitment variant": r"Clarity is our duty|Action is our promise",
    "grade word: well-supported": r"[Ww]ell-supported",
    "grade word: well supported": r"[Ww]ell supported",
    "term: lever": r"\blever\b",
    "term: hinge": r"\bhinge\b",
    "term: lockmark": r"\block[- ]?mark\b",
    "term: Signal Grid": r"\b[Ss]ignal [Gg]rid\b",
    "chapter ref": r"\b(chapter|Chapter)s? \d{2}\b|\b\d{2} [A-Z][a-z]+ (and|chapter)",
}


def main():
    for f in sys.argv[1:]:
        text = Path(f).read_text(encoding="utf-8").splitlines()
        print(f"==== {f}")
        for name, pat in CHECKS.items():
            hits = [(i, l) for i, l in enumerate(text, 1) if re.search(pat, l)]
            if not hits:
                continue
            print(f"-- {name}: {len(hits)}")
            if name.startswith(("term:", "locked", "chapter")):
                continue
            for i, l in hits[:40]:
                m = re.search(pat, l)
                s = max(0, m.start() - 70)
                print(f"   {i}: ...{l[s:m.end() + 70]}...")


if __name__ == "__main__":
    main()
