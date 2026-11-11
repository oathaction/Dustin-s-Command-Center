# Gate 2 contrast summary

Oath & Action Edition 06, November 11, 2026. Written by the accessibility lead for Gate 2 (task 5). The full table is `20261111_Gate-2-Contrast-Table.json` beside this file; every number here comes from it.

## How it was measured

A script read `tokens.json` and `tokens.css` (token release 6.0.0-gate2.8, byte for byte the files that built the frozen page) and measured every color token against each surface or ground the token files place it on, with the WCAG 2.2 formula. Pass or fail is decided on the unrounded ratio; this page prints two decimals.

- **Surfaces.** Newsprint #DCD9D2, White #FFFFFF, Charcoal #121212 and Prussian #1F2D5A. The light theme is Newsprint and the dark theme is Charcoal; White and Prussian are surface classes that keep their surface in either theme.
- **Thresholds by role.** Text 4.5 to 1 (WCAG 1.4.3). Large text, 24 px or 18.66 px bold and up, 3 to 1 (1.4.3). Icons, needed graphics, control edges and focus rings 3 to 1 (1.4.11). The wordmark’s signature red is a logotype and has no threshold (1.4.3’s logo exception). Decoration with no meaning, and data fills whose values are printed in text, have no threshold (1.4.11 asks nothing of them).
- **Placement.** A label is measured on its fill, a bar on its band, and a ground (a field, the selected band, the Error Band) with each text token the token files name for it. Derived colors and tints are measured on each surface their own entry lists. The two watermark opacities are composited over their ground first.

## Totals

- **341 token and surface pairs** from 306 color tokens and the two watermark opacities: 245 pass, 6 pass only with the keyline the guide requires, 90 have no threshold for their role, and **0 fail**.
- **509 short names** checked in the seven theme and surface-class blocks of `tokens.css`. Each resolves to the same value as its token in `tokens.json`, and each passes on its block’s surface or ground. Roles with no token on a surface resolve to `initial`, as the token rules say.
- **269 ratios stored in `tokens.json`** recomputed: 0 differ.
- **Chapter 26’s published ratios:** 323 in the token table of Rule 26.7 and 19 in the chapter’s words and specimens recomputed: 342 of 342 match to the hundredth.
- **The Master Brief’s palette table** (section 8, item 9): 21 of 21 values match.

## Failing pairs

None. No text, icon, border, focus ring or needed graphic token falls under its threshold on any surface or ground the token files give it.

## Pairs under threshold that the guide permits

Each of these measures under 4.5 to 1 (text) or 3 to 1 (marks) and is allowed by a condition the guide states. Aliases that resolve to the same pair are grouped.

