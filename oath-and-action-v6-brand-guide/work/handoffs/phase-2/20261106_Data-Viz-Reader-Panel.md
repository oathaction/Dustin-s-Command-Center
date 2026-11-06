# Reader Panel: Three Chart Systems

Simulated first-time reader panel for the data visualization round, Oath & Action Brand Guide Edition 06, Phase 2, November 6, 2026. Paths are relative to `oath-and-action-v6-brand-guide/`.

**This panel was simulated by one model. It is not a test with real people (DR-51).** The six readers are invented personas, and every quote in this report is simulated. Real readers with these profiles may answer differently. Read the results as a list of likely snags to check later with people.

## How the panel ran

**What the readers saw.** Only screenshots from each concept's `captures/` folder: `-white-390.jpg` and `-newsprint-390.jpg` for phone readers, `-white-1440.jpg` for desktop readers, and `-social-1440.jpg` for the social card. No reader saw HTML, code, makers' notes, the brief's rules or any red team report. The panel runner read `CLAUDE.md` and the "Reader panel" section of `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Brief.md`, and nothing else about the concepts.

**How the captures were cut.** The captures run 10,000 to 25,000 pixels tall. To crop one image per specimen, the runner loaded each page in Playwright at the capture width and read only the top edge and height of each specimen's box. Every page height matched its capture height to the pixel, so the crops line up with the captures. The readers' answers rest on the cropped pixels alone. Crops and scripts sit in the session scratchpad, outside the repo.

**Who read what.**

| Reader | Device | Capture | Specimens |
|---|---|---|---|
| Ray, 67, Ohio | iPhone, large text | White, 390 | S01, S08, S03, S07 |
| Dana, 41, Arizona | Laptop, projected for class | White, 1440 | S01, S08, S04, S09 |
| Keisha, 33, Georgia | Android phone, on break | Newsprint, 390 | S01, S08, S02, S10 |
| Tom, 29, Minnesota | Office desktop | White, 1440 | S01, S08, S06, S07 |
| Luis, 52, Texas | Phone | Newsprint, 390 | S01, S08, S03, S06 |
| Maya, 20, California | Phone, from Instagram | Social card for S01, then White, 390 | S01 (card), S08, S04, S05 |

**Rules the panel kept.**

1. Every capture shows "Show the table", "Show the table and notes", "How the atlas codes direction" and the Table switches closed. Ray, Keisha and Maya would not tap them. Dana and Tom would, and Luis would try once on S06, but the captures do not show what opens, so no reader got anything from them. Where that mattered, the answer says so.
2. Ray reads with large text. The captures are at default text size, so his answers cover what shows at that size. How each layout reflows at his size was not tested.
3. "Point at a square" and "Point at a state" readouts need a pointer, so no reader got them.
4. The studio note boxes ("STUDIO NOTE, NOT PART OF THE CHART" and "STUDIO NOTE FOR REVIEWERS") appear in the captures. Readers skipped them, since they come off before publication.
5. Figures are quoted as the screenshots show them. The panel did not check them against the data.

Each specimen answer runs in the same order: what it says in one sentence, how sure it is, who made it and where the numbers came from, what snagged, whether it seems to take a side, and whether the reader would trust or share it.

**The three concepts as a stranger meets them.**

- **01 Explainer.** White, one reading column. A black "FINDING" or "ESTIMATE" tag sits beside a plain sentence about the evidence ("Documented: a published survey and two recorded votes"). Titles state the point. Notes fold away under "Show the table and notes".
- **02 Register.** Each chart carries a table of figures beside or under it and numbered notes. Navy and green marks. On the White phone page, a ten-row index of "specimens" fills about three screens before the first chart. Charts carry no "Chart: Oath & Action" credit line.
- **03 Instrument.** Record codes in each chart's top right corner ("Atlas sources N40, K1908, W035", "Repair log RL01 to RL64"), Chart and Table buttons, and Download CSV and SVG buttons. The page opens with "Every chart here is a module with the same seven slots, in the same order, on the Signal Grid's 8 px rhythm."

## 1. Ray, 67, retired machinist, Ohio

iPhone with large text. Distrusts national media. Leans right. Ray reads slowly and wants to know who is behind a thing before he believes it. He would not tap any button.

### 01 Explainer

- **S01.** *Says:* "Voters in both parties want Congress out of the stock market. The House passed a ban and the Senate didn't take it up." *Sure:* "It says 'Documented: a published survey and two recorded votes.' Plain enough." *Source:* "University of Maryland survey, House and Senate roll calls. The chart's by Oath & Action, whoever they are." *Snag:* "The survey's from 2023 and the votes are 2026. They tell you that twice, which I'll give them. The source print is tiny and gray." *Side:* "No. Both parties in the same black." *Share:* "Yes."
- **S08.** *Says:* "Since January 2025 more changes went against voters than for them." *Sure:* "'Coded by the atlas.' So they graded it themselves." *Source:* "'The atlas's log.' That's them citing them." *Snag:* "What rules? Voting rules? The '2012' label runs into the squares. 'How the atlas codes direction' is a button I'm not pressing on a phone." *Side:* "January 2025 is when Trump came in, so this reads like a scorecard on him. They do count California's and Virginia's maps against voters along with Texas and Missouri, 'whichever party drew them'. That helps." *Share:* "No. I'd want the list."
- **S03.** *Says:* "State legislatures mostly made the rules worse for voters, and ballot questions never did." *Sure:* "Same atlas coding." *Source:* "Their own log again." *Snag:* "Away is black and toward is dark gray. On my phone they look alike. 'Eight failed, which left the rules in force' I understood." *Side:* "Ohio's legislature is Republican. Calling statehouses bad for voters and ballot questions good for them is a side, and I can't see who made that rule." *Share:* "No."
- **S07.** *Says:* "Nineteen states ban ranked-choice voting, and Ohio partly." *Sure:* "'Secondary compilation: Ballotpedia, checked against the atlas.' Never heard of Ballotpedia." *Source:* "Ballotpedia." *Snag:* "It never says what ranked-choice voting is. Ohio is a white box, and all I get is 'Ohio and Tennessee ban it in some elections only.' Which elections?" *Side:* "It's a map of laws. Fair." *Share:* "Maybe."

