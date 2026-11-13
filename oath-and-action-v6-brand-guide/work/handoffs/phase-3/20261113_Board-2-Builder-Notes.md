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
   - for `board-pictures` and `file`: a PNG prints as it is; an SVG or HTML file is photographed at true size at the window `width` names (default 1440), on the ground `ground` names (default Newsprint).
4. **`facts`** on any item: `[{"label": "...", "value": "..."}]`, short label and value pairs the board prints as a fact list (DR-258's files uploaded and comparisons rerun, a count).
5. **`rows`** keeps the data lead's form; for A5 each row also names `spec`, and for the forms-changed list each row may carry `rule`, `what_changed`, `why` and `refs`.
6. **`counts`**: as proposed. The board prints `by_domain` and `by_state` as live tables with a bar per row against its limit; `note` prints under each.

The board prints `refs` only in the panel's small reference line, after checking each code is in the decision log or the open questions.

### What the board reads from other owners

- **Cartographer** (`work/handoffs/phase-3/board-2-pictures/`): the S12 stacked tile and today's gray 14.124 sketch, as files the decisions file names under `board-pictures`. An SVG is photographed at true size; an HTML page is photographed whole at the width named.
- **Editor**: every word in the content file (`work/boards/phase-3/round-3/board-2/20261113_Board-2-Content.json`) and in the decisions file, once the first full build lands.
- **Creative director**: `work/handoffs/phase-3/20261113_Board-2-CD-Scores.json` for panel 7's last row, read when it lands.
- **Main session**: the strict build the builder makes itself each run (`guide_build.py --strict --out <scratch>`); the quick guide check's results file when the main session names it.

## How to rerun

(Filled in once the script runs.)

## What the page reads

(Filled in once the script runs.)

## Routine calls

## Tested

## Not tested
