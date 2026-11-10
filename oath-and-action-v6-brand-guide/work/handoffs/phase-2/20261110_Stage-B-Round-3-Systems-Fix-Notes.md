# Stage B round 3 fix pass: systems designer's notes

Oath & Action Edition 06, Phase 2, stage B round 3, November 10, 2026. Written by the systems designer (`oa-design-director`, checked against `oa-ux-accessibility-lead`) under `20261110_Stage-B-Round-3-Fix-Brief.md`, section "The systems designer", and the craft items it routes to me. A new agent took over the role for this pass and worked from the round 2 notes, the construction file and the stage A notes. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: done. Every item is applied in a generator: `stage_b_ch10_build.py` (chapter 10), `stage_b_ch12_systems_build.py` (Rules 12.5 to 12.9 and my sentence of chapter 12's intro), and `stage_a_systems_ch05.py` and `stage_a_systems_ch06.py` (chapters 05 and 06). No output file was edited by hand. Before I changed anything I reran all three builds unchanged and found their outputs byte for byte the same as the committed files, so the generators and the outputs agreed when I started.

To rebuild my chapters, in this order: `python3 -I work/build/scripts/phase-2/stage_a_systems_build.py probe --out-dir <scratch>`, `node work/build/scripts/phase-2/stage_a_systems_capture.js <scratch>`, `python3 -I work/build/scripts/phase-2/stage_a_systems_build.py final --out-dir <scratch>`, then `python3 -I work/build/scripts/phase-2/stage_b_ch10_build.py --no-draw`, then `python3 -I work/build/scripts/phase-2/stage_b_ch12_systems_build.py` (before the identity designer's chapter 12 script). `--no-draw` now measures any likeness pair the chapter needs and lacks, and adds only those pairs.

## For the editor

**PP-S3, final.** Rule 10.6 now carries, as its second paragraph:

> A subject that no topic symbol names, such as Housing, takes its word alone. An atlas drawing appears only beside the atlas’s own name, never beside a piece’s own topic word.

It takes your example, Housing, and DR-196's verb, so Rule 01.21's "A subject that none of the 37 stands for, such as Housing, takes its word alone." agrees with it. Rule 01.21 may add the second sentence if you want the atlas half there too.

**CA-S7.** Your three rows for Rule 10.2 (title, `rule[0]` from its third sentence, spec "Red") are in `stage_b_ch10_build.py` word for word.

**Strings for your read after the pass (D2-963).** Every changed string is in the generators at the places named in "Items" below. New sentences of mine: Rule 10.1's last sentence; Rule 10.4's why, second sentence; Rule 10.5's second and third paragraphs and two specs; Rule 10.6's chip sentence, the PP-S3 paragraph, the caption's second sentence and two spec rows; Rule 10.7's row sentence; Rule 10.8's first rule sentence, caption and "Order" spec; Rule 10.9's look-alike paragraph, the why's second paragraph, the caption's last clause and a spec row; Rule 10.10's rule paragraph; group lines 2 and 3; Rule 12.5's gloss of "connection"; Rule 12.6's measure line definition, caption sentence and "Grade marks" spec; Rule 12.7's "State locator" spec and caption; the corrective caption sentence and one spec value in Rule 05.3; the text inside `s-10-9-correct`'s new group, the library header line, and every alt named below.

## Items and what I did

| # | Item | What I did |
|---|---|---|
| 1 | ED 4e, Rule 10.2's caption | "with its keylines," is gone; the caption reads "…at three times its master, with the guide lines that place it, then at 128, 64 and 48 px." |
| 1 | ED 4c and 4e, Rules 12.5 to 12.9 and the intro | All open rows applied: my intro sentence names the marker's job ("the intervention marker, which shows where a reform acts,"); Rule 12.5 "at a heavier weight", "variable" for "condition" in the rule and the "Target weight" spec, and the caption naming Reform R-01 and Loop R10; Rule 12.7's quoted question and "Draw the locator in ink, with no red."; the layer diagram's core plane prints Wealth, Voice, Elections, Checks, Policy, Outside forces (read from the atlas parts' plain names) in the plate and the alt; Rule 12.9 "deadline" in the rule, caption, both handoff specs and both alts. |
| 2 | D2-950, IDs that break | Every drawing ID in visible text in chapter 10 and Rules 12.5 to 12.9 takes U+2011 between its letters and number, in the chapter strings and in the specimen text: Rule 10.4's 24 px row, the list of 41, the library, chips such as Reform R‑01. Alt text and anything inside `<code>` keep the plain hyphen. The 24 px row no longer splits "CL-" from "028" (captured at 1440 px). |
| 3 | Failure alts | All 21 banded failure plates in chapters 05 (five), 06 (one), 10 (ten) and Rules 12.5 to 12.9 (five) now open "Failure case: do not publish." `s-05-7-failure`'s alt, which began "A band across the top reads…", opens the same way. Checked by script. |
| 4 | D2-881, D2-959, `s-05-3-corrective` | The error mark is chapter 11's `U-error` from the sprite at 24 px, in the message's ink (`currentColor`, the error text token, Charcoal), with the 4 px Pillar Red bar on the field and the message, and 12 px clear of the bar, as Rule 11.15 builds it. Alt, notes, Rule 05.3's corrective caption ("The red is the 4 px bar beside the field and the message, and the error mark draws in the text’s ink (Rule 11.15).") and the spec "Working red, first claim" follow. |
| 5 | BE-M1, D2-958, Rule 10.8 | The plate lists all 10 reforms V7 aims at D02's six variables, in V7's order (R-01, R-02, R-03, R-05, R-06, R-07, R-34, R-45, R-46, R-47), each drawn at 48 px with its name and chip, under "The 10 reforms that act on them". They fit the plate's width in two columns at 1440 px and one at 390 and 360 px. The build reads the list from `work/extract/atlas-v7-data.json` and stops if the count is not 10; the figures file records R-01 and R-02 as the two V7 flags. Alt and caption say all 10. |
| 6 | BE-M4, CD-M2, D2-960 | The key plate's title is "Most claims in these three chapters are documented or well supported", in the plate and its alt; the counts stay; the build checks that 28 of 39 is a majority; the caption adds that the title says only what the counts show. |
| 7 | BE-S5, CD-S13 | `s-12-locator-correct` and `s-12-locator-failure` carry one Illustrative label at the plate's head, `illustrative: true`, and "Illustrative" in each alt. |
| 8 | CD-S2 | Rule 10.1's atlas example is CL-009 Safe seats, Variable C1, in the plate and the alt. |
| 9 | CD-S3 | `s-10-9-failure`'s kicker reads "Act · How to take part", with the dot hidden from screen readers; the alt says so. |
| 10 | CD-S4 | Library cells: the name, then the drawing ID in plain gray, then the typed chip in its box; a reform cell's chip ("Reform R-05") carries its ID, which is the drawing's ID too. The 24 px mark is plain text, "Also at 24 px", with no box, and each sheet's header says so. |
| 11 | CD-S12 | Rule 12.5 lists `oa.color.data.emphasisRed.onNewsprint` first in its tokens and on the "Target weight" spec, which now opens "Pillar Red:". |
| 12 | PP-S3 | The sentence above, in Rule 10.6, and sent to the editor here. |
| 13 | PP-S5 | Rule 10.6 defines the typed chip at first use and gains two spec rows: "Typed chip" (the kind, then the atlas ID, in the label style, set after the name) and "Chip outline" (1 px, strong border color, 3 px above and below, 6 px at each side, never wrapping). Name first, then chip, in every chapter 10 plate: `s-10-8-correct` and `s-10-8-failure` now match `s-10-6-correct`, the class table and the library. Rule 10.8 reads "Its other parts take their names in words, each followed by a typed chip with its ID, such as Domain D02", with an "Order" spec. |
| 14 | PP-S7 | Rule 10.5 says a tile holds its drawing at about two thirds of its size: 49 or 50 px in the smallest two-color tiles, 32 to 34 px in the smallest one-color tiles. It names that as the one place a drawing off the list of 41 goes under Rule 10.4's 48 px floor, for the 94 drawings reviewers could still name at 32 px only; the other 30 take one-color tiles from 72, 76 and 80 px. Rule 10.4's why now gives the reviewers' 32 px reading, and its old line "The rest needed 48 px before the reviewer could name them." is gone, since the review read at 32 px, not 48. See question 1. |
| 15 | PP-S8 | Rule 10.7: "Two or more symbols set together with no current item, such as two atlas symbols on one slide, count as a row, so each one goes one color." |
| 16 | PP-S4, PP-S6, PP-S10 | "Edition" is defined at first use, in group 3's line ("one of the four color versions of every drawing"); Rules 10.2 and 12.9 say "our guide’s fourth edition". Rule 10.10 defines a connection ("a claimed relationship between two variables", the atlas glossary's words) and the sign (whether the two variables tend to move the same way or in opposite directions), and Rule 10.1 and its class table no longer say "sign" before that. Rule 12.6 defines the measure line at first use. |
| 17 | CA-S7 | The editor's words, as above. |
| 17 | CA-S8 | Rule 10.7's menu breaks "Contact / an official": each item takes the width its words need, short words stay with the next word, and the items sit 12 px apart. Captured at 1440, 390 and 360 px. |
| 17 | CA-S9 | `s-10-4-correct`: the story card, the one invented piece, carries its Illustrative label at its head, above the kicker. |
| 17 | CA-S12 | The state locator draws 8 px tiles with 1 px gaps, 107 by 71 px, so the headline beside it keeps 205 px at 360 px (it ran six lines in 110 px; it now runs four). The spec states the new sizes. |
| 17 | D2-971 | Rule 10.9 gains a paragraph naming the five (CL-023, CL-028, R-08, R-27, R-45 with their words) and "Never set two of them in one view at that size", plus a spec row. `s-10-9-correct` shows them as a seventh group at 24 px, one color, with what tells them apart from 48 px and their likeness, 0.80 to 0.96. |

