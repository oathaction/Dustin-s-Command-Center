"""Shared helpers for the editor's chapters on stage board A (01 Purpose, 02 Voice).

Imported by guide_editor_build.py. Specimens are self-contained HTML fragments: colors only through var(--oa-...)
from work/build/tokens/tokens.css, text 13 px or larger, no heading elements, no landmark or article elements
(AX-S8), no em dash character anywhere (W21's specimen draws it as a rule one em wide, DR-79). The shell
(guide_build.py) scopes each fragment's <style> to its own stage, so every fragment carries the small style block
it needs.

Type sizes follow D2-254. A fixed artboard up to 600 px wide uses each style's phone floor and one 1,200 px wide or
more uses the desktop ceiling. A specimen that flows with the page (a reference table, a list, a before and after)
uses the same fixed values, switching from the phone floor to the desktop ceiling at 48em, so no size falls between
two steps of the scale. Every size is written through fx(), which takes face, weight, line height and tracking
from the type tokens (so DR-95's tracking reaches the specimens) and the size from the D2-254 table.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHAPTERS = ROOT / "work/build/guide/chapters"
SPECIMENS = ROOT / "work/build/guide/specimens"

AMP16 = "work/build/assets/identity/ampersand/20261028_Amp-B-16px-Master.svg"
AMP24 = "work/build/assets/identity/ampersand/20261028_Amp-B-24px-Master.svg"
AMP_DISPLAY = "work/build/assets/identity/ampersand/20261028_Amp-B-Display-Master.svg"
WORDMARK24 = "work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg"
WORDMARK24_PRUSSIAN = "work/build/assets/identity/prussian/20261028_Wordmark-24px-Master-Prussian-White.svg"
TILE_GRID = "work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json"
CHART_DATA = "work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json"
VOICE_CONTENT = "work/boards/phase-2/voice/20261106_Voice-Rules-Content.json"
ATLAS_DATA = "work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json"

LOCKED = {
    "tagline": "A country that answers to its people.",
    "mission": "Help people understand and improve the rules that shape their lives.",
    "promise": "We explain how a decision is made and give you a practical way to take part.",
    "commitment": "Clarity is our duty. Action is our promise.",
}
PILLARS = ["Explain", "Track", "Connect", "Act"]
# DR-111: the pillar icons are the Civic Line drawings made for the pillars, each always with its word beside it.
CL_DIR = "work/build/assets/civic-line"
PILLAR_ICON = {"Explain": "CL-019", "Track": "CL-020", "Connect": "CL-021", "Act": "CL-022"}
VOICE_LINE_B = ("We’ll explain the rules and track what happens to them. When a decision is coming, "
                "we’ll connect you with the people making it, so you can act in time.")

# H.R. 7008 at its first mention in each chapter (DR-98). The research lead checks the bill's scope in round two.
HR7008 = "H.R. 7008, the Stop Insider Trading Act"
HR7008_BOTH = ("would bar members of Congress, their spouses and dependent children from buying individual stocks, "
               "and would require photo ID to vote in federal elections")
HR7008_TRACKER = "Stop Insider Trading Act Tracker"
# Round two of the apply pass: the committee voted on a text with the stock section alone, and the photo ID section
# joined before the House vote (research lead, November 7, 2026). So each first mention describes the bill as the House
# passed it, with both provisions (DR-98), and implies nothing about the committee's text.
HR7008_FIRST = f"{HR7008}, as the House passed it, {HR7008_BOTH}"

# D2-254: each style's phone floor and desktop ceiling, in rem (16 px root).
PHONE = {"title": 3.5, "section": 2.75, "figure": 3, "h3": 1.625, "h4": 1.25, "quote": 1.5, "intro": 1.1875,
         "ask": 1.1875, "body": 1.0625, "body-small": .9375, "ui": .9375, "caption": .875, "label": .8125,
         "data-label": .8125}
DESK = dict(PHONE, title=6.875, section=5, figure=6.5, h3=2, h4=1.5, quote=2, intro=1.375)
ALLOWED_REM = sorted(set(PHONE.values()) | set(DESK.values()))

e = lambda s: html.escape(str(s), quote=True)


def q(s):
    """Curly double quotes around a line."""
    return f"“{s}”"


def fx(style, size=None, weight=None):
    """A font shorthand from the type tokens with a fixed size from the D2-254 table (the phone floor unless a size
    in rem is given). Tracking comes from the token too."""
    rem = PHONE[style] if size is None else size
    if rem not in ALLOWED_REM:
        raise SystemExit(f"fx: {rem}rem is off the type scale")
    w = weight or f"var(--oa-type-{style}-font-weight)"
    return (f"font:var(--oa-type-{style}-font-style) {w} {rem:g}rem/var(--oa-type-{style}-line-height) "
            f"var(--oa-type-{style}-font-family);letter-spacing:var(--oa-type-{style}-letter-spacing)")


def flow(sel, style, weight=None):
    """A flowing specimen's style: the phone floor, then the desktop ceiling from 48em."""
    a, b = PHONE[style], DESK[style]
    out = f"{sel}{{{fx(style, a, weight)}}}"
    if b != a:
        out += f"@media (min-width:48em){{{sel}{{font-size:{b:g}rem}}}}"
    return out


