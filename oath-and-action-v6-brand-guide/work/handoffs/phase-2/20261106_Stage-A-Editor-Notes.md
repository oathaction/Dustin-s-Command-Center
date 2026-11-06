# Stage board A: editor's notes, chapters 01 Purpose and 02 Voice

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the editor (`oa-editor`) under `work/handoffs/phase-2/20261106_Stage-A-Brief.md`.

## What I built

Both chapters are finished guide pages in the content contract. A script writes them, so the approved writing section is carried from its content file and never retyped.

- `work/build/guide/chapters/01-purpose.json`: 24 rules, 4 extras, 9 source lines.
- `work/build/guide/chapters/02-voice.json`: 27 rules, 9 extras, 7 source lines.
- 115 specimens in `work/build/guide/specimens/` (`s-01-*`, `s-02-*`) and `manifest-editor.json`.
- The build: `python3 -I work/build/scripts/phase-2/guide_editor_build.py`, with `guide_editor_common.py`, `guide_editor_ch01.py` and `guide_editor_ch02.py` beside it. The script runs the editor's checks and writes nothing if any fails.

### Chapter 01 Purpose

- **Before Rule 01.1, three extras:** the hinge in the locked lines (each line shown whole, its commitment in bold and its action underlined); the four pillars in order with each pillar's job and products, named as the brand's set with no dates or status (DR-91); one piece from each pillar at a phone's text width (340 px). Explain and Track use real atlas copy and records (the electric-bill pathway; H.R. 7008, House 232 to 198, Senate cloture 53 to 47). Connect and Act are invented, with the Illustrative label beside each invented item.
- **Rules 01.1 to 01.20:** the nonpartisan rule set approved at Gate 1 (S7), with the numbers kept because icon notes already cite 01.1, 01.4 and 01.6. I copy-edited the wording to pass chapter 02 and left the substance alone, with one exception: Rule 01.3 now names the diverging pair Dustin chose (Prussian through the page color to Verdigris, with boxed arrows, DR-54), where the Gate 1 text left the hues to Phase 3.
- **Rules 01.21 to 01.24:** content labels in the kicker; the process piece; the position piece with its fairness kit (DC-01, G1-01), both at true size as the strategy review asked; product names.
- **After Rule 01.24:** the founding line, “From spectators to stewards.”, as a record with no role.
- The chapter passes its own Rule 01.9: 13 examples, the largest domain supplies three, and no named state supplies more than one. The log is at the end of these notes.

### Chapter 02 Voice

