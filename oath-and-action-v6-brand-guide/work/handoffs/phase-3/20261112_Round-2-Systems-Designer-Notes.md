# Round 2 notes: systems designer, chapter 15 Systems graphics

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Written by the systems designer (a general-purpose agent briefed as the designer of chapters 11, 12 and 15's systems plates) for `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md` (DR-244, D3-659). Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Rules 15.11 and 15.12 (group 2, reforms on the drawing) and worked examples 15.15 to 15.18 (group 3) are built by `work/build/scripts/phase-3/phase3_ch15_build.py`, each with a correct and a failure plate: 12 new plates, 37 in the chapter. They sit on round 1's stage (D3-603 to D3-613): true 296 px drawings, the 680 px composition where the frame holds it and one 328 px column below it, every plate rule in the chapter's `plate_css`, no style in any plate. The six rules left the generator's `PLANNED` list, which now holds 15.19 to 15.25 only.

Every atlas value is read by script from `work/extract/atlas-v7-data.json` (snapshot of October 15, 2026) and held by a `need()` check. Every value the brief names matched the model, so nothing differs: Loop B4 (D5, C3, C5; L23 minus, L24, L54) and Loop R10 (C1 to C4; L08, L25, L53, L42) share Variable C3 alone; Reform R-01 targets L25, L08 and C2, sits on Loops R10, B4 and R11, codes DQ +M, GE +S, EP 0, EQ 0, and has routes BI (medium, checked 2026-10-15), SS (low, no date), LOC (medium, checked 2026-10-15) and FS (very low, no date); the seven authority connections are LE02, LE03, LE19, LT13, LT14, LT16 and LT17; Loops B2, B3 and R9 are the three conceptual loops.

**Chapter 15 weighs 302,270 bytes in the final strict build (after the data lead's SD-6 to SD-8; 298,728 before), 50 percent of its 0.60 MB ceiling** (round 1 closed at 184,665). The page is 10,589,819 bytes, projected 15,042,488, with 0 warnings.

**The editor's words pass is applied** (`20261112_Round-2-Editor-Notes.md`, "Words for the systems designer", run 3): all eleven changes, nine on the six new rules and the two round 1 "Basis" lines of 15.13 and 15.14, and the two titles the main session ruled (D3-670): 15.16 "Show a reform’s four effects apart, with each route’s check date." and 15.17 "Draw who holds power over each layer in one authority diagram." Neither old title printed anywhere else (the `PLANNED` list no longer held them; no opener, index or alt cites them). The data lead's requests had not landed when I finished. The V7 check finds 0 failures in chapter 15's 102 chips. RS-S1 landed on the engineer's side with nothing for me to set (R2-C6); at 1024 and 768 px the 15 round 1 wide plates and my 6 new correct plates and 15.15's failure take the 680 px stage, checked by capture.

### The six rules

| Rule | Correct plate | Failure plate | Example log |
|---|---|---|---|
| 15.11 Place a reform on the exact connections and variables it targets, with its band. | Reform R-03 at the head; Loop R4a with Connection L42 and Variables C1 and D7 in Rule 12.5's red and the rest in ink; Variable C4 named as sharing C1's cluster and staying in ink; its targets in chips; its band, rules, in the atlas's words; its three loops | The red set by the electoral competition cluster: C4 red, D7 in ink, a note "acts on electoral competition" | D02 |
| 15.12 Grade the evidence for the problem and for the remedy apart. | Reform R-32 at the head; the chain TC2, B2, C3 across the technology and core boundary, its three targets red; the drawing's own label (both connections well supported); then two labels apart, problem Well supported and remedy Hypothesis, each with the atlas's words | One label, Well supported, over the whole reform | D01 |
| 15.15 Follow a variable two loops share through each loop in turn. | Loop B4 beside Loop R10, Variable C3's pill filled in ink in both; under each, the connection into C3 and the one out of it with the atlas's sentences on their signs; where the loops meet, in the atlas's words | The shared variable under two names, Electoral pressure and Risk of losing office, with no mark | D04, D02 |
| 15.16 Show a reform’s four effects apart, with each route’s check date. (title by D3-670) | Reform R-01 at the head; Loop R10 with L08, L25 and C2 red; its loops; its two grades as two labels (Rule 15.12); effects one family to a row with pips, code and words, as of October 15, 2026, and the atlas's note that codes are never added; routes with who acts, feasibility, and "Checked October 15, 2026" for BI and LOC, "Not checked" for SS and FS | One "overall" +L score and every route dated October 15, 2026 | D02 |
| 15.17 Draw who holds power over each layer in one authority diagram. (title by D3-670) | The seven authority connections as a ladder: the economy layer, the four core bodies and the technology layer in one column of 156 px pills; lines into the economy layer in nested lanes on the right, into the technology layer on the left, none crossing; a key for "decides"; each connection named beside it, grouped by layer | One pill, "The government", for the four bodies | D05 |
| 15.18 Print a conceptual loop's missing chain beside its grade. | Loop B2 in hollow lines and thin pills, its label "Well supported, the atlas's grade for the mechanism; no numbered chain, which the atlas calls the weakest point"; the atlas's words on the missing chain; its station tied to Variable A4; Loop B3 and Loop R9 with their grades, side by side under the drawing | The same drawing with the grade alone in its label | D08 |

Rule 01.9 over the chapter's 27 examples: D01 4, D02 5, D03 3, D04 2, D05 3, D06 3, D08 3, D09 1, D10 3; no domain over one in four, no state named.

## Routine calls

- D3-xxx | Rule 15.11 draws Reform R-03 on Loop R4a, which holds all three of its targets (one connection, two variables) | A reform with both kinds of target, all on solid lines, away from the Loop R10 plates of 12.5, 15.6, 15.15 and 15.16; R4a's cluster split (C4 and C1 in electoral competition, D7 in governing institutions) lets the failure show red set by a cluster
- D3-xxx | Rule 15.12 draws Reform R-32 on the chain TC2 to B2 to C3, with three grade labels: the drawing's own (Rule 13.1), then the problem's and the remedy's apart | Problem well supported and remedy hypothesis is the widest gap among reforms whose targets draw as one solid chain; by script, 49 of the 50 reforms carry two different grades, and in 48 the remedy's is the lower in Rule 13.3's order (R-38 is the one the other way)
- D3-xxx | A red target is drawn only on a solid connection, and the generator stops on a patterned one | A patterned red target with delay ticks needs its lead-in at the 6 px sizes, which chapter 13's helper does not draw either; every target drawn is documented or well supported
- D3-xxx | A reform's chip and title head its plate, above the evidence label; the note under it reads "It acts where the marks turn red: on one connection and two variables" | In the phone column the reform is named before its red appears; the chip and title stand above the note, so repeating the chip read as a stutter (Rule 12.5's note still names the reform with them)
- D3-xxx | Rule 15.15 marks the shared variable by filling its pill in ink with its name in the surface color, the one fill a pill takes | Red belongs to reforms (Rule 12.5) and a heavier outline to red targets (Rule 15.1); a fill reads at once in both drawings, in gray print and on Charcoal
- D3-xxx | Rule 15.15 keeps Loop R10 on Rule 15.6's square, so Variable C3 sits at the lower right in both loops | One orientation for one loop across the chapter
- D3-xxx | Rule 15.15 says the atlas names four variables Loop B4's strength depends on, and that two of them, C1 and C2, are the ends of Loop R10's first step | Exact to the atlas's sentence, which lists C1, C2, B2 and B4; the build holds the list and L08's ends
- D3-xxx | Rule 15.16 prints no route note and no status text, only each route's who, feasibility and date | R-01's notes and status name the November 3, 2026 ballot, which has passed; Rule 13.10 would then require what happened, with its own source, which the snapshot does not hold
- D3-xxx | Rule 15.16 prints its two evidence grades as two labels under "Its two grades, apart (Rule 15.12)" | The worked example applies the rule just before it
- D3-xxx | Rule 15.17 draws the seven authority connections as a ladder (one 156 px column in three bands, lines in nested lanes 12 px apart, economy on the right and technology on the left) and prints "decides" once, in a key | A stacked two-column layout forced two lines through a 17 px gap and crowded seven "decides" against the layer names; in the ladder no line crosses another, every first run holds its delay ticks, and the build checks both; each connection's name beside the diagram says who decides what
- D3-xxx | Rule 15.17's failure folds the four bodies into one pill, "The government" | The misreading the rule answers: power drawn as one actor hides who decides what, and the plate needs no invented connection
- D3-xxx | Rule 15.18's failure keeps the honest drawing and prints the grade alone | One fault per plate; Rule 15.7's failure already draws a conceptual loop solid and numbered
- D3-xxx | Rule 15.15's failure takes the wide stage | It draws two loops side by side, as 15.3's and 15.4's failures draw two and three connections (D3-605)
- D3-xxx | In 15.11 and 15.16 the loops a reform sits on print under the drawing, and in 15.18 the other conceptual loops print side by side under both columns | The columns balance at 680 px (15.11 at 727 px tall, 15.18 at 687, 15.16 at 1,369)
- D3-xxx | A connection's chip and grade word sit in one no-wrap span, in every plate (`gl()`) | A no-break space alone did not hold across the chip's inline box ("Out of it Connection L24" broke before "Well supported"); round 1's six plates that print a connection with its grade change by that span only, checked by diff
- D3-xxx | The generator now stops on a red mark beyond a reform's targets, any red on a plate without a reform, a word that adds effects (overall, total, net effect) outside the rule's own "Never" line, a printed route whose date differs from its record, and chapter 15 over 600,000 bytes | The docstring's promises, made real; each was tested by planting the fault
- D3-xxx | Chapter 15's groups are 1 (15.1 to 15.10), 2 Reforms on the drawing (15.11, 15.12) and 3 Worked examples from the atlas (15.13 to 15.18) | Round 1's note: the worked examples become group 3 when 15.11 and 15.12 land
- D3-xxx | "Leverage" gives way to "places to intervene in a system" and "bands of change" | Chapter 02's banned list; Meadows' own subtitle carries the idea
- D3-xxx | The editor's run 3 words are applied in the generator: nine lines on the six new rules and the round 1 "Basis" lines of 15.13 and 15.14; titles 15.16 and 15.17 as D3-670 rules them | D3-615: the editor owns the words, the systems designer the file
- D3-xxx | Rule 15.18's source line reads "loop B2, loop B3 and loop R9", and the generator now stops on an R9 or R13 that "Loop" does not directly precede | The guide check's codes test reads a bare R9 or R13 as a decision code; "loops B2, B3 and R9" would have failed it (tested by planting it back)
- D3-xxx | My two "Basis" lines name the record after the ID ("the profile of Reform R-01", "the record and evidence summary of Loop B2") | The shell holds an ID whole, and a possessive after it ("R-01’s") wrapped alone to the next line at 390 px

## Data lead's sign-off, applied (second run)

The data lead signed off the six rules with three requests (`20261112_Round-2-Data-Lead-Notes.md`, "Requests to the systems designer"), all applied in the generator:

- **SD-6.** 15.15's Loop B4 label reads "Well supported, strong research evidence, the grade of all three steps" (a loop whose steps share one grade names none as least certain), and Connection L54's line adds the atlas's words: the weakest for U.S. services, "since its main study covers Brazilian mayors" (held by `need()`).
- **SD-7.** Every drawn connection prints its grade word: "Each step" under the drawing in 15.11 (L42, L55, L56) and 15.16 (L08, L25, L53, L42), and "The loop's other steps" under each loop in 15.15 (L54; L08 and L42), numbered in the atlas's order, read from the model; the alts say so.
- **SD-8.** Rule 15.5's "Word" spec reads "Decides, where a causal line prints its verb, or once in a key where every line in the drawing is an authority connection (Rule 15.17)".

Tested: the generator's checks pass; strict build exit 0, 0 warnings, chapter 15 at 302,270 bytes against 600,000, the page at 10,586,929, projected 15,042,488; the V7 check, 0 failures in chapter 15's 112 chips; 15.11, 15.15, 15.16 and 15.5 captured at 1440 and 390 px (type 13 px or more, nothing outside its stage, no overlap) and 15.11, 15.15 and 15.16 read by eye at both widths. Not tested: Charcoal and the other widths for these three after the change; the guide check after the change.

## Requests

### To the data visualization lead
1. **Sign-off of chapter 15's 12 new plates** (D3-659), from the final build (scratchpad `phase-3/round-2/systems-designer/guide-final.html`, captures in `cap/final3/` at 1440, 1024, 768, 390 and 360 px on both grounds). Points I would like ruled on: (a) Rule 15.17 prints "decides" once, in a key, where Rule 15.5 prints it on each line; (b) Rule 15.15's filled pill for a shared variable; (c) Rule 15.12's three labels on one plate (the drawing's, the problem's, the remedy's); (d) Rule 15.16 leaves out route notes and status text because they name the November 3, 2026 ballot; (e) on Charcoal, the red target's case takes the essential ink token, which is light there, so a red line carries a light edge (chapter 13's targets do the same).

