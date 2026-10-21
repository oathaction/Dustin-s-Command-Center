# Token architecture

Oath & Action Brand Guide, Edition 06. Phase 1 proposal for Gate 1, October 21, 2026, by oa-engineer, revised after the Phase 1 reviews. Nothing ships before Dustin decides section 9.

A token is a named design value that the guide, the asset package and builders all read from one file. Figures come from `work/build/scripts/phase-1/tokens_phase1.py`.

## 1. Format, categories and naming

**Format.** The JSON follows the Design Tokens Community Group (DTCG) Format Module 2025.10. Search results from w3.org and designtokens.org call it the first stable version, a Final Community Group Report of October 28, 2025, outside the W3C Standards track. No later edition turned up. The page itself would not load, so items marked † rest on my knowledge of the drafts.

Format rules that shape the design:

- Names may not contain `{`, `}` or `.`, or start with `$`. An alias (a token pointing to another) is written `{oa.color.palette.charcoal}`.
- Colors carry `colorSpace`, `components`, `alpha` and `hex`.
- Dimensions take `px` or `rem`†, with no `em`, `ch`, `%` or `vw`. So em tracking, `clamp()` sizes and percentage radii live in `$extensions`, and the generator writes their CSS.

**Categories.** The groups are `oa.color`, `oa.font` with `oa.type`, `oa.space`, `oa.size`, `oa.border`, `oa.radius`, `oa.opacity`, `oa.layout`, `oa.motion`, `oa.zIndex`, `oa.chart` and `oa.component`. They cover Master Brief V2 section 10.

**Naming.** JSON segments use camelCase; CSS adds `--oa-` and kebab case, surface last: `oa.color.text.secondary.onNewsprint` becomes `--oa-color-text-secondary-on-newsprint`. Generated surface classes, such as `.oa-surface-prussian`, point short names like `--oa-color-text-secondary` at that surface's tokens. JSON holds only explicit tokens, so each can be tested.

## 2. Tiers

| Tier | Holds | May point to | Example |
|---|---|---|---|
| Primitive | Locked colors, derived colors, scales | Nothing | `oa.color.derived.deepStone` = #4E535B |
| Semantic | A role on a surface | Primitives | `oa.color.text.secondary.onNewsprint` |
| Component | One part of one component | Semantic tokens | `oa.component.button.ask.fill.onNewsprint` |

Identity marks use palette primitives, never tints. Red follows the creative director's red rule (review section 2): signature red in the wordmark and lever does not count, and each view spends one working red, on an error first, then the ask, then the headline's point. Data reaches red only through a future `data.emphasisRed` at that third rank. Series palettes go to Gate 2.

## 3. Roles per surface

WCAG thresholds: 4.5:1 for text; 3:1 for large text (24 px, or 18.66 px bold), needed graphics and focus rings.

| Role | Newsprint | White | Charcoal | Prussian |
|---|---|---|---|---|
| Text, primary | Charcoal 13.29 | Charcoal 18.73 | Newsprint 13.29 | White 13.28 |
| Text, secondary | Deep Stone 5.49 | Deep Stone 7.74 | Dim Newsprint 7.26 | Dim Newsprint 5.14 |
| Identity marks (signature red) | Pillar Red 2.96, logotype | Pillar Red 4.17 | Pillar Red 4.49 | White 13.28 |
| Working red (one per view) | Pillar Red 2.96; 1 px Charcoal keyline 13.29 | Pillar Red 4.17 | Pillar Red 4.49 | None: red never sits on Prussian |
| Graphic, essential; data emphasis | Charcoal 13.29 | Charcoal 18.73 | Newsprint 13.29 | Newsprint 9.42 |
| Graphic, subtle; data context | Stone 4.29 | Stone 6.05 | Dim Newsprint 7.26 | Dim Newsprint 5.14 |
| Border, strong (inputs) | Charcoal 13.29 | Charcoal 18.73 | Newsprint 13.29 | Newsprint 9.42 |
| Border, hairline (decorative) | Stone 4.29 | Stone 6.05 | Stone 3.10 | White 13.28 |
| Focus ring | Verdigris 3.37 | Verdigris 4.74 | Newsprint 13.29 | Newsprint 9.42 |

The hinge divider's ampersand is Charcoal (Newsprint on dark surfaces, my reading). Stone and Verdigris on Newsprint, and Pillar Red on White and Charcoal, pass for large text only.

**Derived values.** Three derived values fill gaps that no palette color serves:

| Name | Hex | Method | One job | Measured |
|---|---|---|---|---|
| Deep Stone | #4E535B | Stone 18% toward Charcoal | Secondary and disabled text on Newsprint and White | 5.49 Newsprint, 7.74 White |
| Dim Newsprint | #A3A19C | Newsprint 25% toward Charcoal | Secondary and disabled text on Charcoal and Prussian | 7.26 Charcoal, 5.14 Prussian |
| Error Band | #E1C9C1 | Pillar Red 88% toward Newsprint | Error message ground on light surfaces | Charcoal text 11.89, Deep Stone 4.91 |

Registered needs: N-01, 49 Stone-on-Newsprint text failures in the V5 census; N-02, 8 Stone failures on dark surfaces; N-03, a red-family ground for small text (Charcoal on Pillar Red is 4.49).

**The Concepts V2 Stone.** #4E535C (5.49 on Newsprint, 2.42 on Charcoal) is exactly Stone scaled to 84% in sRGB, a mix toward black, outside the palette. Deep Stone lies 0.0017 away in OKLab, so its 1,606 uses can move to the token with no visible change.

**Mixing method.** OKLab is a color space where equal numeric steps look equal; OKLCH is the same space as lightness, chroma and hue. Toward Charcoal, which has no chroma, they agree. Toward Newsprint, OKLCH swings the hue: the Error Band would become #DBCDB6, a beige 58 degrees from red. I propose `color-mix(in oklab, …)`.

