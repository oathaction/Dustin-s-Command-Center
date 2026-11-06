"""Assemble the Oath & Action Edition 06 guide page from chapter JSON and specimen fragments.

Usage:
  python3 -I work/build/scripts/phase-2/guide_build.py [--out PATH] [--demo] [--strict] [--quiet]
  python3 -I work/build/scripts/phase-2/guide_build.py --chapters DIR --specimens DIR --out PATH   (fixtures and tests)

Reads, from the repository root (found from this file's place, so the working folder does not matter):
  work/build/guide/chapters/NN-anchor.json        one per chapter, written by the makers (Stage A brief, content contract)
  work/build/guide/chapters/proofs.json           optional: order, groups and captions for the Gate 2 proofs appendix
  work/build/guide/specimens/<id>.html            one self-contained fragment per specimen
  work/build/guide/specimens/manifest-*.json      { id: { chapter, rule, width_px, alt, illustrative, notes, ... } }
  work/build/guide/shell/guide-shell.css, guide-shell.js   the shell's own style and script (engineer)
  work/build/tokens/tokens.css (inlined) and tokens.json (token names and values), when they exist;
  until then a provisional block generated from work/build/tokens/20261021_Token-Schema-Draft.json
  work/build/assets/identity/...                   the wordmark masters and ampersand B for the hinge divider

Writes work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html: one page that stands alone except for Google Fonts.
Any chapter of 01 to 08 without a JSON file gets a placeholder that keeps its anchor and contents entry, so the page
builds with none, some or all chapters. --demo fills those placeholders with the shell's sample rules
(work/build/guide/shell/fixtures/), labeled as a template demonstration.

The build never stops on content problems. It prints each one as a warning and writes them, with counts, to
<out stem>-Build-Report.json beside the page. --strict exits 1 when there is any warning.
"""
import argparse
import base64
import datetime
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GUIDE = ROOT / "work/build/guide"
SHELL = GUIDE / "shell"
TOKENS_CSS = ROOT / "work/build/tokens/tokens.css"
TOKENS_JSON = ROOT / "work/build/tokens/tokens.json"
TOKENS_DRAFT = ROOT / "work/build/tokens/20261021_Token-Schema-Draft.json"
ASSETS = ROOT / "work/build/assets"
WORDMARK_24 = ASSETS / "identity/wordmark/20261028_Wordmark-24px-Master.svg"
WORDMARK_16 = ASSETS / "identity/wordmark/20261028_Wordmark-16px-Master.svg"
WORDMARK_DISPLAY = ASSETS / "identity/wordmark/20261028_Wordmark-Display-Master.svg"
AMP_B_24 = ASSETS / "identity/ampersand/20261028_Amp-B-24px-Master.svg"
DEFAULT_OUT = ROOT / "work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html"
EDITION_DATE = "November 6, 2026"

e = html.escape

# ---------------------------------------------------------------------------------------------------------------
# The contents. Chapter list, parts and instruction lines as in work/ledger/20261021_Guide-Architecture-Map.md,
# section 2, and work/build/scripts/phase-1/build_navigation_wireframe.py (the Gate 1 wireframe). A chapter JSON's
# own title and instruction line win over these for the chapters it covers.
# ---------------------------------------------------------------------------------------------------------------
PARTS = [
    ("foundations", "Foundations", "The identity, its voice, color and type, the page grid and the Signal Grid."),
    ("symbols", "Symbols and graphics", "Pillar marks, symbols and icons, and the graphic devices that guide a reader."),
    ("evidence", "Evidence and media", "How a claim carries its source, then charts, systems graphics and imagery."),
    ("behavior", "Behavior", "How the guide and its products respond to readers who use a keyboard, a screen reader, zoom or touch."),
    ("applications", "Applications", "The system at exact sizes, from the website and the atlas to print."),
    ("production", "Production", "Tokens, files and the checklist that ships them."),
]
PART_NAME = {s: n for s, n, _ in PARTS}
PART_ANCHOR_ALIAS = {"applications": "in-use"}

CHAPTERS = [
    ("01", "purpose", "Purpose", "foundations", "Learn what Oath & Action does, and how its pillars and nonpartisan rules shape every piece."),
    ("02", "voice", "Voice", "foundations", "Write the way you'd explain a rule to a neighbor, and quote the brand lines exactly."),
    ("03", "identity", "Identity", "foundations", "Pick the lockup that fits the surface and size, and give it room on every side."),
    ("04", "ampersand", "The Ampersand and the hinge", "foundations", "Use the ampersand once per composition to join a commitment to what it produces."),
    ("05", "color", "Color", "foundations", "Choose a surface first, then the text and graphic colors that pass on it."),
    ("06", "type", "Type", "foundations", "Set every word at a readable size with the three faces and the type scale."),
    ("07", "layout", "Layout and spacing", "foundations", "Build each page on the column grid and spacing scale, readable at every width."),
    ("08", "signal-grid", "The Signal Grid", "foundations", "Keep the lockmark to its fixed places, and put a key beside every Signal Grid that codes content."),
    ("09", "pillar-marks", "Pillar marks", "symbols", "Mark which pillar a piece serves, always in the order Explain, Track, Connect, Act."),
    ("10", "symbols", "Topic and atlas symbols", "symbols", "Find the symbol for a subject or an atlas element and set it with its label."),
    ("11", "icons", "Status and utility icons", "symbols", "Give each record state or interface action a glyph and a word that read without color."),
    ("12", "graphic-devices", "Graphic devices and patterns", "symbols", "Add dividers, frames, markers and watermarks only where they help someone read."),
    ("13", "evidence", "Evidence and sourcing", "evidence", "Name the kind of evidence behind each claim, with its source and any label beside it."),
    ("14", "data-visualization", "Data visualization", "evidence", "Start from the reader's question to choose a chart, then title it with the evidence it shows."),
    ("15", "systems-graphics", "Systems graphics", "evidence", "Draw Atlas V7's mechanisms so a reader can follow them one link at a time."),
    ("16", "photography", "Photography, illustration and video", "evidence", "Show public life as it happens, and label every placeholder and generated image."),
    ("17", "motion-and-states", "Motion and states", "behavior", "Keep motion under the reader's control, and give every state visible text."),
    ("18", "components", "Components and interaction", "behavior", "Build controls that work by keyboard and screen reader and announce every change."),
    ("19", "accessibility", "Accessibility", "behavior", "Check a page against WCAG 2.2 AA before you call it finished."),
    ("20", "web", "Web", "applications", "Build each web page from the system, opening on the reader's question."),
    ("21", "atlas", "The atlas", "applications", "Apply the system to the atlas, with typed IDs and evidence a step from every claim."),
    ("22", "newsletter-and-email", "Newsletter and email", "applications", "Build an email that reads well with images off and web fonts unavailable."),
    ("23", "social-and-video", "Social and video", "applications", "Size each post and video frame for its platform, with text clear of the app's buttons."),
    ("24", "reports", "Reports", "applications", "Lay out a report page by page, from the cover to the source notes."),
    ("25", "print", "Print and presentation", "applications", "Proof each slide and printed piece at its real size before it goes out."),
    ("26", "tokens", "Tokens and how to choose them", "production", "Choose a token step by step from its surface, and call it by name."),
    ("27", "assets", "Assets and downloads", "production", "Download the file for your size and surface, and see which chapter governs it."),
    ("28", "standards", "Standards checklist", "production", "Run the checklist before you publish anything."),
]
CHAPTER = {c[0]: c for c in CHAPTERS}
STAGE_A = [c[0] for c in CHAPTERS if c[3] == "foundations"]
OWNER = {"01": "editor", "02": "editor", "03": "identity designer", "04": "identity designer", "08": "identity designer",
         "05": "systems designer", "06": "systems designer", "07": "systems designer"}

# V5 anchors kept as aliases on their new homes (map section 4).
ALIASES = {"signal-grid": "grid", "symbols": "topic-icons", "data-visualization": "data",
           "motion-and-states": "motion", "systems-graphics": "atlas-system"}

