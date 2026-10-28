# Systems Map References

Reference brief for the data visualization lead, Oath & Action Edition 06. Written on October 28, 2026 by the research lead.

The brief studies how the strongest systems, network, transit and small-multiple graphics help a first-time reader see a loop or a whole system. It closes with ten ranked ideas for Atlas V7's 23 loops and its 51-variable map, and the pitfalls to design against. It writes to no ledger. Its rows can move into the research and rights ledgers at the next gate.

## How this was checked

- One page fetch was tried. WebFetch on `https://ncase.me/loopy/` returned "getaddrinfo ENOTFOUND ncase.me" on October 28, 2026, the same block recorded on October 20 and 21. No page in this brief was opened.
- Every check is a web search limited with `allowed_domains` to the official domain, the maker's own site or the publishing journal. The search tool returns a summary that embeds text from the result pages. Wording taken from an official-domain result is marked [snippet]. The tool can paraphrase, so a [snippet] must be checked on the page before the guide prints it as a quotation.
- The search tool refused three domains outright on October 28, 2026: nytimes.com, ft.com and reuters.com ("not accessible to our user agent"). Work from The New York Times, the Financial Times and Reuters is checked through award bodies, the makers' own sites and the FT's GitHub organization, and is marked PARTLY where that leaves a gap.
- Status key. VERIFIED: the claim appears in official-domain results and they agree. PARTLY: part of the claim was confirmed, or it rests on a secondary source or the maker's own site. UNVERIFIED: not found on an official domain. CARRIED: verified in `work/research/20261021_Research-Ledger.md` on October 21, 2026, and not rechecked unless the entry says so.
- Studio memory is labeled as such wherever I describe a mechanism the search results did not show.
- Rights: every image named here is study only unless the entry says otherwise. Never trace, embed or ship it (Master Brief V2 section 2). Quotations keep the source's spelling.
- Every entry was checked on 2026-10-28 unless it says CARRIED.

## The shape of Atlas V7 these references must serve

Read from `work/extract/atlas-v7-data.json` with a script on October 28, 2026.

- **Variables (51).** Three layers: core 31, economy 12, technology 8. The core layer holds five regions: A Economic structure (6 variables), B Political inputs (6), C Electoral competition (5), D Governing institutions (7) and E Legitimacy (2), plus X Outside drivers (5). The economy layer holds three regions of four variables, and technology holds one region of eight. A separate `domain` field (D01 to D10) is filled on 31 variables and empty on 20. The task's "five domains" matches the five core regions. Each direction should state which grouping it draws.
- **Variable types.** Stock 31, flow 9, auxiliary 6, driver 5.
- **Connections (118).** Causal 80, money 17, information 9, authority 7, ownership 5. Plus 70, minus 41, no sign 7 (all authority). Delay S 38, M 45, L 35. Evidence: well-supported 37, plausible 35, documented 32, plausible_contested 7, hypothesis 7. Seven connections carry the `contested` flag. Nineteen carry `spine: true`; I found no definition of "spine" in V7's methods text, so confirm its meaning with the atlas editor before drawing it as a core.
- **Loops (23).** 18 reinforcing (R) and 5 balancing (B). Twenty have numbered chains: 11 of two steps, 5 of three and 4 of four. B2, B3 and R9 are conceptual, with no numbered chain. R2 and R16 close through a hypothesized step. No authority connection sits on a loop.
- **Overlap.** 46 distinct connections sit on named loops, and 6 of them sit on more than one. L42, "Incumbent-drawn maps create safe seats," sits on R4a, R10 and R12. 32 of the 51 variables sit on at least one loop. E1, "Policy advantages for wealthy and organized interests," sits on 7 loops. C3, "Risk of losing office," and C4, "Officeholders' control over election rules," sit on 4 each.
- **Crossings.** 81 of the 118 connections join variables in different regions, and 31 join different layers. E1 has 13 connections; B4 and D2 have 11 each.
- **Loop fields that help design.** Each loop carries `how_to_read` (a plain sentence), `reference_mode` (a named measured series, such as "Incumbent defeat rate 1964 to 2024" for B4) and `direction` (such as `running_up`).
- **Identifier collision.** B2, B3, B4 and B5 each name both a variable and a loop. V7's conventions say "the text always says which." V7 also states that the drawn graph contains cycles that carry no name.
- **Reform bands.** V7 sorts its 50 reforms into bands taken from Donella Meadows' ordering of leverage points (V7 source W169): rules 26, parameter 11, feedback 5, information 4, power to change the rules 3, goals 1.

---

## 1. Causal loop and stock-and-flow diagrams

A causal loop diagram draws variables joined by arrows marked plus or minus; a chain of arrows that returns to its start is a feedback loop. A stock-and-flow diagram separates amounts that build up over time (stocks) from the rates that fill or drain them (flows).

### 1.1 Donella Meadows, stocks and flows in "Thinking in Systems"

- **What it is.** A primer on systems. The Donella Meadows Project hosts a chapter on stocks and flows.
- **Who and when.** Donella H. Meadows, Dartmouth College. The hosted file is headed "3/28/13 DRAFT" [snippet]. The book's publication date did not appear in today's results.
- **Mechanism.** The bathtub. "Stocks will be illustrated by boxes or rectangles, and flows by pipes leading into or out of the stocks" [snippet]. Anyone who has filled a tub can reason about a slow rise and a lag.
- **Borrow.** One physical metaphor for V7's 31 stocks, drawn the same way everywhere. A long delay (L) into a stock then reads as natural.
- **Avoid.** Pipes and valves on V7's causal links. Most V7 connections describe influence, and only the money and ownership types resemble a physical flow. Two notations on one page confuse a new reader.
- **Status.** VERIFIED, search only.
- **Rights.** Rights holder not checked. Study only.
- **URL.** https://donellameadows.org/wp-content/userfiles/bathtubs101.pdf

### 1.2 Donella Meadows, "Leverage Points: Places to Intervene in a System"

- **What it is.** An essay that ranks places to intervene in a system by how far a change reaches.
- **Who and when.** Donella Meadows, The Sustainability Institute. V7's source W169 gives 1999. Results describe an original nine-item list and a revised twelve-item list [snippet].
- **Mechanism.** A ladder of intervention types. A reader can ask how deep a reform reaches before asking what it might change.
- **Borrow.** A ladder drawn beside the map that places each reform at its V7 band and, in the same view, at its target link or variable.
- **Avoid.** Any reading of the ladder as a score. V7 never adds reform effects into one number. A band places a reform by depth of change, and the ordinal effect codes carry the expected direction and size.
- **Status.** VERIFIED, search only. The 1999 date rests on V7's source record.
- **Rights.** Study only.
- **URL.** https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/ ; https://donellameadows.org/a-visual-approach-to-leverage-points/

### 1.3 John Sterman, "Business Dynamics," chapter 5

- **What it is.** The standard graduate text on system dynamics. Chapter 5 sets the notation rules for causal loop diagrams.
- **Who and when.** John D. Sterman, MIT Sloan. McGraw-Hill/Irwin, 2000 [snippet].
- **Mechanism.** A short, checkable rule list. MIT course material tells students to follow the chapter, "including labeling the polarity of every link and loop, naming your loops" and "showing important delays" [snippet]. The table of contents covers "not putting all the loops into one large diagram" [snippet].
- **Borrow.** Sign every link. Mark loop polarity at the loop's center. Mark delay on the link itself. Name every loop in words a reader would use, which V7's loop titles already do. Teach loops in separate panels and keep the whole map for orientation.
- **Avoid.** Any suggestion that plus means good. V7's conventions say "a plus sign can mark a harmful effect."
- **Status.** VERIFIED, search only (MIT faculty site and MIT OpenCourseWare).
- **Rights.** Study only.
- **URL.** https://web.mit.edu/jsterman/www/BusDyn2.html ; https://mitmgmtfaculty.mit.edu/jsterman/business-dynamics/ ; https://ocw.mit.edu/courses/15-872-system-dynamics-ii-fall-2013/

### 1.4 Linda Booth Sweeney and John Sterman, "Bathtub Dynamics"

