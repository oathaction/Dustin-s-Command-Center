# Stage B drawings board: editor's notes

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the editor (`.claude/agents/oa-editor.md`) for the main session, as D2-500 asks before the creative director scores the board. I committed nothing and published nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

I read every word the board shows: the rendered text at 1,440 px, the score reasons inside each closed "Every score with its reason" panel, and the alt text and screen reader labels. I fixed the board's own words in `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Content.json` and every other owner's words through that file's `editor_overrides`. No owner's file changed.

## What I changed

**The board's own words.** I rewrote 28 strings in the content file and added three: two legend entries (Pixel fit, 1x and 2x screens) and one cover line. The rewritten look-alike entry carries the main session's addition on what a flag means.

**Other owners' words, through 51 overrides.** The build reports each one matched at least once.

- The creative director's scores file: 29. Eight correct score reasons that still describe options the fix round dropped, such as "All three read as Play" on a card that now shows one Play. Two point the family card's reasons at the designer's plate page, since the board shows neither the stepper row nor the rows' figures. Nine replace code words a founder would trip on, such as `currentColor` and `data-icon`. Two size absolute claims to their evidence, two explain the earlier figure in a real-choice note ("from 0.975" becomes "down from 0.975 before the redraw"), five keep one name for one thing, and one changes a colon in the Testify recommendation.
- The Civic Line designer's manifest: 12. They turn fragments such as "Fence and red door kept." into sentences, explain or replace "attic", "drum" and "bays", define "pediment" at its first use, and cut "a step larger", which tells Dustin nothing.
- The utility designer's manifest: 8. They turn the audit's corrective negations into reasons, merge Play's and Pause's matching reasons into one sentence, and explain "repeated A".
- The accessibility audit: 2. The inner quotation marks inside the lead's quotes become single marks. Every word of each quote stays.

Of the 3,270 or so lines of rendered text, 83 changed. Some of those are the creative director's new family card, committed at 10:38 p.m. UTC while I worked (commit `2a36e203`), which the rebuild picked up.

### Notable edits

- **What a flag means**, as the main session asked. The look-alike entry now reads: "Among the 7,381 pairs of settled Civic Line drawings, one in 20 measures 0.871 or more, and 74 pairs, one in 100, measure 0.913 or more, most of them drawings built on a shared base, such as a page or a document with a different mark on it. The board flags a figure of 0.913 or more, which asks for a look by eye, and marks one from 0.871 up as one to watch. Before CL-014 B was redrawn, it measured 0.950 against R-46 Expand the House, and the creative director set the two side by side and found a reader will not take one for the other." It names that one look and claims no look at every flagged pair.
- **Terms at first use.** The cover now defines "settled drawings" (ones Dustin has already approved), "true size", "device pixel", "pixel fit", "1x and 2x screens", the naming test's verdicts and the maker's verdict, and what a DR- or D2- number points to (H11). L6 is named as the strip that closes a report or a long page.
- **A claim the record does not hold.** "Real readers see the drawings in the combined reader check" became "Real readers see some of these drawings, among them the pillar icons and the end mark". DR-143 lists the pillar icons, the end mark and the 24 px lockmark, and no new Civic Line drawing.
- **D2-620 and D2-636 hold.** Both lines that say "names Congress" carry "without its label". Nothing on the board counts the committees that take written testimony; Testify B's lines describe the drawing alone.
- **Stale score reasons.** Play, Pause, Search, Selected check, Go to another site and Warning had reasons naming options B or C that the fix round removed. Each now names only what the card shows.
- **Sentences, where the scope rule asks for them.** The pillar, identity, Testify, Contact, lockmark and L6 introductions opened with fragments, and each now names who acted, such as "The identity designer rebuilt the 24 and 48 px lockmark masters".
- **One name for one thing.** "Utility icon" replaces "interface glyph" and "glyph" in the creative director's reasons. The family card's answer labels now match the creative director's recommended label, "Bare actions, shaped marks", which sits in a key the overrides cannot reach. The score legend says the tables shorten brand fidelity to Brand and evidence honesty to Evidence.
- **Absolute claims.** "the menu sign on every phone" became "the common menu sign on phones", and "the oldest media sign" became "the long-standing play sign".
- **A wrong comparison left the board.** The family card's old reason said ringed Play and Pause (0.958) sit above the closest pair of Civic Line masters (0.964). The creative director's scored family card replaced that reason before my rebuild, so the line no longer prints. It remains in the scores file's `family_questions` answer (see below).

Every option letter, ID, score and decision number is unchanged; a script compared them before and after. Three figures differ for reasons outside my words: the build time, "1400" written as "1,400" to match the rest of the board, and 0.958 and 0.964, which left with the creative director's new family reason.

## Routine calls

