# Chat 12b editor notes

Editor, chat 12b, turn 2, November 24, 2026. Brief: `work/handoffs/phase-4/20261124_Chat-12b-Brief.md`, sections 1, 2, 3.4 and 4; the design director's notes ("Rulings", DD12b-C1, "Words for", 13 items); Engineer W's contract (W-C1 to W-C4). Started 01:07:46 UTC (`date -u`). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/editor/`.

Turn 2 files: the word fields of `work/build/scripts/phase-4/phase4_ch16_build.py`, `phase4_ch20_build.py` and `phase4_ch21_build.py`, and this file. The design director finished turn 1 at 00:55 UTC.

Generators before my first edit, copied to scratch `before/` with their `--page-words all` output (01:07 UTC), each equal to HEAD `a5bd3cdd`: `phase4_ch16_build.py` SHA-256 `6714797bcf5f3cc4…`, `phase4_ch20_build.py` `aaf958bab433a36d…`, `phase4_ch21_build.py` `790a0603769db4a7…`. After: `f89d393503244a27…`, `2a245ebf47257af6…`, `d763681fc79e6547…` (3 files, 100 insertions, 39 deletions against HEAD).

## Routine calls

- D4-xxx | The caption on screen at 0:08 is the WebVTT file's first cue, "Citizens 18 to 24 reported voting" / "at 47.7 percent, down 3.7 points", with no closing period, and a second cue finishes the sentence: "from 2020." / "Those 65 and over stayed near 75 percent." (11.500 to 15.000) | A21 now draws the caption beside the storyboard's said words, "… down 3.7 points from 2020. Those 65 and over …", and the old cue dropped "from 2020" and closed on a period, which Rule 16.11's "checked word for word" fails on its own plate. The whole clause on one line, "at 47.7 percent, down 3.7 points from 2020.", runs about 682 px at 32 px in the vertical frame's 660 px column (Inter SemiBold advance widths), so it would make a third line
- D4-xxx | The 0:30 caption breaks between the subject and the verb: "So the gap between the youngest and the oldest" / "grew from 23 points to 27." (46 and 26 characters) | The phrase break DD Words 1 and the main session ask for. The words are the sentence said, so they cannot shorten; Rule 16.11 says "about 42", and the storyboard's band holds about 64 at 32 px (DD12b-R1). The other break, after "youngest", splits "the youngest and the oldest"
- D4-xxx | Every row of frames in chapters 20 and 21 says "shown at {pct} percent on a 1440 px screen", and "true size" takes the same words, "true size on a 1440 px screen"; chapter 16's two storyboard cells say "shown at {pct} percent on a 1440 px screen" | The main session's item: each figure is computed at the 1440 px stage (722 px, CR-22). "True size" has the same fault: 19 rows print it, most of them 390 px frames, which a 390 px phone cannot show at true size. "On a 1440 px screen" is the guide's own phrase (chapter 16 already says it)
- D4-xxx | Rule 16.11's scale note reads "Shown at a quarter of 1080 by 1920" (was "Drawn at …") and names no screen | The frame keeps its 270 px wrapper at both widths measured (Engineer W: 268 px drawn at 1440 and 390 px), so the quarter holds; "shown" says what the plate does, since the kit draws the frame at 1080 by 1920
- D4-xxx | A21's overlay names its bases in plain words: vertical "TikTok’s and Instagram’s ad guides, retrieved November 21, 2026", storyboard "Our margin until chapter 23 sets one", "TikTok’s buttons", "The player’s controls" | DD12b-R1's draft basis carried decision codes ("D4-14 and D4-16"), which a reader cannot look up (house rule H11). The platform file names the vertical safe area "the larger of TikTok's and Instagram's margins" and dates both sources November 21, 2026
- D4-xxx | The frame alts say "the L8 monogram" | The composed alts printed a bare "L8" (house rule H11); Rule 16.10 names it "L8, the monogram"
- D4-xxx | Each frame alt describes what the frame shows: the frame and its moment, L8, chart S04's legend, scale ends and four rows with their rates and row words, the source line whole and the captions; S04's finding sentence and measure line stay out | The frame shows neither (DD12b-R1), and the rows carry the finding. The alts run 1,016 to 1,066 characters, where the composed ones ran 1,303 to 1,312
- D4-xxx | The caption lines, the source line and S04's drawn words sit once in the word fields (`CUE_0_08`, `CUE_0_30`, `S04_DRAWN`, and `S04_SOURCE` read from `s04.json`), and the captions, the WebVTT file and the alts take them from there | A frame's caption and its alt cannot drift apart
- D4-xxx | Rule 16.11's alt says the safe areas show when the page loads and a switch hides them | Both 16.11 plates place the frame with `data-oa-app-switch="on"` (W-C3, DD12b-Q3); DD Words 7's parenthetical ("no outlined box unless the reader switches the safe areas on") predates that wiring
- D4-xxx | Rule 16.11's alt names the hatched button column | Engineer W's commit `a5bd3cdd` (00:58 UTC, not yet built) draws the outline and the hatch over the band (DD12b-Q5b, W12b-3); the kit build that takes my words carries it
- D4-xxx | Chapter 16's captions do not use "application kit": Rule 16.10's says "We drew the 0:08 and 0:30 frames at 1920 by 1080 px …" | The term is first used in chapter 20 (house rule H02)
- D4-xxx | Rule 21.9's caption and alt name the 390 px crop under the 1440 px frame: "the sheet’s first three connections at 390 px, each a card with the same parts" | The plate places `390-light-sheettop` (DD12b-R2) and its words named only the 1440 px frame. The crop's three cards (L09, L20, L27) print the chip, both variables, sign, type, delay, grade and citation, read from `plates/a18.json`
- D4-xxx | Rule 20.9's Panels row: "panels that meet along a whole side, as the pillar row’s four cells do at 1440 px, count as one" | I agree with DD12b-R3; "a whole side" carries its test (the shared edge runs the length of the shorter side), so stacked bands and side-by-side cells read alike, and cells that touch along part of a side stay two
- D4-xxx | `signature` "Oath & Action" and `switch` "Show the safe areas" are written in the word field though they match the kit's defaults | Words a reader meets sit in the editor's field, not the kit's

## Rulings

None of mine; I follow the design director's (DD12b-R1, R1a, R2, R3) and Engineer W's contract.

## Words for

Nothing new for the kit to type. Every word above reaches the kit through `--page-words` (chapter 16 for A21; chapter 21 for A11 and A13), so these plates go stale by their words until the kit draws them again: **A21** (all four views), **A11, A13, A17, A18 and A20** (A11's entry names the frames of A11, A17 and A20; A13's names those of A13 and A18). Chapter 20's page words did not change (compared key by key), so A04 to A10 do not move. The overlay's figures stay the kit's.

## Done

All in the three generators' word fields; outputs written by the generators under the lock (last run 01:13:34 to 01:13:38 UTC).

**Chapter 16 (`phase4_ch16_build.py`), the design director's Words 1 to 10 (CD-S7, C16-V):**
- **Words 1.** `R['16.10']['frame_captions']`: `'0:08'` the first WebVTT cue (`CUE_0_08`), `'0:30'` "So the gap between the youngest and the oldest" / "grew from 23 points to 27." (`CUE_0_30`). `--page-words A21` now lists nothing under `composed`.
- **Words 2.** `R['16.10']['frame_alts']` (`1920-light-chart`, `1920-light-gap`) and `R['16.11']['frame_alts']` (`1080-light`, `1080-light-misheard`). For example: "A still from the video at 0:08, a vertical frame 1080 by 1920 px, with the L8 monogram at its top right. Near the top, chart S04 shows reported voting by age group, an open dot for 2020 and a solid dot for 2024 on a scale from 40 to 80 percent: 18 to 24, 51.4 in 2020 and 47.7 in 2024, down 3.7 points; 25 to 44, 62.6 and 60.2, down 2.4 points; 45 to 64, 71.0 and 70.0, too close to call (−1.0); 65 and over, 74.5 and 74.7, no clear change (+0.2). Under the chart, a Charcoal band holds the chart’s source line and then the captions. The source line reads “Source: … for that purpose.” The captions read “Citizens 18 to 24 reported voting at 47.7 percent, down 3.7 points”." The storyboard's say "At the left …", the source line "under the chart", and "Across the foot of the frame, a Charcoal band holds the captions"; the misheard frame's say "the automatic captions" and "down 37 points".
- **Words 3 and W12b-2.** `R['16.10']['frame_scale']`: "shown at {pct} percent on a 1440 px screen"; the cells read "0:08 · shown at 10 percent on a 1440 px screen" (was "0:08 · at 10 percent").
- **Words 4.** `R['16.10']['correct_alt']`: "… at 0:08 and 0:30, chart S04 with its source line under it and the captions on a Charcoal band, the 0:30 captions saying the gap grew from 23 points to 27; …" (was "chart S04 with its source line at 0:08; the gap marked at 0:30").
- **Words 5.** The `chart` and `gap` frames' labels in `R['16.10']['frames']` are empty, with a comment; the said words stay.
- **Words 6.** `R['16.10']['correct_caption']` adds "We drew the 0:08 and 0:30 frames at 1920 by 1080 px, with the chart, its source line and the captions, and our exports keep them at that size."
- **Words 7.** `R['16.11']['correct_alt']`: "A vertical video frame at a quarter of 1080 by 1920: chart S04 near the top, the L8 monogram at the top right, and under the chart a Charcoal band that holds the chart’s source line and two caption lines, Citizens 18 to 24 reported voting at 47.7 percent, down 3.7 points. The safe areas show when the page loads, and a switch hides them. A dashed outline runs 269 px in from the top, 120 px from each side and 672 px from the bottom, from TikTok’s and Instagram’s ad guides, and a hatched box marks TikTok’s button column at the right. Beside the frame, the WebVTT file with these two lines, the next two and their times." `failure_alt`: "The same frame, where the automatic captions read Citizens 18 to 24 reported voting at 47.7 percent, down 37 points." The one fault stays "down 37 points".
- **Words 8.** `R['16.11']['correct_caption']`: "A vertical frame at a quarter of 1080 by 1920, showing chart S04 with its source line and, inside the caption-safe area, its captions on a Charcoal band. Beside it, the WebVTT file; the frame shows its first two lines." (then the figures' line, unchanged). `scale_note`: "Shown at a quarter of 1080 by 1920".
- **Words 9.** `plh` and `safe` removed (nothing read them); new `safe_labels` (`vertical`, `landscape`, `buttons`, `controls`, the renderer's keys), `switch`, `signature` (Routine calls).
- **Words 10.** Rule 16.11's Type row: "Inter 600 in Newsprint on a Charcoal band, 13.29 to 1; 32 px on a 44 px line in our 1080 by 1920 and 1920 by 1080 frames, and chapter 23 sets the size for any other frame".
- **The 0:08 cue** (contradiction 1 below): `R['16.11']['lines']` and `['bad_lines']` drop the closing period, and the WebVTT file gains the second cue.

**Chapter 21 (`phase4_ch21_build.py`):**
- **Words 11, DD12b-R2.** `frame_alts['A18 390-light-sheettop']`: "The first three connections filed on the sheet for Domain D10. At 390 px, in the light theme." (was "The head of the sheet …"). `VIEW_WORDS['parts']['sheettop']`: "the sheet’s first three connections" (was "the sheet’s head and first rows"). Rule 21.9's caption and alt name the crop (Routine calls).
- **Words 12, CD-R1.** Read against Engineer A's load-state frames (`plates/a11.json`: the three first-screen views carry no `data-lit="true"`; the full-length views carry six or three, so `opener_caption` and `opener_alt` for the whole home, which say a question is pressed, stay true). The four strings named no pressed question, and now say the state: `opener_screens_alt` "… first screen twice, as it loads with no question pressed: … the whole drawing of the eight parts at full strength …"; `opener_screens_caption` "The atlas home’s first screen as it loads, before a reader presses a question, …"; `frame_alts['A11 1440-light-screen']` "… first screen with no question pressed: … at full strength, with its key …"; `['A11 390-dark-screen']` "… on a phone with no question pressed: …".
- **The main session's item.** `VIEW_WORDS['scale']` "shown at {pct} percent on a 1440 px screen", `['true']` "true size on a 1440 px screen".

**Chapter 20 (`phase4_ch20_build.py`):**
- **Words 13, CR-11 (DD12b-R3).** Rule 20.9's Panels row (Routine calls). The screen words that print "its cells meeting as one band" stay, since they print only where the pillar row's cells join.
- **The main session's item.** `VIEW_WORDS['scale']` and `['true']`, as chapter 21's.

## Contradictions found

1. `s-16-10-correct` and `s-16-11-correct`: the 0:08 caption ended "down 3.7 points." while the storyboard prints the words said, "down 3.7 points from 2020." Fixed (the cue split).
2. Rule 16.10's storyboard and Rule 16.12's script and transcript give different words for the same moments of the same video. Not fixed (E12b-1).
3. DD Words 7 ("no outlined box unless the reader switches the safe areas on") and the 16.11 plates' switch, which starts on. The words follow the plates.
4. "True size" on 19 rows of frames in chapters 20 and 21, most of them 390 px frames, which a phone shows smaller. Fixed (the main session's item, extended).
5. Rule 21.9's caption and alt named one frame; the plate holds two. Fixed.
6. W-C2's `safe_labels` table (`safe`, `caption`, `buttons`) and the renderer, which reads `vertical`, `landscape`, `buttons`, `controls`. I wrote the renderer's keys, as the design director noted.
7. Rule 16.11's "about 42 characters" and the 0:30 caption's first line at 46. Kept (Routine calls).

## Terms

No new term. "Caption-safe area" (Rule 16.11) and "L8, the monogram" (Rule 16.10) are defined in the chapter before these words use them; "cue" is left out of the reader's words ("the first two lines"); "application kit" stays out of chapter 16 (H02).

## Requests

1. **Main session, for Engineer W:** the kit's run order, under the lock: `phase4_ch16_build.py`, `node work/build/app-kit/oa-app.mjs build A21 --date 20261124`, `phase4_ch16_build.py`, `phase4_ch20_build.py` (`s-20-files` reads the exports manifest); `phase4_ch21_build.py`, `oa-app.mjs build A11 A12 A13 A14 A15 A16 A17 A18 A19 A20 --date 20261122` (A11, A13, A17, A18 and A20 are stale by my words), `phase4_ch21_build.py`; then the strict build. My Python port of the renderer's alt check finds no word missing from the four alts; the kit's own check is the one that counts. A21 is also stale on W's own 00:58 commit (`video-frame.mjs`, `a21-video-s04.json`).
2. **Design director, `s-16-10-correct`:** the 0:08 and 0:30 cell labels now run about three lines in their 200 px cells ("0:08 · SHOWN AT 10" / "PERCENT ON A 1440 PX" / "SCREEN", by Inter Bold's advance widths at 13 px with the label's tracking; not seen in a browser), where 0:00, 0:02, 0:50 and 1:00 take one. At 1440 px the two A21 frames then sit about two label lines lower than the frames beside them. The scale could print on its own line under the frame, or each grid row could give its labels one height. The plate's manifest note still says "shown at 10 percent" with no basis (notes do not print).
3. **Main session, for the board or a later editor turn:** E12b-1 under "Not fixed".
4. **Data visualization lead (3.5):** the four frame alts carry S04's rows; my check of them against `census-cps-reported-voting.csv` and `s04.json` passed (Tested), and the source line is the spec's, read from it.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| E12b-1 | Editor, chat 12b | `phase4_ch16_build.py`, `R['16.10']['frames']` (0:08, 0:30) and `R['16.12']['rows']`, `['transcript']`; plates `s-16-10-correct`, `s-16-12-correct` | The same video says different words at the same moments. At 0:08 the storyboard says "at 47.7 percent, down 3.7 points from 2020", and Rule 16.12's script and transcript say "at 47.7 percent in 2024, down 3.7 points from 2020, in the Census Bureau’s survey". At 0:30 the storyboard says "So the gap …" and "answers to a survey"; the script says "The gap …" and "answers to a Census survey". Rule 16.12 asks a transcript for every word spoken | Give the three rules one script: Rule 16.12's rows and transcript quote the storyboard's words, with the storyboard's 0:30 line naming the Census survey, so the source is said while the chart shows | It changes Rule 16.12's two plates and the said words under two storyboard frames, beyond this turn's items | Done in turn 2b, on the main session's message |
| E12b-2 | Editor, chat 12b | `s-16-10-correct`, the 0:08 and 0:30 cell labels | The longer scale words wrap to about three lines in a 200 px cell, so those frames sit lower than their row's other frames at 1440 px (estimate) | The scale on its own line under the frame, or labels of one height in each grid row | Layout, the design director's | Done in turn 2b, on the main session's message (one line of layout code, logged) |

## Bytes

Chapter files: `16-photography.json` 55,051 to 55,340 bytes; `20-web.json` 45,579 to 45,587; `21-atlas.json` 55,652 to 55,793. Chapter 16's 28 fragments 82,144 bytes after (the design director's 00:51 figure was 82,009 before).

In the built page, two strict builds to scratch inside one hold of the lock (01:14:27 to 01:15:05 UTC), the first with my 33 output files, the second with HEAD's versions of those 33 (written with `git show HEAD:…`), mine copied back after; an MD5 list of every file under `work/` before and after the pair matches line for line. Both read the same kit plates, so these figures are my outputs' share only; the kit's rebuild with my words moves A21's and the atlas frames again.

| Chapter | Before (HEAD's outputs) | After (mine) | Change |
|---|---|---|---|
| 16 | 276,828 | 277,712 | +884 |
| 20 | 860,267 | 860,755 | +488 |
| 21 | 1,276,951 | 1,278,063 | +1,112 |
| Page | 14,439,886 | 14,442,370 | +2,484 |

The page and chapter figures before equal the design director's 00:51 strict build. Chapters 20 and 21 were over their allocations before this turn and stay over (DR-271); nothing was cut.

## Tested

- `--page-words all` of all three generators before (01:07 UTC) and after, compared key by key by script: chapter 16, A21 only (six keys added: `safe_labels` ×4, `signature`, `switch`; the six `composed` entries gone; the four alts, the 0:30 lines and line 2 of the three 0:08 captions changed); chapter 20, nothing; chapter 21, three `frame_alts` (A11 ×2, A18 ×1).
- A21's alts against the words each frame prints: a Python port of `video-frame.mjs`'s `alt_misses` (its `norm`, `pct` and whole-word `carried`; the tick rule), run on the words read from `plates/a21.json` with the new caption lines: 0 missing in all four. A negative test (one rate and one caption word removed from a copy) reports both.
- The alts' figures against S04: each row's two rates read from `work/build/data/census-cps-reported-voting.csv` through `s04.json`'s `where`, the row words from its `labels`, the scale's ends from its `domain`, and its `source_line` whole: all match in all four alts. `--page-words` `source` equals the spec's `source_line`.
- The overlay's words against the renderer's own chip geometry (its formulas run in Python): the vertical basis wraps to three chip lines of a four-line room; "TikTok’s buttons" sits at x 176 to 512 of 576; the storyboard basis runs x 71 to 425 with 26 px before the top figure's chip at 450; "The player’s controls" x 745 to 956 of 960.
- Caption line widths at 32 px (Inter SemiBold advance widths, the system's copy): 0:08 lines 504 and 500 px (the misheard line 490) of the vertical frame's 660; 0:30 lines 746 and 408 px of the storyboard's 1,728.
- `--check` under the lock: chapter 16 at 01:10:46 and 01:12:41, chapter 20 at 01:10:54, chapter 21 at 01:11:24, and all three again at 01:13:34 UTC: exit 0 each (chapter 16: 13 rules, 28 specimens; 20: 11 rules, 24; 21: 16 rules, 35). Chapter 02's `check_copy` runs inside `page_words()` and the chapter checks.
- The plain runs under the lock: all three at 01:11:40 to 01:11:43 and again at 01:13:34 to 01:13:38 UTC, exit 0 each. An MD5 list of every file under `work/build` before and after each hold: the first moved the three chapter files, the two changed manifests and 28 specimens; the second only `16-photography.json` and `manifest-photography.json`. No kit plate, export or other owner's file moved.
- `git diff --stat` at 01:13:42 UTC: 36 files, the three generators and 33 of their outputs (`16-photography.json`, `20-web.json`, `21-atlas.json`, `manifest-photography.json`, `manifest-atlas.json`, `s-16-10-correct`, `s-16-11-correct`, `s-16-11-failure`, eight chapter 20 specimens and 17 chapter 21 specimens), 144 insertions, 79 deletions. A word diff of the outputs: 48 row labels gain "on a 1440 px screen" after "percent", 19 after "true size", two scale notes read "Shown", and the rest are the captions, alts, rows and WebVTT lines listed under Done. Untracked: this file and the data lead's notes.
- The two strict builds (Bytes): exit 1 each with the same 26 warnings, every one a kit plate older than its words: A21 ×4 (my words, and W's `video-frame.mjs` and `a21-video-s04.json`), A11 ×9, A13 ×7, A17 ×2, A18 ×3, A20 ×1. 409 rules in both. In the after page, each of `s-16-10-correct`, `s-16-11-correct` and `s-16-11-failure` keeps one "Illustrative" label and prints its new scale words.
- A script scan of every string this turn added (121 strings, 4,533 characters): em dashes 0, en dashes 0, fillers 0, corporate verbs 0, hedges 0, inflated adjectives 0, straight apostrophes 0, bare decision codes 0, "dark mode" 0. One "no", in "with no question pressed", a state. The "-tion" words are "caption" and our name.
- A full read of every changed string in the generators' diff, against chapter 02's rules.

Pattern violations remaining in my strings, by type: em dashes 0; en dashes 0; fillers 0; corporate verbs 0; hedges 0; inflated adjectives 0; corrective negation 0; straight apostrophes 0; bare codes 0. By hand: no rhetorical triplet ("with the chart, its source line and the captions" lists the frame's three parts), no setup and payoff, no slogan close. The four frame alts share one shape by design, since each is heard alone.

## Not tested

- The kit's own alt check, overlay and type checks on my words: they run when Engineer W builds A21; my port is not the kit.
- The overlay's words drawn: their places are computed from the renderer's formulas, not seen.
- Label wraps and widths in a browser: estimates from the system's Inter, not the guide's subset fonts. I opened no browser.
- Whether "a quarter" holds at 1024 and 360 px (Engineer W measured 1440 and 390).
- The atlas frames with my frame names (A11, A13, A17, A18, A20 wait for the kit).
- The guide check and its self-test, axe, screen readers, the guide's dark theme.
- How the words sound read aloud; my read for triplets, parallel runs and setup and payoff is by hand.

Turn 2 done, 01:18 UTC

# Turn 2b: E12b-1 and E12b-2

Started 01:19:44 UTC (`date -u`), on the main session's message, in `phase4_ch16_build.py`, which I still hold. Generator before: SHA-256 `f89d393503244a27…` (copied to scratch `t2b/`), the version the main session committed as `5c887bee` at 01:18:38 UTC; after: `4d4690f209ff4a05…`.

## Turn 2b routine calls

- D4-xxx | E12b-1: the words said at 0:08 and 0:30 sit once in the word fields (`SAID_0_08`, `SAID_0_30`), and Rule 16.10's storyboard and Rule 16.12's script and transcript take them from there; a check stops the generator if the 0:08 or 0:30 caption stops matching them | The same video now reads one way in three rules, and cannot drift apart again
- D4-xxx | The storyboard's 0:30 line names the survey: "These are answers to the Census Bureau’s survey, which run higher than counted ballots." (was "a survey") | With Rule 16.12's script quoting the storyboard, the old words would have left its correct plate saying no survey by name, which its own rule ("say whose source it is") and its failure caption ("never learns … in which survey") fault. The 0:30 caption shows the first sentence only, so A21's words do not move
- D4-xxx | Rule 16.12's script: row 1 says the storyboard's two 0:08 sentences, row 2 "So the gap …" with the On screen cell "Chart S04, still on screen." (was "The gap between the youngest and oldest groups, marked."), row 3 the survey sentence; the transcript's 0:08 line quotes the storyboard | S04 has no states, so the 0:30 frame draws the chart unmarked (DD12b-R1), and "marked" described a frame the plates no longer show. "In 2024" leaves row 1 and the transcript, since the storyboard asks about 2024 at 0:02
- D4-xxx | E12b-2: the storyboard states its scale once, in a label line over its cells, "The 0:08 and 0:30 frames, shown at 10 percent on a 1440 px screen" (`R['16.10']['frame_scale']`), and the 0:08 and 0:30 labels hold their times alone, as the other four do | CR-22: a row states its scale once. Layout, the smallest change, made because the design director has finished (D4-374's precedent): `frame()` drops the scale from the two labels, and `s16_10_correct()` adds one `<p class="lab sec">` after the Illustrative label. The line runs about 543 px on a 1440 px screen (Inter Bold advance widths at 13 px with the label's tracking), inside the plate

## Turn 2b done

- **E12b-1.** Rule 16.12's rows and transcript and Rule 16.10's 0:30 words, as above. Every figure is still S04's (47.7, 3.7, near 75, 23 to 27).
- **E12b-2.** The scale line over the storyboard; the cell labels read "0:08" and "0:30".
- Requests 2 and 3 of turn 2 are answered by these.

## Turn 2b tested

- `--page-words all` before (01:19 UTC) and after: byte for byte the same (`cmp`), so A21's words, and its plate, do not move.
- `--check` under the lock (01:20:45 UTC): exit 0, 13 rules, 28 specimens, 82,189 bytes. The plain run in the same hold: exit 0. An MD5 list of every file under `work/build` before and after the hold: only `s-16-10-correct.html` and `s-16-12-correct.html` moved; `16-photography.json` and the manifest did not.
- `git diff --stat` at 01:20:51 UTC against `5c887bee`: `phase4_ch16_build.py` (29 insertions, 22 deletions), `s-16-10-correct.html`, `s-16-12-correct.html`, and the data lead's notes, which are not mine. A word diff of the two plates shows only the scale line, the two labels, the 0:30 survey words and Rule 16.12's rows and transcript.
- A script scan of the strings this pass added (28 strings): em and en dashes 0, fillers 0, corporate verbs 0, hedges 0, straight apostrophes 0; one "no", in the generator's own stop message, not reader text.

## Turn 2b not tested

- The two plates in a browser: the line's width is a font-metric estimate, and the cells' level tops follow from equal one-line labels, not from a look. The guide check and a strict build were not run this pass.

Turn 2b done, 01:21 UTC

# Turn 2c: CD12b-S1, CD12b-R7 and CD12b-S3's words

Started 02:04:14 UTC (`date -u`), on the main session's message after the creative director's rescore (`20261124_Chat-12b-CD-Rescore.md`, Required changes), with its amendment to item 3 (D4-421: 37.5 px, not 40). Generators before, copied to scratch `t2c/` with their page words: `phase4_ch16_build.py` `4d4690f209ff4a05…`, `phase4_ch21_build.py` `d763681fc79e6547…` (equal to HEAD `8fd770f5`, the main session's snapshot); after: `c631a5fb7ce910ce…` and `deb47b1955fb8283…`.

## Turn 2c routine calls

- D4-xxx | CD12b-S1: Rule 16.11's correct caption and alt name the case, a platform that takes no caption file and draws no captions of its own, with the captions burned in from the checked WebVTT file and closed captions left off (D4-29) | The creative director's draft, recast in active voice ("We burned its captions in …")
- D4-xxx | The overlay's words stay ("TikTok’s and Instagram’s ad guides, retrieved November 21, 2026"; "TikTok’s buttons"), and the caption says why they appear: "Until chapter 23 sets each platform’s safe area, the frame keeps to the larger of TikTok’s and Instagram’s margins and clear of TikTok’s buttons." | The overlay names where the margins come from, not where the video posts, so with the caption it no longer reads as a TikTok or Instagram frame. CD12b-S2 keeps "TikTok’s buttons" in the overlay, and the frame's words (A21's page words) stay as the kit will draw them
- D4-xxx | CD12b-S3 as D4-421 sets it: Rule 16.11's Type row gives 37.5 px on a 43.125 px line in a 1080 by 1920 frame ("the type scale’s 20 px phone step and its 1.15 line height drawn 1.875 times, so a 390 px phone plays it at 13.5 px") and keeps 32 on 44 px for 1920 by 1080; the Lines row gives about 34 characters a line in a vertical frame and about 42 in a landscape one | The main session's amended call; the step and line height are h4's floor in `tokens.json` (1.25 rem, 1.15), as Engineer W's 02:06 note records; 37.5 × 390 / 1080 = 13.5
- D4-xxx | The WebVTT file's second cue rebreaks: "from 2020. Those 65 and over" / "stayed near 75 percent." (was "from 2020." / "Those 65 and over stayed near 75 percent.") | The captions are burned into the vertical frame from this file, and "Those 65 and over stayed near 75 percent." runs 41 characters, about 779 px at 37.5 px, past the 660 px column; the new lines run 28 and 23 characters (about 552 and 431 px), broken between a subject and its verb. The file's text still reads word for word as the storyboard's 0:08 speech (checked by script)
- D4-xxx | CD12b-R7: `s-21-15-correct`'s caption says "the chooser under it", and its alt "Under it, a chooser of reforms …" (both said "beside") | `s21_15_correct()` places the drawing's row, then the chooser's row, then the ratio table

## Turn 2c done

- **CD12b-S1.** Caption: "A vertical frame of chart S04 with its source line, at a quarter of 1080 by 1920, for a platform that takes no caption file and draws no captions of its own. We burned its captions in from the checked WebVTT file beside it, inside the caption-safe area on a Charcoal band, and left closed captions off. Until chapter 23 sets each platform’s safe area, the frame keeps to the larger of TikTok’s and Instagram’s margins and clear of TikTok’s buttons." (then the figures' line). Alt: opens "A vertical video frame at a quarter of 1080 by 1920, for a platform that takes no caption file and draws no captions of its own: …", says "two caption lines burned into the picture", and ends "Beside the frame, the checked WebVTT file the captions come from, with these two lines, the next two and their times."
- **CD12b-R7.** Rule 21.15's caption and alt, "under".
- **CD12b-S3's words.** Rule 16.11's Type and Lines rows. **The four A21 caption lines fit and none is rebroken:** at 37.5 px "Citizens 18 to 24 reported voting" (33 characters) runs about 590 px, "at 47.7 percent, down 3.7 points" (32) about 586 and the misheard "at 47.7 percent, down 37 points" (31) about 574, each inside the 660 px column. The one line rebroken is the WebVTT file's, which no A21 frame draws.
- **A21's `--page-words` output did not change** (chapters 16 and 21 compared byte for byte before and after with `cmp`), so this pass stales no kit plate.

## Turn 2c tested

- `--page-words all` of both generators before (02:05 UTC) and after: byte for byte the same.
- The WebVTT file's text, cue lines joined, against `SAID_0_08`: equal; its longest line 33 characters.
- Caption widths at 37.5 px: Inter SemiBold advance widths from the system's copy of Inter (`/usr/share/fonts/opentype/inter/`), not the guide's subset fonts. I tried to install the `brotli` module into scratch to read the guide's own WOFF2 files, and the session's permission check refused it; I did not retry. The figures are estimates, with 70 px or more to spare.
- `--check` under the lock (02:07:00 UTC): chapter 16 exit 0 (13 rules, 28 specimens, 82,189 bytes), chapter 21 exit 0 (16 rules, 35 specimens). The plain runs in the same hold: exit 0 each. MD5 of every file under `work/build` before and after: `16-photography.json`, `21-atlas.json`, the two manifests and `s-16-11-correct.html` moved, nothing else.
- `git diff --stat` at 02:07:03 UTC: 7 files, the two generators and those five outputs, 25 insertions and 20 deletions; a word diff shows only the changes above.

## Turn 2c not tested

- The captions at 37.5 px drawn in the frame: Engineer W's build and its checks, which I did not run.
- The guide's own fonts for the widths (above); a browser; the guide check; a strict build.
- CD12b-S2 is the design director's; its words (the failure plate's caption text box, the basis sentence moved into the caption) were not asked of me this pass.

Turn 2c done, 02:07 UTC

# Turn 2d: Rule 16.11's Type row for the landscape frames

On the main session's message (03:26 UTC): since D4-421's extension (built 02:14 UTC) the 1920 by 1080 frames' captions draw at 40 px on a 46 px line, so the Type row's landscape phrase reads "40 px on a 46 px line in a 1920 by 1080 frame, the same step drawn twice" (was "32 px on a 44 px line in a 1920 by 1080 frame").

Tested: `--page-words all` before and after, byte for byte the same (`cmp`); `--check` and the plain run under the lock (03:26:34 to 03:26:37 UTC), exit 0 each; MD5 of every file under `work/build` before and after the hold: only `16-photography.json` moved (its manifest did not). `git diff --stat` at 03:26 UTC shows `16-photography.json` alone, because the main session's snapshot `e6a8ddd9` (03:26:36) took the generator's one-line change; against `3ddc48a1` the change is the generator and that file. Not tested: the kit, a browser, the guide check.

Turn 2d done, 03:26 UTC
