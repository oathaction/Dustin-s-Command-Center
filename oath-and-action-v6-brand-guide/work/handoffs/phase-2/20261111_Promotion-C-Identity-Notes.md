# Promotion C: identity designer's notes

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261111_Promotion-Stage-C-Brief.md`, "Who does what", item 2. I read my role file, `CLAUDE.md`, the brief, the November 10 promotion brief, my November 10 promotion notes, my round 0 notes (sections 2 and 3 and "After approval"), DR-207 to DR-215 and D2-1259 to D2-1267 in the decision log, and V12's section 3.

I changed no identity master, board, ledger, `source/` or `deliverables/` file, no shell file and no file another owner keeps, and I wrote the committed chapters page at no point: every build went to my scratch folder with `--out`. The generator chain rewrote other owners' outputs with their own scripts (change log). I committed and pushed nothing; the main session's snapshot commits took in some of my files while I worked, and the files on disk are the finished ones.

**To rebuild my part:** `python3 -I work/build/scripts/phase-2/promotion_c_identity.py minimums`, then `specimens`, then `feed <scratch>` (about 3 minutes; it builds the page into the scratch folder and writes the figures), then `specimens` again so the chapters print them, then the generator chain, then `plates <scratch>` and `hashes`.

## What I promoted

1. **The print L3 (DR-210).** `lockups/20261110_L3-Horizontal-Print-Master.svg` and its White file go into use by reference, bytes unchanged, through `stage_a_identity_lib.L3["print"]`. Rule 03.2's file list and builders text, Rule 03.6's "In print" row and file list, Rule 08.2's "Masthead" row, file list and builders text, and the minimum sizes record now name the print master for print and every width but the 282 px masthead. The October master stays in `lockups/` as the record, named in the record's `record_files`. No plate drew the October master, so no plate changes for this item.
2. **The 96 px sign-off on social cards (DR-211).** `stage_a_identity_lib.sign_off` draws the 48 px master at exactly twice its size on a social card and at 48 px on a cover or poster. The proofs' link-preview card (`s-proofs-social`) and Rule 08.2's plate (`s-08-2-correct`, the corner of a 1080 px social card) draw it at 96 px. Chapter 08 now names both sizes and their places: Rule 08.1's rule, reason, basis, "48 px master" and "Display master" rows and builders text; Rule 08.2's rule, reason, caption, "Sign-off" row and builders text. Rule 03.4's builders text, which repeats Rule 08.1's ranges, and the minimum sizes record's lockmark row follow.
3. **Rule 08.2's feed figures**, measured again on the 96 px card in the built page and on the same card drawn alone on Newsprint, White, Charcoal and Prussian, and printed from `work/handoffs/phase-2/20261111_Promotion-C-Identity-Figures.json` (keys `feed`, `feed_dark`, `feed_thumbnail`). The dark-card test now counts a block of 2 by 2 pixels where it counted one pixel, with its floors unchanged (section "The dark-card test at 96 px").
4. **`s-01-21-correct`'s kicker icon**, CL-057 at 24 px, takes the switch: `<use class="oa-at-1x" href="#oa-sym-cl-057-24px"/>` with `<use class="oa-at-2x" href="#oa-sym-cl-057"/>` in one `<svg viewBox="0 0 24 24">`, through `stage_b_identity_ch01.py`. The engineer's fit symbols had landed by the time I built, and the built page draws the fit at 1x and the master at 2x. No word changed: the specimen's text, with every tag removed, is identical before and after.

## Every file in use and its source

| Item | File in use | Source | sha256 (first 12) | Same as HEAD |
|---|---|---|---|---|
| L3, print and every width but 282 px | `work/build/assets/identity/lockups/20261110_L3-Horizontal-Print-Master.svg` | The approved file itself (DR-210), unchanged | 909c756d1ece | Yes |
| Its White file | `work/build/assets/identity/prussian/20261110_L3-Horizontal-Print-Master-Prussian-White.svg` | The approved file itself, unchanged | 56565f65245d | Yes |
| L3, the record | `.../lockups/20261028_L3-Horizontal-Master.svg` and its White file | Unchanged; record only | ef6b8b5d8f38, 192a0e144c44 | Yes |
| Sign-off on a social card, 96 px | `.../lockmark/20261109_Lockmark-48px-Master-Outline.svg` at twice its size | The 48 px master in use (DR-181), unchanged | 875abce60a77 | Yes |
| Its White file, on Prussian | `.../prussian/20261109_Lockmark-48px-Master-Outline-Prussian-White.svg` | Unchanged | 6df8df3474de | Yes |
| Kicker icon at 24 px, 1x | sprite symbol `oa-sym-cl-057-24px`, from `work/build/assets/civic-line-v6/fit-24/20261111_Civic-Line-CL-057-*-24px-Fit-Black.svg` | The icon designer's in-use fit (DR-209) | not mine to hash | |

**Byte checks.** Round 0's own generator (`stage_c_identity_round0.print_l3_svg`) run on the October masters returns both print files byte for byte, and its built-in check confirms each differs from its October master only in the lockmark's size and place, the view box and the title. The view boxes match round 0's figures (1256.49 by 218.18 units, lockmark 218.18 units, 2.1818 cap heights).

## The figures

All in `work/handoffs/phase-2/20261111_Promotion-C-Identity-Figures.json`, key `feed_study` in full.

**The built page and the card alone.** The built page sets the proofs' card at a fraction of a pixel (its sign-off at 1030.984, 460.844 in the card's capture), as the page's flow gives it. The sign-off's 96 by 96 box still draws exactly the same pixels as the card drawn alone, and in the card alone each ground's sign-off matches the 96 px drawing alone, pixel for pixel. Elsewhere the two captures of the card differ in 10,199 pixels: 7,494 in the kicker and headline and 2,705 in the wordmark, which the page draws 0.16 px off the pixel grid, so their edges shade differently (up to 202 levels on an edge pixel). None falls in the sign-off's box or on the card's border, so the feed figures hold for the page as drawn. Whether the page should snap the card to whole pixels is a question for the engineer (below).

**Rule 08.2's test at 500 and 360 px** (nodes kept, red pixels; Lanczos):

| Card | 500 px | 360 px | Widths from 300 to 600 px that fail | Fewest red pixels, 300 to 600 px |
|---|---|---|---|---|
| Newsprint, the built page (printed as "our card") | 8 of 8, 52 | 8 of 8, 22 | | |
| Newsprint, alone | 8 of 8, 52 | 8 of 8, 22 | 0 | 15 |
| White | 8 of 8, 48 | 8 of 8, 20 | 0 | 13 |
| Charcoal, block floor 155 | 8 of 8, 48 | 8 of 8, 20 | 0 | 14 |
| Prussian, block floor 190, the White lever as a ninth node | 9 of 9 | 9 of 9 | 0 | |

Bicubic, bilinear and box reductions pass on every ground at both widths, with at least 20 red pixels at 360 px and 40 at 500 px. Round 0 measured the same card at 96 px as its proposal: 52 and 22 red on Newsprint and 48 and 20 on Charcoal, the same figures.

**The thumbnail path** (reduced, then saved as a JPEG at quality 75 with chroma at half size), red pixels at 500 and 360 px:

| Ground | Sign-off at 48 px | At 96 px | Widths that fail, every fourth from 300 to 600 px: 48 px, 96 px |
|---|---|---|---|
| Newsprint | 3, 0 | 41, 17 | 50 of 76, 0 of 76 |
| White | 3, 0 | 35, 17 | 54 of 76, 0 of 76 |
| Charcoal | 3, 0 | 34, 16 | 60 of 76, 0 of 76 |
| Prussian (nodes, of 9) | 1 and 0 nodes | 9 and 9 | 65 of 76, 1 of 76 (300 px) |

Rule 08.2's reason prints the Newsprint pair at 360 px, 0 and 17, from the key `feed_thumbnail`.

**Pixel fit.** The engineer's check on the 48 px master drawn at 96 px: no soft pixel at 1x or 2x, all four counters open, thinnest line 1.94 px at 1x. At 48 px it passes as before (thinnest 0.96 px).

## The dark-card test at 96 px

Round 0's dark test asks each light node to keep one pixel with every channel over a floor, set halfway between the brightest pixel the links alone leave in a node's square and the dimmest node's brightest pixel. On the 48 px card the links are 1 px wide, and the floors came out at 155 on Charcoal and 190 on Prussian.

On the 96 px card the links are 2 px wide and, on a dark ground, take the nodes' color. Reduced to 500 px, a link leaves a pixel as bright as the weakest node's: 210 against 210 on Charcoal and 255 against 255 on Prussian. A single-pixel test there cannot fail a card whose nodes are gone, and the rule's method gives floors of 210 and 255 that separate nothing.

A block of 2 by 2 pixels fixes it. A link shrunk under 1 px wide cannot fill a block, and a node 4 px or more across does. Measured the rule's way, under four filters:

| Ground | Links alone, brightest block, 500 and 360 px | Weakest node, brightest block | Floor by the rule's method |
|---|---|---|---|
| Charcoal | 115 and 87 | 205 and 196 | 155 |
| Prussian | 145 and 112 | 251 and 239 | 190 |

The floors come out at the same 155 and 190 the rule already printed, and from 300 to 600 px no width lets a node fall to the links' level. Rule 08.2's "Feed test, dark card" row now names the block and says why. The light test keeps its single pixel: there the links are Stone, and the links alone never leave a pixel under 70 (darkest 106 on Newsprint and 105 on White).

## Routine calls

- D2-xxx | `stage_a_identity_lib.L3` gains the key `print` for `lockups/20261110_L3-Horizontal-Print-Master.svg`; `today`, the October master, stays in the dictionary as the record | DR-210; the scripts that drew earlier boards still read `today`
- D2-xxx | Rule 03.2's and Rule 03.6's file lists name the print master in place of the October master, and Rule 08.2's list adds it after the masthead master | A rule's file list names the files in use; the October master stays in `lockups/` as the record
- D2-xxx | Rule 08.2's "Masthead" row and builders text name L3's print master for a masthead in print | The round 0 notes' "After approval" paragraph names Rule 08.2, and a masthead in print is the one place that rule reaches L3 off screen
- D2-xxx | The minimum sizes record's L3 row lists the print master and the masthead master in `files`, their White files in `prussian_files`, and the November 8 and October masters in `record_files`; its print figures (3.13 mm capitals, a 0.269 in lockmark at 1.55 in) are read from round 0's figures file | The record names files in use apart from the record, as the lockmark row already does; figures come from a file (D2-805)
- D2-xxx | `stage_a_identity_lib.sign_off` draws the sign-off at its place's size from the 48 px master: 96 px on a social card, 48 px on a cover or poster; `lockmark()` keeps its ranges, so 96 px anywhere else still takes the display master | DR-211 names the social card only; a lockmark drawn at 96 px for any other job keeps Rule 08.1's display master
- D2-xxx | `_social` takes `sign`, 96 by default; the round 0, Q1 to Q4 and stage B scripts that measured the 48 px card now ask for `sign=48`, and `stage_a_identity_q_measure.feed_test` stops on a sign-off that is not 48 px | A rerun of an earlier measure keeps its record, and the old 48 px counter can never misread the 96 px card
- D2-xxx | Rule 08.2's plate shows the social card's corner with the 96 px sign-off, its label reads "96 px at the bottom right of a social card; 48 px on a cover or poster", and its caption and alt say 96 px | The plate draws a social card, and DR-211 sets a social card's sign-off at 96 px; a 48 px corner would contradict the rule beside it
- D2-xxx | That corner grows from 360 by 216 px to 408 by 264 px, the mark still 72 px in from the card's right and bottom edges | At 360 by 216 the 96 px mark left 48 px of card above it and nearly met the corner's label; the plate stays 802 px wide
- D2-xxx | Chapter 08's words name both sign-off sizes: Rule 08.1's rule, reason, basis, two specification rows and builders text; Rule 08.2's rule, reason, caption, "Sign-off" row and builders text; and Rule 03.4's builders text on the 48 px master's sizes | The brief asks for the words that name the sign-off's sizes and places; Rule 03.4 repeats Rule 08.1's ranges
- D2-xxx | Rule 08.2's reason gives the cause of the 96 px sign-off with its figures from the figures file: a thumbnail saved as a JPEG after the reduction leaves the lever no red pixels at 48 px and 17 at 96 px, on our card at 360 px | The reason the earlier text gave, that the 48 px master keeps the sign-off visible at 500 px, no longer explains the size in use
- D2-xxx | The feed test runs on the card in the built page (Newsprint, the figures printed for "our card") and on the same card drawn alone on all four grounds, with a check that both put the same pixels in the sign-off's box | The page is what a reader sees; the card alone gives the other grounds, and the check ties the two together
- D2-xxx | Rule 08.2's dark-card test counts a block of 2 by 2 pixels over the floor in each node's square, where it counted one pixel; the floors stay 155 on Charcoal and 190 on Prussian | On the 96 px sign-off the links run 2 px wide and take the nodes' color, so at 500 px the links alone reach the weakest node's brightest pixel (210 and 210 on Charcoal, 255 and 255 on Prussian) and a single-pixel test could not fail a missing node. A link shrunk under 1 px cannot fill a block: links alone reach 115 and 145, the weakest node 196 and 239, and the rule's own halfway method gives 155 and 190 again
- D2-xxx | "Feed test, our card" prints all four grounds, White added, and joins White and Charcoal in one sentence when their figures match | The brief asks for the four grounds; one sentence avoids two identical ones
- D2-xxx | Rule 03.2's builders text says the print master sets the lockmark at the masthead's proportion and drops any claim that L3 keeps one proportion everywhere | The 196 px minimum form on screen is built from the pixel masters at 2.43 cap heights, which DR-210 does not change (question 1)
- D2-xxx | `s-01-21-correct`'s kicker icon, CL-057 at 24 px, takes the switch in `stage_b_identity_ch01.topic`, which gives it to any 24 px drawing of the 37; `upgrade_24` upgrades a drawing an earlier run placed as the master alone | DR-209 and D2-1265; the editor's build writes the inline master and this step swaps it, so a rerun of either gives the same file
- D2-xxx | The list of 37 in `stage_b_identity_ch01.FIT_24` is chapter 10's construction file, section 10, less the four pillar icons, checked against the icon designer's in-use manifest | One list, D2-587's; the check shows the two agree (37 of 37)

## Questions for Dustin

1. **L3 at its 196 px minimum on screen.** DR-210 gives the print master "every width but the 282 px masthead". On screen, though, L3 under about 465 px wide cannot take the print master without drawing the wordmark's display master under 40 px tall, which Rule 03.4's ranges forbid. The guide's 196 px minimum form (Rule 03.4's sheet) is built from the pixel masters, the 16 px wordmark master and the lockmark's 24 px master at 34 px, so its lockmark stands 2.43 cap heights, as it did before. Round 0's plate said the same: under 37 px capitals a page draws L3 from the pixel masters, and the proposal left them alone. *Recommendation:* keep the minimum form as drawn, and add one sentence to Rule 03.2's builders text at the next identity pass: "On screen, under 40 px tall, build L3 from the pixel masters, as the masthead and the 196 px minimum do." I left the words as they stand and took out the clause I first wrote that L3 keeps one proportion everywhere.

## For the main session and other owners

- **The print master's title.** Both print files still carry round 0's title, which ends "Proposed for board C; the October master stays in use until approved". The brief keeps their bytes, so I left them. The guide strips titles when it inlines a master, so no reader sees it, but the asset package would copy the file with that title. *Recommendation:* when Phase 3 copies the identity files, write the print master as a new dated file beside it with a title that says it is in use (DR-210), as the November 10 promotion did for L3's masthead master, and keep this file as the record.
- **Rule 08.1's plate.** `s-08-1-correct` shows the display master at 96 px among the four masters. A social card now draws the 48 px master at 96 px, and Rule 08.1's words say so, but a reader comparing the plate with the card could ask why one 96 px mark is fine-lined and the other heavy. *Recommendation:* at the next identity pass, set the plate's display sample at 120 px, with its caption. Not done here: the brief names no change to that plate.
- **Creative director and editor.** The dark-card test changed its unit from one pixel to a block of 2 by 2 (section above). It is a routine call, since the floors stay as printed, but it changes how a builder counts. New reader text for the editor's copy edit: Rule 03.2's builders text (last three sentences); Rule 03.4's builders text (the lockmark sentence); Rule 03.6's "In print" row; Rule 08.1's rule, reason, basis, "48 px master" and "Display master" rows and builders text; Rule 08.2's rule, reason, caption, "Masthead", "Sign-off", "Feed test, dark card" and "Feed test, our card" rows and builders text; the proofs' "Lockmark" and "Feed test" specifications; the alt of `s-proofs-social` and `s-08-2-correct` and the label on its sign-off place; the minimum sizes record's L3 and lockmark rows.
- **Engineer.** No shell change needed from me. The kicker's markup is the pattern your check asks for, and the built page finds both symbols. `stage_a_identity_q_measure.feed_test` now stops if the card's sign-off is not 48 px, so `promotion_identity.py checks` would stop at its feed step if anyone reran it; `promotion_c_identity.py feed` is the test for the card in use.
- **Engineer, the card's offset.** In the built page the proofs' 1200 px card lands 0.16 px off the pixel grid (its top at y 472905.84 in a 1700 px window, 490092.83 at 1440 px), from the heights above it in the flow. The sign-off still snaps to whole pixels, but the wordmark and the type do not, so at 1x they draw slightly softer than the card drawn alone. The masthead and L3 plates may share it. A plate stage that starts on a whole pixel would remove it; I did not test where the fraction comes from.
- **Systems designer.** The chain's chapter 10 step stopped on my first run (`20261110_Civic-Line-V6-Inventory.json: 125 drawings, expected 124`) while CL-075 was arriving; on my later runs it passed.
- **Round 1, chapter 18.** On my last run the strict build stopped on 35 warnings, all in Rule 18 (missing specimens and code sets, and its manifest listing specimens no chapter places). With chapter 18's chapter file, manifest and specimens left out of a copy, the strict build passes with 0 warnings.
- **D2 numbers.** The routine calls carry D2-xxx for you to number.

## Tested

- The print files' sha256 against HEAD (unchanged), and their regeneration from the October masters by round 0's generator (byte for byte, with only the lockmark's size and place, the view box and the title differing from the October files).
- The identity build reproduced the committed files byte for byte before my changes; after them it changes `03-identity.json`, `08-lockmark.json`, `manifest-identity.json` (two entries: `s-08-2-correct`, `s-proofs-social`), `s-03-minimums.html`, `s-08-2-correct.html` and `s-proofs-social.html`, and the minimum sizes record. `stage_b_identity_ch01.py` changes only `s-01-21-correct.html`, and a second run changes nothing.
- `s-01-21-correct`'s text with every tag removed: identical before and after.
- My list of 37 against the icon designer's in-use manifest: the same 37.
- Rule 08.2's feed test on the built page's card at 1x, and on the card drawn alone on all four grounds, with the sign-off's pixels compared between the two; four filters at 500 and 360 px; every width from 300 to 600 px; the thumbnail path at 48 and 96 px on all four grounds; the floor study with single pixels and with 2 by 2 blocks.
- The engineer's pixel-fit check on the 48 px master at 48 and at 96 px.
- The generator chain from the project folder (V12's section 3), three full runs, each script exit 0 on the last; `guide_build.py --strict --out` into my scratch folder: 0 warnings before chapter 18 landed; 35 warnings, all Rule 18, after; 0 warnings on a copy without chapter 18's files (12 chapter files, 132 rules, 307 specimens, 6,868,998 bytes).
- Every changed plate in the built page at 1440 and 390 px, at 1x and 2x: `s-08-2-correct`, `s-proofs-social`, `s-03-minimums` and `s-01-21-correct`. The sign-off corner at 2x and 1x enlarged; the kicker icon at 1x and 2x enlarged, with the shell's switch showing the fit at 1x and the master at 2x. The rule text of Rules 03.2, 03.4, 03.6, 08.1 and 08.2 at 1440 and 390 px. Two looks led to changes: the sign-off corner grew, and the minimum sizes table's L3 print cell lost a repeated "1.55 in".
- The print master and the October master at 149 and 465 px wide, and the 96 px sign-off, on Newsprint, White, Charcoal and Prussian at 1x and 2x.
- A scan of every new word in the chapters, specimens, manifest, record and these notes for em and en dashes: none.

## Not tested

- The guide check (`guide_check.js`) result is added below if it finishes before I hand back.
- Firefox, Safari, real phones and screens between 1x and 2x for the kicker's switch; Chromium only.
- A real upload of the 96 px card to any platform; the JPEG figures come from Pillow's encoder.
- Print: no proof was printed with the print master; round 0's PDF measured at 300 dpi stays the evidence.
- `promotion_identity.py checks`, `stage_a_identity_q_measure.py`, `stage_b_identity_drawings.py` and `stage_c_identity_round0.py` were not rerun after my edits to them, since each writes figures, boards or masters that stand as records; I checked the edits by importing the modules and by reading them.
- The editor's copy edit of the new words, and the creative director's look.

## Change log

Created:
- `work/build/scripts/phase-2/promotion_c_identity.py`
- `work/handoffs/phase-2/20261111_Promotion-C-Identity-Figures.json`
- `work/handoffs/phase-2/20261111_Promotion-C-Identity-Notes.md` (this file)

Modified, scripts:
- `work/build/scripts/phase-2/stage_a_identity_lib.py`: `L3["print"]`, `SIGN_OFF`, `sign_off()`, `FIGURES_PROMOTION_C` and `figures()` reading it
- `work/build/scripts/phase-2/stage_a_identity_proofs.py`: `_social(sign=96)`, the card's specifications, feed line, alt and notes
- `work/build/scripts/phase-2/stage_a_identity_s08.py`: the sign-off corner at 96 px, 408 by 264 px, its label, alt and notes
- `work/build/scripts/phase-2/stage_a_identity_chapters.py`: Rules 03.2, 03.4, 03.6, 08.1 and 08.2; `_feed`, `_feed_dark`, `_thumb`
- `work/build/scripts/phase-2/stage_a_identity_s1.py`: `update_minimums` for the L3 and lockmark rows and the updated line
- `work/build/scripts/phase-2/stage_b_identity_ch01.py`: `FIT_24`, `topic()` with the switch, `upgrade_24()`
- `work/build/scripts/phase-2/stage_a_identity_q_measure.py`, `stage_b_identity_drawings.py`, `stage_c_identity_round0.py`: draw the 48 px card they measured (`sign=48`); the Q1 to Q4 feed test stops on a sign-off that is not 48 px

Modified, generated by those scripts:
- `work/build/assets/identity/20261028_Identity-Minimum-Sizes.json`
- `work/build/guide/chapters/03-identity.json`, `08-lockmark.json`
- `work/build/guide/specimens/manifest-identity.json`, `s-03-minimums.html`, `s-08-2-correct.html`, `s-proofs-social.html`, `s-01-21-correct.html`

Rewritten by the chain with other owners' scripts, not my changes: chapter 05, 10 and 11 outputs, including `05-color.json`, `s-10-4-correct.html`, `s-10-9-correct.html`, `s-10-opener.html` and `s-11-12-correct.html`, from the systems designer's work in progress.

Scratch builds, captures and studies: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/promotion-c/identity/` (`guide.html`, `guide-no18.html` and their build reports, `feed/`, `plates/`, `look/`, `pfc/`, `study/`).
