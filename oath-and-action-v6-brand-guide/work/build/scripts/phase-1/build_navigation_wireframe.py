"""Build the guide shell wireframe for the Gate 1 navigation board from one chapter list.

Usage: python3 -I build_navigation_wireframe.py <project-root>

Writes work/boards/phase-1/navigation/20261021_Guide-Shell-Wireframe.html.
Fills the contents table in work/boards/20261021_Navigation-And-Template-Wireframes.html
between <!-- contents:start --> and <!-- contents:end --> when the board exists.
The chapter list matches work/ledger/20261021_Guide-Architecture-Map.md, section 2.
"""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
OUT = root / "work/boards/phase-1/navigation/20261021_Guide-Shell-Wireframe.html"
BOARD = root / "work/boards/20261021_Navigation-And-Template-Wireframes.html"
FRAG = root / "work/build/scripts/phase-1/fragments/05-color.html"
WORDMARK = root / "work/extract/v5-polished/sprite/wordmark.svg"

PARTS = [
    ("foundations", "Foundations", "The identity, its color and type, the page grid and the Signal Grid."),
    ("symbols", "Symbols and graphics", "Pillar marks, symbols and icons, and the graphic devices that guide a reader."),
    ("evidence", "Evidence and media", "How a claim carries its source, then charts, systems graphics and imagery."),
    ("behavior", "Behavior", "How the guide and its products respond to readers who use a keyboard, a screen reader, zoom or touch."),
    ("applications", "Applications", "The system at exact sizes, from the website and the atlas to print."),
    ("production", "Production", "Tokens, files and the checklist that ships them."),
]

CHAPTERS = [
    ("01", "purpose", "Purpose", "foundations", "Learn what Oath & Action does and how the four pillars lead a reader from a question to a next step."),
    ("02", "voice", "Voice", "foundations", "Write copy that sounds like Oath & Action, with the locked lines quoted exactly."),
    ("03", "identity", "Identity", "foundations", "Pick the right lockup for the surface and give the wordmark its clear space."),
    ("04", "ampersand", "The Ampersand and the hinge", "foundations", "Use the ampersand to join a promise to an action, once per composition."),
    ("05", "color", "Color", "foundations", "Choose a surface first, then the text and graphic colors that pass on it."),
    ("06", "type", "Type", "foundations", "Set every word at a readable size with the three faces and the type scale."),
    ("07", "layout", "Layout and spacing", "foundations", "Build pages on the column grid and spacing scale so the measure stays comfortable at every width."),
    ("08", "signal-grid", "The Signal Grid", "foundations", "Place the lockmark in its sanctioned spots, and code content with it only where a key beside it lets a reader decode it."),
    ("09", "pillar-marks", "Pillar marks", "symbols", "Mark which pillar a piece serves, always in the order Explain, Track, Connect, Act."),
    ("10", "symbols", "Topic and atlas symbols", "symbols", "Find the symbol for a subject or an atlas element and set it with its label."),
    ("11", "icons", "Status and utility icons", "symbols", "Show a record's state or an interface action with a glyph that never stands in for a topic."),
    ("12", "graphic-devices", "Graphic devices and patterns", "symbols", "Add dividers, frames, markers and watermarks only where they help someone read."),
    ("13", "evidence", "Evidence and sourcing", "evidence", "Say what kind of evidence a claim rests on, and put its source and any illustrative label beside it."),
    ("14", "data-visualization", "Data visualization", "evidence", "Start from the reader's question to choose a chart, then title it with the evidence it shows."),
    ("15", "systems-graphics", "Systems graphics", "evidence", "Draw causes, loops and authority from Atlas V7 so a reader can follow one link at a time."),
    ("16", "photography", "Photography, illustration and video", "evidence", "Show public life as it happens, and label every placeholder and generated image for what it is."),
    ("17", "motion-and-states", "Motion and states", "behavior", "Keep motion under the reader's control, and give every state a word or a shape as well as a color."),
    ("18", "components", "Components and interaction", "behavior", "Build controls that work by keyboard and screen reader, with a status line for every change."),
    ("19", "accessibility", "Accessibility", "behavior", "Check a page against WCAG 2.2 AA before you call it finished."),
    ("20", "web", "Web", "applications", "Assemble the website mastheads, navigation, article pages, trackers and footer from the system."),
    ("21", "atlas", "The atlas", "applications", "Apply the system to the atlas, its hardest test, with typed IDs and the evidence one step away."),
    ("22", "newsletter-and-email", "Newsletter and email", "applications", "Build an email that reads well with images off and web fonts unavailable."),
    ("23", "social-and-video", "Social and video", "applications", "Size posts, covers and video frames to each platform's safe areas, with captions clear of the interface."),
    ("24", "reports", "Reports", "applications", "Lay out a report page by page, from the cover to the source notes."),
    ("25", "print", "Print and presentation", "applications", "Produce one-pagers, letterhead, slides, event signs and merchandise at their print sizes."),
    ("26", "tokens", "Tokens and how to choose them", "production", "Pick a token by surface, then role, then state."),
    ("27", "assets", "Assets and downloads", "production", "Download a master with a dated name and see which chapter governs it."),
    ("28", "standards", "Standards checklist", "production", "Run the checklist before anything is called final."),
]

