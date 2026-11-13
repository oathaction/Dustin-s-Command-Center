# Round 4, infographics maker notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the infographics maker under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/infographics/`.

## Status

- 21:23 UTC. S89 to S94 built in the repository, each PASS with the sweep (0 faults). Applied the editor's words (first look, 21:03 and 21:17) and the data lead's MI-1, MI-2, MI-4, MI-5, MI-6 and the 7508A ruling. Open: MI-3 (S90's current spending, waiting on the research lead's reading of the Bureau's documentation); IM-E4 (S91's three cards side by side); IM-E5 (the dot-plot card mode, for S95); the editor's ED4-4 (S89's source line words, a sidecar variant); the design director's read. S95's spec and the rewritten `social-data-card` are drafted; the spec waits in scratch until the dot plot's card mode lands, so no `build --all` meets it half-made.
- 21:16 UTC. The engineer landed R4-3 and R4-4; the four card forms and their specs moved from scratch into the kit.
- 20:56 UTC. Read the data lead's rulings (a) to (c) and applied them to S89.
- 20:40 UTC. Started.

## Summary

| Spec | Form | State | Bytes with frame (kit build, 21:22 UTC) |
|---|---|---|---|
| S89 | `process-explainer` (drawing) | Signed off by the data lead (21:14); editor's words applied | 10,222 |
| S90 | `by-the-numbers` (HTML text) | Signed off with MI-3 open (words) | 6,372 |
| S91 | `comparison-cards` (HTML text) | Signed off but for MI-4, now applied; cards two and one at 720 px until IM-E4 | 7,109 |
| S92 | `step-by-step` (HTML text) | Signed off | 9,307 |
| S93 | `annotated-illustration` (drawing) | Signed off whole (MI-2 fixed) | 7,317 |
| S94 | `calendar` (HTML text and one year mark) | MI-5 and MI-6 applied, for the data lead's read | 11,960 |
| S95 | `social-data-card` (two crops) | Module rewritten to R4-4; spec in scratch, waiting on IM-E5 | not built |

Entries 14.135 to 14.141 are written; the chapter generator, run with `--rounds 1,2,3,4`, takes in 14.135 to 14.140 and holds 14.141 among the planned numbers until S95's spec lands (its one fault, "no spec s95.json", says so). Every figure in a title, note, card or alt is checked by `python3 -I work/build/scripts/phase-3/maker_i_round4_derive.py --figures` (all pass; S95 checked from its scratch spec with `--specs`).

## Routine calls

- D3-xxx | S89 draws actors as lanes named in words, one each for local governments, states and tribes, the federal government and residents, and each step's box spans the lanes of those who act at it | Ruling (b): actors by position, not ink; call 7: no approved Civic Line drawing means a level of government, a governor, FEMA or the President, so no icon stands for any of them
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

## Tested

## Not tested