### To the editor
2. Done: your run 3 words are applied, the two round 1 "Basis" lines included, and the main session ruled both titles (D3-670). A second read of the changed lines is welcome: 15.11's rule (the band defined at first use), 15.12's two named connections under the drawing, 15.15's rule, 15.17's rule, why, "Decides" spec and note, 15.18's line on Variable A4.

### To the main session
None blocking. For the makers, from my quick guide check: s-14-55-sketch sets type at 32 px and "of the whole" at a 2.42 contrast ratio (maker A), and s-14-66-sketch paints an ellipse 14 px outside its drawing (maker B), at 1440 and 390 px.

## Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch15_build.py`: every check passes, round 1's and round 2's (no em dash or U+2011, no listed word, no studio word or code, titles of fifteen words or fewer, failure captions led "Fails Rule 15.N." with the do-not-publish band and an alt opening "Failure case: do not publish.", no literal color, no px font size, no heading element, no drawing over 296 px, every stage 328 px with the wide ones at 680, no style in a plate, `plate_css` with no media query and no container but `oa-frame`, every chip's ID in the atlas (now with route codes), each plate's red count equal to its reform's targets and zero elsewhere, no adding word, every route's date as its record holds it, the 0.60 MB ceiling, Rule 01.9 over 27 examples) and every `need()` on the atlas values above.
- Planted faults, each caught by the generator's check: a red outline on a variable a reform does not target (15.11), red on a worked loop with no reform (15.15), "Total effect" in 15.16's plate, Route SS printed "Checked October 15, 2026", Route BI printed "Not checked", a bare R9 in 15.18's source line.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide-ed.html`, after the editor's words: exit 0, 0 warnings; chapter 15 at 298,728 bytes against 600,000; the page at 10,589,819 bytes, projected 15,042,488 (the page grows as other owners land work). The V7 check on that build: 0 failures, chapter 15 at 102 chips.
- `node work/build/scripts/phase-2/guide_check.js <scratch>/guide-qc2.html --quick --no-captures` (1440 and 390 px) on the strict build before the editor's words: FAIL with 6 failures, none in chapter 15: s-14-55-sketch (type at 32 px, one text item at 2.42 contrast) and s-14-66-sketch (a shape 14 px outside its drawing), each at both widths. Chapter 15's codes, type, frame, red and contrast tests pass. An earlier run on a build with "loops B2, B3 and R9" was stopped once I found and fixed that line.
- After the editor's words: 15.12, 15.17 and 15.18's correct plates captured at 1440 and 390 px (type at 13 px or more, nothing outside its stage, no overlap) and read by eye at 1440 (15.12's named connections under the drawing, 15.17's note with each variable's name); 15.18's changed line read back from the plate file.
- `python3 -I work/build/scripts/phase-3/v7_check.py --page <scratch>/guide-final.html`: 0 failures; chapter 15 at 102 chips.
- Captures in Chromium (Playwright) of the 12 new plates from the final build at 1440, 1024, 768, 390 and 360 px on Newsprint and on Charcoal (each stage's surface class set to Charcoal in the page), 120 captures (taken before 15.18's source line changed from "loops B2, B3 and R9" to "loop B2, loop B3 and loop R9", the only change since), measured by script: type at 13 px or more, no text outside its stage, no two drawing labels overlapping, no frame scrolling; wide plates at 680 px at 1440, 1024 and 768, every other stage at 328.
- Read by eye, at 1440 on Newsprint unless named: all six correct plates and all six failures, as they stood before the last layout change; after it, 15.11 and 15.16 at 1440 and 15.12 at 390; 15.15 and 15.16 at 1440 on Charcoal; 15.17 at 1024 on Charcoal; 15.12 at 768; 15.16 and 15.17 at 390 and 15.15 at 360; 15.12 and 15.11 at 360 and 15.18 at 390 on Charcoal; 15.11 in grayscale at 390, where the red target reads by its 4 px line, 6 px tag and head and 3 px outline.
- Round 1's plates: byte-identical to the commit but for the chip-and-grade span in six of them (checked by diff); the opener, 15.3, 15.6, 15.8, 15.9 and 15.10 recaptured at 1440, 390 and 360 px with the same measures, 15.6 and 15.10 read by eye.

## Not tested

- The guide check's full four-width run (zoom, text spacing, forced colors), and the quick run on the build after the editor's words (which changed words only, checked by the generator, the strict build and the V7 check).
- A 320 px window; print; forced colors; color-vision simulations.
- A screen reader on the new alts, keys and lists.
- The guide check after the data lead's SD-6 to SD-8 (words and step lists only).

## Files

- `work/build/scripts/phase-3/phase3_ch15_build.py` (modified)
- `work/build/guide/chapters/15-systems-graphics.json` (written by the generator)
- `work/build/guide/specimens/s-15-11-correct.html` to `s-15-18-failure.html`, 12 new plates, and six round 1 plates rewritten with the chip-and-grade span (written by the generator)
- `work/build/guide/specimens/manifest-systems-graphics.json` (written by the generator)
- `work/handoffs/phase-3/20261112_Round-2-Systems-Designer-Notes.md` (this file)

## Review fix pass

Written for `work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md` and the coordinator's addendum (AX S10). Items: BC S4 (under the data lead's RF-16 and RF-16a), BC S15 (under RF-21), BC S16, CD CH15-S1 and AX S10's chapter 15 half. Every atlas value is still read by script from `work/extract/atlas-v7-data.json` and held by `need()`; the atlas's text stays as stored (D3-349).