- D2-xxx | The board's own words are edited in the content file, and other owners' words only through 51 `editor_overrides`, each matching at least once | The task's instruction; no owner's file is edited
- D2-xxx | Score reasons that name options the fix round dropped now name only the options the board shows (Play, Pause, Search, Selected check, Go to another site, Warning) | The board must not describe a drawing it does not show; the creative director confirms when scoring (D2-500)
- D2-xxx | The family card's score reasons on the stepper row and the rows' look-alike figures are pointed at the designer's plate page or trimmed to what the card shows | The board's card shows neither
- D2-xxx | The look-alike legend says what a flag asks for, with the engineer's 74 pairs and the one pair the creative director looked at, and claims no look at every flagged pair | The main session's instruction; several recommended options carry a Flagged chip
- D2-xxx | The legend gains Pixel fit and 1x and 2x screens and defines the naming test's verdicts; the cover defines settled drawings, true size and DR- and D2- numbers | H02 and H11; the task names these terms
- D2-xxx | "Real readers see the drawings" becomes "some of these drawings, among them the pillar icons and the end mark" | DR-143 names those and no new Civic Line drawing
- D2-xxx | "Utility icon" is the board's one name for a utility drawing; "glyph" stays only where the builder's script writes it | H02 keeps one term after its first use
- D2-xxx | The family card's answer labels follow the creative director's "Bare actions, shaped marks" and "Every action in a ring" | The recommendation sits in an `option` key the overrides never touch, so the board's own labels move to match it
- D2-xxx | "on every phone" and "the oldest media sign" are sized to their evidence | W20; no research stands behind either
- D2-xxx | Fragments in the makers' change lines become sentences, and "attic", "drum" and "bays" are replaced or explained | The scope line lets only labels, captions and keys be phrases; H02
- D2-xxx | "Pediment" is defined in CL-059 A's change line, its first use on the board | H02
- D2-xxx | The audit's "a funnel, not sliders" and "never a cross" give their reasons from D2-508 and D2-509 | W09, corrective negation
- D2-xxx | Play's and Pause's reasons are overridden to one shared sentence, which the build prints once | The two matching sentences read as a parallel run
- D2-xxx | The accessibility lead's quotes keep every word, and only their inner quotation marks change | A quote stays in its owner's words
- D2-xxx | The Testify recommendation reads "state legislatures' own guides" | The meaning sheet's sources are Nebraska, Minnesota and Washington
- D2-xxx | The verdicts "Names it" and "Names the subject" stay as written, and the legend explains both | An override on "Names it" would also change "Names it nearly"
- D2-xxx | Utility ledes read "Used for:" in place of "Where it serves:" | "Where it serves: Close." names no place
- D2-xxx | After the edits I rebuilt the board and ran the board check with `--no-captures`, which rewrote the check results file | The builder's rebuild steps

## What I could not fix without the owner

The board builder's script writes these words, and neither the content file nor the overrides reach them:

1. Success A's pixel-fit line runs two clauses together: "Passes every test at 24 px but line weight, at 1x and 2x, passes every test at 16 px but line weight, at 1x and 2x." A semicolon or two sentences would fix it (`pf_words` and `utility_col`).
2. The pillar captions end "Against its master 0.682." without saying which figure that is. "Look-alike figure against its master: 0.682." would match the legend.
3. The family card's caption says "Each glyph at true size". "Each icon" would keep one term.
4. Alt text: "Contact An Official" takes capitals; the 2x views read "fit a" and "fit b" and "3 times larger" where the other alts say "four times"; L6's alt lowercases "(dr-129)".
5. In the reply panel, CL-014's buttons are labeled "Card 1, Option A" for screen readers, the same as a set would be, so a listener cannot tell CL-014's pick from the set's.
6. The labels' capitals turn "1x and 2x" into "1X AND 2X" on screen.

The creative director owns these:

7. The scores file still holds the stale reasons I overrode. Fixing them at the source would let the overrides go.
8. The `family_questions` answer still says ringed Play and Pause (0.958) sit above the closest master pair (0.964). It no longer prints, but the board would show it again if the family card lost its scores.
9. "Most readers know Congress by the Capitol dome" and "the download sign most readers know" are the creative director's judgments with no research behind them. I left them, since D2-620 carries the first; the creative director may want to mark both as design judgments (W20).

One content string is now unused: `utility-family.unscored` prints only when the family card has no scores. I left it for that case.

## Tested

- `python3 -I work/build/scripts/phase-2/stage_b_drawings_board_build.py --strict` after the last edit: exit 0, no warning, 51 of 51 overrides matched, 27 cards, 0.91 MB with its 117 files.
- `node work/build/scripts/phase-2/dataviz_check.js <board> --board --no-captures`: PASS, 0 failures at three widths.
- The rendered text, the score panels opened by script, and every alt and screen reader label, read through Playwright in Chromium, before and after. Em dashes 0, en dashes 0. The listed fillers, hedges and corporate verbs: 0, down from one "very".
- Decision numbers: none dropped and none added. Option letters, IDs and figures: compared by script, with the three differences explained above.
- All 27 cards keep "What you approve by name" and the "I approve card N by name" box.
- Both "names Congress" lines carry "without its label"; no line counts committees that take written testimony.
- The reply panel by script: card 6 marked bare and approved, and card 1 marked set B, compose "Card 6, Utility family: bare, as recommended. Approved by name." and "Card 1, Congress set: set B."
- A full read of the before text, line by line, and of every changed line after.

## Not tested

- The board check with captures on the scratchpad copy. I ran it with `--no-captures` only.
- The board by eye at any width after my edits, in Safari, Firefox or on a real phone, and with a screen reader by ear.
- Whether the creative director agrees with the reworded score reasons. They change what the creative director wrote, so the scoring pass should confirm them.
- Rhetorical triplets, parallel runs and setup and payoff in the makers' and the creative director's lines beyond my own read. No script can rule them out.
- How the new legend reads to Dustin. It grew from four entries to six.

## Change log

Modified:
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Content.json` (the board's words and 51 overrides)
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board.html` (rebuilt)
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Figures.json` (rebuilt)
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Check-Results.json` (rewritten by the board check)
- Outside the repository, rebuilt by the build: the publish copy and `files.json` in the scratchpad's `publish-drawings-board/`, and the check copy in `drawings-board/check-copy/`

Created:
- `work/handoffs/phase-2/20261109_Stage-B-Drawings-Board-Editor-Notes.md` (this file)
- Outside the repository: my render scripts, text captures and the content file's starting copy in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/443076db-a457-52c0-9ab2-d454e53bc53a/scratchpad/editor/`

I left `source/`, `work/ledger/`, the makers' files, the scores file, the audit, the build script, every master and every other board as I found them.