| Ratio | Color on ground | Role | The guide’s condition | Tokens |
|---|---|---|---|---|
| 2.96 | Pillar Red on Newsprint | Graphic, icon or border | Below 3 to 1 on its own; the guide requires a 1 px Charcoal keyline (13.29 to 1), which carries the boundary | action.ask.fill.onNewsprint, state.error.bar.onNewsprint, state.error.mark.onNewsprint, data.emphasisRed.onNewsprint, chart.point.onNewsprint, component.button.ask.fill.onNewsprint |
| 1.13 | #CECDC7 on Newsprint | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.diverging.fill.step3.onNewsprint, tint.stoneN90 |
| 1.16 | #CCCAC5 on Newsprint | Decoration | Decoration under 3 to 1; the guide gives it no meaning | chart.track.onNewsprint, tint.stoneN88 |
| 1.16 | #202122 on Charcoal | Decoration | Decoration under 3 to 1; the guide gives it no meaning | chart.land.onCharcoal, tint.stoneC80 |
| 1.16 | #CCCAC5 on Newsprint | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.magnitude.fill.step1.onNewsprint |
| 1.17 | #ECEAE6 on Newsprint | Decoration | Decoration under 3 to 1; the guide gives it no meaning | chart.band.onNewsprint, chart.land.onNewsprint, tint.whiteN55 |
| 1.17 | #CCC9C3 on Newsprint | Decoration | A watermark at this opacity carries no meaning (opacity has no other job) | oa.opacity.watermarkOnLight |
| 1.21 | #C1C8C0 on Newsprint | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.sequential.fill.step1.onNewsprint, tint.verdigrisN82 |
| 1.21 | #232426 on Charcoal | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.magnitude.fill.step1.onCharcoal, tint.stoneC75 |
| 1.24 | #262625 on Charcoal | Decoration | A watermark at this opacity carries no meaning (opacity has no other job) | oa.opacity.watermarkOnDark |
| 1.25 | #252729 on Charcoal | Decoration | Decoration under 3 to 1; the guide gives it no meaning | chart.band.onCharcoal, tint.stoneC72 |
| 1.27 | #202A28 on Charcoal | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.sequential.fill.step1.onCharcoal, tint.verdigrisC75 |
| 1.47 | #B4B4B3 on Newsprint | Decoration | Decoration under 3 to 1; the guide gives it no meaning | chart.gridline.onNewsprint, tint.stoneN70 |
| 1.50 | #323438 on Charcoal | Decoration | Decoration under 3 to 1; the guide gives it no meaning | chart.track.onCharcoal, tint.stoneC55 |
| 1.66 | #9AAEA6 on Newsprint | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.diverging.fill.step4.onNewsprint, tint.verdigrisN55 |
| 1.69 | #393C41 on Charcoal | Decoration | Decoration under 3 to 1; the guide gives it no meaning | chart.gridline.onCharcoal, tint.stoneC45 |
| 1.70 | #97ACA4 on Newsprint | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.sequential.fill.step2.onNewsprint, tint.verdigrisN52p75 |
| 1.78 | #2E4340 on Charcoal | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.sequential.fill.step2.onCharcoal, tint.verdigrisC50 |
| 1.80 | #3D4046 on Charcoal | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.magnitude.fill.step2.onCharcoal, tint.stoneC40 |
| 1.81 | #A1A2A3 on Newsprint | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.lightFill.onNewsprint, chart.magnitude.fill.step2.onNewsprint, tint.stoneN55 |
| 2.15 | #8E94A4 on Newsprint | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.diverging.fill.step2.onNewsprint, tint.prussianN62 |
| 2.46 | #6D9189 on Newsprint | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.sequential.fill.step3.onNewsprint, tint.verdigrisN23p5 |
| 2.89 | #3F655E on Charcoal | Data fill, values printed | A data fill under 3 to 1; the guide requires the value printed on or beside it | chart.sequential.fill.step3.onCharcoal, tint.verdigrisC20 |
| 2.96 | Pillar Red on Newsprint | Logotype (signature red) | Signature red under 3 to 1 on Newsprint; exempt as a logotype, and the guide never lets it carry information | identity.signature.onNewsprint, component.icon.accent.onNewsprint |
| 4.17 | White on Pillar Red | Large text | Below 4.5 to 1 for small text; the guide allows it only as large text, set in oa.type.ask at 19 px bold | action.ask.label.onNewsprint, action.ask.label.onWhite, action.ask.label.onCharcoal, component.button.ask.label.onNewsprint, component.button.ask.label.onWhite, component.button.ask.label.onCharcoal |

## The grid: every role on every surface

One row per token family; one column per surface. A blank cell means the family has no token on that surface (charts sit on Newsprint and Charcoal only, and red never sits on Prussian). "(keyline)" passes only with its 1 px Charcoal keyline; "(exempt)" has no threshold for its role.

