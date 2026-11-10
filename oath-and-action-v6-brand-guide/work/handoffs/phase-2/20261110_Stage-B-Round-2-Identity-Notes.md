# Stage B round 2: identity designer's notes

Oath & Action Edition 06, Phase 2, stage B round 2, November 10, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261110_Stage-B-Round-2-Brief.md` and the coordinator's task. I read the round 2 brief, the final stage B brief, the stage A content contract, Master Brief sections 6, 7, 11 and 12, chapter 10's construction text (`20261110_Stage-B-Ch10-Construction.md`), the engineer's promotion notes, the editor's round 2 notes, the pillar icons manifest, Board 6's pillar notes and the decisions that govern the pillar icons (DR-66, DR-67, DR-111, DR-112, DR-133, DR-138, DR-179, D2-375, D2-376, D2-439, D2-497, D2-634, D2-719, D2-783 to D2-785, D2-808, D2-809).

Status: items 1 to 4 are built and checked: the letterhead proof, chapter 09, chapter 01's three specimens and s-08-3, and chapter 12's Rules 12.1 to 12.4.

Nothing committed or pushed by me. No `source/`, ledger, `deliverables/`, master, asset final or other owner's file changed, apart from the three chapter 01 specimens D2-719 moved to me (their words untouched but one, the kicker word the editor gave me).

## What I built

### 1. The letterhead proof (D2-809)

`work/boards/phase-2/stage-a/proofs/20261110_Letterhead-Proof.pdf` and its HTML, printed beside the November 6 and 7 proofs, which stay as they were. One US Letter page (612 by 792 pt). Its footer draws the rebuilt 24 px lockmark master; rendered at 600 dpi, each node is one solid shape. The letterhead specimen `s-proofs-letterhead` now links to it, and its manifest note says so. `stage_a_identity_proofs.py` names the proof by `PROOF_DATE`.

### 2. Chapter 09, Pillar icons

`work/build/guide/chapters/09-pillar-icons.json` (the name `guide_build.py` expects from its chapter list, anchor `pillar-icons`), four rules, nine specimens in `manifest-identity.json`, written by `work/build/scripts/phase-2/stage_b_identity_ch09.py` through the identity build.

| Rule | Title | Correct | Failure |
|---|---|---|---|
| 09.1 | Set the four pillar icons in order, each beside its word. | `s-09-1-correct`: the row at 48 and 24 px on Newsprint and on Charcoal, one color | `s-09-1-failure`: the four icons with no words |
| (after 09.1) | The row on a phone | `s-09-phone`: a 358 px column, the 48 px row stacked with downward arrows (D2-376), the 24 px row wrapping after an arrow | |
| 09.2 | Underline the current pillar's word, and add its red only from 48 px. | `s-09-2-correct`: Track current at 48 px on Newsprint and Charcoal (underline and red), and at 24 px (bold underline, one color) | `s-09-2-failure`: Track marked by red alone |
| 09.3 | Draw a pillar icon from the file made for its size. | `s-09-3-correct`: each pillar at 16, 24, 48 and 96 px, and Track's 16 and 24 px fits enlarged four times from 1x renders | `s-09-3-failure`: Track's master at 16 px beside its fit, true size and enlarged |
| 09.4 | Put pillar icons only in the pillar row, on section openers and on tiles. | `s-09-4-correct`: Track's 128 px section opener on Charcoal with "Watch the vote." (our fifth edition's line), and a card with the rounded Charcoal tile at 76 px | `s-09-4-failure`: a report kicker carrying Track's icon |

How each icon is drawn:
- Every pillar icon is a `<use>` of the guide's sprite, never inlined (D2-590), with `data-icon` and `data-icon-family="pillar"` on its `<svg>`, hidden from assistive technology beside its word.
- 48 px and up: the master, `oa-sym-cl-0xx`, in `--oa-component-icon-ink-on-<surface>`. The current pillar's icon, and the opener's standalone icon, set `--oa-icon-accent` to `--oa-component-icon-accent-on-<surface>` (signature red) and carry `data-red="signature"`.
- 24 px: the engineer's pattern, the fit under 2x and the master from 2x in one `<svg>` (DR-179, D2-783). 16 px: the fit alone (D2-634). No accent under 48 px.
- Words and arrows are spaced from each icon's ink (D2-439): the masters' ink from chapter 01's figures, the fits' from their pixel maps, so a fit's margins are whole pixels and it keeps its grid.
- The 128 px opener icon is pulled in to its ink, so its left edge meets the text's.
- The tile is the Civic Line package's rounded two-color Charcoal tile file, placed as an image at its 76 px minimum (D2-42), which the set in use points to (D2-716).
- The enlarged views are 1x PNG renders of the fit files and the master at 16 px, shown four times in square pixels.

Rule 09.3 states the density rule with its reason (D2-808): "A 24 px icon keeps its fit up to 2x, since below 2x the master's line falls under one device pixel and its counters fill, and the fit keeps every counter and gap." Rule 03.4's end mark line now states its own rule and reason the same way.

### 3. Chapter 01's three pillar specimens and the state bill

**`s-01-pillars`, `s-01-21-correct`, `s-01-21-failure` (D2-719).** `work/build/scripts/phase-2/stage_b_identity_ch01.py` rewrites the drawings in place, in the files the editor's build writes: every inline master becomes chapter 09's glyph from the sprite with `data-icon-family`, and the 24 px row takes the 1x and 2x pattern. In `s-01-21-correct` the Analysis kicker's icon is now CL-057 (one of the 41 that read at 24 px, `data-icon-family="topic"`) beside "Workers' share of income", the word the editor gave in its round 2 notes. Under 48em the 48 px row keeps each icon's whole box, so the stacked words share one left edge, as chapter 09's do. The step touches only inline masters and that one word, and a second run changes nothing.

**`s-08-3-correct` and `s-08-3-failure` (DR-151).** Board 6's S.0876 is now S.99002, School bus contracts, the number chapter 11 gives the same bill at the same step, labeled Illustrative. The steps follow chapter 11's 360 px list as it now stands: 328 px wide, circles 60 px apart from edge to edge, each mark in a group with its status id and `data-icon-family="status"`.

### 4. Chapter 12, Rules 12.1 to 12.4

Written by `work/build/scripts/phase-2/stage_b_identity_ch12.py` through the identity build. The chapter file is shared (D2-829, D2-830). The systems designer created `12-graphic-devices.json` with Rules 12.5 to 12.9. My writer replaces only Rules 12.1 to 12.4 and my extra, and keeps their rules, extras and opener as they stand in the file. It adds one sentence to the intro's second paragraph for Rules 12.1 to 12.4 and puts chapters 04 and 03 at the head of the related list. Their script keeps every rule outside 12.5 to 12.9, so the two scripts can run in either order. Their `check_chapter` passes on the merged file. Specimens are named by device in `manifest-identity.json`. My build's stale-file cleanup in chapter 12 reaches only my five device prefixes, never their `s-12-marker-*` and the rest.

| Rule | Title | Correct | Failure |
|---|---|---|---|
| 12.1 | Divide sections with a Stone hairline. | `s-12-divider-correct`: an Illustrative town budget article with a hairline, then chapter 04's hinge divider before What you can do, and the hairline on the four surfaces | `s-12-divider-failure`: the same article with dashed breaks |
| (after 12.1) | Every graphic device and its rule | `s-12-index`: a readable table of 14 devices with links to their rules, the hinge divider indexed to Rule 04.4 as the architecture map asks | |
| 12.2 | Set a watermark in an open margin, at its token opacity. | `s-12-watermark-correct`: B's display master at 320 px in the open right margin of a report page (Charcoal at 0.08) and a Track section opener (Newsprint at 0.10), running off the edge | `s-12-watermark-failure`: B behind the heading and paragraph |
| 12.3 | Sign a small header or a video's corner with L8 at full strength. | `s-12-signature-correct`: L8 at 48 px in a report's running head on White, and in the top right corner of a 480 by 270 explainer video still on Charcoal | `s-12-signature-failure`: L8 at a watermark's 10 percent in the video's corner |
| 12.4 | Use a pattern only in an open area, away from words. | `s-12-pattern-correct`: two Illustrative screen covers, the hinge arcs from the bottom right corner and a block of hinge rules, each at least 24 px clear of the words | `s-12-pattern-failure`: each pattern behind the title and the paragraph |

The two patterns, built from approved masters after icon study 07's ring rhythm and rule rhythm:
- **Hinge arcs** carry on the hinge diagram's ring and arcs (radii 110 and 165 units, a 2 to 3 ratio) in equal steps: circles from a corner at 2, 3, 4 and more steps of 16 px, ending inside a quarter circle.
- **Hinge rules** repeat the hinge divider's 1 px line every 12 px.

Both draw 1 px in the hairline token. Ink coverage, measured on a 240 px swatch rendered at 1x in Chromium as Phase 1 measured its patterns, is 5.5 percent for the arcs and 8.3 percent for the rules, under the 12 percent ceiling (D1-18).

## Check figures

- **Strict build** (`guide_build.py --strict`, 11 chapters, 123 rules, 285 specimens): 0 warnings. The notes that chapter 01's three specimens inline sprite drawings are gone; the notes left are the engineer's own, on the 16 px utility line token.
- **Guide check** (`guide_check.js`, 1440, 1024, 390 and 360 px): 4 failures, all one: the studio word "gate" in chapter 10's `s-10-lib-03`, at each width, which belongs to chapter 10's maker. Chapters 01, 03, 04, 08 and 09 and the proofs pass every check, among them icon sizes, pillar order, red, text size and contrast, type scale, codes and axe-core.
- **The 1x and 2x pattern, looked at:** in the built page the 24 px rows draw the crisp fits at 1x and the smooth masters at 2x (Rule 09.1's plate, enlarged).
- **Looks:** every chapter 09 plate, chapter 01's three plates and `s-08-3-*` at 1440 and 390 px, with the masthead hidden, and three at 2x. Four looks led to changes: the stacked column's words started at ragged points; the ladder's words sat low beside the 96 px icons; the failure's two enlarged views stacked under long tags; and the opener's icon stood about 10 px inside the text's edge while the card's job line left one word on its last line.

## Routine calls

- D2-xxx | Chapter 09 has four rules: the row and its words, the current pillar, the file for each size, and the places | The round 2 brief's points for chapter 09, one rule each, with the phone column as an extra after Rule 09.1
- D2-xxx | Pillar rows use the component icon tokens: `--oa-component-icon-ink-on-<surface>` for the ink and `--oa-component-icon-accent-on-<surface>` for the accent | Chapter 10's construction text, section 7; the accent token resolves to signature red
- D2-xxx | The 48 px row's words keep chapter 01's style: the intro style, bold, 19 px and 22 px from 48em; the 24 px row's words are body text, bold when current | One row in two chapters looks the same
- D2-xxx | A stacked column drops the ink trim, so the four words share one left edge | In a column, a shared edge reads; across a row, spacing from the ink keeps the gaps even (D2-439)
- D2-xxx | A 24 px fit's margins come from its own pixel map, in whole pixels | The fit keeps its grid; the master's ink at 24 px would give fractional margins
- D2-xxx | Rule 09.2's failure is the current pillar marked by red alone at 48 px | It breaks WCAG 2.2 SC 1.4.1 at the one size where red may appear, and needs no forbidden accent under 48 px
- D2-xxx | Rule 09.3's failure is Track's master at 16 px beside its fit, with 1x renders enlarged four times | Track is the busiest drawing and the faintest at 16 px (Board 6 notes)
- D2-xxx | The section opener is Track's, with "Watch the vote." from our fifth edition's pillar plate, at the title style's 56 px, labeled Illustrative | The brief names the line; Track's job fits it
- D2-xxx | The tile stands alone on a card that leads to a pillar's section, at 76 px | DR-116 gives avatars and the app icon to ampersand B, so the pillar tile leads to a section; 76 px is the rounded two-color minimum (D2-42)
- D2-xxx | Rule 09.4's failure is a Report kicker with Track's icon, on an Illustrative card under the failure band | The brief's failure; Report names no pillar, which is the creative director's Board 6 reason
- D2-xxx | Chapter 01's drawings move to the sprite through a step of mine that rewrites the editor's generated files in place, and runs again after any rebuild of the editor's chapters | The words and the build stay the editor's; the drawings are mine this round (D2-719)
- D2-xxx | `s-08-3` draws S.99002 with chapter 11's 360 px geometry and status groups | DR-151, and the plate's note says it follows chapter 11's marks
- D2-xxx | Chapter 12's identity rules are the hairline (12.1, with the device index after it), the watermark (12.2), the compact signature (12.3) and the patterns (12.4) | D2-829 gives the identity designer 12.1 to 12.4 for dividers, watermarks and patterns; the compact signature is the brief's second watermark point and needs its own failure
- D2-xxx | Rule 12.1's failure is a dashed divider | D1-21: the atlas's key gives dashed lines to plausible links; chapter 07 keeps cards as a layout unit, so "no boxes", our fifth edition's standard, would contradict it
- D2-xxx | The watermark is ampersand B from its display master, and it counts as the view's one ampersand moment (Rule 04.2) | Our fifth edition's quiet signatures used the glyph; a B anywhere in a view is a freestanding or cropped B, which Rule 04.2 counts
- D2-xxx | A watermark stands at least half its page's height | A smaller watermark reads as a mark set too faint, the failure Rule 12.3 shows
- D2-xxx | The compact signature is L8, opaque, from 48 px | D2-193 retired V4.2's typed "O & A" and made L8 the one monogram; DR-116 keeps avatars and the app icon for B alone
- D2-xxx | The video still is a bill's six steps on Charcoal with the step in words, from chapter 11's 360 px list | The guide has no photographs yet (chapter 16), and an explainer frame is real content we make
- D2-xxx | The patterns come from the hinge devices only | Rule 08.3 keeps the lockmark whole, so Phase 1's node rhythm (from the grid) is out; the wordmark, B and the Civic Line drawings each have placement rules a repeat would break; nodes on a line would read as chapter 11's tracker
- D2-xxx | Each pattern runs 1 px in the hairline token, with no pattern on Prussian | One color as Phase 1 proposed; on Prussian the hairline token is White, which a repeat would turn loud
- D2-xxx | The hinge arcs end inside a quarter circle as wide as their area's shorter side | Clipped at a straight edge, the arcs leave a hard line; a quarter circle ends the way the hinge's ring does
- D2-xxx | The pattern covers are 360 by 466 px screen covers with type at the phone floor | Two fit a 600 px plate, and the type stays on the scale (D2-254)
- D2-xxx | Rule 12.4's single failure plate shows both patterns behind words | The brief asks a failure for each pattern; one plate shows both, side by side
- D2-xxx | The device index sits after Rule 12.1 and names the systems devices by their rules (12.5 to 12.9) | The architecture map lists the hinge divider in chapter 12's index, and a builder looks for a device by its job

## For the editor

- **The kicker drawing is in.** `s-01-21-correct` now carries CL-057 beside "Workers' share of income". Your caption in `01-purpose.json` and the alt text in `manifest-editor.json` still name Productivity; your table's new words can go in now.
- **`s-01-21-failure`** keeps "Analysis · Productivity" with Explain's icon, and its alt says "in place of the Productivity icon". Since the correct kicker now reads "Workers' share of income", you may want the failure's words to match.
- **Your build overwrites my drawings.** `guide_editor_build.py` writes the three files with inline masters. After any run of it, run `python3 -I work/build/scripts/phase-2/stage_b_identity_ch01.py`. Or have your generator draw them with `stage_b_identity_ch09.glyph` (pillar icons) and a sprite `<use>` (CL-057), and the step becomes a no-op.
- **`s-01-pillars`'s note** in `manifest-editor.json` says the icons are "inlined from the black masters"; they are now drawn from the sprite.
- **Chapter 09's words** are my drafts for your copy edit, all in `stage_b_identity_ch09.py`'s `chapter()` and the specimens' alt text.
- **Chapter 12's words** for Rules 12.1 to 12.4, the index and the specimens' alt text are my drafts in `stage_b_identity_ch12.py`. I added one sentence to the intro's second paragraph, before the systems designer's sentence on Rules 12.5 to 12.9.

## For the systems designer

- My writer keeps your Rules 12.5 to 12.9, your extras and your opener as they stand in the file, and adds my intro sentence before yours. Please keep the intro's second paragraph when your script writes the file; it already keeps rules outside 12.5 to 12.9.
- The device index after Rule 12.1 names your devices by job and links Rules 12.5 to 12.9. If your numbers move, the build's cross-reference check will flag the index, and I will follow.

## Questions for Dustin

None this round so far.

## Tested

- The letterhead proof: one Letter page; its footer rendered at 600 dpi and looked at.
- The identity build: 57 specimens and chapters 03, 04, 08 and 09; only the files listed below changed.
- `stage_b_identity_ch01.py` run twice: the second run changed nothing.
- The strict build, and the guide check at four widths (figures above).
- The chapter 09, chapter 01 and `s-08-3` plates looked at in the built page at 1440 and 390 px, three at 2x.

## Not tested

- Real 1.25x and 1.5x screens, Firefox and Safari; the pattern's switch was looked at in Chromium at 1x and 2x only.
- The editor's copy edit and the creative director's look at chapter 09.
- The tile on a White page or a phone home screen; the opener at widths other than its 552 px panel.

## Change log

Created:
- `work/boards/phase-2/stage-a/proofs/20261110_Letterhead-Proof.pdf`, `20261110_Letterhead-Proof.html` (D2-809)
- `work/build/scripts/phase-2/stage_b_identity_ch09.py`, `stage_b_identity_ch01.py`, `stage_b_identity_ch12.py`
- `work/build/guide/specimens/`: `s-12-divider-correct.html`, `s-12-divider-failure.html`, `s-12-index.html`, `s-12-watermark-correct.html`, `s-12-watermark-failure.html`, `s-12-signature-correct.html`, `s-12-signature-failure.html`, `s-12-pattern-correct.html`, `s-12-pattern-failure.html`
- `work/build/guide/chapters/09-pillar-icons.json`
- `work/build/guide/specimens/`: `s-09-1-correct.html`, `s-09-1-failure.html`, `s-09-phone.html`, `s-09-2-correct.html`, `s-09-2-failure.html`, `s-09-3-correct.html`, `s-09-3-failure.html`, `s-09-4-correct.html`, `s-09-4-failure.html`
- `work/handoffs/phase-2/20261110_Stage-B-Round-2-Identity-Notes.md` (this file)

Modified:
- `work/build/guide/specimens/manifest-identity.json` (chapter 09's nine entries; `s-proofs-letterhead` and `s-08-3-*` notes and alt text)
- `work/build/guide/specimens/s-proofs-letterhead.html`, `s-08-3-correct.html`, `s-08-3-failure.html`
- `work/build/guide/specimens/s-01-pillars.html`, `s-01-21-correct.html`, `s-01-21-failure.html` (drawings, and the one kicker word; D2-719)
- `work/build/guide/chapters/03-identity.json` (Rule 03.4's end mark line, D2-808)
- `work/build/guide/chapters/12-graphic-devices.json` (Rules 12.1 to 12.4, the index extra, one intro sentence and two related chapters, merged into the systems designer's file)
- `work/build/scripts/phase-2/stage_a_identity_build.py` (chapters 09 and 12 join the identity build), `stage_a_identity_lib.py` (the tracker steps' flush layout and status groups), `stage_a_identity_s08.py`, `stage_a_identity_proofs.py`, `stage_a_identity_chapters.py`
