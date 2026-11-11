"""Chapter 26, Tokens and how to choose them: the chapter file, its specimens and manifest, and the code sets of Rule
26.4's four worked examples.

Usage (from the project folder):
  python3 -I work/build/scripts/phase-2/stage_c_ch26_build.py            write everything below
  python3 -I work/build/scripts/phase-2/stage_c_ch26_build.py --check    fail if any file on disk is not what this script writes now

Reads   work/build/tokens/tokens.json (every value, alias, count and version the chapter prints; each contrast is computed
        here from the hex values with WCAG 2.2's formula, so no figure is typed by hand)
        work/build/assets/utility/svg-24/20261110_Utility-Warning-24px.svg (the warning glyph a code set carries inline)
Writes  work/build/guide/chapters/26-tokens.json
        work/build/guide/specimens/s-26-*.html (all but s-26-token-table, which token_table_build.py writes)
        work/build/guide/specimens/manifest-tokens.json (with the token table's entry)
        work/build/guide/code/c-26-caption, c-26-download, c-26-chart and c-26-warning (.html and .css)

Stage C, round 1, November 11, 2026, by the guide engineer, under 20261111_Stage-C-Round-1-Brief.md (rules 26.1 to 26.8
fixed ahead), DR-214 (tokens.css and tokens.json) and the token architecture, sections 1 to 8. The editor reads the words
afterwards and changes them through this script's data.
"""
import argparse
import html
import importlib.util
import textwrap
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TOKENS = ROOT / "work/build/tokens/tokens.json"
CHAPTER = ROOT / "work/build/guide/chapters/26-tokens.json"
SPEC = ROOT / "work/build/guide/specimens"
MANIFEST = SPEC / "manifest-tokens.json"
CODE = ROOT / "work/build/guide/code"
WARNING_SVG = ROOT / "work/build/assets/utility/svg-24/20261110_Utility-Warning-24px.svg"
# Gate 2 fix pass (CD-M1): Rule 06.1's set is the one set a product loads: Inter 400, 600 and 700; Inter Tight 800; Lora
# Italic 400 and 500. Google serves the same variable files for it (fonts_fetch.py), and the guide carries them itself.
FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800"
         "&family=Lora:ital,wght@1,400;1,500&display=swap")
e = html.escape


# ---------------------------------------------------------------------------------------------------------------
# Tokens: values, aliases and contrast
# ---------------------------------------------------------------------------------------------------------------
TREE = json.loads(TOKENS.read_text())
META = TREE["$extensions"]["org.oathandaction"]
FLAT = {}


def _walk(node, path):
    if isinstance(node, dict):
        if "$value" in node:
            FLAT[".".join(path)] = node
            return
        for k, v in node.items():
            if not k.startswith("$"):
                _walk(v, path + [k])


_walk(TREE, [])


def chain(name):
    """The token and every token it points to, in order."""
    out = [name]
    while isinstance(FLAT[out[-1]]["$value"], str) and FLAT[out[-1]]["$value"].startswith("{") and len(out) < 12:
        out.append(FLAT[out[-1]]["$value"].strip("{}"))
    return out


def hexof(name):
    v = FLAT[chain(name)[-1]]["$value"]
    return (v.get("hex") if isinstance(v, dict) else v).upper()


