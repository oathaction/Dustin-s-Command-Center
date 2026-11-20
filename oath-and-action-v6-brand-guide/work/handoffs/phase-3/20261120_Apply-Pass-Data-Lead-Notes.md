# Apply pass, data lead notes (chat 9, board 3 answers)

Status: 21:18 UTC. Batch 1 (the editor's twelve items and the main session's three A8 lines, D3-2318) reviewed: all signed. Batch 2 (the engineer's eight items) in review, since the engineer's notes say done at 21:15.

What I reviewed against: the baseline is commit `6ba13ecd` (before any owner's work); batch 1 is commit `5dc0d359`, before the engineer's A6. I built both pages strict in my scratch folder and compared them figure by figure, token by token (tags apart from words), and reran every batch 1 generator in a scratch copy of `5dc0d359`.

## Sign-off

### Batch 1, the editor's items and D3-2318

| Batch | Item | Verdict | What I checked |
|---|---|---|---|
| 1 | A11 (reply 16), Rule 15.15's read-aloud lines | Signed | Walked all eight distinct lines on the built page (15 occurrences, the same count as before) against the atlas by my own script, not the generator's: Loops B1a, R10, B5, R1, R8 and B4, Rule 15.8's chain E1, EC6, A4 (LE12 minus, LE14 plus) and Loop B2's two stations. Each line names every variable by its own atlas title, whole, in chain order; each starts with a rise and flips at each minus sign; each closed loop comes back rising for R and falling for B, as its `type` says. Additions to the titles are only "the" (four titles) and "the number of" before Variable C5, which is how the atlas's own `how_to_read` for Loop B4 says it. No old "more ... and back to" line is left on the page. The generator's new direction check fails when I break the sign flip in a scratch copy (11 lines caught). Only words changed in the seven plates; no tag, mark or ink moved. Rules 15.6 and 15.8's "Read aloud" specs now describe the form the plates print |
| 1 | A6w (reply 11), Rule 15.12 names its red variable | Signed | The note now reads "on both connections and on Variable B2 “Availability of local reporting”". Atlas: Reform R-32's `targets` are B2, L26 and LT03, and B2's title is "Availability of local reporting"; the drawing's two connections are LT03 and L26. Only the note changed; the drawing and the alt are as before, and the alt already names the red outline |
| 1 | A13 (reply 18), Rule 15.22's note | Signed | Against `work/research/20261111_Policy-Workflow-Sources.md`, section FS, row "Repeal or sunset" (line 25, checked 2026-11-11, ledger P7-012): Public Law 115-97, sec. 11022, applied its child tax credit rules to tax years "beginning after December 31, 2017, and before January 1, 2026", so "set its rules for the credit to end after 2025" holds; Public Law 119-21, sec. 70104, "struck the end date", as the note says. Stage 18 cites 115-97 ("the tax law approved December 22, 2017") and stage 20 cites 119-21 ("the tax law approved July 4, 2025"), so "the 2017 tax law" and "the 2025 tax law" are the plate's own names. S30's title ("Congress has changed the child tax credit’s top amount three times since 2017, most recently to $2,200 per child from 2025") and Rule 14.36's entry (`"specimen": "S30"`) carry "whose top amount Rule 14.36 charts". No law swapped. Read from the left and from the right: it states how the two examples were chosen and takes no view of either law |
| 1 | A2 (reply 7), S14's line in chapter 13 | Signed | Rule 13.6 (line and table row) and chapter 13's list of sources print the payroll sidecar's `september_release` line: S14's printed line word for word up to its margin of error sentence. Chapter 02's three copies in Rule 02.22 are unchanged. The table's "Title or table" and "Qualification" rows take the release and the new qualification, in order. See Calls on the margin sentence |
| 1 | A7 (reply 12), chapter 13's chips | Signed | Twelve plates each differ from before only by the 44-byte rule `.chip .id{font-variant-numeric:tabular-nums}` (checked by removing it from the old plate and comparing: identical). The page holds the rule 0 times (12 before). The chip's drawing rule is unchanged |
| 1 | A7w (reply 12), Rule 18.24's anatomy key | Signed | Callout 2 says "The atlas ID, each figure at its own width, so the hyphen stays narrow", in the key and in the label; the plate's cut CSS now drops `tabular-nums` from `.sx-kd` (from A7c), so key and drawing agree. Rule 06.5 defines tabular figures as "every digit the same width", so the words say the plain opposite |
| 1 | A14 (reply 20, DR-294), chapter 11's four tables | Signed | In `s-11-steps`, `s-11-marks-drawn`, `s-11-ballot-steps` and `s-11-court-steps`, the alt is now exactly the head sentence and the table's hidden caption is the same sentence (string equal, all four). The only other change in each plate is the hidden rule added to its CSS. No head sentence is new; each was the old alt's first sentence, so no fact changed. Page counts: 101 hidden and 315 open before and after. The accessibility lead checks how it reads |
| 1 | A9 (reply 14), Rule 14.6's ink words | Signed | Seven values in `14-006.json` and `14-data-visualization.json`, "Charcoal at the subject weight" to "the text’s ink at the subject weight"; the spec's token (`oa.chart.color.subject.onNewsprint`) untouched. The page prints the old phrase 0 times (7 before). The two other "Charcoal" phrases stay, as D3-2319 sends them to Dustin |
| 1 | A10 (reply 15), the palette plate's rounding | Signed | I recomputed every contrast figure from the hex values the plate prints and the palette tokens (WCAG relative luminance, floored to two places): all 109 table figures match, including the three keyline and label-beside figures (13.29, Charcoal against Newsprint). Pillar Red on White measures 4.1681, so 4.16 rounded down (chapter 05's 4.17 rounds to nearest); on Newsprint 2.9571, so 2.95; on Charcoal 4.49. The Prussian range: Prussian on Prussian 1.00 and Verdigris 2.7993, so 1.00 to 2.79. All 259 numbers on the plate are the same, in the same order, as before; 112 figures now name their rounding and none prints bare. Only words changed; chapter 05 untouched |
| 1 | A8 (reply 13), "retrieved", the editor's lines | Signed | S71 (grade line, caption, column label, chart note, the 11 routes' under-lines), S67 (measure line, and the Tennessee cell through `typography.replace`, data row untouched), Rule 01.5's map and Rule 14.101's instruction. Kit fragments drawn at 1440 and 390 px at both commits: the only word changes are "read" to "retrieved"; every number is the same; every mark keeps its kind, class and ink; S71's 22 bars keep their widths. S71's drawing grows 34 px at both widths (1,809 to 1,843; 3,037 to 3,071), two under-lines taking one more line each, which is the longer word and nothing else. The kit's CSV exports are byte for byte the same. The page now prints "read" before a date nowhere (6 before) |
| 1 | A8, D3-2318 (main session): S41, S42, S53 | Signed | Each source line changes "read" to "retrieved" and nothing else; each spec's `source_line` equals its sidecar variant, and the kit passes S41, S42 and S53 with 0 faults. `work/build/data/` differs from the baseline in exactly two lines, one in each sidecar. `data_round0_build.py`, rerun in a scratch copy, writes `work/build/data/` byte for byte as committed (126 tables, 0 faults), so its edit holds. No generator writes the census sidecar (searched every script). No other spec reads either variant (S01 reads the stock-trading sidecar's other line and does not change). See Calls |
| 1 | A1w (reply 6), Rule 08.2's footer row | Signed | "16 px at the right end of the source line on a chart exported alone", the answer's own words; the only change in `08-lockmark.json` |
| 1 | A16 (reply 23, D3-2310), chapter 04's sentence | Signed | One sentence after "Ampersand B is our own drawing...": "Before launch, a trademark attorney will check whether our name, our monogram and this ampersand are clear to use." It says what the approved recommendation says, with no filing or result assumed; the only change in `04-ampersand.json` |

