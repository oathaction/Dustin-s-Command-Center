"""Concept 2, Moving part: write the concept board.

Run after the masters, assets and measure scripts: python3 -I icons_r2_moving_board.py
Writes work/boards/20261028_Icon-Concept-2-Moving-Part.html, standalone per
work/boards/20261021_Board-Conventions.md, with its assets in work/boards/phase-2/icons-r2/moving-part/.
Then check it with: node icons_r2_moving_board_check.js <board> <out.json> <screens_dir>
"""
import html as H
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_moving_assets as A  # noqa: E402
import icons_r2_moving_common as C  # noqa: E402
import icons_r2_moving_draw as D  # noqa: E402
import icons_r2_moving_measure as MEAS  # noqa: E402

BOARD = C.BOARDS / f"{C.DATE}_Icon-Concept-2-Moving-Part.html"
R = json.loads(MEAS.MEAS.read_text())
PILLARS = ["explain", "track", "connect", "act"]
SAY = {"explain": "A thing opened so you can see inside", "track": "A decision moving up through stages",
       "connect": "Two halves and the ground between them", "act": "A door you can walk through",
       "ballot": "A box with a slot and a marked paper going in", "bill": "A page with a folded corner and lines of text",
       "testify": "A person speaking at a microphone", "housing": "A house with a pitched roof and a door",
       "money": "Money changing hands", "loop": "Two nodes joined by a forward link and a return"}


def e(t):
    return H.escape(t, quote=True)


def src(p):
    return C.rel(p)


def icon(n, px, cw="Charcoal-Red", open_=False, alt=None, cls=""):
    size = C.best(px)
    a = D.LABELS[n] if alt is None else alt
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{src(C.variant_file(n, size, cw, open_))}" width="{px}" height="{px}" alt="{e(a)}"{c}>'


def pct(v, d=0):
    s = f"{v * 100:.{d}f}"
    if float(s) == 0:
        s = s.lstrip("-")
    return s.replace("-", "−")


def num(v, d=2):
    return f"{v:.{d}f}".replace("-", "−")


def ok(b):
    return '<span class="pass">Pass</span>' if b else '<span class="fail">Fail</span>'


def d96(n):
    return R["drawings"][f"{n}|Display|rest"]


def hm(n, s, st="rest"):
    return R["drawings"][f"{n}|{s}|{st}"]


def worst_pair(n, key="pairs16"):
    best = max(((v["score"], k) for k, v in R[key].items() if n in k.split("|")), key=lambda t: t[0])
    other = [x for x in best[1].split("|") if x != n][0]
    return best[0], other


def worst_watch(n):
    best = max(((v["score"], k) for k, v in R["watch"].items() if k.startswith(n + "|") and "ms-nearest" not in k), key=lambda t: t[0])
    _, nm, sz = best[1].split("|")
    return best[0], nm.replace("ms:", "Material ").replace("_", " "), sz


CSS = """
.board{max-width:1280px}
.lede{font-size:1.125rem;line-height:1.55;max-width:66ch}
.note{font-size:.9375rem;max-width:72ch}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1px solid var(--rule);margin:22px 0 8px}
.stats>div{padding:14px 16px;border-left:1px solid var(--rule);min-width:0}
.stats>div:first-child{border-left:0}
.stats b{display:block;font:800 1.5rem/1.1 var(--display);letter-spacing:-.02em;margin-bottom:6px;font-variant-numeric:tabular-nums}
.stats span{font-size:.875rem;line-height:1.45;color:var(--muted);display:block}
.toc{display:flex;flex-wrap:wrap;gap:6px 18px;margin:18px 0 0;font-weight:600;font-size:.9375rem}
.toc a{color:var(--fg)}
.ten{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:18px 12px;margin:24px 0 0}
.ten figure{margin:0;display:grid;gap:6px;justify-items:start}
.ten img{display:block;max-width:100%;height:auto}
.fig{font-size:.875rem;line-height:1.35}
.fig b{display:block;font-weight:600}
.fig span{color:var(--muted)}
.ptile{background:var(--charcoal);color:var(--newsprint);padding:22px 24px;margin-top:22px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.ptile figure{margin:0;display:grid;gap:8px;justify-items:start}
.ptile img{display:block;max-width:100%;height:auto}
.ptile .fig span{color:#C9C5BC}
.tblwrap{overflow-x:auto;margin:8px 0 6px;border:1px solid var(--rule)}
.tblwrap table{min-width:720px}
td img,th img{display:inline-block;vertical-align:middle}
td.n,th.n{font-variant-numeric:tabular-nums;white-space:nowrap}
.pass{font-weight:700}
.fail{font-weight:700;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:3px}
.study{display:inline-block;font:700 .8125rem/1.2 var(--body);letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--fg);padding:3px 7px;margin-bottom:10px}
.ms{font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;direction:ltr;font-feature-settings:'liga';-webkit-font-smoothing:antialiased;font-variation-settings:'FILL' 1,'wght' 400,'GRAD' 0,'opsz' 24;color:var(--fg);vertical-align:middle}
.ms.s24{font-size:24px;width:24px;height:24px;overflow:hidden}
.ms.s48{font-size:48px;width:48px;height:48px;overflow:hidden;font-variation-settings:'FILL' 1,'wght' 400,'GRAD' 0,'opsz' 48}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
.card{background:var(--surface);border:1px solid var(--rule);padding:14px;min-width:0;display:grid;gap:8px;align-content:start}
.card h3{font-size:1.0625rem}
.card p{margin:0;font-size:.875rem;line-height:1.45}
.card .row{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap}
.card .row img{display:block}
.cmp{display:grid;grid-template-columns:120px 1fr;gap:6px 12px;align-items:center}
.strip{display:flex;flex-wrap:wrap;gap:12px 16px;align-items:flex-end}
.strip img{display:block}
.strip.on-white{background:var(--white);padding:14px}
.pixgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.pixgrid .card .row{gap:8px}
.surf{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule)}
.surf>div{padding:14px;display:flex;flex-wrap:wrap;gap:10px;align-content:flex-start;min-width:0}
.surf .lab{width:100%;font:700 .8125rem/1.2 var(--body);letter-spacing:.06em;text-transform:uppercase}
.surf img{display:block}
.hgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.hgrid .card .row{gap:12px}
.ctx{display:grid;gap:22px}
.ctx figure{margin:0}
.ctx img{display:block;max-width:100%;height:auto;border:1px solid var(--rule)}
.ctx figcaption{font-size:.875rem;line-height:1.45;margin-top:8px;max-width:76ch}
.twocol{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;align-items:start}
.decision h3{margin:18px 0 6px;font-size:1.0625rem}
.decision p,.decision li{font-size:.9375rem}
.decision ol{padding-left:20px;margin:0}
.decision li{margin:0 0 10px}
.lists{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}
.lists ul{margin:0;padding-left:18px;font-size:.9375rem;line-height:1.5}
.lists li{margin:0 0 6px}
blockquote{margin:14px 0;padding:12px 16px;border-left:3px solid var(--fg);background:var(--surface);max-width:76ch}
code{font-size:.875rem}
@media (max-width:900px){.ten{grid-template-columns:repeat(3,minmax(0,1fr))}.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.stats>div:nth-child(3){border-left:0}
.ptile{grid-template-columns:repeat(2,minmax(0,1fr))}.hgrid,.twocol,.lists{grid-template-columns:1fr}.surf{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:480px){.ten{grid-template-columns:repeat(2,minmax(0,1fr))}.stats{grid-template-columns:1fr}.stats>div{border-left:0;border-top:1px solid var(--rule)}.stats>div:first-child{border-top:0}}
"""


