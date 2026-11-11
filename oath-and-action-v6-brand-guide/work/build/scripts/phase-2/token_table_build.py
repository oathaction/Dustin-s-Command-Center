"""Chapter 26's token table: every token in tokens.json as one searchable table, with a Copy button on each name.

Usage (from the project folder):
  python3 -I work/build/scripts/phase-2/token_table_build.py             write the specimen
  python3 -I work/build/scripts/phase-2/token_table_build.py --check     fail if the specimen on disk is not what tokens.json makes now
  python3 -I work/build/scripts/phase-2/token_table_build.py --out PATH [--preview PATH]
                                                                          write elsewhere; --preview also writes a page that
                                                                          shows the specimen in the guide's shell, for tests

Reads   work/build/tokens/tokens.json (names, values, descriptions, tiers and the contrast the token build measured)
Writes  work/build/guide/specimens/s-26-token-table.html, a specimen fragment for guide_build.py. Chapter 26 places it in
        round 1 with this manifest entry (the build warns on a manifest entry no chapter places, so it waits for the chapter):
          "s-26-token-table": {"chapter": "26", "rule": "26.N", "interactive": true, "fit_switch": false,
                               "alt": "Every token in tokens.json, one row each: its name, CSS name, value, use, tier and contrast."}

Each row: the token's name and CSS name, with a Copy button that copies the CSS name; its value (a swatch and hex for a
color, the size, duration, easing or type it sets, and the token it points to); its description; its tier; and, for a
color, the contrast it measures on each surface it serves at the threshold its kind needs. The rows group by category.
A search field above filters by any of these words, and a polite status line says how many rows show. The table reads
every color through var(--oa-...), so a swatch draws what tokens.css holds, and it carries no literal color.

Stage C, round 0, November 10, 2026, by the guide engineer (Stage C brief, Engineer, item 5). The chapter's words come
in round 1. guide_check.js will hold the rendered table to tokens.json in round 1 (row count, and each swatch's computed
color against its hex); --check holds the file to tokens.json now.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TOKENS_JSON = ROOT / "work/build/tokens/tokens.json"
OUT = ROOT / "work/build/guide/specimens/s-26-token-table.html"
SHELL = ROOT / "work/build/guide/shell"
TOKENS_CSS = ROOT / "work/build/tokens/tokens.css"
NS = "org.oathandaction"
SID = "s-26-token-table"
SURF = {"onNewsprint": "Newsprint", "onWhite": "White", "onCharcoal": "Charcoal", "onPrussian": "Prussian"}
KIND = {"text": ("text", 4.5), "largeText": ("large text", 3), "graphic": ("graphic", 3), "focus": ("focus ring", 3),
        "decorative": ("decoration", None), "dataFill": ("data fill, values printed", None), "logotype": ("identity mark", None),
        "background": ("ground", None), "surface": ("surface", None)}
TIER = {"primitive": "Primitive", "semantic": "Semantic", "component": "Component"}
e = html.escape


def dots(path):
    """A dotted name that may break after each dot, and nowhere else."""
    return "<wbr>.".join(e(x) for x in path.split(".")).replace("<wbr>.", ".<wbr>")


def css_name(path):
    return "--" + "-".join(re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", seg).lower() for seg in path.split("."))


def flatten(tree):
    out = {}

    def walk(node, path, typ):
        typ = node.get("$type", typ) if isinstance(node, dict) else typ
        for k, v in node.items():
            if k.startswith("$") or not isinstance(v, dict):
                continue
            p = f"{path}.{k}" if path else k
            if "$value" in v:
                out[p] = dict(v, **{"$type": v.get("$type", typ)})
            else:
                walk(v, p, typ)
    walk(tree, "", None)
    return out


def alias(v):
    return v[1:-1] if isinstance(v, str) and re.fullmatch(r"\{[^{}]+\}", v) else None


def resolve(p, toks, seen=()):
    t = toks[p]
    a = alias(t["$value"])
    return resolve(a, toks, seen + (p,)) if a and a not in seen else (p, t["$value"])


def ext(t):
    return (t.get("$extensions") or {}).get(NS, {})


def num(x):
    s = f"{round(float(x), 4):.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def group_of(p):
    s = p.split(".")
    if s[1] == "color":
        return {"palette": "Color: the palette", "derived": "Color: derived", "tint": "Color: tints"}.get(s[2], "Color: roles by surface")
    if s[1] == "chart":
        return "Chart: color" if s[2] == "color" else "Chart: sizes"
    return {"font": "Type: faces and weights", "type": "Type: styles", "space": "Space", "size": "Size", "layout": "Layout",
            "radius": "Radius", "border": "Border", "opacity": "Opacity", "motion": "Motion", "zIndex": "Stacking order",
            "component": "Components"}.get(s[1], s[1])


def value_html(p, toks):
    t = toks[p]
    typ = t["$type"]
    tgt, v = resolve(p, toks)
    a = alias(t["$value"])
    via = f'<span class="tt-via">From <code>{dots(a)}</code></span>' if a else ""
    if typ == "color":
        return (f'<span class="tt-sw" style="background:var({css_name(p)})" aria-hidden="true"></span>'
                f'<span class="tt-v">{e(v["hex"]).replace("#", "&#35;")}</span>{via}')   # a printed hex is words, as chapter 05 writes it
    if typ in ("dimension", "duration"):
        if isinstance(v, dict):
            extra = f", {num(v['value'] * 16)} px" if v.get("unit") == "rem" else ""
            rm = ext(toks[tgt]).get("reducedMotionValue") if typ == "duration" else None
            rmw = f"; {num(rm['value'])} {rm['unit']} under reduced motion" if rm else ""
            return f'<span class="tt-v">{num(v["value"])}{e(v["unit"])}{extra}{rmw}</span>{via}'
    if typ == "typography" and isinstance(v, dict):
        x = ext(toks[tgt])
        fam = resolve(alias(v["fontFamily"]), toks)[1] if alias(v["fontFamily"]) else v["fontFamily"]
        wt = resolve(alias(v["fontWeight"]), toks)[1] if alias(v["fontWeight"]) else v["fontWeight"]
        lo = (x.get("minFontSize") or v["fontSize"])["value"] * 16
        hi = v["fontSize"]["value"] * 16
        size = f"{num(hi)} px" if abs(lo - hi) < 1e-9 else f"{num(lo)} to {num(hi)} px"
        track = f", tracking {num(x.get('trackingEm', 0))}em" if x.get("trackingEm") else ""
        return f'<span class="tt-v">{e(fam[0] if isinstance(fam, list) else fam)} {num(wt)}, {size}, line height {num(v["lineHeight"])}{track}</span>{via}'
    if typ == "fontFamily":
        return f'<span class="tt-v">{e(", ".join(v) if isinstance(v, list) else v)}</span>{via}'
    if typ == "cubicBezier":
        return f'<span class="tt-v">cubic-bezier({", ".join(num(x) for x in v)})</span>{via}'
    if typ in ("number", "fontWeight"):
        unit = ext(toks[tgt]).get("unit")
        css = ext(toks[tgt]).get("css")
        return f'<span class="tt-v">{num(v)}{" " + e(unit) if unit else ""}{f" (CSS {e(css)})" if css else ""}</span>{via}'
    return f'<span class="tt-v">{e(json.dumps(v))}</span>{via}'


def contrast_html(p, toks):
    """The contrast a color measures where it serves: its own surface for a role, each listed surface for a primitive."""
    t = toks[p]
    if t["$type"] != "color":
        return ""
    sem = p
    chain = [p]
    while alias(toks[chain[-1]]["$value"]) and len(chain) < 12:
        chain.append(alias(toks[chain[-1]]["$value"]))
    for c in chain:
        if ext(toks[c]).get("tier") == "semantic":
            sem = c
            break
    x = ext(toks[sem])
    if x.get("kind") == "surface":
        return ""
    last = p.split(".")[-1]
    if isinstance(x.get("contrast"), (int, float)):
        kind, need = KIND.get(x.get("kind"), (x.get("kind"), None))
        where = SURF.get(last) or SURF.get(sem.split(".")[-1]) or ""
        ground = alias(x.get("ground") or "")
        on = f"on {ground.split('.')[-2]} {ground.split('.')[-1][2:]}" if ground else f"on {where}"
        bits = [f'<span class="tt-r">{num(x["contrast"])}:1 {e(on)}</span>, {e(kind)}' + (f", needs {num(need)}:1" if need else "")]
        if x.get("keylineContrast"):
            bits.append(f"keyline {num(x['keylineContrast'])}:1")
        for g, r in (x.get("contrastAlso") or {}).items():
            bits.append(f"{num(r)}:1 on {e(g.split('.')[-2])}")
        return "; ".join(bits)
    if x.get("kind") == "background" and x.get("textContrast"):
        return "Text on it: " + "; ".join(f'{e(k.split(".")[-2] if k.split(".")[-1].startswith("on") else k.split(".")[-1])} {num(r)}:1'
                                          for k, r in x["textContrast"].items())
    if isinstance(x.get("contrast"), dict):
        kind, need = KIND.get(x.get("kind"), (x.get("kind"), None))
        return "; ".join(f'<span class="tt-r">{num(r)}:1 on {e(s.capitalize())}</span>' for s, r in x["contrast"].items()) \
            + (f", {e(kind)}, needs {num(need)}:1" if need else (f", {e(kind)}" if kind else ""))
    return ""


STYLE = """
.tt { font: var(--oa-type-body-small); color: var(--oa-color-text-primary) }
.tt-find { display: flex; flex-wrap: wrap; align-items: end; gap: var(--oa-space-100) var(--oa-space-300); margin: 0 0 var(--oa-space-200) }
.tt-find label { display: block; font: var(--oa-type-ui) }
.tt-q { box-sizing: border-box; min-height: var(--oa-size-target-touch); width: min(100%, 24rem); padding: 0 var(--oa-space-150);
  border: var(--oa-border-width-hairline) solid var(--oa-color-border-strong); background: var(--oa-color-surface); color: var(--oa-color-text-primary); font: var(--oa-type-body) }
