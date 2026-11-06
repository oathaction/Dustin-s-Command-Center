"""Shared helpers for the editor's chapters on stage board A (01 Purpose, 02 Voice).

Imported by guide_editor_build.py. Specimens are self-contained HTML fragments: colors only through var(--oa-...)
from work/build/tokens/tokens.css, text 13 px or larger, no heading elements, no em dash character anywhere
(W21's specimen draws it as a rule one em wide, DR-79). The shell (guide_build.py) scopes each fragment's <style>
to its own stage, so every fragment carries the small style block it needs.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHAPTERS = ROOT / "work/build/guide/chapters"
SPECIMENS = ROOT / "work/build/guide/specimens"

AMP24 = "work/build/assets/identity/ampersand/20261028_Amp-B-24px-Master.svg"
AMP_DISPLAY = "work/build/assets/identity/ampersand/20261028_Amp-B-Display-Master.svg"
WORDMARK24 = "work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg"
WORDMARK24_PRUSSIAN = "work/build/assets/identity/prussian/20261028_Wordmark-24px-Master-Prussian-White.svg"
TILE_GRID = "work/boards/phase-2/data-viz/shared/geo/us-state-tile-grid.json"
CHART_DATA = "work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json"
VOICE_CONTENT = "work/boards/phase-2/voice/20261106_Voice-Rules-Content.json"

LOCKED = {
    "tagline": "A country that answers to its people.",
    "mission": "Help people understand and improve the rules that shape their lives.",
    "promise": "We explain how a decision is made and give you a practical way to take part.",
    "commitment": "Clarity is our duty. Action is our promise.",
}
PILLARS = ["Explain", "Track", "Connect", "Act"]
VOICE_LINE_B = ("We’ll explain the rules and track what happens to them. When a decision is coming, "
                "we’ll connect you with the people making it, so you can act in time.")

e = lambda s: html.escape(str(s), quote=True)


def q(s):
    """Curly double quotes around a line."""
    return f"“{s}”"


# ---------------------------------------------------------------------------------------------------------------
# Style blocks. Short names (--oa-color-text-primary and the rest) come from the stage's surface class.
# ---------------------------------------------------------------------------------------------------------------
BASE = """
.ed{font-family:var(--oa-font-family-reading);font-size:1.0625rem;line-height:1.6;color:var(--oa-color-text-primary);max-width:100%}
.ed *{box-sizing:border-box}
.ed p{margin:0}
.ed .k{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--oa-color-text-secondary)}
.ed .src{font:var(--oa-type-caption);color:var(--oa-color-text-secondary);margin-top:12px;max-width:68ch}
.ed .chip{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;line-height:1.2;padding:5px 8px;border:1px solid var(--oa-color-border-strong);white-space:nowrap}
.ed .chip.solid{background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label);border-color:var(--oa-color-action-primary-fill)}
.ed .ill{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;line-height:1.3;padding:1px 6px;border:1px solid currentColor;vertical-align:.1em;white-space:nowrap}
.ed del{text-decoration:underline dotted 2px var(--oa-color-graphic-subtle);text-underline-offset:5px;text-decoration-skip-ink:none;color:inherit}
.ed ins{text-decoration:underline solid 2px var(--oa-color-graphic-essential);text-underline-offset:5px;text-decoration-skip-ink:none;color:inherit}
.ed .hinge{display:flex;align-items:center;gap:14px;margin:16px 0;color:var(--oa-color-identity-hinge-divider)}
.ed .hinge::before,.ed .hinge::after{content:"";flex:1 1 auto;border-top:1px solid currentColor}
.ed .hinge .hamp{flex:none;display:block;width:21px;height:24px}
.ed .ask{display:inline-block;background:var(--oa-color-action-ask-fill);color:var(--oa-color-action-ask-label);font:var(--oa-type-ask);padding:12px 18px;border:1px solid var(--oa-component-button-ask-keyline);white-space:nowrap}
.ed .lab{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--oa-color-text-secondary);margin:0 0 6px}
.ed table{border-collapse:collapse;width:100%;font-size:.9375rem;font-variant-numeric:tabular-nums}
.ed th,.ed td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--oa-color-border-hairline)}
.ed thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--oa-color-text-secondary);border-bottom:2px solid var(--oa-color-border-strong)}
.ed .lk{font-family:var(--oa-font-family-quote);font-style:italic}
@media (max-width:47.99em){.ed table.stack,.ed table.stack tbody,.ed table.stack tr,.ed table.stack th,.ed table.stack td{display:block;width:100%;min-width:0}
.ed table.stack thead{display:none}.ed table.stack tr{border-bottom:1px solid var(--oa-color-border-strong);padding:10px 0}
.ed table.stack th,.ed table.stack td{border:0;padding:3px 0}.ed table.stack td[data-k]::before{content:attr(data-k) ": ";font-weight:700}}
"""

PIECE = """
.ed .pc{width:340px;max-width:100%;background:var(--oa-color-surface-newsprint);border-top:4px solid var(--oa-color-border-strong);padding:16px 0 4px}
.ed .pc .kick{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;margin:0 0 10px}
.ed .pc .hl{font:800 1.75rem/1.1 var(--oa-font-family-display);letter-spacing:-.01em;margin:0 0 10px;text-wrap:balance}
.ed .pc .dek{font-size:1.0625rem;line-height:1.5;margin:0 0 12px}
.ed .pc .blk{border-top:1px solid var(--oa-color-border-hairline);padding:10px 0 0;margin:12px 0 0}
.ed .pc .wycd{font:800 1.25rem/1.2 var(--oa-font-family-display);letter-spacing:-.01em;margin:0 0 8px}
.ed .pc .step{margin:0 0 12px}
.ed .pc .by{font:var(--oa-type-caption);color:var(--oa-color-text-secondary);margin:12px 0 0}
"""

ARTICLE = """
.ed .art{max-width:640px;background:var(--oa-color-surface-newsprint)}
.ed .art .kick{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;margin:0 0 12px}
.ed .art .hl{font:800 clamp(1.75rem,1.4rem + 1.4vw,2.5rem)/1.08 var(--oa-font-family-display);letter-spacing:-.015em;margin:0 0 14px;text-wrap:balance}
.ed .art .dek{font-size:1.25rem;line-height:1.5;margin:0 0 18px}
.ed .art .sec{border-top:1px solid var(--oa-color-border-hairline);padding:14px 0 0;margin:18px 0 0}
.ed .art .sec p+p{margin-top:8px}
.ed .art .two{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:16px}
.ed .art .wycd{font:800 1.5rem/1.15 var(--oa-font-family-display);letter-spacing:-.015em;margin:0 0 10px}
.ed .art .step{margin:0 0 10px}
.ed .art .disc{font-size:1rem;border-left:4px solid var(--oa-color-border-strong);padding:4px 0 4px 12px;margin:14px 0}
.ed .art .foot{font:var(--oa-type-caption);color:var(--oa-color-text-secondary);margin-top:18px}
.ed .art .num{display:inline-block;min-width:1.6em;font-weight:700}
"""

PAIR = """
.ed.pair{max-width:760px}
.ed .ex{margin:0;padding:18px 20px;border:1px solid var(--oa-color-border-hairline);background:var(--oa-color-surface-newsprint)}
.ed .ex.after{background:var(--oa-color-surface-white);border-color:var(--oa-color-border-strong)}
.ed .exh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 12px}
.ed .exh .s{font:var(--oa-type-caption);color:var(--oa-color-text-secondary)}
.ed .ex .q{margin:0;font:400 clamp(1.1875rem,1.1rem + .4vw,1.375rem)/1.5 var(--oa-font-family-reading);letter-spacing:-.005em;overflow-wrap:anywhere}
.ed .ex .note{font:var(--oa-type-caption);color:var(--oa-color-text-secondary);margin-top:12px}
.ed .emrule{display:inline-block;width:1em;height:0;border-top:2px solid currentColor;vertical-align:.32em;margin:0 .08em}
.ed del .emrule{height:.47em;vertical-align:-.15em;border-bottom:2px dotted var(--oa-color-graphic-subtle)}
"""

HL = """
.ed .hh{font:800 clamp(1.75rem,1.3rem + 1.8vw,2.5rem)/1.1 var(--oa-font-family-display);letter-spacing:-.012em;color:var(--oa-color-text-primary);margin:0;text-wrap:balance}
.ed .hh .hamp-h{display:inline-block;height:.747em;width:auto;vertical-align:-.01em;color:var(--oa-color-palette-pillar-red)}
"""


def style(*blocks):
    return "<style>" + "".join(blocks) + "</style>"


def hinge():
    """The hinge divider inside a specimen: a hairline broken by ampersand B's 24 px master in the surface's ink."""
    return (f'<div class="hinge" aria-hidden="true"><img data-inline src="{AMP24}" alt="" class="hamp" '
            f'width="21" height="24"></div>')


def amp_h(label="and"):
    """Ampersand B's display master, set at a hinge headline's cap height in the view's working red."""
    return f'<img data-inline src="{AMP_DISPLAY}" alt="{e(label)}" class="hamp-h" data-red="working" data-red-job="headline">'


def ill():
    return '<span class="ill">Illustrative</span>'


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
            interactive=False, exempt=None, height=None, label=None, css=(BASE,)):
        if sid in self.files:
            raise SystemExit(f"duplicate specimen id {sid}")
        self.files[sid] = f"<!-- {sid}: Oath & Action guide, Edition 06, chapter {chapter}. Editor, November 6, 2026. -->\n" \
                          + style(*css) + "\n" + body.strip() + "\n"
        m = {"chapter": chapter, "rule": rule, "width_px": width, "alt": " ".join(alt.split()),
             "illustrative": bool(illustrative), "notes": notes}
        if height:
            m["height_px"] = height
        if surface:
            m["surface"] = surface
        if interactive:
            m["interactive"] = True
        if exempt:
            m["check_exempt"] = exempt
        if label:
            m["label"] = label
        self.manifest[sid] = m
        return sid

    def write(self):
        SPECIMENS.mkdir(parents=True, exist_ok=True)
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
