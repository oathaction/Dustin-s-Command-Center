# Stage B, round 1: identity designer's notes

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261109_Stage-B-Drawings-Brief.md`, "Identity designer". I read my role file, `CLAUDE.md`, the brief, DR-129 to DR-131, D2-465 to D2-478 and the decision log from "Stage B answers" to the end (DR-149 to DR-155 included; none of them touches my three items), the creative director's review of the Q1 to Q4 pass, my November 7 and 8 notes and the Q1 to Q4 figures.

I wrote new files only. No existing master, specimen, chapter file, board, ledger or other owner's file changed. Nothing is committed or pushed by me.

**To open:** `work/boards/phase-2/stage-b/drawings/identity/20261109_Identity-Plates.html`. Three plates, one per card, at true size on Newsprint, each labeled by card and option: `#card-end-mark`, `#card-lockmark`, `#card-l6`. Each plate is also rendered at 1x and 2x beside it (`20261109_Identity-<Card>-Plate-1x.png` and `-2x.png`).

**To rebuild:** `python3 work/build/scripts/phase-2/stage_b_identity_drawings.py` (about 40 seconds). It writes the masters, asserts each one, renders and measures everything in Chromium, runs the feed test and the engineer's pixel-fit check, and writes the plate page, its PNG files and `20261109_Identity-Figures.json`.

## What I made

### 1. The pixel-fit end mark (DR-142, D2-496)

Ampersand B drawn on whole pixels for the end mark: a 14 px master for 17 px body text and a 12 px master for 15 px text, the two sizes today's end mark reaches (14.1 and 12.5 px, from the Q1 to Q4 figures). Every pixel is full or empty, and each drawing is one path: its outline and its two counters. I drew them by hand from the 16 px master as it renders at 16 px and from the display master reduced to each size, keeping the loop with its counter tapering into the crossing, the diagonal, the bowl, the arm with its serif and the tail standing one pixel past the arm.

The real choice the pixels offer is the row B's bottom takes (D2-496's own example), so each size has two fits:

- **Fit A** keeps the master's overshoot. B's top row sits on the capitals' top row and its tail one row under the baseline, as today's end mark sits (DR-130). Set with `vertical-align: -1px`.
- **Fit B** sits B on the baseline, the way a typeface sits its round letters at text sizes. B's top row still sits on the capitals' top row, and B is one row shorter. Set with `vertical-align: 0`.

| Card, option | File | Size | Set | Ink |
|---|---|---|---|---|
| End mark, 14 px, Fit A | `work/build/assets/identity/ampersand/20261109_Amp-B-14px-End-Mark-Fit-A.svg` | 13 by 14 px | −1 px | 90 px |
| End mark, 14 px, Fit B | `work/build/assets/identity/ampersand/20261109_Amp-B-14px-End-Mark-Fit-B.svg` | 13 by 13 px | 0 | 83 px |
| End mark, 12 px, Fit A | `work/build/assets/identity/ampersand/20261109_Amp-B-12px-End-Mark-Fit-A.svg` | 11 by 12 px | −1 px | 66 px |
| End mark, 12 px, Fit B | `work/build/assets/identity/ampersand/20261109_Amp-B-12px-End-Mark-Fit-B.svg` | 11 by 11 px | 0 | 60 px |

Each has a Prussian White file in `work/build/assets/identity/prussian/`, named the same with `-Prussian-White` before `.svg`.

Measured in Chromium, in a line of Inter 400, beside a capital H of the same text, on Newsprint and on Charcoal:

| | Text | B tall | Top over the cap line | Under the baseline | B's rows at 1x, line at 4 positions between pixels | Ink pixels at full color, 1x |
|---|---|---|---|---|---|---|
| Today | 17 px | 14.1 px | 0.6 px | 1.1 px | 15 rows; top 0 to 1 rows over H's, tail 1 to 2 rows under, by where the line falls | 45 percent |
| Fit A, 14 px | 17 px | 14.0 px | 0.6 px | 1.0 px | 14 rows; top on H's top row, tail one row under, at all four | 100 percent |
| Fit B, 14 px | 17 px | 13.0 px | 0.6 px | 0 | 13 rows; top on H's top row, last row on H's last row, at all four | 100 percent |
| Today | 15 px | 12.5 px | 1.1 px | 0.5 px | 13 rows; top 0 to 1 rows over, tail 1 to 2 rows under | 38 percent |
| Fit A, 12 px | 15 px | 12.0 px | 0.1 px | 1.0 px | 12 rows; top on H's top row, tail one row under, at all four | 100 percent |
| Fit B, 12 px | 15 px | 11.0 px | 0.1 px | 0 | 11 rows; exactly H's rows, at all four | 100 percent |

