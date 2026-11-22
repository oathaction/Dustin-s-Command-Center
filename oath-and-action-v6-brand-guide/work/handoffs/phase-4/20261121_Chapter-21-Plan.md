# Chapter 21 plan: The atlas

Data visualization lead, Phase 4, chat 11, November 21, 2026 (written 19:14 to 19:40 UTC, read with `date -u`). Written for the design director, who builds chapter 21 in its own chat from this plan, for the engineer, who draws its views in the application kit, and for the editor, who writes every word a reader sees. I sign off every atlas view the build draws. Brief: `work/handoffs/phase-4/20261121_Chat-11-Brief.md`, section 9.

Corrected in chat 11c by the data visualization lead, November 22, 2026 (22:27:15 UTC): sections 3.3, 5 (Rule 21.4's specifications) and 8 (T10) drop "the same length" and the citation of H08, which sets no length, for the record's own lengths (DR-314, DR-323) and ruling R15, and Rule 21.4's draft takes the editor's chat 11c words for it; section 3.1's title bar follows chapter 20 as built (23:20:29 UTC, ruling R17); logged as C1 to C6 in `work/handoffs/phase-4/20261122_Chat-11c-Dataviz-Lead-Notes.md`. Appendix A's rerun on November 22 matched Appendix B byte for byte, so no value changed.

Inputs read: my role file; `CLAUDE.md`; chapter 02's writing rules; the Gate 3 report's section 9; the decision log from Gate 3's approval to its end (G3-01 to G3-09, DR-301 to DR-311, D4-63's allocation of 655,000 bytes); Master Brief sections 8, 10, 13, 14, 15, 18 and 22; the architecture map's rows for chapters 21 and 28; the chapter 16 plan, whose form this plan follows; chapter 15's 25 rules and its generator's header and drawing functions; chapters 05, 10, 11, 12, 13, 17 and 18's rule lists, and Rules 05.1, 05.5, 10.8, 12.5, 12.7, 13.3 to 13.5, 13.9 to 13.11, 15.12, 15.13, 15.16, 15.20, 15.21, 17.10, 18.22 and 18.24 in full; System 1's page and generator, read by script (its views, its masthead and its drawing constants); Night Edition's loop page; the four favored concepts, Field Manual (03), The Circuit (09), Who Can Act (10) and Register (11), from their board images in `work/boards/phase-1/systems/`; the creative director's finishing list; the register rows ED-F1 to ED-F10, DR-37, UX-4, F-8, F-14 and F-15; the atlas V7.1 issue list, rows 1 to 46; the engineer's chat 10 allocation note and chat 11 contracts C4 to C6; the accessibility lead's chat 11 rulings, AL-01 to AL-18 for chapter 20 and AL-21 to AL-24 for chapter 21 (landed 19:04 UTC); the model, `work/extract/atlas-v7-data.json`, by script. The design director's chapter 20 plan landed at 19:18 UTC while this plan was in progress; section 3.1 builds the atlas's title bar under its masthead (its Rules 20.1 and 20.3).

Draft words in this plan show what each field must say. The editor writes the final words under chapter 02's rules. The atlas's own stored text (titles, summaries, cases, evidence notes) prints as the model stores it, and DR-37 keeps the rewrite of the atlas's own copy for its next version.

Every ID, sign, grade, delay and count below was read from the model by the query script in Appendix A, run from the project folder on November 21, 2026. Each value names its query in brackets, such as [Q09]. Appendix B lists what each query returned. The build re-reads every value from the model at build time and never copies one from this plan.

## 1. The chapter's idea

Our systems atlas, Who Do They Answer To?, is the brand's hardest application and its main test. Chapter 15 teaches how to draw a mechanism. Chapter 21 shows the atlas as a reader meets it on our website: a home page that draws the whole system and answers an everyday question, a page for each reform, the Register that files every connection with its evidence, and a page for each loop that a reader can step through. Every page sits under the site's masthead, with the atlas's own title bar beneath it (DR-307). Every ID a page prints sits in a typed chip, and every claim on a page reaches its evidence in one step: a chip, a figure or a step links straight to the record that grades it and names its source.

Chapter 21 cites chapter 15's rules wherever a page draws a mechanism and never restates them. Its own rules cover what a page adds: where the atlas sits in the site, what each view holds and in what order, how a page leads to its evidence, how the dark mode reads, and the test every atlas page passes before it ships.

The four views rotate across issues and sides by one standard of evidence (DR-93): a health care question on the home page, a wage reform on the reform page, Congress and the agencies on the Register, and presidential power over watchdogs on the loop page. Section 3.6 shows, view by view, the finding a reader on each side would rather skip (DR-55), each as the model records it.

## 2. Opener and intro

- **Number, anchor, title, part:** `21`, `atlas`, "The atlas", `applications`.
- **Instruction (fixed by the architecture map):** "Apply the system to the atlas, with typed IDs and evidence a step from every claim."
- **Opener plate, `s-21-home`:** the atlas home in four frames: 1440 px and 390 px on Newsprint, then 1440 px and 390 px in the dark mode (section 3.2). Draft caption: "The home page of our systems atlas inside our website, on Newsprint and in the dark mode at 1440 and 390 pixels. A reader has pressed the question “Why can the same care produce different bills?”, and the drawing lights the three parts of the system it reaches."
- **Intro, draft, two paragraphs:**
  1. "Our systems atlas, Who Do They Answer To?, lives inside our website, under the site's masthead, with a title bar of its own. This chapter shows its four kinds of page: the home page, which draws the whole system and starts from an everyday question; a page for each reform; the Register, which files each of the atlas's 118 connections once with its evidence; and a page for each loop, which a reader can step through."
  2. "Chapter 15 sets how each mechanism is drawn, and these pages use its rules as they stand. What this chapter adds is the page around the drawing. Every ID sits in a typed chip, every claim links to the record that grades it, and every page passes the atlas test before it ships."
  The 118 is read at build time [Q01].

## 3. The views

Each view is one application in the kit (section 9), drawn at 1440 px and 390 px on Newsprint and in the dark mode, four frames to a plate, as the brief asks. Every frame is a picture inside the guide (contract C4: `inert`, named by its alt), and the working page is the kit's standalone export, where the accessibility lead walks it (AL-18).

### 3.1 What every view shares: the site's masthead and the atlas's title bar

From top to bottom, every atlas page holds:

1. **The site's skip link, masthead and parts,** drawn by the kit's shared site parts (`work/build/app-kit/renderers/site-parts.mjs`, its `masthead` and `theme_switch`, as the engineer wrote them this chat) exactly as chapter 20's Rule 20.1 draws them, with "Who Do They Answer To?" as the current part (bold words, 2 px underline; Rule 18.6, AL-17). From chapter 20's plan (landed 19:18 UTC): at 1440 px an 80 px bar with L3 and the seven parts, then the theme switch on a 44 px row beneath them at the right edge, 16 px of space and a 1 px hairline; at 390 px a 56 px bar with L1 from the 24 px master and Menu, with the switch at the top of the menu; never sticky. Every part stays in the masthead's ink, Subscribe included, so the masthead spends no working red and the atlas's red target stays the view's one working red (Rules 05.3, 12.5).
2. **The atlas's title bar,** directly under the masthead, never a second banner (AL-17): the atlas's name, "Who Do They Answer To?", in the label style, its subtitle from the model, "The Oath & Action Systems Atlas" [Q01, `meta.subtitle`], and "Snapshot of October 15, 2026" [Q01], then a navigation named "Atlas views" holding Home, Loops, Reforms, The Register and How to read (draft words), with the current view marked as Rule 17.10 marks a current link in a masthead. At 390 px the title bar holds the atlas's name and a disclosure button, "Atlas views" (Rule 18.8), that opens the five links in place; the breadcrumb carries the reader's place (Rule 12.7).
3. **A breadcrumb** on every page below the home, `<nav aria-label="Breadcrumb">` (AL-09), such as "Home / Loops / Loop R18", and on those pages at 1440 px **the atlas locator** at the header's top right, 88 by 41 px, the parts as boxes and the current part filled in ink, hidden on phones (Rule 12.7).
4. **The view,** under one `<main>` with one h1 (AL-10).
5. **The site's footer,** on Charcoal in both themes, with its four lists (the pillars, the atlas, Oath & Action, and Help with its one link, Contact us) in the same order as on every other page (chapter 20's Rule 20.3, AL-04).

**Page titles (AL-01):** "[view] | Who Do They Answer To? | Oath & Action". Drafts for the editor: "Atlas home", "Reform R-23, a minimum wage that rises with an index", "The Register: Congress, agencies and public services", "Loop R18, weakening watchdogs". Each plate shows its page's title in words above its frames, read from the export's own `<title>` (AL-01).

**The title bar under chapter 20's masthead:** it starts directly under the masthead's 1 px hairline, on the page's grid columns (chapter 07): at 1440 px one 56 px row, the atlas's name, subtitle and snapshot at the left on columns 1 to 6 and the five views at the right on columns 7 to 12, each 44 px tall, then a 1 px `--oa-color-border-hairline` rule; at 390 px one 56 px row with the atlas's name and the "Atlas views" disclosure button, the five links opening beneath it as 44 px rows. The title bar is a Charcoal band in both themes, as chapter 20 as built opens its home page's atlas section (D4-189; brief 11c, section 5), a navigation and never a second banner: no wordmark, no copy of the site's parts, and on the dark page a 1 px hairline along its bottom edge (chat 11c ruling R17). If chapter 20's masthead measures change in its build, the title bar follows them and nothing else here moves.

**Color by screen (Rule 05.1 under DR-310):** each atlas page marks its sections with `data-oa-section` (contract C5), and the engineer's measure prints every light frame's first screen and each section's opening screen. Drawings and tables on Newsprint will likely run past 85 percent Newsprint, as the chat 10 article did (D4-11). Each view names one candidate Charcoal panel a section, which the design director turns on only where the measure asks for it: on the home page, the questions panel, as chapter 20's home page sets its own questions panel on Charcoal; on the reform page, the panel of its two grades; on the Register, the index's whole-atlas row as a Charcoal band; on the loop page, the stepper. The footer is its own section (chapter 20's Request R2). A panel never holds the red target, so the target stays on Newsprint at its edge (DR-305), and a red mark never sits on Prussian (Rule 05.3).

### 3.2 The atlas home (`s-21-home`)

Drawn from Concept 09, The Circuit (the whole system wired, with a count on every wire), and System 1's overview (the parts as boxes with their questions), finished by ED-F3 and ED-F5 (section 6).

**Entries and the values the build reads:**

- **The h1 and intro:** the atlas's question, "Who do they answer to?", and an intro whose counts come from the model: 51 variables, 118 connections, 23 loops, 20 of them with numbered steps, 50 reforms and 194 issue records, one of them retired (Issue I128) [Q01]. The intro's words are the editor's; DR-37 keeps the atlas's own walk-through copy for its next version, so the home carries no walk-through.
- **The system drawing,** on the first screen at 1440 px. Eight boxes, one per part, each with its plain name and question as Dustin's newest atlas gives them (DR-35, DR-41) and the model's own title beneath (DR-35's "the formal titles sit beneath"): Outside forces, Outside drivers (5 variables); Wealth, Economic structure (6); Voice, Political inputs (6); Elections, Electoral competition (5); Checks, Governing institutions (7); Policy, Legitimacy (2); Your household, How the economy reaches a household (12); Technology, Technology and its effects (8) [Q02]. Each box prints the count of connections that stay inside it: Wealth 6, Voice 5, Elections 5, Checks 7, Your household 11, Technology 3, and none in Policy or Outside forces [Q02]. Each arrow between two parts prints its count: 27 directed pairs of parts carry 81 connections, 38 among the five core parts, 28 to, from or within the economy and technology layers, and 15 from outside drivers [Q02]. The main circuit, Wealth to Voice (5), Voice to Elections (4), Elections to Checks (4), Checks to Policy (4) and Policy back to Wealth (3) [Q03], draws in the essential ink, and every other arrow in the subtle ink, as System 1 draws them. One arrow width throughout; the counts are printed numbers, and no width or size carries a count (Rule 15.1).
- **The switch,** a toggle button (Rule 18.2) whose words say what it shows, such as "Show every variable" (draft): pressed, each box opens in place to list its variables as pills with their own titles (Rule 15.2), 51 in all [Q01], and the counts stay. This is ED-F3's "Main flows / Every connection" switch, and it replaces System 1's second, lower drawing.
- **The everyday questions:** the 16 questions under the atlas's five hubs, Cost of living (4), Health and care (4), Work and financial security (3), Public services where you live (3), and Voice, power and information (2), each as a toggle button with its question as its words [Q04]. Hubs print by name only, with no chip and no ID (Rule 10.8).
- **The pressed question:** "Why can the same care produce different bills?" [Q04], drawn in Rule 17.10's pressed look (AL-21). The question's variables sit in three parts, Wealth (Variables A3 and A4), Checks (Variable D4) and Your household (Variables EC8 and EC9) [Q04], so those three boxes stay in full ink with the words "This question reaches here" (draft) and the other five turn to the muted state (Rule 17.8). The status line says the same in words. The answer panel under the questions prints the question's short answer as the atlas stores it [Q04]. Its one figure, "254% of Medicare rates in 2022", carries Claim CL1340 in its chip as a link to the claim's record, whose grade is well supported and whose period is 2020 to 2022 [Q04] (Rule 21.7).
- **Not on this view:** the walk-through (DR-37), a second drawing (ED-F3), any icon on a part's head (Rule 10.8; ED-F7 in section 6).

**At 390 px** the drawing becomes a stacked list of the eight boxes in the order effects travel, Outside forces, Wealth, Voice, Elections, Checks, Policy, Your household, Technology, each with its count inside and the counts to its neighbors printed as "5 to Voice" lines under it (DR-64 allows a phone drawing to change form when it carries the same data). The questions stack under their hubs.

### 3.3 The reform page (`s-21-reform`): Reform R-23

Drawn from Concept 10, Who Can Act (routes, a reform and its four outcome families), and Concept 03's Detail A (the reform at its target), as chapter 15's Rules 15.11, 15.12, 15.16 and 15.20 set them.

**Entry:** Reform R-23, "Minimum wage that rises with an index" [Q05]. Chosen because its evidence for the remedy is graded contested, so its page must print both readings its record holds, each at the length the record holds (DR-314, DR-323; chat 11c ruling R15), and because its record holds a finding each side may want to skip (section 3.6).

**Sections, in order, with the values the build reads:**

1. **Head:** the chip Reform R-23 and the title as the h1; its band, parameter, with the atlas's words for that band [Q05]; its summary as stored; its status, "As of" the date in words, October 15, 2026, from its own check date [Q05] (Rule 13.10).
2. **Where it acts:** a drawing of its two targets, Variable EC7, "Household income", and Variable A4, "Households' financial security", joined by the one connection between them, Connection LE15, "Higher income strengthens household security": plus, causal, under 2 years, documented [Q05]. The two variables' outlines turn red as the reform's targets (Rule 12.5); LE15 stays in ink, since it is not a target. Each variable prints its own sentence on what a higher value means [Q05]. The note names the reform and both targets in words (Rule 15.11). The record names Loop R6 as the loop it touches, and R6's chain does not hold either target [Q05], so the page names R6 in words with its chip and draws it nowhere.
3. **Other reforms at the same marks,** in ink (ED-F6): Reforms R-24, R-25, R-26 and R-31 also target Variable A4, and no other reform targets EC7 [Q05]. Each prints as a chip with "aims here" (draft) beside A4.
4. **Two grades, apart** (Rule 15.12): the evidence of the problem, documented, and the evidence for the remedy, contested, each with Rule 13.3's word and gloss and the atlas's words quoted [Q05]. Because the remedy is contested, its panel sets the two readings the atlas's text holds side by side, the stored text whole and in order, split at one sentence: little job loss within studied ranges (Cengiz, Dube, Lindner and Zipperer, 2019), and the Congressional Budget Office's 2019 median estimate for a $15 federal floor by 2025 of 1.3 million jobs lost and 1.3 million people lifted from poverty, with wide uncertainty [Q05]. Each reading names its source a step away (Rule 21.7).
5. **Four effects, one family to a row** (Rule 15.16), "As of October 15, 2026": Quality of democracy (DR-39), 0, no expected effect; Government efficacy, 0; Economic performance, "0 to −S at high bite"; Income and wealth equality, "+M lower tail" [Q05, Q13]. Each code prints whole with its qualifier, in a true minus (house rule H07). The atlas's confidence words print as its own, quoted: "high to 60% of median; low above" [Q05]. No row adds them.
6. **Routes** (Rule 15.24): State statute, Legislatures, high; State ballot, Voters, high; Local, Cities, medium, with the atlas's note "Where not preempted."; Federal statute, Congress, low; each "Not checked", since none of the four carries a check date [Q05] (Rule 13.10). Each route's name links to its workflow (Rule 15.22).
7. **Complements:** Reform R-25 [Q05], chip and title.
8. **Sources for this page,** in a disclosure (Rule 18.8) closed on load: the three sources the record lists, from the U.S. Department of Labor's Wage and Hour Division, the Quarterly Journal of Economics (2019) and the Congressional Budget Office (2019) [Q05], each in Rule 13.6's six parts as far as the source record holds them.

**At 390 px** the drawing stacks EC7 above A4, the four tags wrap under A4, and the effects become four rows of label, pips and code.

### 3.4 The evidence view, the Register (`s-21-register`): sheet D04 open

Drawn from Concept 11, Register ("The whole atlas, line by line"). The index rebuilds Concept 11's table from the model alone: each connection files once, on the sheet of the variable it moves; a variable in the economy or technology layer files on sheet EC or TC; the loops column counts numbered loops through a sheet's variables; the reforms column counts reforms that are not rejected with a target on the sheet [Q06]. Run against the model, this method reproduces Concept 11's printed counts on all twelve sheets [Q06].

**The index, one row per sheet [Q06]:**

| Sheet | Variables | Connections | Loops | Reforms | Issue records | Documented | Well supported | Plausible | Contested | Hypothesis |
|---|---|---|---|---|---|---|---|---|---|---|
| Domain D01, News, records and public information | 3 | 9 | 2 | 3 | 17 | 1 | 3 | 3 | 0 | 2 |
| Domain D02, Elections and representation | 8 | 19 | 10 | 14 | 22 | 5 | 9 | 5 | 0 | 0 |
| Domain D03, Money, lobbying and influence | 2 | 7 | 8 | 7 | 17 | 1 | 2 | 3 | 0 | 1 |
| Domain D04, Congress, agencies and public services | 3 | 10 | 6 | 10 | 20 | 2 | 2 | 5 | 0 | 1 |
| Domain D05, Checks on power and equal justice | 3 | 7 | 5 | 7 | 26 | 2 | 2 | 3 | 0 | 0 |
| Domain D06, Competition and market power | 2 | 1 | 0 | 2 | 17 | 0 | 0 | 1 | 0 | 0 |
| Domain D07, Work, pay and bargaining power | 1 | 4 | 2 | 4 | 20 | 0 | 2 | 1 | 1 | 0 |
| Domain D08, Taxes, wealth and economic security | 3 | 13 | 3 | 6 | 19 | 5 | 7 | 1 | 0 | 0 |
| Domain D09, Housing, health care and getting ahead | 2 | 4 | 1 | 3 | 19 | 0 | 2 | 2 | 0 | 0 |
| Domain D10, Taking part, trust and shared norms | 4 | 10 | 4 | 6 | 17 | 0 | 3 | 5 | 2 | 0 |
| How the economy reaches a household (layer) | 12 | 25 | 0 | 19 | none filed | 11 | 4 | 5 | 4 | 1 |
| Technology and its effects (layer) | 8 | 9 | 0 | 5 | none filed | 5 | 1 | 1 | 0 | 2 |
| The whole atlas | 51 | 118 | 20 | 49 | 194, one retired | 32 | 37 | 35 | 7 | 7 |

The whole-atlas row counts each loop and reform once, though many reach several sheets, and says so in a note under the table, as Concept 11 does. Its grade counts come from [Q01]. The two layer rows take no chip, since Rule 10.8 names layers in words. The grade columns replace Concept 11's evidence bars, which ordered grades by darkness; Rule 15.25 resolved that a grade never prints as darkness (its row on Concept 11's bars) and Rule 13.5 says the same, so each grade is a count under a head that carries its 40 px line sample (Rule 13.4) and its word.

