# Stage B round 3 fix pass: editor's notes

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the editor (`.claude/agents/oa-editor.md`), run as a subagent of the main session, under `20261110_Stage-B-Round-3-Fix-Brief.md` ("The editor", items 1 to 7, and the craft items routed to me: CA-S7's words, CA-S9 for `s-01-21-correct`, CA-S15). I am a new agent in this role and worked from my round 2 notes. I committed nothing and published nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: items 1 to 8 done. Item 8, the read after the pass (D2-963), is section 8 below: 14 faults for the short second pass, in other owners' files, and one description fixed in my own questions file. The engineer's ID pass (D2-975) was not marked done when I finished, so its strings are listed as not read. The A-5 failure on `s-01-pieces` noted below is gone: the engineer's check now counts only the row on screen (chapter 11 hand's notes, item 3).

## For the other owners, first

**Chapter 11 hand, `s-01-pieces`.** The Track card's marks come from chapter 11's module, read live by my generator. The place to edit is `work/build/scripts/phase-2/guide_editor_ch01.py`, two functions only:
- `track_css()`, which writes the plate's mark CSS from `apply_systems_ch11.py` (`mark_vars`, `MARK_CSS`, `piece_css`);
- `track_steps()`, which draws the six steps with `steps_svg(states, STEPS_ROW, 24)` and the key with `key(...)`.

Edit those two functions in place, or send me the class names and I will. I keep my own edits out of both functions this pass, so the two sets of changes cannot cross. After either of us edits them, run `python3 -I work/build/scripts/phase-2/guide_editor_build.py`, then `python3 -I work/build/scripts/phase-2/stage_b_identity_ch01.py` (D2-912).

**Chapter 11 hand, a failure your `steps_svg` change brings into `s-01-pieces`.** With the status family on each mark, `guide_check.js` fails `s-01-pieces` four times (A-5, "S-done 4 of 6", at all four widths). The Track card draws its row twice, a 324 px copy and a 288 px copy for screens under 24.25em (`track_steps()`, `.mkw.wd` and `.mkw.nw`), and the check counts the marks in both while the words say each state once. A build with the committed `s-01-pieces` passes, so the cause is the doubled row, not the words. Two ways out, for you and the engineer to pick: draw one row in `track_steps()` that holds its 13 px numbers at both widths, or have the check count only the copy that is displayed. I have not touched either function.

**Systems designer, CA-S7's words for Rule 10.2** (`stage_b_ch10_build.py`; the words are yours to set, and I read them again in the read after this pass):

| Field | Old | New | Rule |
|---|---|---|---|
| Rule 10.2, `title` | Build every drawing on one box, with one line, round ends and one red part. | Build every drawing on one box, with one line, round ends and one red accent. | CA-S7: the accent is one idea, which may take more than one shape |
| Rule 10.2, `rule[0]`, from its third sentence | One part carries the red accent, the detail a reader should see first, such as the door of the hall in Local government. The rest is ink. | The red accent marks one idea, the detail a reader should see first, such as the door of the hall in Local government. It may take one shape or a few, as Track’s icon in chapter 09 colors both its map pin and its magnifier’s handle. The rest is ink. | CA-S7; chapter 09's alt names Track's two red parts, the pin and the handle |
| Rule 10.2, spec "Red" | One accent, in the file’s group `data-part="accent"` | One accent for one idea, in one shape or several, all in the file’s group `data-part="accent"` | CA-S7, so the spec and the rule say the same thing |

**Systems designer, PP-S3.** Rule 01.21 now carries this sentence for a subject with no drawing, after DR-196: "A subject that none of the 37 stands for, such as Housing, takes its word alone." It names the 37 because a kicker may hold only those (Rule 10.4). If your sentence for Rule 10.6 or 10.9 words it differently, post it under "For the editor" in your notes and I will match Rule 01.21 to it; the verb "takes its word alone" is DR-196's and Rule 10.2's.

**Identity designer, two follow-ons from BE-S7.** Rule 01.21 now allows a topic or atlas symbol from the 37 in a kicker, so:
- Rule 09.4's "which may carry a topic icon only (Rule 01.21)" (4b's row would make it "a topic symbol only") now reads against Rule 01.21. Suggested: "It stays out of kickers, which may carry only a topic or atlas symbol (Rule 01.21), and off part openers."
- `stage_b_identity_ch01.py` gives the kicker's CL-057 `data-icon-family="topic"`; chapter 10 files CL-057 under `atlas` (Variable EC3), and Rule 01.21's words and alt now call it an atlas symbol. Suggested: `data-icon-family="atlas"` for CL-057 in `topic()` or its caller.

## Items

| Item | What | Status |
|---|---|---|
| 1. D2-950 | Step 4 of the reader check takes a neutral name | done |
| 2. PP-S13 | Step 7's footer question | done |
| 3. BE-S7, PP-S3 | Rule 01.21: a topic or atlas symbol from the 37; a subject with no drawing | done; the sentence waits to be matched to the systems designer's, if theirs differs |
| 4. PP-S12 | Rule 01.11: Virginia's statewide vote by voters | done |
| 5. CD-S14, CA-S15 | Rule 01.11: the count's source line in H04's order, one source per line, "How we counted" | done |
| 6. CD-S15 | `s-01-pillars`: "On a page that serves Track, at 48 px" | done |
| 7. BE-S8 | Chapter 01's source lines that name no period | done: two atlas lines |
| CA-S9 | `s-01-21-correct`: the Illustrative label in one place | done |
| CA-S7 | Rule 10.2's words, for the systems designer | posted above |
| 8. D2-963 | The read of every changed string | done; table in section 8 |

## What I did, item by item

Every chapter 01 change went into `work/build/scripts/phase-2/guide_editor_ch01.py`. I then ran `guide_editor_build.py` and `stage_b_identity_ch01.py` (D2-912) and compared every output with the copies I saved before the run.

### 1. Step 4's name (D2-950), and a note for the engineer

`20261110_Reader-Check-2-Questions.md`: the flow table's "Name on the page" for step 4 and the step's heading now read "A card and a drawing", the words its ready screen already used. One new line under the heading says the name holds wherever the page names its steps. A note near the top of the file lists both round 3 changes.

**For the engineer.** In `work/boards/phase-2/reader-check-2/reader_check_2_template.html`:
- `STEP_NAMES` gives step 4 as `'Red'` (line 578 as I read it); it becomes `'A card and a drawing'`.
- The copy text's section heading for step 4 is also `'Red'` (the `lines.push('', 'Red', ...)` call, line 847). PP-S14's rewrite of the readable lines is yours; that heading takes the step's new name too.
- Step 7's question (`foot_24:seen`, line 447) takes the words in item 2. Its eyebrow, "The bottom of a page", names the picture and can stay.

### 2. Step 7's footer question (PP-S13)

Now: "Look at the small square mark beside the line of text. What did you see in it?" A line under it says why: the question screen hides the picture, and in the picture the mark sits near the top. Choices, codes and pass rule are unchanged.

### 3. Rule 01.21 (BE-S7, PP-S3, DR-196)

| Field | Old | New | Rule |
|---|---|---|---|
| `rule[1]` | Set the kicker in words. The one picture it may hold is a topic symbol from the Civic Line, our set of symbols in chapter 10, placed directly before the topic’s own word. Pillar icons… | Set the kicker in words. The one picture it may hold is a topic or atlas symbol from the 37 that read at 24 px (Rule 10.4), placed directly before its own word. Both come from the Civic Line, our set of symbols in chapter 10, and an atlas symbol stands for a part of our systems atlas, so its word is the atlas’s name for it. A subject that none of the 37 stands for, such as Housing, takes its word alone. Pillar icons… | BE-S7: CL-057 is an atlas symbol (Variable EC3); PP-S3 and DR-196: a subject with no drawing takes its word alone; H02 for "atlas symbol" at its first use in chapter 01 |
| `why.text`, second sentence | A topic symbol beside its own word shows the subject a second way. | A symbol beside its own word shows the subject a second way. | Follows the rule |
| spec | "Topic icon": Optional: a Civic Line icon at 24 px in one color, 8 px before the topic’s own word, only when the second part is a topic | "Kicker symbol": Optional: a topic or atlas symbol from the 37 that read at 24 px (Rule 10.4), in one color, 8 px before its own word, only when the second part is a topic | BE-S7; "topic icon" was the last of chapter 01's old term (round 2's D2 call on "topic symbol") |
| `builders` | Add a topic symbol only when the kicker’s second part is the word that symbol names | Add a topic or atlas symbol from the 37 that read at 24 px (Rule 10.4) only when the kicker’s second part is that symbol’s own word | BE-S7 |
| `correct.caption` | the icon for workers’ share of income beside its own words … so the label sits beside each invented one | the atlas symbol for workers’ share of income beside the atlas’s name for it … so the Illustrative label ends the kicker of each invented one | BE-S7; CA-S9 |
| `s-01-21-correct` alt | with its topic symbol, a person in the wedge…; The four invented headlines carry the Illustrative label. | with its atlas symbol, a person in the wedge…; Each of the four invented headlines carries the Illustrative label at the end of its kicker. | BE-S7; CA-S9 |
| `s-01-21-failure` alt | in place of the icon for workers’ share of income | in place of the atlas symbol for workers’ share of income | BE-S7 |

