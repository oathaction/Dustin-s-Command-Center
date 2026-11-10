# Brief: stage B round 3, the fix pass

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the main session for five owners: the identity designer, the systems designer, the chapter 11 hand, the editor and the engineer. It merges the four round 3 reports into one list per owner, with the main session's rulings where reports overlap or a fix touches a decision. Dustin approved the plan (DR-190 to DR-194). The main session's calls for this pass start at D2-958.

## Read first

- `CLAUDE.md`, your role file in `.claude/agents/`, the final stage B brief (`20261109_Stage-B-Brief.md`), the round 2 brief, and your own round 2 notes. The writing rules, `20261106_Voice-Writing-Rules.md`, govern every word you write.
- The four round 3 reports, for the items this brief routes to you. Each item below names its report and number; the report holds the quote, the place and the fix:
  - BE: `20261110_Stage-B-Round-3-Red-Team-Brand-Evidence.md`
  - CA: `20261110_Stage-B-Round-3-Red-Team-Craft-Access.md`
  - PP: `20261110_Stage-B-Round-3-Red-Team-Plain-Production.md`
  - CD: `20261110_CD-Review-Of-Stage-B-Chapters.md`
  - ED: the editor's tables, section 4 of `20261110_Stage-B-Round-2-Editor-Notes.md` (4b, 4c, 4d and 4e; 4e says which rows are still open)
- The decision log from DR-93 on. Every answer from DR-95 to DR-194 is settled. If a fix would change one, stop and say so in your notes.

## How to fix

