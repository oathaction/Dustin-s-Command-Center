# Second pass accessibility notes

Oath & Action Edition 06, Phase 3, DR-191's second pass, chat 8, November 20, 2026. Written by the UX and accessibility lead (`oa-ux-accessibility-lead`) under `work/handoffs/phase-3/20261120_Second-Pass-Brief.md`. Items: RS-1 and RS-7 checked in Chromium's accessibility tree, Rule 14.143's alt, and a glance at CR-S1's remainder and CR-S23. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/accessibility/` (`scratch/` below).

## Status

- 17:10 UTC: started. Read my role file (`oath-and-action-v6-brand-guide/.claude/agents/oa-ux-accessibility-lead.md`; the path at the repository root does not exist), `CLAUDE.md`, the brief and the engineer's notes.
- 17:11 UTC: Rule 14.143's alt changed in `rule_14_143()`; generator run (1 of 10 written, 0 faults), `--check` 10 of 10 current; strict build to scratch, exit 0, 0 warnings. The main session's snapshot `c203fe2d` (17:14 UTC) holds the line and its entry.
- 17:15 to 17:16 UTC: browser run 1. 17:19 to 17:20 UTC: browser run 2. Each opened after `browsers.sh` printed "OK to open one" and closed before the next.
- 17:21 UTC: running `phase3_ch14_build.py`, which carries the entry's alt into the page's manifest, was refused by the session's permission check as outside my write scope. Left as a request.
- 17:23 UTC: **done.** RS-1 confirmed except one order point inside the correct plates' cards (Not confirmed, editor). RS-7 confirmed. 14.143's alt fixed in source and entry; it reaches the page when the main session runs the chapter 14 assembler (Requests). Nothing lost for keyboard or screen reader users on 15.20's failure plate or 14.144's line-up.

## Confirmed

### RS-1: the six tracker pictures (Rules 11.10 to 11.12)

Stages `s-11-10-correct`, `s-11-10-failure`, `s-11-11-correct`, `s-11-11-failure`, `s-11-12-correct` and `s-11-12-failure`, read in Chromium 157 at 1440 and 390 px.

- **Hidden.** Each stage is an image in the tree (`role="img"`), and Chromium's computed name equals its `aria-label` character for character. The fragment's wrapper is ignored ("ariaHiddenElement"), its first paragraph is ignored ("ariaHiddenSubtree"), and the image has no descendant left in the tree. The build report agrees: pictures 101 hidden and 315 open, none of the six in `open_stages` (95 and 321 before this pass, with all six open).
- **Heard once.** In each figure the tree holds four things: the plate label ("Correct application" or "Failure case"), the size line ("True size, 360 px wide"), the image named by the alt, and the caption. The alt's words sit in the image's name only; the image carries no description, the caption's words differ, and the frame name is a data attribute that no reader gets.
- **Complete.** Every word the picture shows is in its alt. I took each picture's visible text nodes from Chromium at 1440 px and matched them against the alt with the build's own word pattern: nothing missing on any of the six.
- **Illustrative first.** The three correct alts open "Illustrative." The three failure alts open "Failure case: do not publish. Illustrative.", which is the order the picture sets them: the failure band, then the Illustrative label. The caption carries no second label, since the piece draws its own (CD-N1). The label is heard once, at the head.
- **Order, outside the cards.** The alts run in the picture's order: label, title, then each card in turn, then the key ("The six steps", then "What the marks mean"). The three failure alts follow the picture's order inside their one card too: the name, the marks in words, then "The words read" and the card's sentence.
- **Nothing became unreachable.** Each hidden picture holds no link, button, field or tab stop (0 focusable elements, by query, at both widths), and the build's control test found none. Tab from just before each figure goes straight to the first link after it ("13 Evidence and sourcing") at 1440 and 390 px. The True size switch stays hidden (the 360 px stage fits at both widths, 0 px of overflow) and the frame is no tab stop.

### RS-7: Rule 15.19's stepper against Rule 14.143's

- **DOM order**, both plates, both widths: drawing, status line, controls (a group named "Steps of Loop R1" on 15.19 and "Steps of Loops B4 and R10" on 14.143), the reason line, the list, then the limits and the source.
- **Visual order.** At 390 px both plates stack in DOM order (15.19: drawing 177, status 571, buttons 667, reason 875, list 939 px down the stage; 14.143: 16, 1,483, 1,600, 1,808, 1,872). At 1440 px 14.143 stacks under its two drawings (status 816, buttons 891, reason 995, list 1,035), and 15.19 sets its drawing in a left column with the status line, buttons, reason line and list down a right column (58, 154, 362, 426). Read column by column, 15.19's visual order matches its DOM order. The reason line sits 16 px above the list on both plates at both widths.
- **Tab order**, both plates, both widths: Play, Reset the loop, Previous step, Next step, the link "Rule 18.22", then out of the plate. Each stop draws a 2 px solid outline and sits on screen. Reset the loop and Previous step are `aria-disabled="true"` at load, stay focusable, and are described by the reason line ("Previous step and Reset the loop work once you press Next step or Play.") on both plates.
- **What a screen reader hears first.** Entering either plate: the group "Correct application, Rule 15.19, interactive specimen" (or Rule 14.143), described by its alt. Then, in reading order: the grade label and the loop's chip and title (the drawings are hidden from assistive technology); on 14.143 the second loop's label and title, the note on Variable C3 and the line key; then on both the status line, the group of four buttons, the reason line, the numbered list, the atlas's limits and the source. From the status line on, the two plates match.
- **The status line announces each step.** On both plates and at both widths the status line is a `status` region (live "polite", atomic). Pressing Next step three times, Previous step once and Reset the loop once, by keyboard (Enter), changes its text each time in the same node, which stays in place: "Step 1 of 3: ..." to "Step 3 of 3", back to "Step 2 of 3", then "Ready. ..." on 15.19, and "Loop B4, step 1 of 3: ..." in the same way on 14.143. The current list item takes `aria-current="step"` and loses it on reset.
- **The alts.** 15.19's alt names "a status line, four buttons (Play, Reset the loop, Previous step and Next step) and the three steps in order", the plate's order. 14.143's alt now does the same in source (Fixed); the page shows it after the request below.

### CR-S1's remainder and CR-S23, at a glance

- **15.20's failure plate (two 296 px options).** No input, button, role or tab stop (0 focusable, by query); Tab passes it at both widths. The stage is an image named by its alt, which still fits the new faces ("a chooser with two boxes ... both checked": each option is a bordered face with a check). The options' new list form adds nothing a keyboard user can reach. One older point stays as it was: the plate is one of the 315 open stages, since its alt leaves out the two reforms' quoted titles and the loop's title, and in Chromium the image keeps 93 descendants in the tree, so whether a screen reader user hears those titles depends on the reader. It was open before this pass (16:32 report), and the pass changed no words.
- **14.144's phone line-up.** At 1440 px the line-up is not rendered and is absent from the tree. At 390 px it is in the tree as the heading line, a list of families and a list of rows; each row reads "Reform R-06", "+L local", "large positive". The pips are `aria-hidden` and their meaning is in the code and its words. In each row the DOM order (chip, pips, code, words) is the visual order: the chip on its own line, the pips, code and words on the next (left edges 47, 47, 143 and 209 px in the first row). Nothing in it is focusable. Nothing is lost.

## Fixed

| Code | What changed | File | Proof |
|---|---|---|---|
| RS-7 follow-up (the engineer's request) | Rule 14.143's alt names its parts in the plate's order: "a status line, four buttons (Play, Reset the loop, Previous step and Next step) and the seven steps in order, Loop B4’s three then Loop R10’s four", as 15.19's alt reads. One string in `rule_14_143()`; nothing else in the file changed | `work/build/scripts/phase-3/phase3_ch14_complex_build.py`, then its output `work/build/guide/entries/14-143.json` | `--check` before: 10 of 10 current. Generator: 10 files, 1 written (the entry), 0 faults. `--check` after: 10 of 10 current. `git diff` showed the one string in each file and nothing else. The entry stays 6,170 bytes (the alt keeps its length); `s-14-143-correct.html` unchanged at 25,223 bytes (the alt is not in it). Strict build `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out scratch/build/guide.html`: exit 0, 0 warnings, 12,178,927 bytes; `plate-share.json` not rewritten. Committed by the main session in `c203fe2d` |

## Not confirmed

- **RS-1, order inside each card of the three correct plates.** Every word is present and heard once, but inside each card the alt reads the card's sentences before its marks ("Measure 99010, State park entry fees: Step 6 of 6: Vote. The polls closed ... Steps: 1 Filed done; ..."), while the picture sets the row of numbered marks under the name and the sentences under the marks. On 11.12's correct plate the alt's "Steps" line also falls between the "Waiting on you" line and the warning line, which the picture sets after the marks. The failure plates are in order. No WCAG criterion fails here (1.1.1 is met: the alt serves the picture's purpose), so this is a Could, not a block. Fix, if the editor agrees: move each card's "Steps: ..." line to follow the card's name. Owner: the editor, `work/build/scripts/phase-2/apply_systems_ch11.py`, for the deferred fixes register.
- **14.143's new alt on the page.** The page still carries the old wording as the group's description, because the guide reads alts from `work/build/guide/specimens/manifest-data-visualization.json`, which `phase3_ch14_build.py` writes from the entry. Its `--check` shows that file the only one of 99 not current. Running it was refused as outside my write scope. Owner: the main session (Requests).

## Calls

- D3-xxx | RS-1 passes in the accessibility tree; the order inside the correct plates' cards goes to the register as a Could for the editor | each picture is hidden, its alt is complete and heard once with the Illustrative label first, and the cards and key run in the picture's order; only the order of a card's sentences against its marks differs, and that loses no word
- D3-xxx | I concur with the data lead's call that the six alts may leave out the sample "4" drawn inside each key mark | the key teaches each mark's shape, which the alt says in Rule 11.2's words; the numbers each card's marks carry are read in its "Steps" line
- D3-xxx | RS-7 passes: 15.19's DOM order, Tab order and first heard content match 14.143's at 1440 and 390 px | measured in Chromium's tree and by keyboard on both plates; 15.19's two columns at 1440 px read in DOM order, column by column
- D3-xxx | Rule 14.143's alt names a status line, four buttons and the seven steps, in that order, in 15.19's words | a group's description read before its parts should list them in the order a listener meets them

## Requests

- To the main session: run `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py` (then its `--check`) so 14.143's new alt reaches `manifest-data-visualization.json` and the page. Its `--check` at 17:21 UTC showed that one file of 99 not current, from the alt alone.

## Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch14_complex_build.py --check` before and after the edit (10 of 10 current each time), and the generator once (1 written, 0 faults).
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py --check` at 17:21 UTC: exit 1, 98 of 99 current, the manifest the one stale file.
- Strict build at 17:11 UTC of the tree then (snapshot `1a2bfdb4` plus the alt), to `scratch/build/guide.html`: exit 0, 0 warnings, 12,178,927 bytes; pictures 101 hidden, 315 open; none of RS-1's six open; `s-15-20-failure` open, as in the main session's 16:32 report (95 and 321).
- Offline, from the built page: each of the six stages' markup (image role, `aria-label`, the `data-oa-picture` wrapper with `aria-hidden="true"`), the stepper reason lines' ids (unique per plate: `s-15-19-correct--oa-stepper-why` and `s-14-143-correct--oa-stepper-why`), and the 14.143 description paragraph's text.
- Browser run 1 (`scratch/tools/ax.cjs`, Playwright's Chromium 157.0.8103.78, Newsprint, 1x, one browser, opened 17:15:55 and closed 17:16:50 UTC), on `scratch/build/guide.html` at 1440 and 390 px, through the Chrome DevTools accessibility domain: for the six tracker stages, each stage's role, name and description, the wrapper's and first paragraph's ignored reasons, the image's descendants, each figure's tree, focusable elements inside each picture, the frame's overflow and the Tab path from just before each figure; for 15.19 and 14.143, DOM and visual order, the stage's name and description, the Tab path with each stop's role, name and outline, and the status line's role, live and atomic values and text after Next step three times, Previous step once and Reset the loop once, by keyboard, with `aria-current` on the list; for 15.20's failure, its role, tree, focusable count and Tab path; for 14.144, the line-up's presence in the tree and each row's part positions. Output in `scratch/run1/ax.json`. No captures.
- Browser run 2 (`scratch/tools/ax2.cjs`, same build, opened 17:19:56 and closed 17:20:28 UTC): the deduplicated tree of 15.19 and 14.143 at 1440 px, the controls group's name and each button's name, description and disabled state at both widths, and 14.144's line-up tree at 390 px. Output in `scratch/run2/ax2.json`.
- Picture words against alts (`scratch/tools/order.py`, `order2.py`, on run 1's text nodes): no word missing; block order as reported above.
- After each run `browsers.sh` and `ps` showed only the guide check's browser left.

## Not tested

- Any screen reader (NVDA, JAWS, VoiceOver, TalkBack). The announcements are inferred from Chromium's tree: a polite, atomic status region whose text changes in place. I heard nothing.
- Firefox's and Safari's accessibility trees (DR-279).
- 14.143's new alt as the page's group description, since the manifest is not yet rebuilt.
- Play and its timed steps, and the stepper with reduced motion; only Next step, Previous step and Reset the loop were pressed.
- Focus hidden behind the sticky masthead (2.4.11): I checked only that each focused control sat inside the viewport, with the masthead as the page sets it.
- 360 and 320 px, 200 percent text, forced colors, Charcoal, print and scripts off, for every plate here.
- Target sizes and contrast on the changed plates.
- The guide check, which the main session runs on the joined build.

## Board 3 ruling: the keyline

Without the keyline, Rules 15.11, 15.16, 15.20 and 14.144 still meet WCAG 2.2 AA (1.4.11): each names every red target in words beside the drawing, by the title its pill or step carries, so the 2.96 to 1 ring is never the only way to find one. Rule 15.12 does not: its words never name the one red variable, “Availability of local reporting”, so the ring is a sighted reader’s only sign of it (the alt reaches screen readers only); naming it in the plate’s words, or the keyline, would meet AA.
