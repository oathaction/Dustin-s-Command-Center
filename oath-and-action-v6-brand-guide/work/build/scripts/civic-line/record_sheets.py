"""Parts C and D: the pillar-mark side by side for DR-04, and the size ladder.

    python3 -I record_sheets.py

C. qa/<date>_Pillar-Marks-Side-By-Side.svg and .png: the Gate 1 pillar marks
   (Direction A, approved as Y1) beside Civic Line CL-019 Explain, CL-020
   Track, CL-021 Connect and CL-022 Act, at 24, 48, 96 and 192 px. Direction A
   never got masters after Gate 1: DR-01 and DR-04 replaced it before Phase 2
   drew them. Its latest drawings are the Phase 1 sketch file
   work/boards/phase-1/symbols/20261021_Pillar-Sketches-Direction-A.svg. The
   record uses its filled cut, the approved geometric solid, drawn from the 24 px
   master at every size (a vector scale), in one color as marks sit in a row
   (G1-07). Labels are Inter outlines, so the SVG carries no font data.
D. qa/<date>_Civic-Line-Size-Ladder.png: all 122 red-black exports at 24, 32,
   48 and 64 px on Newsprint, in catalog order, labeled by ID.
Both render in Chromium at device scale 1, so every icon shows at its true
pixel size.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
import contact_sheets as CS  # noqa: E402  (text shaping and outlines)

DIR_A = os.path.join(C.ROOT, "work", "boards", "phase-1", "symbols", "20261021_Pillar-Sketches-Direction-A.svg")
PILLARS = [("explain", "CL-019", "Explain"), ("track", "CL-020", "Track"), ("connect", "CL-021", "Connect"), ("act", "CL-022", "Act")]
SIZES = [24, 48, 96, 192]


def direction_a_symbol(name):
    s = open(DIR_A, encoding="utf-8").read()
    m = re.search(rf'<symbol id="oa-sketch-a-filled-{name}-24" viewBox="0 0 24 24">(.*?)</symbol>', s, re.S)
    if not m:
        raise SystemExit(f"Direction A filled {name} 24 px not found in {DIR_A}")
    body = re.sub(r"<title>.*?</title>", "", m.group(1), flags=re.S)
    # one color: body and node in Charcoal, seat clear (the sketch's own defaults)
    body = body.replace('fill="currentColor"', f'fill="{C.CHARCOAL}"')
    body = body.replace('fill="var(--seat,none)"', 'fill="none"')
    body = body.replace('fill="var(--node,currentColor)"', f'fill="{C.CHARCOAL}"')
    return body.strip()


def export_body(row, edition, new_root):
    """Inner markup of a bare export with its ids moved under new_root, so
    every copy in one record file has its own ids."""
    s = open(C.edition_file(row, edition), encoding="utf-8").read().split("?>", 1)[-1]
    s = re.sub(r"<title>.*?</title>|<desc>.*?</desc>", "", s, flags=re.S)
    inner = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    return inner.replace(C.bare_root(row["id"], edition), new_root).strip()


def render(jobs):
    with tempfile.TemporaryDirectory() as d:
        jp = os.path.join(d, "jobs.json")
        json.dump(jobs, open(jp, "w"))
        r = subprocess.run(["node", C.RENDER_JS, jp], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("render failed:\n" + r.stderr[-2000:])


def pillar_record():
    inv = C.inventory_by_id()
    fonts = CS.Fonts()
    rows = [("Gate 1 pillar marks, Direction A (Y1), one color", "a"),
            ("Civic Line, black edition", "black"),
            ("Civic Line, red-black edition (DR-04)", "red-black")]
    pad, label_h, row_gap, col_gap, group_gap = 40, 26, 34, 24, 64
    group_w = sum(SIZES) + col_gap * (len(SIZES) - 1)
    W = pad * 2 + group_w * 4 + group_gap * 3
    row_h = label_h + 192 + 30
    top = 140
    H = top + len(rows) * (row_h + row_gap) + 40
    lines = [{"id": "title", "size": 100, "runs": [{"family": "Inter-700", "text": "Pillar marks for the record: Gate 1 Direction A beside Civic Line (DR-04)"}]},
             {"id": "sub", "size": 100, "runs": [{"family": "Inter-400", "text": "Actual sizes 24, 48, 96 and 192 px on Newsprint. Direction A is drawn from its Phase 1 sketch file, filled cut, 24 px master scaled. Civic Line is the traced master export."}]}]
    for k, (lab, _) in enumerate(rows):
        lines.append({"id": f"row{k}", "size": 100, "runs": [{"family": "Inter-600", "text": lab}]})
    for name, iid, word in PILLARS:
        lines.append({"id": f"p-{name}", "size": 100, "runs": [{"family": "Inter-700", "text": f"{word}"},
                                                              {"family": "Inter-400", "text": f"   Civic Line {iid}"}]})
    for s in SIZES:
        lines.append({"id": f"s{s}", "size": 100, "runs": [{"family": "Inter-400", "text": f"{s} px"}]})
    sh = CS.shape(lines)

    def txt(lid, size, x, base, fill=C.CHARCOAL, anchor="start"):
        a, b = CS.ink_extent(fonts, sh[lid]["chars"], size)
        dx = x - a if anchor == "start" else x - (a + b) / 2
        return f'<path fill="{fill}" d="{CS.text_path(fonts, sh[lid]["chars"], size, dx, base)}"/>'
    rid = "oa-civic-line-pillar-marks-side-by-side"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" id="{rid}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           "<title>Pillar marks side by side, Gate 1 Direction A and Civic Line</title>",
           "<desc>Record for decision DR-04. Labels are Inter converted to outlines.</desc>",
           f'<rect width="{W}" height="{H}" fill="{C.NEWSPRINT}"/>',
           txt("title", 22, pad, 44), txt("sub", 14, pad, 70)]
    defs = []
    for k, (lab, kind) in enumerate(rows):
        y0 = top + k * (row_h + row_gap)
        out.append(txt(f"row{k}", 14, pad, y0 + 16))
        for g, (name, iid, word) in enumerate(PILLARS):
            gx = pad + g * (group_w + group_gap)
            if k == 0:
                out.append(txt(f"p-{name}", 16, gx, 112))
            x = gx
            base_y = y0 + label_h + 192
            for s in SIZES:
                y = base_y - s
                if kind == "a":
                    out.append(f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 24 24">{direction_a_symbol(name)}</svg>')
                else:
                    out.append(f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 128 128">{export_body(inv[iid], kind, f"{rid}-{iid.lower()}-{kind}-{s}")}</svg>')
                if k == len(rows) - 1:
                    out.append(txt(f"s{s}", 12, x + s / 2, base_y + 22, anchor="middle"))
                x += s + col_gap
    out.append("</svg>")
    svg = "\n".join(o for o in out if o) + "\n"
    base = os.path.join(C.QA, f"{C.DATE}_Pillar-Marks-Side-By-Side")
    open(base + ".svg", "w", encoding="utf-8").write(svg)
    render([{"svg": svg, "w": W, "h": H, "bg": None, "out": base + ".png"}])
    Image.open(base + ".png").convert("RGB").save(base + ".png", optimize=True)
    print(f"wrote {os.path.relpath(base, C.ROOT)}.svg and .png ({W} x {H})")


def size_ladder():
    inv = C.load_inventory()["icons"]
    sizes = [24, 32, 48, 64]
    gap, cell_pad, label_h = 10, 12, 20
    cell_w = sum(sizes) + gap * (len(sizes) - 1) + cell_pad * 2
    cell_h = label_h + 64 + cell_pad * 2
    cols = 6
    top = 60
    nrows = (len(inv) + cols - 1) // cols
    W = cols * cell_w + 40
    H = top + nrows * cell_h + 20
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="Inter, sans-serif">',
           f'<rect width="{W}" height="{H}" fill="{C.NEWSPRINT}"/>',
           f'<text x="20" y="30" font-size="18" font-weight="600" fill="{C.CHARCOAL}">Civic Line size ladder: red-black exports at 24, 32, 48 and 64 px, actual size</text>',
           f'<text x="20" y="50" font-size="12" fill="{C.CHARCOAL}">Catalog order, left to right. Capped fit (DR-08): each icon grows toward 116 of 128 units by at most 1.25 times the shared scale; strokes run 2.68 to 3.35 units.</text>']
    missing = []
    for i, r in enumerate(inv):
        p = os.path.join(C.ASSETS, "red-black", r["exports"]["svg_red_black"])
        cx = 20 + (i % cols) * cell_w
        cy = top + (i // cols) * cell_h
        out.append(f'<text x="{cx + cell_pad}" y="{cy + cell_pad + 12}" font-size="12" font-weight="600" fill="{C.CHARCOAL}">{r["id"]}</text>')
        if not os.path.exists(p):
            missing.append(r["id"])
            out.append(f'<text x="{cx + cell_pad}" y="{cy + cell_pad + label_h + 40}" font-size="12" fill="{C.CHARCOAL}">not built yet</text>')
            continue
        x = cx + cell_pad
        base = cy + cell_pad + label_h + 64
        for s in sizes:
            body = export_body(r, "red-black", f"ladder-{r['id'].lower()}-{s}")
            out.append(f'<svg x="{x}" y="{base - s}" width="{s}" height="{s}" viewBox="0 0 128 128">{body}</svg>')
            x += s + gap
    out.append("</svg>")
    svg = "\n".join(out) + "\n"
    path = os.path.join(C.QA, f"{C.DATE}_Civic-Line-Size-Ladder.png")
    render([{"svg": svg, "w": W, "h": H, "bg": None, "out": path}])
    Image.open(path).convert("RGB").save(path, optimize=True)
    print(f"wrote {os.path.relpath(path, C.ROOT)} ({W} x {H}); not built: {missing or 'none'}")


if __name__ == "__main__":
    pillar_record()
    size_ladder()
