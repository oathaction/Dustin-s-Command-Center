# Round 4, infographics maker notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the infographics maker under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/infographics/`.

## Status

- 21:34 UTC. All seven specs are in the kit. S89 to S94 PASS with the sweep. S95 builds both crops on the dot plot's card mode and fails only on kit items: "no place clear of the dots for Massachusetts 96" (IM-E6, the engineer is building the band) and parity, since the page's card spec drops the grade line the data lead asked for (IM-E8). Applied: the design director's DD-I1 to DD-I3, DD-I5 to DD-I9, DD-I15, DD-I16 and DD-I20; the data lead's MI-1 to MI-7; the editor's first-look words and its S89 eyebrow ruling. Waiting on the engineer for DD-I10 to DD-I14, DD-I17 to DD-I19 (IM-E7 and the director's own kit requests) and the orphan guard (DD-I4), and on the editor's ED4-4 (S89's source line).
- 21:23 UTC. S89 to S94 built; editor's words and MI-1, MI-2, MI-4 to MI-6 applied.
- 21:16 UTC. The engineer landed R4-3 and R4-4; the four card forms and their specs moved from scratch into the kit.
- 20:56 UTC. Read the data lead's rulings (a) to (c) and applied them to S89.
- 20:40 UTC. Started.

## Summary

| Spec | Form | State | Bytes with frame (kit build) |
|---|---|---|---|
| S89 | `process-explainer` (drawing) | Signed off (21:14); DD-I1 to DD-I3 and DD-I5 applied since, for the director's second read | 10,554 |
| S90 | `by-the-numbers` (HTML text) | Signed off; MI-3 applied (current spending's exclusions, fall 2023) | 6,410 |
| S91 | `comparison-cards` (HTML text) | MI-4 and MI-7 applied (the three territories named); the shared-row grid applied (DD-I12, `labels.rows`) | 7,112 |
| S92 | `step-by-step` (HTML text) | Signed off; DD-I15's bold limit applied | 9,358 |
| S93 | `annotated-illustration` (drawing) | Signed off whole; DD-I6 to DD-I9 applied, page order with the data lead's yes | 7,383 |
| S94 | `calendar` (HTML text and one year mark) | MI-5, MI-6, DD-I16 and DD-I20 applied; DD-I17 to DD-I19 wait on the engineer | 12,200 |
| S95 | `social-data-card` (two crops, 1080 by 1350 and 1080 by 1080) | PASS with the sweep after IM-E6 and IM-E8 landed; S19's grade line beside "Finding"; for the data lead's and the accessibility lead's read | 12,326 |

Under DR-271 the share and the 15,000-byte line are figures the build reports; every plate above is under both. Entries 14.135 to 14.141 are written; the chapter generator, run with `--rounds 1,2,3,4`, takes all seven in (141 rules, 0 faults). Every figure in a title, note, card or alt is checked by `python3 -I work/build/scripts/phase-3/maker_i_round4_derive.py --figures` (all pass, S89 to S95).

### The design director's requests: what I did

| Request | Done | How |
|---|---|---|
| DD-I1, Must | Yes | The emergency request's link drops down the middle of the lane to its left (the Local lane), clear of every lane rule, then into the box's side |
| DD-I2, Must | Yes | Every head on one line on one baseline (the form draws lanes only where each head fits on one line and the lane holds its least width); heads now "Local", "State and tribal", "Federal", "Residents"; lanes sized by a stated rule in `notes_internal`: a lane's share follows the steps it holds alone (0.6, 1.2, 1.2, 1.0) |
| DD-I3, Should | Yes | Set-in boxes at 44 px on a phone, so each link shows a 16 px stem before its head |
| DD-I4, Should | Yes, in S89's own boxes | The form narrows a box's measure a step at a time, by up to a third, until no word stands alone on a block's last line ("help" now ends "individual help"; "The President decides" holds two words a line); "the law’s limit" and "30 days" held. The same on S95's title |
| DD-I5, Should | Yes | "30 days" held (`typography.hold`) |
| DD-I6, Must | Yes | A dashed context-ink rule across the sheet's foot and "The page continues with section 2." under it, inside the drawing; the old note is gone |
| DD-I7, Must | Yes, with the data lead's yes (21:25) | Parts numbered in the page's reading order through the spec's sort; the table's Number column maps the same; the file is as stored |
| DD-I8, Should | Yes | A running head that wraps sets "139 STAT. 55" on a line of its own, right-aligned |
| DD-I9, Should | Yes, with the editor's ruling (21:24) | The page's doubled single marks set as double quotation marks (`typography.replace`, printed words only); the note says so beside the dash |
| DD-I10, DD-I11 | Waiting | The engineer's facts variant (the director's own kit request) |
| DD-I12, Must | Yes | The engineer's shared-row grid (`.oac-h-rows`), set by S91's `labels.rows`; stacked on a phone, each card flows as before |
| DD-I13, DD-I14 | Waiting | IM-E7 items 1 and 2 (an eyebrow class; the step's measure is the kit's 38em) |
| DD-I15, Should | In part | The limit's own words in bold; the 8 px above waits on IM-E7 item 2 |
| DD-I16, Must | Yes | Each kind of date on a line of its own, its consequence on the next |
| DD-I17 to DD-I19 | Waiting | IM-E7 items 3 to 5 |
| DD-I20, Should | Yes | "fiscal 2028" held |