# ---------------------------------------------------------------------------------------------------------------
# Style blocks. Short names (--oa-color-text-primary and the rest) come from the stage's surface class.
# ---------------------------------------------------------------------------------------------------------------
BASE = f"""
.ed{{{fx('body')};color:var(--oa-color-text-primary);max-width:100%}}
.sp{{box-sizing:border-box;padding:16px}}
@media (min-width:48em){{.sp-flow{{padding:24px}}}}
.ed *{{box-sizing:border-box}}
.ed p{{margin:0}}
.ed .k{{{fx('label')};text-transform:uppercase;color:var(--oa-color-text-secondary)}}
.ed .src{{{fx('caption')};color:var(--oa-color-text-secondary);margin-top:12px;max-width:34rem;text-wrap:pretty}}
.ed .num{{font-variant-numeric:tabular-nums}}
.ed .chip{{display:inline-block;{fx('label')};text-transform:uppercase;line-height:1.2;padding:5px 8px;border:1px solid var(--oa-color-border-strong);white-space:nowrap}}
.ed .chip.solid{{background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label);border-color:var(--oa-color-action-primary-fill)}}
.ed del{{text-decoration:underline dotted 2px var(--oa-color-graphic-subtle);text-underline-offset:5px;text-decoration-skip-ink:none;color:inherit}}
.ed ins{{text-decoration:underline solid 2px var(--oa-color-graphic-essential);text-underline-offset:5px;text-decoration-skip-ink:none;color:inherit}}
.ed .hg{{display:flex;align-items:center;gap:12px;margin:16px 0;color:var(--oa-color-identity-hinge-divider)}}
.ed .hg::before,.ed .hg::after{{content:"";flex:1 1 0;border-top:1px solid currentColor}}
.ed .hg .hamp{{flex:none;display:block;width:21px;height:24px}}
.ed .ask{{display:inline-block;background:var(--oa-color-action-ask-fill);color:var(--oa-color-action-ask-label);font:var(--oa-type-ask);padding:12px 18px;border:1px solid var(--oa-component-button-ask-keyline);white-space:nowrap}}
.ed .lab{{{fx('label')};text-transform:uppercase;color:var(--oa-color-text-secondary);margin:0 0 6px}}
.ed .kick{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 12px;{fx('label')};text-transform:uppercase}}
.ed .kick .dot{{color:var(--oa-color-text-secondary)}}
.ed .kick .sx{{color:var(--oa-color-text-secondary)}}
.ed .kick .sxi{{display:inline-flex;align-items:center;gap:8px}}
.ed .kick .ki{{flex:none;display:block;color:var(--oa-color-graphic-essential)}}
.ed .pos{{display:inline-block;background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label);padding:3px 8px;{fx('label')};text-transform:uppercase}}
.ed table{{border-collapse:collapse;width:100%;{fx('body-small')}}}
.ed th,.ed td{{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--oa-color-border-hairline)}}
.ed thead th{{{fx('label')};text-transform:uppercase;color:var(--oa-color-text-secondary);border-bottom:2px solid var(--oa-color-border-strong)}}
.ed .lk{{font-family:var(--oa-font-family-quote);font-style:italic}}
.ed .dnp{{display:flex;align-items:center;gap:8px;margin:0 0 16px;padding:6px 10px;background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label);{fx('label')};text-transform:uppercase}}
@media (max-width:47.99em){{.ed table.stack,.ed table.stack tbody,.ed table.stack tr,.ed table.stack th,.ed table.stack td{{display:block;width:100%;min-width:0}}
.ed table.stack thead{{display:none}}.ed table.stack tr{{border-bottom:1px solid var(--oa-color-border-strong);padding:10px 0}}
.ed table.stack th,.ed table.stack td{{border:0;padding:3px 0}}.ed table.stack td[data-k]::before{{content:attr(data-k) ": ";font-weight:700}}}}
"""

