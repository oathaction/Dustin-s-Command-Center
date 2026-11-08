# Apply pass, round one: editor's notes, chapters 01 Purpose and 02 Voice

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the editor (`oa-editor`) under `work/handoffs/phase-2/20261107_Apply-Pass-Brief.md`, section "Editor". I changed only my own files: chapters 01 and 02, their specimens, `manifest-editor.json` and the four `guide_editor_*.py` scripts. I committed nothing; the main session's snapshot commits hold the work in progress.

Two inputs wait for the research lead, as the main session asked: the 2020 court example (atlas issue I155) and the step states of the H.R. 7008 card. Both drop in without any other wording changing. "Round two" below says exactly how.

## What I did, item by item

### 1. Chapter 01, nonpartisan wording (DR-125)

- **Opening.** A13's paragraph is the opening's second paragraph, word for word, right after the first paragraph names us "a nonpartisan publication". The shell's content contract allows two paragraphs, so the hinge paragraph moved, unchanged, to the top of the hinge figure (`s-01-hinge-lines`), where it now introduces the table it explains.
- **Rule 01.11.** A13's added sentence is the rule's second paragraph, and A13's reason replaces the old one, both verbatim. Two edits of my own follow from DR-93:
  - Title. Original: "When majorities of both parties use a mechanism, show a case from each." Revision: "Show a case from each party that uses a mechanism, and report the counts as the record gives them." Reason: the old title taught only the even case, and a reader scanning the index would learn "always show both sides".
  - Failure caption. Original: "With one party’s case alone, the loop reads as a charge against that party, and a reader who votes for it stops at the first line." Revision: "The record holds a case from each party, so a piece that shows Texas alone drops a finding, and the loop reads as a charge against one party." Reason: under DR-93 the fault is the dropped finding, and looking uneven is no fault in itself.
  - For builders now says to count the atlas's case records by party and print the counts when one party leads.
- **Rule 01.20.** The reason now reads "Reporting agreement is the one case where naming the sides in a hinge headline helps a reader."
- **Rule 01.12.** The reason now reads "A log turns the spread of examples into counts anyone can check". The word "balance" no longer appears in chapter 01's text, and the build fails if it returns.
- **Slot for the example.** The example will print as an extra after Rule 01.11, labeled "A finding that falls on one side": the grade, the research lead's sentences and source line exactly as written, and my caption, "The lines name who acted and what the record shows, in words sized to the grade, and they add no case from another party to even the count, as Rule 01.11 asks." It also adds a row to the rotation log. Until the research arrives, nothing prints and nothing points to it. I placed it after Rule 01.11 because that is where a writer learns to report a one-sided record, and it keeps a charged example off the chapter's first screen.

### 2. Chapter 01, pillars and kickers (DR-111, DR-112)

- **Pillars figure (`s-01-pillars`).** It now opens with the pillar row: CL-019 Explain, CL-020 Track, CL-021 Connect and CL-022 Act at 48 px in one color, each word beside its icon, joined by arrows. It closes with the compact row at 24 px on a page that serves Track: Track's word bold and underlined, every icon one color, since red starts at 48 px. Under 48em the 48 px row stacks in one column with downward arrows. At 1,024 px it wraps after Track's arrow, which is what the creative director's Board 6 review asked for. The icons are the black masters drawn inline with their geometry untouched; their ink comes through `currentColor`, and they are hidden from screen readers because the word beside each one names it.
- **Words key.** Pillars: "Each pillar has an icon, set with its word beside it." Signature red: "The red inside our marks and icons, such as the wordmark’s ampersand and the lockmark’s lever." This matches Rule 05.3, which already counts a row's current icon red as signature red.
- **Rule 01.21.** A second paragraph: "Set the kicker in words. The one picture it may hold is a topic icon from the Civic Line, our set of symbols in chapter 10, placed directly before the topic’s own word. Pillar icons belong to the pillar row, section openers and tiles, and never enter a kicker." The reason, the specifications (topic icon 24 px, one color, 8 px before its word; never a pillar icon, the lockmark, or an icon beside a label or a series name), For builders and the related chapters (10 and 13) follow it. The old pointer to Rule 08.8 is gone.
  - The correct plate shows the one icon a kicker may carry: "Analysis · Productivity" with CL-055 Productivity directly before its word. The failure plate adds a fourth kicker: the same Analysis kicker led by the Explain pillar icon.
- **Retired grid copy.** None left in chapters 01 and 02. Rule 01.1's card was labeled Tracker and showed one committee vote with no steps, which DR-109 no longer allows on a tracker; it is now "Report · State senate", so its lesson stays on color.

### 3. Chapter 01, the tracker card

The Track piece is rebuilt for numbered steps (DR-109), drawn exactly as chapter 11 sets them. I read `apply_systems_ch11.py` and matched it: Rule 11.7's 24 px circles for a story card, 13 px numbers, Rule 11.4's take-part disc with its 1 px keyline inside the edge, and Rule 11.3's words for a stop. The card uses `STEPS_FEDERAL`, the six steps with step 6 named President (DR-128). Under the marks it prints a key of the six names, so "President" shows, and it gives a screen reader every step with its state. The status line reads "Step n of 6: Name." with the vote sentence after it. Both provisions stay in the deck at first mention (DR-98).

Until `HR7008_STEPS` arrives, the card prints no marks. It prints the two documented votes in words, so the page stays true. I tested the full card with provisional values in a scratch build only (see Tested).

### 4. Chapter 02

- **Rule 02.23 and `s-02-lines` (DR-122).** The record now lists all six retired fifth-edition lines. DR-122's two survive in our copy only as their first 50 characters, so each is quoted to the end of its last whole sentence with an ellipsis, and one line says "Our copy of that edition keeps only the openings of the last two." The rule gains "The retired lines under the table appear nowhere else." The Pillars row's places now read "Navigation, and the pillar row on section openers and tiles, where each pillar’s icon sits beside its word". The old wording named the four-dot row and the grid's corners.
- **Rule 02.25, last row (DR-126).** "H.R. 7008, the Stop Insider Trading Act, would bar members of Congress, their spouses and dependent children from buying individual stocks, and would require photo ID to vote in federal elections, and it needed 60 votes to move forward in the Senate and got 53, all from Republicans; 45 Democrats and two independents voted no." DR-126's quoted wording opens with "It", and the decision also asks for the count "in the same sentence as both provisions". I joined the two with ", and", which keeps Dustin's words unchanged from "needed" to "voted no" and keeps DR-98's first-mention wording too. One sentence also means no quotation of the count can leave the photo ID provision behind, which was A14's reason. The source line: "Sources: Congressional Record, Senate, Vote 253, cloture on the motion to proceed to H.R. 7008, page S5199, September 30, 2026, United States; party labels from the congress-legislators project’s roster of current members of Congress, a secondary source. Retrieved November 6, 2026. The Record lists each senator’s vote by name, and ending debate needs three-fifths of the Senate, 60 votes."
- **`s-02-14-pair`.** W14's approved source line named the fifth edition's chapter "chapter 07 the Signal Grid". It now reads "Our brand guide, fifth edition, chapter 07, figure caption" (D2-326). My script makes this change the way it applies H10's erratum, and the approved content file is untouched. The before and after are unchanged.
- **`s-02-26-correct`.** The "Signal Grid" term leaves the list. Lockmark, originally "The three by three grid of nodes beside the wordmark", now reads "Our mark of nine nodes in a three by three grid, set in four fixed places: the masthead, page headers, footers and the sign-off", since only the masthead sets it beside the wordmark.
- **DR-55's old clause (DR-124).** It appears nowhere in chapters 01 or 02. A12's card touches Rule 01.16, so I gave 01.16 the one-standard guard: two readings only when the grade is contested, "and no piece adds a second reading to even the score". Its reason and For builders follow.

