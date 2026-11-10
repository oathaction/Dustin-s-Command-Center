# Promotion: engineer's notes

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261110_Promotion-Brief.md` (item 4 of "Who does what") and the main session's task. I read my role file, `CLAUDE.md`, the promotion brief, my round 0 notes, and the decision log entries D2-568 to D2-594, DR-156 to DR-186 and D2-709 to D2-718.

I wrote the code against fixtures first, since the makers' folders did not exist when I started. All three landed while I worked (utility first, then the Civic Line set and the pillar icons at 03:53), and every check below ran on the real finals unless a line says fixtures.

## What changed

The guide's sprite now reads three families of finals, and the masthead draws its menu glyph from it.

- **Three families.** `guide_build.py` reads Civic Line from `civic-line-v6/black/`, the pillar fits from `pillar-icons/` (black edition only, found one folder down in `svg/`), and the utility icons from `utility/svg-24/` and `utility/svg-16/`. Each symbol takes the brief's id: `oa-sym-cl-025`, `oa-sym-cl-019-24px`, `oa-sym-u-close-24px`. The rules from round 0 hold: the page carries only the symbols it references, each once, one hidden sprite per family right after `<body>`, the accent through `--oa-icon-accent`, and every id inside a symbol prefixed with the symbol's own id.
- **A symbol draws its file.** A utility icon keeps its line, caps, joins and `fill="none"` on its root, and a pillar fit keeps `shape-rendering="crispEdges"` there. The sprite copies those root attributes onto a group around the drawing, so a `<use>` draws the file whatever the page's CSS sets on the `<svg>` around it. The file's `color` stays behind, so `currentColor` follows the page. A pillar fit's accent is a single path, not a group, and now takes `--oa-icon-accent` as Civic Line's accent groups do.
- **The masthead's menu glyph** is Utility Menu A (`U-menu`, DR-163), drawn as `<use href="#oa-sym-u-menu-24px"/>`. The shell no longer sets its stroke; under forced colors it sets the glyph's `color` to `ButtonText`, which the symbol's `currentColor` follows. Readers see the approved drawing: three even bars 18 px wide with round ends, now 14 px tall where today's were 12.
- **The 1x and 2x pattern for pillar icons** (DR-179, D2-634): two classes in the shell, `oa-at-1x` and `oa-at-2x`, switch two `<use>` in one `<svg>` at 2 device pixels per CSS pixel. The build checks the markup (below).
- **The utility line token's reader.** The shell's `.bars` rule read `--oa-component-icon-utility-line-medium` until now. The glyph's line now comes from its file, so the build compares every utility icon the page draws against its size's token (line width, caps, joins, grid) and counts that comparison as the token's reader. A 24 px utility icon drawn at another line is a warning.
- **New build checks**, each a warning unless it says note: a family folder that exists but holds nothing the sprite can read; a file with no `data-id` or `data-icon`, an id of the wrong form, no size, or a grid that does not match its size; a second file for one symbol; a reference to no symbol, which names the missing family folder when that is the reason; a 24 px pillar fit without its master for 2x screens beside it; a 16 px fit with a master beside it; an `oa-at-2x` with no `oa-at-1x`; `oa-at-1x` on a drawing that is no fit; `--oa-icon-accent` on a pillar icon under 48 px (R10, D2-497). A missing family folder stays a note, and a 16 px utility icon on a page is a note to me, since its line token does not exist yet (D2-577).
- **`guide_check.js`** now sees a glyph drawn through `<use>`. `forcedGlyphs` reads the symbol's paints from its markup and resolves `currentColor`, the accent variable and literal colors as the `<use>` draws them. Before this, a `<use>` glyph was invisible to the check, and the masthead's glyph would have passed unseen.
- **`sprite_check.js`** (new) draws every symbol through `<use>` beside its own file, at 1x and 2x, and draws the pillar pattern at 1x, 1.5x and 2x. `guide_build.py --sprite-sheet` writes the symbols it reads.
- **The look-alike check reads the set in use** (D2-748). `icon_likeness_check.js` now compares new drawings with the 124 drawings in `civic-line-v6/` by default, so the six redraws and CL-073 and CL-074 count as masters and the October drawings they replaced do not. `--masters october` reads the 122 October masters, which Board 6 measured. Moving the masters moves the lines a little: the flag line (99th percentile) goes from 0.913 to 0.909 and the watch line (95th) from 0.871 to 0.868.

## The families, their folders and symbols

| Family | Folder read | Files read | Symbols | Symbol id | Source of the drawings |
|---|---|---|---|---|---|
| Civic Line | `work/build/assets/civic-line-v6/black/` | `*-Black.svg`, by root `data-id` | 124 | `oa-sym-<id>` | the Civic Line hand's set in use (D2-716): 116 October masters and the eight approved finals (DR-156 to DR-160) |
| Pillar fits | `work/build/assets/pillar-icons/` and below | `*-Black.svg`, not `*-Red-Black.svg`, by root `data-id` and `data-size` | 8 | `oa-sym-<id>-<size>px` | the Civic Line hand's finals: fit B at 24 px, the one fit at 16 px (DR-179) |
| Utility icons | `work/build/assets/utility/svg-24/`, `svg-16/` | `*.svg`, by root `data-icon` and `data-size` | 36 | `oa-sym-u-<name>-<size>px` | the utility hand's 18 finals at two sizes (DR-161 to DR-178), with the ids `U-selected-check` and `U-view-full-size` that match their file names |

All 168 symbols together weigh 342,654 bytes in a sprite (Civic Line 325,388, pillar 6,337, utility 10,929), under the 0.35 MB the page budget gives sprites. A page draws only what it references, and chapter 10 shows the full set as contact sheet images (D2-717), so no page should come near that.

## The pattern specimen makers use

Every glyph is an `<svg>` with `aria-hidden="true" focusable="false"`, a `data-icon` and a `data-icon-family` (D2-517), and its word beside it in the control or text. Write the `<use>` and nothing else inside; the build adds the symbol. Never inline a drawing the sprite holds: from chapter 09 on that is a warning.

**Civic Line** (topic and atlas symbols, and the pillar icons at 48 px and up). 48 px and up, or 24 px for the 41 that read there (DR-136):

```html
<svg viewBox="0 0 128 128" width="48" height="48" aria-hidden="true" focusable="false"
     data-icon="CL-025" data-icon-family="topic"><use href="#oa-sym-cl-025"/></svg>
