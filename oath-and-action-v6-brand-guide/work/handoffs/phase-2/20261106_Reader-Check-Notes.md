# Reader check page: notes

Oath & Action Edition 06, Phase 2, November 6, 2026. Maker's notes from the UX and accessibility lead, for the main session. Brief: `work/handoffs/phase-2/20261106_Reader-Check-Brief.md` (DR-68, DR-84 to DR-87). Nothing here is published, committed or pushed.

## What I built

A private test page for five or more first-time readers on their phones. It tells them only that this is a short test of a draft design for a civic publication. No brand name appears in the page's own words; the wordmark appears only inside the two stimuli that test it (the 16 px sheet and the mastheads).

- **Page:** `work/boards/phase-2/reader-check/20261106_Reader-Check.html`, content only, since the publish step wraps it in the skeleton. Images in `img/` by relative path (31 files, 3.1 MB).
- **Source:** `reader_check_template.html` plus `build_reader_check.js`, which captures the stimuli from the boards, writes the vector stimuli, injects the configuration and writes the answer key. Run `node work/boards/phase-2/reader-check/build_reader_check.js` from the project root (`--no-capture` reuses the captures).
- **Answer key:** `20261106_Reader-Check-Answer-Key.json`. The page never carries it.
- **Tests:** `test_reader_check.js` walks the whole flow with a stub `window.claude` in five modes. Results in `20261106_Reader-Check-Test-Results.json`; captures in `captures/`.

### The flow: 8 steps, 54 screens, about 9 to 10 minutes

| Step | What the reader does | Timed looks |
|---|---|---|
| 1 Welcome | One paragraph (what, how long, what we record, stop any time), the mode sentence, a first name or initials, Start | none |
| 2 Drawings | The overview's first two phone screens, then 2 questions; the R10 close-up and R8, in random order, 4 questions each | 3 at 10 s |
| 3 Symbols | Eight Civic Line icons at 48 px, black on Newsprint, in random order; "What do you think this symbol stands for?" | 8 at 10 s |
| 4 Small marks | A sheet of nine marks at true size; then clear, blurry or can't tell for each | 1 at 10 s |
| 5 Charts | S02, S11, S14 in random order; one sentence on what it tells you; does it favor a party or side | 3 at 15 s |
| 6 Sentences | W02, W10, W11, each pair as A and B in random order; which is easier to follow | none |
| 7 Mastheads | L3 at today's width and condensed, as A and B in random order, together; which reads faster, and an optional why | 1 at 10 s |
| 8 End | Thanks and what happens next; in copy mode, the answers with a Copy button | none |

Fixed looking time is 175 seconds. With 38 answers (12 typed, 26 tapped) and the opening screens, I estimate 9 to 10 minutes for a careful reader and about 7 for a quick one.

### Fair timing

- The reader starts every look: each kind of stimulus has an opening screen, and the next symbol or chart starts from the reader's own Next tap.
- The clock starts only after every image in the look has loaded and decoded, and it counts only while the page is visible. A reader who takes a call mid-look gets the rest of it on return.
- The header shows "8 seconds left" and a draining line; under reduced motion the line goes and the words stay.
- Every question that follows a look has **Show it again**, which reruns the full look and offers "Back to the question" to end it early. The record counts each use and its seconds. Answer times exclude re-shows and hidden time.
- A failed image says so and offers Try again or Skip it, and the record counts it.
- A reload offers "Pick up where I left off". A look cut off by the reload is counted as interrupted and starts again from the top.

### Saving

The page asks `claude.use("db")` and `claude.use("user")`, then `user.id()` and `user.can("data.write")`. With all of them it is in **saved** mode and tells the reader "This page saves your answers as you go." Otherwise it is in **copy** mode and says so in one sentence. Each reader writes one document, `responses/<id>`, holding `runs: { <run id>: run }`, so a second attempt never overwrites the first. The first write is a `set` when the document is absent and an `update` otherwise, with a 10 s limit on the first read and the first write. Writes go one at a time, after every answer, with a change made during a write sent next. A rejected write, a revoked grant or a timeout switches the page to copy mode with one plain line, and the end shows the copy text. `unavailable` retries once after a random short wait; `resource_exhausted` waits for the next answer. The page never reloads itself.

In copy mode the end screen shows the answers as readable lines and one JSON line, with "Copy my answers". When the frame refuses the clipboard, the page selects the text and says to use the phone's Copy.

