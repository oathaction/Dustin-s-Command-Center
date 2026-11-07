"""S1 stacked lockup masters, apply pass, November 7, 2026 (DR-113, D2-328).

Copies Board 6's S1 files into the identity masters with a clean <title> and no board notes, checks that every contour
is a wordmark or ampersand B master contour moved by translation alone, writes S1's Charcoal edition beside each master
and its Prussian White edition in prussian/ (treatment D: one color, White, as every other Prussian file), and updates
the minimum sizes table: S1 added, L2 retired with a pointer to S1, the badge from 48 px (DR-118), and the condensed
figures marked as kept for the record (DR-115, D2-328).

Writes
  work/build/assets/identity/lockups/20261107_S1-Stacked-Master.svg, -24px.svg, -16px.svg
  work/build/assets/identity/lockups/20261107_S1-Stacked-Master-Charcoal.svg, -24px-Charcoal.svg, -16px-Charcoal.svg
  work/build/assets/identity/prussian/20261107_S1-Stacked-Master-Prussian-White.svg, -24px-, -16px- (Prussian-White)
  work/build/assets/identity/20261028_Identity-Minimum-Sizes.json (rows updated in place, idempotent)
Reads Board 6's S1 files and the wordmark and B masters, and writes none of them. L2's files stay where they are.

Fix pass, November 7, 2026 (CD-S8, CA-S9, D2-298): writes the lockmark's display master under a name without the
edition, lockmark/20261107_Lockmark-Display-Master.svg and its Prussian White file, as byte-for-byte copies of the
drawing in 20261028_Lockmark-Master-V5.svg with a clean title. The V5-named files stay, since Board 6's scripts read
them; the asset package retires them. The minimum table calls that master "display master".

Run: python3 -I work/build/scripts/phase-2/stage_a_identity_s1.py      (prints the contour check)
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board6_stacked_geom as G  # noqa: E402  (path reader and glyph split, read only)

ROOT = HERE.parents[3]
ID = ROOT / "work/build/assets/identity"
SRC = ROOT / "work/boards/phase-2/board-6/stacked"
CHARCOAL, RED, WHITE = "#121212", "#E63946", "#FFFFFF"

# size key: (Board 6 source, master name, wordmark master key, B master key, title tail)
FILES = {
    "display": ("20261107_Stacked-S1-Ampersand-Ends-Line-One.svg", "20261107_S1-Stacked-Master.svg", "wm_display", "b_display",
                "display master. Capitals 100 units; line one's cap line at y 4"),
    24: ("20261107_Stacked-S1-Ampersand-Ends-Line-One-24px.svg", "20261107_S1-Stacked-Master-24px.svg", "wm_24", "b_24",
         "24 px master on the pixel grid, capitals 22 px, for capitals 18 to 36 px"),
    16: ("20261107_Stacked-S1-Ampersand-Ends-Line-One-16px.svg", "20261107_S1-Stacked-Master-16px.svg", "wm_16", "b_16",
         "16 px master on the pixel grid, capitals 14 px, for capitals 14 to 17 px"),
}
HEAD = "S1 stacked lockup, OATH & over ACTION, flush left, cut from the wordmark and ampersand B masters at today's width"


def esc(t):
    return t.replace("&", "&amp;").replace("'", "&#x27;")


def clean(svg, tail):
    """Replace the board's title with the master's own; nothing else in the file changes."""
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(HEAD)}: {esc(tail)}</title>", svg, count=1, flags=re.S)
    assert "Board 6" not in s and "exploration" not in s
    return s


def paths(svg):
    return [(fill, G.parse_d(d)) for fill, d in re.findall(r'<path fill="([^"]+)" d="([^"]+)"', svg)]


def pts(subs):
    return [p for sp in subs for seg in sp for p in seg[1:]]


def same_by_translation(a, b):
    """The largest offset between two glyphs once one is moved by the difference of their first points; None when the
    point counts differ. A glyph that matches by translation alone has an offset near zero."""
    pa, pb = pts(a), pts(b)
    if len(pa) != len(pb):
        return None
    dx, dy = pb[0][0] - pa[0][0], pb[0][1] - pa[0][1]
    return max(max(abs(x1 - x0 - dx), abs(y1 - y0 - dy)) for (x0, y0), (x1, y1) in zip(pa, pb))


def check(svg, size):
    """Every letter of S1 is a wordmark master letter moved, and B is B's master moved, with no scale."""
    _, wm_key, b_key = FILES[size][1], FILES[size][2], FILES[size][3]
    _, letters, b_in_wm = G.letters(wm_key)
    _, b_alone = G.b_master(b_key)
    ink = [sp for f, ss in paths(svg) if f == "currentColor" for sp in ss]
    amp = [sp for f, ss in paths(svg) if f.startswith("var(--amp") for sp in ss]
    glyphs = G.split_glyphs(ink)
    out = {"size": str(size), "contours": len(ink) + len(amp), "letters": len(glyphs), "worst_offset": 0.0, "matched": []}
    assert len(glyphs) == 10, f"S1 {size}: {len(glyphs)} letters"
    used = set()
    for g in glyphs:
        best = None
        for name, m in letters.items():
            if name in used:
                continue
            off = same_by_translation(m.subs, g)
            if off is not None and (best is None or off < best[1]):
                best = (name, off)
        assert best is not None and best[1] < 1e-6, f"S1 {size}: a letter matches no master letter by translation"
        used.add(best[0])
        out["matched"].append(best[0])
        out["worst_offset"] = max(out["worst_offset"], best[1])
    for ref, label in ((b_alone.subs, "B master"), (b_in_wm.subs, "B in the wordmark")):
        off = same_by_translation(ref, amp)
        assert off is not None and off < 1e-3, f"S1 {size}: B does not match {label} by translation"
        out[f"b_vs_{'master' if label == 'B master' else 'wordmark'}"] = off
    out["worst_offset"] = max(out["worst_offset"], out["b_vs_master"])
    return out