- **Intro:** the writing section's first two narrative paragraphs, verbatim.
- **Before Rule 02.1:** the brand lines table (the four locked lines, the pillars, voice line B, "Democracy has a structure." in its 08 role, the founding line, and DR-77's four retired lines as a labeled record); the writing section's opening and rule index; group 1's opener.
- **Rules 02.1 to 02.21 are W01 to W21.** Group openers sit after 02.4, 02.8, 02.13 and 02.20.
- **Rule 02.22:** all 12 house rules in Board 5's table, with H08's before and after and its grades table. The checklist follows it.
- **Rules 02.23 to 02.27:** the brand lines in their places, one next step, the mechanism table, vocabulary and the hinge headline copy rule (links to 04). An extra before 02.24 maps the fifth edition's "How we sound" to the rules that now teach it.

**How the 21 writing rules fit the template.** I chose rules 02.n with each W number kept in its title, and I numbered them so Rule 02.n is W(n). The reasons:
- Every W rule gets its own h3 and anchor, so a screen reader user can move rule by rule through the text that binds every word. If the 21 rules were one rule with a specimen set, they would be styled text inside an image, with no headings.
- Every existing citation of a W number stays valid, and its Rule ID has the same number.

What carries each part:
- **Correct application:** Board 5's pair. The before, then the hinge divider, then the after, with a dotted underline on what the rule removes and a solid underline on the repair. Its caption is the approved "What changed" line.
- **Failure case:** the pattern the rule removes, named in the approved terms line, with the before shown again and only its fault in full ink. W03 has no terms line, so its card shows the before's sentence lengths.
- **Why it works:** a new line for each rule, with the basis "Editorial judgment".
- **Specifications:** the rule's group and the before's source.

Every approved string appears unchanged, and the build checks this by script.

## Routine calls, as proposed decision lines

- D2-xxx | Rules 02.1 to 02.21 are W01 to W21, numbered alike, each titled with its W number | Every rule gets a heading and an anchor, and every W citation stays valid
- D2-xxx | The 12 house rules form one rule, 02.22, in Board 5's table, with each row anchored | Board 5 approved them as a table; the index and group 5 link to each row
- D2-xxx | In each W rule, the correct plate is Board 5's pair and the failure plate is the pattern card | This carries the approved pair look into the guide without printing the before twice in the same form
- D2-xxx | Each W rule gets a new "Why it works" line with the basis "Editorial judgment" | The template needs one; the approved words are untouched
- D2-xxx | W21's typesetting note prints without "(DR-79)", and the index says "six marked Illustrative" where Board 5 printed "6" | H11 and H06 on the guide's own page
- D2-xxx | Rules 01.1 to 01.20 keep their Gate 1 numbers; the pillars, products and pieces sit as extras before Rule 01.1, and the Act and naming rules are 01.21 to 01.24 | Icon notes cite 01.1, 01.4 and 01.6; a reader still meets the pillars first
- D2-xxx | The labeled-position pattern lives in 01 as Rules 01.22 and 01.23, and 13 should cite them | The Stage A brief places it in 01; the map and strategy had it in 13
- D2-xxx | The fifth edition's "23 states" row becomes a sourced count: "In 23 states, citizens can petition a proposed law or constitutional amendment onto the statewide ballot." (Ballotpedia, read November 6, 2026) | Tension 17 needs a source or a label; this one is real and checkable
- D2-xxx | The mechanism table's hearing row carries the Illustrative label, and its structure row uses Senate Vote 253 (53 to 47, 60 needed) | The fifth edition's hearing was invented; the vote is in Atlas V7
- D2-xxx | Its columns read "What a draft says" and "What we publish", in place of "We publish the mechanism / Not the mood" | The old heading is a corrective negation (W09)
- D2-xxx | Pillar pieces are 340 px wide, two to a row at 1440 | 340 px is a phone's text column, and two fit in the guide's content column
- D2-xxx | Party bars in Rule 01.2 run in alphabetical order, with Charcoal first | A stated order that favors no party
- D2-xxx | Voice line B appears on the About page, after the mission | Neither Gate 1 nor the strategy named its place
- D2-xxx | The specimen classes `.btn` and `.bars` are renamed (`.cbtn`, `.bchart`) | The shell's own classes of those names leaked into the specimens

## Open questions for Dustin

1. **The "23 states" row.** I replaced the fifth edition's unsourced closed-primary line with a sourced count of states with a working citizen initiative. *Recommendation:* keep the sourced line. The other path keeps the old line with an Illustrative label, but an invented figure about real primaries sits close to your own ballot work. Neither line argues a reform, so I added no disclosure; say if you want one.
2. **Two fifth-edition supporting lines that DR-77 does not cover:** "Here is what the record shows. This part still needs…" and "The rules connect. The gaps create opportunity. Pe…". The text census cuts both at 50 characters. *Recommendation:* retire the second, since it is a parallel run and uses the "gaps" frame Gate 1 dropped. Read the first in full before deciding; it may serve as an example of graded language under W16 and H08.
3. **A content label for Connect pieces.** The six approved labels have none for a guide or a call script, so the Connect specimen borrows "Explainer · Field Notes". *Recommendation:* add "Guide".
4. **Lines I wrote where the census cut the fifth edition's text:** Connect's job line ("Help people reach the office that decides and the evidence it decides on."); the end of the "words we use" list (vote, office, deadline, step); and the mechanism row "The committee chair decides which bills get a hearing.", completed from its first 50 characters. *Recommendation:* approve, or send the full fifth-edition wording.

## Cross-chapter wording issues for the fix pass

1. **Decision codes in reader text.** These print in "Why it works" basis lines, against H11 and the brief's check:
   - 03: DR-55
   - 04: D2-01, DR-66, G1-05, D1-22, G1-01, G1-02, DR-67, I6, S9
   - 05: D2-01, DR-66, D1-04, DR-48, DR-53, DR-54, DR-58
   - 06: DR-47
   - 08: D1-21, DR-67, R9

   Name the decision in words (for example, "approved at Gate 1") and keep the codes in the manifests and notes.
2. **Bare lockup codes.** L1, L2, L3, L6 and L8 appear about 50 times in 03 and 4 times in 08. Under H11, name each at first use, as in "L3, the horizontal lockup".
3. **"Atlas V7" in reader text** in 04. The public name is "our systems atlas".
4. **Corrective negation (W09):**
   - 04: "Set B as an inline image, not a font glyph"
   - 06: "draw a phone version rather than shrinking the desktop one"
5. **Rule titles mix two forms.** Titles in 03, 04 and 08 are instructions; those in 05, 06 and 07 are statements; mine mix both. Pick one form for the guide.
6. **Kickers.** Rule 08.8 builds a kicker from a 24 px grid, an icon and a label. My series kickers in 01.15 and 01.21 carry the label alone. Decide whether 08.8 covers every kicker or series kickers only.
7. **Two hinge divider geometries on one page.** The shell sets the ampersand near the text edge; Board 5's pairs and my piece specimens center it. The identity designer should rule.
8. **Overlapping rules that should cite each other:** 06.5 and H07 (the minus sign); 06.3 and the 13 px rule; 04.3 and Rules 01.18 and 02.27 (hinge headlines).
9. **Chapter 05's `s-05-pairs` failed contrast at three widths in my full run:** Stone "Aa" at 4.29 to 1 on Newsprint, flagged by the rendered check and by axe. My last run, at 1440 and 390 px, passes, so it looks fixed. Confirm at 1024 px.
10. **Shell classes reach into specimens.** `.btn`, `.bars`, `.hinge` and `.n` from the shell's CSS apply inside plates. Worth a note in the shell notes for every maker.

## Tested

- The editor build's checks, all passing:
  - Locked lines exact, with no near miss (tagline 7, mission 4, reader promise 4, commitment 4 in my source text).
  - No em dash character in any file. W21's is drawn as a rule one em wide, labeled "em dash".
  - No decision code or internal edition code in reader text.
  - No listed filler or corporate word outside the rules that name them.
  - Every Illustrative-flagged specimen carries the label.
  - Every W rule's name, rule, terms, why, source, before and after, every house rule field, the grades table, the checklist, the narrative, deck, scope and sources note found in the output.
  - CSS font sizes at 13 px or more; no literal colors; no heading elements.
  - Every token name in `tokens.json`; every file path present; every specimen placed once; chapter 01's own rotation under one in four.
- `guide_build.py`: 0 warnings for the whole page.
- `guide_check.js` at 1440, 1024, 390 and 360 px: chapters 01 and 02 pass every test. This covers structure, anchors, alt text, the 13 px floor, contrast, Rule 05.3, locked lines, em dashes, axe-core 4.10.2 (already in `work/build/node_modules`), focus and sideways scroll. That run's only failures were chapter 05's `s-05-pairs`. A last run at 1440 and 390 px, after my final copy edits, passes the whole page with 0 failures.
- Captures at 1440 and 390 px of chapter 01's head, every extra, Rules 01.1, 01.3, 01.5, 01.22 and 01.23, and chapter 02's index, house table, mechanism table and Rules 02.3 and 02.21, looked at by eye. At 390 px no stage of mine scrolls sideways.
- Weekdays of every invented date by script: March 2, 3 and 9, April 13, 2027, and February 26, 2027.
- A hand read of every line of my prose, and a script that lists every three-item list for that read. It found and I fixed 17 lines: matched pairs, landing lines, negative runs, one typo, one triplet and one fraction.

## Not tested

- I did not view every plate by eye. I looked at about 20 of 128 placements at each width.
- How the copy sounds to real readers. No reader saw it.
- The fifth edition's full text for the census-cut lines in question 4.
- Senate Vote 253 on senate.gov, which refused automated reading earlier (D2-104). It is cited as recorded in the atlas.
- Ballotpedia's initiative count against state constitutions.
- Screen readers, Firefox, Safari, forced colors, 200 percent zoom and print.

## Rotation log, chapter 01 (Rule 01.12)

| Example | Domain | State | Level | Coalition behind any reform shown |
|---|---|---|---|---|
| Who sets your electric rate | Housing, health care and getting ahead | Every state | State | No reform shown |
| The stock trading ban | Money, lobbying and influence | National | Federal | Survey majorities of both parties' voters |
| A county road budget (invented) | Congress, agencies and public services | Alder County, invented | County or city | No reform shown |
| Backyard cottages (invented) | Housing, health care and getting ahead | Alder County, invented | County or city | Invented |
| Posting committee votes, S. 214 (invented) | News, records and public information | Unnamed state, invented | State | Invented |
| Mid-decade map redraws | Elections and representation | Texas and California | State | No reform shown |
| Citizen initiatives | Elections and representation | 50 states and DC | State | No reform shown |
| Productivity and pay | Work, pay and bargaining power | National | Federal | No reform shown |
| The cloture rule | Congress, agencies and public services | National | Federal | No reform shown |
| A state overtime rule (invented) | Work, pay and bargaining power | Unnamed state, invented | State | Invented |
| A school bell schedule (invented) | Housing, health care and getting ahead | Unnamed district, invented | School district | Invented |
| How property tax rates are set | Taxes, wealth and economic security | Every state | County or city | No reform shown |
| A bus route hearing (invented) | Congress, agencies and public services | Unnamed city, invented | County or city | No reform shown |

## Change log

Created:
- `work/build/guide/chapters/01-purpose.json`
- `work/build/guide/chapters/02-voice.json`
- `work/build/guide/specimens/` (115 specimens):
  - `s-01-hinge-lines.html`, `s-01-pillars.html`, `s-01-pieces.html`, `s-01-founding-line.html`
  - `s-01-N-correct.html` and `s-01-N-failure.html` for N from 1 to 24
  - `s-02-lines.html`, `s-02-index.html`, `s-02-group-1.html` to `s-02-group-5.html`, `s-02-checklist.html`, `s-02-sound.html`
  - `s-02-N-pair.html` and `s-02-N-fault.html` for N from 1 to 21
  - `s-02-N-correct.html` and `s-02-N-failure.html` for N from 22 to 27
- `work/build/guide/specimens/manifest-editor.json`
- `work/build/scripts/phase-2/guide_editor_build.py`, `guide_editor_common.py`, `guide_editor_ch01.py`, `guide_editor_ch02.py`
- This file

Modified:
- `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report and its check results, regenerated by the engineer's `guide_build.py` and `guide_check.js`
- Nothing else. No ledger, source file, master, board or other maker's file was touched, and nothing was committed.

## Fix pass, round one

November 6, 2026, under `work/handoffs/phase-2/20261106_Stage-A-Fix-Pass-Brief.md`, "Editor". I changed only my own files: chapters 01 and 02, their specimens, `manifest-editor.json` and the four `guide_editor_*.py` scripts. The container restarted partway through; my edits survived on disk, and the main session's snapshot commit 914c714 holds the work in progress. I committed nothing.

### Items, by ID

**Brand and evidence**
- BE-M1 and DR-98: the bill is "H.R. 7008, the Stop Insider Trading Act" everywhere. At its first mention in each chapter (the Track piece in 01; the structure row of Rule 02.25 in 02) it states both provisions in DR-98's words. The tracker is the "Stop Insider Trading Act Tracker" in the Track piece, Rule 01.21 and Rule 01.24. The survey's source line now ends "The survey asked about a ban in general and names no bill.", and no line ties it to the votes. The rotation log splits the survey and the bill into two rows; the bill's coalition waits for the research lead's roll call check. Rule 02.25's row reads "H.R. 7008, the Stop Insider Trading Act, would bar ... federal elections. It needed 60 votes to move forward in the Senate and got 53."
- BE-M2 and CP-S6: Rule 01.16 describes both holders in one form, "Economists writing for the National Bureau of Economic Research find" and "Economists writing for the Economic Policy Institute find", 24 words each, checked by script. The source line now says the two measure different pay, average pay in one and typical workers' pay in the other.
- BE-M3: Rule 01.2 is rewritten to DR-48 and DR-58: every party's mark in the party mark ink (`oa.chart.color.party.mark.onNewsprint`, Charcoal on Newsprint) with its name printed; solid and outline in the same ink where two sides must be told apart at a glance. Rule 01.1's vote card takes the same standard for the two sides of a vote.
- BE-S1 and CP-M5: Rule 01.11's cases share one form and one length (23 words, checked by script): "In August 2025, the Republican-led legislature passed a congressional map aiming at five more Republican seats, and the governor signed it that month." and "In August 2025, the Democratic-led legislature passed a congressional map aiming at five more Democratic seats, and voters approved it as Proposition 50." The rule text now says "both parties", as the title does.
- BE-S2: Rule 01.2's title reads "In May 2023, most Democrats and most Republicans favored a ban ...", and the measure line says "favored".
- BE-S3: Ballotpedia is marked "a secondary source" with "as of November 6, 2026" in the line itself, on Rule 01.5's map and in Rule 02.25. Each state's limits wait for round two.
- BE-S4: a "Failure case: do not publish" band sits inside the stages of 01.1, 01.2, 01.3, 01.5 and 02.22's failures (01.1 and 02.22 also color a side or a party), and each alt opens with the same words.
- BE-S6: Rule 01.18 says the ampersand takes the headline's ink when an error or a step on the same view holds the red, citing Rule 04.3.
- BE-S7 as D2-257: Rule 01.23's disclosure part reads "Who decided the position and when, any funder's interest in the measure, and links to the bios of those who decided, above the ask." The position piece shows it: our editorial board, February 26, 2027, no funder with a stake, and a link to the board members' bios.
- BE-S9: Rule 01.4's basis is "Design judgment, measured against WCAG 2.2 SC 1.4.11 at rendered sizes", and its why states both reasons: 2.27 to 1 at 16 px, and red on our dark blue pairs the two colors election maps give the parties.

**Accessibility**
- AX-S8: every piece and card is a `div`; my build now fails any landmark or article element in a specimen.
- AX-S14: 01.24's failure alt names both Illustrative items. The group openers are gone (C-S11); their legend now sits in the "How Oath & Action writes" extra and its alt.
- `readable: true` on every static table and list I own: the words key, the hinge lines, the pillars, 01.9's two tallies, 01.10's two level lists, 01.12's two logs, 01.24's two name lists, the founding line, the brand lines, the writing section's opening, 02.22's house table, the checklist, "How we sound", 02.25's mechanism table and 02.26's vocabulary. `interactive` is now on none of my specimens; none has a control.

**Craft**
- C-M5: H08's grades leave the cell and run full width under H08's row as their own table (grade, what it means, title verb), stacking on phones.
- C-M7: every font size in my specimens comes from the D2-254 table through one helper, `fx()`, which takes face, weight, line height and tracking from the type tokens, so DR-95's tracking reaches the specimens. My build fails any size off the table and any hand-written fluid size.
- C-S4: tabular figures only on numbers in columns: 01.9's tallies, the Track piece's step numbers, the checklist's numbers and W03's sentence lengths. The house table, the brand lines and the rotation log set their words without them.
- C-S6: phone pages carry `width_px` 360 with 16 px margins, as chapter 05's do: the vote card (01.1), the Prussian panel (01.4), the cards of 01.6 to 01.8, both Act pieces (01.22, 01.23), the tagline slot (02.23), the newsletter ending (02.24) and the mood card (02.25). Page text flows: reference sheets, the writing pairs, single lines, headlines, readings, charts and the pillar pieces, whose caption gives their 340 px column. See "Declined or changed".
- C-S8: one Illustrative label, the shell's `<span class="illus">`, never restyled; one label at the head of an invented piece and one beside each invented item where real and invented mix (DR-97). The process piece went from seven labels to one.
- C-S11: both chapters carry `groups`. Chapter 01 runs in six groups, chapter 02 in seven (the five teaching groups, then house rules and our lines and words). `s-02-index` and `s-02-group-1` to `s-02-group-5` are retired; the build deletes their files. Checked on the built page: 13 group blocks, each linked from the rule index and from "In this chapter".
- C-S15: every chapter 01 title is an instruction, such as "Keep red off every party, side and person."

**Civic education and plain language**
- CP-M2 and RP-S7: "Words this guide uses" opens chapter 01 after the intro: 15 terms, among them the seven colors, view, working and signature red, kicker, deck, hinge headline and divider, lockup, the atlas with its loops and domains, evidence grade and Illustrative. Token is defined there for the first time. Each links to the rule or chapter that sets it.
- CP-M3: W01's and W02's failure cards name the fault ("Writing for the eye: ...", "Passive voice: ..."). Their approved terms lines print whole in their rule text, so no approved word is lost.
- CP-M6 and RP-M2: Rule 02.24 adds "In a newsletter, the step ends the last story, and the tagline follows it as the issue's sign-off." Its correct plate is one whole newsletter ending: the last story, the hinge divider, "What you can do", the dated step and its button, then the wordmark and the tagline. Rule 02.23's newsletter cell ends on W08's dated step and the tagline; "That's the briefing for November 6." is gone.
- CP-M8 and RP-M1 (D2-250, DR-103, D2-249): Rule 01.21 now carries one kicker grammar and the seven labels, Guide among them, each defined in its specifications; a newsletter issue carries no label in its header; a pillar name alone and a chart's "Finding" line are never kickers; a piece that fits no label goes to the editor. Every kicker in my specimens follows it (for example "Explainer · Utility rates" and "Guide · Field Notes"; round two sets Dispatch stories to "Report · Dispatch").
- CP-S1: chapter 01 in six groups, and the hinge headline rules point at each other: group 5's line names Rules 02.27 and 04.3, and Rule 02.27 names Rules 01.18 to 01.20 and 04.3.
- CP-S2: "our fourth edition" replaces "edition 4.2"; no "V5" or "V4.2" in my reader text or alts.
- CP-S3: "We could not open the Senate's own page for the vote."; "Our editors review the log before each chapter, report or series runs."; "our shared tile grid"; builders notes say "before the piece runs".
- CP-S4: Rule 01.13's why: "they can vote out its members or the official who appointed them."
- CP-S5: Rule 01.17's correct line: "The filibuster lets senators keep debating a bill until 60 of them vote to end debate, a vote called cloture."
- CP-S7: Lever, in 02.26: "A place where one change has wide effects. In the lockmark, the larger red node at bottom right stands for it."
- CP-S9: colophon and the four-dot row explained at first use; "candidate lines" gone; "fairness kit" defined in Rule 01.23's text; "masterbrand" and "trust mark" gone from 01.24's why.
- CP-S10: the contrasting pairs in 01.14's, 02.16's and 02.18's whys rewritten; the legend reads "Illustrative: invented for the example"; the founding line and checklist captions now state facts; the hidden actors in 01.17, 01.23 and 01.24 named ("the officials we ask readers to contact", "Name opponents by office or role").
- CP-S11: Rule 01.9 counts within one unit (a chapter, a report or a month of newsletter issues). Rule 01.10 names the four regions, and its plate and the log carry a region for every example. Ohio's and Pennsylvania's minimum wage floors, from atlas issue I104, give the chapter real Midwest and Northeast cases, with their source line.
- CP-S16: the report in 01.24 is dated (March 2027); "Dispatch from the Front" is described as our fifth edition's series name, with no Illustrative label, since it is real; in 01.15 the label sits beside the invented headline only.
- CP-S17: Alder County appears in no named state anywhere in 01 or 02.
- CP-S18 and D2-256: H10's source line prints "Each margin is the leading party's lead, in percentage points of all presidential votes"; the build applies it to the approved text and fails if that text changes.
- RP-S1: Rule 01.20's headline is "Democratic voters & Republican voters on a stock trading ban.", a pair of people joined through what they agree on, as Rule 01.19 asks; Rule 02.27 now sends pairs of people to Rules 01.19 and 01.20.
- RP-S9: the Senate line now speaks in our voice; what was checked, and where, waits for round two.
- CP-S8 (my part): Dispatch spelled as Rule 02.26 has it; backyard cottages glossed once as "an accessory dwelling unit", and the tracker is the Backyard Cottages Tracker.

**Decisions**
- DR-102 in Rule 01.24: "When we type a partner's name in our own copy, its ampersand becomes “and”, and the partner's logo stays as the partner draws it." Its builders note adds that a piece made with a partner goes to Dustin, or an editor he names, before it prints or posts, and that the host's name leads.
- DR-100: no editor's disclosure anywhere in 01 or 02. The only disclosure left is the position piece's, under D2-257.

### Held for round two (placeholders here only)

- H.R. 7008's grade and scope from the research lead's primary records. The wording now follows DR-98; round two sizes it to what the bill text supports, and fills the bill's coalition row in the rotation log.
- Rule 01.5's state limits (Mississippi, Illinois, Florida) and the 23-state count, with the full source line the research lead gives.
- The Senate vote line in our own voice, in the Track piece, Rule 02.25 and both chapters' sources.
- Rules 01.11, 01.13 and 01.16 against the research lead's checks: who drew each map and when, how many states elect utility commissioners, and how NBER and EPI describe their authors.
- DR-99: Rule 02.25's first row still holds the 23-states line until the research lead names an atlas mechanism.
- Rules 01.6 and 01.8: the photograph placeholders stay until the research lead's public-domain photographs clear, or both rules move to chapter 16.

### Declined or changed

- BE-M1's two follow-ons are not mine: the V7.1 issue list (DC-08) is the main session's, and chart S01 waits for Phase 3 under DR-98.
- C-S6, changed: the craft report asked every specimen to carry a width. I gave widths to the ten kinds of plate that show a phone page and let page text flow, as the brief allows. Fixed 480 and 600 px plates sent 45 of my plates sideways on a 390 px phone in a trial build; now none of my flowing plates scrolls at 1440, 1024 or 390 px.
- C-S6, the tile map: the coordinator reported its labels under 13 px at 390 and 360 px once the phone mat took 16 px each side. The tiles are now 24 px with 2 px gaps (312 px across) and the plate's side padding is 8 px on phones, so the map stays at true size with 13 px labels at both widths.
- Rule 01.9 no longer names Massachusetts. The rule applies the same limit to every state, which keeps DC-06's intent; the civic review found no reason on the page for the name. The failure plate keeps its Massachusetts tally.

### Routine calls, as proposed decision lines

- D2-xxx | Both sides of a vote, and every party, take the party mark ink with names printed; solid and outline in the same ink where sides must be told apart at a glance (Rules 01.1 and 01.2) | One standard under DR-48, DR-58 and DR-93, matching Rule 05.7
- D2-xxx | "Act · How to take part" is one content label and takes nothing after it | It holds its own middle dot; a third part would break D2-250's "at most one more part"
- D2-xxx | Only "Our position" takes the filled Charcoal label; the other labels are set in the label style, with the second part in the secondary text ink | The one kind that argues is seen before the headline (Rule 01.23)
- D2-xxx | The editor's phone pages are 360 px wide with 16 px margins, as chapter 05's are; reference sheets, lines, headlines, charts and the writing pairs flow, at the D2-254 phone floor below 48em and the desktop ceiling from 48em | C-S6 where width is the lesson; no sideways scrolling elsewhere
- D2-xxx | Hinge headline plates set H3 at 26 px on phones and the section style at 44 px from 48em, with B from the 16 px and 24 px masters | Rule 04.3's master table; at 44 px a headline ran to six lines at 390 px
- D2-xxx | Rule 01.20's correct headline is a pair of people joined through what they agree on, and Rule 02.27 sends pairs of people to Rules 01.19 and 01.20 | RP-S1; the two rules no longer disagree
- D2-xxx | Rule 01.9 counts within one unit and names no state | CP-S11
- D2-xxx | Rule 01.10 and the rotation log carry a region; Ohio's and Pennsylvania's minimum wage floors (atlas I104) are the Midwest and Northeast cases | CP-S11, from a sourced atlas record
- D2-xxx | The rotation log keeps the May 2023 survey and H.R. 7008 as two rows | DR-98
- D2-xxx | Rule 01.12's failure row is about town library hours in place of open primaries | Keeps chapter 01 clear of the subjects of the editor's campaigns, in DR-99's spirit
- D2-xxx | Chapter 02 runs in seven groups: the five teaching groups, house rules, and our lines and words | Every rule sits in a group in the shell's index
- D2-xxx | W01's and W02's approved terms print in their rule text, and their failure cards name the fault | CP-M3, with no approved word lost
- D2-xxx | The writing section's deck, third paragraph, scope, legend and sources note sit in one readable extra, "How Oath & Action writes"; its index sentence retires, since the shell's index does that job | C-S11
- D2-xxx | The failure band "Failure case: do not publish" is a Charcoal label inside the stage | BE-S4, with no red on a failure that names parties

### Questions for Dustin

None that a round one fix needs. Round two may bring one on H.R. 7008, once the research lead reports what the primary records support.

### For the main session and the other makers

- At 390 px the phone mat leaves the stage 358 px, so every 360 px phone page scrolls its frame by 2 px: chapter 05's and ten of mine. A 15 px phone mat, or a 358 px allowance in the shell, would let them sit whole.
- Rule 08.8 should point to Rule 01.21 for the kicker's words, as D2-250 asks; Rule 01.21 points back to 08.8 for the grid and icon.

### Tested

- My build (`python3 -I work/build/scripts/phase-2/guide_editor_build.py`): every check passes. New checks: no decision code, internal code or studio word in reader text or alt text (D2-253's list); no landmark or article element in a specimen; every font size on the D2-254 table and none written as a fluid size by hand; no Illustrative label but the shell's. A planted test caught all seven faults I planted (a decision code, V5, "Phase 2", "the studio" in an alt, an article element, 1.125rem and the old label class) and the clean build caught none.
- Equal length by script: Rule 01.11's two cases at 23 words; Rule 01.16's two readings at 24 words.
- Chapter 01 against its own Rule 01.9: 15 examples; the largest domains supply three each, under one in four; Texas, California, Ohio and Pennsylvania supply one each.
- `python3 -I work/build/scripts/phase-2/guide_build.py`: 0 warnings.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px: PASS, 0 failures across 99 rules, 229 specimens and 694 same-page links, with axe-core 4.10.2. This run includes the other makers' finished work. My exemptions are the eight labeled failure plates the manifest marks (01.1 to 01.5, 01.18, 02.22 and 02.24), each for red or contrast.
- Groups on the built page: 13 group blocks (6 in 01, 7 in 02), each linked twice, from the rule index and from "In this chapter".
- Frames by script at 1440, 1024 and 390 px: none of my flowing plates scrolls; at 390 px only my ten kinds of 360 px phone page scroll, by 2 px.
- By eye in Playwright Chromium at 1440 px: chapter 01's head and rule index, the words key, the pieces, Rules 01.1 to 01.5 (both plates), 01.6's failure, 01.7, 01.9 to 01.12, 01.15, 01.16, 01.18 to 01.21, 01.24, chapter 02's opening extra and group block, 02.1's pair and fault, 02.22 (house table and failure), 02.23 to 02.27. At 390 px: the pieces, 02.3's pair, 02.24, 01.20, 01.21 and 02.27.
- A script scan of my reader text and alts for "review", "4.2", "Edition 05", "V5", "studio", "Gate", "eyebrow", "The Dispatch", "Accessory", "disclos", "Yes on 3", "Veterans", "stock trading ban", "Stock Trading Ban", the em dash and "not", each hit read by hand.

### Not tested

- The facts round two checks: H.R. 7008's contents and votes, the Texas and California map details, the state initiative limits, the utility commission count and the NBER and EPI self-descriptions.
- Ohio's and Pennsylvania's minimum wages beyond the atlas's record of the Labor Department's table (snapshot of October 15, 2026). I did not open the Labor Department page.
- Every plate by eye: about 45 of my 111 plates at 1440 px and 7 at 390 px; 1024 and 360 px by script only.
- Screen readers, browsers other than Chromium, forced colors, print and 200 percent zoom.
- How the copy sounds to real readers.

### Change log, fix pass round one

Modified:
- `work/build/scripts/phase-2/guide_editor_common.py`, `guide_editor_ch01.py`, `guide_editor_ch02.py`, `guide_editor_build.py`
- `work/build/guide/chapters/01-purpose.json`, `work/build/guide/chapters/02-voice.json` (rewritten by the build)
- `work/build/guide/specimens/manifest-editor.json` and every `s-01-*` and `s-02-*` specimen (rewritten by the build)
- `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report and its check results, regenerated by `guide_build.py` and `guide_check.js`
- This file

Created: `work/build/guide/specimens/s-01-words.html`, `s-02-about.html`.

Deleted by the build: `work/build/guide/specimens/s-02-index.html`, `s-02-group-1.html` to `s-02-group-5.html`.

Nothing in `source/`, `work/ledger/`, the masters or another maker's files was touched, and nothing was committed.

## Fix pass, round two

November 6, 2026, under the fix pass brief's "Round two" and the main session's round-two message. I applied the research lead's report (`work/handoffs/phase-2/20261106_Stage-A-Fix-Pass-Research.md`) to everything I held, placed the photographs, and copy edited all eight chapters. Copy in chapters 03 to 08 changed only in the owners' build scripts, which I reran; no measurement, token, rule ID or locked line changed. I committed nothing.

### Research applied

- **H.R. 7008 (Documented in the bill texts and the two chambers' records).** DR-98's wording stands, and the report confirms it against the House-passed text. The Track piece's source line now cites the House Clerk's Roll Call 280 and the Congressional Record for Senate Vote 253, page S5199, and ends "Ending debate needs three-fifths of the Senate, 60 votes." Its second stage reads, in our own voice, "A Senate vote to end debate on taking it up got 53 votes, short of the 60 it needed." Rule 02.25's structure row keeps DR-98's first-mention wording and takes the Record as its source. "We could not open the Senate's own page" is gone from both chapters. The rotation log's row for the bill now holds the record's party split, in one form for both chambers.
- **Rule 01.5.** The source line is the report's: Ballotpedia, marked secondary, with Mississippi's May 14, 2021 ruling and Florida's and Illinois's limits. The map, its key and its title stay as drawn, which the report says hold.
- **Rule 01.11.** Both cases take the report's 22-word sentences, the same verb and the majority as the actor in both. The source line now cites the Texas bill history, California's Statement of Vote and the California court's January 14, 2026 order, and says the five-seat aims are each side's stated goals. The caption says why the last clauses differ: Texas's map became law with the governor's signature, and California's needed an amendment only voters could approve.
- **Rule 01.13.** The why already said "vote out its members or the official who appointed them", as the report proposes. The chapter states no count of elected commissions, so no new source line was needed.
- **Rule 01.16.** Both readings take the report's wording, 24 words each, with the verb "find" and each holder by role and affiliation: "Economists at Harvard University" and "Economists at the Economic Policy Institute". The first now covers typical and average pay, as the paper's abstract does. The source line is the report's.
- **Rule 02.25, row one (DR-99).** "Our democracy is broken." now becomes connection L50 in the report's words, "Few voters leave their own party's candidate over an undemocratic stand, so officials who take one face little threat of losing office.", graded well supported, with its source line. The loop's safe-seat line stays out, so the row touches no primaries, ranked-choice voting or Massachusetts Question 3, which concerns primaries. The four row labels now name the four kinds the rule lists: how the system works, the office that decides, a next step and the structure; the rule text says "how the system works" where it said "the rule".
- **Photographs (DR-101).** Rule 01.6 shows the Rosa Parks photograph from the Capitol Rotunda (rights ledger pho-01), cropped to 5:3 from the top so the walls and the public stay and the Architect of the Capitol's mark at lower right falls outside. Its caption is the record's, naming who, what, where and when with the credit; the plate's caption now names that event, since no photograph of the H.R. 7008 vote day exists. Rule 01.8 shows the Zianno photograph from the Lake Isabella public meeting (pho-04), cropped to 3:2, with the record's caption. I chose it over the Menniti frame because the named official faces the camera, so the caption's "who" is the person a reader sees, and the residents, whom the record does not name, face away. The failure plate shows the same photograph with "Democracy in action.", labeled Illustrative beside that invented caption. Both rules gained specifications for the photograph, the crop and the caption, and list the file. The shell embeds both files as it embeds other repository assets; the page grew from 4.31 to 6.05 MB.
- **Rotation (Rule 01.9).** The two photographs are examples, so the log holds 17: the largest domain, Congress, agencies and public services, supplies four, under one in four (4.25); California supplies two, under one in five. Rule 01.10's plate lists both under federal.

### Copy edit, all eight chapters

I read every rule, why, caption, specification and builders note of chapters 03 to 08 as dumped from the chapter files, and scanned every specimen's visible text and alt in all eight chapters and the proofs for the patterns chapter 02 removes. The ten cross-chapter issues in my stage A notes now stand as follows:

1. Decision codes in reader text: none left; the check's codes test passes.
2. Bare lockup codes: named at first use, in Rule 03.2 ("L1, the wordmark alone", "L3, the wordmark with the lockmark", "L2, the stacked lockup", "L8, the monogram") and in Rule 08.2 ("L3, the masthead lockup, and L6, the editorial signature").
3. "Atlas V7": none on the page.
4. Corrective negation: 04.3's builders note was fixed in round one; 06.3's now reads "draw it a phone version with its own label positions".
5. Rule titles: every title is an instruction, after round one.
6. Kickers: one grammar (D2-250). One clash remained: the same kind of Dispatch story took "Tracker · Dispatch" in Rule 01.15 and "Report · Dispatch" in Rule 08.8. Both now read "Report · Dispatch", and Rule 01.21 defines Report as "What the record shows about a decision, from a story in a series such as Dispatch to a numbered study".
7. Hinge divider geometry: one, after DR-96.
8. Rules that should cite each other: 06.5 cites H07; 04.3 cites 02.27 and 01.18 to 01.20; 02.27 cites 01.18 to 01.20 and 04.3.
9. `s-05-pairs` contrast: passes.
10. Shell classes reaching into specimens: the engineer's; I renamed mine in round one.

Other edits, with the plain-language items:
- CP-S2: the editions keep one name each. Prose now writes a contrast ratio as "13.29 to 1", as chapter 05 does, in Rules 03.5 (why and specifications), 04.7 (why and failure caption) and 08.9 (why and failure caption). Tables and specimens keep "13.29:1" as data.
- CP-S8: "Verdigris, a muted green" in chapter 01's words key, as chapter 05's intro says it; "backyard cottages" glossed the same way in Rule 01.22 and the letterhead proof.
- CP-S9: Rule 08.8 now explains the Civic Line at first use: "a topic icon from the Civic Line, our set of topic symbols in chapter 10". Breakpoint, em, Dim Newsprint, lockup, x, rem, OKLab, tracking and widow were already defined at first use.
- CP-S10: two landing lines rewritten (04.6's why now ends "With no words on it, the badge marks where a piece ends and claims nothing more."; 08.4's why ends "With one code per grid, chosen in a fixed order, a reader always knows which code a grid shows."); "just over" in 03.5 became "a little over" (W17); four passive sentences now name who acts (03.4's why, 05.2's roles caption, chapter 01's words key caption and chapter 02's brand lines caption).
- Rule 02.25's mechanism table no longer narrows its first column on phones.

### For the creative director (meaning or measurement, left as they are)

1. **B's master ranges disagree.** Rules 04.1 and 04.6 place the 16 px master from 16 to 23 px and the 24 px master from 24 to 47 px; Rule 04.3's specifications say "16 px master under 22 px capitals, 24 px master to 46 px". A B 22 or 23 px tall gets a different master under each. This is a measurement, so the identity designer should rule.
2. **Scrolling frames.** Rule 07.6's builders note asks for `role="region"` on a frame that scrolls; the guide's own shell now names its frames as groups, to keep 83 same-named regions out of the landmark list (AX-S3). Both are defensible on a site; the guide should teach one.
3. **Report as a label.** I widened Report to cover a story in a series so Rules 01.15 and 08.8 agree. If the creative director prefers Tracker for series stories, both specimens change together.
4. **Rule 01.5's map.** The report offers a fourth fill for amendment-only states (Florida and Illinois). I kept three fills and put the limits in the source line.
5. **360 px phone pages** still scroll their frames by 2 px at 390 px (chapter 05's and ten of mine).
6. **The photographs** are Wikimedia's 1,920 px renditions; the research lead asks that the originals be fetched and checked against their SHA-1 before print.

### Routine calls, as proposed decision lines

- D2-xxx | Rule 01.8 shows the Zianno frame from the Lake Isabella meeting | The named official faces the camera, and the unnamed residents face away
- D2-xxx | Photographs are cropped in the specimen's CSS from the delivered files, with no new image files | Each file stays as the rights ledger records it, so print can swap in the original
- D2-xxx | Rule 01.8's failure shows the same photograph with an invented caption, labeled Illustrative beside the caption | The fault is the caption alone
- D2-xxx | Rule 02.25 labels its four answers as how the system works, the office that decides, a next step and the structure | Row one is now a mechanism (DR-99)
- D2-xxx | A Dispatch story's kicker is "Report · Dispatch" in every chapter, and Rule 01.21's Report covers what the record shows about a decision | One label for one kind of piece
- D2-xxx | Prose writes contrast ratios as "13.29 to 1"; tables and specimens may print "13.29:1" | One form in sentences, compact figures in data
- D2-xxx | The Rosa Parks and Lake Isabella photographs join chapter 01's rotation log | Every example a reader meets is counted

### Tested

- `guide_editor_build.py`: every check passes, including Rule 01.11's two cases at 22 words each and Rule 01.16's two readings at 24 words each, by script.
- `stage_a_identity_build.py` and the three-step `stage_a_systems_build.py` (probe, capture, final) rerun after my edits. Before editing, a rerun of each changed nothing but the measurement file's timestamp, so the diffs after it are my copy edits alone; I read every changed line in the chapter files' word diff.
- `python3 -I work/build/scripts/phase-2/guide_build.py`: 0 warnings, 229 specimens.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px, on the final build: PASS, 0 failures across 99 rules, 229 specimens and 694 same-page links, with axe-core 4.10.2. An earlier full run, before my last fix to the mechanism table's phone layout, also passed.
- By eye in Playwright Chromium: Rules 01.6 and 01.8 (both plates) at 1440 and 390 px, with the photographs rendered and the agency's mark cropped out of the Rotunda frame (checked at 2x the plate's corner); Rules 01.11, 01.16 and 02.25 at 1440 and 390 px; Rules 03.2 and 08.8 at 1440 and 390 px; Rules 06.3 and 01.15 at 1440 px.
- A script scan of every chapter's text and every specimen's text and alt for em dashes, the listed fillers and corporate verbs, ", while", "rather than", "Here is", exclamation points, straight quotes, edition codes, "eyebrow", "diverging pair", "Civic Line", "Atlas V7" and passive verbs; I read each hit.

### Not tested

- The research lead's sources; I used the report's sentences and source lines as written.
- The photographs at print size, and the originals they stand in for.
- Chapters 03 to 08 by eye beyond the rules listed above; I read their text in full but looked at few of their plates.
- Screen readers, other browsers and real readers.

### Change log, round two

Modified:
- `work/build/scripts/phase-2/guide_editor_ch01.py`, `guide_editor_ch02.py`
- `work/build/scripts/phase-2/stage_a_identity_chapters.py` (copy in Rules 03.2, 03.4, 03.5, 04.6, 04.7, 08.2, 08.4, 08.8 and 08.9)
- `work/build/scripts/phase-2/stage_a_systems_ch05.py` (the roles caption) and `stage_a_systems_ch06.py` (Rule 06.3's builders note)
- Regenerated by those scripts: `work/build/guide/chapters/01-purpose.json` to `08-signal-grid.json` where copy changed (01, 02, 03, 04, 05, 06, 08), the `s-01-*`, `s-02-*`, `s-03-*`, `s-04-*`, `s-05-*` to `s-08-*` specimens and their manifests, and `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json` (timestamp only)
- `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report and its check results
- This file

Created: none. The photographs are the research lead's files, read in place.