- **What it is.** A study that tested whether educated adults can reason about stocks and flows with simple bathtub tasks.
- **Who and when.** Booth Sweeney and Sterman, System Dynamics Review 16(4), 2000 [snippet].
- **Mechanism.** Evidence about the reader. Business school students with little training did poorly, and they often drew the stock with the same shape as the net flow [snippet, paraphrased]. A later MIT study found that "84%" of graduate students violated principles of accumulation when reasoning about atmospheric carbon dioxide [snippet].
- **Borrow.** Treat accumulation as something the graphic must teach. Give stocks a shape distinct from flows and auxiliaries, and pair a stock with its slow-moving measured line.
- **Avoid.** Relying on a familiar story to fix the error. A follow-up found no significant differences in performance across task contexts [snippet, paraphrased].
- **Status.** VERIFIED for the paper and its main finding. PARTLY for the 84 percent figure, which reached me through a summary of later MIT papers.
- **Rights.** Study only.
- **URL.** https://web.mit.edu/jsterman/www/Bathtub.pdf ; https://mitmgmtfaculty.mit.edu/jsterman/bathtubdynamics/

### 1.5 Climate Interactive, Climate Bathtub Simulation and En-ROADS

- **What it is.** An animated bathtub model of atmospheric carbon, and En-ROADS, a climate policy simulator.
- **Who and when.** Climate Interactive. The bathtub coach notes credit Drew Jones and sit under a 2014 upload path. En-ROADS is CARRIED from S12 (with MIT Sloan; the Ventana Systems credit was not seen).
- **Mechanism.** The tub level rises while inflow exceeds outflow. To stabilize the level, "net inflows must be zero" [snippet]. En-ROADS moves a lever and redraws the outcome at once, framed as a "what-if" exploration (CARRIED).
- **Borrow.** For reforms: choose one, see its targets light on the map, read its ordinal effects, and open the assumptions in one step.
- **Avoid.** Sliders and continuous curves. V7 has no equations and its effects are ordinal codes, so a slider implies precision the model lacks (Master Brief V2 section 14).
- **Status.** VERIFIED for the bathtub framing. En-ROADS CARRIED.
- **Rights.** Study only.
- **URL.** https://img.climateinteractive.org/2014/01/Climate_Bathtub_Sim_Facilitator_Guide.pdf ; https://www.climateinteractive.org/the-climate-leader/stocks-and-flows/ ; https://www.climateinteractive.org/en-roads/

### 1.6 isee systems, Stella storytelling

- **What it is.** Modeling software for stock-and-flow models, with a storytelling mode that reveals a model in stages.
- **Who and when.** isee systems. Help pages are versioned (v1.2 to v2.1), with no single date. The same site hosts Barry Richmond's "An Introduction to Systems Thinking."
- **Mechanism.** A fixed build order. The help pages suggest revealing the stock, then the flow, then the connector from stock to flow, each step showing a new behavior, and they advise authors to "start with the 5 most important steps that convey your message" [snippet].
- **Borrow.** One build order for every loop card: first variable, first link, next variable, and on around until the loop closes and its R or B mark appears.
- **Avoid.** A step-by-step build of all 51 variables. Keep a build to one loop.
- **Status.** VERIFIED, search only.
- **Rights.** Study only.
- **URL.** https://www.iseesystems.com/resources/help/v1-2/Content/06-Building_Interfaces/1InterfaceBuldingExample.htm ; https://www.iseesystems.com/resources/articles/download/intro-systems-thinking-chapt-1.pdf

### 1.7 Behavior-over-time graphs, The Systems Thinker

- **What it is.** A quick sketch of how a variable has moved over time, paired with the loop that drives it. Practitioners also call these reference modes [snippet, paraphrased].
- **Who and when.** The Systems Thinker toolbox reprints and Daniel H. Kim's "Systems Archetype Basics," hosted at thesystemsthinker.com. Dates were not seen.
- **Mechanism.** Structure and behavior side by side. A curve that climbs faster and faster points to a reinforcing loop, and "for every goal-seeking behavior, there is a balancing loop" [snippet].
- **Borrow.** V7 names a measured series for every loop in `reference_mode` (R1: "Top 1% wealth share 22.8% (1989) to 32.5% (2026Q2, a record)"). A small line chart on each loop card shows the loop's footprint in the world.
- **Avoid.** A smooth textbook curve in place of the measured series. Plot the named series with its source line, and label any schematic shape "Illustration."
- **Status.** VERIFIED, search only.
- **Rights.** Study only.
- **URL.** https://thesystemsthinker.com/wp-content/uploads/2016/03/Systems-Thinking-Tools-TRST01E.pdf ; https://thesystemsthinker.com/wp-content/uploads/2016/03/Systems-Archetypes-Basics-WB002E.pdf

### 1.8 Kumu

- **What it is.** A web platform for systems and network maps, with named loops.
- **Who and when.** Kumu Inc. Live. The search tool reported the loops page as about 558 days old.
- **Mechanism.** A test any reader can run: "If I follow the arrows in this group of connections, can I get trapped?" [snippet]. Loops appear as a text label placed at the center of their connections [snippet, paraphrased]. Showcase highlights an element's direct relations on hover and mutes the rest. Focus shows chosen items and widens or narrows by degree with the plus and minus keys [snippet, paraphrased]. Presentations build a map over successive slides, each with its own focus and filter.
- **Borrow.** The loop label at the center of the ring. The "trapped" test as reader copy on the first loop. Focus by degree on the whole map: one variable, then one step out, then two.
- **Avoid.** Copying the look of public maps on kumu.io. Their authors own them and their quality varies.
- **Status.** VERIFIED, search only.
- **Rights.** Kumu's interface and user maps belong to their owners. Study only.
- **URL.** https://docs.kumu.io/guides/what-are-loops ; https://docs.kumu.io/guides/focus.html ; https://docs.kumu.io/guides/presentations ; https://kumu.io/markets/system-mapping

### 1.9 Nicky Case, LOOPY

- **What it is.** A web tool for drawing a causal loop and running it.
- **Who and when.** Nicky Case, released March 2017 [snippet]. Version 1.1 is current.
- **Mechanism.** Draw, press play, and watch a change travel around the loop. Users "model systems by simply drawing circles & arrows" [snippet]. "To make a stronger relationship, draw multiple arrows!" [snippet]. A longer arrow makes the link delayed [snippet, paraphrased].
- **Borrow.** The traveling pulse as the reading aid for one loop. A marker moves one numbered step at a time, the next variable rises or falls, and the reader can pause, step back or reset. LOOPY's long arrow for delay suggests a length or spacing cue for S, M and L.
- **Avoid.** LOOPY's arrow count for strength. V7 grades evidence and has no strength measure, so line weight stays constant. Avoid an endless pulse on a reinforcing loop, which reads as runaway growth the model does not claim.
- **Status.** VERIFIED, search only. Re-searched today; CARRIED as S11.
- **Rights.** Open source and public domain [snippet]. Models drawn by other people belong to them.
- **URL.** https://ncase.me/loopy/ ; https://ncase.me/loopy/v1.1/

### 1.10 Nicky Case, explorable explanation patterns and "The Wisdom and/or Madness of Crowds"

- **What it is.** Blog posts on designing explorable explanations (interactive essays where the reader works a small model to learn an idea), and an explorable about how network structure shapes group behavior.
- **Who and when.** Nicky Case. "Explorable Explanations" (2014); "Explorable Explanations: 4 More Design Patterns" (June 20, 2018) [snippet]; "Crowds" (April 2018) [snippet].
- **Mechanism.** "Start small, build big" [snippet]: teach each part alone before combining parts. "Place Your Bets": the reader predicts, then sees the result. Case warns that a sandbox (open free play) can overwhelm a learner and suggests placing it at the end [snippet, paraphrased].
- **Borrow.** Open on one two-step loop (R8 on housing has two numbered links), move to a three-step loop, and hold the whole map back as the closing sandbox. Ask the reader to predict the returning sign before the pulse runs.
- **Avoid.** Opening on the full map.
- **Status.** VERIFIED, search only. The advice comes from Case's own practice; I found no independent test of it.
- **Rights.** Study only.
- **URL.** https://blog.ncase.me/explorable-explanations/ ; https://blog.ncase.me/explorable-explanations-4-more-design-patterns/ ; https://ncase.me/crowds/

### 1.11 Bret Victor, "Explorable Explanations"

- **What it is.** An essay on active reading.
- **Who and when.** Bret Victor, dated March 10, 2011, with a postscript added in February 2024 [snippet].
- **Mechanism.** Three building blocks: reactive documents, explorable examples and contextual information [snippet, paraphrased].
- **Borrow.** Contextual information. Tap a variable or link and its definition, its `increase_means` sentence, its sign meaning and its source open in place.
- **Avoid.** Prose numbers that recalculate. V7 has no model to compute them.
- **Status.** VERIFIED, search only.
- **Rights.** Study only.
- **URL.** https://worrydream.com/ExplorableExplanations/

