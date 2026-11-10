# Stage B round 2: systems designer's notes

Oath & Action Edition 06, Phase 2, stage B round 2, November 10, 2026. Written under `20261110_Stage-B-Round-2-Brief.md`. Two agents share this file under the same role file (D2-720): one for chapter 10 and then chapter 12's systems devices, one for chapter 11. Each keeps to its own section.

## Chapter 10

Written by the chapter 10 maker (`oa-design-director`, checked against `oa-ux-accessibility-lead`). This section grew as the work landed.

### Status

- **03:44 UTC: the construction file was done.** `work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md` holds the 128-unit box, the line, caps and joins, the red accent, the capped fit, the four editions and six tiles, the size floors and the list of 41 by ID with how it was decided. Chapters 09 and 11 can start from it. Its section 0 fixes chapter 10's rule numbers. Updated after the build: the printed rule titles, the tile counts from the inventory in use (30 drawings need 48 px on their own), the Civic Line hand's reading of the eight finals at 24 px, and the likeness figures in section 12.
- **Chapter 10 is built and checked** (sections below), with two failures in `guide_check.js` that other owners close: the list of 41 in B-3, and one word in the editor's sentence for CL-064.

### What I built

- **The chapter**, `work/build/guide/chapters/10-symbols.json`: 10 rules in five groups, five library extras after Rule 10.1 and the list of 41 after Rule 10.4.
  1. Find the right symbol: 10.1, the six kinds of symbol and their jobs (D2-515); then the library.
  2. How a drawing is built: 10.2, box, line, round ends and one red part; 10.3, the capped fit.
  3. Size and surface: 10.4, the 48 px floor and the list of 41; 10.5, editions and the six tiles.
  4. Words and red: 10.6, every symbol with its own word (DR-185); 10.7, red only alone or current (Rule 05.3, R11); 10.8, drawings only for atlas variables and reforms.
  5. Before you set it: 10.9, neighbors side by side with their likeness; 10.10, the atlas's encoding glyphs, copied from System 1.