# Chapter-level Related chapters, with reasons, from map section 10. A chapter JSON may replace them with
# "related_chapters": [ {"chapter": "06", "reason": "..."} ].
RELATED_DEFAULT = {
    "01": [("02", "The lines that state the purpose."), ("04", "The hinge in full."), ("09", "The pillar marks."), ("21", "The atlas as the purpose at work.")],
    "02": [("01", "What the voice serves."), ("04", "Hinge headlines."), ("13", "Sourcing and the Act label."), ("22", "The voice in email.")],
    "03": [("04", "The ampersand inside the wordmark."), ("05", "The approved surfaces."), ("07", "Clear space on the grid."), ("27", "The logo files.")],
    "04": [("03", "The wordmark the ampersand belongs to."), ("02", "Hinge headlines in copy."), ("12", "The divider index."), ("17", "Hinge motion.")],
    "05": [("06", "Which sizes count as large text."), ("08", "The lever and content-type colors."), ("14", "The data palettes."), ("17", "States."), ("26", "The color tokens.")],
    "06": [("05", "The pairs that pass."), ("07", "Measure and rhythm."), ("19", "Reading size and zoom."), ("22", "The email stack.")],
    "07": [("06", "The type scale the grid carries."), ("08", "The sanctioned positions."), ("20", "Web pages on the grid."), ("25", "Print and slides on the grid.")],
    "08": [("03", "The lockmark beside the wordmark."), ("09", "The pillar marks."), ("14", "The legend mark."), ("17", "Grid states.")],
}

FRONT_CONTENTS = "Jump to any chapter by its part or number."
LOCKED = {
    "tagline": "A country that answers to its people.",
    "pillars": ["Explain", "Track", "Connect", "Act"],
}

RULE_ID = re.compile(r"^(\d{2})\.(\d{1,2})$")


class Report:
    def __init__(self):
        self.warnings = []
        self.notes = []

    def warn(self, where, msg):
        self.warnings.append({"where": where, "message": msg})

    def note(self, msg):
        self.notes.append(msg)


R = Report()


# ---------------------------------------------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------------------------------------------
def kebab(seg):
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", seg).lower()


def css_name(token):
    """oa.color.text.secondary.onNewsprint -> --oa-color-text-secondary-on-newsprint (Token Architecture, section 1)."""
    t = token.strip()
    if t.startswith("--"):
        return t
    if t.startswith("var(") and t.endswith(")"):
        return t[4:-1].split(",")[0].strip()
    return "--" + "-".join(kebab(s) for s in t.split("."))


def flatten_dtcg(node, path, out):
    if isinstance(node, dict):
        if "$value" in node:
            out[".".join(path)] = node
            return
        for k, v in node.items():
            if not k.startswith("$"):
                flatten_dtcg(v, path + [k], out)


def resolve(flat, value, depth=0):
    if isinstance(value, str) and value.startswith("{") and value.endswith("}") and depth < 12:
        ref = flat.get(value[1:-1])
        return resolve(flat, ref["$value"], depth + 1) if ref else None
    return value


def css_value(flat, tok):
    v = resolve(flat, tok["$value"])
    t = tok.get("$type")
    if isinstance(v, dict) and "hex" in v:
        return v["hex"]
    if isinstance(v, dict) and "value" in v and "unit" in v:
        return f"{v['value']:g}{v['unit']}"
    if t == "fontFamily" and isinstance(v, list):
        return ", ".join(f'"{x}"' if " " in x else x for x in v)
    if t == "cubicBezier" and isinstance(v, list):
        return "cubic-bezier(" + ", ".join(f"{x:g}" for x in v) + ")"
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return f"{v:g}"
    if t == "typography" and isinstance(v, dict):
        # shown, not used as CSS: "Inter 400, 1.0625rem/1.6"
        fam = resolve(flat, v.get("fontFamily"))
        fam = fam[0] if isinstance(fam, list) and fam else fam
        wt = resolve(flat, v.get("fontWeight"))
        size = resolve(flat, v.get("fontSize"))
        size = f"{size['value']:g}{size['unit']}" if isinstance(size, dict) and "value" in size else size
        lh = resolve(flat, v.get("lineHeight"))
        return f"{fam} {wt}, {size}/{lh:g}" if isinstance(lh, (int, float)) else f"{fam} {wt}, {size}"
    return None


class Tokens:
    """Token names and display values: tokens.json when it exists, else the Phase 1 schema draft."""

    def __init__(self):
        self.source = None
        self.flat = {}
        src = TOKENS_JSON if TOKENS_JSON.exists() else TOKENS_DRAFT
        if src.exists():
            try:
                flatten_dtcg(json.loads(src.read_text()), [], self.flat)
                self.source = src
            except Exception as ex:  # a half-written file while the token engineer works
                R.warn("tokens", f"could not read {src.relative_to(ROOT)}: {ex}")
        self.by_css = {css_name(k): k for k in self.flat}
        self.css_text = TOKENS_CSS.read_text() if TOKENS_CSS.exists() else None
        self.css_names = set(re.findall(r"(--oa-[a-z0-9-]+)\s*:", self.css_text)) if self.css_text else set()

    @property
    def final(self):
        return self.css_text is not None

    def known(self, token):
        n = css_name(token)
        return n in self.by_css or n in self.css_names

    def value(self, token):
        k = self.by_css.get(css_name(token))
        return css_value(self.flat, self.flat[k]) if k else None

    def stylesheet(self):
        if self.css_text is not None:
            return f"/* work/build/tokens/tokens.css, inlined by guide_build.py */\n{self.css_text}"
        lines = []
        for k, tok in self.flat.items():
            v = css_value(self.flat, tok)
            if v is not None:
                lines.append(f"  {css_name(k)}: {v};")
        R.note("tokens.css not found: the page carries a provisional token block generated from the Phase 1 schema draft")
        return ("/* PROVISIONAL. work/build/tokens/tokens.css does not exist yet, so guide_build.py generated these custom properties\n"
                "   from work/build/tokens/20261021_Token-Schema-Draft.json. They are replaced by tokens.css when it lands. */\n:root {\n"
                + "\n".join(lines) + "\n}\n")


# ---------------------------------------------------------------------------------------------------------------
# Inline text: plain strings with a small allowed set of inline tags. Everything else is escaped.
# ---------------------------------------------------------------------------------------------------------------
ALLOWED_INLINE = re.compile(
    r"&lt;(/?)(em|strong|code|abbr|q|cite|br|sup|sub|span|a)((?:\s+(?:href|title|class|lang)=&quot;[^&]*?&quot;)*)\s*/?&gt;")


def inline(text, ctx=None):
    """Escape a JSON string, keep <em> <strong> <code> <abbr> <q> <cite> <sup> <sub> <br> <span class> <a href>,
    and link each "Rule NN.n" and "chapter NN" mention that the page holds."""
    if text is None:
        return ""
    s = e(str(text), quote=True)

    def keep(m):
        close, tag, attrs = m.group(1), m.group(2), m.group(3) or ""
        attrs = attrs.replace("&quot;", '"')
        if tag == "a" and not close:
            href = re.search(r'href="([^"]*)"', attrs)
            if not href or not (href.group(1).startswith("#") or href.group(1).startswith("https://")):
                return m.group(0)
            if href.group(1).startswith("https://"):
                return f'<a href="{href.group(1)}" rel="noopener">'
            return f'<a class="xref" href="{href.group(1)}">'
        if tag == "span" and not close:
            cls = re.search(r'class="([^"]*)"', attrs)
            return f'<span class="{cls.group(1)}">' if cls else "<span>"
        if tag == "abbr" and not close:
            t = re.search(r'title="([^"]*)"', attrs)
            return f'<abbr title="{t.group(1)}">' if t else "<abbr>"
        if tag == "br":
            return "<br>"
        return f"<{close}{tag}>"

    s = ALLOWED_INLINE.sub(keep, s)
    if ctx is not None:
        s = autolink(s, ctx)
    return s


def autolink(s, ctx):
    """Link "Rule 05.2" to #rule-05-2 and "chapter 06" to #type, outside existing links and tags."""
    parts = re.split(r"(<a\b.*?</a>|<[^>]+>)", s, flags=re.S)
    out = []
    for p in parts:
        if p.startswith("<"):
            out.append(p)
            continue

        def rule_link(m):
            rid = f"rule-{m.group(1)}-{m.group(2)}"
            if rid in ctx["rule_anchors"] and rid != ctx.get("self_rule"):
                return f'<a class="xref" href="#{rid}">{m.group(0)}</a>'
            return m.group(0)

        p = re.sub(r"Rule (\d{2})\.(\d{1,2})\b", rule_link, p)

        def ch_link(m):
            num = m.group(2)
            if num in ctx["present"] and num != ctx.get("self_chapter"):
                return f'<a class="xref" href="#{CHAPTER[num][1]}">{m.group(0)}</a>'
            return m.group(0)

        p = re.sub(r"\b([Cc]hapter) (\d{2})\b", ch_link, p)
        out.append(p)
    return "".join(out)


