# Data visualization round: the fix pass brief

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Written by the main session from six red team reports and the reader panel. One fix pass per maker. Paths are relative to `oath-and-action-v6-brand-guide/`.

## How to work

1. Read every report, not only your own sections:
   - `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Statistics.md`
   - `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Civic-Education.md`
   - `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Interface-Accessibility.md`
   - `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Brand-Nonpartisan.md`
   - `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Craft.md`
   - `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Production.md`
   - `work/handoffs/phase-2/20261106_Data-Viz-Reader-Panel.md`
2. Rebuild from the current shared data. It changed since your build (decisions D2-104 to D2-107 in `work/ledger/20261020_Decision-Log.md`): the scenario reading now classes "up modestly" as slightly up (one S06 cell, iv-c income and wealth equality, moves), the verifier caps its tolerance and reads timeline dates, S03, S06, S07 and S08 must carry the editor's disclosure, the homeownership source line names the 2020 caution, and Missouri's row prints its certified result.
3. Fix every must fix and should fix that names your concept, and every shared fix below. Do polish items where they cost little. Where a finding conflicts with this brief, this brief wins. Where you disagree with a finding, leave it, and say why in your notes.
4. Keep your concept's idea. A fix that would turn your concept into another one is the wrong fix.
5. Rerun both checks until they pass, look at your captures again (1440, 390, grayscale), and add a "Fix pass" section to your notes listing each finding ID and what you did, or why you left it.

## Shared fixes, all three concepts

**F1. The repair log charts (S03 and S08) say what the log is.** Visible on the face of both charts, in the notes area (never only in a closed table):
- "The log holds the 64 changes the atlas chose to record, not every rule change in the country. It records more of recent years: 33 of the 64 entries fall in 2025 and 2026."
- The coding rule in full, from the shared data's `coding_note`: what "toward voters" covers, including "adds to household security through automatic benefits"; that a failed ballot measure counts as "voters kept existing rules" whichever way it leaned; and the note's own caution on ranked-choice and open-primary entries, "readers may weigh these entries differently". Shorten by dropping words, never clauses.
- One example from each side of the coding rule: "A map redrawn in the middle of a decade counts as away from voters whichever party draws it: Texas's HB 4 (August 2025) and California's Proposition 50 (November 2025) both count as away." (RL38, RL41.)
- V7's neutrality line, word for word: "A row's direction describes the rule's effect on who officials answer to and carries no judgment of the people or parties involved."
- The RL47 note (D2-103): "One entry, RL47 (March 2026), stands for all 19 state bans on ranked-choice voting; Missouri's and Indiana's bans also have entries of their own."
- The editor's disclosure (D2-106), labeled "Disclosure:".

Long notes belong in HTML beside or under the drawing, where they wrap, not inside the SVG.

**F2. S08's title comes from the whole log.** No period split in the title, and no split at January 2025 anywhere (it is the month a new administration took office). The title states the whole log's count of toward and away (24 and 24) with its base. If the chart shows time, it shows the base rate (entries per year), marks RL47 as one distinct roll-up mark labeled "19 states", and says in a note that RL47 is dated 2026 while ten of its bans passed earlier. Explainer: the mid-decade maps marker must include every map row (RL38, RL40, RL41, RL50, RL51, RL54, RL56, and the court rows as the coding note treats them) or be removed.

**F3. S03's claims use the right base.** Citizen ballot initiatives: 17 entries, 7 passed and all 7 moved the rules toward voters, 8 failed and left the rules in force, 2 are pending. Never write "ballot measures" for initiatives alone; referendums are ballot measures too, and 3 of 10 moved the rules away. State statutes: 9 of 11 away as logged (8 of 10 without RL47).

**F4. The editor's disclosure** on S03, S06, S07 and S08, word for word from the shared data's `required_text`, labeled "Disclosure:", where the reader sees it with the chart. The verifier now fails a figure without it.

**F5. S06 never tallies the four families.** No "all four up" in a title, badge, tag or note. Under the title: "Up means better for each family; for income and wealth equality, more equal." Gloss each scenario name in a few words ("fusion voting", "forbearance", "inspectors general"). Show each scenario's assumptions (in the table at least). Any glyph must survive a black-and-white copy on its own; Register's boxed arrows are the model. Print V7's words in every cell. Call the class reading "Oath & Action's reading of the atlas's words", never "the studio's".

**F6. S02's title names no policy.** Follow Explainer's title. At the 2021 point: "The timing alone does not show how much of the drop came from the credit." Add a note at 2025 naming the July 2025 law in the log's words: "P.L. 119-21 set the child tax credit at up to $2,200 per child" (RL35), so the chart names both credit laws in its years.

**F7. S04 calls a change of a point or two a change, not a fall,** and says the rates are self-reported, and that Table A-1 publishes no margins of error, so small changes may be within survey error. Explainer's note is the model.

**F8. S05 names its gray lines** ("Gray lines: the other three groups") and notes 2020: "The Census Bureau asks readers to use caution comparing 2020 with other years, after interviews moved to the phone." Breaks at 2003 (race categories) and at the 2002 reweighting stay unjoined; Instrument must stop bridging 2002.