### 02 Register

The phone page opened with three screens of a table headed "THE TEN SPECIMENS" before any chart. "I almost quit before I saw a picture."

- **S01.** *Says:* Same as Explainer. *Sure:* "'documented record' in small gray letters." *Source:* "Survey and roll calls. I don't see who drew it; there's no name on the chart." *Snag:* "'Senate, cloture on the motion to proceed.' The note says cloture is 'the Senate vote that ends debate.' OK. I'm guessing H.R. 7008 is the ban." *Side:* "No. 'By party, in one ink, highest first.'" *Share:* "Yes, though the votes are a list, not a picture."
- **S08.** *Says:* "Seventeen of 24 changes against voters came in 2025 and 2026." *Sure:* "'documented record', but coded by them." *Source:* "Their log." *Snag:* "'1965' and '1988' sit stacked under one column. No square tells me what it stands for." *Side:* "A pile of navy blocks in Trump's two years and no examples. A note says a redraw counts against voters 'whichever party draws it', but it doesn't show me one." *Share:* "No."
- **S03.** *Says:* "Legislatures and courts made most of the changes against voters." *Sure:* "Their coding." *Source:* "Their log." *Snag:* "Every bar has five little columns of numbers under it. Longest thing I scrolled today, and with my big text it'll be worse." *Side:* "It lumps courts in, and note 1 says 'A direction carries no judgment of the people or parties involved.' Then their rule counts 'limits or shows political money' as good for voters. That's their opinion on campaign money." *Share:* "Halfway."
- **S07.** *Says:* "Nineteen states ban it, and Ohio leaves cities an opening." *Sure:* "'secondary compilation.'" *Source:* "Ballotpedia, and some page that 'refused automated reading'. A robot couldn't read it?" *Snag:* "'On wide screens two digits under a code give the year.' I'm on a phone, so why tell me? Note 2 is the first time anyone said what Ohio did: 'Ohio's ban leaves an opening for home-rule cities, at the cost of state funds.' Note 4 finally says what ranked-choice voting is." *Side:* "No." *Share:* "Yes, for the Ohio part."

### 03 Instrument

The opening paragraph about "the Signal Grid's 8 px rhythm" told Ray the page was "written for somebody else."

- **S01.** *Says:* "The Senate came 7 votes short of taking up a ban that nearly 9 in 10 of both parties wanted." *Sure:* "'FINDING', then 'Atlas sources N40, K1908, W035'. Looks like a parts number." *Source:* "Survey, roll calls, 'Chart: Oath & Action'." *Snag:* "Who were the 47 who voted no? It doesn't say which party." *Side:* "The headline leads with the Senate failing and there's a red bracket under it. That points a finger without saying at whom." *Share:* "Probably. The numbers are all there."
- **S08.** *Says:* "Seventeen of the 24 changes against voters came in 2025 and 2026." *Sure:* "Their coding, and they say 'The split at January 1, 2025 is the studio's.'" *Source:* "Their log." *Snag:* "Numbered squares, 32, 33, 34, like a raffle. 'Point at a square to read its record.' I can't point at a picture." *Side:* "They print what counts as toward voters, down to 'or adds automatic household security.' A benefit check counts as pro-voter? Now I know where they stand. At least they printed it." *Share:* "No, though I respect that they showed their rule."
- **S03.** *Says:* "State laws went against voters 9 of 11 times; ballot initiatives never did." *Sure:* "Their coding." *Source:* "Their log." *Snag:* "None. Numbers inside the bars, black and green, I can tell them apart." *Side:* "Same rulebook as S08, and it favors ballot questions over the legislature." *Share:* "The counting I trust. The labels I don't."
- **S07.** *Says:* "Nineteen states ban it; Ohio's covers some elections since 2026." *Sure:* "Ballotpedia, they say, is 'a secondary source.'" *Source:* "Ballotpedia, plus the 'Atlas repair log RL47' code up top." *Snag:* "No one says what ranked-choice voting is. The Ohio note is the clearest of the three: 'home-rule cities may still adopt it, but they lose state local government fund money while it is in effect.'" *Side:* "No." *Share:* "Yes."

**Ray's ranking: 1 Explainer, 2 Instrument, 3 Register.** "Explainer was the shortest read and the only one that named maps drawn by both parties; Instrument showed its rulebook and read like a parts catalog; Register made me wade through tables first."

## 2. Dana, 41, high school civics teacher, Arizona

Laptop, projected for a class. Independent. Dana asks whether a 16-year-old could say what a chart shows, and whether it carries a caveat she can teach. She would open "Show the table and notes" before class; the captures show it closed, so she judged the face of each chart.

