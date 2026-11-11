# Brief: Phase 3, round 0, fix pass, part 2 (the kit and S01 to S16)

Oath & Action Edition 06, Phase 3, November 11, 2026. Written by the main session from the four part 2 reviews. Part 1's brief (`20261111_Round-0-Fix-Brief-Part-1.md`) still governs chapter 13 and the palettes. This is the round's one fix pass for the kit and the 16 charts; DR-191's short second pass follows the editor's read of what changed.

## The reviews

| Review | Score | Must fix | Should fix | File in `work/handoffs/phase-3/` |
|---|---|---|---|---|
| Statistics and civic education, part 2 | 4 of 5 | 2 | 10 | `20261111_Round-0-Red-Team-Statistics-Civic.md` |
| Nonpartisanship, brand and craft, part 2 | 3 of 5 | 4 | 12 | `20261111_Round-0-Red-Team-Brand-Craft.md` |
| Accessibility and the production test | 3 of 5 | 4 | 10 | `20261111_Round-0-Red-Team-Access-Production.md` and `round-0-production-test/` |
| Creative director, part 2 | Kit with S01 to S16: 3 4 4 4 4 4 | 3 | 6 | `20261111_CD-Review-Of-Round-0.md`, `20261111_Round-0-CD-Scores.json` |

Each owner takes every Must fix and Should fix the four reports give its role, reads it in the report itself, fixes it at its source, and notes which codes each fix closes. Where you disagree, say why in your notes.

## The main session's calls on the shared items

| Call | Item | Decision | Owner |
|---|---|---|---|
| D3-93 | Charts break at widths the kit never draws (access M2) | The kit draws and checks every spec at each column width the guide and zoom produce: 656 px (200 percent text at 1440), 558 px (1024), the phone column at 390, 296 px (360) and 320 px reflow. Every spec passes the layout guard at each, and the guard also fails a leader line that crosses a label (brand and CD on S09, S16) | Engineer; the Explainer maker for spec words a fix needs |
| D3-94 | Forced colors paint over chart content (access M1) | In forced colors every data mark keeps a fill or a pattern a reader can tell from the ground and from its label, using the system colors (`Canvas`, `CanvasText`, `GrayText`, `Highlight`) and the kit's patterns; no label sits on a fill of its own ink; the kit's check emulates forced colors on every spec at every width and fails on any label whose ink matches its ground | Engineer |
| D3-95 | Printed figures off by a tenth (statistics M1) | Data files keep the publisher's own precision; the kit rounds once, from the stored value, to the spec's format; the check compares each printed figure with the raw value rounded once | Engineer, with the research lead for any data file that stored a rounded value |
| D3-96 | S16's circles at a third of their size (brand, CD KM1) | A size scale takes only the rows a chart draws; S16's national row stays in the table and the source line but sets no circle size, and S16 returns to Phase 2's sizes | Engineer |
| D3-97 | Scripts off and drawing at load (access S2, CD on the method) | With scripts off a figure shows its alt text as visible words, a line saying the drawing needs scripts, and its table. With scripts on, each chart draws as it nears the screen, and every chart is drawn before the page prints. Each title and alt text is heard once (access S1); the table disclosure's name ends in the chart's title, never a studio ID (access S3) | Engineer |
| D3-98 | S03 and S08 show three November 3 ballot measures as pending (statistics M2) | Both keep V7's snapshot values and dates, and add one dated note where a reader sees it, under Rule 13.10: "As of November 11, 2026:" then each outcome as the record stands, marked unofficial where the state has not certified, with its source from the research ledger | Explainer maker, with the research lead's sources |
| D3-99 | S01 still ties the votes to the survey (statistics, brand Q2, D3-92) | The votes take a heading that states what they are, with no word that links them to the 2023 survey as a response to it; every segment says "for" or "against"; both provisions of H.R. 7008 are named where the votes are drawn | Explainer maker |
| D3-100 | Printing cuts tall charts (access M4) | Each chart prints whole on its page or breaks only between its drawing and its table, and no chart prints over another | Engineer |
| D3-101 | Chapter 13's five chart plates have no accessible name (access M3) | The kit's guide hook names each figure by a title that is on the page; the editor's plates keep or add that title | Engineer, then the editor's generator |
| D3-102 | The production test: a designer and a non-coder could not finish without help (access S6 to S9) | The kit gains what both panel members needed and DR-235's later page will need, without building that page: a plain recipe in `work/build/chart-kit/README.md`, error messages that say what to change, and a new chart from an existing dataset without a new sidecar where the source line is unchanged. The SVG export names its fonts and says in its description that the fonts are needed (access S9); embedding fonts in every export waits for Phase 5's package | Engineer |

## Who works, in order

| Owner | Agent | When | Notes file section |
|---|---|---|---|
| Explainer maker | resumed | Now: D3-98, D3-99 and every spec item the reports give it | `20261111_Round-0-Explainer-Notes.md`, "Fix pass 2" |
| Research lead | resumed | Now, first: the dated outcomes of the three November 3 measures for D3-98 (Massachusetts Question 3, Alaska Ballot Measure 2, and the Missouri measure in repair log row RL63, which Rule 01.11's plate already reports with its sources), each with its source and certification status; then any data file that stored a rounded value (D3-95) | `20261111_Round-0-Research-Notes.md`, "Fix pass 2" |
| Engineer | the same engineer, after its weight pass | When the weight pass is reported: D3-93 to D3-97, D3-100 to D3-102 and every kit item in the four reports; then rebuild all 16 and the board captures | `20261111_Round-0-Engineer-Notes.md`, "Fix pass 2" |
| Editor | resumed after its part 1 fixes | D3-101's titles in chapter 13; then DR-191's read of every string changed in parts 1 and 2 | `20261111_Round-0-Editor-Notes.md` |
| Data visualization lead | resumed at the end | Signs off every chart after the fixes, and the palette proof sheet's scroll frames (access S10) | `20261111_Round-0-Palette-Notes.md` |

## Limits

As part 1's brief. Scratch under `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0-fix-2/<your-role>/`. Write new routine calls as "D3-xxx | decision | reason" lines in your "Fix pass 2" section, with Tested and Not tested. Reply in under 150 words: what you fixed by code, what you did not and why, and anything blocking.