def css(name):
    """oa.color.text.secondary.onNewsprint -> --oa-color-text-secondary-on-newsprint"""
    return "--" + "-".join(re.sub(r"(?<!^)(?=[A-Z])", "-", seg).lower() for seg in name.split("."))


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def over(fg, alpha, bg):
    """fg at an opacity over bg, as a browser blends it in sRGB."""
    f = [int(fg[i:i + 2], 16) for i in (1, 3, 5)]
    g = [int(bg[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(alpha * a + (1 - alpha) * b):02X}" for a, b in zip(f, g))


def r2(x):
    return f"{x:.2f}"


P = {k: hexof(f"oa.color.palette.{k}") for k in ("newsprint", "white", "charcoal", "prussian", "stone", "pillarRed", "verdigris")}
DEEP, DIM = hexof("oa.color.derived.deepStone"), hexof("oa.color.derived.dimNewsprint")
RED2 = META["held"]["redGraphic"]["hex"].upper()           # the rejected second red
OLD_STONE = "#4E535C"                                       # the gray an older file typed, beside Deep Stone
assert "#" + "".join(f"{round(int(P['stone'][i:i + 2], 16) * 0.84):02X}" for i in (1, 3, 5)) == OLD_STONE   # Stone scaled to 84% in sRGB
F = {
    "ds_n": r2(ratio(DEEP, P["newsprint"])), "stone_n": r2(ratio(P["stone"], P["newsprint"])), "ds_w": r2(ratio(DEEP, P["white"])),
    "op40_w": r2(ratio(over(P["charcoal"], 0.4, P["white"]), P["white"])), "char_n": r2(ratio(P["charcoal"], P["newsprint"])),
    "char_stone": r2(ratio(P["charcoal"], P["stone"])), "red_n": r2(ratio(P["pillarRed"], P["newsprint"])),
    "white_pr": r2(ratio(P["white"], P["prussian"])), "news_pr": r2(ratio(P["newsprint"], P["prussian"])),
    "red_pr": r2(ratio(P["pillarRed"], P["prussian"])), "ds_c": r2(ratio(DEEP, P["charcoal"])), "dim_c": r2(ratio(DIM, P["charcoal"])),
    "ds_pr": r2(ratio(DEEP, P["prussian"])), "red2_n": r2(ratio(RED2, P["newsprint"])), "red_red2": r2(ratio(P["pillarRed"], RED2)),
    "char_c": r2(ratio(P["charcoal"], P["charcoal"])), "news_c": r2(ratio(P["newsprint"], P["charcoal"])),
    "char_n_body": r2(ratio(P["charcoal"], P["newsprint"])),
}
N_TOKENS = len(FLAT)
# the token table's groups, as token_table_build.py makes them (round 2, call 13)
_spec = importlib.util.spec_from_file_location("token_table_build", Path(__file__).with_name("token_table_build.py"))
_tt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tt)
N_GROUPS = len({_tt.group_of(p) for p in FLAT})
N_COLOR_GROUPS = len({_tt.group_of(p) for p in FLAT if p.split(".")[1] == "color"})
N_CHART_GROUPS = len({_tt.group_of(p) for p in FLAT if p.split(".")[1] == "chart"})
WORDS = dict(enumerate(("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")))   # H06
assert _tt.group_of("oa.font.family.reading") == "Type: faces and weights" and _tt.group_of("oa.zIndex.skip") == "Stacking order"
# Deprecated names (DTCG $deprecated, Rule 26.8): each old short name with its new one and the release it leaves with
DEPRECATED = {}
for _p, _t in FLAT.items():
    if "$deprecated" in _t:
        _d = _t["$extensions"]["org.oathandaction"]["deprecated"]
        DEPRECATED.setdefault(css(".".join(_p.split(".")[:-1])), (css(".".join(_d["replacedBy"].strip("{}").split(".")[:-1])), _d["removedIn"], _d["since"]))
CATEGORIES = [k for k in TREE["oa"]]
CAT_WORDS = {"zIndex": "z-index"}
VERSION = META["tokenSetVersion"]
NOTE = META["changeNotes"][0]
STUDIO_CODE = re.compile(r"^(?:(?:DR|D1|D2|G1)-\d+|T-\d+)\s*:\s*")
assert N_TOKENS == 500 or N_TOKENS > 0


MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")


def date_words(iso):
    """2026-11-11 -> November 11, 2026 (H05: dates in words)."""
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{MONTHS[m - 1]} {d}, {y}"


# The head script of Rules 18.4 and 26.6: a stored choice applies before the first paint
HEAD_SCRIPT = ("try { var t = localStorage.getItem('oa-theme'); if (t === 'light' || t === 'dark') "
               "document.documentElement.setAttribute('data-oa-theme', t); } catch (e) {}")


def words_list(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1]


# ---------------------------------------------------------------------------------------------------------------
# Specimens. Each is a fragment the build frames; its <style> applies inside its own frame (the build adds @scope).
# Type uses the token styles that hold one size at every width, so a fixed plate stays on the scale (D2-254).
# ---------------------------------------------------------------------------------------------------------------
BASE = (".sx-k{margin:0;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--oa-color-text-secondary-on-newsprint)}"
        ".sx-p{margin:0;font:var(--oa-type-body)}.sx-s{margin:0;font:var(--oa-type-body-small)}.sx-c{margin:0;font:var(--oa-type-caption)}"
        ".sx-code{display:block;margin:0;padding:12px 16px;background:var(--oa-color-surface-white);color:var(--oa-color-text-primary-on-white);"
        "font-family:ui-monospace,\"SFMono-Regular\",Menlo,Consolas,monospace;font-size:.875rem;line-height:1.6;white-space:pre-wrap;overflow-wrap:anywhere}"
        ".sx-meas{margin:0;padding:12px 16px 16px;font:var(--oa-type-caption);color:var(--oa-color-text-secondary-on-newsprint)}.sx-il{margin:0 0 8px}"
        ".dnp{display:flex;align-items:center;gap:8px;margin:0 0 16px;padding:6px 10px;background:var(--oa-color-action-primary-fill);color:var(--oa-color-text-primary-on-charcoal);"
        "font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase}")
BAND = '<p class="dnp"><span aria-hidden="true">×</span>Failure case: do not publish</p>'
# Round 2 (call 9, D2-1551; CD-S7, BE-S8, CA-S7): an invented piece carries the shell's Illustrative chip at its head,
# under the failure band where it has one, so the caption needs no label of its own.
CHIP = '<p class="sx-il"><span class="illus">Illustrative</span></p>'


def spec(css_text, body):
    return f"<style>{BASE}{css_text}</style>\n{body}\n"


def code(text):
    return f'<code class="sx-code">{hx(e(text, quote=False))}</code>'


def hx(text):
    """A hex value printed as words: the build reads a bare # and six digits as a color the specimen draws."""
    return text.replace("#", "&#35;")


# A bar chart drawn in HTML, so its words stay at their own size at every width. bars: (label, value, kind)
WEEKS = [("Week 1", 120), ("Week 2", 180), ("Week 3", 340), ("Week 4", 150)]
CHART_CSS = (".sx-ch{display:grid;gap:8px;margin:12px 0 0}.sx-row{display:grid;grid-template-columns:4.5rem minmax(0,1fr);align-items:center;gap:8px}"
             ".sx-rl{font:var(--oa-type-data-label)}.sx-track{display:flex;align-items:center;gap:8px;min-width:0}"
             ".sx-bar{height:20px;flex:0 1 auto;min-width:0}.sx-v{flex:none;font:var(--oa-type-data-label);font-variant-numeric:tabular-nums}")


def bars(fill, subject=None, subject_fill=None, attrs=""):
    rows = []
    top = max(v for _, v in WEEKS)
    for i, (lab, v) in enumerate(WEEKS):
        pct = round(v / top * 78)
        f = subject_fill if (subject is not None and i == subject) else fill
        extra = attrs if (subject is not None and i == subject) else ""
        rows.append(f'<div class="sx-row"><span class="sx-rl">{lab}</span><span class="sx-track"><span class="sx-bar" style="width:{pct}%;background:{f}"{extra}></span>'
                    f'<span class="sx-v">{v}</span></span></div>')
    return '<div class="sx-ch" aria-hidden="true">' + "".join(rows) + "</div>"


def specimens():
    S, M = {}, {}

    def add(sid, rule, body, alt, width=None, notes="", illustrative=False, exempt=None, interactive=False):
        if illustrative:
            body = body.replace(BAND, BAND + CHIP, 1) if BAND in body else body.replace("</style>\n", "</style>\n" + CHIP, 1)
        S[sid] = body
        m = {"chapter": "26", "rule": rule, "width_px": width, "alt": alt, "illustrative": illustrative, "notes": notes}
        if exempt:
            m["check_exempt"] = exempt
        if interactive:
            m["interactive"] = True
        M[sid] = m

    ink_n = "var(--oa-color-text-primary-on-newsprint)"
    # The chapter's opener (call 8, D2-1134, D2-1550, CD-S18): the five steps of Rule 26.3 for one caption, as a picture that
    # flows with the column at true size. Short names only, so it follows the page; under 6 KB.
    o_steps = [("Surface", "Charcoal"), ("Role", "Text"), ("Emphasis", "Secondary"), ("State", "None"), ("Component", "None")]
    S["s-26-opener"] = ("<style>.c26o{color:var(--oa-color-text-primary);font:var(--oa-type-body)}.c26o p{margin:0}"
                        ".c26o .c26o-t{font:var(--oa-type-caption);color:var(--oa-color-text-secondary);margin:0 0 8px}"
                        ".c26o-s{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(7.5rem,1fr));gap:8px}"
                        ".c26o-s li{border:1px solid var(--oa-color-border-strong);padding:8px 12px;display:grid;gap:2px;align-content:start}"
                        ".c26o-n{font:var(--oa-type-data-label);color:var(--oa-color-text-secondary)}.c26o-k{font:var(--oa-type-ui);font-weight:var(--oa-font-weight-bold)}"
                        ".c26o-v{font:var(--oa-type-caption)}"
                        ".c26o .c26o-r{margin:12px 0 0;padding:8px 12px;border-left:var(--oa-border-width-bar) solid var(--oa-color-graphic-essential);font:var(--oa-type-ui)}"
                        ".c26o-r code{white-space:nowrap}</style>\n"
                        '<div class="c26o"><p class="c26o-t">Five steps to a token, for a caption on a Charcoal panel</p><ol class="c26o-s">'
                        + "".join(f'<li><span class="c26o-n">{i}</span><span class="c26o-k">{k}</span><span class="c26o-v">{v}</span></li>' for i, (k, v) in enumerate(o_steps, 1))
                        + f'</ol><p class="c26o-r">The token: <code>--oa-color-text-secondary</code>, Dim Newsprint on Charcoal, {F["dim_c"]} to 1</p></div>\n')
    M["s-26-opener"] = {"chapter": "26", "rule": None, "width_px": None,
                        "alt": "The five steps that choose a token, for a caption on a Charcoal panel, in order: surface, Charcoal; role, text; emphasis, secondary; "
                               f"state, none; component, none. They lead to --oa-color-text-secondary, which is Dim Newsprint on Charcoal at {F['dim_c']} to 1.",
                        "illustrative": False,
                        "notes": "Chapter 26's opener (call 8 of the round 2 fix brief, D2-1134, D2-1550, CD-S18): Rule 26.3's five steps on its own worked example, "
                                 "flowing with the column; short names only, so it follows the page's theme. The ratio is computed from tokens.json."}

    # 26.1, the three tiers of one value
    tiers = [("Component", "oa.component.button.disabled.label.onNewsprint", "The label of an unavailable button, on Newsprint."),
             ("Semantic", "oa.color.state.disabled.text.onNewsprint", "Disabled text, on Newsprint."),
             ("Primitive", "oa.color.derived.deepStone", f"Deep Stone, {hx(DEEP)}.")]
    assert chain(tiers[0][1]) == [t[1] for t in tiers], chain(tiers[0][1])
    rows = "".join(f'<li class="sx-t"><p class="sx-k">{k}</p><p class="sx-s"><code>{n}</code></p><p class="sx-s"><code>{css(n)}</code></p>'
                   f'<p class="sx-c sx-job">{j}</p>' + ('<p class="sx-c sx-to">points to</p>' if i < 2 else
                   f'<p class="sx-c sx-sw"><span class="sx-chip" style="background:var({css(n)})"></span>The value itself</p>') + '</li>'
                   for i, (k, n, j) in enumerate(tiers))
    add("s-26-1-correct", "26.1", spec(
        ".sx-tiers{list-style:none;margin:0;padding:0;display:grid;gap:12px}.sx-t{padding:12px 16px;border-left:4px solid var(--oa-color-graphic-essential-on-newsprint);"
        "background:var(--oa-color-surface-white);display:grid;gap:4px}.sx-t code{overflow-wrap:anywhere}.sx-job{color:var(--oa-color-text-secondary-on-white)}"
        ".sx-to{font-weight:var(--oa-font-weight-bold)}.sx-sw{display:flex;align-items:center;gap:8px}.sx-chip{width:24px;height:24px;flex:none;border:1px solid var(--oa-color-border-strong-on-white)}"
        ".sx-out{margin:16px 0 0;display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px}.sx-btn{display:inline-flex;align-items:center;min-height:44px;padding:0 24px;"
        "border:1px dashed var(--oa-component-button-disabled-edge-on-newsprint);color:var(--oa-component-button-disabled-label-on-newsprint);font:var(--oa-type-ui)}",
        f'<ol class="sx-tiers">{rows}</ol><div class="sx-out"><span class="sx-btn">Download the photo</span>'
        f'<p class="sx-c">The label it draws, {F["ds_n"]} to 1 on Newsprint.</p></div>'),
        f"One value in its three tiers, as three linked cards. Component: {tiers[0][1]}, the label of an unavailable button on Newsprint, which points to "
        f"the semantic token {tiers[1][1]}, disabled text on Newsprint, which points to the primitive {tiers[2][1]}, Deep Stone, {DEEP}. Each card gives "
        f"the name in tokens.json and in CSS. Under them, an unavailable Download the photo button with a dashed edge, its label measured at {F['ds_n']} to 1.",
        notes="Names and the alias chain read from tokens.json.")
    add("s-26-1-failure", "26.1", spec(
        ".sx-two{display:grid;grid-template-columns:repeat(auto-fit,minmax(9rem,1fr));gap:12px;margin:12px 0 0}.sx-pane{padding:16px;display:grid;gap:8px}"
        ".sx-pane--n{background:var(--oa-color-surface-newsprint);border:1px solid var(--oa-color-border-hairline-on-newsprint)}.sx-pane--c{background:var(--oa-color-surface-charcoal)}"
        ".sx-lab{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border:1px dashed currentColor;font:var(--oa-type-ui);color:var(--oa-color-derived-deep-stone)}"
        ".sx-pane--c .sx-c{color:var(--oa-color-text-secondary-on-charcoal)}",
        f'{BAND}{code(".download-button[aria-disabled=true] {" + chr(10) + "  color: var(--oa-color-derived-deep-stone);" + chr(10) + "}")}'
        f'<div class="sx-two"><div class="sx-pane sx-pane--n"><span class="sx-lab">Download the photo</span><p class="sx-c">On Newsprint: {F["ds_n"]} to 1</p></div>'
        f'<div class="sx-pane sx-pane--c"><span class="sx-lab">Download the photo</span><p class="sx-c">In the dark theme: {F["ds_c"]} to 1</p></div></div>'),
        f"A line of CSS that colors an unavailable button's label with the primitive Deep Stone, then the same button twice: on Newsprint its label measures "
        f"{F['ds_n']} to 1; in the dark theme, on Charcoal, the primitive stays Deep Stone and the label all but disappears, at {F['ds_c']} to 1.",
        exempt=["contrast"], notes="A labeled failure: the label on Charcoal fails on purpose.")

    # 26.2, the five conditions, met and failed
    need = META["needs"]["N-01"]
    ok = '<span class="sx-yes">Met</span>'
    no = '<span class="sx-no"><span aria-hidden="true">× </span>Fails</span>'
    card_css = (".sx-card{background:var(--oa-color-surface-white);color:var(--oa-color-text-primary-on-white);padding:16px}.sx-head{display:flex;align-items:center;gap:12px;margin:0 0 12px}"
                ".sx-chip{width:40px;height:40px;flex:none}.sx-name{margin:0;font:var(--oa-type-ui);font-weight:var(--oa-font-weight-bold)}"
                ".sx-cond{list-style:none;margin:0;padding:0;display:grid;gap:8px;counter-reset:c}.sx-cond li{display:grid;grid-template-columns:2rem minmax(0,1fr) auto;gap:8px;"
                "align-items:start;padding-top:8px;border-top:1px solid var(--oa-color-border-hairline-on-white);counter-increment:c}"
                ".sx-cond li::before{content:counter(c);font:var(--oa-type-data-label)}.sx-yes,.sx-no{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);"
                "text-transform:uppercase}.sx-no{border-bottom:2px solid currentColor}.sx-cond .sx-c{color:var(--oa-color-text-secondary-on-white)}")

    def cond(rows):
        return '<ol class="sx-cond">' + "".join(f'<li><span><span class="sx-s">{a}</span><br><span class="sx-c">{b}</span></span>{m}</li>' for a, b, m in rows) + "</ol>"

    add("s-26-2-correct", "26.2", spec(card_css,
        f'<div class="sx-card"><div class="sx-head"><span class="sx-chip" style="background:var(--oa-color-derived-deep-stone)"></span>'
        f'<p class="sx-name">Deep Stone, {hx(DEEP)}</p></div>' + cond([
            ("A measured need", f"Stone measures {F['stone_n']} to 1 for small secondary text on Newsprint, under 4.5, and the fifth edition's census counted 49 such failures.", ok),
            ("One palette color, mixed and recorded", "Stone mixed 18 percent toward Charcoal in OKLab.", ok),
            ("One job", "Secondary and disabled text on Newsprint and White.", ok),
            ("Contrast where it serves", f"{F['ds_n']} to 1 on Newsprint and {F['ds_w']} on White, where text needs 4.5.", ok),
            ("Description, tier and status", "In tokens.json with its description, the primitive tier and the status adopted.", ok)]) + "</div>"),
        f"The record of Deep Stone, {DEEP}, against the five conditions, each marked Met: the need (Stone measures {F['stone_n']} to 1 for small secondary text on "
        f"Newsprint, 49 failures counted), the value (Stone mixed 18 percent toward Charcoal in OKLab), one job (secondary and disabled text on Newsprint and White), "
        f"its contrast ({F['ds_n']} to 1 on Newsprint, {F['ds_w']} on White) and its description, tier and status.",
        notes=f"From tokens.json: the need register's N-01 ({need[:60]}...), the derivation and the stored contrast; ratios recomputed here.")
    add("s-26-2-failure", "26.2", spec(card_css + ".sx-pair{display:flex;gap:4px}",
        f'<div class="sx-card"><div class="sx-head"><span class="sx-pair"><span class="sx-chip" style="background:var(--oa-color-palette-pillar-red)" data-red="signature"></span>'
        f'<span class="sx-chip" style="background:{RED2}" data-red="signature"></span></span><p class="sx-name">A second red for marks, {hx(RED2)}</p></div>' + cond([
            ("A measured need", "None: Pillar Red with its 1 px Charcoal keyline already draws marks on Newsprint.", no),
            ("One palette color, mixed and recorded", f"A red of its own, {r2(ratio(P['pillarRed'], RED2))} to 1 from Pillar Red, so a reader cannot tell the two apart.", no),
            ("One job", "Marks, the job Pillar Red already holds.", no),
            ("Contrast where it serves", f"{F['red2_n']} to 1 on Newsprint, over the 3 to 1 a mark needs.", ok),
            ("Description, tier and status", "Recorded as rejected, and never used.", ok)]) + "</div>"),
        f"The record of a proposed second red, {RED2}, shown beside Pillar Red, against the five conditions. It fails three: no measured need, since Pillar Red with "
        f"its keyline already draws marks; a red of its own that measures {r2(ratio(P['pillarRed'], RED2))} to 1 from Pillar Red, so the two cannot be told apart; and a "
        f"job Pillar Red already holds. It meets the contrast condition at {F['red2_n']} to 1 on Newsprint.",
        exempt=["red", "literal"], notes="The rejected value from tokens.json's held list, which no token holds, so its swatch is a literal. Two reds side by side on purpose.")

    # 26.3, five steps, and a skipped first step
    steps = [("Surface", "Charcoal"), ("Role", "Text"), ("Emphasis", "Secondary"), ("State", "None"), ("Component", "None")]
    strip = '<ol class="sx-steps">' + "".join(f'<li><span class="sx-n">{i}</span><span class="sx-s"><strong>{a}</strong><br>{b}</span></li>' for i, (a, b) in enumerate(steps, 1)) + "</ol>"
    steps_css = (".sx-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(6.5rem,1fr));gap:8px}"
                 ".sx-steps li{display:flex;gap:8px;align-items:flex-start;padding:8px;background:var(--oa-color-surface-white);color:var(--oa-color-text-primary-on-white)}"
                 ".sx-n{font:var(--oa-type-data-label);flex:none}.sx-res{margin:12px 0 0;padding:16px}.sx-res .sx-s code{overflow-wrap:anywhere}")
    add("s-26-3-correct", "26.3", spec(steps_css + ".sx-res{background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal)}"
                                       ".sx-cap{margin:8px 0 0;font:var(--oa-type-caption);color:var(--oa-color-text-secondary-on-charcoal)}",
        f'{strip}<div class="sx-res"><p class="sx-s">The token: <code>--oa-color-text-secondary</code> inside <code>.oa-surface-charcoal</code>, which is '
        f'<code>--oa-color-text-secondary-on-charcoal</code>, Dim Newsprint.</p><p class="sx-cap">A caption set with it: {F["dim_c"]} to 1 on Charcoal.</p></div>'),
        f"The five steps for a caption on a Charcoal panel, in order: surface Charcoal, role text, emphasis secondary, state none, component none. Under them, on "
        f"Charcoal, the token they reach, --oa-color-text-secondary inside .oa-surface-charcoal, which is Dim Newsprint, and a caption set with it at {F['dim_c']} to 1.")
    add("s-26-3-failure", "26.3", spec(steps_css + ".sx-res{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian)}"
                                       ".sx-cap{margin:8px 0 0;font:var(--oa-type-caption);color:var(--oa-color-derived-deep-stone)}"
                                       ".sx-skip li:first-child{text-decoration:line-through}",
        f'<div class="sx-skip">{strip.replace("<strong>Surface</strong><br>Charcoal", "<strong>Surface</strong><br>Skipped")}</div><div class="sx-res">'
        f'<p class="sx-s">The token taken from another page: <code>--oa-color-text-secondary-on-newsprint</code>, Deep Stone, on a Prussian panel.</p>'
        f'<p class="sx-cap">A caption set with it: {F["ds_pr"]} to 1 on Prussian.</p></div>'),
        f"The five steps with the first one, the surface, skipped and struck through. On a Prussian panel, a caption takes the secondary text token for Newsprint, "
        f"Deep Stone, and measures {F['ds_pr']} to 1, far under the 4.5 to 1 text needs.",
        exempt=["contrast"], notes="A labeled failure: the caption on Prussian fails on purpose.")

    # 26.4, the four worked examples
    fig_css = (".sx-fig{margin:0;padding:16px;background:var(--oa-color-surface-newsprint)}.sx-ttl{margin:0;font:var(--oa-type-ui);font-weight:var(--oa-font-weight-bold)}"
               + CHART_CSS)
    for kind, color, ratio_txt in (("correct", "var(--oa-color-text-secondary-on-newsprint)", F["ds_n"]), ("failure", "var(--oa-color-palette-stone)", F["stone_n"])):
        body = (BAND if kind == "failure" else "") + (
            f'<figure class="sx-fig"><p class="sx-ttl">Comments on the transit plan, by week</p>{bars(ink_n)}'
            f'<figcaption class="sx-cap" style="margin:12px 0 0;font:var(--oa-type-caption);color:{color}">Comments counted each week, Monday to Sunday.</figcaption></figure>'
            f'<p class="sx-meas">Caption: {"Deep Stone" if kind == "correct" else "Stone"}, {ratio_txt} to 1 on Newsprint.</p>')
        add(f"s-26-4-1-{kind}", "26.4", spec(fig_css, body),
            ("A small bar chart titled Comments on the transit plan, by week, four weeks of illustrative counts, with its caption under it in Deep Stone at "
             f"{F['ds_n']} to 1 on Newsprint." if kind == "correct" else
             "Failure case: do not publish. The same chart with its caption in Stone, which measures "
             f"{F['stone_n']} to 1 on Newsprint, under the 4.5 to 1 small text needs."),
            width=360, illustrative=True, exempt=None if kind == "correct" else ["contrast"],
            notes="Illustrative counts. " + ("" if kind == "correct" else "A labeled failure: the caption fails on purpose."))
    dl_css = (".sx-w{padding:24px 16px;background:var(--oa-color-surface-white);color:var(--oa-color-text-primary-on-white)}"
              ".sx-file{margin:0 0 12px;font:var(--oa-type-ui);font-weight:var(--oa-font-weight-bold)}.sx-btn{display:inline-flex;align-items:center;box-sizing:border-box;max-width:100%;min-height:44px;padding:8px 24px;font:var(--oa-type-ui)}"
              ".sx-why{margin:8px 0 0;font:var(--oa-type-caption);color:var(--oa-color-text-secondary-on-white)}")
    add("s-26-4-2-correct", "26.4", spec(dl_css + ".sx-on{border:1px dashed var(--oa-component-button-disabled-edge-on-white);color:var(--oa-component-button-disabled-label-on-white)}",
        f'<div class="sx-w"><p class="sx-file">Hearing photo, Capitol steps</p><span class="sx-btn sx-on">Download the photo</span>'
        f'<p class="sx-why">Choose a size to download.</p></div><p class="sx-meas">Label and dashed edge: Deep Stone, {F["ds_w"]} to 1 on White.</p>'),
        f"On White, an unavailable button, Download the photo, with a dashed edge and its label in Deep Stone at {F['ds_w']} to 1, and under it the reason: "
        "Choose a size to download.", width=360, illustrative=True, notes="Illustrative file name.")
    add("s-26-4-2-failure", "26.4", spec(dl_css + ".sx-off{background:var(--oa-color-palette-charcoal);color:var(--oa-color-palette-white);opacity:.4}",
        f'{BAND}<div class="sx-w"><p class="sx-file">Hearing photo, Capitol steps</p><span class="sx-btn sx-off">Download the photo</span></div>'
        f'<p class="sx-meas">The whole button at 40 percent opacity: its fill measures {F["op40_w"]} to 1 on White, and no line says why it waits.</p>'),
        f"Failure case: do not publish. On White, the same button faded to 40 percent opacity, its fill measuring {F['op40_w']} to 1, with no reason line, so a reader "
        "cannot tell it is unavailable or what would make it work.",
        width=360, illustrative=True, exempt=["contrast"], notes="A labeled failure: faded on purpose.")
    hl_css = fig_css + ".sx-head{margin:0;font:var(--oa-type-ui);font-weight:var(--oa-font-weight-bold)}"
    add("s-26-4-3-correct", "26.4", spec(hl_css,
        f'<figure class="sx-fig"><p class="sx-head">Week 3 drew the most comments</p>'
        f'{bars("var(--oa-color-data-context-on-newsprint)", 2, "var(--oa-color-data-emphasis-on-newsprint)")}</figure>'
        f'<p class="sx-meas">Week 3 in Charcoal, {F["char_n"]} to 1; the other weeks in Stone, {F["stone_n"]} to 1; the two inks differ by {F["char_stone"]} to 1.</p>'),
        f"A bar chart headed Week 3 drew the most comments, with illustrative counts. The week 3 bar is Charcoal at {F['char_n']} to 1 on Newsprint and the others are "
        f"Stone at {F['stone_n']} to 1; the two inks differ by {F['char_stone']} to 1, and every bar carries its count beside it.",
        width=360, illustrative=True, notes="Illustrative counts.")
    add("s-26-4-3-failure", "26.4", spec(hl_css + ".sx-err{margin:0 0 12px;padding:8px 12px;border-left:4px solid var(--oa-color-palette-pillar-red);background:var(--oa-color-derived-error-band);"
                                          "font:var(--oa-type-body-small);color:var(--oa-color-text-primary-on-newsprint)}",
        f'{BAND}<figure class="sx-fig"><p class="sx-err" data-red="working" data-red-job="error"><strong>Error:</strong> The count for week 4 is missing a day.</p>'
        f'<p class="sx-head">Week 3 drew the most comments</p>'
        f'{bars("var(--oa-color-data-context-on-newsprint)", 2, "var(--oa-color-palette-pillar-red)", " data-red=\"working\" data-red-job=\"point\"")}</figure>'
        f'<p class="sx-meas">Week 3 in Pillar Red with no keyline, {F["red_n"]} to 1 on Newsprint, beside an error that already holds the red.</p>'),
        f"Failure case: do not publish. The same chart under an error message with a red bar, and the week 3 bar in Pillar Red with no keyline, {F['red_n']} to 1 on "
        "Newsprint, so the view gives red two jobs and the highlight reads as part of the error.",
        width=360, illustrative=True, exempt=["red", "contrast"], notes="A labeled failure: two red jobs on purpose.")
    warn_css = (".sx-pr{padding:16px;background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian)}"
                ".sx-step{margin:0 0 12px;font:var(--oa-type-ui);font-weight:var(--oa-font-weight-bold)}.sx-warn{display:flex;gap:8px;align-items:flex-start;margin:0;padding-left:12px;font:var(--oa-type-body-small)}"
                ".sx-ic{flex:none;width:24px;height:24px}")
    add("s-26-4-4-correct", "26.4", spec(warn_css + ".sx-warn{border-left:4px solid var(--oa-color-state-warning-mark-on-prussian);color:var(--oa-color-state-warning-text-on-prussian)}"
                                         ".sx-ic{color:var(--oa-color-state-warning-mark-on-prussian)}",
        f'<div class="sx-pr"><p class="sx-step">Step 2 of 6: Hearing</p><p class="sx-warn">'
        f'<svg class="sx-ic" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="U-warning" data-icon-family="utility"><use href="#oa-sym-u-warning-24px"/></svg>'
        f'<span><strong>Warning:</strong> The committee moved the hearing to March 12. Check the new date before you travel.</span></p></div>'
        f'<p class="sx-meas">Words in White, {F["white_pr"]} to 1; the bar and triangle in Newsprint, {F["news_pr"]} to 1.</p>'),
        f"On a Prussian tracker panel, Step 2 of 6: Hearing, then a warning with a 4 px Newsprint bar, the warning triangle in Newsprint at {F['news_pr']} to 1 "
        f"and the words in White at {F['white_pr']} to 1: Warning: The committee moved the hearing to March 12. Check the new date before you travel.",
        width=360, illustrative=True, notes="Illustrative date.")
    add("s-26-4-4-failure", "26.4", spec(warn_css + ".sx-warn{padding-left:0;color:var(--oa-color-palette-pillar-red)}",
        f'{BAND}<div class="sx-pr"><p class="sx-step">Step 2 of 6: Hearing</p><p class="sx-warn" data-red="working" data-red-job="error">'
        f'<span>The committee moved the hearing to March 12. Check the new date before you travel.</span></p></div>'
        f'<p class="sx-meas">Words in Pillar Red on Prussian, {F["red_pr"]} to 1, with no word and no mark.</p>'),
        f"Failure case: do not publish. The same panel with the warning set in Pillar Red on Prussian at {F['red_pr']} to 1, with no triangle, no bar and no word "
        "Warning, so only color says it matters, in a red that never sits on Prussian.",
        width=360, illustrative=True, exempt=["red", "contrast"], notes="A labeled failure: red on Prussian on purpose.")

    # 26.5, a page started from tokens.css. Round 2: the head script first, for a product with the theme switch (PP-S6), and
    # the frame drawn and named as the browser window's edge, so the 0 margin reads as intended (CD-S14)
    head = ("<!-- For a product with the theme switch (Rule 18.4): -->\n<script>\n  " + HEAD_SCRIPT + "\n</script>\n"
            f'<meta name="color-scheme" content="light dark">\n<link rel="stylesheet" href="{FONTS}">\n'
            '<link rel="stylesheet" href="tokens.css">\n<style>\n  body { margin: 0; font: var(--oa-type-body) }\n</style>')
    page_css = (".sx-pg{margin:12px 0 0;border:2px solid var(--oa-color-border-strong-on-newsprint);background:var(--oa-color-surface-newsprint)}"
                ".sx-bar2{margin:0;padding:6px 12px;background:var(--oa-color-surface-white);border-bottom:2px solid var(--oa-color-border-strong-on-newsprint);"
                "font:var(--oa-type-caption);color:var(--oa-color-text-secondary-on-white)}")
    para = "A regulator approves the rate you pay for water. You can comment before the board votes."
    add("s-26-5-correct", "26.5", spec(page_css + ".sx-in{margin:0;padding:0}.sx-in p{margin:0;font:var(--oa-type-body)}",
        f'<p class="sx-k">In the head</p>{code(head)}<div class="sx-pg"><p class="sx-bar2">Browser window. The frame is its edge, and the text starts there.</p>'
        f'<div class="sx-in"><p>{para}</p></div></div>'),
        "The lines a page's head needs: for a product with the theme switch, the head script first; then the color scheme meta tag, the brand's fonts from "
        "Google Fonts, tokens.css, and the body rule margin 0 with the body type. Under them, a browser window drawn as a frame, and the page inside it: a "
        "sentence in Inter at 17 px that starts at the window's edge, with no margin.")
    add("s-26-5-failure", "26.5", spec(page_css + ".sx-in{margin:0;padding:8px}.sx-in p{margin:0;font:400 16px/normal Georgia,\"Times New Roman\",serif}",
        f'{BAND}<p class="sx-k">In the head</p>{code(head.split(chr(10) + "<style>")[0])}<div class="sx-pg"><p class="sx-bar2">Browser window. The frame is its edge.</p>'
        f'<div class="sx-in"><p>{para}</p></div></div>'),
        "The same head with the body rule left out, and the page it draws in a browser window drawn as a frame: the sentence in the browser's own serif at "
        "16 px, 8 px in from the window's edge, so no component sits where its code says.",
        exempt=["scale"], notes="A labeled failure: the browser's default type, off the scale on purpose.")

    # 26.6, one component in both themes, and one pinned to Newsprint
    th_css = (".sx-two{display:grid;grid-template-columns:repeat(auto-fit,minmax(12rem,1fr));gap:12px;margin:12px 0 0}"
              ".sx-th{padding:16px;background:var(--oa-color-surface);color:var(--oa-color-text-primary);display:grid;gap:8px}"
              ".sx-th .sx-c{color:var(--oa-color-text-secondary)}.sx-fld{display:flex;align-items:center;min-height:44px;padding:0 12px;"
              "background:var(--oa-color-field-ground);border:1px solid var(--oa-color-border-strong);font:var(--oa-type-ui);color:var(--oa-color-text-secondary)}"
              ".sx-th code{white-space:nowrap}.sx-nm{margin:0;font:var(--oa-type-caption);color:var(--oa-color-text-secondary);display:grid;gap:2px}")

    def themed(theme, label):
        return (f'<div class="sx-th" data-oa-theme="{theme}"><p class="sx-k" style="color:var(--oa-color-text-secondary)">{label}</p>'
                f'<p class="sx-s"><strong>Water rate hearing</strong></p><p class="sx-c">Board of Public Utilities, March 12</p>'
                f'<span class="sx-fld">Your email address</span><p class="sx-nm"><code>--oa-color-surface</code><code>--oa-color-field-ground</code></p></div>')
    add("s-26-6-correct", "26.6", spec(th_css,
        f'{code("<html data-oa-theme=" + chr(34) + "device" + chr(34) + ">")}<div class="sx-two">{themed("light", "Light: Newsprint")}{themed("dark", "Dark: Charcoal")}</div>'),
        f"One card drawn twice from the same short names, once in the light theme on Newsprint and once in the dark theme on Charcoal: the title Water rate hearing, "
        f"the line Board of Public Utilities, March 12, and an entry box for an email address on its field ground. Every word passes in both: secondary text measures "
        f"{F['ds_n']} to 1 on Newsprint and {F['dim_c']} on Charcoal.", illustrative=True, notes="Illustrative hearing.")
    add("s-26-6-failure", "26.6", spec(th_css + ".sx-pin{padding:16px;background:var(--oa-color-surface);color:var(--oa-color-text-primary-on-newsprint);display:grid;gap:8px}"
                                       ".sx-pin .sx-c{color:var(--oa-color-text-secondary-on-newsprint)}",
        f'{BAND}{code(".card { color: var(--oa-color-text-primary-on-newsprint) }")}<div class="sx-two"><div class="sx-pin" data-oa-theme="dark">'
        f'<p class="sx-s"><strong>Water rate hearing</strong></p><p class="sx-c">Board of Public Utilities, March 12</p></div></div>'
        f'<p class="sx-meas">In the dark theme the card takes Charcoal, and its words stay Charcoal: {F["char_c"]} to 1.</p>'),
        f"A card whose words name the Newsprint text token, drawn in the dark theme: its ground follows the theme to Charcoal while its words stay Charcoal, so the "
        f"title and line measure {F['char_c']} to 1 and cannot be read.", illustrative=True, exempt=["contrast"],
        notes="A labeled failure: unreadable on purpose.")

    # 26.7, a value typed in place of a name
    add("s-26-7-failure", "26.7", spec(
        ".sx-two{display:flex;flex-wrap:wrap;gap:16px;margin:12px 0 0}.sx-sw{display:flex;align-items:center;gap:8px}.sx-chip{width:40px;height:40px;flex:none}",
        f'{code(".caption { color: " + OLD_STONE + " }")}<div class="sx-two"><p class="sx-sw sx-c"><span class="sx-chip" style="background:color-mix(in srgb, var(--oa-color-palette-stone) 84%, black)"></span>Typed: {hx(OLD_STONE)}</p>'
        f'<p class="sx-sw sx-c"><span class="sx-chip" style="background:var(--oa-color-derived-deep-stone)"></span>Deep Stone: {hx(DEEP)}</p></div>'
        f'<p class="sx-meas">One digit apart today. When Deep Stone changes in a release, the typed gray stays behind.</p>'),
        f"A line of CSS that types the gray {OLD_STONE} from an old file where Deep Stone's name belongs, and the two swatches side by side: {OLD_STONE} and Deep "
        f"Stone, {DEEP}, one digit apart. A release that changes Deep Stone never reaches the typed value.")

    # 26.8, a change note, and a rename with no alias
    reason = STUDIO_CODE.sub("", NOTE["reason"])
    reason = reason[0].upper() + reason[1:]
    rows = [("Version", f"<code>{e(NOTE['version'])}</code>"), ("Date", date_words(NOTE["date"])),
            ("Tokens", e(NOTE["tokens"])), ("Change", e(NOTE["change"])), ("Why", e(reason))]
    add("s-26-8-correct", "26.8", spec(
        ".sx-note{margin:0;padding:16px;background:var(--oa-color-surface-white);color:var(--oa-color-text-primary-on-white);display:grid;grid-template-columns:5.5rem minmax(0,1fr);gap:8px 12px}"
        ".sx-note dt{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--oa-color-text-secondary-on-white)}"
        ".sx-note dd{margin:0;font:var(--oa-type-body-small);overflow-wrap:anywhere}",
        '<dl class="sx-note">' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in rows) + "</dl>"),
        f"The change note of version {NOTE['version']}, as tokens.json records it. Date: {date_words(NOTE['date'])}. Tokens: {NOTE['tokens']}. "
        f"Change: {NOTE['change']} Why: {reason}", notes="The newest change note in tokens.json, read at build.")
    add("s-26-8-failure", "26.8", spec(
        ".sx-two{display:grid;grid-template-columns:repeat(auto-fit,minmax(12rem,1fr));gap:12px;margin:12px 0 0}.sx-v{padding:16px;background:var(--oa-color-surface-newsprint);"
        "border:1px solid var(--oa-color-border-hairline-on-newsprint);display:grid;gap:8px}.sx-v p{margin:0}.sx-cap1{font:var(--oa-type-caption);color:var(--oa-color-text-secondary-on-newsprint)}"
        ".sx-cap2{font:var(--oa-type-caption);color:var(--oa-color-text-primary-on-newsprint)}",
        f'{code("6.0.0   --oa-color-text-secondary" + chr(10) + "6.1.0   --oa-color-text-quiet   (renamed, no alias, no note)")}'
        '<div class="sx-two"><div class="sx-v"><p class="sx-k">With 6.0.0</p><p class="sx-s">Water rates rise in May.</p><p class="sx-cap1">Source: the city budget, page 14.</p></div>'
        '<div class="sx-v"><p class="sx-k">With 6.1.0</p><p class="sx-s">Water rates rise in May.</p><p class="sx-cap2">Source: the city budget, page 14.</p></div></div>'
        '<p class="sx-meas">The caption reads a name that no longer exists, so it falls back to the body\'s ink, and nothing warns.</p>'),
        "Two versions of a made-up release: in 6.0.0 the secondary text token, and in 6.1.0 the same token renamed with no alias and no change note. Beside them the "
        "same sentence and source caption twice: with 6.0.0 the caption is gray, with 6.1.0 it falls back to the body's ink, since the name it reads no longer exists.",
        illustrative=True, notes="Illustrative release and caption.")

    # 26.7's table, written by token_table_build.py
    M["s-26-token-table"] = {"chapter": "26", "rule": "26.7", "interactive": True, "fit_switch": False, "breakout": True,
                             "alt": "Every token in tokens.json, in groups by category, each closed until opened, under a search field and a list of the groups. Each row gives a token's name, CSS name, value, use, tier and contrast."}
    return S, M


