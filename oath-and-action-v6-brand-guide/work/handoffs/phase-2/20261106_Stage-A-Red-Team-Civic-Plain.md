# Stage board A: civic education and plain language review

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Red team lens 4, civic education and plain language. Written by the civic education reviewer for the main session and the fix pass, under `work/handoffs/phase-2/20261106_Stage-A-Red-Team-Brief.md`, applying `.claude/agents/oa-editor.md` and chapter 02's writing rules.

I read the page as an adult who has never seen the brand: a volunteer who writes a newsletter, a partner who makes one card, a reader who found the guide online. For each rule I asked whether that person could follow it and act on it with no other document, whether each term is explained where they first meet it, and whether the examples teach the rule they sit under. The newcomer judgments below are mine; no reader took part.

## 1. Score

**3 of 5.** Most rules teach well, and chapters 02, 05, 06 and 07 explain their own terms as they go, but chapter 01, the newcomer's way in, uses the guide's vocabulary for pages before any chapter defines it, about 30 decision codes and internal document names sit on the page against H11, and five examples contradict or fail to show the rule they sit under.

## 2. Must fix

**CP-M1. Decision codes and internal document names on the page (H11).** H11 says "print no bare code", and the Stage A brief bans decision codes on the page. A public reader cannot look any of these up. Found by script in the rendered text:

- Part opener: "arrives with stage board B (DR-88)."
- 03 Identity: the eight-lockups caption, "until the site is settled (DR-55)"; the minimum-size table caption, "read from the identity masters' table (I8)"; Rule 03.4's basis, "measured in Chromium at device scale 1 (Identity masters notes, October 28, 2026)".
- 04 Ampersand: Rule 04.1 basis "(Identity masters notes, October 28, 2026)"; 04.3 basis "Rule 05.3 (D2-01, DR-66); G1-05"; 04.4 basis "Rule 05.3; D1-22"; 04.5 basis "the five separation rules approved with I6 (G1-01)", and the page never lists those five rules; 04.6 basis "the badge's three conditions (S9, G1-02)", and the page never lists those three conditions; 04.7 basis "R13 (DR-67)" and its why, "(R13)"; 04.5 why, "Atlas V7".
- 05 Color: 05.3 basis "decisions D2-01 and DR-66"; 05.6 basis "Master Brief section 10; decision D1-04"; 05.7 basis "decisions DR-48, DR-53, DR-54 and DR-58" and its specs, "Newsprint (DR-53)"; the palette caption, "locked in Master Brief section 3".
- 06 Type: 06.1 basis "Master Brief section 3; decision DR-47"; 06.3 basis "Master Brief section 8, tension 1; decision T-9"; 06.9 basis "Master Brief section 10"; 06.10 basis and why, "Master Brief section 3 says a font substitution is never a finished identity decision"; 06.2 specs, "chapter 25, Phase 4".
- 08 Signal Grid: 08.1 basis "(Identity masters notes, October 28, 2026)"; 08.5 basis "D1-21"; 08.7 basis "R9 (DR-67)" and its why, "(R9)"; 08.8 basis "Master Brief V2 section 10"; Sources, "approved at Gate 1 (S5)".
- Proofs appendix: "(DR-71)", "(D2-30)", "R13", "(DR-55)" twice.
- 02 Voice: "approved at Gate 1" (brand lines table), "approved on Board 5" (index caption).

Fix: keep the basis to its reason in words. "Design judgment; decisions D2-01 and DR-66" becomes "Design judgment". Where the reason is a locked rule, say so in words: "our locked identity rules" for Master Brief section 3, "our measurements, October 2026" for the identity masters notes, "until our web address is settled" for DR-55, "our systems atlas" for Atlas V7. Where a basis cites a list the page never shows (04.5's five separation rules, 04.6's three conditions), print the list in the rule or drop the reference. State R9 and R13 in words where they apply ("Under 48 px a pillar mark sits with its word"), as 08.7's why already half does. In the proofs, the codes can move to the gate report, where Dustin reads them.