### Summary

All five items are done by code in `work/build/scripts/phase-3/phase3_ch15_build.py`, which rewrote `work/build/guide/chapters/15-systems-graphics.json`, 18 plates and `work/build/guide/specimens/manifest-systems-graphics.json`. The main session's snapshot commits took in the work as it went, so my files now match HEAD; the changes below run from 011cbdec, where the pass started.

- **BC S4 (RF-16, RF-16a, D3-906).** Rule 15.17's four core pills print the variables' own titles: Presidential action without new legislation (D2), Congress’s ability to write and check policy (D1), Ability to investigate and enforce the rules (D4) and State and local testing of reforms (D6). The rule's first paragraph takes RF-16's words ("from a variable in the core layer that holds a body’s power, such as Congress’s ability to write and check policy"). By RF-16a, 15.3's card for L16 and 15.5's two cards draw D4 and D6 under their titles too; 15.5's pills take 148 and 132 px so each sets in three rows. The opener and every loop drawing keep the loops' chain labels.
- **BC S15 (RF-21).** Rule 15.12's plate drops the label over its drawing. Its first label is the problem's, Well supported, and its second the remedy's, Hypothesis; each connection's grade sits in a numbered "Each step" list under the drawing. The note "It acts where the marks turn red" moved under the drawing, where it explains the red.
- **BC S16.**
  - No punctuation touches a typed chip on any plate. A variable's chip takes its title in quotation marks, as a connection's takes its name; the loops a reform sits on print as a row of chips; the other lines are recast so words follow a chip. That covers 19 places in nine plates, round 1's 15.10, 15.13 and 15.14 among them.
  - 15.18's label holds "weakest point" together, and every plate's notes, labels, quotations, sources and list items set with `text-wrap: pretty`.
  - 15.18's line on Variable A4 now ends "which is Variable A4 in the atlas’s model."
  - 15.18 spells out UI from the atlas's own summary of Loop B2: unemployment insurance, the atlas's example of “benefits written into law” that “expand without a new vote”.
  - A four-variable loop's ID now sits above its side steps' tags, so "Loop R10 reinforcing" no longer reads on one line with step 4's words. The same drawing moves in 15.6 (both plates) and 15.16, and the drawings keep their heights.
  - The size line is the shell's. I asked the engineer, who held "under 680 px" together with no-break spaces in `guide_build.py`; at 390 and 360 px its last line now reads "under 680 px".
