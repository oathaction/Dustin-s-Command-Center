# Chat 13b engineer notes (Engineer M): item 1 and C1, the page's weight

Engineer M, chat 13b, November 25, 2026. Brief: `work/handoffs/phase-4/20261125_Chat-13b-Brief.md`, section 3.1. Started 00:15 UTC (`date -u`). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/8ef25629-e16e-52f8-8c11-3387b872b013/scratchpad/c13b/engineer-m/`.

Files I write: `work/build/scripts/phase-3/guide_charts.py`, `work/build/scripts/phase-2/guide_build.py`, new scripts under `work/build/scripts/phase-4/weight/`, and a cache of re-encoded PNGs under `work/build/cache/`.

Status at 00:39 UTC: the check before 3a is done (below: no script reads a plate's own style); C1's four steps, the switch, item 1 and the forecast are written; the proof runs next.

## The check before 3a: does any script read a plate's own `<style>`?

No. Checked on the page of record (14,444,549 bytes, built 00:17 UTC from the tree at commit 9a1162e7), 00:37:18 to 00:38:00 UTC, one Chromium after `browsers.sh` read "OK to open one", with `work/build/scripts/phase-4/weight/style_reads.cjs`:

- While the page loaded and its 151 scripts ran (and the page was scrolled through once), no script read a plate style's `sheet` or `document.styleSheets`, and no `textContent`, `innerText`, `innerHTML`, `outerHTML`, `cloneNode` or `XMLSerializer` call touched a node that is or holds one of the 856 plate styles: 0 reads.
- The elements the scripts read on a click or a keystroke, found by reading every script on the page (the shell, the chart kit, chapter 18's code sets, the reader, library, loop, form and motion demos): table rows and cells, list items, `pre`, `code`, templates, headings, the copy buttons' 95 sources, the status words, the chart kit's 130 art boxes and 131 source lines, 3,714 SVGs, the tracker's news. None holds a plate style. Every plate style sits directly in a plate stage or an inset (`div.plate-stage`, `div.sx-inset`, `div.sx-qi`), never inside an element a script reads.
- The scripts' own text: no `querySelector` of a `style`, no `.sheet`, `cssRules` or `styleSheets` anywhere on the page. The chart kit's one `'<style>'` is a string it writes into a standalone SVG download.
- Outside the page: `guide_check.js` (the main session's check) reads the head's kit styles (`head style[data-oa-app-kit]`) and `document.styleSheets` for `@font-face` rules, never a plate's block; no other script in `work/build` names `@scope`'s plate form but the build and the generators that write it.

## Routine calls

- D4-xxx (M1) | pyoxipng (oxipng's Python bindings) installed into my scratch folder only (`pip install --target`), to fill 3b's committed cache once; the build reads the cache and needs no tool | The brief's way for 3b (a cache keyed by the original PNG's SHA-256); nothing installed system-wide or in the repository; chat 12b did the same (its M8)

## Done

## Requests

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

## Not tested
