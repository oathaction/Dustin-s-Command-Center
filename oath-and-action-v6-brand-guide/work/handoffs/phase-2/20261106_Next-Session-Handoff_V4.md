# Handoff for the next session: Oath & Action Edition 06 (fourth handoff of November 6)

Written November 6, 2026, when Dustin's chat neared 75 percent of its context. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. Decision log entries for this chat end at D2-247 (and DR-92). The starting prompt is in section 8. It replaces `20261106_Next-Session-Handoff_V3.md`.

## 1. Where things stand

| Phase | Status |
|---|---|
| 0, 1 | Done (Gates 0 and 1 approved) |
| 2 Identity, foundations and symbols | **Active.** Chapter 02's writing rules approved (Board 5); tokens built; reader check published; chapters 01 to 08 built and under red team review for stage board A |
| 3 Data visualization and systems | Opens with the chart kit on the new tokens (DR-63) |
| 4, 5 | Not started |

**Done in this chat** (decision log DR-73 to DR-92 and D2-133 to D2-247; change ledger C-026 to C-028):
- **Board 5 answers**: all ten recommendations accepted (DR-73 to DR-83), folded into `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`, which is chapter 02's binding writing section. `CLAUDE.md` names it (DR-92). Four V5 lines retired (DR-77, C-027).
- **Analyst questions answered** "Go, all recommendations" (DR-84 to DR-92).
- **Tokens** (C-028): `work/build/tokens/tokens.json` and `tokens.css` from one source, `work/build/tokens/src/oa-tokens.src.mjs`, by `work/build/scripts/phase-2/tokens_build.mjs`; 485 tokens, version 6.0.0-gate2.1 (pre-release). One command runs every test: `python3 -I work/build/tests/tokens/run_token_tests.py` (parity, contrast and rules, 35 of 35 plants caught, Style Dictionary cross-check, rendered check). The main session ran it twice; all pass. Notes `work/handoffs/phase-2/20261106_Token-Build-Notes.md`; calls D2-134 to D2-161.
- **Reader check** (DR-84 to DR-87): published privately at https://claude.ai/artifact/16SD4uFJTiHKJC5p9CaFpP with the `db` capability (D2-247). Eight steps, about 9 to 10 minutes on a phone: three System 1 drawings (overview, R10, B4), eight Civic Line icons, nine marks at 16 px, charts S02, S11 and S14, three chapter 02 pairs, the masthead at both widths. Answer key `work/boards/phase-2/reader-check/20261106_Reader-Check-Answer-Key.json` (never in the page). Readers in Dustin's organization with interact access save automatically to `responses/<id>`; others finish in copy mode and send their text to Dustin. Notes `work/handoffs/phase-2/20261106_Reader-Check-Notes.md`; calls D2-221 to D2-246.
- **Stage A** (DR-88 to DR-91): brief `work/handoffs/phase-2/20261106_Stage-A-Brief.md`. Four makers built the guide shell and chapters 01 to 08 with the Gate 2 proofs panel: 99 rules and 234 specimens in `work/build/guide/` (chapters as JSON, specimens as HTML fragments with manifests), assembled by `python3 -I work/build/scripts/phase-2/guide_build.py` into `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`. The main session ran `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`: 4 widths, 0 failures, 17 listed exemptions (labeled failure cases and one true-size mark). Makers' notes: `20261106_Guide-Shell-Notes.md`, `20261106_Stage-A-Editor-Notes.md`, `20261106_Stage-A-Identity-Notes.md`, `20261106_Stage-A-Systems-Notes.md` (with `20261106_Stage-A-Systems-Measurements.json`), all in `work/handoffs/phase-2/`. Calls D2-162 to D2-220.
- **Stage A red team** launched under `work/handoffs/phase-2/20261106_Stage-A-Red-Team-Brief.md`: brand, evidence and nonpartisanship; accessibility; craft and typography; civic education and plain language; a simulated reader panel. Their reports land as `work/handoffs/phase-2/20261106_Stage-A-Red-Team-{Brand-Evidence,Accessibility,Craft,Civic-Plain}.md` and `20261106_Stage-A-Reader-Panel.md`. All five arrived before this chat closed:

| Lens | Score | Must fix | Should fix |
|---|---|---|---|
| Brand, evidence and nonpartisanship | 2 | 6 | 12 |
| Accessibility and interface | 4 | 2 | 15 |
| Craft and typography | 3 | 7 | 16 |
| Civic education and plain language | 3 | 9 | 19 |
| Reader panel (simulated, untested) | 3 | 5 | 10 |

