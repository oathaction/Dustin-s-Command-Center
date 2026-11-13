# Round 4 editor notes

Oath & Action Edition 06, Phase 3, round 4. Editor (`oa-editor`), November 13, 2026, under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md` (the editor's row and its "Editor" paragraph bind). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/editor/`. Written as I go; the container can restart.

The owners read the four "Words for" sections directly. Each row gives the file, the field, the old words and the new, and why. The owner applies them; once an owner reports finished, I write straight into its word fields (D3-669) and log each change here. I never touch a key that picks a mark or an ink (V22, D3-1297).

## Status

- 20:41 UTC. Started. Read my role file, `CLAUDE.md`, chapter 02's writing rules, the round 4 brief and my round 3 and board 2 notes. No round 4 spec, entry, sketch or notes file of another owner exists yet. Working tree clean at `829d0db8`. Next: the rest of the brief's "Read first" list, then group lines 9 and 17, then Rule 13.4's plates once the systems designer's DR-265 list lands, and S37 once the data lead rules.

- 21:02 UTC. **S37's curl applied** on the data lead's ED4-1 ruling: one key in `s37.json`, PASS with the sweep, the two drawn labels curled in all four SVGs at the same positions, CSV unchanged; board 3's list is under "S37's curled apostrophes". It showed a kit fault, ED4-3 to the engineer: a pivot table's row headers skip `typography`, so S37's table still prints the straight marks. ED4-4 to the research lead (S89's source line). S89's note words revised after the data lead's 21:00 note.
- 20:57 UTC. First looks written for maker A (S85, S86, S87) and the infographics maker (S89 with the data lead's MI-1, S93), read only, under the two "Words for" sections; the data lead's MA-1, MA-3 and MA-6 agree with mine. Rule 13.4 confirmed unchanged under DR-267 (the systems designer's list agrees). Baseline strict build to scratch (`guide0.html`): exit 0, 11,245,723 bytes, 344 rules, 638 specimens; the build's share per plate is 13,188. Requests: ED4-1 (S37) to the data lead, ED4-2 (S93's source variant) to the research lead. Waiting on: the data lead's S37 ruling, the makers' entries, owners reporting finished.
- 20:49 UTC. Baselines taken: `phase3_ch14_rules_build.py` and `phase3_ch13_build.py` each rerun with no change and write nothing (`git status` unchanged). S37 built as committed to scratch (PASS, 16,065 bytes, 16,815 with its frame), and a scratch preview of its curl (below) for the data lead. Read the data lead's rulings (a) to (c); no ruling on S37 yet. Rule 13.4's two plates print no chain label (below), which the systems designer's list should confirm.

## Summary

## Routine calls

- D3-xxx | The brief's "group lines 9 and 16" are read as the lines of the two round 4 families: group 9, proportion and overlap (coverage plan 3.8), and group 17, infographics (coverage plan 3.16), which the plan file and `14-chapter.json` number 17 | The plan file's `groups` give group 17 the family section 3.16 and rules 14.135 to 14.141; group 16 is tables and plain words, built in round 1, and I read its line too
- D3-xxx | Rule 13.4's two plates stay as built under DR-267, and `phase3_ch13_build.py` is unchanged | They print each loop's own title and each connection's name, the atlas's own, and no chain label or variable name, by my script and the systems designer's scan; DR-267 replaces a label where one prints
- D3-xxx | S37 takes `"typography": {"curl_quotes": true}` after its `table`, and nothing else in the spec moves | The data lead's ED4-1 ruling under D3-1556: typography only, two drawn labels, data and exports as stored
- D3-xxx | S85's "One in ten" stands | S01's approved title says "nine in ten", so the idiom keeps one form across the chapter

## Group lines 9 and 17

## Rule 13.4's plates (DR-267)

**What the two plates print today (20:47 UTC, read by script on `s-13-4-correct.html` and `s-13-4-failure.html`).** Each loop prints its chip and its own title in quotation marks (`loops[].title`), then each connection's chip and its own name (`links[].name`), with the grade word on the correct plate. Neither plate prints a variable's name in any form: no chain label (`loops[].chain_labels`) and no variable title (`nodes[].title`), in the visible text, the alt, any `<svg>` (11 and 4 drawings, none with a `<text>`, `<title>` or `<desc>`), or an attribute. A match of every one of the 31 chain labels that differ from their variable's title, as a whole item or a short phrase, finds none in any chapter 13 plate. The only raw substring hit is "Safe seats", which opens Loop R10's own title ("Safe seats shift accountability to small primary electorates") and Connection L08's name ("Safe seats make the primary decisive"); both are the atlas's names for a loop and a connection, which DR-265 and DR-267 leave as they are. So, unless the systems designer's list shows a label I missed, Rule 13.4's plates need no change under DR-267, and I will say so to the data lead rather than add variable names the plates never printed.

**Confirmed (by 20:57 UTC).** The systems designer's "DR-265 list" (its `dr265_scan.py` over a strict build of HEAD, which masks the atlas's longer names first and matches each label without regard to case, in SVG lines, HTML text, alts, attributes and scripts) finds the same: "Rule 13.4: no chain label prints", and its one request to me says nothing changes unless I read it otherwise. I read it the same way. **`phase3_ch13_build.py` is unchanged under DR-267**, so no plate of Rule 13.4 is re-laid; its plates were looked at in my baseline strict build (under "Tested"). DR-267's words ("print each variable's own title too, words only") replace a label where one prints, and these plates name connections and loops, which keep their atlas names.

## S37's curled apostrophes (D3-1556)

**Scratch preview, before the ruling (20:45 UTC).** A copy of `s37.json` with `"typography": {"curl_quotes": true}` after its `table` (S06's and S42's form), built with `--specs` from scratch; the repository's spec is untouched. PASS, 0 faults. Against the committed spec built the same way, the four SVGs differ in exactly two `<text>` elements each, at the same x and y: the drawn row labels "Rebuild Congress's own staff and experts" and "Limits on pricing software using rivals' data" print "Congress’s" and "rivals’". The CSV export is the same byte for byte. Weight, as the guide places it: 16,065 to 16,194 bytes (16,815 to 16,944 with its frame), 129 bytes more; a scratch copy with no change weighs 16,065, so the 129 bytes are the curl itself, not the scratch path. (Corrected at 21:01: they are the key in the compressed island and a `data-v` attribute on two table row headers; the table's cells do not curl, below.)

**Applied (21:00 UTC), on the data lead's ED4-1 ruling (its 20:58 note).** `work/build/chart-kit/specs/s37.json` gains `"typography": {"curl_quotes": true}` after its `table`, three lines, and nothing else: a parse test asserts every other key equal to the file before and the new key right after `table`, and `git diff` shows three added lines. `oa-chart.mjs build s37`, sweep on: PASS, 126 rows, 4 drawings, 0 faults, one check file; 16,194 bytes as the guide places it, 16,944 with its frame. Against my build of the committed spec, each of the four SVGs (Newsprint and Charcoal, 1440 and 390 px) changes in exactly two `<text>` elements, each at the same x and y; the CSV export is the same byte for byte. Looked at in the Newsprint 1440 px capture, both labels cropped before and after: the curled marks sit in place and nothing else in either row moves.

**A kit fault this shows (for the engineer, ED4-3 under "Requests").** The table equivalent's two row headers still print the straight marks: in a pivot table, `pivot_head` in `kit-build.js` never applies the spec's `typography`, where `pivot_cell` does (C-E7) and an ungrouped table's text columns do (`K.cell_text`). The lean table even writes `data-v="Rebuild Congress's own staff and experts"` on the two headers, since it computes that the printed words should differ, and then prints the stored words. So today S37's drawing says "Congress’s" and its table "Congress's". By script over every spec, S37 is the only pivot table whose row keys hold a straight mark under a `typography` setting (S84's pivot takes a `replace` pair on cells only), so the fix moves no other chart.

