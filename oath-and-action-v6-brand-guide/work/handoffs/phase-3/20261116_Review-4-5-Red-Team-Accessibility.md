# Review of rounds 4 and 5: accessibility red team (AX)

Oath & Action Edition 06, Phase 3, chat 7, November 16, 2026. Reader: the UX and accessibility lead (`.claude/agents/oa-ux-accessibility-lead.md`) as reviewer, under the brief `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md`. The page read is a copy of the strict build of `9a6e1182` (`c07/main/guide.html`, 12,107,102 bytes) in `c07/review/accessibility/`. Started 16:34 UTC.

Status: in progress. Sections fill as the checks run.

## 1. Score

Pending.

## 2. Must fix

Pending.

## 3. Should fix

Draft findings from the markup, 16:49 UTC; each is confirmed or dropped in the browser before the report closes.

- **AX-S1 (draft). Rule 14.5's palette plate prints 16 of its 36 label ratios one hundredth high** (`s-14-palette-spec`, `palette_spec_build.py` line 274). D3-1929 says the plate rounds every ratio down. The ground ratios do (54 of 54 match the WCAG formula rounded down), but each "Label in ..." ratio is round 0's figure, already rounded half up, which `ratio()` then floors to no effect: "Label in Newsprint, 10.47 to 1" measures 10.468, "Label in Charcoal, 7.81 to 1" measures 7.808, "Label in Newsprint, 4.61 to 1" measures 4.606. None crosses 3 or 4.5, so no claim is false today, but the next token release could round a 4.496 up to "4.50 to 1, text". Fix: measure `contrast(r["label_hex"], r["fill_hex"])` in the generator, as the ground ratios are. Owner: engineer.
- **AX-S2 (draft). S95's second crop loses its size line on the page** (`kit.js` near line 1287, rule 14.141). Round 5's fix names the second crop by its size line ("Drawn at 1080 by 1080 px") and then sets that line `hidden`, the step meant for the alt paragraph. The first crop keeps "Drawn at 1080 by 1350 px" under it; the second shows none (capture `newsprint-1x/1440/s-14-s95.png`). The name still computes, since `aria-labelledby` reads hidden text. Fix: hide the label only when it is the alt paragraph. Owner: engineer.
- **AX-S3 (draft). The step tables and 15.22 describe their own words a second time.** A readable plate is a group described by its alt (AX-S2 of Gate 2), and four in this review's scope carry an alt that repeats the live words they describe: `s-15-22-correct` (4,276 characters, 56 percent of its five-word runs repeated from the plate's words), `s-11-ballot-steps` (1,509 against a 1,373-character table), `s-11-court-steps` (1,016 against 931), `s-11-steps` (932 against 883). Chromium hangs the whole description on the group, so a reader can hear every step with its law twice. Fix: an alt for a readable plate says what the plate is in one or two sentences ("A table of the six steps of a citizen initiative, with what happens at each and the law that sets it in the four states we read"). Owners: systems designer (15.22), tracker designer (the three step tables). Guide-wide the same pattern sits on 12 more readable plates outside this review (listed under Measured reach), which can wait for the pass that touches them.
- **AX-S4 (draft). The last question's skip link passes the rule index without saying so** (`s-14-selection-guide`, the 16th question). "Skip these 7 forms" lands on `#group-14-1`, past the rule index and local contents, 333 links in all, while the other 15 "Skip these N forms" land on the next question. The first skip link now says "Skip to Rule 14.1" and lands there, so D3-2086 is met for it. Fix: point the 16th at the rule index's label (`#data-visualization-index-t`), or word it "Skip these 7 forms and the rule index". Owner: selection guide maker.

## 4. The named places in this lens

Pending.

## 5. Measured reach

Measured first by script on the markup of the copy (`scripts/reach.py` in the scratch folder), then in Chromium where marked. Figures in this section are from the markup unless a line says "in Chromium".

**(a) The masthead covering a returned focus at 1024 to 1100 px (2.4.11 met, 2.4.12 not), shell-wide.** From the markup: six CSS rules read `--head-h` (the `scroll-margin-top` on `main, main *, .colophon *`; `.alias`; the rail's sticky top and height; `.cover`'s height; `.route-head`; the chapter's local contents). The page holds 2,663 ids in `main`, 3,748 in-page links (3,726 of them land in `main`), 2,233 links that leave a way back (`a.xref` or `a[data-oa-xref]`) and 147 places a way back returns to (`[data-return-label][id]`). Every one of those landings moves wherever the masthead's height and `--head-h` differ; nowhere else does anything move. Browser measures pending.

**(b) The words inside every `role="img"` stage.** From the markup: 735 plate stages, 416 of them `role="img"` and 319 `role="group"`. 413 of the 416 image stages hold HTML words, 5,008 runs of text in all, in 19 chapters (purpose 41, voice 51, identity 19, ampersand 18, color 15, type 18, layout 12, lockmark 7, pillar icons 10, symbols 15, icons 31, graphic devices 16, evidence 11, data visualization 15, systems graphics 25, motion and states 19, components 49, accessibility 15, tokens 22, outside a chapter 4). No image stage holds a focusable element, so `aria-hidden` on the fragment hides no control. No link, label or description points into an image stage's fragment from outside (the 10 `href`s that do are `<use>` references inside SVG). No CSS or script on the page selects a stage's child by `>`, and no stage is a flex or grid box, so a wrapper element moves no layout box (confirmed in Chromium, pending).

The fix has one reach the brief does not name: `guide_check.js` line 487 skips every HTML text under `[aria-hidden="true"]` in its 13 px floor and contrast scan. Wrapping the fragments would take 4,504 text elements in 411 image stages out of that scan (markup count), so the check would stop measuring the words of most failure plates, anatomy drawings and specimens. The fix needs the check changed in the same commit.

**(c) "Where to start" at 320 px with text at 200 percent.** From the markup: 20 `span.step-to` lines, all on the start page's routes, each inside `a.xref.step-go`. `.step-to` is `display: inline-block` with no `overflow-wrap`, and its words hold no-break spaces from the widow rule ("Components and\u00a0interaction", "Status and utility\u00a0icons", "Layout and\u00a0spacing", "choose\u00a0them"), so an inline block's narrowest width is its longest unbroken run. Browser measures pending.

**(d) Chapter 26's token table script.** From the markup: one element on the whole page carries the class `tt`, the token table's own (`s-26-token-table`, chapter 26). No other element carries `tt` or any `tt-` class. The script sits inside its own stage, so scoping it to that stage touches one script in one plate and moves nothing today. Its style block is page-wide as well: 58 selectors, none scoped to the plate (`.tt`, `.tt-find`, `.tt-grp` and the rest), the same latent fault for styles.

## 6. Questions for Dustin

Pending.

## 7. Tested

Pending.

## 8. Not tested

- Real screen readers (NVDA, JAWS, VoiceOver, TalkBack), Safari and Firefox: Not tested, by DR-279. Where this report says what a reader would hear, it reads Chromium's accessibility tree, labeled as such.
