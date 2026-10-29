"""Build one or more Civic Line icons from src/<ID>.svg.

    python3 -I build_icon.py <ID> [<ID> ...] [--tracer NAME] [--state traced|reviewed|fixed] [--note TEXT]

For each ID: validate the source and its corrections log, bake the export pair
(red-black and black), render the source in crop space at 1x and 4x and compare
it with the reference masks, write the metrics, overlay, blink GIF, size strip,
256 and 512 px PNGs and the per-icon status file. One Chromium launch serves the
whole batch. An ID that fails validation is reported and skipped; the others
still build; the exit code is 1 if any failed.

The bake check renders the baked export back at crop scale and compares it
with the crop-space render. The 4x number is the main one; it leaves out the
pixels within 2 levels of the threshold in either render, because an edge
that lands exactly on a half pixel renders at coverage one half and rounds
either way. The raw 4x and 1x numbers are kept beside it, along with the
largest per-pixel difference between the two 4x renders.
"""
import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
import cl_svg as S  # noqa: E402
import stroke_width as SW  # noqa: E402

Z = 4
EDGE_TOL = 0.5          # source px: edge pixels farther than this from the other edge count as unmatched
STATES = ("todo", "traced", "reviewed", "fixed")
CHARCOAL_G = C.hex_rgb(C.CHARCOAL)[1]
PR = C.hex_rgb(C.PILLAR_RED)
PILLAR_REDNESS = PR[0] - max(PR[1], PR[2])
SIZES = [24, 32, 64, 128, 256]


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def rgb_hex(rgb):
    return "#%02X%02X%02X" % tuple(int(round(v)) for v in rgb)


def load_scale():
    sc = C.read_json(C.SCALE_JSON)
    if sc is None:
        raise SystemExit(f"Scale file missing: {C.SCALE_JSON}. Run measure_scale_stroke.py first.")
    return sc


def load_source(icon_id, row):
    p_svg = os.path.join(C.SRC, f"{icon_id}.svg")
    p_json = os.path.join(C.SRC, f"{icon_id}.json")
    if not os.path.exists(p_svg):
        raise S.SourceError(f"{icon_id}: no source file at {p_svg}")
    with open(p_svg, encoding="utf-8") as fh:
        text = fh.read()
    corr = None
    if os.path.exists(p_json):
        try:
            corr = C.read_json(p_json)
        except json.JSONDecodeError as e:
            raise S.SourceError(f"{icon_id}: src/{icon_id}.json is not valid JSON: {e}")
    return S.parse_source(text, icon_id, row["crop"]["w"], row["crop"]["h"], corr)


# ------------------------------------------------------------------ masks and metrics

def iou(a, b):
    u = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / u) if u else 1.0


def boundary(m):
    return m & ~ndi.binary_erosion(m, structure=np.ones((3, 3), bool), border_value=0)


def edge_stats(ref_b, tr_b, z):
    """Distances (source px) from each boundary pixel to the other mask's boundary."""
    if not ref_b.any() or not tr_b.any():
        return None, None, None
    d_to_tr = ndi.distance_transform_edt(~tr_b) / z
    d_to_ref = ndi.distance_transform_edt(~ref_b) / z
    a = d_to_tr[ref_b]
    b = d_to_ref[tr_b]

    def st(v):
        return {"mean": round(float(v.mean()), 3), "p95": round(float(np.percentile(v, 95)), 3),
                "max": round(float(v.max()), 3)}
    both = np.concatenate([a, b])
    return {"reference_to_trace": st(a), "trace_to_reference": st(b), "symmetric": st(both)}, d_to_tr, d_to_ref


