# Chapter 10 construction and size rules

Oath & Action Edition 06, Phase 2, stage B round 2, November 10, 2026. Written by the systems designer (`oa-design-director`, checked against `oa-ux-accessibility-lead`) under `20261110_Stage-B-Round-2-Brief.md`, for the makers of chapters 09 and 11, the editor and the engineer. This is the one text chapters 09 and 11 cite for the Civic Line grid, line, red and sizes. Chapter 10 carries these rules to the reader; the rule numbers in section 0 are fixed now so other chapters can cite them.

Every figure here comes from the files or the records named beside it. Where the page and this file ever differ after the editor's copy edit, the page's words govern and I update this file.

## 0. The rules chapter 10 will print

| Rule | Title (draft; the editor may tighten the words) | Sections here |
|---|---|---|
| 10.1 | Give each kind of symbol its own job. | 1 |
| 10.2 | Build every drawing on one box, with one line, round ends and one red accent. | 2 to 5 |
| 10.3 | Keep each drawing in its whole box, at the size its file gives it. | 6 |
| 10.4 | Set topic and atlas symbols at 48 px or larger, and at 24 px only from the list of 41. | 9, 10 |
| 10.5 | Match the edition to the surface, and use only the six tiles. | 7, 8 |
| 10.6 | Set every symbol beside its own word. | 1, 11 |
| 10.7 | Give a symbol its red only where it stands alone or marks the current item. | 5 |
| 10.8 | Draw the atlas’s variables and reforms, and name its other parts in words. | 1 |
| 10.9 | Check a symbol beside its neighbors before you set it. | 12 |
| 10.10 | Copy the atlas's encoding glyphs exactly, each with its words. | 1 |

Chapter 10's anchor is `#symbols`; rules land at `#rule-10-1` to `#rule-10-10`. The shell links "Rule 10.4" wherever it appears in another chapter. The titles above are the ones the built chapter prints (`work/build/guide/chapters/10-symbols.json`); the editor may still tighten them, and the numbers stay.

## 1. The classes, and which chapter governs each

| Class | Job | Grid and drawing | Governed by |
|---|---|---|---|
| Pillar icons | Mark which pillar a piece serves, in the order Explain, Track, Connect, Act | Civic Line CL-019 to CL-022 on the 128-unit box; pixel fits at 16 and 24 px (DR-179) | Chapter 09 |
| Topic symbols | Name the subject of a piece | Civic Line, 128-unit box | Chapter 10 |
| Atlas symbols | Name a variable or a reform in our systems atlas | The same Civic Line drawings, keyed to the atlas's IDs | Chapter 10 |
| Status marks | Say where a bill, records request or agency rule stands | The tracker's circles, rings, slash and square (Rules 11.1 to 11.7) | Chapter 11 |
| Utility icons | Name an interface action beside its word | Their own 24-unit grid, 2 px line at 24 px, 1.5 px at 16 px (DR-161 to DR-178) | Chapter 11 |
| Encoding glyphs | Carry the atlas's grammar: sign, authority, evidence grade, delay, where a reform acts | System 1's constants, copied exactly (DR-36) | Shown in 10, taught in 15 |

A topic or atlas drawing never stands for an interface action (D2-515). Chapter 11's failure case shows CL-024 Feedback Loop as a refresh button; chapter 10's shows CL-048 Public Records as a downloads button.

**Atlas symbols are the 51 variables and the 50 reforms.** Each of the atlas's 51 variables has exactly one Civic Line drawing (research notes, section 2), the map is `VARIABLE_ICON` in `work/build/scripts/phase-2/atlas_concepts_common.py`, and drivers X1 to X5 are among the 51 (CL-034 to CL-038). The 50 reform drawings carry the atlas's own reform IDs, R-01 to R-50. Domains, hubs, layers and routes have no drawing: they stay words and typed chips, and nobody draws one for them.

