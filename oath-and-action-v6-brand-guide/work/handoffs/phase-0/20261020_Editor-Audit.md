# Editor audit of V5 Polished

Phase 0, oa-editor. Every change below is a proposal. [07] is a chapter and p05 a report page. The scripts are in `work/build/scripts/phase-0/`. CSS classes set most of the red, so I also counted red on the screenshots.

## 1. Locked lines

Every occurrence is worded exactly. The gaps are in placement.

| Line | Exact uses | Gaps |
|---|---|---|
| Tagline | 10 in text: [00], [02], six in [13], p12 and [17]. It also appears in the L4, L5 and L6 artwork. | [02] says the tagline closes the newsletter ending, and the [13] ending omits it. The L5 and L6 descenders look clipped in the [03] capture. |
| Mission | 2: [01] and [02] | Absent from the report. Near echoes: "the rules that shape our lives" [00] and "gives people a practical way to take part" [01]. |
| Reader promise | 3: [02], the [13] newsletter and p12 | [02] puts it "under the masthead on the home page". Neither home demo carries it. |
| Editorial commitment | 2: [02] and the [13] letterhead | [02] puts it "in the colophon and the method page". Both p11 and the [15] colophon omit it. |
| Pillar order | All in order: 20 runs by script, plus [02] | Five script flags in [08] were false alarms. |

For Dustin: [02] lists the voice line ("We explain the rules. We expose the gaps. We connect people to action. We act.") with the locked lines. Brief section 3 doesn't lock it.

## 2. Voice

By script: 0 em dashes, 3 en dashes in ranges, "simply" once [12] and "leverage" three times as a noun. The four listed fillers appear only in the [02] banned list. I counted the rest by reading.

| Pattern | Count | Examples |
|---|---|---|
| Corrective negation | 12 | "Photograph the process, not the idea of it." [10]; "Hairlines, not boxes." [15] |
| Contrasting pairs | 13 | "understanding on one side, impact on the other" [01]; "Written testimony counts. Spoken testimony counts more." [13] |
| Rhetorical triplets | 20 | "the places we live, the work we do, and the future we share" [01]; "the line, the gap it opens, and the move that closes it" [13] |
| Parallel runs | 8 | the voice line [02]; "The lever is simply there. The hinge is already assembled." [12] |
| Setup and payoff | 9 | "The lever. One point moves the structure. Find it." [13]; "We read it so you can change it." [13] |
| Slogan closers | 8 | "Put the promise to work." [17]; "Institutions endure when people act." [02] |
| Summary beats | 6 | "so it gets a chapter of its own" [04]; "This is how the grid ties to topics." [07] |
| Stacked nouns | about 25 | "Report cover kicker on Prussian" [07]; "Compact secondary cluster for document footers" [03] |
| Nominalizations | 12 | "An allocation alone establishes no claim about service quality." p07; "Decorative opacity is reserved for watermarks" [03] |
| Hedges | 8 | "at least about 11 px" [16]; "usually shorter than this paragraph" [13] |
| Inflated adjectives | 6 | "the most ownable asset" [04]; "fully resolved" [13] |

"Rule, gap, move" repeats at least eight times. "We expose the gaps" and "Who wrote the rule you are angry about?" assume a grievance, against [02]'s "let readers decide".

**Headlines.** Three give an instruction:
- 10 "Photograph the process, not the idea of it." It relies on corrective negation.
- 11 "The chart proves the sentence." The word "proves" overclaims for estimates (brief 15).
- 16 "Make the mechanism easier to see."

05 "Newsprint carries the conversation." comes close. The other thirteen:
- Fragments: 02 "Clear enough to invite someone in.", 03 "A strong center. Room around it.", 06 "A voice you can recognize." and 07 "A structure you can read."
- Contrasting pairs: 04 "One character, a wider range.", 08 "Four silhouettes, one family." and 13 "Fewer applications, fully resolved."
- Descriptions: 01 "People belong in the picture.", 09 "Twenty subjects, drawn like a typeface.", 12 "Things slide, draw and land." and 14 "A complete argument, page by page."
- Slogans: 15 "The working rules stay with the work." and 17 "Put the promise to work."

Proposal: make each headline the chapter's main instruction, such as "Give red one job." for [05].

## 3. Terminology

