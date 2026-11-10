# Stage B round 2: editor's notes

Oath & Action Edition 06, Phase 2, stage B, round 2, November 10, 2026. Written by the editor (`.claude/agents/oa-editor.md`) for the main session, chapter 10's maker, the engineer and the makers of chapters 09, 11 and 12. I committed nothing and published nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: items 1 to 3 are done, with Dustin's answers of November 10 applied (DR-187 to DR-189) and the research lead's round 2 findings on Rule 01.11 (section 2b). Item 4: chapter 10's words are done and applied by its maker (section 4a); chapter 09's (4b) and chapter 12's Rules 12.5 to 12.9 (4c) are done; Rule 01.21's kicker has landed. Chapter 11 has a first pass on its draft (4d), and its final pass and chapter 12's Rules 12.1 to 12.4 wait for their makers.

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

### 2b. Rule 01.11 after the research lead's round 2 notes and DR-187

The research lead's notes (`20261110_Stage-B-Round-2-Research-Notes.md`) found that Missouri's voters rejected the 2025 map on November 3, 2026, by unofficial returns; that Ohio's commission, five Republicans and two Democrats, adopted its map 7 to 0 on the constitution's deadline; and that every party the plate names now rests on a primary source except Virginia's 2025 House of Delegates. Dustin decided the plate counts maps passed, seven and one, with Missouri's rejection named and its figures marked unofficial (DR-187).

I applied section 5's four changes to `s-01-11-correct.html`, to `01-purpose.json` (Rule 01.11's correct caption and the count's source entry) and to `manifest-editor.json` (the alt text and notes), with two changes of my own:
- The plate's own sentence says the result is unofficial: "Missouri’s voters rejected their state’s map, one of the seven, on November 3, 2026, according to unofficial returns."
- The source line names the official page the figures come from, in full: "Its figures are unofficial statewide returns for Proposition A, November 3, 2026, 1,273,815 no and 785,969 yes, from St. Charles County, Missouri, “Voters Turn Out for 2026 Midterm Election in St. Charles County”, sccmo.org, November 4, 2026; the state certifies the count after local election authorities file theirs by November 17, 2026." I also put the counting sentence in the active voice ("We counted each map by the party that led...") and split the research draft's colon into two sentences (W06).

