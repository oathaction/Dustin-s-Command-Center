# Promotion C: engineer's notes

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261111_Promotion-Stage-C-Brief.md` (owner 3, "Engineer"). I read my role file, `CLAUDE.md`, the brief, my November 10 promotion notes, my round 0 notes, the round 1 brief, and the decision log entries DR-136, DR-179, DR-207 to DR-211 and D2-1235 to D2-1267. One message from the main session came in while I worked: `icon_likeness_check.js` is mine, and its self-test's count of 124 must follow the set in use. That is done (below).

This file was written early and grows as the work lands. I built and tested the code against fixtures first; the icon designer's folders landed while I worked, and every figure marked "real" ran on them.

## Status

| Item | What | Status |
|---|---|---|
| 1 | The sprite reads `civic-line-v6/fit-24/` as a fourth family, `oa-sym-<id>-24px` | done; reads the 37 real fits with no warning |
| 2 | DR-179's 1x and 2x check covers all 41 drawings on the list | done, in the build and, rendered, in the guide check |
| 3 | CL-075 Housing joins the Civic Line family, 48 px and up | done; 125 drawings read |
| 4 | The utility family reads `svg-16/` and never `utility/_archive/` | done; reads DR-208's Pause and Filter |
| 5 | Self-test, `sprite_check.js`, `guide_check.js` | done (figures below) |
| 6 | `icon_likeness_check.js --self-test` counts the set in use | done (main session's message) |
| 7 | Strict build, sprite check, token tests and guide check on the makers' files | done on the tree at c4ad5c7f: all pass (below) |

At the start of my pass the strict build of the tree as committed (f6004c6a) gave exit 0, no warnings, 6,812,168 bytes, 12 chapter files, 132 rules, 306 specimens; the build self-test gave 15 of 15 scenarios and 159 of 159 expectations.

## What changed

**Four families.** `guide_build.py` now reads, in this order: Civic Line from `civic-line-v6/black/` (125 drawings with CL-075 Housing), the pillar fits from `pillar-icons/` and below (8), the 37 fits from `civic-line-v6/fit-24/` (black edition only, `-Black.svg` and never `-Red-Black.svg`), and the utility icons from `utility/svg-24/` and `svg-16/` (36). A fit's symbol is `oa-sym-<id lowercased>-24px` (`oa-sym-cl-048-24px`, `oa-sym-r-06-24px`) and sits in its own hidden sprite, `data-sprite="fit-24"`. A fit draws as its file: its root's `shape-rendering="crispEdges"` rides on a group around the drawing, and its ink becomes `currentColor`, so it takes the page's ink and is one color. CL-075 needed no new code: the Civic Line family reads every `-Black.svg` with a `data-id`, and its accent group draws through `--oa-icon-accent` as every Civic Line accent does.

**No `_archive/` is read.** No family reads a file under a folder whose name starts with `_` (`_archive/`, `_templates/`), however deep it looks. The utility family reads only `svg-24/` and `svg-16/`, so the Pause and Filter files moved to `utility/_archive/svg-16/` (D2-1264) never reach the sprite, and the folder in use holds one file per icon and size.

**What the sprite refuses, each a warning, the file left out:** a fit for a drawing off the list of 41 (such as a CL-075 fit); a pillar icon's fit in `fit-24/`; a fit of a non-pillar drawing in `pillar-icons/`; a file sized other than its family's sizes (24 for `fit-24/`, 16 and 24 for the pillar and utility families). Also warnings: a 24 px fit whose master is missing from `civic-line-v6/black/`, so 2x screens would have nothing to draw; and a family folder that exists but lacks a fit the list puts in use ("civic-line-v6/fit-24 lacks 1 of the 37 fits in use: CL-072"). A missing folder stays a note.

**The list of 41 has one source.** The build reads it from `20261110_Stage-B-Ch10-Construction.md`, section 10, "The list, by ID", as chapter 10's generator does, and `guide_check.js` now reads the same lines instead of its own copy (B-3's `READS_AT_24`). If the file ever gives anything but 41 IDs with the four pillar icons, the build warns and switches only the drawings whose 24 px fits it reads; the guide check stops with a message.

**The 1x and 2x check for all 41 (DR-179, DR-209), in the page's markup.** The build reads each `<svg>` that draws a fit, a master of the 41 or the switch's classes:

- A master of the 41 in an `<svg>` 24 px wide with no switch is a warning: "CL-048 at 24 px draws its master on 1x screens; DR-209 gives 1x screens the fit", with the two `<use>` to write. A pillar icon's names DR-179.
- A 24 px fit standing alone is a warning, as before, now for all 41.
- Only the 41 switch: `oa-at-1x` on anything but a 24 px fit of the 41, and `oa-at-2x` on anything but a master of the 41, are each a warning. So the switch on CL-075, on a utility icon or on a drawing off the list fails.
- Each fit switches to its own master: the fit of CL-006 paired with the master of CL-010 is a warning.
- A fit drawn at a size other than its own (a 24 px fit in a 48 px `<svg>`) is a warning, unless the plate is marked `data-oa-res="fixed"`.
- Under 48 px a symbol is one color: `--oa-icon-accent` on a fit, or on a master of the 41 drawn under 48 px, is a warning, for topic and atlas symbols as for pillar icons (R10, D2-497, DR-136).
- `data-oa-res="fixed"` still exempts a plate that shows one drawing on every screen, such as a fit enlarged or a master at 24 px beside its fit.

The build reads the size from the `<svg>`'s `width` attribute, which every specimen writes. Where CSS sets the size instead, the guide check's new `fitSwitch` measures the drawn box (below). The 48 px floor itself, and CL-075 at 24 px, stay with the guide check's B-3 test, which skips pictures: failure plates show symbols at 16 px on purpose (`s-10-4-failure`, `s-09-3-failure`), so a markup warning there would fail the strict build on a correct plate.

**`guide_check.js`, a new test `fitSwitch`.** At every width, at 1x: each `<svg>` outside the sprites that draws one of the 41 at a drawn width of 24 px, or carries the switch's classes, must pair one 24 px fit of the 41 with its own master, the fit must show and the master must not, and a master of the 41 may not stand alone at 24 px. Then two more runs on high-density screens, 1440 px at 2x and 390 px at 3x, each a fresh page, where the master must show alone. This proves on the real page that no specimen's own style breaks the shell's switch, which the build cannot see. The summary line prints the counts.

**`sprite_check.js`.** It reads the fourth family, compares each fit through `<use>` with its file at 1x and 2x (black only; the fits have no red-black edition, D2-1132), and draws the switch for all 41 at 1x, 1.5x and 2x. A build warning while it reads the families now counts as a failure of the sprite check, so a fit missing from its folder fails it. The pattern lines print a count and the range of differences, with each wrong one named.

**`icon_likeness_check.js` (main session's message).** Its self-test asked for exactly 124 drawings in the set in use. It now asks that the inventory's rows, its distinct IDs and the black files in `civic-line-v6/black/` agree, and that each pair is measured once, so the count follows the set in use: 125 drawings, 7,750 pairs. CL-075 moves the set in use's lines a little: the 99th percentile (flag) from 0.9092 to 0.9091, the 95th (watch) from 0.8678 to 0.8672, the median from 0.7143 to 0.7113. The closest pair stays at 0.9644.

The shell's `oa-at-1x` and `oa-at-2x` rules already switch any `<use>` at `min-resolution: 2dppx`, so only their comment changed, to name the 41 and DR-209.

**What a reader sees.** On a 1x screen each 24 px drawing of the 41 is its fit, crisp on whole pixels and grown toward 22 px across; from 2x it is its master, smooth and a little smaller in its box, as the fits manifest says. I looked at `s-10-list-41` at 390 px at 1x and 2x, enlarged: the first six rows draw the fits at 1x and the masters at 2x, each in its row beside its word.

## The families in use

| Family | Folder read | Files read | Symbols (real) | Symbol id | Source |
|---|---|---|---|---|---|
| Civic Line | `work/build/assets/civic-line-v6/black/` | `*-Black.svg`, by root `data-id` | 125 | `oa-sym-<id>` | the set in use (D2-716), with CL-075 Housing (DR-207, D2-1262) |
| Pillar fits | `work/build/assets/pillar-icons/` and below, no `_` folder | `*-Black.svg`, not `*-Red-Black.svg`, by `data-id` and `data-size` | 8 | `oa-sym-<id>-16px`, `-24px` | DR-179 |
| 24 px fits | `work/build/assets/civic-line-v6/fit-24/` | `*-Black.svg`, not `*-Red-Black.svg`, by `data-id` and `data-size="24"` | 37 | `oa-sym-<id>-24px` | DR-209, D2-1265 |
| Utility icons | `work/build/assets/utility/svg-24/`, `svg-16/` | `*.svg`, by `data-icon` and `data-size` | 36 | `oa-sym-u-<name>-<size>px` | DR-161 to DR-178; Pause and Filter at 16 px from DR-208 |

Read on the real folders, the four families give 206 symbols and no warning or note from the sprite.

## The pattern specimen makers write, for all 41

```html
<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"
     data-icon="CL-048" data-icon-family="topic"><use class="oa-at-1x" href="#oa-sym-cl-048-24px"/><use class="oa-at-2x" href="#oa-sym-cl-048"/></svg>
