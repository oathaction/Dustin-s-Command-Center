# Who Do They Answer To? Atlas V7: editorial and QA report

October 15, 2026. Prepared for Dustin Cathcart, editor, Oath & Action.

## 1. What you have

| File | What it is |
|---|---|
| `20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html` | The finished Atlas. One self-contained file (3.1 MB) that opens offline in a browser. |
| `20261015_Atlas-V7-Editorial-And-QA-Report.md` | This report. |
| `20261015_Atlas-V7-Content-Coverage-Manifest.csv` | Every V4 and V6 section, table and control, with its V7 destination or maintenance file. |
| `maintenance/20261015_Atlas-V7-Topic-Taxonomy.md` | Topics, everyday questions, issue areas, reform groups, layers, routes and registers. |
| `maintenance/20261015_Atlas-V7-Identifier-Migration-Map.csv` | How old anchors, V6 view links and changed identifiers resolve in V7. |
| `maintenance/data/` | The canonical V7 dataset and every private build record: earlier wording, grade changes, register cleanup, withheld sources, correction logs. |
| `maintenance/earlier-content/` | The complete V6 dataset and the narrator, disclosure and story material taken out of the public product. |
| `maintenance/research/` | The 16 pathway research files, rewritten copy, citation repair and time-sensitive verification logs. |
| `maintenance/verification/` | Both independent reviews and the final test results. |
| `maintenance/build/` | Build and test scripts and the application source. |
| `_archive/` | The V6 HTML as supplied, the V6 changes and review note, and a copy of the V4 HTML. |

## 2. Inputs and counts

The brief's counts match the V6 data. One model revision (section 5, TC4 and LT09) added a variable and a connection.

| Item | Brief | V6 | V7 |
|---|---|---|---|
| Variables | 50 | 50 | 51 (TC8 added) |
| Connections | 117 | 117 | 118 (LT19 added): 72 core, 27 economy, 19 technology |
| Feedback loops | 23 | 23 | 23 (20 run through numbered connections, 3 are conceptual) |
| Issue records | 194 | 194 | 194 (193 active, 1 retired) |
| Reform profiles | 50 | 50 | 50 (49 options and 1 rejected option, R-35) |
| Sources | 740 | 740 | 1,140 identifiers naming 1,099 distinct documents |
| Everyday questions | at least 12 | none | 16 pathways in 5 topics |
| Pathway claims | not set | none | 433 |

All 740 V6 source identifiers still resolve. Pathway research added 308 entries, the citation repair and status checks added 92, and 41 identifiers are now marked as the same document as another entry. Every count shown in the interface comes from the data at load time.

## 3. Information architecture

The main navigation has five sections plus Search: Topics, How it works, Issue records, Reforms and Evidence. Each topic hub follows the order the brief set: everyday question, short answer, mechanisms, narrower questions, then records and evidence.

| Topic | Everyday questions |
|---|---|
| Cost of living | PW01 Why did my rent go up? · PW02 Why is my grocery bill higher? · PW03 Why is my electric bill going up? · PW04 Why did my home insurance premium go up? |
| Health and care | PW05 Why is it hard to find an appointment? · PW06 Why can the same care produce different bills? · PW07 Why does childcare cost so much, and why can't I find an opening? · PW08 Why is it so hard to get help at home as I age or live with a disability? |
| Work and financial security | PW09 Why isn't my pay keeping up with what my work produces? · PW10 How do taxes and benefit rules change what my household keeps? · PW11 What will I get from Social Security, and could the rules change before I retire? |
| Public services where you live | PW12 Who makes sure my tap water is safe? · PW13 Why is the repair on my street taking so long? · PW14 Why does my child's school have less than schools in other districts? |
| Voice, power and information | PW15 Which election decides who represents me, and how can I influence the people who decide? · PW16 How do algorithms affect the prices I pay, my job, what I see online and the services I get? |

Each pathway carries a short answer led by one sentence, mechanisms with the detail on request, narrower questions that open in place, the offices that can change the rule (with the offices that apply it listed below), responses with requirements, evidence and tradeoffs, who is affected differently, how to judge results, what a reader can do, a comprehension check and every claim with its sources. Across the 16 pathways that is 94 mechanisms, 109 narrower questions, 134 decision makers and 83 responses.

Breadcrumbs show where a reader is, the Return link goes back to the exact item they left, and browser Back restores scroll position, open disclosures and table filters. Experts reach every record through the registers page (`#/registers`): variables, connections, loops, issue records, reform profiles, route feasibility, likely effects, rules that changed, history events, claims and sources. Each register filters, sorts, narrows columns and downloads as CSV with every field.

## 4. Evidence