def paras(items, ctx, cls=None):
    if isinstance(items, str):
        items = [items]
    c = f' class="{cls}"' if cls else ""
    return "".join(f"<p{c}>{inline(t, ctx)}</p>" for t in (items or []) if str(t).strip())


# ---------------------------------------------------------------------------------------------------------------
# SVG and assets
# ---------------------------------------------------------------------------------------------------------------
def svg_inline(path, label=None, cls=None, width=None, height=None, style=None):
    """An identity master as inline SVG. With a label it is an image with that name; without, it is hidden from
    assistive technology. Width and height default to the viewBox, so a pixel-grid master draws at its true size."""
    s = path.read_text()
    s = re.sub(r"<\?xml.*?\?>", "", s)
    s = re.sub(r"<title>.*?</title>", "", s, flags=re.S)
    vb = re.search(r'viewBox="([^"]+)"', s)
    vbw, vbh = (float(x) for x in vb.group(1).split()[2:4]) if vb else (None, None)
    attrs = []
    if label:
        attrs += ['role="img"', f'aria-label="{e(label)}"']
    else:
        attrs += ['aria-hidden="true"']
    attrs.append('focusable="false"')
    if cls:
        attrs.append(f'class="{cls}"')
    if width or height or vbw:
        w = width if width else (round(vbw * (height / vbh), 2) if height else vbw)
        h = height if height else round(vbh * (w / vbw), 2)
        attrs.append(f'width="{w:g}" height="{h:g}"')
    if style:
        attrs.append(f'style="{style}"')
    s = re.sub(r"<svg\b", "<svg " + " ".join(attrs), s, count=1)
    return s.strip()


MIME = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
        ".gif": "image/gif", ".pdf": "application/pdf"}


def data_uri(path):
    mime = MIME.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


# ---------------------------------------------------------------------------------------------------------------
# Specimens
# ---------------------------------------------------------------------------------------------------------------
class Specimens:
    def __init__(self, spec_dir):
        self.dir = spec_dir
        self.manifest = {}
        self.origin = {}
        self.used = {}
        if spec_dir.exists():
            for mf in sorted(spec_dir.glob("manifest-*.json")):
                try:
                    data = json.loads(mf.read_text())
                except Exception as ex:
                    R.warn(mf.name, f"manifest does not parse: {ex}")
                    continue
                for sid, meta in data.items():
                    if sid in self.manifest:
                        R.warn(mf.name, f"specimen {sid} is also listed in {self.origin[sid]}")
                    self.manifest[sid] = meta if isinstance(meta, dict) else {}
                    self.origin[sid] = mf.name
        self.files = {p.stem: p for p in spec_dir.glob("*.html")} if spec_dir.exists() else {}

    def meta(self, sid):
        return self.manifest.get(sid, {})

    def fragment(self, sid, where):
        """The processed fragment, or None when the file is missing."""
        if sid in self.used:
            R.warn(where, f"specimen {sid} is used again (first in {self.used[sid]}); each specimen appears once")
        else:
            self.used[sid] = where
        p = self.files.get(sid)
        if not p:
            R.warn(where, f"specimen file work/build/guide/specimens/{sid}.html is missing")
            return None
        if sid not in self.manifest:
            R.warn(where, f"specimen {sid} has no manifest entry (manifest-<maker>.json), so it has no alt text or width")
        elif not str(self.manifest[sid].get("alt", "")).strip():
            R.warn(where, f"specimen {sid} has no alt in its manifest")
        return process_fragment(p.read_text(), sid, where)


ID_REF_ATTRS = ("aria-labelledby", "aria-describedby", "aria-controls", "aria-owns", "aria-flowto", "aria-details",
                "aria-errormessage", "aria-activedescendant", "for", "headers", "list", "form")


def process_fragment(src, sid, where):
    s = src
    if re.search(r"<body\b", s, re.I):
        R.warn(where, f"{sid}: the file is a whole document; the shell took the inside of its <body>")
        m = re.search(r"<body\b[^>]*>(.*)</body>", s, re.S | re.I)
        heads = re.findall(r"<style\b.*?</style>", re.search(r"<head\b.*?</head>", s, re.S | re.I).group(0), re.S | re.I) if re.search(r"<head\b", s, re.I) else []
        s = "".join(heads) + (m.group(1) if m else "")
    s = re.sub(r"<!doctype[^>]*>", "", s, flags=re.I)
    # heading rule: no h1 to h6 inside a specimen (map section 5)
    hs = re.findall(r"<h[1-6]\b", s, re.I)
    if hs:
        R.warn(where, f"{sid}: {len(hs)} heading element(s) inside the specimen; use styled text (heading rule)")
    if "—" in re.sub(r"<[^>]+>", "", s) and "data-allow-emdash" not in s:
        R.warn(where, f"{sid}: an em dash in the text (DR-79); only W21's labeled specimen may show one, with data-allow-emdash")
    # colors only through var(--oa-...): look for literal colors outside var() fallbacks
    bare = re.sub(r"var\((?:[^()]|\([^()]*\))*\)", "", s)
    bare = re.sub(r'\sd="[^"]*"', "", bare)          # path data
    bare = re.sub(r"data:[^\"')\s]+", "", bare)       # data URIs
    lits = re.findall(r"(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![\w-])|\brgba?\(|\bhsla?\(", bare)
    lits = [x for x in lits if not re.fullmatch(r"#\d{1,2}", x)]
    if lits:
        R.warn(where, f"{sid}: {len(lits)} literal color value(s) ({', '.join(sorted(set(lits))[:4])}); use var(--oa-...) from tokens.css")
    s = inline_assets(s, sid, where)
    s = prefix_ids(s, sid)
    s = scope_styles(s, sid)
    return s.strip()


def inline_assets(s, sid, where):
    """Repository paths in src and href become data URIs; <img data-inline src="...svg"> becomes inline SVG."""

    def img_inline(m):
        tag = m.group(0)
        src = re.search(r'\ssrc="([^"]+)"', tag)
        if not src or not src.group(1).endswith(".svg"):
            return tag
        p = (ROOT / src.group(1)).resolve()
        if not p.exists() or ROOT not in p.parents:
            R.warn(where, f"{sid}: asset {src.group(1)} not found")
            return tag
        alt = re.search(r'\salt="([^"]*)"', tag)
        cls = re.search(r'\sclass="([^"]*)"', tag)
        sty = re.search(r'\sstyle="([^"]*)"', tag)
        w = re.search(r'\swidth="([\d.]+)"', tag)
        h = re.search(r'\sheight="([\d.]+)"', tag)
        svg = svg_inline(p, label=alt.group(1) if alt and alt.group(1) else None, cls=cls.group(1) if cls else None,
                         width=float(w.group(1)) if w else None, height=float(h.group(1)) if h else None,
                         style=sty.group(1) if sty else None)
        dr = re.search(r'\sdata-red="([^"]*)"', tag)
        if dr:
            svg = svg.replace("<svg ", f'<svg data-red="{dr.group(1)}" ', 1)
        return svg

    s = re.sub(r"<img\b[^>]*\sdata-inline\b[^>]*>", img_inline, s)

    def to_uri(m):
        attr, path = m.group(1), m.group(2)
        frag = ""
        if "#" in path:
            path, frag = path.split("#", 1)
            frag = "#" + frag
        p = (ROOT / path).resolve()
        if not p.exists() or ROOT not in p.parents:
            R.warn(where, f"{sid}: asset {path} not found")
            return m.group(0)
        return f'{attr}="{data_uri(p)}{frag}"'

    return re.sub(r'\b(src|href|xlink:href)="((?:work|source|deliverables)/[^"]+)"', to_uri, s)


def prefix_ids(s, sid):
    """Give every id in the fragment the prefix '<specimen id>--' and rewrite the references to it, so ids stay unique
    across the page however many specimens repeat a name."""
    ids = set(re.findall(r'\sid="([^"]+)"', s))
    if not ids:
        return s
    pre = sid + "--"
    s = re.sub(r'(\sid=")([^"]+)(")', lambda m: m.group(1) + pre + m.group(2) + m.group(3), s)

    def refs(m):
        vals = " ".join(pre + v if v in ids else v for v in m.group(2).split())
        return f'{m.group(1)}="{vals}"'

    s = re.sub(r'\b(' + "|".join(re.escape(a) for a in ID_REF_ATTRS) + r')="([^"]*)"', refs, s)
    s = re.sub(r'\b((?:xlink:)?href)="#([^"]+)"', lambda m: f'{m.group(1)}="#{pre + m.group(2) if m.group(2) in ids else m.group(2)}"', s)
    s = re.sub(r"url\(\s*(['\"]?)#([^)'\"]+)\1\s*\)", lambda m: f"url(#{pre + m.group(2) if m.group(2) in ids else m.group(2)})", s)

    def css_ids(block):
        return re.sub(r"#([A-Za-z_][\w-]*)", lambda m: "#" + pre + m.group(1) if m.group(1) in ids else m.group(0), block)

    s = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + css_ids(m.group(2)) + m.group(3), s, flags=re.S)
    s = re.sub(r"""(getElementById\(\s*['"])([^'"]+)(['"])""", lambda m: m.group(1) + (pre + m.group(2) if m.group(2) in ids else m.group(2)) + m.group(3), s)
    return s


