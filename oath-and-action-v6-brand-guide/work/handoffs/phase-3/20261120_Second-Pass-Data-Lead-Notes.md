# Second pass, data lead notes

Written November 20, 2026, by the data lead (`oa-dataviz-systems-lead`). Brief: `20261120_Second-Pass-Brief.md`. I sign off every plate the pass changes, in numbered batches, from the editor's and engineer's notes and the diffs against commit db231c9b and later. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/data-lead/`.

## Status

16:49 UTC: started. Role file read at `oath-and-action-v6-brand-guide/.claude/agents/oa-dataviz-systems-lead.md` (the repository root has no `.claude/agents/`). No browser until the main session says the guide check has ended (about 17:45 UTC).
16:54 UTC: batch 1 (RS-1, RS-6, RS-3) and batch 2 (RS-7, CR-S1's remainder) signed off from source, the plates' HTML and my strict build. Waiting for RS-2, RS-4, RS-5 and CR-S23.
17:00 UTC: batch 3 (RS-2, RS-4, RS-5 as data, and D3-2280's S91 check) signed off. RS-5's visible half goes to board 3 as a held item (D3-2278), with its reach, in the decision file. Waiting for CR-S23.
17:01 UTC: batch 4 (CR-S23) signed off. **All nine items are signed off from source, specs, the plates' HTML and a strict build of the joined pass (17:00 UTC, exit 0, 0 warnings).** The browser views listed under Not tested wait for the main session's word that the guide check has ended; I run them then and add a batch only if one changes a sign-off.
17:11 UTC: batch 5, CR-S23's revision (the engineer's 17:04 UTC layout, after snapshot e1e4e369), reread from the current files and signed off. The pass stays signed off whole.

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

### Batch 3, 17:00 UTC: RS-2, RS-4, RS-5 (data only) and the S91 check (D3-2280)

**RS-2, S91's title (26 words).** Signed off.
- Data. The title keeps batch 9's universe (CD-S4), the federal district courts: S91's three cards are district judges, bankruptcy judges and magistrate judges, from 28 U.S.C. 133, 134, 152, 631 and 633, and bankruptcy courts are units of the district courts (28 U.S.C. 151), so "the federal district courts’ three kinds of judge" names exactly the cards. "Only district judges serve for life" matches the data's terms (row 1 "for life"; rows 2 and 3 fixed terms), and the territorial exception names the three territories whose district judges serve fixed terms (MI-4, MI-7; Puerto Rico's serve for life, so it stays out). The editor's reason for leaving the rescore's example is right: "the three kinds who hear federal trial cases" would take in the Court of International Trade, whose judges also serve for life, a claim S91's data does not hold. The verb stays a documented finding, as the grade line says.
- Read from the left and the right: the title names no party or official.
- The example log's row for Rule 14.137 takes the new title; its domain and states are unchanged, so Rule 01.9's count does not move.

**D3-2280, the S91 check in `maker_i_round4_derive.py`.** Signed off. The check still guards the same universe: it now looks for the new title's scope words and, with them, the measure line's "who hears cases at trial in the federal district courts", so a later title cannot drop the district courts without failing. The added check holds the title at 27 words or fewer. Every other S91 check is unchanged, and the editor's run passes them all.

**RS-4, S90's row 4 note.** Signed off for the page.
- Data. Row 5 of `census-school-system-finances-2024.csv` holds 39,177,454 thousand dollars of COVID-19 relief within federal revenue, which is $39.2 billion to one decimal. The plate's first note prints the same $39.2 billion, and Rule 14.2's anatomy sets the notes above the table, so "as the first note says" points to a note the reader has just passed. The data file is unchanged; the spec's `typography.replace` changes printed words only.
- Not part of RS-4, found while checking it: the kit's CSV export of S90 leaves row 5 out by the spec's `where` and still prints row 4's note "Includes COVID-19 relief funds (row 5)", so the export's note points to a row it does not carry. The guide page is right. See Calls; it goes to the register, owner the engineer (the kit's export), as the editor's Request 2 asks.

**RS-5, the entries' related rules, as data.** Signed off as data. The five entries carry the related rules the rescore names, each target a rule that exists in the guide, and each pairing fits the form: 14.32's noisy monthly columns and 14.74's survey margin with Rule 14.142's margin band; 14.88's bill tracker with the two new trackers (11.10, 11.11) and Rule 15.23's tracker map; 14.96's and 14.135's process forms with Rule 15.22's statute path. The chapter file changes only those five rules' `related_rules`, and `related` gains chapter 15 on 14.88, 14.96 and 14.135, which the page prints as "15 Systems graphics" under Related chapters. That line is the only visible change; Rules 14.88 and 14.96 were shown at board 2, so it joins panel 1's list of changed approved work. The page prints no rule numbers from `related_rules` (`related_inline()` prints chapters only), so the half a reader would see is held for Dustin on board 3 (D3-2278): 138 of chapter 14's 144 rules carry related rules, 363 links in all (284 inside chapter 14, 79 to chapters 01, 05, 06, 11, 12, 13, 15, 18 and 19), against 38 rules that print a Related chapters line today.

### Batch 4, 17:01 UTC: CR-S23, Rule 14.144's phone line-up

**CR-S23.** Signed off from source; the 360 and 390 px measure waits for a browser.
- `s-14-144-correct.html` changes inside its style alone: outside the `<style>` block the markup is byte for byte as committed in db231c9b, so every reform, code, qualifier and pip count prints as before. The line-up's rows change from a two-column grid to a wrapping row whose pips, code and words form one group that never wraps inside, so a code's pips stay on its line. 51,724 to 51,875 bytes.
- Rule 13.5's mark is unchanged (the 22 px pips, read from chapter 13's `pips_svg`), the cards and the key do not move, and the plate still prints no total: the atlas's codes stay uncombined (ruling (d), D3-2127). Rule 14.144 is a round 5 plate shown on board 3, and its pips are already a board 3 item (D3-2127), so no approved drawing changes.

### Batch 5, 17:11 UTC: CR-S23 revised (after snapshot e1e4e369)

**CR-S23, the engineer's second layout.** Signed off from the current files; batch 4's sign-off stands for the revision.
- The revision changes only the line-up's style: the group of pips, code and words takes its own line under the chip unless the line has room for the chip, the pips and about 11em of words (`flex: 1 1 calc(96px + 11em)`), and the row gap drops from 4 to 2 px. Outside the `<style>` block `s-14-144-correct.html` is still byte for byte as committed in db231c9b, so every reform, code, qualifier and pip count prints as before, and the plate still prints no total and no combined score. 51,724 to 51,891 bytes against db231c9b.
- The pips' size, 88 by 22 px, is read from chapter 13's `pips_svg` (Rule 13.5's mark) and not restated, so the mark cannot drift from Rule 13.5. The generator's `--check` reads 10 of 10 files current at 17:10 UTC.
- The engineer's Chromium measures (17:06 to 17:08 UTC, their notes) put all twelve rows' pips on their code's line at 390, 360 and 320 px and with 200 percent text, every code whole at one x; I have not run a browser, so those figures are theirs.

### The joined pass, 17:00 UTC

A strict build of the tree at 15591677 (every item in): exit 0, 0 warnings, 12,178,911 bytes, the editor's figure; pictures 101 hidden and 315 open. My two scripts rerun on it: the six tracker alts agree with their marks and keys, and S94's three year marks carry the same 16 events on the same days. The page prints S91's new title once and the old one nowhere, and S90's new note once, after the note it points to, with "row 5" nowhere.

## Not signed off

None. Every item the pass changed is signed off for data and the chart rules. The views a browser must confirm are listed under Not tested, with the owner who measures each.

## Calls

- D3-xxx | On D3-2281 (S90's CSV export): the fix belongs in the kit's export, which should print the words the plate prints by applying the spec's `typography.replace` to exported cells, and the research lead's frozen data file keeps its note | the file's "(row 5)" is true of the file; the export leaves row 5 out by `where`, so the fault is the export's, and one change in the kit fixes every spec that replaces printed words; owner the engineer, in the finishing pass
- D3-xxx | RS-5 signs off as data only; printing `related_rules` as links goes to board 3 held for Dustin (D3-2278) with its reach: 138 of 144 rules, 363 links | the page prints related items as chapters only, and a new line on 138 rules changes every approved chapter 14 entry's foot

- D3-xxx | The six tracker alts may leave out the sample figure "4" printed inside the key's marks | the marks are `aria-hidden` drawing samples, not data, and D3-2153's test reads them as hidden

## Tested

- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/b1/guide.html` at 16:51 UTC: exit 0, 0 warnings, 12,178,364 bytes; pictures hidden 101, open 315; none of RS-1's six stages open. `plate-share.json` was not rewritten.
- `rs1_check.py` (scratch): the six tracker plates' drawn marks, key words and step names against their alts; exit 0.
- `rs3_check.py` (scratch): S94's mid, desk and phone year marks in my strict page carry the same 16 events on the same days.
- Atlas query: Loop R10 and connection L08 (from, to, sign, evidence) against RS-6's line.
- Fragment comparisons against commit db231c9b: words and SVGs of `s-15-19-correct` and `s-15-20-failure`; the markup of `s-14-144-correct` outside its style, at 16:59 UTC and again at 17:10 UTC after CR-S23's revision; byte sizes.
- `phase3_ch14_complex_build.py --check` at 17:10 UTC: 10 of 10 files current.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/b2/guide.html` at 17:00 UTC on 15591677: exit 0, 0 warnings, 12,178,911 bytes, pictures 101 hidden and 315 open; `rs1_check.py` and `rs3_check.py` rerun on it; S91's title and S90's note read in the page; the working tree unchanged by the build.
- S90's data row 5 (39,177,454 thousand dollars) against "$39.2 billion"; S91's three cards and terms against the title; the kit's S90 CSV export from the editor's scratch run (it leaves row 5 out and keeps "(row 5)").
- RS-5: the five rules' `related_rules` and `related` before and after in the chapter file; every related rule in chapter 14 checked to exist as a rule in the guide; the reach counted (138 of 144 rules, 363 links).

## Not tested

- Any browser view, while the guide check holds the machine: S94's year at a 1024 px page (the engineer measures it too); Rule 15.20's failure plate options at 1440 and 390 px, whether they stop splitting into columns; Rule 14.144's line-up at 360 and 390 px, pips on the code's line; S90 and S91 at 390 px and on Charcoal; Rule 15.19 in a page.
- The kit's whole build (`build --all --no-png`): the editor and the engineer ran it (96 of 96); I did not.
- The accessibility tree for RS-1's six pictures and RS-7's focus order; both are the accessibility lead's.
