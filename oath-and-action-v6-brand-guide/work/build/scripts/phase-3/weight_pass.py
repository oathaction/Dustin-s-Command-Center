"""The guide page's weight pass (Phase 3, round 0, November 11, 2026): bytes that can go with no change a reader sees.

guide_build.py runs it on the assembled page, before the weight gates measure it, and records each step's bytes in the build
report under weight.pass. Two steps, each one safe by construction and checked again here:

  css     every <style> block loses its comments and the white space CSS ignores. A string keeps every character, a
          block a script shows as code (data-oa-code-css) is left whole, and the tokens of each rule stay in order, so
          the browser reads the same rules.
  png     every PNG the page shows (an <img src> or an SVG <image href>, never a file a reader downloads) is compressed
          again without loss: the image data deflated again at level 9, and Pillow's own optimized encoding where the
          file carries no color chunk Pillow would drop. A candidate is used only when it decodes to the same pixels,
          mode, size and palette as the original, and only when it is smaller.

The weight pass proves the whole page the same by screenshots (work/build/scripts/phase-3/weight_pass_proof.js).

  python3 work/build/scripts/phase-3/weight_pass.py PAGE.html [--out SMALLER.html]   measures each step on a built page
  python3 work/build/scripts/phase-3/weight_pass.py --self-test
"""
import base64
import io
import re
import struct
import sys
import zlib

STEPS = ("css", "png")


# --------------------------------------------------------------------------------------------------------------------
# CSS: comments and ignorable white space
# --------------------------------------------------------------------------------------------------------------------
# White space may go before or after these characters wherever they stand outside a string. Never before ":" (in a
# selector, "a :hover" and "a:hover" differ); after ":" it may go, since no selector puts white space after a colon.
TIGHT = set("{};,>")


def css_min(css):
    out = []
    i, n = 0, len(css)
    pending_ws = False

    def last():
        return out[-1][-1] if out and out[-1] else ""

    while i < n:
        c = css[i]
        if c == "/" and css.startswith("/*", i):
            e = css.find("*/", i + 2)
            if e < 0:
                raise ValueError("css_min: an unclosed comment")
            i = e + 2
            pending_ws = True   # a comment separates tokens as white space does
            continue
        if c in " \t\r\n\f":
            pending_ws = True
            i += 1
            continue
        if c in "\"'":
            j = i + 1
            while j < n and css[j] != c:
                if css[j] == "\\":
                    j += 1
                if css[j] == "\n":
                    raise ValueError("css_min: a string runs past its line")
                j += 1
            tok = css[i:j + 1]
            i = j + 1
        elif c == "\\":
            # an escaped character is part of its name, and the space after it may belong to the escape
            tok = css[i:i + 2]
            i += 2
        elif c == "u" and css.startswith("url(", i) and not css.startswith(("url(\"", "url('"), i):
            # an unquoted url() is one token to its closing parenthesis
            j = css.find(")", i)
            tok = css[i:j + 1]
            i = j + 1
        else:
            tok = c
            i += 1
        if pending_ws and out:
            a, b = last(), tok[0]
            # keep one space unless either side is a character that needs none, or the space follows a colon;
            # a custom property set to white space alone keeps it ("--x: ;")
            keep = not (a in TIGHT or b in TIGHT or a == ":") or out[-1].startswith("\\")
            if a == ":" and b in ";}":
                keep = True
            if keep:
                out.append(" ")
        pending_ws = False
        out.append(tok)
    return "".join(out).strip()


def css_tokens(css):
    """The rule's tokens with white space and comments removed, for the check that minifying changed nothing else."""
    toks, i, n = [], 0, len(css)
    while i < n:
        c = css[i]
        if css.startswith("/*", i):
            i = css.find("*/", i + 2) + 2
            continue
        if c in " \t\r\n\f":
            i += 1
            continue
        if c in "\"'":
            j = i + 1
            while css[j] != c:
                j += 2 if css[j] == "\\" else 1
            toks.append(css[i:j + 1])
            i = j + 1
            continue
        toks.append(c)
        i += 1
    return toks


