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

- **IM-E1, a law's number held on one line.** Titles and measure lines are HTML text, and a browser breaks "Public Law 119-12" after the hyphen (S93's title at 390 px breaks "119-" from "12"). A typography key that holds listed phrases together (a nowrap span in the HTML words, measured as one word in the drawing) would keep a law's or bill's number whole. No U+2011, which the checks bar.

## Tested

## Not tested
