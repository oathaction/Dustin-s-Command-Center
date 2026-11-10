"""Shared helpers for the identity designer's stage board A specimens (chapters 03, 04 and 08, and the Gate 2 proofs).

Masters are placed by reference: each mark is read from its file in work/build/assets/identity/ (or the Civic Line
package) at build time and inlined unchanged, with only placement attributes added to its root element (width,
height, class, role, label, style hooks and data-master, which names the source file). Ids inside a master are
prefixed so two copies can share a page (D2-43). No master file is written.

Colors reach the marks only through the --oa- custom properties of work/build/tokens/tokens.css and the masters'
own hooks (currentColor, --amp, --lever, --link, --line).
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                      # oath-and-action-v6-brand-guide/
ID_DIR = ROOT / "work/build/assets/identity"
CL_DIR = ROOT / "work/build/assets/civic-line"
SPEC_DIR = ROOT / "work/build/guide/specimens"
CHAP_DIR = ROOT / "work/build/guide/chapters"

def E(t):
    """Escape for HTML text and double-quoted attributes. Apostrophes stay as typed, so the quote helper can curl them."""
    return html.escape(str(t), quote=False).replace('"', "&quot;")


SURFACES = ("newsprint", "white", "charcoal", "prussian")

# --------------------------------------------------------------------------------------------- quotation marks
# Rule 06.7: curly quotation marks and apostrophes. Every visible string runs through the editor's helper (C-S9).
sys.path.insert(0, str(HERE))
try:
    from guide_editor_common import curl as _curl  # noqa: E402
except Exception:                                   # the editor's file is being rewritten; same rules as its curl()
    def _curl(s):
        s = str(s)
        s = re.sub(r'"([^"<>]*)"', "\u201c\\1\u201d", s)
        s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", "\u2019", s)
        return re.sub(r"(?<![\w'])'([^'\n]{1,80}?)'(?![\w])", "\u2018\\1\u2019", s)


def curl(t):
    return _curl(t) if isinstance(t, str) else t


def curl_html(s):
    """Curl the quotation marks in an HTML fragment's text and in its alt and aria-label values, leaving markup,
    <style> and <script> untouched."""
    out = []
    for part in re.split(r"(<style\b.*?</style>|<script\b.*?</script>|<[^>]+>)", s, flags=re.S):
        if not part:
            continue
        if part.startswith("<style") or part.startswith("<script"):
            out.append(part)
        elif part.startswith("<"):
            out.append(re.sub(r'\b(alt|aria-label)="([^"]*)"', lambda m: f'{m.group(1)}="{curl(m.group(2))}"', part))
        else:
            out.append(curl(part.replace("&#x27;", "'")))
    return "".join(out)


def rel(p):
    return str(Path(p).resolve().relative_to(ROOT))


# --------------------------------------------------------------------------------------------- tokens
def tv(name):
    """A token reference, written as var(--oa-...)."""
    return f"var(--oa-{name})"


def ink(s):
    return tv(f"color-text-primary-on-{s}")


def ink2(s):
    return tv(f"color-text-secondary-on-{s}")


def sig(s):
    return tv(f"color-identity-signature-on-{s}")


def ground(s):
    return tv(f"color-surface-{s}")


def hair(s):
    return tv(f"color-border-hairline-on-{s}")


def strong(s):
    return tv(f"color-border-strong-on-{s}")


def g_ess(s):
    return tv(f"color-graphic-essential-on-{s}")


def g_sub(s):
    return tv(f"color-graphic-subtle-on-{s}")


def pal(n):
    return tv(f"color-palette-{n}")


RED = pal("pillar-red")


def mark_style(surface, mode="color"):
    """CSS for a master's hooks on a surface (the identity masters board's mapping, as tokens).

    color: Charcoal letters, red ampersand and lever, Stone links and lines on Newsprint and White; Newsprint letters,
    links and lines with red on Charcoal. Prussian takes the explicit-White files (treatment D), so no hooks.
    mono: every part in one ink, Charcoal on light grounds and White on dark ones.
    """
    if mode == "mono-dark":
        c = pal("charcoal")
        return f"color:{c};--amp:{c};--lever:{c};--link:{c};--line:{c}"
    if mode == "mono-light":
        c = pal("white")
        return f"color:{c};--amp:{c};--lever:{c};--link:{c};--line:{c}"
    if mode == "mono":
        c = ink(surface)
        return f"color:{c};--amp:{c};--lever:{c};--link:{c};--line:{c}"
    if mode == "divider":
        c = tv(f"color-identity-hinge-divider-on-{surface}")
        return f"color:{c};--amp:{c}"
    if mode == "ink":           # the surface's ink for every part (editorial crop)
        c = ink(surface)
        return f"color:{c};--amp:{c};--lever:{c}"
    if surface in ("newsprint", "white"):
        return f"color:{ink(surface)};--amp:{sig(surface)};--lever:{sig(surface)};--link:{pal('stone')};--line:{pal('stone')}"
    if surface == "charcoal":
        n = pal("newsprint")
        return f"color:{ink('charcoal')};--amp:{sig('charcoal')};--lever:{sig('charcoal')};--link:{n};--line:{n}"
    return f"color:{pal('white')}"


_uid = [0]
INLINE_ALL = [False]          # set True for standalone pages (the letterhead PDF), which no build inlines
LORA = "reexport/20261028_Amp-V5-Lora-Master-Reexported.svg"


def _prussian_file(relpath):
    p = Path(relpath)
    cand = ID_DIR / "prussian" / (p.stem + "-Prussian-White.svg")
    return cand if cand.exists() else None


def _vb(path):
    s = Path(path).read_text()
    m = re.search(r"<svg\b([^>]*)>", s)
    return [float(v) for v in re.search(r'viewBox="([^"]+)"', m.group(1)).group(1).replace(",", " ").split()]


def svg_file(path, *, w=None, h=None, label=None, style="", cls="", red=None, decorative=False, extra="", by_ref=None):
    """Place one SVG file at a set size. Exactly one of w or h may be given; the other follows the viewBox.

    Identity masters and Civic Line files are placed by reference: an <img data-inline src="work/..."> that the guide
    build (guide_build.py) inlines as SVG, so the fragment holds the path and never a copy of the drawing. Files with
    ids that may repeat inside one specimen (the re-exported taglines) are inlined here with their ids prefixed."""
    path = Path(path)
    if by_ref is None:
        by_ref = not INLINE_ALL[0] and "reexport" not in path.parts
    if by_ref:
        vb = _vb(path)
        if w is None and h is None:
            h = vb[3]
        if w is None:
            w = h * vb[2] / vb[3]
        if h is None:
            h = w * vb[3] / vb[2]
        alt = "" if decorative else (label or path.stem)
        st = f' style="{style}"' if style else ""
        out = (f'<img data-inline src="{rel(path)}" alt="{E(alt)}" width="{w:.2f}" height="{h:.2f}" class="oai-svg {cls}"{st}>')
        if red:
            return f'<span class="oai-red" data-red="{red[0]}"' + (f' data-red-job="{E(red[1])}"' if len(red) > 1 else "") + f">{out}</span>"
        return out
    s = path.read_text()
    s = re.sub(r"<\?xml[^>]*\?>\s*", "", s).strip()
    s = re.sub(r"<(title|desc)\b[^>]*>.*?</\1>", "", s, flags=re.S)   # the file's record notes stay in the file
    m = re.match(r"<svg\b([^>]*)>", s)
    attrs = m.group(1)
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', attrs).group(1).replace(",", " ").split()]
    if w is None and h is None:
        h = vb[3]
    if w is None:
        w = h * vb[2] / vb[3]
    if h is None:
        h = w * vb[3] / vb[2]
    _uid[0] += 1
    pre = f"oai{_uid[0]}"
    ids = set(re.findall(r'\bid="([^"]+)"', s))
    for i in sorted(ids, key=len, reverse=True):
        s = s.replace(f'id="{i}"', f'id="{pre}-{i}"').replace(f"url(#{i})", f"url(#{pre}-{i})").replace(f'href="#{i}"', f'href="#{pre}-{i}"')
    body = s[m.end():]
    keep = re.sub(r'\s(width|height|id|style|class|role|aria-[a-z]+|focusable|data-id)="[^"]*"', "", attrs)
    a11y = 'aria-hidden="true"' if decorative else f'role="img" aria-label="{E(label or path.stem)}"'
    st = f' style="{style}"' if style else ""
    root = (f'<svg{keep} width="{w:.2f}" height="{h:.2f}" class="oai-svg {cls}"{st} {a11y} focusable="false" '
            f'data-master="{rel(path)}"{extra}>')
    out = root + body
    if red:
        return f'<span class="oai-red" data-red="{red[0]}"' + (f' data-red-job="{E(red[1])}"' if len(red) > 1 else "") + f">{out}</span>"
    return out


def mark(relpath, *, w=None, h=None, surface="newsprint", mode="color", label=None, cls="", decorative=False, red_job=None, extra=""):
    """Place an identity master on a surface. On Prussian (color mode) the explicit-White file is placed."""
    path = ID_DIR / relpath
    style = mark_style(surface, mode)
    glyph = relpath.startswith(("ampersand/", "badge/")) or relpath == LORA
    if glyph and mode == "color" and surface != "prussian":
        style = f"color:{sig(surface)}"          # the ampersand and the badge are drawn whole in signature red
    if surface == "prussian" and mode == "color":
        alt = _prussian_file(relpath)
        if alt is not None:
            path, style = alt, ""
        elif glyph:
            style = f"color:{pal('white')}"       # treatment D for the narrow drawings, which have no White file
    text = path.read_text()
    has_red = ((("--amp" in text or "--lever" in text) or glyph) and mode == "color" and surface != "prussian")
    red = None
    if has_red:
        red = ("working", red_job) if red_job else ("signature",)
    return svg_file(path, w=w, h=h, label=label, style=style, cls=cls, red=red, decorative=decorative, extra=extra)


def icon(cl_id, *, size=24, edition="black", label=None, decorative=False, surface="newsprint"):
    """Place a Civic Line icon from the approved package (D2-52), one color, by reference (the build makes it a data URI)."""
    f = sorted((CL_DIR / edition).glob(f"*-{cl_id}-*.svg"))[0]
    alt = "" if decorative else (label or cl_id)
    return f'<img src="{rel(f)}" alt="{E(alt)}" width="{size}" height="{size}" class="oai-svg oai-icon">'


# --------------------------------------------------------------------------------------------- file names
WM = {"display": "wordmark/20261028_Wordmark-Display-Master.svg", 24: "wordmark/20261028_Wordmark-24px-Master.svg",
      16: "wordmark/20261028_Wordmark-16px-Master.svg"}
WMC = {"display": "wordmark-condensed/20261028_Wordmark-Condensed-Display-Master.svg",
       24: "wordmark-condensed/20261028_Wordmark-Condensed-24px-Master.svg",
       16: "wordmark-condensed/20261028_Wordmark-Condensed-16px-Master.svg"}
AMP = {"display": "ampersand/20261028_Amp-B-Display-Master.svg", 24: "ampersand/20261028_Amp-B-24px-Master.svg",
       16: "ampersand/20261028_Amp-B-16px-Master.svg"}
AMPN = {"display": "ampersand/20261028_Amp-B-Narrow-Display-Master.svg", 24: "ampersand/20261028_Amp-B-Narrow-24px-Master.svg",
        16: "ampersand/20261028_Amp-B-Narrow-16px-Master.svg"}
LOCK = {"display": "lockmark/20261107_Lockmark-Display-Master.svg", 48: "lockmark/20261109_Lockmark-48px-Master-Outline.svg",
        24: "lockmark/20261109_Lockmark-24px-Master-Outline.svg", 16: "lockmark/20261028_Lockmark-16px-Master.svg"}
# Promotion, November 10, 2026 (DR-181): the rebuilt 24 and 48 px masters, each node and the lever one outline, are the
# files in use. They draw the same pixels as the earlier files at 24 and 48 px (DR-145), and between those sizes their
# nodes stay whole. The earlier files, one rect per pixel row, stay in lockmark/ as the record; the scripts that drew
# earlier boards read them from LOCK_RECT, so a rerun keeps its record. The 16 px master stays as it is (D2-542).
LOCK_RECT = {48: "lockmark/20261108_Lockmark-48px-Master.svg", 24: "lockmark/20261028_Lockmark-24px-Master.svg"}
# The end mark on a 1x screen (DR-180): ampersand B drawn on whole pixels, fit B, sitting on the baseline. Keyed by the
# text size each serves: (file, width px, height px). On other screens and at other text sizes, the 16 px master at the
# text's cap height (stage_a_identity_s04.end_b).
AMP_END = {17: ("ampersand/20261109_Amp-B-14px-End-Mark-Fit-B.svg", 13, 13),
           15: ("ampersand/20261109_Amp-B-12px-End-Mark-Fit-B.svg", 11, 11)}
# The lockmark's four masters and the heights each covers (Q1 to Q4 pass, November 8, 2026; DR-131): the 16 px master
# from 16 to 23 px, the 24 px master from 24 to 47 px, the 48 px master at 48 px, and the display master from 49 px.
# stage_a_identity_q_measure.py's range test chose the switch: built from one rect per pixel row, the 48 px master
# parts into stripes at any size between whole multiples of its grid (its node cores fall to 0 to 72 percent full
# color from 49 to 95 px at 1x), while the display master draws each part as one shape at every size.
LOCK_DISPLAY_FROM = 49
BADGE = {"display": "badge/20261028_Hinge-Badge-Display-Master.svg", 24: "badge/20261028_Hinge-Badge-24px-Master.svg",
         16: "badge/20261028_Hinge-Badge-16px-Master.svg"}
L2 = {"today": "lockups/20261028_L2-Stacked-Master.svg", "condensed": "lockups/20261028_L2-Stacked-Condensed-Master.svg"}
L3 = {"today": "lockups/20261028_L3-Horizontal-Master.svg", "condensed": "lockups/20261028_L3-Horizontal-Condensed-Master.svg",
      "masthead": "lockups/20261110_L3-Horizontal-Master.svg", "masthead_rect": "lockups/20261108_L3-Horizontal-Master.svg"}
# L3 at the masthead since November 8, 2026 (DR-131): the 24 px wordmark master, 13 px of space and the lockmark's 48 px
# master, on the pixel grid, 282 by 48 px. Since November 10, 2026 (DR-181) the masthead master is the file that carries
# the rebuilt 48 px lockmark, written by promotion_identity.py; the November 8 file (stage_a_identity_s1.py) and the
# October file stay as the record.
L8 = {"today": "lockups/20261028_L8-Monogram-Master.svg", "condensed": "lockups/20261028_L8-Monogram-Condensed-Master.svg"}
HINGE = {"display": "hinge/20261028_Hinge-Diagram-V2-Display-Master.svg", "compact": "hinge/20261028_Hinge-Diagram-V2-Compact-Master.svg"}
# S1, the stacked lockup that replaced L2 (DR-113), written by stage_a_identity_s1.py from Board 6's files.
S1 = {"display": "lockups/20261107_S1-Stacked-Master.svg", 24: "lockups/20261107_S1-Stacked-Master-24px.svg",
      16: "lockups/20261107_S1-Stacked-Master-16px.svg"}
S1_BOX = {"display": (508.63, 218.81, 100.0), 24: (115.0, 50.0, 22.0), 16: (79.0, 33.0, 14.0)}   # width, height, capitals
TL1 = "reexport/20261028_Tagline-1-Line-Reexported.svg"
TL2A = "reexport/20261028_Tagline-2-Line-A-Reexported.svg"
TL2B = "reexport/20261028_Tagline-2-Line-B-Reexported.svg"

# master widths in px at their native heights, and display widths in units (cap height 100, box 108)
WM_W = {"today": {"display": 978.31, 24: 221, 16: 152}, "condensed": {"display": 770.07, 24: 181, 16: 120}}


def wordmark(height, *, width="today", surface="newsprint", mode="color", label="Oath & Action", decorative=False):
    """The wordmark at a box height in px, from the master whose range holds it (I8: 16 px master to 19 px tall,
    24 px master to 39 px, display from 40 px)."""
    files = WM if width == "today" else WMC
    if height < 20:
        key = 16
    elif height < 40:
        key = 24
    else:
        key = "display"
    return mark(files[key], h=height, surface=surface, mode=mode, label=label, decorative=decorative)


def amp(height, *, narrow=False, surface="newsprint", mode="color", label="Ampersand", decorative=False, red_job=None):
    files = AMPN if narrow else AMP
    key = 16 if height < 24 else (24 if height < 48 else "display")
    return mark(files[key], h=height, surface=surface, mode=mode, label=label, decorative=decorative, red_job=red_job)


FIGURES = ROOT / "work/handoffs/phase-2/20261108_Q1-To-Q4-Identity-Figures.json"
# Promotion, November 10, 2026: figures measured with the finals in use (the feed test with the rebuilt 48 px master, the
# end mark's pixel masters), written by promotion_identity.py. A key found there wins over the Q1 to Q4 file's.
FIGURES_PROMOTION = ROOT / "work/handoffs/phase-2/20261110_Promotion-Identity-Figures.json"
# Stage C round 0, November 10, 2026 (CD-N12): the feed test on dark cards, written by stage_c_identity_round0.py feed
FIGURES_STAGE_C = ROOT / "work/handoffs/phase-2/20261110_Stage-C-Identity-Figures.json"


def figures(key):
    """Measured figures the chapters print (Q1 to Q4 pass): 'endmark', 'feed' or 'range', written by
    stage_a_identity_q_measure.py, and from the promotion 'feed' again and 'endmark_fit', written by
    promotion_identity.py, and from stage C 'feed_dark', written by stage_c_identity_round0.py. None, with a
    warning, when the test has not run; the page then prints a marker that the
    build's own text scan would show, and the maker reruns the test and the build."""
    import json as _json
    d = _json.loads(FIGURES.read_text()) if FIGURES.exists() else {}
    if FIGURES_PROMOTION.exists():
        d.update({k: v for k, v in _json.loads(FIGURES_PROMOTION.read_text()).items() if k in ("feed", "endmark_fit")})
    if FIGURES_STAGE_C.exists():
        d.update({k: v for k, v in _json.loads(FIGURES_STAGE_C.read_text()).items() if k in ("feed_dark",)})
    if key not in d:
        print(f"  WARNING: no '{key}' figures in {FIGURES.name} or {FIGURES_PROMOTION.name}; run the test that writes it, then build again")
        return None
    if key == "feed" and LOCK[48] not in str(d[key].get("lockmark_master", "")):
        print(f"  WARNING: the feed figures were measured on {d[key].get('lockmark_master')}, not {LOCK[48]}; run the feed test again")
    return d[key]


