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

Q1 to Q4 pass, November 8, 2026 (DR-129 to DR-131): copies the 48 px lockmark master Dustin approved from the changes
board's proposal into lockmark/20261108_Lockmark-48px-Master.svg with a clean title, the drawing byte for byte the
same, and writes its Prussian White file by treatment D. Writes a new L3 master for the masthead,
lockups/20261108_L3-Horizontal-Master.svg, from the 24 px wordmark master and the 48 px lockmark master on the pixel
grid, and its Prussian White file; the October L3 files stay as the record. The display master's title names its new
range. The minimum sizes table gains the lockmark's four masters and their ranges, the end mark's exception on B's row
(DR-130), L3's masthead form and L6's replacement under 884 px (DR-129).

Run: python3 -I work/build/scripts/phase-2/stage_a_identity_s1.py      (prints the contour check)
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board6_stacked_geom as G  # noqa: E402  (path reader and glyph split, read only)
from stage_a_identity_lib import LOCK, LOCK_DISPLAY_FROM, L3, WM  # noqa: E402  (file names and the lockmark's ranges)

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
            r["screen"] = (f"16 px master from 16 to 23 px; 24 px master from 24 to 47 px; 48 px master {M48_RANGE}; "
                           f"display master from {LOCK_DISPLAY_FROM} px")
            r["files"] = ["lockmark/20261028_Lockmark-16px-Master.svg", "lockmark/20261028_Lockmark-24px-Master.svg",
                          LOCK[48], "lockmark/20261107_Lockmark-Display-Master.svg"]
            r["below"] = "Nothing smaller; the lever stays one size up at 16, 24 and 48 px"
            r["print"] = "0.25 in; the sign-off at 0.50 in from the display master"
            r["places"] = ("Masthead (inside L3) and sign-off: the 48 px master at 48 px. Page header and footer: the 24 px master "
                           "at 24 px. A chart's footer: the 16 px master at 16 px. In print, the sign-off at 0.50 in takes the "
                           "display master, since the 48 px master is drawn for a screen's pixel grid (Rule 08.2)")
            r["status_note"] = ("The 48 px master joined on November 8, 2026 (DR-131). A test set its range: drawn from "
                                "one rect per pixel row, it parts into stripes at any size between whole multiples of its grid, "
                                "so builders place it at 48 px only (work/handoffs/phase-2/20261108_Q1-To-Q4-Identity-Figures.json, key range)")
        if r["lockup"] == "Ampersand B, freestanding":
            r["below"] = ("Nothing smaller, except the end mark, which stands at the text's cap height (Rule 04.6). "
                          "Favicon: the 16 px master at 16 px")
            r["end_mark"] = ("Only the end mark, ampersand B at the close of an article, may stand under 16 px, at the text's cap height, because it follows a word and "
                             "names nothing on its own (DR-130, Rules 03.4 and 04.6). It stands 16/14 of the text's cap height tall, "
                             "from the 16 px master")
        if r["lockup"] == "L3 horizontal with lockmark":
            r["screen"] = ("196 px wide (condensed 164 px): wordmark 16 px master, lockmark 34 px from its 24 px master. "
                           "In the masthead, 282 px wide from its masthead master: the wordmark's 24 px master, 13 px of space and the lockmark at 48 px from its 48 px master")
            r["files"] = [L3["masthead"], L3["today"]]
            r["print"] = "1.55 in wide (condensed 1.30 in), from the earlier L3 master (Rule 03.2)"
            r["print_note"] = ("The masthead master serves the 282 px masthead. Print and other widths take the October master, "
                               "lockups/20261028_L3-Horizontal-Master.svg, until a print L3 at the masthead's proportion is drawn (CD-S10)")
            r["status_note"] = ("The masthead master has set the lockmark at 48 px since November 8, 2026 (DR-131). The October "
                                "master, with the lockmark at 2.4 cap heights, stays in lockups/ for the record")
        if r["lockup"] == "L6 editorial signature":
            r["below"] = "Close the page with the footer place: the lockmark at 24 px, then the tagline (Rule 08.2)"
            r["status_note"] = "Drawn without its four pillar dots since November 8, 2026 (DR-129)"
        if r["lockup"] == "L8 monogram":
            r["screen"] = r["screen"].replace("Never a favicon", "Never an avatar or a favicon")
            r["status_note"] = ("For squares where the name must show, such as a tile in a partner's directory. Social avatars "
                                "and the app icon show ampersand B alone on the Charcoal tile (DR-116)")
    d["condensed"] = CONDENSED_NOTE
    d["updated"] = ("November 8, 2026, Q1 to Q4 pass: the lockmark's 48 px master and ranges, the end mark's exception, "
                    "L3's masthead master and L6 without its dots. November 7, 2026, apply pass: S1 added, L2 retired, the "
                    "badge from 48 px, condensed figures kept for the record")
    MIN_FILE.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    return d


LOCK_OLD = ("lockmark/20261028_Lockmark-Master-V5.svg", "prussian/20261028_Lockmark-Master-V5-Prussian-White.svg")
LOCK_NEW = ("lockmark/20261107_Lockmark-Display-Master.svg", "prussian/20261107_Lockmark-Display-Master-Prussian-White.svg")
LOCK_TITLE = f"Lockmark, display master, for {LOCK_DISPLAY_FROM} px and up: the fifth edition's geometry, unchanged"
TREATMENT_D = ". Treatment D for Prussian: one color, White"

