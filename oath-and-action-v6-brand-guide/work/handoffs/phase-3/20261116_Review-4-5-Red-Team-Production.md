# Review of rounds 4 and 5: red team, production

Oath & Action Edition 06, Phase 3, chat 7, November 16, 2026. Reader: production (codes PR). Role: `.claude/agents/oa-engineer.md` as a reviewer, then a simulated designer at a partner organization. **The designer is simulated and untested with a real person.** Brief: `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md`. Build read: the strict build of `9a6e1182` (`scratchpad/c07/main/guide.html`, 12,107,102 bytes), copied to my scratch folder before any script read it. Paths are relative to `oath-and-action-v6-brand-guide/`.

Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/review/production/` (scripts `scan_css.py`, `scan_js.py`, `scan_inward.py`, `scan_sources.py`; results `css_scan.json`, `js_scan.json`, `inward.json`; the generator log `gen-reruns.log`; the kit log `kit-all.log`; a scratch copy of the project folder under `repo/`). The production test's files: `work/handoffs/phase-3/review-4-5-production-test/`.

Started 16:34 UTC. Status: in progress (16:53 UTC). Sections fill as checks finish.

## 1. Score

Pending.

## 2. Must fix

Pending.

## 3. Should fix

Drafted so far; the production test adds to it.

**PR-S1. Chapter 26's token table script still selects `.tt` across the whole page** (named place 2(d), D3-1892, DR-278).
- Where: `work/build/scripts/phase-2/token_table_build.py` line 265 (its `SCRIPT`), written into `work/build/guide/specimens/s-26-token-table.html` line 71.
- What is wrong: `document.querySelectorAll('.tt').forEach(function (box) { var q = box.querySelector('.tt-q'), status = box.querySelector('.tt-status'), words = status.querySelector('.tt-t'); ...`. Any element of class `tt` anywhere on the page is taken for a token table. One without a `.tt-status` child throws on `status.querySelector`, which stops the loop; chapter 14 sits before chapter 26, so a `.tt` in any earlier plate leaves the real table's search and Copy buttons dead. That is what SG-7 caught on Rule 14.144's failure plate.
- Fix: scope it the way the guide's other twelve plate scripts already do: `var S = document.currentScript && document.currentScript.closest('[data-specimen]'); (S || document).querySelectorAll('.tt').forEach(...)`. Owner: engineer (`token_table_build.py` and chapter 26's token table). Rerun the generator; `guide_build.py`'s `token_table_stale()` then accepts the new fragment. Show it on board 3 as a change to approved work (DR-278).

**PR-S2. Only two of about thirty generators that write plate CSS check their braces, and the build checks none** (named place 3).
- Where: brace checks exist only in `phase3_ch14_complex_build.py` (its `check()`, line 1086) and `phase3_ch15_build.py` (`brace_fault`, line 5206). The rest write plate styles with no check, among them round 5's `selection_guide_build.py`, `palette_spec_build.py`, `phase3_ch14_rules_build.py`, `apply_systems_ch11.py` and `token_table_build.py`, and phase 2's `stage_a_systems_build.py`, `stage_b_ch10_build.py`, `stage_b_ch12_systems_build.py`, `stage_c_ch17_build.py`, `stage_c_ch18_build.py`, `stage_c_ch18_anatomy_build.py`, `stage_c_ch19_build.py`, `stage_c_ch26_build.py`, `phase3_ch13_build.py`, `promotion_identity.py`, `stage_a_identity_build.py`, `stage_b_identity_ch01.py` and `guide_editor_*`.
- What is wrong: today nothing leaks (section 4, named place 3), but one stray `}` in any of them sends the rest of that plate's rules to every page element, as D3-1893 did, and only a capture would show it.
- Fix: one check where every plate style passes, `guide_build.py`'s `process_fragment()` just before `scope_styles()`: strip comments and strings, count braces, and warn when a closing brace takes the depth below zero or the style ends open. A warning stops a strict build, so the check covers every generator at once, today's and Phase 4's. Apply the same check to the two chapter blocks (`data-plate-css`) and to the bare plates' style. My scanner (`scan_css.py`, about 60 lines) is a working model; it found every planted fault in its self-test. Owner: engineer.

**PR-S3. Chapter 18's form script and the chart kit share the attribute `data-oa-form`** (found by the named place 3 scan).
- Where: `work/build/guide/code/c-18-form.js` (`document.querySelectorAll('[data-oa-form]')`, placed live at Rule 18's form code set and given to builders to copy); `work/build/chart-kit/kit.js` line 825 and `kit-build.js` line 433, which write `data-oa-form="<form name>"` on every chart drawing.
- What is wrong: the form script takes every chart drawing for a form. On the page today it matches S94's calendar card (drawn into the page at build time) and any chart the kit has drawn by the time chapter 18's script runs; each gets a `submit` listener that never fires. It throws nothing today, so no reader meets it, but a builder who copies the form script into a page with kit charts carries the same collision, and any later change to the script that reads a child without a guard breaks every real form after the first chart.
- Fix: narrow the copy-ready selector to `form[data-oa-form]` (one line in `c-18-form.js`; the code panel and its copy text follow from the file). Renaming the kit's attribute would touch every chart (about 112) and the kit's exports instead. Owner: component engineer. A change to approved chapter 18 code: list it for board 3.

**PR-S4. The kit's weight warning still cites the rule DR-271 retired.**
- Where: `node work/build/chart-kit/oa-chart.mjs build s96` prints "~ warning: weight: about 16,144 bytes on the page with its frame, past 15,000; no plate from round 3 on (S65 and later) goes past it (D3-1328)".
- What is wrong: under DR-271 and D3-1895 the 15,000-byte figure is reported and S96's plate was raised to what it holds. The line tells a designer a rule is broken when it is not. The same run's last line says it wrote "PNG" exports under `--no-png`.
- Fix: word it as a report ("16,144 bytes with its frame; the plate figure is 15,000 (DR-271, reported)") and say "no PNG (--no-png)" when PNGs are off. Owner: engineer.

## 4. The named places in this lens

**2(d), chapter 26's page-wide `.tt` selector.** Still unfixed in the committed state (PR-S1). Measured on the built page: the script's one selector matches 1 element, inside its own plate, and 0 outside. Reach of the fix is in section 5.

**3, page-wide reach, guide-wide.** Scanned every `<style>` and `<script>` on the built page by script (no browser).
- Styles: 671 on the page. 635 plate styles wrapped in `@scope ([data-specimen="..."])`, the 2 chapter blocks (`@scope (#data-visualization [data-specimen])`, `@scope (#systems-graphics [data-specimen])`) and the 1 bare plate's style all balance: no closing brace ends a scope early, no rule sits after its scope, no global at-rule (`@keyframes`, `@font-face`, `@property`, `@import`, `@page`) inside a scope. The 28 code-set styles are page-wide by design and every selector in them names an `oa-` hook. The kit's style names a kit hook in every selector. The scanner's self-test planted one extra brace in chapter 15's block and one in a chapter 14 plate; it reported both, with the 248 and 8 rules that would leak.
- Plate scripts: 13 run (111 more are chart data, `type="text/plain"`). Twelve find their own plate first (`document.currentScript.closest("[data-specimen]")`). One, chapter 26's token table, selects the whole page (PR-S1).
- Code-set scripts: 16, page-wide by design, each on its own `data-oa-*` hook; each matches only its own two live stages, except the stepper (also 14.143 and 15.19, as intended, C-113) and the form (also chart drawings, PR-S3).
- The other direction, page CSS reaching into plates: shell selectors with short names reach plates they were not written for. `.rt` (`grid-column: var(--txt-col)`) matches 11 SVG groups in 7 chapter 15 plates (15.11, 15.12, 15.16, 15.20), where grid placement does nothing; `.n` (tabular figures) matches 28 elements in 4 plates (15.22's stage numbers, two chapter 14 ticks); `.nw`, `.vh` and `.illus` mean the same in plates as in the shell. Chapter 14's block reaches 14.142 to 14.144 with `.p`, `.k`, `.dnp` and `.art`; the declarations match the plates' own, so nothing moves. Nothing moves today; the class list is the same hazard as `.tt`, and the reserved-name check the complex examples generator carries (`{"tt", "rt", "tk", "fx"}`) belongs in the build beside PR-S2's brace check.
- Generators: every specimen source (679 files) and the 28 code CSS files balance today; the two chapter CSS fields (`14-data-visualization.json` 56 rules, `15-systems-graphics.json` 248 rules) balance. Which generators check: PR-S2.

**5, the palette specification.** `palette_spec_build.py --check` reports "2 of 2 files current, tokens 6.0.0-gate3.3"; a rerun in a scratch copy wrote 0 files and left an empty `git diff`. The plate's values and the token release test: in progress.

**11, weight (DR-271), from the build report.** Page 12,107,102 bytes; projection 15,117,621 against the 15,500,000 warning and the 16,000,000 limit; chapter 14 at 2,072,555 against 2,803,941 by the chapter count, and 120,739 bytes past it once the kit (565,548) and the parts that are not plates (286,577) are added, as D3-1895 says; the kit at 565,548 past its 560,000 figure (reported, a note); chapter 15 at 562,202 (figure 600,000); chapter 11 at 500,801 (figure 550,000); S96 15,394 bytes as placed, about 16,144 with its frame. Round 5's plates as placed: selection guide 149,403, palette plate 69,443, Rule 14.142 32,433, 14.143 43,078, 14.144 55,628. All match the brief.
- Bytes a reader never meets: 31,123 bytes of HTML comments in 235 places (maker and file headers, s-15 8,495, s-14 6,117, s-02 5,521, s-01 5,317, s-13 4,217), and 11,254 bytes of comments in plate and shell scripts. The 14,367 bytes of comments in code-set CSS and 7,381 in code-set scripts are part of the code a builder copies, so they earn their place. 14.144's three print copies of Loop R8 (7,428 bytes) are met on paper (D3-1990). The kit on the page carries only the 91 forms the page draws; the four card forms render at build time and stay out of the bundle. So about 42 KB, 0.35 percent of the page, could go by a comment strip in the build; it is not worth a fix on its own.
- Room for Phase 4: the page may grow 3,892,898 bytes to 16,000,000. Less Phase 5's 400,000 for chapters 27 and 28, Phase 4's seven chapters (16 and 20 to 25) have 3,492,898, about 498,985 each, or 2,992,898 (427,557 each) to stay under the 15.5 MB warning. Their allocation is 2.54 MB shared (362,857 each, `guide_charts.py` line 58). The eighteen built chapters other than 14 average 458,048 bytes (median 323,249), but the three that carry applications and live code run past 1 MB (01 at 1,355,471, 18 at 1,164,926, 26 at 1,027,783). Phase 4 is applications and photography. So room exists only if those seven stay near today's median; one chapter at chapter 18's weight takes 0.8 MB of the margin. Question Q-PR1.

## 5. Measured reach

- **2(d), PR-S1.** Touches 1 generator (`token_table_build.py`, 1 line plus 1) and 1 specimen regenerated (`s-26-token-table.html`, line 71). On the page: the selector matches 1 element today, inside the plate; 0 elements move; about 70 bytes added. No other plate uses the class `tt` or any `tt-` name (scan of the built page and the 679 sources).
- **PR-S2.** Touches 1 function in `guide_build.py` (`process_fragment`) and the build's self-test (two fixtures: an extra brace, an open block). On today's page: 0 warnings, 0 plates move (635 plate styles, 2 chapter blocks, 1 bare style balance).
- **PR-S3.** Touches 1 line in `c-18-form.js`; Rule 18's two live form stages and its code panels change by 4 characters each. On the page: the form script stops matching 1 static chart drawing (S94) and every chart drawn before chapter 18's script runs; the two real forms behave as before.

## 6. Questions for Dustin

**Q-PR1. Phase 4's weight.** Phase 4's seven chapters share 2.54 MB in the projection, about 363 KB each; the room to 16 MB is 3.49 MB, about 499 KB each. Three of today's chapters with live examples weigh over 1 MB. Recommendation: ask the engineer to size each Phase 4 chapter from its nearest built analog before Phase 4 starts (photography against chapter 01, applications against 18 and 26), and to decide then which pieces ship as downloads beside the guide rather than on its page; nothing is cut now.

## 7. Tested

- The guide-wide CSS reach scan on the built page: 671 styles parsed with comments and strings removed; 0 faults; self-test with two planted braces found both (`scan_css.py`).
- The plate and code-set script scan: 141 scripts, 13 plate scripts, 16 code-set scripts; every literal selector run on the static page with BeautifulSoup and soupsieve, matches counted inside and outside the owning plate (`scan_js.py`).
- The inward scan: every shell selector and both chapter blocks' selectors run on the static page, matches counted per plate (`scan_inward.py`, 2 minutes 16 seconds).
- Brace balance of the 679 specimen sources, 28 code CSS files and the two chapter CSS fields (`scan_sources.py`).
- Generator reruns in a scratch copy of the project folder (copied 16:44 UTC, a fresh git baseline whose tree matches the repository's `HEAD` for `work/` and `deliverables/` blob for blob, review reports aside), each followed by `git status --porcelain`; all exit 0 with an empty diff: `palette_spec_build.py` (and `--check`), `maker_a_round4_derive.py --figures` (51 checks, 0 failed), `maker_i_round4_derive.py --figures` (all passed), `maker_c_round5_derive.py --figures --drawings` (44 word checks, 0 faults; 1,988 named columns measured), `cartographer_round4_derive.py`, `research_reconciliation_rows.py` (57 rows), `selection_guide_build.py` (both files unchanged), `phase3_ch14_complex_build.py` (0 written, 0 faults), `phase3_ch14_rules_build.py`, `phase3_ch14_build.py` (99 files, 0 written, 0 faults; 112 examples logged), `phase3_ch15_build.py`, `apply_systems_ch11.py`, `apply_systems_ch11_ui.py`, `token_table_build.py`, `stage_c_ch18_build.py`, `stage_c_ch18_anatomy_build.py`.
- The kit: `oa-chart.mjs build --all --no-png` in the scratch copy, 96 of 96 PASS, 0 FAIL, 1 warning (PR-S4), empty diff (3 minutes 4 seconds, no browser).
- Weight figures read from `guide-Build-Report.json`; comment bytes and chart data bytes measured on the page by script.

## 8. Not tested

- Anything in a browser so far: the load rule printed WAIT at 16:48 UTC (2 browsers, load 3.42). The token release test and the production test follow.
