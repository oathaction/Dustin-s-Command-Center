# Chat 10, creative director's notes

Creative director (oa-creative-director), Phase 4, chat 10, November 21, 2026. Started 01:36 UTC; plan written by 01:58 UTC. Brief: `work/handoffs/phase-4/20261121_Chat-10-Brief.md`, sections 1 to 4 and 6. File held this chat: `work/handoffs/phase-4/20261121_Chapter-16-Plan.md`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/127ebfa4-7663-587b-a8ae-9ad439f7784c/scratchpad/c10/creative-director/`.

The research lead's "Facts for chapter 16" landed at 01:41 UTC and the engineer's contract C1 at 01:40 UTC, both before the plan was written, so every rule rests on them. C1 was revised at 01:45 UTC (an `<img>` request cropped in CSS or by `data-oa-crop`, in place of an SVG drawing); I read the revision at 01:59 UTC and moved the plan to it the same minute. One fact is still missing and is marked in the plan as a gap (Requests, item 1).

## Routine calls

- D4-xxx | Chapter 16 has 13 rules in four groups and one extra, "Where each kind of picture may appear" | Master Brief section 16 names sixteen subjects, and thirteen rules carry them with no rule doing two jobs; the brief asked for about 12
- D4-xxx | Black and white is chapter 16's default treatment, with color only where it is part of the record, and V5's Charcoal duotone retires | Gate 1's S10 (G1-03) replaced V5's natural-color default; one treatment keeps photographs from different sources together and keeps a photograph's own reds off the view's one working red (Rule 05.3)
- D4-xxx | Chapter 16 uses no generated image; Rule 16.9 shows its label on a placeholder frame | P4-3's test: the label is a tab, a caption line and the start of the alt text, and a frame shows all three at true size
- D4-xxx | Every 3:2 use of the Rotunda photograph takes the rectangle 60 0 1080 720 | A CSS crop at 3:2 keeps the full 797 px height, which shows the Architect of the Capitol's corner mark, so these uses take `data-oa-crop`
- D4-xxx | The four video rules follow one example video built on chart S04 | Every figure on a video plate is then real and carries S04's source; only the video itself is Illustrative
- D4-xxx | Placeholder frames take a solid keyline and corner crop marks, with no dashed line and no cross | Dashes carry evidence grades in chapters 13 and 15, and a cross can read to a newcomer as a failure mark
- D4-xxx | A photograph shows at 240 px wide or more | Below that, faces and hands stop reading; design judgment
- D4-xxx | On TikTok and Instagram, captions are the app's own, corrected word for word; burned-in captions only where a platform offers neither | The research lead found no caption file upload on either; burned-in captions cannot be turned off or read aloud
- D4-xxx | Rule 16.9's prompt describes a mockup scene (a phone on a kitchen table), with no conceptual drawing | A generated drawing would take the hand-drawn spot illustration's job, which Gate 1's Y6 gives to a person
- D4-xxx | Rule 16.3's failure crops the official out and keeps chapter 01's caption naming him | The fault a crop most often makes: the caption names someone the picture no longer shows

## Done

- Created `work/handoffs/phase-4/20261121_Chapter-16-Plan.md`: opener and intro, four groups, Rules 16.1 to 16.13 with plates, specifications, bases, tokens, related rules and WCAG criteria, the extra, the WCAG table, the byte estimate (about 298,500 against 300,000), sources, and what chapter 16 hands to chapters 20 and 23.
- Created this notes file.
- Crop previews and the script that makes them, in scratch only: `scripts/crops.py` and `crops/*.png`.

## Requests

1. **Research lead, a marked gap:** quote the W3C's "Understanding Success Criterion 1.2.5: Audio Description (Prerecorded)" (and 1.2.3 if it says the same) where it speaks of video whose soundtrack already carries what the picture shows. Rule 16.12's Why needs it; the design director leaves the field `why_understanding_quote` empty until it lands.
2. **Research lead, optional:** a published caption standard for line length and lines per caption, if the editor wants a citation in place of "design judgment" in Rule 16.11; the NPPA Code of Ethics' official text, if the page can be read; a source for state rules on cameras at polling places, only if the editor wants Rules 16.1 and 16.6 to state the law, since today they give a procedure ("ask the election official first").
3. **Engineer, a check only:** under `data-oa-crop` the build wraps the `<img>` in a frame that takes its class; confirm that `filter: grayscale(1)` on that class turns the photograph black and white once, with no second filter on the inner `<img>` that would change it. (With C1's revision to an `<img>`, the filter and an HTML tint layer over the frame are ordinary CSS; my earlier worry about an SVG drawing no longer applies.)
4. **Main session, for the owner of `work/build/scripts/phase-2/stage_c_ch19_build.py` once chapter 16 builds:** in `MAP` and `GAP_OWNERS`, move 1.2.1, 1.2.2, 1.2.3 and 1.2.5 from gap to met with Rules 16.11 and 16.12, keeping chapter 23 as a second owner for its frames; 1.2.4 and 1.4.2 stay "none", with Rules 16.11 and 16.13 as pointers. The register row "Chapter 19's other seven gaps" names this step.
5. **Editor, at the hand-over:** chapter 18 uses "placeholder" for a form field's hint text, so chapter 16 defines its own at first use (house rule H02). V5's shot list has six How lines cut at 50 characters by the census, and the V5 source file is not in this container; complete or rewrite them, and rewrite "Hands, not faces." under Rule 02.9.
6. **Main session, for Phase 4 board 1:** the question for Dustin in "Not fixed", row C16-CD-01.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| C16-CD-01 | Chapter 16 plan, creative director, chat 10 | Rules 01.6 and 01.8: `s-01-6-correct`, `s-01-8-correct`, `s-01-8-failure`, written by `work/build/scripts/phase-2/guide_editor_ch01.py` | The three plates show their photographs in color. Gate 1's S10 (G1-03) sets black and white by default, with color where color is evidence, and chapter 16 follows S10, so the guide shows the same two photographs two ways | Add `filter: grayscale(1)` to the photograph's class on the three plates, a CSS change with no new bytes | It changes approved chapter 01 on screen and needs Dustin's named answer; the engineer's P4-5 work this chat must also leave chapter 01's plates unchanged at every width | Open, for Phase 4 board 1 |

## Tested

- Every crop the plan names was computed by script under C1's rule (`object-position` under `object-fit: cover`), asserted to lie inside the photograph's pixels, rendered in black and white from the 1,200 px renditions and viewed by eye: the meeting at 3:2, 16:9, 1:1, 4:5 and 1.91:1 and the failure crop without the official; the Rotunda at 3:2, 16:9, 1:1, 4:5 and 1.91:1, the walls-only failure and the left 4:5 used in Rule 16.7. Each Rotunda rectangle stops at row 720 or above.
- The plan's plate table recomputed by script: 28 plates, 18 photograph uses, 160,500 bytes.
- Plate sizes for chapters 12 and 13 measured from their specimen files (104,292 and 117,198 bytes); their chapter totals come from the Gate 3 report's bytes per rule times their rule counts, not from a build I ran.
- Every rule number the plan cites was checked against the built chapter JSON for chapters 01, 02, 12, 13, 17 and 19, and S04's figures against `work/build/chart-kit/specs/s04.json`.
- The plan and these notes scanned by script for em and en dashes: none.

## Not tested

- No plate was built or seen in a browser, and I ran no strict build; the design director builds the chapter.
- The contrast under Rule 16.4's failure headline; the design director measures it on the plate and prints the figure.
- The grayscale filter and Rule 16.2's tint layer on a built plate; the design director sees them when the chapter builds (Requests, item 3).
- Rule 16.6's marker positions on the built plate; checked on a preview only.
- The platform and W3C facts as the research lead wrote them; I did not reopen those pages.
- V5's full shot list text; the V5 source file is not in this container, and the census holds 50 characters of each line.
