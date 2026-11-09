# Stage B, round 0: engineer's notes

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261109_Stage-B-Brief.md` ("Engineer") and the main session's task. I read my role file and the Master Brief sections it names, `CLAUDE.md`, the final stage B brief, the drawings brief, the decision log from "Stage B answers" to the end, and my apply pass notes.

This file was written early and grew as the work landed.

## The two checks: commands for the icon designers

Run both from the repository root. Each prints a report, writes JSON with `--json`, and exits 0 on a pass, 1 on a fail and 2 on misuse.

**Pixel-fit check.** One or more SVG files or folders, and one or more target sizes in px.

```
node work/build/scripts/phase-2/icon_pixel_fit_check.js --size 16,24 --weight 1.5,2 --png /path/to/scratch/previews work/build/assets/utility-icons/
python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py --size 24 work/build/assets/pillar-pixel-fit/CL-019-Explain-24px-Fit-1-Black.svg
```

The `.py` name in the drawings brief runs the same check (`.js`), since this environment has Chromium for Node only. `--weight` takes the line the grid asks for at each size (1.5 px at 16, 2 px at 24 from the tokens below) and fails a main stroke width more than 0.15 px off it. `--png` writes, for each file and size, a picture of the 1x and 2x pixels on a grid with each straight edge that misses a pixel edge marked in red. Write it to a scratch folder, not under `work/build`.

**Look-alike check.** A folder of new SVGs (add `--recursive` for subfolders).

```
node work/build/scripts/phase-2/icon_likeness_check.js work/build/assets/utility-icons/ --json /path/to/scratch/likeness.json
```

Name each file with its master's ID where it has one (`CL-025-...`, `R-13-...`, `CL-019-...-24px-Fit-1-...`), so a redraw's or a fit's pair with its own original is reported apart. Options are read from `Option-A`, `Opt-2`, `Fit-1` or `Variant-B` and sizes from `16px` anywhere in the name; the options of one subject are reported apart, not failed. Editions of one drawing (`-Red-Black`, `-Black`, `-Newsprint`, `-Red-Newsprint`, `-One-Color`, `-Two-Color`) are compared once, the black edition first.

Both have a self-test: `--self-test`.

### What the pixel-fit check measures, and its thresholds

Chromium draws each SVG inline in a page, as the guide sets icons, with its box set to the target size, on a clear background, so ink is the alpha channel and every color counts the same. It screenshots the box at device scale 1 (1x), 2 (2x) and a supersample of at least 640 px across for the geometry. A screenshot is used because a canvas keeps a non-scaling stroke at one canvas pixel at any zoom, which misstates the fifth edition's lockmark masters at 2x. Every figure is in device pixels at that scale.

| Measure | How | Passes when |
|---|---|---|
| Stroke widths | Declared: each element's `stroke-width` times its scale on screen. Measured: at every ink pixel, the diameter of the largest disk inside the ink that covers it; pixels no such disk reaches (square corners) take the nearest one's width. "Thinnest" is the thinnest width that covers at least a quarter of a device pixel of ink, and "main" is the most common width. Read to one supersampled pixel | Thinnest at least 1.0 device px. Under one device pixel, a line never reaches full ink |
| Soft edges | Share of ink pixels (alpha 8 or more) with partial coverage (alpha 8 to 246) | At most 95 percent: at least one ink pixel in 20 at full ink. A fit 1.5 px ring at 16 px is 89 percent soft, and a fit 2 px ring at 24 px is 65, so the share cannot tell a fit round drawing from an unfit one. Use it to compare two fits of one drawing; the lower is crisper |
| Straight strokes on whole pixels | Every horizontal or vertical edge at least 1.5 px long, its position read to a hundredth of a pixel from the supersampled coverage. Edges pair into strokes across ink | Each edge within 0.1 px of a pixel edge (a fringe of 10 percent or less). A stroke of whole-pixel width needs both edges there; a stroke of fractional width, such as 1.5 px at 16 px, needs one, since whole pixels cannot hold both. An edge with no partner must sit on a pixel edge |
| Gaps | The smallest distance between separate ink parts | At least 1.0 device px |
| Counters | Enclosed spaces of half a pixel or more in the drawing, against those at 1x and 2x | The same count: none fills in, and no narrow opening closes into a new one |
| Weight (with `--weight`) | The main width against the grid's line | Within 0.15 px |

A file passes at a size when it passes at 1x and at 2x. The check assumes the icon's box sits on whole CSS pixels, as the guide places it.

**Self-test:** 9 of 9 right. Seven planted faults are caught (a square half a pixel off, a 0.5 px line, two parts 0.5 px apart, a hole that fills in, a 1.05 px ring and diagonal set between pixels, a 2 px line where 1.5 px is asked), and two allowances stay quiet (1.5 px strokes at 16 px with one edge on a pixel edge; a round drawing fit to the grid).

**On the masters** (16, 24 and 48 px; the self-test the task asks for):

| File | 16 px | 24 px | 48 px |
|---|---|---|---|
| Lockmark 16 px master | Pass: thinnest 0.99, 46% soft, 10 of 10 straight strokes fit, 4 counters kept | Pass | Pass |
| Lockmark 24 px master | Fail: thinnest 0.64, 99% soft, 8 of 16 fit, 2 of 4 counters left at 1x | Pass: 0% soft, 18 of 18 fit | Pass |
| Lockmark 48 px master | Fail: thinnest 0.34, 100% soft, every counter filled | Fail: thinnest 0.50, every counter filled at 1x | Pass: 0% soft, 22 of 22 fit |
| Lockmark V5 and display masters (identical results) | Fail: 8 of 12 straight edges fit at 1x | Fail: 99% soft, 0 of 12 fit | Fail: 8 of 12 fit at 1x, 4 of 12 at 2x |
| CL-019 Explain | Fail: line 0.42 declared, thinnest 0.39, 100% soft, smallest gap 0.74, every counter filled | Fail: line 0.63, 100% soft, 4 of 8 fit, every counter filled | Fail: 8 of 15 fit at 1x and 6 of 15 at 2x; at 1x two openings close into new counters (6 against 4) |
| CL-024 Feedback Loop | Fail: thinnest 0.39, smallest gap 0.35 px | Fail: thinnest 0.61, smallest gap 0.52 px | Fail: 2 of 8 straight strokes fit at 1x, 3 of 8 at 2x |

Each pixel master passes at its own size and fails at the others, and the Civic Line masters fail on line width at 16 and 24 px, which is DR-136's reason for the 48 px floor. At 48 px the two Civic Line masters pass on width (1.26 px declared, 1.24 measured) and gap, and fail on straight edges and, for CL-019, counters, because they were not drawn to the pixel grid. That is information for the pillar fits, not a fault in the masters.

### The look-alike check's method and threshold

The port of Board 6's likeness is exact. Each drawing is drawn by Chromium in its own box at 24 px on Newsprint, its ink read against Charcoal, blurred with a Gaussian of sigma 1.2 px, and two drawings compared by Pearson correlation, best over shifts of up to 1 px. A 24-unit utility icon and a 128-unit Civic Line drawing both draw at 24 px, so they compare as they would sit side by side. The masters draw exactly as Board 6 drew them. A new drawing draws its coverage in Charcoal first, so red, grey and `currentColor` parts count as ink.

| Figure | Likeness | What it means |
|---|---|---|
| Median of the 7,381 master pairs | 0.721 | Board 6: 0.721 |
| 95th percentile | 0.871 | **Watch**: listed for a look, no fail |
| 99th percentile | 0.913 | **Flag**: as alike as the closest 74 master pairs, and the check fails |
| 99.9th percentile | 0.948 | |
| Closest master pair | 0.964 | R-06 and R-44, which share a base drawing; the next are CL-028 and R-27, R-05 and R-14 |

The flag sits at the 99th percentile because the master pairs above it are drawings that share a base, such as a page or a document with a different mark on it. A new icon that close to a Civic Line drawing would read as part of the topic set. The watch line at the 95th percentile gives the creative director the near misses. Both can be moved with `--flag` and `--watch`.

**Self-test:** the masters reproduce Board 6's distribution (p50, p90, p95) and all 18 of its set pairs with a largest difference of 0.0000. CL-024 under a utility name, and the same drawing scaled onto a 24-unit grid, are both flagged against CL-024. A plus sign is not flagged (its closest master is CL-005 at the 73rd percentile). A redraw named `CL-025-...` and a fit named `CL-019-...` have their pairs with their originals reported apart. A red-black edition beside its black edition is compared once, and a second size and fit of one subject is reported as an option.

The work below this line is in progress.
