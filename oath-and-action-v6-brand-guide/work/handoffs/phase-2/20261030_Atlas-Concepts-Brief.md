# Atlas visual system: concepts brief

Oath & Action Brand Guide, Edition 06. Phase 2, October 30, 2026. Written by the main session from Dustin's request and answers of October 30 (DR-12 to DR-21). Every agent on this work reads this file first. Section 9 fills in after the Stage 1 memos.

## 1. The ask, in Dustin's words

- "We need to be able to visual the entire system and click down into closer views of sub-systems, system components, problems/reforms/loops. It should be easy to understand, intuitive (if possible), and look really really good."
- "Distinct, very visual, intuitive and beautiful." The current system stays the fallback (G1-11).
- "The bar for everything: a finished product that looks like it was made by the best branding and design team in the world."
- On the loop catalog: "Rather than have the icons for all the loops look relatively the same, I think it would look good to just use a smaller image of the actual loop. The pages with all loops would be a page with lots of slightly different looking loops." He likes a catalog that carries more text about each loop.
- "I'd rather see a higher quantity of high-quality 1-2 page concepts than only a handful of more fleshed out concepts."
- Scope: a spec and working specimens, never a redesign of the working atlas file (G1-08).

## 2. What each concept delivers

Twelve concepts (DR-12). Each one is:

1. **The overview**: the whole system on one screen at 1440 px, written for a first-time public reader (DR-19).
2. **One close-up**, the same subject in every concept so Dustin compares like with like (DR-13):
   - the loop close-up is **R10**, "Safe seats shift accountability to small primary electorates";
   - the sub-system close-up is **area C, Electoral competition**, which holds R10. A concept may show both if it fits in two pages.
3. **A strip of all 23 loops**, each drawn as its own route across the concept's system map, with each step's sign and evidence texture (DR-15). R8 appears here.
4. A working click from the overview into the close-up and back, with hover where wires are dense, in plain HTML (DR-16).
5. A 390 px phone form of each view, with no sideways scroll.

The levels (DR-14): the system; an area with all its variables; a loop or a variable; a reform. No invented tier between area and variable.

## 3. The model

Read `work/boards/phase-2/maps/20261028_Maps-Model-Data.json`, generated from Atlas V7 (snapshot October 15, 2026) on October 28 (DR-20). Never type a label, sign or grade by hand; read it from the file.

| Key | What it holds |
|---|---|
| `generated.counts` | 51 variables, 118 connections, 23 loops (20 numbered), 50 reforms, 1,099 sources |
| `areas` | Ten areas: A to E and X (outside drivers) in the core layer; production, household and money in the economy layer; TC in the technology layer. Each has a title, a one-line text and its variables |
| `nodes` | 51 variables: `type` (stock, flow, auxiliary, driver), `area`, `title`, `label`, `short`, `increase_means`, `loops` |
| `links` | 118 connections: `from`, `to`, `polarity` (+, -, or none for authority), `type` (causal, money, information, authority, ownership), `delay` (S, M, L), `evidence`, `name`, `loops` |
| `loops` | 23 loops: `type` R or B, `kind_word`, `kind_gloss`, `title`, `closure`, `steps` (each step a full connection), `stations`, `weakest`, `reforms`, `summary`, `how_to_read`, `qualification`, `delay_word`, `direction_word`, `reference_mode` |
| `loop_order`, `groups` | Catalog order, and which loops belong to which area (SK: three sketched loops without a complete numbered chain) |
| `reforms` | 50 reforms: `targets` (connections and variables), `loops`, `band`, `effects` by family, `routes` with feasibility and check dates, `problem_grade`, `remedy_grade` |
| `families`, `effect_codes`, `route_names`, `feasibility_scale`, `glossary` | Words for effect families, ordinal codes, routes and terms |

Loop lengths: 12 loops have two steps, 7 have three and 4 have four. Shape by step count alone gives three repeated forms, which is why DR-15 draws each loop as its route across the system.

The subjects:
- **Area C** holds C1 Safe seats, C2 Primary decisiveness, C3 Electoral pressure, C4 Incumbent control of election rules and C5 Sanction applied, with loops R4a, R10, R12 and B4 grouped under it.
- **R10** runs C1 to C2 (L08, +, documented, under 2 years), C2 to C3 (L25, minus, well supported, under 2 years), C3 to C4 (L53, minus, plausible, the weakest step, 2 to 10 years) and C4 back to C1 (L42, +, documented, 2 to 10 years). Read these from the file; the line here is a guide.
- **R-01**, "All-party primaries with ranked general elections", targets L25, L08 and C2 and sits on R10, B4 and R11. Effects DQ +M, GE +S, EP 0, EQ 0, never summed.

## 4. Brand rules that bind every concept

**Palette** (locked, Master Brief section 3): Newsprint #DCD9D2, Charcoal #121212, Pillar Red #E63946, Prussian #1F2D5A, Stone #5D636D, Verdigris #4A7C74, White #FFFFFF. Approved derived (T4): Deep Stone #4E535B for small secondary text on Newsprint and White, and Dim Newsprint #A3A19C for secondary text on Charcoal (7.26:1) and Prussian (5.14:1). A concept may propose a new tint only with the five conditions of brief section 10 (measured need, derived by a documented OKLab mix, one job, contrast passes, a token name), and it is marked as proposed.

**Type** (locked): Inter Tight for display, Inter for reading and interface, Lora Italic for editorial quotation. Load them from Google Fonts. No other faces.

**Rule 05.3, the red rule**, quoted from D2-01: "The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither do the ampersands inside the hinge diagram and the hinge-circle badge, which are identity marks. The hinge diagram never shares a view with the wordmark and never stands in for the hinge divider. An icon's red accent counts as signature red when the icon stands alone, as an app tile, an avatar or a single feature icon. In a row or a menu, icons go one color and only the current one keeps its red. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline's ampersand uses the view's working red. The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian."