## Routine calls (proposed decision lines)

Numbers left for the main session to assign.

- D2-xxx | The third loop is R8, drawn by System 1 on its "All loops" view, as the brief asks when the page draws it. B4 is set up in the build script as a one-line swap (`THIRD_LOOP`) | The brief names R8; the cost is below under "Decide before publishing"
- D2-xxx | The loops show as drawn and alone: R10's close-up with R-01's targets in red, R8's catalog card with no reform marks, and no key | The brief asks for the drawings; the "where does a reform act" question then tests whether red reads as a reform with no key beside it
- D2-xxx | The loop order is random per reader, and both loops get the same choices, including "They look about the same", "No reform is shown" and "Not sure" | Readers learn the four questions on the first loop; random order spreads that across both, and identical choices cue neither answer
- D2-xxx | The loop questions avoid the word loop: "Do the arrows come back to where they started?" and an opening screen titled "The next drawing" | Calling it a loop answers the first question
- D2-xxx | The step and reform choices quote the drawing: "3. lowers" over "Risk of losing office → Incumbents control election rules"; R8's unnumbered arrows are "Top arrow, raises" and "Bottom arrow, raises" | The brief asks for the words printed on the drawing; the box names say which arrow is which
- D2-xxx | The overview look is the overview's first two phone screens (kicker, headline, deck and whole-system drawing) without the wordmark, tabs or breadcrumb; readers may scroll | The fix-pass ten-second rule holds on a phone within the first two screens
- D2-xxx | The four topic icons are CL-015 Political Money (sheet 01), CL-032 Local Reporting (02), CL-063 Essential Costs (03) and R-02 Ranked-Choice Voting (04) | One from each of the set's other families, each tied to a part or reform the atlas names
- D2-xxx | Icons, marks and mastheads ship under neutral names (icon-1 to icon-8, mark-1 to mark-9, masthead-1 and -2) with titles, descriptions and ids stripped, and the icons show in random order | The master files' titles and names would tell a reader the answer
- D2-xxx | The 16 px sheet carries both wordmark widths, so it holds nine marks | Readers then meet both widths before the masthead question, and the condensed 16 px master gets a reading for DR-71
- D2-xxx | The rating rows repeat each mark at true size, 16 px | Rating nine small marks from memory is unreliable, and a larger reference would show readers what the small one is
- D2-xxx | The 16 px marks are one color, Charcoal, ampersand, lever and lattice included | R10 of DR-67
- D2-xxx | Charts show for 15 seconds | Charts need longer than marks (brief, step 5)
- D2-xxx | A chart look is the figure as a phone reader meets it first: evidence line, title, measure line and the phone drawing. Notes, source line and table toggle stay off. S02 comes from Explainer's Newsprint view | The title carries the finding by design and was the subject of DR-65's leaning review; the notes would push the drawing past 15 seconds
- D2-xxx | Charts and atlas drawings are captured at 390 and 360 px, twice size, and the page picks by screen width, never scaling up | Chart text holds its 14 px phone floor on phones from 360 px
- D2-xxx | W10 replaces the brief's W05 | W05's county is invented, so house rule H03 would put an Illustrative label beside that one pair only
- D2-xxx | Pair order is fixed (W02, W10, W11); A and B are random within each pair | The brief asks for random A and B
- D2-xxx | Both mastheads use one scale, 0.17 px a unit (217 and 182 px wide, both 41 px tall), with signature red as the masters draw it and no other chrome | The minimum-size table sets both widths at one scale; Rule 05.3 does not count the ampersand's or the lever's red
- D2-xxx | The page keeps one light look on Newsprint in every phone theme | Every reader sees the stimuli on the same ground
- D2-xxx | Each stimulus image carries alt text that identifies it without the answer ("Symbol 3 of 8") | WCAG 1.1.1's exception for tests
- D2-xxx | A first name or initials is required to start; every question can be skipped, and an empty Next asks for an answer or a skip | Each record needs a name to tell readers apart; a stray tap should not skip a question
- D2-xxx | The page saves after each answer, not after each step | A reader who stops halfway leaves every answer given so far
- D2-xxx | Unfinished runs resume from browser storage on the same phone | Phones often reload a tab after a call or an app switch; storage holds only this reader's own draft
- D2-xxx | The page sets `lang="en"` by script | The publish skeleton's `html` tag has none (WCAG 3.1.1)
- D2-xxx | Two page-local tokens, `--press` (Newsprint 6% toward Charcoal) and `--track` (12%), plus `--ink-hover` | Hover and the progress track; they live in this page only and are not proposed for the token file
- D2-xxx | The brief's `npm install --no-save axe-core@4.10.2` removed Style Dictionary 5.8.0 (D2-157) from `work/build/node_modules`; I reinstalled both in one command | npm prunes packages it was not asked for; future briefs should name both: `npm install --no-save axe-core@4.10.2 style-dictionary@5.8.0`

