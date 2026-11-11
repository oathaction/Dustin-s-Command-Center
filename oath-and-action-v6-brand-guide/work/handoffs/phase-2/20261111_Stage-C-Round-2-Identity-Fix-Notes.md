# Stage C, round 2: identity designer's fix notes, Rule 12.4

Oath & Action Edition 06, Phase 2, stage C, round 2, November 11, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under DR-216 and D2-1534 and the main session's task message. I read `CLAUDE.md`, my role file, the creative director's review of Rule 12.4 and its instruction to me, section 2 of my round 1 notes, D2-1405 to D2-1409, DR-216, and chapter 02's writing rules.

This pass wires the rewrite into chapter 12 and does nothing else. I did not touch chapter 03, chapter 08 or any other rule. DR-217's Rule 03.2 sentence and the review findings wait for the fix pass. I changed one script, my own generator, and the chain wrote chapter 12's outputs from it. I wrote no output by hand, committed nothing and pushed nothing.

**To rebuild:** `python3 -I work/build/scripts/phase-2/promotion_identity.py specimens` from the project folder, with `TMPDIR` set to a scratch folder.

## What changed

All in `work/build/scripts/phase-2/stage_b_identity_ch12.py`:

- **Rule 12.4 is the rewrite.** It keeps its number. Its title, rule text and Never row are the creative director's words as Dustin approved them: "Leave an open area plain, or sign it with the large crop of B or a watermark." The why, the other specification rows and the builders line are my round 1 draft (D2-1408), with four fixes listed under Routine calls. The basis is "Design judgment, approved by our founder and editor in November 2026".
- **Its plates are the ones board C showed.** The correct plate is the Report 3 cover at 360 px signed with the large crop of B, 232 px tall (D2-1406). The failure plate is the same cover with the retired arcs under the failure band, with the caption set under D2-1407: "Nothing on this cover says Oath & Action, and the arcs take the corner the crop of B would sign." Both covers carry the Illustrative label. Each plate's HTML is byte for byte the variant I built in round 1, so round 1's measures of the crop still apply.
- **The follow-on changes, as the creative director listed them:**
  - The "Hinge arcs" row is gone from `s-12-index`, which now lists 13 devices.
  - The intro now ends its first sentence with "the rule for open areas" in place of "a pattern drawn from the hinge". That sentence is mine (`INTRO_ADD`), so the systems designer's `stage_b_ch12_systems_build.py` needs no change. The old wording joins `OLD_INTRO_ADDS`, so the shared file swaps it in place.
  - Rule 12.2's Never row now reads "Behind words, a figure or a control; in red; beside a hinge headline or a crop of B".
  - `hinge_arcs()`, `coverage()` and its 5.5 percent figure are gone, along with the imports only they used.
- **The round 1 variant is retired.** `REWRITE_12_4` and `rewrite_plates()` are gone, since the rule now lives in `_rules()`. `crop_b()` and `cover_signed()` keep their names.

**The token table's hairline rows.** Chapter 12's table of tokens is built from the chapter file. Its hairline rows now cite Rule 12.1 alone, because the rewrite names no token. Each row still holds its token name, value and rule link. Chapter 26's token table reads only `tokens.json`, and its hairline descriptions ("Dividers and table rules with no meaning of their own." and "Dividers, keylines and chart axes.") never named the arcs. The engineer needs to change nothing.

**For the main session:**
- Nothing is needed from the systems designer: the intro sentence and the index are mine.
- My round 1 script, `stage_c_identity_round1.py rule-12-4`, should not be rerun. Its measure still works, but it rewrites key `rule_12_4` in round 1's figures file and then stops with an error in `comparison()`, which reads `REWRITE_12_4`. Round 1's committed comparison page and captures stay as board C's record.
- Chapter 12 is outside the round 2 reviewers' frozen copy, so their page does not show this change.

## Routine calls

- D2-xxx | Rule 12.4 takes the rewrite's own title. Chapter 12 keeps its title, "Graphic devices and patterns" | I read DR-216's "number and title" with the creative director's routine call, which keeps Rule 12.4's number and chapter 12's title. The old rule title named the arcs that DR-216 retires
- D2-xxx | Rule 12.4's plates keep the ids `s-12-pattern-correct` and `s-12-pattern-failure` | Board C's list of changes named these ids. The identity build removes stale files only under its own prefixes, so a new id would leave the old files with nothing to remove them. No reader sees an id
- D2-xxx | The failure plate draws the retired arcs with a private helper, `retired_arcs()`. `hinge_arcs()`, `coverage()` and the 5.5 percent figure leave the generator | The review asks for `hinge_arcs` and its coverage figure to go, and its failure plate is the cover with today's arcs. The helper draws the same 12 arcs, byte for byte, and nothing in the guide sets them as a device
- D2-xxx | The basis reads "Design judgment, approved by our founder and editor in November 2026" where the review wrote "approved on board C" | A reader does not know what board C is (H02). The guide's other approved rules use this wording
- D2-xxx | Four fixes to my drafted why (D2-1408): "a view carries one ampersand moment (Rule 04.2)" for "B appears once in a view"; "the numbered steps that follow a bill (Rule 11.1)" for "chapter 11's tracker"; "looks like a stock report template" for "belongs to no one, so a cover that carries one reads as anyone's report"; "the ampersand from our wordmark" for "the mark a reader already knows as ours" | Rule 04.2 counts moments, and the wordmark's own B does not count. The tracker had no explanation at first use. "No one" against "anyone's" is a matched pair (W10). No reader test backs a claim about what readers know (W20, DR-202). The editor reads all four in the fix pass
- D2-xxx | Rule 12.4 names no token, lists B's display master as its file, and relates to chapters 04 and 24 | The rule sends builders to Rules 04.8 and 12.2 for every measure and color. Chapter 12's list of related chapters stays as it was
- D2-xxx | The correct plate's notes read the crop's measures from round 1's figures file (key `rule_12_4`), and the build stops if the height chosen there is not `CROP_B_H` | The figures have one source, and the build stops if the plate differs from the one that was measured
- D2-xxx | The correct plate's alt describes the cut by the two edges that make it, not by the parts of B | A reader can check that against the plate
- D2-xxx | `crop_b()` and `cover_signed()` keep their names | My round 1 measure calls them, so `CROP_B_H` can be checked again

