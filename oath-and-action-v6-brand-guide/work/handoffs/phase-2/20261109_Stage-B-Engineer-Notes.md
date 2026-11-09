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

## Tokens: marks and icons (6.0.0-gate2.4)

The source is `work/build/tokens/src/oa-tokens.src.mjs`; `tokens_build.mjs` wrote `tokens.json` and `tokens.css`, now 495 tokens. Each new token has a reader on the page, and two tests hold that true: the build warns when a token in the mark or utility icon family has no `var()` in the page's CSS, and `guide_check.js` measures every drawn mark against its token (`markTokens`).

| Token | Value | Job | Reader |
|---|---|---|---|
| `oa.component.mark.ring.now` | 3 px | the heavy ring of the step a record is at now | 60 rings in chapter 11 and chapter 01's piece |
| `oa.component.mark.ring.ahead` | 1.5 px | the fine ring of a step not yet reached, and under a slash | 85 rings |
| `oa.component.mark.slash` | 2 px | the slash across a step that never happened | 13 slashes |
| `oa.component.mark.halo` | 4 px | the surface band that keeps a number readable across its slash | 13 numbers |
| `oa.component.mark.line.reached` | `{oa.border.width.rule}`, 2 px | the line between steps reached | 124 lines |
| `oa.component.mark.line.ahead` | `{oa.border.width.hairline}`, 1 px | the line on toward steps ahead | 46 lines |
| `oa.component.mark.takePart.disc` | 11 px | the take-part disc's width | 30 discs |
| `oa.component.mark.takePart.keyline` | `{oa.border.width.hairline}`, 1 px | the Charcoal keyline inside the disc (Rule 05.5) | 32 keylines |
| `oa.component.mark.takePart.cut` | 1.5 px | the band of surface between disc and ring | 30 cuts |
| `oa.component.icon.utility.line.medium` | 2 px | a utility icon's line at 24 px; extensions record the 24-unit grid and round caps and joins | the shell's menu glyph |
| `oa.size.icon.small`, `.medium`, `.large` | 16, 24, 48 px | descriptions now follow DR-136 and D2-497: which family sets an icon at each size | the menu glyph reads `.medium` |

How the plates read them: chapter 11's plates (`apply_systems_ch11.py`, the systems designer's) write each mark's width as a number. `guide-shell.css` now sets each width from its token, with a selector that names the mark by its classes and its drawn width ("Mark tokens", D2-402). A failure plate that draws a fault at another width keeps it, and the three that do (`s-11-5-failure`, `s-11-6-failure`, `s-11-7-failure`) render as before. When the plates write `var()` themselves, those rules go; I ask for that below.

Left out until they have a reader: the circle sizes by place (24, 26, 28 and 30 px), and the 16 px utility line. **For the icon designers, the 16 px line is 1.5 px**, on a 16-unit master, round caps and joins; it enters the token file with the first 16 px utility icon on a page.

## Shell: chapters 09, 10 and 12, and the audit's two shell fixes

- **Chapter list.** Chapter 09's anchor is `pillar-icons` (D2-446), with no alias for `pillar-marks`, since no link to it ever reached a reader. Chapter 10 keeps `symbols` and chapter 12 `graphic-devices`; titles and instruction lines already matched the brief's table. The Symbols and graphics opener lists 09, 10 and 12 as "Coming later" until their files exist, and links each one once it does (unchanged mechanism, proven again by the build self-test).
- **UX-1.** The menu glyph is now an inline SVG, three 2 px strokes in `currentColor` on today's 18 by 12 px geometry, on whole pixels (the pixel-fit check passes it at 24 px with `--weight 2`). It carries `data-icon="U-menu"` and `data-icon-family="utility"` and reads the 24 px size and line tokens. The forced colors block sets it to `ButtonText`. In Chromium's forced colors emulation the bars now show on dark and on light, and normal mode looks as before. The utility hand's Menu drawing replaces it at round 2.
- **DR-153.** The Fit to window switch stands 44 px tall (`--oa-size-target-touch`). The contents and rule lists are unchanged. Its pressed option is now underlined at 2 px as well as filled, since C-5 found the on state told from the off state by color alone.
- **D2-461.** The tokens.css download link is unchanged.

## `guide_check.js`: the audit's checks that run today