Every pathway claim states the claim, what the evidence supports, a confidence label, the population, jurisdiction and period, the main limitation and its sources by title and publisher. Labels in the 433 claims: 321 documented, 56 well supported, 38 plausible and 18 contested.

The label definitions were rewritten. "Well supported" now covers a well-designed study such as a randomized experiment, several consistent studies, or an official estimate made with a published method, with no credible study finding the opposite. "Mixed" is defined for evidence that points different ways for different parts of a claim. Six claims moved down to plausible because their design does not meet the bar (CL1106, CL1125, CL1425, CL1700, CL1701, CL1715). Three pathway responses moved down (PW01 allowing homes by right, PW05 marketplace premium help, PW15 redistricting commissions). Five reform profiles were regraded to match the evidence they cite: R-01's problem evidence and the remedy evidence for R-04, R-05 and R-30 are now plausible, and R-23's is contested. Where a pathway response and its reform profile still carry different labels, the response shows the profile's label.

### Citation repair

The V6 review found legacy citations missing from the register in 40 issue records. Those records held 50 citation uses (48 distinct legacy identifiers), and each was matched to its claim individually.

| Outcome | Count |
|---|---|
| Claim corrected to match the source found | 22 |
| New source added to the register | 19 |
| Mapped to an existing register entry | 4 |
| Unresolved | 5 |

The five unresolved candidates (K1823, K1834, K1837, K1838, K1840) were never read, so they are withheld from the public register and kept in `maintenance/data`. The remedy notes that leaned on them were rewritten. I157 now cites Campbell's 2019 review, and I169 states that no evaluation of an access gain is cited and lists the shortage and supply sources it does use.

### Time-sensitive claims

147 time-sensitive statements were checked against current sources on October 15, 2026: 58 confirmed, 34 updated, 38 partly confirmed and 17 that could not be verified. Statements that could not be verified were rewritten to state a dated limit, or removed. Ten reform status lines that could not be rechecked no longer show a check date. Research produced 114 source records: 92 became new register entries and 22 matched documents already in the register.

### Register cleanup

38 entries that point to the same document as another entry are now marked as the same document, on top of 3 marked before. Every old identifier still resolves, and the sources download lists each document's other identifiers. Publishers were filled for 85 entries from their web domain. 35 entries were retyped: 18 law-firm client alerts as "law firm summary," 7 NCSL and NAIC entries as "association of state officials," 9 Wikipedia entries as "encyclopedia (secondary)," and one bill tracker. Access logs and research tasks in source notes moved to maintenance.

## 5. Integrity tests

| Test | Result |
|---|---|
| B2 to B5 name both a variable and a loop | Passes. Links are typed by context ("loop B4" goes to the loop), both pages cross-reference each other, search returns both with labels, and four untyped mentions were fixed (loop B4 notes, R16 notes, the technology layer and About). |
| R16 closure, drawing and evidence | Passes. The loop page states that T01 is a hypothesis, that the chain closes only through it, and that the diagram draws it as a dotted line. Reform profiles now use the canonical title, which keeps "may." |
| R-35 never reads as a recommendation | Passes. One notice reads "This option is rejected on the evidence below and kept so the reasoning can be checked." The 87% Pew figure is consistent, the lobbyist mechanism is labelled inferred, and code confidence is medium. |
| TC4 and LT09 | Fixed by a model revision. LT09 carried a documented grade for an effect that comes from the amount of AI computing built, while its source variable measured concentration. New variable TC8 (Computing capacity built for AI) holds the amount built. LT09 runs TC8 to TC6 at its documented grade, and new connection LT19 (TC4 to TC8) records the concentration step as a hypothesis. PW03 now cites TC8. |
| X17 population | Fixed: "Pew estimated 14 million unauthorized immigrants in July 2023; about 9.7 million of them were working, 5.6% of the U.S. workforce." The stray disability tag was removed. |
| Indicator direction | Passes for all 51 variables, including the indicators that run opposite to their variable. |
| Inferred reforms | Issue records separate reforms aimed at a mechanism from profiles that only share a model target, with a note that sharing a target does not mean a profile would fix the problem. |
| Paraphrased identifiers | About 60 inline names in reform profiles, pathways, the outcomes page, the delivery log and the history now use each record's canonical title. Nine delivery-log cases mapped to loops whose mechanism did not match no longer name a loop. |
| Deep links | 19 legacy link formats from V4 and V6 tested; all resolve to the right page and type. |

## 6. Ballot neutrality and disclosure

The content review flagged text that cast the Alaska repeal measure as a "failure risk" and called the profiles "proposed reforms," 19 days before the November 3 election. The second verification round found three more places. Fixes:

- R-01 and R-08 describe the Alaska measure only in their status lines, as a pending vote.
- The MassINC horse-race poll was removed from R-01, along with its citation.
- R-08 no longer cites an advocacy piece on Ballot Measure 2.
- R-01, the PW15 Question 3 section and the Ballot Measure 2 section each state that the Atlas takes no position.
- The home page and profiles say "reform profiles."
- R-01 describes Massachusetts accurately: unenrolled voters already pick one party's ballot, and Question 3 would put every candidate on one primary ballot from 2028.
- PW15 and R-01 lead with Cook Political Report's count (398 of 435 House seats rated safe for 2026) before Unite America's advocacy count, which is labelled plausible and moved to the end of the evidence page's headline figures.
- Loop B4 no longer mentions Question 3.
- The disclosure on About, on R-01, R-02 and R-47, and in the PW15 Question 3 section now says that Oath & Action's editor works with the Yes on 3 campaign and promotes it through Veterans for All Voters, where he is Massachusetts state lead.

## 7. Writing

Public text follows your rules: no em dashes, no version or development history, no narrator, no "original wording" panels and no download of earlier versions. Codes always appear with their readable name. About 40 places where "the Atlas" acted as narrator now give the action to the record ("Rejected option: …", "rated low in feasibility"). Contrast constructions, repeated templates and landing sentences that the reviewers found were rewritten.

## 8. Design and accessibility

The design keeps the brand system: warm paper, condensed charcoal headlines, the red serif ampersand, Prussian navy for links and evidence meters, muted verdigris for households and authority lines, and the small grid motif.

Diagrams are exact SVG with measured text. Authority lines are teal and labelled "auth," separate from causal signs. Evidence strength is shown by dash pattern, separate from direction, and conceptual loops have their own grey dashed style and legend. Wide layouts are used only where they fit at full size, so text never renders below 90 percent. Zoom in, zoom out, Fit and Reset all work. On phones, each kind of line gets its own trunk so authority and causation never merge.

Phone tables read as labelled cards, with filters behind one control. Print opens every disclosure, prints diagrams as their text version and adds web addresses to source links.

## 9. Independent review and fixes

Two independent reviewers examined the built product. The interface review found 1 blocker, 8 major, 17 minor and 10 polish items. The content review found 1 blocker, 13 major, 14 minor and 6 polish items. A third reviewer then checked the fixes against both reviews and this report, and its findings were fixed in turn. The reviews are in `maintenance/verification`.

| Finding | Status |
|---|---|
| Diagram zoom in and Reset had no effect (blocker) | Fixed, with a regression test |
| Ballot-measure text implied a vote (blocker) | Fixed (section 6) |
| Paragraph splitter dropped text on About and D07 | Fixed with a lossless splitter that rebuilds and checks each paragraph |
| Tablet diagrams shrank labels to 9 px | Fixed: phone layout below 814 px, never below 90% |
| Search missed everyday wording | Fixed: stemming, synonyms, word-start matching, a partial-match fallback, a best match and fixed result groups. Common phrasings such as "rent went up," "rent increase," "daycare," "minimum wage," "gerrymandering," "ranked choice," "drug prices" and "potholes" now show the right everyday question as the best match. |
| Pathway pages overloaded | Reduced: pathways run 10.8 to 13.9 screens on desktop (was 13.0 to 18.1) and 15.9 to 21.0 on a phone (was 21.0 to 30.2). The reforms landing runs 4.7 phone screens (was 21.8). |
| Parallel mechanisms drawn as a causal chain | Fixed: numbered without arrows, with a note that numbers mark no causal order |
| Print dropped collapsed content | Fixed and tested by reading the printed PDF |
| Phone tables hard to read | Fixed: labelled cards |
| Filters and open disclosures lost on Back | Fixed: filters, sort, columns and open disclosures survive Back and Forward |
| Same facts stated differently (RealPage, Alaska margin, child tax credit, Optum Rx, PBM dates, Graham and Svolik, the Storch docket date) | Fixed everywhere they appeared |
| Process language visible to readers | Fixed in claim limits, source notes and titles, route notes, status lines, headline figures, the repair log, the methods page and the not-found page |
| Claims resting on unread sources | Fixed (section 4) |
| Medill 2026 count unverified | Replaced with Medill's 2025 count (213 counties, about 50 million people), read in Medill's own release |
| Confidence labels claimed too much | Fixed (section 4) |
| Seven issue records lacked a remedy label | Fixed |
| Time-sensitive status (Medicaid start date, SNAP tense, Harvard review size, FAIR Plan, Rural Health awards, Schedule Policy/Career, Missouri, Treasury rules) | Fixed or restated with its date |
| Expert registers incomplete | Added a claims register, a loops register and a registers index |
| Headings, menu focus, contents order, column menu, sort order, CSV exports, card summaries, empty diagram states, conceptual loop style, single-direction diagrams, small pills | Fixed |

