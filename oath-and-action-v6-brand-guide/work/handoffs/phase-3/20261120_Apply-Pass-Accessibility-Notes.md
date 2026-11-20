# Apply pass: accessibility notes, board 3 (chat 9)

Status: 22:21 UTC. Done. A3, A5 and A14 checked in Chromium's accessibility tree and by keyboard on a strict build of my own (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/b10533d7-1a9f-5c9c-9fa4-64f6867e8ec0/scratchpad/c09/accessibility/guide.html`, exit 0, 0 warnings, 12,210,634 bytes, built 21:16 UTC from the tree at commit `b23b1e1c`), with version 13 (`work/boards/phase-3/review-4-5/20261120_Guide-Preview-V13.html`) as the before. No fault found. One item holds a question a screen reader must answer (A14, below). Nothing nearby broke that I could find.

## Confirmed

### A3 (reply 8): "Choose a chart" and chapter 14's group heads

- **Headings and levels (1.3.1).** Chromium's tree holds 505 headings, against 469 in version 13, at 1440 and at 390 px. The 36 added are exactly "Choose a chart" (h3, the plate's label), its 17 lines as h4 (the 16 questions, then "Three charts in full") and chapter 14's 18 group heads (h3). None was removed, and no other heading changed its level or its words. The page keeps one h1 and skips no level anywhere: chapter 14 runs h2 "14 Data visualization", h3 "Choose a chart", 17 h4s, then h3 "Group 1 Every chart" and the rules' h3s, and each group's h3 stands before its rules. The 17 h4s match the words of group heads 2 to 18, in the same order.
- **Moving by headings.** The order in the tree is the source order, and on screen every heading sits below the one before it (0 reversals among 505 at both widths). So a reader moving by headings meets "Choose a chart", the 16 questions and "Three charts in full", then group 1 to group 18, in the order the page shows them. I checked this order in the tree. I did not check it with a screen reader's heading keys.
- **Nothing looks different (1440 and 390 px).** Computed styles of all 36 elements are identical to version 13's paragraphs, property for property, at both widths. On the new page I turned the 36 headings back into paragraphs, keeping their classes and contents. The pictures did not change: the whole "Choose a chart" plate and all 18 group blocks match pixel for pixel, 19 of 19 at each width. Every element's size, its place in its block and the gap to the next block also stay the same. Pictures compared across the two builds differ only by 1 px rounding of the page offset, because other items in this pass moved the page above them.
- **No other plate gained a heading.** In the tree and in the source, the only headings inside any figure or specimen are the 18 in `fig-s-14-selection-guide`. Group heads in other chapters stay paragraphs, and chapter 01's first group block matches its version 13 picture pixel for pixel. The rail and the phone menu are byte for byte the same as version 13's.
- **Names.** Each group head is named, for example, "Group 2 Comparison: which is bigger, and how do they rank?". Chromium exposes the small capitals as "GROUP", just as every rule head already reads "RULE". That is not new behaviour.

### A5 (reply 10): the masthead at 360, 372, 375 and 390 px

- **Wordmark and button line.** Measured with scripts on and with scripts off, before and after:

| Width | Version 13 | This build (scripts on and off alike) |
|---|---|---|
| 320, 359 px | 16 px wordmark (152 px), button on the bar's line, masthead 89 px | same |
| 360, 372 px | 24 px wordmark (221 px), button dropped to a second line (its top at 56 px), masthead 133 px | 16 px wordmark (152 px), button on the bar's line (6 to 50 px, centred on the wordmark), masthead 89 px |
| 373, 374, 375, 390 px | 24 px wordmark, one line, 89 px | same |

  No width scrolls sideways. With scripts off, `--head-h` at 360 and 372 px is now the two bars' sum (88 px). Version 13 used the 8.25rem floor there. The content's `scroll-margin-top` is 112 px at every width I measured, which clears the 89 px masthead. I looked at the masthead pictures at 360, 372 and 375 px: the 16 px wordmark through 372 px, the 24 px from 375 px, and the button on the bar's line.
- **Focus not obscured (2.4.11, and 2.4.12 as well).** This was the main session's sample, after it narrowed my first run. I took 18 links spread through the page: the second and fifth links of the contents, "Where to start" and chapters 01, 05, 11, 14, 15, 18 and 26. I reached each one by keyboard in three ways. With Tab, the link started half under the masthead. With Shift+Tab, it also started half under. With Shift+Tab again, it started a whole screen above. That gives 54 key presses per setting, run at 360, 372, 375 and 390 px with scripts on and at 372 px with scripts off, 270 presses in all. Every press landed on the intended link. Chromium brought every link out with its 2 px ring wholly clear of the masthead: no link ended partly under it and none ended below the window. The smallest gap between a link's top and the masthead's foot was 22.5 px.
- **Fragment targets.** Following `#rule-11-2`, `#rule-03-4` and `#group-14-2` with scripts on, the heading that takes focus sits 109 to 112 px from the top at all four widths, clear of the masthead. `#group-14-2` now focuses the group's own h3 (see "Nearby").

### A14 (reply 20, DR-294): chapter 11's four plates