### 5. Build

Everything is built by `guide_editor_build.py` and its chapter modules. No generated HTML was edited by hand.

## Contradictions found

1. **The Civic Line's Congress icon and Rule 01.6.** CL-025 Congress draws a capitol dome over columns, and I checked it by eye at 64 px. Rule 01.6 keeps domes and columns out of icons. I had put it in the Track kicker, then took it out. The build now fails if CL-025 appears in my chapters. Chapter 10 (stage B) has to settle it; see question 2.
2. **DR-126's wording against its own description.** It is resolved by the joined sentence above.
3. **Rule 01.11's new sentence and Rule 01.13.** 01.11 now says "with the counts, as Rule 01.13 asks", but 01.13 asked for counts only for a party-line vote. 01.13 now reads: "Name a party only when party is part of the finding, such as a party-line vote or a record that shows one party doing more of something, and give the count and its source." Its title follows.
4. **Rule 01.16 and DR-93.** "Show both readings" could be read as a reason to add a counter-reading. Resolved by the guard above.
5. **Rule 01.1's "Tracker" card against DR-109.** Resolved: it is now a Report.
6. **Chapter 09's title against DR-111.** The guide build lists chapter 09 as "Pillar marks", and DR-111 says "pillar icons". My chapters say "pillar icons" and cite chapter 09 by number. I recommend the engineer retitle chapter 09 "Pillar icons".
7. **Board 6's pillar notes put the pillar icon in kickers.** DR-112 settled the opposite, and every kicker I own follows DR-112.
8. **Chapter 01's opening against the content contract.** A13's paragraph made three paragraphs; resolved by moving the hinge paragraph into its figure.

## Terms defined

- Civic Line, at first use in chapter 01: "our set of symbols" (pillars caption), and in Rule 01.21 with its chapter.
- Pillar icons, in the words key and the pillars figure.
- Lockmark, redefined by its four places in Rule 02.26.
- Evidence grade appears in A13's paragraph one screen before the words key defines it. I left A13's wording as approved; the words key follows directly.

## Routine calls, as proposed decision lines

- D2-xxx | A13's paragraph is chapter 01's second opening paragraph, and the hinge paragraph opens the hinge figure | The content contract allows two paragraphs, and the hinge text then sits above the table it explains
- D2-xxx | The 2020 example prints as an extra after Rule 01.11, and only once the research lead's check holds | It shows Rule 01.11's added sentence where a writer learns it, off the chapter's first screen
- D2-xxx | Rule 01.11's title is "Show a case from each party that uses a mechanism, and report the counts as the record gives them." | The old title taught only the even case (DR-93)
- D2-xxx | Rule 01.11's failure names its fault as a dropped finding | DR-93: dropping a documented case is the fault
- D2-xxx | Rule 01.13 names a party when party is part of the finding, a one-sided record included | Rule 01.11's new sentence relies on 01.13's counts (A13)
- D2-xxx | Rule 01.16 gives two readings only to a contested grade, and every other grade one reading | DR-93 and DR-124: no reading added to even the score
- D2-xxx | Rule 01.1's card is a Report | A card that reports one vote needs no tracker steps (DR-109), and its lesson stays on color
- D2-xxx | A kicker's topic icon is 24 px, one color, 8 px directly before the topic's word; Rule 01.21 shows CL-055 on "Analysis · Productivity" | DR-112, with an icon whose name is the kicker's word
- D2-xxx | CL-025 Congress stays out of chapters 01 and 02 | It draws a dome over columns, which Rule 01.6 keeps out of icons
- D2-xxx | The pillars figure opens with the 48 px pillar row, one color and no current pillar, and closes with the 24 px row with Track current | DR-111's underline shown where a current pillar exists; red only from 48 px
- D2-xxx | The 48 px pillar row stacks in one column under 48em, with downward arrows | The creative director's Board 6 review: the phone row dropped its arrow
- D2-xxx | Pillar and topic icons are inlined from the black masters, ink through currentColor, ids, title and desc dropped, hidden from assistive technology | Geometry untouched, no literal colors, and the word carries the meaning
- D2-xxx | The H.R. 7008 card draws Rule 11.7's 24 px circles across 336 px, with a key of the six step names under them | A story card at a phone's text width, and the key shows "President" (DR-128)
- D2-xxx | Until the research lead's mapping arrives, the card prints the two documented votes in words and no step marks | The page stays true while the states wait
- D2-xxx | Rule 02.25's count joins the provisions sentence with ", and it needed" | Keeps DR-98's and DR-126's wording and puts the count in one sentence with both provisions
- D2-xxx | Rule 02.25's source line names the Congressional Record and the congress-legislators roster as a secondary source | DR-126, from the research lead's November 6 report
- D2-xxx | W14's source reads "chapter 07, figure caption" | D2-326; the approved content file stays as Board 5 approved it
- D2-xxx | The retired record lists six lines and quotes DR-122's two to the end of their last whole sentence | Our copy holds only their first 50 characters
- D2-xxx | Rule 02.26 drops the grid's coding term and defines the lockmark by its four places | D2-326, DR-110
- D2-xxx | The pieces figure drops its own side padding from 48em, so two 340 px cards share a row at 1,440 px | The stage's inner width, 675 px, had put one card per row

## Questions for Dustin

1. **Rule 01.11's approved reason opens two sentences with "Where".** That is the parallel run W13 removes. *Recommendation:* approve one sentence with the same meaning: "A case from each party, told the same way, puts a mechanism both parties use in front of the reader, and where the record shows one side doing more, the finding stands as the record shows it." It prints as approved until you answer.
2. **The Civic Line's Congress icon draws a capitol dome over columns, which Rule 01.6 keeps out of icons.** This is for chapter 10 at stage B. *Recommendation:* keep Rule 01.6, and name Congress in words wherever a topic icon would sit until a drawing without the dome is made and approved.

## For the main session and the other owners

- Round two inputs, in `guide_editor_ch01.py`:
  - `UNEVEN = dict(grade=..., lines=[...], source=..., domain=..., state=..., region=..., level=..., alt_note="")`. The extra after Rule 01.11 and its rotation log row then build themselves. Rule 01.10's list of examples by level is written by hand, so I add the example there in round two. If the research lead recommends holding the example, nothing changes, and DR-125's wording stands alone.
  - `HR7008_STEPS` (six pairs of state and words), `HR7008_STATUS` (the line after the step) and `HR7008_AS_OF`. If the research lead's source lines cover the introduction and committee steps, `SRC_STOCK_VOTES` takes them too.
