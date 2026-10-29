"""Measure a reference crop to place geometry: fit lines and circles to the
stroke centreline inside a box, read widths, and find red extents.

    python3 -I fit_ref.py <ID> line   x0,y0,x1,y1
    python3 -I fit_ref.py <ID> circle x0,y0,x1,y1
    python3 -I fit_ref.py <ID> width  x0,y0,x1,y1
    python3 -I fit_ref.py <ID> extent x0,y0,x1,y1 [--red]
    python3 -I fit_ref.py <ID> corner x0,y0,x1,y1

Boxes are in crop pixel coordinates, the same coordinates as src/<ID>.svg and
the grid on qa/ref-zoom/<ID>.png. The centreline is the medial axis of the 8x
ink mask (the same mask the stroke measurement uses). Put only one stroke
segment in a box for 'line', only one arc for 'circle'.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cl_common as C  # noqa: E402
import stroke_width as SW  # noqa: E402
from skimage.morphology import medial_axis  # noqa: E402


def centreline(row, red=False):
    rc = os.path.join(C.ASSETS, "reference-crops")
    mp = row["mask_params"]
    if red:
        rgb = C.load_rgb(os.path.join(rc, row["reference_crops"]["red"]))
        v = SW.upsampled(C.redness(rgb), SW.Z, SW.SIGMA)
        m = v > mp["red_threshold"]
    else:
        rgb = C.load_rgb(os.path.join(rc, row["reference_crops"]["black"]))
        m = SW.upsampled_mask(C.green(rgb), mp["ink_threshold_g"], SW.Z, SW.SIGMA)
    sk, d = medial_axis(m, return_distance=True, rng=0)
    ys, xs = np.nonzero(sk)
    return (xs + 0.5) / SW.Z, (ys + 0.5) / SW.Z, 2 * d[sk] / SW.Z, m


def in_box(X, Y, b):
    return (X >= b[0]) & (X <= b[2]) & (Y >= b[1]) & (Y <= b[3])


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    icon_id, mode, box = sys.argv[1], sys.argv[2], [float(v) for v in sys.argv[3].split(",")]
    red = "--red" in sys.argv
    row = C.inventory_by_id()[icon_id]
    X, Y, D, m = centreline(row, red)
    sel = in_box(X, Y, box)
    if mode == "extent":
        z = SW.Z
        yy, xx = np.nonzero(m)
        fx, fy = (xx + 0.5) / z, (yy + 0.5) / z
        s2 = in_box(fx, fy, box)
        if not s2.any():
            print("no ink in box")
            return
        print(f"{'red' if red else 'ink'} extent in box: x {fx[s2].min() - 0.5 / z:.2f} to {fx[s2].max() + 0.5 / z:.2f}, "
              f"y {fy[s2].min() - 0.5 / z:.2f} to {fy[s2].max() + 0.5 / z:.2f} (edges, not centreline)")
        if sel.any():
            print(f"centreline in box: x {X[sel].min():.2f} to {X[sel].max():.2f}, y {Y[sel].min():.2f} to {Y[sel].max():.2f}")
        return
    if sel.sum() < 5:
        print(f"only {int(sel.sum())} centreline points in the box")
        return
    x, y, d = X[sel], Y[sel], D[sel]
    if mode == "width":
        print(f"width median {np.median(d):.2f} px, p25 {np.percentile(d, 25):.2f}, p75 {np.percentile(d, 75):.2f}, n {len(d)}")
    elif mode == "line":
        mx, my = x.mean(), y.mean()
        u, s, vt = np.linalg.svd(np.c_[x - mx, y - my], full_matrices=False)
        dx, dy = vt[0]
        t = (x - mx) * dx + (y - my) * dy
        res = (x - mx) * (-dy) + (y - my) * dx
        a = (mx + t.min() * dx, my + t.min() * dy)
        b = (mx + t.max() * dx, my + t.max() * dy)
        ang = np.degrees(np.arctan2(dy, dx)) % 180
        print(f"line from ({a[0]:.2f}, {a[1]:.2f}) to ({b[0]:.2f}, {b[1]:.2f}), angle {ang:.2f} deg "
              f"(0 = horizontal, 90 = vertical), rms off-line {np.sqrt((res ** 2).mean()):.2f} px, "
              f"width {np.median(d):.2f} px, n {len(x)}")
        print("  endpoints are centreline ends: a round cap adds half the stroke beyond them")
    elif mode == "circle":
        A = np.c_[2 * x, 2 * y, np.ones_like(x)]
        c = np.linalg.lstsq(A, x * x + y * y, rcond=None)[0]
        r = np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2)
        res = np.hypot(x - c[0], y - c[1]) - r
        ang = np.degrees(np.arctan2(y - c[1], x - c[0]))
        print(f"circle centre ({c[0]:.2f}, {c[1]:.2f}) r {r:.2f}, rms {np.sqrt((res ** 2).mean()):.2f} px, "
              f"arc angles {ang.min():.1f} to {ang.max():.1f} deg (0 = right, 90 = down), width {np.median(d):.2f} px, n {len(x)}")
    elif mode == "corner":
        # two dominant lines in the box and their intersection
        pts = np.c_[x, y]
        best = None
        rng = np.random.default_rng(0)
        for _ in range(400):
            i, j = rng.choice(len(pts), 2, replace=False)
            p, q = pts[i], pts[j]
            n = np.array([-(q - p)[1], (q - p)[0]])
            if np.linalg.norm(n) < 1e-6:
                continue
            n /= np.linalg.norm(n)
            inl = np.abs((pts - p) @ n) < 0.6
            if best is None or inl.sum() > best[0].sum():
                best = (inl, p, n)
        inl1 = best[0]
        rest = pts[~inl1]
        best2 = None
        for _ in range(400):
            if len(rest) < 2:
                break
            i, j = rng.choice(len(rest), 2, replace=False)
            p, q = rest[i], rest[j]
            n = np.array([-(q - p)[1], (q - p)[0]])
            if np.linalg.norm(n) < 1e-6:
                continue
            n /= np.linalg.norm(n)
            inl = np.abs((rest - p) @ n) < 0.6
            if best2 is None or inl.sum() > best2[0].sum():
                best2 = (inl, p, n)
        if best2 is None:
            print("only one line found")
            return

        def refit(P):
            mpt = P.mean(0)
            _, _, vt = np.linalg.svd(P - mpt)
            return mpt, vt[0]
        p1, d1 = refit(pts[inl1])
        p2, d2 = refit(rest[best2[0]])
        M = np.c_[d1, -d2]
        if abs(np.linalg.det(M)) < 1e-6:
            print("lines are parallel")
            return
        t = np.linalg.solve(M, p2 - p1)
        ip = p1 + t[0] * d1
        a1 = np.degrees(np.arctan2(d1[1], d1[0])) % 180
        a2 = np.degrees(np.arctan2(d2[1], d2[0])) % 180
        print(f"corner at ({ip[0]:.2f}, {ip[1]:.2f}); lines at {a1:.1f} and {a2:.1f} deg; "
              f"{int(inl1.sum())} and {int(best2[0].sum())} points")
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