```

`data-icon-family` is `topic` for a CL drawing, `atlas` for an R drawing and `pillar` for CL-019 to CL-022. No `--oa-icon-accent` under 48 px. A plate that shows one drawing on every screen on purpose puts `data-oa-res="fixed"` on its `<svg>`. CL-075 Housing draws at 48 px and up only, as any Civic Line master: `<svg viewBox="0 0 128 128" width="48" height="48" ...><use href="#oa-sym-cl-075"/></svg>`.

## Routine calls

- D2-xxx | The 37 fits form a fourth sprite family, read from `civic-line-v6/fit-24/`, black edition only, 24 px only, with symbols `oa-sym-<id>-24px` in their own sprite, `data-sprite="fit-24"` | The brief's folder and ids (D2-1265); the fits are one color (D2-1132)
- D2-xxx | No sprite family reads a file under a folder whose name starts with `_` | D2-1264 keeps replaced files in `_archive/`, and the sprite must never meet two files for one icon
- D2-xxx | The build and the guide check read the list of 41 from the construction file's section 10, the source chapter 10's generator reads; the guide check's own copy is gone | One list in three readers cannot drift; CL-075 stays off it (D2-1238, DR-207)
- D2-xxx | With no list of 41 to read, the build warns and switches only the drawings whose 24 px fits it reads; the guide check stops | The build never stops on content problems; a check with no list cannot judge sizes
- D2-xxx | The sprite leaves out, with a warning, a fit off the list, a pillar fit in `fit-24/`, a non-pillar fit in `pillar-icons/` and a file of another size | Only approved fits in their own folders reach a page
- D2-xxx | A family folder that lacks a fit the list puts in use, and a 24 px fit with no master for 2x screens, are warnings | DR-209 puts all 37 in use, and the switch needs both drawings
- D2-xxx | A master of the 41 at 24 px with no switch is a warning, and only the 41 switch, each fit to its own master | The brief's rule for DR-209, in DR-179's pattern
- D2-xxx | A fit drawn at a size other than its own is a warning unless its plate is marked `data-oa-res="fixed"` | A fit serves its own size only (the fits manifest, "Use each fit at 24 px only")
- D2-xxx | `--oa-icon-accent` on a topic or atlas symbol under 48 px is a warning, as on a pillar icon | Rule 10.4 sets the 41 at 24 px in one color; R10 and D2-497
- D2-xxx | The build reads the size from the `<svg>`'s width attribute; the guide check's `fitSwitch` measures the drawn box | Markup is what the build sees; CSS can size a glyph, which only the browser knows
- D2-xxx | The 48 px floor and CL-075 at 24 px stay with the guide check's B-3 test, not a build warning | Failure plates show symbols under 48 px on purpose, and B-3 already skips pictures
- D2-xxx | `fitSwitch` runs at 1x at every width and in two runs of its own, 1440 px at 2x and 390 px at 3x | The switch sits at `min-resolution: 2dppx`; a laptop at 2x and a phone at 3x are the screens most readers use above it
- D2-xxx | `sprite_check.js` compares the fits in black only and draws the switch for all 41; a build warning while it reads the families fails it | The fits have no red-black edition; a fit missing from its folder must not pass
- D2-xxx | `icon_likeness_check.js --self-test` asks that the inventory's rows, its IDs and the black files agree, in place of a fixed 124 | The count follows the set in use, 125 with CL-075 (main session's call)
- D2-xxx | The shell's comment on the switch names the 41 and DR-209; its rules stay as they were | One rule already switches any `<use>`
- D2-xxx | The self-test's fixture families add the masters of all 41 from the October set, CL-075 from Housing option A with its new `data-id`, the 37 fits from the approved option files under their in-use names, DR-208's redraws, and the replaced files in `_archive/` folders, all in a temporary folder | The self-test must run before, during and after the makers' work; the approved files stay as the record

## Questions for Dustin

None. Every call above sits inside DR-136, DR-179, DR-207, DR-208, DR-209 and the promotion brief.

## For the main session and other owners

- **Systems designer and identity designer.** When my check first ran on the tree, it found 47 drawings of the 41 at 24 px without the switch: `s-10-list-41` (37), `s-10-9-correct` (5), `s-10-4-correct` (2), `s-10-1-failure`, `s-11-14-failure` and `s-01-21-correct`. By c4ad5c7f each had moved to the switch, and the build warns on none. The page holds 77 switches, none marked `data-oa-res="fixed"`.
- **Chapters 17 and 18 (round 1).** The newest tree's strict build warns 35 times, every one in chapter 18: anatomy plates `s-18-NN-anatomy` not written yet, and code sets `c-18-masthead` and `c-18-location` with no files. Ten more code sets in `work/build/guide/code/` give a note each until a rule shows them. None of this is the promotion's.
- **Sprite weight.** All 206 symbols together weigh 374,957 bytes in a sprite (Civic Line 327,524, fits 30,164, utility 10,932, pillar 6,337), past the 0.35 MB the page budget gives sprites, but a page carries only what it references. Today's page carries 150 symbols in 210,685 bytes, up from 175,026 before the fits.

## Tested

All builds, captures and outputs went to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/promotion-c/engineer/`.

