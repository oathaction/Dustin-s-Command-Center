# Chat 10, design director's notes

Started November 21, 2026, 01:38 UTC. Owner: oa-design-director. Files held this chat: `work/handoffs/phase-4/20261121_Kit-Sample-Specs.md`; `work/build/scripts/phase-4/phase4_ch16_build.py` and its outputs (`work/build/guide/chapters/16-photography.json`, `work/build/guide/specimens/s-16-*`, `manifest-photography.json`).

## Contracts

- **K1. The kit's three measurement samples, complete 02:02 UTC:** `work/handoffs/phase-4/20261121_Kit-Sample-Specs.md`. The engineer builds the application kit's three samples from it (social post 1080 by 1350; article page at 1440, 1024, 390 and 360 px, light and dark; report page 3, US Letter with 0.125 in bleed). Sections 1.3, 2.3 to 2.5 and 3.2 to 3.5 hold every box, style, token and word; 1.4 and 3.6 the overlays; 1.7, 2.7 and 3.4 the exports and checks.

## Routine calls

- D4-xxx | The social post carries S92's figure, 20 working days under the Freedom of Information Act, with S92's source line naming its paragraph | One real figure an approved chart prints (brief 7.1); a rule a reader can look up, so the hinge headline "The records law & your answer." passes Rule 02.27
- D4-xxx | The post's source line and sign-off sit on a full-bleed Charcoal band, the card's one dark panel | Rule 05.1: the band puts the card at 66.3 percent Newsprint; S95's all-Newsprint foot measures 88.7 and a figure-in-band version 58.0
- D4-xxx | The post keeps the proof card's kicker (the H3 face) at 36 px, not 32 | Rule 14.141's 36 px floor for a portrait post shown at about a third of its size
- D4-xxx | The article sample is an Explainer on special districts with chart S86, its headline "What a special district does" | S86 is a compact reading chart that follows the theme; "What is a special district?" would leave one word on its last line at 56 px (Rule 06.6)
- D4-xxx | The article's provisional header sets L1, the wordmark alone, at every width, and the footer keeps the lockmark | Rule 08.2, once in a view: each full-page capture shows header and footer together
- D4-xxx | The article's kicker draws CL-031 from the guide's sprite, never from its fit file | The fit file is Charcoal only and vanished in the dark prototype
- D4-xxx | The report page's page-header lockmark takes the 24 px master at 0.25 in | At 96 px to the inch 0.25 in is 24 px, the 24 px master's range (Rule 08.1); the display master's nodes would print 0.39 mm across
- D4-xxx | The report page's four cut paragraphs are completed by the studio from the report's own later pages and marked as such in the spec, for chat 15 to replace | The census keeps 50 characters a paragraph; V5 arrives at chat 15 (DR-304)

## Done

- Created `work/handoffs/phase-4/20261121_Kit-Sample-Specs.md` (Job A), 02:02 UTC.

## Requests

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| DD10-NF1 | Design director, Job A prototypes | Every hinge headline on Newsprint (Rule 04.3; the proof's card, `s-proofs-social`) | Ampersand B in Pillar Red on Newsprint measures 2.96 to 1, under WCAG 2.2 1.4.3's 3 to 1 for large text if B is read as text; the studio reads B as the identity master, a logotype, with "and" as its accessible name | The accessibility lead rules whether the logotype exception holds; if not, Rule 05.5's 1 px Charcoal keyline inside B | Approved work; a ruling, not a design change, decides it | Open, for chat 12's review |
| DD10-NF2 | Design director, Job A prototypes | Rule 06.5's tabular big figures (`oa.type.figure`) | A tabular "1" in Inter Tight 800 carries wide side bearings, so a figure that starts with 1 ("100") stands about 5 px right of one that does not, in a stacked rail | A note in Rule 06.5 that a figure standing alone may set proportional figures, or an optical left shift | Approved work | Open, low |
| DD10-NF3 | Design director, report prototype | PDF exports from Chromium | Chromium embedded Inter as Type 3 fonts from the variable woff2 (Inter Tight as CID TrueType) | Static Inter instances for PDF exports; the kit sample spec 3.4 asks for it | The engineer's kit; recorded so chapters 24 and 25 inherit it | Open, for the engineer |

## Tested

- Job A prototypes, rendered in Chromium at 1x with the guide's fonts and tokens (scratch `c10/design-director/proto/`): the post's boxes as spec 1.3 lists them; Newsprint shares 66.3 (this post), 88.7 (S95), 90.7 and 58.0 (two rejected layouts); the article at 1440 light and 390 dark; the report sheet and a test PDF at 630 by 810 pt with `pdfinfo` and `pdffonts`.
- Text widths for every headline and source line, from the chart kit's metrics (no kerning), against each measure.
- S95, S86 and S92 built by the kit to scratch: PASS, 0 faults each.
- The Census Bureau's glossary read by `curl` at 01:53 UTC for the special district definition the article quotes.
- The spec file: 0 em dashes, 0 en dashes.

## Not tested

- The kit's own drawings of the samples, their contrast on pixels, axe, keyboard and reflow runs, Rule 08.2's feed test on the post and the samples' bytes: the engineer's build and the main session's checks.
- Safari, Firefox and real screen readers.