DR-18 reads it for atlas views: with no reform in view, the selected item is the point the headline names and may take the working red; with a reform in view, the reform's targets take it.

**Systems grammar** (Gate 1, M1 to M4, and brief section 14):
- Evidence line code from V7: solid for documented and well supported, dashed for plausible, dash-dot for contested, dotted for hypothesis. Grade words are V7's (M2), each with a plain gloss at first use. No brand graphic uses a dotted or dashed line for anything else (D1-21).
- A plus sign means the two variables move the same way and does not mean a benefit. Authority connections (LE02, LE03, LE19, LT13, LT14, LT16, LT17) carry no sign and never close a loop.
- Delay is its own encoding, separate from evidence.
- R loops feed themselves (reinforcing); B loops push back (balancing). Three loops are sketches without a complete numbered chain (B2, B3, R9), and two are closed with a hypothesized step (R2, R16). Say so plainly.
- Reform effects are categorical and never summed.
- Labels and line patterns must survive the removal of color.

**Icons**: the Civic Line set is approved and closed (DR-07). Every variable and reform has an icon: `work/boards/phase-2/atlas-concepts/shared/20261030_Variable-Icon-Map.json`. Use the drawings exactly as delivered, through `icon_svg()` in `work/build/scripts/phase-2/atlas_concepts_common.py`, which keeps ids unique on the page (D2-52). One-color editions in rows and menus; only the current item keeps its red (G1-07). Icon names are not V7 labels; the page prints V7's label.

**Writing** (CLAUDE.md): plain spoken prose in active voice, no em dashes, none of the listed patterns. Headlines in the concept may be studio drafts; label them so in the notes. Every figure on the page comes from the model.

## 5. Accessibility floor

- Text at 13 px or larger, SVG text measured at its rendered size.
- Text contrast 4.5:1, or 3:1 at 24 px and over (or 18.66 px bold). Graphics that carry meaning 3:1.
- Every view works by keyboard, with a visible focus ring, and every drawing has a text alternative ("the lines in words").
- 390 px with no sideways scroll. A wide drawing may sit in a focusable scroll region (`role="region"`, `tabindex="0"`, an `aria-label`) with a link to full size.
- axe-core 4.10.2, WCAG 2.2 AA tags: 0 violations.

## 6. The rubric

Master Brief section 6, 1 to 5, ship threshold 4 on every line: craft, clarity, brand fidelity, usefulness, evidence honesty, accessibility, and beauty and distinctiveness ("would a renowned studio show this?"). Two extra tests for this work:
- **The ten-second test.** A first-time reader looking at the overview for ten seconds can say what the system is about and where to click.
- **The wall test.** The overview would hold a wall at poster size.

## 7. The roster

| # | Concept | Grown from |
|---|---|---|
| 01 | The Circuit, refined | Concepts V2, Concept 09 (`work/research/chat-references/atlas-concepts/20261030_Ref-Atlas-Concept-09-The-Circuit.png`) |
| 02 | The Stack | The Civic Architecture layers and the Decision Grid |
| 03 | Night Schematic | Fine Structure and the Civic Circuit grouped overview, on a dark ground |
| 04 | Civic Landscape | The Civic Landscape territories |
| 05 | Loop Card as the unit | Concept 07 Loop Card (R10) and the Civic Architecture loop page |
| 06 | Loop Lines with the Field Guide | The October 28 studio pick, with loop-route thumbnails |
| 07 to 12 | From scratch | Chosen by Dustin from the ideation agent's directions on Board 1 |

Grounds (DR-17): at least four dark and four light across the twelve.

## 8. Files and the technical contract

- One folder per concept: `work/boards/phase-2/atlas-concepts/NN-slug/`, holding `20261030_Concept-NN-Title.html`, its build script, its captures and a notes file. Build scripts live beside the page or in `work/build/scripts/phase-2/` named `atlas_cNN_*.py`.
- One self-contained HTML file with hash views: `#overview` (default), `#area-c` and/or `#loop-r10`, and `#loops` if the strip has its own view (D2-49). Google Fonts only; no other outside request.
- Every drawn V7 item carries data attributes, and the shared verifier checks them against the model (D2-50):
  - variables: `data-node="C1"`, and on its label `data-name` with the exact printed text;
  - connections: `data-link="L25"` with `data-sign` (`+`, `-` or `none`), `data-grade` (V7's evidence value) and `data-delay`;
  - loops: `data-loop="R10"` with `data-steps="L08 L25 L53 L42"` on each loop drawing and strip item; the three sketched loops (B2, B3, R9) have no numbered chain and carry `data-steps="sketch"`;
  - reforms: `data-reform="R-01"`;
  - printed counts: `data-count="connections"` with the number as its text.
- Every Pillar Red mark, or its wrapper, carries `data-red="signature"` or `data-red="working"`, and working reds carry `data-red-job` (D2-51).
- Every drawing is an `<svg data-view="...">`.
- The page lists its views in `<meta name="atlas-views" content="overview area-c loop-r10">`, and each view's root element carries `data-view-root="<view>"`. Links into a close-up are `<a href="#loop-r10">` or carry `data-goto`.
- Checks: `node work/build/scripts/phase-2/atlas_concepts_check.js <concept.html>` and `python3 -I work/build/scripts/phase-2/atlas_concepts_verify.py <concept.html>`. Both must pass before a concept goes to review.

## 9. Frame from the Stage 1 memos

To be added after the civic education, data visualization, interaction and design memos and the ideation pitch.
