# Editor review of Phase 1

oa-editor, October 21, 2026. Suggested edits only; no board or note was changed. Scripts named below sit in `work/build/scripts/phase-1/`. Fixes are ranked, most important first.

**Script check** (`editor_pattern_check.py`): 0 em dashes, 0 en dashes, 0 corporate verbs, 1 filler. British spellings break D1-12 102 times, 87 of them in the symbol files. Every quoted locked line is exact; the deviations are paraphrases and unquoted uses.

## 1. Strategy and Direction Board, Brand Strategy

| # | Location | Original | Revision | Reason | Source |
|---|---|---|---|---|---|
| 1 | Notes, NP-01 | "Prussian surfaces carry Newsprint marks." | "...carry one-color marks in the color approved at identity item 10." | Identity recommends White (C2) | `20261021_Brand-Strategy.md` l.163 |
| 2 | Positioning | "...that explains how a decision is made and gives a practical way to take part." | "...set of tools. Its reader promise: "We explain how a decision is made and give you a practical way to take part."" | A near-copy reads as a misquote | `strategy-board.template.html` l.143; notes l.19 |
| 3 | Notes §1 | "follows the atlas line code and is drawn dotted" | "follows the systems board's line code" | C5 | notes l.60; R9 sketch in `cd_build_strategy_board.py` |
| 4 | Notes §4 | "the Layout and Signal Grid chapter" | "08 The Signal Grid" | The map splits it; my voice-line file's "chapter 07" too | notes l.129 |
| 5 | Decisions panel | "12 Wordmark and ampersand / On the identity board" | Questions with real options (list below) | Gate 1 format | template l.503; notes |
| 6 | h2s | "Six readers, one record"; "Take the heavy capitals and the serif ampersand, and leave the domes" | "Six audiences and where each one starts"; "What to take from your references" | Slogan; contrasting pair (also notes decision 7) | template l.222, l.422 |

## 2. Identity Refinement Board, Identity Refinement Notes

| # | Location | Original | Revision | Reason | Source |
|---|---|---|---|---|---|
| 1 | Item 7 | "two dotted arcs loop around it" | Redraw as solid hairline arcs | Dotted is V7's hypothesis texture (C1) | `p1_marks.py` l.111; `p1_board.py` l.324 |
| 2 | Item 3 | "and the option A 16 px ampersand" | "and the 16 px master of the approved ampersand" | B is recommended (C7) | `p1_board.py`; `p1_wordmark.py` |
| 3 | Items 8 and 9 | "V5 master from 32 px" against "From 48 px up the V5 master stays" | One threshold, and name what serves 25 to 47 px | Internal contradiction | `p1_board.py` l.342, l.369 |
| 4 | Item 5 table | "With the other serifs 0.47 to 0.60" | "0.48 to 0.61" | The JSON gives 0.484 to 0.613 | `p1_board.py` l.286 |
| 5 | Decision 6 | "Your call. I lean to the condensed ... It is not finished" | "Condensed 7.5 to 1 as the Phase 2 direction, after a drawing pass and a narrow 16 px ampersand." | One recommendation; hedge | `p1_board.py` |

## 3. Systems Marks Board, Systems Marks Notes

| # | Location | Original | Revision | Reason | Source |
|---|---|---|---|---|---|
| 1 | Mark 3 | "They become Std-01 to Std-10" | Hold for Dustin's ruling | The map uses home rule IDs (C4) | `build_systems_marks_board.py`; `systems_marks_data.py` |
| 2 | Grade words | "well-supported neighbours"; aria "well-supported texture"; "V7 loop grade: well-supported for..." | "well supported neighbors"; V7 free text in quotation marks | One display form, "Well supported" | `build_systems_marks_board.py` l.175; `svg_marks.py` |
| 3 | Spelling | colour, neighbours, favour, totalled | color, neighbors, favor, totaled | D1-12 | same script; notes l.26, l.46 |
| 4 | Mark 7 primer | "On Charcoal and Prussian the ampersand is drawn in Newsprint" | Red on Charcoal (4.49:1) | Only Prussian is open | same script |

## 4. Navigation and Template Wireframes, Guide Architecture Map

| # | Location | Original | Revision | Reason | Source |
|---|---|---|---|---|---|
| 1 | Chapter 08 instruction | "code content with it only where a key..." | "code content with the Signal Grid only where a key..." | The lockmark does not code content | map §2; `build_navigation_wireframe.py` l.38 |
| 2 | Token names in 05 Color | `--oa-color-accent-red`, `--oa-color-state-focus`, `--oa-color-pillar-red` | `--oa-color-palette-pillar-red`, `--oa-color-focus-ring-on-newsprint` | Not in the token draft | `fragments/05-color.html`; board l.326 |
| 3 | Map §4 | "V5's ten standards ... map to the home rule" | Hold for Dustin's ruling | C4 | map §4 and V5 15 rows |
| 4 | Check 7.4 | "board-base.css sets ... tags at 12 px ... needs the same change" | "board-base.css now sets 13 px (D1-07)." | Stale | board HTML l.13, l.446 |
| 5 | Closing | "Put the promise to work." | "Colophon, edition notes and the way back to the start." | Slogan; differs from the map | `build_navigation_wireframe.py` l.249 |
| 6 | V5 cover row | "the rules that shape our lives" | Retire, or quote the mission exactly | Echoes the locked mission | map §6 |

