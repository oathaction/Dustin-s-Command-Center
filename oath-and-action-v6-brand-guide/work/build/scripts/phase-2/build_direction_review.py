"""Build the direction review page from its template, the direction review report and the Phase 2 boards.

Usage:
    python3 -I build_direction_review.py <project-root> [--report PATH] [--out PATH] [--no-capture] [--check]

Each run first recaptures the screenshots from the Field Guide and Overprint boards
(capture_direction_review.js), so one rerun picks up any change to the boards. --no-capture reuses
the images in work/boards/phase-2/direction-review/img/. --check runs check_direction_review.js.

The page reads the report at build time: the decision list and sample reply, the three score and test
tables, the three choices' prose, the P1 to P3 calls, the R1 to R14 set, Q-13, the risks and the next
steps. The page and the report cannot disagree.

Images: the poster and the hub crop are the poster's own SVG files, inlined with their styles scoped
to each copy. Icons are their own SVG files, embedded as images. The 16 and 24 px icon cells are the
board's 1x renders, at natural size and magnified without smoothing. The Field Guide pages and the menu
rows are element screenshots at device scale 2, shown at half their pixel width.
"""
import base64
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys

from PIL import Image

args = sys.argv[1:]
if not args:
    raise SystemExit(__doc__)
ROOT = os.path.abspath(args[0])
FLAGS = {a for a in args[1:] if a in ("--no-capture", "--check")}
rest = [a for a in args[1:] if a not in FLAGS]
opts = dict(zip(rest[0::2], rest[1::2]))
HERE = os.path.dirname(os.path.abspath(__file__))
BOARDS = os.path.join(ROOT, "work", "boards")
P2 = os.path.join(BOARDS, "phase-2")
DR = os.path.join(P2, "direction-review")
IMG = os.path.join(DR, "img")
MAPS_C = os.path.join(P2, "maps-r2", "c")
ICONS = os.path.join(P2, "icons-r2")
OVER = os.path.join(ICONS, "overprint")
REPORT = opts.get("--report", os.path.join(ROOT, "work", "ledger", "20261028_Direction-Review-Report.md"))
OUT = opts.get("--out", os.path.join(BOARDS, "20261028_Direction-Review-Board.html"))
WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("WARNING: " + msg, file=sys.stderr)


def need(cond, msg):
    if not cond:
        raise SystemExit("build_direction_review: " + msg)


def run_node(script):
    node = shutil.which("node")
    need(node, "node is not on the PATH")
    subprocess.run([node, os.path.join(HERE, script), ROOT], check=True)


if "--no-capture" not in FLAGS:
    run_node("capture_direction_review.js")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- text helpers

def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


ANCHORS = {"3": "#scores", "4": "#choices", "5": "#calls", "6": "#set", "7": "#q13", "8": "#risks", "9": "#next"}


def link_sections(h):
    return re.sub(r"\b([Ss]ection) (\d+)\b", lambda m: f'<a href="{ANCHORS[m.group(2)]}">{m.group(1)} {m.group(2)}</a>' if m.group(2) in ANCHORS else m.group(0), h)


def lead_in(h):
    """Set a paragraph's lead words in bold: 'Options:', 'The cost:', 'Recommended:'."""
    return re.sub(r"^(Options:|The cost:|Recommended:)", r"<strong>\1</strong>", h)