Also done, beside the brief's list:
- **BE-S8 for Rule 12.9's source line** (D2-968): "as in force on November 9, 2026" after the statute, "via the Legal Information Institute, Cornell Law School", and "no page date" after FOIA.gov. The brief lists BE-S8 under the chapter 11 hand, and the report names me to apply it to Rule 12.9, whose line is mine.
- **PP-S16, Rule 10.8's half:** the why's closing restatement, "Words keep the levels of the atlas apart.", is gone (one run per string).
- **ED 4c's check on grade marks:** Rule 12.6's "Grade marks" spec now says the fills are for bars and areas, and a connection takes Rule 10.10's line textures.
- **Rule 10.9's why:** "Court alignment and Local government come closest" stopped being true once the five joined the plate, so the why now says the six groups of neighbors all score under the flag, and four of the five look-alikes' 10 pairs reach it.
- **The construction file**, section 0 and section 5, follows Rule 10.2's new title and accent wording.

## Routine calls

- D2-xxx | IDs in visible text take U+2011, and alt text keeps the plain hyphen | D2-950; a screen reader reads the plain hyphen as written, and an alt never wraps on screen
- D2-xxx | U+2011 is drawn from Arial, the face after Inter in our stack | Inter as the page loads it has no glyph for U+2011, so Chromium falls back one face; I measured Arial's hyphen beside Inter's at 4x, and the ID reads the same, about 1 px narrower
- D2-xxx | Rule 10.8 lists all 10 reforms in the atlas's own order, and the build stops if the count changes | D2-958 prefers all ten where they fit; the atlas's order picks none, and R-01 and R-02 lead only by number
- D2-xxx | Name first, then the typed chip, everywhere in chapter 10; Rule 10.8 reads "names in words, each followed by a typed chip" | PP-S5 asks for one order; the class table, the library and Rule 10.6 already set the name first, so one plate changed rather than four
- D2-xxx | A reform's library cell shows its chip ("Reform R-05") in place of the bare ID | The drawing's ID and the atlas ID are the same, and H11 asks for no bare ID
- D2-xxx | The 24 px mark in the library is plain text, "Also at 24 px" | CD-S4: a box now means a typed chip and nothing else
- D2-xxx | Rule 10.7's menu sizes each item to its words and binds a short word to the next | CA-S8; it holds at 390 and 360 px with no overflow
- D2-xxx | The five look-alikes' likeness is measured with `icon_likeness_check.js`'s own functions, and only the 10 new pairs join the figures file | The distribution came out identical (7,626 pairs, flag 0.9092), so the figures already printed keep their values
- D2-xxx | Rule 10.5 states the one-color tiles as the one exception to Rule 10.4's floor, for the 94 drawings read at 32 px | PP-S7 asks to square the two rules; the tile minimums come from the inventory's tile rule (bare floor 32 px, 48 px for drawings that stop reading at 32 px), which I did not change (question 1)
- D2-xxx | The state locator draws 8 px tiles with 1 px gaps | CA-S12 asks for 200 px of headline; a locator under the headline would break Rule 12.7's "top right"
- D2-xxx | Rule 12.9's source line takes BE-S8's wording | D2-968; the line is mine, and chapter 11 prints the same statute
- D2-xxx | Rule 12.7's second sentence takes the editor's 4c wording, "Draw the locator in ink, with no red." | The editor's 4e note counted it as applied, but the generator still printed "stays in ink and never takes red"
- D2-xxx | My chapter 12 build normalizes spaces and hyphens in my own rules and intro sentence only | Two makers share the file, and my round 2 build rewrote every rule's spaces
- D2-xxx | My intro sentence is found and replaced in place, after the identity designer's sentence in the same paragraph | Their build prepends theirs; mine now owns only the text from "Rules 12.5 to 12.9 cover" to the paragraph's end
- D2-xxx | `s-05-3-corrective` takes chapter 11's `U-error` at 24 px, with 12 px between the bar and the mark | D2-959; Rule 11.15's band sets the same gap
- D2-xxx | Rule 10.4's why drops "The rest needed 48 px before the reviewer could name them." | The October review read at 128, 64, 32 and 24 px, never at 48 (construction file, section 10), and Rule 10.5 now cites its 32 px reading
- D2-xxx | Rule 12.5 glosses "connection" where it first appears in chapter 12 | A reader can land on Rule 12.5 without Rule 10.10

