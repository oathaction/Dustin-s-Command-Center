"""Board 1's weight options for chapter 14 (D3-104), measured by script on a fresh strict build and a fresh pilot.

    python3 -I work/build/scripts/phase-3/weight_options.py --report STRICT-Build-Report.json --page STRICT.html
        --pilot Pilot-Results.json [--json OUT.json]

Reads the strict build's projection (today's page plus every unbuilt chapter's allocation, chapter 14 at its 1.75 MB),
the pilot's chapter 14 projection for 97 specimens (method load-table), the pilot page's 16 plates and the strict page's
photographs, and prints one Markdown table:

  1. as it stands
  2. chart data carried compressed: each chart's data island deflated and base64 in the page, expanded at load
     (a reader with scripts off loses nothing: only the script reads the island)
  3. tables compressed too: the table equivalent travels with the island, so a reader with scripts off loses every table
  4. the smaller photo copies: chapter 01's two shown photographs at 1,200 px wide (they show at 600 px at most), re-encoded,
     freeing page room; a visible resample
  5. the creative director's recommendation: the photo copies and chart data compressed, tables live, with chapter 14's
     stop raised to fit the chart data row, and the page's room left with Phase 4's share untouched

Each row's ask is the bytes chapter 14 runs over its stop, less the page's room under 15.5 MB, never below zero.

Board 1 apply (DR-238, November 12, 2026): once the guide carries each chart's data compressed (data-oa-chart-data="deflate")
and chapter 01's photographs at 1,200 px, the options above are built, so the script reports the page as built instead:
chapter 14's projection from the pilot, the page's projection with chapter 14 at its stop (the build's own) and at that
projection, the room under 15.5 MB, the photographs' pixel widths, what the compression saves each plate (each island
inflated here and set beside its JSON), and the build report's per-plate share. Pages with JSON islands still get the table.
"""
import argparse
import base64
import io
import json
import re
import sys
import zlib

MB = 1_000_000
STOP = 1.75 * MB                 # board 1's options were measured against the stop of the time
BUDGET = 15.5 * MB
FINISHED = 97
EXPANDER = 600     # bytes for the script that inflates a deflated island or table (DecompressionStream), an estimate


def deflate_b64(text):
    co = zlib.compressobj(9, zlib.DEFLATED, -15, 9)
    return len(base64.b64encode(co.compress(text.encode()) + co.flush()))


ISLAND = re.compile(r'<script type="(?:application/json|text/plain)" data-oa-chart-data(?:="(deflate)")?>(.*?)</script>', re.S)


def plates(page):
    """Each chapter 14 plate's table equivalent and data island; a compressed island is inflated back to its JSON text, and
    its element's bytes are set beside the JSON element the kit wrote before DR-238."""
    out = {}
    for m in re.finditer(r'<figure class="oac-fig" id="oac-(s-14-s\d\d)".*?</figure>', page, re.S):
        fig = m.group(0)
        tab = re.search(r'<div class="oac-tw".*?</table></div>', fig, re.S)
        isl = ISLAND.search(fig)
        packed = bool(isl and isl.group(1) == "deflate")
        text = (zlib.decompress(base64.b64decode(isl.group(2)), -15).decode() if packed else isl.group(2)) if isl else ""
        as_json = '<script type="application/json" data-oa-chart-data>' + text.replace("<", "\\u003c") + "</script>"
        out[m.group(1)] = {"table": tab.group(0) if tab else "", "island": text, "packed": packed,
                           "element": len(isl.group(0)) if isl else 0, "json_element": len(as_json) if isl else 0}
    return out


def photos(page):
    """Each embedded JPEG's pixel size and bytes as embedded data, in page order."""
    from PIL import Image
    out = []
    for m in re.finditer(r'<img\b[^>]*?src="data:image/jpeg;base64,([A-Za-z0-9+/=]+)"', page):
        im = Image.open(io.BytesIO(base64.b64decode(m.group(1))))
        out.append({"width": im.width, "height": im.height, "page_bytes": len(m.group(1))})
    return out


def as_built(a, rep, pil, pp):
    """The page as built after DR-238: compression and the smaller photographs in."""
    n = len(pp)
    ch14 = pil["projection"]["chapter_14"]
    stop = pil["projection"]["stop"]
    proj = rep["weight"]["projection"]
    page_at_stop = proj["projected_bytes"]
    page_at_proj = page_at_stop - proj["unbuilt"].get("14", stop) + ch14 if "14" in proj["unbuilt"] else page_at_stop
    save = sum(p["json_element"] - p["element"] for p in pp.values()) / n
    ph = photos(open(a.page, encoding="utf-8").read())
    share = proj.get("chapter_14_per_plate") or {}
    out = {"page_bytes": rep["bytes"], "plates": n, "islands_compressed": sum(p["packed"] for p in pp.values()),
           "compression_saving_per_plate": round(save), "chapter_14_projected": ch14, "chapter_14_stop": stop,
           "chapter_14_margin": round(stop - ch14), "pilot_plate_average": pil["specimen_avg"], "pilot_frame_average": pil["frame_avg"],
           "page_projected_chapter_14_at_stop": page_at_stop, "room_at_stop": round(BUDGET - page_at_stop),
           "page_projected_chapter_14_as_projected": round(page_at_proj), "room_as_projected": round(BUDGET - page_at_proj),
           "photographs": ph, "per_plate_share": share.get("per_plate"), "per_plate_line": share.get("line")}
    print(f"Strict page {rep['bytes']:,} bytes. Pilot: {n} plates, {out['islands_compressed']} with their data compressed, "
          f"{save:,.0f} bytes saved per plate against JSON islands.")
    print()
    print("| Figure | Bytes | MB |")
    print("|---|---|---|")
    for k, v in (("Chapter 14 projected for 97 specimens", ch14), ("Chapter 14's stop", stop), ("Under the stop", stop - ch14),
                 ("Page projected, chapter 14 at its stop (the build's projection)", page_at_stop),
                 ("Room under 15.5 MB, chapter 14 at its stop", BUDGET - page_at_stop),
                 ("Page projected, chapter 14 as projected", page_at_proj), ("Room under 15.5 MB, chapter 14 as projected", BUDGET - page_at_proj)):
        print(f"| {k} | {v:,.0f} | {v / MB:.3f} |")
    print()
    print("Photographs in the page: " + "; ".join(f"{p['width']} x {p['height']} px, {p['page_bytes']:,} bytes" for p in ph))
    if share:
        print(f"Per plate: {share['line']}")
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
    return 0


