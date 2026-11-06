# Red team: brand and nonpartisanship

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Data visualization round, lens 4. One reviewer, working as the brand and evidence auditor for a nonpartisan civic publisher and holding every word to the editor's standards (`.claude/agents/oa-editor.md`). I read all five views of the three concepts in Playwright at 1440 and 390 px. By script I audited computed color, type, every Pillar Red mark, Prussian, party marks and the wordmark, opened every disclosure, and tabulated the repair log. Then I read each title and note twice, once as a reader on the left and once as a reader on the right. I edited nothing in the repo. Scripts and screenshots sit in the scratchpad (`brandaudit/`).

Scores on this lens: 5 ships as built. 4 has no must-fix of its own, and its should-fixes are word or token edits. 3 has a must-fix of its own that one pass clears. 2 has must-fixes plus a lean that repeats across specimens. 1 reads as partisan. The shared disclosure finding (SH-M1) sits outside the scores, because the brief and the shared data never carried the disclosure. Until it lands, no concept ships on this lens.

## 1. Verdict per concept

### 01 Explainer: 3 of 5

The cleanest brand mechanics and the fullest account of the atlas's coding: the whole coding note opens under S03 and S08, the S02 title leaves the tax credit out, and the reading guide says "Red never means a party, good or bad." Its S08 is the most pointed chart in the round. The title and brackets split the log at January 2025, and the dotted "mid-decade maps" note shows two maps per party where the log holds more on one side.

Reason: two must-fixes on S08, and the page's one red lands on the 2021 credit.

### 02 Register: 2 of 5

Locked type, measured tints, a strict frame, and the only titles that attribute the direction code in so many words ("the atlas codes as"). It also stacks the most emphasis on one side: the credit in the S02 title, the view's red on the same point, a System ask about the 2021 credit, "ALL FOUR UP" tags on two reform programs, and a navy tower of "away" squares with no word on how dense the log is. Its definition of "toward voters" drops the clause that codes benefit policy.

Reason: two must-fixes, and a lean that repeats across four specimens.

### 03 Instrument: 4 of 5

The best emphasis of the three. The working red marks the Senate's 7-vote shortfall on a ban that both parties' voters favored. The S08 note says "The split at January 1, 2025 is the studio's.", its panel heads print 31 and 33 changes so the log's density shows, and its definition keeps the household clause. Five titles still need word changes, chiefly S06, which names "the federal package and capacity first", and S09, which ends on "Trump v. Slaughter".

Reason: no must-fix of its own; every should-fix is a title or note edit.

## 2. Findings per concept

### 01 Explainer

**Must fix**

**EX-M1. S08, White and Newsprint, 1440 and 390 px. The title and brackets split the log at the month a new administration took office.**
- What I see. Title: "Since January 2025, 17 changes in the atlas’s log moved the rules away from voters and 8 moved them toward voters." Bracket labels: "1965 through 2024: 16 toward, 7 away" and "Since January 2025: 8 toward, 17 away".
- What is wrong. The log holds no entry between January 1 and January 20, 2025, so the split falls exactly at the change of administration. The studio chose it, and the page never says so.
- Read from the left: proof that the new administration moved the rules away from voters; worth sharing. Read from the right: a scorecard on one administration, built partly from codes they dispute, such as the proof-of-citizenship order (RL33), the ranked-choice bans (RL46, RL47) and the repeal of an overdraft rule (RL34). They stop trusting the other nine charts.
- What the data holds. 11 of the 17 entries concern congressional maps: seven mid-decade maps or votes to allow one (RL38, RL40, RL41, RL50, RL53, RL54, RL56) and four court rulings on maps (RL48, RL51, RL52, RL57). The other six are RL32, RL33, RL34, RL46, RL47 and RL58. The log holds 33 of its 64 entries in 2025 and 2026.
- Fix. Title the chart by what the entries are, for example "Eleven of the 17 changes the atlas codes as away from voters in 2025 and 2026 concern congressional maps: seven mid-decade maps or votes to allow one, and four court rulings." The maker's own alternative also works: "The atlas’s log holds 24 changes toward voters and 24 away from them." Relabel the brackets "1965 to 2024" and "2025 and 2026", and add to the measure line: "The split at 2025 is the studio’s; the log holds 33 of its 64 entries in those two years."

