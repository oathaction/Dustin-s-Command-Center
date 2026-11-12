# Round 2 notes: systems designer, chapter 15 Systems graphics

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Written by the systems designer (a general-purpose agent briefed as the designer of chapters 11, 12 and 15's systems plates) for `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md` (DR-244, D3-659). Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

In progress (written early; kept current). Rules 15.11 and 15.12 (group 2, reforms on the drawing) and worked examples 15.15 to 15.18 (group 3) are built in `work/build/scripts/phase-3/phase3_ch15_build.py`, each with a correct and a failure plate, on round 1's stage (D3-603 to D3-613): true 296 px drawings, the 680 px composition and one 328 px column, every plate rule in the chapter's `plate_css`. The six rules left the generator's `PLANNED` list. Every atlas value is read by script from `work/extract/atlas-v7-data.json` (snapshot of October 15, 2026) and held by a `need()` check; every value the brief names matched the model, so nothing differs. Chapter 15 places at about 298 KB in a strict build, under its 0.60 MB ceiling.

### The six rules

| Rule | Correct plate | Failure plate | Example log |
|---|---|---|---|
| 15.11 Place a reform on the exact connections and variables it targets, with its band. | Reform R-03 on Loop R4a: Connection L42 and Variables C1 and D7 in Rule 12.5's red, the rest in ink; targets in chips; band "rules" in the atlas's words; its three loops | The red set by the electoral competition cluster: C4 red, D7 in ink, note "acts on electoral competition" | D02 |
| 15.12 Grade the evidence for the problem and for the remedy apart. | Reform R-32 on the chain TC2, B2, C3 across the technology and core boundary, its three targets red; the drawing's own label (both connections well supported), then two labels apart: problem well supported, remedy hypothesis, each with the atlas's words | One label, Well supported, over the whole reform | D01 |
| 15.15 Follow a variable two loops share through each loop in turn. | Loop B4 beside Loop R10, Variable C3's pill filled in ink in both; under each, the connection into C3 and out of it with the atlas's sign sentences; where the loops meet, in the atlas's words | The shared variable under two names (Electoral pressure, Risk of losing office) with no mark | D04, D02 |
| 15.16 Show a reform's four effects side by side, with each route's check date. | Reform R-01 at its targets on Loop R10 (L08, L25, C2 red); its loops; both evidence grades; effects one family to a row with pips, code and words, no total, as of October 15, 2026; routes BI and LOC checked October 15, 2026, SS and FS "Not checked" | One "overall" +L score and every route dated October 15, 2026 | D02 |
| 15.17 Draw who holds power over each level in one authority diagram. | The seven authority connections as a ladder: economy layer, four core bodies, technology layer, lines in nested lanes so none crosses, one "decides" key; each connection named beside it | One pill, "The government", for the four bodies | D05 |
| 15.18 Print a conceptual loop's missing chain beside its grade. | Loop B2, hollow lines and thin pills, its label "Well supported, the atlas's grade for the mechanism; no numbered chain, which the atlas calls the weakest point"; the atlas's words; the station tied to Variable A4; Loops B3 and R9 with their grades | The grade alone in the label | D08 |

Rule 01.9 over the chapter's 27 examples: D01 4, D02 5, D03 3, D04 2, D05 3, D06 3, D08 3, D09 1, D10 3; no domain over one in four, no state.

## Routine calls

- D3-xxx | Rule 15.11 draws Reform R-03 on Loop R4a, which holds all three of its targets (one connection, two variables) | A reform with both kinds of target on a solid connection, outside the R10 plates of 12.5, 15.6, 15.15 and 15.16; R4a's cluster split (C4 and C1 in electoral competition, D7 in governing institutions) lets the failure show red set by a cluster
- D3-xxx | Rule 15.12 draws Reform R-32 on the chain TC2 to B2 to C3, with three grade labels: the drawing's (Rule 13.1) and the problem's and remedy's apart | Problem well supported and remedy hypothesis is the widest gap among reforms whose targets draw as one solid chain; 49 of 50 reforms carry two different grades, and in 48 the remedy's is the lower (counted by script in Rule 13.3's order)
- D3-xxx | A red target is drawn only on a solid connection; the generator stops on a patterned one | A patterned red target with delay ticks needs its lead-in at the 6 px sizes, which chapter 13's helper does not draw either; every target drawn here is documented or well supported
- D3-xxx | The note under a reform's chip and title reads "It acts where the marks turn red: on one connection and two variables" | Rule 12.5's note names the reform; the chip and title stand directly above it, and repeating the chip read as a stutter
- D3-xxx | Rule 15.15 marks the shared variable by filling its pill in ink with its name in the surface color, the one fill a pill takes | Red belongs to reforms (Rule 12.5) and heavier outlines to red targets (Rule 15.1); a fill reads at once in both drawings and survives gray print
- D3-xxx | Rule 15.15 keeps Loop R10 on the square of Rule 15.6, so Variable C3 sits at the lower right in both loops | One orientation for one loop across the chapter
- D3-xxx | Rule 15.16 prints no route note and no status text, only each route's who, feasibility and date | R-01's notes and status name the November 3, 2026 ballot, which has passed; Rule 13.10 would then require what happened, with its own source, which the snapshot does not hold
- D3-xxx | Rule 15.17 draws the seven authority connections as a ladder, one 156 px column of pills in three bands, lines in nested lanes (economy on the right, technology on the left), and prints "decides" once in a key | A stacked two-column layout forced two lines through a 17 px gap and crowded seven labels against the layer names; in the ladder no line crosses another, every first run holds its delay ticks, and the build checks both
- D3-xxx | Rule 15.17's failure folds the four bodies into one pill, "The government" | The misreading the rule answers: power drawn as one actor hides who decides what, and needs no invented connection
- D3-xxx | Rule 15.18's failure keeps the honest drawing and prints the grade alone | One fault per plate: Rule 15.7's failure already draws a conceptual loop solid and numbered
- D3-xxx | Rule 15.15's failure takes the wide stage | It draws two loops side by side, as 15.3's and 15.4's failures draw two and three connections (D3-605)
- D3-xxx | Chapter 15's groups are 1 (15.1 to 15.10), 2 Reforms on the drawing (15.11, 15.12) and 3 Worked examples (15.13 to 15.18) | Round 1's note: the worked examples become group 3 when 15.11 and 15.12 land
- D3-xxx | "Leverage" is replaced by "places to intervene in a system" and "bands of change" | Chapter 02's banned list; Meadows' own subtitle carries the idea

## Requests

(None yet.)

## Tested

(Being filled.)

## Not tested

(Being filled.)

## Files

- `work/build/scripts/phase-3/phase3_ch15_build.py` (modified)
- `work/build/guide/chapters/15-systems-graphics.json` (written by the generator)
- `work/build/guide/specimens/s-15-11-correct.html` to `s-15-18-failure.html`, 12 new plates, and the 25 round 1 plates rewritten unchanged in content (written by the generator)
- `work/build/guide/specimens/manifest-systems-graphics.json` (written by the generator)
- `work/handoffs/phase-3/20261112_Round-2-Systems-Designer-Notes.md` (this file)
