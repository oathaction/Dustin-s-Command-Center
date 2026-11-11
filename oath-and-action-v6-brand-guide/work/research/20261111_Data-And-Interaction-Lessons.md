# What Our World in Data, LOOPY and En-ROADS teach

Oath & Action Edition 06, Phase 3, round 0. Research lead, November 11, 2026, for chapters 13, 14 and 15 (Master Brief sections 13 and 14). Paths are relative to `oath-and-action-v6-brand-guide/`.

Each lesson below comes from a page I read in full today, from this container, on its maker's own site. Where a point rests on a search result alone, the row says so. Each lesson ends in a rule the guide can state, written as chapter 02 asks, with the chapter and the settled decision it would sit beside. The rules are proposals for the data visualization lead and the editor; the guide adopts none of them until a board does.

## The three references, as read today

| # | Reference | Maker | What I read | Date on the page | URL | Checked |
|---|---|---|---|---|---|---|
| L1 | "Redesigning our interactive data visualizations" | Our World in Data (Global Change Data Lab); by Marwa Boukarim, Christian Swinehart and Sophia Mersmann | The whole article | October 18, 2023 | https://ourworldindata.org/redesigning-our-interactive-data-visualizations | 2026-11-11 |
| L2 | LOOPY, "a tool for thinking in systems", version 1.1 | Nicky Case | The landing page, and the labels in the app's play controls and its signal code (`v1.1/js/PlayControls.js`, `Edge.js`) | No date on the page; Phase 1 recorded March 2017 by search | https://ncase.me/loopy/ ; https://ncase.me/loopy/v1.1/ | 2026-11-11 |
| L3 | En-ROADS climate solutions simulator | Climate Interactive and MIT Sloan | The En-ROADS page; "The Science Behind Our Simulators"; the En-ROADS Technical Reference (PDF); the post "Top Nine Ways to Take Your En-ROADS Climate Workshop from Good to Great" | Updates dated April 17 and July 9, 2026 on the En-ROADS page | https://www.climateinteractive.org/en-roads/ ; https://www.climateinteractive.org/simulators-science/ ; https://docs.climateinteractive.org/projects/en-roads-reference-guide/en/latest/ref-guide.pdf ; https://www.climateinteractive.org/blog/top-nine-ways-to-take-your-en-roads-climate-workshop-from-good-to-great/ | 2026-11-11 |

## Our World in Data: one dataset, several views, the source always in sight

Our World in Data's Grapher, the tool behind its charts, groups its 2023 redesign under four headings in the article's words: "Selecting a view", "Downloading and sharing", "Highlighting the data sources" and "Enabling full-screen data exploration".

**What it does.** One dataset shows "as a chart, a color-coded map, and a spreadsheet-like table", switched by buttons at the upper left; each view keeps "just the settings relevant to what you're currently looking at" at the upper right. A settings switch splits a chart into small multiples, and an "Align axis scales" switch decides whether the panels share one scale "to allow for country-to-country comparisons" or zoom to each country's range. Tables sort by their column headings and add summary statistics when a reader picks a range of years. The download menu, at the lower right, "offers graphics (SVG or PNG files) and tabular data (CSV file)". A shared link shows "a preview thumbnail that shows the exact chart configuration", tab and timespan included. "In each of our visualizations, the source of the data is always displayed prominently", and "Learn more about this data" opens the fuller record. Older versions of each article stay browsable, because "our articles are often changed, including the data."

**Rules the guide can state.**

| # | Rule | Where it would sit | Settled decision beside it |
|---|---|---|---|
| OW1 | Show a chart and its table as two views of one dataset, and add a map only when place matters to the reader's question. Put the switch between views first, and each view's own settings beside it | Chapter 14, chart interaction | DR-59 (Chart and Table switches where they help) |
| OW2 | When a reader can split a chart into small multiples, give the panels one shared scale by default, and label any control that lets each panel use its own | Chapter 14, small multiples | DR-64 (charts shown together share one window) |
| OW3 | Let a reader sort a table by any column, and print what a sorted column measures in its heading | Chapter 14, tables | Contract C2's table equivalent |
| OW4 | Offer every chart as SVG, PNG and CSV from one place, and make the CSV hold the rows the chart draws | Chapter 14, exports | DR-49, DR-235, the kit's export check |
| OW5 | Make a shared link open the view the sender saw, and make its preview card show that view | Chapter 14, sharing; chapter 18, share previews | DR-59 |
| OW6 | Print the source line on the chart itself, and put the full record (table, period, vintage, qualification) one click away | Chapter 13, Rule 13.6 | H04 |
| OW7 | Keep each earlier version of a piece whose data changed, reachable from the piece | Chapter 13, Rule 13.13 | DR-233 (corrections in the open) |

**Limits.** The article is three years old, and its "What's next?" list (a new entity selector, a better phone view, a new sources view) may have shipped since; I did not test the live tool. Grapher is built for global comparisons across about 200 countries, while most Oath & Action charts compare 50 states or a few groups. The 2023 article says the code is open source under the MIT license; the site's footer today says the code is public "for transparency and educational reference under a custom license. Re-use requires permission." The studio borrows the conventions, not the code.

## LOOPY: draw a loop, press play, watch the change travel

