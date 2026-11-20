# Second pass, data lead notes

Written November 20, 2026, by the data lead (`oa-dataviz-systems-lead`). Brief: `20261120_Second-Pass-Brief.md`. I sign off every plate the pass changes, in numbered batches, from the editor's and engineer's notes and the diffs against commit db231c9b and later. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/data-lead/`.

## Status

16:49 UTC: started. Role file read at `oath-and-action-v6-brand-guide/.claude/agents/oa-dataviz-systems-lead.md` (the repository root has no `.claude/agents/`). No browser until the main session says the guide check has ended (about 17:45 UTC).
16:54 UTC: batch 1 (RS-1, RS-6, RS-3) and batch 2 (RS-7, CR-S1's remainder) signed off from source, the plates' HTML and my strict build. Waiting for RS-2, RS-4, RS-5 and CR-S23.

## Sign-off

Each batch answers three questions: does the change say only what the data and the record show; does it keep the chart rules of DR-64 and, on a failure plate, the plate's one fault; does any approved drawing change past what the item names.

### Batch 1, 16:54 UTC: RS-1, RS-6, RS-3

**RS-1, the six tracker alts (Rules 11.10 to 11.12; the brief's "11.8 to 11.11" is the old numbering, and the editor's notes have it right).** Signed off.
- Data. My scratch script (`rs1_check.py`) reads each plate's drawn marks (`data-icon` per step) and its key from the six fragments, and the alt from `manifest-systems.json`. In all six, the alt's step names match the key's in number and order, the alt's mark words match the key's words in its order, the key's words match the marks it draws, and on the three correct plates every row's step states in the alt match the marks drawn (ballot 3 rows, court 3, records 2). The three failure alts' new state words match their marks: 11.10's failure draws done, done, done, never happened, done, done; 11.11's draws six done; 11.12's draws done three times, now, then not yet three times.
- The shape words in `MARK_SHAPE` are Rule 11.2's alt word for word ("a filled circle", "a heavy ring", "a fine ring", "the fine ring under a slash", "a filled square"), and each matches the key's drawing (filled circle, 3 px ring, 1.5 px ring, ring with a slash line, filled square).
- The six fragments are byte for byte as committed in 88b73646; only the six `alt` fields in the manifest changed. Each failure alt still opens "Failure case: do not publish." and keeps its one fault's sentences unchanged. No approved drawing moved; the two new trackers are board 3 items, not yet approved.
- The key's sample marks print a "4" inside each mark; those marks are `aria-hidden` and the alt does not voice the sample figure, which I accept, since the figure is a drawing sample and not a datum.
- Build: my strict build (16:51 UTC, tree at 9fa13098 with the owners' uncommitted files of that minute) exits 0 with 0 warnings; `pictures.hidden` 101 and `open` 315, and none of the six stages is in `open_stages`.

**RS-6, Loop R10's first step on Rule 14.143.** Signed off.
- Data. Connection L08 in `atlas-v7-data.json` runs from C1 (seats with little electoral competition) to C2 (how often the primary decides the winner), plus sign, evidence "documented". The supposition says C1 rises and the step says C2 "goes up", with no "can", which is the sign and grade the atlas gives. The new hold in `walk_steps()` stops the build if the supposition and the step's direction disagree, and the check near line 1368 now tests the cause from the supposition.
- The status line drops 16,500 to 15,000 ms by the script's own word-count formula; no data value moves.
- `s-14-143-failure.html` is byte for byte as committed: its fourth list item still reads the step whole ("Seats with little electoral competition rise, so how often the primary decides the winner goes up."), so its one fault, the seven steps read as one balancing loop, stays as captioned. No other fragment or output names the old doubled line. Rule 14.143 is a round 5 plate shown on board 3, not yet approved.

**RS-3, S94's desk year from a 480 px column.** Signed off.
- Data. My scratch script (`rs3_check.py`) reads S94's three year marks from my strict page and maps every square back to its month and day: the mid mark (480 by 380 px), the desk mark (600 by 380) and the phone mark (224 by 332) each draw the same 16 events on the same 16 days, with 8 px squares (6.5 px for the open ones) at 480 and 600 px. At 480 px a day is 14.26 px apart, so adjacent days never touch, and a three-event day (April 15) stacks 28 px inside its 30 px month. The scale ticks stay at days 1, 15 and 31.
- DR-64 allows a narrower drawing that carries the same data and finding; this one is the desk drawing at a narrower pitch, with nothing dropped. The engineer's card dump shows the phone and desk marks byte for byte as before, so the 1440 px page keeps the drawing the rescore read. Only `calendar.js` writes `.oac-h-mid`, so no other chart changes. S94 is a round 4 chart on board 3, not yet approved.
- Weight: S94's plate 14,602 to 16,789 bytes in the page, past the 15,000-byte plate figure, which DR-271 makes a reported figure. I accept the cost for the year at a 1024 px page.

### Batch 2, 16:54 UTC: RS-7 and CR-S1's remainder

**RS-7, Rule 15.19's order.** Signed off for data; the focus order is the accessibility lead's.
- `s-15-19-correct.html` holds the same words as before (the same multiset of text runs) in the new order, and its six SVGs are byte for byte as before, so the loop drawing, its steps and their grades and delays do not move. 7,770 to 7,774 bytes. The alt now lists the parts in the order the plate sets them. The new `st1` style is carried only by 15.19's root; no other plate in chapters 14 or 15 uses it.
- The engineer's request about Rule 14.143's alt (it lists the buttons after the steps) is a words item for the editor; it does not change a datum.

**CR-S1's remainder, Rule 15.20's failure plate.** Signed off from source; the column measure waits for a browser.
- `s-15-20-failure.html` keeps its words in the same order and its loop drawing byte for byte; the two check marks change class only (`ck` to `oa-choice-check`, the same `U-selected-check` symbol). The options now sit in the shared chooser's list form, as on the correct plate, so the failure plate differs from the correct one in its fault alone: both reforms chosen and lit at once, a combined "+L" no atlas reform carries, and no qualification. That is the caption's fault, unchanged, and V7's effect codes stay uncombined everywhere but this do-not-publish plate. 5,223 to 5,415 bytes.
- The chapter's shared style lost `.xb` and changed `.xk`; only `s-15-20-failure` uses either class, so no other plate changes.

## Not signed off

## Calls

- D3-xxx | The six tracker alts may leave out the sample figure "4" printed inside the key's marks | the marks are `aria-hidden` drawing samples, not data, and D3-2153's test reads them as hidden

## Tested

- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/b1/guide.html` at 16:51 UTC: exit 0, 0 warnings, 12,178,364 bytes; pictures hidden 101, open 315; none of RS-1's six stages open. `plate-share.json` was not rewritten.
- `rs1_check.py` (scratch): the six tracker plates' drawn marks, key words and step names against their alts; exit 0.
- `rs3_check.py` (scratch): S94's mid, desk and phone year marks in my strict page carry the same 16 events on the same days.
- Atlas query: Loop R10 and connection L08 (from, to, sign, evidence) against RS-6's line.
- Fragment comparisons against commit db231c9b: words and SVGs of `s-15-19-correct` and `s-15-20-failure`; byte sizes.

## Not tested

- Any browser view, while the guide check holds the machine: S94 at a 1024 px page, Rule 15.20's failure plate options at 1440 and 390 px, Rule 15.19 in a page.
- The accessibility tree for RS-1's six pictures and RS-7's focus order; both are the accessibility lead's.