**Held:** a Verdigris for status on Prussian (#59857D, 3.21), pending the Phase 2 Signal Grid. **Rejected:** a small-text red (#AC3339, 4.53 on Newsprint), 0.033 from Atlas V7's #BD2C32, which DC-03 retired; and a darker red for marks (#DA3843, 3.22), a second red that looks like the first.

## 4. State tokens and the ask button

Every state changes text or shape as well as color. No state uses opacity.

| State | Color | Text or shape change |
|---|---|---|
| Muted | Secondary text; Stone or Dim Newsprint marks | Regular weight; marks drawn as outlines |
| Disabled | Secondary text, dashed edge | `aria-disabled="true"` keeps focus; a reason line says what will make it available |
| Hover | Button fill steps from Charcoal to Prussian | Label underlines; link underline grows from 1 to 2 px |
| Focus | Focus ring per surface | 2 px outline, 2 px offset, shown at once |
| Loading | Secondary text; still Stone outline lever | Visible text ("Loading tracker") in a `role="status"` region; no motion |
| Selected | Paired surface: Newsprint with White, Charcoal with Prussian | 4 px bar, check glyph, `aria-selected` or `aria-pressed` |
| Warning | Primary text; no hue of its own | Triangle glyph, the word "Warning", 4 px bar |
| Error | Working red mark (keyline on Newsprint, Newsprint on Prussian); Error Band on light surfaces | Circle-cross glyph, the word "Error", the fix in plain words |
| Empty | Secondary text; dashed Stone region | What is missing and what to do next |
| Success | Verdigris mark; Newsprint on Prussian | Check glyph and a word such as "Saved" |

Paired surfaces differ by 1.41:1, so the bar and glyph carry the selection. Pillar Red and Verdigris measure 1.14:1, so V5's "status never codes red against green" becomes "status never relies on red and Verdigris alone". A disabled action names its reason beside the control ("Choose a size to download") and in its accessible description.

**Ask button.** The ask is the step a reader can take now, second in the red rule after an error.

| Surface | Fill | Label, Inter 700 at 19 px | Edge |
|---|---|---|---|
| Newsprint | Pillar Red 2.96 | White 4.17 | 1 px Charcoal keyline 13.29 |
| White | Pillar Red 4.17 | White 4.17 | None needed |
| Charcoal | Pillar Red 4.49 | White 4.17 | None needed |
| Prussian | Newsprint 9.42 | Charcoal 13.29 | Red never sits on Prussian |

White on Pillar Red passes only as large text, so `oa.type.ask` stays at 19 px bold or above, which the test checks. When an error holds the view's red, the ask takes the primary button (Charcoal fill, White label, 18.73), and a view with a red ask keeps chart emphasis in Charcoal. Hover underlines the label. A disabled ask takes the disabled pattern, without red.

## 5. Type, space, layout, radius, opacity, motion

**Type.** Sizes are in rem (the reader's base size, 16 px by default), so text follows browser settings; fluid sizes run from 390 to 1440 px.

| Style | Face and weight | Size (rem) | Line height | Tracking |
|---|---|---|---|---|
| Title | Inter Tight 800 | 3.5 to 6.875 | 0.95 | −0.045em |
| Section | Inter Tight 800 | 2.75 to 5 | 1.03 | −0.04em |
| H3 | Inter Tight 800 | 1.625 to 2 | 1.08 | −0.03em |
| H4 | Inter Tight 800 | 1.25 to 1.5 | 1.15 | −0.02em |
| Quote | Lora Italic 400 | 1.5 to 2 | 1.3 | −0.02em |
| Intro | Inter 400 | 1.1875 to 1.375 | 1.5 | 0 |
| Ask | Inter 700 | 1.1875 | 1.2 | 0 |
| Body | Inter 400 | 1.0625 | 1.6 | 0 |
| Small body; UI | Inter 400; 600 | 0.9375 | 1.6; 1.4 | 0 |
| Caption | Inter 400 | 0.875 | 1.5 | 0 |
| Label | Inter 700, capitals | 0.8125 | 1.4 | +0.06em |
| Data label | Inter 600, tabular | 0.8125 | 1.3 | 0 |
| Figure | Inter Tight 800, tabular | 3 to 6.5 | 1.0 | −0.04em |

The floor is 13 px (0.8125 rem), with no screen exceptions. V5 set labels at 10 to 12 px with 9 to 13% tracking; at 13 px, 6% keeps capitals open. Print gets a point scale in Phase 4, and email keeps V5's system stack. Data styles use tabular figures and the true minus sign.

**Measure.** The `ch` unit is the width of a zero, which in Inter is 1.345 average characters, so V5's 65ch intro predicts 87 characters per line; the UX audit measured 84 to 93. Measured over 26,950 characters of V5 prose: body 33.88 rem (68 characters), at most 37.37 rem (75); intro at most 41.91 rem (65).

**Space.** Eleven steps keep V5's 8 px rhythm, named by the multiple of 8 times 100, from `space.050` (4 px) to `space.1300` (104 px). Type rhythm uses rem; margins, gutters and borders use px, so enlarged text gains room.

**Breakpoints.** Media queries cannot read custom properties, so the build writes them in em, which follows text size.

| Name | Width | Query | Columns | Gutter | Margin |
|---|---|---|---|---|---|
| Wide | 1440 | 90em | 12 | 24 | 64 |
| Desktop | 1024 | 64em | 12 | 24 | 40 |
| Tablet | 768 | 48em | 8 | 24 | 32 |
| Phone | 390 | base | 4 | 16 | 20 |
| Small phone (also 320 reflow) | 360 | test width | 4 | 16 | 16 |

**Radius, border, z-index.** Radius `none` for boxes and controls, `full` for nodes and badges. Borders 1, 2 and 4 px; focus offset 2 px (V5 writes 2 and draws 3, a mismatch the parity test catches). Z-index 0, 10, 40 (sticky), 90 (overlay), 100 (skip link).

**Opacity.** Two decorative jobs replace the two-watermark rule: `watermarkOnLight` (Charcoal at 0.08, 1.17:1 on Newsprint) and `watermarkOnDark` (Newsprint at 0.10, 1.24:1 on Charcoal). At those ratios a watermark never carries meaning. Opacity has no other job: a 40% Charcoal label on White measures 2.61:1, and V5's 20% loading lever 1.27:1.

**Motion.** V5's values stay: 120, 200 and 320 ms with a 40 ms stagger; easings standard `(0.2, 0, 0, 1)`, enter `(0, 0, 0.2, 1)` and exit `(0.4, 0, 1, 1)`. Slide, draw and land play on request (hinge 680 ms, lever 560 ms). Under `prefers-reduced-motion: reduce`, durations resolve to 0 ms and the final state shows at once. Nothing loops.

## 6. The rule for adding a token

**Checklist.** A token enters only when all five hold:

1. A measured need exists that no current token meets, registered with an ID and its evidence.
2. The value is one palette color mixed in OKLab toward Newsprint or Charcoal, with the amount recorded.
3. It has one named job, in one sentence.
4. It passes contrast on every surface it serves, at the threshold for its kind, and stores the ratio.
5. It is registered with a `$description` (usage notes), a tier and a status.

The tier rules, the exact locked palette, the red rule and the 13 px floor apply as well. Held and rejected values stay unused.

**Test.** `token_rule_test.py` recomputes every derivation and contrast with its own formulas, so stored numbers cannot go stale. The draft passes: 157 tokens, 0 failures. Eleven broken copies each fail on their own check, among them an 11 px label, a red ask on Prussian and a 15 px ask label.

## 7. Generation pipeline

1. **Source.** One DTCG file, `work/build/tokens/oa.tokens.json`, with the needs register and red rule in its root `$extensions`, as the schema draft sketches.
2. **Validate.** The rule test runs first and stops the build on failure.
3. **Build.** A zero-dependency Node script, `build-tokens.mjs`, writes `tokens.css` (properties, surface classes, reduced-motion block, em media queries) and `tokens.json` (DTCG, aliases kept). A lint fails on raw hex or px font sizes outside `tokens.css`.
4. **Parity.** Playwright at 1440 and 390 px checks `:root` properties, specimens marked `data-token`, values printed in the guide's tables, every computed color (artwork exempt), rendered contrast and reduced-motion durations against the JSON.
5. **Versions.** SemVer from 6.0.0. A rename, removal or primitive change is major, and the palette needs Dustin's named approval. A new token or a passing value change is minor; notes are a patch. A replaced token carries `$deprecated`† for one minor release, with its old CSS name kept as an alias.
6. **Change notes.** `YYYYMMDD_Token-Change-Notes.md` in the package's `tokens/` folder logs version, date, token, change, reason, need and gate. A version rise with no note fails the build.

## 8. Plan for "How to choose a token"

The page is chapter 26, in Production, as the architecture map places it (C9). Token names have copy buttons, and the steps repeat in the AI builder brief: surface, role, emphasis, state, then any component token, which wins. Each example shows the specimen at actual size beside its failure.

| Example | Path | Tokens | Measured | Failure shown |
|---|---|---|---|---|
| Caption under a chart | Newsprint, text, secondary | `--oa-color-text-secondary-on-newsprint`, `oa.type.caption` | 5.49 | Stone, 4.29 |
| Disabled download button | White, action, disabled | `--oa-component-button-disabled-label-on-white`, dashed edge, "Choose a size to download" | 7.74 | 40% opacity, 2.61, no reason |
| Chart highlight | Newsprint, data, emphasis | `data-emphasis` Charcoal; other bars `data-context` Stone; direct label | 13.29 and 4.29; bars differ by 3.10 | Pillar Red bar, no keyline, 2.96, beside an error's red |
| Warning in a Prussian tracker | Prussian, state, warning | White text, Newsprint bar and triangle, the word "Warning" | 13.28 and 9.42 | Red text on Prussian, 3.19 |

## 9. Decisions for Gate 1

| # | Decision | Options | Recommendation |
|---|---|---|---|
| T-1 | Format | DTCG 2025.10; a house format | DTCG 2025.10; the Resolver Module (themes) once its page is read |
| T-2 | Naming and tiers | Sections 1 and 2; flat names | Sections 1 and 2 |
| T-3 | Derivation | OKLab; OKLCH | OKLab |
| T-4 | Deep Stone | 18%, #4E535B, 5.49; 15%, #51565E, 5.24 | 18%, matching Concepts V2 |
| T-5 | Dim Newsprint, Error Band | Adopt; hold | Adopt both |
| T-6 | Red | The red rule with keylines; a derived red | The red rule; no small red text; no derived red |
| T-7 | Ask button | White label (4.17); Charcoal label (4.49) | White label at 19 px bold, as V5 sets it |
| T-8 | Warning, success, selected | As in section 4; tinted selection | As in section 4 |
| T-9 | Type and measure | No screen exceptions; documented exceptions | No exceptions; labels 13 px at 6%; measures in rem |
| T-10 | Opacity and motion | Two decorative jobs; V5's rule | Two jobs; V5 timings; still loading state |
| T-11 | Tooling and versions | Node generator; Style Dictionary 5 | Node, with Style Dictionary as a cross-check; SemVer from 6.0.0 |

## Checks run

- Palette contrast: 21 of 21 cells of the brief's table (section 8, item 9) match.
- Six derived candidates in OKLab and OKLCH; #4E535C traced to sRGB scaling; opacity composites.
- Inter advance widths from the V5 font, checked against the audit's line lengths.
- Rule test: 157 tokens, 0 failures; 11 of 11 broken copies caught.
- Seven web searches on DTCG status.

## Not checked

- The DTCG pages themselves, because the fetch failed: items marked †, the `.tokens.json` extension, `$root` and the Resolver Module.
- Style Dictionary or a published JSON Schema, neither installed.
- Rendered contrast and small keylines, which wait for the Phase 2 build.
- Kerning (about 1 to 2%), color vision simulation, forced colors and print.
- Ownership of oathandaction.org, the `$extensions` namespace.

## Change log

Created this phase and revised after the reviews: this file; `work/build/tokens/20261021_Token-Schema-Draft.json`; `work/handoffs/phase-1/20261021_Token-Contrast-Data.json`; `oa_color.py`, `tokens_phase1.py` and `token_rule_test.py` in `work/build/scripts/phase-1/`. Modified outside these: none.