# ---------------------------------------------------------------------------------------------------------------
# Code sets for Rule 26.4's examples: plain HTML and CSS that read only tokens.css, by short name, with a surface class
# where the example names a surface (Rule 26.3's first step)
# ---------------------------------------------------------------------------------------------------------------
def css_lines(text):
    """Compact CSS as a builder reads it best (CA-S2, call 16): one declaration per line, each rule's close on its own line,
    comments kept as written, an @media block's rules indented inside it."""
    out, i, depth = [], 0, 0
    pad = lambda: "  " * depth
    while i < len(text):
        if text.startswith("/*", i):
            j = text.index("*/", i) + 2
            words = " ".join(text[i + 2:j - 2].split())
            lines = textwrap.wrap(words, 76, initial_indent="/* ", subsequent_indent="   ")
            lines[-1] += " */"
            out += [pad() + x for x in lines]
            i = j
            continue
        if text[i] in " \n":
            i += 1
            continue
        if text[i] == "}":
            depth -= 1
            out.append(pad() + "}")
            i += 1
            continue
        j = text.index("{", i)
        head = " ".join(text[i:j].split())
        if head.startswith("@"):
            out.append(f"{pad()}{head} {{")
            depth += 1
            i = j + 1
            continue
        k = text.index("}", j)
        decls = [d.strip() for d in text[j + 1:k].split(";") if d.strip()]
        out.append(f"{pad()}{head} {{")
        out += [f"{pad()}  {' '.join(d.split())};" for d in decls]
        out.append(f"{pad()}}}")
        i = k + 1
    return "\n".join(out) + "\n"


