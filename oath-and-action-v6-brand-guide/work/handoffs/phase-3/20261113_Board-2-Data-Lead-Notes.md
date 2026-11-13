# Board 2 data lead notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. Data visualization and systems lead (`oa-dataviz-systems-lead`), under `work/handoffs/phase-3/20261113_Board-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/data-lead/`. Owners read "Schema", "Sign-off" and "Rulings" directly (D3-662).

## Status

- 17:09 UTC. Started. Read CLAUDE.md, my role file, the brief, the decision log from D3-1312 to DR-260, V23 section 1, my round 3 notes and Gate 2's section 9.
- 17:14 UTC. **Schema agreed** with the board builder (its notes, "Contracts", 17:12 UTC): my schema below plus its six additions, which I adopt as written: `state` ("draft" or "signed off"); `spec` and `rule` on every one-specimen item; PICTURE `role` (before, after, view) and `element`; `facts` (label and value pairs); `rows` may carry `spec`, `rule`, `what_changed`, `why`, `refs`; `counts` as proposed.
- Count script written and run: `work/build/scripts/phase-3/board_2_data_lead_counts.py` (tiers, datasets against plan rows, Rule 01.9, DR-229). First results under "Rulings".
- Part A sign-offs: none landed yet. The engineer's A1 export check is in (8 of 8 exports whole).

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

None yet.

## Routine calls

## Tested

## Not tested