- Engineer: retitle chapter 09 "Pillar icons" (contradiction 6).
- Chapter 09, at stage B: the creative director's open items for the pillar icons still stand: pixel-fit 16 and 24 px masters, and Act set larger in placement. I did not scale Act.
- Identity designer: chapter 08's opening keeps "Democracy has a structure.", so the brand lines table still places it in chapter 08 and on the About page.

## Tested

- `python3 -I work/build/scripts/phase-2/guide_editor_build.py`: every check passes, the older ones and the new apply-pass checks. Each new check is named for its decision: retired words and old chapter 08 rule numbers; A13's four strings, verbatim; "balance" gone from chapter 01; DR-98's first mention in both chapters; DR-126 in one sentence with both provisions and its source line's two parts; the six federal steps; no step named Governor; four pillar icons with their words; one underlined current pillar; red only on a current icon from 48 px; no pillar icon in a kicker; topic icon beside its own word; no CL-025.
- Planted faults, in memory, with the clean build as baseline: 14 of 14 caught (Signal Grid in a caption, "Stage 4 of 9", a "Rule 08.8" reference, A13 altered, "balance" restored, a pillar icon in a kicker, a topic icon beside the wrong word, a dome icon in a kicker, the Senate count split off, step 6 as Governor, no current pillar, red on a 24 px pillar icon, a retired line outside its record, a provision dropped from 02.25).
- Scratch builds, with provisional values that are layout tests and not research, written only to my scratchpad: the 2020 slot and the card in three variants (a skipped hearing with step 5 current; the take-part mark on step 5; a stop at step 4). `guide_build.py` built each with no warnings. I looked at the step row at twice size in all three; every state reads by shape.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`: 0 warnings, 100 rules, 232 specimens.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px, on the final build: PASS, 0 failures, 754 same-page links. My exemptions are the eight labeled failure plates as before.
- By eye in Playwright Chromium on the real page: chapter 01's opening text; Rule 01.11's text and reason at 1440 px; `s-02-lines` at 1440 px; `s-02-25-correct` and the Track card at 390 px; the pillar row at 1,024 px at twice size. In the provisional scratch page: `s-01-pillars`, `s-01-pieces`, `s-01-21-correct` and `-failure`, the 2020 slot and `s-01-hinge-lines` at 1440 and 390 px. None of my plates scrolls sideways at either width.
- A script listed every string in chapters 01 and 02 that changed since commit 3130c5b, with hits for em dashes, the listed words and negation patterns. I read every string. It found one fix: a filler word W17 lists, in "placed just before", now "placed directly before".
- Pattern count, by script and by my own read of every changed string, in my chapters' reader text and alt text: em dashes 0 (W21's is drawn as a rule); listed fillers and corporate verbs 0 outside W17, W18 and Rule 02.26, which name them; parallel runs 1, Rule 01.11's approved reason (question 1); rhetorical triplets 0. A13's "adds, softens or drops" is a plain list of three acts, which W12 allows; hedges, throat-clearing openers, landing lines and slogan closers 0.

## Not tested

- The research lead's two checks: the step states and the 2020 example are not on the page.
- The congress-legislators roster itself. Rule 02.25's source line rests on the research lead's November 6 report.
- Screen readers, forced colors (my card has no forced-colors rules of its own, as chapter 11's lists do), Firefox, Safari, print, 200 percent zoom and real readers.
- At 1,024 and 360 px I looked only at the pillar row; the check covered the rest by script.

## Change log

Modified:
- `work/build/scripts/phase-2/guide_editor_common.py`: pillar icon map, Civic Line inline helper, pillar row and its style, topic icon in `kicker()`
- `work/build/scripts/phase-2/guide_editor_ch01.py`: the items above, and the round-two inputs `UNEVEN`, `HR7008_STEPS`, `HR7008_STATUS`, `HR7008_AS_OF`
- `work/build/scripts/phase-2/guide_editor_ch02.py`: the items above; `content()` applies H10's erratum and W14's source
- `work/build/scripts/phase-2/guide_editor_build.py`: the apply-pass checks
- Regenerated by the build: `work/build/guide/chapters/01-purpose.json`, `02-voice.json`, `work/build/guide/specimens/manifest-editor.json` and every `s-01-*` and `s-02-*` specimen. Every specimen's style block gained the kicker icon rules. Visible text or alt text changed in `s-01-1-correct`, `s-01-1-failure`, `s-01-21-correct`, `s-01-21-failure`, `s-01-hinge-lines`, `s-01-pieces`, `s-01-pillars`, `s-01-words`, `s-02-14-pair`, `s-02-25-correct`, `s-02-26-correct` and `s-02-lines`.
- Regenerated by the shared build and check: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report and its check results

Created: this file. No specimen was created or deleted; `s-01-uneven` appears only when the 2020 example arrives.

Not touched: `source/`, `work/ledger/`, the Civic Line masters (read only), any board, the reader check, and every other owner's files. Scratch builds, captures and the planted-fault script stay in my session scratchpad.

## Round two

November 7, 2026, under the brief's "Round two" section and the main session's round-two message. I applied the research lead's report (`work/handoffs/phase-2/20261107_Apply-Pass-Research.md`) and copy edited chapters 01 to 08, the identity proofs and chapter 11. Copy in other owners' chapters changed only in their build scripts, which I reran; no generated HTML was edited by hand. Before editing, I reran each owner's build untouched and it reproduced the committed outputs, apart from the letterhead PDF's creation time and the systems measurement file's timestamp. So every diff after that is mine. I committed nothing.

### What I changed

**1. The 2020 court example (DR-125, atlas issue I155), graded Documented.** It prints after Rule 01.11, labeled "A finding that falls on one side", with the research lead's four sentences and source line word for word. They carry the four corrections: the court's whole sentence ("never alleges that any ballot was fraudulent or cast by an illegal voter"), the court's own words for the relief ("block Pennsylvania's certified vote totals from taking effect"), the one Pennsylvania case the review says Trump's side won, and the authors in one form ("eight conservatives, among them two former U.S. senators and three former federal appeals judges"), with their own statement of party ties in the source line. The sentences name who acted, use record verbs and attribute the count and the finding to the review by name; no case from another party sits beside them. The example joins the rotation log (domain D10, Pennsylvania, all four regions in the review) and Rule 01.10's federal list. Rule 01.9 now counts 18 examples; no domain supplies more than four, and California and Pennsylvania supply two each.

**2. H.R. 7008's card, as of November 5, 2026.** The marks are chapter 11's own: the card imports `apply_systems_ch11.py` and draws with its `steps_svg()`, `status_words()`, `names("federal")`, `MARK_CSS` and `mark_vars()`. My round-one drawing functions are deleted. The circles are 24 px, as Rule 11.7 sets for a story card. Steps: 1 Filed, January 12, 2026; 2 Hearing, a slash; 3 Committee vote, January 14, 2026, 7 to 4; 4 First chamber, July 22, 2026, 232 to 198; 5 Second chamber, current; 6 President, ahead. The status line reads "Step 5 of 6: Second chamber. A Senate vote to end debate on taking it up got 53 votes on September 30, 2026, short of the 60 it needed, and the bill has stayed on the Senate’s calendar since." A second line gives what the slash means and how the bill got here: "Step 2 never happened, because the committee held no hearing on this bill. Its report cites only a hearing held November 19, 2025, before the bill was filed. The committee voted 7 to 4 on January 14, 2026, on a version without the photo ID section, and the House passed both provisions 232 to 198 on July 22, 2026." The source line is the research lead's replacement, word for word. The take-part line names no Senate date, as the report advises.

**3. First mentions of H.R. 7008.** Only chapters 01 and 02 mention the bill. Both first mentions (the Track card's deck and Rule 02.25's last row) now read "H.R. 7008, the Stop Insider Trading Act, as the House passed it, would bar ... and would require photo ID to vote in federal elections". Every later mention uses the tracker's or the act's name alone, and none describes the committee's text. Rule 02.25's sentence keeps DR-126's words from "it needed" to "voted no".

**4. Copy edit.** Chapters 05, 06 and 07 changed only in lines I read and kept (Rules 05.1, 05.4's failure caption, 06.8, and the related-chapter reasons). Rule 05.7 carries DR-124's wording exactly. The edits:

| Location | Original | Revision | Reason |
|---|---|---|---|
| Rule 03.1, rule | "though the capitals were cut from it" | "though we cut the capitals from it" | W02, name who acts |
| Rule 04.6, why | "the badge claims nothing more: our fifth edition put the reason plainly, “Seals ...”" | "the badge claims nothing more. Our fifth edition gave the reason: “Seals ...”" | Two sentences joined by a colon; "plainly" adds nothing |
| Rule 04.8, rule | "It takes the surface’s ink, never red. It stays clear of the text ..." | "It takes the surface’s ink, never red, and stays clear of the text ..." | W13, two sentences in a row on one frame |
| Chapter 08, opening | "and a series or a pillar is named in words" | "and words name a series or a pillar" | W02 |
| Rule 08.1, rule | "a 3 by 3 grid" | "a three by three grid" | H06, and Rule 02.26's own wording |
| Rule 08.3, rule | "a bill’s steps are numbered, as chapter 11 sets them; a series is named in words in the kicker (Rule 01.21); and a pillar takes ..." | "chapter 11 numbers a bill’s steps, the kicker names a series in words (Rule 01.21), and a pillar takes ..." | W02, two passives |
| Rule 08.3, specification "Patterns" | "None: the lockmark appears whole or not at all" | "None; the lockmark always appears whole" | W10, a matched pair |
| Rules 04.6, 08.2, 08.3, basis | "Dustin Cathcart’s ruling on the ... , November 7, 2026; Design judgment" | "Design judgment, approved by our founder and editor in November 2026" | One form for Dustin's rulings, as chapter 11 writes them |
| Rules 04.4 and 04.7, basis | "; Design judgment" | "; design judgment" | One capitalization after a semicolon, as elsewhere |
| Chapter 11, opening | "Status marks ... and utility icons for actions such as copy, filter and share join the chapter as their own rule groups once they are drawn." | "Status marks ... join the chapter as rule groups of their own once we draw them, and so do utility icons for actions such as copy, filter and share." | W14, a long subject before its verb; W02 |
| Rule 11.3, builders | "Keep three dates ...: the day it was signed, the day it took effect if that has passed, and the day it takes effect if that is ahead." | "Keep two dates ...: the day it was signed and the day it takes effect, written in the past tense once that day has passed." | The list counted one date twice |
| Rule 11.4, rule | "any step where the public is invited in" | "any step where the public can take part" | W02 |
| Rule 11.5, correct caption | "Five bills ...: one where you can take part, one waiting ..." | "Five bills ..., among them one where you can take part, one waiting ..." | The list names four of the five |
| Chapter 11, "The six steps" caption | "Step 6 is named for whoever signs the bill." | "Step 6 takes the name of whoever signs the bill." | W02 |
| Rule 01.9, tally line | "California supplies two examples, Pennsylvania supplies two examples, and ..." | "California and Pennsylvania supply two examples each, and ..." | W13; the generator now groups states that share a count |

Rule 01.11's approved reason stays exactly as Dustin approved it in DR-125. The dome on CL-025 waits for stage B; nothing changed for it.

**Build.** The step row is 288 px wide, 48 px to a step, so it fits the card's narrowest column (296 px at a 360 px screen) and never scales. My first run drew it at chapter 11's 324 px; at 390 and 360 px it shrank, its numbers fell under 13 px, and `guide_check.js` failed four times on that. The figure's own side padding is now 0 at every width.

### Routine calls, as proposed decision lines

- D2-xxx | Each first mention of H.R. 7008 reads "as the House passed it" before both provisions | The committee voted on the stock section alone, and DR-98's provisions are the House-passed text's
- D2-xxx | The Track card says in words why step 2 has a slash, and that the committee voted on a version without the photo ID section | DR-108 puts the words beside every state, and the marks alone could imply the committee's text held both provisions
- D2-xxx | The card draws its steps with chapter 11's `steps_svg()` and status words, imported from `apply_systems_ch11.py` | One drawing for every tracker, with no marks of the editor's own
- D2-xxx | The card's step row is 288 px, 48 px to a step, with 24 px circles | Rule 11.5's sixths and Rule 11.7's story-card size, at a width that never scales below 13 px numbers
- D2-xxx | The card dates itself "As of November 5, 2026" | The newest Congressional Record the research lead read
- D2-xxx | The 2020 example logs as domain D10, Pennsylvania, all four regions, federal | Atlas issue I155's domain; the court case is Pennsylvania's, and the review's six states span the four regions
- D2-xxx | Basis lines for Dustin's rulings read "Design judgment, approved by our founder and editor in November 2026" | One form across chapters 04, 08 and 11 (D2-253)

### Questions for Dustin

1. **Rule 01.11's reason opens two sentences with "Where".** That is the parallel run W13 removes. It prints exactly as you approved it in DR-125. *Recommendation:* approve one sentence with the same meaning: "A case from each party, told the same way, puts a mechanism both parties use in front of the reader, and where the record shows one side doing more, the finding stands as the record shows it."

### For the main session and the other owners

- **Chapter 11, step 2's meaning (systems designer).** The steps table says the committee "holds a public hearing, where anyone can speak or send written testimony", and Rule 11.1's reason says the hearing "is where the public is invited to speak". The research lead did not check how House and Senate committees take testimony and asks that the wording not be applied to a federal bill until someone does. Chapter 11 shows a federal bill (H.R. 3120) beside the table. I changed nothing in those lines, since I cannot check the fact either. *Recommendation:* once checked, scope the line to state bills, or give the federal case its own words.
- **Atlas V7.1 list.** Issue I155's summary and evidence note say the review found no evidence "in any of 64 cases"; the review records one case Trump's side won. Both lines should take the review's own words (research lead's note).
- **The card's committee vote by party** is in the report as an image the research lead did not read, so the card gives the count alone.

### Tested

- `python3 -I work/build/scripts/phase-2/guide_editor_build.py`: every check passes, with two new ones: each first mention carries "as the House passed it" with both provisions, and no sentence ties the committee to the photo ID section unless it says the committee's version lacked it.
- Planted faults: 16 of 16 caught, the 14 from round one and two new ones (a first mention without "as the House passed it"; a line that gives the committee's vote the photo ID section). The second plant first slipped past a check that read a 12-word window; the check now reads whole sentences, and it catches the plant.
- Each owner's build, rerun untouched before my edits: `stage_a_identity_build.py --pdf`, the systems pipeline (probe, capture in Chromium, final) and `apply_systems_ch11.py`. Each reproduced its committed outputs apart from two timestamps. After my edits I reran the identity build and `apply_systems_ch11.py` and read every changed line in the chapter files' word diff: only my edits.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`: 0 warnings, 9 chapter files, 100 rules, 233 specimens.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px, on the final build: PASS, 0 failures, 755 same-page links. The run before my last fix failed four times (the step numbers under 13 px at 390 and 360 px); that is fixed.
- By eye in Playwright Chromium: the Track card at 390 px and at 360 px at twice size; its step row at twice size at 1440 px; the 2020 example at 1440 px.
- The research lead's sentences, quotations and source lines against my output: copied from the report and compared as strings; the build checks the card's six step names and both provisions.
- A script listed every string in chapters 03 to 08, the proofs and chapter 11 that is new since commit 3130c5b, flagged em dashes, the listed words, negation, passives and "here is", and I read every string. A second script did the same for their specimens' visible text and alt text; I read every hit.