```

For the two-color edition, add `style="--oa-icon-accent: var(--oa-color-identity-signature-on-newsprint)"` to the `<svg>`; without it the accent draws in the ink. `data-icon-family` is `topic` for a CL drawing, `atlas` for an R drawing, and `pillar` for CL-019 to CL-022 at 48 px and up.

**Pillar icons at 24 px.** The fit on screens under 2x, the master from 2x (DR-179), in one `<svg>`. Write both, with these classes:

```html
<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"
     data-icon="CL-019" data-icon-family="pillar"><use class="oa-at-1x" href="#oa-sym-cl-019-24px"/><use class="oa-at-2x" href="#oa-sym-cl-019"/></svg>
```

**Pillar icons at 16 px.** The fit on every screen (D2-634), one `<use>`:

```html
<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false"
     data-icon="CL-019" data-icon-family="pillar"><use href="#oa-sym-cl-019-16px"/></svg>
```

Under 48 px a pillar icon is one color, so it takes no `--oa-icon-accent` (R10, D2-497). A plate that shows a fit itself on every screen, such as the 24 px fit enlarged to show its pixels, puts `data-oa-res="fixed"` on its `<svg>` and draws the fit alone.

**Utility icons at 24 and 16 px.** The `viewBox` matches the size:

```html
<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"
     data-icon="U-close" data-icon-family="utility"><use href="#oa-sym-u-close-24px"/></svg>
<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false"
     data-icon="U-close" data-icon-family="utility"><use href="#oa-sym-u-close-16px"/></svg>
