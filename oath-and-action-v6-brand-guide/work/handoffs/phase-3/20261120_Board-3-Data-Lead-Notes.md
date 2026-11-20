# Board 3, data lead notes

Written November 20, 2026, by the data lead (`oa-dataviz-systems-lead`). Brief: `20261120_Board-3-Brief.md`, my row, "The decision file" and panel 1. Model: `20261113_Board-2-Decisions.json` and `work/build/scripts/phase-3/board_2_data_lead_counts.py`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/data-lead/` (the main session named this folder; the brief's `board-3/<role>/` form is not used).

## Status

16:50 UTC: schema below, for the builder and the research lead. The decision file is not written yet; the second pass sign-off comes first, and I write the file while I wait for its items.
17:09 UTC: **the decision file is written and signed off**, `20261120_Board-3-Decisions.json` (148,473 bytes): 4 panels, 39 items, 24 replies, 86 pictures (77 from guide pages, 8 to make, 1 from board 2's files). Every count is read by script from the repository and from my strict build of the joined second pass (17:00 UTC). The words are a first draft; the editor owns them from here. When the main session's final build lands, I rerun the counts only (`--counts-only`), which leaves every word alone.

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

### Schema changes made while writing the file (17:09 UTC; for the builder and the editor)

- `pages` at the top level maps each page key to its file: `v9` (board 2's page), `v10` (after round 4), `v11` (after round 5), `v12` (after the fix pass) and `final`. A "before" picture comes from the last page before its change: round 4's changes on approved work (C-108, C-113, D3-1711) from V9, round 5's (C-118) from V10, the fix pass's (C-124 to C-132) from V11, and the second pass's from V12. V11 already holds round 4's and round 5's changes, so it cannot be their "before".
- `element` is an element id, or a CSS selector where it holds a dot (`header.masthead`, the shell's masthead).
- `setup` (optional) on a guide picture: `focus` (which control holds focus, in words), `scroll`, and `text_scale` (2 for 200 percent text). Items: the masthead's focus offsets, "Where to start" at 320 px.
- `kind: "to-make"` is a picture no page holds yet: `owner` and `how` say who makes it and from what, and `path` stays null until it lands, so the builder shows it waiting (board 2's `missing` path).
- Every held item carries `settled`: `touches` (the settled or approved element the choice reaches) and `respects` (how the recommendation keeps Dustin's settled list), for the main session's read against the brief's Limits. Register rows carry `register` (`file`, `section`, `code`, the code exactly as the register prints it); D3-2278 carries `decision`; Q-12 carries `question`.
- `changed_found` and `held_found` hold the script's finds whole, and `counts` names the script, its requested home in the repository and the generator that wrote the file. `build_report` names the strict build report the image stage and weight figures come from.
- Panel 2 items carry `ledger`, `approved_at`, `shows` and, where it does not show, `shows_note`; `specs` where one item covers several charts (board 2's `item_specs()` reads it).

## Rulings

### What the file holds, found by script

- **Changed approved work.** `board_3_data_lead_counts.py` reads change ledger rows C-108 to C-134 (27 rows) for "listed for board 3", "board 3 shows" or "shown on board 3" and finds 10: C-108, C-113, C-118, C-124, C-125, C-128, C-129, C-130, C-131 and C-132. The decision log adds five Phase 3 rows that list work for board 3 outside those rows' words: D3-1711 (`text-wrap: pretty` on source lines), D3-2127 (14.144's pips), D3-2140 (15.20's chooser), D3-2143 and D3-2144 (S14). The scan also matches Phase 2's own "Board 3" rows (DR-44, DR-55, DR-231's history); I read and left those, since that board closed in Phase 2. The second pass adds one visible change to approved work (RS-5: chapter 15 under Related chapters on 14.88 and 14.96) and one change heard only by a screen reader (RS-1 on Rule 11.12's records plates). They make 16 items with one approval.
- **"Before" pictures.** Round 4 made C-108's and C-113's changes, and round 5 made C-118's, all before V11 was built, so V11 shows them already changed. Their "before" comes from V9 (board 2's page) or V10. The brief's "before from V11" holds for the fix pass's rows, C-124 to C-132.
- **Held for Dustin.** The register's section "Held for Dustin (board 3)" holds 16 rows by script, not the brief's 17. Two more rows elsewhere in the register carry the status "held for Dustin (board 3)": AX-S3's two approved plates (`s-11-steps`, `s-11-marks-drawn`) and CR-S4's sticky drawing, both under "Not fixed in the fix pass". I put all 18 on the board, with D3-2278 (RS-5's visible half, the main session's call) and Q-12: 20 held items. If the brief's 17 meant one of the two outside rows, the editor can say so; both wait on Dustin by their own status.
- **The trackers.** Steps, what happens at each and the law behind each are read from `BALLOT_STEPS` and `COURT_STEPS` in `apply_systems_ch11.py` (the research lead's facts, read November 14); the marks are each plate's key as printed. Two replies, one per tracker, as DR-108 approved the bill's names by name.
- **The V7.1 row.** `routes[].who` counted by script from `atlas-v7-data.json`: 126 route entries, 89 distinct values, 5 that open with a verb, matching the research lead's round 4 count. One of the five prints on the guide's page: Rule 15.20's correct plate shows R-03's federal statute route as "Repeal the single-member mandate (2 U.S.C. 2c) and require ranked multi-winner counting" where its card means who acts. The guide does not change the V7 model; the row goes to the atlas editor's list.

### Rule 01.9 and DR-229 for the finished chapter 14

- **Rule 01.9 holds.** Chapter 14 as finished holds 112 examples, read from the built chapter file: 13 on the rule plates (entries 14-001 to 14-014; Rule 14.14's plate logs none), 96 kit charts each once (Rules 14.127 and 14.128 point to S06 and S13 and add none), and 3 in the charts in full (Loop B4 and Loop R10 on 14.143, Loop R8 on 14.144). The 30 sketches draw invented data and count none. By round: 48, 26, 23, 11 and 4. The largest domain is Taxes, wealth and economic security (D08), 16 against a limit of 28; California, Florida and New York lead the states at 5 each against 22; 9 examples are atlas-wide. The recount agrees with `14-example-log.json` row for row (rule and domain), with no difference either way. Board 2 counted 97 built and 108 with round 4 planned.
- **DR-229 holds.** 18 of the 112 draw election or voting data: 13 in Elections and representation and 5 on reported voting under taking part. Of the specimens, 8 were built in Phase 2 before the test, 5 new forms pass D3-689's test and none fails; 4 are rule plates. One example joined since board 2: Loop R10 on Rule 14.143, which my round 5 ruling (g) counted as one of Gate 2's named complex examples, outside the coverage plan's forms. The test is board 2's, word for word.

### Recommendations against the settled list

Each held item names what it touches and how it keeps the list. Three choices touch a settled element directly, and the file says so: CE-S22's question words are the coverage plan's (DR-62), so the recommendation keeps them and takes example lines under them instead; the keyline on the red targets touches a mark of the atlas visual system (DR-36), which call 15 already changed on Rules 15.20 and 14.144, so the file puts the one-look choice to Dustin and says why; CR-S19's evidence chip touches the chart system's header (DR-52), so the recommendation moves no approved chart. No recommendation changes a Civic Line icon, a reform's treatment, the chart rules of DR-64, chapter 02's writing rules or an answer Dustin has given; S59 (DR-263), S71, Rules 14.6, 15.15 and chapter 11's plates are approved work put back to him at true size, which is what this board is for.

## Calls

- D3-xxx | Board 3's held items are the 16 rows of the register's held section plus the 2 rows elsewhere whose status holds them for board 3 (AX-S3's approved plates, CR-S4's sticky drawing), with D3-2278 and Q-12: 20 items | the brief's "17 rows" matches neither count found by script, and both outside rows wait on Dustin by their own status
- D3-xxx | A "before" picture comes from the last page before its change: V9 for round 4's changes on approved work, V10 for round 5's, V11 for the fix pass's, V12 for the second pass's | V11 already holds rounds 4 and 5, so it cannot show them before
- D3-xxx | Rule 14.144's pips and Rule 15.20's chooser stay in panel 1's changed work, though both plates were built after board 2 | the brief lists both, and D3-2127 and D3-2140 each send the change to board 3
- D3-xxx | Rule 01.9 counts one example per plate that draws data, each kit chart once, and no sketch | the generator's log counts the same way, and the recount agrees with it row for row
- D3-xxx | Rule 14.143's Loop R10 counts under DR-229 as "not applied": a named complex example outside the coverage plan's forms | round 5 ruling (g); D3-689's test reads a form's coverage plan use, which a chart in full does not have
- D3-xxx | The keyline item names DR-36 among what it touches | the red target is a mark of the atlas visual system; the main session reads the file against the settled list and should see it

## Requests

1. **To the main session.** Copy `board_3_data_lead_counts.py` and `make_board_3_decisions.py` from my scratch folder to `work/build/scripts/phase-3/`, as board 2's counts script sits there; I may not write there. The file names the requested home in `counts.requested_home`.
2. **To the builder.** `pic_request()` needs `page` (pick the page file from `pages`), `element` as a selector where it holds a dot, `setup` for the two pictures that need focus or 200 percent text, and `to-make` shown as waiting. 86 pictures in all; the builder chooses which to capture first.
3. **To the research lead.** Q-12's facts, and the V7.1 row's wording for the atlas editor; my counts are in `panels[3].items[0].counts`.
4. **To the editor.** Every word in the file is yours from here. I wrote no em dashes (the generator refuses one).

## Tested

- `board_3_data_lead_counts.py` (scratch) at 16:57 and 17:09 UTC: Rule 01.9 (112 examples, agrees with the generator's log), DR-229 (18), the ledger find (10 of 27 rows), the register find (16 plus 2), Q-12, `routes[].who` (126, 89, 5).
- `make_board_3_decisions.py --state "signed off"` against my strict build report of 17:00 UTC (exit 0, 0 warnings, 12,178,911 bytes; 101 hidden, 315 open; Phase 4's figures 362,857, 484,488 and 413,060).
- Every one of the 77 guide pictures' elements found in the page it names (V9, V10, V11, V12 and my joined build standing in for the final page); the one board 2 picture's file exists.
- The trackers' twelve names read from the generator's own lists by `ast`, not copied by hand.
- The guide pages that print a verb-led `who` value, by search of chapters 14 and 15's fragments: one, `s-15-20-correct`.
- The related rules' reach (138 of 144 rules, 363 links, every target a rule in the guide), by script on the chapter file.

## Not tested

- The final build: the main session's strict build after the second pass and version 13 have not landed; my figures come from my own strict build of the same tree (15591677). A `--counts-only` run follows when they land.
- Any picture: no browser yet. The 8 pictures to make wait on their owners.
- The weight of printing related rules: about 37,000 bytes is my estimate from one link's markup, not a measure.
- The facts behind Q-12 and the V7.1 row's wording: the research lead's.