| Term | First use | Problem |
|---|---|---|
| lockmark | [07] | Never defined. [03] and the alt text call it the "mechanism grid", and [01] calls it "the grid". |
| Signal Grid | [07] | Its corners and routes appear in [01] and [02] before it is named. |
| lever | [02] | First defined in [07]. It also names the Act mark [08], R2's red emphasis [15] and a policy point [11]. |
| hinge | [01] | Reused, undefined, for the hinge gap, headline, diagram, divider and motion. |
| container marks | [04] | The guide never says what a container is. C1 to M1 go unexplained, and there is no S1. |
| keyline | [04] | Means both the 1 px edge and the icon construction shapes [09]. |
| stock, flow | [04], p09 | "Stock" appears only as paper. "Flow" is defined on p09, never in [16]. |
| polarity, delay, reinforcing loop | [16] | Defined only inside SVG images. The chapter text and alt text say "positive" and "plausible" without a key. |
| evidence grade, Act context, dark beat | [16], [09], [05] | Undefined at first use. |
| unenrolled, cloture, reported out | [02], [07], [13] | Undefined, though the tracker stages depend on them. |
| R1 | [15] | Collides with Loop R1 and Reform R-28 [16]. |

## 4. Illustrative status

Seven items carry an adjacent label: six source lines in [11] and [13], and one row on p11. The rest rely on four global notes, in the [13] intro, the [11] intro, the [15] colophon ("application examples" only) and p11. The p11 note says the figures are labeled in the colophon, and the colophon has no label.

Unlabeled items, highest risk first:
1. Testimonials with a name, town and job. [10] presents Maria T., Derek O. and Priya N. as quotes "from readers". [13] reuses them on quote cards, a pull quote and a witness badge, and p05 reuses Maria T.
2. Real publishers credited for invented data: "legislature.ma.gov bill history" [13] and "Secretary of the Commonwealth" [06].
3. Unsourced policy figures: "In 23 states the primary is closed to 40 percent of registered voters." [02] and "Fifteen states do not." [13].
4. Real places attached to invented events: Melrose Public Library at 69 West Emerson Street, and Room A-1 in the State House [13].
5. Invented records and names: "Town budget, fiscal 2026, table 4" (p07); bill numbers such as H.4212 [07, 09, 13]; "Chair Whitcomb" and "Merrimack Valley Civic Lab" [04, 13].
6. "M.G.L. c. 53, § 37" [13] reads as a real citation and needs a check.

## 5. Contradictions

| # | Rule | Demonstration and evidence |
|---|---|---|
| 1 | Small text is 13 px minimum [15] | Labels are set at 10 to 12 px [06, 07, 11]. The census found 833 of 2,346 elements under 13 px. |
| 2 | No Stone small text on Newsprint [15]; Verdigris "Not text" [05] | The census shows 49 Stone and 10 Verdigris text elements on Newsprint, among them the tracker stage labels [13]. |
| 3 | White on red only at 18.66 px bold [05] | The [08] nav Subscribe button is 12 px, and "Open the script" is 16 px [13]. |
| 4 | Two opacities only [05] | The Loading pulse runs from .2 to .5, the icon keylines sit at .6 [09] and the cap seam at .3 [13]. |
| 5 | "Never: looping animation" [12]; "No autoplay" [15] | Loading runs `pulse 1.2s ease-in-out infinite` with no visible text. The lever reveal plays on page load [12]. |
| 6 | Focus offset is 2 px [12] | [15] and the CSS both use 3 px. |
| 7 | Buttons "darken by one step" [12] | On hover, Charcoal turns to Prussian, which is lighter. |
| 8 | Red does one job [05] | Beyond the identity marks, red does two jobs in the newsletter and article and three on the home page and one-pager [13]. The posters count the exempt lever [08]. |
| 9 | All nav marks are Charcoal [08] | The home page nav shows a red Act lever [13]. |
| 10 | Never red against green [05] | Deltas pair red with Verdigris, a blue-green. This is my judgment. |
| 11 | The title states what the chart proves [11] | "Closed primaries are the largest group." sits over bars of Closed 15 and Open 18. "Twelve years" labels an axis that runs 2014 to 2024. |
| 12 | Demo facts | Closed-primary states number 23 in [02] and 15 in [13]. [13] says Massachusetts already lets unenrolled voters choose a party ballot, yet H.4212 "would open the primary" to them. The newsletter swaps two bills' stages [13]. |
| 13 | Dates | November 4, 2026 is a Wednesday, though p10 calls it a Tuesday. November 6 [13] is a Friday, though the page calls it a Thursday. |
| 14 | Report consistency | p03 counts 4 handoffs, while p08 shows routes of 5 and 3. p02 promises "the route to a hearing", yet the p06 route has no hearing. |
| 15 | Mono below 80 px [03] | C1, C2, C3 and S2 carry red at 16 px [04], and L2's minimum size is 72 px. |
| 16 | Red on Prussian at display size only [03] | C3 shows red on Prussian at 16 px [04]. |
| 17 | Grid in mono below 32 px [07] | The kicker grids are in color at 22 px. |
| 18 | S2 is the favicon [04] | L8 [03] and the mono grid [07, 13] also claim the job. |
| 19 | Misuse: "The lever recolored" [07] | The Active state turns the lever Verdigris. On p01 a Verdigris tracker node marks a research brief. |
| 20 | "No boxes, no cards" [15] | `.card` and the specimen frames draw boxes. |
| 21 | Email uses system fonts [06] | The email headline is set in Inter Tight. |
| 22 | Captions name the place and date [10] | No photo caption does. |
| 23 | Hinge headlines name the rule first [02] | "The hearing & the vote." puts an event first. |
| 24 | File names start with the date [15 checklist, CLAUDE.md] | The asset index uses `OA_C1.svg`. The checklist skips R4 and R10. V5 Polished has R1 to R10, though brief tension 7 says R1 to R9. |
| 25 | Spell out acronyms on first use [15] | RCV, M.G.L., PDF/A and WCAG are never spelled out. |

