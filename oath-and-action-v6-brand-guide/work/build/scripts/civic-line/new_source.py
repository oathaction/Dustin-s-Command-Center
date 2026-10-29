"""Start a source: write src/<ID>.svg and src/<ID>.json skeletons with the
right viewBox, data-id and catalogue text. Refuses to overwrite.

    python3 -I new_source.py <ID> [--tracer NAME]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--tracer", default="")
    a = ap.parse_args()
    row = C.inventory_by_id().get(a.id)
    if row is None:
        raise SystemExit(f"{a.id} is not in the inventory")
    svg = os.path.join(C.SRC, f"{a.id}.svg")
    js = os.path.join(C.SRC, f"{a.id}.json")
    for p in (svg, js):
        if os.path.exists(p):
            raise SystemExit(f"{p} exists; edit it instead")
    w, h = row["crop"]["w"], row["crop"]["h"]
    ib = row["ink_box_crop"]
    with open(svg, "w", encoding="utf-8") as fh:
        fh.write(f"""<svg xmlns="http://www.w3.org/2000/svg" data-id="{a.id}" viewBox="0 0 {w} {h}">
  <!-- {a.id} {row['label']}. Crop {w} x {h} px; ink box x {ib['x0']}..{ib['x1']}, y {ib['y0']}..{ib['y1']}.
       Construction: {row['construction'].replace('--', '-')}
       Red: {row['red_text'].replace('--', '-')} -->
  <g data-role="base">
  </g>
  <g data-role="accent">
  </g>
</svg>
""")
    with open(js, "w", encoding="utf-8") as fh:
        json.dump({"id": a.id, "tracer": a.tracer, "corrections": [], "notes": ""}, fh, indent=2)
        fh.write("\n")
    print(f"wrote {os.path.relpath(svg, C.ROOT)} and {os.path.relpath(js, C.ROOT)}")


if __name__ == "__main__":
    main()
