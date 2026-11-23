# Chat 12 review: words and readers (CE, DF, RP)

Written November 23, 2026 by the words and readers reader, working to oa-editor's rules, from 17:12 to 17:29 UTC (clock read with `date -u` before this write). Chapter 02's writing rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`) are the standard for every word quoted here. Codes: CE for the civic educator's read (terms, clarity, a rule against its own plate), DF for drift between chapters, RP for the simulated reader panel.

## 1. Score

**3 of 5.** The chapters' own prose is close to shipping: no em or en dash, filler, corporate verb or numeric date anywhere a reader looks, and chapter 16 reads whole as plain teaching. The words the kit composes on chapter 21's atlas pages are where readers stumble: chips with no names, studio words ("ink", "Newsprint", "flows") on public pages, mixed apostrophes, and two plates that show what their own rule forbids.

## 2. Must fix

**CE1. Chapter 21's own pages break Rule 21.6 and house rule H11: a chip names a record and no name follows.**
- Where: the kit's atlas pages A12 and A14 (`work/build/app-kit/renderers/atlas-page.mjs`, which composes these lines) and their word fields in `work/build/scripts/phase-4/phase4_ch21_build.py` (`PAGES['A12']['page']['aims_here']`, `'touches'`, `PAGES['A14']['page']['grade_line']`, `'also_aim'`); plates `s-21-reform`, `s-21-5-correct`, `s-21-loop`, `s-21-1-correct`.
- What is wrong: Rule 21.6 says "The first time a page names a record, its name follows the chip", and its specification gives "the record’s name as the link’s description where the words around it do not name it". No chip on the atlas pages carries a description (none has `aria-describedby`), and these print bare:
  - Reform R-23: "Variable A4: Reform R-24 Reform R-25 Reform R-26 Reform R-31 also aim here" (R-24, R-26 and R-31 are never named on the page; there is no comma or "and" between the four chips); "Its record names Loop R6 as a loop it touches" (Loop R6 is never named).
  - Loop R18's head: "Documented for Variable D2 to Variable D4; Plausible for Variable D4 to Variable D2", and the facts panel's "Weakest step: Connection L15 Plausible", both before any name appears.
  - The Register: "It would act on Connection L18 and Connection L19." (L18 is never named there.)
- Fix: compose each first mention as chip, then the stored title, as the rest of the page already does ("Connection LE15 “Higher income strengthens household security”"), and join a list of chips with commas and "and": "Variable A4, “Households’ financial security”: Reform R-24 “…”, Reform R-25 “…”, Reform R-26 “…” and Reform R-31 “…” also aim here." On Loop R18's grade line: "Documented for Connection L14 “Presidential removals weaken watchdog agencies”; Plausible for Connection L15 “Independent watchdogs restrain unilateral action”". Where a list grows too long to name, give each chip its name as its link's description, as the specification says. Add a check for the name to the atlas test's T1.
- Owner: editor (word fields and templates), engineer (the kit's composition and T1), data lead (sign-off, since the views change).

**CE2. Rule 20.9's correct plate prints a count its rule forbids, and a first screen with "no panel" whose page shows one.**
- Where: `s-20-9-correct`, written by `phase4_ch20_build.py` (the measure's panel count near line 1360, and its words `'panels'`, `'none'`).
- What is wrong: Rule 20.9 says each opening screen holds "at most one dark panel". The plate prints "Home page, Explain, Track, Connect, Act / 72.2 percent Newsprint / 22.5 dark, 0.0 red; 4 panels". Rules 20.5 and 20.6 say the pillar row's four cells "meet as one band at 1440 px", and the export shows one band. The same plate prints "Home page, first screen / 81.1 percent Newsprint / 13.4 dark, 0.0 red; no panel" and draws its box empty, though the home page's first screen at 1440 px holds that band (`20261121_Web-Home-Page-1440-Light.png`, the band from about y 190). A builder who copies the correct plate learns that four panels pass and that a screen with a band has none.
- Fix: count touching cells as one panel and print "1 panel, the pillar row’s band"; draw the band in the first screen's box and print "1 panel, counted with its section" (or the rule's own words for where a panel counts). If the studio means four cells to count as one panel only when they meet, Rule 20.9's specification "Panels" says so in one sentence.
- Owner: design director (the measure and drawing), editor (the plate's words and any sentence in Rule 20.9).

**RP1. Reform R-23's contested remedy prints two readings with no labels, where approved Rule 01.16 asks for "matching labels".**
- Where: `s-21-reform` and the working page A12 (`atlas-page.mjs`, the remedy split; word field to add in `PAGES['A12']['page']`).
- What is wrong: Rule 01.16 sets both readings of a contested claim "in one two-column block with matching labels", and its own plate labels them "One reading" and "The other reading". The R-23 page sets the stored text side by side with no label, so the second block opens on the atlas's own words "Main limitation: higher floors fall outside the studied range; the Congressional Budget Office’s 2019 median estimate …". The simulated right-leaning reader read that as the Congressional Budget Office demoted to a footnote; the left-leaning reader did not notice it. D4-253 settled the length (stored text prints as stored); the labels are our words and edit nothing stored.
- Fix: put "One reading in our atlas" and "The other reading in our atlas" (or Rule 01.16's own "One reading" and "The other reading") over the two blocks in the same type, and let the atlas test's T10 accept them.
- Owner: editor (words), engineer (kit), design director (layout), data lead (sign-off).

## 3. Should fix

### Words against chapter 02 and the civic educator's read

**CE3. The Act page leaves its key terms unexplained (H02, H11).** A08, `phase4_ch20_build.py` (A08's word fields). The reader is told to "include the docket number, FDA-2025-N-2699" and meets "Docket FDA-2025-N-2699" over the red link, "Regulation Identifier Number 0910-AI91" and "Citation 91 FR 73717 (21 CFR Part 190)" with no word on what any of them is. Fix: at the first "Docket" in the status panel, "Docket FDA-2025-N-2699, the rule’s public file"; in the steps, "include the docket number, FDA-2025-N-2699, which files your comment with this rule"; in "The rule at a glance", "Regulation Identifier Number, the government’s tracking number for this rule" and "Citation: volume 91 of the Federal Register, page 73717 (91 FR 73717), to be added to Title 21 of the Code of Federal Regulations, Part 190". Owner: editor.

**CE4. The Act page never says what NAC is or why the law kept it out of supplements.** A08. The page says the FDA "proposes to let products containing N-acetyl-L-cysteine (NAC) be sold as dietary supplements" and that the FDA said in 2001, 2010 and 2020 that such products "are excluded", and stops. A newcomer cannot tell why. Fix: one sentence from the rule's own background (pages 73719 to 73720) on why NAC was excluded, in the rule's terms, checked against `work/research/20261121_Act-Page-Docket.md` and the Federal Register. Owner: editor, with the evidence reader's check.

**CE5. One page, two step counts.** A08. The status panel tracks "Step 4: Comments closed", "Step 5: Final rule" and six steps in all; chart S66 under "Who decides" says "A federal agency makes a rule in five steps the law sets", where step 4 is "Final rule published". The simulated teacher and newcomer both read "step 4" as one thing. Fix: under "Who decides", "The chart numbers the five steps the law sets. The panel at the top follows this rule in six, adding the early notice and the close of comments." Owner: editor.

**CE6. Chapter 21 uses its core terms before it explains them.** `21-atlas.json` through `phase4_ch21_build.py`'s chapter words.
- "variable": the intro says "the arrows from one variable to another" and never says what a variable is. Fix: "the arrows from one variable, a quantity or condition that can rise or fall, to another" (the atlas home's own words).
- "grade": the intro says "links every claim to the record that grades it". Fix: "to the record that grades it, giving its evidence one of five grades from documented to hypothesis (Rule 13.3)".
- "sheet": group 3's line, "The Register files each connection once, on one sheet", comes before Rule 21.8 explains sheets. Fix: "on one sheet, the Register’s page for one domain or layer".
- "issue record": used in Rule 21.8 ("loops, reforms and issue records"); explained only in Rule 21.11. Move Rule 21.11's sentence "An issue record is one of the atlas’s files on a documented problem, case or policy." into Rule 21.8.
- Reinforcing and balancing: Rule 21.12 says "an even count makes a loop that feeds itself, and an odd count one that pushes back", and Rule 21.14 then uses "reinforcing" and "balancing" with no tie to them. Fix 21.12: "an even count makes a reinforcing loop, one that feeds itself, and an odd count a balancing loop, one that pushes back".
- The Register page's intro has the same gap. A13 `'intro'`: "Every connection in our atlas files once, on the sheet of the variable it moves" names no actor (W02) and never says what a sheet is. Fix: "Our atlas files every connection once, on the sheet for the domain or layer of the variable it moves, with its sign, its grade and the atlas’s citation."
Owner: editor.

**CE7. Public atlas pages speak the studio's language.** `phase4_ch21_build.py`: A16 `'red'` reads "On Newsprint a red connection carries a thin Charcoal edge." and `'tag'` reads "… in plain ink, so the red stays with the reform you chose."; A12 `'conn_note'` reads "It stays in ink, since the reform does not act on it." A public reader has never met Newsprint, Charcoal or "ink". Fix: "On the light page a red connection carries a thin dark edge."; "… in the text’s own color, so the red stays with the reform you chose."; "It keeps the drawing’s usual color, since the reform does not act on it." The alt for `s-21-3-correct` ("in full ink") can stay, since the guide is its reader. Owner: editor.

**CE8. Composed lines run a chip into its name with no pause.** A12 and A14 templates (`'read_start'`, `'read_step'`, the variables' "higher value" lines). On screen and in a screen reader: "Start with Variable D2 presidential action without new legislation rising."; "Along Connection L14, which lowers, Variable D4 ability to investigate and enforce the rules falls."; "Variable EC7 A higher value means households receive more money over the year." Fix: set the name off with commas or a colon: "Start with Variable D2, presidential action without new legislation, rising."; "Variable EC7, household income: a higher value means households receive more money over the year." Owner: editor (templates), engineer (composition).

**CE9. "This question reaches here" before the reader has met a question.** A11 `'lit'`. On the phone the drawing sits above the questions, so the first screen of the exported state (`20261122_Atlas-Home-Page-390-Light.png`) shows "This question reaches here" in Wealth and Checks with no question in view. Fix: "The question you pressed reaches here". Owner: editor.

**CE10. Rule 20.6 says each card shows its date; two of four do not.** A06's word fields (`'dateline': None` on the Connect and Act cards). The rule: "Each piece is a card with its kicker, headline, a few lines and its date." The Act card prints a status that can change, "Step 3 of 6: Comments open. You can take part now.", with no "As of" line, which Rule 13.10 asks of every status. Fix: "As of November 21, 2026" on the Act card and "As of October 15, 2026" on the Connect card, or reword the rule to "and its date or source line" if the Connect card's source line is meant to carry it. Owner: editor.

**CE11. Reform R-23 puts "Works alongside" inside "How it could pass", before the routes.** A12. Rule 21.4's specification orders "routes; reforms it works alongside; sources", and the page prints "How it could pass / Works alongside: Reform R-25 “Full child tax credit for low-earning families”" above Route SS, so a reader can take Reform R-25 for a route to passage. Fix: its own line or heading after the routes, as the specification orders. Owner: design director, editor.

**CE12. Rule 21.6's chips plate claims a name for every chip.** `s-21-chips`: the caption says "each a real record with its name" and the alt says "each followed by its record’s name", but Claim CL1340, Rule change RL19 and Delivery case DL05 print none (the model gives those three kinds no title field). Fix the caption: "each a real record, with its name where the atlas gives it one"; the alt to match; and Rule 21.6's sentence "its name follows the chip, or for a claim, a rule change or a delivery case, its first words". Owner: editor.

**CE13. Three of chapter 20's sentences are hard to parse.** `20-web.json` through `phase4_ch20_build.py`.
- Rule 20.2: "Its title, Menu, and Close the menu sit at the top" reads as an instruction. Fix: "The title Menu and the button Close the menu sit at the top".
- Rule 20.3's specification "Lockmark row": "the lockmark’s 24 px master, 12 px, and the tagline". Fix: "the lockmark’s 24 px master, a 12 px gap, then the tagline".
- Rule 20.8: "sets out what the record shows from those who asked for the change and on the concern the law guards". Fix: "sets out what the record shows, from the request for the change to the concern the law was written to protect".
Owner: editor.

**CE14. Terms used before their definitions in chapters 16 and 20.**
- Group 2's line in chapter 16 names "our rights ledger" two rules before Rule 16.6 explains it. Fix: "our rights ledger, our record of every picture we use, records its rights …".
- Rule 16.10's specification "each with its caption-safe area" comes before Rule 16.11 explains the term. Fix: "each with its caption-safe area, the part no app button or crop covers (Rule 16.11)".
- Rule 16.11 names WebVTT and SubRip with no word on what they are. Fix: "in one of two caption formats: WebVTT (.vtt) on our own pages …".
- Rule 20.10's "no deck" and Rule 20.11's "maskable". Fix: "no deck, the line under a headline"; "maskable, so a phone can crop it to its own shape".
Owner: editor.

**CE15. "X, never Y" eleven times in the new chapters' specifications (W09's corrective turn).** Chapter 21 has nine, more than any approved chapter (chapter 15, about the same length, has six). Each with a fix:
- 16.2 "made from the original file, never from the 1,200 px copy the page shows" → "made from the original file; the page’s 1,200 px copy is for screens only".
- 16.11 "inside chapter 23’s caption-safe area, never doubled" → "inside chapter 23’s caption-safe area, with closed captions off".
- 21.2 "one arrow for each direction of a pair, never a double head" → "one single-headed arrow for each direction of a pair".
- 21.3 "after each press, never on load" → "after each press, and silent on load"; the same in 21.11.
- 21.6 (spec and builders) "never from its letters" → "since letters repeat across kinds, as B4 does".
- 21.7 "One link or one disclosure, never a search" → "One link or one disclosure, with no search between".
- 21.13 "never under 6,000 ms" → "at least 6,000 ms"; the rule's "never less than six seconds" → "at least six seconds".
- 21.15 "From a token, never a hex in the page’s code" → "From a token named in the page’s code".
- 21.16 "in a copy of a page, never in the model" → "in a copy of a page, with the model untouched".
Owner: editor.

**CE16. Four small faults in plates.**
- `s-16-10-correct`'s caption: "every figure said is the chart’s own. The figures are chart S04’s, …" says it twice. Fix: drop "and every figure said is the chart’s own".
- `s-16-9-correct`'s prompt: "No people, no logos, no words." (W11). Fix: "Leave out people, logos and words."
- `s-21-16-correct`: "T1 typed ids". Fix: "T1 typed IDs" (the atlas test's report labels).
- The article (A07) ends its last section on a description after the step, though Rule 20.7 says it "ends on a step": "Read your state’s summary in … (another site). It covers each state and the District of Columbia, arranged by kind of government." Fix: "Read your state’s summary, one for each state and the District of Columbia, in the Census Bureau’s report … (another site)."
Owner: editor.

### Drift (one word for one thing)

**DF1. Atlas text prints with straight and curly apostrophes, sometimes on one screen.** 22 straight apostrophes on the atlas pages and 8 in chapter 21's failure plates; D3-81 says "Text taken from atlas records prints with curly apostrophes", and chapter 14's charts do so. The same question prints "why can’t I find an opening?" in chapter 20's home table (chart S10) and "why can't I find an opening?" on the atlas home. On Reform R-23's phone screen the drawing reads "Households’ financial security" and the sentence under it reads “Households' financial security”. Others: "Congress's", "Workers'", "Officeholders'", "Government's", "isn't", "child's", "owners'" (A11, A13, A15), and "doctors' offices", "bill's", "patient's" in `s-21-7-failure`. The data lead's note 20 (chat 11c) asked for stored marks as stored; D3-81 is the logged rule. Fix: curl every apostrophe the kit prints from the model in reader text, as D3-81 and chapter 14 do, keeping data and exports as stored. Owner: engineer (kit typography), design director (the failure plates' generator); the main session confirms D3-81 over note 20.

**DF2. "Flow" means two things.** Chapter 15 (approved) defines it: "nine are flows, amounts per period". Chapter 21 uses it for the arrows between parts: Rule 21.2's title "with a count on every flow", "the other flows in a lighter ink", the specification's "a “5 to Voice” line for each flow it sends", and the home page key "Other flows." (A11 `'key_other'`). Chapter 15 governs (H02: keep the same term). Fix: "arrow" in the rule ("with a count on every arrow"), and "Other connections between parts." in the key. Owner: editor.

**DF3. "Checked", "As of", "read" and "retrieved" drift.** Rule 13.10 sets "As of" and the date for a status; Rule 15.23 keeps "Checked" for an atlas entry's check and "Retrieved" for our research. The Act page prints "Checked November 21, 2026" twice (once with a period, once without), while the home page's tracker prints "As of November 21, 2026" for the same kind of status on the same day. Chapter 16 writes "(YouTube Help, read November 21, 2026)" six times beside "retrieved" in its sources. Fix: "As of November 21, 2026" on the Act page and in Rule 20.8's specification "Opening"; "retrieved" in chapter 16's six platform rows. Owner: editor.

**DF4. "Dark mode" once.** Rule 16.8's correct caption: "a 4:5 frame on Charcoal for a portrait post in a dark mode". Chapters 17 to 21 say "dark theme", and a social post has no theme. Fix: "and a 4:5 frame on Charcoal for a portrait post." Owner: editor.

**DF5. Frame alts say "on Newsprint" where captions say "light theme".** Every kit frame alt on A04 to A20 ends "At 1440 px, on Newsprint." beside "At 1440 px, in the dark theme."; chapter 20 and 21's captions and frame labels say "in the light theme" and "light". Fix: "At 1440 px, in the light theme." Owner: engineer (`oa-app.mjs` frame names), editor.

**DF6. "Sheet D04" and "the sheet for Domain D04".** The kit's alts for A13 and A18 ("with sheet D04 open") and the frame label in `s-21-10-failure` ("Sheet D04’s reforms at 390 px") print a code without its kind word; chapter 21's captions say "the sheet for Domain D04", as Rule 21.6 asks. Fix: "with the sheet for Domain D04 open"; "The sheet for Domain D04, its reforms, at 390 px". Owner: engineer, editor.

**DF7. "Kind word" and "grade line" each mean two things in chapter 21.** Rule 21.6's "Kind word" is the record's kind (Loop, Reform); Rule 21.12's specification "Chip, kind word and the title" means Reinforcing or Balancing. Rule 13.4's "grade line" is the drawn line sample; Rule 21.12's title "Head a loop page with its grade line" means a line of words. Fix: "Chip, the loop’s kind (Reinforcing or Balancing) and the title"; "Head a loop page with the grade of each step and the arithmetic of its signs." Owner: editor.

**DF8. Two names for each ink in Rule 21.2.** The rule says "in full ink … and the other flows in a lighter ink"; its specification says "the essential ink … the subtle ink". Fix: the specification's names in both. Owner: editor.

**DF9. Widths printed two ways.** Chapter 20 prints "1,024" eight times and "1024" six, sometimes in one caption ("at 1440, 1024, 390 and 360 px … At 1,024 px the pillar row breaks"); chapter 07 writes "1024" and "1440". Fix: "1024" and "1440" throughout chapter 20, and the same in `s-20-files` ("1024 by 3672 px", or keep the commas there only, as data). Owner: editor.

**DF10. The tag has two names.** The How to read page calls it "Also aim here"; the plate's table beside it says "Ink tag, aims here". Fix: "Also aim here" in both. Owner: editor.

### Readers and balance

**RP2. Chapter 21 prints no reason for its four views.** Both simulated fairness readers asked why the reform is the minimum wage and the loop is presidential power over watchdogs. D4-164 has the reason (a rotation across health care, wages, Congress and the agencies, and presidential power, each with a finding one side may want to skip), and the chapter never says it. Fix: one plain line in chapter 21's intro or the reform plate's caption, with the evidence reader's wording, naming the rotation and pointing to chapter 01's rotation log (Rules 01.9 to 01.12). Owner: editor, with the evidence and balance reader.

**RP3. Rule 21.4 cites house rule H08 for a pair H08 would print at equal length.** Specification "Contested remedy": "each with its source a step away (house rule H08)". H08's table gives contested "Both readings, at the same length"; D4-253 printed the stored readings at the record's lengths and kept H08 for our own sentences. Fix: "(printed as stored; house rule H08 governs our own sentences about the grade)". Owner: editor. The approved wording behind it is in section 5.

**RP4. Two names for one part, unlabeled.** The atlas home prints "Outside forces" over "Outside drivers", "Policy" over "Legitimacy", and so on. The newcomer could not tell which was the name. Fix: label the second line "In the model: Outside drivers", or set it in the caption style with "the model’s title" once in the key. Owner: editor, design director.

## 4. The named places

- **16, balance by the record (RP's left and right readers).** The Act page's "What the record shows" holds to DR-93: the record holds the petitioners' request and the law's concern, and the page says "To date, we have not received any comments expressing concern" in the FDA's words. Both readers read it as fair. Rule 21.4's remedy prints as stored and passes on length (D4-253), but it lacks approved Rule 01.16's matching labels (RP1). Loop R18's stored "How it adapts" names both parties' removals, which both readers credited. The choices of the FDA's NAC rule, S86's special districts and the four views read as defensible from both sides; the chapter does not print why (RP2).
- **17, the Illustrative label (CE).** Pass. It sits beside every invented person, place and quote: Maya Brooks and Alder County High School (`s-16-6-failure`), Alder County (`s-16-9-failure`), the invented caption (`s-16-5-failure`), the four video plates (`s-16-11-correct` through the build's caption from its manifest flag), the ranked index (`s-21-14-failure`), and oathandaction.org in every footer of the nine working pages. None sits on the shot list, the placeholder prompts or the generated-image prompt (D4-85, D4-87). Chapter 21's failure plates with a wrong value carry none, as chapter 15's 25 failure plates carry none; the caption names the wrong value.
- **14, weight (all readers).** I found no words a reader never meets beyond the opener caption already on the register (chapter 20, `W['opener_caption']`). The working pages carry two lines twice in their markup, one copy hidden by width (R-23's status sentence and its lever definition). I did not measure their bytes.

## 5. For Dustin

1. **Rule 01.16, Rule 13.2 and H08's table still say "at the same length" for a contested pair.** Chapter 21 prints the atlas's stored readings at the length the record holds (D4-253), as DR-314 and DR-323 already allow for Act pieces. A reader who puts Rule 01.16 beside Reform R-23's page sees the guide break its own rule. *Recommendation:* Rule 01.16's length row gains "Readings quoted from a record print at the length the record holds (DR-37, DR-93); readings we write run the same length", and Rule 13.2's specification "Contested" cites it. Chapter 21 adds the matching labels (RP1) either way.
2. **Chart S66's source line ends "Steps as the law sets them, not how long agencies take."** That is the "X, not Y" turn chapter 02's W09 removes, in an approved chart the Act page prints. *Recommendation:* "Steps as the law sets them; how long an agency takes is its own practice", the wording the chart's own note already uses. Low.
3. **Routine for the main session, not a decision:** Loop R18's stored "How it adapts" says "are the other party’s instances" and names no party (H10). V6 prints it as stored (DR-37); *recommendation:* a row on the atlas V7.1 issue list, as D4-106 added row 47.

## 6. Tested

- Read whole, every string: `16-photography.json`, `20-web.json` and `21-atlas.json` (1,677 strings dumped by script and read line by line), the 86 specimen fragments of chapters 16, 20 and 21 (words and alts extracted by script), the three manifests' alts, the kit's 17 plate titles and view alts (A04 to A20) and spec alts, and the nine working pages' text (`work/build/exports/phase-4/*.html`, visible text and every `alt`, `aria-label` and `title`).
- Script sweep over 3,701 reader-facing strings: em dashes 0; en dashes 0; straight double quotes in reader text 0; straight apostrophes 32 (22 on atlas pages, 8 in chapter 21 failure plates, 2 in the A03 sample's alt); fillers 0 (one "Clearly" inside the Society of Professional Journalists' quotation); corporate verbs 0; hedges 4, each read and kept ("seems to lecture" describes how a crop looks; "probably made by an image generator" sizes the claim to the evidence; two "tend to" on the How to read page, in the atlas's own sign convention); "This chapter" openers 3, each after or as a statement of purpose, kept; ", never" turns 11 in the new chapters (CE15) and 2 in stored or approved text; "dark mode" 1; hyphen used as minus 0; Latin abbreviations 0; exclamation marks 1 (the retired V5 line in `s-20-6-failure`, sourced); numeric dates 0.
- Drift by script across chapters 01, 02, 03, 05, 07, 11, 12, 13, 14, 15, 17, 18 and 19 against 16, 20 and 21: theme words, date words, step and stage, grade words and glosses, kind words, ink words, "flow", L1, L3 and L8's names, width formats, "same length". L1, L3 and L8 match chapter 03 and 12 everywhere; grade words and glosses match Rule 13.3; step and stage match chapter 11 and 15's uses.
- Rule against plate, by reading: every rule's text and specification in the three chapters against its correct plate's words and the working pages.
- Pictures read: the phone first screens of the home, Act, atlas home, Loop R18 and Reform R-23 exports; the home page's top at 1440 px; R-23's grades and effects at 1440 px; and the capture `newsprint-1x/1440/s-20-9-correct.png`.
- Markup read: the R-23 tag list (no separators, no `aria-describedby` on any chip), the home drawing's and trackers' `aria-hidden`, and the built captions of `s-16-11-correct`, `s-16-10-correct`, `s-21-4-failure` and `s-21-9-failure` in the review page.
- The simulated reader panel below, from the exports and the page text.

### The simulated reader panel (DR-202: simulated, not tested with real people)

What each simulated reader said, kept apart from what I conclude.

| Reader | What it taught them | What confused them | The word that stopped them |
|---|---|---|---|
| A newcomer to civics on a phone | "A special district is a local government that state law sets up to do one job or a few"; how to comment and by when; that an even count of minus signs makes a loop that "feeds itself" | "This question reaches here" above any question; "Outside forces" over "Outside drivers"; Loop R18's head in codes; step 4 in the panel and step 4 in the chart | "docket"; then "Meadows levels 12 to 10" and "at high bite" on R-23 (stored) |
| A high school civics teacher | The tracker's states, chart S66, Rule 16.5's caption order, and 16.10's "answers to a survey, which run higher than counted ballots" | The Act page's two step counts; why H.R. 7008 pairs stock-trading limits with photo ID (the bill's content, not our framing) | "files once" in the Register's intro |
| A local reporter on deadline | Rule 20.4's tab titles, the share card, Rule 16.5's credit lines, alt text per crop (16.7) | Whether to print "Checked" (Act page) or "As of" (tracker card); what a "deck" is | "the lockmark’s 24 px master, 12 px, and the tagline" |
| A staffer at a partner organization who builds one page a month | The masthead's breakpoints and the menu's focus order (20.1, 20.2), Rule 20.9's measure | Rule 20.9's correct plate printing "4 panels"; "Its title, Menu, and Close the menu sit at the top" | "maskable" |
| A reader who leans left, for fairness | The Act page sets out the record and says no concern was filed; R-23 prints the Congressional Budget Office's job-loss estimate, which this reader said their side "would rather skip", and called that fair | Which party "the other party" is on Loop R18 | "the other party’s instances" |
| A reader who leans right, for fairness | The home page's four pieces read neutral; Loop R18 gives both parties' removals | Three of chapter 21's four views sit on topics this reader hears as aimed at their side, with no reason printed; R-23 leads with "little job loss" and puts the Congressional Budget Office under "Main limitation" | "Main limitation" |
| A screen reader user (simulated from the page text) | Tracker steps as lists ("Step 2, Hearing: never happened."), "Comment at Regulations.gov (another site)", Rule 16.7's alt texts that change with the crop | "Variable A4: Reform R-24 Reform R-25 Reform R-26 Reform R-31 also aim here"; "Variable EC7 A higher value means …"; "Start with Variable D2 presidential action without new legislation rising." | The run of four bare codes |

What I conclude from the panel: every chapter's first screen lets a newcomer say what the chapter is for and where to use it; the readers stalled on defined terms left undefined on the pages (CE3, CE6), on codes with no names (CE1, CE8), on studio words in public view (CE7), and on two counts or two dates for one thing (CE5, DF3). The two fairness readers disagreed about the four views and agreed about the Act page; the change both would accept is a printed selection rule (RP2) and matching labels on the contested pair (RP1).

## 7. Not tested

- Real readers of any kind (DR-202), and how any line sounds read aloud by a person or a real screen reader (DR-279); the screen reader row above is simulated from extracted page text, not from an accessibility tree.
- Any browser: I opened none, so nothing here was checked live, by keyboard or at other widths than the exports and one capture show.
- The facts the words carry: H.R. 7008's provisions, the Society of Professional Journalists' revision date ("revised October 4, 2026"), the docket's dates and pages, chart S04's figures and the platform help rows. Those are the evidence reader's.
- The full capture set, which held only `newsprint-1x` at 17:28 UTC; I read one capture from it and the kit's exports for the rest.
- The guide's built page beyond four captions read in the review page; the main page (`main/guide.html`) not opened.
- Approved chapters 01 to 15, 17 to 19 and 26 beyond the drift words listed in section 6, read by script.
- No byte measure of the duplicated lines in named place 14.
