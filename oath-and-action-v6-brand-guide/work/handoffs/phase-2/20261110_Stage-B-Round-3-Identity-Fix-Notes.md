# Stage B round 3 fix pass: identity designer's notes

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261110_Stage-B-Round-3-Fix-Brief.md`, "The identity designer" and the craft items routed to me. I am a new agent in this role. I read the brief, `CLAUDE.md`, my role file, the writing rules, my round 2, promotion and stage A notes, section 4 of the editor's round 2 notes (4b, 4c, 4e), the items the brief routes to me in the four round 3 reports (PP-M2, PP-S1, PP-S2; CD-S1, CD-S10, CD-S11; CA-S5, CA-S6, CA-S10, CA-S11, CA-S13, CA-S14, CA-S18), and the editor's two requests in `20261110_Stage-B-Round-3-Editor-Fix-Notes.md`.

Every change is in a generator. Nothing committed or pushed. No `source/`, ledger, `deliverables/`, board, master, asset final or other owner's file changed.

**To rebuild my part:** `python3 -I work/build/scripts/phase-2/promotion_identity.py specimens` (the identity build without the letterhead print: chapters 03, 04, 08 and 09, the proofs, and Rules 12.1 to 12.4 merged into the shared chapter 12 file), then, after the editor's `guide_editor_ch01.py` or `guide_editor_build.py`, `python3 -I work/build/scripts/phase-2/stage_b_identity_ch01.py`. My chapter 12 writer keeps the systems designer's rules, so the two chapter 12 scripts run in either order.

## Items

| Item | What I did | Status |
|---|---|---|
| ED 4b | All eight rows of chapter 09's table applied in `stage_b_identity_ch09.py`. The editor's 4e count says Rule 09.3's "Never scale a master down..." was in; it was not, so it is applied now too. Rule 09.4's kicker clause takes the editor's round 3 wording, "which may carry only a topic or atlas symbol (Rule 01.21)", so it matches Rule 01.21 as rewritten for BE-S7 | Done |
| ED 4c, 4e | The intro sentence now names "the monogram as a small signature" (and, with CA-S11, "a pattern drawn from the hinge"); my writer replaces the old sentence in place. Rule 12.1's why and failure caption say "connection". Rule 12.4's two rows (texture "to a cover, an opener or the background of a social card"; "our design judgment"). The watermark opener's line is Track's job line, "Follow the decision and keep its record within reach.", in the plate and its alt. 4c had no rows for Rules 12.1 to 12.4 | Done |
| PP-M2, D2-962 | Rule 09.1 names the row's places: "The 48 px row runs near the top of a page that introduces the four pillars or gathers one pillar's work, and the 24 px row, the compact row, runs in the header of a single piece that serves one pillar. A social card and a kicker carry no row." A "Places" row joins its specifications. The social card's "Left out" line says it carries no pillar row and no topic or atlas symbol, and why | Done; board B shows the sentence |
| PP-S1 | "Pixel fit" is defined in chapter 09's intro ("a copy redrawn on whole pixels with a 1 px line, so it stays sharp on a screen that gives each CSS pixel one device pixel"). Rule 04.6 and Rule 03.4's end mark line now say "pixel fit" in place of "a master drawn on whole pixels", "end mark master" and "pixel master". Rule 04.6's why gains: "The pillar icons keep their fits on every screen under 2x instead (Rule 09.3), because a pillar master's thin line fills in there, while B's 16 px master keeps its shape on every screen." Rule 09.3's why gains: "The end mark switches at 1x instead (Rule 04.6), because its pixel fit softens or steps unevenly between 1x and 2x, while B's smooth drawing keeps its shape on every screen." | Done |
| PP-S2 | Rule 09.3: "An exported image or a printed page has no stylesheet to switch them, so pick the 24 px file yourself: the fit in an image exported at 1x, and the master in an image exported at 2x or more and in print." A spec row says the same, and that 16 px takes the fit | Done |
| CD-S1, CA-S6 | In the stacked 48 px column each arrow now stands centered under its icon, in the 20 px gap before the next row, so the three arrows share one x. Same in Rule 09.1 and 09.2's sheets under 48em, in `s-09-phone`, and in chapter 01's `s-01-pillars` through my chapter 01 step | Done |
| CD-S10, CA-S10 | B moved: its top 20 px under the page's top, and the page's right edge cuts it at 50 of its 93.29 units, through the loop, the crossing stroke and the lower counter, left of the arm. No piece of B stands alone at the edge, and no curve grazes an edge (the old position also flattened the bowl's foot by 4 px at the bottom). Both pages are now 360 px tall. Rule 12.2 gains a "Crop" spec row and one builders sentence | Done |
| CD-S11 | The Illustrative label sits inside the plate under the band in `s-12-watermark-failure` and `s-12-pattern-failure`, so the shell no longer puts it in their captions | Done |
| CA-S5 | `s-09-phone`, `s-09-1-failure`, `s-09-3-failure` and `s-09-4-failure` are 360 px wide with a 16 px inner margin, as chapter 11's plates are; the report card in `s-09-4-failure` is a phone's 328 px column. All four fit at 390 and 360 px with no sideways scroll | Done |
| CA-S11 | Rule 12.4 keeps one pattern, the hinge arcs. The hinge rules leave the rule, the index and the plates, and the rule's "Never" row names evenly ruled lines, "which read as a form to fill in". Each plate is one 360 px cover, with the Illustrative label at the cover's head, so no third of the frame stands empty and a phone shows it whole. Design judgment, logged below | Done |
| CA-S13 | `s-03-l6` needs nothing from me: the engineer's shell script adds a breakout to any chapter plate whose fixed stage does not fit its column, from 80em | Done by the engineer; looked at |
| CA-S14 | `s-08-1-correct` sets its four masters in one row and the 48 px master on Charcoal and Prussian in a second, the two groups its caption names. The two dark tiles now stand the same height; the Charcoal one stood 6 px taller | Done |
| CA-S18, D2-973 | The social card's kicker moves from the H4 style at 24 px to the H3 style at 32 px, its label "Explainer" in Charcoal and its topic in Deep Stone, as Rule 01.21 sets a kicker's two parts. At 358 px wide it stands 9.5 px and reads on a 2x phone screen, where 24 px gave 7.2 px. 32 px is the largest step the type scale gives a 1200 px board below the section style (D2-254). The spec's "Kicker" row says so. The engineer recaptures the card | Done |
| Editor's request | CL-057 in Rule 01.21's kicker carries `data-icon-family="atlas"`, as chapter 10 files it (Variable EC3), through `stage_b_identity_ch01.py` | Done |

One more fix the looks led to: `s-09-4-failure`'s kicker set its topic in lowercase regular type, a second fault the plate did not name. It now follows Rule 01.21's type, capitals with the topic in the secondary ink, so the pillar icon is the plate's only fault.

## Second pass (D2-963, DR-191)

The editor's read (section 8 of `20261110_Stage-B-Round-3-Editor-Fix-Notes.md`) gave me six rows, rows 1 to 5 and 14. I applied each in its generator, word for word:

| Row | Where | Now reads |
|---|---|---|
| 1 | Rule 04.6, why (`stage_a_identity_chapters.py`) | "while B's 16 px master keeps its shape on every screen above 1x." |
| 2 | Rule 09.3, why (`stage_b_identity_ch09.py`) | "while B's smooth drawing keeps its shape on every screen above 1x." |
| 3 | Rule 04.5, why (`stage_a_identity_chapters.py`) | "a connection graded plausible as a dashed one" |
| 4 | Rule 04.5, failure caption (same) | "In the atlas's key a dashed line marks a connection graded plausible," |
| 5 | `s-04-5-failure` alt (`stage_a_identity_s04.py`) | "a dashed line marks a connection graded plausible," |
| 14 | Rule 12.4, basis (`stage_b_identity_ch12.py`) | "Our measurements, October and November 2026, and design judgment, which sets the 12 percent ceiling" |

"Plausible link" now appears 0 times in chapter 04 and in `manifest-identity.json`.

Rerun in order: `promotion_identity.py specimens`, then `stage_b_identity_ch01.py` (unchanged, since chapter 01's drawings did not move). `guide_build.py --strict`: exit 0, 0 warnings. `guide_check.js` at four widths: 4 failures, one per width, all in `s-11-12-correct` (four U+2011 hyphens in the live filter's text, the engineer's new D2-975 check), which is the chapter 11 hand's plate. None is in a plate of mine, and none of my files holds a U+2011.

## Routine calls

- D2-xxx | Chapter 09's four phone-size plates are 360 px wide with a 16 px inner margin, and `s-09-4-failure`'s card is 328 px | CA-S5; chapter 11's 360 px plates fit 390 and 360 px screens, and 16 px is the shell's own phone gutter
- D2-xxx | In the stacked 48 px column each downward arrow stands centered under its icon, in a 20 px gap between rows, in chapter 09 and in chapter 01's row | CD-S1, CA-S6; the four masters' ink is centered at 64 of 128 units across, so one x serves all four, and the row looks the same in both chapters
- D2-xxx | Rule 09.1 places the 48 px row near the top of a page that introduces the four pillars or gathers one pillar's work, the 24 px compact row in the header of a single piece that serves one pillar, and no row on a social card or in a kicker | D2-962, PP-M2; chapter 01's captions put both rows "on a page that serves Track", and Rule 09.4 keeps the 128 px icon for section openers
- D2-xxx | The proofs' social card carries no pillar row and no topic or atlas symbol, and its "Left out" line says why | D2-962; a phone's feed shows the 1200 px card at about 30 percent, so a 48 px icon would draw at 14 px, under every icon's floor
- D2-xxx | The social card's kicker takes the H3 style at 32 px, its label in Charcoal and its topic in Deep Stone | D2-973; the kicker tells a reader in the feed whether the piece reports or argues, which the platform's own lines may not; 32 px is the largest size D2-254 gives a 1200 px board short of a second headline
- D2-xxx | "Pixel fit" names every whole-pixel drawing: defined in chapter 09's intro and used in Rules 03.4 and 04.6 | PP-S1, H02; the files keep their names
- D2-xxx | Rules 04.6 and 09.3 each give one clause on why their switch points differ | PP-S1, D2-808
- D2-xxx | Rule 09.3 picks the 24 px file for exported images and print: the fit at 1x, the master at 2x or more and in print; at 16 px, the fit | PP-S2; nothing switches a PNG or a printed page, and the 16 px master never draws (D2-634)
- D2-xxx | Rule 09.4's kicker clause reads "which may carry only a topic or atlas symbol (Rule 01.21)" | ED 4b's row, matched to Rule 01.21's new wording at the editor's request
- D2-xxx | The watermark's top sits 20 px under the page's top and the page's right edge cuts B at 50 of its 93.29 units; both pages are 360 px tall | CD-S10, CA-S10; cutting left of the arm leaves every visible part joined to the letter, and Rule 04.8 already asks a crop for no fragment at the edge. I also tried keeping the arm whole, with B moved down and in, which brought B within 18 px of the text column
- D2-xxx | Rule 12.2 gains a "Crop" spec row and one builders sentence | A builder who copies the plate needs the rule that fixed it
- D2-xxx | Rule 12.4 keeps one pattern, the hinge arcs, and drops the hinge rules from its rule, the device index and its plates | CA-S11, design judgment: sixteen even lines read as lines to write on, the arcs carry the hinge diagram's geometry, the round 2 brief allowed "at most two", and the creative director's risk note doubted the patterns. Rule 12.4's title now names the arcs
- D2-xxx | Rule 12.4's plates are each one 360 px cover, the Illustrative label at the cover's head, the failure's band the plate's width | CA-S11, CD-S11; no empty part of the frame, and both plates fit a phone. The arcs stand 41.5 px from the nearest line of text, measured in the built page
- D2-xxx | The watermark failure carries the Illustrative label inside the plate under the band | CD-S11, as Rules 09.4 and 12.1's failures do
- D2-xxx | Chapter 12's device index names Rule 12.3's device "L8, the monogram" and Rule 12.4's "Hinge arcs" | ED 4e; chapter 03 keeps "compact signature" for our fourth edition's retired typed "O & A"
- D2-xxx | `s-08-1-correct` sets the four masters in one row and the two dark surfaces in a second, and the two dark tiles share one height | CA-S14; the caption already names those two groups, where a grid of three and three would split the ladder of sizes
- D2-xxx | `s-09-4-failure`'s kicker follows Rule 01.21's type | The plate fails Rule 09.4 alone, as CD-S3 asks of chapter 10's failure
- D2-xxx | CL-057 in Rule 01.21's kicker carries `data-icon-family="atlas"` | Chapter 10 files it as Variable EC3 (the editor's request)
- D2-xxx | The watermark failure's B sits at the same height as the correct plate's, 20 px under the page's top | Its foot grazed the page's bottom edge, a second fault the plate did not name
- D2-xxx | Chapter 09's row tags keep a size and its unit on one line | At 360 px "24 px" broke after "24"

## Questions for Dustin

None. Board B shows Rule 09.1's new sentence (D2-962) and Rule 12.4 with one pattern.

## For the other owners

- **Editor (D2-963).** Changed strings for your read, all in my generators: chapter 09's intro (the pixel fit sentence), Rule 09.1's places sentence, its "Under 48em" and "Places" spec rows and its builders sentence; Rule 09.3's export sentence, its why (the end mark clause) and its "Exported image and print" spec row; the phone extra's caption; the alts of `s-09-phone` and `s-09-4-failure`'s notes. Rule 03.4's end mark line; Rule 04.6's rule, why (the pillar clause), "Size", "At 17 px text" and "At 15 px text" specs and builders. Chapter 12's intro sentence, Rule 12.2's caption, "Crop" spec and builders sentence, Rule 12.4 whole (title, rule, why, captions, specs, builders), the device index's two rows, and the alts of `s-12-watermark-correct`, `s-12-pattern-correct` and `s-12-pattern-failure`. The proofs' social card: "Kicker" and "Left out" spec rows and the alt. Rule 12.4's basis keeps your 4e wording, "Design judgment and our measurements, October and November 2026; the 12 percent ceiling is our design judgment", which now says "design judgment" twice; you may want one.
- **Engineer.** D2-973 is in: recapture the social card for the reader check's step 4. CA-S13 needs nothing from my side.
- **Systems designer.** My writer replaced only my own intro sentence and Rules 12.1 to 12.4; your Rules 12.5 to 12.9, extras and intro sentence stand as the file held them.

## Tested

- **Strict build.** `guide_build.py --strict` to my scratch folder: exit 0, 12 chapters, 132 rules, 305 specimens, 0 warnings, on each of four builds (v1 to v4).
- **Guide check.** `guide_check.js` at 1440, 1024, 390 and 360 px on the last build (v4, with every other owner's work as it stood on disk then): PASS, 0 failures, 1,100 same-page links. An earlier run (v2) failed 4 times, once per width, all in `s-01-pieces` (step marks without their state in words, A-5), the chapter 11 hand's and editor's plate, not mine; v4 no longer shows it.
- **Phone fit (CA-S5).** In the built page, `s-09-phone`, `s-09-1-failure`, `s-09-3-failure`, `s-09-4-failure`, `s-12-pattern-correct` and `s-12-pattern-failure` each scroll 0 px sideways at 390 and 360 px, with no "Wider than this column" hint; before, the four chapter 09 plates scrolled 42 to 48 px at 390.
- **Looks.** Every plate I changed, captured from the built page at 1440, 390 and 360 px, at 1x and 2x (15 plates, 90 captures), and looked at: the chapter 09 plates and `s-01-pillars` at all three widths, the 2x phone column, the pattern and watermark plates, `s-08-1-correct` at 1x and 2x, the social card and the device index at 1440. Looks led to three more fixes: the watermark failure's B grazed the page's foot, the 24 px tag in `s-09-2-correct` left "px" alone on a line at 360 px, and `s-08-1-correct`'s Charcoal tile stood 6 px taller than the Prussian one.
- **Arrows.** In the stacked column the three arrows share one x, centered under the icons, at 1x and 2x, in chapter 09 and chapter 01.
- **Watermark crop.** Ten positions rendered on both pages and compared before the one kept: the old one, cuts at 64.3, 56, 52 and 50 units, and five that keep the arm whole with B moved down and in. At the kept position no piece of B stands alone at an edge on either page, and no curve grazes one.
- **Pattern clearance.** In the built page the outermost arc (radius 208 px) stands 41.5 px from the nearest line of text, against the rule's 24 px.
- **Social card kicker.** The card rendered at 1200 px and reduced with Lanczos to 358 px, at 1x and at 2x (716 px), with the kicker at 24 px and at 32 px, and looked at: at 358 px the 24 px kicker stands 7.2 px and barely reads; at 32 px it stands 9.5 px and reads, most clearly at 2x. The lockmark is unchanged, so the feed test's figures stand.
- **L6 (CA-S13).** With the engineer's shell change, `s-03-l6` shows whole at 1440 px: its stage spans 143 to 1075 px with no page scroll.
- **Words.** My four chapter files and every alt in `manifest-identity.json` scanned by script for em and en dashes and the listed fillers and corporate verbs: none.
- **Reruns.** The identity build run twice gives the same bytes; `stage_b_identity_ch01.py` run twice changes nothing the second time. The systems designer's `check_chapter` passes on the merged chapter 12 file, and its Rules 12.5 to 12.9 match what the file held before my writes.

## Not tested

- Real phones, Firefox and Safari; 2x was Chromium's device scale factor.
- A real feed upload of the social card and the platforms' own reduction; I reduced it with Lanczos myself.
- The watermark and the arcs in print, and on White, Prussian or Charcoal for the arcs.
- Screen readers; I changed no names or roles, only alts and words.
- The editor's read of my changed strings, and the creative director's look.
- The full rebuild in the main session's order with every owner's final files.

## Change log

Modified (generators):
- `work/build/scripts/phase-2/stage_b_identity_ch09.py`
- `work/build/scripts/phase-2/stage_b_identity_ch12.py`
- `work/build/scripts/phase-2/stage_b_identity_ch01.py`
- `work/build/scripts/phase-2/stage_a_identity_chapters.py` (Rules 03.4 and 04.6)
- `work/build/scripts/phase-2/stage_a_identity_s08.py` (`s-08-1-correct`)
- `work/build/scripts/phase-2/stage_a_identity_proofs.py` (the social card)

Modified (written by those generators):
- `work/build/guide/chapters/03-identity.json`, `04-ampersand.json`, `09-pillar-icons.json`, `12-graphic-devices.json` (Rules 12.1 to 12.4 and my intro sentence only)
- `work/build/guide/specimens/manifest-identity.json`
- `work/build/guide/specimens/`: `s-08-1-correct.html`, `s-09-1-correct.html`, `s-09-1-failure.html`, `s-09-2-correct.html`, `s-09-2-failure.html`, `s-09-3-failure.html`, `s-09-4-failure.html`, `s-09-phone.html`, `s-12-index.html`, `s-12-pattern-correct.html`, `s-12-pattern-failure.html`, `s-12-watermark-correct.html`, `s-12-watermark-failure.html`, `s-proofs-social.html`
- `work/build/guide/specimens/s-01-pillars.html` and `s-01-21-correct.html` (drawings only, through my chapter 01 step)

Created:
- `work/handoffs/phase-2/20261110_Stage-B-Round-3-Identity-Fix-Notes.md` (this file)

Scratch builds, captures and test scripts: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/round-3/fix/identity/`.