Faults raised by more than one lens come first in the fix pass: decision codes and studio words printed for readers (H11; four lenses); "The hearing & the vote." shown as correct in 04 and as a failure in 02; party inks unequal in Rule 01.2 and sources described unequally in Rule 01.16; kickers that contradict Rule 01.21.

## 2. Next, in order

### A. Read the red team
All five reports are in `work/handoffs/phase-2/` (section 1). Read them in full before writing the fix pass brief. Two findings reach beyond the chapters: the display tracking tokens make letters touch in the locked tagline, chapter titles and rule titles (craft report), so the token engineer changes the source and reruns the token tests; and the copyable "For builders" CSS fails when pasted alone (reader panel), so the engineer fixes the blocks the shell prints. The craft report also holds that gate rule 4 needs the proofs side by side at actual size, which D2-170 had set aside for the 1200 px cards; resolve it, for example with a side-by-side frame that scrolls sideways, and log the call.

### B. One fix pass
Write `work/handoffs/phase-2/20261106_Stage-A-Fix-Pass-Brief.md` from the five reports: shared fixes first, then per-chapter items, each with its owner. Resume or re-brief the makers by ownership: editor (01, 02, and a copy edit of all eight chapters, starting from the ten cross-chapter issues in its notes), identity designer (03, 04, 08, proofs), systems designer (05, 06, 07), engineer (shell, checks). After the pass the main session rebuilds the page, reruns `guide_check.js` at four widths and the token tests, and logs every routine call.

### C. The creative director's scores and board A content
The creative director (`.claude/agents/oa-creative-director.md`) scores the fixed page on the Master Brief section 6 rubric and writes stage board A's content (verdict, scores, what still needs work, decisions for Dustin with recommendations, risks) as `*-Content.json`; the main session writes the `*-Studio-Record.json` (process, checks run, not tested, change log). A builder in the manner of `work/build/scripts/phase-2/voice_board5_build.py` merges them into `work/boards/20261106_Stage-A-Foundations-Board.html` (use the date the file is created), showing each chapter at true size with links into the live page, the proofs panel at actual size, and the decisions. Board check in `--board` mode; publish privately (icon "book"), record links in a `Published-Pages.json`, and publish the chapters page too.

### D. Decisions waiting for Dustin on board A
Collected from the makers' notes, each with its recommendation:
1. V5's "23 states" example becomes "In 23 states, citizens can petition a proposed law or constitutional amendment onto the statewide ballot." (Ballotpedia, read November 6, 2026) (D2-182).
2. Retire two more V5 supporting lines that DR-77 did not list (editor notes).
3. A "Guide" label for Connect pieces (editor notes).
4. Three lines the editor completed where the V5 text census was cut (editor notes).
5. Today's wordmark width and ampersand B as refined, from the proofs panel (DR-71, DR-89).
6. The new Signal Grid codes, Rules 08.4 to 08.8 (D2-189 on).
7. Social avatars and the app icon show B alone on Charcoal; L8 under the 14 px floor at feed size (identity notes).
8. The editorial crop of B always in the surface's ink, never red.
9. The six series-to-route pairs matched from clipped V5 text.
10. Rule 05.1: firm per-view color limits (Newsprint 60 to 85 percent, one dark panel per section, red within 5 percent), with V5's shares as the balance across a body of work.
11. The body-measure token renders 64 to 66 characters against its 68 promise: keep the value and correct the description.
12. Atlas System 1 moves from White to Newsprint in its finishing work (D2-160).
13. How the guide names H.R. 7008. The brand and evidence review found that "the stock trading ban" overstates a bill that bars buying stocks and also carries a voter photo ID requirement (`20261106_Stage-A-Red-Team-Brand-Evidence.md`). The same name sits on chart specimen S01 in the Explainer system and in the shared chart data, so the fix reaches chapter 14's specimens too; the studio should propose one neutral name (H12) for every place it appears.
Add whatever the red team and the creative director raise.

### E. Then
Stage board B (09 Pillar marks, 10 Topic and atlas symbols, 11 Status and utility icons, 12 Graphic devices), stage board C (17, 18, 19, 26), the shell's last pass with the pillar marks, the Gate 2 preview, Gate 2 (with the reader check's answers, read with `ArtifactData` `list` on `responses`), then Phase 3's chart kit on the new tokens.