def lockmark(size, *, surface="newsprint", mode="color", label="Lockmark", decorative=False):
    key = 16 if size < 24 else (24 if size < 48 else (48 if size < LOCK_DISPLAY_FROM else "display"))
    return mark(LOCK[key], h=size, surface=surface, mode=mode, label=label, decorative=decorative)


def s1_key(caps):
    """S1's master for a cap height: the 16 px master for capitals 14 to 17 px, the 24 px master for 18 to 36 px, the
    display master from 37 px (Board 6's ranges, which follow the wordmark's by height)."""
    return 16 if caps < 18 else (24 if caps < 37 else "display")


def s1(caps, *, surface="newsprint", mode="color", label="Oath & Action, S1 stacked lockup", decorative=False):
    """S1 at a cap height in px, from the master whose range holds it."""
    key = s1_key(caps)
    w, h, c = S1_BOX[key]
    return mark(S1[key], h=h * caps / c, surface=surface, mode=mode, label=label, decorative=decorative)


def s1_width(caps):
    w, h, c = S1_BOX[s1_key(caps)]
    return w * caps / c


# ------------------------------------------------------------------- the grid as a code (retired, DR-110)
# Kept only to draw chapter 08's failure case, a tracker on the lockmark's grid. Lattices on whole pixels. 24 px follows the 24 px lockmark master (centers 3.5, 11.5, 19.5). 40 px keeps the same
# margins with a 16 px pitch (3.5, 19.5, 35.5). 80 px is the 40 px drawing at twice size.
LATTICE = {24: (24, (3.5, 11.5, 19.5)), 40: (40, (3.5, 19.5, 35.5))}
POS = {"TL": (0, 0), "TM": (1, 0), "TR": (2, 0), "ML": (0, 1), "C": (1, 1), "MR": (2, 1), "BL": (0, 2), "BM": (1, 2), "BR": (2, 2)}
PILLAR_CORNER = {"Explain": "TL", "Track": "TR", "Connect": "BL", "Act": "BR"}
STAGES = ["Filed", "Sent to committee", "Hearing", "Out of committee", "Passed one chamber", "Passed both chambers",
          "Final text agreed", "Signed", "In effect"]
