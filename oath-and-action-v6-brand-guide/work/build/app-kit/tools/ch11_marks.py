"""Print chapter 11's tracker marks for the application kit, drawn by chapter 11's own code (apply_systems_ch11.py, read
and never edited), so a web page's tracker draws Rules 11.2, 11.4, 11.5 and 11.6 exactly as the guide's chapter 11 does
and the kit keeps no copy of the drawing (chat 11, DD-6).

Usage: python3 -I work/build/app-kit/tools/ch11_marks.py REQUESTS.json
REQUESTS: [{"kind": "row", "states": [...], "W": 324, "d": 24}, {"kind": "mark", "state": "take", "d": 28, "num": 3}]
States are chapter 11's: done, now, take (now with the take-part mark), notyet, skipped (never happened), stopped.
Prints JSON: {"css": MARK_CSS, "words": STATE_WORD, "svgs": [...]}: a row is steps_svg(..., hang=True), the first
circle on the text edge and the last on the far edge (Rule 11.5's card); a mark is sample(), one step centered in a
square 14 px wider than its circle, which leaves room for the take-part disc (Rule 11.6's upright steps).
"""
import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PH2 = ROOT / "work/build/scripts/phase-2"


def load():
    sys.path.insert(0, str(PH2))
    spec = importlib.util.spec_from_file_location("apply_systems_ch11", PH2 / "apply_systems_ch11.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["apply_systems_ch11"] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def main(path):
    m = load()
    reqs = json.loads(Path(path).read_text())
    out = []
    for r in reqs:
        if r["kind"] == "row":
            out.append(m.steps_svg(r["states"], r["W"], r["d"], hang=True))
        elif r["kind"] == "mark":
            out.append(m.sample(r["state"], r["d"], num=r["num"]))
        else:
            raise ValueError(r["kind"])
    print(json.dumps({"css": m.MARK_CSS, "words": m.STATE_WORD, "svgs": out}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
