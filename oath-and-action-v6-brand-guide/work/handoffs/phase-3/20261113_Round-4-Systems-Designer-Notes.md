# Round 4 notes: systems designer, DR-265 and Rules 15.19 to 15.21

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the systems designer (a general-purpose agent briefed as the designer of chapters 11, 12 and 15's systems plates) for `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, under contracts R4-5, R4-6 and R4-7, DR-265, DR-267 and DR-270. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Status

21:42 UTC. **Ready for sign-off and tests: DR-265 in chapters 11, 12, 15 and 17, and Rules 15.19, 15.20 and 15.21 as built.** For the accessibility lead: 15.20 and 15.21 are built, and 15.20's L56 now turns red when Reform R-04 is chosen (fixed 21:38, its unlit case given no paint 21:41); the step space in 15.19 was in place at 21:34. Every generator check passes; the strict build `guide12.html` (21:41) exits 0 with 0 warnings, chapter 15 at 381,215 bytes. The editor's first-read words are applied. Captures of all 51 changed plates at five widths on both grounds: 510, 0 flagged (from `guide9.html`, before the editor's words and the red fix). Running when the machine's load is under 4: the behavior test with L56's stroke check and fresh captures of 15.19 to 15.21 from `guide12.html`.

## Summary

**DR-265 and DR-267.** Every loop drawing I own prints each variable's own title (`nodes[].title`) where it printed the loop's chain label: Rules 11.14 and 11.16 (`apply_systems_ch11_ui.py`), Rule 12.5's two plates (`stage_b_ch12_systems_build.py`), Rules 17.3 and 17.4 (`stage_c_ch17_build.py`) and every plate of chapter 15 that drew a variable (`phase3_ch15_build.py`), each read by script from the atlas. Chapter 15 now prints one name per variable in every drawing, a loop's or not, so Rule 15.2 states the rule, and Rule 15.15's failure plate draws the one fault on purpose (Variable C3 by its chain label in Loop B4, its title in Loop R10). Rule 13.4 prints no chain label (its plates carry the loop's title and connection names, the atlas's own), and the engineer's code sets for Rules 18.22 and 18.23 already print the titles; a rescan of the page finds no chain label in any loop drawing.

**Re-laid under the data lead's ruling (e).** Every title wraps at word breaks onto three rows at most in its pill, never cut. Pills that share a row now take the widths that hold both titles in the fewest rows (each keeps the 130 px base where it can), and a pill stays at least half again as wide as it is tall. Loop B1a (Rule 15.1) could not hold its two titles side by side in three rows each, so it draws one pill above the other, at one width, steps down the right and up the left, step 2 of the ruling. A three-variable loop's lower row may close to 6 px, and where its ID would crowd the lower arch it takes two rows and the arch drops 18 px. No drawing reached step 3 (chips and a key).

**Rules 15.19 to 15.21** (ruling (f)):
- 15.19 steps Loop R1 on Rule 18.22's markup with no script of its own (C-1). The drawing follows `data-oa-at`: the current step on the selected band with its words bold, the steps ahead and the variables not yet reached muted, never red. Steps are numbered by a CSS counter; with scripts off and on paper the list is the still sequence and the buttons hide.
- 15.20 offers Reforms R-03 and R-04 on Loop R4a as Rule 18.3's radio group; the checked radio shows its panel and lights its targets through CSS, scripts on or off; the shell writes the status line (C-2); qualifications and assumptions sit in Rule 18.8's disclosure.
- 15.21 draws Connection L55 with what the model holds on the model's own steps (sign, grade on the ladder, delay class, no strength), against a still picture of a 0 to 100 slider whose 70 the plate names as its own.

**Weight (reported, DR-271).** Rules 15.19 to 15.21: 49,764 bytes (plates 35,498, rule entries 8,288, styles 5,105, the shell's listener 873), against R4-6's 75,000. Chapter 15 in the final strict build: 381,215 bytes of its 600,000.

## DR-265 list

Read by script: `dr265_scan.py` in my scratch folder (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/systems-designer/`) over `guide0.html`, a strict build of HEAD 829d0db8 (`python3 -I work/build/scripts/phase-2/guide_build.py --strict`, exit 0, 0 warnings). It takes every `loops[].chain_labels` entry whose variable's `nodes[].title` differs (54 of the 61 chain entries name a variable, and 53 of those differ from its title; 24 variables, one label each; the other 7 entries are the conceptual loops' stations), reads each specimen's SVG text (each `<text>` and `<tspan>` a line, so a label wrapped over two lines is found), its HTML text, its alt and attributes and its scripts, masks the atlas's own longer strings first (loop titles such as "Safe seats shift accountability to small primary electorates", connection names such as "Safe seats make the primary decisive", reform titles), and matches each label without regard to case, so the stepper's "money in politics" counts.

### Loop drawings that print a chain label, by owner

| Chapter | Rule | Specimens | Variables whose label prints | Owning generator | Owner in round 4 |
|---|---|---|---|---|---|
| 11 | 11.14 | `s-11-14-correct` (the live stepper, Loop R1: ready line, step lines, alt), `s-11-14-failure` (its ready line) | A1, B1, E1 | `work/build/scripts/phase-2/apply_systems_ch11_ui.py` (`loop_steps()` reads `chain_labels`), chapter file through `apply_systems_ch11.py` | Systems designer |
| 11 | 11.16 | `s-11-16-correct`, `s-11-16-failure` (the small figure of Reform R-32 on B2 and C3, and the alts) | B2, C3 | `apply_systems_ch11_ui.py` (`YIELD_PILLS`) | Systems designer |
| 12 | 12.5 | `s-12-marker-correct`, `s-12-marker-failure` (Loop R10's first step with Reform R-01's marks; the notes and alts) | C1, C2 | `work/build/scripts/phase-2/stage_b_ch12_systems_build.py` (`vname()`, from chapter 10's label table) | Systems designer |
| 15 | opener, 15.1 to 15.4, 15.6 to 15.16 | `s-15-opener`; correct and failure plates of 15.1, 15.2, 15.3, 15.4, 15.6, 15.8, 15.10, 15.11, 15.12, 15.13, 15.14, 15.15; correct plates of 15.7, 15.9, 15.16 and 15.9's failure; the rule text and alts with them | A1, A4, A6, B1, B2, B3, B4, B5, B6, C1 to C5, D1, D2, D4, D5, D6, D7, E1 | `work/build/scripts/phase-3/phase3_ch15_build.py` (`short()`, `LOOP_NAME`) | Systems designer |
| 17 | 17.3, 17.4 | `s-17-3-correct`, `s-17-4-correct` (Loop R1's first step, "Wealth concentration raises money in politics", and the names under it; 17.4's script and alt) | A1, B1 | `work/build/scripts/phase-2/stage_c_ch17_build.py` (`MECH_NAMES` and the step words at its line 295) | Systems designer |
| 18 | 18.22 | `c-18-loop-stepper--light`, `c-18-loop-stepper--dark` (the code set, Loop R1), `s-18-22-anatomy`, `s-18-22-failure`, and the rule's alts | A1, B1, E1 | Code set `work/build/guide/code/c-18-loop-stepper.html` and `.keys.json`; anatomy `stage_c_ch18_anatomy_build.py`; failure plate and keys files `stage_c_ch18_build.py` (its lines 1352, 1631, 1954) | Engineer (code sets, under DR-267) |
| 18 | 18.23 | `c-18-diagram-controls--light`, `--dark`, `s-18-23-anatomy` | A1, B1, E1 | Code set `work/build/guide/code/c-18-diagram-controls.html` and `.keys.json`; anatomy `stage_c_ch18_anatomy_build.py` (its lines 1127 and 1129); keys files `stage_c_ch18_build.py` (its line 1970) | Engineer (code sets, under DR-267) |

Chapter 15's three plates that print no chain label: 15.5 and 15.17 print titles already (RF-16, RF-16a), and 15.18 draws Loop B2's two conceptual stations, "Household hardship" and "Automatic support (UI, credits)", which name no variable in the atlas (`B2`'s chain holds `A4 hardship` and `Automatic support`), so they stay as stored, with the line that ties the first to Variable A4.

### Rule 13.4: no chain label prints

`s-13-4-correct` and `s-13-4-failure` print Loop R10's title and the names of Connections L08, L25, L53 and L42, all the atlas's own (`loops[].title`, `links[].name`). The first scan's "Safe seats" sits inside those names ("Safe seats shift accountability to small primary electorates", "Safe seats make the primary decisive", "Incumbent-drawn maps create safe seats"). Neither plate draws a variable's pill or prints a chain label, so DR-267 asks nothing of `phase3_ch13_build.py`. For the editor to confirm.

### Matches that are not loop drawings, which stay

- Chapter 10 (Rules 10.1, 10.4, 10.6, 10.8, 10.9 and the opener): the Civic Line icons' approved names (DR-185, DR-144), CL-026 "Executive unilateralism" among them. DR-267 keeps them.
- Rule 11.12 (`s-11-12-correct`): the symbol search's row data, which holds the same approved icon names.
- Rule 18.6 (`c-18-masthead--light`, `--dark`): "Money in politics" is a topic in the masthead's menu, not a variable.
- Rule 12.7 (`s-12-locator-*`): "How safe seats move the real choice to the primary" is an invented view header.
- Rules 14.15, 14.49 and 14.76 (`s-14-s03`, `s-14-s08`, `s-14-s06`): "household security" and "affective polarization" in plain words in chart notes.

## Routine calls

- D3-xxx | Rule 13.4's plates print no chain label, so DR-267 changes nothing there | They print the atlas's loop title and connection names; the first scan matched "Safe seats" inside those names
- D3-xxx | In chapter 15 every drawing that holds a variable prints its own title, a loop's or not, and the short-name rule (D3-368) and RF-16's split for D1, D2, D4 and D6 retire | DR-265 asks one name per variable; a chapter that printed titles in its loops and chain labels in its cards would print two
- D3-xxx | Rule 15.2's rule now says a pill holds the variable's own title in every drawing, and its card drops the title beside the chip | The pill above the chip already prints the title; the rule teaches DR-265 where the chapter names its variables
- D3-xxx | Rule 15.15's failure keeps Variable C3's chain label, "Electoral pressure", in Loop B4 as its fault, and the correct plate reads "The atlas’s glossary defines it as electoral pressure" | The failure's lesson is one variable under two names; "Electoral pressure" is also the glossary's own term, quoted as such; the generator allows exactly these and fails any other chain label
- D3-xxx | Pills that share a row take the widths that set both titles in the fewest rows (three at most), keep the 130 px base where they can, set their rows as evenly as the words allow, and stay half again as wide as they are tall | Ruling (e), step 1; greedy wrapping left "new" and "and" alone on rows, and a short title on three rows drew a disc
- D3-xxx | Loop B1a (Rule 15.1) draws one pill above the other at one width, step 1 down the right and step 2 up the left, its ID between them above the tags | Ruling (e), step 2: "Policy advantages for wealthy and organized interests" and "Ability to investigate and enforce the rules" cannot share a 296 px row in three rows each; the rule's "two pills of one size" holds
- D3-xxx | A three-variable loop's lower row may close to 6 px, its upright steps land on the shared flat edge where the pills have one, and its ID centers on the lower arch, on two rows with the arch 18 px lower where one row would crowd it | Ruling (e), step 2, for Loops R1, R4a and B4; the ID had run into the arch's upright ends
- D3-xxx | The read-aloud line turns a title that asks how often into "the primary decides the winner more often" | "More how often the primary decides the winner" is not English
- D3-xxx | The opener's letter C moves to the left of "Loop R13" | The wider pills leave 12 px between them, where it stood
- D3-xxx | Rule 11.16's note reads "In our atlas, more local reporting raises officials’ risk of losing office", and Rule 12.5's alts say "the connection from Seats with little electoral competition to how often the primary decides the winner" | The old words used the chain labels; a plural title would have needed its own verb
- D3-xxx | Rule 15.19's title reads "Step a reader through a loop one connection at a time, with a still sequence." | The rule list's title runs 16 words, past the fifteen chapter 13's check holds, as 15.1 and 15.8 did in round 1; number and subject unchanged
- D3-xxx | Rule 15.19's current step takes the selected band behind its line and its two pills, with its words bold; the steps ahead and the variables not yet reached take the muted ink; no line grows heavier | Ruling (f) names the selected look; Rule 15.1 keeps one line width so width never reads as strength; the band differs by lightness, so it holds in grayscale (the accessibility lead asked "heavier"; the band does that work)
- D3-xxx | Rule 15.19 prints Loop R1's qualification once, under the reason line, as "The atlas’s limit on the loop" | Ruling (f); after the controls so the list and the buttons stay together
- D3-xxx | Rule 15.20 draws every target of both reforms with Rule 12.5's red marks ready under one data-red job, and its CSS shows the checked reform's; L42 belongs to both | The choice works with scripts off; the guide check needs every red mark under data-red
- D3-xxx | Rule 15.20 prints each route's stored `who` line unlabeled, as Rule 15.16 does | R-03's federal route stores an action there (the research lead); no route row in chapter 15 labels it "Who acts"
- D3-xxx | Rule 15.20 hides its radio group on paper and prints a line naming the reform the drawing shows | The accessibility lead's print section
- D3-xxx | Rule 15.21's correct plate prints L55's sign, its grade marked on the five-grade ladder and its delay among the three classes, with "None in the model" for strength and the atlas's own sentence | Ruling (f)'s recommendation; the ladders show the model's own steps without any control
- D3-xxx | The plates may name `@media print` and `@media screen`, and no other medium | The still sequence on paper; the plates still compose by their frame alone
- D3-xxx | The code sets' utility icons in 15.19 and 15.20 draw by `<use>` from the sprite, their classes kept | The guide build warns on an inlined sprite drawing
- D3-xxx | The generator reports chapter 15's bytes and R4-6's figure and stops on neither | DR-271

## Requests

### To the editor
1. Rule 13.4: the scan finds no chain label on its two plates (above). Nothing to change unless you read it otherwise.
2. **Words pass, Rules 15.19 to 15.21** (the generator's data; I own the file and will apply your lines, or you may write them once I report, D3-669): each rule's rule, why, basis, captions, specs and builders; group 4's line ("A control lets a reader move through what the atlas holds, one step or one reform at a time, and offers nothing the atlas does not hold."); the intro of related chapters 17 and 18; the six alts; and the plate words: 15.19's ready line, step lines and "more" words (built in `stepper_steps()`), "The atlas’s limit on the loop"; 15.20's legend "Show one reform on Loop R4a", each panel's first line, the heads ("Its targets", "Its band", "Effects by outcome family, as of October 15, 2026", "Routes, with the date each was checked"), the disclosure's summary and its three lines, the print line; 15.21's heads ("Sign", "Grade, on the atlas’s ladder", "Delay, in the atlas’s three classes", "Strength"), "None in the model. The atlas’s record for the connection:", the failure's slider words and its note. Rule 15.19's title is shortened (routine calls).
3. **DR-265's changed lines:** 15.1's alt and Pill spec; 15.2's rule, Name spec, builders and alt; 15.15's rule, Shared variable spec, glossary line and both alts; the alts of the opener, 15.3, 15.7 to 15.14 and 15.16, where the titles now stand; Rule 11.16's note; Rule 12.5's two alts; Rules 17.3 and 17.4's alts, status words and caption.

### To the data visualization lead
1. **Sign-off of DR-265's re-laid drawings** under your ruling (e): every drawing held at step 1 or step 2; none reached step 3. The one step 2 re-lay of form is Loop B1a in Rule 15.1 (one pill above the other); the others widened pills or moved an ID. Captures: `capF/` (Newsprint) and `capFd/` (Charcoal) in my scratch folder, at 1440, 1024, 768, 390 and 360 px.
2. **Sign-off of Rules 15.19 to 15.21** as built to ruling (f): 15.19 on Loop R1 (current step on the selected band, never red); 15.20 on R-03 and R-04 with R4a, no status text, every route "Not checked", the qualification and assumptions verbatim in the disclosure (`effects_confidence`, the remedy grade and text, `tradeoffs`); 15.21 on L55, the slider's 70 named as the picture's own. Each plate logs one example: the chapter holds 30, D02 at 7.

### To the accessibility lead
1. **Both live plates are built for your tests** (`s-15-19-correct`, `s-15-20-correct`, manifest `"interactive": true`). As specified: the drawing inside the stepper's root after the grade line, `aria-hidden` with no stop; the CSS counter; the scripts-off and print rules; `forced-color-adjust: auto` on the plate's root with its own ground and `none` on the drawing with its own; the controls inside chapter 15's 320 px rule; `data-oa-panel`, `data-oa-for`, `data-oa-say` and the `.vh` status line after the fieldset. One difference: the current step differs by the selected band (lightness) and bold words, not a heavier line (routine calls). For your key paths: N is 3; R-a is R-03 and R-b is R-04, and there is no R-c, so ArrowDown from R-04 wraps to R-03.

### To the engineer
1. DR-267 for Rules 18.22 and 18.23: landed on your side; my rescan finds no chain label in chapter 18.
2. For the main session: the strict build at 21:39 warns once, on Rule 26.7's token table (`s-26-token-table` is not what tokens.json 6.0.0-gate3.3 makes; `token_table_build.py`), which is not chapter 15's.

### Answers to the accessibility lead's requests from the tests (21:38 UTC)
3. **15.19's space.** Done at 21:34, before your test build, I expect: each step's line and its more words are joined by `&#32;` (the plate minifier closes a plain space between two tags), and the strict build carries `politics.</span>&#32;<span class="oa-stepper-more">`.
4. **15.20, L56's red.** You read it right: my CSS showed L56's lit marks but left their ink, and my behavior test checked only that `.hi` showed. Fixed at 21:38: when a reform is chosen, its targets' lit marks take the red line on the ink case and the red head, and its pills the 3 px red outline, by the same values the class `rt` and `rp` draw; the other reforms' targets go back to ink. The behavior test now reads L56's computed stroke and head against L42's red (rerun pending under the load limit).

## Tested

All in my scratch folder (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/systems-designer/`), on this container's Chromium (Playwright).

- **Generators and their checks.** `python3 -I work/build/scripts/phase-3/phase3_ch15_build.py`: every check passes, round 1's to round 4's. New this round: no chain label in any plate, alt or line of the chapter but Rule 15.15's fault (exactly once) and the glossary's term; every DR-265 title at three rows or fewer in its pill; a stacked loop's steps on both pills' flat edges, its words inside the artboard and its ID clear of its tags; a three-variable loop's ID clear of its lower arch; no script in any plate; no working control in any failure plate or in 15.21's; 15.19's markup as C-1 lists it, its steps equal to Loop R1's connections; 15.20's radios one group in ruling (f)'s order with one checked, each with its panel and its `data-oa-say` line, and the shell's hooks; 15.20's red marks equal to the union of both reforms' targets (four); every route "Not checked" per its own record; Rule 01.9 over 30 examples (D02 at 7). `apply_systems_ch11.py`, `stage_b_ch12_systems_build.py` and `stage_c_ch17_build.py` run clean.
- **The generator chain** (handoff V12, with V15's `stage_c_ch17_build.py`, then chapter 15's), run five times (`chain.sh`); after runs 2, 3, 4 and 5, `git status` lists no file I own, and between runs 4 and 5 only other owners' files changed (chart kit, notes), so nothing crossed.
- **Strict builds.** `guide12.html` (21:41, final): exit 0, 0 warnings; chapter 15 at 381,215 bytes; the page at 11,500,550, projected 15,051,454. `guide10.html` (21:37): exit 0, 0 warnings; chapter 15 at 380,465 bytes; the page at 11,498,314, projected 15,050,450. `guide11.html` (21:39, after the 15.20 red fix): exit 1 on one warning that is not chapter 15's (Rule 26.7's token table, above); chapter 15 at 381,180 bytes; the page at 11,500,236, projected 15,051,456. Rules 15.19 to 15.21: 49,764 bytes with their styles and the shell's 873-byte listener (reported, DR-271).
- **DR-265 rescan** (`dr265_scan.py`, case-insensitive, atlas strings masked) on `guide10.html`: no chain label in any loop drawing of chapters 11, 12, 13, 15, 17 or 18, but Rule 15.15's deliberate pair; chapter 10's and Rule 11.12's icon names, Rule 18.6's menu topic, Rule 12.7's header and three plain-word notes in chapter 14 remain, as listed above.
- **V7 check** (`v7_check.py --page guide9.html`): PASS, 0 failures; chapter 15 at 145 chips.
- **Captures, measured by script** (`cap.js`: type under 13 px, text outside its stage, two SVG labels overlapping): every changed plate, 51 of them (chapter 15's 43, Rules 11.14 and 11.16's four, Rule 12.5's two, Rules 17.3 and 17.4's two), at 1440, 1024, 768, 390 and 360 px, on Newsprint (`capF/`, 255 captures, 0 flagged) and with the stage set to Charcoal (`capFd/`, 255 captures, 0 flagged), from `guide9.html`.
- **Read by eye:** chapter 15's loop plates at 390 (opener, 15.1, 15.6, 15.7, 15.11, 15.13 to 15.16), its other plates at 390 (15.2 to 15.5, 15.8 to 15.10, 15.12, 15.17, 15.18), 15.6, 15.11, 15.13, 15.16 and the opener at 1440, 15.1 at 1024, 15.15 and 15.20 at 360, 15.19 at 768; Rules 11.14, 11.16, 12.5 and 17.4 at 1440; 15.19, 15.20, 15.1 and 12.5 on Charcoal at 1440; 15.19 to 15.21's six plates at 1440 and 390.
- **Behavior test** (`live.js`) on `guide8.html`, 11 of 11 passing: 15.19 at load (live, `data-oa-at="0"`, controls shown), Next step by keyboard (status "Step 1 of 3: …", focus kept, band on step 1 alone, step 3 muted), the last step (Next unavailable, the loop named reinforcing), print emulation (buttons hidden, no band, every step in ink), scripts off (controls, status and reason hidden, no step current, numbers shown); 15.20 at load (R-03's panel alone, status silent), ArrowDown (R-04 checked and focused, its panel, status line "Reform R-04 acts where the marks turn red: on two connections."), print emulation (both panels, the line naming R-04), scripts off (the radios still choose and the panel follows).

## Not tested

- Rule 15.20's print emulation hid its radio group only after a later fix, and L56's red after another (21:38); the rerun of the behavior test with the stroke-color check and the recaptures of 15.19 to 15.21 after the editor's words wait on the machine's load (see Status when they land).
- The guide check (`guide_check.js`), quick or full, on these builds: not run, to keep browser load down; the accessibility lead ran its tests on 15.19.
- A screen reader; forced colors; 200 percent text; a 320 px window (the accessibility lead covers these for 15.19 and 15.20).
- Rule 12.5's plates on Charcoal: they draw for Newsprint only, as before this round (their wires use Newsprint's tokens); DR-265 changed their words only.
- Print of the shell's own `beforeprint` disclosure opening (C-3): Playwright's print emulation does not fire `beforeprint`.
- Firefox and Safari.

## Files

- `work/build/scripts/phase-3/phase3_ch15_build.py` (modified), with what it writes: `work/build/guide/chapters/15-systems-graphics.json`, `work/build/guide/specimens/s-15-*.html` (37 rewritten, 6 new: `s-15-19-correct`, `s-15-19-failure`, `s-15-20-correct`, `s-15-20-failure`, `s-15-21-correct`, `s-15-21-failure`), `work/build/guide/specimens/manifest-systems-graphics.json`
- `work/build/scripts/phase-2/apply_systems_ch11_ui.py` (modified), with `work/build/guide/chapters/11-icons.json`, `s-11-14-correct.html`, `s-11-14-failure.html`, `s-11-16-correct.html`, `s-11-16-failure.html`, `manifest-systems.json`
- `work/build/scripts/phase-2/stage_b_ch12_systems_build.py` (modified), with `s-12-marker-correct.html`, `s-12-marker-failure.html`, `manifest-systems.json`
- `work/build/scripts/phase-2/stage_c_ch17_build.py` (modified), with `work/build/guide/chapters/17-motion-and-states.json`, `s-17-3-correct.html`, `s-17-4-correct.html`, `manifest-motion.json` and the generator's record `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch17-Figures.json` (its token set line only)
- `work/handoffs/phase-3/20261113_Round-4-Systems-Designer-Notes.md` (this file)
