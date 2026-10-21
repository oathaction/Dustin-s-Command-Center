"""Build the combined Gate 1 review board from its template, the Gate 1 report and the five Phase 1 boards.

Usage:
    python3 -I build_gate1_board.py <project-root> [--report PATH] [--out PATH]

Every table, the approval list, the sample reply and the prose of the seven big calls come from the
report at build time, so the board and the report cannot disagree. Section 3 renders as a pending
note while it reads RUBRIC_PENDING, and as a table once it holds a Markdown table whose header row
starts "| Proposal | Cr |". Rerun the script after editing the report.

Images: the 16 and 24 px cells are the boards' own 1x renders, embedded at natural size and magnified
without smoothing. Larger layouts are Playwright element screenshots at device scale 2 from
capture_gate1_images.js, shown at half their pixel width. Vector masters are inlined as SVG.
The output is one self-contained file: every image is a data URI and every SVG is inline.
"""
import base64
import html
import json
import os
import re
import struct
import sys

# ---------------------------------------------------------------- paths and arguments

args = sys.argv[1:]
if not args:
    raise SystemExit(__doc__)
ROOT = os.path.abspath(args[0])
opts = dict(zip(args[1::2], args[2::2]))
BOARDS = os.path.join(ROOT, "work", "boards")
P1 = os.path.join(BOARDS, "phase-1")
IDPNG = os.path.join(P1, "identity", "png")
IDSVG = os.path.join(P1, "identity")
SYMPX = os.path.join(P1, "symbols", "px")
GATE = os.path.join(P1, "gate-1")
IMG = os.path.join(GATE, "img")
SPRITE = os.path.join(ROOT, "work", "extract", "v5-polished", "sprite")
REPORT = opts.get("--report", os.path.join(ROOT, "work", "ledger", "20261021_Gate-1-Report.md"))
OUT = opts.get("--out", os.path.join(BOARDS, "20261021_Gate-1-Review-Board.html"))
TOKENS = os.path.join(ROOT, "work", "build", "tokens", "20261021_Token-Schema-Draft.json")
VOICE = os.path.join(ROOT, "work", "handoffs", "phase-1", "20261021_Voice-Line-And-Headlines.md")

IDENTITY_BOARD = "20261021_Identity-Refinement-Board.html"
SYMBOL_BOARD = "20261021_Symbol-Family-Board.html"
STRATEGY_BOARD = "20261021_Strategy-And-Direction-Board.html"
SYSTEMS_BOARD = "20261021_Systems-Marks-Board.html"
NAV_BOARD = "20261021_Navigation-And-Template-Wireframes.html"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def need(cond, msg):
    if not cond:
        raise SystemExit("build_gate1_board: " + msg)


# ---------------------------------------------------------------- text helpers

def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


def inline(s):
    """Markdown inline subset used by the report: `code` and **bold**."""
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


SECTION_ANCHORS = {"3": "#scores", "4": "#calls", "5": "#fixes", "6": "#set", "7": "#risks", "9": "#phase2", "10": "#questions"}


def link_sections(h):
    return re.sub(r"\b([Ss]ection) (\d+)\b", lambda m: f'<a href="{SECTION_ANCHORS[m.group(2)]}">{m.group(1)} {m.group(2)}</a>' if m.group(2) in SECTION_ANCHORS else m.group(0), h)


def md_blocks(text, skip=None):
    """Paragraphs, blockquotes, ordered and bulleted lists. Tables and headings are skipped."""
    lines = text.strip("\n").split("\n")
    out, i = [], 0
    start = lambda l: l.startswith(("|", ">", "- ", "#")) or re.match(r"\d+\. ", l)
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("|") or line.startswith("#"):
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
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not start(lines[i]):
                buf.append(lines[i].strip())
                i += 1
            para = " ".join(buf)
            if skip and skip(para):
                continue
            out.append(f"<p>{inline(para)}</p>")
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
    """(header, rows) of the Markdown table whose header line starts with header_prefix."""
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


def tidy(s):
    return re.sub(r"\s+([.,;:)])", r"\1", s)


# ---------------------------------------------------------------- source boards

def board(name):
    return read(os.path.join(BOARDS, name))


def board_section(src, sid):
    s = src.index(f'<section id="{sid}"')
    return src[s: src.index("</section>", s)]


def board_table(fragment, label):
    """Rows of the table that follows aria-label=label, as lists of cell text."""
    k = fragment.index(f'aria-label="{label}"')
    t = fragment[fragment.index("<table", k): fragment.index("</table>", k)]
    rows = []
    for tr in re.findall(r"<tr>(.*?)</tr>", t, flags=re.S):
        rows.append([tidy(strip_tags(c)) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, flags=re.S)])
    return rows[0], rows[1:]


def html_table(header, rows, label, numeric_from=1, row_header=True, cls="table", spec=False):
    th = "".join(f'<th scope="col"{" class=\"n\"" if k >= numeric_from else ""}>{esc(h)}</th>' for k, h in enumerate(header))
    body = []
    for r in rows:
        cells = []
        for k, c in enumerate(r):
            if k == 0 and row_header:
                cells.append(f'<th scope="row">{esc(c)}</th>')
            else:
                cells.append(f'<td{" class=\"n\"" if k >= numeric_from else ""}>{esc(c)}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    table = f'<table><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table>'
    if spec:
        return f'<div class="scroll" tabindex="0" role="region" aria-label="{attr(label)}">{table}</div>'
    return f'<div class="{cls}" tabindex="0" role="region" aria-label="{attr(label)}">{table}</div>'


# ---------------------------------------------------------------- images and SVG

EMBEDDED = {}


def image_size(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5: i + 9])
                return w, h
            seg = struct.unpack(">H", data[i + 2: i + 4])[0]
            i += 2 + seg
    raise SystemExit(f"cannot read image size: {path}")


def data_uri(path):
    if path not in EMBEDDED:
        need(os.path.exists(path), f"missing image {path}")
        mime = "image/png" if path.endswith(".png") else "image/jpeg"
        with open(path, "rb") as f:
            EMBEDDED[path] = f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    return EMBEDDED[path]


USES = []


def img(path, alt, scale=1, factor=None, cls="", style=""):
    pw, ph = image_size(path)
    if factor:
        w, h = pw * factor, ph * factor
        cls = (cls + " px").strip()
    else:
        w, h = round(pw / scale), round(ph / scale)
    USES.append(os.path.relpath(path, ROOT))
    c = f' class="{cls}"' if cls else ""
    s = f' style="{style}"' if style else ""
    return f'<img src="{data_uri(path)}" width="{w}" height="{h}" alt="{attr(alt)}"{c}{s} decoding="async">'


def svg_root_size(markup):
    vb = re.search(r'viewBox="([^"]+)"', markup).group(1).split()
    return float(vb[2]), float(vb[3])


