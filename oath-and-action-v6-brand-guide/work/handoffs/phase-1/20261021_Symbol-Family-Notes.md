# Symbol family notes, Phase 1

Design director pass, October 21, 2026. It covers the symbol family only. A separate pass handles the wordmark and the ampersand.

**Board to open:** `work/boards/20261021_Symbol-Family-Board.html`. It needs `board-base.css` beside it and the PNGs in `work/boards/phase-1/symbols/px/`.

## What changed

Nothing in any master. Every drawing is a proposal under DC-02.

1. **One skeleton per pillar** sits on a shared 24-unit grid with a 2-unit margin. One unit is one pixel at 24 px.
   - **Explain** is a square broken open. Its top-right quarter lifts out along the diagonal.
   - **Track** is three stages on a rising stair.
   - **Connect** is one circle in two equal halves, held apart.
   - **Act** is a door swung open toward the reader.
   - The 48 and 96 px sizes scale the 24 px master. The 16 px masters are separate drawings, fitted to whole pixels.
2. **Two directions** come from the same four skeletons.
   - **A, geometric solid:** filled primitives with square corners. The node is a 4 px dot set into a 1 px clear seat.
   - **B, line with one accent:** a 2 px monoline with round ends. The node is a 6 px dot held off the line by a 1 px gap.
   - Each has filled, line and tile treatments at 16, 24, 48 and 96 px in one color on all four surfaces, with 8x pixel views, plus one composition: a 1080 by 1080 Act post and an article kicker.
3. **The shared element is the hinge node.** Every mark is two parts and the point that joins them: where Explain's quarter lifted out, the stage Track has reached, the space between Connect's halves, and Act's handle. The node always sits on the horizontal center line, so in a row one line passes through all four nodes, the grammar of the hinge diagram and the Signal Grid. The board sketches three alternatives I set aside: the ampersand's crossing (an X at 16 px, and it borrows the master ampersand), a ring around each mark (look-alike badges that drift toward ©) and a shared baseline bar (one more shape common to all four).
4. **Red.** The board adopts the creative director's red rule, quoted verbatim in decision 4. The Act handle is red only when the Act mark is the call to act, as on a social post, and it then spends the view's one working red. The ring is 1 px Charcoal on Newsprint and White (red on Newsprint is 2.96:1), the seat is cut out against Charcoal (4.49:1), and the handle is never red on Prussian or at 16 px. The hinge row and the story list now keep Act in Charcoal.
5. **Topic grammar proof** (tagged Option). I redrew Ballot, Bill, Contact an official and Campaign money in Direction A at 16, 24 and 48 px, with one node per subject. Only the split of Contact an official from Campaign money carries the Defect fix tag: Campaign money is now a coin stack, so it no longer shares the envelope's landscape box.
6. **Sanctioned treatments map** gives each treatment one job and a minimum size: filled marks from 16 px, the line companion from 24 px, tiles for avatars and series markers, isometric only for layer diagrams with flat labels, hand-drawn spot illustration from 96 px drawn by a person, patterns at 12 percent ink or less behind text, and Y2K orbits as motion only. The dotted-arc pattern is dropped, and the construction drawings now use solid guides, because Atlas V7 gives dotted and dashed lines to evidence grades. The hand-drawn texture study is labeled as script-generated.
7. **One post with the whole set** (section 11, before the decisions). The Act post rebuilt at 1080 by 1350 with the identity board's wordmark with ampersand B at today's width, again at the condensed 7.5 to 1 width, and a third time with the wordmark covered. The V2 hinge diagram (solid arcs) sits between headline and steps as a divider, so its ampersand is Charcoal. In the covered post its words are covered too. One working red: the Act handle. Headline and steps are labeled Illustrative.

## Why

- **Track and Act.** V5's Track and Act both run from bottom left to top right and correlate at 0.81 at 16 px. The stair is wide and low, the door tall and narrow. Direction A now correlates at 0.21, a score of 0.29 against V5's 0.65.
- **Phase 0 watch points** are avoided and measured (A filled, higher of 16 and 24 px): Track against a status-light row 0.22; Act against a letter D 0.55, a play triangle 0.33 and an outbound arrow 0.47; Explain against © 0.55 and a letter C 0.54; Connect against V5's chain link 0.57.
- **Contact an official and Campaign money** fall from 0.93 to 0.44 at 16 px, and from 0.86 to 0.44 at 24 px.

## Checks passed

Similarity uses the Phase 0 measure (silhouette overlap plus correlation after a 3 by 3 blur) on Chromium renders at device scale 1.