```

A utility icon draws in `currentColor`, so it takes the ink of the word beside it. To turn or mirror one, as the utility manifest lists for Arrow and Chevron (D2-652, D2-653, D2-556), put a `transform` on the `<use>` about the grid's center, which keeps every line on the grid: `transform="rotate(180 12 12)"` turns the 24 px chevron to open, and `transform="matrix(-1 0 0 1 24 0)"` mirrors the 24 px arrow for Previous. At 16 px the center is 8 8 and the mirror is `matrix(-1 0 0 1 16 0)`. Give the glyph's box whole-pixel CSS coordinates; the pixel-fit result assumes it.

The names in the ids: `close`, `menu`, `arrow`, `chevron`, `download`, `another-site`, `search`, `filter`, `copy`, `play`, `pause`, `reset`, `error`, `success`, `selected-check`, `view-full-size`, `sort`, `warning`, each with `-24px` or `-16px`.

## Why the switch sits at 2x

DR-179 names 1x and 2x screens, and many screens sit between, at 1.25 or 1.5 device pixels per CSS pixel. I ran the pixel-fit check on the four masters and the four 24 px fits at 30, 36, 42 and 48 px, which is what a 24 px icon covers on a 1.25x, 1.5x, 1.75x and 2x screen. Figures at device scale 1:

| Screen | Master: line | Master: counters kept | Master: smallest gap | Fit B: line | Fit B: counters kept | Fit B: smallest gap |
|---|---|---|---|---|---|---|
| 1.25x (30 px) | 0.75 to 0.80 px, fails | Explain 2 of 4, Track 0 of 3, Connect 1 of 3 | Act 0.64 px, fails | 1.25 px | all | Act 1.23 px |
| 1.5x (36 px) | 0.86 to 0.95 px, fails | Explain 0 of 4, Track 1 of 3, Connect 1 of 3 | Act 0.78 px, fails | 1.53 px | all | Act 1.50 px |
| 1.75x (42 px) | 1.09 px | Explain gains two (4 to 6), the rest kept | Act 0.94 px, fails | 1.72 px | all | Act 1.75 px |
| 2x (48 px) | 1.24 px | Explain gains two, the rest kept | Act 1.07 px | 1.96 px | all | Act 2.00 px |

The master clears the line and gap floors only from 2x. Below it, fit B keeps every counter and gap and a full-ink line; it fails only the straight-edge test, since its pixels cannot all land on device pixels at a fractional scale. So the shell switches at `min-resolution: 2dppx`. Explain's two extra counters at 2x are the creative director's known finding, and DR-179 accepted the master there.

The identity designer's end mark switch (`s-04-6-correct`, Rule 04.6's builders text) shows its fit only at exactly `resolution: 1dppx` and the smooth drawing on every other screen. That is their drawing and their call. The two thresholds differ at 1.25x and 1.5x, so I list it for the main session below.

## The checks' figures

- **Strict build** (`guide_build.py --strict`, to the scratch folder, last run at 03:59 on the final folders): exit 0, no warnings, 6,220,081 bytes, 9 chapter files, 100 rules, 233 specimens. The page's sprite holds one symbol, the menu glyph (371 bytes). Three notes, as in round 0: `s-01-pillars`, `s-01-21-correct` and `s-01-21-failure` inline Civic Line masters the sprite holds. The page is 21 KB lighter than at the start of my session, from other owners' chapter and specimen changes that landed meanwhile, and a sentence in chapter 03 changed between my two builds (the identity designer's).
- **Build self-test**: 12 of 12 scenarios and 108 of 108 expectations (round 0: 9 and 61). The three new scenarios read fixture families made in a temporary folder from the October set and the approved option files, so they run whether or not the makers' folders exist, and every older scenario reads those fixtures too.
  - Three families in one page: one sprite per family, three in all, between `<body>` and the skip links; each referenced symbol once and no other; every id inside a symbol starts with its own id (masks in CL-029 and the Success option A fixture); no symbol keeps the ink, the red or a comment; the pillar fit's accent path draws through `--oa-icon-accent`; utility symbols carry their root's line, caps and joins at 24 and 16 px; the masthead's old bars are gone; a 16 px utility icon gives the token note.
  - Faults: no pillar folder (a note, and the reference to `oa-sym-cl-019-24px` names it), an empty `svg-16` folder, a file with no `data-id`, a second file for CL-019, a 24 px Close at a 2.5 px line, and references to `oa-sym-cl-999` and `oa-sym-u-nothing-24px`. Each gives its warning, and the page still builds with the symbols that exist.
  - The 1x and 2x pattern: the right pattern and a 16 px fit alone give no warning, and `data-oa-res="fixed"` silences a lone fit; a lone 24 px fit, a 16 px fit with a master, a lone `oa-at-2x`, an accent on a 24 px pillar icon, and `oa-at-1x` on a master each give their warning. The shell's switch and both symbols are in the page.
- **`guide_check.js` self-test**: PASS. The clean demo passes, 73 of 73 planted faults are caught (one new: a menu glyph through `<use>` from a symbol that keeps a literal ink) and 10 of 10 allowances stay quiet (one new: the same glyph in `currentColor`, with its `<use>` counted as a part).
- **`guide_check.js` on the built page** at 1440, 1024, 390 and 360 px, run on both builds with the same result: PASS, 0 failures, 761 same-page links. axe-core 4.10.2 finds no violation at any width; 60 focus stops show a ring at 1440 and at 390 px; the phone menu opens, holds focus, closes by Escape and by Close, and returns focus at 390 and 360 px. `forcedGlyphs` reads 78 glyph parts at 390 and 360 px, the masthead's `<use>` among them, and none is erased; at 1440 and 1024 px the menu button is hidden, as before, and it reads 77.
- **Sprite check** (`sprite_check.js`, real finals): PASS. 168 symbols. Through `<use>` beside its file, every pair matches with a largest channel difference of 0, at 1x and 2x: Civic Line 248 black and 248 red-black pairs (48 and 128 px), pillar fits 8 and 8, utility icons 36. The pattern draws the fit at 1x and 1.5x (0 against the fit, 166 to 202 against the master) and the master at 2x (0 against the master, 202 to 203 against the fit), for all four pillars. A planted fault proves the check can fail: with the root attributes left off, utility icons differ by 220.
- **Pixel-fit check** on `utility/svg-24/20261110_Utility-Menu-24px.svg` at 24 px with `--weight 2`: pass at 1x (line 2 px, thinnest 1.98, 3 of 3 straight strokes on whole pixels, 11 percent soft edges, smallest gap 4 px) and at 2x (4 px, 3 of 3, 8 percent). In the built page at 390 and 360 px, at 1x and 2x, the glyph's box is 24 by 24 px with its top on a whole pixel (16 px), and each bar fills whole device rows with partial ink only at its round ends.
- **Look-alike check self-test**: all right on both master sets. October: 7,381 pairs, p50 0.721, p90 0.8472, p95 0.8708, each equal to Board 6's, and Board 6's 18 set pairs reproduced within 0.0000. The set in use: 124 drawings, 7,626 pairs, p50 0.7143, p95 0.8678, p99 0.9092, closest pair 0.9644. Every plant behaves on both sets, and on the set in use a drawing named CL-073 pairs with its own master, reported apart.
- **Look-alike check on the 18 utility finals at 24 px**, against the set in use (read only, output to scratch): no look-alike. One pair to watch, Pause and CL-012 Election Rules at 0.897, the 98.3rd percentile (98.1st against the October set). The utility hand owns this figure; I ran it only to prove the new default.
- **Token tests**: all six steps pass. 495 tokens; parity 615 `:root` properties and 0 failures; rules 0 failures; self-test 35 of 35 plants; Style Dictionary 5.8.0 agrees on 495; Chromium resolves 464 values with 0 failures.

## Routine calls

- D2-xxx | The sprite reads three families: Civic Line from `civic-line-v6/black/`, the pillar fits' black edition from `pillar-icons/` and below, and the utility icons from `utility/svg-24/` and `svg-16/`, with the brief's symbol ids | The promotion brief's folders and ids; the black edition is the one in use under 48 px (D2-497)
- D2-xxx | A symbol carries its file root's paint and rendering attributes (fill, stroke, its width, caps and joins, `shape-rendering`, opacity, style) on a group around the drawing, and leaves `color` behind | A `<use>` then draws the file whatever the page's CSS sets on the `<svg>` around it, and `currentColor` still follows the page
- D2-xxx | An accent drawn as a single shape (a pillar fit's path) takes `--oa-icon-accent` as an accent group does | The pillar fits draw their red as one path in the accent part (D2-497)
- D2-xxx | The masthead's menu glyph is `<use href="#oa-sym-u-menu-24px"/>`, and under forced colors the shell sets its `color` to `ButtonText` | DR-163; the symbol draws in `currentColor`, so forced colors keeps it (UX-1)
- D2-xxx | A 24 px pillar icon is one `<svg>` with `<use class="oa-at-1x">` of the fit and `<use class="oa-at-2x">` of the master; a 16 px pillar icon is one `<use>` of its fit | DR-179 and D2-634 in one pattern that keeps one glyph, one box and one name
- D2-xxx | The shell switches the two classes at `min-resolution: 2dppx` | The pixel-fit figures: the master meets the line and gap floors only from 2x, and fit B keeps every counter and gap below it
- D2-xxx | The build warns on a 24 px fit without its master beside it, a 16 px fit with one, a lone `oa-at-2x`, `oa-at-1x` on a non-fit and an accent on a pillar icon under 48 px; `data-oa-res="fixed"` marks a plate that shows one drawing on every screen | The pattern cannot be half written, and a chapter 09 plate can still show a fit itself
- D2-xxx | The utility line token's reader is the build's comparison of each utility icon on the page against its size's token, since the glyph's line now comes from its file | D2-402 asks each token for a reader; the comparison fails a drawing that drifts from its token
- D2-xxx | A 16 px utility icon on a page is a note until its line token exists | D2-577: the token enters with its first reader, and I add it then
- D2-xxx | A missing family folder is a note; an empty folder, an unreadable file, a second file for a symbol and a reference to no symbol are warnings, the last naming the missing folder when that is why | A folder still on its way should not stop the build; a broken one should
- D2-xxx | `forcedGlyphs` reads a `<use>` glyph's paints from its symbol's markup | A `<use>` hides its shapes in a closed shadow tree, and the masthead's glyph is now one
- D2-xxx | `sprite_check.js` compares each `<use>` with its file drawn inline in the same cell in turn, at 1x and 2x, and passes at a channel difference of 8 or less | Chromium's raster of one drawing differs by up to 29 levels between two places on a page at 2x and 128 px; in one place the two draw identically
- D2-xxx | The self-test reads fixture families made from the October set and the approved option files in a temporary folder | It must run before, during and after the makers' work, and those files stay as the record (D2-718)
- D2-xxx | The look-alike check's masters are the set in use, `civic-line-v6/`, by default, and `--masters october` keeps the October set | D2-748; Board 6 measured the October masters, so the self-test still proves the port on them before it checks the set in use
- D2-xxx | All my builds, captures and check outputs went to the scratch folder; I did not rebuild any board page | The brief keeps scratch outputs out of `work/build` and boards untouched

## Questions for Dustin

None. Every call above sits inside DR-179, D2-634, DR-163 and the promotion brief.

## For the main session and other owners

- **Two density switches.** The pillar icons switch at 2x (above). The end mark (identity designer, Rule 04.6) shows its fit only at exactly 1x. On a 1.25x or 1.5x screen, then, a pillar icon draws its fit and the end mark its smooth drawing. Each follows its own drawing's evidence, and the end mark's is the identity designer's. If you want one rule across the guide, the identity designer can measure the end mark at 1.25x and 1.5x with the pixel-fit check (`--size 15,18` for the 12 px fit, and so on), and I would follow the figures. The shell's two classes work on any inline element, so the end mark could use them too.
- **Chapter 01's owner.** `s-01-pillars`, `s-01-21-correct` and `s-01-21-failure` still inline Civic Line masters; the build lists them as notes with the `<use>` to write. At 24 px the pillar row takes the pattern above.
- **Chapter 09 to 12 makers.** Use the patterns above. The build warns from chapter 09 on when a specimen inlines a drawing the sprite holds.
- **Utility hand.** When the first 16 px utility icon goes on a page, tell me and I add `oa.component.icon.utility.line.small` (1.5 px, 16-unit grid, round caps and joins) to the tokens in the same pass.
- **Main session.** Your snapshot commits through `e627d0ad` (04:00) hold my code as it stands now; only this notes file has changed since. I committed and pushed nothing.

## Tested

- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/promotion/engineer/guide.html`: figures above.
- `python3 -I work/build/scripts/phase-2/guide_build.py --self-test`: 12 of 12 scenarios, 108 of 108 expectations.
- `node work/build/scripts/phase-2/guide_check.js <scratch>/promotion/engineer/guide.html` at 1440, 1024, 390 and 360 px, on both builds: PASS, figures above.
- `node work/build/scripts/phase-2/guide_check.js --self-test --results <scratch>`: PASS, run twice (before and after the switch moved to 2x).
- `python3 -I work/build/tests/tokens/run_token_tests.py`: all six steps pass.
- `node work/build/scripts/phase-2/sprite_check.js` on the real finals, and on my fixture folders before the finals landed: PASS both times, every pair at 0.
- A planted fault in the sprite (root attributes left off): the sprite check fails utility icons at 220, then passes again with the code restored.
- `node work/build/scripts/phase-2/icon_pixel_fit_check.js --size 24 --weight 2` on the Menu final: pass at 1x and 2x.
- `node work/build/scripts/phase-2/icon_likeness_check.js --self-test`: all right on the October set and on the set in use. The default run on `utility/svg-24/`, and the same files with `--masters october`.
- The pixel-fit check at 30, 36, 42 and 48 px on the four masters and the four 24 px fits, for the switch's threshold (table above).
- In Chromium: the masthead's menu glyph at 390 and 360 px at 1x and at 390 px at 2x, in normal mode and in forced colors on dark and on light; its box measured, and its rows read from the captures. Looked at, enlarged three times: the bars show in every case. At 1024 and 1440 px the button is hidden, as before.
- Chromium keeps a literal SVG fill or stroke under forced colors and forces `currentColor`, measured on a probe page; `forcedGlyphs` relies on both.

