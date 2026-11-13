# Board 2 data lead notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. Data visualization and systems lead (`oa-dataviz-systems-lead`), under `work/handoffs/phase-3/20261113_Board-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/data-lead/`. Owners read "Schema", "Sign-off" and "Rulings" directly (D3-662).

## Status

Current at 18:02 UTC (clock read). My three tasks are done; what is left is a recheck at the builder's next run.

- **Part A closed (17:48 UTC).** A1 to A5 signed off (17:27 to 17:35), the editor's later S74 and S71 words (17:39) and S73's trim (17:54) signed off; A2 to A5 change no figure and A5 changes words only. A6 passed (the engineer). S73 was ruled to come back to 14,106 bytes or under with its frame; the editor cut note 4's last sentence, and the main session's final strict build measures it.
- **Decisions file signed off (17:35 UTC)**, `work/handoffs/phase-3/20261113_Board-2-Decisions.json`: four panels, 31 items (S05 added at 17:51), `counts` and `checks` from `work/build/scripts/phase-3/board_2_data_lead_counts.py`. The editor owns the words and is editing them in place; my field edits since are logged under "Decisions file: my field edits".
- **Board figures signed off (17:52 UTC)** on the builder's first full build: 54 of 54 checks agree by `scratch/.../data-lead/scripts/board_figures_check.py`. At the 17:51 run the only differences are words the editor changed after that run; no figure differs. The builder's next run prints S05's item, S04's and S08's rows and the DR-229 table without its false "No"s; rerun the script then (`python3 -I <script> <builder scratch> <out.json>` from the brand guide folder).
- **Recommendations for Dustin:** S12, the stacked tile; the loop label question, each variable's own title everywhere; the V7.1 items as listed, RL-3 off the list.

### Log, newest first

- 17:53 UTC. S04 and S08 named in panel 1 with their causes (D3-555's pixel grid, D3-946's knockout); "Sign-off" has the trace.
- 17:52 UTC. The board's figures signed off on the builder's first full build ("Sign-off").
- 17:48 UTC. Part A closed. S73's weight ruled. A4 and the S12 stacked tile picture confirmed.
- 17:39 UTC. The editor's S74 and S71 changes signed off before A6. Replies and requests written.
- 17:35 UTC. A1 to A5 all signed off; the engineer may run A6. Decisions file `state: "signed off"`.
- 17:33 UTC. Decisions file, second draft: the V7.1 and "answered" panels; S12's recommendation changed to the stacked tile ("Rulings").
- 17:25 UTC. Decisions file, first draft; `counts` and `checks` written by the script.
- 17:14 UTC. Schema agreed with the board builder: my schema below plus its six additions (`state`; `spec` and `rule`; picture `role` and `element`; `facts`; `rows` fields; `counts` as proposed). For the builder: `counts.rule_01_9` holds the board's table at the top level (108 examples, limits 27 and 21) and `built` holds the 97 as built; `counts.dr_229.examples` rows carry `passes` true, false or null (null where the test was not applied). Optional fields added later: `facts`, `question`, `list_item`, `list_note`, `list_file`, and `old`/`new` on DR-255.
- 17:09 UTC. Started. Read CLAUDE.md, my role file, the brief, the decision log from D3-1312 to DR-260, V23 section 1, my round 3 notes and Gate 2's section 9.

## Schema for the decisions file (proposed 17:09 UTC, for the board builder)

File: `work/handoffs/phase-3/20261113_Board-2-Decisions.json`, UTF-8 JSON, written by me; the editor owns the words in `title`, `answer`, `what_changed`, `why`, `recommendation`, `question` and the `views` texts once I have written them. Every figure in it is read by script; the builder prints words as stored and reads pictures from the paths named.

```
{
  "schema": "board-2-decisions/1",
  "updated_utc": "2026-11-13T17:09:00Z",
  "written_by": "data lead",
  "words_owner": "editor",
  "reply_line": "To answer, reply “As recommended”, or name the item and your change.",
  "panels": [                         // panel 1's groups, in board order
    {
      "id": "board-1-changed" | "forms-changed" | "atlas-v7-1" | "answered",
      "title": "Board 1 drawings that changed",
      "lede": "one or two sentences: the answer and the studio's recommendation",
      "approval": "one" | "each",      // one approval for the lot, or one per item
      "items": [ ITEM, ... ]
    }
  ],
  "counts": {                         // panel 5 (and the count line on panel 1)
    "script": "work/build/scripts/phase-3/board_2_rule_01_9_count.py",
    "output": "work/handoffs/phase-3/20261113_Board-2-Decisions.json#counts",
    "run_utc": "...",
    "rule_01_9": {
      "limits": {"domain": "1 in 4", "state": "1 in 5"},
      "total_examples": 108,
      "by_domain": [ {"domain": "...", "count": n, "limit": n, "passes": true}, ... ],
      "by_state":  [ {"state": "California", "count": n, "limit": n, "passes": true}, ... ],
      "ruling_g": 108, "recount": n, "note": "what the recount gives against ruling (g)"
    },
    "dr_229": {
      "test": "D3-689's test, in words",
      "forms": [ {"rule": "14.x", "spec": "Sxx", "form": "...", "election_data": true, "passes": true, "why": "..."} ],
      "count": n, "note": "..."
    }
  }
}
```

ITEM (every item has the first eight fields; the rest only where they apply):

