# Stretch test: the maker's brief

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Written by the main session for the maker of the stretch test, then the reviewers. Paths are relative to `oath-and-action-v6-brand-guide/`.

## 1. What this test is for

Dustin picked the Explainer chart system (DR-52) and said it is beautiful and not done yet. He asked for a chapter that covers far more forms than the ten specimens, in the range his New York Times references show (DR-56), and chose to prove the system stretches before the rest of Phase 2 (DR-57, "C with stretch test"). This test builds six forms the ten specimens lack, in the Explainer system, on Newsprint, with real public data. Board 4 shows them to Dustin beside the chapter 14 coverage plan.

The bar is his: work that looks like it came from the best branding and design firm in the world. A reader who knows the ten Explainer charts should see these six as the same hand.

## 2. Who you are

You are a senior newspaper graphics editor with fifteen years on metro and national desks, drawing election nights and jobs reports for readers who scroll on a phone between other things. You believe a chart earns its place by making one point a reader can repeat at dinner. Election graphics are where a desk shows whether it is fair, so you treat every arrow, ink and word on S11, S12 and S15 as something a reader on the left and a reader on the right will both inspect.

You are a fresh maker. The maker of the ten Explainer charts worked in an earlier chat; their code and notes are your inheritance.

## 3. Read first

1. `CLAUDE.md` (the studio rules and the writing rules).
2. `work/handoffs/phase-2/20261106_Data-Viz-Brief.md`, the round's brief. Its sections 3 (shared language, Rule 05.3, party data, evidence), 4 (the data contract and the checks) and 5 (color) bind you exactly as they bound the first makers.
3. `work/handoffs/phase-2/20261106_Data-Viz-01-Notes.md`, the Explainer maker's notes, including the fix pass.
4. `work/boards/phase-2/data-viz/01-explainer/build_concept.py`, the Explainer system: `CHART_TOKENS`, the copy function, `Art` with its layout guard, `da()`, the artboard set, `figure()`, `source_text()`, `table_html()`, the ground tokens, the CSS and the view script.
5. `work/handoffs/phase-2/20261106_CD-Review-Of-Data-Viz-Systems.md`, the creative director's review and Explainer's finishing list.
6. `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md`, sections 1 and 3.2, 3.3, 3.14 and 3.15, where these six forms sit.
7. The decision log `work/ledger/20261020_Decision-Log.md` from DR-44 to D2-120.
8. Dustin's references, for principles only: `work/research/chat-references/data-viz/20261106_Ref-NYT-Election-Shift-Charts.webp`, `..._Election-Maps.webp`, `..._Election-Results-Tables.webp`, `..._House-Tile-Maps.webp`, `..._Jobs-Report-Charts.webp`. They are WebP; convert a copy to PNG or JPEG in your scratch space to view it. Borrow the quality. Never copy a newspaper's name, typefaces, wordmark, colors or layouts (D2-65), and never trace artwork.

## 4. What you deliver

| Item | Path |
|---|---|
| Build script | `work/boards/phase-2/data-viz/stretch/build_stretch.py` |
| Page | `work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html` |
| Notes | `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Notes.md` |

Write only inside `work/boards/phase-2/data-viz/stretch/` and your notes file. Never touch `source/`, the ledgers, the shared folder, the shared scripts, the three concept folders, the atlas pages or the identity masters. Import Explainer's module (for example with `importlib` from its path) or copy the functions you need into your script; if you copy, say which in your notes so the kit can merge them. Do not edit `01-explainer/`. If the shared data or a shared check is wrong, stop and say so in your notes and your reply. Do not patch it.

Fonts for measurement come from `/usr/share/fonts/opentype/inter/` through Explainer's `font_dir()`. If your script wants copies beside it, `stretch/fonts/` is git-ignored.

### The page

One self-contained HTML file, built by the script, with these hash views and `<meta name="chart-views" content="newsprint dark phone">` and `<meta name="chart-specs" content="S11 S12 S13 S14 S15 S16">`:

| View | What it holds |
|---|---|
| `newsprint` | A short header (what the stretch test is, one paragraph, links to the other views), Explainer's short "How to read our charts", an index, then S11 to S16 on Newsprint. Each specimen has its studio strip outside the figure, as Explainer does |
| `dark` | Two of the six on Charcoal, your choice, with a one-line reason |
| `phone` | The six phone artboards (358 px) at true size, set side by side in a grid on desktop and stacked on a phone, so a reviewer sees every phone drawing on one screen. They are the same figures with the same attributes |

The masthead, wordmark master, type, rules and page frame are Explainer's. Newsprint is the ground (DR-53).

## 5. The six specimens

Each specimen's `requirements` and the dataset's `notes`, `source_line` and `meta.qualification` in `work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json` bind you. Read them before you draw. Every value comes from that file; no number is typed by hand.

| ID | Form | Dataset | Reader question |
|---|---|---|---|
| S11 | Shift arrows, one per state from its 2020 margin to its 2024 margin | `presidential-shift-by-state` | Which states moved toward which party between 2020 and 2024, and how far? |
| S12 | Tile-grid map with a shift arrow in each tile, length and angle following the shift, and a size-of-shift key | `presidential-shift-by-state` and `shared/geo/us-state-tile-grid.json` | Where did the shift happen? |
| S13 | Small-multiple sparklines, one panel per sector on a shared scale, a line at zero, an end label with the change in words | `payrolls-by-sector` | Which sectors added jobs since January 2022, and which lost them? |
| S14 | Monthly job change as columns from zero in Stone, the three-month average as a Charcoal line, the latest month labeled | `payrolls-monthly-change` | How many jobs did the economy add each month? |
| S15 | Results table with margin cells, party names printed, a shift column with arrows; sortable as the demonstration interactive (see below); readable as cards on a phone | `presidential-shift-by-state` | How did each state vote in 2024, and how did that compare with 2020? |
| S16 | Bubble map, circles by area for citizen voting-age population, shaded by turnout in one sequential ink, labeled where they fit | `turnout-by-state-2024` | Where did eligible voters turn out, and where are most of them? |

### What the data holds that shapes the design

Check each against the rows yourself; the build script should assert every fact a title or note states, as Explainer's does.

- **S11, S12 and S15.** Every state and DC moved toward the Republican nominee from 2020 to 2024, by 0.98 points (Washington) to 10.54 (New York). Every arrow points the same way. That is the finding, and the design must make it plain without making it look like a wave of one party's color. Six states changed which nominee led (Arizona, Georgia, Michigan, Nevada, Pennsylvania and Wisconsin); a reader will look for them. The margin is the Republican share minus the Democratic share of all presidential votes, so New York's figures count fused party lines; the source line says so. Say once, in words on the chart, which side of zero is which party's lead, and print party names on the axis ends or margin cells, never a party color.
- **S13.** Total nonfarm payrolls rose 6.0 percent from January 2022 to September 2026. Two sectors lost jobs over that span: information and the federal government. Health care and social assistance gained the most. The dataset holds total nonfarm, total private, government, and 15 sectors that overlap (for example, government contains the federal government). Choose the panels a reader needs, say which you left out and why in your notes, and never let a total and its parts read as peers.
- **S14.** Seven months since January 2025 show a loss. The three-month average last reached 150,000 in April 2024, and its high since January 2025 is 141,700 (May 2026). The latest two months are preliminary and revised; mark them so. A title may say what the count did; it may not say why, and it names no administration or policy.
- **S16.** Reported turnout runs from 52.8 percent (Arkansas) to 79.5 (DC). Rates are self-reported and run higher than counted ballots; state margins of error reach 5.6 points, so differences of a few points between two states may not be real. Circle area, never radius, follows citizen voting-age population.

## 6. Rules in force

