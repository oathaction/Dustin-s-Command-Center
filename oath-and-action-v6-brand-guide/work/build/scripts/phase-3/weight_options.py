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

Each row's ask is the bytes chapter 14 runs over its stop, less the page's room under 15.5 MB, never below zero.
"""
import argparse
import base64
import io
import json
import re
import sys
import zlib

MB = 1_000_000
STOP = 1.75 * MB
BUDGET = 15.5 * MB
FINISHED = 97
EXPANDER = 600     # bytes for the script that inflates a deflated island or table (DecompressionStream), an estimate


def deflate_b64(text):
    co = zlib.compressobj(9, zlib.DEFLATED, -15, 9)
    return len(base64.b64encode(co.compress(text.encode()) + co.flush()))


def plates(page):
    out = {}
    for m in re.finditer(r'<figure class="oac-fig" id="oac-(s-14-s\d\d)".*?</figure>', page, re.S):
        fig = m.group(0)
        tab = re.search(r'<div class="oac-tw".*?</table></div>', fig, re.S)
        isl = re.search(r'(<script type="application/json" data-oa-chart-data>)(.*?)(</script>)', fig, re.S)
        out[m.group(1)] = {"table": tab.group(0) if tab else "", "island": isl.group(2) if isl else ""}
    return out


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
         f"Chapter 01's {nph} shown photographs resampled to 1,200 px wide, frees {photos / MB:.3f} MB of the page"),
    ]
    out = {"page_bytes": rep["bytes"], "projected_page": rep["weight"]["projection"]["projected_bytes"], "room": round(room),
           "chapter_14_now": ch14, "stop": STOP, "plates": n, "island_saving_per_plate": round(isl_save),
           "table_and_island_saving_per_plate": round(both_save), "photo_saving": photos,
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