## Not tested

- The 1x and 2x pattern on a real page: no chapter places a pillar icon at 24 px yet. The build self-test and the sprite check cover it on fixtures and on the real finals.
- A 1.25x screen for the pattern; the sprite check draws it at 1x, 1.5x and 2x. The 30 px pixel-fit figures stand in for it.
- Forced colors on Windows itself, Firefox, Safari, real phones and high-density screens; every density and forced colors run here is Chromium's emulation.
- `min-resolution` in browsers that do not support it, where both classes fall back to the fit (the `oa-at-2x` rule hides the master by default).
- Print. In print the media query normally matches, so a pillar icon would print the master; I did not print the page.
- The byte checks on the finals, and the look-alike check on the eight changed Civic Line drawings, belong to the makers, and I did not run them.
- The default build into the stage A board folder, which I did not run.

## Change log

Created:
- `work/build/scripts/phase-2/sprite_check.js`
- `work/handoffs/phase-2/20261110_Promotion-Engineer-Notes.md` (this file)

Modified:
- `work/build/scripts/phase-2/guide_build.py`: the three sprite families and their reading checks, symbols that carry their root's attributes, single-shape accents, the masthead's `<use>`, the 1x and 2x pattern check, the utility line token's comparison and reader, `--sprite-root` and `--sprite-sheet`, three new self-test scenarios and fixture families for every scenario
- `work/build/guide/shell/guide-shell.css`: the menu glyph's rule and its forced colors line, and the `oa-at-1x` and `oa-at-2x` switch
- `work/build/scripts/phase-2/guide_check.js`: `forcedGlyphs` reads a `<use>` glyph's paints, the run reports its `<use>` parts, and two new plants
- `work/build/scripts/phase-2/icon_likeness_check.js`: the set in use as its masters, `--masters october`, and a self-test over both sets (D2-748)
- `work/build/tests/tokens/20261106_Token-Test-Results.json`: rewritten by the token test run

Unchanged: `guide-shell.js`, the shell fixtures, every chapter file and specimen, every asset folder and every board. Nothing in `source/`, `work/ledger/` or `deliverables/`. Nothing committed or pushed.

Scratch outputs, all under `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/promotion/engineer/`: the built page and its report, the page check's results and captures, the sprite check's JSON, the pixel-fit outputs, the masthead captures, and the fixture families I tested against before the finals landed.
