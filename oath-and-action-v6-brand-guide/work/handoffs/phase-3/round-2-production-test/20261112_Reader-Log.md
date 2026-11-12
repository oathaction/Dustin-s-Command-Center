# Production test 2: a reader new to the subject reads five round 2 pieces

Oath & Action Edition 06, Phase 3, round 2 review, November 12, 2026. **Simulated panel, untested with real people.** The UX and accessibility lead played an adult reader who follows the news, has no statistics training, and opens the guide at each piece by a link. The reader read each entry's rule, "Use it when", specimen and notes in the strict build at 1440 and 390 px. For chapter 15, they read the plates as rendered at 1024 px. Paths are relative to `oath-and-action-v6-brand-guide/`.

The five pieces:
- Distribution: entry 14.60, the box plot (S51).
- Uncertainty: entry 14.75, the band around a line (S58).
- Gauges and indicators: entry 14.90, the bullet graph (S64).
- Rule 15.12, and Rule 15.17.

## Entry 14.60, the box plot (S51)

- **What it taught.** The South's typical county has the most people under 65 without insurance, 13.9 percent, and its counties spread the widest. A few counties sit far out, the farthest in Gaines County, Texas, at 42.5 percent.
- **What confused them.**
  - The label over the title says "Estimate", and the line beside it says "Documented: the Census Bureau's Small Area Health Insurance Estimates". The reader asked which one it is. The note's "Method:" line answers it, but only three lines further down.
  - The rule's "whiskers to the last unit within one and a half times the box's length" sent the reader to the measure line, which says it more plainly ("the last county within one and a half times that span").
  - The table's last column, "Counties past a whisker", gives a count. The reader wanted to know which counties the circles are, and the table does not say.
- **The word that stopped them:** "quartile". The rule says "a box from the first to the third quartile" and never says that is the middle half. The measure line says "middle half" but not "quartile", and the table's columns say "First quartile" and "Third quartile".

## Entry 14.75, the band around a line (S58)

- **What it taught.** Median household income reached $87,460 in 2025, in 2025 dollars, the highest since 1967. The survey changed its questions in 2013, so that year has two figures.
- **What confused them.**
  - The chart note says "The gray band around the line spans each year's margin of error". At 390 px the reader could not find a band. At 1440 px they saw a faint haze along the line only once they knew to look for it.
  - The reader took the chart for an exact line and asked why the end label says "±$1,040" when nothing else on the line shows a range.
  - 37 cells under "Change in the survey" are blank. The reader read them as missing data, not as "no change that year".
- **The words that stopped them:** "Stone magnitude step 1", in the rule's own first sentence. It is a builder's name for a color and means nothing to a reader. "Margin of error" is explained in the note, at 90 percent confidence.

## Entry 14.90, the bullet graph (S64)

- **What it taught.** Federal debt subject to the limit stood $776.9 billion under the $41,104.0 billion limit on October 31, 2026.
- **What confused them.**
  - Two gray bands sit behind the bar. The reader asked why the earlier limit, $36,104.0 billion, which no longer applies, is drawn at all. The note says the July 2025 tax law raised it. The entry's "ranges behind it" did not tell the reader that a band can be a past limit.
  - The table is in millions while the title and drawing are in billions, so "40,327,074.7" and "$40,327.1 billion" took a moment to match.
- **The word that stopped them:** "magnitude steps", in the rule ("Draw the ranges as bands in the magnitude steps from zero").

## Rule 15.12, two grades for a reform (plate s-15-12-correct)

- **What it taught.** The atlas can find a problem well documented while the fix for it is untested. Reform R-32's problem, the loss of local news, is "Well supported". Its remedy, public and philanthropic funding, is a "Hypothesis".
- **What confused them.**
  - The drawing's step words "money, lowers" and "information, raises", with a minus and a plus badge, and the double ticks across each line. This plate has no key for them. The "Reading a step" key sits on Rule 15.13's plate, the next rule.
  - The thin rule labeled "Technology layer" above and "Core layer" below. The reader did not know a layer was a part of the atlas's model; it is explained in Rule 15.9.
- **The words that stopped them:** "line code", in the rule text ("the line code on each connection (Rule 13.4)").

## Rule 15.17, the authority diagram (plate s-15-17-correct)

- **What it taught.** Who decides what: Congress and the executive each reach both layers, and three of the four variables answer to two bodies.
- **What confused them.**
  - The rule speaks of four bodies: "Congress", "the executive", "antitrust enforcers" and "state and local governments". The quotations beside the drawing use the same plain names.
  - The pills on the drawing carry the atlas's variable names instead: "Congressional capacity", "Executive unilateralism", "Oversight and enforcement", "State and local experimentation". The reader asked whether "Congressional capacity" is a body or a measure.
  - The key explains the open diamond ("decides") but not the double ticks near the start of each line.
- **The word that stopped them:** "unilateralism", on a pill that the rule calls "the executive".

## What the reader would change

1. Say "the middle half" beside "quartile" in entry 14.60's rule, and add each region's farthest county to the S51 table.
2. Make S58's band visible, and say what a blank "Change in the survey" cell means.
3. Keep color names like "Stone magnitude step 1" and "magnitude steps" in the "For builders" lines, out of the rule a reader reads.
4. Give Rule 15.12's plate a short key for the step words and the ticks, or point to Rule 15.13's key.
5. On Rule 15.17's plate, name each body as the rule does ("Congress", "the executive"), with the atlas's variable name beside it, and add the ticks to the key.
