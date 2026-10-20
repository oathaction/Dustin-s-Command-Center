# Editor audit of V5 Polished

Phase 0, oa-editor. This is a review, so every change here is a proposal. [07] means chapter 07; p05 means report page 5. Scripts are in `work/build/scripts/phase-0/`. `editor_audit_scan.py` checks locked lines, pillar order, listed words and first uses. `editor_red_count.py` counts red per figure. CSS classes set most red, so I also counted red on the screenshots.

## 1. Locked lines

Every occurrence is worded exactly. The gaps are in where the lines appear.

| Line | Exact uses | Gaps |
|---|---|---|
| Tagline | 10 in text: [00], [02], [13] (Substack, home footer, carousel, slide cover, closing slide, email signature), p12, [17]. Also in L4, L5 and L6 artwork. | The [02] rule says it closes the newsletter ending, but the [13] ending leaves it out. L5 and L6 descenders look clipped in the [03] capture. The L4 alt text never says the line. |
| Mission | 2: [01], [02] | Absent from the report. Two near echoes sit beside it: "the rules that shape our lives" [00] and "gives people a practical way to take part" [01]. |
| Reader promise | 3: [02], [13] newsletter, p12 | [02] puts it "under the masthead on the home page". Both home demos leave it out. |
| Editorial commitment | 2: [02], [13] letterhead | [02] puts it "in the colophon and the method page". p11 and the [15] colophon leave it out. |
| Pillar order | 20 runs, all in order | The script flagged five runs in [08]. Each was its search window spanning two sentences. |

For Dustin: [02] lists the voice line ("We explain the rules. We expose the gaps. We connect people to action. We act.") with the locked lines, though brief section 3 doesn't lock it.

## 2. Voice

The script found 0 em dashes and 3 en dashes, all in ranges. Genuinely, really, truly and actually appear only in the [02] banned list. "Simply" appears once [12]. "Leverage" appears 3 times, always as a noun [07, 11]. I counted the rest by reading.

| Pattern | Count | Examples |
|---|---|---|
| Corrective negation | 12 | "Photograph the process, not the idea of it." [10]; "Hairlines, not boxes." [15] |
| Contrasting pairs | 13 | "understanding on one side, impact on the other" [01]; "Written testimony counts. Spoken testimony counts more." [13] |
| Rhetorical triplets | 20 | "the places we live, the work we do, and the future we share" [01]; "the line, the gap it opens, and the move that closes it" [13] |
| Parallel runs | 8 | the voice line [02]; "The lever is simply there. The hinge is already assembled." [12] |
| Setup and payoff | 9 | "The lever. One point moves the structure. Find it." [13]; "We read it so you can change it." [13] |
| Slogan closers | 8 | "Put the promise to work." [17, p10]; "Institutions endure when people act." [02] |
| Throat-clearing, summary beats | 6 | "so it gets a chapter of its own" [04]; "This is how the grid ties to topics." [07] |
| Stacked noun phrases | about 25 | "Report cover kicker on Prussian" [07]; "Compact secondary cluster for document footers" [03] |
| Nominalizations | 12 | "An allocation alone establishes no claim about service quality." p07; "Decorative opacity is reserved for watermarks" [03] |
| Hedges | 8 | "at least about 11 px" [16]; "usually shorter than this paragraph" [13] |
| Inflated adjectives | 6 | "the most ownable asset" [04]; "fully resolved" [13] |

The "rule, gap, move" formula repeats at least eight times in [13] and the report. Two lines assume a grievance, "We expose the gaps" and "Who wrote the rule you are angry about?", even though [02] tells writers to let readers decide.

**Chapter headlines.** Three give an instruction: 10 "Photograph the process, not the idea of it." (it leans on corrective negation), 11 "The chart proves the sentence." ("proves" overclaims for estimates and illustrations, brief 15) and 16 "Make the mechanism easier to see." One comes close: 05 "Newsprint carries the conversation." The rest describe or sell:

- Fragments: 02 "Clear enough to invite someone in.", 03 "A strong center. Room around it.", 06 "A voice you can recognize." and 07 "A structure you can read."
- Contrasting pairs: 04 "One character, a wider range.", 08 "Four silhouettes, one family." and 13 "Fewer applications, fully resolved."
- Statements: 01 "People belong in the picture.", 09 "Twenty subjects, drawn like a typeface.", 12 "Things slide, draw and land." and 14 "A complete argument, page by page."
- Slogans: 15 "The working rules stay with the work." and 17 "Put the promise to work."

Proposal: make each headline the chapter's main instruction, such as "Give red one job." for [05].

## 3. Terminology