"Housing" is the plain language team's case (PP-S3, Q1) and DR-196's: none of the 37 stands for it, and its drawing waits for the next drawings board. When it is approved, this example needs a swap.

### 4. Virginia's sentence (PP-S12)

`R4A_SCOPE`, last sentence. Old: "and the state’s supreme court voided the April 21, 2026 vote that approved it." New: "and the state’s supreme court voided the statewide vote of April 21, 2026, in which voters approved it." The Department of Elections' release of May 8, 2026 names the "April 21, 2026, Redistricting Referendum Special Election" (research round 2, section 4). The caption's "Virginia’s attempt, which a court voided" now reads "which voters approved and a court voided".

### 5. The count's sources and "How we counted" (CD-S14, CA-S15, DR-187)

The plate now sets, under the count paragraph:
- a short list of three source lines, one to a line: the cases' line (unchanged); "Source for the count", cut back to H04's order and its one qualification ("The count measures maps passed and says nothing about the seats they moved."); and a new "Source for Missouri’s figures", the county page in H04's order, which the old count line carried in its middle;
- a label, "How we counted", over one paragraph that holds the method and the Ohio, Missouri and Utah facts.

Every fact the round 2 plate printed is still on it: the method and its sources (member lists and minutes); Ohio's commission, five Republicans and two Democrats, 7 to 0, October 31, 2025, the constitution's deadline and its rule of two votes from each party; Missouri's vote after the snapshot, 1,273,815 no and 785,969 yes, unofficial, certification after November 17, 2026, the rule that a referred law needs voters' approval, and the 2022 districts; Utah's court-adopted map left out. I checked this by listing each figure and date in the old line and finding it in the new plate by script (Tested, below).