**EX-M2. S08, White and Newsprint, both widths, and the table notes. The dotted list of mid-decade maps leaves rows out and looks balanced as a result.**
- What I see. "Dotted: mid-decade congressional maps, coded away from voters whichever party drew them (Texas and Missouri in 2025, California in 2025 and Virginia in 2026)." The build dots four rows: `REDRAWS = ['RL38', 'RL40', 'RL41', 'RL50']` (`build_concept.py`, line 1094).
- What is wrong. The log describes two more mid-decade redraws, both coded away: Florida, which "redrew all 28 congressional districts in the middle of the decade" (RL53), and Tennessee, which repealed its ban on changing districts between censuses and drew a new map (RL54). Louisiana's 2026 map (RL56) may fall under the same rule. The log does not record party control. By my reading of who held each legislature, the note shows two maps per party where the log holds at least four drawn by Republican-led legislatures and two by Democratic-led ones.
- Why it matters. A reader on the left who knows Florida's map sees a balance made by leaving rows out. A reader on the right who later finds the gap distrusts the one note written to reassure them.
- Fix. Dot every mid-decade map entry coded away and list them in date order, with no grouping by party: "Texas, Missouri and California in 2025; Virginia, Florida, Tennessee and Louisiana in 2026". Check RL56 against the atlas's redraw rule first.

**Should fix**

