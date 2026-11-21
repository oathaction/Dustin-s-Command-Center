"""The application kit's checks on its exports' pixels, from the facts oa-app.mjs gathered in the page.

Usage: python3 -I work/build/app-kit/tools/export_checks.py OUT_DIR EXPORTS_DIR [--json REPORT.json]

Per view (each PNG export with its facts):
  live      every word's boxes and every mark's box sit inside the live box (the post's 64 px margin, the report's safe
            line); a full-bleed panel is a ground, not a mark, and is not read
  floor     every word at the sample's floor or larger (the post's 36 px)
  red       at most one working red (Rule 05.3); signature reds are listed apart
  contrast  each word's ink against its ground, measured on the export's pixels: the ground is the commonest color in the
            word's box, the ink the pixel farthest from it in luminance; the WCAG 2.2 ratio of the two, against 4.5 to 1
            (3 to 1 for 24 px and up, or 18.66 px bold and up)
  shares    the Newsprint share of the export (Rule 05.1: 60 to 85 percent), the Charcoal share, and the red share
  feed      the post only (Rule 08.2's feed test, dark card): reduced with Lanczos to 432 and 360 px wide, each of the
            sign-off's eight nodes keeps a 2 by 2 block with every channel over 155, and the lever at least four red pixels
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


def hexrgb(name):
    m = re.search(r"--oa-color-palette-" + name + r":\s*(#[0-9A-Fa-f]{6})", TOKENS)
    h = m.group(1)
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


NEWSPRINT, CHARCOAL, RED = hexrgb("newsprint"), hexrgb("charcoal"), hexrgb("pillar-red")


def lum(c):
    def ch(v):
        v = v / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def inside(r, box, tol=0.5):
    x, y, w, h = r
    return x >= box[0] - tol and y >= box[1] - tol and x + w <= box[0] + box[2] + tol and y + h <= box[1] + box[3] + tol


def share(px, rgb, tol=3):
    return float((np.abs(px - np.array(rgb)).max(axis=2) <= tol).mean())


def word_contrast(px, word):
    """The measured ratio over the word's boxes: ground = commonest color, ink = the pixel farthest from it in luminance."""
    H, W = px.shape[:2]
    pts = []
    for x, y, w, h in word["rects"]:
        x0, y0, x1, y1 = max(0, int(x)), max(0, int(y)), min(W, int(np.ceil(x + w))), min(H, int(np.ceil(y + h)))
        if x1 > x0 and y1 > y0:
            pts.append(px[y0:y1, x0:x1].reshape(-1, 3))
    if not pts:
        return None
    a = np.concatenate(pts)
    ground = Counter(map(tuple, a)).most_common(1)[0][0]
    L = 0.2126 * a[:, 0] + 0.7152 * a[:, 1] + 0.0722 * a[:, 2]
    gL = 0.2126 * ground[0] + 0.7152 * ground[1] + 0.0722 * ground[2]
    ink = tuple(int(v) for v in a[int(np.argmax(np.abs(L - gL)))])
    return {"ground": "#%02X%02X%02X" % tuple(int(v) for v in ground), "ink": "#%02X%02X%02X" % ink, "ratio": round(ratio(ink, ground), 2)}


def ink_box(px, r):
    """The box of the pixels in r that differ from r's commonest color (the letters' ink), or None."""
    H, W = px.shape[:2]
    x0, y0 = max(0, int(r[0])), max(0, int(r[1]))
    x1, y1 = min(W, int(np.ceil(r[0] + r[2]))), min(H, int(np.ceil(r[1] + r[3])))
    if x1 <= x0 or y1 <= y0:
        return None
    a = px[y0:y1, x0:x1]
    ground = np.array(Counter(map(tuple, a.reshape(-1, 3))).most_common(1)[0][0])
    m = np.abs(a - ground).max(axis=2) > 24
    if not m.any():
        return None
    ys, xs = np.where(m)
    return [x0 + xs.min(), y0 + ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1]


def need(word):
    size, weight = word["size"], int(str(word["weight"]).strip() or 400)
    return 3.0 if size >= 24 or (size >= 18.66 and weight >= 700) else 4.5


def feed_test(png, sign):
    """Rule 08.2's dark-card feed test at 432 and 360 px wide."""
    im = Image.open(png).convert("RGB")
    out = {}
    s0, sx, sy = sign["size"] / 48, sign["x"], sign["y"]
    centers = [(4.5, 4.5), (23.5, 4.5), (42.5, 4.5), (4.5, 23.5), (23.5, 23.5), (42.5, 23.5), (4.5, 42.5), (23.5, 42.5)]
    lever = (42.5, 42.5)
    for w in (432, 360):
        k = w / im.width
        sm = np.asarray(im.resize((w, round(im.height * k)), Image.LANCZOS)).astype(int)
        nodes = []
        for cx, cy in centers:
            X, Y = (sx + cx * s0) * k, (sy + cy * s0) * k
            ok = False
            for yy in range(int(Y) - 2, int(Y) + 2):
                for xx in range(int(X) - 2, int(X) + 2):
                    blk = sm[yy:yy + 2, xx:xx + 2]
                    if blk.shape[:2] == (2, 2) and (blk > 155).all():
                        ok = True
            nodes.append(ok)
        X, Y, R = (sx + lever[0] * s0) * k, (sy + lever[1] * s0) * k, 6 * s0 * k
        reg = sm[max(0, int(Y - R)):int(Y + R) + 1, max(0, int(X - R)):int(X + R) + 1]
        reds = int(((reg[:, :, 0] > 170) & (reg[:, :, 1] < 120) & (reg[:, :, 2] < 120)).sum())
        out[w] = {"nodes_kept": sum(nodes), "lever_red_pixels": reds, "pass": all(nodes) and reds >= 4}
    return out


