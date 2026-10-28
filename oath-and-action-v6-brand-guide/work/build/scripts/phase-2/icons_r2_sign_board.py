"""Concept 3, Public sign, stage 2: build the concept board.

Run after icons_r2_sign_assets.py, icons_r2_sign_context.py and icons_r2_sign_measure.py:
  python3 -I icons_r2_sign_board.py
Writes work/boards/20261028_Icon-Concept-3-Public-Sign.html, a standalone page that follows
work/boards/20261021_Board-Conventions.md: doctype, charset and viewport metas, a title, Google
Fonts, board-base.css, inline board CSS, every asset by relative path from work/boards/, and a
decision panel. The numbers come from the measurements JSON; nothing on the board is typed by hand
that a script measured.
"""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_sign_common as C  # noqa: E402
import icons_r2_sign_draw as D  # noqa: E402
import icons_r2_sign_geom as G  # noqa: E402
import icons_r2_sign_studies as S  # noqa: E402

M = json.loads(C.MEASURE_JSON.read_text())
SPEC = M["spec"]
ICONS = D.ICONS
L = D.LABELS
e = html.escape

# The nearest Material Symbols glyph by subject, for the benchmark sheet (study only).
BENCH = {"explain": "info", "track": "stairs", "connect": "link", "act": "door_open", "ballot": "how_to_vote",
         "bill": "description", "testify": "record_voice_over", "housing": "house", "money": "payments",
         "loop": "autorenew"}
# Reference glyphs that draw the same subject: a high score against these confirms the reading.
SAME = {"track": {"Material stairs", "Material trending_up"}, "act": {"Material door_open", "Material meeting_room"},
        "ballot": {"Material how_to_vote"}, "bill": {"Material description"}, "housing": {"Material house", "Material home"},
        "testify": {"Material record_voice_over", "Material podium", "Material mic"}, "money": {"Material payments"}}


def rel(p):
    return C.rel(p)


def img(p, w, h=None, alt="", cls=""):
    h = h or w
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{rel(p)}" width="{w}" height="{h}" alt="{e(alt)}"{c} loading="lazy">'


def disp(n, cw="Charcoal-Red", px=96, alt=None):
    return img(C.variant_file(n, "Display", cw), px, alt=alt or L[n])


def m24(n, cw="Charcoal-Red", px=24, alt=None):
    return img(C.variant_file(n, "24px", cw), px, alt=alt or L[n])


def m16(n, cw="Charcoal-Red", px=16, alt=None):
    return img(C.variant_file(n, "16px", cw), px, alt=alt or L[n])


def inline_svg(lay, px, ink=C.CHAR, acc=C.RED, title=""):
    t = f"<title>{e(title)}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 24 24" role="img">{t}'
            f'<path d="{G.d_of(lay["ink"])}" fill="{ink}"/><path d="{G.d_of(lay["accent"])}" fill="{acc}"/></svg>')


def pct(v, d=1):
    return f"{100 * v:.{d}f}%"


def ok(b):
    return '<b class="pass">Pass</b>' if b else '<b class="fail">Fail</b>'


# ------------------------------------------------------------------ sections

