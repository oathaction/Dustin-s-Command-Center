# Creative director's review of Rule 12.4, the hinge patterns

Oath & Action Edition 06, Phase 2, stage C round 1, November 11, 2026. Written by the creative director (`.claude/agents/oa-creative-director.md`), run as a subagent of the main session, under `20261111_Stage-C-Round-1-Brief.md` ("the creative director on Rule 12.4's arcs") and D2-1114, which hands the question the reader check would have answered (DR-202) to the studio and to Dustin on board C. The page under review is the main session's verify build of the chapters page, identical to the committed page but for its timestamp.

I read my role file, `CLAUDE.md`, Master Brief sections 1 to 7, 11 and 12, my stage B review (the risk note on its line 233), D2-1114, DR-202, D2-894 to D2-904 and D2-989 to D2-992, Gate 1's Y6, chapter 12's file and its two generators, and chapter 04's file.

One fact first. D2-1114 speaks of two patterns, but the page carries one. The round 3 fix pass took the hinge rules (sixteen 1 px lines every 12 px) off the page on the craft team's finding that they read as lines to write on (CA-S11, D2-989). Rule 12.4 now sets the hinge arcs alone. I judged the arcs on the page and the rules from the round 2 notes and a reconstruction.

## Decision or verdict

**Retire both.** Confirm the retirement of the hinge rules, and retire the hinge arcs. Rule 12.4 keeps its number and becomes the rule for open areas: leave them plain, or sign them with the large crop of B or a watermark. I recommend no new pattern for board C. This is Dustin's call, because Gate 1 approved patterns at 12 percent ink (Y6) and Master Brief section 12 lists "restrained patterns derived from the identity".

## Scores

| Item | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Ready |
|---|---|---|---|---|---|---|---|
| Hinge arcs, as built | 3 | 4 | 2 | 3 | 3 | 3 | No |
| Hinge rules, retired (D2-989) | 3 | 2 | 2 | 2 | 4 | 3 | No |

## Reasons

**Hinge arcs**
- **Craft 3.** At 2x the arcs are clean and evenly spaced. On a 1x screen each arc's centre falls on a pixel corner, so wherever an arc runs near vertical or near horizontal, its 1 px line spreads gray over two pixels, and the set beads unevenly (enlarged eight times from a 1x capture).
- **Clarity 4.** The title, the rule and the two plates say plainly what the arcs are for and where they go. A newcomer gets it from the first screen of the rule.
- **Brand fidelity 2.** It fails the distinctiveness test. With the wordmark covered, the cover reads as any report template: concentric arcs from a corner, a ripple or a radar ping. The link to the hinge survives only as the 2 to 3 ratio of the first two circles, which no reader can see. It drops everything that makes the hinge diagram mean something: B, the four nodes, the line and the arrows. It also takes the bottom right corner that Rule 04.8 gives the large crop of B. Set side by side on the same cover with the wordmark covered, the crop reads as Oath & Action at once and the arcs read as nobody's. On the page, the hinge divider sits just above the plate, and the arcs look borrowed beside it.
- **Usefulness 3.** The token, step, coverage ceiling and 24 px clearance are exact. "The area they fill" is not defined, though. Read as the open space starting 24 px under the words, it gives 11 arcs. The plate draws 12, because its box starts 2.6 px under the paragraph. The rule offers no file and says nothing about words that reflow. In the device index, every other device does a reading job. The arcs' job is "Gives an open area texture", and the crop of B and the watermark already do it.
- **Evidence honesty 3.** The 5.5 percent coverage holds: I measured 5.3 percent inside the quarter circle at 1x and 6.0 at 2x. The rule overstates the derivation, though. It says the arcs sit "at the radii of the hinge diagram's ring and arcs". They share only the ratio. Their first two circles are 32 and 48 px, against the ring's 45 and the arc's 68 px on the 600 px display master.
- **Accessibility 3.** The arcs are marked aria-hidden and stay out of the words' layer, and the plate's alt describes them. I set a cover in the type tokens' rem sizes and moved the root to 200 percent, as a reader's text setting does. Six line boxes of the words then fall inside the outermost arc, which is the failure the rule forbids. At 100 percent the gap is 72 px.

