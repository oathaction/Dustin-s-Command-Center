"""Concept 1, Overprint: write the masters, color variants, holders, tiles, app tiles and pixel
renders (design director, Phase 2, round two, October 28, 2026).

Run: python3 -I icons_r2_overprint_assets.py
Writes, in work/boards/phase-2/icons-r2/overprint/:
  20261028_Overprint-<Icon>-{16px,24px,Display}.svg   masters: paths `accent` (Pillar Red, behind)
                                                      and `ink` (Charcoal, on top); the 16 px
                                                      solid cut has `ink` only
  variants/   the five other colorways of the 24 px and display masters, and the Newsprint and
              White versions of the one-color 16 px master
  holders/    9 empty holders and 90 tiles (ten icons, three shapes, three tile colors), at 80 px
  context/    the 1024 px app tile at the three tested glyph scales
  px/         1x renders of the 16 and 24 px masters on Newsprint and Charcoal for magnified views,
              and the same masters as a 2x screen draws them
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_overprint_common as C  # noqa: E402
import icons_r2_overprint_draw as O  # noqa: E402
import icons_geom as g  # noqa: E402


def title(name, kind):
    k = {"Display": "display master for 48 px and up", "24px": "24 px master",
         "16px": "16 px master, solid cut in one color"}[kind]
    return f"{O.LABELS[name]}, Concept 1 Overprint, {k}. Oath &amp; Action icon concept, October 28, 2026. Proposal only."


def write_masters():
    C.OUT.mkdir(parents=True, exist_ok=True)
    C.VARIANTS.mkdir(parents=True, exist_ok=True)
    n = 0
    for name in O.ICONS:
        for kind in C.KINDS:
            L = C.lay(name, kind)
            C.master_file(name, kind).write_text(C.svg(L, kind, title=title(name, kind)) + "\n")
            n += 1
            cws = ("Newsprint", "White") if kind == "16px" else [c for c in C.COLORWAYS if c != "Charcoal-Red"]
            for cw in cws:
                C.variant_file(name, kind, cw).write_text(C.svg(L, kind, cw=cw) + "\n")
                n += 1
    return n


def write_holders():
    C.HOLDERS.mkdir(parents=True, exist_ok=True)
    n = 0
    for shape in C.HOLDER_SHAPES:
        hp = C.RC.holder_path(shape, 100)
        for color, (fill, _) in C.HOLDER_COLORS.items():
            C.holder_file(shape, color).write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'
                f'<title>{shape.replace("-", " ")} holder, {color}</title><path d="{g.d_of(hp)}" fill="{fill}"/></svg>\n')
            n += 1
            for name in O.ICONS:
                s, *_ = C.tile_svg(name, shape, color, 80,
                                   title=f"{O.LABELS[name]} in a {shape.replace('-', ' ').lower()} holder, {color} tile. Proposal only.")
                C.tile_file(name, shape, color).write_text(s + "\n")
                n += 1
    return n


def write_app_tiles():
    C.CONTEXT.mkdir(parents=True, exist_ok=True)
    for sc in C.APP_SCALES:
        C.app_tile_file(sc).write_text(C.app_tile_svg(sc) + "\n")
    # the chosen scale on a Newsprint tile as well
    C.app_tile_file(C.APP_SCALE).with_name(f"{C.DATE}_Overprint-App-Tile-1024-{int(round(C.APP_SCALE * 100))}-Newsprint.svg").write_text(
        C.app_tile_svg(C.APP_SCALE, "Newsprint") + "\n")


def write_px():
    C.PX.mkdir(parents=True, exist_ok=True)
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    jobs = []
    for name in O.ICONS:
        for kind in ("16px", "24px"):
            L = C.lay(name, kind)
            s = C.vb(kind)
            jobs.append({"id": f"{C.stem(name, kind)}-Newsprint", "w": s, "h": s, "bg": C.NEWS, "html": C.svg(L, kind)})
            jobs.append({"id": f"{C.stem(name, kind)}-Charcoal", "w": s, "h": s, "bg": C.CHAR, "html": C.svg(L, kind, cw="Newsprint-Red")})
            # the same master on a 2x screen: a cell twice the size at device scale 1
            jobs.append({"id": f"{C.stem(name, kind)}-2x", "w": 2 * s, "h": 2 * s, "bg": C.NEWS, "html": C.svg(L, kind, px=2 * s)})
            jobs.append({"id": f"{C.stem(name, kind)}-Idle", "w": s, "h": s, "bg": C.NEWS, "html": C.svg(L, kind, cw="Charcoal")})
    jp = C.SCRATCH / "px-jobs.json"
    jp.write_text(json.dumps(jobs))
    subprocess.run(["node", str(C.RENDER_JS), str(jp), str(C.PX)], check=True)
    return len(jobs)


def main():
    n1 = write_masters()
    n2 = write_holders()
    write_app_tiles()
    n3 = write_px()
    print(f"masters and variants {n1}, holders and tiles {n2}, pixel renders {n3}")


if __name__ == "__main__":
    main()
