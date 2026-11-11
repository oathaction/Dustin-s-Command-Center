# Stage C, round 1: chapter 18's anatomy plates

Oath & Action Edition 06, Phase 2, November 11, 2026. Written by the systems designer (`oa-design-director`, checked against `oa-ux-accessibility-lead`), run as a subagent of the main session, under `20261111_Stage-C-Round-1-Brief.md` ("Who works when", item 4) and the main session's instruction. Status: **done**.

I read the round 1 brief, the accessibility lead's chapter 18 notes (its section "Anatomy plates: what each must label" was still empty, so each plate labels the parts its rule's anatomy caption in `18-components.json` names), chapter 17's draft (Rules 17.8, 17.9 and 17.10), the engineer's contracts and the 24 code sets in `work/build/guide/code/c-18-*.html` and `.css` (read only).

## What I built

- **Generator:** `work/build/scripts/phase-2/stage_c_ch18_anatomy_build.py`, new. `--check` builds in memory and prints each plate's size.
- **Plates:** `work/build/guide/specimens/s-18-01-anatomy.html` to `s-18-24-anatomy.html`, one for each of Rules 18.1 to 18.24.
- **Manifest:** `work/build/guide/specimens/manifest-anatomy.json`, 24 entries, chapter "18", rule "18.N", each with its alt and notes. The plates are flowing (no `width_px`), so they fit the column at every width.

**How a plate is drawn.** Each plate is the component's own markup from its code set, cut to the parts its caption names, styled by the code set's own CSS, cut to the rules those parts use. It is a picture (AX-S8, the brief): every button, link, field, label, summary, dialog and landmark becomes a span or a div; ids, names and links go; and a state a reader would set by hand (focus, hover, checked) is set as an attribute that the rewritten CSS reads, so the code's own focus ring, hover underline and checked look draw. Utility icons draw from the sprite (`oa-sym-u-<name>-<size>px`), with the code's turn or mirror on the `<use>`, as the build asks of every specimen from chapter 09 on. Numbered callouts sit on the parts, a bracket marks each target's height, and a key in words follows. The stage's alt names every callout with its words, since the key sits inside a picture a screen reader does not enter. Because the plates read the code sets, a rerun redraws them when the component engineer changes a set; the generator stops if a key's numbers and the plate's callouts ever differ.

**The family look, the same on all 24.** A hairline frame on the surface's ground, 44 px of room at its left for the bracket. A callout is a 20 px Charcoal disc with its number in Newsprint at 13 px bold and a 2 px ring of the ground around it, set on a corner of a control, in the margin before a block of words, or above or below a word in running text. The bracket is a 2 px line down the target's left edge with short returns at each end. The key is a numbered list in the small body style, one column on a phone and two from 34 rem, each line its bold term, a full stop and its words.