The new Missouri source line reads "Retrieved November 10, 2026", the day the research lead read the county page (round 2 research notes, section 1, "read November 10, 2026"). The chapter's source list gains it after the count's line. The alt text follows the plate, with "Then three source lines, each on its own line." before them. The CSS adds `.srl` (the list) and `.how` (the note), and the failure plate, which shares the style block, gains those rules with no change to what it shows.

### 6. `s-01-pillars` (CD-S15)

The second row's label reads "On a page that serves Track, at 48 px". The plate's alt follows ("Then the same row at 48 px on a page that serves Track"), and the extra's caption, which said "as the section opener’s row draws it", now says "from 48 px its icon also shows its red accent as a second sign, as Track’s icon does here." Rule 09.4 keeps "section opener" for the 128 px panel, so the term now means one thing.

### 7. BE-S8 for chapter 01

I listed every source line chapter 01 prints, 15 in all, by script. Two named no date: the Cloture glossary line and the electric bill attribution, both from the atlas. Each now ends "snapshot of October 15, 2026.", the date every other atlas line in the chapter gives. No chapter 01 line cites a statute or an undated web page, so neither of BE-S8's phrases applies. Left alone: "Our brand guide, fifth edition, chapter 13 In use", a quote from our own guide with no date to give.

### CA-S9, `s-01-21-correct`

The four invented headlines carried the label after the headline, and at the column's width one fell onto its own line. The generator now passes `illus=True` to `kicker()`, the helper chapter 01's pieces already use, so the label ends each invented item's kicker line. At 1440 px all four sit on the kicker line; at 390 px three wrap below it and stay between the kicker and the headline. The failure plate keeps its labels after the headlines: its kickers teach a wrong number of parts, and a label on those lines would read as one more part.

### CA-S7, Rule 10.2's words

Posted above for the systems designer. I edited none of their files.

