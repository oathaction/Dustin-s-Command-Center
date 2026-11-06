# Stage A identity notes: chapters 03, 04 and 08, and the Gate 2 proofs

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261106_Stage-A-Brief.md`. I wrote no ledger, master, `source/` file or other maker's file.

## What I built

| Chapter | Rules | Extras | Specimens |
|---|---|---|---|
| 03 Identity | 8 (03.1 to 03.8) | the eight lockups, the minimum-size table, three more failures | 19 |
| 04 The Ampersand and the hinge | 8 (04.1 to 04.8) | none | 17, with one corrective (04.3) |
| 08 The Signal Grid | 9 (08.1 to 08.9) | codes and combinations, nine stages and five shapes, the composer | 21 |
| Proofs for Gate 2 | none | six groups in `proofs.json` | 11, plus a two-page US Letter PDF |

Every rule has a correct application and a failure case at true size. Each failure is one a producer makes: typing the name in Inter Tight, squeezing the wordmark into a tile, dropping the Newsprint file on a Charcoal slide, joining a partner with a second ampersand, placing Edition 05's Lora file, a red divider above a red button, dashed hinge arcs, a badge turned into a seal, lockmarks as bullets, a grid with no key, a diagonal route.

**Masters by reference.** Each specimen holds `<img data-inline src="work/build/assets/identity/...">`, which the shell inlines (Guide Shell Notes section 5), so no fragment carries a copy of a drawing. The re-exported taglines are inlined by my script with their ids prefixed, because one specimen can hold two copies. No master file was written.

**Chapter 08 rebuilt.** V5's rules A to F become Rules 08.4 to 08.8, with 08.1 to 08.3 for the lockmark and the key and 08.9 for states. One grid codes one thing, in this order: tracker progress, a series route, a pillar corner. Content type leaves the grid for words. Stages are told by shape: a filled disc for done, a ring for under way, a gap for a stage that never happened, a small Stone node for not reached, and one red disc for the stage where a reader can take part now. Active and Ready are now a ring and a filled disc. Loading is still: the links alone with the words "Loading tracker". The composer builds only valid combinations and reads the grid back in a status line.

**Proofs.** Masthead (site at 1440 px with the phone bar, and a 600 px email), avatar (circle and square on Charcoal), a 1200 by 630 social card and a US Letter letterhead, each at today's width and condensed, with ampersand B. Every invented headline, address, recipient and letter carries the Illustrative label; the social card has no web address (DR-55). The PDF is `work/boards/phase-2/stage-a/proofs/20261106_Letterhead-Proof.pdf`, and the letterhead plate carries a download link.

## Routine calls, as proposed decision lines

- D2-xxx | Identity masters enter specimens as `<img data-inline src>` for the shell to inline; the re-exported taglines are inlined by `stage_a_identity_lib.py` with prefixed ids | The fragment names its master by path and never copies a drawing; two tagline copies in one specimen need unique ids
- D2-xxx | The hinge divider is drawn whole in the surface's ink, hairline and ampersand alike, with B's 24 px master at 24 px and 12 px on each side; Rule 04.4 says so | It matches the shell's divider and Board 5, which Dustin approved
- D2-xxx | The editorial crop of B takes the surface's ink, never red | Rule 05.3 names no job for a crop, and the divider sets the precedent
- D2-xxx | Social avatars and the app icon show B alone on the Charcoal tile; L8 serves squares where the name must show | A feed draws avatars at about 32 to 48 px, where L8 sets its capitals at 10 to 12 px; V5 already made B the default avatar (C2)
- D2-xxx | V4.2's compact signature, "O & A" typed with spaces, retires; L8 is the one monogram | The map sent it to the identity chapter for this ruling; two monograms split recognition
- D2-xxx | L7's pillar word sits in the surface's ink at a cap height of 0.6x; V5's red "Act" retires | Rule 05.3 gives a label no red; at 0.6x, CONNECT holds 13 px at the 250 px minimum in the I8 table
- D2-xxx | L4 to L7 are assembled from the approved masters on V5's layouts (L6 measured from the Gate 0 capture: 1400 by 300 units), all White on Prussian, with no web address | Their own masters are not drawn yet (I8 note); this shows them at true size meanwhile
- D2-xxx | The masthead sets L3 from 768 px and L1 from the 24 px master below it | The lockmark needs about 34 px, which a phone bar gives to the menu button
- D2-xxx | Signal Grid codes: one per grid, by precedence; progress from 40 px, routes and corners from 24 px; content type in words | Tension 4; V5's content colors fail grayscale and its Active and Ready differ at 1.14 to 1
- D2-xxx | Coded grids are drawn on whole-pixel lattices: 24 px on the 24 px lockmark master's centers, 40 px at 3.5, 19.5 and 35.5 px; 80 px is the 40 px drawing doubled | Pixel fit (D1-17) for marks that carry meaning
- D2-xxx | Coded grids use no Verdigris, so the held `verdigrisOnDark` (#59857D) can be rejected | The token file holds it "for the Signal Grid chapter"; shapes now carry state
- D2-xxx | Loading draws the links alone and Empty draws small nodes, each with its words; the token architecture's "still Stone outline lever" is not used | A ring at the lever's place would read as a stage under way
- D2-xxx | The favicon row leaves the lockmark's positions table | I8: favicons use B's 16 px master
- D2-xxx | The kicker is a 24 px grid, 12 px, a 24 px Civic Line icon in one color, 12 px, then a 13 px label and an optional ID chip | One definition on the 8 px rhythm; V5's labels sat at 10 and 11 px
- D2-xxx | Illustrative bills reuse V5's invented numbers (Q-01) on neutral topics: public meeting notice, school bus contracts, library hours, records request fees | V5's topics were election rules, which carry the editor's disclosure (D2-106)
- D2-xxx | In the proofs both widths sit at the same height, except avatars, where L8 fills the same width of the tile | Mastheads and cards are set by height; a tile is filled by width
- D2-xxx | The letterhead places the display master at 26 px tall, as a print piece would; all its text is 10 pt or larger | The 24 px master is drawn for screens; the 13 px floor holds on screen
- D2-xxx | Two typed failure cases (03.1, 03.7) carry `check_exempt: contrast` and two (04.3, 04.4) `check_exempt: red`; V5's kicker (08.8) is a PNG | A failure has to show at true size; the shell lists every exemption

## Open questions for Dustin

1. **Width and ampersand at Gate 2.** The proofs show both. *Recommendation:* today's width and B as refined (D2-30). The condensed drawing passes the craft checks, but at the same height it only runs narrower, it sits close to campaign-sign lettering, and its monogram reads as 0&A.
2. **The Signal Grid's new codes.** Content type leaves the grid, each grid codes one thing in a fixed order, and stages are told by shape. *Recommendation:* approve, since V5's codes fail grayscale and color-blind reading.
3. **The avatar.** B alone on Charcoal, or L8. *Recommendation:* B alone. At feed size L8 sets its capitals under the 14 px floor at either width, so the avatar does not depend on the width decision.
4. **The editorial crop's color.** *Recommendation:* the surface's ink, as Rule 04.8 now says. Red would spend the view's one working red on decoration.
5. **Series routes.** V5's census clips text at 50 characters, so I matched the six series names to the six routes by their order in V5; every route ends on its pillar's corner, which supports the reading. *Recommendation:* confirm the six pairs in Rule 08.6, or name any that should change.

## Tested

- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`: 8 chapter files, 99 rules, 234 specimens, no warnings.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px: pass, 0 failures, axe-core 4.10.2 with the WCAG 2.2 AA tags, no outside requests but Google Fonts, no script errors. A `--quick` run after my last change also passed.
- The composer, driven by script in the built page: each code, the stage, under way, the gap, the step (disabled until the stage is under way, with its reason shown), series, pillar and Reset; one red node at most; the status line reads each state.
- Every plate of mine captured at 1440 px and looked at; chapter 08 sampled at 390 px. A script measured each stage against its content: the only plates wider than the 1440 column are true-size pieces that must be (the 1440 masthead, L6 at 884 px in the lockup sheet, the 1200 px cards), and the shell scrolls them inside their frames.
- The letterhead PDF with `pdfinfo`: 2 pages, 612 by 792 pt.

