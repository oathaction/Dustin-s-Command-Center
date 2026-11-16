# Fix pass editor notes

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7, November 16, 2026. Editor (`oa-editor`), under `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md` (the editor's row binds). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/fix/editor/`. Written as I go; the container can restart.

The owners read the "Words for ..." sections directly. Each row gives the file, the place, the exact old string and the exact new string, and why. The owner applies them in its generator. Once an owner reports done, I read its changed words a second time and write any correction straight into its generator, after telling the main session (D3-669). I never touch a key that picks a mark or an ink.

## Status

- 17:00 UTC. Started. Read `CLAUDE.md`, my role file, chapter 02's writing rules, the fix brief, the CE, ST, DF and NB reports, and my round 5 notes. Working tree clean at `8ace3dc6`. The data lead's and research lead's fix pass notes are not posted yet. Next: the current words behind each code, then the "Words for ..." sections, hardest first.

## Words for the complex examples maker

Written 17:10 to 17:20 UTC, after the data lead's rulings R2 to R5 (posted 17:08). "Old" strings are the printed words as `phase3_ch14_complex_build.py` held them at `8ace3dc6`, or the code line where the words are built; match them against your working copy. Every figure and atlas value is the data lead's or the research lead's; I add none. Where a row says "computed", the words come from the generator, never typed, so the build can hold them (R2, item 1).

### CE-M1, Rule 14.143's walk (ruling R2)

**The seven lines**, the first sentence of each step (the status line and the still list read it first). Cause first, the walk's direction at both ends; "can" from the plausible step on (R2, item 2); "goes up" and "goes down" after the title that asks how often, since "how often ... rises" stops the ear; "rise" where the title is plural (`PLURAL`). Titles whole (DR-265), by `in_sentence` as now.

| Step | Line now | Line, new |
|---|---|---|
| B4, 1 of 3 | The quality of public services lowers the risk of losing office. | The quality of public services falls, so the risk of losing office rises. |
| B4, 2 of 3 | The risk of losing office raises the number of incumbents defeated or pushed into retirement. | The risk of losing office rises, so the number of incumbents defeated or pushed into retirement rises. |
| B4, 3 of 3 | Incumbents defeated or pushed into retirement raise the quality of public services. | The number of incumbents defeated or pushed into retirement rises, so the quality of public services rises. |
| R10, 1 of 4 | Seats with little electoral competition raise how often the primary decides the winner. | Seats with little electoral competition rise, so how often the primary decides the winner goes up. |
| R10, 2 of 4 | How often the primary decides the winner lowers the risk of losing office. | How often the primary decides the winner goes up, so the risk of losing office falls. |
| R10, 3 of 4 | The risk of losing office can lower officeholders’ control over election rules. | The risk of losing office falls, so officeholders’ control over election rules can rise. |
| R10, 4 of 4 | Officeholders’ control over election rules raises seats with little electoral competition. | Officeholders’ control over election rules can rise, so seats with little electoral competition can rise again. |

How to compute it (a suggestion; the build is yours): carry a direction from `START` through each sign; the cause takes "can" when an earlier step of the same loop is plausible, the effect when this step or an earlier one is; a cause that is Variable C5 reads through `OBJECT` ("the number of incumbents ..."), as the effect already does; "again" only on the step that closes a reinforcing loop. Stop the build if a printed direction differs from the computed one.

**The connection's own claim moves into the further words** (R2, item 3), with its sign in words that hold either way. The `more` template (line 220 at `8ace3dc6`):

- Old: `{chip} “{name}”: {moves}the atlas grades it {grade}{least}, and its effect takes {delay}.` printed as, for L23, "Connection L23 “Poor service raises incumbents’ risk of losing”: the atlas grades it well supported, and its effect takes under 2 years."
- New: `{chip} “{name}” carries a {minus|plus} sign, which means {sign words}{, and money moves along it}. The atlas grades it {grade}{least}, and its effect takes {delay}.` Sign words: for a minus, "that when one rises, the other falls"; for a plus, "that the two rise and fall together". The money, information or ownership clause, where a connection has one, joins the first sentence as ", and {type} moves along it". Printed for L23: "Connection L23 “Poor service raises incumbents’ risk of losing” carries a minus sign, which means that when one rises, the other falls. The atlas grades it well supported, and its effect takes under 2 years."

**Loop R10's first step.** The line now states the rise, so the start sentence after it says where the walk is, not the supposition a second time as a command.

- Old: "The walk moves to Loop R10. Start at seats with little electoral competition, and suppose they rise."
- New: "The walk moves to Loop R10, starting at seats with little electoral competition and supposing they rise."

**Each loop closes on its result** (R2, item 4), in Rule 15.6's words: "pushes back" for balancing (its rule text) and "feeds itself" (its why).

- B4, old: "Loop B4 is back where it began, at the quality of public services, and with one minus sign on its steps it is balancing."
- B4, new: "Loop B4 is back where it began, and the quality of public services now rises, against the first fall. The loop pushes back, so it is balancing, as its one minus sign shows."
- R10, old: "Loop R10 is back where it began, at seats with little electoral competition, and with two minus signs on its steps it is reinforcing. The atlas holds no measure of either loop’s strength, so the walk weighs neither against the other."
- R10, new: "Loop R10 is back where it began, and seats with little electoral competition can rise again, on top of the first rise. The loop can feed itself, so it is reinforcing, as its two minus signs show. The atlas holds no measure of either loop’s strength, so the walk weighs neither against the other."

The count stays computed (`words_n`, "sign" or "signs"). The two sentences naming Variable C3 ("The risk of losing office is the variable both loops pass through." and "Here Loop R10 reaches the risk of losing office, the variable Loop B4 also passes through.") and the atlas's weakest-step sentence on L54 stay as they are. The ready line stays (R2, item 5).

**Rule 14.143's text**, so the rule asks for what the plate now does. `rule[1]`, its first two sentences (line 425):

- Old: "At each loop’s last step, say that the loop is back where it began and name its kind. Say too where the second loop reaches the shared variable."
- New: "Start each loop from a rise or a fall, and say each step in the direction the walk runs, cause first, as in “The quality of public services falls, so the risk of losing office rises.” After a step the atlas grades plausible, say “can” to the end of the loop. At the last step, say that the loop is back where it began, whether it pushes back or feeds itself, and name its kind. Say too where the second loop reaches the shared variable."

The spec "Status line" ("The loop and its own count, as “Loop R10, step 2 of 4”, then the step’s words") stands. The alt (line 383) says what the drawings hold and needs no change. The failure plate's list prints the new lines, which keeps its one fault (no loop names, one count); its caption stands.

### ST-M1, Rule 14.142's failure caption and alt (ruling R3)

- Caption, old: "<strong>Fails Rule 14.142.</strong> With no band, all seven drops read as jobs lost, and the title counts seven losses as findings. Five of the seven sit inside the survey’s margin of error."
- Caption, new: "<strong>Fails Rule 14.142.</strong> The chart leaves out the survey’s margin of error, so all seven drops look alike, and the title states seven months of lost jobs with no word on the margin. Five of the seven sit inside the margin, where the survey cannot tell them from no change."
- Failure alt, old: "The same columns with no band and the seven drops drawn alike in the strongest ink, under a title that counts seven months of lost jobs."
- Failure alt, new: "The same columns with no band and the seven drops drawn alike in the text’s ink, under a title that states seven months of lost jobs with no word on the margin."

The failure title, "The economy lost jobs in seven months of 2025 and 2026.", stays: it is the fault (R3). The latest label and the margin sentence in the source line come off the failure plate (R3); that is the drawing's, yours.

### ST-S1 and CE-S13, what the 90 percent band means (ruling R4)

- S96 `notes[0]`, old: "The band runs from −122,000 to +122,000 jobs, the Bureau of Labor Statistics’ 90 percent margin of error for one month’s change in its survey of employers. A column that ends inside the band is a change the survey cannot tell apart from no change at that level. The band covers one month’s change, so it says nothing about the three-month average."
- New: "The band runs from −122,000 to +122,000 jobs, the Bureau of Labor Statistics’ 90 percent margin of error for one month’s change in its survey of employers. If a month’s true change were zero, the survey’s estimate would land inside the band nine times in ten. A column that ends inside the band is a change the survey cannot tell apart from no change at that level. The band holds for each month alone, so across 57 months a few columns could pass it by chance, and it says nothing about the three-month average."
- Rule 14.142 `rule[0]`, the second and third sentences, old: "Draw the survey’s margin of error for one month’s change as a band around zero, behind the columns, and give its size, its confidence, such as the Bureau’s 90 percent, and its source in a note (Rule 14.9). Name only the changes that pass it, each with its month and value in the subject ink (Rule 14.6), and print the full count beside them, so a reader still learns how many months fell."
- New (with NB-S1 and the ink word): "Draw the survey’s margin of error for one month’s change as a band around zero, behind the columns, and give its size, its confidence and its source in a note (Rule 14.9). The Bureau of Labor Statistics gives a 90 percent margin, so a month with no real change lands inside the band nine times in ten. The band holds for each month alone, and over many months a few can pass it by chance, so the note says that too. Name only the changes past it that the reader’s question asks about, here the drops, each with its month and value in the text’s ink (Rule 14.6), and print the full count beside them, so a reader still learns how many months fell."
- S96 `alt`, old: "...over a shaded band from minus to plus 122,000 jobs, the survey’s margin of error for one month’s change."
- New: "...over a shaded band from minus to plus 122,000 jobs, the survey’s margin of error for one month’s change, inside which a month with no real change would land nine times in ten."

Not printed, as R4 item 4 says: "a range that would hold the true change in nine samples out of ten" and any count of chance passes.

### ST-S2, where each named drop fell (ruling R4b)

- S96 `notes[1]`, add after its last sentence ("...the other five sit inside it."): "In October 2025, government payrolls fell 153,000 and private payrolls rose 13,000. In February 2026, private payrolls fell 148,000, and government payrolls fell 8,000."

Figures are R4b's, by script from the sector file. No federal figure, no cause. The source line's words for the two sector series are the research lead's (R4b, item 3).

### DF-4, the ink word (D3-914, DR-262)

Five places say "the strongest ink"; each becomes "the text’s ink":

| Where (line at `8ace3dc6`) | Old | New |
|---|---|---|
| S96 `reading_guide` (888) | the two in the strongest ink are the drops past the margin | the two in the text’s ink are the drops past the margin |
| S96 `alt` (914) | Two are drawn in the strongest ink and labeled | Two are drawn in the text’s ink and labeled |
| S96 `chart_notes[0]` (925) | and the two in the strongest ink are the drops past the margin | and the two in the text’s ink are the drops past the margin |
| S96 `phone_notes[0]` (938) | The two columns in the strongest ink: | The two columns in the text’s ink: |
| Failure `alt` (1002) | drawn alike in the strongest ink | drawn alike in the text’s ink (the ST-M1 row above carries it) |

A correction to my round 5 notes: I withdrew this same change then, citing S53's reason for "the strongest ink". S53 had already moved to "the text’s ink" by D3-1043, so my reason was stale and the drift reader is right.

Also in Rule 14.142: spec "Named drops", old "The two past the margin, in the subject ink, each with its month and value"; new "The two past the margin, in the text’s ink, each with its month and value". The token stays.

### DF-3, DF-7 and CE-S14, Rule 14.144's words (ruling R5)

- `rule[1]`, old: "Print each effect as the atlas stores it, the code and then any qualifier, followed by the code’s meaning. A qualifier is the words after a code that say where, when or for whom the effect holds, as in “+L local” or “+M renter-owner”. A zero says “no expected effect”. Set the codes as text in the text ink, with no total, count, average or rank, since the atlas never adds effects across families (Rules 15.16 and 15.21). Print each route’s check date or “Not checked”, with the model’s date, October 15, 2026."
- New: "Draw each effect with Rule 13.5’s pips in the text’s ink, then print it as the atlas stores it, the code and then any qualifier, followed by the code’s meaning. A qualifier is the words after a code that say where, when or for whom the effect holds, as in “+L local” or “+M renter-owner”. A zero says “no expected effect”. Give no total, count, average or rank, since the atlas never adds effects across families (Rules 15.16 and 15.21). Print each route’s check date or “Not checked”, with the model’s date, October 15, 2026."
- Spec "Effects", old: "The atlas’s code and qualifier whole, then its words; zero in words; never added". New: "Rule 13.5’s pips, then the atlas’s code and qualifier whole and its words; zero in words; never added".
- Spec "Routes", old: "Name, who acts, feasibility, and the check date or “Not checked”". New: "Under “Routes, with the date each was checked”: the route, who acts, its feasibility in bold, and the check date or “Not checked”, as Rule 15.20 prints them".
- Spec "Never", old: "A total, a count of plus codes, a rank, or a fill, bar or shade by code". New: "A total, a count of codes or pips, a rank, or a fill, shade, length or color by code".
- The card's grade row, old: "Evidence for the problem". New: Rule 15.16's grade block, as R5 sets it: the grade with Rule 13.3's gloss, then "evidence of the problem" (and "evidence for the remedy" for the remedy grade). Rules 13.3, 15.12 and 15.16 say "evidence of the problem".
- The card's effect rows, old: "Effect on quality of democracy" and its kin. New: one heading, "Effects by outcome family", then each family's name as its row label, as Rule 15.20's panel prints them (R5, item 3).
- The band row (CE-S14): "Band, the kind of change" with the word in bold and the atlas's definition quoted, as your working copy now prints it, stands.
- The failure caption stands if the failure plate keeps codes as text. If it draws the pips (R5, item 7), old: "A total score adds each reform’s four codes as points, so a local or sector-only effect counts as if it held everywhere and two different reforms tie." New: "A total score counts each pip as a point and adds each reform’s four effects, so a local or sector-only effect counts as if it held everywhere and two different reforms tie."

### NB-S1, Rule 14.142's promise

Carried in the `rule[0]` row above: "Name only the changes past it that the reader’s question asks about, here the drops". The title stands ("Mark the survey’s margin on a monthly chart, and name the changes that pass it."), since the rule now says which changes.

### NB-M1, group 18's line

Group 18's line sits in my own generator (`GROUP_LINES[18]` in `phase3_ch14_rules_build.py`), so I change it myself; nothing for you to apply. Old: "...and three reforms that act on one housing loop." New: "...and three reforms whose records name one housing loop." Rule 14.144's own `rule[0]` already says "each reform whose record names one loop".

## Words for the systems designer

(Being written.)

## Words for the tracker designer

(Being written.)

## Fixed

## Not fixed

## Calls

| call | reason |
|---|---|

## Requests

## Tested

## Not tested
