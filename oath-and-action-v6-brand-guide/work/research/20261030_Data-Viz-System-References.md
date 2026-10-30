# Data Visualization System References

Reference brief for the data visualization lead and the main session, Oath & Action Edition 06. Written on October 30, 2026 by the research lead.

Dustin wrote on October 30: "i also want a cool oath & action brand system for data visualizations, charts, graphs, maps, tables, and displaying data different ways." He sent four links and three images and asked the studio to pay particular attention to The New York Times. This brief studies each system and turns what it teaches into rules for Master Brief V2 section 13 (selection guide, specimens, palettes, complex examples). Decision DR-22 places the system itself in Phase 3 under its own plan, so nothing here is approved design. The brief writes to no ledger; section 7 holds rights rows for the main session to add.

## How this was checked

- Pages were fetched on October 30, 2026 through the session proxy with curl and WebFetch, turned into text with a small script, and quoted from that text. Slide images were viewed directly. Captures were taken with a headless Chromium browser at 1,440 by 900 px.
- **The New York Times.** No nytimes.com page was requested. The capture script refused any nytimes.com address and blocked requests to that domain from inside other pages. Links to Times articles on other sites were not followed. Every Times observation comes from one of four places: the Jalbert-Gagnier case study's slides, the Times's public ai2html repository, public writing by people who have worked on the Times graphics desk, and Times charts as Datawrapper reproduces them on its own blog.
- **Status tags.** [READ]: I opened the page or file and saw the claim myself. [REPRO]: I saw a Times chart as a third party reproduces it; the image may be cropped or older than the live graphic. [SECOND]: a third party describes the practice and I did not see the Times's own statement. [UNVERIFIED]: no source I could read.
- **One measurement.** A script computed OKLCH lightness and chroma and WCAG contrast for the seven locked colors. OKLCH is a color space in which equal steps look equal; L is lightness from 0 to 1, C is chroma (colorfulness). Results appear where they bear on a rule.

## 1. Sources read

All rows were read on 2026-10-30.

| ID | URL | What it covered |
|---|---|---|
| S01 | https://www.jalbertgagnier.com/work/the-new-york-times | Case study credited to the agency Objective Subject, with David Jalbert-Gagnier as creative director: a Times brand book, type "personalities", Times Journeys, School of The New York Times |
| S02 | https://www.jalbertgagnier.com/wp-content/uploads/2021/05/ (files Principles-Introwhite.svg, Principles-1 to 4, Type-Introwhite.svg, Type-A and Type-B@2x.png, Guidelines-Type, -Colors and -Visual@2x.png) | The case study's slides: four brand principles, NYT Franklin weights, core colors, an illustration page with a Times party-control map. Slide footers name the book "Working with The New York Times Brand" and "Brand Tools" |
| S03 | https://github.com/newsdev/ai2html (README.md, examples/nyt.md, ai2html.js read as raw files) | The Times's open-source Illustrator-to-HTML script; its font table maps NYT Franklin, NYT Cheltenham and other Times faces |
| S04 | http://ai2html.org/ | ai2html documentation: why text is rendered as HTML, artboards, breakpoints |
| S05 | https://github.com/archietse/malofiej-2016 (cloned read-only; tse-malofiej-2016-slides.pdf and ai2html-demo) | Archie Tse, Deputy Graphics Director at the Times, "Why We Are Doing Fewer Interactives", Malofiej 2016 |
| S06 | https://github.com/1wheel/swoopy-drag and http://1wheel.github.io/swoopy-drag/ | Adam Pearce's annotation tool for d3, headed by a quotation credited to Amanda Cox |
| S07 | https://www.vis4.net/blog/in-defense-of-interactive-graphics/ | Gregor Aisch, March 31, 2017, on tooltips and buttons in Times graphics he worked on |
| S08 | https://nightingaledvs.com/interview-with-graphics-editor-marco-hernandez/ | Interview with Times graphics editor Marco Hernandez, April 25, 2023 |
| S09 | https://www.datawrapper.de/blog/text-in-data-visualizations | Lisa Charlotte Muth, September 28, 2022; reproduces three Times charts (2015 Arctic ice, 2018 immigration and crime, 2022 jobs) |
| S10 | https://www.datawrapper.de/blog/colors-for-data-vis-style-guides | Muth, March 30, 2022; Times color practice, Economist palette, a Times hue wheel |
| S11 | https://www.datawrapper.de/blog/emphasize-with-color-in-data-visualizations | Muth, July 24, 2023; reproduces a 2022 Times heat map and Derek Watkins's 2015 Arctic chart |
| S12 | https://carbondesignsystem.com/building-blocks/data-visualization/overview (the old getting-started address redirects here) | Carbon chart catalogue |
| S13 | .../data-visualization/chart-anatomy | Titles, legends, tooltips, frames, circular charts, big numbers |
| S14 | .../data-visualization/axes-and-labels | Zero baselines, data gaps, axis breaks, time series |
| S15 | .../data-visualization/color-palettes | Categorical, sequential, diverging, alert palettes; gradients |
| S16 | .../data-visualization/legends | Legend use, position, hover and click behavior, mobile |
| S17 | .../data-visualization/dashboards | Presentation and exploration dashboards |
| S18 | .../data-visualization/simple-charts, flow-charts, gantt-charts, spatial-charts | Chart types; heat maps, tree maps, choropleths, cartograms, Mapbox themes |
| S19 | https://carbondesignsystem.com/building-blocks/foundations/accessibility/overview | Carbon accessibility overview (no chart-specific guidance) |
| S20 | https://www.bbc.co.uk/gel and its Guidelines, Foundations, Design Patterns, How-tos and Articles indexes | GEL site map; no chart or color foundation beyond the pages below |
| S21 | https://www.bbc.co.uk/gel/features/how-to-design-infographics | BBC infographics guide, published 28 April 2016 |
| S22 | https://www.bbc.co.uk/gel/features/complex-images | Text descriptions for charts, maps and infographics, 30 May 2024 |
| S23 | https://www.bbc.co.uk/gel/features/typography | BBC Reith type scale, updated 7 August 2017 |
| S24 | https://www.bbc.co.uk/gel/features/iconography, /grid, /spacing-units, /how-to-design-for-accessibility, /how-to-write-text-descriptions-alt-text | Icons, grid, spacing, accessibility principles; no chart rules |
| S25 | https://www.bbc.co.uk/accessibility/forproducts/guides/mobile/colour-and-meaning/ and /colour-contrast/ | BBC Mobile Accessibility Guidelines on color |
| S26 | https://github.com/bbc/bbplot (README.md, R/bbc_style.R, R/finalise_plot.R, chart_examples/bbplot_example_plots.png) | The BBC News data team's ggplot2 style |
| S27 | https://bbc.github.io/rcookbook/ | BBC Visual and Data Journalism cookbook for R, last updated 2019-01-24 |
| S28 | https://ourworldindata.org/redesigning-our-interactive-data-visualizations | OWID Grapher redesign, October 18, 2023, by Marwa Boukarim, Christian Swinehart and Sophia Mersmann |
| S29 | https://ourworldindata.org/grapher/life-expectancy (data page text, and chart, map and table views in the browser) | A live OWID chart, its sources block, citation and download options |
| S30 | https://design-system.economist.com/ (page data for Brand and marketing) and https://design-system.economist.com/documents/MAPstyleguide_20170505.pdf | The Economist design system's chart and map links; "The Economist maps styleguide", version 1.2, updated 5 May 2017 |
| S31 | `work/research/chat-references/data-viz/` (three images) | Navy and teal chart collage; Vanzyst "utilitarian" asset pack; Economist chart montage |

