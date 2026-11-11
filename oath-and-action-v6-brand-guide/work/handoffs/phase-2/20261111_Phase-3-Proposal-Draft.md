# Phase 3 proposal: evidence, data and systems

Oath & Action Edition 06. Draft for Gate 2, November 11, 2026. Written by the data visualization and systems lead, with the research lead's source standards, for task 7 of `work/handoffs/phase-2/20261111_Gate-2-Brief.md`. The main session places it in the Gate 2 report and on the board's first panel. Paths are relative to `oath-and-action-v6-brand-guide/`.

## What you approve

Phase 3 builds chapter 13 Evidence and sourcing, chapter 14 Data visualization and chapter 15 Systems graphics, with the chart kit behind them, and ends at Gate 3. Chapter 14 holds the 127 forms you approved on November 6 (DR-62), built in the order you set there: the kit first, then five rounds of forms (DR-63). Chapter 15 draws Atlas V7's six worked examples, Reform R-01 among them, with a workflow for each of the atlas's 11 routes to change and the final reconciliation table. You see three boards before Gate 3 (DR-228). The guide stays one file, and chapter 14 may not pass 1.75 MB (DR-227).

To approve, reply "As proposed" or name your changes, and answer the four questions in section 10.

| Phase 3 item | Size | Where you see it |
|---|---|---|
| Chapter 13 Evidence and sourcing | About 12 rules | Board 1 |
| The chart kit and the data palettes with their proofs | The 16 specimens built in Phase 2, rebuilt from their data by one command | Board 1 |
| Chapter 14 Data visualization | 127 forms in 16 families: 56 core, 41 extended, 22 reference, 8 to avoid | Boards 1, 2 and 3 |
| Chapter 15 Systems graphics | 6 worked examples, 11 workflows, the reconciliation table | Board 3 |
| Page weight | Chapter 13 at most 0.25 MB, chapter 14 at most 1.75 MB (a hard stop), chapter 15 at most 0.60 MB | Every build, and on each board |
| Gate 3 report | Scores, checks, decisions and the Phase 4 proposal | After board 3 |

## 1. What Phase 3 produces

| Output | What it holds | Lead | Done when |
|---|---|---|---|
| Chapter 13 Evidence and sourcing (`#evidence`) | The four title types, grade words and title verbs, the evidence line code, the source line, Illustrative labels, typed ID chips, as-of dates, documented events, quotes (section 1.1) | Editor with the data lead | Each rule has its purpose, a correct plate and a failure plate, and scores 4 or more on all six criteria |
| Chapter 14 Data visualization (`#data-visualization`) | The selection guide by reader question; the 127 forms by tier (section 1.2); the data palettes; chart interaction and exports; three complex examples | Data lead with the chart makers | Every core and extended form finished on real or labeled data, every reference and avoid entry with its rule, twenty specimens passed early in round 1 |
| Chapter 15 Systems graphics (`#systems-graphics`) | The grammar mapped to V7's fields with a reading rule for each; the six worked examples (section 1.3); the interaction rules; the 11 workflows (section 1.4); the reconciliation table (section 1.5) | Data lead with the systems designer | The V7 check finds 0 mismatches, and every workflow cites an official source with the date it was checked |
| The chart kit | The `oa.chart` tokens completed; one generator per form that takes a data file; `register_chart()`; the layout guard; SVG, PNG and CSV exports; one command that builds a chart and runs its checks; the fonts and license texts the guide embeds (D2-1697) | Engineer with the Explainer maker | The 16 built specimens rebuild from their data files through the kit and pass every check |
| Data files | One file per specimen in `work/build/data/`, each with a sidecar naming the publisher, table or series, URL, period, geography, vintage, date retrieved, the qualification and the printed source line | Research lead | Every number that does not come from Atlas V7 traces to a sidecar and a research ledger row |
| The data palette specification | Sequential, diverging and categorical palettes, the magnitude steps and the grade line code on each approved surface, with contrast, grayscale and color-vision proofs (section 1.6) | Data lead with the design director | Proofs on board 1; written into chapter 14 in round 5 |
| Gate 3 report | Scores, checks, decisions, open questions, the Phase 4 proposal and the change log | Main session | You read it at Gate 3 |

### 1.1 Chapter 13, proposed rules

Chapter 13 holds the rules every chart, diagram and claim in the guide obeys. Where chapter 01 or chapter 02 already states a rule, chapter 13 cites it by number and shows its evidence side, so no rule is stated two ways. The editor and I fix the final list in round 0.

| Proposed rule | What it settles | Related rule or decision |
|---|---|---|
| Title a chart or diagram as a finding, an association, an estimate or an illustration | The four title types (Master Brief section 15, tension 5) | Chapter 14's chart anatomy |
| Give the title the verb its grade allows | One grade table for the whole guide | H08 in chapter 02, cited |
| Print V7's grade words with a plain gloss | One display word for each of V7's grade labels on connections, issues and claims, with the mapping table tension 8 asks for | Gate 1, M2 |
| Draw a connection's grade in V7's line code | Solid for documented and well supported, dashed for plausible, dotted for hypothesis, dash-dot for contested, with the record square and the hollow line | Gate 1, M1 |
| Keep grade, effect size, uncertainty and delay apart | Four properties, each with its own mark | Gate 1, M4 |
| Write the source line in its six parts | Publisher, title or table, period, geography, date retrieved, qualification | H04 |
| Print the period and the vintage, and give charts shown together one window | The vintage rule in section 2.3 | H09, DR-64 |
| Label an invented item beside it, or once at the head when everything is invented | Illustrative labels; invented bills numbered from H.99001 and S.99002 | H03, DR-97, DR-151 |
| Name every atlas ID in its typed chip | "Variable B4", "Loop B4", "Reform R-01" | H11, Gate 1, M3 |
| Date a rule or count that changes, and print an undated route as not checked | As-of dates from V7 and from each source | V7's `checked` dates on routes |
| Draw documented events apart from causal findings | Repair log and delivery log entries drawn as records | Gate 1, M4 |
| Quote a person exactly, with who, when and where | Quotes, testimonials and endorsements, and where a quote may sit in a data graphic | Rules 01.22 and 01.23, cited |