def head():
    css = """
.lede{font-size:1.125rem;max-width:62ch}
.status{font-size:.9375rem;color:var(--muted)}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1px solid var(--rule);margin-top:20px}
.stats>div{padding:12px 14px;border-left:1px solid var(--rule);min-width:0}
.stats>div:first-child{border-left:0}
.stats b{display:block;font:800 1.5rem/1.15 var(--display)}
.stats span{font-size:.875rem;line-height:1.4;color:var(--muted)}
nav.toc{display:flex;flex-wrap:wrap;gap:4px 16px;margin-top:16px;font-size:.9375rem}
nav.toc a{color:var(--fg)}
.ten{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:22px 18px}
.ten figure{margin:0;min-width:0}
.ten img{display:block}
.ten figcaption{font-size:.8125rem;line-height:1.4;margin-top:6px}
.ten figcaption b{display:block;font-size:.9375rem}
.ten figcaption span{display:block;color:var(--muted)}
.ptile{background:var(--charcoal);color:var(--newsprint);padding:18px;margin-top:22px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.ptile figure{margin:0;min-width:0}.ptile img{display:block}
.ptile figcaption{font-size:.8125rem;line-height:1.4;color:#C9C5BC;margin-top:6px}
.ptile figcaption b{display:block;color:var(--newsprint);font-size:.9375rem}
.tbl{overflow-x:auto;max-width:100%}
.tbl table{min-width:640px}
td img,td svg{display:inline-block;vertical-align:middle}
.ms{font-family:'Material Symbols Outlined';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;direction:ltr;font-feature-settings:'liga';-webkit-font-smoothing:antialiased;color:var(--charcoal);vertical-align:middle}
.ms24{font-size:24px;width:24px;height:24px;font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24}
.ms48{font-size:48px;width:48px;height:48px;font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 48}
.pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 28px}
.pair>div{border-top:1px solid var(--rule);padding-top:12px;min-width:0}
.pair .ba{display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap;margin-bottom:8px}
.pair .ba figure{margin:0}.pair .ba img{display:block}
.pair figcaption{font-size:.8125rem;color:var(--muted)}
.pair p{font-size:.875rem;line-height:1.5;margin:0 0 6px}
.pair p b{font-size:.9375rem}
.sizes figure{margin:0}.sizes figcaption{font-size:.8125rem;color:var(--muted)}
.szrow{display:grid;grid-template-columns:150px minmax(0,1fr);gap:14px;align-items:end;padding:12px 0;border-bottom:1px solid var(--rule)}
.szrow .lab{font-weight:700;font-size:.9375rem}
.szrow .strip{display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap}
.szrow .strip img{display:block}
.pixgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px 16px}
.pixgrid figure{margin:0}.pixgrid img{display:block}
.pixgrid figcaption{font-size:.8125rem;color:var(--muted);margin-top:4px}
.surf{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--rule)}
.surf>div{padding:14px;min-width:0}
.surf .row{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0}
.surf .row img{display:block}
.surf .cap{margin:0}
.s-charcoal .cap,.s-prussian .cap{color:#C9C5BC}
.hold{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.hold>div{min-width:0}
.hold .row{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.hold .row img{display:block}
.ctx{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 28px}
.ctx figure{margin:0;min-width:0}
.ctx figcaption{font-size:.875rem;line-height:1.5;margin-top:8px}
.ctx .wide{grid-column:1/-1}
.ill{background:transparent;border-color:var(--muted);color:var(--muted);font-size:.8125rem;margin-left:6px}
.navrow{display:flex;align-items:center;flex-wrap:wrap;gap:6px 0;padding:12px 14px;border:1px solid var(--rule)}
.navrow .it{display:flex;align-items:center;gap:8px;font-size:.9375rem;padding-bottom:5px;border-bottom:2px solid transparent}
.navrow .it img{display:block}
.navrow .it.cur{font-weight:700;border-bottom-color:var(--charcoal)}
.navrow .ln{flex:1 1 16px;min-width:12px;height:1px;background:var(--rule);margin:0 10px}
.navrow.dark{background:var(--charcoal);color:var(--newsprint);border-color:var(--charcoal);margin-top:10px}
.navrow.dark .it.cur{border-bottom-color:var(--newsprint)}
.navrow.dark .ln{background:#5D636D}
.topics{border:1px solid var(--rule);background:var(--surface);max-width:420px}
.topics>div{display:grid;grid-template-columns:24px 1fr;gap:12px;align-items:center;padding:8px 14px;border-top:1px solid var(--rule)}
.topics>div:first-child{border-top:0}
.topics img{display:block}
.topics span{font-size:.9375rem;line-height:1.3}
.topics .on span{font-weight:700}
.topics .on{box-shadow:inset 3px 0 0 var(--charcoal)}
.shot{display:block;max-width:100%;height:auto;border:1px solid var(--rule)}
.avatar{display:flex;gap:14px;align-items:center;padding:14px;border:1px solid var(--rule);background:var(--white);flex-wrap:wrap}
.avatar img{display:block;border-radius:50%}
.avatar p{margin:0;font-size:.9375rem;line-height:1.35}
.avatar small{display:block;color:var(--muted);font-size:.8125rem}
.legend{padding:12px 14px;border:1px solid var(--rule);background:var(--surface);max-width:460px}
.legend .lg{display:flex;gap:10px;align-items:center;font-size:13px;line-height:1.4;margin:6px 0}
.legend .lg img{flex:none;display:block}
.tracker{width:100%;max-width:720px;font-size:.875rem}
.tracker td{padding:8px 10px;vertical-align:middle}
.tracker img{display:inline-block;vertical-align:-3px}
.st{display:inline-flex;align-items:center;gap:6px}
.st i{display:inline-block;width:10px;height:10px;border:1.5px solid var(--charcoal);border-radius:50%}
.st i.half{background:linear-gradient(90deg,var(--charcoal) 50%,transparent 50%)}
.st i.full{background:var(--charcoal)}
.wall{display:flex;flex-wrap:wrap;gap:18px 22px;align-items:flex-end;padding:22px;border-radius:10px}
.wall.light{background:linear-gradient(160deg,#F1EEE8,#C9CFD8)}
.wall.dark{background:linear-gradient(160deg,#2B3140,#0E1117);margin-top:10px}
.wall figure{margin:0;text-align:center}
.wall figcaption{font-size:.8125rem;margin-top:4px}
.wall.dark figcaption{color:#C9C5BC}
.wall img{display:block;margin:0 auto}
.scale3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.scale3>div{border-top:1px solid var(--rule);padding-top:10px;min-width:0}
.scale3 .row{display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap}
.scale3 img{display:block}
.pass{color:#1F5E3A}.fail{color:#9E1B26}
.decision h3{margin:18px 0 6px}.decision p,.decision li{max-width:78ch}
.decision ol{padding-left:1.2em;margin:0}.decision li{margin:0 0 10px}
.studies{display:flex;flex-wrap:wrap;gap:18px;margin:8px 0 4px}
.studies figure{margin:0;max-width:150px}
.studies img,.studies svg{display:block}
.studies figcaption{font-size:.8125rem;line-height:1.35;margin-top:4px;color:#DCD9D2}
.studies .np{background:var(--newsprint);padding:6px;display:inline-block}
.lists{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.lists ul{margin:0;padding-left:1.1em}.lists li{margin:0 0 8px;font-size:.9375rem}
.look{display:flex;flex-wrap:wrap;gap:16px 26px}
.look figure{margin:0}.look .pr{display:flex;gap:8px;align-items:center}
.look figcaption{font-size:.8125rem;color:var(--muted);margin-top:4px;max-width:220px}
@media (max-width:900px){.ten{grid-template-columns:repeat(3,minmax(0,1fr))}.ptile{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:760px){.ten{grid-template-columns:repeat(2,minmax(0,1fr))}.stats{grid-template-columns:repeat(2,minmax(0,1fr))}
.stats>div:nth-child(3){border-left:0}.pair,.ctx,.lists,.hold,.scale3{grid-template-columns:minmax(0,1fr)}
.surf{grid-template-columns:repeat(2,minmax(0,1fr))}.szrow{grid-template-columns:minmax(0,1fr)}}
"""
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Icon Concept 3, Public sign</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet">'
            '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0&display=block" rel="stylesheet">'
            f'<link rel="stylesheet" href="board-base.css"><style>{css}</style></head><body><main class="board">')


TOC = [("ten", "The ten"), ("bench", "Benchmark"), ("changed", "After stage 1"), ("rules", "Rules"), ("sizes", "Sizes"),
       ("pixels", "Pixels"), ("cover", "Cover the red"), ("surfaces", "Surfaces"), ("holders", "Holders"),
       ("use", "In use"), ("checks", "Checks"), ("tests", "Tests 2 to 4"), ("rubric", "Rubric"),
       ("decisions", "Decisions"), ("tested", "Tested and not tested")]


