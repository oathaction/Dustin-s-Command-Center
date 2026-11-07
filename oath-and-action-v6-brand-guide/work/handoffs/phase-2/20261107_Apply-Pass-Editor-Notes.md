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