def best_offset(tr, ref, r=3):
    best = None
    H, W = ref.shape
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            sh = np.zeros_like(tr)
            ys0, ys1 = max(0, dy), min(H, H + dy)
            xs0, xs1 = max(0, dx), min(W, W + dx)
            sh[ys0:ys1, xs0:xs1] = tr[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
            v = iou(sh, ref)
            if best is None or v > best[0] + 1e-12:
                best = (v, dx, dy)
    return {"dx": best[1], "dy": best[2], "iou": round(best[0], 4)}


def render_masks(png_path, bg_rgb, kind):
    rgb = np.asarray(Image.open(png_path).convert("RGB"))
    if kind == "ink":
        thr = (float(bg_rgb[1]) + CHARCOAL_G) / 2.0
        return C.green(rgb) < thr, rgb
    bg_r = float(bg_rgb[0]) - max(float(bg_rgb[1]), float(bg_rgb[2]))
    return C.redness(rgb) > (bg_r + PILLAR_REDNESS) / 2.0, rgb


BAKE_BAND = 2   # levels either side of the threshold left out of the main bake IoU


def bake_banded(a_png, b_png, bg_rgb):
    """Main bake metric: IoU of the two 4x ink masks over the pixels that sit
    more than BAKE_BAND levels from the threshold in both renders. A pixel whose
    edge coverage is exactly one half (an edge on a half pixel) rounds to 119
    in one render and 120 in the other; it says nothing about the geometry."""
    thr = (float(bg_rgb[1]) + CHARCOAL_G) / 2.0
    ga = C.green(np.asarray(Image.open(a_png).convert("RGB")))
    gb = C.green(np.asarray(Image.open(b_png).convert("RGB")))
    ok = (np.abs(ga - thr) > BAKE_BAND) & (np.abs(gb - thr) > BAKE_BAND)
    return iou((ga < thr) & ok, (gb < thr) & ok)


def bake_max_diff(a_png, b_png):
    """Largest per-pixel green difference between the two 4x renders, in levels."""
    ga = C.green(np.asarray(Image.open(a_png).convert("RGB")))
    gb = C.green(np.asarray(Image.open(b_png).convert("RGB")))
    return int(np.abs(ga - gb).max())


# ------------------------------------------------------------------ images

def label_strip(img, text, h=22, color=(0, 0, 0)):
    out = Image.new("RGB", (img.width, img.height + h), (255, 255, 255))
    out.paste(img, (0, h))
    ImageDraw.Draw(out).text((4, 4), text, fill=color, font=C.font(13, True))
    return out


def paint(base_rgb, mask, color):
    base_rgb[mask] = color


def overlay_panels(ref_black, tr_rb4, ref_ink4, ref_red4, t_ink4, t_red4, d_to_tr, d_to_ref, title, path):
    h4, w4 = ref_ink4.shape
    p1 = Image.fromarray(ref_black).resize((w4, h4), Image.NEAREST)
    p2 = Image.fromarray(tr_rb4)
    ov = np.full((h4, w4, 3), 255, np.uint8)
    paint(ov, ref_ink4, (205, 205, 205))
    rb = ndi.binary_dilation(boundary(ref_red4), iterations=1)
    paint(ov, rb, (225, 20, 20))
    paint(ov, boundary(t_red4), (0, 160, 70))
    paint(ov, ndi.binary_dilation(boundary(t_ink4), iterations=1) & ~rb, (0, 70, 255))
    p3 = Image.fromarray(ov)
    ed = np.full((h4, w4, 3), 255, np.uint8)
    rbd = boundary(ref_ink4)
    tbd = boundary(t_ink4)
    tol = EDGE_TOL
    if d_to_tr is not None:
        paint(ed, ref_ink4, (240, 240, 240))
        paint(ed, rbd & (d_to_tr <= tol), (150, 150, 150))
        paint(ed, ndi.binary_dilation(rbd & (d_to_tr > tol)), (235, 90, 0))
        paint(ed, ndi.binary_dilation(tbd & (d_to_ref > tol)), (0, 80, 255))
    p4 = Image.fromarray(ed)
    panels = [label_strip(p1, "reference (black sheet)"), label_strip(p2, "trace (red-black)"),
              label_strip(p3, "overlay: ref ink grey, trace edge blue, red mask: ref red / trace green"),
              label_strip(p4, f"edge diff >{tol} px: reference-only orange, trace-only blue")]
    gap = 10
    W = sum(p.width for p in panels) + gap * (len(panels) + 1)
    H = max(p.height for p in panels) + 40
    out = Image.new("RGB", (W, H), (255, 255, 255))
    ImageDraw.Draw(out).text((gap, 8), title, fill=(0, 0, 0), font=C.font(15, True))
    x = gap
    for p in panels:
        out.paste(p, (x, 34))
        x += p.width + gap
    out.save(path)


def blink_gif(ref_black, ref_red, tr_black4, tr_rb4, path):
    h4, w4 = tr_black4.shape[:2]

    def pair(a, b, text, color):
        im = Image.new("RGB", (w4 * 2 + 30, h4 + 28), (255, 255, 255))
        im.paste(a, (10, 24))
        im.paste(b, (w4 + 20, 24))
        ImageDraw.Draw(im).text((10, 4), text, fill=color, font=C.font(14, True))
        return im
    fa = pair(Image.fromarray(ref_black).resize((w4, h4), Image.NEAREST),
              Image.fromarray(ref_red).resize((w4, h4), Image.NEAREST), "REFERENCE", (200, 0, 0))
    fb = pair(Image.fromarray(tr_black4), Image.fromarray(tr_rb4), "TRACE", (0, 70, 220))
    frames = [f.convert("P", palette=Image.ADAPTIVE, colors=255) for f in (fa, fb)]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=600, loop=0, disposal=1)