I found no tint values in the CSS or the markup. The "no tints" rule still conflicts with what hover states and charts need.

## 6. Copy worth recovering

- V4.2 labels each sample in place ("SAMPLE / Fictional process and quantities.") and gives source slots ("[Publisher, budget year, table, URL]"). That pattern fits tension 6.
- V4.2: "Replace the fictional values and source slots with verified evidence before publication."
- V4.2: "Give every handoff an owner." and "Each state keeps its label visible."
- V4.2: "A proposed change describes an intention. A published outcome shows what happened."
- V4.2 says what each library symbol means, such as "Several inputs meet one accountable seat."
- V5: "OATH always sits left. The arc stays dotted." and "Every icon ships with a label."
- The [16] figures: "'Positive' describes direction." and "Thickness never implies an unmeasured effect size."

## 7. Sample rewrites

1. [05]
   - Original: "Red is punctuation. One job per composition: a button, a data point, a rule under a headline, the current step."
   - Revision: "Give Pillar Red one job in each layout, such as the main button or the data point the headline is about."
   - Why: an instruction replaces the metaphor.
2. [03]
   - Original: "Over a photograph the lockup sits in a Newsprint or Charcoal field, never directly on the image."
   - Revision: "To place the logo over a photograph, set it on a solid Newsprint or Charcoal panel first."
   - Why: it drops the corrective negation.
3. [03]
   - Original: "Clear space 1.0x on every side. Nothing enters it: no type, no rule, no edge of a photograph."
   - Revision: "Leave an empty margin around the wordmark as wide as its capital letters are tall. Keep type, lines and photo edges out of it."
   - Why: it explains x.
4. [12]
   - Original: "The lever lands only at stage nine. A user controls the sequence; it never plays on its own."
   - Revision: "The reader starts each step. The lever, the larger node at the bottom right, turns red only when the bill takes effect."
   - Why: it defines the lever and uses the active voice.
5. p05
   - Original: "Describe when a person can participate, what they need to submit, and where the response is recorded."
   - Revision: "Tell readers when they can take part and what to send. Then show them where the answer will be published."
   - Why: it uses plainer verbs and drops the triplet.

## Tested and not tested

Tested: scripts over chapter text and alt text, the CSS rules, red on screenshots, chart values from SVG geometry, 2026 weekdays, and a full read of V5 Polished and V4.2.

Not tested: the 390 px screenshots, the Atlas Visual System, Concepts V2, and whether the named bills and people exist.

## Change log

Created `editor_audit_scan.py` and `editor_red_count.py` in `work/build/scripts/phase-0/`, plus this file. Modified: none.