**Pages I could not read**

- Every nytimes.com page, including https://www.nytimes.com/spotlight/graphics and the Times articles that S03, S09, S10 and S11 link to. Not requested, by rule.
- https://www.niemanlab.org/2016/03/at-the-malofiej-infographics-world-summit-the-best-form-of-storytelling-is-often-static/ returned HTTP 403 to curl and to WebFetch. I did not try the Nieman Lab interview with Times graphics director Steve Duenes after that refusal.
- The Economist's chart guide, https://design-system.economist.com/documents/CHARTstyleguide_20170505.pdf, listed as "The Economist: visual styleguide (May 2017)". The address returns the site's HTML shell, so the file is no longer served there.
- Sarah Leo, "Mistakes, we've drawn a few", https://medium.economist.com/mistakes-weve-drawn-a-few-8cdd8a42d368. The connection was reset and WebFetch refused the host.
- Carbon's data visualization accessibility page, which the legends page cites for "approved textures". https://carbondesignsystem.com/building-blocks/data-visualization/accessibility returns 404.
- GitHub organization listings for newsdev and nytimes. The session's GitHub policy refused them (HTTP 403), and I did not pursue them further.
- The BBC GEL infographic asset file (Ai, 2.3 MB), which holds the BBC infographic palettes. Not downloaded.
- ai2html.org over HTTPS for a capture (HTTP 502). Its text was read over HTTP.

## 2. Each system in turn

### 2.1 The New York Times

