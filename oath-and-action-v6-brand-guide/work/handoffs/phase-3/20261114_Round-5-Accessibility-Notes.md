# Round 5, accessibility lead notes

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Written by the UX and accessibility lead (`oa-ux-accessibility-lead`) under `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md` (DR-272 to DR-276), contracts R5-2, R5-3, R5-4 and R5-7 above all. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/accessibility/`. Criteria numbers and wording from https://www.w3.org/WAI/WCAG22/quickref/. Round 4's "Interaction specification" (`work/handoffs/phase-3/20261113_Round-4-Accessibility-Notes.md`) holds whole for Rules 15.19 and 15.20, whose components round 5 reuses; this file says only what changes or is new.

## Status

- 01:40 UTC: started (clock read). Read the brief, round 4's notes, the engineer's R5-1 to R5-3 (SET 01:58), the component engineer's CE-1 to CE-4 (draft 01:47), the complex examples maker's and tracker designer's notes, the V10 page's chapter 14 head and rules, chapters 11 and 15's plates, the stepper script, the shell's return path and chooser line, S95's spec and the kit's crop code, and the atlas rows for Loops B4, R10 and R8 and Reforms R-06, R-30 and R-38.
- **01:56 UTC: "Interaction specification" WRITTEN** (sections 0 to 9 below) for the selection guide maker, the complex examples maker, the component engineer, the engineer, the tracker designer and the editor. It agrees with the engineer's R5-2 and the component engineer's CE-1 to CE-3 and adds to them where it says so. Requests by owner below; three go to owners' notes in one line to the main session.
- Next: tests as each item lands, at 1440, 1024, 390 and 320 px, keyboard alone and the accessibility tree, load under 4 first.
- 01:57 UTC: first handback to the main session, with the requests to relay (engineer 1 to 3, component engineer 1 and 2, data lead 1 and 2).
- 02:44 UTC: the main session asks a ruling on the design director's DD-C1 (14.143's buttons under the drawings): **yes**, with the reading and Tab order in section 2.8, under "Routine calls", and one line each to the complex examples maker and the component engineer under "Requests". Read and taken in: D3-1880 (each loop's own numbers, "Loop B4, step 2 of 3", one list, `data-oa-at` 1 to 7, by the component engineer's opt-in `data-oa-part`, C-5) and the data lead's ED5-3 ("Affirmed" stays an end word for the court case tracker). Load 5.16 at 02:43, so tests wait for it to fall under 4: the trackers first, then 14.143 and 14.144 once the component engineer's key presses pass on the current plates.

- 02:46 to 02:54 UTC: **Rules 11.10 and 11.11 tested as built** (under "Tested"): met. One low item for the review, shared with 11.8 and 11.9 (under "Requests", engineer 4). The first browser run started at load 4.79, over the brief's 4, by my error; it finished cleanly, and the follow-up runs started at 3.58 and 4.12 (the second also my error, 26 seconds long). I rerun the first under 4 before the closing handback if the load allows.
- 02:55 UTC: the component engineer reports 14.143 (02:45:17, DD-C1 landed) and 14.144 (02:44:47) passing its key presses, 68 of 68; I rebuild and test both next.
- 02:58 UTC: the container restarted mid-run (my first walk of 14.143 and 14.144, started 02:57 at load 3.67, was killed and is not counted). Files and scratch survived.
- 03:00 to 03:31 UTC: at the main session's word, on my strict build of 03:00, **tested as built:** Rules 11.10 and 11.11 again (this run started at load 1.50, so it is the counted run; the 02:46 run matched it on every figure), Rules 14.143 and 14.144 as final, and the palette specification read as text. Every browser run after the restart started under load 4. Results are under "Tested".
  - **One Must for the complex examples maker:** at 200 percent text on the 680 px composition, Rule 14.144's three cards overlap and the third runs past the stage (1.4.4).
  - **Three low items for the engineer:** the palette plate's nowrap values, its Charcoal proof grounds in print, and the image-stage descendants already sent at 02:55.
  - Everything else met.
- 04:03 to 04:19 UTC: at the main session's word, on a fresh strict build (04:03, exit 0, 0 warnings), **the selection guide tested against section 1, and Rule 14.144 retested at 200 percent text.** Every browser run started under load 4.
  - The selection guide meets section 1. Two low items: where the skip link lands now that the guide sits before the rule index, and the masthead's offset at 1,024 px.
  - Rule 14.144's fix holds: the cards go one a row as the text grows. One low note at 320 px.

## Summary

**As tested (03:31 UTC).** Rules 11.10 and 11.11 meet the specification: keyboard, names, text and marks, 200 percent text, print, forced colors and axe. Rule 14.143 meets it with DD-C1 in place: the buttons sit 148 px under the drawings at a desk, and the key paths walk clean at 1440, 1024, 390 and 320 px with and without reduced motion. Rule 14.144 meets it in every mode but one: at 200 percent text on the 680 px composition the three cards overlap, a 1.4.4 failure sent to the complex examples maker as a Must. The palette specification reads as live text: four tables with captions and headers, contrast in words, swatches hidden and kept in forced colors. Two low items go to the engineer. **Selection guide (04:19 UTC):** meets section 1 at 1440, 1024, 390 and 320 px.
- 144 Tab stops (one skip link past the guide, 16 per question, 127 forms), each with the 2 px ring and none hidden.
- Links named "Ranked bar, Core" and "Radar chart, Avoid"; every picture hidden; 16 lists named by their questions.
- Every skip link lands where it says, with scripts on and off. The way back from an entry returns to the form the reader left.
- Reading order holds at every width and at 200 percent text. Forced colors give link colors with pictures intact. Print drops only the skip links. axe-core finds 0 violations.
- Two low items: the skip link now passes the rule index too, since the guide moved before it; and a way back at 1,024 px lands 13 px under the masthead.
- Rule 14.144's Must is fixed: one card a row at 200 percent text at 1440, 1024 and 390 px.

**The specification.** The interaction specification covers every round 5 item a reader operates or hears: the selection guide (a group of 16 question lists holding 127 links, each named by its form and tier with its picture hidden; one skip link past the guide and one per question to the next, so a keyboard reader leaves the guide in one press and reaches any question in at most 32; the shell's way back from an entry to the form the reader left), complex examples 2 and 3 on the stepper and the chooser (one stepper walking seven steps through Variable C3 with the words at the hand-off and the close; three reforms with a status line that counts the red marks, none included, and a comparison with no total), S96's table and reading order, the two trackers' state words and alt pattern as chapter 11's, the palette specification as live text with contrast in words, and S95's second crop by its size. Nothing is built yet, so nothing is tested.

## Interaction specification

### 0. What holds, and who reads which part

| Section | Item | Read by |
|---|---|---|
| 1 | The selection guide, "Choose a chart" (R5-2) | selection guide maker; engineer (its checks); component engineer (the way back, 1.6); editor (the words in 1.3, 1.5, 1.6) |
| 2 | Complex example 2, Rule 14.143, two loops on Rule 18.22's stepper | complex examples maker; component engineer (keys file); editor |
| 3 | Complex example 3, Rule 14.144, three reforms on Rule 15.20's chooser | as section 2; data lead (3.2) |
| 4 | Complex example 1, Rule 14.142, S96 in full: its table and reading order | complex examples maker; engineer (the kit) |
| 5 | The two trackers, Rules 11.10 and 11.11 | tracker designer; editor; research lead (the step names and end words) |
| 6 | The palette specification (R5-3) | engineer (its generator); design director (its layout) |
| 7 | S95's second crop | engineer (request 1) |
| 8 | What every round 5 plate keeps | every owner |
| 9 | What I test once each item lands | the main session |

Round 4's rules stand everywhere below: an interactive plate is a group, never an image; its drawing is a picture beside the controls with no Tab stop; focus never moves on its own; reading order is visual order (1.3.2, 2.4.3); no heading inside a plate; every ID a typed chip; controls 44 px tall and 4 px inside the stage edge; `forced-color-adjust: auto` with its own ground on live words and controls, `none` with its own ground on a drawing; failure plates are still pictures.

### 1. The selection guide, "Choose a chart" (R5-2)

**1.1 Where it sits and how a reader reaches it.** The plate is the extra `s-14-selection-guide`, the first thing in chapter 14's body, before group 1 (the engineer's R5-2a). A reader meets it after the chapter head, whose opener already links the 16 questions to their groups and whose rule index holds a link to every rule. The local contents' line "Choose a chart" links to `#fig-s-14-selection-guide`; the shell then puts focus on the figure (it holds no heading), so the next Tab reaches the guide's first stop, the skip link. Ctrl+F finds any form by name, since every name is live text.

**1.2 What a screen reader meets.** No heading and no landmark anywhere in the plate (the guide check's `structure` and `specimenLandmarks` tests; the chapter's own groups are `p.rg-head`, not headings, so the guide matches the chapter). Its structure is lists, which every screen reader moves through by list and item:

```
figure#fig-s-14-selection-guide            (the shell's: label "Choose a chart", caption)
  div.plate-stage role="group"             named "Choose a chart, interactive specimen", described by the alt
    svg.sg-defs aria-hidden                 the symbol set, 0 by 0
    div.sg (the fragment's root)
      a  "Skip the chart guide"             (1.5)
      ol role="list"                        16 items, one a question, in the chapter's group order
        li data-group="2"
          p#s-14-sg-q-2                     the group's title as 14-chapter.json prints it
          a  "Skip these 10 forms"          (1.5)
          ul role="list" aria-labelledby="s-14-sg-q-2"
            li#s-14-sg-f-15 data-return-label="…"
              a href="#rule-14-15"          picture (hidden) + name + tier
            …
```

