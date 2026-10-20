# Oath & Action V6 prompt: revision notes

Written October 20, 2026. These notes explain how the prompt pack differs from your draft prompt, where each of your requirements now lives, what I corrected, and what the research check found.

## How the prompt changed

Your draft asked for everything in one run. The pack splits it into a master brief, six phase prompts, Claude Code operating rules, and seven studio agents.

- **Gates at every stage.** You asked to review after the review and plan, and again before anything changes. Each phase now ends at a gate. Each gate approves the next phase's proposal. Identity geometry and locked lines need their own named approval, shown side by side at real sizes.
- **Built for Claude Code.** `CLAUDE.md` loads in every session and carries the gate rules, your naming convention, your writing rules and the honesty rules. The seven agents in `.claude/agents/` are real subagents with defined jobs, standards and sign-offs. Ledgers in `work/ledger/` carry decisions from one session to the next, so each phase can start fresh.
- **A researcher added.** `oa-research-lead` verifies awards, finds real examples and public data, checks platform specs and legislative workflows, and keeps a rights ledger.
- **A defined quality bar.** "World-class" is now a list of observable tests and a six-part rubric. Every item has to score 4 of 5 on each part before it ships.
- **Large files handled safely.** The builder splits the 3 to 4 MB source files with scripts and never loads one whole, so the context does not overflow.
- **Grounded in Atlas V7.** The systems grammar maps to V7's own fields: variable types, connection types, signs, delays, grades, closure, reforms, effect codes, routes, and the repair and delivery logs. The worked examples quote real V7 IDs and values, and a script confirmed them.

## Corrections to the draft

| Draft said | Fact | Change |
|---|---|---|
| `20261018_Oath-And-Action-Brand-Guide_V5-Polished(1).html` | The file has no "(1)" | Exact names listed in the brief and run guide |
| "Atlas & Brand.zip" with a nested systems-map folder | Two zips: `data_viz.zip` and `Design_I_like.zip`. The systems-map folder sits inside the second, named `Systems Map and Atlast Design Ideass/` | Sources table rewritten |
| "The older V5 inside the ZIP is background" | V5 and V4.2 were supplied as separate files. Neither zip holds a guide | Both listed as background. V4.2's dropped chapters flagged for recovery |
| Atlas IDs and grades come from "the original atlas" | They come from `20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html`, snapshot October 15, 2026 | Named as the model authority |
| "Give me a concise initial review and work plan, then continue into execution" | Conflicts with your rule to wait for your go | Phase 0 stops at Gate 0 |
| Icon studies described as "geometric pillar studies" and "Y2K references" | There are eight sheets, 01 to 08. 04, 05 and 08 were only pasted in chat | All eight mapped to roles in the brief. 04, 05 and 08 copied into `project-kit/source/icon-studies/` |

## New findings the prompt now addresses

These came from inspecting the files. None was in the draft.

1. **Colliding IDs.** Variable IDs B2 to B5 match loop IDs B2 to B5 in V7. Loop R1 sits beside reform R-01. V5's Standards chapter numbers its rules R1 to R9 too. The brief asks for typed ID chips and renumbered rules.
2. **Grade labels differ across V7 records.** Connections use "well-supported" and "plausible_contested." Issues use "well_supported" and "retired." Claims use "contested." The methods text also defines "Mixed." The brief asks for one display vocabulary and a mapping table, with V7 left untouched.
3. **Measured contrast problems.** Stone on Newsprint is 4.29:1, below the 4.5:1 needed for small text. Pillar Red on Newsprint is 2.96:1, below the 3:1 needed for informative graphics. Red text fails at small sizes on every surface. The full table is in brief section 8.
4. **Lost chapters.** V4.2 had Mastheads, Watermarks, Symbol Library, Relationships, Publications, Footers, Social and Specifications. V5 dropped them. The brief asks the builder to recover what is useful.
5. **Your favored concepts.** Your saved screenshots show 03 Field Manual, 09 The Circuit, 10 Who Can Act and 11 Register. The brief names them for the atlas applications.
6. **Concept 10 draws ordinal effects as widths.** V7 effects are categories (+L to −M and ?). The brief asks for an ordinal legend or a different encoding.
7. **Partisan pairing risk.** Study 05 Hand Drawn pairs red and blue figures and uses a Capitol dome and scales of justice. Red and blue diverging chart scales carry the same risk. The brief rules out both.
8. **The geometric pillar study has watch points.** Track's three circles can read as a status light. Act's quadrant can read as a D or a play button. Red appears in all four marks.
9. **V7 already sets some drawing rules.** Hypothesis links are dotted. Outside drivers are rounded pills. A plus sign does not mean a benefit. The atlas does not sum reform effects into a score. The brief tells the guide to agree with these rules.

