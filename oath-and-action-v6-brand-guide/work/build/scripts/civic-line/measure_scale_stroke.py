"""Step 2: one line weight W and one scale s for the whole Civic Line set.

W: per icon, the median medial-axis width of the black-sheet ink mask (8x
estimator, see stroke_width.py); W is the median of those medians, rounded to
0.25 source px. s: 128-unit viewBox units per source px, set so the largest
pictogram extent (ink box width or height, stroke included) fills 116 units.
Placement: each icon's ink-box center maps to (64, 64).

Run with:  python3 -I measure_scale_stroke.py
Writes the scale JSON and note in qa/ and adds the transform to the inventory.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
import stroke_width as SW  # noqa: E402
from crop_references import write_csv  # noqa: E402

OUTLIER = 0.12


def main():
    inv = C.load_inventory()
    rows = inv["icons"]
    per = []
    for r in rows:
        crop = C.load_rgb(os.path.join(C.ASSETS, "reference-crops", r["reference_crops"]["black"]))
        g = C.green(crop)
        thr = r["mask_params"]["ink_threshold_g"]
        m1 = g < thr
        w4, n4 = SW.measure(g, thr)
        w1, n1 = SW.robust_median(SW.skeleton_widths(m1, 1))
        ys, xs = np.nonzero(m1)
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()) + 1, int(ys.min()), int(ys.max()) + 1
        per.append({"id": r["id"], "stroke_8x": round(w4, 3), "stroke_1x": round(w1, 3), "samples": n4,
                    "ink_box": [x0, y0, x1, y1], "w": x1 - x0, "h": y1 - y0, "extent": max(x1 - x0, y1 - y0),
                    "cx": (x0 + x1) / 2.0, "cy": (y0 + y1) / 2.0})
    widths = np.array([p["stroke_8x"] for p in per])
    widths1 = np.array([p["stroke_1x"] for p in per])
    w_med = float(np.median(widths))
    W = round(w_med * 4) / 4.0
    outliers = [{"id": p["id"], "median": p["stroke_8x"], "diff_pct": round(100 * (p["stroke_8x"] - W) / W, 1)}
                for p in per if abs(p["stroke_8x"] - W) / W > OUTLIER]
    ext = sorted(per, key=lambda p: -p["extent"])
    largest = ext[0]["extent"]
    s = C.FILL_EXTENT / largest
    gap_flag = largest > 1.15 * ext[1]["extent"]
    bins = np.arange(np.floor(widths.min() * 4) / 4, widths.max() + 0.25, 0.25)
    hist, edges = np.histogram(widths, bins=bins)
    result = {
        "date": C.DATE,
        "W_source_px": W,
        "W_raw_median_source_px": round(w_med, 3),
        "s_units_per_source_px": round(s, 6),
        "stroke_width_units": round(W * s, 4),
        "largest_extent_source_px": largest,
        "largest_extent_id": ext[0]["id"],
        "fill_extent_units": C.FILL_EXTENT,
        "clear_space_units": (C.VIEW - C.FILL_EXTENT) / 2,
        "largest_more_than_15pct_beyond_next": bool(gap_flag),
        "ten_largest_extents": [{"id": p["id"], "extent_px": p["extent"], "w": p["w"], "h": p["h"],
                                 "extent_units": round(p["extent"] * s, 2)} for p in ext[:10]],
        "stroke_distribution": {
            "count": len(widths), "min": float(widths.min()), "p10": float(np.percentile(widths, 10)),
            "p25": float(np.percentile(widths, 25)), "median": w_med, "p75": float(np.percentile(widths, 75)),
            "p90": float(np.percentile(widths, 90)), "max": float(widths.max()), "mean": float(widths.mean()),
            "std": float(widths.std()),
            "histogram_0.25px": [{"from": float(edges[i]), "to": float(edges[i + 1]), "n": int(hist[i])} for i in range(len(hist))],
        },
        "stroke_distribution_1x_reference_only": {
            "median": float(np.median(widths1)), "p25": float(np.percentile(widths1, 25)),
            "p75": float(np.percentile(widths1, 75))},
        "outliers_over_12pct": outliers,
        "outlier_notes": {"R-03": "R-03 is drawn entirely as filled seat dots, so its reading is the dot diameter; it has no stroke to measure."},
        "per_sheet_median": {k: float(np.median([p["stroke_8x"] for p, r in zip(per, rows) if r["sheet"] == k])) for k in C.SHEETS},
        "method": {
            "stroke": "Per icon: black-sheet crop, green channel, bilinear 8x upsample with a 3 px Gaussian (at 8x), threshold at the crop's midpoint (local background to full ink); skimage medial_axis with distance; width = 2 * distance / 8 at skeleton points; samples above 2.5x the raw median dropped (fills, junctions); median.",
            "W": "median of the 122 per-icon medians, rounded to the nearest 0.25 source px",
            "extent": "1x midpoint ink mask bounding box, width or height, stroke included",
            "s": "116 / largest extent, so the largest pictogram spans 116 units and keeps 6 units of clear space in the 128-unit viewBox",
            "placement": "X = s * (x - cx) + 64, Y = s * (y - cy) + 64, with (cx, cy) the ink-box center in crop pixel coordinates (pixel i covers [i, i+1])",
        },
        "estimator_calibration": SW.calibration_summary(),
        "per_icon": per,
    }
    for r, p in zip(rows, per):
        r["stroke_median_px"] = p["stroke_8x"]
        r["stroke_median_1x_px"] = p["stroke_1x"]
        r["extent_px"] = p["extent"]
        r["extent_units"] = round(p["extent"] * s, 3)
        r["transform"] = {
            "s": round(s, 6), "cx": p["cx"], "cy": p["cy"],
            "formula": f"X = {s:.6f} * (x - {p['cx']}) + 64; Y = {s:.6f} * (y - {p['cy']}) + 64",
            "matrix": [round(s, 6), 0, 0, round(s, 6), round(64 - s * p["cx"], 6), round(64 - s * p["cy"], 6)],
        }
        if abs(p["stroke_8x"] - W) / W > OUTLIER and "stroke-outlier" not in r["flags"]:
            r["flags"].append("stroke-outlier")
    inv["W_source_px"] = W
    inv["s_units_per_source_px"] = round(s, 6)
    inv["stroke_width_units"] = round(W * s, 4)
    C.write_json(C.INVENTORY_JSON, inv)
    write_csv(rows)
    C.write_json(C.SCALE_JSON, result)
    write_note(result)
    print(f"W = {W} px (raw median {w_med:.3f}), s = {s:.6f}, stroke = {W * s:.3f} units, largest {ext[0]['id']} {largest} px")
    print("ten largest:", [(p["id"], p["extent"]) for p in ext[:10]])
    print("outliers:", outliers)


def write_note(r):
    d = r["stroke_distribution"]
    lines = [
        "# Civic Line scale and line weight",
        "",
        f"Measured on October 29, 2026 from the 122 black-sheet reference crops. Numbers come from `{os.path.basename(C.SCALE_JSON)}` beside this note.",
        "",
        "## Line weight",
        "",
        f"W = **{r['W_source_px']} source px**. That is the median of the 122 per-icon median stroke widths ({d['median']:.3f} px), rounded to the nearest quarter pixel. In the 128-unit export it becomes **{r['stroke_width_units']} units**.",
        "",
        f"The per-icon medians run from {d['min']:.2f} to {d['max']:.2f} px. The middle half sits between {d['p25']:.2f} and {d['p75']:.2f} px, and the standard deviation is {d['std']:.2f} px.",
        "",
        f"Each width is read the way the brief asks: twice the distance-transform value at medial-axis points of the ink mask. The mask is taken at 8x (bilinear upsample, a 3 px Gaussian at 8x, then the midpoint threshold), because a 1x mask rounds every width to whole pixels. On {r['estimator_calibration']['cases']} synthetic antialiased rings and bars of known width the 8x reading is off by {r['estimator_calibration']['8x']['mean_error']:+.2f} px on average and {r['estimator_calibration']['8x']['max_abs_error']:.2f} px at worst. The 1x reading is off by up to {r['estimator_calibration']['1x']['max_abs_error']:.1f} px.",
        "",
        "Per-sheet medians: " + ", ".join(f"sheet {k} {v:.2f} px" for k, v in r["per_sheet_median"].items()) + ".",
        "",
        f"Icons whose own median differs from W by more than 12 percent: {', '.join(f'{o['id']} ({o['median']:.2f} px, {o['diff_pct']:+.1f}%)' for o in r['outliers_over_12pct']) or 'none'}. " + " ".join(r["outlier_notes"].values()),
        "",
        "## Scale",
        "",
        f"s = **{r['s_units_per_source_px']} units per source px**, one value for the whole set. The largest pictogram, {r['largest_extent_id']}, spans {r['largest_extent_source_px']} source px including stroke, so it fills 116 units and keeps 6 units of clear space on its long side. Every other icon keeps its size relative to it, as on the sheets.",
        "",
        "The ten largest extents:",
        "",
        "| ID | Extent (px) | Width | Height | Units |",
        "|---|---:|---:|---:|---:|",
    ]
    for p in r["ten_largest_extents"]:
        lines.append(f"| {p['id']} | {p['extent_px']} | {p['w']} | {p['h']} | {p['extent_units']} |")
    lines += [
        "",
        ("The largest extent is more than 15 percent beyond the next one, so one wide icon sets the scale for all."
         if r["largest_more_than_15pct_beyond_next"] else
         "The largest extent is within 15 percent of the next one, so no single icon sets the scale on its own."),
        "",
        "## What this means at small sizes",
        "",
        f"The brief's starting estimate was 3 to 4 units of stroke in the 128-unit box. The measured weight at one shared scale comes to {r['stroke_width_units']:.2f} units, because the widest reform pictograms set the scale and the set keeps their relative sizes. Rendered at 24 px the stroke is {r['stroke_width_units'] * 24 / 128:.2f} px wide, at 32 px {r['stroke_width_units'] * 32 / 128:.2f} px and at 64 px {r['stroke_width_units'] * 64 / 128:.2f} px. The size strips in `sizes/` show the effect. Use below 32 px would need its own optical-size masters; that is a decision for Dustin, outside this tracing pass.",
        "",
        "## Placement",
        "",
        "Each icon's ink-box center in its crop maps to (64, 64): X = s * (x - cx) + 64 and Y = s * (y - cy) + 64. The inventory stores cx, cy and the matrix per icon.",
        "",
    ]
    with open(C.SCALE_JSON.replace(".json", ".md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


if __name__ == "__main__":
    main()
