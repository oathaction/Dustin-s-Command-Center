# Board 2 apply: research notes

Oath & Action Edition 06, Phase 3. Research lead (`oa-research-lead`), November 13, 2026, 20:06 to 20:18 UTC. Task: apply Dustin's board 2 answer DR-264, and the V7.1 half of DR-265, to the atlas V7.1 issue list. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

`work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md` gains the section "Added November 13, 2026" after the November 6 table, with eight rows in its four columns:

- 38: KFF's 25 million Medicaid disenrollments printed with no period (board item Q-18)
- 39: Reform R-01's two ballot measures, decided after the snapshot (R-01)
- 40: The missing space in source S53's title (A15)
- 41: The Article V route's wording (Article-V)
- 42: Headline figure 5 carries figure 4's qualification (figure-5)
- 43: Figure 7's qualification and R-09's status call H.R. 7008 "a ban"; extends item 36 (figure-7)
- 44: Eighteen titles that state an effect (issue-titles)
- 45: One name for each variable in loops, with CL-026 keeping its approved name (loop-labels, DR-265)

Under the table: a line saying DR-264 approves item 8's fix for Variable D6 as the board wrote it, a sentence that the FEC joint fundraising item (RL-3) gets no row and stays a note with the two FEC data files, and a closing approval line. The file's change log gains one line. Each fix column holds the V7.1 sentence of the board's recommendation, word for word, and cites DR-264 or DR-265. Every ID, field path, quote and count in the section was checked by script against the committed model (121 checks, 0 failures).

One thing for the caller: repair log row RL63, Missouri's Proposition A, also still reads "pending" from the November 3 election. No board item covers it, so it is not on the list.

## Routine calls