Each runs at every width unless noted, and skips a picture stage (`role="img"`); a live specimen (D2-516) is checked like the shell. Icons are found by `data-icon` and `data-icon-family` (D2-517).

| Check | Requirement | Fails on |
|---|---|---|
| `forcedGlyphs` | D-1, UX-1 | with forced colors on, dark and light, a glyph part (any `[data-icon]` part, or a wordless element inside a control) that stands out from its ground at 1.5 to 1 or more normally and drops under 1.5 to 1 |
| `focus` | G-1, UX-5 | a Tab stop without an outline of 2 px or more at 3 to 1 against its ground; a box-shadow no longer counts. Now at 390 px as well as 1440 |
| `menuDialog` | G-2, G-3 | at 390 and 360 px: Menu not opening with focus inside, Tab leaving the open menu or landing out of view, Escape or Close not shutting it, or focus not returning to Menu |
| `motion` | E-1, E-3 | a SMIL element, an autoplay, an animation that repeats forever, or a glyph transition over 200 ms |
| `reducedMotion` | E-2 | at 1440 px, any animation or transition left running under `prefers-reduced-motion` |
| `textSpacing` | F-1, F-3 | at 390 and 360 px, with SC 1.4.12's spacing and then with text at 200 percent: a control that clips its words, a glyph over its word, or (spacing) a sideways scroll |
| `labelInName` | A-3 | a control's name that does not start with its visible words |
| `controlNames` | A-4 | a control with no visible word and no named image, other than "Clear the search" |
| `titleOnly` | A-8 | a control or image named only by `title`, or a `title` holding words found nowhere else |
| `iconNames` | A-1, A-2 | a glyph beside its word that is not hidden, or a named glyph whose name repeats its words |
| `iconTargets` | B-1, DR-153 | a control holding a glyph under 44 by 44 px; a Fit to window button under 44 px tall (measured where it shows, from its minimum height where hidden) |
| `iconSizes` | B-3 | a glyph at a size its family does not use: utility 16 or 24; pillar 16, 24 or 48 up; status 24, 26, 28 or 30; topic and atlas 48 up, or 24 only for the 41 that read there |
| `disabledControls` | G-4 | a `disabled` attribute in a toolbar, or `aria-disabled` with no visible reason through `aria-describedby` |
| `stateCues` | C-5 | a pressed, selected, checked or current control told from its off peer only by color, background or shadow |
| `markTokens` | D2-402 | a mark drawn off its token outside a failure plate, or, where chapter 11 is in the page, a mark token with no reader |

The self-test now plants 72 faults (17 new) and 9 allowances (5 new). `--self-test --results PATH` writes its results where you choose; without it they still go to the stage A board folder.

## Page weight

Today the page is 6.24 MB: chapter 01 2.54 MB (most of it photographs), 02 0.78, 03 0.60, 04 0.38, 05 0.37, 06 0.28, 07 0.23, 08 0.25, 11 0.42, the appendix 0.15, and the head and shell 0.13. The limit is 16 MB.

**Sprites.** A specimen draws a master as `<svg viewBox="0 0 128 128" width="48" height="48" aria-hidden="true" focusable="false" data-icon="CL-019" data-icon-family="pillar"><use href="#oa-sym-cl-019"/></svg>`. The build puts every symbol the page references into one hidden sprite per family, once, right after `<body>`. A symbol draws in `currentColor`; its accent draws in `--oa-icon-accent` where the `<svg>` sets it (`style="--oa-icon-accent: var(--oa-color-identity-signature-on-newsprint)"` for the two-color edition) and in the ink otherwise. Mask ids are kept, prefixed with the symbol's id; ids nothing points at are dropped. Drawn in Chromium beside the masters, all 122 symbols match: largest channel difference 2 against the black edition and 5 against the red-black edition, with no pixel off by more than 8. All 122 together weigh 318 KB. The family list in `guide_build.py` holds Civic Line now; the pixel-fit pillar icons and the utility set join when Dustin approves their drawings, and no family holds a share, zoom, print or information glyph (DR-154).

**Inlined drawings.** A specimen in chapter 09 or later that inlines a master (half or more of its path data, character for character) is a build warning that names the master and the `<use>` to write. Three earlier specimens inline masters today: `s-01-pillars` (CL-019 to CL-022), `s-01-21-correct` (CL-055) and `s-01-21-failure` (CL-019). The build lists them as notes, so the strict build stays clean, and their owner can move them at round 2.

