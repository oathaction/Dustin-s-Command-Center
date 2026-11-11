Release landed, 06:24 UTC, November 11, 2026: tokens 6.0.0-gate2.8.

# Stage C round 2, the fix pass: the guide engineer's notes

Oath & Action Edition 06, Phase 2, stage C round 2, November 11, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261111_Stage-C-Round-2-Fix-Brief.md`. I own the tokens, the shell, `guide_build.py`, `guide_check.js` and chapter 26. The token release came first; the other items follow.

This file is written early and grows as the work lands.

## Status

| Item | What | Status |
|---|---|---|
| Release | 6.0.0-gate2.8: DR-218 and call 1's field ground, one change note (BE-S7's words) | done, 06:24 UTC |

## 1. The token release, 6.0.0-gate2.8

One release, one change note, as call 1 and DR-218 ask. Made in the source, `work/build/tokens/src/oa-tokens.src.mjs`, and written by `tokens_build.mjs`; the token table and chapter 26 regenerated from it.

- **Field ground on Charcoal (call 1, D2-1544, CD-M2, BE-M1).** `oa.color.field.ground.onCharcoal` now points at Charcoal, where it pointed at Prussian. A field in the dark theme shows by its strong Newsprint edge (13.29 to 1 on the surface and on the field), and an error's 4 px Pillar Red bar sits on Charcoal at 4.49 to 1. No value is new. The field ground on Prussian stays Charcoal; the selected band on Charcoal stays Prussian. The description says all of this in reader words.
- **The error bar's name (DR-218).** `oa.color.state.error.mark` becomes `oa.color.state.error.bar` on all four surfaces, so `--oa-color-state-error-bar` and its short name. The old names stay as deprecated aliases: each old token points at its new one, carries DTCG's `$deprecated` ("Renamed oa.color.state.error.bar.onNewsprint in 6.0.0-gate2.8; this alias leaves with 6.1.0.") and keeps its record, so `--oa-color-state-error-mark` and its four surface names still resolve, in the surface classes and both themes too. tokens.css marks each old line with a comment. The token count rises from 500 to 504.
- **Descriptions (DR-218).** 66 token descriptions and nine group descriptions change. Every studio code (DR-, D2-, G1-, T-, R9 to R13), retired name (Signal Grid, V5, "the studio pages") and internal name (Explainer, the palette lab, the stretch test, treatment D) leaves the descriptions. The loading mark's description now reads "The still lines of the loading state: the lines the data will sit on, drawn with no marks on them. They never move (Rule 17.7)." The token table prints each description word for word; its old rewriting step is now a guard that stops the build on any code, retired name or internal name.
- **The change note (BE-S7).** One note for 6.0.0-gate2.8, in reader words: the tokens, the change and the reason, with the decision codes in a separate `record` field that chapter 26 does not print. The 6.0.0-gate2.7 note's reason now says "drawn from our dark atlas style on Charcoal" where it named Night Edition; the 6.0.0-gate2.6 note's reason is in words too.
- **Tests.** The rule test gains a deprecated-token section: a deprecated token points at its replacement alone, in its own tier and type and on its own surface, its description opens with "Deprecated", it names a later release of the second part for its removal, its release has a change note, and no live token points at a deprecated name. Three new plants prove it (44 plants, from 41). The "version rise with no note" plant now rises past whatever today's version is.
- **My files that read the old name** now read the new one: the shell's status line and the token table's status line. Chapter 26 prints the change note's date in words and names the deprecated alias in Rule 26.8.

**Still reading the old name, through the alias, in other owners' files** (they keep working until 6.1.0): chapters 05, 11, 17 and 18 (`*.json` token lists and words), the specimens `s-05-3-corrective`, `s-05-4-correct`, `s-11-15-correct`, `s-11-16-correct`, `s-11-16-failure`, `s-11-marks`, `s-17-8-correct`, `s-18-12-anatomy`, `s-18-17-anatomy`, `s-18-18-anatomy`, and the code sets `c-18-form`, `c-18-tracker`, `c-18-copy`, `c-18-table`, `c-18-code-block`, `c-18-messages` and `c-18-report-reader`. The build does not warn on the old name yet, so no owner's strict build breaks before they move.