### 01 Explainer

- **S01.** *Says:* "Voters in both parties backed a stock-trading ban; the House passed it and the Senate fell 7 votes short of taking it up." *Sure:* "The label says a survey and two recorded votes." *Source:* "Printed in full with roll call numbers." *Snag:* "'7 votes short of the 60 needed.' Students will ask why 60 when 53 is a majority. Nothing on the face explains it." *Side:* "No. 'The two parties sit one point apart, and the bars run from 0 to 100 percent' is a lesson in one sentence." *Share:* "Yes. I'd project it."
- **S08.** *Says:* "Since January 2025, 17 changes moved the rules away from voters and 8 toward; before that it was 16 toward and 7 away." *Sure:* "'The log is the atlas's record and runs denser in recent years.' I can teach that line: more squares might mean more record-keeping." *Source:* "The publisher's own log." *Snag:* "The definition hides behind 'How the atlas codes direction.' A class will argue about what 'away from voters' means, and that definition is what I need on the slide." *Side:* "It names maps drawn by both parties. Some kids will still hear 'away' as a verdict." *Share:* "Yes, with the coding note open."
- **S04.** *Says:* "Young adults reported voting far less than seniors, and the gap grew from 23 to 27 points." *Sure:* "'Official statistic: what survey respondents reported' and 'a change of a point or two may sit within survey error.' That's the caveat I teach." *Source:* "Census survey, Table A-1." *Snag:* "The axis starts at 40 and no sentence says so. A student will think 47.7 percent is near zero." *Side:* "No." *Share:* "Yes."
- **S09.** *Says:* "Most of the 24 changes fall in two stretches, 1964 to 1978 and 2010 to 2026." *Sure:* "'Every event is documented; the atlas chose which to date.' Honest about who picked." *Source:* "The atlas, each event on a statute or ruling." *Snag:* "Short names like '1929 House fixed at 435' need a gloss for kids. Otherwise the best timeline here: names on the drawing, one time scale, shaded bands." *Side:* "Picking 24 events is a choice, and they say so. Shelby County, Citizens United, Taft-Hartley and Proposition 13 all appear, so both sides' grievances show up." *Share:* "Yes, as a handout."

### 02 Register

- **S01.** *Says:* Same as Explainer. *Sure:* "'documented record.'" *Source:* "Survey and roll calls, printed in full." *Snag:* "'Senate, cloture on the motion to proceed' needs help, and note 2 gives it: 'Cloture is the Senate vote that ends debate. Taking up this bill needed three-fifths of the Senate, 60 votes.' That's the line Explainer lacked." *Side:* "No." *Share:* "Yes. The vote table works on a slide."
- **S08.** *Says:* "Seventeen of the 24 changes coded away from voters came in 2025 and 2026." *Sure:* "The atlas's codes." *Source:* "Its log." *Snag:* "Three bands on one year axis reads well on a projector. There's no definition of 'toward' on this chart and no example. The axis jumps from '1965 1988' to 2010; note 4 explains it in small type." *Side:* "Note 2 says a partisan redraw counts against voters whichever party draws it. Show one." *Share:* "Only beside S03, which carries the definition."
- **S04.** *Says:* "Reported voting rose with age; every group under 65 dipped." *Sure:* "'official statistic, self-reported', and 'the scale runs from 40 to 80 percent' is in the measure line." *Source:* "Census Table A-1." *Snag:* "'The table gives no margins of error.' And then what? Explainer says what that means for the reader." *Side:* "No." *Share:* "Yes. The 2020, 2024 and Change columns are a ready worksheet."
- **S09.** *Says:* "The atlas dates 24 changes since 1870, six per thread." *Sure:* "'documented record.'" *Source:* "The atlas's history." *Snag:* "The title only counts, so students won't know what to notice. Time runs down the page in four columns; fine. Note 2 mentions 'Event numbers E01 to E24' and I see no numbers on the drawing." *Side:* "No." *Share:* "Yes."

### 03 Instrument

- **S01.** *Says:* "The Senate fell 7 votes short of taking up a ban that 88 percent of Democrats and 87 percent of Republicans favored." *Sure:* "'FINDING' and a row of codes." *Source:* "Printed; 'three-fifths of the Senate' is on the chart." *Snag:* "Kids will ask what N40, K1908 and W035 are." *Side:* "Leading with the Senate makes it a story about the Senate. The agreement is the bigger lesson." *Share:* "Maybe."
- **S08.** *Says:* "Seventeen of 24 changes away from voters came in 2025 and 2026." *Sure:* "The full rule is printed. That's the paragraph I'd put on a slide." *Source:* "The atlas's log, with record numbers." *Snag:* "One block covers 1965 to 2024 and the other two years, drawn side by side as if they're alike. The numbers on the squares are record IDs, which a student will try to read as something." *Side:* "'The split at January 1, 2025 is the studio's.' Honest, and that split is the whole argument." *Share:* "Yes, for a debate exercise."
- **S04.** *Says:* "Reported turnout ran from 47.7 percent of 18-to-24s to 74.7 percent of seniors, and every group under 65 fell." *Sure:* "'the scale starts at 40%' is printed. The note says reported voting runs higher than counted ballots." *Source:* "Census Table A-1." *Snag:* "No word on survey error." *Side:* "No." *Share:* "Yes."
- **S09.** *Says:* "Twenty-four changes on four threads, from 1870 to 2026." *Sure:* "'documented.'" *Source:* "The atlas." *Snag:* "Students must look up E13 in a list under the line. On a projector that's a scavenger hunt." *Side:* "The title ends on 'Trump v. Slaughter in 2026.' Some students will take that as the point." *Share:* "The lists under each lane would make a study sheet. The drawing less so."