| Token family | Role | Needs | Newsprint | White | Charcoal | Prussian |
|---|---|---|---|---|---|---|
| `text.primary` | Text | 4.5 to 1 | 13.29 | 18.73 | 13.29 | 13.28 |
| `text.secondary` | Text | 4.5 to 1 | 5.49 | 7.74 | 7.26 | 5.14 |
| `graphic.essential` | Graphic, icon or border | 3 to 1 | 13.29 | 18.73 | 13.29 | 9.42 |
| `graphic.subtle` | Graphic, icon or border | 3 to 1 | 4.29 | 6.05 | 7.26 | 5.14 |
| `border.strong` | Graphic, icon or border | 3 to 1 | 13.29 | 18.73 | 13.29 | 9.42 |
| `border.hairline` | Decoration | none | 4.29 (exempt) | 6.05 (exempt) | 3.10 (exempt) | 13.28 (exempt) |
| `focus.ring` | Focus ring | 3 to 1 | 3.37 | 4.74 | 13.29 | 9.42 |
| `field.ground` | Ground (band or field) | none | 1.41 (exempt) | 1.41 (exempt) | 1.00 (exempt) | 1.41 (exempt) |
| `text.primary on field.ground` | Text | 4.5 to 1 | 18.73 | 13.29 | 13.29 | 18.73 |
| `text.secondary on field.ground` | Text | 4.5 to 1 | 7.74 | 5.49 | 7.26 | 7.26 |
| `identity.signature` | Logotype (signature red) | none | 2.96 (exempt) | 4.17 (exempt) | 4.49 (exempt) | 13.28 (exempt) |
| `identity.hingeDivider` | Graphic, icon or border | 3 to 1 | 13.29 | 18.73 | 13.29 | 13.28 |
| `action.ask.fill` | Graphic, icon or border | 3 to 1 | 2.96 (keyline) | 4.17 | 4.49 | 9.42 |
| `action.ask.label` | Large text | 3 to 1 | 4.17 | 4.17 | 4.17 | 13.29 |
| `action.primary.fill` | Graphic, icon or border | 3 to 1 | 13.29 | 18.73 | 13.29 | 9.42 |
| `action.primary.fillHover` | Graphic, icon or border | 3 to 1 | 9.42 | 13.28 | 18.73 | 13.28 |
| `action.primary.label` | Text | 4.5 to 1 | 18.73 | 18.73 | 13.29 | 13.29 |
| `action.primary.label on fillHover` | Text | 4.5 to 1 | 13.28 | 13.28 | 18.73 | 18.73 |
| `state.muted.text` | Text | 4.5 to 1 | 5.49 | 7.74 | 7.26 | 5.14 |
| `state.muted.mark` | Graphic, icon or border | 3 to 1 | 4.29 | 6.05 | 7.26 | 5.14 |
| `state.disabled.text` | Text | 4.5 to 1 | 5.49 | 7.74 | 7.26 | 5.14 |
| `state.disabled.edge` | Graphic, icon or border | 3 to 1 | 5.49 | 7.74 | 7.26 | 5.14 |
| `state.loading.text` | Text | 4.5 to 1 | 5.49 | 7.74 | 7.26 | 5.14 |
| `state.loading.mark` | Graphic, icon or border | 3 to 1 | 4.29 | 6.05 | 7.26 | 5.14 |
| `state.selected.band` | Ground (band or field) | none | 1.41 (exempt) | 1.41 (exempt) | 1.41 (exempt) | 1.41 (exempt) |
| `text.primary on state.selected.band` | Text | 4.5 to 1 | 18.73 | 13.29 | 9.42 | 18.73 |
| `text.secondary on state.selected.band` | Text | 4.5 to 1 | 7.74 | 5.49 | 5.14 | 7.26 |
| `state.selected.bar on state.selected.band` | Graphic, icon or border | 3 to 1 | 18.73 | 13.29 | 9.42 | 18.73 |
| `state.warning.mark` | Graphic, icon or border | 3 to 1 | 13.29 | 18.73 | 13.29 | 9.42 |
| `state.warning.text` | Text | 4.5 to 1 | 13.29 | 18.73 | 13.29 | 13.28 |
| `state.error.band` | Ground (band or field) | none | 1.12 (exempt) | 1.58 (exempt) |  |  |
| `text.primary on state.error.band` | Text | 4.5 to 1 | 11.89 | 11.89 |  |  |
| `text.secondary on state.error.band` | Text | 4.5 to 1 | 4.91 | 4.91 |  |  |
| `state.error.bar` | Graphic, icon or border | 3 to 1 | 2.96 (keyline) | 4.17 | 4.49 | 9.42 |
| `state.error.mark` | Graphic, icon or border | 3 to 1 | 2.96 (keyline) | 4.17 | 4.49 | 9.42 |
| `state.error.text` | Text | 4.5 to 1 | 13.29 | 18.73 | 13.29 | 13.28 |
| `state.empty.text` | Text | 4.5 to 1 | 5.49 | 7.74 | 7.26 | 5.14 |
| `state.empty.edge` | Graphic, icon or border | 3 to 1 | 4.29 | 6.05 | 7.26 | 5.14 |
| `state.success.mark` | Graphic, icon or border | 3 to 1 | 3.37 | 4.74 | 3.95 | 9.42 |
| `state.success.text` | Text | 4.5 to 1 | 13.29 | 18.73 | 13.29 | 13.28 |
| `data.emphasis` | Graphic, icon or border | 3 to 1 | 13.29 | 18.73 | 13.29 | 9.42 |
| `data.context` | Graphic, icon or border | 3 to 1 | 4.29 | 6.05 | 5.41 | 5.14 |
| `data.emphasisRed` | Graphic, icon or border | 3 to 1 | 2.96 (keyline) | 4.17 | 4.49 |  |
| `chart.subject` | Graphic, icon or border | 3 to 1 | 13.29 |  | 13.29 |  |
| `chart.context` | Graphic, icon or border | 3 to 1 | 4.29 |  | 5.41 |  |
| `chart.label` | Text | 4.5 to 1 | 13.29 |  | 13.29 |  |
| `chart.secondary` | Text | 4.5 to 1 | 5.49 |  | 7.26 |  |
| `chart.baseline` | Graphic, icon or border | 3 to 1 | 13.29 |  | 13.29 |  |
| `chart.leader` | Graphic, icon or border | 3 to 1 | 4.29 |  | 5.41 |  |
| `chart.point` | Graphic, icon or border | 3 to 1 | 2.96 (keyline) |  | 4.49 |  |
| `chart.pointKeyline` | Graphic, icon or border | 3 to 1 | 13.29 |  |  |  |
| `chart.party.mark` | Graphic, icon or border | 3 to 1 | 13.29 |  | 13.29 |  |
| `chart.labelOnSubject` | Text | 4.5 to 1 | 18.73 |  | 13.29 |  |
| `chart.chip.fill` | Graphic, icon or border | 3 to 1 | 13.29 |  | 13.29 |  |
| `chart.chip.label` | Text | 4.5 to 1 | 13.29 |  | 13.29 |  |
| `chart.lightFill` | Data fill, values printed | none | 1.81 (exempt) |  | 3.10 (exempt) |  |
| `chart.track` | Decoration | none | 1.16 (exempt) |  | 1.50 (exempt) |  |
| `chart.gridline` | Decoration | none | 1.47 (exempt) |  | 1.69 (exempt) |  |
| `chart.band` | Decoration | none | 1.17 (exempt) |  | 1.25 (exempt) |  |
| `chart.land` | Decoration | none | 1.17 (exempt) |  | 1.16 (exempt) |  |
| `chart.diverging.fill.step1` | Data fill, values printed | none | 9.42 (exempt) |  |  |  |
| `chart.diverging.fill.step2` | Data fill, values printed | none | 2.15 (exempt) |  |  |  |
| `chart.diverging.fill.step3` | Data fill, values printed | none | 1.13 (exempt) |  |  |  |
| `chart.diverging.fill.step4` | Data fill, values printed | none | 1.66 (exempt) |  |  |  |
| `chart.diverging.fill.step5` | Data fill, values printed | none | 5.01 (exempt) |  |  |  |
| `chart.diverging.label.step1` | Text | 4.5 to 1 | 13.28 |  |  |  |
| `chart.diverging.label.step2` | Text | 4.5 to 1 | 6.18 |  |  |  |
| `chart.diverging.label.step3` | Text | 4.5 to 1 | 11.76 |  |  |  |
| `chart.diverging.label.step4` | Text | 4.5 to 1 | 8.01 |  |  |  |
| `chart.diverging.label.step5` | Text | 4.5 to 1 | 7.06 |  |  |  |
| `chart.sequential.fill.step1` | Data fill, values printed | none | 1.21 (exempt) |  | 1.27 (exempt) |  |
| `chart.sequential.fill.step2` | Data fill, values printed | none | 1.70 (exempt) |  | 1.78 (exempt) |  |
| `chart.sequential.fill.step3` | Data fill, values printed | none | 2.46 (exempt) |  | 2.89 (exempt) |  |
| `chart.sequential.fill.step4` | Data fill, values printed | none | 3.69 (exempt) |  | 5.55 (exempt) |  |
| `chart.sequential.fill.step5` | Data fill, values printed | none | 5.87 (exempt) |  | 8.01 (exempt) |  |
| `chart.sequential.label.step1` | Text | 4.5 to 1 | 10.96 |  | 10.47 |  |
| `chart.sequential.label.step2` | Text | 4.5 to 1 | 7.81 |  | 7.48 |  |
| `chart.sequential.label.step3` | Text | 4.5 to 1 | 5.41 |  | 4.61 |  |
| `chart.sequential.label.step4` | Text | 4.5 to 1 | 5.20 |  | 5.55 |  |
| `chart.sequential.label.step5` | Text | 4.5 to 1 | 8.27 |  | 8.01 |  |
| `chart.sequential.outline` | Graphic, icon or border | 3 to 1 | 5.87 |  | 8.01 |  |
| `chart.sequential.outline on land` | Graphic, icon or border | 3 to 1 | 6.89 |  | 6.90 |  |
| `chart.magnitude.fill.step1` | Data fill, values printed | none | 1.16 (exempt) |  | 1.21 (exempt) |  |
| `chart.magnitude.fill.step2` | Data fill, values printed | none | 1.81 (exempt) |  | 1.80 (exempt) |  |
| `chart.magnitude.fill.step3` | Data fill, values printed | none | 4.92 (exempt) |  | 7.33 (exempt) |  |
| `chart.magnitude.fill.step4` | Data fill, values printed | none | 9.38 (exempt) |  | 10.98 (exempt) |  |
| `chart.magnitude.label.step1` | Text | 4.5 to 1 | 11.44 |  | 11.02 |  |
| `chart.magnitude.label.step2` | Text | 4.5 to 1 | 7.33 |  | 7.37 |  |
| `chart.magnitude.label.step3` | Text | 4.5 to 1 | 4.92 |  | 7.33 |  |
| `chart.magnitude.label.step4` | Text | 4.5 to 1 | 9.38 |  | 10.98 |  |
| `component.button.ask.fill` | Graphic, icon or border | 3 to 1 | 2.96 (keyline) | 4.17 | 4.49 | 9.42 |
| `component.button.ask.label` | Large text | 3 to 1 | 4.17 | 4.17 | 4.17 | 13.29 |
| `component.button.ask.keyline` | Graphic, icon or border | 3 to 1 | 13.29 |  |  |  |
| `component.button.primary.fill` | Graphic, icon or border | 3 to 1 | 13.29 | 18.73 | 13.29 | 9.42 |
| `component.button.primary.fillHover` | Graphic, icon or border | 3 to 1 | 9.42 | 13.28 | 18.73 | 13.28 |
| `component.button.primary.label` | Text | 4.5 to 1 | 18.73 | 18.73 | 13.29 | 13.29 |
| `component.button.primary.label on fillHover` | Text | 4.5 to 1 | 13.28 | 13.28 | 18.73 | 18.73 |
| `component.button.disabled.label` | Text | 4.5 to 1 | 5.49 | 7.74 | 7.26 | 5.14 |
| `component.button.disabled.edge` | Graphic, icon or border | 3 to 1 | 5.49 | 7.74 | 7.26 | 5.14 |
| `component.icon.ink` | Graphic, icon or border | 3 to 1 | 13.29 | 18.73 | 13.29 | 9.42 |
| `component.icon.accent` | Logotype (signature red) | none | 2.96 (exempt) | 4.17 (exempt) | 4.49 (exempt) | 13.28 (exempt) |
| `component.appIcon.tile` | Tile ground | none |  |  | 1.00 (exempt) |  |
| `component.appIcon.mark` | Graphic, icon or border | 3 to 1 |  |  | 13.29 |  |
| `component.appIcon.accent` | Logotype (signature red) | none |  |  | 4.49 (exempt) |  |
| `component.avatar.tile` | Tile ground | none |  |  | 1.00 (exempt) |  |
| `component.avatar.mark` | Graphic, icon or border | 3 to 1 |  |  | 13.29 |  |
| `component.avatar.accent` | Logotype (signature red) | none |  |  | 4.49 (exempt) |  |