def chip_css(cls):
    """The Illustrative chip at the head of a set's piece, in the set's own CSS, as chapter 18's sets draw it."""
    return (f".{cls} {{ display: inline-block; margin: 0 0 var(--oa-space-100); padding: 0 .4em; border: var(--oa-border-width-hairline) solid currentColor; "
            f"color: var(--oa-color-text-primary); font: var(--oa-type-label); letter-spacing: var(--oa-type-label-letter-spacing); "
            f"text-transform: var(--oa-type-label-text-transform); line-height: 1.5 }}\n")


def code_sets():
    w = WARNING_SVG.read_text()
    inner = re.sub(r"<!--.*?-->", "", w[re.search(r"<svg\b[^>]*>", w).end():w.rindex("</svg>")], flags=re.S).strip()
    inner = re.sub(r">\s+<", "><", inner)
    top = max(v for _, v in WEEKS)
    # one element to a line (call 16): a grid or flex parent ignores the white space between its children
    week_rows = lambda cls: "\n".join(
        f'    <li class="{cls}-row{f" {cls}-row--subject" if i == 2 and cls == "oa-ex-bars" else ""}">\n'
        f'      <span class="{cls}-label">{lab}</span>\n      <span class="{cls}-track">\n'
        f'        <span class="{cls}-bar {cls}-bar--{i + 1}"></span>\n        <span class="{cls}-value">{v}</span>\n      </span>\n    </li>'
        for i, (lab, v) in enumerate(WEEKS))
    widths = lambda cls: "\n".join(f".{cls}-bar--{i + 1} {{ width: {round(v / top * 78)}% }}" for i, (_, v) in enumerate(WEEKS))
    chart_css = lambda cls: (
        f".{cls}-rows {{ display: grid; gap: var(--oa-space-100); margin: var(--oa-space-150) 0 0; padding: 0; list-style: none }}\n"
        f".{cls}-row {{ display: grid; grid-template-columns: 4.5rem minmax(0, 1fr); align-items: center; gap: var(--oa-space-100) }}\n"
        f".{cls}-label, .{cls}-value {{ font: var(--oa-type-data-label); font-variant-numeric: tabular-nums }}\n"
        f".{cls}-track {{ display: flex; align-items: center; gap: var(--oa-space-100); min-width: 0 }}\n"
        f".{cls}-bar {{ flex: 0 1 auto; min-width: 0; height: 1.25rem }}\n.{cls}-value {{ flex: none }}\n{widths(cls)}\n")
    sets = {}
    sets["c-26-caption"] = {
        "html": ('<figure class="oa-ex-figure">\n  <p class="oa-ex-figure-illus">Illustrative</p>\n  <p class="oa-ex-figure-title">Comments on the transit plan, by week</p>\n'
                 '  <ul class="oa-ex-figure-rows" aria-label="Comments by week">\n' + week_rows("oa-ex-figure") + '\n  </ul>\n'
                 '  <figcaption class="oa-ex-figure-caption">Comments counted each week, Monday to Sunday.</figcaption>\n</figure>\n'),
        "css": ("/* A caption under a chart: surface from the page, role text, emphasis secondary, no state, no component token.\n"
                "   On Newsprint it measures " + F["ds_n"] + " to 1; in the dark theme, on Charcoal, " + F["dim_c"] + " to 1. */\n"
                ".oa-ex-figure { margin: 0; font: var(--oa-type-body); color: var(--oa-color-text-primary) }\n"
                + chip_css("oa-ex-figure-illus") + ".oa-ex-figure-title { margin: 0; font: var(--oa-type-ui); font-weight: var(--oa-font-weight-bold) }\n"
                + chart_css("oa-ex-figure") + ".oa-ex-figure-bar { background: var(--oa-color-graphic-essential) }\n"
                ".oa-ex-figure-caption { margin: var(--oa-space-150) 0 0; font: var(--oa-type-caption); color: var(--oa-color-text-secondary) }\n")}
    sets["c-26-download"] = {
        "html": ('<div class="oa-surface-white oa-ex-download">\n  <p class="oa-ex-download-illus">Illustrative</p>\n  <p class="oa-ex-download-file">Hearing photo, Capitol steps</p>\n'
                 '  <button type="button" class="oa-ex-download-button" aria-disabled="true"\n    aria-describedby="oa-ex-download-why">Download the photo</button>\n'
                 '  <p class="oa-ex-download-why" id="oa-ex-download-why">Choose a size to download.</p>\n</div>\n'),
        "css": ("/* A download button that waits for a choice: surface White (the class on the block), role action, state disabled,\n"
                "   then the button's own component tokens, which win. The label and dashed edge measure " + F["ds_w"] + " to 1 on White.\n"
                "   The button keeps focus and points to its reason, so a keyboard reader learns why it waits. */\n"
                ".oa-ex-download { padding: var(--oa-space-300) var(--oa-space-200); background: var(--oa-color-surface); color: var(--oa-color-text-primary); font: var(--oa-type-body) }\n"
                + chip_css("oa-ex-download-illus") + ".oa-ex-download-file { margin: 0 0 var(--oa-space-150); font: var(--oa-type-ui); font-weight: var(--oa-font-weight-bold) }\n"
                ".oa-ex-download-button { display: inline-flex; align-items: center; box-sizing: border-box; max-width: 100%; min-height: var(--oa-size-target-touch); margin: 0;\n"
                "  padding: var(--oa-space-100) var(--oa-space-300); text-align: start;\n"
                "  border: var(--oa-border-width-hairline) solid var(--oa-component-button-primary-fill); border-radius: 0;\n"
                "  background: var(--oa-component-button-primary-fill); color: var(--oa-component-button-primary-label); font: var(--oa-type-ui); cursor: pointer }\n"
                ".oa-ex-download-button[aria-disabled=\"true\"] { border-style: dashed; border-color: var(--oa-component-button-disabled-edge);\n"
                "  background: transparent; color: var(--oa-component-button-disabled-label); cursor: not-allowed }\n"
                ".oa-ex-download-button:focus-visible { outline: var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring); outline-offset: var(--oa-border-focus-offset) }\n"
                ".oa-ex-download-why { margin: var(--oa-space-100) 0 0; font: var(--oa-type-caption); color: var(--oa-color-text-secondary) }\n"
                "@media (forced-colors: active) {\n  .oa-ex-download-button { border-color: ButtonText }\n"
                "  .oa-ex-download-button[aria-disabled=\"true\"] { border-color: GrayText; color: GrayText }\n}\n")}
    sets["c-26-chart"] = {
        "html": ('<figure class="oa-ex-bars">\n  <p class="oa-ex-bars-illus">Illustrative</p>\n  <p class="oa-ex-bars-head">Week 3 drew the most comments</p>\n'
                 '  <ul class="oa-ex-bars-rows" aria-label="Comments by week">\n' + week_rows("oa-ex-bars") + '\n  </ul>\n</figure>\n'),
        "css": ("/* A highlighted bar: surface from the page, role data, emphasis on the bar the headline names, context on the rest.\n"
                "   On Newsprint: Charcoal " + F["char_n"] + " to 1, Stone " + F["stone_n"] + " to 1, the two " + F["char_stone"] + " to 1 apart.\n"
                "   Each bar carries its count, so the highlight never rests on color alone. */\n"
                ".oa-ex-bars { margin: 0; font: var(--oa-type-body); color: var(--oa-color-text-primary) }\n"
                + chip_css("oa-ex-bars-illus") + ".oa-ex-bars-head { margin: 0; font: var(--oa-type-ui); font-weight: var(--oa-font-weight-bold) }\n"
                + chart_css("oa-ex-bars") + ".oa-ex-bars-bar { background: var(--oa-color-data-context) }\n"
                ".oa-ex-bars-row--subject .oa-ex-bars-bar { background: var(--oa-color-data-emphasis) }\n"
                ".oa-ex-bars-row--subject .oa-ex-bars-label, .oa-ex-bars-row--subject .oa-ex-bars-value { font-weight: var(--oa-font-weight-bold) }\n"
                "@media (forced-colors: active) {\n  .oa-ex-bars-bar { background: GrayText }\n  .oa-ex-bars-row--subject .oa-ex-bars-bar { background: CanvasText }\n}\n")}
    sets["c-26-warning"] = {
        "html": ('<div class="oa-surface-prussian oa-ex-track">\n  <p class="oa-ex-track-illus">Illustrative</p>\n  <p class="oa-ex-track-step">Step 2 of 6: Hearing</p>\n'
                 '  <p class="oa-ex-warning">\n    <svg class="oa-ex-warning-icon" viewBox="0 0 24 24" width="24" height="24"\n'
                 '      fill="none" stroke="currentColor" stroke-width="2"\n      stroke-linecap="round" stroke-linejoin="round"\n'
                 '      aria-hidden="true" focusable="false" data-icon="U-warning" data-icon-family="utility">\n'
                 + "".join(f"      {x}\n" for x in (re.sub(r'd="([^"]{60,})"', lambda m: 'd="' + "\n        ".join(textwrap.wrap(m.group(1), 56)) + '"', t)
                                                    for t in re.findall(r"<[^>]+>", inner))) +
                 '    </svg>\n    <span class="oa-ex-warning-words">\n      <strong class="oa-ex-warning-word">Warning:</strong> The committee moved\n'
                 '      the hearing to March 12. Check the new date before you travel.\n    </span>\n  </p>\n</div>\n'),
        "css": ("/* A warning in a tracker on Prussian: surface Prussian (the class on the block), role state, state warning.\n"
                "   The words in White, " + F["white_pr"] + " to 1; the bar and triangle in Newsprint, " + F["news_pr"] + " to 1. Warning has no hue of its own:\n"
                "   the word and the triangle carry it, and red never sits on Prussian. */\n"
                ".oa-ex-track { padding: var(--oa-space-200); background: var(--oa-color-surface); color: var(--oa-color-text-primary); font: var(--oa-type-body) }\n"
                + chip_css("oa-ex-track-illus") + ".oa-ex-track-step { margin: 0 0 var(--oa-space-150); font: var(--oa-type-ui); font-weight: var(--oa-font-weight-bold) }\n"
                ".oa-ex-warning { display: flex; align-items: flex-start; gap: var(--oa-space-100); margin: 0; padding-left: var(--oa-space-150);\n"
                "  border-left: var(--oa-border-width-bar) solid var(--oa-color-state-warning-mark); color: var(--oa-color-state-warning-text); font: var(--oa-type-body-small) }\n"
                ".oa-ex-warning-icon { flex: none; width: var(--oa-size-icon-medium); height: var(--oa-size-icon-medium); color: var(--oa-color-state-warning-mark) }\n"
                ".oa-ex-warning-word { font-weight: var(--oa-font-weight-bold) }\n"
                "@media (forced-colors: active) {\n  .oa-ex-warning { border-left-color: CanvasText }\n  .oa-ex-warning-icon { color: CanvasText }\n}\n")}
    for parts in sets.values():
        parts["css"] = css_lines(parts["css"])
    # the one example a keyboard reaches: its path for guide_check.js's keyPath (format oa-keys/1)
    btn = ".oa-ex-download-button"
    sets["c-26-download"]["keys.json"] = json.dumps({
        "format": "oa-keys/1", "set": "c-26-download", "rule": "26.4", "component": "Download button that waits",
        "about": "Rule 26.4's second example: the unavailable button keeps focus and its reason, and pressing it changes nothing. Written by stage_c_ch26_build.py.",
        "paths": [{"name": "Reach the button that waits, press it, and leave", "steps": [
            {"key": "Tab", "focus": btn, "states": [{"el": btn, "attr": "aria-disabled", "is": "true"}, {"el": btn, "attr": "aria-describedby", "present": True},
                                                    {"el": ".oa-ex-download-why", "text": "Choose a size to download."}]},
            {"key": "Enter", "focus": btn, "states": [{"el": btn, "attr": "aria-disabled", "is": "true"}]},
            {"key": "Space", "focus": btn, "states": [{"el": btn, "attr": "aria-disabled", "is": "true"}]},
            {"key": "Tab", "focus": "outside"}]}]}, indent=1) + "\n"
    return sets


