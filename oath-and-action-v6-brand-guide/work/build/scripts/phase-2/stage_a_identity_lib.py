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
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                      # oath-and-action-v6-brand-guide/
ID_DIR = ROOT / "work/build/assets/identity"
CL_DIR = ROOT / "work/build/assets/civic-line"
SPEC_DIR = ROOT / "work/build/guide/specimens"
CHAP_DIR = ROOT / "work/build/guide/chapters"

E = html.escape
SURFACES = ("newsprint", "white", "charcoal", "prussian")


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
LOCK = {"display": "lockmark/20261028_Lockmark-Master-V5.svg", 24: "lockmark/20261028_Lockmark-24px-Master.svg",
        16: "lockmark/20261028_Lockmark-16px-Master.svg"}
BADGE = {"display": "badge/20261028_Hinge-Badge-Display-Master.svg", 24: "badge/20261028_Hinge-Badge-24px-Master.svg",
         16: "badge/20261028_Hinge-Badge-16px-Master.svg"}
L2 = {"today": "lockups/20261028_L2-Stacked-Master.svg", "condensed": "lockups/20261028_L2-Stacked-Condensed-Master.svg"}
L3 = {"today": "lockups/20261028_L3-Horizontal-Master.svg", "condensed": "lockups/20261028_L3-Horizontal-Condensed-Master.svg"}
L8 = {"today": "lockups/20261028_L8-Monogram-Master.svg", "condensed": "lockups/20261028_L8-Monogram-Condensed-Master.svg"}
HINGE = {"display": "hinge/20261028_Hinge-Diagram-V2-Display-Master.svg", "compact": "hinge/20261028_Hinge-Diagram-V2-Compact-Master.svg"}
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


def lockmark(size, *, surface="newsprint", mode="color", label="Lockmark", decorative=False):
    key = 16 if size < 24 else (24 if size < 48 else "display")
    return mark(LOCK[key], h=size, surface=surface, mode=mode, label=label, decorative=decorative)


# --------------------------------------------------------------------------------------------- Signal Grid (coded)
# Lattices on whole pixels. 24 px follows the 24 px lockmark master (centers 3.5, 11.5, 19.5). 40 px keeps the same
# margins with a 16 px pitch (3.5, 19.5, 35.5). 80 px is the 40 px drawing at twice size.
LATTICE = {24: (24, (3.5, 11.5, 19.5)), 40: (40, (3.5, 19.5, 35.5))}
POS = {"TL": (0, 0), "TM": (1, 0), "TR": (2, 0), "ML": (0, 1), "C": (1, 1), "MR": (2, 1), "BL": (0, 2), "BM": (1, 2), "BR": (2, 2)}
PILLAR_CORNER = {"Explain": "TL", "Track": "TR", "Connect": "BL", "Act": "BR"}
STAGES = ["Filed", "Referred", "Hearing", "Reported out", "Passed first chamber", "Passed second chamber", "Reconciled",
          "Signed", "In effect"]
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
    """Draw a coded Signal Grid.

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
    a11y = 'aria-hidden="true"' if decorative else f'role="img" aria-label="{E(label or "Signal Grid")}"'
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
def illus(text="Illustrative"):
    return f'<span class="oai-illus">{E(text)}</span>'


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
.oai-illus{display:inline-block;font:600 13px/1.3 var(--oa-font-family-reading);letter-spacing:0;padding:1px 6px;border:1px solid currentColor;border-radius:0;vertical-align:middle;white-space:nowrap}
.oai-scroll{overflow-x:auto;overflow-y:hidden;max-width:100%;padding-bottom:4px}
.oai-scroll:focus-visible{outline:2px solid var(--oa-color-focus-ring-on-newsprint);outline-offset:2px}
.oai-note{font-size:14px;color:var(--oa-color-text-secondary-on-newsprint);max-width:62ch}
.oai-label{font:700 13px/1.4 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase}
.oai-disp{font-family:var(--oa-font-family-display);font-weight:800;letter-spacing:-.03em;line-height:1.05}
.oai-mono{font-variant-numeric:tabular-nums}
.oai table{border-collapse:collapse;font-size:14px;line-height:1.45}
.oai th,.oai td{text-align:left;vertical-align:top;padding:8px 12px 8px 0;border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint)}
.oai th{font-weight:700}
.oai-fail-x{display:none}
"""


def fragment(spec_id, body, *, cls="", extra_css="", role_img=None, attrs=""):
    """One self-contained specimen fragment: a style block, then the root element. The shell's plate stage names the
    specimen from the manifest's alt (role="img"), so the fragment carries no name of its own."""
    if body.startswith('<div class="oai-panel oai-s-newsprint"'):
        body = '<div class="oai-pad oai-s-newsprint"' + body[len('<div class="oai-panel oai-s-newsprint"'):]
    return (f'<style>{CSS}{extra_css}</style>\n'
            f'<div class="oai {cls}" data-oai="{spec_id}"{attrs}>{body}</div>\n')