**Hinge rules**
- **Craft 3, Clarity 2.** Even 1 px lines in a block read as a form to fill in, so a reader looks for a field. That is CA-S11's finding, and my reconstruction agrees.
- **Brand fidelity 2, Usefulness 2.** The hinge divider means something because B sits on the line. Repeating the line without B leaves a stock stripe that the Stone hairline (Rule 12.1) already covers.
- **Evidence honesty 4.** The 8.3 percent coverage was measured and labeled. **Accessibility 3.** Ruled lines next to words invite the wrong reading.

## For board C: the question, the recommendation and the cost of each choice

**Question.** Should Rule 12.4 keep the hinge arcs?

**Recommendation.** Retire them, and rewrite Rule 12.4 as below. Every shape the brand owns already has a rule that a repeat would break: B appears once in a view (Rule 04.2), the lockmark stays whole (Rule 08.3), and a row of nodes reads as chapter 11's tracker (D2-900). Any pattern that avoids them is common property. The brand already has quiet devices of its own for the same places.

- **Retire both (recommended).** The guide loses its one light texture for covers, cards and openers. A designer who wants something quieter than a large black B uses the 8 percent watermark or leaves the surface plain. It changes Gate 1's Y6 approval and the brief's list, so it needs Dustin's named call. The work is one rule and two plates in one generator. Nothing else in the guide depends on the arcs. The token table's hairline row cites Rule 12.4, and that citation updates from the chapter file.
- **Keep the arcs with the changes listed below.** That costs one round for the identity designer and a recheck. Even then, Brand fidelity stays at 2, so the rule ships below the studio's own bar, and any cover that uses the arcs looks like a template.
- **Commission a new pattern.** That costs a stage C drawing round with an uncertain result, for the reason in the recommendation.

**What Rule 12.4 then says (draft, words with the editor).** "12.4 Leave an open area plain, or sign it with the large crop of B or a watermark. We use no repeating pattern. A cover or a section opener may carry the large crop of B (Rule 04.8), and a report page or a section opener may carry a watermark in its open margin (Rule 12.2). A social card, and any view whose ampersand moment is a hinge headline, keeps its open area plain." Never: a repeating pattern of arcs, lines, dots, nodes or ampersands. Basis: design judgment, approved on board C.

**Instruction to the identity designer for board C.** Draw no new pattern. In `stage_b_identity_ch12.py`, build the rewrite above as a variant beside the current rule, with the editor on its words. The correct plate is the Report 3 cover at 360 px with the large crop of B at Rule 04.8's proportions (as `s-04-8-correct`: 142 of 400 px past the right edge, 30 of 440 past the foot), cut so no fragment stands alone. The failure plate is the same cover with the current arcs, under the failure band, with the caption "With the wordmark covered, nothing here says Oath & Action, and the arcs take the corner the crop of B would sign." Label both Illustrative. If Dustin chooses the rewrite, remove the "Hinge arcs" row from `s-12-index`, change the intro's "a pattern drawn from the hinge" to "the rule for open areas", drop "or a pattern" from Rule 12.2's Never row, and remove `hinge_arcs` and its coverage figure. Board C shows the current rule and the rewrite side by side at 360 px, at 1x and 2x.

## Required changes

If Dustin retires the arcs, the instruction above is the whole change.

If he keeps them, each of these must land before sign-off. The identity designer owns them.
1. Move the arcs' centre half a pixel in from the corner, so each arc's straight-running parts land on one pixel row or column at 1x. Check it on an eightfold enlargement.
2. Define the area: from 24 px under the last line of words to the foot. The arcs stop at the largest 16 px step under that height. State the count the plate draws.
3. Size the arcs from the words. Put them in a layer that takes only the height left under the words, and drop them when that height falls under 96 px. Add the 200 percent text case as a second failure.
4. Say "the 2 to 3 ratio of the hinge diagram's ring and arcs" where the rule now says "the radii".
5. Draw the arcs on a social card at true size and at a feed's 360 px, or take social cards out of the rule. Shrunk to 360 px, the arcs turn into a gray, moiré smudge.

## Risks for Dustin to weigh

