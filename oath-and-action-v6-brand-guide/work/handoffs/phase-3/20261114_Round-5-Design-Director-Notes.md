# Round 5, design director notes

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Design director (`oa-design-director`), under `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md` (my row and its "Design director" bullet), the data lead's "Rulings" (a) to (g) with additions A-1 and A-2 in `20261114_Round-5-Data-Lead-Notes.md`, and the creative director's front door items (`20261112_CD-Review-Of-Round-1.md`, `20261113_CD-Review-Of-Board-2.md`). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/design-director/`. I write only this file; every change goes to its owner as a request. Placement is mine to ask for; a ruling's words are the data lead's.

## Status

- 02:47 UTC. Reading the trackers next, at the main session's word (02:52 relay): Rules 11.10 and 11.11 with their plates and step tables, group 2's line and Rule 11.12, beside Rules 11.8 and 11.9. Strict build of 02:46 (12,090,700 bytes, exit 0); captures waiting for the load to fall under 4.
- 02:42 UTC. **First read of the complex examples written** (Rules 14.142 to 14.144, S96 included, from my strict build of 02:26). Requests to the complex examples maker: 3 Must (DD-E1, DD-C1, DD-R1) and 12 Should; two questions to the data lead, two small word items to the editor, one shared item to the systems designer. Next: the selection guide, the palette specification, the trackers and Rules 15.22 to 15.25 as each owner's "Status" says it has landed; then one read of the fixes.
- 02:27 UTC. First captures of 14.143 and 14.144 read from my 02:04 build; the maker's files moved since (02:13 to 02:25), so I rebuilt strict at 02:26 and captured all three rules again. A full-page browser at twice size ran out of memory at 02:09 (other agents' browsers held about 7 GB), so I capture from a copy of my build that keeps chapter 14 whole and every other chapter's styles and scripts only.
- 02:04 UTC. Started. Read `CLAUDE.md`, my role file, the round 5 brief, my round 4 notes, the data lead's rulings with A-1 and A-2, and the creative director's front door items. Strict guide built to my scratch (11,780,771 bytes).

## Summary

**The three complex examples.** Each plate answers its rule, the inks follow rulings (c) and (d), no red sits where the rulings forbid it, and every plate holds in grayscale and on Charcoal. The maker fixed four faults while I read (between my 02:04 and 02:26 builds): 14.143's step numbers that stood alone above each loop's first step, the note that ran into the status line, Loop B4's grade line that named L23 as its "least certain step" while step 3 quoted the atlas naming L54, and the failure plate's bent connectors that drew as filled black shapes. Those are gone and are not requested.

What keeps the three from the bar is placement:
- **S96 (14.142):** the band's lower edge runs through "October 2025" on both grounds (Must). The two named marks are labeled two ways, one beside its column and one about 95 px above its own, on a leader that ends on the average line's low point.
- **14.143:** the buttons sit about 1,180 px below the drawings at a desk, so no window holds the drawing that lights and the button that lights it (Must). The shared variable, the rule's subject, sits at two heights in the two drawings.
- **14.144:** the rule says "compare effect by effect", yet each family's code sits at a different place in each card, mid-sentence, while the failure plate sets all four codes on one line per reform. Today the wrong plate is the faster read (Must). The code key sits about 900 px below the first code.

## Requests to the complex examples maker

**Rule 14.142, S96 and its failure**
- **DD-E1, Must. A line through words.** At 1440 px on Newsprint and on Charcoal, the band's lower edge (minus 122,000) runs through "October 2025". The halo knocks out part of it, but the rule still shows between and beside the words. Set the label wholly clear of the edge, below it or inside the band with 4 px to spare. Or knock the edge out fully behind the words with the kit's `clear_label`. No line may cross a label's words. If the fix sits in the form, it goes to the engineer through you.
- **DD-E2, Should. One placement for the two named marks.** October's label sits under the band, beside its column. February's sits at the plus 250,000 gridline, about 95 px above its column, on a leader through the columns that ends on the average line's low point at zero, so it reads as pointing at the average. Give both one grammar near their columns' feet. One way: stack both labels left of October's column, October above February, each on a short horizontal leader into its column's foot. February's leader then passes under October's foot, which ends 16,000 jobs higher. The scale already runs to minus 200,000, which leaves room. Any geometry serves if both labels share one placement and no leader meets the average line.
- **DD-E3, Should, with the data lead's yes. The latest label leaves S96's plot.** With two named marks on the plot, "+29,000 jobs / in September 2026, preliminary" makes a third leader at the right end. At 390 px its leader runs down the drawing's right edge for most of its height and reads as a frame rule. The spec's chart notes already carry those words ("Latest: +29,000 jobs ..."), and ruling (c) puts the latest average in a note. Drop the on-plot label in S96 alone. S14 keeps its own.
- **DD-E4, Should. The phone's note for the dark columns.** At 390 and 320 px, "The two dark columns: October 2025, −140,000 jobs, and February 2026, −156,000 jobs." prints as a one-item bulleted list between two hairlines, which reads as a stray list. Set it as a plain line in the key's type directly under the year labels, with no bullet and no rule above. That is where the data lead's condition places it ("the phone note placed").
- **DD-E5, Should. A lone word in the key.** At 390 px "The survey's margin of error for one month's / change" leaves "change" alone on its second line. Hold "month's change" with `typography.hold`.
- **DD-E6, Should. The failure's one label points at one month.** "Seven months of job losses" runs a leader to January 2025's column alone. Draw a bracket under the run from January 2025 to July 2026 with the label under it, or set the label under the run with no leader.

**Rule 14.143**
- **DD-C1, Must, with the component engineer and the accessibility lead's yes. Put the buttons under the drawings.** At a desk the drawings end near y 706 and Play starts near y 1,889 in a 2,457 px plate, about 1,180 px apart. In any 900 px window a reader sees either the drawing that lights or the button that lights it, never both. On a phone, where the two drawings stack, the gap is wider. Order: the two drawings, the Variable C3 note, the status line, the controls group with its reason line, then the seven steps as the still list, then the atlas's limits and the source. The status line already speaks each step's words, so the list need not be in view while a reader steps. Print, reduced motion and scripts off keep the list whole, as now. CE-1's hook order changes, so the component engineer and the accessibility lead (focus order) should agree first.
- **DD-C2, Should. The shared variable on one line.** At the 680 px composition, B4's "Risk of losing office" pill centers about 97 px above R10's. Move B4's drawing down by that amount inside its column, so the two filled pills share one horizontal line, with the heads and grade lines still top-aligned. The variable the title names then reads as one thing across the pair at first glance. Nothing changes where the loops stack.
- **DD-C3, Should, words untouched. The rule's title.** At 1440 px the title breaks "share a / variable". Hold "a variable".

**Rule 14.144**
- **DD-R1, Must. Each family's code on one line across the cards.** The cards share rows for each field, as S91's do, but inside the effects field each family runs as prose: "Quality of democracy: +L local, large positive". So a code ends line 1 in one card ("0" for R-38) and starts line 2 in the next ("+L local" for R-06). A reader comparing one family across three reforms has to hunt. The failure plate sets all four codes on one line per reform, so the wrong plate scans faster than the right one.
  - At a desk, give each family its own shared row across the cards (eight subgrid rows become eleven). Set the family name on its own line in the secondary ink. On the next line, set the code and qualifier whole at the line's start in 600 weight, then the meaning. The four codes then sit on one line across the three cards at every desk width.
  - Do the same for the evidence field's two grades: "For the problem" and "For the remedy" on their own lines, the grade word at the start of the next.
  - Should, on a phone: the cards stack, and R-38's effects sit two full cards below R-06's, so the comparison rests on memory. Before the cards, set one small table, families as rows and the three reforms as columns, each code whole with its qualifier, and no total. That table is the line-up ruling (d) describes. The cards keep the rest.
- **DD-R2, Should, with the systems designer. One set of options.** The three choices shrink to their labels (1,052, 872 and 940 px wide at twice size), so their right edges step down the column. Stretch them to one width (`align-items: stretch` on `.ch1`). The rule is Rule 15.20's own chooser style, so change both plates or neither (R4-5).
- **DD-R3, Should. The key beside the codes.** The seven-code key and the atlas's sentence sit after the cards and the disclosures, about 900 px below the first code at a desk. Move both directly under "The three reforms side by side, as of October 15, 2026", above the cards, so a reader meets the scale and its rule before the first code.
- **DD-R4, Should, with the data lead's yes. One date for the set.** "As of October 15, 2026" prints in the section label and again in every card's Effects and Routes labels, seven times in all. In a 197 px column, "Effects by outcome family, as of October 15, 2026" runs three lines. Keep the date in the section label alone. Every card sits under it.
- **DD-R5, Should, with the systems designer. The chosen pill in grayscale.** A chosen variable draws as a 3 px Pillar Red ring with no keyline. In grayscale it turns a lighter gray than the unchosen pill's ink, so the chosen target reads weaker in print and in one-ink copies. The red connection keeps its keyline case and holds. Give the pill the same keyline inside its red ring: Charcoal on Newsprint, Newsprint on Charcoal. This is Rule 15.20's drawing CSS too, so change both or neither.
- **DD-R6, Should. The failure at 320 px.** The total column, the fault this plate teaches, sits past the frame's visible edge (288 px of a 328 px table), so a reader must scroll sideways to see it. Fit the table to the visible width at the narrow frame (add `table` to the plate's narrow-frame `max-width` list), and hold "renter-owner" whole, which breaks at its hyphen there.

## Requests to the data lead

- **DD-E3.** May S96 drop its on-plot latest label, with the words kept in its chart note? Ruling (c) puts the latest average in a note. Yes or no.
- **DD-R4.** May 14.144 print "as of October 15, 2026" once, in the section label over the three cards, rather than in each card's Effects and Routes labels? Every card sits under that label. Yes or no.

## Requests to the editor

- **14.144's failure caption** says "A total row scores each code"; the plate now draws a total column.
- **DD-C3:** a hold on "a variable" in 14.143's title, if the maker asks; no word changes.

## Requests to the systems designer

- **DD-R2 and DD-R5** touch Rule 15.20's chooser and drawing CSS, which 14.144 copies. If you and the maker agree, change both plates in one pass; if not, neither.

## Routine calls

- D3-xxx | I read the complex examples from my own strict builds (02:04 and 02:26 UTC) at twice size, on a copy that keeps chapter 14 whole and only the styles and scripts of the other chapters | A full-page browser at twice size was killed for memory with other agents' browsers open; chapter 14's plates draw with every stylesheet still present
- D3-xxx | Four faults the maker fixed while I read are recorded as seen, not requested | Requests name the draft as it stands
- D3-xxx | 14.143's buttons placement and 14.144's effect alignment are Musts | Watching a step light, and comparing one effect across reforms, are each plate's lesson; today neither works at a desk
- D3-xxx | The 296 px drawings clipped by the 288 px frame at a 320 px window (14.143, 14.144) are not raised | Chapter 15's stage contract (CH15-M1) keeps drawings at true size in a scrolling frame with its hint in words, as Rules 15.6 and 15.20 do
- D3-xxx | The red pill's missing keyline and the chooser's stepped widths go to both the maker and the systems designer as Shoulds | They are Rule 15.20's signed-off treatment; one component keeps one look (R4-5)
- D3-xxx | Rule 14.143 at rest dims both drawings except the start pill and the two filled C3 pills, and I ask nothing of it | It is Rule 18.22's stepper behavior; the two black pills are then what a reader sees first, which is the lesson
- D3-xxx | S96's tallest column rising past the top labeled gridline is not raised | The scale runs to 850,000 with ticks every 250,000, as S14 draws it

## Tested

- Strict guide builds to my scratch: 02:04 UTC (11,780,771 bytes) and 02:26 UTC (12,091,743 bytes, exit 0). Each build rewrote `work/build/chart-kit/plate-share.json`; I copied it back to the state it held before my build, as the maker's script does.
- My own captures at twice size (`cap2x.cjs`, Playwright with `deviceScaleFactor: 2`), each with the 1-minute load under 4 when it started. The first run at 02:06 on the full page was killed for memory. Run 2 at 02:16 used the 02:04 build. Run 3 at 02:27 used the 02:26 build. Each run covered every plate of 14.142 to 14.144 at 1440, 390 and 320 px, on Newsprint and on Charcoal (page theme dark with each stage's surface set to Charcoal), and in grayscale on Newsprint. Run 3 added S96 and the 14.142 failure, the three rule heads and bodies at 1440 px, 14.143 after two and after five presses of Next step, and 14.144 with R-30 and with R-38 chosen, at every width and ground.
- Looked at closely: S96 at 1440 px (Newsprint, Charcoal) with a zoom on both named labels; S96 at 390 px (Newsprint); the 14.142 failure at 1440 px; 14.143 at 1440 px at rest, at step 2 and at step 5 (Newsprint), at 390 px (Newsprint) and 320 px (Charcoal); its failure at 1440 px in both builds, zoomed; 14.144 at 1440 px (Newsprint) at rest, with R-30 (Newsprint, Charcoal, grayscale) and the drawing with R-06; 14.144 at 390 and 320 px (Newsprint); its failure at 1440 px (Newsprint) and 320 px (Charcoal).
- Read the plates' markup and own CSS, as built and in the specimen files: 14.143's order of parts and its step CSS; 14.144's chooser class `.ch1` beside Rule 15.20's; the red target CSS; S96's spec (`scale`, `labels.named`, `labels.margin`) and its data file's extremes.
- Two short probes at 1x (02:25 UTC, load 4.6 and 5.2, one page each) of the computed fill on 14.143's failure connectors.

## Not tested

- 296 and 256 px drawing widths; I read 1440, 390 and 320 px windows only.
- Grayscale on Charcoal; 14.143's step states in grayscale beyond the R-30 drawing of 14.144.
- Keyboard, focus order, the live status line and the keys files (the accessibility lead's and the component engineer's).
- Print, reduced motion, scripts off and forced colors.
- The full page at twice size; my captures come from the trimmed copy described above.
- The kit's own build and sweep of S96 (the maker's and the engineer's).
- Group 18's head and line before Rule 14.142.