def scope_styles(s, sid):
    """A specimen's <style> applies inside its own frame only (CSS @scope)."""
    return re.sub(r"(<style\b[^>]*>)(.*?)(</style>)",
                  lambda m: f'{m.group(1)}@scope ([data-specimen="{sid}"]) {{\n{m.group(2)}\n}}{m.group(3)}', s, flags=re.S)


PLATE_LABEL = {"correct": ("Correct application", "✓"), "failure": ("Failure case", "×"),
               "corrective": ("Corrective example", "→"), "extra": (None, None), "proof": (None, None)}


def plate(kind, spec_id, caption, specs, ctx, where, label=None):
    """One specimen in its frame. The frame, its label, size line and caption belong to the shell; the fragment is the
    maker's. Specimens do not count toward the page's red (D2-102), so the stage carries data-red="specimen"."""
    meta = specs.meta(spec_id) if spec_id else {}
    frag = specs.fragment(spec_id, where) if spec_id else None
    lab, glyph = PLATE_LABEL.get(kind, (None, None))
    lab = label or lab
    width = meta.get("width_px")
    height = meta.get("height_px")
    alt = str(meta.get("alt", "")).strip()
    illustrative = bool(meta.get("illustrative"))
    interactive = bool(meta.get("interactive"))
    exempt = [x for x in (meta.get("check_exempt") or []) if x in ("contrast", "size", "red", "locked")]
    if kind != "failure" and set(exempt) - {"size"}:
        R.warn(where, f"{spec_id}: check_exempt {exempt}: contrast and red exemptions are for failure cases only")
    if "size" in exempt and kind != "failure" and not re.search(r"true size|minimum size|actual size", str(caption or ""), re.I):
        R.warn(where, f"{spec_id}: exempt from the 13 px floor, so its caption must say it shows a mark or a minimum size at true size")
    surface = meta.get("surface")
    head = []
    if lab:
        g = f'<span class="plate-glyph" aria-hidden="true">{glyph}</span>' if glyph else ""
        head.append(f'<p class="plate-label">{g}{e(lab)}</p>')
    size_bits = []
    if width:
        size_bits.append(f"{width:g} px wide" if isinstance(width, (int, float)) else f"{e(str(width))} wide")
    if height and isinstance(height, (int, float)):
        size_bits.append(f"{height:g} px high")
    if size_bits:
        head.append(f'<p class="plate-size">True size, {", ".join(size_bits)}</p>')
    surf = str(surface or "newsprint").lower()
    if surf not in ("newsprint", "white", "charcoal", "prussian"):
        R.warn(where, f"{spec_id}: surface {surface!r} is not newsprint, white, charcoal or prussian")
        surf = "newsprint"
    stage_attrs = [f'class="plate-stage oa-surface-{surf}"', f'data-specimen="{e(spec_id or "pending")}"', 'data-red="specimen"']
    style = []
    if isinstance(width, (int, float)):
        style.append(f"--w:{width:g}px")
    if style:
        stage_attrs.append(f'style="{";".join(style)}"')
    if exempt:
        stage_attrs.append(f'data-check-exempt="{" ".join(exempt)}"')
    stage_attrs.append(f'data-surface="{surf}"')
    alt_html = ""
    if frag is None:
        body = (f'<p class="plate-pending">Specimen <code>{e(spec_id or "(none named)")}</code> is not in '
                f'<code>work/build/guide/specimens/</code> yet.</p>')
        stage_attrs[2] = 'data-red="specimen"'
        stage_attrs.append('data-pending="true"')
    else:
        body = frag
        if interactive:
            aid = f"{spec_id}--alt"
            alt_html = f'<p class="vh" id="{aid}">{e(alt)}</p>' if alt else ""
            stage_attrs.append('role="group"')
            if alt:
                stage_attrs.append(f'aria-describedby="{aid}"')
            if lab:
                stage_attrs.append(f'aria-label="{e(lab)}, interactive specimen"')
        else:
            stage_attrs.append('role="img"')
            stage_attrs.append(f'aria-label="{e(alt) if alt else e(lab or "Specimen")}"')
    cap = ""
    cap_text = inline(caption, ctx) if caption else ""
    if illustrative and not re.search(r"\bIllustrative\b", str(caption or "")):
        cap_text = '<span class="illus">Illustrative</span> ' + cap_text
    if cap_text:
        cap = f'<figcaption class="plate-cap">{cap_text}</figcaption>'
    elif kind in ("correct", "failure", "corrective"):
        R.warn(where, f"{spec_id}: the {kind} specimen has no caption")
    fid = f' id="fig-{e(spec_id)}"' if spec_id else ""
    return (f'<figure class="plate plate--{kind}"{fid}>'
            + (f'<div class="plate-head">{"".join(head)}</div>' if head else "")
            + f'<div class="plate-scroll" data-plate-scroll>{alt_html}<div {" ".join(stage_attrs)}>{body}</div></div>'
            + cap + "</figure>")


# ---------------------------------------------------------------------------------------------------------------
# Template blocks
# ---------------------------------------------------------------------------------------------------------------
def hinge(amp_svg):
    """The hinge divider: a hairline broken by ampersand B in the surface's ink (D1-22, D1-26), set between a rule and
    its correct use (Gate 1 proposal item 4). Decorative, so hidden from assistive technology."""
    return f'<div class="hinge" aria-hidden="true"><span class="hinge-line hinge-line--a"></span>{amp_svg}<span class="hinge-line hinge-line--b"></span></div>'


def token_chip(tok, tokens, where):
    name = css_name(tok)
    if not tokens.known(tok):
        R.warn(where, f"token {tok} is not in {'tokens.json or tokens.css' if tokens.final else 'the token schema draft'}")
    val = tokens.value(tok)
    sw = ""
    if val and re.fullmatch(r"#[0-9A-Fa-f]{6}", val):
        red = ' data-red="swatch"' if val.upper() == "#E63946" else ""
        sw = f'<span class="tok-sw" style="background:var({name})"{red} aria-hidden="true"></span>'
    shown = f'<span class="tok-val">{e(val)}</span>' if val else ""
    return f'<li class="tok"><code class="tok-name">{e(name)}</code>{sw}{shown}</li>'


def basis_tag(basis):
    b = str(basis or "").strip()
    if not b:
        return ""
    cls = "basis basis--judgment" if b.lower().startswith("design judgment") else "basis"
    return f'<p class="{cls}"><span class="basis-k">Basis</span> {e(b)}</p>'


def related_inline(nums, ctx, where):
    items = []
    for n in nums or []:
        n = str(n).zfill(2)
        if n not in CHAPTER:
            R.warn(where, f"related chapter {n} is not a chapter number (01 to 28)")
            continue
        _, cid, cname, _, _ = CHAPTER[n]
        if n in ctx["present"]:
            items.append(f'<li><a class="xref" href="#{cid}"><span class="n">{n}</span> {e(cname)}</a></li>')
        else:
            items.append(f'<li><span class="later"><span class="n">{n}</span> {e(cname)}</span> <span class="later-note">later stage</span></li>')
    return f'<ul class="rel-inline">{"".join(items)}</ul>' if items else ""


def specs_list(specs_rows, tokens, where):
    rows = []
    for s in specs_rows or []:
        if not isinstance(s, dict):
            continue
        tok = s.get("token")
        tok_html = ""
        if tok:
            if not tokens.known(tok):
                R.warn(where, f"spec token {tok} is not in the token file")
            tok_html = f'<dd class="spec-tok"><code>{e(css_name(tok))}</code></dd>'
        rows.append(f'<div class="spec-row"><dt>{inline(s.get("label"))}</dt><dd class="spec-val">{inline(s.get("value"))}</dd>{tok_html}</div>')
    return f'<dl class="spec-list">{"".join(rows)}</dl>' if rows else ""


def files_list(files, where):
    if not files:
        return ""
    items = []
    for f in files:
        p = ROOT / f
        if not p.exists():
            R.warn(where, f"file {f} does not exist in the repository")
        items.append(f"<li><code>{e(f)}</code></li>")
    return f'<p class="label">Files</p><ul class="file-list">{"".join(items)}</ul>'


