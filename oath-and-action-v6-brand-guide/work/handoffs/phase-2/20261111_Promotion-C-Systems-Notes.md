# Promotion C: systems designer's notes, chapters 05, 10 and 11

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the systems designer (`oa-design-director`, checked against `oa-ux-accessibility-lead`), run as a subagent of the main session, as owner 4 of `20261111_Promotion-Stage-C-Brief.md`. I started this file before the work and added to it as each part landed.

I read my role file and the accessibility lead's, `CLAUDE.md`, the promotion brief, the stage C brief, the accessibility lead's inventory (section 5's faults and section 2.1's looks), the engineer's round 0 notes (the opener contract, `--oa-color-surface`, `--oa-color-field-ground`), chapter 10's construction notes, and the decision log from DR-195 on.

## Status

Done, in the brief's order: (a) F-4, (b) chapter 10's promotion, (c) chapter 10's opener, (d) F-1, F-2, F-3, F-5 and F-9. Every word and plate changed through its generator; no output was edited by hand.

## What changed

### (a) F-4: Rule 05.4's ten states, redrawn to DR-199

`s-05-4-correct`, through `stage_a_systems_ch05.py` (two steps, `probe` then `final`, with the capture between).

- **Error:** chapter 11's error mark from the sprite (`oa-sym-u-error-24px`), a circle holding an exclamation mark, drawn in the message's ink through `currentColor`; "Error:" and the fix; the Error Band; the red on a 4 px Pillar Red bar drawn as `border-left`. The retired red disc with Close's cross is gone (D2-1167).
- **Warning:** the utility warning mark (a triangle holding an exclamation mark) in the warning mark's ink, "Warning:" and a 4 px ink bar as a border.
- **Success:** the utility success mark (a check leaving an open circle) in Verdigris, then "Saved".
- **Selected:** the 4 px bar is a border now too (D2-1158 names selected bars), and its hand-drawn check became the utility selected check.
- Every mark sits in a 24 px column as Rule 11.15's messages do. The cue words, alt, caption ("the error mark draws in the text's ink, and its red is the 4 px bar"), the Selected and State bar specifications ("4 px, drawn as a border") and the builders line (draw a bar as a border, since forced colors removes an inset shadow) follow.
- **Also in chapter 05:** `s-05-3-corrective` drew its two error bars as inset shadows; both are borders now, which looks the same (D2-1158).

### (b) Chapter 10, after the icon designer's folders landed

Through `stage_b_ch10_build.py`, run once in full (sheets drawn and likeness measured on the 125 drawings in use), then with `--no-draw` in the chain.

