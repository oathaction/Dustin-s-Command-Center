# Board 2 builder notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. The board builder works as the design director building a review page (`.claude/agents/oa-design-director.md`), under `work/handoffs/phase-3/20261113_Board-2-Brief.md`, Part B. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/builder/`. Owners read "Contracts" directly (D3-662).

## Status

- 18:54 UTC. **Run 15 (`--reuse --check --strict`) exits 0, 0 warnings, no failures**, on this board's strict build of 11,236,260 bytes (the size of the main session's version 9 build) and the engineer's plate file remeasured on that build. Folder 318 files, 41,949,582 bytes. Board check: the page alone fails only axe html-has-lang at 1440, 390 and 360 px; the wrapped copy passes. The quick check line points at `phase-3/board-2/main/v9/quick/guide-Guide-Check-Results.json`, which had not landed, so it prints "Waiting for its file" and the Tested panel reads "Part waiting"; one more run after it lands.

- Waiting: the main session's word that version 9 is published, then `--reuse --check` against it.

## Contracts

### The decisions file (agreed with the data lead, 17:12 UTC)

I read `work/handoffs/phase-3/20261113_Board-2-Decisions.json` exactly as the data lead's notes set it at 17:09 UTC ("Schema for the decisions file"), with these additions. Each is optional; the build prints a "Waiting for" line where a field the panel needs is missing, and never types a word or figure of its own in its place.

