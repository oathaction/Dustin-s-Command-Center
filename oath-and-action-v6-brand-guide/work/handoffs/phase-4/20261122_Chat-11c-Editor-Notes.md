# Chat 11c editor notes

Editor, chat 11c, November 22, 2026. Brief: `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`, section 6.1. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/e76584b2-1bba-5266-a75e-730f247433d8/scratchpad/c11c/editor/`. Started 21:48:24 UTC (`date -u`); notes opened 21:49:11 UTC.

Read first: my role file; `CLAUDE.md`; chapter 02's writing rules; the decision log from line 7342 to its end (D4-100 to D4-241, DR-305 to DR-325); chapter 21's plan, sections 1 to 13; Master Brief sections 3, 8, 15 and 23; chat 11b's editor notes for the identity chain's side effects (D4-222).

## Routine calls

- D4-xxx | DR-323 ran `phase3_ch13_build.py` alone, with no run of `phase3_ch14_build.py` | Chapter 14's build reads its own plan, entries and specs and never `13-evidence.json`, so chapter 13's assembly does not need it; `phase3_ch14_build.py --check` reads 99 of 99 files current after the change
- D4-xxx | The identity chain for DR-324 and DR-325 rewrote the same five files beyond chapter 03 that D4-222 names, and all five went back to their prior bytes from my scratch copies taken before the run: `s-04-1-correct`, `s-09-3-correct`, `s-09-3-failure`, `s-17-hinge-failure` and `work/boards/phase-2/stage-a/proofs/20261110_Letterhead-Proof.html` | They grew 72 to 10,108 bytes in the run (8,670 to 8,742; 9,728 to 9,912; 6,799 to 6,959; 14,823 to 16,063; 105,999 to 116,107), as in chat 11b, and DR-324 and DR-325 name Rule 03.6 alone. Each restored file now equals HEAD (`git diff --quiet`), and the rewritten copies sit in scratch, `identity-run-side-effects/`
- D4-xxx | Rule 03.6's correct plate keeps its label "Phone, 390 px: L1 from the 24 px master" | A 390 px window is 24.375em at the default text size, so it falls in the row "Site, from 24.375em to 48em", and D4-115 keeps the 24 px master at 390 px; the plate and the new words agree
- D4-xxx | Loop R18's status lines take Rule 15.19's step words in the form chapter 15's own stepper uses ("X lowers Y. Connection L14 “name”: the atlas grades it documented, and its effect takes under 2 years."), in place of the plan's draft lines, which printed each connection's plain text and left out its delay; the holds, counted again, are 9,250 and 16,000 ms | Rule 15.19 is approved and lists the step words: the variables, the sign's verb, the connection, what moves along it, its grade and its delay; the counting script gives chapter 15's three holds exactly, so the method matches D3-1755's
- D4-xxx | The tab titles' first parts read "Atlas home", "Reform R-23", "The Register", "Loop R18", "Loops" and "How to read", with no record title, where the plan's drafts paraphrased two stored titles and my first draft quoted them | The design director's rule for the word fields: the atlas's stored text never goes in a field (DR-37), and `page_words` prints the view words as typed; the kind word names what each ID refers to (house rule H11). A `{title}` fill would let the tab carry the record's title (Requests)
- D4-xxx | "Dark theme" wherever the plan says "dark mode", and the basis lines carry no decision or ruling codes, only reader words with the date of the approval, as chapter 20's do | D4-194 (Rule 18.4's word); chapter 13's check bars studio codes from reader text
- D4-xxx | ED-F4's line reads "The loop holds only as firmly as this step." where the draft said "link" | The page, Rule 15.13 and the stepper call each connection of a loop a step (house rule H02: keep the same term)
- D4-xxx | DR-321's note reads "These titles print as our atlas stores them, and its next version reviews the titles that state an effect, among them those of Loop R5 and Loop R11." | DR-321 asks for a one-line note that the next version reviews titles that state an effect; V7.1 item 44 names R5 and R11, and the note says the review is coming without ruling on either title before it happens
- D4-xxx | The loop page's heading for the stored `adaptation` passage reads "How it adapts", where the design director's draft read "The other side’s instances" | The field holds how people work around a loop on every loop ("Money re-routes …" on R1, "Incumbents shift blame …" on B4); a heading that names the other party fits Loop R18 alone and frames the record by party (DR-93, house rule H10); the passage itself prints as stored
- D4-xxx | The reform page's kicker carries the band word as stored ("Parameter"), and the status panel quotes the band's whole definition, where the specs' draft put "Changes a number" in the kicker | Rule 15.11's specification asks for "the atlas’s word and its definition, quoted"; a clause cut at the definition's colon would run to ten words for the feedback band
- D4-xxx | The Grades section's labels read "Evidence of the problem" and "Evidence for the remedy"; "The problem" and "The remedy" stay as the status panel's short rows | Rule 15.12's specification rows name those labels
- D4-xxx | Rule 21.4 says a contested remedy sets "the readings its record holds side by side, in the atlas’s own words", where the plan's draft said "print both readings at the same length" | The readings are the atlas's stored text, which prints as stored (DR-37), so only an edit could make them equal; DR-93 bars manufactured balance, and DR-314 and DR-323 set the same principle for Act pieces ("at the length the record holds"). House rule H08 still governs every title and sentence we write about a contested grade
- D4-xxx | Captions and alts in the generator name no stored text and type no count the model holds: the opener and Rule 21.3 speak of "a question about medical bills" and "the parts it reaches", and the counts that print come from the generator's own fills ({connections}, {double}, {answer_sources}, {loops}, {snapshot}) | The design director's field rules (a `{name}` is a fact the build fills; stored text never in a field) and the coordinator's "write words, not typed counts or holds"
- D4-xxx | The reform page's `problem` and `remedy` keys read "Evidence of the problem" and "Evidence for the remedy", in the status panel and over the two grades alike, and the routes' head says "Feasibility" where the draft said "How likely" | The kit reads one key for both places, and Rule 15.12's specification names those labels; the atlas rates a route's feasibility, whether it is open, which "how likely" would misstate (Rule 15.24 prints "the entry’s feasibility in the atlas’s word")
- D4-xxx | The Register's `rejected_grade` holds our own words, "For a rejected option, the grade measures confidence in harm", where the draft typed the atlas's sentence | The atlas's sentence is stored text, which the kit quotes from the model (specs 10.1); our line introduces it
- D4-xxx | `whole_issues` keeps "{n}, one retired" | The generator's Rule 21.9 failure plate formats it with `n` alone, so a `{retired}` fill stopped `--check` (KeyError, 22:37 UTC); the word stays until the generator fills the count (Requests)

## Rulings

None of my own; I follow the data visualization lead's and the design director's as they land.

## Words for

Chapter 21's words, drafted here until the design director hands the generator's word fields over by name (brief 6.1 step 6). Drafted between 21:55 and 22:05 UTC (`date -u` read at 21:55:27 before the first draft and 22:05:11 after it landed here), and aligned with the design director's specs, hand-overs 1 and 2, at 22:06:59 UTC. Nothing here is in `phase4_ch21_build.py` yet.

How to read this section:

- `{…}` marks a value the generator or the kit reads from the model at build time, never typed: today's value follows in square brackets, for checking only (the data lead's R9). A count names its `data-count-of` method where the data lead's R2 lists one.
- The atlas's stored text (titles, questions, summaries, short answers, citations, cases, the subtitle, the band words, the "higher value" sentences) prints as stored (DR-37) and is never mine; I name the field it comes from.
- Grade words: in a label or a key, Rule 13.3's display word with its capital (Documented, Well supported, Plausible, Contested, Hypothesis); inside a sentence, the same word in lower case ("the atlas grades it plausible"), as chapter 15's stepper prints it.
- "Dark theme" everywhere the plan says "dark mode" (D4-194, Rule 18.4's word). "The model" for the atlas's data, defined once in Rule 21.16.
- Typed chips: wherever a page's words hold an ID, the words are written so the kit can set "Kind ID" in its chip ("Loop R18", "Reform R-23"); in the guide's own rule prose the kind word in plain text does the chip's job (Rule 13.9).

### 1. The chapter (generator's chapter fields, chapter 20's `W`)

- **title:** The atlas
- **instruction** (fixed by the architecture map, kept word for word): Apply the system to the atlas, with typed IDs and evidence a step from every claim.
- **intro**, two paragraphs:
  1. "Our systems atlas, Who Do They Answer To?, lives inside our website, under the site’s masthead, with a title bar of its own. Its home page draws the whole system and starts from a question a reader brings. Each proposed change the atlas weighs, a reform, has a page, and so does each loop, a chain of causes that returns to where it started. The Register files every one of the atlas’s {connections} [118] connections, the arrows from one variable to another, once and with its evidence. An index lists the loops, and a page called How to read explains every mark."
  2. "Chapter 15 sets how each mechanism is drawn, and these pages use its rules as they stand. This chapter covers what a page adds around the drawing. A page names every ID in a typed chip, the label that gives the kind of record with its code, and links every claim to the record that grades it. Before a page ships, the atlas test checks each value it prints against the atlas’s own data."
- **groups:**
  - 21.1, The atlas in our website: "Every atlas page sits under the site’s masthead with the atlas’s own title bar, and the home page draws the whole system and answers a reader’s question."
  - 21.4, A page for each record: "A reform’s page answers a reader’s questions in order from its own record, and every chip and figure on it opens the record behind it."
  - 21.8, The Register: "The Register files each connection once, on one sheet, with its sign, grade and source, and keeps what the atlas rejected in view."
  - 21.12, Loop pages: "A loop page reads the loop’s signs aloud and names its weakest step, and its stepper moves at a pace a reader can follow."
  - 21.15, The dark theme and the atlas test: "The atlas keeps every mark on Charcoal, and each page passes one test against the atlas’s data before it ships."
- **opener_caption:** "Our systems atlas’s home page inside our website, at 1440 and 390 px in the light and the dark theme. A reader has pressed “{pathway question}” [Why can the same care produce different bills?], and the drawing keeps the {question-parts:PW06 in words} [three] parts it reaches at full strength."
- **opener_alt:** "Four frames of the atlas’s home page, at 1440 px and 390 px, each in the light and the dark theme. Under the site’s masthead and the atlas’s title bar, the atlas’s eight parts sit as boxes, with a count on each arrow between them on the desktop and as a stacked list on the phone. The question “{pathway question}” is pressed, and {lit parts, joined} [Wealth, Checks and Your household] stay in full ink while the other parts are muted."
- **related_chapters:**
  - 05: "One working red a view, and each section’s opening screen measured as Rule 05.1 sets."
  - 10: "The atlas’s parts named in words, with no icon (Rule 10.8)."
  - 12: "The red target and the locator (Rules 12.5 and 12.7)."
  - 13: "Grade words and lines, delay ticks, typed chips, dates and source lines."
  - 15: "Every mechanism these pages draw."
  - 17: "The pressed, muted and current looks, and the stepper’s motion."
  - 18: "The chip, stepper, chooser, filters, toggle, disclosure and table."
  - 19: "The accessibility map these pages add to."
  - 20: "The masthead, menu, footer and theme switch the atlas sits in."
  - 28: "The atlas test’s lines on the standards checklist."
- **sources:**
  - "Source: Oath & Action, Who Do They Answer To?, the Oath & Action Systems Atlas, snapshot of {snapshot in words} [October 15, 2026], read from its data file at each build. Every value on the atlas’s pages."
  - "Source: W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024, retrieved November 21, 2026. Behind Rules 21.1, 21.3, 21.11 and 21.13."

### 2. Words every atlas page shares (the kit's `atlas` object, contract C9)

- `views_label`: "Atlas views" (the navigation's name and the phone's disclosure button)
- `views`, in order: "Home", "Loops", "Reforms", "The Register", "How to read" (the paths are the engineer's)
- `snapshot`: "Snapshot of {date}"
- The title bar's name and subtitle are stored: `meta.title` [Who Do They Answer To?] and `meta.subtitle` [The Oath & Action Systems Atlas].
- `views_button` (the design director's key, specs 2.4; at most 46 px in `oa.type.ui`): "Views" (44.3 px, the specs' measure). The navigation keeps its name, "Atlas views", so a screen reader hears "Views, button, collapsed" inside it.
- `breadcrumb_label`: "Breadcrumb"
- `locator_alt`, the locator link's name (its drawing is `aria-hidden`; specs 3.2): "Atlas home. This page sits in {part}." (`{part}` the plain part name, such as Checks; two parts joined with "and")

### 3. Page titles, current view and breadcrumbs (AL-01: "[view] | Who Do They Answer To? | Oath & Action")

| App | `title` | `current_view` | `crumbs` (the page's own crumb is the kit's chip) |
|---|---|---|---|
| A11 | Home \| Who Do They Answer To? \| Oath & Action | Home | none |
| A12 | {Reform R-23}, {stored title} \| Who Do They Answer To? \| Oath & Action [Reform R-23, Minimum wage that rises with an index \| …] | Reforms | Home, Reforms, then Reform R-23 |
| A13 | The Register: {domain title} \| Who Do They Answer To? \| Oath & Action [The Register: Congress, agencies and public services \| …] | The Register | Home, then The Register (specs 3.1: the Register is its own view page) |
| A14 | {Loop R18}, “{stored title}” \| Who Do They Answer To? \| Oath & Action [Loop R18, “Weakening watchdogs lowers the cost of further unilateral action” \| …] | Loops | Home, Loops, then Loop R18 |
| A15 | Loops \| Who Do They Answer To? \| Oath & Action | Loops | Home, then Loops |
| A16 | How to read \| Who Do They Answer To? \| Oath & Action | How to read | Home, then How to read |

The view comes first in every title, so a reader with many tabs open sees the page's own words. The plan's drafts ("a minimum wage that rises with an index", "weakening watchdogs") paraphrased stored titles; these take each title whole, and a loop's title in quotation marks as Rule 18.22 sets.

### 4. Page words by view (the kit's `page` keys; the design director's specs name the final keys)

**A11, the atlas home**

- h1: "Who do they answer to?"
- intro: "Our systems atlas holds {variables} [51] variables, the quantities and conditions that can rise or fall, and {connections} [118] connections between them. It traces {loops} [23] loops, {loops-numbered} [20] of them with numbered steps, weighs {reforms} [50] reforms and files {issues} [194] issue records, {issues-retired in words} [one] of them retired. Start from the drawing, or from a question you bring."
- Part names and questions, Dustin's words (DR-35, DR-41), each with the model's title beneath: Outside forces (no question in DR-35; the box prints its name and the model's title alone); Wealth, "Who holds the cards?"; Voice, "Who pays for influence?"; Elections, "Who picks them?"; Checks, "Who checks their work?"; Policy, "Whose side are the rules on?"; Your household, "Who lives with the results?"; Technology, "Who controls the machines?"
- Box counts: "{n} variables" ("1 variable"); "{n} connections inside" ("1 connection inside"; for 0, "no connections inside")
- Key: "The main circuit, from Wealth through Voice, Elections, Checks and Policy and back to Wealth, draws in full ink with its counts in bold. The other flows draw lighter. Each number counts the connections inside a part or along an arrow."
- Phone flow lines (data lead's R7, outgoing only): "{n} to {part}", such as "5 to Voice"
- Switch (Rule 18.2: the same words pressed or not): "Show every variable"
- Questions section heading: "Start from a question"; the hubs' titles and the questions print as stored
- Lit box words: "This question reaches here"
- Status line after a press: "This question reaches {n in words} parts: {parts}." [This question reaches three parts: Wealth, Checks and Your household.] After a press that unpresses it: "No question is pressed, so every part shows at full strength."
- Answer heading: "The short answer"; the answer prints `pathways[PW06].short_answer` as stored
- Claim disclosure (data lead's R5) labels, in order: "Claim", "Grade", "People", "Place", "Period", "Limit", "Source"; its summary words: "The claim’s record"

**A12, Reform R-23's page**

- Kicker (specs 9.1): the chip, a middle dot, then the band word as the atlas stores it, capitalized [Reform R-23 · Parameter]. The specs' draft "Changes a number" is the first clause of the band's stored definition; the band word in the kicker and the whole definition in the status panel give Rule 15.11's "word and its definition, quoted" for every band, where a clause cut at the colon would run to ten words for the feedback band.
- Status panel (specs 9.1): label "Where it stands"; `status.text` as stored; "As of {status.checked in words}" [As of October 15, 2026]; then two rows, "The problem" and "The remedy", each with its display word, each linked to its block below; then "Band: {band word}" and `leverage.bands[band]` quoted
- Section headings, in the specs' order: "Where it acts" (h3); "How sure our atlas is"; "What it would change"; "How it could pass"; "Works alongside" (h3, the complements; the specs' draft, kept); "Sources for this page" (the disclosure's words)
- Where it acts, the note (Rule 12.5): "{Reform R-23} acts where the marks turn red: on {Variable EC7}, {title} and {Variable A4}, {title}." [… on Variable EC7, Household income and Variable A4, Households’ financial security.]
- Each target's sentence on a higher value prints `nodes[k].increase_means` as stored, under its chip and title
- The loop it touches (specs 9.1's "It touches" block): label "The loop it touches"; the chip and stored title; then "Its steps hold neither of the reform’s targets, so the drawing leaves it out." (with more than two targets, "none of the reform’s targets")
- Ink tags (Rule 21.5): one reform, "{chip} also aims here"; several, "{chips} also aim here", stacked under one leader line; past four, "and {n} more"
- The two grades, the `Grades` section: labels "Evidence of the problem" and "Evidence for the remedy", Rule 15.12's own words (its specification row asks for them), where the specs' draft has "The problem" and "The remedy" (those stay as the status panel's short rows); each with Rule 13.3's word and gloss and the atlas's text quoted; the remedy's text in the two blocks `remedy_split` sets
- Effects: date line "As of {status date in words}" (specs 9.1); each row the family name ("Quality of democracy" for DQ, DR-39), the pips, the code whole with true minus signs, a comma and its words from `outcomes.effect_codes`; the data lead's R12 range row: "0 to −S at high bite, no expected effect to small negative" (stored code, then the two ends' words joined by "to"). Under the rows, label "Confidence" and the stored words quoted [“high to 60% of median; low above”]
- Routes: each row the route's chip and name, "who acts", the feasibility word, the note as stored where there is one, and "Checked {date}" or "Not checked"; feasibility label "Feasibility"
- Works alongside: the complement's chip and stored title

**A13, the Register with sheet D04 open**

- h1: "The Register"
- Lede: "Every connection in our atlas files once, on the sheet of the variable it moves. Each sheet counts its records and grades, and every number below can be checked line by line."
- Index column heads: "Sheet", "Variables", "Connections", "Loops", "Reforms", "Issue records", then "Documented", "Well supported", "Plausible", "Contested", "Hypothesis" (each with its 40 px line sample)
- Layer rows print the layers' titles as stored [How the economy reaches a household; Technology and its effects]; their issue cell: "None filed"
- Whole row: "The whole atlas"; its issue cell: "{issues} [194], {issues-retired in words} [one] retired"
- Note under the index: "The whole atlas counts each loop and reform once, though many reach several sheets. The reforms column leaves out the reform the atlas rejects."
- Sheet heading: the chip, the domain's stored title and its stored everyday question
- Sheet subheadings: "Variables on this sheet"; "Connections filed here"; "Issue records"
- Connection table heads: "Connection", "From", "To", "Sign", "Type", "Delay", "Grade", "Citation"; sign words "raises" and "lowers"; authority "decides"; causal rows leave the type cell as "Causal"; delay words "under 2 years", "2 to 10 years", "over 10 years"
- Rejected option block: heading "Rejected option"; then the chip and the stored title, the effects and the remedy's grade word with the atlas's words quoted beneath it. **Question in Requests:** Reform R-35's stored title already opens "Rejected option: term limits for legislators", so the heading and the title say "Rejected option" twice.
- Reviewed and not drawn block (Rule 15.10): heading "Reviewed and not drawn"; each row "reviewed connection {LTR id}, from {Variable chip} {title} to {Variable chip} {title}", then the reason quoted (data lead's R11: no chip for LTR IDs)
- Filters (Rule 18.16): button "Filters, {n} on" (no filter: "Filters"); each check box "{Variable chip} {title}, {n} records"; "Clear filters"
- Count line, after each change only: "{n} of {total} issue records." [9 of 20 issue records.]
- Each record row: chip, stored title, grade word

**A14, Loop R18's page**

- Kind word beside the chip: "Reinforcing loop" or "Balancing loop"
- h1: the stored title in quotation marks [“Weakening watchdogs lowers the cost of further unilateral action”]
- Grade line (data lead's R11, composed): "Our atlas grades this loop {least grade, lower case}, the grade of its {weaker | weakest} step: {stored evidence text, each grade as its display word in lower case and each code as its chip}." [Our atlas grades this loop plausible, the grade of its weaker step: documented for Variable D2 to Variable D4, and plausible for Variable D4 to Variable D2.] "weaker" for a loop of two steps, "weakest" for more. Where the stored text joins with "; ", print ", and ".
- Facts panel (specs 8.1): label "This loop"; rows "Kind" [Reinforcing], "Steps" [2], "Minus signs" ["2, an even count"; odd: "1, an odd count"; none: "None, an even count"], "How it closes" [the stored closure, closed: every step is a numbered connection], "Delay" [ticks and 2 to 10 years], "Weakest step" [the chip Connection L15 and Plausible]
- Section heading (specs 8.1): "Step through the loop". Label above the sentence: "Read aloud".
- Read-aloud line (data lead's R4; one clause per step, each step clause a chip): "{First variable title} rises. Across {Connection chip}, a minus, {next title, lower case} falls, and across {Connection chip}, another minus, {first title, lower case} rises again, the same way it started." [Presidential action without new legislation rises. Across Connection L14, a minus, the ability to investigate and enforce the rules falls, and across Connection L15, another minus, presidential action without new legislation rises again, the same way it started.] Template words: "a plus" or "a minus" at a step's first sign of its kind, "another plus" or "another minus" after; "rises" or "falls" by R4's turn; the last clause ends "the same way it started" when the first variable returns rising, "the other way from how it started" when it returns falling. Titles enter as chapter 15's `SAY` sets (the engineer's D2 entry: no article, singular).
- The two lines under it (specs 8.1: ED-F6's line, then the arithmetic): ED-F6's line, "This reading starts with a rise and turns at each minus sign."; the arithmetic, "{Count in words, capitalized} minus signs, an even count, make {Loop R18} reinforcing, so it feeds itself." [Two minus signs, an even count, make Loop R18 reinforcing, so it feeds itself.] Odd count: "… {n} minus sign(s), an odd count, make(s) {Loop Bn} balancing, so it pushes back on the first change." No minus sign: "With no minus sign, an even count, {Loop Rn} is reinforcing, so it feeds itself."
- Weakest step (ED-F4, Rule 15.13): label "Weakest step"; line "The loop holds only as firmly as this step." (ED-F4's draft said "link"; "step" is the term the page and chapter 15 use)
- Stepper: section 5 below
- Chooser legend (Rule 15.20, a radio group): "Reforms that aim at this loop" (the specs' draft, kept); the chosen reform's note: "{Reform chip} acts where the marks turn red: on {targets, each chip and title}." Panel labels as A12's: "Band", "What it would change", "How it could pass"
- Ink tags for the others (Rule 21.5): "{Reform R-15} and {Reform R-48} also aim here"
- Section heading: "The loop in our atlas’s words"; subheads for the four stored passages: "Summary", "The case", "What it depends on" (qualification) and "How it adapts" (adaptation). The specs' draft for the last, "The other side’s instances", fits Loop R18's passage alone and frames it by party; on other loops the field holds "Money re-routes …" (R1) or "Incumbents shift blame …" (B4), how people work around the loop, so the heading names the field (DR-93, house rule H10)
- "Evidence for each step" (heading); each row "Step 1", "Step 2"; then: "Each step’s grade and citation sit on its line in the Register: {Connection L14} on the sheet for {Domain D04}, and {Connection L15} on the sheet for {Domain D05}."
- Issue records (specs 8.1): label "Issue records on this loop"; "{loop-records} [8] issue records name this loop. See them in the Register." (the second sentence is the link)

**A15, the loop index**

- h1: "Every loop in the atlas"
- Group heads: "Reinforcing loops, {n}" and "Balancing loops, {n}" [18, 5]
- Column heads: "Loop", "Title", "Steps", "Minus signs", "How it closes", "Grade"
- A conceptual loop's steps and minus signs cells: "No numbered chain" (Rule 15.18)
- DR-321's note under the index: "These titles print as our atlas stores them, and its next version reviews the titles that state an effect, among them those of Loop R5 and Loop R11."

**A16, How to read**

- h1: "How to read the atlas"
- Intro: "Each mark below appears on the atlas’s pages, with what it means. Its row names the rule in our brand guide that sets it." (**Question in Requests:** whether a public page prints guide rule numbers; plan 3.8 asks for them.)
- Rows, each "mark: words (rule)":
  - Sign tag: "Plus, raises: the two variables tend to move the same way. Minus, lowers: they move in opposite directions. “A positive sign does not mean a benefit.”" (15.3; the last sentence is the atlas's, quoted, as Rule 15.3 asks in every key that shows a sign)
  - Type words: "Money, information or ownership before the verb says what moves along a connection. A causal connection takes the verb alone." (15.4)
  - Authority: "An open diamond and the word decides: one body holds legal power over something. It carries no sign and never closes a loop." (15.5)
  - Grade lines, five rows: "Documented, on the public record: a solid line, with the record square"; "Well supported, strong research evidence: a solid line"; "Plausible, some evidence: a dashed line"; "Contested, evidence disputed: dash and dot"; "Hypothesis, not yet tested: dots" (13.3, 13.4)
  - Record square: "A filled square before Documented: the public record itself shows the link." (13.4)
  - Delay ticks: "One tick, under 2 years; two, 2 to 10 years; three, over 10 years." (13.5)
  - Hollow line: "A step of a conceptual loop, one with no complete chain of numbered connections." (15.7)
  - Red target: "Red marks where the chosen reform acts: each connection it changes and the outline of each variable it targets." (12.5)
  - Typed chip: "The kind of record and its code together, such as Loop R18. A chip that is a link opens the record." (13.9)
  - Pressed question: "A check, bold words and a heavier edge mark the question you pressed." (17.10)

### 5. The stepper's status lines, with counts and holds (AL-24)

Each step follows Rule 15.19's step words, "the variables’ titles and the sign’s verb, then the connection, what moves along it, its grade and its delay", in the form chapter 15's own Loop R1 stepper uses (`s-15-19-correct`). Loop R18's two connections are causal, so no type word (Rule 15.4). Counted by script (scratch `holds.py`) the way chapter 18's script builds the status line, "Step i of n: " + line + " " + more, whitespace collapsed; the same script gives chapter 15's three holds exactly (9,750, 12,750 and 15,250 ms). Hold = 250 ms a word, never under 6,000 ms.

| Step | `line` | `more` | Words the status line reads | Hold, `data-oa-hold` |
|---|---|---|---|---|
| 1 | Presidential action without new legislation lowers the ability to investigate and enforce the rules. | Connection L14 “Presidential removals weaken watchdog agencies”: the atlas grades it documented, and its effect takes under 2 years. | 37 | 9,250 ms |
| 2 | The ability to investigate and enforce the rules can lower presidential action without new legislation. | Connection L15 “Independent watchdogs restrain unilateral action”: the atlas grades it plausible, the weaker of the loop’s two steps, and its effect takes 2 to 10 years. The loop is back where it began, and with a minus sign on both steps it is reinforcing. | 64 | 16,000 ms |

What the status line reads, whole:

- Step 1, 37 words, 9,250 ms: "Step 1 of 2: Presidential action without new legislation lowers the ability to investigate and enforce the rules. Connection L14 “Presidential removals weaken watchdog agencies”: the atlas grades it documented, and its effect takes under 2 years."
- Step 2, 64 words, 16,000 ms: "Step 2 of 2: The ability to investigate and enforce the rules can lower presidential action without new legislation. Connection L15 “Independent watchdogs restrain unilateral action”: the atlas grades it plausible, the weaker of the loop’s two steps, and its effect takes 2 to 10 years. The loop is back where it began, and with a minus sign on both steps it is reinforcing."

Ready line (`data-oa-ready`, untimed): "Ready. Start at presidential action without new legislation, and suppose it rises. Press Play, or Next step to follow one connection at a time."

Model values inside these lines, for the kit to read and the atlas test to check: the two variables' titles, each connection's ID, stored name, grade and delay, the sign verbs ("lowers"; "can lower" for a plausible step, house rule H08), and the weakest step (data lead's R8: L15). If any of them changes, the words change and the holds are counted again.

### 6. Rules 21.1 to 21.16

Each rule's fields in chapter 20's order. Measures in specifications follow the design director's specs where they differ; I will match them once the specs land.

#### 21.1

- **title:** Set every atlas page under the site’s masthead, with the atlas’s title bar beneath.
- **rule:**
  1. "Our systems atlas is one part of our website, so every atlas page opens with the site’s masthead, with Who Do They Answer To? marked as the part the reader is in. Directly under it, the atlas’s title bar gives the atlas’s name, the date of its snapshot (Rule 13.10) and its views: Home, Loops, Reforms, The Register and How to read."
  2. "Every page below the home adds a breadcrumb, the trail of links from the home to the page, and on wide screens a small locator that shows where the page sits in the whole system. Each page’s title names the view first, then the atlas, then Oath & Action."
- **why:** "A reader who reaches the atlas from a search or a shared link still sees whose site they are on and can reach every other part of it. The title bar keeps the atlas’s own views one step away, and it is the same Charcoal band that opens the atlas’s section on our home page."
- **basis:** "The atlas’s place inside our website, under the site’s masthead with a title bar of its own, approved by our founder and editor on November 21, 2026; WCAG 2.2 SC 2.4.2 and Technique G88; Rules 12.7 and 17.10; design judgment for the title bar’s contents"
- **specs:**
  - Order: "Skip link, the site’s masthead, the atlas’s title bar, the breadcrumb, the page, the site’s footer"
  - Title bar: "A Charcoal band from edge to edge in both themes, under the masthead’s hairline: the atlas’s name in the label style, its subtitle and snapshot date in the caption style, and the five views in a navigation named “Atlas views”"
  - Current view: "Bold words and a 2 px underline (Rule 17.10)"
  - Phones: "The atlas’s name, its snapshot date and a Views button, 44 px tall, that opens the five views in place (Rule 18.8)"
  - Breadcrumb: "On every page below the home, in a navigation named “Breadcrumb”; the current page last, in bold with no underline"
  - Locator: "88 by 41 px at the breadcrumb’s right end, the parts the page sits in filled in ink; a link to the atlas home; hidden on phones (Rule 12.7)"
  - Page title: "The view, then Who Do They Answer To?, then Oath & Action, joined by vertical bars"
  - Landmarks: "One banner, the site’s; three named navigations, the site’s parts, Atlas views and the breadcrumb; one main; one footer"
- **builders:** "Draw the masthead and footer with the website’s own code, add the title bar as a second named navigation, and build each page title from the view’s own words."
- **correct_caption:** "The top of Loop R18’s page at 1440 px, and at 390 px with Atlas views open: the site’s masthead with the atlas as the current part, the atlas’s title bar, the breadcrumb and, on the desktop, the locator. Above each frame, the page’s title as a browser tab shows it."
- **correct_alt:** "Two page tops. At 1440 px, the skip link in focus above the site’s masthead, where Who Do They Answer To? is underlined; then the atlas’s title bar, a Charcoal band with its name, its subtitle and snapshot date and five views, Loops underlined; then the breadcrumb Home, Loops, Loop R18, with a small locator at the right that fills Checks. At 390 px, the wordmark and Menu, then the band with the atlas’s name, its snapshot date and a Views button, its five views open beneath."
- **failure_caption:** "<strong>Fails Rule 21.1.</strong> The atlas brings a masthead of its own, so a reader sees two sets of links and cannot tell whose site they are on, and the tab’s title names no page."
- **failure_alt:** "A page top with two banners: the site’s masthead with no part marked, and under it a second masthead with the atlas’s own wordmark and its own copy of the site’s parts. The tab’s title reads Oath & Action alone."

#### 21.2

- **title:** Open the atlas home on the whole system, with a count on every flow.
- **rule:**
  1. "Start the atlas’s home page with the whole system on the first screen. Each of its eight parts takes a box with its name, its question and the count of connections inside it. Where two parts connect, an arrow runs each way that connections run, with the count it carries."
  2. "Draw the main circuit, from Wealth through Voice, Elections, Checks and Policy and back to Wealth, in full ink with its counts in bold, and the other flows in a lighter ink, every arrow at one width. A switch, Show every variable, opens each box in place to list its variables and closes them again, so the page draws the system once."
- **why:** "A newcomer sees how the parts fit together before reading any one of them, and every number on the drawing is a count a reader can check in the Register. One drawing that opens in place keeps the first screen short."
- **basis:** "The plain names and questions our founder and editor set for the atlas’s parts, with the model’s titles beneath; Rules 15.1, 15.2 and 15.9; the model’s parts and connections; design judgment, from our earlier drawings of the atlas (Rule 15.25)"
- **specs:**
  - Parts: "Eight boxes in the order effects travel: Outside forces, Wealth, Voice, Elections, Checks, Policy, Your household and Technology, each with its plain name, its question and the model’s title beneath"
  - Boxes and pills: "A part takes a box with square corners, and a variable a pill (Rule 15.2)"
  - Counts: "Inside each box and on each arrow, in the data label style with tabular figures, read from the model at each build"
  - Ink: "The main circuit in the essential graphic ink, its counts bold; the other flows in the subtle graphic ink; every count in the text’s ink; one width, 2 px"
  - Arrows: "One for each direction two parts connect, never a double head"
  - Switch: "A toggle button, Show every variable, with aria-pressed (Rule 18.2)"
  - Phones: "A stacked list in the same order, each part with its counts and one line for each flow it sends, such as “5 to Voice”, so each flow prints once"
  - Redrawing: "When the model adds or removes a part, the boxes reflow in the order effects travel, and the build stops if a count on the drawing differs from the model"
- **builders:** "Count every number on the drawing from the model at each build, and stop the build when a count and the model disagree."
- **correct_caption:** "The home drawing with Show every variable pressed, each of the eight parts opened to its variables, {variables} [51] in all, at 1440 px in the light theme."
- **correct_alt:** "The atlas’s eight parts as boxes, each opened to list its variables as pills, with arrows and counts between the boxes and the main circuit drawn darker."
- **failure_caption:** "<strong>Fails Rule 21.2.</strong> The arrows widen with their counts and nothing on the drawing says what a width measures, so Your household to Wealth, which carries {flow:EC>A} [7], outweighs every step of the main circuit."
- **failure_alt:** "The same eight boxes with arrows of many widths and no key. The arrow from Your household to Wealth is the widest."

#### 21.3

- **title:** Light the parts an everyday question reaches, and name them in words.
- **rule:**
  1. "Offer the atlas’s everyday questions under the {hubs in words} [five] topics the atlas calls hubs, each question as a button. When a reader presses one, it takes the pressed look of Rule 17.10: a check before its words, bold words and a 2 px edge."
  2. "The parts that hold the question’s variables stay at full strength with the words This question reaches here, and the others turn muted (Rule 17.8). A status line names the reached parts in words, and the answer opens below, with each figure in it linked to its evidence."
- **why:** "A reader who arrives with a bill in hand sees at once which parts of the system decide it. Words carry the result too, so a reader who cannot see the shading, or who prints the page in gray, gets the same answer."
- **basis:** "Rules 17.8 and 17.10; the question’s own record in the atlas, which lists the variables it touches; WCAG 2.2 SC 1.4.1 and 4.1.3"
- **specs:**
  - Question: "A toggle button with aria-pressed, one pressed at a time"
  - Pressed: "The selected check before the words, bold words and a 2 px edge in the strong border color; unpressed, a 1 px edge (Rule 17.10)"
  - Lit parts: "Each part that holds a variable the question’s record names, at full strength, with “This question reaches here”"
  - The rest: "Muted outlines (Rule 17.8), their words still in the text’s ink"
  - Status line: "Names the reached parts in words after each press, never on load"
  - Topics: "Named in words, with no chip (Rule 10.8)"
- **builders:** "Light a part only where the question’s own record names a variable in it, and write the same parts in the status line."
- **correct_caption:** "“{pathway question}” pressed beside questions left unpressed, and the {n in words} [three] parts it reaches, at 1440 and 390 px in the light and the dark theme."
- **correct_alt:** "Four frames of the questions and the drawing. The pressed question carries a check, bold words and a heavier edge. {Lit parts} [Wealth, Checks and Your household] stay in full ink with the words This question reaches here, and the other five parts are muted."
- **failure_caption:** "<strong>Fails Rule 21.3.</strong> Only the weight of its words shows which question is pressed, and only a tint shows which parts it reaches, so the answer is lost in gray print and to a reader who cannot see the tint."
- **failure_alt:** "The same questions with one set in bold and no check or heavier edge, and three of the eight boxes tinted with no words."

#### 21.4

- **title:** Build a reform’s page from its own record, in the order a reader asks.
- **rule:**
  1. "Give each reform a page that answers a reader’s questions in order: what it is and its status, with the date; where it acts, drawn at its targets, the variables and connections it acts on; how sure our atlas is that the problem exists and that the remedy works, as two grades; what it would change in each outcome family, the four groups of results the atlas judges reforms by, one to a row; how it could pass, route by route, each with its check date or Not checked; and where its evidence comes from."
  2. "When the atlas grades a remedy contested, set the readings its record holds side by side, in the atlas’s own words, so a reader meets both before the routes."
- **why:** "A reader who asks whether a reform would work gets the evidence for the answer before the routes, and a contested remedy shows both sides of the dispute as our atlas records them."
- **basis:** "Rules 15.11, 15.12, 15.16, 15.20 and 15.24, applied as one page; house rule H08 in chapter 02; Reform R-23’s own record in the atlas"
- **specs:**
  - Order: "Head and status; where it acts; the two grades; the four effects; routes; reforms it works with; sources"
  - Status: "“As of” and the date in words, from the record’s own check date (Rule 13.10)"
  - Contested remedy: "The readings the record holds, side by side on wide screens and one after the other on phones, each with its source a step away (house rule H08)"
  - Effects: "Rule 15.16’s rows in the atlas’s order, each code whole with its qualifier and a true minus; Quality of democracy names the first family"
  - Routes: "Rule 15.24’s rows, each with its check date or “Not checked”"
  - Sources: "In a disclosure, closed on load and open on paper (Rule 18.8), each in Rule 13.6’s six parts as far as the source record holds them"
- **builders:** "Read every field from the reform’s own record, and set a contested remedy’s readings as one pair."
- **correct_caption:** "Reform R-23’s page, “{stored title}” [Minimum wage that rises with an index], at 1440 and 390 px in the light and the dark theme."
- **correct_alt:** "Four frames of Reform R-23’s page. From the top: its chip and title, with its status as of October 15, 2026; a drawing of its two targets, Variables EC7 and A4, outlined in red and joined by Connection LE15 in ink, with four other reforms tagged at A4; the evidence of the problem, Documented, and for the remedy, Contested, with the two readings side by side; four effect rows; four routes, each Not checked; and a closed disclosure of sources." (IDs, grades, counts and the date from the model)
- **failure_caption:** "<strong>Fails Rule 21.4.</strong> The panel keeps the finding of little job loss, drops the Congressional Budget Office’s estimate and grades the remedy well supported. Our atlas grades it contested and records both."
- **failure_alt:** "Reform R-23’s remedy panel under the word Well supported, holding one reading: “Within studied ranges, evidence finds little job loss.”"

#### 21.5

- **title:** Tag reforms that share a target in ink, and keep the red for this one.
- **rule:** "On a reform’s page, only that reform’s targets turn red. Where other reforms in our atlas aim at the same variable or connection, tag the mark with each one’s chip and the words also aims here, in the text’s ink. On a loop page, where a reader chooses one reform, the others that aim at the loop take the same tags."
- **why:** "A reader learns that several reforms aim at the same place in the system, and the one red still shows which reform the page is about (Rule 05.3)."
- **basis:** "Rules 05.3 and 12.5; the reforms’ own lists of targets in the atlas; design judgment for the tags"
- **specs:**
  - Tag: "The reform’s typed chip and “also aims here”, in the data label style and the text’s ink, 6 px from the mark"
  - Several: "Stacked under one leader line, the chips then “also aim here”; past four, “and [n] more” with a link to the list"
  - Red: "The page’s own reform only (Rule 12.5); a tag never takes red, an outline or a fill"
- **builders:** "Find every reform whose own record names the same target, and draw its tag in ink."
- **correct_caption:** "Reform R-23’s two targets in red, and the {n in words} [four] reforms that also aim at Variable A4 tagged in ink, at 1440 and 390 px in the light theme."
- **correct_alt:** "Variables EC7 and A4 with red outlines, joined by an ink connection. Beside A4, a stack of four chips, Reform R-24, Reform R-25, Reform R-26 and Reform R-31, over the words also aim here."
- **failure_caption:** "<strong>Fails Rule 21.5.</strong> Five reforms share the red, so the page has five working reds and no longer shows which reform it is about."
- **failure_alt:** "The same two variables, with all five reforms’ chips set in red beside A4."

#### 21.6

- **title:** Name every record in its typed chip, and let the chip open its page.
- **rule:** "Every ID on an atlas page sits in its typed chip, the kind of record in words with its code, such as Loop R18 or Reform R-23. A chip that names a record with a page of its own links to that page, and a connection’s chip links to its line in the Register. The first time a page names a record, its name follows the chip."
- **why:** "Our atlas uses B4 for a variable and for a loop, and Loop R1 sits one hyphen from Reform R-01. The word in the chip says which record a reader is looking at, and the link takes them to it."
- **basis:** "Rules 13.9 and 18.24; house rule H11 in chapter 02; the codes the atlas repeats across kinds of record"
- **specs:**
  - Kinds: "Rule 13.9’s ten words: Variable, Connection, Loop, Reform, Issue, Claim, Domain, Route, Rule change and Delivery case"
  - Chip: "Rule 18.24’s, plain or as a link with a target at least 24 px tall"
  - Link: "To the record’s own page, or for a connection to its line in the Register, with the record’s name as the link’s description where the words around it do not say it"
  - Kind word: "From where the ID lives in the model, never from its letters"
  - Check: "Every chip’s ID exists under its kind in the model (Rule 21.16)"
- **builders:** "Take each chip’s kind word from where its ID lives in the model, never from its letters."
- **correct_caption:** "A chip for each of the ten kinds of record, each a real record with its name, plain and as a link, then the four codes our atlas repeats across kinds, each pair with both names, on Newsprint and on Charcoal."
- **correct_alt:** "Two panels, light and dark. Ten chips, plain and linked, from Variable D4 to Delivery case DL05, each with its record’s name. Below them, four pairs side by side: Variable B4 and Loop B4, Loop R1 and Reform R-01, Variable D4 and Domain D04, and Variable X1 and Issue X01."
- **failure_caption:** "<strong>Fails Rule 21.6.</strong> Bare codes let a loop pass for a variable: B4 and R1 here are loops, filed under Variables."
- **failure_alt:** "A list under the heading Variables of three bare codes with names: B4, Electoral consequences can improve public performance; D4, Ability to investigate and enforce the rules; R1, Wealth and political influence reinforce each other."

#### 21.7

- **title:** Put the evidence one step from every claim.
- **rule:** "Every claim an atlas page makes reaches its evidence in one step. A figure links to the atlas’s claim record, which gives the claim, its grade, the people and place it covers, its period, its limit and its source. In the Register, a connection’s line gives its grade and citation, and every chip for that connection links there. A reform keeps its sources in a disclosure on its own page."
- **why:** "A reader who doubts a number or a step can check it from the page they are reading, and every claim we print shows where it comes from."
- **basis:** "The instruction for this chapter; Rules 13.6 and 13.9; the atlas’s claim and source records"
- **specs:**
  - Figure: "Its claim’s chip right after it, linked to the claim’s record in a disclosure on the same page"
  - Connection: "Its chip links to its line on its sheet of the Register"
  - Reform: "Its sources in a disclosure, closed on load and open on paper (Rule 18.8)"
  - One step: "One link or one disclosure, never a search"
  - Source lines: "Rule 13.6’s six parts, as far as the source record holds them"
- **builders:** "Give every figure and every connection on a page a link to its own record, and fail the build when one has none."
- **correct_caption:** "Two claims one step from their evidence, at 1440 px: the home answer’s figure opened to its claim record, and Loop R18’s first step beside its line in the Register."
- **correct_alt:** "Left, the answer’s sentence with the figure {figure as stored} [254% of Medicare rates in 2022] followed by the chip Claim CL1340, opened to its record: the claim, graded well supported, the people and place it covers, {period} [2020 to 2022], its limit and its source. Right, the chip Connection L14 on the loop page, and its line on the sheet for Domain D04."
- **failure_caption:** "<strong>Fails Rule 21.7.</strong> The figure points to a list of {source count} [29] sources at the foot of the page, and a reader cannot tell which one holds it."
- **failure_alt:** "The answer’s sentence with the figure and no chip, above a numbered list of {source count} [29] sources at the foot of the page."

#### 21.8

- **title:** Index the Register by sheet, and count each grade under its word.
- **rule:** "Open the Register with one row for each of its twelve sheets: one for each of the atlas’s ten domains, the subject areas it files records under, and one each for its economy and technology layers. Each row gives the sheet’s variables, connections, loops, reforms and issue records, then how many of its connections carry each grade. A last row counts the whole atlas, each loop and reform once."
- **why:** "A reader sees where the atlas’s evidence is strong and where it is thin, sheet by sheet, in numbers they can check line by line."
- **basis:** "Rules 13.3, 13.4 and 13.5; the model’s records, counted by one written method"
- **specs:**
  - Rows: "Domains D01 to D10 with their chips, then the two layers in words (Rule 10.8), then the whole atlas"
  - Counts: "Each connection on the sheet of the variable it moves; loops with numbered steps through the sheet’s variables; reforms the atlas has not rejected, with a target on the sheet"
  - Grade columns: "Rule 13.3’s five words in its order, each head with its 40 px line sample (Rule 13.4); never a shade, width or bar"
  - Issue records: "“None filed” for the two layers; the whole row says one is retired"
  - Whole atlas: "Each loop and reform counted once, with a note under the table that says so"
  - Table: "Rule 18.10’s markup with tabular figures; on phones, one card for each sheet"
- **builders:** "Count every column from the model by one written method, and print the method with the table."
- **correct_caption:** "The Register’s index of twelve sheets, with the sheet for Domain D04, {stored title} [Congress, agencies and public services], open below it, at 1440 and 390 px in the light and the dark theme."
- **correct_alt:** "Four frames of the Register. At the top, a table with a row for each of ten domains and two layers and a last row for the whole atlas, each giving its counts of variables, connections, loops, reforms and issue records, then five grade columns under their line samples. Below, the sheet for Domain D04 with its three variables, its ten connections, each with its sign, type, delay, grade line and citation, the rejected option Reform R-35, and its issue records behind a Filters button. At 390 px each sheet is a card."
- **failure_caption:** "<strong>Fails Rule 21.8.</strong> Shading ranks the grades and hides the counts, so a reader cannot tell how many connections on a sheet are a hypothesis."
- **failure_alt:** "The index with one bar for each sheet, shaded from dark to light, in place of the five grade columns, and no numbers."

#### 21.9

- **title:** File each connection once, on the sheet of the variable it moves.
- **rule:** "On each sheet, list every connection that moves one of the sheet’s variables, once, with its chip, the two variables it joins, its sign as a tag and a word, its type, its delay, its grade as a line and a word, and the atlas’s citation. Give each line an address of its own, so a chip anywhere in the atlas can link to it."
- **why:** "Filed once, every connection has one home a reader can find, and the sheets add up to the atlas’s {connections} [118]."
- **basis:** "Rules 13.4, 13.5 and 15.3 to 15.5; the atlas’s connection records"
- **specs:**
  - Filing: "By the variable the connection moves; a variable in the economy or technology layer files on that layer’s sheet, and one with two domains on the first"
  - Columns: "Chip; from and to by title, with chips; sign tag with raises or lowers; type in words (Rule 15.4); delay ticks and words; grade line and word; the citation as stored"
  - Authority: "“Decides” and the open diamond, with no sign (Rule 15.5)"
  - Address: "Each line’s own anchor, such as register-l14"
- **builders:** "File each connection by its variable’s sheet, and stop the build when the sheets do not add up to the model’s count."
- **correct_caption:** "The sheet for Domain D10, {stored title} [Taking part, trust and shared norms], its {sheet-connections in words} [ten] lines at 1440 px in the light theme, two of them contested, in the dash and dot with the word Contested."
- **correct_alt:** "A table of ten connections, each with its chip, its two variables, a sign tag with raises or lowers, its type, delay ticks, a line in its grade’s pattern with the grade’s word, and the atlas’s citation. Connections L09 and L47 draw dash and dot, marked Contested."
- **failure_caption:** "<strong>Fails Rule 21.9.</strong> Every connection appears on two sheets, so the Register counts {2 × connections} [236] where our atlas holds {connections} [118]."
- **failure_alt:** "The index’s whole-atlas row reading 236 connections, with Connection L14 listed on two sheets."

#### 21.10

- **title:** Keep the rejected option and the connections left off the map on their sheets.
- **rule:** "Where our atlas rejects a reform, keep it on the sheets its targets file on, under the heading Rejected option, with its grade read as the atlas reads it: for a rejected option, a strong grade measures confidence in harm. Where the atlas reviewed a connection and left it off the map, list it on its sheet under Reviewed and not drawn, with its two variables and the atlas’s reason, and draw no line."
- **why:** "What the atlas decided against is evidence too, and a reader who meets a popular idea there sees the finding behind the decision."
- **basis:** "Rules 15.10 and 15.12; the atlas’s rejected reform and the connections it reviewed and left off its map"
- **specs:**
  - Heading: "Rejected option, then the reform’s chip and title as stored"
  - Grade: "The atlas’s words on what the grade measures, quoted under the grade word"
  - Reviewed and not drawn: "Rule 15.10’s form: from and to with chips, the reason quoted, and no line in any pattern"
  - Counts: "A rejected reform stays out of the index’s reforms column"
- **builders:** "Read the rejected flag and the reviewed connections from the model, and file each on its targets’ sheets."
- **correct_caption:** "Two blocks at 390 px in the light theme: the sheet for Domain D04 with its rejected option, Reform R-35, its effects and the atlas’s words on its grade; and the sheet for Domain D10 with its {n in words} [two] connections reviewed and not drawn, each with the atlas’s reason."
- **correct_alt:** "Two blocks. The first, headed Rejected option, holds Reform R-35, “{stored title}”, its effects on the quality of democracy, {code} [−S], and on government efficacy, {code} [−M], and the remedy’s grade, Well supported, with the atlas’s words: “Here the grade measures confidence in a finding of harm.” The second, headed Reviewed and not drawn, lists two connections into Variable B4, one from Variable TC1 and one from Variable X4, each with the atlas’s reason and no line."
- **failure_caption:** "<strong>Fails Rule 21.10.</strong> Term limits read as a well supported remedy, though our atlas rejects them on strong evidence of harm."
- **failure_alt:** "Sheet D04’s reforms with Reform R-35 among them, unlabeled, its remedy graded Well supported."

#### 21.11

- **title:** Filter a sheet’s issue records by variable, and say how many show.
- **rule:** "Under each sheet’s connections, list its issue records with their grades. An issue record is one of the atlas’s files on a documented problem, case or policy. Let a reader narrow the list to the records that name one of the sheet’s variables, with one Filters button that says how many filters are on, and a line that says how many records show out of how many."
- **why:** "A sheet can hold twenty or more records, and a reader who cares about one variable finds its records without reading all of them."
- **basis:** "Rules 18.15 and 18.16; the variables each issue record names in the atlas"
- **specs:**
  - Control: "Rule 18.16’s Filters button, such as “Filters, 1 on”, with one check box for each variable, each with its chip and its count of records"
  - Count line: "A status line after each change, never on load, such as “9 of 20 issue records.” (Rule 18.15)"
  - Each record: "Chip, title as stored, grade word"
  - Records that name no variable on the sheet: "Shown only with every filter off"
- **builders:** "Build the filters from the variables on the sheet, and count each from the records’ own lists of variables."
- **correct_caption:** "The sheet for Domain D04 with its issue records narrowed to Variable D4, {filter-showing} [9] of {filter-of} [20] showing, at 390 px in the light and the dark theme."
- **correct_alt:** "Two phone frames, light and dark. A Filters button reading Filters, 1 on, open above three check boxes, Variable D4 checked; the line 9 of 20 issue records; and nine records, each with its chip, its title and its grade word."
- **failure_caption:** "<strong>Fails Rule 21.11.</strong> Color alone shows which filter is on, nothing says how many records are hidden, and the grades are gone."
- **failure_alt:** "Three colored tabs over a list of record titles, one tab filled, with no count and no grade words."

#### 21.12

- **title:** Head a loop page with its grade line and the arithmetic of its signs.
- **rule:**
  1. "Open a loop page with the loop’s chip, its kind and its title from our atlas in quotation marks. Under the title, give the grade of each step in the atlas’s words and the loop’s own grade, which is the grade of its weakest step."
  2. "Then read the loop aloud in one sentence that starts with a rise in its first variable and turns at each minus sign, and say beside it how the count of minus signs sets the kind: an even count makes a loop that feeds itself, and an odd count one that pushes back. On the drawing, name the weakest step and say that the loop holds only as firmly as that step."
- **why:** "The arithmetic lets a reader check the loop’s kind from its signs, and naming the weakest step keeps the loop’s title from claiming more than its least certain step."
- **basis:** "Rules 15.6, 15.7, 15.13 and 18.22; Loop R18’s record and evidence summary in the atlas"
- **specs:**
  - Head: "Chip, kind word and the title in quotation marks as the page’s main heading; under it the grade line, with chips (Rule 18.22, house rule H08)"
  - Read aloud: "One sentence from the signs, a rise to start and a turn at each minus; beside it the count of minus signs and the kind"
  - Weakest step: "“Weakest step” under its words, where the atlas’s evidence summary names it (Rule 15.13), with the line “The loop holds only as firmly as this step.”"
  - Closure and delay: "In the atlas’s words (Rule 15.7), the delay as ticks and words"
- **builders:** "Build the read-aloud line from the signs, and stop the build when the loop’s kind and its count of minus signs disagree."
- **correct_caption:** "Loop R18’s page, “{stored title}”, at 1440 and 390 px in the light and the dark theme, with Reform R-11 chosen."
- **correct_alt:** "Four frames of Loop R18’s page. Its chip, the words Reinforcing loop and its title in quotation marks, then its grade line: plausible, the grade of its weaker step. A sentence reads the loop from its signs, with the line beside it that two minus signs make it reinforcing. The drawing joins Variable D2 and Variable D4 by Connection L14, solid, and Connection L15, dashed and marked Weakest step, with Reform R-11’s targets in red. The stepper and the reform chooser follow, then the loop in the atlas’s words."
- **failure_caption:** "<strong>Fails Rule 21.12.</strong> The head grades Loop R18 documented, the grade of its first step. Our atlas grades the return step plausible, and the loop holds only as firmly as that step."
- **failure_alt:** "Loop R18’s head with the word Documented under its title, no sentence read from its signs, and no step marked weakest."

#### 21.13

- **title:** Run the atlas’s stepper in the guide’s order and at the guide’s pace.
- **rule:** "Every loop page steps through its loop with the loop stepper of Rule 18.22, the buttons that walk a reader through a loop one step at a time: Play, Reset the loop, Previous step and Next step, in that order, on every screen. Play holds each step 250 ms for every word its status line reads, “Step 1 of 2:” included, and never less than six seconds, with reduced motion too. Nothing plays until a reader presses Play."
- **why:** "A reader who learns the stepper anywhere in our work finds the same buttons in the same order here, and the pace lets a reader, or a screen reader, finish each step before the next."
- **basis:** "Rules 15.19 and 18.22; WCAG 2.2 SC 2.2.2 and 3.2.4"
- **specs:**
  - Order and names: "Play, Reset the loop, Previous step, Next step (Rule 18.22)"
  - Phones: "A two-by-two grid in reading order: Play and Reset the loop, then Previous step and Next step"
  - Step words: "The variables’ titles and the sign’s verb, then the connection, its grade and its delay (Rule 15.19)"
  - Hold: "250 ms a word of everything the status line reads, its step count included, never under 6,000 ms, with reduced motion too; Loop R18’s two steps hold {hold 1} [9,250] and {hold 2} [16,000] ms"
  - Code: "Chapter 18’s loop stepper, read from its files, each step’s hold counted by script from its words"
- **builders:** "Read the stepper from chapter 18’s files, and time each hold from its status line’s words."
- **correct_caption:** "Loop R18’s stepper on step 2 with its status line, at 390 px in the light theme with its buttons two by two, and at 1440 px in the dark theme with its buttons in one row."
- **correct_alt:** "Two steppers on step 2, each with the status line “Step 2 of 2: The ability to investigate and enforce the rules can lower presidential action without new legislation,” and the rest of the step’s words. At 390 px the buttons Play, Reset the loop, Previous step and Next step sit two by two; at 1440 px they sit in one row."
- **failure_caption:** "<strong>Fails Rule 21.13.</strong> The buttons run in another order than the rest of our work, and each step moves on after about three seconds, before a reader can finish it."
- **failure_alt:** "A stepper with the buttons Play, Previous step, Next step and Reset in one row, and beside it the words 3,200 ms a step."

#### 21.14

- **title:** List every loop on one index, by kind, closure and grade.
- **rule:** "Give the atlas one index of its loops, the reinforcing ones first and then the balancing ones, each group in the order the atlas lists it. Each row gives the loop’s chip, its title, its number of steps, its count of minus signs, how it closes and its grade, the last two in the atlas’s words. Print each title as the atlas stores it, and leave out any score or rank of strength."
- **why:** "A reader can find a loop by its kind and see at a glance which loops rest on a hypothesis or close only in concept."
- **basis:** "Rules 15.6, 15.7, 15.18 and 15.21; the atlas’s loop records; every loop title printed as the atlas stores it, approved by our founder and editor on November 22, 2026"
- **specs:**
  - Groups: "Reinforcing, then Balancing, each with its count"
  - Row: "Chip, title as stored, steps, minus signs, closure and grade as stored, each row a link to the loop’s page"
  - Conceptual loops: "“No numbered chain” with their grade (Rule 15.18)"
  - Note: "One line under the index: the titles print as stored, and the atlas’s next version reviews those that state an effect"
  - Never: "A strength, a score or a size for a loop (Rule 15.21)"
- **builders:** "Read every row from the loop’s own record, in the atlas’s order."
- **correct_caption:** "The index of all {loops} [23] loops, {n} [18] reinforcing and {n} [5] balancing, at 1440 and 390 px in the light theme, with its note on the titles."
- **correct_alt:** "Two frames of a table of loops in two groups, reinforcing then balancing. Each row gives a loop’s chip, its title, its steps, its minus signs, how it closes and its grade; the three conceptual loops, two balancing and one reinforcing, read No numbered chain. Under the table, one line says the titles print as the atlas stores them and the atlas’s next version reviews those that state an effect, among them the titles of Loop R5 and Loop R11." (the three conceptual loops today: Loops B2, B3 and R9)
- **failure_caption:** "<strong>Fails Rule 21.14.</strong> A bar ranks each loop by a strength our atlas does not measure."
- **failure_alt:** "A list of loops, each with a bar of a different length beside it, sorted longest first."

#### 21.15

- **title:** Draw the atlas’s dark theme from the Charcoal tokens, and measure every mark.
- **rule:** "In the dark theme, every atlas page draws on Charcoal from the tokens set for Charcoal: text in Newsprint, quieter words and muted marks in Dim Newsprint, the selected bar in Newsprint and the red target in Pillar Red. Line patterns, sign tags, ticks and chips keep their shapes. Measure every mark on the page’s own pixels before it ships."
- **why:** "A reader who sets a device to dark reads the same atlas with the same marks, and every mark keeps the contrast it needs on Charcoal."
- **basis:** "One dark theme for every screen product, with a visible switch that remembers the reader’s choice, approved by our founder and editor on November 10, 2026; Rules 05.2, 05.5 and 17.10; ratios measured on each frame’s pixels"
- **specs:**
  - Ground: "Charcoal"
  - Text: "Newsprint, {measured} [13.29] to 1; quieter words in Dim Newsprint, {measured} [7.26] to 1"
  - Marks: "The essential graphic ink for Charcoal; muted marks in the muted mark color for Charcoal, never Stone"
  - Selected bar: "Newsprint, never White"
  - Red target: "Pillar Red, {measured} [4.49] to 1, with no edge; the 1 px Charcoal edge is for Newsprint (Rule 05.5)"
  - Hairlines that carry no meaning: "Stone, {measured} [3.10] to 1 (Rule 05.5)"
  - Colors: "Every color from a token, never a hex in the page’s code"
  - Switch: "The site’s (Rule 18.4), remembered across a reload"
- **builders:** "Name a token for every color in a dark view, and check each frame’s pixels with the contrast script."
- **correct_caption:** "Loop R18’s drawing with Reform R-11’s targets in red and the chooser beside it, at 1440 px in the dark theme, with the ratios measured on the plate’s pixels."
- **correct_alt:** "On Charcoal, Variable D2 and Variable D4 joined by two connections, Variable D4’s outline and both connections in red for Reform R-11, with the chooser beside them and a table of four measured ratios: text, quieter words and muted marks, the red target, and a plain hairline."
- **failure_caption:** "<strong>Fails Rule 21.15.</strong> Muted marks in Stone clear 3 to 1 by a tenth, and the selection draws in White, a color no token sets on Charcoal."
- **failure_alt:** "Loop R18’s drawing on Charcoal with its muted steps in gray and the chosen reform’s row marked in white."

#### 21.16

- **title:** Test every atlas page against the model before it ships.
- **rule:** "Before any atlas page ships, run the atlas test. It reads the page together with the model, the atlas’s data, and checks every ID, sign, type, delay, grade, count and date the page prints against the model. It checks every red mark against the chosen reform’s targets, every effect against its family, every link from a claim to its evidence, and the stepper’s order and pace. A single failure stops the page."
- **why:** "The atlas changes as its evidence changes, and a page that copies a value can drift from the record without anyone seeing. The test reads the record on every build."
- **basis:** "The atlas test this chapter carries for chapter 28’s standards checklist; chapter 15’s checks of its drawings, extended to pages"
- **specs:**
  - Checks: "Sixteen, each printed as one line a page: typed IDs, connection marks, counts, loops, authority, red, effects, routes and dates, evidence a step away, grade words, the stepper, pressed and lit parts, colors, type, the site’s frame and retired words"
  - Output: "PASS or FAIL, with the page, the frame, the record, the value printed and the model’s value"
  - Stop: "Any FAIL stops the application kit’s build and the guide’s strict build"
  - Self-test: "One planted fault for each check in a copy of a page, never in the model; it passes only when each plant is caught and the clean pages stay quiet"
- **builders:** "Run the atlas test on every build, and treat a failure as a stop."
- **correct_caption:** "The atlas test’s report for the {n in words} [six] atlas pages, one line a check, from the build that drew these plates."
- **correct_alt:** "A list of test lines, each reading PASS with a check’s number, the page and what it read." (the engineer's report sets the final words; I will match them)
- **failure_caption:** "<strong>Fails Rule 21.16.</strong> The page grades Connection L15 documented. Our atlas grades it plausible, and the test stops the page."
- **failure_alt:** "Loop R18’s second step labeled Documented, beside the test’s line: FAIL, the loop page, Connection L15, printed documented, model plausible."

### 7. The extra after Rule 21.14: How to read

- **label:** How to read
- **caption:** "Our atlas’s How to read page, which lists every mark its pages use with its meaning and the rule that sets it, at 1440 px in the light theme and 390 px in the dark theme."
- **alt:** "Two frames of a page of marks, one row a mark: the sign tags with raises and lowers, the type words, the open diamond for authority, the five grade lines with their glosses, the record square, the delay ticks, the hollow line, the red target, the typed chip and the pressed question, each with its words and its rule."

### 8. For the chapter 28 checklist (plan section 8's twelve lines), drafted for later

1. Every atlas ID sits in a typed chip whose kind matches the model.
2. Every sign, type, delay and grade beside a connection matches the model.
3. Every count on an atlas page matches the model.
4. Each loop’s kind matches its count of minus signs, and its weakest step is named.
5. No authority connection carries a sign or sits in a loop.
6. Red marks only the chosen reform’s own targets, once in a view.
7. A reform’s four effects print apart and whole, with no total.
8. Every route prints its check date or “Not checked”, and every status its date.
9. Every figure, step and reform reaches its evidence in one step.
10. The loop stepper runs Play, Reset the loop, Previous step and Next step, at 250 ms a word and never under six seconds.
11. Every dark view takes its colors from the Charcoal tokens and passes 4.5 to 1 for text and 3 to 1 for marks.
12. Every atlas page sits under the site’s masthead, with the atlas’s title bar and a page title in three parts.

## Done

Each time below is a `date -u` value read in the same command.

### A done (DR-323, DR-324, DR-325), 21:51 UTC

1. **DR-323**, Rule 13.12's rule text, second paragraph: `work/build/scripts/phase-3/phase3_ch13_build.py` (the block at line 1716), comment `# DR-323 (ED11B-1)`. Run under the lock 21:50:03 UTC; its own checks passed and it wrote `13-evidence.json`, its 27 specimens and manifest, of which only `13-evidence.json` changed.
   - Original: "An Act piece quotes each side at the same length (Rule 01.22), and an invented quote carries the Illustrative label beside it (Rule 13.8)."
   - Revision: "An Act piece sets out what the record shows from each side, at the length the record holds (Rule 01.22), and an invented quote carries the Illustrative label beside it (Rule 13.8)."
   - `phase3_ch14_build.py --check` under the lock, 21:50:07 UTC: "99 of 99 files current", exit 0.