## 3. Rules in force that the next session must not miss
- Everything in section 3 of the V3 handoff still holds (Rule 05.3 with its icon clause; party marks neutral and no red and blue on election graphics; the disclosure on election-rule charts; Newsprint ground; diverging pair B; the six chart rules of DR-64; chart titles that claim only what the evidence holds).
- Chapter 02's writing section binds every word (DR-73, DR-92). H11: no bare IDs or decision codes on a reader-facing page.
- Chapter pages use today's wordmark width; the condensed width appears only in the proofs panel until Gate 2 (DR-89).
- Products are named with no launch dates or status (DR-91).
- V7 is never edited; inconsistencies go to the V7.1 issue list.

## 4. Working notes for a fresh container
- **npm in `work/build`**: there is no `package.json`, so a lone `npm install --no-save X` removes packages installed earlier. Always install together: `cd work/build && npm install --no-save axe-core@4.10.2 style-dictionary@5.8.0`. Playwright and Chromium are preinstalled.
- **Checks**: tokens `python3 -I work/build/tests/tokens/run_token_tests.py`; guide `node work/build/scripts/phase-2/guide_check.js <page>` (guide pages; has its own 25-plant self-test, see the shell notes); charts and boards `node work/build/scripts/phase-2/dataviz_check.js <page> [--mid] [--board]`; chart data `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest <page>`.
- **Guide build**: `python3 -I work/build/scripts/phase-2/guide_build.py` (`--strict` fails on warnings; `--demo` fills empty chapters). Each maker's specimens also have their own build script in `work/build/scripts/phase-2/` (`guide_editor_build.py`, `stage_a_identity_*`, `stage_a_systems_*`), which writes nothing if its own checks fail.
- **Publishing**: read every file before publishing it (whole page, every image; a contact sheet rendered from a local HTML file works for images). A page with `capabilities` gets one functional pass with `ArtifactData`.
- **Agents**: run each studio role as a general-purpose agent told to read and adopt its file in `.claude/agents/`. Commit snapshots while agents write; the stop hook asks for it.
- **Context**: this chat ran one token build, one page build with its tests and publish, four makers and five reviewers. Plan to hand off after the fix pass and board A, or sooner.

## 5. Dustin's preferences
Ask the questions a good analyst would ask, post a short plan, and wait for his go before building. Make routine calls and log them. Show boards at each stage. Plain spoken prose, no em dashes, chapter 02's rules. End every reply with a change log. Never touch `source/` or anything he did not name. Work on branch `claude/friendly-brahmagupta-tonmfa`, commit and push as you go. Pace: as fast as quality allows (DR-72). Tell him when a chat should hand off.

## 6. Files to read first
1. `CLAUDE.md`, then the decision log from DR-73 on, the change ledger, the open questions.
2. This note.
3. `work/handoffs/phase-2/20261106_Stage-A-Brief.md` and the five red team reports.

## 7. Change log of this handoff
Created: this file. Modified: none. The chat's full change log is in section 1 and in the decision log.

## 8. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from DR-73 on), the change ledger and the open questions.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-2/20261106_Next-Session-Handoff_V4.md, which says where things stand and what is next, in order.

Settled and not to be changed: the Civic Line icons, the atlas visual system (System 1, DR-36), the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61), the chapter 14 coverage plan and Phase 3 build order (DR-62, DR-63), the chart rules of DR-64, and chapter 02's writing rules (DR-73 to DR-83).

Next: collect the stage A red team reports, run one fix pass with the makers, get the creative director's scores, and build and publish stage board A (chapters 01 to 08 and the Gate 2 proofs) with its decisions for me, as the handoff orders them.

The bar for everything: a finished product that looks like it was made by the best branding and design firm in the world. Use specialized agents, red team reviews and the creative director's scoring, as the handoffs describe.

How to work with me:
- Ask me the questions a good analyst would ask, post a short plan, and wait for my go before building anything new.
- Make routine calls yourself and log them.
- Show me boards to review at each stage.
- End every reply with a change log: files created, files modified, and where they live.
- Follow the writing rules in CLAUDE.md and chapter 02. No em dashes.
- Never touch source/ or anything I didn't name.
- Move as fast as quality allows, and tell me when this chat should hand off to a new one.
```