### Not tested

- The research lead's sources: I used the report's sentences, step dates and source lines as written.
- Specimens in chapters 03 to 08 and 11 by eye: I read their text and alts by script and looked at none of their plates in this round.
- Screen readers, forced colors, Firefox, Safari, print, 200 percent zoom and real readers.

### Change log, round two

Modified:
- `work/build/scripts/phase-2/guide_editor_common.py`, `guide_editor_ch01.py`, `guide_editor_ch02.py`, `guide_editor_build.py`
- `work/build/scripts/phase-2/stage_a_identity_chapters.py` (Rules 03.1, 04.6, 04.8, 08.1, 08.3, chapter 08's opening, five basis lines)
- `work/build/scripts/phase-2/apply_systems_ch11.py` (chapter 11's opening, Rules 11.3 and 11.4, two captions)
- Regenerated by those scripts: `work/build/guide/chapters/01-purpose.json`, `03-identity.json`, `04-ampersand.json`, `08-lockmark.json`, `11-icons.json`, `manifest-editor.json`, `s-01-9-correct`, `s-01-10-correct`, `s-01-12-correct`, `s-01-pieces`, `s-02-25-correct`, `s-proofs-letterhead` (timestamp only), `work/boards/phase-2/stage-a/proofs/20261107_Letterhead-Proof.pdf` (timestamp only) and `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json` (timestamp only)
- Regenerated by the shared build and check: the stage A chapters page, its build report, its check results and its captures
- This file

Created: `work/build/guide/specimens/s-01-uneven.html` (the 2020 example).

Not touched: `source/`, `work/ledger/`, the Civic Line masters, any board, the reader check. Nothing committed or pushed.

## Fix pass

November 7, 2026, under `work/handoffs/phase-2/20261107_Apply-Pass-Fix-Brief.md`, "Editor". I read all three reviews in full (`20261107_CD-Review-Of-Apply-Pass.md`, `20261107_Apply-Pass-Red-Team-Brand-Evidence.md`, `20261107_Apply-Pass-Red-Team-Craft-Access.md`). I changed only my own files: chapters 01 and 02, their specimens, `manifest-editor.json` and the four `guide_editor_*.py` scripts. I committed nothing.

### Items, by ID

**Must fix**
- **BE-02, Rule 01.11's correct plate.** No count exists to print. The research lead's reports hold none, and our atlas's case record for Loop R4a names more redraws, but not the party behind each map. So I took the brief's second route: the plate now claims only what it shows. Under the two cases it reads: "Our systems atlas records more redraws for this loop in 2025 and 2026, among them Missouri’s 2025 map and the maps four Southern states drew after a Supreme Court ruling of April 29, 2026. This plate shows two of them, one by each party’s majority, and gives no count." The source line adds the atlas's R4a case record. The caption ends "The line under the cases keeps the plate to what it shows: two of the loop’s redraws, with no count." Rule 01.11's For builders already asks a piece to count the record by party. The build now fails the plate if it has neither a count line nor "gives no count". When the research lead counts the record, a sourced count line in the cases' form replaces the scope line (`R4A_SCOPE`); I carry that count to stage B.

**Should fix**
- **CA-S3 and CD-S1, the H.R. 7008 card.** The card now uses chapter 11's story card form. The row is chapter 11's 324 px `steps_svg()` row, set on the text edge, so the first circle sits 15 px in at 1,440 and 390 px, as it does in chapter 11. Only where the column is narrower than 324 px (screens under 24.25em) does the same function draw a 288 px row, so the numbers never scale under 13 px. The status words and the key come from chapter 11's own CSS (`piece_css()`) and its `key()`, placed after the status words as its lists place them. The key shows the six step names and the four marks this bill uses. "As of November 5, 2026" is now a dateline in the label style above the steps. The four-sentence history is one sentence: "The committee held no hearing on this bill, so step 2 has a slash, and it voted 7 to 4 on January 14, 2026, on a version without the photo ID section." The dates and counts of the other steps stay in the hidden step list, and the earlier hearing moved to the source line.
- **BE-03.** Card wording: "only" is gone. The source line now says "The committee’s report names a November 19, 2025 hearing on the Stop Trading on Congressional Knowledge Act of 2012, held before the bill was filed, as the one used to develop the bill." The call is logged below. Rule 11.2's For builders is the systems designer's, so I ask there.
- **BE-01 alignment (step 2's words).** The card says only that the committee held no hearing on this bill. That holds under BE-01's interim definition ("The committee holds a hearing and takes testimony on the bill. Who can testify depends on the legislature"), and the card makes no claim about who could have spoken.
- **BE-04, BE-06, BE-11, the 2020 example.** "A July 2022 review titled Lost, Not Stolen, written by eight former officials and lawyers, among them two former U.S. senators and three former federal appeals judges, counted 64 cases it says Donald Trump and his supporters brought in six battleground states." The authors are described by role alone, as Rule 01.16 describes every holder. Their stated party ties stay in the source line, with the review's subtitle. "It says" puts the count in the review's voice, and the title no longer opens a line.
- **BE-05.** The caption now reads "they add no counter-case to even the count".
- **BE-10.** Rule 01.6's failure card is about the chapter's invented bill: "What the state senate’s vote on S. 214 means for you / One vote, 21 to 18, and what comes next." It carries one Illustrative label and the "Failure case: do not publish" band. The rotation log follows.
- **CA-S6, in my chapters.** The band now heads every failure plate that could pass for our work: Rules 01.6, 01.7, 01.8, 01.18, 01.19, 01.20, 01.22, 01.23, 02.23, 02.24, 02.25 and 02.27, besides 01.1 to 01.5 and 02.22. Each alt opens "Failure case: do not publish." Fragments of a line (01.13, 01.14, 01.17, 02.26) and lists of kickers or names (01.21, 01.24) keep no band.
- **CA-S7.** The pillars figure adds the row a section opener sets at 48 px with Track current: the word underlined, and Track's red parts drawn (the pin and the magnifier's handle). Each pillar icon's margins are trimmed to its measured ink (`INK` in `guide_editor_common.py`, from getBBox in Chromium), so every word sits 12 px from its drawing at 48 px and 8 px at 24 px; Act's hand left 34 of 128 units empty on each side. The build now requires a current pillar at 48 and 24 px, and red on the 48 px one only. The 24 px icons' light stroke waits for chapter 09's pixel-fit masters (stage B).
- **CA-S8.** `s-01-pieces` is now a readable group, so a screen reader reads every card's text and every source line, and its alt is a three-sentence description.
- **CA-S12.** The 24 px topic icon now sits in the kicker's line with a −5 px margin above and below, so the Analysis headline sits where the other six do. A 16 px pixel-fit icon is chapter 10's (stage B); at 16 px today's line is 0.42 px.
- **CD-S2 and BE-13.** I kept the card's red "Follow this bill", as the creative director prefers; the four pillar cards end the same way. The fix is in Rule 11.4's specification, which is the systems designer's: scope "a text link ... the red button waits for the bill's own page" to cards that carry the take-part mark. Carried to the systems designer.

**Notes taken**
- **CD-N4.** Rule 02.25's source line now names the bill status and the House-passed text, sections 2 and 3, for the two provisions.
- **BE-12.** The office row ("The committee chair decides which bills get a hearing.") now carries "Source: U.S. House of Representatives, Rules of the House, 119th Congress, rule XI, clause 2(g)(3)(A), in the House Rules and Manual, H. Doc. 118-187, via govinfo.gov, United States. Retrieved November 7, 2026. The rule has each committee’s chair announce its hearings; state legislatures set their own rules." DR-123's wording is unchanged.
- **CD-N6.** The hinge table no longer underlines the action half, since an underline now marks the current pillar (DR-111). The commitment stays bold, and the caption and alt say so.
- **CA-N4.** No-break spaces keep "48 px" together in the pillars caption and the card's dateline together.
- **CA-N12.** Rule 01.21's caption adds "“Act · How to take part” is one label, so its dot and both its words belong to the label."
- **CA-N11 and CD-N1, the Illustrative label twice.** These go to the shell (the engineer's CD-N1); I changed nothing.

### Routine calls, as proposed decision lines

- D2-xxx | Rule 01.11's correct plate says it shows two of the loop's redraws and gives no count, until the research lead counts the atlas's record by party | BE-02: no count exists in the research, and the plate may claim only what it shows (DR-93)
- D2-xxx | A hearing on a bill's subject held before the bill was filed does not fill step 2; the step's note or the source line names it | BE-03: one standard for the next bill, matching the H.R. 7008 card
- D2-xxx | The H.R. 7008 card takes chapter 11's 324 px row on the text edge, its status style and its key after the status words; a 288 px row only under 24.25em | CA-S3: one geometry for every story card, and numbers at 13 px at every width checked
- D2-xxx | The card's committee history is one sentence, and the earlier hearing sits in the source line | CD-S1 and CA-S3: Rule 11.1's one plain sentence, with D2-407's two facts kept
- D2-xxx | Authors and holders are described by role and affiliation, and stated politics stay in the source line | BE-04, DR-93's one way of describing sources, as Rule 01.16 does
- D2-xxx | Failure plates that could pass for our work carry the band, and fragments of a line do not | CA-S6 and D2-308, applied across chapters 01 and 02
- D2-xxx | Pillar icons are spaced from their measured ink, not their 128-unit box | CA-S7: equal space from drawing to word for every pillar

### Questions for Dustin

1. **Rule 01.11's reason opens two sentences with "Where" (W13).** It prints exactly as you approved it in DR-125. The creative director proposes a better fix than my one-sentence version, and I now recommend theirs. It recasts the first sentence and keeps the second word for word: "A case from each party, told the same way, puts a mechanism that both parties use in front of the reader. Where the record shows one side doing more, the finding stands as the record shows it." *Recommendation:* approve it.

### For the main session and the other owners

- **Research lead, stage B (BE-02).** Count the 2025 and 2026 congressional redraws in Loop R4a's case record by the party of the majority that drew each map, with a primary source for each. Rule 01.11's plate then prints the count.
- **Systems designer.** (1) BE-03: add to Rule 11.2's For builders: "A hearing on the bill's subject held before the bill was filed does not fill step 2; the step's note names it." (2) CD-S2 and BE-13: scope Rule 11.4's card row to cards that carry the take-part mark. (3) CA-S3: the card places chapter 11's `key(names, show=<the states on the card>)` after the status words, and `s-11-4-correct` can take the same key in the same place.
- **Chapters 09 and 10 at stage B.** Pixel-fit 16 and 24 px masters for the pillar icons (CA-S7) and for a kicker's topic icon (CA-S12).

### Tested

- `python3 -I work/build/scripts/phase-2/guide_editor_build.py`: every check passes. New or changed checks: Rule 01.11's plate has a count line or "gives no count"; the pillars figure shows a current pillar at 48 and 24 px, with red on the 48 px one only.
- Planted faults: 17 of 17 caught, the 16 from round two and one new (the "gives no count" line removed). Three plants had to be re-aimed after their targets moved, and I report them caught only after the re-aim.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`: 0 warnings, 100 rules, 233 specimens.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px, on the final build: PASS, 0 failures, 756 same-page links.
- The card's geometry, measured by script in Chromium: card 340, 326 and 296 px wide at 1440, 390 and 360 px; row 324, 324 and 288 px; first circle 15, 15 and 12 px from the text edge; smallest step number 13.0 px at all three.
- The pillar icons' ink boxes, measured with getBBox in Chromium.
- By eye in Playwright Chromium: the card at 390 px and its steps, status and key at twice size at 1440 px; Rule 01.11's plate and the pillars figure at 1440 px.
- The 2020 example's new sentence, compared by string with BE-04, BE-06 and BE-11's wording.

### Not tested

- BE-12's House rule: I did not open the House Rules and Manual. The source line rests on the brand and evidence red team's reading.
- The count BE-02 asks for; nobody has made it.
- Chapter 02's banded plates by eye; the check passed them at four widths.
- Screen readers by ear, forced colors, Firefox, Safari, print, 200 percent zoom and real readers.

### Change log, fix pass

Modified:
- `work/build/scripts/phase-2/guide_editor_common.py` (ink trims, the kicker icon's margins), `guide_editor_ch01.py`, `guide_editor_ch02.py`, `guide_editor_build.py`
- Regenerated by the build: `work/build/guide/chapters/01-purpose.json`, `02-voice.json`, `manifest-editor.json` and the `s-01-*` and `s-02-*` specimens
- Regenerated by the shared build and check: the stage A chapters page, its build report, its check results and its captures
- This file

Created: none. Nothing committed or pushed.

## Q1 to Q4 pass

November 8, 2026, under `work/handoffs/phase-2/20261108_Q1-To-Q4-Apply-Pass-Brief.md`, section "Editor", item 1. Dustin answered Q4 on the changes board as recommended (DR-132). I changed only my own files: chapter 01 through its build script, and the editor's build checks. I committed nothing; the main session's snapshot commit f5c40d2e holds the change. Item 2, the copy edit of the identity designer's new strings, waits for the main session's message with their notes.

### What I did

**Item 1, Rule 01.11's reason (DR-132).**

| Location | Original | Revision | Reason |
|---|---|---|---|
| Rule 01.11, why it works (`RULE_11_WHY` in `guide_editor_ch01.py`) | "Where both parties use a mechanism, a case from each, told the same way, puts the mechanism in front of the reader. Where the record shows one side doing more, the finding stands as the record shows it." | "A case from each party, told the same way, puts a mechanism that both parties use in front of the reader. Where the record shows one side doing more, the finding stands as the record shows it." | DR-132, Dustin's answer to Q4. The two sentences now open on different frames, as W13 asks, and the second keeps DR-93's standard word for word |

- The new string matches DR-132 in the decision log, the brief and version (c) on the Q4 card, character for character. Its sentences run 21 and 16 words.
- **Other copies.** I searched chapters 01 and 02, the visible text of all 112 of their specimens and every alt text in `manifest-editor.json` for the old reason whole and for its parts ("both parties use", "told the same way", "one side doing more", "in front of the reader", "stands as the record shows"). The old reason appeared once, in Rule 01.11's reason. Two other hits are different sentences that share a phrase: Rule 01.6's reason ("Campaigns in both parties use the dome and the flag ...") and Rule 01.11's own first paragraph ("When majorities of both parties use the same mechanism ..."). Neither repeats the reason, so both stay.
- Outside my files, the old wording survives only on boards, which record what Dustin saw: board A (`work/boards/20261106_Stage-A-Foundations-Board.html` and its content file) and the changes board with its content file, where it is Q4's version (a). I left them alone. The chapters page carried it until the shared build regenerated the page.
- **Build check.** The editor's build now names DR-132 when Rule 01.11's reason differs from the approved string, and it fails if the old first sentence turns up anywhere in chapters 01 and 02, their specimens or their alt text.
- **Basis.** Rule 01.11's basis stays "Design judgment", as on 23 of chapter 01's 24 rules.
- **Patterns in the changed string:** em dashes 0, listed fillers and corporate verbs 0, parallel runs 0. Round one counted one parallel run in my chapters, this reason, and none remains.

### Routine calls, as proposed decision lines

- D2-xxx | The editor's build fails if Rule 01.11's old first sentence appears anywhere in chapters 01 and 02, their specimens or their alt text | DR-132 replaces it, and the check stops a later edit from bringing an old copy back
- D2-xxx | Rule 01.11's basis stays "Design judgment" | DR-132 changes only the reason's wording, and chapter 01's other rules that Dustin worded in DR-125 (01.12, 01.20) carry the same basis

### Questions for Dustin

None. DR-132 answers the question on Rule 01.11's reason that my round one, round two and fix pass notes carried.

### Tested

- `python3 -I work/build/scripts/phase-2/guide_editor_build.py`: every check passes. The build rewrote `01-purpose.json` with one changed string, the reason. `02-voice.json`, the 112 specimens and `manifest-editor.json` came out byte for byte as before; git shows no change to them.
- Planted faults, in memory, with nothing written: 6 of 6 caught, and the clean build drew no DR-132 failure. The plants: the old reason in Rule 01.11; the recast with "that" dropped; the old reason added to a chapter 01 caption, to a chapter 02 rule, to the text of `s-01-11-correct` and to the alt text of `s-02-lines`.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`: 0 warnings, 9 chapter files, 100 rules, 233 specimens. A word diff of the chapters page shows two changes, the reason and the build date.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px: PASS, 0 failures, 756 same-page links. The page it checked carried my change and none of the identity designer's; their files showed no change when I ran it, so the build never failed on a file I do not own.
- By eye in Playwright Chromium: Rule 01.11's reason on the chapters page at 1440 and 390 px. The paragraph's text in the page matches DR-132.
- The new string against DR-132 in the decision log, the brief and the Q4 card, compared by script.
- The search for the old reason, by script, whole and in parts, and my own read of every hit.

### Not tested

- The chapters page with the identity designer's Q1 to Q3 changes in it. Their rebuild carries my chapter 01 file, and the check after their pass covers both.
- Screen readers, forced colors, Firefox, Safari, print, 200 percent zoom and real readers.
- How the recast sounds read aloud to a reader.

### Change log, Q1 to Q4 pass

Modified:
- `work/build/scripts/phase-2/guide_editor_ch01.py`: `RULE_11_WHY` takes DR-132's words; a new `RULE_11_WHY_OLD` holds the old first sentence the build looks for
- `work/build/scripts/phase-2/guide_editor_build.py`: the reason check names DR-132, and a new check fails on the old first sentence
- Regenerated by my build: `work/build/guide/chapters/01-purpose.json` (Rule 01.11's reason only)
- Regenerated by the shared build and check: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report, its check results and four 390 px captures
- This file

Created: none. The planted-fault script and the captures stay in my session scratchpad.

Not touched: `source/`, `work/ledger/`, the Civic Line masters, any board other than reading it, the reader check and every other owner's files. Nothing committed or pushed.

### Round two: copy edit of the identity designer's strings

November 8, 2026, from the main session's message after the identity designer finished. I read their "Q1 to Q4 pass" notes and copy edited every reader string they added or changed in chapters 03, 04 and 08, the proofs, their specimens and alt text, and the minimum sizes file. A script listed 87 strings that are new since commit c734d03d, and I read each one. I changed strings only in the identity designer's build scripts and reran them in the order their notes give. I left every measured figure as their figures file sets it, and every master name as they wrote it. Before I edited, I reran `stage_a_identity_s1.py` and `stage_a_identity_build.py` untouched, and every output matched what was on disk, so each later diff is mine.

The manifest's `notes` fields stay as the designer wrote them: they record studio codes and sources, and the page prints none of them. The proofs read their captions from `proofs.json`, so the notes never reach the page there either.

| Location | Old | New | Reason |
|---|---|---|---|
| Rule 03.4, rule | "The end mark alone may stand under 16 px, at the text’s cap height, ..." | "Only the end mark, ampersand B at the close of an article, may stand under B’s 16 px minimum, at the text’s cap height, ..." | H02: the guide's first use of "end mark" is here, a chapter before Rule 04.6 defines it. The 16 px is B's minimum, which the sentence did not say |
| Rule 03.4, For builders | "The lockmark’s 16 and 24 px masters run the same" | "... take B’s ranges" | "The same" left the reader to find what they match |
| Rule 03.6, rule | "the wordmark at left and the lockmark at its right, 48 px tall, from the lockmark’s 48 px master" | "the wordmark at left and, to its right, the lockmark’s 48 px master at 48 px" | "48 px tall" could read as the wordmark's height, and the size was given twice |
| Rule 04.6, rule | "... run past the capitals: in 17 px body text, B stands 14.1 px tall ... This is the one place B may stand under its 16 px minimum" | "... run past the capitals. In 17 px body text it is 14.1 px tall ... The end mark is the one use of B that may stand under its 16 px minimum" | W06, the colon held the figures back; "B stands" twice; "This" named no noun |
| Rule 04.6, Size | "on the text’s capitals at every text size: 16/14 of the cap height, ... In body text B stands under its 16 px minimum" | "... at every text size, so B stands 16/14 of the cap height tall, ... In body text that puts B under its 16 px minimum" | The colon did not say what 16/14 measured |
| Rule 04.6, For builders | "Draw B in `currentColor`, so it takes the paragraph’s ink, from its 16 px master at 16/14 ...; and it holds for text up to 27 px" | "Draw B from its 16 px master at 16/14 ..., and in `currentColor`, so it takes the paragraph’s ink ...; and those values hold for text up to 27 px" | The inserted clause split "Draw B" from its master; "it" had no clear noun |
| Rule 08.1, rule | "so the drawing holds at small sizes" | "so the drawing holds at the sizes each one serves" | W20: 48 px is the masthead's size, which "small" overstates |
| Rule 08.1, correct caption | "the display master at 96 px, then the 48, 24 and 16 px masters, and the 48 px master on Charcoal and on Prussian" | "the display master at 96 px and the 48, 24 and 16 px masters. Last, the 48 px master on Charcoal and on Prussian" | Two "then"s, and one "and" joined two rows of the plate |
| `s-08-1-correct`, alt | "the 48 pixel master on Charcoal and on Prussian, where it is all White" | "the 48 pixel master on Charcoal, in Newsprint with its red lever, and on Prussian, all in White" | "All White" read as both grounds; on Charcoal the plate draws Newsprint and a red lever |
| Rule 08.2, why | "Each place draws a master ..., so the four places read at one weight" | "Because each place draws a master ..., the four places read at one weight" | W13: two sentences in a row on the frame "..., so ..." |
| Rule 08.2, Masthead specification | "the 24 px wordmark master, 13 px and the lockmark" | "13 px of space and the lockmark" | "13 px and" read as a third object; Rule 03.6 says "of space" |
| Rule 08.2, Feed test | "Reduce the card with Lanczos resampling and count" | "Reduce the card with Lanczos resampling, a common filter for shrinking images, and count" | H02 |
| Rule 08.2, For builders | "the 48 px master for the sign-off, which L3’s masthead master already carries;" | "the 48 px master for the sign-off, and L3’s masthead master, which holds it already, for the masthead;" | The list named three places and left out the masthead |
| Rule 08.2, For builders | "every new social card template" | "every new template for a social card" | W14 |
| Minimum sizes file and `s-03-minimums`, L3 row | "13 px and the lockmark at 48 px" | "13 px of space and the lockmark at 48 px" | As in Rule 08.2 |
| Minimum sizes file, L3 status note | "The masthead master sets the lockmark at 48 px since November 8, 2026" | "... has set ..." | Tense |
| Minimum sizes file, B's `end_mark` | "The end mark alone may stand under 16 px" | "Only the end mark, ampersand B at the close of an article, may stand under 16 px" | Matches Rule 03.4 |
| Minimum sizes file, lockmark status note | "Its range was chosen by test ... so it is placed at 48 px only" | "A test set its range ... so builders place it at 48 px only" | W02, two passives |

The rest I read and kept: Rule 03.2's L3 and L6 rows and builders line, Rule 03.4's "End mark" row, Rule 03.6's specifications and failure caption, L6's caption, Rule 04.6's reason, caption, figures rows and alt text, Rule 08.1's reason, basis, specifications and builders line, Rule 08.2's rule, caption, place rows and "Feed test, our card", Rule 08.3's drawing row, the proofs' social card text, every plate tag, the minimum table's other rows and their SVG titles.

**Routine calls, as proposed decision lines**

- D2-xxx | Rule 03.4's exception names the end mark and defines it there: "Only the end mark, ampersand B at the close of an article, may stand under B’s 16 px minimum" | Chapter 03 is the guide's first use of the term (H02), and the brief's wording "under 16 px" did not say whose minimum
- D2-xxx | The manifest's `notes` fields keep their studio codes and stay unedited | The page prints none of them, and they are the maker's record

**Noted, changed nothing**

- Pixel widths. Chapters 03, 08 and the proofs write "1200 by 630", "1440 px" and "1080 px", and chapter 06 writes "1,200 px". The page uses both forms. I left both, since chapter 06 belongs to another owner. *For the main session:* pick one form at stage B.

**Tested (round two)**

- Each identity build rerun untouched before my edits reproduced every output on disk, checked by hash: 333 files.
- `python3 -I work/build/scripts/phase-2/stage_a_identity_s1.py`, then `stage_a_identity_build.py`: the 48 px master and L3 assertions hold; 48 specimens, 3 chapters. Afterward, only the files my edits reach changed: `03-identity.json`, `04-ampersand.json`, `08-lockmark.json`, `manifest-identity.json`, `s-03-minimums.html` and the minimum sizes file.
- Every number in the 17 changed strings, compared by script before and after: no figure changed.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`: 0 warnings, 9 chapter files, 100 rules, 233 specimens.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px: PASS, 0 failures, 761 same-page links.
- Em and en dashes in the three chapter files, the identity manifest and `s-03-minimums`: 0.
- A pattern scan of all 87 strings found no listed filler or corporate verb; its one filler hit, "key", sat in file references. Its negation hits are plain limits, such as "no tagline under 7 pt", and our fifth edition's quoted reason, and none turns "not X but Y". My edits add none of these.
- By eye in Playwright Chromium: Rules 03.4 and 04.6 at 1440 and 390 px; `s-03-minimums` at 1440 and 390 px. The table measures the same width at 390 px before and after my edits.
- `stage_a_identity_q_measure.py` was not rerun. My edits change no drawing and nothing it reads, and the figures file is untouched.

**Not tested (round two)**

- Rules 03.6, 08.1 and 08.2 by eye after the edits; the guide check covered them at four widths.
- Screen readers, forced colors, Firefox, Safari, print, 200 percent zoom and real readers.

**Change log, round two**

Modified:
- `work/build/scripts/phase-2/stage_a_identity_chapters.py` (Rules 03.4, 03.6, 04.6, 08.1 and 08.2)
- `work/build/scripts/phase-2/stage_a_identity_s08.py` (`s-08-1-correct`'s alt text)
- `work/build/scripts/phase-2/stage_a_identity_s1.py` (three rows of the minimum sizes table)
- Regenerated by those scripts: `work/build/assets/identity/20261028_Identity-Minimum-Sizes.json`, `work/build/guide/chapters/03-identity.json`, `04-ampersand.json`, `08-lockmark.json`, `work/build/guide/specimens/manifest-identity.json` and `s-03-minimums.html`
- Regenerated by the shared build and check: the stage A chapters page, its build report, its check results and its captures
- This file

Created: none. Not touched: `source/`, `work/ledger/`, the identity masters' drawings, the figures file, every board, the reader check, and the build scripts of owners other than the identity designer. Nothing committed or pushed.
