# Chat 12 editor notes

Editor, chat 12's fix pass, November 23, 2026. Brief: `work/handoffs/phase-4/20261123_Chat-12-Fix-Brief.md`, sections 1, 2, 3.4, 3.6 and 4. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/fix/editor/`. Started 17:48:06 UTC (`date -u`); notes opened 17:52:48 UTC.

Turn 1 (section 3.6): I hold the word fields of `work/build/scripts/phase-4/phase4_ch21_build.py`; the design director stays out of that file this turn. Chapter 21's items: CE1's names, CE6, CE7, CE8, CE9, CE12, CE15 (chapter 21's share), RP1's labels, RP2, RP3, RP4, ST-1's line, ST-2, DF1, DF2, DF6, DF7, DF8, DF10, CD-S5, and the words AX-1 to AX-4 need.

Read first: my role file; `CLAUDE.md`; chapter 02's writing rules; the fix brief; the decision log from line 7590 to its end (D4-237 to D4-308, DR-326); the words and readers report (CE, DF, RP), the evidence and balance report (ST-1, ST-2), the accessibility report (AX-1 to AX-4), the creative director's review (CD-M2, CD-S5); my chat 11c predecessor's notes.

Generator before my first edit: SHA-256 `de5c7088e2425c6d…`, copied to scratch `phase4_ch21_build.before.py` (17:48:47 UTC). `21-atlas.json` 52,523 bytes. `--check` and `--page-words all` exit 0 under the lock (17:50:55 UTC); page words saved as scratch `page-words.before.json`.

## Routine calls

- D4-xxx | RP2's reason for the four views is one sentence at the end of chapter 21's first intro paragraph, where a third paragraph first stood | The chapter check allows two intro paragraphs (`check_chapter` stopped the first `--check`, 17:58 UTC); the sentence follows the paragraph that names the pages, and it carries D4-164's reason, the rotation across subjects and a finding from the record that one side may want to skip
- D4-xxx | Rule 21.6 and its chips plate follow the data lead's R22: a rule change and a delivery case print their stored sentence as their name, and a claim prints none, where CE12 offered "its first words" or a caption that names no name for all three | R22 names each kind's field; the plate printed nothing for RL19 and DL05, so the rule, caption and alt would have disagreed with the plate. The plate grew 718 bytes (8,583 to 9,301), two stored sentences in each of its two panels
- D4-xxx | CE8's read-aloud templates keep their words, and the comma that sets off a name travels with the name in the kit's `{var}` (R22 item 1) | A later mention takes the chip alone, and a comma typed in the template would then print "Variable D2, rises"; the composed line is given under "Words for", item 18
- D4-xxx | CE15 also recasts the "never" turns in Rule 21.5's Red row, Rule 21.8's grade columns, Rule 21.15's Marks and Selected bar rows, the third source line and the chips plate's notes; "It carries no sign and never closes a loop" on How to read and Rule 21.14's row label "Never" stay | Each recast one was the same W09 turn the review counted; the two kept are a plain fact and a label for what is ruled out, with no turn from one thing to another
- D4-xxx | Rule 21.12 gains a specification row, "Chosen reform", naming the confidence line under the effects and the disclosure under the panel | ST-1's fix and R21; the evidence reader's item 2 for Dustin asks that the next builder of a chooser cannot miss them, and chapter 21 can say so without touching approved chapter 15
- D4-xxx | R27's column head, "Numbered loops", is typed in `PAGES['A13']['page']['index_head']`, my word field, though R27 names the head the design director's | The design director stays out of this file this turn; the words are the ruling's, and the design director confirms them in turn 2
- D4-xxx | CD-S5 and DF1 needed two small code changes outside the word fields: `view_words()` and `rows()` take the page's ID, with each page's words for a shared part key in `VIEW_WORDS['page_parts']`; and `_esc()` passes text through a new `typo()`, also applied to the two titles in Rule 21.15's failure alt | Both codes are assigned to me this turn and the file is mine alone; neither changes a drawing, and the design director keeps or moves them in turn 2
- D4-xxx | On public pages, CE7's studio words become the reader's: "in the text’s own color", "keeps the drawing’s usual color", "On the light page a red connection carries a thin dark edge" | A public reader has never met Newsprint, Charcoal or "ink"; the guide's own captions and alts keep those words, since builders read them
- D4-xxx | CE9's words, "The question you pressed reaches here", sit in quotation marks wherever Rule 21.3's prose, specification and alt quote them | A seven-word phrase read inside a sentence with no marks runs into the words around it
- D4-xxx | AX-1 and AX-2 need no new words | Rule 21.13's words already count "Step 1 of 2:" in each hold (9,250 and 16,000 ms), right once the engineer moves the part name off the stepper's root; Rule 21.3 already names the bold words AX-2 restores
- D4-xxx | R24's label for the part's second line reads "In our atlas: {title}" | The data lead's suggested form; the pages speak of "our atlas", and the label tells a phone reader which line is the name
- D4-xxx | `answer_label` stays in the field beside the new `answer_heading` until the kit reads the new key | The kit stops on a missing key (`wd()`), and the old key costs nothing a reader sees once the kit switches
- D4-xxx | The Register page's intro says "lists every connection once" where it said "files once" | "files once" stopped the simulated teacher (the reader panel, CE6); the guide's rule prose keeps "files", a builder's word

## Rulings

None of my own; I follow the data visualization lead's (`20261123_Chat-12-Dataviz-Lead-Notes.md`) as they land.

## Words for

Typed into `PAGES` in `phase4_ch21_build.py` by 17:59 UTC; the kit reads them through `--page-words`. `{…}` is a fill the kit makes from the model. Names after chips follow the data lead's R22 throughout: the stored name in typographic quotation marks after the chip at its first mention on a page, set off by commas where the sentence runs on, never recased; later mentions take the chip alone; a list of chips joins with commas and "and".

### For the atlas engineer (`atlas-page.mjs`), keys new or changed

**Land with your next build, or the page prints braces:** A13 `whole_note` now holds three new fills.

A11, the atlas home
1. `lit`, changed (CE9): "The question you pressed reaches here". Eight characters longer than before; check CR-3 in the boxes and cards.
2. `key_other`, changed (R25, DF2): "Other arrows between parts."
3. `part_title`, new (R24, RP4): "In our atlas: {title}", the labeled second line on every box at 1440 px and every card at 390 px, `{title}` the part's title from the model (`layers.core.regions[…].title`, `layers.economy.title`, `layers.technology.title`). The plain name above it stays the part's name and accessible name.
4. `answer_heading`, new (R19, AX-4, CD-M2): "The short answer: {question}", the heading of each question's answer region, `{question}` the pathway's stored question, its apostrophes typographic. `answer_label` ("The short answer") stays in the field until the kit reads `answer_heading`; tell me and it goes.
5. `answer_none`, new (R19): "Our atlas stores no short answer to this question. The parts lit above hold the variables its record names." Printed only where a pathway's `short_answer` is empty (none today).
6. `variables_list`, new (AX-3): "Variables in {part}", the name of each part's nested list of variables that Show every variable opens for every reader, `{part}` the plain name.

A12, Reform R-23
7. `conn_note`, changed (CE7): "{conn} “{name}” joins them: {sign}, {delay}, {grade}. It keeps the drawing’s usual color, since the reform does not act on it."
8. `reading_one` "One reading" and `reading_other` "The other reading", new (R23, RP1): over the two blocks, same class, outside the element that holds the stored text.
9. `means_line`, new (CE8): "{var}: {means}", each target's line, `{var}` the Variable chip (alone, since `where_note` names both targets first; with “name” if it is the first mention), `{means}` the stored `increase_means` whole. Today's line reads "Variable EC7: A higher value means households receive more money over the year."
10. The tag list (CE1, R22 item 2) needs no new key: the kit composes "Variable A4 “Households’ financial security”: Reform R-24 “Paid family and medical leave insurance”, Reform R-25 “Full child tax credit for low-earning families”, Reform R-26 “Recession aid that starts automatically” and Reform R-31 “Childcare supply and pay for care workers” also aim here." `aims_here` and `aims_here_one` are unchanged. Where `where_note` follows, its targets then take the chip alone (R22 item 1), or the tag list's A4 takes the chip alone if you move the note above it.
11. `touches` is unchanged; `{loop}` becomes "Loop R6 “Weak bargaining power and concentrated wealth reinforce each other”".

A13, the Register
12. `intro`, changed (CE6): "Our atlas lists every connection once, with its sign, its grade and its citation, on the sheet for the subject area of the variable it moves. Each sheet counts its records and grades, so a reader can check every number here line by line."
13. `index_head[3]`, changed (R27, ST-2): "Numbered loops". The head is the design director's by R27; it sits in my field, so I typed the ruling's words, and the design director confirms in turn 2.
14. `whole_note`, changed (R27, ST-2): "The whole atlas counts each loop and reform once, though many reach several sheets, and its reforms leave out those the atlas rejects. Its loops column counts the {numbered} loops that close through numbered connections; the loop index lists all {loops}, since {conceptual} more close only in concept, with no chain of connections to file." Fills: `{numbered}` a count span of `atlas:loops-numbered` [20], `{loops}` of `atlas:loops` [23], both as figures; `{conceptual}` of R27's new `atlas:loops-conceptual` [3] in words, as `{retired}` is (house rule H06), with `data-count` the figure.
15. `variable_line`, new (CE8, R22): "{var} “{name}”: {means}" for each variable in "Its variables", `{name}` the stored title, `{means}` the stored `increase_means`. Today: "Variable D1 “Congress’s ability to write and check policy”: A higher value means Congress has more staff and expertise to draft laws and oversee agencies." If the design keeps the title bold, the quotation marks still go round it (R22).
16. `rejected_targets` is unchanged; `{targets}` reads "Connection L18 “Congressional expertise may reduce insider influence” and Connection L19 “Insider-tilted policy may weaken congressional expertise”" at their first mention.

A14, Loop R18
17. `grade_step`, new (R22 item 4): "{grade} for {conn}", `{conn}` the Connection chip and its stored name in quotation marks, the steps joined by "; ": "Documented for Connection L14 “Presidential removals weaken watchdog agencies”; Plausible for Connection L15 “Independent watchdogs restrain unilateral action”". `grade_line` stays in the field for the loop index's form.
18. The read-aloud templates are unchanged (CE8 with R22): the kit composes `{var}` as the chip, a comma, the stored title in quotation marks and a comma at the variable's first mention, and as the chip alone after it. Loop R18 then reads: "Start with Variable D2, “Presidential action without new legislation”, rising. Along Connection L14, which lowers, Variable D4, “Ability to investigate and enforce the rules”, falls. Along Connection L15, which lowers, Variable D2 rises. The loop comes back moving the same way it started." (L14 and L15 take the chip alone here, since the grade line names them first.)
19. `effects_confidence`, `assumptions_summary`, `assumptions_remedy`, `assumptions_tradeoffs`, new (R21, ST-1). Under each panel's four rows: "Our atlas’s confidence in these effects: “{text}”", the same words as A12. The disclosure under the panel, in approved chapter 15's words (`s-15-20-correct`): summary "Our atlas’s qualifications and assumptions for {reform}" (`{reform}` the chip); then "The evidence for the remedy, {grade}: “{text}”" (`{grade}` the display word in lower case, `{text}` the stored `remedy_evidence.text`); then "Its tradeoffs: “{text}”" (the stored `tradeoffs`).
20. `also_aim` and `also_aim_one` are unchanged; each chip takes its name at its first mention.

A16, How to read
21. `marks.red`, changed (CE7): "… On the light page a red connection carries a thin dark edge."; `marks.tag`, changed: "Other reforms that aim at the same place, in the text’s own color, so the red stays with the reform you chose."

Frame names and alts the kit types
22. DF6 (R26): A13's and A18's frame alts read "with sheet D04 open" and "with sheet D10 open"; they become "with the sheet for Domain D04 open" and "with the sheet for Domain D10 open". No alt or frame label prints a bare "sheet D04".
23. DF5 (my turn 2 item, given now so it lands in the same build): every frame alt that ends "At 1440 px, on Newsprint." or "At 390 px, on Newsprint." ends "At 1440 px, in the light theme." and "At 390 px, in the light theme.", as the dark frames already say "in the dark theme".

### For the design director (turn 2 on this file)

- Two small code changes sit outside the word fields, made this turn because the file is mine and each serves a word item: `view_words()` and `rows()` take the page's ID so a plate with two pages on one part key labels each frame in its own words (CD-S5, `VIEW_WORDS['page_parts']`); and `_esc()` passes text through a new `typo()`, which prints the stored text's straight apostrophes and single quotes typographic in this file's own drawings (DF1, fix brief section 2), with `typo()` also on the two titles in Rule 21.15's failure alt. Keep or move them as you see fit.
- R24: the specs gain the labeled second line ("In our atlas: Outside drivers"); Rule 21.2's "Parts" row says so.
- R25: "arrow" in place of "flow" in the specs; Rule 21.2's title, rule and rows now say "arrow".
- R27: `index_head[3]` reads "Numbered loops" (item 13 above).

## Done

All in `work/build/scripts/phase-4/phase4_ch21_build.py`, written to `21-atlas.json`, `manifest-atlas.json` and ten specimens by the generator under the lock (last run 18:04:16 UTC). "R" is the rule's field; "A11" to "A16" the page words the kit reads.

- **CE1** (R22). Words: A14 `grade_step` "{grade} for {conn}"; Rule 21.5's rule and Tags row give each reform's chip its name, joined by commas and "and"; Rule 21.6 gains the row "First mention"; Rule 21.12's Head row says "by its connection’s chip and name"; Rule 21.5's alt. The kit's composition and T1 are the atlas engineer's (Words for, items 10, 11, 16 to 18, 20).
- **CE6.** Intro: "The Register files every one of the atlas’s {connections} connections once, with its evidence. A connection is an arrow from one variable, a quantity or condition that can rise or fall, to another." (was "… connections, the arrows from one variable to another, once and with its evidence."); "links every claim to the record that grades its evidence, on Rule 13.3’s scale from documented to hypothesis" (was "the record that grades it"). Group 3: "… on the sheet for one of the atlas’s subject areas …" (was "on one sheet"). Rule 21.8 now defines an issue record, and Rule 21.11 no longer repeats it. Rule 21.12: "an even count makes a reinforcing loop, one that feeds itself, and an odd count a balancing loop, one that pushes back". A13 `intro`: "Our atlas lists every connection once, with its sign, its grade and its citation, on the sheet for the subject area of the variable it moves." (was "Every connection in our atlas files once, on the sheet of the variable it moves, …").
- **CE7.** A16 `marks.red`: "On the light page a red connection carries a thin dark edge." (was "On Newsprint … a thin Charcoal edge."); A16 `marks.tag`: "in the text’s own color" (was "in plain ink"); A12 `conn_note`: "It keeps the drawing’s usual color, since the reform does not act on it." (was "It stays in ink, …"). No public page word now says ink, Newsprint, Charcoal, Stone or flow (script).
- **CE8.** New A12 `means_line` "{var}: {means}" and A13 `variable_line` "{var} “{name}”: {means}"; the read-aloud composition is the kit's (Words for, items 9, 15, 18).
- **CE9.** A11 `lit`: "The question you pressed reaches here" (was "This question reaches here"); Rule 21.3's rule, Lit parts row and alt quote the new words.
- **CE12.** Rule 21.6: "The first time a page names a record, its name follows the chip, and for a rule change or a delivery case, the sentence the atlas stores for it. A claim has no name, so the sentence that holds its figure names it." Caption: "… each a real record followed by its name as the atlas stores it, all but the claim, which a figure’s own sentence names; …"; alt: "nine of them followed by the record’s name or stored sentence". The chips plate prints RL19's and DL05's stored sentences (R22; Routine calls).
- **CE15, chapter 21's share.** 21.2 Ink: "one single-headed arrow for each direction of a pair" (was "…, never a double head"); 21.3 Status line: "and stays silent on load" (was "never on load"); 21.6 Kind word and builders: "since the same letters name different kinds, as B4 does" (was "never from its letters"); 21.7 One step: "with no search between" (was "never a search"); 21.11 Count line: "silent on load" (was "never on load"); 21.13 rule: "and at least six seconds" (was "never less than six seconds"), Hold row "and at least 6,000 ms" (was "never under 6,000 ms"); 21.15 Every color: "From a token named in the page’s code" (was "From a token, never a hex in the page’s code"); 21.16 Self-test: "with the model untouched" (was "never in the model"). Also 21.5 Red, 21.8 Grade columns, 21.15 Marks and Selected bar, the third source line and the chips plate's notes (Routine calls).
- **RP1** (R23). New A12 `reading_one` "One reading" and `reading_other` "The other reading"; Rule 21.4's Contested remedy row and alt name the labels.
- **RP2.** Intro, paragraph 1, last sentence: "The plates follow four views chosen in turn across subjects, as chapter 01 rotates examples (Rules 01.9 to 01.12): a question about medical bills, Reform R-23 on the minimum wage, the Register’s sheet on Congress and the agencies, and Loop R18 on presidential power over watchdogs, each with a finding from the record that one side of a debate may want to skip." Read from the left: the minimum wage view carries the Congressional Budget Office's job-loss estimate whole. Read from the right: the watchdog loop is "presidential power", which its stored record shows both parties using. Neither reading meets a view named for a side.
- **RP3.** Rule 21.4's Contested remedy row: "… each with its source a step away, printed as stored; house rule H08 governs our own sentences about the grade" (was "(house rule H08)").
- **RP4** (R24). New A11 `part_title` "In our atlas: {title}"; Rule 21.2's Parts row names the labeled line.
- **ST-1's line** (R21). New A14 `effects_confidence` (A12's words), `assumptions_summary`, `assumptions_remedy`, `assumptions_tradeoffs` (approved chapter 15's words); Rule 21.12's new "Chosen reform" row and its alt.
- **ST-2** (R27). A13 `index_head[3]` "Numbered loops"; `whole_note` adds "Its loops column counts the {numbered} loops that close through numbered connections; the loop index lists all {loops}, since {conceptual} more close only in concept, with no chain of connections to file."; Rule 21.8's rule ("numbered loops") and Whole atlas row.
- **DF1.** `typo()` prints the stored text's apostrophes and single quotes typographic in this file's own drawings: `s-21-3-failure` ("can’t"), `s-21-5-failure` ("Households’"), `s-21-7-failure` (six: "bill’s", "doctors’", "patient’s", "Hospitals’", "‘big three’", "Ain’t"), `s-21-11-failure` ("Congress’s"), and the chips plate's "Vice President’s". The kit's pages are the atlas engineer's (at render).
- **DF2** (R25). A11 `key_other` "Other arrows between parts." (was "Other flows."); Rule 21.2's title "with a count on every arrow", its rule "the other arrows", its Ink row, and its At 390 px row "one line for each part its connections reach, such as “5 to Voice”, so each count prints once".
- **DF6** (R26). Rule 21.10's failure label "The sheet for Domain D04, its reforms, at 390 px" (was "Sheet D04’s reforms at 390 px"); two plate notes; the kit's alts are in Words for, item 22.
- **DF7.** Rule 21.12's title "Head a loop page with the grade of each step and the arithmetic of its signs." (was "… with its grade line …"); Head row "Chip, the loop’s kind (Reinforcing or Balancing) and the title …" (was "Chip, kind word and the title …").
- **DF8.** Rule 21.2's rule: "in the essential ink … and the other arrows in the subtle ink" (was "in full ink … in a lighter ink").
- **DF10.** Rule 21.14's How to read table: "Also aim here" (was "Ink tag, aims here"); the extra's alt "the Also aim here tag" (was "the ink tag").
- **CD-S5.** Frame labels, each page's own: `s-21-7-correct` "1440 px, light, Loop R18’s evidence for its first step, Connection L14" and "1440 px, light, Connection L14’s line in the Register" (both were "Connection L14’s row"); `s-21-10-correct` "390 px, light, the rejected option on the sheet for Domain D04" and "390 px, light, reviewed and not drawn, on the sheet for Domain D10" (both were "the rejected option").
- **AX-1 to AX-4, the words they need.** AX-1 and AX-2: none (Routine calls). AX-3: new A11 `variables_list` "Variables in {part}"; Rule 21.2's Switch row: "pressed, it opens each part’s list of variables for every reader, in the boxes on wide screens, in the cards on phones and in the parts list a screen reader reads". AX-4 with CD-M2 (R19): new A11 `answer_heading` "The short answer: {question}" and `answer_none`; Rule 21.3's rule ends "… the question’s own short answer opens below, headed by the question, … The page loads with no question pressed and every part at full strength.", with a new Answer row and "stays silent on load".

### Proof

- `git diff --stat` on my files, 18:04 UTC: `phase4_ch21_build.py`, `21-atlas.json`, `manifest-atlas.json` and ten specimens (`s-21-3-failure`, `-5-failure`, `-7-correct`, `-7-failure`, `-9-failure`, `-10-correct`, `-10-failure`, `-11-failure`, `-chips`, `-how-to-read`), 13 files, 183 insertions, 113 deletions. A word diff of each specimen shows only the changes above. The main session's snapshot commit at 17:56:49 UTC (`b65d0c52`) holds a mid-edit copy of my generator, so against HEAD the generator shows part of its change; against `f52ef2d9`, the commit before my turn (equal to my scratch copy), it reads 1 file, 176 insertions, 97 deletions. Every output file at HEAD is still the pre-turn version (`21-atlas.json` 52,523 bytes in all five commits), so the byte figures below compare my output with the pre-turn output. The tree also holds other owners' changes, none mine: the kit's code, specs and tools (the two engineers), `phase4_ch16_build.py`, `phase4_ch20_build.py` and chapter 20's specimens (the design director's turn 1), and their notes.
- Bytes (DR-271; nothing cut). `21-atlas.json` 52,523 to 55,000; chapter 21's 36 guide files (the chapter, its manifest and 34 specimens) together 156,526 to 160,087, of which the twelve that moved account for all of the change. The generator ends at SHA-256 `01f826c5564fd474…`. In the built page, measured as two strict builds inside one hold of the lock at 18:04 UTC, the second with HEAD's versions of only my output files and mine restored after (checked byte for byte): chapter 21's section 1,124,671 to 1,128,286 (+3,615), the page 14,216,876 to 14,220,491 (+3,615), no other chapter moved. The two builds carry the same 52 warnings.

## Requests

1. **Atlas engineer:** the keys under "Words for", items 1 to 21, and first the three new fills in A13 `whole_note`, which print as braces until the kit fills them. Items 22 and 23 are the kit's frame alts (DF6, and DF5 ahead of turn 2).
2. **Design director, turn 2 on this file:** keep or move my two code changes (CD-S5's `view_words()`, DF1's `typo()`); confirm "Numbered loops" (R27) at its column's width; check CR-3 for the longer lit words in the boxes and cards; and look at the chips plate with RL19's and DL05's sentences, which wrap under their chips.
3. **Main session:** the strict build reads exit 1 now, on stale kit plates and the atlas test's self-test, none from my output (Tested). Once the engineers rebuild the kit (A04 to A10 for chapter 20, A11 to A20 for chapter 21), the run order is the generator, the kit, the generator again, then the strict build.
4. **For my turn 2 (noted from the main session's message, 18:00 UTC):** the accessibility lead's two specification rows for Rule 20.1, "Order" and "Headings" (their notes, Requests), in my words, in `phase4_ch20_build.py`.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

None. Every turn 1 code is under "Done". The page effect of CE1, CE8, RP1, RP4, ST-1, ST-2, DF6, AX-3 and AX-4 waits on the atlas engineer's kit work, which reads these words.

## Tested

- `phase4_ch21_build.py --check` under the lock: exit 1 once (17:58:21 UTC, three intro paragraphs; fixed), then exit 0 at 17:58:44, 17:59:17 and 18:03:43 UTC; last: 16 rules, 34 specimens, 87,827 bytes before the kit's frames. Chapter 02's mechanical checks (`check_copy`) ran on every field.
- `--page-words all` under the lock: exit 0. Against the 17:50 copy: no key removed, 13 keys added, 8 values changed, as listed; the six tab titles unchanged; the stepper holds 9,250 and 16,000 ms, unchanged.
- The generator written under the lock at 18:00:14 and 18:04:16 UTC: exit 0 both times.
- Every stored name quoted under "Words for" read from `work/extract/atlas-v7-data.json`: Reforms R-24, R-25, R-26 and R-31, Loop R6, Connections L14, L15, L18 and L19, Variables A4, EC7, D1, D2 and D4 with their `increase_means`, RL19's `rule`, DL05's `what_was_done`; the reforms aimed at A4.
- `typo()` on five stored strings by script before the run, then on the built specimens by word diff.
- Script scan of chapter 21's JSON, its manifest and the six pages' words (`wordscan.py`): em dashes 0, en dashes 0, fillers 0, corporate verbs 0, hedges 0, straight apostrophes 0, "dark mode" 0, a bare sheet code 0, "flow" 0, studio words on public pages 0. "never" 1 (How to read's fact, kept). Every "not" read by hand (29, 19 of them the plates' "Failure case: do not publish" prefix and Rule 15.10's heading "Reviewed and not drawn"): conditions and plain facts, no corrective turn.
- Word search of the two built pages (18:04 UTC), old and new phrases counted: each new phrase appears where it should, and "with a count on every flow", "never less than six seconds", "Ink tag, aims here" and "Sheet D04’s reforms" are gone. "This question reaches here" (30) and "can't" (7) remain inside the kit's frames, which change when the kit is rebuilt.
- The strict build to scratch under the lock, three times (18:00:32, 18:04:30 and the HEAD-outputs build at 18:04:47 UTC): exit 1 each time, 52 warnings, 0 from my output. 51 are stale kit plates: 19 with only kit inputs changed (chapter 20's A04 to A10, and A15) and 32 whose inputs include my words in the generator together with the kit files the atlas engineer changed (A11 to A14, A16 to A20); one is the atlas test's self-test on the plates, "29 plants, 2 miss(es)", from the engineer's test in progress. 409 rules and 765 specimens placed in both.
- The restore after the HEAD-outputs build: each of my eleven files compared byte for byte with its saved copy, 0 mismatches.
- A full read of every changed string, from the diff of `21-atlas.json` and the page words, against chapter 02's rules.
- Pattern violations remaining in chapter 21's words and plates, by type (script, then my read): em dashes 0; en dashes 0; fillers 0; corporate verbs 0; hedges 0; corrective "X, never Y" turns 0; straight apostrophes in stored text on this file's plates 0; "flow" for an arrow 0; studio words on public pages 0; bare sheet codes 0; "dark mode" 0. By hand: no rhetorical triplet, parallel run, setup and payoff or slogan close found in the changed strings; the read-aloud line repeats one clause shape a step by design, as chapter 15's does.

## Not tested

- A clean strict build (exit 0, 0 warnings, 0 stale plates): it waits on the kit's rebuilds, which are the engineers'.
- My words on drawn pages: the kit has not drawn A11 to A20 with them, so no frame, status line, label or alt of mine has been checked by the atlas test or seen in a browser. I opened no browser.
- The widths of the new words in the kit's boxes, cards and table heads ("The question you pressed reaches here", "Numbered loops", "In our atlas: …").
- The guide check, which the main session runs.
- How the words sound read aloud by a person or a real screen reader. My read for rhetorical triplets, parallel runs, landing lines and setup and payoff is by hand; no script rules them out.

## Turn 1 done, 18:07 UTC

Turn 1 ends here; turn 2 takes chapters 16 and 20 in `phase4_ch16_build.py` and `phase4_ch20_build.py`, and the design director takes this file.