- **The 125th row.** The build now expects 125 drawings (124 and CL-075 Housing); every count the chapter prints reads the inventory: 125 in the intro, "121 of the 125, CL-001 to CL-075" in Rule 10.1, 93 at the cap and 32 filling in Rule 10.3, 94 and 31 one-color tile rows in Rule 10.5, "94 of the 125" in Rule 10.4's reasons.
- **Rule 10.4, the switch for all 41 (DR-209).** A second paragraph defines a pixel fit and sets the switch in chapter 09's own words: the fit on screens under 2x, the master on 2x and denser, both in one svg; the fit in an image exported at 1x, the master at 2x or more and in print. New reasons, two new specifications (24 px by screen; exported image and print), the line specification (1 px in each fit), `civic-line-v6/fit-24/` in Files, and a builders line with the two-use svg.
- **Every 24 px drawing of the 41 takes the switch:** `s-10-list-41` (all 37), `s-10-4-correct` (the ladder's 24 px rung, now labeled "pixel fit, line 1 px", and the kicker), `s-10-1-failure` (CL-048 in the Downloads button), `s-10-9-correct` (the five look-alikes) and `s-11-14-failure` (CL-024 in Start over, through `apply_systems_ch11_ui.py`). Each is `<svg viewBox="0 0 24 24" ...><use class="oa-at-1x" href="#oa-sym-<id>-24px"/><use class="oa-at-2x" href="#oa-sym-<id>"/></svg>`. The `sym()` helper does it for any of the 41 at 24 px, so a new plate cannot miss it, and refuses an accent under 48 px.
- **CL-075 Housing joins the library** (`s-10-lib-03`, "25 drawings, CL-049 to CL-072 and CL-075"; only that contact sheet changed, the other four PNGs are byte for byte the same), with "Smallest size: 48 px" and no "Also at 24 px" tag. **Rule 10.6's words:** "A subject that no topic symbol names, such as Bill, takes its word alone. Housing has its own topic symbol from 48 px, and under 48 px it takes its word alone too, since it is not on Rule 10.4's list of 41." **Its lists:** `s-10-6-correct` gains Housing ("A topic set from 48 px only, so under 48 px its word stands alone"), and `s-10-6-failure` is now four drawings of homes with no words (CL-075, CL-053, CL-054, CL-063), with its caption and alt rewritten.
- **Rule 10.9.** Housing joins the house group (four drawings; the plate sets that group's words under its drawings so they keep their measure). R-06, R-41 and R-44 form a new group, "At 48 px and under, never two in one view" (D2-1237), in the rule, its reasons, a new specification and a new plate row at 48 px. The five look-alikes' row and reasons now give the fits' figures beside the masters'.
- **Words for CL-075.** The editor's label table holds 124 rows and is not mine, so CL-075's label and meaning sit in a new addendum in the table's own form, `20261111_Promotion-C-Ch10-Labels-Addendum.json`, which chapters 10 and 11 read only for a drawing the table does not hold. The meaning sentence is mine and waits for the editor (question 1 below).
- **The construction notes** (`20261110_Stage-B-Ch10-Construction.md`, my file) carry the same changes: 125 drawings, 93 and 32, 94 and 31, the switch for all 41, the two groups, and the new figures.

### (c) Chapter 10's opener (D2-1135)

`s-10-opener`, placed with `"opener": "s-10-opener"`, flowing with the column (no `width_px`). A strip from the library: Voting, Testify, Public records, Housing, Local news supply (Variable B2) and Congress's own experts (Reform R-13), each at 64 px in one color above its word, an atlas element with its typed chip. Six in one row from 44.5 rem, three a row from 22 rem, two on a phone and one at large text sizes, so no row is left with one drawing and no chip spills its column. R-01 and R-02 stay out (D2-958).

At 1440 by 900 the strip's drawings sit on the first screen (the frame starts 720 px down, the drawings near 820). At 390 by 844 the intro fills the first screen and the strip starts right under it, at 842 px, where the shell places any opener.

### (d) F-1, F-2, F-3, F-5 and F-9 in chapter 11's live specimens

Through `apply_systems_ch11_ui.py`.

- **F-1, roles that follow the theme (D2-1159).** `ui_css()` now reads only short names a surface class or the dark theme remaps: the ground is `--oa-color-surface`, a field or a panel one step from the ground is `--oa-color-field-ground`, the disabled label and edge are `--oa-component-button-disabled-label` and `-edge`. `marks_css()` reads the error, success and warning roles by short name, and the form's ask, its keyline and its yield read `--oa-component-button-ask-*` and `-primary-*`. On the guide's Newsprint stage every value resolves as before. On a Charcoal stage the error sits on the ground with its 4 px red bar and no band (D2-1160), and the ask's keyline drops away.
- **F-2, labels that wrap (D2-1155).** No label carries `white-space: nowrap`. The reader's and the stepper's two-button rows are `repeat(auto-fit, minmax(min(100%, 10rem), 1fr))`, two columns at 16 px text and one at 200 percent. The phone menu's bars keep each button whole (`flex: none`) and let the chapter name wrap beside it.
- **F-3, the outside-link mark held to the last word (D2-1156).** The no-wrap span holds the link's last word and the 16 px mark, never the whole quoted title.
- **F-5, the status line carries its advice (D2-1157).** With no match it reads "0 of 125 symbols. No symbol matches. Clear the search or the filters to see more." The count is bold and the advice regular, in the one `role="status"` line; the line under the hits now only counts what is not listed.
- **F-9, the search field.** `type="search"`, the browser's own clear button hidden in favor of ours, and Escape clears the text and keeps focus in the field. **The search landmark is not in the plate**: AX-S8 and the guide check's `specimenLandmarks` refuse any landmark role inside a stage, and the engineer's round 0 notes leave a landmark demo open for chapter 18. Rule 11.12's new builders line names it: "wrap the field, its filters and its status line in a search landmark, `<div role="search">`". See question 2.
- The library also reads its rows from the inventory in use with the addendum, so it searches all 125.

## Routine calls

The main session numbers these when it records them.

- D2-xxx | `stage_b_ch10_build.py` expects 125 drawings, and every count the chapter prints (125, 121, CL-075, 93 and 32, 94 and 31) reads the inventory in use | DR-207 puts CL-075 in the set in use, and the main session's message asked for it; counts typed by hand would drift at the next drawing
- D2-xxx | CL-075's label and meaning sit in an addendum in the editor's own form, read only where the editor's table lacks a row | The table is the editor's file; the build needs words for 125 drawings now, and the editor's words win the moment its table holds the row
- D2-xxx | The likeness figures are measured again on the 125 drawings in use (7,750 pairs; flag 0.9091, watch 0.8672), and the chapter prints them | The set changed; every printed figure rounds as before (0.91, 0.84, 0.79, 0.75, 0.69)
- D2-xxx | `--no-draw` stops when the stored sheets or likeness run no longer match the inventory, and asks for one full run | A stale sheet would show 124 drawings beside words for 125
- D2-xxx | The 37 at 24 px take the switch through `sym()`, which applies it to any of the 41 at 24 px and refuses an accent under 48 px | One helper for every plate, so no 24 px drawing of the 41 can miss the switch (DR-209, D2-1265)
- D2-xxx | `oa-at-1x` and `oa-at-2x` join the classes the specimen build never prefixes | The build prefixes every specimen class with `sx-`, which would have hidden the switch from the shell's stylesheet
- D2-xxx | Rule 10.4's switch words follow Rule 09.3's, including the exported image and print | One switch, one wording, in both chapters (DR-179, DR-209)
- D2-xxx | The 24 px rung of Rule 10.4's ladder reads "pixel fit, line 1 px" | At 1x the rung draws the fit, whose line is one whole pixel; the master's 0.63 px would be wrong there
- D2-xxx | Housing joins Rule 10.9's house group, which becomes four drawings | The subject a builder reaches for first; its likeness to the three is low (0.25 to 0.57), so the group stays a group of subjects, as the rule already says
- D2-xxx | R-06, R-41 and R-44 never share a view at 48 px or smaller | D2-1237 says "at small sizes"; R-41 and R-44 start at 48 px, so 48 px is where the three can meet, and their masters score 0.89 to 0.96 (R-06 and R-44 the closest pair in the set)
- D2-xxx | Rule 10.6's example of a subject with no drawing becomes Bill; Housing is named as a topic from 48 px that takes its word alone under 48 px | DR-207 gave Housing a drawing; DR-137 still leaves Bill without one
- D2-xxx | Rule 10.6's failure row shows four homes with no words (CL-075, CL-053, CL-054, CL-063) | With Housing in the set, four houses make the rule's point more sharply than three houses and a letter
- D2-xxx | The opener is six drawings, four topics and two atlas elements with chips, in one row from 44.5 rem, three from 22 rem, two on a phone and one at large text | Eight drawings left chips wider than their columns at 1440 px; 7 rem columns hold the longest chip on one line, and the steps leave no row with one drawing
- D2-xxx | The opener draws one color | A row with no current item goes one color (Rule 10.7)
- D2-xxx | In chapter 11's live specimens, the reader's page view and the stepper's step box take `--oa-color-field-ground` | They are panels one step from the ground, White on Newsprint and Prussian on Charcoal, the pairing the field ground uses; no role names a raised panel yet (question 3)
- D2-xxx | `s-05-3-corrective`'s two error bars become borders too | D2-1158 covers every state bar, and the plate is chapter 05's
- D2-xxx | The ten states' Selected row takes the utility selected check, and its bar becomes a border | D2-1158 names selected bars; the approved drawing replaces a hand-drawn check
- D2-xxx | The library's status line bolds the count and sets the advice in regular weight | A whole bold sentence read as a heading; the screen reader hears the same words
- D2-xxx | The reader's Fit width and Full size stay a pair of pressed buttons in this pass | D2-1151 and D2-1152 move them to a radio group with one pressed look at their owner's next pass; this pass carries the five routed faults, and neither fails WCAG today (inventory, F-6)

## Questions for Dustin

None that need him. Three for other owners, each with my recommendation:

1. **Editor: CL-075's words.** The addendum's label is "Housing" (the Civic Line word) and its meaning reads "An apartment block stands beside a smaller pitched-roof house on one ground line, for housing as a subject: the homes of every kind where people live." *Recommendation:* fold the row into `20261110_Stage-B-Ch10-Labels.json` as written or reworded; the builds take the table's row from then on.
2. **Engineer and accessibility lead: a search landmark in a live stage (F-9).** AX-S8 and `specimenLandmarks` refuse it, so the plate has no landmark and Rule 11.12's builders line names `<div role="search">`. *Recommendation:* show it where chapter 18's search code set runs, as the engineer's round 0 notes suggest (a set's live demo in its own frame), and leave chapter 11's plate as it is.
3. **Engineer: a role for a raised panel.** The reader's page and the stepper's step box borrow `--oa-color-field-ground`. *Recommendation:* keep that for now; if chapter 18 needs the same panel, a role such as `oa.color.surface.raised` with the same four pairings would name it.

Notes for other owners, no answer needed:
- **Chapter 18's words** say "0 of 124 symbols" and "5 of 124 symbols" (`18-components.json`, the search component); the library now holds 125.
- **Chapter 01** ("A subject that none of the 37 stands for, such as Housing, takes its word alone") stays true: Housing is not among the 37 that may sit in a kicker.
- **`icon_likeness_check.js --self-test`** expects 124 masters (the icon designer noted it); it is the engineer's file.
- **The chain rewrote two identity outputs** from the identity designer's own current scripts: `08-lockmark.json` (Rule 08.2's figures filled in) and `s-proofs-social.html`. I did not edit either.