**CP-M2. Chapter 01 uses the guide's vocabulary before any chapter defines it.** A newcomer opens chapter 01 first and meets, in its first five rules, Pillar Red, Charcoal, Stone, Prussian (23 times in chapter 01), Newsprint, Verdigris, "view", "working red" and a Tokens block of `--oa-color-...` names. Chapter 05's intro defines the seven colors, Rule 04.2 defines a view ("one view: a screen, a card, a slide or a printed page") and Rule 04.3 defines working red ("the one red each view may spend"). "Token" is never defined anywhere in chapters 01 to 08. Later in chapter 01 the reader also meets "Loop R4a, the map-drawing loop" (01.11; nothing says what a loop is), "atlas domain" (01.9), "the deck" (01.20, three times, never defined), "hinge headline" and "hinge pair" (01.18; defined only in 02.27) and "lockup" (the founding line; defined in chapter 03). Rule 01.4, "On Prussian, identity marks turn White and data marks turn Newsprint.", reads as code to someone who does not know Prussian is our dark blue. This breaks H02, "Define each term of art in plain words where it first appears."

Fix: add a short key to chapter 01, after its intro, titled for example "Words this guide uses", with one line each: the seven colors and their jobs (from chapter 05's palette sheet); view; working red and signature red; token ("a named color, size or type setting in our code, such as `--oa-color-text-primary-on-newsprint`; builders use the name, and writers can skip the Tokens lines"); kicker; deck ("the line under a headline"); hinge headline; the atlas, its loops ("a chain of causes that comes back to where it started", or the atlas glossary's own wording) and its ten domains. Or define each at its first use in chapter 01. Either way, link each term to the chapter that sets its rules.

**CP-M3. W01 and W02 show the virtue as the fault.** In chapter 02 the failure plate is the pattern card (D2-177). For W01 it reads "× Failure case. The pattern. Plain prose: everyday words in complete sentences, with nothing a listener would need to see on the page to follow." For W02 it reads "The pattern. Active voice: a sentence that names the actor first". Under a × Failure case label, a newcomer learns that plain prose and active voice are the faults. The other 19 cards name the fault (parataxis, setup and payoff, nominalization and so on). The alt text of `s-02-1-fault` and `s-02-2-fault` repeats it.

Fix: on the failure card, name the fault. W01: "Writing for the eye: phrases a listener cannot follow without seeing them, such as 'the point of responsibility'." W02: lead with "Passive voice: a sentence that puts the thing acted on first and often hides the actor, as in 'The budget was passed.'" Keep the approved Terms wording on the correct plate or in the rule, where it defines the good habit. Update both alt texts.

**CP-M4. Chapter 04 shows a failed hinge headline as correct.** Rule 02.27's failure plate quotes our fifth edition's "The hearing & the vote." and says it "puts an event first". Rule 04.3's correct plate prints "The hearing & the vote." at 24 px as a correct hinge headline (alt text of `s-04-3-correct` too). Rule 04.3's failure and corrective plates use "The bus map & the vote.", which fails 02.27's own test, "ask whether its first half is a rule a reader could look up". The corrective example keeps that headline as the fixed version. "The budget & the bill." on the same plate is unclear in a civic guide, where "bill" first reads as legislation. A reader who checks chapter 04 against chapter 02 finds the guide disagreeing with itself.

Fix: draw 04.3's three scales from 02.27's correct list ("The zoning code & the rent.", "The filing deadline & the ballot.", "The coverage rule & the copay.", "The records law & the answer."), and give the Act card a headline that passes 02.27, such as "The route plan & your commute." Update the alt text and captions.

**CP-M5. Rule 01.11's correct example describes the two parties' cases unevenly.** The rule asks for "a documented case from each, at the same length", and the caption says the plate shows "one case from a Republican majority and one from a Democratic majority". The plate reads:

- Texas: "the Republican-led legislature redrew the congressional map, aiming at five more Republican seats."
- California: "voters approved Proposition 50, which put in place a congressional map drawn to favor Democrats."

