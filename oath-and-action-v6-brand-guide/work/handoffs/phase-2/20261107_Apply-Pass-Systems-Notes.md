# Apply pass, round one: systems designer

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the systems designer, working as maker under `.claude/agents/oa-design-director.md` and checked against `.claude/agents/oa-ux-accessibility-lead.md`, for `work/handoffs/phase-2/20261107_Apply-Pass-Brief.md`. Decisions applied: DR-108, DR-109, DR-110, DR-112, DR-119, DR-120, DR-121, DR-124 and DR-128, with D2-254, D2-301, D2-308, D2-324 and the creative director's two open tracker items on Board 6.

Open the page: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, chapter 11 (anchor `#icons`) and chapters 05 to 07.

## What I did, item by item

### 1. Chapter 11 opens (D2-324)

New script `work/build/scripts/phase-2/apply_systems_ch11.py` writes `work/build/guide/chapters/11-icons.json`, 20 specimens `s-11-*.html` and their entries in the shared manifest. Title Status and utility icons, part Symbols and graphics, the instruction line from the build's chapter list. One rule group, Trackers, with seven rules:

| Rule | Title | Correct | Failure |
|---|---|---|---|
| 11.1 | Follow every bill through six numbered steps with plain names. | A state bill and a federal bill at step 6, 1,024 px: Governor and President | The clerk's names (Introduced to Presented) |
| 11.2 | Draw each step's state as a shape, and say it in words. | The six states on step 4 at true size and twice size (readable list) | Six identical circles told apart by hue, with a grayscale copy |
| 11.3 | Say in words when a bill becomes law or stops. | H.1180 "Became law on April 2. It takes effect July 1."; S.2045 stopped at step 6 by a veto that stood | "Step 6 of 6: Law." on a bill that waits for the governor |
| 11.4 | Mark the one way to take part in red, on its own shape, beside its words. | A story card with the take-part mark on step 5, the second chamber's committee hearing | Red spent on progress as well as the take-part mark |
| 11.5 | Use numbered steps in lists and on story cards. | Five bills at 360 px on Newsprint, one stopped by a veto | Board 6's dots on a line, no numbers |
| 11.6 | Turn the same steps upright on a bill's own page. | H.4212's page at 360 px with the take-part box and the red ask | A stock stepper of checks and boxes |
| 11.7 | Size the marks for reading, and the targets for a thumb. | The four circle sizes and the 44 and 48 px targets (readable list) | 16 px circles, 9 px numbers, a 20 px link |

Extras: the six steps as a readable table after 11.1; the list at 360 px on Charcoal and at 1,024 px on both grounds after 11.5; the bill's page at 1,024 px on Newsprint and 360 px on Charcoal after 11.6.

- **Steps (DR-108, DR-128).** Filed, Hearing, Committee vote, First chamber, Second chamber, and step 6 named for the signer: Governor on a state bill, President on a federal bill. "Chamber" is defined in Rule 11.1. Step 5's line, in the table and on H.4212's page, says the second chamber's committee often holds a hearing of its own.
- **States.** Done (filled), Now (heavy ring), Not yet (fine ring), Never happened (slash, number kept), Stopped (filled square, line ends), You can take part now (the one working red). Signed reads as law in words only. Every state shows by shape; I checked the lists in grayscale on both grounds.
- **Lists and cards (DR-109).** Numbered steps at 360 and 1,024 px on Newsprint and Charcoal; a story card at 360 px. **Bill page.** The same marks as a vertical timeline, 28 px circles, with the take-part box and the ask button.
- **Creative director's items.** Take-part mark on step 5 (Rule 11.4's card); a stopped bill in every list (S.2045).
- **Illustrative (DR-97).** Every bill is invented, and each piece carries one label at its head.
- **Intro.** Says status marks for other records and utility icons "join the chapter as their own rule groups once they are drawn". I kept "stage B" off the page: a newcomer cannot follow it, and the sentence stays true after they land. No closing group block; the shell needs none.

