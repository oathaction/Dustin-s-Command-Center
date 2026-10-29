"""Part B: the searchable Civic Line catalog, one self-contained HTML file.

    python3 -I build_catalog.py

Writes assets/civic-line/<date>_Civic-Line-Icon-Catalog.html, following the
Artifact page contract: no doctype, html, head or body tags; the file opens
with its <title>, the viewport-fit-sides meta and the <style>. Colors exist
only as CSS tokens. Icons are inlined once, from the red-black exports, with
their colors turned into tokens, so one copy serves all four editions: each
edition sets the ink and accent tokens to the colors its export files carry
(DR-09). Stroke widths read a --k token (1 by default), so a tile can hold its
line at the set's cap the way the tile files do (variant review S-1). The
three tile shapes are drawn once as SVG symbols and referenced by every card
(DR-10); in a holder each card scales its icon by the shape factor times its
optical scale and moves it by its optical offset (S-1, S-2), and a card whose
tile sits below the icon's minimum tile size says so (M-1). Reference crops
are the untouched PNG files, embedded byte for byte as data URIs.
"""
import base64
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402

OUT = os.path.join(C.ASSETS, f"{C.DATE}_Civic-Line-Icon-Catalog.html")
SHEET_NAMES = {"01": "Participation & Accountability", "02": "Government, Information & Technology",
               "03": "Economy & Public Issues", "04": "Reforms R-01–R-25", "05": "Reforms R-26–R-50"}
COLOR_TOKENS = {C.CHARCOAL: "var(--icon-ink)", C.PILLAR_RED: "var(--icon-accent)",
                "#FFFFFF": "var(--mask-keep)", "#000000": "var(--mask-cut)"}
LIMIT = 12 * 1024 * 1024

# Brand palette (Edition 06) and the roles built from it. Light values first;
# DARK lists every token again for the two dark blocks.
LIGHT = {
    "newsprint": "#DCD9D2", "charcoal": "#121212", "pillar-red": "#E63946", "prussian": "#1F2D5A",
    "white": "#FFFFFF", "stone": "#5D636D",
    "bg": "var(--white)", "text": "var(--charcoal)", "muted": "var(--stone)", "line": "var(--stone)",
    "hair": "var(--newsprint)", "tile": "var(--newsprint)", "raised": "var(--white)",
    "accent": "var(--prussian)", "on-accent": "var(--white)", "focus": "var(--prussian)",
    "chip": "var(--newsprint)", "on-chip": "var(--charcoal)",
    "icon-ink": "var(--charcoal)", "icon-red": "var(--pillar-red)", "icon-accent": "var(--icon-red)",
    "card-ground": "var(--newsprint)", "holder-fill": "var(--newsprint)", "stage": "var(--charcoal)",
    "mask-keep": "#FFFFFF", "mask-cut": "#000000",
    "scrim": "rgb(18 18 18 / 0.55)",
}
DARK = dict(LIGHT, **{
    "bg": "var(--charcoal)", "text": "var(--white)", "muted": "var(--newsprint)", "line": "var(--stone)",
    "hair": "var(--stone)", "raised": "var(--prussian)", "accent": "var(--newsprint)", "on-accent": "var(--charcoal)",
    "focus": "var(--white)", "chip": "var(--stone)", "on-chip": "var(--white)",
    "scrim": "rgb(18 18 18 / 0.72)",
})


def tokens(d, indent="  "):
    return "".join(f"{indent}--{k}: {v};\n" for k, v in d.items())


def tokenise_colours(svg):
    """Move each element's fill and stroke colors into one style attribute that
    reads the color tokens, and its stroke width into a calc() that reads --k."""
    def fix(m):
        tag = m.group(0)
        style = []
        for prop in ("fill", "stroke"):
            mm = re.search(rf' {prop}="([^"]+)"', tag)
            if not mm or mm.group(1) == "none":
                continue
            v = mm.group(1).upper()
            if v not in COLOR_TOKENS:
                raise SystemExit(f"unexpected color {v} in an export")
            style.append(f"{prop}:{COLOR_TOKENS[v]}")
            tag = tag.replace(mm.group(0), "", 1)
        mm = re.search(r' stroke-width="([^"]+)"', tag)
        if mm:
            style.append(f"stroke-width:calc({mm.group(1)}px * var(--k, 1))")
            tag = tag.replace(mm.group(0), "", 1)
        if style:
            tag = re.sub(r"(/?>)$", f' style="{";".join(style)}"\\1', tag, count=1)
        return tag
    return re.sub(r"<(path|line|polyline|polygon|circle|ellipse|rect)\b[^>]*>", fix, svg)


def icon_inner(row):
    """Inner markup of the red-black export with the file's root id replaced by
    a __P__ marker, so each inline copy can take its own prefix."""
    p = os.path.join(C.ASSETS, "red-black", row["exports"]["svg_red_black"])
    if not os.path.exists(p):
        return None
    s = open(p, encoding="utf-8").read().split("?>", 1)[-1]
    s = re.sub(r"<title>.*?</title>|<desc>.*?</desc>", "", s, flags=re.S)
    inner = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")].strip()
    inner = inner.replace(C.bare_root(row["id"], "red-black") + "-", "__P__")
    if re.search(r'id="(?!__P__)', inner) or re.search(r"url\(#(?!__P__)", inner):
        raise SystemExit(f"{row['id']}: an id in the export does not start with its root id")
    inner = re.sub(r">\s+<", "><", inner)
    return tokenise_colours(inner)