def head():
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Icon Concept 2, Moving Part</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&amp;family=Inter:wght@400;600;700&amp;family=Lora:ital,wght@1,400&amp;display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,1,0&amp;display=block">
<link rel="stylesheet" href="board-base.css">
<style>{CSS}</style></head><body><main class="board">"""


def intro():
    s = R["sets"]
    figs = "".join(f'<figure>{icon(n, 96)}<figcaption class="fig"><b>{e(D.LABELS[n])}</b><span>{e(D.CLASS[n])}</span></figcaption></figure>' for n in D.ICONS)
    pil = "".join(f'<figure>{icon(n, 96, "Newsprint-Red")}<figcaption class="fig"><b>{e(D.LABELS[n])}</b><span>{e(D.STORY[n])}</span></figcaption></figure>' for n in PILLARS)
    red = [d96(n)["red_share_vector"] for n in D.ICONS]
    cr16 = s["crisp_16px"]
    return f"""
<p class="eyebrow">Phase 2, round two &middot; Icon concept 2 of 3 &middot; October 28, 2026</p>
<h1>Moving part</h1>
<p class="lede">Each subject is built from two to four solid pieces held apart by one constant cut. The red piece is the one that moves: the lid lifting, the top stage rising, the door leaf swinging, the ballot going in, the second banknote changing hands. Charcoal holds the structure around it.</p>
<p class="note">Proposal only. Nothing here changes a master. The creative director's stage 1 notes and the blind name test are applied first (section 3). Test 1, naming the icons blind, is the main session's to rerun on these masters.</p>
<div class="ten">{figs}</div>
<div class="ptile" aria-label="The four pillar marks on Charcoal">{pil}</div>
<div class="stats">
<div><b>0 of 45</b><span>pairs at 16 px score 0.60 or more on the Phase 1 similarity measure (D1-16). The closest pair scores {num(s['pairs16']['worst'][1])}.</span></div>
<div><b>{num(cr16['min'])} to {num(cr16['max'])}</b><span>pixel fit at 16 px, the share of inked pixels that render crisp (D1-17 asks for 0.60). At 24 px: {num(s['crisp_24px']['min'])} to {num(s['crisp_24px']['max'])}.</span></div>
<div><b>{pct(min(red))} to {pct(max(red))}%</b><span>red as a share of each icon's painted area, inside the 12 to 25 percent the notes set for this concept.</span></div>
<div><b>9 of 10</b><span>icons inside the weight band at 96 px. Feedback loop paints {pct(d96('loop')['density96'])} percent of the field and sits under it.</span></div>
</div>
<nav class="toc" aria-label="Sections"><a href="#s-bench">1. Beside Material Symbols</a><a href="#s-idea">2. The idea and the red</a><a href="#s-changes">3. What changed</a><a href="#s-grid">4. Grid and craft</a><a href="#s-sizes">5. Sizes</a><a href="#s-pixels">6. Hinted masters</a><a href="#s-row">7. In a row</a><a href="#s-surfaces">8. Surfaces</a><a href="#s-holders">9. Holders and app tile</a><a href="#s-use">10. Contexts</a><a href="#s-tests">11. The four tests</a><a href="#s-checks">12. Checks</a><a href="#s-alike">13. Look-alikes</a><a href="#s-rubric">14. Rubric</a><a href="#s-decide">15. Decisions</a><a href="#s-honest">16. Tested and not tested</a></nav>
"""


def sec_bench():
    rows = []
    for n in D.ICONS:
        g = MEAS.NEAREST[n]
        md = R["material_density"]
        rows.append(f"<tr><td><b>{e(D.LABELS[n])}</b></td><td>{icon(n, 24)}</td><td>{icon(n, 48)}</td>"
                    f'<td><span class="ms s24" aria-hidden="true">{g}</span></td><td><span class="ms s48" aria-hidden="true">{g}</span></td>'
                    f"<td><code>{g}</code></td><td class=\"n\">{pct(R['sets']['row24_density']['values'][n])}%</td><td class=\"n\">{pct(md[g + '|24'])}%</td></tr>")
    return f"""