# ---------------------------------------------------------------------------------------------------------------
# The chapter's words
# ---------------------------------------------------------------------------------------------------------------
def chapter():
    cats = words_list([CAT_WORDS.get(c, c) for c in CATEGORIES])
    rules = [
        {"id": "26.1", "title": "Read every value through a token named for its job.",
         "rule": [f"A token is a named design value, and its name says its job and the surface it sits on. tokens.css and tokens.json hold the same {N_TOKENS} tokens in {len(CATEGORIES)} categories: {cats}. "
                  "A name runs from its category to its surface: <code>oa.color.text.secondary.onNewsprint</code> in tokens.json is "
                  "<code>--oa-color-text-secondary-on-newsprint</code> in CSS. Each part of the name is a word you can look up.",
                  "Tokens come in three tiers. A primitive holds a value, such as Deep Stone. A semantic token gives a primitive one job on one surface, such as "
                  "disabled text on Newsprint. A component token gives one part of one component its value, such as the label of an unavailable button, and points to "
                  "a semantic token. Build with semantic and component tokens. A primitive is there for them to point to."],
         "tokens": ["oa.color.derived.deepStone", "oa.color.state.disabled.text.onNewsprint", "oa.component.button.disabled.label.onNewsprint"],
         "why": {"text": ["A name that says the job lets a page change its surface or its theme with no new value: a surface class or the dark theme points each "
                          "short name at the token for that ground. A primitive cannot follow, because it names a color and nothing else."],
                 "basis": "Design Tokens Format Module 2025.10; design judgment"},
         "correct": {"specimen": "s-26-1-correct", "caption": f"One value in its three tiers. The button's label reads the component token, which points to disabled text on Newsprint, which points to Deep Stone."},
         "failure": {"specimen": "s-26-1-failure", "caption": f"<strong>Fails Rule 26.1.</strong> The label reads the primitive itself. On Newsprint it passes; in the dark theme it stays Deep Stone on Charcoal and measures {F['ds_c']} to 1."},
         "specs": [{"label": "Categories", "value": cats[0].upper() + cats[1:]},
                   {"label": "JSON name", "value": "Segments in camel case, the surface last: <code>oa.color.text.secondary.onNewsprint</code>"},
                   {"label": "CSS name", "value": "<code>--oa-</code>, then the segments in kebab case: <code>--oa-color-text-secondary-on-newsprint</code>"},
                   {"label": "Short name", "value": "The CSS name without its surface, <code>--oa-color-text-secondary</code>, set by a surface class or a theme (Rule 26.6)"},
                   {"label": "Tiers", "value": "Primitive, semantic, component. A token points only to a tier below it"}],
         "related": ["05"],
         "builders": ["Search the table in Rule 26.7 by any word of a name. Its tier is in the fourth column."]},
        {"id": "26.2", "title": "Add a token only when it meets all five conditions.",
         "rule": ["A new token joins tokens.json only when it meets five conditions, and the plates below check two values against them. The need comes first: "
                  "one that no token meets, registered with an ID and its evidence. The value must be one palette color mixed in OKLab toward Newsprint or "
                  "Charcoal, with the amount recorded. A token does one job, said in one sentence, and its contrast passes on every surface it serves at the "
                  "threshold its kind needs, with the ratio stored. Last, its record holds a description, a tier and a status.",
                  "Look in the table first (Rule 26.7). Most needs already have a token, and a second token for one job leaves builders to guess between them. "
                  "Values that failed stay on record as held or rejected, and nothing uses them."],
         "tokens": ["oa.color.derived.deepStone", "oa.color.palette.stone"],
         "why": {"text": ["Each token is a value someone must test, describe and keep. The five conditions keep the set small and every token's reason on record, "
                          "so the next person who asks why a gray exists can read the answer in the file."],
                 "basis": "Design judgment"},
         "correct": {"specimen": "s-26-2-correct", "caption": f"Deep Stone meets all five. Stone measured {F['stone_n']} to 1 for small secondary text, and Deep Stone answers that need with one job."},
         "failure": {"specimen": "s-26-2-failure", "caption": f"<strong>Fails Rule 26.2.</strong> A second red for marks passes its contrast at {F['red2_n']} to 1, and still fails three conditions: no need, no recorded mix and a job already taken."},
         "specs": [{"label": "Value", "value": "One palette color mixed in OKLab toward Newsprint or Charcoal, in CSS through <code>color-mix(in oklab, …)</code>"},
                   {"label": "Contrast", "value": "4.5 to 1 for text, 3 to 1 for large text, needed graphics and focus rings, on every surface the token serves"},
                   {"label": "Record", "value": "<code>$description</code>, tier and status in the token's own entry; the need's ID and evidence in the file's register"},
                   {"label": "Release", "value": "A new token raises the version's second number (Rule 26.8)"}],
         "related": ["05", "19"],
         "builders": ["Ask the editor for a token before you add a value of your own. Send the need and its evidence with the request, and the five conditions decide."]},
        {"id": "26.3", "title": "Choose a token in five steps, starting from its surface.",
         "rule": ["The five steps are surface, role, emphasis, state, then any component token, which wins. Start from the surface the element sits on: Newsprint, White, Charcoal or Prussian. Then its job, which a token’s name calls its role: text, "
                  "graphic, border, focus, data, action, state or field. Then its emphasis: primary or secondary text, an essential or "
                  "subtle graphic, a strong or hairline border, the data a chart is about or its context. Then its state, if it has one, such as selected, disabled, "
                  "warning or error. Last, look for a component token for the part you are drawing, such as a button's disabled label. When one exists, use it, since "
                  "it already holds the component's own choice.",
                  "A message with no state of its own, such as a correction notice, takes primary text for its words and the essential graphic for its 4 px bar: "
                  "<code>--oa-color-text-primary</code>, and <code>--oa-color-graphic-essential</code> at <code>--oa-border-width-bar</code>. Leave the strong border "
                  "to the edges of fields and controls, since a change to those edges would move the notice too.",
                  "In CSS the first step is the theme or a class. With tokens.css linked, the theme points every short name at the tokens for the page’s ground, Newsprint "
                  "in the light theme and Charcoal in the dark one. A block that must keep one ground in both themes takes a surface class: <code>.oa-surface-prussian</code> points "
                  "every short name inside it at Prussian's tokens. Either way your code names the role alone, <code>--oa-color-text-secondary</code>, and draws right "
                  "on whatever ground the block sits on."],
         "tokens": ["oa.color.text.secondary.onCharcoal", "oa.color.text.secondary.onNewsprint", "oa.color.graphic.essential.onNewsprint", "oa.border.width.bar"],
         "why": {"text": ["Each step narrows the choice by a fact about the page, so two builders reach the same token. Every color token was "
                          "measured on its own surface, and starting from the surface keeps you on the one it was measured for."],
                 "basis": "WCAG 2.2 SC 1.4.3 and 1.4.11; design judgment"},
         "correct": {"specimen": "s-26-3-correct", "caption": f"A caption on a Charcoal panel: surface Charcoal, role text, emphasis secondary, no state, no component token. The token is Dim Newsprint, {F['dim_c']} to 1."},
         "failure": {"specimen": "s-26-3-failure", "caption": f"<strong>Fails Rule 26.3.</strong> The first step was skipped, and a caption on Prussian took Newsprint's secondary text token: {F['ds_pr']} to 1."},
         "specs": [{"label": "1 Surface", "value": "Newsprint, White, Charcoal or Prussian; in CSS, <code>.oa-surface-newsprint</code> and the rest, or the theme (Rule 26.6)"},
                   {"label": "2 Role", "value": "The token's job: text, graphic, border, focus, data, action, state, field"},
                   {"label": "3 Emphasis", "value": "Primary or secondary text; essential or subtle graphic; strong or hairline border; emphasis or context in data"},
                   {"label": "4 State", "value": "Muted, disabled, loading, selected, warning, error, empty, success; hover and focus have their own tokens (chapter 17)"},
                   {"label": "5 Component", "value": "A token under <code>oa.component</code> for the part you draw; it wins over the token the first four steps reach"},
                   {"label": "No state", "value": "A notice with no state: <code>--oa-color-text-primary</code> words, a <code>--oa-color-graphic-essential</code> bar at <code>--oa-border-width-bar</code>", "token": "oa.color.graphic.essential.onNewsprint"}],
         "related": ["05", "17", "18"],
         "builders": ["Write the role's short name in your CSS. Add a surface class in your HTML only where a block must keep one ground in both themes, such as a "
                      "Prussian panel. A component then needs no change to move from one surface or theme to another."]},
        {"id": "26.4", "title": "Work through the five steps on four common parts.",
         "rule": ["The four examples below take parts every product needs through the five steps of Rule 26.3, and set each at actual size beside its failure, "
                  "with code to copy. Each code set "
                  "reads only tokens.css, by short name, with a surface class where the example names a surface. Its live demos show it in the light theme and the "
                  "dark theme, so you can see each token follow the ground."],
         "tokens": ["oa.color.text.secondary.onNewsprint", "oa.component.button.disabled.label.onWhite", "oa.color.data.emphasis.onNewsprint",
                    "oa.color.data.context.onNewsprint", "oa.color.state.warning.mark.onPrussian", "oa.color.state.warning.text.onPrussian"],
         "why": {"text": ["A worked example shows the choice at each step and the ratio it buys, so you can check a new part the same way before you ship it."],
                 "basis": "WCAG 2.2 SC 1.4.1, 1.4.3 and 1.4.11; design judgment"},
         "examples": [
             {"title": "A caption under a chart, on Newsprint",
              "correct": {"specimen": "s-26-4-1-correct", "caption": f"Surface Newsprint, role text, emphasis secondary: Deep Stone, {F['ds_n']} to 1."},
              "failure": {"specimen": "s-26-4-1-failure", "caption": f"<strong>Fails Rule 26.4.</strong> Stone looks close, and it is a graphic's color: {F['stone_n']} to 1, under the 4.5 to 1 small text needs."},
              "code": {"set": "c-26-caption", "name": "Chart caption", "caption": "The caption reads <code>--oa-color-text-secondary</code>, so it is Deep Stone on Newsprint and Dim Newsprint on Charcoal."}},
             {"title": "A download button that waits for a choice, on White",
              "correct": {"specimen": "s-26-4-2-correct", "caption": f"Surface White, role action, state disabled, then the button's own tokens, which win: a dashed edge and a label at {F['ds_w']} to 1, with the reason under it."},
              "failure": {"specimen": "s-26-4-2-failure", "caption": f"<strong>Fails Rule 26.4.</strong> The button is faded to 40 percent: {F['op40_w']} to 1, and nothing says why it waits."},
              "code": {"set": "c-26-download", "name": "Download button that waits", "caption": "The block carries <code>.oa-surface-white</code>, so the button draws on White in both themes. It keeps focus and points to its reason."}},
             {"title": "A highlighted bar in a chart, on Newsprint",
              "correct": {"specimen": "s-26-4-3-correct", "caption": f"Surface Newsprint, role data: emphasis for the bar the headline names, context for the rest. Charcoal {F['char_n']} to 1, Stone {F['stone_n']} to 1, {F['char_stone']} to 1 apart."},
              "failure": {"specimen": "s-26-4-3-failure", "caption": f"<strong>Fails Rules 26.4 and 05.3.</strong> The highlight takes Pillar Red with no keyline, {F['red_n']} to 1, while an error already holds the view's red."},
              "code": {"set": "c-26-chart", "name": "Bar chart with one bar highlighted", "caption": "The bars read <code>--oa-color-data-emphasis</code> and <code>--oa-color-data-context</code>, and every bar carries its count."}},
             {"title": "A warning in a tracker, on Prussian",
              "correct": {"specimen": "s-26-4-4-correct", "caption": f"Surface Prussian, role state, state warning: the words in White, {F['white_pr']} to 1, the bar and triangle in Newsprint, {F['news_pr']} to 1, and the word Warning."},
              "failure": {"specimen": "s-26-4-4-failure", "caption": f"<strong>Fails Rules 26.4 and 05.3.</strong> Red words on Prussian, {F['red_pr']} to 1, with no word and no mark."},
              "code": {"set": "c-26-warning", "name": "Warning in a tracker", "caption": "The block carries <code>.oa-surface-prussian</code>, so the warning reads Prussian's tokens in both themes."}}],
         "specs": [{"label": "Caption", "value": f"<code>--oa-color-text-secondary</code>, caption type: {F['ds_n']} to 1 on Newsprint, {F['dim_c']} on Charcoal", "token": "oa.color.text.secondary.onNewsprint"},
                   {"label": "Button that waits", "value": f"<code>--oa-component-button-disabled-label</code> and <code>-edge</code>, dashed: {F['ds_w']} to 1 on White, with a reason line", "token": "oa.component.button.disabled.label.onWhite"},
                   {"label": "Highlighted bar", "value": f"<code>--oa-color-data-emphasis</code> beside <code>--oa-color-data-context</code>: {F['char_n']} and {F['stone_n']} to 1 on Newsprint, {F['char_stone']} apart", "token": "oa.color.data.emphasis.onNewsprint"},
                   {"label": "Warning on Prussian", "value": f"<code>--oa-color-state-warning-text</code> and <code>-mark</code>: {F['white_pr']} and {F['news_pr']} to 1, with the triangle and the word", "token": "oa.color.state.warning.mark.onPrussian"}],
         "related": ["05", "11", "12", "18"],
         "builders": ["Each code set's CSS opens with the five steps it took and the ratios they give, so you can follow the same path for a part of your own."]},
        {"id": "26.5", "title": "Start every page from tokens.css: link it, then set the body's margin and type.",
         "rule": ["Link the brand's fonts and tokens.css before your own styles, then give the body one rule: <code>body { margin: 0; font: var(--oa-type-body) }</code>. "
                  "It sets Inter at 17 px with a line height of 1.6 wherever text asks for no other style, and removes the browser's 8 px margin, so a component sits where "
                  "its code puts it. Leave the body with no surface class, so the theme sets its ground (Rule 26.6).",
                  "A product that follows the reader's light or dark setting also declares <code>&lt;meta name=\"color-scheme\" content=\"light dark\"&gt;</code> in its "
                  "head, so the browser draws its own scroll bars and form controls to match. If it offers the theme switch of Rule 18.4, the head script comes first, "
                  "before the stylesheets, so a stored choice applies before the page first draws (Rule 26.6).",
                  "tokens.css holds tokens and themes and nothing else. A page that draws one of the 41 symbols at 24 px (Rules 09.3 and 10.4) also needs "
                  "the two lines that show the pixel fit on a screen under 2x and the master from 2x: <code>.oa-at-2x { display: none }</code> and "
                  "<code>@media (min-resolution: 2dppx) { .oa-at-1x { display: none } .oa-at-2x { display: inline } }</code>."],
         "tokens": ["oa.type.body"],
         "why": {"text": ["Every code set in chapters 18 and 26 assumes exactly this page. The guide checks each one by pasting its code into a page that holds the "
                          "fonts, tokens.css and this body rule and nothing else, then compares what it draws, and the styles each part computes, with the live demo. "
                          "Rule 19.8's results list any difference."],
                 "basis": "Design judgment"},
         "correct": {"specimen": "s-26-5-correct", "caption": "The head of a page started from tokens.css, and the body text it draws against the window's edge, with no margin."},
         "failure": {"specimen": "s-26-5-failure", "caption": "<strong>Fails Rule 26.5.</strong> With the body rule left out, the text falls back to the browser's serif at 16 px inside an 8 px margin."},
         "specs": [{"label": "Order in the head", "value": "For a product with the theme switch, the head script first (Rule 26.6); then the color scheme meta tag, the fonts, tokens.css and your own styles"},
                   {"label": "Body rule", "value": "<code>body { margin: 0; font: var(--oa-type-body) }</code>", "token": "oa.type.body"},
                   {"label": "Fonts", "value": "Inter 400, 600 and 700, Inter Tight 800 and Lora Italic 400 and 500, from Google Fonts under the SIL Open Font License 1.1 (Rule 06.10). This guide carries the same files inside the page."},
                   {"label": "Themed product", "value": "<code>&lt;meta name=\"color-scheme\" content=\"light dark\"&gt;</code>; a page that stays light writes <code>only light</code>"},
                   {"label": "24 px symbols", "value": "<code>.oa-at-2x { display: none }</code> and <code>@media (min-resolution: 2dppx) { .oa-at-1x { display: none } .oa-at-2x { display: inline } }</code>, in your own stylesheet"}],
         "related": ["06", "07", "18"],
         "builders": [f"A product loads the three faces with this link (Rule 06.10): <code>{e(FONTS)}</code>. This guide carries the same files inside the page, "
                      "unchanged, so it loads no type from elsewhere; its colophon holds their licenses."]},
        {"id": "26.6", "title": "Let a product follow the reader's light or dark setting through one attribute.",
         "rule": ["tokens.css carries a light theme on Newsprint and a dark theme on Charcoal. With no attribute on the page's root, a page follows the device. "
                  "<code>data-oa-theme=\"light\"</code> or <code>\"dark\"</code> on the root wins over the device, and <code>\"device\"</code> hands the choice back. On any "
                  "other element the attribute sets that element and everything inside it.",
                  "A reader's switch (Rule 18.4) stores Light or Dark under the key <code>oa-theme</code>, and Match my device removes it. A short script in the head "
                  "applies a stored choice before the page first draws, so it never flashes the wrong ground. Paint a menu's or dialog's own ground with "
                  "<code>--oa-color-surface</code>, and an entry box's with <code>--oa-color-field-ground</code>, so both follow the theme.",
                  "A surface class keeps its own ground in both themes. In a product that follows the theme, put no surface class on the body, or on any block that "
                  "should follow it. Use one only where a block must keep one ground, as the White and Prussian examples of Rule 26.4 do.",
                  "A few roles have no Charcoal token yet and stay unset in the dark theme: the diverging chart scale, the Error Band, and two keylines red needs only "
                  "on Newsprint, the ask button's and a chart point's. An error on Charcoal keeps its bar, mark and words with no band."],
         "tokens": ["oa.color.surface.newsprint", "oa.color.surface.charcoal", "oa.color.field.ground.onNewsprint", "oa.color.field.ground.onCharcoal"],
         "why": {"text": ["One set of short names serves both grounds, so a component written once draws correctly in both themes, as each code plate in chapter 18 "
                          "shows live. A token named for one surface cannot follow."],
                 "basis": "Media Queries Level 5, prefers-color-scheme; design judgment"},
         "correct": {"specimen": "s-26-6-correct", "caption": f"One card, two themes, the same short names. Secondary text measures {F['ds_n']} to 1 on Newsprint and {F['dim_c']} on Charcoal."},
         "failure": {"specimen": "s-26-6-failure", "caption": f"<strong>Fails Rule 26.6.</strong> The words name Newsprint's text token, so in the dark theme they stay Charcoal on Charcoal: {F['char_c']} to 1."},
         "specs": [{"label": "Attribute", "value": "<code>data-oa-theme</code>: <code>light</code>, <code>dark</code> or <code>device</code>; none follows the device"},
                   {"label": "Storage", "value": "<code>oa-theme</code> in <code>localStorage</code>, holding <code>light</code> or <code>dark</code>; Match my device removes it"},
                   {"label": "Head script", "value": f"<code>{e(HEAD_SCRIPT)}</code>"},
                   {"label": "Grounds", "value": "<code>--oa-color-surface</code> for a menu or dialog; <code>--oa-color-field-ground</code> for an entry box"},
                   {"label": "Unset in the dark theme", "value": "The diverging chart scale, the Error Band, the ask button's keyline and a chart point's keyline"}],
         "related": ["05", "17", "18"],
         "builders": ["Leave the body with no surface class, so the theme sets its ground. Put the head script in its own script element before the stylesheets. "
                      "Rule 18.4 has the switch and its script to copy."]},
        {"id": "26.7", "title": "Look up any token in the table, and copy its name from there.",
         "rule": [f"The table lists every token in tokens.json, {N_TOKENS} in all, in {N_GROUPS} groups, each closed until you open it. The groups follow "
                  f"Rule 26.1’s {len(CATEGORIES)} categories, with color split into {WORDS[N_COLOR_GROUPS]} groups and chart into {WORDS[N_CHART_GROUPS]}, "
                  "font listed as “Type: faces and weights” and z-index as “Stacking order”. A row gives "
                  "the token's name in the JSON and in CSS, its value, its job, its tier and, for a color, the contrast it measures on each surface it serves. "
                  "Search by any of those words, and every group that holds a match opens. Copy puts the CSS name on your clipboard."],
         "tokens": [],
         "why": {"text": ["A name copied from the source cannot drift, and a value typed by hand stays as it was when the next release changes the token."],
                 "basis": "Design judgment"},
         "correct": {"specimen": "s-26-token-table", "caption": f"Every token in tokens.json, version {VERSION}. Search, then copy a name."},
         "failure": {"specimen": "s-26-7-failure", "caption": f"<strong>Fails Rule 26.7.</strong> A gray typed from an old file, {OLD_STONE}, where Deep Stone's name belongs. It matches today and falls behind with the next release."},
         "specs": [{"label": "Rows", "value": f"{N_TOKENS}, in {N_GROUPS} groups by category, each closed until opened; the list above them opens one"},
                   {"label": "Search", "value": "Any word of a name, a value, a job or a tier; every group with a match opens, and the line beside the field says how many rows show"},
                   {"label": "Copy", "value": "The CSS name, with a line that says what was copied, or what to do when the browser refuses"}],
         "related": ["05", "06"],
         "builders": ["The Use column prints each token's description from tokens.json word for word, and a deprecated token says which name replaced it."]},
        {"id": "26.8", "title": "Read the version before you update, and download both token files here.",
         "rule": ["tokens.css and tokens.json carry one version number, in three parts. A renamed or removed token, or a changed palette color, raises the first "
                  "part, and may break a page. A new token, or a changed value that still passes its contrast, raises the second. A change to descriptions alone "
                  "raises the third.",
                  "A replaced token keeps its old CSS name as an alias for one more release of the second part, marked as deprecated, so a page that reads it keeps "
                  "working while you move it. Every version comes with a change note: its date, the tokens it touches, what changed and why.",
                  f"The files in this draft carry <code>{e(VERSION)}</code>. The part after the hyphen marks a draft before 6.0.0, the first release."
                  + ("".join(f" Since {e(since)}, <code>{e(old)}</code> is the deprecated old name of <code>{e(new)}</code>, and it leaves with {e(gone)}."
                             for old, (new, gone, since) in DEPRECATED.items()))],
         "downloads": ["tokens.css", "tokens.json"],
         "tokens": [],
         "why": {"text": ["A builder who reads the first part of the number knows at once whether an update can break a page, and the note says what to change."],
                 "basis": "Semantic Versioning 2.0.0"},
         "correct": {"specimen": "s-26-8-correct", "caption": f"The change note for {e(NOTE['version'])}, as tokens.json records it."},
         "failure": {"specimen": "s-26-8-failure", "caption": "<strong>Fails Rule 26.8.</strong> A token renamed in a release of the second part, with no alias and no note. A page's caption loses its gray, and nothing warns."},
         "specs": [{"label": "First part", "value": "A renamed or removed token, or a changed palette color"},
                   {"label": "Second part", "value": "A new token, or a changed value that still passes its contrast"},
                   {"label": "Third part", "value": "Descriptions and notes alone"},
                   {"label": "Deprecated token", "value": "Its old CSS name stays as an alias for one more release of the second part"},
                   {"label": "Files", "value": "tokens.css for a web page; tokens.json, in the Design Tokens Format Module 2025.10, for design tools and build scripts"}],
         "related": ["27", "28"],
         "builders": ["Read the change note before you update a product's copy of tokens.css. The newest note also sits at the top of the file."]},
    ]
    return {
        "number": "26", "anchor": "tokens", "title": "Tokens and how to choose them", "part": "Production", "opener": "s-26-opener",
        "instruction": "Choose a token step by step from its surface, and call it by name.",
        "intro": [f"Every color, size, space and speed in this guide comes from a design token: a named value kept in the token files, which the guide, the asset package "
                  f"and every product read. This chapter shows how the names work, when a new token may join, and how to choose the right one in five steps, with "
                  f"four worked examples to copy.",
                  f"The files are tokens.css, for a web page, and tokens.json, for design tools and build scripts. Both hold the same {N_TOKENS} tokens and the same "
                  f"version, and Rule 26.8 has both to download."],
        "groups": [{"before_rule": "26.1", "number": 1, "title": "What a token is", "line": "A token names one value for one job, and its name says which."},
                   {"before_rule": "26.3", "number": 2, "title": "Choosing a token", "line": "Five steps take you from the surface to the token, and four examples show each step."},
                   {"before_rule": "26.5", "number": 3, "title": "Using the files", "line": "Start a page from tokens.css, follow the reader's light or dark setting, look up any token and download the files."}],
        "rules": rules, "extras": [],
        "related_chapters": [{"chapter": "05", "reason": "The palette, the four surfaces and one working red in each view."},
                             {"chapter": "06", "reason": "The type styles the type tokens set."},
                             {"chapter": "07", "reason": "The space, layout and breakpoint tokens at work."},
                             {"chapter": "17", "reason": "The state and motion tokens in use."},
                             {"chapter": "18", "reason": "Every component's code, built on these tokens, in both themes."},
                             {"chapter": "19", "reason": "The contrast thresholds each token is measured against."},
                             {"chapter": "27", "reason": "The asset package that carries the token files."},
                             {"chapter": "28", "reason": "The checklist that asks for tokens by name."}],
        "sources": ["Source: Design Tokens Community Group, “Design Tokens Format Module 2025.10”, Final Community Group Report, October 28, 2025, retrieved November 11, 2026. The format of tokens.json, behind Rules 26.1 and 26.8.",
                    "Source: W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024, success criteria 1.4.1, 1.4.3 and 1.4.11, retrieved November 10, 2026. The contrast thresholds behind Rules 26.2 to 26.4.",
                    "Source: W3C, “Media Queries Level 5”, W3C Working Draft, February 19, 2026, the prefers-color-scheme feature, retrieved November 10, 2026. The device setting behind Rule 26.6.",
                    "Source: Tom Preston-Werner, “Semantic Versioning 2.0.0”, semver.org, retrieved November 11, 2026. The version rule behind Rule 26.8."],
    }


