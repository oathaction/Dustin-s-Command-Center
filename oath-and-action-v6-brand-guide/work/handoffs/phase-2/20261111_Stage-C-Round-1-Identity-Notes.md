# Stage C, round 1: identity designer's notes

Oath & Action Edition 06, Phase 2, stage C, round 1, November 11, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261111_Stage-C-Round-1-Brief.md` and the main session's task message after promotion C. I read the round 1 brief, the chapter 17 maker's notes, figures and draft chapter file, its generator's contract for Rule 17.6 (`stage_c_ch17_build.py`, module docstring and `identity_slots`), the engineer's motion contract (round 0 notes, "Checks planned for round 1", item 2), our fifth edition's motion chapter as the Phase 0 text census records it, the creative director's review of Rule 12.4, the editor's round 1 notes (sections 1c and 2), and D2-1313 to D2-1345.

I changed no identity master, board, ledger, `source/` or shell file, and no file another owner keeps. I wrote the committed chapters page at no point: every build went to my scratch folder with `--out`. The chain rewrote other owners' outputs with their own scripts (change log). I committed and pushed nothing; the main session's snapshot commits took in my files as I worked.

**To rebuild my part:** `python3 -I work/build/scripts/phase-2/promotion_identity.py specimens` (the identity build, which now writes Rule 17.6's three specimens last), then `stage_c_ch17_build.py` (the chapter 17 maker's, which places them), then `stage_c_identity_round1.py ch17 <built page> <scratch>` for the checks and `stage_c_identity_round1.py rule-12-4 <scratch>` for the board C page. Set `TMPDIR` to a scratch folder: the identity build renders a few PNGs through temporary files.

## Tasks

1. Rule 17.6's specimens, the hinge and the lever, live, through my own generator, in `manifest-identity.json`. Done; chapter 17 places them.
2. Rule 12.4's rewrite for board C, beside the current rule, with comparison plates in `work/handoffs/phase-2/stage-c-identity/`. Done; chapter 12 is unchanged.
3. Rule 03.2's sentence from D2-1329. Done, then replaced by the editor's fuller wording (below).
4. The editor's rows for my chapters. Done.

## 1. Rule 17.6, the hinge and the lever

**What I built.** `stage_c_identity_ch17.py`, registered last in the identity build, writes three specimens into `manifest-identity.json` with chapter "17" and rule "17.6", each with the caption chapter 17's generator reads:

| Specimen | Slot in Rule 17.6 | What it is |
|---|---|---|
| `s-17-hinge-correct` | Correct plate | The hinge, live, on Newsprint and on Charcoal: the wordmark's 24 px master at 24 px, and where the panel is at least 41rem wide, its display master at 64 px tall as well |
| `s-17-hinge-failure` | Failure plate | Last frames half a pixel off their masters, for the hinge and the lever alike, at true size and enlarged six times from a 1x screen |
| `s-17-lever-correct` | Extra after the rule, labeled "The lockmark’s motion" | The lever landing, live, on Newsprint and on Charcoal: the 48 px master at 48 px and the display master at 120 px |

**The motions, from tokens.json** (the script reads each token again at the moment of a press):

| Motion | Steps | Comes to rest |
|---|---|---|
| Hinge | OATH and ACTION slide toward each other over the slow 320 ms with the standard easing, 12 px each at 24 px and 32 px each at 64 px; the gap holds; B lands from 112 percent to its true size over the standard 200 ms with the enter easing, starting at 480 ms | 680 ms, the hinge token: B starts at hinge minus standard |
| Lever | The six links draw from the top left over 200 ms with the enter easing; one stagger later, at 240 ms, the eight nodes land together from 112 percent; the lever lands last, from 360 ms | 560 ms, the lever token: the lever starts at lever minus standard |

Both build from Rule 17.5's slide, draw and land; 112 percent is chapter 17's land, read from its figures file. The generator asserts that each motion comes to rest exactly at its own token.

**How each player lands on its master.** Each size of each mark holds two layers in one place. The moving layer is the master's own elements, inlined and named for the script: the wordmark's one letter path split by position into OATH (six subpaths) and ACTION (eight), each subpath's bytes unchanged, and B's path as the file draws it; the lockmark's six links, eight nodes and lever as the file draws them. The end layer is the master placed by reference, which the guide build inlines unchanged. Play runs the moving layer; at its end the player shows the end layer, so the last frame is the master file itself. Reset returns to the first frame. Under reduced motion every duration token is 0 ms and Play shows the end layer at once.

**The player** follows the engineer's contract (`data-oa-motion` on the root, `data-oa-play` and `data-oa-pause` on one button, `data-oa-reset`) and chapter 17's player in its parts and words: one Play and Pause button that reads Play, Pause and Play again, Reset unavailable at the first frame with its reason, Slow motion at one tenth speed (unavailable under reduced motion, with its reason), a polite status line, and a still view with three frames at true size and every step with its time. The script is chapter 17's, with two additions: a step may start at a token minus another (a mark that comes to rest at its motion's own duration), and a part names every element that carries it, so both grounds and both sizes play on one press.

**Figures** (`work/handoffs/phase-2/20261111_Stage-C-Round-1-Identity-Figures.json`, key `ch17`; Chromium, the strict build without chapter 18's files, at 1440 and 390 px, 1x and 2x, with and without reduced motion):

- On load, every player stands at its first frame with no animation running.
- Play runs once, ends on the end frame at 680 ms and 560 ms, and the button reads Play again; Reset returns to the first frame, the same pixels in 54 of 56 checks. The other two, the 24 px hinge at 1440 px, 1x, under reduced motion, differ in 2 pixels by at most 5 levels on the edge of OATH's O, a raster difference after the page scrolled.
- Under reduced motion, Play draws the end frame at once with no animation, the five motion tokens read 0 ms, and Slow motion is unavailable with its reason.
- Every end-layer drawing in the page, 4 per player in every run, is its master file's drawing, element for element, its title aside.
- The 48 px lockmark's end frame holds exactly 4 colors on Newsprint (Charcoal, Stone, Newsprint, the red) and 3 on Charcoal: it sits on whole pixels.
- The moving layer at rest, with no animation applied, against the master, at 1440 px: the lockmark at both sizes, identical at 1x and 2x; the wordmark, 91 to 149 edge pixels differ by at most 7 levels, except the 64 px wordmark at 2x, which is identical. Two paths for OATH and ACTION shade a few edge pixels differently from one.
- The moving layer's last keyframe against the end frame: the 48 px lockmark identical everywhere; the 24 px wordmark up to 9 levels on 151 edge pixels at 1440 px, 1x, and up to 86 levels on 160 to 395 edge pixels at the other three settings; the 64 px wordmark and the 120 px lockmark up to 60 to 92 levels on edge pixels. Chromium draws an element it has just animated a little differently. This is why the player shows the master itself at the end; the moving layer's last keyframe shows for one frame at most before it.

**Looks.** Each plate at 1440 and 390 px, at 1x and 2x, and frames from the run. Three looks led to changes. The lever's first frame was an empty field, which read as a broken plate, so a dashed square now marks where each lockmark will stand, in the first frame only. The extra's label repeated the player's title, so the label reads "The lockmark’s motion" and the kickers give the durations. The first failure moved the marks with padding, which Chromium snaps back onto whole pixels, so the fault never showed; it now moves them with a transform, and the half-pixel lockmark's links turn into gray bands (9 colors against the master's 4). At 390 px the failure plate first fell back to a sideways frame; its pairs now wrap.

## For the chapter 17 maker

Your rule text, why and plates read right with my specimens, and row 54 is in. Draft words I suggest, for your generator and the editor:

- **Specification "Hinge":** "680 ms in all, on request: OATH and ACTION slide toward each other over the slow 320 ms, and the ampersand lands from 480 ms and comes to rest at 680 ms"
- **Specification "Lever":** "560 ms in all, on request: the links draw over 200 ms, the nodes land together from 240 ms, and the lever lands from 360 ms and comes to rest at 560 ms"
- **Builders, a sentence after the first:** "When the motion ends, show the master file itself, placed as Rules 03.1 and 08.1 place it, so the last frame is the master and not the moving copy. Check the last frame on a 1x screen, since a 2x screen hides a mark that rests half a pixel off the grid."

The figures above back each sentence; the numbers are tokens.json's.

## 2. Rule 12.4's rewrite, for board C

**What I built.** The creative director's rewrite as a variant beside the current rule in `stage_b_identity_ch12.py`: `REWRITE_12_4` (the rule as the creative director drafted it, with a why, specifications and builders text I drafted from the review's reasons, for the editor), `cover_signed` and `rewrite_plates`. None of these is a specimen, so chapter 12 and its plates are unchanged: after the chain, `12-graphic-devices.json` and every `s-12-*` file match HEAD. `stage_c_identity_round1.py rule-12-4` measures the crop and writes the comparison page.

**The plates**, as the review instructs: the correct plate is the Report 3 cover at 360 px signed with the large crop of B; the failure plate is the same cover with today's arcs under the failure band. Both covers are invented and carry the Illustrative label.

**The crop, measured** (key `rule_12_4`): B's display master in the cover's ink, at Rule 04.8's proportions as its own plate sets them, 35.5 percent of B's width past the right edge and 6.8 percent of its height past the foot. I measured every height from 180 to 320 px in 4 px steps on a 1x render. B stands 232 px tall: 30.1 percent of its ink falls outside the cover, within Rule 04.8's 25 to 40 percent; what stays inside is one piece at that place and at every offset within 4 px; and its ink stands 31.1 px from the words, over the body text's 27.2 px line height. At 236 px the clearance falls to 27.5 px, 0.3 px over the line, so I chose the largest height with 2 px to spare.

**The page:** `work/handoffs/phase-2/stage-c-identity/20261111_Rule-12-4-Comparison.html`, with `-1x.png` and `-2x.png` full-page captures. Today's rule at left as the guide prints it, the rewrite at right; each with its words, both plates at true size with a keyline, and its specifications; then the crop's figures and the follow-on changes if Dustin chooses the rewrite (the index row, the intro's words, Rule 12.2's Never row, and the generator's arcs).

## 3. Rule 03.2 and the editor's rows

I first added D2-1329's sentence. The editor's row for the same four sentences then replaced it with a fuller version, which names "the masters drawn on the pixel grid" and states the 40 px line both ways, so the page prints the editor's words.

From `20261111_Stage-C-Round-1-Editor-Notes.md`, as the main session asked, each through my generators and word for word as the editor wrote it:

- Section 1c, all ten rows. In `stage_b_identity_ch09.py`: Rule 09.1's "48 px row" now says where the row breaks two and two (D2-1179's gap); `s-09-opener`'s alt gains the same sentence before its last; Rule 09.3's builders line prints the two CSS lines that switch a fit for its master (D2-1343). In `stage_a_identity_chapters.py`: Rule 03.2's last four builders sentences; Rule 03.4's fourth builders sentence; Rule 08.1's third sentence, now three; Rule 08.1's display master row, "except"; Rule 08.2's "Sign-off" row, "every link"; Rule 08.2's "Feed test, dark card", its third and fourth sentences with "because" and the rounding to a multiple of 5; Rule 08.2's "Feed test, our card", which now names Newsprint, says each figure's unit and prints Prussian's equal figures once.
- Section 2, row 55: both Rule 17.6 captions now read "Live. Press Play, and ...".
- Section 2, row 54 changes the chapter 17 maker's `rule[1]`; their generator applied it. Row 16 needed nothing from me.
- Section 2, the Reset reason row (after the main session's note): both Rule 17.6 players now read "Reset works once you press Play.", chapter 17's `WHY_START`, in place of "At the first frame, so Reset waits until you press Play." Rebuilt with `--out` into my scratch folder (strict build without chapter 18's files, 0 warnings); `stage_c_identity_round1.py ch17` passes all 16 runs at 1440 and 390 px, and the line shows in both players at both widths, word for word as in `s-17-1-correct`.

## Routine calls

- D2-xxx | Rule 17.6's specimens come from a new generator, `stage_c_identity_ch17.py`, run last in the identity build, with "s-17-hinge-" and "s-17-lever-" as its exact prefixes | Run last, its inlined masters cannot renumber the ids in the proofs; the exact prefixes keep the build from ever touching the chapter 17 maker's `s-17-*` files
- D2-xxx | The hinge's B starts at hinge minus standard, 480 ms, so it comes to rest at the hinge token; the gap holds 160 ms after the slide | The token sets the motion's length (V5: 680 ms in all), and a beat of stillness before B lands lets the eye see the place it fills
- D2-xxx | The lever's links draw from 0, its nodes land at standard plus stagger, 240 ms, and the lever lands from lever minus standard, 360 ms, coming to rest at the lever token | V5's order (lines, then nodes together, the lever last) in Rule 17.5's behaviors, ending on the token
- D2-xxx | Each player shows the master file itself at the end, placed by reference beside the moving layer | The last frame is then the master by construction; the moving layer's last keyframe differs from it by up to 92 levels on edge pixels of the display drawings, as Chromium draws an element it has just animated
- D2-xxx | The wordmark's letter path is split by position into OATH and ACTION for the moving layer, each subpath's bytes unchanged | The two words must move apart; the file draws them as one path
- D2-xxx | The hinge plays the 24 px master at 24 px on every screen, and the display master at 64 px tall only where the panel is at least 41rem wide | A phone column cannot hold the 64 px wordmark, and the display master may not stand under 40 px tall (Rule 03.4)
- D2-xxx | The lever plays the 48 px master at 48 px and the display master at 120 px | Rule 08.1's ranges: 96 px belongs to a social card's sign-off
- D2-xxx | The first frame's slides are whole pixels on screen, 12 px at 24 px and 32 px at 64 px | The first frame of the 24 px master then lands on the pixel grid too
- D2-xxx | The lever's first frame shows a dashed square where each lockmark will stand, in the first frame only, and the words say it is no part of the mark | An empty first frame read as a broken plate
- D2-xxx | One player per motion shows both grounds, Newsprint and Charcoal, playing together on one press | The brief asks for both; one press keeps one status line and one still view
- D2-xxx | The still view shows three frames, from the 24 px and 48 px masters only, and lists every step with its time | It fits a phone column and gives every fact the motion shows (Rule 17.3)
- D2-xxx | The failure plate shows both marks half a pixel low, moved with a transform, and enlarges Chromium's 1x renders six times | Chromium snaps an svg's box to whole pixels but not a transform, so padding hid the fault; a 2x screen hides it too
- D2-xxx | The players' kickers give the durations, and the extra's label reads "The lockmark’s motion" | The label repeated the player's title
- D2-xxx | The specimens take Rule 17.6's slots as chapter 17's contract names them: the hinge's correct and failure plates, the lever as the extra | The generator's docstring sets the names and their order
- D2-xxx | Rule 12.4's rewrite sits in `stage_b_identity_ch12.py` as unregistered functions and words | The creative director's instruction places it there, and chapter 12 must not change until Dustin chooses
- D2-xxx | The crop of B on the 360 px cover stands 232 px tall: the largest height, in 4 px steps, that keeps Rule 04.8's three measures with 2 px to spare | At 236 px the clearance is 0.3 px over the line height, which type rendered a little differently could break
- D2-xxx | The rewrite's failure caption reads "Nothing on this cover says Oath & Action, and the arcs take the corner the crop of B would sign." where the review wrote "With the wordmark covered, nothing here says Oath & Action, ..." | The plate's cover carries no wordmark to cover
- D2-xxx | I drafted the rewrite's why, specifications and builders text from the review's reasons, marked for the editor | The review gives the rule and its Never row; a rule in the guide's form needs the rest
- D2-xxx | The comparison page draws a keyline around each cover and reads the shell's Illustrative style from its stylesheet | On the Newsprint page the cover's edge, and so the crop, could not be seen; the label printed as plain text
- D2-xxx | My scratch builds use copies of the chapters and specimens, with chapter 18's files left out for the strict build | Chapter 18's 24 anatomy plates are still being drawn, so a strict build of the whole guide stops on them; the copy shows that nothing else warns
- D2-xxx | I set `TMPDIR` to the scratchpad for every run | The identity build renders PNGs through temporary files, which would otherwise land in `/tmp`

## Questions for Dustin

1. **Rule 12.4, for board C.** Retire the hinge arcs and rewrite Rule 12.4 as the rule for open areas: leave them plain, or sign them with the large crop of B or a watermark? *Recommendation:* the creative director's, retire them. The comparison page shows why at true size: with the arcs, nothing on the cover says Oath & Action, and the crop of B signs the same corner as ours. The cost: it changes Gate 1's Y6 and the brief's list of restrained patterns, and covers without photographs lean on type and the crop.

## Tested

- The identity build before and after: it adds the three Rule 17.6 specimens and their manifest entries, and changes chapters 03, 08 and 09 only by the editor's rows; chapter 12 and every `s-12-*` file match HEAD after the chain.
- The chapter 17 maker's generator in its check mode, then their written chapter: all three specimens placed, with my captions.
- `stage_c_identity_round1.py ch17` on the strict page: the figures in section 1, 16 player runs (two players, two widths, two densities, with and without reduced motion).
- The end layers against the master files, element for element; the 48 px lockmark's end frame colors; the moving layer at rest and at its last keyframe against the end frame.
- The failure's renders: 9 colors in the half-pixel lockmark against 4 in the master; 206 against 219 in the wordmark's crop.
- The crop of B at 36 heights, and at 9 offsets for the height chosen.
- The generator chain from the project folder, each script exit 0 on its last run; `guide_build.py --strict --out` into my scratch folder: the whole guide stops on 24 warnings, all chapter 18's missing anatomy plates; the copy without chapter 18's files passes with 0 warnings (14 chapter files, 152 rules, 354 specimens).
- Looks: Rule 17.6's three plates at 1440 and 390 px at 1x and 2x; frames from the run at 2x; the comparison page at 1x and 2x.
- A scan of every new word in the chapters, the manifest, the generators, the comparison page and these notes for em and en dashes: none.

## Not tested

- Firefox, Safari, real phones, 1.25x and 1.5x screens; the players in Chromium only.
- A screen reader by ear on the players; the status line is `role="status"` and the controls are buttons with their words.
- Slow motion pressed during a run (its checkbox and its reason were checked, not the rate in motion).
- The engineer's guide check (`guide_check.js`) on a page with Rule 17.6 in it; the engineer runs it on the page as it stands.
- The comparison page at phone width; board C shows it at 360 px per plate, which the page draws.
- The editor's read of the rewrite's why, specifications and builders text, and the creative director's look at the crop.

## Change log

Created:
- `work/build/scripts/phase-2/stage_c_identity_ch17.py`
- `work/build/scripts/phase-2/stage_c_identity_round1.py`
- `work/build/guide/specimens/s-17-hinge-correct.html`, `s-17-hinge-failure.html`, `s-17-lever-correct.html` (generated)
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Identity-Figures.json`
- `work/handoffs/phase-2/stage-c-identity/20261111_Rule-12-4-Comparison.html`, `-1x.png`, `-2x.png`
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Identity-Notes.md` (this file)

Modified, scripts:
- `work/build/scripts/phase-2/stage_a_identity_build.py`: runs `stage_c_identity_ch17` last and owns its two prefixes
- `work/build/scripts/phase-2/stage_b_identity_ch12.py`: Rule 12.4's rewrite as a variant (`CROP_B_H`, `crop_b`, `cover_signed`, `rewrite_plates`, `REWRITE_12_4`); `import re`
- `work/build/scripts/phase-2/stage_a_identity_chapters.py`: Rule 03.2's D2-1329 sentence, then the editor's rows for Rules 03.2, 03.4, 08.1 and 08.2
- `work/build/scripts/phase-2/stage_b_identity_ch09.py`: the editor's rows for Rule 09.1, `s-09-opener` and Rule 09.3

Modified, generated by those scripts:
- `work/build/guide/chapters/03-identity.json`, `08-lockmark.json`, `09-pillar-icons.json`
- `work/build/guide/specimens/manifest-identity.json`

Rewritten by the chain with other owners' scripts, not my changes: chapter 05 and 11 outputs, including `05-color.json`, `manifest-systems.json`, `s-05-4-correct.html` and several `s-11-*` files, from the systems designer's work in progress.

Scratch builds, captures and studies: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/identity/`.
