# Brief: stage B round 1, the drawings and the drawings board

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the main session for two icon designers, the identity designer, the board builder, the editor and the creative director. It applies the final stage B brief (`20261109_Stage-B-Brief.md`, round 1) as Dustin's November 9 answers amend it: DR-146 to DR-148 and D2-495 to D2-502 in `work/ledger/20261020_Decision-Log.md`.

## What Dustin asked for

"The icons should clearly depict the institution, organization, concept, reform, whatever. It needs to be clear." He wants three options for each new or redrawn icon, and he approves by name from the options (DR-146). Clarity is the first test of every drawing. A reader who has never seen the brand should name the subject at 48 px without its label, or at worst recognize it at once with the label beside it.

## The bar

The best brand guide any studio has shipped: calm, exact, one hand per family, every line on purpose. The board shows true size first. Nothing on it is decoration.

## Who draws what

All three makers read `.claude/agents/oa-design-director.md` first, then `CLAUDE.md`, the final stage B brief, this brief and the Master Brief sections their role file names (`brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`). Civic Line's construction is in `work/ledger/20261029_Civic-Line-Icons-Report.md` and each drawing's correction log is in `work/build/assets/civic-line/src/<ID>.json`.

### Icon designer, Civic Line hand (D2-498)

1. **Six redraws (DR-135, DR-146, D2-495).** CL-025 Congress, CL-014 Entrenched Power, R-13 Congressional Capacity and R-42 Congressional Tariff Votes lose their domes; CL-059 Credit Allocation and R-48 Agency Independence lose their columns. Three options each.
   - At least one option keeps every other part of the drawing and its red, as DR-135 approved. Mark it "Within DR-135".
   - The other options may change more where that makes the subject clearer. Mark each "Outside DR-135" and say in one line what changed.
   - CL-025's options include the House chamber seen from the gallery, its seats curving around the rostrum, with the red on the rostrum (DR-146).
   - No option may show a dome, a column or a flag (Rule 01.6). Watch for drawings that read as a bank, a courthouse or a church.
   - Where a red accent sat on a column (CL-025) or a dome, the "Within DR-135" option moves it to the nearest part that stays, such as the center door, and says so.
   - The original masters stay as they are, as the record. Write new files only, in `work/build/assets/civic-line-redraws/`.
2. **Testify and Contact an official (DR-141, DR-147).** Three options each, in Civic Line's hand, in `work/build/assets/civic-line-new-topics/`.
   - Contact an official: (a) a person and an official's desk joined by one line with a red speech mark; (b) a very simple phone, which Dustin asked for by name; (c) your own.
   - Testify: (a) a person at a witness table with a microphone, facing a raised bench; (b) and (c) your own.
   - The research lead's meaning sheet (`20261109_Stage-B-Research-Notes.md`, section 1) says what each must show and what would mislead. The accessibility audit (`20261109_Stage-B-Accessibility-Audit.md`) says whether a phone collides with a utility glyph.
3. **Pixel-fit pillar icons (DR-133, D2-496, D2-497).** 16 and 24 px drawings of CL-019 Explain, CL-020 Track, CL-021 Connect and CL-022 Act, keeping every feature and every red placement, with the red as its own shape. Two fits each where a real choice exists, such as the line weight at 16 px. One-color editions are the ones in use under 48 px. New files in `work/build/assets/pillar-pixel-fit/`.

Construction for everything above: Civic Line's 128-unit box, one line weight, round caps and joins, one red accent, the capped fit (DR-08). Each drawing ships as a red-black and a black SVG, with 1x and 2x PNG previews.

### Icon designer, utility hand (D2-498)

1. **The utility set (DR-134, DR-146).** The actions listed in section 1 of `20261109_Stage-B-Accessibility-Audit.md`, three options each, in `work/build/assets/utility-icons/`.
   - A 24-unit grid, a line about 2 px at 24 px and 1.5 px at 16 px, round caps and joins, one color through `currentColor`, no red. Take the exact values from the engineer's tokens (`20261109_Stage-B-Engineer-Notes.md`).
   - Draw on the pixel grid at 24 px, with a 16 px master wherever the 24 px drawing does not hold at 16 px.
   - All three options of one action share the grid and the line, so Dustin can pick per icon and the set stays one family. Options differ in the picture, such as an arrow into a tray, onto a line or in a circle.
   - The set must stay apart from Civic Line: run the look-alike check against the 122 masters, and keep any glyph that reads like a Civic Line drawing out (CL-024 Feedback Loop already reads as refresh).
   - The meaning a reader names comes before novelty. Use the forms readers already know where they exist.

