# Stage B round 2: editor's notes

Oath & Action Edition 06, Phase 2, stage B, round 2, November 10, 2026. Written by the editor (`.claude/agents/oa-editor.md`) for the main session, chapter 10's maker, the engineer and the makers of chapters 09, 11 and 12. I committed nothing and published nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: items 1 to 3 are done. Item 4 waits for drafts: chapters 09 and 12 have no file yet, and chapter 11's file has not changed since stage A. One request to me has come in (Rule 01.21's kicker, below).

## What I wrote

### 1. Labels and meaning sentences for chapter 10

`work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json` holds 124 rows, CL-001 to CL-074 and R-01 to R-50, in ID order. Each row carries the ID, the Civic Line word, its class, the V7 ID with its typed chip (such as "Variable B3"), V7's title and short name, the label chapter 10 prints under DR-185, where the label came from, one meaning sentence, and whether the drawing is a master or a drawing Dustin approved by name on the drawings board. CL-025 also carries `label_where_atlas` and `meaning_where_atlas`. R-35 carries `rejected: true`.

How the labels follow DR-185:
- **Topic symbols (19) print their Civic Line word** in sentence case: Public meeting, Feedback loop, Contact an official. The words are the inventory's; only the capitals change.
- **The four pillar icons print their names**, Explain, Track, Connect and Act, and chapter 09 governs them.
- **Atlas variables (51) print V7's name.** Where V7 holds a short name for the variable, the name it uses on its loops, the label is that short name (25 of 51, among them "Congressional capacity" for D1, as DR-185 sets). Where V7 holds no short name, the label is V7's title (26 of 51, such as "Where newly created credit goes" for EC5).
- **Reforms (50) print V7's title**, except the two DR-185 sets: R-13, "Congress’s own experts", and R-36, "Lasting public investment". R-35's title, "Rejected option: term limits for legislators", keeps the word Rejected with the drawing wherever it appears.
- **CL-025 has two labels:** "Congress" as a topic and "Congressional capacity" where it stands for D1.

How the sentences are written:
- One full sentence each, saying what the drawing shows and what it stands for, as each is drawn now. The six redraws and the two new drawings are described from the approved SVGs (DR-156 to DR-160), which I rendered and looked at, and from the notes in `civic-line-v6/20261110_Civic-Line-V6-Inventory.csv`.
- Parts are named by their shape, never by color, so each sentence holds for the one-color edition under 48 px, in a row where only the current drawing keeps its red, and in the Black files.
- An atlas symbol's sentence gives V7's meaning in plain words, and where V7's short name is a term of art it says what the term means, as in "affective polarization, how strongly people dislike supporters of the other party" (H02).
- Sentences run from 11 to 35 words, median 23. Their first two words differ in 102 of 124, and 69 take the caption shape "a drawing, for its meaning"; the other 55 say it with "stands for", "shows", "marks" or the meaning first.

Chapter 10's maker has the file, and the construction notes already point to it (`20261110_Stage-B-Ch10-Construction.md`, section 10). Labels for chapter 10's maker to watch:
- Some labels run long under a 48 px drawing, up to 57 characters ("Popular-vote compact and constitutional amendment options"). Two lines under the drawing hold them.
- Six of V7's short names are terms a newcomer will not know on sight: Sanction applied (C5), Affective polarization (B4), Executive unilateralism (D2), Doctrine favoring the appointing coalition (D3), Warranted trust (E2) and Primary decisiveness (C2). DR-185 prints them, and each meaning sentence explains its term. I flag them for round 3's red teams.

The readable table follows the routine calls, at the end of these notes.

### 2. Rule 01.11's map count (DR-149)

I applied the research lead's section 3 draft to Rule 01.11's plate, `work/build/guide/specimens/s-01-11-correct.html`, under the two cases. The plate now reads:

> Our systems atlas records eight new congressional maps passed between censuses in 2025 and 2026. Republican-led legislatures or commissions passed seven, and California’s Democratic-led legislature passed one, which voters approved. Virginia’s Democratic-led legislature sought a ninth through a constitutional amendment, and the state’s supreme court struck the amendment down after voters approved it.

A second source line follows the cases' line:

> Source for the count: Oath & Action’s systems atlas, Who Do They Answer To?, its records for Loop R4a and its log of rule changes, snapshot of October 15, 2026; congressional maps passed between censuses, January 2025 to October 2026; United States. Retrieved November 10, 2026. Each map is counted by the party that led the legislature or commission when it passed. Ohio’s map came from the state’s redistricting commission under a deadline in the state constitution. The Missouri Supreme Court suspended the state’s map for 2026 ahead of a referendum on it held November 3, 2026, after the snapshot. A court adopted Utah’s map, so the count leaves it out. The count measures maps passed and says nothing about the seats they moved.

The same words went into chapter 01's JSON (the correct and failure captions, and the source list) and the plate's alt text in `manifest-editor.json`. Two changes from the research draft, each logged below: Virginia's sentence names the amendment, since the atlas records an amendment and no map, and Missouri's referendum reads as held, since November 3 has passed.

**Every figure, checked by script against the full Atlas V7 model** (`work/extract/atlas-v7-data.json`):

| Figure | Where V7 holds it | Holds |
|---|---|---|
| Eight new maps | Texas RL38, Missouri RL40, California RL41, Florida RL53, Tennessee RL54, Louisiana RL56; North Carolina and Ohio in connection L56, issue I022 and reform R-04's problem evidence | Yes |
| California's one, approved by voters | RL41: Proposition 50, 64.42 percent, November 4, 2025 | Yes |
| Virginia's attempt struck down | RL50: amendment approved April 21, 2026; RL55: voided 4 to 3 on May 8, 2026 | Yes |
| Utah's map adopted by a court | RL45: Judge Gibson adopted the plaintiffs' map, November 10, 2025 | Yes |
| Missouri's suspension | RL60: the Missouri Supreme Court, 7 to 0, September 3, 2026; RL61; RL63 records Proposition A as pending on November 3, 2026 | Yes |
| January 2025 to October 2026 | The earliest map is Texas's, August 2025; the snapshot is October 15, 2026 | Yes |

**Which party led each body, and how far that is checked** (research section 3's own "How I checked" column):
- Texas: the atlas states it.
- California: a court record and the Assembly's member list.
- Missouri and Louisiana: the House member lists, read on each legislature's own site.
- Florida: inferred from the atlas's own vote note (five Republicans opposed the map), not read on the legislature's site.
- North Carolina: not checked. The atlas calls the state a unified government; search results say its governor is a Democrat and that the map needed no signature from him.
- Tennessee: not checked. The member directory returned no list to a script.
- Ohio: not checked beyond search results. That the commission has a Republican majority is the research lead's understanding.
- Virginia: the atlas calls the amendment Democratic-backed.

**Figures that rest on search results only:**
- **Ohio.** That the state constitution set the deadline that required a new map, which the source line prints. That the commission voted unanimously with members of both parties, which the plate leaves out. That the commission has a Republican majority, on which the seven rests.
- **Missouri.** The result of the November 3, 2026 referendum. Missouri's results site refused the research lead's request, so the line says only that the vote was held after the snapshot. Missouri's suspension rests on the atlas, and the legislature's party on its member list.

### 3. The combined reader check's questions

`work/handoffs/phase-2/20261110_Reader-Check-2-Questions.md` sets the whole check in 11 steps, about 15 minutes, with every word a reader sees, the answer choices and their codes, what counts as a pass and why each question is asked, then the record's new fields, what the answer key holds, the words the page must never print, and the two-line invitation.

- **Kept from the first check:** the overview, R10 and B4 with their questions; four of the eight symbols; the three charts; the three sentence pairs; the welcome and the end. Nobody has answered them yet, since the first link was never sent (DR-143).
- **Left out:** the masthead question (DR-115, D2-323), the condensed wordmark and the 16 px badge on the small marks sheet (DR-115, DR-118), and the four pillar icons shown bare for naming (DR-111 sets each with its word).
- **New:** a link card and R-46 for reading Pillar Red for party (DR-114, DR-152); the pillar row at 24 and 48 px (DR-111, DR-133, DR-179); five questions on the six tracker steps (DR-108); a rebuilt small marks sheet and the 24 px lockmark in a footer (DR-181); the end mark at 14 and 12 px under two real sentences from the atlas (DR-180).

The invitation, for Dustin to paste:

> Could you spare about 15 minutes on your phone for a short test of a draft design for a civic publication? You’ll look at some drawings, charts and pages and say what you see, and there are no wrong answers: [link]
>
> It asks only for a first name or initials, and you can stop at any time. If the last screen shows your answers with a Copy button, please paste them into a reply to me.

### 4. Words for chapters 09, 11 and 12

Nothing to edit yet: `09-pillar-icons`, `10-symbols` and `12-graphic-devices` have no chapter file, and `11-icons.json` is unchanged since stage A. One request has come in from chapter 10's maker, on Rule 01.21's kicker in chapter 01, which sets CL-055 Productivity at 24 px although CL-055 is not among the 41 that read at that size. The drawing in `s-01-21-correct` is the identity designer's this round (D2-719), and the words are mine. My answer is the word change below; the identity designer swaps the drawing to CL-057, and I change the caption and alt text in the same pass so the page never shows one without the other.

| File | Field | Old | New | Rule |
|---|---|---|---|---|
| `work/build/guide/specimens/s-01-21-correct.html` (identity designer applies) | The Analysis kicker's topic word, after the icon | Productivity | Workers’ share of income | DR-112, a topic icon sits beside its own word; D2-373, a kicker's icon comes from the 41; DR-185, CL-057's word is V7's title for EC3 |
| `work/build/guide/chapters/01-purpose.json` (editor applies with the swap) | Rule 01.21, `correct.caption`, second sentence | the Productivity icon beside its own word | the icon for workers’ share of income beside its own words | Follows the swap |
| `work/build/guide/specimens/manifest-editor.json` (editor applies with the swap) | `s-01-21-correct.alt` | Analysis, productivity, with the Productivity topic icon, a worker at a desk beside a clock, directly before the word Productivity: Does pay rise with productivity? | Analysis, workers’ share of income, with its topic icon, a person in the wedge cut from a circle, directly before those words: Does pay rise with productivity? | Follows the swap |

The headline, "Does pay rise with productivity?", and its source stay: the share of income paid to workers is the measure that question turns on.

## Routine calls

Numbers left for the main session to assign.

Labels and meanings (item 1):
- D2-xxx | Chapter 10 prints every topic word in sentence case (Public meeting, Contact an official), keeping the inventory's words | V7 writes its names in sentence case, so one case runs across a contact sheet; file names keep the inventory's title case (D2-714)
- D2-xxx | An atlas variable's label is V7's short name where V7 holds one (25 of 51), and V7's title where it holds none (26) | DR-185's own example for D1 is the short name, "Congressional capacity", and research section 2 confirmed the 25 against V7's loops; I confirmed them again against the full model
- D2-xxx | A reform's label is V7's title, except R-13 and R-36, which DR-185 sets | V7 holds no short name for a reform, research section 2 puts V7's title on the page, and the atlas editorial data's `short` field holds the studio's own wording
- D2-xxx | R-35's label is V7's title, "Rejected option: term limits for legislators" | It keeps "Rejected" with the drawing, as DR-185's brief asks, and needs no middle dot
- D2-xxx | Meaning sentences name parts by shape, never by color | Each then holds for the one-color edition under 48 px, rows where only the current drawing keeps its red, and the Black files (R10, DR-66, DR-67)
- D2-xxx | CL-025 carries two labels and two sentences, one for the topic and one for D1 | DR-185
- D2-xxx | Each atlas row carries a typed chip for its V7 ID, "Variable B3" or "Reform R-01" | H11 and the Master Brief's tension 7: no bare ID on a reader page
- D2-xxx | Labels and sentences use typographic apostrophes, and `v7_title` keeps V7's straight ones | The guide prints typographic marks, and a matching script needs V7's own characters
- D2-xxx | CL-027's sentence says the atlas proposes the pattern | V7 calls D3 "a proposed pattern read across decisions" (W20, H08)
- D2-xxx | CL-061's sentence says an arrow "joins" a person and an envelope | It names what is drawn without reading a direction into income, which research section 2 found reads as sending mail
- D2-xxx | CL-073 and CL-074 sit after CL-072 and before R-01, on sheet 01 | D2-714
- D2-xxx | The research notes' count of "22" symbols with no V7 element is 21: 17 topic drawings and the four pillar icons. With CL-073 and CL-074 the topic and pillar rows come to 23 | Counted by script against the icon map

Rule 01.11 (item 2):
- D2-xxx | The plate's count is the research lead's draft line, with Virginia's sentence recast to name the amendment | The atlas records an amendment that voters approved and the state's supreme court voided (RL50, RL55), and no map
- D2-xxx | The count's source line says Missouri's referendum was held November 3, 2026, after the snapshot, in place of "pending" | The vote has happened and its result is not checked; the line stays true whatever the result
- D2-xxx | The count takes its own source line, "Source for the count:", after the cases' line, and chapter 01's source list gains the same entry | H04; the cases and the count differ in publisher and period
- D2-xxx | The count's line reads "Retrieved November 10, 2026" | I checked every map against the full Atlas V7 model that day
- D2-xxx | Rule 01.11's failure caption names what a Texas-only plate drops, California's case and the count | With the count printed, the old caption's "reads as a charge against one party" no longer named the fault, since the record does lean one way (DR-93)

The reader check (item 3):
- D2-xxx | The four pillar icons leave the bare naming step, and step 5 tests them in rows with their words | Since November 7 every pillar icon sits with its word (DR-111); the first check was written the day before
- D2-xxx | The small marks sheet drops the condensed wordmark and the 16 px badge, takes the 16 px pillar fits, and adds the rebuilt 24 px lockmark and the pillar icons at 24 px | DR-115, DR-118, DR-179, DR-181
- D2-xxx | The red step comes before the pillar rows, the tracker and the charts | The first question about party then meets the brand's red before any other question names party
- D2-xxx | R-46 shows without its label | The bare drawing is the hard case for DR-152's question; chapter 10 always sets it with its label
- D2-xxx | The tracker and end mark questions keep their picture on screen, with no timer | People read a tracker or an article ending at their own pace
- D2-xxx | The tracker's mark questions hide the bill's words and the key, and the dot question also passes "Not sure" | They ask what each shape says alone; the dot's meaning is always printed beside it (Rule 11.4)
- D2-xxx | The end mark sits under two sentences quoted word for word from Atlas V7's pathway PW03 | Real lines need no Illustrative label and hold no statistic; the same answer's first line stays out, since the sentence pairs test our rewrite of it (W02)
- D2-xxx | The record adds `device_pixel_ratio` | Pixel fits are drawn for 1x screens, so what a reader saw depends on the screen
- D2-xxx | Meaning choices shuffle per reader with "Not sure" last; scales, step numbers and the party choices keep one order | Position can sway a meaning answer; the party choices keep the first check's order so answers compare across steps
- D2-xxx | The invitation says about 15 minutes | The estimate runs from 11 to 15 minutes, so the invitation promises the longer end

## Questions for Dustin

1. **The check runs about 15 minutes.** The first check was estimated at 9 to 10 (DR-86), and this one adds DR-143's five topics. *Recommendation:* keep it whole and say 15 minutes in the invitation. If you want it near 12, the four-symbol naming step can go, which saves about 2 minutes.
2. **Should the new Congress, Testify and Contact an official drawings join the symbol naming step?** DR-143 names no new Civic Line drawing, and each adds about half a minute. *Recommendation:* leave them out of this check, so it stays near 15 minutes; the creative director's naming reads on the drawings board stand for now.
3. **If Missouri's voters rejected the 2025 map on November 3, what does the plate count?** Research D2-525 counts the map as passed, with its suspension explained. A map voters turned down would read more like Virginia's attempt. *Recommendation:* once Missouri's certified result is read, report the record as it stands (DR-93): if voters rejected the map, the plate counts six maps from Republican-led bodies and names Missouri's beside Virginia's; if they approved it, the plate stands as written.

Requests to other owners:
- **Research lead:** before board B, read Missouri's certified Proposition A result, Ohio's constitution on the 2025 deadline and the commission's October 31, 2025 vote, and the member lists for North Carolina, Tennessee, Ohio and Florida, so every party in the count rests on a primary source.
- **Identity designer:** the kicker swap in `s-01-21-correct` above.
- **Engineer:** build the page from `20261110_Reader-Check-2-Questions.md`; its "Answer key" section lists what the key file holds.

## Tested

- The labels file by script: it parses; 124 rows in ID order, CL-001 to CL-074 then R-01 to R-50, no repeat; every row has a label and one meaning sentence ending in a period; every Civic Line word matches `civic-line-v6/20261110_Civic-Line-V6-Inventory.csv` exactly (124 of 124).
- Every V7 ID, title and short name read from the full model (`work/extract/atlas-v7-data.json`): 51 variables mapped to 51 drawings through the icon map, 50 reforms, 25 short names from the loops' chain labels, each variable with one short name at most.
- My words in the labels file, by script: no em or en dash, no straight quote, none of the listed fillers or corporate verbs, no "not" or "never", no color word in a meaning sentence, no figure under ten in a sentence.
- The eight changed drawings rendered from their approved SVGs in Chromium and looked at; all 122 October drawings looked at on two contact sheets; my sentences compared with the v6 inventory's notes on the eight.
- Rule 01.11: every figure in the count against V7's records (the table above); the build (`guide_build.py --strict`: 9 chapter files, 100 rules, 233 specimens, 0 placeholders); the plate looked at in the built guide at 1,440 and 390 px; the chapter JSON and the editor manifest parse and change only in the fields named.
- The reader check file: the PW03 lines match V7's text exactly; the first check's question words and rating labels compared with its template; the answer counts (54) and fixed looking time (175 s) added up by hand; a scan for dashes, fillers and negations, each hit read.
- A full read of all three files against chapter 02's rules.

## Not tested

- How the labels and sentences read aloud to real readers, and how they fit chapter 10's contact sheets, which do not exist yet.
- Whether the 24 px lockmark, the pixel fits and the end mark look as these questions assume on real phones; the questions are written from the decisions and the specimens, not from phone captures.
- The reader check page, which the engineer builds; the time estimate, which no reader has measured.
- The party attributions the research lead marked as not checked (North Carolina, Tennessee, Ohio, Florida), and Missouri's referendum result.
- My notes' prose for rhetorical triplets and parallel runs, which no script can rule out; I read for them.

## Change log

Created:
- `work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json`
- `work/handoffs/phase-2/20261110_Reader-Check-2-Questions.md`
- `work/handoffs/phase-2/20261110_Stage-B-Round-2-Editor-Notes.md` (this file)

Modified:
- `work/build/guide/specimens/s-01-11-correct.html`: the count paragraph, its source line and the header comment
- `work/build/guide/chapters/01-purpose.json`: Rule 01.11's correct and failure captions; the count's source in the chapter's source list
- `work/build/guide/specimens/manifest-editor.json`: `s-01-11-correct`'s alt text and notes

Scratch only, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/round-2/editor/`: the label build and check scripts, contact sheets, the built guide and its plate captures, and backups of the three chapter 01 files before my edits.

## Labels and meaning sentences, readable table

The JSON governs; this is the same text. V7 is the atlas ID where the drawing stands for an atlas element.

| ID | Label chapter 10 prints | V7 | Meaning sentence |
|---|---|---|---|
| CL-001 | Voting |  | A ballot going into a ballot box is the sign for casting a vote. |
| CL-002 | Representation |  | One person at a lectern between two others stands for an official chosen to speak for the people around them. |
| CL-003 | Registration |  | An ID card carries a check badge on its corner, for signing up to vote and getting on the voter list. |
| CL-004 | Petition |  | A pen rests on a lined page, ready to sign a petition that asks officials to act. |
| CL-005 | Public meeting |  | A speaker at a lectern with two residents in front shows a public meeting that anyone may attend. |
| CL-006 | Cross-cutting civic ties | B3 | Three open arcs link three people, for cross-cutting civic ties, the bonds that shared work builds across party or income lines. |
| CL-007 | Turnout equality | B5 | Three people of equal height, each holding a marked ballot, show how evenly people vote across income groups. |
| CL-008 | Affective polarization | B4 | Two speech bubbles turn away from each other around a lightning bolt, for affective polarization, how strongly people dislike supporters of the other party. |
| CL-009 | Safe seats | C1 | A chair inside a stepped district line marks a safe seat, a district one party wins by a wide margin. |
| CL-010 | Primary decisiveness | C2 | Three paths narrowing into one channel toward a single circle show how often the primary settles who takes office. |
| CL-011 | Electoral pressure | C3 | An arrow runs from an officeholder at a desk toward a ballot box, for the credible chance that an incumbent loses the next election. |
| CL-012 | Incumbent control of election rules | C4 | A page of rules carries two sliders, for the power people in office hold to set district maps, voting rules and other election choices. |
| CL-013 | Sanction applied | C5 | An empty office chair with an arrow leading away marks officeholders who lose an election or retire under threat of defeat. |
| CL-014 | Entrenched majority control | D7 | A ballot’s arrow stops at a bar on the fence around a chamber, for a majority’s lasting hold on a legislature or another body that sets the rules, which the next election cannot easily break. |
| CL-015 | Money in politics | B1 | A path carries money from a dollar coin into a ballot box, for campaign gifts, outside spending and paid lobbying used to sway public decisions. |
| CL-016 | Lobbying |  | Two people meeting across a table over one paper show lobbying, paid work to persuade officials. |
| CL-017 | Policy tilt to insiders | E1 | A page of rules sends a route to each of three people, for policy that tilts toward wealthy and organized interests. |
| CL-018 | Warranted trust | E2 | A check badge sits in front of three people, for warranted trust, confidence in institutions that rests on how competently and honestly they act. |
| CL-019 | Explain |  | Three short rays rise from an open book, the icon for Explain, our pillar that makes the rules and their effects understandable. |
| CL-020 | Track |  | Track’s icon runs a route from a map pin to a magnifier, because Track follows a decision and keeps its record within reach. |
| CL-021 | Connect |  | Two overlapping rings stand for Connect, which helps people reach the office that decides and the evidence it decides on. |
| CL-022 | Act |  | A finger pressing a round control marks Act, the pillar that gives a reader a useful next step. |
| CL-023 | Evidence |  | Evidence, the record a claim stands on, appears as a magnifier with a check in its lens resting on a page. |
| CL-024 | Feedback loop |  | Two arrows carry a change from one box to another and back again, for a feedback loop, a chain of causes that returns to where it started. |
| CL-025 | Congress (as D1: Congressional capacity) | D1 | A chamber in session, seen from the gallery, with members on a curved bench below a three-tier rostrum, stands for Congress. Where it stands for the atlas element, the same chamber means congressional capacity, the staff and expertise Congress needs to investigate problems, write laws and oversee agencies. |
| CL-026 | Executive unilateralism | D2 | An official at a desk sits beside a signed order, for executive unilateralism, a president setting policy through orders or emergency powers without a new law. |
| CL-027 | Doctrine favoring the appointing coalition | D3 | A balance scale stands before a sealed ruling, for a pattern the atlas proposes in which courts rule for the coalition that appointed the judges. |
| CL-028 | Oversight and enforcement | D4 | A magnifier with an empty lens over part of a record stands for the power watchdogs have to obtain records, investigate wrongdoing and get a response. |
| CL-029 | Public service quality | D5 | A staff member serving a visitor across a counter shows how reliably government delivers the services people use. |
| CL-030 | State and local experimentation | D6 | Two small test results join and lead down to a check, for states and towns that try a policy and learn from its results. |
| CL-031 | Local government |  | A low town hall with a tall central doorway stands for local government, the city, county and town offices closest to home. |
| CL-032 | Local news supply | B2 | A folded newspaper with a story block in its corner shows the reporters and newsrooms that cover local decisions. |
| CL-033 | Hostile-content exposure | B6 | A laptop screen holds a heated post beside a warning sign, for how often people see political material that attacks the other party. |
| CL-034 | What new technology can do | X1 | A wire running from a lightbulb to a circuit point stands for technical advances that change which tasks machines can do and how much workers produce. |
| CL-035 | Population patterns and residential sorting | X2 | Two clusters of houses on either side of a dashed line show where people live and how communities differ by age, education or party. |
| CL-036 | Trade and the movement of capital | X3 | Two parcels and a dollar coin sit between arrows that run both ways, for goods, investment and wealth moving across borders. |
| CL-037 | Foreign interference | X4 | A globe sends signals toward a ballot box marked with a warning, for documented efforts by foreign actors to sway U.S. politics. |
| CL-038 | Major external shocks | X5 | A burst breaks a winding road, for shocks from outside such as wars, pandemics and climate disasters, which strain households and public institutions. |
| CL-039 | How platforms rank feeds and seek attention | TC1 | A slider beside three stacked posts picks out the middle one, for the choices platforms make about which posts people see. |
| CL-040 | Concentration of platforms and digital advertising | TC2 | One ring branching down to three people shows how much of digital advertising and distribution a few platforms hold. |
| CL-041 | Use of AI at work | TC3 | A worker at a laptop beside a small robot shows workers and employers putting AI to use in their jobs. |
| CL-042 | Concentration of AI funding and computing power | TC4 | Three servers feed into one circle marked with a dollar sign, for how much of the money and computing power behind AI sits with a few firms. |
| CL-043 | Government’s ability to build and run digital services | TC5 | A browser window sits in front of a town hall, for the public teams and skills that deliver government services through reliable software. |
| CL-044 | Data centers’ demand on the electricity grid | TC6 | A stack of servers beside an electric plug stands for the power and grid capacity that data centers need. |
| CL-045 | Use of pricing algorithms | TC7 | Two price tags beside a small circuit mark software that sellers and landlords use to set prices. |
| CL-046 | Computing capacity built for AI | TC8 | A microchip sits next to a stack of servers, for the data centers and specialized chips built to train and run AI. |
| CL-047 | Data rights |  | A key across a page of records stands for people’s rights over the data held about them. |
| CL-048 | Public records |  | Public records, which anyone can ask a government to release, appear as a page rising out of an open folder. |
| CL-049 | Wealth concentration | A1 | Three coin stacks rising from short to tall show the share of household wealth held by the households at the top. |
| CL-050 | Worker bargaining power | A2 | A two-way arrow runs between two people across a table, for workers’ power to negotiate pay and conditions, alone or together. |
| CL-051 | Market concentration | A3 | One tall building towering over two small ones shows how much of a market a few firms control. |
| CL-052 | Household security | A4 | A paper marked with a dollar sign leans on a house, for a household’s ability to meet basic needs and absorb an unexpected expense. |
| CL-053 | Housing scarcity | A5 | Between two houses, a dashed outline marks the home that is missing, for a shortage of homes where people need to live. |
| CL-054 | Owner home equity | A6 | A rising chart against a house marks the value owners hold in their homes after mortgage debt. |
| CL-055 | Output produced per hour of work | EC1 | An arrow runs from a worker at a laptop to a clock, for how much a worker produces in an hour. |
| CL-056 | Public investment in research and infrastructure | EC2 | A lightbulb glows above a suspension bridge, for government money spent on research and on the systems the economy runs on. |
| CL-057 | Workers’ share of income | EC3 | A person fills the wedge cut from a circle, for the part of business income paid to workers. |
| CL-058 | Concentration of stock ownership | EC4 | A stock certificate stands beside three rising bars, for how much of the stock households own belongs to the wealthiest. |
| CL-059 | Where newly created credit goes | EC5 | A path from a bank with a round vault door splits toward a home and a factory, for where new money goes when banks lend. |
| CL-060 | Net support from taxes and public benefits | EC6 | Two arrows run opposite ways beside a page of records, for what households receive in public benefits set against what they pay in taxes. |
| CL-061 | Household income | EC7 | Household income, the money a household receives over a period from pay and other sources, appears as an arrow joining a person and an envelope. |
| CL-062 | Household assets and debts | EC8 | Two coin stacks in front of a page with a minus sign show what households own and what they owe. |
| CL-063 | Cost of essentials | EC9 | A grocery bag and a price tag sit in front of a house, for what households pay for necessities such as housing, groceries and insurance. |
| CL-064 | Costs of tariffs and trade rules | EC10 | A parcel meets a gate with two bars across it, for import taxes and trade rules that can raise what U.S. buyers pay. |
| CL-065 | Climate hazards and insurance costs | EC11 | Rain falls on a house beside an insurance page with an umbrella on it, for the risk of climate damage and the cost of insuring against it. |
| CL-066 | Energy demand and emissions | EC12 | A plug’s cable curling into a cloud of emissions stands for the energy the economy uses and the greenhouse gases it releases. |
| CL-067 | Healthcare |  | A heartbeat line through a medical cross stands for health care, from coverage to getting treatment. |
| CL-068 | Education |  | A small lightbulb rising from an open book stands for schools and learning. |
| CL-069 | Childcare |  | An adult’s arm curving around a child stands for childcare and the people who provide it. |
| CL-070 | Environment |  | A leaf beside a drop of water stands for the environment. |
| CL-071 | Policy |  | A slider running out of a page of rules means policy, the settings a government chooses and can change. |
| CL-072 | Reform |  | Of three paths from one start, the middle one bends up to an arrowhead, for reform, a change that sends a rule in a new direction. |
| CL-073 | Testify |  | A witness at a table speaks into a microphone below three officials on a raised, curved dais, for testifying at a public hearing. |
| CL-074 | Contact an official |  | One line carries a speech mark from a person to an official at a desk, for calling, writing to or visiting the office of someone who represents you. |
| R-01 | All-party primaries with ranked general elections | R-01 | Paths from three voters meet at one checked ballot, for a first round open to every voter, whatever their party, followed by a ranked general election. |
| R-02 | Ranked-choice voting for single-winner races | R-02 | A ballot that ranks three candidates in order stands for voters ranking candidates by preference in a race with one winner. |
| R-03 | Proportional elections in multi-seat House districts | R-03 | Seat dots fill a half ring, for larger House districts that each elect several members, with seats shared in proportion to votes. |
| R-04 | Independent citizen commissions draw election maps | R-04 | Three residents before a map split into districts stand for independent citizen commissions that draw election maps. |
| R-05 | Automatic voter registration | R-05 | A check badge marks an ID card, for registering eligible people to vote when they deal with a state agency, unless they opt out. |
| R-06 | Hold local elections alongside November races | R-06 | Two calendars joined by an arrow and marked on the same date stand for holding city and county elections on the November ballot with state and national races. |
| R-07 | Public matching for small donations and vouchers | R-07 | An arrow runs from a short coin stack to a tall one, for public money that multiplies small donations, or vouchers that voters give to candidates. |
| R-08 | Disclose the original funders of political spending | R-08 | A magnifier sits over a page marked with a dollar sign, for requiring groups that spend on elections to report who paid. |
| R-09 | Ban stock trading by members of Congress | R-09 | A slash across a stock certificate stands for barring members of Congress from trading individual stocks. |
| R-10 | Limits on lobbying and the revolving door | R-10 | A figure walks out a door toward an office building past a no-entry sign, for waiting periods before former officials can lobby the offices they left. |
| R-11 | A Federal Election Commission able to act | R-11 | A gavel lies beside a ballot record with a checked box, for a Federal Election Commission with enough commissioners to enforce campaign-finance law. |
| R-12 | Senate filibuster reform | R-12 | An open padlock between two speech bubbles above a chamber rail shows a Senate majority able to pass ordinary bills without first gathering 60 votes to end debate. |
| R-13 | Congress’s own experts | R-13 | Two staff members and an analyst’s report with a rising chart line sit below a chamber in session, for Congress hiring and keeping more of its own analysts and experts. |
| R-14 | Automatic funding to prevent government shutdowns | R-14 | A funding arrow runs through a budget record and out the other side, for funding that continues at the prior year’s level when Congress misses a budget deadline. |
| R-15 | Inspectors general with remedies that work | R-15 | A magnifier, its handle to the lower left, holds a check over a page, for inspectors general, the watchdogs inside federal agencies, with remedies that work when officials obstruct them. |
| R-16 | Supreme Court 18-year terms and enforceable ethics | R-16 | A clock hangs under a balance scale beside a check badge, for 18-year terms for Supreme Court justices and an ethics code with a way to enforce it. |
| R-17 | Protect the career civil service | R-17 | A brace guarding one side of an employee ID card stands for protecting career federal workers from being fired for political reasons. |
| R-18 | Expiring emergency powers and enforced spending law | R-18 | A clock sits over the corner of an order, for emergency powers that end unless Congress renews them, and spending law enforced on time. |
| R-19 | Rules for drug-pricing middlemen (PBMs) | R-19 | Two capsules lean against a price tag, for rules on pharmacy benefit managers, the companies that run drug benefits for insurers and employers. |
| R-20 | Merger enforcement for consumers and workers | R-20 | A magnifier looks at two groups of company buildings joined by an arch, for agencies that block mergers that would raise prices or cut wages. |
| R-21 | Faster labor-law remedies and first-contract arbitration | R-21 | A worker in a hard hat stands before a document with a check badge, for faster remedies when workers are fired for organizing, and an arbitrator who sets a first contract. |
| R-22 | Industry-wide wage boards and sector bargaining | R-22 | Three people meeting around one table show a board of workers and employers that sets wage and safety floors for a whole industry. |
| R-23 | Minimum wage that rises with an index | R-23 | A curved arrow climbs over a wage record and its bar chart, for a minimum wage that rises each year with a published measure of prices or wages. |
| R-24 | Paid family and medical leave insurance | R-24 | An adult and a child stand before a calendar marked with a dollar shield, for paid time off when a worker is ill, has a new child or cares for a sick relative. |
| R-25 | Full child tax credit for low-earning families | R-25 | An arrow points from a tax record and a dollar coin toward a child, for paying the full child tax credit to families who earn little or nothing. |
| R-26 | Recession aid that starts automatically | R-26 | A zigzag arrow falls over a home and two coin stacks, for benefits such as unemployment insurance that grow on their own when a recession starts. |
| R-27 | IRS enforcement of taxes already owed | R-27 | A tax record under a magnifier with a gauge in its lens stands for steady funding so the IRS can collect taxes already owed. |
| R-28 | Taxing inherited gains and capital income | R-28 | Coin stacks stand in front of a tax record with a dollar sign, for taxing gains on assets when their owner dies and taxing income from capital more like wages. |
| R-29 | Baby bonds: publicly funded child accounts | R-29 | A coin dropping toward a piggy bank beside a child shows a publicly funded savings account that each child receives early in life. |
| R-30 | More homes allowed by right near jobs | R-30 | Two houses stand beside a permit with a check badge, for allowing homes that meet clear, published rules near jobs without a separate hearing for each project. |
| R-31 | Childcare supply and pay for care workers | R-31 | An adult beside a small childcare center stands for public money that pays for childcare places and the wages needed to keep staff. |
| R-32 | Public and philanthropic funding for local news | R-32 | A stack of coins beside a newspaper stands for public and foundation money that pays for reporting on local government. |
| R-33 | Citizen assemblies that officials must answer | R-33 | Five people around an oval table make up a citizen assembly, residents chosen by lottery who study a public question and get a public answer from officials. |
| R-34 | Participatory budgeting: residents decide spending | R-34 | People stand in front of a checklist with boxes ticked, for residents who propose projects and vote on how to spend part of a city’s budget. |
| R-35 | Rejected option: term limits for legislators | R-35 | A disc with a cross over the clock behind an officeholder marks term limits for legislators, an option the atlas rejects because studies of state legislatures find that limits weaken how a legislature works. |
| R-36 | Lasting public investment | R-36 | A lightbulb, a bridge and a funding record stand in a row, for funding research and infrastructure over several years and protecting that money until projects are finished. |
| R-37 | Feed choice and data access for researchers | R-37 | A browser window with a slider stands beside a key, for letting users choose how their feeds are ranked and letting researchers study platform data. |
| R-38 | Limits on pricing software using rivals’ data | R-38 | A prohibition sign cutting the dashed link between two price tags stands for barring pricing software from using competitors’ private data to set prices. |
| R-39 | Government teams that build digital services | R-39 | Two people stand beside a screen holding an ID and a form, for the government’s own technology teams, who build the software people use to claim benefits, get tax refunds and apply for permits. |
| R-40 | Notice and a voice for workers on AI | R-40 | A worker speaks up beside a chip marked AI, for telling workers when AI helps hire, schedule or rate them, and giving them a say in how it is used. |
| R-41 | Large power users pay their grid costs | R-41 | A row of servers plugs into a bill marked with a dollar sign, for making large new power users such as data centers pay for the grid upgrades their demand requires. |
| R-42 | Congress votes on lasting tariffs | R-42 | A chamber in session sits above a vote card marked yes and no and a tagged parcel, for tariffs, taxes on imports, that last beyond a short period only if Congress approves them. |
| R-43 | Building codes and mitigation against disaster losses | R-43 | A house with a strengthened roof, under a storm and above floodwater, shows stronger building codes and upgrades that cut the damage when disaster strikes. |
| R-44 | Competition remedies for search and ad markets | R-44 | Two browser windows, each with a search magnifier, pass arrows both ways, for remedies that open search and online advertising to rival companies. |
| R-45 | Verifiable elections with paper records and audits | R-45 | Paper ballots under a magnifier with a check stand for elections in which every vote leaves a paper record and results are audited. |
| R-46 | Expand the House of Representatives | R-46 | Seats added along the outer row of a chamber seen from above show a larger House, where each member represents fewer people. |
| R-47 | Fusion voting and public funding for parties | R-47 | Lines from two candidate cards meet at one person between them, for letting more than one party nominate the same candidate, with public funding for parties. |
| R-48 | Agency independence after the Slaughter ruling | R-48 | An arrow from an official at a desk stops at a brace before a commission at its table, for Congress protecting independent agencies after the Supreme Court’s June 2026 ruling in Trump v. Slaughter. |
| R-49 | Civic work that crosses party lines | R-49 | An arc and a small bridge join two people, for groups that bring people of different parties together for shared work, such as serving as poll workers. |
| R-50 | Popular-vote compact and constitutional amendment options | R-50 | A brace gathers four ballots above a map of the United States, for the National Popular Vote compact and constitutional amendments that would change how presidents and senators are chosen. |