def as_list(v):
    if v is None:
        return []
    return list(v) if isinstance(v, (list, tuple)) else [v]


def normalize_rule(r):
    """Accept the small slips a hand-written file makes: a bare string where an object or a list belongs."""
    r = dict(r)
    for k in ("correct", "failure", "corrective"):
        if isinstance(r.get(k), str):
            r[k] = {"specimen": r[k]}
    for k in ("tokens", "files", "related", "specs"):
        r[k] = as_list(r.get(k))
    return r


def render_rule(ch_num, r, specs, tokens, ctx, amp_svg, demo=False):
    r = normalize_rule(r)
    rid = str(r.get("id", ""))
    where = f"Rule {rid}"
    m = RULE_ID.match(rid)
    if not m:
        R.warn(f"chapter {ch_num}", f"rule id {rid!r} is not of the form NN.n")
    elif m.group(1) != ch_num:
        R.warn(where, f"rule id {rid} does not start with its chapter number {ch_num}")
    anchor = "rule-" + rid.replace(".", "-")
    ctx = dict(ctx, self_rule=anchor)
    title = str(r.get("title", "")).strip()
    if not title:
        R.warn(where, "the rule has no title")
    for k in ("rule", "why", "correct", "failure"):
        if not r.get(k):
            R.warn(where, f"the rule has no {k!r} block")
    why = r.get("why") or {}
    if isinstance(why, str):
        why = {"text": why}
    out = [f'<div class="rule" id="{anchor}" data-rule="{e(rid)}">']
    demo_tag = '<p class="demo-tag">Template demonstration. Not chapter content.</p>' if demo else ""
    out.append(f'<h3 class="rule-h"><span class="rid"><span class="rid-w">Rule</span> <span class="rid-n">{e(rid)}</span></span> <span class="rt">{inline(title)}</span></h3>')
    out.append('<div class="rule-body">' + demo_tag)
    out.append(paras(r.get("rule"), ctx, "rule-text"))
    if r.get("tokens"):
        out.append('<div class="tokens"><p class="label">Tokens</p><ul class="tok-list">'
                   + "".join(token_chip(t, tokens, where) for t in r["tokens"]) + "</ul></div>")
    if why:
        out.append('<div class="why"><p class="label">Why it works</p>' + basis_tag(why.get("basis")) + paras(why.get("text"), ctx) + "</div>")
        if not why.get("basis"):
            R.warn(where, "why.basis is empty: name the source, or write \"Design judgment\"")
    out.append("</div>")
    out.append(hinge(amp_svg))
    for kind in ("correct", "failure", "corrective"):
        blk = r.get(kind)
        if blk:
            out.append(plate(kind, blk.get("specimen"), blk.get("caption"), specs, ctx, where))
    foot = []
    sl = specs_list(r.get("specs"), tokens, where)
    fl = files_list(r.get("files"), where)
    if sl or fl:
        foot.append(f'<div class="foot-block foot-specs"><p class="label">Specifications</p>{sl}{fl}</div>')
    rel = related_inline(r.get("related"), ctx, where)
    if rel:
        foot.append(f'<div class="foot-block foot-related"><p class="label">Related chapters</p>{rel}</div>')
    if r.get("builders"):
        foot.append(f'<div class="foot-block foot-builders"><p class="label">For builders</p>{paras(r.get("builders"), ctx)}</div>')
    if foot:
        out.append(f'<div class="rule-foot">{"".join(foot)}</div>')
    out.append("</div>")
    return "".join(out), anchor, title


def chapnav(i, order, ctx):
    nums = order
    prev_ = nums[i - 1] if i > 0 else None
    next_ = nums[i + 1] if i < len(nums) - 1 else None
    out = ['<div class="chapnav">']
    if prev_:
        out.append(f'<a href="#{CHAPTER[prev_][1]}" rel="prev"><span class="chapnav-k">Previous</span> <span class="n">{prev_}</span> {e(CHAPTER[prev_][2])}</a>')
    if next_:
        out.append(f'<a href="#{CHAPTER[next_][1]}" rel="next"><span class="chapnav-k">Next</span> <span class="n">{next_}</span> {e(CHAPTER[next_][2])}</a>')
    elif ctx.get("has_proofs"):
        out.append('<a href="#proofs" rel="next"><span class="chapnav-k">Next</span> Proofs for Gate 2</a>')
    out.append('<a class="to-contents" href="#contents">Back to contents</a></div>')
    return "".join(out)


