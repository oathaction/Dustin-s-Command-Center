"""DR-08: write the capped-fit framing into the inventory.

    python3 -I apply_framing.py

Per icon, s_i = min(116 / extent_i, 1.25 * s), with s the shared scale from
the scale file (0.487395). The stroke becomes W * s_i, so it runs from 2.68 to
3.35 units. Centring stays on the ink box. The script also writes each icon's
export names for the four editions and its twelve tile names, and records the
framing in the scale file and its note. It reads the shared scale every time,
so a rerun gives the same numbers.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
from crop_references import write_csv  # noqa: E402


def main():
    inv = C.load_inventory()
    sc = C.read_json(C.SCALE_JSON)
    s0 = sc["s_units_per_source_px"]
    W = sc["W_source_px"]
    strokes = []
    capped = 0
    for r in inv["icons"]:
        si = C.framed_scale(r["extent_px"], s0)
        if si < C.FILL_EXTENT / r["extent_px"] - 1e-12:
            capped += 1
        t = r["transform"]
        cx, cy = t["cx"], t["cy"]
        r["transform"] = {
            "s": round(si, 6), "s_shared": s0, "cap": C.FRAMING_CAP, "framing": "DR-08 capped fit",
            "cx": cx, "cy": cy,
            "formula": f"X = {si:.6f} * (x - {cx}) + 64; Y = {si:.6f} * (y - {cy}) + 64",
            "matrix": [round(si, 6), 0, 0, round(si, 6), round(64 - si * cx, 6), round(64 - si * cy, 6)],
        }
        r["stroke_units"] = round(W * si, 4)
        r["extent_units"] = round(r["extent_px"] * si, 3)
        names = C.export_names(r["id"], r["slug"])
        ex = {k: v for k, v in names.items() if k.startswith(("svg_", "png_"))}
        paths = []
        for ed in C.EDITIONS:
            k = ed.replace("-", "_")
            paths += [f"{ed}/{ex['svg_' + k]}", f"png-256/{ed}/{ex['png_' + k]}", f"png-512/{ed}/{ex['png_' + k]}"]
        ex["paths"] = paths
        r["exports"] = ex
        r["tiles"] = [f"tiles/{sh}-{tl}/svg/{C.tile_name(r['id'], r['slug'], sh, tl, md)}.svg"
                      for sh in C.TILE_SHAPES for tl in C.TILE_COLOURS for md in C.TILE_MODES]
        strokes.append(W * si)
    inv["framing"] = {"rule": "s_i = min(116 / extent_i, 1.25 * s)", "s_shared": s0, "cap": C.FRAMING_CAP,
                      "stroke_units_range": [round(min(strokes), 4), round(max(strokes), 4)], "decision": "DR-08"}
    inv["stroke_width_units"] = [round(min(strokes), 4), round(max(strokes), 4)]
    C.write_json(C.INVENTORY_JSON, inv)
    write_csv(inv["icons"])
    sc["framing"] = {"decision": "DR-08", "rule": "s_i = min(116 / extent_i, 1.25 * s)", "cap": C.FRAMING_CAP,
                     "stroke_units_min": round(min(strokes), 4), "stroke_units_max": round(max(strokes), 4),
                     "icons_at_cap": capped, "icons_filling_116": len(strokes) - capped}
    C.write_json(C.SCALE_JSON, sc)
    note = C.SCALE_JSON.replace(".json", ".md")
    text = open(note, encoding="utf-8").read()
    marker = "\n## Framing in the 128 box (DR-08)\n"
    text = text.split(marker)[0].rstrip() + "\n" + marker + (
        f"\nDustin approved the capped fit on October 29 (DR-08). Each icon grows toward 116 units by at most "
        f"{C.FRAMING_CAP} times the shared scale: s_i = min(116 / extent_i, {C.FRAMING_CAP} x {s0}). The stroke grows with it, "
        f"so it runs from {min(strokes):.2f} to {max(strokes):.2f} units across the set, a spread of 25 percent at most. "
        f"{capped} icons stop at the cap and {len(strokes) - capped} fill 116 units. Centring stays on each icon's ink box. "
        f"The shared scale above still governs the contact sheets, which repeat the source layout.\n")
    with open(note, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"framing written: stroke {min(strokes):.4f} to {max(strokes):.4f} units; {capped} at the cap, {len(strokes) - capped} fill 116")


if __name__ == "__main__":
    main()