## Not tested

- The PDF on paper, and its scale with a ruler.
- Screen readers by ear; Firefox and Safari; Windows and macOS rendering.
- Keyboard order past the check's first 60 Tab stops, so the composer's order was checked by script only.
- Readers: whether the stage shapes, routes and corners decode without the key. No person has seen them (DR-68's reader check does not include them).
- Feed sizes for avatars are a design judgment; I read no platform's specification.
- `dataviz_check.js`: the shell notes replace it for guide pages with `guide_check.js`, and it has no exemptions for labeled failures.

## What I could not finish

- L4 to L7 as masters. They are assembled from masters on V5's layouts, and their minimums come from the I8 table.
- The coded Signal Grid drawings live in `stage_a_identity_lib.py` (`sgrid`). They are not yet cut as SVG files for the asset package.
- The hinge motion's still frame waits for chapter 17, as the map moves the motion there.

## Change log

Created:
- `work/build/guide/chapters/03-identity.json`, `04-ampersand.json`, `08-signal-grid.json`, `proofs.json`
- `work/build/guide/specimens/`: 57 chapter specimens (`s-03-*`, `s-04-*`, `s-08-*`), 11 proofs (`s-proofs-*`) and `manifest-identity.json`
- `work/boards/phase-2/stage-a/proofs/20261106_Letterhead-Proof.html` and `20261106_Letterhead-Proof.pdf`
- `work/build/scripts/phase-2/`: `stage_a_identity_build.py`, `stage_a_identity_lib.py`, `stage_a_identity_s03.py`, `stage_a_identity_s04.py`, `stage_a_identity_s08.py`, `stage_a_identity_proofs.py`, `stage_a_identity_chapters.py`, `stage_a_identity_raster.js`
- `work/handoffs/phase-2/20261106_Stage-A-Identity-Notes.md` (this file)

Regenerated by running the engineer's scripts: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report, check results and captures.

Modified: none. Rebuild with `python3 work/build/scripts/phase-2/stage_a_identity_build.py --pdf`, then `python3 -I work/build/scripts/phase-2/guide_build.py`.