def intro():
    n_tiles = len(M["tiles"])
    return f"""
<p class="eyebrow">Phase 2 · Icon round two · Stage 2 · Concept 3 of 3</p>
<h1>Public sign</h1>
<p class="lede">Oath &amp; Action's subjects drawn the way public information symbols are drawn: people and objects built from one bar on a 45 and 90 degree grid, plain enough to read across a room. The red marks the verb, the one stroke that shows what happens to the subject.</p>
<p class="status">A proposal for the creative director and Dustin, October 28, 2026. No master in the guide changes. The blind name test on these finished masters is run by the main session and is not on this board yet.</p>
<div class="stats"><div><b>10</b><span>icons, each with a 16 px, a 24 px and a display master</span></div>
<div><b>{n_tiles}</b><span>holder tiles rendered and measured for the safe area</span></div>
<div><b>0</b><span>pairs at or over the 0.60 similarity limit, at 16, 24 and 48 px</span></div>
<div><b>{max(M['icons'][n]['d96']['red_share'] for n in ICONS) * 100:.1f}%</b><span>largest red share, under the 14 percent ceiling</span></div></div>
<nav class="toc">{''.join(f'<a href="#{a}">{b}</a>' for a, b in TOC)}</nav>"""


def sec_ten():
    figs = "".join(
        f'<figure>{disp(n)}<figcaption><b>{L[n]}</b><span>{D.CLASS[n]}</span>{e(D.VERB[n])}</figcaption></figure>' for n in ICONS)
    pill = "".join(
        f'<figure>{disp(n, "Newsprint-Red")}<figcaption><b>{L[n]}</b>{e(D.STORY[n])}</figcaption></figure>' for n in D.PILLARS)
    return f"""<section id="ten"><h2>1. The ten icons at 96 px</h2>
<p>Display masters on Newsprint. Under each, the one line that names its red. Each red is a verb: a swing, an arrow, a bridge, a mark or a sound.</p>
<div class="ten">{figs}</div>
<div class="ptile">{pill}</div></section>"""


def sec_bench():
    rows = []
    for n in ICONS:
        g = BENCH[n]
        rows.append(f"<tr><td><b>{L[n]}</b></td><td>{m24(n)}</td><td><span class='ms ms24'>{g}</span></td>"
                    f"<td>{disp(n, px=48)}</td><td><span class='ms ms48'>{g}</span></td><td><code>{g}</code></td></tr>")
    return f"""<section id="bench"><h2>2. Beside the best: a benchmark sheet <span class="tag">Study</span></h2>
<p>Each icon at 24 px (its hinted master) and 48 px (its display master) beside the nearest Material Symbols glyph by subject, Outlined, weight 400, optical size matched. Material Symbols is Apache 2.0 and loads here through Google Fonts (D1-19). This is a study for judging finish; no Material drawing enters the family.</p>
<div class="tbl"><table><thead><tr><th>Icon</th><th>Public sign 24</th><th>Material 24</th><th>Public sign 48</th><th>Material 48</th><th>Glyph</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="cap">Read at 24 px, the Public sign set is heavier than Material: a 3 px bar against Material's 2 px line. Its curves and joins are as clean at 48 px. At 24 px its weak points are Testify, where the arm, lectern and microphone fuse, and Ballot's check, which fills at 3 px. My judgement, not a reader's.</p></section>"""


CHANGES = [
    ("explain", "Note 1 and ruling 1: bring the lid back in ink, a bar L turned up 45 degrees on its hinge, the red tracing its swing.",
     "The top-right quarter is an ink L hinged at the end of the top bar and turned up 45 degrees. The red follows the lid's free end around the hinge. A lid turned 45 degrees travels 45 degrees, so the swing is an eighth of a circle; section 14 shows the quarter circle as a study."),
    ("track", "Note 2: give the red arrow a shaft.", "A 45 degree bar along the line of the stair now ends in the solid head."),
    ("connect", "Note 3: two bar arcs held apart, the red bridge across the gap, the node on it.",
     "Two arcs of the round-ended bar with their ends 4 units apart, each reaching in with a short spur. The bridge spans the gap between the spurs, and the node sits on it."),
    ("act", "Note 4: add a floor bar; draw the swing as a true quarter circle down to the floor.",
     "Floor bar under the opening, and a true quarter circle from the leaf's free edge down to the floor. The full lintel stays and goes to Dustin (section 14)."),
    ("ballot", "Note 5: taller box with a slot bar, paper sunk a third, a check with a long right arm, 7 units across.",
     "A low wide box with walls rising to the slot, the paper's lower part inside it, and a check 7 units across on an 8-unit paper, red on Charcoal at 4.49:1."),
    ("bill", "Note 6: draw the corner as a fold, a diagonal with its small triangle, and two text bars of different lengths above the red line.",
     "The page now fills the portrait keyline, so its silhouette stays apart from Explain's square (0.555 at 24 px). The first text bar stops short of the fold. The page weighs 37.9 percent of the field, over the band."),
    ("testify", "Note 7: stand the figure at a lectern, with a gooseneck microphone to the mouth and one red sound arc ahead of the face.",
     "Standing figure, arm resting on a sloped lectern, gooseneck rising toward the mouth, one red arc ahead of and above the face. There is no room for the arc level with the mouth without touching the microphone."),
    ("housing", "Note 8: passes; keep it as drawn.",
     "Kept, with one fix: the walls start 1.5 units lower. At stage 1 their round tops came within 0.2 units of the roof, against the family's 1.5-unit gap, and at 24 px they joined it."),
    ("money", "Note 9 and ruling 2: a banknote about 18 by 11 with a solid disc, the red an arrow with a shaft leaving the upper right edge.",
     "A landscape bar frame 20 by 11 units outside with a solid disc at its center, and a red arrow with a shaft leaving the upper right edge, outside the badge corner."),
    ("loop", "Note 10 and ruling 2: two nodes on the center line, a straight forward link with its arrowhead, the return as an arc below with the red head.",
     "Straight forward link with its head, return arc with the red head, so a half turn no longer maps the loop onto itself. The return runs over the top: drawn below, two nodes over a curve read as a face (study in section 14)."),
]


def sec_changed():
    out = []
    for n, note, did in CHANGES:
        before = C.OUT / "stage-1" / f"{C.DATE}_Public-Sign-{D.FILE_NAME[n]}-Display.svg"
        out.append(f'<div><div class="ba"><figure>{img(before, 96, alt=L[n] + ", stage 1")}<figcaption>Stage 1</figcaption></figure>'
                   f'<figure>{disp(n)}<figcaption>Stage 2</figcaption></figure></div>'
                   f'<p><b>{L[n]}</b></p><p>{e(note)}</p><p>{e(did)}</p></div>')
    return f"""<section id="changed"><h2>3. What changed after stage 1</h2>
<p>Each pair shows the stage 1 display master beside stage 2 at 96 px, with the creative director's note and what the drawing now does.</p>
<div class="pair">{''.join(out)}</div></section>"""