### Identity designer

1. **Pixel-fit end mark (DR-142, D2-496).** Ampersand B at 12 and 14 px, two fits each where a real choice exists, set in a line of text beside today's end mark (DR-130, D2-470). New files beside the masters in `work/build/assets/identity/ampersand/`.
2. **Lockmark masters rebuilt (DR-145).** The 16, 24 and 48 px masters with each node and the lever as one outline, the same pixels at each master's own size, beside today's files at 16, 24, 34, 40 and 48 px. Run the feed test (D2-468) on the new 48 px master and say whether it changes the 5 red pixels at 360 px the creative director flagged. New files beside the masters in `work/build/assets/identity/lockmark/` and `prussian/`.
3. **L6 centered.** The wordmark and tagline centered on the strip, beside L6 as drawn today without its dots (DR-129). This changes L6's proportion, so it needs approval by name. Your plate files go in `work/boards/phase-2/stage-b/drawings/identity/`; no master changes until Dustin answers.

## Checks every maker runs

- The engineer's pixel-fit check (`work/build/scripts/phase-2/icon_pixel_fit_check.py`) on every drawing meant for 16 or 24 px.
- The engineer's look-alike check (`work/build/scripts/phase-2/icon_likeness_check.js`) on every new or redrawn icon, against the 122 masters and each other. A redraw is expected to stay close to its own original; report that pair apart.
- A naming test: render each option at 48 px with no label and write what a first-time reader would most likely call it. If that name is not the subject, say so beside the option. The creative director repeats it.

## Notes and limits

Each maker writes `work/handoffs/phase-2/20261109_Stage-B-<Role>-Notes.md` (`Civic-Line-Icons`, `Utility-Icons`, `Identity`) with: what it drew, a table of every option with its file paths, the checks' figures, routine calls as "D2-xxx | decision | reason" lines, questions for Dustin with a recommendation, Tested and Not tested kept apart, and a change log. Each also writes a plate page in `work/boards/phase-2/stage-b/drawings/<role>/` that shows its drawings at the board's sizes, for the board builder to capture.

Never touch `source/`, `work/ledger/`, the Civic Line masters, the identity masters (new files beside them only), any existing board, the first reader check, or another owner's files. Do not commit or push. Reply to the main session in 200 words or fewer.

## The drawings board

A board builder, working as the engineer with the design director's layout judgment, builds `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board.html` from the makers' plate pages and notes, in the shell and style of the changes board (`work/boards/phase-2/apply-pass/`, builder's notes `20261107_Apply-Pass-Board-Builder-Notes.md`).

- **Cards, in this order:** the six redraws; Testify and Contact an official; the utility set; the pixel-fit pillar icons; the end mark; the lockmark masters; L6 centered.
- **Each card shows:**
  - the options at true size beside the master or original at the sizes the final brief names: redraws at 24, 48 and 128 px; utility icons at 16 and 24 px on Newsprint and Charcoal; pillar icons at 16, 24, 48 and 96 px; the end mark in a line of text; the lockmark at 16, 24, 34, 40 and 48 px
  - each option's naming-test result and look-alike figure
  - whether it stays within DR-135 (redraws only)
  - the creative director's recommended option with a one-line reason (D2-499)
  - what Dustin approves by name
- **The reply panel:** one line per card with option buttons and an "I approve by name" box, as on the changes board. Cards are numbered with plain numbers, with no letter prefix that clashes with board A, Board 6, the changes board or chapter codes.
- **The scores:** the creative director's scores on the six criteria for each card, with any drawing under 4 flagged (D2-499).

The editor copy-edits every word on the board before the creative director scores it (D2-500).