## The palette on every surface, for reference

A palette color gets its job from a role token, so this matrix shows each color’s reach: text means 4.5 to 1 or more; large means large text and needed graphics only (3 to 4.49); neither means under 3 to 1.

| Color | Newsprint | White | Charcoal | Prussian |
|---|---|---|---|---|
| Newsprint #DCD9D2 | 1.00 neither | 1.41 neither | 13.29 text | 9.42 text |
| Charcoal #121212 | 13.29 text | 18.73 text | 1.00 neither | 1.41 neither |
| Pillar Red #E63946 | 2.96 neither | 4.17 large | 4.49 large | 3.19 large |
| Prussian #1F2D5A | 9.42 text | 13.28 text | 1.41 neither | 1.00 neither |
| Stone #5D636D | 4.29 large | 6.05 text | 3.10 large | 2.20 neither |
| Verdigris #4A7C74 | 3.37 large | 4.74 text | 3.95 large | 2.80 neither |
| White #FFFFFF | 1.41 neither | 1.00 neither | 18.73 text | 13.28 text |
| Deep Stone #4E535B | 5.49 text | 7.74 text | 2.42 neither | 1.72 neither |
| Dim Newsprint #A3A19C | 1.83 neither | 2.58 neither | 7.26 text | 5.14 text |
| Error Band #E1C9C1 | 1.12 neither | 1.58 neither | 11.89 text | 8.43 text |