### 1.2 Chapter 14 and the 127 forms, in the order you set

The coverage plan's build order names 15 of its 16 families. Proportion and overlap has no round, so I place it in round 4 beside the infographics, since its icon arrays draw on Civic Line as they do (DR-61) and round 4 carries the lightest load.

| Round | What it builds | Forms | Core | Extended | Reference | Avoid | Makers |
|---|---|---|---|---|---|---|---|
| 0 | The chart kit, the palettes and their proofs, chapter 13, and the 16 specimens from Phase 2 rebuilt in the kit (they cover 19 of the 127 forms) | 0 new | | | | | Engineer and the Explainer maker; data lead and design director; editor |
| 1 | Comparison, shift and swing, change over time, tables and plain words | 41 | 26 | 11 | 2 | 2 | Two makers |
| 2 | Composition, distribution and density, correlation, uncertainty and estimates, gauges and indicators | 41 | 15 | 11 | 11 | 4 | Two makers |
| 3 | Maps, structure, relationships, flow, behavior | 32 | 9 | 14 | 8 | 1 | Two makers, a cartographer among them |
| 4 | Infographics and social formats, with proportion and overlap | 13 | 6 | 5 | 1 | 1 | A maker with the design director |
| 5 | The selection guide by reader question, the palette specification written up, three complex examples | 0 new | | | | | Data lead, main session and accessibility lead |
| All | 16 families | 127 | 56 | 41 | 22 | 8 | |

**Twenty specimens early.** Round 0 rebuilds S01 to S16 through the kit. They test the kit and the drawing method on real charts, and round 1's first four new forms pass the Master Brief's floor of twenty.

**Three complex examples (round 5).** I recommend one per domain, so the three do not crowd one topic (Rule 01.9):

| Kind | Example | Why this one |
|---|---|---|
| Chart | S14, monthly job change with its three-month average, from FRED's copy of the Bureau of Labor Statistics series | It has a time window to state, preliminary months to mark, and a CSV export that maps row for row to the chart |
| Systems diagram | Loop B4 and Loop R10 stepped one connection at a time, with pause, reset and a still sequence | The two loops share Variable C3, Risk of losing office, so a reader sees one variable work in two loops |
| Policy comparison | The three reforms that act on Loop R8: Reform R-06, "Hold local elections alongside November races"; Reform R-30, "More homes allowed by right near jobs"; and Reform R-38, "Limits on pricing software using rivals' data"; compared by target, band, ordinal effects, grades and routes, with no summed score | Several of their effects carry V7's qualifiers ("+L local", "+S delayed", "+M renter-owner"), which tests that the guide keeps them |

### 1.3 Chapter 15's six worked examples

Every value below was read today by script from `work/extract/atlas-v7-data.json`, which matches `work/research/atlas-v7-docs/20261015_Atlas-V7-Model.json` byte for byte (V7 snapshot of October 15, 2026). The build reads them again; nothing here is typed by hand into a chapter.

| # | Example | V7 values | What the reader learns |
|---|---|---|---|
| 1 | Loop R1, "Wealth and political influence reinforce each other" | Reinforcing; closed, every step numbered; the loop graded plausible, delay long. L01 A1 to B1, +, money, well-supported, S. L02 B1 to E1, +, money, plausible, M, which V7 names the weakest step. L03 E1 to A1, +, money, well-supported, L | The least certain step sets how far a reader can trust the whole loop. This example uses chapter 11's live loop stepper, which already runs Loop R1 (DR-195) |
| 2 | Loop R8, "Housing scarcity strengthens owners' incentive to restrict building" | Closed; L38 A5 to A6, +, causal, well-supported, L; L39 A6 to A5, +, causal, well-supported, L. V7's evidence field says "the loop no longer depends on A1" | How to show a revision of the model in V7's own words, with no earlier drawing offered as evidence |
| 3 | Loop B4, "Electoral consequences can improve public performance", beside Loop R10, "Safe seats shift accountability to small primary electorates" | B4: L23 D5 to C3, −, well-supported, S; L24 C3 to C5, +, well-supported, M; L54 C5 to D5, +, well-supported, M, the weakest for U.S. services in V7's evidence summary. R10: L08 C1 to C2, +, documented, S; L25 C2 to C3, −, well-supported, S; L53 C3 to C4, −, plausible, M, the weakest; L42 C4 to C1, +, documented, M | One accountability chain read in both directions, through the variable the two loops share |
| 4 | Reform R-01, "All-party primaries with ranked general elections" | Targets L25, L08 and C2; loops R10, B4 and R11; band, rules. Effects: Quality of democracy +M, Government efficacy +S, Economic performance 0, Income and wealth equality 0; V7 rates its confidence "medium (participation); low (moderation)". Problem evidence plausible, remedy evidence plausible_contested. Routes: BI medium (checked October 15, 2026), SS low (not checked), LOC medium (checked October 15, 2026), FS very low (not checked) | A reform marked at its actual targets with chapter 12's red target (Rule 12.5), four ordinal effects shown side by side with no total, and each route's date or its absence printed (D2-1700, DR-223) |
| 5 | The authority diagram | Seven authority connections, all documented, none signed and none in a loop: LE02 D1 to EC2 (M), LE03 D2 to EC2 (S), LE19 D2 to EC10 (S), LT13 D4 to TC7 (S), LT14 D6 to TC7 (S), LT16 D2 to TC5 (S), LT17 D1 to TC5 (M) | Who holds the power to set a level, drawn with no causal sign so it can never close a loop |
| 6 | Loop B2, "Automatic benefits cushion economic shocks", with Loop B3 and Loop R9 named beside it | Balancing; "conceptual: no complete numbered chain"; graded well supported; delay short | A mechanism can be well supported and still lack a numbered chain, so closure and grade are separate things to disclose |

R-01's status text in V7 describes two ballot measures that went to voters on November 3, 2026, after the snapshot. The example prints V7's values with the date "as of October 15, 2026" beside the status and routes, the research lead records the outcomes in the research ledger, and the update goes to the V7.1 issue list. The studio never edits V7.

### 1.4 The policy workflows, one for each V7 route

