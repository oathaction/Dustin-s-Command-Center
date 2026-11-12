# Brief: applying Dustin's board 1 answers

Oath & Action Edition 06, Phase 3, November 12, 2026. Written by the main session for four owners. Paths are relative to `oath-and-action-v6-brand-guide/`. This is one short pass before round 1. It applies four answers Dustin has already given and builds nothing new.

## Dustin's answers

Dustin, November 12, on board 1: "As recommended, and I approve the smaller photographs". Logged as DR-236 to DR-239 in `work/ledger/20261020_Decision-Log.md`. Read those four rows, D3-87, D3-104, D3-187, D3-190 and D3-193 before you start.

| # | Answer | Owners |
|---|---|---|
| DR-236 | The data palettes are approved: the two new values #828A9D and #505C7D for diverging pair B on Charcoal, and the four-ink order Charcoal, Verdigris, Prussian, Stone, with Stone always hatched. The tokens drop "proposed" from their descriptions in the next pre-release | Engineer |
| DR-237 | Chapter 13 is approved as built | Nobody: chapter 13 does not change |
| DR-238 | Page weight takes the combined option: chapter 01's two photographs (the Rosa Parks photograph by the Architect of the Capitol, Rule 01.6; the Corps of Engineers public meeting at Lake Isabella by Zianno, Rule 01.8, shown twice) go to 1,200 px wide; each chart's drawing data is carried compressed; every table stays live text; chapter 14's stop rises to 2.804 MB; nothing comes from Phase 4's share. Every original and its record is kept | Research lead, editor, engineer |
| DR-239 | Chapter 02 keeps "shrank in seven of the 57 months charted", and the sentence "Only the October 2025 and February 2026 drops pass the survey's margin of error." joins it in H08's after line, the H06 example and S14's note | Editor, Explainer maker |

## Read first, every owner