**Overall character.** The brand book pages in the case study name four principles: Simplicity, Hierarchy, Focus and Quality [READ, S02]. Hierarchy reads: "Elegant compositions are created with clear visual hierarchy, relaxed pacing of content and generous use of white space." The case study says the book serves Times staff, marketers, designers and advertisers (S01); I found nothing that ties it to the graphics desk. Lisa Charlotte Muth quotes Stuart Thompson, head of visual journalism at Times Opinion: "At The New York Times, the only guidelines/rules I've ever seen are 'Is it Timesian?'" (https://www.datawrapper.de/blog/colors-for-data-vis-style-guides) [SECOND]. Marco Hernandez describes working from "a basic template, a set of basic building blocks" and says "Beauty in a vacuum is a waste of time, my time." (S08) [READ].

**Titles and annotation.** The 2022 jobs chart opens with a sentence that states the finding, "Payrolls have fully recovered the jobs lost in the pandemic.", in a bold serif, with a gray serif subtitle naming the measure [REPRO, S09]. The 2022 heat map uses a headline in title case, "Where Thursday's Forecast Temperatures Are Warmer Than Normal" [REPRO, S11]. Annotation lives inside the plot. Derek Watkins's 2015 Arctic ice chart explains its own encoding ("Each line represents one yearly cycle of sea ice fluctuations"), marks the 2012 record ("Arctic ice extent reached the lowest point on record") and gives the axis a reader's scale ("Size of Canada", "Size of Alaska") [REPRO, S11]. Adam Pearce's d3 annotation tool opens with "The annotation layer is the most important thing we do", credited to Amanda Cox (https://github.com/1wheel/swoopy-drag) [READ; the original venue of the quotation is UNVERIFIED]. The tool hand-places labels and leader lines, and its documentation suggests a separate set of annotations for narrow screens [READ, S06].

**Direct labels and legends.** The jobs chart labels its end point in bold, "+32,000 jobs since Feb. 2020", and its start, "152.5 million jobs in February 2020" [REPRO]. The Arctic chart labels its teal series in teal text inside the plot [REPRO]. The immigration scatter names directions with arrows in bold black ("← Fewer | More immigrants →", "↑ More crime", "↓ Less crime") and labels only two cities among more than a hundred dots [REPRO, S09]. The heat map carries a stepped legend bar under its subtitle, with a signed scale from "-20°F" to "+15°" [REPRO]. None of the five reproductions has a legend box.

**Gridlines and axes.** Gridlines are thin and pale. Tick labels are light gray, and the unit appears once, on the top or last tick: "18 million sq. km", "+500 violent crimes per 100,000 people", "+20,000 immigrants per 100,000 people" [REPRO]. The jobs chart prints "−5 mil." with a minus sign wider than a hyphen; the image cannot show which character it is [REPRO]. No chart has an axis title.

**Type.** ai2html's font table maps NYT Franklin (sans serif) and NYT Cheltenham (serif) for web output, alongside other Times faces [READ, S03]. In the reproductions, titles are a bold serif and every label is a sans serif; by eye these match Cheltenham and Franklin [REPRO; identification UNVERIFIED]. The brand book: "NYT Franklin is clear and objective, and makes the point with ease and purpose." [READ, S02]. Muth captions six 2021 Times charts: "The visualizations all use different colors, but are held together by the title font Cheltenham." [SECOND, S10].

**Color.** The brand book: "Our core ‘colors’ are Black, and White." and "Additional colors may play a supporting role, if used judiciously." [READ, S02; several hex values on that slide repeat across different swatches, so its numbers are unreliable]. In charts, the Arctic piece draws every past year in light gray, five recent years in teal and 2015 as a thick black line [REPRO]. The heat map runs one-sided: cooler areas stay in grays and only warmer areas take red [REPRO]. The immigration scatter diverges from pink to green [REPRO]. Muth reports that the Times used one red and one blue throughout its 2020 election reporting [SECOND, S10]. The case study's illustration page shows a Times map, "Holding a Monopoly", of states where one party holds the legislature and the governorship, in Democratic blue and Republican red [READ, S02].

**Small multiples and tables.** [UNVERIFIED]. No source I read shows a Times small multiple or table.

**Maps.** The heat map uses stepped bins, gray base geography and state labels as gray abbreviations ("MONT.", "N.D.") [REPRO]. The research ledger carries an SND47 search snippet in which judges call the Times's election maps an "industry standard" (row S4 of `work/research/20261021_Research-Ledger.md`) [SECOND, carried].

**Mobile.** ai2html.org explains the tool: "By rendering the text as html, we can scale the “graphic” up and down, but keep the text readable at the same font-size and line-height." It does this to reduce "the number of versions of the artwork" across "mobile phones up to giant desktop monitors" [READ, S04]. Each artboard can carry a minimum width as its breakpoint, and Tse's demo ships three artboards at 1,440, 900 and 600 px [READ, S05]. Hernandez: "not everything should be multi platform" [READ, S08]. Whether Times charts stack panels vertically on phones is [UNVERIFIED].

**Interaction and tooltips.** Tse's 2016 slides give "3 rules for visual storytelling (2016 edition)". Rule 1: "If you make the reader click or do anything other than scroll, something spectacular has to happen." Rule 2: "If you make a tooltip or rollover, assume no one will ever see it. If content is important for readers to see, don’t hide it." The slides add "Most visuals are static." and "If animation or motion is needed, try to trigger it when user scrolls." [READ, S05]. Aisch answers a year later that the widely quoted 85 percent figure measured readers who did not click one button, and that "All it means is that you should not hide important content behind interactions." He reports that tooltips on a European election graphic drew readers who fact-checked party labels and led to corrections [READ, S07].

**Accessibility and source lines.** [UNVERIFIED]. The reproductions are cropped above any source line, and no Times source I read covers accessibility.

### 2.2 Carbon (IBM)

Carbon is a product design system for dashboards inside software, and every page calls its guidance "a work in progress" [READ, S13 to S18].

- **Titles, labels, legends.** A title should be "descriptive and qualitative" and state the main insight (S13). "When possible, avoid using a legend and label data representations directly." (https://carbondesignsystem.com/building-blocks/data-visualization/legends). Legends sit at the bottom by default, dim other categories to 30 percent opacity on hover and isolate one on click (S16).
- **Axes.** Bars and areas start at zero; lines may crop. "Never interpolate between periods when data is unavailable." A new day, month or year gets a semibold "landmark" tick label (S14).
- **Color.** A 14-color categorical sequence used "strictly" in order, including two reds; single-hue sequential scales of ten steps; diverging red to cyan for temperature and purple to teal otherwise (S15). "Please note that the 3:1 minimum contrast requirement does not apply to heat maps." (S18).
- **Small multiples, tables, maps.** No small multiples; exploration dashboards link charts instead (S17). Tables appear only as the fallback for pie slices under 1 degree (S13). Choropleths, symbol maps and cartograms are design-only, with four Mapbox themes (S18).
- **Mobile, tooltips, accessibility.** Legends stack or hide behind "View legends" (S16). "A tooltip should repeat the corresponding values of the data point on both axes and any other relevant details." (S13). Texture can support color (S16), but the texture page returns 404. Source lines are not covered.

### 2.3 BBC GEL, the Mobile Accessibility Guidelines and bbplot

- **Character.** "Our overall visual style is minimal and visually engaging but with a neutral tone." (https://www.bbc.co.uk/gel/features/how-to-design-infographics) [READ].
- **Type and labels.** BBC Reith throughout: titles in Great Primer, labels in Pica, source in Brevier (S21), which on desktop measure 20/24, 16/20 and 13/16 px (S23). bbplot sets a 28-point bold title in #222222, drops axis titles, ticks and axis lines, and puts any legend at the top without a title (S26). The cookbook: "Remove the legend to become one - it’s better to label data directly with text annotations." (https://bbc.github.io/rcookbook/) [READ].
- **Gridlines.** Horizontal gridlines only, in #cbcbcb, over a #333333 baseline at zero, which the cookbook calls "our design style" (S27).
- **Color.** "Use a neutral colour palette so important information stands out more in comparison." (S21). The bbplot example sheet colors parties by convention: Democrat blue, Republican red, Conservative blue, Labour red [READ, S26].
- **Small multiples.** "It’s always best to use the same y axis scale across small multiples, to avoid misleading" (S27).
- **Mobile.** Graphics are drawn at 400, 750 and 976 px. "Small (mobile) is presented as a vertical stack while medium (tablet) and large (desktop) have a more horizontal layout." (S21).
- **Accessibility.** "Information or meaning must not be conveyed by colour only." (S25). For charts and maps, "The text description must provide all the information available to a sighted reader." Designers write a suggested description for each graphic; long ones move into the article, a list or an HTML table, and the note and source must be equally accessible (https://www.bbc.co.uk/gel/features/complex-images) [READ].
- **Source lines.** finalise_plot draws a full-width rule with "Source: ..." at bottom left and the BBC blocks at bottom right (S26). Maps get "labels, keys and scales" (S21). Interaction is not covered.

### 2.4 Our World in Data

- **Views.** Chart, map and table views switch by buttons at upper left, with each view's controls at upper right (https://ourworldindata.org/redesigning-our-interactive-data-visualizations) [READ]. The live page shows Table, Map, Line and Bar tabs (S29).
- **Titles and labels.** A serif title, then a one-sentence definition. Lines carry direct labels at their right ends; gridlines are dashed; every tick carries its unit ("80 years") (S29).
- **Small multiples.** Settings split a chart into panels, and "Align axis scales" holds one scale across them (S28).
- **Tables and maps.** Sortable columns, a sparkline "Trend" column, absolute and relative change (S29). Maps use stepped yellow-to-blue bins with a hatched "No data" swatch, and a click on a country opens its chart (S28, S29).
- **Sources.** "In each of our visualizations, the source of the data is always displayed prominently." (S28). Under each chart sit "Data source:" with short citations and "OurWorldinData.org/life-expectancy | CC BY". The data page lists unit, date range, last updated and next expected update, gives each source a "Retrieved on" date and citation, and offers "this abbreviated in-line citation" for tight spaces (S29).
- **Downloads.** SVG, PNG, CSV and embed code (S28); the quick download is "a ZIP file containing a CSV file, metadata in JSON format, and a README" (S29). Mobile was still "What's next" in 2023 (S28).
- **Rights note.** OWID's charts and data are CC BY. The 2023 article calls Grapher's code MIT-licensed; the footer now says "under a custom license. Re-use requires permission." [READ, S28]. Check before adapting any code.

### 2.5 The Economist

From the montage image (S31) [READ, by eye]: each chart opens with a short red rule and red tab at top left, a bold title in red, a bold subtitle naming the measure, then the units. The y-axis numbers sit at the right edge. Gridlines run horizontally only. "Source:" sits at bottom left and "The Economist" at bottom right. Red is the main series color, with dark blue and teal as seconds. Annotations sit in the plot ("The Arctic is warming much faster than everywhere else"). Australia's temperature chart diverges red above zero and blue below. A ranked table of polluted cities tints value cells in reds.

From the maps style guide (S30) [READ]: labels in Econ Sans Condensed at 6.5 to 9 pt; leader lines 0.5 pt black at right angles, or 45 degrees if needed; "Labels over 3 lines should go in a key"; single-hue scales in red, blue, purple, yellow, green and stone; diverging pairs yellow-blue and green-purple; and two US county maps that pair a stone scale with a green scale, and a blue scale with a red one.

From Muth (S10) [SECOND]: Economist charts use "a business-y dark blue" in most charts with turquoise and red, rarely other hues, and warm grays such as RGB(135, 135, 113).

### 2.6 The navy and teal collage

A collage of chart forms in navy, teal and their tints on light gray tiles, with no text [READ, by eye; maker unknown]. It shows arrow dot plots for change, stacked and Marimekko bars, a people unit chart, a population pyramid, donut small multiples, a streamgraph, a waffle, a bubble cluster, four line small multiples that each highlight one line against faded others, a dot plot, a Sankey, a parliament chart, a French choropleth and a proportional symbol map. It teaches two-hue discipline: tints of two inks carry every form.

### 2.7 The utilitarian asset pack

A commercial sheet, "200 graphic assets", "Designed by Vanzyst", described on the sheet as "inspired by utilitarian design aesthetic" [READ, by eye]. Black hairline charts on gray paper texture: radar charts, dials, dot clouds, step lines, hatched bars, stacked lines, numbered markers 01 to 12, and serial numbers such as "0-9-98P-18-76". No chart carries real data or a source. It teaches line-weight hierarchy, indexing and hatching as a non-color code. It also shows the risk: furniture that looks like evidence and holds none.

## 3. Comparison

| Property | New York Times | Carbon | BBC GEL and bbplot | Our World in Data | The Economist | Two images |
|---|---|---|---|---|---|---|
| Title | Sentence stating the finding, serif bold [REPRO] | Descriptive, states the insight | Short, bold, left-aligned | Indicator name, serif | Bold red title, measure as subtitle | None |
| Annotation | In-plot, explains encoding, reader's scale [REPRO] | Trends and peaks on dashboards | Labels, arrows, curved lines in cookbook | Info icons, notes below | In-plot callouts | None |
| Labels and legends | Direct labels; legend bar for maps only [REPRO] | Direct first; legend at bottom | Direct first; legend at top | Direct line-end labels | Small legend under subtitle | None |
| Gridlines and axes | Pale grid; unit on one tick; wide minus [REPRO] | Zero for bars; gaps never bridged | Horizontal grid #cbcbcb; #333333 baseline | Dashed grid; unit on every tick | Horizontal grid; numbers at right | Pack: axes without values |
| Type | Cheltenham titles, Franklin labels [READ, REPRO] | IBM Plex | BBC Reith; Helvetica in bbplot | Serif title, sans body | Econ Sans | None |
| Categorical color | Story-specific; no fixed palette [SECOND] | 14 in fixed order | Product palettes; blue and amber | Many hues | Dark blue, turquoise, red | Navy and teal; black only |
| Sequential | Stepped bins [REPRO] | Ten-step single hue | Not stated | Stepped yellow to blue | Six single-hue scales | Tints |
| Diverging | Gray to red one-sided; pink to green [REPRO] | Red to cyan; purple to teal | Not stated | Not seen | Red and blue; stone and green | None |
| Highlight and gray | Black or one hue over gray [REPRO] | Hover dims others | Neutral palette, key info stands out | Reader picks the lines shown | Bright vs dark tones | Collage: one line over faded lines |
| Small multiples | [UNVERIFIED] | Linked charts | Facets, one scale | Toggle, align scales | Seen in montage | Collage: yes |
| Tables | [UNVERIFIED] | Fallback only | HTML table as alternative | Full view, sortable, sparklines | Ranked, tinted cells | None |
| Maps | Stepped choropleth; party colors for elections [REPRO, READ] | Design-only; Mapbox themes | Labels, keys, scales | World choropleth, no-data hatch | Full map style guide | Choropleth, symbols |
| Mobile | Text as HTML; artboards per width [READ] | Legend stack or button | Vertical stack at 400 px | Planned in 2023 | Not seen | None |
| Interaction | Mostly static; nothing important on hover [READ] | Hover, click, zoom | Not covered | Tabs, slider, selector, full screen | Print-first | None |
| Accessibility | [UNVERIFIED] | Texture; heat maps exempt from 3:1 | Color never alone; full text description | Not stated | Not stated | Not applicable |
| Source line | [UNVERIFIED] | Not covered | "Source:" left, logo right, rule above | Visible in every view; citation block | "Source:" left, name right | None |

## 4. What makes the Times's style look the way it does

1. **The title makes the point.** A sentence in a bold serif states the finding; a quieter subtitle names the measure. [REPRO, S09]
2. **Annotation sits in the chart.** Notes explain the encoding, name the record and give the reader a familiar scale, joined to the data by thin leader lines. [REPRO, S11; READ, S06]
3. **One thing is dark and the rest is gray.** Context data recedes into light gray and the series the story is about takes black or a single strong hue at a heavier weight. [REPRO, S11]
4. **Color changes from story to story, and type holds the brand.** The brand book calls black and white the core colors; Muth shows varied chart colors held together by Cheltenham titles. [READ, S02; SECOND, S10]
5. **Two typefaces with fixed jobs.** Serif for the title, sans for every label and number. [READ, S03; REPRO]
6. **Light scaffolding.** Pale gridlines, gray tick labels, the unit written once, no axis titles, no frame. [REPRO, S09, S11]
7. **Plain words before exact values.** "More crime" in large bold type outranks "+500 violent crimes per 100,000 people" in small gray type. [REPRO, S09, with Muth's reading]
8. **White space and pacing.** "relaxed pacing of content and generous use of white space" is a stated brand principle. [READ, S02]
9. **Static first.** Readers scroll, so important content never waits behind a click or hover; motion triggers on scroll. [READ, S05, S07]
10. **Text keeps its size while the art scales.** ai2html keeps labels as HTML and lets a graphic carry separate artboards for different widths; annotation sets can differ by width. [READ, S04, S05, S06]
11. **On a phone.** I could not confirm how Times charts stack on a phone. The mechanism for redrawing a graphic at narrow widths exists in ai2html, and the BBC documents a vertical stack, but I saw no Times phone layout. [UNVERIFIED]
12. **Party colors for party data.** Election and party-control graphics use red for Republicans and blue for Democrats. Section 5 flags this. [SECOND, S10; READ, S02]

## 5. Teachable rules for Oath & Action

Each rule is written for the locked palette, Inter Tight, Inter and Lora Italic, the token architecture (`work/ledger/20261021_Token-Architecture.md`) and Rule 05.3 (D2-01). Contrast figures come from that file or from my measurement.

| # | Rule | Reason | Section 13 part |
|---|---|---|---|
| R01 | Start from the reader's question and use one sentence or a table whenever either answers it faster than a chart. | The Times and BBC put the story first; section 13 asks when a table or sentence wins. | Selection guide |
| R02 | Title every chart with a full sentence that states the finding, set in Inter Tight 800, with the evidence kind (Finding, Association, Estimate, Illustration) above it as a label. | The Times title carries the point (S09); section 15 requires the evidence kind. | Specimens |
| R03 | Match the title's verb to the Atlas V7 grade: "can" or "may" for plausible, "untested" for hypothesis, both readings for contested. | Section 15; a sentence title makes a claim, so its strength must match the evidence. | Specimens |
| R04 | Under the title, name the measure, unit, place and period in Inter 400 secondary text. | The Times subtitle and Economist measure line separate claim from measure. | Specimens |
| R05 | Label series directly on the line end or the bar; use a legend only when labels cannot fit, and never for one series. | Carbon (S16), the BBC cookbook (S27) and Times reproductions agree. | Specimens |
| R06 | Write the unit once, on the top tick or first label, and keep other ticks bare. | Times practice (S09, S11); fewer repeated words. | Specimens |
| R07 | Treat annotation as part of the chart: name the record, explain any unusual encoding, give a reader's scale, and join notes to data with 1 px leader lines. | Cox via Pearce (S06); Watkins's chart (S11). | Specimens |
| R08 | Draw context data in Stone and the series the title names in Charcoal at a heavier stroke. | Times gray-and-black move (S11); the tokens already assign Charcoal to data emphasis and Stone to data context. | Palettes |
| R09 | Data reaches Pillar Red only for the one point the headline names, when no error or ask holds the view's red; on Newsprint the red mark takes a 1 px Charcoal keyline. | Rule 05.3; Pillar Red measures 2.96:1 on Newsprint, below the 3:1 needed for graphics. | Palettes |
| R10 | Never give red to a category, a series or a scale; red points, and it never encodes. | One working red per view; every reference uses red as a series color (section 5 conflicts). | Palettes |
| R11 | Categorical order: Prussian, Verdigris, Stone, then lighter tints of each; past about five categories, switch to small multiples or a table. | The Economist and the collage show few-ink discipline; on Newsprint, Prussian measures 9.42:1, Stone 4.29:1, Verdigris 3.37:1. | Palettes |
| R12 | Sequential scales use one hue (Verdigris or Prussian), stepped in OKLab toward Newsprint, darkest for the largest value, in labeled stepped bins. | Carbon's single-hue rule (S15); stepped legends in the Times heat map and OWID map. | Palettes |
| R13 | Diverging scales never pair red with blue. Test two at Gate 2: one-sided Stone to Verdigris, with gray for the side the title does not name, and two-sided Prussian through Newsprint to Verdigris. Label the midpoint in words. | Section 13; the Times heat map is one-sided (S11); the Economist pairs stone with green (S30). Stone and Verdigris sit close in lightness (OKLCH L 0.498 and 0.548), so hue, labels and the midpoint must separate the arms. | Palettes |
| R14 | Show party data with neutral inks and printed names or letters; never assign Pillar Red or Prussian to a party. | The Times and BBC use party colors (S02, S26); red and blue read as partisan, and Prussian beside red would read as Democratic blue (design judgment). | Palettes; complex examples |
| R15 | Start bars and areas at zero; a line may crop its axis when the subtitle says so. | Carbon (S14). | Specimens |
| R16 | Never bridge missing data; break the line and label both ends of the gap. | Carbon (S14); a bridged gap invents values. | Specimens |
| R17 | Keep one y scale across small multiples unless the subtitle says the scales differ. | BBC cookbook (S27); OWID's "Align axis scales" (S28). | Specimens |
| R18 | Set chart labels in Inter 600 at 13 px or larger with tabular figures and a true minus; secondary text in Deep Stone on Newsprint. Keep Lora Italic for quoted words only. | Token type scale and 13 px floor; the Times's serif-title, sans-label split maps onto Inter Tight and Inter, and Lora Italic stays locked to quotation. | Specimens |
| R19 | Draw horizontal hairline gridlines in Stone, no vertical grid, no ticks, and a Charcoal baseline at zero. | bbplot (S26), the Economist and the Times converge here. | Specimens |
| R20 | Put a source line under every chart in section 15 order (publisher, table, period, geography, date retrieved, qualification), left-aligned, with the Oath & Action credit at right. | bbplot's footer (S26), the Economist's montage and OWID (S29). | Specimens |
| R21 | Give every chart a text or table equivalent, written by its designer, that carries everything a sighted reader gets, including notes and source. | BBC complex images (S22); section 13 asks for it on every specimen. | Specimens; complex examples |
| R22 | Hide nothing important behind hover; a tooltip repeats both axis values and adds detail for readers who dig. | Tse (S05), Aisch (S07), Carbon (S13). | Complex examples |
| R23 | Offer Chart and Table views on every interactive, a Map view only when location matters, and downloads in PNG, SVG and CSV with metadata and a README. Keep the source visible in each view. | OWID (S28, S29); section 13's export list. | Complex examples |
| R24 | Give each data page a citation block: a short in-line citation, a full citation, last updated and next expected update. | OWID's data pages (S29). | Specimens |
| R25 | Design at 390 and 360 px first: stack panels vertically, move secondary notes below the plot, and keep text at its set size while the plot scales. | BBC (S21), ai2html (S04), Pearce (S06). | Complex examples |
| R26 | Never let color carry meaning alone; pair it with a label, shape, pattern or line style, and prove it with a grayscale proof. | BBC (S25), Carbon textures (S16), section 13's grayscale proofs. | Palettes |
| R27 | Run motion only on scroll or request, and resolve it to the final state under reduced motion. | Tse (S05); the token motion rules. | Complex examples |
| R28 | Every mark, tick and number traces to data, and illustrative values carry an "Illustrative data" label beside the chart. | The asset pack's invented serials; section 15. | Specimens |

**Conflicts with our rules and how to resolve them**

| Reference practice | Our rule it breaks | Resolution |
|---|---|---|
| The Economist uses its brand red as the default series color, for titles and for the tab on every chart (S31) | Rule 05.3: one working red per view | Primary series in Charcoal; no red tab or red title on charts; red marks only the headline's one point (R09) |
| Red and blue diverging scales: Economist temperature chart (S31), Economist map guide's blue and red pairing (S30), Carbon's red to cyan (S15) | Section 13: no red and blue diverging pair | Use R13's two candidates; temperature data gets no exception |
| Party colors: Times election maps (S10), Times "Holding a Monopoly" map (S02), BBC bbplot examples (S26) | Nonpartisan stance; Rule 05.3 | R14: neutral inks, party names printed on the marks, order by value or alphabet |
| Red for several series or categories: Carbon's categorical sequence holds two reds (S15); the Economist's stacked bars use several reds; OWID's line palette includes a red | Rule 05.3 | R10: remove red from categorical and sequential scales |
| Red sequential fills: the Economist's tinted table cells and the Times's one-sided red heat map | Rule 05.3 allows one job with several marks, but a red scale would compete with any ask or error in the view | Run the same one-sided pattern in Stone to Verdigris; test a red scale only in the demonstrated specimen section 13 requires |
| Carbon exempts heat maps from 3:1 contrast (S18) | Token roles: essential graphics meet 3:1 | Print values in cells or supply the table equivalent; keep the exemption as Carbon's practice and label it a design judgment if adopted |
| Carbon dims other series to 30 percent opacity on hover; map legends sit on an 80 percent opaque panel (S16) | Token architecture: opacity has two decorative jobs only | Dim by recoloring to Stone; put map legends on a solid Newsprint panel |
| BBC Minion at 12 px (S23); Economist map labels at 6.5 pt (S30) | 13 px screen floor | Screen labels at 13 px or more; print sizes wait for the Phase 4 point scale |
| A dark Prussian dashboard ground invites red alerts, as in Carbon's dark themes | Red never sits on Prussian | On Prussian, emphasis takes Newsprint and alerts take the glyph and word pattern from the state tokens |
| The Times's serif titles suggest Lora for chart titles | Lora Italic is locked to editorial quotation | Inter Tight 800 for titles; Lora Italic only for quoted words inside an annotation |
| The asset pack's decorative charts with invented serials (S31) | Section 15 evidence rules | R28; never use or trace its assets |

## 6. Candidate directions

**Direction A, Annotated Newsprint.** The editorial direction, closest to what Dustin admires in the Times. Charts sit on Newsprint with wide margins. Each opens with an evidence label and a sentence title in Inter Tight, then a measure line in Inter. Context data is Stone, the named series is Charcoal, and annotation does the explaining in the plot with fine leader lines. It borrows the Times's title, annotation and gray-against-black moves, the BBC's source footer and description rule, and OWID's table view. What makes it ours: the section 15 evidence label and grade-matched verbs, the single working red reserved for the headline's point under Rule 05.3, and the warm Newsprint ground in place of the Times's white.

**Direction B, Field Instrument.** The systematic direction, built for the atlas, the tracker and dashboards. It borrows the asset pack's line-weight hierarchy, indexing and hatching, and Carbon's exact behaviors for axes, gaps, legends and tooltips. Charts sit in hairline frames on the Signal Grid, with Atlas V7 identifiers (such as L42 or R10) as printed labels and hatching as the second code after color. Prussian surfaces carry exploration views, where emphasis turns Newsprint and red never appears. What makes it ours: every index number is a real Atlas ID, and section 15's sourcing holds, so the technical look always points at evidence.

**Direction C, Two-Ink Register.** The recurring-explainer direction. It takes the Economist's and the collage's discipline of very few inks, and assigns them to Prussian and Verdigris with their OKLab tints, with Stone for context and a one-sided Stone to Verdigris scale for change. Tables are first-class: ranked registers with tabular figures, sparklines and change columns, after OWID. Every interactive offers Chart, Table and Map tabs, downloads and a citation block. What makes it ours: Verdigris carries the data work that red does for the Economist, which leaves Pillar Red free for the reader's next step, and the register form ties the charts to Concept 11 Register, which Dustin favored.

## 7. Rights

All references in this brief are study only and never ship (Master Brief V2 section 2). Rows follow the main table in `work/research/20261020_Rights-Ledger.md`. "T-TP" means no license held and copyright stays with the maker. Two new codes are proposed: T-BBCGEL for the GEL infographic asset licence on S21 (read on October 30: free use without attribution, no redistribution of the assets, no implied BBC endorsement), and T-OWID upgraded from a search snippet to a page read on S28.

| # | File or reference | Set | Likely origin | Evidence | Permitted use | Notes |
|---|---|---|---|---|---|---|
| dvs-01 | S01, S02: Jalbert-Gagnier case study and slides | data-viz-system | third-party screenshot | Page and slide files read October 30, 2026 | study only | T-TP. Page by David Jalbert-Gagnier and Objective Subject; slides show pages of a New York Times Company brand book and the Times's trademarks |
| dvs-02 | S03, S04: ai2html repository and documentation | data-viz-system | third-party screenshot | README states "Copyright (c) 2011-2021 The New York Times Company" | study only | T-TP. License file not read; read it before any code reuse |
| dvs-03 | S05: Archie Tse, Malofiej 2016 slides | data-viz-system | third-party screenshot | PDF in archietse/malofiej-2016, cloned read-only | study only | T-TP. Archie Tse; slides credit The New York Times |
| dvs-04 | S06: swoopy-drag | data-viz-system | third-party screenshot | README and demo page | study only | T-TP. Adam Pearce; license not checked |
| dvs-05 | S07: "In Defense of Interactive Graphics" | data-viz-system | third-party screenshot | Blog post dated March 31, 2017 | study only | T-TP. Gregor Aisch |
| dvs-06 | S08: Marco Hernandez interview | data-viz-system | third-party screenshot | Nightingale, April 25, 2023 | study only | T-TP. Data Visualization Society and interviewer TK Sajeev Kumar; first published by NewspaperDesign.in |
| dvs-07 | S09, S10, S11: Datawrapper blog posts | data-viz-system | third-party screenshot | Three posts by Lisa Charlotte Muth | study only | T-TP. Datawrapper GmbH |
| dvs-08 | Times charts reproduced on S09 and S11 (2015 Arctic ice, 2018 immigration scatter, 2022 jobs, 2022 heat map, Times hue wheel on S10) | data-viz-system | third-party screenshot | Images on kirby.datawrapper.de | study only | T-TP. The New York Times Company; never reproduce or trace |
| dvs-09 | S12 to S19: Carbon Design System pages | data-viz-system | third-party screenshot | Pages read October 30, 2026 | study only | T-TP. IBM; site terms not checked |
| dvs-10 | S20 to S25: BBC GEL and Mobile Accessibility Guidelines | data-viz-system | third-party screenshot | Pages read October 30, 2026 | study only | T-BBCGEL for the GEL infographic assets, which were not downloaded; BBC |
| dvs-11 | S26, S27: bbplot and the R cookbook, including the bbplot example sheet | data-viz-system | third-party screenshot | GitHub files and cookbook page | study only | T-TP. BBC; license file not read |
| dvs-12 | S28, S29: OWID redesign article and life expectancy data page | data-viz-system | third-party screenshot | Pages and live views read October 30, 2026 | study only | T-OWID. Global Change Data Lab. Its charts and data are CC BY; third-party data keeps its own license; code license conflicts between article and footer |
| dvs-13 | S30: The Economist design system and maps style guide v1.2 | data-viz-system | third-party screenshot | PDF dated 5 May 2017 | study only | T-TP. The Economist |
| dvs-14 | `20261030_Ref-Data-Viz-Chart-Collage-Blue-Teal.webp` | data-viz | third-party screenshot | Already in the ledger | study only | No change; source unknown |
| dvs-15 | `20261030_Ref-Data-Viz-Utilitarian-Graphic-Assets.webp` | data-viz | stock preview | Already in the ledger; credit "Designed by Vanzyst" | study only | No change; commercial asset pack |
| dvs-16 | `20261030_Ref-Data-Viz-Economist-Chart-Montage.webp` | data-viz | third-party screenshot | Already in the ledger | study only | No change; The Economist's charts and trademark |
| dvs-17 | 13 captures in `work/research/data-viz-references/` (listed in the change log) | data-viz-system | third-party screenshot | Taken October 30, 2026 at 1,440 px | study only | Studio captures of third-party pages for the board; the Gagnier capture shows Times brand book pages |

## Claims I could not verify

- How Times charts behave on phones, including whether panels stack vertically.
- Times practice for small multiples, tables, source lines and accessibility.
- The original venue and date of Amanda Cox's line "The annotation layer is the most important thing we do".
- The Times's current election color values. Muth reports them; I did not see them.
- The Economist's chart rules from its own 2017 chart guide and from Sarah Leo's 2019 article, neither of which I could open.
- Carbon's approved chart textures, whose page returns 404.
- The BBC's per-product infographic palettes, held in an asset file I did not open.
- The license terms for ai2html, swoopy-drag, bbplot and Carbon Charts.
- Typeface identifications made by eye: Franklin in the Times reproductions and the serif on OWID's titles.

## Change log

Files created:

- `work/research/20261030_Data-Viz-System-References.md` (this brief)
- `work/research/data-viz-references/20261030_Capture-Gagnier-NYT-Case-Study.jpg`
- `work/research/data-viz-references/20261030_Capture-Carbon-Color-Palettes.jpg`
- `work/research/data-viz-references/20261030_Capture-Carbon-Chart-Anatomy.jpg`
- `work/research/data-viz-references/20261030_Capture-Carbon-Legends.jpg`
- `work/research/data-viz-references/20261030_Capture-BBC-GEL-How-To-Design-Infographics.jpg`
- `work/research/data-viz-references/20261030_Capture-BBC-GEL-Complex-Images.jpg`
- `work/research/data-viz-references/20261030_Capture-BBC-Bbplot-GitHub.jpg`
- `work/research/data-viz-references/20261030_Capture-BBC-R-Cookbook.jpg`
- `work/research/data-viz-references/20261030_Capture-OWID-Redesign-Article.jpg`
- `work/research/data-viz-references/20261030_Capture-OWID-Grapher-Chart.jpg`
- `work/research/data-viz-references/20261030_Capture-OWID-Grapher-Map.jpg`
- `work/research/data-viz-references/20261030_Capture-OWID-Grapher-Table.jpg`
- `work/research/data-viz-references/20261030_Capture-Economist-Maps-Styleguide-Colour-Scales.jpg`

Files modified: none. Scratch scripts and fetched pages stay in the session scratchpad and are not part of the project.