STYLE = re.compile(r"(<style\b([^>]*)>)(.*?)(</style>)", re.S)


def pass_css(page):
    saved, blocks = 0, 0

    def one(m):
        nonlocal saved, blocks
        head, attrs, body, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        if "data-oa-code-css" in attrs:
            return m.group(0)
        small = css_min(body)
        if css_tokens(small) != css_tokens(body):
            raise AssertionError("weight pass: minified CSS reads differently from its source")
        if len(small) >= len(body):
            return m.group(0)
        saved += len(body) - len(small)
        blocks += 1
        return head + small + tail

    page = STYLE.sub(one, page)
    return page, {"bytes_saved": saved, "blocks": blocks}


# --------------------------------------------------------------------------------------------------------------------
# PNG: the same pixels in fewer bytes
# --------------------------------------------------------------------------------------------------------------------
PNG_SIG = b"\x89PNG\r\n\x1a\n"
COLOR_CHUNKS = {b"gAMA", b"cHRM", b"sRGB", b"iCCP", b"sBIT", b"cICP", b"mDCv", b"cLLi"}


def chunks(b):
    i, out = 8, []
    while i < len(b):
        n = struct.unpack(">I", b[i:i + 4])[0]
        out.append((b[i + 4:i + 8], b[i + 8:i + 8 + n]))
        i += 12 + n
    return out


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def redeflate(b):
    """The same file with its image data deflated again at level 9; every other chunk byte for byte."""
    cs = chunks(b)
    raw = zlib.decompress(b"".join(d for k, d in cs if k == b"IDAT"))
    best = None
    for strategy in (zlib.Z_DEFAULT_STRATEGY, zlib.Z_FILTERED):
        co = zlib.compressobj(9, zlib.DEFLATED, 15, 9, strategy)
        z = co.compress(raw) + co.flush()
        if best is None or len(z) < len(best):
            best = z
    out, done = [PNG_SIG], False
    for k, d in cs:
        if k == b"IDAT":
            if not done:
                out.append(chunk(b"IDAT", best))
                done = True
            continue
        out.append(chunk(k, d))
    return b"".join(out)


def pillow_optimized(b):
    from PIL import Image
    if any(k in COLOR_CHUNKS for k, _ in chunks(b)):
        return None
    im = Image.open(io.BytesIO(b))
    kw = {"optimize": True}
    if "transparency" in im.info:
        kw["transparency"] = im.info["transparency"]
    buf = io.BytesIO()
    im.save(buf, "PNG", **kw)
    return buf.getvalue()


def same_pixels(a, b):
    from PIL import Image
    ia, ib = Image.open(io.BytesIO(a)), Image.open(io.BytesIO(b))
    if ia.size != ib.size or ia.mode != ib.mode:
        return False
    if ia.mode == "P" and (ia.getpalette() != ib.getpalette() or ia.info.get("transparency") != ib.info.get("transparency")):
        return False
    if ia.info.get("transparency") != ib.info.get("transparency"):
        return False
    return ia.tobytes() == ib.tobytes() and ia.convert("RGBA").tobytes() == ib.convert("RGBA").tobytes()


def png_smaller(b):
    best = b
    for make in (redeflate, pillow_optimized):
        try:
            c = make(b)
        except Exception:
            c = None
        if c and len(c) < len(best) and same_pixels(b, c):
            best = c
    return best


# an image the page shows: <img src="data:image/png..."> or an SVG <image href="data:image/png...">; a download link's
# href is a file the reader keeps, and stays byte for byte
SHOWN_PNG = re.compile(r'(<(?:img|image)\b[^>]*?\s(?:src|href|xlink:href)=")data:image/png;base64,([A-Za-z0-9+/=]+)(")')


