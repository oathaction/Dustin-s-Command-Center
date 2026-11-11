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
| 7 | Strict build, sprite check, token tests and guide check on the makers' files | waiting for the systems designer's `s-10-*` and `s-11-14-failure` |

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

The shell needed no change: its `oa-at-1x` and `oa-at-2x` rules already switch any `<use>` at `min-resolution: 2dppx`.

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
- D2-xxx | The self-test's fixture families add the masters of all 41 from the October set, CL-075 from Housing option A with its new `data-id`, the 37 fits from the approved option files under their in-use names, DR-208's redraws, and the replaced files in `_archive/` folders, all in a temporary folder | The self-test must run before, during and after the makers' work; the approved files stay as the record

## Questions for Dustin

None. Every call above sits inside DR-136, DR-179, DR-207, DR-208, DR-209 and the promotion brief.

## For the main session and other owners

- **Systems designer.** The strict build on the tree as it stands warns 46 times, each a 24 px master of the 41 without the switch: `s-10-list-41` (37), `s-10-9-correct` (5), `s-10-4-correct` (2), `s-10-1-failure` (1) and `s-11-14-failure` (1). Each warning gives the two `<use>` to write. `s-10-1-failure` is a failure plate: if it shows the master at 24 px on purpose, `data-oa-res="fixed"` on its `<svg>` keeps it and silences the warning; if it shows something else, it takes the switch like the rest.
- **Identity designer.** `s-01-21-correct` now passes the switch check.

## Tested

(being filled in)

## Not tested

(being filled in)

## Change log

Created:
- `work/handoffs/phase-2/20261111_Promotion-C-Engineer-Notes.md` (this file)

Modified:
- `work/build/scripts/phase-2/guide_build.py`: the fourth family, no `_` folders, the list of 41 from the construction file, the fits' checks, the 1x and 2x check for all 41, four self-test scenarios and the fixtures they read
- `work/build/scripts/phase-2/guide_check.js`: the list of 41 from the construction file, `fitSwitch` at 1x and in two high-density runs, nine plants
- `work/build/scripts/phase-2/sprite_check.js`: the fourth family and the switch for all 41; build warnings count as failures
- `work/build/scripts/phase-2/icon_likeness_check.js`: the self-test's count follows the set in use

Unchanged: the shell, every chapter file, specimen, manifest and asset folder, every board. Nothing in `source/`, `work/ledger/` or `deliverables/`. Nothing committed or pushed.