```
{
  "id": "S12" | "S16" | "S10" | "placement" | "round-1-notes" | "S73" | "Q-18" | "DR-254" ...,
  "title": "short name",
  "answer": "the answer in a sentence or two",
  "what_changed": "...",
  "why": "...",
  "recommendation": "...",
  "refs": ["D3-1372", "DR-64", ...],          // small reference line only
  "pictures": [ PICTURE, ... ],               // [] if none
  "question_for_dustin": true | false,        // true only where Dustin decides something still open
  "views": [ {"who": "data lead" | "creative director", "text": "...", "source": "path#key"} ],   // S12 only
  "old": "...", "new": "...",                 // answered items, words before and after
  "rows": [ {"spec": "S69", "where": "caption", "old": "...", "new": "..."} ],  // lists (A1 nine places, A5 lines, placement moves, round 1 notes)
  "new_to_v7_1_list": true | false,           // atlas items only, against work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md
  "tier": {"plan": "core", "built": "core"},  // forms-changed only
  "plan_row": {"file": "work/handoffs/phase-3/...Data-Plan...", "said": "..."}, "built": "..."   // forms-changed only
}
```

PICTURE: `{"kind": "guide" | "kit" | "board-1" | "board-pictures" | "file", "spec": "s12", "width": 1440, "ground": "newsprint" | "charcoal", "path": "repo path or null", "label": "Board 1, 1024 px"}`. `guide` means a photograph of the strict build at that window width; `kit` a kit capture; `board-1` a file under `work/boards/phase-3/round-0/`; `board-pictures` a file in `work/handoffs/phase-3/board-2-pictures/`; `file` any other repository file at its path.

## Rulings

### A2, sketch 14.124: one request before sign-off (17:18 UTC, for the cartographer)

Read by script from `work/build/guide/specimens/s-14-124-sketch.html` against the committed gray file (`33dc30a3`): the places, their sizes and positions are byte for byte as signed off (Party A seven small places, Party B five large blocks), the better half is unchanged, the file is 3,932 bytes under R3-9's 4,096, and neither `#CC0000` nor `#2C7BB6` is any value in `tokens.css`. No figure changes. One item:

- **The two fills are too close in lightness for a sketch whose places carry no words.** The kit's own key test (`checks.js`, `KEY_LIGHTNESS_MARGIN` 10: the smaller of the CIE L* gap and the grayscale proof's luma gap, for fills told apart by fill alone) reads `#CC0000` at L* 42.5 and `#2C7BB6` at L* 49.6, a gap of 7.1, though their luma gap is 26. The sketch never runs through that check, but the standard is the guide's, and the lesson's second harm (land for votes) needs a grayscale reader to see which places belong to which party.
- **Asked:** keep the red and lighten the blue until the gap is 10 or more by that test, staying a plain news blue far from Prussian. For example `#3A8AC4`: L* 55.1, gap 12.6, 3.1 to 1 on Newsprint and 4.3 to 1 on Charcoal (my figures, a one-off check in my scratch). Any blue that passes the test and the ΔE distance you measured is fine; say which in your notes and I sign off.

### S12: the stacked tile, recommended (17:33 UTC)

My first draft (17:25) recommended the 1,024 px frame as built, on the belief that the stacked tile fits only from a 723 px column. The cartographer's measure (`work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Measure.json`, 17:27 UTC) changes that, and I changed the recommendation:

- The stacked tile holds every code, figure and arrow in all 51 tiles from a **618 px** drawing, which the guide's column gives from a **1,104 px** window. At 1,440 px it draws the whole map in the column (723 px, 54 px tiles) with the chapter list in place; the frame as built shows 943 of 1,024 px there and hides the chapter list.
- Where the column is narrower (windows from 1,024 to 1,103 px), the stacked tile held in a 618 px frame scrolls about 60 px, against 468 px for the 1,024 px frame. This is my round 3 C-M2 ruling's order (point 3): the stacked tile first, and a stage at the narrowest width that fits where it does not.
- **The cost, stated on the board:** arrows at 3.8 px a point against board 1's 6.2, so 12 states' small shifts draw as an arrowhead alone at 1,440 px against 6; a change to a drawing Dustin approved; and the kit bytes of a stacked layout, which the engineer has not measured. The figure in every tile carries each value either way, and the encoding, scale rule, inks and words are board 1's.
- Read from both sides: no party or side is named in the choice; New York, New Jersey, Florida and California, the title's states, are in view at 1,440 px either way.
- I looked at the cartographer's 1x captures of the stacked tile at 1,440 and 1,024 px on Newsprint (`scratch/.../cartographer/shots/stacked/`) and board 1's 1,024 px drawing. At 1,024 px the forced stacked tile runs its arrows past the tiles' feet, as the measure says, so the board labels that picture as the width that needs the 618 px frame.
- The creative director's view goes beside mine, quoted from the rescores, with a note that it was written before the frame widened over the rail and before the 618 px measure.

### Counts and checks by script (17:16 UTC; the script is `work/build/scripts/phase-3/board_2_data_lead_counts.py`)

