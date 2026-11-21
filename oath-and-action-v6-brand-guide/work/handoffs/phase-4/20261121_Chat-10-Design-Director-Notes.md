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
- D4-xxx | Chapter 16: every plate is a readable stage (a group its alt describes), except Rule 16.8's failure, an image stage | Rule 16.8 makes a placeholder live text; the fifth edition's panel is a picture of a fault
- D4-xxx | Chapter 16's placeholder frames keep 19 px above and below for their crop marks and none at the sides | The marks then clear the words around them, and the stage's 24 px padding holds them at the sides
- D4-xxx | Rule 16.2's correct plate sets the photograph at 360 px and the placeholder at 320 px, side by side | The plan's 540 and 260 px wrap in the 722 px stage at 1440
- D4-xxx | Rule 16.10's storyboard runs one frame a row under 48em | Two a row on a 390 px phone clip a 16:9 frame's words
- D4-xxx | Rule 16.4's correct kicker is "Report · Public lands" | The plan left the label to the design director; the headline reports an agency's record (Rule 01.21)
- D4-xxx | Each chapter 16 rule prints a "WCAG 2.2" specification row with the plan's criteria | The plan names them by rule, and chapter 19's map reads them there
- D4-xxx | Rule 16.4's failure figures come from the photograph's pixels, measured by the generator: lowest 1.0 to 1, 17 percent of the ground under 3 to 1 | The plan asked for the measured figure in the caption
- D4-xxx | The report page's four cut paragraphs are completed by the studio from the report's own later pages and marked as such in the spec, for chat 15 to replace | The census keeps 50 characters a paragraph; V5 arrives at chat 15 (DR-304)

## Done

- Created `work/handoffs/phase-4/20261121_Kit-Sample-Specs.md` (Job A), 02:02 UTC.
- Created `work/build/scripts/phase-4/phase4_ch16_build.py` (Job B), which writes `work/build/guide/chapters/16-photography.json` (13 rules in four groups, an opener and one extra), 28 specimens `work/build/guide/specimens/s-16-*.html` and `work/build/guide/specimens/manifest-photography.json`. Built from the creative director's plan and contract C1: 18 photograph uses by name, none embedded, every photograph in black and white. No tracked file changed (`git status`: only these new files of mine).
- Chapter 16 weighs 213,681 bytes against its 300,000 (71 percent; the build's own line). Its 28 plates with their frames, as placed: opener 3,412; 16.1 6,839 and 3,217; 16.2 5,027 and 3,584; 16.3 4,572 and 3,372; 16.4 3,852 and 4,263; 16.5 4,515 and 3,093; 16.6 5,477 and 4,668; 16.7 4,363 and 3,440; 16.8 5,700 and 2,968; 16.9 4,757 and 4,359; picture kinds 4,779; 16.10 5,259 and 4,386; 16.11 4,185 and 3,724; 16.12 4,603 and 3,538; 16.13 7,117 and 2,633; 121,702 in all. The photographs weigh in the page's own part, 489,462 bytes, one copy each.

## Words ready for the editor

02:21 UTC. Chapter 16's words are yours from now on; I write no word field again. Every field is in `work/build/scripts/phase-4/phase4_ch16_build.py`, in the WORDS section near its top (the module docstring lists them):
- `W`: `title`, `instruction` (fixed by the brief), `intro`, `groups`, `cap_lake`, `cap_rotunda`, `alt_lake`, `alt_rotunda` (chapter 01's, kept word for word), `opener_alt`, `related_chapters`, `sources`.
- `R['16.1']` to `R['16.13']`: `title`, `rule`, `why`, `basis`, `specs`, `builders`, `correct_caption`, `failure_caption`, `correct_alt`, `failure_alt`, then each plate's own words under the keys after them (for example `R['16.1']['rows']`, `R['16.6']['record']`, `R['16.10']['frames']`, `R['16.11']['vtt']`).
- `EXTRA_KINDS`: the extra after Rule 16.9.
- To look at: the six How lines marked `# completed` in `R['16.1']['rows']` (the census cut them at 50 characters) and the rewritten kitchen-table line; the credit forms for our own photographs in `R['16.5']['specs']` (the plan asks you to confirm them); `R['16.12']['why_understanding_quote']`, filled from the main session's addendum and quoted in the Why; the plan's draft words throughout, which I set as written except where a check or a plate needed a change.
- Run it as `flock <scratch>/c10/build.lock python3 -I work/build/scripts/phase-4/phase4_ch16_build.py`, then the strict build. Its check fails on an em dash, an en dash, a straight quote or apostrophe and the listed filler words, and on a specimen with a literal color or a heading element.

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
- Chapter 16: the generator's `--check` and write, then the strict build under the lock, three times, the last at 02:20 UTC: exit 0, 0 warnings, 382 rules, 12,233,841 bytes; chapter 16 at 213,681 bytes. The build report lists each photograph with one copy (rotunda-2005 and lake-isabella-2014).
- Every chapter 16 plate captured from the built page at 1440 and 390 px in Chromium and looked at: the crops, markers and placeholders sit as the plan sets them; tables stack on phones; three layout faults found and fixed (crop marks over a failure band and over captions, Rule 16.2's pair wrapping, the storyboard clipping at 390).

## Not tested

- The kit's own drawings of the samples, their contrast on pixels, axe, keyboard and reflow runs, Rule 08.2's feed test on the post and the samples' bytes: the engineer's build and the main session's checks.
- Safari, Firefox and real screen readers.
- Chapter 16: the guide check (axe, contrast on pixels, the red test) and the four-width check, which the main session runs; plates at 1024 and 360 px; reading order heard with a screen reader.