# What each stage means, in plain words (H02, CP-M9). Printed once per tracker page and in the stages sheet.
GLOSS = ["A legislator introduced the bill.",
         "The bill went to the committee that studies its subject.",
         "The committee heard from the public.",
         "The committee voted to send it to the full chamber, the House or the Senate.",
         "The House or the Senate approved it.",
         "The other chamber approved it too.",
         "Both chambers agreed on one text.",
         "The governor signed it into law.",
         "The law now applies."]
SERIES = [  # V5's six series and routes (V5 07, "Six series, six routes"); "Dispatch from the Front" renamed (S2)
    ("Reform 101", "Explain", ["BL", "ML", "TL"]),
    ("The Oath", "Explain", ["TR", "TM", "TL"]),
    ("Dispatch", "Track", ["ML", "C", "MR", "TR"]),
    ("The Public Record", "Track", ["BR", "MR", "TR"]),
    ("Field Notes", "Connect", ["C", "BM", "BL"]),
    ("Proof It Works", "Act", ["TM", "C", "BM", "BR"]),
]
NAMES = {"TL": "top left", "TM": "top middle", "TR": "top right", "ML": "middle left", "C": "center", "MR": "middle right",
         "BL": "bottom left", "BM": "bottom middle", "BR": "bottom right"}