def svg_inline(source, label, height=None, width=None, cls="", style="", is_text=False):
    t = source if is_text else read(source)
    t = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", t, flags=re.S).strip()
    t = re.sub(r"<title>.*?</title>|<desc>.*?</desc>", "", t, flags=re.S)
    t = re.sub(r'\s(id)="[^"]*"', "", t)
    vbw, vbh = svg_root_size(t)
    if height:
        width = height * vbw / vbh
    elif width:
        height = width * vbh / vbw
    else:
        width, height = vbw, vbh
    root = re.match(r"<svg\b[^>]*>", t).group(0)
    new = re.sub(r'\s(width|height|style|role|aria-label|class)="[^"]*"', "", root)
    extra = f' role="img" aria-label="{attr(label)}" width="{width:.2f}" height="{height:.2f}" focusable="false"'
    if cls:
        extra += f' class="{cls}"'
    if style:
        extra += f' style="{style}"'
    new = new[:-1] + extra + ">"
    return new + t[len(root):]


def idpng(folder, name):
    return os.path.join(IDPNG, folder, name)


# ---------------------------------------------------------------- report

report = read(REPORT)
sections = split_headings(report, 2)
title_line = report.split("\n", 1)[0]
need(title_line.startswith("# Gate 1 report: "), "report title line changed")
title = title_line.split(": ", 1)[1]
title = title[0].upper() + title[1:]
need("waiting for Dustin's approval" in report, "status line changed")

approve = section(sections, "What you are asked to approve")
paras = [p.strip() for p in approve.strip().split("\n\n")]
lede = paras[0]
approve_list = [re.sub(r"^\d+\. ", "", l) for l in approve.split("\n") if re.match(r"\d+\. ", l)]
need(len(approve_list) == 4, "approval list should have four items")
m = re.search(r'^(A reply can be this short:) "(.+)"\s*$', approve, flags=re.M)
need(m, "sample reply not found")
reply_intro, reply = m.group(1), m.group(2)
after = [p for p in paras if p.startswith("Section 10")]
need(after, "closing approval paragraph not found")

s4 = section(sections, "4. ")
calls_head, call_rows = md_table(s4, "| # | Call |")
need(len(call_rows) == 7, "expected seven big calls")
call_prose = {t.split(".", 1)[0]: (t.split(". ", 1)[1], body) for t, body in split_headings(s4, 3)}
need(sorted(call_prose) == [str(n) for n in range(1, 8)], "expected ### 1. to ### 7. in section 4")
l_note = [p for p in s4.split("\n\n") if p.strip().startswith("**L** marks")]
need(l_note, "L note missing")

s5 = section(sections, "5. ")
fix_head, fix_rows = md_table(s5, "| ID | Fix |")
need([r[0] for r in fix_rows] == ["I1", "I2", "I3", "I7", "I8", "S9"], "fix IDs changed")
fix_after = [p.strip() for p in s5.split("\n\n") if p.strip() and not p.strip().startswith("|")]

s6 = section(sections, "6. ")
set_head, set_rows = md_table(s6, "| ID | Question |")
need(len(set_rows) == 22, f"expected 22 recommendations, found {len(set_rows)}")

s3 = section(sections, "3. ")
s7 = section(sections, "7. ")
s9 = section(sections, "9. ")
s10 = section(sections, "10. ")
q_head, q_rows = md_table(s10, "| # | Question |")
risks = [l[2:] for l in s7.split("\n") if l.startswith("- ")]
board_files = re.findall(r"^- `(2026\d{4}_[^`]+\.html)`", report, flags=re.M)
need(len(board_files) == 5, "five board files expected in the report header")


def find_sentence(text, pattern):
    m = re.search(pattern, text)
    need(m, f"sentence not found: {pattern}")
    return m.group(0)


def find_risk(prefix):
    hits = [r for r in risks if r.startswith(prefix)]
    need(len(hits) == 1, f"risk not found: {prefix}")
    return hits[0]


COSTS = {
    "1": lambda: find_risk("Ampersand B is a first drawing."),
    "2": lambda: find_sentence(call_prose["2"][1], r"It costs double work[^.]*\."),
    "3": lambda: find_sentence(call_prose["3"][1], r"The display master holds[^.]*\."),
    "4": lambda: find_sentence(call_prose["4"][1], r"The cost is that[^.]*\."),
    "5": lambda: find_sentence(call_prose["5"][1], r"A's Act mark at 16 px[^.]*\."),
    "6": lambda: find_risk('"From spectators to stewards." with no role'),
    "7": lambda: find_sentence(call_prose["7"][1], r"Each position piece puts[^.]*\."),
}

EVIDENCE = {
    "1": [(IDENTITY_BOARD, "items 4 and 5", "#item-4, #item-5")],
    "2": [(IDENTITY_BOARD, "item 6", "#item-6")],
    "3": [(IDENTITY_BOARD, "item 7", "#item-7"), (SYSTEMS_BOARD, "mark 7, with the five separation rules", "#m7")],
    "4": [(IDENTITY_BOARD, "item 10", "#item-10")],
    "5": [(SYMBOL_BOARD, "sections 3, 4 and 5", "#direction-a, #direction-b, #track-act")],
    "6": [(STRATEGY_BOARD, "section 4, The lines", "#lines"), ("work/handoffs/phase-1/20261021_Voice-Line-And-Headlines.md", "section 1", None)],
    "7": [(STRATEGY_BOARD, "sections 5 and 6, the Act pattern and the rules", "#act, #rules")],
}

idb = board(IDENTITY_BOARD)
symb = board(SYMBOL_BOARD)
sysb = board(SYSTEMS_BOARD)


def pair_title(pid):
    m = re.search(rf'<div class="pair" id="{pid}"><h3>(.*?)</h3>', idb)
    need(m, f"identity pair {pid} not found")
    return strip_tags(m.group(1))


# ---------------------------------------------------------------- shared specimen builders

def cell(path, size_label, alt, factor=None):
    return f'<figure class="cell">{img(path, alt, factor=factor)}<figcaption class="lab">{esc(size_label)}</figcaption></figure>'


def scroll(inner, label, cls=""):
    return f'<div class="scroll {cls}" tabindex="0" role="region" aria-label="{attr(label)}">{inner}</div>'


def ladder_row(name, sub, files, what, mags=((16, 8), (24, 6))):
    """files: dict size -> path for 16, 24, 48, 96. Natural sizes, then magnified small sizes."""
    cells = [cell(files[s], f"{s} px", f"{what} at {s} px, actual size") for s in (16, 24, 48, 96) if s in files]
    mag = [cell(files[s], f"{s} px at {f}x", f"{what} at {s} px, magnified {f} times without smoothing", factor=f) for s, f in mags if s in files]
    lname = f'<p class="lname">{esc(name)}<span>{esc(sub)}</span></p>' if sub else f'<p class="lname">{esc(name)}</p>'
    return f'<div class="lrow">{lname}{"".join(cells)}<span class="gap" aria-hidden="true"></span>{"".join(mag)}</div>'


def spec_figure(inner, caption, cls=""):
    return f'<figure><div class="spec {cls}">{inner}</div><figcaption class="cap">{caption}</figcaption></figure>'


# ---------------------------------------------------------------- one identity

