# Data visualization round: red team report, interface and accessibility

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Lens 3 of the red team brief (`work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Brief.md`), written by the interface and accessibility reviewer, a separate agent working to `.claude/agents/oa-ux-accessibility-lead.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

Pages reviewed:

- 01 Explainer: `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html`
- 02 Register: `work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register.html`
- 03 Instrument: `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument.html`

**I could not run a real screen reader.** No NVDA, JAWS, VoiceOver or TalkBack runs in this environment. Where this report says what a screen reader "hears", it means Chromium's accessibility tree, read through the Chrome DevTools Protocol (`Accessibility.getFullAXTree`) and through Playwright's `ariaSnapshot()`. Playwright 1.63 no longer has `page.accessibility.snapshot()`, so I used those two instead. Chromium's tree lists the drawing's own text under each `role="img"` node. ARIA makes an image's children presentational, so I assumed a screen reader announces only the image's name and treated the drawing's text as out of reach. A real reader may differ.

The shared check passes on all three pages. I ran `node work/build/scripts/phase-2/dataviz_check.js <page> --no-captures` on byte-identical copies in my scratchpad. The script writes a results file beside the page it checks, and I was asked to write nothing else in the repo, so the copies kept the concept folders untouched. All three pass: 5 views at 1440, 390 and 360 px, 0 failures, 0 axe-core violations in 15 runs each, every tested focus stop with a ring. So everything below is something that check cannot see.

## 1. Verdict per concept

### 01 Explainer: 4 of 5

Explainer gives keyboard and screen reader users the best route through the page. A view change moves focus to the new view's heading, and an index link moves focus to that chart's heading. Every drawing note is repeated in words under "Notes in the chart", inside each table toggle. Two things hold it back. The toggles have no visible marker and no visible open state. On four charts, the image's name tells a screen reader user only the chart type and sends them to the table.

**Score 4:** the equivalents are complete and the focus handling is the best of the three; they sit behind toggles that do not look like controls.

### 02 Register: 4 of 5

Register gives screen readers the most by default. S01, S03, S06 and S10 are real HTML tables. Notes are an HTML list beside every chart, and image names carry the values. One image name gives a wrong count (RG-M1). The rest is fit and finish: a skipped heading level on every specimen, focus dropped to the page body after in-view links, 20 and 24 px tap targets in the contents and the sortable tables, and in-row bars that vanish in forced colors.

**Score 4:** the strongest structure for assistive technology, with one wrong number to fix before it ships.

### 03 Instrument: 3 of 5

Instrument has the best phone targets (44 px almost everywhere) and the only Chart and Table switch. The switch works by keyboard, reports its state, and keeps the source visible in both states. But every Table pane opens with "Every value in the chart, with its notes", and some of those notes exist only inside the drawing. The most serious gap is S07's limit on what the map shows (IN-M1). The SVG button also does nothing, silently, while the table is showing.

**Score 3:** the module works well, but its equivalents do not yet carry everything a sighted reader gets.

### What a screen reader user meets on one chart, by default

| | Explainer | Register | Instrument |
|---|---|---|---|
| Name of each drawn chart | 95 to 252 characters; four charts give only the form ("Dot plot of reported voting by age group in 2020 and 2024. The table below carries every value.") | 196 to 1,022 characters, with values | 286 to 1,007 characters, with values |
| Notes from the drawing | In a closed toggle, restated in full under "Notes in the chart" | An HTML list beside every chart, readable at once | Some in HTML, some only inside the drawing (IN-M1) |
| Table | In a closed toggle (`details`) | Visible register on S01, S03, S06, S10; full table in a toggle | Hidden until the Table button is pressed |
| Hidden artboards in the tree | 0 | 0 | 0 |
| Source line | Visible HTML text | Visible HTML text | Visible HTML text, kept in both switch states |

## 2. Findings per concept

Severity follows the brief. Must fix: a reader is misled, blocked or excluded, or a locked rule is broken. Should fix: a clear loss of quality. Polish: detail a top studio would not ship. Each finding names the criterion it meets or fails (WCAG 2.2, the research rules R01 to R28, or the agent standard).

### 01 Explainer

No must-fix findings.

**EX-S1. The table toggles look like plain text and never show their state.** All specimens, every view, every width. The summaries "Show the table and notes" and "How the atlas codes direction" are styled `display:flex`. In Chromium that removes the disclosure triangle. My captures show bold text with no arrow or plus sign. When a toggle opens, its label stays "Show the table and notes" and nothing changes beside it. Why it matters: the table and the written notes are this concept's whole text equivalent. A sighted reader who wants the numbers, such as a low-vision reader at high zoom or a teacher, has no cue that this line opens anything. Screen readers do get the expanded state from the native element. Criterion: agent standard, "Each state has visible text or a shape change in addition to color"; R21, since the equivalent has to be findable. Fix: put a marker in the summary, a plus that turns into a minus or a chevron that turns over (CSS content with empty alt text, `content: "+" / ""`). Switch the label to "Hide the table and notes" when the toggle is open.

**EX-S2. Four image names state only the chart type.** S03, S04, S08 and S09, White, Newsprint and Charcoal. The names are "Ranked bar chart of the 64 repair-log entries by instrument, each split by direction. The table below carries every value.", "Dot plot of reported voting by age group in 2020 and 2024. The table below carries every value.", "Unit chart of the 64 repair-log entries by year and direction. The table below lists every entry." and "Timeline of 24 rule changes from 1870 to 2026 on four lanes. The table below lists every event." Why it matters: a sighted reader takes in the pattern at a glance, for example that statutes moved the rules away from voters and initiatives never did. A screen reader user hears the title, then this name, and has to open a toggle and read a table to get the same picture. Register and Instrument put the values in the name. Criterion: WCAG 1.1.1 is met only in the minimum sense; R21. Fix: write each name the way S01 and S02 already are. State the pattern and the key numbers, for example "State statute 11, 9 away from voters; ballot initiative 17, none away; court ruling 14, 8 away".

**EX-S3. S09's four thread questions drop out at 200 percent zoom and on phones, and never reach the table.** S09, White and Newsprint. At 1440 px the drawing prints "Who counts" with the question "Who gets to vote, and whose vote counts fully?" beside it, and a question beside each of the other three threads. At 720 px (a 1440 px window at 200 percent) and at 390 and 360 px, the narrower drawing prints only "WHO COUNTS". The table's Thread column says "Who counts", and "Notes in the chart" does not carry the questions. Why it matters: the questions explain what each thread means. Zoom users, phone readers and screen reader users never meet them. Criterion: WCAG 1.4.10 (no lost content on reflow); R21. Fix: add the four questions to the table's caption or notes, and print them under the thread names on the 600 and 320 px drawings.

**EX-S4. S10's grade meanings live only in the drawing's key.** S10, White, Newsprint and Charcoal. The key reads "Documented: on the public record", "Well supported: strong research evidence", "Plausible: some evidence" and "Contested: evidence disputed". The table gives only the grade names as column headers, and the notes do not define them. Criterion: R21. Fix: add the four definitions to "Notes in the chart". The same gap is in Instrument (SH-2).

**EX-P1. S07's image name tells screen reader users to hover.** "Tile map of the 50 states and DC: 19 states ban ranked-choice voting, 17 in all elections. Hover a square for its state. The table below lists every state." The tiles cannot take keyboard focus. Fix: drop "Hover a square for its state."

**EX-P2. S06's scroll box is a focus stop that never scrolls, and its name is wrong at phone width.** The region is named "Scenario table, scrolls sideways when narrow" and carries `tabindex="0"`. At 1440 px it is 1,024 px wide and fits. At 390 px the table reflows into cards 2,694 px tall and does not scroll sideways. Fix: drop the region role and the tabindex, or keep them only when the table overflows.

**EX-P3. S08 on a 360 px phone: the "To 2012" label touches both axis rules.** In my 2x capture, the left rule runs through the "T" and the right rule touches the "2". The shared check tests text against text only, so it cannot see this. Fix: widen the year column on the 320 px drawing by about 8 px.

**EX-P4. The "Other views" links in each view header are 24 px tall on phones.** "Newsprint" 75 by 24, "Charcoal" 65 by 24, and so on, in a list 41 px apart. They pass WCAG 2.5.8 through the spacing exception and miss the brief's 44 px. Fix: give the links a 44 px line box.

### 02 Register

**RG-M1. S07's image name gives the wrong count of states with no ban.** S07, White and Newsprint, every width (four drawings). The name says "17 states ban ranked-choice voting in all elections, 2 in some (Ohio and Tennessee), and 32 states and DC have no state ban, as of November 2026." The visible key says "No state ban **31 states and DC**", and 50 states less 19 is 31. Why it matters: a screen reader user gets a number that disagrees with the chart a sighted reader sees, on the specimen about where a city can adopt ranked-choice voting. I scripted a check that every number in every image name appears somewhere else in its figure; this was the only real mismatch on any page. Criterion: R28 (every number traces to data); R21; WCAG 1.1.1. Fix: "31 states and DC have no state ban". Better still, build the name from the same count the key uses.

**RG-S1. Every specimen title skips from heading level 1 to level 3.** White, Newsprint, Charcoal and Social views. The view heading is an `h1` and the ten chart titles are `h3`, with no `h2` between. Screen reader users who move by heading level, or who scan a list of headings, get a broken outline. Criterion: agent standard, "Headings form a correct outline"; WCAG 1.3.1 (best practice). Fix: make the specimen titles `h2`, as Instrument does, or add an `h2` per plate.

**RG-S2. Links inside a view drop keyboard focus to the page body.** White view header links ("Newsprint", "Charcoal", "Social card", "System") and the contents links "S01" to "S10". After Enter on "Newsprint" in the White view header, focus sits on the page body, because the link's own view is now hidden. After Enter on "S03" in the contents, the page scrolls to the plate and focus also sits on the body. Chromium's next Tab lands in the right place, but nothing is announced, and some screen reader and browser pairs restart from the top of the page. Explainer moves focus to the new view's heading and to the chart's heading. Criterion: WCAG 2.4.3 (focus order); agent standard on keyboard. Fix: copy Explainer's router. After a view change, focus the new view's `h1`, with `tabindex="-1"` set on it. After a contents link, focus the plate's title.

**RG-S3. Tap targets in the contents register and the sortable tables are 20 to 24 px tall on phones.** White view, 390 and 360 px. The contents links "S01" to "S10" measure 29 to 34 by 20 px. With the S07 to S10 tables open, 23 sort buttons measure 24 or 36 px tall, and the "ID" sort button is 13 px wide. All pass WCAG 2.5.8 through the spacing exception. All miss the brief's 44 px, and a 13 px wide button is hard to hit with a thumb. Fix: make the whole contents row the link, or pad the link to 44 px. Give each sort button a 44 px minimum height and width, or move the sort options into one labeled control above the table.

**RG-S4. The in-row bars disappear in forced-colors mode.** S01, S03 and S10 (and the S03 plate on the System and Charcoal views). The bars are HTML spans painted with `background-color`, which forced colors replaces with the page color. Under Chromium's forced-colors emulation, S01's party bars and S03's "Rule changes" column are empty, and only the Pending swatch's dashed border is left. Every count still prints, so nothing is lost, but the figure is gone for Windows contrast-theme users. Criterion: Master Brief section 22 (forced colors); WCAG 1.4.11. Fix: add `forced-color-adjust: none` to the bar spans, or draw each bar with a border, or as inline SVG as the line charts are.

**RG-P1. Row headers in S03 carry notes, so the note repeats in every cell.** The row header reads "Ballot initiative None of 17 moved the rules away from voters." and likewise "State statute 9 of 11 moved the rules away from voters.". A screen reader repeats the row header at each cell in that row. Fix: move each note into its own cell or a footnote, and keep the header to the instrument's name.

**RG-P2. The toggle's plus sign is part of its name.** The accessible name is "+ Show the table", and "− Show the table" when open, because the sign is CSS generated content. The label stays "Show the table" when open. Fix: `content: "+" / ""`, and "Hide the table" when open.

**RG-P3. S01's party register reads as loose text.** A screen reader hears "Democrats 88 % Republicans 87 % 0 100%". Fix: mark the register as a list, or a two-column table, and hide the 0 and 100% scale labels from assistive technology.

**RG-P4. The sort arrow is read aloud.** The header button's name becomes "Date ↓". `aria-sort` already carries the state. Fix: `content: "\2193" / ""`.

**RG-P5. S06's glyphs carry the studio's reading only for sighted readers.** The cells read V7's words ("up in reform states"). The glyph that shows the studio's reading is hidden from assistive technology. Explainer's cells read "Up: Up in reform states". Fix: add the class as visually hidden text before each cell's words.

### 03 Instrument

**IN-M1. The Table pane leaves out notes that exist only in the drawing, including S07's limit on what the map shows.** S07, White and Newsprint, every width; the same pattern in S02, S09 and S10. Every Table pane opens with "Every value in the chart, with its notes. The source line stays below." On S07 the drawing carries four notes:

- "Ohio, 2026: home-rule cities may still adopt it, but they lose state local government fund money while it is in effect."
- "Tennessee, 2022: county election commissions may not use it for state or local offices."
- "Missouri wrote its ban into the state constitution in 2024; the other 18 are statutes."
- "The map shows state bans only. Whether a city in a state with no ban may adopt it depends on other state law, which the map does not show."

None of the four is in the image name, the HTML notes or the Table pane. The Ohio and Tennessee scope does reach the table, as each state's scope text. The Missouri note and the last note never reach assistive technology. Why it matters: the reader question is "Where can a city adopt ranked-choice voting?" A screen reader user hears "The other 31 states and DC have no state ban" and nothing that limits it, so they can conclude that a city in any of those states may adopt it. That is the reading the sighted note exists to prevent. Smaller cases on other modules:

- S02's 2021 note "(RL15) … It expired after 2021 (RL16)" is in neither the name nor the table.
- S10's key definitions ("Plausible: some evidence", "Contested: evidence disputed") and its note "PW16, algorithms in daily life: 7 of its 22 claims are plausible or contested, the largest share of any question." are in neither.
- S09's four thread questions are in neither.

Criterion: R21 ("carries everything a sighted reader gets, notes and source included"); R22; WCAG 1.1.1. Fix: build the Table pane from the same note list the drawing uses, and print the notes under the table, as Explainer's "Notes in the chart" does. Add the S07 limit to the image name as well.

**IN-S1. The SVG button does nothing while the table shows.** Any module with an SVG download. With the Table pane showing, "Download this chart as SVG" stays enabled. In my test, no download started within 2.5 seconds and nothing told the reader why. The script exports the first visible drawing, and the drawing is hidden. Criterion: agent standard, "A disabled action says why it is unavailable and what makes it available"; WCAG 3.3.1 in spirit. Fix: export the hidden chart drawing anyway, since the reader asked for the chart. Or set `aria-disabled="true"` with the visible note "Switch to Chart to download the drawing".

**IN-S2. The pressed state of Chart and Table shows only as a fill.** All modules. The pressed button is Charcoal with White text, and the other is outlined. Under forced-colors emulation both buttons look the same, so the state disappears. Screen readers get it from `aria-pressed`. Criterion: agent standard, "Each state has visible text or a shape change in addition to color"; WCAG 1.4.1 and 1.4.11 under forced colors. Fix: add a shape cue to the pressed button, such as a 3 px underline bar or a check mark, and map it to `Highlight` and `HighlightText` in a `@media (forced-colors: active)` block.

**IN-S3. There is no index of the ten modules.** The White and Newsprint views. Explainer and Register list the ten charts at the top; Instrument does not. The White view has 50 Tab stops, four per module. A keyboard user needs 48 presses from the skip link to reach S10's Table button, and the phone page runs past 18,000 px. Criterion: agent standard (anchor links, navigation); WCAG 2.4.5. Fix: add a ten-link module index under the header, and have each link focus the module's title.

**IN-S4. Plausible and contested look alike in S10's narrow segments.** S10, every view that shows it. Plausible is a dashed fill and contested a dash-dot fill. In the 1440 px capture, Grocery prices has two plausible and two contested claims side by side, and they read as one patterned block, in color and in grayscale. No count prints inside those segments; the counts sit behind the Table button. Criterion: R26, WCAG 1.4.1 and 1.4.11. Fix: make the two patterns differ in density or angle (open dots against a dense hatch, say), or print the plausible and contested counts at the bar's end.

**IN-S5. Links inside a view drop focus to the page body.** Same behavior and fix as RG-S2. Enter on "Newsprint The same ten modules on the warm ground…" in the White view header leaves focus on the body.

**IN-P1. The social card's image name points to a button that is not there.** Social view. The card's chart name ends "The Table button lists every value." The social view has no Table button. Fix: drop the sentence on the card, or point to the table under the card.

**IN-P2. The pointer readouts ask the reader to point.** S07, S08 and S09: "Point at a state to read its law. The table lists every state." The readout is hidden from assistive technology and does nothing for keyboard users. Fix: "The table lists every state." alone, or make the marks focusable and update the readout on focus as well.

**IN-P3. "Download this chart as SVG" has the same name in every module.** The CSV buttons already name the module ("Download the S03 data as CSV"). Fix: "Download S03 as SVG".

**IN-P4. S03's Away and Toward fills sit about 2.7:1 apart.** I computed this from the notes' hex values (#121212 against #3C5F59). The "Mixed" split pairs the same two inks diagonally. Every count prints and the order of segments never changes, so this is detail. Fix: lighten Toward one step, or add a 1 px ground-colored gap between segments.

**IN-P5. The focus ring on Newsprint measures 3.37:1.** It passes the 3:1 floor, with the least margin of the three concepts (Verdigris 2 px). Fix: switch the ring to Charcoal on light grounds, as Explainer and Register do, or make it 3 px.

## 3. Shared findings

**SH-1 (should fix, all three). Chart labels collide when a reader sets wider text spacing.** I injected the WCAG 1.4.12 values on the White view at 1440 px: line height 1.5, letter spacing 0.12 em, word spacing 0.16 em, paragraph spacing 2 em. HTML text reflowed with no clipping on any page. SVG labels overlapped or ran past their drawing:

| Concept | Overlaps | Past the drawing's edge | Specimens with collisions |
|---|---|---|---|
| Explainer | 14 | 25 | S01, S02, S03, S04, S05, S08, S09, S10 |
| Register | 2 | 6 | S02, S05, S09 |
| Instrument | 13 | 16 | S01, S03, S05, S07, S09, S10 |

The tables stay readable, so no number is lost, but the drawing breaks for readers who use spacing tools. Fix for the kit: leave label headroom of about 15 percent in the generators' width budgets, and put long notes in HTML beside the drawing, as Register does, where they can wrap.

**SH-2 (should fix, Explainer and Instrument; Register in part). Text in a drawing's key or notes never reaches assistive technology.** S10's grade definitions are missing in Explainer and Instrument. S09's thread questions are missing in all three: Register's S09 name gives the thread names without the questions. The rule for the kit: every string the generator draws inside an SVG with `role="img"` is either in the image name or in the equivalent. A build-time check can compare the two lists. I did that by script for this report.

**SH-3 (should fix, all three). S06's tints vanish in forced colors.** The cell tints are CSS backgrounds. Under forced-colors emulation the glyphs and V7's words remain, so the reading survives. Name this in the palette spec: in contrast themes, a tint never carries meaning that its glyph does not also carry.

**SH-4 (polish, Register and Instrument). A view change is not announced.** After a masthead link, focus stays on the link and the document title never changes ("Register Chart System", "Chart system 03, Instrument"). Explainer moves focus to the new view's heading, which a screen reader then reads. Fix: copy Explainer's focus move, and set `document.title` per view (for example "Newsprint · Register chart system").

**SH-5 (polish, all three). Ten toggles or buttons share one name.** "Show the table and notes" ten times (Explainer), "Show the table" ten times (Register), "Chart" and "Table" ten times (Instrument, where the group name "Show S03 as" helps on entry). In a screen reader's list of controls they cannot be told apart. Fix: add the specimen ID as visually hidden text ("Show the S03 table").

**SH-6 (polish, all three). Text set in capitals by CSS reaches the tree in capitals.** Chromium exposes `text-transform: uppercase` text as capitals: "FINDING", "WHAT CONGRESS DID NEXT", "QUALITY OF DEMOCRACY" (Explainer S06 on phones), "STATE" and "STATUS" (Instrument's phone tables). Some screen readers spell out short words in capitals. Fix: none needed for long words. For short labels, keep the capitals and add `aria-label` text in sentence case, or accept it and record the decision.

**SH-7 (polish, all three). Masthead targets.** The wordmark link is 358 by 16 px at 390 px (328 by 16 at 360), and the "White" view link is 42 by 44 px. Both pass WCAG 2.5.8 through spacing. Fix: give the wordmark link 14 px of padding top and bottom, and give the view links a 44 px minimum width.

**SH-8 (pass, all three, with one note for the kit).** Reduced motion has nothing to act on. I scanned every stylesheet and drawing: 0 transitions, 0 animations, 0 keyframes, no smooth scrolling, no SVG animation. The type is set in px with no rem anywhere, and pinch zoom is allowed (`initial-scale=1`, no maximum scale). Browser zoom works; settings that scale only text will not move this type. Record the motion rule in the kit now, so the first animated chart arrives with a `prefers-reduced-motion` path.

### What passed in all three

These checks found no fault in any concept:

- Table semantics: every table has a `caption`, a `thead` and `th` cells with `scope`; I found 0 `th` without scope. Every body row starts with a row header.
- Phone tables (Explainer S06, Register's registers, every Instrument table) reflow into labeled rows and keep table semantics in the tree.
- Hidden artboards are `display:none`: 0 hidden drawings reach the tree, so each chart is announced once at every width.
- Small text on Newsprint: the lowest small-text contrast is 5.49:1 (Deep Stone). That includes everything inside opened toggles and Table panes, which the shared check skips because it measures only visible text.
- Text that sits on hatch or dash fills (Explainer S03 and S10, Instrument S10 keys) could not be measured by script; see the tested list.
- At 720 and 640 px with double density (200 percent zoom on a 1440 or 1280 px window): no sideways scroll on any view, no text under 13 px, and no lost content apart from EX-S3.
- Reading order follows visual order in every figure. The studio strips sit before (Explainer) or after (Register, Instrument) the figure in the source, matching where they show. CSS reordering touches only Register's S10 bar cell on phones, which carries no text.
- No keyboard traps, and no focus hidden behind sticky elements. Explainer's sticky studio strips sit in their own column and never covered a focused control.
- Focus rings measure: Explainer 3 px Charcoal (18.73:1 on White, 13.29:1 on Newsprint, Newsprint on Charcoal 13.29:1); Register 2 px with the same colors; Instrument 2 px Verdigris (4.74:1 on White, 3.37:1 on Newsprint, Newsprint on Charcoal 13.29:1).

## 4. What I tested and what I could not test

### Tested

- The shared rendered check on scratch copies of all three pages (byte-identical, so the concept folders' results files stayed as they were): PASS, 0 failures, 0 axe-core violations. Focus stops reached on White at 1440 px: Explainer 34, Register 31, Instrument 40 (the script stops at 40).
- Chromium's accessibility tree for the White view of each page at 1440 and 390 px, with toggles closed and opened, plus the Social view at 390 px and single figures at 390 px with tables shown. I read each chart's name, role and position against the visible chart.
- A script that lists every line of text in each visible drawing and checks whether its word pairs appear in what assistive technology can reach: image names, HTML text, toggles and Table panes. I then read each flagged line by hand against the equivalent; most flags were reworded notes and are not findings.
- A script that checks every number in every image name against the rest of its figure, on the White, Charcoal and Social views. It found RG-M1.
- A full Tab walk of the White and Newsprint views at 1440 px and the White view at 390 px, recording order, position, ring style and whether anything covered the focused element.
- Keyboard tests of each skip link, a contents link, an in-view link and a masthead link, recording where focus landed and where the next Tab went.
- Instrument's Chart and Table switch on S03 at 1440 and 390 px: 21 Tab stops to reach it; Enter shows the table, `aria-pressed` changes, the source stays visible; Space returns to the chart; CSV downloads `S03-data.csv`; SVG gives nothing while the table shows.
- Tap target sizes for every link, button, toggle and focusable region on all five views at 390 and 360 px (touch emulation), with toggles and Table panes both closed and open, against 44 px and WCAG 2.5.8.
- Text contrast of every visible text node, and focus-ring contrast, on all five views at 1440 and 390 px, with every toggle and Table pane open.
- 200 percent zoom: viewport 720 and 640 px at double density, all five views; plus visible-text comparison across 1440, 720, 640, 390 and 360 px for every White view figure.
- Text spacing override (WCAG 1.4.12) on each White view at 1440 px.
- Forced colors under Chromium emulation, screenshots of Register S01, S03 and S08; Instrument S03, S06 and S08; Explainer S03 and S06.
- Grayscale screenshots of S03, S08 and S10 in each concept at 1440 px.
- A scan of every stylesheet and drawing for motion, focus styles, generated content and reordering.
- By eye, from my own captures: Explainer S09 at 720 px, S08 and S07 at 360 px, S04 opened at 390 px; Register S07 at 360 px; Instrument S03 at 720 px and S07 at 360 px. Captures are in my scratchpad, `/tmp/claude-0/-home-user-Dustin-s-Command-Center/bce9c31a-68c6-5654-913f-e031125afc9e/scratchpad/shots/`.

### Could not test

- Any real screen reader: NVDA, JAWS, VoiceOver on Mac or iPhone, TalkBack. I do not know how each one treats the text Chromium lists inside a `role="img"` drawing, or how each reads text set in capitals.
- Real phones, iOS Safari Page Zoom, iOS Dynamic Type, Android text scaling, and browsers other than headless Chromium.
- Windows contrast themes on Windows itself (only Chromium's forced-colors emulation).
- Voice control (Voice Control, Dragon), switch access and screen magnifiers.
- `prefers-reduced-motion` in emulation; I did not run it because the pages carry no motion to reduce.
- Print.
- Keyboard walks of the Charcoal, Social and System views in full; I measured their targets and contrast but did not Tab through them.
- Text over hatch and dash fills; the script cannot compute a contrast against a pattern.
- Opening the downloaded CSV and SVG files in other software.
- Any test with real readers.

## Files

Created: `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Interface-Accessibility.md` (this report). Modified: none. Page copies, scripts, accessibility-tree dumps, results files and screenshots stayed in my scratchpad.
