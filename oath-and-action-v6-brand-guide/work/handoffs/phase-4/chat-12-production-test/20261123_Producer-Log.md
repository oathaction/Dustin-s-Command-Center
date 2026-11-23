# The simulated producer's log (chat 12, production reader)

A staffer at a partner organization who builds one web page a month, working only from chapters 16, 20 and 21, chapter 18 and the kit's own file headers. Every step, every place looked and every guess is logged here, in order. Simulated; no real producer was tested.

## Task 1: a new atlas reform page from chapter 21 alone

### The selection rule, written at 17:15 UTC, before looking at any reform

1. Read the four views' domains from chapter 21's words alone (the home question, Reform R-23, the Register's sheet D04, Loop R18 with Reform R-11).
2. List every reform in the atlas model in ID order (R-01, R-02, ...).
3. Take the first reform whose domain is none of the domains found in step 1. Do not read any reform's title, summary or remedy before taking it. Do not skip a reform for its subject, its side or its grade (DR-55 as DR-94 restates it; DR-93: no counterweight, no choice made to even a score).
4. If chapter 21 does not say what a reform's domain is, or how to find it, log that as a gap and use the model's own field for a reform's domain.

### Applying the rule (17:17 UTC)

- Step 1 from chapter 21's words: the views are the atlas home (the question "Why can the same care produce different bills?"), Reform R-23, the Register with sheet D04 open, and Loop R18 with Reform R-11 chosen. Chapter 21 names the domains only in Rule 21.8 ("Domains D01 to D10"), and gives no way to find a reform's domain. **Gap 1:** chapter 21 never says which domain a reform belongs to; a reform has targets, and Rule 21.9 files a target's connection "by the variable the connection moves; ... one with two domains on the first". **Guess 1:** a reform's domains are the first domains of its targets' variables (a connection target counts by the variable it moves), read from the model, `work/extract/atlas-v7-data.json`.
- Domains the four views show, read from the model with that guess: the home question (pathway PW06's variables) reaches D04, D05, D06, D08, D09, D10 and the economy layer; Reform R-23 acts in the economy layer and D08; the Register shows D04; Loop R18 runs through D04 and D05, and Reform R-11 targets D04 and D05. Shown: D04, D05, D06, D08, D09, D10 and the economy layer. Not shown: D01, D02, D03, D07 and the technology layer.
- Step 2 and 3: in ID order, Reform R-01's targets all file on D02. **Chosen: Reform R-01**, taken by the rule before reading its title, summary or grades. (DR-223: R-01 is handled like every other reform.)

### Finding how to make the page (17:16 to 17:30 UTC)

| Step | Where I looked | What I found | Guess or gap |
|---|---|---|---|
| 1 | Chapter 21, its intro, Rules 21.1 to 21.16 and How to read | What a reform page holds and in what order (Rule 21.4), the chips (21.6), the evidence links (21.7), the test (21.16) | **Gap 2:** no word on how to make a page: no content file, no command, no kit |
| 2 | Chapter 18 | The components the page uses (chips, disclosures, stepper) | Nothing on the kit |
| 3 | A README for the application kit | None in `work/build/app-kit/` (the chart kit has one) | **Gap 3** |
| 4 | `oa-app.mjs`'s header | The command, `node work/build/app-kit/oa-app.mjs build [ID...] [--out DIR] [--exports DIR] [--date YYYYMMDD]`, and "content file (specs/<id>-*.json)" | The header lists no content keys for an atlas page; `--spec-dir` and `--plates` work but the header does not name them |
| 5 | `renderers/atlas-page.mjs`'s header | Templates: home, reform, register, loop, loop-index, how-to-read; "every word the page adds from chapter 21's generator (phase4_ch21_build.py --page-words all)" | **Gap 4:** a page's words live in the studio's chapter 21 generator, keyed by application ID; a partner has no place to write them |
| 6 | `specs/a12-atlas-reform.json` | The nearest model: id, type, view "reform", record, panels, remedy_split 4, widths, views, export_name, alt | **Guess 7:** a new page is a copy of A12's file with a new id (A21) and record (R-01). **Guess 8:** `remedy_split` names the sentence where R-23's contested remedy splits; nothing says how to choose it for R-01, so I removed it |
| 7 | The application ID | Chapter 21 and the kit say nothing about numbering | **Guess 9:** A21, the next free number; chapter 22's applications may want it |

### Drawing the reform page (17:35 to 17:39 UTC)

All runs in the production reader's scratch copy, under the build lock, with `--spec-dir`, `--out`, `--exports` and `--plates` pointed at scratch folders, so nothing reached the repository.

| Run | What I ran | What happened |
|---|---|---|
| 1 | `node work/build/app-kit/oa-app.mjs build A21 --spec-dir ... --date 20261123` with `a21-atlas-reform-r-01.json` (this folder) | Stopped: "the atlas page words hold no entry for A21 (contract C9)". A partner cannot go further without writing into the studio's chapter 21 generator |
| 2 | The same, with `"of": "A12"` added. **Guess 15:** I found the key in A17's content file and in `render()`'s code, not in any header: a page that is a state of another takes that page's words | The kit drew the page and its four exports, then stopped: "ENOENT ... pplates/web-site.css". **Gap 7:** `--plates` must name a folder that already holds the kit's styles; a fresh folder fails after the drawing |
| 3 | The atlas test on run 2's output: `python3 -I work/build/app-kit/tools/atlas_test.py OUT --plates PLATES --ids A21` | 168 PASS, 24 FAIL: T2 and T6 on every view ("found nothing to check on a reform page, which must hold it") and T10 ("the remedy prints in 1 blocks, two asked (R15)"). The test stopped the page, as Rule 21.16 says it must |

What the drawn page shows (`20261123_Producer-Test-Atlas-Reform-R-01-Page-1440-Light.png` in the scratch exports):

- The tab title reads "Reform R-23, Minimum wage that rises with an index | Who Do They Answer To? | Oath & Action" on Reform R-01's page, since the words came from A12. The atlas test passed it: T15 checks the title's three parts, not that the first names the page's own record.
- "Where it acts" has no drawing. Its note names one target, "Variable C2", where R-01's record names three (Variable C2 and Connections L25 and L08), and two lines below say "the drawing leaves it out" of a drawing the page does not hold. The figure step draws a reform only when its targets are exactly two variables joined by one connection (`atlas_figures.py`, `view_reform`), which 12 of the atlas's 50 reforms are; 33 of the 50 name a connection among their targets, and the renderer prints only the variable targets (`atlas-page.mjs`, `tv = v.targets.filter((t) => 'part' in t)`).
- R-01's remedy is graded plausible and contested, so Rule 21.4 asks for its two readings side by side. The content file's `remedy_split` sets where the stored text splits, and no rule or header says how to choose it, so it printed whole (T10's failure).
- The status panel reads "As of October 15, 2026" and then the stored text, which itself begins "As of October 15, 2026, two measures ...". 15 of the 50 reforms' stored statuses begin "As of".

What chapter 21 did not tell me: how to make a page at all (content file, words, command, application number), a reform's domain, how a contested remedy's split is chosen, and that the reform page draws only one shape of reform.

## Task 2: a new article page from chapter 20 alone

| Step | Where I looked | What I found | Guess or gap |
|---|---|---|---|
| 1 | Chapter 20, Rule 20.7 and its specifications | The article's order: compact pillar row, kicker, headline that answers the question, intro, byline, count panel, body at five of 12 columns, fact box, chart whole, the step on a Charcoal box ending on B | **Gap 5:** nothing on how to make one with the kit |
| 2 | Choosing the chart | Rule 20.7 names S86 only | **Guess 10:** chart S04 (reported voting by age), which chapter 16's video plates print; its facts and source line read from the chart kit's `s04.json`, which is outside chapter 20 |
| 3 | `renderers/web-site.mjs`'s header | "Content keys (layout only; words come from the generator)"; the words from `phase4_ch20_build.py --page-words`, "until it exists, the file OA_PAGE_WORDS names" | **Gap 6:** the content file holds no words. A page's words must be added to the studio's chapter 20 generator, or the generator hidden so the kit reads a stand-in file |
| 4 | The words' form | Not written anywhere a producer reads; I printed A07's with `--page-words A07` | **Guess 11:** a new article's words take A07's keys (title, current, kicker, symbol, headline, intro, byline, count, sections, count_fact, def_source) |
| 5 | The kicker's icon | A07 uses `cl-031`; chapter 20 names no icon for an Elections kicker | **Guess 12:** left out, to see whether the kit needs one |
| 6 | The count panel | Rule 20.7 lists a count panel for the article | **Guess 13:** every article has one; I set S04's 27 point gap |
| 7 | The chart's sizes | A07's content file gives S86 `[621, 328]` | **Guess 14:** the same column sizes serve S04 |

### Drawing the article (17:41 to 17:47 UTC)

| Run | What I ran | What happened |
|---|---|---|
| 1 | `node work/build/app-kit/oa-app.mjs build A22 --spec-dir ... --date 20261123` with `a22-web-article-s04.json` (this folder), the studio's generator in place | Stopped: "the generator prints no words for A22" |
| 2 | The same, with the chapter 20 generator moved aside in my scratch copy and `OA_PAGE_WORDS` naming my words file (`a22-page-words.json`, its site words copied from A07's). **Guess 16:** this is the only way the header leaves a partner, and it means hiding the studio's own file | Drawn: six views and the working page, 7 exports, exit 0. No icon was needed for the kicker (Guess 12 held) |
| 3 | `python3 -I work/build/app-kit/tools/export_checks.py OUT EXPORTS` (named in `oa-app.mjs`'s header) | FAIL on every light view: the Count section's opening screen holds no dark panel, Newsprint 94.1 percent at 1440 (92.4 at 1024, 87.7 at 390, 86.6 at 360), past Rule 05.1's 85. The first screen, the Step section and the footer pass; contrast's lowest 5.49 to 1; no working red. My Guess 13 left out the fact box, which Rule 20.7 lists, so the check caught a fault of mine, and Rule 20.9 says what to do ("move a panel before you add one") |
| 4 | Run 2 again with a fact box in my words file (S04's 47.7 percent for citizens 18 to 24) | See the result below |

What the article taught: chapter 20 gives every part of an article and its sizes, and the kit's checks hold a producer to Rule 20.9. What it did not tell me: how to make a page with the kit, where a page's words go, which icon an Elections kicker takes, and that the fact box is what keeps the Count section's opening screen inside Rule 05.1.

## Task 3: a photograph to commission and a video, from chapter 16 alone (17:30 UTC)

The files are `20261123_Producer-Commission-Photograph.md`, `20261123_Producer-Placeholder-Frame.html` and `20261123_Producer-Video-S66.md`, with their guesses numbered inside them. What chapter 16 did not tell me:

- The rotation log for settings (Rule 16.1 points to chapter 01).
- Whether a machine test's marked test ballots count as "marked ballots" (Rule 16.6).
- An article photograph's display size (Rule 16.8 says "display size" and gives none).
- A license line for commissioned work, and a file name pattern for a photograph (Rule 16.9 gives one for a generated image only).
- The token values behind the token names it prints (the placeholder frame uses my guesses for Newsprint and Charcoal).
- Which charts a video may use and where their source lines are (only S04 is named).
- The title frame, end frame and name plate: "Chapter 23 draws" them, and chapter 23 is not built.
