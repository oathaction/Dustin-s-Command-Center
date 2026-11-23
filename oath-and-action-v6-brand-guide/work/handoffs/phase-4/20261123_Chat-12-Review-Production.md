# Chat 12 review: Production (PR)

Written November 23, 2026 by the production reader (the engineer as reviewer, then a simulated producer at a partner organization), from `work/handoffs/phase-4/20261123_Chat-12-Review-Brief.md`. Started 17:13 UTC. This file is written as the work goes; sections still marked "In progress" are not finished.

## 1. Score

In progress.

## 2. Must fix

Early finding, 17:30 UTC, written first because it reaches approved chapters.

**PR-M1. The kit's head styles reach outside their frames and break approved plates in chapters 14 and 15.** Where: `work/build/app-kit/tools/app_plates.py`, `head_styles()`, which places `plates/web-site.css`, `plates/atlas-page.css`, `plates/share-image.css`, `plates/favicon-set.css` and the plate style in the page's head with no scope; the renderers that write those files (`renderers/share-image.mjs`, `renderers/atlas-page.mjs`, `renderers/web-site.mjs`). What is wrong: the share card's style opens with `.sh{position:relative;width:1200px;height:630px;box-sizing:border-box;overflow:hidden;background:var(--oa-color-surface-newsprint);...}`. Chapters 14 and 15 draw a shaded pill as `<rect class="pl sh">`, and Chromium applies CSS `width` and `height` to an SVG rect, so on the page of record each shaded pill in `s-14-143-correct`, `s-14-143-failure` and `s-15-15-correct` is drawn 1200 by 630 px and covers the loop drawing and its read-aloud list with a Charcoal block. Proof: on the full strict build (`scratchpad/c12/main/guide.html`) at 1440 px, the same plate photographed with the kit's head styles on (as built) and off differs over 477 by 539 px; the side-by-side is `scratchpad/c12/review/production/leakshots/cmp-s-14-143-failure.png`. A computed-style scan of all 829 selectors in the kit's head styles found 2,779 elements outside the kit's frames that they match (chapters 01, 13, 14, 15 and chapter 18's live components), 97 whose computed style they change, and this one visible break. The short generic names `.sh`, `.sv`, `.ln`, `.pp` and `.rs`, and chapter 18's component classes, are the reach. Fix: scope every rule in the kit's head styles to the frames (wrap each file in `@scope (.oa-app-art)` or prefix `.ws`, as the atlas renderer's header already claims "every rule starts with .ws.wa" when it does not for the component and figure rules), and add a guide check plant: a chapter 15 pill with class `sh` beside a share card frame, which must draw at its own size. Owner: engineer. The fix changes no approved chapter's files; it puts chapters 14 and 15 back as Dustin approved them, so Dustin is told (section 5).

More in progress.

## 3. Should fix

In progress.

## 4. The named places

In progress.

## 5. For Dustin

In progress.

## 6. Tested

In progress.

## 7. Not tested

In progress.