The pixel fits also cure CD-N10: today's B moves a row up or down with the line's position, and every fit stays locked to the capitals' rows at all four positions. On a 2x screen the fits double into 2 px steps, where today's scaled master draws smoothly; the plate shows both, and question 2 is about it.

### 2. The lockmark masters rebuilt (DR-145)

The 24 and 48 px masters with each node and the lever as one outline, traced from the pixel rows today's files draw. The links stay as today's six rects, byte for byte. The script asserts that each outline fills exactly the pixels it replaces, and the renders match today's pixel for pixel at each master's own size, at 1x and 2x, on Newsprint, Charcoal and Prussian.

| Card, option | File | Prussian White file |
|---|---|---|
| Lockmark, 24 px, rebuilt | `work/build/assets/identity/lockmark/20261109_Lockmark-24px-Master-Outline.svg` (6 link rects, 9 paths; today's file has 53 rects) | `work/build/assets/identity/prussian/20261109_Lockmark-24px-Master-Outline-Prussian-White.svg` |
| Lockmark, 48 px, rebuilt | `work/build/assets/identity/lockmark/20261109_Lockmark-48px-Master-Outline.svg` (6 link rects, 9 paths; today's has 71 rects) | `work/build/assets/identity/prussian/20261109_Lockmark-48px-Master-Outline-Prussian-White.svg` |
| Lockmark, 16 px | No new file. Today's `lockmark/20261028_Lockmark-16px-Master.svg` already draws each node and the lever as one circle | Today's file in `prussian/` |

**The 16 px master needs no rebuild.** My November 8 question said the 16 and 24 px masters were both built from pixel rows. That was true of the 24 and 48 px masters only: the 16 px master draws circles, so it never parted into stripes. Measured from 16 to 23 px, its node and lever cores are whole at every size above 16 px, at 1x and 2x. At 16 px itself the core test reads 60 percent because each circle's edge pixels are about 95 percent covered, which is the circle's soft edge and not a stripe.

The plate sets today's files beside the rebuilt ones at 16, 24, 34, 40 and 48 px, each size from the master its range names. The share of a node's core and the lever's core drawn at full color (the range test of D2-465), on Newsprint:

| Size, master | Today 1x, node / lever | Rebuilt 1x | Today 2x, node / lever | Rebuilt 2x |
|---|---|---|---|---|
| 24 px, 24 px master | 100 / 100 percent | 100 / 100 | 100 / 100 | 100 / 100 |
| 34 px, 24 px master | 50 / 54 | 100 / 100 | 65 / 76 | 100 / 100 |
| 40 px, 24 px master | 57 / 67 | 100 / 100 | 78 / 85 | 100 / 100 |
| 47 px, 24 px master | 49 / 51 | 100 / 100 | 74 / 77 | 100 / 100 |
| 48 px, 48 px master | 100 / 100 | 100 / 100 | 100 / 100 | 100 / 100 |
| 49 px, 48 px master | 57 / 70 | 100 / 100 | 51 / 50 | 100 / 100 |
| 56 px, 48 px master | 32 / 35 | 100 / 100 | 78 / 71 | 100 / 100 |
| 72 px, 48 px master | 68 / 67 | 100 / 100 | 100 / 100 | 100 / 100 |

Between whole multiples the rebuilt edges still soften (ink at full color at 34 px rises from 37 to 60 percent at 1x, not to 100), but no node parts into stripes.

**The feed test (D2-468)** on the proofs' 1200 by 630 card, drawn standalone as `stage_a_identity_q_measure.feed_control` draws it, reduced with Lanczos:

| Sign-off | 500 px: nodes, red pixels | 360 px: nodes, red pixels |
|---|---|---|
| Today's 48 px master | 8 of 8, 11 | 8 of 8, 5 |
| Rebuilt 48 px master | 8 of 8, 11 | 8 of 8, 5 |

The rebuild does not change the 5 red pixels at 360 px, and it cannot: the card is a 1x image, and the rebuilt master draws the sign-off on it pixel for pixel as today's does (the lockmark's box plus 8 px compares equal byte for byte). The margin stays 5 against a floor of 4. Raising it would take a different change, such as a larger lever or a larger sign-off, which I have not drawn.

**The 48 px master on a 2x screen.** I looked at it at four times, beside today's and the display master. The rebuilt master draws the same stepped nodes as today's: each 7 px node doubles into a 14 px shape with 2 px steps, and the lever into an 18 px one. The rebuild leaves the creative director's risk where it was. I tried one second fit for it, circles with `shape-rendering="crispEdges"`, which would draw rounder nodes on a 2x screen. Chromium draws those circles lopsided (two 7 px rows at the top of each node and one at the bottom), so they do not give the same pixels at 1x: 4 pixels differ at 24 px and 39 at 48 px. That fails DR-145, so I left it out and give one proposal, as D2-496 expects.

### 3. L6 centered (one proposal, D2-496)

L6 as drawn today without its dots (DR-129), beside L6 with the wordmark and tagline moved down 14.72 units of L6's 1400 by 300 layout, 9.3 px at its 884 px minimum. The span from the wordmark's cap line to the tagline's baseline then has its middle on the strip's middle, where the lockmark's middle already sits (149.5 units against 150). The strip, the lockmark, the left margin and every size stay as they are. Measured on the 2x renders, from the flat tops of the capitals to the bottoms of the tagline's letters: the span's middle falls at 85.5 px today and 95.0 px centered, against the strip's middle at 94.7 px (the renders resolve half a pixel).

What it costs: today the wordmark's cap line meets the top of the lockmark's nodes (84.4 against 84.4 units). Centered, the cap line stands 14.7 units under the top nodes and the tagline's baseline 13.6 units over the bottom ones. Plate files only, in the board folder: `20261109_Identity-L6-Today-No-Dots-1x.png` and `-2x.png`, `20261109_Identity-L6-Centered-1x.png` and `-2x.png`. No L6 file or specimen changed.

## Routine calls

- D2-xxx | The end mark's pixel fits draw every pixel full or empty, as one path | DR-142 asks for crisp edges at 1x, and a curve would put soft pixels back; the pixel-fit check finds no soft pixel in any fit
- D2-xxx | The 14 px master serves 17 px text and the 12 px master 15 px text | Today's end mark is 14.1 px tall at 17 px and 12.5 px at 15 px (Q1 to Q4 figures)
- D2-xxx | The two fits at each size differ in where B's bottom falls and draw the same strokes: walls 2 px, with the bowl's left side 3 px at 14 px | D2-496 names the band's row as the real choice. The display master's walls reduce to 2.4 to 3.0 px at 14 px and 2.1 to 2.5 px at 12 px, and the 16 px master draws 2 and 3 px at 16 px; the next whole width down is 1 px, so weight gives no real choice at these sizes
- D2-xxx | In both fits B's top row sits on the capitals' top row | It keeps DR-130's band on the capitals: at 17 px text that row is the capitals' faint top row, and at 15 px their full top row
- D2-xxx | Fit B takes one row out of the diagonal at 14 px and out of the crossing at 12 px, and keeps the bottom two rows deep | Dropping only the overshoot row would leave B's bottom stroke one row thin
- D2-xxx | B is 13 px wide at 14 px and 11 px wide at 12 px | The masters' proportions give 12.3 to 12.7 and 10.5 to 10.9; the wider fit keeps the tail standing one pixel past the arm, as both masters draw it
- D2-xxx | Each end mark fit gets a Prussian White file in `prussian/` | B's other masters have one there (treatment D)
- D2-xxx | The script asserts that each B fit keeps exactly two counters | A first draft of Fit B at 14 px and Fit A at 12 px left a one-pixel hole under the arm's serif; both are redrawn
- D2-xxx | The rebuilt lockmarks keep the link rects byte for byte and trace only the nodes and the lever | DR-145 names the nodes and the lever; the links never parted, since they are single rects
- D2-xxx | No new 16 px lockmark file | Its nodes and lever are already one circle each, and it never parted into stripes (cores whole from 17 to 23 px)
- D2-xxx | No second fit for the 16 px lockmark | I drew square and plus-shaped nodes on whole pixels and looked at them: the squares read as a grid of squares and the plus shapes as crosses, where today's circles read as dots, and both change approved pixels
- D2-xxx | One proposal for the rebuilt lockmark, with no crisp-edged circle fit | Chromium draws crisp-edged circles lopsided, so they fail DR-145's same pixels at 1x
- D2-xxx | The feed test runs on the proofs' card drawn standalone, with today's master and the rebuilt one in turn | No master changes until Dustin answers, so the guide page still draws today's master; the standalone card reproduces the page's figures (11 and 5)
- D2-xxx | L6 centers the span from the wordmark's cap line to the tagline's baseline | Descenders hang below a line in type; counting them would move the group 12.6 units in place of 14.7, 1.4 px less at 884 px, so it gives no real choice
- D2-xxx | L6 centered moves only the wordmark and the tagline | DR-129 keeps L6's own proportion for the strip and the lockmark
- D2-xxx | The engineer's pixel-fit check runs on square copies of B's masters, padded on the right, in a scratch folder | The check sets every box square and would place B's 13 by 14 box half a pixel off
- D2-xxx | The end mark is measured with the line at four positions between pixels (0, 0.25, 0.5 and 0.75 px) | CD-N10 found today's B moves a pixel with the line's position, so a fit has to hold at each one
- D2-xxx | Enlarged views on the plates show 1x renders at eight times and 2x renders at four times, the same physical size; the lockmark's 1x views are at six times so five sizes fit one row | Each view says its magnification

## Questions for Dustin

1. **The end mark: Fit A or Fit B, at 14 px and at 12 px.** Fit A keeps today's proportion, with B's tail one pixel under the baseline. Fit B sits B on the baseline beside the letters, its top on the capitals' top row. *Recommendation:* Fit B at both sizes. B then stands exactly at the text's cap height, as DR-130 asks, and at 1x a whole pixel under the baseline reads as B dropping out of the line, where today the same dip was blurred.
2. **The end mark on a 2x screen.** The pixel fits double into 2 px steps there, while today's drawing renders smoothly. *Recommendation:* the page serves the pixel fit to 1x screens and keeps today's end mark on 2x screens, switched by screen resolution; the engineer would build the switch. On a 2x screen B then keeps today's 1 px dip.
3. **The rebuilt lockmark masters (DR-145).** One proposal: the 24 and 48 px files with each node and the lever as one outline, and today's 16 px file unchanged. *Recommendation:* approve. Nothing changes at 16, 24 or 48 px, and every size between keeps whole nodes, so L3 at its 196 px minimum (the 24 px master at 34 px) stops looking striped. The 2x steps and the feed margin of 5 red pixels stay as they are today.
4. **L6 centered.** *Recommendation:* approve. With the dots gone, the wordmark and tagline sit 9.3 px high on the strip; centered, they share the lockmark's middle and the strip reads balanced. The cost is that the wordmark's cap line no longer lines up with the lockmark's top nodes.

## For the main session and other owners

- **Board builder.** The card order in the brief puts the end mark, then the lockmark masters, then L6 centered. Each plate's options are labeled: "Today", "Fit A", "Fit B"; "Today", "Rebuilt"; "Today, without its dots", "Proposal: centered". What Dustin approves by name: one fit at 14 px and one at 12 px; the rebuilt 24 and 48 px lockmark files; L6 centered. Every figure on the plates comes from `20261109_Identity-Figures.json`.
- **Engineer.** Once Dustin approves, the end mark needs a switch by screen resolution if he takes question 2's recommendation. With whole nodes between 49 and 95 px, the 48 px master could serve that range too, which D2-465 ruled out only because of the stripes; ink at full color there is 52 to 71 percent at 1x, so that is a separate look, not part of this answer.
- **Creative director.** The naming test and the look-alike check are written for icons; I did not run them on these identity marks (see Not tested).
- **Main session.** No ledger entry is mine to write; the routine calls above carry D2-xxx for you to number.

## Tested

- Each outline drawn from pixels, by script: every B fit and every rebuilt node and lever fills exactly its pixels under the nonzero rule; each B fit keeps exactly two counters; each rebuilt node and lever is one closed outline; the rebuilt files keep today's link rects byte for byte; every Prussian White file holds only `#FFFFFF`.
- The rebuilt lockmarks against today's, rendered in Chromium at 24 and 48 px, at 1x and 2x, on Newsprint, Charcoal and Prussian: identical pixel for pixel in all twelve cases.
- The range test (node and lever cores at full color, crisp share, ink, near black, red) for today's 16 px master at 16, 17, 18, 20 and 23 px, today's and the rebuilt 24 px masters at 24, 34, 40 and 47 px, and today's and the rebuilt 48 px masters at 48, 49, 56, 72 and 96 px, at 1x and 2x.
- The feed test at 500 and 360 px on the standalone card with each 48 px master: 8 of 8 nodes and 11 and 5 red pixels for both, and the sign-off's box equal byte for byte.
- The end mark in a line of Inter 400 beside a capital H at 17 and 15 px, on Newsprint and Charcoal: geometry at eight times, and rows and full-color share at 1x and 2x with the line at four positions between pixels, for today's end mark and all four fits.
- The engineer's pixel-fit check (`python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py --size N`) on all four B fits (at 14, 13, 12 and 11 px), both rebuilt lockmarks (24 and 48 px), and today's 16, 24 and 48 px masters for comparison: every file passes at 1x and 2x. The B fits and the rebuilt lockmarks have no soft pixel, and every counter stays open; today's 16 px master has 46 percent soft pixels at 1x and passes.
- Crisp-edged circles at 24 and 48 px against today's masters (4 and 39 pixels differ), and square and plus-shaped 16 px nodes, both in a scratch folder.
- L6: the span's middle measured on the 2x render of each strip (85.5 px today, 95.0 px centered, against the strip's middle at 94.7 px).
- Looks, in Chromium at 1x and 2x, enlarged: the four B fits as grids and in their lines beside today's at near true size; each enlarged end mark crop; the lockmark plate (the stripes at 34 and 40 px today and none rebuilt, the 2x comparison, Charcoal and Prussian, the feed crops); both L6 strips at 2x. These looks led to fixes: a heavy first draft of B, the one-pixel holes under the arm's serif, a wrong first transcription of the 16 px master's rows, tall empty crops around the end marks, misaligned feed captions, and a whole-card pixel comparison that caught text rendering differences in the headline instead of the sign-off.
- A scan of the plate page's words: no em or en dash.