# A piece at a phone's text width, 340 px (phone floor).
PIECE = f"""
.ed .pc{{width:340px;max-width:100%;background:var(--oa-color-surface-newsprint);border-top:4px solid var(--oa-color-border-strong);padding:16px 0 4px}}
.ed .pc .hl{{{fx('h3')};margin:0 0 10px;text-wrap:balance}}
.ed .pc .dek{{{fx('body')};margin:0 0 12px}}
.ed .pc .blk{{border-top:1px solid var(--oa-color-border-hairline);padding:10px 0 0;margin:12px 0 0}}
.ed .pc .wycd{{{fx('h4')};margin:0 0 8px}}
.ed .pc .step{{margin:0 0 12px}}
.ed .pc .by{{{fx('caption')};color:var(--oa-color-text-secondary);margin:12px 0 0}}
"""

# A piece on a 600 px artboard (phone floor), such as the two kinds of Act piece.
ARTICLE = f"""
.ed .art{{background:var(--oa-color-surface-newsprint)}}
.ed .art .hl{{{fx('h3')};margin:0 0 12px;text-wrap:balance}}
.ed .art .dek{{{fx('intro')};margin:0 0 16px}}
.ed .art .sec{{border-top:1px solid var(--oa-color-border-hairline);padding:14px 0 0;margin:16px 0 0}}
.ed .art .sec p+p{{margin-top:8px}}
.ed .art .two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:16px}}
.ed .art .wycd{{{fx('h4')};margin:0 0 10px}}
.ed .art .step{{margin:0 0 10px}}
.ed .art .disc{{border-left:4px solid var(--oa-color-border-strong);padding:4px 0 4px 12px;margin:14px 0}}
.ed .art .disc a,.ed .art .bio{{color:inherit;text-decoration:underline;text-underline-offset:3px}}
.ed .art .foot{{{fx('caption')};color:var(--oa-color-text-secondary);margin-top:16px}}
"""

PAIR = """
.ed.pair{max-width:760px}
.ed .ex{margin:0;padding:18px 20px;border:1px solid var(--oa-color-border-hairline);background:var(--oa-color-surface-newsprint)}
.ed .ex.after{background:var(--oa-color-surface-white);border-color:var(--oa-color-border-strong)}
.ed .exh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 12px}
""" + f""".ed .exh .s{{{fx('caption')};color:var(--oa-color-text-secondary)}}
{flow('.ed .ex .q', 'intro')}
.ed .ex .q{{margin:0;overflow-wrap:anywhere}}
.ed .ex .note{{{fx('caption')};color:var(--oa-color-text-secondary);margin-top:12px;max-width:34rem}}
.ed .emrule{{display:inline-block;width:1em;height:0;border-top:2px solid currentColor;vertical-align:.32em;margin:0 .08em}}
.ed del .emrule{{height:.47em;vertical-align:-.15em;border-bottom:2px dotted var(--oa-color-graphic-subtle)}}
"""

# A hinge headline in a flowing plate: H3 at its phone floor, 26 px, on a phone, and the section style at its phone
# floor, 44 px, from 48em. B sits at the cap height from the master Rule 04.3 names for it: the 16 px master under
# 22 px capitals (19 px here), the 24 px master to 46 px (32 px here).
HL = f"""
.ed .hh{{{fx('h3')};color:var(--oa-color-text-primary);margin:0;max-width:640px;text-wrap:balance}}
.ed .hh .hamp-h{{height:.7275em;width:auto;vertical-align:0;color:var(--oa-color-palette-pillar-red)}}
.ed .hh .hamp-h.s{{display:inline-block}}.ed .hh .hamp-h.l{{display:none}}
@media (min-width:48em){{.ed .hh{{{fx('section')}}}.ed .hh .hamp-h.s{{display:none}}.ed .hh .hamp-h.l{{display:inline-block}}}}
"""


def style(*blocks):
    return "<style>" + "".join(blocks) + "</style>"


def hinge():
    """The hinge divider inside a specimen (DR-96): ampersand B's 24 px master at 24 px, centered on a 1 px line as wide
    as the text block it divides, with 12 px of clear line on each side, in the surface's ink."""
    return (f'<div class="hg" aria-hidden="true"><img data-inline src="{AMP24}" alt="" class="hamp" '
            f'width="21" height="24"></div>')