- **Tiers: no form's tier changed.** All 114 forms of rounds 1 to 3 (50 core, 36 extended, 21 reference, 7 avoid, Gate 2's table) read the same tier in the coverage plan, the chapter 14 plan, the data plans' rows, each entry file and each spec (S06 and S13 each serve two forms and are left out of the spec column). Every form matched a coverage plan row.
- **Datasets against the plan rows:** all 84 specs (86 plan rows; S06 and S13 serve two each) traced through each derived sidecar's `derived_from`. Five do not read as their plan row: S73 draws none of the planned file (`fec-jfc-transfers-2024-all-committees` in place of `fec-jfc-transfers-2024`); S59 adds `fred-unemployment-fourth-quarter` (round 2's RF-20); S04, S05 and S20 add the Census Bureau's published margins files. S76's per-candidate netting and S78's line are changes of derivation and measure inside the planned files, which a file test cannot see; I list them by ruling.
- **Rule 01.9:** the recount gives 97 examples as built (13 rule plates and 84 specimens, equal to the generator's log) and 108 with round 4's 11 rows as planned, ruling (g)'s figure. The largest domain is taxes, wealth and economic security, 16 of 108 against 27; California and Florida 5 each against 21. Every domain and state passes at 97 and at 108.
- **DR-229 under D3-689:** 17 examples draw election or voting data: 12 in elections and representation, 5 voting examples counted under taking part. All five new forms that keep election data pass the test (S26, S48, S67, S80, S82). Eight are Phase 2 specimens board 1 approved before the test (S03, S04, S07, S08, S11, S12, S15, S16; S11 and S15 pass it anyway), and four are rule plates. Round 4 plans no election data.

## Sign-off

How I check Part A: a script (`scratch/.../data-lead/scripts/parta_diff.py`) compares every spec, entry, sidecar, `words.json` and specimen file with the committed state before Part A (`33dc30a3`, copied to my scratch at 17:16 UTC) and lists every changed field with the figures in its old and new words; `a5_lines.py` counts October 15, 2026 in each spec's printed source, grade and measure lines. No CSV in `work/build/data/` may change.

### A5, the research lead's six variants: signed off (17:25 UTC)

- Each of the six sidecars (`v7-claims-by-grade`, `v7-claims-by-hub-and-grade`, `v7-claims-drug-prices`, `v7-issue-status-checks-on-power`, `v7-issues`, `v7-numbers`) gains one key under `source_line_variants` and nothing else: `printed_source_line` and every older variant are unchanged, by script.
- Each new line prints October 15, 2026 once (each old line twice), and keeps every other figure of the old line: 433, 16, 432 and 433; 11; 17 and 194. S39's line adds "all 11", the count it already names.
- The two new sentences are true of the model, by script on `work/extract/atlas-v7-data.json`: 432 of the 433 claims carry `verified_on` 2026-10-15 (CL1723 none); all 11 drug-price claims (CL1357 to CL1367) carry 2026-10-15; all eight headline figures read "checked October 15, 2026"; all six statuses in S63's file carry `checked` 2026-10-15.
- No CSV changed. This half of A5 changes words only.
- The 21 lines of D3-1308: 6 print on the page, in S10, S21, S23, S38, S39, S60 and S63; the other 15 print nowhere, so no reader meets them and the board says so. Recounted by script on the committed sidecars: 21 lines in nine sidecars.
- Waiting: the editor's `source_line` keys in the seven specs, which I check by `a5_lines.py` (no spec's source line may print the date twice).

### A5, the editor's seven specs: signed off (17:27 UTC). A5 is signed off whole.