<section id="s-bench"><h2>1. Beside the best: Material Symbols at 24 and 48 px</h2>
<p class="study">Study</p>
<p class="note">Each icon sits beside the nearest Material Symbols glyph, the Rounded style, filled, at weight 400, the closest Google set to a filled family. Material Symbols is Apache 2.0 and loads here through Google Fonts (D1-19). SF Symbols stays out of the file, since its license ties it to Apple platforms. Painted share is the inked share of the 24 px cell, measured from Chromium renders.</p>
<div class="tblwrap"><table><thead><tr><th>Icon</th><th>Ours, 24 px</th><th>Ours, 48 px</th><th>Material, 24 px</th><th>Material, 48 px</th><th>Glyph</th><th class="n">Ours, painted</th><th class="n">Material, painted</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="note">At 24 px Material's filled glyphs paint {pct(min(R['material_density'][g + '|24'] for g in MEAS.NEAREST.values()))} to {pct(max(R['material_density'][g + '|24'] for g in MEAS.NEAREST.values()))} percent of the cell and these icons {pct(min(R['sets']['row24_density']['values'].values()))} to {pct(max(R['sets']['row24_density']['values'].values()))} percent, a little lighter, with one cut where Material uses an outline or a knock-out. Material draws for system tasks, so for three subjects its nearest glyph is a neighbor: <code>unarchive</code> for Explain, <code>join</code> for Connect and <code>cycle</code> for Feedback loop.</p>
</section>"""


def sec_idea():
    cards = []
    for n in D.ICONS:
        cards.append(f'<div class="card"><div class="row">{icon(n, 96)}{icon(n, 40, "Charcoal")}{icon(n, 40, "Charcoal-No-Red")}</div>'
                     f'<h3>{e(D.LABELS[n])}</h3><p><b>Says:</b> {e(SAY[n])}.</p><p>{e(D.REASON[n])}</p></div>')
    return f"""
<section id="s-idea"><h2>2. The idea and the red</h2>
<p class="note">The brand's central idea is the hinge, a promise followed by action. Here every subject has one part that moves, and that part is red. It nests against a Charcoal piece across the cut, so Charcoal draws most of its outline and the subject still reads with the red turned to ink or removed (the second and third drawings in each card). Rule 05.3 governs, as D2-01 words it:</p>
<blockquote>"An icon's red accent counts as signature red when the icon stands alone, as an app tile, an avatar or a single feature icon. In a row or a menu, icons go one color and only the current one keeps its red."</blockquote>
<div class="cards">{''.join(cards)}</div>
</section>"""


CHANGES = {
    "explain": "The lid is the size of the notch it left. It hinges on the corner nearest the node, lifts 0.75 units and turns 20 degrees, with the 1.5-unit cut along its hinge side. The blind test read the stage 1 drawing as an app icon with a notification badge.",
    "track": "Three stages of equal rise and run climb from y 4 to 20, so the full-width slab is gone. The node rests in the joint between the first two stages. The red top stage takes the full rise and rests on a shelf one cut lower, which brings red to 15 percent. The blind test read a platform.",
    "connect": "The bridge is a bar across a 5-unit gap, its ends seated in slots in both halves, the node knocked out at its center. The bar is 4.5 units tall where the notes asked for about 3, so the 3-unit knock-out keeps 0.75-unit walls. The blind test read a record button.",
    "act": "Red falls from 48 to 22 percent. The leaf narrows to 3.5 units at its free edge, the node becomes its hinge pin, and a 2-unit Charcoal threshold runs under the opening. The full lintel stays and waits on Dustin's named approval.",
    "ballot": "The slot moves to the box's top edge and the paper's lower third sinks behind the box's face. The paper narrows to 5 units, and its oval knock-out is 3 by 2.2 units.",
    "bill": "The fold's top point sits 1.5 units below the page's top edge, so it reads as a fold.",
    "testify": "The microphone moves 0.75 units toward the face, its head at mouth height. The sound ring between them sets the distance, so it stops short of the full unit.",
    "housing": "Still a house with a pitched roof and a door. The body narrows to 13 units under 18-unit eaves and the door moves to the center, because the 16 px similarity check scored the stage 2 draft 0.68 against Ballot. The window goes.",
    "money": "A pair of banknotes replaces the hand and coin: a Charcoal note with its center disc knocked out, and a red note sliding out from behind it, turned 12 degrees. The front note rises to the field's center, which keeps it clear of Track and Ballot at 16 px. The blind test read a person on a bed.",
    "loop": "Two nodes on the vertical axis, a straight Charcoal forward link with a solid arrowhead, and a red return arc whose arrowhead enters the first node. The notes put the nodes on the horizontal center line; drawn that way it read as a face, so it stands upright. Red is 24.7 percent of its paint.",
}


def sec_changes():
    rows = "".join(f'<tr><td><b>{e(D.LABELS[n])}</b></td><td><img src="{src(C.OUT / "stage-1" / f"{C.DATE}_Moving-Part-{D.FILE_NAME[n]}-Display.svg")}" width="96" height="96" alt="{e(D.LABELS[n])}, stage 1"></td>'
                   f'<td>{icon(n, 96, alt=D.LABELS[n] + ", stage 2")}</td><td>{e(CHANGES[n])}</td></tr>' for n in D.ICONS)
    return f"""
<section id="s-changes"><h2>3. What changed after the stage 1 review</h2>
<p class="note">Stage 1 on the left, as the creative director reviewed it, and stage 2 on the right, both at 96 px. The notes set a red ceiling of 25 percent for this concept, so a moving piece keeps its presence. Three changes depart from the notes and go back to the creative director: Connect's taller bar, Feedback loop standing upright, and Housing redrawn after the notes said to keep it.</p>
<div class="tblwrap"><table><thead><tr><th>Icon</th><th>Stage 1</th><th>Stage 2</th><th>What changed and why</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>"""


def sec_grid():
    rows = [("Grid", "Round one's 24-unit grid, 2-unit padding, live area 2 to 22. Keylines: circle 20, square 18, portrait 16 by 20, landscape 20 by 16."),
            ("Pieces", "Two to four solid pieces per icon from the kit: square, rectangle, disc, half disc, quarter ring, stadium and 45 degree triangle."),
            ("Cut", "1.5 units in the display master, 2 px at 24 px, 1 px at 16 px, the same on every side of every piece."),
            ("Corners", "Convex corners take a 1-unit radius in the display master and stay square in the hinted masters. Concave corners stay square. Arrowhead corners take half a unit, an optical correction, since a full unit blunts an acute point."),
            ("Counters", "3 units or more at 24 units. Two knock-outs sit under it and are flagged in section 12: Ballot's oval mark (2.2 units tall) and the cuts that set Bill's text lines and Campaign money's corner marks (1.5 units, the cut itself)."),
            ("Node", "3 units across in the display master, with a bite of the node plus the cut around it, Direction A's 6-unit seat. It is ink in Explain, Track and Act and a Newsprint knock-out in Connect, where it falls on red. At 24 px it is a 4 px disc; at 16 px a 2 px square, with the bite widened so the square's corners keep a full cut."),
            ("Red", "One piece, 12 to 25 percent of the painted area. It is the one piece allowed off the 90 degree grid, turned up to 20 degrees, and it moves no more than 2 units from the gap it left."),
            ("Weight", "Ink and red together paint 24 to 32 percent of the field at 96 px, within 15 percent of the set's median."),
            ("Hinting", "The 24 px master is the drawing redrawn with a 2-unit cut and square corners. The 16 px master is the display geometry scaled by 2/3, which turns the 1.5-unit cut into 1 px. Horizontal and vertical edges move to whole pixels, both sides of each cut together. Turned and curved edges stay true vectors. Feedback loop at 24 and 16 px and Testify at 16 px are drawn by hand in whole pixels."),
            ("Files", "<code>20261028_Moving-Part-&lt;Icon&gt;-Display.svg</code>, <code>-24px.svg</code> and <code>-16px.svg</code>, each with an <code>-Open</code> row-state twin. Paths <code>ink</code> and <code>accent</code>; the hinted open masters add an unfilled <code>keyline</code>.")]
    body = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows)
    return f"""