Each workflow is the full route with its alternative paths, vetoes, funding, implementation and reversal. Chapter 11's six-step trackers (Rules 11.1 to 11.10) stay the reader's display for the most common routes, and chapter 15 shows how each display step maps to the stages behind it. V7 holds 126 route entries across its 50 reforms; 13 carry a check date (October 15, 2026), and the guide prints the other 113 as not checked.

| V7 code | V7 name and instrument | Stages the research lead verifies | V7 entries | Official sources, and how they answered today | Tracker display |
|---|---|---|---|---|---|
| FS | Federal statute: Act of Congress, including appropriations and reconciliation | Introduction, committee, floor, the other chamber, reconciling differences, presentment, signature, veto or pocket veto, override, appropriations, agency rulemaking, litigation, repeal or sunset | 38 | `How Our Laws Are Made` on govinfo.gov, house.gov and clerk.house.gov answered; api.congress.gov answered; congress.gov's pages refused | Chapter 11's six steps, step 6 "President" (DR-128) |
| SS | State statute: a bill passed and signed, or a state agency rule | The same skeleton with each state's veto types, line-item veto and override thresholds | 29 | State constitutions and legislature pages, one state per region; ncsl.org refused; Ballotpedia answered, labeled secondary | Six steps, step 6 "Governor"; Nebraska's one chamber (DR-150) |
| BI | State ballot: citizen initiative, referendum or legislative referral | Petition, certification, ballot title, election, implementation, legislative amendment or repeal where allowed, court challenge | 11 | State election offices; Ballotpedia, labeled secondary | A new step set if you say yes to question 3 |
| LOC | Local: ordinance, charter amendment or local practice | Introduction, hearing, readings, vote, signature or veto, referendum petition where allowed, state preemption | 15 | City charters of sample cities in four regions, and each state's home-rule law | Six steps, as chapter 11 sets them |
| FA | Federal executive action: executive order, agency rule, guidance | Order or proposed rule, comment period, final rule, Congressional Review Act window, litigation, revocation by a later administration | 7 | archives.gov and regulations.gov answered; federalregister.gov sent a bot check | Chapter 11's agency rule tracker (Rule 11.9) |
| FR | Chamber rule or confirmation | Rule change by a majority; nomination, hearing, committee vote, cloture, confirmation vote | 6 | house.gov and senate.gov's home page answered | None today |
| ENF | Enforcement and litigation | Investigation, complaint, settlement or consent decree, trial, appeal, compliance term | 5 | uscourts.gov answered | None today |
| CRT | Court doctrine | Filing, ruling, appeal, review by a higher court, decision, remand, later doctrine | 7 | uscourts.gov answered | A new step set if you say yes to question 3 |
| AV | Article V: constitutional amendment | Proposal by two-thirds of each chamber or by a convention, ratification by three-quarters of the states | 3 | archives.gov's Article V page answered; law.cornell.edu answered, secondary | None today |
| IC | Interstate compact | Drafting, enactment state by state, the threshold reached, consent of Congress where required, administration, withdrawal | 1 | Member states' statutes | None today |
| CIV | Civil society | No government stage: organize, fund, act, sustain | 4 | No official source needed | None today |

Records requests (Rule 11.8) follow a public records law, which V7 does not treat as a route; chapter 15 maps them to SS and LOC in a note.

### 1.5 The reconciliation table

Phase 0 compared every atlas diagram in V5 Polished, the Atlas Visual System and Concepts V2 with V7: 2,644 comparisons, two value conflicts and 45 rows of conflicts and ambiguities (9 ID, 1 sign, 1 grade, 1 delay, 12 label, 7 structure, 14 encoding), in `work/handoffs/phase-0/20261020_Atlas-Reconciliation-Table.md`. Those source files are not in this container, so Phase 3 re-runs the comparison from Phase 0's committed extraction (`20261020_Atlas-Reconciliation-Data.json`) against today's V7. The final table adds where the guide applies each resolution (chapter and rule), its status, and new rows for what Phase 2 drew from V7: the atlas pick, chapter 11's stepper, chapter 12's devices and the chart specimens. One row already needs the re-run. Row 40 says V7 names no weakest step for Loop B4, while today's V7 evidence summary names L54 for U.S. services. No earlier diagram appears in the guide as evidence for a V7 value.

### 1.6 The data palettes

Tokens in release 6.0.0-gate2.8 already cover part of this. Phase 3 adds what is missing under Master Brief section 10's five conditions for a new token, and you approve the new colors on board 1.

| Palette | Job | In the tokens today | Phase 3 adds | Proofs |
|---|---|---|---|---|
| Sequential | One measure from low to high | Verdigris in five steps on Newsprint and Charcoal (22 tokens) | A Prussian set, only if a chart needs a second measure in sequence | Contrast of each step and its label on Newsprint, White, Charcoal and Prussian where allowed; grayscale; three color-vision simulations |
| Diverging, pair B | Above and below a midpoint | Prussian through the page color to Verdigris on Newsprint, with a boxed arrow for direction (DR-54, Rule 01.3) | The Charcoal steps for dark mode (DR-204) | As above, and each cell read with its arrow in grayscale |
| Categorical | Up to four named groups | No set | Four inks (Charcoal, Prussian, Verdigris, Stone) with direct labels and patterns, where Verdigris and Stone never separate two groups alone (D2-95) | As above, and the set printed in black only |
| Magnitude | Size of a value with no direction | Stone steps on Newsprint and Charcoal (16 tokens) | None planned | As above |
| Grade line code | Evidence grade on connections | No tokens | The dash patterns of V7's renderer as tokens (Gate 1, M1) | Each pattern at 1x and 2x, in color and black |
| Red emphasis | The one working red per view (Rule 05.3) | `oa.chart.color.point` with its Charcoal keyline | A specimen where the chart's red meets a status red, with its resolution (tension 14) | The specimen at true size |

Party data stays in neutral inks with the party named on the mark (DR-48, DR-58, Rule 01.2), and no election graphic uses red and blue (DR-64).

## 2. Data

### 2.1 What answered from this container

