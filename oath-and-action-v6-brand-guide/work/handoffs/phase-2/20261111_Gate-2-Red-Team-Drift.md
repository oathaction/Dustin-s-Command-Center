# Gate 2 red team: drift across the 16 chapters

Oath & Action Edition 06, Phase 2, November 11, 2026. Task 2 of `20261111_Gate-2-Brief.md` (DR-226). Role: the design director as a reviewer, with the editor's eye for words. Page read: the frozen page `scratchpad/gate-2/review/guide.html`, SHA-256 605377d2…8b6154, 16 chapters, 185 rules, 424 specimens. The chapter data in `work/build/guide/` is unchanged since commit 043ad4d8, so the data and the page agree. Scripts and their output sit in `scratchpad/gate-2/drift/`.

## Score

**4 of 5.** The chapters read as one system: every rule reference resolves and says what it claims, every number agrees with the token, icon and WCAG data, every Atlas V7 ID is real, and the locked lines are exact; the drift that remains sits where stage C's later rules have not reached back into the guide's own shell, into stage A and B file lists, and into a dozen words and code comments.

## Must fix

**M1. Ten chapters print studio repository paths as each rule's "Files".**
- Where: chapters 01, 02, 03, 04, 05, 08, 09, 10, 11 and 12, the "Files" list under 49 rules (106 entries in the chapter data, 71 distinct paths, 190 list items on the page). Chapters 06, 07, 17, 18, 19 and 26 print none.
- What: the lists name internal files a reader cannot open, among them studio documents and build scripts: "work/handoffs/phase-2/20261106_Voice-Writing-Rules.md" (Rule 02.22), "work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py" (Rules 10.10 and 12.5), "work/boards/phase-2/data-viz/shared/20261106_Palette-Lab.json" (Rule 05.7), "work/extract/atlas-v7-data.json" (Rule 12.8), "work/build/scripts/phase-2/icon_likeness_check.js" (Rule 10.9), and "work/build/assets/civic-line-v6/20261110_Civic-Line-V6-Inventory.json" (six rules in chapter 10). The studio's own standard keeps these off the page: D2-253 ("Decision codes and internal document names leave every reader page") and D2-1098 (repository paths, "which the brief keeps off the page"). Chapter 05 also lists "work/build/tokens/tokens.css" under the note "Download buttons arrive with the asset package. Until then, ask the editor for any file listed here.", while the same chapter's builders block and Rule 26.8 already download that file.
- Why it blocks: it breaks a standard the studio set for every reader page, the brief's voice check names it, the paths would ship wrong (DR-184 moves the approved files to the asset package), and the guide now shows two conventions, one for stage A and B and one for stage C.
- Fix: list each asset by its file name alone, the name it will carry in the asset package, and drop every studio source (boards, handoffs, extract, scripts, inventories). Where a rule's only file is a studio source, remove the list. Point the token files to Rule 26.8's downloads, and keep D2-252's note only where no download exists yet.
- Owner: the engineer for `guide_build.py` (`FILES_NOTE` and the list renderer), with each chapter's owner for its `files` data in the generator scripts (`stage_a_systems_ch05.py`, `stage_b_ch10_build.py`, `stage_b_ch12_systems_build.py`, `guide_editor_ch02.py`, `apply_systems_ch11_ui.py` and the identity scripts for 03, 04, 08 and 09). Fix in the scripts, never in the chapter JSON alone.

## Should fix

Ordered by weight. Each fix goes into the generator or code file named, under the generator trap.

