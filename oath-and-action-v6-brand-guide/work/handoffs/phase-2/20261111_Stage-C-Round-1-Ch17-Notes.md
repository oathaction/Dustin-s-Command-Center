# Stage C, round 1: chapter 17, Motion and states, systems designer's notes

Oath & Action Edition 06, Phase 2, stage C, round 1, November 11, 2026. Written by the systems designer (`oa-design-director`, checked against `oa-ux-accessibility-lead`), run as a subagent of the main session, under `20261111_Stage-C-Round-1-Brief.md` (chapter 17's row and the fixed rule numbers 17.1 to 17.10) and `20261110_Stage-C-Brief.md` ("What each chapter holds", 17).

Status: in progress. This file is written early and grows as the work lands.

## Read first

My role file and the accessibility lead's, `CLAUDE.md`, the round 1 brief, the stage C brief, Master Brief sections 3, 10 and 17, the token architecture, `tokens.json` and `tokens.css` (version 6.0.0-gate2.7: the nine motion tokens, the state tokens, the two themes and the reduced motion block), the interaction inventory (section 3, gaps G-1 to G-9, faults F-1 to F-16, and its routine calls, now D2-1146 to D2-1167), the engineer's round 0 notes (contracts, the planned reduced motion check), the research notes (section 1 for WCAG's words, section 3 for browser support), chapter 02's writing rules, chapter 11's file, generator and `s-11-14-correct`, chapter 05's Rule 05.4, the decision log entries D2-200, D2-859, DR-199 and D2-1129 to D2-1267, and our fifth edition's motion chapter as the Phase 0 text census, UX audit and editor audit record it. The fifth edition's page itself is not in this container (only `source/brand-mockups` and `source/icon-studies` are), so its motion chapter comes to me as the census's 50-character samples and the audits' quotations: "Things slide, draw and land.", the lever reveal's timeline (0 ms lines draw from the top left, 200 ms lines complete, 320 ms eight nodes appear together, 440 ms the lever lands at 1.4x, 560 ms it settles at 1.25x), "OATH and ACTION settle into place and the ampersand lands", the token table, the three easings, the reduced motion block and the "Never" list.

## What I built

- **The generator** `work/build/scripts/phase-2/stage_c_ch17_build.py` writes the chapter, its 24 specimens, `manifest-motion.json` and a figures record. `--check` builds in memory and writes nothing. It reuses `stage_a_systems_build.Ctx` for the specimen checks (no heading or landmark, no dash, no literal color, no px font size, `sx-` class prefix), as chapter 11's generator does, and reads tokens only.
- **The chapter** `work/build/guide/chapters/17-motion-and-states.json`: 12 rules in three groups. Rules 17.1 to 17.10 keep the brief's numbers and subjects. Two rules follow where a state needs its own: **17.11 Disabled** ("Keep an unavailable action in reach and say what makes it available") and **17.12 Empty** ("Say what is missing and what to do next when a region is empty"). Muted, warning, error and success stay on the plate of Rule 17.8, since Rules 11.12, 11.15 and 05.3 already govern their marks and red.
- **24 specimens** `work/build/guide/specimens/s-17-*.html`, each rule with a correct and a failure plate:
  - Three live motion players: `s-17-1-correct` (an Illustrative bill, S.99002, moves from step 3 to step 4: step 3 lands as done, then the ring slides to step 4 and draws the line behind it), `s-17-4-correct` (loop R1's first link from our systems atlas draws, then its arrowhead and second node land, with a "Preview reduced motion" check box), `s-17-5-correct` (slide, draw and land, each on its own). Every player has one Play and Pause button, Reset (unavailable at the first frame with its reason), Slow motion at one tenth speed, a polite status line, and a still view with the first and last frames at true size, their times and words, and the timeline in words.
  - `s-17-3-correct`: the player's seven parts, numbered, drawn as a picture with no controls.
  - `s-17-2-correct`: the nine tokens, six durations as bars on one scale (calc of value over 680 ms, so the scale holds at every width) and the three easings drawn as their curves.
  - `s-17-8-correct`: **the canonical ten-states plate.** Each state in a `data-oa-theme="light"` cell and a `data-oa-theme="dark"` cell, with its cue in words; every color is a role name the theme points at Newsprint or Charcoal. Readable (role group), so its words reach a screen reader.
  - `s-17-7`, `s-17-9` to `s-17-12` correct: loading, hover and focus, pressed and current, disabled, empty, each on both surfaces the same way.
  - Failure plates: motion failures are still frames, never animated (a count that ticks up on load, an autoplaying loop with a bare icon, a script's own 400 ms under reduced motion, a bouncing land, the fifth edition's loading pulse); state failures are drawn plainly (literal timing with an overshooting curve, four states by color alone, a focus ring with no gap on Charcoal and an inset-shadow hover, three pressed looks, a faded disabled button, "No results.").
  - `s-17-6-pending` and `s-17-6-pending-failure`: the pending markers for Rule 17.6 (below).
- **Figures** `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch17-Figures.json`: every ratio and motion value the chapter prints, each with its method, computed from `tokens.json`.

## Rule 17.6: what it needs from the identity designer

The rule's frame is written: the hinge over 680 ms (OATH and ACTION settle, then the ampersand lands), the lever over 560 ms in the lockmark (links draw, nodes land together, the lever lands last), each built from slide, draw and land, played on request, ending on the approved master for its size pixel for pixel, signature red in every frame and never the view's working red. The identity designer owns the motion, its specimens and the draft words.

**What to deliver**, through the identity designer's own generator, into `manifest-identity.json`:

1. `s-17-hinge-correct`: the hinge, live. My generator places it as Rule 17.6's correct plate.
2. `s-17-lever-correct`: the lever landing, live. Placed as an extra plate after Rule 17.6.
3. `s-17-hinge-failure` or `s-17-lever-failure`: one failure (my suggestion: a last frame a pixel off its master, beside the master at the same size, in still frames). Placed as the rule's failure plate. Any further `s-17-hinge-*` or `s-17-lever-*` entry is placed as another extra after 17.6, in name order.
4. In each manifest entry: `alt`, `notes`, and a `"caption"` (and for an extra, a `"label"`); my generator copies the caption into the chapter, so the words are the identity designer's. If the hinge or lever needs a different rule text than my frame, send it through the main session and I change it in my generator.
5. **The player contract**, as my three players follow it: the player's root carries `data-oa-motion` and `data-frame="start"`; one button carries Play and Pause (`data-oa-play data-oa-pause`), changing its icon and word together (Play, Pause, Play again); Reset carries `data-oa-reset`, is `aria-disabled` at the first frame and points `aria-describedby` at a reason line; nothing moves before a press and nothing loops; durations and easings are read from `--oa-motion-duration-hinge` and `--oa-motion-duration-lever` (and the other tokens) with `getComputedStyle` at the moment of the press, so under reduced motion they are 0 and Play draws the master at once; a still view shows the first and last frames at true size with their times and words. The identity designer may copy my player script (`PLAYER_JS` and `player()` in my generator): it reads a JSON list of tracks (`part`, `frames`, `dur`, `ease`, `at`) and works on any drawing whose moving parts carry `data-part`.
6. **Weight**: chapter 17 weighs 0.31 MB of its 0.5 MB budget with my specimens, so the hinge and lever specimens together have about 0.19 MB. A master inlined with `<img data-inline>` once per frame adds up quickly; draw each frame from one inlined master with `<use>`.
7. **Rerun** `python3 -I work/build/scripts/phase-2/stage_c_ch17_build.py` after the identity designer's files land (or ask the main session to). The pending markers then leave my manifest and the identity specimens take their slots. Until then the build stays clean: the markers are ordinary specimens with a dashed edge that say "Coming later."

## Routine calls

- D2-xxx | Rules 17.11 (disabled) and 17.12 (empty) follow the brief's ten; muted, warning, error and success stay on Rule 17.8's plate | The brief allows rules after 17.10 only where a state needs its own; disabled and empty each carry behavior beyond their look (focus kept, the reason in the description; the count and the advice in one status line), and the other four are already governed by Rules 11.12, 11.15 and 05.3
- D2-xxx | A land starts at 112 percent of the mark's size and settles to true size over the standard duration with the enter easing | Our fifth edition's lever landed at 1.4 times a node and settled at 1.25; 1.4 / 1.25 = 1.12, so every land keeps that proportion; no new token, since the factor is a proportion in the rule and the timing stays on the nine tokens
- D2-xxx | A draw takes the standard duration with the enter easing on its own, and the slide's duration and easing when it is drawn behind a slide | The fifth edition's lines drew in 200 ms; a line drawn behind a moving ring has to keep pace with it
- D2-xxx | No motion uses opacity, and nothing overshoots | The token architecture gives opacity no state job, and the fifth edition's "Never" list leaves out bounce and elastic easing
- D2-xxx | One button carries Play and Pause, so it carries both `data-oa-play` and `data-oa-pause` | The utility icons' rule (U-play, U-pause) and the stepper (`s-11-14-correct`) set one button whose icon and word change together; the engineer's planned check names three controls, and this keeps the attributes on the controls a reader has
- D2-xxx | Every player has Slow motion, a check box at one tenth speed, unavailable under reduced motion with its reason | Our motions last 120 to 680 ms, so Pause can never be pressed in time at true speed; at one tenth speed it can, and a reader can see the easing
- D2-xxx | The guide's players start at the first frame, and Play draws the last frame at once whenever every duration token reads 0 | Rule 17.4; tokens.css already resolves the six durations to 0 ms under reduced motion
- D2-xxx | Motion runs through the Web Animations API, timed from the tokens read at the press; the frames at rest are drawn by CSS from `data-frame` | No `@keyframes` inside the build's `@scope`; the last frame is the drawing's own state, so nothing lingers as a filled animation
- D2-xxx | Failure cases of motion are shown as still frames, never animated | The guide never plays a motion it forbids, and the guide check fails any animation that repeats
- D2-xxx | Rule 17.4's player carries a "Preview reduced motion" check box that sets the player's own duration tokens to 0 ms; when the device asks for reduced motion it is checked and unavailable, with its reason | A reader without the setting can see what a reader with it sees, and the preview runs the same token path as the media query
- D2-xxx | Loading draws the lines the data will sit on, with no marks on them, in the loading mark token: for a tracker, its line alone | D2-200 for the lockmark ("links alone"), applied to any region: a ring or node would read as a state the data has not reached
- D2-xxx | The ten-states plate (`s-17-8-correct`) is readable, a named group, so a screen reader reaches every sample's words | It is a reference that builders and auditors read, and its samples are words
- D2-xxx | On Charcoal an error takes no band; the 4 px Pillar Red bar (4.49 to 1) and the mark and "Error:" in Newsprint carry it | Confirms D2-1160, as the inventory asked chapter 17's maker to
- D2-xxx | Hover on a quiet control thickens its edge from 1 to 2 px and takes the pixel from its padding | Rule 17.9: hover never moves layout
- D2-xxx | Check boxes in the players take `accent-color` from the essential graphic role | A browser's own blue sits outside the palette; Charcoal on Newsprint measures 13.29 to 1
- D2-xxx | Each specimen's styles are pruned to the rules its markup uses | Shared style sets cost a specimen only what it draws, which keeps 0.19 MB of the chapter's budget for Rule 17.6
- D2-xxx | The bill in the players is chapter 11's Illustrative S.99002, School bus contracts, moving from step 3 to step 4 | Chapter 11 shows S.99002 at step 4, so the two chapters agree, and DR-151's numbering stands

## Questions for Dustin

None this round. Every call above sits inside the approved stage C plan and the round 1 brief.

## Tested

## Not tested

## For other owners

## Change log
