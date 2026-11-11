# Stage C round 2: red team on brand, evidence and nonpartisanship

Oath & Action Edition 06, Phase 2, stage C, round 2, November 11, 2026. Reviewer: brand, evidence and nonpartisanship, in the research lead's role (`.claude/agents/oa-research-lead.md`) with the creative director's brand knowledge. Page reviewed: the frozen copy at the scratchpad's `round-2/review/guide.html` (SHA-256 starts ba1e1f97ee988b1e, as D2-1531 records), built from commit df0fb08d. `git diff df0fb08d HEAD` touches only the round 2 brief, the decision log and the open questions, so the chapter JSON, specimen and code files in `work/build/guide/` are the page's words. Paths are relative to `oath-and-action-v6-brand-guide/`. My scratch files, scripts and screenshots are in the scratchpad's `round-2/brand-evidence/`.

Status: complete.

## 1. Score

**3 of 5.** The record work is strong and exact: all 55 criteria carry W3C's numbers, names and levels, every chapter 18 browser line matches MDN's data 8.1.8, 264 contrast ratios and 30 derived colors recompute to the figure printed, every source I could fetch is real, and the identity players land pixel for pixel on their masters; but the dark theme puts Pillar Red on Prussian in every form with an error, four criteria are not quoted in W3C's order (3.3.7 now says something else), Loop R1 is titled as a finding where the atlas grades it plausible, and chapter 18's atlas samples come back to the editor's own campaign subject, which the studio has taken out twice before.

## 2. Must fix

### M1. Chapter 18, Rule 18.17, `c-18-form` in the dark theme: Pillar Red sits on Prussian in every form field with an error