## Tested

All in Chromium through Playwright on November 11, 2026, with outside requests blocked except Google Fonts where named. Scripts, captures and results are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/promotion-c/systems/`.

- **Reproducibility before any change:** the two-step chapter 05 to 07 build on the tree as found changed no chapter or specimen; only the measurement record's token version and date moved.
- **The generator chain** (V12's section 3) in order: every step ran. Mine changed only the files in the change log; the identity outputs above came from the identity designer's scripts.
- **Strict build** into my scratch folder: chapters 01 to 12 alone (`--chapters` and `--specimens` copies without the in-progress chapter 18 and its manifest), exit 0, 132 rules, 307 specimens, 0 warnings, 6.87 MB. With chapter 18 in the folder the build warns only on chapter 18's own pending files.
- **The switch:** in every `s-10-*` plate and `s-11-14-failure`, 46 svgs pair `oa-at-1x` and `oa-at-2x`; at device scale 1 all 46 show the fit and hide the master, at 2 all 46 do the reverse, and each `-24px` symbol is in the sprite. Captures of `s-10-list-41` at 1x and 2x show the fits and the masters.
- **The plates at 1440 and 390 px on Newsprint**, looked at: `s-05-4-correct`, `s-05-3-corrective`, `s-10-opener` (also 1024 and 360, and at 200 percent root text at 390), `s-10-4-correct`, `s-10-6-correct`, `s-10-6-failure`, `s-10-9-correct`, `s-10-list-41`, `s-10-lib-03`, `s-10-1-failure`, `s-11-14-failure`, and chapter 10's first screen at 1440 by 900 and 390 by 844. `s-05-4-correct` also under emulated forced colors (a picture, so it keeps its colors; its bars are now borders).
- **F-1 on a Charcoal stage** (the stage given `oa-surface-charcoal` and `data-oa-theme="dark"`), computed colors at 1440: in all six live specimens the ink on the ground measures 13.29 to 1; fields and panels draw Prussian, ink on them 9.42; button edges 13.29, the reader's unavailable button 7.26; the ask 4.17 (White on Pillar Red, 19 px bold). The form sent empty on Charcoal: no band (transparent), a 4 px Pillar Red bar, Newsprint ink. Captures of the reader, library, stepper and form on Charcoal looked at.
- **F-2 and F-3:** no button or link whose content spills its box, and no stage wider than its content, in the six live specimens at 320 px, at 200 percent root text in 390 and 360 px, and with WCAG 1.4.12's text spacing at 320 px. Captures at 200 percent show the reader's and the stepper's buttons stacked one to a row with whole labels, the menu's button whole, and each outside-link mark on the line of its last word.
- **F-5 and F-9:** the field's type is `search`; typing "zzzz" puts "0 of 125 symbols. No symbol matches. Clear the search or the filters to see more." in the status line and nothing in the line under it; Escape clears the field, keeps focus there and the status returns to "101 of 125 symbols"; "vot" gives "5 of 125 symbols" and "The first three are listed here, and two more match."
- **Likeness:** the engineer's check's own functions on the 125 drawings in use (7,750 pairs), as written in `20261110_Stage-B-Ch10-Figures.json`. The fits' figures are read from the icon designer's QA files, not rerun.
- **Guide check, quick (1440 and 390 px)** on my chapters 01 to 12 build: PASS, 0 failures, 132 rules, 307 specimens, 1,102 same-page links. Its fit switch check found 77 switches at each width; at 1x the fit showed in all 77, and at 2x (1440) and 3x (390) the master showed in all 77.
- **The generators are stable:** a second run of `apply_systems_ch11.py` and `stage_b_ch10_build.py --no-draw` left every chapter 10 and 11 output byte for byte the same.

## Not tested

- Any screen reader: the status line's words are what the live region holds, not speech heard.
- Real phones and real 2x screens (only Chromium's device scale emulation), Safari and Firefox. Firefox does not clear a search field on Escape by itself; the script does, but I did not run it there.
- Forced colors on chapter 11's live specimens after this pass: their borders, check and dashed edges are unchanged from the inventory's run, which I did not repeat.
- Page zoom at 200 percent (only the root text size was doubled), and print.
- The guide check at 1024 and 360 px, and the full four-width run; the engineer runs it.
- Whether readers can name Housing at 48 px or the fits at 24 px; no reader tests (DR-202).

## Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, any asset folder, any board, the committed chapters page or another owner's files was edited by me. Nothing committed or pushed (the main session committed snapshots while I worked).

**Created**
- `work/handoffs/phase-2/20261111_Promotion-C-Systems-Notes.md` (this file)
- `work/handoffs/phase-2/20261111_Promotion-C-Ch10-Labels-Addendum.json` (CL-075's words for the editor)
- `work/build/guide/specimens/s-10-opener.html` (generator output)

**Modified, generators and their data**
- `work/build/scripts/phase-2/stage_a_systems_ch05.py` (the ten states; the corrective plate's bars; Rule 05.4's words)
- `work/build/scripts/phase-2/stage_a_systems_build.py` (`oa-at-1x` and `oa-at-2x` kept unprefixed)
- `work/build/scripts/phase-2/stage_b_ch10_build.py` (125 drawings, the switch, Housing, the groups, the opener, Rule 10.4, 10.6 and 10.9's words)
- `work/build/scripts/phase-2/apply_systems_ch11_ui.py` (F-1, F-2, F-3, F-5, F-9; the library's 125; CL-024's switch; Rule 11.12's builders line)
- `work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md` (my construction notes, brought up to date)

**Modified, generator outputs**
- `work/build/guide/chapters/05-color.json`, `10-symbols.json`, `11-icons.json`
- `work/build/guide/specimens/s-05-3-corrective.html`, `s-05-4-correct.html`
- `work/build/guide/specimens/s-10-1-failure.html`, `s-10-4-correct.html`, `s-10-6-correct.html`, `s-10-6-failure.html`, `s-10-9-correct.html`, `s-10-lib-03.html`, `s-10-list-41.html`
- `work/build/guide/specimens/s-11-11-correct.html`, `s-11-11-failure.html`, `s-11-12-correct.html`, `s-11-12-failure.html`, `s-11-13-correct.html`, `s-11-13-failure.html`, `s-11-14-correct.html`, `s-11-14-failure.html`, `s-11-15-correct.html`, `s-11-15-failure.html`, `s-11-16-correct.html`, `s-11-16-failure.html`, `s-11-marks.html`, `s-11-menu.html`
- `work/build/guide/specimens/manifest-systems.json`
- `work/build/guide/specimens/img/20261110_Ch10-Library-03-Economy-Issues.png` (the other four sheets byte for byte the same)
- `work/handoffs/phase-2/20261110_Stage-B-Ch10-Figures.json`, `20261106_Stage-A-Systems-Measurements.json`, `20261110_Stage-B-Round-2-Ch11-Figures.json` (the tokens the specimens cite)

**Scratch, outside the repository** (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/promotion-c/systems/`): builds `build-1/` to `build-3/`, the chapter and specimen copies `ch-mine/` and `sp-mine/`, scripts `shot.js`, `clip.js`, `first.js`, `sw.js`, `live.js`, `look.js`, results `live.json` and `guide-check-quick.log`, and captures in `shots/` to `shots4/`.