### The editor's words: what I applied

- First look (21:03) and 21:17 rows: all applied, S89's title, chart note, note 2 and alt; S93's title and grade line; S90's gloss of current spending and note 2; S91's territorial line ("10-year") and note; S92's title and note with I013's own title; S94's note 2 with "written"; entry 14.135's rule.
- 21:22 and 21:24 rulings: S94's title (no colon); S89's eyebrow "In place of step 3"; S93 keeps "119-12" in our words, sets the page's paired single marks as double marks, its crop line in the label style and its one note in the editor's words.
- 21:28 rows: S90's shares split as the editor worded them (45 cents the states; 43 cents local with the federal 12 cents), New York and Idaho sharing one fact, so six facts stay.
- 21:35 entry rows: 14.137, 14.138, 14.140 and 14.141 applied as written.
- **For the editor:** S91's title is not your 21:22 row. The data lead's MI-7 (21:24, after your row) asks the title to name the three territories, since Puerto Rico's district judges serve for life; it now reads "District judges serve for life except in Guam, the Northern Mariana Islands and the Virgin Islands; judges pick bankruptcy judges for 14 years and full-time magistrate judges for eight." (29 words). Its words and length are yours to set within MI-7.
- Waiting: ED4-4 (S89's source line ending) and ED4-5 (S91's source line, "four in the territorial courts"), both sidecar variants for the research lead.

## Routine calls

- D3-xxx | S89 draws actors as lanes named in words, one each for local, state and tribal, federal and residents, and each step's box spans the lanes of those who act at it | Ruling (b): actors by position, not ink; call 7: no approved Civic Line drawing means a level of government, a governor, FEMA or the President, so no icon stands for any of them
- D3-xxx | S89's two last steps (public assistance and individual help) share one row after step 6, governments at the left, with the spec's sort putting order 9 before 8 so the numbers read left to right | Both follow FEMA's designation; one row with two arrows from step 6 shows they run side by side, which two rows in sequence would hide
- D3-xxx | S93's page is redrawn in Inter at the kit's sizes, with line breaks the drawing's measure sets, not the page's | The kit sets no type under 13 px and carries only Inter and Inter Tight; the words are the page's own, and the note says the drawing is a redraw
- D3-xxx | S93's running head draws the page's dash as a rule one em wide, so no em dash prints | Chapter 02 bars the em dash in reader text; DR-79 drew one the same way in W21's before
- D3-xxx | S93 numbers its parts on the page and in the callout list, with no leader lines | Ruling (b) puts the callouts' words in HTML text beside or under the page, where a leader from the drawing cannot reach them; the numbers carry the link at every width

- D3-xxx | S93 stays a drawing, its callouts drawn beside the page in the SVG, with the table giving every part, its words as printed and what it tells, in the order the parts sit on the page | The engineer's R4-3 keeps the annotated illustration a drawing through `draw`; the accessibility lead's reading order for a drawing is its text equivalent, which the table now follows (row 11 before row 10)
- D3-xxx | S93 numbers its parts by their place on the page, so row 11 (the margin short title, added by the research lead) prints as 10 and row 10 (the U.S. Code note) as 11, the table's Number column mapping both | The research lead kept row numbers fixed; a reader meets the margin's short title above the code note, and the callout list follows the page
- D3-xxx | S90 sets six facts: New York's and Idaho's spending per pupil take a fact each | Five facts left a hole in the grid's second row; six fill two rows of three at a desk and three of two at 656 px, and each figure is one row's value
- D3-xxx | S90 leaves row 5, the COVID-19 relief sum, out of its cards and table by `where`, and prints it in the note | The brief and the data lead's condition put the $39.2 billion in the note; the source line also carries it
- D3-xxx | S94's year mark draws at 224 px, the art box at a 256 px window, with every month a row, a hairline for its days and each event a 6 px square on its day | `h.mark` draws at a fixed size and never scales its words, so the mark is drawn at the narrowest width the page can give it
- D3-xxx | S94's list holds one item a day, with every event on it; its table gives the date, what falls due and the law | Grouping by day spares the date line three times; the table stays lean since the list already carries who and each consequence as live text, which kept the plate near 12,000 bytes with its frame
- D3-xxx | S92 and S94 end each step's "what happens" line with a period the spec adds (S92's `labels.stop`), and S94's events stay phrases, as a date book sets them | The research lead's summaries are sentences stored without a stop; chapter 02 asks a full sentence of every line but labels
- D3-xxx | The four card forms register `html` and no `draw`, so the guide's page carries none of their code | R4-3, item 1; a card form adds no byte to the renderer
- D3-xxx | `social-data-card` sets the evidence word at 36 px, the title at 62 px on the tall crop and 54 px on the square, the inner form at k = 36/13 through `c.inner`, and the card's own source line, which names where every state's rate is, at 36 px under a 2 px hairline | R4-4's floor (36 px at true size) and the data lead's condition that the card say where the full list is; the inner form's own words (IM-E5's condition) say each dot is a state