- `a5_lines.py` on the specs as they stand: no spec's printed source line holds October 15, 2026 twice (seven did at `33dc30a3`: S10, S21, S23, S38, S39, S60, S63). Each of the seven now copies its sidecar's `snapshot_once` variant exactly (the kit's check accepts no other line).
- `parta_diff.py`: in each of the seven specs only `source_line` changed; its figures are the old line's less one October 15, 2026. Grade lines unchanged; S60's and S63's keep "as of October 15, 2026", as S68's does (D3-1493).
- Weights, from the editor's and the research lead's notes (frame included): S10 8,153 to 8,156; S21 6,429 to 6,432; S23 6,959 to 6,962; S38 10,791 to 10,767; S39 11,027 to 11,031; S60 9,811 to 9,827; S63 11,105 to 11,081. All under the 13,322 share and 15,000.
- **A5 changes words only.** No CSV and no data JSON changed (125 of 125 files equal to `33dc30a3`, by `cmp`), no drawing and no table.
- Noted for the editor, not part of A5: the snapshot date still prints twice on some older plates outside the source line, which DR-257 did not name. S10 and S21 print it in the measure line and the source line; S74, a round 3 spec, prints it in the grade, measure and source lines, where D3-1485 would drop it from the measure line. I ask nothing for this board; the editor may take S74's measure line in the fix round.

### A1, DR-254: signed off (17:27 UTC)

- **All nine places name the file through `{data_file}`**: the captions of S69, S70, S72 and S73; S73 note 4, S74 note 4, S81 note 4, S83 note 3 (as printed); entry 14.120's rule text. By script over every spec and entry: 9 strings hold `{data_file}`, none opens a sentence (D3-1529), and `words.json`'s `data_file` is DR-254's phrase exactly (the engineer's read).
- **No reader text promises "the download" or "the CSV file".** By script over every spec and entry string a reader meets: two hits, both written by the rules generator, both naming chapter 18's download rule by its subject (Rule 14.14's "as Rule 18.14 asks of a download"; chapter 14's related-chapters line, "tables and named downloads"). Neither promises this chart's data to a reader, so I accept both; the editor's request for literal zero is the main session's call.
- **The raw placeholder the editor found** (the caption's two hidden copies, the table's name and the summary words) is fixed in `kit-build.js` by the engineer (17:20 UTC); I read the diff: two lines, both through `K.fill_words`, nothing else.
- **No figure changed.** `parta_diff.py`: every changed field keeps its figures but S69's caption, which drops "from the Clerk’s file of November 3, 2026"; S69's grade line holds that date ("the Clerk of the House’s committee list of November 3, 2026"), so this is D3-1485's rule and words only. The engineer's export check holds every row of the eight charts' CSVs (S69 136, S70 111, S72 533, S73 125, S74 44 cells, S81 3,144, S82 435, S83 3,144).
- Weights with the frame (the editor's and engineer's notes), before A1 to after the caption fix: S69 14,369 to 14,366; S70 10,703 to 10,871; S72 7,802 to 7,934; S73 13,913 to 14,087 (19 under D3-1328's 14,106); S74 11,707 to 11,750; S81 13,597 to 13,640; S83 13,295 to 13,338. None passes a ceiling, and S69 does not grow (D3-1412).

### A3, the check's one exception: signed off (17:27 UTC)

I read the diff of `work/build/scripts/phase-2/guide_build.py` against `33dc30a3`: `LITERAL_HALF = {"s-14-124-sketch": 0}` with DR-64's one exception recorded in its comment, five lines in `process_fragment` that drop the first `<svg>` of that specimen's avoid pair from the literal color scan only when the file holds exactly two drawings, and a self-test scenario that proves the better half and another avoid sketch still warn. Nothing else in the check changed. The engineer reports `--self-test` 33 of 33 and the guide check and kit check passing the drawing with no exemption; I did not rerun them.

### A2, DR-255: signed off (17:29 UTC)

- The cartographer took `#3A8AC4` for the blue at 17:28 UTC. By the kit's key test the two fills now differ by 12.6 (L* 42.5 and 55.1; luma gap 82), over its 10. **My request carried one wrong figure:** I measured contrast against `#ECEAE6`, but Newsprint is `#DCD9D2` (`tokens.css`), so the blue reaches 2.65 to 1 on Newsprint, as the cartographer says, not 3.1. Every place keeps its 1 px context edge, which carries its outline at 4.29 to 1, so the shapes stay apart from the ground; I accept it.
- By script against `33dc30a3`: the places' paths and rectangles are unchanged (seven small places for Party A, five large blocks for Party B); the only geometry added is the context edge round the large blocks and the second swatch. The better half is byte for byte as signed off. The file is 3,941 bytes, under 4,096. Neither `#CC0000` nor `#3A8AC4` is a value in `tokens.css`.
- The caption (`sketch_alt`'s first sentence) and the first `<desc>` match character for character: "A map that shades Party A’s seven small places red and Party B’s five large places blue, which takes a side at a glance and makes Party B look bigger than its count." Seven and five are the drawing's counts. The key names each color.
- Looked at: the cartographer's 1x grayscale comparison on both grounds (`scratch/.../cartographer/shots/a2-gray-compare.png`, 17:16 UTC, with the earlier blue): the bar, the label, every place and its edge read; Party A's small places are the darkest marks and Party B's large blocks a mid gray. The blue has since only grown lighter, which widens that gap. I did not render the final file myself.
- **A2 changes no figure.** The do-not-publish bar is the guide's own.

### A4, DR-256: the words signed off (17:27 UTC); the layout waits on the cartographer

- Note 3's range and the alt's last sentence read DR-256's words exactly.
- Every figure checked by my own script on `census-cps-2024-turnout-by-state.csv` (2024 rows, 50 states and DC): Arkansas 52.8 (±2.7) is lowest, past the gap's margin to the next place (Texas 57.9: 5.1 against 3.55; Louisiana 58.0: 5.2 against 4.50); DC 79.5 (±3.3) is highest and within the gap's margin of exactly two places, Minnesota 75.9 (3.6 against 4.39) and Oregon 75.3 (4.2 against 4.33); the next, Virginia 72.9, is past it (6.6 against 4.08). The words add two figures, 75.9 and 75.3, both values in the file; no other figure moved.
- S16's weight 10,732 to 10,933 with the frame (the editor's build), under every ceiling. I sign off A4 whole when the cartographer reports the layout at every width the sweep runs.

### A4, the layout: signed off (17:35 UTC). A4 is signed off whole.

- The cartographer's report (17:34 UTC): `oa-chart.mjs build s16`, sweep on, PASS, 0 faults, 0 warnings, over every whole width from 256 to 869 px and the 1440 and 390 px pages on both grounds; S16 drawn as committed before Part A and as it stands, 1,230 of 1,230 drawings equal with the alt set aside. Codes placed as round 3 left them (all 51 from 358 px up). I read the report and did not rerun it.
- Note 3 wraps in eight lines at 390 px with no break inside a figure and its margin. "DC" ends one line and "79.5% (±3.3)" opens the next; a no-break space after "DC" is the editor's choice, words only, and does not block A4.
- **A4 changes words only:** two sentences, figures checked by script against the data above.

### Part A: A1 to A5 all signed off (17:35 UTC). The engineer may run A6.

For the main session and the engineer: A1 (17:27), A2 (17:29), A3 (17:27), A4 (17:35) and A5 (17:27) are signed off, each under its heading above. A2 to A5 change no figure, and A5 changes words only: every changed field was compared with the committed state before Part A (`33dc30a3`) by script, figure by figure, and no file in `work/build/data/` but six sidecars' added variants changed (125 of 125 data files equal). Plate weights before and after are listed under A1 and A5; S16 10,732 to 10,933 and sketch 14.124 3,817 to 3,941 bytes; none passes D3-1328's ceilings or R3-9's 4,096. Two items for the editor's fix round, neither blocking: S74's measure line still prints the snapshot date that its grade and source lines print (D3-1485), and "DC" could hold to its figure in S16's note 3.


### Two editor changes after the Part A sign-off, before A6: signed off (17:39 UTC)

The editor changed two specs after my 17:27 field comparison: S74 at 17:28 and S71 at 17:37 (file times). Both are words only, and **A6 should run on the specs as they stand now**, which hold both.
- **S74:** the measure line and the table caption drop "as of October 15, 2026"; the grade line ("as of October 15, 2026") and the source line ("snapshot of October 15, 2026") still print it. D3-1485's rule, the item I left to the editor at 17:27. No figure moves.
- **S71:** a `typography.replace` pair prints the four state constitutions' web addresses (Massachusetts, Nebraska, Virginia, Arizona, in the row's own order) in place of the stored cell "work/research/20261111_Policy-Workflow-Sources.md, section SS", a studio path a reader would have met in the table. Each address is in that sources file, by `grep`. Printed words only (D3-519): the CSV export still holds the path, which goes to the main session as the editor asks (under "Requests").
- The rest of the comparison is as at 17:27: no data file changed, and the only other file the editor's later work touched is the guide's specimen manifest, whose S16 and sketch 14.124 alt texts follow the signed-off words.
### S73's weight after A1: trim it (17:48 UTC, for the editor and the main session)

