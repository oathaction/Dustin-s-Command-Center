# Token build notes

Phase 2, item 3 of the Gate 1 proposal (Gate 1 report section 9) and step C of the third handoff of November 6. Built November 6, 2026 by the studio engineer, in the `oa-engineer` role, run as a subagent of the main session.

## What I built

One source file now generates both token files. The source states recipes: a palette color, the color it mixes toward and the amount, or a size in the unit the brand sets it in. The generator computes every hex, sRGB component, contrast ratio, `clamp()` size, rem value and em value, then writes `tokens.json` in the Design Tokens Community Group format (DTCG, Format Module 2025.10) and `tokens.css`. Before it writes, it runs the rule test on a temporary copy, and a failure leaves the files on disk as they were.

Seven test files hold the files to the spec. The parity test checks that the JSON and the CSS say the same thing. The rule test checks contrast on every surface, Rule 05.3, the chart rules and the rest of the Token Architecture. The self-test plants 35 broken copies and proves each one is caught by the test aimed at it. Style Dictionary 5.8.0 cross-checks the JSON, and Chromium resolves every token in a real page. One command runs all of it.

| File | Job |
|---|---|
| `work/build/tokens/src/oa-tokens.src.mjs` | The one source of truth |
| `work/build/scripts/phase-2/tokens_build.mjs` | The generator, zero dependencies |
| `work/build/tokens/tokens.json` | 485 tokens, DTCG 2025.10, aliases kept as `{path}` references |
| `work/build/tokens/tokens.css` | 605 custom properties, four surface classes, the reduced-motion block |
| `work/build/tests/tokens/run_token_tests.py` | The one command |
| `work/build/tests/tokens/test_token_parity.py` | Parity, JSON against CSS |
| `work/build/tests/tokens/test_token_rules.py` | Contrast and rule test |
| `work/build/tests/tokens/test_token_selftest.py` | The 35 plants |
| `work/build/tests/tokens/sd_crosscheck.mjs` | Style Dictionary cross-check |
| `work/build/tests/tokens/test_token_render.mjs` | Rendered check in Chromium |
| `work/build/tests/tokens/token_test_lib.py` | The tests' own color math, alias resolver and CSS reader |
| `work/build/tests/tokens/20261106_Token-Test-Results.json` | The last run: steps, counts, plants and the role table by surface |

## The source form, and why

The source is a single JavaScript definition module, not a set of DTCG JSON partials. Three reasons decided it.

1. Nothing computed is typed by hand. Deep Stone is written as Stone mixed 18% toward Charcoal, and the 13 px label as 13 px. In JSON partials the hex, the components, every stored ratio and every `clamp()` string would be typed, and only a test would stop them drifting from their recipe.
2. JSON has no comments. The module carries the decision number beside every token a later decision changed, and the reason a value stays out.
3. A role on four surfaces is written once, as a map from surface to value, so a role cannot drop a surface by accident. Where a surface has no token, such as any red on Prussian, the map leaves it out on purpose.

A person who changes a value edits the module and runs the build. Tools read `tokens.json`, and Style Dictionary reads it without any adapter.

## How the two files are laid out

**tokens.json.** Groups follow sections 1 and 2 of the Token Architecture: `oa.color` (palette, derived, tint, surface and roles), `oa.font`, `oa.type`, `oa.space`, `oa.size`, `oa.layout`, `oa.radius`, `oa.border`, `oa.opacity`, `oa.motion`, `oa.zIndex`, `oa.chart` and `oa.component`. Each token's `$extensions["org.oathandaction"]` (D1-06) holds what DTCG cannot: its tier, job, kind, surface and stored contrast; a derivation with its CSS `color-mix()` form; for type, the em tracking, the `clamp()` size and the minimum size; for the full radius, `50%`; for durations, the reduced-motion value. The root `$extensions` holds the version, the needs register, Rule 05.3 word for word, the register of held and rejected values, and the chart rules.

**tokens.css.**
- `:root` declares one property per token. A typography token becomes a `font` shorthand plus eight part properties, since CSS cannot hold a composite and the `font` shorthand drops letter-spacing. Set type with `font: var(--oa-type-body); letter-spacing: var(--oa-type-body-letter-spacing);`.
- Four surface classes, `.oa-surface-newsprint`, `.oa-surface-white`, `.oa-surface-charcoal` and `.oa-surface-prussian`, set the background, the ink, `color-scheme` and 90 short names, such as `--oa-color-text-secondary`. A short name with no token on that surface is set to `initial`, so a value from an outer surface can never leak in. Red therefore cannot reach Prussian through inheritance.
- The Charcoal class is the dark ground block. It points interface and chart roles at their Charcoal values (DR-50) and sets `color-scheme: dark`.
- The reduced-motion block sets every duration to 0 ms.
- The header carries the version and the breakpoint queries in em, because media queries cannot read custom properties.

