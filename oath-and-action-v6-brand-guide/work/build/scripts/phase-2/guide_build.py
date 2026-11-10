"""Assemble the Oath & Action Edition 06 guide page from chapter JSON and specimen fragments.

Usage:
  python3 -I work/build/scripts/phase-2/guide_build.py [--out PATH] [--demo] [--strict] [--quiet]
  python3 -I work/build/scripts/phase-2/guide_build.py --chapters DIR --specimens DIR [--code DIR] --out PATH   (fixtures and tests)
  python3 -I work/build/scripts/phase-2/guide_build.py --sprite-root DIR ...   (the sprite families from fixture folders)

Reads, from the repository root (found from this file's place, so the working folder does not matter):
  work/build/guide/chapters/NN-anchor.json        one per chapter, written by the makers (Stage A brief, content contract);
                                                  chapter 08 is 08-lockmark.json from the apply pass (D2-325)
  work/build/guide/chapters/proofs.json           optional: order, groups and captions for the identity proofs appendix
  work/build/guide/specimens/<id>.html            one self-contained fragment per specimen
  work/build/guide/specimens/manifest-*.json      { id: { chapter, rule, width_px, alt, illustrative, notes, ... } }
  work/build/guide/shell/guide-shell.css, guide-shell.js   the shell's own style and script (engineer)
  work/build/guide/code/c-NN-name.html, .css, .js   code to copy (DR-203): a rule shows a set with "code"; stage C
  work/build/tokens/tokens.css (inlined) and tokens.json (token names and values), when they exist;
  until then a provisional block generated from work/build/tokens/20261021_Token-Schema-Draft.json
  work/build/assets/identity/...                   the wordmark masters and ampersand B for the hinge divider
  work/build/assets/civic-line-v6/black/, pillar-icons/, utility/svg-24/ and svg-16/   the sprite's three families
                                                  (promotion brief); a page draws them by <use href="#oa-sym-...">

Writes work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html: one page that stands alone except for Google Fonts.
Any chapter of 01 to 08 without a JSON file gets a placeholder that keeps its anchor and contents entry, so the page
builds with none, some or all chapters. A later chapter joins the page, under its part opener, once its file exists
(chapter 11 from the apply pass, D2-324); the other chapters of that part show as "Coming later". --demo fills the
placeholders with the shell's sample rules (work/build/guide/shell/fixtures/), labeled as a template demonstration.

Cross-references: every "Rule NN.n" (or "Rules NN.n and NN.m", "Rules NN.n to NN.m", "#rule-NN-n") in reader text,
specimens, captions and alt text must name a rule the page holds when chapter NN is in the page, and no sentence may
still carry one of chapter 08's numbers from before it became The lockmark (D2-325). Each miss is a warning, so
--strict fails until it is fixed. --self-test proves these and the other apply-pass checks on fixtures.

The build never stops on content problems. It prints each one as a warning and writes them, with counts, to
<out stem>-Build-Report.json beside the page. --strict exits 1 when there is any warning.
"""
import argparse
import base64
import datetime
import html
import io
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GUIDE = ROOT / "work/build/guide"
SHELL = GUIDE / "shell"
TOKENS_CSS = ROOT / "work/build/tokens/tokens.css"
TOKENS_JSON = ROOT / "work/build/tokens/tokens.json"
TOKENS_DRAFT = ROOT / "work/build/tokens/20261021_Token-Schema-Draft.json"
# Token families that must each have a reader in the page (D2-402): the marks on the tracker's shapes and the utility icons
READ_FAMILIES = ("--oa-component-mark-", "--oa-component-icon-utility-")
ASSETS = ROOT / "work/build/assets"
WORDMARK_24 = ASSETS / "identity/wordmark/20261028_Wordmark-24px-Master.svg"
WORDMARK_16 = ASSETS / "identity/wordmark/20261028_Wordmark-16px-Master.svg"
WORDMARK_DISPLAY = ASSETS / "identity/wordmark/20261028_Wordmark-Display-Master.svg"
AMP_B_24 = ASSETS / "identity/ampersand/20261028_Amp-B-24px-Master.svg"
DEFAULT_OUT = ROOT / "work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html"
EDITION_DATE = "November 7, 2026"   # the apply pass draft

e = html.escape

# ---------------------------------------------------------------------------------------------------------------
# The contents. Chapter list, parts and instruction lines as in work/ledger/20261021_Guide-Architecture-Map.md,
# section 2, and work/build/scripts/phase-1/build_navigation_wireframe.py (the Gate 1 wireframe). A chapter JSON's
# own title and instruction line win over these for the chapters it covers.
# ---------------------------------------------------------------------------------------------------------------
PARTS = [
    ("foundations", "Foundations", "The identity, its voice, color and type, the page grid and the lockmark."),
    ("symbols", "Symbols and graphics", "Pillar icons, topic symbols, status and utility icons, and the graphic devices that guide a reader."),
    ("evidence", "Evidence and media", "How a claim carries its source, then charts, systems graphics and imagery."),
    ("behavior", "Behavior", "How the guide and its products respond to readers who use a keyboard, a screen reader, zoom or touch."),
    ("applications", "Applications", "The system at exact sizes, from the website and the atlas to print."),
    ("production", "Production", "Tokens, files and the checklist that ships them."),
]
PART_NAME = {s: n for s, n, _ in PARTS}
PART_ANCHOR_ALIAS = {"applications": "in-use"}

CHAPTERS = [
    ("01", "purpose", "Purpose", "foundations", "Learn what Oath & Action does, and how its pillars and nonpartisan rules shape every piece."),
    ("02", "voice", "Voice", "foundations", "Write the way you’d explain a rule to a neighbor, and quote the brand lines exactly."),
    ("03", "identity", "Identity", "foundations", "Pick the lockup that fits the surface and size, and give it room on every side."),
    ("04", "ampersand", "The Ampersand and the hinge", "foundations", "Use the ampersand once per composition to join a commitment to what it produces."),
    ("05", "color", "Color", "foundations", "Choose a surface first, then the text and graphic colors that pass on it."),
    ("06", "type", "Type", "foundations", "Set every word at a readable size with the three faces and the type scale."),
    ("07", "layout", "Layout and spacing", "foundations", "Build each page on the column grid and spacing scale, readable at every width."),
    # D2-325, D2-326: chapter 08 is The lockmark, anchor "lockmark"; its instruction line is the identity designer's.
    ("08", "lockmark", "The lockmark", "foundations", "Draw the lockmark from its master, and place it only in its four fixed places."),
    # D2-415: chapter 09 is "Pillar icons", Dustin's term in DR-105 and DR-111. D2-446: its anchor becomes pillar-icons at
    # stage B, with no alias for pillar-marks, since no link to it reached a reader. 10 and 12 keep the map's anchors.
    ("09", "pillar-icons", "Pillar icons", "symbols", "Mark which pillar a piece serves, always in the order Explain, Track, Connect, Act."),
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
         "05": "systems designer", "06": "systems designer", "07": "systems designer", "11": "systems designer"}

# A chapter file under an old name, read with a note while its new file is missing, so other makers keep building
# through a rename; once the new file exists, the old name is a warning. The apply pass used {"08": "signal-grid"}
# while 08-signal-grid.json became 08-lockmark.json (D2-325). That rename landed on November 7, 2026, so the map is
# empty and the build expects 08-lockmark.json: an 08-signal-grid.json is now a warning.
LEGACY_FILE = {}

# V5 anchors kept as aliases on their new homes (map section 4). V5's #grid now lands on The lockmark (D2-325).
ALIASES = {"lockmark": "grid", "symbols": "topic-icons", "data-visualization": "data",
           "motion-and-states": "motion", "systems-graphics": "atlas-system"}

# Chapter-level Related chapters, with reasons, from map section 10. A chapter JSON may replace them with
# "related_chapters": [ {"chapter": "06", "reason": "..."} ].
RELATED_DEFAULT = {
    "01": [("02", "The lines that state the purpose."), ("04", "The hinge in full."), ("09", "The pillar icons."), ("21", "The atlas as the purpose at work.")],
    "02": [("01", "What the voice serves."), ("04", "Hinge headlines."), ("13", "Sourcing and the Act label."), ("22", "The voice in email.")],
    "03": [("04", "The ampersand inside the wordmark."), ("05", "The approved surfaces."), ("07", "Clear space on the grid."), ("27", "The logo files.")],
    "04": [("03", "The wordmark the ampersand belongs to."), ("02", "Hinge headlines in copy."), ("12", "The divider index."), ("17", "Hinge motion.")],
    "05": [("06", "Which sizes count as large text."), ("08", "The lockmark and its red lever."), ("14", "The data palettes."), ("17", "States."), ("26", "The color tokens.")],
    "06": [("05", "The pairs that pass."), ("07", "Measure and rhythm."), ("19", "Reading size and zoom."), ("22", "The email stack.")],
    "07": [("06", "The type scale the grid carries."), ("08", "The four fixed places of the lockmark."), ("20", "Web pages on the grid."), ("25", "Print and slides on the grid.")],
    # DR-110: the lockmark keeps four fixed places and codes nothing, so trackers move to chapter 11
    "08": [("03", "The lockups that carry the lockmark."), ("07", "The page header and footer it sits in."), ("11", "Trackers, drawn as numbered steps."), ("14", "The lockmark in a chart’s footer.")],
}

FRONT_CONTENTS = "Jump to any chapter by its part or number."
LOCKED = {
    "tagline": "A country that answers to its people.",
    "pillars": ["Explain", "Track", "Connect", "Act"],
}

RULE_ID = re.compile(r"^(\d{2})\.(\d{1,2})$")

# ---------------------------------------------------------------------------------------------------------------
# Cross-references (apply pass, D2-325). A citation is "Rule 05.2", "Rules 05.3 and 05.5", "Rules 08.4 to 08.8" or a
# link to "#rule-05-2". When chapter NN is in the page, every rule it cites must exist there.
# ---------------------------------------------------------------------------------------------------------------
XREF = re.compile(r"\bRules?(?:\s| )+\d{2}\.\d{1,2}\b(?:\s*(?:,|and|or|to|through)\s*\d{2}\.\d{1,2}\b)*")
XREF_HREF = re.compile(r"#rule-(\d{2})-(\d{1,2})\b")
# Sentences that carried chapter 08's numbers before it became The lockmark, read from commit 3130c5b (the page before
# the apply pass). Each points at a rule that moved, changed or retired, so the build warns while one survives as written.
OLD_08_REFS = [
    "Rule 08.8 sets the grid and icon that may lead a kicker",
    "The composer after Rule 08.9 builds only the combinations",
    "40 px, bottom right, inside the margin (Rule 08.2)",
]
XREF_SKIP_KEYS = {"specimen", "id", "after_rule", "before_rule", "token", "tokens", "files", "number", "anchor", "part",
                  "chapter", "related", "_legacy_file", "notes", "opener", "set"}


def cited_rules(text):
    """Every (chapter, rule) a string cites, with ranges expanded: "Rules 08.4 to 08.6" gives 08.4, 08.5 and 08.6."""
    out = []
    for m in XREF.finditer(text):
        toks = re.findall(r"(\d{2})\.(\d{1,2})|\b(to|through)\b", m.group(0))
        prev, rng = None, False
        for a, b, word in toks:
            if word:
                rng = True
                continue
            cur = (a, int(b))
            if rng and prev and prev[0] == cur[0] and cur[1] > prev[1]:
                out += [(a, k) for k in range(prev[1] + 1, cur[1])]
            out.append(cur)
            prev, rng = cur, False
    out += [(a, int(b)) for a, b in XREF_HREF.findall(text)]
    return out


def reader_text(s):
    """Markup as a reader meets it: styles, scripts and comments gone, tags as spaces, entities decoded, one space."""
    s = re.sub(r"<style\b.*?</style>|<script\b.*?</script>|<!--.*?-->", " ", str(s), flags=re.S | re.I)
    hrefs = " ".join(re.findall(r"#rule-\d{2}-\d{1,2}\b", s))   # links keep their targets, which tags would lose
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip() + (" " + hrefs if hrefs else "")


def json_strings(node, where, out, path=()):
    if isinstance(node, str):
        out.append((where + (" " + ".".join(str(p) for p in path) if path else ""), node))
    elif isinstance(node, list):
        for i, x in enumerate(node):
            rid = x.get("id") if isinstance(x, dict) and isinstance(x.get("id"), str) else None
            json_strings(x, where, out, path + ((f"rule {rid}",) if rid else (i,)))
    elif isinstance(node, dict):
        for k, v in node.items():
            if k not in XREF_SKIP_KEYS:
                json_strings(v, where, out, path + (k,))