- **Strict build** of the tree at c4ad5c7f, with the icon designer's folders and the systems and identity designers' specimens on the switch: `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/strict/guide.html`, exit 0, no warnings, 6,868,870 bytes, 12 chapter files, 132 rules, 307 specimens. Four sprites on the page: Civic Line 69 symbols, fits 37, pillar 8, utility 36. Ten notes, each a chapter 18 code set no rule shows yet.
- **Chapters 01 to 12 with the shell's final comment**, built strict from a scratch copy of the chapter folder without 17 and 18: 6,869,033 bytes, 132 rules, 307 specimens; its only warnings are the 48 specimens chapters 17 and 18 list in their manifests, which no chapter places when those two are left out.
- **Build self-test**: 19 of 19 scenarios and 220 of 220 expectations (15 and 159 at the start). Four new scenarios, on fixture families in a temporary folder:
  - Four families: one sprite per family, four in all, after `<body>`; each referenced symbol once; a fit draws in `currentColor` with no ink, accent, id or comment of its file; CL-075's accent draws through `--oa-icon-accent`; the 16 px Pause and Filter are DR-208's redraws; nothing from `utility/_archive/` or `pillar-icons/_archive/` reaches the sprite.
  - The fits folder's faults: a fit off the list (CL-075), a pillar fit in `fit-24/`, a 16 px file, a second file, a fit whose master is missing (R-45) and a missing fit (CL-072) each give their warning; a red-black file is ignored; the page still builds with the fits that exist.
  - The switch for all 41: the right pattern for CL-048, R-06, CL-001 and a pillar icon gives no warning, nor does `data-oa-res="fixed"`, nor a master at 48 px; a master alone at 24 px (topic and pillar), a fit alone, a fit paired with another drawing's master, the classes on CL-025, CL-029, CL-075 and a utility icon, an accent on a fit and on a master under 48 px, a fit drawn at 48 px and a master on 2x screens only each give their warning.
  - No list of 41: a warning, and the drawings whose fits are read still switch.