## 8. The read after the pass (D2-963)

**What I read.** Every string and alt that differs from commit ddd3a898, the frozen review copy's source (D2-977), in `chapters/` and the three manifests, and the visible text of every changed specimen: 347 changed items in chapters 01, 03, 04, 05, 09, 10, 11 and 12 and the proofs (chapters 06 and 08 changed only in alt openings and markup). I pulled them by script (`git diff ddd3a898`, each JSON flattened to its strings, each specimen reduced to its visible text), set aside 35 whose only change was the "Labeled" opening or a non-breaking hyphen, and read the other 312 in full against chapter 02's rules and my section 4e terms. I also read the strings inside three live plates' scripts (the report reader's four pages, the filter's count lines, the stepper's steps), the reader check's template lines that changed, and the shell's two download labels.

**Rule 01.21 against Rule 10.6.** The systems designer's final PP-S3 paragraph in Rule 10.6 reads "A subject that no topic symbol names, such as Housing, takes its word alone. An atlas drawing appears only beside the atlas’s own name…". Rule 01.21 says "A subject that none of the 37 stands for, such as Housing, takes its word alone", with the same verb and example, and already says an atlas symbol's word "is the atlas’s name for it". They agree, so Rule 01.21 stays as it is. It names the 37 because a kicker may hold only those (Rule 10.4).

**Facts the reports set, checked:**
- The state hearing source line (chapter 11, `sources[1]`) keeps every fact of the research lead's line (`20261109_Stage-B-Research-Notes.md`, section 4): the five legislatures, their page names and dates, "five states", retrieved November 9, 2026, and the qualification on sign-up, time limits and hearings. The recast clause, "we read these five as examples and made no national count", says what "these five are examples, not a count" said, without the "not" turn (W09). "No page date" after Nebraska, Utah and Texas follows BE-S8. It passes.
- The Justice Department line matches BE-S1's fix (sections V.B.(1) and VI.B, the Justice Department and its components). Rule 11.10 takes BE-S2's sentence with "up to 10 working days" (D2-961), Rule 11.9 "the main way", and Rule 11.8 BE-S3's scope sentence word for word. The invented requests now have subjects a federal agency holds (weather station repairs, prison inspections, food safety).
- H.99009's figure, against Atlas V7 by script: connection L26, from Variable B2 to C3, is graded well supported, so "more local news raises electoral pressure" takes a direct verb (H08). R-32's remedy evidence is a hypothesis, and V7 says "no evaluation has yet shown that these funds improve coverage or accountability", so the plate's sentence holds. Loop R1's step 2 is plausible and takes "can" with D2-969's sentence.
- The chart key's title is D2-960's. Rule 10.8's plate lists all ten reforms on D02's variables, as D2-958 allows when they fit. Rule 12.5 and its caption stay on Loop R10 and Reform R-01 (DR-195).
- The tile figures in Rule 10.5 add up: 0.68, 0.66 and 0.62 of 72, 76 and 80 px give 49 to 50 px, of 48 and 52 px give 32 to 34 px, and 94 and 30 make 124.

**Terms from 4e, across the changed chapters:** "topic icon" 0; "clock" 0; "Labeled Failure case" 0, so every banded failure alt now opens "Failure case: do not publish."; "keyline" only in chapter 05's sense; "condition" only in Rule 10.1's definition of a variable; Track's job line one wording everywhere. "Plausible link" is left in chapter 04 only (row 3 below). Script scans of the 312 strings found no em or en dash, listed filler, corporate verb, hedge or studio word.

**Looked at and left alone, with a reason:**
- "Money in politics can raise policy tilt to insiders." (the chapter 11 hand asked). It keeps V7's name for Variable E1, which DR-185 prints, and the step's next sentence says what the tilt is.
- The reader check's copy text ("once", "twice", "the first step", "About the same", times in words) uses the words the reader saw. Its section heads "Rows" and "Bills" differ from the step names "The four" and "Steps". That doesn't break a rule, so I left it.
- The download labels, "Download tokens.css" and "Download tokens.css in a zip file", say what the reader gets.

**Fixed in my own file.** `20261110_Reader-Check-2-Questions.md`, row_48: its head and description said "section opener at 48 px". Rule 09.1 and `s-01-pillars` now put the 48 px row near the top of a page, and a section opener is the 128 px panel (Rule 09.4), so they now read "the 48 px row on a page that serves Track". No word a reader sees changed, so the page needs no rebuild.

