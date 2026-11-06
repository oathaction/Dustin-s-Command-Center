# Stage A identity notes: chapters 03, 04 and 08, and the Gate 2 proofs

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261106_Stage-A-Brief.md`. I wrote no ledger, master, `source/` file or other maker's file.

## What I built

| Chapter | Rules | Extras | Specimens |
|---|---|---|---|
| 03 Identity | 8 (03.1 to 03.8) | the eight lockups, the minimum-size table, three more failures | 19 |
| 04 The Ampersand and the hinge | 8 (04.1 to 04.8) | none | 17, with one corrective (04.3) |
| 08 The Signal Grid | 9 (08.1 to 08.9) | codes and combinations, nine stages and five shapes, the composer | 21 |
| Proofs for Gate 2 | none | six groups in `proofs.json` | 11, plus a two-page US Letter PDF |

Every rule has a correct application and a failure case at true size. Each failure is one a producer makes: typing the name in Inter Tight, squeezing the wordmark into a tile, dropping the Newsprint file on a Charcoal slide, joining a partner with a second ampersand, placing Edition 05's Lora file, a red divider above a red button, dashed hinge arcs, a badge turned into a seal, lockmarks as bullets, a grid with no key, a diagonal route.

**Masters by reference.** Each specimen holds `<img data-inline src="work/build/assets/identity/...">`, which the shell inlines (Guide Shell Notes section 5), so no fragment carries a copy of a drawing. The re-exported taglines are inlined by my script with their ids prefixed, because one specimen can hold two copies. No master file was written.

**Chapter 08 rebuilt.** V5's rules A to F become Rules 08.4 to 08.8, with 08.1 to 08.3 for the lockmark and the key and 08.9 for states. One grid codes one thing, in this order: tracker progress, a series route, a pillar corner. Content type leaves the grid for words. Stages are told by shape: a filled disc for done, a ring for under way, a gap for a stage that never happened, a small Stone node for not reached, and one red disc for the stage where a reader can take part now. Active and Ready are now a ring and a filled disc. Loading is still: the links alone with the words "Loading tracker". The composer builds only valid combinations and reads the grid back in a status line.

**Proofs.** Masthead (site at 1440 px with the phone bar, and a 600 px email), avatar (circle and square on Charcoal), a 1200 by 630 social card and a US Letter letterhead, each at today's width and condensed, with ampersand B. Every invented headline, address, recipient and letter carries the Illustrative label; the social card has no web address (DR-55). The PDF is `work/boards/phase-2/stage-a/proofs/20261106_Letterhead-Proof.pdf`, and the letterhead plate carries a download link.

## Routine calls, as proposed decision lines

- D2-xxx | Identity masters enter specimens as `<img data-inline src>` for the shell to inline; the re-exported taglines are inlined by `stage_a_identity_lib.py` with prefixed ids | The fragment names its master by path and never copies a drawing; two tagline copies in one specimen need unique ids
- D2-xxx | The hinge divider is drawn whole in the surface's ink, hairline and ampersand alike, with B's 24 px master at 24 px and 12 px on each side; Rule 04.4 says so | It matches the shell's divider and Board 5, which Dustin approved
- D2-xxx | The editorial crop of B takes the surface's ink, never red | Rule 05.3 names no job for a crop, and the divider sets the precedent
- D2-xxx | Social avatars and the app icon show B alone on the Charcoal tile; L8 serves squares where the name must show | A feed draws avatars at about 32 to 48 px, where L8 sets its capitals at 10 to 12 px; V5 already made B the default avatar (C2)
- D2-xxx | V4.2's compact signature, "O & A" typed with spaces, retires; L8 is the one monogram | The map sent it to the identity chapter for this ruling; two monograms split recognition
- D2-xxx | L7's pillar word sits in the surface's ink at a cap height of 0.6x; V5's red "Act" retires | Rule 05.3 gives a label no red; at 0.6x, CONNECT holds 13 px at the 250 px minimum in the I8 table
- D2-xxx | L4 to L7 are assembled from the approved masters on V5's layouts (L6 measured from the Gate 0 capture: 1400 by 300 units), all White on Prussian, with no web address | Their own masters are not drawn yet (I8 note); this shows them at true size meanwhile
- D2-xxx | The masthead sets L3 from 768 px and L1 from the 24 px master below it | The lockmark needs about 34 px, which a phone bar gives to the menu button
- D2-xxx | Signal Grid codes: one per grid, by precedence; progress from 40 px, routes and corners from 24 px; content type in words | Tension 4; V5's content colors fail grayscale and its Active and Ready differ at 1.14 to 1
- D2-xxx | Coded grids are drawn on whole-pixel lattices: 24 px on the 24 px lockmark master's centers, 40 px at 3.5, 19.5 and 35.5 px; 80 px is the 40 px drawing doubled | Pixel fit (D1-17) for marks that carry meaning
- D2-xxx | Coded grids use no Verdigris, so the held `verdigrisOnDark` (#59857D) can be rejected | The token file holds it "for the Signal Grid chapter"; shapes now carry state
- D2-xxx | Loading draws the links alone and Empty draws small nodes, each with its words; the token architecture's "still Stone outline lever" is not used | A ring at the lever's place would read as a stage under way
- D2-xxx | The favicon row leaves the lockmark's positions table | I8: favicons use B's 16 px master
- D2-xxx | The kicker is a 24 px grid, 12 px, a 24 px Civic Line icon in one color, 12 px, then a 13 px label and an optional ID chip | One definition on the 8 px rhythm; V5's labels sat at 10 and 11 px
- D2-xxx | Illustrative bills reuse V5's invented numbers (Q-01) on neutral topics: public meeting notice, school bus contracts, library hours, records request fees | V5's topics were election rules, which carry the editor's disclosure (D2-106)
- D2-xxx | In the proofs both widths sit at the same height, except avatars, where L8 fills the same width of the tile | Mastheads and cards are set by height; a tile is filled by width
- D2-xxx | The letterhead places the display master at 26 px tall, as a print piece would; all its text is 10 pt or larger | The 24 px master is drawn for screens; the 13 px floor holds on screen
- D2-xxx | Two typed failure cases (03.1, 03.7) carry `check_exempt: contrast` and two (04.3, 04.4) `check_exempt: red`; V5's kicker (08.8) is a PNG | A failure has to show at true size; the shell lists every exemption

## Open questions for Dustin

1. **Width and ampersand at Gate 2.** The proofs show both. *Recommendation:* today's width and B as refined (D2-30). The condensed drawing passes the craft checks, but at the same height it only runs narrower, it sits close to campaign-sign lettering, and its monogram reads as 0&A.
2. **The Signal Grid's new codes.** Content type leaves the grid, each grid codes one thing in a fixed order, and stages are told by shape. *Recommendation:* approve, since V5's codes fail grayscale and color-blind reading.
3. **The avatar.** B alone on Charcoal, or L8. *Recommendation:* B alone. At feed size L8 sets its capitals under the 14 px floor at either width, so the avatar does not depend on the width decision.
4. **The editorial crop's color.** *Recommendation:* the surface's ink, as Rule 04.8 now says. Red would spend the view's one working red on decoration.
5. **Series routes.** V5's census clips text at 50 characters, so I matched the six series names to the six routes by their order in V5; every route ends on its pillar's corner, which supports the reading. *Recommendation:* confirm the six pairs in Rule 08.6, or name any that should change.

## Tested

- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`: 8 chapter files, 99 rules, 234 specimens, no warnings.
- `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` at 1440, 1024, 390 and 360 px: pass, 0 failures, axe-core 4.10.2 with the WCAG 2.2 AA tags, no outside requests but Google Fonts, no script errors. A `--quick` run after my last change also passed.
- The composer, driven by script in the built page: each code, the stage, under way, the gap, the step (disabled until the stage is under way, with its reason shown), series, pillar and Reset; one red node at most; the status line reads each state.
- Every plate of mine captured at 1440 px and looked at; chapter 08 sampled at 390 px. A script measured each stage against its content: the only plates wider than the 1440 column are true-size pieces that must be (the 1440 masthead, L6 at 884 px in the lockup sheet, the 1200 px cards), and the shell scrolls them inside their frames.
- The letterhead PDF with `pdfinfo`: 2 pages, 612 by 792 pt.