## 5. Token Architecture

| # | Location | Original | Revision | Reason |
|---|---|---|---|---|
| 1 | §8 | "sits in the guide's foundations part" | "is chapter 26, in Production" | The map (C9) |
| 2 | §9 | No options | Add options, such as T-4 "18% or 15%" | Gate 1 format |

## 6. Research Summary

| # | Location | Original | Revision | Reason |
|---|---|---|---|---|
| 1 | Item 3 | "Brief section 13 rules the pairing out." | "...rules it out for diverging scales, and V5 says "Never red against blue."" | Accuracy |

## 7. Symbol Family Board, Symbol Family Notes

| # | Location | Original | Revision | Reason | Source |
|---|---|---|---|---|---|
| 1 | §7 patterns | "Dotted arcs, 2.5 percent ink" | Drop, or redraw solid | A grade texture on a brand mark (C1) | `symbols_board_build.py` l.479 |
| 2 | §2 figure | "Schematic of the V5 hinge" | "Schematic of the proposed hinge diagram (identity item 7)" | V5's hinge has no ring | l.693 |
| 3 | §7 Tile row | "app and favicon tiles" | "app tiles" | Identity gives favicons to the ampersand (C6) | l.776 |
| 4 | §2 | "The node won for three reasons a reader can feel." | Delete; keep the reasons | Four reasons follow; performed tone | l.696 |
| 5 | Intro | "Every mark carries one hinge node, so the family belongs to the ampersand." | "Every mark carries one node, the point where its two parts meet." | Slogan; "hinge node" undefined | intro |
| 6 | §3 story list | One label for the figure | "Illustrative" beside each headline | "Three groups on opposite sides agreed..." reads as news | l.298 |
| 7 | Spelling | colour, centre, labelled, grey, mitred | color, center, labeled, gray, mitered | D1-12 | script; notes |

**Minor:** The strategy board's pillar-split aria-label leaves "Clarity is our duty." unquoted. Identity items 4 and 8 use corrective negation ("not its color"). Map §4 should say "connections" and "variable X1". Research item 2's house format becomes decision 13. In the strategy narrative, "You both get the same record and the same way in." is a parallel run. Identity: "centring" to "centering", drop "just", and label item 2 "(design judgment)". Systems Mark 4 "Pips for scanning, words for reading" is a contrasting pair. The map's Rule 05.2 title should match the board's. In the wireframe, "3 px out" becomes 2 px and "grey" becomes "gray". On the symbol board, "Act · Take part" becomes "Act · How to take part". The symbol notes' 3.48:1 belongs to Direction B; A measures 3.58:1.

## Cross-board contradictions

- **C1 Hinge arcs.** Identity item 7 draws dotted arcs. Strategy and Systems ask for solid ones. The symbol board ships dotted arcs as a pattern.
- **C2 Ampersand on Prussian.** Identity recommends White (D). Strategy NP-01, the systems primer and the token roles use Newsprint.
- **C3 Red's one job.** Strategy's Act pattern puts red on the ask only, and NP-04 adds the headline's data point. Systems uses red in data figures only where a reform acts. Wireframe Rule 05.3 lists four jobs and exempts the ampersand and lever. The symbol board's Act post spends its red on the Act handle. Nobody says whether the handle counts as identity.
- **C4 Standards IDs.** Systems proposes Std-01 to Std-10. The map gives each standard its home rule ID, such as Rule 05.1.
- **C5 Loop R9.** Strategy draws it dotted. Systems draws conceptual loops, R9 named, as a hollow line.
- **C6 Favicon.** Identity uses the ampersand's 16 px master. The symbol board uses pillar tiles.
- **C7 Small wordmark.** The 16 px master carries ampersand A, while B is recommended.
- **C8 Candidate lines.** Strategy: 01 Purpose and 08. Map: 02 Voice.
- **C9 Token chapter.** Token Architecture says Foundations. The map says 26, Production.
- **C10 Terms.** The drawing is the "hinge loop" (strategy), "hinge mark" (identity) and "hinge diagram" (V5, map, systems); I propose "hinge diagram". "Signal Grid lever" and "Signal Grid lockmark" blur the strategy's defined terms. "Hinge node" and "S2 tile" are undefined. Label tracking is 0.06 em in the tokens and 0.04 em on the chips.
- **C11 Navigation row.** Strategy uses four filled circles; the symbol board uses the new pillar marks.

