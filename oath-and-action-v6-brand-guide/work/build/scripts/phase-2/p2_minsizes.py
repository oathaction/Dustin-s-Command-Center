"""I8. One minimum-size rule, computed from the Phase 2 masters, as a table the guide can carry.

The rule: on screen, no identity mark draws its capitals under 14 px and no tagline inside a lockup
sets under 13 px; in print, no capitals under 3 mm and no tagline under 7 pt. Each lockup names
its replacement below its minimum. Favicons use the ampersand's 16 px master.

Inter's cap height is 0.727 em, so a 13 px tagline has 9.45 px capitals and a 7 pt tagline 5.09 pt.
L4 to L7 are not redrawn in this pass; their minimums come from V5's layouts with the re-exported
taglines (I1) and the Phase 2 wordmark width.

Run: python3 -I p2_minsizes.py
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oa_p2 as P  # noqa: E402

CAP_PX, TAG_PX, CAP_MM, TAG_PT = 14.0, 13.0, 3.0, 7.0
INTER_CAP = 0.727
MM_PER_IN = 25.4


def up(v, step):
    return math.ceil(v / step - 1e-9) * step


def spec(name):
    return P.load_json(P.SCRATCH / f"specs/{name}.json")


def build():
    wm, cd, lk, mk = spec("wordmark"), spec("condensed"), spec("lockups"), spec("marks")
    wd, cdd = wm["display"]["viewBox"][2], cd["display"]["viewBox"][2]
    rows = []

    def print_w(units_wide, cap_units=100.0):
        """Print width in inches at which the capitals reach 3 mm, rounded up to 0.05 in."""
        return up(units_wide * (CAP_MM / MM_PER_IN) / cap_units, 0.05)

    rows.append({"lockup": "L1 wordmark",
                 "v5": "120 px wide (13.4 px tall, cap 12.4 px)",
                 "screen": f"16 px tall: 16 px master from 16 to 19 px tall ({wm['16']['viewBox'][2]} px wide; condensed {cd['16']['viewBox'][2]} px), 24 px master from 20 to 39 px, display master from 40 px",
                 "print": f"{print_w(wd):.2f} in wide (condensed {print_w(cdd):.2f} in)",
                 "below": "Use L8; below 48 px wide, the ampersand's 16 px master"})
    l2, l2c = lk["L2_regular"]["width_units"], lk["L2_condensed"]["width_units"]
    rows.append({"lockup": "L2 stacked", "v5": "72 px wide (cap 11.5 px)",
                 "screen": f"{math.ceil(l2 * CAP_PX / 100)} px wide (condensed {math.ceil(l2c * CAP_PX / 100)} px), capitals 14 px",
                 "print": f"{print_w(l2):.2f} in wide (condensed {print_w(l2c):.2f} in)", "below": "Use L8"})
    # L3: the wordmark's 16 px master, 60 units of gap and the lockmark at 2.4 cap heights
    k = CAP_PX / 100
    l3 = wm["16"]["viewBox"][2] + 60 * k + 240 * k
    l3c = cd["16"]["viewBox"][2] + 60 * k + 240 * k
    rows.append({"lockup": "L3 horizontal with lockmark", "v5": "192 px wide",
                 "screen": f"{up(l3, 4):.0f} px wide (condensed {up(l3c, 4):.0f} px): wordmark 16 px master, lockmark 34 px from its 24 px master",
                 "print": f"{print_w(lk['L3_regular']['width_units']):.2f} in wide (condensed {print_w(lk['L3_condensed']['width_units']):.2f} in)",
                 "below": "Use L1"})
    # taglines: re-exported symbols, cap 100 of their own units
    tag_cap_l5 = 100 * 25.92 / 108           # tl-1 in L5 drawn 25.92 units tall for a 108 unit box
    s13 = TAG_PX * INTER_CAP / tag_cap_l5     # px per L5 unit at a 13 px tagline
    s7 = TAG_PT * INTER_CAP / 72 / tag_cap_l5  # inches per L5 unit at a 7 pt tagline
    rows.append({"lockup": "L5 wordmark and tagline", "v5": "240 px wide (tagline cap 5.9 px)",
                 "screen": f"{up(wd * s13, 4):.0f} px wide (tagline at 13 px)", "print": f"{up(wd * s7, 0.05):.2f} in (tagline at 7 pt)",
                 "below": "Use L1 and set the tagline as live text"})
    tag_cap_l4 = 100 * 23.76 / 108
    l4w = 706.7
    rows.append({"lockup": "L4 monogram and tagline", "v5": "144 px wide (tagline cap 4.5 px)",
                 "screen": f"{up(l4w * TAG_PX * INTER_CAP / tag_cap_l4, 4):.0f} px wide (tagline at 13 px)",
                 "print": f"{up(l4w * TAG_PT * INTER_CAP / 72 / tag_cap_l4, 0.05):.2f} in (tagline at 7 pt)", "below": "Use L8 and set the tagline as live text"})
    tag_cap_l6 = 100 * 16.2 / 108
    rows.append({"lockup": "L6 editorial signature", "v5": "288 px wide (tagline cap 3.1 px)",
                 "screen": f"{up(1400 * TAG_PX * INTER_CAP / tag_cap_l6, 4):.0f} px wide (tagline at 13 px)",
                 "print": f"{up(1400 * TAG_PT * INTER_CAP / 72 / tag_cap_l6, 0.05):.2f} in (tagline at 7 pt)", "below": "Use L3 with the tagline as live text"})
    rows.append({"lockup": "L7 section masthead", "v5": "168 px wide",
                 "screen": "250 px wide (pillar word at 13 px), from V5's layout", "print": "1.90 in (pillar word at 7 pt)",
                 "below": "Use L1 and name the pillar in live text"})
    l8, l8c = lk["L8_regular"]["width_units"], lk["L8_condensed"]["width_units"]
    rows.append({"lockup": "L8 monogram", "v5": "48 px wide, also listed for favicons",
                 "screen": f"48 px wide (capitals {48 * 100 / l8:.1f} px; condensed {48 * 100 / l8c:.1f} px). Never a favicon",
                 "print": f"{max(0.5, print_w(l8)):.2f} in wide", "below": "Use the ampersand's 16 px master"})
    rows.append({"lockup": "Ampersand B, freestanding", "v5": "16 px with V5's stroked optical drawing",
                 "screen": "16 px master from 16 to 23 px tall; 24 px master from 24 to 47 px; display master from 48 px",
                 "print": "0.25 in tall", "below": "Nothing smaller. Favicon: the 16 px master at 16 px"})
    rows.append({"lockup": "Lockmark", "v5": "16 px, one color",
                 "screen": "16 px master from 16 to 23 px; 24 px master from 24 to 47 px; V5 master from 48 px",
                 "print": "0.25 in", "below": "Nothing smaller; the lever stays one size up at 16 and 24 px"})
    hd, hc = mk["hinge_regular_display"], mk["hinge_regular_compact"]
    hdc, hcc = mk["hinge_condensed_display"], mk["hinge_condensed_compact"]
    rows.append({"lockup": "Hinge diagram V2", "v5": "None set",
                 "screen": f"Display master from {hd['min_width_px']} px wide (labels at 13 px; condensed {hdc['min_width_px']} px); compact master from {hc['min_width_px']} px (lines 1 px; condensed {hcc['min_width_px']} px)",
                 "print": f"{up(hd['viewBox'][2] * TAG_PT * INTER_CAP / 72 / 26, 0.05):.2f} in wide (labels at 7 pt)", "below": "Use a hinge headline"})
    rows.append({"lockup": "Hinge-circle badge", "v5": "New mark (S9)",
                 "screen": "16 px master from 16 to 23 px; 24 px master from 24 to 47 px; display master from 48 px",
                 "print": "0.25 in", "below": "Nothing smaller. Never an avatar or favicon"})
    rule = ("On screen, no identity mark draws its capitals under 14 px, and no tagline inside a lockup sets under 13 px. "
            "In print, no capitals under 3 mm and no tagline under 7 pt. Each lockup names its replacement below its minimum. "
            "Favicons use the ampersand's 16 px master.")
    order = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"]
    rows.sort(key=lambda r: order.index(r["lockup"][:2]) if r["lockup"][:2] in order else 99)
    out = {"rule": rule, "rows": rows}
    P.save_json(P.SCRATCH / "specs/minsizes.json", out)
    P.save_json(P.asset(f"{P.DATE}_Identity-Minimum-Sizes.json"), out)
    return out


def markdown(out):
    lines = ["| Lockup | V5 minimum | Screen minimum | Print minimum | Below the minimum |", "|---|---|---|---|---|"]
    for r in out["rows"]:
        lines.append(f"| {r['lockup']} | {r['v5']} | {r['screen']} | {r['print']} | {r['below']} |")
    return "\n".join(lines)


if __name__ == "__main__":
    r = build()
    print(r["rule"])
    print(markdown(r))
