# Chat 13b editor notes

Editor (oa-editor), chat 13b, Part A turn, opened 00:16 UTC, November 25, 2026. Items: 8 (DR-336), 2's words (DR-330), 4's line words (DR-332), 7 (DR-335, once Engineer A passes `phase3_ch15_build.py`).

## Routine calls

- D4-x | Rule 01.16's Length row prints Dustin's sentence without "(DR-37, DR-93)" | No row, caption or rule text in the guide prints a decision code (checked by script over every chapter JSON and specimen: the only DR codes are in code comments in `s-26-token-table.html`'s script and the shell's JS and CSS), and `guide_editor_build.py`'s H11 check refuses one in reader text, as `phase3_ch13_build.py`'s does; the brief prints the codes only if rows print them elsewhere
- D4-x | Rule 13.2's Contested row, final words: "Both readings at the same length, except a reading quoted from a record, which prints at the length the record holds (Rule 01.16)" | It keeps the row's first words and its citation, takes Rule 01.16's own term ("the length the record holds", H02), and states the exception once in a plain clause, where the board's draft ("or at the length the record holds for readings quoted from it") put the condition after the length it governs

## Words for Engineer A

### Item 2 (DR-330): Rule 04.3 names the keyline; Rule 05.3 does not change (00:23 UTC)

**The call.** Rule 04.3 must name the hinge headline's keyline, and Rule 05.3's keyline row need not. Rule 05.3 already covers B: its spec row "A hinge headline" says "A hinge headline’s ampersand uses the view’s working red", its why says "a working red mark there takes a keyline, a 1 px Charcoal edge drawn inside the mark", and its keyline row ("Keyline on a red mark on Newsprint: Charcoal, 1 px, 13.29 to 1, except the marks Rule 05.5 names") leaves out only the error bar and the atlas target. So B in a hinge headline was always inside Rule 05.3's words, and DD10-NF1 was a drawing that missed them. Rule 04.3 is the rule a builder follows to set a hinge headline, and its specifications (face, B's height, B's position, line break, master) say nothing of color or edge, while its plate will now draw the keyline. Its words must say what its plate shows. So `stage_a_systems_ch05.py` stays as it is, and no chapter 05 run is needed.

**Words, in `work/build/scripts/phase-2/stage_a_identity_chapters.py`, Rule 04.3** (straight apostrophes as the file writes them; the build curls them):
1. A sixth spec row, after "Master":
   `S("B's keyline", "On Newsprint, a 1 px Charcoal edge drawn inside the mark, 13.29 to 1, as Rule 05.3 sets; none on White or Charcoal", "oa.color.border.strong.onNewsprint")`
   The token is the one tokens.json describes as "the keyline on a red mark" (`oa.color.border.strong.onNewsprint`, Charcoal). Leave the rule's own `tokens=[...]` list as it is unless your check needs the token there too.