.tt-q:focus-visible, .tt-copy:focus-visible { outline: var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring); outline-offset: var(--oa-border-focus-offset) }
.tt-status { margin: 0; font: var(--oa-type-caption); color: var(--oa-color-text-secondary) }
.tt table { border-collapse: collapse; width: 100% }
.tt caption { text-align: left; font: var(--oa-type-caption); color: var(--oa-color-text-secondary); padding-bottom: var(--oa-space-100) }
.tt thead th { font: var(--oa-type-label); letter-spacing: var(--oa-type-label-letter-spacing); text-transform: uppercase; text-align: left;
  padding: var(--oa-space-100) var(--oa-space-200) var(--oa-space-100) 0; border-bottom: var(--oa-border-width-hairline) solid var(--oa-color-border-strong) }
.tt tbody th, .tt td { text-align: left; vertical-align: top; padding: var(--oa-space-150) var(--oa-space-200) var(--oa-space-150) 0;
  border-bottom: var(--oa-border-width-hairline) solid var(--oa-color-border-hairline); font: var(--oa-type-body-small) }
.tt .tt-g th { padding-top: var(--oa-space-400); font: var(--oa-type-h4); letter-spacing: var(--oa-type-h4-letter-spacing); border-bottom-color: var(--oa-color-border-strong) }
.tt-n { display: block; font-weight: var(--oa-font-weight-semibold); overflow-wrap: break-word }
.tt-c { display: block; margin-top: var(--oa-space-050); font-size: .875rem; overflow-wrap: break-word; color: var(--oa-color-text-secondary) }
.tt tbody th[scope="row"] { width: 16rem }
.tt-copy { box-sizing: border-box; margin-top: var(--oa-space-100); min-height: var(--oa-size-target-touch); padding: 0 var(--oa-space-200); border: 0;
  box-shadow: inset 0 0 0 var(--oa-border-width-hairline) var(--oa-color-border-strong); background: transparent; color: var(--oa-color-text-primary); font: var(--oa-type-ui); cursor: pointer }