## Questions for Dustin

1. **The smallest one-color tiles sit under the 48 px floor.** A one-color tile from 48 px square or 52 px rounded or round holds its drawing at 32 to 34 px. The tile minimums came from the October review's 32 px reading (the inventory's tile rule), before DR-136 set 48 px as the floor for topic and atlas symbols, and no rule had squared the two. Rule 10.5 now states the tiles as the one exception, for the 94 drawings reviewers could still name at 32 px. *Recommendation:* keep the exception, since avatars and small app tiles show at 32 to 48 px and the drawing there sits on a solid ground. The other answer is one-color tiles from 72, 76 and 80 px for all 124, the two-color sizes, which keeps DR-136 without an exception and rules out small avatars. Board B can show the sentence.

## Tested

- Before any change: `stage_b_ch10_build.py --no-draw`, `stage_b_ch12_systems_build.py` and the stage A probe, capture and final, rerun on the committed generators. Every output was byte for byte the committed file, apart from the stage A measurement record's token set version (gate2.3 to gate2.5) and capture date. The capture loaded every Google Fonts face it checks.
- After my changes, the same builds: chapter 10, 10 rules and 26 specimens; chapter 12, 5 rules of mine and 10 specimens, with the identity designer's Rules 12.1 to 12.4, their extra and their intro sentence kept as their latest run wrote them; chapters 05 to 07, 23 rules and 53 specimens. Each build's own checks pass (no heading or landmark, dash, literal color, px font size or straight quote; every specimen used once).
- `git diff` on every output after each of my runs: only the intended changes. My runs touched only the s-05, s-06, s-10 and my s-12 entries in the manifest; the chapter 11 hand's entries changed through their own runs.
- By script: 21 banded failure plates in my chapters, every alt opens "Failure case: do not publish."; no alt holds U+2011; no ID with a plain hyphen left in the visible text of chapter 10 or Rules 12.5 to 12.9.
- By script on Atlas V7 (`python3 -I`, queried, never read whole): the 10 reforms that aim at B5 and C1 to C5, and that only R-01 and R-02 carry `interest_note`. Each of the 10 names on the plate matches V7's reform title character for character, and each chip reads "Reform" and its V7 ID; the six variables' chips match their V7 IDs.
- Likeness of the five look-alikes, with the engineer's functions: 0.80 to 0.96; four pairs reach the flag (CL-028 and R-27 0.958, R-08 and R-27 0.945, CL-028 and R-08 0.942, CL-023 and CL-028 0.928). The distribution matched the round 2 run exactly.
- U+2011 in Chromium with Inter loaded from Google Fonts: Inter has no glyph for it, and with our stack the mark comes from Arial (Liberation Sans here), which I compared at 4x.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`: exit 0, 0 warnings, 0 notes, 132 rules, 305 specimens.
- `node work/build/scripts/phase-2/guide_check.js`, full, at 1440, 1024, 390 and 360 px: PASS, 0 failures, 132 rules, 305 specimens, 1,100 same-page links, twice: once before the editor's Rule 10.2 words and once after them. My exemptions are unchanged: `s-05-2-failure`, `s-05-3-failure`, `s-05-6-failure`, `s-05-7-failure`, `s-06-2-failure`, `s-06-3-failure`, `s-07-5-failure`, `s-10-5-failure`, `s-10-10-failure`, `s-12-marker-failure`, `s-12-key-failure`, `s-12-locator-failure`, each a labeled failure.
- After that, five small wording edits (Rule 10.5's third paragraph, Rule 10.10's sign sentence, Rule 12.5's connection sentence, Rule 12.6's caption, two spec values in Rule 10.6), then a fresh strict build (exit 0) and `guide_check.js --quick` at 1440 and 390 px: PASS, 0 failures, 1,101 same-page links. I did not rerun the full four widths after those edits.
- Looked at, by capture: at 1440 px and 2x, `s-05-3-corrective`, `s-10-1-correct`, `s-10-lib-01`, `s-10-lib-04`, `s-10-4-correct`, `s-10-7-correct`, `s-10-8-correct`, `s-10-9-correct`, `s-10-9-failure`, Rule 10.4's specs, `s-12-key-correct`, `s-12-locator-correct`, `s-12-layers-correct`, `s-12-owner-correct`; at 390 and 360 px and 2x, those and `s-10-2-correct`, `s-10-8-failure`, `s-10-10-correct`, `s-10-list-41`, `s-12-locator-failure`, and Rules 10.5's and 10.6's specs. Fixed from what I saw: the menu items ran together ("Voting Petition") at 4 px apart, the 24 px group's drawings floated in 64 px of space, and the library header printed "the 9" where H06 wants "nine".

## Not tested

- A screen reader by ear, Firefox, Safari, real phones, print.
- How U+2011 renders on a Mac or Windows machine whose Arial or fallback face differs from Liberation Sans.
- Forced colors and 200 percent text on the changed plates by eye; the guide check's forced colors and text spacing tests ran and passed.
- Whether readers tell the five look-alikes apart at 48 px; the plate's words come from the editor's meaning sentences.
- The 1x captures at 390 and 360 px; I looked at 2x there and at 1x only at 1440 px for Rule 10.4.

## Change log

Modified (generators):
- `work/build/scripts/phase-2/stage_b_ch10_build.py`
- `work/build/scripts/phase-2/stage_b_ch12_systems_build.py`
- `work/build/scripts/phase-2/stage_a_systems_ch05.py`
- `work/build/scripts/phase-2/stage_a_systems_ch06.py`

Modified (written by those generators):
- `work/build/guide/chapters/05-color.json`, `10-symbols.json`, `12-graphic-devices.json` (my rules and my intro sentence only)
- `work/build/guide/specimens/s-05-3-corrective.html`; `s-10-1-correct`, `s-10-2-correct`, `s-10-4-correct`, `s-10-6-correct`, `s-10-7-correct`, `s-10-7-failure`, `s-10-8-correct`, `s-10-8-failure`, `s-10-9-correct`, `s-10-9-failure`, `s-10-10-correct`, `s-10-lib-01` to `s-10-lib-05`, `s-10-list-41`; `s-12-marker-correct`, `s-12-key-correct`, `s-12-locator-correct`, `s-12-locator-failure`, `s-12-layers-correct`, `s-12-owner-correct` (all `.html`)
- `work/build/guide/specimens/manifest-systems.json` (the s-05, s-06, s-10 and my s-12 entries)
- `work/handoffs/phase-2/20261110_Stage-B-Ch10-Figures.json`, `20261110_Stage-B-Ch12-Systems-Figures.json`, `20261106_Stage-A-Systems-Measurements.json`

Modified by hand: `work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md` (sections 0 and 5, Rule 10.2's title and accent).

Created: `work/handoffs/phase-2/20261110_Stage-B-Round-3-Systems-Fix-Notes.md` (this file).

Scratch only: builds, checks and captures in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/round-3/fix/systems/`. The `s-06-*` fragments did not change; only one chapter 06 alt in the manifest did.