def md_blocks(text):
    lines = text.strip("\n").split("\n")
    out, i = [], 0
    start = lambda l: l.startswith(("|", ">", "- ", "#")) or re.match(r"\d+\. ", l)
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.startswith(("|", "#")):
            i += 1
        elif line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip())
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(buf))}</p></blockquote>")
        elif re.match(r"\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            out.append('<ul class="list">' + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not start(lines[i]):
                buf.append(lines[i].strip())
                i += 1
            out.append(f"<p>{lead_in(inline(' '.join(buf)))}</p>")
    return "\n".join(out)


def split_headings(text, level):
    pat = re.compile(r"^" + "#" * level + r" (.+)$", re.M)
    ms = list(pat.finditer(text))
    return [(m.group(1).strip(), text[m.end(): ms[k + 1].start() if k + 1 < len(ms) else len(text)]) for k, m in enumerate(ms)]


def section(sections, prefix):
    hits = [body for title, body in sections if title.startswith(prefix)]
    need(len(hits) == 1, f"report section starting {prefix!r} not found once")
    return hits[0]


def md_table(text, header_prefix):
    lines = text.split("\n")
    idx = [k for k, l in enumerate(lines) if l.startswith(header_prefix)]
    need(idx, f"table {header_prefix!r} not found")
    rows = []
    for line in lines[idx[0]:]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            continue
        rows.append(cells)
    return rows[0], rows[1:]


def strip_tags(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def count_word(n):
    words = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
    return words[n] if n < len(words) else str(n)


# ---------------------------------------------------------------- images and SVG

EMBEDDED = {}
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml"}


def image_size(path):
    if path.endswith(".svg"):
        head = read(path)[:600]
        m = re.search(r'<svg[^>]*\swidth="([\d.]+)"[^>]*\sheight="([\d.]+)"', head)
        if m:
            return float(m.group(1)), float(m.group(2))
        vb = re.search(r'viewBox="([^"]+)"', head).group(1).split()
        return float(vb[2]), float(vb[3])
    with Image.open(path) as im:
        return im.size


def data_uri(path):
    if path not in EMBEDDED:
        need(os.path.exists(path), f"missing image {path}")
        with open(path, "rb") as f:
            EMBEDDED[path] = f"data:{MIME[os.path.splitext(path)[1].lower()]};base64," + base64.b64encode(f.read()).decode()
    return EMBEDDED[path]


def img(path, alt, scale=1, factor=None, width=None, cls="", style=""):
    pw, ph = image_size(path)
    if width:
        w, h = width, width * ph / pw
    elif factor:
        w, h = pw * factor, ph * factor
        cls = (cls + " px").strip()
    else:
        w, h = pw / scale, ph / scale
    c = f' class="{cls}"' if cls else ""
    s = f' style="{style}"' if style else ""
    return f'<img src="{data_uri(path)}" width="{round(w)}" height="{round(h)}" alt="{attr(alt)}"{c}{s}>'


SCOPES = []


def svg_inline(path, label, width=None, viewbox=None, cls="", style=""):
    """Inline an SVG file. Its <style> rules are scoped to this copy, so they cannot restyle the page."""
    t = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", read(path), flags=re.S).strip()
    t = re.sub(r"<title>.*?</title>|<desc>.*?</desc>", "", t, flags=re.S)
    root = re.match(r"<svg\b[^>]*>", t).group(0)
    vb = viewbox or re.search(r'viewBox="([^"]+)"', root).group(1)
    vbw, vbh = (float(x) for x in vb.split()[2:])
    width = width or vbw
    height = width * vbh / vbw
    sid = f"svg{len(SCOPES) + 1}"
    SCOPES.append(sid)

    def scope(m):
        css = re.sub(r"([^{}]+)\{", lambda mm: ",".join(f"#{sid} {s.strip()}" for s in mm.group(1).split(",")) + "{", m.group(1))
        return f"<style>{css}</style>"

    body = re.sub(r"<style>(.*?)</style>", scope, t[len(root):], flags=re.S)
    new = re.sub(r'\s(width|height|viewBox|style|role|aria-label|class|id|data-[\w-]+)="[^"]*"', "", root)[:-1]
    new += f' id="{sid}" viewBox="{vb}" width="{width:.0f}" height="{height:.0f}" role="img" aria-label="{attr(label)}" focusable="false"'
    if cls:
        new += f' class="{cls}"'
    if style:
        new += f' style="{style}"'
    return new + ">" + body


def scroll(inner, label, cls=""):
    return f'<div class="scroll {cls}" tabindex="0" role="region" aria-label="{attr(label)}">{inner}</div>'


MANIFEST = json.load(open(os.path.join(IMG, "manifest.json"), encoding="utf-8"))


def cap_img(name, alt, **kw):
    need(name in MANIFEST, f"capture {name} missing; run capture_direction_review.js")
    return img(os.path.join(IMG, name), alt, scale=2, **kw)


# ---------------------------------------------------------------- report

report = read(REPORT)
sections = split_headings(report, 2)
title = report.split("\n", 1)[0]
need(title.startswith("# Direction review: "), "report title line changed")
title = title[2:]

decide = section(sections, "What you are asked to decide")
decide_items = [re.sub(r"^\d+\. ", "", l) for l in decide.split("\n") if re.match(r"\d+\. ", l)]
m = re.search(r'^(A reply can be this short:) "(.+?)"\s*(.*)$', decide, flags=re.M)
need(m, "sample reply not found")
reply_intro, reply, reply_after = m.group(1), m.group(2), m.group(3)

s3 = section(sections, "3. ")
maps_head, maps_rows = md_table(s3, "| Direction | Cr |")
icon_head, icon_rows = md_table(s3, "| Concept | Cr |")
name_head, name_rows = md_table(s3, "| Subject |")
s3_parts = re.split(r"\n(?=\||\*\*)", s3)

s4 = section(sections, "4. ")
choices = [(t, body) for t, body in split_headings(s4, 3) if t.startswith("Choice")]
need(len(choices) >= 3, "expected three choices in section 4")
s5 = section(sections, "5. ")
call_head, call_rows = md_table(s5, "| ID | Call |")
s6 = section(sections, "6. ")
set_head, set_rows = md_table(s6, "| ID | Recommendation |")
s7 = section(sections, "7. ")
s8 = section(sections, "8. ")
s9 = section(sections, "9. ")

# ---------------------------------------------------------------- maps

POSTER = os.path.join(MAPS_C, "20261028_Loop-Lines-Poster.svg")
POSTER_PRINT = os.path.join(MAPS_C, "20261028_Loop-Lines-Poster-Print.svg")
NETWORK = json.load(open(os.path.join(MAPS_C, "20261028_Loop-Lines-Network-Data.json"), encoding="utf-8"))
PRINT_SCALE = 2.4  # the 24 by 36 inch PDF draws the 1440 by 960 drawing 2.4 times larger, in CSS inches
CHOICE1 = [b for t, b in choices if t.startswith("Choice 1")][0]


def poster_band():
    alt = "Loop Lines poster on Prussian: twenty numbered loops drawn as closed transit lines in Newsprint through shared variable stations, the hub at the center with eight spokes, district fields A to E, the frame bands and the legend."
    svg = svg_inline(POSTER, alt, width=1440, cls="poster")
    note = re.search(r"The poster draws[^.]*;[^.]*\.", CHOICE1)
    return (f'<section class="band prussian" aria-labelledby="poster-h"><div class="band-in">'
            '<h3 id="poster-h" class="bandline">The whole system on one poster, and every loop on its own card.</h3>'
            f'{svg}<p class="band-cap">Loop Lines, Direction C\'s poster, inlined from its own drawing at 1440 by 960. '
            f'{inline(note.group(0)) if note else ""}</p></div></section>')


def hub_crop():
    cx, cy = NETWORK["stations"]["E1"]["px"]
    w_css, h_css = 1248, 720
    vw, vh = w_css / PRINT_SCALE, h_css / PRINT_SCALE
    vb = f"{cx - vw / 2:.1f} {cy - vh / 2:.1f} {vw:.1f} {vh:.1f}"
    hub = NETWORK["stations"]["E1"]
    svg = svg_inline(POSTER_PRINT, f"The poster's hub at print size: station E1, {hub['name']}, where {count_word(len(hub['loops']))} loop lines meet, with the lines, bullets and labels around it.", width=w_css, viewbox=vb, cls="hub")
    return ('<h3 id="hub-h">The hub at 1:1, as it prints</h3>'
            f'<figure>{scroll(f"<div class=\"hubframe\">{svg}</div>", "The poster hub at print size")}'
            f'<figcaption class="cap">A crop of the print drawing around E1, {esc(hub["name"])}, at the size it prints on the 24 by 36 inch sheet, '
            'taking a CSS inch as 96 px. The print drawing is the poster scaled 2.4 times, with each line bullet carrying its kind glyph. '
            'Screens differ in density, so treat the size as close, not exact. On a phone the frame scrolls.</figcaption></figure>')


def r8_card():
    return ('<h3 id="r8-h">The R8 card you pointed to, with its catalog tile and the locator lit</h3>'
            '<p class="sec-intro">The R8 card from the Field Guide, at true size on White. Its catalog tile comes first, as the plate shows it. '
            'At top right of the card, the locator lights R8 on the poster\'s working map, so a reader can find the loop on the whole system.</p>'
            '<figure class="truesize">'
            f'{cap_img("r8-tile.jpg", "Catalog tile for loop R8 on plate A: the two boxes Housing scarcity and Owner home equity, the forward step and the return line, beside the loop ID, its title and its read-aloud sentence.", cls="fit edge")}'
            '<figcaption class="cap"><b>The catalog tile.</b> R8 leads plate A, Economic structure.</figcaption></figure>'
            '<figure class="truesize" style="margin-top:20px">'
            f'{cap_img("r8-card.jpg", "Loop card R8 on White: the headline Scarce homes build owners’ equity, which keeps homes scarce; the loop drawn as two boxes with a forward step L38 and a red return line L39 where reform R-30 acts; the locator at top right with R8 lit in Charcoal on the working map; a rail on how the loop behaves; and the reform panel for R-30 with its effects and routes.", cls="fit edge")}'
            '<figcaption class="cap"><b>The R8 card</b>, from the Field Guide board, at true size. The one working red marks where reform R-30 acts.</figcaption></figure>')


def catalog_page():
    return ('<h3 id="catalog-h">The catalog page, as a page</h3>'
            '<p class="sec-intro">The Charcoal head teaches R8 at full size with five numbered callouts, then plate A begins. At 1440 px first, then at 390 px.</p>'
            '</div><div class="band plain"><div class="band-in">'
            f'<figure>{cap_img("catalog-1440.jpg", "Catalog page at 1440 px: the Charcoal head with the display line Twenty-three loops, the R8 card drawn at full size with five numbered callouts and the key that explains them, then plate A, Economic structure, with its locator and the tiles for R8, R1, R5 and R6.", cls="fit")}'
            '<figcaption class="cap">At 1440 px, the head and plate A.</figcaption></figure></div></div><div class="wrap">'
            f'<figure class="phone">{scroll(cap_img("catalog-390.jpg", "The same catalog head and plate A at 390 px: the head stacks the R8 drawing above its five callouts, and the plate stacks its tiles one to a row."), "Catalog page at 390 px, scrollable", cls="tall")}'
            '<figcaption class="cap">At 390 px. The frame scrolls through the head and plate A.</figcaption></figure>')


def sign_choice():
    c3 = [b for t, b in choices if t.startswith("Choice 3")][0]
    figs = []
    for name, info in sorted(((k, v.get("info", {})) for k, v in MANIFEST.items() if k.startswith("sign-")), key=lambda kv: kv[0]):
        option = info.get("option", "")
        tag = ' <span class="tag rec">Studio recommendation</span>' if re.search(r"pointing tag", option, re.I) and re.search(r"Recommended: the pointing tag", c3) else ""
        figs.append(f'<figure class="truesize"><p class="ba-label">{esc(option)}{tag}</p>'
                    f'{cap_img(name, f"Loop card R8 drawn with {option.split(":", 1)[-1].strip()}: the same card as above, with the steps between Housing scarcity and Owner home equity marked this way.", cls="fit edge")}</figure>')
    return ('<h3 id="sign-h">Choice 3: one sign mark, the R8 card both ways</h3>'
            '<p class="sec-intro">The same card twice, at true size. Only the sign mark changes, and the reform foot is left off both.</p>'
            + '<div class="stack-lg">' + "".join(figs) + "</div>")


def current_system():
    cat = os.path.join(ROOT, "work", "research", "chat-references", "20261028_Ref-Atlas-Loop-Catalog-Current.png")
    r8 = os.path.join(ROOT, "work", "research", "chat-references", "20261028_Ref-Atlas-Loop-R8-Concept-08.webp")
    return ('<h3 id="current-h">The current system, the fallback</h3>'
            '<p class="sec-intro">Concepts V2 stays the fallback if you choose none of the above (G1-11). Its R8 card and its loop catalog, at the same sizes as the pick\'s.</p>'
            '<figure class="truesize">'
            f'{img(r8, "Concept 08 loop card for R8 from Concepts V2: Housing scarcity and Owner home equity as boxes, a forward arrow, and a red return line marking where reform R-30 enters.", width=1248, cls="fit edge")}'
            '<figcaption class="cap"><span class="tag solid">Fallback</span> The current R8 card, Concept 08, at the same width as the Field Guide card above.</figcaption></figure>'
            '</div><div class="band plain"><div class="band-in">'
            f'<figure>{img(cat, "The current loop catalog from Concepts V2: 23 loops, each drawn on the same ring with ID circles, grouped by area A to D.", width=1440, cls="fit")}'
            '<figcaption class="cap"><span class="tag solid">Fallback</span> The current loop catalog, at the width of the catalog page above. It draws every loop on the same ring.</figcaption></figure></div></div><div class="wrap">')


# ---------------------------------------------------------------- icons

PILLARS = ["Explain", "Track", "Connect", "Act"]
TEN = ["Explain", "Track", "Connect", "Act", "Ballot", "Bill", "Testify", "Housing", "Campaign money", "Feedback loop"]
OPEN = {"Ballot", "Campaign money", "Testify"}
HOLDERS = [("Square", "Square"), ("Rounded-Square", "Rounded square"), ("Circle", "Circle")]
CHOICE2 = [b for t, b in choices if t.startswith("Choice 2")][0]


def slug(name):
    return "-".join(w[0].upper() + w[1:] for w in name.split())


def holders_panel():
    idea = re.split(r"(?<=\.)\s", CHOICE2.strip(), maxsplit=1)[0]
    cols = []
    for tile, frame in (("Charcoal", ""), ("Newsprint", "white")):
        rows = []
        for key, label in HOLDERS:
            marks = "".join(img(os.path.join(OVER, "holders", f"20261028_Overprint-{p}-{key}-{tile}.svg"), f"{p} in a {tile} {label.lower()}", width=96) for p in PILLARS)
            rows.append(f'<div class="hrow"><p class="lname">{esc(label)}</p><div class="marks">{marks}</div></div>')
        cols.append(f'<figure><div class="spec {frame}"><p class="tname">{tile} tile</p>{"".join(rows)}</div></figure>')
    ten = []
    for n in TEN:
        tag = '<span class="tag out open">Open drawing</span>' if n in OPEN else ""
        ten.append(f'<figure class="icon">{img(os.path.join(OVER, f"20261028_Overprint-{slug(n)}-Display.svg"), f"{n}, Overprint display master at 96 px", width=96)}<figcaption class="lab">{esc(n)}{tag}</figcaption></figure>')
    return ('<h3 id="holders-h">Overprint: the four pillar marks in three holders</h3>'
            f'<p class="idea">{inline(idea)}</p>'
            f'<div class="two holders">{"".join(cols)}</div>'
            '<p class="cap">At 96 px. The Newsprint tiles sit on White so their edges show.</p>'
            f'<h4>The ten icons, bare, at 96 px</h4><div class="spec">{scroll(f"<div class=\"tenrow\">{"".join(ten)}</div>", "The ten Overprint icons at 96 px")}</div>'
            f'<p class="cap">Open drawing marks the three the report names: {inline(re.search(r"three drawings are still open[^.]*\.", CHOICE2).group(0)) if re.search(r"three drawings are still open[^.]*\.", CHOICE2) else "Ballot, Campaign money and Testify."}</p>')


def app_and_menu():
    tile = os.path.join(OVER, "context", "20261028_Overprint-App-Tile-1024-62.svg")
    tiles = "".join(f'<figure class="cell">{img(tile, f"App tile, Act in the Charcoal superellipse, at {s} px", width=s)}<figcaption class="lab">{s} px</figcaption></figure>' for s in (180, 60, 29))
    rows = sorted(k for k in MANIFEST if k.startswith("menu-row-"))
    cap = MANIFEST.get("menu-row-1.png", {}).get("info", {}).get("caption", "")
    cap = re.sub(r"^\d+\.\s*", "", cap)
    menus = "".join(f'<div class="item">{cap_img(k, ("Menu row on Charcoal" if MANIFEST[k]["info"].get("dark") else "Menu row on Newsprint") + ": Explain, Track, Connect and Act at 24 px, with Track current, its red plane back, its label bold and a rule beneath it.")}</div>' for k in rows)
    return ('<h3 id="tile-h">The app tile, and the red in a menu</h3>'
            f'<div class="spec"><div class="lrow" style="flex-wrap:wrap;align-items:flex-end">{tiles}</div></div>'
            '<p class="cap">Act in the Charcoal superellipse, the corner iOS uses, with a live area of 62 percent of the side.</p>'
            f'<div class="spec white" style="margin-top:20px">{scroll(f"<div class=\"stack\">{menus}</div>", "Menu rows with Track current")}</div>'
            f'<p class="cap">{esc(cap)}</p>')


def small_sizes():
    def row(size, factor, label, tag=""):
        cells = []
        for n in TEN:
            p = os.path.join(OVER, "px", f"20261028_Overprint-{slug(n)}-{size}px-Newsprint.png")
            cells.append(f'<figure class="cell">{img(p, f"{n} at {size} px, actual size", cls="px")}{img(p, f"{n} at {size} px, magnified {factor} times without smoothing", factor=factor)}<figcaption class="lab">{esc(n)}</figcaption></figure>')
        return f'<div class="item"><p class="lab"><b style="color:#121212">{label}</b> {tag}</p><div class="lrow" style="gap:14px;flex-wrap:wrap">{"".join(cells)}</div></div>'
    return ('<h3 id="small-h">Small sizes: the 16 px solid cut beside the 24 px line</h3>'
            f'<div class="spec">{scroll("<div class=\"stack\">" + row(24, 4, "24 px line, with its red plane") + row(16, 6, "16 px solid cut, one color", "<span class=\"tag out\">Open drawing</span>") + "</div>", "Overprint at 24 and 16 px")}</div>'
            '<p class="cap">Each cell is the board\'s own render at 1x, then the same pixels magnified, drawn as squares with no smoothing. The 16 px cut is the least finished part of the family, and it gets its own pass first (R14).</p>')


def others_strip():
    op = [r for r in icon_rows if r[0].startswith("Overprint")]
    blocks = []
    for key, folder, prefix in (("Moving part", "moving-part", "Moving-Part"), ("Public sign", "public-sign", "Public-Sign")):
        icons = "".join(img(os.path.join(ICONS, folder, f"20261028_{prefix}-{slug(n)}-Display.svg"), f"{n}, {key}", width=48) for n in TEN)
        score = [r for r in icon_rows if r[0].startswith(key)]
        if key == "Moving part":
            col = name_head.index("Moving part") if "Moving part" in name_head else None
            chosen = [r for r in name_rows if r[0].startswith("Chosen")]
            line = (f"It scores {score[0][7]} on beauty where Overprint scores {op[0][7]}." if score and op else "")
            if chosen and col:
                line += f" Raters who compared the families chose it: {chosen[0][col].lower()}." 
            test = " · ".join(f"{r[0]}: {r[col]}" for r in name_rows) if col else ""
        else:
            stop = re.search(r"^Public sign stopped[^\n]*", s3, flags=re.M)
            line = (f"It scores {score[0][2]} on clarity and {score[0][7]} on beauty." if score else "")
            test = stop.group(0) if stop else ""
        blocks.append(f'<div class="other"><p class="oname">{esc(key)}</p><div class="spec">{scroll(f"<div class=\"lrow\" style=\"gap:10px;flex-wrap:wrap\">{icons}</div>", key + " icons at 48 px")}</div>'
                      f'<p class="small"><b>Why it ranks lower.</b> {esc(line)}</p><p class="small"><b>Name test.</b> {inline(test)}</p></div>')
    return '<h3 id="others-h">The other two concepts</h3><div class="others">' + "".join(blocks) + "</div>"


# ---------------------------------------------------------------- tables and decisions

def score_table(head, rows, label):
    th = "".join(f'<th scope="col"{" class=\"n\"" if k else ""}>{esc(h)}</th>' for k, h in enumerate(head))
    body = []
    for r in rows:
        cells = [f'<th scope="row">{inline(r[0])}</th>']
        for c in r[1:]:
            m = re.fullmatch(r"\s*([1-5])\s*", c)
            cells.append(f'<td class="s s{m.group(1)}">{esc(c)}</td>' if m else f"<td>{inline(c)}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="table" tabindex="0" role="region" aria-label="{attr(label)}"><table><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def text_table(head, rows, label, idcol=False):
    th = "".join(f'<th scope="col">{esc(h)}</th>' for h in head)
    body = "".join("<tr>" + "".join((f'<th scope="row">{inline(c)}</th>' if k == 0 else f"<td>{inline(c)}</td>") for k, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="table" tabindex="0" role="region" aria-label="{attr(label)}"><table class="{"ids" if idcol else ""}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


KEY = '<div class="key"><span><i style="background:var(--low-bg)"></i>1 or 2</span><span><i style="background:var(--mid-bg)"></i>3</span><span><i style="background:var(--ok-bg)"></i>4 or 5</span></div>'


def scores_html():
    lead = [p for p in s3.strip().split("\n\n") if p.strip() and not p.lstrip().startswith(("|", "**"))]
    note = re.search(r"\*\*Name test[^\n]*", s3)
    icon_note = re.search(r"^The creative director's final scores[^\n]*", s3, flags=re.M)
    stop = re.search(r"^Public sign stopped[^\n]*", s3, flags=re.M)
    nt = note.group(0).replace("**Name test, at 24 px**, ", "") if note else ""
    nt = nt[:1].upper() + nt[1:]
    return ((f"<p>{inline(lead[0].strip())}</p>" if lead else "") + KEY
            + '<h3 id="scores-maps">Maps</h3><p class="small">The creative director\'s scores after the fix pass.</p>' + score_table(maps_head, maps_rows, "Map scores")
            + f'<h3 id="scores-icons">Icons</h3><p class="small">{inline(icon_note.group(0)) if icon_note else ""}</p>' + score_table(icon_head, icon_rows, "Icon scores")
            + f'<h3 id="name-test">The name test, at 24 px</h3><p class="small">{inline(nt)}</p>'
            + text_table(name_head, name_rows, "Name test results at 24 px")
            + (f'<p class="cap">{inline(stop.group(0))}</p>' if stop else ""))


SPECIMEN_LINKS = {"1": ("#maps", "the maps above"), "2": ("#icons", "the icons above"), "3": ("#sign-h", "the two R8 cards above")}


def choices_html():
    out = []
    for t, body in choices:
        n = re.match(r"Choice (\d+)", t).group(1)
        name = t.split(". ", 1)[1] if ". " in t else t
        rec = re.search(r"Recommended: ([^.]+)", body)
        if rec:
            rec_text = rec.group(1)
        else:
            opt = re.search(r"Options: ([^\n]*)", body)
            pick = re.search(r"([^;:]+?) \(recommended\)", opt.group(1)) if opt else None
            rec_text = pick.group(1).strip() if pick else "See the options."
        href, what = SPECIMEN_LINKS.get(n, ("#maps", "above"))
        out.append(f'<article class="choice" id="choice-{n}" aria-labelledby="choice-{n}-h"><p class="eyebrow">Choice {n} of {len(choices)}</p><h4 id="choice-{n}-h">{esc(name)}</h4>'
                   f'<div class="prose">{md_blocks(body)}</div>'
                   f'<p class="verdict-line"><span class="tag rec">Studio recommendation</span> {inline(rec_text[0].upper() + rec_text[1:])}. <a href="{href}">See {what}</a>.</p></article>')
    return "".join(out)


def calls_html():
    cards = []
    for r in call_rows:
        cid, call, what, why = r[0], r[1], r[2], r[3]
        cards.append(f'<article class="fix" id="call-{cid}" aria-labelledby="call-{cid}-h"><div class="fix-head"><span class="fix-id">{esc(cid)}</span><h4 id="call-{cid}-h">{inline(call)}</h4></div>'
                     f'<dl class="fix-dl"><div><dt>What changes</dt><dd>{inline(what)}</dd></div><div><dt>Why</dt><dd>{inline(why)}</dd></div></dl></article>')
    return "".join(cards)


def set_html():
    body = "".join(f'<tr><td class="id">{esc(r[0])}</td><td>{inline(r[1])}</td></tr>' for r in set_rows)
    return f'<div class="table" tabindex="0" role="region" aria-label="Studio recommendations R1 to R{len(set_rows)}"><table class="settable"><colgroup><col style="width:4.5em"><col></colgroup><thead><tr><th scope="col">ID</th><th scope="col">{esc(set_head[1])}</th></tr></thead><tbody>{body}</tbody></table></div>'


def files_html():
    out = [f'<li><code>{esc(os.path.relpath(REPORT, ROOT))}</code>: the report this page is built from</li>']
    boards = sorted(glob.glob(os.path.join(BOARDS, "20261028_*.html")))
    appendix = []
    for b in boards:
        name = os.path.basename(b)
        if os.path.abspath(b) == os.path.abspath(OUT):
            continue
        if not re.search(r"Map-Direction|Systems-Map-Directions|Icon-Concept", name):
            if "Identity-Masters" in name:
                out.append(f'<li><code>work/boards/{esc(name)}</code>: the approved identity masters with ampersand B refined, which come to you at Gate 2</li>')
            continue
        t = re.search(r"<title>(.*?)</title>", read(b)[:4000], flags=re.S)
        appendix.append(f'<li><code>work/boards/{esc(os.path.basename(b))}</code>: {esc(strip_tags(t.group(1))) if t else ""}</li>')
    handoffs = os.path.join(ROOT, "work", "handoffs", "phase-2")
    notes = sorted({"work/handoffs/phase-2/" + os.path.basename(n) for n in re.findall(r"`((?:work/handoffs/phase-2/)?2026\d{4}_[^`/]+\.md)`", report)
                    if os.path.exists(os.path.join(handoffs, os.path.basename(n)))})
    note_items = "".join(f"<li><code>{esc(n)}</code></li>" for n in notes)
    return ("".join(out), "".join(appendix), note_items)


# ---------------------------------------------------------------- assemble

page = read(os.path.join(DR, "direction-review.template.html"))
files, appendix, notes = files_html()
fills = {
    "title": esc(title),
    "decide_items": "".join(f"<li>{link_sections(inline(x))}</li>" for x in decide_items),
    "reply_intro": esc(reply_intro),
    "reply": esc(reply),
    "reply_after": esc(reply_after),
    "poster": poster_band(),
    "hub": hub_crop(),
    "r8": r8_card(),
    "catalog": catalog_page(),
    "sign": sign_choice(),
    "current": current_system(),
    "holders": holders_panel(),
    "tile_menu": app_and_menu(),
    "small": small_sizes(),
    "others": others_strip(),
    "scores": scores_html(),
    "choices": choices_html(),
    "calls": calls_html(),
    "calls_count": count_word(len(call_rows)).capitalize(),
    "set": set_html(),
    "set_count": count_word(len(set_rows)).capitalize(),
    "q13": md_blocks(s7),
    "risks": md_blocks(s8),
    "next": md_blocks(s9),
    "files": files,
    "appendix": appendix,
    "notes": notes,
}
for key, value in fills.items():
    need("{{" + key + "}}" in page, f"template has no {{{{{key}}}}}")
    page = page.replace("{{" + key + "}}", value)
left = re.findall(r"\{\{[a-z_0-9]+\}\}", page)
need(not left, f"unfilled placeholders: {left}")
need(page.startswith("<title>"), "page must start with <title>")
need("#E63946" not in page.split("</style>", 1)[0], "Pillar Red found in the page's own stylesheet")
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
size = os.path.getsize(OUT)
need(size < 10 * 1024 * 1024, f"page is {size} bytes, over 10 MB")
print(f"{OUT}: {size / 1024 / 1024:.2f} MB, {len(EMBEDDED)} images embedded, {len(SCOPES)} inline SVGs, "
      f"{len(choices)} choices, {len(call_rows)} calls, {len(set_rows)} recommendations, {len(WARNINGS)} warnings")
for w in WARNINGS:
    print("  warning: " + w)
if "--check" in FLAGS:
    run_node("check_direction_review.js")
