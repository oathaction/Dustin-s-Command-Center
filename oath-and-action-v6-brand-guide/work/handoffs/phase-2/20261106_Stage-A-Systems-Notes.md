# Stage A, systems designer: chapters 05 Color, 06 Type and 07 Layout and spacing

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the systems designer (`oa-design-director`, with the checks in `oa-ux-accessibility-lead`) under `work/handoffs/phase-2/20261106_Stage-A-Brief.md`.

## What I built

Three chapters as finished guide pages, in the content contract: 23 rules and 51 specimens.

| Chapter | Rules | Specimens | Extras |
|---|---|---|---|
| 05 Color | 7 (05.1 to 05.7) | 19, one corrective | Palette sheet; roles on each surface; the ask on four surfaces; every palette pair, measured |
| 06 Type | 10 (06.1 to 06.10) | 20 | None; the type scale is 06.2's correct application |
| 07 Layout and spacing | 6 (07.1 to 07.6) | 12 | None |

- **05 Color.** 05.1 Newsprint covers most of every page; 05.2 text sits only on pairs that pass; 05.3 one working red per view, quoted word for word as D2-01 with DR-66's sentence (the build checks it against `redRule` in `tokens.json`); 05.4 every state shows a word or a shape; 05.5 marks pass 3 to 1 and red on Newsprint takes a Charcoal keyline; 05.6 bounded tints with one job each (V5's "There are no tints." retires); 05.7 charts and the atlas on Newsprint with diverging pair B, summarized and pointing to chapter 14. The roles table is tension 9's text-safe and graphic-safe roles per surface; 05.3's corrective resolves tension 14 (an error takes the red and the ask steps down to Charcoal).
- **06 Type.** Faces and their jobs; the fourteen-style scale in rem; the 13 px floor with labels at 13 px and 6 percent (tension 1); tracking by size; tabular figures and the true minus; balanced headings; hanging punctuation; measure in characters; the email system stack; load the faces and never substitute (V5's list carried forward).
- **07 Layout and spacing.** The 8 px scale; column grids at 1440, 1024, 768, 390 and 360 px; body spans that hold the measure; heading proximity and section rhythm; breakpoints in em; reflow at 320 px.

Every specimen is live HTML in tokens; none is an image. Failure cases are labeled and exempt only where they fail by design (`check_exempt`: four contrast, one red, one size). Invented content carries the Illustrative label. Real data: the payroll-by-sector series (FRED copies of BLS) from the shared chart data, with its full source line.

**Every figure is measured.** Contrast, OKLab and color-vision figures are computed from `tokens.json` (version 6.0.0-gate2.1) by my own scripts; characters per line, color shares, word spaces, heading widths and the quote mark's hang come from a Chromium render with the Google Fonts files the page loads. All 165 printed figures and their methods are in `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json`.

To rebuild: `stage_a_systems_build.py probe --out-dir <scratch>`, then `node stage_a_systems_capture.js <scratch>`, then `stage_a_systems_build.py final --out-dir <scratch>` (all in `work/build/scripts/phase-2/`).

## Findings for the engineer and the main session

1. **The body measure token renders shorter than its description.** `oa.layout.measure.bodyIdeal` (33.88 rem) says "68 characters". Rendered in Chromium with Google Fonts Inter at 17 px, it gives 63 to 67 characters on the W07 paragraph and averages 64 over 7,041 characters of chapter 02's prose; `bodyMax` (37.37 rem) averages 71. Both sit inside 60 to 75, so I print the measured figures and leave the token alone. See question 2.
2. **Shell classes reach into specimens.** `@scope` keeps a specimen's styles in, but the shell's class styles still apply inside it: my phone mock's `.menu` took the shell menu's `height: 100vh`. I now prefix every class in my fragments with `sx-` at build time. The other makers may want the same, and the shell notes could warn about it.
3. **Fluid specimens touch the screen edge on phones**, since the mat has no side padding below 48em. Mine add a 16 px inset of their own below 48em.
4. **Tokens used:** the specimens' styles reference 139 token paths, all found in `tokens.css` (a missing name stops my build), and every token chip and specification in the three chapter files resolved in `guide_build.py` with no warning.

## Routine calls, as proposed decision lines

- D2-xxx | Rule 05.3's `rule` field holds the full wording as D2-01 and DR-66 give it, past the contract's one to three sentences | The rule binds every page and must be quoted exactly
- D2-xxx | Rule IDs 05.1 to 05.4 keep the Gate 1 wireframe's subjects (Newsprint leads, pairs that pass, one working red, state cues); 05.5 to 05.7 are new | Links and citations made since Gate 1 still land
- D2-xxx | Rule 05.1 sets firm limits per view (Newsprint 60 to 85 percent, one dark panel per section, red within 5 percent) and keeps V5's other shares as the balance across a body of work | Measured on one phone page, no view can hold all seven colors inside their V5 ranges; Verdigris may be absent
- D2-xxx | Color shares are measured by assigning each rendered pixel to its nearest palette color, with Deep Stone counted as Stone and Dim Newsprint as Newsprint | A repeatable measure of area; type counts as ink, so Charcoal reads low (4 percent) when the dark panel is Prussian
- D2-xxx | Failure cases are live HTML with `check_exempt`, never images | The shell supports it, failures stay sharp at 2x, and the check lists each exemption
- D2-xxx | Every class in my fragments is prefixed `sx-` at build time | Shell class names (`.menu`) leaked into a specimen
- D2-xxx | The phone mock in 05.1 and 05.3 carries a hinge divider between the article and its dates, in Charcoal | It shows the divider's ink in an application; the shell notes ask makers not to draw it to separate guide blocks, which this does not do. The identity designer may prefer it out
- D2-xxx | Hex values printed as text in specimens are written `&#35;DCD9D2` | They render the same and do not trip the literal-color check meant for styles
- D2-xxx | Display sizes in a phone mock use the style's phone size (the clamp's floor), such as H3 at 1.625 rem | A phone page at true size shows what a phone reader sees, whatever the guide reader's window
- D2-xxx | 06.6's widow is set with a line break, so it shows at every window width | Ordinary wrapping produces it only at some widths; the specimen notes say so
- D2-xxx | 06.2's failure draws both columns at the sizes a 200 percent text setting produces | The guide page runs at the reader's own setting, so it cannot show the failure live
- D2-xxx | Body spans picked by measurement: 5 of 12 at 1440 px, 7 of 12 at 1024 px, 6 of 8 at 768 px, all 4 on phones | Each span's measured mean sits nearest 68 within 60 to 75
- D2-xxx | Section rhythm in 07.4 matches the shell: 80 px between rules, 32 px above a label and 8 px below, 16 px between paragraphs | The guide follows its own rule
- D2-xxx | Chapter 05's chart summary shows Newsprint tokens only | Pair B exists on Newsprint only; the dark ground belongs to chapter 14

