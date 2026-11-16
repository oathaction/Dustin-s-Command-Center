# Review of rounds 4 and 5: reader panel, simulated (RP)

Oath & Action Edition 06, Phase 3, chat 7, November 16, 2026. Written by the reader panel agent for the main session, under the review brief `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md` ("Reader panel, simulated").

**Every reader on this page is simulated.** Dustin struck real reader tests before launch (DR-202). No real person read this work. Each reader below is a profile written by one agent, and each reader's words are that agent's prediction of how such a person would read. Treat them as hypotheses to check with real readers in a later phase, never as findings from people.

Status: in progress. Started 16:35 UTC (read by `date -u`).

**Score: 3 of 5.** The simulated readers took the main lesson from all but one of the seventy readings (R1 gave up on 15.24 after two cards), but two plates teach a reader something false (RP-1, RP-2), and the front door never leads a reader to round 5's three full charts or chapter 15's workflows (RP-3).

**Counts:** 2 Must fix, 18 Should fix.

**What readers stumbled on most:** words the plates use without a gloss ("band" in two senses, "90 percent", "slash", "Illustrative", the delay ticks); the way from "Choose a chart" to the work they needed; and chapter 15's longest plates, which lost the phone reader and, by ear, repeat themselves.

## How the panel ran

- Build read: the strict build of `9a6e1182` at `scratchpad/c07/main/guide.html`, never read whole. Page text came from a script (`scratchpad/c07/review/reader-panel/scripts/extract.py`) that pulls each rule and plate by its anchor.
- Pictures: the shared capture set (`scratchpad/c07/captures/`), as `index.json` listed them while the capture run went on.
- Each reader read the selection guide "Choose a chart", Rules 14.142, 14.143, 14.144, 15.22, 15.23, 15.24, 11.10 and 11.11, and one round 4 form chosen to fit that reader.
- Seven readers: the two fairness readers count as two.

## Reader profiles, written before they read

Each profile is invented for this panel. None is a real person.

| # | Simulated reader | Profile | Screen | Round 4 form |
|---|---|---|---|---|
| R1 | Newcomer on a phone | Thirty-one, works shifts at a distribution warehouse, votes in presidential years. Knows the Supreme Court and Congress exist; has never met "cloture", "remand" or "interval". Reads on a phone between tasks, thumbs down the page, quits a table wider than the screen. | 390 and 320 px, Newsprint and Charcoal | 14.138, S92 step-by-step |
| R2 | High school civics teacher | Teaches eleventh-grade U.S. Government in a public school, fourteenth year. Plans a 50-minute lesson on how a law is made, struck down and challenged, and wants one plate to project and one to print. Knows the process well and catches a wrong legal term at once. | 1440 px on a laptop and a classroom projector; grayscale print | 14.135, S89 process explainer |
| R3 | Local reporter on deadline | Covers county government for a small daily. Has 90 minutes to file a monthly jobs chart for tonight's paper. Uses a web chart tool, knows "margin of error" loosely, has never read a style guide past its color page. | 1440 and 1024 px | 14.79, S85 icon array |
| R4 | Partner staffer, one chart a month | Communications associate at a partner nonprofit. Makes one chart a month for a newsletter and social posts in a design app. Not a statistician; afraid of getting the brand wrong; wants to be told which chart and which colors. | 1024 and 768 px, then 390 px to check the post | 14.141, S95 social data card |
| R5L | Reader who leans left | Retired public school librarian, volunteers with a voter registration group, gives to Democratic candidates. Reads for whether the guide's examples and words favor one side. Knows campaign finance cases by name. | 1440 px | 14.137, S91 comparison cards |
| R5R | Reader who leans right | Owns a small machine shop, votes in Republican primaries, serves on the county planning board. Reads for whether the jobs chart or the reform examples quietly argue against the party in power or for one side's reforms. | 1440 px and 390 px | 14.136, S90 by-the-numbers panel |
| R6 | Screen reader user | Blind from birth, a benefits counselor, uses a screen reader with Chrome every working day and moves by headings, tables and links. Simulated from the page's accessibility text (see "How R6 was simulated"), never from a real screen reader. | No picture; text only | 14.81, S87 Venn diagram |

## The readers, in their own simulated words

Every quoted line below is a simulated reader's words, written by the panel agent from that reader's profile and the page text and pictures listed. No real person said any of it. The panel's own conclusions sit apart, under "What the panel concludes".

### R1, newcomer to civics on a phone (simulated)