**Dana's ranking: 1 Explainer, 2 Register, 3 Instrument.** "Explainer gives students one thing to notice per chart and carries the best caveats; Register's numbered notes teach the vocabulary; Instrument makes them decode keys before they can read."

## 3. Keisha, 33, night-shift nurse, Georgia

Android phone, Newsprint ground, ten minutes on a break in a dim room. Does not follow politics. Would not tap anything. Across all three: "Small gray print on the tan background is hard at 3 a.m."

### 01 Explainer

- **S01.** *Says:* "Most voters want to stop Congress trading stocks, and Congress didn't finish it." *Sure:* "'Documented.' Sounds checked." *Source:* "University of Maryland." *Snag:* "None." *Side:* "No, both parties agree." *Share:* "I'd send it to my mom."
- **S08.** *Says:* "Lately more changes have been bad for voters?" *Sure:* "No idea what 'the atlas's log' is." *Source:* "The atlas, whatever that is." *Snag:* "Which rules? Voting rules? Two columns of black squares with years down the middle, and a note about 'mid-decade congressional maps.'" *Side:* "Can't tell." *Share:* "No. I don't get it enough."
- **S02.** *Says:* "Child poverty dropped way down in 2021 and more than doubled the next year." *Sure:* "'Official statistic: Census Bureau survey estimates.' Census is real." *Source:* "Census." *Snag:* "Two lines, 'Supplemental' and 'Official.' I don't know why there are two or which is right." *Side:* "The red dot on the low point makes me think they want that credit back. They do say Census reads it 'as a description, not the effect of one policy.'" *Share:* "Maybe, to a coworker with kids."
- **S10.** *Says:* "About three in four of their claims are documented?" *Sure:* "'Documented: the atlas's own register of graded claims.' They're grading themselves." *Source:* "Them." *Snag:* "What are 'the atlas's 16 everyday answers'? A line runs right through the words 'Taxes, benefits and financial security.'" *Side:* "No." *Share:* "No."

### 02 Register

- **S01.** *Says:* Same as Explainer. *Sure:* "'documented record.'" *Source:* "Survey and votes." *Snag:* "'cloture on the motion to proceed.' Glad there's a note. Is H.R. 7008 the ban?" *Side:* "No." *Share:* "Yes."
- **S08.** *Says:* "Most of the bad-for-voters changes were in the last two years." *Sure:* "Can't tell." *Source:* "The atlas." *Snag:* "Navy, green and outline boxes. What's 'Neither way 16'?" *Side:* "Can't tell." *Share:* "No."
- **S02.** *Says:* "Child poverty hit 5.1 percent in 2021 while families got the bigger child tax credit, then rose to 12 percent when it expired." *Sure:* "'Margins of error run from 0.4 to 0.9 points.' Close but not exact." *Source:* "Census." *Snag:* "Note 1 says 'The Supplemental Poverty Measure counts tax credits and other aid that the official measure leaves out.' That's why there are two lines. Got it." *Side:* "The red dot again. Feels like it's cheering." *Share:* "Yes."
- **S10.** *Says:* "For each everyday question, how much of the answer rests on documented fact." *Sure:* "Their grades." *Source:* "The atlas." *Snag:* "'Why is it hard to find an appointment?' That's my patients every shift: 78.1. But 'Points from all claims +4.0' means nothing to me, and it's sixteen rows long. Note 3, 'Light fills fall under 3:1 against the ground', is for designers." *Side:* "No." *Share:* "The health one, yes."

### 03 Instrument

- **S01.** *Says:* "The Senate fell 7 short of taking up a ban most Democrats and Republicans wanted." *Sure:* "'FINDING.'" *Source:* "Survey and votes." *Snag:* "'Atlas sources N40, K1908, W035', 'Download CSV SVG.' What's a CSV?" *Side:* "No." *Share:* "Yes."
- **S08.** *Says:* "Seventeen changes went against voters in 2025 and 2026." *Sure:* "Can't tell." *Source:* "The atlas." *Snag:* "Numbered tiles like a bingo card, then a long paragraph of rules." *Side:* "Can't tell." *Share:* "No."
- **S02.** *Says:* "Child poverty fell to 5.1 percent the year the child tax credit paid out." *Sure:* "Census." *Source:* "Census, and a line above the title, 'Census P60-290 Tables 3 and 8; atlas RL15, RL16.'" *Snag:* "'Supplemental Poverty Measure in Charcoal, official measure in Stone.' Charcoal and Stone are colors? Sounds like a countertop. Three labels, 'Survey change', 'Processing change' and 'Method change', crowd the top. 'The official measure counts pretax money income and leaves out tax credits' helped." *Side:* "The title ties the drop to the credit; a note says Census doesn't." *Share:* "Maybe."
- **S10.** *Says:* "The public record backs 74 percent of their 433 claims." *Sure:* "Their grades." *Source:* "The atlas." *Snag:* "PW12, PW13. Tiny dashed patterns I can't make out on my phone." *Side:* "No." *Share:* "No."