Nothing in `source/`, `work/ledger/`, `deliverables/`, any asset folder, any board or another owner's script. Nothing committed or pushed.

## Second pass (D2-963, DR-191)

The editor's read after the pass (`20261110_Stage-B-Round-3-Editor-Fix-Notes.md`, section 8) lists five faults in my strings: rows 6, 7, 8, 9 and 13. Each is applied word for word in my generators.

| Row | Where | Now reads |
|---|---|---|
| 6 | Rule 10.6, `rule[1]`, second sentence (`stage_b_ch10_build.py`) | “An atlas drawing appears only beside the atlas’s own name for it.” |
| 7 | Rule 10.4, spec "Floor" | “48 px for any of the 124, except inside a one-color tile (Rule 10.5)”, so Rule 10.4's floor names Rule 10.5's tile exception |
| 8 | Rule 10.9, `why.text[1]` | “…and four of their 10 pairs score 0.91 or more…”, the figure read from the likeness record, as the paragraph before prints it |
| 9 | `s-10-9-correct`, the new group's head, and its alt | “At 24 px, never two in one view” |
| 13 | Rule 12.7, `correct.caption` (`stage_b_ch12_systems_build.py`) | “…each in ink, small enough that the headline beside it keeps at least 200 px on a phone.” |

- D2-xxx | Sources keep U+2011 in IDs | The engineer's build pass writes IDs with an ASCII hyphen in a no-wrap span (D2-975), as the main session's message says
- I reran `stage_b_ch10_build.py --no-draw`, then `stage_b_ch12_systems_build.py`. My chapter 12 build changes only Rules 12.5 to 12.9 and my intro sentence, so the identity designer's rules stand as their last run wrote them. Their script runs through `promotion_identity.py specimens`, which writes their own files, so I left that run to them and the main session.

