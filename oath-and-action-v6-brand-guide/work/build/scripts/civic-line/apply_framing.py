"""DR-08: write the capped-fit framing into the inventory.

    python3 -I apply_framing.py

Per icon, s_i = min(116 / extent_i, 1.25 * s), with s the shared scale from
the scale file (0.487395). The stroke becomes W * s_i, so it runs from 2.68 to
3.35 units. Centering stays on the ink box. The script also writes each icon's
export names for the four editions and its twelve tile names, its tile optics
(the optical scale and offset from the variant review, S-1 and S-2, the stroke
multiplier that holds the 3.3508-unit cap, the resulting scale per shape) and
its minimum tile sizes (M-1), and records the framing in the scale file and its
note. It reads the shared scale every time, so a rerun gives the same numbers.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
from crop_references import write_csv  # noqa: E402


def tile_fields(r):
    """Write one icon's tile optics and minimum sizes into its inventory row."""
    a, dx, k = C.tile_optics(r["id"], r["stroke_units"])
    r["tile_optical_scale"] = a
    r["tile_offset_x"] = dx
    r["tile_stroke_scale"] = round(k, 6)
    r["tile_stroke_units"] = round(min(r["stroke_units"] * a, C.TILE_STROKE_CAP), 4)
    r["tile_scale"] = {sh: round(f * a, 6) for sh, f in C.TILE_FACTORS.items()}
    r["tile_min_px"] = C.tile_min_px(r["id"])


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
        tile_fields(r)
        strokes.append(W * si)
    inv["tiles_rule"] = {
        "factors": C.TILE_FACTORS, "decision": "DR-10, variant review M-1, S-1 and S-2",
        "transform": "matrix(f*a 0 0 f*a 64(1 - f*a) + f*dx 64(1 - f*a)), f the shape factor, a tile_optical_scale, dx tile_offset_x",
        "stroke": f"every stroke-width times tile_stroke_scale = min(1, {C.TILE_STROKE_CAP} / (stroke_units * a))",
        "min_px": "bare floor (32 px, or 48 px for the 28 icons that stop reading at 32 px; 48 px for every two-color tile) "
                  "divided by the shape factor, rounded up to a multiple of 4 px",
        "pillar_group": C.PILLAR_GROUP}
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
        f"{capped} icons stop at the cap and {len(strokes) - capped} fill 116 units. Centering stays on each icon's ink box. "
        f"The shared scale above still governs the contact sheets, which repeat the source layout.\n")
    with open(note, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"framing written: stroke {min(strokes):.4f} to {max(strokes):.4f} units; {capped} at the cap, {len(strokes) - capped} fill 116")


if __name__ == "__main__":
    main()