def composite():
    sec = board_section(symb, "composite")
    caps = [tidy(strip_tags(c)) for c in re.findall(r'<figure class="comp">.*?<figcaption>(.*?)</figcaption>', sec, flags=re.S)]
    need(len(caps) == 3, "composite captions")
    note = re.search(r'<p class="cap"><span class="tag">Illustrative</span>(.*?)</p>', sec, flags=re.S)
    need(note, "composite note")
    alts = [
        "Portrait Act post on Newsprint. At the top, the wordmark with ampersand B at today's width. Below it the Act mark with its red handle and the word ACT, the headline How to speak at a public hearing in your state, the V2 hinge diagram as a divider with a Charcoal ampersand, three numbered steps, and a row of the four pillar marks labeled Explain, Track, Connect and Act.",
        "The same portrait Act post with the wordmark at the condensed 7.5 to 1 width, which stands taller in the same space. Everything below the wordmark is unchanged.",
        "The same portrait Act post with the wordmark covered by a gray bar and the hinge diagram's words covered. The Act mark, the hinge ring, nodes, arcs and ampersand, the steps and the pillar row stay visible.",
    ]
    files = ["post-today-width.jpg", "post-condensed-width.jpg", "post-wordmark-covered.jpg"]
    figs = "".join(f'<figure>{img(os.path.join(IMG, f), a, scale=2)}<figcaption class="cap">{esc(c)}</figcaption></figure>' for f, a, c in zip(files, alts, caps))
    return f'<div class="posts">{figs}</div><p class="cap"><span class="illus">Illustrative</span> {esc(tidy(strip_tags(note.group(1))))}</p>'


# ---------------------------------------------------------------- the seven calls

def sizes(folder, who, surface="newsprint", mode="color"):
    return {s: idpng(folder, f"{who}__{surface}__{mode}__{s}.png") for s in (16, 24, 48, 96)}


def call1():
    a_title, b_title = pair_title("p04-amp"), pair_title("p05-amp")
    rows = [
        ladder_row("V5", "Lora Bold, in force", sizes("p04-amp", "orig"), "V5's red ampersand on Newsprint"),
        ladder_row("Option A", a_title.split(": ", 1)[-1], sizes("p04-amp", "prop"), "Option A's red ampersand on Newsprint"),
        ladder_row("Option B", b_title.split(": ", 1)[-1], sizes("p05-amp", "prop"), "Option B's red ampersand on Newsprint"),
    ]
    h = ['<h4>The glyph at 16, 24, 48 and 96 px</h4>']
    h.append(spec_figure(scroll(f'<div class="ladder">{"".join(rows)}</div>', "Ampersands at 16, 24, 48 and 96 px"),
                         "The identity board's own renders at 1x, in Pillar Red on Newsprint. The magnified cells draw each screen pixel as a square, with no smoothing."))
    disp = [
        (os.path.join(IDSVG, "01-reexport", "20261021_Amp-Master-Reexported.svg"), "V5", "Lora Bold, drawn with its full outline (fix I1)", "V5's ampersand, Lora Bold, at display size"),
        (os.path.join(IDSVG, "04-amp-a", "20261021_Amp-A-Display-Tune.svg"), "Option A", "V5's glyph tuned", "Option A's ampersand at display size"),
        (os.path.join(IDSVG, "05-amp-b", "20261021_Amp-B-Drawn-Master.svg"), "Option B", "Drawn, Oath & Action's own", "Option B's ampersand at display size"),
    ]
    cells = "".join(f'<div class="spec">{svg_inline(p, a, height=240, cls="fit", style="color:#E63946")}<p class="lab"><b style="color:#121212">{esc(n)}</b> · {esc(s)}</p></div>' for p, n, s, a in disp)
    h.append('<h4>At display size</h4>')
    h.append(f'<div class="display3">{cells}</div><p class="cap">The vector masters at 240 px tall, inlined from the identity board\'s files.</p>')
    con = re.search(r'<figure class="constr"><figcaption>(.*?)</figcaption>(<svg.*?</svg>)</figure>', idb, flags=re.S)
    need(con, "construction figure")
    con_svg = re.sub(r'\swidth="420"', ' width="420" height="458" class="fit"', con.group(2), count=1)
    sec5 = board_section(idb, "item-5")
    gh, gr = board_table(sec5, "Glyph table")
    gcap = re.search(r"Silhouette overlap[^<]*", sec5).group(0)
    h.append('<h4>How option B was drawn, and how close it sits to other serif ampersands</h4>')
    h.append(f'<div class="two"><figure><div class="spec white">{con_svg}</div><figcaption class="cap">{esc(strip_tags(con.group(1)))}</figcaption></figure>'
             f'<div>{html_table(gh, gr, "Silhouette overlap with options A and B")}<p class="cap">{esc(html.unescape(gcap))}</p></div></div>')
    wm = [
        (os.path.join(SPRITE, "wordmark.svg"), "V5, in force", "V5's wordmark with its Lora Bold ampersand"),
        (os.path.join(IDSVG, "03-wordmark-masters", "20261021_Wordmark-Display-Amp-A.svg"), "With option A", "The display wordmark with ampersand option A"),
        (os.path.join(IDSVG, "03-wordmark-masters", "20261021_Wordmark-Display-Amp-B.svg"), "With option B", "The display wordmark with ampersand option B"),
    ]
    items = "".join(f'<div class="item">{svg_inline(p, a, height=108, cls="fit", style="color:#121212")}<p class="lab">{esc(n)}</p></div>' for p, n, a in wm)
    h.append('<h4>In the display wordmark</h4>')
    h.append(spec_figure(f'<div class="stack">{items}</div>', "Options A and B sit in the display master of fix I3, which carries the hinge gaps of fix I2. The wordmarks are shown 108 px tall, scaled down on narrow screens."))
    return "".join(h)


def call2():
    cur = os.path.join(IDSVG, "03-wordmark-masters", "20261021_Wordmark-Display-Amp-B.svg")
    con = os.path.join(IDSVG, "06-condensed", "20261021_Wordmark-Condensed-7-5-To-1-Display.svg")
    (cw, ch), (kw, kh) = svg_root_size(read(cur)), svg_root_size(read(con))
    ratio = (kh / kw) / (ch / cw)
    items = (f'<div class="item">{svg_inline(cur, "The wordmark at today&#39;s width with ampersand B", width=640, cls="fit", style="color:#121212")}<p class="lab">Today\'s width, with ampersand B</p></div>'
             f'<div class="item">{svg_inline(con, "The condensed wordmark at 7.5 to 1, at the same width", width=640, cls="fit", style="color:#121212")}<p class="lab">Condensed 7.5 to 1, same width</p></div>')
    h = ['<h4>Same width, more height</h4>']
    h.append(spec_figure(f'<div class="stack">{items}</div>', f"Both drawings set to the same width. The condensed wordmark stands {ratio:.2f} times taller, measured from the two files."))
    rows = []
    for s, f in ((16, 4), (24, 4)):
        for who, name in (("orig", "Today's width"), ("prop", "Condensed 7.5 to 1")):
            p = idpng("p06-c75", f"{who}__newsprint__color__{s}.png")
            rows.append(f'<div class="item"><p class="lab"><b style="color:#121212">{esc(name)}, {s} px</b></p><div class="lrow">{cell(p, "actual size", f"{name} wordmark at {s} px, actual size")}{cell(p, f"magnified {f}x", f"{name} wordmark at {s} px, magnified {f} times without smoothing", factor=f)}</div></div>')
    h.append('<h4>At 16 and 24 px</h4>')
    h.append(spec_figure(scroll(f'<div class="stack">{"".join(rows)}</div>', "Wordmark widths at 16 and 24 px"), "Each width's own 16 and 24 px master, rendered at 1x by the identity board."))
    return "".join(h)