I fetched each address from this container on November 11, 2026, between 16:53 and 16:58 UTC, with a browser user agent, and recorded the HTTP status. Each page got one request; the FEC and Congress APIs got two or three, and FRED one second try over an older protocol. The logs are `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2/phase3/reach-results.tsv`, `reach-results-2.tsv` and `reach-results-3.tsv` in the same folder.

| Host | What I fetched | Time (UTC) | Answer |
|---|---|---|---|
| census.gov | Home page | 16:53:15 | 200 |
| www2.census.gov | Current Population Survey table 4a, reported voting for states, November 2020 (`p20/585/table04a.xlsx`) | 16:53:17 | 200, a valid spreadsheet with that title |
| www2.census.gov | Congressional district boundary folder, TIGER 2024 | 16:53:47 | 200 |
| api.census.gov | One query of the American Community Survey with no key | 16:53:16 | Redirected to a "Missing Key" page, so the data API asks for a free key |
| fec.gov | Home page; election results page; the 2024 presidential results file | 16:53:17 to 16:53:47 | 200 each |
| api.open.fec.gov | Three queries with the shared demonstration key | 16:53:17, 16:53:30, 16:54:45 | 429, then 200, then 429. The error names a limit of 40 calls an hour on the demonstration key and 1,000 on a free personal key |
| api.congress.gov | Home page; two bill queries with the demonstration key | 16:53:18, 16:53:31 | 200 each, with a bill record returned |
| data.gov | Home page; catalog.data.gov | 16:53:19, 16:53:44 | 200 each |
| catalog.data.gov | Its search API (`/api/3/action/package_search`) | 16:53:20 | 404 at that path and at `/api/action`, so the studio finds datasets on the catalog's pages and fetches each from its publisher |
| api.fiscaldata.treasury.gov | Monthly Treasury Statement, one row | 16:53:49 | 200 |
| govinfo.gov | Home page; `How Our Laws Are Made` | 16:53:47, 16:58:16 | 200 each |
| clerk.house.gov, house.gov | Home page; the legislative process page | 16:53:47, 16:58:19 | 200 each |
| senate.gov | Home page | 16:53:48 | 200 |
| archives.gov, uscourts.gov, regulations.gov | Article V page; court structure page; home page | 16:58:17 to 16:58:18 | 200 each |
| ballotpedia.org, law.cornell.edu | Main page; Article V | 16:53:50, 16:58:20 | 200 each, both secondary |
| sos.mo.gov | Home page only | 16:53:50 | 200; DR-222 records a 403 from its own checks on result pages |
| bls.gov, cbo.gov, ncsl.org, csg.org | Home pages | 16:53:48 to 16:58:19 | 403 each |
| congress.gov, constitution.congress.gov | Home pages | 16:53:47, 16:58:19 | 403 each |
| fred.stlouisfed.org | Home page; the payrolls CSV | 16:53:48, 16:53:59 | The connection closed with no answer, twice; the proxy logged no refusal. FRED answered on November 6 (D2-120) |
| federalregister.gov | The rulemaking guide | 16:58:17 | Sent to a bot check page |

DR-222's four hosts all answer. Two of their APIs need a free key for steady use: the Census Bureau's data API and the FEC's. The bulk files on www2.census.gov and fec.gov need no key, so Phase 3 can start on them (question 2).

### 2.2 Sources and the specimens they serve

| Source | Answers from here | Specimens it serves (from the coverage plan) |
|---|---|---|
| Atlas V7 (`work/extract/atlas-v7-data.json`) | In the repository | Ranked bar, unit chart, timeline, evidence mix, scenario directions and comparison matrix, lollipop of claims, small-multiple bars, stacked column and bubble timeline of the repair log, implementation timeline, status chips, indicator row, by-the-numbers panel, adjacency matrix, heat table of reforms by route, lookup table of issues, evidence table, comparison grid, decision tree, who-decides diagram, and every chapter 15 example |
| Census Bureau, Current Population Survey voting tables | Yes, as files | Bar with a benchmark tick, dumbbell, grouped bar, range bar with margins of error, funnel, bubble map, scatter of turnout against registration deadlines |
| Census Bureau, poverty, housing and population tables, and boundary files | Yes, as files; the data API needs a key | Column and line of child poverty, confidence band, icon array, choropleth by state, county choropleth, homeownership slope and multi-line, population pyramid, dot density, district map, locator map |
| Federal Election Commission results and filings | Yes, as files; the API needs a key for steady use | Shift arrows, tile map of shifts, results table, dot plot, beeswarm, stacked share bar, change lollipop, histogram, box plot and line histogram of House margins, network of committee transfers |
| Clerk of the House | Yes | Parliament chart, House seat advantage over time, committee org chart, district tile map from 2024 results, roll-call grid only with the Senate's record beside it (D2-104) |
| api.congress.gov | Yes, with the demonstration key | Arc diagram of shared sponsors, step tracker and tracker list of real federal bills, the federal process diagram |
| Treasury, Fiscal Data | Yes | Treemap, stacked area and proportional symbols of outlays, Sankey through one Treasury node, hierarchy tree of budget functions, a public budget's waterfall |
| FRED copies of Bureau of Labor Statistics series (DR-60) | Not today; the November 6 payroll files are in the repository | Columns with a moving average, sector sparklines, diverging bar of jobs by sector, indexed line, line with a data gap, connected scatter, area chart |
| Congressional Budget Office | Refused | Fan chart of projections: a CSV you download (DR-60) or Illustrative data |
| Ballotpedia, labeled secondary (D2-99) | Yes | Tile map of states that prohibit ranked-choice voting, Venn and Euler diagrams of two state lists, ballot measure facts where a state's own page refuses |

### 2.3 The vintage and period rule

