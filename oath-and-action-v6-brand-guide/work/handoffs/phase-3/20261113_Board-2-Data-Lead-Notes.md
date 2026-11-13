# Board 2 data lead notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. Data visualization and systems lead (`oa-dataviz-systems-lead`), under `work/handoffs/phase-3/20261113_Board-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/data-lead/`. Owners read "Schema", "Sign-off" and "Rulings" directly (D3-662).

## Status

- 17:09 UTC. Started. Read CLAUDE.md, my role file, the brief, the decision log from D3-1312 to DR-260, V23 section 1, my round 3 notes and Gate 2's section 9.
- Schema for `20261113_Board-2-Decisions.json` proposed below for the builder (deadline 17:27 UTC). The builder may answer under its own notes' "Contracts"; I adopt any field renames it needs.
- Part A sign-offs: none landed yet.

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

None yet.

## Sign-off

None yet.

## Routine calls

## Tested

## Not tested