# V5 anchors kept as aliases on their new homes (map section 4).
ALIASES = {"signal-grid": "grid", "symbols": "topic-icons", "data-visualization": "data",
           "motion-and-states": "motion", "systems-graphics": "atlas-system"}
PART_ALIAS = {"applications": "in-use"}

PALETTE = [("Newsprint", "#DCD9D2"), ("Charcoal", "#121212"), ("Pillar Red", "#E63946"), ("Prussian", "#1F2D5A"),
           ("Stone", "#5D636D"), ("Verdigris", "#4A7C74"), ("White", "#FFFFFF")]
SURFACES = [("Newsprint", "#DCD9D2"), ("White", "#FFFFFF"), ("Charcoal", "#121212"), ("Prussian", "#1F2D5A")]

e = html.escape


def lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def verdict(r):
    if r >= 4.5:
        return "Text"
    if r >= 3:
        return "Large and graphics"
    return "Fails"


def color_table():
    rows = []
    for name, hx in PALETTE:
        cells = []
        for sname, shx in SURFACES:
            if sname == name:
                cells.append(f'<td role="cell" data-label="On {sname}"><span class="cell"><span class="r">n/a</span><span class="v">Same color</span></span></td>')
                continue
            r = ratio(hx, shx)
            # Rounded to two decimals, as in Master Brief V2 section 8. The verdict uses the unrounded ratio.
            shown = f"{r:.2f}"
            cells.append(f'<td role="cell" data-label="On {sname}"><span class="cell"><span class="r">{shown} to 1</span><span class="v">{verdict(r)}</span></span></td>')
        rows.append(
            f'<tr role="row"><th role="rowheader" scope="row"><span class="sw" style="background:{hx}" aria-hidden="true"></span>{e(name)}'
            f'<span class="hex"><code>{hx}</code> <button type="button" class="copy" data-copy="{hx}" aria-label="Copy {hx}, {e(name)}">Copy</button></span></th>'
            + "".join(cells) + "</tr>")
    head = "".join(f'<th role="columnheader" scope="col">On {s}</th>' for s, _ in SURFACES)
    return ('<table class="ctable" role="table">'
            '<caption>Contrast of each locked color on each approved surface</caption>'
            f'<thead role="rowgroup"><tr role="row"><th role="columnheader" scope="col">Color</th>{head}</tr></thead>'
            f'<tbody role="rowgroup">{"".join(rows)}</tbody></table>'
            '<p class="status" role="status" id="status-table">Nothing copied yet.</p>')


def chapnav(i):
    prev_ = CHAPTERS[i - 1] if i > 0 else None
    next_ = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None
    out = ['<div class="chapnav">']
    if prev_:
        out.append(f'<a href="#{prev_[1]}" rel="prev">Previous chapter: <span class="n">{prev_[0]}</span> {e(prev_[2])}</a>')
    if next_:
        out.append(f'<a href="#{next_[1]}" rel="next">Next chapter: <span class="n">{next_[0]}</span> {e(next_[2])}</a>')
    else:
        out.append('<a href="#closing">Next: Closing</a>')
    out.append('<a class="to-contents" href="#contents">Back to contents</a></div>')
    return "".join(out)


def wordmark_svg():
    s = WORDMARK.read_text()
    s = re.sub(r"<title>.*?</title>", "", s)
    s = s.replace('<svg ', '<svg role="img" aria-label="Oath and Action" focusable="false" ', 1)
    s = re.sub(r'\sstyle="[^"]*"', "", s, count=1)
    return s


def part_name(slug):
    return next(p[1] for p in PARTS if p[0] == slug)