def pass_png(page):
    saved, changed, seen = 0, 0, {}

    def one(m):
        nonlocal saved, changed
        b64 = m.group(2)
        if b64 not in seen:
            raw = base64.b64decode(b64)
            small = png_smaller(raw)
            seen[b64] = base64.b64encode(small).decode() if small is not raw else b64
        new = seen[b64]
        if new != b64:
            saved += len(b64) - len(new)
            changed += 1
        return m.group(1) + "data:image/png;base64," + new + m.group(3)

    page = SHOWN_PNG.sub(one, page)
    return page, {"bytes_saved": saved, "images": changed, "shown_pngs": len(seen)}


def run(page, steps=STEPS):
    """Returns the smaller page and each step's record."""
    rec = {"before": len(page.encode())}
    for s in steps:
        page, r = {"css": pass_css, "png": pass_png}[s](page)
        rec[s] = r
    rec["after"] = len(page.encode())
    rec["bytes_saved"] = rec["before"] - rec["after"]
    return page, rec


def self_test():
    bad = 0
    cases = [
        (".a  > .b { color : red ; }\n/* note */\n.c :hover{x:1}", ".a>.b{color :red;}.c :hover{x:1}"),
        ("a{content:\"  /* kept */  \"}", "a{content:\"  /* kept */  \"}"),
        ("@media (min-width: 48em) and (max-width: 60em) { .x { y: calc(1px + 2px) } }", "@media (min-width:48em) and (max-width:60em){.x{y:calc(1px + 2px)}}"),
        ("a{--x: ;}", "a{--x: ;}"),
        (".a\\: b{x:1}", ".a\\: b{x:1}"),
        ("a{background:url( data:image/png;base64,AA== )}", "a{background:url( data:image/png;base64,AA== )}"),
        ("@scope ([data-specimen=\"s\"]) to ([data-x]) { p { margin: 0 } }", "@scope ([data-specimen=\"s\"]) to ([data-x]){p{margin:0}}"),
    ]
    for src, want in cases:
        got = css_min(src)
        ok = got == want
        print(f"{'pass' if ok else 'FAIL'} css: {src[:40]!r} -> {got!r}")
        bad += not ok
    # a PNG compressed badly comes back smaller with the same pixels; a planted pixel change is refused
    from PIL import Image
    im = Image.new("RGB", (64, 64), (220, 217, 210))
    for x in range(64):
        im.putpixel((x, x), (18, 18, 18))
    buf = io.BytesIO()
    im.save(buf, "PNG", compress_level=0)
    raw = buf.getvalue()
    small = png_smaller(raw)
    ok = len(small) < len(raw) and same_pixels(raw, small)
    print(f"{'pass' if ok else 'FAIL'} png: {len(raw)} -> {len(small)} bytes, same pixels")
    bad += not ok
    im2 = im.copy()
    im2.putpixel((0, 1), (0, 0, 0))
    b2 = io.BytesIO()
    im2.save(b2, "PNG")
    ok = not same_pixels(raw, b2.getvalue())
    print(f"{'pass' if ok else 'FAIL'} png: a changed pixel is told apart")
    bad += not ok
    page = f'<p><img src="data:image/png;base64,{base64.b64encode(raw).decode()}"></p><a download href="data:image/png;base64,{base64.b64encode(raw).decode()}">x</a>'
    out, rec = run(page)
    ok = rec["png"]["images"] == 1 and base64.b64encode(raw).decode() in out
    print(f"{'pass' if ok else 'FAIL'} png: the shown image shrinks and the download stays byte for byte")
    bad += not ok
    print("weight_pass self-test: " + ("every case passes" if not bad else f"{bad} failed"))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    src = sys.argv[1]
    page = open(src, encoding="utf-8").read()
    for s in STEPS:
        _, r = run(page, (s,))
        print(s, r[s])
    out, rec = run(page)
    print("all", {k: v for k, v in rec.items() if k in ("before", "after", "bytes_saved")})
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w", encoding="utf-8").write(out)
