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
  screens   a web page (chat 11, contract C5; DR-310): the shares and dark panels of its first screen and of each section's
            opening screen, by tools/screen_shares.py, judged by Rule 05.1 on a light page (red alone on a dark one); this
            replaces the whole capture's Newsprint test for web pages
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import screen_shares  # noqa: E402

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


def feed_test(png, sign, widths=(432, 360)):
    """Rule 08.2's feed test: the dark card's (a 2 by 2 block of every channel over 155 in each node) by default, or on a
    light ground (sign["ground"] newsprint or white) one near-black pixel, every channel under 70, in each node's square plus
    1 px on every side; the lever keeps four red pixels either way. The 1200 by 630 card is reduced to 500 and 360 px."""
    im = Image.open(png).convert("RGB")
    out = {}
    s0, sx, sy = sign["size"] / 48, sign["x"], sign["y"]
    light = sign.get("ground") in ("newsprint", "white")
    centers = [(4.5, 4.5), (23.5, 4.5), (42.5, 4.5), (4.5, 23.5), (23.5, 23.5), (42.5, 23.5), (4.5, 42.5), (23.5, 42.5)]
    lever = (42.5, 42.5)
    for w in widths:
        k = w / im.width
        sm = np.asarray(im.resize((w, round(im.height * k)), Image.LANCZOS)).astype(int)
        nodes = []
        for cx, cy in centers:
            X, Y = (sx + cx * s0) * k, (sy + cy * s0) * k
            ok = False
            if light:
                h = 4.5 * s0 * k + 1
                sq = sm[max(0, int(np.floor(Y - h))):int(np.ceil(Y + h)) + 1, max(0, int(np.floor(X - h))):int(np.ceil(X + h)) + 1]
                ok = bool((sq < 70).all(axis=2).any())
            else:
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
    if kind == "web-site" and view.get("vh"):
        # chat 11: on a long page a view is one window (Rule 05.3 read as DR-310 reads Rule 05.1): two working reds with
        # different jobs may not stand within one window of each other; marks of one job (the take-part mark and the ask,
        # Rule 11.4) may share a view
        wm = [m for m in view.get("red_marks", []) if m["red"] == "working"]
        clash = [(a["job"], b["job"]) for i, a in enumerate(wm) for b in wm[i + 1:]
                 if a["job"] != b["job"] and abs(a["rect"][1] - b["rect"][1]) < view["vh"]]
        res["red"]["jobs"] = sorted({m["job"] for m in wm})
        if clash:
            res["faults"].append(f"working reds of different jobs within one window: {clash[:2]}")
    elif len(working) > 1:
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