**Sheet D04 open,** chosen because the loop page's first step, Connection L14, files here [Q09], so the plates show a reader's one step from a loop to its evidence:

- **Head:** chip Domain D04, "Congress, agencies and public services", and its everyday question, "Why does it take so long to get a benefit, a permit or a new law?" [Q07].
- **Its three variables:** Variable D1, "Congress's ability to write and check policy"; Variable D4, "Ability to investigate and enforce the rules"; Variable D5, "Quality of public services", each with its sentence on what a higher value means [Q07].
- **Its ten connections, one row each** (Rule 21.9) [Q07]:

| Connection | From, to | Sign | Type | Delay | Grade | The atlas's citation |
|---|---|---|---|---|---|---|
| L10 | B4 to D1 | minus | causal | 2 to 10 years | Well supported | Binder 2003; Lee 2016 |
| L12 | D2 to D1 | minus | causal | over 10 years | Plausible | Chafetz 2017 |
| L14 | D2 to D4 | minus | causal | under 2 years | Documented | 17 IGs removed Jan 24, 2025; ruled unlawful Sept 24, 2025; FEC without quorum since May 1, 2025 |
| L17 | E1 to D4 | plus | causal | 2 to 10 years | Plausible | HB6 investigation (DOJ 2023); GAO mandate structure |
| L19 | E1 to D1 | minus | causal | over 10 years | Hypothesis | 1995 staff cuts and OTA abolition (event) |
| L21 | E2 to D5 | plus | causal | over 10 years | Plausible | Luttmer and Singhal 2014; Bargain and Aminjonov 2020 |
| L22 | E1 to D5 | minus | money | 2 to 10 years | Documented | TIGTA and OPM staffing data (official) |
| T03 | D4 to D5 | plus | causal | 2 to 10 years | Plausible | GAO recommendations implemented |
| L54 | C5 to D5 | plus | causal | 2 to 10 years | Well supported | Ferraz and Finan 2011; Besley 2006 |
| LT15 | TC5 to D5 | plus | causal | 2 to 10 years | Plausible | GAO (W117, W118); Direct File volumes (W120) |

  On the page each ID is a chip, each variable is named by its title, the sign prints as its tag and word (raises, lowers), the delay as ticks and words, the grade as its line sample and word, and the citation as the atlas stores it, shortened above only for this plan. Each row carries an anchor, such as `#register-l14`, so a chip anywhere in the atlas links to its line.
- **The rejected option on this sheet:** Reform R-35, "Rejected option: term limits for legislators", which targets Connections L18 and L19 and so files on sheets D03 and D04 [Q08], with its effects, Quality of democracy −S and Government efficacy −M, and its remedy graded well supported as a finding of harm, in the atlas's own words, "Here the grade measures confidence in a finding of harm" [Q08] (Rule 21.10).
- **Its issue records:** 20, of which 11 are graded documented, 6 well supported and 3 plausible [Q07], behind a Filters button (Rule 18.16). The plate shows the filter "Variable D4" on, with 9 of 20 records showing: Issues I053, I055, I056, I057, I061, I064 and I164, and Issues X04 and X14, each with its title as stored and its grade word [Q07] (Rule 21.11). Variable D1 names 8 records, D5 names 11, and 2 name none of the three [Q07].

**At 390 px** the index becomes one card per sheet, its counts in a two-column list, and the connection table becomes one block per connection with its six facts as labeled lines (Rule 18.10's table stays the markup, restyled by its container; no sideways scroll).

### 3.5 The loop page (`s-21-loop`): Loop R18

Drawn from System 1's loop page and Night Edition's, finished by ED-F4 and ED-F6, with the stepper ruled by AL-22 and AL-24.

**Entry:** Loop R18, "Weakening watchdogs lowers the cost of further unilateral action" [Q09]. Chosen because its two steps carry two grades, documented and plausible, so the page teaches the weakest step on a short loop; its two minus signs teach the sign arithmetic; three reforms name it; and its case records instances from both parties as the model holds them (section 3.6).

**Sections, in order, with the values the build reads:**

1. **Head:** the chip Loop R18 and its kind, reinforcing [Q09]; the h1, the atlas's title in quotation marks (Rule 18.22); under it the grade line, from the atlas's grade text "documented for D2 to D4; plausible for D4 to D2" [Q09], set in display words with chips; its closure in the atlas's words, "closed: every step is a numbered connection", and its delay, 2 to 10 years [Q09].
2. **Read aloud, with the arithmetic of its signs** (ED-F4, ED-F6): start with more presidential action without new legislation; Connection L14 carries a minus, so the ability to investigate and enforce the rules falls; Connection L15 carries a minus, so presidential action without new legislation rises, and the loop comes back to where it began, moving the same way [Q09]. Two minus signs, an even count, make it reinforcing (Rule 15.6). The line beside it is ED-F6's, "Built from the signs: start with more, flip at each minus." (draft; the editor's words).
3. **The drawing,** chapter 15's two-variable loop: Variable D2, "Presidential action without new legislation", and Variable D4, "Ability to investigate and enforce the rules", each by its own title (DR-265) [Q09]. Step 1, Connection L14: minus, causal, under 2 years, documented, solid with the record square and one tick. Step 2, Connection L15: minus, causal, 2 to 10 years, plausible, dashed with two ticks, marked "Weakest step" [Q09] (Rules 13.4, 15.13). The weakest step carries ED-F4's line, "The loop holds only as firmly as this link." (draft).
4. **The stepper** (Rule 18.22, Rule 21.13): Play, Reset the loop, Previous step, Next step (AL-22). Holds, counted from the draft status lines by AL-24's method: step 1, 39 words, 9,750 ms; step 2, 58 words, 14,500 ms [Q10]. The editor's final lines are re-timed by the same count.
5. **The reform chooser** (Rule 15.20): the reforms whose own records name Loop R18, Reforms R-11, R-15 and R-48 [Q09], as a named radio group, the first chosen on load. Chosen on the plate: Reform R-11, "A Federal Election Commission able to act", whose targets, Variable D4 and Connections L14 and L15, all sit on the drawing and turn red [Q09]. Its panel: band feedback; effects, Quality of democracy "+M precondition", Government efficacy +S, Economic performance 0, Income and wealth equality 0; routes Chamber rule or confirmation, medium, and Federal statute, low, both "Not checked" [Q09]. Reforms R-15 and R-48 also aim at both steps, so each step carries them as ink tags, "Reform R-15 and Reform R-48 also aim here" (draft) (ED-F6). The loop's own record lists only R-11 and R-15 [Q09]; V7.1 item 29 already asks the atlas to make the two lists agree, and the page follows the reforms' own records, as Rule 15.20 does.
6. **The loop in the atlas's words:** its summary, case, qualification and adaptation as stored [Q09]. The case documents the 2025 removals of seventeen inspectors general and the court's ruling of September 24, 2025; the adaptation names the 2021 removals the model calls "the other party's instances" [Q09]. Both print as stored.
7. **Evidence for each step,** one step away: the chip Connection L14 links to its line on sheet D04 and Connection L15 to its line on sheet D05 [Q09] (Rule 21.7).
8. **Issue records on this loop:** a count, 8, as a link to the Register filtered to them [Q09]. The plate prints no titles here: three of the eight titles sit on V7.1 item 44's list of judging verbs, and the Register prints titles with their grades.

**At 390 px** the drawing sits above the stepper, the four buttons form a two-by-two grid in reading order, Play and Reset the loop, then Previous step and Next step (AL-22), and the chooser's three choices stack.

### 3.6 How the four views rotate across issues and sides

| View | Issue | A finding the record holds that one side may want to skip | The finding the other side may want to skip |
|---|---|---|---|
| Home | Health care prices | Private plans paid hospitals 254% of Medicare rates in 2022, well supported, and hospitals with few nearby rivals win higher rates [Q04] | Medicare itself pays more for some services in hospital outpatient departments than in doctors' offices [Q04] |
| Reform R-23 | Wages | The remedy is graded contested, with the Congressional Budget Office's estimate of 1.3 million jobs lost beside 1.3 million people lifted from poverty [Q05] | The federal minimum wage has been $7.25 an hour since July 2009, documented, and 30 states and the District of Columbia set a higher one [Q05] |
| Register, sheet D04 | Congress, agencies and public services | Connection L14, documented: presidential removals weaken watchdog agencies [Q07] | Reform R-35, term limits, is the atlas's one rejected option, graded well supported as a finding of harm, though the atlas's own route note records that 87% of adults favored congressional term limits (Pew, July 2023) [Q08, Q16] |
| Loop R18 | Presidential power over watchdogs | The case documents the 2025 removals of seventeen inspectors general [Q09] | The adaptation records the other party's 2021 removals, upheld under Collins v. Yellen, and the return step is only plausible [Q09] |

Every finding above prints at the grade the model gives it, with nothing added or softened to even the sides (DR-93), and every title is read from the left and the right before it ships (DR-55).

### 3.7 The typed ID chips (`s-21-chips`)

One plate, on Newsprint and on Charcoal, each chip plain and as a link (Rule 18.24), one for each of Rule 13.9's ten kind words, each with a real record and its name [Q12]: Variable D4, Connection L14, Loop R18, Reform R-23, Issue I164, Claim CL1340, Domain D04, Route SS ("State statute"), Rule change RL19 and Delivery case DL05. Then the model's colliding codes side by side, each pair with both names [Q12]: Variable B4 and Loop B4; Loop R1 and Reform R-01; Variable D4 and Domain D04; Variable X1 and Issue X01 (V7.1 item 12).

### 3.8 How to read (`s-21-how-to-read`)

The conventions sheet ED-F4 asks for, drawn from System 3's: one page that lists every mark the atlas's pages use, each with its words and the rule that sets it: the sign tag with raises and lowers (Rule 15.3), the type words (15.4), authority's open diamond (15.5), the five grade lines with their glosses (13.3, 13.4), the delay ticks (13.5), the record square (13.4), the hollow line (15.7), the red target (12.5), the typed chip (13.9) and the pressed question (17.10). Two frames: 1440 px on Newsprint and 390 px in the dark mode. Every view's title bar links to it.

## 4. Groups

| Group | Before rule | Title | Line (draft) |
|---|---|---|---|
| 1 | 21.1 | The atlas in our website | The atlas sits under the site's masthead with a title bar of its own, and its home page draws the whole system and starts from a reader's question. |
| 2 | 21.4 | A page for each record | A reform's page reads its own record in the order a reader asks, and every ID on it opens the record it names. |
| 3 | 21.8 | The Register | The Register files each of the atlas's connections once, with its sign, its grade and its source, and keeps what the atlas rejected in view. |
| 4 | 21.12 | Loop pages | A loop page reads the loop's signs aloud, names its weakest step and lets a reader step through it at a pace they can follow. |
| 5 | 21.15 | The dark mode and the atlas test | The atlas reads the same on Charcoal, and every page passes one test against the model before it ships. |

## 5. The rules

Sixteen rules and one extra, as the brief asks. Every plate below is drawn by the application kit from a content file that names only IDs and choices (section 9), and the kit reads every value from the model at build time. Sizes are each frame's CSS width. A rule whose correct plate is a view plate (21.4, 21.8 and 21.12) shows that view's four frames; the opener carries the home view.

### Group 1. The atlas in our website

#### 21.1 Set every atlas page under the site's masthead, with the atlas's title bar beneath.

- **Teaches:** where the atlas lives in the site (DR-307) and what a reader sees above every atlas page.
- **Rule, draft:** "Our systems atlas is one part of our website, so every atlas page opens with the site's masthead, with Who Do They Answer To? marked as the part the reader is in. Directly under it, the atlas's title bar names the atlas, gives the date of its snapshot and lists its views: Home, Loops, Reforms, The Register and How to read. Pages below the home add a breadcrumb, and on wide screens a small locator that shows where the page sits in the whole system. Each page's title names the view first, then the atlas, then Oath & Action."
- **Why, draft:** "A reader who reaches the atlas from a search or a shared link still sees whose site they are on and can reach every other part of it. The title bar keeps the atlas's own views one step away without a second masthead."
- **Correct plate `s-21-1-correct`:** the top of the loop page (section 3.5) at 1440 px on Newsprint and at 390 px on Newsprint with the "Atlas views" disclosure open: the site's skip link (shown as focused, Rule 18.5), masthead with the atlas as the current part, the title bar, the breadcrumb "Home / Loops / Loop R18" and, at 1440 px, the locator with the Checks part filled. Above the frames, the page title as the export's `<title>` holds it. About 1440 by 260 and 390 by 420 px.
- **Failure plate `s-21-1-failure`:** the same page with a second banner of the atlas's own, its own wordmark and its own copy of the site's parts, no current part marked in the site's masthead, and the page title "Oath & Action" alone. Draft caption: "Fails Rule 21.1. The atlas brings a masthead of its own, so a reader sees two sets of links and cannot tell which site they are on, and the tab's title names no page."
- **Specifications:** Order: skip link, site masthead, atlas title bar, breadcrumb, main, site footer. Title bar: the atlas's name in `oa.type.label`, the subtitle and snapshot date in `oa.type.bodySmall`, the views in a `<nav aria-label="Atlas views">`. Current view: bold words and a 2 px underline (Rule 17.10). At 390 px: the atlas's name and an "Atlas views" disclosure, 44 px tall. Locator: 88 by 41 px at the header's top right, hidden on phones (Rule 12.7). Page title: "[view] | Who Do They Answer To? | Oath & Action" (AL-01). Landmarks: one banner (the site's), two named navigations plus the breadcrumb, one main, one contentinfo (AL-09, AL-17).
- **Basis:** DR-307; the accessibility lead's AL-01, AL-09 and AL-17; ED-F8 and D2-65 (no newspaper's name in the header or title); design judgment for the title bar's contents.
- **Tokens:** `oa.type.label`, `oa.type.bodySmall`, `oa.border.width.underline`, `oa.color.border.hairline.onNewsprint`, `oa.size.target.touch`.
- **Related:** Rules 12.7, 17.10, 18.5, 18.6, 18.7, 18.8; chapter 20's masthead and footer rules.
- **WCAG:** 1.3.1, 2.4.1, 2.4.2, 2.4.3, 3.2.3, 3.2.6, 4.1.2.
- **For builders, draft:** "Draw the masthead and footer from the website's own renderer, add the atlas's title bar as a second named navigation, and build each page title from the view's own words."