**S1. The guide's own shell draws hover, focus and the current place otherwise than Rules 17.9, 17.10 and 18.7.**
- Where: `work/build/guide/shell/guide-shell.css`, seen on every chapter: the 89 "Copy this chapter's properties" and code-panel Copy buttons (`.btn--quiet`), the 504 Copy buttons of the token table (`.tt-copy`, specimen `s-26-token-table`, Rule 26.7), the phone menu button (`.menubtn`), the scroll frames (`.plate-scroll`, `.code`, `.table-wrap`), the part navigation, the rail and the "In this chapter" list.
- What: the quiet buttons draw their edge and their hover as an inset shadow, `box-shadow: inset 0 0 0 …`, which Rule 17.9 forbids ("Hover never draws an inset shadow, which forced colors removes") and its failure plate `s-17-9-failure` shows. Chapter 18's own Copy components (`c-18-copy.css`, `c-18-code-block.css`) draw a real 1 px border that thickens to 2 px, so the guide shows one component two ways. The current part in the masthead takes the same underline as its hover and no bold (`.partnav a:hover, .partnav a[aria-current]`), where Rule 17.10 says "bold words, with a 2 px underline in a masthead". The rail's current link is semibold (600), where Rules 17.10 and 18.7 say bold. The "In this chapter" list marks its current item with an underline only, though Rule 18.7 names that very list: "A list beside the text marks it with the selected band, a 4 px bar at its left edge and bold words." The scroll frames take a Charcoal ring on the frame's edge with no gap, where Rule 18.11 draws the ring inside with its 2 px gap (offset −4 px) in the focus ring color.
- Fix: a 1 px border thickening to 2 px for every quiet control; current places per Rules 17.10 and 18.7; the scroll frames' ring as Rule 18.11 draws it, or one line in Rule 18.11 that names the guide's mat and its Charcoal ring.
- Owner: engineer (shell, token table builder `token_table_build.py`).

**S2. Chapter 18's tabs and location list draw the focus ring with no gap.**
- Where: Rules 18.7 and 18.9; `work/build/guide/code/c-18-tabs.css` and `c-18-location.css` (`outline-offset: calc(-1 * var(--oa-border-width-focus-ring))`), and the anatomy plates that draw the same ring (`.sx-kd[data-ax-focus]`).
- What: Rule 17.9 says "Focus draws a 2 px ring 2 px outside the control" and its specification reads "Focus gap: 2 px; never 0". These components put the ring on their own edge. Rule 18.11 shows the studio's answer for a control that cannot take an outside ring: inside, "its width and its 2 px gap in from the edge", offset −4 px. Builders copy this code (DR-203).
- Fix: offset −4 px with a comment that cites Rule 18.11, or the outside ring; if inside rings stay, add one sentence to Rule 17.9 that names the case.
- Owner: component engineer; systems designer for any words in Rule 17.9.

**S3. A warning is drawn three ways.**
- Where: Rule 18.18 and `c-18-messages.html`; Rule 17.8's plate `s-17-8-correct`; Rule 11.10, its plate `s-11-10-correct` and chapter 11's mark table `s-11-marks`; Rule 18.20's code `c-18-tracker.html`.
- What: Rule 18.18 says "A warning starts “Warning:” beside a 4 px bar in ink", and 17.8 and 18.18 print "Warning: Checked April 20. The agency may have acted since." Rule 11.10's words, its plate and chapter 18's tracker print the mark and "Checked April 20." or "Checked March 17. The committee may have acted since." with no first word. Chapter 11's mark table says "a 4 px Charcoal bar" where 17.8 and 18.18 say the bar is in the text's ink.
- Fix: add "Warning:" to the check-date notice in Rule 11.10, its plate and the tracker code, and say "a 4 px bar in the text's ink" in chapter 11's table. If the studio wants the bare form inside a tracker, Rule 18.18 names that exception instead.
- Owner: systems designer (chapter 11), component engineer (`c-18-tracker.html`), editor for the words.

**S4. The current item in a row of icons is drawn two ways at 48 px.**
- Where: Rule 09.2 and `s-09-2-correct`; Rule 10.7 and `s-10-7-correct`.
- What: Rule 09.2 underlines the current pillar's word "at every size" and sets it "bold under 48 px", so at 48 px the word is underlined and not bold. Rule 10.7's menu at the same size makes Testify's word "bold and underlined", and says "the red agrees with the bold, underlined word". Rule 17.10 gives a current link "bold words, with a 2 px underline".
- Fix: Rule 09.2 sets the current word bold at every size, as 10.7 and 17.10 do; the 48 px red stays the second sign.
- Owner: identity designer (chapter 09).

