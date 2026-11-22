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

STATE = {"types": {}, "plates": {}, "dir": PLATES, "words": {}, "symbols": {}}
GENERATOR = "work/build/scripts/phase-4/phase4_ch20_build.py"   # DD-3: the chapter 20 generator prints the pages' words


def words_hash(app_id, generator=GENERATOR):
    """The SHA-256 of one application's words as the chapter generator prints them now (--page-words all, read-only), in a
    canonical JSON; None when the generator prints none for it. Cached for the run. An ID may name one key of an entry,
    "A06:site" (chat 11c: an atlas page's plate holds chapter 20's site words, not the home page's)."""
    import subprocess
    if generator not in STATE["words"]:
        r = subprocess.run(["python3", "-I", str(ROOT / generator), "--page-words", "all"], capture_output=True, text=True, cwd=str(ROOT))
        STATE["words"][generator] = json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else {}
    ids = str(app_id).split(",")
    got = STATE["words"][generator]

    def one(i):
        k, _, sub = i.partition(":")
        e = got.get(k)
        return e.get(sub) if (sub and isinstance(e, dict)) else (e if not sub else None)
    entry = one(ids[0]) if len(ids) == 1 else {i: one(i) for i in ids}
    if entry is None or (isinstance(entry, dict) and len(ids) > 1 and any(v is None for v in entry.values())):
        return None
    return hashlib.sha256(json.dumps(entry, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def reset(plates_dir=None):
    STATE["types"].clear()
    STATE["plates"].clear()
    STATE["words"].clear()
    STATE["symbols"].clear()
    STATE.pop("atlas_self_test", None)
    STATE["dir"] = Path(plates_dir) if plates_dir else PLATES


def _load(app_id):
    if app_id in STATE["plates"]:
        return STATE["plates"][app_id]
    p = STATE["dir"] / f"{app_id.lower()}.json"
    data = json.loads(p.read_text()) if p.exists() else None
    STATE["plates"][app_id] = data
    return data


def stale(data):
    """The inputs whose bytes changed since the kit drew the plate (or that are gone), and its words, where the plate took
    them from the chapter generator, if they changed since."""
    out = []
    # chat 11c: a plate may hold its words from more than one generator (an atlas page: chapter 21's and chapter 20's site)
    ws = data.get("words")
    for w in (ws if isinstance(ws, list) else [ws] if ws else []):
        if words_hash(w.get("id", data["id"]), w.get("generator", GENERATOR)) != w.get("sha256"):
            out.append(f"its words in {w.get('generator', GENERATOR)}")
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
        if data.get("provisional_words"):
            warn(f"{sid}: the kit drew {app_id} from stand-in words ({data['provisional_words']}), not the chapter generator's; "
                 f"run node work/build/app-kit/oa-app.mjs build {app_id} once the generator prints them (contract C4, DD-3)")
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
        # chat 11c (DR-319): an atlas plate stands on the website's style, which its frames need in the head too
        for t in data.get("styles") or []:
            STATE["types"].setdefault(t, f"{t}.css")
        # chat 11c (contract C9): an atlas plate carries the atlas test's result for its own frames and working page; a
        # FAIL, a self-test that failed or no result is a warning, so --strict fails (Rule 21.16)
        if data["type"] == "atlas-page":
            at = data.get("atlas_test")
            if not at:
                warn(f"{sid}: the kit's plate {app_id} carries no atlas test result; run node work/build/app-kit/oa-app.mjs build {app_id} (contract C9)")
            else:
                if at.get("fail"):
                    warn(f"{sid}: the atlas test fails {app_id} {at['fail']} time(s), first: {at.get('first_fail', '')} (Rule 21.16, contract C9)")
                if at.get("self_test") != "PASS":
                    warn(f"{sid}: the atlas test's self-test did not pass when the kit drew {app_id} ({at.get('self_test')}) (contract C9)")
            # the self-test again here, once a build, on the plates' own frames (a planted fault a check, caught by its check)
            if "atlas_self_test" not in STATE:
                import subprocess
                r = subprocess.run(["python3", "-I", str(ROOT / "work/build/app-kit/tools/atlas_test.py"), "--self-test", "--plates", str(STATE["dir"])],
                                   capture_output=True, text=True, cwd=str(ROOT))
                STATE["atlas_self_test"] = (r.returncode, (r.stdout or r.stderr).strip().splitlines()[-1:] or [""])
                if r.returncode:
                    warn(f"{sid}: the atlas test's self-test fails on the plates: {STATE['atlas_self_test'][1][0]} (Rule 21.16, contract C9)")
        # the identity masters the frames draw by <use>, carried once for the page (step 4)
        for sid_, sym in (data.get("symbols") or {}).items():
            if sid_ in STATE["symbols"] and STATE["symbols"][sid_] != sym:
                warn(f"{sid}: {app_id} draws {sid_} unlike another plate; rebuild the kit's plates together (contract C4)")
            STATE["symbols"][sid_] = sym
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
        row = f'<div class="oa-app-row" data-oa-app="{html.escape(app_id)}">' + "".join(frames) + "</div>"
        if any('class="oa-app-safe"' in f for f in frames):
            # contract C3: a frame with an overlay takes the plate's switch, a native checkbox that shows it by keyboard
            # with scripts off (PLATE_CSS's :has() rule reads it inside .oa-app-plate)
            words_ = html.escape(data.get("switch_words") or "Show the safe areas")
            return (f'<div class="oa-app-plate" data-oa-app-switch="{html.escape(app_id)}">{title}<label class="oa-app-switch">'
                    f'<input type="checkbox" name="{html.escape(sid)}-safe">{words_}</label>{row}</div>')
        return title + row
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
def sprite_span(page):
    """Where the identity sprite sits in the page, (start, end), counting nested <svg> (L3's master holds one); or None."""
    i = page.find('<svg data-oa-app-kit="identity"')
    if i < 0:
        return None
    depth = 0
    for m in re.finditer(r"<svg\b|</svg>", page[i:]):
        depth += 1 if m.group(0) == "<svg" else -1
        if depth == 0:
            return i, i + m.end()
    return None


def body_sprite():
    """The identity masters every placed frame draws by <use>, once for the page, hidden, for the top of the body."""
    if not STATE["symbols"]:
        return ""
    return ('<svg data-oa-app-kit="identity" aria-hidden="true" focusable="false" width="0" height="0" '
            'style="position:absolute;width:0;height:0;overflow:hidden">' + "".join(STATE["symbols"].values()) + "</svg>")


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
        hs_kept = head_styles()
        # the words: a plate whose generator now prints other words for it is stale; another page's words do not touch it
        gen = d / "gen.py"
        gen.write_text('import json,sys\nprint(json.dumps({"A99": {"title": "One"}, "A98": {"title": "x"}}))\n')
        h = hashlib.sha256(json.dumps({"title": "One"}, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
        reset(d)
        fresh = stale({"id": "A99", "inputs": {}, "words": {"generator": str(gen), "sha256": h}})
        gen.write_text('import json,sys\nprint(json.dumps({"A99": {"title": "One"}, "A98": {"title": "changed"}}))\n')
        reset(d)
        other = stale({"id": "A99", "inputs": {}, "words": {"generator": str(gen), "sha256": h}})
        gen.write_text('import json,sys\nprint(json.dumps({"A99": {"title": "Two"}}))\n')
        reset(d)
        mine = stale({"id": "A99", "inputs": {}, "words": {"generator": str(gen), "sha256": h}})
        check("a plate stays fresh while its own words do (another page's words changing), and goes stale when they change",
              fresh == [] and other == [] and mine and "its words" in mine[0])
        hs = hs_kept
        check("the page's head gets each placed type's style once, and the frames' own", hs.count("<style") == 2 and ".wa{color:red}" in hs and ".oa-app-frame" in hs)
        # chat 11c: one key of an entry, a plate with two generators' words, an atlas plate's styles and its test result
        gen.write_text('import json,sys\nprint(json.dumps({"A06": {"site": {"skip": "Skip"}, "title": "Home"}, "A99": {"title": "Two"}}))\n')
        reset(d)
        hs_ = hashlib.sha256(json.dumps({"skip": "Skip"}, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
        check("a words record may name one key of an entry (A06:site)", words_hash("A06:site", str(gen)) == hs_)
        two = [{"generator": str(gen), "id": "A06:site", "sha256": hs_}, {"generator": str(gen), "id": "A99", "sha256": h}]
        reset(d)
        both = stale({"id": "A99", "inputs": {}, "words": two})
        check("a plate with two generators' words goes stale when either changes", len(both) == 1 and "its words" in both[0])
        atlas = {"id": "A97", "type": "atlas-page", "css": "atlas-page.css", "styles": ["web-site"], "inputs": {},
                 "views": [{"key": "390-light", "w": 390, "h": 800, "theme": "light", "alt": "x", "html": frame.replace("A99", "A97")}]}
        (d / "atlas-page.css").write_text(".wa-tb{display:block}")
        (d / "web-site.css").write_text(".ws{display:block}")
        for name, rec, want in (("no atlas test result", None, "carries no atlas test result"),
                                ("an atlas test FAIL", {"pass": 40, "fail": 1, "first_fail": "FAIL T2 A97 390-light", "self_test": "PASS"}, "the atlas test fails A97"),
                                ("a self-test that did not pass", {"pass": 41, "fail": 0, "self_test": "FAIL"}, "self-test did not pass"),
                                ("a clean result", {"pass": 41, "fail": 0, "self_test": "PASS"}, None)):
            a_ = dict(atlas, **({"atlas_test": rec} if rec else {}))
            (d / "a97.json").write_text(json.dumps(a_))
            reset(d)
            STATE["atlas_self_test"] = (0, ["the fixture's frames hold no atlas page; the self-test's own run is the next case"])
            w = []
            expand('<div data-oa-app="A97"></div>', "s-21-x", w.append)
            check(f"an atlas plate with {name} {'warns' if want else 'is quiet'}", any(want in x for x in w) if want else not w)
        hs2 = head_styles()
        reset(d)
        w = []
        expand('<div data-oa-app="A97"></div>', "s-21-x", w.append)
        check("the atlas test's self-test runs once on the plates, and a fixture with no atlas page fails it", any("self-test fails on the plates" in x for x in w))
        check("an atlas plate puts the website's style in the head beside its own", ".ws{display:block}" in hs2 and ".wa-tb{display:block}" in hs2)
    reset()
    return bad


if __name__ == "__main__":
    if "--words-hash" in sys.argv:
        gen = sys.argv[sys.argv.index("--generator") + 1] if "--generator" in sys.argv else GENERATOR
        print(words_hash(sys.argv[sys.argv.index("--words-hash") + 1], gen) or "")
        sys.exit(0)
    if "--self-test" in sys.argv:
        sys.exit(1 if self_test() else 0)
    print(__doc__)
