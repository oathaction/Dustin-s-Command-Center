"""The photographs the guide page carries once, for any plate to show by name (P4-5, chat 10, November 21, 2026).

guide_build.py imports this module; a chapter generator may import it for photo_img() and a scratch page for photo_style().
The contract is C1 in work/handoffs/phase-4/20261121_Chat-10-Engineer-Notes.md. In short:

  A specimen asks for a photograph by name with an <img> that has no src:
      <img data-oa-photo="lake-isabella-2014" alt="..." class="ph r32" width="1200" height="768">
  and crops it either in its own CSS (object-fit: cover, an aspect-ratio and object-position, as chapter 01 does) or with
  data-oa-crop="x y width height", a rectangle in the photograph's own pixels, which the build turns into a frame.
  The build writes one rule per photograph the page names into <style id="oa-photos"> in the head:
      img[data-oa-photo="lake-isabella-2014"]{content:url(data:image/jpeg;base64,...)}
  CSS content replacement (Chrome 28, Firefox 63, Safari 9) draws the image through the <img>, so the plate keeps its
  element, its alt, its crop and the browser's image drawing, and the page carries each photograph once, with no script.

A photograph joins PHOTOS only with a rights row in work/research/20261020_Rights-Ledger.md and its sidecar JSON beside it.

Run: python3 -I work/build/scripts/phase-4/guide_photos.py --self-test
"""
import base64
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PHOTO_DIR = "work/build/assets/photography/"

# name -> the studio's rendition the page shows (DR-238), its pixels and its rights row. The 1,920 px originals stay the source.
PHOTOS = {
    "rotunda-2005": {
        "file": PHOTO_DIR + "20261112_Photo-Rule-01-6-Rosa-Parks-Lying-In-Honor-Capitol-Rotunda-2005-1200-Wide.jpg",
        "width": 1200, "height": 797, "rights": "pho-01r", "mime": "image/jpeg",
        "what": "Rosa Parks lying in honor in the Capitol Rotunda, October 2005; Architect of the Capitol",
    },
    "lake-isabella-2014": {
        "file": PHOTO_DIR + "20261112_Photo-Rule-01-8-Corps-Of-Engineers-Public-Meeting-Lake-Isabella-2014-Zianno-1200-Wide.jpg",
        "width": 1200, "height": 768, "rights": "pho-04r", "mime": "image/jpeg",
        "what": "Paul Zianno at a Corps of Engineers public meeting, Lake Isabella, California, March 27, 2014; John Prettyman, U.S. Army",
    },
}

REQUEST = re.compile(r'<img\b[^>]*\sdata-oa-photo="[^"]*"[^>]*>')
CROP_FRAME = "oa-photo-crop"   # the class of the frame the build sets around a data-oa-crop request


def uri(name):
    p = PHOTOS[name]
    return f"data:{p['mime']};base64," + base64.b64encode((ROOT / p["file"]).read_bytes()).decode()


def rule(name):
    """The one CSS rule that draws a photograph through every <img> that names it."""
    return f'img[data-oa-photo="{name}"]{{content:url({uri(name)})}}'


def photo_style(names):
    """The <style> block for the named photographs, once each, in a stable order (a scratch page uses it too)."""
    names = [n for n in PHOTOS if n in set(names)]
    if not names:
        return ""
    return '<style id="oa-photos">' + "".join(rule(n) for n in names) + "</style>"


def photo_img(name, alt, cls="", crop=None, style=None, size=True):
    """A request tag, as a generator writes it. crop: (x, y, width, height) in the photograph's pixels, or None."""
    if name not in PHOTOS:
        raise KeyError(f"no photograph named {name!r}; the names are {', '.join(PHOTOS)}")
    p = PHOTOS[name]
    a = [f'data-oa-photo="{name}"', f'alt="{html.escape(alt, quote=True)}"']
    if crop:
        a.append('data-oa-crop="' + " ".join(str(int(v)) for v in crop) + '"')
    if cls:
        a.append(f'class="{cls}"')
    if style:
        a.append(f'style="{style}"')
    if size:
        a.append(f'width="{p["width"]}" height="{p["height"]}"')
    return "<img " + " ".join(a) + ">"


def _attr(tag, name):
    m = re.search(r'\s' + re.escape(name) + r'="([^"]*)"', tag)
    return m.group(1) if m else None


