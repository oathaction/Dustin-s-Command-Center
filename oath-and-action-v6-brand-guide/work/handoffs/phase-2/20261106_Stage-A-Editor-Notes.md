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
