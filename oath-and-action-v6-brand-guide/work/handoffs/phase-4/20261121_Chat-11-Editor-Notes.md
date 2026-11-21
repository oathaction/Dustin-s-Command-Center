# Chat 11, editor's notes

Editor (oa-editor), chat 11 of Phase 4, November 21, 2026. Brief: `work/handoffs/phase-4/20261121_Chat-11-Brief.md`, sections 1 to 4 and 9a. Job 1 is Dustin's answers DR-305 and DR-310 in chapter 05, word for word as the decision log prints them ("### Dustin's answers on chat 11's questions"), with ED10-2's row as the register prints it. Job 2, chapter 20's words, waits for the design director's hand-over.

Started 18:58 UTC. Read: my role file, the brief in full, DR-305 to DR-311 and D4-104 to D4-105 in the decision log (found by searching for "DR-305"), the register rows ED10-1 to ED10-3, my chat 10 notes, Master Brief sections 3, 8, 15 and 23, and Rules 05.1, 05.3, 05.5, 12.5 and 15.11 as built.

## Routine calls

- D4-xxx | DR-310's sentence opens the second paragraph of Rule 05.1, before "The other shares in the palette sheet below" | There "the limits" follows straight on from the first paragraph's "three limits", so a reader takes them as the same three. At the paragraph's end it would follow "A single view may fall outside them", where "the limits" could be read as the body-of-work shares
- D4-xxx | The "Atlas red target" row sits after the "Error bar" row in Rule 05.5's specifications, and its value opens with a capital ("Red connections …"), as every value cell in the chapter does; every other word is the register's | The rule's text names the two exceptions in that order; the register prints the row as "label: value", where the value follows a colon
- D4-xxx | The new row carries no token | Its words name a red mark and a Charcoal edge and send the reader to Rule 12.5, whose rows carry those tokens; a token here would print a name the approved row does not hold, and five of the six rows Rule 05.3 takes from its approved wording carry none
- D4-xxx | Rule 05.3's keyline row reads "Charcoal, 1 px, 13.29 to 1, except the marks Rule 05.5 names", the phrase joined with a comma | The value is a list of short parts joined by commas; the ratio stays computed from the tokens (`{ch_n}`)
- D4-xxx | The generator's two `# G3-06 (c)` comments become `# DR-305 (ED10-1)`, and the new words carry `# DR-305 (ED10-2)`, `# DR-305 (ED10-3)` and `# DR-310` comments | The next maker can trace each phrase to Dustin's answer
- D4-xxx | The measurement record keeps its new render line (Chromium 157.0.8103.78, 18:59:23 UTC) | `stage_a_systems_build.py final` writes it; the 55 rendered figures equal the committed record's, so the render date is all that moved, as in chat 10's rebuild

## Done

Dustin's answers DR-305 and DR-310, built 18:59 UTC, word for word, with the typographer's apostrophes (U+2019) in "atlas’s", "variable’s" and "section’s". All through `work/build/scripts/phase-2/stage_a_systems_ch05.py`, rebuilt through `stage_a_systems_build.py` probe, capture, final, each under the lock.

- **Rule 05.5's sentence (DR-305, ED10-1).** G3-06 (c)'s sentence ("The atlas’s red target takes none either: …") is replaced by "On the atlas’s red target, only the red connections carry a 1 px Charcoal edge on each side (Rule 12.5). Every plate names each target in words beside the drawing (Rule 15.11), so the red outline of a target variable and each red arrowhead go without an edge." It sits where the old sentence sat, after the error bar's and before "Stone passes for marks on light surfaces".
- **Rule 05.3's reason (DR-305).** Its second paragraph now ends "On Newsprint it measures 2.96 to 1, so a working red mark there takes a keyline, a 1 px Charcoal edge drawn inside the mark. Rule 05.5 lets the error bar, and the red outlines and arrowheads of the atlas’s target, go without one." The 2.96 stays computed from the tokens (`{red_n}`).
- **Rule 05.5's new specification row (DR-305, ED10-2).** "Atlas red target": "Red connections on a 1 px Charcoal edge each side (Rule 12.5); a target variable’s red outline and its arrowheads with no keyline; the words beside the drawing name each target (Rule 15.11)", after "Error bar".
- **Rule 05.3's keyline row (DR-305, ED10-3).** "Keyline on a red mark on Newsprint": "Charcoal, 1 px, 13.29 to 1, except the marks Rule 05.5 names".
- **Rule 05.1's new sentence (DR-310).** For the main session: it opens the rule's second paragraph, so the paragraph reads "On a long page the limits hold for the first screen and for each section’s opening screen; screens of running text between them may hold more Newsprint. The other shares in the palette sheet below, carried from our fifth edition, set the balance across a body of work, such as a month of stories or a whole report. A single view may fall outside them." The reason is under "Routine calls".

