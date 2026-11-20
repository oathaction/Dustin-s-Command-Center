# Board 3, editor notes

Written November 20, 2026, by the editor (`oa-editor`). Brief: `20261120_Board-3-Brief.md`, row "Editor", with the coordinator's task and its correction (the builder alone writes the board's output files, so I did not run `board_3_build.py`). Read first: my role file, the project's `CLAUDE.md`, chapter 02's writing rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`), the brief, the research lead's notes, the data lead's notes, the builder's notes, the decision log rows the items cite, and the board's first full build (`work/boards/phase-3/review-4-5/board-3/20261120_Board-3.html`, 17:53 UTC) read whole. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/board-3/editor/`.

## Status

EDITOR FIX ROUND DONE, 18:39 UTC. Every item assigned to me is in the two JSON files, B3-M1's ruling included (D3-2301): decision file 156,907 bytes, content file 28,126 bytes. The builder reruns when the main session says. See "Fix round" below.

EDITOR DONE, 18:18 UTC. Both JSON files carry my words: `work/handoffs/phase-3/20261120_Board-3-Decisions.json` (154,682 bytes) and `work/boards/phase-3/review-4-5/board-3/20261120_Board-3-Content.json` (27,940 bytes). The builder reruns when the main session says; the board on disk (18:09 UTC) predates my edits. Nothing blocks.

One risk: the builder was still adding slots to the content file while I worked (18:09 and 18:14 UTC). Every write I made read the file fresh and changed only word fields, so its additions are kept. If the builder writes the content file again from a copy it read before 18:15 UTC, my words there are lost; the list under "Content file" says what to look for.

## Fix round

From the creative director's review (`20261120_CD-Review-Of-Board-3.md`) and the coordinator's list. The main session's 18:33 UTC page figures in the decision file (12,178,909 bytes, 459,191, the version 13 report path) are kept. I did not run the builder.

