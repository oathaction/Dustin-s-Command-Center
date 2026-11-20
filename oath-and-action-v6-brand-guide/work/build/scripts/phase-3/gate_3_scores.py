"""Gate 3: the creative director's last score for every Phase 3 item, read from the score files in order.

Run from oath-and-action-v6-brand-guide/: python3 -I work/build/scripts/phase-3/gate_3_scores.py [--out JSON]
A later file's score for an item replaces an earlier one; boards are read apart from items.
"""
import json, os, sys, argparse

H = "work/handoffs/phase-3/"
ITEM_FILES = [  # in time order; each later file's scores replace the earlier ones for the same key
    ("Round 0", "20261111_Round-0-CD-Scores.json"), ("Round 0", "20261112_Round-0-CD-Rescores.json"),
    ("Round 1", "20261112_Round-1-CD-Scores.json"), ("Round 1", "20261112_Round-1-CD-Rescores.json"),
    ("Round 2", "20261112_Round-2-CD-Scores.json"), ("Round 2", "20261112_Round-2-CD-Rescores.json"),
    ("Round 3", "20261113_Round-3-CD-Scores.json"), ("Round 3", "20261113_Round-3-CD-Rescores.json"),
    ("Rounds 4 and 5", "20261116_Rounds-4-5-CD-Scores.json"), ("Rounds 4 and 5", "20261116_Rounds-4-5-CD-Rescores.json"),
    ("Rounds 4 and 5", "20261120_Second-Pass-CD-Rescores.json"), ("Rounds 4 and 5", "20261120_Apply-Pass-CD-Rescores.json"),
]
BOARD_FILES = ["20261113_Board-2-CD-Scores.json", "20261113_Board-2-CD-Rescores.json",
               "20261120_Board-3-CD-Scores.json", "20261121_Gate-3-Board-CD-Scores.json", "20261120_Gate-3-Board-CD-Scores.json"]
CRIT = ["craft", "clarity", "brand_fidelity", "usefulness", "evidence_honesty", "accessibility"]


def items_of(d):
    return d.get("items") if isinstance(d, dict) else d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    last, seen = {}, []
    for rnd, f in ITEM_FILES:
        p = H + f
        if not os.path.exists(p):
            continue
        seen.append(f)
        for it in items_of(json.load(open(p))) or []:
            s = it.get("scores")
            if not s:
                continue
            r = it.get("round", rnd)  # the apply pass rescore names each item's round
            k = (r, it["key"])
            last[k] = {"round": r, "key": it["key"], "name": it.get("name", ""), "file": f,
                       "scores": {c: s.get(c) for c in CRIT}, "min": min(v for v in s.values() if isinstance(v, int))}
    boards = []
    for f in BOARD_FILES:
        p = H + f
        if os.path.exists(p):
            for it in items_of(json.load(open(p))) or []:
                s = it.get("scores")
                boards.append({"file": f, "key": it["key"], "scores": {c: s.get(c) for c in CRIT} if s else None})
    rows = list(last.values())
    out = {"files_read": seen, "items": rows, "boards": boards,
           "items_count": len(rows), "items_at_4_or_more": sum(r["min"] >= 4 for r in rows)}
    for r in rows:
        print(f'{r["round"]:15} {r["key"]:14} min {r["min"]}  ' + " ".join(str(r["scores"][c]) for c in CRIT) + f'  {r["file"]}')
    print(f'{out["items_at_4_or_more"]} of {out["items_count"]} items at 4 or more on all six')
    for b in boards:
        print("board", b["file"], b["key"], b["scores"])
    if a.out:
        json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
