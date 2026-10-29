"""Write qa/<date>_Civic-Line-Fidelity-Metrics.csv: one row per icon.

    python3 -I write_fidelity.py

Metrics come from qa/metrics/<ID>.json (refreshed by every build); builds,
state and tracer come from the status files, which this script only reads.
Edge distances are in source px. The bake check at 4x is the main bake
number; the 1x number is kept beside it.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402

OUT = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Fidelity-Metrics.csv")
FIELDS = ["id", "label", "sheet", "row", "column", "silhouette_iou", "red_iou", "edge_mean_px", "edge_p95_px", "edge_max_px",
          "ink_ratio", "bake_iou_4x", "bake_iou_1x", "builds", "state", "tracer"]


def main():
    rows = C.load_inventory()["icons"]
    n = 0
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(FIELDS)
        for r in rows:
            i = r["id"]
            m = C.read_json(os.path.join(C.QA, "metrics", f"{i}.json")) or {}
            st = C.read_json(os.path.join(C.QA, "status", f"{i}.json")) or {}
            has_src = os.path.exists(os.path.join(C.SRC, f"{i}.svg"))
            e = ((m.get("edge_distance_px") or {}).get("symmetric")) or {}
            w.writerow([i, r["label"], r["sheet"], r["row"], r["column"],
                        m.get("silhouette_iou_1x", ""), m.get("red_iou_1x", ""), e.get("mean", ""), e.get("p95", ""), e.get("max", ""),
                        m.get("ink_area_ratio_trace_over_reference", ""), m.get("bake_check_iou_4x", ""), m.get("bake_check_iou_1x", ""),
                        st.get("iterations", 0) if has_src else 0, (st.get("state") or "traced") if has_src else "todo",
                        st.get("tracer", "") if has_src else ""])
            n += 1
    print(f"wrote {os.path.relpath(OUT, C.ROOT)}: {n} rows")


if __name__ == "__main__":
    main()