1. Each outside dataset comes from its publisher's own file or API, saved with a sidecar that names the publisher, table or series ID, URL, observation period, geography, vintage or release date, date retrieved, the qualification a reader needs and the printed source line.
2. The research lead fetches a round's data before its makers start and freezes it for that round. A newer release waits for one refresh at Phase 5's assembly, on a date the report states.
3. A chart prints its observation period in the measure line, and its vintage when the publisher revises figures, such as preliminary jobs months or the Census Bureau's revised poverty years.
4. Charts shown together share one time window, printed with its reason, and no chart splits a period at an inauguration date (DR-64, H09).
5. A chart ranks or singles out survey estimates only where the gap passes the margin of error, and says so (DR-64).
6. A chart of state election results draws the national figure, set apart and labeled (DR-64). Election specimens use official 2020 and 2024 results until 2026 results are certified; Missouri's 2026 count waits for Phase 5 (D2-1696).
7. Atlas values print V7's snapshot date, October 15, 2026, wherever a status, route or count could have changed since.

### 2.4 What stays labeled Illustrative

| Item | Label | Rule |
|---|---|---|
| Invented bills, state and federal, numbered from H.99001 and S.99002 | Illustrative, beside each bill, or once at the head when the whole piece is invented | DR-151, DR-97, H03 |
| Invented people, places, quotes and ballots, such as the ranked ballot in the annotated illustration | Illustrative, beside the item | H03 |
| A household budget waterfall and the benefit-cliff line's family | "Illustrative data", beside the chart | DR-46 |
| A bullet graph with no numeric target set in law | "Illustrative data", beside the chart | Coverage plan, section 3.9 |
| Any specimen whose data cannot be read from a primary source or a labeled secondary one | "Illustrative data", beside the chart | DR-46 |

Atlas V7 values and primary public data carry their source lines and need no label.

## 3. Page weight (DR-227)

**Where the page stands.** The frozen chapters page weighs 8,965,291 bytes (8.97 MB, where 1 MB is 1,000,000 bytes, as `guide_build.py` counts). The engineer fetched the fonts at 329,896 bytes, which come to 439,872 bytes as embedded data, so the Gate 2 preview lands near 9.4 MB by my count; the engineer's measured figure replaces mine. The page budget stays 15.5 MB, half a megabyte under the 16 MB limit. The engineer's November 10 projection put the whole guide near 14.6 MB with every unbuilt chapter at the build's 0.45 MB default and no fonts (D2-1214). The fonts add 0.44 MB, and 127 forms cannot fit in 0.45 MB, so the allocation below sets every part.

**Allocation through Phase 5.** I propose these ceilings so the page budget holds with all 28 chapters in it:

| Part | Today | Allocation |
|---|---|---|
| The 16 built chapters | 8.26 MB | 8.45 MB, with room for Gate 2's fix pass and the cross-references Phase 3 adds |
| Identity proofs | 0.14 MB | 0.20 MB |
| Head, shell and closing script | 0.18 MB | 0.20 MB |
| Navigation, colophon and its tokens.css download | 0.15 MB | 0.20 MB |
| Symbol sprites | 0.21 MB | 0.35 MB |
| Front matter and part openers, with "Where to start" | 0.02 MB | 0.10 MB |
| Embedded fonts with their three license texts | none | 0.46 MB |
| **Subtotal** | **8.97 MB** | **9.96 MB** |
| Chapter 13 | | 0.25 MB |
| Chapter 14, a hard stop | | 1.75 MB |
| Chapter 15 | | 0.60 MB |
| Phase 4's seven chapters (16, 20 to 25) | | 2.54 MB |
| Phase 5's two chapters (27, 28) | | 0.40 MB |
| **Page** | | **15.50 MB** |

Phase 4's share averages 0.36 MB a chapter, under the build's 0.45 MB default. Every byte Phase 3 leaves unspent goes to Phase 4, whose proposal sets its own ceilings at Gate 3.

**Chapter 14's ceiling, by part.** The ceiling is set by what 127 forms need when each byte is spent once:

| Part | Count | About each | Total |
|---|---|---|---|
| Core and extended specimens: words, table equivalent and data | 97 | 8 KB | 0.78 MB |
| Reference sketches | 22 | 4 KB | 0.09 MB |
| Avoid entries | 8 | 2 KB | 0.02 MB |
| The chapter's rules with correct and failure plates, the selection guide and the palette specification | | | 0.30 MB |
| The three complex examples' controls and still frames | 3 | 30 KB | 0.09 MB |
| One shared chart renderer | 1 | | 0.22 MB |
| Shared map geometry: states once, one state's districts, counties simplified | | | 0.25 MB |
| **Chapter 14** | | | **1.75 MB** |

**Why the drawing method decides it.** The Phase 2 stretch page holds six specimens in 2.32 MB, drawn as full inline SVG at desktop, phone and dark sizes; the Explainer page holds ten specimens in five views in 1.51 MB. At the stretch page's rate, 97 finished specimens would weigh about 37 MB. DR-227 leaves the method to the engineer, who measures each candidate on the 16 rebuilt specimens in round 0 and picks the lightest that passes every check:

| Method | How it works | Chapter 14, my estimate | What it costs |
|---|---|---|---|
| Inline SVG as Phase 2 drew it | Every desktop and phone drawing written out in full | 12 MB or more | Fails the ceiling |
| Lean inline SVG | Coordinates rounded to the artboard's half pixel, classes in place of repeated attributes, shared definitions once per page, repeated marks by `<use>`, one drawing per specimen with a phone drawing only where the form changes (DR-64) | 2.5 to 3.5 MB | Passes only if extended forms drop their phone drawings |
| Drawn when the page loads | The page carries each specimen's words and table; the kit's one script reads the table and draws the SVG, the same script that makes the exports and still images | 1.5 to 1.75 MB | Charts need script to appear, while words and tables stay readable without it; the checks read the drawn page; print waits for the drawing |
| Image sheets for sketches | Reference and avoid sketches as one 16-color PNG sheet at twice size, as chapter 10's contact sheets are | Saves about 0.05 MB | Only for small sketches |

**How the check enforces it.**
1. `guide_build.py` stops with an error whenever chapter 14 passes 1.75 MB, in every mode, so no maker's build gets through over it.
2. Chapters 13 and 15 take ceilings as warnings, which `--strict` turns into failures, as for the other chapters.
3. The build report lists every chapter 14 specimen's bytes with its form, tier and round, and the spend of the shared renderer and geometry, so each round sees its share.
4. A projection test adds today's bytes to the allocation of every chapter not yet built and fails `--strict` above 15.5 MB.
5. The fonts become a part of their own, checked against the font manifest's bytes.
6. The build's self-test plants chapter 14 one byte over its ceiling, a specimen far over its form's average, and a projection over the budget, and must catch all three.