def sgrid(size, *, nodes=None, route=None, surface="newsprint", label=None, decorative=False, cls="", links=True,
          step_job="the step a reader can take now"):
    """Draw the grid as a code, for a failure case only (DR-110 retires every coded grid).

    nodes: nine states in reading order (left to right, top to bottom): 'off' small subtle node, 'done' filled disc,
    'now' ring (7 px outside, 1 px line, so its 5 px hole reads at 40 px), 'gap' no node and its links cut, 'step' working-red disc with a keyline, 'lit' corner disc,
    'none' nothing at all (loading). route: a list of positions; route nodes 5 px, the end 7 px, a 3 px bar between.
    """
    base = 40 if size >= 40 else 24
    field, c = LATTICE[base]
    nodes = list(nodes or ["off"] * 9)
    e, sb = g_ess(surface), g_sub(surface)
    parts = []
    gaps = [i for i, n in enumerate(nodes) if n == "gap"]
    if links:
        for r in range(3):
            for k in range(2):
                parts.append(_seg((k, r), (k + 1, r), c, sb, 1, gaps))
                parts.append(_seg((r, k), (r, k + 1), c, sb, 1, gaps))
    if route:
        for a, b in zip(route, route[1:]):
            parts.append(_seg(POS[a], POS[b], c, e, 3, []))
        for i, p in enumerate(route):
            col, row = POS[p]
            nodes[row * 3 + col] = "lit" if i == len(route) - 1 else "route"
    for i, n in enumerate(nodes):
        x, y = c[i % 3], c[i // 3]
        if n == "off":
            parts.append(f'<circle cx="{x}" cy="{y}" r="1.5" fill="{sb}"/>')
        elif n in ("done", "lit"):
            parts.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{e}"/>')
        elif n == "route":
            parts.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{e}"/>')
        elif n == "now":
            parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="none" stroke="{e}" stroke-width="1"/>')
        elif n == "step":
            if surface == "prussian":
                raise ValueError("Rule 05.3: red never sits on Prussian")
            kl = f' stroke="{strong(surface)}" stroke-width="1"' if surface in ("newsprint", "white") else ""
            rr = "3" if kl else "3.5"
            parts.append(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{RED}"{kl} data-red="working" data-red-job="{E(step_job)}"/>')
    a11y = 'aria-hidden="true"' if decorative else f'role="img" aria-label="{E(label or "The lockmark grid")}"'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {field} {field}" width="{size}" height="{size}" '
           f'class="oai-svg oai-grid {cls}" shape-rendering="geometricPrecision" {a11y} focusable="false">{"".join(parts)}</svg>')
    if "step" in nodes:
        svg = f'<span class="oai-red" data-red="working" data-red-job="{E(step_job)}">{svg}</span>'
    return svg


def _seg(a, b, c, color, t, gaps):
    """One link from node a to node b as a rect of thickness t, shortened by 5 px at a gap node."""
    (ax, ay), (bx, by) = a, b
    x1, y1, x2, y2 = c[ax], c[ay], c[bx], c[by]
    ia, ib = ay * 3 + ax, by * 3 + bx
    cut_a = 5 if ia in gaps else 0
    cut_b = 5 if ib in gaps else 0
    if y1 == y2:
        xs, xe = min(x1, x2) + (cut_a if x1 < x2 else cut_b), max(x1, x2) - (cut_b if x1 < x2 else cut_a)
        if xe <= xs:
            return ""
        return f'<rect x="{xs:g}" y="{y1 - t / 2:g}" width="{xe - xs:g}" height="{t:g}" fill="{color}"/>'
    ys, ye = min(y1, y2) + (cut_a if y1 < y2 else cut_b), max(y1, y2) - (cut_b if y1 < y2 else cut_a)
    if ye <= ys:
        return ""
    return f'<rect x="{x1 - t / 2:g}" y="{ys:g}" width="{t:g}" height="{ye - ys:g}" fill="{color}"/>'


def progress(stage, *, now=False, gap=None, step=None, final=False):
    """Nine node states for a tracker at a stage (1 to 9). now: the stage is under way (a ring). gap: a stage that
    never happened. step: the stage where a reader can take part now (working red)."""
    out = []
    for i in range(1, 10):
        if final or i < stage:
            out.append("done")
        elif i == stage:
            out.append("now" if now else "done")
        else:
            out.append("off")
    if gap:
        out[gap - 1] = "gap"
    if step:
        out[step - 1] = "step"
    return out


def corner(pillar):
    out = ["off"] * 9
    col, row = POS[PILLAR_CORNER[pillar]]
    out[row * 3 + col] = "lit"
    return out


# --------------------------------------------------------------------------------------------- page bits
def illus():
    """The shell's one Illustrative label (DR-97, C-S8): <span class="illus">Illustrative</span>, never restyled."""
    return '<span class="illus">Illustrative</span>'


def head_label(scope=""):
    """One label at the head of a piece. scope names what is invented when real and invented items mix."""
    tail = f' <span class="oai-tag">{E(scope)}</span>' if scope else ""
    return f'<p class="oai-head">{illus()}{tail}</p>'


def dnp():
    """The Charcoal band inside a failure stage that could pass for our work, so a cropped capture still says what it
    is. Same form as the editor's and the systems designer's bands (D2-282, D2-308)."""
    return '<p class="oai-dnp"><span aria-hidden="true">×</span>Failure case: do not publish</p>'


# ------------------------------------------------------------------------- numbered steps, as chapter 11 draws them
# Board 6's Option B, which Dustin chose for lists and story cards (DR-108, DR-109, DR-128), drawn with the same
# geometry as work/build/scripts/phase-2/board6_tracker_build.py (b_node, mk_steps, line_segments) and colored with
# tokens. Chapter 11 owns these marks; chapter 08 shows them once, beside the failure they replace.
STEP_NAMES_STATE = ["Filed", "Hearing", "Committee vote", "First chamber", "Second chamber", "Governor"]


def _step_node(cx, cy, d, st, num, surface):
    ink_, sub, bg, t2 = g_ess(surface), g_sub(surface), ground(surface), ink2(surface)
    R = d / 2
    fs = 14 if d >= 28 else 13
    ty_ = cy + 0.36 * fs
    txt = (f'font-family="Inter, Arial, sans-serif" font-size="{fs}" text-anchor="middle" '
           f'style="font-family:var(--oa-font-family-reading);font-variant-numeric:tabular-nums"')
    if st == "done":
        return (f'<circle cx="{cx:g}" cy="{cy:g}" r="{R:g}" fill="{ink_}"/>'
                f'<text x="{cx:g}" y="{ty_:.2f}" font-weight="700" fill="{bg}" {txt}>{num}</text>')
    if st == "now":
        return (f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 1.5:g}" fill="{bg}" stroke="{ink_}" stroke-width="3"/>'
                f'<text x="{cx:g}" y="{ty_:.2f}" font-weight="800" fill="{ink_}" {txt}>{num}</text>')
    if st == "notyet":
        return (f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 0.75:g}" fill="{bg}" stroke="{sub}" stroke-width="1.5"/>'
                f'<text x="{cx:g}" y="{ty_:.2f}" font-weight="600" fill="{t2}" {txt}>{num}</text>')
    raise ValueError(st)