.tt-copy:hover { box-shadow: inset 0 0 0 var(--oa-border-width-rule) var(--oa-color-border-strong); text-decoration: underline }
.tt-sw { display: inline-block; width: 1.25rem; height: 1.25rem; margin-right: var(--oa-space-100); vertical-align: -.3em;
  box-shadow: inset 0 0 0 var(--oa-border-width-hairline) var(--oa-color-border-strong) }
.tt-v { font-variant-numeric: tabular-nums }
.tt-via { display: block; margin-top: var(--oa-space-050); font: var(--oa-type-caption); color: var(--oa-color-text-secondary) }
.tt-via code { overflow-wrap: break-word }
.tt-st .tt-mk { width: var(--oa-size-icon-small); height: var(--oa-size-icon-small); margin-right: .4em; vertical-align: -.2em }
.tt-st .tt-ok { color: var(--oa-color-state-success-mark) }
.tt-st.is-error { color: var(--oa-color-state-error-text); background: var(--oa-color-state-error-band); border-left: var(--oa-border-width-bar) solid var(--oa-color-state-error-bar); padding: var(--oa-space-100) var(--oa-space-150) }
.tt-wrap { container-type: inline-size }
@container (max-width: 50rem) {
  .tt thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%) }
  .tt tr { display: block; padding: var(--oa-space-100) 0; border-bottom: var(--oa-border-width-hairline) solid var(--oa-color-border-hairline) }
  .tt .tt-g { border-bottom-color: var(--oa-color-border-strong) }
  .tt tbody th, .tt td { display: block; border: 0; padding: var(--oa-space-050) 0 }
  .tt td::before { display: block; font: var(--oa-type-label); letter-spacing: var(--oa-type-label-letter-spacing); text-transform: uppercase; color: var(--oa-color-text-secondary) }
  .tt td:nth-child(2)::before { content: "Value" }
  .tt td:nth-child(3)::before { content: "Use" }
  .tt td:nth-child(4)::before { content: "Tier" }
  .tt td:nth-child(5)::before { content: "Contrast" }
  .tt td:empty { display: none }
}
@media (forced-colors: active) { .tt-copy { border: 1px solid ButtonText } .tt-sw { forced-color-adjust: none } }
"""

SCRIPT = """
// Chapter 26's token table: the search filters the rows and says how many show; each Copy copies its CSS name.
document.querySelectorAll('.tt').forEach(function (box) {
  var q = box.querySelector('.tt-q'), status = box.querySelector('.tt-status'), words = status.querySelector('.tt-t');
  var groups = Array.prototype.slice.call(box.querySelectorAll('tbody'));
  var rows = Array.prototype.slice.call(box.querySelectorAll('tbody tr:not(.tt-g)'));
  var text = rows.map(function (r) { return r.textContent.replace(/\\s+/g, ' ').toLowerCase(); });
  var total = rows.length, timer = null;
  // the line carries the count with its advice (F-5), and a copy's result with the success or the error mark (F-7)
  var say = function (t, mark) {
    words.textContent = '';
    if (mark === 'err') { var b = document.createElement('b'); b.textContent = 'Error:'; words.appendChild(b); words.appendChild(document.createTextNode(' ' + t)); } else words.textContent = t;
    status.querySelector('.tt-ok').toggleAttribute('hidden', mark !== 'ok');
    status.querySelector('.tt-er').toggleAttribute('hidden', mark !== 'err');
    status.classList.toggle('is-error', mark === 'err');
    if (mark === 'err') { status.setAttribute('data-red', 'working'); status.setAttribute('data-red-job', 'error'); } else { status.removeAttribute('data-red'); status.removeAttribute('data-red-job'); }
  };
  function filter() {
    var words = q.value.toLowerCase().replace(/^--/, '').split(/\\s+/).filter(Boolean), shown = 0;   // the search's words
    rows.forEach(function (r, i) { var hit = words.every(function (w) { return text[i].indexOf(w) >= 0; }); r.hidden = !hit; if (hit) shown++; });
    groups.forEach(function (g) { g.hidden = !g.querySelector('tr:not(.tt-g):not([hidden])'); });
    say(!words.length ? 'Showing all ' + total + ' tokens.' : shown ? 'Showing ' + shown + ' of ' + total + ' tokens.'
      : 'Showing 0 of ' + total + ' tokens. No token matches. Try a role, such as text or focus, or a surface, such as Charcoal.');
  }
  q.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(filter, 250); });
  box.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('.tt-copy');
    if (!b) return;
    var name = b.getAttribute('data-copy');
    var fail = function () {
      var c = b.parentNode.querySelector('.tt-c'), r = document.createRange();
      r.selectNodeContents(c); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      say('The browser blocked copying. ' + name + ' is selected: press Control and C, or Command and C.', 'err');
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(name).then(function () { say('Copied ' + name + '.', 'ok'); }, fail); else fail();
  });
});
"""


# The table is reader text (guide_check.js's codes and retiredWords tests hold every reader page to this). Since
# 6.0.0-gate2.8 (DR-218) every description in tokens.json is written for readers, so the table prints each one word for
# word, and this guard stops the script on any description that brings back a studio code, a retired name or an
# internal one, so a new one cannot slip through. Round 1 rewrote the descriptions here; the source now does.
NOT_FOR_READERS = re.compile(r"\b(?:DR|D1|D2|G1)-\d+|\bT-\d+\b|\bN-\d+\b|\b(?:PP|BE|CD|CA|AX|RP)-[MS]\d+|\b[RIS]\d+\b|"
                             r"Signal Grid|\bV5\b|\bV4\.2\b|the studio|\bGates?\b|\bPhase\b|Master Brief|Atlas V7|\bBoard \d|"
                             r"Explainer|palette lab|stretch test|Night Edition|treatment [A-Z]\b|\bsection \d")


def reader(text, where):
    """A description as the guide's readers see it: tokens.json's words, held to the guard above."""
    left = NOT_FOR_READERS.search(text)
    if left:
        raise SystemExit(f"token_table_build: the description of {where} says {left.group(0)!r} to readers: {text}")
    return text


def build(tokens_path):
    tree = json.loads(Path(tokens_path).read_text())
    meta = tree.get("$extensions", {}).get(NS, {})
    toks = flatten(tree)
    groups = {}
    for p in toks:
        groups.setdefault(group_of(p), []).append(p)
    body = []
    for g, paths in groups.items():
        rows = [f'<tr class="tt-g"><th scope="rowgroup" colspan="5">{e(g)} <span class="tt-k">({len(paths)})</span></th></tr>']
        for p in paths:
            t = toks[p]
            x = ext(t)
            cn = css_name(p)
            rows.append(f'<tr><th scope="row"><span class="tt-n">{dots(p)}</span><code class="tt-c">{e(cn)}</code>'
                        f'<button type="button" class="tt-copy" data-copy="{e(cn)}" aria-label="Copy {e(cn)}">Copy</button></th>'
                        f'<td>{value_html(p, toks)}</td><td>{e(reader(t.get("$description", ""), p))}</td><td>{e(TIER.get(x.get("tier"), "Untiered"))}{", deprecated" if "$deprecated" in t else ""}</td>'
                        f'<td>{contrast_html(p, toks)}</td></tr>')
        body.append(f'<tbody>{"".join(rows)}</tbody>')
    n = len(toks)
    version = meta.get("tokenSetVersion", "")
    return (f'<!-- Generated by work/build/scripts/phase-2/token_table_build.py from work/build/tokens/tokens.json, version {e(version)}, {n} tokens. '
            f'Do not edit by hand: run the script; its --check fails when this file and tokens.json disagree. -->\n'
            f'<style>{STYLE}</style>\n'
            f'<div class="tt" data-token-count="{n}" data-token-version="{e(version)}">'
            f'<div class="tt-find"><div><label for="tt-q">Search the tokens</label>'
            f'<input class="tt-q" id="tt-q" type="search" autocomplete="off" spellcheck="false" aria-describedby="tt-status"></div>'
            f'<p class="tt-status tt-st" id="tt-status" role="status">'
            f'<svg class="tt-mk tt-ok" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false" data-icon="U-success" data-icon-family="utility" hidden><use href="#oa-sym-u-success-16px"/></svg>'
            f'<svg class="tt-mk tt-er" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false" data-icon="U-error" data-icon-family="utility" hidden><use href="#oa-sym-u-error-16px"/></svg>'
            f'<span class="tt-t">Showing all {n} tokens.</span></p></div>'
            f'<div class="tt-wrap"><table><caption>Every token in tokens.json, version {e(version)}, by category: its name and CSS name, value, use, tier and the contrast it measures where it serves.</caption>'
            f'<thead><tr><th scope="col">Token</th><th scope="col">Value</th><th scope="col">Use</th><th scope="col">Tier</th><th scope="col">Contrast</th></tr></thead>'
            f'{"".join(body)}</table></div></div>\n'
            f'<script>{SCRIPT}</script>\n'), n, version


def preview(fragment, out):
    """The specimen in a page with tokens.css and the shell's CSS, in a stage as guide_build.py frames it, for tests."""
    css = TOKENS_CSS.read_text()
    shell = (SHELL / "guide-shell.css").read_text()
    frag = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)", lambda m: f'{m.group(1)}@scope ([data-specimen="{SID}"]) {{\n{m.group(2)}\n}}{m.group(3)}', fragment, flags=re.S)
    page = (f'<!doctype html><html lang="en" data-oa-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Token table preview</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&amp;family=Inter:wght@400;500;600;700&amp;display=swap">'
            f'<style>{css}</style><style>{shell}</style></head><body class="oa-surface-newsprint"><main id="main" style="padding:0 var(--m)">'
            f'<div class="plate-stage oa-surface-newsprint" data-specimen="{SID}" role="group" aria-label="Token table, interactive specimen">{frag}</div></main></body></html>')
    Path(out).write_text(page)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tokens", default=str(TOKENS_JSON))
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--check", action="store_true", help="fail if the specimen on disk differs from what tokens.json makes")
    ap.add_argument("--preview", help="also write a test page that shows the specimen in the shell")
    a = ap.parse_args()
    frag, n, version = build(a.tokens)
    out = Path(a.out)
    if a.check:
        if not out.exists() or out.read_text() != frag:
            print(f"token_table_build --check: {out.name} is not what tokens.json {version} makes; run the script.")
            sys.exit(1)
        print(f"token_table_build --check: {out.name} matches tokens.json {version}, {n} tokens.")
        return
    out.write_text(frag)
    print(f"token_table_build: wrote {out} ({len(frag.encode()):,} bytes), {n} tokens, version {version}.")
    if a.preview:
        preview(frag, a.preview)
        print(f"  preview: {a.preview}")


if __name__ == "__main__":
    main()