2. **DR-324**, Rule 03.6: `work/build/scripts/phase-2/stage_a_identity_chapters.py`, comment `# DR-324 (ED11B-2)` above the rule text and above the row.
   - Rule text, original: "Under 48em, it sets L1 from the 24 px master beside the menu button."
   - Rule text, revision: "Under 48em, it sets L1 from the 24 px master beside the menu button, and under 24.375em, 390 px, from the 16 px master."
   - Row label, original: "Site, under 48em"; revision: "Site, from 24.375em to 48em". Its value and token stay.
3. **DR-325**, Rule 03.6's `files=`: `A + "wordmark/20261028_Wordmark-16px-Master.svg"` after the 24 px master, comment `# DR-325 (ED11B-3)`. The file exists at `work/build/assets/identity/wordmark/20261028_Wordmark-16px-Master.svg`.
4. **The identity chain's side effects (C11B-1, D4-222).** Copied the five files to scratch `before-identity-run/` with their SHA-256 (21:49:26 UTC), ran `stage_a_identity_build.py` under the lock (21:50:26 to 21:50:37 UTC, exit 0: 73 specimens, chapters 03, 04, 08 and 09), and the run rewrote all five. I put back all five from my copies (21:50:44 UTC): `s-04-1-correct`, `s-09-3-correct`, `s-09-3-failure`, `s-17-hinge-failure` and `20261110_Letterhead-Proof.html`. Each now equals HEAD. Chapters 04, 08 and 09, every other specimen and `manifest-identity.json` kept their bytes.
5. **Proof.**
   - Strict build after, under the lock (21:50:52 to 21:51:03 UTC): exit 0, 0 warnings, 0 stale plates, 13,084,029 bytes, 393 rules, 731 specimens. The before build (21:49:31 to 21:49:42 UTC, same tree less my four files) gave exit 0, 0 warnings, 13,083,858 bytes, the opening figure.
   - Word search of the built HTML (tags and `<wbr>` stripped, no-break spaces read as spaces), before → after: Rule 13.12's new phrase 0 → 1, in Rule 13.12 only; "An Act piece quotes each side at the same length" 1 → 0 on the page. Rule 03.6's new sentence 0 → 1, in Rule 03.6 only; the old sentence 1 → 0. "Site, from 24.375em to 48em" 0 → 1, in Rule 03.6; "Site, under 48em" 1 → 0 on the page. `20261028_Wordmark-16px-Master.svg` 4 → 5, the new one in Rule 03.6's file list (the others sit in Rules 03.1, 03.8, 05.3 and 05.7, as before).
   - A line diff of the two pages shows these four places and the build-time line, nothing else.
   - `git diff --stat` after the restore: `03-identity.json` (5), `13-evidence.json` (2), `stage_a_identity_chapters.py` (10), `phase3_ch13_build.py` (5); four files, 14 insertions, 8 deletions. Nothing else in the tree moved.