The number lives in one sentence of the plate (`R4A_SCOPE`'s second sentence), one of the caption ("seven to one") and the source line's last sentence, so a later change is three swaps. Before Phase 5, the Missouri figures and their page give way to the certified statement once Missouri's board of state canvassers issues it (research section 5, change 2).

**The chapter 01 generator now holds these words.** Chapter 01 and 02 are written by my generator, `work/build/scripts/phase-2/guide_editor_build.py` with `guide_editor_ch01.py`, and my earlier edits went into its outputs only, so a rebuild would have undone them. I moved every Rule 01.11 string into `guide_editor_ch01.py` (`R4A_SCOPE`, a new `SRC_R4A_COUNT`, both captions, the alt, the notes and the chapter's source list), with Rule 01.21's new caption and alt, and widened the build's own count check (BE-02) so it accepts a sourced count. Then I rebuilt chapters 01 and 02 and ran the identity designer's step, `python3 -I work/build/scripts/phase-2/stage_b_identity_ch01.py`, and compared all 115 files against the committed copies. Three differences remain, each intended or held back:
- Rule 01.21's caption and alt, the change below.
- The header comment in `s-01-11-correct.html` is back to the generator's standard line; the manifest's notes keep the plate's history.
- `s-01-pieces.html` came out with chapter 11's newer mark code, which is mid-build, so I restored the committed file. The next rebuild after chapter 11 lands picks the new marks up, as the generator intends.

**Rebuild order, my choice of the two the identity designer offered:** after every rebuild of chapter 01, run `stage_b_identity_ch01.py`. It touches only the inline masters and the kicker word, and a second run changes nothing, so the generator stays as it is and both owners' steps stay apart.

### 3. The combined reader check's questions

`work/handoffs/phase-2/20261110_Reader-Check-2-Questions.md` sets the whole check in 11 steps, about 15 minutes, with every word a reader sees, the answer choices and their codes, what counts as a pass and why each question is asked, then the record's new fields, what the answer key holds, the words the page must never print, and the two-line invitation.

- **Kept from the first check:** the overview, R10 and B4 with their questions; four of the eight symbols; the three charts; the three sentence pairs; the welcome and the end. Nobody has answered them yet, since the first link was never sent (DR-143).
- **Left out:** the masthead question (DR-115, D2-323), the condensed wordmark and the 16 px badge on the small marks sheet (DR-115, DR-118), and the four pillar icons shown bare for naming (DR-111 sets each with its word).
- **New:** a link card and R-46 for reading Pillar Red for party (DR-114, DR-152); the pillar row at 24 and 48 px (DR-111, DR-133, DR-179); five questions on the six tracker steps (DR-108); a rebuilt small marks sheet and the 24 px lockmark in a footer (DR-181); the end mark at 14 and 12 px under two real sentences from the atlas (DR-180).

**Dustin's answers (DR-188, DR-189).** The check keeps all eleven steps and says about 15 minutes in the invitation. Step 3 now names CL-025 Congress, CL-073 Testify, CL-074 Contact an Official and R-02 Ranked-choice voting, drawn from `civic-line-v6/black/`. **For the engineer: step 3's pass and partly rows for Congress, Testify and Contact an Official are in the questions file**, with the misreadings to report to Dustin for each (a court, a job interview and the like), what to expect from Congress (D2-620), and four more words to keep off the page up to the end of step 3.

The invitation, for Dustin to paste:

> Could you spare about 15 minutes on your phone for a short test of a draft design for a civic publication? You’ll look at some drawings, charts and pages and say what you see, and there are no wrong answers: [link]
>
> It asks only for a first name or initials, and you can stop at any time. If the last screen shows your answers with a Copy button, please paste them into a reply to me.

### 4. Words for chapters 09, 10, 11 and 12

Rule 01.21's kicker in chapter 01 set CL-055 Productivity at 24 px, although CL-055 is not among the 41 that read at that size (chapter 10's maker's request). The drawing in `s-01-21-correct` is the identity designer's this round (D2-719), and the words are mine. The identity designer has swapped the drawing to CL-057 beside "Workers’ share of income", and I have applied the caption and alt below, in the generator too (section 2b).

| File | Field | Old | New | Rule |
|---|---|---|---|---|
| `work/build/guide/specimens/s-01-21-correct.html` (identity designer, applied) | The Analysis kicker's topic word, after the icon | Productivity | Workers’ share of income | DR-112, a topic icon sits beside its own word; D2-373, a kicker's icon comes from the 41; DR-185, CL-057's word is V7's title for EC3 |
| `work/build/guide/chapters/01-purpose.json` (editor, applied) | Rule 01.21, `correct.caption`, second sentence | the Productivity icon beside its own word | the icon for workers’ share of income beside its own words | Follows the swap |
| `work/build/guide/specimens/manifest-editor.json` (editor, applied) | `s-01-21-correct.alt` | Analysis, productivity, with the Productivity topic icon, a worker at a desk beside a clock, directly before the word Productivity: Does pay rise with productivity? | Analysis, workers’ share of income, with its topic icon, a person in the wedge cut from a circle, directly before those words: Does pay rise with productivity? | Follows the swap |

The headline, "Does pay rise with productivity?", and its source stay: the share of income paid to workers is the measure that question turns on.

### 4a. Chapter 10's words, as built

I read `work/build/guide/chapters/10-symbols.json`, the class table in `s-10-1-correct`, the `LOOKALIKES` lines in `work/build/scripts/phase-2/stage_b_ch10_build.py`, the library's meaning lists and every `s-10-*` alt in `manifest-systems.json`. The chapter reads well, and its facts check: 7,626 pairs is every pair of 124, 3.35 is 1.25 times 2.68, and the library prints my labels and sentences as written. The script writes the chapter's JSON, so each change below goes into `stage_b_ch10_build.py` at the string quoted.

**Two changes in my own file, for chapter 10's maker to rebuild from** (`20261110_Stage-B-Ch10-Labels.json`):
- CL-064's sentence said "gate", which the guide check refuses on reader pages (D2-253). It now reads: "A parcel meets a checkpoint with two bars across it, for import taxes and trade rules that can raise what U.S. buyers pay." No other label or sentence matches any of the check's studio words, by script, and my build now runs those patterns.
- CL-025's second sentence printed in the library after its chip and its name, so it repeated both. It now reads: "The same chamber stands for the staff and expertise Congress needs to investigate problems, write laws and oversee agencies."

**Changes to the maker's words:**

| File | Field | Old | New | Rule |
|---|---|---|---|---|
| `10-symbols.json` | `intro[0]` | each on a square box. A topic symbol names the subject of a piece, such as Voting or Public records. An atlas symbol names a variable or a reform in our systems atlas. | each drawn in a square box. A topic symbol names the subject of a piece, such as Voting or Public records, and an atlas symbol names a variable or a reform in our systems atlas. | W13, two sentences on one frame; "on a square box" reads as sitting on top of it |
| `10-symbols.json` | `groups[2].line` | A drawing reads from 48 px, a short list reads at 24 px, and each surface takes its own edition. | Every drawing reads from 48 px and 41 of them at 24 px, and each surface takes its own edition. | W12, a three-beat chant; "a short list" gives no number |
| `10-symbols.json` | Rule 10.1, `rule[0]`, from its second sentence | Pillar icons mark which of our four pillars a piece serves. Topic symbols name the subject of a piece. Atlas symbols name a variable or a reform in our systems atlas, Who Do They Answer To?, where a variable is a condition that can rise or fall, such as safe seats. Status marks say where a bill or a record stands, and utility icons name an action beside its word. Encoding glyphs carry the atlas’s own marks for sign, evidence and delay. | Pillar icons mark which of our four pillars a piece serves, and a topic symbol names its subject. An atlas symbol stands for a variable or a reform in our systems atlas, Who Do They Answer To?, where a variable is a condition that can rise or fall, such as safe seats. Chapter 11’s status marks say where a bill, a records request or an agency rule stands, and its utility icons name an action beside the words that say it. The atlas’s own marks for sign, authority, evidence and delay are its encoding glyphs. | W13, five sentences on one frame; the class table and Rule 10.10 name records requests, agency rules and authority, and the rule should match them |
| `s-10-1-correct` (class table, in the script) | Utility icon row | Names an action a reader takes, always beside its word. | Names an action a reader takes, beside the words that say it. | W20: chapter 11's four exceptions (D2-506) sit beside other words, so "always beside its word" claims more than the rule |
| `10-symbols.json` | Rule 10.1, spec "Topic and atlas symbols" | 124 Civic Line drawings: CL-001 to CL-074, and the reform drawings R-01 to R-50 | 120 of the 124 Civic Line drawings, CL-001 to CL-074 and R-01 to R-50; the other four are the pillar icons | Accuracy: 19 topic, 51 variable (one of them also a topic) and 50 reform drawings make 120 |
| `10-symbols.json` | Rule 10.1, `builders` | where every drawing carries its ID, the name its file and the sprite use, such as CL-031 | where every drawing carries its ID, which its file and the sprite use, such as CL-031 | "the name" read as a second thing beside the ID |
| `10-symbols.json` | Rule 10.2, `rule[0]` | Its line is one weight, from 2.68 to 3.35 units, with round ends and round corners. One part of the drawing carries the red accent: the detail a reader should see first, | Each drawing keeps its line at one weight, set between 2.68 and 3.35 units, with round ends and round corners. One part carries the red accent, the detail a reader should see first, | "one weight, from 2.68 to 3.35" read as a contradiction; W06, the colon held the point back |
| `10-symbols.json` | Rule 10.2, `rule[1]` | takes its word alone until a drawing made this way is approved by our founder and editor. | takes its word alone until our founder and editor approves a drawing made this way. | W02 |
| `10-symbols.json` | Rule 10.2, `why[1]` | The drawings keep open counters inside a steady line, | The drawings keep open space inside each shape and a steady line, | H02: the guide defines "counters" only for letters (Rule 03.4) |
| `10-symbols.json` | Rule 10.2, `correct.caption` | with the keylines that place it, | with its keylines, the guide lines that place it, | H02 |
| `10-symbols.json` and `manifest-systems.json` | Rule 10.2, `failure.caption`; `s-10-2-failure.alt` | A filled stock icon stands in for Bill; Bill is a filled stock document icon | A filled icon from a generic icon library stands in for Bill; Bill is a filled document icon from a generic icon library | H02: "stock" is the atlas's word for an amount built up over time, and chapter 10 sits beside the atlas's variables |
| `10-symbols.json` | Rule 10.3, `why[0]`, first sentence | The cap keeps the line within a quarter of its weight across all 124 drawings. | The cap holds every line in the set between 2.68 and 3.35 units, so the heaviest is a quarter heavier than the lightest. | The old sentence did not say which weight the quarter is of |
| `10-symbols.json` | Rule 10.4, `rule[0]`, last sentence | No topic or atlas symbol is set at 16 px. | Never set a topic or atlas symbol at 16 px. | W02: a rule names who acts |
| `10-symbols.json` | Rule 10.4, `rule[1]` | may hold one topic icon from those 37, | may hold one of those 37 drawings, | H02 keeps "topic symbol" in this chapter, and some of the 37 are atlas symbols |
| `10-symbols.json` | Rule 10.4, `why[0]`, last sentence | The rest need 48 px before a reader can name them. | The rest needed 48 px before the reviewer could name them. | W20: one reviewer's reading, sized to its evidence |
| `s-10-4-correct` and `manifest-systems.json` | The story card's headline, "How to ask your town for its meeting minutes" | no label; `illustrative: false` | the Illustrative label beside the headline; `illustrative: true` | H03: Rule 01.21's kickers label each invented headline the same way |
| `10-symbols.json` | Rule 10.5, `rule[0]`, from its second sentence | Red-Black and Black serve Newsprint and White. Red-Newsprint and Newsprint serve Charcoal. Newsprint alone serves Prussian, where red never sits. | Red-Black and Black serve Newsprint and White, and Red-Newsprint and Newsprint serve Charcoal. Prussian, where red never sits, takes the Newsprint edition alone. | W13 |
| `10-symbols.json` | Rule 10.5, `why[0]` | Each edition keeps the ink at 13.29 to 1 against its own ground, | Each edition keeps the ink at 13.29 to 1 or more against its own ground, | Charcoal on White measures 18.73 to 1 (Master Brief, tension 9) |
| `10-symbols.json` | Rule 10.6, `rule[0]`, from its second sentence | A topic symbol carries its own word, such as Congress. An atlas symbol carries the atlas’s name for its element, such as Congressional capacity for the same drawing where it stands for that variable, with a typed chip such as Variable D1. A reform carries the reform’s name, and the rejected option on term limits keeps the word Rejected wherever it appears. | A topic symbol carries its own word, such as Congress. Where the same drawing stands for the atlas variable, it takes the atlas’s name, Congressional capacity, with a typed chip such as Variable D1, and each reform drawing takes its reform’s name. The rejected option on term limits keeps the word Rejected wherever it appears. | W13 |
| `10-symbols.json` | Rule 10.6, `rule[1]` | Beside its word, the drawing is hidden from screen readers, so the word is read once. | Hide the drawing from screen readers when its word sits beside it, so the word is read once. | W02 |
| `10-symbols.json` | Rule 10.7, `rule[0]` | keeps its red accent, bare on Newsprint, as signature red. | keeps its red accent, set straight on Newsprint with no tile, as signature red. | "Bare" is studio shorthand |
| `10-symbols.json` | Rule 10.8, `rule[0]`, second sentence | Its domains, hubs, layers and routes to change appear as words, or as a typed chip that holds the ID and the name, even where a page lists them beside drawn variables. | Its other parts take words, or a typed chip that holds the ID and the name, even where a page lists them beside drawn variables. Those parts are its domains, which sort issues by subject; its hubs, which gather everyday questions such as Cost of living; its three layers; and its routes to change, the paths a reform can travel, such as a ballot measure. | H02: the guide defines hubs, layers and routes nowhere before this; "route" follows the atlas glossary, and Cost of living is one of the atlas's five hubs |
| `10-symbols.json` | Rule 10.9, `why[0]`, third sentence | Most groups here score well under that, so the trouble lies in the subject: Testify and Public meeting score −0.09, yet a builder looking for a hearing can still reach for the meeting. | Most groups here score well under that, and their risk lies in the subjects, since a builder looking for a hearing can reach for Public meeting although the two drawings score −0.09. | W06, the colon held the point back; W10, the "yet" turn |
| `10-symbols.json` | Rule 10.9, spec "Likeness test" | 0.91 or more is as alike as the closest one pair in a hundred | 0.91 or more puts a pair among the closest one in a hundred | Clarity |
| `10-symbols.json` | Rule 10.10, `rule[0]` | an open diamond for authority, | an open diamond for authority, where one body holds legal power over something, | H02, in the atlas glossary's words for an authority connection |

Left as written, with a reason: the `LOOKALIKES` lines (each pair is a comparison by design, and the words are mine); the four principles quoted from the fourth edition (exact quotes, labeled as design judgment); "Bill and State house have no drawing" in both Rule 10.2 and Rule 10.9 (10.2 says how a drawing joins the set, and 10.9 sends a builder to the word, so each reader meets it where they look); the paths in the builders lines (other chapters print paths there too).

### 4b. Chapter 09's words, as built

I read `work/build/guide/chapters/09-pillar-icons.json` and every `s-09-*` alt in `manifest-identity.json`. The identity designer writes them from `stage_b_identity_ch09.py`'s `chapter()`, so each change goes in there at the string quoted. The pillars run in their locked order everywhere, and the figures check: the 24 px fit B and the 16 px fit both draw a 1 px line (fit manifest), and each pillar master's line is 3.35 units (inventory in use).

| File | Field | Old | New | Rule |
|---|---|---|---|---|
| `09-pillar-icons.json` | Rule 09.1, `why[0]`, second sentence | A reader learns four drawings faster with their words beside them, and the word settles a drawing that could pass for another pillar: Track’s magnifier can read as looking into a question, which is Explain’s job. | The word beside each drawing names it at once, and it settles a drawing that could pass for another pillar, as Track’s magnifier can read as looking into a question, which is Explain’s job. | W20: no one measured "faster"; W06, the colon held the example back |
| `09-pillar-icons.json` | Rule 09.2, `rule[0]`, second sentence | and the red counts as signature red (Rule 05.3). | and that red is signature red, which never counts against a view’s working red (Rule 05.3). | Says what "counts as" means, in chapter 10's words for the same point (Rule 10.7) |
| `09-pillar-icons.json` | Rule 09.3, `rule[0]`, last sentence | Never scale a master to 16 px, and never draw a fit at any size but its own. | Never scale a master down to 16 px or draw a fit at any size but its own. | W11, a run of negatives under one verb |
| `09-pillar-icons.json` | Rule 09.3, `why[0]`, first sentence | with a line about 3 units wide, so at 24 px the line falls to half a pixel, | with a line 3.35 units wide, so at 24 px the line falls to 0.63 px, | Accuracy; Rule 10.4 gives the same 0.63 px |
| `09-pillar-icons.json` | Rule 09.3, `why[0]`, third sentence | A 24 px icon keeps its fit up to 2x, since below 2x the master’s line falls under one device pixel and its counters fill, and the fit keeps every counter and gap. | A 24 px icon keeps its fit on screens under 2x, where the master’s line falls under one device pixel and its open spaces fill in, and the fit keeps every one of them. | H02: the guide defines "counters" only for letters (Rule 03.4); "up to 2x" and "below 2x" said the same thing twice |
| `09-pillar-icons.json` | Rule 09.3, spec "Line" | about 3 units of 128 in each master | 3.35 units of 128 in each master | Matches Rules 10.2 and 10.3 |
| `09-pillar-icons.json` | Rule 09.4, `rule[0]`, second sentence | It never enters a kicker, which may carry a topic icon only (Rule 01.21), and it never sits on a part opener. | It stays out of kickers, which may carry a topic symbol only (Rule 01.21), and off part openers. | W11; H02, "topic symbol", the term chapters 01 and 10 now share |
| `09-pillar-icons.json` | Rule 09.4, `builders` | give it the word of its pillar nearby. | set its pillar’s word beside or under it. | "Nearby" sets no place; under 48 px and on an opener the word sits with the icon |

Left as written: "Watch the vote." on the opener, which the brief names and the plate labels Illustrative; "Four icons that turn up only where a pillar is named stay easy to learn", which the basis labels a design judgment.

### 4c. Chapter 12's words, as built so far

`12-graphic-devices.json` holds the opener and the systems designer's Rules 12.5 to 12.9; the identity designer's Rules 12.1 to 12.4 are not in yet. I read the chapter, the ten `s-12-*` specimens' text and their alts in `manifest-systems.json`. The records request frame's deadlines match 5 U.S.C. 552 as its source line cites it (20 working days, at least 90 days to appeal, 20 working days for the appeal), and the key chart carries its Illustrative label and "Counts invented for this example." The systems designer's build writes these strings (`stage_b_ch12_systems_build.py`).

| File | Field | Old | New | Rule |
|---|---|---|---|---|
| `12-graphic-devices.json` | `intro[1]` | the intervention marker, chart keys, | the intervention marker, which shows where a reform acts, chart keys, | H02, first use; the sentence will also need a clause for Rules 12.1 to 12.4 when they land |
| `12-graphic-devices.json` | Rule 12.5, `rule[0]` | turn Pillar Red at the heavier selected weight: | turn Pillar Red at a heavier weight: | "Selected" is the atlas build's word for a state the reader never sees here |
| `12-graphic-devices.json` | Rule 12.5, `why[0]`, last sentence | Pillar Red measures 2.96 to 1 on Newsprint, so the Charcoal edge keeps the red line at 13.29 to 1 against the page. | Pillar Red measures 2.96 to 1 on Newsprint, under the 3 to 1 a graphic needs, so the Charcoal edge, at 13.29 to 1, gives the red line an outline the page holds. | Accuracy: the edge measures 13.29 to 1, and the red line itself stays at 2.96 |
| `12-graphic-devices.json` | Rule 12.5, `correct.caption` | Reform R-01 on one step of the safe-seat loop: | Reform R-01, all-party primaries with ranked general elections, on one step of Loop R10, the safe-seat loop: | H11, name what an ID refers to, as the plate's own note does |
| `12-graphic-devices.json` | Rule 12.7, `rule[1]` | The locator is always ink. It never takes red. | Draw the locator in ink, with no red. | W10, two short halves that say one thing |
| `12-graphic-devices.json` | Rule 12.7, `why[0]` | A locator answers where am I before the reader asks, | A locator answers “Where am I?” before the reader asks, | A quoted question needs its marks |
| `s-12-layers-correct` and its alt | The core plane's tiles | Economic structure, Political inputs, Electoral competition, Governing institutions, Legitimacy, Outside drivers | Wealth, Voice, Elections, Checks, Policy, Outside forces | DR-32 and DR-35: the plain names lead, and Rule 12.7's locator on the next plate already says "Elections"; "Legitimacy" for the part every other page calls Policy would send a reader looking for a part that is not there. The economy and technology planes keep the atlas's region titles, which have no plain names |
| `12-graphic-devices.json` | Rule 12.9, `rule[0]` | name who owns the next step and the clock that runs, as the law sets it. | name who owns the next step and the deadline the law sets. | W01: the plain word |
| `12-graphic-devices.json` | Rule 12.9, `correct.caption`; spec "Each handoff"; `s-12-owner-correct` alt; `s-12-owner-failure` alt | the clock the law sets; then the clock; with the clock that runs; and no clock | the deadline the law sets; then the deadline; with the deadline the law sets; and no deadline | One word for one thing (H02), following the rule |

Check for the systems designer, not a word change: Rule 12.6 draws the grades as fills (solid, gray, light gray, a hatch, a dotted outline), while Rule 10.10 draws them on the atlas's connections as line textures. If both are right for their own system, one clause in 12.6 saying that bars and areas take fills, and connections take Rule 10.10's lines, keeps a reader from thinking the grades changed.

### 4d. Chapter 11's words, first pass on the draft of 04:37 UTC

Chapter 11's maker is still writing (its notes say in progress), so this pass reads `11-icons.json` as it stood at 04:37 UTC: Rules 11.1 to 11.16, the five extras and the four sources. I found no studio word, em dash or listed filler. The renumbered bills (DR-151), Nebraska's slash and words (DR-150) and Rule 11.7's 44 px (DR-153) all read as decided, and Rule 11.16's order matches Rule 05.3. I will read the specimens' alts and the final text once the maker says the chapter is done.

| File | Field | Old | New | Rule |
|---|---|---|---|---|
| `11-icons.json` | Rule 11.1, `builders[1]`, first sentence | Number an invented bill far past any number a legislature has used: a federal bill from H.R. 99001 up, a state bill from H.99001 and S.99002 up, | Number an invented bill past the numbers legislatures assign: a federal bill from H.R. 99001 up, state bills from one count that starts at H.99001 and S.99002, | W20: no one checked every legislature; "from H.99001 and S.99002 up" read as two counts, and DR-151 sets one |
| `11-icons.json` | Rule 11.2, `failure.caption` | <strong>Fails 1.4.1.</strong> | <strong>Fails WCAG 2.2 SC 1.4.1.</strong> | H11, and Rule 11.15's failure already names it this way |
| `11-icons.json` | Rule 11.6, `failure.caption` | A stock stepper draws checks and boxes | A generic stepper from a component library draws checks and boxes | H02: "stock" is the atlas's word for an amount built up over time (same change as Rule 10.2) |
| `11-icons.json` | Rule 11.8, `rule[1]`, last sentence | An appeal ends in words too: Upheld, Partly reversed, or Reversed and sent back. | An appeal ends in words too: Upheld, Partly reversed, Reversed and sent back, or Closed for other reasons. | The spec lists four appeal endings and the rule three |
| `11-icons.json` | Rule 11.9, `rule[1]` | such as an interim final rule, | such as an interim final rule, which takes comments only after it takes effect, | H02, first use |
| `11-icons.json` | Rule 11.9, `why[0]`, first sentence | Sending a comment is the public’s main way to take part in a federal rule, | Sending a comment is the way the law gives the public to take part in a federal rule, | W20: "main" ranks ways no one counted; 5 U.S.C. 553(c) sets the comment as the public's route |
| `11-icons.json` | Rule 11.11, `why[0]`, first sentence | A reader who meets an icon beside its word learns the sign once and reads it faster after that, and the word carries the meaning for anyone who does not know the sign. | A reader who meets an icon beside its word learns the sign once, and the word carries the meaning for anyone who does not know the sign. | W20: "faster" was not measured (same change as Rule 09.1) |
| `11-icons.json` | Rule 11.11, `correct.caption`, last clause | and the page’s size stays two words. | and the control for the page’s size stays in words. | Clarity: "two words" left the reader to guess which |
| `11-icons.json` | Rule 11.14, `why[0]`, second sentence | CL-024, Feedback loop, comes nearest to the refresh sign a builder reaches for, and a loop stepper is the place a builder would reach for it. | CL-024, Feedback loop, looks most like a refresh sign, and a loop stepper is where a builder would reach for one. | The sentence said "reach for" twice |
| `11-icons.json` | Rule 11.14, `builders` | use the word alone and ask the editor; do not borrow a drawing from chapter 10. | use the word alone and ask the editor, and leave chapter 10’s drawings to the subjects they name. | W09 |
| `11-icons.json` | Rule 11.16, `correct.caption` | where reform R-01 acts | where reform R-01, all-party primaries with ranked general elections, acts | H11 |
| `11-icons.json` | `sources[2]` | “Fiscal Year 2024 Annual Freedom of Information Act Report”, March 6, 2025, section III. The categories | “Fiscal Year 2024 Annual Freedom of Information Act Report”, March 6, 2025, section III, fiscal year 2024, federal agencies. Retrieved November 9, 2026. The categories | H04 asks for the period, the place and the date retrieved; the research notes of November 9, section 7, give the date it was read |

**One correction to my own chapter 10 row.** Chapter 05 defines a keyline as "a 1 px Charcoal edge drawn inside the mark", and chapters 11 and 12 use it that way, so my Rule 10.2 caption brought in a second meaning. Chapter 10's maker should set Rule 10.2's `correct.caption` from "with its keylines, the guide lines that place it," to "with the guide lines that place it," (H02).

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
- D2-xxx | Step 3's Congress counts "Congress, the House or the Senate" as a pass and a legislature or a chamber in session as partly | No Congress drawing names Congress without its label (D2-620), so a partial answer still shows the drawing points at the right word
- D2-xxx | Step 3 lists, for each new drawing, the misreadings to report to Dustin in the reader's own words | Each drawing was drawn to rule them out (research notes of November 9, section 1)

Rule 01.11 after the research lead's round 2 notes (DR-187):
- D2-xxx | The plate's Missouri sentence says "according to unofficial returns" | The count is not certified; the coordinator asked that the plate or its line say so
- D2-xxx | The source line names the county page in full, with its title, site and date | H04, and the coordinator's request that the official page be named
- D2-xxx | The counting sentence is active, "We counted each map...", and the research draft's colon becomes two sentences | W02, W06
- D2-xxx | Every Rule 01.11 and Rule 01.21 string now lives in `guide_editor_ch01.py`, and the build's count check accepts a sourced count | A rebuild of chapter 01 would otherwise undo them, and the old check failed any plate that counts
- D2-xxx | After every rebuild of chapter 01, run `stage_b_identity_ch01.py` | It touches only the inline masters and the kicker word and is safe to rerun, so the two owners' steps stay apart
- D2-xxx | `s-01-pieces.html` stays as committed until chapter 11 lands | A rebuild now would carry chapter 11's mark code mid-build onto chapter 01

Chapter 10 (item 4):
- D2-xxx | CL-064's sentence says "checkpoint" in place of "gate" | The guide check refuses "gate" on reader pages (D2-253)
- D2-xxx | CL-025's second sentence drops the words the library already prints before it | The library sets the chip and "Congressional capacity" first, so the old sentence repeated both
- D2-xxx | My label build runs the guide check's studio-word patterns | A word the page refuses never reaches chapter 10's maker again

Chapters 01, 09 and 12 (item 4):
- D2-xxx | The guide says "topic symbol" for a topic drawing everywhere, and chapter 01's three "topic icon" become "topic symbol" | H02 keeps one term; chapter 10's class name governs, and "icon" stays for pillar and utility icons
- D2-xxx | Rule 01.21's failure kicker reads "Workers’ share of income", like the correct one | The pair then differs only in the drawing, which is the fault it teaches (identity designer's request)
- D2-xxx | `s-01-pillars`'s manifest note says its icons come from the sprite through the identity designer's step | The identity designer's request; the note had said they were inlined
- D2-xxx | Rule 12.8's core plane takes the plain part names | DR-32 and DR-35, and Rule 12.7's locator already uses them
- D2-xxx | Rule 12.9 says "deadline" for the time the law sets | The plain word, used the same way in the rule, caption, spec and alts
- D2-xxx | "Keyline" keeps chapter 05's meaning, a 1 px Charcoal edge inside a mark, and chapter 10 calls its construction lines "guide lines" | H02; chapters 11 and 12 use chapter 05's meaning
- D2-xxx | "Stock" leaves every reader page where it means generic, in chapters 10 and 11 | H02: the atlas defines a stock as an amount built up over time
- D2-xxx | Chapter 11's pass reads the draft of 04:37 UTC, and a final pass follows when its maker says the chapter is done | The maker was still writing, and an early table lets it apply the changes as it goes

## Questions for Dustin

All three are answered: 1 and 2 by DR-188 and DR-189, 3 by DR-187.

1. **The check runs about 15 minutes.** The first check was estimated at 9 to 10 (DR-86), and this one adds DR-143's five topics. *Recommendation:* keep it whole and say 15 minutes in the invitation. If you want it near 12, the four-symbol naming step can go, which saves about 2 minutes.
2. **Should the new Congress, Testify and Contact an official drawings join the symbol naming step?** DR-143 names no new Civic Line drawing, and each adds about half a minute. *Recommendation:* leave them out of this check, so it stays near 15 minutes; the creative director's naming reads on the drawings board stand for now.
3. **If Missouri's voters rejected the 2025 map on November 3, what does the plate count?** Research D2-525 counts the map as passed, with its suspension explained. A map voters turned down would read more like Virginia's attempt. *Recommendation:* once Missouri's certified result is read, report the record as it stands (DR-93): if voters rejected the map, the plate counts six maps from Republican-led bodies and names Missouri's beside Virginia's; if they approved it, the plate stands as written.

Requests to other owners:
- **Research lead:** done in its round 2 notes. Still open: Missouri's certified statement, to swap in before Phase 5, and Virginia's 2025 House of Delegates.
- **Identity designer:** the kicker swap is in, and the caption and alt match it.
- **Engineer:** build the page from `20261110_Reader-Check-2-Questions.md`; step 3's new rows are in, and its "Answer key" section lists what the key file holds.
- **Chapter 10's maker:** rebuild from the labels file for CL-064 and CL-025, and take section 4a's table.

## Tested

- The labels file by script: it parses; 124 rows in ID order, CL-001 to CL-074 then R-01 to R-50, no repeat; every row has a label and one meaning sentence ending in a period; every Civic Line word matches `civic-line-v6/20261110_Civic-Line-V6-Inventory.csv` exactly (124 of 124).
- Every V7 ID, title and short name read from the full model (`work/extract/atlas-v7-data.json`): 51 variables mapped to 51 drawings through the icon map, 50 reforms, 25 short names from the loops' chain labels, each variable with one short name at most.
- My words in the labels file, by script: no em or en dash, no straight quote, none of the listed fillers or corporate verbs, no "not" or "never", no color word in a meaning sentence, no figure under ten in a sentence.
- The eight changed drawings rendered from their approved SVGs in Chromium and looked at; all 122 October drawings looked at on two contact sheets; my sentences compared with the v6 inventory's notes on the eight.
- Rule 01.11: every figure in the count against V7's records (the table above); the build (`guide_build.py --strict`: 9 chapter files, 100 rules, 233 specimens, 0 placeholders); the plate looked at in the built guide at 1,440 and 390 px; the chapter JSON and the editor manifest parse and change only in the fields named.
- The reader check file: the PW03 lines match V7's text exactly; the first check's question words and rating labels compared with its template; the answer counts (54) and fixed looking time (175 s) added up by hand; a scan for dashes, fillers and negations, each hit read.
- A full read of all three files against chapter 02's rules.
- Round 2: the labels file against the guide check's studio-word patterns (CL-064 the one hit, now fixed); Rule 01.11's new strings in all three files, each old string matched once; Missouri's figures against the research notes; chapters 01 and 02 rebuilt by the generator and the identity step, then all 115 files compared with the committed copies (three differences, each explained in section 2b); `guide_build.py --strict` after the restore (12 chapter files, 128 rules, 295 specimens, 0 placeholders); the plate looked at in the built guide at 390 px.
- Chapter 10: its JSON, the class table, the `LOOKALIKES` lines, the library's meaning lists and every `s-10-*` alt read in full; 7,626 pairs and the 1.25 line ratio checked by arithmetic; hubs, layers and the route definition read from the atlas model.
- Chapter 09: the JSON and nine alts read in full; the fits' line widths from `20261109_Pillar-Pixel-Fit-Manifest.json` (fit B at 24 px and the 16 px fit, 1 px) and the masters' 3.35 units from the inventory in use.
- Chapter 11: the draft JSON of 04:37 UTC read in full, and scanned by script with chapters 09, 10 and 12 for the guide check's studio words, em dashes, the listed fillers, "stock", "clock" and "keyline".
- Chapter 12: the JSON, the ten specimens' text and alts read in full; the frame's deadlines against the statute sections its source line cites; the core layer's part names against the atlas editorial data's `parts`.
- Chapter 01 after the terminology and failure kicker changes: generator and identity step rerun, every output compared with the copy before the run, then `guide_build.py --strict` (12 chapter files, 128 rules, 295 specimens, 0 placeholders).

## Not tested

- How the labels and sentences read aloud to real readers, and how they fit chapter 10's contact sheets, which do not exist yet.
- Whether the 24 px lockmark, the pixel fits and the end mark look as these questions assume on real phones; the questions are written from the decisions and the specimens, not from phone captures.
- The reader check page, which the engineer builds; the time estimate, which no reader has measured.
- Missouri's certified result, which is not out, and Virginia's 2025 House of Delegates; the research lead read every other party on a primary source.
- `guide_check.js` on chapters 01 and 10 after these edits; I ran the build only.
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

Round 2, after the coordinator's messages:
- `work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json`: CL-064's sentence and CL-025's second sentence
- `work/handoffs/phase-2/20261110_Reader-Check-2-Questions.md`: step 3's four symbols and their rows (DR-189), and the words to keep off the page
- `work/build/guide/specimens/s-01-11-correct.html`, `work/build/guide/chapters/01-purpose.json`, `work/build/guide/specimens/manifest-editor.json`: Rule 01.11 after the research lead's round 2 notes (DR-187); Rule 01.21's caption and alt
- `work/build/scripts/phase-2/guide_editor_ch01.py`: the same Rule 01.11 and Rule 01.21 strings, so a rebuild keeps them
- `work/build/scripts/phase-2/guide_editor_build.py`: the BE-02 count check accepts a sourced count
- `work/build/scripts/phase-2/guide_editor_ch01.py`, then by a rebuild `01-purpose.json`, `manifest-editor.json` and `s-01-21-failure.html`: "topic symbol" for "topic icon" in Rule 01.21; the failure kicker's word; `s-01-pillars`'s note. After each rebuild I ran `stage_b_identity_ch01.py` and restored the committed `s-01-pieces.html`, and the compare showed only these changes

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
| CL-025 | Congress (as D1: Congressional capacity) | D1 | A chamber in session, seen from the gallery, with members on a curved bench below a three-tier rostrum, stands for Congress. Where it stands for D1: The same chamber stands for the staff and expertise Congress needs to investigate problems, write laws and oversee agencies. |
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
| CL-064 | Costs of tariffs and trade rules | EC10 | A parcel meets a checkpoint with two bars across it, for import taxes and trade rules that can raise what U.S. buyers pay. |
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