<section id="s-grid"><h2>4. Grid and craft rules</h2>
<div class="tblwrap"><table><tbody>{body}</tbody></table></div>
</section>"""


def sec_sizes():
    rows = []
    for px in (16, 24, 48, 96):
        rows.append(f'<h3 style="margin:14px 0 8px">{px} px</h3><div class="strip">{"".join(icon(n, px) for n in D.ICONS)}</div>')
    white = "".join(icon(n, 24) for n in D.ICONS) + "".join(icon(n, 16) for n in D.ICONS)
    return f"""
<section id="s-sizes"><h2>5. The ten icons at 16, 24, 48 and 96 px</h2>
<p class="note">At 16 px each image is the 16 px master, at 24 px the 24 px master, and at 48 and 96 px the display master, all at true size on Newsprint.</p>
{''.join(rows)}
<h3 style="margin:18px 0 8px">On White, 24 and 16 px</h3><div class="strip on-white">{white}</div>
</section>"""


def sec_pixels():
    cards = []
    for n in D.ICONS:
        imgs = []
        for s, k in (("24px", 8), ("16px", 8)):
            for o in (False, True):
                f = C.PX / f"{C.DATE}_Moving-Part-{D.FILE_NAME[n]}-{s}{'-Open' if o else ''}.png"
                U = C.UNITS[s]
                imgs.append(f'<figure style="margin:0"><img class="pix" src="{src(f)}" width="{U * 4}" height="{U * 4}" alt="{e(D.LABELS[n])}, {s.replace("px", " px")}{", row state" if o else ""}, magnified 4 times">'
                            f'<figcaption class="cap">{s.replace("px", " px")}{" open" if o else ""}</figcaption></figure>')
        d = hm(n, "16px")
        cards.append(f'<div class="card"><h3>{e(D.LABELS[n])}</h3><div class="row">{"".join(imgs)}</div>'
                     f'<p>Pixel fit {num(hm(n, "24px")["crisp"])} at 24 px and {num(d["crisp"])} at 16 px. Smallest cut {num(hm(n, "24px")["min_gap_px"], 1)} px and {num(d["min_gap_px"], 1)} px.</p></div>')
    return f"""
<section id="s-pixels"><h2>6. The 16 and 24 px masters, magnified without smoothing</h2>
<p class="note">Each image is a Chromium render at 1x, magnified 4 times with no smoothing, at rest and in the row state with its keyline. The red pieces that turn off the grid (Explain's lid, the second banknote, Testify's sound at 24 px) and the curved Charcoal pieces stay true vectors, so their edges carry gray pixels by design. Pixel fit counts the share of inked pixels that render crisp.</p>
<div class="pixgrid">{''.join(cards)}</div>
</section>"""


def sec_row():
    cur = "".join(icon(n, 24, "Charcoal-Red-Keyline", open_=True) for n in D.ICONS)
    idle = "".join(icon(n, 24, "Charcoal") for n in D.ICONS)
    cur16 = "".join(icon(n, 16, "Charcoal-Red-Keyline", open_=True) for n in D.ICONS)
    idle16 = "".join(icon(n, 16, "Charcoal") for n in D.ICONS)
    big = "".join(f'<figure style="margin:0">{icon(n, 96, "Charcoal-Red", open_=True)}<figcaption class="cap">{e(D.LABELS[n])}</figcaption></figure>' for n in D.ICONS)
    return f"""
<section id="s-row"><h2>7. In a row: idle and current</h2>
<p class="note">Idle icons go one color, and the cut still shows the moving part. The current icon keeps its red with a 1 px Charcoal keyline at 16 and 24 px on Newsprint, since red on Newsprint measures {num(R['contrast']['Red on Newsprint'])}:1. The keyline stops a pixel short of any Charcoal piece, so at 16 px the 1 px cut stays open. The red piece moves one step further open, 1 px at 24 and 16 px, and the label goes bold. On Charcoal the red needs no keyline ({num(R['contrast']['Red on Charcoal'])}:1). On Prussian the icons are White with no red, and the current one shows by its open piece and its bold label.</p>
<figure style="margin:14px 0"><img src="{src(C.CONTEXT / f'{C.DATE}_Moving-Part-Context-1-Menu-Row.png')}" width="560" height="156" alt="The four pillars in a menu row on Newsprint, Charcoal and Prussian, Track current" style="max-width:100%;height:auto;display:block"><figcaption class="cap">The pillar menu row at 24 px, Track current. Chromium render at 1x.</figcaption></figure>
<h3 style="margin:16px 0 8px">All ten idle, then all ten current, at 24 px</h3><div class="strip">{idle}</div><div class="strip" style="margin-top:10px">{cur}</div>
<h3 style="margin:16px 0 8px">At 16 px</h3><div class="strip">{idle16}</div><div class="strip" style="margin-top:10px">{cur16}</div>
<h3 style="margin:16px 0 8px">The open step in the display master, 2 units, at 96 px</h3><div class="strip">{big}</div>
<p class="note">The motion chapter animates this step. Campaign money's note lifts 1.6 units, short of the full 2, so its corner stays inside the live area. In the open state Act, Campaign money and Feedback loop carry more than 25 percent red; the ceiling applies to the icon at rest.</p>
</section>"""


def sec_surfaces():
    blocks = []
    for lab, cls, cw in (("Newsprint", "s-newsprint", "Charcoal-Red"), ("White", "s-white", "Charcoal-Red"), ("Charcoal", "s-charcoal", "Newsprint-Red"), ("Prussian, no red", "s-prussian", "White")):
        blocks.append(f'<div class="{cls}"><span class="lab">{lab}</span>{"".join(icon(n, 48, cw) for n in D.ICONS)}</div>')
    c = R["contrast"]
    return f"""