**Per plate, in brief.** 18.1 buttons (primary with focus, quiet, with an icon, unavailable with its reason); 18.2 chips on and off; 18.3 a choice with focus on the checked segment and a waiting choice; 18.4 the theme switch at the top of the phone menu (the masthead set's menu head and the theme set together); 18.5 links in running text with the skip link drawn in place and one link under a pointer; 18.6 the phone bar, the navigation as it sits with 40 rem of room, and the open menu; 18.7 a breadcrumb and a list of places; 18.8 a disclosure open and one closed in focus; 18.9 tabs with the selected tab in focus, an unavailable tab and its reason; 18.10 the table, two rows and three columns, sorted by bill; 18.11 a scroll region in focus with its hint shown; 18.12 a code panel with its status line and the copy refused; 18.13 a copy row and its status line; 18.14 a download ready and one not ready; 18.15 a search with no match; 18.16 the filter bar open with one chip on, its count read from the set's own results; 18.17 a field in error, a field with a hint, the send button stepped down and the success line; 18.18 the three messages; 18.19 loading and empty; 18.20 the tracker card; 18.21 the report reader on its first page; 18.22 the stepper at its last step; 18.23 the diagram controls with one item selected, another in focus, the panel and the lines in words; 18.24 typed ID chips, plain and as a link under a pointer.

## Weight

The 24 plates weigh 146,870 bytes with their alts (6.1 KB a plate on average; the plates alone, without alts, about 5.4 KB). In the strict build with every chapter in the folder, **chapter 18 weighs 1,096,881 bytes, inside its 1.1 MB budget**, so its ceiling need not rise. The page weighs 9.54 MB. What keeps it there: utility icons from the sprite, the code's CSS cut to the rules a plate uses with state rules it never sets dropped, tokens read twice or more aliased once per plate, and the code's class names shortened inside the plate (D2-1366).

## Routine calls

The main session numbers these when it records them.

- D2-xxx | Each plate is drawn from its component's own code set, markup and CSS, cut to the parts its caption names | The plate shows the real parts, and a rerun follows any change the component engineer makes
- D2-xxx | A plate is a picture: controls and landmarks become spans and divs, ids, names and links go, and the stage is `role="img"` with an alt that names every callout and its words | AX-S8 and the brief; the key sits inside the picture, so the alt carries it for a screen reader
- D2-xxx | States a reader sets by hand (focus, hover, checked, disabled) are set as `data-ax-*` attributes, and the code's CSS is rewritten to read them | The plate draws the code's own focus ring, hover and checked look, with no script
- D2-xxx | Inside a plate the code's class names are shortened to letters, and tokens read twice or more are aliased once | Weight (D2-1366); letters only, since the specimen build leaves a class unprefixed after a digit
- D2-xxx | Utility icons in the plates draw from the sprite, one `<use>` for each turn, mirror or state class the code draws | The build warns on an inlined drawing the sprite holds; a table heading's two arrows keep the classes its CSS shows and hides by sort state
- D2-xxx | One callout style and one key layout across the 24: a 20 px Charcoal numbered disc with a ring of the ground, a 2 px bracket for the target's height, a numbered key in one column on a phone and two from 34 rem | A family the reader learns once
- D2-xxx | A callout on a block of words sits in the margin before its first line; on a control, on a corner; on a word in running text, above or below that word | No callout covers a word
- D2-xxx | The theme switch's plate shows it at the top of the phone menu, drawn from the masthead set's menu head and the theme set | Its caption names its place in the masthead, and the menu's head is the masthead set's own
- D2-xxx | The masthead's plate shows the phone bar, then the navigation as it sits with 40 rem of room, under a dashed rule, then the open menu | One picture holds every part the caption names at a phone's width
- D2-xxx | The links plate draws the skip link in place above the text and spaces the lines at 2.4 | The skip link otherwise covers the text it skips to, and the callouts need room between lines
- D2-xxx | The scroll region's frame clips its content in the plate, and the reader's page view does not | The first shows a cut, which is its point; the second's callout would be cut off
- D2-xxx | The stepper is drawn at its last step, with the reason the stepper's own script writes there | The caption asks for a current step and an unavailable button's reason at once; only the last step has both
- D2-xxx | Invented content keeps the code set's own Illustrative label; the table's plate takes the caption's label instead, so its caption's callout has room | DR-97, one label per piece
- D2-xxx | Every key's words describe what the code draws, where the caption says otherwise | The plate is the code; the differences go to their owners below

## For the accessibility lead and the component engineer

Where a caption in `18-components.json` and its code set differ, the plate follows the code and its key says what the code draws:

1. **Rule 18.7:** the caption gives the breadcrumb's current page a 2 px underline and the list's current place semibold words; the code draws the current page bold and not underlined, and the current place bold.
2. **Rule 18.10:** the caption says each sort button fills its heading; the code's button is as wide as its words and arrow (`max-width: 100%`), 44 px tall.
3. **Rule 18.19:** the caption names a control in the empty state; the code's empty state names its next step in words and holds no control.
4. **Rule 18.23:** the caption names disclosures for the words and the table; the code holds the disclosure for the lines in words only.

When a caption or a set changes, rerun `python3 -I work/build/scripts/phase-2/stage_c_ch18_anatomy_build.py`; a key's words live in the generator's plate functions.

## Questions for Dustin

None.

## Tested

In Chromium through Playwright, November 11, 2026, outside requests blocked except Google Fonts.

- The generator twice in a row: the 24 plates and the manifest byte for byte the same.
- Strict build into my scratch folder with every chapter in the folder (01 to 12, 17, 18, 26 and the proofs), after the last change: exit 0, no warning, 16 chapter files, 185 rules, 420 specimens, 9,538,194 bytes; chapter 18 at 1,096,881 bytes of its 1.1 MB budget.
- Every plate captured and looked at, at 1440 and at 390 px, through several rounds of fixes (callouts covering words, clipped callouts, a phone menu that clipped its title, a table whose sort arrows went missing when the set changed, the success marks hidden by their `hidden` attribute).
- By script at both widths on every plate: every callout drawn and visible, no stage wider than its frame, no frame that scrolls sideways; each bracketed target measured 44 px tall (the form's fields 48, a two-line download 60 at 390, the linked ID chip 24, as its rule sets).

## Not tested

- Any screen reader reading the plates' alts.
- Real phones, Safari and Firefox; forced colors (a picture keeps its colors, and the code sets' forced-color rules are left out of the plates).
- The plates at 1024 and 360 px, and at 200 percent text.
- `guide_check.js`: my quick run (1440 and 390 px) stopped on a page-load timeout at its line 1785 before it checked anything, so it says nothing about the plates; the engineer's full run covers them.

## Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, any asset, any board, the committed chapters page, the code sets or another owner's files changed. Nothing committed or pushed.

**Created**
- `work/build/scripts/phase-2/stage_c_ch18_anatomy_build.py`
- `work/build/guide/specimens/s-18-01-anatomy.html` to `s-18-24-anatomy.html` (24 files)
- `work/build/guide/specimens/manifest-anatomy.json`
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Anatomy-Notes.md` (this file)

**Scratch, outside the repository** (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/systems/`): builds `build-a1/` and `build-a2/`, capture scripts `plates.js` and `clip.js`, captures `shots-a1/` to `shots-a6/` and `shots-final/`, sheets in `sheets/`, and `guide-check-a2.log`.
