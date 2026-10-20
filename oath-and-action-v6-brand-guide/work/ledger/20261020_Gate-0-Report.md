# Gate 0 report: intake and review

Oath & Action Brand Guide, Edition 06. Phase 0, October 20, 2026. Status: stopped at Gate 0, waiting for Dustin's approval.

Open the review board: `work/boards/20261020_Gate-0-Review-Board.html`, also published as a private page at https://claude.ai/artifact/G6XczqbHo93sjZH7Wv6Qkj

## What you are asked to approve

1. The review in section 3.
2. The corrections to the Master Brief in section 6, issued as Master Brief V2 at the start of Phase 1.
3. The Phase 1 proposal in section 8.

The open questions in section 10 can be answered at any time. Each has a default the studio follows until you answer.

## 1. What was done

| Step | Who ran it | Output |
|---|---|---|
| Project set up from the kit, sources copied under their exact names and made read-only, checksums recorded | Main session | `work/ledger/20261020_Source-Manifest.md` |
| Sources split into CSS, script, sprite symbols, fonts, images, chapters and text. Atlas V7 JSON extracted. Both zips unpacked | Main session, as engineer | `work/extract/` (regenerable with `work/build/scripts/extract_sources.py`) |
| Every V5 Polished chapter rendered at 1440 and 390 px, all 12 report pages at both widths, the sprite sheet, and the companion files at 1440 px. Text census, tab order and axe-core scan | Main session, as engineer | `work/boards/screens/`, `work/handoffs/phase-0/render-report.json`, `20261020_V5-Text-Census-Summary.md` |
| Brand strategy and art direction audit, with rubric scores | Creative director | `work/handoffs/phase-0/20261020_Creative-Director-Audit.md` |
| Identity geometry and symbol audit, two diagnostic boards | Design director | `20261020_Design-Director-Audit.md`; `work/boards/phase-0/` |
| Navigation, interaction, states and accessibility audit | UX and accessibility lead | `20261020_UX-Accessibility-Audit.md`; `work/boards/screens/phase-0-ux/` |
| Data visualization audit and the Atlas V7 reconciliation | Data visualization and systems lead | `20261020_Dataviz-Systems-Audit.md`; `20261020_Atlas-Reconciliation-Table.md` |
| Voice, locked lines, terminology, labels and contradictions | Editor | `20261020_Editor-Audit.md` |
| Rights inventory of every reference, font and embedded image | Research lead | `work/research/20261020_Rights-Ledger.md`; `20261020_Research-Rights-Audit.md` |
| Synthesis, tension check, plan and this report | Main session | This file, the board, the open questions |

How the agents ran: this session's agent roster was fixed when it started, so each studio agent ran as a general-purpose subagent briefed to read and adopt its role file in `.claude/agents/`. The main session did the engineer's Phase 0 work itself, because every audit depended on it.

## 2. Verification

**Extraction counts match the sources.**

| Check | Expected | Found |
|---|---|---|
| V5 Polished sections | Cover, 16 chapters, closing | 18 |
| Sprite symbols | All `<symbol>` elements | 107 |
| Embedded fonts | All `@font-face` rules | 9 (Inter 400, 600, 700; Inter Tight 400, 600, 800; Lora Bold, Italic, Medium Italic) |
| Scripts | All `<script>` blocks | 1 |
| Downloads | Any download or copy control | 0. The Standards chapter lists 21 OA_* naming patterns in a table |
| Embedded images | All `data:image` URIs | 4 SVG diagrams, all in the Atlas System chapter |
| Atlas V7 `meta.counts` against counts computed from the JSON | 16 counts | 15 match. `sources` reads 1,099 against 1,140 source records; V7 itself reports 1,140 as `sources_total_ids`, so 1,099 counts cited sources |

**Screenshots.** 18 chapters at 1440 and 390 px (54 tiles and 35 phone composites for review), 24 report reader captures, the sprite sheet, and 38 companion tiles. A copy of the sticky navigation and the skip tab appears partway down some tall captures. That is a capture artifact, confirmed in the CSS, and no audit counted it.