**What it does.** The landing page offers to "model systems by simply drawing circles & arrows" and to "play with simulations to ask 'what if' questions". The player's controls, as its code labels them, are Play, Stop, Reset, Edit and Remix, with a speed slider between a slow and a fast icon. During play, a change moves along each arrow as a "signal"; each arrow has a strength, 1 by default, and the app caps the signals in flight (100 in all, 10 on one arrow). A model travels inside its link, so anyone can open it, change it and send it on: "LOOPY lets you have a conversation with simulations!" The page calls LOOPY "open source and public domain".

**Rules the guide can state.**

| # | Rule | Where it would sit | Settled decision beside it |
|---|---|---|---|
| LP1 | Let a reader start a loop by acting on one variable, and show the change travel one numbered connection at a time, each step named with its sign and its grade | Chapter 15, interaction | Master Brief section 14; chapter 11's live stepper (DR-195) |
| LP2 | Give every loop playback Pause, Reset and a speed the reader sets, start it only when the reader asks, and offer the same steps as a still sequence | Chapter 15, interaction; chapter 17, motion | Master Brief section 17 |
| LP3 | Draw a loop's connections at one weight unless V7 gives a measured size; a thicker arrow claims an effect size the atlas does not hold | Chapter 15, grammar | Master Brief section 14 ("line width may encode a quantity only with a defined measure") |
| LP4 | Let a reader explore a loop without changing it: no control in the guide or the atlas edits a V7 value, sign or grade | Chapter 15, interaction | V7 is never edited |

**Limits.** LOOPY is qualitative and has no data behind its arrows; its signals all travel at one strength unless a maker sets another, which is the reason for LP3. Its remix feature suits a classroom, and it does not suit a model of record such as Atlas V7, which is the reason for LP4. The page gives no date; the release year rests on Phase 1's search.

## En-ROADS: levers that redraw outcomes, framed as "what if"

**What it does.** Climate Interactive calls En-ROADS a simulator that shows "how today's policy and technology choices can shape our planet's future", "developed by Climate Interactive and MIT Sloan", and says its design allows "instantaneously creating and testing hundreds of climate scenarios". Its science page sets it apart from cost-optimizing models: "En-ROADS is instead a simulation model that explores 'what-if' scenarios under different policies and assumptions, using behavioral decision rules to reflect how people and organizations actually make choices with limited information." The Technical Reference says: "It is not intended as a tool for prediction or projections", and "En-ROADS is dynamic, showing behavior over time, and does not find 'optimal' results." Users can adjust the model's assumptions, and the workshop guide tells facilitators that "if anyone disagrees with any parameters or assumptions, they can change many of them in the 'Assumptions' pane". The same guide says "En-ROADS doesn't 'prove' or 'predict' anything. Instead, use phrases like 'the simulator suggests' and 'in this scenario…'", and asks an audience to "make some prediction" before each change, because "if people just wait and see what happens, they don't learn."

**Rules the guide can state.**

| # | Rule | Where it would sit | Settled decision beside it |
|---|---|---|---|
| ER1 | When a reader picks a reform, show its targets, loops and four ordinal effects at once, side by side, with no total | Chapter 15, worked example 4 (Reform R-01) and the policy comparison | Master Brief section 14 (effects never summed); Rule 12.5 |
| ER2 | Word every outcome an interactive shows as conditional on its assumptions, in the scenario's own terms ("if its assumptions hold"), and never as a forecast | Chapter 13, Rules 13.1 and 13.2; chapter 14, scenario directions | S06's approved title wording; H08 |
| ER3 | Put the assumptions behind any outcome one click from it, in the atlas's own words | Chapter 15, interaction | Master Brief section 14 ("assumptions one click away") |
| ER4 | Before a step-through reveals what a connection does, a piece may ask the reader to guess which way it moves; the answer then comes from V7 | Chapter 15, interaction (an option for teaching pieces) | Research ledger Part 3, I2 (the perception gap quiz's commit-then-reveal pattern) |

**Limits.** En-ROADS runs a quantitative model of climate, energy and the economy, and Atlas V7 holds ordinal effects with no model to run, so the guide borrows the interaction and the "what if" wording, not the simulation: no slider in the guide may move a number V7 does not hold. The awards and user counts on the En-ROADS page are Climate Interactive's own claims and were not checked. The Technical Reference adds that "En-ROADS is constructed using Vensim modeling software from Ventana Systems", which answers the research ledger's open item on Ventana's credit (Phase 1, claim 6): Ventana Systems makes the modeling software, and the page credits the simulator itself to Climate Interactive and MIT Sloan.

## What the three share

All three let the reader decide what changes and when, and each keeps the record behind a view in reach: Our World in Data through its sources overlay and its CSV, LOOPY through a model anyone can open, En-ROADS through its assumptions pane. Chapter 14's interaction section can state that as one rule: keep the source, the table and the assumptions behind a view one click from it, and let no control change an atlas value.

## Claims I could not verify

1. Whether Our World in Data's planned features (new selector, phone view, sources view) have shipped; the live Grapher was not opened.
2. LOOPY's release date on its own page; it gives none.
3. The click-to-change gesture in LOOPY's player: the code shows signals traveling along arrows and the play controls, and I did not run the app.
4. En-ROADS's awards, user counts and languages, as the page states them.
5. The En-ROADS Technical Reference's version and date, which I did not record from the PDF's cover.