def sec_rules():
    rows = [("Grid", "The shared 24-unit grid, 2-unit padding, live area 2 to 22; lines at 0, 45 and 90 degrees; curves taken from circles"),
            ("Bar", f"{SPEC['bar_units']:g} units with round ends and joins; 3 px at 24 px, 2 px at 16 px"),
            ("Figure", f"Disc head {SPEC['head_units']:g} units held {SPEC['gap_units']:g} units off a bar body; no hands, feet, faces or gender cues; never red"),
            ("Node", f"A disc {SPEC['node_units']:g} units across on the horizontal center line in the four pillar marks"),
            ("Gap", f"{SPEC['gap_units']:g} units (1 px at 16, 1 or 2 px at 24) between parts and between ink and red"),
            ("Red", f"One stroke or arrowhead at bar width, at most {SPEC['red_ceiling'] * 100:.0f} percent of the painted area; every arrowhead has a shaft; red touches ink only where the verb acts on the object; no red alone in the top-right 6 by 6 units; no red plus shape"),
            ("Weight", f"Ink and red {SPEC['weight_band'][0] * 100:.0f} to {SPEC['weight_band'][1] * 100:.0f} percent of the field at 96 px"),
            ("Balance", f"Center of mass within {SPEC['centroid_limit'] * 100:.0f} percent of the field from its center"),
            ("Distinct", f"Every pair under {SPEC['similarity_limit']:.2f} (D1-16: mean of filled-silhouette overlap and blurred correlation, the Phase 1 practice), at 16, 24 and 48 px, with red and without"),
            ("Pixel fit", f"At least {SPEC['pixel_fit_limit']:.2f} of inked pixels crisp at 16 and 24 px (D1-17)"),
            ("16 px", "A separate drawing on the 16-unit grid, 2 px bars on whole pixels; detail drops where the object alone names the subject"),
            ("Banned", "Domes, columns, flags, scales, seals and stars; a house in the utility set")]
    return f"""<section id="rules"><h2>4. The rules, as drawn</h2>
<div class="tbl"><table><tbody>{''.join(f'<tr><th>{a}</th><td>{e(b)}</td></tr>' for a, b in rows)}</tbody></table></div></section>"""


def sec_sizes():
    rows = []
    for n in ICONS:
        strip = (f'<figure>{m16(n)}<figcaption>16</figcaption></figure><figure>{m24(n)}<figcaption>24</figcaption></figure>'
                 + "".join(f'<figure>{disp(n, px=s)}<figcaption>{s}</figcaption></figure>' for s in (32, 48, 64, 96)))
        rows.append(f'<div class="szrow"><div class="lab">{L[n]}</div><div class="strip">{strip}</div></div>')
    return f"""<section id="sizes"><h2>5. Sizes</h2>
<p>16 and 24 px are the hinted masters. 32 px and up scale the display master; the display master is meant for 48 px and up, and 32 px is shown to find where the 24 px master should hand over.</p>
{''.join(rows)}</section>"""


def sec_pixels():
    figs = []
    for n in ICONS:
        for kind, s in (("24px", 24), ("16px", 16)):
            p = C.PX / f"{C.stem(n, kind)}-Charcoal-Red.png"
            figs.append(f'<figure>{img(p, s * 6, alt=f"{L[n]}, {s} px master magnified six times", cls="pix")}<figcaption>{L[n]}, {s} px, 6x</figcaption></figure>')
    return f"""<section id="pixels"><h2>6. Pixels</h2>
<p>Chromium renders of the hinted masters at 1x, magnified six times without smoothing. Feedback loop, Campaign money and Bill have 24 px drawings made on the pixel grid: fitted from the display master, the loop's arrowheads became blocks, the coin a blob and Bill's text bars nubs. Every other 24 px master is the display drawing fitted to whole pixels.</p>
<div class="pixgrid">{''.join(figs)}</div></section>"""


def sec_cover():
    rows = []
    for n in ICONS:
        t2 = M["test2"][n]
        cells = []
        for kind, s, f in (("16px", 16, m16), ("24px", 24, m24), ("Display", 48, None)):
            def one(cw, kind=kind, s=s, f=f):
                return f(n, cw) if f else disp(n, cw, px=48)
            cells.append(f"<td>{one('Charcoal-Red')} {one('Charcoal-Red-As-Ink')} {one('Charcoal-Idle')}</td>")
        pr = f'<td class="s-prussian" style="background:var(--prussian)">{m24(n, "White-Idle")} {disp(n, "White-Idle", px=48)}</td>'
        near = t2["24"]["idle_nearest_other"]
        rows.append(f"<tr><td><b>{L[n]}</b></td>{''.join(cells)}{pr}<td>{t2['24']['idle_vs_own_full']:.2f}</td><td>{near[0]:.2f} {L[near[1]]}</td></tr>")
    return f"""<section id="cover"><h2>7. Cover the red (test 2)</h2>
<p>In each cell: as drawn, the red turned to ink, and the red removed (the idle state in a row). The last image column is White on Prussian with no red, at 24 and 48 px. The two number columns are measured at 24 px: how closely the idle icon matches its own full drawing, and its nearest other icon without red, which must stay under 0.60.</p>
<div class="tbl"><table><thead><tr><th>Icon</th><th>16 px</th><th>24 px</th><th>48 px</th><th>Prussian</th><th>Idle vs own</th><th>Nearest other, idle</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="cap">With the red gone, each drawing keeps its subject in ink: the frame and lid, the stair, the two halves, the doorway, the box and paper, the page, the speaker, the house, the note, the two nodes and their links. Testify without its sound arc reads as a person at a lectern, which is still the subject. Explain without its swing loses the motion and keeps the open lid. My reading; the rater has not seen these.</p></section>"""


