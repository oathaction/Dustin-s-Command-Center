# Stage B round 3: red team on brand, evidence and nonpartisanship

Oath & Action Edition 06, Phase 2, stage B, round 3, November 10, 2026. Reviewer: brand, evidence and nonpartisanship, in the research lead's role (`.claude/agents/oa-research-lead.md`) with the creative director's brand knowledge. Page reviewed: the frozen copy at the scratchpad's `round-3/review/guide.html`, built from commit ddd3a898 (D2-955). The chapter JSON and specimen files in `work/build/guide/` are unchanged since that commit (`git diff ddd3a898 HEAD` touches only the brief and the decision log), so their words are the page's words. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: complete.

## 1. Score

**3 of 5.** The record work is sound: every atlas label and ID matches Atlas V7 by script, Rule 01.11's count and its sources hold, every invented bill sits in DR-151's range with its label, and no topic, atlas or pillar drawing keeps its red under 48 px; but the systems examples in chapters 10 and 11 lean on the two reforms V7 flags for the editor's own campaigns, one plate lists two of ten reforms as if they were all, and two specimens state more than their evidence holds.

## 2. Must fix

### M1. Chapter 10, Rule 10.8, `s-10-8-correct`: two of ten reforms, both the editor's, printed as "the reforms that act on them"