**S5. The selected band has three names, and its token describes a check that a list never draws.**
- Where: Rule 05.4's specification ("in a list, the paired surface and its 4 px bar"); the token `oa.color.state.selected.band.*`, shown in Rule 26.7's table ("Ground of a selected row or option: the paired surface. Pair it with the 4 px bar and a check glyph."); Rule 17.8 ("the band"); Rules 17.10 and 18.7 ("the selected band").
- What: one thing, named "paired surface", "band" and "selected band". The token's own name and the later rules say "selected band". Rule 17.10 marks a current place in a list with the band, the 4 px bar and bold words; the check belongs to toggles and choices.
- Fix: "the selected band" everywhere; the token description becomes "Ground of the current or selected row in a list. Pair it with the 4 px bar and bold words (Rule 17.10)."
- Owner: systems designer (`stage_a_systems_ch05.py`), engineer (`work/build/tokens/src/oa-tokens.src.mjs`).

**S6. Two more token descriptions disagree with the chapters.**
- Where: `oa.size.icon.medium` and `oa.color.action.ask.fill.onPrussian`, in `oa-tokens.src.mjs`, shown in Rule 26.7's table and shipped in tokens.json.
- What: the icon token says "one of the 41 topic symbols that read at this size". Rule 10.4 says "Four of the 41 are the pillar icons … so 37 topic and atlas symbols remain for 24 px". The ask fill on Prussian resolves to Newsprint, yet its description says "the second claim on the view's working red".
- Fix: "one of the 37 topic and atlas symbols on Rule 10.4's list"; for the Prussian ask fill, "Newsprint, since red never sits on Prussian (Rule 05.3)". Raise the pre-release number under Rule 26.8.
- Owner: engineer.

**S7. A stale reason in chapter 18's code.**
- Where: Rule 18.21, `work/build/guide/code/c-18-report-reader.css`, line 220.
- What: "an error sits under it, on the surface, since red never sits on the field ground's Prussian in the dark theme". Since round 2 the field ground on Charcoal is Charcoal (tokens.css line 111; Rule 26.8: "The field ground on Charcoal is now Charcoal").
- Fix: give the comment its current reason, or drop the clause.
- Owner: component engineer.

**S8. Reset has two naming rules.**
- Where: Rule 11.14's specification and chapter 11's utility table ("Reset or Start over, with its object, such as Reset the loop"); chapter 17's seven live players in `s-17-1-correct`, `s-17-4-correct`, `s-17-5-correct` (three), `s-17-hinge-correct` and `s-17-lever-correct`, and Rule 17.3's title.
- What: every chapter 17 player names its button "Reset" alone, with no accessible name beyond the word, so a screen reader that lists the page's buttons hears "Reset" seven times.
- Fix: name the object, such as "Reset the bill" or "Reset the lockmark", or let Rule 11.14 allow a bare "Reset" inside a named player group and say so.
- Owner: systems designer (`stage_c_ch17_build.py`), editor.

**S9. Chapter 11's words for a chip that is on lag behind its own plate.**
- Where: Rule 11.12 and its icon table.
- What: "Atlas is on, so it carries a check and a heavier outline" and "Inside a chip that is on, before its word, with a heavier outline". The plate's code draws the check, bold words and a 2 px edge, as Rule 17.10 sets.
- Fix: "a check, bold words and a 2 px edge (Rule 17.10)".
- Owner: systems designer (`apply_systems_ch11_ui.py`).

