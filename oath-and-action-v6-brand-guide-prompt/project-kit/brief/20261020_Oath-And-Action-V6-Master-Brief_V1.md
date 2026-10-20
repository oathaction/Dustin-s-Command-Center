# Oath & Action Brand Guide, Edition 06: Master Brief

Client: Dustin Cathcart, Founder and Editor, Oath & Action
Brief written: October 20, 2026
Status: Version 1, for use with the phase prompts in `brief/phase-prompts/`

This brief is the full specification for Edition 06. The phase prompts say what to do now. `CLAUDE.md` holds the operating rules that apply in every session. When this brief and a phase prompt disagree, stop and ask Dustin at the next gate.

---

## 1. The commission

Rebuild the Oath & Action brand guide into a finished identity system with the craft of a leading international branding studio. Deliver an elevated, fully working HTML guide, supported by real reusable assets: vector masters, PNG variants, tokens, templates, licenses and an implementation brief for AI builders.

Oath & Action is a nonpartisan civic publication and set of tools that explain how public rules affect ordinary lives. Its products include a publication and newsletter, the systems atlas "Who Do They Answer To?", trackers, reports and explainers. The brand is preparing for launch soon, so the guide has to be production-ready on delivery.

The identity should feel current, intelligent, human and inviting. Preserve the recognizable brand and improve its craft and usefulness. The guide and the production system it defines are the focus. The atlas is the hardest real application and the main test of the system.

Five outcomes define success:

1. A newcomer understands what Oath & Action is, how to read its graphics, and how to take part.
2. A designer or an AI builder can make a correct new asset from the guide and the tokens alone.
3. Every rule shows its purpose, a correct application and a meaningful failure case.
4. The data visualization and systems chapters teach a complete, honest graphic language for data, evidence and cause and effect.
5. Every download works, and every claim is sourced or labeled.

---

## 2. Sources and authority

Place the supplied files in `source/` exactly as named below. Never edit, move, rename or delete them.

| File or folder in `source/` | What it holds | Role |
|---|---|---|
| `20261018_Oath-And-Action-Brand-Guide_V5-Polished.html` (4.3 MB) | Current identity: 16 chapters (Purpose, Voice, Identity, The Ampersand, Color, Type, The Grid, Pillar Marks, Topic Icons, Photography, Data Visualization, Motion, In Use, Reports, Standards, Atlas System) plus a closing; inline SVG sprite; embedded Inter Tight, Inter and Lora; application specimens; 12-page report reader; 9 downloads; scripts | Identity authority |
| `20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html` (3.1 MB) | Atlas model, snapshot October 15, 2026. JSON in `<script type="application/json" id="atlas-data">`. Counts in `meta.counts`: 51 variables, 118 connections, 23 loops (20 numbered), 50 reforms, 194 issues (193 active), 433 claims, 1,099 sources, 16 pathways, 5 hubs | Model authority for every ID, sign, delay, grade, effect, route and source |
| `20261018_Oath-And-Action-Atlas-Visual-System.html` | The atlas visual system and refined icons. States that its IDs, signs, delays and grades come from Atlas V7 and that it does not revalidate the model | Application test. Reconcile against V7 |
| `20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html` | Concept 00 (the shared language) and eleven concepts: 01 Transit Atlas, 02 Orbit, 03 Field Manual, 04 Broadsheet, 05 Iceberg Descent, 06 Ledger, 07 Loop Card, 08 Loop Field Guide, 09 The Circuit, 10 Who Can Act, 11 Register | Application test. Dustin's saved screenshots favor 03 Field Manual, 09 The Circuit, 10 Who Can Act and 11 Register |
| `20261019_Oath-And-Action-Atlas-Design-Concepts_V1.html` | Earlier concepts | Background |
| `20261018_Oath-And-Action-Brand-Guide_V5.html` | Edition 05 before the polish pass | Background |
| `20261018_Oath-And-Action-Brand-Guide_V4.2.html` | "Brand Field Guide / V4 Refined." Includes chapters later dropped: Mastheads, Watermarks, Symbol Library, Relationships ("Give every handoff an owner"), Publications, Footers, Social, Specifications | Background. Recover useful material that V5 lost |
| `data_viz.zip` (about 75 images in `data viz/`) | Chart, table, infographic and systems references | Principles only |
| `Design_I_like.zip` (50 files in `Design I like/`) | Y2K icon sheets, icon studies, screenshots of favored concepts, and the nested folder `Systems Map and Atlast Design Ideass/` (folder name as supplied) | Principles only |
| `icon-studies/` | Study sheets 04 Flat Square, 05 Hand Drawn and 08 Simple Line, which were supplied outside the zips | Direction for the symbol family (section 11) |

Phase 0 unpacks both zips with a script into `work/extract/references/data-viz/` and `work/extract/references/design-i-like/`, leaving the zips untouched. The full set of eight icon studies is: 01 Y2K (`Y2K Civic Pillar Icon Sheet.png` in the Design zip), 02 Flat Geo (`Flat civic pillar icon studies.png`), 03 Isometric (`Isometric civic pillars_ explain, track, connect, act.png`), 04 Flat Square (`icon-studies/`), 05 Hand Drawn (`icon-studies/`), 06 Geometric (`Oath & action geometric pillars.png`), 07 Abstract Geometric (`Abstract geometric civic icon concept sheet.png`) and 08 Simple Line (`icon-studies/`).

Order of authority, highest first:

1. A newer guide that Dustin explicitly approves in writing.
2. V5 Polished for identity rules. Atlas V7 for model content.
3. The Atlas Visual System and Concepts V2 as demonstrations to test and reconcile.
4. V5, V4.2 and Concepts V1 as background and a source of recoverable material.
5. Reference images and outside research, for principles and mechanisms only.

Rights rules for references: many images in the reference folders are stock previews (filenames beginning `1000_F_`, `360_F_`, `istockphoto-`, `gettyimages-`) or third-party screenshots. Several icon study sheets appear to be AI-generated. Study them for principles. Never trace, copy, embed or ship them. Final marks are authored vectors.

---

## 3. Locked identity