def sec_surfaces():
    cols = []
    for key, label, bg in C.SURFACES:
        cw = {"newsprint": "Charcoal-Red", "white": "Charcoal-Red", "charcoal": "Newsprint-Red", "prussian": "White-Idle"}[key]
        r24 = "".join(m24(n, cw) for n in ICONS)
        r48 = "".join(disp(n, cw, px=48) for n in ICONS)
        ink = M["contrast"][f"ink|{key}"]
        red = M["contrast"].get(f"red|{key}")
        note = f"Ink {ink:.2f}:1" + (f", red {red:.2f}:1" if key != "prussian" else ", no red on Prussian")
        cols.append(f'<div class="s-{key}"><p class="cap">{label}. {note}</p><div class="row">{r24}</div><div class="row">{r48}</div></div>')
    c = M["contrast"]
    return f"""<section id="surfaces"><h2>8. Surfaces</h2>
<div class="surf">{''.join(cols)}</div>
<p class="cap">Red on Newsprint measures {c['red|newsprint']:.2f}:1, under the 3:1 a graphic needs, so no subject depends on its red: test 2 holds every name in ink. On Charcoal the red measures {c['red|charcoal']:.2f}:1, and Ballot's check sits on its Charcoal paper at {c['red|charcoal paper (Ballot)']:.2f}:1. In a row on Newsprint the current item's red takes a 1 px Charcoal keyline ({c['red|keyline']:.2f}:1 against it).</p></section>"""


def sec_holders():
    blocks = []
    for shape in C.HOLDER_SHAPES:
        rows = []
        for color in C.HOLDER_COLORS:
            row96 = "".join(img(C.tile_file(n, shape, color, 96), 96, alt=f"{L[n]}, {color} {C.HOLDER_LABEL[shape].lower()}") for n in ICONS)
            rows.append(f'<p class="cap">{color}, 96 px</p><div class="row">{row96}</div>')
        small = "".join(img(C.tile_file(n, shape, "Charcoal", 40), 40, alt=f"{L[n]}, 40 px") for n in ICONS)
        tiny = "".join(img(C.tile_file(n, shape, "Newsprint", 28), 28, alt=f"{L[n]}, 28 px") for n in ICONS)
        blocks.append(f'<div class="wide" style="grid-column:1/-1"><h3>{C.HOLDER_LABEL[shape]}{" (leads)" if shape == "Sign-Panel" else ""}</h3>{"".join(rows)}'
                      f'<p class="cap">Charcoal at 40 px with the 24 px master; Newsprint at 28 px with the 16 px master</p><div class="row">{small}</div><div class="row">{tiny}</div></div>')
    cons = C.HOLDERS / f"{C.DATE}_Public-Sign-Holder-Construction.svg"
    return f"""<section id="holders"><h2>9. Holders and tile colors</h2>
<p>The square sign panel leads: a 2-unit corner radius on the icon's grid, 5 percent of the side, so the panel reads as a sign plate. The icon's 24-unit field takes 60 percent of the side and its live area half, as in round one. A Charcoal panel carries a Newsprint pictogram with red, a Newsprint panel a Charcoal one with red (G1-09), and Prussian carries White with no red. The superellipse is the app tile; the circle is the avatar.</p>
<div class="hold">{''.join(blocks)}</div>
<figure style="margin:18px 0 0">{img(cons, 260, alt="Sign panel construction")}<figcaption class="cap">Construction: the panel at 240 px with the icon field (Verdigris), the live area (light rule), the circle safe zone (blue) and Act inside.</figcaption></figure></section>"""


