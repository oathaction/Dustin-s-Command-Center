# Stage C round 2: craft and accessibility red team

Oath & Action Edition 06, Phase 2, stage C round 2, November 11, 2026. Reviewer: the design director as reviewer, checked against the UX and accessibility lead's checks. Page reviewed: the frozen chapters page at commit df0fb08d (`round-2/review/guide.html` in the session scratchpad). Work in progress; this file grows as checks finish.

## Score

Pending.

## Must fix

Pending.

## Should fix

Pending.

## Questions for Dustin

Pending.

## Working notes (interim, folded into the sections above when done)

- Copy promise, first pass: twelve sets copied through their own Copy buttons (clipboard read back, identical to the panels): c-18-tabs, -masthead, -form, -filter-bar, -search, -theme-switch (with its head script), -table, -toggle, -messages, -copy, c-26-download, c-26-warning. Each in a blank page built as Rule 26.5 says (color scheme meta, the fonts link, tokens.css as the page's own download gives it, the body rule, the set's CSS, the HTML, the script last). Draws: light, device dark and forced colors at the stage's width, side by side with the live stage: no difference I could see. Behaves: every keys.json path walked with the guide check's own step reader, at 1440 and 390, in the copy (light and dark) and in the guide: identical results; the only misses are the harness's (focus leaving a blank page lands on its body).
- Computed style diff, stage against copy, element by element: identical for ten sets. Two differences: the form's title is a fluid size (24 px at a 1440 window, 21.39 px at 755), a harness artifact; and the filter bar's and search's IDs, which the guide's build wraps in `span.nw` inside the live stage, so the stage's markup is not the code a builder copies.
- c-18-download live stage: pressing "Download tokens.css, CSS, 93 KB" navigates the whole guide to Chromium's error page (`chrome-error://chromewebdata/`), since `href="tokens.css"` names a file that does not sit beside the guide.

- codeMatch (D2-1526): `guide_check.js` sets `EDGE_TOL = 64`, while D2-1526 and the comment above it say 49. Rerun of codeMatch's own capture and comparison with faults planted in the pasted copy only: as built the four stages differ by at most 41 (table, dark). At 64, error words and table cells drawn in `--oa-color-text-secondary` on Charcoal (Dim Newsprint for Newsprint, 13.29 to 1 falling to 7.26) pass; at 49 they are caught. The success mark drawn in Stone for Verdigris passes at 64, 49 and even 32 (largest pixel difference 38 light, 27 dark). Row rules in Deep Stone for Stone pass at every tolerance; 754 differing pixels sat on the capture's outer ring, which is never compared.

## Tested

Pending.

## Not tested

Pending.