### 1.12 UK Government Office for Science, Foresight obesity system map

- **What it is.** A public systems map of the causes of obesity, published with "Tackling Obesities: Future Choices."
- **Who and when.** Foresight program, UK government. Search summaries give October 17, 2007 (PARTLY).
- **Mechanism to learn.** The map anchors on one variable, energy balance [snippet, paraphrased], groups its variables into seven themes [snippet], and builds outward from a core engine of loops, adding key variables and then tiers of others [snippet, paraphrased]. Results give 108 variables and 304 causal linkages; the page that states the count was not pinned (PARTLY).
- **Borrow.** The build order: core engine, then themes, then tiers.
- **Avoid.** The full poster as a first view. Foresight's own blog says "some have criticised its complexity" [snippet]. It is the best-known public-policy hairball (a network drawn so densely that no path can be followed).
- **Status.** VERIFIED for the project and the blog line. PARTLY for the counts and date.
- **Rights.** UK Crown copyright. License terms not checked. Study only.
- **URL.** https://www.gov.uk/government/publications/reducing-obesity-obesity-system-map ; https://assets.publishing.service.gov.uk/media/5a7b8811ed915d4147620fb2/07-1177-obesity-system-atlas.pdf ; https://foresightprojects.blog.gov.uk/2017/10/04/dusting-off-foresights-obesity-report/

---

## 2. Transit diagrams

A transit diagram keeps the order of stops and the places where lines meet, and drops true distance and direction.

### 2.1 Harry Beck, London Underground diagram

- **What it is.** The diagram that set the pattern for transit maps.
- **Who and when.** Henry C. (Harry) Beck. Sketched in 1931 while he was out of work; first pocket edition printed January 1933 [snippet, London Transport Museum]. TfL calls him an "Underground electrical draughtsman" [snippet] and says he based the map on the circuit diagrams he drew for his day job [snippet, paraphrased].
- **Mechanism.** Order and connection on a strict grid. He used "only horizontal, vertical and 45º lines" [snippet], spaced stations evenly, and replaced "circular 'blobs', representing stations, with the now familiar rectangular 'ticks'" [snippet].
- **Borrow.** Angles at 0, 45 and 90 degrees. Even spacing between loop steps, since V7 has no distances to keep. An interchange symbol for variables that sit on several loops (E1 on 7, C3 and C4 on 4).
- **Avoid.** Underground styling. The roundel, the Johnston typeface and the diagram's look belong to TfL, which publishes guidance on third-party use of its brand IP (title seen in search, not read).
- **Also.** The London Transport Museum holds a 1933 Beck print of a "spoof Underground map annotated as a radio circuit diagram" [snippet]. It joins the transit and circuit traditions in one sheet.
- **Status.** VERIFIED, search only.
- **Rights.** TfL and the London Transport Museum. Study only.
- **URL.** https://www.ltmuseum.co.uk/collections/stories/design/transforming-tube-map-harry-becks-iconic-design ; https://content.tfl.gov.uk/research-guide-24-harry-beck.pdf ; https://www.ltmuseum.co.uk/collections/collections-online/photographs/item/2004-18155 ; https://content.tfl.gov.uk/tfl-ip-guidance.pdf

### 2.2 Massimo Vignelli and Unimark, New York City subway diagram

- **What it is.** The 1972 New York City subway diagram.
- **Who and when.** MoMA credits Massimo Vignelli, Joan Charysyn, Bob Noorda and Unimark International Corporation, New York, and dates it 1970 to 1972 [snippet]. It was replaced in 1979 by a more geographic map [snippet, paraphrased]. MoMA acquired it in 2004.
- **Mechanism.** One color per route on a rectilinear grid. The diagram "eliminated winding train lines and topographical references in favor of a rectilinear format" [snippet].
- **Borrow.** Parallel route lines through shared track. Six V7 connections sit on more than one loop, and L42 sits on three, so loops can run side by side along a shared connection.
- **Avoid.** Removing every anchor the reader already holds. The 1972 diagram drew criticism and was replaced. In V7 the anchor is plain language, so every variable needs its everyday name and what a higher value means.
- **Status.** VERIFIED, search only (MoMA, MTA).
- **Rights.** MoMA collection and MTA. Study only.
- **URL.** https://www.moma.org/collection/works/89300 ; https://www.mta.info/agency/arts-design/collection/subway-design-for-modern-icon

### 2.3 MTA, 2025 subway diagram and Live Subway Map

- **What it is.** The MTA's 2025 redesigned subway diagram, and its 2020 live digital map.
- **Who and when.** Press release dated April 2, 2025: the first new design since 1979, with geometry drawn from the 1972 Vignelli diagram and colors kept from the Hertz maps [snippet, paraphrased]. Live Subway Map: MTA, Work & Co and the Transit Innovation Partnership, beta in October 2020, designed pro bono [snippet].
- **Mechanism.** Status drawn on the line. On the live map, train lines redraw from real-time data and "sections fade out where service is suspended" [snippet]. The 2025 legend gathers accessibility, transfer and safety information [snippet, paraphrased].
- **Borrow.** A faded segment, with a text label, for a hypothesized step (R2, R16) and for a conceptual loop (B2, B3, R9).
- **Avoid.** Fading as the only cue. Pair it with a label and a line pattern so the status survives grayscale.
- **Awards.** Gold Lion, Cannes 2021; Webby 2021; Fast Company Innovation by Design 2021; TIME Best Inventions 2021 (MTA and Work & Co pages).
- **Status.** VERIFIED, search only.
- **Rights.** MTA. Study only.
- **URL.** https://www.mta.info/press-release/mta-unveils-first-fully-redesigned-subway-map-half-century ; https://www.mta.info/press-release/mta-launches-groundbreaking-subway-map-creating-next-generation-map-following-iconic-hertz-and-vignelli-designs ; https://work.co/news/mta-new-live-subway-map/

### 2.4 Jug Cerović and INAT, standard metro maps

- **What it is.** One mapping standard applied to metro systems in many cities.
- **Who and when.** Jug Cerović, founder of INAT, a mapping and wayfinding consultancy. Ongoing. INAT notes his membership of the UITP Design and Culture Committee [snippet].
- **Mechanism.** One grammar for many maps. "All lines are represented vertical, horizontal, or 45° inclined. Line angles are gently curved" [snippet]. The Tokyo map draws the Oedo line as an axially symmetric loop [snippet, paraphrased].
- **Borrow.** One standard across 23 loop cards and the whole map, so a reader who learns one card can read every card. Gently curved corners give the circuit grid a calmer look for a general reader.
- **Avoid.** A new geometry for each loop.
- **Status.** VERIFIED, search only.
- **Rights.** INAT. Study only.
- **URL.** https://www.inat.fr/metro-maps/ ; https://www.inat.fr/metro/tokyo/ ; https://www.inat.fr/about/

### 2.5 Art. Lebedev Studio, Moscow Metro map and in-car line maps

- **What it is.** The Moscow Metro diagram, version 2.0 and later, and the line maps inside cars.
- **Who and when.** Art. Lebedev Studio. Search summaries date map 2.0 to 2013 (PARTLY); later versions run to map 5.0.
- **Mechanism.** The loop drawn as a true circle. The studio writes that "the loop line represented with a geometrical circle is the most recognizable, the signature element of the Moscow Metro Map" [snippet]. The map is "free from confusing line overlaps at the most critical locations, the connections" [snippet]. On in-car line maps, the Circle line "must not steal all the attention" [snippet].
- **Borrow.** Each closed loop as a circle, so a reader sees that it returns to its start before reading a word. Interchanges kept clear of overlaps. The in-car strip map as the narrow-screen form of one loop: a straight strip of steps with a marked return.
- **Avoid.** One dominant ring on the whole map. With 20 closed loops, a single hero ring pulls attention from the rest.
- **Status.** VERIFIED, search only.
- **Rights.** The studio and Moscow Metro. Study only.
- **URL.** https://www.artlebedev.com/metro/map2/ ; https://www.artlebedev.com/metro/line-map/ ; https://www.artlebedev.com/metro/line-map/process/

---

## 3. Small multiples

Small multiples are a set of small graphics that share one design, each showing a different slice of the data, so the eye compares across them.

### 3.1 Edward Tufte, small multiples