## Chapter 26’s published ratios against ours

All 323 ratios in the token table (Rule 26.7) were parsed from the frozen page and recomputed from the token values; the JSON lists each. The 19 ratios the chapter states in its words and specimens were matched by hand to the two colors each sentence names:

| Published, quoted from the page | Colors | Published | Ours | Result |
|---|---|---|---|---|
| “Dim Newsprint on Charcoal, 7.26 to 1” | dimNewsprint on charcoal | 7.26 | 7.26 | match |
| “The label it draws, 5.49 to 1 on Newsprint” | deepStone on newsprint | 5.49 | 5.49 | match |
| “in the dark theme it stays Deep Stone on Charcoal and measures 2.42 to 1” | deepStone on charcoal | 2.42 | 2.42 | match |
| “Stone measures 4.29 to 1 for small secondary text on Newsprint” | stone on newsprint | 4.29 | 4.29 | match |
| “A red of its own, 1.09 to 1 from Pillar Red” | #DA3843 on pillarRed | 1.09 | 1.09 | match |
| “3.22 to 1 on Newsprint, over the 3 to 1 a mark needs” | #DA3843 on newsprint | 3.22 | 3.22 | match |
| “A caption set with it: 1.72 to 1 on Prussian” | deepStone on prussian | 1.72 | 1.72 | match |
| “Label and dashed edge: Deep Stone, 7.74 to 1 on White” | deepStone on white | 7.74 | 7.74 | match |
| “The whole button at 40 percent opacity: its fill measures 2.61 to 1 on White” | charcoal@0.4/white on white | 2.61 | 2.61 | match |
| “Week 3 in Charcoal, 13.29 to 1” | charcoal on newsprint | 13.29 | 13.29 | match |
| “the two inks differ by 3.10 to 1” | charcoal on stone | 3.10 | 3.10 | match |
| “Week 3 in Pillar Red with no keyline, 2.96 to 1 on Newsprint” | pillarRed on newsprint | 2.96 | 2.96 | match |
| “Words in White, 13.28 to 1” | white on prussian | 13.28 | 13.28 | match |
| “the bar and triangle in Newsprint, 9.42 to 1” | newsprint on prussian | 9.42 | 9.42 | match |
| “Words in Pillar Red on Prussian, 3.19 to 1, with no word and no mark” | pillarRed on prussian | 3.19 | 3.19 | match |
| “In the dark theme the card takes Charcoal, and its words stay Charcoal: 1.00 to 1” | charcoal on charcoal | 1.00 | 1.00 | match |
| “an error's red bar sits on Charcoal at 4.49 to 1” | pillarRed on charcoal | 4.49 | 4.49 | match |
| “Contrast where it serves 5.49 to 1 on Newsprint and 7.74 on White (the second figure)” | deepStone on white | 7.74 | 7.74 | match |
| “Caption: Stone, 4.29 to 1 on Newsprint” | stone on newsprint | 4.29 | 4.29 | match |

