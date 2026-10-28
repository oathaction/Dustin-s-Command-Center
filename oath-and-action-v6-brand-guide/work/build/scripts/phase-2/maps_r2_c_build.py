#!/usr/bin/env python3
"""Direction C, Loop Lines: build every drawing, page and the board from Atlas V7.

Run:  python3 -I work/build/scripts/phase-2/maps_r2_c_build.py
Then: python3 -I work/build/scripts/phase-2/maps_r2_c_verify.py
      node work/build/scripts/phase-2/maps_r2_c_check.js       (captures, PDF, rendered checks)
      python3 -I work/build/scripts/phase-2/maps_r2_c_build.py  (again, to print the results on the board)
Reads  work/extract/atlas-v7-data.json through maps_model.py (never written)
       work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Station-Table.csv and -District-Fields.csv
Writes work/boards/phase-2/maps-r2/c/20261028_*.svg, *.html, the network data JSON
       work/boards/20261028_Map-Direction-C-Loop-Lines.html
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import maps_r2_c_cards as C  # noqa: E402
import maps_r2_c_draw as D  # noqa: E402
import maps_r2_c_geom as G  # noqa: E402
import maps_r2_c_pages as P  # noqa: E402
import maps_r2_c_views as V  # noqa: E402

ROOT = G.ROOT
A = G.ASSETS
PFX = "20261028_"
WRITTEN = []


def save(name, text, ext):
    path = A / f"{PFX}{name}.{ext}"
    if ext == "svg":
        text = '<?xml version="1.0" encoding="UTF-8"?>\n' + text
    path.write_text(text, encoding="utf-8")
    WRITTEN.append(path)
    return path


def network_data(L):
    """Everything the drawings place, for the handoff and the verifier: stations, corridors, routes, tracks."""
    out = {"source": "work/extract/atlas-v7-data.json via maps_model.py", "cell_px": L.cell, "origin_px": [L.ox, L.oy],
           "pitch_px": L.pitch, "corner_radius_px": L.radius, "stations": {}, "corridors": []}
    for sid in G.STATIONS:
        t = L.table[sid]
        out["stations"][sid] = {"col": t["col"], "row": t["row"], "px": list(L.station_px(sid)), "district": t["district"],
                                "label_side": t["label"], "loops": G.station_loops(sid), "name": G.M["nodes"][sid]["short"]}
    for (a, b), trs in L.tracks.items():
        out["corridors"].append({"stations": [a, b], "route_cells": [list(c) for c in G.simplify(L.routes_cells[(a, b)])],
                                 "tracks": [{"link": t["link"], "loop": t["loop"], "offset_px": t["offset"]} for t in trs]})
    return out


def main():
    A.mkdir(parents=True, exist_ok=True)
    L = V.layout()
    Ls = C.locator_layout(L, 300, 196)                       # the locator inset, same routes
    # 1. poster, working map, reform view
    poster, _, boxes, _ = V.poster(L)
    save("Loop-Lines-Poster", poster, "svg")
    working, _, _, _ = V.poster(L, "newsprint", lit_loop="R10", view="c-working",
                                label="Loop Lines working map on Newsprint with Loop R10 lit and every other line in Stone")
    save("Loop-Lines-Working-Map-R10-Lit", working, "svg")
    reform, _, _, _ = V.poster(L, "white", reform="R-01", lit_loop=G.M["reforms"]["R-01"]["loops"], view="c-reform",
                               label="Loop Lines reform view on White: Reform R-01 acts on L25, L08 and C2, marked in red; "
                                     "the three loops it touches stay in Charcoal and the rest drop to Stone")
    save("Loop-Lines-Reform-View-R-01", reform, "svg")
    printed, _, _, _ = V.poster(L, print_=True, view="c-poster-print",
                                label="Loop Lines poster for print at 24 by 36 inches: the 20 numbered loops of Atlas V7 as closed lines, "
                                      "each line bullet carrying its kind glyph")
    save("Loop-Lines-Poster-Print", printed, "svg")
    cap = lambda n: f"{PFX}Loop-Lines-{n}-Capture.png"
    save("Loop-Lines-Poster", P.view_page("Loop Lines Poster", poster, "prussian", "The Loop Lines poster, 1440 px and fit to a phone",
                                          cap("Poster"), "The Loop Lines poster: the 20 numbered loops of Atlas V7 as closed lines through 25 variables in five areas."), "html")
    save("Loop-Lines-Poster-Print", P.print_page(printed), "html")
    save("Loop-Lines-Working-Map", P.view_page("Loop Lines Working Map", working, "", "Working map with R10 lit, 1440 px and fit to a phone",
                                               cap("Working-Map"), "The working map on Newsprint with Loop R10 lit in Charcoal and every other line in Stone."), "html")
    save("Loop-Lines-Reform-View-R-01", P.view_page("Reform View R-01", reform, "white", "Reform R-01 on the whole map, on White",
                                                    cap("Reform-View-R-01"), "The reform view on White: Reform R-01 marked in red where it acts, "
                                                    "the three loops it touches in Charcoal and the rest in Stone.",
                                                    panel=P.reform_panel("R-01", responsive=True)), "html")
    # 2. catalog pages
    written = []
    cat, order = P.catalog_page(L, written=written)
    save("Loop-Lines-Catalog", cat, "html")
    catp, order_p = P.catalog_page(L, phone=True, written=written)
    save("Loop-Lines-Catalog-Phone", catp, "html")
    # 3. card pages
    for lid, rid in (("R8", "R-30"), ("R10", "R-01")):
        save(f"Loop-Lines-Card-{lid}", P.card_page(L, Ls, lid, rid, written=written), "html")
        save(f"Loop-Lines-Card-{lid}-Phone", P.card_page(L, Ls, lid, rid, phone=True, written=written), "html")
    seen = set()
    for name, svg in written:
        if name in seen:
            continue
        seen.add(name)
        save("Loop-Lines-" + name, svg, "svg")
    data = network_data(L)
    data["catalog_order_1440"] = [lid for lid, _ in order]
    data["catalog_order_390"] = [lid for lid, _ in order_p]
    data["label_overlaps_poster"] = D.overlaps(boxes)
    (A / f"{PFX}Loop-Lines-Network-Data.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    WRITTEN.append(A / f"{PFX}Loop-Lines-Network-Data.json")
    import maps_r2_c_board as B  # noqa: E402
    B.build(L, order)
    print(f"wrote {len(WRITTEN)} files to {A.relative_to(ROOT)}; catalog order {[lid for lid, _ in order]}")


if __name__ == "__main__":
    main()