**Keisha's ranking: 1 Register, 2 Explainer, 3 Instrument.** "Register answered my 'why two lines' and asked my patients' question; it took longer, and I got the most out of it. Explainer was quickest. Instrument felt like reading a lab requisition."

## 4. Tom, 29, city council staffer, Minnesota

Office desktop. Leans left. Comfortable with data; reads every footnote and would open tables and download files. The captures show tables closed, so he could not check counts.

### 01 Explainer

- **S01.** *Says:* "86 percent support, the parties within a point, the House passed it 232 to 198, and the Senate vote to take it up failed 53 to 47 against a 60-vote bar." *Sure:* "A survey of 2,625 with dates, and roll call numbers. Solid." *Source:* "PPC at Maryland and the roll calls, as recorded in the publisher's atlas." *Snag:* "I want the party split on both roll calls. It's the obvious next question." *Side:* "No." *Share:* "Yes."
- **S08.** *Says:* "After January 2025, 17 away and 8 toward; before, 16 toward and 7 away." *Sure:* "'The log is the atlas's record and runs denser in recent years.' Right caveat: the jump could be partly what the atlas chose to log lately. And 'One 2026 entry, RL47, counts 19 state bans on ranked-choice voting... as a single change.' They disclose the bundling." *Source:* "The atlas's own log." *Snag:* "The coding rule sits behind a toggle I can't see open here." *Side:* "Maps from both parties named. I'd cite this." *Share:* "Yes. It's the only one of the three that tells me how much weight the trend can bear."
- **S06.** *Says:* "If assumptions hold, five of seven reform scenarios lift at least one outcome by 2036, and the baseline lifts none." *Sure:* "'ESTIMATE. Conditional directions: no forecast and no odds.' Clear." *Source:* "'In the atlas's words.' The atlas is the publisher's." *Snag:* "'At least one' is a soft bar. Who wrote the scenarios?" *Side:* "It doesn't crown a winner. A Republican colleague could read it without flinching." *Share:* "Internally, yes."
- **S07.** *Says:* "Nineteen states ban RCV, 17 in all elections, and 12 of the bans came in 2024 or 2025." *Sure:* "'Secondary compilation: Ballotpedia, checked against the atlas.' Honest about the source." *Source:* "Ballotpedia." *Snag:* "A council member will ask whether a city can adopt RCV, and the face of the chart doesn't say. No definition of RCV either." *Side:* "No." *Share:* "Yes."

### 02 Register

- **S01.** *Says:* Same as Explainer. *Sure:* "'documented record.'" *Source:* "Printed in full. No 'Chart:' credit, so if I clip it nothing says who made it." *Snag:* "Party split of the votes, again." *Side:* "No." *Share:* "Yes. Cloture is defined, which saves me a footnote."
- **S08.** *Says:* "Seventeen of 24 away came in 2025 and 2026." *Sure:* "Three bands on one year axis is the clearest drawing of the trend, and note 1 gives both halves." *Source:* "The atlas's log." *Snag:* "No caveat that the log gets denser over time." *Side:* "The redraw note is good." *Share:* "Yes, with a caveat I'd add myself."
- **S06.** *Says:* "Two of eight paths move all four outcome families up, if assumptions hold." *Sure:* "'conditional estimate, no forecast.'" *Source:* "Atlas V7." *Snag:* "Note 3: 'Where V7 writes "same as scenario ii", the glyph shows that pointer; the title reads scenario ii's direction there.' So one of the 'all four up' claims leans on a pointer. And note 4, 'Up is Verdigris and down is Prussian.' Who talks like that?" *Side:* "'ALL FOUR UP' badges read as endorsements. One sits on the IRS-and-civil-service path; a bipartisan briefing would toss it." *Share:* "Not with the badges."
- **S07.** *Says:* "Nineteen states, listed by year." *Sure:* "'secondary compilation.'" *Source:* "Ballotpedia; the atlas cites NCSL." *Snag:* "'whose page refused automated reading' is a process note. Otherwise the best of the three: the year register (2024: 'Alabama, Kentucky, Louisiana, Mississippi, Missouri, Oklahoma'), note 1 ('A state without a ban may still give its cities no way to adopt ranked-choice voting') and a definition in note 4." *Side:* "No." *Share:* "Yes. I'd hand this to a council member."

### 03 Instrument

- **S01.** *Says:* "The Senate fell 7 short of taking up a ban 88 percent of Democrats and 87 percent of Republicans favored." *Sure:* "'All registered voters 86%' is its own bar, and a note says the 86 'comes from the survey's own release.' Good transparency." *Source:* "Codes I could trace, a CSV I could pull." *Snag:* "N40, K1908 and W035 mean nothing yet." *Side:* "The red bracket makes the Senate the story." *Share:* "Yes."
- **S08.** *Says:* "Seventeen of 24 away came in 2025 and 2026." *Sure:* "Definition printed in full, and 'The split at January 1, 2025 is the studio's.'" *Source:* "Record numbers I can match once the table is open." *Snag:* "Sixty years and two years drawn as equal blocks. No density caveat, and the RCV bundling isn't disclosed on the face." *Side:* "'Adds automatic household security' is in the rule. I agree with it; my Republican colleagues won't." *Share:* "Yes, with the CSV."
- **S06.** *Says:* "Two of eight scenarios move all four families up: 'the federal package and capacity first.'" *Sure:* "The conditional moved down into the measure line." *Source:* "The atlas." *Snag:* "A note admits 'Capacity first reaches "up" on economic performance through "same as scenario ii".' A headline that needs that footnote is overselling." *Side:* "It names winners. I'd agree with it and still not circulate it." *Share:* "No."
- **S07.** *Says:* "Nineteen states, with Ohio, Tennessee and Missouri explained beside the map." *Sure:* "'Ballotpedia is a secondary source.'" *Source:* "Ballotpedia, checked against NCSL and RL47." *Snag:* "'Whether a city in a state with no ban may adopt it depends on other state law, which the map does not show.' Good. No RCV definition, and 'refused an automated read' again." *Side:* "No." *Share:* "Yes."