**Contact sheets as images.** `<img data-oa-sheet="600" src="work/build/assets/civic-line/contact-sheets/...-2x.png" alt="..." width="600">` embeds the sheet resampled to twice the width it is shown at, as a 16-color palette PNG. A 2x sheet of 435 KB comes to 127 KB at full size, and the five red-black sheets shown 600 px wide come to 69 to 93 KB each, 393 KB in all (524 KB once encoded in the page).

**Budgets.** The build weighs each chapter in the page and warns past its budget, and warns when the page passes 15.5 MB, half a megabyte under the limit. The budgets sum to 15.5 MB across all 26 chapters, so stages C and D inherit room:

| Part | Budget (MB) | Today (MB) |
|---|---|---|
| 01 | 2.70 | 2.54 |
| 02, 03 | 0.85, 0.65 | 0.78, 0.60 |
| 04, 05 | 0.45 each | 0.38, 0.37 |
| 06, 07, 08 | 0.35, 0.30, 0.30 | 0.28, 0.23, 0.25 |
| 09 | 0.40 | not built |
| 10 | 1.00 (122 drawings through the sprite and the contact sheets) | not built |
| 11 | 0.55 | 0.42 |
| 12 | 0.50 | not built |
| 13 to 26 | 0.45 each | not built |
| head and shell, sprites, appendix, front matter | 0.20, 0.35, 0.20, 0.10 | 0.13, 0, 0.15, 0.01 |

The build report carries the figures under `weight`.

## Routine calls

- D2-xxx | The pixel-fit check is a Node script that renders in Chromium, and the drawings brief's `.py` path runs it through a thin wrapper | No SVG renderer exists for Python here, and Chromium draws icons as the guide does
- D2-xxx | The pixel-fit check rasterizes by screenshotting the SVG inline in a page at device scale 1, 2 and a supersample | A canvas keeps a non-scaling stroke at one canvas pixel at any zoom, which misstates the fifth edition's lockmark masters
- D2-xxx | Pixel-fit thresholds: thinnest stroke 1.0 device px, soft edges 95 percent, straight edges within 0.1 px of a pixel edge, gaps 1.0 device px, the same counters as drawn, and with `--weight` the main width within 0.15 px | Under one device pixel a line never reaches full ink; the soft share cannot tell a fit round drawing from an unfit one, so it fails only an all-fringe drawing
- D2-xxx | A stroke of fractional width passes with one edge on a pixel edge, a whole-pixel stroke needs both | A 1.5 px line at 16 px cannot hold both edges on whole pixels
- D2-xxx | A drawing passes a size only when it passes at 1x and at 2x | Both densities are in use
- D2-xxx | The look-alike check flags at the 99th percentile of the masters' pairs (0.913) and lists from the 95th (0.871) | The master pairs above the 99th are drawings that share a base; a utility icon that close would read as part of the topic set
- D2-xxx | The look-alike check draws masters exactly as Board 6 did, and new drawings as their coverage in Charcoal | The port then reproduces Board 6 exactly, and red, grey and `currentColor` parts count as ink
- D2-xxx | A pair with the master whose ID a file name carries is reported apart; options (Option, Opt, Fit, Variant), sizes and editions are read from file names | DR-135's redraws and the pixel fits are meant to stay close to their originals
- D2-xxx | Mark tokens are literal dimensions with no tier, as chart sizes are; the two lines and the keyline alias the border widths | The tier rule asks a component token to alias a semantic one, and no semantic dimension exists for these jobs
- D2-xxx | The circle sizes by place and the 16 px utility line wait for a reader | D2-402: a token with no reader escapes the parity test
- D2-xxx | The shell sets each mark's width from its token by the mark's classes and drawn width, until the plates write `var()` themselves | The plates belong to the systems designer; a failure plate's deliberate fault keeps its own width
- D2-xxx | The build warns on a mark or utility icon token with no `var()` reader, and `markTokens` measures the drawn marks | The guide and the token file cannot then drift apart unseen
- D2-xxx | The icon size tokens' descriptions follow DR-136 and D2-497 | They described every 16 px icon as a Civic Line icon
- D2-xxx | Chapter 09's anchor is `pillar-icons`, with no alias for `pillar-marks` | D2-446; no link to it reached a reader
- D2-xxx | The menu glyph is drawn as an SVG stroke on today's geometry, tagged `U-menu` in the utility family | UX-1, with no visible change until the utility set's Menu drawing replaces it
- D2-xxx | The Fit to window switch's pressed option is underlined at 2 px as well as filled | C-5; the guide underlines the current item elsewhere
- D2-xxx | `forcedGlyphs` fails a part that stands out at 1.5 to 1 or more normally and under 1.5 to 1 in forced colors | A red accent on Newsprint (2.96 to 1) and a tracker's surface-colored cut are drawn that way on purpose; an erased part is what UX-1 found
- D2-xxx | `focus` counts an outline only, 2 px or more, at 3 to 1 against the better of the ground outside and the control's own fill, and runs at 390 px too | UX-5; the skip link's Newsprint ring reads against its own Charcoal box
- D2-xxx | A glyph without `data-icon-family` is listed and its family inferred from its ID; it fails from round 2 (`REQUIRE_FAMILY`) | Chapter 01's pillar row carries `data-icon` alone today, and its owner adds the family
- D2-xxx | B-3's list of the 41 topic symbols that read at 24 px is empty until round 2, so any topic symbol at 24 px fails until it is listed | The list exists only as a count in the scoping notes (DR-136)
- D2-xxx | A control hidden until it takes focus (the skip links) is left out of A-3 and A-4 | Its words show when it is used
- D2-xxx | One sprite per family holds only the symbols the page references, after `<body>`, with ids `oa-sym-` and the master's ID | The page carries each drawing once, and contact sheets cover the rest as images
- D2-xxx | A specimen from chapter 09 on that inlines a master is a warning; the three earlier ones are notes | The plan serves the new chapters, and the strict build stays clean while their owner moves them
- D2-xxx | A contact sheet embeds at twice its shown width as a 16-color palette PNG | Line art keeps its look at a quarter of the weight or less
- D2-xxx | Chapter budgets sum to 15.5 MB across all 26 chapters, with a page warning at 15.5 MB | Half a megabyte stays under the 16 MB limit, and later stages inherit room
- D2-xxx | All my builds and check outputs went to a scratch folder, and the stage A board page was not rebuilt | The task keeps outputs out of `work/build` and boards untouched