- D3-xxx | The new section uses straight apostrophes and quote marks, as the rest of the file does (48 straight apostrophes, 212 straight double quotes, 0 curly marks before this pass) | The task asked for apostrophes "as the file already uses them", and the file has none curly; one form keeps the list consistent and keeps quoted atlas text byte for byte, since the atlas stores straight marks. Swapping to curly is one find and replace if the caller wants it
- D3-xxx | Rows are numbered 38 to 45 | The November 6 table already ends at row 37 (the editor's disclosure, DR-100), so numbering runs on from it
- D3-xxx | Rows follow the board's item order, with D6 and RL-3 as lines under the table | The board's order; D6 is item 8 already, and RL-3 comes off the list
- D3-xxx | Each fix column carries only the V7.1 sentence of the board's recommendation; the guide-side sentences (Q-18's on S65, R-01's on the notes of S03 and S08) stay on the board and in the decisions file | The list is for the atlas editor, and the November 6 rows carry no guide-side lines; D6's "Chapter 15 prints no kind for D6 until then" stays in its line because the task asked for the fix as the board wrote it
- D3-xxx | Row 40's fix adds the plain edit after the board's words: "add a space after "Act," in S53's title" | The board's sentence says what stays on the list, and the editor needs the change to the record
- D3-xxx | Row 43's fix keeps "the October list" and adds "(item 36)" | The board's words, approved; item 36 sits in this file's November 6 table, so the number says where
- D3-xxx | Row 38 prints what the fields hold: I062, I133's evidence note and PW05 give no period; I133's summary opens "In 2024", the year of the uninsured rate beside it; PW10 and PW16 give "during the 2023 to 2024 renewal process" and "by mid-2024"; source Q097's note ("25m+ disenrolled") is added | The board said three pathways print the figure with no period; two of them carry loose periods, and one standard of evidence (DR-93) means the row says so. The fix's words ("wherever the atlas gives the figure without one") are unchanged
- D3-xxx | Row 39 counts 45 text fields that name one or both 2026 measures, by a name match with nine named fields left out (Alaska's 2020 measure in RL14's `rule` and `source_title`, its 2024 measure in RL21's `rule` and `source_title` and in sources K1900 and K1923, and Nevada's Question 3 in RL17's `rule` and `source_title` and RL26's `rule`) | The board printed 49 from a match on the names, which cannot tell the 2026 measures from the earlier ones of the same name; today a match on "Question 3" or "Ballot Measure 2" gives 48 and one that adds "Measure 2" and "24ESEG" gives 54. The board-time script is gone with its container, so the 49 could not be reproduced exactly
- D3-xxx | Row 39 lists RL62's and RL64's `direction` and `margin` beside their `rule`, though those two fields name no measure | They read "pending" and "pending (election Nov 3, 2026)", which the rewrite has to reach
- D3-xxx | Row 39's certification status is the one board 2's research pass read today (Alaska's unofficial summary of November 12; the Massachusetts results site listing no 2026 question) | This pass did not reread either state's site; the row names the date of that reading
- D3-xxx | Row 41 says Congress calls the convention when two-thirds of the state legislatures apply, read today on the National Archives transcript | Article V's own words ("on the Application of the Legislatures of two thirds of the several States, shall call a Convention"); the board's "a convention the states call" was looser, and the fix's words are unchanged
- D3-xxx | Row 44 reproduces the board's six-verb test over 334 headings and leaves out four raw matches by hand: I046 ("Narrow" is an adjective), I091 and I109 ("harm" and "harms" are nouns) and loop R18 ("Weakening watchdogs" is the subject; the verb is "lowers") | That gives the board's 16 issue titles and 2 loop titles; the script asserts each exclusion is a raw match and the final list
- D3-xxx | Row 45's averages are over the 24 variables whose label differs (titles 36.5 characters, labels 22.0) | That reproduces the board's figures; over all 25 they are 35.7 and 21.7
- D3-xxx | Row 45 cites DR-264 and DR-265, and the CL-026 sentence sits in its fix column | DR-264 puts the item on the list as new; DR-265 answers its question; the sentence belongs beside the ask it qualifies
- D3-xxx | "The two FEC data files" are read as the two public files, `fec-jfc-transfers-2024.csv` (ledger row P7-216) and `fec-jfc-transfers-2024-all-committees.csv` (P7-226) | Both sidecars state lines 22, 28C and 21B; `fec-jfc-transfers-2024-by-node` is derived from the second and repeats its qualification, so it is no third data file
- D3-xxx | RL63 (Missouri's Proposition A, still "pending") is reported to the caller and kept off the list | DR-264 approved the board's items; a new row would need its own approval
- D3-xxx | The change log line is added after the file's "Modified: none." line, which stays as written | That line records the October 21 state of the file; the November 6 additions carry no change log line, and this pass logs only its own change

## Tested

- The model's hash: `work/extract/atlas-v7-data.json` SHA-256 ef1028ac...c7f2, snapshot 2026-10-15, the committed file.
- `v71_rows_verify.py` (scratch, below) parses the new section from the file and runs 121 checks, all passing: rows 38 to 45 in order after row 37; each fix cites DR-264 or DR-265; every atlas ID in the eight rows exists in its kind, with ranges such as CL1724 to CL1730 expanded; every field path printed resolves; every quoted atlas string appears in its field exactly; no em dash, en dash, U+2011 or curly mark in the section.
- Row 38: each of the seven issue and pathway fields holds the figure, with the period test per sentence; the claims' `period` fields; CMS's 22,914,537 ended and 69.7% procedural recomputed from `work/build/data/cms-medicaid-chip-renewal-outcomes.csv` (12 months, April 2023 to March 2024; 15,966,431 procedural).
- Row 39: the 45 fields, grouped by record exactly as printed; the nine left out are each a raw match; RL62 and RL64 read "pending" with the margin quoted.
- Row 40: one field holds "Act,2026"; S53 is cited by CL1361; the three straight marks are where the row says.
- Row 41: the AV route's `who` text and its empty `sources`; Article V read on https://www.archives.gov/founding-docs/constitution-transcript at 20:12 UTC (200, 70,555 bytes, SHA-256 21176370...69a2).
- Row 42: figure 5's figure and caption; its first sentence equals figure 4's; the docket dates July 20 and July 22, 2026; no "GAO" or "Accountability" in its qualification.
- Row 43: both quotes; R-09's status has no "photo"; I043's status names the bill and photo identification; item 36 is the H.R. 7008 row.
- Row 44: 334 headings by kind (194, 10, 91, 23, 16); the 16 and 2 titles; the five executive titles in D05, all graded documented, and X07 the only other D05 title kept.
- Row 45: the 20 numbered loops; 25 variables, 24 with a label unlike their title, A5 the one alike; one label per variable across loops; the three label and title pairs quoted; the averages; R9's E2 label; B2's "A4 hardship" step; item 16 is the conceptual chains row.
- D6 and FEC lines: D6's `type` "flow" and `kind_plain` opening; item 8 is the D6 row; 0 atlas fields match "joint fundrais" or "JFC"; both FEC sidecars are kind public and state lines 22, 28C and 21B; both CSVs exist.
- `git status` before and after: only the issue list and this file changed in the repository.

## Not tested

- Whether either state has certified its result since board 2's research pass read them, and Alaska's November 25, 2026 target date; neither was reread in this pass.
- H.R. 7008's text: the row leans on issue I043's own status for the photo identification section, and on board 2's reading of the engrossed bill on govinfo.gov (November 12); not reread.
- KFF's tracker pages behind the claims; the row quotes the atlas's own claim fields.
- The Atlas V3.2 traces of figures 5 and 7 from board 2's notes; they are left out of the rows.
- The atlas renderer: `work/extract/atlas-v7/script.js` is not in this checkout, so where the renderer names loop variables, beyond `chain_labels`, is not mapped. The fix's "wherever a loop names its variables" covers it in words only.
- Prose fields that use a label's words as ordinary phrases (for example "safe seats" in 58 fields, 7 of them in loops): counted, not judged, and not named in the row.
- Which guide plates print loop labels today.
- How the table renders in a Markdown viewer; the check script read eight rows of four cells each.

## Files

- Modified: `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md` (the section "Added November 13, 2026" and one change log line; 22 lines added, none removed).
- Created: `work/handoffs/phase-3/20261113_Board-2-Apply-Research-Notes.md` (this file).
- Scratch only, outside the repository: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/research/scripts/v71_apply_check.py` (the first read of every value), `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/research/scripts/v71_rows_verify.py` (the 121 checks), their outputs in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/research/out/`, and the Archives page in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/research/dl/article-v/archives-transcript.html`.
- Unchanged: Atlas V7, `work/research/atlas-v7-docs/`, `source/`, `deliverables/`, `work/ledger/` and `work/build/data/`.