### Faults for the short second pass (DR-191)

| # | File (owner, generator) | Field | Old | New | Rule |
|---|---|---|---|---|---|
| 1 | `04-ampersand.json` (identity designer) | Rule 04.6, `why.text`, the new sentence | while B’s 16 px master keeps its shape on every screen. | while B’s 16 px master keeps its shape on every screen above 1x. | W20: the same paragraph says the smooth drawing blurred on a 1x screen, which is why B switches there |
| 2 | `09-pillar-icons.json` (identity designer, `stage_b_identity_ch09.py`) | Rule 09.3, `why.text`, last sentence | while B’s smooth drawing keeps its shape on every screen. | while B’s smooth drawing keeps its shape on every screen above 1x. | W20, as row 1 |
| 3 | `04-ampersand.json` (identity designer) | Rule 04.5, `why.text` | a plausible link as a dashed one | a connection graded plausible as a dashed one | 4e: the atlas's links are connections on every reader page (Rule 10.10; Rule 12.1 now says so). Not changed this pass, so the reports did not list it |
| 4 | `04-ampersand.json` (identity designer) | Rule 04.5, `failure.caption` | In the atlas’s key a dashed line means a plausible link, | In the atlas’s key a dashed line marks a connection graded plausible, | As row 3 |
| 5 | `manifest-identity.json` (identity designer) | `s-04-5-failure.alt` | a dashed line means a plausible link, | a dashed line marks a connection graded plausible, | As row 3 |
| 6 | `10-symbols.json` (systems designer, `stage_b_ch10_build.py`) | Rule 10.6, `rule[1]`, second sentence | An atlas drawing appears only beside the atlas’s own name, never beside a piece’s own topic word. | An atlas drawing appears only beside the atlas’s own name for it. | W09 and W11: "never" restates "only" as a matched negative |
| 7 | `10-symbols.json` (systems designer) | Rule 10.4, spec "Floor" | 48 px for any of the 124 | 48 px for any of the 124, except inside a one-color tile (Rule 10.5) | Rule 10.5 now sets 94 drawings at 32 to 34 px in one-color tiles and calls it the one exception to Rule 10.4's floor, while Rule 10.4 still gives the floor with no exception |
| 8 | `10-symbols.json` (systems designer) | Rule 10.9, `why.text[1]` | and four of their 10 pairs reach the flag, | and four of their 10 pairs score 0.91 or more, | H02: "the flag" is never defined; the paragraph before gives 0.91 |
| 9 | `s-10-9-correct` and `manifest-systems.json`, its alt (systems designer) | The new group's head | At 24 px only: never two in one view | At 24 px, never two in one view | Clarity: "At 24 px only" reads as if the five may be set only at 24 px |
| 10 | `11-icons.json` (chapter 11 hand) | Rule 11.14, `correct.caption` | A stepper for loop R1 from our systems atlas, live at 360 px. | A stepper for Loop R1 from our systems atlas, “Wealth and political influence reinforce each other”, live at 360 px. | H11: no bare ID; chapters 01 and 12 write "Loop R4a" and "Loop R10" with a capital |
| 11 | `11-icons.json` (chapter 11 hand) | `extras[s-11-marks-drawn].caption`, second sentence | On Charcoal, read “charcoal” for &lt;surface&gt;. | Read &lt;surface&gt; as “newsprint” or “charcoal”, the ground the tracker sits on. | The caption names one of the two grounds the table's tokens take |
| 12 | `s-11-12-correct` (chapter 11 hand), the filter's count line in its script | `'The first three are listed here, and '+k+' more '` | "…and 4 more match." | spell 1 to 9 as words: "…and four more match." | H06; the reader check's copy text already spells them |
| 13 | `12-graphic-devices.json` (systems designer, `stage_b_ch12_systems_build.py`) | Rule 12.7, `correct.caption` | each in ink, beside headlines that keep their width. | each in ink, small enough that the headline beside it keeps at least 200 px on a phone. | W01 and W20: "keep their width" names no width; the spec gives 200 px |
| 14 | `12-graphic-devices.json` (identity designer, `stage_b_identity_ch12.py`) | Rule 12.4, `why.basis` | Design judgment and our measurements, October and November 2026; the 12 percent ceiling is our design judgment | Our measurements, October and November 2026, and design judgment, which sets the 12 percent ceiling | "Design judgment" twice; the second half was my 4e wording, and the identity designer flagged it |

