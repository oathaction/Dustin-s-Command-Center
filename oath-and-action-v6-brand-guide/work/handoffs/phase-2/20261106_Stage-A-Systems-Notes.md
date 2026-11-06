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
