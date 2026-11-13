# Board 2 builder notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. The board builder works as the design director building a review page (`.claude/agents/oa-design-director.md`), under `work/handoffs/phase-3/20261113_Board-2-Brief.md`, Part B. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/builder/`. Owners read "Contracts" directly (D3-662).

## Status

- 17:12 UTC. Started. Read CLAUDE.md, my role file, the brief, the decision log from D3-1312 to DR-260 (and D3-1536 to D3-1541), V23 section 1, board 1's and the round 2 progress page's builders, the progress page's brief and notes, board C's `rule_href`, chapter 02's writing rules and the data lead's proposed schema.
- Contracts: I adopt the data lead's schema for `20261113_Board-2-Decisions.json` (17:09 UTC) with the six additions under "Contracts" below. Writing the script next.

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
| 7, tested | the strict build's report; the main session's quick check results file in scratch; the kit's check files from this run; this board's last check results file |
| 8, next | the content file |

## Routine calls

- D3-xxx | Each chart's desk and phone pictures are the kit's own captures, made at the window that gives the drawing width the guide draws at a 1440 px and a 390 px window, measured on today's strict build: 720 px reading charts at the kit's 1440 px window, the 723 px charts (the column at 1440 px) at a 787 px window, S12's 1,024 px stage at 1,088, and every phone drawing (326 px) at a 358 px window | The brief asks for the drawings "as the guide draws them"; the kit's own 1440 and 390 px windows draw 869 or 1,024 px and 358 px, wider than the guide gives, and S16's phone codes differ at 326 and 358 px (D3-1527)
- D3-xxx | Labels say the reader's window and the drawing's width ("At a 390 px window · 326 px drawing"), read from each chart's check file | The label must say what the picture is; the kit window that made it is a method detail kept in the figures file
- D3-xxx | A board 1 chart says whether its drawing changed since board 1 by a Node drawing at board 1's windows (1440 and 390 px, both grounds) compared in width, height and bytes with board 1's check files, and the desk export on Newsprint compared character for character where both exist | The brief asks whether the drawing changed; a picture of the whole figure would also change with a note's words, which panel 1 lists apart
- D3-xxx | Within each family the forms to avoid come first, then the plan's order | The brief: "the avoid pairs marked and first in their family"
- D3-xxx | A sketch form prints the entry's "Use it when" where a chart form prints its reader question | The plan leaves the reader question empty for sketches, and the entry's own line answers the same need
- D3-xxx | Each chart takes three pictures: Newsprint, desk and phone; Charcoal, desk and phone; and one grayscale proof of both grounds and both widths, two by two | 84 charts at three pictures, with 28 sketches, 15 rule pictures and panel 1's, keep the folder near the brief's 300 files
- D3-xxx | Each chart's grayscale proof sits in a fold under its Newsprint and Charcoal pictures, labeled "Grayscale proof of both grounds" | Shown open, the 84 proofs (about 3,000 px tall each, two grounds at two widths) would add about 250,000 px to a page Dustin browses; a fold keeps them one click away at true size, and a closed fold's lazy images do not load until opened
- D3-xxx | The page table is the guide's own table from the strict build, with its caption, its classes and data attributes left out, in a fold under each chart | Live text as printed, with no second source to drift
- D3-xxx | The strict build's rewrite of `plate-share.json` is put back after each run when the file carries this build's own timestamp | The board's build is a scratch build; the file belongs to the guide's own builds (D3-1500), and this builder writes only its two scripts, the board folder, its notes and scratch

## Tested

## Not tested