1. **`state`** at the top: `"draft"` or `"signed off"`. Panel 1 and panel 5 carry the chip "Waiting for the data lead's sign-off" until it reads `"signed off"`.
2. **`spec` and `rule`** on every item that is about one specimen (`"spec": "S73"`, `"rule": "14.104"`), so the board links the item to its live entry and draws today's picture. An `id` that reads `S\d\d` is taken as `spec` when `spec` is absent.
3. **PICTURE** keeps the data lead's fields and adds:
   - `"role": "before" | "after" | "view"`: pictures with `before` and `after` in one item sit side by side, before first, each labeled with its `label`.
   - `"element"` for `guide`: the id of the element to photograph in the strict build (default `oac-s-14-<spec>`, the specimen's figure in chapter 14; a sketch is `fig-<specimen>`, a rule plate `fig-<specimen>`).
   - for `board-pictures` and `file`: a PNG prints as it is; a whole HTML page is photographed at the window `width` names (default 1440), its `element` if one is named, else its body; a fragment or an SVG is drawn in a page that carries the strict build's own styles, on the ground `ground` names (default Newsprint), at true size.
   - for a fragment, `element` means more (added 17:24 UTC, for the gray 14.124 "before"): the builder sets the fragment's drawings in place of that element's drawings in the strict build, in order, gives the element's caption the words of the fragment's first `<desc>`, and photographs it at the width the guide gives that element at the window named. So `{"kind": "board-pictures", "path": "work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before.html", "element": "fig-s-14-124-sketch", "width": 1440, "role": "before"}` beside `{"kind": "guide", "element": "fig-s-14-124-sketch", "width": 1440, "role": "after"}` shows the gray sketch and today's in the same plate, heading and bar, each with its own caption.
4. **`facts`** on any item: `[{"label": "...", "value": "..."}]`, short label and value pairs the board prints as a fact list (DR-258's files uploaded and comparisons rerun, a count).
5. **`rows`** keeps the data lead's form; for A5 each row also names `spec`, and for the forms-changed list each row may carry `rule`, `what_changed`, `why` and `refs`.
6. **`counts`**: as proposed. The board prints `by_domain` and `by_state` as live tables with a bar per row against its limit; `note` prints under each.

The board prints `refs` only in the panel's small reference line, after checking each code is in the decision log or the open questions.

### For the data lead (17:28 UTC, on the decisions file of 17:25)

- Read as written: groups, items, `views` with their `note`, `plan_row.said` and `built` (printed as "The plan said" and "As built"), `rows` with their `refs` (moved to the panel's reference line), `counts.rule_01_9` with `built` (the 97 as built and the 108 as planned), and `counts.dr_229` with `examples` (printed as a table: where, form, example, data, test, passes) and its count fields. `checks` is not printed. A group with no items yet prints "Waiting for this group's items".
- A picture with `"path": null` prints "Waiting for the picture" with its label until the path is filled.
- Pictures print in the file's order; a `before` opens a row that the `after` pictures after it join, and `view` pictures sit in rows of their own. S12's seven pictures therefore read: board 1 at 1,440 beside today at 1,440 and 1,024; the two stacked tiles; board 1's phone beside today's.
- **A suggestion, your call:** `oac-s-14-s12` is the figure inside the scrolling frame, so its photograph is the figure's box (945 px at 1,440) with whatever the frame shows, and it leaves out the line above the map that says the frame scrolls and the frame's scroll bar. `fig-s-14-s12` is the whole plate (heading, the hint line, the frame and its bar), which is what a reader sees at each width. Either works with the builder.

### Fix round additions to the decisions file (18:20 UTC, for the data lead and the editor)

All optional; the build reads them as they land.

- **`replies`** at the top (B2-M1): `[{"n": 1, "item": "S12", "line": "one line: the reply and its recommendation"}, ...]`, the five replies Dustin owes in order. `item` names an item's `id` or a group's `id`; the board prints the five as a numbered list at panel 1's top, each linked to its item or group on the page, then the reply line, and tags the item or group heading "Reply 1" to "Reply 5". Until `replies` lands, panel 1 opens with "Waiting for the five replies".
- **PICTURE `row`** (B2-M2): pictures with the same `row` value sit side by side in one row, in the file's order, rows in order of first appearance; **`fold`: true** puts a picture in one closed fold at the item's end, headed by the item's `fold_title` or the content file's default. Without `row`, the before and after grouping holds.
- **PICTURE `element`** may be an id followed by a CSS selector inside it, for a guide photograph of part of an element: `"fig-s-14-s12 .plate-scroll"` photographs the frame alone, as a reader sees it at that window.
- **PICTURE `alt`** (B2-S3): the words for the picture's alt text, saying what it shows. Without it, the build writes one from the label, the form, the window and the chart's title.
- **`specs`** on an item that covers two charts (`"specs": ["S54", "S55"]`), so B2-M7 shows both of panel 2's Newsprint pictures. An item with a spec and no pictures of its own shows panel 2's Newsprint picture under its recommendation, linked to the form.
- **Election table (B2-M6):** an example whose test was not applied takes `"passes": null` (printed "Not applied"); the build fails on a `"passes": false` whose `test` says it was not applied ("not a form", "before the test", "not applied").

### For the engineer (18:21 UTC): the plate measure file (B2-M4)

The builder reads `work/handoffs/phase-3/board-2-pictures/20261113_Plate-Bytes.json` (or the path you name in your notes): `{"build": {"bytes": 11236319, "built": "..."}, "plates": {"S73": {"as_placed": 13263, "frame": 885, "on_page": 14148}, ...}}`, one entry for each of the 84 charts, keyed by spec id. `as_placed` is the build report's figure, `frame` the plate's own frame measured on the page, `on_page` their sum; the board prints `on_page` with the two parts beside it, everywhere one weight shows, and warns where `as_placed` differs from the build report it reads. Until the file lands the board prints the report's bytes as placed and says the frame waits.

### For the data lead (18:33 UTC): S12's and DR-255's pictures for B2-M2 and B2-S2

The builder lays S12 out from the decisions file's picture list, so B2-M2's two rows and fold need these fields on S12's `pictures` (the cartographer's PNGs, 18:25 to 18:26 UTC, print as they are). Labels and alts are yours and the editor's; the rest is the layout:

```
{"kind": "board-pictures", "path": "work/handoffs/phase-3/board-2-pictures/20261113_S12-Stage-1440-Frame-Newsprint.png", "width": 1440, "role": "after", "row": "1440", "label": "..."},
{"kind": "board-pictures", "path": "work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-1440-Drawing-Newsprint.png", "width": 1440, "role": "view", "row": "1440", "label": "..."},
{"kind": "board-pictures", "path": "work/handoffs/phase-3/board-2-pictures/20261113_S12-Stage-1024-Frame-Newsprint.png", "width": 1024, "role": "after", "row": "1024", "label": "..."},
{"kind": "board-pictures", "path": "work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-1024-Frame-Newsprint.png", "width": 1024, "role": "view", "row": "1024", "label": "..."},
then, each with "fold": true: board 1's s12-newsprint-1440.png, the guide's oac-s-14-s12 at 1440 and at 1024, board 1's s12-newsprint-390.png and the guide's oac-s-14-s12 at 390 (in one "row": "phone" if you want the pair side by side inside the fold)
```

and `"fold_title"` on the item if the content file's default ("More pictures: board 1's plate, today's full plates and the phone drawings") does not fit. For DR-255 (B2-S2): `20261113_S-14-124-Sketch-Gray-Before-Plate-1440-Newsprint.png` (role before) beside `20261113_S-14-124-Sketch-After-Plate-1440-Newsprint.png` (role after), both 868 by 545, in place of the fragment and the guide photograph. A phone picture's label gains its drawing width by itself (" · 326 px drawing", " · 358 px drawing" for board 1's) unless the label already names one.

### What the board reads from other owners

- **Cartographer** (`work/handoffs/phase-3/board-2-pictures/`): the S12 stacked tile and today's gray 14.124 sketch, as files the decisions file names under `board-pictures`. An SVG is photographed at true size; an HTML page is photographed whole at the width named.
- **Editor**: every word in the content file (`work/boards/phase-3/round-3/board-2/20261113_Board-2-Content.json`) and in the decisions file, once the first full build lands.
- **Creative director**: `work/handoffs/phase-3/20261113_Board-2-CD-Scores.json` for panel 7's last row, read when it lands.
- **Main session**: the strict build the builder makes itself each run (`guide_build.py --strict --out <scratch>`); the quick guide check's results file when the main session names it.

## How to rerun

```
python3 -I work/build/scripts/phase-3/board_2_build.py --reuse --check
```

- `--reuse` keeps a kit capture when its spec, data, form module, the kit's shared files, tokens.css and the widths asked are unchanged, and a guide photograph or measurement when its element's HTML, the guide page's styles and scripts and the window width are unchanged. The strict guide build always runs afresh. Drop `--reuse` to remake every capture.
- `--check` runs `node work/build/scripts/phase-2/dataviz_check.js <page> --board --no-captures` from `work/build` on the page itself (results file beside it, `20261113_Board-2-Check-Results.json`) and on a copy in scratch wrapped as the host wraps it (doctype, `<html lang="en">`, charset, viewport). The page carries no `<html>` tag by contract, so axe's html-has-lang is the one failure allowed on the page itself; the wrapped copy must pass every check.
- `--strict` exits 1 on any warning. `--scratch DIR` moves scratch (default `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/builder/`). `--out PATH` writes the page elsewhere. `--decisions FILE` reads another decisions file, for a method test only, and warns so.
- One browser at a time: the guide photographs and measurements (one page load per window width), then the board-only pictures, then the kit in batches of 12 charts (each batch one kit browser, closed at its end), then the two page checks. Nothing runs in parallel.
- The strict build rewrites `work/build/chart-kit/plate-share.json`; the script puts back what it found when only the timestamp moved, and warns (leaving the file) if the share itself changed.

## What the page reads

| Panel | Reads |
|---|---|
| Cover | the plan's rows for rounds 1 to 3 (counts), the panels' states, the content file's words |
| 1, what you decide | `work/handoffs/phase-3/20261113_Board-2-Decisions.json` (groups, items, words, rows, facts, views, pictures, `reply_line`); each picture from the strict build (photographed), the kit's captures, board 1's files or the cartographer's files in `work/handoffs/phase-3/board-2-pictures/` |
| 2, the forms | the plan's 114 rows (rounds 1 to 3) in its family order, the avoid sketches first in each family; each spec's reader question; from the strict build each chart's printed title, evidence label, source line and table, each sketch's heading and caption (photographed at 1440 px), and each entry's anchor for its live link; the guide's drawing width of each chart at 1440 and 390 px (measured), and the kit's captures at the window widths that give those drawings (both grounds, both widths, grayscale) with each check file's faults and weight with its plate frame; for S01 to S16, board 1's check files and desk exports, against a fresh Node drawing at board 1's widths |
| 3, rules 14.1 to 14.14 | chapter 14's rule titles, plates and opener, each plate photographed from the strict build at 1440 px |
| 4, the count | the decisions file's `counts` (Rule 01.9 by topic and by state, DR-229), the script it names |
| 5, the spend | the strict build's report: chapter 14 with the kit against its stop, the kit, map shapes against their reserve, rules with the opener, the share per plate, the projection; bytes by family from each chart's and sketch entry's bytes; the ten heaviest charts with the kit's frame measure |
| 6, scores | the creative director's first scores and rescores for rounds 1 to 3, the nine red team reports (first score and counts before "Second pass", second score after), the board's own scores when they land |
| 7, tested | the strict build's report; the main session's quick check results file in scratch (`phase-3/board-2/main/quick/guide-Guide-Check-Results.json`, the content file's `scratch_file`); the kit's check files from this run; the engineer's A6 table in `20261113_Board-2-Engineer-Notes.md` by pattern (generator check, `build --all` with the sweep, data check, map shapes, V7 check, kit self-test); this board's check results file from its last run |
| 8, next | the content file |

## Routine calls

- D3-xxx | Each chart's desk and phone pictures are the kit's own captures, made at the window that gives the drawing width the guide draws at a 1440 px and a 390 px window, measured on today's strict build: 720 px reading charts at the kit's 1440 px window, the 723 px charts (the column at 1440 px) at a 787 px window, S12's 1,024 px stage at 1,088, and every phone drawing (326 px) at a 358 px window | The brief asks for the drawings "as the guide draws them"; the kit's own 1440 and 390 px windows draw 869 or 1,024 px and 358 px, wider than the guide gives, and S16's phone codes differ at 326 and 358 px (D3-1527)
- D3-xxx | Labels say the reader's window and the drawing's width ("At a 390 px window · 326 px drawing"), read from each chart's check file | The label must say what the picture is; the kit window that made it is a method detail kept in the figures file
- D3-xxx | A board 1 chart says it changed since board 1 where the decisions file's board 1 group names it (in an item or a row), with a link to that item; otherwise it says whether its drawing at a 1440 px window on Newsprint matches board 1's pixel for pixel (the kit's drawing-only file at twice the pixels against board 1's), and a difference panel 1 does not name warns | A first test by each drawing's bytes called 14 of 16 changed: the kit's forced-colors marks and export details change the bytes of a drawing a reader sees unchanged. Panel 1 is the data lead's list of what changed, and a pixel test of the visible drawing guards it
- D3-xxx | Within each family the forms to avoid come first, then the plan's order | The brief: "the avoid pairs marked and first in their family"
- D3-xxx | A sketch form prints the entry's "Use it when" where a chart form prints its reader question | The plan leaves the reader question empty for sketches, and the entry's own line answers the same need
- D3-xxx | Each chart takes three pictures: Newsprint, desk and phone; Charcoal, desk and phone; and one grayscale proof of both grounds and both widths, two by two | 84 charts at three pictures, with 28 sketches, 15 rule pictures and panel 1's, keep the folder near the brief's 300 files
- D3-xxx | Each chart's grayscale proof sits in a fold under its Newsprint and Charcoal pictures, labeled "Grayscale proof of both grounds" | Shown open, the 84 proofs (about 3,000 px tall each, two grounds at two widths) would add about 250,000 px to a page Dustin browses; a fold keeps them one click away at true size, and a closed fold's lazy images do not load until opened
- D3-xxx | The composed pictures are lossless WebP, pixel for pixel the captures (checked by decoding four against their PNGs), not PNG | The first run's PNGs came to 124.55 MB for the folder, past the brief's 120 MB; lossless WebP holds the same pixels at about a fifth of the bytes for color pictures and a half for gray, and it is a standard web image type
- D3-xxx | The page table is the guide's own table from the strict build, with its caption, its classes and data attributes left out, in a fold under each chart | Live text as printed, with no second source to drift
- D3-xxx | The strict build's rewrite of `plate-share.json` is put back after each run when the file carries this build's own timestamp | The board's build is a scratch build; the file belongs to the guide's own builds (D3-1500), and this builder writes only its two scripts, the board folder, its notes and scratch

## Fix round

Under `work/handoffs/phase-3/20261113_Board-2-Fix-Brief.md` (calls 1 to 8) and the creative director's review, from 18:19 UTC.

- D3-xxx | Panel 1 opens with the decisions file's `replies`, each line with its recommendation and a same-page link, then the reply line; the group navigation goes, since the replies link to their items and groups | B2-M1: board 1 named its answers, recommendations and reply line in its first screen
- D3-xxx | The answered group folds closed under one heading with a "Done" chip and its count; an answered item whose recommendation reads "Done." prints no "Recommended" line | B2-M1 and B2-S5
- D3-xxx | A decision item's table of more than six rows folds closed under "The N places, line by line" | B2-M1's long "Answered" tables; the moves and plan-changes lists fold the same way, which shortens panel 1 without hiding a decision
- D3-xxx | The cover's minutes line counts panel 1's words with every fold closed (summaries kept, reference lines left out) and divides by 200, rounded | Call 1: measured by word count at 200 a minute
- D3-xxx | Pictures may carry `row` (side by side), `fold` (one closed fold at the item's end) and an `element` with a selector inside it | B2-M2's two rows and fold, written by the data lead in its own file
- D3-xxx | A phone picture's label gains its drawing width, read from the guide's measure or board 1's check file, unless the label names one | B2-M3: every phone picture labeled by its drawing width
- D3-xxx | A picture's alt text is the data lead's `alt`, else the label, the chart's form and id, where it comes from, the window and the chart's title | B2-S3: say what each picture shows
- D3-xxx | An item about charts with no pictures of its own shows panel 2's Newsprint picture of each chart, the same file, under its recommendation with a link to the form | B2-M7; an item covering two charts (S54-S55) shows both
- D3-xxx | Every weight is the build report's bytes as placed plus the plate's frame and what the page adds inside it, from the engineer's `20261113_Plate-Bytes.json`; the ceiling prints where the engineer's file sets it on that whole measure (round 3, 14,106) | B2-M4 and call 4; the kit's 15,000 hard limit is not the ceiling that binds (the data lead's sign-off)
- D3-xxx | The page sum uses this build's bytes as placed with the engineer's frame, and warns where the engineer's as-placed figure differs | The frame does not move when a chart's words do; the warning says when to remeasure
- D3-xxx | A board 1 drawing that differs from board 1's and panel 1 does not name, and a "No" in the election table whose test was not applied, fail the build (exit 1, page still written); a test not applied prints "Not applied" | B2-M6 and call 6
- D3-xxx | The count captions name their base from the decisions file: 108 examples (97 built and round 4's 11 as planned) by topic and by state; the 17 of the 97 built for election data | B2-S7 and the data lead's sign-off
- D3-xxx | The quick check line says it ran on the committed build before the answers landed, with this board's build beside it; Not tested counts every link to the preview and the entries they reach | B2-S6
- D3-xxx | A chart the guide shows in a scrolling frame is labeled "the whole N px drawing, which the guide shows in a frame that scrolls" | B2-S8: S12's picture is the drawing the frame scrolls through
- D3-xxx | The cover's minutes line gives both figures: the words from panel 1's top through the reply line (lede, the five replies, the reply line) and every item with its folds closed, each at 200 words a minute | The coordinator's change after run 11: the time to answer and the time to read every item, in one sentence
- D3-xxx | Pictures in one `row` that do not fit the column side by side at true size wrap, one under the other, inside one bordered row | S12's frame (946 px) and stacked tile (723 px) need 1,693 px at true size, wider than the 1,312 px column at 1440
- D3-xxx | A decision item's entry link takes a 44 px target | Run 13's axe target-size failure: the link sat alone in its line beside the new picture fold
- D3-xxx | The Scores panel's board row reads `20261113_Board-2-CD-Rescores.json` as the rescore beside the first score, as rounds 1 to 3 do, with one line on what each found | B2-S14
- D3-xxx | A Tested line waiting for its file names that file in the panel's chip ("the quick guide check's results file") | B2-S14: the chip read "the owners' notes" where it waited for the quick check
- D3-xxx | S06's and S67's weight lines name apart the bytes the build adds inside the chart round its atlas IDs (360 and 48, the engineer's `added_on_page`); the ten-heaviest table keeps one "Frame" column and says which charts it also counts them for | B2-S13
- D3-xxx | An item whose id names two charts (S54-S55) shows both of panel 2's Newsprint pictures even where it names one `spec` | B2-S15
- D3-xxx | The content file keeps the editor's two alts for sketch 14.124's pair (its 18:26 words), keyed by each picture's file, read where the decisions file's picture carries none | B2-S3: the alts the editor set in the decisions file left with the pictures the data lead replaced for B2-S2
- D3-xxx | Under 760 px a side-by-side chart frame opens at its right end, on the phone drawing (`direction: rtl` on the frame), with a line above it saying so; composed Charcoal pictures take a 16 px Charcoal margin | B2-S12; one picture a ground keeps the folder near 300 files, where separate phone pictures would add 168

## Tested

- Six runs, 17:22 to 17:50 UTC. Run 1 without `--reuse`: strict build exit 0; 225 guide elements photographed or measured, none failed; the kit built all 84 charts, 84 check files, 0 faults, 0 warnings; 295 pictures; 124.55 MB as PNG, past the 120 MB aim. Runs 2 to 6 with `--reuse --check`: 9 wide charts and S12 rebuilt at the guide's widths; the decisions file read; 310 pictures; 41.8 MB as lossless WebP; the board check as in Status every time.
- The guide's drawing widths, measured on the strict build: 74 charts at 720 px and 9 at 723 px at a 1440 px window, S12 at 1,024; all 84 at 326 px at a 390 px window. After the kit's builds, every chart's kit drawing equals the guide's at both windows (the build warns on any difference; none since run 2).
- Lossless WebP: four composed pictures decoded and compared with their PNGs pixel for pixel, all equal.
- The board 1 comparison: the kit's drawing-only file at 1440 px on Newsprint against board 1's for S01 to S16: S03, S06 and S07 equal pixel for pixel; S04 and S08 differ and are not named (above); the other 11 differ and are named in panel 1.
- Red team counts read by script from the nine reports: round 3 statistics 3 of 5, 4 Must fix, 12 Should fix, second 3.5; access 3, 2, 8, second 4; brand and craft 3, 3, 15, second 4, matching V23's figures.
- The build's own checks every run: no em dash in the board's text or alt text; no flagged word, unfilled field or en dash in the board's own words; decision codes and file paths only in reference lines for the board's own words (quoted words flagged above); every reference code in the decision log; no private path, no script, no document tags, no dark-mode block, no color outside a token, no type under 13 px; every image with alt text, width, height and `loading="lazy"`; links only to the guide preview; outside loads only from Google Fonts; the page names exactly the images in `img/`; `plate-share.json` left as found (`git status` shows no builder file outside the board folder and these notes).
- Read by eye from screenshots of the wrapped copy: at 1440 px the cover, panel 1's S12 item, form 14.104 (S73), form 14.124 (the avoid sketch), panels 4 and 5; at 390 px the cover, panel 1's S16 item and form 14.104; scroll width equal to the window at both (1440 and 390).

## Not tested

- The final build and preview version 9: the board links to `https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF#rule-14-N`, and each anchor is checked on today's strict build, not on the published page.
- The guide check: never run by this builder.
- The board in Safari or Firefox, on a 2x screen, printed, or as the host shows it once published; the wrapped copy stands in.
- Most of the 310 pictures one by one, and most of the forms panel at 390 px by eye.
- A keyboard walk past the check's focus stops, and a screen reader.
- The words the board quotes from the decisions file and teammates' files beyond the build's checks; the editor reads them.

## Change log

- Created: `work/build/scripts/phase-3/board_2_build.py`, `work/build/scripts/phase-3/board_2_render.js` (copied from `progress_round_2_render.js`, measure item extended), `work/boards/phase-3/round-3/board-2/` (`20261113_Board-2.html`, `20261113_Board-2-Content.json`, `20261113_Board-2-Figures.json`, `20261113_Board-2-Check-Results.json`, `img/`), this file.
- Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/builder/` (strict builds, `kit-out/`, `board1-compare/`, `shots/`, `files/`, caches, `publish-view/`, `view/` screenshots, run logs, `test-decisions.json`).
- Modified outside these: none. `work/build/chart-kit/plate-share.json`, rewritten by run 1's strict build, was put back as committed at 17:26 UTC; the script now does so itself.