- **What it is.** Tufte's treatment of small multiples in "Envisioning Information," and of visual parallelism in "Visual Explanations."
- **Who and when.** Edward Tufte, Graphics Press. "Envisioning Information" (1990) covers small multiples [snippet, book page]. "Visual Explanations" is dated 1997 by the secondary papers in the results.
- **Mechanism.** A constant frame. When the design repeats exactly, every difference a reader sees comes from the data.
- **Borrow.** 23 loop cards in one geometry: the same ring, step 1 at twelve o'clock, clockwise reading, the R or B mark at the center, the reference-mode line in the same corner. Two-, three- and four-step loops differ only in the number of stops on the ring. Conceptual loops use the same frame with their status written in.
- **Avoid.** Rescaling or rotating cards to fit content.
- **Status.** VERIFIED for the book's contents, search only. Tufte's own wording did not appear in official results, so this brief quotes none.
- **Rights.** Graphics Press. Study only.
- **URL.** https://www.edwardtufte.com/book/envisioning-information/ ; https://www.edwardtufte.com/notebook/london-underground-maps-worldwide-subway-maps/

### 3.2 Financial Times, Visual Vocabulary and pandemic data coverage

- **What it is.** The FT's chart chooser, organized by the relationship a chart shows, and its pandemic data coverage.
- **Who and when.** FT visual and data journalism team. The Visual Vocabulary guide sits on the FT's GitHub organization. The Royal Statistical Society named the team's pandemic data coverage, with John Burn-Murdoch among the named contributors, a winner of its 2021 Statistical Excellence in Journalism Awards [snippet].
- **Mechanism.** Choose the form by the reader's question. The guide's flow family covers "volumes or intensity of movement between states or conditions" [snippet]. It describes the Sankey as suited to tracing "the eventual outcome of a multi-step process," the chord as "complex but powerful" for two-way flows, and the network for "the strength and interconnection of relationships of varying types" [snippet].
- **Borrow.** The question-first structure for the systems chapter's chooser.
- **Avoid.** Treating "flow" forms as a fit for causal loops. Each one in the FT family assumes a measured volume.
- **Status.** VERIFIED for Visual Vocabulary (GitHub, Financial-Times organization) and the RSS award. PARTLY for the pandemic charts' design, since ft.com could not be searched. CARRIED as S26.
- **Rights.** The FT's template repositories carry an MIT license that excludes FT content and branding [snippet, paraphrased]. Study only.
- **URL.** https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md ; https://rss.org.uk/news-publication/news-publications/2021/general-news/statistical-excellence-in-journalism-awards-2021-w/

---

## 4. Network forms

A node-link diagram draws each variable as a node and each connection as a line. The forms below rearrange that picture to cut crossings.

### 4.1 Arc diagram