## Requests

### Requests to the research lead

- **IM-1, S89's source line (ruling (c), call 1).** A variant of `govinfo-disaster-declaration-steps.meta.json`'s printed line without "as in force November 9, 2026", since the grade line prints that date once. Suggested name `in_force_in_grade`; the rest of the line as it stands.
- **IM-2, S91's source line (ruling (c)).** A variant of `uscode-federal-trial-judges.meta.json`'s line without "seats as of September 30, 2025", since S91's grade line prints the seats' date once. Suggested name `seats_date_in_grade`.
- **IM-3, S93's source line (ruling (c)).** A variant of `govinfo-pl-119-12-first-page.meta.json`'s line without "approved May 19, 2025": the data lead's (c) keeps the approval date to the page drawing and its callout. Suggested name `date_on_page`.
- **IM-4, S93's margin words.** The page's right margin beside section 1 prints the short title, "Tools to Address Known Exploitation by Immobilizing Technological Deepfakes on Websites and Networks Act.", above "47 USC 609 note." (page 1 of PLAW-119publ12.pdf, read with pdftotext -layout). Row 10's `printed_text` holds only "47 USC 609 note.". If you agree the margin note is both lines, please give row 10 both (or add row 11, "Margin short title"), so the redraw can print every word the page prints. Until then the drawing prints row 10 as it stands.

### Requests to the engineer

- **IM-E1, a law's number held on one line.** (SET by the engineer with R4-3 as `typography.hold`.) Titles and measure lines are HTML text, and a browser breaks "Public Law 119-12" after the hyphen (S93's title at 390 px breaks "119-" from "12"). A typography key that holds listed phrases together (a nowrap span in the HTML words, measured as one word in the drawing) would keep a law's or bill's number whole. No U+2011, which the checks bar.

- **IM-E2, four small additions to R4-3, for S90, S92 and S94 (21:02 UTC).**
  1. *A figure and its words in one block (S90).* The accessibility lead asks that a screen reader say "$994.9 billion came in to public school systems ..." as one sentence; the contract sets `oac-h-big` on a `p`, which makes the figure its own paragraph. Please let `oac-h-big` sit on a `span` (or `strong`) at the start of a `p.oac-h-body`, set on its own line by the class, so the figure and its words are one block.
  2. *One fact for several rows (S90).* Fact 2 prints the three revenue shares (rows 2, 3 and 4) and fact 4 New York's and Idaho's spending (rows 7 and 8). Please let `h.row` take a list, `h.row([2, 3, 4])` giving `data-oa-row="2 3 4"`, with the check counting each row once across items.
  3. *Order marks on the steps (S92), ruling (b).* The data lead sets each step's number on a 24 px disc in the subject ink with its numeral in the label-on-subject ink, the line joining the discs in the subject ink, and an optional step (S92's rows 4 and 7) on a disc edged in the context ink with a text-ink numeral, named optional in words. Please draw `oac-h-steps`' counter that way, with a modifier for the optional step's `li` (`oac-h-branch`, say); the words "Optional" print in the step as HTML text.
  4. *Months in order (S94).* The calendar lists its dates as an `ol.oac-h-dates` under one year mark drawn by `h.mark`; nothing more is needed if `h.mark`'s drawing holds its month names (a picture, `aria-hidden`, as the accessibility lead allows for a grid). I draw it 256 px wide, the narrowest column, so it never scales.

