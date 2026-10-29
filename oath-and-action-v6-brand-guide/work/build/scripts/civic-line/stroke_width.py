"""Stroke-width estimators shared by the scale step and the build tool.

The core rule follows the brief: take the ink mask's medial axis and the
Euclidean distance transform, and read the stroke width as twice the distance
at skeleton points. On a 1x mask that reading is quantised to whole pixels, so
the pipeline takes it on an 8x mask: the crop's green channel upsampled
bilinearly, smoothed with a 3 px Gaussian (at 8x) to remove the staircase that
grows medial-axis spurs on diagonal edges, then thresholded at the same
midpoint. That mask puts each edge where antialiased coverage crosses one half,
which is where a rendered stroke of width W also puts it.

`calibrate()` measures synthetic antialiased rings and bars of known width
(5 to 7 px in 0.25 px steps, at 0, 10, 30 and 45 degrees). At 8x the reading
2 * d / 8 is off by +0.01 px on average, 0.05 px standard deviation and
0.16 px at worst. At 4x it is +0.02 px, 0.12 px and 0.32 px; at 1x, 2 * d is
quantised to whole pixels and is off by up to 1.5 px.
"""
import numpy as np
from scipy import ndimage as ndi
from skimage.morphology import medial_axis


def skeleton_widths(mask, scale=1):
    """Width samples (in source px) at medial-axis points of a boolean mask
    drawn at `scale` times source resolution."""
    if not mask.any():
        return np.array([])
    skel, dist = medial_axis(mask, return_distance=True, rng=0)  # fixed tie-breaking: reproducible
    d = dist[skel]
    return 2.0 * d / scale


def upsampled(gray, z=4, sigma=1.5):
    """Bilinear upsample of a single-channel crop to z times, pixel-centre aligned,
    then a light Gaussian of sigma (in upsampled px)."""
    h, w = gray.shape
    yy = (np.arange(h * z) + 0.5) / z - 0.5
    xx = (np.arange(w * z) + 0.5) / z - 0.5
    Y, X = np.meshgrid(yy, xx, indexing="ij")
    v = ndi.map_coordinates(gray.astype(np.float64), [Y, X], order=1, mode="nearest")
    if sigma:
        v = ndi.gaussian_filter(v, sigma)
    return v


def upsampled_mask(gray, thr, z=4, sigma=1.5):
    """4x ink mask: upsampled green channel darker than thr."""
    return upsampled(gray, z, sigma) < thr


def robust_median(samples):
    """Median of the skeleton widths after dropping samples above 2.5 times the
    raw median: those come from filled shapes, junction blobs and dense clusters."""
    if len(samples) == 0:
        return float("nan"), 0
    m = np.median(samples)
    keep = samples[samples <= 2.5 * m]
    return float(np.median(keep)), int(len(keep))


def _aa_ring(width, radius=30.0, size=90, ss=8):
    """Antialiased ring of a given stroke width as green-channel values (bg 219, ink 7)."""
    n = size * ss
    c = (n - 1) / 2.0
    y, x = np.mgrid[0:n, 0:n]
    r = np.hypot(y - c, x - c) / ss
    hi = (np.abs(r - radius) <= width / 2.0).astype(np.float64)
    cov = hi.reshape(size, ss, size, ss).mean(axis=(1, 3))
    return 219.0 - cov * (219.0 - 7.0)


def _aa_bar(width, angle_deg, size=90, ss=8):
    n = size * ss
    c = (n - 1) / 2.0
    y, x = np.mgrid[0:n, 0:n]
    t = np.deg2rad(angle_deg)
    d = np.abs((x - c) * np.sin(t) - (y - c) * np.cos(t)) / ss
    along = np.abs((x - c) * np.cos(t) + (y - c) * np.sin(t)) / ss
    hi = ((d <= width / 2.0) & (along <= 30)).astype(np.float64)
    cov = hi.reshape(size, ss, size, ss).mean(axis=(1, 3))
    return 219.0 - cov * (219.0 - 7.0)


Z = 8
SIGMA = 3.0


def measure(gray, thr):
    """Per-icon stroke width in source px: 8x estimator, robust median."""
    return robust_median(skeleton_widths(upsampled_mask(gray, thr, Z, SIGMA), Z))


def calibrate():
    """Measure known widths with the 1x, 4x and 8x estimators. Returns rows of
    (true width, shape, 1x median, 4x median, 8x median)."""
    rows = []
    thr = (219.0 + 7.0) / 2.0
    for w in np.arange(5.0, 7.01, 0.25):
        for name, g in [("ring", _aa_ring(w)), ("bar0", _aa_bar(w, 0)), ("bar10", _aa_bar(w, 10)),
                        ("bar30", _aa_bar(w, 30)), ("bar45", _aa_bar(w, 45))]:
            rows.append((float(w), name, robust_median(skeleton_widths(g < thr, 1))[0],
                         robust_median(skeleton_widths(upsampled_mask(g, thr, 4, 1.5), 4))[0],
                         measure(g, thr)[0]))
    return rows


def calibration_summary():
    rows = calibrate()
    out = {}
    for k, name in [(2, "1x"), (3, "4x"), (4, "8x")]:
        e = np.array([r[k] - r[0] for r in rows])
        out[name] = {"mean_error": round(float(e.mean()), 3), "sd": round(float(e.std()), 3),
                     "max_abs_error": round(float(np.abs(e).max()), 3)}
    out["cases"] = len(rows)
    return out


if __name__ == "__main__":
    for r in calibrate():
        print(f"true {r[0]:5.2f}  {r[1]:6s}  1x {r[2]:5.2f}  4x {r[3]:5.2f}  8x {r[4]:5.2f}")
    print(calibration_summary())