- Retiring the arcs overrides an approved treatment (Y6) and the brief's list, which is why it needs his name on board C.
- With no pattern, covers without photographs lean on type and the crop of B. If the crop runs on every cover, covers will look alike. Chapter 24 (Reports) should set when to use the crop and when to leave a cover plain.
- No reader has seen the arcs (DR-202). "Stock" is the studio's design judgment.

## Routine calls

- D2-xxx | I judged the page as built: one pattern, the hinge arcs. I scored the hinge rules from the round 2 notes and a reconstruction | D2-989 took the rules off the page; D2-1114 still says two patterns
- D2-xxx | The comparison covers clone the built cover inside its own specimen scope and add the crop of B at `s-04-8-correct`'s proportions | That is a fair test against the device that owns the same corner
- D2-xxx | My test arcs follow my reading of "the area", starting 24 px under the words | The rule leaves the area undefined, so I report the gap and leave the choice to the maker
- D2-xxx | The 200 percent text test sets a cover in the type tokens' rem sizes with the root at 200 percent | The plate is a fixed-size artboard in px and cannot reflow
- D2-xxx | I recommend no new pattern for board C, and the rewrite instead | Each owned shape has a rule a repeat breaks (Rules 04.2 and 08.3, D2-900)
- D2-xxx | Rule 12.4 keeps its number, and chapter 12 keeps its title | Rules 12.5 to 12.9 stay put, and a reader who looks for patterns finds the answer at 12.4

## Tested

- Read Rule 12.4, chapter 12's intro, index, and Rules 12.1 to 12.3, plus Rules 04.2, 04.5 and 04.8, by script from the chapter files. Searched the page by script: the arcs' SVG appears in Rule 12.4's two plates only. It is not on the cover, the proofs or any other plate. Rule 12.4 is cited by the device index and by the token table's hairline rows.
- Captured in Chromium at 1440 and 390 px, at device scale 1 and 2: Rule 12.4 whole, both plates, the device index, Rule 12.2's correct plate, the proofs' social card and the cover's first screen. I also captured screen views of both plates with the masthead wordmark in view, at 1440 1x and 390 2x, and `s-04-5-correct` and `s-04-8-correct`.
- Looked at: the correct plate at 1x and 2x, the failure plate at 1x, the rule at 1440 1x and 390 2x, both screen views, the index, the social card, and chapter 04's two plates.
- Test compositions, built in the browser from the page's own cover, tokens and fonts, and looked at: the arcs on Newsprint, White, Charcoal and Prussian; arcs, crop of B and a plain cover with the wordmark covered and in view (1440 at 1x and 2x, 390 at 2x); Charcoal with the wordmark; the social card with the arcs on Newsprint, White and Charcoal, with and without its wordmark; the card shrunk to 500 and 360 px with PIL; the hinge rules reconstructed.
- Measured: 41.5 px from the words to the outermost arc at all four settings. The arcs' box starts 2.6 px under the paragraph. Ink is 5.3 and 6.0 percent in the quarter circle at 1x and 2x, and 2.8 and 3.1 percent across the 360 by 220 box. Stone measures 4.29, 6.05 and 3.10 to 1 on Newsprint, White and Charcoal. At 200 percent text, six line boxes fall inside the outermost arc. Each plate scrolls 0 px sideways at 390. Under forced colors the plate keeps its colors, since it is a specimen.
- Enlarged the arcs eight times from the 1x capture and four times from the 2x capture.

## Not tested

- No reader saw any of this (DR-202).
- I did not use Firefox, Safari, a real phone, 1.25x or 1.5x screens, print, 360 or 1024 px widths, or forced colors on a production page.
- The 200 percent test ran on my own cover, since no production template exists before chapter 24.
- My test covers are compositions for this review, not approved specimens. I did not measure how much of my crop's ink falls outside the frame.
- I never saw the round 2 plate of the hinge rules. My reconstruction sits closer to the words than the old rule allowed.
- I did not run the guide build or the guide check.

## Change log

Created: `work/handoffs/phase-2/20261111_CD-Review-Of-Rule-12-4.md` (this file).

Outside the repository: `cap_page.js`, `cap_ref.js`, `cap_tests.js`, `cap_checks.js`, `cap_rules.js` and 76 captures with their logs, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/cd/`. No other file was changed, and nothing was committed or pushed.