| Chapter | JSON file before | after | Section of the built page before | after |
|---|---|---|---|---|
| 03 Identity | 27,118 | 27,259 (+141) | 463,108 | 463,237 (+129) |
| 13 Evidence | 45,531 | 45,573 (+42) | 243,027 | 243,069 (+42) |

The page grew 171 bytes, 13,083,858 to 13,084,029, all of it in chapters 03 and 13 (the build report's per-chapter figures; no other chapter moved).

### B drafted, waiting on the hand-over (22:07:39 UTC)

Every word chapter 21 needs from me is drafted under "Words for": the chapter's fields; the words every atlas page shares; the six page titles, current views and breadcrumbs; each view's words, aligned with the design director's specs for the shell, the loop page and the reform page; the stepper's status lines with their counts and holds (step 1, 37 words, 9,250 ms; step 2, 64 words, 16,000 ms); ED-F6's two lines; ED-F4's weakest-step line; DR-321's note; Rules 21.1 to 21.16 in full; the How to read extra; and the twelve checklist lines for chapter 28. Nothing is written into `phase4_ch21_build.py`, which does not exist yet; the design director's notes say "Words for the editor: Not yet". When the word fields are handed over by name, I type these words into them, run the generator under the lock, then the strict build, and re-count the holds from the words as typed.

### B typed into the generator (22:38:56 UTC)

The design director handed the word fields over at 22:09 UTC and answered my requests 3 to 5 (DD-11C-1 to DD-11C-3, read before typing). Under the lock (22:37:26 UTC) a script typed my words into `W`, `ATLAS['locator_alt']`, `PAGES`, `R` and `EXTRA_HOW` of `work/build/scripts/phase-4/phase4_ch21_build.py` and nothing else; `PARTS`, the rest of `ATLAS`, `_holds()` and every line outside the word fields are byte for byte as the design director left them (checked by script against my copy taken at 22:34:39, scratch `phase4_ch21_build.before-editor.py`), and no key the old fields held was dropped.

- **`--check`** under the lock (22:37:49 UTC): exit 0; "chapter 21: 16 rules, 17 specimens (61,487 bytes before the kit’s frames); model ef1028ac87e402e3", with the plates that wait for the kit listed as waiting. Chapter 02's mechanical checks ran on every field.
- **`--page-words all`** under the lock: exit 0, A11 to A16. Titles: "Atlas home | Who Do They Answer To? | Oath & Action", "Reform R-23 | …", "The Register | …", "Loop R18 | …", "Loops | …", "How to read | …".
- **Holds**, computed by `_holds()` from my lines: step 1, 9,250 ms; step 2, 16,000 ms. My count of the same lines: 37 and 64 words, 9,250 and 16,000 ms. They match.
- **The home intro** reaches the kit with `{variables}`, `{connections}`, `{loops}`, `{reforms}` and `{issues}` unfilled, as DD-11C-6 sets, and types no count.
- **Keys added** (each listed under Requests, since the kit must read them): A11 `key_counts`; A13 `rejected_section`; A14 `also_aim_one`; A16 `groups` and `marks`.
- **Where the typed words differ from the drafts above:** the tab titles; the captions and alts (no stored question text, no typed counts); the loop page's grade line keeps the kit's per-step form "{grade} for {from} to {to}", joined by the kit, since the field holds no wrapper; the read-aloud line goes in the kit's templates ("Start with {var} rising." / "Along {conn}, which {sign}, {var} {dir}." / "The loop comes back moving the same way it started."); the parity line reads "An even count of minus signs, {n} here, makes the loop reinforcing, so it feeds itself."; the ready line names no variable ("Ready. Press Play to step through the loop, or Next step to follow one connection at a time."); How to read carries meanings only (DD-11C-2); Rule 21.5's words describe the tags as a list beside the drawing (DD-11C-6 (3c)); Rule 21.10's heading row follows DD-11C-1.

### Keys the kit asked for, and the kit's build (23:05:52 UTC)

On the coordinator's message (the kit's first build of A11 to A20 failed 27 T16 lines, each a word key the generator lacked), I added under the lock (23:03:56 UTC), in the word fields only: A11 `claim_summary` ("in full", after the claim's chip) and `claim_labels` (Grade, People, Place, Period, Limit, Sources); A13 `problem` and `remedy` (Rule 15.12's labels), `to`, `reviewed_word` ("reviewed connection {id}", R11), `filters_clear` ("Clear filters"), `records_noun` ("issue records") and `records_none` ("No issue record matches. Turn a filter off, or clear the filters, to see more.", chapter 18's form); A12 `aims_here_one` ("also aims here"); `ATLAS['types']`, Rule 15.4's words by the model's type. A13's `showing` drops its final period, so the line on load matches what chapter 18's script writes after a change. The tab titles take the kit's `{title}` fill: A12 "Reform R-23, {title}" and A14 "Loop R18, “{title}”", in quotation marks as Rule 18.22 names a loop (this answers Request 10 (b)).

- `--check` exit 0 (34 specimens, 88,194 bytes before the kit's frames); `--page-words all` exit 0; holds still 9,250 and 16,000 ms.
- `node work/build/app-kit/oa-app.mjs build A11 … A20 --date 20261122` under the lock (23:04:01 to 23:05:39 UTC, load 0.21): exit 0, 67 exports; **atlas test 1,264 PASS, 0 FAIL, self-test PASS** (`plates/atlas-test.json`, ran 23:05:39 UTC). No `⟦` left in the six working pages. The exports' titles read "Reform R-23, Minimum wage that rises with an index | Who Do They Answer To? | Oath & Action" and "Loop R18, “Weakening watchdogs lowers the cost of further unilateral action” | …".

### Band ledes and Rule 21.16's table words (23:11:47 UTC)

On the design director's DD11C-Q5 and Q8 (and Q4's title bar row), under the lock (23:11:37 UTC), word fields only:
- Seven ledes for specs 14.1's section bands, each a line that tells a reader what the section holds or how to use it: A11 `questions_lede` "Press a question to see which parts of the system decide it."; A12 `grades_lede` "Our atlas grades the evidence that the problem exists and the evidence that the remedy works, each on its own." (the draft's "apart from" can read as "except"); A13 `rejected_lede` "The atlas keeps what it rejected on the sheet, with the evidence behind each decision." and `records_lede` "Each issue record names the variables it touches. Narrow the list to the records for one of them." ("variables", the page's term, for the draft's "conditions"); A14 `record_lede` "Its summary, a case on the record, what it depends on and how it adapts, each as the atlas stores it." (the draft repeated the heading); A15 `reinforcing_lede` and `balancing_lede`, each "Each of these loops feeds itself [pushes back on a change]; where its steps are numbered, an even [odd] count of minus signs shows it.", since the three conceptual loops in the groups have no numbered steps to count.
- Rule 21.16's caption and alt describe the plate as it now draws: a live-text table, each check against the four views, each cell PASS or FAIL with how many frames and pages the check read. The alt calls it a readable table and names the four column heads.
- Rule 21.1's Title bar row adds "on the atlas home, the head band below joins it" (Q4).
- `whole_issues` stays "{n}, one retired": the generator now fills `{retired}` for its failure plate, but the kit's line 360 still fills `{n}` alone, so the page would print the brace until the engineer adds it.
- `--check` exit 0 (34 specimens, 87,007 bytes before the kit's frames; `s-21-16-correct` 4,889 bytes); `--page-words all` exit 0, all seven ledes present, holds 9,250 and 16,000 ms. The kit was not rebuilt by me after these words.

### The data lead's batch 1, my items (23:22:45 UTC)

Under the lock (23:22:29 UTC), word fields only; `--check` exit 0 (34 specimens, 87,068 bytes before the kit's frames), `--page-words all` exit 0, holds 9,250 and 16,000 ms. I did not rebuild the kit.
- **5:** A11 `variables` reads "{n} variables," and `inside_none` "no connections inside", so a box's one line reads "6 variables, 6 connections inside" (the kit prints the two keys side by side; two lines would be the engineer's).
- **7:** A11's key phrases take their stops: "The main circuit, part to part." "Other flows." "Each number counts connections."
- **8:** new A12 key `conn_note`: "{conn} “{name}” joins them: {sign}, {delay}, {grade}. It stays in ink, since the reform does not act on it." For LE15: "Connection LE15 “Higher income strengthens household security” joins them: raises, under 2 years, Documented. …", the record square before Documented, the chip linked to `#register-le15`.
- **10:** new `ATLAS['feasibility']`: high, medium, low and very low as "High feasibility", "Medium feasibility", "Low feasibility", "Very low feasibility" (Rule 15.16's form).
- **16:** new A13 key `rejected_targets`: "It would act on {targets}." ({targets} the linked chips of Connections L18 and L19, joined with "and"); the "As of" over its effects uses the existing `ATLAS['as_of']`.
- **18:** new A14 keys `chosen_note` "{reform} acts where the marks turn red: on {targets}.", `chosen_off` "Its other targets, {off}, sit off this drawing." (Reform R-15's L16) and `chosen_none` "{reform} acts on {off}, none of which sits on this drawing, so nothing turns red." (Rule 15.20), each changing with the chooser.
- **22:** A15 `no_chain` reads "None"; Rule 21.14's specification row now says "None" in the two cells and lets the stored closure ("conceptual: no complete numbered chain") say why.

**For the engineer, keys the kit must read** (item numbers from the data lead's batch 1): `ATLAS['feasibility']` in `route_rows` in place of the bare stored word (10); A12 `conn_note` beside the reform drawing for each drawn connection that is not a target (8); A13 `rejected_targets` in the rejected option's block, with `ATLAS['as_of']` over its effects (16); A14 `chosen_note`, `chosen_off` and `chosen_none` beside the loop drawing, filled for the chosen reform and redrawn with the chooser (18).

## Requests

Status at 22:38:56 UTC (`date -u`): the word fields were handed over at 22:09 UTC and my words are typed (Done, "B typed"). Items 3 to 5 below are answered by the design director's DD-11C-1 to DD-11C-3; item 6 is the data lead's to rule as R15.

1. **Done:** the design director handed the word fields over by name at 22:09 UTC.
2. **Answered by the design director's specs 9.1 (`remedy_split: 4`):** R-23's stored remedy text prints whole in two blocks, split at the sentence that opens "Main limitation". My Rule 21.4 words ("set the readings its record holds side by side, in the atlas’s own words") fit that split, and they no longer say "at the same length", which only an edit of the stored text could guarantee (DR-37, DR-93); the specs' own check holds the blocks within one line of each other at 1440 px (T10).
3. **To the design director, Reform R-35's heading:** its stored title is "Rejected option: term limits for legislators", so the block heading "Rejected option" (plan Rule 21.10) prints the words twice in a row. Either the heading stays and the title prints as stored beneath it, or the block takes the title alone as its heading. Your call as the layout's owner; Rule 21.10's words fit either.
4. **To the design director, How to read (plan 3.8):** the plan prints the rule in our brand guide that sets each mark on a public page. I drafted the intro to say so ("Its row names the rule in our brand guide that sets it"); if the page should carry the marks' meanings alone, I drop that sentence and the rule column's head.
5. **To the design director, Outside forces:** DR-35 gives seven parts a question and Outside forces none; my words print its name and the model's title alone.
6. **To the data visualization lead, T10's length condition (plan section 8):** T10 passes a contested remedy when its two readings sit "within a line's length of each other". Both readings are the atlas's stored words, split at `remedy_split`, so a later remedy whose record runs longer on one side would fail a page that prints the record faithfully. Suggest the condition read: the stored text prints whole, in order, split at one sentence, with both blocks side by side (H08's "both readings"), and the lengths printed in the test's line for the record. R-23 today passes either way (about 42 and 38 words).
7. **To the engineer, keys the kit must read** (added to the word fields under the lock, 22:37 UTC): A11 `key_counts`, "Each number counts connections" (the specs' 12.1 key line); A13 `rejected_section`, the h2 "What our atlas decided against" (specs 10.1); A14 `also_aim_one`, "{chips} also aims here", for a step or target with one other reform (choose it when one chip fills `{chips}`; `also_aim` stays the form for two or more); the reform page's `aims_here` now reads "also aim here", which needs the same choice ("also aims here" for one); A16 `groups` and `marks`, the How to read page's five group heads and each mark's name and meaning, keyed by the stored grade spellings and delay codes where they match.
8. **To the engineer, the read-aloud line:** the kit today joins chips and sign words with commas (`v.reads`); the templates `read_start`, `read_step`, `read_end_same`, `read_end_other` and `dirs` hold the words (DD-11C-6 (2)). The line they make for Loop R18: "Start with Variable D2 Presidential action without new legislation rising. Along Connection L14, which lowers, Variable D4 Ability to investigate and enforce the rules falls. Along Connection L15, which lowers, Variable D2 Presidential action without new legislation rises. The loop comes back moving the same way it started." If the kit prints each title after its chip in lower case mid-sentence, the line reads more smoothly; your call.
9. **To the engineer, numbers in prose:** `parity_even` and `parity_odd` print `{n}` inside a sentence, and house rule H06 spells out one to nine in prose. A fill in words for `{n}` there ("two"), with `data-count` still the figure, keeps the rule; T3 already accepts number words.
10. **To the design director, fills that would keep words from going stale:** (a) `{retired}` in `whole_issues`, filled from `FACT['retired']` in the Rule 21.9 failure plate's `format()` and by the kit; (b) a `{title}` fill in A12's and A14's `view`, from the record the content file names, if the tab should carry the record's title (A12 "Reform R-23, {title}", A14 "Loop R18, “{title}”"); (c) a check in the generator that each stepper line holds its connection's ID, stored name, grade word and delay words and both variables' titles, as chapter 20's generator checks its facts, since the lines quote stored names the model could change.
11. **To the engineer, How to read's sign rows:** Rule 15.3 asks every key that shows a sign to quote the atlas's sentence "A positive sign does not mean a benefit."; it is stored text, so the kit quotes it from the model under the two sign rows; my `marks` give the meanings only.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

- Strict build before and after, under the lock, with the figures under "A done".
- `phase3_ch14_build.py --check`, 99 of 99.
- Word search of both built pages for the old and new phrases, by rule block (scratch `wordsearch.py`).
- A line diff of the two built pages (split at each `>`).
- `git diff --stat` and `git status --short` after the restore; each of the five restored files against HEAD with `git diff --quiet`, and my scratch copies against their SHA-256.
- A search of the after page for "same length", "under 48em" and the 24 px master near "phone", "390" or "menu": no other rule says an Act piece quotes each side at the same length, and Rule 20.1's "under 48em the bar sets L1" names no master, so nothing else contradicts the new words.
- Script check of the three new texts and this file for em dashes and the listed words (genuinely, really, truly, actually, leverage, underscore, reflect, very, just, simply): 0.
- The stepper's holds by script (scratch `holds.py`), building each status line as chapter 18's `c-18-loop-stepper.js` does ("Step i of n: " + line + " " + more, whitespace collapsed) and timing it at 250 ms a word, never under 6,000 ms: Loop R18's lines give 37 words, 9,250 ms and 64 words, 16,000 ms. The same script on chapter 15's built `s-15-19-correct` gives its 9,750, 12,750 and 15,250 ms exactly.
- Model fields behind the drafts, read by script from `work/extract/atlas-v7-data.json` (SHA-256 beginning ef1028ac87e402e3): `meta`, the 23 loops' titles, types, closures and grades, Loop R18's record, Reform R-23's and Reform R-35's records, Domain D04, Variables D1, D2, D4, D5 and EC7, the reviewed connections, the band definitions, the routes and the glossary entries quoted or followed.
- Script check of the drafted words (scratch `words-for.md`) for em dashes, en dashes and the listed words: 0 em dashes, 0 en dashes; "leverage" once, in the model field name `leverage.bands`, which no reader sees. Every "not" read by hand: Rule 15.10's heading "Reviewed and not drawn", the atlas's quoted sentence, conditions ("where the words around it do not say it") and plain facts; no corrective negation.
- `phase4_ch21_build.py --check` under the lock after typing: first run (22:37:33 UTC) stopped on my `{retired}` fill (KeyError in the Rule 21.9 failure plate); after restoring "{n}, one retired", exit 0 (22:37:49 UTC). `--page-words all`: exit 0 both times.
- The holds `_holds()` computes against my own count: 9,250 and 16,000 ms both ways.
- The generator outside its word fields, `PARTS`, `_holds()` and `ATLAS` but `locator_alt`: byte for byte as before my edit (script against my copy from 22:34:39 UTC).
- A scan of the word fields' strings (comments left out) for "dark mode", studio names (Concept, System 1), decision and ruling codes (DR-, AL-, ED-F, D4-, D2-), "data lead", "accessibility lead", em and en dashes and the listed words: 0 in reader text (two AL- codes sit in code comments).

## Not tested

- The guide check, which the main session runs at the close.
- Whether the five rewritten side-effect files differ in pixels from their originals; I put the originals back, so nothing new ships.
- Chapter 21's words on drawn pages: the kit has not drawn A11 to A20 with them, so no plate, page title, status line or hold of mine has been checked by the atlas test or read in a browser, and the generator has not written `21-atlas.json` (it waits for the kit's plates). The strict build was not run for B, since chapter 21 is not yet written.
- The words' widths: only the views button's ("Views", 44.3 px) comes from a measure, the design director's.
- My read of the drafts for rhetorical triplets, parallel runs, landing lines and setup and payoff is a read by hand; no script can rule them out. The read-aloud line repeats one clause shape for each step by design, as chapter 15's read-aloud line does.