def amp_h(label="and"):
    """Ampersand B set at a hinge headline's cap height in the view's working red, from the master Rule 04.3 names for
    each cap height HL sets: the 16 px master on a phone and the 24 px master from 48em. Only one shows at a time."""
    return "".join(f'<img data-inline src="{src}" alt="{e(label)}" class="hamp-h {k}" data-red="working" data-red-job="headline">'
                   for k, src in (("s", AMP16), ("l", AMP24)))


def ill():
    """The shell's one Illustrative label (DR-97)."""
    return '<span class="illus">Illustrative</span>'


def kicker(label, more=None, illus=False, icon=None):
    """One kicker grammar (D2-250, DR-103): the content label, then at most one more part after a middle dot, the series
    name if the piece belongs to one, otherwise the topic. "Our position" takes the position label's Charcoal fill.
    DR-112: a kicker is words; the one picture it may hold is a topic icon, 24 px in one color, directly before the topic's
    own word. `icon` is that topic's Civic Line ID, and the build checks that the icon's name is the word beside it."""
    lab = f'<span class="pos">{e(label)}</span>' if label == "Our position" else f'<span class="lb">{e(label)}</span>'
    tail = ""
    if more:
        word = f'<span class="sx">{e(more)}</span>'
        if icon:
            word = f'<span class="sxi">{cl_icon(icon, 24, cls="ki")}{word}</span>'
        tail = f'<span class="dot" aria-hidden="true">·</span>{word}'
    return f'<p class="kick">{lab}{tail}{" " + ill() if illus else ""}</p>'


def cl_file(cl_id, edition="black"):
    """The Civic Line master file for an ID and edition."""
    return sorted((ROOT / CL_DIR / edition).glob(f"*-{cl_id}-*.svg"))[0]


def cl_name(cl_id):
    """A Civic Line icon's name, from its master's file name: CL-025 is "Congress"."""
    return re.sub(r"^.*-CL-\d{3}-(.+)-Black$", r"\1", cl_file(cl_id).stem).replace("-", " ")


def cl_icon(cl_id, size, red=False, cls="cl"):
    """A Civic Line master inline at `size` px, its geometry exactly as drawn. The strokes take the icon's ink through
    currentColor; with red=True the accent part takes Pillar Red, which Rule 05.3 counts as signature red. The file's
    ids, title and desc are dropped: nothing in the drawing refers to the ids, and the word beside the icon names it,
    so the icon is hidden from assistive technology."""
    s = cl_file(cl_id, "red-black" if red else "black").read_text()
    s = re.sub(r"<\?xml.*?\?>", "", s)
    s = re.sub(r"<title>.*?</title>|<desc>.*?</desc>", "", s, flags=re.S)
    s = re.sub(r'\s(id|data-id)="[^"]*"', "", s)
    s = re.sub(r'(stroke|fill)="#121212"', r'\1="currentColor"', s)
    s = re.sub(r'(stroke|fill)="#E63946"', r'\1="var(--oa-color-palette-pillar-red)"', s)
    if re.search(r'#[0-9A-Fa-f]{6}\b', s):
        raise SystemExit(f"{cl_id}: the master holds a color this helper does not map")
    red_attr = ' data-red="signature"' if red else ""
    s = re.sub(r"<svg\b[^>]*>", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="{size}" height="{size}" '
                                f'class="{cls}" data-icon="{cl_id}" aria-hidden="true" focusable="false"{red_attr}>', s, count=1)
    return re.sub(r">\s+<", "><", s.strip())


def pillar_row(size, current=None, label="The four pillars, in order"):
    """The pillar row (DR-111): each pillar's icon with its word beside it, in order, one color. The current pillar's
    word is underlined at every size and set bold under 48 px; from 48 px its icon also keeps its red, a second sign.
    The arrows are drawn by CSS and hidden from screen readers; the list's order carries the sequence."""
    lis = []
    for p in PILLARS:
        cur = p == current
        attrs = ' class="pi cur" aria-current="true"' if cur else ' class="pi"'
        lis.append(f'<li{attrs}>{cl_icon(PILLAR_ICON[p], size, red=cur and size >= 48)}<span class="pw">{e(p)}</span></li>')
    return f'<ol class="prow prow-{size}" aria-label="{e(label)}">{"".join(lis)}</ol>'