**Reconciliation.** 1,447 uses of 250 Atlas V7 identifiers across V5 Polished, the Atlas Visual System and Concepts V2 all exist in V7, apart from the placeholder "L##". Of 2,644 value comparisons, 2 conflict: Concept 06 counts the rejected reform R-35 in its D03 and D04 totals. The 45-row table also lists 9 ID, 1 sign, 1 grade, 1 delay, 12 label, 7 structure and 14 encoding findings. Every Atlas V7 value the Master Brief quotes was rechecked: 71 of 76 confirmed, 4 corrected (section 6) and 1 unconfirmed.

**Rubric scores** are in section 4.

**Tested in Phase 0:** extraction counts; rendering in Chromium at 1440, 390, 360 and 320 px; axe-core with WCAG 2.2 AA tags; computed size and contrast of 2,346 text elements; keyboard order through 59 stops; focus visibility and obscuring; target sizes; reflow at 320 px; text at 200 percent (emulated); reduced motion and forced colors (emulated); report reader keyboard behavior; vector geometry and pixel fit of every symbol; similarity of all 190 topic icon pairs; every atlas identifier against V7; font name tables; image metadata and signed provenance records.

**Not tested:** real screen readers; Firefox and Safari; real text-only zoom and Windows contrast themes; touch; print; rendering outside Chromium on Linux; whether named bills, people and organizations in the demos exist; exact license wording, because this environment blocks page fetches and research rested on official-domain search results.

## 3. Review

**What to protect.** The editorial base of Newsprint, Charcoal and red punctuation passes the cover-the-wordmark test on the cover and the closing. The hinge works as a headline, a diagram and the divider before "What you can do". The measured contrast table, the voice method "We publish the mechanism / Not the mood", the Signal Grid's geometry and the idea of the nine-stage tracker are worth keeping. The atlas demonstrations hold V7's values almost perfectly, the Atlas Visual System states the honest rule "Closure is a claim.", and Concept 11 Register reproduces V7 row for row. Tab order, visible focus, target sizes, the dialog's Escape and focus return, and the icon library's empty state already pass.

**What to fix.**

1. **Evidence honesty.** The first chart titled "Closed primaries are the largest group." shows Open at 18 and Closed at 15. "Twelve years" sits over a 2014 to 2024 axis. Two dates fall on the wrong weekday. Invented figures carry real-looking source lines, and only 7 illustrative items carry a label beside them.
2. **Nonpartisan reading.** Red sits on Prussian on the same Voice page that says "Never red against blue". Every application example serves one Massachusetts open-primaries campaign, and some copy assumes a grievance ("Who wrote the rule you are angry about?").
3. **Accessibility.** 35 percent of rendered text is under 13 px. Stone text sits on Newsprint 49 times at 4.29:1, against the Type chapter's own rule. Loading pulses forever. The Signal Grid tells states apart by hue on dots 1 to 3 px wide. The report reader takes the arrow keys. The page is 524 px wide at 320 px. No chart or map has a text or table equivalent.
4. **Identity craft.** The wordmark is stock Inter Tight 800 with display tracking at every size, and the ampersand is the unmodified Lora Bold glyph, which V5 calls "redrawn". Six symbols clip their own outlines, so the tagline renders as "A countrv that answers to its peoole." and the URL as ".orq". No working small-size ampersand or lockmark exists.
5. **Symbols.** The four pillar marks use four constructions and generic metaphors (a book, a chain link, an outbound arrow). The 24 px topic masters are the 48 px drawings halved, so none sits on the pixel grid. Campaign money and Contact an official have the same silhouette at 16 px.
6. **Usefulness.** No download or copy control exists, and no font license text ships.
7. **Data and systems.** V5 dashes hypotheses where V7 dots them. Concepts 10 and 11 draw ordinal effects as quantities. No file draws a documented event. The chapter has no chart chooser and no data palettes.
8. **Structure.** Seven navigation links serve 16 chapters with misleading groups. Chapter headings are slogans, 41 mockup headings crowd the outline, and cross-references are not links.

**The biggest opportunities.**

1. A Signal Grid that a reader can decode, with one job per encoding, minimum sizes and a key beside each use.
2. One symbol family drawn from one skeleton per pillar, with sanctioned treatments derived from the same drawing.
3. A written nonpartisan rule set, plus the labeled-position pattern you approved for Act.
4. Labels at the point of use, and a claim line under every chart title that names the evidence type.
5. The hinge as a data grammar: "the rule & the result" as a signature chart with a dated rule change.
6. The atlas inside the identity: live SVG in guide tokens, typed ID chips, the Register as the evidence view, and V7's question-first entry as the model for newcomers.
7. The asset package on the page: working downloads, copy controls, dated filenames and a "For builders" note for each mark.
8. Everything at reading size: the 13 px floor, rem-based type and specimens at 1:1.

