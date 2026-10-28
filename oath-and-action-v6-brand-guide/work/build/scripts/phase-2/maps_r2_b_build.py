#!/usr/bin/env python3
"""Build Direction B, Snowball and Thermostat: drawings, specimen pages, geometry data and the review board.

Run:  python3 -I work/build/scripts/phase-2/maps_r2_b_build.py
Then: python3 -I work/build/scripts/phase-2/maps_r2_b_verify.py
      node work/build/scripts/phase-2/maps_r2_b_check.js
      python3 -I work/build/scripts/phase-2/maps_r2_b_build.py   (again, to print the check results on the board)
      node work/build/scripts/phase-2/maps_r2_b_check.js         (again, to check the board as it ships)
Reads  work/extract/atlas-v7-data.json through maps_model.py (never written)
Writes work/boards/phase-2/maps-r2/b/ (SVG drawings, five specimen pages, geometry data)
       work/boards/20261028_Map-Direction-B-Snowball-And-Thermostat.html
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import maps_model as MM  # noqa: E402
import maps_r2_b_draw as D  # noqa: E402
import maps_r2_b_geom as G  # noqa: E402
import maps_r2_b_pages as P  # noqa: E402

ROOT = HERE.parents[3]
ASSETS = ROOT / "work/boards/phase-2/maps-r2/b"
BOARD = ROOT / "work/boards/20261028_Map-Direction-B-Snowball-And-Thermostat.html"
M = MM.build_model()
LP = M["loops"]
WRITTEN = []
esc = P.esc


def save(name, text):
    path = ASSETS / name
    if name.endswith(".svg"):
        text = '<?xml version="1.0" encoding="UTF-8"?>\n' + text
    path.write_text(text, encoding="utf-8")
    WRITTEN.append(path)
    return path


def svg_body(text):
    return text.split("?>", 1)[1].strip() if text.startswith("<?xml") else text


# ------------------------------------------------------------------ drawings

def demo_svg():
    """How-to-read demo on Charcoal: the spiral with its start and its echo named."""
    geo = D.head_geo(size=132, disc=11, stroke=3)
    geo["arrow"] = (10, 5)
    geo["gap"] = 3
    em = D.emblem("R", geo, ink=D.NEWS, ground=D.INK)
    body = svg_body(em)
    inner = body[body.index("</style>") + 8:body.rindex("</svg>")]
    r, k, cx, cy = geo["r"], geo["k"], geo["cx"], geo["cy"]
    x0, y0 = G.pt(cx, cy, r, 0)
    x1, y1 = G.pt(cx, cy, k * r, G.TAU)
    W = 300
    lab = (D.T(x0, y0 + geo["disc"] + 20, "Start", 14, 600, D.NEWS, "middle")
           + D.T(x1 + 18, y1 + 5, "Start again, one turn later", 14, 600, D.NEWS))
    return D.svg_doc(W, 132, inner + lab, "The spiral: the first disc is the start; the outlined disc above it is the same variable one turn later",
                     "b-demo")


def build_drawings():
    out = {"mini": {}, "card": {}, "phone": {}}
    geo = D.mini_geo()
    for lid in M["loop_order"]:
        svg = D.miniature(LP[lid], geo)
        save(f"20261028_B-Mini-{lid}.svg", svg)
        out["mini"][lid] = svg
    for lid, rid in (("R8", "R-30"), ("R10", "R-01"), ("B4", "R-07")):
        svg, f = D.card_figure(LP[lid], M, rid)
        assert not f, (lid, f)
        save(f"20261028_B-Card-{lid}.svg", svg)
        out["card"][lid] = svg
        ph, f = D.phone_figure(LP[lid], M, rid)
        assert not f, (lid, f)
        save(f"20261028_B-Card-Phone-{lid}.svg", ph)
        out["phone"][lid] = ph
    # the reform view draws R10 with R-01 named (same as the R10 card figure, named for its own view)
    rv, f = D.card_figure(LP["R10"], M, "R-01", view="b-reform")
    save("20261028_B-Reform-R-01-On-R10.svg", rv)
    out["reform"] = rv
    rvp, f = D.phone_figure(LP["R10"], M, "R-01", view="b-reform-phone")
    save("20261028_B-Reform-R-01-On-R10-Phone.svg", rvp)
    out["reform_phone"] = rvp
    hg = D.head_geo(disc=20, stroke=5)
    hg["arrow"] = (18, 9)
    hg["gap"] = 5
    out["emblem"] = {k: D.emblem(k, hg) for k in ("R", "B")}
    out["emblem_geo"] = hg
    save("20261028_B-Emblem-Snowball-240.svg", out["emblem"]["R"])
    save("20261028_B-Emblem-Thermostat-240.svg", out["emblem"]["B"])
    out["glyph"] = {k: D.glyph24(k) for k in ("R", "B")}
    save("20261028_B-Kind-Mark-Snowball-24.svg", out["glyph"]["R"])
    save("20261028_B-Kind-Mark-Thermostat-24.svg", out["glyph"]["B"])
    out["demo"] = demo_svg()
    save("20261028_B-How-To-Read-Demo.svg", out["demo"])
    # test panel: the review's ratio (1.3) beside the chosen one (1.8), at miniature and card size
    out["test"] = {}
    for kk, tag in ((D.K_BRIEF, "K13"), (D.K, "K18")):
        g = D.mini_geo(kk)
        for lid in ("R8", "R10", "B4"):
            svg = D.miniature(LP[lid], g, view="b-test-mini", label_extra=f" Test drawing, spiral ratio {kk}.")
            svg = svg.replace('data-view="b-test-mini"', f'data-view="b-test-mini" data-test-k="{kk}"')
            save(f"20261028_B-Test-Mini-{lid}-{tag}.svg", svg)
            out["test"][(lid, tag, "mini")] = svg
    svg13, f = D.card_figure(LP["R8"], M, None, geo=D.card_geo(k=D.K_BRIEF), view="b-test-card")
    svg13 = svg13.replace('data-view="b-test-card"', f'data-view="b-test-card" data-test-k="{D.K_BRIEF}"')
    save("20261028_B-Test-Card-R8-K13.svg", svg13)
    out["test"][("R8", "K13", "card")] = svg13
    svg18, f = D.card_figure(LP["R8"], M, None, view="b-test-card")
    svg18 = svg18.replace('data-view="b-test-card"', f'data-view="b-test-card" data-test-k="{D.K}"')
    save("20261028_B-Test-Card-R8-K18.svg", svg18)
    out["test"][("R8", "K18", "card")] = svg18
    # phone size, so the board can show the same test at 390 px
    for kk, tag in ((D.K_BRIEF, "K13"), (D.K, "K18")):
        ph, f = D._figure(LP["R8"], M, None, dict(D.phone_geo(), k=kk), 358, 44, 64, "b-test-phone", D.WHITE, True, True)
        ph = ph.replace('data-view="b-test-phone"', f'data-view="b-test-phone" data-test-k="{kk}"')
        save(f"20261028_B-Test-Phone-R8-{tag}.svg", ph)
        out["test"][("R8", tag, "phone")] = ph
    return out


def geometry_data(dr):
    geo = D.mini_geo()
    cg = D.card_geo()
    rows = {}
    for lid, lp in LP.items():
        k = 1 if lp["type"] == "B" else D.K
        st = []
        for i, s in enumerate(lp["stations"]):
            t = G.TAU * i / lp["n"]
            st.append({"code": s["code"], "label": s["label"], "angle_deg": round(math.degrees(t), 4),
                       "radius_in_r": round(G.rho(t, 1, k), 4)})
        if lp["type"] == "R":
            st.append({"code": lp["stations"][0]["code"], "label": lp["stations"][0]["label"] + ", one turn later", "angle_deg": 360.0,
                       "radius_in_r": round(D.K, 4), "echo": True})
        rows[lid] = {"type": lp["type"], "shape": "spiral" if lp["type"] == "R" else "ring", "stations": st,
                     "steps": [s["id"] for s in lp["steps"]], "group": lp["group"]}
    data = {"source": "work/extract/atlas-v7-data.json via work/build/scripts/phase-2/maps_model.py", "snapshot": SNAP_ISO,
            "rule": "Snowball: p(t) = r (1 + (k - 1) t / 2 pi), t clockwise from twelve o'clock, one turn. Thermostat: circle at r. "
                    "Stations at t_i = 2 pi i / n. k is one constant for every reinforcing loop.",
            "k": D.K, "k_review_start": D.K_BRIEF,
            "scales": {"miniature": geo, "card": dict(cg), "phone_card": D.phone_geo(), "head_emblem": dr["emblem_geo"]},
            "loops": rows}
    save("20261028_Direction-B-Geometry-Data.json", json.dumps(data, indent=1, ensure_ascii=False))


SNAP_ISO = "2026-10-15"


# ------------------------------------------------------------------ rails

def rails():
    r8 = "".join([
        P.rail_block("Feeds itself", "Each turn builds on the last",
                     ("Follow the line clockwise from A5, Housing scarcity. It reaches A6, Owner home equity, then comes back to A5 one lap further out.", ""),
                     (esc(P.HONEST), "honest")),
        P.rail_block("Now", P.direction_text(LP["R8"]),
                     (f'Atlas V7\'s measured series for this loop: {esc(LP["R8"]["reference_mode"])}.', ""),
                     ("A chart of that series sits here once the research lead supplies sourced values with their period.", "")),
        P.rail_block("One turn", P.cap1(LP["R8"]["delay_word"]),
                     ("A loop turns at the pace of its slowest step. Both steps here take over 10 years.", "")),
        P.rail_block("Least certain step", "A tie: both well supported",
                     ("V7's evidence note names L39 the weaker step, “because equity is one motive among several for opposing construction.”", "")),
        P.rail_block("Revision", None, ("V7 notes that the loop no longer depends on A1, Concentration of household wealth.", "")),
    ])
    r10 = "".join([
        P.rail_block("Feeds itself", "Each turn builds on the last",
                     ("Follow the line clockwise from C1, Safe seats. Four steps later it comes back to C1 one lap further out.", ""),
                     (esc(P.HONEST), "honest")),
        P.rail_block("Now", P.direction_text(LP["R10"]),
                     (f'Atlas V7\'s measured series for this loop: {esc(LP["R10"]["reference_mode"])}.', ""),
                     ("A chart of that series sits here once the research lead supplies sourced values with their period.", "")),
        P.rail_block("One turn", P.cap1(LP["R10"]["delay_word"]),
                     ("A loop turns at the pace of its slowest step. L53 and L42 each take 2 to 10 years.", "")),
        P.rail_block("Least certain step", "L53, plausible",
                     ("A coherent mechanism with some evidence. V7: “its evidence is the 2025 mid-decade redistricting in states with one-party control and legal analysis.”", "")),
        P.rail_block("What V7 does not claim", None,
                     ("“The claim that primary reform makes legislators more moderate is contested, so the loop concerns accountability more than ideology.”", "")),
    ])
    b4 = "".join([
        P.rail_block("Pushes back", "The system corrects itself",
                     ("Follow the ring clockwise from D5, Public service quality. It passes C3 and C5 and closes on D5 where it began.", "")),
        P.rail_block("How it should work", None, (esc(LP["B4"]["summary"]), "")),
        P.rail_block("What is happening now", P.direction_text(LP["B4"]),
                     (f'Atlas V7\'s measured series for this loop: {esc(LP["B4"]["reference_mode"])}.', ""),
                     ("A chart of that series sits here once the research lead supplies sourced values with their period.", ""),
                     (f'V7: “{esc(LP["B4"]["qualification"].split(". ")[0])}.”', "")),
        P.rail_block("One turn", P.cap1(LP["B4"]["delay_word"]),
                     ("A loop turns at the pace of its slowest step. L24 and L54 each take 2 to 10 years.", "")),
        P.rail_block("Least certain step", "A tie: all three well supported",
                     ("V7's evidence note: “For U.S. services the weakest is L54, since its main study covers Brazilian mayors.”", "")),
    ])
    return {"R8": r8, "R10": r10, "B4": b4}


HEADLINES = {
    "R8": "Scarce housing builds the equity that keeps it scarce",
    "R10": "In safe seats, officials can write the rules that keep the seats safe",
    "B4": "When services slip, the risk of defeat can push them back up",
    "R-01": "All-party primaries act where the primary picks the winner",
}


def build_pages(dr):
    pages = {}
    cat = P.catalog_page(M, {k: svg_body(v) for k, v in dr["mini"].items()}, {k: svg_body(v) for k, v in dr["emblem"].items()},
                         svg_body(dr["demo"]))
    pages["catalog"] = save("20261028_Direction-B-Loop-Catalog.html", cat)
    rl = rails()
    for lid, rid in (("R8", "R-30"), ("R10", "R-01"), ("B4", "R-07")):
        html_ = P.card_page(M, lid, rid, HEADLINES[lid], {"desk": svg_body(dr["card"][lid]), "phone": svg_body(dr["phone"][lid])},
                            rl[lid], f"Loop Card {lid}, Direction B")
        pages[lid] = save(f"20261028_Direction-B-Loop-Card-{lid}.html", html_)
    also = []
    for lid in ("B4", "R11"):
        lp = LP[lid]
        also.append(f'<figure data-loop="{lid}">{svg_body(dr["mini"][lid])}<figcaption>{P.chip("Loop", lid)}<h3>{esc(lp["title"])}</h3>'
                    f'<p style="margin:0">{P.kind_word(lp)}. Atlas V7 lists R-01 on this loop, but none of its three targets sits on this loop\'s steps or stations, '
                    f'so nothing here is red.</p></figcaption></figure>')
    rv = P.reform_page(M, "R-01", HEADLINES["R-01"], svg_body(dr["reform"]), svg_body(dr["reform_phone"]), "".join(also), "Reform View R-01, Direction B")
    pages["R-01"] = save("20261028_Direction-B-Reform-View-R-01.html", rv)
    return pages


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    dr = build_drawings()
    geometry_data(dr)
    pages = build_pages(dr)
    if "--no-board" not in sys.argv:
        import maps_r2_b_board as B
        page = B.board(M, dr, pages)
        BOARD.write_text(page, encoding="utf-8")
        WRITTEN.append(BOARD)
        print("board", BOARD.relative_to(ROOT), f"{len(page) / 1e6:.2f} MB")
    print(len(WRITTEN), "files written")