Every Old string above was found once in its file by script. In rows 1, 7 and 10 the files set a non-breaking space between the number and "px" (16 px, 48 px, 360 px), so match it that way.

### Not read

- The engineer's build pass that keeps IDs whole (D2-975). Its notes did not mark it done when I finished, and they do not name it yet. Any strings it changes, and any shell strings changed after my read, are unread.
- The reader check page as rendered; I read its template's changed lines and the built page's step name.

## Routine calls

- D2-xxx | Step 4's name on the page is "A card and a drawing", its ready screen's words | D2-950 asks for a neutral title; one name for one step
- D2-xxx | Step 7's question asks in the past tense, "What did you see in it?" | The question screen hides the picture (PP-S13)
- D2-xxx | Rule 01.21 allows "a topic or atlas symbol from the 37 that read at 24 px (Rule 10.4)" in the rule, spec and builders line, and names Housing as a subject that takes its word alone | BE-S7, PP-S3, DR-196; the plate's CL-057 is an atlas symbol
- D2-xxx | Chapter 01 defines "atlas symbol" at its first use, in Rule 01.21 | H02; chapter 10 defines it in full
- D2-xxx | Rule 01.21's spec row "Topic icon" becomes "Kicker symbol" | The row now covers both kinds, and "topic icon" was the old term
- D2-xxx | Virginia's sentence takes PP-S12's words, with a comma after the year | W02; the guide sets a comma after a full date mid-sentence elsewhere
- D2-xxx | Missouri's county page takes its own source line, "Source for Missouri’s figures", retrieved November 10, 2026 | CA-S15 asks for one source per line; H04's order; the research lead read the page that day
- D2-xxx | The "How we counted" note holds the method, Ohio, Missouri and Utah, with Missouri's figures and status, and every fact the round 2 line held | CD-S14, DR-187
- D2-xxx | The plate's three source lines sit in a list with no bullets, 12 px apart, and the note sits under a label 20 px below | CA-S15: each source readable as one; a screen reader hears a list of three
- D2-xxx | The atlas's Cloture line and electric bill line end "snapshot of October 15, 2026." | BE-S8; every other atlas line in chapter 01 names the snapshot
- D2-xxx | `s-01-pillars`'s caption says "as Track’s icon does here" in place of "as the section opener’s row draws it" | CD-S15: "section opener" means the 128 px panel in Rule 09.4
- D2-xxx | The Illustrative label ends the kicker line of each invented headline in `s-01-21-correct`; the failure plate keeps its labels after the headlines | CA-S9; a label on a faulty kicker would read as one more part
- D2-xxx | Rule 01.21 keeps its sentence for a subject with no drawing | It agrees with Rule 10.6's final paragraph in verb and example, and names the 37 a kicker may hold
- D2-xxx | The read after the pass lists the three "plausible link" strings in chapter 04, unchanged this pass | 4e's call puts "connection" on every reader page
- D2-xxx | The questions file's row_48 description says "the 48 px row on a page that serves Track" | Rule 09.1 and `s-01-pillars`; a section opener is the 128 px panel
- D2-xxx | I left `track_css()` and `track_steps()` to the chapter 11 hand and kept the generator's current `s-01-pieces` output in the tree | The brief gives the marks in `s-01-pieces` to that owner, and the main session's rerun of every generator settles the final file

## Questions for Dustin

None from this pass.

## Requests to other owners

