# Round 1 progress page builder notes

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. The page builder works as the design director building a review page (`.claude/agents/oa-design-director.md`), under `work/handoffs/phase-3/20261112_Round-1-Progress-Page-Brief.md` (DR-241). Paths are relative to `oath-and-action-v6-brand-guide/`.

## Status

- **Method proven; waiting for the fix pass and the rescore.** The script and content file are written and ran on the current files (November 12, about 16:20 UTC). The main session reruns it when the rescore lands (see "How to rerun").
- Built: `work/boards/phase-3/round-1/progress/20261112_Round-1-Progress.html` with `img/` beside it, by `work/build/scripts/phase-3/progress_round_1_build.py` and `progress_round_1_render.js`, from the words in `20261112_Round-1-Progress-Content.json`. Every figure the page prints, with its source, goes to `20261112_Round-1-Progress-Figures.json`; the check writes `20261112_Round-1-Progress-Check-Results.json`.
- The folder holds 102 files, 32,708,268 bytes: the page (about 197 kB), the content, figures and check results files, and 98 composed PNGs (largest 1,261,899 bytes, the heat table's Newsprint pair). Limits: under 200 files and 50 MB; the build warns past either.
- Parts at the last run: 1 to 6, 8 and 10 Ready. Part 7, Scores, shows the creative director's first scores (`20261112_Round-1-CD-Scores.json`, which landed during this task: none of the five parts ready yet) and waits for the rescore; of the red team reports, statistics reads 3 of 5 with 5 Must fix and 13 Should fix, access reads 4 of 5 with 1 Must fix and 10 Should fix, and brand and craft is still pending. Part 9 waits on the brand and craft report and any list a file still marks pending. Each fills in on the next run once its file lands.
- At this run the research lead had frozen the Department of Labor table (`dol-state-minimum-wage-history`, ledger row P7-223) and its notes record it, so part 1 prints it frozen. Round 3's map geometry is still waiting: 14 of 20 data rows have every file frozen, 24 of the 27 files the plan names.

## How to rerun

```
python3 -I work/build/scripts/phase-3/progress_round_1_build.py --reuse --check
```

- About 25 seconds when nothing changed, about 2 minutes when every chart and photograph is new (kit build about 2 minutes for all 26; guide photographs about 1 to 2 minutes; strict guide build about 10 seconds; the two checks about 15 seconds). Drop `--reuse` to remake every capture.
- `--reuse` keeps a kit capture when its spec, its data and sidecar, its form module and the kit's shared files (and tokens.css) are unchanged, and a guide photograph when its element's HTML, the guide page's styles and scripts and the window width are unchanged. The strict guide build always runs afresh.
- `--check` runs `dataviz_check.js --board --no-captures` from `work/build` twice: on the page itself and on a copy in scratch wrapped as the host wraps it. `--strict` exits 1 on any warning. Scratch defaults to this session's `.../scratchpad/phase-3/round-1/progress-page/`; `--scratch DIR` moves it.
- The scores file names are in the content file's `slots`; the rescore is read from the newest `work/handoffs/phase-3/*Round-1-CD-Rescore*.json`. The entry shown in part 3 is the content file's `sections.entry.rule` (14.16).
- After the rerun, read part 7's red team counts against each report's headings (statistics and access already match theirs): the counter reads bold-led or heading-led finding IDs (M1, S13, SC-M1) and falls back to numbered items; a report that numbers findings another way would need a look.

## What the page reads

| Part | Reads |
|---|---|
| 1, round 1 in one screen | the plan file (round 1's forms by status, the chapter-wide rules), chapters 14 and 15 (entries, plates, opener), round 3's plan table "Datasets to fetch and freeze" against `work/build/data/`, the Department of Labor file and its sidecar plus the research notes' "Frozen" line with its ledger row, and the strict build's report (bytes, rules, examples, warnings) |
| 2, the 26 new charts | the plan's new forms in its order, grouped by its family titles; each chart's title as the strict build prints it (the one-sentence form prints its spec's sentence, which it draws in place of a title); the kit's own captures and check file from a fresh `oa-chart.mjs build` into scratch; each chart's bytes from the build report's `weight.charts` |
| 3, an entry | Rule 14.16 photographed whole from the strict build at 1440 and 390 px |
| 4, sketches | the plan's sketch forms; the heading each plate prints, read from the strict build; each photographed at 1440 px |
| 5, rules 14.1 to 14.14 | chapter 14's opener and each rule's correct and failure plates, photographed at 1440 px |
| 6, chapter 15 | the opener and every plate in chapter 15's JSON, photographed at 1440 and 390 px |
| 7, scores | `20261112_Round-1-CD-Scores.json`, the newest rescore, the three red team reports |
| 8, weight | the build report: chapter 14 against its stop and the share per plate still to come, chapter 15 against its ceiling, the page projection against the budget |
| 9, tested | every Tested and Not tested list in the eleven files the content file names |

## Routine calls

- D3-xxx | The page reads every number, title and picture from files at build time; the content file holds only words, file names and the one entry part 3 shows | The fix pass and rescore are still running, so the main session reruns it with nothing typed by hand
- D3-xxx | Board 1's Markdown readers, its quoted-words rule and its Tested-list reader are imported from `board_1_build.py`, not copied | One reader for both pages, and a quoted code moves to the reference line the same way (D3-206)
- D3-xxx | Each new chart shows in two composed pictures, Newsprint and Charcoal, each with the 1440 and 390 px page drawings side by side, labeled in Inter Medium at 13 px (board 1's D3-195 and D3-196), without board 1's grayscale and Phase 2 rows | The brief asks for these two pairs, and the page is shorter than board 1
- D3-xxx | A chart's title is read from the strict build's figure; the one-sentence form (Rule 14.134) draws its sentence in place of a title, so its spec's title, the sentence itself, prints | "Its title as printed"; S42's figure has no title paragraph to read
- D3-xxx | A guide element taller than the window is photographed by making the window taller, its width kept at 1440 or 390 px, and clipping the picture from the window, rounded outward to whole pixels, with CSS animations and transitions off | Playwright's capture beyond the window took 15 to 30 seconds per plate on the 10 MB guide and timed out on four plates in the first run (18 minutes); the clip takes about a second and every layout width stays the same
- D3-xxx | Every chart is drawn with `OAChart.draw_all()`, the page's height must hold still, and each element is photographed only once its own position holds still, with sticky bars set static (D3-200) | A chart drawn above an element can shift it after the scroll
- D3-xxx | Rule plates sit side by side when both fit 1,280 px and one above the other when not; at a 1440 px window each plate is 868 px wide, so all fourteen stack | "Side by side or stacked as reads best"; side by side they would scroll sideways at 1440
- D3-xxx | Chapter 14's opening plate heads part 5 | The creative director scores the rules "with the opener", and it shows the chapter's question-first structure
- D3-xxx | Each chapter 15 plate's 1440 and 390 px photographs share one composed picture, the opener first, with chapter 15's group titles | Twenty-five pictures in place of fifty, and the two widths read together
- D3-xxx | Part 3 shows Rule 14.16, the column entry | A short entry that carries every part: the rule, use it when, use instead, why it works, the chart and its table
- D3-xxx | Round 3's data counts come from the plan's table "Datasets to fetch and freeze", with "Geometry" expanded to its three files and "107 to 112" to its rows; a file is frozen when it and its sidecar are in the data folder, a row when every file it needs is | The table names the geometry the map rows need, which the plan's forms table names only in words; counting files keeps the count true as files land
- D3-xxx | The Department of Labor table counts as frozen only when its file and sidecar are in the data folder and the research notes say "Frozen" with the sidecar's ledger row | "If the research lead's notes say so"
- D3-xxx | The weight bars show each part's share of its own limit | The three limits run from 600,000 to 15,500,000 bytes, so one byte scale would hide chapter 15
- D3-xxx | Part 7 names the creative director's parts by short names from the content file, keyed by the scores file's keys, and drops review finding IDs in parentheses from quoted reasons | The scores file's item names run to forty words; a reader would not know an ID such as CH15-M1
- D3-xxx | Red team counts are read from each report's Must fix and Should fix sections: bold-led or heading-led finding IDs, else numbered items; a section that reads "Pending" waits | D3-205's method, widened for round 1's report forms; on the statistics report it reads M1 to M5 and S1 to S13
- D3-xxx | Only the tokens.css `:root` definitions the page's styles name, and the ones they name in turn, are inlined; no surface or dark-mode block | The page commits to Newsprint and every color stays a token on `:root`
- D3-xxx | Google Fonts load by `@import` at the head of the page's one style block | The brief puts the title, the viewport meta and one style block first, with outside requests to Google Fonts only
- D3-xxx | The check runs with `--no-captures`, on the page and on a scratch copy wrapped as the host wraps it; the page itself may fail only axe's html-has-lang | Captures would land in a folder beside the page; the page carries no `<html>` tag by its contract, so the language comes from the host's wrapper
- D3-xxx | Images the page no longer names are removed from `img/` on every run, and each picture is a PNG saved with lossless compression | The folder publishes as it stands

## Tested

- First run, without `--reuse`: strict guide build exit 0, 0 warnings, 10,017,051 bytes, 265 rules, 554 specimens; the kit built all 26 new charts, 26 PASS with 0 faults each; 81 of 85 guide photographs taken and four plates timed out (chapter 14's opener and the correct plates of 14.1, 14.4 and 14.8). That run took 18 minutes.
- The renderer after the change: on six elements, the new clip pictures match the first run's in width (868 and 350 px) and within a pixel in height; pixel differences come from the element's fractional position on the page. Chapter 14's opener and 14.1's correct plate, which timed out before, were taken in under a second each; 14.1's correct plate viewed whole.
- Second run, without `--reuse`: 26 charts built afresh, 85 photographs, 98 images composed, 0 warnings. `dataviz_check.js --board --no-captures` on the page: three failures, all axe html-has-lang at 1440, 390 and 360 px, and nothing else (no sideways scroll, no text under 13 px, no low contrast, focus rings on the first 40 stops, outside requests).
- Third and fourth runs, with `--reuse --check`: 24 seconds; all 26 kit captures and 85 photographs reused. The page itself: the same three html-has-lang failures only. The page as the host wraps it (doctype, `<html lang="en">`, charset, viewport): PASS at 1440, 390 and 360 px, axe-core WCAG 2.2 AA clean, the scale check reading the three weight bars as one group with no fault, 0 warnings from the build.
- The build's own checks on every run: no em or en dash in the page's text or alt text, no flagged word in its own words, no unfilled field, no decision code on the page's face, every code in a reference line found in the decision log, no private path, no script, no `<!doctype>`, `<html>`, `<head>` or `<body>`, no dark-mode block, no color in the page CSS outside a token, no font size under 13 px, alt text on every image, the page names exactly the images in `img/`.
- The page read by eye from screenshots of a wrapped copy at 1440 px (cover, parts 1, 2, 3, 5, 7, 8 and 9) and 390 px (part 2, part 6's opening); three composed pictures viewed whole (Rule 14.27 on Charcoal, Rule 15.6's correct plate, Rule 14.1's plates).
- Part 7 on stand-in files: round 0's scores and rescores render the table with both scores, and with no rescore the part reads "Part waiting for the creative director's second scores". On round 1's own first scores, once they landed: the table, the five parts not yet ready, and each score under 4 with its reason, with the review IDs in parentheses dropped. The red team counter: statistics 3 of 5, 5 Must fix, 13 Should fix (headings M1 to M5, S1 to S13); access 4 of 5, 1 Must fix, 10 Should fix (M1, S1 to S10).
- The final run, `--reuse --check --strict`: exit 0, 0 warnings; the page itself fails only axe html-has-lang at three widths; the wrapped copy passes at all three.
- Round 3's data counts and the Department of Labor reading, by script against the files: 20 data rows, 14 with every file frozen, 24 of 27 files, the three geometry files waiting; the table frozen as P7-223, recorded in the research notes.

## Not tested

- The page in Safari or Firefox, on a 2x screen, printed, or as the host actually wraps it once published; the wrapped copy stands in for the host.
- 95 of the 98 composed pictures one by one, and the chapter 15 and entry pictures at 390 px by eye beyond part 6's opening screen.
- Part 7 with the rescore file and the brand and craft report, untested until they land.
- A keyboard walk past the first 40 stops, and a screen reader.
- The figures quoted from teammates' files beyond the counts above; the page prints them as written.
- Publishing; the main session publishes.

## Change log

- Created: `work/build/scripts/phase-3/progress_round_1_build.py`, `work/build/scripts/phase-3/progress_round_1_render.js`, `work/boards/phase-3/round-1/progress/20261112_Round-1-Progress.html`, `20261112_Round-1-Progress-Content.json`, `20261112_Round-1-Progress-Figures.json`, `20261112_Round-1-Progress-Check-Results.json` and `img/` (all in `work/boards/phase-3/round-1/progress/`), and this file.
- Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1/progress-page/` (the strict guide build and its report, `kit-out/` with the kit's builds, `shots/` with the guide photographs, the signature and composition caches, `publish-view/` with the wrapped copy and its check results, logs, probes and screenshots).
- Modified: none outside these.
