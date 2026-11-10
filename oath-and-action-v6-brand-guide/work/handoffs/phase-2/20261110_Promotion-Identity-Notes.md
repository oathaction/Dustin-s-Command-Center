# Promotion: identity designer's notes

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261110_Promotion-Brief.md`, "Who does what", item 3. I read my role file, `CLAUDE.md`, the brief, DR-129 to DR-131, DR-142, DR-145, DR-180 to DR-186, D2-533 to D2-550 and D2-709 to D2-718, my stage B notes, figures, plates and script, the guide's identity sources and the guide build's usage header. Later I read the engineer's promotion notes on the pillar icons' switch, at the coordinator's request.

I changed no existing identity master, board, ledger, `source/` or `deliverables/` file, and no file another owner keeps. I committed and pushed nothing. The main session's snapshot commits took in some of my files while I worked; the files on disk are the finished ones.

**To rebuild:** `python3 -I work/build/scripts/phase-2/promotion_identity.py masters`, then `specimens`, then `checks <scratch>` and `density <scratch>`. Run `specimens` once more after `checks`, so the chapters print the figures it writes.

## What I promoted

**1. The end mark (DR-180).** Ampersand B's pixel masters, fit B, now close an article on a 1x screen, a screen that gives each CSS pixel one device pixel: the 14 px master in 17 px body text and the 12 px master in 15 px text, each sitting on the baseline (`vertical-align: 0`). Every other screen keeps today's drawing, the 16 px master at 16/14 of the cap height. That is my stage B recommendation (question 2), which Dustin approved with every recommendation (D2-709). Both drawings sit in the last word's no-wrap span and a media query in the specimen's own style shows one. Rule 04.6's plate is the only specimen that draws the end mark; I searched all 259 specimens. It gains a third paragraph, in 15 px text, so the 12 px master is drawn somewhere in the guide. Rule 03.4's specification, Rule 04.6's text, figures, files and builders text, and the minimum sizes record now name the pixel masters.

**2. The lockmark masters (DR-181).** `stage_a_identity_lib.LOCK` now names the rebuilt 24 and 48 px files, so every specimen that draws them takes them: chapter 08's four masters and four places, the identity proofs' masthead, sign-off and letterhead footer, chapter 03's lockup sheet, minimum sheet, mastheads and masthead failure. The 16 px master stays (D2-542). L3's masthead master carried the 48 px master's rects, so it gets a new dated file beside the November 8 one, with only the lockmark's paths and the title changed. The October L3 draws circles from the display drawing, so it needs no new file. The minimum sizes record and chapters 03 and 08 name the files in use, and Rule 08.1 no longer says the 48 px master parts into stripes.

**3. L6 centered (DR-182).** The wordmark and tagline move down 14.72 of L6's 300 units, 9.3 px at 884 px: the wordmark's top from 52.1 to 61.4 px and the tagline's from 107.6 to 116.9 px in the specimen. The strip, the lockmark at 739.1 by 47.3 px, the left margin and every size stay. `stage_a_identity_s03.l6` centers by default; the two scripts that drew earlier boards ask for the old position, so their records hold.

**4. The specimen manifest's notes.** Each note for these items now names the final in use and its DR: `s-04-6-correct` (DR-180), `s-03-l6` (DR-182), and `s-08-1-correct`, `s-08-2-correct`, `s-proofs-masthead`, `s-proofs-social`, `s-proofs-letterhead`, `s-03-lockups`, `s-03-4-correct`, `s-03-6-correct` and `s-03-6-failure` (DR-181).

## Every final and its source

| Item | Final in use | Source | sha256 (first 12) |
|---|---|---|---|
| End mark, 17 px text, 1x | `work/build/assets/identity/ampersand/20261109_Amp-B-14px-End-Mark-Fit-B.svg`, 13 by 13 px | The approved file itself, unchanged (DR-180) | 42d921bf1ec9 |
| End mark, 15 px text, 1x | `.../ampersand/20261109_Amp-B-12px-End-Mark-Fit-B.svg`, 11 by 11 px | The approved file itself, unchanged | 340904c4ba86 |
| Their White files | `.../prussian/20261109_Amp-B-14px-End-Mark-Fit-B-Prussian-White.svg`, `...-12px-...` | Unchanged | 26a1b19d40bd, e636bee6f4b0 |
| End mark, other screens and text sizes | `.../ampersand/20261028_Amp-B-16px-Master.svg` at 16/14 of the cap height | Today's drawing (DR-130), unchanged | |
| Lockmark, 24 px | `.../lockmark/20261109_Lockmark-24px-Master-Outline.svg` | The approved file itself, unchanged (DR-181) | 209ec533cd49 |
| Lockmark, 48 px | `.../lockmark/20261109_Lockmark-48px-Master-Outline.svg` | The approved file itself, unchanged | 875abce60a77 |
| Their White files | `.../prussian/20261109_Lockmark-{24,48}px-Master-Outline-Prussian-White.svg` | Unchanged | a30d2d007dc9, 6df8df3474de |
| Lockmark, 16 px | `.../lockmark/20261028_Lockmark-16px-Master.svg` | Stays (DR-181, D2-542) | a7edf0fa5b76 |
| L3, masthead master | `.../lockups/20261110_L3-Horizontal-Master.svg` (new) | `lockups/20261108_L3-Horizontal-Master.svg` with the 48 px master's drawing swapped for the rebuilt file's and a new title | 90034ceaf399 |
| L3, masthead, White | `.../prussian/20261110_L3-Horizontal-Master-Prussian-White.svg` (new) | The same from `prussian/20261108_L3-Horizontal-Master-Prussian-White.svg` | 4f6dfef714ea |
| L6 | Drawn in `s-03-l6` by `stage_a_identity_s03.l6`; no master file | My stage B proposal, section 3, its 14.72 units (DR-182) | |

Every file above that already existed hashes the same as at HEAD. The earlier 24 and 48 px files and the November 8 L3 files stay beside them as the record (`stage_a_identity_lib.LOCK_RECT`, `L3["masthead_rect"]`).

## Check figures

All figures are in `work/handoffs/phase-2/20261110_Promotion-Identity-Figures.json`.

**Same pixels at each master's own size (DR-145).** I built the guide page, then a control page from the same chapters and specimens with the earlier lockmark and L3 files swapped back into the identity specimens, so the two pages differ only in those drawings. In Chromium at 1x and 2x I captured every 24 and 48 px lockmark and every L3 masthead master in the identity specimens and compared each pair pixel for pixel. 28 of 32 are identical. The four that differ are the two drawn away from their own size, at 1x and 2x: L3 at its 196 px minimum, whose lockmark is the 24 px master at 34 px (358 pixels differ at 1x: the stripes are gone, which is what DR-145 asked for), and the masthead failure, L3 squeezed to 150 px (160 pixels at 1x). Alone, on two pages with each pair at the same place, the rebuilt 24 and 48 px masters and the new L3 match the earlier files on Newsprint, White, Charcoal and Prussian at 1x and 2x: 24 of 24.

**Byte checks.** The new L3 is the November 8 file with only the nested lockmark's contents and the title changed (asserted, true); its White file is the November 8 White file with only the lockmark's White drawing and the title changed (true). The wordmark's 24 px master sits in it byte for byte.

**Feed test (D2-468), run again on the built page.** The proofs' social card at 1x, reduced with Lanczos: at 500 px, 8 of 8 nodes and 11 red pixels; at 360 px, 8 of 8 nodes and 5 red pixels, with the rebuilt 48 px master. The control page with the November 8 master gives the same: 8 and 11, 8 and 5. The standalone control still fails the display master (1 red pixel at 500 and 360 px, 0 of 8 nodes at 360 px) and passes the 48 px master. The margin stays 5 against a floor of 4.

**The end mark in the built page.** At 1x the pixel master shows and the smooth drawing is hidden, in all three paragraphs; beside a probe capital H set in the same span, B covers exactly the H's rows: 13 of 13 in 17 px text on Newsprint and on Charcoal, 11 of 11 in 15 px text, with every ink pixel at full color. At 2x the smooth drawing shows, 14.12 px tall in 17 px text and 12.47 px in 15 px text. The fit figures the chapters print come from the stage B measurement Dustin approved them on: 13.0 px against capitals 12.38 px in 17 px text and 11.0 against 10.88 in 15 px text, on the capitals' rows at four positions of the line.

**L6.** The guide's L6 and my stage B proposal produce the same markup, masters inlined, and draw the same pixels at 1x and 2x, rendered at the same place.

**Pixel-fit check** (`icon_pixel_fit_check.py`), on the finals at their own sizes, B's masters on square copies (D2-548): all four pass at 1x and 2x, with no soft pixel and every counter open (B: 2 of 2; lockmark: 4 of 4). Thinnest line 0.99 and 1.01 px for B at 1x, 1.02 and 0.96 px for the 24 and 48 px lockmarks.

**Strict build and guide check.** `guide_build.py --strict` writes the page with 0 warnings. `guide_check.js` at 1440, 1024, 390 and 360 px passed with 0 failures on the page as it stood with my changes in (9 chapters, 100 rules, 233 specimens, 761 same-page links). During my last runs chapter 10's round 2 work landed in the page (10 chapters, 259 specimens) and the check then reports 8 failures, all in `s-10-*` specimens: the studio word "gate" in `s-10-lib-03` and 37 glyphs at a size their family does not use, from `s-10-list-41`, at each width. None touches chapters 03, 04 or 08 or the proofs. The last run, after my last change (Rule 04.6's builders text), gives the same: the strict build with 0 warnings, and the check with 8 failures across the four widths, every one in `s-10-*`.

**Looks.** I looked at every changed plate at 1440 and 390 px with the masthead hidden, and at Rule 04.6, L6 and Rule 08.1 at 2x as well; at the end marks enlarged at 1x and 2x; at L3's 34 px lockmark and the squeezed L3 before and after, enlarged. Two looks led to changes: the squeezed L3's lockmark no longer parts into stripes, so the failure's alt, note and caption no longer say its nodes run together; and that caption first left a three-word last line at 1440 px, so I rephrased it.

## The end mark between 1x and 2x

The engineer's pillar icons draw the fit below 2 device pixels per CSS pixel and the master from 2x; my end mark showed its pixel master only at exactly 1x. I measured both end mark drawings, each forced, beside a capital H at 1, 1.25, 1.5, 1.75 and 2x, in 17 and 15 px text on Newsprint, with the line at four positions between pixels (`promotion_identity.py density`). Full: share of B's ink pixels at full color. Soft: share between 5 and 95 percent. Rows: device rows B's top stands over H's top, and its last row under H's last.

| Text, scale | Pixel master: full, soft | Rows over, under | Smooth drawing: full, soft | Rows over, under |
|---|---|---|---|---|
| 17 px, 1x | 100, 0 percent | 0, 0 | 45, 55 | 0 to 1, 1 to 2 |
| 17 px, 1.25x | 46 to 47, 53 to 54 | 0 to 1, 0 to 1 | 52 to 53, 47 to 48 | 0 to 2, 1 to 2 |
| 17 px, 1.5x | 65 to 66, 34 to 35 | 1, 0 | 57 to 58, 42 to 43 | 1 to 3, 0 to 2 |
| 17 px, 1.75x | 61 to 62, 38 to 39 | 1, 0 | 61 to 64, 36 to 39 | 1 to 3, 0 to 2 |
| 17 px, 2x | 100, 0 | 1, 0 | 67, 33 | 1 to 3, 1 to 3 |
| 15 px, 1x | 100, 0 | 0, 0 | 38, 62 | 0 to 1, 1 to 2 |
| 15 px, 1.25x | 39 to 42, 58 to 61 | 0, 0 | 48, 52 | 0 to 2, 1 to 2 |
| 15 px, 1.5x | 55 to 63, 37 to 45 | 0, 0 | 52 to 54, 46 to 48 | 0 to 2, 1 to 2 |
| 15 px, 1.75x | 55 to 58, 42 to 45 | 0 to 1, 0 to 1 | 59 to 60, 40 to 41 | 0 to 2, 1 to 3 |
| 15 px, 2x | 100, 0 | 0, 0 | 64, 36 | 0 to 2, 1 to 3 |

Both drawings keep B's two counters open at every scale. At 1.25x in 15 px text the smooth drawing also shows one enclosed pixel under half coverage in the notch between the crossing and the arm; it is one device pixel and no counter closes.

Between 1x and 2x the pixel master's pixels fall across device pixels. At 1.25x it is softer than the smooth drawing (46 against 52 percent full in 17 px text, 39 to 42 against 48 in 15 px text). At 1.5x it scores higher on full color, but its rows double unevenly, one CSS row to one device row and the next to two, and enlarged it reads as a lumpy staircase, where the smooth drawing reads as B. The pixel master holds B on the capitals' rows more steadily at every scale; the smooth drawing moves up to 3 device rows with the line, as it does on the 2x screens Dustin approved it for. The smooth drawing's master never fails here the way the pillar master does under 2x, where its line falls under one device pixel and its counters fill.

**The rule I kept:** the end mark shows its pixel master only at exactly one device pixel per CSS pixel, `@media (resolution: 1dppx), (-webkit-device-pixel-ratio: 1)`, and the smooth drawing on every other screen, 1.25x, 1.5x and zoomed pages included. A browser that reads neither query keeps the smooth drawing. Rule 04.6's builders text now says why.

One line each, for chapters 03 and 09:

- **End mark:** its pixel master is drawn for one device pixel per CSS pixel, so it shows only on 1x screens; on any denser screen its pixels fall between device pixels and its edges soften, and the smooth master draws B better.
- **Pillar icons:** a 24 px icon keeps its fit up to 2x, since below 2x the master's line falls under one device pixel and its counters fill, and the fit keeps every counter and gap.

## Routine calls

- D2-xxx | The end mark shows its pixel master only at exactly 1 device pixel per CSS pixel (`resolution: 1dppx`, or `-webkit-device-pixel-ratio: 1`), and the smooth drawing on every other screen | The density figures above: between 1x and 2x the pixel master softens or steps unevenly, and the smooth drawing keeps its counters and its shape
- D2-xxx | The switch lives in the specimen's own style (`END_CSS` in `stage_a_identity_s04.py`), and a browser that reads neither query keeps the smooth drawing | The shell's CSS is the engineer's, and the smooth drawing is acceptable on every screen
- D2-xxx | `end_b` stays today's smooth drawing and the new `end_mark` pairs it with the pixel master | The stage B board script and the Q1 to Q4 measurement call `end_b` for today's end mark, so a rerun keeps their records
- D2-xxx | Rule 04.6's plate adds a third paragraph, in 15 px text on Newsprint | The 12 px master serves 15 px text, and no plate drew it
- D2-xxx | The end mark's fit figures in chapters 03 and 04 come from the stage B measurement Dustin approved the fits on, copied into the promotion figures with its source named; the built page confirms the rows at 1x | They are the approved figures, measured at four positions of the line, which the built page cannot vary
- D2-xxx | `stage_a_identity_lib.LOCK` names the rebuilt 24 and 48 px files, and `LOCK_RECT` keeps the earlier two for the scripts that drew earlier boards | The stage B script traces from the earlier files and compares with them, and the fix-pass board shows them
- D2-xxx | `stage_a_identity_s1.py` writes the November 8 48 px master and L3 under their own names (`LOCK_RECT[48]`, `L3["masthead_rect"]`) | Otherwise a rerun would write the November 8 drawing over the rebuilt file in use
- D2-xxx | L3's new masthead master is the November 8 file with only the nested lockmark's contents and the title changed, asserted by the script | The brief: a master that embeds a changed drawing gets a new dated file beside it, and nothing else in it moves
- D2-xxx | The October L3 master gets no new file | It draws the lockmark as circles from the display drawing, so no rebuilt path is in it
- D2-xxx | The masthead failure (`s-03-6-failure`) draws the masthead master in use, and its alt, note and Rule 03.6's caption now name the capitals under 14 px and L3 under its 196 px minimum | A producer squeezes the file in use, and with the rebuilt master the lockmark's nodes no longer run together
- D2-xxx | `stage_a_identity_s03.l6` centers by default without the dots; the fix-pass and stage B board scripts ask for `centered=False` | The guide takes the final, and the boards keep the L6 they showed
- D2-xxx | The feed figures the chapters print now come from `20261110_Promotion-Identity-Figures.json`, read before the Q1 to Q4 file for the keys `feed` and `endmark_fit` | The feed test ran again with the rebuilt master, and the Q1 to Q4 file stays the record of November 8
- D2-xxx | The pixel comparison runs on a control page built from the same chapters and specimens with the earlier files swapped back | Two pages that differ only in the drawings put each pair at the same place; Chromium shades a curve's edge a few levels differently at different places (up to 6 levels on 98 pixels of the wordmark, none in the lockmark)
- D2-xxx | The letterhead's print proof is not printed again | It sits in `work/boards/phase-2/stage-a/proofs/`, and the brief keeps boards closed to me; the specimen's note says the proof carries the earlier 24 px file

## Questions for Dustin

1. **One density rule or two.** The pillar icons switch at 2x and the end mark at exactly 1x, so on a 1.25x or 1.5x laptop screen a pillar icon draws its fit and the end mark its smooth drawing. *Recommendation:* keep the two rules. Each follows what its own drawing does at those densities (the figures above and the engineer's), and readers never see the two marks side by side at the same size.

## For the main session and other owners

- **Letterhead proof.** The PDF that the proofs' letterhead specimen links to, `work/boards/phase-2/stage-a/proofs/20261107_Letterhead-Proof.pdf`, was printed with the earlier 24 px lockmark file. If you open that folder to me, `stage_a_identity_proofs.write_letterhead(pdf=True)` would print it with the file in use; I would write it as a new dated file beside the old one, which needs a one-line change to `PDF` there.
- **Engineer.** No shell change is needed. If the shell or a later chapter ever ends an article with B outside a specimen, it needs the end mark's two drawings and `END_CSS`'s query, which differs from the `oa-at-1x` and `oa-at-2x` classes that switch at 2x.
- **Editor.** New reader text for your copy edit: Rule 04.6's rule, reason, specifications, caption and builders text; Rule 03.4's end mark line; Rule 03.2's L6 line, builders text and the L6 plate's caption; Rule 03.6's failure caption; Rule 08.1's reason, basis and builders text; the alt text of `s-04-6-correct`, `s-03-l6` and `s-03-6-failure`.
- **D2 numbers.** The routine calls carry D2-xxx for you to number.

## Tested

- The new L3 and its White file against the November 8 files, by script: only the lockmark's contents and the title changed; the wordmark's 24 px master and the rebuilt 48 px master's drawing sit in it byte for byte.
- Every existing final's sha256 against HEAD: unchanged.
- The identity build reproduces today's specimens and chapters byte for byte before my changes (only id prefixes differed when the letterhead step was skipped, which the promotion script now matches); after them it changes the 11 specimens, the manifest and chapters 03, 04 and 08 above, and nothing else.
- In Chromium at 1x and 2x: every 24 and 48 px lockmark and L3 masthead master in the built page against the control page (28 of 32 identical, the 4 others drawn away from their own size); the masters alone on four surfaces (24 of 24).
- The feed test on the built page and on the control page, and the standalone control.
- The end mark in the built page at 1x and 2x: which drawing shows, its height, and its rows beside a probe H, in all three paragraphs.
- The end mark's two drawings at 1, 1.25, 1.5, 1.75 and 2x, at four positions of the line, in 17 and 15 px text; looked at enlarged.
- L6 against my stage B proposal: markup, and pixels at 1x and 2x.
- The engineer's pixel-fit check on the four finals at 1x and 2x.
- `guide_build.py --strict` and `guide_check.js` at 1440, 1024, 390 and 360 px.
- Every changed plate looked at in the built page at 1440 and 390 px, three at 2x.
- A scan of my new words for em and en dashes: none.

## Not tested

- Firefox, Safari and real devices. 1.25x to 2x screens were simulated with Chromium's device scale factor; browser zoom was not tried, and neither was the `-webkit-device-pixel-ratio` query in WebKit.
- Windows text rendering and hinting, where the text's baseline may land differently from B's.
- The end mark at text sizes other than 15 and 17 px in the built page, and on White or Prussian.
- A real feed upload and JPEG compression; print, and the letterhead proof with the rebuilt file.
- The naming test and the look-alike check, which are written for icons (as in stage B).
- The stage B board script, the fix-pass board script and `stage_a_identity_s1.py` were not rerun after my edits, since each writes boards or masters; I checked their edits by reading them and by importing the modules.
- The editor's copy edit of the new words, and the creative director's look.

## Change log

Created:
- `work/build/assets/identity/lockups/20261110_L3-Horizontal-Master.svg`
- `work/build/assets/identity/prussian/20261110_L3-Horizontal-Master-Prussian-White.svg`
- `work/build/scripts/phase-2/promotion_identity.py`
- `work/handoffs/phase-2/20261110_Promotion-Identity-Figures.json`
- `work/handoffs/phase-2/20261110_Promotion-Identity-Notes.md` (this file)

Modified:
- `work/build/assets/identity/20261028_Identity-Minimum-Sizes.json`: the L3, L6, ampersand B and lockmark rows and the updated line
- `work/build/guide/chapters/03-identity.json`, `04-ampersand.json`, `08-lockmark.json`
- `work/build/guide/specimens/manifest-identity.json`
- `work/build/guide/specimens/`: `s-03-4-correct.html`, `s-03-6-correct.html`, `s-03-6-failure.html`, `s-03-l6.html`, `s-03-lockups.html`, `s-04-6-correct.html`, `s-08-1-correct.html`, `s-08-2-correct.html`, `s-proofs-letterhead.html`, `s-proofs-masthead.html`, `s-proofs-social.html`
- `work/build/scripts/phase-2/`: `stage_a_identity_lib.py`, `stage_a_identity_s03.py`, `stage_a_identity_s04.py`, `stage_a_identity_s08.py`, `stage_a_identity_proofs.py`, `stage_a_identity_chapters.py`, `stage_a_identity_s1.py`, `stage_a_identity_fix_boards.py`, `stage_b_identity_drawings.py`

Unchanged, checked: `work/build/guide/chapters/proofs.json` and `s-03-minimums.html` (the table's columns did not change).

Scratch renders, captures and pages: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/promotion/identity/`.