def _pct(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return ("0" if s in ("-0", "") else s) + "%"


def expand(fragment, where, warn):
    """Check every request in a fragment and turn a data-oa-crop request into its frame. Returns (fragment, names used).
    warn(where, message) takes each fault; the request is left as written when it is faulty."""
    used = []

    def one(m):
        tag = m.group(0)
        name = _attr(tag, "data-oa-photo")
        if name not in PHOTOS:
            warn(where, f'a photograph request names "{name}", which is not one of the page\'s photographs ({", ".join(PHOTOS)}); '
                        "a new photograph joins guide_photos.PHOTOS with its rights row (contract C1)")
            return tag
        if _attr(tag, "src") is not None:
            warn(where, f'the request for {name} carries a src; a request has none, and the page draws the photograph once (contract C1)')
        if _attr(tag, "alt") is None:
            warn(where, f'the request for {name} has no alt; write one for this use, or alt="" for a decorative use (contract C1)')
        used.append(name)
        crop = _attr(tag, "data-oa-crop")
        if crop is None:
            return tag
        p = PHOTOS[name]
        try:
            x, y, w, h = (int(v) for v in crop.split())
        except ValueError:
            warn(where, f'the request for {name} has data-oa-crop="{crop}"; give four whole numbers, x y width height, in the photograph\'s pixels')
            return tag
        if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > p["width"] or y + h > p["height"]:
            warn(where, f'the crop {crop} for {name} runs outside the photograph, {p["width"]} by {p["height"]} pixels')
            return tag
        # the frame takes the request's class and style; the photograph fills it at the crop's scale, by percent, so the
        # frame keeps the crop at every width
        cls = _attr(tag, "class")
        sty = _attr(tag, "style")
        frame = (f'<span class="{CROP_FRAME}{(" " + cls) if cls else ""}" style="display:block;position:relative;overflow:hidden;'
                 f'aspect-ratio:{w}/{h}{(";" + sty) if sty else ""}">')
        inner = re.sub(r'\s(?:class|style|width|height|loading)="[^"]*"', "", tag)
        place = (f'position:absolute;display:block;max-width:none;margin:0;border:0;padding:0;object-fit:fill;aspect-ratio:{p["width"]}/{p["height"]};'
                 f'width:{_pct(p["width"] / w * 100)};height:auto;left:{_pct(-x / w * 100)};top:{_pct(-y / h * 100)}')
        inner = inner[:-1].rstrip("/").rstrip() + f' style="{place}">'
        return frame + inner + "</span>"

    out = REQUEST.sub(one, fragment)
    return out, used


def placed_by_path(fragment):
    """Photograph files a fragment places by path (src, href or url()), which the contract forbids."""
    return sorted(set(re.findall(r'(?:work|source|deliverables)/build/assets/photography/[^"\'\s)]+', fragment)))


def self_test():
    bad = 0
    got = []
    warn = lambda w, m: got.append(m)
    frag = photo_img("lake-isabella-2014", "An official at a map.", cls="ph r32")
    out, used = expand(frag, "t", warn)
    ok = out == frag and used == ["lake-isabella-2014"] and not got
    print(f"{'pass' if ok else 'FAIL'} a plain request passes through unchanged and is counted")
    bad += not ok
    got.clear()
    out, used = expand('<img data-oa-photo="nowhere" alt="x">', "t", warn)
    ok = used == [] and any("not one of the page" in g for g in got)
    print(f"{'pass' if ok else 'FAIL'} an unknown name warns")
    bad += not ok
    got.clear()
    expand('<img data-oa-photo="rotunda-2005" src="x.jpg">', "t", warn)
    ok = any("carries a src" in g for g in got) and any("has no alt" in g for g in got)
    print(f"{'pass' if ok else 'FAIL'} a request with a src and no alt warns twice")
    bad += not ok
    got.clear()
    out, _ = expand(photo_img("rotunda-2005", "A detail.", cls="ph", crop=(300, 100, 600, 400)), "t", warn)
    ok = (not got and out.startswith(f'<span class="{CROP_FRAME} ph" style="display:block;position:relative;overflow:hidden;aspect-ratio:600/400">')
          and "width:200%" in out and "left:-50%" in out and "top:-25%" in out and out.endswith("></span>") and 'class="ph"' not in out)
    print(f"{'pass' if ok else 'FAIL'} a tight crop becomes a frame of its ratio with the photograph placed by percent")
    bad += not ok
    got.clear()
    expand(photo_img("rotunda-2005", "x", crop=(700, 0, 600, 400)), "t", warn)
    ok = any("outside the photograph" in g for g in got)
    print(f"{'pass' if ok else 'FAIL'} a crop past the photograph's edge warns")
    bad += not ok
    ok = placed_by_path('<img src="work/build/assets/photography/a.jpg"><i style="background:url(work/build/assets/photography/b.jpg)">') == \
        ["work/build/assets/photography/a.jpg", "work/build/assets/photography/b.jpg"]
    print(f"{'pass' if ok else 'FAIL'} a photograph placed by path is found, in src and in url()")
    bad += not ok
    st = photo_style(["lake-isabella-2014", "rotunda-2005", "lake-isabella-2014"])
    ok = st.count("content:url(data:image/jpeg;base64,") == 2 and st.index("rotunda-2005") < st.index("lake-isabella-2014")
    print(f"{'pass' if ok else 'FAIL'} the style block carries each named photograph once, in the registry's order")
    bad += not ok
    for n, p in PHOTOS.items():
        from PIL import Image
        with Image.open(ROOT / p["file"]) as im:
            ok = im.size == (p["width"], p["height"])
        print(f"{'pass' if ok else 'FAIL'} {n}: the registry's pixels match the file")
        bad += not ok
    print("guide_photos self-test: " + ("every check passed" if not bad else f"{bad} failed"))
    return bad


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(1 if self_test() else 0)
    print(__doc__)