- **What it is.** Nodes placed along one line, with connections drawn as arcs above or below it.
- **Who and when.** Martin Wattenberg, IBM Research, "Arc Diagrams: Visualizing Structure in Strings," IEEE InfoVis 2002, pages 110 to 116 [snippet].
- **Mechanism.** A one-dimensional order. The original highlights "repeated subsequences" in music, text and code [snippet]. Applied to a network, the reader sees where a connection jumps forward or back.
- **Borrow.** One loop or one region laid on a line in loop order, with a returning arc from the last variable to the first that closes the loop. Plus and minus links can sit on opposite sides of the line, with the sign printed on each arc.
- **Avoid.** All 118 connections on one line. Long arcs pile up into a fan.
- **Status.** VERIFIED, search only (maker's sites).
- **Rights.** Study only.
- **URL.** http://hint.fm/papers/arc-diagrams.pdf ; https://www.bewitched.com/song.html

### 4.2 Chord diagram (Circos)

- **What it is.** Segments around a circle with ribbons between them; a ribbon's width shows a quantity.
- **Who and when.** Martin Krzywinski and colleagues, "Circos: An information aesthetic for comparative genomics," Genome Research 19, 2009, pages 1639 to 1645 [snippet].
- **Mechanism.** "A circular ideogram layout to facilitate the display of relationships between pairs of positions by the use of ribbons" [snippet].
- **Borrow.** A summary of which regions connect to which: the five core regions, X, economy and technology around a ring, with ribbon width set to the count of connections (81 of the 118 connections cross regions). A count is a defined measure, so width is allowed under Master Brief V2 section 14 if the legend says "number of connections."
- **Avoid.** Ribbons for sign, direction or evidence. Circos shows direction with ribbon thickness, segment order and twists [snippet, paraphrased], which a new reader will miss.
- **Status.** VERIFIED, search only.
- **Rights.** Study only.
- **URL.** https://genome.cshlp.org/content/19/9/1639 ; https://circos.ca/intro/data_visualization/

### 4.3 Hierarchical edge bundling

- **What it is.** Links that share a branch of a hierarchy curve together into bundles.
- **Who and when.** Danny Holten, "Hierarchical edge bundles: visualization of adjacency relations in hierarchical data," IEEE Transactions on Visualization and Computer Graphics 12(5), 2006, pages 741 to 748 [snippet]. IEEE InfoVis Test of Time Award, 2016 [snippet].
- **Mechanism.** Bundling along the hierarchy cuts clutter and shows implied links between parent groups [snippet, paraphrased]. The D3 example isolates a node's incoming and outgoing links on hover.
- **Borrow.** An overview ring: variables grouped by region around a circle, bundles showing which regions talk, hover isolating one variable's links.
- **Avoid.** Tracing a loop through bundles. Bundles merge lines, so a reader cannot tell which link goes where. A 2021 paper is titled "Edge-Path Bundling: A Less Ambiguous Edge Bundling Approach" (arXiv, title only).
- **Status.** VERIFIED, search only (TU Eindhoven research portal and news).
- **Rights.** Study only.
- **URL.** https://research.tue.nl/en/publications/hierarchical-edge-bundles-visualization-of-adjacency-relations-in/ ; https://www.tue.nl/en/mathematics-and-computer-science/news-1/08-11-2016-danny-holten-receives-infovis-test-of-time-award ; https://observablehq.com/@d3/hierarchical-edge-bundling

### 4.4 Adjacency matrix

- **What it is.** A grid with every variable on both axes; a filled cell means the row variable connects to the column variable.
- **Who and when.** Mohammad Ghoniem, Jean-Daniel Fekete and Philippe Castagliola, "A Comparison of the Readability of Graphs Using Node-Link and Matrix-Based Representations," IEEE InfoVis 2004, pages 17 to 24 [snippet, HAL record]. Mike Bostock's "Les Misérables Co-occurrence" matrix lets the reader order rows by name, frequency or cluster [snippet]; the same page credits Jacques Bertin's team with reordering matrices by hand [snippet, paraphrased].
- **Mechanism.** No line ever crosses another, and row order makes clusters visible. Later papers report that the 2004 study favored node-link drawings for small sparse networks and matrices for larger ones, except on tasks that trace a path (secondary sources on arXiv).
- **Borrow.** A 51 by 51 matrix sorted by region as the companion index to the map, with a sign and grade glyph in each filled cell. It doubles as the table equivalent for screen readers and suits the favored Concept 11 Register.
- **Avoid.** The matrix as the way to teach a loop. Path tracing is its weak task.
- **Status.** VERIFIED for the citation and Bostock's page. PARTLY for the findings, which reached me through secondary papers.
- **Rights.** Study only.
- **URL.** https://hal.science/hal-00343819v1 ; https://bost.ocks.org/mike/miserables/

### 4.5 Hive plot

- **What it is.** Nodes placed on a few radial axes by fixed rules, with links curving between axes.
- **Who and when.** Martin Krzywinski and colleagues, "Hive plots: rational approach to visualizing networks," Briefings in Bioinformatics 13(5), 2012 [snippet].
- **Mechanism.** Placement by rule. The same structure always gets the same layout under a rule set [snippet, paraphrased]. The authors note that force-based layouts "have earned the disparaging moniker 'hairballs'" [snippet]. (A force-directed layout places nodes by simulating springs and repulsion, so the picture changes with each run.)
- **Borrow.** A placement rule a reader can hear in one sentence, such as axes by variable type (stock, flow, auxiliary, driver) or by layer, with position along an axis set by number of connections.
- **Avoid.** A hive plot as the public face of the atlas. Its axes need teaching.
- **Status.** VERIFIED, search only.
- **Rights.** Study only.
- **URL.** https://academic.oup.com/bib/article/13/5/627/412507 ; http://mkweb.bcgsc.ca/linnet/

### 4.6 BioFabric

- **What it is.** A network drawing where each node is a horizontal line and each connection a short vertical line between two node rows.
- **Who and when.** William Longabaugh, "Combing the hairball with BioFabric," BMC Bioinformatics 13:275, 2012 [snippet].
- **Mechanism.** Every connection gets its own column, so nothing overlaps and nodes with similar connections can be scanned in very large networks [snippet, paraphrased].
- **Borrow.** A print index of all 118 connections, ordered by loop so the 46 loop connections sit together and the rest follow by region.
- **Avoid.** As a first view. It reads as abstract to a general audience.
- **Status.** VERIFIED, search only (PubMed Central and biofabric.org).
- **Rights.** Study only.
- **URL.** https://pmc.ncbi.nlm.nih.gov/articles/PMC3574047/ ; https://biofabric.org/

### 4.7 Sankey diagram and flow maps

- **What it is.** A flow drawing where band width is proportional to a measured quantity.
- **Who and when.** H. R. Sankey's 1898 committee report on the thermal efficiency of steam engines, Minutes of the Proceedings of the Institution of Civil Engineers 134, pages 278 to 312, "including appendixes and plate at back of volume" [snippet]; the plate's contents were not confirmed. Lawrence Livermore National Laboratory has produced United States energy flow charts since the mid-1970s [snippet]. Charles Joseph Minard's 1869 map of Napoleon's 1812 campaign, which Tufte calls "probably the best statistical graphic ever drawn" [snippet], uses band width for the army's size.
- **Mechanism.** Conservation made visible: what enters a node leaves it, and the reader sees losses as narrowing bands. LLNL: "Flow charts, also referred to as Sankey Diagrams, are single-page references that contain quantitative data about resource, commodity, and byproduct flows" [snippet].
- **Borrow.** Only where V7 offers measured, compatible amounts, such as a specimen on money flows with sourced figures.
- **Avoid.** A Sankey for any loop. The D3 Sankey module exists to "visualize flow between nodes in a directed acyclic network" [snippet], and a loop is a cycle. Avoid band width for evidence or importance.
- **Status.** VERIFIED for LLNL, the D3 module, the ICE record and Tufte's description of Minard.
- **Rights.** LLNL charts: terms not checked. Minard: the 1869 original is old, and the rights in any particular scan were not checked. Study only.
- **URL.** https://flowcharts.llnl.gov/ ; https://www.icevirtuallibrary.com/doi/10.1680/imotp.1898.19100 ; https://observablehq.com/collection/@d3/d3-sankey ; https://www.edwardtufte.com/product/napoleons-march/

### 4.8 Harvard Growth Lab, Atlas of Economic Complexity, Product Space

- **What it is.** A network of about 800 traded products, linked when the same countries export them.
- **Who and when.** Harvard Growth Lab. The redesigned Product Space shipped with Atlas 10.0, about 13 months before the search [snippet, metadata].
- **Mechanism.** A fixed layout, reused on every view, with labeled knowledge clusters and color by complexity [snippet, paraphrased]. A secondary source says a plain force layout curled the products into a loop with no direction, so the designers stretched the map to show development paths (arXiv, PARTLY).
- **Borrow.** One fixed position for each of the 51 variables, kept on every view, so a reader learns the map once. Region labels on the map itself.
- **Avoid.** Its density. V7 is small enough to label every variable.
- **Status.** VERIFIED for the structure (Growth Lab). PARTLY for the layout history.
- **Rights.** Study only.
- **URL.** https://growthlab.hks.harvard.edu/news/atlas-economic-complexity-100-brings-new-data-and-product-space-design/ ; https://growthlab.hks.harvard.edu/wp-content/uploads/2015/07/economic_complexity_briefing.pdf

---

## 5. Data journalism systems graphics

### 5.1 The Washington Post, "Why outbreaks like coronavirus spread exponentially, and how to 'flatten the curve'"

- **What it is.** An explainer built on simulations of a made-up disease, "simulitis," spreading through a small town.
- **Who and when.** Harry Stevens, graphics reporter, March 14, 2020 [snippet]. A Post video calls it the most-read story in Washington Post history, which is the paper's own claim.
- **Mechanism.** A toy model makes a reinforcing loop visible as moving dots, then shows the lever: fewer contacts weaken the loop. The text marks its doubling arithmetic as a calculation and declines to call it a forecast [snippet, paraphrased].
- **Borrow.** A small, plainly labeled toy beside a real claim, and the explicit line between arithmetic and forecast.
- **Avoid.** Toy dynamics beside a V7 loop without an "Illustration" label. Moving dots suggest rates V7 does not estimate.
- **Status.** VERIFIED, search only.
- **Rights.** The Washington Post. Study only.
- **URL.** https://www.washingtonpost.com/graphics/2020/world/corona-simulator/

### 5.2 The New York Times, "512 Paths to the White House"

- **What it is.** A 2012 election graphic.
- **Who and when.** Mike Bostock's site lists "512 Paths to the White House" under November 2, 2012 [snippet]. Shan Carter's site lists it among his previous work and links Bostock's write-up [snippet, paraphrased].
- **Mechanism.** Studio memory, unverified today: a branching tree of outcomes that prunes as the reader picks a winner in each swing state. The results did not describe how it works.
- **Borrow.** If confirmed, the pruning tree suits the route-to-change tracker, where each choice closes some paths and opens others.
- **Avoid.** Citing its mechanics until someone reads the page.
- **Status.** PARTLY. nytimes.com could not be searched.
- **Rights.** The New York Times. Study only.
- **URL.** https://bost.ocks.org/mike/ ; http://shancarter.com/talk/2012/visualized/

### 5.3 The New York Times, election maps (SND47)

- **What it is.** The Times' digital presence, including its election maps.
- **Who and when.** SND47 World's Best-Designed Digital Presence, results April 2026. Judges said the election maps could become an "industry standard" [snippet, CARRIED as S4].
- **Mechanism.** Not checked on the Times' site.
- **Borrow.** A benchmark for craft, with the limits of a large newsroom budget.
- **Status.** CARRIED, re-searched today on snd.org.
- **URL.** https://snd.org/snd-2026-worlds-best-designed/

### 5.4 Reuters, Sudan famine and the IPC system

- **What it is.** "The world's hunger watchdog warned of catastrophe in Sudan. Famine struck anyway." [snippet, award listing]
- **Who and when.** Reuters. Gold, Humanitarian, Information is Beautiful Awards, 2024 edition [snippet].
- **Mechanism.** CARRIED from the October 20 ledger (C18): the piece explains how the global hunger classification system is meant to work, then shows what happened. That is the shape of every V7 balancing loop: how the correction should work, and where a step failed.
- **Borrow.** "How it should work, then what happened" as the reading order for B1a, B4 and B5.
- **Status.** VERIFIED for the award. Mechanism CARRIED. reuters.com could not be searched.
- **Rights.** Reuters. Study only.
- **URL.** https://www.informationisbeautifulawards.com/news/680-announcing-the-2024-winners

### 5.5 Bloomberg, "What's Really Warming the World?"

- **What it is.** A 2015 explainer that tests each suspected cause of warming against the observed temperature record.
- **Who and when.** Bloomberg, 2015. CARRIED as S19.
- **Mechanism.** One cause at a time against the evidence, with bands for the range of estimates (CARRIED).
- **Borrow.** One loop step at a time against its evidence grade and source, before the loop is shown closed.
- **Status.** CARRIED. A new search on bloomberg.com found no network explainer to add.
- **Rights.** Bloomberg. Study only.
- **URL.** https://www.bloomberg.com/graphics/2015-whats-warming-the-world/

### 5.6 The Pudding, scrollytelling

- **What it is.** The Pudding's method for visual essays where the graphic changes as the reader scrolls.
- **Who and when.** The Pudding's process pages (several years old per the search tool). SND47 Best in Show, micro and small newsrooms, 2026; Information is Beautiful Outstanding Studio, Gold, 2024 edition (CARRIED).
- **Mechanism.** Storyboard first. Visual changes fire at scroll points. The team warns that each step's visual state must be explicit, because readers often skip quickly [snippet, paraphrased].
- **Borrow.** On narrow screens, one loop step per scroll step, each step complete without the one before it.
- **Avoid.** A step that only makes sense if the reader saw the previous one.
- **Status.** VERIFIED, search only.
- **Rights.** The Pudding. Study only.
- **URL.** https://pudding.cool/process/how-to-implement-scrollytelling/ ; https://pudding.cool/process/how-to-make-dope-shit-part-3/

---

## 6. Circuit, wiring and flow diagrams

### 6.1 IEEE 315 and IEC 60617, symbols for electrical diagrams

- **What it is.** Standard symbol sets for electrical and electronic diagrams.
- **Who and when.** IEEE/ANSI 315-1975, whose symbols "have connection points on a modular grid" [snippet, paraphrased]; IEEE lists it as Inactive-Reserved since 2019-11-07 [snippet]. IEC 60617:2026 DB, a database edition published 2026-03-04 [snippet]; the IEC's own pages disagree on its size (more than 1,500 symbols, or about 1,900).
- **Mechanism.** A closed vocabulary on a grid with fixed connection points, so any trained reader can read any drawing.
- **Borrow.** For a circuit direction (Concept 09 The Circuit is a favored concept): fixed connection points on each variable glyph, a grid for every wire, and a closed glyph set for V7's five connection types with one legend.
- **Avoid.** Electrical symbols themselves. A resistor or ground symbol means something specific to an engineer and nothing to most readers. Studio memory, unverified today: schematics mark a joined crossing with a dot and leave a pass-over crossing bare; confirm before adopting.
- **Status.** VERIFIED, search only (standards.ieee.org, iec.ch).
- **Rights.** The standards are paid documents and the IEC database is by subscription. Study only.
- **URL.** https://standards.ieee.org/ieee/315/515/ ; https://webstore.iec.ch/en/publication/2723 ; https://library.iec.ch/iec60617

### 6.2 Howard T. Odum, Energy Systems Language

- **What it is.** A symbol language for drawing ecosystems, economies and regions as energy networks.
- **Who and when.** Howard T. Odum, developed in the 1960s and 1970s [snippet, University of Florida finding aid]. The University of Florida names his 1994 book "Ecological and General Systems" as the main reference [snippet].
- **Mechanism.** One symbol set across very different systems: a source for an outside input, a tank for a storage that acts as a state variable, a heat sink for energy lost, an interaction where flows combine [snippet, paraphrased].
- **Borrow.** V7's outside drivers (X1 to X5) drawn as sources at the boundary, and stocks drawn as containers. V7's glossary already places drivers outside the clusters.
- **Avoid.** The full Odum set. It carries energy meanings V7 does not have.
- **Status.** VERIFIED, search only.
- **Rights.** Study only.
- **URL.** https://cep.ees.ufl.edu/emergy/resources/symbols_diagrams.shtml ; https://findingaids.uflib.ufl.edu/repositories/2/resources/1304

### 6.3 ISO 5807, flowchart symbols

- **What it is.** The international standard for flowchart symbols and conventions.
- **Who and when.** ISO 5807:1985, which replaced ISO 1028 and ISO 2636 of 1973 and remains confirmed [snippet].
- **Mechanism.** Shape names the kind of step, so a decision looks different from a process.
- **Borrow.** For the route-to-change tracker: decisions, vetoes and court challenges as a distinct shape.
- **Avoid.** One arrow style shared by procedure steps and causal links. When the tracker and the map share a page, give the two arrow kinds different heads.
- **Status.** VERIFIED, search only.
- **Rights.** Paid standard. Study only.
- **URL.** https://www.iso.org/standard/11955.html

---

## 7. Isotype and pictogram systems

### 7.1 Isotype

- **What it is.** A method for showing social and economic facts with standardized pictograms.
- **Who and when.** The "Vienna Method of Pictorial Statistics," developed from 1925 at the Social and Economic Museum of Vienna under Otto Neurath; "in 1934 it became known as the ISOTYPE," the International System of Typographic Picture Education [snippet, University of Reading]. Gerd Arntz designed the pictograms, around 4,000 by one account [snippet]. Marie Reidemeister (later Marie Neurath) led the work of "transformation" [snippet]. The Isotype Institute worked in England until 1971 [snippet, paraphrased].
- **Mechanism.** The transformer: a team member whose job is to turn expert material into a picture a lay reader can follow. Counts are shown by repeating one unit.
- **Borrow.** The transformer step for every loop. V7's `how_to_read` sentence is the draft; the card is drawn from it. Repeated units for counts in indexes, such as one mark per loop on a variable that sits on several.
- **Avoid.** Arntz's figures or a pastiche of them.
- **Status.** VERIFIED, search only.
- **Rights.** The Gerd Arntz web archive states: "Any use of any of the images from the website without permission by Pictoright/Gerd Arntz Estate is prohibited" [snippet]. Study only.
- **URL.** https://centaur.reading.ac.uk/16340/1/IDJ-Burke2010.pdf ; https://collections.reading.ac.uk/special-collections/collections/marie-neurath-collection/ ; https://www.gerdarntz.org/content/copyright.html

### 7.2 Otl Aicher, Munich 1972 pictograms

- **What it is.** The sports and wayfinding pictograms for the 1972 Munich Olympics.
- **Who and when.** Otl Aicher and his team, 1972. The Olympic Studies reference document describes figures built on a square grid with lines at 45 or 90 degrees [snippet, paraphrased]. ERCO describes "a syntax with strict design rules" in place of isolated icons [snippet, paraphrased].
- **Mechanism.** A grammar. Parts combine under fixed rules, so the set can grow without losing its look.
- **Borrow.** Build every variable-type and connection-type glyph from one grid, so V7.1 can add glyphs that match.
- **Avoid.** Aicher figures or close imitations.
- **Status.** VERIFIED, search only (olympics.com, ERCO).
- **Rights.** ERCO says it holds the worldwide licensing for the system [snippet, paraphrased]. Study only.
- **URL.** https://stillmed.olympics.com/media/Document%20Library/OlympicOrg/Factsheets-Reference-Documents/Games/Pictograms/Reference-document-The-Sports-Pictograms-of-the-OG.pdf ; https://press.erco.com/en_us/press-release/company/pictograms-quickly-comprehended-easily-interpreted-immediately-understood_2403

### 7.3 AIGA and the U.S. Department of Transportation, Symbol Signs

- **What it is.** A public set of 50 passenger and pedestrian symbols.
- **Who and when.** AIGA for the U.S. Department of Transportation. 34 symbols in 1974, which received one of the first Presidential Design Awards, and 16 more in 1979 [snippet].
- **Mechanism.** A set designed and tested for strangers moving fast.
- **Borrow.** The habit of testing glyphs with first-time readers before locking them.
- **Avoid.** Using the set inside the atlas. The Master Brief requires authored vectors for Oath & Action's own symbols.
- **Status.** VERIFIED, search only.
- **Rights.** AIGA calls them "copyright-free symbols" [snippet]. Check AIGA's download terms before any use.
- **URL.** https://www.aiga.org/resources/symbol-signs

### 7.4 Lance Wyman, Mexico City Metro graphics

- **What it is.** The logo, icons and wayfinding signs for the Mexico City Metro.
- **Who and when.** Lance Wyman. His site dates the project to 1968 [snippet].
- **Mechanism.** Studio memory, unverified today: each station carries its own pictogram, so riders who cannot read a name can still find a stop.
- **Borrow.** If confirmed, a reason to give each loop a small identifying mark in the index, drawn from the existing topic icon family.
- **Avoid.** 51 unique variable icons. No reader will learn them.
- **Status.** PARTLY. The site confirms the project and its scope, and did not describe the icons.
- **Rights.** Study only.
- **URL.** https://lancewyman.com/brand-project/mexico-city-metro-system-graphics/

---

## 8. Food webs and ecology diagrams

### 8.1 Summerhayes and Elton, Bear Island food web

- **What it is.** An early drawn food web, a diagram of which organisms feed on which.
- **Who and when.** V. S. Summerhayes and Charles Elton, "Contributions to the ecology of Spitsbergen and Bear Island," Journal of Ecology 11, 1923 [snippet, cited by later Journal of Animal Ecology papers]. Citing papers disagree on the last page (286 or 287).
- **Mechanism.** One arrow meaning across a whole picture.
- **Borrow.** A single arrow meaning on each V7 view. Connection type changes the line, and the arrow always means "changes."
- **Status.** PARTLY. The paper itself did not appear in results.
- **URL.** https://besjournals.onlinelibrary.wiley.com/doi/10.1111/j.0021-8790.2004.00829.x

### 8.2 U.S. National Park Service, Yellowstone trophic cascade

- **What it is.** Park explainers on how wolves may affect elk, and through elk, willow and aspen.
- **Who and when.** National Park Service, Yellowstone. Undated pages.
- **Mechanism.** An indirect chain of three links, shown with its scientific dispute in view. The Park Service states that "not all scientists agree that this relationship is causal" [snippet] and names rival explanations such as groundwater and the loss of beavers [snippet, paraphrased].
- **Borrow.** V7's seven plausible_contested connections and seven contested flags: draw the contested link with both readings, and print the rival explanation beside the line.
- **Avoid.** A tidy chain drawn as settled. A preprint argues sampling bias exaggerated this textbook example (bioRxiv preprint, outside the official domains).
- **Status.** VERIFIED, search only.
- **Rights.** Federal pages; image credits vary and were not checked. Study only.
- **URL.** https://www.nps.gov/articles/the-big-scientific-debate-trophic-cascades.htm ; https://www.nps.gov/places/000/lamar-valley-trophic-cascades.htm

---

## 9. Recent award-winning work

| Award | Work and maker | Mechanism worth studying | Status | URL |
|---|---|---|---|---|
| Information is Beautiful Awards, 2024 edition (Data Visualization Society; most recent; DVS says the awards resume in 2027, CARRIED) | "Zoonotic Web," Liuhuaying Yang. Gold, Science, Technology and Health; Yang also won Gold, Impressive Individual [snippet] | A network of disease links between species, judging by the title. Results did not describe the work, so its mechanism is unknown | VERIFIED for the award. Content UNVERIFIED | https://www.informationisbeautifulawards.com/news/680-announcing-the-2024-winners |
| Information is Beautiful Awards, 2024 edition | "I Want a Better Catastrophe: A Flowchart for Navigating our Climate Predicament," University of Applied Sciences Potsdam: Andrew Boyd (book and original flowchart), Jona Pomerance (design and development), Marian Dörk (research supervision). Gold [snippet] | A narrated path through a branching chart: audio guides the reader along one route, and the reader can leave it [snippet, paraphrased]. A model for a guided tour of the whole map | VERIFIED. Category conflict: the showcase page lists Places, Spaces and Environment, and a search summary named People, Language and Identity | https://www.informationisbeautifulawards.com/showcase/7487-i-want-a-better-catastrophe-a-flowchart-for-navigating-our-climate-predicament |
| Information is Beautiful Awards, 2024 edition | Reuters, Sudan famine and IPC. Gold, Humanitarian. The Pudding, Gold, Outstanding Studio (CARRIED) | See 5.4 and 5.6 | VERIFIED | https://www.informationisbeautifulawards.com/news/680-announcing-the-2024-winners |
| Information is Beautiful Awards, 2023 entry | "Depicting the Need for Systems Change," Graphicacy (Carni Klirs, data visualization design) for the Systems Change Lab of the World Resources Institute, the Bezos Earth Fund and partners; launched at COP27. Longlist and shortlist [snippet] | Progress tracking across many system shifts on one platform. Mechanism not described in results | VERIFIED for the entry. Longlist and shortlist only | https://www.informationisbeautifulawards.com/showcase/6544-depicting-the-need-for-systems-change |
| SND47, 2026 (Society for News Design) | The New York Times, World's Best-Designed Digital Presence; The Pudding and The Washington Post, Best in Show; Tyler Remmel (The Washington Post), World's Best Designer [snippet] | Editorial craft benchmark | VERIFIED, re-searched today | https://snd.org/snd-2026-worlds-best-designed/ ; https://snd.org/snd-2026-worlds-best-designers/ |
| Royal Statistical Society, 2021 | Financial Times pandemic data coverage (see 3.2) | Shared frames across many places | VERIFIED for the award | https://rss.org.uk/news-publication/news-publications/2021/general-news/statistical-excellence-in-journalism-awards-2021-w/ |
| IEEE InfoVis Test of Time, 2016 | Danny Holten, hierarchical edge bundles (see 4.3) | Bundled overview | VERIFIED | https://www.tue.nl/en/mathematics-and-computer-science/news-1/08-11-2016-danny-holten-receives-infovis-test-of-time-award |
| Cannes Lions, Webby, Fast Company, TIME, 2021 | MTA Live Subway Map, Work & Co (see 2.3) | Status drawn on the line | VERIFIED | https://www.mta.info/press-release/mta-live-subway-map-wins-prestigious-gold-lion-cannes |
| Cooper Hewitt National Design Awards, 2026 | Laura Kurgan, Digital Design (CARRIED as S1) | Civic spatial data | CARRIED | https://www.cooperhewitt.org/national-design-awards/2026-national-design-award-winners/ |
| Malofiej | No 2025 or 2026 edition found. A search of malofiejgraphics.com on October 28, 2026 returned only older editions (Malofiej 23 and 26 PDFs and earlier calls for entries) | None to cite | Matches the brief's rule: do not cite as current | https://www.malofiejgraphics.com/documents/24144149/42535971/malofiej-26.pdf |

---

## Ten ideas for 23 loops and a 51-variable map, ranked

Ranked by how much each helps a first-time reader see a loop, and how directly it fits V7's data. Each idea names its sources by entry number.

1. **One loop, one card, one geometry.** Draw every loop on the same ring: step 1 at twelve o'clock, clockwise, evenly spaced stops, the R or B mark and the loop title at the center, the reference-mode line in a fixed corner. Two-, three- and four-step loops (11, 5 and 4 of them) differ only in the number of stops. The three conceptual loops keep the frame and state "no complete numbered chain" in words. A reader who learns one card can read all 23, and the ring alone says "this comes back around." Sources: 1.3, 1.8, 2.4, 2.5, 3.1. Fits every direction.

2. **Step through one numbered link at a time.** Reveal variable, link, next variable, until the loop closes and its mark appears. Give play, pause, step back and reset, and stop after one full turn. For print and reduced motion, show the same build as a strip of small frames. Sources: 1.6, 1.8 (presentations), 1.9, 5.5, 5.6. Fits loop cards and any interactive view.

3. **A fixed, rule-based position for every variable.** Place the 51 variables by a rule a reader can hear in one sentence: regions as fixed zones on a 0, 45 and 90 degree grid, drivers at the boundary, economy and technology as their own bands. Keep each variable in the same place on every view, so a reader learns the map once. Sources: 2.1, 2.4, 4.5, 4.8. This is the main defense against pitfall 1.

4. **Loops as lines, shared variables as interchanges.** On the whole map, draw each closed loop as a route through its variables, with parallel lines where loops share a connection (six do; L42 carries three) and an interchange mark where a variable sits on several loops (E1 on seven). The transit form suits V7 because a loop is a route that returns to its start. Twenty colors will not separate, so draw loop lines in one neutral tone, light the chosen loop, and label every line with its ID in a loop-shaped badge. Sources: 2.1, 2.2, 2.5. Fits a transit direction; a circuit direction can use the same rule with wires.

5. **Focus with context.** Light one loop or one variable and mute the rest, then widen by one step at a time. The muted map stays visible so the reader keeps orientation. Sources: 1.8 (Showcase, Focus), 2.3 (faded sections), 4.3 (hover). Fits the whole-system map in every direction.

6. **Evidence and delay carried by line pattern and marks.** Line pattern carries the V7 grade (V7 draws hypotheses dotted and plausible links dashed). A separate mark carries delay, such as one, two or three ticks across the line for S, M and L, so delay and evidence never share a channel. Call out each loop's weakest step in words, for example R1's L02 (plausible) and R10's C3 to C4. Contested links show both readings. Sources: 1.3, 1.9, 2.3, 8.2; Master Brief V2 section 14. Fits every direction and survives grayscale.

7. **Structure beside behavior.** Pair each loop card with its `reference_mode` series as a small sourced line chart, so the reader sees the loop's footprint in the record. Draw stocks with their own shape so readers stop matching a stock's curve to its inflow. Sources: 1.1, 1.4, 1.7. Fits loop cards and the evidence view.

8. **A matrix companion for the whole system.** A 51 by 51 grid sorted by region shows all 118 connections with no crossings, makes the 81 cross-region connections visible as off-diagonal blocks, and serves as the screen reader table. Use it to answer "what connects to what," and use the drawn map to follow a path. Sources: 4.4, 4.6, 4.2 (as a region-level summary). Fits a register direction.

9. **Predict, then run.** Before a loop plays, ask the reader which way the starting variable moves after one full turn. Then run it, and show the evidence for each step. For reforms, let the reader choose a reform and see its targets light on the map with ordinal effects and routes, assumptions one step away, and no total. Sources: 1.5, 1.10, 5.1, 5.5.

10. **A small glyph grammar on one grid, written by a transformer.** Variable types (stock, flow, auxiliary, driver) and connection types (causal, money, information, authority, ownership) each get one glyph from one construction grid, explained in one legend. Before any card is drawn, a writer turns the loop's `how_to_read` sentence into the card's caption. Sources: 6.1, 6.2, 7.1, 7.2, 7.3.

---

## Pitfalls to design against

1. **The hairball.** A force-directed drawing of all 118 connections. Hive plot authors call such layouts "hairballs" (4.5); Foresight's own blog records criticism of its map's complexity (1.12). Use idea 3.
2. **Every loop in one picture.** Sterman's chapter 5 warns against "putting all the loops into one large diagram" (1.3). The whole map orients; the cards teach.
3. **Flow forms for feedback.** A Sankey needs a directed acyclic network (4.7), and FT's flow family assumes measured volumes (3.2). A loop is a cycle, and V7 links carry no measured amounts. Width may encode only a defined count with a legend.
4. **Plus read as good.** V7: a plus sign "can mark a harmful effect." Green and red for signs teaches the wrong reading, and red with blue reads as partisan (Master Brief V2 section 13). Print the sign and a reading rule.
5. **Color as the only code.** Twenty closed loops cannot each own a hue, and grade, delay and status must survive grayscale. Use pattern, marks and labels (idea 6).
6. **Implied precision.** Animated pulses, sliders and smooth curves suggest rates and magnitudes V7 does not estimate. Stop pulses after one turn, keep effects ordinal, never sum them, and label any toy as "Illustration" (1.5, 1.9, 5.1).
7. **Contested drawn as settled.** The trophic cascade shows how a tidy chain hides a live dispute (8.2). Show both readings on V7's contested links.
8. **Closure overstated.** B2, B3 and R9 have no numbered chain; R2 and R16 close through a hypothesized step. Draw them in the same frame as an open ring, with their status written in.
9. **Authority closing a loop.** V7's seven authority connections have no sign and never close a loop. Give them their own line and keep them off loop rings.
10. **Abstraction with no anchor.** The 1972 Vignelli diagram was replaced after criticism (2.2). Every V7 variable needs its everyday title and its `increase_means` sentence one tap away.
11. **Identifier collisions.** B2, B3, B4 and B5 name both a variable and a loop. Loop IDs need a visibly different badge from variable IDs on every view.
12. **Bundles for tracing.** Edge bundles merge lines and hide which link goes where (4.3). Use bundling for overview only.
13. **Sandbox first.** Case warns that open free play overwhelms a learner (1.10). Open on one two-step loop.
14. **Scroll states that need the previous step.** Readers skip (5.6). Each step must stand alone.
15. **Borrowed identity.** The Tube diagram's look, Aicher's figures and Arntz's pictograms belong to their owners (2.1, 7.1, 7.2). Learn the rule and draw Oath & Action's own.

---

## Rights positions

| Reference | Rights position found | What the studio may do |
|---|---|---|
| Meadows texts and figures | Rights holder not checked | Study only |
| Sterman text and MIT course material | Not checked | Study only |
| Kumu interface and user maps | Owned by Kumu and map authors | Study only |
| LOOPY | Open source and public domain [snippet] | The tool may be studied and used to sketch; other people's models stay theirs; ship nothing traced from it |
| Stella, Climate Interactive, The Systems Thinker | Not checked | Study only |
| Foresight obesity map | UK Crown copyright; license not checked | Study only |
| Tube diagram, roundel, Johnston | TfL brand IP; TfL publishes third-party guidance (not read) | Study only |
| Vignelli diagram; MTA maps | MoMA collection; MTA | Study only |
| INAT and Art. Lebedev maps | Makers' work | Study only |
| Tufte books and Minard reproductions | Graphics Press; scan rights not checked | Study only |
| Circos, hive plot, BioFabric, Holten, Wattenberg figures | Journal and maker rights not checked | Study only |
| D3 examples on Observable | Code license not checked today | Study only until checked |
| LLNL energy flow charts | Federal laboratory; terms not checked | Study only until checked |
| Atlas of Economic Complexity | Harvard Growth Lab | Study only |
| Newsroom graphics (Washington Post, New York Times, Reuters, Bloomberg, The Pudding, FT) | Publishers' rights. FT templates carry an MIT license that excludes FT content and branding | Study only |
| IEEE 315, IEC 60617, ISO 5807 | Paid standards; IEC database by subscription | Study only |
| Odum symbols | Not checked | Study only |
| Gerd Arntz and Isotype pictograms | Use without permission of Pictoright or the Gerd Arntz Estate is prohibited [snippet] | Study only |
| Aicher pictograms | ERCO holds worldwide licensing [snippet] | Study only |
| AIGA and DOT Symbol Signs | "Copyright-free" per AIGA [snippet] | Usable after checking AIGA's download terms; the atlas still needs authored vectors |
| Lance Wyman Metro graphics | Maker's work | Study only |
| NPS pages | Federal; image credits vary, not checked | Study only |
| Award entries | Entrants' rights | Study only |
| Supplied references already in the rights ledger, such as data-viz-09, data-viz-13 and data-viz-51 (Leyla Acaroglu system diagrams) and data-viz-76 (Tudor networks graph) | Third-party screenshots | Study only, per `work/research/20261020_Rights-Ledger.md` |

---

## What I verified and what I could not

### Verified on October 28, 2026 (search only, official or maker domains)

- Meadows' stock-and-flow notation and the Leverage Points essay on donellameadows.org.
- Sterman's chapter 5 rules and the Bathtub Dynamics paper on MIT domains.
- Climate Interactive's bathtub framing; isee systems' storytelling guidance; The Systems Thinker's behavior-over-time guidance.
- Kumu's loop, Focus, Showcase and presentation features.
- LOOPY's release month, drawing rules and public domain status; Nicky Case's design patterns and "Crowds."
- Bret Victor's essay and date.
- The Foresight project, its seven themes and its core-engine structure, and the blog's line on complexity.
- Beck's dates, angle rule, ticks and circuit-diagram basis; the 1933 spoof circuit print.
- The Vignelli diagram's credits and dates at MoMA; the MTA's April 2, 2025 redesign; the Live Subway Map's partners, behavior and awards.
- INAT's line standard; Art. Lebedev's circle-line rules.
- Tufte's book contents and Minard description; the FT Visual Vocabulary flow family and the RSS 2021 award.
- Citations for Wattenberg, Circos, Holten (and the 2016 award), Ghoniem and colleagues, hive plots and BioFabric; Bostock's matrix; the D3 Sankey module's scope; LLNL's flow charts; Sankey's 1898 ICE record.
- The Growth Lab's Product Space structure.
- The Washington Post simulator's author and date.
- IEEE 315 status; IEC 60617:2026 DB; ISO 5807.
- Odum's language on University of Florida pages.
- Isotype history at Reading; the Arntz copyright notice; Aicher's grid and ERCO's licensing; AIGA Symbol Signs' history and terms; Wyman's 1968 project date.
- NPS trophic cascade pages and their stated dispute.
- IIB 2024 Golds for "Zoonotic Web" and "I Want a Better Catastrophe"; the Graphicacy 2023 shortlist; SND47 winners; no Malofiej edition after the older ones found.
- All Atlas V7 counts in this brief, read from the extracted JSON.

### Could not verify

- Any page content beyond search summaries. No page was opened.
- Every [snippet] as an exact quotation. Each needs a page read before printing.
- New York Times, Financial Times and Reuters pages: the search tool refused those domains. The mechanics of "512 Paths to the White House," the FT trajectory charts and the Reuters IPC piece rest on carried rows, makers' sites or studio memory.
- The publication date of "Thinking in Systems" (not in today's results).
- The Foresight map's 108 variables and 304 links, and its October 17, 2007 date (the stating page was not pinned).
- Art. Lebedev's map 2.0 date of 2013.
- The 84 percent figure from the later MIT accumulation study, beyond a search summary.
- The 2004 matrix study's findings, which reached me through secondary papers.
- The Product Space layout history, which came from a secondary paper.
- The schematic junction-dot convention (studio memory).
- Lance Wyman's one-pictogram-per-station mechanism (studio memory).
- The content of "Zoonotic Web," and the correct IIB category for "I Want a Better Catastrophe."
- The Summerhayes and Elton paper itself, and the contents of Sankey's 1898 plate.
- The meaning of V7's `spine` flag.
- License terms for LLNL charts, D3 examples, Crown copyright maps and NPS images.
- A PowerPoint slide on Afghanistan strategy that is often cited as a hairball (studio memory): not checked, because the newsroom that reported it could not be searched. Left out of the entries.

---

## Change log

- Created: `work/research/20261028_Systems-Map-References.md`.
- Modified: none. No ledger was written, and nothing in `source/` was touched.