The Texas line names the majority that acts. The California line names voters as the actor and hides who drew the map in a passive verb (W02), so it does not show a Democratic majority drawing a map. A reader on the right will read the pair as easier on Democrats, which is the outcome the rule exists to prevent. By search: Proposition 50 put in place the map in Assembly Bill 604, drawn for the Democratic-controlled legislature, and aimed at five Republican-held seats (Ballotpedia; PBS NewsHour, November 2025).

Fix: "In November 2025, California voters approved Proposition 50, which put in place a congressional map the Democratic-led legislature drew, aiming at five more Democratic seats." Make the same change in the alt text of `s-01-11-correct`.

**CP-M6. A newsletter writer gets two endings.** Rule 02.24 says "End every piece on the one step a reader is most likely to take, with its date". Rule 02.23's correct plate ends the newsletter on "That's the briefing for November 6." and the tagline, with no step. Rule 02.8 allows the tagline "where a sign-off line belongs". A volunteer writing an issue cannot tell whether the last line is the step or the tagline. "That's the briefing for November 6." also tells readers what they have read, the summary beat W07 removes.

Fix: in 02.24, add one sentence: "In a newsletter, the step ends the last story, and the sign-off and the tagline follow it." In 02.23's plate, replace "That's the briefing for November 6." with a dated step, such as "Sign up with the board clerk by April 10 to speak before the vote." Illustrative, then the tagline.

**CP-M7. Rule 02.25's first row swaps a mood for an unrelated fact.** The rule says to replace a mood "with the mechanism behind it". The first row turns "Our democracy is broken." into "In 23 states, citizens can petition a proposed law or constitutional amendment onto the statewide ballot." Nothing in the initiative count explains the claim it replaces, so a writer learns to answer a feeling with any true fact. The editor's notes record that this line replaced the fifth edition's closed-primary line (open question 1).

Fix: use a mechanism a reader could tie to the claim. Our own atlas already supplies one, in W07's rewrite: "In most districts the general election is easy to predict, so the contest that decides the seat is a low-turnout primary." Keep the initiative count where it teaches, on Rule 01.5's map. See question 2.

**CP-M8. Rule 01.21 asks a writer to pick one of six labels and never says what they mean.** The rule lists "Explainer, Tracker, Analysis, Report, Act · How to take part, or Our position". Nothing tells a volunteer how an Analysis differs from an Explainer or a Report, and the pillar list in the same chapter never mentions Analysis or says which label a newsletter issue takes. The correct plate's last kicker reads "OUR POSITION / ACT", two words where the rule says "one content label"; "Act" is the pillar's name, and nothing on the page says so. The builders note says a piece that fits none "needs a ruling before it runs" and does not say whose.

Fix: give each label one line ("Explainer: how a rule or decision works", "Analysis: what the evidence shows about a contested question", and so on), say which label a newsletter issue and its stories take, say that "Act" after "Our position" names the pillar, and name who rules on a piece that fits no label (the editor).

**CP-M9. The tracker's key speaks legislative jargon.** Rule 08.3 says a coded grid "sits beside words that say what it shows". The words on the page are the nine stage names in `s-08-stages`, `s-08-3-correct` and `s-08-5-correct`: "Filed", "Referred", "Reported out", "Passed first chamber", "Reconciled", "In effect". A newcomer does not know that "referred" means sent to a committee or that "reported out" means the committee sent the bill on. "Reconciled" will remind some readers of federal budget reconciliation, a different procedure. Rule 04.4's divider specimen uses "reports the bill out" with no gloss as well. The tracker is the product that teaches a reader where a bill stands, so its key has to pass H02.

Fix: give each stage a plain name or a gloss in the legend, for example "Referred: sent to a committee", "Reported out: the committee sent it to the full chamber", "Passed first chamber", "Both chambers agreed on one text" in place of "Reconciled". Keep the short names in the key line if space needs them, and print the glosses once per tracker page.

## 3. Should fix

**CP-S1. Chapter 01 runs 24 rules with no groups.** Chapter 02 sorts its rules into teaching groups; chapter 01 runs from color to photographs to example rotation to word choice to hinge headlines to labels in one list. Group them under headings without changing the Rule IDs (D2-180): party and color (01.1 to 01.5), pictures (01.6 to 01.8), choosing examples (01.9 to 01.12), words (01.13 to 01.17), hinge headlines (01.18 to 01.20), labels and Act pieces (01.21 to 01.23), names (01.24). Hinge headline rules sit in three places (01.18 to 01.20, 02.27, 04.3); add one line in each that points to the other two.