def render_chapter(num, data, specs, tokens, ctx, amp_svg, idx, order, demo=False):
    _, cid, cname, part, line = CHAPTER[num]
    where = f"chapter {num}"
    placeholder = data is None or demo
    if data is not None and not demo:
        if str(data.get("number", "")).zfill(2) != num:
            R.warn(where, f"\"number\" is {data.get('number')!r}, expected \"{num}\"")
        if data.get("anchor") != cid:
            R.warn(where, f"\"anchor\" is {data.get('anchor')!r}; the architecture map fixes it as \"{cid}\"")
        cname = data.get("title") or cname
        line = data.get("instruction") or line
        if not data.get("instruction"):
            R.warn(where, "no instruction line; the map's draft line is shown")
    alias = f'<span id="{ALIASES[cid]}" class="alias" aria-hidden="true"></span>' if cid in ALIASES else ""
    loc = (f'<p class="loc-line"><a href="#part-{part}">{e(PART_NAME[part])}</a> <span aria-hidden="true">·</span> '
           f'Chapter {num} of 28</p>')
    head = (f'<div class="ch-head">{loc}<p class="return" hidden></p>'
            f'<h2 class="ch-title" id="{cid}-h"><span class="n">{num}</span> <span class="t">{e(cname)}</span></h2>'
            f'<p class="instr">{inline(line)}</p>')
    out = [f'<section class="chapter{" chapter--placeholder" if placeholder else ""}" id="{cid}" data-track="chapter" '
           f'data-part="{part}" data-label="{num} {e(cname)}" data-chapter="{num}">{alias}']
    rules = (data or {}).get("rules") or []
    if placeholder:
        out.append(head + "</div>")
        out.append(f'<div class="pending-note"><p class="label">In progress</p><p>The {OWNER.get(num, "maker")} is writing this chapter. '
                   f'Its file will be <code>work/build/guide/chapters/{num}-{cid}.json</code>; until it lands, this placeholder keeps the '
                   f'chapter&#8217;s anchor, number and contents entry.'
                   + (' Below it, the shell&#8217;s sample rules show every template block (<code>--demo</code>).' if demo else '') + '</p></div>')
        if not demo:
            out.append(chapnav(idx, order, ctx) + "</section>")
            return "".join(out)
    else:
        out.append(head + paras(data.get("intro"), dict(ctx, self_chapter=num), "intro") + "</div>")
        if len(data.get("intro") or []) > 2:
            R.warn(where, "intro has more than two paragraphs (content contract: at most two short paragraphs)")
    cctx = dict(ctx, self_chapter=num)
    # local contents: rules, then the three closers
    seen = set()
    rendered = []
    extras = (data or {}).get("extras") or []
    extras_by = {}
    for x in extras:
        if not isinstance(x, dict):
            R.warn(where, f"an extra is not an object: {str(x)[:60]!r}")
            continue
        extras_by.setdefault(str(x.get("after_rule") or ""), []).append(x)
    known_rules = {str(r.get("id")) for r in rules}
    for k in extras_by:
        if k and k not in known_rules:
            R.warn(where, f"an extra sits after rule {k}, which this chapter does not have")
    body = []
    for x in extras_by.get("", []):
        body.append(plate("extra", x.get("specimen"), x.get("caption"), specs, cctx, where, label=x.get("label")))
    toc = []
    all_tokens, all_files, rule_related = [], [], []
    for r in rules:
        if not isinstance(r, dict):
            R.warn(where, f"a rule entry is not an object: {str(r)[:60]!r}")
            continue
        r = normalize_rule(r)
        rid = str(r.get("id"))
        if rid in seen:
            R.warn(where, f"rule id {rid} appears twice")
        seen.add(rid)
        h, anchor, title = render_rule(num, r, specs, tokens, cctx, amp_svg, demo=demo)
        body.append(h)
        toc.append((anchor, f"Rule {rid}", title))
        for x in extras_by.get(rid, []):
            body.append(plate("extra", x.get("specimen"), x.get("caption"), specs, cctx, where, label=x.get("label")))
        for t in r.get("tokens") or []:
            all_tokens.append((t, rid))
        for s in r.get("specs") or []:
            if isinstance(s, dict) and s.get("token"):
                all_tokens.append((s["token"], rid))
        for f in r.get("files") or []:
            all_files.append((f, rid))
        for n in r.get("related") or []:
            rule_related.append((str(n).zfill(2), rid))
    if not placeholder and not rules:
        R.warn(where, "the chapter has no rules")
    # sources
    srcs = (data or {}).get("sources") or []
    if srcs:
        body.append('<div class="sources" id="%s-sources"><p class="label">Sources</p><ol class="src-list">%s</ol></div>'
                    % (cid, "".join(f"<li>{inline(s, cctx)}</li>" for s in srcs)))
    # closers
    closers = []
    # Specifications: one index of every token and file the chapter's rules name
    tok_rows = {}
    for t, rid in all_tokens:
        tok_rows.setdefault(css_name(t), {"tok": t, "rules": []})["rules"].append(rid)
    if tok_rows or all_files:
        rows = []
        for name, d in tok_rows.items():
            val = tokens.value(d["tok"])
            rules_cell = ", ".join(f'<a class="xref" href="#rule-{x.replace(".", "-")}">{x}</a>' for x in dict.fromkeys(d["rules"]))
            rows.append(f'<tr><th scope="row"><code>{e(name)}</code></th><td>{e(val) if val else ""}</td><td>{rules_cell}</td></tr>')
        table = ""
        if rows:
            table = ('<div class="table-wrap" data-plate-scroll><table class="tok-table"><caption>Tokens named in this chapter, with the rules that use them</caption>'
                     '<thead><tr><th scope="col">Token</th><th scope="col">Value</th><th scope="col">Rules</th></tr></thead>'
                     f'<tbody>{"".join(rows)}</tbody></table></div>')
        flist = ""
        if all_files:
            uniq = list(dict.fromkeys(f for f, _ in all_files))
            flist = '<p class="label">Files</p><ul class="file-list">' + "".join(f"<li><code>{e(f)}</code></li>" for f in uniq) + "</ul>"
        closers.append(f'<div class="closer" id="{cid}-specs"><h3>Specifications</h3>{table}{flist}'
                       '<p class="closer-note">Download buttons for these files arrive with the asset package in Phase 5.</p></div>')
        toc.append((f"{cid}-specs", None, "Specifications"))
    # Related chapters: the map's list with reasons, then any further chapter a rule cites
    rel = [(n, reason) for n, reason in ((d.get("chapter"), d.get("reason")) for d in (data or {}).get("related_chapters", []))] \
        if (data or {}).get("related_chapters") else list(RELATED_DEFAULT.get(num, []))
    listed = {str(n).zfill(2) for n, _ in rel}
    for n, rid in rule_related:
        if n not in listed and n != num and n in CHAPTER:
            rel.append((n, f"Cited in Rule {rid}."))
            listed.add(n)
    if rel:
        items = []
        for n, reason in rel:
            n = str(n).zfill(2)
            if n not in CHAPTER:
                R.warn(where, f"related_chapters names {n}, which is not a chapter")
                continue
            _, rcid, rname, _, _ = CHAPTER[n]
            if n in ctx["present"]:
                items.append(f'<li><a class="xref" href="#{rcid}"><span class="n">{n}</span> {e(rname)}</a><span class="rel-why">{inline(reason)}</span></li>')
            else:
                items.append(f'<li><span class="later"><span class="n">{n}</span> {e(rname)}</span><span class="rel-why">{inline(reason)} '
                             f'<span class="later-note">In a later stage.</span></span></li>')
        closers.append(f'<div class="closer" id="{cid}-related"><h3>Related chapters</h3><ul class="related">{"".join(items)}</ul></div>')
        toc.append((f"{cid}-related", None, "Related chapters"))
    # For builders: the chapter's custom properties, ready to copy
    if tok_rows:
        css_lines = []
        for name, d in tok_rows.items():
            val = tokens.value(d["tok"])
            tk = tokens.by_css.get(name)
            is_type = tk and tokens.flat[tk].get("$type") == "typography"
            css_lines.append(f"  /* {name}: {val} */" if is_type else (f"  {name}: {val};" if val else f"  /* {name} */"))
        block = ":root {\n" + "\n".join(css_lines) + "\n}"
        closers.append(f'<div class="closer" id="{cid}-builders"><h3>For builders</h3>'
                       '<p>Every custom property this chapter names, with the value tokens.css gives it. Read the rule&#8217;s own note '
                       'before you pick one: the surface comes first, then the role.</p>'
                       f'<pre class="code" id="{cid}-css" role="region" tabindex="0" aria-label="Custom properties for chapter {num}, scrolls sideways when wide"><code>{e(block)}</code></pre>'
                       f'<p><button type="button" class="btn copy" data-copy-from="{cid}-css">Copy the custom properties</button></p>'
                       f'<p class="status" role="status" id="{cid}-copy-status">Nothing copied yet.</p></div>')
        toc.append((f"{cid}-builders", None, "For builders"))
    if toc:
        items = "".join(
            f'<li><a href="#{a}">' + (f'<span class="toc-rid">{e(lbl)}</span> ' if lbl else "") + f"{inline(t)}</a></li>" for a, lbl, t in toc)
        out.append(f'<div class="local-toc"><p class="local-toc-title" id="{cid}-toc-t">In this chapter</p>'
                   f'<ul aria-labelledby="{cid}-toc-t">{items}</ul></div>')
    out.append('<div class="ch-body">' + "".join(body) + "".join(closers) + "</div>")
    out.append(chapnav(idx, order, ctx) + "</section>")
    return "".join(out)


def contents_section(present, has_proofs):
    out = ['<section class="contents" id="contents" data-track="front" data-label="Contents"><div class="ch-head">',
           '<h2 id="contents-h" class="front-title">Contents</h2>', f'<p class="instr">{e(FRONT_CONTENTS)}</p></div>',
           '<div class="toc-parts">']
    for slug, name, desc in PARTS:
        chs = [c for c in CHAPTERS if c[3] == slug]
        built = any(c[0] in present for c in chs)
        head = f'<a href="#part-{slug}">{e(name)}</a>' if built else e(name)
        status = "" if built else '<span class="later-note">Later stages</span>'
        out.append(f'<div class="toc-part{"" if built else " toc-part--later"}"><h3 class="toc-part-h">{head}</h3>{status}<ol class="toc-list">')
        for num, cid, cname, _, line in chs:
            if num in present:
                out.append(f'<li><a href="#{cid}"><span class="n">{num}</span> <span class="t">{e(cname)}</span></a><p>{e(line)}</p></li>')
            else:
                out.append(f'<li class="toc-later"><span class="toc-name"><span class="n">{num}</span> <span class="t">{e(cname)}</span></span></li>')
        out.append("</ol></div>")
    if has_proofs:
        out.append('<div class="toc-part"><h3 class="toc-part-h"><a href="#proofs">Appendix</a></h3><ol class="toc-list toc-list--plain">'
                   '<li><a href="#proofs"><span class="t">Proofs for Gate 2</span></a><p>The masthead, avatar, social card and letterhead at both wordmark widths, side by side at actual size.</p></li></ol></div>')
    out.append("</div></section>")
    return "".join(out)


def part_section(slug, name, desc, present, ctx):
    alias = f'<span id="{PART_ANCHOR_ALIAS[slug]}" class="alias" aria-hidden="true"></span>' if slug in PART_ANCHOR_ALIAS else ""
    items = []
    for num, cid, cname, cpart, line in CHAPTERS:
        if cpart != slug:
            continue
        if num in present:
            items.append(f'<li><a href="#{cid}"><span class="n">{num}</span> <span class="t">{e(cname)}</span></a><p>{e(ctx["lines"].get(num, line))}</p></li>')
    return (f'<section class="part" id="part-{slug}" data-track="part" data-part="{slug}" data-label="Part: {e(name)}">{alias}'
            f'<div class="part-inner oa-surface-charcoal"><h2 id="part-{slug}-h" class="part-title"><span class="lbl">Part</span> {e(name)}</h2>'
            f'<p class="instr">{e(desc)}</p><ol class="part-list">{"".join(items)}</ol>'
            '<p class="part-note">The pillar mark that marks this part arrives with stage board B (DR-88).</p></div></section>')