The engineer's A6 measures S73 at 14,148 bytes with its frame on the page, 42 over D3-1328's 14,106 (under 15,000; no check fails). **Ruled: the editor trims S73's words until the page measure is 14,106 or under.** D3-1328 bars a round 3 plate from growing past the share, and S73 grew with A1's phrase; D3-1412 let S69 stand only because it shrank, so it does not reach S73.
- **The cut I recommend:** drop note 4's last sentence, "Each, with its transfers, is in {data_file}." The table caption already says "every committee is in" the data file, so the promise stays on the plate once, and the note keeps every figure and its count rule ("a committee two funds paid counts once"). It is about 45 characters of the note's words.
- The editor may choose another cut, under three conditions: no figure, name or count leaves the plate; the data file is still named once on the plate; the title, bar heads and note 2's July 21, 2024 split are untouched.
- The editor measures the plate after the cut with the kit and the main session's final strict build confirms it; I sign off the words when they land (a cut that only removes a sentence needs no new figure check).

### A4 and the stacked tile picture: confirmed (17:48 UTC)

- **A4 is signed off whole:** the words at 17:27 and the cartographer's layout at 17:35 (both under their headings above).
- **The S12 stacked tile picture is signed off** (board only, nothing in `work/build/` changed). Its spec, `work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Spec.json`, equals `s12.json` but for four keys: no `stage`, `labels.stack: "force"`, the alt's clause on the frame, and a board-only line in `notes_internal`. By script on the 1,440 px file, all 51 state codes print with a figure, and each figure equals the state's `shift_pts` in `fec-presidential-shift-by-state.csv` to one decimal; "United States 5.9" and the largest and smallest lists print as on S12. The measure file's figures are the ones the decisions file quotes (618, 1,104, 54, 3.8 against 6.17, 12 against 6). The 1,024 px picture forces the layout into a column it does not fit, as the board's label says.

### Part A closed (17:48 UTC)

A1 (17:27), A2 (17:29), A3 (17:27), A4 (17:27 words, 17:35 layout), A5 (17:27) and the two later editor changes, S74 and S71 (17:39), are signed off; A6 passed (the engineer, as the main session reports: 84 of 84, 0 faults, strict build exit 0, 0 warnings, 11,236,319 bytes, share per plate 13,230). Every Part A item is closed. One follow-on is open and does not reopen Part A: S73's trim above, which the main session's final strict build measures.

### The board's figures, first full build: signed off with two corrections of mine (17:52 UTC)

Read the builder's first full build (17:48 UTC) and its 17:50 rerun (`work/boards/phase-3/round-3/board-2/20261113_Board-2.html` and `-Figures.json`, the builder's strict build report in its scratch). My script, `scratch/.../data-lead/scripts/board_figures_check.py`, reads each figure the board prints against the file it comes from: **54 checks agree, 0 differ** on the figures the board drew from today's files.
- **Forms (panel 2):** 114 forms, 86 rows with a chart, 84 charts, 28 sketches, as the plan holds them; each form's name, tier, round and maker against its plan row; each chart's bytes with the frame, bytes as drawn and fault count against its kit check file; each printed title against its spec (spaces folded); each evidence label against the spec's kind; the seven Estimate charts (14.60 to 14.62, 14.76, 14.77, 14.127, 14.129) against the specs marked estimate.
- **Spend (panel 5):** chapter 14 with the kit 2,228,367 of 2,803,941; the kit 512,961; map shapes 133,117 of 250,000; rules with the opener 175,678 of 212,288; the projection 15,044,827 of 15,500,000; the share per plate 13,230 for 13 plates to come; the strict build 11,236,319 bytes, 344 rules, 638 placed, 0 warnings. Each equals the strict build report and the engineer's A6 table. Bytes by family, chart by chart as placed and each sketch entry's bytes, all 14 families; the ten heaviest charts and their bytes.
- **Scores (panel 6):** all nine red team reports' first scores, Must fix and Should fix counts and second scores, which I parsed from the reports myself; the creative director's ready counts for rounds 1 to 3 (0, 2 and 2 of 5 first; 5 of 5 after).
- **Count (panel 4):** every Rule 01.9 domain and state row on the page with its count; the DR-229 table as the decisions file holds it.
- **Tested (panel 7):** the strict build line equals the report; the engineer's line equals its A6 table; the quick check line (694 examples, 3,296 links) equals D3-1537.
- **Panel 1:** every item's answer, what changed, why and recommendation printed as stored.
- **Cover:** 114 forms in 14 families, 86 with a chart and 28 with a sketch.