Changes from Board 6's drawing: the badge's 1 px Charcoal keyline now sits inside its 11 px disc, as Rule 05.5 draws a keyline, with 1.5 px of the surface cut around it; every type size is on the scale (Board 6 set 16 px rows); the kicker is text only, because DR-112 puts a topic icon only beside its own word and CL-005 measured faint at 24 px.

### 2. Chapter 05

- **Rule 05.1 (DR-119).** "Every view keeps three limits": Newsprint 60 to 85 percent, one dark panel per section, red within 5 percent, signature red included. A second paragraph: the other fifth-edition shares set the balance across a body of work, and a single view may fall outside them. Spec label now "Dark panels in each section".
- **Rule 05.7 (DR-124).** Neither the old clause nor its idea was in the rule; I searched the chapter, its script and every `s-05-*` file. Board A's A12 card names 05.7, so its why gains a second paragraph with DR-124's three sentences word for word, led by "The same standard decides which charts run."
- **DR-121.** No text in chapters 05 to 07 puts the atlas on White. Rule 05.7 already says Newsprint.
- **Specimens.** None draws a grid kicker or a grid tracker. Prussian's job in `s-05-palette` and `s-05-2-correct` said "panels that hold a tracker"; a tracker carries the take-part red, and red never sits on Prussian, so it now says "panels that hold dates". `s-05-6-failure`'s card said "Tracker · State bills" with no steps; it is now "Explainer · State bills". `s-05-4-correct` keeps "Loading tracker", a words-and-outline state with no grid. Rule 05.4's failure caption now points to Rule 11.2.
- **Related chapters.** The build's default named chapter 08 for "content-type colors", a retired job. Chapter 05 now carries its own list, with 08 as the lockmark and 11 added.

### 3. Chapter 06

- **Rule 06.8 (DR-120).** The rule says "The body measure, 33.88 rem, holds about 65 characters of 17 px Inter, measured in Chromium", and so does its specification row. The plate's measured figures (65 to 66 on full lines, 64 on average) still print.
- `s-06-1-correct` and `s-06-2-correct` show "Download the lockmark" as sample interface text. No grid is drawn, and the lockmark stays a download, so I kept it.

### 4. Chapter 07

- `s-07-1-correct` and `s-07-1-failure` drew a "Tracker · City council" card with no tracker on it, only a kicker, headline and text. No grid was drawn. A Tracker card now carries numbered steps (Rule 11.5), so the kicker is "Act · How to take part", which fits its text about speaking before a budget vote. The alts say "story card".
- Chapter 07 carries its own related list; 08 is the lockmark's four fixed places.

### Build plumbing

- The brief names `work/build/guide/shell/manifest-systems.json`; the file lives at `work/build/guide/specimens/manifest-systems.json`, where `guide_build.py` reads it. I kept it there.
- `stage_a_systems_build.py final` now keeps manifest entries from chapters it does not write, so a rebuild of 05 to 07 keeps chapter 11's entries. `apply_systems_ch11.py` keeps every entry outside chapter 11 the same way.
- Rebuild order: `stage_a_systems_build.py probe --out-dir <scratch>`, `node stage_a_systems_capture.js <scratch>`, `stage_a_systems_build.py final --out-dir <scratch>`, then `apply_systems_ch11.py`. Either order works.

## Routine calls