**The set in use** is `work/build/assets/civic-line-v6/`: 124 drawings in four editions (D2-716).
- CL-001 to CL-074: 74 drawings. CL-073 Testify and CL-074 Contact an Official are new (D2-714, DR-159, DR-160). CL-019 to CL-022 are the pillar icons, and chapter 09 governs them.
- R-01 to R-50: 50 reform drawings.
- The six redraws keep their IDs (CL-014, CL-025, CL-059, R-13, R-42, R-48; DR-156 to DR-158). They are the drawings in use. The October originals stay in `work/build/assets/civic-line/` as the record and never appear on a reader page as a choice.
- The Master Brief's Bill and State house have no drawing (DR-137). A page that needs them uses the word.

## 2. The box

- Every drawing sits in a square viewBox of 128 by 128 units, `0 0 128 128`.
- Nothing is drawn outside the box once the line's width is counted (`verify_set.py`, Civic Line report section 2).
- The box is the drawing's frame at every size. A builder sets the box's size and never crops the box to the ink or moves the drawing inside it (section 6).
- The box is transparent: no background rectangle, text or image in any file.

## 3. The line

- **One line weight for the set.** The traced line is 5.5 source px, the median of the sheets (D2-31). At the shared scale it exports as 2.6807 units (D2-32).
- **In the files.** The capped fit (section 6) lets each drawing grow by up to 1.25 times, so its line runs from 2.68 to 3.35 units of 128. Each drawing keeps one width for every visible line. Three recorded exceptions follow their sheets: R-02 draws its rank cells and numerals finer, R-10 draws its walker's torso heavier, and CL-029 and R-49 use wider strokes only inside masks, where they cut gaps and never show as a line (trace review, sections 4 and 5).
- **What the line measures on screen,** for the two ends of the range:

| Box size | 2.68-unit line | 3.35-unit line |
|---|---|---|
| 16 px | 0.34 px | 0.42 px |
| 24 px | 0.50 px | 0.63 px |
| 32 px | 0.67 px | 0.84 px |
| 48 px | 1.01 px | 1.26 px |
| 64 px | 1.34 px | 1.68 px |
| 96 px | 2.01 px | 2.51 px |
| 128 px | 2.68 px | 3.35 px |