| Term | First use | Problem |
|---|---|---|
| lockmark | [07] | Never defined. The same mark is "mechanism grid" in [03] and its alt text, and "the grid" in [01]. |
| Signal Grid | [07] | Its corner and route ideas appear in [01] and [02] before it has a name. |
| lever | [02] | Defined only in [07]. It also names the Act mark's drawing [08], R2's "one red emphasis" [15] and a policy point [11]. |
| hinge | [01] | Reused for the gap, headline, diagram, divider and motion without separate definitions. |
| container marks | [04] | Never says what a container is. C1 to M1 go unexplained, and there is no S1. |
| keyline | [04] | Means both the 1 px edge [05] and the icon construction shapes [09]. |
| stock | [04] | Appears only as paper. p09 describes a stock without naming it. |
| flow | p09 | Defined well there, never in [16]. |
| polarity, delay, reinforcing loop | [16] | Defined only inside the SVG images. Chapter text and alt text say "positive" and "plausible" without a key. |
| evidence grade, Act context, dark beat | [16], [09], [05] | Undefined at first use. |
| unenrolled, cloture, reported out | [02, 07, 13] | Undefined, though the tracker stages depend on them. |
| R1 | [15] | Collides with Loop R1 and Reform R-28 [16]. |

## 4. Illustrative status

Seven items carry an adjacent label: four source lines in [11], two in [13] and one row on p11. V5 relies on four global notes: the [13] intro, the [11] intro, the [15] colophon, and p11, which says the figures "are labeled as such in the colophon". The report's colophon has no such label. The [15] note covers "application examples" only.

Unlabeled, highest risk first:

1. Testimonials with name, town and job. [10] has Maria T., Derek O. and Priya N., presented as "quotes ... from readers". [13] has the Derek O. pull quote, the Hank W. and Rosa M. cards, and Maria T.'s witness badge. Maria T. appears again on p05.
2. Real publishers credited for invented data: "legislature.ma.gov bill history" [13] and "Secretary of the Commonwealth, enrollment statistics" [06].
3. Unsourced policy figures: "In 23 states the primary is closed to 40 percent of registered voters." [02], "It received 56." [02] and "Fifteen states do not." [13].
4. Real places with invented events [13]: Melrose Public Library at 69 West Emerson Street, Room A-1 in the State House, the Election Laws Committee, and a "Dear Chair Whitcomb" letter signed by Dustin.
5. Invented records presented as real: "Town budget, fiscal 2026, table 4" p07, the clerk procedure and counter log p11, bills H.4212 to S.0412 [07, 09, 13], and "Merrimack Valley Civic Lab" [04].
6. "M.G.L. c. 53, § 37" [13] looks like a real citation and needs checking.

## 5. Contradictions

| # | Rule | Demonstration and evidence |
|---|---|---|
| 1 | "Small text 13 px minimum" [15] | Labels run 10 to 12 px [06], the kicker 11 px [07] and chart labels 12 px [11]. The census found 833 of 2,346 text elements under 13 px. |
| 2 | Stone small text never on Newsprint [15]; Verdigris "Not text" [05] | The census shows 49 Stone and 10 Verdigris text elements on Newsprint, including the tracker stage labels set in `#4A7C74` [13]. |
| 3 | White on red only bold at 18.66 px or more [05] | The red Subscribe buttons are 13 px [08, 13], and "Open the script" is 16 px [13]. |
| 4 | Only the two watermark opacities [03, 05] | The loading pulse runs .2 to .5, 66 icon keyline lines sit at .6 [09] and the cap seam at .3 [13]. |
| 5 | "Never: looping animation" [12]; "No autoplay" [15] | The Loading lever runs `pulse 1.2s ease-in-out infinite`, which loops, uses no motion token and shows no text. The lever reveal plays "once per page load" [12]. |
| 6 | Focus ring offset 2 px [12] | [15] and the CSS use 3 px. Report thumbnails get a Charcoal ring at 4 px. |
| 7 | "Buttons darken by one step" [12] | On hover the Charcoal button turns Prussian, which is lighter. Red buttons don't change. |
| 8 | Red does one job [05, 15] | The newsletter and article each use red for the divider ampersand and a button. The home page uses it on Subscribe, the Act nav mark and a footer dot. The one-pager uses it on a bar, a rule and a button [13]. The posters count the exempt lever as their one use [08]. |
| 9 | Nav marks all Charcoal [08] | The home desktop nav shows the Act mark's lever in red [13]. |
| 10 | Never red against green [05, 11] | Deltas pair red with Verdigris, a blue-green near hue 170. This one is my judgment. |
| 11 | The chart title states what the chart proves [11] | "Closed primaries are the largest group." sits over bars showing Closed 15 and Open 18. "Twelve years" sits over an axis from 2014 to 2024 [11, 13]. |
| 12 | Demo facts agree | [02] says 23 closed-primary states and [13] says 15. Massachusetts already "lets unenrolled voters choose a party ballot", yet H.4212 "would open the primary to unenrolled voters". The newsletter gives H.4212 and S.0876 the reverse of their tracker stages [13]. |
| 13 | Dates | p10's "Tuesday, November 4" falls on a Wednesday in 2026. "Thursday, November 6" [13] falls on a Friday. |
| 14 | The report agrees with itself | p03 counts 4 handoffs, while p08 shows routes of 5 and 3. p02 promises "the route to a hearing", but the p06 route has no hearing. The p05 hearing quote sits on a page about opening hours. |
| 15 | Mono below 80 px [03] | C1, C2, C3 and S2 carry red at 16 to 64 px [04]. L2's minimum is 72 px. |
| 16 | Red on Prussian at display size only [03] | C3 shows red on Prussian at 16 px [04]. |
| 17 | Grid mono below 32 px [07] | Kicker grids are in color at 20 to 24 px. The 16 px legend mark has a red lever [11]. |
| 18 | One favicon | S2 [04], L8 with its 48 px minimum [03] and the mono grid [07, 13] all claim the job. |
| 19 | Misuse: "The lever recolored" [07] | The Active state turns the lever Verdigris [07]. On p01 a Verdigris tracker node marks a research brief. |
| 20 | "No boxes, no cards" [15] | `.card`, `.quote-card` and every specimen frame draw 1 px boxes. |
| 21 | Email uses a system font stack [06] | The email headline is Inter Tight, and the CSS has no Helvetica or Georgia rule. |
| 22 | Captions name the place and date [10] | Every caption gives only the treatment and the subject. |
| 23 | In a hinge headline, the first noun names the rule [02] | Examples include "The hearing & the vote." and "The promise & the record." |
| 24 | File names start with the date [15 checklist] | The asset index in the same chapter uses `OA_C1.svg` and names the guide `..._V5.html`. The checklist also drops R4 and R10, and brief tension 7 says the rules run R1 to R9. |
| 25 | "Acronyms spelled out on first use" [15] | RCV, M.G.L., PDF/A and WCAG are never spelled out. |