def call3():
    sec = board_section(idb, "item-7")
    names =["threeup__v5.png", "threeup__draft.png", "threeup__v2.png"]
    labels = [strip_tags(re.search(rf'<figcaption>([^<]*)</figcaption><img src="phase-1/identity/png/p07/{n}"', sec).group(1)) for n in names]
    alts = [
        "V5's hinge diagram: the wordmark under one dotted arc ending in an open arrowhead, with UNDERSTAND and IMPACT beneath.",
        "The withdrawn first draft: the ampersand in a circle on a line joining OATH and ACTION, with dotted arcs above and below.",
        "V2: the ampersand in a circle on a line joining OATH and ACTION with four nodes, two solid hairline arcs running clockwise, and UNDERSTAND and IMPACT beneath.",
    ]
    figs = "".join(f'<figure><div class="spec">{img(os.path.join(IDPNG, "p07", n), a, cls="fit")}</div><figcaption class="cap"><b>{esc(l)}</b></figcaption></figure>' for n, l, a in zip(names, labels, alts))
    cap = re.search(r"Each rendered 640 px wide[^<]*?\.", sec).group(0)
    master = os.path.join(IDSVG, "07-hinge", "20261021_Hinge-Display-Master_V2.svg")
    svg = svg_inline(master, "Hinge diagram V2 display master: OATH and ACTION on a line with four nodes, the red ampersand in a circle at the center, two solid hairline arcs running clockwise, and UNDERSTAND and IMPACT beneath", width=1100, style="color:#121212;width:100%;min-width:560px;height:auto")
    h = ['<h4>V5, the withdrawn first draft and V2</h4>', f'<div class="three">{figs}</div><p class="cap">{esc(cap)}</p>']
    h.append('<h4>The V2 display master</h4>')
    h.append(spec_figure(scroll(svg, "Hinge diagram V2 display master"), "The display master file, <code>work/boards/phase-1/identity/07-hinge/20261021_Hinge-Display-Master_V2.svg</code>, inlined as drawn. Below 560 px the frame scrolls, so the labels never draw under the master's 526 px minimum."))
    return "".join(h)


def call4():
    sec = board_section(idb, "item-10")
    th, tr = board_table(sec, "Treatment table")
    tcap = strip_tags(re.search(r'<p class="cap">(Median contrast of the ampersand.s pixels against Prussian.*?)</p>', sec, flags=re.S).group(1))
    treatments = [
        ("p10-display-only", "orig", tr[0][0], ""),
        ("p10-display-only", "prop", pair_title("p10-display-only").split(":")[0], "out"),
        ("p10-newsprint", "prop", pair_title("p10-newsprint").split(":")[0], ""),
        ("p10-keyline", "prop", pair_title("p10-keyline").split(":")[0], "out"),
        ("p10-mono", "prop", pair_title("p10-mono").split(":")[0], "rec"),
    ]
    tags = {"out": '<span class="tag out" style="color:#DCD9D2">Ruled out by the red rule</span>', "rec": '<span class="tag rec">Studio recommendation</span>', "": ""}
    r16, r96 = [], []
    for folder, who, name, t in treatments:
        p16 = idpng(folder, f"{who}__prussian__color__16.png")
        p96 = idpng(folder, f"{who}__prussian__color__96.png")
        what = f"Wordmark on Prussian, {name}"
        r16.append(f'<div class="lrow"><p class="lname">{esc(name)}<span>{tags[t]}</span></p>{cell(p16, "16 px", what + ", at 16 px, actual size")}{cell(p16, "16 px at 4x", what + ", at 16 px, magnified 4 times without smoothing", factor=4)}</div>')
        r96.append(f'<div class="item"><p class="lab"><b style="color:#DCD9D2">{esc(name)}</b> {tags[t]}</p>{img(p96, what + ", at 96 px tall, actual size")}</div>')
    h = ['<h4>On Prussian at 16 px</h4>']
    h.append(spec_figure(scroll(f'<div class="ladder">{"".join(r16)}</div>', "Treatments on Prussian at 16 px"), "V5 first, then options A to D. Renders at 1x from the identity board.", cls="prussian"))
    h.append('<h4>On Prussian at 96 px</h4>')
    h.append(spec_figure(scroll(f'<div class="stack">{"".join(r96)}</div>', "Treatments on Prussian at 96 px"), "The same treatments at 96 px tall.", cls="prussian"))
    h.append(html_table(th, tr, "Contrast on Prussian by treatment and size"))
    h.append(f'<p class="cap">{esc(tcap)}</p>')
    return "".join(h)


PILLARS = ["Explain", "Track", "Connect", "Act"]
TREATS = ["filled", "line", "tile"]


def psheet(d):
    head = '<div class="ps-row ps-head"><span></span>' + "".join(f'<span class="ps-group"><b>{t.capitalize()}</b><span class="ps-sizes"><i>16</i><i>24</i><i>48</i><i>96</i></span></span>' for t in TREATS) + "</div>"
    rows = []
    for p in PILLARS:
        groups = []
        for t in TREATS:
            what = f"Direction {d} {p} mark, {t}"
            c16 = img(os.path.join(SYMPX, f"n-{d}-{t}-{p.lower()}-16.png"), f"{what}, 16 px, actual size", cls="px")
            c24 = img(os.path.join(SYMPX, f"n-{d}-{t}-{p.lower()}-24.png"), f"{what}, 24 px, actual size", cls="px")
            c48 = img(os.path.join(IMG, f"sym-{d}-{t}-{p.lower()}-48.png"), f"{what}, 48 px", scale=2)
            c96 = img(os.path.join(IMG, f"sym-{d}-{t}-{p.lower()}-96.png"), f"{what}, 96 px", scale=2)
            groups.append(f'<span class="ps-group ps-cells">{c16}{c24}{c48}{c96}</span>')
        rows.append(f'<div class="ps-row"><span class="ps-name">{p}</span>{"".join(groups)}</div>')
    mags = []
    for t in TREATS:
        cells = "".join(cell(os.path.join(SYMPX, f"n-{d}-{t}-{p.lower()}-16.png"), f"{p}, 16 px at 6x", f"Direction {d} {p} mark, {t}, 16 px, magnified 6 times without smoothing", factor=6) for p in PILLARS)
        mags.append(f'<div class="item"><p class="lab"><b style="color:#121212">{t.capitalize()}, 16 px magnified</b></p><div class="lrow">{cells}</div></div>')
    return (scroll(f'<div class="psheet">{head}{"".join(rows)}</div>', f"Direction {d} pillar marks at 16, 24, 48 and 96 px")
            + scroll(f'<div class="stack" style="margin-top:20px">{"".join(mags)}</div>', f"Direction {d} marks at 16 px, magnified"))