### For board 3: S37's two changed labels

| Where it prints | Before | After |
|---|---|---|
| S37's drawing, the row label of Reform R-13 under "Congress, courts and the executive" (desk and phone drawings, both grounds) | Rebuild Congress's own staff and experts | Rebuild Congress’s own staff and experts |
| S37's drawing, the row label of Reform R-38 under "Competition and technology" (desk and phone drawings, both grounds) | Limits on pricing software using rivals' data | Limits on pricing software using rivals’ data |

The same two words print in S37's table once the engineer's ED4-3 fix lands; the CSV export keeps the atlas's straight marks, as D3-519 sets. No figure, ink, mark, order or position changes.

## Words for maker A

### First look (by 20:57 UTC): S85 and S86 as drafted, read only

Maker A applies these until it reports finished; after that I write any still open straight in (D3-669). Each title's word count is by script; the house limit is under 30 (round 3's RS-4).

| File | Field | Now | Suggested | Why |
|---|---|---|---|---|
| S85 | `labels.topic.words` | Worker bargaining | Worker bargaining power | Chapter 10 prints CL-050's word as "Worker bargaining power" (`s-10-list-41`, `s-10-lib-03`, `s-11-12-correct`: "Worker bargaining power, CL-050"). Rule 10.6 sets an icon beside its own word, and the data lead's (b) asks for the ID and approved name checked by script against chapter 10's register. The inventory's sheet label, "Worker Bargaining", is not the word a reader meets beside the icon in chapter 10. **For the data lead too**, since DR-266 quotes the sheet label |
| S85 | `grade_line` | Documented: the Bureau of Labor Statistics’ count of union members, as the atlas records it | Documented: a Bureau of Labor Statistics survey, as the atlas records it on October 15, 2026 | The data lead's (c) words. The Bureau's union figures come from a survey, so "count" claims more than the evidence (W20), and the brief's call 1 puts the snapshot date once, here, with the source line taking the data lead's request R-1 variant |
| S85 | `notes[0]` | In 1983, 20.1 percent of wage and salary workers belonged to a union. In 2025, 5.9 percent of workers in the private sector did and 32.9 percent in the public sector, 14.7 million members in all. | The share stood at 20.1 percent in 1983. In 2025 it was 5.9 percent in the private sector and 32.9 percent in the public sector, with 14.7 million members in all. | Two sentences opening on the same frame, "In 1983," and "In 2025," (W13). Figures unchanged |
| S85 | `chart_notes[0]` | Each square stands for one worker in 100: the 10 union members are filled, in the text’s ink, and the 90 others are open. | Each square stands for one worker in 100. The 10 squares filled in the text’s ink are union members, and the 90 open squares are the rest. | Says what each kind of mark means, as a key does, and drops the passive "are filled" (W02) |
| S85 | `title` | One in ten U.S. wage and salary workers belonged to a union in 2025. (14 words) | Stands | "One in ten" follows S01's approved "nine in ten"; record language for a documented figure (H08) |
| S86 | `title` | Special districts are the most common kind of government in the country, 39,555 of the 90,888 the Census Bureau counted in 2022. (22) | Special districts were the most common kind of government in the country in 2022, 39,555 of the 90,888 the Census Bureau counted. (22) | A 2022 count takes the past tense, as Rule 13.2's record language does (H08); "the most common" claims no majority, as the data lead's (a) asks (39,555 of 90,837 local governments, 43.5 percent) |
| S86 | `notes[0]` | School systems run by a state, county, city or township count with that government, so independent school districts are not every school system. | The Census Bureau counts a school system run by a state, county, city or township as part of that government, so the 12,546 independent school districts leave those systems out. | Names who counts (W02) and says what the count holds in place of what it is not (W09). 12,546 is the file's `Independent school district governments` row |
| S86 | `chart_notes[0]`, second sentence | The federal government and the 50 states print in words, since their circles would draw under a pixel and a few pixels across. | The federal government and the 50 states print in words, since at this scale the federal government’s circle would be under a pixel across and the states’ a few pixels. | The old clause paired two sizes with two subjects a reader has to sort out |
| S86 | `grade_line` | Documented: the Census Bureau’s 2022 count of every government in the country | Either this or the data lead's "Documented: the Census Bureau’s 2022 Census of Governments" | Both read plainly; the data lead's names the census a reader can look up, so it is the data lead's call |