STEP_ICON = {"done": "S-done", "now": "S-now", "notyet": "S-not-yet"}      # chapter 11's status ids (D2-517)


def steps(states, W=324, d=26, surface="newsprint", flush=False, tag=False):
    """Six numbered steps on a line: solid 2 px where the bill has come, a fine line ahead. Hidden from assistive
    technology; the words beside it carry the step. flush sets the first and last circles at the edges, as chapter 11's
    lists draw them (360 px list: W 328, circles 60 px apart); tag wraps each mark in a group with its status id and
    data-icon-family, as chapter 11 does (round 2)."""
    c = W // 6
    xs = [d / 2 + i * (W - d) / 5 for i in range(6)] if flush else [c * i + c // 2 for i in range(6)]
    R = d / 2
    cy = 6 + R
    H = int(cy + R + 2)
    body = []
    for i in range(5):
        if states[i + 1] != "notyet":
            body.append(f'<rect x="{xs[i]:g}" y="{cy - 1:g}" width="{xs[i + 1] - xs[i]:g}" height="2" fill="{g_ess(surface)}"/>')
        else:
            body.append(f'<rect x="{xs[i]:g}" y="{cy - 1:g}" width="{xs[i + 1] - xs[i]:g}" height="1" fill="{g_sub(surface)}"/>')
    nodes = [_step_node(x, cy, d, s, i + 1, surface) for i, (x, s) in enumerate(zip(xs, states))]
    if tag:
        nodes = [f'<g data-icon="{STEP_ICON[s]}" data-icon-family="status">{n}</g>' for n, s in zip(nodes, states)]
    body += nodes
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" class="oai-svg" '
            f'aria-hidden="true" focusable="false">{"".join(body)}</svg>')