<section id="s-surfaces"><h2>8. On all four surfaces</h2>
<div class="surf">{''.join(blocks)}</div>
<p class="note">Ink measures {num(c['Charcoal ink on Newsprint'])}:1 on Newsprint, {num(c['Charcoal ink on White'])}:1 on White, {num(c['Newsprint ink on Charcoal'])}:1 on Charcoal and {num(c['White ink on Prussian'])}:1 on Prussian. Red measures {num(c['Red on Newsprint'])}:1 on Newsprint, {num(c['Red on White'])}:1 on White and {num(c['Red on Charcoal'])}:1 on Charcoal, so on Newsprint no subject depends on the red piece's outer edge (test 2).</p>
</section>"""


def sec_holders():
    shapes = []
    for shape in A.SHAPES:
        imgs = "".join(f'<img src="{src(A.tile_file(n, shape, color, 96))}" width="96" height="96" alt="{e(D.LABELS[n])}, {shape.replace("-", " ").lower()}, {color}">'
                       for color in A.TILE for n in ("act",))
        shapes.append(f'<div class="card"><h3>{shape.replace("-", " ")}{" (leads)" if shape == "Rounded-Square" else (" (avatars)" if shape == "Circle" else "")}</h3><div class="row">{imgs}</div></div>')
    lead = {}
    for color in A.TILE:
        lead[color] = "".join(f'<img src="{src(A.tile_file(n, "Rounded-Square", color, 96))}" width="96" height="96" alt="{e(D.LABELS[n])}, rounded square, {color}">' for n in D.ICONS)
    small = "".join(f'<img src="{src(A.tile_file(n, "Rounded-Square", "Charcoal", 40))}" width="40" height="40" alt="{e(D.LABELS[n])}, 40 px tile">' for n in D.ICONS)
    t = R["tiles"]
    return f"""
<section id="s-holders"><h2>9. Holders and the app tile</h2>
<p class="note">Round one's geometry: the 24-unit field is 60 percent of the holder's side and the 20-unit live area half of it. The rounded square is a true superellipse, exponent 5, and it leads, after the two-tone reference. The circle serves avatars. Each holder comes in a Charcoal tile with a Newsprint icon and red, a Newsprint tile with a Charcoal icon and red (G1-09), and a Prussian tile in White with no red.</p>
<div class="hgrid">{''.join(shapes)}</div>
<h3 style="margin:18px 0 8px">All ten in the rounded square: Charcoal, Newsprint, Prussian</h3>
<div class="strip">{lead['Charcoal']}</div><div class="strip" style="margin-top:10px">{lead['Newsprint']}</div><div class="strip" style="margin-top:10px">{lead['Prussian']}</div>
<h3 style="margin:18px 0 8px">At 40 px, with the 24 px master at 1:1</h3><div class="strip">{small}</div>
<h3 style="margin:22px 0 8px">The 1024 px app tile: glyph scale</h3>
<div class="twocol"><figure style="margin:0"><img src="{src(C.APP / f'{C.DATE}_Moving-Part-App-Tile-Glyph-Test.png')}" width="1180" height="548" alt="Act as an app tile with its glyph at 56, 62 and 66 percent of the side, at 180, 60 and 29 px on light and dark wallpaper" style="max-width:100%;height:auto;display:block;border:1px solid var(--rule)"><figcaption class="cap">Glyph live area at 56, 62 and 66 percent of the side, each at 180, 60 and 29 px.</figcaption></figure>
<div><img src="{src(A.app_file())}" width="240" height="240" alt="The chosen app tile, Act on a Charcoal superellipse, at 240 px"><p class="note" style="margin-top:10px"><b>Chosen: 66 percent.</b> At 29 px the lintel and the threshold still render as lines and the hinge pin as a dot; at 56 percent they thin to gray. At 180 px the 66 percent glyph keeps a margin of {pct(t['app-1024']['margin_share'])} percent of the side. Act carries the tile, as in round one: a door you can walk through is the brand's promise followed by action.</p></div></div>
</section>"""


CTX = [("1-Menu-Row", 560, "1. The four pillars in a menu row on Newsprint, Charcoal and Prussian at 24 px, Track current."),
       ("2-Topic-List", 420, "2. A topic list of all ten at 24 px with labels, Campaign money current."),
       ("3-Article-Header", 1440, "3. An article header at 1440 px with Bill as a 64 px feature icon in signature red. Shown here at the board's width; the image is a 1440 px render. Headline and dek are illustrative."),
       ("4-Avatar", 760, "4. A social avatar: the 400 px master (Act on a Charcoal circle, live area at 56 percent of the diameter) shown at 200, 72 and 40 px. The handle is illustrative."),
       ("5-Social-Card", 1080, "5. A social card at 1080 by 1350 px, shown at a third: Ballot large in a Newsprint rounded square, with one working red, the rule above the eyebrow. Copy is illustrative."),
       ("6-Atlas-Legend", 380, "6. An atlas legend at 16 px beside 13 px text, Feedback loop first. In a list the icons go one color; the selected entry keeps its red with the keyline."),
       ("7-Tracker-Row", 900, "7. Tracker table rows at 16 px beside filled, half and open status marks. Bill numbers, dates and steps are illustrative."),
       ("8-App-Tile", 620, "8. The app tile at 180, 120, 60 and 29 px on a light and a dark wallpaper.")]


def sec_use():
    from PIL import Image
    figs = []
    for key, w, cap in CTX:
        p = C.CONTEXT / f"{C.DATE}_Moving-Part-Context-{key}.png"
        im = Image.open(p)
        disp = min(im.width, 1200) if key != "5-Social-Card" else 360
        h = round(im.height * disp / im.width)
        figs.append(f'<figure><img src="{src(p)}" width="{disp}" height="{h}" alt="{e(cap)}"><figcaption>{e(cap)}</figcaption></figure>')
    return f"""
