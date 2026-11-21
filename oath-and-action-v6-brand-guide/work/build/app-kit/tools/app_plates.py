"""The application kit's hook in the guide build (chat 11, contract C4): a specimen asks for an application by its id, and
the build places the frames the kit drew, from work/build/app-kit/plates/<id>.json, with no second renderer on the page.

guide_build.py imports this module. Its self-test runs alone:
    python3 -I work/build/app-kit/tools/app_plates.py --self-test

A specimen holds one placeholder per row of frames:
    <div data-oa-app="A05" data-oa-app-views="1440-light 390-light"></div>
The frames listed share one row at one scale (each frame grows by its true width), so a 1440 px page and a 390 px page sit
side by side in proportion. The kit wrote each frame as a picture of the working page: an SVG named by its alt, whose
markup is inert and hidden from the accessibility tree (data-oa-page-frame). Only this hook writes that markup; a specimen
that carries it in its own file is a warning, and so is a plate older than any file the kit read to draw it.
"""
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PLATES = ROOT / "work/build/app-kit/plates"
PLATE_CSS_JS = ROOT / "work/build/app-kit/lib.mjs"     # PLATE_CSS, the frames' own style, is read from the kit's code
PLACEHOLDER = re.compile(r'<div data-oa-app="(A\d{2,3})"((?:\s+data-oa-app-[a-z]+="[^"]*")*)\s*>\s*</div>')
ATTR = re.compile(r'data-oa-app-([a-z]+)="([^"]*)"')
FRAME_ATTR = "data-oa-page-frame"
# a page frame as the kit writes it, from its opening tag to the end of its svg, for the checks that leave it alone
FRAME_RE = re.compile(r'<div class="oa-app-frame[^"]*"[^>]*\sdata-oa-page-frame="[^"]*"[^>]*>.*?</foreignObject>.*?</svg></div>', re.S)

STATE = {"types": {}, "plates": {}, "dir": PLATES}


def reset(plates_dir=None):
    STATE["types"].clear()
    STATE["plates"].clear()
    STATE["dir"] = Path(plates_dir) if plates_dir else PLATES


def _load(app_id):
    if app_id in STATE["plates"]:
        return STATE["plates"][app_id]
    p = STATE["dir"] / f"{app_id.lower()}.json"
    data = json.loads(p.read_text()) if p.exists() else None
    STATE["plates"][app_id] = data
    return data


def stale(data):
    """The inputs whose bytes changed since the kit drew the plate (or that are gone)."""
    out = []
    for rel, h in sorted((data.get("inputs") or {}).items()):
        f = ROOT / rel
        if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != h:
            out.append(rel)
    return out


def raw_frames(src):
    """True when a specimen's own file carries the kit's frame markup, which only this hook writes."""
    return FRAME_ATTR in src


def expand(src, sid, warn):
    """Put the kit's frames in place of each placeholder in the specimen. warn(message) reports a fault."""
    def repl(m):
        attrs = dict(ATTR.findall(m.group(2) or ""))
        app_id, views = m.group(1), attrs.get("views", "").split()
        unknown_attrs = sorted(set(attrs) - {"views", "title"})
        if unknown_attrs:
            warn(f"{sid}: the placeholder for {app_id} carries data-oa-app-{unknown_attrs[0]}, which the hook does not read (contract C4)")
        data = _load(app_id)
        if not data:
            warn(f"{sid}: no plate for {app_id} in {STATE['dir'].relative_to(ROOT) if ROOT in STATE['dir'].parents else STATE['dir']}; "
                 f"run node work/build/app-kit/oa-app.mjs build {app_id} (contract C4)")
            return m.group(0)
        old = stale(data)
        if old:
            warn(f"{sid}: the kit's plate {app_id} is older than {len(old)} of its inputs ({', '.join(old[:3])}); "
                 f"run node work/build/app-kit/oa-app.mjs build {app_id} (contract C4)")
        by_key = {v["key"]: v for v in data["views"]}
        keys = views or [v["key"] for v in data["views"]]
        unknown = [k for k in keys if k not in by_key]
        if unknown:
            warn(f"{sid}: {app_id} has no view {', '.join(unknown)}; it draws {', '.join(by_key)}")
        chosen = [by_key[k] for k in keys if k in by_key]
        if not chosen:
            return m.group(0)
        STATE["types"].setdefault(data["type"], data.get("css") or f"{data['type']}.css")
        STATE["types"].setdefault("plate", None)
        frames = []
        for v in chosen:
            # one scale for the row: each frame grows by its true width and never past it
            fr = v["html"].replace('<div class="oa-app-frame"', f'<div class="oa-app-frame" style="flex:{v["w"]} 1 0;max-width:{v["w"]}px"', 1)
            frames.append(fr)
        title = ""
        if "title" in attrs:
            if data.get("title"):
                title = (f'<p class="oa-app-title"><span class="oa-app-title-k">{html.escape(attrs["title"])}</span> '
                         f'<span class="oa-app-title-t">{html.escape(data["title"])}</span></p>')
            else:
                warn(f"{sid}: {app_id} has no page title to print (contract C4)")
        return title + f'<div class="oa-app-row" data-oa-app="{html.escape(app_id)}">' + "".join(frames) + "</div>"
    return PLACEHOLDER.sub(repl, src)


def outside_frames(s):
    """The fragment with every kit page frame taken out, for the checks a frame is allowed to meet (headings, controls)."""
    return FRAME_RE.sub("", s)