def sec_use():
    cur = "track"
    nav_l = "".join(
        (f'<span class="it{" cur" if n == cur else ""}">{m24(n, "Charcoal-Keyline" if n == cur else "Charcoal-Idle")}{L[n]}</span>'
         + ('<span class="ln"></span>' if i < 3 else "")) for i, n in enumerate(D.PILLARS))
    nav_d = "".join(
        (f'<span class="it{" cur" if n == cur else ""}">{m24(n, "Newsprint-Red" if n == cur else "Newsprint-Idle")}{L[n]}</span>'
         + ('<span class="ln"></span>' if i < 3 else "")) for i, n in enumerate(D.PILLARS))
    topics = "".join(f'<div class="{"on" if n == "bill" else ""}">{m24(n, "Charcoal-Keyline" if n == "bill" else "Charcoal-Idle")}<span>{L[n]}</span></div>' for n in ICONS)
    av = C.CONTEXT / f"{C.DATE}_Public-Sign-Avatar-400.svg"
    card = C.CONTEXT / f"{C.DATE}_Public-Sign-Social-Card-1080x1350.png"
    art = C.CONTEXT / f"{C.DATE}_Public-Sign-Article-Header-1440.png"
    legend = "".join(f'<div class="lg">{m16(n, "Charcoal-Idle")}<span>{t}</span></div>' for n, t in (
        ("loop", "Feedback loop: a result that changes the next decision"), ("bill", "Bill in the legislature"),
        ("testify", "Public hearing with sign-up"), ("money", "Campaign money reported")))
    tr = (f'<tr><td>{m16("bill", "Charcoal-Idle")}</td><td>Rental registry bill</td><td><span class="st"><i class="half"></i>In committee</span></td><td>Mar 4</td></tr>'
          f'<tr><td>{m16("bill")}</td><td><b>Public records fee bill</b></td><td><span class="st"><i class="full"></i>Passed one chamber</span></td><td>Feb 27</td></tr>'
          f'<tr><td>{m16("testify", "Charcoal-Idle")}</td><td>Budget hearing sign-up</td><td><span class="st"><i></i>Open</span></td><td>Mar 11</td></tr>')
    app = C.CONTEXT / f"{C.DATE}_Public-Sign-App-Tile-1024.svg"
    walls = "".join(
        f'<div class="wall {w}">' + "".join(f'<figure>{img(app, s, alt=f"App tile at {s} px")}<figcaption>{s}</figcaption></figure>' for s in (180, 120, 60, 29)) + "</div>"
        for w in ("light", "dark"))
    scale = "".join(
        f'<div><p class="cap">{sc} percent{" (chosen)" if sc == 62 else ""}</p><div class="row">'
        + "".join(img(C.CONTEXT / f"{C.DATE}_Public-Sign-App-Tile-1024-Charcoal-{sc}.svg", s, alt=f"Act tile, {sc} percent, {s} px") for s in (180, 60, 29))
        + "</div></div>" for sc in (56, 62, 66))
    ill = '<span class="tag ill">Illustrative</span>'
    return f"""<section id="use"><h2>10. In use</h2>
<div class="ctx">
<figure class="wide"><div class="navrow">{nav_l}</div><div class="navrow dark">{nav_d}</div>
<figcaption>1. The four pillars in a menu row on Newsprint and on Charcoal, Track current. Idle icons go one color and drop the verb; the current icon keeps its red and its label goes bold (Rule 05.3, D2-01). On Newsprint the current red carries a 1 px Charcoal keyline.</figcaption></figure>
<figure><div class="topics">{topics}</div><figcaption>2. A topic list with labels at 24 px, all ten icons, Bill current.</figcaption></figure>
<figure><div class="avatar">{img(av, 72, alt="Avatar at 72 px")}{img(av, 40, alt="Avatar at 40 px")}<p>Profile name<small>Avatar at 72 and 40 px</small></p></div>
<figcaption>4. A social avatar, 400 px, shown at 72 and 40 px: Track in the circle holder on Charcoal. The profile name is a placeholder. {ill}</figcaption></figure>
<figure class="wide">{img(art, 1440, 520, alt="Article header at 1440 px", cls="shot")}
<figcaption>3. An article header at 1440 px with Testify at 64 px beside the headline, shown scaled to this column. Headline, dek and byline are invented. {ill}</figcaption></figure>
<figure>{img(card, 432, 540, alt="Social card, 1080 by 1350", cls="shot")}<figcaption>5. A social card, 1080 by 1350, shown at 40 percent: Testify large in the Charcoal sign panel, and one working red elsewhere, the rule over the headline. The copy is invented. {ill}</figcaption></figure>
<figure><div class="legend">{legend}</div><figcaption>6. An atlas legend at 16 px beside 13 px text, with Feedback loop. A legend is a list, so every icon is one color. The legend lines are invented. {ill}</figcaption>
<div style="margin-top:22px"><table class="tracker"><tbody>{tr}</tbody></table></div>
<figcaption>7. A tracker table row at 16 px beside status marks. The current row keeps its red. The status marks are placeholders drawn for this board, and the bills and dates are invented. {ill}</figcaption></figure>
<figure class="wide">{walls}<figcaption>8. The app tile, Act at 62 percent of the side in a Charcoal superellipse, at 180, 120, 60 and 29 px on a light and a dark wallpaper. The wallpapers are plain gradients drawn for this board. {ill}</figcaption></figure>
<figure class="wide"><div class="scale3">{scale}</div><figcaption>The glyph scale study at 180, 60 and 29 px. At 66 percent the lintel crowds the tile's top corners at 29 px; at 56 percent the tile reads as a dark square first. I chose 62 percent by eye.</figcaption></figure>
</div></section>"""


def look_flags(n):
    full = M["lookalike"][f"{n}|full|24"]
    same = SAME.get(n, set())
    wrong = [(v, nm) for v, nm in full if nm not in same]
    conf = [(v, nm) for v, nm in full if nm in same]
    return wrong, conf