# The pillar row's style: words in the intro style beside 48 px icons and in body bold beside 24 px icons. A row that
# no longer fits on one line wraps after an arrow; under 48em the 48 px row stacks in one column with downward arrows.
PROW = f"""
.ed .prow{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:center;row-gap:12px}}
.ed .prow .pi{{display:flex;align-items:center;gap:12px}}
.ed .prow .cl{{flex:none;display:block;color:var(--oa-color-graphic-essential)}}
.ed .prow .pi:not(:last-child)::after{{content:"→" / "";color:var(--oa-color-text-secondary);{fx('body')};margin:0 14px 0 2px}}
.ed .prow-48 .pw{{{fx('intro', weight='700')}}}
@media (min-width:48em){{.ed .prow-48 .pw{{font-size:{DESK['intro']:g}rem}}}}
.ed .prow-24 .pi{{gap:8px}}
.ed .prow-24 .pw{{{fx('body')}}}
.ed .prow .cur .pw{{text-decoration:underline solid 2px;text-underline-offset:5px;text-decoration-skip-ink:none}}
.ed .prow-24 .cur .pw{{font-weight:700}}
@media (max-width:47.99em){{.ed .prow-48{{flex-direction:column;align-items:flex-start}}
.ed .prow-48 .pi:not(:last-child)::after{{content:"↓" / "";margin:0 0 0 4px}}}}
"""


def dnp():
    """The band inside a partisan failure stage, so a cropped capture still says what it is (BE-S4)."""
    return '<p class="dnp"><span aria-hidden="true">×</span>Failure case: do not publish</p>'


def marks(s):
    """[-removed-] becomes <del> (dotted underline) and [+repair+] becomes <ins> (solid underline), as on Board 5.
    A removed em dash is drawn as a rule one em wide and named for screen readers (DR-79)."""
    t = html.escape(curl(s), quote=False)
    t = re.sub(r"\[-(.+?)-\]", r"<del>\1</del>", t)
    t = re.sub(r"\[\+(.+?)\+\]", r"<ins>\1</ins>", t)
    return t.replace("—", '<span class="emrule" role="img" aria-label="em dash"></span>')


def plain(s):
    """The text with edit marks removed, for alt text and checks."""
    return re.sub(r"\[[-+](.+?)[-+]\]", r"\1", curl(s))


def removed(s):
    return [curl(x) for x in re.findall(r"\[-(.+?)-\]", s)]


def added(s):
    return [curl(x) for x in re.findall(r"\[\+(.+?)\+\]", s)]


def curl(s):
    """Quote marks only, as Board 5's builder does: a quoted before keeps every other character as published."""
    s = str(s)
    s = re.sub(r'"([^"<>]*)"', "“\\1”", s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", "’", s)
    return re.sub(r"(?<![\w'])'([^'\n]{1,80}?)'(?![\w])", "‘\\1’", s)


def say_dash(s):
    """For alt text: name the em dash in words."""
    return s.replace("—", "(em dash)")


class Book:
    """Collects specimens and their manifest entries."""

    def __init__(self, maker="editor"):
        self.maker = maker
        self.files = {}
        self.manifest = {}

    def add(self, sid, body, *, chapter, rule, alt, width=None, illustrative=False, notes="", surface=None,
            readable=False, interactive=False, exempt=None, height=None, label=None, scale=None, css=(BASE,)):
        if sid in self.files:
            raise SystemExit(f"duplicate specimen id {sid}")
        wrap = "sp sp-fixed" if width else "sp sp-flow"
        self.files[sid] = f"<!-- {sid}: Oath & Action guide, Edition 06, chapter {chapter}. Editor, November 6, 2026. -->\n" \
                          + style(*css) + f'\n<div class="{wrap}">' + body.strip() + "</div>\n"
        m = {"chapter": chapter, "rule": rule, "width_px": width, "alt": " ".join(alt.split()),
             "illustrative": bool(illustrative), "notes": notes}
        if height:
            m["height_px"] = height
        if surface:
            m["surface"] = surface
        if readable:
            m["readable"] = True
        if interactive:
            m["interactive"] = True
        if scale:
            m["scale"] = scale
        if exempt:
            m["check_exempt"] = exempt
        if label:
            m["label"] = label
        self.manifest[sid] = m
        return sid

    def write(self):
        SPECIMENS.mkdir(parents=True, exist_ok=True)
        for old in SPECIMENS.glob("s-0[12]-*.html"):
            if old.stem not in self.files:
                old.unlink()
        for sid, txt in self.files.items():
            (SPECIMENS / f"{sid}.html").write_text(txt)
        (SPECIMENS / f"manifest-{self.maker}.json").write_text(json.dumps(self.manifest, indent=1, ensure_ascii=False) + "\n")


def write_chapter(data):
    CHAPTERS.mkdir(parents=True, exist_ok=True)
    p = CHAPTERS / f"{data['number']}-{data['anchor']}.json"
    p.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    return p


def load(rel):
    return json.loads((ROOT / rel).read_text())