- **IM-E3, the facts grid's least column, 13.5rem (21:13 UTC).** S90's widest figure, "$994.9 billion", measures 177.3 px in the display face at the title size (the kit's metrics), so a fact box needs 211 px with its padding and border. `oac-h-facts` at `minmax(min(100%, 12rem), 1fr)` gives three columns of 208 px at a 656 px column, and the build fails "a span.oac-h-big whose words overflow it" there. At 13.5rem (216 px) the grid takes two columns at 656 and three from 680 px, where each box holds 182 px. Only S90 uses `oac-h-facts`.

- **IM-E4, three cards side by side at a desk, 13rem (21:15 UTC).** `oac-h-cards` at 15rem (240 px) sets S91's three cards two and one at the 720 px artboard (three need 752 px), so the cards stop reading side by side, which is the form's job ("two or three options side by side") and the data lead's (b) ("three cards of one width and one height"). At 13rem (208 px) three stand side by side from 656 px. Only S91 uses `oac-h-cards`.

- **IM-E5, dot-plot's card mode fits the crop (21:17 UTC; the main session relays).** Labeling only Mississippi and Massachusetts leaves 50 rows: at k = 2.77 (36 px words) the form's pitch runs about 3,100 px, where the 1080 by 1350 crop leaves about 550 px for the plot and the square about 380. Please let the card mode read `c.card.height` (inner px) and `c.card.ranks: "across"`: one column a state, left to right in rank order; the value scale vertical with its ticks at the left; the all-states line horizontal, dashed, with its words; Mississippi and Massachusetts named beside their dots in the subject ink; the open dots and their key as S19 draws them; the plot filling `c.card.height`. S19's dots, inks, key and line stay (ruling (b)); at 936 px each state takes about 18.7 px. `social-data-card` passes `c.card = {label: "named", ranks: "across", height}`.

- **IM-E6, two kit items (21:30 UTC).**
  1. *S95: a place for the lowest named dot's label.* Built on the card mode (21:36 landing), both crops fail "card: no place clear of the dots for "Massachusetts 96"". Massachusetts is the last column, 96 on the 0 to 700 scale, so its dot sits about 49 px over the zero line on the tall crop (less on the square), with higher dots to its left and the drawing's edge to its right; every spot the form tries is under a dot, past the right edge or below the drawing's foot. A band one label tall under the zero line, inside `c.card.height`, kept only when a named dot sits within a label's height of zero, with "below the dot, anchored at its right edge" tried into that band, would give it a place on both crops. The card gives the plot all the height the crop leaves (title 56 px tall crop, 46 px square, a one-line note and a two-line source).
  2. *A held phrase in a table's row-header column fails parity.* S89 with `typography.hold: ["individual help"]` (or "the help"), both in the `step` column that the table sets as its row header, fails "parity: the page's drawing ... differs from the Node drawing" at every width; the same hold on a phrase in another column ("law’s limit") passes. S89 holds only "30 days" and "law’s limit" for now.

- **IM-E7, R4-3 classes the design director's card reads need (21:32 UTC; each a Should unless marked).** The forms write the elements already; these are kit CSS or `h` items.
  1. *An eyebrow line (DD-I13, S92).* A class for a step's opening line ("Optional, when the need is urgent") and its actor line ("Agency"), in the secondary ink at 600 weight, as S66, S77 and S89 set an eyebrow; `oac-h-k` on a `p` would do. Today both print through `oac-h-small` in the text ink.
  2. *Space before the limit (DD-I15, S92).* 8 px above a step's limit line; the form now sets the limit's own words in `strong`. A class for that line (`oac-h-limit`), or 8 px on an `oac-h-small` that follows `oac-h-body`.
  3. *Squares for the kinds of date (DD-I17, S94).* A tag variant that draws a 10 px square before its words in 600 weight, filled in the subject ink for the strong kind and open with a 1.5 px subject edge for the plain one, in place of the boxed chip; the same two squares before the year mark's key words. The words stay, so the kind never rests on a mark alone.
  4. *The year mark at the plate's width (DD-I18, S94).* `h.mark` draws at one fixed width, so S94's year is 224 px at every width. Either let a card form give `h.mark` two widths (the artboard's and 224 px) with the page showing the one its box holds, or a mark that scales with no words inside it (the month names then set as HTML beside it). I draw whichever lands.
  5. *Dates as rows (DD-I19, S94).* At a desk, `oac-h-dates` items as two columns, the date's `p.oac-h-name` in a left column about 180 px wide and the rest beside it, hairlines between items, one column on a phone (S60's grammar).

- **IM-E8, the card’s grade line on the page (21:33 UTC).** S95 prints S19's grade line under "Finding" on both crops (the data lead's R4-4 condition, 21:32). `draw_spec()` in `oa-chart.mjs` carries `evidence_label`, `title` and `source_line` to the page for a `social-data-card`, but not `grade_line`, so the page and its PNGs draw no grade line and S95 fails parity at every crop. One word added to that list would carry it.

## Tested

## Not tested