- Explainer's anatomy on every chart: evidence label, sentence title with a verb matched to the grade, measure line, the drawing with notes inside it, the source line in section 15 order, and a table or text equivalent (R21). Titles are studio drafts.
- **Party marks (DR-48, DR-58).** Neutral inks only. Wrap every mark that stands for a party's lead or vote in an element with `data-party="Republicans"` or `data-party="Democrats"`. Arrows, position and printed words carry direction. Pillar Red and Prussian never mark a party. No red and blue pair anywhere, including by suggestion.
- **Diverging pair B (DR-54)** wherever a diverging scale appears: Prussian through Newsprint to Verdigris, with a boxed arrow or a printed sign carrying direction, since neither end keeps its order in grayscale. A shift toward one party is not a diverging scale with a good and a bad end; if you use pair B on election data at all, you must show it cannot read as a party pair, and the nonpartisanship reviewer will test that. The safer course on S11, S12 and S15 is Charcoal and Stone with arrows and words.
- **Rule 05.3.** At most one working red per view, marked `data-red="working" data-red-job="<job>"`; a red mark on Newsprint takes a 1 px Charcoal keyline. Red never encodes a series, a category or a scale. You may use none.
- **Interactive layer (DR-59).** One specimen at most carries one, as a demonstration: S15 sortable by column (keyboard operable, `aria-sort` on the active header, a visible focus ring, works without hover), or a Chart and Table switch on one chart. The still image must stand on its own without it.
- **Phones (R25).** Each figure carries artboards at its full width, 600, 358 and 328 px through Explainer's artboard set. Text keeps its set size at every width (13 px floor; 14 px on phones per `CHART_TOKENS`). S12 and S16 must work at 358 px: a tile grid of 51 tiles in 358 px leaves tiles near 30 px, so decide what the phone map shows and what moves to a list under it. S15 becomes cards or a two-line row on phones.
- **Data contract.** Brief section 4. Marks on S11, S12 and S15 use `data-field="margin_2020"` and `data-field="margin_2024"` for the two ends of an arrow and `data-field="shift_pts"` for a shift; S13 marks use the dataset's keys (`PAYEMS|2026-09` and so on); S16 circles use `data-field="citizen_vap_thousands"` for size and `data-field="voted_pct"` for shade. Every row in each dataset's `required_keys` must be drawn. Bars and points carry `data-axis` and, where two scales share one drawing, `data-scale`, and must sit exactly on their scales: the rendered check measures them.
- **Copy.** Explainer's `copy()` on every reader-facing string: dates in words, curly quotes, the true minus sign before a figure, no em dash. Numbers in the thousands print as people say them ("+3.8 million", "140,000 jobs lost"). No record codes, color names or "the studio" on a chart's face (fix pass F12).
- **No disclosure** is required on these six: they do not count or map election rules. If you write a note that touches ranked-choice voting or primaries, the disclosure in D2-106 applies word for word.
- **New sizes** (arrowheads, tile size, circle area scale, sparkline height) go into one dict in your script that extends `CHART_TOKENS`, printed in a short "New tokens" table at the foot of the `newsprint` view, so the kit can adopt them.

## 7. Checks you must pass before you hand back

```bash
python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html
```

```bash
node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html
```

axe-core is installed in `work/build/node_modules/`. The second check takes about a minute and writes captures, grayscale included, to `stretch/captures/`. Look at your own captures at 1440 and 390 px, at 2x, before you hand back, and fix what a picky art director would see: crowding, uneven spacing, a label that fights a mark, a weak first screen.

## 8. Your notes file

Use `work/handoffs/phase-2/20261106_Data-Viz-01-Notes.md` as the model: the idea; each view; each specimen's title, evidence kind and why its form answers the question; your decisions with one-line reasons; the inks you used with measurements; where red appears and why, or that it does not; what you took from Explainer and what you added; titles you would flag for Dustin, each read once from the left and once from the right; a self-score 1 to 5 on Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility and Beauty and distinctiveness, with a line each; what you tested and what you could not test, as separate lists; a change log. Finish your reply with a summary under 200 words.

## 9. What happens next

One reviewer reads the page for statistics and nonpartisanship together (election graphics are the test), then the creative director scores it on the seven-line rubric with a ship threshold of 4 on every line. You will be resumed for one fix pass.