def nav_list(cls_prefix):
    out = [f'<ul>']
    out.append(f'<li><a href="#start" data-loc="start">Where to start</a></li>')
    for slug, name, _ in PARTS:
        out.append(f'<li><a class="{cls_prefix}-partlink" href="#part-{slug}" data-loc="part-{slug}">{e(name)}</a><ul>')
        for num, cid, cname, cpart, _ in CHAPTERS:
            if cpart == slug:
                out.append(f'<li><a href="#{cid}" data-loc="{cid}"><span class="n">{num}</span> <span>{e(cname)}</span></a></li>')
        out.append('</ul></li>')
    out.append('<li><a class="%s-partlink" href="#closing" data-loc="closing">Closing</a></li></ul>' % cls_prefix)
    return "".join(out)


def contents_section():
    out = ['<section class="contents" id="contents"><h2 id="contents-h">Contents</h2>',
           '<p>Six parts and 28 chapters. Each chapter opens with one sentence that says what it helps you do.</p>']
    for slug, name, desc in PARTS:
        out.append(f'<div class="toc-part"><h3><a href="#part-{slug}">{e(name)}</a></h3><ul class="toc-list">')
        for num, cid, cname, cpart, line in CHAPTERS:
            if cpart == slug:
                out.append(f'<li><a href="#{cid}"><span class="n">{num}</span> {e(cname)}</a><p>{e(line)}</p></li>')
        out.append('</ul></div>')
    out.append('<div class="toc-part"><h3><a href="#closing">Closing</a></h3><p class="cap">Colophon and edition notes.</p></div></section>')
    return "".join(out)


def start_section():
    return ('<section class="start" id="start"><h2 id="start-h">Where to start</h2>'
            '<p>Pick the route that matches what you came to do.</p><ul class="routes">'
            '<li><p class="route-name">New to Oath &amp; Action</p><p>Read <a href="#purpose">01 Purpose</a> first. '
            '<a href="#evidence">13 Evidence and sourcing</a> then shows how every chart and claim says what it rests on.</p></li>'
            '<li><p class="route-name">Making something</p><p>Start in <a href="#color">05 Color</a> and <a href="#identity">03 Identity</a>. '
            'Before you send anything, run <a href="#standards">28 Standards checklist</a>.</p></li>'
            '<li><p class="route-name">Building with code or an AI tool</p><p>Begin with <a href="#tokens">26 Tokens and how to choose them</a>, '
            'then take files from <a href="#assets">27 Assets and downloads</a>.</p></li></ul></section>')


def part_section(slug, name, desc):
    alias = f'<span id="{PART_ALIAS[slug]}" class="alias"></span>' if slug in PART_ALIAS else ""
    items = "".join(
        f'<li><a href="#{cid}"><span class="n">{num}</span> {e(cname)}</a><p>{e(line)}</p></li>'
        for num, cid, cname, cpart, line in CHAPTERS if cpart == slug)
    return (f'<section class="part" id="part-{slug}" data-track="part" data-part="{slug}" data-label="Part: {e(name)}">{alias}'
            f'<h2 id="part-{slug}-h"><span class="lbl">Part</span> {e(name)}</h2><p class="instr">{e(desc)}</p>'
            f'<ul class="part-list">{items}</ul></section>')


def stub_section(i):
    num, cid, cname, cpart, line = CHAPTERS[i]
    alias = f'<span id="{ALIASES[cid]}" class="alias"></span>' if cid in ALIASES else ""
    return (f'<section class="chapter stubbed" id="{cid}" data-track="chapter" data-part="{cpart}" data-label="{num} {e(cname)}">{alias}'
            f'<div class="loc"><p class="loc-line"><a href="#part-{cpart}">{e(part_name(cpart))}</a> <span aria-hidden="true">·</span> Chapter {num} of 28</p>'
            f'</div>'
            f'<h2 id="{cid}-h"><span class="n">{num}</span> {e(cname)}</h2><p class="instr">{e(line)}</p><p class="return" hidden></p>'
            f'<p class="stub">Wireframe stub. This chapter follows the template shown in full in <a href="#color">05 Color</a>.</p>'
            f'{chapnav(i)}</section>')