- **Where:** the live stage `c-18-form--dark`, and every product form a builder copies from `c-18-form.css` (line 19) under the dark theme. The cause sits in the tokens: `--oa-color-field-ground-on-charcoal` resolves to Prussian (#1F2D5A, `work/build/tokens/tokens.css` line 111), while the error mark on Charcoal stays Pillar Red.
- **What is wrong:** I pressed Remind me with both fields empty in the dark stage. Each field takes `aria-invalid="true"`, a Prussian ground (rgb 31, 45, 90) and a 4 px Pillar Red left border (rgb 230, 57, 70): a red bar on the edge of a navy box, twice in one card (screenshot `form-dark-error.png` in my scratch folder). Rule 05.3 says "Red never sits on Prussian", and its reason gives the brand cause: "where it measures 3.19 to 1 and reads as a party pair of red and blue." The token table's own description of Prussian says "Red never sits on it.", and the token architecture's table gives working red on Prussian as "None: red never sits on Prussian". D2-1469 kept the bar on contrast alone; it did not weigh Rule 05.3's partisan reason. Because the tokens resolve the error mark by the page's surface (Charcoal) while the bar sits on the field's ground (Prussian), the shared check that fails "any red over Prussian" never sees it, and the stage shows it only after a press.
- **Fix:** keep the bar off Prussian. The smallest change, with no new value: in the dark theme the field ground on Charcoal resolves to Charcoal, and the field shows by its 1 px Newsprint edge (13.29 to 1), so the 4 px bar sits on Charcoal at 4.49 to 1, as the message under it already does. A raised field on Charcoal would need a Charcoal-derived ground that meets Rule 26.2's five conditions, never Prussian. Hold the selected band on Charcoal (also Prussian today) to the same rule before any red mark may touch it. Add a guide check step that presses Send in every form stage in both themes and fails a red pixel beside Prussian. See question 1.
- **Owner:** Engineer (the field ground role in `tokens.css` and `tokens.json`; the guide check); Component engineer (`c-18-form`); Accessibility lead (Rule 18.17's rows if the drawing changes).

### M2. Chapter 19, Rule 19.1, `s-19-criteria`: four criteria are not printed in W3C's order, and 3.3.7 now says something else

- **Where:** `s-19-criteria`, from `stage_c_ch19_build.py`: criteria 3.3.7, 1.4.10, 1.4.12 and 1.4.13.
- **What is wrong:** I compared all 55 criteria with the W3C Recommendation of 12 December 2024, fetched today from w3.org/TR/WCAG22. Numbers, names and levels match for all 55, and 51 texts match word for word. In the other four the generator prints every paragraph first and every list item after, so a sentence W3C places after a list moves in front of it.
  - 3.3.7 Redundant Entry prints "...is required to be entered again in the same process is either:", then "Except when:", then one list of five items: "auto-populated, or", "available for the user to select.", "re-entering the information is essential,", "the information is required to ensure the security of the content, or", "previously entered information is no longer valid." W3C has two lists: the two ways to meet it after "either:", then the three exceptions after "Except when:". As printed, a builder reads auto-population as an exception.
  - 1.4.10 Reflow prints "Except for parts of the content which require two-dimensional layout for usage or meaning." between "...scrolling in two dimensions for:" and its two widths.
  - 1.4.12 Text Spacing and 1.4.13 Content on Hover or Focus print their "Exception:" paragraphs between the lead-in and the list it introduces.
  The chapter's source line promises each criterion "quoted as the Recommendation prints them".
- **Fix:** print each criterion's parts in the Recommendation's document order: lead-in, its list, then any paragraph after it; for 3.3.7, "either:" with its two items, then "Except when:" with its three. Add a generator check that compares each criterion's text and order with a stored copy of the Recommendation.
- **Owner:** Accessibility lead (`stage_c_ch19_build.py`); Research lead to supply the stored text.

### M3. Chapters 17 and 18, Loop R1: a loop the atlas grades plausible is titled as a finding

- **Where:** the heading "From our systems atlas, Loop R1 / Wealth and political influence reinforce each other" in `c-18-loop-stepper` (Rule 18.22) and `c-18-diagram-controls` (Rule 18.23), in both live stages and in the code a builder copies; the same heading on chapter 17's players, `s-17-3-correct` and `s-17-4-correct`; the anatomy plates `s-18-22-anatomy` and `s-18-23-anatomy`, drawn from the sets.
- **What is wrong:** by script on `work/extract/atlas-v7-data.json`, Loop R1 carries `"evidence": "plausible"`. Its middle link, L02, is plausible, and V7's evidence summary calls it "the weakest"; the loop's qualification reads "The loop runs on issues where wealthy donors' preferences differ from those of middle-income voters; on most issues the two groups agree, so its reach depends on the issue." The stepper handles the step well ("Money in politics can raise policy tilt to insiders ... Our atlas grades this step plausible, the least certain in the loop"), but the heading over it states the whole loop as fact, and the diagram's heading carries no grade at all. Master Brief section 15: "Match the title verb to the V7 grade ... Plausible takes 'can' or 'may.'" This is the guide's main example of a loop about money in politics, it appears on four plates in two chapters, and a builder who copies the component copies a heading that claims more than its evidence on a subject readers on each side watch closely (DR-93: size the claim to its evidence grade).
- **Fix:** keep V7's title as the loop's name and print its grade under it, in both sets and both chapter 17 players: "Loop R1, “Wealth and political influence reinforce each other”. Our atlas grades this loop plausible: its middle step is the least certain, and it runs only on issues where large donors and middle-income voters want different things." Or make the heading "Wealth and political influence can reinforce each other". Rerun both anatomy plates and update the alts.
- **Owner:** Component engineer (`c-18-loop-stepper`, `c-18-diagram-controls`); Systems designer (chapter 17's players; the anatomy plates rerun from the sets); Editor for the words; Research lead for the grade line.

### M4. Chapter 18: the atlas samples return to the subject of the editor's campaign

- **Where:** Rule 18.24's rule ("such as “Loop R10” or “Reform R-01”"); `s-18-24-failure` ("R10 shifts accountability to small primary electorates, and R-01 sits on that loop."); `c-18-location` (Rule 18.7: "Atlas / Elections / Safe seats", with "Primary decisiveness" as the next place); `c-18-disclosure` (Rule 18.8: "Illustrative Each line in the drawing joins two parts of the rules. Read in order, they say that more safe seats make the primary the race that decides the seat."); `s-18-23-failure` ("C1 Safe seats"); the anatomy plates drawn from those sets.
- **What is wrong:** by script on the atlas, R-01 (All-party primaries with ranked general elections) and R-02 are the only two of 50 reforms with `interest_note: true`, V7's flag for the editor's own work (the Yes on 3 campaign, D2-106). R-01's targets are L08, L25 and C2, and its loops include R10, so the failure plate names R-01 as acting on its own loop, and the location and disclosure samples teach the exact mechanism R-01 is argued from (L08, "Safe seats make the primary decisive", into C2, "How often the primary decides the winner"). The guide carries no disclosure (DR-100), and the studio has twice moved examples off this subject for that reason: D2-278 took open primaries out of chapter 01, and D2-958 took R-01 and R-02 out of Rule 10.8 and an all-party primary bill out of Rule 11.16, as DR-99 and D2-203 already asked. Chapter 18 brings it back across five plates. Separately, the disclosure labels L08's documented finding "Illustrative", which DR-97 keeps for invented content, so a reader learns that a documented claim is made up.
- **Fix:** take chapter 18's atlas samples from a part of the atlas no flagged reform targets, for example the housing variables (Housing scarcity, Owner home equity) or work and pay, and keep their real grades. Rule 18.24's examples become a loop and a reform with no flag, such as "Loop R1" or "Reform R-04", which the chip set already shows. Rewrite `s-18-24-failure`'s sentence on the new subject. Where a disclosure shows real atlas lines, drop "Illustrative" and give the source and snapshot date; where it shows invented lines, use an invented subject. The filter bar and the search may keep R-01 to R-12, since they list the atlas in its own order (see S2).
- **Owner:** Component engineer (`c-18-location`, `c-18-disclosure`); Accessibility lead (Rule 18.24's words, `s-18-23-failure` and `s-18-24-failure` in `stage_c_ch18_build.py`); Systems designer (the anatomy plates rerun); Editor for the words. See question 2.

## 3. Should fix

### S1. Chapters 11 and 18: invented bill H.99004 means two incompatible things, and H.99001's dates differ

- **Where:** chapter 11's tracker list (Rule 11.5); chapter 18's live tracker `c-18-tracker` (Rule 18.20), table `c-18-table` (Rule 18.10), `s-18-10-anatomy` and `s-18-10-failure`.
- **What is wrong:** chapter 11 says "Bill H.99004, Records request fees ... Step 4 of 6: First chamber. Step 2 never happened, because the committee voted without holding a hearing. The House votes next." Chapter 18's tracker gives the same bill a hearing ("The committee hears the bill on March 19") and ends "Stopped at step 3 of 6: Committee vote, on March 26. The committee voted against the bill.", and its table prints "Records request fees, Filed March 5, Status Stopped in committee". D2-1487 moved the tracker to H.99004 so that "one invented bill means one thing across the guide" (D2-1364); the move made a new conflict. H.99001 is "Filed January 16" in chapter 11 (`s-11-6-correct`) and "January 12" in chapter 18's table and anatomy plate; the table failure plate's "Last action" gives H.99003 February 11, though its other plates say it was filed February 2 and became law April 2.
- **Fix:** give chapter 18's stopped-in-committee story the next number on chapter 11's counter (D2-848) with a new neutral title, or rewrite chapter 18's H.99004 to chapter 11's story; set H.99001 to January 16; give each failure plate row a last action its own story allows. Search all chapters for each bill number after the change.
- **Owner:** Component engineer (`c-18-tracker`, `c-18-table`); Accessibility lead (`s-18-10-failure`); Systems designer (`s-18-10-anatomy`, rerun).

### S2. Chapter 18, Rules 18.15 and 18.16: bare atlas codes, and a sample read as the whole set

- **Where:** `c-18-filter-bar` and `c-18-search`, results lists and status lines, both stages each.
- **What is wrong:** each result prints a bare code, "R-01 All-party primaries with ranked general elections" through "R-12 Senate filibuster reform", 48 bare codes on the page. Rule 18.24, in the same chapter, says a typed ID sets the type word and code together "so a reader never meets a bare code" (house rule H11, D2-756). The status lines read "12 of 12 reforms" under a source line that says the areas and routes "come from our systems atlas, as of October 15, 2026", so a reader takes 12 as the atlas's count; it holds 50. I checked each of the 12 rows by script: titles, areas and routes all match the atlas (city for LOC, Congress for FS, voters for BI).
- **Fix:** write each result as its name followed by its typed chip, "Reform R-01", as Rule 10.8 does; add to the source line "the first 12 of its 50 reforms, in the atlas's order".
- **Owner:** Component engineer.

### S3. Chapter 18: the atlas content has no dated source

- **Where:** chapter 18's `sources`; `c-18-loop-stepper`, `c-18-diagram-controls`, `c-18-location`, `c-18-id-chip`.
- **What is wrong:** chapter 18 shows atlas content in Rules 18.7, 18.15, 18.16, 18.22, 18.23 and 18.24, but its source list has no entry for the atlas, and only the filter bar prints a dated source line. Chapter 17 cites the atlas with its snapshot date; chapter 18 does not. Master Brief section 6 asks every diagram for a source line.
- **Fix:** add "Source: Oath & Action’s systems atlas, Who Do They Answer To?, snapshot of October 15, 2026" to chapter 18's sources with the loops, variables and reforms it uses, and a short dated source line under the stepper and the diagram, as the filter bar has.
- **Owner:** Accessibility lead (sources); Component engineer (the sets).

### S4. Chapter 19, `s-19-criteria`: four "met by" lines claim more than the rules say

- **Where:** criteria 2.2.1, 2.5.4, 1.4.13 and 3.3.4.
- **What is wrong:** I read the cited rules for 20 criteria (listed under Tested). Sixteen hold. Four do not:
  - 2.2.1 Timing Adjustable, "Met, Rules 11.14, 18.20 and 18.22". Rule 11.14 is "Keep topic and atlas symbols out of buttons, and draw each action with its utility icon", and Rule 18.20 is the tracker's updates; neither says anything about time limits. Only Rule 18.22's six-second floor and Pause touch timing, and that is motion, which 2.2.2 covers.
  - 2.5.4 Motion Actuation, "Met, Rule 19.5". Rule 19.5 gives a control beside a tilt or a shake, but the criterion also asks that "responding to the motion can be disabled to prevent accidental actuation", which no rule says.
  - 1.4.13 Content on Hover or Focus, "Met, Rules 11.11, 18.6 and 18.23". No rule states the criterion's three conditions (dismissible, hoverable, persistent) or forbids content that appears on hover or focus; Rule 18.6's menu opens on a press, not on hover.
  - 3.3.4 Error Prevention, "Not used today ... No product takes money or legal statements today". The criterion also covers pages that "modify or delete user-controllable data", and chapter 18's own components save explainers, follow bills and send testimony ("Sent. Your testimony reached the committee clerk.").
- **Fix:** 2.2.1: cite a rule that sets no time limits, or mark it Not used today; 2.5.4: add to Rule 19.5 "and a setting turns the motion response off", or mark it Met in part; 1.4.13: add a line to Rule 18.23 or 11.11 that nothing appears on hover or focus alone, or mark it Met in part; 3.3.4: mark it a gap owed by chapter 18, with a rule that a send that reaches a legislature, or a delete of saved items, can be checked, confirmed or undone.
- **Owner:** Accessibility lead.

### S5. Chapters 17 and 19: small faults in what a standard or a maker says

- **Where and what:**
  - Rule 17.9's reason: "2.4.11 Focus Not Obscured (Minimum) asks that content we place never hide it." The criterion asks that a focused component "is not entirely hidden due to author-created content"; "never hide it" is the AAA criterion 2.4.12.
  - `s-19-criteria`'s last line: "The problems it covered now fall under 1.3.1 and 4.1.2". W3C's Understanding page says "Many issues that would have failed this criterion will fail Info and Relationships or Name, Role, Value. Other issues are excepted".
  - `s-19-devices`, Windows: "Press Insert and Q to quit NVDA." NVDA's user guide gives "NVDA+q, then enter": the key opens an exit dialog that needs Enter.
  - Chapter 19's further reading line names five makers' guides with no address or date read. I fetched all five today, and each title is real as printed.
- **Fix:** "asks that content we place never hide it entirely"; "Many of the problems it covered now fail 1.3.1 or 4.1.2, W3C's Understanding page says."; "Press Insert and Q, then Enter, to quit NVDA."; give each guide its address and the date read.
- **Owner:** Systems designer (Rule 17.9); Accessibility lead (chapter 19); Research lead for the addresses.

### S6. Chapters 18 and 26: invented content that adds a party balance or hides an actor

- **Where and what:** `c-18-tabs`, the Sponsors panel of invented S.99002: "Two sponsors, one from each party." Nothing in the component needs a party; the line invents an even split, the counterweight DR-93 rules out, and teaches that balance makes a bill worth showing. `c-26-warning` (Rule 26.4, example 4, and its plates): "Warning: The hearing moved to March 12." names no one who moved it; DR-93 asks the copy to name who acted.
- **Fix:** "Two sponsors." or "Two sponsors, each listed by name and party as the legislature records them."; "Warning: The committee moved the hearing to March 12."
- **Owner:** Component engineer (`c-18-tabs`); Engineer (`c-26-warning`, its plates); Editor.

### S7. Studio names on reader pages outside the token table

- **Where and what:** code a builder copies carries inventory fault codes in its comments: `c-18-link.css` line 14, "(F-3)", and `c-18-report-reader.css` line 21, "(F-2)". Rule 26.8's change note plate, `s-26-8-correct`, reads "drawn from Night Edition on Charcoal", a name no reader page defines. The results plate, `s-19-results`, names studio roles as owners: "open, with the component engineer", "with the component engineer and the guide engineer", "with the test's owner". DR-218 covers the token table's rows only.
- **Fix:** drop the codes from the comments; write the change note's reason without the internal name ("drawn from our dark atlas style on Charcoal"), in the 6.0.0-gate2.8 release; at the results rerun, write an open item as "open, to fix before launch" with no role names.
- **Owner:** Component engineer; Engineer (the change note in `tokens.json`); Accessibility lead (the results file).

### S8. Chapter 26, Rule 26.4: the live demos carry no Illustrative label beside their invented content

- **Where:** the code plates of `c-26-caption`, `c-26-chart`, `c-26-download` and `c-26-warning`.
- **What is wrong:** each live demo shows invented counts, a file or a date, and the only label is a sentence at the end of the code caption ("Illustrative counts."), after the HTML and CSS panels, well below the demos. Chapter 18's sets carry the label in their own markup at the head of the piece (DR-97).
- **Fix:** put the Illustrative label at the head of each chapter 26 set's markup, as chapter 18's sets do.
- **Owner:** Engineer (`c-26-*`, `stage_c_ch26_build.py`).

## 4. Questions for Dustin

1. **Prussian fields in the dark theme (M1).** If the studio wants raised entry fields on Charcoal in Prussian, as the dark atlas panels are, an error's 4 px red bar would sit on Prussian, which needs an exception to Rule 05.3's "Red never sits on Prussian". **Recommendation:** no exception. Fields on Charcoal take the Charcoal ground with their Newsprint edge, and red stays off Prussian everywhere.
2. **A standing rule for examples (M4).** DR-99 kept one chapter 02 example off the editor's campaigns, and the studio has applied the same idea case by case (D2-203, D2-278, D2-958), yet chapter 18 drifted back. **Recommendation:** approve one standing rule: no example, sample or failure plate in the guide uses a reform the atlas flags for the editor's work, or the mechanism that reform targets; real atlas content elsewhere keeps its grade and source.
3. **Prussian hover beside the ask.** The token architecture steps a primary button's hover fill from Charcoal to Prussian. In Rule 18.1's stage, hovering "Save to your list" draws a Prussian button 12 px from the Pillar Red "Remind me" (screenshot `button-hover-light.png`), a red and blue pair for as long as the pointer rests. Rule 05.3 forbids red on Prussian, not beside it. **Recommendation:** keep the hover token, and set the primary and the ask on separate rows in Rule 18.1's plate, so no specimen teaches the pair; change the hover to another step only if you see the pair as partisan in use.

## 5. Tested

All in Chromium through Playwright on the frozen page, at 1440 px and device scale factor 1 unless named, with Python run with `-I`.

- **Text extraction.** The rendered text and attributes of all 16 chapters and the proofs, scanned for party words, loaded words, studio codes, internal names, retired names, the locked lines and atlas IDs.
- **WCAG 2.2.** Fetched the Recommendation from w3.org (W3C Recommendation, 12 December 2024) and compared all 55 criteria by script: numbers, names and levels match for 55; 31 at A and 24 at AA; the six new criteria tagged; texts match for 51 (M2 has the four). Counted the statuses: 37 met, 5 in part, 8 gaps, 5 not used today, as Rule 19.1 says. All 49 rule links in the list point to anchors on the page. Read the cited rules for 20 criteria: 1.3.1, 1.3.3, 1.3.4, 1.3.5, 1.4.3, 1.4.4, 1.4.10, 1.4.12, 1.4.13, 2.1.4, 2.2.1, 2.4.1, 2.4.4, 2.4.7, 2.5.1, 2.5.2, 2.5.4, 2.5.8, 3.2.3 and 3.3.3, with 3.3.4's status (S4 has the four that fail). Fetched the Understanding page for 4.1.1 and the quick reference.
- **Chapter 19's results and matrix.** The results plate matches `20261111_Stage-C-Round-1-Ch19-Results.json` line for line, with Tested and Not tested apart and no claim beyond the file. The matrix's 14 checks and methods match Master Brief section 22.
- **Browser support.** Downloaded `@mdn/browser-compat-data` 8.1.8 from npm (SHA-1 5604db35..., matching the registry; data timestamp November 2, 2026) and recomputed the first version with full support (no flag, prefix, other name or partial mark) for 32 features. Every figure in chapter 18's 24 "Browser support" lines matches, and so do the notes behind Rules 18.12 to 18.14 (clipboard gesture rules, Chrome 65 and Edge 79 on cross-site downloads). MDN's storage page confirms Safari's seven days.
- **Sources fetched today.** Media Queries Level 5 (W3C Working Draft, 19 February 2026) and its reduce text word for word; WAI-ARIA 1.2 (6 June 2023); Design Tokens Format Module 2025.10 (Final Community Group Report, 28 October 2025); Semantic Versioning 2.0.0 and its author; 12 APG pattern and example pages chapter 18 names, all 200, and the Carousel pattern's note that its buttons do not move focus; the Nebraska Legislature's "Lawmaking in Nebraska" page that Rule 18.5's link opens; the five device guides in chapter 19's further reading; NVDA's user guide for its keys.
- **Contrast.** 236 ratios in the token table recomputed from `tokens.json` with the WCAG formula: 0 differ. 500 rows against 500 tokens, every hex matching. 28 ratios printed in the words of chapters 05, 17, 18 and 26 (among them 4.49, 3.19, 2.96, 4.17, 1.41, 3.37, 13.29, 5.49, 7.26, 7.74, 2.42, 1.72, 2.48, 2.61, 4.29, 3.10, 13.28, 9.42, 1.27, and the rejected red's 3.22 and 1.09): all match.
- **Derived colors.** All 30 OKLab-derived tokens recomputed from their recorded base, target and amount: all 30 reproduce their hex exactly. N-01's 49 failures trace to the token file's register. All 500 names are defined in `tokens.css`, and both files carry 6.0.0-gate2.7.
- **Atlas.** The filter bar's 12 reforms (titles, areas from the reform groups, routes) against `atlas-v7-data.json`, snapshot 2026-10-15: all match. Loop R1's grade, links and qualification; the diagram's three details against the variables' descriptions; the location labels against V7's chain labels; L08's grade; R-01's targets and loops; which reforms carry `interest_note`.
- **Invented bills.** Every bill number and title on the page: all in DR-151's range, each title the same everywhere; statuses compared across chapters 08, 11, 17 and 18 (S1).
- **Red.** A scan of every element's computed fill, stroke, color, border and outline in chapters 01, 03, 05, 08, 09, 10, 11, 17, 18, 19 and 26, with the ground each red sits on. No red sits on Prussian outside labeled failure plates at load, no red icon accent appears under 48 px in the new chapters, and each chapter 18 stage holds one working red at load. Pressed Remind me in both form stages and read the fields (M1). Read the tracker's take-part disc from its CSS. Read the 2x master behind `s-01-21-correct`'s 24 px kicker drawing: its accent defaults to ink. Hovered the primary button in Rule 18.1's stage (question 3).
- **Identity players.** Played the hinge and the lever: each ends with its end layer showing and its moving layer hidden. The hinge's last frames carry path data byte-identical to the 24 px and display wordmark masters; the lever's last frames are pixel-identical to the 48 px and display lockmark masters on Newsprint and Charcoal (0 pixels differ at 1x).
- **Changed parts of 01 to 11.** Rule 08.2's feed figures and floors against `20261111_Promotion-C-Identity-Figures.json`: all match, and the floors follow from the stored study (155 and 190). Chapter 10's counts against the inventory in use: 125 drawings, 94 that read at 32 px, with CL-075 among the other 31 as D2-1236 sets. Every file named in a rule file list in chapters 01, 03, 05, 08 to 11, 17 to 19 and 26 exists. The switch lines in Rules 09.3, 10.4 and 26.5 match. The locked lines: none is misquoted anywhere on the page, and the four new chapters quote none.
- **Studio codes.** Visible text of the four chapters and the code files: F-2 and F-3 only, besides house rules H03, H08 and H11, which chapter 02 names for readers.

## 6. Not tested

- Real screen readers, real phones, Safari, Firefox and Windows contrast themes: none in this container.
- Pseudo-elements in the red scan: the tracker's take-part disc was read from its CSS, not measured.
- The red scan at 2x and 3x and at 390 and 360 px, and dark-theme states that appear only after interaction, other than the form's errors.
- The fifth edition's values that chapter 17 says it keeps (durations, easings, the lever's 1.4 and 1.25, the pulse's 20 percent): the fifth edition's files are not in this container. I recomputed 1.27 to 1 from a 20 percent Pillar Red only.
- The "met by" lines of the other 35 criteria.
- Each APG pattern's keyboard table against the keyboard rows of chapter 18.
- Atlas grades beyond Loop R1, Loop R10, L08 and the 12 reforms in the filter bar.
- Every word of the changed rules in chapters 03 and 09 beyond their file lists and switch lines.
- Items the brief gives other lenses: Rule 08.1's plate, the dark-card feed method (D2-1331), `codeMatch`'s tolerance and the token table's layout. Items waiting by decision: Missouri's count and the four device scripts.