**CP-S2. One edition gets five names.** Our fifth edition appears as "our brand guide, fifth edition" (chapters 01, 02, 05, 06, 07), "Edition 05" (chapters 03, 04, 08), "V5" (03's minimum table, "from V5's layout"; specimen labels in 04.1, 08.1 and 08.5; seven alt texts), and the fourth as "edition 4.2", "Edition 04" and "V4.2" (alt text of `s-03-7-failure`). H02 asks for one term. Use "our fifth edition" and "our fourth edition" after one full first use, and drop V5 and V4.2 from labels and alt text.

**CP-S3. Production words on the page.** Every chapter's Files closer says "Download buttons for these files arrive with the asset package in Phase 5." Rule 03.2's builders note says "until their own masters are drawn after Gate 2". Rule 01.12 says "The studio reviews the log at each gate", and 01.9's builders note says "before a chapter goes to review". The Track piece and Rule 02.25's source lines say "The studio could not open the Senate's own page for the vote." "Later stage" appears about 200 times. A partner or volunteer does not know what a phase, a gate or the studio is, and the Senate line sits inside a specimen that models our published voice. Fix: "Download buttons arrive with the asset package."; "Our editors review the log before each report or series runs."; "We could not open the Senate's own page for the vote."; and "In a later chapter" or "Coming later" for "later stage".

**CP-S4. Rule 01.13 teaches a wrong fact about the office it names.** Its why says "at the next election they can vote its members out", and its correct plate names the state public utility commission. Voters elect commissioners in about 10 states; the other 40 appoint them, mostly by the governor (Ballotpedia, May 2026; Canary Media). Fix: "A reader can call an office or testify before it, and at the next election they can vote out its members or the official who appointed them."

**CP-S5. Rule 01.17's pair describes two different things.** The failure line is about "the filibuster"; the correct line defines "cloture". A newcomer will not see that they describe one rule, so the pair does not show how to rewrite the first. Fix the correct line: "The filibuster lets senators keep debating a bill until 60 of them vote to end debate, a vote called cloture." Keep the glossary source.

**CP-S6. Rule 01.16 labels the two readings unevenly.** The rule asks for the same treatment of both. The plate gives one side a credential, "Economists Anna Stansbury and Lawrence Summers", and the other a tag, "The Economic Policy Institute, an advocacy group". Describe both holders the same way, by role and affiliation, with no tag on one that the other lacks.

**CP-S7. "Lever" gets two definitions in one chapter.** W04's rewrite defines it as "a place where one change has wide effects"; Rule 02.26's terms table defines it as "The lockmark's larger red node, bottom right: the point that moves the structure." Join them: "Lever: a place where one change has wide effects. In the lockmark, the larger red node at bottom right stands for it."

**CP-S8. Terms drift between chapters.** "Kicker" (01.21, 02.14, 08.8) becomes "eyebrows" in 06.3's why. The same housing topic is "backyard cottages" (01, 02), the "Accessory Homes Tracker" (01.22) and the "accessory dwelling bylaw" (letterhead proof). Chapter 01's pillar list says "The Dispatch"; Rule 02.26, which asks writers to "spell the six series names exactly", and Rule 08.6 say "Dispatch". Pick one term for each, and gloss the housing term once ("backyard cottages, which zoning codes call accessory dwelling units").

**CP-S9. Other terms used with no definition.** "Candidate lines" (02.23, "keep the candidate and founding lines out of the tagline's slot"); "colophon" (02.23 and the brand lines table); "the four-dot row" (brand lines table); "fairness kit" (01.23's title; its rule lists three items and its builders note asks for "the eight kit items"); "masterbrand" and "trust mark" (01.24's why); "Civic Line" (08.8); "breakpoint" and "em" (07.5; chapter 06 defines rem only); "Dim Newsprint" (first use 05.2, defined in 05.6); "diverging pair B" (05.6, 05.7; no pair A appears). Define each at first use or use the plain word.

**CP-S10. The chapters' own prose breaks chapter 02's rules in a few places.**
- Contrasting pairs (W09, W10): 01.14's why, "...tells half our readers the piece is not for them, while a question about who decided... invites everyone in"; 02.16's why, "A stack of softeners blurs how sure we are, while one grade verb..."; 02.18's why, "Memo verbs put distance between the writer and the reader, while the words a resident would use...".
- Corrective negation (W09): 04.3's builders note, "Set B as an inline image, not a font glyph"; the chapter 02 legend, "Illustrative: written to show the fault, not quoted", printed six times. That legend is also wrong for W05, whose before is quoted from a real draft, and it redefines the label H03 sets ("beside every invented person, quote, place or figure"). Write: "Illustrative: invented for the example."
- Landing line and summary beat (W07): the founding line panel's "The founding line stays in our history, out of every lockup and headline."; the checklist's "The ten questions close the writing section. A yes to each one means the draft passes."
- Openers that only announce (W05): the proofs' email line, "Here is who wrote it, what changed since the draft, and how to speak before the vote." (also a list of three on one frame, W12); the letterhead, "We are writing to ask for the approved minutes...". Write "Sign up with the clerk by noon Monday to speak before Tuesday's vote." and "Please send us the approved minutes...".
- Hidden actors (W02): 04.6's plate, "when the minutes are published"; 01.17 and 01.24, "the officials a reader is asked to contact"; 01.23's specs, "Opponents are named by office or role, never by party as a villain."

**CP-S11. Rules 01.9 and 01.10 cannot be applied as written.** Rule 01.10 asks for examples "from every region of the country", and neither its plate nor the rotation log shows a region; the chapter's named places are Texas, California and the invented Alder County. Add a region column to the log and to 01.10's plate, and a case from the Midwest or the Northeast. Rule 01.9 names Massachusetts with no reason a reader can see; say why. Both rules count "within a chapter", a unit a newsletter or a tracker does not have; name the unit for each product (an issue, a month of issues, a report).

**CP-S12. Chapter 05 gives two answers for the series a chart's title names.** Rule 05.7 says "The series a title names takes Charcoal". Rule 05.5's correct plate gives that bar the working red. Say when the named series stays Charcoal and when it takes the view's red ("the one point the headline names", Rule 05.3).

**CP-S13. Rule 06.5 lists "scorecards" among our products**, while Rule 01.24's failure plate names "The Senator Scorecard" as a product we do not make. Drop "scorecards" from 06.5.

**CP-S14. Rule 04.6 bans the badge "from candidates and ballots" with no reason**, and "candidates" first reads as people. Write: "Keep it off anything about a candidate or a ballot measure, where a seal-like mark could read as an endorsement."

**CP-S15. Rule 05.7's why leads with measurements.** "At least 0.106 apart in OKLab, about 5 times the 0.02 that CSS Color 4 treats as the smallest visible difference" comes before a newcomer knows why the pair is safe. Lead with the plain reason (neither end belongs to a party, and the arrow carries the direction) and move the numbers to Specifications. Its failure caption, "Fails the nonpartisan rule.", should name the rule: "Fails Rule 01.3."

**CP-S16. Two small rule and plate mismatches in 01.24.** The correct plate captions a report as "numbered and dated" and shows no date. The failure plate's "Dispatch from the Front" carries no Illustrative label here, though it carries one in 01.15.

**CP-S17. "Alder" is two invented places with different governments.** Alder County has "Five county supervisors" and a "Board of Supervisors"; the letterhead puts a "Town of Alder" in Massachusetts with a town clerk and a Planning Board. Massachusetts counties have no boards of supervisors, so a reader who joins the two learns a government that does not exist. Rename the letterhead's town or keep Alder County out of any named state.

**CP-S18. H10's example contradicts its own source line.** The example reads "Georgia: Democratic +0.2 in 2020"; the qualification says "Margins are Republican minus Democratic share", which makes 2020 −0.2. Reword the qualification: "Each margin is the leading party's lead, in percentage points of all presidential votes."

**CP-S19. On a phone, the tracker example hides its step.** At 390 px, Rule 08.5's correct plate scrolls sideways and cuts "Testimony is open until March 3", the one line that tells a reader what to do, off the frame. Show the tracker list at phone width too, since most readers meet it there (02.1's why).