def sec_checks():
    rows = []
    for n in ICONS:
        r = M["icons"][n]
        d = r["d96"]
        lo, hi = SPEC["weight_band"]
        wt_ok = lo <= d["density"] <= hi
        com = max(abs(d["centroid"][0]), abs(d["centroid"][1]))
        worst = max(((v["score"], k) for k, v in M["pairs"].items() if n in k.split("|")[:2]), key=lambda t: t[0])
        a, b, s = worst[1].split("|")
        other = b if a == n else a
        wrong, conf = look_flags(n)
        w0 = wrong[0]
        rows.append(
            f"<tr><td><b>{L[n]}</b></td><td>{r['m16']['crisp']:.2f} / {r['m24']['crisp']:.2f} {ok(r['m16']['pixel_fit_pass'] and r['m24']['pixel_fit_pass'])}</td>"
            f"<td>{pct(d['red_share'])} {ok(d['red_share'] <= SPEC['red_ceiling'])}</td>"
            f"<td>{pct(d['density'])} {ok(wt_ok)}</td>"
            f"<td>{d['centroid'][0]:+.3f}, {d['centroid'][1]:+.3f} {ok(com <= SPEC['centroid_limit'])}</td>"
            f"<td>{worst[0]:.3f} {L[other]} at {s} {ok(worst[0] < SPEC['similarity_limit'])}</td>"
            f"<td>{w0[0]:.2f} {e(w0[1])}{' <b class=fail>Flag</b>' if w0[0] >= 0.60 else ''}</td>"
            f"<td>{r['m16']['components']} of {r['m16']['components_display']}</td>"
            f"<td>{ok(d['straight_edges_in_live'] and d['round_overshoot_ok'])}</td>"
            f"<td>{ok(d['badge_red_area'] == 0 and not r['m16']['red_plus'] and not r['m24']['red_plus'])}</td></tr>")
    sets = M["sets"]
    tiles_bad = [k for k, v in M["tiles"].items() if not v["in_live_area"] or v.get("in_circle_safe") is False]
    flagged = []
    for n in ICONS:
        wrong, conf = look_flags(n)
        for v, nm in wrong:
            if v >= 0.60:
                flagged.append((n, v, nm))
    looks = []
    for n, v, nm in flagged:
        ref = ""
        if nm.startswith("Material "):
            g = nm.split(" ", 1)[1]
            ref = f"<span class='ms ms24'>{g}</span> <span class='ms ms48'>{g}</span>"
        else:
            ch = {"letter theta": "θ", "letter omega": "Ω", "chapter number 01": "01", "numeral 2": "2"}.get(nm, nm.split()[-1])
            ref = f"<span style='font:800 24px/1 var(--display)'>{e(ch)}</span> <span style='font:800 48px/1 var(--display)'>{e(ch)}</span>"
        looks.append(f'<figure><div class="pr">{m24(n)} {disp(n, px=48)} {ref}</div><figcaption>{L[n]} against {e(nm)}, {v:.2f} at 24 px</figcaption></figure>')
    return f"""<section id="checks"><h2>11. Checks</h2>
<p>Every number below comes from <code>icons_r2_sign_measure.py</code>, which renders each master in Chromium at device scale 1 and measures the pixels. Pixel fit is the crisp share at 16 and 24 px (D1-17). Red and weight are measured on the 96 px display render. Center of mass is the offset from the field's center as a share of the field. Similarity is the worst pair the icon takes part in, at 16, 24 or 48 px. Look-alike is the nearest reference glyph at 24 px that draws a different subject. Parts compares the separate pieces in the 16 px master with the display master's. Testify gains one at 16 px because the arm drops and the body stands apart from the lectern.</p>
<div class="tbl"><table><thead><tr><th>Icon</th><th>Pixel fit 16 / 24</th><th>Red share</th><th>Weight</th><th>Center of mass</th><th>Worst pair</th><th>Nearest look-alike</th><th>Parts at 16</th><th>Live area</th><th>Badge corner, plus</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="cap">Sets: worst pair at 16 px {sets['16']['worst'][1]:.3f} ({e(sets['16']['worst'][0].replace('|', ', '))}), at 24 px {sets['24']['worst'][1]:.3f}, at 48 px {sets['48']['worst'][1]:.3f}; without red, worst {sets['16']['idle_worst'][1]:.3f}, {sets['24']['idle_worst'][1]:.3f} and {sets['48']['idle_worst'][1]:.3f}. Weight runs {pct(sets['density96']['min'])} to {pct(sets['density96']['max'])} around a median of {pct(sets['density96']['median'])}. Holder safe area: {len(M['tiles'])} tiles rendered, {len(tiles_bad)} outside the live area or the circle's safe zone; round forms may cross the live area by 0.25 units, as ruling 4 allows.</p>
<h3>Two weight misses</h3>
<p>Bill weighs {pct(M['icons']['bill']['d96']['density'])}. A page at the bar's 3 units with two text bars and a fold cannot get lighter without narrowing, and a narrower page scored 0.62 against Explain. I kept Bill distinct and heavy. Feedback loop weighs {pct(M['icons']['loop']['d96']['density'])}: two nodes and two thin paths leave most of the field open, and larger nodes crowd the forward arrow at 24 px.</p>
<h3>Look-alikes at 0.60 or more</h3>
<p>The look-alike score compares filled silhouettes and blurred pixels, so it cannot see interiors. Bill scores {M['lookalike']['bill|full|24'][1][0] if False else look_flags('bill')[0][0][0]:.2f} against the SIM card because a page and a SIM card share an outline; what separates them is the text bars inside, and the rater who saw SIM card at stage 1 saw rounded blocks there. Explain's score against the house glyph is the risk I take most seriously: the lid turned up 45 degrees makes a roof line over a square. The blind name test is the judge for all of these.</p>
<div class="look">{''.join(looks)}</div>
<p class="cap">Same-subject glyphs score high and confirm the reading: Ballot against how_to_vote {[v for v, nm in M['lookalike']['ballot|full|24'] if nm == 'Material how_to_vote'][0]:.2f}, Bill against description {[v for v, nm in M['lookalike']['bill|full|24'] if nm == 'Material description'][0]:.2f}.</p></section>"""


def sec_tests():
    return f"""<section id="tests"><h2>12. Tests 2 to 4</h2>
<div class="tbl"><table><thead><tr><th>Test</th><th>Result</th><th>How it was run</th></tr></thead><tbody>
<tr><td><b>1. Name it</b></td><td>Not run on these masters</td><td>The main session runs it with a fresh rater. The concept stops if more than two icons fail.</td></tr>
<tr><td><b>2. Cover the red</b></td><td>Pass on measures; my reading passes all ten</td><td>Red turned to ink and removed at 16, 24 and 48 px and White on Prussian (section 7). Without red, the worst pair is {M['sets']['16']['idle_worst'][1]:.3f} at 16 px, so no two icons merge. Whether each keeps its name is my reading until a rater sees them.</td></tr>
<tr><td><b>3. Hold up at 2x</b></td><td>Pass on measures, with two weight misses</td><td>One bar weight: the median stroke is 3.00 units in eight of ten; Ballot and Testify measure wider because their paper and lectern are solids. Pixel fit 1.00 at 16 and 24 px. Centers of mass all inside {SPEC['centroid_limit'] * 100:.0f} percent. Bill and Feedback loop sit outside the weight band (section 11).</td></tr>
<tr><td><b>4. Beside the best</b></td><td>Partial, my judgement</td><td>At 48 px the set looks as finished as Material Symbols. At 24 px it is heavier and Testify fuses. In a one-color row of all ten it reads as one family (section 7, middle image in each cell). With the wordmark covered at 48 px it reads as public information signage first and as Oath &amp; Action second: the red verbs carry the brand, and the bars belong to the genre.</td></tr>
</tbody></table></div></section>"""


RUBRIC = [
    ("Craft", 3, "Clean joins and one bar throughout, and hand-drawn 24 px masters where fitting failed. The bars are blunt at 96 px and Testify fuses at 24 px."),
    ("Clarity", 4, "The concept the stage 1 rater read most easily. Every pair separates at 16, 24 and 48 px with and without red. Unproven until the name test reruns."),
    ("Brand fidelity", 3, "The red verbs and the node carry Oath &amp; Action. The bar drawing and the sign panel come from transit and government signage, and the pillar marks give up Direction A's solids."),
    ("Usefulness", 4, "Idle, current and Prussian states, three holders in three colors, 16 px drawings for legends and tables, an app tile and an avatar."),
    ("Evidence honesty", 4, "Every number on the board is measured by script; misses and deviations are shown beside the drawings. No person has read an icon."),
    ("Accessibility", 4, "Ink passes 13:1 on every surface; no subject depends on red, which measures 2.96:1 on Newsprint; the current item's red takes a Charcoal keyline."),
    ("Beauty and distinctiveness", 2, "Legible and orderly. Beside Dustin's references and Aicher's own sheets it looks like a competent public sign set, and the genre's familiarity is the reason."),
]