**Tom's ranking: 1 Instrument, 2 Register, 3 Explainer.** "Instrument is the closest to a data product I can reuse, with downloads, record keys and the rule printed; I'd rewrite its S06 title myself. Register puts the numbers on the page. Explainer's captions are the most careful, and everything I want sits behind a toggle."

## 5. Luis, 52, small business owner, rural Texas

Phone, Newsprint ground. Leans right. Wary of experts telling him what to think. He tried "Show the table" once on S06; the capture shows it closed, so he got nothing from it.

### 01 Explainer

- **S01.** *Says:* "Almost everybody in both parties wants Congress out of the stock market, and the Senate didn't do it." *Sure:* "A survey and recorded votes." *Source:* "University of Maryland. A college poll, but I'd believe 86 percent on this." *Snag:* "Who voted no in the Senate?" *Side:* "No." *Share:* "Yes."
- **S08.** *Says:* "Since January 2025 more changes went against voters." *Sure:* "'Coded by the atlas.'" *Source:* "Their own log." *Snag:* "What's 'away from voters'? There's a button. I'm not tapping it." *Side:* "Texas and Missouri get named for their maps, and so do California and Virginia. Fair. But they keep the log and they score it." *Share:* "No."
- **S03.** *Says:* "State laws mostly went against voters; ballot initiatives never did." *Sure:* "Their coding." *Source:* "Their log." *Snag:* "Black and dark gray on this tan. I can't tell them apart." *Side:* "Texas has no citizen initiatives. Whoever writes the rule decides who looks good." *Share:* "No."
- **S06.** *Says:* "If their guesses pan out, most of their reform ideas help something by 2036." *Sure:* "'Conditional directions: no forecast and no odds.' At least they admit it's a guess." *Source:* "The atlas." *Snag:* "A long scroll of colored boxes. 'Capacity first: civil service, IRS, inspectors general.' Hiring at the IRS is a reform?" *Side:* "'Baseline: no reform beyond current law' comes out down or flat everywhere. So doing nothing is bad, they say. That's experts telling me what to think. The title itself doesn't push one plan." *Share:* "No."

### 02 Register

- **S01.** *Says:* Same as Explainer. *Sure:* "'documented record.'" *Source:* "Survey and votes." *Snag:* "The votes are a list. 'Fell seven short of the 60 votes needed.' Who voted no?" *Side:* "No." *Share:* "Yes."
- **S08.** *Says:* "Most changes against voters came in 2025 and 2026." *Sure:* "Their codes." *Source:* "Their log." *Snag:* "No examples at all." *Side:* "A navy tower in the last two years. Looks aimed at one party." *Share:* "No."
- **S03.** *Says:* "Legislatures and courts made 19 of the 24 changes against voters." *Sure:* "Their codes." *Source:* "Their log." *Snag:* "Lots of little number grids. Long." *Side:* "Courts too, so not only legislatures. Note 1 says a direction 'carries no judgment of the people or parties involved,' and then the rule counts 'limits or shows political money' as good. That's a judgment." *Share:* "Some."
- **S06.** *Says:* "Two of eight paths move everything up, if their assumptions hold." *Sure:* "'conditional estimate, no forecast.'" *Source:* "Atlas V7." *Snag:* "'Up is Verdigris and down is Prussian.' What language is that?" *Side:* "'ALL FOUR UP' stamped on the federal package and the IRS one. That's a recommendation." *Share:* "No."

### 03 Instrument

- **S01.** *Says:* "The Senate fell 7 short of a ban both parties' voters wanted." *Sure:* "'FINDING.'" *Source:* "Survey and votes, plus 'N40, K1908, W035.'" *Snag:* "If they're going to put a red mark under the Senate, show me the parties." *Side:* "Leans on the Senate." *Share:* "Maybe."
- **S08.** *Says:* "Seventeen of 24 changes against voters came in 2025 and 2026." *Sure:* "Their codes." *Source:* "Their log." *Snag:* "None. They print the rule: 'opens the contest that decides the seat, limits or shows political money... or adds automatic household security.'" *Side:* "That rule is a policy wish list. Thank you for showing it, because now I know." *Share:* "No."
- **S03.** *Says:* "State statutes went against voters 9 of 11 times; initiatives never." *Sure:* "Their codes." *Source:* "Their log." *Snag:* "None. Easiest of the three, with the numbers right in the bars." *Side:* "Same rulebook printed under it." *Share:* "The counting, yes."
- **S06.** *Says:* "Two of eight scenarios move all four families up: 'the federal package and capacity first.'" *Sure:* "'ESTIMATE,' and the condition is in the small print." *Source:* "The atlas." *Snag:* "None." *Side:* "They pick winners in the headline: a federal package and more IRS. This one's selling." *Share:* "No."

