# Brief: Phase 3, round 0, fix pass, part 1 (chapter 13, the palettes, the data plan)

Oath & Action Edition 06, Phase 3, November 11, 2026. Written by the main session from the three part 1 reviews. Part 2 (the kit and S01 to S16) follows when the engineer finishes; its fixes go in their own brief. This is the round's one fix pass for these items; DR-191's short second pass follows the editor's read of what changed.

## The reviews

| Review | Score | Must fix | Should fix | File in `work/handoffs/phase-3/` |
|---|---|---|---|---|
| Statistics and civic education | 3 of 5 | 6 | 19 | `20261111_Round-0-Red-Team-Statistics-Civic.md` |
| Nonpartisanship, brand and craft | 3 of 5 | 3 | 14 (9 chapter 13, 5 palettes) | `20261111_Round-0-Red-Team-Brand-Craft.md` |
| Creative director | Chapter 13: 4 4 4 3 3 4. Palettes: 4 4 5 4 3 4 | Chapter 13: 4; palettes: 2 (one shared) | Chapter 13: 7; palettes: 3 | `20261111_CD-Review-Of-Round-0.md`, `20261111_Round-0-CD-Scores.json` |

Each owner takes every Must fix and Should fix the three reports give its role, reads it in the report itself, and fixes it at its source (the generator or data file, never only the output). Where reports overlap, fix once and note which codes it closes. Where you disagree with an item, say why in your notes; do not skip it silently.

## The main session's calls on the shared items

| Call | Item | Decision | Owners |
|---|---|---|---|
| D3-83 | Public statistics have no grade rule (statistics M1, CD M1, brand fault 2) | Adopt the statistics reviewer's fix in Rule 13.1, with a spec row: a figure from outside the atlas takes its grade word from H08's table, so an official statistic or a public record prints "Documented" with its source after the colon ("Documented: a Census Bureau survey"). A count or a survey tabulation is a finding and carries the publisher's margin of error where one exists; a figure that rests on a model's assumptions (a projection, a small-area model, a with-and-without calculation) is an estimate and prints its range or method. "Official statistic" leaves every plate and every spec | Editor (Rules 13.1 to 13.3 and plates); data lead signs it off; the Explainer maker applies it to S01 to S16 in part 2 |
| D3-84 | The line code stated two ways (CD M2, brand fault 3) | One source: the atlas build's own constants, `wire_marks` in `work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py`, which Rule 10.10's builders line names. The data lead reads them by script and sets every value (dash patterns, shortest line, the hollow line's rails, the record square) in the palette proposal; the engineer's tokens take those values; Rule 13.4 states the same numbers and cites the tokens. Where the atlas build does not define a value, the data lead sets it once and logs why. The hypothesis gloss is the one word Rule 13.3's table prints | Data lead first, then the engineer (tokens) and the editor (Rule 13.4) |
| D3-85 | Rule 13.11's plate reads as partisan from the right (brand M1) | Keep all seven repair log rows. Put the atlas's coding note at the top of the plate, and attribute each heading to the atlas ("The atlas codes these rows as away from voters") | Editor |
| D3-86 | Do DR-124's terms govern a chapter's teaching examples as they govern chart sets (brand Q1)? | Yes, under DR-93 and DR-124 as they stand, so this is not a new question for Dustin: no example is added, softened or swapped to even the score. Fix the one plate whose words invite a partisan reading (D3-85). When a plate is redrawn for another reason, its example comes from the evidence that teaches the rule best, read from both sides | Editor |
| D3-87 | Chapter 02's approved "shrank in seven of the 57 months charted" (statistics question 1) | Goes to Dustin with the reviewer's recommendation. Until he answers, chapter 02 and S14 keep the approved words, and chapter 13's own plates take a level title that makes no count of drops | Editor (chapter 13 only) |
| D3-88 | Rent share in data plan rows 63 and 64 divides rent by all households' income (statistics M) | Re-pick to the Census Bureau's own measure of gross rent as a percentage of renter household income from the American Community Survey, with its margins, and re-run the Rule 01.9 count if a domain or state changes | Research lead; data lead signs off |
| D3-89 | The 2023 survey set beside the H.R. 7008 votes (data plan row 40) | Fix as the statistics report says; the sidecar's qualification already states the survey predates both votes by three years, and the chart must say so where a reader sees it | Research lead with the data lead |

## Who works

| Owner | Agent | Fixes | Notes file section |
|---|---|---|---|
| Editor | resumed from round 0 | Chapter 13: every item in the three reports for the editor; D3-83 to D3-87 | `20261111_Round-0-Editor-Notes.md`, new section "Fix pass" |
| Data visualization lead | resumed from round 0 | The palettes: every item for the data lead (CD M5's key that serves two charts among them); D3-84's values first, sent to the engineer and the editor; the sign-off of D3-83 and D3-88 | `20261111_Round-0-Palette-Notes.md`, "Fix pass" |
| Research lead | resumed from round 0 | The data plan and datasets: every item for the research lead; D3-88, D3-89; the editor's request for the Brandeis opinion in the research ledger | `20261111_Round-0-Research-Notes.md`, "Fix pass" |
| Engineer | still finishing the kit | D3-84's token values when the data lead sends them, in the same pre-release | `20261111_Round-0-Engineer-Notes.md` |

Order: the data lead sends D3-84's values first. The editor and the research lead start at once on everything else.

## Limits

The round 0 brief's limits hold: write only your own files; never touch `source/`, `deliverables/` or Atlas V7; do not commit or push; never run `git checkout --`; scratch by absolute path under `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0-fix/<your-role>/`. Rebuild with `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch path>` (0 warnings) and look at every changed plate at 1440 and 390 px. Write new routine calls as "D3-xxx | decision | reason" lines in your "Fix pass" section, with Tested and Not tested. Reply to the main session in under 150 words: what you fixed by code, what you did not and why, and anything blocking.