**S87 as drafted (by 20:57 UTC), read only:**

| File | Field | Now | Suggested | Why |
|---|---|---|---|---|
| S87 | `evidence_label`, `grade_line` | Estimate; "Official statistics: the Census Bureau’s American Community Survey" | Finding; "Documented: a Census Bureau survey, with its published margins of error" | The data lead's (c) makes every round 4 title a Finding and gives S87 and S88 this grade line, so the Venn and the Euler read as one file drawn two ways. `evidence` is the data lead's key, so I name it only |
| S87 | `title` | About 23.8 million Americans had both private and public health coverage in 2025, and 28.3 million had neither. (18) | In 2025, 23.8 million people had both private and public health coverage, and 28.3 million had neither. (17) | The survey counts the civilian noninstitutionalized population, which leaves out the military and people in institutions, so "Americans" names more than was measured (W20); the grade line and the table's margins carry the survey's doubt, so "About" is a second hedge (W16). The year leads so the sentence does not open on a figure |
| S87 | `notes[0]` | The two circles are drawn the same size, so their areas carry no count; the chart for Rule 14.82 draws each region at its true size. | The two circles share one size, so their areas carry no count; Rule 14.82’s chart draws each region at its true size. | Drops the passive (W02) and the long way round to the cross-reference |

**Read again at 21:03 UTC, as maker A works.** S87's label and grade line now follow the data lead's (c), its title lists all four groups ("In 2025, 189.4 million people had private health coverage alone, 95.4 million had public coverage alone, 23.8 million had both and 28.3 million had neither.", 26 words, a list of four the facts hold, W12), and notes 2 and 3 say the groups are our sums and that the Bureau sorts the plans, so those rows above are settled. Still open on S87 and now S88:

| File | Field | Now | Suggested | Why |
|---|---|---|---|---|
| S87, S88 | `notes[2]` | The Bureau counts coverage through an employer, coverage bought directly and TRICARE as private, and Medicare, Medicaid, other means-tested coverage and VA care as public. | The Bureau counts coverage through an employer, coverage bought directly and TRICARE, the military’s health plan, as private, and Medicare, Medicaid, other coverage for people under an income limit and care from the Department of Veterans Affairs as public. | TRICARE, "means-tested" and VA each need their meaning at first use (H02, H11) |
| S87 | `notes[0]` | (as above) | (as above) | Still open |
| S88 | `title` | Drawn at true size, the 23.8 million people with both private and public health coverage in 2025 share a narrow overlap, and the 28.3 million with neither form a circle of their own. (33) | In 2025, 213.2 million people had private health coverage and 119.1 million had public coverage, and 23.8 million had both. (20; set at 21:05 UTC on the data lead's MA-8, which leaves the words to me) | Over 30 words; "Drawn at true size" hangs on the people, who are not drawn; the title tells what the drawing looks like ("a narrow overlap", "a circle of their own") where a Finding states what the survey shows (the data lead's (c) and MA-8). The new title names the Euler's two circles and their overlap, so S87 and S88 state two findings from one file, each in its drawing's terms. 213,152,333, 119,137,655 and 23,775,140 round to 213.2, 119.1 and 23.8 million, by script on `census-acs-health-coverage-types` and the derived file. I dropped MA-8's "of them", which a listener could take for either circle |
| S88 | `notes[0]` | …; the chart for Rule 14.81 draws the same groups with circles of one size. | …; Rule 14.81’s chart draws the same groups with circles of one size. | The same short cross-reference as S87's |

| S87 | `notes[1]` | Private coverage includes plans through an employer, plans bought directly and TRICARE; public coverage includes Medicare, Medicaid and other means-tested plans, and VA care. | The Census Bureau counts plans through an employer, plans bought directly and TRICARE, the military’s health plan, as private coverage, and Medicare, Medicaid, other plans with an income limit and care from the Department of Veterans Affairs as public. | Names who sorts the plans (W02), as the sidecar says ("The Bureau counts…"); glosses TRICARE and "means-tested" at first use (H02) and spells out VA |
| S87 | notes | (none) | A note that the four groups are Oath & Action's sums of the published counts, unless the source line's "Overlap computed by Oath & Action from the published counts; margins approximate" is the place you and the data lead settle on | The data lead's (b) for S87 asks the note to say so; the source line already does, so one place is enough |