## Tested

- Before the refactor, I saved round 1's variant plates (`rewrite_plates()`). After it, the new correct plate's cover and the failure plate's body matched them byte for byte.
- I ran the generator chain on the unchanged tree first, each script with `python3 -I`: `apply_systems_ch11.py`, `stage_b_ch10_build.py --no-draw`, `stage_b_ch12_systems_build.py`, `promotion_identity.py specimens`, `guide_editor_build.py`, `stage_b_identity_ch01.py`. All exited 0 and changed no file.
- I ran the same chain twice after my changes, and every script exited 0 both times. `git status` showed my generator and five chapter 12 outputs: `12-graphic-devices.json`, `manifest-identity.json`, `s-12-index.html`, `s-12-pattern-correct.html` and `s-12-pattern-failure.html`. Two other entries appeared during the run, `20261111_CD-Review-Of-Stage-C-Chapters.md` and `stage-c-round-2/production-test/`. Those are the reviewers' files, and no generator in the chain writes them.
- I diffed the manifest by script. Only `s-12-pattern-correct` and `s-12-pattern-failure` changed, in their alt and notes. No entry was added or removed.
- `guide_build.py --strict --out` into my scratch folder: 0 warnings, 16 chapter files, 185 rules, 420 specimens, 9,543,666 bytes.
- Scans of the built page by script:
  - The words "hinge arcs" appear nowhere, and the page holds no em dash or en dash.
  - Rule 12.4's cross-references link to Rules 04.8, 12.2, 04.2, 08.3 and 11.1.
  - Chapter 12's hairline token rows cite Rule 12.1 only.
  - My generator and the chapter file hold no em or en dash.
- Captures in Chromium at 1440 and 360 px, at 1x and 2x: the whole rule, each plate and the device index. At 360 px the page scrolls 0 px sideways and each plate's frame scrolls 0 px. The correct plate measures 360 by 466 px, and the failure plate 360 by 496 px with its band.
- I looked at both plates at all four settings, the whole rule at 1440 px 1x and 360 px 2x, and the index at 1440 px 1x. The crop reads as one letter, clear of the words. Each cover shows its Illustrative label, and the failure band runs the plate's width. In the whole-rule captures the sticky masthead covers a strip of the page. The capture tool causes that, and the plate captures show what it hides.

## Not tested

- I did not run `guide_check.js` on the new page.
- I did not use Firefox, Safari, a real phone, 1.25x or 1.5x screens, forced colors, print or a screen reader.
- I did not measure the crop again. The plates are byte for byte the ones round 1 measured, so D2-1406's figures stand, but this pass did not render them anew.
- The 200 percent text case on the signed cover. The plate is a fixed 360 px artboard. On a live cover, words that reflow can come closer to B than Rule 04.8 allows.
- The editor has not read the why, the specification rows other than Never, or the builders line. The creative director has not seen the rule as wired.
- **Seen, not changed:** at 1440 px the device index's row "Marks the turn from how a decision is made to what a reader can do" leaves "do" alone on its second line. It was there before this pass and belongs to Rule 12.1's extra, so it waits for the fix pass.

## Change log

Created:
- `work/handoffs/phase-2/20261111_Stage-C-Round-2-Identity-Fix-Notes.md` (this file)

Modified, script:
- `work/build/scripts/phase-2/stage_b_identity_ch12.py`

Modified, written by that script through the identity build:
- `work/build/guide/chapters/12-graphic-devices.json`
- `work/build/guide/specimens/manifest-identity.json`
- `work/build/guide/specimens/s-12-index.html`
- `work/build/guide/specimens/s-12-pattern-correct.html`
- `work/build/guide/specimens/s-12-pattern-failure.html`

Outside the repository: the scratch build `guide.html` and its report, chain and build logs, copies of the files as they stood before, the saved variant plates, `cap/cap.js` and 16 captures, and the build's temporary renders, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2/identity/`.