## 4. Rubric scores

Scored by the creative director against Master Brief section 6, using the automated findings. The ship threshold is 4 on every criterion. No chapter meets it.

| Chapter | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Lowest, and why |
|---|---|---|---|---|---|---|---|
| 00 Cover | 4 | 4 | 5 | 3 | 5 | 3 | Accessibility: 34 of 53 text items under 13 px |
| 01 Purpose | 4 | 4 | 4 | 3 | 4 | 3 | Usefulness: pillars never point to products |
| 02 Voice | 4 | 4 | 2 | 4 | 2 | 3 | Brand fidelity: red ampersands on Prussian |
| 03 Identity | 3 | 4 | 3 | 3 | 4 | 3 | Craft: tagline masters lose descenders |
| 04 The Ampersand | 4 | 4 | 4 | 3 | 3 | 2 | Accessibility: 25 Stone size tags fail 4.5:1 |
| 05 Color | 4 | 4 | 4 | 3 | 5 | 2 | Accessibility: 13 pairs fail the chapter's own table |
| 06 Type | 4 | 4 | 4 | 4 | 4 | 3 | Accessibility: labels specified at 10 to 12 px |
| 07 The Grid | 3 | 2 | 3 | 3 | 3 | 2 | Clarity: rules A and B look identical |
| 08 Pillar Marks | 3 | 3 | 3 | 3 | 4 | 3 | Brand fidelity: four constructions, generic silhouettes |
| 09 Topic Icons | 3 | 3 | 2 | 3 | 3 | 2 | Brand fidelity: reads as a stock set |
| 10 Photography | 2 | 3 | 3 | 3 | 2 | 2 | Craft: no photographs |
| 11 Data Visualization | 3 | 2 | 2 | 2 | 2 | 2 | Evidence honesty: a bar chart contradicts its title |
| 12 Motion | 3 | 4 | 4 | 4 | 5 | 3 | Accessibility: Loading loops without a still text state |
| 13 In Use | 3 | 3 | 3 | 3 | 1 | 1 | Evidence honesty: unlabeled people and sources; 173 items under 10 px |
| 14 Reports | 3 | 3 | 4 | 3 | 2 | 2 | Evidence honesty: invented figures carry a source line |
| 15 Standards | 4 | 4 | 4 | 3 | 4 | 3 | Usefulness: lists files nobody can download |
| 16 Atlas System | 3 | 3 | 2 | 3 | 4 | 2 | Brand fidelity: images in another house style |
| 17 Closing | 4 | 4 | 5 | 3 | 5 | 3 | Usefulness: no route to the assets |

## 5. Tensions

### The fifteen in the brief

| # | Tension | Status | Evidence |
|---|---|---|---|
| 1 | Small text | Confirmed and wider | The Type chapter specifies labels at 10 to 12 px beside its own 13 px minimum. 833 of 2,346 rendered text elements are under 13 px. Mockup text falls to 2.8 px at 390 px |
| 2 | Loading state | Confirmed | Pulses from page load with no pause (WCAG 2.2.2). Freezes at 1.27:1 under reduced motion (1.4.11). No text of its own |
| 3 | Tints and utility glyphs | Confirmed | "There are no tints." Six utility glyphs; the menu glyph has no solid pixel at 16 px. Concepts V2 already uses more than 20 off-palette values |
| 4 | Signal Grid meanings | Confirmed and wider | Six meanings, not five: report page 08 adds a count of steps. Nodes are 1 to 1.5 px at sanctioned sizes. The four content types look alike in grayscale. Active and Ready differ by hue alone (1.14:1) |
| 5 | "The chart proves the sentence." | Confirmed, and its first demonstration fails it | Title against bars (Open 18, Closed 15); "twelve years" over ten |
| 6 | Illustrative status | Confirmed | 7 adjacent labels; 4 global notes. Testimonials are presented as quotes "from readers". Real publishers are credited for invented data |
| 7 | Colliding IDs | Corrected | V5's Standards chapter uses R for two lists: principles R1 to R10 and a checklist that runs R1 to R9 and skips R4. Concepts V2 uses bare chips that mix loops and variables |
| 8 | Grade vocabulary | Confirmed | As stated in the brief |
| 9 | Palette contrast | Confirmed on rendered pages | axe flags 96 nodes. The red ampersand at 16 px has a median of 2.47:1 on Newsprint, and no red pixel reaches 3:1 there at any size |
| 10 | Download names | Corrected | No download or copy control exists. The Standards table lists 21 OA_* patterns (9 fixed names, 12 templated) |
| 11 | Lost chapters | Confirmed | V4.2's in-place "SAMPLE" labels and source slots are worth recovering |
| 12 | One tracker | Confirmed | One two-chamber bill route, no key beside it, bill numbers in a real state's format |
| 13 | Widths for ordinal effects | Confirmed and wider | Concept 10 widths at 1:2:3 and Concept 11 fills by thirds. Both drop the qualifiers on 38 of 200 effect values, and Concept 10 draws gains only |
| 14 | Red on red | Confirmed | Red marks the chart's point, the atlas intervention, the lever and negative deltas. Red does two or three jobs in several layouts |
| 15 | Hand-drawn study risks | Confirmed | Study 05 is likely AI-generated. Its minimum size should rise to 96 px |