## 4. Three boards before Gate 3 (DR-228)

| Board | After | What it shows | What you decide | Scores on it |
|---|---|---|---|---|
| 1 | Round 0 | The chart kit: S01 to S16 rebuilt from their data by one command, at 1440 and 390 px, on Newsprint and Charcoal, each with its grayscale proof, its exports and its bytes. The palette proofs of section 1.6. The drawing method the engineer chose, and chapter 14's projected weight against 1.75 MB. Chapter 13 as built in the guide | The new palette colors; chapter 13; question 4, only if the projection runs over | The creative director's scores for the kit and chapter 13; the six red team scores |
| 2 | Rounds 1 to 3 | 114 forms at true size, grouped by family under their reader questions, each with its phone drawing, grayscale proof, table and source line. The balance read, the example log counted under Rule 01.9, chapter 14's spend so far, the V7.1 items found and the new research ledger rows | Any form whose tier or data changed during the rounds; any V7.1 item; notes that go into round 4 | The creative director's scores by family and for every core form; the red team scores |
| 3 | Rounds 4 and 5, with chapter 15 | Round 4's 13 forms and the social formats; the selection guide; the written palette specification; the three complex examples with interaction and exports; chapter 15 whole, with its six worked examples, 11 workflows with sources and dates, and the reconciliation table; a drift read of chapters 13 to 15 against the built chapters | The worked examples and workflows as drawn; the new tracker step sets if you said yes to question 3; anything that goes to Gate 3 | The creative director's scores for chapters 13, 14 and 15; the red team scores |

Each board is one private page in plain words, with decision codes only in a small reference line under each panel, as the Gate 2 board has them. Notes you send on a board join the next round.

## 5. Team and rounds

| Role | Agent | Phase 3 work |
|---|---|---|
| Coordinator | Main session | Briefs, shared data, kit integration, the decision log, merges, boards and the Gate 3 report |
| Data visualization and systems lead | `oa-dataviz-systems-lead` | Selection guide; palettes with the design director; the evidence rules each chart carries; the systems grammar; the six worked examples; the reconciliation table; mapping workflows to V7's routes. Signs off every chart, table, map and diagram |
| Research lead | `oa-research-lead` | Each round's data one round ahead, with sidecars and research ledger rows; workflow facts from official sources with dates; the lessons of Our World in Data, LOOPY and En-ROADS; rights rows for geometry and data |
| Engineer | `oa-engineer` | The chart kit and the drawing-method pilot in round 0; weight checks; exports; the V7 and source checks; guide builds and full checks |
| Chart makers | General-purpose agents briefed as specialists, as in Phase 2 (D2-91, D2-121) | Round 0, the Explainer maker, a senior newspaper graphics editor, with the engineer; rounds 1 to 3, two makers a round, a cartographer in round 3; round 4, an infographics maker with the design director |
| Systems designer | Briefed as chapters 11 and 12's systems designer | Chapter 15's diagrams, worked examples and workflow drawings from round 1; chapter 11's new tracker plates if you say yes to question 3 |
| Design director | `oa-design-director` | Palettes with the data lead; reviews every visual before it ships; round 4's infographics |
| Accessibility lead | `oa-ux-accessibility-lead` | Interaction for the complex examples, loop playback with pause, reset and a still sequence, and the configurable tracker; the accessibility lens on every red team |
| Editor | `oa-editor` | Chapter 13's words; every reading guide, caption, title and source line in chapters 14 and 15 |
| Creative director | `oa-creative-director` | A first pass beside each red team, scores at each board, and the final rubric at Gate 3 |

**How a round runs.** The makers build on the kit. Six red team lenses then read the round side by side, one reviewer per lens across all its forms, with the creative director's first pass beside them (D2-76, D2-123): statistics; civic education; accessibility; nonpartisanship and brand, reading every title from the left and the right under DR-93 and DR-124; craft at twice size; and production, where a simulated designer makes a new chart from the chapter and the kit alone, as DR-219 tested the components. A simulated reader panel reads each board's charts and is reported as simulated, since no real readers test before launch (DR-202). One fix pass follows, then DR-191's short second pass and the creative director's scores. An item ships at 4 or more on all six criteria.

**What runs at once.**

| Step | Work | Runs beside it |
|---|---|---|
| Round 0 | The kit and method pilot; palettes and proofs; chapter 13 | The research lead fetches rounds 1 and 2's data, gathers workflow sources and writes up the three references' lessons |
| Board 1 | You decide | Round 1's makers start on the kit |
| Rounds 1 to 3 | Two makers a round | Chapter 15 starts in round 1; the research lead stays a round ahead; the reconciliation re-run happens in round 2; each round's review overlaps the next round's start |
| Board 2 | You decide | Round 4 starts |
| Rounds 4 and 5 | Infographics and proportion; the selection guide and the complex examples | Chapter 15 finishes; a drift reader reads chapters 13 to 15 against 01, 02, 05, 11, 12 and 18 |
| Board 3, then Gate 3 | You decide; the creative director's final rubric | The Gate 3 report and the Phase 4 proposal |

The main session hands off to a new chat after each board, as the last handoff advises.

## 6. Risks and answers

