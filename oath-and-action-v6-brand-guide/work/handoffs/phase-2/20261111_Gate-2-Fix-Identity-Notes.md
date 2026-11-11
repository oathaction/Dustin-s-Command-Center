# Gate 2 fix pass: identity designer's notes

Oath & Action Edition 06, Phase 2, November 11, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `20261111_Gate-2-Fix-Brief.md`, my row in "Who fixes what". I read `CLAUDE.md`, my role file, chapter 02's writing rules, Master Brief section 3, the Gate 2 brief's shared sections, the fix brief, the creative director's read and scores, the drift red team's report, my round 2 notes and section 3 of handoffs V11, V12 and V15.

Work in progress: sections fill as items land. I changed my generators only and wrote no output by hand. I committed and pushed nothing.

## What changed

**CD-S1, openers.** Each reuses a drawing the chapter already has, at true size, with no new drawing. Weights as the strict build places them, frame included:

| Chapter | Opener | What it shows | Bytes placed |
|---|---|---|---|
| 01 | `s-01-opener` (`stage_b_identity_ch01.py`) | The four pillar pieces, read from the editor's `s-01-pieces` and cut to kicker, headline, Track's "as of" date, hinge divider, "What you can do", step and red button | 10,378 |
| 03 | `s-03-opener` (`stage_a_identity_s03.py`) | Seven lockups at Rule 03.2's sizes, each an `<svg>` with one `<use>` of the master `s-03-lockups` carries; L5 from 48em, L6 named in the caption | 8,786 |
| 04 | `s-04-opener` (`stage_a_identity_s04.py`) | B's display master at 160 px beside the hinge headline "The zoning code & the rent." in its own frame: title style at 56 px from 48em, H3 at 26 px on a phone | 6,545 |
| 08 | `s-08-opener` (`stage_a_identity_s08.py`) | Rule 08.2's four places, each cropped to the part that holds the lockmark, from the same place functions and masters | 15,024 |
| 12 | `s-12-index` (`stage_b_identity_ch12.py`) | The device index, moved from its place after Rule 12.1 to the opener, so the page carries it once | 6,819 |

- The library (`stage_a_identity_lib.py`) gains `SHARE` and `REF`: while `SHARE` names a plate, each master it places goes inline once with an id (`m-<file stem>`); while `REF` names it, the same lockup functions draw an `<svg>` holding one `<use href="#<plate>--m-...">`. `s-03-lockups` carries the masters; chapter 03's opener references them. The page holds each drawing once.
- An opener's fragment keeps only the shared CSS rules its classes use (`trim_css`), which also trims `s-09-opener` from 7,463 to 4,947 bytes in its file with no change on screen.
- Chapter 12's intro: my sentence is now "Hairlines, watermarks and the monogram divide and sign a page (Rules 12.1 to 12.3), and Rule 12.4 says when an open area stays plain." so the index reaches the first screen; the old sentence joins `OLD_INTRO_ADDS`.

**CD-S2, failure plates.** Every failure caption in 03, 04, 08, 09 and 12.1 to 12.4 leads `<strong>Fails Rule NN.N.</strong>` (`R()` in `stage_a_identity_chapters.py`), and `s-03-misuse` leads "Fails Rules 03.1 and 03.5." Every failure plate I draw carries the do-not-publish band, added by `fragment()` where a plate lacked it (inside a padded stage at its top, otherwise above the piece, 12 px clear), and its alt opens "Failure case: do not publish." The band's words take `--oa-color-text-primary-on-charcoal` on `--oa-color-surface-charcoal`, as stage C's bands do. Plates that gained the band: all eight in 03 and `s-03-misuse`; 04.1, 04.2, 04.3, 04.4, 04.5, 04.7, 04.8; 08.1; 09.3. Chapter 01's `s-01-21-failure` carries the editor's band already.

**CD-S3, titles.** Rule 04.3 is "Join a rule to its result with a hinge headline."; its rule's first sentence now carries the red ("..., and B takes the view's working red"). Rule 04.4 is "Set a hinge divider before the step a reader can take."; its rule opens "Set the divider between how a decision is made and what you can do about it." No other title in 03, 04, 08, 09 or 12.1 to 12.3 passes fifteen words. Rule 12.4's seventeen words stay (see Routine calls).

**CD-S5.** Rule 04.5's compact masters stand side by side under the display master; the frame is 676 px, two 330 px panels and a 16 px gap, and the display master sits centered in a panel as wide.

**CD-S7 (04).** The ask button's Charcoal keyline on red is a 1 px border in `--oa-component-button-ask-keyline-on-newsprint` (`ask()` in `stage_a_identity_s04.py`), as chapter 18's button draws it.

**CD-S8.** The "x" in `s-03-1-correct` sets in Inter 400 roman. The current step's numeral in the step marks (`stage_a_identity_lib._step_node`, used by `s-08-3-correct` and `s-12-signature-*`) sets in Inter 700, as chapter 11's marks do.

**CD-S11.** Rule 03.8's basis: "Design judgment, approved by our founder and editor in November 2026".

**DT-S4.** Rule 09.2 sets the current word bold at every size; its rule, its Bold row ("The current word, at every size; in the 48 px row all four words are bold") and its code (`.p9-cur .p9-w{font-weight:700}`) say so. The 48 px row already set all four words bold, so nothing changes on screen.

**DT-S8.** The hinge player's Reset reads "Reset the wordmark" and the lever's "Reset the lockmark", in visible words.

**DT-S13.** Rule 08.2's three long sentences: the rule opens "The lockmark signs four places: the masthead, the page header, the footer and the sign-off." and sends the sizes to its specification rows; the correct caption is "The four places at true size, each with the size it sets: the masthead, a report's page header, two footers and the corner of a social card."; the builders line opens "Pick the master by the size each place sets in the specifications, and set it on whole pixels."

**`stage_c_identity_ch17.py` under `python3 -I`.** It is a module the identity build imports, and run alone it failed at its first import, since `-I` leaves the script's folder off the path. It now adds its own folder to the path, as `stage_b_identity_ch01.py` does, and run alone it runs the identity build (`stage_a_identity_build.build()`), the same work as `promotion_identity.py specimens`. Either line in the chain now does its work.

## Routine calls

## Questions for Dustin

## Tested

## Not tested

## Change log