**EX-S1. Working red on S02 in White, Newsprint and Charcoal; System demonstrations A and B; the type ramp's note example.** The page's one red, and the guide's model of how red behaves, lands on "the 2021 low the title names": the year of the expanded child tax credit, a policy most readers tie to one party. From the right, the brand's single accent reads as applause for that policy; from the left, as an endorsement. Fix: give the views' working red to a point both sides read the same way, such as S01's Senate shortfall with a title that names it (Instrument's S01), or use no working red on the chart views (D2-97 allows none). Rebuild System demonstrations A and B on that specimen.

**EX-S2. S03, White and Newsprint. The title states the atlas's code as plain fact.** "Nine of the 11 state statutes in the atlas’s log moved the rules away from voters." The attribution sits below, in the label and measure line, and a shared headline travels without them. The nine are five congressional maps (RL38, RL40, RL53, RL54, RL56), three limits on ranked-choice voting (RL08, RL46, RL47) and Utah's commission rollback (RL13). The atlas's own coding note says readers may weigh the ranked-choice entries differently. A reader on the right sees state legislatures branded as working against voters, with no way to set aside the codes they dispute. Fix: retitle as "The atlas codes 9 of the 11 state statutes in its log as moving the rules away from voters." Add a note: "Five are mid-decade congressional maps and three limit ranked-choice voting, entries the atlas says readers may weigh differently. Without those three, 6 of 8 statutes moved away, still the largest share."

**EX-S3. System view, demonstration B. The ask carries no illustrative label.** "Find your state’s child poverty rate" has no "Illustrative" beside it. Register and Instrument both label theirs "Illustrative ask", and CLAUDE.md requires the label beside the item. Fix: add "Illustrative ask" beside the button.

**Polish**

**EX-P1. S02 note on White, Newsprint, Charcoal and System.** "Census reads a change between years as a description, not the effect of one policy." This is the line that keeps S02 even-handed, and it is set as a corrective negation. Fix: "Census describes the change between years and credits no single policy with it."

**EX-P2. System, demonstration A.** "Red points; it never encodes a series." This is a contrasting pair. Fix: "Red marks the one point the title names."

**EX-P3. Distinctiveness.** With the wordmark covered, the White view reads as a careful newsroom page set in Inter; the maker's notes say the same. The Newsprint view and the black evidence chip carry the brand. See the distinctiveness note in section 3.

### 02 Register

**Must fix**

**RG-M1. S03 note 1 and table, on White, Newsprint, Charcoal and the System plate. The definition of "toward voters" drops two clauses, and the full coding note never appears.**
- What I see. "Directions are the atlas's own codes, set out in its coding note: "toward voters" means a change widens who can vote or have a ballot counted, opens the deciding contest, limits or shows political money, or strengthens a check on officials."
- What is missing. The atlas's definition also covers changes that make "each vote weigh more equally" and that add "to household security through automatic benefits". The page never prints the full note, so its cross-party rules on maps and the ranked-choice caveat ("readers may weigh these entries differently") appear nowhere. "household security" and "weigh these entries" each occur 0 times in the file.
- Why it matters. Five rows rest on the household clause (RL15, RL16, RL31, RL34, RL35). RL34, the repeal of a bank overdraft rule, is one of the 17 away squares in S08, and S08's table lists it as "away from voters". A reader on the right who opens that table finds a consumer-finance vote coded against voters with no stated reason, and reads the code as policy preference. The brief allows source text to be shortened by dropping words, never facts.
- Fix. Print the definition whole, and add a "Read the atlas's full coding note" disclosure under S03 and S08, as Instrument does on S08.

**RG-M2. S08, White and Newsprint. The title presents a surge without saying how dense the log is.**
- What I see. Title: "Seventeen of the 24 rule changes the atlas codes as moving away from voters came in 2025 and 2026." The drawing labels a tall Prussian stack "17 of the 24 came in 2025 and 2026". Note 1 reads "...since January 2025, 8 toward and 17 away."
- What is wrong. Nothing on the figure says that the log holds 33 of its 64 entries in those two years, or that the split is the studio's. "17 of 24" reads as a surge. Measured against a log that is half 2025 and 2026, the same years hold 71 percent of away entries and 52 percent of all entries.
- How it reads. From the left: the surge is the new administration's doing. From the right: the scorecard described in EX-M1.
- Fix. Add to the measure line: "The log holds 33 of its 64 entries in 2025 and 2026; the split at 2025 is the studio's." Change "since January 2025" to "in 2025 and 2026". Retitle by what the entries are; EX-M1's wording fits.

**Should fix**

**RG-S1. S02 on White, Newsprint and Charcoal, and the System view. Three emphases fall on one policy.** The title, "...while the expanded child tax credit was paid.", pairs the policy with the low in display type. The views' one red sits on the same point. The System ask reads "Read how the 2021 credit was paid". Readers tie that policy to one party. Fix: use Explainer's title ("...the lowest since the series began in 2009, and more than doubled the next year."), keep the policy in the note only, move the working red as in EX-S1, and give the System demonstration an ask that names no policy.

**RG-S2. S03 and S08 on White and Newsprint. Prussian marks "away from voters".** That is 6 segments in S03 and 25 squares in S08. The research brief's R14 notes that "Prussian beside red would read as Democratic blue (design judgment)". In S08 a navy tower of away entries, most of them actions by officials of the other party, invites readers to take the tint as a party code, read either way. Fix: draw away in Charcoal and toward in Verdigris, as Instrument does, and keep Prussian for S06's diverging arm.

**RG-S3. S06 on White and Newsprint. "ALL FOUR UP" tags crown two programs.** The tags sit on "A coherent federal package" and "Capacity first: civil service, IRS, inspectors general, congressional staff and digital service", under the title "Two of the eight reform paths would move all four outcome families up by 2036, if their assumptions hold." Capacity first gets its fourth "up" from the studio's reading of "same as scenario ii", as note 3 says. A reader on the right sees the publisher endorsing federal action and IRS capacity. "Reform paths" also takes in the baseline, which has no reform. Fix: drop the tags, call the rows scenarios, and use a title that names no program, such as Explainer's ("If their assumptions hold, five of the seven scenarios beyond the baseline would lift at least one outcome family by 2036.").

**RG-S4. Every chart on White and Newsprint. No chart carries an Oath & Action credit.** R20 asks for the credit at the right of the source line. The Census charts (S02, S04, S05) and the Ballotpedia map (S07) carry no Oath & Action name anywhere in the figure, so a still shared on its own names no maker. Fix: add "Chart: Oath & Action" at the right of the source line, set as Explainer and Instrument set it (Inter 400, 13 px, Deep Stone).

**RG-S5. System view, "How to read our charts". The guide never says what red means.** Explainer says "Red never means a party, good or bad." Instrument says "It never stands for a party, a side or a group." Pillar Red is the color many U.S. readers tie to one party. Fix: add one line.

**Polish**

**RG-P1. System view (98 swatches) and Charcoal view (5 swatches).** Swatch outlines use `rgba(127, 127, 127, 0.35)`, a gray at 35 percent that is neither a locked color nor a listed tint. Fix: a full-strength Stone or Deep Stone hairline.

### 03 Instrument

**Should fix**

**IN-S1. S06 title on White and Newsprint. The title crowns two programs.** "Two of eight scenarios would move all four outcome families up by 2036: the federal package and capacity first." One of the two lists "civil service, IRS, inspectors general, congressional staff and digital service". The note concedes that "Capacity first reaches "up" on economic performance through "same as scenario ii"." A reader on the right reads this as the publisher's choice of programs. Fix: name no program in the title; Explainer's form works.

**IN-S2. S09 title on White and Newsprint. The title ends on a case named for the sitting president.** "The atlas traces 24 documented rule changes on four threads, from the Fifteenth Amendment in 1870 to Trump v. Slaughter in 2026." No other title in the round names a sitting officeholder. This one sets his name as the end of an arc that starts with the Fifteenth Amendment. Readers on the left see an arc of decline; readers on the right see commentary. Fix: "...on four threads, from 1870 to 2026."

**IN-S3. S02 title. The title pairs the credit with the low.** "...fell to 5.1% in 2021, the year the expanded child tax credit paid out, and was 12.0% in 2022." Red sits elsewhere, so the lean is lighter than Register's, but the display line still ties the policy to the low. Fix: use Explainer's title, and keep RL15 and RL16 in the note.

**IN-S4. S03 title. The title states the code as fact and sets legislatures against voters.** "State statutes moved the rules away from voters in 9 of 11 logged changes; ballot initiatives did so in none of 17." The second clause makes a contrasting pair, a form the maker flagged. S03 prints the short definition but has no full coding note, so the ranked-choice caveat never reaches it. Fix: retitle as "The atlas codes 9 of 11 logged state statutes as moving the rules away from voters, the largest share of any instrument." Move the initiatives' count into the note beside its bar, add "Read the atlas's full coding note" under S03, and add EX-S2's composition note.

**IN-S5. S08 title. The best treatment of the split still leads with it.** "Seventeen of the 24 logged changes that moved rules away from voters came in 2025 and 2026." The figure handles the split best of the three: its panel heads print 31 and 33 changes, and its note says "The split at January 1, 2025 is the studio's." The title still leads with the split and states the code as fact. Fix: retitle as in EX-M1.

**Polish**

**IN-P1. Social card. The signature tag wraps the whole card.** `data-red="signature"` sits on a span that wraps the full 1080 by 1350 card (`class="sigwrap"`). Any red mark on the card without a tag of its own would count as signature red; the bracket escapes only because it carries its own tag. Fix: put the attribute on the wordmark group alone.

**IN-P2. S02 note.** "The Census Bureau describes a change between two years; it does not credit one policy with it." This is a contrasting pair. Fix: "The Census Bureau describes the change between two years and credits no single policy with it."

**IN-P3. System view, 42 swatches.** Outlines use `rgba(93, 99, 109, 0.5)`, Stone at half strength. Fix: full-strength Stone.

## 3. Shared findings

**SH-M1. Must fix, all three. The editor's disclosure is missing where his campaign's subject is charted.** V7's nomination disclosure, as the atlas round copied it into `atlas_editorial_data.py`, reads: "Oath & Action's editor works with the Yes on 3 campaign for Massachusetts Question 3 and promotes it through Veterans for All Voters, where he is Massachusetts state lead. He also co-leads Ranked Choice Melrose, a local campaign." D2-80 prints it wherever the reform is argued. In this round the subject appears in four specimens:
- S07 maps state bans on ranked-choice voting under the reader question "Where can a city adopt ranked-choice voting".
- S03 and S08 count ranked-choice adoptions and open primaries toward voters and bans away. RL64, Massachusetts Question 3 itself, is one of the squares; Register's table and Instrument's tooltip and CSV print its text.
- S06 prints V7's reason that "How often the primary decides the winner falls where nomination rules change", and scenario iv-a's fusion voting. Explainer's S06 table names R-47 and R-07.

None of the three pages prints the disclosure: "Yes on 3", "Veterans for All Voters" and "Ranked Choice Melrose" each occur 0 times in each file. The shared data carries no interest field, so the makers had no way to know. A reader on the right who learns of the campaign after sharing S07 will read the ranked-choice codes as the editor's advocacy. Fix: the main session adds the disclosure to the shared data, and each concept prints it, labeled "Disclosure", in the notes of S03, S06, S07 and S08. Dustin should confirm the wording, since it describes his own work.

**SH-S1. Should fix, all three. The set leans one way.** Read across, five of the ten specimens point the same direction:
- S02: the best year of a policy most readers tie to one party.
- S03 and S08: codes that put most recent actions by one party's officials in the away column.
- S06: V7's baseline reasons, printed in all three tables, include "the 2025 law shifts resources toward higher-income households".
- S07: bans passed by legislatures of one party, on the editor's own cause.

None points the other way. S01, S04, S05, S09 and S10 read the same from both sides, apart from Instrument's S09 title (IN-S2). The set is the main session's (D2-92), so a maker can only soften it with titles, notes and red, which the findings above do. For the chapter 14 set, pick specimens so that each side meets a finding it would rather skip. Write a two-reader check into the system sheet: before a title ships, it is read once from the left and once from the right.

**SH-S2. Should fix, all three. The atlas's own neutrality line is hidden or missing on the repair-log charts.** V7's coding note ends: "A row's direction describes the rule's effect on who officials answer to and carries no judgment of the people or parties involved." Register prints a short form on S03 only. Explainer and Instrument keep it inside a closed disclosure. Fix: print it in the visible notes of S03 and S08.

**SH-S3. Should fix, all three; overlaps the statistics lens. The RL47 note is missing from the charts that need it.** D2-103 requires the RL47 note on every count from the log: RL47 rolls 19 state bans into one row, and Indiana and Missouri are also counted on their own. No concept shows it in the S03 drawing; Explainer has it in the table only. On S08, only Explainer shows it. Fix: add the one-line note under S03 and S08.

**SH-P1. Polish, all three. S02 names one credit law and leaves out another.** S02's notes cite the 2021 expansion (RL15) and its lapse (RL16). They leave out RL35, the July 2025 law that set the credit at up to $2,200 per child, which sits in the same log and inside the chart's years. A reader on the right will notice which law is named. Fix: add a note at 2025 that names RL35 in the log's words.

### Notes for Dustin (V7 text, which the studio does not edit)

1. **Map descriptions in the repair log are uneven.** Register's S08 table and Instrument's S08 tooltips, table and CSV print the log's row text. It gives the seat aim of the Texas and Florida maps ("designed to move five seats held by Democrats to Republicans"; "three to four additional Republican seats"). It describes California's and Virginia's maps as responses ("in response to Texas"; "in response to other states' mid-decade maps"), with no seat aim. Readers on the right will read the asymmetry. Suggested item for the V7.1 list: give every map the same two facts, its stated aim and its seat effect.
2. **S06's baseline reasons read as a verdict on current policy.** S06 prints V7's reasons for the baseline, including "Workforce losses, funding lapses and closed digital service teams" and "the 2025 law shifts resources toward higher-income households". To a reader on the right, the baseline column reads as a verdict on current policy. Confirm that each reason carries its source in V7.
3. **The household-security clause will draw the first challenge.** It codes benefit and consumer-finance votes as a direction for voters (RL15, RL16, RL31, RL34, RL35). Readers on the right will contest this code first, and the charts explain it least.

### Brand checks, all three

| Check | 01 Explainer | 02 Register | 03 Instrument |
|---|---|---|---|
| One working-red job per view, at 1440 and 390 px | Pass: S02's 2021 low on White, Newsprint and Charcoal; none on the card or System | Pass: S02's 2021 low on White, Newsprint and Charcoal | Pass: S01's 7-vote bracket on every view |
| Red never encodes | Pass | Pass | Pass |
| Newsprint keyline | 1 px Charcoal stroke on the red dot, both widths | 1 px Charcoal stroke, both widths | 5 px Charcoal path under the 3 px red stroke (1 px each side), both widths and on the Newsprint card |
| Red on Prussian | None | None; S02 holds no Prussian | None |
| Rule 05.3 quoted on System | Exact to D2-01 (script) | Exact | Exact |
| System red as specimen (D2-102) | `specimen` | `specimen` | Swatches `swatch`; the S01 demonstration stays `working`, and the ask button turned the bracket Charcoal when pressed |
| Party marks (DR-48) | Charcoal bars, names printed, `data-party`, ordered by value | Same | Same; "All registered voters" in Stone |
| Palette | Locked colors and the listed OKLab mixes | Adds the `rgba` outline (RG-P1) | Adds the `rgba` outline (IN-P3) |
| Type | Inter and Inter Tight; Lora Italic only on two quotations (the editorial commitment in the type ramp, and Rule 05.3) | Inter and Inter Tight | Inter and Inter Tight |
| Wordmark master | Masthead paths match the 24 px master at 221 by 24 px; the 16 px master shows at 390; display master on the card; inside `data-red="signature"` | Same | Same; signature tag wraps the card (IN-P1) |
| Borrowed newspaper marks (D2-65) | None found by name or face | None | None |
| Chart credit | "Chart: Oath & Action", Inter 400, 13 px, Deep Stone | None (RG-S4) | As Explainer |

**Distinctiveness.** With the wordmark hidden, all three White views read as careful editorial pages set in Inter: black titles, gray context, hairline rules. Very little on them is Oath & Action's alone. All three read as the same family as the atlas pick: the same masthead, Inter Tight 800 titles, Stone and Charcoal layering and 2 px section rules. Explainer sits closest to the pick and is the most generic. Register's Prussian and Verdigris and Instrument's record keys (RL07, PW15) and module frame are the most ownable. On every concept, the Newsprint view carries the brand far better than White. In my judgment, that argues for Newsprint as the chart ground when Dustin settles it (DR-45).

### Every title, read from the left and the right

| Spec | How it reads | Titles that lean |
|---|---|---|
| S01 | All three read the same from both sides. Both parties' voters agree, and Congress fell short. | None |
| S02 | Left: the credit worked. Right: a case for one party's credit, and the 2025 law goes unnamed. | Register and Instrument name the credit in the title; Explainer keeps it in the note |
| S03 | Left: legislatures work against voters. Right: mostly their own party's legislatures are branded, through codes the atlas itself says readers may weigh differently. | Explainer and Instrument state the code as fact; Register attributes it |
| S04 | Even from both sides | None |
| S05 | Even from both sides. Register adds that the Hispanic gap narrowed. | None |
| S06 | Left: reform works. Right: the publisher endorses federal programs and IRS capacity. | Register's tags and Instrument's title name programs; Explainer's title names none |
| S07 | Facts read the same from both sides. The ranked-choice cause is the editor's own (SH-M1). | None in wording |
| S08 | Left: the administration moved the rules away from voters. Right: a scorecard against them. | All three split at 2025. Explainer says "Since January 2025" in the title; Register says it in a note and gives no density; Instrument discloses the split and shows density |
| S09 | Even from both sides in Explainer and Register | Instrument ends on "Trump v. Slaughter" |
| S10 | Even from both sides | None |

The writing scan found no em dashes and none of the listed words in any view. It found the corrective negations and contrasting pairs listed above (EX-P1, EX-P2, IN-P2, IN-S4). It also found "a claim's grade covers that claim, not the whole answer", which comes from the shared S10 source line, so the fix belongs in the shared data.

## 4. What I tested and what I could not test

**Tested**
- Visible text (`innerText`) of all 15 views at 1440 px and at 390 px, written per view to the scratchpad, and read in full for the White view of each concept and every System and social view.
- The hidden text of every `details` element on the White views: coding notes, tables and notes. I also grepped each page for the S08 table's row text and for Instrument's tooltip text.
- Computed fill, stroke, color, background, border, shadow and gradient on every visible element of every view at 1440 px, tallied by value and traced to its element.
- Computed font family, weight and style on every text element. Lora appears only on two quotations in Explainer's System view. I also listed the families declared in each Google Fonts link.
- Every Pillar Red element per view at 1440 and 390 px: its `data-red` value, job, specimen, stroke and sibling paint, as the keyline check. I also counted Prussian paint per specimen and recorded the paints and printed names of every `data-party` mark.
- Wordmark path data in each masthead and social card against the three masters (16 px, 24 px, display), and the masthead size at 1440 and 390 px.
- Every live-type "Oath & Action" outside source lines: only the "Chart: Oath & Action" credits.
- Rule 05.3 on each System view against D2-01, by script after normalizing quotation marks.
- Instrument's "Put an ask in this view" button, pressed in Playwright. The ask took the red and the bracket's stroke turned Charcoal.
- Grep for newspaper names and faces in the three pages and the three build scripts.
- Tabulations of the repair log by script: by period, instrument and direction; the 17 away entries since 2025 by subject; statute composition with and without the ranked-choice rows; the household-clause rows; the log's density by year.
- A search of the pages and the shared data for the editor's interest disclosure and for R-01, R-07 and R-47.
- Screenshots with the wordmark hidden: the opening screen of each concept, and S01, S02, S03 and S08 on White and S02 on Newsprint. I compared them with the atlas pick's captures, and I compared the makers' Newsprint and Charcoal captures with the masthead covered.
- The stored results of the shared rendered check (run at 05:30 to 05:33). Red jobs, unmarked red, red on Prussian and party marks are clean at 1440, 390 and 360 px for all three.
- A regex scan of all visible text for em dashes, the listed filler and corporate words, hedges and corrective negation.

**Could not test**
- I did not run `dataviz_check.js` or `dataviz_verify.py` myself. Both write results beside the pages, and this task allows no repo writes. Their numbers above are the makers' stored runs.
- My own audit at 360 px; the stored check covers that width.
- Rendered font files in my own runs. I read declared and computed families; the stored check lists Inter and Inter Tight as loaded, plus Lora on Explainer's System view.
- Hover states. I read Instrument's tooltip text from the markup without hovering.
- Real readers. The left and right readings are one reviewer's simulation, not a test with people.
- Party control of each legislature, which the log does not record. EX-M2's count rests on my own knowledge, marked as such.
- Whether V7's codes and row texts are right about the world, and the sources behind them.
- The PNG or SVG exports, social posting, and print.
- Rhetorical triplets, nominalizations and setup-and-payoff lines across every note. I read titles and notes for these, and the regex does not catch them.
- The current S06 data. During this review the shared data's `scenarios-2030` class rules changed in the working tree, after the pages were built; the repair log did not change. My S06 findings quote the pages as built.