def photo_saving(page):
    from PIL import Image
    saved, n = 0, 0
    for m in re.finditer(r'<img\b[^>]*?src="data:image/jpeg;base64,([A-Za-z0-9+/=]+)"', page):
        raw = base64.b64decode(m.group(1))
        im = Image.open(io.BytesIO(raw))
        if im.width <= 1200:
            continue
        h = round(im.height * 1200 / im.width)
        small = io.BytesIO()
        im.resize((1200, h), Image.LANCZOS).save(small, "JPEG", quality=85, optimize=True, progressive=True,
                                                 icc_profile=im.info.get("icc_profile"))
        saved += len(m.group(1)) - len(base64.b64encode(small.getvalue()))
        n += 1
    return saved, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--page", required=True)
    ap.add_argument("--pilot", required=True)
    ap.add_argument("--json")
    a = ap.parse_args()
    rep = json.load(open(a.report))
    pil = json.load(open(a.pilot))["methods"]["load-table"]
    room = BUDGET - rep["weight"]["projection"]["projected_bytes"]
    ch14 = pil["projection"]["chapter_14"]
    pp = plates(open(pil["page"], encoding="utf-8").read())
    if pp and all(p["packed"] for p in pp.values()):
        return as_built(a, rep, pil, pp)
    n = len(pp)
    isl_save = sum(len(p["island"]) - deflate_b64(p["island"]) - 2 for p in pp.values()) / n
    both_save = sum(len(p["table"]) + len(p["island"]) - deflate_b64(p["table"] + "\0" + p["island"]) - 40 for p in pp.values()) / n
    photos, nph = photo_saving(open(a.page, encoding="utf-8").read())

    def ask(c14, extra_room=0):
        return max(0, round(c14 - STOP - room - extra_room))

    rows = [
        ("As it stands", ch14, ask(ch14), "Nothing"),
        ("Chart data carried compressed", ch14 - FINISHED * isl_save + EXPANDER, ask(ch14 - FINISHED * isl_save + EXPANDER),
         "Nothing: only the script reads the data"),
        ("Tables compressed too", ch14 - FINISHED * both_save + EXPANDER, ask(ch14 - FINISHED * both_save + EXPANDER),
         "With scripts off, every chart's table (title, description, notes and source line stay)"),
        ("The smaller photo copies", ch14, ask(ch14, photos),
         f"A visible resample: chapter 01's photographs ({nph} on the page, one shown twice) at 1,200 px wide, which frees {photos / MB:.3f} MB of the page"),
    ]
    # 5: the stop rises to the chart-data row's chapter 14; the page then carries that overrun less the photos' saving
    c14_rec = ch14 - FINISHED * isl_save + EXPANDER
    page_rec = rep["weight"]["projection"]["projected_bytes"] + (c14_rec - STOP) - photos
    rows.append(("Recommended: photo copies and chart data compressed, tables live", c14_rec, max(0, round(page_rec - BUDGET)),
                 f"The photo resample only; chapter 14's stop rises to {c14_rec / MB:.3f} MB and the page keeps {(BUDGET - page_rec) / MB:.3f} MB of room with Phase 4's share untouched"))
    out = {"page_bytes": rep["bytes"], "projected_page": rep["weight"]["projection"]["projected_bytes"], "room": round(room),
           "chapter_14_now": ch14, "stop": STOP, "plates": n, "island_saving_per_plate": round(isl_save),
           "table_and_island_saving_per_plate": round(both_save), "photo_saving": photos,
           "recommended": {"chapter_14_stop": round(c14_rec), "page_projected": round(page_rec), "room_left": round(BUDGET - page_rec),
                           "phase_4_share_untouched": BUDGET - page_rec >= 0},
           "options": [{"option": r[0], "chapter_14": round(r[1]), "ask_of_phase_4": r[2], "reader_loses": r[3]} for r in rows]}
    print(f"Strict page {rep['bytes']:,} bytes, projected {out['projected_page']:,}; room under 15.5 MB {room:,.0f}. "
          f"Pilot: {n} plates, chapter 14 projected {ch14:,}.")
    print()
    print("| Option | Chapter 14 projected | Over its 1.75 MB stop | Smallest ask of Phase 4's 2.54 MB | What a reader loses |")
    print("|---|---|---|---|---|")
    for r in rows:
        print(f"| {r[0]} | {r[1] / MB:.3f} MB | {(r[1] - STOP) / MB:.3f} MB | {r[2] / MB:.3f} MB | {r[3]} |")
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