**Two corrections, mine, that reach the board at its next run (the builder reruns `--reuse`):**
1. The builder's pixel comparison found S04's and S08's desk drawings off board 1's and unnamed in panel 1. My crops of all fourteen board 1 charts that differ found one more change of substance: **S05 now draws four gap brackets and a 2003 tick** (round 1, D3-428), which board 1 gave in a note. Panel 1 now holds S05 as its own item, with its four figures checked by script against the Census file, and the placement list adds S04 (rules break round its labels) and S08 (two rules a pixel lower). Panel 1 now names all fourteen board 1 charts whose drawing differs; S03, S06 and S07 draw the same as on board 1.
2. The DR-229 table printed "No" under "Passes" for the twelve examples the test does not apply to; those rows now carry no value, and the test's words and two notes lost their decision codes (into `refs`).

**Not checked by me:** the pictures' pixels beyond the board 1 comparisons (the builder photographs them from the strict build and the kit); the rules panel's photographs; the image and folder byte counts; the board's own check results (the builder's); the creative director's score of this board, still to come.

### S73's trim: the words signed off (17:54 UTC)

The editor dropped note 4's last sentence, "Each, with its transfers, is in {data_file}.", the cut I recommended. By `parta_diff.py`, note 4 and the table caption keep every figure; the caption still names the data file ("every committee is in" it), so the plate names it once. Not tested by me: the plate's page weight after the cut, which the main session's final strict build measures against 14,106. The editor's words in the decisions file's DR-254 item already say eight of the nine places name the file; I set the S73 note row's new words to the note as it stands.

### S04 and S08 against board 1: named in panel 1 (17:53 UTC, for the main session)

The builder's run 6 found S04's and S08's desk drawings off board 1's pixel for pixel. I diffed board 1's SVG files (`work/boards/phase-3/round-0/specimens/20261112_S04-…` and `…_S08-…`) against today's kit drawings:
- **S08:** every difference is a 1 px rule moved half a pixel (for example `y1="66"` to `"66.5"`), the round 1 fix pass's pixel grid (D3-555: straight lines of a whole-pixel width snap to the grid so they draw crisp at 1x; the engineer's round 1 notes count the board 1 specimens among the 48 specs it moved). No word, figure or square moved.
- **S04:** the same half-pixel move of its row rules, and four knockout rectangles in the ground's color where a rule crosses a value label, round 2's kit fix (D3-946, BC S1). No word or figure moved.
- Both are in panel 1's placement list now, each with one plain line and its codes, and the list's "what changed" says once that the round 1 pixel grid moved lines in most board 1 drawings by up to half a pixel. The same cause explains the faint differences in S01, S02, S09, S11, S13 and S15, so their rows keep only the moves their owners made. With S05 (gap brackets, D3-428, added at 17:51), panel 1 names all fourteen board 1 charts whose drawing differs; S03, S06 and S07 match board 1.

## Replies and requests

- **To the editor, the decisions file's words (17:39 UTC): agreed.** Every panel is written. I do not rerun `write_decisions_v1.py` or `patch_decisions_2.py`; any later change of mine is a targeted edit of one field, logged here, and `board_2_data_lead_counts.py --write` touches only `counts` and `checks` and keeps each `note`. Edit the word fields in place as you propose. Figures stay mine: a sentence whose figure you move comes back to me.
- **To the editor, straight apostrophes in S21, S09 and S10's tables (17:39 UTC): yes, in the fix round.** Each takes `"typography": {"curl_quotes": true}`, printed words only (D3-519), with the data as stored; S09 and S10 are board 1 charts, and a curled apostrophe moves no figure or mark. Not before A6, so A6 runs on the state I signed off.
- **To the main session:** S71's data file `usgov-v7-route-grid.csv` stores a studio path in the SS row's `url` cell, which the chart's CSV export would ship under DR-254. The page now prints the four addresses; the stored cell is maker A's derive or the research lead's, before Phase 5's package.
- **To the main session:** the two generator lines that still say "download" (Rule 14.14's "as Rule 18.14 asks of a download"; the related-chapters line's "named downloads") promise no file; I accept them as they stand, and the editor's words for a literal zero are in its notes if you want them.

## Decisions file: my field edits after the second draft

Each a targeted edit of one field, for the editor's table.

