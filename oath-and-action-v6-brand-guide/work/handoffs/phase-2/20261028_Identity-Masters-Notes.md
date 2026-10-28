# Identity masters notes

Phase 2, step 1, October 28, 2026. oa-design-director, run as a subagent of the main session. It applies the identity refinements Dustin approved at Gate 1 (G1-01, G1-02) as masters. V5's masters in `work/extract/` are untouched and stay as the record. I wrote to no ledger: the change-ledger rows and decisions below are for the main session to merge.

**Board to open:** `work/boards/20261028_Identity-Masters-Board.html`. It needs `board-base.css` beside it and its images in `work/boards/phase-2/identity/`.

**Masters:** `work/build/assets/identity/`, 59 SVG files and one JSON table, in nine folders by mark.

**Numbers:** `20261028_Identity-Masters-Measurements.json` and `20261028_Ampersand-B-Similarity.json` beside this note. In the text, x is one cap height of the wordmark, 100 units. B's own drawing uses font units: cap height 700, so 7 font units make 1 wordmark unit.

## B's refinement result

B passes all four tests Gate 1 set for it, so option A stays the unused fallback and I did not prepare it.

| Test | Target | Result |
|---|---|---|
| Stroke contrast | From about 1.5 to 1 toward 1.7 to 1 | 1.74 to 1, thickest over thinnest station (first drawing 1.51 by the same stations); 1.66 to 1 as means (first drawing 1.42) |
| Crossing on the hinge diagram's center line | The waist crossing on the line through the four nodes | 0.1 diagram units off the line (first drawing: 39.1 font units above the glyph's ink center, about 6.8 diagram units) |
| Refined at twice size | Clean curves and nodes at 2x | Redrawn by hand as cubic contours, 27 nodes against 41, nodes on extrema; the 2x drawing with nodes, handles and stations is on the board |
| Print proof | A PDF at real print sizes | `work/boards/phase-2/identity/04-amp-b/20261028_Ampersand-B-Print-Proof.pdf`, 5 pages, US Letter. Scale checked on a 300 dpi render: the 100 mm bar measures 99.99 mm and the 50 mm ampersand 49.95 mm. **It was not printed on paper.** |
| Silhouette against installed serif ampersands | Recognizable and distinct | Pass. Overlap with Lora Bold 0.734 (rule: 0.70 or more). Nearest other face Liberation Mono Bold at 0.686, under the 0.698 line (the median Regular-to-Bold overlap of the eight installed serif families). 33 faces checked |

The silhouette margin is narrow: 0.012 to Liberation Mono Bold and 0.013 to Courier 10 Pitch Bold, both typewriter slabs that resemble B in mass. The Phase 1 drawing would have failed this rule at 0.713 against Courier 10 Pitch Bold, so the refinement moved B away from its nearest neighbors.

## Each master, its measurements and its checks

Crisp share is D1-17's pixel-fit measure: ink pixels at 90 percent coverage or more over ink pixels at 10 percent or more, one color on Newsprint, Chromium at device scale 1. A master passes at 0.60.

### I1. Re-exported outlines, `reexport/`

Six V5 symbols with viewBoxes widened to their full ink, outlines and origins unchanged: `#amp` (now `20261028_Amp-V5-Lora-Master-Reexported.svg`), `#tl-1`, `#tl-2a`, `#tl-2b`, `#url-1` and `#stacked`. The taglines and the web address are live masters for L4, L5 and L6. The Lora ampersand and the V5 stacked lockup stay as the record and the base for option A.

Checks: silhouette pass (open counters match V5 on every symbol); pixel fit not applicable; consistency, overshoot, one color (0.9 RGB units at most off the ink line) and red discipline pass; contrast fails only for red on Newsprint (2.96:1, logotype).

### I2. Hinge gaps by equal white area (2b)

Applied in every wordmark and L8 master. With B, both sides of the ampersand hold 0.203x of white; nearest ink 0.093x on the left and 0.070x on the right, at the floor. The V5 glyph with 2b, the Phase 1 record, also measured 0.205x on each side.

### I4. Ampersand B, `ampersand/`