- **CD CH15-S1.** 15.15's L54 line reads "Connection L54 Well supported. The atlas calls it the weakest for U.S. services, …"; any step with words after its grade word takes the period.
- **AX S10.**
  - Rule 15.12's plate carries a short key, "Reading a step", across both columns under the drawing. It covers the step words (money, lowers and information, raises), the ticks (two for 2 to 10 years and three for over 10 years) and the two layers, all read from the connections' own records.
  - Rule 15.12's rule glosses "line code" at first use: "the solid, dashed or dotted line Rule 13.4 sets by grade".
  - Rule 15.17's plate lists "The four bodies, as the atlas’s connections name them" under the drawing, each body with its variable's chip and title: Congress, the executive, antitrust enforcers, states and cities. The names come from the atlas's own connection names, and the build stops if a connection from a variable stops naming its body.
  - Rule 15.17's key adds the ticks, drawn as a short authority line with two ticks: one for under 2 years and two for 2 to 10 years.

The editor's second pass on these words is applied: seven rows, listed under "Words changed" below. Chapter 15 weighs 306,894 bytes in the final strict build, against its 600,000 ceiling (302,270 at the end of round 2).

### Routine calls

- D3-xxx | Rule 15.17's four core pills print the variables' own titles, and Rules 15.3 and 15.5 draw D4 and D6 under theirs; the opener and every loop drawing keep the loops' chain labels | RF-16 and RF-16a (D3-893, D3-906); the generator stops if 15.3, 15.5 or 15.17 prints a chain label for D1, D2, D4 or D6
- D3-xxx | Rule 15.17's rule says each line runs from a variable that holds a body's power, and names each body beside the diagram as the atlas's connections name it | RF-16's words; the reader in production test 2 asked whether "Congressional capacity" is a body or a measure (AX S10)
- D3-xxx | Rule 15.17 lists the four bodies under its drawing, each with its variable's chip and title, the body's name read from the atlas's connection names (Congress, The executive, Antitrust enforcers, States and cities) | AX S10 asked for each body's plain name with its variable name; the columns stay balanced at 680 px
- D3-xxx | Rule 15.5's two pills take 148 and 132 px, each three rows | At 140 px "Ability to investigate and enforce the rules" set four rows with "rules" alone, and the two lines left their pills at different heights
- D3-xxx | Rule 15.12's plate leads with its two grades as its only labels; the connections' grades sit in a numbered list under the drawing, and the drawing carries no label of its own | BC S15 under RF-21; the correct plate's first label no longer matches the failure's one label. Rule 15.12's specs now say so ("Order"; "Connections")
- D3-xxx | Rule 15.12's note "It acts where the marks turn red" sits under the drawing, above its steps | Beside the drawing it read as part of the remedy's block
- D3-xxx | Rules 15.12 and 15.17 carry a short key built from the drawn connections' own types, signs and delays; 15.12's runs across both columns under them | AX S10; a reader who lands by a link needs the key on the plate, and set across both columns it keeps the columns balanced
- D3-xxx | Rule 15.12's rule glosses the line code at first use | AX S10: "line code" stopped the reader (H02)
- D3-xxx | No punctuation touches a typed chip: a variable's chip takes its title in quotation marks, a list of loops is a row of chips, and other lines are recast; the generator stops on a chip followed by punctuation | BC S16: the chip's 8 px padding and edge set a comma or a period apart ("Variable C1 , seats"); round 1's three cases change with round 2's
- D3-xxx | A four-variable loop's ID sits above its side steps' tags, centered between the top row's pills and the higher tag; the generator stops if the room is short | BC S16: "4 raises + Loop R10" in 15.15; 15.6 and 15.16 draw the same loop and change with it
- D3-xxx | Every plate's notes, labels, quotations, sources and list items set with `text-wrap: pretty`, and 15.18's label ties its last two words | BC S16: "point" stood alone; the tie holds where a browser ignores `pretty`
- D3-xxx | 15.18 spells out UI in the atlas's words for Loop B2 and keeps the chain label "Automatic support (UI, credits)" as stored | BC S16 and D3-349; the build holds the summary's sentence
- D3-xxx | A grade word with words after it ends with a period, and the generator stops on one that runs on | CD CH15-S1