## Decide before publishing

1. **Who can save.** Saving needs the Contributor level (`interact`). Readers outside Dustin's organization, by link or email invitation, hold `view` and land in copy mode; signed-out readers too. An outside reader can write only as an Editor, which also lets them read every `responses/` document. For strangers, copy mode is the likely path: Dustin shares a link and readers send back the text. If saved answers matter, Dustin should share with organization members at Contributor.
2. **R8 or B4.** R8 and R10 both feed themselves, so a reader who always answers "feeds itself" gets both right, and R8's honest answers to two questions are "about the same" and "no reform is shown". B4 pushes back and would separate readers who read the signs from readers who guess. Swapping is one line and a rebuild.
3. **Pillar marks at 16 px.** Civic Line has no 16 px drawing of the pillar marks; m6 to m9 are the black edition scaled below the set's 32 px floor (D2-42), with strokes near 0.4 px. Expect "blurry", and read it as a known floor rather than a finding.
4. **Publish only the page and `img/`.** Keep the answer key, template, scripts, results and captures out of the artifact.

## Answer key, in short

- Overview: what the page is for passes when it names who officials answer to, or how economic and public life connect. "Open first" has no right answer.
- R10: comes back, yes; feeds itself; least certain is step 3 (L53, plausible, drawn dashed and labeled "weakest step"); a reform acts at "Seats settled in the primary" (R-01 targets L08, L25 and C2), with the two neighboring boxes as partial.
- R8: comes back, yes; feeds itself; the two steps look the same (both well supported); no reform is shown.
- Icons: i1 Local Reporting (CL-032), i2 Track (CL-020), i3 Act (CL-022), i4 Ranked-Choice Voting (R-02), i5 Explain (CL-019), i6 Essential Costs (CL-063), i7 Connect (CL-021), i8 Political Money (CL-015). Pillar meanings follow voice line B (DR-76).
- Marks: m1 wordmark today, m2 wordmark condensed, m3 ampersand B, m4 lockmark, m5 hinge-circle badge, m6 to m9 Explain, Track, Connect and Act.
- Charts: each one's title, finding and evidence grade; the intended answer on bias is no.
- Pairs: the after is expected to read easier.
- The record's fields are described in the key's `record_fields`.

## Tested

RESULTS

## Not tested

- The real claude.ai viewer, its `db` and `user` capabilities and its access levels. Every saved-mode result comes from the stub.
- Real phones: iOS Safari, Android Chrome, the Claude apps, a real 3x screen, an app switch or call mid-look on a real device.
- The clipboard inside the artifact frame.
- Screen readers (VoiceOver, TalkBack) and voice control.
- The viewer's live-update hook (`hot`), which the page registers but this environment cannot exercise.
- Browser text zoom at 200 percent on a phone; the 320 px reflow run stands in for it.
- How long real readers take; the 9 to 10 minute figure is an estimate.

## Change log

Created, all in `work/boards/phase-2/reader-check/` unless named:
- `build_reader_check.js`, `reader_check_template.html`, `test_reader_check.js`
- `20261106_Reader-Check.html`, `20261106_Reader-Check-Answer-Key.json`
- `img/` (12 PNG captures, 8 icon, 9 mark and 2 masthead SVGs)
- `20261106_Reader-Check-Test-Results.json`, `20261106_Reader-Check-Check-Results.json`
- `captures/` (the 390 px walk, one or more per step, in both modes)
- `work/handoffs/phase-2/20261106_Reader-Check-Notes.md` (this file)

Modified: none in the repository. Outside it, `work/build/node_modules/` (not tracked, D0-05) lost and regained Style Dictionary 5.8.0 as described above. Nothing in `source/`, the ledgers or any other board was touched. Nothing was committed.