# ------------------------------------------------------------------------------- type on fixed artboards (D2-254)
# Up to 600 px wide: each style's phone floor. 1,200 px and wider: its desktop ceiling. Print: points (D2-205).
FLOOR = {"title": 56, "section": 44, "figure": 48, "h3": 26, "h4": 20, "quote": 24, "intro": 19, "ask": 19, "body": 17,
         "body-small": 15, "ui": 15, "caption": 14, "label": 13, "data-label": 13}
CEIL = dict(FLOOR, title=110, section=80, figure=104, h3=32, h4=24, quote=32, intro=22)


def ty(style, board=600, size=None):
    """CSS for a type style at its fixed size on an artboard of a given width: face, weight, size, line height and
    tracking from the style's tokens, so the tracking follows tokens.css."""
    px = size or (CEIL if board >= 1200 else FLOOR)[style]
    t = f"--oa-type-{style}"
    css = (f"font-family:var({t}-font-family);font-weight:var({t}-font-weight);font-style:var({t}-font-style);"
           f"font-size:{px}px;line-height:var({t}-line-height);letter-spacing:var({t}-letter-spacing)")
    if style == "label":
        css += ";text-transform:uppercase"
    return css


def tag(text):
    return f'<span class="oai-tag">{E(text)}</span>'


