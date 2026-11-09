"""Write the Civic Line drawings' plate page for the stage B drawings board.

    python3 -I work/build/scripts/phase-2/civic_line_stage_b_plates.py

Reads the two drawing manifests, the pillar-fit manifest and the check results
kept beside the page, and writes
work/boards/phase-2/stage-b/drawings/civic-line/20261109_Civic-Line-Drawings-Plates.html.
Every drawing is an <img> of its own SVG at true size on Newsprint (no
inlined ids to collide), referenced by a path relative to the page.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import civic_line_stage_b_common as C  # noqa: E402

ROOT = C.ROOT
PAGE_DIR = os.path.join(ROOT, "work", "boards", "phase-2", "stage-b", "drawings", "civic-line")
PAGE = os.path.join(PAGE_DIR, "20261109_Civic-Line-Drawings-Plates.html")
CHK = os.path.join(PAGE_DIR, "checks")
INV = json.load(open(os.path.join(ROOT, "work/build/assets/civic-line/20261029_Civic-Line-Inventory.json")))
BY = {r["id"]: r for r in INV["icons"]}


def rel(p):
    return os.path.relpath(os.path.join(ROOT, p), PAGE_DIR)


def master(icon_id, ed="red-black"):
    r = BY[icon_id]
    key = "svg_red_black" if ed == "red-black" else "svg_black"
    name = r.get(key) or r["exports"][key]
    return f"work/build/assets/civic-line/{ed}/{name}"


# The naming test (drawings brief): each option at 48 px, no label, and what a
# first-time reader would most likely call it. The reader here is the icon
# designer, an agent standing in; the creative director repeats it.
NAMING = {
    ("CL-025", "A"): ("A large public building, most likely a city hall or a museum.", "label"),
    ("CL-025", "B"): ("A chamber or an auditorium with a stage; a reader who knows the House may say Congress.", "label"),
    ("CL-025", "C"): ("Two seating chambers, one larger than the other; with the label, the House and the Senate.", "label"),
    ("CL-014", "A"): ("A government building fenced in.", "near"),
    ("CL-014", "B"): ("A chamber or an arena behind a fence.", "label"),
    ("CL-014", "C"): ("A chamber or an arena behind a fence.", "label"),
    ("R-13", "A"): ("Two people, a building and an open book; the book pulls toward reading or a library.", "weak"),
    ("R-13", "B"): ("A chamber with two staff and a report: staff working for a legislature.", "label"),
    ("R-13", "C"): ("Two chambers with two staff and a report.", "label"),
    ("R-42", "A"): ("A building, a ballot box and a crate with an arrow; the ballot box reads as a public election.", "weak"),
    ("R-42", "B"): ("A chamber, a yes-and-no card and a parcel with a tag: a vote on goods.", "label"),
    ("R-42", "C"): ("Two chambers, a yes-and-no card and a parcel with a tag: a vote on goods.", "label"),
    ("CL-059", "A"): ("A bank, or a temple, sending money to a home and a factory.", "names"),
    ("CL-059", "B"): ("A bank vault sending money to a home and a factory.", "names"),
    ("CL-059", "C"): ("A safe paying out to a home and a factory.", "names"),
    ("R-48", "A"): ("A house or a school and a speaker at a lectern, set apart by a bracket; the pediment over a door reads as a house.", "label"),
    ("R-48", "B"): ("A panel of three and a speaker at a lectern, set apart by a bracket; some may say a debate.", "label"),
    ("R-48", "C"): ("A panel of three kept apart from a person at a desk, whose arrow stops at the bracket.", "near"),
    ("Testify", "A"): ("A hearing: a person at a microphone facing a panel.", "names"),
    ("Testify", "B"): ("A person at a microphone speaking up to a raised panel.", "names"),
    ("Testify", "C"): ("A panel and a microphone: a hearing, or a panel discussion.", "near"),
    ("Contact-An-Official", "A"): ("A person sending a message to someone at a desk.", "names"),
    ("Contact-An-Official", "B"): ("A phone line to someone at a desk: calling an office.", "names"),
    ("Contact-An-Official", "C"): ("A person talking to someone at a desk: a visit, or a help desk.", "near"),
}
VERDICT = {"names": "Names the subject", "near": "Names it nearly; the label settles it",
           "label": "Recognized with the label", "weak": "Misleads without the label (kept by DR-135)"}

NEAREST = {"Testify": ["CL-005", "CL-027"], "Contact-An-Official": ["CL-026", "CL-061"]}
# Settled drawings shown after the options, to compare (DR-152 asks for R-46 beside the Congress options).
NEIGHBORS = {"CL-025": [("R-46", "Draws the House from above; stays as drawn (DR-152)."),
                        ("R-03", "Draws a hemicycle of seats as dots.")],
             "CL-014": [("R-46", "CL-014 B's closest drawing on the look-alike check.")]}
CARD_NO = {"CL-025": 1, "CL-014": 2, "R-13": 3, "R-42": 4, "CL-059": 5, "R-48": 6, "Testify": 7,
           "Contact-An-Official": 8}
TITLES = {"CL-025": "CL-025 Congress", "CL-014": "CL-014 Entrenched Power", "R-13": "R-13 Congressional Capacity",
          "R-42": "R-42 Congressional Tariff Votes", "CL-059": "CL-059 Credit Allocation",
          "R-48": "R-48 Agency Independence", "Testify": "Testify (new)", "Contact-An-Official": "Contact an official (new)"}


def likeness_for(data, stem):
    f = stem + "-Black.svg"
    out = {}
    for c in data.get("closest", []):
        if c["a"] == f:
            out["closest"] = (c["b"].replace("20261109_", "").replace("-Black.svg", ""), c["likeness"], c["percentile"])
    for c in data.get("own", []):
        if c["a"] == f:
            out["own"] = (c["b"], c["likeness"])
    flags = [p for p in data.get("flagged", []) if f in (p["a"], p["b"])]
    out["flags"] = len(flags)
    return out


def sizes_cell(src, sizes, label, sub="", alt=""):
    imgs = "".join(f'<figure class="sz"><img src="{html.escape(rel(src))}" width="{s}" height="{s}" alt="{html.escape(alt)} at {s} px">'
                   f'<figcaption>{s}</figcaption></figure>' for s in sizes)
    return (f'<div class="opt"><div class="opt-h">{label}</div><div class="sizes">{imgs}</div>{sub}</div>')


def option_cell(o, lk):
    key = (o["id"], o["option"])
    nm, v = NAMING[key]
    dr = ""
    if o.get("within_dr135") is not None:
        dr = ('<p class="tag in">Within DR-135</p>' if o["within_dr135"] else '<p class="tag out">Outside DR-135</p>')
    fig = ""
    if "closest" in lk:
        b, l, pc = lk["closest"]
        fig += f'<p class="fig">Closest drawing: {html.escape(b)}, {l:.3f}, percentile {pc:g}'
        fig += ", flagged" if l >= 0.9127 else (", watch" if l >= 0.8708 else "") + "</p>"
    if "own" in lk:
        fig += f'<p class="fig">Own original: {lk["own"][1]:.3f}</p>'
    sub = (f'{dr}<p class="chg">{html.escape(o["change"])}</p>'
           f'<p class="nm"><span>At 48 px:</span> {html.escape(nm)}</p><p class="vd v-{v}">{VERDICT[v]}</p>{fig}')
    return sizes_cell(o["svg_red_black"], (128, 48, 24), f'Option {o["option"]}', sub, f'{o["name"]} option {o["option"]}')


def pillar_rows(fits, pxres):
    out = []
    for pid, name in (("CL-019", "Explain"), ("CL-020", "Track"), ("CL-021", "Connect"), ("CL-022", "Act")):
        mrow = lambda ed: "".join(
            f'<figure class="sz"><img src="{html.escape(rel(master(pid, ed)))}" width="{z}" height="{z}" alt="{name} master, {ed}, at {z} px">'
            f'<figcaption>{z}</figcaption></figure>' for z in (96, 48, 24, 16))
        cells = [f'<div class="opt"><div class="opt-h">Master</div><div class="sizes">{mrow("red-black")}</div>'
                 f'<div class="sizes short">{mrow("black")}</div><p class="chg">Red-black above, black below. The masters are '
                 f'drawn for 48 px and up; at 24 and 16 px their line falls under one pixel.</p></div>']
        for f in [x for x in fits if x["id"] == pid]:
            s = f["size_px"]
            res = pxres.get(os.path.basename(f["svg_black"]))
            figs = ""
            if res:
                one = res["scales"]["1x"]
                figs = (f'<p class="fig">Pixel-fit check at {s} px: {"pass" if res["scales"]["1x"]["pass"] and res["scales"]["2x"]["pass"] else "fail"}; '
                        f'{one["straight"]["fit"]} of {one["straight"]["total"]} straight edges on pixel edges, '
                        f'{round(one["soft_edges"]["share"] * 100)}% soft, ' + (f'smallest gap {one["gap"]["smallest_px"]:g} px, ' if one["gap"]["smallest_px"] is not None else "one connected part, ") +
                        f'counters {one["counters"]["drawn"]} kept {one["counters"]["open"]}</p>')
            enl = os.path.join("work/build/assets/pillar-pixel-fit/png", os.path.basename(f["svg_red_black"]).replace(".svg", ".png"))
            enl_b = enl.replace("-Red-Black.png", "-Black.png")
            body = (f'<div class="sizes">'
                    f'<figure class="sz"><img src="{html.escape(rel(f["svg_red_black"]))}" width="{s}" height="{s}" alt="{name} {s} px fit {f["fit"]}, red-black"><figcaption>{s}, red</figcaption></figure>'
                    f'<figure class="sz"><img src="{html.escape(rel(f["svg_black"]))}" width="{s}" height="{s}" alt="{name} {s} px fit {f["fit"]}, black"><figcaption>{s}, in use</figcaption></figure>'
                    f'<figure class="sz enl"><img class="px" src="{html.escape(rel(enl))}" width="{s * 4}" height="{s * 4}" alt="{name} {s} px fit {f["fit"]}, enlarged four times"><figcaption>4x, inspection only</figcaption></figure>'
                    f'<figure class="sz enl"><img class="px" src="{html.escape(rel(enl_b))}" width="{s * 4}" height="{s * 4}" alt="{name} {s} px fit {f["fit"]}, black, enlarged four times"><figcaption>4x, black</figcaption></figure>'
                    f'</div><p class="chg">{f["line_px"]} px line, {f["red_px"]} red and {f["black_px"]} black pixels.</p>{figs}')
            cells.append(f'<div class="opt wide"><div class="opt-h">{s} px, fit {f["fit"]}</div>{body}</div>')
        out.append(f'<section class="card" id="pillar-{pid.lower()}"><h3>Pillar fit: {pid} {name}</h3>'
                   f'<div class="row">{"".join(cells)}</div></section>')
    return "".join(out)


def main():
    m1 = json.load(open(os.path.join(ROOT, "work/build/assets/civic-line-redraws/20261109_Stage-B-Drawings-Manifest.json")))["options"]
    m2 = json.load(open(os.path.join(ROOT, "work/build/assets/civic-line-new-topics/20261109_Stage-B-Drawings-Manifest.json")))["options"]
    fits = json.load(open(os.path.join(ROOT, "work/build/assets/pillar-pixel-fit/20261109_Pillar-Pixel-Fit-Manifest.json")))["fits"]
    lr = json.load(open(os.path.join(CHK, "20261109_Likeness-Redraws.json")))
    ln = json.load(open(os.path.join(CHK, "20261109_Likeness-New-Topics.json")))
    pxres = {}
    for f in ("20261109_Pixel-Fit-16px-Fit-A.json", "20261109_Pixel-Fit-24px-Fit-A.json", "20261109_Pixel-Fit-24px-Fit-B.json"):
        for r in json.load(open(os.path.join(CHK, f)))["results"]:
            pxres[os.path.basename(r["file"])] = r
    cards = []
    for subj in ("CL-025", "CL-014", "R-13", "R-42", "CL-059", "R-48", "Testify", "Contact-An-Official"):
        opts = [o for o in m1 + m2 if o["id"] == subj]
        data = lr if subj in BY else ln
        cells = []
        if subj in BY:
            cells.append(sizes_cell(master(subj), (128, 48, 24), "Original master",
                                    '<p class="chg">October 29 master, kept as the record.</p>', f"{subj} original"))
        else:
            for nid in NEAREST[subj]:
                cells.append(sizes_cell(master(nid), (128, 48, 24), f"Nearest: {nid} {BY[nid]['label']}",
                                        '<p class="chg">Topic drawing it must not be read as.</p>', f"{nid} {BY[nid]['label']}"))
        for o in opts:
            cells.append(option_cell(o, likeness_for(data, o["stem"])))
        for nid, why in NEIGHBORS.get(subj, []):
            cells.append(sizes_cell(master(nid), (128, 48, 24), f"Neighbor: {nid} {BY[nid]['label']}",
                                    f'<p class="chg">{html.escape(why)}</p>', f"{nid} {BY[nid]['label']}"))
        cards.append(f'<section class="card" id="card-{CARD_NO[subj]}"><h3><span class="no">{CARD_NO[subj]}</span> {html.escape(TITLES[subj])}</h3>'
                     f'<div class="row">{"".join(cells)}</div></section>')
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Civic Line Drawings Plates</title>
<style>
:root {{ --newsprint: #DCD9D2; --charcoal: #121212; --red: #E63946; --stone: #5D636D; --deep-stone: #4E535B; --rule: #A3A19C; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: var(--newsprint); color: var(--charcoal); }}
body {{ font-family: "Inter", "Arial", sans-serif; font-size: 15px; line-height: 1.45; padding: 32px 24px 64px; }}
main {{ max-width: 1360px; margin: 0 auto; }}
h1, h2, h3 {{ font-family: "Inter Tight", "Arial", sans-serif; font-weight: 700; letter-spacing: -0.01em; margin: 0; }}
h1 {{ font-size: 30px; }}
h2 {{ font-size: 21px; margin: 40px 0 8px; padding-top: 16px; border-top: 2px solid var(--charcoal); }}
h3 {{ font-size: 17px; margin-bottom: 12px; }}
.lede {{ max-width: 68ch; margin: 8px 0 0; }}
.meta {{ color: var(--deep-stone); font-size: 13px; margin: 8px 0 0; }}
.card {{ padding: 20px 0 24px; border-top: 1px solid var(--rule); }}
.no {{ display: inline-block; min-width: 2.2em; font-variant-numeric: tabular-nums; color: var(--deep-stone); }}
.row {{ display: flex; flex-wrap: wrap; gap: 24px 28px; align-items: flex-start; }}
.opt {{ width: 280px; }}
.opt.wide {{ width: 320px; }}
.sizes.short {{ min-height: 0; }}
.opt-h {{ font-family: "Inter Tight", "Arial", sans-serif; font-weight: 700; font-size: 15px; }}
.sizes {{ display: flex; align-items: flex-end; gap: 16px; margin: 10px 0 6px; flex-wrap: wrap; min-height: 152px; }}
.sz {{ margin: 0; display: flex; flex-direction: column; align-items: center; gap: 4px; }}
.sz img {{ display: block; }}
.sz img.px {{ image-rendering: pixelated; }}
.sz figcaption {{ font-size: 13px; color: var(--deep-stone); font-variant-numeric: tabular-nums; }}
.tag {{ display: inline-block; margin: 6px 0 0; font-size: 13px; font-weight: 600; padding: 1px 6px; border: 1px solid var(--charcoal); }}
.tag.out {{ border-style: dashed; }}
.chg, .nm, .vd, .fig {{ margin: 6px 0 0; font-size: 13px; }}
.nm span {{ font-weight: 600; }}
.vd {{ font-weight: 600; }}
.v-weak {{ text-decoration: underline; text-decoration-thickness: 2px; }}
.fig {{ color: var(--deep-stone); font-variant-numeric: tabular-nums; }}
@media (max-width: 640px) {{ body {{ padding: 24px 16px 48px; }} .opt {{ width: 100%; }} }}
</style>
</head>
<body>
<main>
<h1>Civic Line drawings, stage B</h1>
<p class="lede">Every drawing is shown at true size on Newsprint, beside its original master or the topic drawing it must not be read as. Redraws and new topics show at 128, 48 and 24 px; their floor is 48 px (DR-136), and 24 px is shown only to compare. The pillar fits show at their own size beside the masters at 96, 48, 24 and 16 px, with a four-times enlargement for inspection only. The four dome drawings come as three matched sets (D2-503): set A keeps every other part of each drawing (DR-135), set B draws the House chamber from the gallery, and set C draws the two chambers.</p>
<p class="meta">Icon designer, Civic Line hand, November 9, 2026. Naming test: each option read at 48 px with no label by the icon designer, an agent standing in for a first-time reader; the creative director repeats it. Look-alike figures: the engineer's check at 24 px; flag at 0.913 (99th percentile of master pairs), watch from 0.871. Card numbers 1 to 8 follow the brief's order for these drawings; the board builder sets the board's own numbers. Notes: work/handoffs/phase-2/20261109_Stage-B-Civic-Line-Icons-Notes.md.</p>
<h2>The six redraws</h2>
{"".join(cards[:6])}
<h2>Testify and Contact an official</h2>
{"".join(cards[6:])}
<h2>Pixel-fit pillar icons</h2>
<p class="lede">Each fit is drawn pixel by pixel and keeps every feature and red placement of its master, with the red as its own shape. Under 48 px the black edition is the one in use (D2-497). At 24 px, fit A has a 2 px line and fit B a 1 px line. At 16 px there is one fit: a 2 px line there closes Connect's lens, Track's pin and lens, the book's doubled edge and Act's finger.</p>
{pillar_rows(fits, pxres)}
</main>
</body>
</html>
"""
    os.makedirs(PAGE_DIR, exist_ok=True)
    with open(PAGE, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(os.path.relpath(PAGE, ROOT), len(page))


if __name__ == "__main__":
    main()