### Added by the Phase 0 audits

| # | Tension | Evidence |
|---|---|---|
| 16 | Nonpartisan reading | Red on Prussian beside "Never red against blue"; one campaign throughout; grievance framing. Act may now take a labeled position (your decision DC-01), which needs its own visible pattern |
| 17 | Factual slips in demos | November 4, 2026 is a Wednesday and November 6 a Friday; the demos call them Tuesday and Thursday. 23 closed states in one chapter, 15 in another. H.4212 "would open" a primary the guide says is open |
| 18 | The wordmark is stock type | Inter Tight 800 outlines with uniform tracking; the ampersand is Lora Bold, unmodified. The right hinge gap measures 0.083x against a stated 0.10x |
| 19 | Clipped outlines | Six symbols cut their own outlines: the ampersand loses its loop top and tail tip; the tagline and URL lose descenders |
| 20 | Lockmark at small sizes | At 16 px a node is as wide as a link and the centre cross splits into two gray rows |
| 21 | Pillar marks | Four constructions; ink density from 0.18 to 0.32; Track and Act look alike at 16 px |
| 22 | Topic icon pixel fit and similarity | 24 px masters halved from 48 px; Campaign money and Contact an official share one silhouette at 16 px |
| 23 | Evidence line code | V5 and the Atlas Visual System dash hypotheses. V7 draws hypotheses dotted and plausible links dashed |
| 24 | Documented events | No file draws the repair log or the delivery log, and no event mark exists |
| 25 | Atlas diagrams as images | The Atlas System chapter shows four embedded images in another house style. They crop at 390 px and their text is not live |
| 26 | Navigation and outline | 7 links for 16 chapters; Systems never marked current; slogan headings; 41 mockup headings in the outline; cross-references not linked; measure of 74 to 93 characters |
| 27 | Reflow and resize | The page is 524 px wide at 320 px. Every size is in px, and 44 boxes clip text at 200 percent |
| 28 | Report reader keyboard | Arrow keys turn pages even where a keyboard user needs to pan. Focus drops to the body at page 12 |
| 29 | Text equivalents | No chart or map has a data table or step list |
| 30 | Fonts and licenses | No license text ships. Atlas V7 embeds URW Nimbus faces renamed "Atlas Display, Sans, Mono" (resolved by DC-03). Concepts V1 and V2 embed Lora subsets that keep the reserved name |
| 31 | Photography | No photographs. Ten gray panels are announced as photographs |
| 32 | Status and toggle announcements | Demo state changes are silent. "View on dark" announces "View on light, pressed" |

## 6. Corrections to the Master Brief

Proposed for Master Brief V2, applied at the start of Phase 1 if you approve.

