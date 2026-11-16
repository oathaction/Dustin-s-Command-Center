# Fix pass editor notes

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7, November 16, 2026. Editor (`oa-editor`), under `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md` (the editor's row binds). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/fix/editor/`. Written as I go; the container can restart.

The owners read the "Words for ..." sections directly. Each row gives the file, the place, the exact old string and the exact new string, and why. The owner applies them in its generator. Once an owner reports done, I read its changed words a second time and write any correction straight into its generator, after telling the main session (D3-669). I never touch a key that picks a mark or an ink.

## Status

- 17:22 UTC. **The waiting rows are final, and each owner's section says so in its head:** for the systems designer, stage 2 (F3), stage 7 (F4), stage 19 (F7) and ST-M2's row under step 1 (F1); for the tracker designer, CE-S17 (F9), NB-S7's reason (F8) and ST-S3 (F2). **DF-13's Rule 14.6 part**, routed to me at 17:20, is in my generator: the ink words a reader meets in Rules 14.3, 14.5 and 14.6 are defined or said in the reader's word, run twice, the second changing nothing, scratch strict build exit 0, 0 warnings. **ST-S8 revised** to the research lead's placement of the release. **The main session's question on S14's line in chapter 13** is answered below ("S14's release and chapter 13"). Waiting on the main session's word that an owner is done before each second read.
- 17:18 UTC. **All three "Words for ..." sections are final**, the fact rows made final on the research lead's F1 to F9 (posted by 17:16). **DF-12 and group 18's line are in my own generator** (`phase3_ch14_rules_build.py`): run twice, the second changing nothing; strict build from a scratch chapters folder exit 0, 0 warnings, every one of Rules 14.1 to 14.14 printing its Basis line. Waiting on: each owner's "done" for my second read (D3-669), and whoever next runs `phase3_ch14_build.py` to carry my two changes into the chapter file (Requests).
- 17:13 UTC. "Words for the systems designer" posted (main session told).
- 17:11 UTC. "Words for the tracker designer" posted (main session told).
- 17:10 UTC. "Words for the complex examples maker" posted, CE-M1 first, on the data lead's rulings R2 to R5 (main session told).
- 17:00 UTC. Started. Read `CLAUDE.md`, my role file, chapter 02's writing rules, the fix brief, the CE, ST, DF and NB reports, and my round 5 notes. Working tree clean at `8ace3dc6`. The data lead's and research lead's fix pass notes are not posted yet. Next: the current words behind each code, then the "Words for ..." sections, hardest first.

## Words for the complex examples maker

Written at 17:10 UTC, after the data lead's rulings R2 to R5 (posted 17:08); ST-S8's row added at 17:17 on the research lead's F6. "Old" strings are the printed words as `phase3_ch14_complex_build.py` held them at `8ace3dc6`, or the code line where the words are built; match them against your working copy. Every figure and atlas value is the data lead's or the research lead's; I add none. Where a row says "computed", the words come from the generator, never typed, so the build can hold them (R2, item 1).

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

### ST-S8, S96's source line names the release (the research lead's F6)

Revised at 17:22: the research lead's sidecar now carries its own variants (`september_release`, `september_release_margin`, `september_release_sectors_margin`), which set the release with the title, and the main session has called that S14 names the release too. I withdraw my 17:17 draft, which put the release in the qualification, and take the research lead's placement with one change.

- S96's `source_line`, old: "Source: U.S. Bureau of Labor Statistics, Current Employment Statistics, all nonfarm employees, monthly change, seasonally adjusted, January 2022 to September 2026, United States, via FRED, Federal Reserve Bank of St. Louis. Retrieved November 6, 2026. August and September 2026 are preliminary and will be revised. The margin of error is ..."
- New: "Source: U.S. Bureau of Labor Statistics, Current Employment Statistics, all nonfarm employees, monthly change, seasonally adjusted, from the Employment Situation for September 2026, released October 2, 2026, January 2022 to September 2026, United States, via FRED, Federal Reserve Bank of St. Louis. Retrieved November 6, 2026. August and September 2026 are preliminary and will be revised. The margin of error is ..." (with R4b's sector series, the research lead's `september_release_sectors_margin` the same way)
- The one change from the research lead's variants: the qualification keeps the approved words, "August and September 2026 are preliminary and will be revised.", where the variants say "are preliminary, and later releases revise them." Chapter 02's H06, H07 and H08 and chapter 13's Rule 13.6 print the approved words, and Rule 13.6's own build check holds them; the release is the only change S14 and S96 need.

H04 has no part of its own for a vintage, and the release names the publication the figures come from, so it sits with the title, as Rule 13.7 asks ("the release its figures come from"). Fact: F6.

### NB-S1, Rule 14.142's promise

Carried in the `rule[0]` row above: "Name only the changes past it that the reader’s question asks about, here the drops". The title stands ("Mark the survey’s margin on a monthly chart, and name the changes that pass it."), since the rule now says which changes.

### NB-M1, group 18's line

Group 18's line sits in my own generator (`GROUP_LINES[18]` in `phase3_ch14_rules_build.py`), so I change it myself; nothing for you to apply. Old: "...and three reforms that act on one housing loop." New: "...and three reforms whose records name one housing loop." Rule 14.144's own `rule[0]` already says "each reform whose record names one loop".

## Words for the systems designer

Written at 17:13 UTC, after the data lead's R1 and against your "Fixed" list as it stood at 17:11. "Old" strings are the printed words in `phase3_ch15_build.py` as your working copy held them at 17:11; match the joined words. Four rows waited on the research lead's "Facts" (stage 2's majority, stage 7's conference, stage 19's scope, ST-M2's statute row); all four were made final at 17:17 on F1, F3, F4 and F7, and each says so.

**Read and kept as you applied them:** CE-M3 and DF-1 (the two subheads say "stages"), CE-S7 (each chip with the atlas's name), DF-8 (one to nine in words), DF-9 (the card reads Rule 15.22's names, so CE-S3's new name reaches it), ST-S9's attributions, ST-S7's dates, DF-10's reordered source line, CE-S12 ("the seven effect codes, ranks of direction and rough size with no measured amount", computed) and 15.20's why ("the atlas’s own codes, one to each outcome family").

### CE-M4, DF-2 and DF-5, Rule 15.22's marks in words (ruling R1)

The key, one row a mark, as R1 item 4 draws them:

| Key row | Old | New |
|---|---|---|
| `km-st` | A stage every enacted bill passes, in order, on the dark line | A stage every enacted bill passes, in order, numbered on the line in the text’s ink |
| `km-br` | A path a bill can take instead, set to one side on a short arrow, saying where it leaves and where it goes next | A stage only some bills pass, set to one side on a short gray arrow, saying where it leaves the line and where it goes next |
| `km-af` | What can follow the law, on the lighter line | What can follow the law, numbered on the gray line |
| `km-sq` | A path that stops there | Stands; it is now the plate's one square |
| `km-bk` | The line on the left: a repeal is a new act, so it runs back to stage 1 | Stands |

`km-br` drops "instead" because stage 9 now sits there too, and signing is one of the President's outcomes, not a detour.

- The alt, old: "The stages every enacted bill passes sit on a dark line in filled squares; the other paths and what follows the law are in a lighter ink with outlined squares."
- New: "Each stage is a bold number set on its line. The stages every enacted bill passes sit on a line in the text’s ink; the other paths and what follows the law sit on gray lines, and a small square ends a path that stops."
- `rule[0]`, old: "Number every stage in reading order. Set the stages every change on the route passes through on one dark line in filled squares, and the paths that leave it in the lighter context ink with outlined squares, each saying in words where it leaves, as Rule 14.6 sets a diagram’s path."
- New: "Number every stage in reading order, and set each number on its line with no shape around it, since a circle, a ring or a square on a tracker marks a state (Rule 11.2). Set the stages every change on the route passes through on one line in the text’s ink, and the paths that leave it on gray lines, each saying in words where it leaves, as Rule 14.6 sets a diagram’s path."
- The rest of `rule[0]` ("End a path that stops on a small square, as a tracker ends a bill that stops (Rule 11.3), and print beside each stage ...") stands.
- Spec "The spine", old: "The stages every change on the route passes, numbered in reading order, filled squares on a line in Charcoal at the subject weight". New: "The stages every change on the route passes, each a bold number in reading order on a line in the text’s ink at the subject weight". "Charcoal" goes because the line is light on a Charcoal ground.
- Spec "Other paths", old: "Outlined squares in the context ink, set to one side, each saying in words where it leaves the spine". New: "Bold numbers on gray lines at the context weight, set to one side, each saying in words where it leaves the spine".
- The failure plate's alt, old: "Route FS drawn as six filled steps on one line, ..." New: "Route FS drawn as six numbered stages on one line, ..." (R1 item 7; the rest of the alt stands).

### DF-14 with CE-S1 to CE-S4, the stage sentences, actor first

| Stage | Old | New |
|---|---|---|
| 2 | A simple majority: 218 of 435 in the House, or 51 of 100 in the Senate. | The first chamber passes it by a majority of the members who vote, 218 when all 435 House members vote or 51 when all 100 senators do. A tie fails, and in the Senate the Vice President may break it. (Final at 17:17, on F3; cite beside the stage the research lead's new rows for Article I, Section 3 and the Senate's "About Voting".) |
| 3 | Forty minutes of debate, and two-thirds of the members voting, on a Monday, Tuesday or Wednesday. | The House takes the bill up on a Monday, Tuesday or Wednesday, debates it for no more than 40 minutes and passes it with two-thirds of the members voting. |
| 5 | Debate is held to 20 hours, so no cloture vote is needed and a simple majority passes it. A part that does not change spending or revenue is struck when a senator raises a point of order and the chair agrees. | Reconciliation is a budget procedure that lets qualifying tax and spending bills pass the Senate by a simple majority. The law holds debate to 20 hours, so the Senate needs no cloture vote. A senator can object to a part that does not change spending or revenue, and if the presiding officer agrees, that part comes out of the bill. |
| 6 | A simple majority, by the same paths as stage 2. | The second chamber passes it by the same count as stage 2, or by one of the paths at stages 3 to 5. |
| 7 | A conference committee settles the differences, and both chambers approve the same text. | The two chambers pass the same text. Where their versions differ, they settle the differences by amending each other’s text or in a conference committee. (Final at 17:17, on F4, "How Our Laws Are Made", House Document 110-49, parts XV to XVII; cite it beside the stage with the House page.) |
| 8, name | Enrolled and presented | Sent to the President |
| 8, words | The final text is printed and sent to the President, who has 10 days, Sundays excepted, to act. | The Government Publishing Office prints the final text, a step called enrolling, and Congress presents it to the President, who has 10 days, Sundays excepted, to act. |
| 11 | Ten days pass, Sundays excepted, while Congress sits, and it becomes law. | The President lets 10 days pass, Sundays excepted, while Congress is in session, and the bill becomes law. |
| 14 | Money leaves the Treasury only through an appropriation made by law. If the President proposes to cancel some, the money must be released for spending unless Congress passes a rescission bill within the 45-day period the law sets. | Congress funds the law in an appropriation, since money leaves the Treasury only through one made by law. If the President proposes to cancel some of that money, the President must still release it for spending unless Congress passes a rescission bill, which cancels it, within the 45-day period the law sets. |
| 16 | A major rule waits at least 60 days. A joint resolution of disapproval, passed and signed like a bill, ends it. | The agency reports each rule to Congress, and a major rule waits at least 60 days to take effect. Congress can end a rule with a joint resolution of disapproval, passed and signed like a bill. |

Facts behind the rows, all in the workflow sources file as your generator already holds them: stage 3, House Rule XV ("debatable for 40 minutes", "two-thirds of the Members voting", "Mondays, Tuesdays, and Wednesdays"); stage 5, the atlas glossary's "Reconciliation" ("lets qualifying tax and spending legislation pass the Senate by simple majority", chapter 02's H02 asks for the glossary's words where they fit), 2 U.S.C. 641(e)(2) and 644 ("when the Chair sustains a point of order", "deemed stricken"); stage 8, the House page ("prints the revised bill in a process called enrolling") and Article I, Section 7 ("presented to the President", ten days "Sundays excepted"); stage 14, Article I, Section 9 and 2 U.S.C. 683 ("shall be made available for obligation unless, within the prescribed 45-day period"); stage 16, 5 U.S.C. 801(a) ("submit to each House of the Congress", "60 days after") and 802. Stage 8's new name reaches Rule 15.23 ("Stage 8: Sent to the President") and the Route FS card through your readers of the stage row. Stages 1, 4, 9, 10, 12, 13, 15, 17, 18 and 20 already open with their actor or need no change.

### ST-M2 and CE-S8, the records request's 20 working days

The rows under Rule 11.8's steps (your `rows8`). The rows say what each step holds in the law; the generator's `fw("5", ...)` gives way to words per row.

| Row | Old | New |
|---|---|---|
| Step 1, Requested, a new last row | (none) | The agency’s 20 working days to decide start when the right office receives the request, and no later than 10 days after any office the agency names for requests receives it |
| Step 2, Acknowledged | The agency decides, within 20 working days that start here | The agency’s 20 working days to decide, already running |
| Step 3, Searching | The agency decides, inside the same 20 working days | The agency searches for the records, inside the same 20 working days |
| Step 4, Reviewing | The agency decides, inside the same 20 working days | The agency reviews what it found, before the 20 working days run out |
| Step 5, Answered | The agency decides within 20 working days, or 10 more in unusual circumstances | The agency answers within the 20 working days, or 10 more in unusual circumstances |

- The alt, old: "...steps 2 to 5 share the agency’s 20 working days to decide, ..." New: "...the agency’s 20 working days to decide start when the right office receives the request, and steps 2 to 5 share them, ..."
- Fact: the research lead's F1, 5 U.S.C. 552(a)(6)(A), the paragraph after clause (ii) ("shall commence on the date on which the request is first received by the appropriate component of the agency, but in any event not later than ten days after the request is first received by any component of the agency that is designated in the agency's regulations ... to receive requests"). Final at 17:17, with one change F1 asks for: the step 1 row reads "The agency’s 20 working days to decide start when the right office receives the request, and no later than 10 days after any office the agency names for requests receives it"; the alt's clause stays as above. The law says "ten days" there, not working days, so the row says "10 days".

### CE-S9, the rule issued without comment

- The row under "In place of steps 2 to 4", old: "Guidance without comment". New: "A rule issued without advance comment, such as an interim final rule, or guidance, which states how the agency reads the law and takes no comment".
- Facts: Rule 11.9 ("An interim final rule is one such rule"); the FA row "Guidance with no comment period" (5 U.S.C. 553's "interpretative rules"). The data file's step name stays for its check; only the printed words change.

### CE-S10, Rule 15.23's lead line (R1 item 5)

- The paragraph under "Five trackers, each beside its workflow" ends, old: "...and some stages sit before step 1 or after step 6, where the tracker does not follow them."
- Add after it: "Steps keep their trackers’ numbers, and Route FS’s stages keep the word “Stage” and Rule 15.22’s numbers."

### CE-S11, court terms on Rules 15.23 and 15.24

- 15.23, the step 2 row of the court case (`cr[1]`), old: "Motions, discovery, a settlement or a trial, and the judgment". New: "Motions, which ask the judge to rule on a point, and discovery, when each side gathers evidence from the other; then a settlement or a trial, and the judgment".
- 15.23, the row after step 6 (`cr[8]`), old: "A later ruling that replaces earlier doctrine". New: "A later ruling that replaces earlier doctrine, the rules courts build from their rulings".
- "Injunction" stays bare here: Rule 11.11 glosses it at its first use in the guide (the tracker designer's row above).
- 15.24, the court doctrine card's stage (CE-S18), old: "Decision, rehearing or remand". New: "Decision, rehearing or a remand, which sends the case back".

I ask the research lead below to check the three glosses against the federal courts' own glossary.

### ST-S5, NB-S6 and CE-S5, stage 19's example and its rule

- Old: "A court can rule that a law, or a part of it, violates the Constitution. In the Supreme Court’s words of 1803, “a law repugnant to the constitution is void”. The latest such ruling we found came on June 30, 2026, when the Supreme Court held that the limits on what a political party may spend in coordination with its candidates, in 52 U.S.C. 30116(d), violate the First Amendment."
- New: "A court can rule that a law, or a part of it, violates the Constitution, a power the Supreme Court set out in Marbury v. Madison in 1803. The Supreme Court’s most recent decision to hold part of an Act of Congress unconstitutional, in its opinions through November 9, 2026, came on June 30, 2026, when it held that the limits on what a political party may spend in coordination with its candidates, in 52 U.S.C. 30116(d), violate the First Amendment."
- The stop line, "The part the court holds void no longer applies.", stands (the data lead's round 5 ruling). The Marbury citation stays in the source column.
- Final at 17:17, on F7: the Supreme Court only, an Act of Congress only, a holding in the judgment, by date, from the Court's opinion lists read to November 9, 2026; the recheck of November 16 picks the same case, so "through November 9, 2026" stays with the read date the sources file records. NB-S6's point on "repugnant" is met by letting Marbury name the power and the 2026 holding keep its own words.

### NB-M1, Rule 15.20's selection rule (call 3)

- `rule[0]`, first sentence, old: "Offer the reforms that act on one drawing as a named group of radio buttons (Rule 18.3), so a reader chooses one at a time."
- New: "Offer the reforms whose own records name the loop on the drawing as a named group of radio buttons (Rule 18.3), so a reader chooses one at a time."
- `rule[1]`, last sentence, old: "Offer only reforms whose every target sits on the drawing, so nothing lights for a reform that does not act there."
- New: "Where a reform has a target off the drawing, name it in words with its layer, as Rule 14.144 does, and say so when nothing on the drawing turns red."
- Checked by script on the model: Reforms R-03 and R-04 each name Loop R4a in their own records (R-03: R4a, R10, R12; R-04: R4a), so 15.20's own plate keeps its rule; R-06, R-30 and R-38 each name Loop R8 (Loop R8's record lists R-30 alone, which is why the rule says "their own records"). The failure plate and its spec keep their faults, as NB-M1 says.

### CE-S23, three small words

- 15.16, your draft gloss, old: "...then print its effects one outcome family to a row, an outcome family being one of the four groups of results the atlas judges reforms by. Give each row ..."
- New: "...then print its effects one outcome family to a row. An outcome family is one of the four groups of results the atlas judges reforms by. Give each row ..."
- 15.21's failure alt, last sentence, old: "It is a picture, not a control." New: "It is a still picture, with nothing to move." (W09, the same turn the spec lost.)
- 15.21's spec ("A drawing of the control, with its alt saying it is a picture") and the read-aloud "fewer" stand as you applied them.

### DF-10, the version date on a law (words; the choice of one word across chapters is a request below)

For a statute or a rule cited beside a stage or on a card, print the version with the date read, in chapter 11's form: "Source: 2 U.S.C. 641, as in force on November 14, 2026, read November 14, 2026" is long twenty times over, so where the two dates are one day, print "Source: 2 U.S.C. 641, as in force on November 14, 2026, the day we read it". A page that is not a law keeps "read" and its date: "Source: U.S. House, “The Legislative Process”, read November 11, 2026".

## Words for the tracker designer

Written at 17:11 UTC. "Old" strings are the printed words in `apply_systems_ch11.py` (the generator splits them across lines; match the joined words) as your working copy held them at 17:10. Three rows waited on the research lead's "Facts" (CE-S17, NB-S7's reason, ST-S3's figure); all three were made final at 17:17 on F9, F8 and F2, and each says so. Your CE-S20 and CE-S18 text gets my second read once you report done.

### CE-S11, "injunction" glossed where chapter 11 first uses it

- Rule 11.11 `rule[0]`, old: "...as when a district court of three judges grants or denies an injunction and the law sends the appeal straight to the Supreme Court."
- New: "...as when a district court of three judges grants or denies an injunction, a court order to do or to stop doing something, and the law sends the appeal straight to the Supreme Court."

Rule 11.12 and the specs then use the word bare, as they do now.

### CE-S15, "certify" as one verb

- `BALLOT_STEPS`, step 2's words (line 115), old: "The attorney general clears the measure and writes the title and summary that petitions and ballots carry."
- New: "The attorney general writes the title and summary that petitions and ballots carry, and where the law asks, first certifies that the measure is in proper form and on a subject the initiative may cover."
- Rule 11.10 `rule[1]`, first sentence, old: "Until the state certifies the count, a measure at step 6 stays current, and its words say so: ..."
- New: "Until the state certifies the count, which makes the result official, a measure at step 6 stays current, and its words say so: ..."

Facts: the workflow sources file, row "2 Title and summary" (Massachusetts's attorney general certifies "proper form" and "only subjects not excluded from the popular initiative"; California's prepares the title and summary). "Where the law asks" keeps California true. Steps 5 and 6 keep "certifies": with the gloss and the actor named each time ("the attorney general", "the state’s election officer", "the state"), one verb now means one act, done by three offices.

### CE-S16 and NB-S7, the kinds of measure and why these four states

- Rule 11.10 `rule[0]`, old: "A ballot measure here is a citizen initiative: voters propose a law or an amendment to their state’s constitution by petition, and the voters decide it. These steps follow the constitutions of Massachusetts, California, Ohio and Michigan, with California’s election office, and each state sets its own deadlines and signature counts. The tracker uses the bill tracker’s marks for six steps of its own: Filed, Title and summary, Signatures, Legislature, On the ballot and Vote. Step 4 counts only where the Legislature votes on the measure first, so a measure that goes straight to the ballot keeps step 4 under a slash. The same steps carry a measure the Legislature sends to the voters itself, which has no petition, so steps 1 to 3 keep their slashes."
- New: "A ballot measure here is a law or an amendment to a state’s constitution that the voters decide. It starts as a citizen initiative, which voters propose by petition, or as a legislative referral, which the Legislature sends to the voters itself. An initiative is indirect where the Legislature votes on it first and direct where it goes straight to the ballot. These steps follow the constitutions of Massachusetts, Ohio and Michigan, where the Legislature votes first on a proposed law, and California’s constitution and election office, where an initiative goes straight to the ballot; each state sets its own deadlines and signature counts. The tracker uses the bill tracker’s marks for six steps of its own: Filed, Title and summary, Signatures, Legislature, On the ballot and Vote. Step 4 counts only for an indirect initiative, so a direct one keeps step 4 under a slash, and a referral, which has no petition, keeps steps 1 to 3 under slashes."
- The ballot step table's caption (`s_route_steps`, line 1385), old: "The six steps of a state ballot measure, a citizen initiative, with what happens at each and where the law sets it in the four states we read."
- New: "The six steps of a state ballot measure, with what happens at each and where the law sets it in four states: Massachusetts, Ohio and Michigan, where the Legislature votes first on a proposed law, and California, where an initiative goes straight to the ballot."

Facts: the sources file's BI rows 4 (indirect: Massachusetts, Ohio, Michigan; direct: California, Elections Code 9007) and the four states' frame the nonpartisan reader quotes from the round 5 research notes. Confirmed at 17:17 by the research lead's F8, which also asks the clause to keep "for a law": "on a proposed law" does, since Ohio and Michigan put constitutional amendments straight on the ballot too.

### CE-S17, a measure the Legislature passes (final at 17:17, on the research lead's F9)

- Rule 11.10 `rule[1]`, last sentence, old: "A measure the Legislature passes keeps steps 5 and 6 under slashes, and its words give the date: “Passed by the Legislature on May 2.”"
- New: "A measure the Legislature passes keeps steps 5 and 6 under slashes, and its words give the date and what comes next. In Massachusetts and Ohio it goes to the governor, as a bill does, and in Michigan it becomes law without one: “Passed by the Legislature on May 2. It goes to the governor.”"
- Spec "Passed by the Legislature", old: "Steps 5 and 6 under slashes, and “Passed by the Legislature on” with its date"
- New: "Steps 5 and 6 under slashes, then “Passed by the Legislature on” with its date and what comes next: “It goes to the governor.”, or “It becomes law without the governor.” where the governor takes no part, as in Michigan"

Facts: F9 (Ohio, Article II, Sections 1b and 16; Michigan, Article II, Section 9, and the House Fiscal Agency's analysis; Massachusetts by the research lead's reading of Part the Second, Chapter I, Section I, Article II). The cards name no state, so a card that ends this way takes one of the two endings and never a state's name. California is left out of the sentence because its initiatives never go to the Legislature (the step table's direct initiative).

### CE-S19, every "Affirmed" says what stands

- Rule 11.11 `rule[1]`, after "...when it returns the case.", add: "Every ending that leaves a ruling in place says so in one sentence: “The lower court’s ruling stands.” after Affirmed or a tie, and “The appeals court’s ruling stands.” after a denied petition."
- Spec "A higher court’s ruling", old: "Affirmed; Reversed; Vacated; Modified; each with the court, as in “Affirmed by the appeals court”, and “and sent back” where the court returns the case"
- New: "Affirmed, then “The lower court’s ruling stands.”; Reversed; Vacated; Modified; each with the court, as in “Affirmed by the appeals court”, and “and sent back” where the court returns the case"

The tie's spec ("Affirmed by an equally divided Court, which is a tie vote, and “The lower court’s ruling stands.”") and Measure 99016's "The appeals court’s ruling stands." already match. The failure plate's "Affirmed by the Supreme Court on January 11." stays: it is the fault.

### CE-S21, the measure most voters approved

- Rule 11.10 spec "The end, in words", old: "...; Not approved by voters where most said yes but a second test failed, with a sentence that names it"
- New: "...; Fell short of the vote the law requires, where most said yes but a second test failed, with a sentence that names the test"

No plate prints it today. The sentence after it, where a card needs one, follows my round 5 row: "Most voters said yes, but the law also needs yes votes equal to 30 percent of all ballots cast." (Massachusetts's Amendment Article LXXXI, the sources file's row "6 Vote, certification and effect"; the cards name no state, so "the law".)

### ST-S3, the sample that stopped Measure 99013

- `BALLOTS`, Measure 99013's `line` (line 259), old: "On July 14, a random sample of the signatures projected fewer valid ones than the law requires."
- New: "On July 14, a random sample of the signatures projected fewer than 95 percent of the valid signatures the law requires, so election officials did not go on to check every signature."

Facts: the research lead's F2 (California's guide, Elections Code 9030(f) and 9031(a): projected under 95 percent, the measure "fails to qualify for the ballot"; 95 to 110 percent, county officials "verify every signature"). "Election officials" is the step table's own actor for step 3. Confirmed at 17:17.

## S14's release and chapter 13 (the main session's question, 17:22)

The main session has called that S14 names the payroll release in its source line, as S96 will. Where else the guide prints S14's line, by search of the chapter files, entries, specimens and generators:

| Where | How it gets the line | Approved | Should it follow? |
|---|---|---|---|
| Rule 13.6's correct plate (`s-13-6-correct`), the line under its jobs head and the table under it, "The same line, part by part, in H04’s order" | `phase3_ch13_build.py`, `rule_13_6`: the line from the payroll sidecar's `printed_source_line`; the table's seven rows typed in the generator, each held in order against the line by a build check | Chapter 13, DR-237 | **Yes.** Rule 13.7, the next rule on the same page, says that where a publisher revises its figures "the chart also names the vintage, the release its figures come from". The payroll series is revised, so once S14's line names the release, chapter 13's own example of a source line would break its neighbor rule if it did not. |
| Chapter 13's sources list | The same line, as the chapter's source for that plate | DR-237 | Yes, with the plate, so the two agree. |
| Chapter 02, H06, H07 and H08 (`s-02-22-correct` and the chapter file) | The same line, quoted under each example | Board 5, DR-73; DR-239 for H08's sentence | Yes, so one chart prints one line across the guide; but chapter 02 is approved, so board 3 shows it beside chapter 13's change. |
| Chapters 05 and 06 (`s-05-5`, `s-06-5`) | The sector file's line ("all employees by industry"), a different chart | Gate 2 | Not under this call, which names S14. The same reason reaches them, since that file has the same vintage (F6); I suggest board 3 asks it once for all three. |

**The words, if chapter 13 follows** (for the owner of `phase3_ch13_build.py`, through the main session):

- The line is the sidecar's `printed_source_line`, so it follows when the research lead sets that key to the release line. With the qualification kept as approved (my ST-S8 row), the plate's line reads: "Source: U.S. Bureau of Labor Statistics, Current Employment Statistics, all nonfarm employees, monthly change, seasonally adjusted, from the Employment Situation for September 2026, released October 2, 2026, January 2022 to September 2026, United States, via FRED, Federal Reserve Bank of St. Louis. Retrieved November 6, 2026. August and September 2026 are preliminary and will be revised."
- The table's "Title or table" row, old: "Current Employment Statistics, all nonfarm employees, monthly change, seasonally adjusted". New: "Current Employment Statistics, all nonfarm employees, monthly change, seasonally adjusted, from the Employment Situation for September 2026, released October 2, 2026". Without it, the release's words sit in the line and in no row of the table that takes the line apart, and the build check, which only looks for each row's words in order, would not notice.
- The other six rows stand. If the qualification changes to the research lead's "are preliminary, and later releases revise them.", the "Qualification" row changes to match, or the build check stops the chapter, which is the check doing its job.
- Chapter 02's three quoted lines take the same words as the plate.

This touches approved chapters 02 and 13, so I write none of it. It is the main session's to put on board 3 with DR-278's carried items, or to rule out.

## Fixed

| Code | What changed | File | Proof |
|---|---|---|---|
| DF-12 | Each of Rules 14.1 to 14.12 and 14.14 now carries its own Basis line naming its standard or approval, as every rule in chapters 01 onward prints one; Rule 14.13 keeps its own. The chapter's basis still prints once after the intro for the 127 form entries (D3-556). A new check stops the build if a rule's basis repeats the chapter's, since `phase3_ch14_build.py` would drop it and the rule would print none. The lines: 14.1 "Design judgment, from the coverage plan our founder and editor approved in November 2026" (DR-62); 14.2 "Rules 13.1, 13.2, 13.6 and 13.7, and chapter 02, house rule H08; the order of the parts is design judgment"; 14.3 "Rule 12.6, and WCAG 2.2, success criterion 1.4.1, Use of Color"; 14.4 "Design judgment, from the chart system our founder and editor approved in November 2026, whose bars always start at zero" (DR-52; the Explainer board's "Bars always start here"); 14.5 "Design judgment, with the data palettes and the group order our founder and editor approved in November 2026" (DR-54, DR-234, DR-236); 14.6 "Rules 05.1, 05.3, 05.5 and 05.7; the mark the title names is design judgment"; 14.7 "Rules 01.1 and 01.2, and chapter 02, house rule H10"; 14.8 "Design judgment, approved by our founder and editor in November 2026" (DR-234, in D2-412's form); 14.9 "Rule 13.5, and design judgment, approved by our founder and editor in November 2026" (DR-64); 14.10 "Chapter 02, house rule H09, and Rule 13.7"; 14.11 "Rule 13.7, and design judgment"; 14.12 "Rule 06.3, and design judgment, approved by our founder and editor in November 2026" (DR-64); 14.14 "Design judgment, with the chart kit our founder and editor approved in November 2026; Rule 18.14" (DR-235) | `phase3_ch14_rules_build.py` (`RULE_BASIS`, `entry`); outputs `14-001.json` to `14-012.json` and `14-014.json` | Baseline run first: no output changed. After the edit, run twice: the second run changed nothing (hashes). Scratch proof: the bases carried into a copy of the chapter file by `carry_basis.py` exactly as `phase3_ch14_build.py` carries them (a basis that repeats the chapter's is dropped), strict build `guide.html` exit 0, 0 warnings, and a script reads one Basis line under each of Rules 14.1 to 14.14 and one chapter box |
| NB-M1, group 18's line (call 3) | "...and three reforms that act on one housing loop." becomes "...and three reforms whose records name one housing loop." | `phase3_ch14_rules_build.py` (`GROUP_LINES[18]`); output `14-chapter.json` | The same two runs; the scratch build prints the new line once and the old words nowhere |
| DF-13, Rule 14.6's part (routed at 17:20) | The ink words a reader meets in my rules, defined at first use or said in the reader's word. Rule 14.5: "Inside any of them, Rule 05.7 sets three roles: the subject, the series the title names, in the text’s ink; the context, every other series, in gray; and the one red point." Rule 14.6, `rule[0]`: "...inside Rule 05.5’s keyline, a 1 px edge around the red, and with its own label. Every other series takes the context ink, the gray Rule 05.7 gives each series the title does not name. Where the title names one bar, every other bar takes the light fill on Newsprint, a paler gray, so the named bar still stands apart in gray print, and keeps the context ink on Charcoal." (was "every other mark takes the light fill on Newsprint and the context ink on Charcoal (Rule 05.7)", which Rule 05.7's "every other series takes Stone" contradicted for lines; the light fill token's own description limits it to "every other bar wherever a chart names one bar"). Rule 14.6, `rule[2]`: "Charcoal at the subject weight, the 3 px line of the series a title names". Specs: 14.6's "Its label" says "in the text’s ink" (was "the text ink"), and 14.3's "A line" says "in the text’s ink" (was "the label ink"; its token is the text's own color) | `phase3_ch14_rules_build.py`; outputs `14-003.json`, `14-005.json`, `14-006.json` | Run twice, the second changing nothing (hashes). Scratch: the five changed fields and DF-12's bases carried into a copy of the chapter file by `carry_rules.py` as `phase3_ch14_build.py` carries them; strict build `guide2.html` exit 0, 0 warnings; each new phrase found once on the page; one Basis line under each of Rules 14.1 to 14.14 |
| CE-M1, ST-M1, ST-S1, CE-S13, ST-S2, ST-S8, DF-3, DF-4, DF-7, CE-S14, NB-S1 | Words, for the complex examples maker to apply | My notes, "Words for the complex examples maker" | The maker reported them applied at 17:14 (its notes); my second read waits for its "done" |
| CE-M4, DF-1, DF-2, DF-5, DF-10, DF-14, CE-M3, CE-S1 to CE-S5, CE-S8 to CE-S11, CE-S23, ST-M2, ST-S5, ST-S6, NB-M1, NB-S6 | Words, for the systems designer to apply | My notes, "Words for the systems designer" | Second read waits for its "done" |
| CE-S11, CE-S15 to CE-S17, CE-S19, CE-S21, ST-S3, NB-S7 | Words, for the tracker designer to apply | My notes, "Words for the tracker designer" | Second read waits for its "done"; CE-S18 and CE-S20 are its own words, which I read then too |

## Not fixed

| Code | Reason |
|---|---|
| DF-13, the palette plate's list of role inks | The engineer's (the main session's routing at 17:20). "Subject ink" still prints bare in Rule 14.46 and later entries that are not mine; Rule 14.5's roles and Rule 14.6's definitions now come first in reading order, before the palette plate after Rule 14.5 would name them by token. "Charcoal at the subject weight" in Rule 14.6 is true on Newsprint, the chart ground, and names a color that is light on a Charcoal ground; I left the color word, since the rule names both grounds where it matters, and list it for board 3 beside DF-5's ink words |
| NB-M2, entry 14.141 | Not in my routed codes and not my file. The words, if its owner wants them: add "and the lockmark’s sign-off at 96 px (Rule 08.2)" to the list of what a card holds, as NB-M2 drafts it |

## Calls

| call | reason |
|---|---|
| Rules 14.1 to 14.12 and 14.14 each print a Basis line that names the rule's own standard or approval, and the chapter's basis keeps printing once for the form entries | DF-12: every rule in chapters 01 onward prints one, and a rule's own line tells a reader what it rests on; D3-556's one box still serves the 127 entries |
| Rule 14.6's light fill covers every other bar where the title names one bar, and every other series takes the context ink | DF-13: Rule 05.7 says every other series takes Stone, and the light fill token itself limits the fill to the other bars of a chart that names one bar |
| S96's source line sets the release with the title and keeps the approved qualification words | F6, Rule 13.7's "the release its figures come from", and the research lead's variants; the approved "are preliminary and will be revised" stays because chapters 02 and 13 print it and Rule 13.6's check holds it |
| Group 18's line says the three reforms' records name the housing loop | Call 3 and NB-M1: Reform R-38 has no target on Loop R8, so "act on" said more than the plate shows; Rule 14.144's own text already says "whose record names one loop" |
| The chart notes on S96 say "the text’s ink", and I withdraw my round 5 reason for "the strongest ink" | D3-914 and DR-262 set one ink word, and S53, which I cited in round 5, had moved to "the text’s ink" by D3-1043 |
| Rule 14.143's lines say each change in the walk's direction, cause first, with "goes up" and "goes down" after the title that asks how often | Ruling R2; "how often the primary decides the winner rises" stops the ear |
| Rule 15.22's stage 8 is named "Sent to the President", with "enrolling" kept inside its sentence | CE-S3: Rule 11.1's failure caption rules out "Enrolled" as a clerk's word |
| Stage 19 lets Marbury name the power, and the 2026 holding keeps its own words, with the selection rule stated | NB-S6 and ST-S5, on the research lead's F7 |
| A ballot measure the Legislature passes says what comes next, by state, in Rule 11.10's text, and a card takes one of two endings without naming a state | CE-S17 on F9: Massachusetts and Ohio send it to the governor, Michigan does not; the cards name no state (DR-275) |

## Requests

- **To the main session.** My two changes (DF-12 and group 18's line) are in the entries and `14-chapter.json` but not yet in `work/build/guide/chapters/14-data-visualization.json`, which `phase3_ch14_build.py` writes. I have not run it, so I write no file outside my row while other owners' chapter 14 work is in flight. The main session runs the whole chain once at the join (its word at 17:20), which carries them; `phase3_ch14_build.py --check` reports the chapter file and its manifest as not what it writes until then, which is expected. The same holds for DF-13's words.
- **To the main session, DF-10's one word.** The drift reader asks for one of "read" and "retrieved" across chapters 11, 14 and 15. Chapter 02's H04 says "the date retrieved", and chapters 11 and 14 use "retrieved"; chapter 15's route pages use "read", with S71 on board 2 as precedent. Changing either reaches approved work, so I suggest board 3 shows it. Inside this pass my words for the systems designer add "as in force on" to each law on Rules 15.22 to 15.24 and keep chapter 15's "read".
- **To the research lead.** Please check three glosses I wrote for the systems designer against the federal courts' own glossary (uscourts.gov): "motions, which ask the judge to rule on a point", "discovery, when each side gathers evidence from the other" and "doctrine, the rules courts build from their rulings"; and "an injunction, a court order to do or to stop doing something" for the tracker designer. If any reads otherwise, I change it.
- **To the systems designer.** Stages 2 and 7 now rest on new sources (F3's Article I, Section 3 and the Senate's "About Voting"; F4's "How Our Laws Are Made"); please cite them beside the stages, from the research lead's new rows.

## Tested

- Read whole: `CLAUDE.md`, my role file, chapter 02's writing rules, the fix brief, the CE, ST, DF and NB reports, my round 5 notes, the data lead's rulings R1 to R5 and the research lead's facts F1 to F9.
- Every "old" string in my three sections read from the owner's generator or its output at the time named in each section's head (by `grep` and `sed` on the files, and by dumping the plates' words with a script for Rule 14.143's seven steps).
- Atlas values by script on `work/extract/atlas-v7-data.json`: the glossary's "Reconciliation", "Effect code", "Outcome family", "Cloture" and others; the loops each reform's record names (R-03: R4a, R10, R12; R-04: R4a; R-06, R-30, R-38: R8) and Loop R8's own list (R-30).
- The decision log by search: D2-412, D3-556, D3-914, D3-994, D3-1043, D3-1992, DR-52, DR-54, DR-62, DR-64, DR-234 to DR-240, DR-262; the approved Explainer board's words on bars and keys, by search.
- `phase3_ch14_rules_build.py`: baseline run (no output changed); after the edits, two runs, the second changing nothing (`md5sum` of `14-001.json` to `14-019.json` and `14-chapter.json` before and after).
- Strict build of the committed chapter files to scratch (`guide-base.html`): exit 0, 12,118,300 bytes. Strict build with my two changes carried into a scratch copy of the chapter file (`--chapters`, `guide.html`): exit 0, 0 warnings; one Basis line under each of Rules 14.1 to 14.14, one chapter box, group 18's new line once and its old words nowhere (script).
- `phase3_ch14_build.py --check`, read only: 97 of 99 files current, the two not current being the chapter file and its manifest.
- DF-13 (17:21): my generator run twice after the edits, the second changing nothing; `carry_rules.py` carried Rules 14.1 to 14.14's text, specs and why into a scratch copy of the chapter file (two rules' text, two rules' specs and 13 whys changed, as expected); strict build `guide2.html` exit 0, 0 warnings, each of the five new phrases found once and a Basis line under each of the 14 rules.
- S14's line: searched the chapter files, entries, specimens, specs, data sidecars and generators for its qualification sentence; read `phase3_ch13_build.py`'s `rule_13_6`, the payroll sidecar's `printed_source_line` and its new variants, and Rules 13.6 and 13.7 in chapter 13's file.
- `git status` after my builds: only my entries and `14-chapter.json` changed, and `plate-share.json`'s timestamp, which I restored by the one allowed checkout (its diff was the timestamp alone).

## Not tested

- A full build with my changes in the real chapter file: `phase3_ch14_build.py` was not run by me (Requests). The scratch build used `--chapters`, which turns off the embedded fonts and the "Where to start" page, so its bytes (11,749,628) are not the page's; the content of chapter 14 is what the real build will carry.
- No browser opened, no capture looked at. Every word above was read as source text, not as a rendered page.
- My second read of each owner's applied words: waits for each owner's "done".
- The pattern script over my three sections and over the owners' applied words: to run in the second read, on the words as applied.