The four requests at the top of this file: the chapter 11 hand (`s-01-pieces`'s A-5 failure, and where its marks live in my generator); the systems designer (CA-S7's words for Rule 10.2; PP-S3's sentence, to match Rule 01.21); the identity designer (Rule 09.4's kicker clause and CL-057's family attribute); and the engineer, under item 1 (the step name and question in the template).

## Tested

- `python3 -I work/build/scripts/phase-2/guide_editor_build.py`: it runs its own checks (locked lines, em dashes, studio words, fillers, the BE-02 count check, the kicker icon check) and wrote 112 specimens with no failure. Then `stage_b_identity_ch01.py`, which swapped CL-055 for CL-057 and drew the pillar icons as before.
- Every output compared with the copy saved before my first run: 01-purpose.json, manifest-editor.json and seven specimens changed (`s-01-11-correct`, `s-01-11-failure`, `s-01-13-correct`, `s-01-17-correct`, `s-01-21-correct`, `s-01-pieces`, `s-01-pillars`); chapter 02 and its 56 specimens are byte for byte the same. In `s-01-11-failure` the only change is the five new CSS rules. In `s-01-pieces`, my change is the electric bill line; every other change is chapter 11's mark code, read live from `apply_systems_ch11.py`.
- Rule 01.11's facts: 34 named facts and every date and number in the round 2 plate found again in the new plate's text by script, none missing; the BE-02 check passes.
- `guide_build.py --strict --out` to my scratch folder: exit 0, 12 chapter files, 0 placeholders, 132 rules.
- `guide_check.js` on that build: 4 failures, all A-5 on `s-01-pieces` at the four widths, from chapter 11's in-progress marks drawn twice (the second request at the top). The same build with the committed `s-01-pieces` swapped in for one build only, then put back, passes with 0 failures (4 widths, 132 rules, 305 specimens), so every change of mine passes the check. Both checks ran after my last wording change.
- Plates looked at in the built guide at 1440 and 390 px, at 1x and 2x: `s-01-11-correct`, `s-01-21-correct`, `s-01-pillars`, `s-01-13-correct`, `s-01-17-correct`. No sideways scroll at either width. At 390 px three Illustrative labels in `s-01-21-correct` wrap under their kicker line, as item CA-S9 says.
- Script scans of the questions file, this file and my generator's changed lines: no em dash; none of the listed fillers or corporate verbs.
- A read of every new string against chapter 02's rules.

- Item 8: every changed string and alt against ddd3a898, pulled by script and read in full (312 after the 35 mechanical ones); scans of them for dashes, fillers, corporate verbs, hedges, studio words and corrective turns; 4e's terms counted across every chapter and manifest; Atlas V7 read by script for L26, T01 and R-32; the research lead's section 4 and BE-S1 to S4 compared with chapter 11's source lines and rules; the tile arithmetic in Rule 10.5; the reader check template's two changed lines and the built page's step name.

## Not tested

- The reader check page as a reader uses it; I read its template and built page, and the engineer's own test covers the rest.
- The engineer's ID pass (D2-975), not done when I read.
- The changed plates of other owners at 1440 and 390 px; item 8 read their words, not their layout.
- `s-01-pieces` as it will finally stand: it depends on chapter 11's marks, which are still changing.
- How the new sentences sound read aloud to real readers, and whether a newcomer finds "How we counted" without help.
- Missouri's certified result, which is not out; the plate still gives the unofficial figures.
- My prose here for rhetorical triplets and parallel runs, which no script can rule out; I read for them.

## Change log

Modified:
- `work/build/scripts/phase-2/guide_editor_ch01.py`: Rule 01.11's strings (`R4A_SCOPE`, `SRC_R4A_COUNT`, new `SRC_R4A_MO`, `R4A_HOW_HEAD` and `R4A_HOW`, the plate's markup and CSS, alt, notes, caption and the chapter's source list); Rule 01.21's rule, why, spec, builders, captions and alts, and the kickers' Illustrative place; `s-01-pillars`'s label, alt and caption; `SRC_CLOTURE` and `SRC_ELECTRIC`.
- `work/handoffs/phase-2/20261110_Reader-Check-2-Questions.md`: step 4's name, step 7's footer question, and a note of both; in item 8, row_48's head and description.
- By the generator and the identity step (outputs, not edited by hand): `work/build/guide/chapters/01-purpose.json`, `work/build/guide/specimens/manifest-editor.json`, and `s-01-11-correct.html`, `s-01-11-failure.html`, `s-01-13-correct.html`, `s-01-17-correct.html`, `s-01-21-correct.html`, `s-01-pieces.html`, `s-01-pillars.html` in `work/build/guide/specimens/`.

Created:
- `work/handoffs/phase-2/20261110_Stage-B-Round-3-Editor-Fix-Notes.md` (this file).

Scratch only, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/round-3/fix/editor/`: copies of my files before the pass (`before/`), the built guide and its check results, the isolation build, the screenshot script and the plate captures (`shots/`), and item 8's string extracts (`read/`).