def size_strip(files, path, title):
    """files: list of (label, png path). Each size sits in a slot at least 96 px wide."""
    ims = [(lab, Image.open(p).convert("RGB")) for lab, p in files]
    gap = 20
    slot = [max(96, im.width) for _, im in ims]
    top = 34
    base = top + max(im.height for _, im in ims)
    H = base + 40
    W = sum(slot) + gap * (len(ims) + 1)
    out = Image.new("RGB", (W, H), C.hex_rgb(C.NEWSPRINT))
    d = ImageDraw.Draw(out)
    d.text((gap, 8), title, fill=(18, 18, 18), font=C.font(14, True))
    x = gap
    for (lab, im), sw in zip(ims, slot):
        out.paste(im, (x + (sw - im.width) // 2, base - im.height))
        d.text((x, base + 10), lab, fill=(18, 18, 18), font=C.font(12))
        x += sw + gap
    out.save(path)


def sized(svg, px):
    return svg.replace('width="128" height="128" viewBox="0 0 128 128"',
                       f'width="{px}" height="{px}" viewBox="0 0 128 128"', 1)


def strip_decl(svg):
    return svg.split("?>", 1)[1].lstrip() if svg.startswith("<?xml") else svg


# ------------------------------------------------------------------ build

def build(ids, tracer=None, state=None, note=None, rebuild=False):
    inv = C.inventory_by_id()
    sc = load_scale()
    W = sc["W_source_px"]
    failures = {}
    ready = []
    for icon_id in ids:
        if icon_id not in inv:
            failures[icon_id] = f"{icon_id}: not in the inventory"
            continue
        try:
            src = load_source(icon_id, inv[icon_id])
        except S.SourceError as e:
            failures[icon_id] = str(e)
            continue
        ready.append((icon_id, src))
    tmp = tempfile.mkdtemp(prefix="civic-line-build-")
    jobs = []
    plan = {}
    for icon_id, src in ready:
        row = inv[icon_id]
        mp = row["mask_params"]
        bg_b, bg_r = rgb_hex(mp["bg_black_rgb"]), rgb_hex(mp["bg_red_rgb"])
        rb, bk = S.export_pair(src, row, W)
        black_cols = {"base": C.CHARCOAL, "accent": C.CHARCOAL}
        rb_cols = {"base": C.CHARCOAL, "accent": C.PILLAR_RED}
        d = os.path.join(tmp, icon_id)
        p = {k: os.path.join(d, f"{k}.png") for k in
             ["cs1_black", "cs1_rb", "cs4_black", "cs4_rb", "bake1", "bake4"]}
        cw, ch = row["crop"]["w"], row["crop"]["h"]
        jobs += [
            {"svg": S.crop_space_svg(src, W, black_cols, 1), "w": cw, "h": ch, "bg": bg_b, "out": p["cs1_black"]},
            {"svg": S.crop_space_svg(src, W, rb_cols, 1), "w": cw, "h": ch, "bg": bg_r, "out": p["cs1_rb"]},
            {"svg": S.crop_space_svg(src, W, black_cols, Z), "w": cw * Z, "h": ch * Z, "bg": bg_b, "out": p["cs4_black"]},
            {"svg": S.crop_space_svg(src, W, rb_cols, Z), "w": cw * Z, "h": ch * Z, "bg": bg_r, "out": p["cs4_rb"]},
            {"svg": S.export_at_crop_scale(bk, row, 1), "w": cw, "h": ch, "bg": bg_b, "out": p["bake1"]},
            {"svg": S.export_at_crop_scale(bk, row, Z), "w": cw * Z, "h": ch * Z, "bg": bg_b, "out": p["bake4"]},
        ]
        sizes = []
        for px in SIZES:
            f = os.path.join(d, f"rb_{px}.png")
            jobs.append({"svg": sized(strip_decl(rb), px), "w": px, "h": px, "bg": C.NEWSPRINT, "out": f})
            sizes.append((f"red-black {px} px", f))
        for px in (24, 64):
            f = os.path.join(d, f"bk_{px}.png")
            jobs.append({"svg": sized(strip_decl(bk), px), "w": px, "h": px, "bg": C.NEWSPRINT, "out": f})
            sizes.append((f"black {px} px", f))
        ex = row["exports"]
        for px in (256, 512):
            jobs.append({"svg": sized(strip_decl(rb), px), "w": px, "h": px, "bg": None,
                         "out": os.path.join(C.ASSETS, f"png-{px}", "red-black", ex["png_red_black"])})
            jobs.append({"svg": sized(strip_decl(bk), px), "w": px, "h": px, "bg": None,
                         "out": os.path.join(C.ASSETS, f"png-{px}", "black", ex["png_black"])})
        plan[icon_id] = {"src": src, "row": row, "rb": rb, "bk": bk, "p": p, "sizes": sizes}
    if jobs:
        jp = os.path.join(tmp, "jobs.json")
        with open(jp, "w", encoding="utf-8") as fh:
            json.dump(jobs, fh)
        r = subprocess.run(["node", C.RENDER_JS, jp], capture_output=True, text=True)
        if r.returncode != 0:
            shutil.rmtree(tmp, ignore_errors=True)
            raise SystemExit(f"Renderer failed:\n{r.stderr[-3000:]}")
    results = {}
    for icon_id, P in plan.items():
        results[icon_id] = finish(icon_id, P, W, sc, tracer, state, note, rebuild)
    shutil.rmtree(tmp, ignore_errors=True)
    return results, failures


def finish(icon_id, P, W, sc, tracer, state, note, rebuild=False):
    row, src, p = P["row"], P["src"], P["p"]
    ex = row["exports"]
    # exports
    with open(os.path.join(C.ASSETS, "red-black", ex["svg_red_black"]), "w", encoding="utf-8") as fh:
        fh.write(P["rb"])
    with open(os.path.join(C.ASSETS, "black", ex["svg_black"]), "w", encoding="utf-8") as fh:
        fh.write(P["bk"])
    pair_ok = P["rb"].replace(C.PILLAR_RED, C.CHARCOAL) == P["bk"]
    bounds, _ = S.drawn_bounds(strip_decl(P["rb"]))
    # references
    refc = os.path.join(C.ASSETS, "reference-crops")
    ref_black = C.load_rgb(os.path.join(refc, row["reference_crops"]["black"]))
    ref_red = C.load_rgb(os.path.join(refc, row["reference_crops"]["red"]))
    mp = row["mask_params"]
    ref_ink1 = C.load_mask(os.path.join(C.QA, "masks", f"{icon_id}-ink.png"))
    ref_red1 = C.load_mask(os.path.join(C.QA, "masks", f"{icon_id}-red.png"))
    ref_ink4 = SW.upsampled(C.green(ref_black), Z, 1.5) < mp["ink_threshold_g"]
    ref_red4 = SW.upsampled(C.redness(ref_red), Z, 1.5) > mp["red_threshold"]
    # trace renders
    t_ink1, _ = render_masks(p["cs1_black"], mp["bg_black_rgb"], "ink")
    t_red1, _ = render_masks(p["cs1_rb"], mp["bg_red_rgb"], "red")
    t_ink4, tr_black4 = render_masks(p["cs4_black"], mp["bg_black_rgb"], "ink")
    t_red4, tr_rb4 = render_masks(p["cs4_rb"], mp["bg_red_rgb"], "red")
    b_ink1, _ = render_masks(p["bake1"], mp["bg_black_rgb"], "ink")
    b_ink4, _ = render_masks(p["bake4"], mp["bg_black_rgb"], "ink")
    edges, d_to_tr, d_to_ref = edge_stats(boundary(ref_ink4), boundary(t_ink4), Z)
    red_edges, _, _ = edge_stats(boundary(ref_red4), boundary(t_red4), Z)
    n_corr = len(src.corrections.get("corrections", []))
    metrics = {
        "id": icon_id, "label": row["label"], "built": now(),
        "W_source_px": W, "s": row["transform"]["s"], "stroke_units": round(W * row["transform"]["s"], 4),
        "silhouette_iou_1x": round(iou(t_ink1, ref_ink1), 4),
        "silhouette_iou_4x": round(iou(t_ink4, ref_ink4), 4),
        "red_iou_1x": round(iou(t_red1, ref_red1), 4),
        "red_iou_4x": round(iou(t_red4, ref_red4), 4),
        "edge_distance_px": edges,
        "red_edge_distance_px": red_edges,
        "best_offset_1x": best_offset(t_ink1, ref_ink1, 3),
        "ink_area_ratio_trace_over_reference": round(float(t_ink4.sum()) / max(1, ref_ink4.sum()), 4),
        "bake_check_iou_4x": round(bake_banded(p["bake4"], p["cs4_black"], mp["bg_black_rgb"]), 4),
        "bake_check_iou_4x_raw": round(iou(b_ink4, t_ink4), 4),
        "bake_check_iou_1x": round(iou(b_ink1, t_ink1), 4),
        "bake_check_max_diff_levels_4x": bake_max_diff(p["bake4"], p["cs4_black"]),
        "pair_identical_after_swap": pair_ok,
        "export_drawn_bounds": [round(v, 3) for v in bounds] if bounds else None,
        "export_inside_0_128": bool(bounds and bounds[0] >= 0 and bounds[1] >= 0 and bounds[2] <= 128 and bounds[3] <= 128),
        "elements": sum(len(g.elems) for g in src.groups),
        "groups": [g.role for g in src.groups],
        "masks": list(src.masks),
        "corrections_logged": n_corr,
        "rules": {
            "reference_ink": "green below the crop's midpoint (local background to full ink)",
            "reference_red": "redness R - max(G, B) above the crop's midpoint (local background to full red)",
            "trace_ink": "black-edition render on the crop's own background; green below the midpoint between that background and Charcoal",
            "trace_red": "red-black render on the red crop's background; redness above the midpoint between that background and Pillar Red",
            "4x_reference": "reference channel upsampled 4x (bilinear, 1.5 px Gaussian) and thresholded with the same midpoint",
            "edge_distance": "boundary pixels of each 4x mask; distance transform to the other mask's boundary; reported in source px",
        },
    }
    C.write_json(os.path.join(C.QA, "metrics", f"{icon_id}.json"), metrics)
    title = (f"{icon_id} {row['label']}  |  silhouette IoU {metrics['silhouette_iou_1x']:.3f}  red IoU {metrics['red_iou_1x']:.3f}  "
             f"edge mean {edges['symmetric']['mean'] if edges else float('nan'):.2f} px  p95 {edges['symmetric']['p95'] if edges else float('nan'):.2f} px  "
             f"offset ({metrics['best_offset_1x']['dx']},{metrics['best_offset_1x']['dy']})  W {W} px")
    overlay_panels(ref_black, tr_rb4, ref_ink4, ref_red4, t_ink4, t_red4, d_to_tr, d_to_ref, title,
                   os.path.join(C.QA, "overlays", f"{icon_id}.png"))
    blink_gif(ref_black, ref_red, tr_black4, tr_rb4, os.path.join(C.QA, "blink", f"{icon_id}.gif"))
    size_strip(P["sizes"], os.path.join(C.QA, "sizes", f"{icon_id}.png"),
               f"{icon_id} {row['label']}  |  exports on Newsprint at 1x; stroke {W * row['transform']['s']:.2f} of 128 units")
    summary = {k: metrics[k] for k in ("silhouette_iou_1x", "red_iou_1x", "bake_check_iou_4x", "bake_check_iou_1x", "pair_identical_after_swap",
                                       "export_inside_0_128", "ink_area_ratio_trace_over_reference")}
    summary["edge_mean_px"] = edges["symmetric"]["mean"] if edges else None
    summary["edge_p95_px"] = edges["symmetric"]["p95"] if edges else None
    summary["edge_max_px"] = edges["symmetric"]["max"] if edges else None
    summary["best_offset"] = [metrics["best_offset_1x"]["dx"], metrics["best_offset_1x"]["dy"]]
    if not rebuild:
        update_status(icon_id, row, src, summary, tracer, state, note)
    return summary


def update_status(icon_id, row, src, summary, tracer, state, note, rebuild=False):
    """Per-icon status, the tracer's record: every tracer build counts one
    iteration. A whole-set rebuild (build_all.py) never calls this; it leaves
    the status files as the tracers wrote them and refreshes qa/metrics only."""
    path = os.path.join(C.QA, "status", f"{icon_id}.json")
    st = C.read_json(path) or {"id": icon_id, "label": row["label"], "state": "todo", "tracer": None,
                               "iterations": 0, "history": [], "notes": []}
    if not rebuild:
        st["iterations"] = int(st.get("iterations", 0)) + 1
    st["tracer"] = tracer or st.get("tracer") or src.corrections.get("tracer")
    if state:
        st["state"] = state
    elif st.get("state", "todo") == "todo":
        st["state"] = "traced"
    st["last_build"] = now()
    st["last_metrics"] = summary
    st["corrections"] = src.corrections.get("corrections", [])
    st["source_notes"] = src.corrections.get("notes", "")
    if note:
        st.setdefault("notes", []).append({"time": now(), "by": st["tracer"], "note": note})
    st.setdefault("history", []).append({"iteration": st["iterations"], "time": st["last_build"], "state": st["state"],
                                         "kind": "rebuild" if rebuild else "build",
                                         **{k: summary[k] for k in ("silhouette_iou_1x", "red_iou_1x", "edge_mean_px", "edge_p95_px")}})
    C.write_json(path, st)


def main():
    ap = argparse.ArgumentParser(description="Build Civic Line icons from src/<ID>.svg")
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--tracer", help="your agent or person name, recorded in the status file")
    ap.add_argument("--state", choices=STATES[1:], help="set the status state (default: traced on first build)")
    ap.add_argument("--note", help="append a note to the status file")
    a = ap.parse_args()
    results, failures = build(a.ids, a.tracer, a.state, a.note)
    for icon_id, s in results.items():
        print(f"{icon_id}: silhouette IoU {s['silhouette_iou_1x']:.4f}  red IoU {s['red_iou_1x']:.4f}  "
              f"edge mean {s['edge_mean_px']:.3f} px  p95 {s['edge_p95_px']:.3f} px  max {s['edge_max_px']:.2f} px  "
              f"offset {tuple(s['best_offset'])}  area ratio {s['ink_area_ratio_trace_over_reference']:.3f}  "
              f"bake IoU 4x {s['bake_check_iou_4x']:.4f} (1x {s['bake_check_iou_1x']:.4f})  pair ok {s['pair_identical_after_swap']}  inside 0-128 {s['export_inside_0_128']}")
        print(f"    view: qa/overlays/{icon_id}.png  qa/blink/{icon_id}.gif  qa/sizes/{icon_id}.png")
    for icon_id, msg in failures.items():
        print(f"FAILED {msg}", file=sys.stderr)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
