"""Rebuild every Civic Line icon that has a source in src/.

    python3 -I build_all.py [--chunk 30]

Builds in chunks (one Chromium launch per chunk). A whole-set rebuild refreshes
exports, QA images, metrics and status without counting a tracer iteration.
Icons without a source stay 'todo'. Exit code 1 if any source fails validation.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
from build_icon import build  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk", type=int, default=30)
    a = ap.parse_args()
    order = [r["id"] for r in C.load_inventory()["icons"]]
    ids = [i for i in order if os.path.exists(os.path.join(C.SRC, f"{i}.svg"))]
    stray = sorted(f for f in os.listdir(C.SRC) if f.endswith(".svg") and f[:-4] not in order)
    print(f"{len(ids)} of {len(order)} icons have a source; {len(order) - len(ids)} remain todo")
    if stray:
        print(f"ignored, not in the inventory: {', '.join(stray)}")
    failed = {}
    done = 0
    for k in range(0, len(ids), a.chunk):
        res, fail = build(ids[k:k + a.chunk], rebuild=True)
        failed.update(fail)
        done += len(res)
        for i, s in res.items():
            print(f"{i}: IoU {s['silhouette_iou_1x']:.3f}  red {s['red_iou_1x']:.3f}  edge mean {s['edge_mean_px']:.2f} px  "
                  f"p95 {s['edge_p95_px']:.2f} px  bake {s['bake_check_iou_1x']:.4f}")
    print(f"built {done}, failed {len(failed)}")
    for i, m in failed.items():
        print(f"FAILED {m}", file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