- **B3-M2, masthead-360.** Title, answer, recommendation, what changed, the four picture labels and reply 10 now say 360 to 372 px: the switch at 372 px (23.25em, the register's range), so phones 375 px wide keep the 24 px wordmark, which already fits on one line there. The design director's look is now stated for 360 px, the width that changes. The two "with the 16 px wordmark" pictures were made with the switch at about 376 px; at 360 px that is the same picture as a 372 px switch, and the 375 px one is now labeled "for comparison only". Builder: fold that last picture if you like; its `row` pairs it with "Today at 375 px".
- **B3-S3, reply 16 (15.15-read-aloud).** Touches now names "the read-aloud line, a device of the atlas visual system you settled (DR-36)"; the parenthesis moves to the reference line, and DR-36 is in `refs`. Respects says the line keeps the system's rule: it starts with a rise and flips at each minus sign. The check the review asks for: the key line "Built from the signs: start with more, flip at each minus." sits only in DR-36's finishing list (`work/handoffs/phase-2/20261105_CD-Review-Of-Editorial-Systems.md`, item 6); no chapter, plate or generator prints it today (searched `work/build/guide/` and the build scripts). The new form starts with a rise, so if that key line is ever printed beside a read-aloud line, its words become "start with a rise, flip at each minus".
- **B3-S4, the second pass score table (content file).** `scores.second_lede` adds "Each cell gives the score after the fix pass, small, then the score after the second pass." and `second_line` ends "and with this pass every item of rounds 4 and 5 is ready." (true by the rescore file and the second pass file, 13 then 14 of 14; D3-2292). No number is written into the words.
- **B3-S8, the keyline item.** The creative director's view is in a new `views` key on `red-target-keyline`, board 2's schema (`who`, `text`, `source`), and the content file's `decide.view_by` is board 2's "The {who}’s view.". Builder: `decide_item()` in `board_3_build.py` has no views block; board 2's (`board_2_build.py`, lines 897 to 900) sets each view as a blockquote, and it belongs right after the recommendation. The quote is the review's "My view on the keyline, for panel 1" word for word, but for two bracketed changes that keep decision codes off the face ("after [he chose] the atlas system" for "after DR-36 chose the atlas system"; "[His choice] made" for "DR-36 made") and curled apostrophes.
- **B3-S9, panel 6.** `counts.dr_229.test` ends with its full stop. A `--counts-only` run rewrites that key from the counts script, so the script needs the full stop too (data lead or main session).
- **B3-M1, the keyline item, with the accessibility lead's ruling and the main session's D3-2301.** The answer ends on the ruling in one sentence: without the keyline Rules 15.11, 15.16, 15.20 and 14.144 still meet WCAG 2.2 AA, because each names every red target in words beside the drawing, and Rule 15.12 falls short, because its words never name its one red variable, "Availability of local reporting". What changed ends on the grayscale cost in one sentence (the creative director's luma reading of Rule 15.11: mid gray and weakest today, strongest with the keyline). The recommendation keeps D3-2284's substance (the atlas target as settled, the keyline and edge off Rules 15.20 and 14.144, "Keyline everywhere" as the named reply) and adds D3-2301's part: Rule 15.12 names its red variable in the plate's own words once Dustin answers, so all five plates meet AA with no change to the settled mark. The old cost sentence ("on Newsprint the red ring stays at 2.96 to 1 on all five plates, under the 3 to 1 that Rule 05.5 and … WCAG 2.2, 1.4.11 ask …") is gone; the cost now reads "the five plates go without Rule 05.5’s keyline, so in grayscale their red targets read weakest". Touches adds the words of Rule 15.12's plate, respects says those words leave its marks as drawn, `refs` gains D3-2301, and reply 11 carries the extended recommendation.
- **B3-S5.** The builder has not asked; I am ready to write each picture's one fact into an `alt` key on its picture, which `picture_alt()` already reads first.
- Not mine but noted: B3-S2 says S59's sketch also prints 2027's "4.1"; the item's "Only the label’s place moves." stays true of the proposal, and the sketch is the builder's to correct or for me to describe once the builder says which.

Lint after the fix round (`face.py`): 0 em or en dashes, flagged words, decision codes, studio codes or paths on panel 1's face.

## What I changed and why

Every change is words only. No item id, count, picture element, page, width, row or fold changed, and every studio code I took out of a sentence went into the item's `refs`, so the reference lines still carry it. Originals are in scratch (`orig-Decisions.json`, `orig-Content.json`); the scripts that made the edits are in `scripts/` there.

### The research lead's corrections

| Item | Original | Revision | Source |
|---|---|---|---|
| `routes-who`, picture label (and so its alt) | "Rule 15.20 today: R-03’s federal statute route prints an action where it means who acts" | "Rule 15.20 today: under R-03’s federal statute route, the atlas’s words name an action, where the card’s other routes name who acts" | W1, F32a |
| `Q-12`, what changed | "Nothing. The question has stood since Gate 1; the guide flags the need and assumes no filing." | W2's words, with "the register" said as "the list of deferred fixes" | W2 |
| `Q-12`, recommendation | "Yes, before Phase 5’s release; the guide keeps its flag until the attorney reports. The research lead adds the facts." | W3's words, plus "Chapter 04 is approved, so a yes here also approves that sentence." (the research lead's note that the sentence is Dustin's call) | W3 |
| `15.22-examples`, recommendation | "State the rule in the note, for example the most recent sunset and the most recent repeal the research lead found, with the date searched. The laws stay as the rule finds them …" | Recommends W4's first choice, the rule the files show (both are the child tax credit's own laws, which S30 charts; 2017 set the end date, 2025 struck it), and offers W4's second choice as a named reply, "Run the search". Its why now says no such search has run | W4; a call below |
| `S40`, what changed | "Four cells such as …" | "Five cells such as …" | W5 |
| `S71-retrieved`, title, answer, recommendation, what changed, why, touches | S71 alone, "where every other date says “retrieved”" | All six places (S71, S41, S42, S53, S67, Rule 01.5's map), with W6's answer, and Rule 14.101's own instruction, "the date it was read", changed to match | W6; a call below |

Later items in the research lead's notes:

- F5 and F7, routes-who: the answer said "move an instrument or an action to the route’s note or a new field". It now says "into a field of its own, as the atlas’s eleven route records already do", and the why says the notes already hold text on 50 entries, as the research lead's call and row 46's wording set.
- F15, S14: "The data, the scale and the title are as board 1 approved" became "The data and the title …", since the research lead confirmed those two and did not compare the scale.
- F32b, Rule 15.25: the content file's `recon_lede` promised rows for the atlas's next version and the board prints none under that head. The lede now names the two rows that concern V7.1 (row 56, which panel 1 asks about, and row 57, already on the list from board 2) and drops "Gate 3 decides any new item".
- F16 (S14's "October 2026 release" clause) and W7 (Rule 15.25 row 50) are words in the guide, not in my two files: see "For the main session".

### The decision file, item by item

Panel 1 now opens each item with its answer in a sentence or two and the recommendation in plain words. Across all 39 items:

- Decision and studio codes left every sentence on the face (the build had warned on 15: D3-1701, D3-1705, D3-1712, D3-2140, D3-2142, D3-2243, D3-689, DR-108, DR-231, DR-265, DR-271, DR-274, DR-278, DR-62, Q-12), and so did "call 15", "ruling (d)", "CR-S1’s remainder", "AX-S5", "DF-16", "ED5-3" and the like. A code becomes what it refers to ("you approved the bill tracker’s six names by name", "as you asked at board 2") and stays in `refs`.
- Studio words a reader would not know became plain ones: alt became "text description" (defined once as the words a screen reader speaks for a picture), spec key and opt-in became "a setting in the chart’s own file", the shell became "the page frame", the register "the list of deferred fixes", scratch "a working copy", image stage "plate picture", edge guard "label-clearance check", tabular figures "figures set at a fixed width", sweep "a run at every width". Code spans (`labels.latest_clear`, `date-lead`, `oa-choice-row--list`, `data-oa-live`, `form[data-oa-form]`, `.tok-v`, `text-wrap: pretty`, `evidence_layout`, `s-11-steps`, `plate()`, `who`) left the face.
- Terms defined at first use: pips ("the one to three small marks that size an effect"), context ink ("the gray for what a title does not name"), chart token ("a value all charts share"), read-aloud line ("the sentence under a loop that reads it step by step"), evidence chip ("the tag naming its kind of evidence"), WCAG 2.4.11 and 1.4.10 by what they ask, Reform R-03 by its title (house rule H11).
- Consistency: the masthead item said 1,024 to 1,362 px in its answer and 1,360 in its why; both now say 1,362, the measured range in the change ledger (C-132). Numbers under ten in prose are words (house rule H06): "four of 107 source lines", "five an action". " ... " became " … ", since the builder's spacing rule turned " ... " into "...".
- Titles: four retitled to say what the item is ("Words inside pictures: heard once", "A focused link stays clear of the masthead", "Chapter 18’s code and the page frame", "“Read” or “retrieved” for the date a source was taken", among others). Picture labels: S07's "1 px apart from the gap token", Rule 15.11's "before" and the masthead's "rail link" now say what they show.
- Group ledes rewritten: the trackers' and the V7.1 row's lose their codes; "16 changes" and "16 rows … and 2 more" open on words; the held group's lede counts its twenty choices by source.
- The 24 replies: each line now names the choice, and each recommendation is one short instruction that matches its item. Reply words fell from 777 to 513.
- Panel 1's words, folds closed: the items rose from 5,414 to 5,953 (plain words where codes stood, and the research lead's corrections), the replies fell by 264, so the panel reads about 275 words longer, near 38 minutes. The sixteen example lines sit in a closed fold.
- Counts: `rule_01_9.note` and `dr_229.note` lose "domain", "the generator’s log" and "D3-689’s test". A `--counts-only` run keeps both notes.
- `words_edited_by` and `words_edited_utc` added at the top level. Nothing reads them.

Items whose substance I changed or kept with care:

- **red-target-keyline (D3-2284).** Substance kept exactly: keep the atlas's red target as Dustin settled it, the keyline and the arrowhead's ink edge come off Rules 15.20 and 14.144, the cost is stated, and the keyline everywhere takes his named reply "Keyline everywhere". Words only: codes out, WCAG named as "the web accessibility standard (WCAG 2.2, 1.4.11)", and one figure for one measure. The item printed Pillar Red at 2.96 to 1 in its answer (Rule 05.5's figure) and 2.95 in its recommendation and what changed (the palette plate's rounding down), the very split that the pillar-red-ratio item puts to Dustin. It now says 2.96 throughout, as chapter 05 prints it; the measure is 2.9568 and the ring is under 3 to 1 either way. What changed no longer repeats the 3 to 1 sentence the recommendation carries.
- **S14-line-02-13.** The recommendation said "Update both copies". Rule 02.22 is chapter 02's house rules, part of the writing section Dustin approved "with every before and after as printed" (DR-73), and chapter 02's writing rules are on his settled list. So "As recommended" would have changed a settled element. It now updates chapter 13's copies, keeps chapter 02's older line (true of the same data) and offers the named reply "Chapter 02 too". The why, touches and respects say so.
- **15.22-examples.** W4 gave two choices and no recommendation; each panel 1 item has to carry one. I recommend the rule the files show, since it needs no new search and is true today, and offer the search as "Run the search". Either way no law is swapped (DR-93).
- **masthead-360.** The design director has now looked at 360 and 375 px (the builder's notes) and sees nothing against the switch, so the recommendation says so in place of "with the design director’s look first". The why said "a change to identity needs your named approval (gate rule 4)"; neither wordmark's drawing changes, so it now says the change moves where the two approved masters meet and waits on his reply, as the register's row puts it.
- **CE-S22-examples.** The sixteen lines are written (below), shown in a closed fold as a table (`rows`, keys `question` and `example`), and the two for the picture are in the to-make picture's new `lines` key, with its owner now the board builder.

### The content file

Changed words, each checked against the words I read before I wrote:

- `sections.decide.lede`, `alt_made` ("in scratch" became "in a working copy").
- `sections.spend.lede` ("Under DR-271 …" became "As you decided, …") and `parts_line` ("The first row adds up the next three").
- `sections.ch15.recon_lede` (F32b).
- `sections.tested`: the kit build line ("build --all --no-png on the final tree" became "the kit built every chart from the final files, without pictures"), "Chapter 14’s generator check" became "Chapter 14’s build check" with plain words, "kit specs" became "kit chart files", "anchor" became "target" twice, and the board check's line reads "{failures} failures apart from the page’s language, which the host sets when it wraps the page".
- `slots.made.*.how` for masthead-360, red-target-keyline, CR-S19-chip, related-rules, NB-S4, S59-label and CE-S22-examples: no "scratch", "spec", "flag", "opt-in key" or "22.49em"; the slots' `set`, `patch`, `spec` and `rule` keys are untouched.

## The sixteen example lines, for the finishing pass

Under each question in "Choose a chart", before its skip link, in the tier words' type. None holds an invented figure, person or place, so none needs the Illustrative label; the years name real elections and a real data span. Three of the sixteen touch voting, under Rule 01.9's one in four. Each line is 39 to 80 bytes as text.

| Question | Example line |
|---|---|
| Comparison: which is bigger, and how do they rank? | Which states spend the most per student on public schools? |
| Shift and swing: what moved, and which way? | Did turnout rise or fall in each state from 2020 to 2024? |
| Change over time: how has it moved? | How have job numbers moved month by month since 2022? |
| Composition: what is it made of? | What makes up my monthly electric bill? |
| Distribution and density: how are the values spread? | How long do most voters wait in line, and how many wait over an hour? |
| Correlation: do two things move together? | Do counties with more broadband also have more people working from home? |
| Uncertainty and estimates: how sure is it? | How sure is the survey’s count of people without health insurance in my state? |
| Proportion and overlap: how much, and how do groups overlap? | How many people qualify for both Medicare and Medicaid? |
| Gauges and indicators: where does it stand now? | How much of the road repair money has the city spent so far? |
| Behavior: how do people move through a process? | How many people who start an unemployment claim finish it? |
| Structure: who decides, and how does it work? | Who has to sign off before a new bus route starts? |
| Relationships: who is connected to whom? | Which agencies share responsibility for my drinking water? |
| Flow: where does it go? | Where does the money from the gas tax end up? |
| Maps: where is it happening? | Which counties have no hospital that delivers babies? |
| Tables and plain words: where does a reader look things up, and when do words answer faster? | What is the minimum wage in my state this year? |
| Infographics: how does it work, in one look? | What does my mail ballot envelope ask me to fill in? |

The three pairs the civic education reader found alike read apart: two dates and a direction against a run of months; the parts of one bill against two groups that overlap; who signs off against what one form asks.

## Words for

**The builder.**

1. CE-S22-examples' picture: the two lines and their questions are in the decision file (`pictures[0].lines`) and in the table above: "Did turnout rise or fall in each state from 2020 to 2024?" under "Shift and swing: what moved, and which way?", and "How have job numbers moved month by month since 2022?" under "Change over time: how has it moved?".
2. The 14.144 states' alts lowercase "Reform": "reform R-30 chosen", "reform R-38 chosen", where the label and the first state keep "Reform R-06". A reform's name keeps its capital.
3. Panel 5's heaviest charts print S96 with no rule and its form as the code `columns-moving-average`. S96 is Rule 14.142's chart in full, form "Columns with a moving average".
4. My flags differ from the brief's: I did not run the builder (the coordinator's correction). The brief's command stands for your rerun: `python3 -I work/build/scripts/phase-3/board_3_build.py --final work/boards/phase-3/review-4-5/20261120_Guide-Preview-V13.html --reuse --check`.

**The data lead.** The counts script writes words a `--counts-only` run would restore, so I left them: `dr_229.test` prints as a paragraph with no full stop ("A form keeps election data only where the coverage plan writes its use as an election question"); the examples' test words use straight apostrophes ("a rule's own plate") and one says "(round 5 ruling (g))" on the face. Suggested: "A form keeps election data only where the coverage plan writes its use as an election question." and "Not applied: one of the three complex examples Gate 2 named, approved with the Phase 3 proposal; it draws no form of the coverage plan". Also, C-130 lists "the card’s desk and phone classes" for board 3; no panel 1 item names them, and I could not tell whether they reach approved work.

**The main session.**

1. Settled-list read: the S14-line-02-13 change above. Two more I left as written but flag: Rule 15.15's read-aloud form comes from System 1's `read_aloud` (the build's own comment), so confirm the line is text and not part of the atlas visual system (DR-36); CR-S19's layout adds a second chart header for three charts not yet approved, inside the chart system (DR-52), and moves no approved chart.
2. D3-2292: a "Keep the atlas target" answer reopens C15-I and R5-3 for a rescore. The item states the contrast cost; it does not say the creative director rescores two items. I left the item's substance as D3-2284 set it.
3. F16, for S14's spec owner, if S14's approval allows one more word change: "from the technical note to its October 2026 report, posted November 6, 2026", in place of "technical note, October 2026 release".
4. W7, for the chapter 15 generator's owner: Rule 15.25 row 50 should say D6's "kind in words" opens "Stock (an amount built up over time)", where it says "description".

## Calls

- D3-xxx | Apply the research lead's W1 to W6 as written, with "the register" said as "the list of deferred fixes" | W1 to W6 are facts checked against their sources; the register's name is a studio word on the face
- D3-xxx | 15.22-examples recommends the rule the files show and offers the search as the named reply "Run the search" | each panel 1 item carries one recommendation, the files' rule is true today, and no one has run the search
- D3-xxx | S71-retrieved covers all six places and Rule 14.101's own words | one kind of date takes one word (Rule 13.6), and a rule that says "the date it was read" would contradict its own chart once S71 says "retrieved"
- D3-xxx | S14-line-02-13 keeps chapter 02's copy as settled, updates chapter 13's, and offers "Chapter 02 too" | Rule 02.22 belongs to the writing section DR-73 approved with every example as printed, and "As recommended" must never change a settled element (D3-2284)
- D3-xxx | The keyline item prints Pillar Red's ratio as 2.96 to 1 throughout, chapter 05's figure | one measure took two figures inside one item, the split the pillar-red-ratio item asks about; substance unchanged
- D3-xxx | masthead-360 says the design director has looked, and drops "named approval (gate rule 4)" | the builder's notes record the look at 360 and 375 px, and the change moves no identity geometry
- D3-xxx | routes-who proposes a field of its own, not the note | the research lead's call and row 46: the note already holds text on 50 entries
- D3-xxx | S14's what changed claims the data and title as board 1 approved, not the scale | the research lead compared the data and title and not the scale
- D3-xxx | The sixteen example lines go on the board in a closed fold as well as in these notes | Dustin cannot approve lines he cannot read, and a closed fold adds no reading time
- D3-xxx | Codes leave sentences and stay in `refs`; studio words become plain words | chapter 02's rules and the brief: decision codes and file paths only in small reference lines
- D3-xxx | The masthead item recommends the switch at 372 px and labels the 375 px sketch "for comparison only" | B3-M2: the fault runs 360 to 372 px, and at 375 px the 24 px wordmark already fits on one line
- D3-xxx | The creative director's keyline view goes in board 2's `views` key, quoted, with two decision codes set as bracketed words | B3-S8 asks for the view beside the recommendation, and the board's face carries no decision code
- D3-xxx | The keyline's grayscale cost sits in what changed, and a short form of it is the recommendation's cost | the coordinator asked for one sentence on it; the full sentence describes the two looks, the short one prices the choice

## Tested

- Fix round (18:33 to 18:40 UTC): each change read the file fresh and checked the exact words it replaced, with the main session's 18:33 figures kept; `face.py` after it: 0 em or en dashes, flagged words, decision codes, studio codes or paths on panel 1's face, and no "3 to 1" left in the keyline item; D3-2301 is in the decision log; the read-aloud key line searched across `work/build/guide/` and the build scripts (not printed).
- Both files parse as JSON and round-trip byte for byte in the generator's format (indent 1, no ASCII escapes, a closing newline); neither holds an em dash or an en dash.
- By script against my scratch copy of the original: the same panels, items and ids in the same order; every picture's kind, page, element, width, row, role, fold and path; and every item's steps, marks, counts, verb-led rows, top values, reply numbers, `question_for_dustin` and `shows`. In the counts, only the two notes differ.
- Every decision code in an item's `refs` (46) is in the decision log or the open questions.
- `face.py` (scratch), which prints panel 1's words as `decide_item()` and `decide_panel()` set them, including the builder's rule that moves a parenthesis of codes: 0 em dashes, 0 en dashes, 0 flagged words from board 1's list, 0 decision codes, 0 studio codes and 0 file paths on the face. Its figure check and its negation scan, both read by hand: the figures left are ratios, measures and counts in data; the one "X, not Y" turn (the weight estimate) is rewritten.
- Word counts of panel 1's fields before and after, by item.
- The sixteen example lines: 39 to 80 bytes each.
- Each content file change read the file fresh and checked the words it replaced, so the builder's additions of 18:09 and 18:14 UTC stayed.
- A full read of panel 1 as printed, item by item, against chapter 02's rules, and of the content file's own words; the board of 17:53 UTC read whole as text.
- The facts behind my rewrites, in the files: the masthead's 1,362 px (C-132 and the fix pass notes), Rule 14.101's "the date it was read" (`14-101.json`), Rule 02.22 as the house rules (`02-voice.json`), Reform R-03's title (the atlas extract), Rule 14.6's "Charcoal at the subject weight" (`14-006.json`), the builder's masthead look and its 89 px.

## Not tested

- The board with my words: the builder has not rerun, and I opened no browser. Whether every word fits its box, at 1440 or 390 px, is unseen.
- That the builder's `rows_table()` sets the sixteen lines as I expect; I read the code, and `face.py` mimics it.
- How the words sound read aloud to Dustin; no script finds triplets, parallel runs or landing lines, so those rest on my read.
- The facts I did not write: the trackers' steps and laws, the counts, the V7.1 figures and Q-12's facts stand as the data lead and the research lead checked them.
- Panels 2 to 9's quoted words (titles, source lines, tables, captions), which come from the guide's files and are not mine to change.

## Change log

- Modified: `work/handoffs/phase-3/20261120_Board-3-Decisions.json` (words; `rows` and `lines` added to CE-S22-examples; `words_edited_by` and `words_edited_utc` at the top level).
- Modified: `work/boards/phase-3/review-4-5/board-3/20261120_Board-3-Content.json` (words only).
- Created: `work/handoffs/phase-3/20261120_Board-3-Editor-Notes.md` (this file).
- Scratch only: the originals, the edit scripts and `face.py`.
