# Design director audit: identity geometry and symbols

Phase 0, October 20, 2026.

**Boards** (PNG beside each): `work/boards/phase-0/20261020_Identity-Small-Size-Diagnostic.html` and `work/boards/phase-0/20261020_Symbol-Pixel-Fit-And-Similarity-Diagnostic.html`. Numbers: `work/handoffs/phase-0/20261020_Design-Director-Measurements.json`. x is one wordmark cap height (100 units).

## 1. Identity at small sizes

**Construction.** The letters are stock Inter Tight 800 outlines tracked minus 2 percent, with the font's kerning on O to A and A to C (minus 3.8 percent) and A to T (minus 9.1 percent). The ampersand is the unmodified Lora Bold glyph: all 120 coordinate pairs match the font in V5, scaled by 0.14. V5 calls it "redrawn."

**Letterspacing**, as the nearest ink gap, then the area gap (white between neighbours across the cap band, depth capped at 0.2x):

| | OA | AT | TH | H& | &A | AC | CT | TI | IO | ON |
|---|---|---|---|---|---|---|---|---|---|---|
| Nearest | .108 | .156 | .053 | .101 | .083 | .108 | .089 | .053 | .074 | .074 |
| Area | .200 | .281 | .214 | .198 | .261 | .200 | .267 | .214 | .149 | .149 |

- V5 states a 0.10x hinge gap each side. The right gap measures 0.083x and reads 32 percent more open, because of the wedge above the A's diagonal. The ampersand leans toward OATH.
- I to O and O to N are the densest pairs. ACTION ends heavier than OATH begins.
- One master serves every size, so 16 px carries display tracking.
- The monogram balances. The stacked lockup hangs a 1.32x ampersand right of ACTION and reads OATH ACTION &.

**Ampersand weight.** It sits 0.0024x above the cap line and 0.022x below the baseline; V5 states 0.02x at both. Thick strokes are 0.67 to 0.78 of the 24.1-unit cap stems. Thin strokes (9.8 to 10.2 units) are 0.41 of the stems: contrast 1.9 to 1 against the letters' 1.22. The red glyph reads lighter than the words. Its hairlines measure 1.45 px at 16 px tall, 1.2 px at the L1 minimum, and reach 2 px at 22 px tall.

**Joins that clog** (1.0 means a full column of background shows). At 16 px, T to H opens only to 0.73 and T to I to 0.62; other pairs reach 0.89, and all reach 0.95 at 24 px. Inside the ampersand the upper loop's base fills to 0.66, the bowl's tip to 0.46 and the arm notch to 0.23, so the crossing becomes one dark mass.

**Red edge contrast.** At 16 px, 43 percent of the ampersand's pixels are solid and the median red pixel measures 2.47:1 on Newsprint, 3.17 on White, 3.10 on Charcoal and 2.43 on Prussian. At 24 px the median reaches the nominal ratio. On Newsprint no red pixel reaches 3:1 at any size.

**Clipped outlines.**
- `#amp`'s viewBox cuts 1.83 units off the loop and 1.72 off the tail, wherever V5 uses it: master figure, hinge, containers, watermarks, headlines, cover.
- `#tl-1`, `#tl-2a`, `#tl-2b` and `#url-1` lose 24 to 26 units of descender. L5 and L6 read "countrv," "peoole" and ".orq" (03-identity-01.jpg).
- `#stacked` clips 0.89 units of the ampersand's tail.

**The 16 px ampersand.** `#amp-16` is the master with a 0.73-unit stroke in a padded viewBox. At 16 px it adds 0.055 px per side, draws the glyph at 94 percent size and shows 7.6 percent less ink. V5 credits "a heavier contour, so the counter stays open"; a heavier contour would close counters. The 16 px container enlarges it to 70 percent of the circle (58 elsewhere), about 12 px tall, under V5's own 16 px minimum.

**Lockmark.** Links are 1 px non-scaling strokes.
- A node is 0.98 px at 16 px, the width of a link, and 1.48 px at 24. The lever at 16 px is one pink pixel.
- The middle link lands on a whole pixel at 16, 24 and 48 px and splits into two half-strength rows, so the cross reads grey inside a dark frame.
- `#lockmark-mono` keeps Stone links.

**Hinge diagram.** The arc keeps a fixed 1.25 px weight as the letters shrink. Labels reach a 13 px font size from 516 px wide; V5 sets no minimum.

**Stated minimums that conflict**
- L1's 120 px minimum is 13.35 px tall; "below 80 px the monogram replaces the wordmark" leaves 80 to 120 px undefined.
- L2 at 72 px has a smaller cap height (11.45 px) than L1. L8's 48 px minimum sits beside its favicon use.
- Red on Prussian "stays at display size or goes mono," yet the color matrix shows small red ampersands there (03-identity-03.jpg).
- Clear space allows "no type," yet taglines sit 0.39x (L5) and 0.79x (L6) below the baseline.

## 2. Pillar marks