## Words for the infographics maker

### First look (by 20:57 UTC): S89 and S93 as drafted, read only

The infographics maker applies these until it reports finished; after that I write any still open straight in (D3-669). Title word counts by script; the house limit is under 30 (round 3's RS-4).

| File | Field | Now | Suggested | Why |
|---|---|---|---|---|
| S89 | `title` | A governor or a tribal government’s chief executive asks the President for a disaster declaration, within 30 days of the disaster under the law, and a declaration opens federal help to people and to governments. (35 words) | Under the law, a governor or a tribal government’s chief executive has 30 days from the incident to ask the President for a disaster declaration, which opens federal help. (28) | Under 30 words; "has 30 days under the law" states a limit, as the data lead's (c) and the plan's condition ask; "incident" is the regulation's word and the alt's, where the title said "disaster". The two kinds of help stay in the drawing, the alt and the table |
| S89 | `chart_notes[0]` (the data lead's MI-1) | Each column is a level of government, or residents, named at its head. Each step’s box spans the levels that act at it. Numbered boxes edged in the text’s ink are the steps every declaration takes, in order; the box with a gray edge is the request some cases make in its place. | Each column is a level of government, or residents, named at its head, and a step’s box spans the levels that act at it. Boxes edged in the text’s ink run in order from the disaster to the help a declaration names; the box with a gray edge is the emergency request some cases make in place of step 3. A denial at step 5 ends the path, and steps 7 and 8 follow only where FEMA names that help for an area. | MI-1: "the steps every declaration takes" was untrue, since a denial ends the path at step 5 and steps 7 and 8 follow only for the help FEMA names. Joining the first two sentences also breaks the run of two "Each…" openers (W13) |
| S89 | `notes[1]` | Times are limits in law, not measured waits, and FEMA may extend several of them. | FEMA may extend several of these limits. | Revised at 21:02, after the data lead's 21:00 note: the source line already says the times are limits, so once is enough there, and the note keeps only what the source line lacks. It also drops the ", not measured waits" turn (W09) |
| S89 | source line | (sidecar) …Retrieved November 12, 2026. Times are limits in law, not measured waits. | …Retrieved November 12, 2026. Times are the law’s limits. | The same turn (W09); S77's source line says "Times are the regulation’s limits", so the family keeps one form. The sidecar is the research lead's: request ED4-4 below |
| S89 | `alt` | …within 5 days after the need becomes apparent and no later than 30 days. | …within five days after the need becomes apparent and no later than 30 days. | Numbers under ten in words in an alt (H06) |
| S93 | `grade_line` | Documented: Public Law 119-12 as the Government Publishing Office publishes it, approved May 19, 2025 | Documented: Public Law 119-12’s first page, as the Government Publishing Office prints it | The data lead's (c): the approval date is a part the page prints and a callout names, so it prints there once, never again in the grade or source line. The sidecar's source line also carries "approved May 19, 2025", so S93 needs a source variant without it (a request to the research lead, below) |
| S93 | `title` | The first page of Public Law 119-12 gives its number, the Congress that passed it, where it starts in the Statutes at Large, the day it was approved and the bill it began as. (34) | Public Law 119-12’s first page gives its number, the Congress that passed it, its place in the Statutes at Large, its approval date and the bill it began as. (28) | Under 30 words, and no passive "was approved" (W02); "approval date" keeps the page's own word, "Approved" |
| S93 | `alt` | …Public Law 119–12, May 19, 2025… 2, the Public Law number, Public Law 119–12. | …Public Law 119-12, May 19, 2025… 2, the Public Law number, Public Law 119-12. | An en dash in an alt can be read aloud as "to" ("119 to 12"); the table's "As printed" column may keep the page's own mark, and note 2 already says the page prints a dash |

**Entries 14.135 and 14.139, read at 21:03 UTC.** Both read plainly, each rule names who draws what and why, and 14.139's dash note matches S93's. One item:

| File | Field | Now | Suggested | Why |
|---|---|---|---|---|
| 14.135 | `rule[0]`, third sentence | Print each time as the law’s limit, never as a wait, and the date of the law once, in the grade line. | Print each time as the law’s limit, and the date of the law once, in the grade line. | The ", never as a wait" turn (W09); "limit" already says it |

**S94's note on 26 U.S.C. 7508A, before S94 lands (21:10 UTC).** The data lead's 21:09 sentence holds all four causes and reads well aloud. One word, from the law's subsection (c): "The IRS may postpone tax dates for people affected by a federally declared disaster, a significant fire or a terrorist or military action, and, at a governor’s **written** request, by a disaster the state declares (26 U.S.C. 7508A)." Here "may" states what the law lets the IRS do, so it is no hedge (W16).

## Words for the cartographer

Nothing yet: no change to S12, S16 or S78 or their entries has landed.

## Words for the systems designer

- **Rule 13.4 (by 20:57 UTC).** Your scan and mine agree: its two plates print no chain label, so `phase3_ch13_build.py` stays as it is under DR-267. Thank you for the list.
- Nothing else yet: rules 15.19 to 15.21 have not landed, and I read each DR-265 title change in your generators' words once you report them.

## Requests

### Requests to the engineer

- **ED4-3, a pivot table's row header ignores `typography` (21:01 UTC).** In `kit-build.js`, `pivot_head(rc, v)` returns the column's `words` or `K.fmt(v, rc.format)` and never calls `K.typeset`, while `pivot_cell` does (C-E7) and `K.cell_text` does for an ungrouped table's text columns. The planted case is S37 as it now stands, with `"typography": {"curl_quotes": true}`: its drawing prints "Rebuild Congress’s own staff and experts" and "Limits on pricing software using rivals’ data", and its table's row headers print the straight marks, each with `data-v` set to the stored words. The smallest change, as I read it: in the pivot branch, typeset `head_txt` when `spec.typography` is set and the row column is text, as `pivot_cell` does, so the read-back's `data-v` keeps the stored value as it does now. By script, S37 is the only pivot table this moves today. A kit self-test line on a pivot whose row key holds an apostrophe would keep it fixed. Board 3 lists the two labels either way.

### Requests to the research lead

- **ED4-2, S93's source line without the approval date (by 20:57 UTC).** `govinfo-pl-119-12-first-page`'s `printed_source_line` reads "…139 Stat. 55, approved May 19, 2025, first page, United States…". The data lead's (c) prints the approval date once, as the part a callout names, and in neither the grade nor the source line. Please add a variant without it (as `snapshot_once` and `date_in_grade_line` were added before), for the infographics maker to print.
- **ED4-4, S89’s source line qualification (21:02 UTC).** `govinfo-disaster-declaration-steps`' `printed_source_line` and its `in_force_in_grade` variant end "Times are limits in law, not measured waits." That is chapter 02's corrective negation (W09). S77's line says the same fact as "Times are the regulation’s limits." Please give the variant S89 prints (`in_force_in_grade`, per the data lead's (c)) the ending "Times are the law’s limits.", or tell me if the qualification must keep its second half, and I will find words that say it without the turn.

### Requests to the data lead

- **ED4-1, S37’s curl (D3-1556): ruled at 20:58 and applied at 21:00 (under "S37’s curled apostrophes"). Asked by 20:57 UTC:** The facts are under "S37's curled apostrophes": `"typography": {"curl_quotes": true}` changes two drawn row labels and nothing else in the drawing, keeps the CSV as stored, and costs 129 bytes on the page (16,944 with its frame). Please rule in your notes whether I apply it. Once you do, I write the one key, rebuild S37, check the drawings again and list the two labels for board 3.

## Tested

## Not tested

## Files

- Created: this file.
- Modified: `work/build/chart-kit/specs/s37.json` (the `typography` key, three lines, ED4-1).
