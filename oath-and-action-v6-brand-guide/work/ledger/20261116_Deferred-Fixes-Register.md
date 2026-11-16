# Deferred fixes register

A living ledger, opened November 16, 2026 at Dustin's request (DR-282). It holds every fix a review, a reader or an owner flagged that was not made: Should fixes declined or left, Must fixes held for Dustin's call, carried items, and suggestions an owner weighed and set aside. Its purpose is the final finishing pass Dustin plans after the guide is complete, when one model reviews everything and makes these fixes. Each row stands on its own, so that pass can act on it without reading the report it came from.

Every chat that runs a review, a fix pass or a board adds its rows here before it hands off, and marks a row closed (with the commit and decision number) when a later pass fixes it. Nothing is deleted.

## How to read a row

| Field | Meaning |
|---|---|
| Code | The finding's code in its report (for example CE-S22), or a carried item's name |
| Source | The report or notes file that raised it, by path |
| Where | The rule, plate, specimen and the file a fix goes into (the generator or data file, never only an output) |
| What is wrong | The fault in one or two plain sentences, with the words quoted where words are the fault |
| Suggested fix | What the reviewer proposed, and any ruling that bears on it |
| Why not made | Declined (with the reason the data lead or main session accepted), held for Dustin, waiting on a fact, out of scope for the pass, or no time |
| Status | Open, held for Dustin (board N), or closed (commit, decision number) |

## Review of rounds 4 and 5 (chat 7, November 16, 2026)

Reports: `work/handoffs/phase-3/20261116_Review-4-5-*.md` and `20261116_CD-Review-Of-Rounds-4-5.md`. Fix brief: `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md`. Owners' notes: `work/handoffs/phase-3/20261116_Fix-Pass-*-Notes.md`, each with a "Not fixed" section. The main session fills this section from those files at the close of the fix pass and the second pass, checking every code in every report against a "Fixed" or "Not fixed" line.

### Held for Dustin (board 3)

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| CE-S22 | Civic education report | Chapter 14's selection guide, `selection_guide_build.py`; the coverage plan's question words (DR-62) | Three pairs of the sixteen family questions ask nearly the same thing in a newcomer's words | Sharper words for three questions, for example "Shift and swing: what changed between two dates, and which way?" | The questions are the approved coverage plan's words, so they change only on Dustin's word | Held for Dustin (board 3) |
| NB-S4 | Nonpartisanship and brand report | Every chart the kit draws or exports; the kit's source line part | No chart carries the lockmark Rule 08.2 puts at the end of a chart's source line | Add the lockmark to the kit's source line | Charts approved at boards 1 and 2 carry none; a change to every approved chart needs Dustin's call | Held for Dustin (board 3) |
| S14 line in chapters 02 and 13 | Editor's fix notes | Chapters 02 and 13 where they print S14's source line as an example | S14's source line now names the September 2026 release; the copies printed in approved chapters 02 and 13 do not | The editor's words are in `20261116_Fix-Pass-Editor-Notes.md` | Chapters 02 and 13 are approved; the change waits on Dustin | Held for Dustin (board 3) |

### Not fixed in the fix pass

Filled at the close from the owners' "Not fixed" sections and the reports.

### Suggestions weighed and set aside

Filled at the close.

### Not tested (DR-279 and the readers' lists)

Safari, Firefox and real screen readers stay untested until Phase 5's release checks (DR-279). The rest is filled at the close from every report's "Not tested".
