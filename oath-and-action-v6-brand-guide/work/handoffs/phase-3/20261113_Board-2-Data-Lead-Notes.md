# Board 2 data lead notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. Data visualization and systems lead (`oa-dataviz-systems-lead`), under `work/handoffs/phase-3/20261113_Board-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/data-lead/`. Owners read "Schema", "Sign-off" and "Rulings" directly (D3-662).

## Status

- 17:09 UTC. Started. Read CLAUDE.md, my role file, the brief, the decision log from D3-1312 to DR-260, V23 section 1, my round 3 notes and Gate 2's section 9.
- 17:14 UTC. **Schema agreed** with the board builder (its notes, "Contracts", 17:12 UTC): my schema below plus its six additions, which I adopt as written: `state` ("draft" or "signed off"); `spec` and `rule` on every one-specimen item; PICTURE `role` (before, after, view) and `element`; `facts` (label and value pairs); `rows` may carry `spec`, `rule`, `what_changed`, `why`, `refs`; `counts` as proposed.
- Count script written and run: `work/build/scripts/phase-3/board_2_data_lead_counts.py` (tiers, datasets against plan rows, Rule 01.9, DR-229). First results under "Rulings".
- 17:25 UTC. **Decisions file, first draft written:** `work/handoffs/phase-3/20261113_Board-2-Decisions.json`, `state: "draft"`. Panels: board 1 drawings that changed (S12 with both views, S16, S10, the eleven placement moves, the twelve note-word changes), forms whose tier or data changed (tiers by script; S73, S76, S78, S80, S59, S54 and S55, S41, S20; the seventeen plan changes), and `counts` and `checks` written by the script with `--write` (a rerun keeps the editor's `note` words). Still to come: the atlas V7.1 panel (waits on the research lead's facts), the "answered" panel (waits on A1 to A5), and S12's stacked tile pictures (the cartographer's files).
- **For the builder, the `counts` layout:** `counts.rule_01_9` holds the board's table at the top level (`total_examples` 108, `limit_domain` 27, `limit_state` 21, `by_domain` and `by_state` rows with `count`, `limit`, `passes`, `note`), and `built` holds the same for the 97 examples as built. `counts.dr_229.examples` rows carry `spec` or `where`, `rule`, `form`, `data`, `coverage_use`, `election_data`, `passes`, `test`; `note` is the words.
- Part A: A5's sidecar variants verified (below, "Sign-off"); A1, A2, A4 and the editor's A5 specs in progress. The engineer's A1 export check is in (8 of 8 exports whole). A2 has one request (lighter blue) under "Rulings".

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

## Routine calls

## Tested

## Not tested