def call5():
    a_intro = strip_tags(re.search(r'<h2 id="h-direction-a">(.*?)</h2>', symb).group(1))
    b_intro = strip_tags(re.search(r'<h2 id="h-direction-b">(.*?)</h2>', symb).group(1))
    h = [f'<h4>{esc(re.sub(r"^[0-9]+. ", "", a_intro))}</h4>', spec_figure(psheet("A"), "16 and 24 px: the symbol board's 1x cells at actual size. 48 and 96 px: captured from the symbol board at 2x. All in one color on Newsprint.")]
    h.append(f'<h4>{esc(re.sub(r"^[0-9]+. ", "", b_intro))}</h4>')
    h.append(spec_figure(psheet("B"), "The same sizes and treatments for Direction B."))
    sec = board_section(symb, "track-act")
    th, tr = board_table(sec, "Track against Act scores")
    intro = strip_tags(re.search(r"</span><p>(.*?)</p>", sec, flags=re.S).group(1))
    pairs = [("n-v5-track-16.png", "V5 Track"), ("n-v5-act-16.png", "V5 Act"), ("n-A-filled-track-16.png", "A Track"), ("n-A-filled-act-16.png", "A Act"), ("n-B-line-track-16.png", "B Track"), ("n-B-line-act-16.png", "B Act")]
    cells = "".join(f'<figure class="cell">{img(os.path.join(SYMPX, f), n + " at 16 px, actual size", cls="px")}{img(os.path.join(SYMPX, f), n + " at 16 px, magnified 6 times without smoothing", factor=6)}<figcaption class="lab">{n}, 16 px, and at 6x</figcaption></figure>' for f, n in pairs)
    h.append('<h4>Track and Act no longer look alike at 16 px</h4>')
    h.append(f'<div class="two"><div>{spec_figure(scroll(f"<div class=\"lrow\" style=\"flex-wrap:wrap\">{cells}</div>", "Track and Act at 16 px"), esc(intro))}</div><div>{html_table(th, tr, "Track against Act scores")}<p class="cap">From the symbol board, section 5. A pair passes under 0.60.</p></div></div>')
    return "".join(h)


def call6():
    voice = read(VOICE)
    vsec = split_headings(voice, 2)
    v1 = [b for t, b in vsec if t.startswith("1. Voice line")][0]
    orig = re.search(r'^Original, in force until Dustin approves a revision \(DC-04\): "(.+)"$', v1, flags=re.M)
    need(orig, "original voice line")
    vh, vr = md_table(v1, "| | Revision | Reason |")
    rec = re.search(r"\*\*Recommendation: ([ABC])\.\*\*", v1).group(1)
    cards = [f'<div class="line-card"><p class="head">V5 <span class="tag solid">In force</span></p><p class="says">"{esc(orig.group(1))}"</p><p class="small muted">The original, in force until you approve a revision (DC-04).</p></div>']
    for r in vr:
        isrec = r[0] == rec
        cards.append(f'<div class="line-card{" is-rec" if isrec else ""}"><p class="head">Revision {esc(r[0])}{" <span class=\"tag rec\">Studio recommendation</span>" if isrec else ""}</p><p class="says">{esc(r[1])}</p><p class="small">{inline(r[2])}</p></div>')
    ref = os.path.join(P1, "strategy", "refs", "20261021_Ref-Page-07.jpg")
    h = ['<h4>The voice line: V5 and three revisions</h4>', f'<div class="lines">{"".join(cards)}</div>',
         '<p class="cap">From the editor\'s voice line handoff, section 1, with each revision\'s reason.</p>',
         '<h4>"From spectators to stewards." in your references</h4>',
         f'<figure style="max-width:880px"><div class="spec">{img(ref, "Generated reference slide p07, a logo system: the condensed wordmark with a red ampersand above the line FROM SPECTATORS TO STEWARDS., repeated in the stacked logo, the horizontal lockup, the secondary lockups and two round seals.", cls="fit")}</div>'
         '<figcaption class="cap"><span class="illus">Generated reference, study only</span> Page 7 of <code>pics_i_like.pdf</code>, the logo system slide. It sets the line under the wordmark, beside each lockup and around two seals.</figcaption></figure>']
    return "".join(h)


def call7():
    a1 = "Mock layout of a process piece, every factual line tagged Illustrative: the kicker Act, How to take part; the headline Alder County votes on backyard cottages March 9. Here is how to weigh in; Who decides; What each side has said; a hinge divider; What you can do, with two dated steps; a red Send a comment button; and a line pointing to the tracker."
    a2 = "Mock layout of a position piece, every factual line tagged Illustrative: the label Our position before the headline State senate committees should post every vote within two days; What the record shows; a boxed section The strongest case against; What we don't know; a hinge divider; a disclosure above a red Ask your senator to vote yes button; and a line naming who decided the position and when."
    return ('<h4>The two kinds of Act piece</h4><div class="two">'
            f'<figure>{img(os.path.join(IMG, "act-mock-process.jpg"), a1, scale=2, cls="fit", style="border:1px solid var(--rule)")}<figcaption class="cap"><b>Process piece.</b> A step with a date and a place, taking no side.</figcaption></figure>'
            f'<figure>{img(os.path.join(IMG, "act-mock-position.jpg"), a2, scale=2, cls="fit", style="border:1px solid var(--rule)")}<figcaption class="cap"><b>Position piece.</b> Labeled "Our position", with the fairness kit.</figcaption></figure>'
            '</div><p class="cap"><span class="illus">Illustrative</span> Mock layouts from the strategy board, section 5. Every name, date, measure and figure in them is example copy, labeled Illustrative beside the item.</p>')


CALL_SPECIMENS = {"1": call1, "2": call2, "3": call3, "4": call4, "5": call5, "6": call6, "7": call7}


def evidence_line(n):
    parts = []
    for f, what, anchors in EVIDENCE[n]:
        a = f" (<code>{esc(anchors)}</code>)" if anchors else ""
        parts.append(f"<code>{esc(f)}</code>, {esc(what)}{a}")
    return '<p class="evidence"><b>Full evidence:</b> ' + "; ".join(parts) + ".</p>"


def calls_html():
    out = []
    for row in call_rows:
        n, name, ids, options, rec = row
        ptitle, body = call_prose[n]
        need(ptitle.lower().startswith(name.lower()[:12]), f"call {n} title mismatch: {ptitle!r} vs {name!r}")
        out.append(f'''<article class="call" id="call-{n}" aria-labelledby="call-{n}-h">
  <p class="eyebrow">Big call {n} of 7 · {esc(ids)}</p>
  <h3 id="call-{n}-h">{esc(ptitle)}</h3>
  <div class="call-body">
    <div class="prose">{md_blocks(body)}</div>
    <aside class="options" aria-labelledby="call-{n}-opt"><h4 id="call-{n}-opt">Options</h4><p>{inline(options)}</p></aside>
  </div>
  {CALL_SPECIMENS[n]()}
  <dl class="verdict">
    <div><dt>Studio recommendation</dt><dd>{inline(rec)}</dd></div>
    <div><dt>What it costs</dt><dd>{inline(COSTS[n]())}</dd></div>
    <div><dt>Decision IDs</dt><dd>{inline(ids)}</dd></div>
  </dl>
  {evidence_line(n)}
</article>''')
    return "\n".join(out)


def calls_table():
    head = "".join(f'<th scope="col">{esc(h)}</th>' for h in calls_head)
    rows = "".join(f'<tr><td class="id"><a href="#call-{r[0]}">{esc(r[0])}</a></td><th scope="row"><a href="#call-{r[0]}">{esc(r[1])}</a></th><td>{inline(r[2])}</td><td>{inline(r[3])}</td><td>{inline(r[4])}</td></tr>' for r in call_rows)
    return (f'<div class="table calltable" tabindex="0" role="region" aria-label="The seven big calls"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="cap">{inline(l_note[0].strip())}</p>')