def build():
    frag = FRAG.read_text().replace("<!--COLOR-TABLE-->", color_table())
    ci = next(i for i, c in enumerate(CHAPTERS) if c[1] == "color")
    frag = frag.replace("<!--CHAPNAV-->", chapnav(ci))
    body = []
    for slug, name, desc in PARTS:
        body.append(part_section(slug, name, desc))
        for i, c in enumerate(CHAPTERS):
            if c[3] != slug:
                continue
            body.append(frag if c[1] == "color" else stub_section(i))
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guide shell wireframe, Edition 06 proposal</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&amp;family=Inter:wght@400;600;700&amp;family=Lora:ital,wght@1,400&amp;display=swap">
<link rel="stylesheet" href="wireframe.css">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<a class="skip" href="#contents">Skip to contents</a>
<header class="masthead">
  <a class="home" href="#top">{wordmark_svg()}<span class="edition">Brand Guide, Edition 06</span></a>
  <nav class="partnav" aria-label="Parts"><ul>
    {"".join(f'<li><a href="#part-{s}" data-part-link="{s}">{e(n)}</a></li>' for s, n, _ in PARTS)}
    <li><a href="#contents">Contents</a></li></ul></nav>
  <p class="where" id="where">Front matter</p>
  <button class="menubtn" id="menubtn" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="menu"><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span>Menu</button>
</header>
<div class="frame">
  <nav class="rail" aria-label="Chapters">{nav_list("rail")}</nav>
  <main id="main" tabindex="-1">
    <section class="cover" id="top">
      <p class="wf-label">Wireframe for Gate 1, October 21, 2026. A proposal for the Edition 06 navigation and chapter template. It is not a V6 chapter, and grey dashed boxes stand in for specimens.</p>
      <p class="eyebrow">Brand Guide · Edition 06</p>
      <h1>Oath &amp; Action Brand Guide, Edition 06</h1>
      <p class="tagline">A country that answers to its people.</p>
      <p class="pillars">Explain → Track → Connect → Act</p>
    </section>
    {contents_section()}
    {start_section()}
    {"".join(body)}
    <section class="closing" id="closing" data-track="closing" data-part="production" data-label="Closing">
      <h2 id="closing-h">Closing</h2>
      <p class="instr">Put the promise to work.</p>
      <p class="stub">Wireframe stub. The colophon and edition notes go here.</p>
      <div class="chapnav"><a href="#standards" rel="prev">Previous chapter: <span class="n">28</span> Standards checklist</a><a class="to-contents" href="#contents">Back to contents</a></div>
    </section>
  </main>
</div>
<footer class="colophon">
  <p>Oath &amp; Action Brand Guide, Edition 06. Navigation wireframe for Gate 1, prepared October 21, 2026 by the UX and accessibility lead. <a href="#contents">Back to contents</a></p>
</footer>
<dialog class="menu" id="menu" aria-labelledby="menu-h">
  <div class="menu-inner">
    <div class="menu-head"><h2 id="menu-h">Contents</h2><button type="button" class="menu-close" id="menuclose">Close</button></div>
    <p class="menu-where">You are in <strong id="menu-where-text">Front matter</strong>.</p>
    <div class="menu-scroll">
      <nav aria-label="Guide contents"><ul><li><a href="#top">Cover</a></li><li><a href="#contents">Contents, full page</a></li></ul>{nav_list("menu")}</nav>
    </div>
  </div>
</dialog>
<script src="wireframe.js"></script>
</body>
</html>
"""
    OUT.write_text(page)
    print(f"wrote {OUT.relative_to(root)} ({len(page):,} bytes)")


def board_contents():
    if not BOARD.exists():
        return
    rows = []
    for slug, name, _ in PARTS:
        chs = [c for c in CHAPTERS if c[3] == slug]
        for k, (num, cid, cname, cpart, line) in enumerate(chs):
            part_cell = f'<th scope="rowgroup" rowspan="{len(chs)}">{e(name)}</th>' if k == 0 else ""
            rows.append(f"<tr>{part_cell}<td class=\"num\">{num}</td><td><strong>{e(cname)}</strong></td><td>{e(line)}</td></tr>")
    table = ('<div class="tablewrap" role="region" aria-labelledby="contents-cap" tabindex="0"><table class="contents-table">'
             '<caption id="contents-cap">Proposed V6 contents, with the draft instruction line for each chapter</caption>'
             '<thead><tr><th scope="col">Part</th><th scope="col">No.</th><th scope="col">Chapter</th><th scope="col">Instruction line, draft for the editor</th></tr></thead>'
             f'<tbody>{"".join(rows)}</tbody></table></div>')
    s = BOARD.read_text()
    new = re.sub(r"(<!-- contents:start -->).*?(<!-- contents:end -->)", lambda m: m.group(1) + table + m.group(2), s, flags=re.S)
    if new != s:
        BOARD.write_text(new)
        print(f"updated contents table in {BOARD.relative_to(root)}")


build()
board_contents()