`CLAUDE.md`; your role file in `.claude/agents/` (the Explainer maker has none and reads the round 0 brief's description of the role); `work/handoffs/phase-3/20261112_Next-Session-Handoff_V17.md` section 2A; your own round 0 notes file; chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`. The engineer also reads its notes' "Board 1 weight options" section; the Explainer maker reads the engineer's notes' "Contracts" section.

## Each task

**Research lead** (start now).
1. From the two originals in `work/build/assets/photography/` (`20261106_Photo-Rule-01-6-Rosa-Parks-Lying-In-Honor-Capitol-Rotunda-2005.jpg` and `20261106_Photo-Rule-01-8-Corps-Of-Engineers-Public-Meeting-Lake-Isabella-2014-Zianno.jpg`), make one rendition each at 1,200 px wide, by the method the engineer measured for board 1: Lanczos resampling, JPEG quality 85, progressive, color profile and any rights metadata kept. Name each `20261112_` plus the original's title words plus `-1200-Wide.jpg`, beside the originals. Write a record beside each, in the shape of the original's `.json`, naming its original, method, pixel size, bytes and SHA-256.
2. Check each rendition: pixel width 1,200, height in proportion, bytes near the engineer's board 1 figures (Rosa Parks about 223,719; Zianno about 143,243), and a side-by-side look at 600 px display width and at 2x against the original, saved to your scratch folder.
3. Add the renditions to the rights ledger (`work/research/20261020_Rights-Ledger.md`, beside rows pho-01 and pho-04) and to any research ledger row that records these files, stating the original stays the source and the rendition is what the guide shows (DR-238). Never edit or move the originals.
4. Tell the main session the two file names as soon as they are written, so the editor can switch to them.

**Editor** (start now on part A; part B when the research lead's file names arrive).
- A. DR-239 in chapter 02. Add "Only the October 2025 and February 2026 drops pass the survey’s margin of error." (curly apostrophe, as the guide sets text) after "payrolls shrank in seven of the 57 months charted" in H08's after line and in the H06 example, through chapter 02's generator and its source files (`guide_editor_ch02.py`, `guide_editor_common.py`, and the voice content it reads), never by editing an output alone. Check the result reads as one plain passage under chapter 02's rules. Chapter 13 does not change (DR-237).
- B. DR-238 in chapter 01. Point `guide_editor_ch01.py`'s two photograph paths (`PHOTO_PARKS`, `PHOTO_ZIANNO`) at the research lead's renditions, and any "Files" or builders line that names them. Then run the chain V16 sets: `guide_editor_build.py`, then `stage_b_identity_ch01.py` after it, every time (the editor's chapter 01 build deletes specimens it did not write). Alt texts, credits and captions stay as they are. Confirm the chapter 01 plates show the renditions at their display size and that `git status` shows only the files you meant to change.

**Engineer** (start now).
1. DR-236. A pre-release `6.0.0-gate3.2` under Rule 26.8: every token description that says "Proposed, until our founder and editor approves it." or "The second job is proposed, until our founder and editor approves it." loses that sentence, and the machine field `proposed: 'board 1'` goes. The change note records the approval in reader words with no decision code in the reader text (D3-119). Names and values do not change. Rebuild tokens (`node scripts/phase-2/tokens_build.mjs` from `work/build`), regenerate the token table, and pass the token tests.
2. DR-238. Adopt chart data carried compressed in the guide build, as `weight_options.py` measured it: each chart's data island deflated and inflated by the kit at load, every table equivalent kept as live text. Prove no reader loses anything: scripts off (description, the drawing-needs-scripts line and the table), print, forced colors, export parity, and page-to-Node parity on S01 to S16. Then set chapter 14's stop to 2.804 MB (2,803,941 bytes, D3-190's recommended figure) in `guide_charts.py`'s ceiling and allocation, keep it a hard stop in every mode, keep the 15.5 MB projection test, and update the build's self-test planted faults to the new stop.
3. Add a per-plate line to the build report: chapter 14's room divided among the specimens still to come, so each round sees its share per plate (the creative director advised about 15 KB). State the figure you compute and how.
4. When the editor's chapter 01 change lands, run a fresh strict build and `weight_options.py`, and report chapter 14's projection, the page projection and the room under 15.5 MB with the photographs and compression both in.

**Explainer maker** (start now). DR-239 in S14. In `work/build/chart-kit/specs/s14.json`, follow the note "Payrolls shrank in seven months: January, June, August, October and December 2025, and February and July 2026." with "Only the October 2025 and February 2026 drops pass the survey’s margin of error." in the same note or the next, whichever reads better at 358 px. The title keeps its words. Remove D3-87's hold from `notes_internal` and say DR-239 settled it. Run `node work/build/chart-kit/oa-chart.mjs build s14 --out <your scratch folder>/kit-out` and fix every failed check in the spec. Do not overwrite round 0's board captures in `work/boards/phase-3/round-0/specimens/`; they are the record of what Dustin saw. If the margin's figure should print, write it as a request with its source (D3-171) rather than adding it yourself.

## Notes and limits

- Each owner adds a section `## Board 1 apply` to its own round 0 notes file (`work/handoffs/phase-3/20261111_Round-0-<Role>-Notes.md`; the Explainer maker's is `...-Explainer-Notes.md`) with: what changed, routine calls as `- D3-xxx | decision | reason` lines, requests, Tested and Not tested.
- Write only the files your task names. If you need a change in another owner's file, write it under requests and tell the main session.
- Never touch `source/` or `deliverables/`. Never edit Atlas V7. Do not commit or push. Never run `git checkout --` or any command that discards changes.
- Scratch work goes to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f15cd04b-21be-5dde-a467-804e951756a2/scratchpad/phase-3/board-1-apply/<your-role>/` by absolute path, never into the repository by a relative path.
- Python that reads supplied or downloaded files runs with `-I`.
- No em dashes. Report what you tested and what you did not as separate lists.
- Your final message: under 150 words, the paths you wrote, anything blocking.