Under one device pixel a line never reaches full ink (engineer's pixel-fit check, D2-570), which is why section 9 sets the floor at 48 px. At 48 px every line is at least one CSS pixel wide.

## 4. Caps and joins

- **Round caps and round joins** are the family's finish. In the 122 October red-black files, 1,429 of 1,458 cap declarations are round and 1,456 of 1,458 join declarations are round. The eight new and redrawn finals use round caps and joins on every line.
- **Butt caps** appear at 29 places in 21 drawings, only where a line meets a color split or a mask cut, so the two colors meet edge to edge.
- **Mitre joins** appear twice, where a sheet draws a sharp point: the center of CL-057 Labor Share's divided circle and the tip of CL-070 Environment's leaf.
- A new drawing uses round caps and joins everywhere, and a butt cap only at a color split.

## 5. The red accent

- **One red accent per drawing.** The red marks one idea, the part the inventory's red note names. The accent may take one shape or a few (Track's icon colors its map pin and its magnifier's handle); round 3 put that in Rule 10.2's words (CA-S7). In the file it is the group `data-part="accent"`; the rest is `data-part="base"`. 120 October files hold one accent group, and CL-015 and R-30 split theirs into two groups for parts the sheet colored apart. Every one of the eight new and redrawn finals holds one.
- **Colors.** Charcoal `#121212` ink and Pillar Red `#E63946` accent in the red-black edition; nothing else outside masks.
- **Where red may show** (Rule 05.3 as it reads, DR-66, DR-67 R10 and R11):
  - A standalone drawing at 48 px or larger keeps its red, bare on Newsprint, as signature red. Signature red does not count against a view's one working red.
  - In a row or a menu, every drawing goes one color, and only the current item keeps its red, as signature red.
  - **No red under 48 px.** Under 48 px every Civic Line drawing is one color: a kicker's 24 px topic icon (D2-373), the pillar fits at 16 and 24 px (D2-497) and any of the 41 at 24 px.
  - Red never sits on Prussian. On Prussian a drawing takes the Newsprint edition, one color (DR-09).
- **Contrast.** Pillar Red measures 2.96 to 1 on Newsprint, under the 3 to 1 a graphic needs (SC 1.4.11). The drawing's shape carries its meaning in ink at 13.29 to 1, so the red adds emphasis and carries no meaning alone. Red measures 4.17 to 1 on White and 4.49 to 1 on Charcoal.
- **With the sprite** (engineer's notes, "Sprites"): a `<use>` draws the accent in `--oa-icon-accent` when the `<svg>` sets it, and in the ink otherwise. Set `style="--oa-icon-accent: var(--oa-component-icon-accent-on-newsprint)"` for a two-color drawing; leave it out for one color.

## 6. The capped fit

- **Framing option 3 (DR-08).** In each standalone file, a drawing grows toward 116 of the 128 units, by at most 1.25 times the shared scale. A compact drawing stops at the cap with room around it; a wide one fills to 116 units across. The line then varies by at most 25 percent across the set (2.68 to 3.35 units, section 3).
- **In the set in use,** 92 drawings stop at the cap, with a 3.3508-unit line, and 32 fill to 116 units with a lighter line. Both counts include the eight new finals: CL-025, CL-059, R-13, R-42 and CL-073 sit at the cap; CL-014 (3.09 units), R-48 (2.70) and CL-074 (2.90) fill to 116.
- Each drawing's ink box is centered on (64, 64).
- **What a builder never does:** trim the box to the ink, scale the drawing inside the box, or stretch it. Each one changes the line weight, so a row of drawings stops matching. Set every symbol in a row at one box size.

## 7. The four editions

All four share every coordinate; only the inks change (DR-09, `verify_set.py`).

| Edition | Ink | Accent | For | Contrast of the ink |
|---|---|---|---|---|
| Red-Black | Charcoal | Pillar Red | Newsprint and White, standalone or current, 48 px and up | 13.29 to 1 on Newsprint, 18.73 on White |
| Black | Charcoal | Charcoal | Newsprint and White, any size the family allows | as above |
| Red-Newsprint | Newsprint | Pillar Red | Charcoal, standalone or current, 48 px and up | 13.29 to 1 on Charcoal; red 4.49 |
| Newsprint | Newsprint | Newsprint | Charcoal and Prussian | 13.29 on Charcoal, 9.42 on Prussian |

Files: `work/build/assets/civic-line-v6/{red-black,black,red-newsprint,newsprint}/`. In a guide page the sprite draws every edition from the Black file with `color` and `--oa-icon-accent` set from the tokens:

| Surface | `color` | `--oa-icon-accent` (two-color only) |
|---|---|---|
| Newsprint | `var(--oa-component-icon-ink-on-newsprint)` | `var(--oa-component-icon-accent-on-newsprint)` |
| White | `var(--oa-component-icon-ink-on-white)` | `var(--oa-component-icon-accent-on-white)` |
| Charcoal | `var(--oa-component-icon-ink-on-charcoal)` | `var(--oa-component-icon-accent-on-charcoal)` |
| Prussian | `var(--oa-component-icon-ink-on-prussian)` | none: one color only |

## 8. The six tiles

- **Shapes and grounds (DR-10, D2-41).** Square, rounded square (a superellipse of exponent 5 with continuous curvature) and circle, each on a Charcoal tile with the light editions or a Newsprint tile with the dark editions: six tiles. Each comes in two-color and one-color, so a drawing has 12 tile files.
- **Charcoal is the default tile** for the app icon and avatars (DR-67 R13).
- **The drawing in the tile (D2-40, D2-44).** It fills 0.68 of a square, 0.66 of a rounded square and 0.62 of a circle. 36 drawings take an optical scale from 0.94 to 1.09 with the line still capped at 3.35 units, and 8 asymmetric drawings move up to 3.8 units toward their light side. Every drawing keeps at least 21 units of margin to the tile's edge.
- **Minimum tile sizes (D2-42).**

| Tile | Square | Rounded | Circle |
|---|---|---|---|
| Two-color | 72 px | 76 px | 80 px |
| One-color | 48 px | 52 px | 52 px |
| One-color, for the drawings that need 48 px on their own | 72 px | 76 px | 80 px |

  The inventory in use records each drawing's minimums: 94 drawings take the one-color row and 30 the row below it (`tile_min_px` in `20261110_Civic-Line-V6-Inventory.json`, read by script). The October set had 28 in the last row; the redraws and CL-074 change the count.
- **Never:** a Newsprint tile on a White page, where its edge measures 1.41 to 1 against White; a Pillar Red tile, which breaks Rule 05.3; red on a tile set on Prussian.
- Files: `work/build/assets/civic-line-v6/tiles/` for the eight new and redrawn drawings, and `work/build/assets/civic-line/tiles/` for the other 116, as the inventory in use points (D2-716). App platforms take the square tile and apply their own mask.

## 9. Size floors

| Family | 16 px | 24 px | 48 px and up |
|---|---|---|---|
| Topic and atlas symbols | Never | Only the 41 in section 10 (37 topic and atlas drawings plus the four pillar icons), one color | Any of the 124, at whole pixel sizes |
| Pillar icons (chapter 09) | The 16 px pixel fit, one color | The 24 px pixel fit B on 1x screens and the master on 2x screens, one color (DR-179) | The master; red is a second sign from 48 px |
| Utility icons (chapter 11) | The 16 px master, inline in text or a table heading | The 24 px master beside a control's word | Not used |
| Status marks (chapter 11) | Not used | Circles at 24, 26, 28 and 30 px (Rule 11.7) | Not used |

- **The floor for topic and atlas symbols is 48 px (DR-136).** At 48 px the line is 1.01 to 1.26 px, the first size where every line reaches a full pixel.
- **A kicker's topic icon is 24 px,** one color, 8 px directly before the topic's own word, and comes from the 37 topic and atlas drawings on the list (D2-373, DR-112). A pillar icon never enters a kicker.
- **One size per row.** Every symbol in a row, a list or a menu takes the same box size.
- **Under 48 px, one color** (section 5).
- **Tokens.** `oa.size.icon.large` (48 px) is the floor; `oa.size.icon.medium` (24 px) is the size for the 41 and the kicker; `oa.size.icon.small` (16 px) never holds a topic or atlas symbol.

## 10. The 41 that read at 24 px

**The list, by ID** (this is guide check B-3's list; D2-587):

CL-001, CL-004, CL-006, CL-010, CL-013, CL-019, CL-020, CL-021, CL-022, CL-023, CL-024, CL-028, CL-031, CL-032, CL-039, CL-040, CL-047, CL-048, CL-050, CL-051, CL-054, CL-057, CL-060, CL-061, CL-067, CL-068, CL-070, CL-071, CL-072, R-05, R-06, R-08, R-09, R-14, R-15, R-17, R-19, R-23, R-27, R-37, R-45.

That is 29 CL drawings and 12 reform drawings.

**The four pillar icons** (CL-019 Explain, CL-020 Track, CL-021 Connect, CL-022 Act) are among the 41. At 24 px they draw from chapter 09's pixel fits on 1x screens and from their masters on 2x screens (DR-179), and they never stand in for a topic.

**The 37 topic and atlas drawings** that may be set at 24 px, with the Civic Line word and, where the drawing is an atlas symbol, the atlas ID:

| ID | Civic Line word | Atlas ID |
|---|---|---|
| CL-001 | Voting | |
| CL-004 | Petition | |
| CL-006 | Civic Ties | B3 |
| CL-010 | Decisive Primaries | C2 |
| CL-013 | Incumbent Defeat | C5 |
| CL-023 | Evidence | |
| CL-024 | Feedback Loop | |
| CL-028 | Watchdogs | D4 |
| CL-031 | Local Government | |
| CL-032 | Local Reporting | B2 |
| CL-039 | Feed Ranking | TC1 |
| CL-040 | Platform Power | TC2 |
| CL-047 | Data Rights | |
| CL-048 | Public Records | |
| CL-050 | Worker Bargaining | A2 |
| CL-051 | Market Power | A3 |
| CL-054 | Home Equity | A6 |
| CL-057 | Labor Share | EC3 |
| CL-060 | Taxes & Benefits | EC6 |
| CL-061 | Household Income | EC7 |
| CL-067 | Healthcare | |
| CL-068 | Education | |
| CL-070 | Environment | |
| CL-071 | Policy | |
| CL-072 | Reform | |
| R-05 | Automatic Registration | R-05 |
| R-06 | On-Cycle Elections | R-06 |
| R-08 | Donor Disclosure | R-08 |
| R-09 | Stock-Trading Ban | R-09 |
| R-14 | Automatic Funding | R-14 |
| R-15 | Watchdog Remedies | R-15 |
| R-17 | Civil Service | R-17 |
| R-19 | Drug-Pricing Rules | R-19 |
| R-23 | Indexed Minimum Wage | R-23 |
| R-27 | Tax Enforcement | R-27 |
| R-37 | Feed Choice | R-37 |
| R-45 | Paper Ballots & Audits | R-45 |

The words on a reader page come from the editor's label table (DR-185, `20261110_Stage-B-Ch10-Labels.json`); the words above are the inventory's, for finding a drawing.

**How the list was decided.** I did not draw up a new list. The list is the creative director's, from the October 29 trace review (`20261029_Civic-Line-Review.md`, section 6): every red-black export rendered with the studio's `render_svgs.js` at 128, 64, 32 and 24 px on Newsprint, tiled in catalog order with IDs, and read by eye for whether each subject still reads. It found 41 that still read at 24 px, 53 more that read at 32 px but not at 24, and 28 that stop reading at 32 px. The stage B scoping notes carried the count to Dustin (question 4, option a), he approved it as DR-136, and the engineer left B-3's list empty until this file (D2-587). Board 6's pillar icon shortlist started from the same 41 (`20261107_Board-6-Pillar-Icons-Notes.md`). A script reads section 6's line and this file's list and finds them identical, 41 IDs with no repeat. I also rendered all 41 at 24 px on Newsprint at 1x and 2x to confirm none has changed since October: none of the 41 was redrawn, and the set in use copies them byte for byte (D2-716).

**What is not on the list, and why.**
- The six redraws (CL-014, CL-025, CL-059, R-13, R-42, R-48). Their October originals were not on it (CL-014, R-13 and R-42 stopped reading at 32 px; CL-025, CL-059 and R-48 at 24 px), and the drawings board showed every redraw at 24 px as "reference size only" (D2-673).
- CL-073 Testify and CL-074 Contact an Official, for the same reason: the board showed them at 24 px as reference only.
- The inventory in use agrees: the Civic Line hand read each of the eight finals at 24 px and recorded "does not read" for all eight (`final.reads_at_px` in `20261110_Civic-Line-V6-Inventory.json`).
- Adding a drawing to the list changes what DR-136 approved, so it goes to Dustin first. These eight stay at 48 px and up.

**For the engineer's B-3 check:** the list above as written, with the four pillar icons checked under the pillar family's rule. A topic or atlas symbol at 24 px passes only when its `data-icon` is one of the 37.

## 11. Words beside symbols (for chapters 09 and 11 to match)

- Every symbol sits with its word (DR-146, the round 2 brief's binding rules). Beside its visible word the drawing is hidden from assistive technology: `aria-hidden="true" focusable="false"` on the `<svg>` (A-1).
- A topic symbol prints its Civic Line word; an atlas symbol prints the atlas's name for the element (DR-185). CL-025 reads "Congress" as a topic and "Congressional capacity" where it stands for D1; R-13 reads "Congress's own experts"; R-36 reads "Lasting public investment"; R-35 keeps "Rejected" with it wherever it appears. The editor's table governs every word.
- Every use carries `data-icon="<ID>"` and `data-icon-family`: `pillar`, `topic`, `atlas` or `encoding` here; `status` and `utility` in chapter 11 (D2-517).

## 12. Neighbors chapter 10 sets side by side

CL-073 Testify and CL-005 Public Meeting; CL-074 Contact an Official and CL-061 Household Income; CL-025 Congress and CL-014 Entrenched Power; CL-053 Housing Scarcity, CL-054 Home Equity and CL-063 Essential Costs; CL-027 Court Alignment and CL-031 Local Government; CL-048 Public Records and CL-023 Evidence.

Each pair carries the engineer's likeness figure, computed with `icon_likeness_check.js`'s own functions on the 124 drawings in use (7,626 pairs; flag 0.9092 at the 99th percentile, watch 0.8678 at the 95th; `20261110_Stage-B-Ch10-Figures.json`). The figures: CL-005 and CL-073 −0.09; CL-061 and CL-074 0.79; CL-014 and CL-025 0.75; CL-053 and CL-054 0.70; CL-053 and CL-063 0.60; CL-054 and CL-063 0.71; CL-027 and CL-031 0.84; CL-023 and CL-048 0.69. None reaches the flag. These are neighbors by subject more than by outline: Testify and Public meeting have nearly unrelated outlines, and Court alignment and Local government come closest. Rule 10.9 says so and calls the groups neighbors.

## 13. Notes for other owners

- **Chapter 01's owner and the editor (s-01-21-correct).** Rule 01.21's kicker sets CL-055 Productivity at 24 px. CL-055 is not on the list of 41 (the trace review found it stops reading at 24 px), so B-3 will fail it once the list is on. Recommendation: swap to one of the 37 whose word fits an analysis kicker, such as CL-057 Labor Share or CL-060 Taxes & Benefits, with the kicker's word changed to match (DR-112 keeps the icon beside its own word).
- **Engineer, tokens.** `oa.component.icon.accent.*` describes the accent as shown "at 24 px and up", with `minSize` `oa.size.icon.medium`. The round 2 brief, D2-373 and D2-497 put every Civic Line drawing in one color under 48 px. Recommendation: `minSize` `{oa.size.icon.large}` and the description "at 48 px and up". The same tokens say "White on Prussian"; for a Civic Line drawing on Prussian the Newsprint edition is one color (DR-09), so chapter 10 sets the accent to the ink there and names no accent token on Prussian. The White on Prussian treatment belongs to the identity marks.
- **Chapter 09.** Section 9's pillar row is chapter 09's to state; this file only records it so the size table is whole.
- **Chapter 11.** The utility grid (24 units) is its own family; nothing in this file binds it beyond the class table and D2-515.

## 14. Tested and not tested

**Tested**
- Construction figures read by script from the 122 October red-black files and the eight approved option files (caps, joins, accent groups, line widths, viewBox).
- The 41 compared by script with the trace review's section 6 line: identical, 41 IDs, no repeat; rendered at 24 px on Newsprint at 1x and 2x in Chromium and looked at.
- The cap counts in section 6 (92 and 32 of 124) computed by script from the October inventory's line widths with the eight finals' widths put in.
- Contrast figures computed from the hex values with the WCAG 2.x formula (`stage_a_systems_core.py`).

**Not tested**
- The cap counts in section 6 against the inventory in use's own `stroke_units`: rechecked once `civic-line-v6/` landed (see the notes file).
- Whether people can name any drawing at 24 px. The list is one reviewer's reading, approved by Dustin; no reader test has covered it.