def check_cross_refs(chapters, pconf, specs):
    """Warn on a citation of a rule that the page's copy of its chapter does not hold, and on any sentence that still
    carries one of chapter 08's numbers from before the lockmark rename. Reads every reader string: chapter files,
    proofs.json, the placed specimens, and their alt text, captions and labels."""
    texts = []
    for n, d in sorted(chapters.items()):
        json_strings(d, d.get("_legacy_file") or f"{n}-{CHAPTER[n][1]}.json", texts)
    if pconf:
        json_strings(pconf, "proofs.json", texts)
    for sid in specs.used:
        p = specs.files.get(sid)
        if p:
            texts.append((f"specimen {sid}", p.read_text()))
        meta = specs.meta(sid)
        for k in ("alt", "caption", "label"):
            if meta.get(k):
                texts.append((f"{specs.origin.get(sid, 'manifest')} {sid}.{k}", str(meta[k])))
    held = {n: {str(r.get("id")) for r in (d.get("rules") or []) if isinstance(r, dict)} for n, d in chapters.items()}
    renamed = "08" in chapters and not chapters["08"].get("_legacy_file")
    seen = set()
    for where, raw in texts:
        t = reader_text(raw)
        for ch, k in cited_rules(t):
            rid = f"{ch}.{k}"
            if ch in held and rid not in held[ch] and (where, rid) not in seen:
                seen.add((where, rid))
                tail = (" Chapter 08 renumbered from 08.1 when it became The lockmark (D2-325): point the sentence at the rule it now means."
                        if ch == "08" and renamed else "")
                R.warn(where, f"cites Rule {rid}, which chapter {ch} does not hold.{tail}")
        if renamed:
            for fp in OLD_08_REFS:
                if fp in t:
                    R.warn(where, f"still reads \"{fp}\", a chapter 08 number from before The lockmark (D2-325); "
                                  "check which rule it means now and edit the sentence")


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
        # shown, not used as CSS (RP-S5): "Inter Tight 800, 56 to 110 px, line height 0.95, tracking −3%".
        # The CSS, clamp() included, is in the chapter's For builders block.
        fam = resolve(flat, v.get("fontFamily"))
        fam = fam[0] if isinstance(fam, list) and fam else fam
        wt = resolve(flat, v.get("fontWeight"))
        ext = (tok.get("$extensions") or {}).get("org.oathandaction", {})

        def px_of(d):
            return d["value"] * (16 if d.get("unit") == "rem" else 1) if isinstance(d, dict) and "value" in d else None
        hi = px_of(resolve(flat, v.get("fontSize")))
        lo = px_of(ext.get("minFontSize")) or hi
        size = (f"{lo:g} to {hi:g} px" if lo is not None and hi is not None and abs(lo - hi) > 1e-6 else f"{hi:g} px") if hi else "?"
        bits = [f"{fam} {wt}", size]
        lh = resolve(flat, v.get("lineHeight"))
        if isinstance(lh, (int, float)):
            bits.append(f"line height {lh:g}")
        tr = ext.get("trackingEm")
        if isinstance(tr, (int, float)) and tr:
            bits.append(f"tracking {'+' if tr > 0 else '\u2212'}{abs(tr) * 100:g}%")
        return ", ".join(bits)
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
        self.tcss = TokenCSS(self.css_text)
        # tokens.css as a download from the page (RP-M3), with a dated, descriptive file name
        self.download_name = "20261106_Oath-And-Action-Tokens.css"
        self.download_uri = ("data:text/css;charset=utf-8;base64," + base64.b64encode(self.css_text.encode()).decode()) if self.css_text else ""
        # Round 3 (DR-192, D2-964): the published page saves through the host, whose save call refuses a .css name and
        # takes a .zip. The build packs tokens.css alone in a zip, byte for byte, dated as the file name is, so the same
        # tokens give the same bytes on every build; the shell's script hands those bytes to the host on a click.
        self.zip_name = "20261106_Oath-And-Action-Tokens.zip"
        self.zip_b64 = base64.b64encode(self.zip_bytes()).decode() if self.css_text else ""
        # F-10 (stage C): each download's words name the file, its type and its size, measured here
        self.css_words = f"{DL_CSS_WORDS}, CSS, {kb_words(len(self.css_text.encode()))}" if self.css_text else DL_CSS_WORDS
        self.zip_words = f"{DL_ZIP_WORDS}, ZIP, {kb_words(len(self.zip_bytes()))}" if self.css_text else DL_ZIP_WORDS

    def zip_bytes(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            info = zipfile.ZipInfo("tokens.css", date_time=(2026, 11, 6, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            info.create_system = 3
            z.writestr(info, self.css_text.encode(), compresslevel=9)
        return buf.getvalue()

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
CODE_SPAN = re.compile(r"&lt;code&gt;(.*?)&lt;/code&gt;", re.S)


def inline(text, ctx=None):
    """Escape a JSON string, keep <em> <strong> <code> <abbr> <q> <cite> <sup> <sub> <br> <span class> <a href>,
    and link each "Rule NN.n" and "chapter NN" mention that the page holds.

    Entities are decoded once before escaping (RP-M4), so "&amp;" and "&" both print as "&", and "&amp;minus;" prints
    as "&minus;". Inside <code>, everything prints as written, tags included, and nothing is linked."""
    if text is None:
        return ""
    s = e(html.unescape(str(text)), quote=True)
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    s = CODE_SPAN.sub(stash, s)

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
    return re.sub("\x00(\\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)


def plain(text):
    """A plain string for an attribute or a text node: entities decoded once, then escaped once."""
    return e(html.unescape(str(text or "")), quote=True)


def break_code(name, sep="-"):
    """A token name or path that may break only between its segments, never mid-segment (C-S5)."""
    parts = e(str(name)).split(sep)
    return (sep + "<wbr>").join(parts) if len(parts) > 1 else parts[0]


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
    # DR-115, D2-328: today's width carries Edition 06; the condensed drawing leaves every page and its files stay only
    # as a record, so a placed specimen that draws from a condensed master is a warning.
    cond = sorted(set(re.findall(r'(?:work|source|deliverables)/[^"\'\s)]*condensed[^"\'\s)]*', s, re.I)))
    if cond:
        R.warn(where, f"{sid}: draws the condensed wordmark ({', '.join(Path(c).name for c in cond[:3])}); "
                      "it left every page when today's width was kept (DR-115)")

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
        # the attribute is HTML source, so decode it once before svg_inline escapes it (AX-M2)
        svg = svg_inline(p, label=html.unescape(alt.group(1)) if alt and alt.group(1) else None, cls=cls.group(1) if cls else None,
                         width=float(w.group(1)) if w else None, height=float(h.group(1)) if h else None,
                         style=sty.group(1) if sty else None)
        dr = re.search(r'\sdata-red="([^"]*)"', tag)
        if dr:
            svg = svg.replace("<svg ", f'<svg data-red="{dr.group(1)}" ', 1)
        return svg

    s = re.sub(r"<img\b[^>]*\sdata-inline\b[^>]*>", img_inline, s)

    # Stage B: <img data-oa-sheet="600" src="work/...png"> is a contact sheet shown 600 px wide, embedded as an image
    def sheet(m):
        tag = m.group(0)
        w = re.search(r'\sdata-oa-sheet="([\d.]+)"', tag)
        src = re.search(r'\ssrc="((?:work|source|deliverables)/[^"]+\.png)"', tag)
        if not (w and src):
            R.warn(where, f"{sid}: a contact sheet needs data-oa-sheet with its shown width in px and a repository PNG in src")
            return tag
        p = (ROOT / src.group(1)).resolve()
        if not p.exists() or ROOT not in p.parents:
            R.warn(where, f"{sid}: asset {src.group(1)} not found")
            return tag
        return tag.replace(src.group(0), f' src="{sheet_uri(p, float(w.group(1)), where, sid)}"')

    s = re.sub(r'<img\b[^>]*\sdata-oa-sheet="[^"]*"[^>]*>', sheet, s)

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
               "corrective": ("Corrective example", "→"), "extra": (None, None), "proof": (None, None), "opener": (None, None)}
# D2-965, D2-1134 (stage C): a chapter from 09 on may open with one figure under its intro, named by "opener". It fits
# the column at true size: a flowing specimen fits at every width, and a fixed one may be at most 328 px wide, the
# column of a 360 px screen. Chapters 01 to 08 open with words alone.
OPENER_FROM = "09"
OPENER_MAX_PX = 328
EXEMPT_KINDS = ("contrast", "size", "red", "locked", "scale")
SCALE_WORDS = {0.5: "Half size", 0.25: "One quarter size", 0.2: "One fifth size", 0.125: "One eighth size", 0.1: "One tenth size",
               2: "Twice true size"}


def num(n):
    """1440 -> '1,440'; 0.5 -> '0.5'."""
    return f"{n:,g}" if isinstance(n, (int, float)) and not isinstance(n, bool) else str(n)


def scale_words(sc):
    for k, v in SCALE_WORDS.items():
        if abs(sc - k) < 1e-6:
            return v
    if abs(sc - 1 / 3) < 0.002:
        return "One third size"
    return f"{sc * 100:.0f} percent of true size"


def first_words(text, n=8):
    w = re.sub(r"\s+", " ", str(text or "")).strip().split(" ")
    return " ".join(w[:n]).rstrip(",.;:") + ("…" if len(w) > n else "")


def plate(kind, spec_id, caption, specs, ctx, where, label=None, rule_id=None, frame_ctx=None):
    """One specimen in its frame. The frame, its label, size line and caption belong to the shell; the fragment is the
    maker's. Specimens do not count toward the page's red (D2-102), so the stage carries data-red="specimen".

    Manifest keys the shell reads (shell notes, section 0): width_px, height_px, surface, alt, illustrative, readable,
    interactive, scale, fit_switch, check_exempt."""
    meta = specs.meta(spec_id) if spec_id else {}
    frag = specs.fragment(spec_id, where) if spec_id else None
    lab, glyph = PLATE_LABEL.get(kind, (None, None))
    lab = html.unescape(str(label or lab or "")) or None
    width = meta.get("width_px")
    height = meta.get("height_px")
    alt = html.unescape(str(meta.get("alt", ""))).strip()
    illustrative = bool(meta.get("illustrative"))
    interactive = bool(meta.get("interactive"))
    readable = bool(meta.get("readable")) and not interactive
    # CA-N9 and CA-M1 (fix pass): every plate with a fixed width carries the True size / Fit to window switch, hidden
    # until the shell's script finds the stage wider than its frame and finds that fitting keeps every text at 13 px or
    # more. "fit_switch": false leaves it out; "fit_switch": true without a width is still a warning.
    fit = meta.get("fit_switch") is not False and (isinstance(width, (int, float)) or bool(meta.get("fit_switch")))
    sc = meta.get("scale")
    if sc is not None and not (isinstance(sc, (int, float)) and not isinstance(sc, bool) and sc > 0):
        R.warn(where, f"{spec_id}: scale {sc!r} is not a positive number; ignored")
        sc = None
    if sc is not None and abs(sc - 1) < 1e-9:
        sc = None
    exempt = [x for x in as_list(meta.get("check_exempt")) if x in EXEMPT_KINDS]
    unknown = [x for x in as_list(meta.get("check_exempt")) if x not in EXEMPT_KINDS]
    if unknown:
        R.warn(where, f"{spec_id}: check_exempt {unknown} not known; the shell reads {', '.join(EXEMPT_KINDS)}")
    if kind != "failure" and set(exempt) & {"contrast", "red", "locked"}:
        R.warn(where, f"{spec_id}: check_exempt {exempt}: contrast, red and locked exemptions are for failure cases only")
    if "size" in exempt and kind != "failure" and not re.search(r"true size|minimum size|actual size", str(caption or ""), re.I):
        R.warn(where, f"{spec_id}: exempt from the 13 px floor, so its caption must say it shows a mark or a minimum size at true size")
    if "scale" in exempt:
        notes = str(meta.get("notes") or "").strip()
        if not notes:
            R.warn(where, f"{spec_id}: check_exempt \"scale\" needs its reason in notes (D2-254)")
        elif kind != "failure" and not re.search(r"print|points|\bpt\b|historic|record|fifth edition|fourth edition|edition 05|edition 04|V5|V4", notes, re.I):
            R.warn(where, f"{spec_id}: check_exempt \"scale\" is for a labeled failure, a historical record or a print piece; notes give none of these")
    if fit and not isinstance(width, (int, float)):
        R.warn(where, f"{spec_id}: fit_switch needs width_px")
        fit = False
    surface = meta.get("surface")
    rule_bit = f", Rule {rule_id}" if rule_id else (f", {html.unescape(str(frame_ctx))}" if frame_ctx else "")
    frame_name = (lab or first_words(alt, 6) or "Specimen") + rule_bit
    head = []
    if lab:
        g = f'<span class="plate-glyph" aria-hidden="true">{glyph}</span>' if glyph else ""
        # Stage C (D2-1103): the words sit in one span, so the label stays one flex item beside its glyph. Bare words
        # broke into one flex item per ID once D2-975 held IDs whole, which set a .6em gap for a space and kept the
        # label from wrapping at 200 percent text.
        head.append(f'<p class="plate-label">{g}<span class="plate-label-t">{e(lab)}</span></p>')
    size_bits = []
    if width:
        size_bits.append(f"{num(width)} px wide" if isinstance(width, (int, float)) else f"{e(str(width))} wide")
    if height and isinstance(height, (int, float)):
        size_bits.append(f"{num(height)} px high")
    if sc is not None:
        head.append(f'<p class="plate-size">{e(scale_words(sc))}</p>')
    elif size_bits:
        head.append(f'<p class="plate-size" data-true="True size, {", ".join(size_bits)}">True size, {", ".join(size_bits)}</p>')
    if fit:
        head.append('<div class="fit-switch" role="group" aria-label="Size of this specimen" hidden>'
                    '<button type="button" class="fit-btn" data-fit="true" aria-pressed="true">True size</button>'
                    '<button type="button" class="fit-btn" data-fit="fit" aria-pressed="false">Fit to window</button></div>')
    head.append('<p class="plate-hint" hidden>Wider than this column. Scroll the frame sideways to see all of it.</p>')
    surf = str(surface or "newsprint").lower()
    if surf not in ("newsprint", "white", "charcoal", "prussian"):
        R.warn(where, f"{spec_id}: surface {surface!r} is not newsprint, white, charcoal or prussian")
        surf = "newsprint"
    stage_attrs = [f'class="plate-stage oa-surface-{surf}"', f'data-specimen="{e(spec_id or "pending")}"', 'data-red="specimen"']
    if isinstance(width, (int, float)):
        stage_attrs.append(f'style="--w:{width:g}px"')
        stage_attrs.append(f'data-width="{width:g}"')
    if sc is not None:
        stage_attrs.append(f'data-scale="{sc:g}"')
    if exempt:
        stage_attrs.append(f'data-check-exempt="{" ".join(exempt)}"')
    stage_attrs.append(f'data-surface="{surf}"')
    alt_html = ""
    if frag is None:
        body = (f'<p class="plate-pending">Specimen <code>{e(spec_id or "(none named)")}</code> is not in '
                f'<code>work/build/guide/specimens/</code> yet.</p>')
        stage_attrs.append('data-pending="true"')
    else:
        body = frag
        if interactive or readable:
            # D2-255, AX-S2: a group named by the plate, described once by the alt. The alt paragraph is hidden from
            # assistive technology, so it is heard only as the group's description.
            aid = f"{spec_id}--alt"
            alt_html = f'<p class="vh" id="{aid}" aria-hidden="true">{e(alt)}</p>' if alt else ""
            stage_attrs.append('role="group"')
            stage_attrs.append(f'aria-label="{e(frame_name)}, {"interactive specimen" if interactive else "specimen"}"')
            if alt:
                stage_attrs.append(f'aria-describedby="{aid}"')
            stage_attrs.append(f'data-mode="{"interactive" if interactive else "readable"}"')
        else:
            stage_attrs.append('role="img"')
            stage_attrs.append(f'aria-label="{e(alt) if alt else e(lab or "Specimen")}"')
    stage = f'<div {" ".join(stage_attrs)}>{body}</div>'
    if fit:
        stage = f'<div class="plate-fit">{stage}</div>'
    cap = ""
    cap_text = inline(caption, ctx) if caption else ""
    # CD-N1, CA-N11 (fix pass): DR-97 asks for one Illustrative label at the head of a wholly invented piece. When the
    # piece draws the shell's label itself, the caption takes none; the caption carries it only for a piece that shows none.
    piece_has_label = frag is not None and re.search(r'class="[^"]*\billus\b', frag) is not None
    if illustrative and not piece_has_label and not re.search(r"\bIllustrative\b", str(caption or "")):
        cap_text = '<span class="illus">Illustrative</span> ' + cap_text
    if cap_text:
        cap = f'<figcaption class="plate-cap">{cap_text}</figcaption>'
    elif kind in ("correct", "failure", "corrective"):
        R.warn(where, f"{spec_id}: the {kind} specimen has no caption")
    fid = f' id="fig-{e(spec_id)}"' if spec_id else ""
    return (f'<figure class="plate plate--{kind}{" plate--fit" if fit else ""}"{fid}>'
            + f'<div class="plate-head">{"".join(head)}</div>'
            + f'<div class="plate-scroll" data-plate-scroll data-frame-name="{e(frame_name)}"'
            + (f' data-width="{width:g}" style="--w:{width:g}px"' if isinstance(width, (int, float)) else "")
            + f'>{alt_html}{stage}</div>'
            + cap + "</figure>")



# ---------------------------------------------------------------------------------------------------------------
# Code to copy (DR-203, stage C round 0). A rule attaches a code set with "code": "c-NN-name", or
# {"set": "c-NN-name", "name": "Primary button", "caption": "..."}. The set is two or three files in
# work/build/guide/code/: <set>.html (the markup a builder pastes into a page's body), <set>.css (its styles, which read
# only tokens.css) and, only where the component needs one, <set>.js (a plain script, no framework). The build shows the
# set live, built from those same files, in the light theme and in the dark theme (DR-204), then each file in its own
# panel with a Copy button. guide_check.js (codeMatch) pastes the panels' text into a page that holds tokens.css alone and
# fails any pixel that draws differently from the live demo, so the guide cannot show what the copied code does not do.
# ---------------------------------------------------------------------------------------------------------------
CODE_DIR = GUIDE / "code"
CODE_SET_ID = re.compile(r"^c-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
CODE_LANGS = (("html", "HTML", "the HTML"), ("css", "CSS", "the CSS"), ("js", "Script", "the script"))
CODE_COLOR = re.compile(r"(?<![\w&-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b(?![\w-])|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(", re.I)
CODE_NAMED = re.compile(r"\b(?:white|black|red|blue|green|gray|grey|silver|navy|maroon|purple|orange|yellow|pink|brown)\b", re.I)
CODE_TAGS = re.compile(r"<(html|head|body|style|script|link|meta|iframe)\b", re.I)
CODE_ROOTS = re.compile(r"(?:^|[\s>+~,(])(?::root|html|body)(?![\w-])")


def css_rules(css):
    """(selector list, inside @keyframes) for every style rule, at any depth of @media, @supports and @container."""
    text = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, stack, i, start = [], [], 0, 0
    while i < len(text):
        ch = text[i]
        if ch == "{":
            prelude = text[start:i].strip().split(";")[-1].strip()
            stack.append(prelude)
            if not prelude.startswith("@") and not any(x.startswith("@keyframes") for x in stack[:-1]):
                out.append(prelude)
            start = i + 1
        elif ch == "}":
            if stack:
                stack.pop()
            start = i + 1
        elif ch == ";":
            start = i + 1
        i += 1
    return out


def split_selectors(sel):
    parts, depth, cur = [], 0, ""
    for ch in sel:
        depth += {"(": 1, "[": 1, ")": -1, "]": -1}.get(ch, 0)
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    return [x for x in parts + [cur.strip()] if x]


class CodeSets:
    """The code sets a page may show: work/build/guide/code/, plus the shell's fixture sets in a --demo build."""

    def __init__(self, dirs, token_names, shell_css):
        self.files = {}
        for d in dirs:
            if not d.exists():
                continue
            for f in sorted(d.glob("c-*.*")):
                if f.suffix[1:] in ("html", "css", "js"):
                    self.files.setdefault(f.stem, {}).setdefault(f.suffix[1:], f)
        self.token_names = token_names
        self.shell_css = shell_css
        self.used = {}

    def load(self, sid, where):
        if sid in self.used:
            R.warn(where, f"code set {sid} is shown again (first in {self.used[sid]}); each set shows once, and a rule that needs it again links there")
            return None
        self.used[sid] = where
        if not CODE_SET_ID.match(sid or ""):
            R.warn(where, f"code set {sid!r} is not named c-NN-name")
        f = self.files.get(sid) or {}
        if "html" not in f or "css" not in f:
            R.warn(where, f"code set {sid} needs work/build/guide/code/{sid}.html and {sid}.css" + ("" if f else "; neither is there"))
            return None
        parts = {k: v.read_text() for k, v in f.items()}
        self.validate(sid, parts, where)
        return parts

    def validate(self, sid, parts, where):
        h, c, j = parts.get("html", ""), parts.get("css", ""), parts.get("js")
        w = lambda msg: R.warn(where, f"code set {sid}: {msg}")
        # the markup: what a builder pastes into a body, styled only by its own CSS
        tags = sorted({m.lower() for m in CODE_TAGS.findall(h)})
        if tags:
            w(f"the HTML holds <{'>, <'.join(tags)}>; it is the markup for a page's body, and its styles and script are their own files")
        if re.search(r"\sstyle\s*=", h, re.I):
            w("the HTML carries a style attribute; every style goes in the CSS file, where tokens.css reaches it")
        if re.search(r"\son[a-z]+\s*=", h, re.I):
            w("the HTML carries an event handler attribute; behavior goes in the script file")
        classes = {c2 for m in re.finditer(r'\sclass="([^"]*)"', h) for c2 in m.group(1).split()}
        css_sel = " ".join(css_rules(c))
        stray = sorted(x for x in classes | set(re.findall(r"\.(-?[_a-zA-Z][\w-]*)", css_sel)) if not x.startswith("oa-"))
        if stray:
            w(f"class(es) {', '.join(stray[:5])} do not start with oa-; a set's own names start with oa- so no page's styles reach them")
        # the styles: tokens.css only
        bare = re.sub(r"var\((?:[^()]|\([^()]*\))*\)", "", re.sub(r"/\*.*?\*/", "", c, flags=re.S))
        lits = sorted(set(CODE_COLOR.findall(bare))) + sorted({m.group(0).lower() for m in CODE_NAMED.finditer(re.sub(r"[.#\[][^{,]*?(?=[{,])", "", bare))})
        if lits:
            w(f"the CSS sets {len(lits)} literal color(s) ({', '.join(lits[:4])}); read them from tokens.css with var(--oa-...)")
        own = set(re.findall(r"(--[\w-]+)\s*:", c))
        unknown = sorted({n for n in re.findall(r"var\(\s*(--[\w-]+)", c) if n not in self.token_names and n not in own})
        if unknown:
            w(f"the CSS reads {', '.join(unknown[:5])}, which tokens.css does not define")
        for m in re.finditer(r"font(?:-size)?\s*:\s*[^;{}]*?(\d*\.?\d+)(px|rem)\b", c):
            v = float(m.group(1)) * (16 if m.group(2) == "rem" else 1)
            if "font-size" in m.group(0) or re.search(r"/|\b(?:Inter|serif|sans)", m.group(0)):
                if v < 13 - 1e-9:
                    w(f"the CSS sets type at {v:g} px ({m.group(0).strip()[:40]}); 13 px is the floor")
        for sel in css_rules(c):
            for one in split_selectors(sel):
                if not re.search(r"\.oa-[\w-]|\[data-oa-[\w-]", one):
                    w(f"the selector \"{one[:50]}\" names no oa- class or data-oa- attribute, so it would reach the page around the component")
                elif CODE_ROOTS.search(" " + one):
                    w(f"the selector \"{one[:50]}\" styles the page's root or body; tokens.css and the page own those")
        if re.search(r"@scope|:scope\b", c):
            w("the CSS uses @scope or :scope; code to copy uses plain class selectors, which every browser reads alike (F-16)")
        pinned = sorted({n for n in re.findall(r"var\(\s*(--oa-[\w-]+)", c)
                         if re.search(r"-on-(?:newsprint|white|charcoal|prussian)$|^--oa-color-surface-(?:newsprint|white|charcoal|prussian)$|^--oa-color-(?:palette|derived|tint)-", n)})
        if pinned:
            w(f"the CSS reads {', '.join(pinned[:4])}, named for one surface or a palette color; read the role's short name, such as "
              f"--oa-color-text-primary or --oa-color-surface, so a surface class and the dark theme reach it (F-1)")
        css_classes = set(re.findall(r"\.(oa-[\w-]+)", css_sel)) | classes
        shared = sorted(x for x in css_classes if not x.startswith("oa-surface-") and re.search(r"\." + re.escape(x) + r"(?![\w-])", self.shell_css))
        if shared:
            w(f"the guide's shell also styles {', '.join(shared[:5])}, so the guide would draw it differently from a copy")
        if j is not None:
            for pat, why in ((r"\bimport\s*[\w{*('\"]", "an import"), (r"\brequire\s*\(", "require()"), (r"\beval\s*\(", "eval()"),
                             (r"document\.write", "document.write"), (r"getElementById\(\s*['\"]", "an ID written into the script"),
                             (r"</?script", "a script tag")):
                if re.search(pat, j):
                    w(f"the script holds {why}; it is a plain script that finds each copy of its component and reads IDs from attributes")


def code_instance(html_src, sid, theme):
    """The set's markup for one live stage: every id, and every reference to it, takes the stage's prefix, so the two
    stages hold unique ids while the copy panel keeps the builder's own."""
    return prefix_ids(html_src, f"{sid}--{theme}")


def code_plate(rid, block, ctx, where):
    codes = ctx.get("codes")
    if isinstance(block, str):
        block = {"set": block}
    if not isinstance(block, dict) or not block.get("set"):
        R.warn(where, "\"code\" names no set: write \"code\": \"c-NN-name\", or an object with \"set\"")
        return ""
    sid = str(block["set"])
    parts = codes.load(sid, where) if codes else None
    name = html.unescape(str(block.get("name") or "")).strip()
    if not name:
        R.warn(where, f"code set {sid}: \"name\" is empty; the panels, buttons and live stages are named for the component")
        name = sid
    if parts is None:
        return (f'<figure class="plate plate--code" id="code-{e(sid)}"><div class="plate-head"><p class="plate-label"><span class="plate-label-t">Code to copy</span></p></div>'
                f'<p class="plate-pending">Code set <code>{e(sid)}</code> is not in <code>work/build/guide/code/</code> yet.</p></figure>')
    nid = f"code-{sid}-name"
    files = "the HTML, CSS and script" if "js" in parts else "the HTML and CSS"
    alt = html.unescape(str(block.get("alt") or "")).strip() or f"{name}, drawn live from {files} below, as a page that links tokens.css draws it."
    aid = f"code-{sid}-alt"
    stages = []
    for theme, words in (("light", "in the light theme, on Newsprint"), ("dark", "in the dark theme, on Charcoal")):
        stages.append(f'<div class="code-demo-item"><p class="code-demo-k">{e(words[0].upper() + words[1:])}</p>'
                      f'<div class="plate-stage code-stage" data-oa-theme="{theme}" data-specimen="{e(sid)}--{theme}" data-code-set="{e(sid)}" data-code-theme="{theme}" '
                      f'data-red="specimen" data-surface="{"newsprint" if theme == "light" else "charcoal"}" data-mode="interactive" role="group" aria-label="{e(name)}, live, {words}" aria-describedby="{aid}">'
                      f'<div class="code-root">{code_instance(parts["html"], sid, theme)}</div></div></div>')
    panels = []
    for lang, label, what in CODE_LANGS:
        if lang not in parts:
            continue
        pid = f"code-{sid}-{lang}"
        text = parts[lang].strip("\n") + "\n"
        panels.append(f'<div class="code-panel" data-code-lang="{lang}"><div class="code-panel-head"><p class="code-lang" id="{pid}-t">{label}</p>'
                      f'<button type="button" class="btn btn--quiet copy" data-copy-from="{pid}" data-copy-what="{what} of the {e(name[0].lower() + name[1:])}" '
                      f'aria-describedby="{nid}">Copy {what}</button></div>'
                      f'<pre class="code" id="{pid}" data-plate-scroll data-frame-name="{label} of the {e(name[0].lower() + name[1:])}"><code>{e(text)}</code></pre></div>')
    cap = inline(block.get("caption"), ctx) if block.get("caption") else ""
    style = f'<style data-oa-code-css="{e(sid)}">\n{parts["css"]}\n</style>'
    script = f'<script data-oa-code-js="{e(sid)}">\n{parts["js"]}\n</script>' if "js" in parts else ""
    return (f'<figure class="plate plate--code" id="code-{e(sid)}" data-code-set="{e(sid)}">{style}'
            f'<div class="plate-head"><p class="plate-label"><span class="plate-label-t">Code to copy</span></p>'
            f'<p class="plate-size" id="{nid}">{e(name)}</p></div>'
            f'<p class="vh" id="{aid}" aria-hidden="true">{e(alt)}</p><div class="code-demo">{"".join(stages)}</div>'
            f'<div class="code-panels">{"".join(panels)}</div>'
            + status_line(f"code-{sid}-status", cls="status code-status")
            + (f'<figcaption class="plate-cap">{cap}</figcaption>' if cap else "")
            + f'{script}</figure>')


# ---------------------------------------------------------------------------------------------------------------
# Template blocks
# ---------------------------------------------------------------------------------------------------------------
def hinge(amp_svg):
    """The hinge divider (DR-96): ampersand B's 24 px master at 24 px, centered on a 1 px line as wide as the text block
    it divides, with 12 px of clear line on each side of B, in the surface's ink (D1-22, D1-26). It sits between a
    rule and its correct use (Gate 1 proposal item 4). Decorative, so hidden from assistive technology."""
    return f'<div class="hinge" aria-hidden="true"><span class="hinge-line"></span>{amp_svg}<span class="hinge-line"></span></div>'


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
    return f'<li class="tok"><code class="tok-name">{break_code(name)}</code>{sw}{shown}</li>'


def basis_tag(basis):
    b = str(basis or "").strip()
    if not b:
        return ""
    cls = "basis basis--judgment" if b.lower().startswith("design judgment") else "basis"
    return f'<p class="{cls}"><span class="basis-k">Basis</span> {plain(b)}</p>'


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
            items.append(f'<li><span class="later"><span class="n">{n}</span> {e(cname)}</span> <span class="later-note">Coming later</span></li>')
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
            tok_html = f'<dd class="spec-tok"><code>{break_code(css_name(tok))}</code></dd>'
        rows.append(f'<div class="spec-row{" spec-row--tok" if tok else ""}"><dt>{inline(s.get("label"))}</dt><dd class="spec-val">{inline(s.get("value"))}</dd>{tok_html}</div>')
    return f'<dl class="spec-list">{"".join(rows)}</dl>' if rows else ""


def files_list(files, where):
    if not files:
        return ""
    items = []
    for f in files:
        p = ROOT / f
        if not p.exists():
            R.warn(where, f"file {f} does not exist in the repository")
        items.append(f"<li><code>{break_code(f, '/')}</code></li>")
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
    # C-M4: the Rule ID is one line tall, "Rule" hung above the number, so every title sits the same distance above
    # its text whatever its length.
    out.append(f'<h3 class="rule-h"><span class="rid"><span class="rid-w">Rule</span> <span class="rid-n">{e(rid)}</span></span> <span class="rt">{inline(title)}</span></h3>')
    out.append('<p class="return" hidden></p>')
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
            out.append(plate(kind, blk.get("specimen"), blk.get("caption"), specs, ctx, where, rule_id=rid))
    # DR-203: the rule's code to copy, live in both themes, then each file with its Copy button
    if r.get("code"):
        out.append(code_plate(rid, r.get("code"), ctx, where))
    # C-S5: the specifications run across the whole text column as one table, and Related chapters and For builders
    # share one row under it.
    foot = []
    sl = specs_list(r.get("specs"), tokens, where)
    fl = files_list(r.get("files"), where)
    if sl or fl:
        foot.append(f'<div class="foot-block foot-specs"><p class="label">Specifications</p>{sl}{fl}</div>')
    pair = []
    rel = related_inline(r.get("related"), ctx, where)
    if rel:
        pair.append(f'<div class="foot-block foot-related"><p class="label">Related chapters</p>{rel}</div>')
    if r.get("builders"):
        pair.append(f'<div class="foot-block foot-builders"><p class="label">For builders</p>{paras(r.get("builders"), ctx)}</div>')
    if pair:
        foot.append(f'<div class="foot-pair">{"".join(pair)}</div>')
    if foot:
        out.append(f'<div class="rule-foot">{"".join(foot)}</div>')
    out.append("</div>")
    return "".join(out), anchor, title


# D2-328: the proofs appendix is "Identity proofs": today's width in use, and L2 beside S1. proofs.json may set its own
# instruction line; its title must stay this one.
APPENDIX_TITLE = "Identity proofs"
APPENDIX_LINE = "See today’s wordmark in use at actual size, and the new stacked lockup beside the one it replaces."
# The tokens.css button's words on each path (D2-964): the plain file where no host answers, the zip through the host
DL_CSS_WORDS = "Download tokens.css"
DL_ZIP_WORDS = "Download tokens.css in a zip file"


def kb_words(n):
    """A file's size as the download's words give it (F-10): kilobytes of 1,000 bytes, rounded, at least 1."""
    return f"{max(1, round(n / 1000)):,} KB"


def status_line(sid, initial="", cls="status"):
    """A status line for Copy and its kin (F-7, Rules 11.12 and 11.15): the words, after the success mark or the error
    mark, which the shell's script shows with its result. Both marks are 16 px utility drawings, hidden until used."""
    mark = lambda k, name: (f'<svg class="st-mark st-{k}" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false" '
                            f'data-icon="U-{name}" data-icon-family="utility" hidden><use href="#oa-sym-u-{name}-16px"/></svg>')
    return f'<p class="{cls}" role="status" id="{sid}">{mark("ok", "success")}{mark("err", "error")}<span class="st-t">{initial}</span></p>'
FILES_NOTE = "Download buttons arrive with the asset package. Until then, ask the editor for any file listed here."   # D2-252
LATER = "Coming later"   # CP-S3


def chapnav(i, order, ctx):
    nums = order
    prev_ = nums[i - 1] if i > 0 else None
    next_ = nums[i + 1] if i < len(nums) - 1 else None
    out = ['<div class="chapnav">']
    if prev_:
        out.append(f'<a href="#{CHAPTER[prev_][1]}" rel="prev"><span class="chapnav-k">Previous</span> <span class="n">{prev_}</span> {e(ctx["names"].get(prev_, CHAPTER[prev_][2]))}</a>')
    if next_:
        out.append(f'<a href="#{CHAPTER[next_][1]}" rel="next"><span class="chapnav-k">Next</span> <span class="n">{next_}</span> {e(ctx["names"].get(next_, CHAPTER[next_][2]))}</a>')
    elif ctx.get("has_proofs"):
        out.append(f'<a href="#proofs" rel="next"><span class="chapnav-k">Next</span> Appendix: {e(ctx.get("appendix_title", APPENDIX_TITLE))}</a>')
    out.append('<a class="to-contents" href="#contents">Back to contents</a></div>')
    return "".join(out)


TYPE_PARTS = ("font-family", "font-style", "font-weight", "font-size", "line-height", "letter-spacing", "text-transform", "font-variant-numeric")


class TokenCSS:
    """tokens.css read as data, so each chapter's For builders block copies exactly what tokens.css holds (RP-M3)."""

    def __init__(self, text):
        self.text = text or ""
        self.decl = {}
        root = re.search(r":root\s*\{(.*?)\n\}", self.text, re.S)
        if root:
            for m in re.finditer(r"(--oa-[a-z0-9-]+)\s*:\s*([^;]+);", root.group(1)):
                self.decl[m.group(1)] = m.group(2).strip()
        self.surfaces = []
        for m in re.finditer(r"(\.oa-surface-[a-z]+)\s*\{(.*?)\n\}", self.text, re.S):
            body = re.sub(r"/\*.*?\*/", "", m.group(2), flags=re.S)
            self.surfaces.append((m.group(1), [x.strip() for x in body.splitlines() if x.strip()]))
        rm = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{\s*:root\s*\{(.*?)\}", self.text, re.S)
        self.reduced = re.findall(r"(--oa-[a-z0-9-]+)\s*:\s*([^;]+);", rm.group(1)) if rm else []

    def closure(self, names):
        have, todo = set(), list(names)
        while todo:
            n = todo.pop()
            if n in have or n not in self.decl:
                continue
            have.add(n)
            todo += re.findall(r"var\((--oa-[a-z0-9-]+)", self.decl[n])
        return [n for n in self.decl if n in have]   # in tokens.css order

    def block(self, names, num):
        deps = set(names)
        # a type style brings all its parts, tracking and case included, not only the ones its shorthand reads
        for n in names:
            if re.fullmatch(r"--oa-type-[a-z-]+", n) and n in self.decl and "var(" in self.decl[n]:
                deps.update(f"{n}-{part}" for part in TYPE_PARTS if f"{n}-{part}" in self.decl)
        for _, decls in self.surfaces:
            for d in decls:
                deps.update(re.findall(r"var\((--oa-[a-z0-9-]+)", d))
        order = self.closure(deps)
        lines = ["/* tokens.css is the full source of these values: download it from this page and link it before your own styles.",
                 f"   This block copies, as tokens.css holds them, the custom properties chapter {num} names, every property they",
                 "   depend on and the four surface classes, so it also works on its own. Set a page's ground with a surface",
                 "   class, as in <body class=\"oa-surface-newsprint\">, and set type with font: var(--oa-type-body).",
                 "   tokens.css also holds the light and dark themes, which follow the reader's device and data-oa-theme on",
                 "   the root; this block leaves them out. */",
                 ":root {"]
        lines += [f"  {n}: {self.decl[n]};" for n in order] + ["}"]
        for sel, decls in self.surfaces:
            lines += ["", sel + " {"] + ["  " + d for d in decls] + ["}"]
        keep = set(order)
        red = [(n, v.strip()) for n, v in self.reduced if n in keep]
        if red:
            lines += ["", "@media (prefers-reduced-motion: reduce) {", "  :root {"] + [f"    {n}: {v};" for n, v in red] + ["  }", "}"]
        return "\n".join(lines), len(order)


def chapter_groups(data, rules, num, where):
    """Validate the chapter's "groups" (shell notes, section 0). Returns the groups in rule order, keyed by the rule
    each opens, and each rule's group."""
    raw = (data or {}).get("groups")
    if not raw:
        return [], {}
    if not isinstance(raw, list):
        R.warn(where, '"groups" is not a list; it is ignored')
        return [], {}
    ids = [str(r.get("id")) for r in rules if isinstance(r, dict)]
    found = []
    for g in raw:
        if not isinstance(g, dict):
            R.warn(where, f"a group is not an object: {str(g)[:60]!r}")
            continue
        br = str(g.get("before_rule") or "")
        if br not in ids:
            R.warn(where, f"group {g.get('number')!r} opens before rule {br or '(none)'}, which this chapter does not have")
            continue
        if any(str(x["before_rule"]) == br for x in found):
            R.warn(where, f"two groups open before rule {br}; the first wins")
            continue
        if not str(g.get("title") or "").strip():
            R.warn(where, f"group {g.get('number')!r} has no title")
        if not str(g.get("line") or "").strip():
            R.warn(where, f"group {g.get('number')!r} has no line")
        found.append(g)
    found.sort(key=lambda g: ids.index(str(g["before_rule"])))
    if found and str(found[0]["before_rule"]) != ids[0]:
        R.warn(where, f"the first group opens before rule {found[0]['before_rule']}, so the rules ahead of it sit outside any group")
    nums = [g.get("number") for g in found]
    if nums != list(range(1, len(found) + 1)):
        R.warn(where, f"group numbers run {nums}; write 1, 2, 3 in rule order")
    member, cur = {}, None
    starts = {str(g["before_rule"]): g for g in found}
    for rid in ids:
        cur = starts.get(rid, cur)
        member[rid] = cur
    return found, member


def group_id(num, g):
    return f"group-{num}-{g.get('number')}"


def render_chapter(num, data, specs, tokens, ctx, amp_svg, idx, order, demo=False):
    _, cid, cname, part, line = CHAPTER[num]
    where = f"chapter {num}"
    placeholder = data is None or demo
    if data is not None and not demo:
        if str(data.get("number", "")).zfill(2) != num:
            R.warn(where, f"\"number\" is {data.get('number')!r}, expected \"{num}\"")
        if data.get("anchor") != cid and not (data.get("_legacy_file") and data.get("anchor") == LEGACY_FILE.get(num)):
            R.warn(where, f"\"anchor\" is {data.get('anchor')!r}; the architecture map fixes it as \"{cid}\"")
        cname = data.get("title") or cname
        line = data.get("instruction") or line
        if not data.get("instruction"):
            R.warn(where, "no instruction line; the map's draft line is shown")
    alias = f'<span id="{ALIASES[cid]}" class="alias" aria-hidden="true"></span>' if cid in ALIASES else ""
    loc = (f'<p class="loc-line"><a href="#part-{part}">{e(PART_NAME[part])}</a> <span aria-hidden="true">·</span> '
           f'Chapter {num} of 28</p>')
    head = (f'<div class="ch-head">{loc}'
            f'<h2 class="ch-title" id="{cid}-h"><span class="n">{num}</span> <span class="t">{plain(cname)}</span></h2>'
            f'<p class="return" hidden></p><p class="instr">{inline(line)}</p>')
    rules = [r for r in ((data or {}).get("rules") or []) if isinstance(r, dict)]
    groups, member = chapter_groups(data, rules, num, where) if not placeholder else ([], {})
    out = [f'<section class="chapter{" chapter--placeholder" if placeholder else ""}{" chapter--grouped" if groups else ""}" id="{cid}" data-track="chapter" '
           f'data-part="{part}" data-label="{num} {plain(cname)}" data-chapter="{num}">{alias}']
    if placeholder:
        out.append(head + "</div>")
        out.append(f'<div class="pending-note"><p class="label">In progress</p><p>The {OWNER.get(num, "maker")} is writing this chapter. '
                   f'Its file will be <code>work/build/guide/chapters/{num}-{cid}.json</code>; until it lands, this placeholder keeps the '
                   f'chapter&#8217;s anchor, number and contents entry.'
                   + (' Below it, the shell&#8217;s sample rules show every template block (<code>--demo</code>).' if demo else '') + '</p></div>')
        if not demo:
            out.append(chapnav(idx, order, ctx) + "</section>")
            return "".join(out)
        rules = [r for r in ((data or {}).get("rules") or []) if isinstance(r, dict)]
        intro_html = ""
    else:
        intro_html = paras(data.get("intro"), dict(ctx, self_chapter=num), "intro")
        if len(data.get("intro") or []) > 2:
            R.warn(where, "intro has more than two paragraphs (content contract: at most two short paragraphs)")
    cctx = dict(ctx, self_chapter=num)
    # D2-965, D2-1134: the opener figure, under the intro and before the rule index
    opener_html = ""
    op = None if placeholder else (data or {}).get("opener")
    if op is not None:
        sid, cap = (op, None) if isinstance(op, str) else ((op.get("specimen"), op.get("caption")) if isinstance(op, dict) else (None, None))
        if not sid:
            R.warn(where, "\"opener\" names no specimen: write \"opener\": \"s-NN-...\"")
        elif num < OPENER_FROM:
            R.warn(where, f"\"opener\" names {sid}, but chapters 01 to 08 open with words alone (D2-1134)")
        else:
            w = specs.meta(sid).get("width_px")
            if isinstance(w, (int, float)) and w > OPENER_MAX_PX:
                R.warn(where, f"the opener {sid} is {w:g} px wide; an opener fits the column at true size, {OPENER_MAX_PX} px at most on a 360 px screen, or flows with it")
            opener_html = plate("opener", sid, cap, specs, cctx, where, frame_ctx=f"opening figure of chapter {num}")
    seen = set()
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
    starts = {str(g["before_rule"]): g for g in groups}
    for r in rules:
        r = normalize_rule(r)
        rid = str(r.get("id"))
        if rid in seen:
            R.warn(where, f"rule id {rid} appears twice")
        seen.add(rid)
        g = starts.get(rid)
        if g:
            gid = group_id(num, g)
            body.append(f'<div class="rule-group" id="{gid}" data-group="{e(str(g.get("number")))}">'
                        f'<p class="rg-head"><span class="rg-n"><span class="rg-w">Group</span> {e(str(g.get("number")))}</span> '
                        f'<span class="rg-t">{inline(g.get("title"))}</span></p><p class="return" hidden></p>'
                        f'{paras(g.get("line"), cctx, "rg-line")}</div>')
            toc.append((gid, "group", f'{g.get("number")} {g.get("title")}'))
        h, anchor, title = render_rule(num, r, specs, tokens, cctx, amp_svg, demo=demo)
        body.append(h)
        toc.append((anchor, f"Rule {rid}", title))
        for x in extras_by.get(rid, []):
            body.append(plate("extra", x.get("specimen"), x.get("caption"), specs, cctx, where, label=x.get("label")))
        for t in r.get("tokens") or []:
            all_tokens.append((t, rid))
        for sp in r.get("specs") or []:
            if isinstance(sp, dict) and sp.get("token"):
                all_tokens.append((sp["token"], rid))
        for f in r.get("files") or []:
            all_files.append((f, rid))
        for n in r.get("related") or []:
            rule_related.append((str(n).zfill(2), rid))
    if not placeholder and not rules:
        R.warn(where, "the chapter has no rules")
    after = []   # the closers, for the rule index
    # sources
    srcs = (data or {}).get("sources") or []
    if srcs:
        body.append('<div class="sources" id="%s-sources"><p class="label">Sources</p><ol class="src-list">%s</ol></div>'
                    % (cid, "".join(f"<li>{inline(x, cctx)}</li>" for x in srcs)))
        after.append((f"{cid}-sources", "Sources"))
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
            rules_cell = ", ".join(f'<a class="xref" href="#rule-{x.replace(".", "-")}">Rule {x}</a>' for x in dict.fromkeys(d["rules"]))
            rows.append(f'<tr><th scope="row"><code>{break_code(name)}</code></th><td data-k="Value">{e(val) if val else ""}</td>'
                        f'<td data-k="Rules">{rules_cell}</td></tr>')
        table = ""
        if rows:
            table = (f'<div class="table-wrap" data-plate-scroll data-frame-name="Tokens named in chapter {num}"><table class="tok-table"><caption>Tokens named in this chapter, with the rules that use them</caption>'
                     '<thead><tr><th scope="col">Token</th><th scope="col">Value</th><th scope="col">Rules</th></tr></thead>'
                     f'<tbody>{"".join(rows)}</tbody></table></div>')
        flist = ""
        if all_files:
            uniq = list(dict.fromkeys(f for f, _ in all_files))
            flist = ('<p class="label">Files</p><ul class="file-list">' + "".join(f"<li><code>{break_code(f, '/')}</code></li>" for f in uniq) + "</ul>"
                     f'<p class="closer-note">{e(FILES_NOTE)}</p>')
        closers.append(f'<div class="closer" id="{cid}-specs"><h3>Specifications</h3><p class="return" hidden></p>{table}{flist}</div>')
        toc.append((f"{cid}-specs", None, "Specifications"))
        after.append((f"{cid}-specs", "Specifications"))
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
            rname = ctx["names"].get(n, rname)
            if n in ctx["present"]:
                items.append(f'<li><a class="xref" href="#{rcid}"><span class="n">{n}</span> {e(rname)}</a><span class="rel-why">{inline(reason)}</span></li>')
            else:
                items.append(f'<li><span class="later"><span class="n">{n}</span> {e(rname)}</span><span class="rel-why">{inline(reason)} '
                             f'<span class="later-note">{LATER}.</span></span></li>')
        closers.append(f'<div class="closer" id="{cid}-related"><h3>Related chapters</h3><p class="return" hidden></p><ul class="related">{"".join(items)}</ul></div>')
        toc.append((f"{cid}-related", None, "Related chapters"))
        after.append((f"{cid}-related", "Related chapters"))
    # For builders: working CSS for the chapter's custom properties, and tokens.css itself (RP-M3)
    if tok_rows:
        if tokens.final:
            block, n_props = tokens.tcss.block(list(tok_rows), num)
            intro_p = (f"<p>tokens.css is the full source for every token in this guide. Link it before your own styles, or copy "
                       f"this chapter&#8217;s block, which holds the {n_props} custom properties it needs, with the type parts and "
                       f"their clamps, and the four surface classes.</p>")
            # Round 2 (November 10, 2026): the page carries tokens.css as a download once, in the colophon; each chapter's
            # button is a link to it, which the shell's script turns into the download (without script, it lands there)
            dl = f'<a class="btn" href="#tokens-download" data-oa-download="tokens-download">{tokens.css_words}</a>'
        else:
            css_lines = []
            for name, d in tok_rows.items():
                val = tokens.value(d["tok"])
                css_lines.append(f"  {name}: {val};" if val else f"  /* {name} */")
            block = "/* Provisional: tokens.css was not there when this page was built. */\n:root {\n" + "\n".join(css_lines) + "\n}"
            intro_p = "<p>Every custom property this chapter names. tokens.css replaces this block when it lands.</p>"
            dl = ""
        closers.append(f'<div class="closer" id="{cid}-builders"><h3>For builders</h3><p class="return" hidden></p>{intro_p}'
                       f'<p class="btn-row">{dl}<button type="button" class="btn btn--quiet copy" data-copy-from="{cid}-css">Copy this chapter&#8217;s CSS</button></p>'
                       + status_line(f"{cid}-copy-status", "Nothing copied yet.") +
                       f'<pre class="code" id="{cid}-css" data-plate-scroll data-frame-name="CSS for chapter {num}"><code>{e(block)}</code></pre></div>')
        toc.append((f"{cid}-builders", None, "For builders"))
        after.append((f"{cid}-builders", "For builders"))
    # The rule index, after the intro, in a chapter with groups (C-S11, CP-S1)
    index_html = ""
    if groups:
        lis, cur = [], None
        loose = [t for t in toc if t[1] and t[1].startswith("Rule ") and member.get(t[1][5:]) is None]
        if loose:
            lis.append('<li class="ri-group"><ul class="ri-rules">' + "".join(
                f'<li><a href="#{a}"><span class="toc-rid">{e(l[5:])}</span> {inline(t)}</a></li>' for a, l, t in loose) + "</ul></li>")
        for g in groups:
            gid = group_id(num, g)
            mine = [t for t in toc if t[1] and t[1].startswith("Rule ") and member.get(t[1][5:]) is g]
            lis.append(f'<li class="ri-group"><a class="ri-g" href="#{gid}"><span class="rg-n">{e(str(g.get("number")))}</span> '
                       f'<span class="t">{inline(g.get("title"))}</span></a><ul class="ri-rules">'
                       + "".join(f'<li><a href="#{a}"><span class="toc-rid">{e(l[5:])}</span> {inline(t)}</a></li>' for a, l, t in mine)
                       + "</ul></li>")
        tail = ""
        if after:
            tail = ('<p class="ri-after"><span class="ri-after-k">After the rules</span> '
                    + ", ".join(f'<a href="#{a}">{e(t)}</a>' for a, t in after) + "</p>")
        index_html = (f'<div class="rule-index"><p class="label" id="{cid}-index-t">Rules in this chapter, by group</p>'
                      f'<ol class="ri-groups" aria-labelledby="{cid}-index-t">{"".join(lis)}</ol>{tail}</div>')
    if not placeholder:
        out.append(head + intro_html + opener_html + index_html + "</div>")
    if toc:
        items = []
        for a, lbl, t in toc:
            if lbl == "group":
                items.append(f'<li class="toc-group"><a href="#{a}">{inline(t)}</a></li>')
            else:
                items.append(f'<li><a href="#{a}">' + (f'<span class="toc-rid">{e(lbl)}</span> ' if lbl else "") + f"{inline(t)}</a></li>")
        out.append(f'<div class="local-toc"><p class="local-toc-title" id="{cid}-toc-t">In this chapter</p>'
                   f'<ul aria-labelledby="{cid}-toc-t">{"".join(items)}</ul></div>')
    out.append('<div class="ch-body">' + "".join(body) + "".join(closers) + "</div>")
    out.append(chapnav(idx, order, ctx) + "</section>")
    return "".join(out)


def chapter_span(nums):
    """["01", ..., "08", "11"] -> "Chapters 01 to 08 and 11": runs of consecutive chapters as ranges, joined in words."""
    runs = []
    for n in sorted(nums):
        if runs and int(n) == int(runs[-1][-1]) + 1:
            runs[-1].append(n)
        else:
            runs.append([n])
    parts = [f"{r[0]} to {r[-1]}" if len(r) > 2 else (f"{r[0]} and {r[1]}" if len(r) == 2 else r[0]) for r in runs]
    words = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    return ("Chapters " if len(nums) > 1 else "Chapter ") + words


def contents_section(present, has_proofs, ctx):
    out = ['<section class="contents" id="contents" data-track="front" data-label="Contents"><div class="ch-head">',
           '<h2 id="contents-h" class="front-title">Contents</h2><p class="return" hidden></p>', f'<p class="instr">{e(FRONT_CONTENTS)}</p></div>',
           '<div class="toc-parts">']
    for slug, name, desc in PARTS:
        chs = [c for c in CHAPTERS if c[3] == slug]
        built = any(c[0] in present for c in chs)
        # C-S16: a link and plain text take the same box, so the part labels line up
        head = f'<a class="toc-part-k" href="#part-{slug}">{e(name)}</a>' if built else f'<span class="toc-part-k">{e(name)}</span>'
        status = "" if built else f'<span class="later-note">{LATER}</span>'
        out.append(f'<div class="toc-part{"" if built else " toc-part--later"}"><h3 class="toc-part-h">{head}</h3>{status}<ol class="toc-list">')
        for num, cid, cname, _, line in chs:
            if num in present:
                out.append(f'<li><a href="#{cid}"><span class="n">{num}</span> <span class="t">{e(ctx["names"].get(num, cname))}</span></a>'
                           f'<p>{inline(ctx["lines"].get(num, line))}</p></li>')   # C-S9: the chapter file's own line
            else:
                out.append(f'<li class="toc-later"><span class="toc-name"><span class="n">{num}</span> <span class="t">{e(cname)}</span></span></li>')
        out.append("</ol></div>")
    if has_proofs:
        out.append(f'<div class="toc-part"><h3 class="toc-part-h"><a class="toc-part-k" href="#proofs">Appendix</a></h3><ol class="toc-list toc-list--plain">'
                   f'<li><a href="#proofs"><span class="t">{e(ctx.get("appendix_title", APPENDIX_TITLE))}</span></a><p>{inline(ctx.get("appendix_line") or APPENDIX_LINE)}</p></li></ol></div>')
    out.append("</div></section>")
    return "".join(out)


def part_section(slug, name, desc, present, ctx):
    """A part opener lists every chapter of its part: the chapters in the page as links with their instruction lines,
    the rest as text marked "Coming later" (chapters 09, 10 and 12 while chapter 11 opens the Symbols part)."""
    alias = f'<span id="{PART_ANCHOR_ALIAS[slug]}" class="alias" aria-hidden="true"></span>' if slug in PART_ANCHOR_ALIAS else ""
    items = []
    for num, cid, cname, cpart, line in CHAPTERS:
        if cpart != slug:
            continue
        if num in present:
            items.append(f'<li><a href="#{cid}"><span class="n">{num}</span> <span class="t">{e(ctx["names"].get(num, cname))}</span></a>'
                         f'<p>{inline(ctx["lines"].get(num, line))}</p></li>')
        else:
            items.append(f'<li class="part-later"><span class="part-name"><span class="n">{num}</span> <span class="t">{e(cname)}</span></span>'
                         f'<p><span class="later-note">{LATER}</span></p></li>')
    return (f'<section class="part" id="part-{slug}" data-track="part" data-part="{slug}" data-label="Part: {e(name)}">{alias}'
            f'<div class="part-inner oa-surface-charcoal"><h2 id="part-{slug}-h" class="part-title"><span class="lbl">Part</span> {e(name)}</h2>'
            f'<p class="return" hidden></p><p class="instr">{e(desc)}</p><ol class="part-list">{"".join(items)}</ol></div></section>')


def proofs_section(chap_dir, specs, ctx):
    ids = [x for x in specs.manifest if x.startswith("s-proofs-")]
    ids += [x for x in specs.files if x.startswith("s-proofs-") and x not in ids]
    pj = chap_dir / "proofs.json"
    conf = {}
    if pj.exists():
        try:
            conf = json.loads(pj.read_text())
        except Exception as ex:
            R.warn("proofs.json", f"does not parse: {ex}")
    if not ids and not conf:
        return "", False
    title = conf.get("title") or APPENDIX_TITLE
    if html.unescape(str(title)).strip() != APPENDIX_TITLE:
        R.warn("proofs.json", f"the appendix is titled {title!r}; D2-328 names it \"{APPENDIX_TITLE}\"")
    ctx["appendix_title"] = title
    last = ctx["order"][-1]
    out = [f'<section class="appendix" id="proofs" data-track="appendix" data-part="appendix" data-label="Appendix: {plain(title)}">',
           f'<div class="ch-head"><p class="loc-line">Appendix <span aria-hidden="true">·</span> After chapter {last}</p>',
           f'<h2 id="proofs-h" class="ch-title ch-title--appendix">{plain(title)}</h2><p class="return" hidden></p>',
           f'<p class="instr">{inline(conf.get("instruction") or APPENDIX_LINE, ctx)}</p>',
           paras(conf.get("intro"), ctx, "intro"), "</div><div class=\"ch-body\">"]
    groups = conf.get("groups")
    if not groups:
        items = conf.get("items") or [{"specimen": x} for x in ids]
        groups = [{"label": None, "items": items}]
    placed = set()
    for g in groups:
        if g.get("label"):
            gid = "proofs-" + re.sub(r"[^a-z0-9]+", "-", html.unescape(g["label"]).lower()).strip("-")
            out.append(f'<div class="proof-group" id="{gid}"><h3 class="proof-h">{inline(g["label"])}</h3><p class="return" hidden></p>{paras(g.get("text"), ctx)}')
        else:
            out.append('<div class="proof-group">')
        pair = g.get("pair") or len(g.get("items") or []) == 2
        out.append(f'<div class="proof-row{" proof-row--pair" if pair else ""}">')
        for it in g.get("items") or []:
            sid = it.get("specimen")
            placed.add(sid)
            meta = specs.meta(sid)
            cap = it.get("caption") or meta.get("caption") or meta.get("notes")
            out.append(plate("proof", sid, cap, specs, ctx, f"proofs {sid}", label=it.get("label") or meta.get("label"), frame_ctx=g.get("label")))
        out.append("</div></div>")
    for sid in ids:
        if sid not in placed:
            R.warn("proofs", f"{sid} is in a manifest but not in proofs.json, so it is not shown")
    out.append(f'<div class="chapnav"><a href="#{CHAPTER[last][1]}" rel="prev"><span class="chapnav-k">Previous</span> <span class="n">{last}</span> {e(ctx["names"].get(last, CHAPTER[last][2]))}</a>'
               '<a class="to-contents" href="#contents">Back to contents</a></div></div></section>')
    return "".join(out), True


# ---------------------------------------------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------------------------------------------
def nav_list(prefix, present, has_proofs, menu=False, appendix_title=None):
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
                   f'<li><a href="#proofs" data-loc="proofs-item"><span class="t">{e(appendix_title or APPENDIX_TITLE)}</span></a></li></ul></li>')
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
    files = sorted(chap_dir.glob("[0-9][0-9]-*.json"))
    canonical = {p.stem for p in files}
    for p in files:
        num = p.name[:2]
        if num not in CHAPTER:
            R.warn(p.name, "the file name does not start with a chapter number from 01 to 28")
            continue
        legacy = LEGACY_FILE.get(num)
        is_legacy = legacy is not None and p.stem == f"{num}-{legacy}"
        if is_legacy and f"{num}-{CHAPTER[num][1]}" in canonical:
            R.warn(p.name, f"the chapter's old file name; {num}-{CHAPTER[num][1]}.json replaces it and wins, so remove the old file")
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
        if is_legacy:
            # apply pass only: read under the old name and anchor, with a note, until the new file lands
            R.note(f"{p.name} read as chapter {num} under its old name during the apply pass; "
                   f"{num}-{CHAPTER[num][1]}.json replaces it, with the anchor \"{CHAPTER[num][1]}\"")
            data["_legacy_file"] = p.name
        elif p.stem != f"{num}-{CHAPTER[num][1]}":
            R.warn(p.name, f"expected the file name {num}-{CHAPTER[num][1]}.json")
        if num in found:
            R.warn(p.name, f"a second file for chapter {num}; the first one wins")
            continue
        found[num] = data
    return found


# ---------------------------------------------------------------------------------------------------------------
# Page weight (stage B, November 9, 2026): one sprite per icon family, contact sheets as images, a budget per chapter
# ---------------------------------------------------------------------------------------------------------------
# A family's folder holds its final, approved drawings only; a family joins when Dustin approves its drawings by name.
# A specimen draws a drawing as <svg viewBox="0 0 128 128" ...><use href="#oa-sym-cl-019"/></svg>, and the build puts
# the symbols the page references into one hidden sprite per family, once. Two-color use: set --oa-icon-accent on the
# <svg> (signature red); otherwise the accent draws in the ink, currentColor.
# DR-154: share, zoom, print and information stay words, so no family holds a glyph for them.
#
# Promotion (November 10, 2026, the promotion brief): three families, each read from its folder of finals. The symbol id
# comes from the file's root: data-id for Civic Line ("oa-sym-cl-025"); data-id and data-size for a pillar fit
# ("oa-sym-cl-019-24px"); data-icon and data-size for a utility icon ("oa-sym-u-close-24px"). A symbol carries the
# root's own paint and rendering attributes (a utility icon's line, caps and joins; a pillar fit's crisp edges) on a
# group around the drawing, so a <use> draws the file whatever the page's CSS sets on the <svg> around it.
#
# Pixel fits on 1x and 2x screens (DR-179, D2-634): a 24 px pillar icon draws its fit on screens under two device pixels
# per CSS pixel and the master from two up, in one <svg> with two <use>, which the shell switches by class:
#   <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="CL-019"
#        data-icon-family="pillar"><use class="oa-at-1x" href="#oa-sym-cl-019-24px"/><use class="oa-at-2x"
#        href="#oa-sym-cl-019"/></svg>
# A 16 px pillar icon keeps its fit on every screen (one <use> of oa-sym-<id>-16px). Under 48 px a pillar icon is one
# color (R10, D2-497), so it sets no --oa-icon-accent. data-oa-res="fixed" on the <svg> marks a plate that shows one
# drawing on every screen on purpose, such as a fit enlarged to show its pixels.
SPRITE_ROOT = ASSETS          # --sprite-root moves it, for fixture runs while the makers' folders are on their way
SPRITE_FAMILIES = {
    # the 124 drawings in use, black edition (D2-716)
    "civic-line": {"name": "Civic Line", "dirs": ("civic-line-v6/black",), "deep": False, "pick": r"-Black\.svg$",
                   "key": "data-id", "key_re": r"(?:CL|R)-\d+", "sized": False, "ink": "#121212"},
    # the pillar fits in use under 48 px, black edition only (D2-497); the red-black files beside them stay as the record
    "pillar": {"name": "pillar fits", "dirs": ("pillar-icons",), "deep": True, "pick": r"(?<!-Red)-Black\.svg$",
               "key": "data-id", "key_re": r"CL-\d+", "sized": True, "ink": "#121212"},
    # the utility set at its two sizes, drawn in currentColor with no red (DR-134, DR-161)
    "utility": {"name": "utility icons", "dirs": ("utility/svg-24", "utility/svg-16"), "deep": False, "pick": r"\.svg$",
                "key": "data-icon", "key_re": r"U-[a-z0-9]+(?:-[a-z0-9]+)*", "sized": True, "ink": None},
}
# The root attributes a symbol carries onto its drawing: the inherited paint and rendering properties. color stays
# behind, so currentColor follows the page; width, height and the data and aria attributes describe the file.
SPRITE_CARRY = ("fill", "fill-opacity", "fill-rule", "clip-rule", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin",
                "stroke-miterlimit", "stroke-dasharray", "stroke-dashoffset", "stroke-opacity", "shape-rendering", "paint-order",
                "opacity", "style")
# The token that sets a utility icon's line at each size; the 16 px line joins the token file with the first 16 px
# utility icon on a page (D2-577).
UTILITY_LINE = {24: "oa.component.icon.utility.line.medium", 16: "oa.component.icon.utility.line.small"}
PILLAR_FIT = re.compile(r"^oa-sym-((?:cl|r)-\d+)-(16|24)px$")
SPRITE_FROM_CHAPTER = "09"     # from this chapter on, a specimen that inlines a drawing a sprite holds is a warning
SHEET_COLORS = 16              # a contact sheet image is line art: a 16-color palette PNG at twice its shown width
MB = 1_000_000
WEIGHT_LIMIT = 16 * MB         # the artifact's limit
WEIGHT_PAGE = 15.5 * MB        # the page's budget: half a megabyte under the limit
# Budgets per chapter in MB. They sum, with the shell, sprites and appendix, to the page budget across all 26 chapters:
# 01 to 08 and 11 at their stage A and B weight plus room to grow, 10 with its 122 drawings and contact sheets, and
# every later chapter at the default. The main session can move weight between chapters as long as the sum holds.
WEIGHT_BUDGET = {"01": 2.7, "02": 0.85, "03": 0.65, "04": 0.45, "05": 0.45, "06": 0.35, "07": 0.3, "08": 0.3,
                 "09": 0.4, "10": 1.0, "11": 0.55, "12": 0.5}
WEIGHT_DEFAULT = 0.45          # chapters 13 to 26
WEIGHT_FIXED = {"head and shell": 0.2, "sprites": 0.35, "appendix": 0.2, "front matter and part openers": 0.1}


class Sprites:
    """The drawings a page may reference by <use>, read once from each family's folder of finals."""

    def __init__(self):
        self.symbols = {}      # symbol id -> (family, path, label)
        self.prints = {}       # symbol id -> set of path data, to find a drawing a specimen inlines
        self.missing = {}      # family -> its folders that do not exist
        self.placed = []       # the symbol ids the last page referenced and the sprite holds
        for fam, cfg in SPRITE_FAMILIES.items():
            for sub in cfg["dirs"]:
                folder = SPRITE_ROOT / sub
                if not folder.is_dir():
                    self.missing.setdefault(fam, []).append(sub)
                    R.note(f"sprite family {fam}: {self.rel(folder)} does not exist yet")
                    continue
                files = sorted(p for p in (folder.rglob("*.svg") if cfg["deep"] else folder.glob("*.svg")) if re.search(cfg["pick"], p.name))
                n = 0
                for p in files:
                    if self.read(fam, cfg, p):
                        n += 1
                if not n:
                    R.warn(f"sprite {fam}", f"{self.rel(folder)} holds no {cfg['name']} drawing the sprite can read")

    @staticmethod
    def rel(p):
        return p.relative_to(ROOT) if ROOT in p.parents else p

    def read(self, fam, cfg, p):
        t = p.read_text()
        root = re.search(r"<svg\b[^>]*>", t)
        where = f"sprite {fam}"
        key = root and re.search(rf'\s{cfg["key"]}="([^"]+)"', root.group(0))
        if not key:
            R.warn(where, f"{p.name} has no {cfg['key']} on its root, so the sprite cannot name it")
            return False
        key = key.group(1)
        if not re.fullmatch(cfg["key_re"], key):
            R.warn(where, f"{p.name}: {cfg['key']}=\"{key}\" is not a {cfg['name']} id")
            return False
        vb = re.search(r'\sviewBox="([^"]+)"', root.group(0))
        if not vb:
            R.warn(where, f"{p.name} has no viewBox on its root")
            return False
        sid, label = "oa-sym-" + key.lower(), key
        if cfg["sized"]:
            size = re.search(r'\sdata-size="(\d+)"', root.group(0)) or re.search(r"-(\d+)px\b", p.name)
            if not size:
                R.warn(where, f"{p.name} names no size (data-size on its root, or NNpx in its name)")
                return False
            size = int(size.group(1))
            units = float(vb.group(1).split()[2])
            if abs(units - size) > 1e-6:
                R.warn(where, f"{p.name}: drawn on a {units:g}-unit grid but sized {size} px, so its pixels would miss the grid")
            sid, label = f"{sid}-{size}px", f"{key} at {size} px"
        if sid in self.symbols:
            R.warn(where, f"{p.name} is a second drawing for {sid}; the sprite keeps {self.symbols[sid][1].name}")
            return False
        self.symbols[sid] = (fam, p, label)
        ds = set(re.findall(r'\sd="([^"]{20,})"', t))
        if ds:
            self.prints[sid] = ds
        return True

    def family_of(self, sid):
        """The family a symbol id belongs to by its form, for a reference the sprite cannot meet."""
        if sid.startswith("oa-sym-u-"):
            return "utility"
        return "pillar" if PILLAR_FIT.match(sid) else "civic-line"

    def inlined(self, text):
        """Symbols whose drawing a fragment carries inline: half or more of its path data, character for character."""
        return sorted(sid for sid, ds in self.prints.items() if sum(1 for d in ds if d in text) * 2 >= len(ds))

    def use_tag(self, sid):
        """The markup a specimen writes for one symbol at its own size (or 48 px for a Civic Line drawing)."""
        fam, p, _ = self.symbols[sid]
        vb = re.search(r'\sviewBox="([^"]+)"', p.read_text()).group(1)
        px = 48 if fam == "civic-line" else int(re.search(r"-(\d+)px$", sid).group(1))
        return f'<svg viewBox="{vb}" width="{px}" height="{px}"><use href="#{sid}"/></svg>'

    @staticmethod
    def symbol(path, sid, ink):
        t = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
        root = re.search(r"<svg\b[^>]*>", t)
        vb = re.search(r'viewBox="([^"]+)"', root.group(0)).group(1)
        inner = t[root.end():t.rindex("</svg>")]
        inner = re.sub(r"<title>.*?</title>|<desc>.*?</desc>", "", inner, flags=re.S)
        inner = re.sub(r'\sdata-id="[^"]*"', "", inner)
        # the root's paint and rendering attributes go on a group around the drawing, so the symbol draws as the file
        # does: presentation attributes on the group outrank anything the <svg> around a <use> passes down
        carry = [(k, v) for k, v in re.findall(r'\s([a-zA-Z:-]+)="([^"]*)"', root.group(0)) if k in SPRITE_CARRY]
        if carry:
            inner = "<g" + "".join(f' {k}="{v}"' for k, v in carry) + ">" + inner + "</g>"
        # ids nothing points at go; the rest (the masks) take the symbol's id as a prefix, so they stay unique beside a
        # specimen's own copy
        wanted = set(re.findall(r"url\(#([^)]+)\)", inner)) | set(re.findall(r'href="#([^"]+)"', inner))
        inner = re.sub(r'\sid="([^"]+)"', lambda m: m.group(0) if m.group(1) in wanted else "", inner)
        ids = set(re.findall(r'\sid="([^"]+)"', inner))
        inner = re.sub(r'(\sid=")([^"]+)"', lambda m: f'{m.group(1)}{sid}--{m.group(2)}"', inner)
        inner = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{sid}--{m.group(1)})" if m.group(1) in ids else m.group(0), inner)
        inner = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{sid}--{m.group(1)}"' if m.group(1) in ids else m.group(0), inner)
        if ink:
            inner = Sprites.accent(inner, ink)
            inner = inner.replace(f'"{ink}"', '"currentColor"')
        inner = re.sub(r">\s+<", "><", inner).strip()
        return f'<symbol id="{sid}" viewBox="{vb}">{inner}</symbol>'

    @staticmethod
    def accent(inner, ink):
        """Each accent part draws in --oa-icon-accent, and in the ink where a use sets none. The accent is a group
        (Civic Line) or a single shape (a pillar fit's path). The color goes on each element's own declared fill or
        stroke, so a filled part gains no stroke (a drawing may hold several accents)."""
        acc = "var(--oa-icon-accent,currentColor)"
        tag_re = r"<([a-zA-Z]+)\b([^>]*?)(/?)>"

        def paint(m):
            tag, attrs = m.group(1), m.group(2)
            props = [f"{k}:{acc}" for k in ("stroke", "fill") if f' {k}="{ink}"' in attrs]
            if not props:
                return m.group(0)
            attrs = re.sub(rf'\s(stroke|fill)="{re.escape(ink)}"', "", attrs)
            return f'<{tag}{attrs} style="{";".join(props)}"' + ("/>" if m.group(3) else ">")

        out, i = [], 0
        for a in re.finditer(r'<([a-zA-Z]+)\b[^>]*\sdata-part="accent"[^>]*?(/?)>', inner):
            if a.start() < i:
                continue
            head = re.sub(tag_re, paint, a.group(0), count=1)
            if a.group(1) != "g" or a.group(2):
                out.append(inner[i:a.start()] + head)
                i = a.end()
                continue
            depth, j = 1, a.end()
            while depth and j < len(inner):
                nxt = re.search(r"<g\b|</g>", inner[j:])
                if not nxt:
                    break
                depth += 1 if nxt.group(0) == "<g" else -1
                j += nxt.end()
            out.append(inner[i:a.start()] + head + re.sub(tag_re, paint, inner[a.end():j]))
            i = j
        return "".join(out) + inner[i:]

    def check_res(self, page):
        """DR-179 and D2-634 in the page's markup: a 24 px pillar fit draws on 1x screens with its master on 2x screens
        beside it in one <svg>, a 16 px fit draws on every screen, and a pillar icon under 48 px sets no accent (R10,
        D2-497). A plate marked data-oa-res="fixed" shows one drawing on every screen on purpose."""
        specs = [(m.start(), m.group(1)) for m in re.finditer(r'\sdata-specimen="([^"]+)"', page)]

        def where(pos):
            k = max((s for s in specs if s[0] < pos), default=None)
            return k[1] if k else "masthead and shell"

        uses = list(re.finditer(r"<use\b[^>]*>", page))
        seen = set()
        for u in uses:
            ref = re.search(r'href="#(oa-sym-[a-z0-9-]+)"', u.group(0))
            if not ref or not (PILLAR_FIT.match(ref.group(1)) or "oa-at-" in u.group(0)):
                continue
            start = page.rfind("<svg", 0, u.start())
            end = page.find("</svg>", u.end())
            if start < 0 or end < 0 or start in seen:
                continue
            seen.add(start)
            open_tag = re.match(r"<svg\b[^>]*>", page[start:]).group(0)
            group = []
            for v in uses:
                if start < v.start() < end:
                    r = re.search(r'href="#(oa-sym-[a-z0-9-]+)"', v.group(0))
                    cls = (re.search(r'\sclass="([^"]*)"', v.group(0)) or [None, ""])[1].split()
                    group.append((r.group(1) if r else "", "oa-at-1x" in cls, "oa-at-2x" in cls))
            fits = [(g, PILLAR_FIT.match(g[0])) for g in group if PILLAR_FIT.match(g[0])]
            at = where(start)
            if fits and "--oa-icon-accent" in open_tag:
                R.warn(at, f"a pillar icon under 48 px ({fits[0][0][0]}) sets --oa-icon-accent; icons are one color under 48 px (R10, D2-497)")
            if 'data-oa-res="fixed"' in open_tag:
                continue
            ones = [g for g in group if g[1]]
            twos = [g for g in group if g[2]]
            for (sid, one, two), m in fits:
                master = f"oa-sym-{m.group(1)}"
                if m.group(2) == "24":
                    if not one or not any(t[0] == master for t in twos):
                        R.warn(at, f'{sid} draws the 24 px fit on 2x screens too; DR-179 gives them the master: <use class="oa-at-1x" '
                                   f'href="#{sid}"/><use class="oa-at-2x" href="#{master}"/> in one <svg>, or data-oa-res="fixed" on a plate that shows the fit itself')
                elif twos:
                    R.warn(at, f"{sid} has a master on 2x screens beside it; a 16 px pillar icon keeps its fit on every screen (D2-634)")
            if twos and not ones:
                R.warn(at, f"{twos[0][0]} draws only on 2x screens, so 1x screens show nothing; pair it with an oa-at-1x <use>")
            for sid, one, two in ones:
                if not PILLAR_FIT.match(sid):
                    R.warn(at, f'{sid} is marked oa-at-1x but is no pixel fit; only a 24 px pillar fit switches by screen (DR-179)')

    def parity(self, tokens):
        """Each utility icon the page draws carries the line, caps, joins and grid its size's token sets, and is that
        token's reader on the page (D2-402). Returns the custom property names read this way."""
        read = set()
        for sid in self.placed:
            fam, p, label = self.symbols[sid]
            if fam != "utility":
                continue
            size = int(re.search(r"-(\d+)px$", sid).group(1))
            tok = UTILITY_LINE.get(size)
            if not tok or not tokens.known(tok):
                R.note(f"{label} is on the page and the {size} px utility line has no token yet; the engineer adds it (D2-577)")
                continue
            root = re.search(r"<svg\b[^>]*>", p.read_text()).group(0)
            attr = lambda k: (re.search(rf'\s{k}="([^"]*)"', root) or [None, None])[1]
            want = tokens.value(tok)
            ext = ((tokens.flat[tokens.by_css[css_name(tok)]].get("$extensions") or {}).get("org.oathandaction") or {}) if css_name(tok) in tokens.by_css else {}
            off = []
            sw = attr("stroke-width")
            try:
                if sw is None or abs(float(sw) - float(re.sub(r"px$", "", want))) > 1e-6:
                    off.append(f"a line of {sw or 'no declared width'} where {tok} sets {want}")
            except ValueError:
                off.append(f"a line of {sw} that cannot be read against {tok} ({want})")
            for k, e in (("stroke-linecap", "linecap"), ("stroke-linejoin", "linejoin")):
                if ext.get(e) and attr(k) != ext[e]:
                    off.append(f"{k} {attr(k)} where the token's grid sets {ext[e]}")
            vb = attr("viewBox")
            if ext.get("grid") and vb and abs(float(vb.split()[2]) - float(ext["grid"])) > 1e-6:
                off.append(f"a {vb.split()[2]}-unit grid where the token sets a {ext['grid']}-unit grid")
            if off:
                R.warn("sprite utility", f"{p.name} ({label}) draws {'; '.join(off)}")
            read.add(css_name(tok))
        return read

    def inject(self, page):
        """One hidden sprite per family, after <body>, holding the symbols the page references; and the bytes it adds."""
        used = sorted(set(re.findall(r'href="#(oa-sym-[a-z0-9-]+)"', page)))
        unknown = [u for u in used if u not in self.symbols]
        if unknown:
            gone = sorted({self.family_of(u) for u in unknown} & set(self.missing))
            why = "".join(f"; the {SPRITE_FAMILIES[f]['name']} folder {', '.join(str(self.rel(SPRITE_ROOT / d)) for d in self.missing[f])} does not exist"
                          for f in gone)
            R.warn("sprites", f"{len(unknown)} <use> reference(s) to no symbol: {', '.join(unknown[:6])}{why}")
        self.placed = [u for u in used if u in self.symbols]
        fams = {}
        for u in self.placed:
            fam, path, _ = self.symbols[u]
            fams.setdefault(fam, []).append(self.symbol(path, u, SPRITE_FAMILIES[fam]["ink"]))
        if not fams:
            return page, 0, {}
        sprite = "".join(f'<svg class="oa-sprite" data-sprite="{fam}" aria-hidden="true" focusable="false" width="0" height="0" '
                         f'style="position:absolute;width:0;height:0;overflow:hidden">{"".join(syms)}</svg>' for fam, syms in fams.items())
        page = re.sub(r"(<body\b[^>]*>)", lambda m: m.group(1) + "\n" + sprite, page, count=1)
        return page, len(sprite.encode()), {fam: len(syms) for fam, syms in fams.items()}


def sprite_sheet(out):
    """Every symbol of every family with its file, for sprite_check.js, which draws each through <use> beside its file."""
    s = Sprites()
    rows = {sid: {"family": fam, "file": str(p), "label": label, "symbol": Sprites.symbol(p, sid, SPRITE_FAMILIES[fam]["ink"])}
            for sid, (fam, p, label) in s.symbols.items()}
    Path(out).write_text(json.dumps({"root": str(SPRITE_ROOT), "missing": s.missing, "warnings": R.warnings, "notes": R.notes,
                                     "inks": {f: c["ink"] for f, c in SPRITE_FAMILIES.items()}, "symbols": rows}, indent=1))
    print(f"wrote {out}: {len(rows)} symbols, " + ", ".join(f"{f} {sum(1 for r in rows.values() if r['family'] == f)}" for f in SPRITE_FAMILIES)
          + "".join(f"\n  warning [{w['where']}] {w['message']}" for w in R.warnings) + "".join(f"\n  note: {n}" for n in R.notes))
    return 1 if R.warnings else 0


def sheet_uri(path, shown_px, where, sid):
    """A contact sheet as an image: resampled to twice the width it is shown at and kept to a small palette."""
    try:
        from PIL import Image
    except ImportError:
        R.warn(where, f"{sid}: Pillow is missing, so {path.name} is embedded as it is")
        return data_uri(path)
    im = Image.open(path).convert("RGB")
    w = int(round(2 * shown_px))
    if im.width > w:
        im = im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)
    buf = io.BytesIO()
    im.quantize(colors=SHEET_COLORS, method=Image.Quantize.MEDIANCUT).save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------------------------------------------------------
# IDs at line ends (D2-975, round 3 fix pass, November 10, 2026). D2-950 keeps an ID whole at a line end; the makers wrote
# IDs with U+2011, the non-breaking hyphen, which the Inter files this page loads do not draw (the browser borrows it
# from another font) and which a producer who copies "CL-001" or searches for it cannot match. The built page writes
# every ID with an ASCII hyphen and holds it whole with the shell's .nw: in text, each ID (and any other word a maker
# wrote with U+2011) goes in <span class="nw">; inside a tag's attributes, in SVG text and in raw text (scripts, styles,
# the title, a textarea), U+2011 turns into an ASCII hyphen and nothing is added. The makers' sources may keep U+2011.
# ---------------------------------------------------------------------------------------------------------------
NBH = "\u2011"
_H = "[-\u2011]"
_UTILITY_IDS = ("another-site", "selected-check", "view-full-size", "download", "chevron", "warning", "success", "filter",
                "search", "arrow", "close", "error", "pause", "reset", "menu", "copy", "play", "sort")
_STATUS_IDS = ("never-happened", "take-part", "not-yet", "stopped", "done", "now")
ID_PATTERN = re.compile(
    "(?<![\\w\u2011-])(?:"
    "CL" + _H + "\\d{3}(?:" + _H + "\\d+px)?"
    "|R" + _H + "\\d{2}"
    "|U" + _H + "(?:" + "|".join(n.replace("-", _H) for n in _UTILITY_IDS) + ")"
    "|S" + _H + "(?:" + "|".join(n.replace("-", _H) for n in _STATUS_IDS) + ")"
    "|E" + _H + "[a-z]+(?:" + _H + "[A-Za-z]+)*"
    ")(?![\\w\u2011]|-\\w)"
    "|[\\w.]*\u2011[\\w\u2011]*")
_TAG = re.compile(r"<!--.*?-->|<(/?)([A-Za-z][\w:-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>", re.S)
_RAW = ("script", "style", "textarea", "title")


def keep_ids_whole(page, wrap=True, mark=""):
    """D2-975: IDs in text in <span class="nw"> with an ASCII hyphen; U+2011 out of attributes, SVG and raw text."""
    page = re.sub("&#(?:8209|x2011);", NBH, page, flags=re.I)
    out, pos, svg, n_ids = [], 0, 0, 0

    def text(t):
        nonlocal n_ids
        if svg or not wrap:
            return t.replace(NBH, "-")

        def one(m):
            nonlocal n_ids
            n_ids += 1
            return f'<span class="nw"{mark}>' + m.group(0).replace(NBH, "-") + "</span>"
        return ID_PATTERN.sub(one, t).replace(NBH, "-")

    while True:
        m = _TAG.search(page, pos)
        if not m:
            out.append(text(page[pos:]))
            break
        out.append(text(page[pos:m.start()]))
        tok = m.group(0)
        out.append(tok.replace(NBH, "-"))
        pos = m.end()
        if tok.startswith("<!--"):
            continue
        close, name = m.group(1), m.group(2).lower()
        if name == "svg" and not tok.endswith("/>"):
            svg += -1 if close else 1
        if not close and name in _RAW:
            end = re.compile(rf"</{name}\s*>", re.I).search(page, pos)
            stop = end.start() if end else len(page)
            out.append(page[pos:stop].replace(NBH, "-"))
            pos = stop
    return "".join(out), n_ids


def weigh(page, sprite_bytes):
    """Bytes by part of the page: head and shell, sprites, each chapter, the appendix and the rest, against the budgets."""
    size = lambda x: len(x.encode())
    parts = {"head and shell": size(page[:page.find("<body")]) + size(page[page.rfind("<script>"):]), "sprites": sprite_bytes}
    marks = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(r'<section class="(chapter|part|contents|appendix|cover)[^"]*" id="([^"]+)"', page)]
    end = page.find("</main>")
    anchors = {a: n for n, a, *_ in CHAPTERS}
    chapters = {}
    for (start, kind, anchor), nxt in zip(marks, [m[0] for m in marks[1:]] + [end]):
        b = size(page[start:nxt])
        if kind == "chapter" and anchor in anchors:
            chapters[anchors[anchor]] = b
        elif kind == "appendix":
            parts["appendix"] = parts.get("appendix", 0) + b
        else:
            parts["front matter and part openers"] = parts.get("front matter and part openers", 0) + b
    total = size(page)
    for n, b in sorted(chapters.items()):
        budget = WEIGHT_BUDGET.get(n, WEIGHT_DEFAULT) * MB
        if b > budget:
            R.warn(f"chapter {n}", f"weighs {b / MB:.2f} MB, over its budget of {budget / MB:.2f} MB; draw symbols from the sprite, show "
                                   f"contact sheets as images and keep photographs at the size shown")
    for k, b in parts.items():
        if b > WEIGHT_FIXED.get(k, 0) * MB:
            R.warn("page weight", f"{k} weighs {b / MB:.2f} MB, over its budget of {WEIGHT_FIXED.get(k, 0):.2f} MB")
    if total > WEIGHT_PAGE:
        R.warn("page weight", f"the page weighs {total / MB:.2f} MB, over its budget of {WEIGHT_PAGE / MB:.1f} MB (the limit is {WEIGHT_LIMIT / MB:.0f} MB)")
    return {"bytes": total, "budget_page": WEIGHT_PAGE, "limit": WEIGHT_LIMIT, "parts": parts,
            "chapters": {n: {"bytes": b, "budget": WEIGHT_BUDGET.get(n, WEIGHT_DEFAULT) * MB} for n, b in sorted(chapters.items())}}


def build(args):
    chap_dir = Path(args.chapters).resolve() if args.chapters else GUIDE / "chapters"
    spec_dir = Path(args.specimens).resolve() if args.specimens else GUIDE / "specimens"
    out_path = Path(args.out).resolve() if args.out else DEFAULT_OUT
    tokens = Tokens()
    sprites = Sprites()
    specs = Specimens(spec_dir)
    # DR-203: the code sets rules may show; a --demo build adds the shell's fixture set
    code_dirs = [Path(args.code).resolve()] if getattr(args, "code", None) else [CODE_DIR]
    if args.demo:
        code_dirs.append(SHELL / "fixtures/code")
    codes = CodeSets(code_dirs, tokens.css_names, (SHELL / "guide-shell.css").read_text())
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
    ctx = {"codes": codes, "present": present, "rule_anchors": rule_anchors, "lines": lines, "names": names, "has_proofs": has_proofs_ids,
           "appendix_title": APPENDIX_TITLE, "appendix_line": None, "order": order}
    pconf = None
    try:
        pconf = json.loads((chap_dir / "proofs.json").read_text())
        ctx["appendix_title"] = pconf.get("title") or APPENDIX_TITLE
        ctx["appendix_line"] = pconf.get("instruction") or None
    except Exception:
        pass

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
    check_cross_refs(chapters, pconf if isinstance(pconf, dict) else None, specs)
    for sid in sorted(set(codes.files) - set(codes.used)):
        R.note(f"code set {sid} is in the code folder, and no rule shows it yet")
    # Stage B page weight: a drawing a sprite holds is drawn by <use>. From chapter 09 on, a specimen that inlines one is a
    # warning; earlier chapters' specimens are listed for their owners.
    for sid in sorted(specs.used):
        if sid not in specs.files:
            continue
        syms = sprites.inlined(specs.files[sid].read_text())
        if not syms:
            continue
        ch = re.match(r"s-(\d\d)-", sid)
        msg = (f"{sid} inlines {len(syms)} drawing(s) the sprite holds ({', '.join(sprites.symbols[s][2] for s in syms[:6])}); "
               f"draw each as {sprites.use_tag(syms[0])}")
        if ch and ch.group(1) >= SPRITE_FROM_CHAPTER:
            R.warn(specs.used[sid], msg)
        else:
            R.note(msg)

    css = (SHELL / "guide-shell.css").read_text()
    js = (SHELL / "guide-shell.js").read_text()
    used_vars = set(re.findall(r"var\((--oa-[a-z0-9-]+)", css))
    tok_css = tokens.stylesheet()
    defined = set(re.findall(r"(--oa-[a-z0-9-]+)\s*:", tok_css))
    missing = sorted(used_vars - defined)
    if missing:
        R.warn("shell", f"the shell uses {len(missing)} custom properties the token stylesheet does not define: {', '.join(missing[:8])}")
    # D2-402, stage B: every token in the mark family and the utility icon family has a reader in the page, a var() in
    # the shell's or a placed specimen's CSS, so the guide and tokens.css cannot drift apart unseen. guide_check.js
    # then measures the drawn marks against the token values (markTokens). Promotion: a utility icon drawn from the
    # sprite reads its line token through the build's parity test (Sprites.parity), once the page is assembled below.
    readers = css + "".join(specs.files[s].read_text() for s in specs.used if s in specs.files)
    unread = sorted(n for n in defined if n.startswith(READ_FAMILIES) and f"var({n}" not in readers) if tokens.final else []
    # Round 2: chapter 11's plates read the mark tokens and the shell no longer does, so a page without chapter 11 asks
    # for no mark reader (as guide_check.js's markTokens asks only where chapter 11 is in the page)
    if "11" not in chapters:
        unread = [n for n in unread if not n.startswith("--oa-component-mark-")]

    wm24 = svg_inline(WORDMARK_24, label="Oath & Action", cls="wm wm-24")
    wm16 = svg_inline(WORDMARK_16, label="Oath & Action", cls="wm wm-16")
    # the cover's h1 names the guide in full, so the display wordmark above it is hidden from assistive technology
    wm_display = svg_inline(WORDMARK_DISPLAY, cls="cover-wm")
    built = datetime.datetime.now().strftime("%B %-d, %Y at %H:%M")
    n_real = len(chapters)
    n_rules = sum(len(d.get("rules") or []) for d in chapters.values())
    n_specs = len(specs.used)
    appendix_title = ctx.get("appendix_title", APPENDIX_TITLE)
    # The page's scope in words, from the chapters it holds: "Chapters 01 to 08" or "Chapters 01 to 08 and 11"
    scope = chapter_span(order)
    only_foundations = all(CHAPTER[n][3] == "foundations" for n in order)
    scope_long = f"{scope}, the Foundations part" if only_foundations and order == STAGE_A else scope
    edition_line = (f"{scope_long}, in draft, {EDITION_DATE}"
                    + ((", with an appendix of identity proofs." if appendix_title == APPENDIX_TITLE else f", with the appendix “{appendix_title}”.")
                       if has_proofs else "."))
    n_found = sum(1 for n in STAGE_A if n in chapters)
    count_line = (f"{n_real} chapters, {n_rules} rules and {n_specs} specimens." if n_found == len(STAGE_A) else
                  f"{n_found} of {len(STAGE_A)} Foundations chapters written so far, with {n_rules} rules and {n_specs} specimens in all; placeholders hold the rest.")
    folio = f"Foundations, {scope[0].lower() + scope[1:]}" if only_foundations else scope
    # C-S10, RP-S10: each arrow stays with the pillar after it, so the line breaks whole
    arr = '<span class="arr" aria-hidden="true">→</span>'
    pillars = LOCKED["pillars"][0] + "".join(f' <span class="nw">{arr} {p}</span>' for p in LOCKED["pillars"][1:])
    # The colophon's link is the page's one copy of tokens.css. data-oa-zip holds the zip the shell offers through the
    # host where one answers (DR-192, D2-964), and the two data-oa-*-words say what the button gives on each path.
    dl_tokens = (f' <a id="tokens-download" href="{tokens.download_uri}" download="{tokens.download_name}" data-oa-zip="{tokens.zip_b64}" '
                 f'data-oa-zip-name="{tokens.zip_name}" data-oa-css-words="{tokens.css_words}" data-oa-zip-words="{tokens.zip_words}">{tokens.css_words}</a>.' if tokens.final else "")

    # D2-1133 (stage C): the guide stays light whatever the device asks. tokens.css follows the device's dark setting
    # (DR-204), and data-oa-theme="light" on the root wins over it, so a plate shows a piece at its true colors.
    page = f"""<!doctype html>
<html lang="en" data-oa-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="only light">
<title>Oath &amp; Action Brand Guide, Edition 06: {"Foundations draft" if only_foundations else "draft of " + e(scope[0].lower() + scope[1:])}</title>
<meta name="description" content="Oath &amp; Action Brand Guide, Edition 06: the rules for everything Oath &amp; Action publishes. {e(scope_long)}, in draft.">
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
  <div class="mh-bar">
    <a class="home" href="#top" data-red="signature">{wm24}{wm16}</a>
    <span class="edition"><span class="edition-k">Brand Guide</span> Edition 06</span>
    <nav class="partnav" aria-label="Parts"><ul>
      <li><a href="#contents" data-part-link="contents">Contents</a></li>
      {"".join(f'<li><a href="#part-{s}" data-part-link="{s}">{e(n)}</a></li>' for s, n, _ in PARTS if any(CHAPTER[x][3] == s for x in order))}
      {'<li><a href="#proofs" data-part-link="appendix">Appendix</a></li>' if has_proofs else ''}
    </ul></nav>
    <button class="menubtn" id="menubtn" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="menu"><svg class="bars" viewBox="0 0 24 24" aria-hidden="true" focusable="false" data-icon="U-menu" data-icon-family="utility"><use href="#oa-sym-u-menu-24px"/></svg>Menu</button>
  </div>
  <p class="where" id="where" aria-hidden="true">Cover</p>
</header>
<div class="frame">
  <nav class="rail" aria-label="Chapters">{nav_list("rail", present, has_proofs, appendix_title=appendix_title)}</nav>
  <main id="main" tabindex="-1" data-view-root="overview">
    <section class="cover" id="top" data-track="front" data-label="Cover">
      <p class="cover-folio"><span>{e(folio)}</span> <span>Draft of {e(EDITION_DATE)}</span></p>
      <div class="cover-mark" data-red="signature">{wm_display}</div>
      <h1 class="cover-h1"><span class="vh">Oath &amp; Action </span>Brand Guide, Edition 06</h1>
      <p class="tagline">{e(LOCKED["tagline"])}</p>
      <p class="pillars">{pillars}</p>
      <p class="cover-purpose">This guide holds the rules for everything Oath &amp; Action publishes, for the staff, partners, designers and developers who make it.</p>
      <p class="cover-start"><a href="#contents">Open the contents</a></p>
    </section>
    {contents_section(present, has_proofs, ctx)}
    {"".join(body)}
    {proofs_html}
  </main>
</div>
<footer class="colophon oa-surface-charcoal" id="colophon">
  <div class="colophon-inner">
    <p class="colophon-k">Colophon</p>
    <dl class="colophon-list">
      <div><dt>Edition</dt><dd>Oath &amp; Action Brand Guide, Edition 06. {e(edition_line)}</dd></div>
      <div><dt>Contact</dt><dd>The editor. Ask the editor for any file this guide lists. Every co-branded piece goes to Dustin Cathcart, or an editor he names, before it prints or posts. An address follows once our web address is settled.</dd></div>
      <div><dt>Approval</dt><dd>Dustin Cathcart, Founder and Editor, approves every change to these rules.</dd></div>
      <div><dt>Type</dt><dd>Inter Tight for display, Inter for reading and interface, Lora Italic for quoted lines. All three are published under the SIL Open Font License 1.1 and load from Google Fonts in this draft.</dd></div>
      <div><dt>Tokens</dt><dd>{("Every color, size and space on this page comes from tokens.css, inlined when the page was built." + dl_tokens) if tokens.final else "This build carries a provisional token block, because tokens.css was not there yet."}</dd></div>
      <div><dt>Built</dt><dd>{e(built)}, from the guide&#8217;s source files: {e(count_line)}</dd></div>
    </dl>
    <p class="colophon-back"><a href="#contents">Back to contents</a></p>
  </div>
</footer>
<dialog class="menu" id="menu" aria-labelledby="menu-h">
  <div class="menu-inner">
    <div class="menu-head"><h2 id="menu-h" class="menu-title">Contents</h2><button type="button" class="menu-close" id="menuclose">Close the menu</button></div>
    <p class="menu-where">You are in <strong id="menu-where-text">Cover</strong>.</p>
    <div class="menu-scroll">
      <nav aria-label="Guide contents">{nav_list("menu", present, has_proofs, menu=True, appendix_title=appendix_title)}</nav>
    </div>
  </div>
</dialog>
<script>
{js}
</script>
</body>
</html>
"""
    sprites.check_res(page)
    page, sprite_bytes, sprite_counts = sprites.inject(page)
    page, n_whole = keep_ids_whole(page)   # D2-975
    if tokens.final:
        unread = [n for n in unread if n not in sprites.parity(tokens)]
        if unread:
            R.warn("tokens", f"{len(unread)} token(s) in the mark or utility icon family have no reader in the page: {', '.join(unread[:6])}")
    weights = weigh(page, sprite_bytes)
    weights["sprites"] = sprite_counts
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page)
    report = {
        "page": str(out_path.relative_to(ROOT)) if ROOT in out_path.parents else str(out_path),
        "built": datetime.datetime.now().isoformat(timespec="seconds"),
        "chapters": sorted(chapters), "placeholders": sorted(set(STAGE_A) - set(chapters)),
        "rules": n_rules, "specimens_placed": n_specs, "tokens": "tokens.css" if tokens.final else "provisional from the schema draft",
        "demo": bool(args.demo), "bytes": len(page.encode()), "weight": weights, "ids_held_whole": n_whole,
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


# ---------------------------------------------------------------------------------------------------------------
# Self-test (apply pass, November 7, 2026): fixture chapters in a temporary folder, one scenario per check, each with
# the warnings it must raise and the ones it must not. The fixtures are throwaway; nothing in the repository changes.
# ---------------------------------------------------------------------------------------------------------------
def self_test():
    import shutil
    import tempfile
    global R, LEGACY_FILE, SPRITE_ROOT
    kept_legacy, kept_root = LEGACY_FILE, SPRITE_ROOT

    def rule(rid, extra=None):
        r = {"id": rid, "title": f"Rule {rid} in a fixture.", "rule": "A fixture rule.", "why": {"text": "A fixture.", "basis": "Design judgment"}}
        r.update(extra or {})
        return r

    def chapter(num, anchor, title, rules, **more):
        return dict({"number": num, "anchor": anchor, "title": title, "instruction": f"Read the {title.lower()} fixture.",
                     "intro": ["A fixture chapter."], "rules": rules}, **more)

    ch01 = chapter("01", "purpose", "Purpose", [rule("01.1", {"builders": "Rule 08.8 sets the grid and icon that may lead a kicker, after Rule 01.1."})])
    old08 = chapter("08", "signal-grid", "The Signal Grid", [rule(f"08.{k}") for k in range(1, 10)])
    new08 = chapter("08", "lockmark", "The lockmark", [rule("08.1"), rule("08.2"), rule("08.3")])
    ch11 = chapter("11", "icons", "Status and utility icons", [rule("11.1"), rule("11.2")])
    gap08 = chapter("08", "lockmark", "The lockmark", [rule("08.1"), rule("08.3", {"correct": {"specimen": "s-test-old", "caption": "A fixture."}}),
                                                       rule("08.4", {"failure": {"specimen": "s-test-condensed", "caption": "A fixture."}})])
    xref01 = chapter("01", "purpose", "Purpose", [rule("01.1", {"rule": "Rules 08.1 to 08.3 place it. Rule 08.3 holds. See <a href=\"#rule-08-7\">the old composer</a>."})])
    specs = {"s-test-old.html": "<p>Lockmark 40 px, bottom right, inside the margin (Rule 08.2)</p>",
             "s-test-condensed.html": '<img data-inline src="work/build/assets/identity/wordmark-condensed/20261028_Wordmark-Condensed-24px-Master.svg" alt="Oath &amp; Action">'}
    manifest = {"s-test-old": {"chapter": "08", "rule": "08.3", "alt": "A lockmark drawn as Rule 08.5 sets it, at true size.", "notes": "fixture"},
                "s-test-condensed": {"chapter": "08", "rule": "08.4", "alt": "The condensed wordmark, a fixture at true size.", "notes": "fixture"}}
    # While LEGACY_FILE holds chapter 08 (the apply pass), the old name alone is read with a note; once the map is
    # emptied, the build expects 08-lockmark.json and the old name alone is a warning.
    legacy_on = LEGACY_FILE.get("08") == "signal-grid"
    lab_specs = {"s-lab-own.html": '<p><span class="illus">Illustrative</span> A notice.</p>', "s-lab-none.html": "<p>A notice.</p>",
                 "s-lab-flow.html": "<p>A notice that flows.</p>"}
    lab_manifest = {"s-lab-own": {"chapter": "08", "rule": "08.1", "width_px": 1400, "alt": "A wholly invented notice, a fixture.", "illustrative": True, "notes": "fixture"},
                    "s-lab-none": {"chapter": "08", "rule": "08.1", "width_px": 360, "fit_switch": False, "alt": "A wholly invented notice, a fixture.", "illustrative": True, "notes": "fixture"},
                    "s-lab-flow": {"chapter": "08", "rule": "08.2", "alt": "A notice that flows with the page, a fixture.", "notes": "fixture"}}
    lab08 = chapter("08", "lockmark", "The lockmark", [rule("08.1", {"correct": {"specimen": "s-lab-own", "caption": "A fixture."}, "failure": {"specimen": "s-lab-none", "caption": "A fixture."}}),
                                                       rule("08.2", {"correct": {"specimen": "s-lab-flow", "caption": "A fixture."}})])

    # Sprite families as fixtures (promotion, November 10, 2026), named and rooted as the promotion brief sets the finals,
    # made from the October set and the approved option files, which stay as the record (D2-718). Every scenario reads
    # the full set unless it names another; the faulty set lacks the pillar folder and holds the faults the build names.
    def families(root, faulty=False):
        cl = root / "civic-line-v6/black"
        cl.mkdir(parents=True)
        october = ASSETS / "civic-line/black"
        for cid in (("CL-019", "CL-024") if faulty else ("CL-019", "CL-020", "CL-021", "CL-022", "CL-024", "CL-025", "CL-029")):
            src = next(october.glob(f"*-{cid}-*-Black.svg"))
            shutil.copyfile(src, cl / src.name)
        utility = {"24": [("Menu", "A"), ("Close", "A")] + ([] if faulty else [("Success", "A")]), "16": [] if faulty else [("Close", "A")]}
        for size, names in utility.items():
            d = root / f"utility/svg-{size}"
            d.mkdir(parents=True)
            for nm, opt in names:   # Success option A for its mask, the one utility drawing that carries one
                s = re.sub(r'\sdata-option="[^"]*"', "", (ASSETS / f"utility-icons/svg-{size}/20261109_Utility-{nm}-Option-{opt}-{size}px.svg").read_text(), count=1)
                if faulty and nm == "Close":
                    s = s.replace('stroke-width="2"', 'stroke-width="2.5"', 1)
                (d / f"20261110_Utility-{nm}-{size}px.svg").write_text(s)
        if faulty:   # a file with no data-id, and a second file for CL-019
            (cl / "20261110_Oath-And-Action-Civic-Line-No-Id-Black.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><path d="M0 0h1"/></svg>')
            shutil.copyfile(next(cl.glob("*-CL-019-*")), cl / "20261110_Oath-And-Action-Civic-Line-CL-019-Explain-Copy-Black.svg")
            return
        pf = root / "pillar-icons"
        (pf / "svg").mkdir(parents=True)
        for src in sorted((ASSETS / "pillar-pixel-fit/svg").glob("*.svg")):
            m = re.match(r"20261109_(CL-\d+)-(\w+)-(16|24)px-Fit-([AB])-(Black|Red-Black)\.svg$", src.name)
            if not m or (m.group(3) == "24" and m.group(4) != "B"):
                continue
            cid, word, size, _, ed = m.groups()
            s = src.read_text().replace(f' data-id="{cid}"', f' data-id="{cid}" data-size="{size}"', 1)
            # the black edition one folder down, the red-black beside it, so the sprite must look down and pick black
            (pf / ("svg" if ed == "Black" else "") / f"20261110_Pillar-Icon-{cid}-{word}-{size}px-{ed}.svg").write_text(s)

    # stage B page weight fixtures (November 9, 2026)
    cl24 = next((ASSETS / "civic-line/black").glob("*CL-024-*-Black.svg")).read_text()
    sheet = next((ASSETS / "civic-line/contact-sheets").glob("*-01-*-Black-2x.png")).relative_to(ROOT)
    use = lambda i, extra="": f'<svg viewBox="0 0 128 128" width="48" height="48" aria-hidden="true" focusable="false"{extra}><use href="#oa-sym-{i}"/></svg>'
    hide = 'aria-hidden="true" focusable="false"'
    # the pattern specimen makers write: a 24 px pillar icon, fit on 1x screens and master on 2x (DR-179); a 16 px one
    pair = lambda i, extra="": (f'<svg viewBox="0 0 24 24" width="24" height="24" {hide} data-icon="{i.upper()}" data-icon-family="pillar"{extra}>'
                                f'<use class="oa-at-1x" href="#oa-sym-{i}-24px"/><use class="oa-at-2x" href="#oa-sym-{i}"/></svg>')
    fit16 = lambda i: f'<svg viewBox="0 0 16 16" width="16" height="16" {hide} data-icon="{i.upper()}" data-icon-family="pillar"><use href="#oa-sym-{i}-16px"/></svg>'
    util = lambda n, px: (f'<svg viewBox="0 0 {px} {px}" width="{px}" height="{px}" {hide} data-icon="U-{n}" data-icon-family="utility">'
                          f'<use href="#oa-sym-u-{n}-{px}px"/></svg>')
    wt_specs = {"s-10-use.html": f"<p>{use('cl-019')} Explain</p><p>{use('cl-025', ' style=\"--oa-icon-accent:var(--oa-color-identity-signature-on-newsprint)\"')} Congress</p>",
                "s-10-inline.html": f"<p>{cl24} Feedback loop</p>",
                "s-10-sheet.html": f'<img data-oa-sheet="600" src="{sheet}" alt="Civic Line sheet 01, a fixture." width="600">',
                "s-10-badref.html": f"<p>{use('cl-999')} No such symbol</p>",
                "s-09-big.html": "<p>" + "Weight. " * 56000 + "</p>"}
    wt_manifest = {k[:-5]: {"chapter": k[2:4], "rule": f"{k[2:4]}.1", "alt": f"A page weight fixture, {k[:-5]}.", "notes": "fixture"} for k in wt_specs}
    wt10 = chapter("10", "symbols", "Topic and atlas symbols", [rule("10.1", {"correct": {"specimen": "s-10-use", "caption": "A fixture."}, "failure": {"specimen": "s-10-inline", "caption": "A fixture."}}),
                                                                rule("10.2", {"correct": {"specimen": "s-10-sheet", "caption": "A fixture."}, "failure": {"specimen": "s-10-badref", "caption": "A fixture."}})])
    wt09 = chapter("09", "pillar-icons", "Pillar icons", [rule("09.1", {"correct": {"specimen": "s-09-big", "caption": "A fixture."}})])
    wt_manifest = {k: dict(v, rule={"s-10-use": "10.1", "s-10-inline": "10.1", "s-10-sheet": "10.2", "s-10-badref": "10.2", "s-09-big": "09.1"}[k]) for k, v in wt_manifest.items()}

    # promotion fixtures (November 10, 2026): three families in one page, the faults, and the 1x and 2x pattern
    def plates(num, anchor, title, sids):
        rules, pairs = [], [sids[k:k + 2] for k in range(0, len(sids), 2)]
        for n, two in enumerate(pairs, 1):
            r = {"correct": {"specimen": two[0], "caption": "A fixture."}}
            if len(two) > 1:
                r["failure"] = {"specimen": two[1], "caption": "A fixture."}
            rules.append(rule(f"{num}.{n}", r))
        man = {s: {"chapter": num, "rule": f"{num}.{k // 2 + 1}", "alt": f"A sprite fixture, {s}.", "notes": "fixture"} for k, s in enumerate(sids)}
        return chapter(num, anchor, title, rules), man

    accent = ' style="--oa-icon-accent:var(--oa-color-identity-signature-on-newsprint)"'
    fam_specs = {"s-09-px.html": f"<p>{pair('cl-019')} Explain</p><p>{fit16('cl-019')} Explain</p>",
                 "s-10-two.html": f"<p>{use('cl-025', accent)} Congress</p><p>{use('cl-029')} Public services</p>",
                 "s-11-ui.html": f"<p>{util('close', 24)}Close</p><p>{util('success', 24)}Saved</p><p>{util('close', 16)}Close</p>"}
    f09, m09 = plates("09", "pillar-icons", "Pillar icons", ["s-09-px"])
    f10, m10 = plates("10", "symbols", "Topic and atlas symbols", ["s-10-two"])
    f11, m11 = plates("11", "icons", "Status and utility icons", ["s-11-ui"])
    bad_specs = {"s-10-bad.html": f"<p>{use('cl-999')} No such drawing</p><p>{pair('cl-019')} Explain</p><p>{util('nothing', 24)}Nothing</p><p>{util('close', 24)}Close</p>"}
    b10, b10m = plates("10", "symbols", "Topic and atlas symbols", ["s-10-bad"])
    res_specs = {"s-09-good.html": f"<p>{pair('cl-019')} Explain</p><p>{fit16('cl-020')} Track</p>",
                 "s-09-alone.html": f'<p><svg viewBox="0 0 24 24" width="24" height="24" {hide} data-icon="CL-020" data-icon-family="pillar"><use href="#oa-sym-cl-020-24px"/></svg> Track</p>',
                 "s-09-sixteen.html": (f'<p><svg viewBox="0 0 16 16" width="16" height="16" {hide} data-icon="CL-021" data-icon-family="pillar"><use class="oa-at-1x" '
                                       f'href="#oa-sym-cl-021-16px"/><use class="oa-at-2x" href="#oa-sym-cl-021"/></svg> Connect</p>'),
                 "s-09-twoonly.html": f'<p><svg viewBox="0 0 24 24" width="24" height="24" {hide} data-icon="CL-022" data-icon-family="pillar"><use class="oa-at-2x" href="#oa-sym-cl-022"/></svg> Act</p>',
                 "s-09-accent.html": f"<p>{pair('cl-022', accent)} Act</p>",
                 "s-09-wrongone.html": (f'<p><svg viewBox="0 0 24 24" width="24" height="24" {hide} data-icon="CL-020" data-icon-family="pillar"><use class="oa-at-1x" '
                                        f'href="#oa-sym-cl-020"/><use class="oa-at-2x" href="#oa-sym-cl-020"/></svg> Track</p>'),
                 "s-09-fixed.html": f'<p><svg viewBox="0 0 24 24" width="96" height="96" {hide} data-oa-res="fixed"><use href="#oa-sym-cl-019-24px"/></svg> The fit, enlarged four times</p>'}
    r09, r09m = plates("09", "pillar-icons", "Pillar icons", [k[:-5] for k in res_specs])

    def sprites_of(pg):
        return re.findall(r'<svg class="oa-sprite" data-sprite="([^"]+)"[^>]*>(.*?)</svg>', pg, re.S)

    def symbols_of(pg):
        return re.findall(r'<symbol id="([^"]+)"[^>]*>(.*?)</symbol>', "".join(b for _, b in sprites_of(pg)), re.S)

    def figure_of(pg, sid):
        m = re.search(r'<figure[^>]*id="fig-' + re.escape(sid) + r'".*?</figure>', pg, re.S)
        return m.group(0) if m else ""

    def caption_of(pg, sid):
        m = re.search(r'<figcaption class="plate-cap">(.*?)</figcaption>', figure_of(pg, sid), re.S)
        return m.group(1) if m else ""

    scenarios = [
        (("old file name alone: read silently, old numbers still valid" if legacy_on else
          "old file name alone: a warning, since the build expects 08-lockmark.json"),
         {"01-purpose.json": ch01, "08-signal-grid.json": old08}, {},
         ({"note": ["under its old name"], "absent": ["expected the file name", "\"anchor\" is", "cites Rule", "still reads"],
           "html": ['<section class="chapter" id="lockmark"', '<span id="grid" class="alias"']} if legacy_on else
          {"warn": ["expected the file name 08-lockmark.json", "\"anchor\" is 'signal-grid'"], "absent": ["under its old name"]})),
        ("renamed file: an old 08 number fails until the sentence changes", {"01-purpose.json": ch01, "08-lockmark.json": new08}, {},
         {"warn": ["cites Rule 08.8, which chapter 08 does not hold", "still reads \"Rule 08.8 sets the grid"],
          "absent": ["under its old name", "cites Rule 01.1", "expected the file name"],
          "html": ['<section class="chapter" id="lockmark"', '<span id="grid" class="alias"']}),
        ("both file names: the new one wins and the old one is a warning", {"08-lockmark.json": new08, "08-signal-grid.json": old08}, {},
         {"warn": ["the chapter's old file name" if legacy_on else "expected the file name 08-lockmark.json"],
          "html": ['<span class="t">The lockmark</span></h2>']}),
        ("cross-references: ranges, links, specimens, alt text and the condensed drawing",
         {"01-purpose.json": xref01, "08-lockmark.json": gap08}, {"specimens": specs, "manifest": manifest},
         {"warn": ["cites Rule 08.2, which chapter 08", "cites Rule 08.7, which chapter 08", "cites Rule 08.5, which chapter 08",
                   "still reads \"40 px, bottom right, inside the margin (Rule 08.2)\"", "draws the condensed wordmark"],
          "absent": ["cites Rule 08.1,", "cites Rule 08.3,"]}),
        ("chapter 11 under its part opener; 09, 10 and 12 coming later; the appendix follows it",
         {"08-lockmark.json": new08, "11-icons.json": ch11, "proofs.json": {"title": "Identity proofs", "items": []}}, {},
         {"absent": ["expected the file name", "D2-328"],
          "order": ['id="part-foundations"', 'id="lockmark"', 'id="part-symbols"', 'id="icons"', 'id="proofs"'],
          "html": ['<li class="part-later"><span class="part-name"><span class="n">09</span>', '<span class="n">10</span> <span class="t">Topic and atlas symbols</span></span>',
                   '<span class="n">12</span> <span class="t">Graphic devices and patterns</span></span>', 'href="#icons" rel="next"',
                   'After chapter 11</p>', '<a href="#icons" rel="prev">', 'Chapters 01 to 08 and 11']}),
        ("a rename in progress: with the old name in LEGACY_FILE, it is read with a note and old numbers stay valid",
         {"01-purpose.json": ch01, "08-signal-grid.json": old08}, {"legacy": {"08": "signal-grid"}},
         {"note": ["under its old name"], "absent": ["expected the file name", "\"anchor\" is", "cites Rule", "still reads"],
          "html": ['<section class="chapter" id="lockmark"', '<span id="grid" class="alias"']}),
        ("fix pass: one Illustrative label per plate, and the switch on every fixed-width plate unless the manifest opts out",
         {"08-lockmark.json": lab08}, {"specimens": lab_specs, "manifest": lab_manifest},
         {"absent": ["fit_switch needs width_px"],
          "tests": [("the piece with its own label gets none in its caption", lambda pg: '<span class="illus">' not in caption_of(pg, "s-lab-own")),
                    ("the piece with no label gets the caption's", lambda pg: '<span class="illus">Illustrative</span>' in caption_of(pg, "s-lab-none")),
                    ("a fixed-width plate carries the switch, hidden until the shell offers it", lambda pg: 'aria-label="Size of this specimen" hidden>' in figure_of(pg, "s-lab-own")),
                    ("a plate with no width carries none", lambda pg: "fit-switch" not in figure_of(pg, "s-lab-flow")),
                    ("\"fit_switch\": false leaves it out", lambda pg: "fit-switch" not in figure_of(pg, "s-lab-none")),
                    ("the hint names the column", lambda pg: "Wider than this column." in figure_of(pg, "s-lab-own"))]}),
        ("appendix title: anything but Identity proofs is a warning", {"proofs.json": {"title": "Wordmark width proofs", "items": []}}, {},
         {"warn": ["D2-328 names it \"Identity proofs\""], "html": ['After chapter 08</p>', 'Foundations, chapters 01 to 08']}),
        ("stage B page weight: one sprite of the symbols referenced, a contact sheet as an image, inlined drawings and budgets",
         {"09-pillar-icons.json": wt09, "10-symbols.json": wt10}, {"specimens": wt_specs, "manifest": wt_manifest},
         {"warn": ["s-10-inline inlines 1 drawing(s) the sprite holds (CL-024)", "<use> reference(s) to no symbol: oa-sym-cl-999",
                   "over its budget of 0.40 MB"],
          "absent": ["s-10-use inlines", "s-10-sheet inlines", "chapter 10] weighs"],
          "html": ['<section class="chapter" id="pillar-icons"', 'data-sprite="civic-line"', '<symbol id="oa-sym-cl-019" viewBox="0 0 128 128">',
                   'var(--oa-icon-accent,currentColor)', 'href="#oa-sym-cl-025"'],
          "tests": [("the sprite holds the two symbols referenced and the masthead's menu glyph, and only those",
                     lambda pg: sorted(s for s, _ in symbols_of(pg)) == ["oa-sym-cl-019", "oa-sym-cl-025", "oa-sym-u-menu-24px"]),
                    ("one sprite for the family, placed once", lambda pg: [f for f, _ in sprites_of(pg)].count("civic-line") == 1),
                    ("the sprite draws in currentColor, never the master's ink", lambda pg: all("#121212" not in b for _, b in sprites_of(pg))),
                    ("the contact sheet is an image under 150 KB", lambda pg: 0 < len((re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', pg) or [None, ""])[1]) * 3 / 4 < 150_000)]}),
        ("promotion: three families, each symbol the page references once, after <body>, drawing as its file",
         {"09-pillar-icons.json": f09, "10-symbols.json": f10, "11-icons.json": f11},
         {"specimens": fam_specs, "manifest": {**m09, **m10, **m11}},
         {"absent": ["reference(s) to no symbol", "draws the 24 px fit", "--oa-component-icon-utility-", "[sprite ", "inlines", "sets --oa-icon-accent"],
          "html": ['data-sprite="civic-line"', 'data-sprite="pillar"', 'data-sprite="utility"',
                   '<symbol id="oa-sym-cl-019-24px" viewBox="0 0 24 24"><g shape-rendering="crispEdges">',
                   '<symbol id="oa-sym-cl-019-16px" viewBox="0 0 16 16"><g shape-rendering="crispEdges">',
                   '<symbol id="oa-sym-u-close-24px" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
                   '<symbol id="oa-sym-u-close-16px" viewBox="0 0 16 16"><g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">',
                   '<use href="#oa-sym-u-menu-24px"/></svg>Menu</button>', 'mask="url(#oa-sym-u-success-24px--', 'mask="url(#oa-sym-cl-029--'],
          "tests": [("one sprite per family, three in all, right after <body> and before the skip links",
                     lambda pg: sorted(f for f, _ in sprites_of(pg)) == ["civic-line", "pillar", "utility"]
                     and re.search(r'<body\b[^>]*>\s*(<svg class="oa-sprite".*?</svg>){3}\s*<a class="skip"', pg, re.S) is not None),
                    ("the sprite holds each symbol the page references, once, and no other",
                     lambda pg: sorted(s for s, _ in symbols_of(pg)) == sorted(set(re.findall(r'href="#(oa-sym-[a-z0-9-]+)"', pg)))),
                    ("every id inside a symbol starts with the symbol's own id",
                     lambda pg: all(i.startswith(s + "--") for s, b in symbols_of(pg) for i in re.findall(r'\sid="([^"]+)"', b))),
                    ("no symbol keeps the files' ink, red or comment", lambda pg: all("#121212" not in b and "#E63946" not in b and "<!--" not in b for _, b in sprites_of(pg))),
                    ("the pillar fit's accent shape draws through --oa-icon-accent",
                     lambda pg: re.search(r'<path data-part="accent"[^>]*\sstyle="fill:var\(--oa-icon-accent,currentColor\)"', dict(symbols_of(pg)).get("oa-sym-cl-019-24px", ""))),
                    ("a utility symbol carries no accent", lambda pg: "oa-icon-accent" not in dict(symbols_of(pg)).get("oa-sym-u-close-24px", "x")),
                    ("the masthead's old inline bars are gone", lambda pg: "M3 7h18" not in pg),
                    ("both utility line tokens are read, the 16 px one by the 16 px Close (round 2)", lambda pg: not any("16 px utility line has no token" in n for n in R.notes))]}),
        ("promotion: a missing family folder, an empty one, unreadable files, a line off its token and unknown references",
         {"10-symbols.json": b10}, {"specimens": bad_specs, "manifest": b10m, "sprites": "faulty"},
         {"note": ["sprite family pillar:", "pillar-icons does not exist yet"],
          "warn": ["reference(s) to no symbol: oa-sym-cl-019-24px, oa-sym-cl-999, oa-sym-u-nothing-24px", "the pillar fits folder",
                   "utility/svg-16 holds no utility icons drawing", "has no data-id on its root", "is a second drawing for oa-sym-cl-019",
                   "draws a line of 2.5 where oa.component.icon.utility.line.medium sets 2px"],
          "absent": ["draws the 24 px fit"],
          "tests": [("the page still builds, with the symbols that exist", lambda pg: sorted(f for f, _ in sprites_of(pg)) == ["civic-line", "utility"]
                     and {"oa-sym-cl-019", "oa-sym-u-menu-24px", "oa-sym-u-close-24px"} <= {s for s, _ in symbols_of(pg)})]}),
        ("promotion: the 1x and 2x pillar pattern (DR-179, D2-634) and one color under 48 px",
         {"09-pillar-icons.json": r09}, {"specimens": res_specs, "manifest": r09m},
         {"warn": ["[s-09-alone] oa-sym-cl-020-24px draws the 24 px fit on 2x screens too", "[s-09-sixteen] oa-sym-cl-021-16px has a master on 2x screens beside it",
                   "[s-09-twoonly] oa-sym-cl-022 draws only on 2x screens", "[s-09-accent] a pillar icon under 48 px (oa-sym-cl-022-24px) sets --oa-icon-accent",
                   "[s-09-wrongone] oa-sym-cl-020 is marked oa-at-1x but is no pixel fit"],
          "absent": ["[s-09-good]", "[s-09-fixed]", "reference(s) to no symbol"],
          "html": [".oa-at-2x { display: none }", "@media (min-resolution: 2dppx) { .oa-at-1x { display: none } .oa-at-2x { display: inline } }",
                   '<use class="oa-at-1x" href="#oa-sym-cl-019-24px"/><use class="oa-at-2x" href="#oa-sym-cl-019"/></svg>'],
          "tests": [("the sprite holds the fit and the master the pattern names", lambda pg: {"oa-sym-cl-019-24px", "oa-sym-cl-019", "oa-sym-cl-020-16px"} <= {s for s, _ in symbols_of(pg)}),
                    ("the 16 px fit draws alone, on every screen", lambda pg: '<use href="#oa-sym-cl-020-16px"/>' in figure_of(pg, "s-09-good"))]}),
        ("IDs held whole (D2-975): an ASCII hyphen inside span.nw in text, no U+2011 anywhere",
         {"01-purpose.json": chapter("01", "purpose", "Purpose", [rule("01.1", {"rule": "Draw CL\u2011001 and R\u201102 beside the take\u2011part mark, and U-close at 24 px.",
                                                                                "correct": {"specimen": "s-test-ids", "caption": "Reforms R\u201101 to R\u201125."}})])},
         {"specimens": {"s-test-ids.html": '<p>CL\u2011019 <b>S\u2011not\u2011yet</b></p><svg viewBox="0 0 80 20" width="80" height="20" aria-hidden="true"><text x="0" y="14">CL\u2011020</text></svg><script>var t = "two\u2011lane";</script>'},
          "manifest": {"s-test-ids": {"chapter": "01", "rule": "01.1", "alt": "A list of reforms, R\u201101 to R\u201125, at true size.", "width_px": 320, "notes": "fixture"}}},
         {"html": ['<span class="nw">CL-001</span>', '<span class="nw">R-02</span>', '<span class="nw">take-part</span>', '<span class="nw">U-close</span>',
                   '<span class="nw">CL-019</span>', '<span class="nw">S-not-yet</span>', '<text x="0" y="14">CL-020</text>', 'var t = "two-lane"',
                   'A list of reforms, R-01 to R-25, at true size.', '.nw { white-space: nowrap }'],
          "tests": [("no U+2011 is left anywhere in the page", lambda pg: "\u2011" not in pg),
                    ("SVG text takes no span", lambda pg: '<text x="0" y="14"><span' not in pg)]}),
    ]
    # stage C, round 0 (November 10, 2026): the opener figure (D2-965, D2-1134) and code to copy (DR-203)
    op_specs = {"s-09-op.html": "<p>An opening figure that flows with the column.</p>", "s-10-wide.html": "<p>A wide opener.</p>",
                "s-03-op.html": "<p>An opener in chapter 03.</p>"}
    op_manifest = {"s-09-op": {"chapter": "09", "alt": "An opening figure that flows, a fixture.", "notes": "fixture"},
                   "s-10-wide": {"chapter": "10", "width_px": 600, "alt": "A 600 px opening figure, a fixture at true size.", "notes": "fixture"},
                   "s-03-op": {"chapter": "03", "alt": "An opening figure for chapter 03, a fixture.", "notes": "fixture"}}
    op09 = chapter("09", "pillar-icons", "Pillar icons", [rule("09.1")], opener="s-09-op", intro=["The intro of chapter 09."])
    op10 = chapter("10", "symbols", "Topic and atlas symbols", [rule("10.1")], opener={"specimen": "s-10-wide", "caption": "A fixture."})
    op03 = chapter("03", "identity", "Identity", [rule("03.1")], opener="s-03-op")

    def ch09(pg):
        m = re.search(r'<section class="chapter[^"]*" id="pillar-icons".*?</section>', pg, re.S)
        return m.group(0) if m else ""

    code_files = {
        "c-01-good.html": '<div class="oa-good"><button type="button" class="oa-good-btn" aria-controls="panel">Show</button><p id="panel" class="oa-good-note">Shown.</p></div>\n',
        "c-01-good.css": ".oa-good { font: var(--oa-type-body); color: var(--oa-color-text-primary); background: var(--oa-color-surface) }\n"
                         ".oa-good-btn { font: var(--oa-type-ui); background: var(--oa-color-action-primary-fill); color: var(--oa-color-action-primary-label) }\n",
        "c-01-good.js": "document.querySelectorAll('.oa-good').forEach(function (box) { var b = box.querySelector('.oa-good-btn');"
                        " b.addEventListener('click', function () { document.getElementById(b.getAttribute('aria-controls')).hidden = false; }); });\n",
        "c-01-bad.html": '<div class="oa-bad sx-card" style="color:red"><button onclick="go()">Go</button><span class="oa-at-2x">2x</span></div>\n',
        "c-01-bad.css": ":scope { color: #E63946 } .oa-bad { color: var(--oa-color-text-primary-on-newsprint); background: white; font-size: 11px }\n"
                        "button { padding: 0 } .oa-bad .btn { color: var(--oa-no-such-token) } body .oa-bad { margin: 0 }\n",
        "c-01-bad.js": "import x from './x.js'; document.getElementById('panel');\n",
    }
    code01 = chapter("01", "purpose", "Purpose", [rule("01.1", {"code": {"set": "c-01-good", "name": "Show button", "caption": "A fixture."}}),
                                                  rule("01.2", {"code": {"set": "c-01-bad", "name": "Bad button"}}),
                                                  rule("01.3", {"code": "c-01-missing"}), rule("01.4", {"code": {"set": "c-01-good", "name": "Show button"}})])
    scenarios += [
        ("opener (D2-1134): chapter 09's figure under its intro and before its rules; 03's is refused; a 600 px opener is too wide",
         {"03-identity.json": op03, "09-pillar-icons.json": op09, "10-symbols.json": op10}, {"specimens": op_specs, "manifest": op_manifest},
         {"warn": ["\"opener\" names s-03-op, but chapters 01 to 08 open with words alone", "the opener s-10-wide is 600 px wide"],
          "absent": ["s-09-op is listed but no chapter places it", "[chapter 09] the opener"],
          "tests": [("chapter 09 holds its opener in the chapter head, after the intro and before the first rule",
                     lambda pg: 0 < ch09(pg).find('class="intro"') < ch09(pg).find('id="fig-s-09-op"') < ch09(pg).find('<div class="rule"')
                     and ch09(pg).find('id="fig-s-09-op"') < ch09(pg).find('<div class="ch-body">')),
                    ("the opener carries no label and the plate--opener class",
                     lambda pg: re.search(r'<figure class="plate plate--opener" id="fig-s-09-op"><div class="plate-head"><p class="plate-hint" hidden>', pg) is not None),
                    ("chapter 03 shows no opener", lambda pg: 'id="fig-s-03-op"' not in pg)]}),
        ("code to copy (DR-203): a set live in both themes with its panels; a faulty set warned on each fault; a missing set pending",
         {"01-purpose.json": code01}, {"code": code_files},
         {"warn": ["code set c-01-bad: the HTML carries a style attribute", "c-01-bad: the HTML carries an event handler attribute",
                   "literal color(s)", "reads --oa-no-such-token, which tokens.css does not define",
                   "type at 11 px", "the selector \"button\" names no oa- class", "styles the page's root or body", "uses @scope or :scope",
                   "reads --oa-color-text-primary-on-newsprint, named for one surface", "the guide's shell also styles", "the script holds an import",
                   "the script holds an ID written into the script", "code set c-01-missing needs work/build/guide/code/c-01-missing.html",
                   "class(es) btn, sx-card do not start with oa-", "the guide's shell also styles oa-at-2x",
                   "code set c-01-good is shown again", "\"name\" is empty"],
          "absent": ["code set c-01-good: ", "Rule 01.1] code set"],
          "html": ['<figure class="plate plate--code" id="code-c-01-good" data-code-set="c-01-good">', 'data-oa-theme="light" data-specimen="c-01-good--light"',
                   'data-oa-theme="dark" data-specimen="c-01-good--dark"', 'id="c-01-good--light--panel"', 'aria-controls="c-01-good--dark--panel"',
                   '>Copy the HTML</button>', '>Copy the CSS</button>', '>Copy the script</button>', '<style data-oa-code-css="c-01-good">',
                   '<script data-oa-code-js="c-01-good">', 'Code set <code>c-01-missing</code> is not in'],
          "tests": [("the HTML panel keeps the builder's own ids", lambda pg: 'aria-controls=&quot;panel&quot;' in pg and 'id=&quot;panel&quot;' in pg),
                    ("the status line carries the success and the error marks, hidden", lambda pg: 'id="code-c-01-good-status"><svg class="st-mark st-ok"' in pg)]}),
    ]
    results, ok_all = [], True
    with tempfile.TemporaryDirectory(prefix="oa-guide-build-") as tmp:
        roots = {"full": Path(tmp) / "families-full", "faulty": Path(tmp) / "families-faulty"}
        families(roots["full"])
        families(roots["faulty"], faulty=True)
        for i, (name, files, extra, expect) in enumerate(scenarios):
            base = Path(tmp) / f"s{i}"
            (base / "chapters").mkdir(parents=True)
            (base / "specimens").mkdir()
            for fn, data in files.items():
                (base / "chapters" / fn).write_text(json.dumps(data))
            for fn, text in (extra.get("specimens") or {}).items():
                (base / "specimens" / fn).write_text(text)
            if extra.get("manifest"):
                (base / "specimens" / "manifest-test.json").write_text(json.dumps(extra["manifest"]))
            if extra.get("code"):
                (base / "code").mkdir()
                for fn, text in extra["code"].items():
                    (base / "code" / fn).write_text(text)
            R = Report()
            LEGACY_FILE = extra.get("legacy", kept_legacy)
            SPRITE_ROOT = roots[extra.get("sprites", "full")]
            out = base / "page.html"
            try:
                build(argparse.Namespace(chapters=str(base / "chapters"), specimens=str(base / "specimens"), out=str(out),
                                         code=str(base / "code"), demo=False, strict=False, quiet=True))
            finally:
                LEGACY_FILE, SPRITE_ROOT = kept_legacy, kept_root
            warns = [f"[{w['where']}] {w['message']}" for w in R.warnings]
            page = out.read_text()
            checks = []
            for frag in expect.get("warn", []):
                checks.append((f"warns: {frag}", any(frag in w for w in warns)))
            for frag in expect.get("note", []):
                checks.append((f"notes: {frag}", any(frag in n for n in R.notes)))
            for frag in expect.get("absent", []):
                checks.append((f"no warning: {frag}", not any(frag in w for w in warns)))
            for frag in expect.get("html", []):
                checks.append((f"page holds: {frag}", frag in page))
            for desc, fn in expect.get("tests", []):
                checks.append((desc, bool(fn(page))))
            if expect.get("order"):
                pos = [page.find(x) for x in expect["order"]]
                checks.append(("page order: " + " < ".join(expect["order"]), all(p >= 0 for p in pos) and pos == sorted(pos)))
            ok = all(c for _, c in checks)
            ok_all &= ok
            results.append({"scenario": name, "pass": ok, "checks": [{"check": c, "pass": p} for c, p in checks]})
            print(f"{'pass' if ok else 'FAIL'}  {name}")
            for c, p in checks:
                if not p:
                    print(f"        missed: {c}")
            if not ok:
                for w in warns:
                    print(f"        warning {w}")
    n = sum(len(r["checks"]) for r in results)
    print(f"{'PASS' if ok_all else 'FAIL'} guide_build.py self-test: {sum(r['pass'] for r in results)} of {len(results)} scenarios, "
          f"{sum(c['pass'] for r in results for c in r['checks'])} of {n} expectations")
    return 0 if ok_all else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="output HTML path (default: the Stage A board page)")
    ap.add_argument("--chapters", help="folder of chapter JSON (default work/build/guide/chapters)")
    ap.add_argument("--specimens", help="folder of specimens and manifests (default work/build/guide/specimens)")
    ap.add_argument("--code", help="folder of code sets (default work/build/guide/code; --demo adds the shell's fixture set)")
    ap.add_argument("--demo", action="store_true", help="fill placeholder chapters with the shell's sample rules")
    ap.add_argument("--strict", action="store_true", help="exit 1 when there is any warning")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--sprite-root", help="folder that holds the sprite families' folders (default work/build/assets)")
    ap.add_argument("--sprite-sheet", metavar="JSON", help="write every symbol of every family, with its file, for sprite_check.js, and stop")
    ap.add_argument("--self-test", action="store_true", help="prove the build's checks on fixtures in a temporary folder")
    args = ap.parse_args()
    if args.sprite_root:
        global SPRITE_ROOT
        SPRITE_ROOT = Path(args.sprite_root).resolve()
    if args.sprite_sheet:
        sys.exit(sprite_sheet(args.sprite_sheet))
    sys.exit(self_test() if args.self_test else build(args))


if __name__ == "__main__":
    main()