## Questions for Dustin

None. Every item above is a routine call inside the approved stage, or one Dustin settled today (DR-153, DR-154).

## Requests to other owners

- **Systems designer.** Write the mark widths in `MARK_CSS` as `var(--oa-component-mark-...)` (the names are in the table above) and keep the classes for the status marks of records requests and agency rules (DR-140); then I remove the shell's bridge rules. When the plates read the circle sizes by place from tokens, I add them. Build chapter 11's five interactive specimens as live components (D2-516), since the checks above run inside them.
- **Chapter 01's owner.** Add `data-icon-family="pillar"` to the twelve icons in `s-01-pillars`, and at round 2 draw `s-01-pillars`, `s-01-21-correct` and `s-01-21-failure` from the sprite with `<use>`.
- **Icon designers.** Run the pixel-fit check with `--weight 1.5` at 16 px and `--weight 2` at 24 px on utility drawings; name each file with its master's ID where it has one; send finals for the sprite to one folder per family once approved.
- **Main session.** The stage A board page still holds the build from before my changes; the next default build rewrites it.

## Left for round 2 in `guide_check.js`

These need specimens or lists that do not exist yet: A-5 (a state word on every step), A-6 (one `aria-current` per pillar row, on the underlined item), A-7 (a kicker's icon beside its own word), A-9 (status lines after a press), B-4 (glyph and word in one control in the library and filter bar), C-1 to C-4 (state marks by shape, ink at 3 to 1 on rendered pixels, red never alone, the yielding red), C-6 (grayscale captures of chapters 09 to 11), D-2 (a red accent under forced colors), D-3 (states and focus in forced colors), D-4 (shell controls in system colors), F-2 (no truncated label, 320 px), G-3 for Close and View full size inside live specimens, G-5 (a grid of symbols as one Tab stop or links in reading order), B-3's list of 41, and `REQUIRE_FAMILY` turned on. UX-2's second pass, the three marks against the badge corners of the fourteen Civic Line drawings that carry one, needs a cropped comparison the look-alike check does not do yet.