## Gate 1 decisions, deduplicated

| # | Question | Options | Recommendation |
|---|---|---|---|
| 1 | Is the hinge the system's organizing idea? | As written; edited | Strategy: as written |
| 2 | How is the hinge diagram drawn? | V5 arc; two-way dashed; item 7 dotted; one-way solid | Strategy, Systems: solid. Identity: item 7 |
| 3 | One masterbrand? | Masterbrand; separate brands | Strategy: masterbrand |
| 4 | Rename "Dispatch from the Front" to "Dispatch"? | Rename; keep | Strategy: rename |
| 5 | What role for "From spectators to stewards."? | Founding line; events; lockups | Strategy: founding line, shown with V4.2's retirement record (map) |
| 6 | What role for "Democracy has a structure."? | Lockmark explanation; brand line; none | Strategy: lockmark explanation |
| 7 | Which voice line? | V5; revision A, B or C | Editor, Strategy: B |
| 8 | How do Act pieces work, under which label? | Fairness kit or none; "Our position", "Opinion", "Position: Support" | Strategy: kit, "Our position" |
| 9 | Adopt NP-01 to NP-20? | Adopt; edit | Strategy: adopt |
| 10 | Seals? | V5 rule plus wordless badge; worded seals | Strategy: V5 plus badge |
| 11 | May patterns sit behind content? | Low density, 12 percent ink; "never wallpaper" | Strategy, Symbol: allow with limits |
| 12 | Photography default? | Black and white; color | Strategy: black and white |
| 13 | Which house format for "you & me" pieces? | Quiz; for and against; before and after | None given |
| 14 | Re-export six clipped symbols? | Accept; decline | Identity: accept |
| 15 | How are hinge gaps set? | 2a nearest ink; 2b equal area; V5 | Identity: 2b |
| 16 | Separate display, 24 and 16 px wordmark masters? | All; without larger ampersand; none | Identity: all |
| 17 | Which ampersand? | A tune; B drawn; V5 | Identity, Strategy: B, A fallback |
| 18 | Condense the wordmark? | 7.5 to 1; current | Strategy: condensed. Identity: leans condensed |
| 19 | Lockmark small masters? | Accept; decline | Identity: accept |
| 20 | One minimum-size rule? | Accept; V5 | Identity: accept |
| 21 | How does the ampersand appear on Prussian? | A to D | Identity: D, White. Others: Newsprint |
| 22 | Which symbol direction and skeletons? | A or B; approve or change | Symbol: A; raise Track's stair |
| 23 | What joins the pillar marks? | Node; crossing; ring; bar | Symbol: node |
| 24 | Red in pillar marks, and does it count as the layout's red? | Act handle only; all four | Symbol: Act only. Unresolved (C3) |
| 25 | Line marks at 16 px? | Allow; from 24 px | Symbol: from 24 px |
| 26 | Redraw all twenty topics? | Redraw; keep V5 | Symbol: redraw |
| 27 | Approve the treatments map? | Approve; amend | Symbol: approve |
| 28 | Evidence line code? | V7 plus square and hollow line; V5; ramp | Systems: V7 with square and hollow line |
| 29 | Grade words? | V7; Concepts V2; hybrid | Systems: hybrid |
| 30 | ID chips and Standards prefix? | Bare; colon; two-part; Std-, G-, Rule NN.n | Systems: two-part, Std-. Map: Rule NN.n |
| 31 | Effect mark? | Words; pips; width | Systems: pips with words |
| 32 | Event mark and period rule? | Adopt; revise | Systems: adopt |
| 33 | Authority and delay marks? | Arrowhead, teal, diamond; letters, ticks | Systems: diamond; ticks |
| 34 | Atlas bases? | Per concept | Systems: 03, 09, 11, revised 10, 07 with 04 |
| 35 | Send the V7.1 issue list? | Send; hold | Systems: send |
| 36 | Six parts, 28 chapters (A1 to A6)? | Each change; brief's map | Map: each change |
| 37 | Numbering and headings (A7, A8)? | 01 to 28, word anchors; per-part | Map: 01 to 28 |
| 38 | Navigation and interaction (N1 to N3, T1, I1 to I3)? | As proposed; alternatives | Wireframes: as proposed |
| 39 | Token format and derived colors (T-1 to T-5, T-10)? | As proposed; Deep Stone 18% or 15% | Token: as proposed, 18% |
| 40 | Red, states, type, opacity, motion (T-6 to T-9)? | As proposed; amend | Token: as proposed |

## Tested and not tested

Tested: board and wireframe text by script; all Markdown files read; locked lines; mock dates; token names against the schema draft; similarity and ring figures against their JSON.

Not tested: rendered pages, label placement on screen, screen readers, text inside raster images.

**Created:** this file, `editor_board_text.py` and `editor_pattern_check.py`. **Modified:** none.