### Words changed, for the editor's second pass

Each line is in the generator's data; I own the file and will apply any change (D3-900).

- **15.10 correct (round 1).** The heading reads "From Variable TC1 to Variable B4 “Hostility toward the other political party”". The note reads "Its reason opens on the drawn connection: feed ranking “changes what people see”, as Connection LT01 records."
- **15.11 correct.**
  - The targets read "Variable C1 “Seats with little electoral competition”" and "Variable D7 “Entrenched control of rule-setting institutions”".
  - The cluster note reads "Variable C4 sits in the electoral competition cluster with Variable C1 and stays in ink."
  - Its loops print as a row of chips, then "The drawing shows Loop R4a because it holds every target." 15.16 shows the same with Loop R10.
  - The alt says the same.
- **15.12.**
  - Rule, second paragraph: "A drawing of the reform carries a third grade in the line code of each connection, the solid, dashed or dotted line Rule 13.4 sets by grade, which says how sure the atlas is of the mechanism. Print each connection’s grade word in the list of steps under the drawing, and keep all three grades apart. …"
  - Caption: "… each in the atlas’s words, with each connection’s grade in the list of steps under the drawing."
  - Specs: "Order", "The problem’s label first and the remedy’s second, as the first two labels on the plate"; "Connections", "Their own line code (Rule 13.4), and each one’s grade word in the list of steps under the drawing".
  - Plate: the head "Each step"; the key "Reading a step" with its three items.
  - The alt.