CSS = """
.oai{font-family:var(--oa-font-family-reading);font-size:15px;line-height:1.5;color:var(--oa-color-text-primary-on-newsprint)}
.oai *{box-sizing:border-box}
.oai p{margin:0}
.oai .oai-svg{display:block;flex:none;max-width:none;overflow:visible}
.oai .oai-red{display:inline-block;line-height:0}
.oai-panel{padding:24px;border:1px solid var(--oa-color-border-hairline-on-newsprint)}
.oai-pad{padding:24px}
.oai-s-newsprint{background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint)}
.oai-s-white{background:var(--oa-color-surface-white);color:var(--oa-color-text-primary-on-white)}
.oai-s-charcoal{background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);border-color:var(--oa-color-surface-charcoal)}
.oai-s-prussian{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);border-color:var(--oa-color-surface-prussian)}
.oai-row{display:flex;flex-wrap:wrap;gap:24px 32px;align-items:flex-end}
.oai-row.top{align-items:flex-start}
.oai-row.mid{align-items:center}
.oai-cell{display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.oai-stack{display:flex;flex-direction:column;gap:16px}
.oai-tag{font:600 13px/1.4 var(--oa-font-family-reading);color:var(--oa-color-text-secondary-on-newsprint)}
.oai-s-white .oai-tag{color:var(--oa-color-text-secondary-on-white)}
.oai-s-charcoal .oai-tag{color:var(--oa-color-text-secondary-on-charcoal)}
.oai-s-prussian .oai-tag{color:var(--oa-color-text-secondary-on-prussian)}
.oai .oai-head{display:flex;flex-wrap:wrap;align-items:center;gap:4px 0;margin:0 0 12px}
.oai-note{font-size:14px;color:var(--oa-color-text-secondary-on-newsprint);max-width:62ch}
.oai-label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase}
.oai-num{font-variant-numeric:tabular-nums}
.oai table{border-collapse:collapse;font-size:14px;line-height:1.45}
.oai th,.oai td{text-align:left;vertical-align:top;padding:8px 12px 8px 0;border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint)}
.oai thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--oa-color-text-secondary-on-newsprint);border-bottom:2px solid var(--oa-color-border-strong-on-newsprint)}
@media (max-width:35.49em){.oai table.stack,.oai table.stack tbody,.oai table.stack tr,.oai table.stack th,.oai table.stack td{display:block;width:100%}.oai table.stack thead,.oai table.stack caption+thead{display:none}.oai table.stack tr{border-bottom:1px solid var(--oa-color-border-strong-on-newsprint);padding:10px 0}.oai table.stack caption{display:block;width:100%}.oai table.stack th,.oai table.stack td{border:0;padding:2px 0}.oai table.stack td[data-k]::before{content:attr(data-k) ": ";font-weight:700}}
.oai th{font-weight:700}
.oai-fail-x{display:none}
.oai .oai-dnp{display:flex;align-items:center;gap:8px;margin:0;padding:6px 10px;background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label);font:var(--oa-type-label-font-style) var(--oa-type-label-font-weight) 0.8125rem/var(--oa-type-label-line-height) var(--oa-type-label-font-family);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase}
"""