def proofs_section(chap_dir, specs, ctx):
    ids = [s for s in specs.manifest if s.startswith("s-proofs-")]
    ids += [s for s in specs.files if s.startswith("s-proofs-") and s not in ids]
    pj = chap_dir / "proofs.json"
    conf = {}
    if pj.exists():
        try:
            conf = json.loads(pj.read_text())
        except Exception as ex:
            R.warn("proofs.json", f"does not parse: {ex}")
    if not ids and not conf:
        return "", False
    out = ['<section class="appendix" id="proofs" data-track="appendix" data-part="appendix" data-label="Proofs for Gate 2">',
           '<div class="ch-head"><p class="loc-line">Appendix <span aria-hidden="true">·</span> After chapter 08</p><p class="return" hidden></p>',
           f'<h2 id="proofs-h" class="ch-title ch-title--appendix">{e(conf.get("title", "Proofs for Gate 2"))}</h2>',
           f'<p class="instr">{inline(conf.get("instruction", "Compare each piece at both wordmark widths, side by side at actual size, before you choose at Gate 2."), ctx)}</p>',
           paras(conf.get("intro"), ctx, "intro"), "</div><div class=\"ch-body\">"]
    groups = conf.get("groups")
    if not groups:
        items = conf.get("items") or [{"specimen": s} for s in ids]
        groups = [{"label": None, "items": items}]
    placed = set()
    for g in groups:
        if g.get("label"):
            gid = "proofs-" + re.sub(r"[^a-z0-9]+", "-", g["label"].lower()).strip("-")
            out.append(f'<div class="proof-group" id="{gid}"><h3 class="proof-h">{inline(g["label"])}</h3>{paras(g.get("text"), ctx)}')
        else:
            out.append('<div class="proof-group">')
        pair = g.get("pair") or len(g.get("items") or []) == 2
        out.append(f'<div class="proof-row{" proof-row--pair" if pair else ""}">')
        for it in g.get("items") or []:
            sid = it.get("specimen")
            placed.add(sid)
            meta = specs.meta(sid)
            cap = it.get("caption") or meta.get("caption") or meta.get("notes")
            out.append(plate("proof", sid, cap, specs, ctx, f"proofs {sid}", label=it.get("label") or meta.get("label")))
        out.append("</div></div>")
    for sid in ids:
        if sid not in placed:
            R.warn("proofs", f"{sid} is in a manifest but not in proofs.json, so it is not shown")
    out.append('<div class="chapnav"><a href="#signal-grid" rel="prev"><span class="chapnav-k">Previous</span> <span class="n">08</span> The Signal Grid</a>'
               '<a class="to-contents" href="#contents">Back to contents</a></div></div></section>')
    return "".join(out), True


# ---------------------------------------------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------------------------------------------
def nav_list(prefix, present, has_proofs, menu=False):
    out = ["<ul>"]
    if menu:
        out.append('<li><a href="#top" data-loc="top">Cover</a></li>')
    out.append('<li><a href="#contents" data-loc="contents">Contents</a></li>')
    for slug, name, _ in PARTS:
        chs = [c for c in CHAPTERS if c[3] == slug and c[0] in present]
        if not chs:
            continue
        out.append(f'<li><a class="{prefix}-partlink" href="#part-{slug}" data-loc="part-{slug}">{e(name)}</a><ul>')
        for num, cid, cname, _, _ in chs:
            out.append(f'<li><a href="#{cid}" data-loc="{cid}"><span class="n">{num}</span> <span class="t">{e(cname)}</span></a></li>')
        out.append("</ul></li>")
    if has_proofs:
        out.append(f'<li><a class="{prefix}-partlink" href="#proofs" data-loc="proofs">Appendix</a><ul>'
                   '<li><a href="#proofs" data-loc="proofs-item"><span class="t">Proofs for Gate 2</span></a></li></ul></li>')
    out.append(f'<li><a class="{prefix}-partlink" href="#colophon" data-loc="colophon">Colophon</a></li>')
    out.append("</ul>")
    return "".join(out)


# ---------------------------------------------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------------------------------------------
def load_chapters(chap_dir):
    found = {}
    if not chap_dir.exists():
        return found
    for p in sorted(chap_dir.glob("[0-9][0-9]-*.json")):
        num = p.name[:2]
        if num not in CHAPTER:
            R.warn(p.name, "the file name does not start with a chapter number from 01 to 28")
            continue
        try:
            data = json.loads(p.read_text())
        except Exception as ex:
            R.warn(p.name, f"does not parse as JSON, so the chapter shows as a placeholder: {ex}")
            continue
        if not isinstance(data, dict):
            R.warn(p.name, "the file is not a JSON object, so the chapter shows as a placeholder")
            continue
        for key in ("rules", "extras", "sources", "intro", "related_chapters"):
            if key in data and not isinstance(data[key], list):
                if key == "intro" and isinstance(data[key], str):
                    data[key] = [data[key]]
                    continue
                R.warn(p.name, f'"{key}" is not a list; it is ignored')
                data[key] = []
        bad = [r for r in data.get("rules", []) if not isinstance(r, dict)]
        if bad:
            R.warn(p.name, (f"{len(bad)} rule entry is not an object; skipped" if len(bad) == 1 else f"{len(bad)} rule entries are not objects; skipped"))
            data["rules"] = [r for r in data["rules"] if isinstance(r, dict)]
        if p.stem != f"{num}-{CHAPTER[num][1]}":
            R.warn(p.name, f"expected the file name {num}-{CHAPTER[num][1]}.json")
        if num in found:
            R.warn(p.name, f"a second file for chapter {num}; the first one wins")
            continue
        found[num] = data
    return found