- **Alt is the head sentence.** Each alt is the first sentence of its version 13 alt and nothing more: `s-11-steps` 932 to 41 characters, `s-11-marks-drawn` 1,807 to 125, `s-11-ballot-steps` 1,758 to 260, `s-11-court-steps` 1,016 to 91. The steps' and marks' own words now reach the tree once, from the table. In version 13 the stage's description held 99 to 100 percent of the table's words.
- **Each table named by its caption.** In Chromium's tree each table takes its name from its `<caption>` (source: related element), and the caption holds the head sentence. In version 13 none of the four tables had a name. Each caption measures 1 by 1 px, positioned absolutely with `clip-path: inset(50%)`.
- **Nothing changed on screen.** On the new page I took the four captions out, and nothing changed: the four plates match pixel for pixel at 1440, 390 and 360 px. Figure size, table size and place, and the gap to the next block are also the same. Between builds, figure and table geometry match at all three widths. Seven of the 12 pictures match pixel for pixel, and the other five differ only by 1 px of page offset.
- The build's picture counts stay at 101 hidden and 315 open, the same as version 13.

### Nearby

- After A3, `#group-14-*` links focus the group's h3, where version 13 focused the group block. The shell's `onHash` picks the first h1 to h3 in its target. The focused heading sits clear of the masthead, and the next Tab continues from it. The return link's label for a group (the shell's `h3, .rg-head` lookup) reads the same words.
- The masthead at 320, 359, 373 and 374 px is unchanged, and no width scrolls sideways.
- Every heading outside chapter 14 is unchanged in level and words. The rail and menu markup are unchanged.

## Not confirmed

- **A14, "heard once," in a screen reader.** In the tree, the head sentence now sits three times in a row: as the stage's description (`aria-describedby` to the alt), as the table's name and as the caption's own text. The long repeat is gone. The step words are heard once. Whether a reader speaks the sentence once, twice or three times depends on the screen reader and its settings, and I had none to run. On `s-11-ballot-steps`, the visible figcaption also repeats most of the same 260-character sentence (the four states). There a listener may hear that sentence up to four times. This is not a WCAG failure. See the call below for the fix, if the main session wants one.
- **A3, moving by headings with a screen reader's own keys.** I confirmed the order in the accessibility tree and on screen only.

## Calls

- D3-xxx | A3: chapter 14's group heads stand at h3, peers of the rules' h3s, and the rules are not moved under them to h4 | The brief asks for levels that skip none, and this outline skips none. Moving chapter 14's rules to h4 would make one chapter's rules differ from every other chapter's for a reader moving by headings
- D3-xxx | A3: "Three charts in full" as the 17th h4 in "Choose a chart" stands (the engineer's call) | It heads its own links. As a paragraph, its links would fall under question 16 for a reader moving by headings
- D3-xxx | A14: accept as built, with the head sentence kept as the stage's description beside the table's caption | Dustin's answer sets the same sentence in both places, and the tree then holds it three times in a row. If the main session wants it heard once, the cure is a build rule in `work/build/scripts/phase-2/guide_build.py` (the engineer's file): leave out `aria-describedby` on a readable stage whose one table carries a `<caption>` that matches its alt. That is best taken in the finishing pass with AX-S3's 30 other readable plates

## Tested

- Strict build: `flock .../c09/build.lock python3 -I work/build/scripts/phase-2/guide_build.py --strict --out .../c09/accessibility/guide.html`, exit 0, 0 warnings, 369 rules, 679 specimens; pictures 101 hidden, 315 open (version 13 the same).
- Chromium (Playwright 1.63, headless), every launch after `browsers.sh` said "OK to open one":
  - The tree's headings by `Accessibility.queryAXTree` (role heading), with level, name, place and section, both builds at 1440 and 390 px.
  - Computed styles and pictures of A3's 36 elements across builds. The same-page swap of headings to paragraphs at 1440 and 390 px.
  - The masthead on both builds, scripts on and off, at 320, 359, 360, 372, 373, 374, 375 and 390 px, with pictures at 360, 372, 375 and 390 px.
  - Keyboard: 270 presses over 18 sampled links, as above.
  - Chapter 11's four plates: tree, alt, caption and geometry on both builds at 1440, 390 and 360 px. The same-page caption removal at the same widths.
- A static outline of both pages (Python's HTML parser): 470 to 506 headings in the source, 36 added, 0 skipped levels, headings only in `fig-s-14-selection-guide` among figures and specimens.
- Probe, data and pictures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/b10533d7-1a9f-5c9c-9fa4-64f6867e8ec0/scratchpad/c09/accessibility/` (`probe.mjs`, `a3-headings.json`, `a3-look.json`, `a3-swap.json`, `a5-masthead.json`, `a5-focus-sample.json`, `a14.json`, `a14-swap.json`, the PNGs).

## Not tested

- Any screen reader (NVDA, JAWS, VoiceOver, TalkBack). For A14 and for heading keys in A3, I read the tree only.
- A broad keyboard run. My first wide run (three starting points, arrow-key scrolling between presses) measured links while Chromium's scroll animation was still moving, so I set its numbers aside. A second, settled run was stopped at the main session's word at 22:17 UTC before it wrote results. The 18-link sample stands in its place. The main session's guide check tests focus offsets at four widths after me.
- The masthead and focus at 200 percent text and at 400 percent zoom, in forced colors and in print. A3 and A14 at widths other than 1440, 390 and 360 px. Scripts off at 360, 375 and 390 px for the keyboard sample (the masthead itself was measured scripts off at every width).
- The guide check, as the brief says. The main session runs it on the joined build.