- **26 specimens**, `work/build/guide/specimens/s-10-*.html`, with entries in `manifest-systems.json` (the s-10-* entries only; every other chapter's entry kept). Ten correct applications, ten failure cases (the four the brief names among them: a symbol at 16 px in 10.4, a symbol without its word in 10.6, red in a row on items that are not current in 10.7, a drawing used as a button in 10.1), the five library sheets and the list of 41.
- **The library.** Five contact sheet images by category, drawn from `civic-line-v6/black/` in Chromium at 128 px a drawing, kept to 16 colors, in `work/build/guide/specimens/img/20261110_Ch10-Library-0n-*.png` (124,850 bytes for all five). Each cell of the library grid draws its square of its sheet through `<use>` of one `<image>`, so the page carries each sheet once while every word stays live text that wraps on a phone. Each cell shows the drawing at 64 px, the editor's label, the ID, the typed chip for an atlas variable, and a 24 px tag on the 37 that may go to 24 px. Under each sheet a closed list (`<details>`, opened by the utility chevron and its words) holds every drawing's meaning sentence and smallest size.
- **The build**, `work/build/scripts/phase-2/stage_b_ch10_build.py`: reads the inventory in use, the editor's label table, the construction file's list of 41, the atlas model, System 1's build and the October rounded tile outline; draws the sheets; measures the likeness pairs with the engineer's own functions; writes the chapter, the specimens, the manifest entries and `work/handoffs/phase-2/20261110_Stage-B-Ch10-Figures.json` (every figure the chapter prints, and how). `--no-draw` reuses the sheets and figures.
- **Weight.** Chapter 10 weighs 0.62 MB against its 1.0 MB budget (618,190 bytes in the build report). The sprites part of the page is 0.14 MB.

### Routine calls

- D2-xxx | The list of 41 for 24 px is the trace review's section 6 list, unchanged, and none of the six redraws, CL-073 or CL-074 joins it | DR-136 approved "the 41"; the drawings board showed the eight new finals at 24 px as reference only (D2-673), and the Civic Line hand's inventory records all eight as not reading at 24 px
- D2-xxx | Of the 41, the four pillar icons draw from chapter 09's fits at 24 px, so 37 topic and atlas drawings may be set at 24 px, and a kicker's icon comes from those 37 | DR-179 and DR-112 keep the pillar icons to their own fits and out of kickers
- D2-xxx | Chapter 10's rule numbers are fixed in the construction file before the chapter is written | Chapters 09 and 11 cite them in parallel, and the shell links "Rule 10.n" only when the numbers hold
- D2-xxx | On Prussian a Civic Line drawing is one color in the ink token, with no accent token named | DR-09 sets the Newsprint edition alone on Prussian; the accent token's "White on Prussian" belongs to the identity marks
- D2-xxx | Each library cell draws its square of one category sheet with `<use>` of a single `<image>`, and the words beside it stay live text | D2-591 and D2-717 ask for contact sheet images; this way the page carries each sheet once (25 KB a sheet) and the words still wrap, search and read aloud
- D2-xxx | The library sheets are drawn in one color from the Black files | A sheet is a row of many drawings, and Rule 10.7 keeps a row one color; each red-black file places its own red, and Rules 10.2 and 10.7 show red in place
- D2-xxx | Each sheet's meanings sit in one closed list under it, opened by the chevron (DR-165) beside its words | 124 sentences open would add about 6,000 px at 1440 px; a closed list is one Tab stop a category (G-5) and keeps every sentence reachable as text
- D2-xxx | The library, the class table, the list of 41, the label pairs, the atlas list, the neighbors and the encoding key flow with the page; pieces shown at true size keep a width of 600 or 360 px | Lists reflow on a phone; a size ladder or a phone page has a true width to show
- D2-xxx | The encoding glyphs are drawn by importing System 1's `build_system.py` and calling its `wire_marks`, and shown on White, System 1's surface | The brief asks for System 1's constants exactly (DR-36); calling its code copies them with no retyping, and red on White measures 4.17 to 1, so the reform mark takes no keyline there
- D2-xxx | The likeness figures come from loading `icon_likeness_check.js` without its command line and reading the master pairs of the set in use with its own `inkMaps` and `corr` | The command line lists only pairs above its watch line, and Testify against Public meeting scores under every listing; the engineer's own functions give the figure the check would compute
- D2-xxx | Rule 10.9 calls the brief's groups neighbors and prints their outline likeness, and says plainly that most sit well under the flag | The figures run from −0.09 (Testify, Public meeting) to 0.84 (Court alignment, Local government) against a flag of 0.91; the risk is the subject a builder reaches for, so the rule asks for a look by subject at the size in use
- D2-xxx | The tiles in Rule 10.5 are drawn from the sprite in CL-031, with the rounded outline read from its October tile file | A `<use>` cannot cap each stroke the way the tile files do (D2-44); CL-031 takes optical scale 1.0, no offset and no cap, so the sprite draws its tile exactly
- D2-xxx | Newsprint tiles show on a Charcoal band in the plate | On a Newsprint stage their edge vanishes, and a White ground is the one Rule 10.5 rules out (1.41 to 1)
- D2-xxx | Rule 10.1's failure is CL-048 Public records on a Downloads button | Chapter 11 owns CL-024 as a refresh button (D2-515); the audit names CL-048 as the drawing a builder may grab for downloads (section 1.4)
- D2-xxx | Rule 10.2's failure is a stock "Bill" icon drawn for the plate, filled and square-cornered, in a row of Civic Line drawings | Bill has no drawing (DR-137), so it is the likeliest place for a stock icon to slip in
- D2-xxx | Rule 10.8's example is domain D02 with its six variables and the first two reforms whose targets touch them, read from the atlas model | The plate then prints the atlas's own membership, not a list I chose
- D2-xxx | The status mark in Rule 10.1's class table is drawn with its ring width from `oa.component.mark.ring.now` and class names apart from the tracker's | `markTokens` then measures chapter 11's marks only, and the example still reads its token
- D2-xxx | Encoding glyphs carry `data-icon="E-…"` and the status example `data-icon="S-now"`, each with its family | D2-517 asks every use to carry both; no ID scheme exists yet for those two families, and the checker reads the family
- D2-xxx | A number and its unit never part across a line: the build sets a no-break space in "24 px" and "128 units" in every string it writes | Short labels under drawings broke "24" from "px" at 1440 and 390 px

### Questions for Dustin

None. Every call above sits inside DR-136, DR-185 and the round 2 brief. If Dustin wants a drawing added to the 24 px list, that changes DR-136 and comes to him by name; I do not recommend it, since no new final reads at 24 px.

### Requests to other owners

- **Editor, `20261110_Stage-B-Ch10-Labels.json`, CL-064.** The meaning "A parcel meets a gate with two bars across it, …" fails `guide_check.js`'s `codes` test at every width, which fails the word "gate" in any reader text (D2-253). Recommendation: "a barrier" or "a bar across the road". I did not change it: the label table governs the words. Rebuild with `python3 -I work/build/scripts/phase-2/stage_b_ch10_build.py --no-draw`.
- **Editor, chapter 10's words.** My strings for the copy edit: the chapter file, the class table in `s-10-1-correct`, the six "what tells them apart" lines in `LOOKALIKES` (written from your meaning sentences), and every alt in the manifest. Send changes as a table and I apply them in the build script.
- **Engineer, B-3.** `guide_check.js`'s `READS_AT_24` is empty, so 37 drawings in `s-10-list-41` fail B-3 at every width. The 41 IDs are in the construction file, section 10. With a scratch copy of the check that holds them, B-3 passes at 1440 and 390 px. `REQUIRE_FAMILY` can go on for chapter 10: every icon use in it carries `data-icon-family`.
- **Engineer, tokens.** `oa.component.icon.accent.*`: `minSize` to `{oa.size.icon.large}` and the description to "at 48 px and up", since every Civic Line drawing is one color under 48 px (round 2 brief, D2-373, D2-497). The "White on Prussian" line does not hold for Civic Line drawings (DR-09).
- **Identity designer and editor, `s-01-21-correct`.** Rule 01.21's kicker sets CL-055 Productivity at 24 px; CL-055 is not among the 41, so B-3 fails it once the list is on. Recommendation: one of the 37 whose word fits an analysis kicker, such as CL-057 Workers' share of income or CL-060 Net support from taxes and public benefits, with the kicker's word changed to match.
- **Main session.** Two builds during my work stopped on chapter 11's work in progress: one strict build warned on chapter 11's weight (0.58 MB over 0.55 MB), and one failed reading an `s-11-*` file that the chapter 11 build was rewriting at that moment. My last strict build passed. The chapter 11 failures in the last check are listed under Tested.

### Tested

- `python3 -I work/build/scripts/phase-2/stage_b_ch10_build.py`: 10 rules, 26 specimens, 5 sheets; its own checks pass (no heading or landmark in a specimen, no dash, no literal color, no px font size, no straight quote, every specimen used once).
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`: chapter 10 adds no warning or note; chapter 10 weighs 618,190 bytes against 1,000,000.
- `node work/build/scripts/phase-2/guide_check.js <scratch>/guide.html` at 1440, 1024, 390 and 360 px. My first full run, before chapter 11's new specimens reached the page: 8 failures, all chapter 10's two open items above, `codes` at each width (CL-064's "gate") and `iconSizes` at each width (B-3's empty list); axe-core and every other test passed. My last full run, with chapter 11's work in progress in the page: 19 failures. Chapter 10's are the same two items. The other eleven come from chapter 11: text under contrast and one axe color-contrast item in `s-11-15-correct`, a sideways scroll of 370 px at 360 px, and a sideways scroll under text spacing at 390 and 360 px. I traced both scrolls by hiding one chapter at a time: each goes away only when chapter 11 is hidden. Exemptions listed for chapter 10: `s-10-5-failure` and `s-10-10-failure`, red, both labeled failures.
- `guide_build.py --strict` at my last run: exit 0, with two notes from chapter 11 (16 px utility icons without their line token, D2-577).
- The same check from a scratch copy with `READS_AT_24` holding the 41, `--quick` (1440 and 390 px): only the `codes` failure remains.
- Looked at every chapter 10 plate at 1440 and 390 px, and again at 2x, by capture: construction, sizes, tiles, the library grids and the list of 41 enlarged. Fixed from what I saw: labels in capitals and wrapped units, Newsprint tiles lost on the stage, crowded cells in the list of 41, leaders that crossed the drawing, a doubled title in the reform sheets.
- The library's closed list opened by keyboard (focus, then Enter): it opens, the chevron turns, the focus ring shows, 24 meanings for sheet 02.
- Grayscale capture of Rule 10.7's menu (the current item keeps its bold underline) and a forced colors capture, dark, of a library plate (the stage keeps its colors).
- The 41 compared by script with the trace review: identical. Cap counts against the inventory in use: 92 at the cap and 32 filling to 116 units, lines 2.6807 to 3.3508 units.
- Likeness pairs computed with the engineer's own functions on the 124 drawings in use: the pair distribution matches the check's own run (7,626 pairs, flag 0.9092 at the 99th percentile).

### Not tested

- A screen reader by ear, Firefox and Safari. `<use>` of an `<image>` inside another inline SVG and `@scope` are Chromium-tested only.
- Real screens at 1.25x and 1.5x, and print.
- Whether readers can name any drawing at 24 or 64 px; the list of 41 is one reviewer's reading, approved by Dustin.
- Forced colors and text spacing across every chapter 10 plate; the check's `forcedGlyphs`, `textSpacing` and `motion` ran and passed, and I looked at one plate.

### Change log

Created:
- `work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md`
- `work/handoffs/phase-2/20261110_Stage-B-Ch10-Figures.json`
- `work/handoffs/phase-2/20261110_Stage-B-Round-2-Systems-Notes.md` (this file; the chapter 11 maker adds its own section)
- `work/build/scripts/phase-2/stage_b_ch10_build.py`
- `work/build/guide/chapters/10-symbols.json`
- `work/build/guide/specimens/s-10-1-correct.html` to `s-10-10-failure.html` (20 files), `s-10-lib-01.html` to `s-10-lib-05.html`, `s-10-list-41.html`
- `work/build/guide/specimens/img/` with `20261110_Ch10-Library-01-Participation.png`, `-02-Government-Tech.png`, `-03-Economy-Issues.png`, `-04-Reforms-01-25.png`, `-05-Reforms-26-50.png`

Modified:
- `work/build/guide/specimens/manifest-systems.json`: the 26 s-10-* entries added; no other entry changed

Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/round-2/ch10/` (builds, captures, the scratch copy of the check).

Nothing in `source/`, `work/ledger/`, `deliverables/`, any asset folder, any board, the shell or another owner's script. Nothing committed or pushed.