**S10. Rule 18.22 cites the wrong rule for the loop's pace.**
- Where: Rule 18.22, second paragraph.
- What: "it holds each step about 250 ms a word and never under six seconds, with reduced motion too (Rule 17.3)". Rule 17.3 sets Play, Pause and Reset; the pace is in Rule 11.14's specification.
- Fix: cite Rules 17.3 and 11.14, or give the pace its own sentence citing 11.14.
- Owner: accessibility lead (chapter 18's words).

**S11. Contrast ratios print in three forms.**
- Where: prose everywhere ("4.29 to 1"); plates in chapters 05 and 07 ("4.29:1"); the token table in Rule 26.7 ("3.1:1 on Charcoal", "1.8:1", "needs 3:1").
- What: every value is true against the tokens. The token table drops trailing zeros, so the same pair reads "3.10 to 1" in chapters 05 and 26's own prose and "3.1:1" in its table.
- Fix: two decimals everywhere; one form, "to 1", in prose and plates, or a one-line note that tables use the colon form.
- Owner: engineer (`token_table_build.py`), systems designer (05, 07).

**S12. Smaller names.**
- "Prussian blue" in three of chapter 01's failure descriptions (`s-01-2-failure`, `s-01-3-failure`, `s-01-5-failure`); the color is "Prussian" everywhere else. Owner: editor.
- "civic line" in lower case in Rule 19.8's results (`s-19-results`); "Civic Line" everywhere else. Owner: accessibility lead.
- Rule 18.14's copyable example labels "Download tokens.css" and saves `download="20261106_Oath-And-Action-Tokens.css"`, against its own rule, "Name each download for its file". The guide's real button is settled (D2-266, D2-964); only the example needs the saved name to match its label. Owner: component engineer.

**S13. Chapter 08's rule prose runs the longest sentences.**
- Where: Rule 08.2.
- What: three list sentences of 71, 76 and 77 words ("The lockmark signs four places, at the size each one sets: …"); 20 percent of chapter 08's rule sentences run past 30 words, against 5 to 13 percent in the other chapters. Chapter 02's W03 asks for varied length.
- Fix: break each list into a short lead sentence and the specification rows that already hold the sizes.
- Owner: editor, in the identity script for chapter 08.

## Questions for Dustin

None. No finding needs a settled decision changed.

## Tested

Every check below ran by script on the frozen page or its build data, with output in `scratchpad/gate-2/drift/`.

- **Text extraction** (`extract.py`): 19,382 text blocks, 1,979 links and 2,040 accessible names, alts and frame names, each with its chapter, rule and specimen.
- **Rule references** (`xref.py`): 1,929 mentions of "Rule NN.N" or "Rules NN.N to NN.N", in words, captions, accessible names and link texts, reach all 185 rules; none names a rule that does not exist, and all use one form. All 1,135 rule links land on the rule their words name. No same-page link is dead.
- **Claims against targets**: the 351 distinct sentences that cite a rule in another chapter, each read beside its target's title (`xsent.json`); 24 target rules printed in full (`showrule.py`) and more than 40 claims checked against their words (01.21 to 10.4, 09.2 to 05.3, 12.4 to 04.2, 08.3 and 11.1, 18.1 to 17.9 and 05.3, 18.20 to 11.2, 11.4 and 11.10, 18.22 to 11.14 and 17.3, 08.2 to 03.2 and 03.6, 12.6 to 10.10, 05.4 to 17.8 and 17.10, 04.6 and 09.3 both ways, 03.4 to 04.1 and 04.6, 12.2 to 05.6, 12.3 to 03.4 and 03.5, 11.16 to 05.3, 26.5 to 09.3 and 10.4, 26.6 to 18.4, 17.6 to 03.1 and 08.1, 11.11 to 17.10, 18.17 and 18.18 to 11.15 and 11.16, 19.6 to 07.6, and the token table to 05.3, 05.5, 17.7 and 18.5). One misattribution found (S10).
- **Chapter references**: every mention of a chapter not on the page (13 to 16, 20 to 25, 27, 28) is plain text or marked for later; none is a link.
- **Contrast** (`ratios.py`, `ratioscan.py`): all 45 pairs of the ten named colors and all pairs of the 37 token colors by WCAG 2.2's formula; each of 528 printed ratios matches a token pair to two decimals, except a failure plate's proposed second red (3.22, `s-26-2-failure`) and a faded button (2.61, Rule 26.4), which are not tokens by design. The page rounds to nearest, as WCAG allows when no pair sits at a threshold; Deep Stone on Dim Newsprint (2.999) is printed nowhere.
- **Counts**: 504 tokens and 13 categories in tokens.json and Rule 26.1; download sizes 95 KB and 284 KB against the files; 125 Civic Line drawings in the inventory (sheets of 26, 24, 25, 25, 25); Rule 10.4's list of 41 against `civic-line-v6/fit-24/` (37 fits) plus the four pillar icons; each contact sheet's "Also at 24 px" count (7, 7, 11, 9, 3) sums to 37; 94 and 31 drawings at 32 px sum to 125; 18 utility icons in the sprite; 185 rules and 424 specimens.
- **WCAG** (`20261111_WCAG22-Criteria-Text.json`): all 55 criteria's number, name, level and first 150 characters of words match; 31 at A, 24 at AA, six new; statuses 33 Met, 8 Met in part, 9 Gaps, 5 Not used today.
- **Atlas V7** (`atlas.py`): the typed IDs name 5 loops, all 50 reforms and 51 variables, and every one exists in the model; the 50 reform names in chapter 10 match the atlas titles except R-13 and R-36, set by DR-185, and an apostrophe; R-01's targets, R-32's, Loop R1's grade (plausible) and Loop R8's (well supported) match what the plates say.
- **Invented items**: every invented bill, request and agency rule keeps one title in every chapter (20 numbers); stages differ only as moments of one timeline. Every specimen holding an invented ID carries an Illustrative label; a scan for invented places and dated events found no unlabeled one.
- **Locked lines**: the tagline (22), mission (4), reader promise (4) and editorial commitment (14) are exact everywhere they appear; the pillars run in order in every list.
- **Plates against chapters 17, 18 and 26**: Rule 05.4's ten states against Rule 17.8's; every hex value in every specimen (only identity masters' own fills, printed token blocks and labeled failures); every focus and hover rule in the page's CSS; every current, selected and pressed state named in chapters 01 to 12; red beside Prussian in every sentence (only failures, White marks and a share figure); no token resolves to Pillar Red on Prussian.
- **Names**: color names and their variants; lockups, marks, hinge terms, end mark and sign-off; components (ask, primary and quiet buttons, take-part mark and disc, stepper and player, status line); edition names; studio codes (none on the page); file paths (M1).
- **Voice** (`voice.py`, 8,518 prose blocks): no em dash; the listed intensifiers, corporate verbs and hedges appear only as chapter 02's own examples; no numeric dates; hyphen-minus only in CSS values and a labeled failure; sentence length by chapter (mean 13.3 to 19.0 words).

**For the main session.** The brief says chapter 19 has "eight gaps owed by chapters 02, 16, 20 and 23". The page says nine, owed by chapters 02, 16, 18, 20 and 23; the ninth is 3.3.4 Error Prevention (Legal, Financial, Data), which chapter 18 owes. The page agrees with itself; the gate report should use its count.

## Not tested

- I did not render the page. Hover, focus and current-place findings come from the page's CSS, and the forced-colors effect of inset shadows is inferred from how browsers treat `box-shadow` there, not observed.
- I did not read all 8,518 prose blocks by eye. Voice was read by script, by chapter statistics and through the 351 citing sentences and 29 full rules.
- Words drawn inside raster images (photographs and PNG plates) were not checked.
- Print sizes (inches, millimeters, points) were compared only where they sit beside screen sizes, not converted against the masters.
- Bare IDs inside source lines (A4, A5, A6, X5, R-01 to R-12 in chapter 18's source) were checked for existence only. Of chapter 10's 125 meanings, only the reform names were checked against the atlas.
- Where a sentence names one color with its ratio (272 cases), the ratio matches a palette pair, but I did not confirm which surface each sentence meant.
- The guide check's own results (`redTouchesPrussian`, `fitSwitch`, `keyPath`) were not rerun; I relied on my word and token scans for red on Prussian.
- The Gate 2 preview and its new pages (Where to start, the font license, the edition line) were not built while I worked and were not read.

## Routine calls

- D2-xxx | The studio paths in ten chapters' Files lists go under Must fix | They break D2-253 and D2-1098's standard for every reader page, would ship wrong, and stage C already shows the page without them.
- D2-xxx | Invented bills shown at different stages in different chapters count as one timeline, not drift | Each number keeps one title, and its stages run forward in time, as H.99003 waits for the governor in Rule 11.1 and becomes law on April 2 in Rule 11.3.
- D2-xxx | Ratios that differ only in form (colon, one decimal) are one Should fix, not a numbers fault | Every value is true against the tokens.
- D2-xxx | The brief's count of chapter 19's gaps goes to the main session, not into the findings | The page's nine gaps agree with its own list of 55 criteria.