## Token counts by group and tier

| Group | Primitive | Semantic | Component | No tier | Total |
|---|---|---|---|---|---|
| `oa.color.palette` | 7 | | | | 7 |
| `oa.color.derived` | 3 | | | | 3 |
| `oa.color.tint` | 27 | | | | 27 |
| `oa.color` roles (surface, text, graphic, border, focus, identity, action, state, data) | | 137 | | | 137 |
| `oa.font` | | | | 10 | 10 |
| `oa.type` | | 14 | | | 14 |
| `oa.space` | | | | 12 | 12 |
| `oa.size` | | | | 5 | 5 |
| `oa.layout` | | | | 23 | 23 |
| `oa.radius` | | | | 2 | 2 |
| `oa.border` | | | | 7 | 7 |
| `oa.opacity` | | | | 2 | 2 |
| `oa.motion` | | | | 9 | 9 |
| `oa.zIndex` | | | | 5 | 5 |
| `oa.chart.color` | | 64 | 17 | | 81 |
| `oa.chart` sizes | | | | 97 | 97 |
| `oa.component` | | | 44 | | 44 |
| **Total** | **37** | **215** | **61** | **172** | **485** |

Tiers apply to color and type, where section 2 defines them. Sizes, durations and the other scales carry literal values with no tier.

## Commands

Run both from `oath-and-action-v6-brand-guide/`.

- **Build:** `node work/build/scripts/phase-2/tokens_build.mjs`
- **Test, one command:** `python3 -I work/build/tests/tokens/run_token_tests.py`

The test command runs the build check, parity, rules, the self-test, the Style Dictionary cross-check and the rendered check, and writes the results file. It takes about seven seconds. Style Dictionary needs `cd work/build && npm install --no-save style-dictionary` once per container; `node_modules` stays out of git. Without it, or without Playwright, that step reports itself skipped.

## Version

The files carry **6.0.0-gate2.1** with status **pre-release**. Gate 2 has not approved the token files, so they have not shipped. In SemVer a pre-release sorts after the Phase 1 draft's 6.0.0-draft.1 and before 6.0.0, which these files become when Dustin approves them at Gate 2.

## Where the values come from, and where a later decision won