**Luis's ranking: 1 Explainer, 2 Instrument, 3 Register.** "Explainer pushed me least and named both parties' maps; Instrument at least shows its rulebook before it sells me a plan; Register stamps badges on plans and shows a pile of blue with no examples."

## 6. Maya, 20, first-generation college student, California

Phone. Gets most news from Instagram. Leans left. She meets S01 as the social card in her feed, then taps through to the White page on her phone.

### 01 Explainer

- **S01 (card).** *Says:* "Nearly 9 in 10 Republican and Democratic voters want a ban on Congress trading stocks, and the Senate still didn't take it up." *Sure:* "'Documented.'" *Source:* "Oath & Action logo at the top; survey and roll calls at the bottom." *Snag:* "None. Big 86%, big type, I got it in two seconds." *Side:* "No." *Share:* "Yes, to my story."
- **S08.** *Says:* "Since 2025 way more rule changes have gone against voters." *Sure:* "The atlas's codes, whatever the atlas is." *Source:* "The atlas." *Snag:* "What rules?" *Side:* "It feels like 'democracy is going backward under Trump.' It never says Trump. It does count California's map against voters too." *Share:* "Yes. The shape with the pile at the bottom left is striking."
- **S04.** *Says:* "People my age vote way less than older people, and the gap got bigger." *Sure:* "It's what people told a survey, and a point or two could be error." *Source:* "Census." *Snag:* "The '2024' and '2020' labels on the first row tell me which dot is which." *Side:* "No." *Share:* "Yes. Kind of a call-out to my friends."
- **S05.** *Says:* "Black families own homes way less than white families, nearly 30 points, and the gap is wider than in 2003." *Sure:* "Census." *Source:* "Census Housing Vacancy Survey." *Snag:* "Two values in 2002? The note explains, sort of. I also saw the Hispanic gap shrank, 28.7 to 25.8." *Side:* "No, it's Census numbers." *Share:* "Yes."

### 02 Register

- **S01 (card).** *Says:* Same, plus "86 percent of all registered voters." *Sure:* "'documented record.'" *Source:* "Full source, logo at the bottom." *Snag:* "A big blank gap in the middle, and 'Studio draft for the brand guide' next to the logo." *Side:* "No." *Share:* "Maybe. The bottom half is a lot of text."
- **S08.** *Says:* "Seventeen of 24 against-voter changes came in 2025 and 2026." *Sure:* "'documented record.'" *Source:* "The atlas." *Snag:* "Three rows of small blocks; the year labels are crammed." *Side:* "Same feeling as before." *Share:* "Maybe."
- **S04.** *Says:* "Reported voting rose with age: 47.7 percent of 18-to-24s, 74.7 percent of seniors." *Sure:* "'self-reported.'" *Source:* "Census." *Snag:* "I read the numbers line under each row to know which dot was which." *Side:* "No." *Share:* "Maybe."
- **S05.** *Says:* "The Black and white homeownership gap was 29.6 points in 2025." *Sure:* "Census." *Source:* "Census." *Snag:* "Four tiny charts in a grid; I'd have to zoom." *Side:* "No." *Share:* "No."

On the way to her first chart she scrolled past "three screens of 'specimens'."

### 03 Instrument

- **S01 (card).** *Says:* "The Senate fell 7 short of a ban both parties' voters favored." *Sure:* "'FINDING.'" *Source:* "Long source at the bottom." *Snag:* "Logo, a long headline, 86%, three bars, two vote bars, a red bracket and a paragraph of source. It's a lot for a post." *Side:* "No." *Share:* "No, too busy."
- **S08.** *Says:* "Seventeen of 24 changes against voters came in 2025 and 2026." *Sure:* "They print their rule." *Source:* "The atlas." *Snag:* "Numbered squares. 'Point at a square to read its record' doesn't work on a screenshot." *Side:* "Same feeling." *Share:* "No."
- **S04.** *Says:* "Turnout ran from 47.7 percent for 18-to-24s to 74.7 percent for seniors, and every group under 65 dropped." *Sure:* "Self-reported survey." *Source:* "Census." *Snag:* "None." *Side:* "No." *Share:* "Yes."
- **S05.** *Says:* "The white and Black homeownership gap was 29.6 points in 2025, wider than 2003." *Sure:* "Census." *Source:* "Census." *Snag:* "None. Full-width charts with the labels on the lines." *Side:* "No." *Share:* "Yes."

**Maya's ranking: 1 Explainer, 2 Instrument, 3 Register.** "Explainer's card is the one I'd post and its charts read fast; Instrument's charts are clear, though its card is crowded; Register's are small on a phone."

## Rankings

| Reader | First | Second | Third |
|---|---|---|---|
| Ray | Explainer | Instrument | Register |
| Dana | Explainer | Register | Instrument |
| Keisha | Register | Explainer | Instrument |
| Tom | Instrument | Register | Explainer |
| Luis | Explainer | Instrument | Register |
| Maya | Explainer | Instrument | Register |

Explainer placed first with four readers. Register and Instrument each placed first once. Scored three, two and one points by place, Explainer has 15, Instrument 11 and Register 10.

## Where the panel agreed

