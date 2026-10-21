# Token architecture

Oath & Action Brand Guide, Edition 06. Phase 1 proposal for Gate 1, October 21, 2026, by oa-engineer. Nothing ships until Dustin decides section 9.

A token is a named design value, such as a color or a type size, that the guide, the asset package and builders all read from one file. Figures come from `work/build/scripts/phase-1/tokens_phase1.py`.

## 1. Format, categories and naming

**Format.** The JSON follows the Design Tokens Community Group (DTCG) Format Module 2025.10. Search results from w3.org and designtokens.org describe it as the group's first stable version, a Final Community Group Report of October 28, 2025, outside the W3C Standards track. No later edition turned up. The specification page would not load here, so items marked † rest on my knowledge of the drafts.

Format rules that shape the design:

- Names may not contain `{`, `}` or `.`, or start with `$`.
- An alias (a token pointing to another) is written `{oa.color.palette.charcoal}`.
- Colors carry `colorSpace`, `components`, `alpha` and `hex`.
- Dimensions take `px` or `rem`†, with no `em`, `ch`, `%` or `vw`. So em tracking, `clamp()` sizes and percentage radii live in `$extensions`, and the generator writes their CSS.

**Categories.** The groups are `oa.color`, `oa.font` with `oa.type`, `oa.space`, `oa.size`, `oa.border`, `oa.radius`, `oa.opacity`, `oa.layout`, `oa.motion`, `oa.zIndex`, `oa.chart` and `oa.component`. They cover Master Brief V2 section 10.

**Naming.** JSON path segments use camelCase. The CSS name is `--oa-` followed by the path in kebab case, with the surface last: `oa.color.text.secondary.onNewsprint` becomes `--oa-color-text-secondary-on-newsprint`. Four generated surface classes, such as `.oa-surface-prussian`, point short names like `--oa-color-text-secondary` at that surface's tokens. JSON holds only the explicit tokens, so each one can be tested.

## 2. Tiers

| Tier | Holds | May point to | Example |
|---|---|---|---|
| Primitive | Literal values: the seven locked colors, derived colors, the scales | Nothing | `oa.color.derived.deepStone` = #4E535B |
| Semantic | A role on a surface | Primitives | `oa.color.text.secondary.onNewsprint` |
| Component | One part of one component | Semantic tokens | `oa.component.button.disabled.label.onWhite` |

Identity marks use palette primitives, never tints. State and data colors have their own groups. Data reaches Pillar Red only through a future `data.emphasisRed`, which carries the one-red rule and switches off when status already uses red (tension 14). Series palettes go to Gate 2.

## 3. Roles per surface

The WCAG thresholds are 4.5:1 for text, and 3:1 for large text (24 px, or 18.66 px bold), for graphics a reader needs and for focus rings. All 21 cells of the brief's table (section 8, item 9) match the script.

| Role | Newsprint | White | Charcoal | Prussian |
|---|---|---|---|---|
| Text, primary | Charcoal 13.29 | Charcoal 18.73 | Newsprint 13.29 | White 13.28 |
| Text, secondary | Deep Stone 5.49 | Deep Stone 7.74 | Dim Newsprint 7.26 | Dim Newsprint 5.14 |
| Graphic, essential; data emphasis | Charcoal 13.29 | Charcoal 18.73 | Newsprint 13.29 | Newsprint 9.42 |
| Graphic, subtle; data context | Stone 4.29 | Stone 6.05 | Dim Newsprint 7.26 | Dim Newsprint 5.14 |
| Graphic, red (one per composition) | Pillar Red 2.96; its 1 px Charcoal keyline 13.29 | Pillar Red 4.17 | Pillar Red 4.49 | 3.19, pending the red-on-Prussian decision |
| Border, strong (inputs) | Charcoal 13.29 | Charcoal 18.73 | Newsprint 13.29 | Newsprint 9.42 |
| Border, hairline (decorative) | Stone 4.29 | Stone 6.05 | Stone 3.10 | White 13.28 |
| Focus ring | Verdigris 3.37 | Verdigris 4.74 | Newsprint 13.29 | Newsprint 9.42 |

Stone and Verdigris on Newsprint, and Pillar Red on White and Charcoal, pass for large text only. Pillar Red on Newsprint fails at every size.

**Derived values.** No palette color serves secondary text on Newsprint, Charcoal or Prussian. Three derived values fill those gaps:

| Name | Hex | Method | One job | Measured |
|---|---|---|---|---|
| Deep Stone | #4E535B | Stone 18% toward Charcoal | Secondary and disabled text on Newsprint and White | 5.49 Newsprint, 7.74 White |
| Dim Newsprint | #A3A19C | Newsprint 25% toward Charcoal | Secondary and disabled text on Charcoal and Prussian | 7.26 Charcoal, 5.14 Prussian |
| Error Band | #E1C9C1 | Pillar Red 88% toward Newsprint | Error message ground on light surfaces | Charcoal text 11.89, Deep Stone 4.91 |

The registered needs: N-01, 49 Stone-on-Newsprint text failures in the V5 census; N-02, 8 Stone failures on Charcoal and Prussian; N-03, a red-family ground for small text, which Pillar Red cannot give (Charcoal on it 4.49, White 4.17).

**The Concepts V2 Stone.** #4E535C measures 5.49 on Newsprint and 7.73 on White, and fails on both dark surfaces (2.42, 1.72). It is exactly Stone scaled to 84% in sRGB, a mix toward black, which sits outside the palette. Deep Stone lies 0.0017 away in OKLab, far below a visible difference, so its 1,606 uses can move to the token unchanged.

**Mixing method.** OKLab is a color space where equal numeric steps look equal; OKLCH is the same space as lightness, chroma and hue. Toward Charcoal, which has no chroma, both give identical results. Toward Newsprint, OKLCH swings the hue, and the Error Band would become #DBCDB6, a beige 58 degrees from red. I propose CSS `color-mix(in oklab, …)`.