- **T-1 to T-11** as approved at Gate 1 (G1-03, T5): DTCG 2025.10, the names and tiers of sections 1 and 2, OKLab mixes, Deep Stone at 18% (#4E535B), Dim Newsprint and Error Band, Rule 05.3 with keylines and no derived red, the ask label in White at 19 px bold, section 4's states, the 13 px floor with no exceptions, labels at 13 px with 6% tracking, measures in rem, two decorative opacity jobs, V5's timings, a still loading state, the Node generator with Style Dictionary as a cross-check, and SemVer from 6.0.0.
- **Rule 05.3** reads as D2-01 with the sentence DR-66 approved. The rule test reads both lines from the decision log and fails if the stored wording differs.
- **Chart grounds.** Chart tokens exist on Newsprint, the page color (DR-53), and on Charcoal, the dark ground (DR-50). On White and Prussian the surface classes set them to `initial`.
- **Diverging pair B (DR-54)** comes from the palette lab's recipes in `work/build/scripts/phase-2/dataviz_palette_lab.py`, which Explainer reads and prints. Explainer's own S06 still draws diverging A (Stone to Verdigris); DR-54 and the creative director's finishing list replace it, so diverging A is not a token. Pair B has no Charcoal ramp yet, because none has been measured.
- **Data context on Charcoal.** Section 3 set Dim Newsprint. Explainer (DR-52, later) sets context marks one step quieter, Stone mixed 35% toward Newsprint (#878A8F, 5.41:1), because Dim Newsprint carries secondary text there. The later decision wins: `oa.color.data.context.onCharcoal` takes #878A8F, and `oa.color.graphic.subtle.onCharcoal` keeps Dim Newsprint.
- **Explainer's colors** come from `ground_tokens()` in `work/boards/phase-2/data-viz/01-explainer/build_concept.py`: the subject and context inks, secondary text, light fill, track, gridline, band, the evidence chip, text on a subject bar, red, and the Charcoal lifts. The stretch test's added colors come from `stretch_ground()` in `stretch/build_stretch.py`: five sequential Verdigris steps per ground with their label inks, S12's four gray phone steps (DR-64), map land and the circle outline. Explainer's `rule` ink is page chrome, which `oa.color.border.hairline` already covers.
- **Party marks (DR-48, DR-58)** take one neutral ink per ground, `oa.chart.color.party.mark`, which points at the subject ink.
- **Icons and tiles (DR-66, DR-67).** A red icon accent carries a 24 px minimum (R10, R11), and the app icon and avatar tiles point at Charcoal (R13).
- **Chart type faces (DR-47)** appear in the chart type tokens' descriptions. The chart type tokens are sizes only.
- **The palette lab's cautions (D2-95)** keep the four categorical inks out of the token set for now. No built chart uses them, so no need is measured.

## Chart values left with their specimen

These sixteen `STRETCH_TOKENS` values describe one dataset's axis, bins or key, not a brand size, so they stay with the S11 to S16 builders:

- `arrow.key_points`
- `shift_axis.far_segment`, `near_segment`, `tick_step` and `phone_lollipop_ppp`
- `tile.phone_steps`
- `tile_arrow.key_points`
- `spark.px_per_point`, `phone_px_per_point`, `domain` and `ticks`
- `columns.prelim_months`, `domain` and `ticks`
- `bubble.bins` and `key_millions`
- `results.shift_px_per_point`

Every other `CHART_TOKENS` and `STRETCH_TOKENS` value is a token, with a `source` record naming its Python key.

## Proposed decision lines

| # | Decision | Reason |
|---|---|---|
| D2-xxx | The token source is one JavaScript module of recipes, `work/build/tokens/src/oa-tokens.src.mjs` | No computed number is typed by hand, and comments carry each value's decision |
| D2-xxx | The token files carry version 6.0.0-gate2.1, status pre-release | Gate 2 has not approved them; the label sorts between the Phase 1 draft and 6.0.0 |
| D2-xxx | Chart tokens exist on Newsprint and Charcoal only; White and Prussian set them to initial | DR-53 makes Newsprint the chart ground and DR-50 Charcoal the dark one |
| D2-xxx | Data context on Charcoal takes Stone 35% toward Newsprint (#878A8F, 5.41:1) in place of Dim Newsprint | DR-52's Explainer keeps context marks quieter than the Dim Newsprint secondary text |
| D2-xxx | Diverging pair B becomes five Newsprint tokens from the palette lab's recipes; diverging A is not adopted; Charcoal waits for a measured ramp | DR-54 picked B, and no Charcoal ramp exists |
| D2-xxx | Sequential Verdigris and the gray magnitude steps become tokens with label inks picked by measured contrast | The stretch test's S16 and S12 use them, and DR-64 makes gray phone steps a rule |
| D2-xxx | The categorical inks and sequential Prussian wait for the Phase 3 palette specification | No built chart uses them, so condition 1 has no measured need |
| D2-xxx | Sixteen dataset values in STRETCH_TOKENS stay with their specimens | They describe one dataset's axes, bins and keys |
| D2-xxx | Explainer's "Newsprint 45% toward White" is recorded as White 55% toward Newsprint | OKLab mixing is linear, so the value is the same and D1-04's form holds |
| D2-xxx | Chart tint primitives take recipe names, such as stoneN55 and verdigrisN52p75, with p for a decimal point | One primitive per value; the job lives in the chart role that points at it |
| D2-xxx | Chart sizes take readable names, such as subjectRadius for subject_r, and record their Python key | The kit can map them, and the names read in CSS |
| D2-xxx | On Charcoal and Prussian, the primary button's hover fill steps from Newsprint to White | Section 4 names only the light-surface step; the Charcoal label holds 18.73:1 on White |
| D2-xxx | oa.color.data.emphasisRed enters now at rank 3, with a keyline on Newsprint and no Prussian token | Explainer's red demonstration uses it; section 2 reserved the name |
| D2-xxx | The selected state's 4 px bar takes the surface's primary ink, measured on the selected band | Section 4 names the bar and not its ink |
| D2-xxx | The selected band and error band name the text they carry, and both primary and secondary text are measured on them | A band passes only when every text set on it passes |
| D2-xxx | oa.size holds icons at 16, 24 and 48 px and targets at 24 px (WCAG 2.5.8) and 44 px | Master Brief section 10 lists size tokens; R9 and R10 key to these sizes; studio tabs and links use 44 px |
| D2-xxx | The focus ring, link underline and hover underline get border widths of their own | One job per token; section 4 names them |
| D2-xxx | The hinge (680 ms) and lever (560 ms) durations join motion | Section 5 names them, and the draft left them out |
| D2-xxx | Grid columns, gutters and margins become tokens beside each breakpoint, and the 360 px width takes no query | CSS cannot read the draft's extension fields, and 360 px is a test width of the base layout |
| D2-xxx | A typography token becomes a font shorthand plus eight part properties in CSS | CSS cannot hold a composite, and the shorthand drops letter-spacing |
| D2-xxx | A surface class sets each role its surface lacks to initial, and sets color-scheme | No value leaks from an outer surface, so red cannot reach Prussian by inheritance |
| D2-xxx | The held Verdigris on dark and the rejected reds stay in the root register, out of the token files | Section 6 keeps held and rejected values unused |
| D2-xxx | The build runs the rule test on a temporary copy and writes nothing when it fails | Token Architecture section 7, step 2 |
| D2-xxx | Style Dictionary 5.8.0 is installed with npm install --no-save for the cross-check and not committed | T-11; node_modules stays out of git (D0-05) |
| D2-xxx | A rendered check in Chromium joins the token run | The browser's own color-mix() and var() resolution check the generator's math |
| D2-xxx | The file keeps the name tokens.json | Master Brief section 20 names it; DTCG recommends .tokens.json, which the package can add in Phase 5 |

## For the main session to decide or tell Dustin

1. **Data context on Charcoal** changes a Gate 1 table value (Dim Newsprint to #878A8F) on the strength of DR-52. If Dustin reads DR-52 as approving the chart system and not its dark palette, revert the one line in the source; the chart context token follows it.
2. **The primary button's hover on dark surfaces** (Newsprint to White) is my call, since section 4 names only the light-surface step.
3. **The guide build reads these files.** `work/build/scripts/phase-2/guide_build.py`, written in parallel, inlines `tokens.css` when it exists, and now it does. Master Brief section 21's test that the guide and the token files agree waits for that build.
4. **Atlas System 1 draws on White** (its body ground is #FFFFFF), while DR-53 makes Newsprint the atlas page color. That belongs to chapter 21's work, so I changed nothing.

## Atlas System 1 values that look like future tokens

From `work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py`, for chapters 15 and 21. I added none of them.

- Link weights `--ak-w-lo` 2 px, `--ak-w-hi` 3 px and `--ak-w-sel` 6 px.
- Arrowheads by link weight, `ARROW` {2: (10, 8), 3: (13, 11), 6: (22, 18)}; tag sizes, `TAG`; and bend radii, `BEND` {2: 8, 3: 12, 6: 18}.
- The drawing type scale `STY`: station 20 px Inter Tight 700 on 22, map label 15 px 600 on 18, note 13 px on 16, eyebrow 13 px 700 on 18, head and count 22 px 800 on 26, figure 40 px 800, caption 14 px on 20.
- The station pill: minimum height 44 px, stroke 2 px, 1 px when sketched.
- The side panel width `--ak-panel-w` 420 px, the gutter 24 px and the drawing's minimum width 1312 px.
- Page type: display 56 on 60 at −0.035 em and headline 40 on 44 at −0.03 em. These differ from the guide's own type scale.
- The count chip, 26 px tall and 22 px compact.

## Tested

Every check below ran in this session on the files as written to disk.

- Build check: `tokens_build.mjs --check` finds both files equal to what the source builds (485 tokens).
- Validation gate: a copy of the source with Deep Stone at 5% failed three rule checks (Deep Stone on Error Band at 4.09:1), and the build wrote nothing; the target files' checksums held.
- Parity: 485 tokens, 605 `:root` properties and 90 short names in each of four surface classes, with 0 failures. Every JSON token has its property and the CSS has none the JSON lacks. Aliases are mirrored as `var()`, and every value resolves the same. `clamp()` sizes hit their minimum at 390 px and their maximum at 1440 px, em tracking matches the stored rem, and `50%` matches 0.5. The surface classes hold exactly the expected names, and the reduced-motion block holds every duration and nothing else.
- Rules: 485 tokens, 30 derived colors and tints, 201 semantic color cells measured, 0 failures. This covers the DTCG shape, the locked palette, the five conditions with every derivation recomputed in OKLab, the tiers, contrast on every surface with keylines, other grounds and band text, Rule 05.3 in the JSON and in the stylesheet, the party, diverging and scale rules, type, opacity, motion, icons, tiles and the version.
- Section 3's table: every value the Token Architecture prints for the four surfaces measured the same, except data context on Charcoal, which changed as described above.
- Self-test: the clean files pass, and 35 of 35 plants are caught by the test aimed at each. The seven named in the brief are a changed CSS value, a missing CSS property, an extra CSS property, a red ask on Prussian, Stone as secondary text at 4.29:1, a broken alias and a party mark in Pillar Red. The other 28 are a changed JSON value, a red leak onto Prussian through the surface class, a chart role leaking onto White, a party in Prussian, a party color pair, working red without its keyline, red text, a red hinge divider, a red diverging step, a derived red, a wrong derivation, a missing need, a changed Pillar Red, a stale ratio, an 11 px label, a 15 px ask label, 12 px chart type, a third opacity job, a transparent color, an off-V5 duration, a missing reduced-motion line, a broken `clamp()`, a 16 px red accent, an app icon tile on Newsprint, an alias cycle, a component pointing at a primitive, a reworded Rule 05.3 and a stylesheet edited by hand.
- Style Dictionary 5.8.0 read all 485 tokens as DTCG, and every name and value agreed with `tokens.css`; the 120 typography part properties are the only properties it does not produce. It reported a planted Stone change.
- Rendered check in Chromium 153 (Playwright): 454 token values computed as the JSON resolves them. The browser's own `color-mix(in oklab, …)` painted all 30 derivations to the exact hex, with a largest channel difference of 0. 360 short names nested inside another surface computed to their own surface's value or the fallback. 14 type styles computed to their minimum at 390 px and their maximum at 1440 px, with weight, line height and tracking. 6 durations fell to 0 s under reduced motion. It reported a planted red leak onto Prussian.
- The DTCG 2025.10 format and color pages loaded this time (designtokens.org), and I read sections 4, 5, 6.1 to 6.3, 7.1, 7.2, 8 and 9.8 and the color module's format section. They confirm the items Phase 1 marked as unread: dimensions take only px and rem, `.tokens` and `.tokens.json` are the recommended extensions, `$root` and `$deprecated` exist, and aliases use curly braces, with JSON Pointer `$ref` as a second syntax. These files use curly-brace aliases only.

## Not tested

- The guide reading these tokens. The guide build has not run against them, so Master Brief section 21's check that its computed values match the token files waits.
- Contrast measured on rendered pages, forced colors, print, and grayscale or color-vision proofs of the scales. The palette lab simulated color vision earlier; I did not run it again.
- Validation against a JSON Schema. DTCG has published none; its editors' note says one is being explored.
- Import into Figma, Tokens Studio or any DTCG tool other than Style Dictionary.
- The Resolver Module (themes), which I did not read and the files do not use.
- Ownership of oathandaction.org, the `$extensions` key.
- The measures (33.88, 37.37 and 41.91 rem), which I carried from Phase 1 and did not measure again; Phase 1 ignored kerning.
- The chart kit drawing from these tokens, which is Phase 3 round 0.

## Change log

Created:
- `work/build/tokens/src/oa-tokens.src.mjs`
- `work/build/tokens/tokens.json`
- `work/build/tokens/tokens.css`
- `work/build/scripts/phase-2/tokens_build.mjs`
- `work/build/tests/tokens/run_token_tests.py`
- `work/build/tests/tokens/test_token_parity.py`
- `work/build/tests/tokens/test_token_rules.py`
- `work/build/tests/tokens/test_token_selftest.py`
- `work/build/tests/tokens/sd_crosscheck.mjs`
- `work/build/tests/tokens/test_token_render.mjs`
- `work/build/tests/tokens/token_test_lib.py`
- `work/build/tests/tokens/20261106_Token-Test-Results.json`
- `work/handoffs/phase-2/20261106_Token-Build-Notes.md` (this file)

Installed, not committed: Style Dictionary 5.8.0 and its 105 dependencies in `work/build/node_modules/`, which `.gitignore` excludes.

Modified: none. The Phase 1 draft and scripts, the ledgers, `source/`, `work/extract/` and every board and concept folder are unchanged.