- **Fix in the generator, never in an output file.** Chapter files and specimens are written by build scripts; an edit made only to an output is lost on the next rebuild. Word changes go into your scripts or their data files. After your edits, rerun your own scripts in the order your round 2 notes give.
- **One run per string.** Several reports touch the same strings. Apply every item for a string in one edit, so no fix undoes another (CD's risk note).
- **Your own new sentences** follow chapter 02's rules. The editor reads every changed string after this pass (D2-963), and wording faults go to a short second pass (DR-191).
- **Check as you go.** `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <your scratch>/guide.html` must exit 0, and `node work/build/scripts/phase-2/guide_check.js <your scratch>/guide.html` must show 0 failures. Look at your changed plates at 1440 and 390 px, at 1x and 2x where pixels matter.
- **Shared chapter 12.** Rules 12.1 to 12.4 and the identity intro sentence are the identity designer's (`stage_b_identity_ch12.py`); Rules 12.5 to 12.9 and the rest of the intro are the systems designer's (`stage_b_ch12_systems_build.py`). Each script rewrites only its own rules, as in round 2. Run the systems script first, then the identity script.
- **Shared manifests.** `manifest-systems.json` is written by the systems designer's scripts and the chapter 11 hand's; each merges only its own entries. Write it only through your scripts. When every owner is done, the main session reruns every generator in order and rebuilds, which heals any write that crossed another.
- **Chapter 01.** The editor runs `guide_editor_ch01.py`, then the identity designer runs `stage_b_identity_ch01.py` (D2-912). The chapter 11 hand's `s-01-pieces` change goes through the editor's build: send the editor the class names, or edit the mark markup in the place the editor's notes name.

## Rulings by the main session

- **D2-958. Examples on the editor's campaigns (BE-M1, BE-M2).** V7 flags R-01 and R-02 for the editor's own work, and the guide carries no disclosure (DR-100). Under DR-93, DR-99 and D2-203 these are routine fixes. Rule 10.8's plate lists every reform that acts on D02's six variables (ten, as chips with their names) if they fit its width; if not, it prints "Two of the ten reforms that act on them" with two V7 does not flag (R-05 and R-45). H.99009 takes a neutral subject, and its figure draws a reform V7 does not flag (R-32 on Variable B2, or R-14 on Variable D5). Rule 11.16's three marks, their order and the yielding stay exactly as built.
- **D2-959. Chapter 05's error plate (D2-881, BE-S9).** `s-05-3-corrective` draws `U-error` in the text's ink with the 4 px Pillar Red bar, as Rule 11.15 is built, so chapters 05 and 11 show one error treatment until Dustin rules on D2-880 at board B.
- **D2-960. The chart key's title (BE-M4, CD-M2).** Retitle to what the invented counts hold: "Most claims in these three chapters are documented or well supported" (28 of 39). The counts stay.
- **D2-961. Numbers and the records clock (BE-S2, PP-S16).** Rule 11.10 takes BE-S2's sentence with numerals: "up to 10 working days" (H06). Rule 11.9 takes "the main way the law gives the public".
- **D2-962. Where the pillar row goes (PP-M2).** The identity designer names the places in Rule 09.1, in line with chapter 01's `s-01-pillars` captions and Rule 09.4's places, and says in the proofs' social card spec whether a social card carries a pillar row and a topic symbol. Board B shows the sentence to Dustin.
- **D2-969. The loop stepper's plausible step (BE-M3).** Whatever loop the stepper runs, a step graded plausible takes "can" or "may" and the sentence "Our atlas grades this step plausible, the least certain in the loop." Which loop it runs is Dustin's call (asked now). Until he answers, the chapter 11 hand does every other item first.
- **D2-964. The tokens.css download (DR-192).** The host's save call takes only these extensions: gif png jpg jpeg webp mp4 webm mov txt json md docx pptx epub csv ttf html svg pdf xlsx zip fig. A `.css` file is refused. On the published page the button saves `20261106_Oath-And-Action-Tokens.zip` holding `tokens.css`; where the host is absent, the plain `.css` link stays. Details under the engineer.

## The identity designer

Chapters 03, 04, 08, 09, Rules 12.1 to 12.4, `s-01-pillars`, `s-01-21-*`, `s-08-3-*` and the proofs.
1. ED 4b: chapter 09's seven open rows. ED 4c and 4e: the open rows for Rules 12.1 to 12.4, the watermark plate's alt (Track's job line), and the intro sentence.
2. PP-M2 with D2-962: where the pillar row goes, in Rule 09.1 and the proofs' social card spec.
3. PP-S1: define "pixel fit" at first use in chapter 09, use the same term in Rule 04.6, and give each of Rules 04.6 and 09.3 one clause on why their switch points differ (D2-808).
4. PP-S2: one sentence in Rule 09.3 for an exported image and print.
5. CD-S1: the phone column's arrows in one column.
6. CD-S10: the watermark's crop cuts B's terminal off whole or keeps it whole, on both covers.
7. CD-S11: the Illustrative chip inside the plate for Rules 12.2 and 12.4's failures.
8. Every craft and accessibility item routed to you in the CA section below.

## The systems designer

Chapters 05, 06, 07, 10 and Rules 12.5 to 12.9.
1. ED 4e: Rule 10.2's caption. ED 4c and 4e: the open rows for Rules 12.5 to 12.9 and chapter 12's intro.
2. D2-950: non-breaking hyphens (U+2011) in the IDs of chapter 10's 24 px list, and anywhere else an ID can break.
3. Every banded failure plate's alt in chapters 05, 06, 10 and 12.5 to 12.9 opens "Failure case: do not publish." (ED 4e, the band's own words).
4. D2-881 with D2-959: `s-05-3-corrective`.
5. BE-M1 with D2-958: Rule 10.8's reforms.
6. BE-M4 and CD-M2 with D2-960: the chart key's title and alt.
7. BE-S5 and CD-S13: the Illustrative label on `s-12-locator-correct` and its failure.
8. CD-S2: Rule 10.1's atlas example becomes CL-009 Safe seats.
9. CD-S3: `s-10-9-failure`'s kicker reads "Act · How to take part".
10. CD-S4: the library sheets box each atlas ID as the typed chip, and set the 24 px tag in a different form.
11. CD-S12: Rule 12.5 lists the red's token in its tokens and its "Target weight" spec.
12. PP-S3: one sentence in Rule 10.6 or 10.9 for a subject no topic drawing names (its word alone, or an atlas drawing only with the atlas's own name). Send the sentence to the editor for Rule 01.21.
13. PP-S5: a spec row for the typed chip (outline, padding, type), one order for chip and name in both specimens, and Rule 10.8's wording.
14. PP-S7: Rule 10.5 says how large the drawing stands in each tile size and squares it with Rule 10.4's floor.
15. PP-S8: Rule 10.7 says what two symbols with no current item do.
16. PP-S4, PP-S6 and PP-S10: define "edition" (and write "our guide's fourth edition" in Rule 10.2), "connection" and "sign" (Rule 10.10), and "measure line" (Rule 12.6) at first use.
17. Every craft and accessibility item routed to you in the CA section below.

## The chapter 11 hand

Chapter 11 and the marks in `s-01-pieces`.
1. ED 4e: chapter 11's five rows. Every banded failure plate's alt opens "Failure case: do not publish."
2. D2-950: six tracker pictures name each step's state in their alt, not the marks' shapes.
3. `s-01-pieces` takes chapter 11's mark classes (the engineer's round 2 note).
4. PP-M1: correct Rule 11.2's why on which marks take Stone, and add one spec table, "Drawing the marks": each mark's size at each circle size, stroke, color token and geometry (the slash's angle, length and ink; the halo as a 4 px stroke that shows 2 px; the square's size; the take-part disc's center; the line into a final step that never happened). Make `s-11-8-correct`'s request 99003 and the words agree. Fix Rule 11.5's 60 px and 328 px sentence so both halves hold.
5. PP-M3 and CD-S7: the specs list `--oa-color-state-error-text-on-<surface>` as the error mark's ink and label `--oa-color-state-error-mark-on-<surface>` "the red bar".
6. CD-M1: the report reader shows real lines of the report's text under each heading, at the page's own type size, and either twelve distinct headings or a four-page report.
7. BE-M2 with D2-958: H.99009's subject and figure; then BE-S6, the Illustrative label beside the bill card only; CD-S5's line breaks in what remains.
8. BE-M3 with D2-969, last, once Dustin answers.
9. BE-S1: the Justice Department source line, as BE-S1 writes it.
10. BE-S2 with D2-961, BE-S3 (Rule 11.8's scope sentence; the invented requests take federal subjects or drop "20 working days"), BE-S4 and CD-S8 (the research lead's state hearing source line from `20261109_Stage-B-Research-Notes.md`, section 4), BE-S8 (periods in source lines: "as in force on November 9, 2026" after a statute, "no page date" after an undated page).
11. PP-S11: Rule 11.10 says which statuses carry the warning mark and a check date.
12. PP-S16: Rule 11.16's why loses its closing restatement, "only the color moves".
13. CD-S6: `s-11-marks`'s Illustrative chip at the plate's head. CD-S9: the stepper's visible text says "connection".
14. Every craft and accessibility item routed to you in the CA section below.

## The editor

Chapter 01's words (`guide_editor_ch01.py`), the reader check's questions file, and the read after this pass.
1. D2-950: step 4 of the reader check takes a neutral title, such as "A card and a drawing", in `20261110_Reader-Check-2-Questions.md`; tell the engineer.
2. PP-S13: step 7's footer question: "Look at the small square mark beside the line of text. What did you see in it?"
3. BE-S7 and PP-S3: Rule 01.21 names "a topic or atlas symbol from the 37 that read at 24 px (Rule 10.4)" in its rule, spec and builders line, and takes the systems designer's sentence for a subject with no drawing.
4. PP-S12: Rule 01.11's Virginia sentence names the statewide vote by voters.
5. CD-S14: Rule 01.11's count source keeps H04's order, and a short note headed "How we counted" holds the method, Ohio, Missouri and Utah, every fact kept as DR-187 sets it.
6. CD-S15: `s-01-pillars`'s label reads "On a page that serves Track, at 48 px".
7. BE-S8 for chapter 01's source lines, if any lacks a period.
8. Do items 1 to 7 now and write your notes. Then stop: the main session sends you a message when the other owners finish, and you read every changed string in chapters 01 and 05 and 09 to 12 and their alts against chapter 02's rules, and list any fault as a table for the short second pass (D2-963). Edit no other owner's file.

## The engineer

The shell, `guide_build.py`, `guide_check.js`, tokens and the reader check page.
1. DR-192 with D2-964: in `guide-shell.js`, the download button calls `await window.claude.use("downloads")` when `window.claude` exists; if that resolves to a namespace, a click builds a zip holding `tokens.css` (the build can embed the zip's bytes) and calls `downloads.save({filename: "20261106_Oath-And-Action-Tokens.zip", data})`, catching every rejection (`declined` needs no message; `unavailable` and the rest fall back to the plain link). With no host, the plain `.css` link works as now. The button's words say what the reader gets on each. The type definitions are at `/tmp/claude-0/bundled-skills/2.1.322/ed282e60ed6f99dc0e6f3ccb79b24de5/artifact-capabilities/0.2.96/downloads.d.ts` and `claude.d.ts`. The main session publishes with `capabilities: {downloads: true}`.
2. The reader check page: rebuild after the editor's two changes; PP-S14 (the readable lines of the copy text drop studio codes and the before and after labels, and write times in words; the record line keeps every code); PP-S15 (drop the 9 px ring on the copy-mode line). Rerun its test script.
3. PP-M3: the error mark token's description says it colors the 4 px bar beside an error, not the mark. Its name waits for Gate 2 (D2-880). Rerun the token tests.
4. Every craft and accessibility item routed to you in the CA section below.
5. CD-S16 (an opener figure for chapters 09 and 10) waits for stage C's shell pass (D2-965).

## Craft and accessibility items

Rulings first:
- **D2-971. Five drawings that look alike at 24 px (CA Q1).** The 41 stay as DR-136 set them. Rule 10.9 gains one line: at 24 px, never set two of CL-023, CL-028, R-08, R-27 and R-45 in one view; `s-10-9-correct` shows the five as a 24 px look-alike group. The line narrows use and changes no approved list, so it is routine; board B shows it.
- **D2-972. The stepper's pace (CA-M1).** Play holds each step for about 250 ms a word and never under 6 seconds, under reduced motion too, and Rule 11.14's spec states the pace. This replaces D2-868's 2.4 seconds.
- **D2-973. The social card in the reader check (CA-S18, first point).** The identity designer judges whether the proofs' social card kicker should read at feed size (358 px wide, Rule 08.2's feed test) and either enlarges it in `s-proofs-social` or logs why not. The engineer recaptures the card after.

Overlaps, applied once: CA-S4 with CD-S5 (moot if BE-M2 removes "all-party"); CA-S6 with CD-S1; CA-S10 with CD-S10; CA-S15 with CD-S14; CA-S18's copy text with PP-S14; CA-S1 with CD-M1.

| Item | Owner | What |
|---|---|---|
| CA-M1 | Chapter 11 hand | The stepper's pace, D2-972 |
| CA-M2 | Chapter 11 hand; engineer | "Clear the search" at 44 by 44 px; the guide check types into the field before it measures |
| CA-S1 | Chapter 11 hand | The reader's page title reaches screen readers (with CD-M1's real text lines, the whole page can be readable) and the status line names the page's title |
| CA-S2 | Chapter 11 hand | The filter's results say how many more there are |
| CA-S3 | Chapter 11 hand | The phone menu's header bar stays put while its list scrolls |
| CA-S4 | Chapter 11 hand | Hyphenated compounds never split at a line end in a fixed plate |
| CA-S5 | Identity designer | Chapter 09's four 400 to 406 px plates fit at 390 and 360 px (build at 358 or 360 px, as chapter 11 does) |
| CA-S6 | Identity designer | With CD-S1 |
| CA-S7 | Systems designer; editor for words | Rule 10.2: one red accent for one idea, which may be one shape or a few, pointing to Track |
| CA-S8 | Systems designer | "Contact an official" breaks as "Contact / an official" or takes the width it needs |
| CA-S9 | Systems designer (`s-10-4-correct`); editor (`s-01-21-correct`) | The Illustrative label at the head of a wholly invented piece; beside the item, in one place, where real and invented mix |
| CA-S10 | Identity designer | With CD-S10 |
| CA-S11 | Identity designer | Rule 12.4's patterns: the rules drawn from the hinge or dropped, and the two covers set without a third of the frame empty (design judgment, logged) |
| CA-S12 | Systems designer | The locator's state headline gets at least 200 px |
| CA-S13 | Engineer; identity designer | `s-03-l6` breaks out of the text column at 1280 px and up, so L6 shows whole |
| CA-S14 | Identity designer | `s-08-1-correct`'s six masters in two rows of three or one row of six |
| CA-S15 | Editor | With CD-S14: one source per line, the method its own paragraph |
| CA-S16 | Engineer | The masthead wordmark takes one system color in forced colors |
| CA-S17 | Engineer | The part navigation wraps at 200 percent text |
| CA-S18 | Identity designer (card, D2-973); engineer (copy text, step 7's grid of four columns) | The reader check's three faults |

## Notes and limits

Each owner writes `work/handoffs/phase-2/20261110_Stage-B-Round-3-<Role>-Fix-Notes.md` (`Identity`, `Systems`, `Ch11`, `Editor`, `Engineer`) early and adds as it goes: each item and what you did, routine calls as "D2-xxx | decision | reason" lines, questions for Dustin with a recommendation, Tested and Not tested kept apart, and a change log.

Never touch `source/`, `work/ledger/`, `deliverables/`, the asset folders' finals or masters, any board except the reader check page (engineer), the first reader check, or another owner's files. Do not commit or push. Scratch outputs go to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/round-3/fix/<role>/`. Reply to the main session in 200 words or fewer.