Read at 390 px from the Newsprint 1x captures (the plates land 350 px wide in the phone's column) and the page text. The 320 px and Charcoal captures had not landed when this reader read; see "Captures read".

| Plate | What it taught (simulated) | What confused (simulated) | The word that stopped them |
|---|---|---|---|
| "Choose a chart" | "Every kind of chart has a little picture, so I can match my question to a picture without knowing the name." | "It went on and on, two pictures a row; I thumbed for a long time. 'Marimekko', 'Beeswarm' and 'Alluvial' mean nothing to me; the pictures did the work." | "density" |
| 14.142, S96 | "Most of the months with fewer jobs could be the survey being off. Two drops were big enough to count, and the chart says so under it in words." | "The words 'Margin of error' sit under the zero line, so at first I took the gray strip for where the losses go. And what does '90 percent' mean?" | "90 percent" |
| 14.143 | "Things go in circles: if services get worse, officials are likelier to lose, and the ones who replace them may do better." | "'The quality of public services lowers the risk of losing office' read backward to me. The status line's 'suppose it falls' is what made it click." | "balancing" |
| 14.144 | "A plan can help one thing and do nothing for another, and you should not add them up." | "On the phone the three cards stack, so I scrolled up and down to compare them. '+L local' and 'renter-owner' look like codes." | "qualifier" |
| 15.22 | "A law can be undone after it passes: by money, by a court, by a date written into it, by a later law." | "Cloture, reconciliation, rescission, point of order, joint resolution of disapproval, all in one drawing. Stage 10's last lines broke into narrow columns: 'Short', 'of', 'two-thirds', 'in either chamber, the bill dies' stacked side by side." | "rescission" |
| 15.23 | "The tracker's six steps are a short version of a longer list in the law." | "'So step 4 keeps its slash.' What slash?" | "slash" |
| 15.24 | "There are many ways to change things: a city council, a ballot, Congress, a court." | "Gave up after the second card. It never told me what 'Not checked' means for me." | "feasibility" |
| 11.10 | "Election night numbers are not final until the state certifies them, and the date it will is printed." | "Is Measure 99010 real? The tag says 'Illustrative' and I did not know that means made up." | "Illustrative" |
| 11.11 | "If the Supreme Court will not hear a case, the lower court's ruling stands." | "'Reversed and sent back', yet every circle is filled. I thought filled meant over." | "Reversed" |
| 14.138, S92 step-by-step | "I can ask a federal agency for records. The first two hours of searching and 100 pages are free, and it has 20 working days to answer." | "I opened the table: 'Go to court', 'Every request'. Do I have to sue?" | "expedited" |

Summary in the reader's words (simulated): "The trackers and the records steps I could use tonight. The long drawings lost me halfway. Cloture was explained right where I met it; rescission, Illustrative and 90 percent were not."

### R2, high school civics teacher (simulated)

Read at 1440 px from the Newsprint 1x captures and the page text, as if projecting it, with the grayscale captures for a printed handout where they had landed.

| Plate | What it taught (simulated) | What confused (simulated) | The word that stopped them |
|---|---|---|---|
| "Choose a chart" | "Sixteen questions a student could ask out loud. 'Avoid' with the cross through the radar chart is clear on a projector." | "I want 'how a bill becomes law'. Three questions sound right: 'Behavior: how do people move through a process?', 'Structure: who decides, and how does it work?' and 'Infographics: how does it work, in one look?'. None of them sends me to chapter 15's federal statute drawing." | "Extended" |
| 14.142, S96 | "A margin of error drawn as a band around zero, and five of seven drops that the survey cannot tell from no change. That is a whole statistics lesson." | "'The span both jobs charts share.' Which other chart? I see one." | "both" |
| 14.143, Loops B4 and R10 | "A loop is a chain that comes back to its start, and one minus sign makes it balancing, two make it reinforcing." | "Step 3 is graded 'well supported', and the next sentence calls it 'the weakest step for U.S. services, since its main study covers Brazilian mayors'. Which do I tell students? And nothing on the drawing says what the dashed line or the little crossbars mean." | "weakest" |
| 14.144, three reforms | "Never add effects across families; a word like 'local' after a code changes what it means." | "Why is an election-timing reform, R-06, on a housing loop? The card says it targets owners' opposition to building but never says how. Then 'Band, the kind of change: Rules', when 14.142 just taught me a band is a margin of error." | "Band" |
| 15.22, Route FS | "The whole life of a law past the signature: the money, the agency's rules, Congress striking a rule, the courts, a sunset and repeal. This is the slide I have wanted for years." | "Stage 2 says a simple majority is '218 of 435'. I spend a class un-teaching that: it is a majority of those voting, with a quorum present, and this guide's own chapter 14 counts two empty House seats. Stage 7 names only a conference committee; most bills now settle differences by trading amendments. On the projector, stage 10 reads 'Short of', then a gap, 'two-thirds', a gap, 'in either chamber, the bill dies' in three columns." | "218" |
| 15.23, steps beside stages | "A tracker's step and a law's stage are different things, and three of the bill tracker's steps sit inside stage 1." | "Why does one court case sit on two routes, 'Route ENF and Route CRT'?" | "doctrine" |
| 15.24, eleven routes | "Eleven ways a reform can travel, with the atlas's feasibility words quoted and reconciliation as the 51-vote path." | "Why is 'Taxing inherited gains and capital income' the one reform read through? A student will ask whose side that is. And 113 entries 'Not checked': can I trust the atlas?" | "Not checked" |
| 11.10, ballot measure | "A count is unofficial until the state certifies it, and a direct initiative skips the legislature, shown by the slash." | "The specifications mention 'Not approved by voters where most said yes but a second test failed'. The rule never says what a second test is." | "slash" |
| 11.11, court case | "A denied petition is not a ruling; a tie leaves the lower court's ruling in place; the marks never move backward." | "My students hear 'cert denied' on the news. The guide never says 'certiorari', so they cannot connect the two." | "Vacated" |
| 14.135, S89 process explainer | "Who asks at each step: the governor within 30 days, FEMA reviews, the President declares. Columns by level of government read well." | "FEMA is never spelled out." | "FEMA" |

Summary in the reader's words (simulated): "Chapter 15's route drawings are the best civics teaching material in the guide. I would project 15.22 tomorrow if stage 2 and stage 7 were right."

### R3, local reporter on deadline (simulated)

Read at 1440 px from the Newsprint 1x captures and the page text. The 1024 px captures had not landed when this reader read.

| Plate | What it taught (simulated) | What confused (simulated) | The word that stopped them |
|---|---|---|---|
| "Choose a chart" | "Monthly jobs, change over time: 'Columns with a moving average', Core. Found it in ten seconds." | "That link goes to Rule 14.32, which never mentions the margin band. I only found 14.142 by scrolling to the chapter's end. 'Uncertainty and estimates' offers a band on a line, not on columns." | "Reference" |
| 14.142, S96 | "Do not call a month of minus 20,000 a loss: it sits inside plus or minus 122,000. Name only the two drops past it, and still say seven months fell." | "Where do I get the margin for a state's jobs numbers? And the table says 'Final' for July 2026 while a note says a yearly revision can move earlier months." | "subject ink" |
| 14.143 | "Not for my deadline, but: do not add the minus signs of two loops together." | "Every step carries a code like 'Connection L23'." | "Connection" |
| 14.144 | "No total score. Good rule for any 'which plan is best' graphic." | "Three ticks on each line of the loop, and no words for them anywhere." | "qualifier" |
| 15.22 | "What happens after a bill is signed. Useful for any story that ends at 'signed into law'." | "'The latest such ruling we found.' Found how? I would want the search." | "repugnant" |
| 15.23 | "A tracker stops at step 6 while the law goes on." | "Skimmed; too much for a deadline." | "stage" |
| 15.24 | "'Read' for when we read the law, 'Checked' for when the atlas checked an entry: a good habit for a reporter." | "Why are 113 of 126 entries 'Not checked'?" | "feasibility" |
| 11.10 | "Election night: the count is unofficial until certified, with the certification date. That is my paper's style already." | "What do I write when most voters said yes and the measure still failed?" | "certified" |
| 11.11 | "A denied petition leaves the appeals court's ruling standing. I have written that wrong before." | "Nothing." | "appellant" |
| 14.79, S85 icon array | "One in ten as a grid of 100. Fast to read." | "'Worker bargaining power' and a 'Variable A2' tag sit above the grid like a second headline, and my chart is about union membership." | "Variable A2" |

Summary in the reader's words (simulated): "14.142 would change how I write jobs stories. I nearly missed it, because the chart picker sent me somewhere else."

### R4, partner staffer who makes one chart a month (simulated)

Read at 1440 px from the Newsprint 1x captures and the page text, then at 390 px where captures had landed. The 1024 and 768 px captures had not landed when this reader read.

| Plate | What it taught (simulated) | What confused (simulated) | The word that stopped them |
|---|---|---|---|
| "Choose a chart" | "I can find my question and see the shape before I click. The little drawings help more than the names." | "Nothing here tells me which colors. The key says a Reference form is 'drawn as a sketch'; am I allowed to publish one?" | "Reference" |
| 14.142 | "Put the margin behind the bars and say its size and source." | "'The kit draws the phone drawing, the table and the files.' I work in a design app; I do not have the kit." | "kit" |
| 14.143 | "Number each loop's steps on its own." | "I would never make this; it reads as the studio's own tool." | "pill" |
| 14.144 | "Same rows on every card, no totals." | "Too much for me to copy." | "layer" |
| 15.22 | "Every stage has its source and the date someone read it." | "Long. I scrolled past the sources." | "enrolled" |
| 15.23 | "Steps and stages are different." | "Which one do I put on our newsletter?" | "stage" |
| 15.24 | "A reform has routes with feasibility words." | "Eleven cards, each with a closed list; I did not open them." | "Route" |
| 11.10 | "We could use this for our state's measure: six steps and the date it is certified." | "Can I put our real measure in, or must it be Illustrative?" | "Illustrative" |
| 11.11 | "Same marks as the ballot tracker." | "Nothing." | "Vacated" |
| 14.141, S95 social data card | "Two crops at true size, the words to post and the alt text to post. I can copy those." | "'Drawn at 1080 by 1350 px', but there is no button to get the picture. How do I post it?" | "crop" |

Summary in the reader's words (simulated): "The social card and the ballot tracker are what I would use. I still need someone to hand me the files."

### R5L, reader who leans left, reading for fairness (simulated)

Read at 1440 px from the Newsprint 1x captures and the page text.

| Plate | What it taught (simulated) | What confused (simulated) | The word that stopped them |
|---|---|---|---|
| "Choose a chart" | "Neutral inks, no party anywhere. Nothing to read for fairness." | "Nothing." | None |
| 14.142 | "The band calls five of seven drops since 2025 noise. I wondered if that softens bad news for the people in power, but the same band marks gains as 'Within the margin' too, and the window holds three years before the inauguration by a stated reason." | "Nothing on fairness." | "inauguration" |
| 14.143 | "Loop R10 says officials safe from defeat write rules for themselves. Both parties draw maps; the plate blames neither." | "Nothing on fairness." | "Safe seats" |
| 14.144 | "The reforms are picked by a stated rule: each names Loop R8." | "R-38's evidence for the problem is 'Contested'. The rent-software cases are real; I would have called it documented. It is the atlas's grade, quoted." | "Contested" |
| 15.22 | "The one real court case is chosen by a stated rule, the latest ruling that struck down part of an Act of Congress, and the plate prints the holding with no praise or blame." | "That case is a Republican committee's win that lets parties spend more with their candidates. 'We found' makes me ask how hard you looked. The sunset and the repeal sources are both tax laws one party passed, named only by number." | "we found" |
| 15.23 | "Steps beside stages; nothing partisan." | "Nothing." | None |
| 15.24 | "The atlas's words for what each route depends on, quoted." | "Route CRT quotes 'Court rulings favoring the appointing coalition'. I agree with it; a conservative reader will read it as a jab at this Court." | "appointing coalition" |
| 11.10 | "Park fees, library funding, lake setbacks: no party cue, and each labeled Illustrative." | "Nothing." | None |
| 11.11 | "A trademark, a ferry contract, noise walls: no party cue." | "Nothing." | None |
| 14.137, S91 comparison cards | "Who picks each kind of trial judge, side by side, no adjectives." | "Nothing." | "good behavior" |

Summary in the reader's words (simulated): "I looked hard and found the selection rules stated where it matters most. The one place I could not see a rule was 15.24's example."

### R5R, reader who leans right, reading for fairness (simulated)

Read at 1440 px and, where captures had landed, 390 px, from the Newsprint 1x captures and the page text.

| Plate | What it taught (simulated) | What confused (simulated) | The word that stopped them |
|---|---|---|---|
| "Choose a chart" | "No party anywhere." | "Nothing." | None |
| 14.142 | "All seven drops fall after the January 2025 inauguration and the title opens 'Payrolls shrank'. But the band says five of them are noise, the window's reason is printed, and the failure plate's 'The economy lost jobs in seven months of 2025 and 2026' is marked as the thing not to publish. That is fair." | "The table marks every month through July 2026 'Final' while a note says yearly revisions move earlier months." | "shrank" |
| 14.143 | "Safe seats and primaries: true of both parties' districts." | "Nothing on fairness." | "balancing" |
| 14.144 | "The three reforms are picked by a stated rule, each names Loop R8. On-cycle local elections have backers in both parties." | "R-38 regulates landlords' pricing software. Two of the three cards are rules on markets." | "renter-owner" |
| 15.22 | "The court case is stated by its holding, plainly." | "The sunset source is the 2017 tax law and the repeal source is the July 2025 tax law, both passed by one party, used as the examples of how a law ends or changes. Named only as 'Public Law 115-97' and 'Public Law 119-21', most readers will not notice; I did, and I wanted the rule that picked them." | "Public Law 119-21" |
| 15.23 | "Nothing partisan." | "Nothing." | None |
| 15.24 | "The atlas's own feasibility words, quoted." | "The one reform read through in full is R-28, 'Taxing inherited gains and capital income'. Why that one? The atlas's reform list reads like one side's agenda: an indexed minimum wage, sector bargaining, baby bonds. The plate puts a tax increase in the spotlight and says nothing about why." | "inherited gains" |
| 11.10 | "Invented measures with no party cue." | "Nothing." | None |
| 11.11 | "Invented cases with no party cue." | "Nothing." | None |
| 14.136, S90 by-the-numbers | "Six facts, each with its table. New York spends the most and Idaho the least, which is what the record says." | "The table prints '46,370,928.0' students and '994,922,042.0' thousands of dollars. Fractions of a student." | "46,370,928.0" |

Summary in the reader's words (simulated): "The jobs chart surprised me by being fair. 15.24's example and the two tax-law sources are where I would push."

### R6, screen reader user (simulated from the page's text, not from a screen reader)

**How R6 was simulated.** At 16:41 and 16:51 UTC `browsers.sh` printed "WAIT" (two browsers open, load 3.15 and 4.31), so R6 was built without a browser, from the built page's markup by script (`scripts/extract.py`, the `*.a11y.txt` files): headings, links, buttons, lists and table rows in reading order; an `aria-hidden` subtree dropped; a `role="img"` node read as its label; a group read as its label plus its `aria-describedby` text; live regions flagged. The script cannot see CSS, so text a style hides (a note shown only for the chosen reform, the "needs JavaScript" line) may be in R6's transcript when a real screen reader would skip it. No screen reader, Safari or Firefox was used (DR-279). The character counts below are measured; what R6 "hears" is the panel's model of it.

| Plate | What it taught (simulated) | What confused (simulated) | The word that stopped them |
|---|---|---|---|
| "Choose a chart" | "A group named 'Choose a chart', then sixteen lists, each named by its question, with links like 'Ranked bar, Core'. The 'Skip these 10 forms' links let me jump a question." | "I move by headings. The sixteen questions are not headings, so pressing H took me past all 144 links to the first heading after the guide. I found the questions only by list navigation." | "Core" (a tier word follows every one of the 127 names) |
| 14.142, S96 | "The table is the chart for me: 57 rows, and a last column that says 'Drop past the margin' twice and 'Within the margin' where the survey cannot tell. The alt text gives both named drops." | "The alt says 'Two are drawn in the strongest ink'. Ink tells me nothing; 'the two marked drops' would." | "strongest ink" |
| 14.143 | "The status line reads 'Loop R10, step 2 of 4' and the step, so I always know which loop I am in. 'Reset the loop' and 'Previous step' say why they are unavailable." | "The group's description says the shared variable is 'the pill filled in ink in both'." | "pill" |
| 14.144 | "Three radio buttons in a group named 'Show one reform on Loop R8'. Each card reads row by row, with every effect code then its meaning." | "'Reform R-06 turns one connection red.' The status line has to tell me which one; the card's sentence is about a color I cannot see." | "red" |
| 15.22 | "Every stage with its source and the date it was read." | "Entering the plate, I hear a description of 4,276 characters that walks all 20 stages, and then the plate's own text, 5,973 characters, walks them again." | "squares" |
| 15.23 | "Five lists, each step with its stages under it." | "'Step 4 keeps its slash' assumes I know what the slash looks like." | "slash" |
| 15.24 | "Eleven routes, each with a closed disclosure I can open." | "About 3,800 words of live text; 'Not checked' repeated on 113 lines once opened." | "feasibility" |
| 11.10 | "The plate's label reads all three measures with each step as 'done', 'now', 'never happened' or 'stopped'. Clear." | "After that label, the same plate's words play again (873 characters), because the words inside the picture are not hidden from me (DR-278's item b). The label starts 'at 360 px on Newsprint'." | "Newsprint" |
| 11.11 | "'Petition denied by the Supreme Court on January 11. The appeals court's ruling stands.' Clear." | "The same repetition after the label (599 characters)." | "Newsprint" |
| 14.81, S87 Venn diagram | "Four groups with their counts and shares, and a table with a margin column." | "I heard '28.3 percent' for public coverage alone and '28.3 million' for no coverage in one breath, and had to go back." | "28.3" |

Summary in the reader's words (simulated): "The live parts work by ear: the stepper's status line and the radio buttons are the best I have met in a guide. The long descriptions on live-text plates, and the questions that are not headings, cost me the most time."

## What the panel concludes

This section is the panel agent's own reading of what the simulated readers met, checked against the page by script and the captures. The readers' words above are hypotheses; each fault below was confirmed on the built page or in its source before it was written here.

### Must fix

**RP-1. Rule 14.144: choosing Reform R-38 leaves a heavy line on the loop.** Where: `fig-s-14-144-correct`, state capture `newsprint-1x/1440/states/s-14-144-correct--R-38.png`; the plate CSS written by `phase3_ch14_complex_build.py`. What is wrong: with R-38 chosen, Connection L39 still draws as a 6 px Charcoal line, the heaviest stroke on the drawing, while the plate says "Neither target of Reform R-38 sits on the drawing, so nothing on it turns red" and the rule's whole point is that "A reform can name a loop and target nothing on it, as Reform R-38 does with Loop R8." R2, R5L and R5R read the heavy line as R-38's target. Cause, read from the plate's styles: the rules for a reform not chosen reset `.ak-mark` to 2 px but never reset `.ak-case`, so the default `.sv .crt .ak-case{stroke:var(--oa-color-graphic-essential);stroke-width:6px}` keeps drawing the keyline case of R-06's and R-30's target. Rule 15.20's chooser has no `.ak-case` rules and is not touched. Fix: for each reform, add `.p:has([value="R-xx"]:checked) [data-oa-for]:not([data-oa-for~="R-xx"]) .ak-case{stroke:none}`, or draw the case only under the chosen reform's targets; then recapture all three states at 1440 and 390 on both grounds. Owner: complex examples maker, with the component engineer for the chooser part.

**RP-2. Rule 14.138, S92: the table says every records request ends in an appeal and a lawsuit.** Where: S92's table, column "Every request or optional" (`work/build/chart-kit/specs/s92.json`, `table.columns[2].words`; `work/build/data/govinfo-foia-request-steps.csv`, column `path`). What is wrong: rows 6 and 8 read "Appeal a denial | Every request" and "Go to court | Every request", because the column maps the data's `main` path to the words "Every request". R1 read it as "every request goes to court". A reader who checks the table learns a false thing about the law the plate teaches. Fix: give the steps that follow a denial their condition, for example a `path` value `if_denied` worded "Only if the agency says no" for rows 6 and 8, keep "Every request" for rows 1 to 3 and 5 and "Optional" for rows 4 and 7; or rename the column "On the main path or a branch". Owner: infographics maker, with the editor for the words.

### Should fix

**RP-3. The front door does not lead to round 5's best work.** Where: `s-14-selection-guide.html` (`selection_guide_build.py`); entries `14-032.json`, `14-074.json`, `14-075.json`, `14-088.json`, `14-096.json`, `14-135.json`. What is wrong: "Choose a chart" holds 144 links, 127 forms, 16 skips and "Skip to Rule 14.1", and none reaches Rules 14.142 to 14.144. The entries a reader lands on point nowhere near them: 14.32 "Columns with a moving average" relates only to 14.9 and 14.11; 14.96 and 14.135 never point to 15.22; 14.88's step tracker never points to 11.10 or 11.11. R3 picked 14.32 for a jobs chart and never met the band; R2 picked a process form and never met 15.22. Fix: one line under the sixteen questions naming group 18, "Three charts in full", and chapter 15 for workflows and routes; add 14.142 to 14.32's and 14.74's related rules, 15.22 to 14.96's and 14.135's, and 11.10, 11.11 and 15.23 to 14.88's. Owners: selection guide maker; editor for the entries.

**RP-4. Rule 15.22, stage 2 states a majority as a fixed count.** Where: `fig-s-15-22-correct`, stage 2 (`phase3_ch15_build.py`, `fs_stages()`). Quoted: "A simple majority: 218 of 435 in the House, or 51 of 100 in the Senate." A simple majority is a majority of the members voting, with a quorum present; stage 3 on the same plate says "two-thirds of the members voting", and chapter 14's plates for Rule 14.7 and S26 count two empty House seats on November 11, 2026. R2 called it the number a teacher spends a class un-teaching. Fix: "A simple majority of the members voting, with a quorum present. In the Senate the Vice President breaks a tie." Owner: systems designer, with the research lead for the law and the editor for the words.

**RP-5. Rule 15.22, stage 7 names only a conference committee.** Where: stage 7, a filled square on the line of stages "every enacted bill passes". Quoted: "A conference committee settles the differences, and both chambers approve the same text." Most bills now settle their differences by passing amendments back and forth, and many pass the second chamber unchanged. Fix: "Both chambers pass the same text, by trading amendments or through a conference committee." Owner: systems designer, with the research lead (who should cite the source for the amendment exchange) and the editor.

**RP-6. Rule 15.22, stage 10's two lines print in three columns.** Where: `fig-s-15-22-correct`, captured at 1440 (`newsprint-1x/1440/s-15-22-correct.png`). "Short of two-thirds in either chamber, the bill dies." prints as "Short of", a gap, "two-thirds", a gap, "in either chamber, the bill dies.", and "With two-thirds in each, then stage 13." gains the same gaps. Cause: `.wf .sq{display:flex;gap:8px}` makes the `span.nw2` around "two-thirds" a flex item of its own. At 390 px it is worse: the three pieces stack in narrow columns over four lines (`newsprint-1x/390/s-15-22-correct.png`). Reach, measured by script across the page: 2 lines, both on this plate. Fix: drop the `nw2` span inside `.sq` lines, or wrap the words after the square in one span. Owner: systems designer.

**RP-7. Rule 14.144: one variable sits in two layers.** Where: the R-38 card, "Targets outside this loop". Quoted: "Connection LT12 “Shared-data pricing software can raise rents”, contested, from Variable TC7 to Variable EC9 “Cost of essentials”, in the technology layer", while the R-30 card prints "Variable EC9 “Cost of essentials”, in the economy layer". The atlas holds EC9 in the economy layer and LT12 in the technology layer (`atlas-v7-data.json`, `nodes.EC9.layer`, `links.LT12.layer`). R2 asked which is right. Fix: set a connection's layer after its own name, "Connection LT12 “…”, contested, in the technology layer, from Variable TC7 to Variable EC9 “Cost of essentials”", the same on both cards. Owner: complex examples maker.

**RP-8. "Band" means two things in two neighboring rules.** Where: Rule 14.142 (the shaded margin of error) and Rule 14.144's card row "Band, the kind of change: Rules", which carries the atlas's `band` field (rules, parameter, feedback and the rest). R2 and R1 stopped on it. Fix: name 14.144's row "Kind of change" and gloss the atlas's word once if it must appear. Owner: complex examples maker, with the editor (the drift read may rule on the word guide-wide).

**RP-9. The loop drawings on 14.143 and 14.144 carry marks no key reads.** Where: both plates. Each connection carries one to three delay ticks, and 14.143's Connection L53 is dashed for its plausible grade; neither plate has a key for ticks or line codes, which Rule 15.17's plate gives. On 14.144 the ticks have no words anywhere: "Each step" lists Connections L38 and L39 with their grades only, while the atlas codes both delays L. R2, R3 and R1 asked what the crossbars mean. Fix: a short key on both plates (one tick under 2 years, two ticks 2 to 10 years, three ticks longer; solid, dashed and dotted by grade, as Rule 13.4 sets), and each step's delay in words on 14.144. Owner: complex examples maker.

**RP-10. Rule 14.142 points to a second jobs chart it never names.** Where: S96's measure line, "the span both jobs charts share", and its last note, "Both jobs charts run from January 2022 to September 2026". The other chart is S14, Rule 14.32, 110 rules earlier. R2 and R3 stopped on "both". Fix: "the span this chart shares with the jobs chart of Rule 14.32", and the same in the note. Owner: complex examples maker, with the editor.

**RP-11. Two choices on chapter 15's plates have no stated rule, and both fairness readers asked.** Where: Rule 15.24's one worked reform, "Reform R-28 “Taxing inherited gains and capital income”", and Rule 15.22's sunset and repeal sources, Public Law 115-97, section 11022, and Public Law 119-21, section 70104. No line says why R-28 was chosen; R-25 "Full child tax credit for low-earning families" also names reconciliation (`atlas-v7-data.json`, `reforms.R-25.routes`). The decision log's one R-28 entry, D3-2044, sets how the entry's words print, not why R-28 was chosen. The two public laws print as bare numbers, though H12 asks for the neutral name ("Public Law 119-21, the July 2025 tax law"). Fix: print the rule that picks the worked reform (for example "the two entries that name reconciliation are R-25 and R-28; this plate reads ...", with the reason), and name each public law in words where it appears. Owner: systems designer, with the data lead for the rule and the editor for the names.

**RP-12. Rule 14.136, S90's table prints counts with a decimal.** Where: S90's table, column "Value" (`s90.json`, format `number:1`). Quoted: "46,370,928.0 | students" and "994,922,042.0 | thousands of dollars". R5R stopped on fractions of a student. Fix: format by row: whole numbers for counts and dollar totals, one decimal for shares and per-pupil dollars, or round dollars as the panel prints them. Owner: infographics maker.

**RP-13. On chapter 15's live-text plates, a screen reader hears the plate twice (simulated, measured).** Where: the group descriptions (`aria-describedby`) of `fig-s-15-22-correct` (4,276 characters), `fig-s-15-24-correct` (1,906) and `fig-s-15-23-correct` (1,072), each followed by the plate's own live text (5,973, 24,837 and 5,139 characters) that says the same stages again. Fix: on a plate whose content is live text, keep the description to one or two sentences on what the plate holds and how it is laid out. Owner: systems designer; the accessibility lead confirms with the accessibility tree.

**RP-14. "Choose a chart"'s sixteen questions are not headings.** Where: `p.sg-qt` in `s-14-selection-guide.html`. A reader who moves by headings, as R6 does, passes all 144 links without meeting a question. Each list is named by its question (`aria-labelledby`), so list navigation works. Fix: mark each question as a heading at the level under the plate, or give it `role="heading"` with its level. Owner: selection guide maker; the accessibility lead confirms.

**RP-15. Rule 11.11 never names certiorari.** Where: Rule 11.11's text and step 5, "Supreme Court petition". News reports say "cert denied"; R2 said students could not connect the two. Fix: one gloss at first use, such as "a petition for a writ of certiorari, the order that brings a case up, which news reports shorten to cert". Owner: tracker designer, with the editor. Board 3 shows the step names to Dustin; this gloss changes no step name.

**RP-16. Rule 11.10 names an end it never explains.** Where: Rule 11.10's specifications, "Not approved by voters where most said yes but a second test failed, with a sentence that names it". The rule text and plates never say what a second test is. R2 and R3 asked. Fix: one sentence in the rule naming the kinds of second test the four states' law sets, with its source, or drop the end words if none of the four states has one. Owner: tracker designer, with the research lead.

**RP-17. Rule 14.79, S85: the Civic Line heading reads as a second title.** Where: S85, the line "Worker bargaining power | Variable A2" above the grid. R3 read it as a claim that union membership measures bargaining power. The sentence that explains it, "The drawing beside “Worker bargaining power” is the atlas's symbol for Variable A2", sits only in the closed "The table and notes". DR-266 set the drawing, so it stays. Fix: move that sentence, with what ties the measure to the variable, into the visible notes. Owner: maker A, with the editor.

**RP-18. Rule 14.135, S89 never spells out FEMA.** Where: S89's grade line, title, steps and notes; "Federal Emergency Management Agency" appears nowhere in Rule 14.135 (counted by script). H02 and H11. Fix: spell it out at first use in the grade line or the first step. Owner: infographics maker, with the editor.

**RP-19. Rule 15.22, stage 19 hedges its stated rule.** Where: stage 19. Quoted: "The latest such ruling we found came on June 30, 2026". The rule that picks the case is stated and date-based, so it would pick the same case for either side, and R5L and R5R both accepted the plain holding. "We found" is what made R5L ask how hard the studio looked: it reads as a hedge (chapter 02, W16) where a date would carry the limit. Fix: "As of November 14, 2026, the latest such ruling came on June 30, 2026, when ...". Owner: systems designer, with the editor.

**RP-20. Rule 14.142 never says what "90 percent" means.** Where: S96's measure line, notes and source line, which give "the survey’s 90 percent margin of error" and "the Bureau’s 90 percent interval" with no plain gloss; Rule 14.9, which the rule cites, does not give one either. R1 and R3 stopped on it. Fix: one clause in the first note, for example "a range the Bureau expects to hold the true change in nine samples of ten", worded with the data lead. Owner: complex examples maker, with the editor and the data lead.

## The twelve named places, as the panel met them

1. **Carried items.** The panel's readers did not stumble on the chooser's pill widths (DD-R2); the keyline case under a chosen target (DD-R5's neighbor) is where RP-1's fault lives, so whichever way the design director's pair is ruled, the case must clear when a reform with no target is chosen. SG-6: readers met the tier after the name ("Ranked bar, Core"); R6 hears "Core" 127 times as a suffix and R4 asked what a tier allows, which a tier word above the name would not change. S14's label, S94's year mark and S16's note were not in the panel's reading. Round 4's cards: S95 read at 1440 and 390 on Newsprint; see "Tested" for Charcoal.
2. **DR-278's four items.** Item (b) is what R6 met on Rules 11.10 and 11.11: the plate's words heard again after its label (873 and 599 characters). Items (a), (c) and (d) were outside the panel's reading.
3. **Page-wide reach.** Outside the panel's lens. The one style fault the readers exposed, RP-6, stays inside 15.22's `.wf` scope and reaches 2 lines.
4. **The selection guide at true size.** At 1440 and 390 the readers told forms apart by their drawings (R4: "the little drawings help more than the names"). At 390 the guide runs 11,375 px tall, about sixteen phone screens, and R1 scrolled it whole. "Skip to Rule 14.1" lands on Group 1's head, directly above Rule 14.1. RP-3 and RP-14 are this place's faults.
5. **The palette specification.** Not in the panel's reading.
6. **Rule 14.142.** Every reader learned the band's lesson in one reading, and both fairness readers called the chart fair, R5R because the failure plate is the headline he expected. RP-10 ("both jobs charts") and RP-20 ("90 percent") are its word faults. R1 first read the shaded band as the zone where losses go, because its label "Margin of error" sits under the zero line; the craft reader may judge whether the label should sit on the band's edge.
7. **Rules 14.143 and 14.144 live and still.** The stepper counts each loop's own steps: after five presses the status line reads "Loop R10, step 2 of 4" (state capture). RP-1 is the live chooser's fault; RP-7, RP-8 and RP-9 are words and marks.
8. **Chapter 15 as one chapter.** The panel read 15.22 to 15.24 only. R2 and R3 told a step from a stage after 15.23; R1 lost the thread in 15.24's eleven cards. RP-4, RP-5, RP-6, RP-11, RP-13 and RP-19.
9. **The trackers' law.** Readers understood "Affirmed", "Vacated" with its gloss, the tie and the denied petition at step 5 without the law in hand. RP-15 (certiorari) and RP-16 (the second test) are the gaps they named.
10. **NRSC v. FEC from the left and the right.** The rule is stated and dated, the plate prints the holding alone, and the same rule would pick the same case whoever won it. R5L asked how the case was found (RP-19); both fairness readers asked instead about 15.24's R-28 and 15.22's two tax-law sources, which have no stated rule (RP-11).
11. **Weight.** Outside the panel's lens.
12. **Loop titles and DR-274's numbers.** Each variable's own title prints in every loop the readers read (14.143, 14.144). No stale "Rule 11.1N" citation appeared in the text the panel extracted from its nine rules and seven forms; the panel did not scan the rest of the guide.

## Questions for Dustin

None. Every fix above sits inside an owner's approved work. The two that touch what board 3 shows him, RP-15 (a gloss for certiorari beside the court case tracker's step 5) and RP-16 (the ballot tracker's "second test"), change no step name or end word; board 3 still shows those for his approval.

## Tested

- Page text for the selection guide, Rules 14.142, 14.143, 14.144, 15.22, 15.23, 15.24, 11.10, 11.11 and 11.12, the two step tables and seven round 4 forms (14.79, 14.81, 14.135 to 14.138, 14.141), extracted by script from the strict build of `9a6e1182` (`scratchpad/c07/main/guide.html`), never read whole.
- The selection guide's questions, forms, tiers and links counted by script (16 questions, 127 forms, 144 links), and every link on the page that points to Rules 14.142 to 14.144 traced to its source (rule index, local contents, chapter 14's token table, two chapter 15 disclosures).
- Captures read with the file reader: Newsprint 1x at 1440 px for every plate above, the 1440 state captures of 14.143 (step 5) and 14.144 (R-30 and R-38), and Newsprint 1x at 390 px for S96, S92, 14.143, 14.144 and the selection guide; further widths and grounds as listed under "Captures read" below.
- RP-1's cause read from the plate's own styles; RP-2's from `s92.json` and its data file; RP-6's from the page's `.wf .sq` rule, with its reach counted page-wide (2 lines); RP-7 against `atlas-v7-data.json`; RP-11 against the atlas's reform routes and the decision log (searched for "R-28"); RP-12 from `s90.json`; RP-13's characters counted per plate; RP-14 from the selection guide's markup; RP-18 by a count of "Federal Emergency" in Rule 14.135 and its spec and entry.
- R6's transcript, built by script from the markup as described under R6, with the browser rule checked by `browsers.sh` at 16:41, 16:51 and 16:56 UTC (all "WAIT").

## Not tested

- No real reader. Every reader is simulated (DR-202).
- No screen reader, Safari or Firefox (DR-279). R6 is a model built from markup, and CSS hiding was not seen.
- No browser was opened by the panel while `browsers.sh` printed "WAIT".
- The panel ran no guide check, no kit build and no contrast measure.
- The palette specification, S86, S88, S93, S94, the two sketches, S12's tile, Rule 15.25 and Rule 18.22's plates were outside the panel's reading.