def check_icons(facts, exports):
    """Chat 11 (contract C6): the favicon set. The SVG favicon's viewBox is square and it names itself; the ICO holds 16, 32
    and 48 px PNGs; each app icon's B, measured on its pixels against its tile, holds 3 to 1 (Rule 04.7's 4.49 for signature
    red on Charcoal), stands 58 percent of the tile tall to within a pixel, and on the maskable icon its ink stays inside the
    row's safe circle."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ico as icomod
    res = {}
    for v in facts["views"]:
        faults, out = [], {}
        if v.get("kind") == "svg":
            t = (exports / v["svg"]).read_text()
            vb = re.search(r'viewBox="([^"]+)"', t)
            nums = [float(x) for x in vb.group(1).split()] if vb else []
            out = {"viewBox": nums, "title": bool(re.search(r"<title\b", t)), "desc": bool(re.search(r"<desc\b", t)), "bytes": len(t.encode())}
            if len(nums) != 4 or nums[2] != nums[3]:
                faults.append("the viewBox is not square")
            if not out["title"] or not out["desc"]:
                faults.append("no title or desc")
            key = v["svg"]
        elif v.get("kind") == "ico":
            ent = icomod.read(exports / v["ico"])
            out = {"entries": [(e["width"], e["format"]) for e in ent]}
            if sorted(e["width"] for e in ent) != [16, 32, 48]:
                faults.append(f"holds {[e['width'] for e in ent]}, not 16, 32 and 48 px")
            key = v["ico"]
        elif v.get("kind") == "app-icon":
            px = np.asarray(Image.open(exports / v["png"]).convert("RGB")).astype(int)
            tile = Counter(map(tuple, px.reshape(-1, 3))).most_common(1)[0][0]
            ink = np.abs(px - np.array(tile)).max(axis=2) > 24
            ys, xs = np.where(ink)
            red = px[(np.abs(px - np.array(RED)).max(axis=2) <= 3)]
            h = int(ys.max() - ys.min() + 1) if len(ys) else 0
            out = {"tile": "#%02X%02X%02X" % tuple(tile), "b_height_px": h, "b_share": round(h / px.shape[0] * 100, 1),
                   "contrast": round(ratio(RED, tile), 2), "red_pixels": int(len(red))}
            if out["contrast"] < 3:
                faults.append(f"B on its tile measures {out['contrast']} to 1, under 3")
            if abs(h - 0.58 * px.shape[0]) > 1.5:
                faults.append(f"B stands {h} px, not 58 percent of {px.shape[0]}")
            if v.get("safe"):
                c = v["safe"]
                d = np.sqrt((xs + 0.5 - c["cx"]) ** 2 + (ys + 0.5 - c["cy"]) ** 2)
                out["farthest_ink_px"] = round(float(d.max()), 1)
                out["safe_radius_px"] = c["r"]
                if d.max() > c["r"]:
                    faults.append(f"ink reaches {d.max():.1f} px from the center, past the safe circle's {c['r']}")
            key = v["png"]
        else:
            continue
        res[key] = {"faults": faults, **out}
        print(f"{'PASS' if not faults else 'FAIL'} {key}: " + ", ".join(f"{k} {val}" for k, val in out.items()))
        for f in faults:
            print("  - " + f)
    return res


def main(out_dir, exports, report=None):
    out_dir, exports = Path(out_dir), Path(exports)
    all_res, bad = {}, 0
    for fp in sorted(out_dir.glob("a*/facts.json")):
        facts = json.loads(fp.read_text())
        if facts["type"] == "favicon-set":
            for k, r in check_icons(facts, exports).items():
                all_res[k] = r
                bad += bool(r["faults"])
            continue
        for v in facts["views"]:
            if not v.get("png"):
                continue
            if "words" not in v:
                # a capture with no page facts (the menu open, chat 11): its state is in facts.json, checked there
                all_res[v["png"]] = {"faults": [] if (v.get("menu") or {}).get("open") else ["the menu did not open"], "menu": v.get("menu")}
                print(f"{'PASS' if (v.get('menu') or {}).get('open') else 'FAIL'} {v['png']}: menu {v.get('menu')}")
                continue
            r = check_view(v, exports, facts["type"])
            if facts["type"] in ("social-post", "share-image") and v.get("sign_off"):
                r["feed"] = feed_test(exports / v["png"], v["sign_off"], (500, 360) if facts["type"] == "share-image" else (432, 360))
                if not all(x["pass"] for x in r["feed"].values()):
                    r["faults"].append("the feed test fails")
                nsh = r["shares"]["newsprint"]
                if v["sign_off"].get("ground", "newsprint") == "newsprint" and not 60 <= nsh <= 85:
                    r["faults"].append(f"Newsprint covers {nsh} percent, outside Rule 05.1's 60 to 85")
            if facts["type"] in ("web-page", "web-site") and v.get("vh"):
                # chat 11 (contract C5, DR-310): Rule 05.1 by screen, the first and each section's opening screen
                r["screens"] = screen_shares.measure(exports / v["png"], v["vh"], v.get("sections") or [], v.get("dark") or [],
                                                     v.get("theme", "light"), v.get("width"))
                for scr in r["screens"]:
                    for f in scr["faults"]:
                        r["faults"].append(f"{scr['screen']}: {f}")
            key = v["png"]
            all_res[key] = r
            bad += bool(r["faults"])
            c = r["contrast"]
            print(f"{'PASS' if not r['faults'] else 'FAIL'} {key}: {c['words']} word runs, lowest contrast {c['min']}; "
                  f"Newsprint {r['shares']['newsprint']}%, Charcoal {r['shares']['charcoal']}%, red {r['shares']['red']}%; "
                  f"reds {r['red']['working']} working, {r['red']['signature']} signature"
                  + (f"; feed test {', '.join(f'{k} px {x['nodes_kept']} of 8 nodes, {x['lever_red_pixels']} red' for k, x in r['feed'].items())}" if r.get("feed") else ""))
            for scr in r.get("screens") or []:
                print("  " + screen_shares.line(f"{v.get('width')} {v.get('theme')}", scr))
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