| Element | Current system |
|---|---|
| Brand | Oath & Action |
| Pillars | Explain → Track → Connect → Act |
| Principal tagline | "A country that answers to its people." |
| Mission | "Help people understand and improve the rules that shape their lives." |
| Reader promise | "We explain how a decision is made and give you a practical way to take part." |
| Editorial commitment | "Clarity is our duty. Action is our promise." |
| Display | Inter Tight |
| Reading and UI | Inter |
| Editorial quotation | Lora Italic |
| Newsprint | #DCD9D2 |
| Charcoal | #121212 |
| Pillar Red | #E63946 |
| Prussian | #1F2D5A |
| Stone | #5D636D |
| Verdigris | #4A7C74 |
| White | #FFFFFF |

Retain the custom wordmark, the recognizable master ampersand, the hinge idea, the lockmark and the Signal Grid. Use the actual vector masters from the V5 Polished sprite.

Change control:

- Locked lines stay exact. Propose a change only when it is substantive and necessary, mark it clearly for Dustin, and keep the original in force until he approves.
- Identity geometry may be refined. Show the original and the proposal side by side at 16, 24, 48 and 96 px and at display size, state the reason, and wait for a named approval. After approval, apply the refinement everywhere.
- A font substitution is never a finished identity decision.
- Ordinary instructions and example copy can be improved freely within an approved phase.

---

## 4. The studio team

Run these as separate Claude Code subagents defined in `.claude/agents/`. If a pass runs in the main session instead, say so in the gate report.

| Agent | Owns | Signs off on |
|---|---|---|
| `oa-creative-director` | Brand strategy, art direction, symbol family architecture, chapter ambition | Every chapter and application, last |
| `oa-design-director` | Identity geometry, all icons and graphics, layout, typographic detail | Every visual item before it ships |
| `oa-ux-accessibility-lead` | Information architecture, navigation, interaction, states, WCAG 2.2 AA | Every interactive item and page structure |
| `oa-dataviz-systems-lead` | Chart chooser, palettes, specimens, systems grammar, Atlas V7 fidelity, policy workflows | Every chart, table, map and diagram |
| `oa-research-lead` | Awards, references, real data, workflow facts, platform specs, rights | Every claim, statistic, reference and image right |
| `oa-editor` | Voice, locked lines, terminology, illustrative labels, rule-versus-demo contradictions | Every word |
| `oa-engineer` | Extraction, modular build, tokens, downloads, exports, tests | Functionality and verification |

How they work together:

- The research lead supplies facts and references before drafting starts on any item that depends on them.
- The design director and the UX lead resolve representative pages and applications together at 1440 px and 390 px before either finalizes. They record agreed decisions in `work/handoffs/`.
- Review order for each item: maker, design director, UX lead (when interactive), data visualization lead (when it shows data or cause and effect), editor, engineer, creative director.
- Agents pass work as files with a short summary. Each review returns scores and specific required changes.

---

## 5. Process, gates and ledgers

| Phase | Work | Gate output |
|---|---|---|
| 0 Intake and review | Extract sources, render and audit V5 Polished, reconcile with V7, inventory rights, write the concise review and work plan | Review, plan, Phase 1 proposal |
| 1 Research, strategy and direction | Verified research ledger, brand strategy, art direction, symbol family architecture, identity refinement proposals, guide architecture, token architecture | Direction board and refinement boards for approval |
| 2 Identity, foundations and symbols | Apply approved refinements; color, type, layout, tokens, states; Signal Grid; pillar marks; topic, atlas, status and utility symbols; graphic devices; motion | Foundations and symbols chapters, vector masters |
| 3 Data visualization and systems | Chart chooser, data palettes, at least twenty specimens, systems grammar, Atlas V7 worked examples, configurable policy workflows | Data and systems chapters |
| 4 Applications and reports | Digital, newsletter, social, report, print, slides, event and video applications; photography and video rules | Applications and reports chapters |
| 5 Assembly and verification | Final single-file guide, asset package, AI builder brief, full test matrix, change and validation report | Final deliverables for acceptance |

Each gate approves the proposal for the next phase. Dustin reviews every stage before changes are made.

Keep these ledgers in `work/ledger/` and `work/research/`:

- `change-ledger.md`: one line per change, with the chapter, the change, the reason and the approving gate.
- `decision-log.md`: routine decisions made inside an approved phase.
- `open-questions.md`: factual, rights and model questions for Dustin.
- `research/research-ledger.md`: reference, maker, verified status and date, principle observed, proposed use, limits, URL, date checked.
- `research/rights-ledger.md`: every font, image, reference and generated asset, with source, license or terms and whether it may ship.
- `gate-0-report.md` through `gate-5-report.md`.

### Research starting points

These were checked on October 20, 2026 through search results from each official domain. The drafting environment could not open the pages, so the research lead opens each one, re-verifies it, and quotes exact wording only after reading the page. The full ledger, with 16 award results and 25 interactive references, is `brief/20261020_Research-Verification-Ledger.md`. Treat trend forecasts as creative inputs only.

Formal awards, 2025 and 2026:

| Reference | Verified status | Principle to study | Limits |
|---|---|---|---|
| Cooper Hewitt National Design Awards 2026: Thought Matter (Communication Design) and Laura Kurgan (Digital Design). https://www.cooperhewitt.org/national-design-awards/2026-national-design-award-winners/ | Announced February 25, 2026; gala May 19, 2026. The museum describes Kurgan's work as "spatial computation, data visualization, and digital cartography" | Kurgan's civic and spatial work, such as Million Dollar Blocks with Eric Cadora (Columbia Center for Spatial Research), which maps the public cost of incarceration block by block | Million Dollar Blocks is a mid-2000s project. Cite it to Columbia's site |
| Fieldwork Facility, V&A East Storehouse. https://www.fieldworkfacility.com/projects/storehouse | Gold, Best wayfinding or signage, Transform Awards Europe 2026 (ceremony March 26, 2026), credited to the V&A and Fieldwork Facility. The One Club lists the project as ADC 105th Best of Discipline in Architecture, Interiors and Environmental Design | How an identity becomes a practical interface for discovery and interpretation | The Transform award is for wayfinding and signage. Avoid calling it an identity award |
| Shopify, "The Renaissance Edition" (Winter '26 Edition, released December 10, 2025). https://www.awwwards.com/websites/sites_of_the_month/ and https://www.shopify.com/editions/winter2026 | Awwwards Site of the Month, February 2026 | Consistency across a large body of content (150+ product updates) | A commerce site with a generative painting aesthetic. Borrow the system, leave the style |
| SND47 Best of Design, 2026 | The New York Times: World's Best-Designed Digital Presence. Best in Show: The Pudding (small newsrooms) and The Washington Post (large) | Editorial and data presentation at the highest level, including election maps | Large-newsroom budgets |
| Online Journalism Awards 2025 | CalMatters, General Excellence (Digital Democracy and the Voter Guide). The Globe and Mail, "House Poor," Explanatory Reporting | Linking a rule to the people, votes, money and testimony behind it; explaining one policy system in household terms | California and Canadian contexts |
| Sigma Awards 2026 | Ten winners, including "Invisibles" (Salud con Lupa), on older adults left without pensions after system failures and an algorithm | How a public rule and its algorithm reach ordinary lives | Peru context |
| Information is Beautiful Awards, 2024 edition, presented June 2025 | The Washington Post, "How the 2024 U.S. election was decided, vote by vote" (Silver); Reuters on the Sudan famine and the IPC system (Gold); The Pudding, Outstanding Studio (Gold) | A nonpartisan alternative to red and blue election maps; "how the system should work, and what happened" | Not a 2026 award. The awards now run under the Data Visualization Society and resume in 2027 |

Trend forecasts, as creative inputs:

| Reference | What it says | Proposed use | Limits |
|---|---|---|---|
| Adobe 2026 Creative Trends. https://business.adobe.com/resources/creative-trends-report.html | Four trends: All the Feels, Connectioneering, Surreal Silliness, Local Flavor | Human texture, real people and real stories, local context | Vendor marketing research |
| Canva, "Imperfect by Design," 2026 trends (published December 2025). https://www.canva.com/newsroom/news/design-trends-2026/ | Ten trends, including Texture Check, Explorecore and Notes App Chic | Tactile texture and calm, clear layouts, used selectively | Consumer template styles. Never an editorial or civic norm |

Interactive and rule references (mechanisms to learn):

| Reference | Mechanism |
|---|---|
| Our World in Data Grapher redesign (about 2023, older). https://ourworldindata.org/redesigning-our-interactive-data-visualizations | Chart, map and table tabs; sources view; SVG, PNG and CSV downloads; full screen |
| LOOPY, Nicky Case (2017, older). https://ncase.me/loopy/ | Draw circles and signed arrows, press play, and watch a loop run |
| En-ROADS, Climate Interactive, MIT Sloan and Ventana Systems. https://www.climateinteractive.org/en-roads/ | Policy sliders redraw outcomes at once, framed as "what-if," never a forecast |
| PolicyEngine US | A reader enters a household and sees the net change, then a breakdown by provision |
| The Budget Lab at Yale interactives | An "as of" stamp on every view of a changing rule |
| CRFB Debt Fixer | Trade-offs against a visible goal. Disclose whose menu of options it is |
| USAFacts tax receipt | National budgets at personal scale. State that the allocation is illustrative |
| Urban Institute Net Income Change Calculator | The benefit-cliff chart. Its rules are dated, so use the pattern only |
| Parable of the Polygons (2014, older) | Try a small rule, see a large outcome, then read why |
| Bloomberg, "What's Really Warming the World?" (2015, older) | Test each suspected cause against the observed line, one at a time |
| CalMatters Digital Democracy; GovTrack; ProPublica Nonprofit Explorer; Ballotpedia Sample Ballot Lookup | Who decided, how they voted, the primary document behind each number, and an address-to-ballot entry point |
| Urban Institute Data Visualization Style Guide (updated August 27, 2025); UK Government Analysis Function guidance; FT Visual Vocabulary; USWDS data visualization guidance; Datawrapper Academy | Rulebook structure, chart selection by relationship, accessibility and publishing checklists |

Do not cite these as current: Malofiej 2025 or 2026 (no edition found; reported paused in 2021), the Brand New Awards (ended in 2015), or the "Kantar" name for the Information is Beautiful Awards. Re-check before citing: individual D&AD 2026 Yellow Pencils, the Webby 2026 data visualization winner, and Transform Awards North America 2026 public-sector results.

---

## 6. Quality bar and review rubric

"World-class" means these observable things:

- Every specimen uses finished content at its true ratio. No lorem ipsum, no "TBD," no grey boxes.
- Every rule is shown and explained: the rule, its purpose, a correct application and a meaningful failure case.
- The wordmark and ampersand hold their spacing at 16 px and in print. Icons sit on the pixel grid at 16 and 24 px.
- Typography is finished: balanced headings with no widows, comfortable measure, tabular figures in tables, true minus signs, consistent number and date formats, correct quotation marks and apostrophes.
- Every chart and diagram decodes in grayscale, with direct labels where possible, a reading guide and a source line.
- The distinctiveness test passes: cover the wordmark and the page still reads as Oath & Action.
- The production test passes: a builder makes a correct new asset from the guide and tokens without asking.
- The page rewards close inspection with considered detail, and a first-time reader still feels welcome.

Rubric. Score every chapter and application 1 to 5 on each criterion. The ship threshold is 4 on every criterion.

| Criterion | A 5 looks like |
|---|---|
| Craft | Optical spacing, alignment, type detail and drawing quality hold up at 2x zoom |
| Clarity | A newcomer can say what it is for, how to read it and where to use it from the first screen |
| Brand fidelity | Locked elements exact; red discipline; the system recognizable without the wordmark |
| Usefulness | Exact sizes, tokens, files and rules a producer can act on |
| Evidence honesty | Claims sourced; illustrative items labeled beside the item; evidence strength stated correctly |
| Accessibility | WCAG 2.2 AA met and checked; equivalents exist for diagrams and motion |

Record scores and reasons in the gate report. An item under threshold goes back with a concrete instruction. Repeat until it passes, or bring it to the gate with the reason it could not pass.

---

## 7. Guide architecture and chapter template

Preserve the substance of every V5 Polished chapter. Improve structure. Build a clear contents system, anchor links, responsive navigation, readable measures and useful cross-references.

Starting map for the new contents. The UX lead and creative director confirm or revise it at Gate 1, with a table that maps each V5 chapter and each recovered V4.2 chapter to its new home.

| Part | Chapters |
|---|---|
| Foundations | Purpose; Voice; Identity (wordmark, lockups, mastheads); The Ampersand and the hinge; Color; Type; Layout, spacing and the Signal Grid |
| Symbols and graphics | Pillar marks; Topic and atlas symbols; Status and utility icons; Graphic devices and patterns (including watermarks) |
| Evidence and media | Photography, illustration and video; Data visualization; Systems graphics; Evidence and sourcing |
| Behavior | Motion and states; Components and interaction |
| Applications | Web and atlas; Newsletter and email; Social; Reports; Print and presentation; Video frames |
| Production | Tokens and how to choose them; Assets and downloads; Standards checklist; Atlas system test; Closing |

Every chapter follows this template:

1. Opener: number, title, and one sentence that states what the chapter helps a reader do.
2. The rule, stated plainly, with its tokens.
3. Why it works: the purpose, with a citation for formal guidance or the label "Design judgment" for a studio decision.
4. A correct application: finished, at true size, in a realistic context.
5. A failure case: a visible and meaningful one. Include a corrective example only when the difference teaches something.
6. Specifications: sizes, tokens, files and download links.
7. Cross-references to related chapters.
8. A short "For builders" note on choosing the right token or asset.

---

## 8. Tensions to repair

Resolve each of these, show the resolution in a specimen, and list it in the change report.

1. Small text. Tracked labels in V5 are specified at 10 to 12 px (eyebrows at 11 px, tags and footers at 10 px, navigation at 12 px) against a 13 px small-text minimum. Set a readable hierarchy and document any exception precisely, with its size, weight, tracking, contrast and permitted contexts.
2. Loading state. V5 pulses the Signal Grid lever at 20 percent opacity, which conflicts with its own opacity rule (two watermark values only) and its motion rules. Define consistent, accessible states with a still alternative and visible text.
3. Tints and utility glyphs. The blanket "There are no tints" rule and the six utility glyphs (menu, close, search, arrow, download, external link) cannot support charts and interactive products. Establish bounded extensions with tokens, named jobs and examples. Section 10 gives the rule for adding a token.
4. Signal Grid meaning. V5 uses the grid to code pillar, content type, progress, gaps and series. Decide which encoding takes precedence, which combinations are valid, and how a reader decodes it from a key beside the graphic.
5. "The chart proves the sentence." A chart can show a finding, an association, an estimate or an illustration. Define titles that state which one, matched to the evidence grade (section 15).
6. Illustrative status. V5 carries one global note that people, quotes and figures are illustrative. Put the label beside each realistic quote, person and figure that a reader could mistake for a real endorsement or finding.
7. Colliding IDs. In Atlas V7, variable IDs B2, B3, B4 and B5 match loop IDs B2, B3, B4 and B5. Loop IDs R1 to R18 sit beside reform IDs R-01 to R-50. V5's Standards chapter numbers its rules R1 to R9. Design a typed ID chip (for example "Variable B4," "Loop B4," "Reform R-01") so a bare ID never appears, and renumber the Standards rules with a prefix that cannot collide.
8. Grade vocabulary. V7 uses "well-supported" and "plausible_contested" on connections, "well_supported" and "retired" on issues, "contested" on claims, and its methods text also defines "Mixed." Create one display vocabulary and a mapping table. Never edit V7. Log the inconsistency for Dustin.
9. Measured contrast of the locked palette, computed with the WCAG formula:

| Foreground | on Newsprint | on White | on Charcoal | on Prussian |
|---|---|---|---|---|
| Charcoal | 13.29 | 18.73 | n/a | 1.41 |
| Prussian | 9.42 | 13.28 | 1.41 | n/a |
| Stone | 4.29 | 6.05 | 3.10 | 2.20 |
| Verdigris | 3.37 | 4.74 | 3.95 | 2.80 |
| Pillar Red | 2.96 | 4.17 | 4.49 | 3.19 |
| Newsprint | n/a | 1.41 | 13.29 | 9.42 |

   Stone fails 4.5:1 for small text on Newsprint. Pillar Red fails 3:1 for informative graphics on Newsprint, which is why V5 adds a 1 px Charcoal edge. Red text fails at small sizes on every surface. Define text-safe and graphic-safe roles for each color on each surface, and confirm the numbers on rendered pages.
10. Download names. Replace the nine OA_* filenames (`OA_Amp_16.svg`, `OA_Amp_Master.svg`, `OA_C1.svg`, `OA_C2.svg`, `OA_C3.svg`, `OA_Hinge.svg`, `OA_L6_Prussian.svg`, `OA_M1.svg`, `OA_S2.svg`) with dated descriptive names. Keep the internal IDs in the SVG `id` attributes and in the asset index.
11. Lost chapters. V4.2 had Mastheads, Watermarks, Symbol Library, Relationships, Publications, Footers, Social and Specifications. Evaluate each and recover what is useful.
12. One tracker for every route. The nine-stage bill tracker is a configurable example. Section 14 defines the workflows it has to support.
13. Widths for ordinal effects. Concept 10 draws expected gain as strand width. V7 reform effects are ordinal codes. Either label the widths as ordinal categories with a legend or choose another encoding.
14. Red on red. When status or data already uses red, editorial red emphasis needs another method. Resolve it in a specimen.
15. Partisan and cliché risk in the icon studies. Study 05 Hand Drawn pairs red and blue figures and uses a Capitol dome and scales of justice. Keep the human texture and avoid the pairing and the clichés.

---

## 9. Identity refinement

Inspect the real vector masters from the V5 Polished sprite: wordmark, master ampersand, small-size ampersand, hinge, lockmark and Signal Grid (V5 values include a 123.5 unit field, links of 1 px in Stone, node diameter 7.6, and a lever at 1.25x).

For each element:

1. Measure: letterspacing and kerning pairs across O A T H & A C T I O N, ampersand weight and size against the capitals, clear space, minimum sizes in print and on screen.
2. Render at 16, 24, 48 and 96 px and at display size, on Newsprint, White, Charcoal and Prussian, in color and in one color.
3. Diagnose: list optical problems with screenshots, such as uneven gaps, a heavy joint at small sizes, or red losing edge contrast on Newsprint.
4. Propose: draw the refinement as vectors. Build a comparison board with original, proposal and an overlay, plus the reason for each change.
5. After Dustin approves, apply the refinement to every use and asset, and record it in the change ledger.

Also define lockups and mastheads for desktop, mobile, newsletter and social; clear space; minimum sizes; approved surfaces; and misuse cases that matter.

---

## 10. Color, type, layout, tokens and states

### Color

- Separate three kinds of color: identity color (the locked palette), state color (interface feedback), and data color (section 13). Keep identity colors out of data semantics unless a rule says otherwise.
- A new token is allowed only when all five conditions hold: a measured need exists that no current token meets; the value derives from the palette by a documented method (for example mixing toward Newsprint or Charcoal in OKLCH); it has one named job; it passes contrast on every surface it is used on; and it is registered in the token file with usage notes.
- Tints are permitted for data scales, state backgrounds and selection. Identity marks stay in solid palette colors.
- Give readable treatments to muted, disabled, hover, focus, loading, selected, warning, error, empty and success. Each state uses a text label or a shape change in addition to color. A disabled action stays legible and says what will make it available.

### Type

- Inter Tight for display, Inter for reading and interface, Lora Italic for editorial quotation.
- Set a full scale for screen and print, with sizes, line heights, tracking, weights and measures. Body measure 60 to 75 characters.
- 13 px is the small-text floor on screen. Document any exception precisely.
- Email uses the system stack documented in V5 (Helvetica, Arial, sans-serif for display and body, Georgia Italic for quotation). Keep that rule and show it.
- Tabular figures in tables and numeric columns. A true minus sign (−) in data.

### Layout

- A spacing scale, a column grid per breakpoint (1440, 1024, 768, 390, 360), section rhythm and measure rules.
- The Signal Grid: its geometry, sanctioned positions and sizes, its encodings with precedence and valid combinations, and a decoding key beside each use.

### Tokens

- Categories: color, typography, space, size, border and hairline, radius, opacity, layout and breakpoints, motion (durations and easings), z-index, chart (marks, axes, gridlines, annotations, palettes), and component tokens.
- One source file generates `tokens.css` and a JSON file in the W3C Design Tokens Community Group format. Record the format version used.
- Name tokens by role, for example `--oa-color-text-secondary-on-newsprint` and `oa.color.text.secondary.onNewsprint`.
- Write a decision guide called "How to choose a token": surface first, then role, then state, with worked examples for a caption, a disabled button, a chart highlight and a warning.

---

## 11. The symbol system

### Architecture

Define one master family and a short list of sanctioned treatments. The creative director and design director propose the architecture at Gate 1. This starting proposal is for them to confirm or revise with reasons:

| Study | Proposed role | Watch points |
|---|---|---|
| 06 Geometric | Basis for the four master pillar marks: strong filled silhouettes at large sizes | In Track, three circles in Prussian, Verdigris and red can read as a status light. Act's quadrant can read as a letter D or a play button. Explain's arcs and square can echo a letterform. Red appears in all four marks, so red discipline needs a rule |
| 08 Simple Line | Line companion for the pillars at small sizes, and the grammar for topic and atlas symbols, extending V5's 24-unit, 2 px stroke family with one accent node | Act's open door connects to the brand's open-door idea. Track's tree must stay distinct from the Signal Grid |
| 07 Abstract Geometric | Source for restrained patterns, rhythm lines and halftone texture in editorial graphics | Keep pattern density low behind text |
| 01 Y2K | Energy for orbit, ring and motion vocabulary in Track, Connect and loop graphics | A source of silhouettes and movement, never a separate icon style |
| 02 Flat Geo | Comparison study for pillar silhouettes | Overlapping forms can blur at 16 px |
| 03 Isometric | Exploded layer diagrams only, such as the three atlas layers in Concept 03 | Never for icons. Keep labels flat and readable |
| 04 Flat Square | Tiles for avatars, app icons and social cards | A fully red tile breaks red discipline |
| 05 Hand Drawn | Editorial spot illustration with human texture, at 48 px and larger | No red and blue pairing; avoid the Capitol dome and scales; never used as an icon |

### Semantic classes

Define each class, its job, its grid, and where it may appear:

- Pillar marks: the four pillars, in order.
- Topic symbols: subjects of coverage. Start from V5's twenty: Ballot, Ranked ballot, Open primary, District map, State house, Bill, Committee hearing, Roll call vote, Court, Campaign money, Local government, Public records, Housing, Work and wages, Taxes and budget, Health care, Cost of living, Contact an official, Testify, Organize.
- Atlas symbols: system areas and the things in the model. Derive the inventory from Atlas V7 content. Candidates include the ten domains (D01 News, records and public information; D02 Elections and representation; D03 Money, lobbying and influence; D04 Congress, agencies and public services; D05 Checks on power and equal justice; D06 Competition and market power; D07 Work, pay and bargaining power; D08 Taxes, wealth and economic security; D09 Housing, health care and getting ahead; D10 Taking part, trust and shared norms), the three layers (Power and accountability; How the economy reaches a household; Technology and its effects), the five outside drivers X1 to X5, the five hubs, the eleven routes to change (LOC, SS, BI, FS, FR, FA, ENF, CRT, AV, IC, CIV), problems, reforms, evidence, cases, authority and civic action. Avoid an arbitrary count of interchangeable symbols.
- Status marks: tracker and record states.
- Encoding glyphs: polarity signs, link types, delay marks, evidence grades, loop types, closure, intervention markers. Define these with the systems grammar in section 14.
- Utility icons: interface actions. Extend the six V5 glyphs only for real interface needs, such as copy, filter, sort, expand, collapse, play, pause, reset, share, print, info and warning.

### Specifications

- Shared grids with keylines for 16, 24 and 48 px masters. Pixel-fit 16 and 24 px versions.
- One stroke system, cap and join style, corner radius, counter size, accent node size, and optical overshoot rules.
- For every mark: monochrome, every approved surface, actual small size, with a label, and in a realistic composition.
- Side-by-side similarity checks for related subjects, such as Bill and Public records, Court and State house, Testify and Contact an official, Housing and Cost of living, and the ten domain symbols as a set.
- Semantic rules that keep topic symbols, status marks and utility icons from standing in for each other.

---

## 12. Graphic devices

Develop original devices where they help a reader: mechanism frames, explanatory layer diagrams (exploded views used selectively), intervention markers, evidence annotations, document references, chart keys, map locators, dividers, watermarks (recover from V4.2 and resolve with the opacity rules) and restrained patterns derived from the identity.

Precise diagrams, marks and logos remain authored vectors or code. Image generation may support conceptual illustration or mockup context, with an explicit label and rights information.

---

## 13. Data visualization

Expand the current chapter, which holds two specimens (an illustrative competitiveness index and an illustrative nine-stage tracker), into a practical reference for the atlas and future work.

### Selection guide

Organize by the reader's question and the data available. For each question, give the best forms, the forms to avoid, and the data they need. Include when a table or one sentence is the clearest choice, with an example of each.

### Specimens

Build at least twenty fully designed, readable specimens, chosen for real needs rather than an equal count per type. Each specimen carries: the reader question, data requirements, real data or clearly labeled illustrative data, the visual, a plain-language reading guide, the title, caption and source treatment, and rules for use. Each has a text or table equivalent.

| Need | Possible forms | Data that exists in Atlas V7 for real specimens |
|---|---|---|
| Compare values | Bar, dot plot, ranked list, dumbbell, small multiples | Variables, connections, loops, reforms and issues per domain (as on the Concept 11 Register index) |
| Explain change | Line, indexed series, slope, event annotations | Repair log dates (64 rows), delivery log dates (24 cases) |
| Show distribution | Histogram, quantiles, box plot when appropriate | Delays and grades across the 118 connections |
| Show composition | Stacked bars, unit chart | Evidence mix per domain; repair log by direction (toward voters, away from voters, voters kept existing rules, mixed, pending) and instrument |
| Explore relationships | Scatterplot, relationship matrix | Cross-domain connections (as on the Concept 11 "How the sheets connect" matrix) |
| Explain geography | Choropleth or proportional symbols, only when location matters | Repair log jurisdictions; route notes such as the 19 states that prohibit ranked-choice voting in some or all elections as of October 15, 2026 |
| Explain systems | Whole-system map, subsystem, signed link, loop, open chain, boundary, authority diagram | Section 14 |
| Explain policy and evidence | Intervention view, comparison matrix, uncertainty interval, implementation timeline, evidence table | Reforms (targets, loops, routes, effects), scenarios, claims with confidence, population, jurisdiction, period, limitation and sources |

Atlas values above were read from the V7 snapshot on October 20, 2026. Re-read every value from the extracted JSON before use. Quantitative specimens that need outside data use primary public sources found by the research lead, with source, series, observation period and qualification, or carry an "Illustrative data" label beside the chart.

`meta`, `numbers` (eight headline figures with captions, qualifications, sources and check dates), `outcomes`, `scenarios`, `overlays`, `omissions` and `leverage` in V7 also supply real material for big-number, comparison and evidence specimens.

### Palettes

Write a separate specification for sequential, diverging and categorical data palettes. Measure contrast on each approved surface, show grayscale proofs, and explain how each relates to the brand palette. A diverging scale must avoid a red and blue pairing, because it reads as partisan in the United States. Test red emphasis when status or data already uses red, and resolve the conflict in a demonstrated specimen.

### Representative complex examples

For at least three complex specimens (one chart, one systems diagram, one policy comparison), demonstrate desktop, narrow screen, grayscale, keyboard and screen reader behavior, interaction, and export (PNG, SVG and CSV where the data allows).

Study Our World in Data's chart, table, map, sources and download conventions (https://ourworldindata.org/redesigning-our-interactive-data-visualizations). Turn what you learn into teachable rules.

---

## 14. Systems graphics and the atlas

Define qualitative system graphics separately from quantitative charts. Build the grammar from Atlas V7's own fields and conventions, so the guide and the model agree.

### Grammar mapped to V7

| Property | V7 field and values | Reading rule to design |
|---|---|---|
| Variable type | `nodes[].type`: stock (31), flow (9), auxiliary (6), driver (5) | Show what a higher value means, from `increase_means`, beside the variable |
| Outside driver | Type driver, X1 to X5 | V7 draws these as rounded pills outside the clusters |
| Connection type | `links[].type`: causal (80), money (17), information (9), authority (7), ownership (5) | Distinguish without color |
| Polarity | `links[].polarity`: + (70), − (41), none (7, all authority) | V7: a plus sign means the variables move in the same direction and does not mean a benefit. Provide original signs and a written reading rule |
| Authority | Type authority, no polarity: LE02, LE03, LE19, LT13, LT14, LT16, LT17 | Has no causal sign and never closes a loop |
| Delay | `links[].delay`: S under 2 years, M 2 to 10 years, L over 10 years | Its own encoding, separate from evidence |
| Evidence grade | Connections: documented, well-supported, plausible, plausible_contested, hypothesis, plus a `contested` flag on 7 | V7 draws hypothesis as a dotted line. Grade, effect size, uncertainty and delay stay separate properties |
| Loop type | R reinforcing (18), B balancing (5) | Numbered links shown in order |
| Closure | Closed with every step numbered; closed with a hypothesized step (R2, R16); conceptual with no complete numbered chain (B2, B3, R9) | Disclose incomplete chains plainly |
| Layers and areas | Layers core, economy, technology; domains D01 to D10; subsystems | Boundaries and cross-layer connections |
| Interventions | `reforms[].targets` (links and variables), `loops`, `band` (parameter, feedback, information, rules, power to change the rules, goals) | Mark the intervention at its actual target |
| Reform effects | `effects` by family DQ Democratic quality, GE Government efficacy, EP Economic performance, EQ Income and wealth equality, in ordinal codes +L, +M, +S, 0, −S, −M, ? | Categorical. Never summed. V7 states the atlas does not add reform effects into a single score |
| Problem and remedy evidence | `problem_evidence` and `remedy_evidence` on each reform | Grade them separately, as V7 does |
| Routes to change | `routes.items`: 11 codes; feasibility high, medium, low, very low; dependencies authority, funding, enforcement, capacity, durability; per-reform `checked` dates | Feeds the configurable tracker |
| Documented events | `repairLog` (64 rows) and `deliveryLog` (24 cases) | Style events and cases differently from causal findings |
| Model limits | `omissions` (9), `rejectedLinks` (3), `methods` | Show what the model leaves out |

Line width and node area may encode a quantity only with a defined measure and a legend. A Sankey needs compatible measured flows. Labels and line patterns must survive the removal of color.

### Worked examples

Use the original V7 IDs and grades. These values were read on October 20, 2026. Re-verify each one.

1. R1, "Wealth and political influence reinforce each other." L01 A1 to B1 (+, money, well-supported, S); L02 B1 to E1 (+, money, plausible, M), the least certain step; L03 E1 to A1 (+, money, well-supported, L). Show the least certain step clearly and explain what it means for the whole loop.
2. A housing mechanism: R8, "Housing scarcity strengthens owners' incentive to restrict building." L38 A5 to A6 (+, well-supported, L) and L39 A6 to A5 (+, well-supported, L). V7 notes the loop no longer depends on A1. Show that revision honestly.
3. An electoral accountability chain: B4, "Electoral consequences can improve public performance" (L23 D5 to C3, −; L24 C3 to C5, +; L54 C5 to D5, +), alongside R10, "Safe seats shift accountability to small primary electorates" (L08, L25, L53, L42; V7 names C3 to C4 as the weakest link).
4. An intervention at its actual target: Reform R-01, "All-party primaries with ranked general elections," targets L25, L08 and C2, touches loops R10, B4 and R11, and lists effects DQ +M, GE +S, EP 0, EQ 0, with routes BI (medium), SS (low), LOC (medium) and FS (very low) and their check dates. Present it without an additive score.
5. An authority diagram built from the seven authority connections.
6. A conceptual loop with clear disclosure, using B2, B3 or R9.

Preserve the difference between documented events and causal findings throughout.

### Reconciliation

Compare every diagram in V5 Polished's Atlas System chapter, the Atlas Visual System and Concepts V2 against V7. Produce a table of each conflict (ID, sign, grade, delay, label or structure), the V7 value, and the resolution. Never present an earlier diagram as independent evidence.

### Interaction

Study the interaction logic of LOOPY (https://ncase.me/loopy/) and En-ROADS (https://www.climateinteractive.org/en-roads/). Turn the lessons into teachable rules, for example: let the reader step through a loop one numbered link at a time, with pause, reset and a still sequence; let a reader choose a reform and see its targets and ordinal effects, with the assumptions one click away. Never imply numeric precision the model lacks.

### Configurable policy workflows

Treat the nine-stage bill tracker as one configuration. Define accurate workflows for each route and instrument, with alternative paths, veto, funding, implementation and reversal where they apply:

- Federal statute: introduction, committee, floor, the other chamber, reconciling differences, presentment, signature, veto or pocket veto, override, appropriations, agency implementation and rulemaking, litigation, repeal or sunset.
- State statute: the same skeleton with state-specific steps, such as governor veto types, line-item veto and override thresholds.
- State ballot measure: petition, certification, ballot title, election, implementation, legislative amendment or repeal where permitted, court challenge.
- Local ordinance, federal executive action, chamber rule or confirmation, enforcement and litigation, court doctrine, Article V amendment, interstate compact, and civil society action.

Map each workflow to the V7 route codes. The research lead verifies each against official or authoritative sources, such as congress.gov, the National Conference of State Legislatures and Ballotpedia, and records the date checked.

---

## 15. Evidence, sourcing and illustrative status

- Chart and diagram titles state the kind of evidence:
  - Finding: a measured result with a source and period.
  - Association: a pattern that does not establish cause.
  - Estimate: a modeled value with a stated range or method.
  - Illustration: a demonstration of a design convention with illustrative values.
- Match the title verb to the V7 grade. Documented supports record and event language. Well-supported supports a direct finding. Plausible takes "can" or "may." Hypothesis is labeled as untested. Contested shows both readings.
- Source line format: publisher, title or table, observation period, geography, date retrieved, and the qualification that matters.
- Every public policy statistic in a specimen carries its source, observation period and relevant qualification.
- Label illustrative people, quotes, places and figures beside the item.
- Cite formal accessibility and technical guidance. Label design judgments as judgments.
- Real evidence imagery comes from real sources with credits. Conceptual and stock context carry labels.

---

## 16. Photography, illustration and video

- Keep the documentary photography direction: photograph the process. Add rules for selection, cropping, captions (who, what, where, when), credits, consent and rights, and alt text written for purpose.
- Illustration: define where hand-drawn spot illustration, exploded diagrams and generated conceptual images may appear, and how each is labeled.
- Image generation is allowed for conceptual illustration and mockup context. Use a connected image tool if the session has one. Otherwise write the generation prompt, a suggested filename, and a labeled placeholder. Record the tool, date, prompt and terms of use in the rights ledger. Never use a generated image as evidence.
- Video supports an explanation. Define short-video structure, open and closed captions, transcripts, title and end frames, and a useful fallback when an embed fails (poster frame, transcript link and summary). No autoplay with sound.

---

## 17. Motion and states

- Motion explains a state or a mechanism.
- Playback for video and loop demonstrations stays reader-controlled, with pause and reset and an equivalent still view.
- Honor `prefers-reduced-motion`. Keep native scrolling. No scroll hijacking.
- Replace the pulsing loading state with an accessible pattern that has visible text and a still alternative.
- Document durations and easings as tokens, with the three V5 behaviors (slide, draw, land) refined or kept.

---

## 18. Applications

Each application needs finished content, spacing, hierarchy, exact dimensions, safe areas, minimum sizes and export specifications, shown at full size. Thumbnail rows may supplement the full-size views. The research lead checks every platform specification on its official help page on the execution date and records the date. The sizes below are starting points to verify.

| Application | Deliverables | Starting sizes to verify |
|---|---|---|
| Web | Desktop and mobile mastheads, home navigation, footer, atlas detail and evidence view | 1440, 1024, 390 and 360 px widths |
| Newsletter and Substack | Masthead, email header and footer, article opener, divider, one complete working email built for email-client constraints | Substack logo, wordmark and cover sizes from Substack's help center; email body 600 to 640 px |
| Social | Avatar, horizontal banners, square and portrait posts, a carousel sequence, share preview | Avatar 400 x 400 with circle-safe area; square 1080 x 1080; portrait 1080 x 1350; vertical 1080 x 1920; Open Graph 1200 x 630; X header 1500 x 500; LinkedIn banners per current spec |
| Reports | Cover, executive brief, chart page, evidence spread, source notes, closing page | US Letter, 8.5 x 11 in, with bleed and margins stated |
| Print and presentation | One-page explainer, letterhead, slide cover, content and data layouts, event sign | US Letter; slides 1920 x 1080; event poster 24 x 36 in; table sign 11 x 17 in |
| Video | Accessible title and end frames | 1920 x 1080 and 1080 x 1920, with caption-safe areas |

Representative applications are resolved jointly by the design director and the UX lead. The atlas detail and evidence view should draw on the favored concepts: 03 Field Manual, 09 The Circuit, 10 Who Can Act and 11 Register.

Content for applications uses real Oath & Action material where it exists and real public examples found by the research lead, or carries illustrative labels beside the item.

---

## 19. Reports

Give the existing twelve-page report a complete editorial and visual pass. The V5 sequence includes narrative, system map, evidence, comparison, case study, "What you can do," sources and back cover. Keep the report reader working with keyboard support and page controls. Every page passes the rubric. Show the cover, executive brief, chart page, evidence spread, source notes and closing page at full size.

---

## 20. Asset package

```
deliverables/
  YYYYMMDD_Oath-And-Action-Brand-Guide_V6.html
  YYYYMMDD_Oath-And-Action-V6-Change-And-Validation-Report.md
  oath-and-action-v6-asset-package/
    YYYYMMDD_Asset-Index.md
    YYYYMMDD_AI-Builder-Implementation-Brief.md
    identity/          wordmark, ampersand, hinge, lockmark, Signal Grid: SVG masters and PNG variants
    symbols/           pillars, topics, atlas, status, encoding, utility: 16, 24 and 48 px SVG, plus PNG where useful
    graphics/          devices, patterns, dividers, watermarks
    data-viz/          palette specification, chart templates as SVG, specimen data as CSV
    applications/      email HTML, social templates, slide and letterhead templates
    tokens/            tokens.css, tokens.json, a generation script
    fonts/             font files permitted for redistribution, with license texts
    licenses-and-credits/
```

- Filenames follow the convention, for example `YYYYMMDD_Wordmark-Charcoal-On-Newsprint.svg`. Keep each internal ID (for example `oa-wordmark`, `ic-housing`) in the SVG `id` and in the index.
- The index lists every file with its ID, purpose, sizes, surfaces and the guide section that governs it.
- The AI builder brief tells a builder how to choose tokens, symbols, chart types and applications, with do and avoid examples and the rules that matter most.
- The guide works without the package. The package contains usable assets.

---

## 21. Engineering

- Extract the sources with scripts into `work/extract/`. Build V6 from modular partials in `work/build/` and assemble one self-contained HTML file with embedded fonts, vectors, styles and scripts.
- Tokens drive the guide's CSS. A test fails if the guide's computed values and the token files disagree.
- Every download button produces a usable file. Standalone SVG exports resolve `<use>` references, inline required styles and include `title` and `desc`. PNG exports have exact dimensions and the stated background.
- Include font license details and redistribute only what the license permits.
- Keep the file under 16 MB. Subset fonts where the license allows.
- Produce a PDF only if Dustin asks or if a complete, accessible export can be verified without reducing the main deliverables.

---

## 22. Accessibility and verification

Target WCAG 2.2 AA. Use https://www.w3.org/WAI/WCAG22/quickref/ for criteria.

| Check | Method |
|---|---|
| Every chapter rendered | Playwright screenshots at 1440, 1024, 390 and 360 px |
| All report pages | Screenshot each page in the reader |
| Keyboard and focus | Scripted tab order plus manual review of order and visibility |
| Reading order and headings | Accessibility tree outline |
| Automated rules | axe-core on every chapter |
| Contrast | Script on rendered colors for text, graphics and component states |
| 200% text zoom and 320 px reflow | Screenshots with no lost content |
| Reduced motion | Emulated `prefers-reduced-motion` |
| Forced colors | Emulated forced-colors mode |
| Dark surfaces and long labels | Specimens on Charcoal and Prussian surfaces, and with the longest real labels, such as full V7 variable and reform titles |
| Print | Print emulation and a print stylesheet |
| Downloads | Click each button, open each file, check SVG validity and PNG dimensions |
| Diagram and chart equivalents | Each has a text or table equivalent and a reading guide |
| Grayscale | Grayscale screenshots of every data and systems specimen |

Report completed checks and checks the environment could not run as separate lists.

---

## 23. Writing

Follow the writing rules in `CLAUDE.md`. In addition:

- Improve the explanation of every important rule and asset: what it communicates, how a person reads it, where it belongs, and why the treatment helps.
- Concrete examples teach the principle.
- Explain terminology at first use. Use V7's glossary definitions when they fit, quoted or credited.
- Keep research citations out of brand voice specimens unless the specimen needs them.

---

## 24. Deliverables and definition of done

1. `YYYYMMDD_Oath-And-Action-Brand-Guide_V6.html`, named with the execution date.
2. The asset package in section 20.
3. `YYYYMMDD_Oath-And-Action-V6-Change-And-Validation-Report.md`: resolved conflicts, identity refinements, new assets, test results, and remaining factual and rights questions.

Done means all of the following are true:

- [ ] Every V5 Polished chapter's substance appears in V6, mapped in the report.
- [ ] Every chapter follows the template in section 7 and scores at least 4 on every rubric criterion.
- [ ] The fifteen tensions in section 8 are resolved and shown.
- [ ] Approved identity refinements are applied everywhere, with before and after in the report.
- [ ] Pillar marks, twenty refined topic symbols and the derived atlas, status, encoding and utility symbols exist as 16, 24 and 48 px masters where useful.
- [ ] At least twenty data and systems specimens meet section 13, and the six worked examples meet section 14.
- [ ] Every application in section 18 is finished at its exact size, with verified specifications.
- [ ] The twelve-page report has passed a full editorial and visual review.
- [ ] Tokens match the visible guide in CSS and JSON, and the "How to choose a token" guide exists.
- [ ] Every download works and uses a dated descriptive filename.
- [ ] The verification matrix in section 22 is complete, with untested items listed.
- [ ] The research and rights ledgers are complete, and nothing that may not ship is shipped.
- [ ] No locked line has changed without Dustin's approval.