<section id="s-use"><h2>10. In use: the eight contexts</h2>
<p class="note">Each context is a Chromium render at device scale 1, with the board's fonts loaded from the guide's extracted files. The 16 and 24 px icons in them are the hinted masters; everything 48 px and up is the display master.</p>
<div class="ctx">{''.join(figs)}</div>
</section>"""


def sec_tests():
    cover_rows = []
    for n in D.ICONS:
        cells = []
        for s, px in (("48px", 48), ("24px", 24), ("16px", 16)):
            cells.append(f'<td>{icon(n, px)} {icon(n, px, "Charcoal")} {icon(n, px, "Charcoal-No-Red")}</td>')
        pru = f'<td style="background:var(--prussian)">{icon(n, 48, "White")} {icon(n, 24, "White")}</td>'
        res = R["cover"]
        flags = ", ".join(f"{s.replace('px', ' px')}: {res[f'{n}|{s}']['nearest_other_score']:.2f} to {D.LABELS[res[f'{n}|{s}']['nearest_other']]}" for s in ("16px", "24px", "48px") if not res[f"{n}|{s}"]["pass_proxy"])
        cover_rows.append(f"<tr><td><b>{e(D.LABELS[n])}</b></td>{''.join(cells)}{pru}<td>{e(flags) if flags else 'Under 0.60 at all three sizes'}</td></tr>")
    twox = "".join(f'<figure style="margin:0">{icon(n, 192)}<figcaption class="cap">{e(D.LABELS[n])}</figcaption></figure>' for n in D.ICONS)
    row24 = "".join(icon(n, 24, "Charcoal") for n in D.ICONS)
    row48 = "".join(icon(n, 48, "Charcoal") for n in D.ICONS)
    s = R["sets"]
    return f"""
<section id="s-tests"><h2>11. The four tests</h2>
<h3>Test 1. Name it</h3>
<p class="note">The main session reruns the blind name test on these finished masters; it is not run here. On the stage 1 sheet (P) this concept passed Bill, Housing, Ballot and Testify, failed Campaign money ("a person reclining on a bed"), read Feedback loop first as reload or sync and Explain as an app icon with a badge, and matched all four pillar marks after one reading of their stories, with Track read as a platform. Section 3 shows each redraw. Until readers can be tested (Q-13), this blind read stands in for them.</p>
<h3 style="margin-top:20px">Test 2. Cover the red</h3>
<p class="note">For each size: as drawn, the red turned to ink, the red removed; then White on Prussian. The last column is a shape proxy for the naming: the Phase 1 similarity of the red-removed render to the nearest other icon in its full form, which should stay under 0.60. My reading by eye follows the table.</p>
<div class="tblwrap"><table><thead><tr><th>Icon</th><th>48 px</th><th>24 px</th><th>16 px</th><th>White on Prussian</th><th>Proxy over 0.60</th></tr></thead><tbody>{''.join(cover_rows)}</tbody></table></div>
<p class="note">My reading by eye: with the red turned to ink every icon keeps its name at all three sizes. With the red removed, Ballot becomes an empty box with a slot, which may read as a tray or inbox, and Track loses its top stage and reads as two steps; both are where the proxy flags them. Campaign money without its red note is still one banknote, and Feedback loop without its return is a one-way link between two nodes, which keeps its nodes and loses the loop. The proxy misses that last one, which the main session's naming should decide.</p>
<h3 style="margin-top:20px">Test 3. Hold up at 2x</h3>
<div class="strip">{twox}</div>
<p class="note">At 192 px: one cut weight in every drawing ({num(min(d96(n)['min_gap'] for n in D.ICONS))} units everywhere, and {num(s['min_gap_24px'], 2)} px and {num(s['min_gap_16px'], 2)} px at the smallest in the hinted masters); counters at 3 units or more except the two noted in section 4; by eye, curves meet straight edges cleanly. Nine of ten sit in the weight band, all ten inside the center-of-mass limit, and every hinted master passes pixel fit (sections 6 and 12).</p>
<h3 style="margin-top:20px">Test 4. Beside the best</h3>
<p class="note">Section 1 sets each icon beside Material Symbols at 24 and 48 px. Below, all ten in one color at 24 and 48 px, the way a row shows them, with no wordmark on the page. The weight spread at 24 px runs {pct(min(s['row24_density']['values'].values()))} to {pct(max(s['row24_density']['values'].values()))} percent of the cell; Ballot is the heaviest and Feedback loop the lightest, both outside 15 percent of the median.</p>
<div class="strip" style="margin-top:8px">{row24}</div><div class="strip" style="margin-top:12px">{row48}</div>
</section>"""


def sec_checks():
    rows = []
    for n in D.ICONS:
        d = d96(n)
        cx, cy = d["centroid96"]
        com_ok = max(abs(cx), abs(cy)) <= 0.12
        band = R["sets"]["density96"]["band"]
        bp, bo = worst_pair(n)
        ws, wn, wsz = worst_watch(n)
        tiles = [v for k, v in R["tiles"].items() if k.startswith(n + "-")]
        live = all(v["in_live_area"] for v in tiles)
        circ = all(v.get("in_circle_safe", True) for v in tiles)
        cnt = ", ".join(num(c, 1) for c in d["counters"]) or "None"
        rows.append(
            f"<tr><td><b>{e(D.LABELS[n])}</b></td>"
            f"<td class=\"n\">{pct(d['density96'], 1)}% {ok(band[0] <= d['density96'] <= band[1])}</td>"
            f"<td class=\"n\">{pct(d['red_share_vector'], 1)}% {ok(0.12 <= d['red_share_vector'] <= 0.25)}</td>"
            f"<td class=\"n\">{pct(cx, 1)}, {pct(cy, 1)}% {ok(com_ok)}</td>"
            f"<td class=\"n\">{num(hm(n, '24px')['crisp'])} / {num(hm(n, '16px')['crisp'])} {ok(hm(n, '24px')['crisp'] >= 0.6 and hm(n, '16px')['crisp'] >= 0.6)}</td>"
            f"<td class=\"n\">{num(bp)} {e(D.LABELS[bo])}</td>"
            f"<td class=\"n\">{num(ws)} {e(wn)}, {wsz} px</td>"
            f"<td class=\"n\">{cnt}</td>"
            f"<td>{'Inside' if live else 'Round overshoot at 96 px'}{'' if circ else ', outside the circle'}</td></tr>")
    s = R["sets"]
    c = R["contrast"]
    crows = "".join(f'<tr><td>{e(k)}</td><td class="n">{num(v)}:1</td></tr>' for k, v in c.items())
    return f"""