- The outer list is an `ol` (a reader hears "1 of 16", "2 of 16"); each question's forms a `ul` named by its question line, so a screen reader that announces a list's name says the question on entering it.
- The alt is short, since every word is live (R4-3, item 5): what the plate holds in one or two sentences, for example "Every chart form in this chapter, under the sixteen questions a reader brings, each a small picture with its name and tier and a link to its rule. Forms to avoid are marked." The engineer's meta file sets `"interactive": true`; keep it (the stage then reads as a group and every link stays in the tree).

**1.3 Each link's name.** One `a` per form, `href="#rule-14-NN"`, holding three things in this order: the picture, the form's name, its tier in words.

```
<a href="#rule-14-15" data-tier="core" data-rule="14.15" data-oa-xref>
  <svg class="oac-svg sg-pic" … aria-hidden="true" focusable="false"><use href="#s-14-sg-15"/></svg>
  <span class="sg-n">Ranked bar</span><span class="vh">, </span><span class="sg-t">Core</span>
</a>
```

- **Name:** "Ranked bar, Core". The visually hidden comma makes the pause a screen reader needs; without it the name runs "Ranked bar Core". The name starts with the visible words in the order seen (2.5.3, Label in Name), so a voice user says "click Ranked bar".
- **Tier words** as the plan prints them: Core, Extended, Reference, Avoid, and "Extended, interactive" for the one form that has it. The tier is in words on the face, never only by weight, color, a dot or position (1.4.1). One line at the guide's head says what the tiers mean (the editor's words), so "Core" is explained at first use.
- **An avoid form** reads as one in words and in its mark (R5-2): its tier word is "Avoid", so its name is "Radar chart, Avoid", and its picture carries the mark ruling (a) sets (a cross or a strike, never red alone). The link still goes to its entry, which says why. If ruling (a) prints more words on the face ("Do not publish"), they join the name after the tier.
- **A rule number** joins the name only if the face prints it ("Ranked bar, Core, Rule 14.15"). No hidden words beyond the comma.
- No `title` attribute on a link or a picture (no tooltip a hover alone shows, 1.4.13). No `aria-label` on the link: the name comes from its words, so what a reader sees and hears match.
- The 127 names are unique (checked by script on the plan's rows at 01:49: no two forms share a name), so a links list (Insert+F7 in NVDA, the rotor in VoiceOver) tells every form apart.

**1.4 The pictures.** Each picture is an `svg` with `aria-hidden="true" focusable="false"`, no `title`, no `desc`, no words (the engineer's R5-2, item 3). The sprite `svg.sg-defs` is hidden the same way. Strokes and fills that make the form's shape stand at 3 to 1 or more against the tile's ground (Stone is 4.29 to 1 on Newsprint), so a reader with low vision can still use the picture to find a form, though the name carries it. A picture never holds the only sign of a tier.

**1.5 The way past the guide, and from question to question.** Every link stays a link in the Tab order (Rule 18's link: "Tab reaches it; Enter follows it"), and two kinds of skip link cut the walk.

- **Past the whole guide:** the fragment's first stop, "Skip the chart guide", `href="#group-14-1"`. The shell puts focus on group 1's block (no heading inside it, AX-S11), so the next Tab continues in group 1.
- **To the next question:** in each question's block, after its question line and before its list, "Skip these N forms" (N in figures, the count of that question's forms), `href="#s-14-sg-q-(next group)"`; in the last question, `href="#group-14-1"`. Following it puts focus on the next question's line, which a screen reader reads ("Proportion and overlap: how much, and how do groups overlap?"); the next Tab reaches that question's own skip link, so Tab then Enter moves question by question.
- **Look:** Rule 18's skip link (the code set's `oa-link-skip`, global CSS): hidden until it takes focus, then shown with its edge and the 2 px ring. Set `position: relative` on the fragment's root and on each question's `li`, and offset the link 4 px inside, so it shows at the top left of the block it skips and its ring falls on the stage's ground, never clipped. It shifts nothing when it shows.
- **The count:** 1 + 16 + 127 = 144 Tab stops through the whole guide. A keyboard reader leaves the guide in one press of Tab and Enter from its top, and reaches the 16th question in 16 pairs at most, against 121 Tabs without them. Every skip link works with scripts off: following a same-page link moves the browser's focus start point to its target, so the next Tab goes on from there.
- **No question line is a link.** The opener above already links each question to its group, and 16 more links would add stops with nowhere new to go.
- **Ids** start `s-14-sg-` (the engineer's rule): `s-14-sg-q-N` for a question line, N the group's number (2 to 17); `s-14-sg-f-NN` for a form's item, NN the rule's number after the point.

**1.6 The way back from an entry.** The shell already writes "Return to …" after the heading a cross-reference lands on and puts focus on that heading, so the next Tab reaches the way back (AX-S1). It does this only for `a.xref` links and only remembers a rule, closer, group or route step as the place to return to; a link in the guide would return to the top of chapter 14. Request 1 to the component engineer makes the guide's links return to the form the reader left:
- each form link carries `data-oa-xref` (an attribute, so the shell's `.xref` look does not reach the guide);
- each form's `li` carries its id and `data-return-label`, for example `data-return-label="Ranked bar in Choose a chart"` (the editor's words), so the way back reads "Return to Ranked bar in Choose a chart, 14 Data visualization";
- following it puts focus on that item, so the next Tab is the same form's link and the one after it the next form.

**1.7 Focus, targets and hover.** Each link is a tile, picture and words together, at least 44 px tall and wide (2.5.8 asks 24), with at least 4 px between tiles so two targets never touch. Focus shows the guide's 2 px Verdigris ring at its 2 px gap around the whole tile (2.4.7), never clipped by the stage (no `overflow: hidden` on any box that holds a tile) and never under the sticky masthead (the shell's `scroll-margin-top` on everything in `main` covers a question line or a form item that takes focus, 2.4.11). Hover underlines the name and may darken the picture's edge; hover and focus add nothing a reader must read (1.4.13). Nothing moves on hover beyond the 120 ms token, which tokens.css sets to 0 under reduced motion.

**1.8 Reading order at every width, and the phone's order.** The DOM order is: the skip link, then question by question in the chapter's group order, each its line, its skip link and its forms in ruling (a)'s order (core, then extended, then reference, then avoid). Grid or columns lay it out with no `order`, no `row-reverse` or `column-reverse`, no `grid-auto-flow: dense` and no words placed by `position: absolute` (the skip links aside), so Tab, a screen reader and the eye meet the same order.
- **1440 and 1024 px:** questions may stand in two or three columns. Either rows left to right then down, or newspaper columns down then across; both match the DOM if the CSS keeps its order. Within a question, tiles run left to right, then down.
- **390 px:** one column of questions, each question's line full width above its tiles; tiles two or three a row, left to right, then down.
- **320 px:** the stage flows (no `width_px`, `fit_switch: false`), so the frame never scrolls; tiles two a row, or one where a name would break mid-word. Every word and tile sits inside the visible frame.
- Tiles size their columns in rem, for example `grid-template-columns: repeat(auto-fill, minmax(min(100%, 9rem), 1fr))`, so larger text takes fewer columns instead of clipping.

**1.9 Text at 200 percent and reflow (1.4.4, 1.4.10, Rule 19.6).** With `html { font-size: 200% }` at 1440, 390 and 320 px: no sideways scroll, no clipped or overlapping word; names wrap (no `white-space: nowrap` on a name, a tier or a question line); no box of words has a fixed height; a picture may keep its pixel size. The skip links, when shown, may cover the line they sit on; they never cover a link.

**1.10 Forced colors.** The shell keeps a specimen's colors (`.plate-stage { forced-color-adjust: none }`, AX-S6); a set of 127 live links should follow the reader's colors instead. The fragment's root takes `forced-color-adjust: auto` and paints its own background (round 4's measure: `auto` with no background of its own turns the words white over the stage's kept Newsprint). Then names and tiers take the system's link and text colors, the ring the system's highlight, and the pictures the colors kit.css maps their classes to (the engineer measured this through `<use>` at 01:50). The hatch stays a hatch and the avoid mark stays a shape, so both survive one ink.

**1.11 Print.** The guide prints whole: every question, every picture (SVG fills print; no picture is a CSS background, which a browser drops in print) and every name and tier. The skip links do not print. Links print as their words, with no web address added. A tile never breaks across a page (`break-inside: avoid`); a question's line stays with its first row of tiles (`break-after: avoid`).

**1.12 Scripts off and reduced motion.** The guide needs no script: links, skip links and pictures all work without one. Only the shell's "Return to" line needs the shell's script, as it does everywhere. Nothing in the plate moves, so it carries no `data-oa-motion`.

**1.13 Checks.** The engineer's R5-2 item 7 covers links, names, tiers, symbols and hidden pictures. Please add (request 2 to the engineer): each question's list is named by its question line; each skip link's target exists on the page and is the next question's line or `#group-14-1`; the first skip link is the guide's first focusable element; no question line is a link.

### 2. Complex example 2, Rule 14.143: Loops B4 and R10 on Rule 18.22's stepper

Round 4's section 2 (Rule 15.19) holds whole, with the component engineer's CE-1. What changes for two loops that share Variable C3:

**2.1 One stepper walks both loops.** One `[data-oa-stepper]` root, one status line, one step list, one set of four buttons, one source of state for the one drawing. Two steppers on one drawing would give it two states that could disagree. The script counts every `.oa-stepper-step` in the root in document order, so the walk runs "Step 1 of 7" to "Step 7 of 7" across both loops. Keep one `ol` (a second list adds a list boundary a screen reader announces mid-walk and nothing else); the CSS counter runs 1 to 7 without a reset, and the drawing's numbers match the list's.

**2.2 The walk.** From today's model (D3-1870): Loop B4 is L23, L24 and L54 through Variables D5, C3 and C5; Loop R10 is L08, L25, L53 and L42 through C1, C2, C3 and C4; both pass through C3, "Risk of losing office". Ruling (d) sets the order. The words below assume it starts at C3, walks B4 back to C3, then R10 back to C3 (seven steps); they change with the ruling.

**2.3 The group's name** is "Steps of Loops B4 and R10". The buttons keep Rule 18.22's words ("Play", "Reset the loop", "Previous step", "Next step"): the script's reason line names "Reset the loop", and a button whose word differed from the line that explains it would confuse.

**2.4 The status lines' words.** The systems pattern of 15.19, plus three things: every step names its loop, the step that closes a loop says so and names its kind, and the walk names C3 as the shared variable at the start, at the hand-off and at the end. Below, the pattern with the model's own words as an example; the editor writes the final words, and the component engineer re-times each hold from them (CE-1's formula, 250 ms a word, never under 6,000 ms).

| When | Status line (example) | Focus |
|---|---|---|
| Page opens, not announced | "Ready. Start at the risk of losing office, which both loops pass through, and suppose it rises. Press Play, or Next step to follow one connection at a time." | where the reader left it |
| Step 1 | "Step 1 of 7: In Loop B4, the risk of losing office raises the number of incumbents defeated or pushed into retirement." then its more: the typed chip "Connection L24", its atlas name in quotation marks, "the atlas grades it well supported, and its effect takes 2 to 10 years" | on the button pressed |
| Step 3, B4 closes | "Step 3 of 7: In Loop B4, the quality of public services lowers the risk of losing office." then its more, ending "Loop B4 is back where it began, at the risk of losing office, and with one minus sign it is balancing. Loop R10 starts here too." | on the button pressed |
| Step 4, R10 begins | "Step 4 of 7: In Loop R10, the risk of losing office can lower officeholders’ control over election rules." then its more, with "the atlas grades it plausible" ("can" for a plausible step, as 15.19's step 2 says it) | on the button pressed |
| Step 7, R10 closes | "Step 7 of 7: In Loop R10, how often the primary decides the winner lowers the risk of losing office." then its more, ending "Loop R10 is back where it began, at the risk of losing office, and with two minus signs it is reinforcing. Both loops pass through the risk of losing office, and the atlas does not say which is stronger." | on the button pressed |
| End of playback | as step 7; Next step turns unavailable; Play's word reads "Play again" | on Play |
| Reset the loop | the ready line again | stays on Reset the loop, now unavailable |

- The last sentence at step 7 keeps Rule 15.21: no word or mark says one loop wins, outweighs or cancels the other, since the model holds no loop strengths.
- Each step's words carry every fact the drawing shows for it: the typed connection, which way it moves its variable ("raises" or "lowers" from its sign; "can" for a plausible step), the grade in Rule 13.3's word, the delay where the drawing draws it, and each variable by its atlas title (DR-265). A sign is said as a word, never only as "+" or a minus glyph.

**2.5 The drawing.** One drawing of both loops, `aria-hidden`, after the loops' names and grade lines and before the status line, inside the stepper's root (CE-1). It follows `data-oa-at` as 15.19's does: the current connection and its two variables heavier with the step's words bold, the steps behind in ink, the steps ahead muted at 3 to 1 or more, each line keeping its grade's dash. C3 is drawn once and marked as shared by a shape a reader sees in gray (a double outline or a second ring, ruling (d) or the maker) and by the words "Shared by both loops" beside it in the drawing and in the plate's words above it. No red (the working red belongs to a reform's targets, Rule 15.11). Two grade lines, one per loop, sit above the drawing as text.

**2.6 The still sequence, for print, reduced motion and scripts off.** As 15.19's: every step numbered 1 to 7 in full ink, none current; the buttons, the status line and the reason line hidden (scripts off by `:not([data-oa-live])`, print by `@media print`); the drawing with every step in ink. Under reduced motion nothing moves and Play keeps its pace. Because chapter 15's plate CSS is scoped to chapter 15 (`@scope (#systems-graphics [data-specimen])`, read in the V10 page), none of it reaches a chapter 14 plate; the plate's own CSS must carry each of these, as the complex examples maker plans (its "My own" contract):
- `.lv { forced-color-adjust: auto; background: var(--oa-color-surface) }` on the live root and `forced-color-adjust: none` with its own ground on the drawing's wrapper;
- `[data-oa-stepper]:not([data-oa-live]) :is(.oa-stepper-controls, .oa-stepper-status, .oa-stepper-why) { display: none }`;
- the step counter on `.oa-stepper-step::before`, never in `.oa-stepper-line`;
- the `@media print` still sequence;
- `@container oa-frame (max-width: 327.98px) { .p :is(p, ul, ol, .evr, .oa-stepper-controls, fieldset, .oa-choice-item, details) { max-width: calc(100cqi - 32px) } }`, so every word and control sits inside the visible frame at 320 px and only the 296 px drawing reaches past it. The manifest carries `frame_container: true` (the maker's request to the engineer).

**2.7 Key path** for the component engineer's keys file (CE-3), `s-14-143-correct.keys.json`, written for seven steps; the counts and the step where Loop R10 begins follow ruling (d).

```json
{
 "format": "oa-keys/1",
 "set": "s-14-143-correct",
 "rule": "14.143",
 "component": "Loop stepper walking two loops through a shared variable",
 "paths": [
  {
   "name": "Step through both loops by hand; the line names each step and the hand-off, the drawing follows, focus stays",
   "steps": [
    { "key": "Tab", "focus": ".oa-stepper-play" },
    { "key": "Tab", "focus": ".oa-stepper-reset", "states": [ { "el": ".oa-stepper-reset", "attr": "aria-disabled", "is": "true" } ] },
    { "key": "Tab", "focus": ".oa-stepper-prev", "states": [ { "el": ".oa-stepper-prev", "attr": "aria-disabled", "is": "true" } ] },
    { "key": "Tab", "focus": ".oa-stepper-next" },
    { "key": "Enter", "focus": ".oa-stepper-next", "states": [ { "el": ".oa-stepper-step:nth-child(1)", "attr": "aria-current", "is": "step" }, { "el": "[data-oa-stepper]", "attr": "data-oa-at", "is": "1" } ], "status_has": "Step 1 of 7:", "status_el": ".oa-stepper-status" },
    { "key": "Enter", "focus": ".oa-stepper-next", "status_has": "Step 2 of 7:", "status_el": ".oa-stepper-status" },
    { "key": "Enter", "focus": ".oa-stepper-next", "status_has": "Step 3 of 7:", "status_el": ".oa-stepper-status" },
    { "key": "Enter", "focus": ".oa-stepper-next", "states": [ { "el": "[data-oa-stepper]", "attr": "data-oa-at", "is": "4" } ], "status_has": "Step 4 of 7:", "status_el": ".oa-stepper-status" },
    { "key": "Enter", "focus": ".oa-stepper-next", "status_has": "Step 5 of 7:", "status_el": ".oa-stepper-status" },
    { "key": "Enter", "focus": ".oa-stepper-next", "status_has": "Step 6 of 7:", "status_el": ".oa-stepper-status" },
    { "key": "Enter", "focus": ".oa-stepper-next", "states": [ { "el": ".oa-stepper-next", "attr": "aria-disabled", "is": "true" }, { "el": "[data-oa-stepper]", "attr": "data-oa-at", "is": "7" } ], "status_has": "Step 7 of 7:", "status_el": ".oa-stepper-status" },
    { "key": "Shift+Tab", "focus": ".oa-stepper-prev" },
    { "key": "Enter", "focus": ".oa-stepper-prev", "states": [ { "el": ".oa-stepper-next", "attr": "aria-disabled", "is": null } ], "status_has": "Step 6 of 7:", "status_el": ".oa-stepper-status" },
    { "key": "Shift+Tab", "focus": ".oa-stepper-reset" },
    { "key": "Enter", "focus": ".oa-stepper-reset", "states": [ { "el": ".oa-stepper-reset", "attr": "aria-disabled", "is": "true" }, { "el": "[data-oa-stepper]", "attr": "data-oa-at", "is": "0" } ], "status_has": "Ready.", "status_el": ".oa-stepper-status" },
    { "key": "Tab", "focus": ".oa-stepper-prev" },
    { "key": "Tab", "focus": ".oa-stepper-next" },
    { "key": "Tab", "focus": "outside" }
   ]
  },
  {
   "name": "Play becomes Pause and back, with focus on it, under reduced motion too",
   "setup": { "reducedMotion": true },
   "steps": [
    { "key": "Tab", "focus": ".oa-stepper-play", "states": [ { "el": ".oa-stepper-word", "text": "Play" } ] },
    { "key": "Enter", "focus": ".oa-stepper-play", "states": [ { "el": ".oa-stepper-word", "text": "Pause" } ], "status_has": "Step 1 of 7:", "status_el": ".oa-stepper-status" },
    { "key": "Enter", "focus": ".oa-stepper-play", "states": [ { "el": ".oa-stepper-word", "text": "Play" } ] }
   ]
  }
 ]
}
```

If the plate holds a link or a disclosure after the stepper (a qualification in a `details`, say), its stop comes before "outside"; write it into the path as built.

**2.8 After D3-1880 and DD-C1 (02:44 UTC).** Two changes to sections 2.1 to 2.7. The plate of 02:20 already meets the count; the order waits on the complex examples maker:
- **The count.** The status line says each loop's own count, "Loop B4, step 1 of 3:" to "Loop R10, step 4 of 4:", through the stepper script's opt-in `data-oa-part` (the component engineer's C-5). The list's numbers restart at Loop R10's first step, so the line, the list and each drawing say one number; `data-oa-at` still runs 0 to 7 for the drawing. Section 2.4's words then need not open with "In Loop B4,": the head names the loop. The key path's `status_has` checks these heads (the component engineer's keys file already does).
- **The order (DD-C1, yes).** The DOM, the eye and a screen reader meet the plate in this order at every width: each loop's name and grade line with its drawing (`aria-hidden`), Loop B4's then Loop R10's; the note on Variable C3; the status line; the controls group (Play, Reset the loop, Previous step, Next step); the reason line straight after it (the unavailable buttons' description); the seven steps as the still list; the atlas's limits; the source. The move is in the markup, never by CSS `order`, grid placement or `position`, so reading order stays visual order (1.3.2). Tab order is unchanged: from before the stage, Play, Reset the loop, Previous step, Next step, then out of the plate, four stops, since the list, the limits and the source hold no control. At 320 px the frame's own stop comes first, as in 15.19. Focus stays on the button pressed. With the buttons under the drawings, the drawing that lights and the button that lights it share one window, and the status line above the buttons says each step, so the list need not be in view while a reader steps; the current step keeps `aria-current="step"` and its bar in the list. Print, reduced motion and scripts off keep section 2.6's still sequence: the buttons, status line and reason line hidden, the list whole and numbered.

### 3. Complex example 3, Rule 14.144: Reforms R-06, R-30 and R-38 on Rule 15.20's chooser

Round 4's section 3 (Rule 15.20) holds whole, with CE-2. What changes for three reforms on one loop, compared:

**3.1 The choice.** One `fieldset` with a visible legend ("Show one reform on Loop R8"), three native radios in ruling (d)'s order, the first checked on load, `name="s-14-144-reform"`. Each radio's name: "Reform R-06 “Hold local elections alongside November races”" (the typed chip and the atlas's title). Three is inside Rule 18.3's two to five. Tab enters at the checked reform; the arrow keys move and check, wrapping from the third to the first.

**3.2 The status lines' words, and a reform with nothing to light.** On each change, and only then, one sentence from the chosen panel's `[data-oa-say]` line (CE-2): which marks turn red, counted in words (Rule 15.11). Today's model (read at 01:52) puts two of the three reforms' targets partly or wholly off Loop R8's two steps (L38 and L39 through A5 and A6):
- R-06 targets B5 and L39: one mark on the loop.
- R-30 targets L39, A5 and LE17: two marks on the loop.
- R-38 targets LT12 and TC7: none on the loop.

So the line always gives the count on this drawing, none included, and names in the panel what sits elsewhere. Examples (the editor's words decide):
- "Reform R-06 acts where the marks turn red: on one connection. It also acts on one variable outside this loop."
- "Reform R-30 acts where the marks turn red: on one connection and one variable. It also acts on one connection outside this loop."
- "Reform R-38 acts on Loop R8 through two parts outside this drawing, so no mark turns red."

A chosen reform that lights nothing and says nothing would read to a sighted reader as a fault and to a screen reader as silence. If ruling (d) draws the outside targets attached to the loop instead, each is named on the drawing and in the panel's typed chips, and the line counts it.

**3.3 The comparison, with no total.** The chooser shows one reform's targets on the drawing; the comparison sets all three side by side in live text, so a reader compares without holding one panel in memory. It is either a `table` or three cards (R4-3), and in both:
- **As a table:** a `caption` that names it and the model's date ("The three reforms that act on Loop R8, side by side, as of October 15, 2026"); one column per reform, its header `th scope="col"` holding the typed chip and the title; one row per measure, its header `th scope="row"`: targets on this loop, targets elsewhere, band, the four outcome families' effects (one row each), grade, routes. No total row or column, no average, no rank, no sort control, no shading that grows with the effects (Rule 15.21, R5-4).
- **As cards:** a `ul role="list"`, one `li` per reform, each a `dl` of the same terms in the same order.
- **Each effect cell** holds the atlas's code with its qualifier whole and its words: "+L local", then the words ruling (d) gives (for example "large positive, in local elections"). The qualifier never moves to a footnote or a mark alone. A zero says so in words ("0, no change expected"); no cell is empty, since a screen reader says "blank". Pips are `aria-hidden`.
- **Routes:** each route's name and instrument in words, its feasibility in the atlas's word, and its check date, or "Not checked" where the model holds none (Rule 13.10). Today only R-38's SS route carries a date (D3-1870).
- **At 680 px** the table shows whole. **In the 328 px column** it scrolls sideways in its own frame, which takes a Tab stop and a name ("The three reforms side by side, table; scroll sideways to see all of it"), with the row headers held at the left (`position: sticky`); a table of two dimensions may scroll under 1.4.10. Or it reads as the three cards, one under another. Either keeps every word as live text; no label in CSS `content` (R4-3, item 6).

**3.4 Print and the still sequence.** The `fieldset` hidden; the comparison whole; every panel in the radios' order with its qualifications open (the shell opens every `details` at `beforeprint`, C-3). For the drawing, three print-only copies, one per reform, each titled with its reform and its targets heavier and outlined (red prints as gray, so weight carries it), is the better page; DR-271 allows the bytes. At the least, the print-only line names the reform the drawing shows ("The drawing shows Reform R-30 in red."), as 15.20 does. Scripts off: the radios still choose through CSS; the status line stays silent. Reduced motion: nothing moves.

**3.5 Key path** for `s-14-144-correct.keys.json`, written for R-06, R-30, R-38 in that order with R-06 checked; the order follows ruling (d).

```json
{
 "format": "oa-keys/1",
 "set": "s-14-144-correct",
 "rule": "14.144",
 "component": "Reform chooser with three reforms on one loop",
 "paths": [
  {
   "name": "Enter at the checked reform; the arrow keys choose all three and wrap; the panel and the line follow; focus stays",
   "steps": [
    { "key": "Tab", "focus": ".oa-choice-input[value=\"R-06\"]", "states": [ { "el": ".oa-choice-input[value=\"R-06\"]", "prop": "checked", "is": true }, { "el": "[data-oa-panel=\"R-06\"]", "visible": true }, { "el": "[data-oa-panel=\"R-30\"]", "visible": false }, { "el": "[data-oa-panel=\"R-38\"]", "visible": false } ] },
    { "key": "ArrowDown", "focus": ".oa-choice-input[value=\"R-30\"]", "states": [ { "el": "[data-oa-panel=\"R-30\"]", "visible": true }, { "el": "[data-oa-panel=\"R-06\"]", "visible": false } ], "status_has": "Reform R-30" },
    { "key": "ArrowDown", "focus": ".oa-choice-input[value=\"R-38\"]", "states": [ { "el": "[data-oa-panel=\"R-38\"]", "visible": true } ], "status_has": "Reform R-38" },
    { "key": "ArrowDown", "focus": ".oa-choice-input[value=\"R-06\"]", "states": [ { "el": "[data-oa-panel=\"R-06\"]", "visible": true } ], "status_has": "Reform R-06" },
    { "key": "ArrowUp", "focus": ".oa-choice-input[value=\"R-38\"]", "status_has": "Reform R-38" },
    { "key": "Tab", "focus": "[data-oa-panel=\"R-38\"] summary", "states": [ { "el": "[data-oa-panel=\"R-38\"] details", "prop": "open", "is": false } ] },
    { "key": "Enter", "focus": "[data-oa-panel=\"R-38\"] summary", "states": [ { "el": "[data-oa-panel=\"R-38\"] details", "prop": "open", "is": true } ] },
    { "key": "Shift+Tab", "focus": ".oa-choice-input[value=\"R-38\"]" },
    { "key": "ArrowUp", "focus": ".oa-choice-input[value=\"R-30\"]", "states": [ { "el": "[data-oa-panel=\"R-38\"] details", "prop": "open", "is": true } ], "status_has": "Reform R-30" },
    { "key": "Tab", "focus": "[data-oa-panel=\"R-30\"] summary" }
   ]
  }
 ]
}
```

After the summary, the path ends with the plate's other stops as built (the comparison's frame where it scrolls, any link) and then `"outside"`.

### 4. Complex example 1, Rule 14.142: S96, S14 in full

S96 is a kit figure (the engineer's R5-1), so the kit's figure order and C7 hold; this section fixes what "in full" adds.

**4.1 Reading order,** which is also the DOM order at every width: the evidence word and grade line; the title, which names the finding, the two drops past the margin by month; the measure line; the reading guide (columns are each month's change, the line is the three-month average, the band is the margin of error, how a preliminary month is drawn); the drawing; the notes; the source line (the `with_margin` variant); the table in its disclosure. Then the failure plate, if the rule has one, as a picture whose caption leads with "Fails Rule 14.142." and whose alt names what misleads.

**4.2 The drawing's name** is short (one or two sentences: the span of months, the two drops past the margin with their months and values, the average's path), since the table holds every month. The two named drops carry their month and value as labels in the drawing, beside the point red (1.4.1); a preliminary month differs by a pattern or an outline as well as a lighter fill, and the reading guide says which.

**4.3 The table.**
- **Caption:** what it holds and its span, for example "Monthly change in jobs, January 2022 to September 2026".
- **Columns,** each header `th scope="col"` with its unit in words: Month (the row header, `th scope="row"`); change from the month before, in thousands of jobs; three-month average, in thousands; status in words ("Preliminary" or "Final", as the data lead's ruling (c) names them); and whether the change passes the margin, in words for every row (for example "Drop past the margin" on the two months the title names, "Within the margin" on the rest). A row is never marked by bold, color or a symbol alone.
- **Rows** in date order, oldest first, as the drawing reads left to right, never by a text sort of month names (the kit sorted row 11 before row 10 in S93's table). A month with no average says so in words ("Needs three months"); no cell is empty.
- **Numbers:** a loss carries the same minus sign the guide's tables use (U+2212, which screen readers say as "minus"); a number keeps its unit in the header, not in each cell, so a screen reader hears "minus 92" under "Change from the month before, in thousands of jobs".
- **The margin** in the notes and in the column header with its size and its confidence level, as the source states them (the research lead's line), so "past the margin" means one thing everywhere.
- **Phone:** the kit's table, as every chart's (C7); I test it at 390 and 320 px.

**4.4 Two figures from one data file.** S14 stays at its entry and S96 sits at Rule 14.142: their ids (`oac-s-14-s96-*` and S14's) stay unique, and their tables' captions differ, so a reader who lists tables tells them apart.

### 5. The two trackers, Rules 11.10 (ballot measures) and 11.11 (court cases)

Group 2's trackers read one way, so a reader who knows the records request and agency rule trackers (now Rules 11.8 and 11.9) knows these. Each plate is a picture named by an alt that carries every word on it (the manifest leaves `readable` off, so the stage is `role="img"`), as 11.8 and 11.9 are; the marks inside are `aria-hidden`.

**5.1 The words each state says.** Every mark has one word in the key and the same word in the alt for each step. The shape carries the state, so it holds in gray, in print and in one ink.

| State | Mark (DR-108, DR-150, as chapter 11 draws it) | Key word | Alt word for a step |
|---|---|---|---|
| Done | filled circle, its number knocked out | Done | done |
| Now | ring 3 px, its number in ink | Now | now |
| A reader can act now | the take-part mark chapter 11 uses (11.9) | You can take part now | you can take part now |
| Not yet | thin ring 1.5 px in the muted ink, 3 to 1 or more | Not yet | not yet |
| Never happened | thin ring with DR-150's slash, its number kept | Never happened | never happened |
| Stopped | filled square, where the line ends | Stopped | stopped |

- The key lists only the marks the plate uses, as 11.8's failure plate does.
- The steps after a square read "not yet", as 11.8 and 11.9 print them (Request 99005, Rule 99006).
- **Ballot measures:** "You can take part now" only where the research lead's source names a step a reader can act in (signing a petition, voting), with the take-part line in words that say who may ("if you are a registered voter in the state", the editor's words) and by when.
- **Court cases:** the public has no step to act in, so the plate shows "Now", never the take-part mark, unless the research lead's source names one.

**5.2 Each item's status line** (`p.sx-st`), its first sentence bold, as 11.8's:
- **In progress:** "Step k of 6: [the step's name]." then one sentence of what is happening, with the date the law sets where it sets one.
- **Ended:** the end in words with its date, then one sentence. A decided or certified item says so ("Decided on May 4.", "Approved by voters on November 3."), and a stopped one names who stopped it ("Withdrawn by its sponsors on April 9.", "Dismissed on …"). The words are the research lead's and the editor's, from the law (R5-7).

**5.3 The alt,** in 11.8's pattern, so the six trackers sound alike: "Three Illustrative ballot measures at 360 px on Newsprint, each drawn as six numbered steps with the bill tracker’s marks, and a key of the six steps, [the six names], and of the marks. [Item ID], [its title]: [its status line, every sentence]. Steps: 1 [name] [state]; 2 [name] [state]; … 6 [name] [state]. [Where it applies: You can take part now: the action and its date.]", then the next item. "Illustrative" stays in the alt, since the label drawn on the plate sits inside the picture and is not read. A failure plate's alt starts "Failure case: do not publish." and says what the plate gets wrong, as 11.8's does; its caption leads with "Fails Rule 11.10." (the guide check's `failureLead`).

**5.4 What stays as chapter 11 has it:** the 360 px stage, its 13 px floor (the step numbers inside the marks included), the muted ring at 3 to 1 or more, the shapes apart in grayscale, the frame that scrolls at 320 px. A reading group in place of the picture would suit all six trackers better (a reader could move item by item); that is a change for all six at once, not for two, so it waits for the review.

### 6. The palette specification (R5-3)

The plate is live text a reader can search and copy (R4-3), generated by the engineer from the tokens. How swatches, values and contrast read:

**6.1 Order.** Palette by palette, in ruling (b)'s order: its job in one sentence, then its table, then its proofs. Labels are `p.k`, never headings. The DOM keeps this order at every width, however the 1440 px layout sets palettes side by side.

**6.2 Each palette's table.**
- `caption` names the palette and its job ("Sequential, Verdigris, five steps: one measure from low to high").
- Columns, each `th scope="col"`: Step (the row header, `th scope="row"`, the swatch inside it, `aria-hidden`); Token (`code`); Value (`code`, as tokens.json prints it); then one column per approved ground for its contrast ("On Newsprint", "On White", "On Charcoal", "On Prussian").
- The swatch sits in the Step cell, never in a column of its own, so no column is read as a run of blanks.
- **A contrast cell** says the ratio and what it allows, in words: "4.29 to 1, marks" (3 to 1 or more, a mark or a large label, 1.4.11), "7.26 to 1, text" (4.5 to 1 or more), "2.10 to 1, not for marks". Never a check mark, a cross or a color alone. A ground the palette is not approved on says "Not used on Prussian"; no cell is empty or a dash.
- **Ratios are rounded down** to two places, so a value never rounds up across 3 or 4.5 (2.996 prints "2.99 to 1").
- **The label ink,** where the plate sets a step's label in its own ink, gives its ratio against the step in the same words.
- **Stone's hatch** is named in words in its row ("Stone, hatched"), and the swatch draws the hatch.

**6.3 Swatches.** Each is a picture of the color: `aria-hidden`, at least 24 by 24 px, with a 1 px edge so it holds on any ground. It keeps its color under forced colors (`forced-color-adjust: none` on the swatch alone; the words and table edges take the system's colors), and it prints: a filled SVG shape, or a box with `print-color-adjust: exact`, since a browser drops CSS backgrounds in print. The engineer's guide check compares each swatch with its token.

**6.4 Values a reader copies.** A token name breaks only at its hyphens with `<wbr>` (the build's `break_code`), never a soft hyphen or zero-width space, so a copy gives the exact name. A hex value never breaks. The grade line's code is a code block a reader copies whole; if it carries a Copy button, it is Rule 18's copy code set with its status line, not a second copy.

**6.5 The proofs.** The grayscale and three color-vision proofs are pictures (`aria-hidden`, or `role="img"` with a short name), and each says its result in words beside it: in gray, how far apart the closest two neighboring steps stand; under each simulation, whether neighboring steps stay apart, and which two come closest if any. Each simulation is explained at first use in plain words (protanopia, where the eye has no red-sensing cones; deuteranopia, no green-sensing cones; tritanopia, no blue-sensing cones), with the method the script names. No figure about how many people have each goes in without its source.

**6.6 Phone widths.** A table wider than the 328 px column either scrolls in its own named frame with a Tab stop, the Step column held at the left (preferred: table semantics hold in every browser), or stacks one row to a block as chapter 26's token table does (AX-S10). In a stacked row each value keeps its label where a reader hears it. Text at 200 percent: no clipped value; a token name wraps at its hyphens.

### 7. S95's second crop (carried, low)

Today both crops are named by the same full alt and described by the card's title, and the "Alt text to post" line repeats the alt as text, so a screen reader hears the alt three times and the title four. Request 1 to the engineer, who holds S95's spec, `work/build/chart-kit/specs/s95.json`, this round: the first crop keeps the full alt as its name; the second is named by its size alone ("The same card at 1080 by 1080 px"); neither crop takes the card's title as its description. The crop names are set where `kit.js` draws each crop (`label_id` for every crop, near line 1276). Then the alt is heard once as a picture's name and once as the words to post, which is that line's job. Nothing is lost as it stands.

### 8. What every round 5 plate keeps

- No decision code, studio word or path in reader text, alt text or a name (the guide check's `codes`); curly quotation marks and apostrophes; no em dash; no U+2011.
- Text at 13 px or more; text contrast 4.5 to 1 (3 to 1 at 24 px, or 18.66 px bold); marks and control edges 3 to 1 (1.4.11), measured on the real ground.
- Every id unique on the page, with the specimen's prefix.
- Nothing moves without a reader's press; nothing happens on hover or focus alone.

### 9. What I test once each item lands

At 1440, 1024, 390 and 320 px, on the light ground (the stage set to Charcoal where a plate offers both), with the keyboard alone and Chromium's accessibility tree (Playwright's snapshot and CDP): Tab order and every key above; the skip links' targets and where focus lands; the way back from an entry; focus visible, inside the stage and never under the masthead (2.4.11); names, roles and states in the tree; the status lines' words after each press; reduced motion; scripts off; print emulation; forced colors, dark and light; text at 200 percent; 320 px reflow; axe-core over each plate; the trackers' alts against their plates' words, and their marks in grayscale. No screen reader runs in this container, so what NVDA, JAWS, VoiceOver or TalkBack say goes under "Not tested". Load under 4 before each browser run.

## Routine calls

- D3-xxx | The selection guide keeps no heading: its 16 questions are an ordered list, each question's forms a list named by its question line | The guide check allows no heading in a plate, and chapter 14's own 16 groups are `p.rg-head`, so the guide reads as the chapter does; lists give screen readers a way between questions
- D3-xxx | Every form link stays in the Tab order, with one skip link past the guide and one per question to the next | Rule 18's link (Tab reaches it, Enter follows it); 144 stops in all, the guide left in one press and any question reached in 16 pairs at most, with or without scripts; arrow-key movement among links would be a new way of working a reader cannot guess
- D3-xxx | No question line in the guide is a link | The opener already links each question to its group; 16 more stops would go nowhere new
- D3-xxx | A form link's name is its name, a hidden comma and its tier word ("Ranked bar, Core"); the rule number joins only if the face prints it | The name starts with what a reader sees (2.5.3), the tier is in words (1.4.1), and no hidden words beyond the pause
- D3-xxx | The selection guide's words and links follow the reader's colors under forced colors (`auto` with its own ground) | A set of 127 live links is controls, not a picture (round 4's rule for live plates)
- D3-xxx | Complex example 2 is one stepper with one step list of seven steps across both loops | One source of state for one drawing; the script counts every step in its root (CE-1)
- D3-xxx | Its buttons keep Rule 18.22's words, "Reset the loop" included | The script's reason line names that word
- D3-xxx | DD-C1, yes: Rule 14.143's status line, controls and reason line move in the markup to directly under the two drawings and the Variable C3 note, before the seven-step list; reading order the drawings, the C3 note, the status line, the controls, the reason line, the list, the limits, the source; Tab order unchanged, Play, Reset the loop, Previous step, Next step, then out (section 2.8) | Today about 1,180 px separate the drawing that lights from the button that lights it, so no window holds both; the move keeps DOM order equal to visual order and adds no stop, and the status line says each step where the list is out of view
- D3-xxx | The chooser's status line counts the marks that turn red on the drawing, none included, and the panel names targets outside the loop | Reform R-38's two targets sit off Loop R8's two steps in today's model; silence or an empty drawing would read as a fault
- D3-xxx | Complex example 3's comparison is a table or three cards with no total, every effect cell its code, qualifier and words, no empty cell | Rule 15.21 and R5-4; a screen reader says "blank" for an empty cell
- D3-xxx | The two trackers follow 11.8 and 11.9: a picture named by an alt that carries every word, in the same pattern | A reader meets six trackers in one group that read alike; a reading group for all six is a change for the review, not for two
- D3-xxx | Contrast in the palette specification prints as "N to 1" with what it allows in words, rounded down | A color or a check mark alone fails 1.4.1; rounding up could cross a threshold
- D3-xxx | The selection guide's "Skip the chart guide" should land right after the guide (the rule index's label) now that the guide sits before the rule index, or its words should name where it lands | A skip link that passes 161 more links than its words say surprises a keyboard reader; Shift+Tab is the only way back to the index

## Requests

### To the engineer

1. **S95's second crop (low, carried from round 4, D3-1875).** In the page, name the second crop by its size alone ("The same card at 1080 by 1080 px") and give neither crop the card's title as its description; the first crop keeps the full alt as its name (section 7). The crops are drawn in `kit.js` near line 1276 with the alt's id as every crop's `label_id`. Please tell the infographics maker, whose spec `work/build/chart-kit/specs/s95.json` you hold this round, if the spec changes.
2. **The selection guide's checks (R5-2, item 7), four more:** each question's list is named by its question line (`aria-labelledby`); every skip link's target exists and is the next question's line or `#group-14-1`; the first skip link is the guide's first focusable element; no question line is a link (section 1.13).
3. **The palette specification (R5-3):** sections 6.2 to 6.6 for the generator: contrast in words and rounded down, the swatch in the Step cell, no empty cell, swatches that print and keep their color under forced colors, `<wbr>` breaks in token names.

4. **(Low, for the review: every picture stage that holds HTML words.)** Chromium exposes the words inside a `role="img"` stage as its descendants: 106 nodes under Rule 11.10's tracker, 103 under 11.8's. A screen reader may say the alt and then the same words again. In `plate()`, wrapping the fragment of an image stage in an element with `aria-hidden="true"` keeps the alt the one thing heard. It changes no pixel, but it reaches every image stage, so measure its reach first (call 2). No screen reader runs here to show what is heard today.
5. **(Low, outside round 5.)** At 320 px with text at 200 percent, the page scrolls sideways by 19 px because of two "Where to start" `span.step-to` links (right edges 324 and 330 px). The guide check's text-spacing test runs at 360 and 390 px, where it passes. This combination goes beyond 1.4.4 and 1.4.10, so the item is a note for whoever owns the start page.

6. **The palette specification (low, 03:30 UTC).** Two items:
   - Let each value break between the hex value and its ratio, and before the words after the ratio ("1.21 to 1" stays whole), in place of `.ps-v`'s `white-space: nowrap`, so the plate stays inside a 390 px screen with text at 200 percent.
   - Give the proof blocks' grounds (`.ps-g`) the same `print-color-adjust: exact` the swatches have, so the Charcoal proof prints on Charcoal.
   Whether every Charcoal stage in the guide should keep its ground in print is a question for the review.

### To the component engineer

1. **The way back from the selection guide (the shell, low reach).** In `guide-shell.js`'s cross-reference click handler, accept `a[data-oa-xref]` beside `a.xref`, and add `[data-return-label][id]` to the elements it remembers as the place to return to (section 1.6). Measured in the V10 page: `data-return-label` sits only on "Where to start"'s route steps, which the handler already remembers, so nothing signed off changes.
2. **Keys files:** sections 2.7 and 3.5, adjusted to ruling (d) and the plates as built.

3. **DD-C1 (02:44 UTC):** once the complex examples maker moves 14.143's status line, controls and reason line above the step list, rerun the keys file's walk on the plate; the path itself should need no change, since the four buttons stay the plate's only stops and come first from before the stage (section 2.8).

4. **The masthead's offset at 1,024 to 1,100 px (low, 04:19 UTC).** There the masthead measures 101 px while `--head-h` reads 4rem (64 px), so `main *`'s `scroll-margin-top` is 88 px and a target whose first line is its top lands 13 px under the masthead. Example: the selection guide's form item that the way back returns to. Rules' headings clear it because they sit lower in their blocks. Set `--head-h` to the masthead's height at those widths, measured as at 390 px, where it reads 3.5rem + 2rem against an 89 px masthead. Shell-wide, so measure its reach first (call 2).

### To the selection guide maker

1. Section 1 whole: the markup in 1.2 and 1.3, the pictures in 1.4, the skip links in 1.5, the return labels in 1.6, and 1.7 to 1.12.

2. **Where "Skip the chart guide" lands (low, 04:19 UTC).** The guide now sits before the rule index, so `#group-14-1` passes the rule index and the local contents as well, while the link's words name only the guide.
   - Point the first skip link and the 16th question's skip link at the rule index's label (`data-visualization-index-t`), so each lands right after the guide.
   - Or, if the studio wants the jump straight to the rules, let the words say so ("Skip to Rule 14.1").
   My section 1.5 assumed the guide would sit in the chapter's body; whichever way you choose, I retest it.

### To the complex examples maker

1. Sections 2, 3 and 4. Above all: the step words that name each loop and the hand-off (2.4); C3 marked as shared by shape and words (2.5); the plate CSS items in 2.6, since chapter 15's scoped CSS does not reach chapter 14; the status line for a reform with nothing on the loop (3.2); the comparison's table or cards with no total and no empty cell (3.3); print-only copies of the drawing per reform if you can (3.4); S96's table columns and date order (4.3).

2. **DD-C1 (02:44 UTC), yes:** in 14.143's markup, move the status line, the controls group and the reason line to directly after the Variable C3 note, before the seven-step list; no CSS `order` or placement, and print, reduced motion and scripts off keep the still sequence (section 2.8).

3. **Rule 14.144, Must (1.4.4), 03:31 UTC.** At 200 percent text on the 680 px composition (1440 px, and the 1024 px desk by the same layout), the three cards stay three columns of about 234 px, so words overlap the next card and R-38's card runs 13 px past the stage. Set the columns in em so larger text takes fewer, for example three columns only where each card holds about 14em (a container query in em on the cards' row) and one card a row below that, as the phone already does. DD-R1's shared rows need only one column count at a time. Capture: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/accessibility/shots-complex/s-14-144-cards-1440-text200.png`. I retest once it lands.

4. **Rule 14.144 (low, 04:19 UTC).** At 320 px with text at 200 percent, "+M renter-owner" and the chips "Connection LE17" and "Connection LT12", each on one line, run up to 29 px past their card (inside the frame). Letting a code break before its qualifier would close it. 320 px at 200 percent goes beyond 1.4.4 and 1.4.10, so this is optional. **Item 3 is closed:** one card a row at 200 percent text at 1440, 1024 and 390 px.

### To the tracker designer

1. Section 5: the state words, the status lines and the alt pattern of 11.8 and 11.9, "Illustrative" in the alt, and "You can take part now" only where the research lead's source names a public step.

### To the data lead

1. **Ruling (a):** the avoid form's word on the tile ("Avoid", with any further words joining the link's name after it) and its mark, never red alone.
2. **Ruling (d):** today's model puts Reform R-38's targets (LT12, TC7) and one each of R-06's (B5) and R-30's (LE17) off Loop R8's two steps. Please rule whether the drawing draws them attached or the panel names them, so the status line can count what turns red (section 3.2).

### Words for the editor

The skip links ("Skip the chart guide", "Skip these N forms"); the return label ("Ranked bar in Choose a chart"); the tiers' line at the guide's head; the guide's alt; complex example 2's group name and status lines (2.3, 2.4); complex example 3's legend and status lines (3.1, 3.2); S96's table caption and column headers (4.3); the palette specification's contrast words (6.2). Each example here is a pattern; your words decide.

## Tested

- Read in the V10 page (`work/boards/phase-3/round-4/20261113_Guide-Preview-V10.html`) by script (`ch14_top.py`, `ch_body.py`, `rule_struct.py` in my scratch): chapter 14's head (opener with 16 question links to groups, the rule index with every rule linked, the local contents), its body order (group blocks as `p.rg-head`, rules as `h3` in `div.rule#rule-14-NN`), an avoid rule's sketch plate ("Form to avoid: Do not publish"), and that no tier word is printed in the chapter today.
- Read the shell's cross-reference and return code (`guide-shell.js` lines 149 to 200) and its chooser and print code (lines 563 to 593); `[tabindex="-1"]:focus` draws no ring and `main *` carries `scroll-margin-top` (`guide-shell.css`); `data-return-label` appears only on route steps in V10.
- Read `c-18-loop-stepper.js` whole: it counts every `.oa-stepper-step` in its root and writes "Step k of N"; its reason line names "Reset the loop".
- Read chapter 15's scoped plate CSS in V10: `.lv`'s forced-colors pair, the scripts-off rule, the counter, three print blocks and the 320 px container rule, all under `@scope (#systems-graphics [data-specimen])`.
- Read chapter 11's tracker plates 11.8 and 11.9, correct and failure, and their manifest alts.
- Read S95's spec and the kit's crop naming (`kit.js` lines 810 to 830 and 1273 to 1278; `kit-build.js` line 464).
- Read from the atlas model by script: Loops B4, R10 and R8, their connections' signs, delays and grades and their variables' titles; Reforms R-06, R-30 and R-38's targets, effects and routes.
- The plan file's 127 form names are unique; its tiers are Core 56, Extended 40, Reference 22, Avoid 8, "Extended, interactive" 1.

- **Rules 11.10 and 11.11 as built (02:44 to 02:54 UTC).** Static, by script on the specimens and `manifest-systems.json` (files of 02:41): each correct plate's alt holds every row's status line word for word (no-break spaces read as spaces) and every step's state in the plate's own key words, in 11.8's pattern ("Steps: 1 Filed done; 2 Title and summary done; 3 Signatures done; 4 Legislature never happened; 5 On the ballot done; 6 Vote now"); "Illustrative" opens each alt; each key lists only the marks its plate draws (11.10: Done, Now, Not yet, Never happened, Stopped; 11.11: Done, Now, Not yet, Stopped; the failures only theirs); the decided and certified items say so in words ("Approved by voters on November 3, certified on November 24.", "Reversed and sent back by the Supreme Court on June 2."), the stopped ones end on a square with the steps after it "not yet" (Measure 99013 at step 3, Case 99016 at step 5); no take-part mark, rightly (the measure at step 6 has its polls closed, and no court step is open to the public); both failure alts open "Failure case: do not publish." and both failure captions lead with "Fails Rule 11.10." and "Fails Rule 11.11." in bold; every SVG is `aria-hidden`.
  In Chromium (Playwright 1.63), on my build of the working tree at 02:45 (`guide_build.py`, not strict, exit 0, 0 warnings, 12,090,747 bytes, scratch `b1/`; the build's rewrite of `plate-share.json`'s time was put back), `tracker_test.js` and `tracker_test2.js` in my scratch:
  - **Names:** each stage is one image (CDP role "image") named by its manifest alt exactly (1,288, 413, 1,134 and 382 characters).
  - **Keyboard alone, from a stand-in button before each figure:** at 1440, 1024 and 390 px the plate takes no Tab stop (its frame holds the 360 px stage whole, no hint shown) and the next stop leaves the figure, with the 2 px Verdigris ring. At 320 px the frame takes one stop, named "Correct application, Rule 11.10, at true size. Scroll sideways to see all of it." (and the same for each), with the shell's 2 px inside ring, below the masthead and not covered (`elementFromPoint`), and the hint shows.
  - **Text:** smallest 13 px at every width (the step numbers), every text 4.5 to 1 or more against what it sits on; the lowest is a "not yet" number in the muted ink, 5.49 to 1.
  - **Marks against Newsprint,** each mark's painted fill or stroke: Done, Now, Never happened, Stopped and the done line 13.29 to 1; Not yet and its line 4.29 to 1 (Stone), the same figures as 11.8's.
  - **Shapes:** captures at 1440, 390 and 320 px read. Filled circle, 3 px ring, thin gray ring, ring with a slash, and filled square stay apart without color.
  - **Text at 200 percent** at 1440, 390 and 320 px: nothing in the stages clipped or past their edge, smallest text 26 px. At 1440 and 390 px no sideways page scroll. At 320 px the frames scroll as at 100 percent (their sides grow with the text, 424 px against 392 px), and the page scrolls sideways by 19 px because of "Where to start"'s `span.step-to` links, outside chapter 11. 320 px with text at 200 percent asks more than 1.4.4 or 1.4.10 do, so this is a note, not a fault (engineer 5, low).
  - **Print emulation** with `beforeprint`: every stage shown, text and marks as on screen; the two correct plates may break across pages (the shell's tall-plate rule), the failures keep whole.
  - **Forced colors,** dark at 1440 px and light at 390 px: each plate keeps its picture on its own Newsprint (`forced-color-adjust: none`), text 5.49 to 1 or more, marks as on screen.
  - **axe-core 4.10.2** on each figure at 1440 px, WCAG 2.2 AA tags: 0 violations, 15 passes; color-contrast incomplete (axe cannot resolve text inside an image role), which the measure above covers.
  - **The tree:** Chromium exposes each tracker image's HTML words as descendants under it (106 nodes under 11.10's image, 62 under 11.11's failure), as it does under 11.8's (103) and the chapter 14 opener's. Whether a screen reader then says them after the alt is untested here (engineer 4).
  - **Met.**

- **My strict build for the tests (03:00 UTC):** `guide_build.py --strict` of the working tree at HEAD a952b1a1 to scratch `b3/`, 12,096,754 bytes. It exited 1 on two warnings, both S96's ("no clear place for the words of 2026-02 at 656 px" and "at 558 px", the complex examples maker's chart), which touch none of the items below. The page was written and is what I tested. The build's rewrite of `plate-share.json`'s time was put back.
- **Rules 11.10 and 11.11, counted run (03:00 to 03:08 UTC, load 1.50 at the start).** `tracker_test.js` on `b3/`, with the specimens of 02:48:45. Every figure equals the 02:46 run's but one: 11.10's correct alt changed with the tracker designer's edits and still equals its manifest alt word for word. With scripts off and with reduced motion (`static_modes.js`, 03:31) the four stages hold no script, animation or `data-oa-motion`, and read as with them. **Met.**
- **Rule 14.143 as final (03:13 to 03:24 UTC, plate of 02:45:17, load 3.90 and 3.65 at the starts).** `complex_test.js` on `b3/`. **Met.**
  - **Order (DD-C1):** the DOM and the page set the drawings, the C3 note, the status line, the controls, the reason line, the seven steps, then the source, in that order at 1440, 1024, 390 and 320 px. Play stands 148 px under the drawings at 1440 and 1024 px, 232 px at 390 and 274 px at 320 (about 1,180 px before).
  - **Keyboard alone,** the component engineer's keys file walked by my own script from a stand-in before the stage:
    - The hand path, 18 steps, at 1440, 1024, 390 and 320 px: every step passes. The status line runs "Loop B4, step 1 of 3:" to "Loop R10, step 4 of 4:", then "Loop R10, step 3 of 4:" after Previous step, then the ready line after Reset the loop. `data-oa-at` runs 0 to 7. Focus never moves. Each focused button shows the 2 px Verdigris ring at 2 px, below the masthead, not covered and inside the visible frame.
    - The Play path under reduced motion (Play, Pause, Play) passes at every width.
    - Tab stops from before the figure: Play, Reset the loop, Previous step, Next step (each 44 px tall), then the caption's link. At 320 px the frame's own stop comes first, with its inside ring.
  - **Each step by Next step:** exactly one step carries `aria-current`; the steps ahead carry `data-oa-ahead`; one drawn group per step carries `data-s`. Each hold equals 250 ms a word of its status line, never under 6,000 ms (12,750, 10,750, 20,500, 14,000, 13,750, 12,000 and 19,500 ms). At the last step Next step is unavailable and the reason line reads "At the last step. Reset the loop to start again."
  - **Scripts off:** the root takes no `data-oa-live`; the buttons, status line and reason line are hidden; all seven steps show, numbered, none current.
  - **Print emulation at step 3:** the same still sequence, every step in ink.
  - **Forced colors,** dark at 1440 px and light at 390 px: the live root takes `auto` with the system's Canvas (black or white), words at 21 to 1, button edges in the system's text color, and the drawing keeps `none` on its own Newsprint.
  - **Text at 200 percent** at 1440, 390 and 320 px: nothing clipped, every control inside the visible frame.
  - **axe-core 4.10.2 at 1440 px:** 0 violations, 19 passes.
- **Rule 14.144 as final (same runs, plate of 02:44:47).**
  - **Keyboard alone:** the keys path walks clean, 13 steps at 1440, 1024, 390 and 320 px. The radios wrap. The status lines read:
    - "Reform R-30 turns one connection and one variable red. One connection it targets sits outside this loop, in the economy layer."
    - "Reform R-38 turns no mark red. Its two targets sit outside this loop, in the technology layer."
    - "Reform R-06 turns one connection red. One variable it targets sits outside this loop, in the core layer."
    - Focus stays on the radio, and the status line is empty on load.
  - **Tab stops:** the radio group, then each card's disclosure summary (three, 60 to 81 px tall), then out. At 320 px the frame comes first. Every stop shows the 2 px ring, inside the frame, not covered.
  - **Red marks after the 120 ms token:** R-06 lights the group it shares with R-30, Connection L39. R-30 lights L39 and its own, Variable A5. R-38 lights none, as its line says.
  - **The comparison:** three cards (`li[data-oa-panel]`), each a `dl` with the same eleven terms in the same order, Targets on Loop R8 to Routes. No empty term or value; "None" where a reform has no target on the loop. No total, sum, average or rank in the words. Each effect keeps its code and qualifier whole with its words ("+L local, large positive"). Each route without a date reads "Not checked."
  - **Scripts off:** the radios choose; the red follows from CSS; the status line stays silent.
  - **Print emulation:** the radio group hidden, the three cards shown, the three disclosures opened by the shell and closed again after. The three print copies of the drawing show, one per reform (my section 3.4's better page).
  - **Forced colors:** as 14.143's.
  - **axe-core:** 0 violations, 22 passes.
  - **Text at 200 percent:** at 390 and 320 px nothing is clipped. **At 1440 px it fails 1.4.4:** on the 680 px composition the three cards stay three columns of about 234 px, so words run into the next card ("Connection LE17" over "Shared-data pricing", the chips of R-30's and R-38's routes), and R-38's card runs 13 px past the stage's edge. Capture `shots-complex/s-14-144-cards-1440-text200.png`. The 1024 px desk sets the same 680 px composition and was not run at 200 percent. Request below.
- **The palette specification read as text (03:24 to 03:30 UTC, specimen of 02:04:53).** `palette_test.js`, `palette_follow2.js`, `palette_follow3.js` and `static_modes.js` on `b3/`. **Met, with two low items.**
  - **Placement:** after Rule 14.5. Its line in the local contents reads "The four data palettes, step by step".
  - **The tree:** a group named "The four data palettes, step by step, specimen" and described by the alt; four tables, each with a caption and five column headers (Step or Group, Token, On Newsprint, On Charcoal, On White paper). Each row's header holds the step and its code with the swatch `aria-hidden`; each cell holds the value, its ratio in words ("1.21 to 1, not for marks alone", "9.42 to 1, marks", "13.28 to 1, text"), the label ink's ratio and the step's lightness. No empty cell. The proofs are images with names, and their results are lists in words (nearest neighbors in gray and under each simulation, with the bar). Prussian is one note in words, not a column.
  - **Keyboard:** no Tab stop inside the stage at any width; the next stops are the caption's links.
  - **Text:** 13 px or more. Every number on a swatch measures 4.61 to 1 or more against the swatch it sits on (the lowest, Newsprint on sequential step 3 on Charcoal, at 13 px). My first measure read 1.00 to 1 by setting a swatch's number against the cell's ground; the second, against the swatch's own rect, corrects it.
  - **Reflow:** at 390 and 320 px the tables stack one row to a block, and Chromium keeps table, row, header and cell roles with each cell's label ("On Newsprint") read in it. No sideways scroll at 1440, 1024, 390 or 320 px.
  - **Forced colors,** dark and light: swatches keep their colors (`forced-color-adjust: none`), and the words take the system's.
  - **Scripts off and reduced motion:** no script, no animation, no change.
  - **axe-core:** 0 violations, 19 passes.
  - **Text at 200 percent, low:** at 390 px each value with its ratio is held on one line (`.ps-v`, `white-space: nowrap`), so the stage widens to 496 px and the frame scrolls (560 against 390 px, with its Tab stop once the shell re-measures). Nothing is lost, which 1.4.4 asks, but every line of the plate then needs a sideways scroll. At 1440 px it fits.
  - **Print, low:** the swatches, strips and lines print (`print-color-adjust: exact`). The proof blocks' Newsprint and Charcoal grounds (`.ps-g`) compute `economy`, so under a browser's default print setting the Charcoal block's labels print in Newsprint ink on white paper. Read from computed styles in print emulation, not from a printed page. Every Charcoal stage in the guide prints the same way; nothing in the shell keeps a ground in print.

- **The selection guide, "Choose a chart" (04:05 to 04:19 UTC).** Specimen of 03:53:57 in my strict build of 04:03 (`guide_build.py --strict` to scratch `b4/`, exit 0, 0 warnings, 12,106,233 bytes, HEAD bae34442; `plate-share.json`'s time put back). `sg_test.js`, `sg_follow.js` and `sg_follow2.js` in my scratch, all started under load 4. **Met, with two low items.**
  - **Static, by script against the plan:** 127 form links, each rule once, each under its own question; each link's text starts with the plan's form name and holds its tier word ("Extended" for Rule 14.130, as ruling (a) set it); `data-oa-xref` on every link; each form's `li` carries `s-14-sg-f-NN` and `data-return-label` ("Ranked bar in Choose a chart"); every `svg` is `aria-hidden` and `focusable="false"`; no heading, no `title`, no `aria-label` on a link; one `ol` of 16 questions, each with its question line, its skip link and a `ul` named by `aria-labelledby` its question line; the tier key is a `dl` of four terms; grid columns in rem (`minmax(min(100%, 9rem), 1fr)`); no `order` or `dense`; `forced-color-adjust: auto` on the root; print hides the skip links.
  - **Placement:** the figure stands straight after the opener, before the rule index. The stage is a group named "Choose a chart, interactive specimen", described by the alt. The local contents line reads "Choose a chart".
  - **Names, read from Chromium's own tree (CDP):** "Ranked bar, Core", "Column, Core", "Radar chart, Avoid", "Streamgraph, Avoid". The hidden comma makes the pause. All 127 form names are unique; the only repeated names are skip links with the same count ("Skip these 10 forms" twice), which their questions tell apart (2.4.4). 128 SVGs, none exposed.
  - **Keyboard alone,** from a stand-in before the figure, at 1440, 1024, 390 and 320 px:
    - 144 stops in DOM order: "Skip the chart guide", "Skip these 10 forms", "Ranked bar, Core" and on to the last form, then out to the rule index.
    - Every stop has the 2 px Verdigris ring, is in view below the masthead, is not covered and sits inside the stage. Every skip link shows when focused (no clip). No form tile is under 44 by 44 px (smallest 120 by 114 px at 320 px).
  - **Skip links:**
    - "Skip the chart guide" lands on `#group-14-1` with focus there, and the next Tab is group 1's first link.
    - The 16 question skip links, taken in turn with Tab and Enter, each land on the next question's line, which takes focus and reads its question ("Shift and swing: what moved, and which way?"). The 16th lands on `#group-14-1`.
    - With scripts off, the same two kinds of skip land and the next Tab continues from them ("Skip these 10 forms" leads to "Skip these 4 forms").
  - **The way back (component engineer's S-2)** at every width: Enter on "Ranked bar, Core" puts focus on Rule 14.15's heading; Tab reaches "Return to Ranked bar in Choose a chart, 14 Data visualization"; Enter puts focus on the form's item; the next Tab is "Ranked bar, Core" again. The same holds for Histogram and Social data card.
    - **Low:** at 1024 and 1100 px the masthead measures 101 px while `--head-h` reads 4rem, so the returned item lands at 88 px, and its top 13 px and its link's top sit under the masthead. The link stays mostly in view, so 2.4.11 is met; 2.4.12 is not. Rules' headings land at 122 px and clear it. At 1440 (masthead 65 px) and 390 px the item lands clear.
  - **Reading order:** each tile is right of or below the one before it, in every question at every width; questions run down one column. Tiles a row: 4 to 5 at 1440, 3 to 4 at 1024, 2 at 390 and 320 px, 1 at 1024, 390 and 320 px with text at 200 percent.
  - **Text:** 14 px or more; the lowest is the tier key's words at 5.49 to 1. With text at 200 percent at 1440, 1024, 390 and 320 px nothing is clipped, tiles do not overlap, and none runs past the stage. At 320 px the frame then scrolls with its Tab stop (its sides grow with the text), and the page's 19 px sideways scroll is "Where to start"'s, as before.
  - **Forced colors,** dark at 1440 and light at 390 px: the root takes the system's Canvas; names and tiers take the link color (yellow on black, dark blue on white), 19.56 and 13.99 to 1. The pictures draw in the system's colors, and the avoid mark keeps its cross (capture read).
  - **Print emulation:** skip links hidden; all 127 links and 127 pictures shown; tiles keep whole; each question line stays with its tiles; no address added after a link.
  - **Reduced motion:** no animation; transitions 0 s.
  - **axe-core 4.10.2 at 1440 px:** 0 violations, 19 passes, none incomplete.
  - **Low, where "Skip the chart guide" lands.** The guide now stands before the rule index (161 links) and the local contents, so `#group-14-1` passes all three while its words name only the guide. Section 1.5 set that target when the guide was planned for the chapter's body; the 16th question's skip link does the same. Request below.
- **Rule 14.144 at 200 percent text, retested (04:15 UTC, plate of 03:50:02).** The complex examples maker's fix holds:
  - At 1440, 1024 and 390 px the three cards stand one a row (632, 296 and 296 px wide), none past the stage, no word outside its card, no sideways page scroll. **The Must is closed.**
  - **Low:** at 320 px with text at 200 percent, three typed chips ("Connection LE17", "Connection LT12") and the code "+M renter-owner", each held on one line, run 2 to 29 px past their 224 px card. They stay inside the frame, which scrolls. 320 px at 200 percent text goes beyond what 1.4.4 and 1.4.10 ask.

## Not tested

- The selection guide at 768 and 360 px; its hover state; any screen reader's reading of its list names.
- Rule 14.144 at 1024 px with text at 200 percent (the same 680 px composition as 1440 px, where it fails); 768 and 360 px for every item; Charcoal for 14.143 and 14.144 by the stage's theme (the design director read both grounds).
- A printed page or PDF of the palette specification: print was read from computed styles in print emulation.
- Rule 14.142 (S96): not asked in this pass, and its spec still carries two strict build warnings.
- Any screen reader: none runs in this container. What a screen reader says for list names, skip links and status lines is what the markup exposes, not what a reader hears.
- Safari and Firefox: no WebKit or Gecko run here, so `:has()` fallbacks, list roles after `list-style: none` and table semantics in a stacked table are unverified.