**Held:** a Verdigris for status on Prussian (#59857D, 3.21), pending the Phase 2 Signal Grid. **Rejected:** a small-text red (#AC3339, 4.53 on Newsprint), 0.033 from Atlas V7's #BD2C32, which DC-03 retired; and a darker red for marks (#DA3843, 3.22), a second red that looks like the first.

## 4. State tokens

Every state changes text or shape as well as color. No state uses opacity.

| State | Color | Text or shape change |
|---|---|---|
| Muted | Secondary text; Stone or Dim Newsprint marks | Regular weight; marks drawn as outlines |
| Disabled | Secondary text, dashed edge | `aria-disabled="true"` keeps focus; a reason line says what makes it available |
| Hover | Button fill steps from Charcoal to Prussian | Label underlines; link underline grows from 1 to 2 px |
| Focus | Focus ring per surface | 2 px outline, 2 px offset, shown at once |
| Loading | Secondary text; still Stone outline lever | Visible text ("Loading tracker") in a `role="status"` region; no motion |
| Selected | Paired surface: Newsprint with White, Charcoal with Prussian | 4 px bar, check glyph, `aria-selected` or `aria-pressed` |
| Warning | Primary text; no hue of its own | Triangle glyph, the word "Warning", 4 px bar |
| Error | Pillar Red mark (keyline on Newsprint); Error Band on light surfaces | Circle-cross glyph, the word "Error", the fix in plain words |
| Empty | Secondary text; dashed Stone region | What is missing and what to do next |
| Success | Verdigris mark; Newsprint on Prussian | Check glyph and a word such as "Saved" |

Paired surfaces differ by 1.41:1, so the bar and glyph carry the selection, and every text token passes on them. Pillar Red and Verdigris measure 1.14:1 against each other, so V5's "status never codes red against green" becomes "status never relies on red and Verdigris alone". A disabled action names its reason beside the control ("Choose a size to download"), and its accessible description repeats it.

## 5. Type, space, layout, radius, opacity, motion

**Type.** Sizes are in rem (the reader's base size, 16 px by default), so text follows browser settings. Fluid sizes run from 390 to 1440 px.

| Style | Face and weight | Size | Line height | Tracking |
|---|---|---|---|---|
| Title | Inter Tight 800 | 3.5 to 6.875 rem (56 to 110 px) | 0.95 | −0.045em |
| Section | Inter Tight 800 | 2.75 to 5 rem (44 to 80) | 1.03 | −0.04em |
| H3 | Inter Tight 800 | 1.625 to 2 rem (26 to 32) | 1.08 | −0.03em |
| H4 | Inter Tight 800 | 1.25 to 1.5 rem (20 to 24) | 1.15 | −0.02em |
| Quote | Lora Italic 400 | 1.5 to 2 rem (24 to 32) | 1.3 | −0.02em |
| Intro | Inter 400 | 1.1875 to 1.375 rem (19 to 22) | 1.5 | 0 |
| Body | Inter 400 | 1.0625 rem (17) | 1.6 | 0 |
| Small body; UI | Inter 400; 600 | 0.9375 rem (15) | 1.6; 1.4 | 0 |
| Caption | Inter 400 | 0.875 rem (14) | 1.5 | 0 |
| Label | Inter 700, capitals | 0.8125 rem (13) | 1.4 | +0.06em |
| Data label | Inter 600, tabular | 0.8125 rem (13) | 1.3 | 0 |
| Figure | Inter Tight 800, tabular | 3 to 6.5 rem (48 to 104) | 1.0 | −0.04em |

The floor is 13 px, with no screen exceptions. V5 set labels at 10 to 12 px with 9 to 13% tracking; at 13 px, 6% keeps capitals open. Print gets a point scale in Phase 4, and email keeps V5's system stack. Data styles use tabular figures and the true minus sign.

**Measure.** The `ch` unit is the width of a zero, which in Inter is 1.345 average characters. V5's 65ch intro therefore predicts 87 characters per line, inside the 84 to 93 the UX audit measured. From Inter's widths over 26,950 characters of V5 prose: body 33.88 rem (68 characters), body maximum 37.37 rem (75), intro maximum 41.91 rem (65).

**Space.** Eleven steps keep V5's 8 px rhythm, named by the multiple of 8 times 100, from `space.050` (4 px) to `space.1300` (104 px); `space.300` is 24 px. Type rhythm uses rem. Margins, gutters and borders use px, so enlarged text gains room.

**Breakpoints.** Media queries cannot read custom properties, so the build writes them in em, which also follows text size.

| Name | Width | Query | Columns | Gutter | Margin |
|---|---|---|---|---|---|
| Wide | 1440 | 90em | 12 | 24 | 64 |
| Desktop | 1024 | 64em | 12 | 24 | 40 |
| Tablet | 768 | 48em | 8 | 24 | 32 |
| Phone | 390 | base | 4 | 16 | 20 |
| Small phone, and the 320 reflow test | 360 | test width | 4 | 16 | 16 |

**Radius, border, z-index.** Radius `none` for boxes and controls, `full` (50%) for nodes and badges. Borders: hairline 1 px, rule 2 px, state bar 4 px, focus offset 2 px (V5 writes 2 px and draws 3 px, a mismatch the parity test catches). Z-index: base 0, raised 10, sticky 40, overlay 90, skip link 100.

**Opacity.** Two named decorative jobs replace the two-watermark rule. `watermarkOnLight`, Charcoal at 0.08, measures 1.17:1 on Newsprint. `watermarkOnDark`, Newsprint at 0.10, measures 1.24:1 on Charcoal and 1.28:1 on Prussian, so a watermark never carries meaning. Opacity has no other job: a label at 40% Charcoal on White falls to 2.61:1, and V5's loading lever at 20% to 1.27:1.

**Motion.** V5's values stay: 120, 200 and 320 ms with a 40 ms stagger; easings standard `(0.2, 0, 0, 1)`, enter `(0, 0, 0.2, 1)` and exit `(0.4, 0, 1, 1)`. Slide, draw and land play on request (hinge 680 ms, lever 560 ms). Under `prefers-reduced-motion: reduce`, every duration resolves to 0 ms and the final state shows at once. Nothing loops.

## 6. The rule for adding a token

**Checklist.** A token enters only when all five hold:

1. A measured need exists that no current token meets, registered with an ID and its evidence.
2. The value is one palette color mixed in OKLab toward Newsprint or Charcoal, with the amount recorded.
3. It has one named job, in one sentence.
4. It passes contrast on every surface it serves, at the threshold for its kind, and stores the ratio.
5. It is registered with a `$description` (usage notes), a tier and a status.

The tier rules, the exact locked palette and the 13 px floor apply as well. Held and rejected values stay unused.

**Test.** `token_rule_test.py` recomputes each derivation and contrast with its own copy of the formulas, so a stored number cannot go stale. On the draft it finds 110 tokens and 0 failures. Seven broken copies each fail on their own check, among them Stone as secondary text, an 11 px label and a changed Pillar Red. On my first draft it caught two real defects: missing descriptions, and an error band at 1.00:1.

## 7. Generation pipeline

1. **Source.** One DTCG file, `work/build/tokens/oa.tokens.json`, with the needs register in its root `$extensions`. The schema draft sketches it.
2. **Validate.** The rule test runs first and stops the build on failure.
3. **Build.** A zero-dependency Node script, `build-tokens.mjs`, writes `tokens.css` (`:root` properties, surface classes, the reduced-motion block, em media queries) and `tokens.json` (DTCG, aliases kept). A lint fails on any raw hex or px font size outside `tokens.css`.
4. **Parity.** Playwright at 1440 and 390 px compares with the JSON: each `:root` property, each specimen marked `data-token`, each value printed in the guide's tables, every computed color per chapter (artwork exempt), rendered contrast, and durations under reduced motion.
5. **Versions.** SemVer from 6.0.0. A rename, removal or primitive change is major, and the palette also needs Dustin's named approval. A new token or a passing value change is minor; notes are a patch. A replaced token carries `$deprecated`† for one minor release and keeps its CSS name as an alias.
6. **Change notes.** `YYYYMMDD_Token-Change-Notes.md` in the package's `tokens/` folder records version, date, token, change, reason, need and gate. The build fails if the version rises with no note.

## 8. Plan for "How to choose a token"

The page sits in the guide's foundations part, with a copy button on each token name, and its steps repeat in the AI builder brief. The order is surface, role, emphasis, state, then any component token, which wins. The reader ends by checking the ratio and the text or shape cue.

| Example | Path | Tokens | Measured | Failure shown |
|---|---|---|---|---|
| Caption under a chart | Newsprint, text, secondary | `--oa-color-text-secondary-on-newsprint`, `oa.type.caption` | 5.49 | Stone, 4.29 |
| Disabled download button | White, action, disabled | `--oa-component-button-disabled-label-on-white`, dashed edge, "Choose a size to download" | 7.74 | 40% opacity, 2.61, no reason |
| Chart highlight | Newsprint, data, emphasis | `data-emphasis` Charcoal; other bars `data-context` Stone; direct label | 13.29 and 4.29; bars differ by 3.10 | Pillar Red bar with no keyline, 2.96, beside red status |
| Warning in a Prussian tracker | Prussian, state, warning | White text, Newsprint bar and triangle, the word "Warning" | 13.28 and 9.42 | Red text, 3.19, reading as red against blue |

Each specimen appears at actual size, with its failure beside it.

## 9. Decisions for Gate 1

| # | Decision | Recommendation |
|---|---|---|
| T-1 | Format | DTCG 2025.10 in one source file; the Resolver Module (themes) waits until its page can be read |
| T-2 | Naming and tiers | Sections 1 and 2 |
| T-3 | Derivation | `color-mix` in OKLab toward Newsprint or Charcoal |
| T-4 | Deep Stone | #4E535B (18%), matching Concepts V2; the 15% option is #51565E, 5.24:1 |
| T-5 | Dim Newsprint, Error Band | Adopt both |
| T-6 | Red | No small red text or derived red; keyline rule kept |
| T-7 | Warning, success, selected | Warning without a hue; success as a Verdigris check with a word; selection by paired surface, bar and check |
| T-8 | Type and measure | 13 px floor without screen exceptions; labels 13 px at 6%; captions 14 px; measures in rem |
| T-9 | Opacity and motion | Two decorative opacity jobs; V5 timings kept; still loading state; zero durations under reduced motion |
| T-10 | Tooling and versions | Zero-dependency Node generator, Style Dictionary 5 as a cross-check if it installs, SemVer from 6.0.0 |

## Checks run

- Palette contrast on four surfaces: 21 of 21 brief cells match.
- Six derived candidates in OKLab and OKLCH on all surfaces; #4E535C traced to sRGB scaling.
- Opacity composites.
- Inter advance widths from the V5 font, checked against the audit's line lengths.
- Rule test: 0 failures; 7 of 7 broken copies caught.
- Seven web searches on DTCG status.

## Not checked

- The DTCG pages themselves, because the fetch failed: items marked †, the `.tokens.json` extension, `$root` and the Resolver Module.
- Style Dictionary or a published JSON Schema, neither installed.
- Rendered contrast and the keyline at small sizes, which wait for the Phase 2 build.
- Kerning (ignored, about 1 to 2%), color vision simulation, forced colors and print.
- Ownership of oathandaction.org, the `$extensions` namespace.

## Change log

Created: this file; `work/build/tokens/20261021_Token-Schema-Draft.json`; `work/handoffs/phase-1/20261021_Token-Contrast-Data.json`; `oa_color.py`, `tokens_phase1.py` and `token_rule_test.py` in `work/build/scripts/phase-1/`. Modified: none.
