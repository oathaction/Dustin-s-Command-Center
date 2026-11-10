# Stage B round 3: red team, craft and accessibility

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the craft and accessibility red team, run as a subagent of the main session under `20261110_Stage-B-Round-3-Brief.md`. I reviewed as the design director (`oa-design-director.md`), as a reviewer and not a maker, and checked every finding against the UX and accessibility lead (`oa-ux-accessibility-lead.md`). I read the brief, `CLAUDE.md`, both role files, Master Brief sections 3, 6, 10 to 12, 17 and 22, the stage B brief, the round 2 brief, the accessibility audit, and the round 2 notes of the identity designer, chapter 11's hand and the engineer. I skimmed the systems notes and the construction text for the rules I cite. I did not read the other reviewers' reports.

Page reviewed: the frozen copy `scratchpad/round-3/review/guide.html` (commit ddd3a898, D2-955), rendered in Chromium through Playwright. Reader check: `work/boards/phase-2/reader-check-2/20261110_Reader-Check-2.html`, wrapped in the same skeleton its own test uses. Captures and scripts are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/round-3/craft-access/`.

## Score

**4 of 5.** Chapters 09 to 12 are calm, consistent with 01 to 08 and accessible in practice: the pixel fits land on whole pixels at 1x, the five live components work by keyboard, in forced colors and under reduced motion, and nothing overflows at 320 px; what stands between them and the bar is one live specimen that teaches an unreadable pace, one correct plate that breaks its own chapter's target rule, and a run of composition faults a top studio would not let through.

## Must fix

**M1. Chapter 11, Rule 11.14, `s-11-14-correct`, the loop stepper: Play turns the step every 2.4 seconds, faster than anyone can read it.** Driven by keyboard at 1440, 390 and 360 px: after Play, the live text went from "Step 1 of 4" to "Step 3 of 4" in 5.2 seconds. Each step is 25 to 30 words, for example "Step 3 of 4: Electoral pressure lowers incumbent control of election rules. Officeholders who face little risk of losing can redraw maps and change election rules to protect their position." That takes 7 to 9 seconds to read, and a screen reader is still reading step 2 when step 4 lands in the polite live region. Pause and Reset work, so SC 2.2.2 passes, but the plate is labeled Correct application and a developer copying it builds a stepper whose Play mode cannot be read (Master Brief section 17: playback stays reader-controlled and explains a state). It does the same under `prefers-reduced-motion: reduce`. Fix: time each step from its words (about 250 ms a word, never under 6 seconds), or let Play stop at each step with Next step doing the turning; say the pace in the rule's specifications so a builder copies it. Owner: chapter 11 hand.

**M2. Chapter 11, Rule 11.12, `s-11-12-correct`, the library filter bar: the "Clear the search" button is 42 by 44 px, under Rule 11.7's 44.** It appears after a reader types; measured at 1440, 390 and 360 px it is 42 px wide. Rule 11.7 (DR-153) sets 44 px for every control that carries a utility icon, and the audit's table lists Close at 44 by 44, the clear control included. A correct application that breaks the chapter's own target rule teaches the fault, and the guide check missed it because the button is hidden when the check runs. Fix: 44 by 44 px, and have the check type into the field before it measures. Owners: chapter 11 hand (the button), engineer (the check).

## Should fix

**Chapter 11's live components**

**S1. `s-11-11-correct`, the reader toolbar: the page a reader turns to is hidden from screen readers.** The report page is a focusable group named "The report page" whose contents carry `aria-hidden="true"`, so a screen reader hears "The report page, group" and nothing of the visible page title, "Where the money comes from", which changes with each page. The status line says only "Page 2 of 12". SC 1.3.1. Fix: leave the page's header and title readable (hide only the grey text bars), or put the title in the status line: "Page 2 of 12: Where the money comes from". Owner: chapter 11 hand.

**S2. `s-11-12-correct`: the results list shows three rows under any count.** "120 of 124 symbols" sits over three rows, CL-001 to CL-003, with nothing saying the rest are left out, so the filter looks broken. Fix: end the list with "and 117 more" in words, or say "first three shown" in the caption. Owner: chapter 11 hand.

**S3. `s-11-menu`, the phone menu: Close scrolls away with the list.** With the rows open the dialog scrolls 1,268 px inside a 440 px frame, and the "In this chapter" bar with "Close the menu" scrolls off the top. Keyboard and Escape work (focus stays inside, every one of 24 Tab stops stayed in view, Escape and Close return focus to Menu, a link closes the dialog and lands on its rule's heading), but a thumb has to scroll back up to close. Fix: keep the dialog's header bar sticky. Owner: chapter 11 hand.

**S4. `s-11-16-correct`: the headline breaks inside a hyphenated word.** It reads "The House hears the all- / party primary bill on March 3". Master Brief section 6 asks for balanced headings with no widows; a compound split at a line end is the worst kind. The plate is fixed at 360 px, so it breaks this way on every screen. Fix: a non-breaking hyphen (U+2011) in "all-party", or `text-wrap: balance` with the compound kept whole. Owner: chapter 11 hand.

**Chapter 09**

**S5. Chapter 09's small plates do not fit a phone, while chapter 11's do.** `s-09-phone` ("The row on a phone", 406 px), `s-09-1-failure` (400), `s-09-3-failure` (400) and `s-09-4-failure` (406) scroll sideways by 42 to 48 px at 390 and by 72 to 78 px at 360. The plate that shows the phone column cannot be seen whole on a phone: at 390 its right edge is cut and the hint "Wider than this column. Scroll the frame sideways to see all of it." shows above it. Chapter 11's 360 px specimens fit at both widths. Fix: build these four at 358 or 360 px, as chapter 11 does, and let the 24 px inner margin collapse at phone width. Owner: identity designer.

**S6. `s-09-phone`: the downward arrows sit at ragged points.** In the stacked 48 px row each arrow follows its word, so they land at three different x positions ("Explain ↓", "Track ↓", "Connect ↓"), and the eye reads three loose marks instead of one flow. Fix: set the arrows in one column, centered under each icon between rows, or aligned to a common x after the longest word. Owner: identity designer.

**S7. Rule 09 and Rule 10.2 disagree about red in front of the reader.** Rule 10.2 reads "Build every drawing on one box, with one line, round ends and one red part", and its text says "One part carries the red accent". Chapter 09 shows Track at 48 and 128 px with two red pieces, the map pin and the magnifier's handle, and its own alt says "Track's icon keeps its red parts". The construction text explains that the accent is one group that may hold separate shapes (CL-015 and R-30 split theirs), but the page never says so. A producer reading 10.2 after 09 will think Track breaks the rule. Fix: word 10.2 as one red accent for one idea, which may be one shape or a few, and point to Track. Owners: editor (words), systems designer (chapter 10).

**Chapter 10**

**S8. Rule 10.7, `s-10-7-correct`: "Contact an official" breaks over three lines in the menu.** It reads "Contact / an / official", with "an" alone on a line, while the other four labels take one or two lines. Fix: let this item's cell take the width it needs, or break it "Contact / an official". Owner: systems designer.

**S9. The Illustrative label sits in two places across the makers.** Most plates put it at the head of the piece (`s-09-4-correct`, `s-11-11-correct`, `s-12-watermark-correct`). `s-10-4-correct` sets it after the headline's last word ("meeting minutes ILLUSTRATIVE"), and `s-01-21-correct` sets it after three headlines, one of them on its own line under "Oath & Action Report 3: How state committees record their votes". D2-440 asks for one label at the head of a wholly invented piece. Fix: head of the piece in `s-10-4-correct`; in `s-01-21-correct`, where real and invented headlines share a list, keep the label beside the item but hold it to one place, the end of the kicker line. Owners: systems designer (`s-10-4-correct`), editor (`s-01-21-correct`).

**Chapter 12**

**S10. Rule 12.2, `s-12-watermark-correct` and its failure: the crop leaves a stray square.** At the right edge of both panels the frame cuts the ampersand's arm, so a detached 15 px rectangle floats beside the bowl. Enlarged, it reads as a fault in the file, not a crop. Fix: move B so the edge cuts through a stroke the eye can follow, or clears the arm. Owner: identity designer.

**S11. Rule 12.4, `s-12-pattern-correct`: the hinge rules read as a ruled form, and the plate leaves a third of its frame empty.** Sixteen evenly spaced 1 px lines in a block look like lines to write on, which on a cover invites the wrong reading; the hinge arcs carry the identity, the rules do not. The two 360 px covers sit at the left of a 600 px frame. Fix: either draw the rules from the hinge (two weights, or the divider's rhythm with the hinge's 2 to 3 step) or keep only the arcs; set the plate at 360 px or put the two covers side by side. Design judgment. Owner: identity designer.

**S12. Rule 12.7, `s-12-locator-correct`: the state headline is set six lines deep in a 110 px column.** "Nebraska / has one / chamber, so / a bill's fifth / step never / comes" sits beside a tile map that takes more width than the words. Fix: put the map under the headline, or narrow it so the headline gets at least 200 px. Owner: systems designer.

**Changed parts of 01, 03, 08**

**S13. Chapter 03, `s-03-l6`: L6 cannot be seen whole on a 1440 px screen.** The plate is 932 px in a 771 px column; at 1440 the lockmark is cut off at the right and the plate scrolls, with no Fit to window (hidden, since fitting would set the tagline under 13 px). L6 centered on its strip, the change under review, is only visible after scrolling. Seen whole at 2,200 px, the wordmark and tagline block and the lockmark are both centered on the strip's height, within 1 px. Fix: let this plate break out of the text column to the page's full content width at 1280 px and up, where 932 px fits. Owners: engineer (the breakout), identity designer.

**S14. Chapter 08, `s-08-1-correct`: one master falls alone onto a second row.** Five items sit in the first row ("Display master, 96 px" to "On Charcoal"), and "On Prussian, all White" wraps alone under them. Fix: two rows of three, or narrow the gaps so all six share one row. The rebuilt masters themselves are crisp at 1x: each node and the lever draw as solid pixels at 48, 24 and 16 px. Owner: identity designer.

**S15. Chapter 01, `s-01-11-correct`: the source lines outweigh the finding.** Under four lines of finding, the plate prints two grey source paragraphs of 7 and 15 lines, run together without breaks. Every item belongs there; the setting makes them unreadable as sources. Fix: one source per line as a short list, with the method ("We counted each map by the party that led...") as its own paragraph after it. Owner: editor.

**The shell and the reader check**

**S16. Forced colors: the masthead wordmark turns link blue with a red ampersand.** At 390 px in Chromium's forced colors, "OATH" and "ACTION" draw in the system link color and the ampersand stays Pillar Red. The menu glyph is now the utility drawing and shows in forced colors, which fixes the audit's UX-1. Fix: give the wordmark one system color, or `forced-color-adjust: none` on an opaque ground, as chapter 03 sets for marks. Owner: engineer.

**S17. Text at 200 percent: the part navigation runs off the page at 1024 px.** With the root text size at 200 percent, `nav.partnav` measures 721 px and pushes the page to 1,467 px wide. Chapters 09 to 12 themselves do not overflow. SC 1.4.4. Fix: let the part links wrap. Owner: engineer.

**S18. Reader check: three faults a reader sees.** At 390 px, walked by keyboard:
- Step 4's card: the card is captured at 1200 px and shown 358 px wide, so its kicker "Explainer · Zoning" stands about 5 px tall and cannot be read, though the card is meant to be judged as a feed shows it. If the card's kicker is meant to be read in a feed, the card needs a larger kicker; if not, say nothing. Owner: identity designer, for `s-proofs-social`.
- The end screen's copy text shows machine strings to the reader: "Started: 2026-11-10T15:07:20.287Z", "Drawing 2 (r10)", "Least certain: step1". Fix: a plain date and time, no loop codes, "the first step". Owner: engineer.
- Step 7's sheet of twelve marks wraps 5, 2 and 5 at 390 px, with marks 6 and 7 alone on the middle row. Fix: a fixed grid of four columns. Owner: engineer.

## Questions for Dustin

**Q1. Five of the 41 symbols cleared for 24 px become one shape at 24 px.** At 1x, CL-023 Evidence, CL-028 Oversight and enforcement, R-08 Disclose the original funders of political spending, R-27 IRS enforcement of taxes already owed and R-45 Verifiable elections with paper records and audits each draw as a page with a magnifier, about 22 px wide. Side by side at true size they read as one shape; only the small check inside two of the lenses differs. Several of the 41 also draw mostly gray at 24 px: in eight (R-05, CL-004, CL-071, CL-023, R-15, R-14, CL-047, R-37) under a quarter of the visible ink pixels reach 3 to 1 on Newsprint, though every one has some ink above 3 to 1, which is the audit's own test (C-2). DR-136 settles the 41, so this needs your call. *Recommendation:* keep the 41, and add one line to Rule 10.9: at 24 px, never set two of these five in one view. The systems designer adds the five as a 24 px look-alike pair in `s-10-9-correct`.

## Tested

- **Captures, looked at myself.** Every specimen in chapters 09 to 12 captured at 1440 px, device scale 1 (91 plates and the chapter 09 opener); I looked at about 45 of them, every chapter 09 and 12 plate, chapter 10's 1, 2, 4, 5 to 10 and its list of 41 and first library sheet, chapter 11's five live components, its utility sheet and Rules 11.8, 11.9, 11.10 and 11.16. At 390 px: 13 plates and the chapter 09 head. At 1024 px: Rule 10.1 and `s-12-owner-correct`. Changed parts at 1440: `s-01-pillars`, `s-01-21-correct`, `s-01-11-correct`, `s-03-l6` (also whole at 2,200 px), `s-04-6-correct`, `s-08-1-correct`, `s-08-3-correct`. I did not look at `s-05-3-corrective`, which is on the fix list (D2-881).
- **Pixel fits.** Positions of every 16 and 24 px pillar icon, utility icon and end mark at 1440, 1024, 390 and 360 px, device scale 1 and 2. Every fit sits at a fractional CSS position (for example x 380.656), so I rendered the fits at whole and at fractional positions in one page: Chromium snaps them, and the pixels are identical. The four 24 px and four 16 px pillar fits render at 1x with no mid-tone pixels. The 24 px rows show the fits at 1x and the masters at 2x; 16 px shows the fit at both. The end mark draws its fit only at exactly 1x and the smooth mark at 1.5x and 2x; enlarged at 1x it sits on the baseline, crisp, a touch heavier than the text's stems. The enlarged views in `s-09-3-*` are pixelated images and stay square at 2x.
- **16 px utility icons at 1x**, enlarged six times: each 1.5 px line has one edge on a whole pixel and one half pixel of gray; Pause's insides read gray (D2-730, the creative director's).
- **Sprite against files.** All 106 sprite symbols rendered by `<use>` beside their files in `assets/utility`, `assets/pillar-icons/svg` and `assets/civic-line-v6/black`, compared pixel by pixel at 1x and 2x. Utility drawings differ only in ink color (the file's `currentColor` draws black in an `<img>`); topic, atlas and pillar drawings differ only in anti-aliased edge pixels (at most 123 of about 2,500 ink pixels). Shapes match.
- **Ink contrast of 157 glyphs of 30 px or less at 1x**, from rendered pixels against the sampled ground.
- **Keyboard through the five live components** at 1440 px, at 390 px with forced colors, and at 360 px with reduced motion: every Tab stop, Enter and Space, `aria-disabled` controls with their reasons, the status lines' text after each action, the dialog's focus trap, Escape and focus return, following a menu link, the form's focus to the first error, `aria-invalid` and `aria-describedby`, the red button stepping down to Charcoal and back, and the success line. No page errors. The guide shows no animation or transition in chapters 09 to 12 or the masthead under either motion setting.
- **Focus through chapters 09 to 12**: 360 Tab stops at 1440, 340 at 390, 340 at 390 in forced colors; every stop had a 2 px outline; none sat hidden under the masthead except five scroll frames taller than the screen, which stay partly in view.
- **Forced colors**: three plates, Rule 09.1's text and the masthead at 390 and 1440. Specimens keep their colors; the shell takes system colors.
- **Reflow** at 320, 360 and 390 px over chapters 01, 03, 04, 05, 08 and 09 to 12: no page overflow; frames that need sideways scroll listed at 360 and 390. Text at 200 percent of the root size at 1024 px.
- **Text contrast and size** from computed colors in chapters 09 to 12 at 1440: two hits, both deliberate faults in failure plates.
- **Red under 48 px** on every glyph in the page: none outside a construction drawing whose box is 40 by 48 px.
- **The masthead menu**: the glyph at 390 and 360, normal and forced colors; opened with Enter, closed with Escape, focus back on Menu.
- **Reader check**: walked by keyboard from the welcome screen to "Thank you" at 390 and 320 px, 91 screens, with time scaled to a tenth and no `window.claude` (the copy mode); every timed look starts from a reader's press, focus lands on each new screen's heading, no sideways scroll, no page errors. I read its reduced motion rule (the clock bar hides; the words count down).

## Not tested

- Screen readers (VoiceOver, NVDA, TalkBack) and voice control; my screen reader findings come from the markup and Playwright's accessibility snapshot.
- Real phones, real 1.5x and 3x screens, Safari and Firefox; the 1x and 2x switches ran in Chromium only. Windows High Contrast itself; only Chromium's forced colors emulation.
- Browser page zoom at 200 percent; I raised the root text size instead.
- Print, grayscale captures and the dark color scheme.
- The reader check in real time, at 2x, in its saved mode with `window.claude`, and under emulated reduced motion.
- Every plate at 1024 and 360 px by eye; I looked at a sample and scanned the rest by script.
- Words, facts and sources: the editor's and the research lead's lanes.

## Change log

- Created: `work/handoffs/phase-2/20261110_Stage-B-Round-3-Red-Team-Craft-Access.md` (this report).
- Scratch only: scripts and captures in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/round-3/craft-access/`.
- No other file changed.