## 10. Checks performed on the final build

| Check | Result |
|---|---|
| Route crawl at 320, 390, 640, 768, 1024 and 1440 px | 2,028 routes at each width: no script errors, no page overflow, no duplicate IDs, 860 section links all land |
| Diagram geometry at 320, 390, 768, 1024 and 1440 px | 182 diagrams at each width: no text outside boxes, no collisions, no content outside the canvas, unique marker IDs. Smallest rendered diagram text: 12 px at 390, 1024 and 1440; 11.4 px at 320; 10.8 px at 768 (loops at 90%) |
| Zoom controls | Zoom in enlarges and scrolls, Reset returns to 100%, Fit fits, at every width |
| Interactions | 76 of 76 pass: navigation, Return, Back and Forward, disclosures, checks, search, tables, CSV, diagrams, legacy links, keyboard, phone menu, phone tables, print |
| Accessibility (axe-core 4.10, WCAG 2.2 AA plus best practice) | 86 page audits (43 routes at 1280 and 390 px): 0 violations |
| 200% zoom simulation (640 by 450 at double density) | 8 routes: no overflow and no nested scroll boxes |
| Public text scan | No dashes, version words, filler or not-but patterns. Remaining hits for "verify" describe what agencies verify, not research steps. |

## 11. What remains open

Close items 1 through 3 before anything is published.

1. **Graham and Svolik (2020).** The Atlas states one wording everywhere: about 3.5% of respondents defected in realistic matchups, and the average penalty across all matchups was 11.7 points. The article's results section sits behind a paywall and was not read in this session.
2. **Surface transportation.** Authorization ran through September 30, 2026. The sources cited show the House committee bill from May 2026 and no later action, and PW13 says so. Confirm the current status on Congress.gov.
3. **Rural Health Transformation.** PW05 states the statute's December 31, 2025 deadline for CMS decisions and the October 2026 state announcements. The date CMS announced first-year awards was not confirmed.
4. **Web research budget.** The session's web search budget ran out during the QA pass, and direct page fetches to several publishers failed, so the items above and below could not be re-read today.
5. **Other dated status lines.** Head Start's pay rule (proposed May 2026), the Schedule Policy/Career lawsuits (latest check: a CRS review of March 26, 2026), Storch v. Hegseth (latest docket entry July 20, 2026), the Census Bureau's revised poverty series and ten reform status lines without a recent check each state their own date and were not rechecked.
6. **PW13 is the thinnest pathway** (13 claims). It explains funding structure well and says little about local causes of delay such as crews, contractors, utility coordination and permits. The December 2020 transit relief law is noted as uncounted.
7. **Weaker source choices.** CL1600 cites a CRS cyber report for water system sizes, CL1606 cites secondary pages for a court argument date, CL1621 cites the receiver's website for a court order, CL1312 cites CBO through a Georgetown summary, and CL1408 relies on an advocacy tracker. Nine Wikipedia entries remain, labelled as secondary.
8. **Unused register entries.** 87 distinct sources are cited by no current record, including Medill's 2026 report. They stay in the register for reference and are marked as not cited.
9. **Delivery-log mappings.** DL06 (vehicle safety standards) and DL20 (the Cal/OSHA inspection lottery) still map to loop B1a, independent oversight. Both are enforcement by an independent agency; drop the mapping if you read B1a more narrowly.
10. **Household-effects figures.** A few figures in "What households feel" sections (PW05, PW06) carry no claim link of their own.
11. **Interface items deferred.** Desktop table headers do not stay fixed while the page scrolls. Focus diagrams do not tint neighbors by area. Hub and reform cards use the first sentence of each summary.
12. **Testing limits.** All browser testing ran in Chromium. There was no Firefox or Safari testing, no real phone, no screen reader and no testing with readers.

## 12. Decisions for you

1. **Disclosure wording.** The disclosure now names your Yes on 3 work, based on what you have told me about the campaign. Confirm the wording before anything is published, and add anything it should cover.
2. **LT19's grade.** The content reviewer suggested "plausible" for the new link from concentration to computing built. I graded it a hypothesis because no study separates concentration from overall demand. Raise it if you know of such a study.
3. **Footer tagline.** "From spectators to stewards" was kept as brand language. Remove it if it is not approved.
4. **Publishing.** This is a local artifact project and nothing was published. Publishing the Atlas, as an artifact or on the Oath & Action site, needs your instruction.
