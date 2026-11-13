# Round 3 red team: nonpartisanship, brand and craft

Oath & Action Edition 06, Phase 3, round 3 review, November 13, 2026. Reviewer: the design director (`oa-design-director.md`) as reviewer, holding the creative director's brand knowledge (`oa-creative-director.md`), for `work/handoffs/phase-3/20261113_Phase-3-Round-3-Review-Brief.md`. Lens: nonpartisanship, brand and craft. Codes run BC-M1 (Must fix) and BC-S1 (Should fix). Paths are relative to `oath-and-action-v6-brand-guide/`.

Build read: the main session's strict build of `8507b822` (`.../round-3-review/main/guide.html`, 11,226,718 bytes, 0 warnings), copied to this lens's scratch before any capture. All 20 round 3 specs and S07, S12 and S16 were also built alone with the kit at page widths 1440, 390, 328 and 288 (drawings of 720, 358, 296 and 256 px; S16 and the wide plates at their own widths) on both grounds: 23 of 23 PASS, 0 faults. Scratch and captures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c39ddae-7cec-55d0-9e8a-b2e47330229b/scratchpad/phase-3/round-3-review/brand-craft/`.

Status: draft, written 04:35 UTC; sections marked "(pending)" fill as checks finish.

## 1. Score for this lens

(pending)

## 2. Must fix

**BC-M1. S73's title sets one fundraising committee of each nominee against the other, and the breadth it contrasts comes from the rule that picked them.** Owners: maker B (S73, entry 14.104), the research lead (the other committees' transfers), the data lead (sign-off), the editor (words).
- Where: `work/build/chart-kit/specs/s73.json`; `work/build/data/fec-jfc-transfers-2024.meta.json`.
- What is wrong: the title reads "The Harris Victory Fund sent $899.4 million to 53 committees in the 2024 cycle, and the Trump National Committee JFC sent $273.8 million to two." The file picks, for each nominee, "the joint fundraising committee that transferred the most to the nominee’s principal campaign committee". That rule is read the same way for both, but the title's contrast is breadth ("53 committees" against "two"), which the rule does not measure. The sidecar's own note lists the committees left out: for Trump, "TRUMP SAVE AMERICA JOINT FUNDRAISING COMMITTEE" ($134,018,942.92 to the campaign) and "TRUMP 47 COMMITTEE, INC." ($26,908,283.76); for Harris, "HARRIS ACTION FUND" ($4,900,000.00) and "HARRIS BALDWIN VICTORY FUND". The file reads only what those committees sent to the campaigns, never what they sent to party committees. Read from the right, the title and the drawing say Trump's joint fundraising reached two committees while Harris's reached 53 state and national parties; a reader who knows that a second Trump committee raised money with party committees will take the chart as built to show the gap. Read from the left, the title holds as a statement about two named committees. One reading leaves a side short, which is the fault DR-93 and DR-124 guard against. The chart note's "$4.9 million and ... $160.9 million" gives the campaigns' side of the other committees and nothing of their transfers to parties, so the reader cannot judge the breadth claim.
- Fix, either: (a) the research lead reads line 22 for all four other committees (two for each nominee) and the note gives each nominee's committees together, with counts of recipients, and the title keeps a breadth contrast only if it holds across all of them; or (b) the title drops the breadth contrast and names what the rule picks, for example "The Harris Victory Fund sent its campaign $528.7 million and the Trump National Committee JFC sent its campaign $246.8 million; the Harris fund also sent $370.7 million to 52 party committees", with a note naming the four committees not drawn and saying their transfers to party committees are not counted here. (b) costs no new data. The data lead picks; the editor reads both titles from both sides.

**BC-M2. Two diagram tables print their links wrong, so the page table no longer answers who sent what or who governs whom.** Owners: the engineer (`table.group`, `agg: "first"`), maker B (S73), maker A (S68). Named place 4.
- S73 (`specs/s73.json`, `table.group.columns[0]`, `{"label": "From", "agg": "first", "field": "jfc_name"}`): the "From" column is empty in all 7 rows of the page table, in the kit's page and in the guide build alike, and the two refund rows' "Report line" is empty too. The CSV export holds `jfc_name` for all 57 rows. With scripts off or with a screen reader, the table lists "Harris for President, the campaign", "Republican National Committee" and the two refunds with no sender, so it no longer prints links as rows (from, to, measure) as R3-6 asks, and it cannot answer "Where did each ... committee send what it raised?". The kit's checks passed it (23 of 23 PASS).
- S68 (`specs/s68.json`, the column `{"field": "order", "label": "Line of authority", "words": {...}, "empty": "None drawn"}`): `words` maps orders 1, 2, 5 and 6 only, so four bodies print their sort number as their line of authority: "Congress and the Department of Health and Human Services | ... | 7", "City council or municipal utility board | ... | 3", "Electric cooperative board of directors | ... | 4", "Investor-owned utility | ... | 8". A reader takes "7" for a count of lines.
- Fix: the engineer makes `agg: "first"` keep a text field the group's rows carry (or fails the check when a grouped column comes back empty in every row), and maps the refunds' `28C` through `words`. Maker A gives S68's column every order its words, "None drawn" for 3, 4, 7 and 8, or moves the authority words to a field of their own so `empty` applies.

**BC-M3. S71 prints a studio word in reader text.** Owners: maker A (`usgov-v7-route-grid` text or the spec), the editor.
- Where: S71, the "State statute" row's source line under "What it takes": "State constitutions read in round 0: Massachusetts, Nebraska, Virginia, Arizona; read November 11, 2026".
- What is wrong: the round brief's limits say "no decision codes or studio words in reader text". "Round 0" names the studio's process, which a reader cannot know.
- Fix: "State constitutions read: Massachusetts, Nebraska, Virginia and Arizona; read November 11, 2026", or name the date they were first read.

## 3. Should fix

(pending, drafted below in working notes)

## 4. The seven named places

(pending)

## 5. Questions for Dustin

(pending)

## 6. Tested

(pending)

## 7. Not tested

(pending)

## Working notes (removed when final)

- Plate bytes measured in the guide build: only S69 (14,591) over 13,852, none over 15,000; S07 14,351 (board 1).
- Should list so far: S80 Detroit and land; S73 node bars hidden; S81 Charcoal no-estimate equals under $50,000 (1.09 to 1); S82 Charcoal closest races 1.78 to 1; map codes missing; S79 floating neighbor lines; S69 and S70 masonry order; S66 spine gap; S65 procedural meaning and title break; S72 title crossovers; S76 key ink; entry 14.119 "Gray steps", 14.124 "gray panels"; typography; S77 "some miss the limits"; S74 diagonal; entry 14.115 example.