| File | Use | Measures |
|---|---|---|
| `20261028_Amp-B-Display-Master.svg` | From 48 px, and in every display lockup | Bowl stem 153.9 font units (0.913 of the wordmark stem); diagonal 144.8; loop sides 123.4 and 124.0; waist upstroke 86.4; hairlines: loop top 88.5, bowl bottom 89.5, arm 91.6. Overshoot 9.4 font units top and bottom, 1.34 wordmark units, as the O. Beak 54 font units clear of the loop |
| `20261028_Amp-B-24px-Master.svg` | 24 to 47 px | 21 by 24 px; hairlines 3 px, bowl stem 5 px; crisp 0.743 |
| `20261028_Amp-B-16px-Master.svg` | 16 to 23 px, favicons | 14 by 16 px; hairlines 2 px, bowl stem 3 px; crisp 0.662 (V5's stroked 16 px drawing: 0.478); 2 open counters (V5: 3, its notch closes) |
| `20261028_Amp-B-Narrow-Display-Master.svg` | The condensed wordmark | Redrawn from the refined points: 0.85 width with stems at their regular weight; 1.72 to 1 |
| `20261028_Amp-B-Narrow-24px-Master.svg` | Condensed 24 px master | 18 by 24 px; crisp 0.747 |
| `20261028_Amp-B-Narrow-16px-Master.svg` | Condensed 16 px master | 12 by 16 px; crisp 0.622; no beak at this size |

Checks: silhouette, pixel fit, consistent weights, overshoot, one color (0.8) and red discipline pass. Similarity passes with the narrow margin above. Contrast fails only for red on Newsprint: the 16 px master reaches the nominal 2.96:1 (V5's 16 px drawing 2.49), 4.17 on White, 4.45 on Charcoal, White on Prussian 13.28.

### I3. Wordmark masters, `wordmark/`

Display (978.31 units wide), 24 px (221 px wide, 22 px capitals, 5 px stems) and 16 px (152 px wide, 14 px capitals, 3 px stems), each carrying B's matching master at full box height. Crisp 0.691 at 16 px and 0.770 at 24 px (V5 0.556 and 0.742). Six open counters at 16 px, as V5. Nearest ink between neighbors at 16 px is 2.06 px or more; T to H 3.05 px, T to I 2.99 px.

All nine checks pass except red on Newsprint (logotype); similarity not applicable.

### I5. The condensed drawing pass, `wordmark-condensed/` and `lockups/`

O, C, A and N are redrawn at weight; T, H and I keep Phase 1's narrowing. Width over ink height 7.50 to 1 (770.07 units). Hinge 0.181x on each side. 24 px master 181 px wide, 16 px master 120 px wide, crisp 0.768 and 0.860 (Phase 1 condensed 0.749 and 0.839), six open counters at 16 px against Phase 1's eight.

- O: straight sides between quarter arcs, sides 22.6, top and bottom 19, counter 28.8 units wide.
- C: cut from the O, terminals at y 40 and 68, aperture 28 units (4 px at 16 px).
- A: flat apex 26, legs 21.5 at 74.4 degrees, bar 16.5 at y 69; counter 31.7 tall and 17.7 wide at the bar. The bar is 2 px at 16 px and 3 px at 24 px.
- N: stems 22, diagonal 18.5 (0.84 of the stem) at 64.1 degrees, notch tips blunted 0.8 units.

**Main lockups:** L1 wordmark, L2 stacked, L3 horizontal with the lockmark, L8 monogram. V5's color matrix names L1, L2 and L8 as its primary lockups, and L3 is the site and email masthead. Each is drawn at both widths: L2 638.32 and 514.10 units, L3 1278.31 and 1070.07, L8 299.67 and 246.15.

Checks pass except two. Similarity stays open: heavy condensed capitals are common on campaign signs. And in the condensed L8 the narrow O reads close to a zero, 0&A. Red on Newsprint fails as everywhere (logotype).

### I6. Hinge diagram V2, `hinge/`

Display and compact masters at today's width and condensed. The words are the display wordmark masters' own letters and spacing; B sits at 1.25 cap heights, centered on its ink, its waist crossing 0.1 units from the center line. Minimum widths: display 533 px (labels at 13 px) and compact 245 px (lines at 1 px); condensed 463 and 213 px. Lines 3.5 units and arcs 2.8 on the display master, 6 on the compact. Solid arcs only.

Checks pass. Silhouette and pixel fit are not applicable (no small master). Contrast passes for the Stone lines (4.29:1 on Newsprint, 6.05:1 on White by token) and fails for red on Newsprint.

### I7. Lockmark, `lockmark/`

16 px master as Phase 1 drew it (crisp 0.605). The 24 px master now draws its nodes and lever as whole-pixel discs: Phase 1's vector discs measured 0.599, under D1-17's 0.60; the new master measures 1.00. V5's master, geometry unchanged, serves from 48 px (`20261028_Lockmark-Master-V5.svg`). V5 measured 0.51 and 0.05.

### I8. One minimum-size rule, `20261028_Identity-Minimum-Sizes.json`

The rule: "On screen, no identity mark draws its capitals under 14 px, and no tagline inside a lockup sets under 13 px. In print, no capitals under 3 mm and no tagline under 7 pt. Each lockup names its replacement below its minimum. Favicons use the ampersand's 16 px master."

| Lockup | V5 minimum | Screen minimum | Print minimum | Below the minimum |
|---|---|---|---|---|
| L1 wordmark | 120 px wide (13.4 px tall, cap 12.4 px) | 16 px tall: 16 px master from 16 to 19 px tall (152 px wide; condensed 120 px), 24 px master from 20 to 39 px, display master from 40 px | 1.20 in wide (condensed 0.95 in) | Use L8; below 48 px wide, the ampersand's 16 px master |
| L2 stacked | 72 px wide (cap 11.5 px) | 90 px wide (condensed 72 px), capitals 14 px | 0.80 in wide (condensed 0.65 in) | Use L8 |
| L3 horizontal with lockmark | 192 px wide | 196 px wide (condensed 164 px): wordmark 16 px master, lockmark 34 px from its 24 px master | 1.55 in wide (condensed 1.30 in) | Use L1 |
| L4 monogram and tagline | 144 px wide (tagline cap 4.5 px) | 304 px wide (tagline at 13 px) | 2.30 in (tagline at 7 pt) | Use L8 and set the tagline as live text |
| L5 wordmark and tagline | 240 px wide (tagline cap 5.9 px) | 388 px wide (tagline at 13 px) | 2.90 in (tagline at 7 pt) | Use L1 and set the tagline as live text |
| L6 editorial signature | 288 px wide (tagline cap 3.1 px) | 884 px wide (tagline at 13 px) | 6.60 in (tagline at 7 pt) | Use L3 with the tagline as live text |
| L7 section masthead | 168 px wide | 250 px wide (pillar word at 13 px), from V5's layout | 1.90 in (pillar word at 7 pt) | Use L1 and name the pillar in live text |
| L8 monogram | 48 px wide, also listed for favicons | 48 px wide (capitals 16.0 px; condensed 19.5 px). Never a favicon | 0.50 in wide | Use the ampersand's 16 px master |
| Ampersand B, freestanding | 16 px with V5's stroked optical drawing | 16 px master from 16 to 23 px tall; 24 px master from 24 to 47 px; display master from 48 px | 0.25 in tall | Nothing smaller. Favicon: the 16 px master at 16 px |
| Lockmark | 16 px, one color | 16 px master from 16 to 23 px; 24 px master from 24 to 47 px; V5 master from 48 px | 0.25 in | Nothing smaller; the lever stays one size up at 16 and 24 px |
| Hinge diagram V2 | None set | Display master from 533 px wide (labels at 13 px; condensed 463 px); compact master from 245 px (lines 1 px; condensed 213 px) | 4.00 in wide (labels at 7 pt) | Use a hinge headline |
| Hinge-circle badge | New mark (S9) | 16 px master from 16 to 23 px; 24 px master from 24 to 47 px; display master from 48 px | 0.25 in | Nothing smaller. Never an avatar or favicon |

L4 to L7 are not redrawn in this pass; their rows come from V5's layouts with the re-exported taglines and the Phase 2 wordmark width. At each minimum the Phase 2 L1 keeps 6 enclosed counters and the ampersand 2; V5's L1 and ampersand close a notch there (7 and 3).

### I9. Treatment D on Prussian, `prussian/`

25 explicit-color White files, one per mark and size. A scan of each file finds one color, #FFFFFF. Every render on Prussian has 0 red pixels and stays within 1.2 RGB units of the ink line; White measures 13.28:1. Rule 05.3 is quoted on the board word for word as D2-01 sets it.

### S9. The hinge-circle badge, `badge/`

| Condition | Status |
|---|---|
| Rule 05.3 names it as signature red | Met by D2-01 |
| It keeps to its jobs: an end mark, a report's back cover and events; never an avatar or favicon, never near a candidate or a ballot, never beside the wordmark or the hinge diagram, no words or dates | Written on the board for the identity chapter to carry |
| Its 16 px master is redrawn from B's 16 px master | Met: B's 16 px master area-sampled onto the 10 by 10 px inner field, then corrected by hand. The crossing sits on the badge's center line, the loop keeps a three-row counter, and the ink's center of mass sits 0.05 px from center across and 0.50 px below |

24 px master: B's 16 px master in a 1 px ring (crisp 0.774). Display master: B's display drawing in the V2 ring, ring 4.6 units. 16 px crisp 1.00, 3 enclosed regions in both polarities. Similarity to a seal stays open: Phase 1 measured 0.584 at 16 px and 0.608 at 24 px, and no reader has tested it.

## Craft checks on the board

Every item on the board carries the nine checks, with the result and what I measured. Totals across the ten items:

- **Pass:** silhouette, pixel fit for every 16 and 24 px master, consistent weights, overshoot, one color per surface, red follows Rule 05.3, and contrast for ink and for White on Prussian.
- **Fail, inherited:** Pillar Red on Newsprint at 2.96:1 at best, wherever red appears. WCAG exempts logotypes.
- **Open:** condensed capitals resemble campaign-sign lettering; the condensed L8 reads as 0&A; the badge's resemblance to a seal is untested with readers.

## Decisions I made

One line each, with the reason. For the main session to merge into the decision log as D2 rows.

| Decision | Reason |
|---|---|
| Read "its crossing" as B's waist crossing, between loop and bowl | It is the pen path's pivot near mid-height; the arm crossing sits at 0.19 of the cap height, and lifting it to the center line would need a new skeleton |
| Set the waist crossing at the glyph's vertical ink center, y 350 | The hinge diagram centers B on its ink, so the ink center is its center line; in the wordmark the same point is the cap band's middle |
| Measure contrast as thickest over thinnest station chord, and report means beside it | The same stations reproduce Phase 1's "about 1.5 to 1" (1.51), so before and after share one method |
| Raise B's thick strokes to 0.91 of the wordmark stem and lower its hairlines to 88.5 to 91.6 font units | Raises contrast while keeping the glyph's color beside the capitals; D1-14's 0.85 floor holds |
| Set B's overshoot to 9.4 font units top and bottom | Matches the wordmark O's 1.34 units |
| Narrow B's loop 13 units and extend its bowl 8 units left | The lower crossing made the loop taller and the glyph top-heavy at 16 and 24 px |
| Lower the serif 7 units and shorten the beak 4 | Keeps 54 units of white between the beak and the larger loop |
| Draw a 24 px master of B on the pixel grid | Phase 1 scaled the display drawing at 24 px; pixel fit under D1-17 needs its own drawing |
| Redraw the narrow B from the refined points instead of scaling it | Scaling and restoring stems closed the upper counter to a slot |
| Drop the beak from the narrow 16 px master | At 12 px wide the beak closed the notch under the arm, making a third enclosed counter |
| Set the silhouette pass rules before the run: 0.70 or more against Lora Bold; below the median Regular-to-Bold overlap of the installed families | A weight variant is the closest pair that still counts as one design |
| Count Courier 10 Pitch, FreeMono and Liberation Mono as serif ampersands | They are slab-serif designs installed on this machine |
| Build the print proof as true-size HTML printed to PDF by Chromium, and check its scale on a 300 dpi render | The only print-size proof this session can make; it was not printed on paper |
| Redraw the condensed O along with the C, N and A | The C is cut from the O, and two curve structures in one word would show |
| Keep Phase 1's narrowing for the condensed T, H and I | Straight stems survive a scale with their weight restored |
| Hold the condensed A's bar at 2 px at 16 px and 3 px at 24 px | Keeps the A's counter open at small sizes |
| Count L1, L2, L3 and L8 as the main lockups | V5's color matrix names L1, L2 and L8 as primary; L3 is the site and email masthead |
| Use the narrow B in condensed lockups and the regular B in the hinge diagram's ring at both widths | The ring sets the ampersand's space; the narrow drawing exists to fit the wordmark's line |
| Set L8's hinge white equal to the wordmark's (0.203x; condensed 0.181x) | One hinge across the lockups |
| Keep V5's L2 construction: its leading, 10 units of clear space to the N, the ampersand at 1.283 times, centered on the stack's middle | V5's drawing; B's waist crossing then lands between the two lines |
| Build the hinge diagram's words from the display wordmark masters | The diagram and the wordmark share one drawing and one spacing |
| Draw the 24 px lockmark's nodes and lever as whole-pixel discs | Phase 1's vector discs measured 0.599 crisp, under D1-17 |
| Shift the badge's 16 px ampersand 1 px right and end its tail at column 11 | Centers its ink within 0.05 px and keeps it clear of the ring |
| Write treatment D as separate explicit-White SVGs in `prussian/` | A producer can place them on Prussian without CSS |
| Write the print floors into the I8 rule: capitals 3 mm, taglines 7 pt | Phase 1's print floors; L1's print minimum becomes 1.20 in |
| Keep masters on currentColor with the --amp, --lever, --link and --line hooks | One file serves every surface; explicit color only where a surface demands it |
| Draw the board's construction annotations in Charcoal and White | Keeps red off Prussian on the board |
| Recommend today's width at Gate 2, and L8 at today's width if Dustin picks the condensed | The condensed drawing passes the craft checks but gains only height, sits near campaign lettering, and its monogram reads as 0&A |

## Change-ledger rows

One row per applied refinement, for the main session to number and merge into `work/ledger/20261020_Change-Ledger.md`.

| # | Date | Area | Change | Reason | Approved at |
|---|---|---|---|---|---|
| (next) | 2026-10-28 | Identity: six V5 symbols | I1 applied: `#amp`, `#tl-1`, `#tl-2a`, `#tl-2b`, `#url-1` and `#stacked` re-exported with viewBoxes that hold their full ink, outlines unchanged, in `work/build/assets/identity/reexport/` | V5 clipped their ink (defect) | Gate 1, G1-02 |
| (next) | 2026-10-28 | Identity: wordmark hinge | I2 applied: the ampersand's gaps set by equal white area (0.203x on each side, 0.07x floor) in every wordmark and L8 master | V5's right gap held 1.24 times the left's white (defect) | Gate 1, G1-02 |
| (next) | 2026-10-28 | Identity: ampersand | I4 applied: ampersand B refined (contrast 1.74 to 1, waist crossing on the center line, overshoot 1.34 units, 27 nodes) with display, 24 px and 16 px masters and a narrow drawing with its own 24 and 16 px masters, in `ampersand/`. B passed its print-scale and silhouette checks, so A was not prepared | B is the approved direction | Gate 1, G1-01 (B as refined to be confirmed at Gate 2) |
| (next) | 2026-10-28 | Identity: wordmark | I3 applied: display, 24 px and 16 px wordmark masters carrying B, in `wordmark/` | V5 scaled one master down and its small sizes blurred | Gate 1, G1-02 |
| (next) | 2026-10-28 | Identity: condensed width | I5 applied: the condensed drawing pass at 7.5 to 1 (O, C, A and N redrawn), display, 24 and 16 px masters in `wordmark-condensed/`, and L2, L3 and L8 at both widths in `lockups/`. Today's width stays in force | Dustin chooses the width at Gate 2 | Gate 1, G1-01 |
| (next) | 2026-10-28 | Identity: hinge diagram | I6 applied: hinge diagram V2 display and compact masters with B, at both widths, in `hinge/` | Solid arcs keep the diagram apart from V7's evidence lines | Gate 1, G1-01 |
| (next) | 2026-10-28 | Identity: lockmark | I7 applied: 16 and 24 px lockmark masters (24 px nodes as whole-pixel discs) and V5's master from 48 px, in `lockmark/` | At 24 px V5's lockmark had 5 percent solid ink (defect) | Gate 1, G1-02 |
| (next) | 2026-10-28 | Identity: minimum sizes | I8 applied: one minimum-size rule and its table for every mark, in `20261028_Identity-Minimum-Sizes.json` | V5's minimums conflicted (defect) | Gate 1, G1-02 |
| (next) | 2026-10-28 | Identity: Prussian | I9 applied: treatment D, every identity mark one color White on Prussian, 25 files in `prussian/` | Rule 05.3: red never sits on Prussian | Gate 1, G1-01 |
| (next) | 2026-10-28 | Identity: badge | S9 applied: hinge-circle badge masters at 16 px (redrawn from B's 16 px master), 24 px and display, in `badge/`, with its three conditions | A wordless end mark | Gate 1, G1-02 |

## Tested

- Every board cell rendered in Chromium (Playwright's build at `/opt/pw-browsers/chromium`) on Linux at device scale 1, from the masters.
- B's stroke widths as chords on the outline at eight stations, for the refined, first and narrow drawings; its crossings from its corners; overshoot and ink boxes from the curves.
- Crisp share at 16 and 24 px, open counters at 16 px and at each minimum, one-color purity on all four surfaces, ink and red contrast, and red pixels on Prussian, from the renders.
- B's silhouette against 33 ampersands: every style of Bitstream Charter, Caladea, Courier 10 Pitch, DejaVu Serif, FreeMono, FreeSerif, Liberation Mono and Liberation Serif, and the three Lora files extracted from V5.
- The print proof's page count and size (5 pages, 612 by 792 pt) with pdfinfo, its scale on a 300 dpi render, and the 3 mm ampersand's counters by eye at 300 dpi.
- Every treatment D file scanned for any color but White.
- The board at 1440 and 390 px, panels closed and open: no horizontal page scroll, all 2,390 images load, no text under 13 px, no skipped heading levels. Pixel audit: 1,902 Pillar Red pixels sit within 3 px of Prussian at 1440 px, all in the two labeled V5 cells; with those hidden, 0 at both widths. Results in `work/boards/phase-2/identity/20261028_Identity-Masters-Board-Check.json`.
- I looked at the board renders at both widths and at every master at 2x or 4x, and fixed what looked wrong: side-by-side display figures, tables that squeezed at 390 px, code labels at 11.9 px, two wide specimen rows, a closed notch in the narrow 16 px master, and a 24 px lockmark at 0.599 crisp.

## Not tested

- Paper: the print proof has not been printed, so press gain, paper color and ink density are untested.
- Windows, macOS, Firefox, Safari and high-density screens. Pixel fit holds for 1x Chromium on Linux.
- Commercial serif ampersands: none are installed here.
- Readers: the similarity limit, the pixel-fit limit and every optical judgment are studio thresholds that no reader has checked (Q-13). The badge's resemblance to a seal is untested.
- Trademark clearance of B and the badge (Q-12).
- Screen readers on the board.
- L4 to L7 rebuilt with B: their minimum sizes come from V5's layouts.

## Change log

**Created**

- `work/build/assets/identity/` (new): `20261028_Identity-Minimum-Sizes.json`; `ampersand/` 6 SVG; `wordmark/` 3; `wordmark-condensed/` 3; `lockups/` 6; `hinge/` 4; `lockmark/` 3; `badge/` 3; `reexport/` 6; `prussian/` 25.
- `work/boards/20261028_Identity-Masters-Board.html`.
- `work/boards/phase-2/identity/`: `20261028_Identity-Masters-Board-Check.json`; `04-amp-b/20261028_Ampersand-B-Print-Proof.pdf`, five `proof-page-*.png` previews and `similarity/` (34 contact-sheet PNGs: B and the 33 faces); the rendered cells in `i1/` to `i9/` and `s9/`.
- `work/handoffs/phase-2/20261028_Identity-Masters-Notes.md` (this file), `20261028_Identity-Masters-Measurements.json`, `20261028_Ampersand-B-Similarity.json`.
- `work/build/scripts/phase-2/`: `oa_p2.py`, `p2_amp_b.py`, `p2_amp_similarity.py`, `p2_reexport.py`, `p2_wordmark.py`, `p2_condensed.py`, `p2_marks.py`, `p2_lockups.py`, `p2_prussian.py`, `p2_minsizes.py`, `p2_print_proof.py`, `p2_print_pdf.js`, `p2_pairs.py`, `p2_render.py`, `p2_board.py`, `p2_check_board.js`, `p2_red_audit.py`.

**Modified:** none. `source/`, `work/extract/`, the ledgers, `board-base.css` and the Phase 1 scripts and boards are untouched; Phase 2 scripts import the Phase 1 modules and write only to Phase 2 paths.

**Rebuild order** (each with `python3 -I` from `work/build/scripts/phase-2/`): `p2_amp_b.py`, `p2_amp_similarity.py`, `p2_reexport.py`, `p2_wordmark.py`, `p2_condensed.py`, `p2_marks.py`, `p2_lockups.py`, `p2_prussian.py`, `p2_minsizes.py`, `p2_print_proof.py`, `p2_render.py`, `p2_board.py`; then `node p2_check_board.js <board> <dir>`, again with `HIDE_SPECIMENS=1`, and `p2_red_audit.py <dir> <dir>`.
