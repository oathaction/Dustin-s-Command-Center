# Apply pass, round one: identity designer's notes

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `work/handoffs/phase-2/20261107_Apply-Pass-Brief.md`. I changed only my own files: chapters 03, 04 and 08, the proofs appendix, `manifest-identity.json` and its specimens, my build scripts `stage_a_identity_*.py`, and identity assets. I wrote no ledger, `source/` file, board or other owner's file.

**To open:** `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, at `#identity`, `#ampersand`, `#lockmark` and `#proofs`.

**To rebuild:** `python3 -I work/build/scripts/phase-2/stage_a_identity_s1.py` (S1's masters and the minimum sizes table), then `python3 work/build/scripts/phase-2/stage_a_identity_build.py --pdf`, then `python3 -I work/build/scripts/phase-2/guide_build.py --strict`.

## What I did, item by item

**1. S1 masters.** `stage_a_identity_s1.py` copies Board 6's three S1 files into `work/build/assets/identity/lockups/` as `20261107_S1-Stacked-Master.svg`, `-24px.svg` and `-16px.svg`. Each gets a clean `<title>` naming the lockup and its master range; the path data is byte for byte Board 6's, and the script asserts it. A contour check reads each written file, splits it into letters and matches every letter to a wordmark master letter, and B to B's master, by translation alone: 17 contours and 10 letters in each file, worst offset 1.1 × 10⁻¹³ units in the display master and 2.8 × 10⁻¹⁴ in the 24 and 16 px masters. B also matches the B inside the wordmark at offset 0. The script writes a Charcoal edition beside each master (`-Charcoal.svg`: Charcoal letters, B in signature red, colors written in for light grounds) and a Prussian White edition in `prussian/` (`-Prussian-White.svg`: every part White, treatment D). Both editions keep the master's paths unchanged, which the script asserts. L2's files stay where they are, kept for the record: `lockups/20261028_L2-Stacked-Master.svg`, `lockups/20261028_L2-Stacked-Condensed-Master.svg` and their two files in `prussian/`.

**2. Minimum sizes.** `20261028_Identity-Minimum-Sizes.json` gains an S1 row from Board 6's measurements (79 px wide with 14 px capitals, 0.65 in, below it L8, the three masters and their ranges). L2's row is marked `"status": "retired"`, `"replaced_by": "S1 stacked"`, with a note. Every row that carries condensed figures is marked `"condensed": "kept for the record, not in use (D2-328)"`, and a top-level `condensed` note says the same. The badge row now reads 48 px from the display master, 0.50 in, with its 16 and 24 px masters kept in `badge/` for the record (DR-118). L8's row adds "never an avatar" with a note on DR-116. The update is idempotent.

**3. Chapter 03.** S1 replaces L2 in the lockup sheet (`s-03-lockups`, at 40 px capitals), Rule 03.2's text, specifications and files, Rule 03.4's specifications, the minimum sheet (`s-03-4-correct`, S1 at its 79 px minimum) and the minimum table (`s-03-minimums`, still `readable`; it now leaves out retired rows). Rule 03.5's surfaces sheet shows L1, S1 and L8, S1's Prussian White file included. The intro and Rule 03.1 name the one width in force: "the width our fifth edition drew, with ampersand B as refined for this edition", and Rule 03.1 gains a Width specification (9.78x). No word about the condensed drawing remains in the chapter. Rule 03.7 and its builders note follow DR-116: L8 serves squares where the name must show, and avatars and the app icon show B alone (Rule 04.7). Rule 03.2's builders note tells producers to retire L2 and names S1's two editions. Rule 03.4 gives the badge its own 48 px minimum. Rule 03.6's builders note points a short email to Rule 08.2's once-in-a-view rule. L6's job reads "The strip that closes a report or a long page", since "sign-off" now names one of the lockmark's places.

**4. Chapter 04.** Rule 04.6 is now "End an article with B alone, and keep the badge for back covers and events." Its correct plate ends a paragraph of 17 px body text on B in Charcoal, the text's ink, from the 16 px master, and shows the badge at 96 px on the back of a 4 by 6 in event card. Its failure plate ends the same paragraph with the badge at 16 px, and under it a PNG compares "minutes." plus the badge with "minutes." plus the registered trademark sign, at true size and at twice size. Rule 04.2 adds the end mark to what does not count as the view's ampersand moment. Rule 04.7 names L8 for squares where the name must show (DR-116). Rule 04.8 says "never red" in its rule and its color specification (DR-117). Rule 04.1 loses its sentence about the narrow B. The chapter intro lists the end mark among the places the hinge appears. No other specimen of mine ended an article with the badge; I searched every owner's specimens and found none.

**5. Chapter 08, The lockmark.** `08-lockmark.json`, anchor `lockmark`, three rules. My build deletes `08-signal-grid.json`.
- Rule 08.1 keeps today's 08.1 and its two plates.
- Rule 08.2, "Place the lockmark only in its four places, once in a view." One plate draws all four at true size: a 768 px masthead with L3 (the lockmark at 52 px from its display master), a report page header with the lockmark at 24 px beside the section label, a Charcoal footer at 24 px beside the tagline and a chart's footer at 16 px beside chapter 02's jobs chart source line, and the bottom-right corner of a 1080 px social card with the lockmark at 48 px from the display master, 72 px in from both edges, with dimension lines. The failure keeps the lockmark-as-bullets flyer.
- Rule 08.3, "Let the lockmark code nothing." Its correct plate shows Board 6's bill S.0876 as Rule 11.5 draws it: six numbered steps, step 4 current, and the step in words. Its failure draws the same bill on the lockmark's nine nodes with four filled, under the Charcoal band "Failure case: do not publish". The rule text, the intro and the builders note send readers to chapter 11 for trackers.
- Today's Rules 08.3 to 08.9, the codes table, the stages sheet and the composer leave the chapter: 18 specimens removed in all, with the proofs below.
- Instruction line: "Draw the lockmark from its master, and place it only in its four fixed places." The editor may tune it in round two.

**6. Proofs.** `proofs.json` is titled "Identity proofs", with five groups: the site masthead (1440 px bar and 390 px phone bar), the avatar (a 400 px upload with the platform's circle drawn as a guide, feed rows at 48 and 32 px, and a 180 px app icon, all B alone on Charcoal), the social card (sign-off now 48 px from the display master), the letterhead (one sheet, footer lockmark at 24 px, and a new one-page PDF), and "L2 beside S1" (`s-proofs-stacked`) at capitals 22, 44 and 100 px, so L2 stands 48, 96 and 218 px tall. The glance, email and condensed minimum plates leave. The new PDF is `work/boards/phase-2/stage-a/proofs/20261107_Letterhead-Proof.pdf`; the stage A two-page proof beside it stays as the record of board A.

**7. Retired grid uses in my specimens.** None of `s-03-*`, `s-04-*` or `s-proofs-*` draws a grid kicker, a coded grid, a series route, a pillar corner or tracker progress. I checked each of the brief's known hits:
- `s-03-4-correct` shows the lockmark at its 16 px minimum and L3 at its 196 px minimum. Both are the lockmark itself, and the plate now carries S1 and the badge at 48 px.
- `s-03-6-correct` is the masthead place.
- `s-03-lockups` and `s-03-minimums` changed for S1.
- `s-03-l6` draws L6 with the lockmark and four pillar dots. It draws no coded grid, so I left its drawing alone and put it to Dustin below.
- Every `s-08-*` plate was rewritten or removed. The coded grid drawing (`sgrid`) survives in `stage_a_identity_lib.py` only to draw Rule 08.3's failure.

## Routine calls

- D2-xxx | S1's Charcoal edition sets Charcoal letters with B in signature red, colors written in, beside each master in `lockups/`; its Prussian White edition sits in `prussian/` | The Civic Line package calls the editions drawn in Charcoal "Charcoal editions", and `prussian/` holds every treatment D file, where Rule 03.1 already sends builders
- D2-xxx | S1's masters cover capitals 14 to 17 px (16 px master), 18 to 36 px (24 px master) and from 37 px (display master) | Board 6's proposed ranges, which follow the wordmark's ranges by height
- D2-xxx | The badge's minimum is 48 px on screen and 0.50 in in print; its 16 and 24 px masters stay in `badge/` for the record | DR-118 keeps the badge from 48 px; 0.50 in is 48 px at 96 px to the inch
- D2-xxx | At body size, B as the end mark takes its 16 px master at 16 px, 14 px tall, 1.6 px taller than the capitals of 17 px text | DR-118's cap height meets Rule 03.4's 14 px floor for identity marks, and the floor wins; the rule says "as tall as the text's capitals, or 14 px tall where they are shorter", as the old Rule 04.6 builders note did
- D2-xxx | The end mark does not count as the view's one ampersand moment (Rule 04.2) | Every article now ends on B, and a hinge headline must stay possible in the same article
- D2-xxx | Rule 04.6's failure sets the registered sign in Liberation Sans, the metric twin of Arial, inside a PNG | Inter draws the sign as a small raised glyph; most typefaces draw it full height on the baseline, the form a reader would confuse with the badge, and a PNG keeps the comparison the same on every screen
- D2-xxx | Chapter 08 holds three rules: the master (08.1), the four places (08.2) and no codes (08.3) | The brief asks for a short chapter, and each place's size sits in Rule 08.2's specifications
- D2-xxx | The four places share one plate, 770 px wide, with the fit switch | Each place shows at true size, and the masthead needs its 768 px breakpoint
- D2-xxx | The masthead place includes the email header | Rule 03.6 already sets L3 at the head of an email
- D2-xxx | When a masthead and a footer share one view, the footer keeps the lockmark and the masthead sets the wordmark alone | Rule 08.2 has always said once per view; Board 6's tracker notes proposed this form, and Rule 03.6's builders note now says the same
- D2-xxx | L6 is listed under the footer place, with its lockmark at L6's own proportion | L6 is the strip that closes a report; changing its proportion would change a lockup (question 1)
- D2-xxx | The chart footer prints chapter 02's jobs chart source line word for word | A real, approved source line, and no invented statistic
- D2-xxx | Rule 08.3's correct plate draws Board 6's Option B with the same geometry as chapter 11 | A reader sees the fix beside the failure; I compared it with `s-11-list-360-charcoal` (324 by 34 px, 26 px circles), and they match
- D2-xxx | Rule 08.3's failure draws Board 6's S.0876 on stage A's 40 px lattice | One retired use, as the brief asks, with the same bill as the correct plate and one Illustrative label at the head of each card
- D2-xxx | L6's job reads "the strip that closes a report or a long page" | "Sign-off" now names one of the lockmark's places
- D2-xxx | The proofs drop the email pair | The brief lists the masthead, avatar, social card and letterhead, and chapter 03 already shows the email header
- D2-xxx | "48 px, 96 px and display size" are read as lockup heights at one cap height: capitals 22, 44 and 100 px. L2 comes from its display master at every size, and S1 from the master its range picks | L2 has only a display master, and S1 at 22 px capitals is its 24 px master at true size
- D2-xxx | The minimum table on the page leaves out retired rows, while the JSON keeps L2 as retired | The asset record keeps the history, and the reader page shows what is in force
- D2-xxx | A new one-page letterhead proof, `20261107_Letterhead-Proof.pdf`, sits beside the stage A proof | The stage A file is the record of what board A showed

## Question for Dustin

1. **L6, the editorial signature.** L6 sets the lockmark at about three cap heights (93 px at its 884 px minimum) beside the tagline, with four pillar dots under the tagline and no words beside them. Since November 7, pillars take their icons with their words (DR-111), and the lockmark keeps four places with fixed sizes (DR-110). Changing L6 changes a lockup, so it needs your named approval. *Recommendation:* redraw L6 without the four dots and keep its lockmark at L6's own proportion, as the form the footer takes at the end of a report. The other choice is to retire L6 and close reports with the footer place, 24 px beside the tagline.

## For the main session and other owners

- **Engineer.** Chapter 08's instruction line in `08-lockmark.json` is "Draw the lockmark from its master, and place it only in its four fixed places." The chapter file wins, but the draft line in `guide_build.py`'s chapter list differs ("...and keep it to its four fixed places."), so please align it. `08-signal-grid.json` no longer exists, so `LEGACY_FILE` can be emptied. The brief names `work/build/guide/shell/manifest-identity.json`; the manifest lives in `work/build/guide/specimens/manifest-identity.json`, as before. The display lockmark file still carries "V5" in its name (D2-298); the asset package should rename it.
- **Systems designer.** `s-08-3-correct` copies chapter 11's numbered steps. If Rule 11.5's marks change, the main session should send that to me. Rule 08.3 cites Rule 11.5 by number.
- **Editor, round two.** Chapters 03, 04 and 08 and the proofs are ready for the copy edit, through `stage_a_identity_chapters.py` and `stage_a_identity_proofs.py`. The build warning that Rule 01.21's builders note cited Rule 08.8 had cleared by my last build.

## Tested

- `python3 -I work/build/scripts/phase-2/stage_a_identity_s1.py`: three masters, three Charcoal and three Prussian White editions written. The contour check matched 17 contours and 10 letters per master by translation alone, worst offset 1.1 × 10⁻¹³ units. Every edition's paths equal the master's, and the master's equal Board 6's. Colors: Charcoal editions hold only #121212 and #E63946, and Prussian White editions only #FFFFFF. All nine files parse as XML.
- `python3 work/build/scripts/phase-2/stage_a_identity_build.py --pdf`: 48 specimens and 3 chapters (03: 8 rules, 04: 8, 08: 3), 18 stale specimens and `08-signal-grid.json` removed. A dry run into my scratchpad first reproduced the committed outputs byte for byte before any change.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict`: exit 0, no warnings, 9 chapter files, 100 rules, 232 specimens.
- `node work/build/scripts/phase-2/guide_check.js ... --no-captures` at 1440, 1024, 390 and 360 px: PASS, 0 failures, with the engineer's new retired-words check in place. My exemptions are unchanged from stage A, apart from the email and condensed plates that left. I ran it again on the final build, after my last edits (the Rule 11.5 references and the fit switch on Rule 04.6's plates): PASS at all four widths, 0 failures, 754 same-page links.
- A script scan of my chapter JSON, proofs JSON, manifest alt text and specimen text and labels found no "Signal Grid", "Stage n of 9", "condensed", "Gate", decision code, "V5", em or en dash, listed filler or corporate verb, or straight apostrophe. "Badge at 16" appears once, in Rule 04.6's failure caption, on purpose.
- Looked at in Chromium: chapter 08 whole at 1440 px, and at 390 px at twice size; the proofs whole at 1440 px; at twice size, Rule 08.2's places plate, Rule 08.3's failure, Rule 04.6's failure, the lockup sheet, the minimum sheet and table, and the surfaces sheet; Rule 04.6's correct plate at 390 px at twice size. These looks led to fixes: the places plate overflowed the column at 816 px, guide lines crossed the sign-off lockmark, the Illustrative label sat outside the bill cards, the avatar proof's two columns wrapped, Rule 04.6's article did not fill its plate, and Inter's raised registered sign made a weak comparison.
- Chapter 11's list specimen compared with my step marks: same width, height, circle radii and line positions.
- The new letterhead PDF with `pdfinfo` (1 page, 612 by 792 pt) and `pdftotext`, and rendered at 60 dpi and looked at.

## Not tested

- Chapters 03 and 04 at 390 and 360 px beyond Rule 04.6's correct plate; the guide check covered their overflow, text size and contrast, but I did not look at every plate.
- S1's 16 and 24 px masters rendered at 1x against the pixel grid. Board 6 measured their crisp share (0.69 and 0.77), and I did not repeat it.
- Screen readers by ear; Firefox, Safari and real phones; the fit switch on the new plates beyond seeing it in the plate head.
- The letterhead PDF on paper, and the Charcoal editions placed in a slide or design app.
- Any reader on the end mark, S1 or the four places.

## Change log

Created:
- `work/build/scripts/phase-2/stage_a_identity_s1.py`
- `work/build/assets/identity/lockups/20261107_S1-Stacked-Master.svg`, `20261107_S1-Stacked-Master-24px.svg`, `20261107_S1-Stacked-Master-16px.svg`, and the same three with `-Charcoal` before `.svg`
- `work/build/assets/identity/prussian/20261107_S1-Stacked-Master-Prussian-White.svg`, `20261107_S1-Stacked-Master-24px-Prussian-White.svg`, `20261107_S1-Stacked-Master-16px-Prussian-White.svg`
- `work/build/guide/chapters/08-lockmark.json`
- `work/build/guide/specimens/s-proofs-stacked.html`
- `work/boards/phase-2/stage-a/proofs/20261107_Letterhead-Proof.html` and `20261107_Letterhead-Proof.pdf`
- `work/handoffs/phase-2/20261107_Apply-Pass-Identity-Notes.md` (this file)

Modified:
- `work/build/scripts/phase-2/stage_a_identity_lib.py`, `stage_a_identity_chapters.py`, `stage_a_identity_s03.py`, `stage_a_identity_s04.py`, `stage_a_identity_s08.py`, `stage_a_identity_proofs.py`, `stage_a_identity_build.py`
- `work/build/assets/identity/20261028_Identity-Minimum-Sizes.json`
- Regenerated by my build: `work/build/guide/chapters/03-identity.json`, `04-ampersand.json`, `proofs.json`, `work/build/guide/specimens/manifest-identity.json` and every `s-03-*`, `s-04-*`, `s-08-1-*`, `s-08-2-*`, `s-08-3-*`, `s-proofs-masthead`, `s-proofs-avatar`, `s-proofs-social` and `s-proofs-letterhead` fragment

Removed (mine):
- `work/build/guide/chapters/08-signal-grid.json`
- Specimens `s-08-4` to `s-08-9` (correct and failure), `s-08-combinations`, `s-08-stages`, `s-08-composer`, `s-proofs-glance`, `s-proofs-email`, `s-proofs-minimums`

Kept for the record, untouched: L2's four files, every condensed wordmark, lockup and hinge file, and `20261106_Letterhead-Proof.html` and `.pdf`.

Regenerated by running the engineer's scripts: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, its build report and its guide check results. Nothing committed or pushed.