def nb(label):
    """Keep a middle-dot separator with the word after it, so a wrapped label
    starts its second line with the separator (variant review S-7)."""
    return label.replace(" · ", " ·\u00a0")


def data_uri(path):
    with open(path, "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode("ascii")


def fnum(v, nd=3):
    return None if v is None else round(float(v), nd)


def gather():
    inv = C.load_inventory()
    icons = []
    for r in inv["icons"]:
        i = r["id"]
        m = C.read_json(os.path.join(C.QA, "metrics", f"{i}.json")) or {}
        st = C.read_json(os.path.join(C.QA, "status", f"{i}.json")) or {}
        corr = C.read_json(os.path.join(C.SRC, f"{i}.json")) or {}
        inner = icon_inner(r)
        has_src = os.path.exists(os.path.join(C.SRC, f"{i}.svg"))
        t = r["transform"]
        sc = t["s"]
        ed = (m.get("edge_distance_px") or {}).get("symmetric") or {}
        a, dx, kk = C.tile_optics(i, r["stroke_units"])
        icons.append({
            "id": i, "label": r["label"], "labelNb": nb(r["label"]), "slug": r["slug"], "sheet": r["sheet"], "row": r["row"], "col": r["column"],
            "a": a, "dx": dx, "sk": round(kk, 6), "min": C.tile_min_px(i),
            "w": r["crop"]["w"], "h": r["crop"]["h"],
            "vb": f"{64 - sc * t['cx']:.4f} {64 - sc * t['cy']:.4f} {r['crop']['w'] * sc:.4f} {r['crop']['h'] * sc:.4f}",
            "svg": inner,
            "refBlack": data_uri(os.path.join(C.ASSETS, "reference-crops", r["reference_crops"]["black"])),
            "refRed": data_uri(os.path.join(C.ASSETS, "reference-crops", r["reference_crops"]["red"])),
            "m": {"sil": fnum(m.get("silhouette_iou_1x"), 4), "red": fnum(m.get("red_iou_1x"), 4),
                  "em": fnum(ed.get("mean")), "ep": fnum(ed.get("p95")), "ex": fnum(ed.get("max")),
                  "off": [m["best_offset_1x"]["dx"], m["best_offset_1x"]["dy"]] if m.get("best_offset_1x") else None,
                  "ratio": fnum(m.get("ink_area_ratio_trace_over_reference"), 3),
                  "b4": fnum(m.get("bake_check_iou_4x"), 4), "b1": fnum(m.get("bake_check_iou_1x"), 4)} if m else None,
            "state": (st.get("state") or "traced") if has_src and inner else "todo",
            "tracer": st.get("tracer") or corr.get("tracer") or "",
            "builds": st.get("iterations", 0),
            "corr": [{"what": c.get("what", ""), "why": c.get("why", ""), "el": c.get("element")} for c in corr.get("corrections", [])],
            "notes": corr.get("notes", "") if isinstance(corr.get("notes", ""), str) else "",
            "construction": r["construction"], "redText": r["red_text"],
        })
    return inv, icons


HOLDERS = '<use class="hold h-square" href="#h-square" x="0" y="0" width="128" height="128"/>' \
          '<use class="hold h-rounded" href="#h-rounded" x="0" y="0" width="128" height="128"/>' \
          '<use class="hold h-circle" href="#h-circle" x="0" y="0" width="128" height="128"/>'


def sprite():
    """The three tile shapes, drawn once (DR-10)."""
    import cl_tiles as T
    return ('<svg class="sprite" aria-hidden="true" focusable="false" width="0" height="0"><defs>'
            '<symbol id="h-square" viewBox="0 0 128 128"><rect x="0" y="0" width="128" height="128"/></symbol>'
            f'<symbol id="h-rounded" viewBox="0 0 128 128"><path d="{T.ROUNDED_D}"/></symbol>'
            '<symbol id="h-circle" viewBox="0 0 128 128"><circle cx="64" cy="64" r="64"/></symbol>'
            '</defs></svg>')


def card(ic):
    tile = (f'<svg class="ic" viewBox="0 0 128 128" aria-hidden="true" focusable="false">{HOLDERS}'
            f'<g class="glyph">{ic["svg"].replace("__P__", "g-" + ic["id"].lower() + "-")}</g></svg>'
            if ic["svg"] else '<span class="pending">Not traced yet</span>')
    label = html.escape(ic["label"])
    shown = html.escape(ic["labelNb"])
    hay = html.escape(f'{ic["id"]} {ic["label"]} {ic["slug"]}'.lower())
    optics = f'--a:{ic["a"]:g};--dx:{ic["dx"]:g};--tk:{ic["sk"]:g}'
    return (f'<li class="cell" data-id="{ic["id"]}" data-sheet="{ic["sheet"]}" data-hay="{hay}" style="{optics}">'
            f'<button type="button" class="card" data-open="{ic["id"]}" aria-label="{ic["id"]} {label}, open details">'
            f'<span class="tile">{tile}</span>'
            f'<span class="cid">{ic["id"]}</span><span class="cname">{shown}</span>'
            f'<span class="minnote" hidden></span></button></li>')


CSS = """
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@600;700&display=swap");
/* Layout: a masthead, then a sticky tool bar over the five source sheets as sections of specimen tiles; a dialog shows one icon at review scale with its editions and tiles. */
:root {
__LIGHT__  --font-display: "Inter Tight", "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-body: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --icon-size: 64px;
  --card-min: 128px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
__DARK__    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
__DARKROOT__  color-scheme: dark;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font-family: var(--font-body); font-size: 15px; line-height: 1.5;
  -webkit-text-size-adjust: 100%;
}
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); }
.wrap {
  max-width: 1320px; margin: 0 auto;
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 0 48px;
}
.masthead { padding-block: 40px 20px; display: grid; gap: 12px; }
.eyebrow { font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin: 0; }
h1 { font-family: var(--font-display); font-weight: 700; font-size: clamp(30px, 4.4vw, 48px); line-height: 1.05; letter-spacing: -0.01em; margin: 0; text-wrap: balance; }
.lead { max-width: 65ch; margin: 0; color: var(--text); }
.facts { display: flex; flex-wrap: wrap; gap: 8px 24px; margin: 8px 0 0; padding: 0; list-style: none; font-size: 13px; color: var(--muted); font-variant-numeric: tabular-nums; }
.facts b { color: var(--text); font-weight: 600; }
.toolbar {
  position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg);
  display: flex; flex-wrap: wrap; align-items: end; gap: 12px 20px; padding-block: 12px;
  border-bottom: 1px solid var(--hair);
}
.field { display: grid; gap: 4px; min-width: 0; }
.field > span, .field legend { font-size: 13px; font-weight: 600; color: var(--muted); }
fieldset.field { border: 0; margin: 0; padding: 0; }
fieldset.field legend { padding: 0; margin-bottom: 4px; }
input[type="search"], select {
  font: inherit; font-size: 15px; color: var(--text); background: var(--bg);
  border: 1px solid var(--line); border-radius: 6px; padding: 7px 10px; min-height: 40px;
}
input[type="search"] { width: min(280px, 100%); }
.search { flex: 1 1 220px; }
.seg { display: inline-flex; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }
.seg label { position: relative; }
.seg input { position: absolute; opacity: 0; inset: 0; margin: 0; cursor: pointer; }
.seg span { display: block; padding: 8px 12px; min-height: 38px; font-size: 14px; font-variant-numeric: tabular-nums; color: var(--text); border-left: 1px solid var(--line); cursor: pointer; white-space: nowrap; }
.seg { max-width: 100%; flex-wrap: wrap; }
.seg label:first-child span { border-left: 0; }
.seg input:checked + span { background: var(--accent); color: var(--on-accent); }
.seg input:focus-visible + span { outline: 3px solid var(--focus); outline-offset: -3px; }
.count { font-size: 13px; color: var(--muted); margin: 0 0 0 auto; font-variant-numeric: tabular-nums; align-self: center; }
:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.sheet { margin-top: 28px; }
.sheet h2 { font-family: var(--font-display); font-weight: 600; font-size: 20px; margin: 0 0 12px; display: flex; flex-wrap: wrap; gap: 4px 12px; align-items: baseline; text-wrap: balance; }
.sheet h2 small { font-family: var(--font-body); font-size: 13px; font-weight: 500; color: var(--muted); font-variant-numeric: tabular-nums; }
.grid { list-style: none; margin: 0; padding: 0; display: grid; gap: 16px 12px; grid-template-columns: repeat(auto-fill, minmax(min(var(--card-min), 100%), 1fr)); }
.cell { min-width: 0; }
.card {
  all: unset; box-sizing: border-box; display: grid; gap: 2px; width: 100%; cursor: pointer;
  border-radius: 8px; padding: 0 0 4px; color: var(--text);
}
.card:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
.tile {
  display: grid; place-items: center; background: var(--card-ground); border-radius: 6px;
  height: calc(var(--icon-size) + 40px); max-width: 100%; margin-bottom: 6px;
}
main:not([data-holder="none"]) .tile { background: var(--stage); }
.card:hover .tile { box-shadow: inset 0 0 0 2px var(--focus); }
.ic { width: var(--icon-size); height: var(--icon-size); display: block; overflow: visible; }
.sprite { position: absolute; width: 0; height: 0; overflow: hidden; }
.hold { display: none; fill: var(--holder-fill); }
main[data-holder="square"] .h-square, main[data-holder="rounded"] .h-rounded, main[data-holder="circle"] .h-circle { display: inline; }
.glyph { transform-origin: 64px 64px; transform: scale(var(--f, 1)); }
main:not([data-holder="none"]) .glyph { --k: var(--tk, 1); transform: translate(calc(var(--f) * var(--dx, 0) * 1px), 0px) scale(calc(var(--f) * var(--a, 1))); }
main[data-holder="square"] { --f: __F_SQUARE__; }
main[data-holder="rounded"] { --f: __F_ROUNDED__; }
main[data-holder="circle"] { --f: __F_CIRCLE__; }
.ed-red-black, main[data-edition="red-black"], dialog[data-edition="red-black"] { --icon-ink: var(--charcoal); --icon-accent: var(--pillar-red); --card-ground: var(--newsprint); --holder-fill: var(--newsprint); --stage: var(--charcoal); }
.ed-black, main[data-edition="black"], dialog[data-edition="black"] { --icon-ink: var(--charcoal); --icon-accent: var(--charcoal); --card-ground: var(--newsprint); --holder-fill: var(--newsprint); --stage: var(--charcoal); }
.ed-red-newsprint, main[data-edition="red-newsprint"], dialog[data-edition="red-newsprint"] { --icon-ink: var(--newsprint); --icon-accent: var(--pillar-red); --card-ground: var(--charcoal); --holder-fill: var(--charcoal); --stage: var(--newsprint); }
.ed-newsprint, main[data-edition="newsprint"], dialog[data-edition="newsprint"] { --icon-ink: var(--newsprint); --icon-accent: var(--newsprint); --card-ground: var(--charcoal); --holder-fill: var(--charcoal); --stage: var(--newsprint); }
.variants { display: grid; gap: 12px; }
.variants h3 { font-size: 14px; font-weight: 600; margin: 0; }
.spec-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(124px, 1fr)); gap: 14px 12px; margin: 0; padding: 0; list-style: none; }
.spec-grid.four { grid-template-columns: repeat(auto-fill, 140px); }
.tile-row { display: grid; gap: 6px; }
.row-label { font-size: 13px; font-weight: 600; margin: 0; color: var(--text); }
.spec { margin: 0; display: grid; gap: 6px; justify-items: start; min-width: 0; }
.spec .stage { width: 120px; height: 120px; display: grid; place-items: center; border-radius: 6px; background: var(--card-ground); }
.spec.on-stage .stage { background: var(--stage); }
.spec.on-prussian .stage { background: var(--prussian); }
.spec svg { width: 96px; height: 96px; display: block; }
.spec .hold { display: inline; }
.spec figcaption { font-size: 13px; color: var(--muted); line-height: 1.35; }
.pending { font-size: 13px; color: var(--charcoal); padding: 8px; text-align: center; }
.cid { font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; color: var(--muted); }
.cname { font-size: 14px; line-height: 1.3; overflow-wrap: normal; hyphens: manual; }
.minnote { font-size: 12px; line-height: 1.3; color: var(--muted); }
.minnote[hidden] { display: none; }
.empty { margin: 40px 0; font-size: 15px; }
.empty button { font: inherit; color: var(--text); background: none; border: 0; padding: 0; text-decoration: underline; cursor: pointer; }
.notes { margin-top: 48px; padding-top: 20px; border-top: 1px solid var(--hair); display: grid; gap: 12px; max-width: 72ch; font-size: 14px; }
.notes h2 { font-family: var(--font-display); font-size: 18px; margin: 0; }
.notes p { margin: 0; }
dialog {
  width: min(1120px, calc(100vw - 24px)); max-height: calc(100dvh - 24px); padding: 0;
  border: 1px solid var(--line); border-radius: 10px; background: var(--raised); color: var(--text);
}
dialog::backdrop { background: var(--scrim); }
.dlg { padding: 20px max(16px, env(safe-area-inset-left, 0px)) 24px; display: grid; gap: 20px; }
.dlg-head { display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: start; justify-content: space-between; }
.dlg-head h2 { font-family: var(--font-display); font-size: clamp(22px, 3vw, 30px); margin: 0; line-height: 1.1; text-wrap: balance; }
.dlg-head p { margin: 4px 0 0; font-size: 13px; color: var(--muted); font-variant-numeric: tabular-nums; }
.dlg-nav { display: flex; gap: 8px; }
.btn { font: inherit; font-size: 14px; color: var(--text); background: var(--raised); border: 1px solid var(--line); border-radius: 6px; padding: 7px 12px; min-height: 40px; cursor: pointer; }
.btn:hover { box-shadow: inset 0 0 0 1px var(--text); }
.chip { display: inline-block; font-size: 13px; font-weight: 600; padding: 2px 8px; border-radius: 999px; background: var(--chip); color: var(--on-chip); }
.compare { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 16px; }
figure { margin: 0; display: grid; gap: 6px; min-width: 0; }
figcaption { font-size: 13px; color: var(--muted); }
.view { width: min(100%, var(--vw)); aspect-ratio: var(--ar); background: var(--tile); border-radius: 4px; overflow: hidden; }
.view.trace { background: var(--card-ground); }
.view img, .view svg { display: block; width: 100%; height: 100%; image-rendering: pixelated; }
.facts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 20px 28px; }
.facts-grid h3 { font-size: 14px; font-weight: 600; margin: 0 0 8px; }
dl.metrics { display: grid; grid-template-columns: max-content 1fr; gap: 4px 16px; margin: 0; font-size: 14px; font-variant-numeric: tabular-nums; }
dl.metrics dt { color: var(--muted); }
dl.metrics dd { margin: 0; }
ol.corr { margin: 0; padding-left: 20px; display: grid; gap: 8px; font-size: 14px; }
ol.corr .why { color: var(--muted); display: block; }
.prose { font-size: 14px; margin: 0; max-width: 72ch; }
.small { font-size: 13px; color: var(--muted); margin: 0; }
@media (prefers-reduced-motion: no-preference) {
  .tile { transition: box-shadow 120ms ease-out; }
}
@media (max-width: 560px) {
  .toolbar { position: static; gap: 12px; }
  .count { margin-left: 0; width: 100%; }
  .seg span { padding: 8px 10px; }
}
@media (max-width: 400px) {
  .seg span { padding: 8px 8px; font-size: 13px; }
}
"""

JS = r"""
(function () {
  var data = JSON.parse(document.getElementById('cl-data').textContent);
  var byId = {}; data.icons.forEach(function (ic, k) { ic.k = k; byId[ic.id] = ic; });
  var main = document.getElementById('catalog');
  var dlg = document.getElementById('detail');
  var q = document.getElementById('q');
  var sheetSel = document.getElementById('sheet');
  var countEl = document.getElementById('count');
  var empty = document.getElementById('empty');
  var cells = Array.prototype.slice.call(document.querySelectorAll('.cell'));
  var sizes = { '24': 124, '32': 124, '48': 124, '64': 128, '128': 168 };   // 124 px holds the widest label word, Emergency-Power, on one line
  var lastOpener = null, current = null, visibleIds = [];

  function store(k, v) { try { localStorage.setItem('civic-line-' + k, v); } catch (e) {} }
  function recall(k) { try { return localStorage.getItem('civic-line-' + k); } catch (e) { return null; } }
  function edition() { return document.querySelector('input[name="edition"]:checked').value; }
  function setEdition(v) {
    main.setAttribute('data-edition', v); dlg.setAttribute('data-edition', v); store('edition', v);
    markMin();
    if (dlg.open && current) render(current);
  }
  function setHolder(v) { main.setAttribute('data-holder', v); store('holder', v); markMin(); }
  function setSize(v) {
    main.style.setProperty('--icon-size', v + 'px');
    main.style.setProperty('--card-min', (sizes[v] || 112) + 'px');
    store('size', v);
    markMin();
  }
  // M-1: a tile shown below the icon's minimum tile size says so on its card
  function markMin() {
    var hEl = document.querySelector('input[name="holder"]:checked'), sEl = document.querySelector('input[name="size"]:checked');
    if (!hEl || !sEl) return;
    var h = hEl.value, px = Number(sEl.value), ed = edition();
    var mode = (ed === 'red-black' || ed === 'red-newsprint') ? 'two-color' : 'one-color';
    cells.forEach(function (c) {
      var ic = byId[c.getAttribute('data-id')], note = c.querySelector('.minnote'), b = c.querySelector('.card');
      var min = h === 'none' || !ic ? 0 : ic.min[mode][h];
      var below = min > 0 && px < min;
      c.classList.toggle('below-min', below);
      note.hidden = !below;
      note.textContent = below ? 'Below the tile minimum (' + min + ' px)' : '';
      b.setAttribute('aria-label', ic.id + ' ' + ic.label + (below ? ', tile below its ' + min + ' px minimum' : '') + ', open details');
    });
  }
  function apply() {
    var term = q.value.trim().toLowerCase(), sh = sheetSel.value, n = 0;
    visibleIds = [];
    cells.forEach(function (c) {
      var ok = (!term || c.getAttribute('data-hay').indexOf(term) !== -1) && (!sh || c.getAttribute('data-sheet') === sh);
      c.hidden = !ok; if (ok) { n++; visibleIds.push(c.getAttribute('data-id')); }
    });
    document.querySelectorAll('.sheet').forEach(function (s) {
      var shown = s.querySelectorAll('.cell:not([hidden])').length;
      s.hidden = shown === 0;
      s.querySelector('[data-shown]').textContent = shown + (shown === 1 ? ' icon' : ' icons');
    });
    countEl.textContent = 'Showing ' + n + ' of ' + data.icons.length + ' icons';
    empty.hidden = n !== 0;
    if (n === 0) document.getElementById('empty-term').textContent = term ? '"' + q.value.trim() + '"' : 'this sheet';
  }
  function fmt(v, d) { return v === null || v === undefined ? 'not measured' : Number(v).toFixed(d); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var EDS = [['red-black', 'Red-black'], ['black', 'Black'], ['red-newsprint', 'Red-newsprint'], ['newsprint', 'Newsprint']];
  var TILES = [['charcoal', 'two-color', 'red-newsprint'], ['charcoal', 'one-color', 'newsprint'],
               ['newsprint', 'two-color', 'red-black'], ['newsprint', 'one-color', 'black']];
  var SHAPES = [['square', 'Square'], ['rounded', 'Rounded square'], ['circle', 'Circle']];
  function edName(ed) { for (var i = 0; i < EDS.length; i++) if (EDS[i][0] === ed) return EDS[i][1]; return ed; }
  function glyph(ic, pre) { return ic.svg.split('__P__').join(pre); }
  function variants(ic) {
    if (!ic.svg) return '';
    var base = ic.id.toLowerCase(), out = '<section class="variants"><h3>The four editions, 96 px, each on its ground, and Newsprint on Prussian</h3><ul class="spec-grid">';
    EDS.concat([['newsprint', 'Newsprint on Prussian', 'prussian']]).forEach(function (e) {
      var cls = 'spec ed-' + e[0] + (e[2] ? ' on-prussian' : ''), key = e[2] || e[0];
      out += '<li><figure class="' + cls + '"><div class="stage"><svg viewBox="0 0 128 128" role="img" aria-label="' + esc(ic.label) + ', ' + e[1] + (e[2] ? '' : ' edition') + '">' +
        glyph(ic, 'v-' + key + '-' + base + '-') + '</svg></div><figcaption>' + e[1] + '</figcaption></figure></li>';
    });
    out += '</ul><h3>The twelve tiles, 96 px</h3>';
    SHAPES.forEach(function (sh) {
      var f = data.factors[sh[0]], fa = f * ic.a, tx = (64 * (1 - fa) + f * ic.dx).toFixed(4), t = (64 * (1 - fa)).toFixed(4);
      var at = ic.a === 1 ? String(f) : (Math.round(fa * 1000) / 1000) + ' (' + f + ' times optical scale ' + ic.a + ')';
      var mins = ic.min['two-color'][sh[0]] + ' px two-color, ' + ic.min['one-color'][sh[0]] + ' px one-color';
      out += '<div class="tile-row"><p class="row-label">' + sh[1] + ', icon at ' + at + (ic.dx ? ', moved ' + Math.abs(Math.round(f * ic.dx * 100) / 100) + ' units ' + (ic.dx > 0 ? 'right' : 'left') : '') +
        '. Smallest size ' + mins + '.</p><ul class="spec-grid four">';
      TILES.forEach(function (tl) {
        var cap = (tl[0] === 'charcoal' ? 'Charcoal' : 'Newsprint') + ', ' + tl[1];
        out += '<li><figure class="spec on-stage ed-' + tl[2] + '"><div class="stage"><svg viewBox="0 0 128 128" role="img" aria-label="' + esc(ic.label) + ' tile: ' + sh[1] + ', ' + cap + '">' +
          '<use class="hold" href="#h-' + sh[0] + '" x="0" y="0" width="128" height="128"/>' +
          '<g transform="matrix(' + fa + ' 0 0 ' + fa + ' ' + tx + ' ' + t + ')" style="--k:' + ic.sk + '">' + glyph(ic, 't-' + sh[0] + '-' + tl[0] + '-' + tl[1] + '-' + base + '-') + '</g></svg></div>' +
          '<figcaption>' + cap + '</figcaption></figure></li>';
      });
      out += '</ul></div>';
    });
    return out + '</section>';
  }
  function render(ic) {
    current = ic;
    var ed = edition(), z = ic.w * 3 <= 520 ? 3 : 2;
    var two = ed === 'red-black' || ed === 'red-newsprint';
    var m = ic.m || {};
    var trace = ic.svg
      ? '<svg viewBox="' + ic.vb + '" role="img" aria-label="Trace of ' + esc(ic.label) + ', ' + edName(ed) + ' edition">' + glyph(ic, 'd-' + ic.id.toLowerCase() + '-') + '</svg>'
      : '<p class="pending">Not traced yet</p>';
    var corr = ic.corr.length
      ? '<ol class="corr">' + ic.corr.map(function (c) { return '<li>' + esc(c.what) + (c.el ? ' (element ' + esc(c.el) + ')' : '') + '<span class="why">' + esc(c.why) + '</span></li>'; }).join('') + '</ol>'
      : '<p class="small">No corrections logged.</p>';
    var pos = visibleIds.indexOf(ic.id);
    document.getElementById('dlg-body').innerHTML =
      '<div class="dlg-head"><div><h2 id="dlg-title">' + ic.id + ' ' + esc(ic.labelNb) + '</h2>' +
      '<p>Sheet ' + ic.sheet + ', row ' + ic.row + ', column ' + ic.col + ' &middot; crop ' + ic.w + ' &times; ' + ic.h + ' px &middot; shown at ' + z + 'x &middot; <span class="chip">' + ic.state + '</span></p></div>' +
      '<div class="dlg-nav"><button type="button" class="btn" data-step="-1"' + (pos <= 0 ? ' disabled' : '') + '>Previous</button>' +
      '<button type="button" class="btn" data-step="1"' + (pos < 0 || pos >= visibleIds.length - 1 ? ' disabled' : '') + '>Next</button>' +
      '<button type="button" class="btn" data-close>Close</button></div></div>' +
      '<div class="compare" style="--vw:' + (ic.w * z) + 'px;--ar:' + ic.w + ' / ' + ic.h + '">' +
      '<figure><div class="view"><img alt="Reference crop of ' + esc(ic.label) + ' from the ' + (two ? 'red' : 'black') + ' sheet" src="' + (two ? ic.refRed : ic.refBlack) + '"></div>' +
      '<figcaption>Reference crop, ' + (two ? 'red' : 'black') + ' sheet: untouched source pixels</figcaption></figure>' +
      '<figure><div class="view trace">' + trace + '</div><figcaption>Trace, ' + edName(ed) + ' edition, at the same scale</figcaption></figure></div>' +
      variants(ic) +
      '<div class="facts-grid"><section><h3>Measurements against the reference</h3><dl class="metrics">' +
      '<dt>Silhouette IoU</dt><dd>' + fmt(m.sil, 3) + '</dd>' +
      '<dt>Red IoU</dt><dd>' + fmt(m.red, 3) + '</dd>' +
      '<dt>Edge distance, mean</dt><dd>' + fmt(m.em, 2) + ' px</dd>' +
      '<dt>Edge distance, 95th pct</dt><dd>' + fmt(m.ep, 2) + ' px</dd>' +
      '<dt>Edge distance, max</dt><dd>' + fmt(m.ex, 2) + ' px</dd>' +
      '<dt>Best offset</dt><dd>' + (m.off ? '(' + m.off[0] + ', ' + m.off[1] + ') px' : 'not measured') + '</dd>' +
      '<dt>Ink ratio, trace to reference</dt><dd>' + fmt(m.ratio, 3) + '</dd>' +
      '<dt>Bake check at 4x</dt><dd>' + fmt(m.b4, 4) + (m.b1 !== undefined && m.b1 !== null ? ' (1x ' + fmt(m.b1, 4) + ')' : '') + '</dd>' +
      '<dt>Builds</dt><dd>' + ic.builds + '</dd><dt>Tracer</dt><dd>' + (esc(ic.tracer) || 'none yet') + '</dd></dl>' +
      '<p class="small" style="margin-top:8px">IoU compares two shapes: 1 means identical. Edge distance is how far the trace\'s edges sit from the reference\'s, in source pixels.</p></section>' +
      '<section><h3>Corrections logged by the tracer</h3>' + corr + (ic.notes ? '<p class="prose" style="margin-top:8px">' + esc(ic.notes) + '</p>' : '') + '</section>' +
      '<section><h3>Catalog description</h3><p class="prose"><b>Construction:</b> ' + esc(ic.construction) + '</p><p class="prose" style="margin-top:8px"><b>Accent:</b> ' + esc(ic.redText) + '</p></section></div>';
  }
  function open(id, opener) {
    var ic = byId[id]; if (!ic) return;
    lastOpener = opener || document.querySelector('[data-open="' + id + '"]');
    render(ic);
    if (!dlg.open) dlg.showModal();
    try { history.replaceState(null, '', '#' + id.toLowerCase()); } catch (e) {}
    var c = dlg.querySelector('[data-close]'); if (c) c.focus();
  }
  dlg.addEventListener('close', function () {
    try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
    if (lastOpener) lastOpener.focus();
  });
  dlg.addEventListener('click', function (e) {
    if (e.target === dlg) { dlg.close(); return; }
    var b = e.target.closest('button'); if (!b) return;
    if (b.hasAttribute('data-close')) dlg.close();
    if (b.hasAttribute('data-step') && current) {
      var pos = visibleIds.indexOf(current.id) + Number(b.getAttribute('data-step'));
      if (pos >= 0 && pos < visibleIds.length) { open(visibleIds[pos], document.querySelector('[data-open="' + visibleIds[pos] + '"]')); }
    }
  });
  main.addEventListener('click', function (e) {
    var b = e.target.closest('[data-open]'); if (b) open(b.getAttribute('data-open'), b);
  });
  q.addEventListener('input', apply);
  sheetSel.addEventListener('change', apply);
  document.getElementById('clear').addEventListener('click', function () { q.value = ''; sheetSel.value = ''; apply(); q.focus(); });
  document.querySelectorAll('input[name="edition"]').forEach(function (r) { r.addEventListener('change', function () { setEdition(r.value); }); });
  document.querySelectorAll('input[name="size"]').forEach(function (r) { r.addEventListener('change', function () { setSize(r.value); }); });
  document.querySelectorAll('input[name="holder"]').forEach(function (r) { r.addEventListener('change', function () { setHolder(r.value); }); });
  var e0 = recall('edition'), s0 = recall('size'), h0 = recall('holder');
  if (h0 && document.querySelector('input[name="holder"][value="' + h0 + '"]')) document.querySelector('input[name="holder"][value="' + h0 + '"]').checked = true;
  if (e0 && document.querySelector('input[name="edition"][value="' + e0 + '"]')) document.querySelector('input[name="edition"][value="' + e0 + '"]').checked = true;
  if (s0 && document.querySelector('input[name="size"][value="' + s0 + '"]')) document.querySelector('input[name="size"][value="' + s0 + '"]').checked = true;
  setEdition(edition());
  setSize(document.querySelector('input[name="size"]:checked').value);
  setHolder(document.querySelector('input[name="holder"]:checked').value);
  apply();
  function fromHash() {
    var h = (location.hash || '').slice(1).toUpperCase();
    if (h && byId[h]) open(h);
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();
"""


def build():
    inv, icons = gather()
    css = CSS.replace("__LIGHT__", tokens(LIGHT)).replace("__DARK__", tokens(DARK, "    ")).replace("__DARKROOT__", tokens(DARK))
    for k, v in C.TILE_FACTORS.items():
        css = css.replace(f"__F_{k.upper()}__", f"{v:g}")
    lo, hi = inv["stroke_width_units"]
    built = sum(1 for ic in icons if ic["svg"])
    reviewed = sum(1 for ic in icons if ic["svg"] and ic.get("state") == "reviewed")
    sections = []
    for key, name in SHEET_NAMES.items():
        cells = [ic for ic in icons if ic["sheet"] == key]
        sections.append(
            f'<section class="sheet" id="sheet-{key}" aria-labelledby="h-{key}"><h2 id="h-{key}">Sheet {key}: {html.escape(name)} '
            f'<small data-shown>{len(cells)} icons</small></h2>'
            f'<ul class="grid">{"".join(card(ic) for ic in cells)}</ul></section>')
    sheet_opts = "".join(f'<option value="{k}">{k} {html.escape(v)}</option>' for k, v in SHEET_NAMES.items())
    size_opts = "".join(f'<label><input type="radio" name="size" value="{s}"{" checked" if s == 64 else ""}><span>{s}</span></label>' for s in (24, 32, 48, 64, 128))
    payload = json.dumps({"icons": icons, "factors": C.TILE_FACTORS}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    body = f"""<title>Civic Line Icons</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>{css}</style>
<div class="wrap">
<header class="masthead">
<p class="eyebrow">Oath &amp; Action, Edition 06</p>
<h1>Civic Line icons</h1>
<p class="lead">All {len(icons)} Civic Line icons, traced as vector masters from the reference sheets you sent on October 29. Search by ID or name, pick an edition and a holder, and open any icon to see its untouched reference crop beside the trace, its four editions, its twelve tiles, its measurements and the tracer's corrections.</p>
<ul class="facts">
<li><b>{len(icons)}</b> icons in five sheets</li>
<li><b>4</b> editions from one drawing</li>
<li><b>12</b> tiles per icon</li>
<li>128-unit box, capped fit; stroke <b>{lo:.2f}</b> to <b>{hi:.2f}</b> units</li>
<li><b>{reviewed}</b> of {len(icons)} passed the independent review</li>
</ul>
</header>
<div class="toolbar" role="search" aria-label="Filter icons">
<label class="field search"><span>Search ID or name</span><input type="search" id="q" placeholder="R-35 or term limits" autocomplete="off"></label>
<fieldset class="field"><legend>Edition</legend><div class="seg">
<label><input type="radio" name="edition" id="ed-rb" value="red-black" checked><span>Red-black</span></label>
<label><input type="radio" name="edition" id="ed-bk" value="black"><span>Black</span></label>
<label><input type="radio" name="edition" id="ed-rn" value="red-newsprint"><span>Red-newsprint</span></label>
<label><input type="radio" name="edition" id="ed-nw" value="newsprint"><span>Newsprint</span></label></div></fieldset>
<fieldset class="field"><legend>Holder</legend><div class="seg">
<label><input type="radio" name="holder" id="ho-none" value="none" checked><span>None</span></label>
<label><input type="radio" name="holder" id="ho-square" value="square"><span>Square</span></label>
<label><input type="radio" name="holder" id="ho-rounded" value="rounded"><span>Rounded</span></label>
<label><input type="radio" name="holder" id="ho-circle" value="circle"><span>Circle</span></label></div></fieldset>
<label class="field"><span>Sheet</span><select id="sheet"><option value="">All sheets</option>{sheet_opts}</select></label>
<fieldset class="field"><legend>Size in px</legend><div class="seg">{size_opts}</div></fieldset>
<p class="count" id="count" aria-live="polite">Showing {len(icons)} of {len(icons)} icons</p>
</div>
<main id="catalog" data-edition="red-black" data-holder="none">
{"".join(sections)}
<p class="empty" id="empty" hidden>No icon matches <span id="empty-term"></span>. <button type="button" id="clear">Clear the search and sheet filter</button></p>
</main>
<footer class="notes">
<h2>About these files</h2>
<p>Each icon is a traced reconstruction: a clean vector drawing measured against the source sheet, with one line weight across the set. It is not a pixel copy. The reference crops in the detail view are the untouched source pixels, shown for comparison.</p>
<p>Four editions share every coordinate. Red-black and black draw in Charcoal for Newsprint and White grounds; red-newsprint and newsprint draw in Newsprint for Charcoal grounds, and newsprint alone also serves Prussian, where red never sits. Pillar Red on Newsprint measures 2.96:1, under the 3:1 guideline for graphics, so the red parts carry emphasis and never the only meaning.</p>
<p>The holders are a square, a rounded square drawn as a continuous-curvature superellipse, and a circle. A Charcoal tile carries the light editions and a Newsprint tile the dark ones. In a tile the icon scales by {C.TILE_FACTORS["square"]:g} (square), {C.TILE_FACTORS["rounded"]:g} (rounded) or {C.TILE_FACTORS["circle"]:g} (circle), times an optical scale between 0.94 and 1.09 for the {len(C.TILE_OPTICAL_SCALE)} icons that read small or large, and {len(C.TILE_OFFSET_X)} icons move a little toward their light side.</p>
<p>A two-color tile needs at least 72 px (square), 76 px (rounded) or 80 px (circle). A one-color tile needs 48, 52 or 52 px, or 72, 76 or 80 px for the 28 icons that need 48 px on their own. With a holder on, a card whose tile sits below its minimum says so.</p>
<p>The icons read best from 48 px up. At 24 px the stroke is about half a pixel wide. R-35 records an option the atlas rejected, so its name stays "Term Limits · Rejected".</p>
<p>The sheets were supplied by Dustin Cathcart, and the studio traced them under decision DR-02.</p>
</footer>
</div>
<dialog id="detail" aria-labelledby="dlg-title" data-edition="red-black"><div class="dlg" id="dlg-body"></div></dialog>
{sprite()}
<script type="application/json" id="cl-data">{payload}</script>
<script>{JS}</script>
"""
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(body)
    size = os.path.getsize(OUT)
    if "—" in body:
        raise SystemExit("an em dash slipped into the catalog")
    if size > LIMIT:
        raise SystemExit(f"catalog is {size / 1e6:.2f} MB, over the 12 MB limit")
    print(f"wrote {os.path.relpath(OUT, C.ROOT)}: {size / 1024 / 1024:.2f} MB, {len(icons)} icons, {built} with traces")


if __name__ == "__main__":
    build()