## Editor's pass

November 11, after the main session logged my calls as D2-1278 to D2-1296. I applied the eight changes in section 1b of `20261111_Stage-C-Round-1-Editor-Notes.md` through my generators, with the two answers that bind them: D2-1343 (Rule 10.4 prints the two CSS lines that switch a fit for its master) and D2-1344 (Rule 11.12's search follows Rule 18.15's `search` element, with chapter 18 as its home). None of the eight had been applied before.

**What changed**
- `stage_a_systems_ch05.py`, Rule 05.4: the builders line defines forced colors at its first use in the editor's words (Rule 17.8's), and the caption reads "the error's red is its 4 px bar".
- `stage_b_ch10_build.py`: Rule 10.4's second builders line ends with the shell's two lines, `.oa-at-2x { display: none } @media (min-resolution: 2dppx) { .oa-at-1x { display: none } .oa-at-2x { display: inline } }`, for a builder to copy; Rule 10.6's caption takes semicolons; Rule 10.9's reasons read "sit further apart" and "the closest pair, Evidence with Oversight and enforcement, still scores 0.90" (the pair read from the icon designer's figures, not typed), and "the only one of the three"; `s-10-9-correct`'s alt lists a group of three or more with commas and a last "and".
- `apply_systems_ch11_ui.py`, Rule 11.12's builders line: the search landmark is the `<search>` element, "so a screen reader can jump straight to it, as Rule 18.15's code does", and a closing sentence names Rule 18.15 as the search's home. The shell links both mentions to `#rule-18-15`. The live plate still holds no landmark, since AX-S8 still binds specimens; the engineer's landmark swap serves code sets only.
- The editor's new meaning for CL-075 (D2-1334) was already in `s-10-lib-03` from the main session's rebuild; my run left that file as it was.

**Routine calls**
- D2-xxx | Rule 10.9's closest pair of fits is read from the icon designer's figures and stored in the figures file as `fits_closest` | The editor's sentence names the pair; a name typed by hand would go stale if the fits change
- D2-xxx | Rule 11.12's builders line ends "Rule 18.15 is the search's home, with every state and its code to copy." | D2-1344 asks Rule 11.12 to link to Rule 18.15 as the component's home; the editor's sentence names the rule for its markup only

**Tested**
- Chapters 05 to 07 rebuilt in two steps (probe, capture, final): only `05-color.json`'s two strings and the measurement record's date changed.
- The generator chain in order: my generators changed `05-color.json`, `10-symbols.json`, `11-icons.json`, `manifest-systems.json` (`s-10-9-correct`'s alt) and the chapter 10 figures file (`fits_closest`), and nothing else. Chapter 26 and chapter 18 files that show as changed in the tree are their owners' work in progress; the chain does not write them.
- Strict build of every chapter in the folder (01 to 12, 17, 18 and 26) into my scratch folder: 9,204,248 bytes, 15 chapter files, 176 rules, 402 specimens; exit 1 on 24 warnings, every one a missing chapter 18 anatomy specimen (`s-18-NN-anatomy.html`, Rules 18.1 to 18.24). No other warning.
- In that build, Rule 11.12's two mentions of Rule 18.15 link to `#rule-18-15`, which exists.

**Not tested**
- The guide check on this build (chapter 18 is still in progress); the words changed and no plate did.

**Change log**
- Modified: `work/build/scripts/phase-2/stage_a_systems_ch05.py`, `stage_b_ch10_build.py`, `apply_systems_ch11_ui.py`; their outputs `work/build/guide/chapters/05-color.json`, `10-symbols.json`, `11-icons.json`, `work/build/guide/specimens/manifest-systems.json`, `work/handoffs/phase-2/20261110_Stage-B-Ch10-Figures.json`, `20261106_Stage-A-Systems-Measurements.json` (date only); this file.
- Scratch: `build-4/` and `build-4.log`, `stagea-2/`.