1. **S01 is the strongest specimen in all three concepts.** Every reader stated it in one sentence in every concept, and every reader would share it in at least one. The repeated line that the survey came three years before the votes earned trust from Ray, Luis and Tom.
2. **"The atlas" stopped every reader except Dana and Tom.** Labels and source lines say "the atlas's log", "repair log", "Atlas V7", "RL47" and "PW12" without saying that the atlas is the publisher's own research. Once Ray and Luis worked that out, they read every atlas-sourced chart as the publisher grading itself.
3. **S08 read as a verdict on the current administration** to Ray, Luis and Maya in all three concepts, because the split falls at January 2025. Explainer's dotted-map note, which names maps drawn by both parties, softened this for Ray and Luis. No concept removed it.
4. **A plain sentence about the evidence answered "how sure" best.** Readers used Explainer's "Official statistic: what survey respondents reported" and "Conditional directions: no forecast and no odds" word for word. Register's "secondary compilation" and Instrument's record codes gave them nothing to repeat.
5. **The S06 title set how the right-leaning readers judged a whole concept.** Explainer's title, which leads with the condition and names no plan, kept Luis reading. Instrument's title naming "the federal package and capacity first" and Register's "ALL FOUR UP" badges read to Luis and Tom as endorsements.
6. **Small gray source and note text on Newsprint** was hard for Keisha and Luis in all three concepts.

## Where the panel split

1. **Codes and downloads.** Tom wanted Instrument's record keys and CSV buttons. Ray, Keisha, Luis and Maya read them as clutter ("a parts number", "a lab requisition").
2. **The printed rule for "toward voters".** Dana and Luis wanted it on the face of the chart, and only Instrument and Register's S03 print it. Reading it lowered Ray's and Luis's trust in the coding and raised their trust in the publisher's openness. Keisha and Maya skipped it.
3. **Register's numbered notes and tables.** Dana, Keisha and Tom learned the most from them: cloture, the two poverty measures, the bans by year. Ray, Luis and Maya found Register long and small on the phone.
4. **Sharing S08.** Maya would share Explainer's S08; Ray and Luis would share it in no concept. Maya's takeaway, "going backward under Trump", goes further than any version of the chart says.
5. **The red dot on S02** (Explainer and Register) helped Keisha find the point, and also read to her as cheering for the credit.

## The five changes that would help most

1. **Say what "the atlas" is on every chart drawn from it, and take internal words off the face of the chart.** One plain phrase in the measure or source line, such as "Oath & Action's own record of 64 rule changes", would have answered Ray, Keisha, Luis and Maya. Move record codes (RL47, PW12, N40, E01) into the table, and replace studio words with reader words: "Charcoal" and "Stone" (Instrument S02), "Verdigris" and "Prussian" (Register S06), "refused an automated read" (Register and Instrument S07), "secondary compilation", "Light fills fall under 3:1" (Register S10). Applies to all three.
2. **Put the rule for "toward voters" and "away from voters" on the face of S03 and S08, with an example from each party.** One or two plain sentences, plus one change coded each way from each side, as Explainer's dotted-map note begins to do. Explainer folds the rule away, Register's S08 lacks it, and Instrument prints it with no examples.
3. **Keep the S06 title to the condition and a neutral count.** Drop plan names from the title (Instrument) and the "ALL FOUR UP" badges (Register), and say in one line who wrote the scenarios. Explainer's title is the model the panel accepted.
4. **Make the phone read fast.** Put the first chart on the first screen (Register's White page opens with three screens of index). Run small multiples full width (Register S05). Shorten the repeated number grids (Register S03 and S10). Give toward and away marks that differ by more than shade (Explainer S03, black against dark gray). Clear the label collisions (Explainer S08 "To 2012", Explainer S10 average line through row names). Raise source and note text size and contrast on Newsprint.
5. **Answer "who voted no" and "why 60" on S01.** Ray, Luis and Tom each asked for the party split of the House and Senate votes; show it in the same neutral ink if the record holds it. Dana asked why 53 votes fell short; Register's note 2 answers that, and the other two should carry the same line.

## What was tested

- Read `CLAUDE.md` and the "Reader panel" section of the red team brief.
- Measured each specimen's top edge and height on all three pages at 390 and 1440 px, White and Newsprint, in Playwright, and confirmed every page height matched its capture height.
- Cropped and viewed, for each concept: the White 1440 page head and S01, S04, S06, S07, S08 and S09; the White 390 page head and S01, S03, S04, S05, S07 and S08; the Newsprint 390 S02, S06 and S10, with S01, S03 and S08 viewed side by side across the three concepts; and the social card in two halves.
- Played six personas through four specimens each in each concept (72 specimen readings) and ranked the concepts per reader.

## What was not tested

- Real readers. One model played all six people.
- Ray's large text. The captures are at default size; reflow at his size is unknown.
- Anything behind "Show the table", "Show the table and notes", "How the atlas codes direction" or the Table switches, and the pointer readouts. The captures show these closed.
- The Charcoal views, the System view and its "How to read our charts", the 390 px social card and the grayscale captures. No reader was shown them.
- Widths of 360 px, a real Android browser, and a dim screen. Keisha's reading used the 390 px Newsprint capture.
- Whether any figure is correct. The panel quoted figures as shown and did not check them against the data.
- Legibility beyond the JPEG captures. Judgments about small gray text rest on compressed images at one pixel per CSS pixel.

## Change log

- Created: `work/handoffs/phase-2/20261106_Data-Viz-Reader-Panel.md` (this report).
- Modified: none.
- Working files (crops, the measuring script, notes) sit in the session scratchpad, outside the repo.