- D2-xxx | Chapter 11's plates draw Board 6's Option B and Option D marks in tokens, with the take-part badge's 1 px Charcoal keyline inside its 11 px disc and 1.5 px of the surface cut around it | Rule 05.5 draws a keyline inside the mark, and the cut parts the disc from the ring at 24 px
- D2-xxx | Every type size in chapter 11's plates is on the scale: bill name 17 px, status and take-part lines 15, keys 14, step names and numbers 13 (14 in circles from 28 px), list titles H3 at 26 or 32, the card headline H4 at 20 | D2-254 and D2-301; Board 6's 16 px rows would fail the guide check
- D2-xxx | The list grows from Board 6's four bills to five, adding S.2045, stopped at step 6 by a veto that stood | The creative director's open item asks for one list with a stopped bill
- D2-xxx | The take-part mark on step 5 is shown on a story card (S.0412), and the lists keep one take-part bill | The creative director's other open item; one red row per list keeps the ask clear
- D2-xxx | The federal example is an invented bill, H.R. 3120, Passport wait times, beside a state bill, both at step 6 | DR-128 shown where the two names differ, at true size
- D2-xxx | Chapter 11's kickers are text only, "Tracker · State bills"; the bill page drops Board 6's CL-005 icon | DR-112, and the Board 6 notes found CL-005 faint at 24 px
- D2-xxx | Every failure plate in chapter 11 carries the "Failure case: do not publish" band | D2-308; each could pass for a real tracker
- D2-xxx | Rule 11.1's failure uses the clerk's step names and Rule 11.3's prints "Step 6 of 6: Law" | One fault a producer could make in each, and neither prints the nine retired stages the check rejects
- D2-xxx | Chapter 11's 1,024 px plates carry the True size / Fit to window switch | At 1440 px the chapter column holds about 867 px, so they scroll at true size by default; the switch shows them whole at 75 percent
- D2-xxx | Chapter 11's intro names the coming groups in plain words with no stage name, and the chapter ends with no placeholder group | D2-253; the shell needs no block, and the sentence stays true once the groups land
- D2-xxx | In chapter 11, dates, "N px" and "step N" carry a no-break space, and running lines set `text-wrap: pretty` | No date splits from its day and no line ends on one word at 360 px
- D2-xxx | Rules 11.1, 11.3, 11.5 and 11.6 cite "Design judgment, approved by our founder and editor in November 2026" | DR-108, DR-109 and DR-128 approved these choices; the basis says so in words (D2-253)
- D2-xxx | Prussian's job reads "panels that hold dates, an explainer or a set of figures" | A tracker carries the take-part red, and red never sits on Prussian (Rule 05.3)
- D2-xxx | Rule 05.7's why takes DR-124's wording as a second paragraph | Board A's A12 card names Rule 05.7; the old clause was not there, and this is where chapter 05 meets chart choice
- D2-xxx | The cards in `s-05-6-failure` and `s-07-1-*` change kicker from Tracker to Explainer and to Act · How to take part | A Tracker card now carries numbered steps (Rule 11.5); these plates teach contrast and spacing
- D2-xxx | Chapters 05 and 07 carry their own related chapter lists | The build's default reasons named content-type colors and sanctioned positions, both retired with the grid's codes
- D2-xxx | `stage_a_systems_build.py` keeps manifest entries from chapters it does not write | Chapter 11 shares `manifest-systems.json`

## Requests for other owners (the main session routes them)

- **Engineer.** (1) `RELATED_DEFAULT` for 05 and 07 still names chapter 08 for "the lever and content-type colors" and "the sanctioned positions"; my chapter files override both, but the defaults may want the same fix. (2) At stage B, consider tracker tokens (`oa.component.tracker.*`: circle sizes 24, 26, 28 and 30 px, line 2 and 1 px, badge 11 px) so builders can name them; Rule 11.7 cites `oa.size.target.*` and border widths for now.
- **Editor.** (1) Chapter 01's tracker card for H.R. 7008 can draw its steps with `steps_svg()` and `node()` in `apply_systems_ch11.py` (24 px circles on a card, status words "Step n of 6: Name.", step 6 President), so it matches Rule 11.5. (2) Round two copy edit of chapter 11 goes through `apply_systems_ch11.py`.
- **Identity designer.** Chapter 08's line sending readers to trackers can point to Rule 11.5; Rule 11.5's why says the lockmark "codes nothing (chapter 08)", matching DR-110.

## Questions for Dustin

None. Every change follows a decision he has made.

## Tested