- **15.13 correct (round 1).** "The atlas’s evidence summary names Connection L02 as the middle step, which “is plausible and the weakest.”" The alt says the same.
- **15.14 correct (round 1).** "… says the loop “no longer depends on” Variable A1 “Concentration of household wealth”." The alt says the same.
- **15.15 correct.**
  - "Variable C3 “Risk of losing office” is the pill filled in ink in both drawings."
  - "Of the four variables the atlas says its strength depends on, Variable C1 and Variable C2 sit at the two ends of Loop R10’s first step."
  - L54's period.
  - The alt.
- **15.16 correct.** The target "Variable C2 “How often the primary decides the winner”" and the loops row.
- **15.17.**
  - Rule, first paragraph, as above.
  - Caption: "… from the powers of four bodies in the core layer to four variables in the economy and technology layers, with each body and each connection named beside it."
  - Specs: "Bodies" and "Key" (which replaces "Decides").
  - Plate: the list head "The four bodies, as the atlas’s connections name them" and its four rows; the key's ticks line; "Two bodies decide each of Variable EC2 “Public investment in research and infrastructure”, Variable TC5 “Government’s ability to build and run digital services” and Variable TC7 “Use of pricing algorithms”; one decides Variable EC10 “Costs of tariffs and trade rules”."
  - The alt.