| UTC | Item, field | Why |
|---|---|---|
| 17:34 | `S10`, `answer` and `what_changed` | Board 1 drew the "All 433 claims" line solid; the first draft called it a bar |
| 17:34 | `placement`, `title`, `answer`, `what_changed`; `board-1-changed`, `lede` | S14's note moved at every desk width, so "at widths board 1 did not show" was too broad |
| 17:34 | `placement`, row S05 | Drawing order only, said without a negation |
| 17:35 | `S73` `why`; `RL-3` `answer`; `R-01` `what_changed`, `why` | Corrective negations rewritten (chapter 02) |
| 17:43 | `placement`, `what_changed` | The owners compared each drawing with itself before its move, not with board 1's files; my pixel check finds S01 and S02 a pixel or so off board 1's 1,440 px files (S01's leader, S02's antialiasing) and S14's note 10 px higher, as its row says |
| 17:51 | new item `S05` in `board-1-changed`; `board-1-changed` `lede`; `placement` `title`, `answer`, rows S09 and S15 reworded, rows S04 and S08 added | The builder's pixel comparison (17:48) found S04's and S08's desk drawings off board 1's and unnamed; my own crops of all fourteen that differ show S05's four gap brackets and 2003 tick (D3-428, round 1), S04's rules breaking round its labels (D3-946), S08's two rules a pixel lower, and S09's and S15's lines a pixel off. S05's four figures checked by script against the Census file (Hispanic 28.7 and 25.8, Black 27.3 and 29.6) |
| 17:52 | `S12` creative director's view `note`; `S16` `what_changed`; `DR-255` `answer`; `counts.dr_229` `note` | Decision codes (D3-1515, DR-256, DR-64, D3-689) out of the words on the board's face; each code is in the item's `refs` |
| 17:52 | `counts.dr_229` (script): `test` without its code, `refs` added on both counts; each row's `passes` null where the test was not applied (rule plates, Phase 2 specimens), and `data` and `test` words capitalized for a table | The board's 17:48 table printed "No" under "Passes" for twelve examples the test never applied to, which read as failures |
| 17:53 | `placement`: `what_changed` adds the round 1 pixel grid; rows S04, S08 reworded with their causes; rows S09, S15 drop the pixel clause; `refs` add D3-555, D3-946 | The main session's question on S04 and S08; one cause stated once |
| 17:54 | `DR-254` row S73 note 4 `new` (the editor had already rewritten the answer; my appended sentence removed at once) | The editor's S73 trim removed that place's line |

## Routine calls

- D3-xxx | The decisions file's schema is the data lead's of 17:09 UTC with the board builder's six additions (`state`, `spec` and `rule`, picture `role` and `element`, `facts`, `rows` fields) | Agreed within the brief's first 20 minutes; the builder prints only what the file holds
- D3-xxx | Board 2's Rule 01.9 and DR-229 counts come from `work/build/scripts/phase-3/board_2_data_lead_counts.py`, which also checks every form's tier and every spec's files against its plan row and writes `counts` and `checks` into the decisions file, keeping the editor's `note` words | One script the main session can rerun; the brief asks for a recount by script named in the file
- D3-xxx | DR-229's count takes election data as the elections and representation domain plus reported voting counted under taking part; campaign money (S73, S76, S36, Rule 14.13's plate) counts under money, as ruling (g) set | One reading of "election or voting data" (Gate 2 question 1) across the chapter
- D3-xxx | D3-689's test is applied to forms built in rounds 1 to 3; Phase 2's specimens approved on board 1 and the rule plates are listed with the test's result and are not moved by it | DR-229 keeps every form and its approved drawings; the test governs new picks
- D3-xxx | The forms-changed list names nine specimens changed after their plan row was signed off (S73, S76, S78, S80, S59, S54, S55, S41, S20) and lists the seventeen data plan changes separately; S04's and S05's margins files are left out | Their margins files (P7-037, P7-038) date from round 0, before board 1 showed both drawings
- D3-xxx | Sketch 14.124's two fills differ by 10 or more on the kit's key test (`KEY_LIGHTNESS_MARGIN`, the smaller of the CIE L* and grayscale luma gaps); the blue is `#3A8AC4` | The places carry no words, so a grayscale reader needs the gap the guide asks of any key told apart by fill alone
- D3-xxx | A2 to A5 are signed off on a field-by-field comparison with the committed state before Part A (`33dc30a3`), every figure in each changed string listed old and new, and a `cmp` of all 125 data files | "No figure changes" is checked by script, not by reading
- D3-xxx | The 15 of D3-1308's 21 atlas source lines that print nowhere stay as stored; board 2 says so | DR-257 fixes what a reader meets; a future spec that prints one takes a `snapshot_once` variant
- D3-xxx | S12's recommendation is the stacked tile at every desk width, held in a 618 px frame that scrolls where the column is narrower; it replaces my first draft's recommendation of the 1,024 px frame | The cartographer's measure: the stacked tile fits from 618 px (a 1,104 px window), shows the whole map at 1,440 px and scrolls about 60 px at 1,024 against 468; C-M2 point 3
- D3-xxx | The loop label question (D3-912) is recommended "yes": each variable's own title in every loop drawing in chapters 10, 11 and 15, and in V7.1 | The titles carry no verdict and need no gloss ("Executive unilateralism", "Policy tilt to insiders", "Affective polarization" do); one name per variable; the costs (longer words, CL-026's printed name) go on the board
- D3-xxx | RL-3 is recommended off the V7.1 list | No atlas record names joint fundraising; the fact lives in the two FEC sidecars
- D3-xxx | The issue title item asks one test for all 18 atlas titles with an effect verb, whoever the actor | DR-93; five concern the executive and thirteen do not, and a test applied to five alone would be one standard for one side
- D3-xxx | S74's measure line and caption drop the snapshot date its grade and source lines print, and S71 prints the four constitutions' addresses in place of a studio path; both signed off before A6 | D3-1485; no studio path in reader text (H11); words only
- D3-xxx | S21, S09 and S10 curl the atlas's straight apostrophes in their tables in the fix round, not before A6 | D3-519's printed-words rule; A6 runs on the state signed off at 17:35 and 17:39
- D3-xxx | S73 comes back to 14,106 bytes or under with its frame by the editor's least cut, recommended as note 4's last sentence, since the table caption already names the data file | D3-1328 bars a round 3 plate from growing past the share; S73 grew 42 bytes over it with A1's phrase; D3-1412's exception covered a plate that shrank
- D3-xxx | Part A is closed at 17:48 UTC, with S73's trim as a follow-on that does not reopen it | Every A item and the two later editor changes are signed off and A6 passed
- D3-xxx | The decisions file is `state: "signed off"` from 17:35 UTC, and the editor edits its words in place from 17:39 | Every panel written; figures checked by script; the editor owns the words (brief)