# ---------------------------------------------------------------- the six fixes

def ba(before, after, grid=False):
    b = f'<div class="side"><p class="ba-label">Before, V5</p>{before}</div>'
    a = f'<div class="side"><p class="ba-label">After, the proposal</p>{after}</div>'
    return f'<div class="ba{" ba-grid" if grid else ""}">{b}{a}</div>'


def fix_I1():
    def side(who, tl_alt, amp_alt):
        tl = idpng("p01-tl-1", f"{who}__newsprint__mono__display.png")
        amp = idpng("p01-amp", f"{who}__newsprint__color__display.png")
        return f'<div class="spec"><div class="stack"><div class="item">{img(tl, tl_alt, cls="fit")}<p class="lab">Tagline, one line, 40 px tall</p></div><div class="item">{img(amp, amp_alt, cls="fit")}<p class="lab">Master ampersand, 240 px tall</p></div></div></div>'
    return ba(side("orig", "V5's tagline A country that answers to its people., with the bottoms of y and p cut off so it reads A countrv that answers to its peoole.", "V5's master ampersand, with the top of its loop and the tip of its tail cut off by its box"),
              side("prop", "The re-exported tagline with every descender whole", "The re-exported master ampersand with its full loop and tail"), grid=True)


def fix_I2():
    legend = strip_tags(re.search(r"Overlay legend for every panel: ([^.]*\.)", idb).group(1))
    o = lambda w, a: f'<div class="spec">{img(idpng("p02-optical", w), a, cls="fit")}</div>'
    return (ba(o("orig__newsprint__color__display.png", "V5's wordmark at display size, with the ampersand closer to ACTION than to OATH"),
               o("prop__newsprint__color__display.png", "The wordmark with option 2b spacing: the ampersand moved 1.42 units toward ACTION so both sides hold equal white"))
            + f'<figure><div class="spec">{img(idpng("p02-optical", "overlay__display.png"), "Overlay of V5 and the proposal at display size: the ampersand and ACTION show thin edges where they moved", cls="fit")}</div><figcaption class="cap"><b>Overlay.</b> {esc(legend)}</figcaption></figure>')


def small_pair(folder, name, mags=((16, 4), (24, 4))):
    def side(who, label):
        items = []
        for s, f in mags:
            p = idpng(folder, f"{who}__newsprint__color__{s}.png")
            items.append(f'<div class="item"><p class="lab">{s} px, actual size and at {f}x</p><div class="lrow">{img(p, f"{label} {name} at {s} px, actual size", cls="px")}{img(p, f"{label} {name} at {s} px, magnified {f} times without smoothing", factor=f)}</div></div>')
        return f'<div class="spec">{scroll(f"<div class=\"stack\">{"".join(items)}</div>", f"{label} {name} at small sizes")}</div>'
    return side("orig", "V5"), side("prop", "Proposed")


def fix_I3():
    b, a = small_pair("p03-masters", "wordmark")
    return ba(b, a) + '<p class="cap">The 16 and 24 px masters carry ampersand B, the studio\'s recommendation in call 1.</p>'


def fix_I7():
    b, a = small_pair("p08-lockmark", "lockmark", mags=((16, 6), (24, 6)))
    return ba(b, a, grid=True)


def fix_I8():
    def side(who, label):
        items = []
        for key, name, mag in (("L1", "L1 wordmark", 4), ("L5", "L5 wordmark and tagline", None), ("AMP", "Ampersand, freestanding", 8)):
            p = idpng("p09", f"{key}__{who}__newsprint__color.png")
            w, h = image_size(p)
            m = img(p, f"{label} {name} at its minimum, magnified {mag} times without smoothing", factor=mag) if mag else ""
            items.append(f'<div class="item"><p class="lab">{esc(name)}, {w} by {h} px at its minimum{f", and at {mag}x" if mag else ""}</p><div class="lrow">{img(p, f"{label} {name} at its minimum size, {w} by {h} px", cls="px")}{m}</div></div>')
        return f'<div class="spec">{scroll(f"<div class=\"stack\">{"".join(items)}</div>", f"{label} minimum sizes")}</div>'
    return ba(side("orig", "V5"), side("prop", "Proposed"), grid=True) + '<p class="cap">Each mark at its minimum, at 1x, from the identity board\'s item 9.</p>'


def badge_svg():
    t = read(os.path.join(IDSVG, "07-hinge", "20261021_Hinge-Display-Master_V2.svg"))
    ring = re.search(r'<circle cx="638.67" cy="54.0" r="110.0"[^>]*/>', t)
    nodes = re.findall(r'<circle cx="(?:528|748)\.67" cy="54.0" r="9.0"[^>]*/>', t)
    amp = re.search(r'<path fill="var\(--amp,#E63946\)" d="[^"]+"/>', t)
    need(ring and len(nodes) == 2 and amp, "hinge master parts for the badge")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="516.17 -60 245 228">{ring.group(0)}{"".join(nodes)}{amp.group(0)}</svg>'


def fix_S9():
    crop = os.path.join(IMG, "ref-p07-seals.jpg")
    bsvg = badge_svg()
    before = (f'<div class="spec">{img(crop, "Generated reference: four round seals and badges with rings of words such as FROM SPECTATORS TO STEWARDS around a red ampersand", scale=0.5, cls="fit")}'
              '<p class="lab"><span class="illus">Generated reference, study only</span> Your references p07, seals with a ring of words, enlarged 2x</p></div>'
              '<p class="small">V5: "Seals imply an authority we do not claim."</p>')
    after = (f'<div class="spec"><div class="lrow" style="flex-wrap:wrap;align-items:flex-end">{svg_inline(bsvg, "Wordless badge: the red ampersand inside the hinge circle with its two nodes, 200 px", height=200, cls="fit", style="color:#121212", is_text=True)}'
             f'{svg_inline(bsvg, "Wordless badge at 64 px", height=64, style="color:#121212", is_text=True)}</div><p class="lab">The ring, two nodes and ampersand of the V2 hinge display master, at 200 and 64 px</p></div>'
             '<p class="small">Cut from the hinge master at its own geometry. The strategy board describes the badge in words, and no separate badge master is drawn yet.</p>')
    return ba(before, after, grid=True)


FIX_SPECIMENS = {"I1": fix_I1, "I2": fix_I2, "I3": fix_I3, "I7": fix_I7, "I8": fix_I8, "S9": fix_S9}
FIX_SOURCE = {"I1": "identity board item 1", "I2": "identity board item 2", "I3": "identity board item 3", "I7": "identity board item 8", "I8": "identity board item 9", "S9": "strategy board sections 7 and 9"}