- `python3 -I work/build/scripts/phase-2/apply_systems_ch11.py`: 7 rules, 20 specimens, 14 figures; every fragment through the systems checks (no heading or landmark, no dash, no literal color, no px font size, classes prefixed) and every chapter string through the copy check.
- `stage_a_systems_build.py` probe, capture and final: 23 rules, 53 specimens, 172 figures. Before my edits the same pipeline reproduced the committed chapter files and fragments byte for byte.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`: exit 0, 9 chapter files, 100 rules, 232 specimens. One warning, chapter 01's three intro paragraphs (the editor's file), cleared in the last run.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`: PASS at 1440, 1024, 390 and 360 px, 0 failures. My exemptions: `s-11-4-failure` (red, contrast), `s-11-7-failure` (size, scale), each a labeled failure with its reason in `notes`.
- By eye in Chromium: all of chapter 11 at 1440 px and 390 px, the state key, the story cards and the 360 px list at twice size, the fit switch on the 1,024 px bill page, and both 360 px lists in grayscale (every state tells apart by shape on both grounds).
- Rendered measurements in chapter 11's specimens at true size: links 44 px tall, ask buttons 48 px, step numbers 13 and 14 px (26 px in the twice-size key).
- Contrast from `tokens.json` (token set 6.0.0-gate2.3), written to `work/handoffs/phase-2/20261107_Apply-Pass-Systems-Ch11-Figures.json`: marks 13.29 to 1 on both grounds, Stone 4.29, Dim Newsprint 7.26, numbers ahead 5.49 and 7.26, Pillar Red 2.96 on Newsprint with a 13.29 keyline and 4.49 on Charcoal, White on Pillar Red 4.17; Verdigris against Stone 1.28, and 1.25 in grayscale.
- A scan of the rendered page: no "hold a tracker", no "Tracker · City council", and the new 05.1, 05.7 and 06.8 wording present once each. No em or en dash and none of the flagged words in chapter 11's file.

## Not tested

- Screen readers by ear; Safari, Firefox and real phones; print; forced colors (the stage keeps its colors by design); 200 percent text on the rendered chapter.
- No reader has seen the six steps or the marks; the reader check's second round (D2-323) covers them.
- Whether H.R. 3120 matches a real bill in some Congress. It carries the Illustrative label at the head of its piece.
- The chapter 11 tracker's live behavior (announcements, loading and empty states); chapters 17 and 18 own it, and the rules point there.

## Change log

Created:
- `work/build/scripts/phase-2/apply_systems_ch11.py` (an early copy is in the main session's snapshot commit `56f5c43`; this pass changed it since)
- `work/build/guide/chapters/11-icons.json`
- `work/build/guide/specimens/s-11-1-correct.html`, `s-11-1-failure.html`, `s-11-2-correct.html`, `s-11-2-failure.html`, `s-11-3-correct.html`, `s-11-3-failure.html`, `s-11-4-correct.html`, `s-11-4-failure.html`, `s-11-5-correct.html`, `s-11-5-failure.html`, `s-11-6-correct.html`, `s-11-6-failure.html`, `s-11-7-correct.html`, `s-11-7-failure.html`, `s-11-steps.html`, `s-11-list-360-charcoal.html`, `s-11-list-1024-newsprint.html`, `s-11-list-1024-charcoal.html`, `s-11-page-1024-newsprint.html`, `s-11-page-360-charcoal.html`
- `work/handoffs/phase-2/20261107_Apply-Pass-Systems-Ch11-Figures.json`
- `work/handoffs/phase-2/20261107_Apply-Pass-Systems-Notes.md` (this file)

Modified:
- `work/build/scripts/phase-2/stage_a_systems_build.py`, `stage_a_systems_ch05.py`, `stage_a_systems_ch06.py`, `stage_a_systems_ch07.py`
- `work/build/guide/chapters/05-color.json`, `06-type.json`, `07-layout.json` (written by the build)
- `work/build/guide/specimens/s-05-2-correct.html`, `s-05-6-failure.html`, `s-05-palette.html`, `s-07-1-correct.html`, `s-07-1-failure.html`, `manifest-systems.json` (written by the builds)
- `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json` (written by the build)
- `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report and check results, regenerated by the shared build and check as the brief asks

Probe pages, captures and scratch checks are in my session scratchpad. Nothing committed or pushed by me.