def charcoal(svg):
    s = svg.replace('fill="currentColor"', f'fill="{CHARCOAL}"').replace('fill="var(--amp,#E63946)"', f'fill="{RED}"')
    s = re.sub(r"</title>", ". Charcoal edition: Charcoal letters and ampersand B in signature red, explicit colors for "
                            "Newsprint and White grounds</title>", s, count=1)
    assert sorted(set(re.findall(r"#[0-9A-Fa-f]{6}", s))) == [CHARCOAL, RED]
    return s


def prussian_white(svg):
    s = svg.replace('fill="currentColor"', f'fill="{WHITE}"').replace('fill="var(--amp,#E63946)"', f'fill="{WHITE}"')
    s = re.sub(r"</title>", ". Treatment D for Prussian: one color, White</title>", s, count=1)
    assert sorted(set(re.findall(r"#[0-9A-Fa-f]{6}", s))) == [WHITE] and "currentColor" not in s and "var(" not in s
    return s


def d_only(svg):
    return re.findall(r' d="([^"]+)"', svg)


# ------------------------------------------------------------------------------------------- minimum sizes table
MIN_FILE = ID / "20261028_Identity-Minimum-Sizes.json"
S1_ROW = {
    "lockup": "S1 stacked",
    "v5": "None. New in Edition 06; replaced L2 on November 7, 2026 (DR-113)",
    "screen": "79 px wide, capitals 14 px: 16 px master for capitals 14 to 17 px (79 by 33 px), 24 px master for capitals 18 to 36 px (115 by 50 px), display master from 37 px",
    "print": "0.65 in wide",
    "below": "Use L8",
    "files": ["lockups/20261107_S1-Stacked-Master.svg", "lockups/20261107_S1-Stacked-Master-24px.svg",
              "lockups/20261107_S1-Stacked-Master-16px.svg"],
    "source": "work/boards/phase-2/board-6/stacked/20261107_Board-6-Stacked-Measurements.json, variant S1",
}
CONDENSED_NOTE = ("Figures marked condensed belong to the condensed wordmark, kept in the files for the record and not in use: "
                  "Edition 06 keeps today's width (DR-115, D2-328).")


