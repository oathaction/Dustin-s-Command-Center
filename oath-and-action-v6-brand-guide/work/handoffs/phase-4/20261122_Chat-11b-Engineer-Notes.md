# Chat 11b engineer notes

Engineer, chat 11b, November 22, 2026. Brief: `work/handoffs/phase-4/20261122_Chat-11b-Brief.md`, section 5.2 (DR-316 and DR-317). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/d65811ca-3324-52ca-92e9-a6b33b098503/scratchpad/c11b/engineer/`. Started 15:34:19 UTC (`date -u`).

Status: 15:57 UTC. Section 5.2 is done: DR-316 and DR-317 applied in chapter 18's code set, its keys file and its anatomy through their generators; the website's menu follows; the editor's words for Rule 18.6 typed; the kit, the chapter 20 generator and the strict build rerun in order under the lock; every proof below passed. The main session's snapshot a0ff7648 (15:48:14 UTC) holds all of it, and the tree has not moved since (the anatomy rerun at 15:56:40 left `git status` clean). Waiting for chapter 21's jobs.

**For the accessibility lead:** the three working pages in `work/build/exports/phase-4/` changed at 15:41:37 to 15:42:19 UTC: the article's Explain link and the Act page's Act link now carry `aria-current="true"` (the home link keeps "page"), and the menu's scroll padding now comes from chapter 18's own CSS and script, at the same values. Their 38 PNG captures are byte for byte the files they replace.

## Routine calls

- D4-xxx | Chapter 18's code set draws its page inside Explainers: both Explainers links carry `aria-current="true"`, and an HTML comment in the parts list says the part's own front page takes `aria-current="page"` | DR-316 names the code set and its keys file; the set's one generic page shows the case DR-316 adds, and the key paths now prove the value. The comment sits inside the list the website replaces, so no site page carries it
- D4-xxx | Chapter 18's CSS keeps its `[aria-current]` selectors, which match both values | DR-316 asks the CSS to match either value, and these already do; no approved CSS line changes for DR-316 (the `"false"` value is under "Not fixed", E11b-1)
- D4-xxx | DR-317 in chapter 18: the dialog takes `scroll-padding-top: calc(var(--oa-space-800) + 1px)` in `c-18-masthead.css`, and `c-18-masthead.js` sets it on opening to the title row's height plus 9 px (the 2 px ring set 2 px out, and 5 px of air), measured after `showModal()` and before focus moves | The website's D4-161 values, the accessibility lead's AL11-2 fix; the row can only be measured once the dialog shows, and setting it before focus moves means the first scroll already respects it; a row that wraps at a large text size still clears
- D4-xxx | The website's scroll padding defers to chapter 18's: the site's own CSS rule and its copy in the site's script (D4-161) are removed, and the site reads chapter 18's through `masthead_css()` and `masthead_js()` | One rule holds it (reuse, never copy); the values are the same, so the site behaves as before, proved by the W1 rerun on the three working pages (below)
- D4-xxx | On the website the current part takes `"true"`: the kit draws no part's front page (its article sits inside Explain, its Act page inside Act), and the home page keeps `aria-current="page"` on the home link | DR-316; `site-parts.mjs`'s `masthead()` already took `'page'` or `'true'` from its caller
- D4-xxx | The kit runs with `--date 20261121`, so it rewrites the 41 exports in place | CLAUDE.md: a file keeps the date it was first created; the default (today) would have written a second set of 41 files and a renamed manifest beside the first
- D4-xxx | Register codes (`DR-316 (AL11-1)`, `DR-317 (AL11-2)`) go in the Python generator and the kit's sources; the code set's own comments are plain words | The code set's text prints in the guide as code to copy, and no code set file carries a register code

## Contracts

### C8. Chapter 18's masthead and the website's menu, after DR-316 and DR-317 (for the accessibility lead, the design director and the editor)

Live since 15:42:19 UTC.

- `c-18-masthead.html`: the example page sits inside Explainers; its bar link and menu row carry `aria-current="true"`. The bold words, the 2 px underline, the menu's selected band, 4 px bar and bold words are unchanged; the CSS reads `[aria-current]`, so `"page"` draws the same.
- `c-18-masthead.css` and `.js`: the dialog's scroll padding, `calc(var(--oa-space-800) + 1px)` until the menu opens, then the title row's measured height plus 9 px. The website reads both files, so its menu takes the same padding from chapter 18; the site's own copies are gone.
- The website (`renderers/web-site.mjs`): a part link takes `'true'` on a page inside its part; a future part front page passes `'page'` to `masthead()`. The home page keeps `aria-current="page"` on the home link.

## Done

1. **DR-316 in chapter 18.** `work/build/guide/code/c-18-masthead.html`: both Explainers links `aria-current="true"`, with a comment naming `"page"` for the part's own front page. `stage_c_ch18_build.py`'s `KEYS[6]`: the five focus targets read `[aria-current="true"]` (comment `# DR-316 (AL11-1)`), written to `c-18-masthead.keys.json`. `stage_c_ch18_anatomy_build.py` needed no change: it reads the code set, and its rerun moved `s-18-06-anatomy.html` (the attribute's value, inside a picture) and, for DR-317, `s-18-04-anatomy.html` and `s-18-06-anatomy.html` (the cut CSS carries the new rule). Both plates are pixel for pixel the same as before at 1440 and 390 px.
2. **Rule 18.6's words**, typed from the editor's "Words for the engineer" (written 15:35:29 UTC) after the code: the first paragraph's second sentence, the States row and the Hear row, with the file's curly quotes. Comment `# DR-316 (AL11-1)` above the rule, with `DR-317 (AL11-2)` noting no words change (the editor's finding).
3. **DR-317 in chapter 18.** `c-18-masthead.css` (a rule after the title row's) and `c-18-masthead.js` (on opening), as in the routine call.
4. **The website follows.** `renderers/web-site.mjs`: parts take `'true'` (comment `// DR-316 (AL11-1)`); the site's W1 CSS rule removed. `renderers/site-parts.mjs`: the W1 block of `close_on_widen_js` removed, with `// DR-317 (AL11-2)` and `// DR-316 (AL11-1)` notes in the source. Each working page now holds one `scroll-padding-top` rule and one `scrollPaddingTop` line, both chapter 18's.
5. **Run order, each under the lock:** `stage_c_ch18_build.py` (15:41:02) and `--check` ("chapter 18: current", exit 0); `stage_c_ch18_anatomy_build.py` (15:41:10, and again at 15:56:40, after which `git status` stayed clean); `node work/build/app-kit/oa-app.mjs build A04 A05 A06 A07 A08 A09 A10 --date 20261121` with `OA_APP_OUT` in my scratch (15:41:37 to 15:42:19); `phase4_ch20_build.py` (15:43:38; its outputs did not change); the strict build (15:43:44 to 15:43:55, and on the final tree 15:56:22 to 15:56:34).
6. **Proof.**
   - Strict build: exit 0, 0 warnings, 0 stale plates (no "stale" line in the log), 13,083,858 bytes, 393 rules, 731 specimens.
   - **Chapter 18: 1,167,458 bytes before, 1,170,416 after (+2,958)**: the rule's longer words, the comment and the script's new lines, each printed two or three times (two live stages, the style or script element, the code panel). **Chapter 20: 839,159 before, 839,156 after (−3)**: the kit's website style lost its own W1 rule and gained chapter 18's (49,347 to 49,344 bytes). Before is my baseline build of 15:38:15 on the opening tree with the editor's work in progress, which touches neither chapter.
   - Word search of the built HTML: each of the three new phrases prints once, in `rule-18-6`; the three old phrases print 0 times (once each before).
   - `check-dimensions.py`: 41 of 41 exports pass. `tools/export_checks.py`: 27 of 27 views pass. The kit's web checks from its facts: 18 page views with axe 0 and 12 of 12 Tab stops ringed, the theme kept after reload at 1440 on all three pages, reflow at 320 px and 200 percent text with no sideways scroll on all three, and the menu at 390 and 360 light and 390 dark opening on Explain with Escape returning to Menu: **0 faults**.
   - The 38 PNG exports are byte for byte the files they replaced; the changes are the three working pages, the manifest's `written` time, and the plates' input hashes and style.
   - **W1's case on chapter 18's live masthead** (my script, `tools/w1_ch18.cjs` in scratch, the accessibility lead's method): the built guide at 320 by 256 and 390 by 422 CSS px, the light and dark live stages, the Topics row closed and open, Shift+Tab and Tab, 24 presses a run, 16 runs. After: **0 controls hidden and 0 partly hidden under the title row in 16 of 16 runs**; Menu opens on Explainers (`"true"`), the padding reads 74 px (65 px row + 9). Before, on the baseline build: at 320 by 256 with Topics open, Shift+Tab left 4 stops hidden and 4 partly hidden; with Topics closed, 3 partly hidden; at 390 by 422 with Topics open, 2 partly hidden.
   - The same case on the three website working pages (`tools/w1_site.cjs`), 12 runs: 0 hidden, 0 partly hidden, 0 rings under the row; the least gap below the row 9 px, as in chat 11's rerun.
   - Pixels: chapter 18's two live stages (closed) and the anatomy plates s-18-04 and s-18-06, captured from the before and after builds at 1440 and 390 px in a 2,400 px tall window: 8 of 8 identical. (A first try in a 900 px window showed s-18-06 at 390 as different: that plate is taller than the window, and the capture stitched it under the guide's sticky header from different scroll positions; the tall window settles it.)
   - `git diff --stat 3bb5a1b0` (the editor's commit) shows only my 22 files and these notes: the four `c-18-masthead.*` files, `18-components.json`, `s-18-04-anatomy.html`, `s-18-06-anatomy.html`, `stage_c_ch18_build.py`, `site-parts.mjs`, `web-site.mjs`, the kit's seven plates and `web-site.css`, the three working pages and the exports manifest.

## Requests

- Main session or design director: `work/handoffs/phase-4/20261121_Web-Page-Specs.md`, the table row "Current part", still reads `aria-current="page"` (Rule 18.6 as approved; the accessibility lead's AL11-1 note stands for later). If that spec stays a living reference, the row could read "`aria-current="page"` on a part's front page, `"true"` on the pages inside it (DR-316)". I left it alone; it is not my file.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| E11b-1 | Engineer, chat 11b, while applying DR-316 | `work/build/guide/code/c-18-masthead.css`, `.oa-masthead-part[aria-current]`, `.oa-masthead-row-link[aria-current]` (and its forced-colors rule); `c-18-masthead.js`, `dialog.querySelector('[aria-current]')` | The selectors match any `aria-current` value, `"false"` included, which ARIA defines as "not current". A copy that writes `aria-current="false"` on the other links would draw them all bold and underlined, and the menu would open on the first of them | Match `[aria-current]:not([aria-current="false"])`, as `guide_check.js` already reads a current state | Approved code; DR-316 asks only that the CSS match both values, which it does; no page of the guide or the website writes `"false"` | Open |
| E11b-2 | Engineer, chat 11b, W1 runs | `c-18-masthead.css`: the dialog's navigation sits flush under `.oa-masthead-dialog-head` | At the top of the open menu, where it cannot scroll further, the first row's 2 px ring, set 2 px out, draws its top side under the title row's 1 px rule: 40 of 40 such stops in my runs, the same before and after DR-317. The row itself is never hidden or partly hidden, so WCAG 2.4.11 is met; the ring shows on three sides | A gap of at least 4 px between the title row and the first row (for example `margin-top` on `.oa-masthead-dialog-nav`); the website's menu has 24 px there, and its rings show whole | Approved layout; DR-317 names the scroll padding only | Open |

## Tested

- `stage_c_ch18_build.py` and its `--check` ("chapter 18: current"); `stage_c_ch18_anatomy_build.py` twice, the second run changing nothing (`git status` clean); its `--check` mode only reports sizes, and ran (25 plates, 158,518 bytes).
- The kit build of A04 to A10; `tools/export_checks.py` 27 of 27; `check-dimensions.py` 41 of 41; the kit's web checks read from every `facts.json` by my summary script (`tools/web_faults.py` in scratch), 0 faults; every export compared byte for byte with its copy from before the build.
- `phase4_ch20_build.py` after the kit; its outputs unchanged.
- Strict builds at 15:38:15 (before), 15:43:44 and 15:56:22 (after), each exit 0 with 0 warnings; the build report's chapter weights; a word search of the after page for the old and new Rule 18.6 phrases.
- W1's case in Chromium on chapter 18's live masthead in the before and after builds (32 runs), and on the three website working pages (12 runs).
- Pixel comparison of chapter 18's two live stages and anatomy plates s-18-04 and s-18-06, before and after, at 1440 and 390 px.
- A static check that each live stage of the built guide holds one bar link and one menu row with `aria-current="true"`, the targets the new key paths name; the W1 runs saw Menu open with focus on that row.

## Not tested

- The guide check's walk of `c-18-masthead.keys.json` (`guide_check.js`): the brief leaves the guide check to the main session's closing checks. My static check and the W1 runs cover the targets the paths name, not the walk itself.
- A screen reader announcing "current" for `aria-current="true"`: no screen reader runs here.
- W1 at other windows (360 by 400, 390 by 844) and with the title row wrapped at a large text size: I ran 320 by 256 and 390 by 422 at 100 percent text, as the brief sets. The script measures the row on each opening, so a wrapped row is in its reach, but I did not make one wrap.
- Forced colors and print on the menu; Safari and Firefox (only Chromium is installed).