def build(args):
    chap_dir = Path(args.chapters).resolve() if args.chapters else GUIDE / "chapters"
    spec_dir = Path(args.specimens).resolve() if args.specimens else GUIDE / "specimens"
    out_path = Path(args.out).resolve() if args.out else DEFAULT_OUT
    tokens = Tokens()
    specs = Specimens(spec_dir)
    chapters = load_chapters(chap_dir)
    demo_num, demo_data = None, None
    missing = [n for n in STAGE_A if n not in chapters]
    if args.demo and missing:
        # the shell's sample chapter fills the first missing chapter, renumbered to it
        demo_num = missing[0]
        fx = json.loads((SHELL / "fixtures/demo-chapter.json").read_text())
        remap = lambda rid: demo_num + "." + str(rid).split(".", 1)[1]
        fx["rules"] = [dict(r, id=remap(r["id"])) for r in fx["rules"]]
        fx["extras"] = [dict(x, after_rule=remap(x["after_rule"])) if x.get("after_rule") else x for x in fx.get("extras", [])]
        demo_data = fx
        specs_fx = Specimens(SHELL / "fixtures/specimens")
        for k, v in specs_fx.manifest.items():
            specs.manifest.setdefault(k, v)
        for k, v in specs_fx.files.items():
            specs.files.setdefault(k, v)

    # The page holds chapters 01 to 08 (placeholders where a file is missing) and any later chapter that has a file.
    order = sorted(set(STAGE_A) | set(chapters))
    present = set(order)
    lines = {n: (chapters.get(n) or {}).get("instruction") or CHAPTER[n][4] for n in order}
    names = {n: (chapters.get(n) or {}).get("title") or CHAPTER[n][2] for n in order}
    rule_anchors = set()
    for n, d in list(chapters.items()) + ([(demo_num, demo_data)] if demo_data else []):
        for r in d.get("rules") or []:
            rule_anchors.add("rule-" + str(r.get("id", "")).replace(".", "-"))
    has_proofs_ids = any(s.startswith("s-proofs-") for s in list(specs.manifest) + list(specs.files)) or (chap_dir / "proofs.json").exists()
    ctx = {"present": present, "rule_anchors": rule_anchors, "lines": lines, "has_proofs": has_proofs_ids}

    amp = svg_inline(AMP_B_24, cls="hinge-amp")
    body = []
    for slug, name, desc in PARTS:
        nums = [n for n in order if CHAPTER[n][3] == slug]
        if not nums:
            continue
        body.append(part_section(slug, name, desc, present, ctx))
        for n in nums:
            if n == demo_num:
                body.append(render_chapter(n, demo_data, specs, tokens, ctx, amp, order.index(n), order, demo=True))
            else:
                try:
                    body.append(render_chapter(n, chapters.get(n), specs, tokens, ctx, amp, order.index(n), order))
                except Exception as ex:  # one malformed file must not stop the page
                    R.warn(f"chapter {n}", f"could not render ({type(ex).__name__}: {ex}); shown as a placeholder")
                    body.append(render_chapter(n, None, specs, tokens, ctx, amp, order.index(n), order))
    proofs_html, has_proofs = proofs_section(chap_dir, specs, ctx)
    if not has_proofs:
        ctx["has_proofs"] = False
    for sid in specs.manifest:
        if sid not in specs.used and not sid.startswith("s-proofs-") and not sid.startswith("s-demo-"):
            R.warn(specs.origin.get(sid, "manifest"), f"specimen {sid} is listed but no chapter places it")

    css = (SHELL / "guide-shell.css").read_text()
    js = (SHELL / "guide-shell.js").read_text()
    used_vars = set(re.findall(r"var\((--oa-[a-z0-9-]+)", css))
    tok_css = tokens.stylesheet()
    defined = set(re.findall(r"(--oa-[a-z0-9-]+)\s*:", tok_css))
    missing = sorted(used_vars - defined)
    if missing:
        R.warn("shell", f"the shell uses {len(missing)} custom properties the token stylesheet does not define: {', '.join(missing[:8])}")

    wm24 = svg_inline(WORDMARK_24, label="Oath & Action", cls="wm wm-24")
    wm16 = svg_inline(WORDMARK_16, label="Oath & Action", cls="wm wm-16")
    wm_display = svg_inline(WORDMARK_DISPLAY, label="Oath & Action", cls="cover-wm")
    built = datetime.datetime.now().strftime("%B %-d, %Y at %H:%M")
    n_real = len(chapters)
    n_rules = sum(len(d.get("rules") or []) for d in chapters.values())
    n_specs = len(specs.used)
    stage_line = (f"Stage board A draft, {EDITION_DATE}. Chapters 01 to 08 of the Foundations part"
                  + (", with the proofs for Gate 2." if has_proofs else "."))
    status_line = (f"{n_real} of 8 chapters delivered, {n_rules} rules, {n_specs} specimens placed."
                   + (" Placeholders hold the rest." if n_real < 8 else ""))
    pillars = ' <span class="arr" aria-hidden="true">→</span> '.join(f'<span class="pillar">{p}</span>' for p in LOCKED["pillars"])
    pillars_label = ", ".join(LOCKED["pillars"])

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Oath &amp; Action Brand Guide, Edition 06: Foundations draft</title>
<meta name="description" content="Oath &amp; Action Brand Guide, Edition 06. Stage board A: chapters 01 to 08, the Foundations part, in the first draft of the guide shell.">
<meta name="generator" content="work/build/scripts/phase-2/guide_build.py">
<meta name="guide-build" content="{e(json.dumps({"chapters": sorted(chapters), "placeholders": sorted(set(STAGE_A) - set(chapters)), "tokens": "tokens.css" if tokens.final else "draft", "demo": bool(args.demo)}))}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&amp;family=Inter:wght@400;500;600;700&amp;family=Lora:ital,wght@1,400;1,500&amp;display=swap">
<style id="oa-tokens">
{tok_css}
</style>
<style id="oa-guide-shell">
{css}
</style>
</head>
<body class="oa-surface-newsprint">
<a class="skip" href="#main">Skip to main content</a>
<a class="skip" href="#contents">Skip to contents</a>
<header class="masthead">
  <a class="home" href="#top" data-red="signature">{wm24}{wm16}</a>
  <span class="edition"><span class="edition-k">Brand Guide</span> Edition 06</span>
  <nav class="partnav" aria-label="Parts"><ul>
    <li><a href="#contents" data-part-link="contents">Contents</a></li>
    {"".join(f'<li><a href="#part-{s}" data-part-link="{s}">{e(n)}</a></li>' for s, n, _ in PARTS if any(CHAPTER[x][3] == s for x in order))}
    {'<li><a href="#proofs" data-part-link="appendix">Proofs</a></li>' if has_proofs else ''}
  </ul></nav>
  <p class="where" id="where" aria-hidden="true">Cover</p>
  <button class="menubtn" id="menubtn" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="menu"><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span>Menu</button>
</header>
<div class="frame">
  <nav class="rail" aria-label="Chapters">{nav_list("rail", present, has_proofs)}</nav>
  <main id="main" tabindex="-1" data-view-root="overview">
    <section class="cover" id="top" data-track="front" data-label="Cover">
      <div class="cover-folio"><span>Brand Guide</span><span>Edition 06</span><span>{e(EDITION_DATE)}</span></div>
      <div class="cover-mark" data-red="signature">{wm_display}</div>
      <h1 class="cover-h1">Oath &amp; Action Brand Guide, Edition 06</h1>
      <p class="tagline">{e(LOCKED["tagline"])}</p>
      <p class="pillars" aria-label="The four pillars, in order: {e(pillars_label)}">{pillars}</p>
      <div class="cover-foot">
        <p class="cover-stage">{e(stage_line)}</p>
        <p class="cover-status">{e(status_line)}</p>
        <p class="cover-start"><a href="#contents">Open the contents</a></p>
      </div>
    </section>
    {contents_section(present, has_proofs)}
    {"".join(body)}
    {proofs_html}
  </main>
</div>
<footer class="colophon oa-surface-charcoal" id="colophon">
  <div class="colophon-inner">
    <p class="colophon-k">Colophon</p>
    <dl class="colophon-list">
      <div><dt>Edition</dt><dd>Oath &amp; Action Brand Guide, Edition 06. {e(stage_line)}</dd></div>
      <div><dt>Client</dt><dd>Dustin Cathcart, Founder and Editor, who approves every change.</dd></div>
      <div><dt>Type</dt><dd>Inter Tight for display, Inter for reading and interface, Lora Italic for quoted lines. All three are published under the SIL Open Font License 1.1 and load from Google Fonts in this draft.</dd></div>
      <div><dt>Tokens</dt><dd>{"Every color, size and space on this page comes from <code>work/build/tokens/tokens.css</code>, inlined when the page was built." if tokens.final else "This build carries a provisional token block generated from the Phase 1 schema draft, because <code>work/build/tokens/tokens.css</code> was not there yet."}</dd></div>
      <div><dt>Built</dt><dd>{e(built)}, by <code>work/build/scripts/phase-2/guide_build.py</code> from <code>work/build/guide/</code>. {e(status_line)}</dd></div>
    </dl>
    <p class="colophon-back"><a href="#contents">Back to contents</a></p>
  </div>
</footer>
<dialog class="menu" id="menu" aria-labelledby="menu-h">
  <div class="menu-inner">
    <div class="menu-head"><h2 id="menu-h" class="menu-title">Contents</h2><button type="button" class="menu-close" id="menuclose">Close</button></div>
    <p class="menu-where">You are in <strong id="menu-where-text">Cover</strong>.</p>
    <div class="menu-scroll">
      <nav aria-label="Guide contents">{nav_list("menu", present, has_proofs, menu=True)}</nav>
    </div>
  </div>
</dialog>
<script>
{js}
</script>
</body>
</html>
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page)
    report = {
        "page": str(out_path.relative_to(ROOT)) if ROOT in out_path.parents else str(out_path),
        "built": datetime.datetime.now().isoformat(timespec="seconds"),
        "chapters": sorted(chapters), "placeholders": sorted(set(STAGE_A) - set(chapters)),
        "rules": n_rules, "specimens_placed": n_specs, "tokens": "tokens.css" if tokens.final else "provisional from the schema draft",
        "demo": bool(args.demo), "bytes": len(page.encode()),
        "warnings": R.warnings, "notes": R.notes,
    }
    rep_path = out_path.with_name(out_path.stem + "-Build-Report.json")
    rep_path.write_text(json.dumps(report, indent=1, ensure_ascii=False))
    if not args.quiet:
        rel = report["page"]
        print(f"wrote {rel} ({len(page.encode()):,} bytes): {n_real} chapter file(s), {len(report['placeholders'])} placeholder(s), "
              f"{n_rules} rules, {n_specs} specimens, tokens: {report['tokens']}")
        for w in R.warnings:
            print(f"  warning [{w['where']}] {w['message']}")
        for nt in R.notes:
            print(f"  note: {nt}")
        print(f"  report: {rep_path.relative_to(ROOT) if ROOT in rep_path.parents else rep_path}")
    return 1 if (args.strict and R.warnings) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="output HTML path (default: the Stage A board page)")
    ap.add_argument("--chapters", help="folder of chapter JSON (default work/build/guide/chapters)")
    ap.add_argument("--specimens", help="folder of specimens and manifests (default work/build/guide/specimens)")
    ap.add_argument("--demo", action="store_true", help="fill placeholder chapters with the shell's sample rules")
    ap.add_argument("--strict", action="store_true", help="exit 1 when there is any warning")
    ap.add_argument("--quiet", action="store_true")
    sys.exit(build(ap.parse_args()))


if __name__ == "__main__":
    main()