## Open questions for Dustin

1. **Rule 05.1's shares.** Our fifth edition gave every color a share of a composition (Newsprint 60 to 85 percent, Charcoal 10 to 25 and so on). Measured on a real view, a phone page can meet Newsprint's range but not every other range at once. *Recommendation:* make Newsprint's range, one dark panel per section and red within 5 percent the firm rule for each view, and keep the other shares as the balance across a body of work, as the chapter now does.
2. **The body measure token.** It promises 68 characters and renders about 64 to 66. *Recommendation:* keep the value, which sits inside 60 to 75 and matches what the page already uses, and have the engineer change the token's description to "about 65 characters of 17 px Inter, measured in Chromium" at the next token release.

## Tested

- `stage_a_systems_build.py final`: every specimen fragment passes its own checks (no heading elements, no em or en dash, no literal color, no px font size), every chapter string passes the copy check (no em or en dash, no straight quotes outside code, no listed fillers or corporate verbs), and every specimen named by a chapter exists and is used once.
- Rule 05.3's wording matches `redRule` in `tokens.json` character for character, apostrophes aside.
- `guide_build.py --out` to my scratchpad with all eight chapters present: 0 warnings.
- `guide_check.js` on that page at 1440, 1024, 390 and 360 px: PASS, 0 failures, axe-core 4.10.2 with no violations, no sideways scroll, every red mark under `data-red`, no red on Prussian. My exemptions are listed in its results.
- My chapters by eye: every plate captured at 1440 px and every plate at 390 px, after fixing the faults those captures showed (the `.menu` collision, the compound selector in the corrective, the clipped 8 px label, the share bar's edge, the scale sheet's missing size ranges, the quote's guide line, the edge-to-edge text on phones).
- The CSS Color 4 just-noticeable difference (0.02 in OKLCh), read from https://www.w3.org/TR/css-color-4/ on November 6, 2026.

## Not tested

- `dataviz_check.js --board`: the engineer's notes make `guide_check.js` the guide's check, and `dataviz_check.js` has no exemptions, so it would fail on every labeled failure plate by design.
- Screen readers by ear, Safari, Firefox, real phones, print, forced colors, 200 percent text zoom on the rendered page (07.5's layout table is worked out from the em breakpoints, not rendered at 200 percent), and keyboard order through my plates beyond the check's first 60 Tab stops.
- Arial, Helvetica and Georgia themselves: this container renders them as Liberation Sans and DejaVu Serif. Liberation Sans matches Arial's widths, so 06.10's width figures hold; the letterforms on screen differ.
- Color-vision figures rest on the Machado simulation, not on readers with color-vision deficiency.
- The 1024 and 768 px views of my chapters by eye (the check covered 1024 px).
- No red team, reader panel or creative director has seen these chapters yet.

## Change log

Created:
- `work/build/guide/chapters/05-color.json`, `06-type.json`, `07-layout.json`
- `work/build/guide/specimens/`: 51 fragments (`s-05-*.html`, `s-06-*.html`, `s-07-*.html`) and `manifest-systems.json`
- `work/build/scripts/phase-2/stage_a_systems_build.py`, `stage_a_systems_core.py`, `stage_a_systems_ch05.py`, `stage_a_systems_ch06.py`, `stage_a_systems_ch07.py`, `stage_a_systems_capture.js`
- `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json`
- `work/handoffs/phase-2/20261106_Stage-A-Systems-Notes.md` (this file)

Modified: none. I read `tokens.json`, `tokens.css`, the token source, the shell, the identity masters and the shared chart data, and edited none of them. Preview builds, probe pages and captures went to my session scratchpad, not to `work/boards/`. Nothing committed or pushed.

## Fix pass

Round one of `work/handoffs/phase-2/20261106_Stage-A-Fix-Pass-Brief.md`, systems designer, November 6, 2026. Every change is in my build scripts; the chapter files, fragments, manifest and measurement record are their output. The container restarted partway through; my edits survived on disk, and I resumed from them.

### Each item and what I did

- **BE-M5, CP-M1 (codes and internal names).** Every Basis line in chapters 05 to 07 now gives its reason in words: "Design judgment", "Our locked identity rules; design judgment", "Design judgment; our measurements of the fifth edition, October 2026", "Our measurements, November 2026; design judgment", "Design judgment; Rules 01.1 and 01.3" and the WCAG criteria. Gone from reader text and alt text: D2-01, DR-66, D1-04, DR-47, DR-48, DR-53, DR-54, DR-58, T-9, "Master Brief", "Phase 4" and "W07". The palette caption says the hex values are "locked in our identity rules".
- **BE-S4.** Rule 05.7's failure stage opens with a Charcoal band, "× Failure case: do not publish", in Newsprint label type, and its alt text says so.
- **BE-S5.** I took the second option the reviewer offered: the "What happens next" panel in 05.1 and 05.3 is now Charcoal, and 24 px of Newsprint part it from the red button. The hinge divider stays between the article and the dates, where Rule 04.4 puts it.
- **BE-S10.** Rule 06.2 now says "when our audit doubled its root text size, no text on the page grew", so the only count left is Rule 06.3's, which says what it counted: 2,346 text elements rendered at 1440 px, text inside SVG drawings left out.
- **AX-S2.** `readable: true` on the seven static tables and lists (`s-05-palette`, `s-05-roles`, `s-05-pairs`, `s-05-6-correct`, `s-06-2-correct`, `s-06-5-correct`, `s-07-5-correct`) and on the two new ones (`s-06-artboards`, `s-07-spans`); none carries `interactive` now. Every extra has a plate label ("The seven colors", "Color roles on each surface", "The ask on four surfaces", "Every palette pair, measured", "Sizes for fixed artboards", "Body span at each width"). Swatches and "Aa" samples inside them are hidden from assistive technology.
- **AX-S14.** Rule 05.7's alt text and specifications carry every measured ratio: the four roles, the five label ratios on the diverging scale (13.28, 6.18, 11.76, 8.01, 7.06 to 1) and the five on sequential Verdigris (10.96, 7.81, 5.41, 5.20, 8.27 to 1).
- **C-M2.** The phone pages in 05.1 and 05.3 draw the hinge divider as DR-96 sets it: B's 24 px master at 24 px, centered on a 1 px line as wide as the 328 px text block, 12 px clear on each side, Charcoal, 24 px above and below.
- **C-M3.** Rule 06.4 now reads every tracking value from `tokens.json` (title −3, section −2.5, H3 −1, H4 −0.5, figure −3 as the engineer set it, quote −2, label +6) and the build stops if the four DR-95 values are missing. I re-measured both plates at the new values and moved them from H4 at 24 px to H3 at 32 px, where the craft review found the fusing. I added a measurement of letters that touch (canvas at twice size, with kerning; a pair touches when no white device pixel separates the two glyphs). Results: the plate heading, 1 of 28 pairs at −1 percent ("ro") and 4 at −3 percent; word space 5.7 px against 5.0 px. The tagline at 110 px, 2 of 24 at −3 percent ("ry", "rs", the craft review's own result) and 7 at our fifth edition's −4.5 percent. The 23 rule titles of chapters 05 to 07 at 32 px, 32 of 738 at −1 percent, 107 at −3 percent and 4 at the font's own spacing.
- **C-M7, D2-254.** Rule 06.2 states the fixed-artboard sizes in its rule and specifications, and a new readable table after it, "Sizes for fixed artboards", prints each style on a web page, up to 600 px and from 1,200 px, read from `tokens.json` and checked against D2-254's list in the build. Print reads "Points, with all text at 10 pt or larger; chapter 25 sets the point scale". My own specimens follow it: fixed widths up to 600 px take the floor, and sheets that flow with the page show the floor on phones and the ceiling from 48em. The email in 06.9 moved from 28 and 22 px to 26 and 24 px. Off-scale sizes remain only in three labeled failures, each with `check_exempt: "scale"` and its reason in `notes`.
- **C-S6.** The grids in 07.2 and 07.3 carry `scale: 0.25` on a 360 px stage and print "One quarter size". 07.3's correct plate is now the quarter-size drawing alone, and its table moved to the readable extra `s-07-spans`. The two charts in 05.5 carry `width_px: 600`.
- **C-S15.** All 23 rule titles are instructions ("Cover most of every view in Newsprint.", "Tighten tracking only as headings grow.", "Set breakpoints in em, so larger text gets fewer columns.").
- **CP-S8.** "Eyebrows" is now "kickers" in 06.3, and the failure plate labels V5's "06 / Type" as a kicker.
- **CP-S9.** Chapter 07's intro defines breakpoints, Rule 07.5 defines breakpoint and em, Rule 05.2 defines Dim Newsprint at its first use, and "diverging pair B" is now "the diverging scale, which runs from Prussian through a pale middle to Verdigris". The intro defines a view and the token values; Rule 05.3 defines a keyline.
- **CP-S10.** In my own prose I removed the contrasting pairs built on "while" (05 intro, 05.5, 07.3), the matched halves in 06.2, 06.4 and 06.7, the corrective "never" turns in 05.6, 05.7 and 07.4 builders, the colon reveals in 05.1, 06.9 and 06.10, and the landing line in 05.1's failure caption.
- **CP-S12.** Rule 05.7 now says when the named series stays Charcoal and when one point takes the working red with its keyline, as in Rule 05.5.
- **CP-S13.** "Scorecards" is out of Rule 06.5.
- **CP-S15.** Rule 05.7's why leads with the plain reason; the OKLab distances and lightness moved to Specifications, and the failure caption names "Rules 01.1 and 01.3".
- **D2-248.** Rules 06.8 and 07.5 show the first paragraph of chapter 02's writing section, real copy with no unexplained term. Column spans are now measured over 7,041 characters of chapter 02's prose, which moved two picks: 1024 px stays seven of 12 (64 characters), 768 px goes from six to seven of eight (73).
- **RP-M1, D2-250.** Kickers: "Explainer · Local schools", "Explainer · Local budgets", "Explainer · Local utilities", "Explainer · Primaries", "Tracker · State bills", "Tracker · City council". "Finding" stays above the chart and the table (D2-249).
- **DR-97, C-S8.** My plain "Illustrative: ..." lines are gone. Each invented piece carries one `<span class="illus">Illustrative</span>` at its head, unstyled by me.
- **AX-S8.** No landmark or sectioning element in any fragment; my build now refuses one.

### Declined or changed

- BE-S5: I chose the Charcoal panel over moving the hinge, because Rule 04.4 places the divider between the explanation and what a reader can do, and moving it under the dates would have broken that rule.
- C-S6: reference sheets and tables (palette, roles, pairs, tints, scale, states, the faces, single headings) keep no `width_px`, since they are guide content the shell should flow. Their display type still lands only on the scale's two fixed sizes.
- C-M3: the plates now show H3 at 32 px in place of H4 at 24 px, as above. The failure is the H3 value this guide's first draft used, which is the "before" DR-95 asks to see.

### Routine calls, as proposed decision lines

- D2-xxx | An artboard between 600 and 1,200 px wide takes each style's size from either column of Rule 06.2 | D2-254 names no size for that band; the engineer's check accepts either set there
- D2-xxx | A specimen sheet with no fixed width shows each display style at its phone floor below 48em and its desktop ceiling from 48em | Every size a reader sees in a specimen is then one D2-254 names
- D2-xxx | Rule 05.1's and 05.3's phone page puts its dates on a Charcoal panel | Keeps the red ask clear of Prussian (BE-S5) and keeps the hinge where Rule 04.4 puts it
- D2-xxx | Rule 06.4's plates show an H3 at 32 px at −1 percent against −3 percent, with word spaces and touching letter pairs measured | The fusing DR-95 fixes showed most at H3; −3 percent is the guide's own earlier value
- D2-xxx | Letters touch when no white device pixel separates their ink at twice size, on canvas with kerning | Repeats the craft review's tagline result (2 of 24 at −3 percent)
- D2-xxx | Rule 07.3's table moves to its own readable extra, and its correct plate is the quarter-size drawing | A plate can carry one scale
- D2-xxx | Column spans are measured over chapter 02's prose (7,041 characters), and plates show chapter 02's opening paragraph | D2-248 retires W07's paragraph as sample text, and a longer sample steadies the averages
- D2-xxx | A failure plate that could be mistaken for our work carries a Charcoal "Failure case: do not publish" band at the top of its stage | BE-S4; the editor may want the same form in 01.2, 01.3 and 01.5

### Questions for Dustin

None. Both open questions from stage A (Rule 05.1's shares and the body measure token) stand as written above.

### Tested

- `stage_a_systems_build.py probe`, `stage_a_systems_capture.js` and `stage_a_systems_build.py final` on `tokens.json` after the engineer's DR-95 change: 23 rules, 53 specimens, 172 figures recorded, every fragment through my own checks (no heading, landmark or sectioning element, no dash, no literal color, no px font size, a reason in `notes` for every scale exemption).
- `python3 -I work/build/scripts/phase-2/guide_build.py`: 0 warnings.
- `node work/build/scripts/phase-2/guide_check.js` on the page at 1440, 1024, 390 and 360 px: no failure in chapters 05 to 07 in any run. The last run reports FAIL for decision codes and studio words in chapters 03, 04 and 08, which other makers own; an earlier run's only failure was 11.88 px text in `s-01-5-correct`. The new type-scale and landmark checks pass my specimens.
- My own scripted check of the built page at 1440, 1024 and 390 px: every font size in my 53 specimens is one D2-254 allows for that specimen's width; no landmark inside my stages; no decision code, "Master Brief", "Phase", "Gate", "the studio", "V5", "eyebrow" or dash in the rendered text or alt text of chapters 05 to 07, apart from the repository path `work/boards/phase-2/...` in two Files lists.
- The font link in Rule 06.1 and the minus note in Rule 06.5 render `&family=` and `&minus;` once.
- My nine readable stages render as groups named "<label>, specimen"; the 07.2 and 07.3 grids print "One quarter size".
- Rule 05.3's text still matches `redRule` in `tokens.json`.
- By eye: every plate of chapters 05 to 07 captured at 1440 and 390 px at twice size, plus viewport captures at both widths of the phone page, the scale sheet, the artboard and roles tables, the chart palette and Rule 06.4. Faults found and fixed: the artboard table's headers broke inside "600 px", "one of 28 pairs touch", the share bar ran to the stage edge at 390 px, and "Pillar Red 3" had no unit.

### Not tested

- Screen readers by ear, Safari and Firefox. The display sizes in my sheets rely on custom properties set on `:scope` inside the shell's `@scope` wrapper with a nested `@media`; I saw them work in Chromium only. Without them, a sheet falls back to each style's phone floor.
- The touching-pair method in any engine but Chromium's canvas, or against printed type; the count depends on the ink threshold (alpha above 96 of 255 at twice size).
- The 1024 and 360 px views of my chapters by eye; the scripted size check covered 1024 px and the guide check covered both.
- Real phones, forced colors, 200 percent text on the rendered page, print.
- No red team or reader has seen the fixed chapters.

### Follow-up: Rule 07.6's scrolling frame

From the creative director's review (`work/handoffs/phase-2/20261106_CD-Review-Of-Stage-A.md`, ruling 2). Rule 07.6 taught `role="region"` for a frame that scrolls, and the shell now draws each such frame as a group named for its plate, focusable only while it overflows (AX-S3; shell notes, section 9). Rule 07.6 now teaches the same pattern:

- The rule: content that needs two dimensions scrolls sideways inside its own frame, "a group named for what it holds", which takes keyboard focus only while its content overflows.
- Specifications: three new rows, "A frame that scrolls" (a group named for what it holds, such as the table's title), "Keyboard focus" (only while the content overflows, checked on load and on resize) and "Scroll cue" (a line above the frame saying it scrolls sideways, where the shell puts its hint).
- For builders: the review's wording, with the markup: `role="group"` and an `aria-label` such as "Contrast pairs, scroll sideways", and `tabindex="0"`, while `scrollWidth > clientWidth`, and neither once the content fits.
- The correct caption adds that a table which must keep its columns scrolls in a named frame, as the guide's wide plates do on a phone. The two specimens are pictures inside image stages, so they hold no focusable frame of their own.

Tested: `stage_a_systems_build.py final`; `python3 -I work/build/scripts/phase-2/guide_build.py --strict`, exit 0 with 0 warnings; `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, PASS at 1440, 1024, 390 and 360 px with 0 failures; Rule 07.6's rendered text read at 1440 px, with no `role="region"` left in my chapters. Not tested: a screen reader on the new wording, and the CD review's blocking item B1 (specimens touching the new keyline), which it assigns to the shell's CSS.

### Change log

Modified:
- `work/build/scripts/phase-2/stage_a_systems_build.py`, `stage_a_systems_ch05.py`, `stage_a_systems_ch06.py`, `stage_a_systems_ch07.py`, `stage_a_systems_capture.js` (`stage_a_systems_core.py` unchanged)
- `work/build/guide/chapters/05-color.json`, `06-type.json`, `07-layout.json` (written by the build)
- `work/build/guide/specimens/s-05-*.html`, `s-06-*.html`, `s-07-*.html` and `manifest-systems.json` (written by the build)
- `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json` (written by the build)
- `work/handoffs/phase-2/20261106_Stage-A-Systems-Notes.md` (this section)
- `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report and check results, regenerated by the shared build and check as the brief asks

Created:
- `work/build/guide/specimens/s-06-artboards.html`, `s-07-spans.html` (by the build)

Probe pages, captures and scratch checks are in my session scratchpad. Nothing committed or pushed.
