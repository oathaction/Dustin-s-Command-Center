# Brief: stage C round 2, the fix pass

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the main session for the owners who fix what round 2's reviewers found. It carries out the second half of "Order of work" 4 of `20261110_Stage-C-Brief.md`: one fix pass, then DR-191's short second pass on any item still under 4, the editor's read and the creative director's rescore. The studio's calls for this pass start at D2-1544.

## The reports

Every item below is named by its report and number. Read your items in the report itself, where each has its place, the quoted fault and the fix.

| Code | Report in `work/handoffs/phase-2/` | Score |
|---|---|---|
| CD | `20261111_CD-Review-Of-Stage-C-Chapters.md` and `20261111_Stage-C-Round-2-CD-Scores.json` | 17: 3,4,3,4,4,4; 18: 3,4,3,5,4,4; 19: 3,4,4,3,5,4; 26: 3,4,4,4,4,4; changed parts of 01 to 11: all 4 |
| BE | `20261111_Stage-C-Round-2-Red-Team-Brand-Evidence.md` | 3 of 5; 4 Must fix, 8 Should fix |
| PP | `20261111_Stage-C-Round-2-Red-Team-Plain-Production.md`, with the panel's files in `stage-c-round-2/production-test/` | 3 of 5; 2 Must fix, 13 Should fix |
| CA | `20261111_Stage-C-Round-2-Red-Team-Craft-Access.md` | Still running; its items reach you as an addendum to this brief and a message |

## Calls the main session makes now

These settle the choices the reports leave open. Each is logged in the decision log.

1. **Red stays off Prussian (CD-M2, BE-M1, BE question 1).** `oa.color.field.ground.onCharcoal` resolves to Charcoal, so a field on Charcoal shows by its strong Newsprint edge and an error's 4 px Pillar Red bar sits on Charcoal at 4.49 to 1. No new value. It ships in the same token release as DR-218, with one change note. Rule 05.3 already forbids red on Prussian, so this follows an approved rule; D2-1469 is withdrawn. The selected band on Charcoal stays Prussian, and the guide check gains a step that fails any red pixel touching Prussian, in every stage, in both themes, after pressing Send in every form.
2. **The primary button and the ask stand on separate rows (CD-M2, BE question 3).** The hover token stays. Rule 18.1 gains the sentence that the ask stands apart from a primary button, whose hover turns Prussian.
3. **Chapter 18's atlas samples leave R-01's subject (BE-M4).** They move to the housing variables or to work and pay, with their real grades and a dated source, as D2-278 and D2-958 moved earlier examples. Where a disclosure shows real atlas lines, it drops "Illustrative". Rule 18.24's examples become "Loop R1" and "Reform R-04". The filter bar and the search keep R-01 to R-12 in the atlas's own order, as typed chips (BE-S2). Whether this becomes a standing rule for the whole guide is Dustin's call, asked on board C.
4. **Loop R1 carries its grade (BE-M3).** Its heading keeps V7's title as the loop's name, in quotation marks, and a line under it gives the grade: "Our atlas grades this loop plausible: its middle step is the least certain, and it runs only on issues where large donors and middle-income voters want different things." The same words go in both chapter 18 sets and both chapter 17 players. CD-S9's last step closes the loop: "raises wealth concentration, where the loop began".
5. **An identity player rests on its master (CD-M1).** Play steps to the first frame and runs to the master; Reset returns to the master and, at rest, is unavailable with the line "The mark is at rest on its master." The dashed squares go. A state or mechanism player still rests on its first frame. Rule 17.3 says both, and its builders text and anatomy key agree.
6. **The closing token block (PP-M2).** The engineer either builds each chapter's block from every property its code and specimens read, with their dependencies, tested by the copy check, or drops the "or copy this chapter's block" route and the "works on its own" claim. Either way, the words beside a block say it holds no themes, so a themed product links tokens.css. The engineer's call under D2-266, logged with its test.
7. **A surface class pins its ground (PP-M1).** PP-M1's three changes as written: Rule 26.6 says a themed product puts no surface class on the body; Rule 26.3's builders line and the closing blocks say so too.
8. **Openers for the four new chapters (CD-S18).** Each takes an `"opener"` under D2-1134: chapter 17 the ten states strip and chapter 18 a row of button, chip and choice drawn from the code sets (systems designer), chapter 19 its status counts (accessibility lead), chapter 26 the five steps (engineer). Each fits the column at true size, is a picture (`role="img"` with alt) and weighs under 6 KB.
9. **Illustrative labels (CD-S7, BE-S8).** The uppercase chip at the plate's head everywhere, as stage B set for chapters 11 and 12, in specimens, anatomy plates and live sets alike.
10. **The bills (BE-S1).** Chapter 18's stopped-in-committee story takes the next free number on chapter 11's counter (D2-848) with a new neutral title; H.99001 is filed January 16 everywhere; each failure plate's row gives a last action its own story allows. Search every chapter for each bill number after the change.
11. **Chapter 19's "met by" lines (BE-S4).** A criterion is Met only where a rule states what the criterion asks. Where no rule does, the line says Met in part, Gap with its owner, or Not used today, whichever is true. No new chapter 18 rule is written to close 3.3.4 in this pass unless the form already meets it.
12. **DR-217 is in place.** Rule 03.2's builders text already carries the sentence (the editor's fuller wording, round 1). PP-S12 asks to break that paragraph into short lines, one per lockup.