# ------------------------------------------------------------------------------------- the 48 px master (DR-131)
PROPOSAL = ROOT / "work/boards/phase-2/apply-pass/lockmark/20261107_Lockmark-48px-Proposal.svg"
M48_RANGE = "at 48 px" if LOCK_DISPLAY_FROM == 49 else f"for 48 to {LOCK_DISPLAY_FROM - 1} px"
M48_TITLE = (f"Lockmark, 48 px master on the pixel grid, {M48_RANGE}: the masthead and the sign-off. "
             "Centers at 4.5, 23.5 and 42.5 px, 7 px nodes, a 9 px lever, 1 px links")


def no_title(svg):
    return re.sub(r"<title>.*?</title>", "", svg, count=1, flags=re.S)


def prussian_hooks(svg):
    """Treatment D for a lockmark or L3 file: every color hook becomes White."""
    s = (svg.replace('fill="var(--link,#5D636D)"', f'fill="{WHITE}"').replace('fill="currentColor"', f'fill="{WHITE}"')
         .replace('fill="var(--lever,#E63946)"', f'fill="{WHITE}"').replace('fill="var(--amp,#E63946)"', f'fill="{WHITE}"'))
    s = re.sub(r"</title>", TREATMENT_D + "</title>", s, count=1)
    assert sorted(set(re.findall(r"#[0-9A-Fa-f]{6}", s))) == [WHITE] and "currentColor" not in s and "var(" not in s
    return s


def lockmark_48():
    """The proposal Dustin approved, as a master: a clean title, and every byte of the drawing unchanged."""
    src = PROPOSAL.read_text()
    dst = re.sub(r"<title>.*?</title>", f"<title>{esc(M48_TITLE)}</title>", src, count=1, flags=re.S)
    assert no_title(dst) == no_title(src), "the 48 px master's drawing differs from the approved proposal"
    assert "proposal" not in dst.lower() and "board" not in dst.lower() and "approval" not in dst.lower()
    master = ID / LOCK[48]
    master.write_text(dst)
    pw = ID / "prussian" / (master.stem + "-Prussian-White.svg")
    pw.write_text(prussian_hooks(dst))
    assert re.findall(r"<rect [^>]*>", pw.read_text()) == re.findall(r"<rect [^>]*>", dst), "the Prussian file's rects differ"
    return [str(master.relative_to(ROOT)), str(pw.relative_to(ROOT))]


# ---------------------------------------------------------------------------------- L3 at the masthead (DR-131)
L3_GAP, L3_LOCK = 13, 48                 # 13 px of space, 0.6 of the 22 px capitals rounded down; the lockmark at 48 px
L3_TITLE = ("L3 horizontal lockup, masthead master on the pixel grid: the wordmark's 24 px master (capitals 22 px), "
            "13 px of space and the lockmark's 48 px master, centered on the wordmark's box. 282 by 48 px, for the site "
            "and email masthead")


def _inner(svg):
    """Everything inside a master's root <svg>, title removed."""
    body = no_title(svg)
    return body[re.match(r"<svg\b[^>]*>", body).end():body.rindex("</svg>")]


def l3_masthead():
    """L3 as Rule 03.6 now sets it in the masthead, built from two masters with their drawings unchanged."""
    wm = (ID / WM[24]).read_text()
    lk = (ID / LOCK[48]).read_text()
    wvb = [float(v) for v in re.search(r'viewBox="([^"]+)"', wm).group(1).split()]
    assert wvb == [0, 0, 221, 24], wvb
    x, top = int(wvb[2]) + L3_GAP, int(wvb[3] / 2 - L3_LOCK / 2)
    W = x + L3_LOCK
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {top} {W} {L3_LOCK}"><title>{esc(L3_TITLE)}</title>{_inner(wm)}'
           f'<svg x="{x}" y="{top}" width="{L3_LOCK}" height="{L3_LOCK}" viewBox="0 0 48 48">{_inner(lk)}</svg></svg>')
    assert _inner(wm) in svg and _inner(lk) in svg and (x, top, W) == (234, -12, 282)
    master = ID / L3["masthead"]
    master.write_text(svg)
    pw = ID / "prussian" / (master.stem + "-Prussian-White.svg")
    pw.write_text(prussian_hooks(svg))
    return [str(master.relative_to(ROOT)), str(pw.relative_to(ROOT))]


def display_lockmark():
    """The display master under its new name: same drawing, clean title."""
    out = []
    for old, new in zip(LOCK_OLD, LOCK_NEW):
        src = (ID / old).read_text()
        tail = TREATMENT_D if "prussian/" in old else ""
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
    display_lockmark()
    report.append({"m48": lockmark_48(), "l3": l3_masthead()})
    update_minimums()
    return report


if __name__ == "__main__":
    rep = run()
    extra = rep.pop()
    for c in rep:
        print(f'S1 {c["size"]}: {c["contours"]} contours, {c["letters"]} letters matched ({" ".join(c["matched"])}), '
              f'B vs its master {c["b_vs_master"]:.1e}, B vs the wordmark\'s B {c["b_vs_wordmark"]:.1e}, '
              f'worst offset {c["worst_offset"]:.1e} units')
        for f in c["files"]:
            print("  wrote", f)
    print("updated", MIN_FILE.relative_to(ROOT))
    print("wrote", ", ".join(LOCK_NEW))
    print("wrote", ", ".join(extra["m48"] + extra["l3"]), "(48 px master byte for byte the approved drawing; L3 from two masters unchanged)")