def fixes_html():
    out = []
    for fid, fix, what, why in fix_rows:
        defect = "(defect fix)" in why
        tag = ' <span class="tag solid">Defect fix</span>' if defect else ""
        out.append(f'''<article class="fix" id="fix-{fid}" aria-labelledby="fix-{fid}-h">
  <div class="fix-head"><span class="fix-id">{esc(fid)}</span><h3 id="fix-{fid}-h">{inline(fix)}</h3>{tag}</div>
  <dl class="fix-dl"><div><dt>What changes</dt><dd>{inline(what)}</dd></div><div><dt>Why</dt><dd>{inline(why)}</dd></div></dl>
  {FIX_SPECIMENS[fid]()}
  <p class="evidence"><b>Full evidence:</b> {esc(FIX_SOURCE[fid])}.</p>
</article>''')
    return "\n".join(out)


# ---------------------------------------------------------------- the set

def hexes():
    t = json.load(open(TOKENS, encoding="utf-8"))
    col = t["oa"]["color"]

    def resolve(v):
        if isinstance(v, str) and v.startswith("{"):
            node = t
            for k in v.strip("{}").split("."):
                node = node[k]
            return resolve(node["$value"])
        return v["hex"].upper()

    return t, col, resolve


NAMES = {"#DCD9D2": "Newsprint", "#121212": "Charcoal", "#FFFFFF": "White", "#1F2D5A": "Prussian", "#5D636D": "Stone", "#4A7C74": "Verdigris", "#4E535B": "Deep Stone", "#A3A19C": "Dim Newsprint", "#E63946": "Pillar Red"}