## Who fixes what

| Owner | Role file | Items | Notes file in `work/handoffs/phase-2/` |
|---|---|---|---|
| Engineer | `oa-engineer.md` | DR-218's release with call 1's field ground, one change note, 6.0.0-gate2.8; the guide check's red-on-Prussian step (call 1); CD-M3; PP-M1; PP-M2 (call 6); PP-S6; PP-S7; PP-S11; PP-S12 (Rule 26.2); CD-S14; CD-S7 and BE-S8 for chapter 26; BE-S6 (`c-26-warning`); BE-S7 (the change note's words); chapter 26's opener (call 8); the token chips for short names (round 2 brief's fix list) | `20261111_Stage-C-Round-2-Engineer-Fix-Notes.md` |
| Component engineer | `oa-engineer.md` | CD-M2 (`c-18-button`'s rows; `c-18-form` in dark after the release); BE-M3 and CD-S9 (the two loop sets); BE-M4 (`c-18-location`, `c-18-disclosure`); BE-S1 (`c-18-tracker`, `c-18-table`); BE-S2; BE-S3 (the sets' source lines); BE-S6 (`c-18-tabs`); BE-S7 (comments); PP-S1; CD-S7 (live sets); CD-S8; the renamed error token in any set that reads it, once the release lands | `20261111_Stage-C-Round-2-Components-Fix-Notes.md` |
| Accessibility lead | `oa-ux-accessibility-lead.md` | CD-M2 (Rule 18.1's sentence); BE-M2, with a stored copy of the Recommendation's text fetched from w3.org/TR/WCAG22 and a generator check against it; BE-M4 (Rule 18.24, `s-18-23-failure`, `s-18-24-failure`); BE-S1 (`s-18-10-failure`); BE-S3 (chapter 18's sources); BE-S4 (call 11); BE-S5 (chapter 19's items, with each guide's address and date read); PP-S2 to PP-S5; PP-S8 and PP-S9 (chapters 18 and 19); PP-S10; CD-S11 to CD-S13; chapter 19's opener (call 8); every keys file whose set changes; chapter 19's results, rerun last (BE-S7's words) | `20261111_Stage-C-Round-2-Accessibility-Fix-Notes.md` |
| Systems designer | `oa-design-director.md` | CD-M1 (Rule 17.3's words and key); CD-M2 (chapter 11's Charcoal stages still part their panels by an edge after the release); BE-M3 (chapter 17's players); BE-S5 (Rule 17.9); CD-S1, S2, S3, S5, S6, S10 and S17; CD-S7 (anatomy plates); openers for 17 and 18 (call 8); PP-S8 (the first "landmark" in chapter 07 and chapter 11's uses); PP-S12 (Rule 10.9); PP-S13; chapter 11's reader as chapter 18's radio group with Rule 17.10's look (D2-1151, D2-1296, D2-1390); the anatomy plates rerun once the component engineer's sets land (BE-M3, BE-M4, BE-S1, CD-S9) | `20261111_Stage-C-Round-2-Systems-Fix-Notes.md` |
| Identity designer | `oa-design-director.md` | CD-M1 (the hinge and lever players, call 5); CD-S4; CD-S15 (Rule 08.1's plate at 120 px with a fifth sample, the 48 px master at 96 px, "Social card sign-off only"); CD-S16 (Rule 08.2's dark-card words as the creative director wrote them); PP-S12 (Rule 03.2's paragraph, one short line per lockup, the record sentence dropped) | `20261111_Stage-C-Round-2-Identity-Fix-Notes.md`, a new section "## Fix pass" |
| Editor | `oa-editor.md` | After the owners: every changed string, with wording faults going back to owners in DR-191's short second pass | `20261111_Stage-C-Round-2-Editor-Notes.md` |

Each owner writes its own new sentences in this pass (D2-963). Every word follows chapter 02's writing rules.

## Order and crossings

1. **The engineer's token release comes first.** Call 1 and DR-218 change `tokens.json`, `tokens.css`, the token tests, the token table and chapter 26. Until the release lands, the component engineer and the systems designer work on items that do not depend on it; the main session tells them when it lands.
2. **The component engineer's sets come before the anatomy plates.** The systems designer reruns the plates once the sets land; the main session says when.
3. **Chapter 19's results come last,** from the main session's final guide check on the fixed page.
4. **One owner per file.** The engineer alone edits `guide_build.py`, `guide_check.js`, the shell, the tokens and chapter 26; the component engineer alone edits `work/build/guide/code/c-18-*`. A change another owner needs in those files goes through the main session. A specimen another owner draws for your chapter sits in its own manifest (D2-1267).
5. **Change words and plates only through your generators,** never in their outputs. After any change to a chapter, run the generator chain from the project folder, each with `python3 -I work/build/scripts/phase-2/`: `apply_systems_ch11.py`, `stage_b_ch10_build.py --no-draw`, `stage_b_ch12_systems_build.py`, `promotion_identity.py specimens`, `guide_editor_build.py`, `stage_b_identity_ch01.py`; then your own chapter's generator. The round 1 generators have `--check` modes: `stage_c_ch17_build.py`, `stage_c_ch18_build.py`, `stage_c_ch19_build.py`, `stage_c_ch26_build.py`, `token_table_build.py`, `stage_c_ch18_anatomy_build.py`. A clean `git status` outside your own files proves nothing crossed.

## Checks each owner runs

- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <your scratch>/guide.html`: 0 warnings. Never build over the committed chapters page.
- Look at every plate you changed at 1440 and 390 px, at 1x and 2x, in both live themes where it has them.
- The engineer: the token tests (`node scripts/phase-2/tokens_build.mjs` from `work/build`, then `python3 -I work/build/tests/tokens/run_token_tests.py`), and `guide_check.js` with its self-test after any change to it.
- The component engineer: every changed set's keys path walked in both stages at 1440 and 390 px, and its copy drawn in a blank page with tokens.css.
- The main session runs the full guide check at four widths once every owner is done.

## Notes and limits for every agent

Each agent writes its notes with: what it changed, item by item with the report code; routine calls as "D2-xxx | decision | reason" lines under a heading "## Routine calls"; questions for Dustin with a recommendation (only where a fix needs his call); Tested and Not tested, kept apart; a change log. Write notes early and add as you go, since the container can restart.

Use the scratchpad `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2-fix/<your role>/` for anything temporary, never `/tmp` itself, and set `TMPDIR` there. Run Python with `-I`. Never touch `source/`, `work/ledger/`, `deliverables/`, any asset master, any board, or another owner's files. Do not commit or push; the main session commits snapshots. Reply to the main session in 150 words or fewer. Plain spoken prose, no em dashes. Label illustrative people, places, bills and figures beside the item, and give every public policy figure its source, period and qualification.

## Addendum: the craft and accessibility report (CA)

`20261111_Stage-C-Round-2-Red-Team-Craft-Access.md` landed after this brief: 3 of 5, 2 Must fix, 8 Should fix. The copy promise holds: 16 sets, 13 with scripts, copied into blank pages draw and behave as their live stages in light, dark and forced colors. Its judgment on D2-1469 (keep the bar on Prussian, on contrast) is overtaken by call 1, which follows Rule 05.3's party reason.

**Calls on CA's items:**
13. **The token table (CA-M2 with CD-M3).** A real table whenever the plate's own width reaches 40rem, in CA's five columns (name with its CSS name and Copy under it; value with its swatch; use; tier; contrast). Each category is a disclosure, closed by default, its head giving the count; search opens every group that holds a match; a category index heads the plate. From 1280 px it breaks out over the rail as wide plates do, if its columns need the room. A name breaks only at a dot or a hyphen, and only when the cell truly lacks the room. Under 40rem the cards stay.
14. **`codeMatch` (CA-S1).** The pixel tolerance goes to 49, the measured antialiasing maximum the log records, and the check adds the computed-style comparison CA describes for every element of each live stage and its pasted copy. Record the change against D2-1519 and D2-1526.
15. **The live download (CA-M1).** In the live stages only, the build marks `c-18-download`'s ready link `data-oa-file`, so the shell serves the page's own tokens.css; the HTML panel keeps `href="tokens.css"`. The guide check's download test adds the live stage.
16. **Code panels (CA-S2).** One declaration per line in every CSS panel, long attributes and SVG path data broken onto their own lines; a panel shows about 40 lines before it scrolls, and its name says when it scrolls both ways. Chapter 18 stays under its 1.25 MB ceiling: the component engineer measures the weight before and after and reports it.
17. **Stages side by side (CA-S3).** From 80em, the two stages of a set whose content fits 32rem sit side by side, as CA lists them; the wide sets keep the stack.

| Owner | CA items |
|---|---|
| Engineer | CA-M1 (build and shell, call 15); CA-M2 (call 13, with CD-M3); CA-S1 (call 14); CA-S2 (panel height and names); CA-S3 (call 17); CA-S6 (the build's text transforms skip everything inside `.code-root`); CA-S7 (chapter 26's plates); CA-S8 (the rail's cue and the current chapter scrolled into view) |
| Component engineer | CA-S2 (formatting in `c-18-*`, call 16, with the weight measured); CA-M1 (a note only if the set's markup changes) |
| Systems designer | CA-S4 (with CD-S6); CA-S5 (with CD-S3); CA-S7 (anatomy plates `s-18-10` and `s-18-16`) |