## Where each draft requirement lives

| Draft requirement | Location in the pack |
|---|---|
| Read the full V5 Polished: sprite, fonts, chapters, specimens, report reader, exports, scripts | Phase 0 steps 2 and 3; brief section 2 |
| Inspect the atlas and the eleven concepts | Phase 0 step 4; brief sections 2 and 14 |
| Open the data viz, Design I like and systems-map references | Phase 0 steps 2 and 4 |
| V5 as authority, older versions as background, a newer approved guide supersedes | Brief section 2, order of authority |
| Agents for brand strategy, iconography, UX and accessibility, data viz, editor and engineer | `.claude/agents/`; brief section 4 |
| Design and UX jointly resolve representative pages | Brief sections 4 and 18; Phase 4 step 3 |
| State accurately when separate agents were not used | `CLAUDE.md`; brief section 4 |
| Initial review and plan | Phase 0 |
| Routine decisions and a compact change ledger | `CLAUDE.md`; brief section 5 |
| Continue until finished; an audit alone does not count | Brief sections 1 and 24 |
| Foundations table and locked lines | Brief section 3 |
| Wordmark, ampersand, hinge, lockmark and Signal Grid refinement, shown and compared | Brief section 9; Phase 1 step 4; Phase 2 step 1 |
| A font substitution is not a finished identity decision | Brief section 3 |
| Replace the OA_* download names | Brief sections 8 and 20 |
| Art direction and the symbol family from the geometric, Y2K and isometric studies | Brief section 11 |
| 2026 research with verified status and a research-to-design ledger | Brief section 5; Phase 1 step 1; research agent |
| Contents, anchors, navigation, measures and cross-references | Brief section 7 |
| Rule, purpose, correct application and failure case in every chapter | Brief section 7 template |
| The six tensions | Brief section 8, items 1 to 6 |
| Configurable tracker workflows | Brief sections 8 and 14 |
| Identity versus data color, new token rules, measured contrast, all states | Brief section 10 |
| Tokens in CSS and JSON, and how to choose a token | Brief sections 10, 20 and 21 |
| Pillar marks, twenty topic icons, derived atlas symbols, 16, 24 and 48 px masters | Brief section 11 |
| Graphic devices; vectors versus generated imagery | Brief sections 12 and 16 |
| Every production application at exact size | Brief section 18; Phase 4 |
| A full pass on the twelve-page report | Brief section 19 |
| A data viz chapter: selection guide, twenty or more specimens, palettes, complex examples | Brief section 13; Phase 3 |
| Systems grammar, worked examples, reconciliation, encoding limits | Brief section 14; Phase 3 |
| Lessons from Our World in Data, LOOPY and En-ROADS | Brief sections 13 and 14 |
| Evidence honesty, illustrative labels, sourced statistics | Brief section 15 |
| Photography, video and image rights | Brief section 16 |
| Motion | Brief section 17 |
| Self-contained guide, working downloads, SVG and PNG export, font licenses | Brief section 21 |
| WCAG 2.2 AA and the rendered test matrix | Brief section 22 |
| Plain language rules | `CLAUDE.md`; editor agent; brief section 23 |
| The three deliverables and the PDF condition | Brief sections 21 and 24; Phase 5 |
| Naming convention | `CLAUDE.md` |
| Context: the latest trends, 2026 award winners, and the best interactive tools | Brief section 5; Phase 1 step 1 |
| Context: a researcher to strengthen evidence and real-world examples | Research agent; brief section 15 |
| Context: design and brand experts to raise the work to best in class | Creative director and design director agents; brief section 6 |

