# Board 3, data lead notes

Written November 20, 2026, by the data lead (`oa-dataviz-systems-lead`). Brief: `20261120_Board-3-Brief.md`, my row, "The decision file" and panel 1. Model: `20261113_Board-2-Decisions.json` and `work/build/scripts/phase-3/board_2_data_lead_counts.py`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/data-lead/` (the main session named this folder; the brief's `board-3/<role>/` form is not used).

## Status

16:50 UTC: schema below, for the builder and the research lead. The decision file is not written yet; the second pass sign-off comes first, and I write the file while I wait for its items.

## Schema of `20261120_Board-3-Decisions.json`

Board 2's schema (`board-2-decisions/1`) with the changes listed after it. The builder's `board_2_build.py` reads every key below the same way, so a copy reads this file with the additions only.

Top level:

- `schema`: `"board-3-decisions/1"`.
- `state`: `"draft"`, then `"signed off"`. `updated_utc`, `written_by` (`"data lead"`), `words_owner` (`"editor"`), `reply_line` (the brief's line, exactly).
- `panels`: a list, in the board's order (below). Each panel: `id`, `title`, `lede`, `approval` (`"one"` for one reply for the lot, `"each"` for one reply per item, `"none"`), `items`, and `reply_number` where the panel takes one reply.
- `counts`: `script`, `run_utc`, `rule_01_9`, `dr_229`, as board 2's (same keys), written by my scratch script `board_3_data_lead_counts.py` and copied in. `rule_01_9.built` becomes the finished chapter 14 (rounds 0 to 5, no planned rows), and `round_4_rows` is dropped since round 4 is built.
- `changed_found`: how panel 1's changed approved work was found: `script` (scratch path), `run_utc`, `ledger` (`work/ledger/20261020_Change-Ledger.md`), `rows_read` (`"C-108 to C-134"`), `match` (the two phrases), `found` (the C codes it found), `second_pass` (the RS and CR codes that change approved work).
- `replies`: as board 2's: `n`, `panel`, `id` (null for a whole panel), `line`, `recommendation`, `item`.
- `signed_off_utc`, `signed_off_note` once signed off.

Panels, in order:

1. `trackers`: "The two new trackers' step names". Two items, `11.10` and `11.11`, approval `"each"`. Each item adds `steps` (a list of `{n, name}`, read from `apply_systems_ch11.py`'s output) and `marks` (the mark words the plate's key prints).
2. `changed-approved`: "Changed approved work", approval `"one"`. One item per change; each adds `ledger` (a list of C codes and D3 or DR codes behind it), `approved_at` (board 1, board 2, Gate 2, and so on) and `shows` (`true`, or `false` with `shows_note`, the one line saying it does not show).
3. `held`: "Held for Dustin", approval `"each"`. One item per register row under "Held for Dustin (board 3)", plus `Q-12`, plus any second pass item flagged for him. Each adds `register` (`{"file", "section", "code"}`) or `question` (`"Q-12"`).
4. `atlas-v7-1`: "The proposed atlas V7.1 row", one item `routes-who`, approval `"one"`, with board 2's `new_to_v7_1_list`, `source` and `facts` keys and a `counts` list (`{label, value, from}`).

Items keep board 2's keys: `id`, `title`, `answer`, `what_changed`, `why`, `recommendation`, `refs`, `question_for_dustin`, `pictures`, `facts` (`{label, value}`), `rows`, `views`, `spec`, `rule`.

Pictures keep board 2's keys (`kind`, `spec`, `element`, `width`, `ground`, `path`, `label`, `role`, `row`, `alt`, `fold`) and add one:

- `page`: which page a `kind: "guide"` picture comes from: `"v11"` (`work/boards/phase-3/round-5/20261114_Guide-Preview-V11.html`, the "before"), `"final"` (the chat 8 strict build, version 13, the "after"; until it lands the builder reads the V12 page), or `"v12"`. A guide picture with no `page` reads `"final"`.
- `role` keeps board 2's `"before"`, `"after"` and `"view"`; a V11 picture is `"before"`.
- A change that does not show carries no pictures and `shows: false` with its one line.

Every key a board 2 builder does not know is extra, so a straight copy of the builder still builds; the builder adds `page` to `pic_request()`.

## Rulings

## Calls

## Tested

## Not tested