| Risk | What would happen | Answer |
|---|---|---|
| Chapter 14 runs over 1.75 MB | The page passes 15.5 MB, or Phase 4 is squeezed | A build error at the ceiling; the round 0 pilot on real charts; the engineer's choice of method; the trade order in question 4 |
| The Census and FEC data APIs need free keys for steady use | Slow or blocked downloads | Bulk files from www2.census.gov and fec.gov need no key; free keys (question 2) |
| bls.gov, cbo.gov, ncsl.org, csg.org and congress.gov refuse automated readers, and FRED closed the connection today | Some economy charts, the fan chart and some workflow facts lack a fresh primary download | FRED copies from November 6 stay in the repository (DR-60); a short list of files for you to download (question 2); govinfo.gov, house.gov, clerk.house.gov, archives.gov and uscourts.gov answer for workflow facts; a labeled secondary source where a primary refuses, as D2-99 did |
| About 38 of the plan's 97 core and extended forms name election or voting data (a keyword count of its specimen column) | Chapter 14 breaks Rule 01.9, no more than one example in four from one atlas domain | Re-pick specimen data, keeping every form and tier (question 1) |
| V7's snapshot is October 15, 2026, and events have moved since, such as R-01's two ballot measures | A worked example reads as current after events have moved on | V7's date beside every status and route; outcomes in the research ledger; a V7.1 item; no edit to V7 |
| A rule in chapters 01, 02, 05, 11 or 12 restated in 13 to 15 | One rule stated two ways | Chapters 13 to 15 cite rules by number; the drift red team's scripted checks of names and cross-references run on them each round |
| The Phase 2 chart data still marks the editor's disclosure as required text on four datasets (D2-106) | A rebuilt chart carries a line DR-100 retired | The kit's data drops it, and the check fails any copy of it |
| The coverage plan quotes DR-55's balance clause | Makers follow wording you replaced | Titles and sets follow DR-124's wording |
| V5 Polished, the Atlas Visual System and Concepts V2 are not in this container | The reconciliation cannot re-read them | Phase 0's committed extraction holds every value compared; you are asked for a file only if one row needs it |
| Review of 127 forms | Reviewers skim | Scripts own every measurable check; reviewers read by family at twice size; the creative director scores every core form |
| Data revised during the phase | A chart disagrees with a newer figure | The vintage rule freezes each round's data and refreshes once at Phase 5 |
| A drawing in the guide and its export drift apart | An export disagrees with the page | One kit script draws the page, the exports and the boards; the export check compares the CSV with the data file |
| The full guide check slows as the page grows | Rounds wait on it | The quick check (1440 and 390 px) each round; all four widths at each board, in the background |
| Findings fall more on one side (DR-93) | A finding gets softened, or a counterweight invented | Report the record as it stands; read each title from both sides; no finding added or dropped to even the score (DR-124) |

## 7. How each Phase 3 check runs

The first five rows are the Phase 3 prompt's checks; the rest come from Master Brief section 22 and the rules already settled.

| Check | How it runs | Passes when | When |
|---|---|---|---|
| Every Atlas V7 ID, sign, type, delay, grade, effect code and route in the chapters matches the JSON | A script, grown from `atlas_concepts_verify.py` and `dataviz_verify.py`, reads every typed chip and data attribute in chapters 13 to 15 and the kit's data files and compares each with `work/extract/atlas-v7-data.json`. It also fails an authority link given a sign or a loop, an effect total or tally, an undated route shown as checked, a bare ID, and a qualifier dropped from an effect | 0 mismatches, and its self-test catches one planted fault of each kind | Every build |
| Source, series, period and qualification for every statistic outside the atlas, or the "Illustrative data" label beside the chart | Each specimen with outside data must have a sidecar; the check compares the printed source line with the sidecar's, in H04's order, and each number in a title or note with the data. A specimen with no sidecar must print the label inside its figure. The research lead adds a ledger row with URL and date checked; the statistics lens rebuilds a sample from the raw files | Every specimen passes, and every sidecar has its ledger row | Every build; the sample each round |
| Grayscale screenshots of every specimen | Playwright captures each specimen at 1440 and 390 px through a grayscale filter, saved as PNG beside the board. A measured test also requires that each key's groups differ in lightness by a set margin, or carry a pattern or a direct label | Every key passes, and the data lead and the creative director look at every capture | Each board |
| The three complex examples: desktop, 390 px, keyboard and screen reader order, interaction, and each export opened | Captures at 1440 and 390 px; a scripted Tab walk that records each stop's accessible name and focus ring; the accessibility tree's outline for reading order; scripted step, pause, reset and still sequence, reform choice and the Chart and Table switch; each download clicked, saved and opened: SVG parsed and rendered, PNG checked for size and drawn pixels, CSV parsed and compared row for row with the data file | Every stop named and visible, every control works, every export opens and matches | Round 5 and board 3 |
| A text or table equivalent for every specimen | The build fails a specimen with no table or text equivalent, or with a table whose rows differ from its data file; the guide check confirms keyboard reach | Every specimen | Every build |
| The guide check | `guide_check.js` at 1440, 1024, 390 and 360 px: headings, anchors, text size, contrast, Rule 05.3, writing and codes, axe-core, focus | 0 failures | Quick each round; full at each board |
| The chart rendered check | `dataviz_check.js`: bars on their zero line, points on one scale, sized circles by area (D2-124), marks inside their drawing, no party mark in red or Prussian | 0 failures | Every build |
| The rules of DR-64 | National row on state results; survey rankings only past the margin of error; one window with its reason; no split at an inauguration; no red and blue on election graphics | 0 failures | Every build |
| Rule 01.9's spread | A script counts the example log (Rule 01.12) by atlas domain and state, per chapter | No domain over one in four, no state over one in five | Each round |
| Page weight | The checks of section 3 | Chapter 14 under 1.75 MB; projection under 15.5 MB | Every build |
| Dark mode, long labels, 200 percent text, 320 px reflow, reduced motion, forced colors, print | Playwright emulation on the interactive specimens and each family's first specimen | No lost content and every frame readable | Each board |
| Real screen readers and devices | DR-213's four device scripts | Not run in this container | Listed as not tested at Gate 3 |

## 8. Settled inputs and carried items

**Settled, and used as given.** The atlas visual system (DR-36); data from Atlas V7 and primary public sources (DR-46); the chart system, Newsprint, pair B and the rules of the data round (DR-52 to DR-61); the 127 forms and the build order (DR-62, DR-63); the stretch test's rules (DR-64); one standard of evidence (DR-93) with DR-124's wording; labels (DR-97); S01's fix to name H.R. 7008, the Stop Insider Trading Act (DR-98); no disclosure (DR-100); invented bills (DR-151); no reader tests before launch (DR-202); one dark mode on Charcoal (DR-204); R-01 and R-02 as examples like every other reform (DR-223); public data downloads (DR-222); version 8 at one link (DR-225); one guide file and chapter 14's ceiling (DR-227); three boards (DR-228); Gate 1's M1 to M4 for the evidence line code, grade words, chips and marks. Chapter 02's writing rules govern every word.

