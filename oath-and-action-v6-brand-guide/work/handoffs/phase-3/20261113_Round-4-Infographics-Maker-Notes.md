# Round 4, infographics maker notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the infographics maker under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/infographics/`.

## Status

- 20:56 UTC. Read the data lead's rulings (a) to (c) and applied them to S89. Drafts exist for S89 (`process-explainer`, SVG) and S93 (`annotated-illustration`, the page in SVG); both build with 0 faults, sweep not yet run. S90, S91, S92 and S94 (call 8's cards) and S93's callout list wait on the engineer's R4-3 contract; S95 waits on R4-4. Ceiling: 13,172 bytes a plate with its frame.
- 20:40 UTC. Started.

## Summary

| Spec | Form | State | Bytes with frame (kit build) |
|---|---|---|---|
| S89 | `process-explainer` | Draft, rulings applied; waiting on R-2's source line variant and the editor | about 10,200 |
| S90 | `by-the-numbers` | Waiting on R4-3 | |
| S91 | `comparison-cards` | Waiting on R4-3 | |
| S92 | `step-by-step` | Waiting on R4-3 | |
| S93 | `annotated-illustration` | Page drawing drafted; callout list waits on R4-3 | about 7,300 |
| S94 | `calendar` | Waiting on R4-3 | |
| S95 | `social-data-card` | Waiting on R4-4 | |

## Routine calls

- D3-xxx | S89 draws actors as lanes named in words, one each for local governments, states and tribes, the federal government and residents, and each step's box spans the lanes of those who act at it | Ruling (b): actors by position, not ink; call 7: no approved Civic Line drawing means a level of government, a governor, FEMA or the President, so no icon stands for any of them
- D3-xxx | S89's two last steps (public assistance and individual help) share one row after step 6, governments at the left, with the spec's sort putting order 9 before 8 so the numbers read left to right | Both follow FEMA's designation; one row with two arrows from step 6 shows they run side by side, which two rows in sequence would hide
- D3-xxx | S93's page is redrawn in Inter at the kit's sizes, with line breaks the drawing's measure sets, not the page's | The kit sets no type under 13 px and carries only Inter and Inter Tight; the words are the page's own, and the note says the drawing is a redraw
- D3-xxx | S93's running head draws the page's dash as a rule one em wide, so no em dash prints | Chapter 02 bars the em dash in reader text; DR-79 drew one the same way in W21's before
- D3-xxx | S93 numbers its parts on the page and in the callout list, with no leader lines | Ruling (b) puts the callouts' words in HTML text beside or under the page, where a leader from the drawing cannot reach them; the numbers carry the link at every width

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

## Tested

## Not tested