- **Silhouette.** Explain is the generic "read" book. Connect is the interface "copy link" chain. Act's arrow points like `ui-external`. Track uses the Signal Grid's node-and-link grammar.
- **Family resemblance.** Four constructions: a stroked outline (7 and 5 units), a stroke with unequal dots, a solid fill, and a filled polygon with a ring. Corners mix round joins, sharp points and one 3-unit radius. Ink density at 96 px runs from 0.18 (Track) to 0.32 (Explain). Connect fills 64 percent of the field's height and the others about 85. Act's centroid sits 4 percent low.
- **Color.** Each mark has its own accent; red appears only in Act, whose arrow measures 2.96:1 on Newsprint without an edge, because V5 exempts "the lever."
- **Small sizes.** Crisp pixel share at 16 px runs from 0.30 to 0.57, and 0.38 to 0.54 for the simplified masters. Track and Act correlate at 0.81, both running from a node at bottom left to an accent at top right. Other pairs score 0.40 or less.

## 3. Topic icons

| Master | Strokes, px | Axis edges on whole pixels | Icons fully on grid | Circles on grid | Crisp share |
|---|---|---|---|---|---|
| 48 | 2.0 to 4.5 (7 widths) | n/a | n/a | n/a | 0.83 |
| 24 | 1.0 to 2.25 (6 widths) | 127 of 258 | 0 of 20 | 0 of 10 | 0.62 |
| 16 | 1.5, 1.8, 2.0 | 210 of 225 | 14 of 20 | 3 of 10 | 0.77 |

- **The 24 px set** is the 48 drawings halved, so odd coordinates land on half pixels. It is V5's most used size (131 of 216 uses), and the kicker shows it at 22 px (07-grid-02.jpg). The 16 px masters appear only in chapter 09.
- **Off-grid 16 px masters** come from 1.5 and 1.8 px strokes and one half-pixel rect.
- **Caps and joins** are round on all 59 stroked elements. Corner radii vary (0, 2 and 7 on rects; arcs of 4 to 18).
- **Stroke rule.** V5 states 3.5 to 4 main and 2.3 to 3 detail at 48; Local government uses 2.0 and Open primary 4.5.
- **Weight.** Ink density at 16 px runs from 0.26 (Testify) to 0.50 (Work and wages). Filled-only 16 px masters average 0.85 crisp share; stroked ones 0.68.
- **Accent.** One `--dot` element in each of the 60 masters; in four topics it switches between stroke and fill across sizes.

**Similarity** (rank among 190 pairs at 16 and 24 px, by silhouette overlap and blurred correlation): Ballot and Ranked ballot 12 and 19; Bill and Public records 19 and 27; Housing and Cost of living 24 and 116; Court and State house 104 and 31; Testify and Contact an official 116 and 168; Open primary against either ballot 130 or lower. The worst pairs sit outside this list. Campaign money and Contact an official overlap completely at 16 px, each a landscape box with a centre mark. Public records with Work and wages comes next, then Ranked ballot with Bill. Portrait sheets and landscape boxes are the groups to separate. Housing and Cost of living separate by eye despite their score.

**Utility glyphs.** Six live in the sprite (menu, close, search, arrow, download, external), 24-unit field, 2-unit stroke, used only in the icon library and the mobile specimen. At 16 px the menu glyph has no solid pixel. The four-dot pillar row has no master and appears at four pitches (01-purpose, 07-grid, 13-in-use, L6).

## 4. Graphic devices, layout and typography

- **Grid and rhythm.** Sections switch among 2- to 6-column grids, so no column line runs through a chapter. Rule-and-heading openings keep a steady rhythm worth protecting (03-identity-01.jpg).
- **Hierarchy.** Every heading from 24 to 110 px uses minus 4.5 percent tracking (06-type-00.jpg). That removes 24 percent of the word space, and the word spaces close up at H3 and H4 (08-pillar-marks-01.jpg, "In a name lockup.").
- **Measure.** Ledes run 82 to 86 characters against V5's stated 60 to 72 (03-identity-00.jpg, 04-ampersand-00.jpg). I found no single-word widows in headings.
- **Figures.** Three frame dialects: Stone boxes with two-part captions (03-identity-02.jpg), unframed rows (08-pillar-marks-00.jpg), and the strongest, atlas frames with a header strip (16-atlas-system-00.jpg).
- **Signal Grid.** The construction figure is clear (07-grid-00.jpg). Five encodings ride on nodes of 1 to 1.5 px at the sanctioned 16 to 24 px sizes (07-grid-01.jpg), and the 2 px progress ring is wider than its node. Report page 08 adds a sixth meaning, a count of steps.
- **Applications** have true ratios and dimension labels (13-in-use-00.jpg to -05.jpg). Their text renders at 6.4 to 8.9 px. Photographs are grey boxes (13-in-use-01.jpg); merchandise is flat silhouettes (13-in-use-04.jpg). The social tile cuts "budget" mid-word and spills its ampersand over the caption (09-topic-icons-02.jpg). The hinge motion ends with wider gaps than the wordmark (04-ampersand-03.jpg).
- **Report pages** share one kicker, heading and folio system. "Fit width" shows only the top two thirds of each page at 1440 by 1000. Dark pages show Newsprint edge strips (reports-1440/04.jpg, 12.jpg); the cover photograph is a flat block (01.jpg); topic icons stand in for actors (06.jpg).