**F9. S07 explains itself.** One line on what ranked-choice voting is ("Voters rank candidates in order; if no one wins a majority of first choices, the last-place candidate drops out and those ballots count for their next choice, round by round."). One line saying a state with no ban may still keep its cities from adopting it, because many cities need the state's permission. The count reads "31 states and DC have no state ban". Every note in the drawing also reaches the equivalent.

**F10. S10 claims only what a grade covers.** A title may say how many of an answer's claims carry each grade; it may not say documented fact "carries" the answer. Print the claim count beside each share. The plausible and contested codes must be told apart at 1x and in grayscale. Where the darkest ink means "the subject" elsewhere, this chart's legend says the grade code replaces that rule here.

**F11. S01** keeps vote totals without a party split (D2-104) and says in one line why the Senate needed 60 votes: "Taking up the bill needed 60 votes, three-fifths of the Senate, to end debate (cloture)." No title may tie the 2023 survey to the 2026 bill as cause; the survey date stays in the title or measure line.

**F12. Reader-facing words.** On the face of a chart and in its notes: no source codes (N40, K1908, W035), no color names (Charcoal, Stone, Verdigris, Prussian; say "the dark line", "the gray bars"), no "the studio" (say "Oath & Action" or "our"). Record IDs (RL38, PW12, E09) may print only in Instrument's index slot and in tables. Source lines name publishers, never codes.

**F13. "How to read our charts" is easy to find.** Each chart's source row links to it, and a short version sits near the top of the White and Newsprint views (five or six lines). The full guide on the `system` view defines all four evidence kinds, lists the title verbs for each grade, says what red does, and explains a survey's margin of error in plain words.

**F14. Phones.** At 390 px the first chart's title sits on the first screen. Small multiples run full width. Toward and away marks differ by shape or fill, never by shade alone, and never in Prussian or red (S03, S08). Small text on Newsprint keeps 4.5:1 or better.

**F15. Accessibility.**
- Every string drawn inside an SVG with `role="img"` appears in its name or its equivalent.
- Each table toggle or Chart and Table switch carries the specimen ID in its accessible name ("Show the S03 table") and shows its open state.
- A view change moves focus to the view's heading and sets `document.title` (Explainer's pattern).
- No heading levels skip.
- Touch targets at least 24 by 24 px, 44 where the layout allows.
- In-row bars stay visible in forced colors.
- Leave about 15 percent headroom in label widths for readers who widen text spacing.

**F16. The kit (DR-49).**
- Generators take data. No hard-coded divisor, row count or label list.
- Chart values live in one `CHART_TOKENS` dict at the top of the build script, read by both the generators and the `system` sheet.
- Fonts are measured from files found by a relative path, or the script stops and says which file is missing.
- One copy function sets curly quotes and apostrophes, dates in words, and the true minus. Explainer's `typo()` and `iso_to_words()` are the model.
- A one-line rule on the sheet: a chart posted alone may mark the point its title names in red; a chart added to a page takes red only when the page's red job moves to it.

**F17. Social card.** Keep the source line. Add no web address: Dustin has not settled the site, so the card names "Oath & Action" and the atlas instead. Board 3 asks him.

**F18. Craft at 2x (the craft review's shared findings).**
- Tabular figures in every drawn chart. In CSS, set `font-variant-numeric` after any `font` shorthand, which resets it (Register).
- Apply tabular figures to numbers only, so hyphens in words do not widen ("Non-Hispanic", never "Non - Hispanic").
- Draw each phone artboard at the width it shows. A drawing must never scale up, so every line weight stays in the 1, 1.5, 2, 3 and 6 px family.
- Set big numbers optically flush with the left edge, correcting the 4 to 5 px side bearing.
- No rule, gridline or leader crosses a word. Place notes clear of gridlines, or give them a knockout in the ground color.
- Notes run 45 to 75 characters a line.
- Dates print in words, with no line break inside a date.
- Extend each generator's layout guard to test label boxes against lines, rules and baselines, not only against other labels.

## Per-concept priorities

- **01 Explainer:** F2's title and map marker first (brand EX-M1, EX-M2; statistics), then the craft report's items (rules crossing words in four places, widened hyphens), then the line-crossing-label guard the production review asks for (S03 and S10 baselines on phones).
- **02 Register:** the S10 title (civic RG-M1), the "How to read" guide (civic RG-M2), F1's full coding rule (brand), the S06 badges (statistics, brand), Prussian off "away" (brand), the S07 count (interface RG-M1), heading levels, phone targets, forced colors, the copy pipeline, and from the craft review: S02's series label on the wrong line (its one must fix), tabular figures in every drawing, and notes at 75 characters a line at most.
- **03 Instrument:** the evidence label's grade words and no source codes (civic IN-M1), S10's two patterns (civic IN-M2), S07's note in the equivalent (interface IN-M1), S06's title (statistics, brand), S01's title (statistics), S05's 2002 bridge, the generators that hard-code `/17` and the missing `ranked_bar()` (production), the copy pipeline (442 straight apostrophes, ISO dates that break), and notes printed over gridlines (craft).

## Checks

```bash
python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest <your page>
```

```bash
node work/build/scripts/phase-2/dataviz_check.js <your page>
```

Both must pass. Do not commit; the main session commits. Finish with a summary under 200 words.