def lum(hx):
    c = [int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


TOKEN_REPORT = []


def token_strip():
    t, col, resolve = hexes()
    surfaces = [("newsprint", "Newsprint"), ("white", "White"), ("charcoal", "Charcoal"), ("prussian", "Prussian")]
    roles = [("Primary text", "text", ("text", "primary")), ("Secondary text", "text", ("text", "secondary")),
             ("Strong border", "graphic", ("border", "strong")), ("Data context", "graphic", ("data", "context")), ("Focus ring", "graphic", ("focus", "ring"))]
    panels = []
    for key, name in surfaces:
        bg = resolve(col["palette"][key]["$value"])
        fg = resolve(col["text"]["primary"]["on" + name]["$value"])
        rows = []
        for label, kind, (a, b) in roles:
            tok = col[a][b]["on" + name]
            hx = resolve(tok["$value"])
            ratio = contrast(hx, bg)
            stored = tok["$extensions"]["org.oathandaction"].get("contrast")
            minimum = 4.5 if kind == "text" else 3.0
            TOKEN_REPORT.append({"surface": name, "role": label, "token": f"oa.color.{a}.{b}.on{name}", "fg": hx, "bg": bg, "computed": round(ratio, 2), "stored": stored, "minimum": minimum})
            need(stored is None or abs(round(ratio, 2) - stored) <= 0.01, f"token contrast mismatch {a}.{b}.on{name}: {ratio:.2f} vs {stored}")
            if kind == "text":
                sw = f'<span class="tsw" style="color:{hx}" aria-hidden="true">Aa</span>'
            elif b == "strong":
                sw = f'<span class="tsw" aria-hidden="true"><span class="edge" style="border-color:{hx}"></span></span>'
            elif b == "ring":
                sw = f'<span class="tsw" aria-hidden="true"><span class="ring" style="border-color:{hx}"></span></span>'
            else:
                sw = f'<span class="tsw" aria-hidden="true"><span class="bar" style="background:{hx}"></span></span>'
            ok = "passes" if ratio >= minimum else "falls short of"
            rows.append(f'<div class="trow" data-fg="{hx}" data-bg="{bg}" data-ratio="{ratio:.2f}" data-min="{minimum}">{sw}<p class="tmeta" style="margin:0"><b>{label}</b>{NAMES.get(hx, hx)} {hx} · <span class="ratio">{ratio:.2f}:1</span>, {ok} {minimum:g}:1</p></div>')
        panels.append(f'<div class="tsurf" style="background:{bg};color:{fg}"><h5>{name} <span style="font-weight:400">{bg}</span></h5>{"".join(rows)}</div>')
    return f'<div class="tokens" role="group" aria-label="Token roles on the four surfaces">{"".join(panels)}</div>'


def systems_bases():
    sec = board_section(sysb, "m8")
    arts = re.findall(r'<article class="base">\s*<div class="opthead"><span class="tag">(.*?)</span><h3>(.*?)</h3></div>\s*<img src="([^"]+)" alt="([^"]+)"', sec, flags=re.S)
    need(len(arts) >= 5, "atlas bases")
    figs = "".join(f'<figure>{img(os.path.join(BOARDS, src), html.unescape(alt), cls="fit")}<figcaption class="cap"><b>{esc(strip_tags(h3))}</b> · {esc(strip_tags(tag))}</figcaption></figure>' for tag, h3, src, alt in arts)
    return f'<div class="thumbs">{figs}</div><p class="cap">Thumbnails from the systems board, section 8: Phase 0 captures of Concepts V2 at 1440 px, scaled down for review.</p>'


GROUPS = [("S", "Strategy"), ("Y", "Symbols"), ("M", "Systems marks"), ("T", "Structure and tokens")]


def set_html():
    out = []
    for prefix, name in GROUPS:
        rows = [r for r in set_rows if r[0].startswith(prefix)]
        body = "".join(f'<tr><td class="id">{esc(r[0])}</td><td>{inline(r[1])}</td><td>{inline(r[2])}</td></tr>' for r in rows)
        table = f'<div class="table" tabindex="0" role="region" aria-label="{attr(name)} recommendations"><table><thead><tr><th scope="col">ID</th><th scope="col">{esc(set_head[1])}</th><th scope="col">{esc(set_head[2])}</th></tr></thead><tbody>{body}</tbody></table></div>'
        extra = ""
        if prefix == "M":
            extra = ('<h4>Evidence line code and typed chips (M1, M3)</h4>'
                     f'<figure class="strip"><div class="spec" style="padding:0;border:0">{img(os.path.join(IMG, "systems-evidence-lines.png"), "Evidence line code on Newsprint, White, Charcoal and Prussian: documented and well supported as solid arrows with record chips, plausible dashed, contested dash-dot, hypothesis dotted.", scale=2, cls="fit")}</div>'
                     '<figcaption class="cap">The systems board\'s recommended option for mark 1, V7\'s code with the record square, on all four surfaces.</figcaption></figure>'
                     f'<figure class="strip"><div class="spec" style="padding:0;border:0">{img(os.path.join(IMG, "systems-typed-chips.png"), "Two-part typed ID chips on the four surfaces: VARIABLE B4, LOOP B4, LOOP R1 and REFORM R-01, each above its name, with contrast values beneath.", scale=2, cls="fit")}</div>'
                     '<figcaption class="cap">The recommended option for mark 3, the two-part chip with the full type word.</figcaption></figure>'
                     '<h4>The atlas bases (M5)</h4>' + systems_bases())
        if prefix == "T":
            nav = os.path.join(P1, "navigation", "20261021_Nav-390-Menu.png")
            chap = os.path.join(P1, "navigation", "20261021_Color-Chapter-1440.jpg")
            extra = ('<h4>Navigation and the chapter template (T3)</h4><div class="wire">'
                     f'<figure>{img(nav, "Phone contents menu at 390 px, open on 05 Color: Cover, Contents, Where to start, then Foundations with chapters 01 to 08, 05 Color marked as current, and Symbols and graphics below.", cls="fit")}<figcaption class="cap">The contents menu at 390 px, open on 05 Color.</figcaption></figure>'
                     f'<figure><div class="tall" tabindex="0" role="region" aria-label="Chapter template applied to 05 Color, scrollable">{img(chap, "Wireframe of chapter 05 Color at 1440 px: the title and instruction line, an in-chapter list of rules, then Rule 05.1 Newsprint leads and Rule 05.2 Text sits only on pairs that pass, each with tokens, a copy control, Why it works, and correct and failure placeholders, continuing down the full chapter.")}</div>'
                     '<figcaption class="cap">The chapter template applied to 05 Color at 1440 px, shown reduced. Scroll inside the frame to read the whole chapter.</figcaption></figure></div>'
                     '<h4>Token roles on the four surfaces (T4, T5)</h4>' + token_strip()
                     + '<p class="cap">Rendered from <code>work/build/tokens/20261021_Token-Schema-Draft.json</code>. Each ratio is worked out here from the two hex values with the WCAG formula, and it matches the value stored in the file. Text needs 4.5 to 1 and graphics need 3 to 1.</p>')
        out.append(f'<div class="group" id="set-{prefix.lower()}"><h3>{esc(name)} ({prefix}) <span class="count">{len(rows)} recommendations</span></h3>{table}{extra}</div>')
    return "\n".join(out)


# ---------------------------------------------------------------- rubric, risks, Phase 2, questions, files

RUBRIC_KEY = '<div class="key"><span><i style="background:var(--low-bg)"></i>1 or 2</span><span><i style="background:var(--mid-bg)"></i>3</span><span><i style="background:var(--ok-bg)"></i>4 or 5</span></div>'


def rubric_html():
    lines = s3.split("\n")
    if any(l.startswith("| Proposal | Cr |") for l in lines):
        head, rows = md_table(s3, "| Proposal | Cr |")
        th = "".join(f'<th scope="col">{esc(h)}</th>' for h in head)
        body = []
        for r in rows:
            cells = [f'<th scope="row">{inline(r[0])}</th>']
            for c in r[1:]:
                m = re.fullmatch(r"\s*([1-5])\s*(\*?)\s*", c)
                cells.append(f'<td class="s s{m.group(1)}">{esc(c.strip())}</td>' if m else f"<td>{inline(c)}</td>")
            body.append("<tr>" + "".join(cells) + "</tr>")
        prose = md_blocks(s3)
        return (prose + RUBRIC_KEY + f'<div class="table" tabindex="0" role="region" aria-label="Rubric scores"><table><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'), len(rows)
    need("RUBRIC_PENDING" in s3, "section 3 has neither a rubric table nor RUBRIC_PENDING")
    return ('<div class="pending"><p style="margin:0"><b>Pending.</b> The creative director\'s re-scores after the fix round are not in the report yet. '
            'This section fills in from the report\'s section 3 the next time the board is built.</p></div>'), 0


def phase2_html():
    blocks = [b.strip() for b in s9.strip().split("\n\n") if b.strip()]
    left, right = [], []
    k = 0
    while k < len(blocks):
        b = blocks[k]
        if b == "**Phase 2 produces**":
            left.append("<h3>Phase 2 produces</h3>" + md_blocks(blocks[k + 1]))
            k += 2
        elif b == "**What your answers set in motion**":
            right.append("<h3>What your answers set in motion</h3>" + md_blocks(blocks[k + 1]))
            k += 2
        elif b.startswith("**Order.**"):
            k += 1  # condensed: the order of work stays in the report
        else:
            right.append(md_blocks(b))
            k += 1
    need(left and right, "Phase 2 blocks")
    return f'<div class="two"><div>{"".join(left)}</div><div>{"".join(right)}</div></div><p class="cap">The order of work is in the report, section 9.</p>'


def questions_html():
    out = []
    for qid, q, why, dflt in q_rows:
        out.append(f'<li id="{attr(qid.lower())}"><span class="qid">{esc(qid)}</span><p class="q">{inline(q)}</p><p><span class="muted">Why it matters:</span> {inline(why)}</p><p class="dflt"><b>Default until you answer:</b> {inline(dflt)}</p></li>')
    return "".join(out)


FILE_NOTES = {
    "20261021_Strategy-And-Direction-Board.html": "Calls 6 and 7, the S recommendations and the S9 badge",
    "20261021_Identity-Refinement-Board.html": "Calls 1 to 4 and fixes I1 to I8",
    "20261021_Symbol-Family-Board.html": "Call 5, the Y recommendations and the composite post",
    "20261021_Systems-Marks-Board.html": "The M recommendations and the hinge's five separation rules",
    "20261021_Navigation-And-Template-Wireframes.html": "The T recommendations: architecture, navigation and the chapter template",
}


def files_html():
    out = [f'<li><code>work/boards/{esc(f)}</code>: {esc(FILE_NOTES.get(f, ""))}</li>' for f in board_files]
    out.append(f'<li><code>{esc(os.path.relpath(REPORT, ROOT))}</code>: the Gate 1 report, the source of every table and decision on this page</li>')
    return "".join(out)


# ---------------------------------------------------------------- assemble

page = read(os.path.join(GATE, "gate-1-board.template.html"))
rubric, rubric_rows = rubric_html()
fills = {
    "wordmark": svg_inline(os.path.join(SPRITE, "wordmark.svg"), "Oath & Action", width=210, cls="mark"),
    "status": "Waiting for your approval",
    "title": esc(title),
    "lede": inline(lede),
    "approve_items": "".join(f"<li>{link_sections(inline(x))}</li>" for x in approve_list),
    "reply_intro": esc(reply_intro),
    "reply": esc(reply),
    "approve_after": link_sections(inline(after[0])),
    "composite": composite(),
    "calls_table": calls_table(),
    "calls": calls_html(),
    "fixes_intro": inline(re.sub(r"^\*\*Six identity fixes\*\* in section 5\. ", "", approve_list[1])) + " " + " ".join(inline(p) for p in fix_after),
    "fixes": fixes_html(),
    "set_intro": "The studio asks you to approve these as one set. Name any you would change, and the rest stand.",
    "set_groups": set_html(),
    "rubric": rubric,
    "risks": md_blocks(s7).replace("<ul>", '<ul class="list">', 1),
    "phase2": phase2_html(),
    "questions": questions_html(),
    "files": files_html(),
}
for key, value in fills.items():
    need("{{" + key + "}}" in page, f"template has no {{{{{key}}}}}")
    page = page.replace("{{" + key + "}}", value)
left = re.findall(r"\{\{[a-z_]+\}\}", page)
need(not left, f"unfilled placeholders: {left}")
need(page.startswith("<title>"), "page must start with <title>")
need("#E63946" not in page.split("</style>", 1)[0], "Pillar Red found in the board's own stylesheet")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
size = os.path.getsize(OUT)
need(size < 10 * 1024 * 1024, f"board is {size} bytes, over 10 MB")
print(f"{OUT}: {size / 1024 / 1024:.2f} MB, {len(EMBEDDED)} images embedded ({len(USES)} uses), "
      f"{len(call_rows)} calls, {len(fix_rows)} fixes, {len(set_rows)} recommendations, {len(q_rows)} questions, "
      f"rubric rows {rubric_rows or 'pending'}, {len(TOKEN_REPORT)} token pairs")
