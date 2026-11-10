# Stage B round 2: chapter 11, systems designer's notes

Oath & Action Edition 06, Phase 2, stage B round 2, November 10, 2026. Written by chapter 11's systems designer (`oa-design-director`, checked against `oa-ux-accessibility-lead`), run as a subagent of the main session under D2-720 and `20261110_Stage-B-Round-2-Brief.md` ("Chapter 11"). Chapter 10's maker keeps `20261110_Stage-B-Round-2-Systems-Notes.md`; the main session asked for chapter 11's notes in this file. I committed nothing and published nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: built and checked. The editor's first-pass table for chapter 11 (editor's notes, section 4d, 12 rows) is applied in full. The editor still means to read the specimens' alts and the final text.

## For other owners, first

**Renumbered bills (DR-151), one map for chapters 08 and 11.** One counter from H.99001 and S.99002 up, in the order chapter 11 first shows each bill. Chapter 08's `s-08-3-*` already carries S.99002 (identity designer, commit e1b227be).

| Old number | Title | New number |
|---|---|---|
| H.4212 | Public meeting notice | H.99001 |
| S.0876 | School bus contracts | S.99002 |
| H.1180 | Library hours | H.99003 |
| H.3301 | Records request fees | H.99004 |
| S.2045 | Parking meter fees | S.99005 |
| S.1517 | Snow route parking | S.99006 |
| S.0412 | Town audit deadlines | S.99007 |
| (new) | Rural clinic grants, a Nebraska bill (DR-150) | LB 99008 |
| (new) | All-party primaries, Rule 11.16's view | H.99009 |
| H.R. 99012 | Passport wait times | unchanged (D2-427) |

Invented records requests and agency rules take numbers from 99001 up ("Request 99001", "Rule 99002") and name no agency.

**Chapter 01's H.R. 7008 card** draws its steps with this module (D2-408). The functions it calls keep their signatures (`steps_svg`, `key`, `piece_css`, `mark_vars`, `status_words`, `names`, `MARK_CSS`, `STATE_ORDER`), and `piece_css` still holds `MARK_CSS` once, so its split works. On its next rebuild the card picks up the status tags, the token classes and 13 px numbers from CSS. I checked by import that `track_css()` and `track_steps()` still run.

## What I built

Chapter 11 now runs in four groups and 16 rules, with 37 specimens (5 of them live components), from `work/build/scripts/phase-2/apply_systems_ch11.py` and a new module beside it, `apply_systems_ch11_ui.py`.

**Group 1, Trackers (Rules 11.1 to 11.7), kept.**
- Every invented state bill renumbered (table above).
- Rule 11.1 adds a Nebraska bill to its correct plate: six steps, step 5 under DR-108's slash, and "Nebraska has one chamber." as the first words of its status line, beside the marks (DR-150). The rule text, specifications and the steps table say the same, and the builders note gives the three number ranges.
- Rule 11.7 now reads DR-153: 44 px for every link and button in a tracker and every control that carries a utility icon; a plain list of text links keeps WCAG's 24 px through spacing.
- Every mark carries `data-icon` (`S-done`, `S-now`, `S-take-part`, `S-not-yet`, `S-never-happened`, `S-stopped`) and `data-icon-family="status"` (D2-517).
- `MARK_CSS` writes every mark width as `var(--oa-component-mark-...)`, by class (the engineer's request). Rules 11.2, 11.4 and 11.5 cite the mark tokens in their chips and specifications.

**Group 2, Records requests and agency rules (Rules 11.8 to 11.10), new (DR-140, D2-526 to D2-529).**
- 11.8: a records request in six steps (Requested, Acknowledged, Searching, Reviewing, Answered, Appeal), end words with their date, "Withdrawn by the requester". Failure: the government's "Full denial" category on a withdrawn request.
- 11.9: a federal agency rule in six steps (Early notice, Proposed, Comments open, Comments closed, Final rule, In effect), the take-part mark on Comments open, slashes for a rule issued without advance comment. Failure: that rule drawn with steps 2 to 4 filled.
- 11.10: waits and later steps in words, the count kept at six, and the dated check under the warning mark. Failure: a fee estimate drawn as a seventh step.

**Group 3, Utility icons (Rules 11.11 to 11.14), new (DR-161 to DR-178, DR-154, D2-506 to D2-515).** Every icon is drawn from the sprite with the engineer's pattern, `<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="U-<name>" data-icon-family="utility"><use href="#oa-sym-u-<name>-24px"/></svg>`, turned or mirrored on the `<use>` with the manifest's transforms.
- 11.11, beside the word at 24 px and inside a line at 16 px; share, zoom, print and information stay words. Correct: the report reader toolbar, live. Failure: glyph-only 32 px buttons with a name shown on hover. Extra: the 18 icons at 24 and 16 px with their words.
- 11.12, one drawing, one meaning. Correct: the library filter bar, live. Failure: a chevron that turns pages and opens a row in one view. Extra: the phone menu, live.
- 11.13, a link to another site, same tab, mark after the last word, hidden "(another site)". Correct: three real sources, live links. Failure: a new tab with no warning and a mark broken onto its own line.
- 11.14, topic and atlas symbols stay out of buttons. Correct: the loop stepper, live, on Atlas V7's loop R10. Failure: CL-024 used as the reset button (D2-515).

**Group 4, Error, success and warning (Rules 11.15 and 11.16), new.**
- 11.15, each mark with its words. Correct: the sign-up form, live. Failure: red "Invalid" text beside the Close cross. Extra: the three marks in their messages.
- 11.16 answers the brief's question. **When an error, the take-part mark and an intervention marker meet in one view, the error keeps the red.** Rule 05.3 already sets the order: an error the reader must fix, then the step a reader can take now, then the point the headline names, which in a systems figure is where a reform acts. The take-part mark yields: its disc draws in the surface's ink in its place on the ring, "You can take part now" stays, and the ask steps down to the Charcoal primary button. The intervention marker yields too, keeping its heavier outline and its words in ink. Once the error is fixed, the red returns to the take-part mark. Correct: one view at 360 px with all three. Failure: all three in red.

**The five live specimens (D2-516)** are components, with manifest `"interactive": true`, so the check runs inside them:
- the reader toolbar (`s-11-11-correct`);
- the library filter bar (`s-11-12-correct`);
- the phone menu (`s-11-menu`);
- the loop stepper (`s-11-14-correct`);
- the form error (`s-11-15-correct`).

The links list (`s-11-13-correct`) is live too. Each finds its elements by data attributes from `document.currentScript`, since the build prefixes every id and class.

**Weight.** Chapter 11 measures 548,024 bytes in the built page, under its 550,000 budget by about 2 KB; it measured 751,545 before the trims listed under D2 lines below. A longer word pass could tip it over; the engineer's tokens.css link (requests) is the room.

**Figures** every rule prints are in `work/handoffs/phase-2/20261110_Stage-B-Round-2-Ch11-Figures.json`. The apply pass's `20261107_Apply-Pass-Systems-Ch11-Figures.json` stays as its record.

## Routine calls

- D2-xxx | Chapter 11's invented state bills share one counter, H.99001, S.99002, H.99003 and on, in the order the chapter first shows them; S.0876 becomes S.99002 so chapter 08's plate keeps the same bill | DR-151 names the first two numbers; one counter keeps every number unique across both chambers and both chapters
- D2-xxx | The Nebraska bill is LB 99008, with Nebraska's own prefix for a Legislative Bill | Nebraska has no House or Senate prefix; the number follows DR-151's range
- D2-xxx | The Nebraska bill joins Rule 11.1's correct plate, and its status line opens "Nebraska has one chamber." directly under the marks | DR-150 puts the words beside step 5 on every Nebraska card; Rule 11.1 is the rule that says every state keeps six steps
- D2-xxx | Each mark sits in a group tagged `data-icon="S-<state>"` and `data-icon-family="status"`, with a clear square of the circle's own size first, and the take-part disc after the group | Chromium measures a group by its shapes without their strokes, so the square makes guide check B-3 read 24, 26, 28 or 30 px; the disc reaches past the circle and would read 29 px
- D2-xxx | The clear square is dropped from marks inside a picture plate | B-3 reads marks only outside pictures; the squares would cost about 20 KB of the chapter's budget for nothing
- D2-xxx | `MARK_CSS` sets each mark width from its token by class (`rn`, `ra`, `sl`, `lr`, `la`, `td`, `tk`, `tc`, and `halo`), and the markup keeps its width attributes | The engineer's request, with the attributes left as the fallback and as `markTokens`' hooks; a failure plate's deliberate fault carries no token class, so it keeps its own width
- D2-xxx | A records request and an agency rule print their end words, bold, in place of "Step n of 6", with the date | DR-108 says a signed bill reads as law in words; the end state is what a reader needs first
- D2-xxx | A rule issued without advance comment slashes step 1 as well as steps 2 to 4 | The agency gave no early notice either, and D2-527 slashes step 1 when it is skipped
- D2-xxx | "In effect" fills all six steps, as "Became law" does | The research lead left the question to the systems designer; both mean the process finished and the text binds
- D2-xxx | A proposed rule that sits says "No action since" and the date under its step, with no mark of its own | The research lead's second question; D2-528 keeps waits in words
- D2-xxx | The warning mark stays in the set, for a status we read from the record ourselves, with "Checked" and the date | D2-510 leaves the call to me; a dated check is the notice the audit names, and Rule 11.10 needs it
- D2-xxx | The error mark draws in the text's ink; the error's red is a 4 px bar at the left of the field and of the message, drawn as a border | Pillar Red measures 2.64 to 1 on the Error Band and 2.96 on Newsprint, under 3 to 1 for a mark; Charcoal measures 11.89 on the band; a border survives forced colors where a box-shadow does not (question 1)
- D2-xxx | The success mark draws in Verdigris, 3.37 to 1 on Newsprint, and the warning mark in ink | The state tokens as they stand
- D2-xxx | Rule 11.16 draws the intervention marker as System 1 draws a reform's target: the variable's outline at 3 px, red only when it holds the view's red | The Times Explainer's own rule (`.node.ak-target .pl{stroke-width:3px}`); chapter 12 owns the final marker, and I match it when it lands
- D2-xxx | A live specimen sets `forced-color-adjust: auto` on its component and gives it an opaque ground | Its controls then take the system's colors as a product's would, while the stage around it keeps the guide's (AX-S6, D-4); the opaque ground turns to Canvas, so text never lands on a kept Newsprint
- D2-xxx | Every control rule in a live specimen names `.ui` first | The shell sets `font: inherit` on every button and input in a stage at (0,1,1), which outranked my class rules and set the red ask in 17 px regular, under 4.5 to 1 as small text
- D2-xxx | The reader's page size stays two word buttons, Fit width and Full size, pressed one bold and underlined at 2 px | DR-154 keeps zoom as words; C-5 asks for a cue besides color
- D2-xxx | The library demo reads the editor's label table for chapter 10 and chapter 10's list of 41, and counts by kind: topic, atlas, pillar | One source for the words; the counts are true to the set in use, 124 drawings, 101 atlas, 41 at 24 px
- D2-xxx | The phone menu is a modal dialog inside the phone frame: the rest of the frame goes inert, Tab stays inside, Escape and Close return focus to Menu, and its links lead to chapter 11's own rules | G-3, and every link lands on an id in the page whatever other chapters it holds
- D2-xxx | The loop stepper uses Atlas V7's loop R10, with each step's verb read from the chain's sign and the link's own plain sentence, and its text set with typographic apostrophes | Real atlas content; the atlas data writes straight apostrophes, which chapter 02 rules out
- D2-xxx | Play advances every 2.4 seconds only after a press, and Pause stops it | E-3; reader-controlled playback
- D2-xxx | The form validates on submit, moves focus to the first field to fix, and sends success to a status line from a template | SC 3.3.1 and 4.1.3; a status region that exists from the start is announced reliably
- D2-xxx | The links in Rule 11.13's correct plate are real sources from the research lead's sections 5 and 7, in the same tab | D2-513; a live link to a real page shows the rule as a reader meets it
- D2-xxx | Rule 11.14's failure draws CL-024 from the sprite at 24 px, one color, tagged `topic` | CL-024 is among the 41, so B-3 holds; the fault is semantic (D2-515)
- D2-xxx | Fault drawings that belong to no family (Rule 11.5's dots, Rule 11.6's generic stepper, the information mark, the pointer and the small figure's arrows) carry no `data-icon` | Tagging them would add made-up members to a family
- D2-xxx | Each specimen keeps only the CSS rules whose classes its markup carries, and drops a type style's own `font-variant-numeric: normal` after `font:`, and `letter-spacing: 0em` and `text-transform: none` for the reading styles | The pieces share one style source; the stage already inherits those values, and no piece sets a reading style inside a label; this saved about 100 KB
- D2-xxx | Fixed-width plates in chapter 11 set `fit_switch: false` | Every one sets 13 px step names or numbers, so D2-442 can never offer a fit, and the switch's markup cost about 10 KB
- D2-xxx | The wide list on Charcoal, the bill page on Charcoal and the wide bill page leave the chapter, and one extra now shows the wide form on Charcoal with two bills | Chapter 11's 0.55 MB budget; one plate still shows both the wide form and the Charcoal marks, and the wide page's key of meanings is the six-steps table after Rule 11.1
- D2-xxx | Rule 11.2's states show at true size only, and a table of the request and rule steps is not shipped | The same budget; each step's name and meaning sit in Rules 11.8 to 11.10 and the sources list
- D2-xxx | 13 px step numbers take their size from the marks' CSS (0.8125rem), and only 14 px numbers write a size | 13 is the common size; about 5 KB
- D2-xxx | The marks and live specimens read the surface's short role names (`--oa-color-graphic-essential` and the rest) | The stage's surface class points them at its own values (shell notes, section 5), so one declaration serves Newsprint and Charcoal
- D2-xxx | Source lines name a site without its long path | A long path does not wrap and pushed the page 10 px sideways at 360 px

## Questions for Dustin

1. **The error mark in ink, its red in a bar.** The token `oa.color.state.error.mark` describes the error glyph and its bar in Pillar Red. A red line glyph measures 2.64 to 1 on the pale Error Band and 2.96 on Newsprint, under the 3 to 1 a mark needs (Rule 05.5), and a 2 px line cannot take the Charcoal keyline a red disc takes. *Recommendation:* draw the error mark in the text's ink (11.89 to 1 on the band), and let a 4 px Pillar Red bar at the left of the field and of the message carry the error's claim on the view's red, as chapter 11 now shows. The engineer would then reword the token's description. It changes one color in one glyph, and is reversible by setting the glyph's color.

## Requests to other owners

- **Engineer.**
  - The shell's mark bridge rules can go: `MARK_CSS` reads every mark token itself. `markTokens` still finds its readers by the width attributes, which I kept.
  - The 16 px utility line token arrived while I worked (6.0.0-gate2.5). Two plates draw 16 px icons: `s-11-icons` and `s-11-13-correct`.
  - B-1 (`iconTargets`) fails any control holding a glyph under 44 by 44 px, so a link with its 16 px mark inside running text would fail, though SC 2.5.8's inline exception allows it (audit 1.2, item 7). I showed the list form only. Could B-1 skip a link inside a paragraph's running text?
  - Under forced colors, `.plate-scroll { border: 1px solid CanvasText }` makes 360 px stages 2 px too wide at 390 px, so their scroll hints show. That is 32 plates in chapter 11 and 125 in the page, where normal colors show 46.
  - The For builders closer embeds tokens.css as a 90,650-byte data link in every chapter, about a sixth of chapter 11's budget. One download for the page would hand each chapter about 90 KB.
  - If Dustin agrees to question 1, reword `oa.color.state.error.mark.*`.
  - For A-5: my trackers carry their state words in the alt and status line, and carry no `data-step`.
- **Chapter 05's owner.** `s-05-3-corrective` draws the error as a white cross in a red disc. DR-173 and D2-509 make the error mark a circle holding an exclamation mark, and the cross means Close. The approved drawing is `U-error`.
- **Chapter 10's maker.**
  - `s-10-lib-03`'s meaning sentence ("A parcel meets a gate with two bars across it") fails `codes` on the word "gate", the page's only remaining failure.
  - Please confirm the intervention marker for chapter 12, or send me its final drawing for Rule 11.16 to match.
- **Editor.**
  - Every word in chapter 11 is yours to change through your table.
  - The library demo reads `20261110_Stage-B-Ch10-Labels.json` (its `rows`: `id`, `label`, `class`), and my build stops with a message if the rows stop totaling 124, or 41 at 24 px.
  - Three extras left for weight (listed above), so their captions are gone.

## Tested

- `python3 -I work/build/scripts/phase-2/apply_systems_ch11.py`: 16 rules, 37 specimens, 19 figures. Every specimen passes the systems checks: no heading, landmark, dash, literal color or px font size; curly quotes in every alt.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`: exit 0, no warnings, 12 chapter files, 128 rules, 295 specimens. Chapter 11 weighs 548,024 bytes against 550,000.
- `node work/build/scripts/phase-2/guide_check.js <scratch>/guide.html` at 1440, 1024, 390 and 360 px.
  - Chapter 11 has no failure.
  - The page's only failure is `s-10-lib-03`'s "gate" (chapter 10).
  - Stage B checks at 390 px found 304 icons outside pictures, none without a family. They read 359 glyph parts (263 through `<use>`), and every mark token has readers (ring now 52, ahead 90, slash 18, halo 18, lines 123 and 45, disc 24, keyline 26, cut 26).
  - axe-core 4.10.2 passes, and so do `focus`, `menuDialog` and `textSpacing`.
- An earlier run caught three of my faults, now fixed: the red ask at 17 px (font inherited), and a source path that pushed the page to 370 px at 360.
- By script in Chromium at 390 px, every live specimen.
  - **Reader:** page 1 to 2 to 12; Previous and Next unavailable at each end with their reason; Full size pressed.
  - **Library:** "vot" gives 5 of 124 and shows the clear control; Clear the search empties the field and focuses it; Reads at 24 px gives 25 of 124 and 2 on, with the check; the sheet collapses with the chevron turned back; Clear filters gives 124 and returns focus to Filters.
  - **Menu:** opens with focus on Close; Tab cycles inside the panel; a row opens with its chevron turned; Escape closes and returns focus to Menu.
  - **Stepper:** Next shows step 1; Play swaps to Pause and runs to step 4, "Play again"; Reset returns to Ready with Reset unavailable.
  - **Form:** an empty submit marks both fields invalid with their messages, focuses Email and turns the ask Charcoal with no red; a valid submit shows the success line and returns the ask's red.
  - No script errors on the page.
- Looked at, every chapter 11 plate at 1440 and 390 px. Plates at 1440 px at device scale 2. The four main live specimens at 390 px in forced colors, dark: every icon, dashed unavailable outline, pressed underline and the chip's check stay visible.
- Contrast from the token values: Pillar Red on the Error Band 2.64, Charcoal on the band 11.89, Verdigris on Newsprint 3.37, the focus ring 3.37.

## Not tested

- A screen reader by ear, other browsers than Chromium, real phones and Windows high contrast itself; forced colors and reduced motion are Chromium's emulation.
- The live specimens at 1024 and 1440 px by script (the check ran there; my interaction script ran at 390 px only).
- Text at 200 percent inside the picture plates, which the checks skip.
- Whether readers name the status marks or the utility icons; the combined reader check is the place.
- The engineer's `sprite_check.js`, `icon_pixel_fit_check.js` and look-alike check on my plates: I drew no new icon, and the sprite and finals are theirs.
- Chapter 01's card rebuilt with the new module: I checked by import that its functions run, and did not run its generator, which writes another owner's files.

## Change log

Created:
- `work/build/scripts/phase-2/apply_systems_ch11_ui.py`
- `work/handoffs/phase-2/20261110_Stage-B-Round-2-Ch11-Figures.json` (by the script)
- `work/handoffs/phase-2/20261110_Stage-B-Round-2-Systems-Ch11-Notes.md` (this file)
- Specimens: `s-11-8-correct`, `s-11-8-failure`, `s-11-9-correct`, `s-11-9-failure`, `s-11-10-correct`, `s-11-10-failure`, `s-11-11-correct`, `s-11-11-failure`, `s-11-icons`, `s-11-12-correct`, `s-11-12-failure`, `s-11-menu`, `s-11-13-correct`, `s-11-13-failure`, `s-11-14-correct`, `s-11-14-failure`, `s-11-15-correct`, `s-11-15-failure`, `s-11-marks`, `s-11-16-correct`, `s-11-16-failure` (all `.html` in `work/build/guide/specimens/`)

Modified:
- `work/build/scripts/phase-2/apply_systems_ch11.py` (and the new module) with the editor's 12 changes from section 4d of `20261110_Stage-B-Round-2-Editor-Notes.md`
- `work/build/guide/chapters/11-icons.json`
- `work/build/guide/specimens/manifest-systems.json` (chapter 11's entries only; 05 to 07 kept)
- Every other `s-11-*.html` specimen, rebuilt by the script

Removed (by the script, which deletes chapter 11 specimens it no longer writes): `s-11-list-360-charcoal.html`, `s-11-list-600-newsprint.html`, `s-11-page-360-charcoal.html`, `s-11-page-600-newsprint.html`. Their replacement is `s-11-list-600-charcoal.html`.

Not touched: `source/`, `work/ledger/`, `deliverables/`, every asset folder, every board, the shell, the build and check scripts, and every other owner's file. `20261107_Apply-Pass-Systems-Ch11-Figures.json` is back as committed after one accidental rewrite during my first run.

Scratch (outside the repository): `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/round-2/ch11/` holds the builds, the check results, the captures and the probe scripts.
