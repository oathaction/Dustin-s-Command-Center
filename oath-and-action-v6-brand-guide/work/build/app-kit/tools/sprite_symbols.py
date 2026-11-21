"""Print a hidden sprite holding the named symbols, drawn by the guide build's own sprite code (guide_build.Sprites), so an
application draws a Civic Line symbol or a utility icon exactly as the guide's page does and the kit keeps no copy of it.

Usage: python3 -I work/build/app-kit/tools/sprite_symbols.py oa-sym-cl-031 oa-sym-cl-031-24px ...
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "work/build/scripts/phase-2"))
import guide_build as gb  # noqa: E402


def main(ids):
    sp = gb.Sprites()
    out = []
    for sid in ids:
        if sid not in sp.symbols:
            print(f"no symbol {sid} in the guide's sprite families", file=sys.stderr)
            return 1
        fam, path, _ = sp.symbols[sid]
        out.append(gb.Sprites.symbol(path, sid, gb.SPRITE_FAMILIES[fam]["ink"]))
    print('<svg class="oa-sprite" aria-hidden="true" focusable="false" width="0" height="0" '
          'style="position:absolute;width:0;height:0;overflow:hidden">' + "".join(out) + "</svg>")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