def frames_in(s):
    return len(FRAME_RE.findall(s))


def plate_css():
    t = PLATE_CSS_JS.read_text()
    m = re.search(r"export const PLATE_CSS = `(.*?)`;", t, re.S)
    return m.group(1).strip() if m else ""


def head_styles():
    """One style per renderer type the page placed, plus the frames' own style, for the page's head."""
    out = []
    for t, css_file in STATE["types"].items():
        if t == "plate":
            css = (plate_css() + "\n.oa-app-row[data-oa-app]{display:flex;flex-wrap:nowrap;gap:16px;align-items:flex-start}"
                   "\n.oa-app-title{margin:0 0 8px;font:var(--oa-type-caption-font-style) var(--oa-type-caption-font-weight) var(--oa-type-caption-font-size)/var(--oa-type-caption-line-height) var(--oa-type-caption-font-family);color:var(--oa-color-text-primary)}"
                   "\n.oa-app-title-k{font-weight:var(--oa-font-weight-bold);margin-right:8px}")
        else:
            p = STATE["dir"] / css_file
            css = p.read_text() if p.exists() else ""
        out.append(f'<style data-oa-app-kit="{html.escape(t)}">\n{css}\n</style>')
    return "\n".join(out)


STYLE_RE = re.compile(r'<style data-oa-app-kit="([^"]+)">.*?</style>', re.S)


def self_test():
    import tempfile
    bad = 0

    def check(name, ok):
        nonlocal bad
        print(f"{'pass' if ok else 'FAIL'} {name}")
        bad += not ok
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        inp = d / "input.txt"
        inp.write_text("one")
        rel = str(inp)   # absolute paths stay absolute when joined to ROOT
        frame = ('<div class="oa-app-frame" data-oa-page-frame="A99 390-light" data-oa-app-type="web-page" data-w="390" data-h="800">'
                 '<svg class="oa-app-scale" viewBox="0 0 390 800" role="img" aria-label="A fixture page at 390 px, on Newsprint.">'
                 '<foreignObject x="0" y="0" width="390" height="800"><div xmlns="http://www.w3.org/1999/xhtml" class="oa-app-art" inert '
                 'aria-hidden="true" data-oa-picture style="width:390px;height:800px"><h1>Title</h1><a href="#x">Link</a></div>'
                 '</foreignObject></svg></div>')
        (d / "a99.json").write_text(json.dumps({"id": "A99", "type": "web-page", "css": "web-page.css",
            "views": [{"key": "390-light", "w": 390, "h": 800, "theme": "light", "alt": "x", "html": frame},
                      {"key": "1440-light", "w": 1440, "h": 900, "theme": "light", "alt": "y", "html": frame.replace("390", "1440")}],
            "inputs": {rel: hashlib.sha256(b"one").hexdigest()}}))
        (d / "web-page.css").write_text(".wa{color:red}")
        reset(d)
        w = []
        out = expand('<p>Before</p><div data-oa-app="A99" data-oa-app-views="390-light"></div>', "s-20-x", w.append)
        check("a placeholder becomes its one chosen frame, in a row, with nothing to warn", out.count(FRAME_ATTR) == 1 and 'data-oa-app="A99"' in out and not w)
        check("the frame grows by its true width", 'style="flex:390 1 0;max-width:390px"' in out)
        check("the checks read the fragment without the frame", "<h1>" not in outside_frames(out) and "<p>Before</p>" in outside_frames(out))
        w = []
        out = expand('<div data-oa-app="A99"></div>', "s-20-x", w.append)
        check("no views named: every frame, in the plate's order", out.count(FRAME_ATTR) == 2 and out.index("390") < out.index("1440"))
        w = []
        expand('<div data-oa-app="A99" data-oa-app-views="768-light"></div>', "s-20-x", w.append)
        check("an unknown view warns", any("no view 768-light" in x for x in w))
        w = []
        expand('<div data-oa-app="A42"></div>', "s-20-x", w.append)
        check("an application with no plate warns", any("no plate for A42" in x for x in w))
        inp.write_text("two")
        reset(d)
        w = []
        expand('<div data-oa-app="A99"></div>', "s-20-x", w.append)
        check("a plate older than an input warns", any("older than 1 of its inputs" in x for x in w))
        check("a specimen that carries frame markup in its own file is caught", raw_frames(frame) and not raw_frames("<p>x</p>"))
        w = []
        data = json.loads((d / "a99.json").read_text()); data["title"] = "A fixture page | Oath & Action"; (d / "a99.json").write_text(json.dumps(data))
        reset(d)
        out = expand('<div data-oa-app="A99" data-oa-app-views="390-light" data-oa-app-title="Page title"></div>', "s-20-x", w.append)
        check("data-oa-app-title prints the page's own title above the row", '<span class="oa-app-title-k">Page title</span> <span class="oa-app-title-t">A fixture page | Oath &amp; Action</span>' in out
              and out.index("oa-app-title") < out.index("oa-app-row"))
        w = []
        expand('<div data-oa-app="A99" data-oa-app-size="2"></div>', "s-20-x", w.append)
        check("an attribute the hook does not read warns", any("data-oa-app-size" in x for x in w))
        hs = head_styles()
        check("the page's head gets each placed type's style once, and the frames' own", hs.count("<style") == 2 and ".wa{color:red}" in hs and ".oa-app-frame" in hs)
    reset()
    return bad


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(1 if self_test() else 0)
    print(__doc__)
