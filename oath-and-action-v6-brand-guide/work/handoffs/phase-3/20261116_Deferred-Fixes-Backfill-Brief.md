# Brief: backfilling the deferred fixes register from Phase 0 on

Oath & Action Edition 06, November 16, 2026. Written by the main session for four backfill readers. Paths are relative to `oath-and-action-v6-brand-guide/`.

**Why.** Dustin asked (DR-282, and on November 16: "backfill all the fixes that were not made from round zero, from the very beginning, and include them all in one master register that I can return to later") for one register of every fix the studio flagged and never made, so that a final finishing pass, run by one model after the guide is complete, can make them. The register is `work/ledger/20261116_Deferred-Fixes-Register.md`. Read its head for the row format. You do not write it; you write a section file the main session merges.

## What counts

Anything a review, red team, creative director, board, gate, reader panel or owner flagged as a fault or an improvement and that was not made: Should fixes declined or left, Must fixes held or carried, items "carried to" a later round, board or phase, owners' "Not fixed" lines, a creative director's instruction for an item under 4 that the rescore did not close, suggestions an owner weighed and set aside, and checks named as not run where a later check never ran them. Leave out what Dustin decided against (a DR row that rejects it) and what a later pass fixed.

## Was it fixed later?

This is the hard part, and the register is only useful if you get it right. For every candidate, look for its fix before you list it as open: the same item's code in later notes ("Fixed", "closed"), a decision log row (search `work/ledger/20261020_Decision-Log.md` by the code or by its words; never read the log whole, it is 1.2 MB), the change ledger, and the current file (grep the generator, chapter JSON, spec or entry for the quoted words or the property). A chapter rebuilt later may have removed the fault with it. Mark each candidate:
- **Open**: not fixed, and the fault still stands in today's files (say how you checked).
- **Unclear**: you could not tell; say what you checked and what would settle it.
- **Closed later**: fixed; give where. List these only as a count and a compact list of codes at the end of your file, not as rows.

## Your file

Write `work/handoffs/phase-3/deferred-fixes-backfill/20261116_Backfill-<Your-Part>.md` (create the folder): a heading for your part, then one table per review or board in time order with the register's columns (Code, Source, Where, What is wrong, Suggested fix, Why not made, Status), then "Closed later" (count and codes) and "Tested and how" (what you searched and read). Each row stands on its own: a later model must be able to act on it without opening the source. Quote words where words are the fault. Where names the file a fix goes into today (the generator or data file, not only an output), checked against the current tree.

Start the file within 20 minutes and add as you go; the container can restart. Read files with search and excerpts; do not read any file over 200 KB whole. Edit nothing else. No browser. Do not commit or push. Read the clock with `date -u`. Plain sentences, no em dashes.

## The four parts

| Part | Files | Your file |
|---|---|---|
| Phase 0 and Phase 1, and the stage reports in the ledger | `work/handoffs/phase-0/`, `work/handoffs/phase-1/`, `work/ledger/20261020_Gate-0-Report.md`, `20261021_Gate-1-Report.md`, `20261028_Direction-Review-Report.md`, `20261029_Civic-Line-Icons-Report.md`, `20261030_Atlas-Concepts-Stage-1-Report.md`, `20261105_Atlas-Editorial-Systems-Report.md`, `20261106_Data-Viz-Stretch-And-Coverage-Report.md`, `20261106_Data-Viz-Systems-Report.md`; `work/ledger/20261020_Open-Questions.md` for open items | `20261116_Backfill-Phases-0-1.md` |
| Phase 2, October 22 to November 7 | `work/handoffs/phase-2/` files dated 20261022 to 20261107 (icon and map concepts, editorial systems, data visualization systems and stretch test, writing rules, stage A, the apply pass, board 6) | `20261116_Backfill-Phase-2-Part-1.md` |
| Phase 2, November 8 to 11, and Gate 2 | `work/handoffs/phase-2/` files dated 20261108 to 20261111 (the Q1 to Q4 pass, drawings, stages B and C, board C, the Gate 2 fix brief), the handoffs V8 to V16's carried lists, and `work/ledger/20261111_Gate-2-Report.md` section 6 | `20261116_Backfill-Phase-2-Part-2.md` |
| Phase 3, rounds 0 to 5 and boards 1 and 2 | `work/handoffs/phase-3/` files dated 20261111 to 20261114 (rounds 0 to 3's reviews, fix briefs, CD scores and rescores, owners' notes; boards 1 and 2; rounds 4 and 5's build notes and carried items), handoffs V17 to V26's carried lists; leave out this chat's review of rounds 4 and 5 (files dated 20261116), which the main session fills | `20261116_Backfill-Phase-3-Rounds-0-5.md` |