def sec_rubric():
    rows = "".join(f"<tr><td><b>{a}</b></td><td>{s}</td><td>{b}</td></tr>" for a, s, b in RUBRIC)
    return f"""<section id="rubric"><h2>13. Rubric</h2>
<p>Master Brief section 6 plus the seventh line, 1 to 5, ship threshold 4 on every line. My scores, for the creative director to overrule.</p>
<div class="tbl"><table><thead><tr><th>Line</th><th>Score</th><th>Reason</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>Public sign does not meet the ship threshold on craft, brand fidelity or beauty. Its case is legibility for newcomers.</p></section>"""


def sec_decisions():
    approved = C.BOARDS / "phase-1/gate-1/img"
    ex90 = S.explain_open90()
    below = S.loop_arc_below()
    pillars_a = "".join(
        f'<figure><span class="np">{img(approved / f"sym-A-filled-{n}-96.png", 96, 97, alt=f"{L[n]}, approved Direction A")}</span><figcaption>{L[n]}, approved (Direction A, Gate 1)</figcaption></figure>'
        f'<figure><span class="np">{disp(n)}</span><figcaption>{L[n]}, Public sign</figcaption></figure>' for n in D.PILLARS)
    ex = (f'<figure><span class="np">{img(approved / "sym-A-filled-explain-96.png", 96, 97, alt="Explain, approved")}</span><figcaption>Approved skeleton</figcaption></figure>'
          f'<figure><span class="np">{disp("explain")}</span><figcaption>Master: lid hinged and turned up 45 degrees</figcaption></figure>'
          f'<figure><span class="np">{inline_svg(ex90, 96, title="Explain study, lid open 90 degrees")}</span><figcaption>Study: lid open 90 degrees, quarter-circle swing, red 18.8 percent</figcaption></figure>')
    lp = (f'<figure><span class="np">{disp("loop")}</span><figcaption>Master: return over the top</figcaption></figure>'
          f'<figure><span class="np">{inline_svg(below, 96, title="Feedback loop study, return below")}</span><figcaption>Study: return below, as note 10 words it</figcaption></figure>')
    return f"""<section id="decisions"><h2>14. Decisions</h2>
<div class="decision">
<h3>For Dustin's named approval</h3>
<ol>
<li><b>The pillar marks change treatment.</b> Direction A's skeletons stay; the solids become bars with round ends and a disc node. Options: approve the bar treatment for this concept, or keep the solids and drop the concept. Recommendation: decide only if Public sign wins, since it changes Y1's solid treatment.
<div class="studies">{pillars_a}</div></li>
<li><b>Act keeps its full lintel</b> (round one's IC-04). Options: full lintel, or the frame over the opening only. Recommendation: the full lintel, because without it the doorway reads as the letter n at 24 px.</li>
<li><b>Explain, if it fails the name test.</b> Its skeleton then goes to Dustin as a question, with the drawings beside the approved one. Options: the hinged lid at 45 degrees (the master), the lid open 90 degrees with a true quarter-circle swing (a study, over the red ceiling), or the approved lifted quarter. Recommendation: the master; the 90 degree lid reads as a tab.
<div class="studies">{ex}</div></li>
<li><b>Topic symbols carry a node only where it is part of the subject.</b> This narrows Y5. Recommendation: approve; Ballot, Bill, Testify, Housing and Campaign money carry no node.</li>
</ol>
<h3>For the creative director</h3>
<ol>
<li><b>Feedback loop's return runs over the top.</b> Note 10 asks for it below. Options: as drawn, or below. Recommendation: over the top, because two nodes over a curve read as a smiling face.
<div class="studies">{lp}</div></li>
<li><b>Bill stays over the weight band</b> at {pct(M['icons']['bill']['d96']['density'])}. Options: keep the wide page, or narrow it into the band and fail similarity with Explain. Recommendation: keep; D1-16 protects the name.</li>
<li><b>Feedback loop stays under the band</b> at {pct(M['icons']['loop']['d96']['density'])}. Recommendation: accept; the drawing is two nodes and two paths.</li>
<li><b>Explain's swing is 45 degrees.</b> Note 1 asks for a lid turned 45 degrees and a quarter-circle swing; one lid cannot do both. Recommendation: keep the 45 degree lid.</li>
<li><b>App tile at 62 percent.</b> Chosen by eye from 56, 62 and 66 (section 10).</li>
</ol>
</div></section>"""


def sec_tested():
    return """<section id="tested"><h2>15. Tested and not tested</h2>
<div class="lists"><div><h3>Tested</h3><ul>
<li>Pixel fit, density, red share, center of mass, stroke width, bounds, badge corner and red plus shapes for all ten at 16, 24 and 96 px, from Chromium renders at device scale 1.</li>
<li>Similarity of all 45 pairs at 16, 24 and 48 px, with red and without.</li>
<li>Look-alikes against 42 Material Symbols glyphs, 13 letters and numerals, and the Phase 0 watch items, at 16, 24 and 48 px.</li>
<li>Contrast of ink, red and keyline on Newsprint, White, Charcoal and Prussian.</li>
<li>The safe area of 270 holder tiles (three shapes, three colors, 28, 40 and 96 px).</li>
<li>This board in Chromium at 1440 and 390 px: no sideways scroll, no text under 13 px, every image loaded (screens in the public-sign folder).</li>
</ul></div><div><h3>Not tested</h3><ul>
<li>The blind name test on these masters (the main session runs it).</li>
<li>Any reader. No person has seen an icon (Q-13).</li>
<li>Rendering in Safari, Firefox, Windows ClearType or on a phone screen.</li>
<li>The app tile on a real home screen; the wallpapers here are drawn gradients.</li>
<li>Print.</li>
<li>Whether the sign panel's official tone suggests an authority the brand does not claim. That is a judgement for Dustin.</li>
</ul></div></div></section>"""


def build():
    parts = [head(), intro(), sec_ten(), sec_bench(), sec_changed(), sec_rules(), sec_sizes(), sec_pixels(), sec_cover(),
             sec_surfaces(), sec_holders(), sec_use(), sec_checks(), sec_tests(), sec_rubric(), sec_decisions(), sec_tested(),
             "</main></body></html>"]
    C.BOARD.write_text("\n".join(parts))
    print(C.BOARD, C.BOARD.stat().st_size)


if __name__ == "__main__":
    build()