`git diff --stat` at 19:01 UTC shows three files and no others: the generator (26 lines), `work/build/guide/chapters/05-color.json` (the five values above) and `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json` (its render date alone). Chapters 06 and 07, all 56 stage A specimens and `manifest-systems.json` came out byte for byte as committed.

Bytes on the strict build: chapter 05, 240,871 to 241,529 (+658); the page, 12,239,498 to 12,240,156 (+658). No plate changed. Chapter 05 has no Phase 4 allocation.

My scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ac32a0f7-d562-5d93-9aba-0ef59f7ca891/scratchpad/c11/editor/` (`before/` holds the committed outputs and hashes; `stageA-base/` and `stageA/` the probes and capture; `guide.html`, `guide-Build-Report.json` and `strict.log` the strict build; `page-diff.txt` the tag-by-tag diff).

## Requests

None.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| ED11-1 | Editor, chat 11, reading DR-310 as built | Rule 05.1's specification "Newsprint in each view"; `stage_a_systems_ch05.py`, output `05-color.json` | The rule's text now lets screens of running text on a long page hold more Newsprint, while the row still gives "60 to 85 percent" for every view with no exception. A builder who reads only the specifications, as chapter 20's per-screen measure will, applies the 85 percent ceiling to every screen. The same pattern as ED10-2 and ED10-3 | Value: "60 to 85 percent; on a long page, screens of running text between the opening screens may hold more" | DR-310 names one sentence; approved chapters change only where an approved answer names the change | Open, for Dustin |

## Tested

- `stage_a_systems_build.py probe` under the lock, before the edits (18:58 UTC) and after (18:59): the probe pages are byte for byte the same (`measure.html`, both phone pages, `probes.json`), so one capture served the rebuild.
- `stage_a_systems_capture.js` under the lock at 18:59 UTC (load 0.29, no other browser running): 55 results, each equal to the committed record's rendered figure; only the render date differs.
- `stage_a_systems_build.py final` under the lock: exit 0; chapters 05 (7 rules), 06 (10) and 07 (6), 56 specimens, 173 figures. Its `check_chapter` runs the house-rule copy check on every word of the three chapter files, and the CD-S10 check that Rule 05.3's approved wording appears once sentence by sentence; both passed.
- SHA-256 of every file under `work/build/guide/chapters/` and `work/build/guide/specimens/` and of the measurement record, before and after: only `05-color.json` and the measurement record changed.
- By script, against the decision log's DR-305 and DR-310 rows and the register's ED10-2 row: each quoted sentence appears in `05-color.json` once and character for character; the row's label matches, and its value matches but for the capital R.
- The strict build to my scratch under the lock (19:00 UTC): exit 0, 0 warnings, 12,240,156 bytes, 20 chapter files, 382 rules, 707 specimens.
- Against the main session's 17:37 strict build of the committed tree (`scratchpad/c11/main/guide.html`), tag by tag: eight hunks, the five word changes (Rule 05.3's reason and Rule 05.5's text each split in two around a link) and the build's time line, nothing else.
- Word search of the strict build's text (tags, scripts and styles stripped): each new phrase prints once (Rule 05.5's two sentences, Rule 05.3's reason, "Atlas red target" and its value, "except the marks Rule 05.5 names", Rule 05.1's sentence); the old ones print 0 times ("The atlas’s red target takes none either", "red ring and arrowhead", "names its target in words beside the drawing", "apart from the two marks Rule 05.5 names"). Raw HTML counts agree, so no script or index carries a second copy.
- Links: "Rule 12.5" in Rule 05.5's text prints as a link (links to `#rule-12-5` go from 7 to 8); "Rule 15.11" and Rule 05.3's "Rule 05.5" stay links. The new row's "(Rule 12.5)" and "(Rule 15.11)" print as plain text, as every rule named in a specification value does (166 such values in the guide, none linked).
- Script check of the five changed strings: no em or en dash, no straight quote, none of the listed fillers, hedges or corporate verbs, no "not … but" turn.
- Against the chapters: Rule 12.5's text and its "Edge on Newsprint" row ("1 px Charcoal on each side of a red connection") and Rule 15.11's "Targets" row agree with the new words. The page states the 60 to 85 percent view limit only in Rule 05.1 and its row; the palette plates give the body-of-work shares, which DR-310 does not touch.

## Not tested

- The changed rules in a browser at any width. I read their words in the built page by script and did not look at how the new row or the longer paragraphs wrap.
- The four-width guide check and the quick guide check, which the main session runs at the close.
- Read aloud by a person.