#### 21.2 Open the atlas home on the whole system, with a count on every flow.

- **Teaches:** the home page's first screen: the system drawn in its parts, the counts the model holds, and one switch that opens every part to its variables (ED-F3).
- **Rule, draft:** "Start the atlas's home page with the whole system on the first screen: one box for each part, each with its name, its question and the count of connections inside it, and one arrow for each pair of parts that connect, with the count of connections it carries. Draw the main circuit in full ink and the other flows in a lighter ink, all at one width. A switch opens every box in place to show its variables, and closes them again. Draw the system once on the page."
- **Why, draft:** "A newcomer sees how the parts fit together before reading any one of them, and every number on the drawing is a count a reader can check in the Register. One drawing that opens in place keeps the first screen short."
- **Correct plate `s-21-2-correct`:** the home drawing with the switch pressed, every box open to its variables' pills (51 in all [Q01]), at 1440 px on Newsprint. About 1440 by 900 px.
- **Failure plate `s-21-2-failure`:** the same drawing with each arrow's width grown with its count and no key, so Your household to Wealth, which carries 7, looks heavier than any step of the main circuit [Q02]. Draft caption: "Fails Rule 21.2. The arrows widen with their counts and nothing on the drawing says what a width measures, so the eye reads weight where the page prints a number."
- **Specifications:** Parts: eight boxes in the order effects travel, Outside forces, Wealth, Voice, Elections, Checks, Policy, Your household, Technology, each with its plain name, its question and the model's title beneath (DR-35). Boxes and pills: a part takes a box with square corners; a variable takes a pill (Rule 15.2); this is ED-F9's one rule. Counts: inside each box, and on each arrow, in `oa.type.dataLabel` with tabular figures, read at build time [Q02]. Ink: the main circuit in `oa.color.graphic.essential`, other flows in `oa.color.graphic.subtle`, one width, 2 px. Switch: a toggle button (Rule 18.2) with its words, `aria-pressed`. Redrawing: when a model version adds or removes a part, the boxes reflow on the same grid in the order effects travel, and the build stops if a count on the drawing differs from the model (ED-F10). At 390 px: a stacked list with "[count] to [part]" lines (DR-64).
- **Basis:** Concept 09, The Circuit; System 1's overview; ED-F3, ED-F9 and ED-F10; DR-35; Rule 15.1; the model's layer and region fields [Q02, Q03].
- **Tokens:** `oa.color.graphic.essential.onNewsprint`, `oa.color.graphic.subtle.onNewsprint`, `oa.type.dataLabel`, `oa.type.label`, `oa.border.width.hairline`.
- **Related:** Rules 07.2, 12.7, 15.1, 15.2, 15.9, 18.2.
- **WCAG:** 1.1.1 (the drawing's text equivalent is its parts and counts as a list), 1.3.1, 1.4.10, 1.4.11, 4.1.2.
- **For builders, draft:** "Count every number on the drawing from the model at build time, and stop the build when a count and the model disagree."

#### 21.3 Light the parts an everyday question reaches, and say which they are in words.

- **Teaches:** how the home page answers a reader's question on the drawing (ED-F5, second half) and how a pressed question looks (UX-4, AL-21).
- **Rule, draft:** "Offer the atlas's everyday questions under their hubs, each as a button. When a reader presses one, mark it pressed with a check, bold words and a heavier edge, keep the parts its variables sit in at full strength with the words This question reaches here, and mute the rest. A status line names the parts in words, and the answer opens below with each figure linked to its evidence."
- **Why, draft:** "A reader who arrives with a bill in hand sees at once which parts of the system decide it. Words carry the result, so a reader who cannot see the shading, or who prints the page in gray, gets the same answer."
- **Correct plate `s-21-3-correct`:** the questions and the drawing's three lit parts, "Why can the same care produce different bills?" pressed beside unpressed questions, in four frames: 1440 px and 390 px on Newsprint and on Charcoal (AL-21). Lit: Wealth, Checks and Your household [Q04].
- **Failure plate `s-21-3-failure`:** the pressed question shown by bold words alone, and the three parts tinted with no words. Draft caption: "Fails Rule 21.3. Only the weight of its words shows which question is pressed, and only a tint shows which parts it reaches, so the answer is lost in gray print and to a reader who cannot see the tint."
- **Specifications:** Question: a toggle button, `aria-pressed="true"` when pressed; one pressed at a time. Pressed look: the selected check before the words, bold words, a 2 px edge in the strong border color, where an unpressed question keeps 1 px (Rule 17.10, AL-21). Lit parts: the parts that hold the question's variables, read from the question's own record [Q04]; full strength with the words "This question reaches here"; the rest in `oa.color.state.muted.mark` and `oa.color.state.muted.text`. Status line: names the parts in words, once per press, never on load. Hubs: named in words, no chip (Rule 10.8).
- **Basis:** ED-F5; UX-4 and the accessibility lead's AL-21; D2-1152; the pathway's `model_refs` [Q04].
- **Tokens:** `oa.color.border.strong.onNewsprint`, `oa.border.width.rule`, `oa.size.icon.medium`, `oa.color.state.muted.mark.onNewsprint`, `oa.color.state.muted.text.onNewsprint`, and their Charcoal twins.
- **Related:** Rules 05.4, 17.8, 17.10, 18.2, 21.7.
- **WCAG:** 1.4.1, 4.1.2, 4.1.3.
- **For builders, draft:** "Light a part only when the question's own record names a variable in it, and write the same list in the status line."

### Group 2. A page for each record

#### 21.4 Build a reform's page from its own record, in the order a reader asks.

- **Teaches:** the order of a reform's page and how it applies chapter 15's reform rules as one page (Concepts 03 and 10).
- **Rule, draft:** "Give each reform a page that answers a reader's questions in order: what it is and its status, with its date; where it acts, drawn at its targets; how sure our atlas is that the problem exists and that the remedy works, as two grades; what it would change in each of the four outcome families, one to a row; how it could pass, route by route, each with its check date or Not checked; and where its evidence comes from. When the atlas grades a remedy contested, set the readings its record holds side by side, in the atlas's own words."
- **Why, draft:** "A reader who asks whether a reform would work gets the evidence for that answer before the routes, and a contested remedy shows both sides of the dispute, as our atlas records it."
- **Correct plate:** the reform view, `s-21-reform` (section 3.3), four frames.
- **Failure plate `s-21-4-failure`:** Reform R-23's remedy panel with one reading, "Within studied ranges, evidence finds little job loss", under the word Well supported, and the budget office's estimate left out [Q05]. Draft caption: "Fails Rule 21.4. The panel keeps the finding of little job loss, drops the budget office's estimate and grades the remedy well supported. Our atlas grades it contested and records both."
- **Specifications:** Order: head and status; where it acts; the two grades; the four effects; routes; complements; sources. Contested remedy: the stored text whole and in order, split at one sentence into two readings, side by side at 1440 px and one after the other at 390 px, each at the length the record holds, each with its source a step away (DR-314, DR-323; R15). Effects: Rule 15.16's rows, codes whole with qualifiers, true minus (H07), "Quality of democracy" for DQ (DR-39). Routes: Rule 15.24's row form with "Not checked" where the record holds no date (Rule 13.10). Status: "As of" and the date in words.
- **Basis:** Rules 15.11, 15.12, 15.16, 15.20 and 15.24, applied as one page; house rule H08; Concept 10, Who Can Act, without its strand widths (Rule 15.25's row on strand widths); Concept 03's Detail A.
- **Tokens:** `oa.color.data.emphasisRed.onNewsprint`, `oa.color.graphic.essential.onNewsprint`, `oa.chart.grade.documented`, `oa.type.dataLabel`, `oa.type.section`.
- **Related:** Rules 13.3, 13.5, 13.10, 15.11, 15.12, 15.16, 15.20, 15.24, 18.8.
- **WCAG:** 1.3.1, 1.4.1, 2.4.6.
- **For builders, draft:** "Read every field from the reform's own record, and set a contested remedy's two readings as one pair."

#### 21.5 Tag reforms that share a target in ink, and keep the red for this one.

- **Teaches:** ED-F6's ink tags: how a page shows that other reforms aim at the same target without a second red.
- **Rule, draft:** "On a reform's page, the reform's own targets turn red. Where other reforms in our atlas aim at the same variable or connection, tag that mark with each one's chip and the words aims here, in the text's ink. On a loop page, where a reader chooses one reform, the others that aim at the loop take the same ink tags."
- **Why, draft:** "A reader learns that several reforms compete for the same lever, and the one red still shows which reform the page is about (Rule 05.3)."
- **Correct plate `s-21-5-correct`:** Reform R-23's targets, Variables EC7 and A4, with their red outlines, and four ink tags at A4: Reforms R-24, R-25, R-26 and R-31 [Q05]. At 1440 px and 390 px on Newsprint.
- **Failure plate `s-21-5-failure`:** the same drawing with all five reforms' tags in red. Draft caption: "Fails Rule 21.5. Five reforms share the red, so the page has five working reds and no longer shows which reform it is about."
- **Specifications:** Tag: the reform's typed chip and "aims here", in `oa.type.dataLabel`, in the text's ink, beside the mark, 6 px from it. Several tags: stacked under one leader line; past four, "and [n] more" with a link to the list. Red: the page's own reform only (Rule 12.5); the tags never take red, an outline or a fill.
- **Basis:** ED-F6 (from System 4); Rules 05.3 and 12.5; the reforms' own target lists [Q05, Q09].
- **Tokens:** `oa.type.dataLabel`, `oa.color.text.primary.onNewsprint`, `oa.color.data.emphasisRed.onNewsprint`.
- **Related:** Rules 05.3, 12.5, 12.6, 15.11, 15.20.
- **WCAG:** 1.4.1, 2.4.4.
- **For builders, draft:** "Find every reform that names the same target in its own record, and draw its tag in ink."

#### 21.6 Name every record in its typed chip, and let the chip open the record's page.

- **Teaches:** chips across the atlas's pages, the ten kinds of record and the codes the model repeats (Master Brief section 8, item 7).
- **Rule, draft:** "Every ID on an atlas page sits in its typed chip, the kind of record in words and its code, such as Loop R18 or Reform R-23. A chip that names a record with a page of its own links to that page, and the first time a page names a record, its name follows the chip."
- **Why, draft:** "Our atlas uses B4 for a variable and for a loop, and R1 sits one hyphen from R-01. The word in the chip says which record a reader is looking at, and the link takes them to it."
- **Correct plate `s-21-chips`** (section 3.7): the ten kinds, each with a real record, plain and linked, then the four colliding pairs [Q12], on Newsprint and on Charcoal.
- **Failure plate `s-21-6-failure`:** a list under the heading Variables of bare codes with names: "B4 Electoral consequences can improve public performance", "D4 Ability to investigate and enforce the rules", "R1 Wealth and political influence reinforce each other" [Q12]. Draft caption: "Fails Rule 21.6. Bare codes let a loop pass for a variable: B4 and R1 here are loops, filed under Variables."
- **Specifications:** Kinds: Rule 13.9's ten words. Chip: Rule 18.24's, plain or as a link with a target at least 24 px tall. Link: to the record's own page, or for a connection to its Register line; the record's name as the link's description where the words around it do not name it. Check: every chip's ID exists under its kind in the model (Rule 21.16).
- **Basis:** Rules 13.9 and 18.24; house rule H11; V7.1 item 12; the model's IDs [Q12].
- **Tokens:** `oa.type.dataLabel`, `oa.color.border.strong.onNewsprint`, `oa.size.target.minimum`.
- **Related:** Rules 13.9, 18.5, 18.24.
- **WCAG:** 1.3.1, 2.4.4, 2.5.8.
- **For builders, draft:** "Take each chip's kind word from where its ID lives in the model, never from its letters."

#### 21.7 Put the evidence one step from every claim.

- **Teaches:** the chapter's instruction: how each claim, figure and step on an atlas page reaches the record that grades it.
- **Rule, draft:** "Every claim an atlas page makes links to its evidence in one step. A figure links to the atlas's claim record, which gives the claim, its grade, the people and place it covers, its period, its limit and its source. A connection's chip links to its line in the Register, with its grade and citation. A reform's sources sit in a disclosure on its own page."
- **Why, draft:** "A reader who doubts a number or a step can check it without leaving the page they are reading, and we never ask them to trust a claim we cannot show."
- **Correct plate `s-21-7-correct`:** two paths at 1440 px on Newsprint: the home answer's figure, "254% of Medicare rates in 2022", with its chip Claim CL1340 opened to the claim's record (grade well supported; privately insured patients in participating employer and insurer data; United States, by state; 2020 to 2022; its limitation as stored) [Q04]; and the loop page's step chip Connection L14 beside its line on sheet D04 [Q07, Q09].
- **Failure plate `s-21-7-failure`:** the same figure with the answer's 29 sources listed at the page's foot and none tied to the figure [Q04]. Draft caption: "Fails Rule 21.7. The figure points to a list of 29 sources at the foot of the page, and a reader cannot tell which one holds it."
- **Specifications:** Figure: its claim's chip right after it, linked; the claim's record in a disclosure or its own page. Connection: its chip links to `#register-<id>` on its sheet. Reform: its sources in a disclosure, closed on load, open on paper (Rule 18.8). Steps: one link or one disclosure, never a search. Source lines: Rule 13.6's six parts as the source record holds them.
- **Basis:** the architecture map's instruction for chapter 21; Rules 13.6 and 13.12; the model's claim and source records [Q04, Q05].
- **Tokens:** `oa.type.caption`, `oa.type.dataLabel`, `oa.border.width.underline`.
- **Related:** Rules 13.6, 13.9, 14.13, 18.5, 18.8, 21.9.
- **WCAG:** 2.4.4, 1.3.1.
- **For builders, draft:** "Give every figure and every connection on a page a link to its own record, and fail the build when one has none."

### Group 3. The Register

#### 21.8 Index the Register by sheet, and count each grade in words.

- **Teaches:** the Register's index (Concept 11), rebuilt from the model, with grades counted and never shaded.
- **Rule, draft:** "Open the Register with one row for each of its twelve sheets, one for each domain and one for each of the two lower layers, giving the sheet's variables, connections, loops, reforms and issue records, and then how many of its connections carry each grade. A last row counts the whole atlas, each loop and reform once."
- **Why, draft:** "A reader sees where the atlas's evidence is strong and where it is thin, sheet by sheet, in numbers they can check line by line."
- **Correct plate:** the Register view, `s-21-register` (section 3.4), four frames.
- **Failure plate `s-21-8-failure`:** the index with each sheet's grades as one bar shaded from dark to light and no counts, as Concept 11 drew it. Draft caption: "Fails Rule 21.8. Shading ranks the grades and hides the counts, so a reader cannot tell how many connections on a sheet are a hypothesis."
- **Specifications:** Rows: Domains D01 to D10 with their chips, then the two layers in words (Rule 10.8), then the whole atlas. Counts: as section 3.4 sets the method [Q06]; the whole row's grades from all 118 connections [Q01]. Grade columns: Rule 13.3's five words in its order, each head with its 40 px line sample (Rule 13.4); never a shade, width or bar. Issue records: "none filed" for the two layers; the whole row says one is retired [Q01]. Table: Rule 18.10's markup with tabular figures; at 390 px a card per sheet.
- **Basis:** Concept 11, Register; Rule 15.25's row on Concept 11's evidence bars; Rule 13.5; the method that reproduces Concept 11's counts [Q06].
- **Tokens:** `oa.type.dataLabel`, `oa.chart.grade.documented`, `oa.chart.grade.plausible`, `oa.chart.grade.contested`, `oa.chart.grade.hypothesis`, `oa.chart.grade.minRun`.
- **Related:** Rules 10.8, 13.3, 13.4, 13.5, 14.13, 18.10.
- **WCAG:** 1.3.1, 1.4.1, 1.4.10.
- **For builders, draft:** "Count every column from the model by one written method, and print it with the table."

#### 21.9 File each connection once, on the sheet of the variable it moves.

- **Teaches:** the Register's line: one row per connection, with every mark chapter 13 gives it.
- **Rule, draft:** "On each sheet, list every connection that moves one of the sheet's variables, once, with its chip, the variables it joins, its sign as a tag and a word, its type, its delay, its grade as a line and a word, and the atlas's citation. Give each line an address of its own, so a chip anywhere in the atlas can link to it."
- **Why, draft:** "Filed once, every connection has one home a reader can find, and the sheets add up to the atlas's 118."
- **Correct plate `s-21-9-correct`:** sheet D10, "Taking part, trust and shared norms", its ten lines at 1440 px on Newsprint, two of them contested, Connections L09 and L47, in the dash and dot with the word Contested [Q15].
- **Failure plate `s-21-9-failure`:** a Register that files each connection on both its variables' sheets, so the whole-atlas row reads 236 connections. Draft caption: "Fails Rule 21.9. Every connection appears on two sheets, so the Register counts 236 where our atlas holds 118."
- **Specifications:** Filing: by the variable the connection moves (its "to"); a variable in the economy or technology layer files on that layer's sheet; a variable with two domains files on the first (V7.1 item 21). Columns: chip; from and to by title with chips; sign tag and raises or lowers; type in words (Rule 15.4); delay ticks and words; grade line and word; citation as stored. Authority: decides and the open diamond, no sign (Rule 15.5). Address: `id="register-<connection id>"`.
- **Basis:** Concept 11; Rules 13.4, 13.5, 15.3 to 15.5; the filing method [Q06, Q07, Q15].
- **Tokens:** `oa.chart.grade.*`, `oa.type.dataLabel`, `oa.color.graphic.essential.onNewsprint`.
- **Related:** Rules 13.4, 13.5, 15.3, 15.4, 15.5, 18.10, 21.7.
- **WCAG:** 1.3.1, 1.4.1.
- **For builders, draft:** "File each connection by its variable's sheet and stop the build when the sheets do not sum to the model's count."

#### 21.10 Keep the rejected option and the connections left off the map on their sheets.

- **Teaches:** what the Register shows of the atlas's own negatives: the reform it rejects and the connections it reviewed and did not draw.
- **Rule, draft:** "Where our atlas rejects a reform, keep it on the sheets its targets file on, under the label Rejected option, with its grade read as the atlas reads it: for a rejected option, a strong grade measures confidence in harm. Where the atlas reviewed a connection and did not draw it, list it on its sheet under Reviewed and not drawn, with its two variables and the atlas's reason, and draw no line."
- **Why, draft:** "What the atlas decided against is evidence too, and a reader who meets a popular idea there sees the finding behind the decision."
- **Correct plate `s-21-10-correct`:** two blocks at 390 px on Newsprint: sheet D04's Rejected option, Reform R-35, with its two effects, Quality of democracy −S and Government efficacy −M, and the atlas's words "Here the grade measures confidence in a finding of harm" [Q08]; and sheet D10's two connections reviewed and not drawn, from Variable TC1 and from Variable X4 to Variable B4, each with the atlas's reason [Q15].
- **Failure plate `s-21-10-failure`:** Reform R-35 listed among the sheet's reforms with no label and its remedy grade, Well supported, printed as if for a remedy that works. Draft caption: "Fails Rule 21.10. Term limits read as a well supported remedy, though our atlas rejects them on strong evidence of harm."
- **Specifications:** Label: "Rejected option" as the block's heading, the reform's title as stored. Grade: the atlas's words quoted under the grade word. Reviewed and not drawn: Rule 15.10's form, from and to with chips, the reason quoted, no line in any pattern. Counts: rejected reforms stay out of the index's reforms column [Q06].
- **Basis:** Rule 15.10; the model's `rejected` flag and `rejectedLinks` [Q08, Q15]; Concept 11, which keeps the rejected option in the evidence view.
- **Tokens:** `oa.type.label`, `oa.type.bodySmall`, `oa.color.border.hairline.onNewsprint`.
- **Related:** Rules 13.3, 15.10, 15.12.
- **WCAG:** 1.3.1.
- **For builders, draft:** "Read the rejected flag and the reviewed connections from the model, and file each on its targets' sheets."

#### 21.11 Filter a sheet's issue records by variable, and say how many show.

- **Teaches:** ED-F4's condition filters, on the Register's issue lists.
- **Rule, draft:** "Under each sheet's connections, list its issue records with their grades. Let a reader narrow the list to the records that name one of the sheet's variables, with one Filters button that says how many filters are on, and a line that says how many records show out of how many."
- **Why, draft:** "A sheet can hold twenty or more records, and a reader who cares about one variable finds its records without reading all of them."
- **Correct plate `s-21-11-correct`:** sheet D04's records with the filter Variable D4 on, "9 of 20 issue records" [Q07], at 390 px on Newsprint and in the dark mode.
- **Failure plate `s-21-11-failure`:** the same list filtered by three colored tabs with no count, its records' grade words gone. Draft caption: "Fails Rule 21.11. Color alone shows which filter is on, nothing says how many records are hidden, and the grades are gone."
- **Specifications:** Control: Rule 18.16's Filters button, "Filters, 1 on" (draft), with one check box per variable, each with its chip and its count of records [Q07]. Count line: a status line on each change, never on load (Rule 18.15). Each record: chip, title as stored, grade word. Records that name none of the sheet's variables show only with every filter off [Q07].
- **Basis:** ED-F4; Rule 18.16; the issue records' `nodes` fields [Q07].
- **Tokens:** `oa.size.target.touch`, `oa.type.ui`, `oa.type.dataLabel`.
- **Related:** Rules 18.15, 18.16, 18.19.
- **WCAG:** 1.3.1, 2.1.1, 4.1.2, 4.1.3.
- **For builders, draft:** "Build the filters from the variables on the sheet and count each from the records' own variable lists."

### Group 4. Loop pages

#### 21.12 Head a loop page with its grade line and the arithmetic of its signs.

- **Teaches:** the top of a loop page: the loop's name and grade, its signs read aloud with their arithmetic (ED-F4, ED-F6), and its weakest step.
- **Rule, draft:** "Open a loop page with the loop's chip, its kind and its title from our atlas in quotation marks, and under the title the grade of each step from the atlas's own words. Read the loop aloud in one sentence that starts with more of its first variable and turns at each minus sign, and say beside it that an even count of minus signs makes a loop that feeds itself. On the drawing, name the weakest step and say that the loop holds only as firmly as that step."
- **Why, draft:** "The arithmetic lets a reader check the loop's kind from its signs, and naming the weakest step keeps the loop's title from claiming more than its least certain link."
- **Correct plate:** the loop view, `s-21-loop` (section 3.5), four frames.
- **Failure plate `s-21-12-failure`:** Loop R18's head graded Documented, the grade of its first step, with no reading of its signs and no weakest step [Q09]. Draft caption: "Fails Rule 21.12. The head grades Loop R18 documented, the grade of its first step. Our atlas grades the return step plausible, and the loop holds only as firmly as that step."
- **Specifications:** Head: chip, kind word, title in quotation marks as the h1, grade line in display words with chips (Rule 18.22, H08). Read aloud: one sentence from the signs, built by chapter 15's `read_aloud`; the arithmetic line beside it (ED-F6's words are the editor's). Weakest step: "Weakest step" under its words where the atlas's evidence summary names it (Rule 15.13), with ED-F4's line. Closure and delay: in the atlas's words (Rule 15.7).
- **Basis:** ED-F4 and ED-F6 (from Systems 3 and 4); Rules 15.6, 15.7, 15.13 and 18.22; the model's loop record [Q09].
- **Tokens:** `oa.type.title`, `oa.type.intro`, `oa.chart.grade.documented`, `oa.chart.grade.plausible`.
- **Related:** Rules 13.2, 15.3, 15.6, 15.7, 15.13, 18.22.
- **WCAG:** 1.1.1, 1.3.1, 2.4.6.
- **For builders, draft:** "Build the read-aloud line from the signs, and stop the build when the loop's kind and its count of minus signs disagree."

#### 21.13 Run the atlas's stepper in the guide's order and at the guide's pace.

- **Teaches:** the loop page's stepper, with the register rows F-8 and F-15 settled (AL-22, AL-24).
- **Rule, draft:** "Every loop page steps through its loop with the guide's loop stepper: Play, Reset the loop, Previous step and Next step, in that order, on every screen. Play holds each step about a quarter of a second for every word the status line reads, and never less than six seconds. Nothing plays until a reader presses Play."
- **Why, draft:** "A reader who learns the stepper anywhere in our work finds the same buttons in the same place here, and the pace lets a reader, or a screen reader, finish each step before the next."
- **Correct plate `s-21-13-correct`:** Loop R18's stepper at 390 px on Newsprint, its four buttons in a two-by-two grid in reading order, and at 1440 px in the dark mode, in one row, each on step 2 with its status line [Q10]. The specification table prints each step's hold: 9,750 and 14,500 ms [Q10].
- **Failure plate `s-21-13-failure`:** the stepper as System 1 runs it today: Play, Previous step, Next step, Reset, at 3,200 ms a step (registers F-8 and F-15). Draft caption: "Fails Rule 21.13. The buttons run in another order than the rest of our work, and each step moves on after about three seconds, before a reader can finish it."
- **Specifications:** Order and names: Play, Reset the loop, Previous step, Next step (Rule 18.22, AL-22). Phone: a two-by-two grid, Play and Reset the loop, then Previous step and Next step. Hold: 250 ms a word of everything the status line reads, "Step 1 of 2:" included, never under 6,000 ms, with reduced motion too (D2-972, D2-1019, AL-24); computed by script from the editor's final lines, as D3-1755 did. Code: chapter 18's `c-18-loop-stepper`, read from its files, each step's `data-oa-hold` set from the count.
- **Basis:** Rule 18.22; D2-1154; the accessibility lead's AL-22 and AL-24; registers F-8 and F-15.
- **Tokens:** `oa.size.target.touch`, `oa.size.icon.medium`, `oa.color.state.selected.bar.onNewsprint`, `oa.border.width.bar`.
- **Related:** Rules 11.16, 15.19, 17.3, 17.4, 18.22.
- **WCAG:** 2.1.1, 2.2.2, 2.4.3, 3.2.4, 4.1.3; 2.3.3 (level AAA, the guide's own pace, AL-24).
- **For builders, draft:** "Read the stepper from chapter 18's files, and time each hold from its status line's words."

#### 21.14 List every loop on one index, by kind, closure and grade.

- **Teaches:** ED-F4's loop index.
- **Rule, draft:** "Give the atlas one index of its loops: the reinforcing ones and then the balancing ones, each with its chip, its title, its number of steps, its count of minus signs, how it closes in the atlas's words and its grade in the atlas's words. Order each group as the atlas lists it. Leave out any score or rank of strength."
- **Why, draft:** "A reader can find a loop by its kind and see at a glance which loops rest on a hypothesis or close only in concept."
- **Correct plate `s-21-14-correct`:** the index of all 23 loops, 18 reinforcing and 5 balancing [Q11], at 1440 px and 390 px on Newsprint.
- **Failure plate `s-21-14-failure`:** the loops ranked by a bar of strength. Draft caption: "Fails Rule 21.14. A bar ranks each loop by a strength our atlas does not measure."
- **Specifications:** Groups: Reinforcing (18), Balancing (5) [Q11]. Row: chip, title, steps, minus signs, closure and grade as stored, each a link to the loop's page. The three conceptual loops print "no numbered chain" with their grade (Rule 15.18). Never: a strength, a score, or a size for a loop (Rule 15.21).
- **Basis:** ED-F4 (System 3's loop index); Rules 15.6, 15.7, 15.18, 15.21; the model's loops [Q11].
- **Tokens:** `oa.type.dataLabel`, `oa.type.bodySmall`.
- **Related:** Rules 15.6, 15.7, 15.18, 15.21, 18.10.
- **WCAG:** 1.3.1.
- **For builders, draft:** "Read every row from the loop's own record, in the atlas's order."

#### Extra after 21.14: How to read (`s-21-how-to-read`)

The conventions sheet of section 3.8, at 1440 px on Newsprint and at 390 px in the dark mode, each mark with its words and the rule that sets it. Draft caption: "Our atlas's How to read page, which lists every mark its pages use with the rule that sets it."

### Group 5. The dark mode and the atlas test

#### 21.15 Draw the atlas's dark mode from the Charcoal tokens, and measure every mark.

- **Teaches:** the atlas on Charcoal (DR-204, from Night Edition), with register row F-14 settled (AL-23).
- **Rule, draft:** "In the dark mode, every atlas page draws on Charcoal from the tokens set for Charcoal: text in Newsprint, quieter words and muted marks in Dim Newsprint, the selected bar in Newsprint and the red target in Pillar Red. Line patterns, sign tags, ticks and chips keep their shapes. Measure every mark on the page's own pixels before it ships."
- **Why, draft:** "A reader who sets their device to dark reads the same atlas with the same marks, and every mark keeps the contrast it needs on Charcoal."
- **Correct plate `s-21-15-correct`:** Loop R18's drawing with Reform R-11's targets in red and the chooser beside it, at 1440 px in the dark mode, with a table of the ratios measured on the plate's pixels; the ratios the tokens give [Q14]: text Newsprint on Charcoal 13.29 to 1; muted marks and secondary text Dim Newsprint 7.26 to 1; the red target Pillar Red 4.49 to 1; a decorative hairline Stone 3.10 to 1.
- **Failure plate `s-21-15-failure`:** the same drawing in the colors Night Edition's kit uses today: muted marks in Stone and the selection in White (register F-14). Draft caption: "Fails Rule 21.15. Muted marks in Stone clear 3 to 1 by a tenth, and the selection draws in White, a color no token sets on Charcoal."
- **Specifications:** Ground: `oa.color.surface.charcoal`. Text: `oa.color.text.primary.onCharcoal`, 13.29 to 1; secondary: `oa.color.text.secondary.onCharcoal`, 7.26 to 1. Marks: essential `oa.color.graphic.essential.onCharcoal`; muted `oa.color.state.muted.mark.onCharcoal`, never Stone (AL-23). Selected bar: `oa.color.state.selected.bar.onCharcoal`, Newsprint, never White. Red target: `oa.color.data.emphasisRed.onCharcoal`, 4.49 to 1, with no edge (DR-305's edge is for Newsprint). Layer frames: `oa.color.graphic.subtle.onCharcoal`. Hairlines that carry no meaning: Stone, 3.10 to 1 (Rule 05.5). Every color from a token read from `tokens.css`, never a hex in the renderer (AL-23). Switch: the site's (Rule 18.4), remembered across a reload (AL-08).
- **Basis:** DR-36 and DR-204 (Night Edition as the dark mode); ED-F2; register F-14 and the accessibility lead's AL-23; measured ratios [Q14].
- **Tokens:** as in the specifications.
- **Related:** Rules 05.2, 05.5, 17.10, 18.4.
- **WCAG:** 1.4.3, 1.4.11.
- **For builders, draft:** "Name a token for every color in a dark view, and check each frame's pixels with the contrast script."

#### 21.16 Test every atlas page against the model before it ships.

- **Teaches:** the atlas system test (section 8) and what it hands to chapter 28.
- **Rule, draft:** "Before any atlas page ships, run the atlas test. It reads the page and the model together and checks every ID, sign, type, delay, grade, count and date the page prints against the model, every red mark against the chosen reform's targets, every effect against its family, every link from a claim to its evidence, and the stepper's order and pace. A single failure stops the page."
- **Why, draft:** "The atlas changes as its evidence changes, and a page that copies a value can drift from the record without anyone seeing. The test reads the record each time."
- **Correct plate `s-21-16-correct`:** the test's report for the four views, one line per check with what it read and its result, from the build's own run.
- **Failure plate `s-21-16-failure`:** a loop page that prints Connection L15 as Documented, beside the test's line that stops it: the page, the mark, the value printed and the model's value, plausible [Q09]. Draft caption: "Fails Rule 21.16. The page grades Connection L15 documented. Our atlas grades it plausible, and the test stops the page."
- **Specifications:** the checks of section 8, each with its pass condition; output one line a check, PASS or FAIL with the page, the record and both values; any FAIL stops the generator and the strict build; a self-test with planted faults proves each check catches its fault.
- **Basis:** Master Brief section 14 and the architecture map (the atlas system test folds into chapter 21, its lines into chapter 28); chapter 15's generator checks, extended to pages.
- **Tokens:** `oa.type.dataLabel`, `oa.type.bodySmall`.
- **Related:** Rules 13.9, 15.6, 15.11, 15.16, 19.7, 19.8; chapter 28.
- **WCAG:** none of its own; it checks 1.3.1 and 4.1.2 markup on every view.
- **For builders, draft:** "Run the atlas test on every build, and treat a failure as a stop."

## 6. The finishing list: how each item lands

The creative director's finishing list for System 1 (DR-36), as the register's rows ED-F1 to ED-F10 carry it, with DR-37.

| Item | What it asks | How it lands in chapter 21 |
|---|---|---|
| ED-F1 | A layer rule down the left edge of every box, in Prussian, Verdigris and Stone, teaching "Color is the layer" | **Waits for Dustin.** Approved work forbids it: Rule 15.25's resolution on layer colors (G3-03) reads "Layers coded by a frame and a name, never a color", and Rule 15.9 frames layers with a 1 px rule and a name. A left rule in ink would not code the layer either: at 4 px it is Rule 17.10's selected bar and at 2 px its pressed edge. Chapter 21 draws the parts as Rule 15.9 frames them. The signature the item wanted is tested on the built views: the creative director reruns the wall test in chat 12 with the wordmark covered, on Newsprint with the pointing sign tag (DR-38), the record square, the typed chips and the red target. If it still fails, Dustin chooses at Phase 4 board 1 between reopening Rule 15.25's row for a colored layer rule and leaving the boxes as they are. On Charcoal, Prussian measures 1.41 to 1 and would need its lifted tint, 6.18 to 1 [Q14], if he chooses color |
| ED-F2 | Newsprint, and Night Edition's Charcoal as the dark mode | **Lands** in every view (DR-121, DR-204) and in Rule 21.15 |
| ED-F3 | One first-screen drawing that opens in place to every variable; drop the second drawing; shorten each walk-through stop | **Lands** in Rule 21.2: the switch opens every box in place, and the page draws the system once. The walk-through's words are the atlas's copy, which DR-37 keeps for its next version, so the home carries no walk-through; the kit's `home` view keeps a template for a stop (its question, two sentences, its variables, one named flow and its grade counts in words, Rule 21.8) for that version to fill. System 2's evidence bar becomes counts in words, as Rule 21.8 sets |
| ED-F4 | Sign arithmetic on loop pages; "The loop holds only as firmly as this link"; condition filters on problem lists; a loop index; System 3's conventions sheet as How to read | **Lands:** the arithmetic and the weakest-step line in Rule 21.12, the filters in Rule 21.11 on the Register's issue lists, the index in Rule 21.14, the conventions sheet in the extra after Rule 21.14 |
| ED-F5 | "Why it matters" under each variable, and lit parts for a question | **Half lands.** The lit parts land in Rule 21.3. "Why it matters" waits for the atlas's next version: the model holds no such field [Q17], and the lines the five editorial systems printed came from the dark atlas's plain-language layer, whose copy DR-37 keeps for that version. Each variable prints the model's own sentence on what a higher value means (Rule 15.2), and the kit keeps a slot under it for the next version's field |
| ED-F6 | "Built from the signs: start with more, flip at each minus." beside each read-aloud line; ink tags such as "R-02 aims here" | **Lands** in Rules 21.12 and 21.5; the line's final words are the editor's |
| ED-F7 | One Civic Line icon per part head at 24 px; icons out of loop pills | **Settled by approved Rule 10.8**, which draws the atlas's variables and reforms and names its other parts in words. A part is neither, so its head takes its name and question with no icon, and loop pills hold titles alone (Rule 15.2). The register row can close as settled; that is the main session's call (section 13) |
| ED-F8 | Drop the newspaper's name from the header and title | **Lands** in Rule 21.1: the title bar names the atlas, and each page title follows AL-01 |
| ED-F9 | A craft pass at twice size: labels at 13 px or more, no step label ending on one word, one rule for boxes and pills | **Lands** as specifications: every label from a type token at 13 px or more (the atlas test checks it, section 8), chapter 15's balanced wrapping for step labels (its `rows_of`), and Rule 21.2's rule, boxes for parts and pills for variables. The pass itself runs at the chat 12 review on the built views |
| ED-F10 | Tokens for the pill, sign tag, ticks and layer rule; six view templates; the build script as generator; a rule for redrawing the first screen | **Lands in part.** The views are the kit's templates (section 9) and the kit is the generator. Rule 21.2 holds the redrawing rule. The tokens are proposed in section 9.4 for Phase 5's token version, as G3-04 did for the chart roles; the layer rule's token waits for ED-F1 |
| DR-37 | Rewrite the overview's walk-through and the page's copy | **Stays deferred** to the atlas's next version. The plates print the atlas's stored text as stored, and every word the plates add is the editor's |

## 7. The accessibility lead's rulings, applied

| Ruling | Register row | Where it lands |
|---|---|---|
| AL-21: a pressed question takes Rule 17.10's one look: the selected check, bold words, a 2 px edge; `aria-pressed` | UX-4 | Rule 21.3 and its plate, pressed beside unpressed at 1440 and 390 px, on Newsprint and Charcoal; the home view |
| AL-22: the stepper runs Play, Reset the loop, Previous step, Next step everywhere; a two-by-two grid on phones in that reading order | F-8 | Rule 21.13 and its plate; the loop view |
| AL-23: on Charcoal, muted marks in `--oa-color-state-muted-mark-on-charcoal` (7.26 to 1), never Stone; the selected bar in `--oa-color-state-selected-bar-on-charcoal`, never White; every color from a token, ratios measured on the plate's pixels | F-14 | Rule 21.15 and its plate; every dark frame; the atlas test's color check |
| AL-24: 250 ms a word of everything the status line reads, "Step 2 of 3:" included, never under 6 seconds, reduced motion too; nothing plays until Play; each loop's holds printed, counted by script | F-15 | Rule 21.13; Loop R18's holds, 9,750 and 14,500 ms from the draft lines [Q10], re-counted from the editor's lines |
| AL-17: the site's masthead with the atlas as the current part; the title bar a second navigation named for what it holds; AL-01's three-part title; the site's footer | none | Rule 21.1; section 3.1 |
| AL-18 and contract C4: every frame in the guide is an inert picture named by its alt; the working pages are the exports | none | Every plate; the accessibility lead walks the exports |

## 8. The atlas system test

**What it is.** One script that reads every atlas view the kit draws, in its standalone export and as each plate's frames, together with the model, and checks that each page says what the model holds and works as the guide's rules require. The architecture map folds the atlas system test into chapter 21 and hands its pass or fail lines to chapter 28. Proposed path: `work/build/app-kit/tools/atlas_test.py`, run by the kit's build and by the strict guide build under the lock; the chapter 21 build chat confirms the owner.

**How the pages make themselves checkable.** Every atlas mark carries its record in data attributes the renderer writes from the model: `data-atlas-kind` and `data-atlas-id` on chips and marks, `data-sign`, `data-type`, `data-delay` and `data-grade` on connections, `data-count` and `data-count-of` on every printed count, `data-red="working"` on red marks (Rule 12.5's marker), `data-effect-family` and `data-effect-code` on effect rows, `data-route` and `data-checked` on routes, and `data-evidence-href` on every claim, figure and step. The test reads those and the visible words.

**The checks, each with its pass condition:**

| # | Check | Passes when |
|---|---|---|
| T1 | Typed IDs | Every ID in reader text sits in a chip; each chip's kind word matches where its ID lives in the model (Rule 13.9's ten kinds); no bare code (H11) |
| T2 | Connection marks | Every printed sign, type, delay and grade matches the connection's record, and its line pattern matches its grade (Rule 13.4) |
| T3 | Counts | Every number with `data-count` equals the model's count by the method this plan writes down (sections 3.2 and 3.4) |
| T4 | Loops | Each numbered loop's kind matches its count of minus signs; the read-aloud line turns at each minus; the weakest step is the one the atlas's evidence summary names |
| T5 | Authority | No authority connection carries a sign or sits in a loop (Rule 15.5) |
| T6 | Red | Red marks sit only on the chosen reform's own targets; one working red a view; every other reform's tag in ink (Rules 05.3, 12.5, 21.5) |
| T7 | Effects | Four rows a reform, one per family, each code and qualifier whole as stored, a true minus; no total, average or score anywhere (Rule 15.16) |
| T8 | Routes and dates | Every route prints its own check date or "Not checked"; every status prints "As of" and its date; the snapshot date prints in the title bar (Rule 13.10) |
| T9 | Evidence a step away | Every figure, connection chip and reform on a page has one link or disclosure to its own record, and the target exists (Rule 21.7) |
| T10 | Grades in words | Every grade prints in Rule 13.3's display words; a contested remedy prints its stored text whole and in order, split at one sentence into two blocks with the same standing, and the line prints each block's length (chat 11c ruling R15) |
| T11 | Stepper | Buttons in AL-22's order with their names; each hold is 250 ms a word of its status line, never under 6,000 ms (AL-24) |
| T12 | Pressed and lit | A pressed question carries `aria-pressed`, the check and the 2 px edge; lit parts are the parts of the question's own variables, named in the status line (AL-21) |
| T13 | Colors | Every color in a view resolves to a token for its ground; dark muted marks and the selected bar use AL-23's tokens; text at 4.5 to 1 and marks at 3 to 1 on the frame's pixels |
| T14 | Type | Every word from a type token, none under 13 px; no step label's last line holds one word (ED-F9) |
| T15 | Site frame | The site's masthead with the atlas as the current part, the title bar as a navigation named "Atlas views", the breadcrumb below the home, the site's footer with Help in its place, the page title in AL-01's three parts |
| T16 | Words the atlas retired | No newspaper's name (ED-F8), no editor's disclosure (DR-100), no bare loop or reform code in a title |

**How it passes or fails.** It prints one line a check and view, PASS or FAIL, and for a failure the page, the frame, the record, the value printed and the model's value, as Rule 21.16's failure plate shows. Any FAIL stops the kit's build and the strict guide build. A self-test plants one fault for each check in a copy of a view's export, never in the model, such as Connection L15 printed as documented [Q09] or a route dated from its reform's status, and passes only when every planted fault is caught and the clean views stay quiet, as the guide check's own self-test does (D4-90).

**What it does not check.** Whether the atlas's own findings are right: the test holds the pages to the model, and the model's faults go to the V7.1 issue list (G3-03). Screen readers, Safari, Firefox and real phones are listed as not tested at Gate 4 (DR-279).

**The lines it hands to chapter 28,** draft words for the standards checklist, each one line a publisher can tick:

1. Every atlas ID sits in a typed chip whose kind matches the model.
2. Every sign, type, delay and grade beside a connection matches the model.
3. Every count on an atlas page matches the model.
4. Each loop's kind matches its count of minus signs, and its weakest step is named.
5. No authority connection carries a sign or sits in a loop.
6. Red marks only the chosen reform's own targets, once in a view.
7. A reform's four effects print apart, whole, with no total.
8. Every route prints its check date or "Not checked", and every status its date.
9. Every figure, step and reform reaches its evidence in one step.
10. The loop stepper runs Play, Reset the loop, Previous step, Next step, at 250 ms a word and never under six seconds.
11. Every dark view takes its colors from the Charcoal tokens and passes 4.5 to 1 for text and 3 to 1 for marks.
12. Every atlas page sits under the site's masthead, with the atlas's title bar and a three-part page title.

## 9. What the application kit needs

### 9.1 One new renderer type, `atlas-page`

`work/build/app-kit/renderers/atlas-page.mjs` draws an atlas page inside the website's shell: it takes the skip link, masthead, menu and theme switch from `site-parts.mjs` and the footer from the website's page renderer, by importing their functions (never by copying their markup), and adds the title bar, breadcrumb and locator (section 3.1). The engineer's chat 11 header for `site-parts.mjs` names `web-site.mjs` as the page renderers that wrap these parts; `atlas-page` follows the same pattern. Its view templates: `home`, `reform`, `register`, `loop`, `loop-index`, `how-to-read`, and `part` and `issue` for the atlas's next pages (templates only; no plate this chapter). Its shared style goes into the page once, under contract C4, and weighs against chapter 21.

### 9.2 Content files that name only IDs

Each view's content file in `work/build/app-kit/specs/` holds choices, never values: for example `{"view": "loop", "loop": "R18", "chosen_reform": "R-11"}`, `{"view": "reform", "reform": "R-23"}`, `{"view": "register", "open_sheet": "D04", "filter": ["D4"]}`, `{"view": "home", "pressed_question": "Why can the same care produce different bills?", "every_variable": false}`, plus the frames `1440-light`, `390-light`, `1440-dark`, `390-dark`. The renderer reads every value from `work/extract/atlas-v7-data.json` and lists its SHA-256 in the plate's `inputs` (C4), so a changed model makes the guide build warn and the strict build fail until the plates are redrawn. The application IDs are the engineer's to assign (A-numbers after chapter 20's).

### 9.3 One source of drawing

The atlas's figures come from chapter 15's own drawing code: its loop, connection and pill functions in `work/build/scripts/phase-3/phase3_ch15_build.py`, which draw with System 1's `wire_marks` as chapter 15 does. A small figure step, proposed as `work/build/app-kit/tools/atlas_figures.py`, imports them with `importlib` (as chapter 15 imports chapter 13's generator, read and never edited) and writes each figure's SVG to a file the renderer places. The home drawing of parts and flows is new geometry, and System 1's overview drawing in its `build_system.py` is its model. Code sets come from chapter 18's files: `c-18-id-chip`, `c-18-loop-stepper` (with each `data-oa-hold` set from the count), `c-18-choice` and `c-18-disclosure` for the reform chooser, `c-18-filter-bar` for the filters, and the toggle of Rule 18.2. Icons come from the guide's sprite (C4).

### 9.4 Tokens proposed for Phase 5's token version (ED-F10)

None is written this chat; each passes the five conditions of Master Brief section 10 when it is registered. Values are System 1's, as the token build notes list them (`work/handoffs/phase-2/20261106_Token-Build-Notes.md`): `oa.atlas.pill.minHeight` 44 px; `oa.atlas.pill.stroke` 2 px and `oa.atlas.pill.strokeSketched` 1 px; `oa.atlas.signTag` sizes by line weight (body, point, height, sign length and bar: 14, 6, 16, 8 and 2 px at 2 px); `oa.atlas.arrowhead` by weight (10 by 8 px at 2 px); `oa.atlas.bend` radii (8, 12 and 18 px at 2, 3 and 6 px); `oa.atlas.panel.width` 420 px; `oa.atlas.countChip.height` 26 px, 22 px compact. Until they exist, the figure step reads these values from chapter 15's and System 1's code, never from numbers typed into the kit.

### 9.5 Exports

For each view, a standalone HTML page with the working masthead, menu, switch, stepper, chooser and filters (the pages the accessibility lead walks), and one PNG a frame, into `work/build/exports/phase-4/` under the studio's file names, listed in the exports manifest, with `check-dimensions.py` reading each PNG's size and the contrast script each frame's pixels.

## 10. WCAG 2.2 criteria the chapter meets

Criteria text: the accessibility lead's notes, read from the W3C on November 21, 2026. Chapter 21 moves no criterion on chapter 19's map; each row below is met elsewhere already, and chapter 21 adds the atlas's pages to its evidence.

| Criterion | Level | Rules |
|---|---|---|
| 1.1.1 Non-text Content | A | 21.2, 21.12 (each drawing's parts, counts and steps as text) |
| 1.3.1 Info and Relationships | A | 21.1, 21.4, 21.6 to 21.12, 21.14 |
| 1.4.1 Use of Color | A | 21.3, 21.4, 21.5, 21.8, 21.9 |
| 1.4.3 Contrast (Minimum) | AA | 21.15 |
| 1.4.10 Reflow | AA | 21.2, 21.8 (every view at 390 px, no sideways scroll) |
| 1.4.11 Non-text Contrast | AA | 21.2, 21.15 |
| 2.1.1 Keyboard | A | 21.11, 21.13 |
| 2.2.2 Pause, Stop, Hide | A | 21.13 |
| 2.4.1 Bypass Blocks | A | 21.1 |
| 2.4.2 Page Titled | A | 21.1 |
| 2.4.3 Focus Order | A | 21.1, 21.13 |
| 2.4.4 Link Purpose (In Context) | A | 21.5, 21.6, 21.7 |
| 2.4.6 Headings and Labels | AA | 21.4, 21.12 |
| 2.5.8 Target Size (Minimum) | AA | 21.6 (linked chips at 24 px), 21.11 and 21.13 (44 px) |
| 3.2.3 Consistent Navigation | AA | 21.1 |
| 3.2.4 Consistent Identification | AA | 21.13 (AL-22) |
| 3.2.6 Consistent Help | A | 21.1 (the site's footer) |
| 4.1.2 Name, Role, Value | A | 21.1, 21.2, 21.3, 21.11 |
| 4.1.3 Status Messages | AA | 21.3, 21.11, 21.13 |
| 2.3.3 Animation from Interactions | AAA | 21.13 (the guide's own pace, AL-24; beyond the AA target) |

## 11. Plates and bytes

Allocation 655,000 bytes (D4-63). Units from the engineer's measures (`20261121_Phase-4-Allocations.md`): a web frame with a figure, 21,530 bytes; a rule's words and frames, 6,726; a renderer type's shared style, about 13,000 once (the article's was 12,960). Chapter 15's built plates set the size of a drawing: a loop plate weighs 5,300 to 8,200 bytes and a failure plate 2,345 at the median, measured on disk today. Atlas frames carry tables and drawings where the article carried prose, so I price the Register's frames higher.

| Plate | What it holds | Frames | Estimate, bytes |
|---|---|---|---|
| s-21-home (opener) | Home view | 4 | 88,000 |
| s-21-reform (21.4) | Reform R-23's page | 4 | 88,000 |
| s-21-register (21.8) | Index and sheet D04 | 4 | 104,000 |
| s-21-loop (21.12) | Loop R18's page | 4 | 96,000 |
| `atlas-page` style | Shared once | | 13,000 |
| s-21-1-correct | Masthead, title bar, breadcrumb, locator | 2 | 9,000 |
| s-21-2-correct | Drawing opened to 51 variables | 1 | 12,000 |
| s-21-3-correct | Pressed question and lit parts | 4 | 12,000 |
| s-21-5-correct | Targets and four ink tags | 2 | 7,000 |
| s-21-chips (21.6) | Ten kinds, four pairs, two grounds | 1 | 8,000 |
| s-21-7-correct | Two one-step paths | 1 | 7,000 |
| s-21-9-correct | Sheet D10's ten lines | 1 | 9,000 |
| s-21-10-correct | Rejected option; reviewed and not drawn | 1 | 5,000 |
| s-21-11-correct | Filtered issue list | 2 | 7,000 |
| s-21-13-correct | Stepper, two widths | 2 | 6,000 |
| s-21-14-correct | Loop index, 23 rows | 2 | 14,000 |
| s-21-how-to-read (extra) | Conventions sheet | 2 | 18,000 |
| s-21-15-correct | Dark drawing and ratio table | 1 | 8,000 |
| s-21-16-correct | The test's report | 1 | 6,000 |
| 16 failure plates | One fragment each, with the do-not-publish band | 16 | 80,000 |
| **Plates** | | | **597,000** |
| Rule text, specifications and frames | 16 rules at 6,726 | | 107,616 |
| Chapter head, groups, related chapters, sources | | | 8,000 |
| **Chapter 21** | | | **about 712,600** |

The estimate runs about 57,600 bytes past the allocation, almost all of it in the four view plates' sixteen full-page frames, which I price above the engineer's 21,530 a frame because the Register and loop pages carry tables and drawings, and in the How to read extra. Nothing is cut to meet a figure (DR-271), and the page's 16 MB is the one stop. Two choices would lower it without losing content, and both are the design director's: the view plates may share one `atlas-page` style with chapter 20's `web-page` style where their rules match (contract C4 counts a style once a page), and the How to read extra may drop its dark frame, since every view plate already shows the dark mode. The design director reports each plate's built bytes and the chapter's total against 655,000, and the main session re-sizes the projection in `guide_charts.py` if the built figure holds.

## 12. Related chapters and sources

**Related chapters, draft reasons:** 05 Color (one working red a view, Rule 05.1's screens under DR-310, the marks that keep 3 to 1); 10 Topic and atlas symbols (Rule 10.8, the parts named in words, and the encoding glyphs of Rule 10.10); 12 Graphic devices (the red target, Rule 12.5, and the atlas locator, Rule 12.7); 13 Evidence and sourcing (grade words, line code, delay, chips, dates and source lines); 15 Systems graphics (every mechanism these pages draw); 17 Motion and states (pressed, muted and current looks; the stepper's motion); 18 Components (the chip, stepper, chooser, filters, toggle, disclosure and table); 19 Accessibility (the map these pages add to); 20 Web (the masthead, menu, footer and switch the atlas sits in); 28 Standards checklist (the atlas test's lines). The architecture map names 15, 10, 20 and 28.

**Sources:**
- Our systems atlas, Who Do They Answer To?, Atlas V7, snapshot of October 15, 2026, as extracted to `work/extract/atlas-v7-data.json` (SHA-256 beginning ef1028ac87e402e3), read by the script in Appendix A on November 21, 2026.
- The atlas concepts Field Manual (03), The Circuit (09), Who Can Act (10) and Register (11), October 21, 2026 (`work/boards/phase-1/systems/`), and the atlas editorial systems 1 to 5 of November 5, 2026 (`work/boards/phase-2/atlas-editorial/`), cited as earlier drawings and never as evidence (Rule 15.25).
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", W3C Recommendation, December 12, 2024, as the accessibility lead read and quoted it on November 21, 2026.
- Chapter 18's code sets and chapter 15's generator, read from their files.

## 13. Open items and requests

**For Dustin, at Phase 4 board 1:**
- **ED-F1, the layer color.** The finishing list asks for color by layer, and Rule 15.25's approved resolution says a layer is coded by a frame and a name, never a color (section 6). The studio recommends rerunning the wall test on the built views first and asking only if it fails.

**For the main session:**
- The register's ED-F7 row can close as settled by Rule 10.8 (section 6); ED-F5's "Why it matters" half and DR-37 stay open for the atlas's next version; ED-F1 becomes a board question.
- A new item for the V7.1 issue list: Loop R18's `valence` field reads "Harmful; this is 's B1b with its true polarity.", with a word missing before "'s" [Q17]. Chapter 21's loop page does not print `valence`, so no plate carries it.
- Projection: chapter 21's estimate (section 11) against its 655,000.

**For the engineer, in chapter 21's build chat:** the `atlas-page` renderer and its six templates (9.1); content files that name only IDs (9.2); the figure step that imports chapter 15's drawing code (9.3); the exports (9.5); the atlas test with its self-test (section 8).

**For the editor, in chapter 21's build chat:** every word a reader sees on the plates and in the rules, the page titles (AL-01), the status lines (whose holds are then re-counted, AL-24), and ED-F6's arithmetic line.

**For the design director, in chapter 21's build chat:** the build from this plan, the Charcoal panels where the measure asks for them (section 3.1), each plate's bytes, and my sign-off on every view before the strict build.

**What waits for the atlas's next version:** the walk-through and the atlas's own copy (DR-37); a "Why it matters" field for each variable (ED-F5); the loop and reform lists that disagree, R18's among them (V7.1 item 29); the judging verbs in eighteen titles (V7.1 item 44), which is why the loop page prints its issue records as a count.

## Appendix A. The query script

Saved as `ch21_queries.py` in my scratch folder (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/ac32a0f7-d562-5d93-9aba-0ef59f7ca891/scratchpad/c11/dataviz-lead/`). The scratch folder can be cleared, so the whole script is copied here. Run it from the project folder with `python3 -I ch21_queries.py`, or with query names such as `Q05 Q09`. It reads the model and, for Q14, `tokens.css`, and writes nothing. Its last run: November 21, 2026, 19:20 UTC, on the model whose SHA-256 begins ef1028ac87e402e3.

```python
"""Chapter 21 plan: every model value the plan prints, read from the atlas model by script.

Run from the project folder:  python3 -I ch21_queries.py [Q01 Q05 ...]   (no argument runs every query)
Reads work/extract/atlas-v7-data.json (Atlas V7, snapshot of October 15, 2026) and, for Q14 only,
work/build/tokens/tokens.css. Writes nothing.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

D = json.loads(Path("work/extract/atlas-v7-data.json").read_text())
N, L, LO, RF, IS = D["nodes"], D["links"], D["loops"], D["reforms"], D["issues"]
GRADES = ["documented", "well-supported", "plausible", "plausible_contested", "hypothesis"]


def part(n):            # the home drawing's part: the economy and technology layers, else the core region (cluster)
    x = N[n]
    return {"economy": "EC", "technology": "TC"}.get(x["layer"], x["cluster"])


def sheet(n):           # the Register's sheet: EC and TC for the two lower layers, else the variable's first domain
    x = N[n]
    return {"economy": "EC", "technology": "TC"}.get(x["layer"]) or x["domain"].split("/")[0]


def ln(k):
    x = L[k]
    return (f"{k} {x['from']}->{x['to']} sign={x['polarity'] or 'none'} type={x['type']} delay={x['delay']} "
            f"grade={x['evidence']} contested={x['contested']} | {x['name']}")


def Q01():
    print("snapshot", D["meta"]["snapshot"], "| counts", json.dumps(D["meta"]["counts"]))
    print("variables by type", dict(Counter(x["type"] for x in N.values())), "by layer", dict(Counter(x["layer"] for x in N.values())))
    print("connections by type", dict(Counter(x["type"] for x in L.values())), "| sign", dict(Counter(x["polarity"] or "none" for x in L.values())))
    print("connections by grade", dict(Counter(x["evidence"] for x in L.values())), "| delay", dict(Counter(x["delay"] for x in L.values())))
    print("loops by kind", dict(Counter(x["type"] for x in LO.values())), "| closure", dict(Counter(x["closure"] for x in LO.values())))
    print("issue records", len(IS), "retired", [k for k, v in IS.items() if v.get("retired")])
    print("reforms", len(RF), "rejected", [k for k, v in RF.items() if v.get("rejected")])
    rt = [r for v in RF.values() for r in v["routes"]]
    print("route entries", len(rt), "with a check date", sum(1 for r in rt if r.get("checked")))


def Q02():
    print("variables per part", dict(Counter(part(n) for n in N)))
    print("region titles", {r["id"]: r["title"] for r in D["layers"]["core"]["regions"]}, "| layers", {k: v["title"] for k, v in D["layers"].items()})
    inside, cross = Counter(), Counter()
    for x in L.values():
        a, b = part(x["from"]), part(x["to"])
        (inside.__setitem__(a, inside[a] + 1) if a == b else cross.__setitem__((a, b), cross[(a, b)] + 1))
    print("inside a part", dict(inside), "total", sum(inside.values()))
    print("between parts", {f"{a}->{b}": n for (a, b), n in sorted(cross.items())}, "total", sum(cross.values()))
    core = set("ABCDE")
    print("among core parts", sum(n for (a, b), n in cross.items() if a in core and b in core),
          "| from outside drivers", sum(n for (a, b), n in cross.items() if a == "X"),
          "| to, from or within the lower layers", sum(n for (a, b), n in cross.items() if a != "X" and ({a, b} & {"EC", "TC"})))


def Q03():
    sp = [k for k, x in L.items() if x.get("spine")]
    print("spine connections", len(sp), sp)
    print("main circuit flows", {f"{a}->{b}": sum(1 for x in L.values() if part(x["from"]) == a and part(x["to"]) == b)
                                 for a, b in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")]})


def Q04():
    for h in D["hubs"]:
        print("hub", h["title"], "|", [p["question"] for p in D["pathways"] if p["hub"] == h["id"]])
    pw = next(p for p in D["pathways"] if p["question"].startswith("Why can the same care"))
    r = pw["model_refs"]
    print("pressed question:", pw["question"], "| variables", r["nodes"], "-> parts", sorted({part(n) for n in r["nodes"]}))
    print("  connections", r["links"], "| loops", r["loops"], "| reforms", r["reforms"], "| issues", r["issues"])
    print("  short answer:", pw["short_answer"])
    print("  figures in it:", re.findall(r"\d[\d,.]*%?", pw["short_answer"]), "| claims", len(pw["claim_ids"]), "| sources", len(pw["source_ids"]))
    c = D["claims"]["CL1340"]
    print("  CL1340", {k: c[k] for k in ("claim", "confidence", "population", "jurisdiction", "period", "limitation") if k in c})
    print("  CL1340 sources", c.get("sources"))


def Q05():
    r = RF["R-23"]
    for k in ("title", "band", "targets", "loops", "effects", "effects_confidence", "complements", "sources", "rejected"):
        print(k, "=", json.dumps(r[k], ensure_ascii=False))
    print("problem", r["problem_evidence"]["grade"], "|", r["problem_evidence"]["text"])
    print("remedy", r["remedy_evidence"]["grade"], "|", r["remedy_evidence"]["text"])
    print("status", json.dumps(r["status"], ensure_ascii=False))
    print("routes", [(x["route"], x["who"], x["feasibility"], x["note"], x["checked"]) for x in r["routes"]])
    print("target titles", {t: N[t]["title"] for t in r["targets"]}, "| increase_means", {t: N[t]["increase_means"] for t in r["targets"]})
    print("between the targets:", [ln(k) for k, x in L.items() if {x["from"], x["to"]} == set(r["targets"])])
    print("other reforms with these targets", {t: [k for k, v in RF.items() if t in v["targets"] and k != "R-23"] for t in r["targets"]})
    print("Loop R6's chain", [c[0] for c in LO["R6"]["chain"]], "| issues aiming R-23", [k for k, v in IS.items() if any(a["id"] == "R-23" for a in v.get("aimed_reforms") or [])])
    print("sources", {s: (D["sources"][s]["publisher"], D["sources"][s]["title"], D["sources"][s]["year"]) for s in r["sources"]})
    print("band words", D["leverage"]["bands"]["parameter"])


def Q06():
    num = {k for k, v in LO.items() if not v["closure"].startswith("conceptual")}
    for sh in [d["id"] for d in D["domains"]] + ["EC", "TC"]:
        vs = [n for n in N if sheet(n) == sh]
        ls = [k for k, x in L.items() if sheet(x["to"]) == sh]
        lo = [k for k in num if any(c[0] in vs for c in LO[k]["chain"])]
        rf = [k for k, v in RF.items() if (set(vs) | set(ls)) & set(v["targets"]) and not v.get("rejected")]
        iss = next((len(d["issues"]) for d in D["domains"] if d["id"] == sh), 0)
        g = Counter(L[k]["evidence"] for k in ls)
        print(f"{sh}: variables {len(vs)}, connections {len(ls)}, loops {len(lo)}, reforms {len(rf)}, issues {iss} | " + ", ".join(f"{x} {g[x]}" for x in GRADES))
    print("whole atlas: variables", len(N), "connections", len(L), "numbered loops", len(num), "reforms not rejected",
          sum(1 for v in RF.values() if not v.get("rejected")), "issue records", len(IS))


def Q07():
    d = next(x for x in D["domains"] if x["id"] == "D04")
    print("D04", d["title"], "|", d["everyday_question"])
    for n in [n for n in N if sheet(n) == "D04"]:
        print("  variable", n, N[n]["type"], "|", N[n]["title"], "|", N[n]["increase_means"])
    for k in [k for k, x in L.items() if sheet(x["to"]) == "D04"]:
        print("  ", ln(k), "| citation:", L[k]["citation"])
    iss = d["issues"]
    print("  issue records", len(iss), dict(Counter(IS[i]["grade"] for i in iss)))
    print("  naming each variable", {v: sum(1 for i in iss if v in (IS[i]["nodes"] or [])) for v in ("D1", "D4", "D5")},
          "| naming none", sum(1 for i in iss if not {"D1", "D4", "D5"} & set(IS[i]["nodes"] or [])))
    print("  naming D4:", [(i, IS[i]["grade"], IS[i]["title"]) for i in iss if "D4" in (IS[i]["nodes"] or [])])


def Q08():
    r = RF["R-35"]
    print("R-35", r["title"], "| targets", r["targets"], "-> sheets", sorted({sheet(L[t]["to"]) for t in r["targets"]}),
          "| loops", r["loops"], "| effects", r["effects"], "| problem", r["problem_evidence"]["grade"], "| remedy", r["remedy_evidence"]["grade"])
    print("  remedy words:", r["remedy_evidence"]["text"][:260])
    for x in D["rejectedLinks"]:
        print(x["id"], x["status"], "|", x["from"], "->", x["to"], "| sheet", sheet(x["to"].split(":")[0]), "| sources", len(x["sources"]))
    print("omissions", len(D["omissions"]))


def Q09():
    lp = LO["R18"]
    for k in ("title", "type", "closure", "evidence", "delay", "direction", "chain", "links", "reforms", "records"):
        print(k, "=", json.dumps(lp.get(k), ensure_ascii=False))
    for k in ("summary", "how_to_read", "evidence_summary", "qualification", "case", "adaptation"):
        print(k, "=", lp[k])
    for k in lp["links"]:
        print("  ", ln(k), "| plain:", L[k]["plain"])
    print("minus signs", sum(1 for k in lp["links"] if L[k]["polarity"] == "-"), "| variables", {c[0]: (N[c[0]]["title"], part(c[0]), sheet(c[0])) for c in lp["chain"]})
    print("connection sheets", {k: sheet(L[k]["to"]) for k in lp["links"]})
    named = [k for k, v in RF.items() if "R18" in v["loops"]]
    print("reforms whose records name R18", named, "| the loop's own list", lp["reforms"])
    for k in named:
        v = RF[k]
        print("  ", k, v["title"], "| band", v["band"], "| targets", v["targets"], "| effects", v["effects"],
              "| problem", v["problem_evidence"]["grade"], "| remedy", v["remedy_evidence"]["grade"], "| routes", [(x["route"], x["feasibility"], x["checked"]) for x in v["routes"]])
    print("records", [(i, IS[i]["grade"], IS[i]["domain"], IS[i]["title"]) for i in lp["records"]])


def Q10():
    say = {"D2": "presidential action without new legislation", "D4": "the ability to investigate and enforce the rules"}
    lp = LO["R18"]
    for i, k in enumerate(lp["links"]):
        x = L[k]
        weak = x["evidence"] in ("plausible", "plausible_contested", "hypothesis")
        verb = ("can " if weak else "") + {("+", 0): "raises", ("-", 0): "lowers", ("+", 1): "raise", ("-", 1): "lower"}[(x["polarity"], int(weak))]
        a, b = say[x["from"]], say[x["to"]]
        line = f"{a[0].upper() + a[1:]} {verb} {b}" + (", where the loop began." if i == len(lp["links"]) - 1 else ".")
        more = x["plain"] + (" Our atlas grades this step plausible, the least certain in the loop." if x["evidence"] == "plausible" else "")
        s = f"Step {i + 1} of {len(lp['links'])}: {line} {more}"
        print(k, len(s.split()), "words ->", max(6000, 250 * len(s.split())), "ms |", s)


def Q11():
    for k, v in LO.items():
        m = sum(1 for x in v["links"] if L[x]["polarity"] == "-")
        print(f"{k} {v['type']} steps={len(v['links'])} minus={m} delay={v['delay']} closure={v['closure']} | grade={v['evidence']} | {v['title']}")


def Q12():
    print("Variable B4", N["B4"]["title"], "| Loop B4", LO["B4"]["title"])
    print("Loop R1", LO["R1"]["title"], "| Reform R-01", RF["R-01"]["title"])
    print("Variable D4", N["D4"]["title"], "| Domain D04", next(d["title"] for d in D["domains"] if d["id"] == "D04"))
    print("Variable X1", N["X1"]["title"], "| Issue X01", IS["X01"]["title"])
    print("Connection L14", L["L14"]["name"], "| Issue I164", IS["I164"]["title"], "| Claim CL1340", D["claims"]["CL1340"]["claim"][:60])
    print("Route SS", next(r["name"] for r in D["routes"]["items"] if r["code"] == "SS"))
    rl = next(r for r in D["repairLog"]["rows"] if r["id"] == "RL19")
    dl = next(r for r in D["deliveryLog"]["rows"] if r["id"] == "DL05")
    print("Rule change RL19", rl["date"], rl["jurisdiction"], "|", rl["rule"][:90])
    print("Delivery case DL05", dl["date"], dl["jurisdiction"], "|", dl["what_was_done"][:90])


def Q13():
    print("families", {k: v["name"] for k, v in D["outcomes"]["families"].items()})
    print("effect codes", D["outcomes"]["effect_codes"])
    print("route names", {r["code"]: r["name"] for r in D["routes"]["items"]})
    print("bands", list(D["leverage"]["bands"]))


def Q14():
    css = Path("work/build/tokens/tokens.css").read_text()
    hx = lambda t: re.search(r"--" + t + r":\s*(#[0-9A-Fa-f]{6})", css).group(1)

    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    ratio = lambda a, b: (max(lum(a), lum(b)) + 0.05) / (min(lum(a), lum(b)) + 0.05)
    for g in ("oa-color-palette-newsprint", "oa-color-palette-charcoal"):
        for m in ("oa-color-palette-charcoal", "oa-color-palette-newsprint", "oa-color-derived-dim-newsprint", "oa-color-palette-stone",
                  "oa-color-derived-deep-stone", "oa-color-palette-pillar-red", "oa-color-palette-prussian", "oa-color-tint-prussian-n62",
                  "oa-color-palette-verdigris", "oa-color-palette-white"):
            print(f"{m} {hx(m)} on {g} {hx(g)}: {ratio(hx(m), hx(g)):.2f}")

def Q15():
    d = next(x for x in D["domains"] if x["id"] == "D10")
    print("D10", d["title"], "|", d["everyday_question"])
    for k in [k for k, x in L.items() if sheet(x["to"]) == "D10"]:
        print("  ", ln(k), "| citation:", L[k]["citation"])
    for x in D["rejectedLinks"]:
        if sheet(x["to"].split(":")[0]) == "D10":
            print("  reviewed and not drawn:", x["id"], "|", x["from"], "->", x["to"], "| reason:", x["reason"][:200])


def Q16():
    r = RF["R-35"]
    print("R-35 routes", [(x["route"], x["who"], x["feasibility"], x["note"], x["checked"]) for x in r["routes"]])
    print("R-35 effects_confidence", r["effects_confidence"], "| status", json.dumps(r["status"], ensure_ascii=False))

def Q17():
    keys = sorted({k for n in N.values() for k in n})
    print("variable fields", keys, "| a why-it-matters field:", [k for k in keys if "why" in k.lower() or "matter" in k.lower()] or "none")
    print("Loop R18 valence =", repr(LO["R18"].get("valence")))



if __name__ == "__main__":
    for q in (sys.argv[1:] or [f"Q{i:02d}" for i in range(1, 18)]):
        print(f"===== {q}")
        globals()[q]()
```

## Appendix B. What each query returned

The full output of that run, as printed. Long text fields print whole where the plan quotes them.

```text
===== Q01
snapshot 2026-10-15 | counts {"variables": 51, "connections": 118, "loops": 23, "loops_numbered": 20, "issues": 194, "issues_active": 193, "reforms": 50, "sources": 1099, "sources_total_ids": 1140, "pathways": 16, "hubs": 5, "claims": 433, "core_links": 72, "economy_links": 27, "technology_links": 19, "core_variables": 31}
variables by type {'stock': 31, 'flow': 9, 'auxiliary': 6, 'driver': 5} by layer {'core': 31, 'economy': 12, 'technology': 8}
connections by type {'money': 17, 'causal': 80, 'information': 9, 'ownership': 5, 'authority': 7} | sign {'+': 70, '-': 41, 'none': 7}
connections by grade {'well-supported': 37, 'plausible': 35, 'documented': 32, 'plausible_contested': 7, 'hypothesis': 7} | delay {'S': 38, 'M': 45, 'L': 35}
loops by kind {'R': 18, 'B': 5} | closure {'closed: every step is a numbered connection': 18, 'closed with a hypothesized step': 2, 'conceptual: no complete numbered chain': 3}
issue records 194 retired ['I128']
reforms 50 rejected ['R-35']
route entries 126 with a check date 13
===== Q02
variables per part {'A': 6, 'B': 6, 'C': 5, 'D': 7, 'E': 2, 'X': 5, 'EC': 12, 'TC': 8}
region titles {'A': 'Economic structure', 'B': 'Political inputs', 'C': 'Electoral competition', 'D': 'Governing institutions', 'E': 'Legitimacy', 'X': 'Outside drivers'} | layers {'core': 'Power and accountability', 'economy': 'How the economy reaches a household', 'technology': 'Technology and its effects'}
inside a part {'C': 5, 'D': 7, 'B': 5, 'A': 6, 'EC': 11, 'TC': 3} total 37
between parts {'A->B': 5, 'A->EC': 4, 'B->C': 4, 'B->D': 2, 'B->E': 3, 'C->B': 3, 'C->D': 4, 'D->B': 2, 'D->C': 3, 'D->E': 4, 'D->EC': 3, 'D->TC': 4, 'E->A': 3, 'E->D': 5, 'E->EC': 1, 'EC->A': 7, 'TC->A': 1, 'TC->B': 2, 'TC->D': 1, 'TC->EC': 5, 'X->A': 5, 'X->B': 4, 'X->C': 1, 'X->D': 1, 'X->E': 1, 'X->EC': 1, 'X->TC': 2} total 81
among core parts 38 | from outside drivers 15 | to, from or within the lower layers 28
===== Q03
spine connections 19 ['L01', 'L02', 'L03', 'L08', 'L10', 'L11', 'L12', 'L14', 'L15', 'L20', 'L21', 'L23', 'L24', 'L25', 'L26', 'L28', 'L42', 'L53', 'L54']
main circuit flows {'A->B': 5, 'B->C': 4, 'C->D': 4, 'D->E': 4, 'E->A': 3}
===== Q04
hub Cost of living | ['Why did my rent go up?', 'Why is my grocery bill higher?', 'Why is my electric bill going up?', 'Why did my home insurance premium go up?']
hub Health and care | ['Why is it hard to find an appointment?', 'Why can the same care produce different bills?', "Why does childcare cost so much, and why can't I find an opening?", 'Why is it so hard to get help at home as I age or live with a disability?']
hub Work and financial security | ["Why isn't my pay keeping up with what my work produces?", 'How do taxes and benefit rules change what my household keeps?', 'What will I get from Social Security, and could the rules change before I retire?']
hub Public services where you live | ['Who makes sure my tap water is safe?', 'Why is the repair on my street taking so long?', "Why does my child's school have less than schools in other districts?"]
hub Voice, power and information | ['Which election decides who represents me, and how can I influence the people who decide?', 'How do algorithms affect the prices I pay, my job, what I see online and the services I get?']
pressed question: Why can the same care produce different bills? | variables ['A3', 'EC9', 'EC8', 'A4', 'D4'] -> parts ['A', 'D', 'EC']
  connections ['LE16', 'LE26', 'LE27'] | loops ['B3'] | reforms ['R-19', 'R-20'] | issues ['I134', 'I085', 'I084', 'I092', 'I123']
  short answer: Most of a medical bill's price comes from a private contract. Each insurer or employer plan negotiates its own rates with each hospital and clinician, so a scan can cost widely different amounts within one city. Hospitals with few nearby rivals win higher rates, and Medicare pays more for some services in hospital outpatient departments than in doctors' offices. RAND, a nonprofit research organization, found private plans paid hospitals 254% of Medicare rates in 2022. For medicines, the manufacturer sets a list price protected by patents, and pharmacy benefit managers negotiate rebates off that price, so a patient's coinsurance can still be based on the full list price.
  figures in it: ['254%', '2022.'] | claims 28 | sources 29
  CL1340 {'claim': 'In 2022, employers and private insurers paid hospitals 254% of what Medicare would have paid for the same services, with wide differences by state.', 'confidence': 'well-supported', 'population': 'Privately insured patients in participating employer and insurer data', 'jurisdiction': 'United States, by state', 'period': '2020 to 2022', 'limitation': 'Claims come from participating employers and insurers, not a random sample of all private plans.'}
  CL1340 sources ['Q212']
===== Q05
title = "Minimum wage that rises with an index"
band = "parameter"
targets = ["EC7", "A4"]
loops = ["R6"]
effects = {"DQ": "0", "GE": "0", "EP": "0 to -S at high bite", "EQ": "+M lower tail"}
effects_confidence = "high to 60% of median; low above"
complements = ["R-25"]
sources = ["Q255", "Q257", "Q256"]
rejected = false
problem documented | The federal minimum wage has been $7.25 an hour since July 2009, according to the Department of Labor.
remedy contested | Within studied ranges, evidence finds little job loss. Cengiz, Dube, Lindner and Zipperer (2019), studying state increases through 2016, found no detectable job loss, a result other methods dispute. The evidence is strongest up to about 60% of the local median wage. Main limitation: higher floors fall outside the studied range; the Congressional Budget Office's 2019 median estimate for a $15 federal floor by 2025 was 1.3 million jobs lost and 1.3 million people lifted from poverty, with wide uncertainty.
status {"text": "As of the Labor Department's state table updated July 1, 2026, 30 states and the District of Columbia set a minimum wage above the federal $7.25 an hour.", "checked": "2026-10-15", "result": "confirmed", "sources": ["Q255", "K1508"]}
routes [('SS', 'Legislatures', 'high', None, None), ('BI', 'Voters', 'high', None, None), ('LOC', 'Cities', 'medium', 'Where not preempted.', None), ('FS', 'Congress', 'low', None, None)]
target titles {'EC7': 'Household income', 'A4': "Households' financial security"} | increase_means {'EC7': 'A higher value means households receive more money over the year.', 'A4': 'A higher value means more households can cover their needs and a surprise bill.'}
between the targets: ['LE15 EC7->A4 sign=+ type=causal delay=S grade=documented contested=False | Higher income strengthens household security']
other reforms with these targets {'EC7': [], 'A4': ['R-24', 'R-25', 'R-26', 'R-31']}
Loop R6's chain ['A2', 'A1', 'B1', 'E1'] | issues aiming R-23 ['I104', 'X08']
sources {'Q255': ('U.S. Department of Labor, Wage and Hour Division', 'History of Federal Minimum Wage Rates Under the FLSA', 'current'), 'Q257': ('Quarterly Journal of Economics', 'The Effect of Minimum Wages on Low-Wage Jobs (Cengiz, Dube, Lindner, Zipperer)', '2019'), 'Q256': ('Congressional Budget Office', 'The Effects on Employment and Family Income of Increasing the Federal Minimum Wage', '2019')}
band words Changes a number: a rate, a subsidy, a tax, a budget, or the size of a stock such as staff (Meadows levels 12 to 10).
===== Q06
D01: variables 3, connections 9, loops 2, reforms 3, issues 17 | documented 1, well-supported 3, plausible 3, plausible_contested 0, hypothesis 2
D02: variables 8, connections 19, loops 10, reforms 14, issues 22 | documented 5, well-supported 9, plausible 5, plausible_contested 0, hypothesis 0
D03: variables 2, connections 7, loops 8, reforms 7, issues 17 | documented 1, well-supported 2, plausible 3, plausible_contested 0, hypothesis 1
D04: variables 3, connections 10, loops 6, reforms 10, issues 20 | documented 2, well-supported 2, plausible 5, plausible_contested 0, hypothesis 1
D05: variables 3, connections 7, loops 5, reforms 7, issues 26 | documented 2, well-supported 2, plausible 3, plausible_contested 0, hypothesis 0
D06: variables 2, connections 1, loops 0, reforms 2, issues 17 | documented 0, well-supported 0, plausible 1, plausible_contested 0, hypothesis 0
D07: variables 1, connections 4, loops 2, reforms 4, issues 20 | documented 0, well-supported 2, plausible 1, plausible_contested 1, hypothesis 0
D08: variables 3, connections 13, loops 3, reforms 6, issues 19 | documented 5, well-supported 7, plausible 1, plausible_contested 0, hypothesis 0
D09: variables 2, connections 4, loops 1, reforms 3, issues 19 | documented 0, well-supported 2, plausible 2, plausible_contested 0, hypothesis 0
D10: variables 4, connections 10, loops 4, reforms 6, issues 17 | documented 0, well-supported 3, plausible 5, plausible_contested 2, hypothesis 0
EC: variables 12, connections 25, loops 0, reforms 19, issues 0 | documented 11, well-supported 4, plausible 5, plausible_contested 4, hypothesis 1
TC: variables 8, connections 9, loops 0, reforms 5, issues 0 | documented 5, well-supported 1, plausible 1, plausible_contested 0, hypothesis 2
whole atlas: variables 51 connections 118 numbered loops 20 reforms not rejected 49 issue records 194
===== Q07
D04 Congress, agencies and public services | Why does it take so long to get a benefit, a permit or a new law?
  variable D1 stock | Congress's ability to write and check policy | A higher value means Congress has more staff and expertise to draft laws and oversee agencies.
  variable D4 stock | Ability to investigate and enforce the rules | A higher value means watchdogs can get records, investigate and make findings stick.
  variable D5 stock | Quality of public services | A higher value means services are delivered faster and with fewer errors.
   L10 B4->D1 sign=- type=causal delay=M grade=well-supported contested=False | Partisan hostility weakens Congress's capacity | citation: Binder 2003, Stalemate; Lee 2016, Insecure Majorities
   L12 D2->D1 sign=- type=causal delay=L grade=plausible contested=False | Presidential action erodes Congress's will to legislate | citation: Chafetz 2017, Congress's Constitution
   L14 D2->D4 sign=- type=causal delay=S grade=documented contested=False | Presidential removals weaken watchdog agencies | citation: 17 IGs removed Jan 24, 2025; ruled unlawful Sept 24, 2025; FEC without quorum since May 1, 2025
   L17 E1->D4 sign=+ type=causal delay=M grade=plausible contested=False | Visible favoritism can prompt investigations | citation: HB6 investigation (DOJ 2023); GAO mandate structure
   L19 E1->D1 sign=- type=causal delay=L grade=hypothesis contested=False | Insider-tilted policy may weaken congressional expertise | citation: 1995 staff cuts and OTA abolition (event)
   L21 E2->D5 sign=+ type=causal delay=L grade=plausible contested=False | Earned trust supports compliance and service funding | citation: Luttmer and Singhal 2014, JEP (tax morale); Bargain and Aminjonov 2020 (COVID compliance)
   L22 E1->D5 sign=- type=money delay=M grade=documented contested=False | Insider-tilted policy cuts public service capacity | citation: TIGTA and OPM staffing data (official)
   T03 D4->D5 sign=+ type=causal delay=M grade=plausible contested=False | Oversight corrects failing public services | citation: GAO recommendations implemented
   L54 C5->D5 sign=+ type=causal delay=M grade=well-supported contested=False | Removing incumbents improves performance of those remaining | citation: Ferraz and Finan 2011 (audits and reelection incentives); Besley 2006
   LT15 TC5->D5 sign=+ type=causal delay=M grade=plausible contested=False | In-house digital teams improve service delivery | citation: GAO on HealthCare.gov (W117); GAO on UI improper payments (W118); Direct File volumes (W120)
  issue records 20 {'well_supported': 6, 'plausible': 3, 'documented': 11}
  naming each variable {'D1': 8, 'D4': 9, 'D5': 11} | naming none 2
  naming D4: [('I053', 'plausible', 'Deadline bills bundle unrelated choices with little scrutiny'), ('I055', 'documented', 'Debt-limit standoffs create a risk of default'), ('I056', 'documented', "Congress's demands for information can expire unanswered"), ('I057', 'documented', 'Programs continue without evidence of results'), ('I061', 'plausible', 'Contracting rules can reward paperwork over results'), ('I064', 'documented', 'Permitting reviews lack a predictable path to a decision'), ('I164', 'documented', 'Empty seats and acting officials can stop agencies from acting'), ('X04', 'documented', 'Removing job protections shifts agencies from career to political control'), ('X14', 'documented', 'Court rulings and White House orders move agency decisions to the President and the courts')]
===== Q08
R-35 Rejected option: term limits for legislators | targets ['L18', 'L19'] -> sheets ['D03', 'D04'] | loops ['R2'] | effects {'DQ': '-S', 'GE': '-M', 'EP': '0', 'EQ': '0'} | problem documented | remedy well-supported
  remedy words: Here the grade measures confidence in a finding of harm: strong evidence that term limits weaken legislatures. That finding is the reason the option is rejected, and a strong grade on this page is a warning against adoption. Olson and Rogowski (2020), using st
LTR1 reviewed and not drawn | TC1: How platforms rank feeds and seek attention -> B4: Hostility toward the other political party | sheet D10 | sources 7
LTR2 reviewed and not drawn | X4: Foreign interference -> B4: Hostility toward the other political party | sheet D10 | sources 1
LTR3 reviewed and not drawn | EC10: Costs of tariffs and trade rules -> A2: Workers' bargaining power | sheet D07 | sources 0
omissions 9
===== Q09
title = "Weakening watchdogs lowers the cost of further unilateral action"
type = "R"
closure = "closed: every step is a numbered connection"
evidence = "documented for D2 to D4; plausible for D4 to D2"
delay = "M"
direction = "running_up"
chain = [["D2", "-"], ["D4", "-"]]
links = ["L14", "L15"]
reforms = ["R-11", "R-15"]
records = ["I056", "I070", "I161", "I163", "I164", "X04", "X06", "X14"]
summary = A president can remove inspectors general, leave commissions without a quorum or cut investigative staff. With fewer independent watchdogs, the next action taken without Congress meets less resistance. Each removal makes the next one cheaper.
how_to_read = Presidential action without new legislation lowers the ability to investigate and enforce the rules, and weaker enforcement raises presidential action without new legislation; two negative steps make the loop reinforcing.
evidence_summary = L14: Presidential removals weaken watchdog agencies is documented by the January 2025 removals and the Federal Election Commission's loss of a quorum on May 1, 2025. The return step, L15: Independent watchdogs restrain unilateral action, is plausible and the weaker: GAO found several 2025 impoundments unlawful, and restraint depends on courts and Congress acting on such findings.
qualification = Watchdogs restrain action only when they answer to the law and their findings can be enforced, so the loop's strength depends on remedies such as subpoena enforcement and standing to sue.
case = Seventeen inspectors general were removed by email on January 24, 2025, without the 30 days' notice the law requires. On September 24, 2025, a federal court said the removals 'almost undoubtedly' violated the law and reinstated no one, because the President could remove them again with proper notice; no ruling on the merits had been issued as of October 15, 2026. The case documents the first step and does not show that later actions met less resistance.
adaptation = The 2021 removals of NLRB general counsel Peter Robb and SSA commissioner Andrew Saul, both later upheld under Collins v. Yellen, are the other party's instances; each administration widens the channel the last one opened.
   L14 D2->D4 sign=- type=causal delay=S grade=documented contested=False | Presidential removals weaken watchdog agencies | plain: Firing inspectors general and commissioners, leaving boards without a quorum and cutting staff all reduce what watchdogs can investigate and enforce.
   L15 D4->D2 sign=- type=causal delay=M grade=plausible contested=False | Independent watchdogs restrain unilateral action | plain: Audits, lawsuits and enforcement raise the cost of acting without a law, provided the enforcer does not answer to the official being checked.
minus signs 2 | variables {'D2': ('Presidential action without new legislation', 'D', 'D05'), 'D4': ('Ability to investigate and enforce the rules', 'D', 'D04')}
connection sheets {'L14': 'D04', 'L15': 'D05'}
reforms whose records name R18 ['R-11', 'R-15', 'R-48'] | the loop's own list ['R-11', 'R-15']
   R-11 A Federal Election Commission able to act | band feedback | targets ['D4', 'L14', 'L15'] | effects {'DQ': '+M precondition', 'GE': '+S', 'EP': '0', 'EQ': '0'} | problem documented | remedy plausible | routes [('FR', 'medium', None), ('FS', 'low', None)]
   R-15 Inspectors general with remedies that work | band feedback | targets ['L14', 'L15', 'L16'] | effects {'DQ': '+M', 'GE': '+M', 'EP': '+S', 'EQ': '0'} | problem documented | remedy plausible | routes [('FS', 'low', None), ('CRT', 'low', None)]
   R-48 Agency independence after the Slaughter ruling | band rules | targets ['L14', 'L15'] | effects {'DQ': '+M', 'GE': '+S', 'EP': '0', 'EQ': '0'} | problem documented | remedy hypothesis | routes [('FS', 'low', None), ('CRT', 'low', None)]
records [('I056', 'documented', 'D04', "Congress's demands for information can expire unanswered"), ('I070', 'documented', 'D05', 'Firing and emptying watchdog offices weakens oversight'), ('I161', 'documented', 'D05', 'Presidential direction of prosecutions threatens equal enforcement'), ('I163', 'documented', 'D05', 'At-will removal of regulators narrows agency independence'), ('I164', 'documented', 'D04', 'Empty seats and acting officials can stop agencies from acting'), ('X04', 'documented', 'D04', 'Removing job protections shifts agencies from career to political control'), ('X06', 'documented', 'D05', 'An attempted removal tests Federal Reserve independence'), ('X14', 'documented', 'D04', 'Court rulings and White House orders move agency decisions to the President and the courts')]
===== Q10
L14 39 words -> 9750 ms | Step 1 of 2: Presidential action without new legislation lowers the ability to investigate and enforce the rules. Firing inspectors general and commissioners, leaving boards without a quorum and cutting staff all reduce what watchdogs can investigate and enforce.
L15 58 words -> 14500 ms | Step 2 of 2: The ability to investigate and enforce the rules can lower presidential action without new legislation, where the loop began. Audits, lawsuits and enforcement raise the cost of acting without a law, provided the enforcer does not answer to the official being checked. Our atlas grades this step plausible, the least certain in the loop.
===== Q11
R1 R steps=3 minus=0 delay=L closure=closed: every step is a numbered connection | grade=plausible | Wealth and political influence reinforce each other
R1b R steps=2 minus=0 delay=L closure=closed: every step is a numbered connection | grade=plausible | Political spending and court rulings reinforce each other
R2 R steps=2 minus=2 delay=L closure=closed with a hypothesized step | grade=hypothesis | Congress becomes dependent on outside expertise
R3 R steps=2 minus=0 delay=S closure=closed: every step is a numbered connection | grade=plausible_contested | Political hostility and hostile content may reinforce each other
R4a R steps=3 minus=0 delay=M closure=closed: every step is a numbered connection | grade=documented for C4 to C1 and D7 to C4; plausible for C1 to D7 | Majorities draw maps that help them keep control
R4b R steps=2 minus=2 delay=M closure=closed: every step is a numbered connection | grade=plausible | Voting rules shape who can hold rule-makers accountable
R5 R steps=3 minus=2 delay=L closure=closed: every step is a numbered connection | grade=plausible | Financial strain narrows who takes part in policy decisions
R6 R steps=4 minus=2 delay=L closure=closed: every step is a numbered connection | grade=well-supported for A2 to A1; plausible for the rest | Weak bargaining power and concentrated wealth reinforce each other
R7 R steps=2 minus=0 delay=L closure=closed: every step is a numbered connection | grade=hypothesis for the named direction; plausible for the compliance channel; the delivery leg is documented case by case in the Delivery Log, though no study measures the loop closing | Service performance and earned trust can reinforce each other
R8 R steps=2 minus=0 delay=L closure=closed: every step is a numbered connection | grade=well-supported for both links; the loop no longer depends on A1 | Housing scarcity strengthens owners' incentive to restrict building
R10 R steps=4 minus=2 delay=M closure=closed: every step is a numbered connection | grade=documented for C1 to C2; well-supported for C2 to C3; plausible for C3 to C4 (the weakest link) | Safe seats shift accountability to small primary electorates
R11 R steps=3 minus=2 delay=M closure=closed: every step is a numbered connection | grade=well-supported for B4 to C3; plausible for the rest | Party loyalty weakens consequences for breaking norms
R12 R steps=4 minus=0 delay=L closure=closed: every step is a numbered connection | grade=documented for D3 to C4; plausible for C1 to D7 and D7 to D3 | Entrenched majorities shape courts that rule on election rules
R13 R steps=2 minus=2 delay=L closure=closed: every step is a numbered connection | grade=well-supported for D1 to D2; plausible for D2 to D1 | Congressional weakness creates room for presidential action
R15 R steps=4 minus=2 delay=L closure=closed: every step is a numbered connection | grade=plausible | Unions, civic ties and equal turnout reinforce each other
R16 R steps=2 minus=0 delay=L closure=closed with a hypothesized step | grade=well-supported for the step from local reporting to the risk of losing office; hypothesis for the closing step | Local news loss and weak electoral pressure may reinforce each other
R18 R steps=2 minus=2 delay=M closure=closed: every step is a numbered connection | grade=documented for D2 to D4; plausible for D4 to D2 | Weakening watchdogs lowers the cost of further unilateral action
B1a B steps=2 minus=1 delay=M closure=closed: every step is a numbered connection | grade=plausible for E1 to D4; well-supported for D4 to E1 | Independent oversight can limit policy favoritism
B4 B steps=3 minus=1 delay=M closure=closed: every step is a numbered connection | grade=well-supported where seats are competitive; C5 to D5 well-supported | Electoral consequences can improve public performance
B5 B steps=2 minus=1 delay=L closure=closed: every step is a numbered connection | grade=plausible | State and local experiments can correct policy favoritism
B2 B steps=0 minus=0 delay=S closure=conceptual: no complete numbered chain | grade=well-supported | Automatic benefits cushion economic shocks
B3 B steps=0 minus=0 delay=M closure=conceptual: no complete numbered chain | grade=well-supported where entry is possible | New competitors can limit market power
R9 R steps=0 minus=0 delay=M closure=conceptual: no complete numbered chain | grade=hypothesis | Taking part in a successful repair may support the next one
===== Q12
Variable B4 Hostility toward the other political party | Loop B4 Electoral consequences can improve public performance
Loop R1 Wealth and political influence reinforce each other | Reform R-01 All-party primaries with ranked general elections
Variable D4 Ability to investigate and enforce the rules | Domain D04 Congress, agencies and public services
Variable X1 What new technology can do | Issue X01 In safe seats, a small primary electorate picks the winner
Connection L14 Presidential removals weaken watchdog agencies | Issue I164 Empty seats and acting officials can stop agencies from acting | Claim CL1340 In 2022, employers and private insurers paid hospitals 254% 
Route SS State statute
Rule change RL19 2022-12-29 United States | The Electoral Count Reform Act made the Vice President's role ministerial and raised the t
Delivery case DL05 1965-07-30 to 1966-07-01 federal | Congress enrolled every American over 65 in a single hospital insurance program and stood 
===== Q13
families {'DQ': 'Democratic quality', 'GE': 'Government efficacy', 'EP': 'Economic performance', 'EQ': 'Income and wealth equality'}
effect codes {'+L': 'large positive', '+M': 'moderate positive', '+S': 'small positive', '0': 'no expected effect', '-S': 'small negative', '-M': 'moderate negative', '?': 'direction uncertain'}
route names {'LOC': 'Local', 'SS': 'State statute', 'BI': 'State ballot', 'FS': 'Federal statute', 'FR': 'Chamber rule or confirmation', 'FA': 'Federal executive action', 'ENF': 'Enforcement and litigation', 'CRT': 'Court doctrine', 'AV': 'Article V', 'IC': 'Interstate compact', 'CIV': 'Civil society'}
bands ['parameter', 'feedback', 'information', 'rules', 'power to change the rules', 'goals']
===== Q14
oa-color-palette-charcoal #121212 on oa-color-palette-newsprint #DCD9D2: 13.29
oa-color-palette-newsprint #DCD9D2 on oa-color-palette-newsprint #DCD9D2: 1.00
oa-color-derived-dim-newsprint #A3A19C on oa-color-palette-newsprint #DCD9D2: 1.83
oa-color-palette-stone #5D636D on oa-color-palette-newsprint #DCD9D2: 4.29
oa-color-derived-deep-stone #4E535B on oa-color-palette-newsprint #DCD9D2: 5.49
oa-color-palette-pillar-red #E63946 on oa-color-palette-newsprint #DCD9D2: 2.96
oa-color-palette-prussian #1F2D5A on oa-color-palette-newsprint #DCD9D2: 9.42
oa-color-tint-prussian-n62 #8E94A4 on oa-color-palette-newsprint #DCD9D2: 2.15
oa-color-palette-verdigris #4A7C74 on oa-color-palette-newsprint #DCD9D2: 3.37
oa-color-palette-white #FFFFFF on oa-color-palette-newsprint #DCD9D2: 1.41
oa-color-palette-charcoal #121212 on oa-color-palette-charcoal #121212: 1.00
oa-color-palette-newsprint #DCD9D2 on oa-color-palette-charcoal #121212: 13.29
oa-color-derived-dim-newsprint #A3A19C on oa-color-palette-charcoal #121212: 7.26
oa-color-palette-stone #5D636D on oa-color-palette-charcoal #121212: 3.10
oa-color-derived-deep-stone #4E535B on oa-color-palette-charcoal #121212: 2.42
oa-color-palette-pillar-red #E63946 on oa-color-palette-charcoal #121212: 4.49
oa-color-palette-prussian #1F2D5A on oa-color-palette-charcoal #121212: 1.41
oa-color-tint-prussian-n62 #8E94A4 on oa-color-palette-charcoal #121212: 6.18
oa-color-palette-verdigris #4A7C74 on oa-color-palette-charcoal #121212: 3.95
oa-color-palette-white #FFFFFF on oa-color-palette-charcoal #121212: 18.73
===== Q15
D10 Taking part, trust and shared norms | Why does showing up feel pointless, and why do people across the party divide distrust each other so much?
   L09 C2->B4 sign=+ type=causal delay=L grade=plausible_contested contested=True | Decisive primaries may deepen partisan hostility | citation: McGhee, Masket, Shor, Rogers and McCarty 2014, AJPS; Hirano et al. 2010; Reilly, Wright and Lublin 2025 (Alaska, one cycle, moderation)
   L20 D5->E2 sign=+ type=causal delay=L grade=plausible contested=False | Better public services build earned trust | citation: Hetherington 2005, Why Trust Matters
   L27 B2->B4 sign=- type=information delay=M grade=well-supported contested=False | Local reporting can temper partisan hostility | citation: Darr, Hitt and Dunaway 2018, Journal of Communication
   L32 A2->B3 sign=+ type=causal delay=L grade=plausible contested=False | Strong unions build cross-group civic ties | citation: Ahlquist 2017, Annual Review of Political Science
   L33 B3->B4 sign=- type=causal delay=L grade=plausible contested=False | Cross-group ties reduce partisan hostility | citation: Mason 2018; Pettigrew and Tropp 2006 (contact, general)
   L41 B4->E2 sign=- type=causal delay=M grade=well-supported contested=False | Partisan hostility lowers trust in government | citation: Hetherington and Rudolph 2015, Why Washington Won't Work
   L47 B6->B4 sign=+ type=information delay=S grade=plausible_contested contested=True | Hostile content may raise partisan hostility slightly | citation: Guess et al. 2023 (W090); Nyhan et al. 2023 (W091); Allcott et al. 2024 (W093); Gauthier et al. 2026 (W095); Piccardi et al. 2025 (W096); Allcott et al. 2020 (W094); Budak et al. 2024 on concentrated exposure (W098)
   L52 D2->B4 sign=+ type=causal delay=M grade=plausible contested=False | Unilateral action deepens partisan hostility | citation: Mason 2018 (mechanism); no direct test
   T08 X3->B4 sign=+ type=causal delay=L grade=well-supported contested=False | Trade shocks deepen partisan polarization | citation: Autor, Dorn, Hanson and Majlesi 2020, AER
   T10 X4->E2 sign=- type=causal delay=S grade=plausible contested=False | Foreign interference can lower trust in elections | citation: Eady et al. 2023 (discussion)
  reviewed and not drawn: LTR1 | TC1: How platforms rank feeds and seek attention -> B4: Hostility toward the other political party | reason: Feed ranking changes what people see (LT01). In the largest experiments, changing the feed did not measurably change hostility toward the other party: Facebook and Instagram feed changes in 2020, plat
  reviewed and not drawn: LTR2 | X4: Foreign interference -> B4: Hostility toward the other political party | reason: Measured exposure to the 2016 Russian influence campaign on Twitter was concentrated in about 1% of users and showed no meaningful relationship with attitudes or votes. Foreign operations stay in the 
===== Q16
R-35 routes [('BI', 'Voters', 'high', '87% of adults favored congressional term limits (Pew, July 2023).', None), ('AV', 'Amendment', 'very low', None, None)]
R-35 effects_confidence medium | status {"text": "Research on state legislatures links term limits to weaker legislative capacity.", "checked": "2026-10-15", "result": "confirmed", "sources": ["N52", "N53"]}
===== Q17
variable fields ['band', 'cluster', 'description', 'domain', 'id', 'increase_means', 'indicator', 'indicator_note', 'kind_plain', 'layer', 'part_of', 'records', 'title', 'type'] | a why-it-matters field: none
Loop R18 valence = "Harmful; this is 's B1b with its true polarity. When the person inspected can remove the inspector, the breaker becomes a bypass."
```