## 4. Questions for Dustin

1. **May the fix pass amend three approved rewrites (DR-73)?** Chapter 02 says each quoted rewrite passes "every rule on the page". Two still trip a newcomer. W03's after leaves "the federal statute" unnamed and says "Audits then check" with no actor (W02). W07's after uses "electorate" and "Incumbents" with no gloss (H02), and Rules 06.8 and 07.5 reuse that paragraph as sample text. W20's after uses "margin of error" with no gloss. *Recommendation:* allow small amendments that name the law and who audits from the atlas record, and add a short gloss: "incumbents, the officials already in office"; "the survey's margin of error, the range within which its estimate could be off".
2. **Which line answers "Our democracy is broken." in Rule 02.25?** The editor asks you to keep the sourced initiative count (open question 1 in the editor's notes). *Recommendation:* use a mechanism that explains the claim, W07's atlas line about predictable general elections and low-turnout primaries, and keep the initiative count on Rule 01.5's map, where it teaches.

## 5. Tested and not tested

### Tested

- Read `CLAUDE.md`, the red team brief, the Stage A brief, `oa-editor.md`, chapter 02's writing section, the decision log from DR-36 to DR-92 and D2-162 to D2-220, and the editor notes' open questions.
- Rendered the page in Chromium with Playwright at 1440 px and 390 px, extracted the visible text of the cover, contents, part opener, chapters 01 to 08 and the proofs appendix, and read all of it.
- Element screenshots at 1440 px (1x) and 390 px (2x) of the cover, chapter 01's head and Rules 01.1, 01.21, 02.1, 02.22, 02.23, 02.25, 04.3 and 08.5; viewport screenshots at 390 px of 02.22's two plates, chapter 01's head and 08.5's plate. Looked at 02.1, 02.22's failure plate, chapter 01's head and 08.5 closely.
- Read all 234 specimen text alternatives as extracted from the page.
- Script counts, per section, of decision codes (DR-, D1-, D2-, G1-, T-, R9, R13, I6, I8, S5, S9), "Master Brief", "Phase", "Gate", "Board 5", "the studio", "later stage" and the edition names; the same scan over alt texts.
- Script counts of where key terms first appear by chapter (token, view, working red, Prussian, kicker, deck, loop, domain, lever and others).
- Script scan of the chapter JSON prose: em dashes 0; listed intensifiers and corporate verbs only inside W17, W18 and 02.26, which name them; ", while" 8, read by hand; corrective negation 1; 28 passive hits, read by hand.
- Script scan of the correct-use specimen copy for announcing openers, exclamation points, negation and hidden-actor passives.
- Script check of which specimen frames scroll sideways at 390 px: 64 do; 02.22's house rules table does not.
- Web searches: utility commissioners elected or appointed (Ballotpedia, May 2026, and Canary Media: about 10 states elect, 40 appoint); California Proposition 50 (Ballotpedia, PBS NewsHour, Wikipedia: the legislature's map from Assembly Bill 604, aimed at five Republican-held seats, approved November 4, 2025).

### Not tested

- No real reader took part; every newcomer judgment is mine.
- Widths 1024, 360 and 320 px, and text at 200 percent.
- A screen reader; I read the alt text as text only.
- The facts in the source lines beyond the two searches above (the Ballotpedia initiative count, the BLS, Census and FEC figures, the 2023 survey), which belong to the brand and evidence lens.
- The makers' notes in full; I read the editor notes' open questions only.
- The interactive composer after Rule 08.9, beyond its text.

## Change log

- Created: `work/handoffs/phase-2/20261106_Stage-A-Red-Team-Civic-Plain.md` (this file).
- Modified: none. Scratch files (text extracts, screenshots, scripts) sit in the session scratchpad, outside the repository.