<section id="s-checks"><h2>12. Checks on every drawing</h2>
<p class="note">Weight is the painted share of the field at 96 px, with a band of 15 percent either side of the median ({pct(s['density96']['band'][0], 1)} to {pct(s['density96']['band'][1], 1)} percent). Center of mass is the 96 px render's offset from the field's center, with a limit of 12 percent. Pixel fit is the crisp share at 24 and 16 px (D1-17, 0.60). Closest pair is the icon's highest similarity score against the other nine at 16 px (D1-16, under 0.60). Closest look-alike is its highest score against letters, the numeral pair "01", V5 marks and the Material Symbols system glyphs the name test bans; section 13 shows the ones over 0.60. Counters are the knock-outs' smallest sides in units.</p>
<div class="tblwrap"><table><thead><tr><th>Icon</th><th class="n">Weight</th><th class="n">Red</th><th class="n">Center of mass</th><th class="n">Pixel fit, 24 / 16</th><th class="n">Closest pair</th><th class="n">Closest look-alike</th><th class="n">Counters</th><th>Holder safe area</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="note">Nine icons sit inside the live area of all nine holders at 40 and 96 px, and all ten sit inside the circle's safe radius (0.40 of the diameter). Feedback loop's nodes overshoot the live area by the 0.25 units a round form is allowed, which shows at 96 px. The avatar's ink reaches {pct(R['tiles']['avatar-400']['r_max_share'], 1)} percent of its diameter from the center. In the vector pixel-fit test of Phase 1 (axis edges and large curve extremes on whole pixels), the hinted masters score {num(s['vector_pixel_fit_24px'])} at the lowest at 24 px and {num(s['vector_pixel_fit_16px'])} at 16 px; the misses are the turned red pieces and arcs, which the test exempts only in part.</p>
<h3 style="margin-top:16px">Contrast</h3>
<div class="tblwrap"><table style="min-width:420px"><thead><tr><th>Pair</th><th class="n">Ratio</th></tr></thead><tbody>{crows}</tbody></table></div>
</section>"""


def sec_alike():
    over = [k for k in R["sets"]["watch_over_060"]]
    rows = []
    for k in over:
        n, nm, sz = k.split("|")
        sc = R["watch"][k]["score"]
        if nm.startswith("ms:"):
            g = nm[3:]
            ref = f'<span class="ms s{24 if sz == "24" else 24}" aria-hidden="true">{g}</span>'
            label = f"Material <code>{g}</code>"
        else:
            glyph = {"letter L": ("L", "800 24px/1 'Inter Tight'"), "letter C": ("C", "800 24px/1 'Inter Tight'"), "letter D": ("D", "800 24px/1 'Inter Tight'"),
                     "copyright sign": ("\u00a9", "700 24px/1 Inter"), "chapter number 01": ("01", "800 24px/1 'Inter Tight'")}.get(nm)
            ref = f'<span aria-hidden="true" style="font:{glyph[1]}">{glyph[0]}</span>' if glyph else ""
            label = e(nm)
        rows.append(f'<tr><td><b>{e(D.LABELS[n])}</b></td><td>{icon(n, int(sz))} {icon(n, 24 if sz == "16" else 48)}</td><td>{ref}</td><td>{label}</td><td class="n">{sz} px</td><td class="n">{num(sc, 2)}</td></tr>')
    return f"""
<section id="s-alike"><h2>13. Look-alikes over 0.60</h2>
<p class="note">The Phase 1 measure compares filled silhouettes and blurred tone, so at 16 px any filled, bottom-heavy shape scores high against Material's filled bell. These scores say where to look, and the name test decides. By eye, the risks worth carrying to the main session are Explain beside <code>app_badging</code> at 16 px, the creative director's badge worry in another form, and Bill beside the letter L. Connect beside the copyright sign at 16 px repeats a round one watch. Housing, Ballot and Campaign money beside the bell, the inbox, the storefront, the pause bars and the wallet read as their own subjects to me at 24 px; the wallet is a fair second read for a banknote.</p>
<div class="tblwrap"><table><thead><tr><th>Icon</th><th>Ours</th><th>Reference, 24 px</th><th>Against</th><th class="n">Size</th><th class="n">Score</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</section>"""


RUBRIC = [("Craft", 3, "One cut weight and whole-pixel edges throughout, and the hinted masters pass pixel fit. Feedback loop is light, and the turned red pieces leave gray pixels at 16 px."),
          ("Clarity", 3, "Every stage 1 failure is redrawn, and the 16 px set clears the similarity check. Naming waits on the main session's rerun, and by my eye Ballot and Track lose their names with the red removed."),
          ("Brand fidelity", 4, "Direction A's skeletons, its node and its seat, drawn filled as approved, with the hinge as the idea and red used as Rule 05.3 words it."),
          ("Usefulness", 4, "A row state that changes shape as well as color, masters at three sizes, holders, an app tile and eight contexts."),
          ("Evidence honesty", 5, "Every number comes from a Chromium render or the vector files, and the misses are listed."),
          ("Accessibility", 4, "Ink measures 13:1 or more on every surface; red on Newsprint gets a keyline in rows, and no subject depends on red's outer edge."),
          ("Beauty and distinctiveness", 3, "The constant cut and the moving red give the set a look of its own, and the pillar marks are its best drawings. Several topic symbols are plain, and the set would not yet stop a client on the page.")]


def sec_rubric():
    rows = "".join(f'<tr><td>{a}</td><td class="n">{b}</td><td>{e(c)}</td></tr>' for a, b, c in RUBRIC)
    return f"""
<section id="s-rubric"><h2>14. Rubric and recommendation</h2>
<p class="note">Master Brief section 6, 1 to 5, ship threshold 4, plus the seventh line. These are the maker's scores.</p>
<div class="tblwrap"><table style="min-width:560px"><thead><tr><th>Line</th><th class="n">Score</th><th>Why</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note"><b>Recommendation.</b> Run the name test on these masters. If two or fewer fail, carry Moving part forward and spend the next pass on craft and beauty, the two lines under 4: a heavier Feedback loop that keeps its red under the ceiling, a Ballot that keeps its name with its paper removed, and a closer study of Explain beside a badge at 16 px. If more than two fail, the concept stops here, as the brief sets.</p>
</section>"""


def sec_decide():
    return f"""