## Tested

- `board_figures_check.py` on the builder's 17:48, 17:50 and 17:51 runs: 54 checks agree each time; the only differences at 17:51 are panel 1 words the editor changed after that run.
- `diff` of board 1's SVG files against today's kit drawings for S04 and S08 (half-pixel line moves; S04's four knockouts); pixel crops of all fourteen board 1 charts that differ; S05's four gap figures by script against `census-hvs-homeownership-by-race-annual.csv`.
- `parta_diff.py` after S74's, S71's and S73's later edits (figures kept; S71's four addresses found in the sources file by `grep`).
- Clock read with `date -u` at 17:35, 17:38, 17:39, 17:43, 17:48 and earlier at 17:07, 17:08, 17:10, 17:13, 17:14, 17:15, 17:17, 17:18, 17:19, 17:22, 17:24, 17:25, 17:26, 17:27, 17:29 and 17:33 UTC.
- `board_2_data_lead_counts.py` (`python3 -I`), run five times, the last with `--write`: 114 forms, tiers 50, 36, 21, 7, none changed, every form matched in the coverage plan; 84 specs traced through `derived_from`, five not as their plan row (S73, S59, S04, S05, S20); Rule 01.9 97 built (equal to `14-example-log.json`, domain by domain) and 108 with round 4, every domain and state within its limit; DR-229 17 examples, 5 new forms all passing.
- `a5_lines.py` before and after the editor's A5: source lines printing October 15, 2026 twice, 7 then 0; grade and source lines both printing it, 6 both times (S60, S63 and round 3's S67, S68, S71, S74).
- `parta_diff.py` against `33dc30a3`, three runs: every changed field in specs, entries, sidecars, `words.json` and the specimens folder, with figures old and new; `cmp` of 125 data files, all equal.
- By script on the committed sidecars: D3-1308's 21 lines in nine sidecars.
- By script on `work/extract/atlas-v7-data.json`: claims' `verified_on` (432 of 433), the 11 drug-price claims, the eight headline figures' status, the six status rows' `checked`; the 25 looped variables' titles against their chain labels (24 differ; mean length 36.5 against 22.0).
- By script on `census-cps-2024-turnout-by-state.csv`: A4's figures and the gap tests (Arkansas against Texas and Louisiana; DC against Minnesota, Oregon, Virginia and New Jersey).
- By script: `{data_file}` in 9 strings, none opening a sentence; "download" and "CSV file" in reader strings, 2 hits, both chapter 18 references.
- Lightness of the sketch's inks by the kit's own formulas (CIE L*, luma); contrast against `tokens.css`'s Newsprint.
- Read: the diffs of `guide_build.py` (A3) and `kit-build.js` (the caption fix) against `33dc30a3`.
- By script on the stacked tile's 1,440 px file: its spec against `s12.json` (four keys differ), and its 51 codes and figures against `fec-presidential-shift-by-state.csv` (0 mismatches).
- By pixels: board 1's 1,440 px files of S01, S02, S04, S10 and S14 against the builder's fresh kit drawings (S03 and S07 the same; S01 and S02 a pixel or so; S10's dashed line; S14's note 10 px higher); the other nine board 1 charts draw wider than the kit's capture and were not compared.
- `board_figures_check.py` on the builder's 17:36 build: 54 checks agree, 0 differ (forms' bytes, faults, titles and evidence labels against each spec and kit check file; estimate list; spend rows and share against the strict build report; bytes by family; the ten heaviest; nine red team reports' scores and counts, parsed independently; the creative director's ready counts; the Rule 01.9 rows and every decisions answer printed on the page).
- Looked at: the cartographer's grayscale comparison of sketch 14.124 (earlier blue), the stacked tile at 1,440 and 1,024 px on Newsprint, board 1's S12 at 1,024 px.

## Not tested

- S73's page weight after the trim, and every plate's page weight: the engineer's and the main session's strict builds measure them.
- The board's run after my 17:51 to 17:54 edits (S05's item, S04's and S08's rows, the DR-229 table): not yet built when I stopped.
- No build, capture or browser of my own: I ran no kit build, no guide build and no guide check. The engineer's export check, A3 self-test and kit checks, the editor's and cartographer's builds and weights, and the cartographer's color measures are theirs, read from their notes.
- Sketch 14.124 with its final blue, rendered: I looked only at the earlier blue's capture.
- S16's layout at the sweep's widths (the cartographer's A4 check, pending).
- The stacked tile's kit bytes and its behavior in the guide's page (it is a board-only picture).
- The live FEC, Census, Clerk, CMS and state election sources behind the V7.1 facts; I read the research lead's facts and the atlas extract.