A sample of the token table’s rows, one per family:

| Token | Published | Ours | Result |
|---|---|---|---|
| `oa.color.derived.deepStone` | 5.49:1 on Newsprint | 5.49 | match |
| `oa.color.derived.dimNewsprint` | 7.26:1 on Charcoal | 7.26 | match |
| `oa.color.derived.errorBand` | charcoal 11.89:1 | 11.89 | match |
| `oa.color.tint.stoneN55` | 1.81:1 on Newsprint | 1.81 | match |
| `oa.color.tint.stoneN70` | 1.47:1 on Newsprint | 1.47 | match |
| `oa.color.tint.stoneN88` | 1.16:1 on Newsprint | 1.16 | match |
| `oa.color.tint.stoneN90` | 1.13:1 on Newsprint | 1.13 | match |
| `oa.color.tint.stoneN35` | 5.41:1 on Charcoal | 5.41 | match |
| `oa.color.tint.stoneN85` | 10.98:1 on Charcoal | 10.98 | match |
| `oa.color.tint.stoneC10` | 4.92:1 on Newsprint | 4.92 | match |
| `oa.color.tint.stoneC40` | 1.8:1 on Charcoal | 1.80 | match |
| `oa.color.tint.stoneC45` | 1.69:1 on Charcoal | 1.69 | match |
| `oa.color.tint.stoneC55` | 1.5:1 on Charcoal | 1.50 | match |
| `oa.color.tint.stoneC60` | 9.38:1 on Newsprint | 9.38 | match |
| `oa.color.tint.stoneC72` | 1.25:1 on Charcoal | 1.25 | match |
| `oa.color.tint.stoneC75` | 1.21:1 on Charcoal | 1.21 | match |
| `oa.color.tint.stoneC80` | 1.16:1 on Charcoal | 1.16 | match |
| `oa.color.tint.whiteN55` | 1.17:1 on Newsprint | 1.17 | match |
| `oa.color.tint.prussianN62` | 2.15:1 on Newsprint | 2.15 | match |
| `oa.color.tint.verdigrisN55` | 1.66:1 on Newsprint | 1.66 | match |
| `oa.color.tint.verdigrisC25` | 5.01:1 on Newsprint | 5.01 | match |
| `oa.color.tint.verdigrisN82` | 1.21:1 on Newsprint | 1.21 | match |
| `oa.color.tint.verdigrisN52p75` | 1.7:1 on Newsprint | 1.70 | match |
| `oa.color.tint.verdigrisN23p5` | 2.46:1 on Newsprint | 2.46 | match |