<section id="s-decide" class="decision"><h2>15. Decisions for Dustin</h2>
<ol>
<li><b>Act's full lintel (named approval, IC-04).</b> Options: keep the full lintel, or draw the frame over the opening only. Recommendation: keep it. Round one measured 0.60 against Inter Tight 800 "01" without it and 0.42 with it; this 16 px master scores {num(R['watch']['act|chapter number 01|16']['score'])}.</li>
<li><b>Topic symbols carry the node only where it is part of the subject.</b> This narrows Y5. In this concept no topic symbol carries the pillar node; Feedback loop's two nodes are its subject. Recommendation: approve.</li>
<li><b>No line companion.</b> This concept has no line cut, so it drops Y4 if chosen. Recommendation: decide it with the concept, since Overprint and Public sign answer it differently.</li>
<li><b>Under 48 px a pillar mark always sits with its word.</b> Studio proposal from the creative director's rules. Recommendation: approve; the menu row and the topic list show it.</li>
</ol>
<h3>For the creative director</h3>
<ol>
<li>Connect's bridge is 4.5 units tall where the notes asked for about 3, so the 3-unit knock-out keeps 0.75-unit walls. A 3-unit bar would need a 1.5-unit knock-out, smaller than the other nodes.</li>
<li>Feedback loop stands upright. With the nodes on the horizontal center line, as the notes set, it read as a face at 24 px. It also sits under the weight band at {pct(d96('loop')['density96'], 1)} percent painted, since a heavier drawing pushed its red past 25 percent.</li>
<li>Housing is redrawn after the notes said to keep it: the 16 px similarity check scored the stage 2 draft 0.68 against Ballot. The narrower body under wider eaves and the centered door bring every pair under 0.60.</li>
<li>Track's red block sits in the badge corner (x 16 to 22, y 2 to 8), attached across the cut to the stair below it; Campaign money's red note crosses it too. Neither stands alone there.</li>
</ol>
</section>"""


TESTED = [
    "Vector checks on all ten display masters at rest and open: painted share, red share, the smallest gap between pieces, overlaps, bounding box, center of mass and red inside the badge corner.",
    "Hinted masters at 24 and 16 px, at rest and open: the smallest cut between pieces in the vector files.",
    "Pixel fit (D1-17) from Chromium renders at 1x, at 24 and 16 px, at rest and open, and Phase 1's vector pixel-fit test.",
    "Similarity (D1-16) for all 45 pairs at 16 px and at 24 px.",
    "Look-alike scores against letters C, D, L and Z, the copyright sign, Inter Tight 800 \"01\", the V5 chain link and Signal Grid lockmark, a play button, a status light, and 17 Material Symbols glyphs at 16 and 24 px.",
    "Weight band and center of mass from 96 px renders, and the weight spread of a one-color row at 24 px.",
    "Red share in vector and at 96 px.",
    "Holder safe area for every icon in nine holders at 40 and 96 px, the 400 px avatar and the 1024 px app tile, from renders.",
    "Contrast ratios for every ink, red and keyline pairing (WCAG formula).",
    "The cover-the-red proxy (test 2) at 16, 24 and 48 px.",
    "The board's layout at 1440 and 390 px: horizontal scroll, elements outside the viewport, text under 13 px, images that fail to load, heading widows and tabular figures (icons_r2_moving_board_check.js).",
]
NOT_TESTED = [
    "Test 1, naming the icons blind: the main session reruns it on these masters.",
    "Any reader. No person has seen these icons (Q-13).",
    "Naming with the red covered (test 2) beyond my own reading; the proxy measures shape, not names.",
    "Whether the set reads as Oath & Action at 48 px with the wordmark covered (test 4), which needs a reader who has not seen the drawings.",
    "Rendering outside Chromium: Safari, Firefox, Windows ClearType and printed output.",
    "Retina and other device scales above 1x for the hinted masters.",
    "The app tile on a real device home screen and under the platforms' own masks.",
    "The motion chapter's animation of the open step.",
    "Rights for the reference sets; they were studied, never traced, and nothing from them is in the files.",
]


def sec_honest():
    return f"""
<section id="s-honest"><h2>16. Tested and not tested</h2>
<div class="lists"><div><h3>Tested</h3><ul>{''.join(f'<li>{e(t)}</li>' for t in TESTED)}</ul></div>
<div><h3>Not tested</h3><ul>{''.join(f'<li>{e(t)}</li>' for t in NOT_TESTED)}</ul></div></div>
</section>"""


def sec_files():
    n_var = len(list(C.VARIANTS.glob("*.svg")))
    n_h = len(list(C.HOLDERS.glob("*.svg")))
    return f"""
<section><h2>Files</h2>
<p class="note">All in <code>work/boards/phase-2/icons-r2/moving-part/</code>. The masters: 60 SVGs, three sizes for ten icons, at rest and open. <code>variants/</code>: {n_var} color variants. <code>holders/</code>: {n_h} holder SVGs. <code>app-tile/</code>: the three glyph-scale tests, the chosen 1024 px tile and the test sheet. <code>context/</code>: the eight context renders, the 400 px avatar and the card tile. <code>px/</code>: the 1x renders magnified in section 6. <code>stage-1/</code>: the stage 1 display masters as reviewed. Measurements: <code>20261028_Moving-Part-Measurements.json</code>. Notes: <code>work/handoffs/phase-2/20261028_Icon-Concept-2-Moving-Part-Notes.md</code>. Scripts: <code>work/build/scripts/phase-2/icons_r2_moving_*</code>.</p>
</section>"""


def main():
    page = (head() + intro() + sec_bench() + sec_idea() + sec_changes() + sec_grid() + sec_sizes() + sec_pixels() + sec_row()
            + sec_surfaces() + sec_holders() + sec_use() + sec_tests() + sec_checks() + sec_alike() + sec_rubric() + sec_decide()
            + sec_honest() + sec_files() + "</main></body></html>\n")
    BOARD.write_text(page)
    print(BOARD, len(page))


if __name__ == "__main__":
    main()
