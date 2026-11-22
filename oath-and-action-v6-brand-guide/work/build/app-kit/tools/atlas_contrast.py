"""Contrast measured on an atlas page's pixels (chat 11c; Rule 21.15; AL-23), for Rule 21.15's ratio table.

    python3 -I work/build/app-kit/tools/atlas_contrast.py CAPTURE.png light|dark      prints JSON
    python3 -I work/build/app-kit/tools/atlas_contrast.py --self-test

For the four rows of Rule 21.15's table (text, quieter words and muted marks, the red target, a hairline that carries no
meaning), each the token the dark or light page sets: the colors are read from tokens.css, and each row's ratio is
measured between the pixel color the capture actually holds nearest the token (the commonest pixel within 6 levels of it)
and the page's ground (the capture's commonest pixel). A row whose color the capture does not hold at all (fewer than 20
pixels) says so, with no ratio. WCAG 2.2's relative luminance and contrast ratio.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
TOKENS = (ROOT / "work/build/tokens/tokens.css").read_text()
ROWS = {"text": "oa.color.text.primary", "secondary": "oa.color.text.secondary", "red": "oa.color.data.emphasisRed",
        "hairline": "oa.color.border.hairline"}


def token_hex(name):
    """A token's color, every var() resolved, from tokens.css (its first definition, the :root one)."""
    css = "--" + name.replace(".", "-")
    css = re.sub(r"([a-z])([A-Z])", lambda m: m.group(1) + "-" + m.group(2).lower(), css)
    for _ in range(12):
        m = re.search(re.escape(css) + r":\s*([^;]+);", TOKENS)
        if not m:
            return None
        v = m.group(1).strip()
        if v.startswith("#"):
            return v
        css = re.match(r"var\((--[a-z0-9-]+)\)", v).group(1)
    return None


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def measure(png, theme):
    px = np.asarray(Image.open(png).convert("RGB")).reshape(-1, 3)
    counts = Counter(map(tuple, px[:: 7].tolist()))
    ground = counts.most_common(1)[0][0]
    on = "on-charcoal" if theme == "dark" else "on-newsprint"
    out = {}
    for row, tok in ROWS.items():
        name = f"{tok}.{'onCharcoal' if theme == 'dark' else 'onNewsprint'}"
        h = token_hex(name)
        if not h:
            out[row] = {"token": name, "ratio": None, "note": "no such token"}
            continue
        t = np.array(rgb(h))
        near = px[np.abs(px - t).max(axis=1) <= 6]
        if len(near) < 20:
            out[row] = {"token": name, "ratio": None, "note": "the capture holds no pixel of this color"}
            continue
        held = Counter(map(tuple, near.tolist())).most_common(1)[0][0]
        out[row] = {"token": name, "ratio": round(ratio(held, ground), 2), "pixels": int(len(near)), "color": "#%02X%02X%02X" % held,
                    "ground": "#%02X%02X%02X" % ground}
    return out


def self_test():
    import tempfile
    bad = 0
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "c.png"
        im = np.zeros((100, 100, 3), dtype=np.uint8)
        im[:] = rgb(token_hex("oa.color.surface.charcoal") or "#121212")
        im[0:10] = rgb(token_hex("oa.color.text.primary.onCharcoal"))
        im[10:20, 0:50] = rgb(token_hex("oa.color.data.emphasisRed.onCharcoal"))
        Image.fromarray(im).save(p)
        r = measure(p, "dark")
        ok = r["text"]["ratio"] == 13.29 and r["red"]["ratio"] == 4.49 and r["hairline"]["ratio"] is None
        print(("pass" if ok else "FAIL") + f" Newsprint on Charcoal 13.29, red 4.49, an absent hairline named absent: {r['text']['ratio']}, {r['red']['ratio']}")
        bad += not ok
    return bad


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(1 if self_test() else 0)
    print(json.dumps(measure(sys.argv[1], sys.argv[2])))
