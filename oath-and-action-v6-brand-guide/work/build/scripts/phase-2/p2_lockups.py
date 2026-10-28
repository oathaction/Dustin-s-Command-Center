"""I5 lockups. The main lockups drawn at today's width and at the condensed width, with ampersand B.

Main lockups: L1 wordmark, L2 stacked, L3 horizontal with the lockmark, L8 monogram. V5's color
matrix names L1, L2 and L8 as its primary lockups; L3 is the site and email masthead, the
placement readers see most. L1 is the wordmark master itself (p2_wordmark, p2_condensed).

  L2  OATH over ACTION, leading as V5 (ACTION's cap line 9.96 units under OATH's baseline), the
      ampersand at 1.283 times the wordmark's, centered on the stack's middle so its waist crossing
      sits between the two lines, 10 units clear of the N, as V5
  L3  the wordmark, then the lockmark 2.4 cap heights square, 60 units to the right, centered on
      the cap band, as V5
  L8  O, ampersand, A, with the hinge gaps set by equal white area (I2), as the wordmark

Condensed versions use the condensed letters and the narrow B.

Run: python3 -I p2_lockups.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402
from oa_p2 import o  # noqa: E402
import p1_wordmark as W  # noqa: E402
import p2_amp_b as B2  # noqa: E402
import p2_wordmark as WM  # noqa: E402
import p2_condensed as CD  # noqa: E402

AMP = 'fill="var(--amp,#E63946)"'
INK = 'fill="currentColor"'


def parts(width):
    if width == "condensed":
        return CD.display()[0], B2.display_symbol(narrow_=True)
    return WM.display_parts()[0], B2.display_symbol()


def stacked(width):
    pt, amp0 = parts(width)
    oath = o.union(*[pt[n] for n in ("O", "A", "T", "H")])
    ob = o.bounds(oath)
    oath = o.tx(oath, e=-ob[0])
    action = o.union(*[pt[n] for n in ("A2", "C", "T2", "I", "O2", "N")])
    ab = o.bounds(action)
    action = o.tx(action, e=-ab[0], f=109.96)          # cap line 4 + 100 + 9.96 + 4 - 4: V5's leading
    acb = o.bounds(action)
    b = o.bounds(amp0)
    s = 1.283
    amp = o.tx(amp0, a=s, d=s)
    b = o.bounds(amp)
    mid = (104.0 + 113.96) / 2
    amp = o.tx(amp, e=-b[0], f=mid - (b[1] + b[3]) / 2)
    # 10 units of clear space to the N at the nearest point, across ACTION's cap band
    pa, pn = o.Profile(o.tx(action, f=-109.96)), o.Profile(o.tx(amp, f=-109.96))
    g = o.gap_profiles(pa, pn, 0.0, W.DEPTH)
    amp = o.tx(amp, e=10.0 - g["min"])
    body = f'<path {INK} d="{o.d_from_path(o.union(oath, action))}"/><path {AMP} d="{o.d_from_path(amp)}"/>'
    bx = o.bounds(o.union(oath, action, amp))
    vb = [0, 0, round(bx[2], 2), round(max(217.96, bx[3]), 2)]
    return body, vb, {"amp_scale": s, "amp_box": [round(v, 2) for v in o.bounds(amp)], "width_units": vb[2]}


def horizontal(width):
    pt, _ = parts(width)
    wm = W.to_svg(pt, None)
    bx = o.bounds(o.union(*pt.values()))
    lm, lvb = P.svg_parts(o.SPRITE / "lockmark.svg")
    x = round(bx[2] + 60, 2)
    body = wm + f'<svg x="{x}" y="-66" width="240" height="240" viewBox="0 0 123.5 123.5" overflow="visible">{lm}</svg>'
    vb = [0, -66, round(x + 240, 2), 240]
    return body, vb, {"lockmark_x": x, "width_units": vb[2]}


def monogram(width):
    if width == "condensed":
        cg, specs, _ = CD.letters()
        O_, A_ = cg["O"], cg["A"]
        amp = o.tx(B2.display_symbol(narrow_=True), f=4.0)
    else:
        G, _ = W.glyphs()
        O_, A_ = G["O"], o.tx(G["A"], e=-93.16)
        amp = WM.amp_display()
    ob = o.bounds(O_)
    O_ = o.tx(O_, e=-ob[0])
    # the hinge white on each side matches the wordmark's own (I2), so L8 and L1 share one hinge
    target = (CD.display()[0] if width == "condensed" else WM.display_parts()[0])
    tw = o.pair_gap(target["H"], target["&"], depth=W.DEPTH)["area"]
    pa, pA = o.Profile(o.tx(amp, e=-o.bounds(amp)[0])), o.Profile(o.tx(A_, e=-o.bounds(A_)[0]))
    ow = o.bounds(O_)[2]

    def side(prof_a, prof_b, area):
        lo, hi = -40.0, 80.0
        for _ in range(50):
            mid = (lo + hi) / 2
            if o.gap_profiles(prof_a, prof_b, mid, W.DEPTH)["area"] < area:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    # positions measured from the O's right edge; Profile offsets are relative to each glyph's left ink edge at 0
    dl = side(o.Profile(o.tx(O_, e=-ow)), pa, tw)
    dr = side(o.Profile(o.tx(amp, e=-o.bounds(amp)[2])), pA, tw)
    amp = o.tx(amp, e=ow + dl - o.bounds(amp)[0])
    A_ = o.tx(A_, e=o.bounds(amp)[2] + dr - o.bounds(A_)[0])
    l = o.pair_gap(O_, amp, depth=W.DEPTH)
    r = o.pair_gap(amp, A_, depth=W.DEPTH)
    body = f'<path {INK} d="{o.d_from_path(o.union(O_, A_))}"/><path {AMP} d="{o.d_from_path(amp)}"/>'
    bx = o.bounds(o.union(O_, amp, A_))
    vb = [0, 0, round(bx[2], 2), 108]
    return body, vb, {"hinge_left_area_x": round(l["area"] / 100, 3), "hinge_right_area_x": round(r["area"] / 100, 3),
                      "nearest_left_x": round(l["min"] / 100, 3), "nearest_right_x": round(r["min"] / 100, 3), "width_units": vb[2]}


NAMES = {"L2": ("Stacked", stacked), "L3": ("Horizontal", horizontal), "L8": ("Monogram", monogram)}


def export():
    out = {}
    for lk, (nm, fn) in NAMES.items():
        for width in ("regular", "condensed"):
            body, vb, info = fn(width)
            suffix = "-Condensed" if width == "condensed" else ""
            f = P.write_svg(P.asset("lockups", f"{P.DATE}_{lk}-{nm}{suffix}-Master.svg"), vb, body,
                            f"{lk} {nm.lower()} lockup, {'condensed 7.5 to 1' if width == 'condensed' else 'today' + chr(39) + 's width'}, ampersand B (Phase 2)")
            out[f"{lk}_{width}"] = {"file": P.rel(f), "viewBox": vb, **info}
    P.save_json(P.SCRATCH / "specs/lockups.json", out)
    return out


if __name__ == "__main__":
    print(json.dumps(export(), indent=1))
