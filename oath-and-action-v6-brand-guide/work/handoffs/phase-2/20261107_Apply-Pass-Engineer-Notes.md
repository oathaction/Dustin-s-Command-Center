# Apply pass, round one: engineer's notes

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `work/handoffs/phase-2/20261107_Apply-Pass-Brief.md`, "Engineer". I read the brief, chapter 02's writing rules, the decision log from DR-93 to D2-329, board A's cards (A8 in full), the creative director's Board 6 review, my token notes and my shell notes. Board 6 has no engineer section, and the review asks nothing of the shell, build, checks or tokens.

At hand-back, `guide_build.py --strict` exits 0 with no warnings (9 chapter files, 100 rules, 232 specimens), and `guide_check.js` passes the page at 1440, 1024, 390 and 360 px with 0 failures, every new check included. The other makers kept editing while I worked, so the main session's final build is the one that counts.

## What I did, item by item

### 1. Chapter list

- **Chapter 08.** `CHAPTERS` now reads `("08", "lockmark", "The lockmark", "foundations", "Draw the lockmark from its master, and place it only in its four fixed places.")`. The line is the identity designer's, copied from `stage_a_identity_chapters.py`; the chapter file's own line wins on the page, as before.
- **No `signal-grid` left.** The build, the shell and the check hold no `signal-grid` anchor or "Signal Grid" name, apart from the rename fixtures in the build's self-test. V5's `#grid` alias now sits at the top of `#lockmark`. The appendix's Previous link and location line, which named `#signal-grid` and chapter 08, now follow the last chapter in the page. The Foundations part line ends "the page grid and the lockmark". Related reasons that named the grid's retired jobs changed: chapter 05 relates to 08 for "The lockmark and its red lever.", chapter 07 for "The four fixed places of the lockmark.", and chapter 08 relates to 03, 07, 11 and 14 (lockups, the page header and footer, trackers as numbered steps, the lockmark in a chart's footer). Chapter 08's file now sets its own list in any case.
- **Either file name during the pass.** A small map, `LEGACY_FILE`, let the build read `08-signal-grid.json` under its old name and anchor, with a note in place of a warning, while `08-lockmark.json` was missing. Once the new file existed, the old name became a warning. The identity designer's rename landed during my session, so I emptied the map: the finished build expects `08-lockmark.json`, and an `08-signal-grid.json` is now a warning. The mechanism stays, empty, for a later rename, and the self-test still proves it.
- **Chapter 11.** The page already took any later chapter that has a file. It now places chapter 11 under the Symbols and graphics opener, and that opener lists all four chapters of its part: 11 as a link with its instruction line, and 09, 10 and 12 as text with "Coming later". The contents, rail, part links and phone menu list 11; 09, 10 and 12 stay "Coming later" in the contents and get no section, as before. Chapter 08's Next link goes to 11, and 11's goes to the appendix.
- **Old 08 numbers fail the build.** Two checks, both build warnings, so `--strict` fails until each is fixed:
  1. Every citation in reader text ("Rule 05.2", "Rules 05.3 and 05.5", "Rules 08.4 to 08.8" with the range expanded, and links to `#rule-NN-n`) must name a rule its chapter holds, whenever that chapter's file is in the page. The build reads every chapter string, `proofs.json`, each placed specimen, and each placed specimen's alt, caption and label.
  2. Three sentences carried chapter 08 numbers before the rename (read from commit 3130c5b): "Rule 08.8 sets the grid and icon that may lead a kicker" (chapter 01), "The composer after Rule 08.9 builds only the combinations" (old chapter 08) and "40 px, bottom right, inside the margin (Rule 08.2)" (the social card proof). Each one warns while it survives as written, even where its number lands on a new rule by chance.
  At hand-back neither check finds anything: the editor and the identity designer had already changed those sentences.
- **Cover and colophon.** The page now names the chapters it holds, worked out from the files: the cover folio reads "Chapters 01 to 08 and 11", the page title "draft of chapters 01 to 08 and 11", and the colophon "Chapters 01 to 08 and 11, in draft, November 7, 2026, with an appendix of identity proofs." The draft date moved from November 6 to November 7.

### 2. Tokens (DR-120)

- `oa.layout.measure.bodyIdeal` keeps 33.88 rem. Its description now reads "Body measure: holds about 65 characters of 17 px Inter, measured in Chromium.", and its `chars` extension reads 65 (it said 68). A comment beside it gives DR-120 and the 64 to 66 measured on chapter 02's prose.
- The version moved from 6.0.0-gate2.2 to **6.0.0-gate2.3**, still marked pre-release. I rebuilt both files with `tokens_build.mjs` and ran the token tests (results under Tested).

### 3. Checks in `guide_check.js`

Each new check has planted faults in the self-test, and the one allowance has a plant that must stay quiet.

| Check | Fails on | Plants |
|---|---|---|
| `retiredWords` | "Signal Grid" in any case or spacing; "Stage n of 9" (digits or words); "nine stages"; "condensed width, proposed". It reads reader text, alt text, accessible names and the document title, failure plates included, since a failure plate can name its fault without the old name | in rule text; in a specimen alt; "Stage 4 of 9" in a caption; "nine stages" in a failure plate; "Condensed width, proposed" as a proof label |
| `retiredClasses` | any element with a class the stage A grid specimens used for a retired job: `oai-grid` (the coded grid), `oai-lg` (its key), `oai-st`, `oai-gl`, `oai-gl-d` (the nine-stage sheet and glossary), `oai-pulse` (grid states), `oai-comp`, `oai-compwrap` (the composer). Inside a labeled failure plate they are allowed and listed, since chapter 08 shows one retired use on purpose | a coded grid in a correct plate; the composer after a rule; a coded grid in a failure plate (must not be flagged) |
| `codes`, widened | "gate" in any case, as in "for the gate" (it read only "Gate"); "Board N" and "board A" to "F"; "stage A" to "stage C" | a lowercase "gate"; "Board 6" in a caption; "stage B" in a chapter intro |
| `partOrder` | a chapter that sits under another part's opener, or whose opener does not link to it | a chapter naming another part; an opener missing its chapter's link |
| `ruleRefs` | a citation of a rule the page does not hold, where that chapter's rules are in the page, in text or in alt text and names. It repeats the build's citation check on the rendered page | "Rule 01.9" when chapter 01 holds two rules; "Rules 01.1 to 01.4"; a citation in an alt |

The self-test catches 48 of 48 planted faults (33 from before, 15 new) and leaves the 1 allowed case alone. I also checked the self-test itself: it reports a plant with `expect: false` as "FLAGGED" if the check fires.

The check also removes its own captures for sections the page no longer holds, so `captures/` lost its two `signal-grid` images and shows only the current page.

On the page as it stood before the makers' changes, `retiredWords` found 76 hits and `retiredClasses` 65 elements, all in chapters 02 and 08 and the proofs. At hand-back both find 0, and the only retired classes on the page sit in chapter 08's failure plate `s-08-3-failure`, which is allowed.

### 4. Shell

- **Appendix (D2-328).** The shell's title is "Identity proofs", and its fallback line is "See today’s wordmark in use at actual size, and the new stacked lockup beside the one it replaces." `proofs.json` with any other title is a build warning. The contents entry now prints `proofs.json`'s own instruction line in place of the old fixed sentence about both widths. The rail label and the phone menu take the same title. On the built page they read "Identity proofs".
- **Part openers.** The Foundations opener no longer names the Signal Grid. The new "Coming later" entries in an opener are set in the H4 style in the surface's secondary ink (`.part-later`), which on Charcoal is Dim Newsprint at 7.26 to 1.
- **Cover and contents.** The cover named no grid or stages; its folio now follows the chapters held (item 1). The contents lists 11 with its line.
- **Condensed drawing (DR-115).** A placed specimen that draws from a condensed master is now a build warning. It found all six condensed proofs on the page before the pass and finds none now.
- `guide-shell.js` and the fixtures needed no change.

### 5. Build self-test

`python3 -I work/build/scripts/phase-2/guide_build.py --self-test` builds fixture chapters in a temporary folder and passes 7 of 7 scenarios and 39 of 39 expectations: the old file name alone (a warning now that the map is empty); a rename in progress (read with a note, old numbers valid); the renamed file with an old number (both warnings); both names present; citations by range, link, specimen, alt text and caption, plus the condensed drawing; chapter 11 under its opener with 09, 10 and 12 coming later and the appendix after it; and the appendix title. With the checks sabotaged in a scratch copy, the self-test failed as it should.

### 6. The systems designer's two requests

The coordinator routed both from `20261107_Apply-Pass-Systems-Notes.md` during the pass.

1. **Default reasons on links to chapter 08.** Done in item 1. The defaults for chapters 05 and 07 no longer name "the lever and content-type colors" or "the sanctioned positions". Chapters 05 and 07 now carry their own lists, so the defaults show only if a file drops its list.
2. **Tracker tokens.** My call is to add none in this pass and to define them at stage B, with the status marks. Three reasons:
   - The guide's own test ties tokens to the page that reads them (Master Brief section 21: a test fails when the guide and the token files disagree). Chapter 11's plates draw their sizes as SVG geometry in `apply_systems_ch11.py` (ring line widths of 3 and 1.5 px, radii worked out from the circle size, the 11 px disc and its 1.5 px cut). A token added now would have no reader, so the guide and the token could drift apart with no test to catch it.
   - Stage B draws the status marks with the same shapes: a filled mark for done, a heavy ring for now, a fine ring for ahead, a slash for never happened, a square for stopped. One set of mark tokens should serve both. A set named for the tracker today would likely be renamed in a few weeks.
   - The lines already have tokens, and chapter 11 cites them: `oa.border.width.rule` (2 px) and `oa.border.width.hairline` (1 px), with `oa.size.target.touch` and `oa.size.target.minimum` for targets. What lacks a name is the circle sizes (24, 26, 28 and 30 px by place), the ring weights (3 and 1.5 px), the slash and halo (2 px), the numbers (13 and 14 px) and the take-part disc (11 px, 1 px keyline, 1.5 px cut). Rule 11.7 states each one in words.

   For stage B I propose one family under `oa.component.mark`: sizes by place (`size.card`, `size.listPhone`, `size.page`, `size.listWide`), `ring.now` and `ring.ahead`, `line.reached` and `line.ahead` as aliases of the two border widths, `slash` and `halo`, and `takePart.disc`, `takePart.cut` and `takePart.keyline`, which aliases the ask button's keyline color. The plates would then read them through CSS, as `stroke-width: var(...)`, so the parity test covers them. Each token enters with a need in the register (condition 1 of the rule for adding a token), its use being Rules 11.5 to 11.7 and the stage B status marks.

## Routine calls

- D2-xxx | The build reads a chapter file under its old name, with a note, only while the new file is missing; once the new file exists the old name is a warning. The map held `08-signal-grid` during the pass and is empty since the rename landed | Other makers kept building through the rename, and the finished build expects `08-lockmark.json`
- D2-xxx | A citation of a rule its chapter does not hold is a build warning for every chapter in the page, and the three sentences that carried chapter 08's old numbers warn while they survive as written | D2-325: no old number may survive, including one that lands on a new rule by chance
- D2-xxx | `guide_check.js` repeats the citation check on the rendered page as `ruleRefs`, alt text included | The build reads raw files; the check reads what a reader meets
- D2-xxx | V5's `#grid` alias moves to `#lockmark`, and no `#signal-grid` alias is kept | D2-325: nothing has shipped, so no reader holds the old anchor
- D2-xxx | A part opener lists every chapter of its part, those not in the page as text with "Coming later" | Chapter 11 opens its part alone, and the reader sees where 09, 10 and 12 will sit
- D2-xxx | The appendix stays after the last chapter in the page; its location line and Previous link follow that chapter | An appendix closes the guide; with chapter 11 in the page it follows 11
- D2-xxx | The shell fixes the appendix title as "Identity proofs" and warns on any other; the contents takes `proofs.json`'s instruction line | D2-328
- D2-xxx | The cover folio, page title, description and colophon name the chapters the page holds, and the draft date moves to November 7, 2026 | The cover said "Foundations, chapters 01 to 08" with chapter 11 in the page
- D2-xxx | Related reasons for chapters 05, 07 and 08 drop the grid's retired jobs, and chapter 08 relates to 03, 07, 11 and 14 | DR-110
- D2-xxx | A placed specimen drawn from a condensed wordmark master is a build warning | DR-115 and D2-328: the condensed drawing leaves every page and stays only as files
- D2-xxx | The `codes` check reads "gate" in any case, "Board N", "board A" to "F" and "stage A" to "C" | Brief item 3's "Gate" wording, and the board and stage names are the same kind of studio word D2-253 bans
- D2-xxx | `retiredWords` fails "Signal Grid", "Stage n of 9", "nine stages" and "condensed width, proposed" everywhere, failure plates included | D2-326, DR-108 and DR-115; a failure plate can name its fault without the old name
- D2-xxx | `retiredClasses` fails the eight classes of the stage A grid specimens, except inside a failure plate | Chapter 08's failure plate shows one retired use on purpose, as the brief asks
- D2-xxx | `partOrder` fails a chapter outside its own part's opener or missing from its list | D2-324 puts a chapter in a second part for the first time
- D2-xxx | `guide_check.js` removes its own captures of sections the page no longer holds | Stale `signal-grid` captures would show a chapter that no longer exists
- D2-xxx | The body measure token reads "Body measure: holds about 65 characters of 17 px Inter, measured in Chromium.", with `chars` 65, at version 6.0.0-gate2.3 | DR-120
- D2-xxx | The tracker gets no tokens in this pass; stage B defines one family of mark tokens for trackers and status marks, read by the plates through CSS | A token with no reader escapes the guide-to-token parity test, and stage B's status marks share the tracker's shapes

## For makers

- New words to avoid on reader pages: "Signal Grid", "Stage n of 9", "nine stages", "condensed width, proposed", "gate" in any case, "Board 6", "board A", "stage B". Name the drawing the lockmark, and say "later" or "a coming section" in place of a stage name.
- The eight retired classes are listed above. A new specimen should not reuse them, except in a labeled failure plate.
- A citation such as "Rule 08.5" must name a rule its chapter holds. Run `python3 -I work/build/scripts/phase-2/guide_build.py --strict` to see any that do not.
- `work/handoffs/phase-2/20261106_Guide-Shell-Notes.md` now names `08-lockmark.json`, `#lockmark` and "Identity proofs" where it named the old ones, and points here.

## Requests to other owners

None open. During the pass the new checks found "Signal Grid" in chapter 02's source line and glossary (`s-02-14-pair`, `s-02-26-correct`, `s-02-lines`), "Rule 08.8" in Rule 01.21, "(Rule 08.2)" with 40 px in the social card proof, the condensed proofs and the old chapter 08. Each owner had fixed its own by hand-back.

## Questions for Dustin

None. Every item is a routine call inside the approved pass.

## Tested

- `python3 -I work/build/tests/tokens/run_token_tests.py`: all six steps pass. Build check: both files match the source, 485 tokens. Parity: 485 tokens, 605 `:root` properties, 90 short names in each of 4 surface classes, 0 failures. Rules: 485 tokens, 30 derived colors and tints, 201 semantic color cells, 0 failures. Self-test: 35 of 35 plants caught. Style Dictionary 5.8.0: 485 tokens read, 485 agree, 0 disagreements, the planted Stone change reported. Rendered in Chromium 153: 454 token values, 30 `color-mix()` derivations with a largest channel difference of 0, 360 nested short names, 14 type styles at 390 and 1440 px, 6 durations under reduced motion, 0 failures, the planted red leak reported.
- `tokens.json` holds the new description, `chars` 65 and version 6.0.0-gate2.3; `tokens.css` carries the version in its header.
- `python3 -I work/build/scripts/phase-2/guide_build.py --self-test`: 7 of 7 scenarios, 39 of 39 expectations, with the map empty; 36 of 36 earlier with the map holding `08-signal-grid`. A sabotaged copy (map emptied, fingerprints cleared, range expansion broken) failed 2 scenarios, as it should.
- `node work/build/scripts/phase-2/guide_check.js --self-test`: the clean demo passes at 1440 and 390 px, 48 of 48 planted faults caught, 1 of 1 allowed case left alone. Results: `work/boards/phase-2/stage-a/20261106_Guide-Check-Plant-Results.json`.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict` on the shared page at hand-back: exit 0, no warnings, 9 chapter files, 100 rules, 232 specimens.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px: PASS, 0 failures, axe-core 4.10.2 with no violations, focus rings on 60 stops at 1440. `retiredWords`, `retiredClasses`, `partOrder`, `ruleRefs` and `codes` all 0 at every width; `s-08-3-failure` listed as the one allowed use of a retired class.
- The same check on a scratch build of the sources as they stood early in the pass: it found the retired words and classes described above, and no `partOrder`, `ruleRefs` or `codes` fault. A scratch build with chapter 08 renamed and cut to three rules raised both citation warnings for Rule 01.21 and the fingerprint warning for the social card proof.
- Looked at, on the built page: the cover at 1440 and 390 px; the contents at 1440; the Symbols and graphics opener at 1440 and 390 (the 390 view in a phone viewport); chapter 11's head with the rail and local contents at 1440; the appendix head at 1440, with the rail hidden. Read by script: the chapter navigation from 07 to the appendix, the appendix location line, the page title, the folio and the colophon.

## Not tested

- A screen reader by ear, and browsers other than Chromium.
- Chapter 11 in captures: the check writes no capture for a section taller than 30,000 px, and chapter 11 runs 34,149 px at 1440 and 42,390 px at 390 (as do chapters 01, 02, 05 and 06, and more at 390). This limit is older than this pass.
- Print, forced colors and 200 percent zoom for the new "Coming later" entries in the part opener. Their colors come from the surface's secondary ink, which forced colors replace.
- The main session's final build and check, after round two.
- Whether the systems designer's or the identity designer's own build scripts still write any retired class name in a file I did not render; the check reads the page only.

## Change log

Created:
- `work/handoffs/phase-2/20261107_Apply-Pass-Engineer-Notes.md` (this file)

Modified:
- `work/build/scripts/phase-2/guide_build.py`: chapter 08, `LEGACY_FILE`, aliases, related reasons, part openers, appendix, cover and colophon scope, citation checks, the condensed warning, `--self-test`
- `work/build/scripts/phase-2/guide_check.js`: `retiredWords`, `retiredClasses`, `partOrder`, `ruleRefs`, the wider `codes`, 15 new plants and one allowance, the `#grid` alias on `#lockmark`, capture pruning
- `work/build/guide/shell/guide-shell.css`: `.part-later` and the part opener's "Coming later"
- `work/build/tokens/src/oa-tokens.src.mjs`; regenerated by `tokens_build.mjs`: `work/build/tokens/tokens.json`, `work/build/tokens/tokens.css`; regenerated by the tests: `work/build/tests/tokens/20261106_Token-Test-Results.json`
- `work/handoffs/phase-2/20261106_Guide-Shell-Notes.md`: sections 0, 2 and 7 name `08-lockmark.json`, `#lockmark` and "Identity proofs"
- Regenerated by the build and the checks: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, `20261106_Stage-A-Chapters-Build-Report.json`, `20261106_Stage-A-Chapters-Guide-Check-Results.json`, `20261106_Guide-Check-Plant-Results.json`, and `captures/` (refreshed, with `20261106_Stage-A-Chapters-1440-signal-grid.jpg` and `-390-signal-grid.jpg` removed)

Unchanged: `guide-shell.js`, the shell fixtures, `tokens_build.mjs` and the token tests. Nothing in `source/`, `work/ledger/`, the masters, any other owner's file or any existing board. Nothing committed or pushed.

## Fix pass

Written November 7, 2026, under `work/handoffs/phase-2/20261107_Apply-Pass-Fix-Brief.md`, "Engineer". I read the three reviews in full. At hand-back, `guide_build.py --strict` exits 0 with no warnings (9 chapter files, 100 rules, 233 specimens), and `guide_check.js` passes the page at 1440, 1024, 390 and 360 px with 0 failures. The other makers were still editing, so the main session's final run is the one that counts.

### Items

- **CD-N1, with CA-N11 (one Illustrative label).** The shell no longer adds the label to a caption when the piece itself shows the shell's label (`class="illus"`). It adds one only to a piece that shows none. DR-97's label at the head of the piece wins. Before the change, 73 plates carried the label twice; now none do. A new check, `illusOnce`, fails a plate with the label in both places.
- **CD-N2, with CA-N7 (the scroll hint).** It now reads "Wider than this column. Scroll the frame sideways to see all of it." That is true at every width.
- **CA-N8 (alignment).** In the part openers and the contents, a chapter's number now takes a fixed 36 px box with a 12 px gap. Its title, its instruction line, "Coming later" and a later chapter's name all start 48 px in, at 1440 and at 390 px. They were 31 and 50 px before. The appendix line in the contents now starts under its title. Chapter 09's name is item D2-415 below.
- **CA-N9 (the switch).** Every plate with a fixed width now carries the True size / Fit to window switch, hidden at first. The shell shows it only where the stage is wider than its frame and fitting it keeps the smallest text at 13 px or more. That floor is the rule CA-M1 set: Fit to window may never set type under 13 px. The four plates CA-N9 names all hold 13 px labels, and fitting would set them at 7 to 11.3 px, so they keep no switch and scroll at true size under the hint. Measured: `s-03-l6` would fit at 87 percent (11.3 px); `s-03-6-correct` at 54 percent (7 px); `s-08-1-correct` at 87 percent at 1024 px (11.3 px). `s-11-1-failure` now fits its frame at 1024 px, since the systems designer redrew it. On the page today the switch shows on `s-03-1-failure` at 1024, 390 and 360 px (its smallest text fits at 33 px or more), and on three drawings with no text at the phone widths. A manifest can still opt a plate out with `"fit_switch": false`.
- **CA-N10 (specification tables).** The label column is now 11rem wide in every rule from 30em, so values start on one edge down a chapter. Before, it ranged from about 120 to 250 px. Checked in Rules 08.2 and 11.5 at 1440 px: both start their values 177 px in.
- **D2-415 (chapter 09).** The chapter list names chapter 09 "Pillar icons". The Symbols and graphics part line reads "Pillar icons, topic symbols, status and utility icons, and the graphic devices that guide a reader.", and chapter 01's default related reason reads "The pillar icons." The anchor stays `pillar-marks`, as the architecture map set it, because chapter 09 has no file and no link to it reaches the page yet. Rename it when the chapter's file is first written at stage B. No "pillar mark" is left on the page or in any chapter or specimen file.
- **New check, `fitFloor`.** At every width it switches each plate whose switch shows to Fit to window. It then measures the smallest rendered text: HTML text times the fit scale, and SVG text at its drawn size. It fails any plate under 13 px, then sets the switch back. The self-test gives it one planted fault and two allowances. The fault is a 2,000 px plate with its switch forced to show, caught at 5.78 px. The first allowance is the same plate after a resize: the shell hides the switch, and the check stays quiet. The second is a 1,200 px plate set only in 48 px type: the shell offers the switch, fitting keeps the type at 34 px, and the check stays quiet. Each allowance also confirms whether the switch was offered, so the guard is proven in both directions.

### Routine calls

- D2-xxx | The shell adds an Illustrative label to a caption only when the piece shows none, and `illusOnce` fails a plate with both | DR-97: one label at the head of a wholly invented piece (CD-N1, CA-N11)
- D2-xxx | The scroll hint reads "Wider than this column." | The column is the limit at every width (CD-N2, CA-N7)
- D2-xxx | Every fixed-width plate carries the Fit to window switch, shown only where fitting keeps every text at 13 px or more | CA-N9 asks for the switch on wide plates, and CA-M1's floor rules out any fit that sets type under 13 px
- D2-xxx | `fitFloor` sets each offered switch to Fit to window and fails text rendered under 13 px | The fix brief's check, which also guards the shell's own rule
- D2-xxx | A chapter's number takes a 36 px box and a 12 px gap in the contents and the part openers | Titles, lines and later names start on one edge (CA-N8)
- D2-xxx | The specification tables' label column is 11rem in every rule | Values start on one edge down a chapter (CA-N10)
- D2-xxx | Chapter 09 keeps the anchor `pillar-marks` until its file is first written | No link to it reaches the page yet, and D2-415 renames the title

### Questions for Dustin

None.

### Tested

- `python3 -I work/build/scripts/phase-2/guide_build.py --self-test`: 8 of 8 scenarios and 46 of 46 expectations. The new scenario covers one label per plate, the switch on fixed-width plates only, the opt-out and the hint's words.
- `node work/build/scripts/phase-2/guide_check.js --self-test`: the clean demo passes, 50 of 50 planted faults are caught and 3 of 3 allowances stay quiet, with both switch allowances verified.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict` on the shared page: exit 0, no warnings.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px: PASS with 0 failures, including `fitFloor` and `illusOnce`.
- Measured by script: the four plates CA-N9 names (stage width, room, fit scale and smallest text); which plates show the switch at each width.
- Looked at: the Symbols and graphics opener at 1440 and 390 px; the contents at 1440; Rules 08.2 and 11.5's specification tables at 1440; `s-03-1-failure` with its switch at 390 px at twice size.

### Not tested

- Fit to window by keyboard and with a screen reader. The switch keeps the same buttons and pressed states as before.
- The switch at widths between the four the check uses, apart from what a resize recomputes.
- Print, forced colors and 200 percent text for the new alignment and the fixed label column.
- Firefox, Safari and real phones.

### Change log

Modified:
- `work/build/scripts/phase-2/guide_build.py`: chapter 09's name and the part line, the related reason, the switch on every fixed-width plate, the hint, one Illustrative label, and a new self-test scenario
- `work/build/scripts/phase-2/guide_check.js`: `fitFloor`, `illusOnce`, four new plants, and plant verification
- `work/build/guide/shell/guide-shell.js`: the switch is offered only where fitting keeps the 13 px floor
- `work/build/guide/shell/guide-shell.css`: the number box and gap in the contents and part openers, the appendix line, and the specification label column
- `work/handoffs/phase-2/20261107_Apply-Pass-Engineer-Notes.md` (this section)
- Regenerated by the build and the checks: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report, check results, `20261106_Guide-Check-Plant-Results.json` and `captures/`

Unchanged: the tokens and their tests, the fixtures, and every other owner's file. Nothing committed or pushed.

## Q1 to Q4 pass, CD-S9

Written November 8, 2026, in the `oa-engineer` role, run as a subagent of the main session, for the creative director's Should fix CD-S9 in `work/handoffs/phase-2/20261108_CD-Review-Of-Q1-To-Q4-Pass.md`. I changed the shell and the guide check. No chapter file, specimen or maker's build script changed, and `guide_build.py` needed no change.

At hand-back, `guide_build.py --strict` exits 0 with no warnings (9 chapter files, 100 rules, 233 specimens), and `guide_check.js` passes the page at 1440, 1024, 390 and 360 px with 0 failures, the two new checks included. The identity designer was editing chapters 03 and 08 while I worked, so the main session's final run is the one that counts.

### What I did

- **The shell.** From 48em a plate frame has 48 px sides. The script now finds each frame whose stage scrolls inside those sides and gives it the narrower sides of a new class, `.is-snug`: 32 px, the `oa.space.400` token. It keeps them only where the stage then fits whole, so the stage sits centered at true size. The hint, the tab stop and the "Scroll sideways" name already follow the frame's overflow, so a frame that now fits loses all three. A frame that fits today keeps its sides. A frame that still overflows at 32 px keeps 48 px and scrolls under its hint as before. Phones keep their 16 px sides, and the appendix keeps 24 px.
- **How the script measures.** It reads each stage's layout width at true size. A flowing stage that holds a wide table therefore counts as well as a fixed-width one, and a plate left at Fit to window is judged at true size. The script runs on load, when the fonts arrive and after each resize, before it decides whether to offer Fit to window. A plate that fits at 32 px never offers the switch, and one left at Fit to window goes back to true size.
- **Rule 08.2's places plate.** At 1440 px the frame is 866.7 px wide. With 32 px sides the 802 px plate has 802.7 px, so it sits whole with 32.3 px on each side, and it shows no hint, takes no tab stop and has no scroll name. At 1024 and 390 px it still scrolls under its hint, with a tab stop and its name.
- **Two new checks in `guide_check.js`,** read at true size before `fitFloor` runs:
  - `scrollHint` fails a frame that holds its stage whole yet shows the "Wider than this column" hint, a tab stop or a "Scroll sideways" name. It also fails a frame that scrolls without all three.
  - `frameFit` fails a frame that scrolls with sides over 32 px when 32 px sides would hold its stage. It also fails a stage in a frame that does not scroll when the stage sits more than 1 px off center or is drawn at other than its true size.
  - Six plants test them on the demo's 640 px sheet at 1440 px. The faults: the hint shown on the fitting sheet; a tab stop and scroll name on the same frame; a 2,000 px sheet that scrolls with its hint left hidden; the CD-S9 fault itself, a sheet 16 px too wide for 48 px sides with its frame held at 48 px; and the fitting sheet pushed off center by a 120 px left side. The allowance is the same 16 px case with the shell's own sides after a resize. It must stay quiet, and the run must show the frame at 32 px sides with no hint.

### Plates that change

A plate changes only where it scrolls today with 48 px sides and fits with 32 px. Every plate that fits today keeps its layout at every width I measured.

| Width | Plates that now sit whole with 32 px sides |
|---|---|
| 1440 | `s-08-2-correct`, Rule 08.2's places plate (802 px) |
| 1024 | `s-02-lines`, chapter 02's brand lines (a flowing stage whose content needs 638 px), and `s-03-1-failure` (610 px), which scrolled 4 px and offered Fit to window and now needs neither |
| 390 and 360 | None. Phone frames already have 16 px sides or less |

At other widths the same rule picks up other plates as the column changes. In a sweep from 768 to 1,920 px: `s-02-lines` and `s-03-1-failure` at 768; `s-04-5-correct` and `s-04-5-failure` at 800; `s-03-8-correct` at 900; `s-03-1-correct` at 1,100; `s-08-2-correct` at 1,280; and `s-06-8-failure` at 1,680 and 1,920. Nothing changes at 1,000, 1,180, 1,366 or 1,536 px. The shell notes' "Room at true size" now gives the new limits: 802 px at 1440, 638 px at 1024 and 640 px at 768.

### Routine calls

- D2-xxx | From 48em a plate frame takes 32 px sides only where its stage scrolls inside 48 px sides and fits whole inside 32 px ones | CD-S9; every plate that fits today keeps its layout
- D2-xxx | A frame whose stage still overflows at 32 px keeps its 48 px sides and scrolls | CD-S9 narrows the sides only where that makes a plate fit, so wide plates and their Fit to window scale stay as reviewed
- D2-xxx | The shell measures each stage's layout width in the page, so flowing stages qualify too | The review asks for a general fix, and `s-02-lines` overflows its frame at 1024 px the way a fixed-width plate does
- D2-xxx | The 32 px side is the `oa.space.400` token; phones and the appendix keep their own sides | Every space in the shell comes from a token, and those frames already have sides under 32 px
- D2-xxx | `scrollHint` fails a fitting frame with the hint, a tab stop or a "Scroll sideways" name, and a scrolling frame missing any of them | The hint, name and tab stop follow the frame's overflow both ways (CD-S9, AX-S3, AX-S12)
- D2-xxx | `frameFit` fails a frame that scrolls when 32 px sides would hold its stage, and a stage in a frame that does not scroll if it sits more than 1 px off center or off its true size | It guards the faults CD-S9 names: a needless scroll and an off-center plate

### Questions for Dustin

None.

### Tested

- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`, twice, the last after every shell change: exit 0, no warnings, 9 chapter files, 100 rules, 233 specimens. Outside the shell, the page differs from the build before mine only in its build stamp.
- `python3 -I work/build/scripts/phase-2/guide_build.py --self-test`: 8 of 8 scenarios, 46 of 46 expectations.
- `node work/build/scripts/phase-2/guide_check.js --self-test`: the clean demo passes, 55 of 55 planted faults are caught (50 before, 5 new) and 4 of 4 allowances stay quiet (3 before, 1 new). The new allowance's run shows the sheet at 32 px sides with no hint, and `scrollHint` quiet. The older `fitFloor` plant with a 2,000 px sheet and no resize now trips `scrollHint` too, as it should.
- The new checks on a copy of the page as built with the old shell: `frameFit` fails `s-08-2-correct` at 1440 px, and `s-02-lines` and `s-03-1-failure` at 1024 px, and nothing else. `scrollHint` finds nothing there, since the old shell's hints matched its overflow.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px: PASS with 0 failures, axe-core with no violations, and focus rings on 60 stops at 1440. Of 233 frames, 4, 17, 40 and 45 scroll at the four widths, and 1, 2, 0 and 0 take 32 px sides.
- `#rule-08-2` in Playwright Chromium at 1x. At 1440 px the plate sits whole, 32.3 px from each side of the frame, drawn 802 px wide with no transform; there is no hint, no tab stop, no group role or name, and no Fit to window switch. At 1024 px it scrolls 196 px with its hint, a tab stop and the name "Correct application, Rule 08.2, at true size. Scroll sideways to see all of it." At 390 px it scrolls 444 px the same way. I looked at captures of the plate at all three widths; the guide check's own capture is `work/boards/phase-2/stage-a/captures/20261106_Stage-A-Chapters-1440-lockmark.jpg`.
- Keyboard at 1024 px: the places frame takes focus, and two presses of the right arrow scroll it 80 px.
- Resizing one page from 1440 to 1024 to 390, setting `s-03-1-failure` to Fit to window, then to 1024 and 1440: the sides, hint, tab stop and switch followed each width, and the plate at Fit to window went back to true size at 1024, where it fits.
- A sweep of 13 widths from 768 to 1,920 px, old shell against new: no plate that fit before changed; every plate that changed now fits; on every plate the hint and tab stop match the overflow; and no stage in a frame that does not scroll sits off center or scaled.

### Not tested

- Forced colors, print and 200 percent text with the new sides. In forced colors the frame gains a 1 px border, which the script leaves out of the room it measures.
- Widths other than those listed, apart from what a resize recomputes, and a stage within a pixel of the 32 px limit, where the rounding of the frame's width decides.
- Firefox, Safari, real phones and a screen reader by ear.
- The main session's final build and check after the identity designer's edits.

### Change log

Modified:
- `work/build/guide/shell/guide-shell.js`: `snug()` and `sizeFrames()`, run on load, when fonts arrive and on resize
- `work/build/guide/shell/guide-shell.css`: `.plate-scroll.is-snug`, 32 px sides from 48em
- `work/build/scripts/phase-2/guide_check.js`: `frameAudit`, the `scrollHint` and `frameFit` checks, six plants and the header list
- `work/handoffs/phase-2/20261106_Guide-Shell-Notes.md`: one sentence in section 0's "Room at true size"
- `work/handoffs/phase-2/20261107_Apply-Pass-Engineer-Notes.md` (this section)
- Regenerated by the build and the checks: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report, check results, `20261106_Guide-Check-Plant-Results.json` and `captures/`

Unchanged: `guide_build.py`, the tokens and their tests, the fixtures, every chapter file and specimen, and every other owner's file. Nothing in `source/` or `work/ledger/`. Nothing committed or pushed.