1. Section 8, item 10: V5 has no download or copy control. The Standards chapter lists 21 OA_* naming patterns, none of them downloadable.
2. Section 8, item 7: the Standards chapter uses R for a principles list (R1 to R10) and a checklist (R1 to R9, skipping R4).
3. Section 13: the Data Visualization chapter draws four specimens (a bar chart, a line chart, a dumbbell and a tracker list).
4. Section 14: V7 draws hypotheses dotted and plausible links dashed, in its methods and its renderer. The guide reconciles to V7.
5. Section 14: 38 of V7's 200 effect values carry qualifiers beyond the seven codes, for example "Large positive · local".
6. Section 14: 13 of V7's 126 route entries carry a check date. R-01's SS and FS routes have none.
7. Section 14: V7's glossary says outside drivers are drawn as rounded pills; its renderer uses pills only for connection labels. Treat the pill as unconfirmed.
8. Sections 3 and 9: the wordmark is built from Inter Tight 800 outlines and the ampersand from the Lora Bold glyph. Refinement proposals start from that fact.
9. Section 11: V5's topic set is a 48-unit family of filled silhouettes. Only the six utility glyphs form a 24-unit, 2 px stroke family.
10. Section 16: V5 bans generated imagery. You allowed labeled generated conceptual imagery. The rule becomes: never as evidence or documentary imagery.
11. Section 1 and section 15: add the labeled-position pattern for Act (DC-01).
12. Section 2: Atlas V7's typography converges on the guide (DC-03).

## 7. Plan for Phases 1 to 5

| Phase | Work | Agents | What you see at the gate | Main risks |
|---|---|---|---|---|
| 1 Research, strategy and direction | Verified research ledger; strategy and the Act pattern; nonpartisan rules; voice line revision; symbol family in two directions; identity refinement proposals; systems marks; guide architecture; token architecture; Brief V2 | Research, creative director, design director, UX, engineer, editor | Strategy board; one identity board per element with each change to accept or decline; symbol family board; systems marks board; architecture map; token architecture | Exact wording needs page access. Redrawing the ampersand is a large identity decision |
| 2 Identity, foundations and symbols | Approved refinements applied; color, type, layout, tokens and states; the Signal Grid redesign; pillar marks; topic redraw; atlas, status, encoding and utility symbols; graphic devices; motion | Design director, UX, engineer, editor, data visualization (glyph review), creative director | A preview build of fourteen chapters; before and after boards; icon craft checks; contrast output; token parity test | The largest drawing load of the commission. Similarity fixes across 20 topics and the new atlas symbols |
| 3 Data visualization and systems | Chart chooser; palettes; at least twenty specimens built on V7 and public data; systems grammar; six worked examples; policy workflows; final reconciliation | Data visualization, research, design director, UX, editor, engineer, creative director | Three chapters; a script showing zero mismatches against V7; grayscale proofs; complex examples at desktop, phone, keyboard and export | Sourcing public data without page access |
| 4 Applications and reports | Web and atlas views; newsletter and email; social; the twelve-page report; print; slides; event signs; video frames; photography and video rules | Design director with UX, research (platform specs), editor, engineer, creative director | Every application at exact size; the email with images off; every report page | Platform specs must be checked on official pages. No image generation tool connected in this session, so conceptual images become prompts and labeled placeholders unless one connects |
| 5 Assembly and verification | Single-file guide; asset package; AI builder brief; full test matrix; validation report | Engineer, UX, editor, research, design director, creative director | The three deliverables and the definition-of-done checklist | File size under 16 MB with embedded fonts and specimens |

## 8. Phase 1 proposal

**Phase 1 produces:**

1. **Research ledger,** extending `brief/20261020_Research-Verification-Ledger.md`: every starting point re-verified; civic and cultural identity benchmarks; interactive references with the mechanism each teaches; the OFL position on a logo built from Inter Tight and Lora outlines; the URW replacement recorded.
2. **Strategy and direction board:** positioning; audiences; brand architecture across the publication, newsletter, atlas, trackers and reports; the Act pattern that separates process pieces from labeled position pieces; a written nonpartisan rule set; the voice line revision beside the original; a headline system where each chapter's h2 names the chapter and its instruction sits beneath.
3. **Identity refinement board,** one panel per element, each marked as a defect fix or an option:
   - Re-exported outlines for the six clipped symbols (defect).
   - Equal hinge gaps.
   - Wordmark masters for display, 24 px and 16 px with optical tracking.
   - The ampersand in two options: an optical tune of the current glyph with a true small master, or a drawn ampersand that keeps the recognizable silhouette and becomes Oath & Action's own.
   - A lockmark master for small sizes.
   - One set of minimum sizes with no gaps or conflicts.
   - The red ampersand on Prussian, with options.