- **Pixel fit:** all 48 pillar masters at 16 and 24 px, and all 8 topic masters. Every straight edge and every tangent of a node, seat, disc and arc lands on a whole pixel. Round caps, joins and fillets are exempt.
- **Silhouette at 16 px:** every filled master in both directions passes. A filled crisp share runs 0.69 to 0.91, against V5's 0.38 to 0.54.
- **Similarity:** every pillar pair in every set scores under 0.60. Direction A's highest is 0.47. Every topic pair scores under 0.60.
- **Optical balance:** A filled ink runs 0.297 to 0.365 at 96 px.
- **Monochrome:** the node stays a separate shape in both polarities for every drawing at 16 and 24 px.
- **Contrast:** ink against surface is 9.42:1 or better on all four surfaces. The red-handle ring measures 3.58:1 (A) and 3.48:1 (B) or better against red at 24 px, and 4.49:1 at 48 px.
- **Board layout,** re-run after the review fixes: at 1440 and 390 px there is no horizontal overflow and no text under 13 px. No heading ends on a single word, all 161 numeric cells use tabular figures, and no hyphen stands in for a minus. Board and notes use American spelling (D1-12).

Totals: Direction A, 86 pass and 10 fail. Direction B, 85 pass and 11 fail.

## Checks that still fail

- **Track sits low.** The solid stair's center of mass is 17 to 18 percent of the field below center, in A filled, A line and B filled. Phase 2 should test a raised stair.
- **The Act handle at 16 px** is a declared exception in every treatment. A 6 px leaf cannot hold a 3 px dot and a ring, so the handle is 2 px.
- **Line masters at 16 px.** A Connect, B Track and B Connect fail the silhouette test, so the line companion should start at 24 px. A line Connect and B line Track are also light on ink.
- **Tiles at 16 px** hold a 10 px micro drawing that both directions share. Its nodes are 2 px with no seat, so all eight count as consistency failures. The B tile Track is also light on ink.
- **Watch for a reader test.** Ballot against Bill scores 0.58 at 16 px, down from V5's 0.71. A filled Connect against © scores 0.53; round marks score high on the silhouette half of that test.

## Rubric (Master Brief V2 section 6)

| Criterion | A | B |
|---|---|---|
| Craft | 4 | 3 |
| Clarity | 4 | 3 |
| Brand fidelity | 4 | 3 |
| Usefulness | 3 | 3 |
| Evidence honesty | 5 | 5 |
| Accessibility | 4 | 3 |

Reasons are on the board. Neither reaches 4 on usefulness until Phase 2. B's clarity and brand fidelity scores are labeled studio judgment.

## Recommendation

**Direction A.** Its leading treatment, the filled master, passes at 16 px for all four pillars; B leads with the line, which fails there for Track and Connect. A keeps red in one place and gives topic and atlas symbols a grammar that holds at small sizes. Section 12 of the board lists the seven Gate 1 decisions: direction, skeletons, shared node, red rule, line companion from 24 px, topic redraw and treatments map. For the decision log: the 24-unit grid and node rule, the studio thresholds (60 percent crisp share, 0.60 similarity) and the 12 percent pattern limit.

## Checked and not checked

**Checked:** every drawing rendered in Chromium on Linux at 16, 24, 48 and 96 px on four surfaces; the nine craft checks on 24 pillar drawings and 4 topics; similarity against V5 and the watch items; red-ring contrast on rendered pixels; pattern coverage; board layout and type at 1440 and 390 px. Inter and Inter Tight loaded from Google Fonts; Lora was requested but did not appear in the loaded list.

**Not checked:** readers (similarity comes from a model of a glance); other browsers, high-density screens, Windows or macOS rendering; print sizes; the other sixteen topics and the atlas, status and utility symbols; screen-reader output beyond the labels in the board; whether the illustrative headlines describe real procedures in every state (they are labeled).

## Change log

**Created**
- `work/boards/20261021_Symbol-Family-Board.html`
- `work/boards/phase-1/symbols/`: `20261021_Pillar-Sketches-Direction-A.svg`, `20261021_Pillar-Sketches-Direction-B.svg`, `20261021_Topic-Sketches-Direction-A.svg`, `20261021_Symbol-Family-Measurements.json`, `20261021_Symbol-Family-Board-Check.json`, `px/` (1x renders), `screens/20261021_Symbol-Family-Board-1440.jpg` and `-390.jpg`
- `work/build/scripts/phase-1/`: `symbols_geom.py`, `symbols_family.py`, `symbols_measure.py`, `symbols_board_build.py`, `symbols_board_check.js`, `symbols_render_cells.js`
- `work/handoffs/phase-1/20261021_Symbol-Family-Notes.md` (this file)

**Modified after the creative director's and editor's reviews:** the board, these notes, `symbols_board_build.py`, `symbols_family.py` and `symbols_measure.py` (spelling only in the last two), the measurement and check JSON, and the captures. No master, ledger or source file changed. The board reads the identity board's wordmark and V2 hinge files and inlines them unchanged; `board-base.css` is untouched.

**Rebuild:** `symbols_measure.py`, `symbols_board_build.py`, `symbols_board_check.js`, then the build script again to fold in the check.