## Not tested

- Firefox, Safari and real devices. A 2x screen was simulated with Chromium's device scale factor of 2; Windows text rendering and font hinting were not tried, and the text's baseline may land differently there.
- The fits in the built guide page: no chapter or specimen changed, so the end mark was measured on my plate and measurement pages only.
- The end mark at text sizes other than 15 and 17 px, and at line heights other than the body token's and 28 px.
- A real feed upload and JPEG compression; print.
- The naming test and the look-alike check. Both are written for icons; B and the lockmark are identity marks with approved forms, and a 12 px end mark has no meaning at 48 px without its line of text.
- Readers. The combined reader check (DR-143) asks about the end mark and the 24 px lockmark after Dustin answers this board.
- The editor's copy edit of the plate words, which comes before the creative director scores the board (D2-500).

## Change log

Created:
- `work/build/scripts/phase-2/stage_b_identity_drawings.py`
- `work/build/assets/identity/ampersand/20261109_Amp-B-14px-End-Mark-Fit-A.svg`, `20261109_Amp-B-14px-End-Mark-Fit-B.svg`, `20261109_Amp-B-12px-End-Mark-Fit-A.svg`, `20261109_Amp-B-12px-End-Mark-Fit-B.svg`
- `work/build/assets/identity/lockmark/20261109_Lockmark-24px-Master-Outline.svg`, `20261109_Lockmark-48px-Master-Outline.svg`
- `work/build/assets/identity/prussian/`: the six files above with `-Prussian-White` before `.svg`
- `work/boards/phase-2/stage-b/drawings/identity/`: `20261109_Identity-Plates.html`, `20261109_Identity-Figures.json`, three plate renders at 1x and 2x (`End-Mark`, `Lockmark-Masters`, `L6-Centered`), the L6 strips at 1x and 2x (`L6-Today-No-Dots`, `L6-Centered`), and the enlarged views the plates show (12 end mark crops, 13 lockmark crops, 4 feed crops), every name starting `20261109_Identity-`
- `work/handoffs/phase-2/20261109_Stage-B-Identity-Notes.md` (this file)

Modified: none. Today's masters, specimens, chapters, boards and ledgers are unchanged. The main session's snapshot commits took in-progress copies of some of the files above; the files on disk are the finished ones.