I found no tint values in the CSS or the chapter markup. The "no tints" rule still conflicts with what hover states, chart states and duotones need.

## 6. Copy worth recovering

- V4.2 labels each sample where it sits: "SAMPLE / Fictional process and quantities." and "It represents no real jurisdiction, household, or measured outcome." This is the model for tension 6.
- V4.2 source slots, "[Publisher, budget year, table, URL]", match the brief 15 source line.
- V4.2 gives two checks before publishing: "Replace the fictional values and source slots with verified evidence before publication." and "Verify the underlying story before using any sample as public content."
- V4.2 says "Give every handoff an owner." and "link each handoff to the current official procedure."
- V4.2: "A proposed change describes an intention. A published outcome shows what happened."
- V4.2: "Each state keeps its label visible." This supports the Loading fix.
- V4.2 gives each library symbol a meaning line, such as "Several inputs meet one accountable seat."
- V4.2: "Keep decorative watermark opacity separate from the palette."
- V4.2: "These checks do not constitute a full accessibility audit."
- V5 has two rules the polish pass cut: "OATH always sits left. The arc stays dotted." and "Every icon ships with a label."
- The [16] figures say "'Positive' describes direction." and "Thickness never implies an unmeasured effect size." Both should move into the chapter text.

## 7. Sample rewrites

1. [05]. Original: "Red is punctuation. One job per composition: a button, a data point, a rule under a headline, the current step. The wordmark ampersand and the grid lever are identity and do not count." Revision: "Give Pillar Red one job in each layout, such as the main button or the data point the headline is about. The red ampersand and the red corner node of the grid belong to the logo, so leave them out of the count." Why: it turns the metaphor into an instruction.
2. [03]. Original: "Over a photograph the lockup sits in a Newsprint or Charcoal field, never directly on the image." Revision: "To place the logo over a photograph, set it on a solid Newsprint or Charcoal panel first." Why: it removes the corrective negation.
3. [03]. Original: "Clear space 1.0x on every side. Nothing enters it: no type, no rule, no edge of a photograph." Revision: "Leave an empty margin around the wordmark as wide as its capital letters are tall. Keep type, lines and photo edges out of it." Why: it explains what x means.
4. [12]. Original: "The lever lands only at stage nine. A user controls the sequence; it never plays on its own." Revision: "The reader starts each step. The lever, the larger node at the bottom right, turns red only when the bill takes effect." Why: it defines the lever and uses the active voice.
5. p05. Original: "Describe when a person can participate, what they need to submit, and where the response is recorded." Revision: "Tell readers when they can take part and what to send. Then show them where the answer will be published." Why: it breaks up the triplet and uses plainer verbs.

## Tested and not tested

**Tested:**
- Scripts over the chapter text and alt text.
- Red on the screenshots.
- The CSS rules for opacity, focus, hover, animation and fonts.
- Chart values read from the SVG geometry.
- Weekdays for the 2026 dates.
- Text inside the [16] SVG figures.
- A full read of V5 Polished, and diffs against V5 and V4.2.

**Not tested:**
- The 390 px screenshots.
- Copy in the Atlas Visual System and Concepts V2.
- Whether the bills, the statute and the named people exist.

## Change log

Created:
- `work/build/scripts/phase-0/editor_audit_scan.py`
- `work/build/scripts/phase-0/editor_red_count.py`
- this file

Modified: none.
