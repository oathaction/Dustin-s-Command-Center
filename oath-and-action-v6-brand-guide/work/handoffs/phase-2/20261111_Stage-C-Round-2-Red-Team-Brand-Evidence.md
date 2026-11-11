# Stage C round 2: red team on brand, evidence and nonpartisanship

Oath & Action Edition 06, Phase 2, stage C, round 2, November 11, 2026. Reviewer: brand, evidence and nonpartisanship, in the research lead's role (`.claude/agents/oa-research-lead.md`) with the creative director's brand knowledge. Page reviewed: the frozen copy at the scratchpad's `round-2/review/guide.html` (SHA-256 starts ba1e1f97ee988b1e, as D2-1531 records), built from commit df0fb08d. `git diff df0fb08d HEAD` touches only the round 2 brief, the decision log and the open questions, so the chapter JSON, specimen and code files in `work/build/guide/` are the page's words. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: draft, checks still running. Sections fill as checks finish.

## 1. Score

Pending.

## 2. Must fix

### M1. Chapter 18, Rule 18.17, `c-18-form` in the dark theme: Pillar Red sits on Prussian in every form field with an error

- **Where:** the live stage `c-18-form--dark`, and every product form a builder copies from `c-18-form.css` (line 19) under the dark theme. The cause is in the tokens: `--oa-color-field-ground-on-charcoal` resolves to Prussian (#1F2D5A, `tokens.css` line 111), while `--oa-color-state-error-mark` on Charcoal stays Pillar Red.
- **What is wrong:** I pressed Remind me with both fields empty in the dark stage. Each field takes `aria-invalid="true"`, a Prussian ground (rgb 31, 45, 90) and a 4 px Pillar Red left border (rgb 230, 57, 70): a red bar drawn on the edge of a navy box, twice in one card, with Newsprint edges round them (screenshot in my scratch folder, `form-dark-error.png`). Rule 05.3 says "Red never sits on Prussian", and its reason says why: "where it measures 3.19 to 1 and reads as a party pair of red and blue." The palette's own description of Prussian in the token table says "Red never sits on it." Chapter 03 turns every mark White on Prussian for the same reason. D2-1469 kept the bar on contrast grounds alone (3.19 to 1 passes 3 to 1 for a graphic); it did not weigh Rule 05.3's partisan reason. The token system resolves the error mark by the page's surface (Charcoal) while the bar sits on the field's ground (Prussian), so the shared check that "fails a view with ... any red over Prussian" never sees it, and the stage shows it only after a press.
- **Fix:** keep the bar off Prussian. The smallest change that uses no new value: in the dark theme the field ground on Charcoal resolves to Charcoal, and the field is drawn by its 1 px Newsprint edge (13.29 to 1), so the 4 px red bar sits on Charcoal at 4.49 to 1, as the message under it already does. If the studio wants a raised field on Charcoal, it needs a Charcoal-derived ground that meets Rule 26.2's five conditions, never Prussian. Check the selected band on Charcoal (also Prussian) the same way before any red mark is allowed to touch it. Add a step to the guide check that presses Send in each form stage in both themes and fails any red pixel whose neighbor is Prussian.
- **Owner:** Engineer (the field ground role in `tokens.css` and `tokens.json`, the guide check); Component engineer (`c-18-form`); Accessibility lead (Rule 18.17's forced colors and dark rows if they change).

### M2. Chapter 19, Rule 19.1, `s-19-criteria`: four criteria are not printed "in W3C's words" in W3C's order, and 3.3.7 now says something else

- **Where:** `s-19-criteria` (from `stage_c_ch19_build.py`), criteria 3.3.7, 1.4.10, 1.4.12 and 1.4.13.
- **What is wrong:** I compared all 55 criteria with the W3C Recommendation of 12 December 2024, fetched today from w3.org/TR/WCAG22. Numbers, names and levels match for all 55, and 51 texts match word for word. In four, the generator prints every paragraph first and every list item after, so a sentence W3C puts after a list moves in front of it.
  - 3.3.7 Redundant Entry reads: "...is required to be entered again in the same process is either:" then "Except when:" then one list of five items: "auto-populated, or", "available for the user to select.", "re-entering the information is essential,", "the information is required to ensure the security of the content, or", "previously entered information is no longer valid." W3C has two lists: the two ways to meet it after "either:", then the three exceptions after "Except when:". As printed, a builder reads auto-population as an exception.
  - 1.4.10 Reflow prints "Except for parts of the content which require two-dimensional layout for usage or meaning." between "...scrolling in two dimensions for:" and its list of 320 and 256 CSS pixels.
  - 1.4.12 Text Spacing prints its Exception paragraph between the lead-in and the four spacing values.
  - 1.4.13 Content on Hover or Focus prints its Exception paragraph between "the following are true:" and Dismissible, Hoverable and Persistent.
  The chapter's source line says each criterion is "quoted as the Recommendation prints them".
- **Fix:** print each criterion's paragraphs and lists in the Recommendation's document order: lead-in, its list, then any paragraph after it; for 3.3.7, "either:", its two items, "Except when:", its three items. Add a check to the generator that compares each criterion's text and order with a stored copy of the Recommendation.
- **Owner:** Accessibility lead (`stage_c_ch19_build.py`); Research lead to supply the stored text.

### M3. Chapters 17 and 18, Loop R1: a loop our atlas grades plausible is titled and taught as a finding

- **Where:** `c-18-loop-stepper` (Rule 18.22) and `c-18-diagram-controls` (Rule 18.23), each headed "From our systems atlas, Loop R1 / Wealth and political influence reinforce each other", in both live stages and in the code a builder copies; chapter 17's source line for Rule 17.4's player quotes the same title.
- **What is wrong:** by script on `work/extract/atlas-v7-data.json`, Loop R1 carries `"evidence": "plausible"`. Its middle link, L02, is plausible, and V7's own evidence summary calls it "the weakest"; its qualification says "The loop runs on issues where wealthy donors' preferences differ from those of middle-income voters; on most issues the two groups agree, so its reach depends on the issue." The stepper handles the step well ("Money in politics can raise policy tilt to insiders ... Our atlas grades this step plausible, the least certain in the loop"), but the heading over it states the whole loop as fact, and the diagram's heading does the same with no grade at all. Master Brief section 15 matches the title verb to the grade: "Plausible takes 'can' or 'may.'" This is the guide's main example of a loop about money in politics, it appears three times in two chapters, and a builder who copies the component copies a heading that overstates its evidence on a subject readers on each side watch closely (DR-93: size the claim to its evidence grade).
- **Fix:** keep V7's name as the loop's name and print its grade under it, in both sets: "Loop R1, “Wealth and political influence reinforce each other”. Our atlas grades this loop plausible: its middle step is the least certain, and it runs only on issues where large donors and middle-income voters want different things." Or title the heading "Wealth and political influence can reinforce each other". Do the same in Rule 17.4's source line and both anatomy plates drawn from these sets, and in the alts.
- **Owner:** Component engineer (`c-18-loop-stepper`, `c-18-diagram-controls`); Systems designer (Rule 17.4's player and source line; the anatomy plates rerun from the sets); Editor for the words; Research lead for the grade line.

## 3. Should fix

Pending, being written up.

## 4. Questions for Dustin

Pending.

## 5. Tested

Pending.

## 6. Not tested

Pending.
