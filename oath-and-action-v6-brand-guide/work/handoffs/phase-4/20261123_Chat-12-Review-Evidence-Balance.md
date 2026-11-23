# Chat 12 review: evidence and balance (ST, NB)

Reader: Evidence and balance (statistics, then nonpartisanship), with the research lead's source standards and the data visualization lead's chart and atlas rules. Started 17:11 UTC and finished 17:29 UTC on November 23, 2026, by `date -u`. Every check below ran from my own scripts in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/review/evidence-balance/scripts/` (`st_model.py` holds my count methods, written from the model and the text of rulings R2, R8 and R16; `st_check.py` reads every plate view and export; `st_text.py` pulls a page's words). I never ran or read the data lead's or the engineer's scripts for a value.

## 1. Score

**4 of 5.** Every count, ID, sign, type, delay, grade, effect and route that chapter 21 prints matches the model, 0 faults in about 3,800 values. Chapter 20's and chapter 16's figures match their primary sources, read again today. Two faults keep the score from 5. The loop page shows three reforms' effects without the confidence the atlas gives them. The Act page's record section leaves out the first of the two reasons the law gives.

## 2. Must fix

**ST-1. Loop R18's reform panels print effects without the atlas's confidence, and without Rule 15.20's disclosure.**
- Where: A14 and A19, the chosen reform's panel (`data-oa-panel`), on every view and in `20261122_Atlas-Loop-R18-Page.html`. The fix goes in `atlas-page.mjs`, specs 3 (the chooser row of `20261122_Atlas-View-Specs.md`, line 213) and the A14 words. Plates `s-21-loop`, `s-21-13-correct` and `s-21-15-correct` show it.
- What is wrong: each panel prints its four effect rows as codes and words with no confidence. Reform R-48 shows "Quality of democracy +M, moderate positive", but the atlas stores its `effects_confidence` as "low (doctrine)" and grades its remedy a hypothesis. R-11 stores "medium (design inference)" and R-15 stores "medium (value); low (post-Slaughter durability)". None of these words appear on the page or in the plates. `grep` finds 0 matches in the export and in `a14.json` and `a19.json`, and the page holds no `details` element.
- Why it matters: R12 says the confidence words "print quoted as stored (`effects_confidence`), once, under the four rows". The R-23 page follows it ("Our atlas's confidence in these effects: “high to 60% of median; low above”"). Rule 15.20 says to keep "the atlas's qualifications and assumptions one step away, in a disclosure under the panel". Chapter 21's intro says its pages use chapter 15's rules "as they stand". So a reader comparing the three reforms sees a hypothesis at the same standing as the others.
- Fix: under each panel's four rows, print the same line the R-23 page carries, "Our atlas's confidence in these effects: “low (doctrine)”". Add Rule 15.20's disclosure under the panel, holding the remedy's grade word and its stored `remedy_evidence.text`. Extend the atlas test's T7 so a panel without the confidence line fails.
- Owners: the design director (spec and generator), the engineer (renderer and T7), the editor (the line's words, as on A12), and the data visualization lead (sign-off).

**NB-1. The Act page's "What the record shows" prints only one of the two reasons the record gives for the law.**
- Where: A08, `20261121_Web-Act-Page-Comment-On-A-Proposed-Rule.html`, h3 "What the record shows", the paragraph headed "The concern in the law." The fix goes in the A08 page words through `phase4_ch20_build.py`'s word fields or the kit's `--page-words`. The research note `work/research/20261121_Act-Page-Docket.md`, section R5, needs the same correction.
- What is wrong: the page says the exclusion "exists in part “to protect the incentives for new drug development” (page 73721)". The rule, which I read again today in govinfo's PDF, says on page 73720 that Congress included the clause "for two main reasons. The first reason is to prevent manufacturers from escaping appropriate safety and efficacy review and FDA oversight for drugs by classifying these products as dietary supplements." The page leaves that first reason out.
- What else is missing: the rule's own safety finding, "a reasonable expectation of safety for the use of NAC in or as a dietary supplement" (page 73722). The quoted line "To date, we have not received any comments expressing concern…" (page 73723) also needs its context: it refers to comments since FDA's 2022 draft guidance and its 30-day comment period, not to this rule's comment period, which opened November 17, 2026.
- How each side reads it: a reader who wants oversight of supplements finds their concern absent from "the concern the law guards". A reader who wants the change finds FDA's safety finding absent. DR-93 asks for findings as the record shows them, and this record holds both.
- Fix (draft words for the editor): "The concerns in the law. The rule says Congress wrote the exclusion for “two main reasons”: to keep drugs from escaping “appropriate safety and efficacy review and FDA oversight” by being sold as supplements, and “to protect the incentives for new drug development” (page 73720). In 2001, 2010 and 2020, the FDA said products containing NAC are excluded (pages 73719 to 73720). On safety, the rule finds “a reasonable expectation of safety for the use of NAC in or as a dietary supplement” (page 73722). On drug development, it says no comment since its 2022 draft guidance has raised a concern (page 73723), and it asks commenters “whether …” (page 73723)."
- Also: Rule 20.8's text "on the concern the law guards" should read "on the concerns the law guards".
- Owners: the editor (words), and the main session for the research note.

## 3. Should fix

**ST-2. The Register's loops column counts 20 for the whole atlas, where the home page and the loop index say 23, and nothing says why.**
- Where: A13, the index's whole-atlas row and the note under the table (`phase4_ch21_build.py` word fields; the column head in the generator).
- What is wrong: the row reads "51 118 20 49 194, one retired". The home page says "It traces 23 loops", and Rule 21.14's index lists all 23. The note explains the reforms ("its reforms leave out those the atlas rejects") but not the loops. The column counts numbered loops only, by D4-165's method, which is correct.
- Fix: head the column "Numbered loops", or add to the note: "and its loops count the 20 that close through numbered connections; the loop index lists all 23."
- Owners: the editor (note), the design director (head).

**ST-3. Rule 20.11's maskable icon spec misstates its source, and two studio choices read as platform rules.**
- Where: Rule 20.11's specs in `phase4_ch20_build.py`.
- What is wrong: "the 512 px icon maskable, with B inside the circle of 40 percent of its width" reads as a circle 40 percent across. The source, web.dev, which the platform file quotes, sets a circle whose radius is 40 percent of the icon's width. The built icon meets the source: B reaches 197.4 px from the center, 38.6 percent of 512, measured on `20261121_Web-Manifest-Icon-512-Maskable.png`. Separately, "favicon.ico = 16, 32 and 48 px in one file" is marked "not-found, studio-choice" in `20261121_Platform-Specifications.json`, yet the rule's basis cites only "the platform rows".
- Fix: "with B inside the center circle whose radius is 40 percent of the icon's width". Add to the basis: "the ICO's three sizes are our choice; the HTML standard sets none."
- Owner: the editor.

**ST-4. H.R. 7008's source line on the home page breaks H04's order.**
- Where: A06, the Track card. `phase4_ch20_build.py` line 290 appends to the approved `HR_SOURCE`.
- What is wrong: the appended sentence, "Steps from the bill's status file on govinfo.gov, retrieved November 21, 2026.", comes after the qualification and names no publisher or period. H04 asks for publisher, title, period, geography, retrieval date and qualification, in that order.
- Fix: keep the approved line as it stands, and give the steps their own line, as D2-764 did: "Source for the steps: U.S. Government Publishing Office, bill status for H.R. 7008, 119th Congress, updated October 1, 2026, United States. Retrieved November 21, 2026."
- Owner: the editor.

**NB-2. A failure plate credits a real person with an invented photograph that breaks the consent rule.**
- Where: `s-16-6-failure` (`phase4_ch16_build.py`).
- What is wrong: the caption labels the invented student and school "Illustrative", then credits the invented photograph "Photograph: Dustin Cathcart, Oath & Action" with no label. The plate's fault is the missing parent's consent, not the credit. As printed, it puts our founder's name on a consent failure that never happened. DR-302 labels every invented person and quote, and the credit is invented.
- Fix: credit "Photograph: Oath & Action" with Illustrative beside it, as `s-16-9-failure` does with its place.
- Owner: the editor.

**NB-3. The Act page's first tracker step drops the condition FDA attached.**
- Where: A08 and the home's Act card, step 1.
- What is wrong: "April 22, 2022: the FDA said it was likely to propose this rule". The rule (page 73723) records that FDA said it was likely to propose the rule "if, among other considerations, we did not identify safety-related concerns".
- Fix: "April 22, 2022: the FDA said it would likely propose this rule if its safety review found no concern".
- Owner: the editor. Low.

## 4. The named places

- **6, DD11C-Q1, the locator's fill.** The built reading matches the model on every view.
  - Reform R-23 fills Wealth and Your household, from its targets A4 and EC7.
  - Sheet D04 fills Checks, from D1, D4 and D5.
  - Loop R18 fills Checks, from its chain D2 and D4.
  - The fill is Charcoal in ink with no red, as Rule 12.7 sets. A page in two parts filling two reads fine against Rule 12.7's "current part", since R-23's own record holds two parts.
  - Recommendation: the data lead writes this reading as a ruling, and the row closes.
- **14, weight.** The atlas plates carry machine attributes that no reader meets. This is a lossless lead for the engineer's E12 measurement.
  - The test attributes (`data-count-of`, `data-atlas-field`, `data-atlas-kind`, `data-atlas-id`, `data-evidence-href` and others) total 198,582 bytes in `guide.html`.
  - By a rough search, about 127,700 of those bytes are in attributes that no style or script on the page reads.
  - They are 246,752 of the 916,946 bytes of view markup in A11 to A20.
  - Stripping them from the guide's copy after the atlas test passes, while keeping them in the exports, would cut no content. The engineer should confirm which ones the guide's scripts and the check read.
- **15, Rule 05.1 by screen.** I recounted ten first screens from the export PNGs: A11 at 1440 and 390, A12 at 1440, A13 at 390, A14 at 1440, A15 at 390, A06 at 1440 and 360, A07 at 1024, and A08 at 390.
  - My Newsprint share is within 1.3 points of the kit's figure on every screen. All ten fall inside 60 to 85 percent, and red stays at 0.1 percent or less.
  - Rule 20.9's correct plate prints the home's first screen as 81.1 percent, and the kit's facts agree.
- **16, balance by the record.**
  - The four atlas views pass from the left and from the right. R-23's contested remedy prints both readings whole, in order, split at one sentence, with the Congressional Budget Office's estimate of 1.3 million jobs lost and 1.3 million people lifted from poverty. R-35, term limits, prints rejected with the 87 percent figure. Loop R18 prints the 2025 removals as its case and the 2021 removals as "the other party's instances", each whole.
  - The selection rule of D4-164 holds. One caution, with no change asked for: the only reform with a full page is a policy coded left, and the right's favored reform appears only as a rejected option. Each prints its record, so DR-93 asks for nothing more. If a right-leaning reader on board 1 raises it, the answer is D4-164's rotation.
  - The NAC rule passes as a choice of subject, but its record section fails NB-1.
  - S86 is neutral.
  - The H.R. 7008 card names both of the passed bill's provisions. I confirmed the photo ID clause in the engrossed text, Sec. 3.
- **17, the Illustrative label.**
  - The web address carries it in every page footer, and the share card carries no address.
  - The video plates and the failure captions carry it.
  - No direction or prompt carries it, as D4-85 sets.
  - One gap, NB-2.
- **18, the photographs (my part: captions and credits).** Every chapter 16 caption and credit I read is whole: who, what, where, when, then "Photograph: maker".
  - Each agrees with the rights ledger's rows pho-01 and pho-04: maker, agency and license.
  - Rosa Parks's dates (October 30 and 31, 2005) agree with the caption's "October 2005" and its note.
  - The single `photoDrawn` copy, black and white, and the crop rectangle are CR's and AX's to check.
- **Other places I can speak to.**
  - 1: not in my lens.
  - 2: the stepper's holds recount from the words. The status lines read 37 and 64 words, "Step N of 2:" included, so 9,250 and 16,000 ms at 250 ms a word. Both exceed 6,000 ms, as Rule 21.13 sets.

## 5. For Dustin

1. **Connection L14's stored citation overstates its own case (the model; V6 never edits it).**
   - The citation reads "17 IGs removed Jan 24, 2025; ruled unlawful Sept 24, 2025; FEC without quorum since May 1, 2025".
   - Loop R18's stored case says the court said the removals "‘almost undoubtedly’ violated the law" and that "no ruling on the merits had been issued as of October 15, 2026".
   - Both print on the loop page ("Evidence for each step") and on sheet D04's row L14.
   - From the right, "ruled unlawful" reads as a merits ruling the record says did not happen.
   - Recommendation: add it to the atlas V7.1 issue list, beside rows 38 to 46 (G3-03), with the wording "found likely unlawful Sept 24, 2025" for the atlas editor. The guide prints it as stored (DR-37).
2. **Rules 15.16 and 15.20 (approved chapter 15) do not name the effects' confidence words.**
   - The data lead's R12 requires them, and the R-23 page prints them. ST-1's fix brings the loop page into line without touching chapter 15.
   - Recommendation: one sentence added to Rule 15.16, "Print the atlas's confidence in these effects, quoted as stored, once under the four rows.", so the next builder of a chooser cannot miss it.

## 6. Tested

All checks below ran November 23, 2026, between 17:12 and 17:28 UTC.

**Atlas checks against the model** (`work/extract/atlas-v7-data.json`, SHA-256 ef1028ac87e402e30af9e3cda234fed63794b5570d0a165b9dab39073e08c7f2, matching each plate's `atlas.model`):
- My script read every view of plates A11 to A20 and the six exported atlas pages, and checked each value against my own count methods:
  - 1,598 printed counts under 220 distinct keys: attribute equals my count, and printed digit equals attribute.
  - 1,296 typed IDs: each exists in the model under its kind, and each chip carries its ID.
  - 93 connection rows: sign, type, delay and grade.
  - 76 effect codes, by family and printed text.
  - 48 route rows: route, feasibility and checked state.
  - 712 stored-text fields, which print as stored apart from curly quotes and R11's chips.
  - 87 loop grade lines, against each loop's stored `evidence`.
  - Result: 0 faults.
- The Register's index on all twelve sheets matches D4-165's method: variables, connections, numbered loops, active reforms, issues and the five grade columns. So does D04's "9 of 20 issue records" with D4 on.
- The home drawing has 27 outgoing pairs, 81 flows and 37 inside, 118 in all. Each pair prints once in every view, and the five main-circuit flows (A to B, B to C, C to D, D to E, E to A) are all non-zero.
- Loop R18:
  - Two minus signs, so it is reinforcing, which matches the stored type R and the read-aloud line.
  - Weakest step by my own reading of the evidence summary: L15. It is also the least certain grade, plausible.
  - The loop's delay is M. Holds recount as 9,250 and 16,000 ms.
  - Its reform list (R-11, R-15, R-48, from `reforms[k].loops`) and every "also aim here" tag on A12 and A14 match the reforms' targets.
- Chapter 21's captions agree with the model:
  - 5 reforms on A4 or EC7 (21.5's failure).
  - 29 sources on PW06 (21.7's failure).
  - R-11's targets D4, L14 and L15 (21.15).
  - R-35 rejected, with its remedy graded well supported (21.10).
  - 236 is twice 118 (21.9).
  - The index order is reinforcing then balancing, in the atlas's order (21.14).
- The chips plate's ten names and four colliding pairs match the model.
- The atlas test's plate (`s-21-16-correct`) matches the test log: 15, 12, 14 and 15 frames for the four views, 16 checks.

**Chapter 20 against primary sources:**
- The Federal Register API, read today for document 2026-23351, matches every docket fact the Act page prints: title, FDA-2025-N-2699, RIN 0910-AI91, 91 FR 73717, 21 CFR Part 190, published November 17, 2026, comments close January 19, 2027, the comment URL, and the summary quoted word for word.
- govinfo's PDF of the rule, read today, confirms each quotation and page number the page prints. It also gave NB-1's and NB-3's passages.
- govinfo's bill status for H.R. 7008, read today, confirms the steps:
  - introduced and referred January 12, 2026;
  - markup and a 7 to 4 vote on January 14, 2026, with no hearing, so step 2 is a slash;
  - passed the House 232 to 198 on July 22, 2026;
  - cloture not invoked 53 to 47 on September 30, 2026.
- The engrossed text, read today, holds the photo ID section.
- The Census Bureau's own 2022 tables CG2200ORG01 and ORG02, downloaded today, confirm S86:
  - 90,888 governments in all, 90,837 local;
  - 39,555 special districts, 19,491 municipalities, 16,214 townships, 12,546 independent school districts and 3,031 counties;
  - "more than four in ten" is 43.5 percent.
- 13 U.S.C. 161, read today on govinfo, sets a census of governments "for every fifth year".
- The home's claims chart, rebuilt from the model's 433 claims:
  - 74 percent documented overall, from 96 percent (23 of 24) for clean drinking water to 59 percent (13 of 22) for algorithms in daily life;
  - 6 of 39 claims contested for pay and working conditions;
  - 432 of 433 checked.
- PW03 lists 8 decision makers, 6 of whom can change the rules.

**Chapter 16 and the post:**
- S04's figures against the chart kit's data file: 47.7 and 51.4 percent (down 3.7), 74.5 and 74.7 percent, a gap growing from 23.1 to 27.0 points. All four of chapter 16's S04 source lines equal S04's spec line exactly.
- The post's S92 figure: 20 working days plus up to 10, against the data file's row 5. Issue I013's title and grade match the post's text.

**Platform facts:** chapter 20's sizes against `20261121_Platform-Specifications.json`: 1200 by 630 (read), 180 (read), 192 and 512 (read), and the ICO (studio choice). I measured the maskable icon's extent.

**Rule 05.1:** ten first screens, as listed under named place 15.

## 7. Not tested

- Concept 11's printed Register counts. The source file is not in this checkout, so my index rebuild shows only that the page follows D4-165's method, not that the method reproduces Concept 11.
- The Commons file pages for the two photographs answered 429. I checked the captions' names and dates against the rights ledger only. The photograph files carry no caption metadata.
- Regulations.gov's comment form. It answers automated readers with 403, as the research note records.
- The FEC and Congress.gov APIs (no keys), and the Census API's data tables (no key). The Census figures came from the Bureau's published tables instead.
- The rendered guide pages in a browser. I opened no browser and read the plates, exports, specimens and `guide.html` as files.
- The Labor Department's state table behind R-23's status line ("30 states and the District of Columbia"). It is stored text, printed as stored.
- Whether the exports and the guide's plates draw the same page heights. A11's export at 390 px is 5,224 px tall against the plate's 5,249. That is PR's to judge.
- The `photoDrawn` copy, the black and white filter and the crop rectangle, all CR's and AX's.
