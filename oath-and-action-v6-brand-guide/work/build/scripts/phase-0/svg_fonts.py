"""Phase 0 rights inventory: list fonts embedded inside extracted SVG files.

Read-only. Usage: python3 -I svg_fonts.py SVG [SVG ...]
Prints, for each @font-face data URI, the CSS family and weight and the
name-table fields that matter for licensing.
"""
import base64, hashlib, io, re, site, sys
sys.path.append(site.getusersitepackages())
from fontTools.ttLib import TTFont  # noqa: E402

for arg in sys.argv[1:]:
    raw = open(arg, "rb").read()
    print("==", arg.split("/")[-1], len(raw), "bytes, <image> tags:", raw.count(b"<image"),
          "raster data URIs:", len(re.findall(rb"data:image/(?:png|jpe?g|webp|gif)", raw)))
    for m in re.finditer(rb"@font-face\{([^}]*?)src:url\(data:(font/[a-z0-9]+);base64,([A-Za-z0-9+/=]+)\)", raw):
        css = m.group(1).decode()
        data = base64.b64decode(m.group(3))
        f = TTFont(io.BytesIO(data), lazy=True)
        n = f["name"]
        g = lambda i: str(n.getName(i, 3, 1, 0x409) or "")
        print("  ", css.strip(), m.group(2).decode(), len(data), hashlib.sha256(data).hexdigest()[:12],
              "|", g(4), "|", g(5), "|", g(0)[:70], "| lic URL:", g(14) or None,
              "| glyphs", f["maxp"].numGlyphs, "| fsType", f["OS/2"].fsType)