Generator trap, batch 1: in a scratch copy of `5dc0d359` I reran `phase3_ch15_build.py`, `phase3_ch13_build.py`, `apply_systems_ch11.py`, `phase3_ch14_rules_build.py`, `phase3_ch14_build.py`, `palette_spec_build.py`, `stage_c_ch18_anatomy_build.py`, `guide_editor_build.py` then `stage_b_identity_ch01.py`, and `stage_a_identity_build.py`. Every output came out byte for byte as committed, except the four specimens with embedded PNGs and the letterhead proof that `stage_a_identity_build.py` re-encodes; those four differ only inside their `data:image/png` strings, as the editor's notes say.

### Batch 2, the engineer's items

(in review)

## Calls

- D3-xxx | Batch 1 signed whole: A1w, A2, A6w, A7, A7w, A8 (the editor's lines and D3-2318's three), A9, A10, A11, A13, A14 and A16 | Each matches its approved answer and goes no further; no number, mark or ink key moved; the facts check against the atlas, the sources file, S30 and the tokens
- D3-xxx | Chapter 13's copy of S14's line leaves out S14's margin of error sentence | No chapter 13 plate prints the margin figure, the plate never says the line is S14's, the six-part table has no row for it, and the words shown to Dustin for the new copies had none
- D3-xxx | D3-2318's two sidecar lines were edited in place, not added as new variants | No other spec reads `survey_only_margin_credited` or `with_program_ages`, no generator writes the census sidecar, and `data_round0_build.py` reproduces the other; the data rows stay frozen, so the brief's rule holds
- D3-xxx | S71's drawing growing 34 px from the longer word is inside reply 13 | The bars, numbers, marks and inks are unchanged; only two under-lines wrap

## Not fixed

(none from batch 1)

## Tested

- Strict page build in my scratch folder at batch 1's tree (working tree at 21:00, before A6): exit 0, 0 warnings, 12,212,558 bytes, 369 rules, 679 specimens, 101 hidden and 315 open. Baseline (`6ba13ecd`) built the same way: exit 0, 12,178,909 bytes, as D3-2313.
- Figure-by-figure token diff of the two pages, tags apart from words, for every batch 1 plate.
- My own read-aloud walker against `work/extract/atlas-v7-data.json` (titles, chain order, link polarity, loop type).
- My own contrast calculator over the palette plate's printed hex values.
- Kit `build --no-png` and `fragments` (lean) for S41, S42, S53, S67 and S71 at both commits: all PASS, 0 faults; words, numbers and shapes compared.
- Reruns of every batch 1 generator and of `data_round0_build.py` in scratch copies, compared by hash; `phase3_ch14_build.py --check` 99 of 99; `palette_spec_build.py --check` 2 of 2; `data_round0_build.py --check` 126 tables, 0 faults.
- A mutation of `read_aloud` in a scratch copy: chapter 15's direction check fails it.
- Em dashes: 0 on either page; 0 in any added line of the generators', specs', data and chapter diffs.

## Not tested

- Batch 1's plates in a browser; I compared bytes, words and shapes, not layout. The accessibility lead checks A14.
- The guide check (the main session runs it).
- How the read-aloud lines and captions sound in a real screen reader.