## 5. Icon studies and references

| Study | Take | Avoid at small sizes | Section 11 role |
|---|---|---|---|
| 01 Y2K | Orbits, ring motion | Stripes and rays clog under 48 px | Confirm |
| 02 Flat Geo | Open-door Act, page panels | Slits fill at 16 px; Connect resembles a card logo | Confirm |
| 03 Isometric | Exploded layers | All icon use | Confirm |
| 04 Flat Square | Rounded tile | All-red Act tile; interior lists vanish at 32 px | Confirm |
| 05 Hand Drawn | Hands, human texture | Red and blue figures, dome, scales; hatching collapses | Revise minimum to 96 px |
| 06 Geometric | Filled silhouettes, circle and square, a linking node | Tricolor; Explain reads G or ©, Track a status light, Act D or a pie; gaps close at 16 px | Confirm as geometry source, red on Act only |
| 07 Abstract Geometric | Rhythm lines, dotted arcs, halftone | Moiré; clichés | Confirm |
| 08 Simple Line | Act's open door; one accent node | Track and Connect share one grammar that echoes the Signal Grid; Explain reads © | Revise |

**Revision to section 11.** The table calls V5's topic set a "24-unit, 2 px stroke family." That fits only the utility glyphs. The topic set is a 48-unit family of filled silhouettes, which render crisper at 16 px. So 08 suits a line companion from 24 px up, and Gate 1 chooses the topic grammar. The open door in 08 and 02 carries Act's "a way in" better than 06's quadrant.

**Data-viz principles:**
- Annotate the decisive moment in the plot (data-viz-03 #38).
- Title the finding, then give units and source (data-viz-02 #26, data-viz-04 #50).
- Label directly and sort (data-viz-03 #37).
- Explain scale and axis direction inside the chart (data-viz-02 #21, data-viz-04 #57).
- Show intervention strength as an ordinal ramp (data-viz-04 #62).
- Draw the boundary before the arrows (data-viz-04 #51).
- Use one accent on a quiet field (data-viz-05 #76).
- Avoid glowing 3D dashboards (data-viz-01 #01 to #03).

**Design-I-like principles:**
- One drawing in sanctioned treatments (design-i-like-02 #18).
- Causal loops with polarity, loop markers, delay marks and an adjacent legend (design-i-like-02 #25).
- Exploded layers with flat labels (design-i-like-02 #23).
- One orthogonal route with terminal nodes (design-i-like-03 #41).
- The register as interface (design-i-like-01 #16).
- Solid silhouettes with one offset accent (design-i-like-01 #12).

## 6. Facts Phase 1 needs

1. Wordmark field 970.71 by 108 units; cap band y 4 to 104; stems 24.1; bars 19.7.
2. Ampersand: Lora Bold at 0.14, `translate(365.5 104)`, ink 368.72 to 460.00 by 3.76 to 106.24. The rights lead should confirm the license position for a logo built from font outlines.
3. Hairlines reach 1.5 px at 16.5 px tall and 2 px at 22 px; the red turns mostly solid at 24 px. No working optical small ampersand exists.
4. Lockmark centres 11.75, 61.75, 111.75 on a 50-unit pitch: 6.48 px at 16, 9.72 px at 24. A 1 px link draws solid only on a half pixel.
5. Six symbols overflow their viewBoxes; re-export from ink bounds.
6. Topic field 48 units with a 4-unit margin; the 24 px set is halved; 1.5 and 1.8 px strokes cannot pixel-fit. Pillar marks sit in a 100-unit space scaled by 1.235.

## 7. Checked and not checked

**Checked.** Parsed the identity, lockup, pillar, topic and utility symbols; compared outlines with the V5 fonts; rendered and measured every cell in Chromium at device scale 1 on Linux. Viewed every chapter's 1440 tiles (03, 04 and 08 in full, the rest as composites), the twelve report pages, all reference sheets and the five Design-zip studies at full size. Capture artifacts (the repeated sticky navigation and skip tab) are excluded.

**Not checked.** Print and inch minimums. Windows, macOS and high-density rendering, so the pixel figures hold for Chromium on Linux only. The 390 px composites, and the V4.2 and Concepts V2 screens. The Atlas Visual System figures, which capture empty. Studies 04, 05 and 08 at full size. Reader tests: similarity and spacing come from models. Report reader keyboard behaviour.

## Change log

**Created:** this note; `work/handoffs/phase-0/20261020_Design-Director-Measurements.json`; both boards with PNGs in `work/boards/phase-0/`; in `work/build/scripts/phase-0/`: `oa_geom.py`, `identity_geometry.py`, `amp_vs_lora.py`, `wordmark_vs_inter_tight.py`, `identity_board.py`, `symbols_board.py`, `render_cells.js`, `screenshot_board.js`, `stitch_png.py`. **Modified:** none. `source/` and `work/extract/` are untouched.