- **Mutation test of the build's new checks**, run on in-memory copies of `guide_build.py` (nothing written to the tree): reading `_archive/` folders, skipping the 24 px master check, not reading `fit-24/`, no membership check, letting any master take `oa-at-2x`, no completeness check, and the accent check on fits only. The self-test fails on each of the seven.
- **`guide_check.js` on the strict page at 1440, 1024, 390 and 360 px**: PASS, 0 failures, 1,102 same-page links. `fitSwitch` finds 77 switches at each width, the fit shown in all 77 at 1x; in the high-density runs, 1440 px at 2x and 390 px at 3x, the master shown in all 77. axe-core 4.10.2 finds no violation at any width; 60 focus stops show a ring at 1440 and 390 px; `lightOnDark` reads 37,201 elements and none changes; `forcedGlyphs` reads 399 glyph parts at 1440 and 1024 px and 400 at 390 and 360 px, 281 and 282 of them through `<use>`, none erased; the phone menu opens, holds focus, closes by Escape and by Close and returns focus at 390 and 360 px. It took 4 minutes 50 seconds.
- **`guide_check.js --quick` on the chapters 01 to 12 page with the shell's final comment**, at 1440 and 390 px: PASS, 0 failures, 1,102 same-page links; `fitSwitch` finds 77 switches, the fit shown in all at 1x and the master in all at 2x (1440 px) and 3x (390 px).
- **`guide_check.js --self-test`**: PASS. The clean demo passes (with the two high-density runs), 97 of 97 planted faults are caught and 28 of 28 allowances stay quiet (round 0: 91 and 25). New plants: a master of the 41 at 24 px sized by CSS, which the build cannot see; a specimen style that shows both drawings at 1x; a specimen style that keeps the fit at 2x, which only the high-density run catches (its 1x run stays quiet); the switch on CL-075; a fit alone at 24 px; CL-075 at 24 px (B-3). New allowances: the pattern, with the fit shown at 1x and the master at 2x; a master at 24 px marked `data-oa-res="fixed"`; CL-075 at 48 px.
- **`sprite_check.js` on the real folders**, run twice (before and after the shell's comment changed): PASS. 206 symbols. Through `<use>` beside its file, every pair matches with a largest channel difference of 0 at 1x and 2x: Civic Line 250 black and 250 red-black pairs (48 and 128 px), pillar 8 and 8, fits 37, utility 36. The switch draws the fit alone for 41 of 41 at 1x and 1.5x (0 against the fit, 162 to 202 against the master) and the master alone for 41 of 41 at 2x (0 against the master, 202 to 203 against the fit).
- **Two plants in the sprite check**, from a scratch copy of the script: with the shell's switch left out of the page, 0 of 41 patterns draw right; with the fits' symbols shifted one unit, the fits differ from their files by 202. Both fail, as they should.
- **`icon_likeness_check.js --self-test`**: all right on the October set (7,381 pairs, Board 6's figures within 0.0000) and on the set in use (125 drawings in the inventory, 125 black files, 7,750 pairs; p50 0.7113, p95 0.8672, p99 0.9091, closest 0.9644).
- **Token tests** (`python3 -I work/build/tests/tokens/run_token_tests.py`): all six steps pass. 500 tokens; parity 620 `:root` properties and 0 failures; rules 0 failures; self-test 41 of 41 plants; Style Dictionary 5.8.0 agrees on 500; Chromium resolves 469 values with 0 failures.
- **Looked at**: `s-10-list-41`'s first six rows at 390 px at 1x and 2x, enlarged four times at one CSS scale; in each the 1x run shows the `oa-at-1x` `<use>` and hides the other, and the 2x run the reverse.

## Not tested

- The byte checks, pixel-fit checks and likeness check on the fits, CL-075 and the two utility files belong to the makers, and I did not run them. The sprite check proves each symbol draws as its file in use.
- A 1.25x or 1.75x screen; the sprite check draws the switch at 1x, 1.5x and 2x, and the guide check at 1x, 2x and 3x.
- `min-resolution` in a browser that lacks it, where both classes fall back to the fit.
- Forced colors on Windows itself, Firefox, Safari, real phones and real high-density screens; every density and forced colors run here is Chromium's emulation.
- Print. In print the media query normally matches, so the page would print the masters; I did not print it.
- A glyph a specimen sizes by CSS to 24 px inside a larger drawing, as one `<use>` with its own width among other shapes: `fitSwitch` measures each `<svg>`, so such a `<use>` passes unseen. None is on the page today.
- The full guide check on the newest tree with chapters 17 and 18 in it, which are still being written.
- The default build into the stage A board folder, which I did not run.

## Change log

Created:
- `work/handoffs/phase-2/20261111_Promotion-C-Engineer-Notes.md` (this file)

Modified:
- `work/build/scripts/phase-2/guide_build.py`: the fourth family, no `_` folders, the list of 41 from the construction file, the fits' checks, the 1x and 2x check for all 41, four self-test scenarios and the fixtures they read
- `work/build/scripts/phase-2/guide_check.js`: the list of 41 from the construction file, `fitSwitch` at 1x and in two high-density runs, nine plants
- `work/build/scripts/phase-2/sprite_check.js`: the fourth family and the switch for all 41; build warnings count as failures; a shorter pattern summary
- `work/build/scripts/phase-2/icon_likeness_check.js`: the self-test's count follows the set in use
- `work/build/guide/shell/guide-shell.css`: the switch's comment only
- `work/build/tests/tokens/20261106_Token-Test-Results.json`: rewritten by the token test run

Unchanged: `guide-shell.js`, every chapter file, specimen, manifest and asset folder, every board. Nothing in `source/`, `work/ledger/` or `deliverables/`. I committed and pushed nothing; the main session's snapshots from 95cf5f64 to 9c31a284 already hold my changes to `guide_build.py`, `guide_check.js`, `sprite_check.js` and `icon_likeness_check.js`; the shell's comment and this file's last lines are not yet committed.

Scratch outputs, all under `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/promotion-c/engineer/`: the built pages and their reports (`baseline/`, `strict/`, `scope/`, `final/`), the guide check's results and the self-test's, the sprite check's JSON, the sprite sheet, the mutation and plant scripts, and the captures in `look/`.