def update_minimums():
    d = json.loads(MIN_FILE.read_text())
    rows = d["rows"]
    rows[:] = [r for r in rows if r.get("lockup") != "S1 stacked"]
    i = next(k for k, r in enumerate(rows) if r["lockup"] == "L2 stacked")
    rows[i].update({"status": "retired", "replaced_by": "S1 stacked",
                    "status_note": "Kept for the record. S1 replaced L2 on November 7, 2026 (DR-113); its files stay in lockups/ and prussian/."})
    rows.insert(i + 1, dict(S1_ROW))
    for r in rows:
        if any("condensed" in str(r.get(k, "")) for k in ("screen", "print")):
            r["condensed"] = "kept for the record, not in use (D2-328)"
        if r["lockup"] == "Hinge-circle badge":
            r.update({"screen": "48 px, from the display master",
                      "masters_note": "The 16 px and 24 px badge masters stay in badge/ for the record and are not placed",
                      "print": "0.50 in",
                      "below": "End an article with ampersand B alone (Rule 04.6). Never an avatar or favicon",
                      "status_note": "From 48 px only, for back covers and events, since November 7, 2026 (DR-118)"})
        if r["lockup"] == "Lockmark":
            r["screen"] = r["screen"].replace("V5 master from 48 px", "display master from 48 px")
            r["files"] = ["lockmark/20261028_Lockmark-16px-Master.svg", "lockmark/20261028_Lockmark-24px-Master.svg",
                          "lockmark/20261107_Lockmark-Display-Master.svg"]
        if r["lockup"] == "L8 monogram":
            r["screen"] = r["screen"].replace("Never a favicon", "Never an avatar or a favicon")
            r["status_note"] = ("For squares where the name must show, such as a tile in a partner's directory. Social avatars "
                                "and the app icon show ampersand B alone on the Charcoal tile (DR-116)")
    d["condensed"] = CONDENSED_NOTE
    d["updated"] = "November 7, 2026, apply pass: S1 added, L2 retired, the badge from 48 px, condensed figures kept for the record"
    MIN_FILE.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    return d


LOCK_OLD = ("lockmark/20261028_Lockmark-Master-V5.svg", "prussian/20261028_Lockmark-Master-V5-Prussian-White.svg")
LOCK_NEW = ("lockmark/20261107_Lockmark-Display-Master.svg", "prussian/20261107_Lockmark-Display-Master-Prussian-White.svg")
LOCK_TITLE = "Lockmark, display master, for 48 px and up: the fifth edition's geometry, unchanged"


def display_lockmark():
    """The display master under its new name: same drawing, clean title."""
    out = []
    for old, new in zip(LOCK_OLD, LOCK_NEW):
        src = (ID / old).read_text()
        tail = ". Treatment D for Prussian: one color, White" if "prussian/" in old else ""
        dst = re.sub(r"<title>.*?</title>", f"<title>{esc(LOCK_TITLE)}{tail}</title>", src, count=1, flags=re.S)
        assert "V5" not in dst and re.sub(r"<title>.*?</title>", "", dst) == re.sub(r"<title>.*?</title>", "", src)
        (ID / new).write_text(dst)
        out.append(new)
    return out


def run():
    report = []
    for size, (src, name, _, _, tail) in FILES.items():
        svg = clean((SRC / src).read_text(), tail)
        master = ID / "lockups" / name
        master.write_text(svg)
        c = check(master.read_text(), size)
        stem = master.stem
        ch = ID / "lockups" / f"{stem}-Charcoal.svg"
        ch.write_text(charcoal(svg))
        pw = ID / "prussian" / f"{stem}-Prussian-White.svg"
        pw.write_text(prussian_white(svg))
        assert d_only(ch.read_text()) == d_only(svg) == d_only(pw.read_text()), "an edition's paths differ from the master"
        assert d_only(svg) == d_only((SRC / src).read_text()), "the master's paths differ from Board 6's file"
        c["files"] = [str(p.relative_to(ROOT)) for p in (master, ch, pw)]
        report.append(c)
    update_minimums()
    display_lockmark()
    return report


if __name__ == "__main__":
    for c in run():
        print(f'S1 {c["size"]}: {c["contours"]} contours, {c["letters"]} letters matched ({" ".join(c["matched"])}), '
              f'B vs its master {c["b_vs_master"]:.1e}, B vs the wordmark\'s B {c["b_vs_wordmark"]:.1e}, '
              f'worst offset {c["worst_offset"]:.1e} units')
        for f in c["files"]:
            print("  wrote", f)
    print("updated", MIN_FILE.relative_to(ROOT))
    print("wrote", ", ".join(LOCK_NEW))