def raster_png(html_body, w, h, name, scale=2):
    """Render a small piece of HTML to a PNG data URI with Chromium: at twice size for a failure case that must show
    text under the 13 px floor as an image (D1-09), or at 1x to show how a master falls on the pixel grid."""
    import base64
    import subprocess
    import tempfile
    tmpd = Path(tempfile.mkdtemp(prefix="oai-raster-"))
    out = tmpd / f"oai-{name}.png"
    tokens = (ROOT / "work/build/tokens/tokens.css").resolve()
    page = ('<!doctype html><html><head><meta charset="utf-8">'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="file://{tokens}">'
            '<style>body{margin:0;background:var(--oa-color-surface-newsprint);font-family:Inter;color:var(--oa-color-text-primary-on-newsprint)}</style></head>'
            f'<body><div id="c" style="width:{w}px;height:{h}px;overflow:hidden">{html_body}</div></body></html>')
    tmp = tmpd / f"oai-{name}.html"
    tmp.write_text(page)
    js = HERE / "stage_a_identity_raster.js"
    subprocess.run(["node", str(js), str(tmp), str(out), str(w), str(h), str(scale)], check=True, capture_output=True)
    return "data:image/png;base64," + base64.b64encode(out.read_bytes()).decode()


def inline_master(relpath, h, style=""):
    """A master's SVG text, for a standalone page that no build inlines (rasters, the letterhead PDF)."""
    s = (ID_DIR / relpath).read_text()
    s = re.sub(r"<\?xml[^>]*\?>\s*", "", s).strip()
    s = re.sub(r"<(title|desc)\b[^>]*>.*?</\1>", "", s, flags=re.S)
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).replace(",", " ").split()]
    w = h * vb[2] / vb[3]
    s = re.sub(r"<svg\b([^>]*)>", lambda m: "<svg" + re.sub(r'\s(width|height|style)="[^"]*"', "", m.group(1))
               + f' width="{w:.2f}" height="{h:.2f}" style="display:block;{style}">', s, count=1)
    return s


def fragment(spec_id, body, *, cls="", extra_css="", role_img=None, attrs=""):
    """One self-contained specimen fragment: a style block, then the root element. The shell's plate stage names the
    specimen from the manifest's alt (role="img"), so the fragment carries no name of its own."""
    if body.startswith('<div class="oai-panel oai-s-newsprint"'):
        body = '<div class="oai-pad oai-s-newsprint"' + body[len('<div class="oai-panel oai-s-newsprint"'):]
    return curl_html(f'<style>{CSS}{extra_css}</style>\n'
                     f'<div class="oai {cls}" data-oai="{spec_id}"{attrs}>{body}</div>\n')