## Marks inside a surface’s own grounds

The token files name the text that sits on each ground, and nothing else. A product can still place a mark inside a ground: a check in a selected row, a red bar on an Error Band. These are measured as risks to state in the guide, not as failing token pairs.

| Mark | On | Ratio | Needs | Note |
|---|---|---|---|---|
| `action.ask.fill.onNewsprint` (Pillar Red) | state.error.band.onNewsprint (Error Band) | 2.64 | 3.0 | Under 3 to 1 against this ground |
| `state.error.bar.onNewsprint` (Pillar Red) | state.error.band.onNewsprint (Error Band) | 2.64 | 3.0 | Under 3 to 1 against this ground |
| `data.emphasisRed.onNewsprint` (Pillar Red) | state.error.band.onNewsprint (Error Band) | 2.64 | 3.0 | Under 3 to 1 against this ground |
| `action.ask.fill.onWhite` (Pillar Red) | field.ground.onWhite (Newsprint) | 2.96 | 3.0 | Under 3 to 1 against this ground |
| `state.error.bar.onWhite` (Pillar Red) | field.ground.onWhite (Newsprint) | 2.96 | 3.0 | Under 3 to 1 against this ground |
| `data.emphasisRed.onWhite` (Pillar Red) | field.ground.onWhite (Newsprint) | 2.96 | 3.0 | Under 3 to 1 against this ground |
| `action.ask.fill.onWhite` (Pillar Red) | state.selected.band.onWhite (Newsprint) | 2.96 | 3.0 | Under 3 to 1 against this ground |
| `state.error.bar.onWhite` (Pillar Red) | state.selected.band.onWhite (Newsprint) | 2.96 | 3.0 | Under 3 to 1 against this ground |
| `data.emphasisRed.onWhite` (Pillar Red) | state.selected.band.onWhite (Newsprint) | 2.96 | 3.0 | Under 3 to 1 against this ground |
| `action.ask.fill.onWhite` (Pillar Red) | state.error.band.onWhite (Error Band) | 2.64 | 3.0 | Under 3 to 1 against this ground |
| `state.error.bar.onWhite` (Pillar Red) | state.error.band.onWhite (Error Band) | 2.64 | 3.0 | Under 3 to 1 against this ground |
| `data.emphasisRed.onWhite` (Pillar Red) | state.error.band.onWhite (Error Band) | 2.64 | 3.0 | Under 3 to 1 against this ground |
| `identity.signature.onCharcoal` (Pillar Red) | state.selected.band.onCharcoal (Prussian) | 3.19 | none | Red on Prussian breaks Rule 05.3 whatever the ratio |
| `action.ask.fill.onCharcoal` (Pillar Red) | state.selected.band.onCharcoal (Prussian) | 3.19 | 3.0 | Red on Prussian breaks Rule 05.3 whatever the ratio |
| `state.error.bar.onCharcoal` (Pillar Red) | state.selected.band.onCharcoal (Prussian) | 3.19 | 3.0 | Red on Prussian breaks Rule 05.3 whatever the ratio |
| `state.success.mark.onCharcoal` (Verdigris) | state.selected.band.onCharcoal (Prussian) | 2.80 | 3.0 | Under 3 to 1 against this ground |
| `data.emphasisRed.onCharcoal` (Pillar Red) | state.selected.band.onCharcoal (Prussian) | 3.19 | 3.0 | Red on Prussian breaks Rule 05.3 whatever the ratio |

## What this does not cover

- Colors written into specimens and drawings as raw values outside the token files. The guide check’s rendered scans cover those; this table covers the tokens.
- Text over images or photographs.
- Contrast as a reader’s own screen, a contrast theme or print shows it. The ratios are computed from sRGB values.
