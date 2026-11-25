"""C1's pixel proof, the compare (DR-331): every tile proof.cjs captured with C1 off beside the same tile with C1 on.

  python3 compare.py OUTDIR [--json OUT.json]

A tile is identical when its two PNG files hold the same bytes, or, failing that, decode to the same pixels. Prints, for each
width, the plates and tiles compared, identical, different and missing, and lists each plate with a difference.
"""
import io
import json
import sys
from pathlib import Path


def pixels(p):
    from PIL import Image
    im = Image.open(p)
    im.load()
    return im.size, im.convert("RGBA").tobytes()


def main():
    out = Path(sys.argv[1])
    rec = {}
    for wdir in sorted(d for d in out.iterdir() if d.is_dir() and d.name.isdigit()):
        offs = {p.name: p for p in (wdir / "off").glob("*.png")}
        ons = {p.name: p for p in (wdir / "on").glob("*.png")}
        same = by_pixels = 0
        differ, missing = [], sorted(set(offs) ^ set(ons))
        for name in sorted(set(offs) & set(ons)):
            a, b = offs[name].read_bytes(), ons[name].read_bytes()
            if a == b:
                same += 1
            elif pixels(io.BytesIO(a)) == pixels(io.BytesIO(b)):
                by_pixels += 1
            else:
                differ.append(name)
        plates = lambda names: sorted({n.rsplit("--", 1)[0] for n in names})
        rec[wdir.name] = {"plates": len(plates(offs)), "tiles": len(offs), "identical_bytes": same, "identical_pixels": by_pixels,
                          "different": differ, "plates_different": plates(differ), "missing": missing}
        print(f"{wdir.name} px: {len(plates(offs))} plates, {len(offs)} tiles; {same} identical by bytes, {by_pixels} more by pixels; "
              f"{len(differ)} different in {len(plates(differ))} plate(s); {len(missing)} without a partner")
        for n in plates(differ):
            print(f"  differs: {n}")
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(rec, indent=1))
    bad = any(r["different"] or r["missing"] for r in rec.values())
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