**Carried into Phase 3 from Phase 2.** The asset package's copy of the print L3 files takes its final title (D2-1330), and the dark-card feed test script ships with the package (Rule 08.2). Any notes you send on the preview after Gate 2's fix pass join board 1.

## 9. You decide at Gate 3

- Chapters 13, 14 and 15 as built, with the creative director's scores.
- The chart kit as an asset of the package.
- The reconciliation table's resolutions, and any new V7.1 items.
- Any token release that adds chart tokens.
- The Phase 4 proposal, with its chapter ceilings set from what Phase 3 spent.

## 10. Questions for Dustin

1. **Chapter 14's examples and Rule 01.9.** About 38 of the plan's 97 core and extended forms name election or voting data, while Rule 01.9 allows no more than one example in four from one atlas domain in a chapter. Both were approved. *Recommendation:* keep every form and tier, and let the studio re-pick specimen data from other domains (taxes and budgets, work and pay, housing, Congress and agencies) until the count holds, keeping election data for the forms built for elections, such as shift arrows, results tables and election maps. The log on board 2 shows the count.
2. **Data access.** The Census Bureau's data API asks for a free key, the FEC's shared demonstration key allows 40 calls an hour, and bls.gov, cbo.gov and ncsl.org refuse automated readers. *Recommendation:* sign up for a free api.data.gov key (it serves the FEC and Congress APIs) and a free Census Bureau key, and enter them only in the environment's credential form when Phase 3 starts. Also agree to download up to five files the studio lists with links at round 1, such as the Congressional Budget Office projections for the fan chart. Without either, the studio uses bulk files and labels as Illustrative any chart it cannot source.
3. **Trackers for ballot measures and court cases.** DR-140 kept these for a later stage. Chapter 15's workflows set their steps in Phase 3. *Recommendation:* add both to chapter 11 in Phase 3 as six-step trackers under the rules of DR-108 and DR-150, drawn by the systems designer and shown on board 3, so Phase 4's applications find them ready.
4. **If chapter 14 cannot fit.** This applies only if the round 0 pilot projects chapter 14 over 1.75 MB with the lightest method. *Recommendation:* the studio first draws the reference and avoid sketches as one image sheet, then drops the separate phone drawing from extended forms whose form does not change. Only if both fall short would you be asked on board 1 to move bytes from Phase 4's share.

## Tested and not tested

**Tested, for this draft**
- Every Atlas V7 value in sections 1.3 and 1.4, read by script from `work/extract/atlas-v7-data.json`, which matches the committed model byte for byte: the six examples' loops, connections, signs, types, grades, delays and closures; R-01's targets, loops, band, effects, confidence, evidence grades and routes; the seven authority connections; the 11 route codes; 126 route entries with 13 dated; 38 of 200 effect values with qualifiers; and the reforms acting on Loops R8 and R10.
- The reachability of every host in section 2.1, with each request's time and status logged; the census table opened as a valid spreadsheet, the FEC and Congress APIs returned records.
- The page's weight by part, from the committed build report and a script on the frozen page; the font bytes, fetched and measured the same way the engineer's notes report them (329,896 bytes).
- The coverage plan's 127 forms, by family and tier, counted by script from its tables, and the family missing from its build order.
- A keyword count of the plan's specimen column for election and voting data (about 38 of 97). It is a rough count, and the round 0 log replaces it.

**Not tested**
- The drawing methods' weights in section 3 are my estimates from the Phase 2 pages; the round 0 pilot measures them.
- The workflow stages in section 1.4 come from Master Brief section 14 and V7's route text. The research lead verifies each against official sources in Phase 3.
- I fetched home pages and single files only. Whether each specimen's exact table answers is checked when the research lead fetches it.
- The coverage board, read by script for its text only; I did not view it.
- The Gate 2 preview's measured weight, which the engineer reports.

## Routine calls

D2-xxx | Proportion and overlap, the one family the coverage plan's build order leaves out, joins round 4 with the infographics | Its icon arrays draw on Civic Line as the infographics do (DR-61), and round 4 carries the lightest load
D2-xxx | Round 0 rebuilds S01 to S16 in the kit as its test set and weight pilot | They are the only finished specimens, so the kit and the method are proven on real charts before round 1, and the floor of twenty is passed early in round 1
D2-xxx | Worked example 1 uses chapter 11's live stepper for Loop R1 | DR-195 already runs it there; one drawing of one loop keeps the chapters in step and saves bytes
D2-xxx | Worked example 6 is Loop B2, with Loops B3 and R9 named beside it | B2 is graded well supported yet has no numbered chain, which teaches that closure and grade are separate; R9 would stack a hypothesis on top
D2-xxx | The three complex examples, recommended: S14 (work and pay), Loops B4 and R10 (elections), the three reforms acting on Loop R8 (housing) | One per domain under Rule 01.9, each with data its exports can carry
D2-xxx | The kit's data drops the editor's disclosure, and the chart check fails any copy of it | DR-100 retired it; `dataviz_shared_data.py` still marks it required text on four datasets (D2-106)
D2-xxx | Chart titles and sets follow DR-124's wording wherever the coverage plan quotes DR-55's balance clause | DR-124 replaced that clause on November 7
D2-xxx | The district tile map uses the Clerk of the House's 2024 results until 2026 results are certified | The plan's "once certified" would leave the specimen without data in Phase 3
D2-xxx | The worked examples print V7's snapshot date beside R-01's status and routes | Its status text names two ballot measures that went to voters on November 3, 2026, after the snapshot, and the studio never edits V7

## Change log

- Created: `work/handoffs/phase-2/20261111_Phase-3-Proposal-Draft.md` (this file).
- Scratch only, outside the repository: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2/phase3/` holds the reachability logs (`reach-results.tsv`, `reach-results-2.tsv`, `reach-results-3.tsv`), the fetch script, the downloads it made (`dl1/`, `fonts/`), the coverage board's extracted text and the plan's rows as JSON.
- Modified: none.
