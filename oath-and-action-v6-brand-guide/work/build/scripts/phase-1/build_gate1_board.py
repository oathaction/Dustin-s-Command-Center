"""Build the combined Gate 1 review board from its template, the Gate 1 report and the five Phase 1 boards.

Usage:
    python3 -I build_gate1_board.py <project-root> [--report PATH] [--out PATH] [--no-capture] [--check]

Each run first recaptures every screenshot from the five boards (capture_gate1_images.js), so one
rerun picks up any change to the boards. --no-capture reuses the images already in
work/boards/phase-1/gate-1/img/. --check runs check_gate1_board.js on the result.

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
import shutil
import struct
import subprocess
import sys

# ---------------------------------------------------------------- paths and arguments

args = sys.argv[1:]
if not args:
    raise SystemExit(__doc__)
ROOT = os.path.abspath(args[0])
FLAGS = {a for a in args[1:] if a in ("--no-capture", "--check")}
rest = [a for a in args[1:] if a not in FLAGS]
opts = dict(zip(rest[0::2], rest[1::2]))
HERE = os.path.dirname(os.path.abspath(__file__))
WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("WARNING: " + msg, file=sys.stderr)


def run_node(script):
    node = shutil.which("node")
    if not node:
        raise SystemExit("build_gate1_board: node is not on the PATH")
    subprocess.run([node, os.path.join(HERE, script), ROOT], check=True)


if "--no-capture" not in FLAGS:
    run_node("capture_gate1_images.js")
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
    return f'<img src="{data_uri(path)}" width="{w}" height="{h}" alt="{attr(alt)}"{c}{s}>'


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
if len(call_rows) != 7:
    warn(f"section 4 lists {len(call_rows)} big calls, the board's specimens are drawn for seven")
call_prose = {t.split(".", 1)[0]: (t.split(". ", 1)[1], body) for t, body in split_headings(s4, 3)}
need(sorted(call_prose, key=int) == [r[0] for r in call_rows], "section 4's ### headings must match its table rows")
l_note = [p for p in s4.split("\n\n") if p.strip().startswith("**L** marks")]
need(l_note, "L note missing")

s5 = section(sections, "5. ")
fix_head, fix_rows = md_table(s5, "| ID | Fix |")
fix_after = [p.strip() for p in s5.split("\n\n") if p.strip() and not p.strip().startswith("|")]

s6 = section(sections, "6. ")
set_head, set_rows = md_table(s6, "| ID | Question |")

WORDS = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()


def count_word(n):
    if n < len(WORDS):
        return WORDS[n]
    tens = {2: "twenty", 3: "thirty", 4: "forty"}
    return tens[n // 10] + ("-" + WORDS[n % 10] if n % 10 else "") if n // 10 in tens else str(n)

s3 = section(sections, "3. ")
s7 = section(sections, "7. ")
s9 = section(sections, "9. ")
s10 = section(sections, "10. ")
q_head, q_rows = md_table(s10, "| # | Question |")
risks = [l[2:] for l in s7.split("\n") if l.startswith("- ")]
board_files = re.findall(r"^- `(2026\d{4}_[^`]+\.html)`", report, flags=re.M)
need(len(board_files) == 5, "five board files expected in the report header")


def sentences(text):
    flat = " ".join(l.strip() for l in text.split("\n") if l.strip() and not l.startswith(("|", ">", "#")))
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'])", flat) if s.strip()]


# What each call costs, as the report words it. Each entry lists where to look, in order: a risk bullet
# that starts with the given words, or a prose sentence matching the pattern. If none matches after the
# report is edited, the builder takes the call's first sentence that names a cost, and warns.
COSTS = {
    "1": [("risk", "Ampersand B is a first drawing"), ("prose", r"fallback|fails")],
    "2": [("prose", r"\bcosts?\b"), ("risk", "A condensed drawing pass")],
    "3": [("prose", r"compact master drops"), ("prose", r"\bcosts?\b")],
    "4": [("prose", r"\bThe cost\b|\bcosts?\b"), ("risk", "Under the red rule")],
    "5": [("prose", r"A's Act mark at 16 px"), ("prose", r"\btests?\b")],
    "6": [("risk", '"From spectators to stewards." with no role'), ("prose", r"\bcosts?\b")],
    "7": [("prose", r"puts the nonpartisan standing at stake"), ("risk", "Each position piece")],
}


def cost(n):
    prose = sentences(call_prose[n][1])
    for kind, key in COSTS.get(n, []) + [("prose", r"\bcosts?\b|\bat stake\b|\bloses?\b")]:
        if kind == "risk":
            hits = [r for r in risks if r.startswith(key)]
        else:
            hits = [s for s in prose if re.search(key, s)]
        if hits:
            return hits[0]
    warn(f"call {n}: no cost sentence found in the report; the board says so")
    return "The report names no cost for this call."

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

MANIFEST = json.load(open(os.path.join(IMG, "manifest.json"), encoding="utf-8"))


def captured(prefix):
    """Captured files whose names start with prefix, in capture order, with their recorded info."""
    names = sorted((k for k in MANIFEST if k.startswith(prefix)), key=lambda k: int(re.search(r"(\d+)\.\w+$", k).group(1)))
    need(names, f"no captured images named {prefix}*; run capture_gate1_images.js")
    return [(os.path.join(IMG, k), MANIFEST[k].get("info", {})) for k in names]


def composite():
    sec = board_section(symb, "composite")
    note = re.search(r'<p class="cap"><span class="tag">Illustrative</span>(.*?)</p>', sec, flags=re.S)
    posts = captured("post-")
    if len(posts) != 4:
        warn(f"the symbol board shows {len(posts)} composite posts; the section intro describes four")
    figs = []
    for path, info in posts:
        label = info.get("label") or "Portrait Act post"
        bits = [f"{label}, 1080 by 1350 on Newsprint."]
        if info.get("covered"):
            bits.append("The wordmark is covered by a gray bar.")
        if info.get("kicker"):
            bits.append(f"Kicker: {info['kicker']}.")
        if info.get("head"):
            bits.append(f"Headline: {info['head'].rstrip('.')}.")
        shows = list(info.get("named", []))
        if info.get("steps"):
            shows.append(f"{count_word(info['steps'])} numbered steps")
        if shows:
            bits.append("It shows " + (", ".join(shows[:-1]) + " and " + shows[-1] if len(shows) > 1 else shows[0]) + ".")
        alt = " ".join(bits)
        figs.append(f'<figure>{img(path, alt, scale=2, cls="fit")}<figcaption class="cap">{esc(tidy(info.get("caption", "").strip()))}</figcaption></figure>')
    note_html = f'<p class="cap"><span class="illus">Illustrative</span> {esc(tidy(strip_tags(note.group(1))))}</p>' if note else ""
    return f'<div class="posts n{len(posts)}">{"".join(figs)}</div>{note_html}'


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
    items = "".join(f'<div class="item"><p class="lab">{esc(n)}</p>{svg_inline(p, a, height=108, cls="fit", style="color:#121212")}</div>' for p, n, a in wm)
    h.append('<h4>In the display wordmark</h4>')
    h.append(spec_figure(f'<div class="stack">{items}</div>', "Options A and B sit in the display master of fix I3, which carries the hinge gaps of fix I2. The wordmarks are shown 108 px tall, scaled down on narrow screens."))
    return "".join(h)


def call2():
    cur = os.path.join(IDSVG, "03-wordmark-masters", "20261021_Wordmark-Display-Amp-B.svg")
    con = os.path.join(IDSVG, "06-condensed", "20261021_Wordmark-Condensed-7-5-To-1-Display.svg")
    (cw, ch), (kw, kh) = svg_root_size(read(cur)), svg_root_size(read(con))
    ratio = (kh / kw) / (ch / cw)
    items = (f'<div class="item"><p class="lab">Today\'s width, with ampersand B</p>{svg_inline(cur, "The wordmark at today's width with ampersand B", width=640, cls="fit", style="color:#121212")}</div>'
             f'<div class="item"><p class="lab">Condensed 7.5 to 1, at the same width</p>{svg_inline(con, "The condensed wordmark at 7.5 to 1, at the same width", width=640, cls="fit", style="color:#121212")}</div>')
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


KNOWN_HINGE_ALTS = {
    "threeup__v5.png": "V5's hinge diagram: the wordmark under one dotted arc ending in an open arrowhead, with UNDERSTAND and IMPACT beneath.",
    "threeup__draft.png": "The withdrawn first draft: the ampersand in a circle on a line joining OATH and ACTION, with dotted arcs above and below.",
    "threeup__v2.png": "V2: the ampersand in a circle on a line joining OATH and ACTION with four nodes, two solid hairline arcs running clockwise, and UNDERSTAND and IMPACT beneath.",
}


def call3():
    sec = board_section(idb, "item-7")
    block = re.search(r'<div class="three">(.*?)</div>', sec, flags=re.S)
    need(block, "identity board item 7 has no three-up comparison")
    found = re.findall(r'<figure><figcaption>(.*?)</figcaption><img src="([^"]+)"[^>]*alt="([^"]*)"', block.group(1), flags=re.S)
    need(found, "identity board item 7 three-up has no figures")
    figs = "".join(f'<figure><div class="spec">{img(os.path.join(BOARDS, src), KNOWN_HINGE_ALTS.get(os.path.basename(src), html.unescape(alt)), cls="fit")}</div><figcaption class="cap"><b>{esc(strip_tags(fc))}</b></figcaption></figure>' for fc, src, alt in found)
    grid = "three" if len(found) == 3 else "two"
    cm = re.search(r"Each rendered 640 px wide[^<]*?\.", sec)
    cap = cm.group(0) if cm else "Each rendered 640 px wide and shown reduced."
    master = os.path.join(IDSVG, "07-hinge", "20261021_Hinge-Display-Master_V2.svg")
    svg = svg_inline(master, "Hinge diagram V2 display master: OATH and ACTION on a line with four nodes, the red ampersand in a circle at the center, two solid hairline arcs running clockwise, and UNDERSTAND and IMPACT beneath", width=1100, style="color:#121212;width:100%;min-width:560px;height:auto")
    head = re.search(r'<h3>([^<]*)</h3><div class="three">', sec)
    h = [f'<h4>{esc(head.group(1)) if head else "The drawings side by side"}</h4>', f'<div class="{grid} eq">{figs}</div><p class="cap">{esc(cap)}</p>']
    h.append('<h4>The V2 display master</h4>')
    h.append(spec_figure(scroll(svg, "Hinge diagram V2 display master"), "The display master file, <code>work/boards/phase-1/identity/07-hinge/20261021_Hinge-Display-Master_V2.svg</code>, inlined as drawn. Below 560 px the frame scrolls, so the labels never draw under the master's 526 px minimum."))
    return "".join(h)


def call4():
    sec = board_section(idb, "item-10")
    has_table = 'aria-label="Treatment table"' in sec
    th, tr = board_table(sec, "Treatment table") if has_table else ([], [])
    tcap = re.search(r'<p class="cap">(Median contrast of the ampersand.s pixels against Prussian.*?)</p>', sec, flags=re.S)
    # The option set is the identity board's own p10 pairs, in board order.
    pids = re.findall(r'<div class="pair" id="(p10-[^"]+)">', sec)
    need(pids, "identity board item 10 has no p10 pairs")
    rec_row = [r for r in call_rows if r[0] == "4"]
    rec_letter = (re.findall(r"\b([A-D])\b", rec_row[0][4]) or [None])[-1] if rec_row else None
    rows, v5caps, v5note = [], {}, ""
    v5 = re.search(r'<div class="pair v5today"[^>]*><h3>(.*?)</h3>(.*?)(?=<div class="pair")', sec, flags=re.S)
    if v5:
        # V5 today, the one red on Prussian the identity board keeps, with its own measured captions.
        v5name = strip_tags(v5.group(1)).split(":")[0].strip()
        srcs = dict((sz, src) for src, sz in re.findall(r'<img src="(phase-1/identity/png/[^"]+__(16|96)\.png)"', v5.group(2)))
        for fc, sz in re.findall(r"<figcaption>([^<]*?, (16|96) px:[^<]*)</figcaption>", v5.group(2)):
            v5caps[sz] = strip_tags(fc)
        note = re.search(r'<p class="cap">(.*?)</p>', v5.group(2), flags=re.S)
        v5note = strip_tags(note.group(1)) if note else ""
        need("16" in srcs and "96" in srcs, "V5 today needs 16 and 96 px renders")
        rows.append(("v5", srcs, v5name, "v5"))
    else:
        for pid in pids:
            if os.path.exists(idpng(pid, "orig__prussian__color__16.png")):
                rows.append((pid, "orig", "V5", "v5"))
                break
    for pid in pids:
        title = pair_title(pid)
        name = re.sub(r"\s*\(recommended\)", "", title.split(":")[0]).strip()
        letter = re.sub(r"^Option ", "", name)[:1]
        tag = "rec" if ("(recommended)" in title or letter == rec_letter) else ""
        if os.path.exists(idpng(pid, "prop__prussian__color__16.png")):
            rows.append((pid, "prop", name, tag))
    tags = {"rec": '<span class="tag rec">Studio recommendation</span>', "v5": '<span class="tag" style="color:#DCD9D2">In force</span>', "": ""}
    r16, r96 = [], []
    for folder, who, name, tg in rows:
        if folder == "v5":
            p16, p96 = os.path.join(BOARDS, who["16"]), os.path.join(BOARDS, who["96"])
            what = f"{name}: V5's wordmark with its red ampersand on Prussian"
        else:
            p16 = idpng(folder, f"{who}__prussian__color__16.png")
            p96 = idpng(folder, f"{who}__prussian__color__96.png")
            what = f"Wordmark on Prussian, {name}"
        m16 = f'<span>{esc(re.sub(r"^[^:]*:\s*", "", v5caps["16"]))}</span>' if folder == "v5" and "16" in v5caps else ""
        l96 = f" · {esc(v5caps['96'])}" if folder == "v5" and "96" in v5caps else ""
        r16.append(f'<div class="lrow"><p class="lname">{esc(name)}<span>{tags[tg]}</span>{m16}</p>{cell(p16, "16 px", what + ", at 16 px, actual size")}{cell(p16, "16 px at 4x", what + ", at 16 px, magnified 4 times without smoothing", factor=4)}</div>')
        r96.append(f'<div class="item"><p class="lab"><b style="color:#DCD9D2">{esc(name)}</b> {tags[tg]}{l96}</p>{img(p96, what + ", at 96 px tall, actual size")}</div>')
    names = ", then ".join(r[2] for r in rows)
    first = f" {esc(v5note)}" if v5note else ""
    h = ['<h4>V5 today and the live options on Prussian, at 16 px</h4>']
    h.append(spec_figure(scroll(f'<div class="ladder">{"".join(r16)}</div>', "V5 today and the options on Prussian at 16 px"), f"{esc(names)}. Renders at 1x from the identity board's item 10.{first}", cls="prussian"))
    h.append('<h4>The same, at 96 px</h4>')
    h.append(spec_figure(scroll(f'<div class="stack">{"".join(r96)}</div>', "V5 today and the options on Prussian at 96 px"), "Each at 96 px tall.", cls="prussian"))
    ruled = re.search(r'<div class="ruled">(.*?)</div></div>', sec, flags=re.S)
    if ruled:
        rcap = re.search(r'<p class="cap">(.*?)</p>', ruled.group(1), flags=re.S)
        figs = []
        for fc, src, w, hh, alt in re.findall(r'<figure><figcaption>(.*?)</figcaption><img src="([^"]+)" width="(\d+)" height="(\d+)" alt="([^"]*)"', ruled.group(1), flags=re.S):
            path = os.path.join(BOARDS, src)
            pw, _ = image_size(path)
            figs.append(f'<figure class="cell">{img(path, html.unescape(alt), scale=pw / int(w))}<figcaption class="lab">{esc(strip_tags(fc))}</figcaption></figure>')
        h.append('<h4>Ruled out by Rule 05.3</h4>')
        h.append(spec_figure(scroll(f'<div class="lrow" style="flex-wrap:wrap;gap:24px">{"".join(figs)}</div>', "Ruled-out treatments in grayscale"),
                             esc(strip_tags(rcap.group(1))) if rcap else "Shown in grayscale, as the identity board shows them.", cls="white"))
    if has_table:
        h.append(html_table(th, tr, "Contrast on Prussian by treatment and size"))
    if tcap:
        h.append(f'<p class="cap">{esc(strip_tags(tcap.group(1)))}</p>')
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


def mock_alt(info):
    parts = [f"Mock layout, {info.get('label', 'Act piece').replace('Mock layout: ', '')}"]
    if info.get("kicker"):
        parts.append(f"kicker {info['kicker']}")
    if info.get("head"):
        parts.append(f"headline {info['head']}")
    if info.get("sections"):
        parts.append("sections " + ", ".join(s for s in info["sections"] if s))
    if info.get("ask"):
        parts.append(f"an ask button reading {info['ask']}")
    n = info.get("illustrative", 0)
    tail = f" {count_word(n).capitalize()} lines carry an Illustrative label." if n else ""
    return "; ".join(parts) + "." + tail


def call7():
    mocks = captured("act-mock-")
    figs = []
    for path, info in mocks:
        label = info.get("label", "").replace("Mock layout: ", "")
        kind = label[:1].upper() + label[1:] if label else "Act piece"
        desc = next((s for s in sentences(call_prose["7"][1]) if label and s.lower().startswith("a " + label.lower())), "")
        desc = desc.split(":")[0].rstrip(".") + "." if desc else ""
        figs.append(f'<figure>{img(path, mock_alt(info), scale=2, cls="fit")}<figcaption class="cap"><b>{esc(kind)}.</b> {esc(desc)}</figcaption></figure>')
    return ('<h4>The two kinds of Act piece</h4><div class="two">' + "".join(figs) +
            '</div><p class="cap"><span class="illus">Illustrative</span> Mock layouts from the strategy board, section 5. Every name, date, measure and figure in them is example copy, labeled Illustrative beside the item.</p>')


CALL_SPECIMENS = {"1": call1, "2": call2, "3": call3, "4": call4, "5": call5, "6": call6, "7": call7}


def evidence_line(n):
    parts = []
    for f, what, anchors in EVIDENCE.get(n, [("work/ledger/20261021_Gate-1-Report.md", "section 4", None)]):
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
  <p class="eyebrow">Big call {n} of {len(call_rows)} · {esc(ids)}</p>
  <h3 id="call-{n}-h">{esc(ptitle)}</h3>
  <div class="call-body">
    <div class="prose">{md_blocks(body)}</div>
    <aside class="options" aria-labelledby="call-{n}-opt"><h4 id="call-{n}-opt">Options</h4><p>{inline(options)}</p></aside>
  </div>
  {CALL_SPECIMENS[n]() if n in CALL_SPECIMENS else ""}
  <dl class="verdict">
    <div><dt>Studio recommendation</dt><dd>{inline(rec)}</dd></div>
    <div><dt>What it costs</dt><dd>{inline(cost(n))}</dd></div>
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

def ba(before, after, grid=False, labels=("Before, V5", "After, the proposal")):
    b = f'<div class="side"><p class="ba-label">{esc(labels[0])}</p>{before}</div>'
    a = f'<div class="side"><p class="ba-label">{esc(labels[1])}</p>{after}</div>'
    return f'<div class="ba{" ba-grid" if grid else ""}">{b}{a}</div>'


def fix_I1():
    def side(who, tl_alt, amp_alt):
        tl = idpng("p01-tl-1", f"{who}__newsprint__mono__display.png")
        amp = idpng("p01-amp", f"{who}__newsprint__color__display.png")
        return f'<div class="spec"><div class="stack"><div class="item"><p class="lab">Tagline, one line, 40 px tall</p>{img(tl, tl_alt, cls="fit")}</div><div class="item"><p class="lab">Master ampersand, 240 px tall</p>{img(amp, amp_alt, cls="fit")}</div></div></div>'
    return ba(side("orig", "V5's tagline A country that answers to its people., with the bottoms of y and p cut off so it reads A countrv that answers to its peoole.", "V5's master ampersand, with the top of its loop and the tip of its tail cut off by its box"),
              side("prop", "The re-exported tagline with every descender whole", "The re-exported master ampersand with its full loop and tail"), grid=True)


def fix_I2():
    lm = re.search(r"Overlay legend for every panel: ([^.]*\.)", idb)
    legend = strip_tags(lm.group(1)) if lm else "Charcoal where both versions have ink, light gray where only the original has ink, Verdigris where only the proposal has ink."
    o = lambda w, a: f'<div class="spec">{img(idpng("p02-optical", w), a, cls="fit")}</div>'
    return (ba(o("orig__newsprint__color__display.png", "V5's wordmark at display size, with the ampersand closer to ACTION than to OATH"),
               o("prop__newsprint__color__display.png", "The wordmark with option 2b spacing: the ampersand moved 1.42 units toward ACTION so both sides hold equal white"))
            + f'<figure class="side" style="margin-top:12px"><p class="ba-label">Overlay of the two</p><div class="spec white">{img(idpng("p02-optical", "overlay__display.png"), "Overlay of V5 and the proposal at display size: the ampersand and ACTION show thin edges where they moved", cls="fit")}</div><figcaption class="cap">{esc(legend)}</figcaption></figure>')


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
    return ba(side("orig", "V5"), side("prop", "Proposed")) + '<p class="cap">Each mark at its minimum, at 1x, from the identity board\'s item 9.</p>'


BADGE = os.path.join(P1, "symbols", "badge")
SURFACE_HEX = {"newsprint": "#DCD9D2", "white": "#FFFFFF", "charcoal": "#121212", "prussian": "#1F2D5A"}


def fix_S9():
    sec = board_section(symb, "badge")
    meas = json.load(open(os.path.join(BADGE, "20261021_Hinge-Badge-Measurements.json"), encoding="utf-8"))
    m16, m24, mdisp = (os.path.join(BADGE, meas["masters"][k]) for k in ("16", "24", "display"))
    blocks = re.findall(r'<div class="s-(\w+) mx"><p class="sname">([^<]*)</p>(.*?)<p class="cap">([^<]*)</p></div>', sec, flags=re.S)
    need(blocks, "symbol board section 12 has no badge surfaces")
    panels = []
    for key, name, inner, cap in blocks:
        color = re.search(r'style="color:(#[0-9A-Fa-f]{6})"', inner).group(1)
        ink = "#121212" if key in ("newsprint", "white") else "#DCD9D2"
        sizes = [(m16, 16), (m24, 24), (mdisp, 48), (mdisp, 96)]
        cells = "".join(f'<figure class="bcell">{svg_inline(m, f"Badge at {s} px on {name}", width=s, style=f"color:{color}")}<figcaption class="tmeta">{s}</figcaption></figure>' for m, s in sizes)
        disp = svg_inline(mdisp, f"Badge at display size, 160 px, on {name}", width=160, cls="fit", style=f"color:{color}")
        panels.append(f'<div class="tsurf" style="background:{SURFACE_HEX.get(key, "#DCD9D2")};color:{ink}"><p class="tname">{esc(name)}</p><div class="bsizes">{cells}</div>{disp}<p class="tmeta" style="margin:0">{esc(cap)}</p></div>')
    mags = []
    for f, s, k in (("nbadge-16.png", 16, 6), ("nbadge-24.png", 24, 4)):
        p = os.path.join(SYMPX, f)
        if os.path.exists(p):
            mags.append(cell(p, f"{s} px master at {k}x", f"The badge's {s} px master, magnified {k} times without smoothing", factor=k))
    rule = re.search(r'"(Seals imply[^"]*)"', [r for r in fix_rows if r[0] == "S9"][0][3]) if any(r[0] == "S9" for r in fix_rows) else None
    rule_text = rule.group(1) if rule else "Seals imply an authority we do not claim."
    seal = [c for c in MANIFEST if c.startswith("ref-seal-")]
    seal_html = ""
    if seal:
        info = MANIFEST[seal[0]].get("info", {})
        seal_html = (f'<figure style="margin-top:12px;display:grid;gap:6px;justify-items:start">{img(os.path.join(IMG, seal[0]), info.get("label") or "Generated reference seal", scale=2)}'
                     '<figcaption class="lab"><span class="illus">Generated reference, study only</span> A seal with a ring of words, the form V5\'s rule bars</figcaption></figure>')
    before = (f'<div class="spec"><p style="margin:0;font:italic 400 1.125rem/1.5 var(--quote);color:#121212">V5: "{esc(rule_text)}"</p>'
              '<p class="lab">V5 draws no badge. Its rule bars seals outright.</p>' + seal_html + '</div>')
    after = (f'<div class="tokens" role="group" aria-label="The proposed badge on four surfaces">{"".join(panels)}</div>'
             + (f'<div class="spec" style="margin-top:12px">{scroll(f"<div class=\"lrow\" style=\"flex-wrap:wrap\">{"".join(mags)}</div>", "The badge masters magnified")}</div>' if mags else "")
             + '<p class="cap">The symbol board\'s three masters, from <code>work/boards/phase-1/symbols/badge/</code>: the 16 px master at 16, the 24 px master at 24, and the display master at 48, 96 and 160 px. Each surface takes one color, as the symbol board sets it.</p>')
    return ba(before, after, labels=("Before: V5's rule, and the kind of seal it bars", "After: the proposed badge"))


FIX_SPECIMENS = {"I1": fix_I1, "I2": fix_I2, "I3": fix_I3, "I7": fix_I7, "I8": fix_I8, "S9": fix_S9}
FIX_SOURCE = {
    "I1": [(IDENTITY_BOARD, "item 1", "#item-1")], "I2": [(IDENTITY_BOARD, "item 2", "#item-2")], "I3": [(IDENTITY_BOARD, "item 3", "#item-3")],
    "I7": [(IDENTITY_BOARD, "item 8", "#item-8")], "I8": [(IDENTITY_BOARD, "item 9", "#item-9")],
    "S9": [(SYMBOL_BOARD, "section 12, the hinge-circle badge", "#badge"), (STRATEGY_BOARD, "section 7, Art direction", "#art")],
}


def evidence_parts(entries):
    parts = []
    for f, what, anchors in entries:
        a = f" (<code>{esc(anchors)}</code>)" if anchors else ""
        parts.append(f"<code>{esc(f)}</code>, {esc(what)}{a}")
    return '<p class="evidence"><b>Full evidence:</b> ' + "; ".join(parts) + ".</p>"


def fixes_html():
    out = []
    for fid, fix, what, why in fix_rows:
        defect = "(defect fix)" in why
        if fid not in FIX_SPECIMENS:
            warn(f"fix {fid} is new in section 5 and has no drawings on this board")
        tag = ' <span class="tag solid">Defect fix</span>' if defect else ""
        out.append(f'''<article class="fix" id="fix-{fid}" aria-labelledby="fix-{fid}-h">
  <div class="fix-head"><span class="fix-id">{esc(fid)}</span><h3 id="fix-{fid}-h">{inline(fix)}</h3>{tag}</div>
  <dl class="fix-dl"><div><dt>What changes</dt><dd>{inline(what)}</dd></div><div><dt>Why</dt><dd>{inline(why)}</dd></div></dl>
  {FIX_SPECIMENS[fid]() if fid in FIX_SPECIMENS else ""}
  {evidence_parts(FIX_SOURCE.get(fid, [("work/ledger/20261021_Gate-1-Report.md", "section 5", None)]))}
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
    figs = "".join(f'<figure><div class="tb">{img(os.path.join(BOARDS, src), html.unescape(alt))}</div><figcaption class="cap"><b>{esc(strip_tags(h3))}</b> · {esc(strip_tags(tag))}</figcaption></figure>' for tag, h3, src, alt in arts)
    return f'<div class="thumbs">{figs}</div><p class="cap">Thumbnails from the systems board, section 8: Phase 0 captures of Concepts V2 at 1440 px, scaled down for review.</p>'


GROUPS = [("S", "Strategy"), ("Y", "Symbols"), ("M", "Systems marks"), ("T", "Structure and tokens")]


def set_html():
    out = []
    known = tuple(p for p, _ in GROUPS)
    stray = [r[0] for r in set_rows if not r[0].startswith(known)]
    groups = GROUPS + ([("", "Other")] if stray else [])
    if stray:
        warn(f"section 6 IDs outside S, Y, M and T: {stray}")
    for prefix, name in groups:
        rows = [r for r in set_rows if (r[0].startswith(prefix) if prefix else not r[0].startswith(known))]
        if not rows:
            continue
        body = "".join(f'<tr><td class="id">{esc(r[0])}</td><td>{inline(r[1])}</td><td>{inline(r[2])}</td></tr>' for r in rows)
        table = f'<div class="table" tabindex="0" role="region" aria-label="{attr(name)} recommendations"><table class="settable"><colgroup><col style="width:4.5em"><col style="width:44%"><col></colgroup><thead><tr><th scope="col">ID</th><th scope="col">{esc(set_head[1])}</th><th scope="col">{esc(set_head[2])}</th></tr></thead><tbody>{body}</tbody></table></div>'
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
        pid = prefix.lower() or "other"
        ptxt = f" ({prefix})" if prefix else ""
        out.append(f'<div class="group" id="set-{pid}"><h3>{esc(name)}{ptxt} <span class="count">{len(rows)} recommendation{"s" if len(rows) != 1 else ""}</span></h3>{table}{extra}</div>')
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
    "20261021_Strategy-And-Direction-Board.html": "Calls 6 and 7 and the S recommendations",
    "20261021_Identity-Refinement-Board.html": "Calls 1 to 4 and fixes I1 to I8",
    "20261021_Symbol-Family-Board.html": "Call 5, the Y recommendations, the composite post and the S9 badge",
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
    "fixes_intro": inline(re.sub(r"^\*\*[^*]+\*\* in section 5\. ", "", approve_list[1])) + " " + " ".join(inline(p) for p in fix_after),
    "calls_heading": f"The {count_word(len(call_rows))} big calls",
    "fixes_heading": f"{count_word(len(fix_rows)).capitalize()} identity fixes to approve by name",
    "set_heading": f"{count_word(len(set_rows)).capitalize()} studio recommendations, approved as a set",
    "toc_calls": f"The {count_word(len(call_rows))} big calls",
    "toc_fixes": f"{count_word(len(fix_rows)).capitalize()} identity fixes",
    "toc_set": f"{count_word(len(set_rows)).capitalize()} recommendations",
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
      f"rubric rows {rubric_rows or 'pending'}, {len(TOKEN_REPORT)} token pairs, {len(WARNINGS)} warnings")
for w in WARNINGS:
    print("  warning: " + w)
if "--check" in FLAGS:
    run_node("check_gate1_board.js")