- **Where:** `s-10-8-correct` (Rule 10.8's correct plate), its alt in `manifest-systems.json`, and Rule 10.8's correct caption.
- **What is wrong:** under "Domain D02, Elections and representation" and its six variables, the plate heads a list "Reforms that act on them" and names two: "Reform R-01, All-party primaries with ranked general elections" and "Reform R-02, Ranked-choice voting for single-winner races". By script on `work/extract/atlas-v7-data.json`, ten reforms aim directly at one of D02's six variables (B5, C1 to C5): R-01, R-02, R-03, R-05, R-06, R-07, R-34, R-45, R-46 and R-47. The heading tells a reader these two are the reforms that act on the domain, which drops eight (DR-93: no piece drops a finding). And R-01 and R-02 are the only two of V7's fifty reforms that carry `interest_note: true`, V7's flag for the editor's disclosed work (D2-106: the Yes on 3 campaign for Massachusetts Question 3, and Ranked Choice Melrose). DR-100 took that disclosure off every page, so nothing tells a reader why these two lead. DR-99 and D2-203 already keep examples and invented bills off the editor's campaigns.
- **Fix:** print the count and choose by a rule that is not the editor's work. For example, set the list's head to "Two of the ten reforms that act on them" and show two V7 does not flag, such as Reform R-05, Automatic voter registration, and Reform R-45, Verifiable elections with paper records and audits; or list all ten as chips with their names. Change the alt and the caption to match. Rerun the label check on the new rows.
- **Owner:** Systems designer (chapter 10); Editor for the words.

### M2. Chapter 11, Rule 11.16, `s-11-16-correct` and `s-11-16-failure`: an invented bill on the editor's campaign topic, with an ask

- **Where:** both plates, their alts, Rule 11.16's correct caption, and the counter table in `20261110_Stage-B-Round-2-Systems-Ch11-Notes.md` (H.99009).
- **What is wrong:** the view invents "Bill H.99009, All-party primaries", headed "The House hears the all-party primary bill on March 3", with "You can take part now. Send written testimony by March 3." and a figure "Where the bill would act, in our systems atlas", where "Reform R-01 acts here. All-party primaries would move the choice a primary makes in a safe seat to every voter." The topic is the editor's own campaign (D2-106), V7 flags R-01 for his interest, and D2-203 moved every invented bill to neutral topics (public meeting notice, school bus contracts, library hours, records request fees) for exactly this reason. Of the nine invented state bills in chapters 08 and 11, this is the only one on an election rule. A guide that models taking part on its editor's cause, with no disclosure on the page, hands a critic the case that the brand is not nonpartisan.
- **Fix:** give H.99009 a neutral subject in D2-203's sense, and draw the figure from a reform V7 does not flag (for example R-32, Public and philanthropic funding for local news, on Variable B2, or R-14, Automatic funding to prevent government shutdowns, on Variable D5). Keep the three marks, their order and the yielding exactly as they are; only the subject changes. Update the caption, both alts and the notes' counter table.
- **Owner:** Chapter 11 hand; Editor for the words.

### M3. Chapter 11, Rule 11.14, `s-11-14-correct` (and its failure copy): the loop's weakest step stated as a finding

- **Where:** the loop stepper's step 3, in the specimen's `data-steps` JSON.
- **What is wrong:** step 3 reads "Electoral pressure lowers incumbent control of election rules." That step is V7's link L53, graded plausible, and V7 names it the loop's weakest link ("plausible for C3 to C4 (the weakest link)"). H08 and W16 give a plausible claim "can" or "may", and the Master Brief (section 15) matches the verb to the grade. The stepper prints every step as a direct claim and says nothing about grades, so a producer copying this live component learns to drop the grade. The other three steps hold: L08 and L42 are documented and L25 is well supported.
- **Fix:** step 3's first line: "Electoral pressure can lower incumbent control of election rules." Its second line keeps V7's plain sentence and adds: "Our atlas grades this step plausible, the least certain in the loop." Apply the same words wherever the failure plate repeats the steps.
- **Owner:** Chapter 11 hand; Editor for the words.

### M4. Chapter 12, Rule 12.6, `s-12-key-correct`: the chart's title says more than its own counts

- **Where:** the title of the key plate's chart, its alt, and the alt text in `stage_b_ch12_systems_build.py` (line 228).
- **What is wrong:** the title reads "Most claims in these three chapters rest on the record", and the plate's own key defines "Documented, on the public record". The counts the plate draws (build script line 163: Wages 6, 4, 3, 1, 1; Housing 4, 5, 2, 2, 0; Elections 7, 2, 1, 0, 1) put 17 of 39 claims at Documented, 44 percent, and Documented is a minority in Wages (6 of 15) and Housing (4 of 13). The counts are invented and labeled so, but the title is the rule a producer copies, and H08 says a title states only what its evidence shows. A plate in the chapter that teaches keys should not teach an overclaiming title.
- **Fix:** either retitle to what the counts show, "Most claims in these three chapters are documented or well supported" (28 of 39), or change the invented counts so Documented is a majority in each bar and keep the title. Change the alt to match.
- **Owner:** Systems designer (Rules 12.5 to 12.9); Editor for the words.

## 3. Should fix

### S1. Chapter 11, `sources[2]`: the Justice Department report is cited to the wrong section and the wrong coverage

- **What is wrong:** the line reads "Office of Information Policy, Justice Department, “Fiscal Year 2024 Annual Freedom of Information Act Report”, March 6, 2025, section III, fiscal year 2024, federal agencies." I downloaded the report from justice.gov. Its title and date are right. Section III is "Definitions, Exemptions, and Component Acronyms" and does not hold the categories Rule 11.8 uses: "Request Withdrawn" sits among the "Full Denials Based on Reasons Other than Exemptions" in section V.B.(1), and the appeal outcomes (affirmed, partially affirmed and partially reversed or remanded, completely reversed or remanded, closed for other reasons) in section VI.B. The report covers the Justice Department and its components (ATF, BOP, FBI and the rest), not all federal agencies.
- **Fix:** "Source: Office of Information Policy, U.S. Department of Justice, “Fiscal Year 2024 Annual Freedom of Information Act Report”, March 6, 2025, sections V.B.(1) and VI.B, fiscal year 2024, the Justice Department and its components. Retrieved November 9, 2026. The categories behind the end words in Rule 11.8." If the studio wants to say every agency reports on the same categories, the research lead should cite OIP's guidance for agency annual reports first.
- **Owner:** Research lead; Chapter 11 hand to apply.

### S2. Chapter 11, Rule 11.10's reason (and Rule 11.9's): the law's clock described loosely

- **What is wrong:** Rule 11.10 lists "an agency’s question to the requester, a fee estimate or a ten-day extension" and says "The law treats these waits as pauses in the agency’s 20 working days". 5 U.S.C. 552(a)(6)(A)(ii), read today on the Legal Information Institute, lets an agency toll the 20 days once while it waits on information it asked for, and as needed to clarify fees. The ten-day extension is a different thing: under (a)(6)(B)(i) the agency extends its deadline by up to ten working days in unusual circumstances, by written notice. Rule 11.9's reason says sending a comment is "the way the law gives the public to take part in a federal rule"; 5 U.S.C. 553(e) also gives a right to petition for a rule.
- **Fix:** Rule 11.10: "The law lets an agency stop its 20 working days while it waits on the requester, once for more information and again to settle fees, and add up to ten working days in unusual circumstances, so each wait belongs inside the step it falls in." Rule 11.9: "the main way the law gives the public".
- **Owner:** Editor, with the Research lead.

### S3. Chapter 11, Rules 11.8 and 11.10: federal clocks on requests that read as local

- **What is wrong:** Rule 11.8 says "A records request asks a government agency", and its reason and sources are federal (FOIA and the Justice Department). The plates print the federal clock ("Its 20 working days stop until you answer") on subjects most readers place with a town or a state, such as "Snowplow contract records" and "School lunch inspection records". Rule 12.9's source line already says "Federal agencies only; states set their own records laws."
- **Fix:** add to Rule 11.8: "These steps and end words follow the federal Freedom of Information Act and the Justice Department’s categories; a request to a state or local agency follows that state’s law." Give the invented requests subjects a federal agency holds, or drop "20 working days" from them.
- **Owner:** Chapter 11 hand; Editor for the words.

### S4. Chapter 11, Rule 11.1's reason: the state hearing claim has a source ready and prints none

- **What is wrong:** the reason says a committee takes testimony "from the public in many state legislatures". The research lead's round 0 notes (`20261109_Stage-B-Research-Notes.md`, section 4) give five legislatures' own pages and a ready source line. All five answered 200 today, and I read Nebraska's.
- **Fix:** add the research lead's line to chapter 11's sources, as written in section 4 of those notes, behind Rule 11.1.
- **Owner:** Chapter 11 hand; Research lead.

### S5. Chapter 12, Rule 12.7, `s-12-locator-correct`: invented headers with no label

- **What is wrong:** the plate prints an atlas view titled "How safe seats move the real choice to the primary" and a state story "Tracker · Nebraska / Nebraska has one chamber, so a bill’s fifth step never comes". Neither is a real view or story (the title appears nowhere in V7; it comes from the stage A board), and the plate carries no Illustrative label, though every other invented piece in chapters 09 to 12 does (H03, DR-97). "Elections" in the breadcrumb is DR-35's plain name and stands.
- **Fix:** one Illustrative label at the plate's head, in the alt as well.
- **Owner:** Systems designer.

### S6. Chapter 11, `s-11-16-correct`: one label over a mix of real and invented items

- **What is wrong:** the view's one Illustrative label at its head covers an invented bill and a figure "from our systems atlas" with a real reform and real variables. DR-97 puts a label beside each invented item where real and invented items mix.
- **Fix:** once M2 is done, set Illustrative beside the bill card, and leave the atlas figure unlabeled.
- **Owner:** Chapter 11 hand.

### S7. Chapter 01, Rule 01.21 and `s-01-21-correct`: "topic symbol" in the rule, an atlas symbol in its kicker

- **What is wrong:** Rule 01.21 says the one picture a kicker may hold "is a topic symbol from the Civic Line". Its correct plate's Analysis kicker draws CL-057, which the editor's own label table classes as an atlas variable (EC3, "Workers’ share of income"). Rule 10.4 allows any of the 37 topic and atlas drawings at 24 px in a kicker. A producer reading 01.21 alone would refuse CL-057.
- **Fix:** Rule 01.21: "a topic or atlas symbol from the 37 that read at 24 px (Rule 10.4)", and the same in its specification and builders line.
- **Owner:** Editor.

### S8. Source lines in scope that name no period

- **What is wrong:** chapter 11's sources 1, 2 and 4 and Rule 12.9's source line give publisher, title and retrieval, and no period: the statutes and FOIA.gov, RegInfo.gov and the Nebraska page carry no date. Rule 12.9's line also drops "via the Legal Information Institute", which chapter 11 prints for the same statute.
- **Fix:** add "as in force on November 9, 2026" after each statute and "no page date" after each undated web page; add "via the Legal Information Institute, Cornell Law School" to Rule 12.9's line.
- **Owner:** Research lead; Chapter 11 hand and Systems designer to apply.

### S9. Chapter 05, `s-05-3-corrective`: the D2-881 redraw should take Rule 11.15's color

- **What is wrong:** already on the fix list as a cross in a red disc. The plate also draws the glyph in red, which Rule 11.15 measures at 2.64 to 1 on the Error Band. A redraw that swaps the shape and keeps the red would leave chapters 05 and 11 showing two error treatments.
- **Fix:** draw `U-error` in the text's ink with the 4 px red bar, as Rule 11.15 and D2-880 do, until Dustin rules on D2-880 at board B.
- **Owner:** Systems designer.

## 4. Questions for Dustin

1. **How far should the guide's systems examples rotate away from your campaigns?** After M1 and M2, the atlas examples in chapters 11 and 12 and the reader check still center on one mechanism and its two reforms: Rule 12.5's marker shows R-01 on loop R10 (the Master Brief's worked example 4 named R-01), Rule 11.14's stepper runs loop R10 (both R-01 and R-02 act on it), and the reader check shows R10 with R-01's targets in red (D2-222) and asks readers to name R-02 (DR-189). V7 flags R-01 and R-02 for your interest, and DR-100 took the disclosure off every page. Nothing here is false, and DR-189 and the Master Brief stand, so this is your call. **Recommendation:** keep Rule 12.5 and the reader check as they are, and let the studio move Rule 11.14's stepper to loop R1, "Wealth and political influence reinforce each other" (no flagged reform acts on it, and its plausible middle step teaches the least certain step, the Master Brief's worked example 1), so chapters 10 to 12 do not read as a showcase for one reform.

## 5. Tested

- Read the round 3 brief, `CLAUDE.md`, my role file and the creative director's, Master Brief sections 2, 3, 6, 11, 12, 14 and 15, the stage B brief and round 2 brief, the writing rules' W16, W20 and house rules, the decision log from DR-93 to DR-194 with the D2 calls the brief names, the round 2 research notes and chapter 11's notes, and the round 0 research notes' sections on hearings.
- Extracted the text, alts and labels of chapters 09 to 12 from the frozen page by script, and read chapters 09 to 12 in full from their chapter JSON and the page text, with chapter 01's Rule 01.11, Rule 01.21 and pillar specimens, `s-08-3-*` and `s-05-3-corrective` from their specimen files.
- **Atlas labels and IDs, by script against `work/extract/atlas-v7-data.json` (`python3 -I`):** all 124 library rows (50 reforms against V7 titles, R-13 and R-36 against DR-185; 51 variables against V7 loop short names or titles, D2-751); every "Variable" and "Reform" chip with its name in the page's text and alts; Domain D02's name and its six variables; loop R10's and R4a's titles; hubs, layers, parts and route names; loop R10's chain signs and each link's plain sentence against the stepper; R-01's targets against the marker plate; L08's sign, grade and delay against the marker's tag, line and tick. Every label matches; R-38 differs only by its curly apostrophe. A pattern scan of chapters 09 to 12 for V7, decision and studio codes found every V7 ID in a typed chip or named in words ("loop R10", "reform R-01"), except the library's reform rows, which print the drawing ID under the sheet heading "Reforms R-01 to R-25" that names them; no decision or studio code.
- **Rule 01.11's count:** V7's repair log rows RL38 to RL64, claim CL1713 and pathway PW15 give the same eight maps the plate counts once Missouri is counted as passed and Utah's court map left out (DR-187).
- **Sources fetched today and read:** nebraskalegislature.gov "Lawmaking in Nebraska" and "Tips on Testifying"; 5 U.S.C. 552, 553, 801 and 706 on law.cornell.edu (tolling, the ten-day extension, 90 days to appeal, 20 days for an appeal, OGIS mediation, district court jurisdiction, tracking numbers, 30-day effective date, the 60-day major rule, disapproval, set aside); foia.gov FAQ; reginfo.gov FAQ (pre-rule, proposed, final and interim final rules, the Congressional Review Act); the Justice Department's FY 2024 annual FOIA report, its web page and PDF (title, March 6, 2025 cover date, sections III, V.B.(1) and VI.B); Texas Legislature Online, H.B. 4 history, 89(2) (House 08/20/2025, Senate 08/23/2025, signed 08/29/2025); California Secretary of State, Statement of Vote, November 4, 2025, Proposition 50; St. Charles County's November 4, 2026 page (785,969 yes and 1,273,815 no on Proposition A); Virginia Department of Elections' May 8, 2026 release. The three live links in `s-11-13-correct` and the four other hearing pages answered 200.
- **Invented items:** every invented bill, request and rule in scope checked for its Illustrative label and number range (DR-151; H.R. 99012, H.99001 to H.99009, S.99002 to S.99007, LB 99008; requests and rules from 99001).
- **Red, in Chromium on the frozen page at 1440 px:** every `svg[data-icon-family]` read for `--oa-icon-accent` and its drawn size from its screen matrix (427 drawings). No topic, atlas or pillar drawing keeps red under 48 px; only the 41 appear at 24 px; in each correct row only the current item keeps red. By their markup (`data-red-job`), the correct plates of Rules 11.4, 11.5, 11.6, 11.9, 11.15, 11.16 and 12.5, the Charcoal list and `s-05-3-corrective` each hold one red job, and Rule 12.7's holds none. Contact sheets and tiles drawn as images were looked at only where named below.
- **Approved finals:** the page's sprite symbols for CL-025, CL-014, R-13, CL-073 and CL-074 match the element structure of the approved options (B, C, B, A and A); CL-059, R-42 and R-48 in the library sheets looked at beside the three options each, and match B, B and C. The masthead's menu glyph is `U-menu`, byte for byte the final. Rule 08.1 lists the rebuilt 24 and 48 px lockmark files and keeps the 16 px master (DR-181); chapters 03 and 04 cite the end mark's fit B files (DR-180) and L6 centered (DR-182).
- **The reader check:** read the editor's questions file and the page's configuration; confirmed by script that step 8's lines are word for word from V7's pathway PW03, and that the bills and party questions are as the file sets them.
- Contrast ratios the chapters print (13.29, 9.42, 2.96, 2.64, 11.89, 3.37, 1.17, 1.24 and others) recomputed from the token values.

## 6. Not tested

- Tangipa v. Newsom's January 14, 2026 order (courtlistener answered 403 and the govinfo API hit its rate limit); the Ohio Redistricting Commission's minutes and transcript, Missouri's certified result (not issued; D2-838) and the other party counts in the round 2 research notes, which I did not reopen.
- The four construction principles credited to our fourth edition (Rule 10.2) and the lines credited to the fifth edition (Rules 12.1 to 12.3, 12.9): V4.2 and V5 are not in this checkout (DR-90), so I checked them only against the Master Brief and the round 2 brief.
- I did not try ncsl.org, congress.gov or regulations.gov, as the brief asks.
- The library's PNG sheets beyond the three redraws I looked at; the tile images; how any plate looks at 390 or 360 px or at 2x; forced colors.
- Whether readers read a party into any plate: only the reader check can say.
- A grep pattern I ran over `work/handoffs/phase-2/20261110_*.md` returned one line from the plain language team's report. I read no more of it, and nothing in this report rests on it.

## Change log

- Created: `work/handoffs/phase-2/20261110_Stage-B-Round-3-Red-Team-Brand-Evidence.md` (this file).
- Modified: none. Scratch scripts, downloads and captures are in the scratchpad's `round-3/brand-evidence/`.
