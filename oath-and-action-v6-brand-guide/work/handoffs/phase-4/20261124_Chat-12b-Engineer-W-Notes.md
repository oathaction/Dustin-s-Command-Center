# Chat 12b, Engineer W: the video frame, A21 (CD-S7, item C16-V)

Started 00:01:58 UTC (`date -u`), under `work/handoffs/phase-4/20261124_Chat-12b-Brief.md`, sections 1, 2, 3.1 and 4. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/engineer-w/`. My files: `work/build/app-kit/oa-app.mjs`, `lib.mjs`, `renderers/video-frame.mjs` (new), `specs/a21-video-s04.json` (new), `check-dimensions.py`, `tools/` except `atlas_figures.py` and `atlas_test.py`, `work/build/scripts/phase-2/guide_build.py` and `guide_check.js`, and A21's exports. The chart kit is called, never edited.

## Contracts

Written 00:05 UTC, before the design director's rulings. Where a ruling differs, the ruling wins and I change this section and say so.

### W-C1, the application and its views

A21 is a content file, `work/build/app-kit/specs/a21-video-s04.json`, of a new type, `video-frame`, drawn by `work/build/app-kit/renderers/video-frame.mjs`. Every frame is a still of one moment of the video on chart S04, at the true size of its platform row in `work/research/20261121_Platform-Specifications.json`:

| View key | Size | Platform row | Moment | For |
|---|---|---|---|---|
| `1080-light` | 1080 by 1920 px | `video.vertical` (D4-16: insets 269 top, 120 sides, 672 bottom, and TikTok's button column, x 780 to 960, y 840 to 1260) | 0:08, S04 with its caption | `s-16-11-correct` |
| `1080-light-misheard` | 1080 by 1920 px | `video.vertical` | 0:08, the automatic caption that reads "down 37 points" | `s-16-11-failure`, only if the design director rules that it changes; built only then |
| `1920-light-chart` | 1920 by 1080 px | `video.landscape` | 0:08, "Chart S04, with its source line" | `s-16-10-correct`, the 0:08 cell |
| `1920-light-gap` | 1920 by 1080 px | `video.landscape` | 0:30, "The gap, 23 points to 27" | `s-16-10-correct`, the 0:30 cell |

"light" means the frame's ground is Newsprint, as the storyboard's chart cells are now. A key follows the kit's form, `<width>-<theme>[-<part>]`.

Each frame holds, unless the rulings say otherwise: S04's drawing from the chart kit (`K.draw` on `work/build/chart-kit/specs/s04.json` and its rows, called, never copied or edited), drawn at a narrow width and shown larger as a vector, so the kit's 13 px words grow by the frame's scale (S04 at 280 px is 280 by 273 px; at 3 times, 840 by 819 px with its words at 39 to 42 px); S04's source line on screen while the chart shows (Rule 16.10); the caption band, Inter 600 in Newsprint on Charcoal, two lines at most (Rule 16.11), inside the caption-safe area; and the safe areas as an overlay a reader switches on, as A01 and A09 carry one. The chart's size (the width the kit draws at and the scale), each part's type size and place, and whether a name plate shows come from the design director's rulings and go into the content file as numbers; the renderer lays out from them and fails the build when a word leaves the frame's live box, a word sits under the floor the content file names, or a part crosses the button column.

### W-C2, the words the renderer reads (chapter 16's `--page-words` hook)

`python3 -I work/build/scripts/phase-4/phase4_ch16_build.py --page-words all` prints `{"A21": {...}}`, and `--page-words A21` prints the entry alone, as chapter 20's generator does. The entry's keys:

| Key | What it holds | Required |
|---|---|---|
| `frames` | An object keyed by view key (W-C1), one entry for each view a plate places | yes |
| `frames.<key>.caption` | The caption band's lines, a list of one or two strings, about 42 characters each, broken at a phrase (Rule 16.11) | yes |
| `frames.<key>.alt` | The frame's alt: every word the frame shows (D4-211, D4-299), since at a plate's scale its words fall under the 13 px floor and the frame is a picture | yes |
| `frames.<key>.time` | The moment, such as "0:08", for the frame's record; printed only if a ruling says so | no |
| `source` | S04's source line as `s04.json` carries it; the renderer fails the build if it differs from the spec's `source_line` | yes |
| `name_plate` | "Dustin Cathcart, Founder and Editor", or null when the rulings put no name plate in these frames | no |
| `safe_labels` | The overlay's words (amended 00:20 UTC after DD12b-R1, which labels each safe area with its basis): `vertical` (the vertical frame's basis, such as "Meta's and TikTok's ads guides, D4-14 and D4-16"), `landscape` (the storyboard's, such as "Studio title-safe, until chapter 23"), `buttons` (the app's button column), `controls` (the player's control bar, the storyboard's bottom tenth). `safe` stands in for `vertical` if written. Absent, the overlay draws the outlines, the hatching and the inset figures with no words; the kit types only the figures ("269 px") | no |
| `switch` | The plate switch's words; default "Show the safe areas" | no |

The renderer reads the chart's own words (labels, values, ticks, the measure line if a ruling shows it) from `s04.json` through the chart kit, never from these keys. Until the hook exists the renderer reads a fixture, the file `OA_PAGE_WORDS_A21` names (mine: `.../engineer-w/a21-words-fixture.json`, placeholder words copied from Rules 16.10 and 16.11 as they stand), and the plate carries `provisional_words`, so the guide build warns and `--strict` fails until the kit draws A21 again from the generator. The plate records `{"generator": "work/build/scripts/phase-4/phase4_ch16_build.py", "id": "A21", "sha256": ...}`, so a change to A21's words stales the plate and nothing else does.

The alt check: the renderer collects every word the frame shows (the export page's text and the drawing's `<text>`) and fails the build when one is missing from the view's `alt`, after spaces and quotation marks are made plain. The drawing's axis numbers between the first and last tick (50, 60, 70) count as carried when the alt gives the scale's ends ("from 40 to 80 percent"), as S04's measure line does.

### W-C3, the placeholder a plate uses

As A09 is placed: one element per place, empty, in the generator's specimen HTML:

```html
<div data-oa-app="A21" data-oa-app-views="1080-light"></div>          <!-- s-16-11-correct -->
<div data-oa-app="A21" data-oa-app-views="1920-light-chart"></div>    <!-- s-16-10-correct, in the 0:08 cell -->
<div data-oa-app="A21" data-oa-app-views="1920-light-gap"></div>      <!-- s-16-10-correct, in the 0:30 cell -->
```

The guide build puts the kit's frame in its place: an `<svg role="img" aria-label="<the view's alt>">` scaling the frame's markup, whose inside is `inert` and `aria-hidden`, so the frame is a picture named by its alt (D4-211). The frame grows to its wrapper's width and never past its true width, so the wrapper sets the scale: a 270 px wrapper shows the vertical frame at exactly a quarter, a 200 px wrapper a landscape frame at about a tenth (200 of 1920). The plate's label states the scale (the generator's words). A view with safe areas brings the plate's switch ("Show the safe areas"), one per placeholder; a landscape view has no safe area of its own in the table (`video.landscape`: "Safe area set in chapter 23"), so it brings none unless a ruling sets one. Since the words fall under 13 px at those scales, each frame is a picture whose alt carries every word, as W-C2's alt does. (Amended 00:20 UTC: the specimen stays `readable=True`, the design director's DD12b-Q2, since `guide_build.py` and the guide check's `pageFrame` test fault a kit page frame inside an image stage; the frame itself is the picture, an `svg role="img"`.)

**The switch (00:25 UTC, DD12b-Q3):** a placeholder may carry `data-oa-app-switch="none"` (the frames placed without their overlays and with no switch; for the storyboard's 200 px cells, whose overlays are in the exports) or `data-oa-app-switch="on"` (the plate's switch starts checked, so the safe areas show when the page loads and a reader can switch them off; for both 16.11 plates). Any other value warns, so `--strict` fails. In `tools/app_plates.py`, with four new self-test cases (25 of 25 pass).

**As built (00:20 UTC, DD12b-R1):** each frame is a page laid out at its pixels divided by its scale (540 by 960 CSS px for the vertical frame, 960 by 540 for the storyboard's) and captured at that device scale (2) to the row's pixels. The plate's view records the layout page's size (`w` 540, `h` 960), so a frame never shows past half its exported size on the guide's page, and the guide check reads its words at the layout page's sizes (13 px source line, 13 and 14 px chart words, 16 px caption), which sit on the type scale; the exported pixels are twice those.

### W-C4, the exports

One PNG per view at its true size, `20261124_Video-Frame-S04-<Part>-<W>x<H>.png` in `work/build/exports/phase-4/`, and one more per view with the safe areas drawn on (`...-Safe-Areas-<W>x<H>.png`; not for the misheard view, which repeats the vertical frame), each listed in the exports manifest with its platform row, its view and its device scale, and checked by `check-dimensions.py` (exact pixels, the row's size). The run order: `phase4_ch16_build.py`, `node work/build/app-kit/oa-app.mjs build A21 --date 20261124`, `phase4_ch16_build.py` again, then the strict build, each under the lock.

## Rulings

None of mine; I follow the design director's (`20261124_Chat-12b-Design-Director-Notes.md`, "Rulings").

## Routine calls

- D4-xxx | A21 is drawn by a renderer that captures its own exports and checks (`R.build`, a branch in `oa-app.mjs`), not by the share card's path | Its views have their own sizes, device scale and checks; one generic branch keeps every other renderer's path as it was
- D4-xxx | The source line is the chart kit's own element (`p.oac-source` from `K.figure`), set in the kit's source-line type, with the kit's `max-width: 42em` lifted inside the frame | DD12b-R1 asks for the kit's source-line type at 330 and 680 layout px; at 42em (546 px) the storyboard's line would break at 546
- D4-xxx | The source line sits its gap under the chart's last ink, measured in the browser at build, the margin set from it | DD12b-R1 says "under the chart's last ink"; the kit pads the drawing 10 layout px under its last row, which left the vertical frame's source line 3 px above the band
- D4-xxx | A frame fails its build when its source line ends less than 16 px above the caption band | DD12b-R1's own least gap in its overflow order; 3 px read as touching
- D4-xxx | The overlay's inset figures sit in the top inset (the sides' figure at the left, the top's centered) and the bottom's in the bottom inset, the basis under them where the top inset has room, beside them where not | A figure at the side's middle lay over the source line
- D4-xxx | A placeholder's `data-oa-app-switch` takes "none" (no overlay, no switch) or "on" (the switch starts checked) | DD12b-Q3: a 200 px storyboard cell has no room for a switch, and Rule 16.11 teaches the caption-safe area, so its plates may open with it shown
- D4-xxx | The alt check matches a word whole ("50" is not carried by "2050") and reads "%" as "percent" | A substring match let tick numbers pass inside other figures

## Done

## Requests

- **`oa-app.mjs` and `lib.mjs` final, 00:20 UTC** (SHA-256 starting `5ebcbacf8e4ea85d` and `846b7680f4351b0d`). I edit neither after this; A21's work goes on in `renderers/video-frame.mjs` and `specs/a21-video-s04.json`, which only A21's plate reads. Engineer A's A11 to A20 builds from now on are fresh against them.
- **Design director and editor (00:21 UTC): the four alts lack the row values.** The kit's check (D4-211, D4-299, W-C2) finds every frame's alt missing seven of the words the drawing prints: "51.4", "60.2", "62.6", "70.0", "71.0", "74.5", "74.7" (47.7 is there through S04's alt). The composed alt's "Its rows" gives each row's name and row words; it needs each row's two rates too, for example "18 to 24, 51.4 in 2020 and 47.7 in 2024, Down 3.7 points; 25 to 44, 62.6 and 60.2, Down 2.4 points; 45 to 64, 71.0 and 70.0, Too close to call (−1.0); 65 and over, 74.5 and 74.7, No clear change (+0.2)". The figures are S04's rows (`work/build/data/census-cps-reported-voting.csv`, the chart's two years). Either the composer in `phase4_ch16_build.py` adds them or the editor's `frame_alts` carry them; until one does, the kit places no A21 plate (the build exits 1 and names the words). Every other word passes: the ticks by the scale's ends ("40 to 80 percent"), the source line, the caption lines, the row names and row words, the legend's years.
- **Design director, DD12b-Q3 answered (00:25 UTC):** `data-oa-app-switch="none"` on the two storyboard placeholders in `s-16-10-correct`, `data-oa-app-switch="on"` on the two 16.11 placeholders, if you want them on (W-C3, "The switch"). The hook reads it now; nothing needs a kit rebuild.
- **Editor, via the design director's "Words for": `safe_labels`.** `R['16.11']['safe_labels']` with `vertical`, `landscape`, `buttons` and `controls` (W-C2, amended), so each overlay names its basis as DD12b-R1 asks. Without them the overlays carry the figures alone.

- **Engineer A and the main session (00:14 UTC):** A21 needs a new branch in `oa-app.mjs` (a renderer that builds its own views, `R.build`, edited 00:13 UTC) and two new overlay kinds in `lib.mjs` (`hatch-in`, `label`, edited 00:12 UTC). Both files are inputs of every kit plate, so **A04 to A20 read stale from 00:12 UTC** until rebuilt. Engineer A: your final A11 to A20 build needs to come after my last edit to `oa-app.mjs` and `lib.mjs`; I will write "oa-app.mjs and lib.mjs final, HH:MM UTC" here and edit neither after it. I rebuild A04 to A10 myself (`--date 20261121`, under the lock) and run `phase4_ch20_build.py` after them, so chapter 20 is not stale.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

## Not tested