Tested and Not tested for this pass: see the lines added under "Tested" below this section.

### Second pass: Tested

- Each of the five new strings found by script in its output: `10-symbols.json` (rows 6, 7, 8), `s-10-9-correct.html` and its manifest alt (row 9, with the no-break space in “24 px”), `12-graphic-devices.json` (row 13); “At 24 px only” no longer appears.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide-p2.html`: exit 0, 132 rules, 305 specimens, with the engineer's D2-975 pass in the build.
- `node work/build/scripts/phase-2/guide_check.js` on it, at 1440, 1024, 390 and 360 px: 4 failures, one per width, all the new `nbHyphen` test (D2-975) and all in one plate, `s-11-12-correct`, chapter 11's filter: "CL‑006", "CL‑007", "CL‑008" and "Cross‑cutting civic ties". Its script adds the U+2011 as the page runs (`function h(x){return x.replace(/(\w)-(?=\w)/g,'$1‑');}`), after the build pass has run, so the build cannot replace it. That plate belongs to the chapter 11 hand, and I did not edit it. No hit in chapters 05, 06, 07, 10 or 12, and no other test failed.

### Second pass: Not tested

- A four-width check with 0 failures: it waits on the chapter 11 hand's fix to `s-11-12-correct`'s script. I did not rerun after it.
- Captures of the five changed strings; rows 6 to 8 and 13 change words only, and row 9 changes a short label in the same place.