def check_view(view, exports, kind):
    res = {"png": view.get("png"), "faults": []}
    px = np.asarray(Image.open(exports / view["png"]).convert("RGB")).astype(int)
    live = view.get("live")
    if live:
        # a word is read by its ink: its line box (the font's whole ascent and descent) may reach past the margin when the
        # letters do not
        out_w = [w["text"] for w in view["words"] if not all(inside(ink_box(px, r) or r, live) for r in w["rects"])]
        out_m = [m["cls"] or "svg" for m in view["marks"] if not inside(m["rect"], live)]
        res["live"] = {"box": live, "words_outside": out_w, "marks_outside": out_m}
        if out_w or out_m:
            res["faults"].append(f"outside the live box: {out_w[:3]} {out_m[:3]}")
    if view.get("floor_px"):
        small = [(w["text"], w["size"]) for w in view["words"] if w["size"] + 0.01 < view["floor_px"]]
        res["floor"] = {"px": view["floor_px"], "under": small}
        if small:
            res["faults"].append(f"{len(small)} word run(s) under {view['floor_px']} px")
    working = [r for r in view["reds"] if r == "working"]
    res["red"] = {"working": len(working), "signature": len([r for r in view["reds"] if r == "signature"])}
    if len(working) > 1:
        res["faults"].append(f"{len(working)} working reds in one view")
    rows = []
    for w in view["words"]:
        c = word_contrast(px, w)
        if not c:
            continue
        rows.append({"text": w["text"], "size": w["size"], "weight": w["weight"], "need": need(w), **c})
    low = [r for r in rows if r["ratio"] < r["need"]]
    res["contrast"] = {"words": len(rows), "min": min((r["ratio"] for r in rows), default=None), "under": low,
                       "pairs": sorted({(r["ink"], r["ground"]): r["ratio"] for r in rows}.items(), key=lambda kv: kv[1])[:12]}
    if low:
        res["faults"].append(f"{len(low)} word run(s) under their contrast ratio")
    res["shares"] = {"newsprint": round(share(px, NEWSPRINT) * 100, 1), "charcoal": round(share(px, CHARCOAL) * 100, 1),
                     "red": round(share(px, RED, tol=24) * 100, 2)}
    return res


def main(out_dir, exports, report=None):
    out_dir, exports = Path(out_dir), Path(exports)
    all_res, bad = {}, 0
    for fp in sorted(out_dir.glob("a*/facts.json")):
        facts = json.loads(fp.read_text())
        for v in facts["views"]:
            if not v.get("png"):
                continue
            r = check_view(v, exports, facts["type"])
            if facts["type"] == "social-post" and v.get("sign_off"):
                r["feed"] = feed_test(exports / v["png"], v["sign_off"])
                if not all(x["pass"] for x in r["feed"].values()):
                    r["faults"].append("the feed test fails")
                nsh = r["shares"]["newsprint"]
                if not 60 <= nsh <= 85:
                    r["faults"].append(f"Newsprint covers {nsh} percent, outside Rule 05.1's 60 to 85")
            if facts["type"] == "web-page" and v.get("theme") == "light":
                nsh = r["shares"]["newsprint"]
                if not 60 <= nsh <= 85:
                    r["faults"].append(f"Newsprint covers {nsh} percent of the light capture, outside Rule 05.1's 60 to 85 (sample spec 2.7)")
            key = v["png"]
            all_res[key] = r
            bad += bool(r["faults"])
            c = r["contrast"]
            print(f"{'PASS' if not r['faults'] else 'FAIL'} {key}: {c['words']} word runs, lowest contrast {c['min']}; "
                  f"Newsprint {r['shares']['newsprint']}%, Charcoal {r['shares']['charcoal']}%, red {r['shares']['red']}%; "
                  f"reds {r['red']['working']} working, {r['red']['signature']} signature"
                  + (f"; feed test {', '.join(f'{k} px {x['nodes_kept']} of 8 nodes, {x['lever_red_pixels']} red' for k, x in r['feed'].items())}" if r.get("feed") else ""))
            for f in r["faults"]:
                print("  - " + f)
    if report:
        Path(report).write_text(json.dumps(all_res, indent=1))
    print(f"{len(all_res) - bad} of {len(all_res)} views pass")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    rep = None
    if "--json" in a:
        i = a.index("--json")
        rep = a[i + 1]
        a = a[:i] + a[i + 2:]
    sys.exit(main(a[0], a[1], rep))