# ---------------------------------------------------------------------------------------------------------------
# DR-191's second pass, E9: the guide prints typographic apostrophes in prose (chapter 02's notes, item 16); code keeps its own
CODE_SPAN = re.compile(r"(<code\b[^>]*>.*?</code>)", re.S)


def curly(x):
    if isinstance(x, str):
        return "".join(part if part.startswith("<code") else part.replace("'", "’") for part in CODE_SPAN.split(x))
    if isinstance(x, list):
        return [curly(v) for v in x]
    if isinstance(x, dict):
        return {k: (curly(v) if k not in ("id", "specimen", "set", "tokens", "token", "anchor", "opener", "downloads") else v) for k, v in x.items()}
    return x


def outputs():
    S, M = specimens()
    M = {k: dict(v, alt=curly(v["alt"])) if "alt" in v else v for k, v in M.items()}
    files = {CHAPTER: json.dumps(curly(chapter()), indent=1, ensure_ascii=False) + "\n", MANIFEST: json.dumps(M, indent=1, ensure_ascii=False) + "\n"}
    for sid, text in S.items():
        files[SPEC / f"{sid}.html"] = text
    for sid, parts in code_sets().items():
        for ext, text in parts.items():
            files[CODE / f"{sid}.{ext}"] = text
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="fail if any file on disk differs from what this script writes")
    args = ap.parse_args()
    files = outputs()
    stale = [p for p, t in files.items() if not p.exists() or p.read_text() != t]
    if args.check:
        for p in stale:
            print(f"stage_c_ch26_build --check: {p.relative_to(ROOT)} is not what the script writes")
        print(f"stage_c_ch26_build --check: {len(files) - len(stale)} of {len(files)} files current")
        return 1 if stale else 0
    for p in stale:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(files[p])
    print(f"stage_c_ch26_build: {len(files)} files, {len(stale)} written; tokens {N_TOKENS}, version {VERSION}; figures {json.dumps(F)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
