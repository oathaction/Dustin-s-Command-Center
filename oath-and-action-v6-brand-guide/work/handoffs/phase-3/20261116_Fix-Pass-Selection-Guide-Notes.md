# Fix pass notes: selection guide maker, "Choose a chart"

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7, November 16, 2026. Written by the selection guide maker (a general-purpose agent briefed as the senior information designer who drew chapter 14's "Choose a chart", its 133 symbols and its links) for `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md`, Addendum 1, calls 16 and 17. Paths are relative to `oath-and-action-v6-brand-guide/`. Files I write: `work/build/scripts/phase-3/selection_guide_build.py`, its outputs `work/build/guide/specimens/s-14-selection-guide.html` and `s-14-selection-guide.meta.json`, and these notes. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/fix/selection-guide/`.

## Status

17:45 UTC. Started. Read CLAUDE.md, the fix brief whole with Addendum 1, the creative director's R5-G reasons (review and scores file), AX-S4, RP-3, RP-14, PR-S9, CE-S22, what the craft report says of the guide, my round 5 notes and D3-2074 to D3-2086. Working order: AX-S4 (the 16th skip link), then call 17's road to Rules 14.142 to 14.144, then the creative director's accessibility reason inside call 17's limit, then the board 3 recommendation for CE-S22.

17:55 UTC. **Call 17 and AX-S4 in the generator.** The guide now ends with a closing block, "Three charts in full" (group 18's own title), which links Rules 14.142, 14.143 and 14.144 and, for a public process, chapter 15's Rule 15.22; questions 4 and 8 carry a line to Rule 14.142 between the question and its skip link. The 16th question's "Skip these 7 forms" lands on the closing block's line, where its forms end. Generator run twice (the second writes nothing), `--check` passes, strict build `guide1.html` exit 0 with 0 warnings, `--page` finds 127 form links and 6 road links on their rule blocks and every skip link landing. **Two checks I do not own now fault on the new links** (request SG-9 below): `phase3_ch14_build.py`'s `selection_guide_faults` (5 faults, computed read-only) and `guide_check.js`'s `selectionGuide`. The browser load rule said WAIT at 17:55.

## Fixed

| Code | What changed | File | Proof |
|---|---|---|---|

## Not fixed

| Code | Reason |
|---|---|

## Calls

| call | reason |
|---|---|

## Words for the editor

## Recommendation for board 3

## Requests

## Tested

## Not tested