2. The correct caption's second sentence, from "Each B comes from the master whose range holds that cap height." to:
   "Each B comes from the master whose range holds that cap height, with a 1 px Charcoal keyline drawn inside it on Newsprint."
   (The plate's panel is fixed Newsprint, `oai-s-newsprint`, so the caption holds in both themes.)

**Words, in `work/build/scripts/phase-2/stage_a_identity_s04.py`, `s_04_3_correct`'s alt**, from "joined by a red ampersand B that leads the second line:" to:
   "joined by a red ampersand B that leads the second line and carries a thin Charcoal edge:"
   The full alt then reads: "Three hinge headlines at true size in heavy type, each naming a rule and then what it produces, joined by a red ampersand B that leads the second line and carries a thin Charcoal edge: The zoning code & the rent. at 56 pixels, The filing deadline & the ballot. at 44, and The records law & the answer. at 26."

Nothing else in Rule 04.3 changes: its title, rule, why, failure and corrective words stay. The failure plate's caption and alt stay true whether or not its B takes the keyline, since it fails on two working reds.

**For the identity proofs' link card and A01:** their words do not change. B stays "a red ampersand" in each alt; the keyline is a 1 px edge on the same mark.

### Item 4 (DR-332): the line that opens a wide frame's export (00:23 UTC)

One form of words, filled from the frame's width and theme, as a page-words field beside chapter 20's `VIEW_WORDS` and chapter 21's matching dictionary (suggested key `'wide_line'`):

`'wide_line': 'Open the {w} px page in the {theme} theme at true size'`

- `{w}` is the view's width as the labels print it, with no comma: 1440 or 1024. `{theme}` is the view key's theme word: light or dark.
- It reads: "Open the 1440 px page in the light theme at true size", "Open the 1024 px page in the light theme at true size", "Open the 1440 px page in the dark theme at true size".
- "Page", since each export in `work/build/exports/phase-4/` is a whole page at one width and theme (`20261121_Web-Article-Page-Special-Districts-1440-Light.png`, `20261122_Atlas-Loop-R18-Page-1440-Dark.png`), so the words stay true when the wide frame on the plate shows only part of that page, as chapter 21's `1440-light-drawing` does. The plate around the line names which page it is.
- The whole line is the link text, so a screen reader's list of links names the width and theme of each. "True size" is the chapters' own phrase (chapter 20's opening: "our exports keep every frame at true size").
- A wide view with no export at its width and theme (the masthead and footer rows, unless a page export holds them) would leave the line pointing nowhere; whether such a frame stays is Engineer A's layout call, not a words question.

## Done

- **Item 8 (DR-336), 00:19 UTC.** Rule 01.16's Length row now reads "The same number of words in each reading. Readings quoted from a record print at the length the record holds; readings we write run the same length" (`work/build/scripts/phase-2/guide_editor_ch01.py`, `SPECS01["01.16"]`; run `guide_editor_build.py` then `stage_b_identity_ch01.py`, 00:17:48 to 00:17:50 UTC, exit 0). Rule 13.2's Contested row reads "Both readings at the same length, except a reading quoted from a record, which prints at the length the record holds (Rule 01.16)" (`work/build/scripts/phase-3/phase3_ch13_build.py`, Rule 13.2's `specs`; run 00:18:07 UTC, exit 0). Files moved, by a SHA-256 list of `work/build/guide/` before and after each run and by `git diff --stat`: `01-purpose.json` (1 line) after the chapter 01 chain, `13-evidence.json` (1 line) after chapter 13's; no specimen, manifest or other chapter moved. `phase3_ch14_build.py --check`: 99 of 99 files current (00:18:12 UTC). Bytes: chapter 01, 675,695 before and 675,802 after (+107); chapter 13, 242,840 before and 242,924 after (+84); the page 14,444,549 before and 14,444,740 after (+191, the two phrases' bytes exactly). A line diff of the page against the opening build (`scratchpad/opening/guide.html`) shows the two rows and the colophon's build time and nothing else.

## Requests

- **Chapter 21's kit plates A11 to A20 (`work/build/app-kit/plates/a11.json` to `a20.json`), for Engineer A or the main session.** The kit hashes `phase3_ch13_build.py` and `phase3_ch15_build.py` as inputs of every atlas page plate, A11 to A20 (`atlas_figures.py` imports chapter 15's generator, which imports chapter 13's). Item 8's edit to `phase3_ch13_build.py` therefore makes the strict build warn 41 times, "the kit's plate A1x is older than 1 of its inputs (phase3_ch13_build.py)", and exit 1, with the page otherwise exactly as expected (00:18 UTC). Items 6 and 7 edit `phase3_ch15_build.py` and will do the same. Suggested: rerun chapter 21's run order (V33) once, after items 6, 7 and 8 have all landed, and prove the plates' drawings unchanged apart from item 6's case. I did not run the kit: its plates are not my files

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| ED13b-1 | Editor, item 2's words | Hinge headlines drawn before DR-330 with a red B on Newsprint and no keyline, outside the three places DR-330 names: `s-01-18-correct`, `s-01-18-failure`, `s-01-19-correct`, `s-01-19-failure`, `s-01-20-correct`, `s-01-20-failure`, `s-02-27-correct`, `s-02-27-failure` (the editor's chapters 01 and 02, `amp_h()` in `guide_editor_common.py`, on Newsprint in the light theme since `.ed` takes the page's surface); chapter 04's opener `s-04-opener` and Rule 04.2's link card `s-04-2-correct` (`headline()` in `stage_a_identity_s04.py`, unless Engineer A's change already reaches them); chapter 20's share preview A09 (`share-image.mjs`, B at 110 px on Newsprint, unless Engineer A's change reaches it) | Once Rule 04.3 names the keyline, each of these plates shows a hinge headline its own guide now says is drawn wrong on Newsprint (a rule and its demonstration disagree) | Draw the keyline on each, through its generator, with the same 1 px Charcoal edge; failure plates keep the reason they fail | Chapters 01, 02, 04 and 20 are approved, and DR-330 names only Rule 04.3's plate, the proofs' link card and A01, plus hinge headlines built from now on; these need the main session's reading of DR-330, or Dustin's word by name | Open |

## Tested

- Item 8: `guide_editor_build.py` and `stage_b_identity_ch01.py` exit 0 with the editor's checks (locked lines exact, H11's code check, fillers); `phase3_ch13_build.py` exit 0 with its checks; a SHA-256 list of every file under `work/build/guide/` before and after each run (one file moved each time); `git diff --stat` and `git diff` of both chapter files; `phase3_ch14_build.py --check` 99 of 99; a strict build to scratch (00:18:17 to 00:18:32 UTC): 14,444,740 bytes, 22 chapters, 409 rules, 766 specimens, exit 1 on 41 warnings, every one "plate A11 to A20 older than phase3_ch13_build.py" (see Requests); a line diff of that page against the opening build (the two rows and the colophon's time); chapter bytes from both builds' reports.
- Decision codes on the page: a script over every chapter JSON (no DR code in any field) and a grep of every specimen and the shell (DR codes only in code comments).
- Item 2 and 4's words: a script check for em and en dashes, the listed fillers and corporate verbs, hedges, decision codes and "not" (none), with word counts; the board's pictures for Rules 01.16, 13.2, 15.16, 04.3 (DD10-NF1) and Rule 20.7 at 390 px (C11-1) read at true size.

## Not tested

- The strict build at exit 0: it waits on the rebuild of plates A11 to A20 (Requests).
- How Rule 04.3's new words sit on the built plate: Engineer A places them; I did not run chapter 03's chain.
- The line words for item 4 in place: Engineer A's layout lands after Engineer M's C1.
- No browser was opened for these items.