4. **Symbol family board:** one skeleton per pillar in two directions. Direction A is a geometric solid, drawn from study 06 and the filled-silhouette references you shared today. Direction B is a line with one accent, drawn from study 08 and the offset-accent references. Each is shown filled, as a line and as a tile, at 16, 24, 48 and 96 px, in monochrome, on all four surfaces and in one composition. Four sample topics are redrawn in the leading grammar as proof. A map shows where each sanctioned treatment belongs.
5. **Systems marks board:** the evidence line code, grade display words, typed ID chips, the ordinal effect mark, the event mark and the authority mark, each with a recommendation.
6. **Guide architecture map,** with the navigation model at desktop and phone and one chapter wireframed in the new template.
7. **Token architecture,** with naming, categories, the rule for adding a token and the plan for "How to choose a token".
8. **Master Brief V2** with the corrections in section 6.
9. **Gate 1 report.**

**Order.** Research and strategy start together. The symbol directions and identity boards follow, in parallel. Architecture and tokens run beside them. The editor reviews every board, then the creative director scores everything.

**You decide at Gate 1:** the strategy and Act pattern; the voice line revision; one of the two symbol directions and the topic grammar; each identity refinement, accepted or declined; the red ampersand on Prussian; the systems marks; the architecture and navigation; the token architecture; the atlas bases (Concepts 03, 09, 10 and 11, with 07 Loop Card proposed as a fifth).

**Phase 1 does not** change any master, build any V6 chapter, or ship any reference image.

## 9. Decisions made

Yours, recorded in `work/ledger/20261020_Decision-Log.md`:

- DC-01: Act may take a labeled position.
- DC-02: the pillar marks are redrawn from one shared skeleton.
- DC-03: the atlas converges on Inter Tight, Inter and Pillar Red.
- DC-04: the voice line is editable, with any revision shown beside the original at Gate 1.

The studio's routine decisions D0-01 to D0-09 are in the same log.

## 10. Open questions

The full list, with defaults, is `work/ledger/20261020_Open-Questions.md`. In order:

1. Are the demo bills, people and organizations real? (Default: invented, labeled or replaced.)
2. Which tool made icon studies 04, 05 and 08, under which plan, and did any outside image go into a prompt?
3. Is Oath & Action the owner of Concepts V1 and V2, the Atlas Visual System and Atlas V7?
4. Is a photography commission or licensed documentary photography planned before launch?
5. Do you hold any stock licenses? (Default: none.)
6. Where do the video-call screenshots in data-viz references 25 to 28 come from? They show private people's names.
7. Should the V7 inconsistencies go to an atlas V7.1? (Default: log only.)
8. Which platforms matter at launch?
9. Can this environment's network access be widened so research can open pages?
10. Example geography. (Default: Massachusetts and national, rotated across issues.)

You also shared five icon style collages during Phase 0. They are recorded in `work/research/20261020_Icon-Style-References-Chat.md` and feed the Phase 1 symbol directions. Two carry Getty watermarks, and all five are study only.

## 11. Change log

**Created**
- `oath-and-action-v6-brand-guide/` project folder, from the kit
- `.gitignore`
- `source/` copies of the nine supplied files
- `work/ledger/`: `20261020_Source-Manifest.md`, `20261020_Decision-Log.md`, `20261020_Change-Ledger.md`, `20261020_Open-Questions.md`, this report
- `work/research/`: `20261020_Rights-Ledger.md`, `20261020_Icon-Style-References-Chat.md`
- `work/handoffs/phase-0/`: six audits, the reconciliation table, census summary, render report, measurement and metadata JSON files, `ux-data/`
- `work/boards/`: `20261020_Gate-0-Review-Board.html`, `sprite-sheet.html`, `phase-0/` (two diagnostic boards with PNGs), `gate-0-images/`
- `work/build/scripts/`: `extract_sources.py`, `render_v5.js`, and the audit scripts in `phase-0/`
- `work/extract/` and `work/boards/screens/` (generated, not committed)

**Modified**
- The commission kit in both copies (`CLAUDE.md`, the brief, all six phase prompts, two agent files): ledger and gate report names now carry a date prefix (change C-001)

**Not modified**
- Every file in `source/`