## Not tested

- The PDF on paper, and its scale with a ruler.
- Screen readers by ear; Firefox and Safari; Windows and macOS rendering.
- Keyboard order past the check's first 60 Tab stops, so the composer's order was checked by script only.
- Readers: whether the stage shapes, routes and corners decode without the key. No person has seen them (DR-68's reader check does not include them).
- Feed sizes for avatars are a design judgment; I read no platform's specification.
- `dataviz_check.js`: the shell notes replace it for guide pages with `guide_check.js`, and it has no exemptions for labeled failures.

## What I could not finish

- L4 to L7 as masters. They are assembled from masters on V5's layouts, and their minimums come from the I8 table.
- The coded Signal Grid drawings live in `stage_a_identity_lib.py` (`sgrid`). They are not yet cut as SVG files for the asset package.
- The hinge motion's still frame waits for chapter 17, as the map moves the motion there.

## Change log

Created:
- `work/build/guide/chapters/03-identity.json`, `04-ampersand.json`, `08-signal-grid.json`, `proofs.json`
- `work/build/guide/specimens/`: 57 chapter specimens (`s-03-*`, `s-04-*`, `s-08-*`), 11 proofs (`s-proofs-*`) and `manifest-identity.json`
- `work/boards/phase-2/stage-a/proofs/20261106_Letterhead-Proof.html` and `20261106_Letterhead-Proof.pdf`
- `work/build/scripts/phase-2/`: `stage_a_identity_build.py`, `stage_a_identity_lib.py`, `stage_a_identity_s03.py`, `stage_a_identity_s04.py`, `stage_a_identity_s08.py`, `stage_a_identity_proofs.py`, `stage_a_identity_chapters.py`, `stage_a_identity_raster.js`
- `work/handoffs/phase-2/20261106_Stage-A-Identity-Notes.md` (this file)

Regenerated by running the engineer's scripts: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report, check results and captures.

Modified: none. Rebuild with `python3 work/build/scripts/phase-2/stage_a_identity_build.py --pdf`, then `python3 -I work/build/scripts/phase-2/guide_build.py`.

## Fix pass

Round one, November 6, 2026, under `work/handoffs/phase-2/20261106_Stage-A-Fix-Pass-Brief.md`. The identity designer (oa-design-director, as maker, a subagent of the main session) changed only its own build scripts, which rewrite chapters 03, 04 and 08, `proofs.json`, the `s-03-*`, `s-04-*`, `s-08-*` and `s-proofs-*` specimens, `manifest-identity.json` and the letterhead proof. No identity master, ledger, `source/` file or other maker's file was edited. A container restart came partway through; the edits on disk survived and the work resumed from them.

### Items, by ID

**Brand and evidence**
- BE-M4. The letterhead proof prints its width and one Illustrative line in the top margin of each sheet: "Today's width" on page 1 and "Condensed width, proposed" on page 2, each with "The address, recipient and letter are invented." The screen plate shows the same line. PDF rebuilt.
- BE-M5 and CP-M1. Every decision code and production word left my chapters, captions, specimens and alt text. Basis lines now read "Design judgment", "Our measurements, October 2026", "Rule 05.3, the red rule", "Dustin Cathcart's ruling on partners, November 6, 2026" or a WCAG criterion. Rule 04.5's basis drops "the five separation rules"; its rule text now states them in words. Rule 04.6 drops "the badge's three conditions". "R9" and "R13" are said in words. Codes stay in `notes` in the manifest.
- BE-M6 and CP-M4. Rule 04.3's correct plate sets three headlines from Rule 02.27's correct list: "The zoning code & the rent.", "The filing deadline & the ballot." and "The records law & the answer." The Act card reads "The route plan & your commute."
- BE-S8. "Atlas V7" is "our systems atlas"; specimen labels say "our fifth edition".
- BE-S9. Rule 03.5's basis is "Design judgment, measured against WCAG 2.2 SC 1.4.11 at rendered sizes; Rule 05.3 for red", and its why gives both reasons: red falls to 2.27:1 on Prussian once drawn at 16 px, and red on our dark blue reads as a pair of party colors.
- BE-S11. Chapter 03's minimum table shows today's width alone. The condensed minimums moved to a new readable table in the proofs, `s-proofs-minimums`, whose figures the build checks against the masters' table.
- BE-S12 and RP-S1. The email deck opens on the step: "Sign up with the board clerk by noon Monday to speak before the vote."

**Accessibility**
- AX-M1. `s-03-minimums` is `readable` and stacks on phones with each cell's column named. Rule 03.2's specifications give all eight lockups' minimums on screen and in print.
- AX-S5. The composer has no `width_px`, fills its column and switches to one column by container query under 560 px.
- AX-S8. Rule 03.6's navigation words sit in a `div`. None of my specimens holds a landmark element.
- AX-S9. `s-08-combinations` is `readable`, and Rule 08.4 says "A pillar corner shares its grid with nothing else."
- AX-S14. `s-proofs-glance`'s alt gives all three width pairs: 152 against 120 px, 221 against 181, 435 against 342.
- AX-S15. The composer's "take part now" checkbox carries `aria-describedby` to its reason while it is disabled, and drops it once enabled.

**Craft**
- C-M2. Rule 04.4's rule and specifications say B's 24 px master sits at the center of a 1 px line as wide as the text block it divides, with 12 px of clear line on each side, line and B in the surface's ink. Its plates draw exactly that.
- C-M6 (D2-251). Each pair is one comparison specimen at actual size, both widths labeled inside the stage, with ampersand B: `s-proofs-masthead` (site and phone bars, stacked on one left edge), `s-proofs-email` (side by side), `s-proofs-avatar` (side by side), `s-proofs-social` (stacked on one left edge) and `s-proofs-letterhead` (side by side). The wide four carry `fit_switch`. The ten single-width plates they replace were removed.
- C-M7 (D2-254). Type on fixed artboards takes the scale's sizes through a helper that reads each style's face, line height and tracking from the tokens: phone floor up to 600 px, desktop ceiling at 1,200 px. Labeled failures typed off the scale (03.1, 03.7, 03.8) and print pieces set in points (the 04.8 cover, the letterhead) carry `check_exempt` "scale" with the reason in `notes`. The typeScale check passes for every plate of mine at all four widths.
- C-S6. Every artboard keeps `width_px`; sheets of marks and tables leave it out and flow, since each mark prints its own size.
- C-S7. Cards and the link card are drawn at a phone column's 358 px, so they fit a 390 px phone at true size. Sheets flow and wrap. The lockup sheet runs as two columns at 712 px, with L5 across both, and L6 has its own plate at its 884 px minimum.
- C-S8. Every label is the shell's `<span class="illus">Illustrative</span>`, unstyled by my CSS: one at the head of a piece where all of it is invented, and beside the invented item where real and invented mix (the partner lockups, the page head, the letterhead).
- C-S9. Every visible string, alt and `aria-label` in my specimens, and the chapter text, runs through the editor's `curl()` from `guide_editor_common.py`. The scan finds no straight apostrophe in my files.
- C-S12. Looked, and declined the change pending Dustin; see question 1.
- C-S13. Each row of the minimum sheet sits on one bottom line: L3's lockmark now hangs equally above and below the wordmark's box. B's sizes in Rule 04.1 share one baseline, and the 16 px master shows as the pixels Chromium draws at 1x, enlarged four times with nearest-neighbor scaling, beside its outline on the grid.
- C-S14. Both social cards break the headline at the hinge: "The zoning code / & the rent."
- C-S15. All 25 of my rule titles were already instructions; no change.

**Civic and plain language**
- CP-M9 and RP-S8. The nine stages take plain names: Filed, Sent to committee, Hearing, Out of committee, Passed one chamber, Passed both chambers, Final text agreed, Signed, In effect. The tracker list and the readable stages sheet say once what each means. Rule 04.4's passage now reads "The committee votes on whether to report the bill out, which sends it to the full House."
- CP-S2. Each chapter's first mention is "our brand guide's fifth edition" (or fourth), then "our fifth edition". No "V5", "V4.2" or "Edition 05" remains in reader text.
- CP-S3. Rule 03.2's builders note drops "after Gate 2"; L4 to L7 files come from the editor until they are drawn.
- CP-S14. Rule 04.6: "Keep it off anything about a candidate or a ballot measure, where a seal-like mark could read as an endorsement."
- CP-S17. The letterhead's town is Wrenfield, so nothing joins it to Alder County.
- CP-S19. Rule 08.5's plate shows the tracker list first at 358 px, so a phone reader sees every bill and the testimony line without scrolling, then at 600 px.
- The letterhead opens "Please send us the approved minutes", and "accessory dwelling" is glossed as backyard cottages.

**Reader panel**
- RP-S3 with DR-102. Rule 03.8 says the host's name leads and shows both orders, gives print values (hairline 0.5 pt, 1.2x tall, 0.6x of space), sets L8 beside the partner for squares, keeps the partner's logo as drawn with "and" only in our own copy, and sends every co-branded piece to Dustin or an editor he names. Rule 03.3 says the hairline and the partner's logo belong to the lockup.
- RP-S4. The social card proof carries a seven-line specification list. The appendix names Dustin as the one who chooses.
- RP-S5. Rule 03.6 reads "From 48em wide, 768 px at the default text size", and its builders note gives the em media query.
- RP-M1 (D2-250). Every kicker follows Rule 01.21: "Explainer · Zoning" (social card), "Explainer · Local budgets" (email story), "Act · How to take part" (Act card), "Report · Dispatch" (Rule 08.8), "Report · Local budgets" (cover). Rule 08.8's text points to Rule 01.21.

### Routine calls, as proposed decision lines

- D2-xxx | Letterhead proofs sit side by side, not stacked as the fix pass brief lists | Side by side, both wordmarks sit on one line 72 px from the top; stacked, they sit 1,128 px apart, more than a 900 px window, which defeats the comparison D2-251 asks for
- D2-xxx | Proof labels read "Today's width" and "Condensed width, proposed"; the appendix is titled "Wordmark width proofs" | D2-253 keeps "Gate" off reader pages, and the labels still name which width is in force
- D2-xxx | Cards in chapters 04 and 08 are drawn at 358 px, a 390 px phone's column | They fit a phone at true size (C-S7) and take the phone floor's sizes (D2-254)
- D2-xxx | Sheets of marks and reference tables leave out `width_px` and flow; artboards keep it | Each mark in a sheet prints its own size, so a sheet width would claim nothing (C-S6)
- D2-xxx | Tracker stages take plain names, with one line on each stage's meaning per tracker page | A newcomer reads the key without the legislative terms (H02, CP-M9)
- D2-xxx | The social card sets its kicker in the H4 style at 24 px, its headline in the title style at 110 px, 72 px margins, and no deck | Every size is on the desktop ceiling; a deck at the body size would be unreadable at feed size
- D2-xxx | The two-email proof uses only sizes both type sets share: 24 px headline, 17 px body, 13 px kicker | The pair is 1,280 px wide, so the check reads it against the desktop ceiling, while each email is a 600 px piece
- D2-xxx | L6 has its own plate at its 884 px minimum | Its minimum is wider than the guide's column, and the sheet stays readable at 712 px
- D2-xxx | The display lockmark's file, `20261028_Lockmark-Master-V5.svg`, leaves the Files lists of Rules 03.6 and 08.1, and the builders note says to ask the editor for it | Its name holds "V5", which D2-253 keeps off reader pages; the asset package should rename it, for example `Lockmark-Display-Master.svg`
- D2-xxx | `<title>` and `<desc>` are stripped from SVG files my build inlines itself (the taglines, the Lora record, the letterhead PDF); the files keep them | Their record notes held "V5" and "Phase 2" and reached the page
- D2-xxx | The letterhead's town is Wrenfield, Massachusetts, invented | CP-S17: it cannot be joined to Alder County

### Questions for Dustin

1. **The badge as an article's end mark.** At 16 px after a period, the badge, B in a ring, reads close to a registered sign (®). I set the two side by side and looked; a reader skimming would take it for a trademark. Its end-mark job was approved by name with the badge's conditions, so Rule 04.6 still teaches it. *Recommendation:* end an article with B alone at the text's cap height, in the text's ink, and keep the badge for back covers and events from 48 px.

### Seen, not changed

- The lockmark at 40 px, the anchor size Rule 08.2 sets, comes from the 24 px master scaled up, and at twice size its nodes look blocky (social card proof, composer). Setting the anchor at 48 px from the display master, or drawing a 40 px master, would fix it. It touches the masters' size ranges, so it waits for a ruling.
- The full guide check's four failures all sit in `s-01-5-correct` and `s-01-5-failure`, the editor's map, at 390 and 360 px.

### Tested

- `python3 work/build/scripts/phase-2/stage_a_identity_build.py --pdf`: 65 specimens, 3 chapters, the proofs file and the PDF, no errors; ten stale proof files removed.
- `python3 -I work/build/scripts/phase-2/guide_build.py`: 8 chapter files, 99 rules, 229 specimens, 0 warnings.
- `node work/build/scripts/phase-2/guide_check.js ... --quick` (1440 and 390 px): pass, 0 failures. The full run on the final build (1440, 1024, 390, 360 px): 4 failures, all in the editor's `s-01-5` map plates at 390 and 360 px (state labels at 11.81 and 10.72 px); none in chapters 03, 04, 08 or the proofs, including the new codes, nameEntities, typeScale and specimenLandmarks checks. Exemptions of mine listed: `s-03-1-failure`, `s-03-7-failure` (contrast, scale), `s-03-8-failure`, `s-04-8-correct`, `s-04-8-failure`, `s-proofs-letterhead` (scale), `s-04-3-failure`, `s-04-4-failure`, `s-08-4-failure` (red).
- Every plate of mine captured at 1440 px and at 390 px (twice size), and looked at: all proofs, the lockup sheet, the minimum sheet and table, 03.6, 03.8, 04.1, 04.3, 04.4, the Act cards, 08.5 and the composer. Detail plates also at twice size at 1440: 03.4, 03.8, 04.1, 04.4, 08.8, the glance and the avatars. These looks found and fixed L3 riding 7 px high in its bar, the lockmark's line box, a partner name that stood taller than our capitals, label margins, the stacked table caption and an unpadded sheet.
- A script scan of my specimens, alt texts and chapter JSON: no em dash, no straight apostrophe, no decision code or banned word, no landmark element.
- The letterhead PDF with `pdfinfo` (2 pages, 612 by 792 pt) and `pdftotext`, and both pages rendered at 90 dpi and looked at: each carries its width and the Illustrative line in the top margin.
- The badge beside a registered sign at 16 px, rendered at 1x and 2x, looked at.

### Not tested

- The PDF on paper, its scale with a ruler, and whether a home printer clips the top-margin line at 0.27 in.
- Screen readers by ear; Firefox and Safari; real phones.
- The fit-to-window switch beyond seeing it in the plate head; the engineer owns it.
- The composer by keyboard and screen reader after this pass; its `aria-describedby` change was read in the source, not heard.
- Any reader on the plain stage names or the badge question.
- The last three small fixes (the pad on Rule 04.4's sheet, the stacked table caption, the unused CSS rule) passed the full check but were not captured and looked at again.

### Change log

Modified (all mine):
- `work/build/scripts/phase-2/stage_a_identity_lib.py`, `stage_a_identity_s03.py`, `stage_a_identity_s04.py`, `stage_a_identity_s08.py`, `stage_a_identity_proofs.py`, `stage_a_identity_chapters.py`, `stage_a_identity_build.py`, `stage_a_identity_raster.js`
- Regenerated by them: `work/build/guide/chapters/03-identity.json`, `04-ampersand.json`, `08-signal-grid.json`, `proofs.json`; `work/build/guide/specimens/manifest-identity.json` and every `s-03-*`, `s-04-*`, `s-08-*` and `s-proofs-*` fragment; `work/boards/phase-2/stage-a/proofs/20261106_Letterhead-Proof.html` and `.pdf`
- `work/handoffs/phase-2/20261106_Stage-A-Identity-Notes.md` (this section)

Created: `work/build/guide/specimens/s-03-l6.html`, `s-proofs-masthead.html`, `s-proofs-email.html`, `s-proofs-avatar.html`, `s-proofs-social.html`, `s-proofs-letterhead.html`, `s-proofs-minimums.html`.

Removed (replaced by the pairs): `s-proofs-masthead-today`, `-condensed`, `s-proofs-email-today`, `-condensed`, `s-proofs-avatar-today`, `-condensed`, `s-proofs-social-today`, `-condensed`, `s-proofs-letterhead-today`, `-condensed` (`.html`).

Regenerated by running the engineer's scripts: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report, check results and captures. Nothing committed or pushed.