- **15.18 correct.**
  - "Household hardship is “the reverse of households’ financial security”, which is Variable A4 in the atlas’s model." This replaces your run 3 line, which ended on the chip and its period.
  - "In the pill, UI is unemployment insurance, which the atlas gives as its example of “benefits written into law” that “expand without a new vote”."
  - The alt.
- **15.3 and 15.5 (round 1).** Their alts name D4 and D6 by their titles.

### The editor's second pass, applied

The editor's seven rows (`20261112_Round-2-Editor-Notes.md`, "Second pass: words for the systems designer (chapter 15)") are applied as written:

- 15.12's rule, second paragraph, opens "A drawing of the reform carries a third grade, how sure the atlas is of the mechanism. Each connection shows it in its line code, the solid, dashed or dotted line Rule 13.4 sets by grade."
- 15.17's rule and its "Bodies" spec read "carrying the variable’s own title".
- 15.17's "Key" spec reads "Two entries: decides, printed once because every line in the diagram means the same, and the delay ticks (Rule 13.5); …".
- 15.11's note and alt name Variable C4 with its title and "the pill at the top".
- 15.10's heading names Variable TC1 with its title. It holds three lines at 1440, 1024, 768, 390 and 360 px, measured in Chromium, so the editor's fallback was not needed.

- D3-xxx | The editor's second-pass words for chapter 15 are applied in the generator | D3-900 and D3-615: the editor owns the words, the systems designer the file

### Requests

1. **Data lead.** Sign-off, as offered: Rule 15.17's plate (node titles, the four bodies, the key's ticks); Rule 15.12's plate (RF-21's order, the step list, the key); the cards of 15.3 and 15.5 under RF-16a; and the moved loop ID in 15.6, 15.15 and 15.16. The final build is `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-fix/systems-designer/guide3.html`, with captures beside it in `cap/final3/` (all 37 plates on Newsprint at five widths) and in `cap/final-ch/` and `cap/final3-ch/` (Charcoal).
2. **Editor. Done:** your second pass, applied as written (below).
3. **Engineer. Landed:** the size line's no-break spaces in `guide_build.py` (BC S16's last point).