## Research check

A research agent checked every award and reference in your draft on October 20, 2026. This cloud session's network policy blocked page fetches, so each check rests on search results from the official domain. The builder's research agent will open the pages and verify them again in Phase 1. The full ledger is `project-kit/brief/20261020_Research-Verification-Ledger.md`.

| Draft claim | Result | Wording now in the brief |
|---|---|---|
| Cooper Hewitt 2026: Thought Matter for Communication Design, Laura Kurgan for Digital Design | Confirmed | Adds the dates (announced February 25, 2026; gala May 19, 2026) and points to Kurgan's Million Dollar Blocks on Columbia's site |
| Fieldwork Facility's Storehouse: Transform Awards Europe Gold, March 2026 | Confirmed, with a correction. The Gold is for Best wayfinding or signage, credited to the V&A and Fieldwork Facility, at the March 26, 2026 ceremony | States the category and adds the ADC 105th Best of Discipline listed by The One Club |
| Shopify's Renaissance Edition: Awwwards Site of the Month, February 2026 | Confirmed. Awwwards lists it as "The Renaissance Edition." Shopify released it on December 10, 2025 | Uses both names and the release date |
| Adobe 2026 creative forecast | Confirmed. Four trends: All the Feels, Connectioneering, Surreal Silliness, Local Flavor | Labeled vendor marketing research |
| Canva 2026 design forecast | Confirmed. "Imperfect by Design," published December 2025, names ten trends | Labeled consumer template styles, used selectively |
| Our World in Data redesign post | Exists. It dates from about 2023 | Labeled older |
| LOOPY and En-ROADS | Confirmed. LOOPY dates from 2017 | LOOPY labeled older. En-ROADS framed as "what-if," never a forecast |
| WCAG 2.2 Quick Reference | Confirmed | Unchanged |

New formal awards the agent found and added: SND47 (2026), the 2025 Online Journalism Awards (CalMatters Digital Democracy and The Globe and Mail's "House Poor"), the 2026 Sigma Awards ("Invisibles"), and the most recent Information is Beautiful Awards (presented June 2025).

To avoid citing as current: Malofiej (no 2025 or 2026 edition found), the Brand New Awards (ended in 2015), and the old "Kantar" name for the Information is Beautiful Awards. Individual D&AD 2026 Yellow Pencils and the Webby 2026 data visualization winner are confirmed only by the makers or secondary outlets, so the brief tells the builder to re-check them.

## Checks run on this pack

Checks that ran:

| Check | Result |
|---|---|
| Atlas V7 values quoted in the brief (counts, types, signs, grades, the R1, R8, B4 and R10 chains, Reform R-01, authority links, closure, routes, logs, effect codes) checked by script against the V7 JSON | 37 of 37 match |
| Palette contrast in brief section 8, computed with the WCAG formula | Table generated from the locked hex values |
| File names against your convention | All pass. `CLAUDE.md` and the seven agent files keep the names Claude Code requires |
| Folder names | All lowercase kebab-case |
| Em and en dashes in every file | None |
| Banned words | None remain in my writing. The only matches are the title of Bloomberg's "What's Really Warming the World?" and the V7 field name `leverage` |
| Section references in the agents and phase prompts | Every cited brief section exists |

Checks that could not run here:

- URL loading. The session's network policy blocks direct requests, so I could not open the 70 URLs in the pack. The research agent confirmed that each URL your draft cited appears as a live result on its official domain.
- Running the prompts. The phases have not been executed. Claude Code should list the seven agents when you type `/agents` in the project folder. The run guide covers this.

## Questions you may want to settle early

The builder will raise these at Gate 0. You can answer them now if you like.

1. Should a future atlas edition fix the colliding IDs and the grade labels inside the model itself? This commission only works around them in the display.
2. Do you have photographs you own or license for the documentary direction? If not, the builder will use labeled placeholders and generated context images.
3. Which platforms matter at launch? The application list covers Substack, email, X, LinkedIn, Instagram-sized posts and Open Graph. Remove any you won't use, to save effort in Phase 4.
