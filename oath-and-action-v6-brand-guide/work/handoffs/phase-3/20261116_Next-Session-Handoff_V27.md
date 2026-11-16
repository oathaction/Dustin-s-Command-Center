# Handoff for the next session: Oath & Action Edition 06 (twenty-seventh handoff, November 16)

Written November 16, 2026, after the review of rounds 4 and 5 and its fix pass. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261114_Next-Session-Handoff_V26.md`. V5's sections 3 to 5, section 3 of V8 to V26, and section 3 below hold together. Decision log entries for this chat run from D3-2122 to D3-2265, with Dustin's answers DR-277 to DR-284. The change ledger runs to C-134.

## 1. Where things stand

Phase 3 is the active phase. The review of rounds 4 and 5 (row `c07`) is done: nine readers, one fix pass in two waves, the data lead's sign-off in eleven batches, a clean join build and the creative director's rescore. What remains before board 3 is the full four-width guide check (DR-284) and DR-191's second pass on any item the rescore left under 4 (D3-2265). The chapters page is version 12 (section 1, "Published").

**Dustin's answers this chat**
- DR-277: nine separate readers reading one shared capture set.
- DR-278: the four carried items that reach approved work (the masthead, the words inside image stages, the "Where to start" links, chapter 26's token table selector) measured, fixed here and shown on board 3.
- DR-279: Safari, Firefox and real screen readers stay "Not tested" until Phase 5.
- DR-280: the chapters page as version 12 after the fix pass.
- DR-281: this branch, `claude/friendly-brahmagupta-tonmfa`.
- DR-282: one register of every flagged fix not made, `work/ledger/20261116_Deferred-Fixes-Register.md`, for Dustin's final finishing pass; every chat adds its rows before it hands off.
- DR-283: the register backfilled from Phase 0 on.
- DR-284: the four-width guide check moves to chat 8's first step, before board 3 is built.

**The review** (brief `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md`; reports `work/handoffs/phase-3/20261116_Review-4-5-*.md` and `20261116_CD-Review-Of-Rounds-4-5.md`)

| Reader | Score | Must | Should |
|---|---|---|---|
| Statistics | 3.5 | 2 | 10 |
| Civic education | 3 | 4 | 23 |
| Accessibility | 4 | 1 | 7 |
| Nonpartisanship and brand | 3 | 3 | 7 |
| Craft at twice size | 3.5 | 2 | 22 |
| Production | 4 | 0 | 11 |
| Reader panel (simulated, DR-202) | 3 | 2 | 18 |
| Drift read | 3 | 3 | 13 |
| Creative director, first pass | 7 of 14 items at 4 or more | 3 | 12 |

**The fix pass** (brief `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md` with its calls 1 to 18; owners' notes `work/handoffs/phase-3/20261116_Fix-Pass-*-Notes.md`). The main calls: chapter 11's square keeps its one meaning, "Stopped", so Rule 15.22's stages print as bold numbers on the line (data lead's R1); Rule 13.5's effect pips on Rule 14.144's cards; Rule 15.20's sentence rewritten so Reform R-38 stays; an unappealed case under slashes; the chooser changed once on both Rules 15.20 and 14.144 (one width, a keyline in the red ring); S95 signs off with the 96 px lockmark (DR-211); S14 and S96 name the September 2026 payroll release; call 11 narrowed so a stage's words are hidden only where its alt carries every word (95 stages hidden, 321 left open and listed in `20261116_Fix-Pass-Engineer-Picture-Words.json`); the masthead's room set from its measured height (218 of 587 landings covered before, 0 after); new build guards for braces, page-wide selectors and a stale palette plate.

**The join** (commit `b86226e8`): strict build exit 0, 0 warnings, 12,174,060 bytes, 369 rules, 679 specimens; projection 15,144,130; chapters 11, 14 and 15 at 505,397, 2,114,782 and 569,930 bytes; chapter 14 with the kit 2,817,491, past its 2,803,941 figure and reported under DR-271; kit `build --all --no-png` 96 of 96; V7 check 0 failures; data check 126 tables, 0 faults; `phase3_ch14_build.py --check` 99 of 99; guide check self-test 150 of 150 plants; reader text scan clean. The quick guide check with photographs passes on the join build (D3-2266): 1440 and 390 px, 369 rules, 735 specimens, 3,764 same-page links, 152 key path walks and 834 steps, 0 failures; the selection guide's 127 form links and 6 road links land.

RESCORE_LINE

**The register.** 90 Open and 8 Unclear rows from the backfill of Phases 0 to 3 round 5, and 76 rows from this review (15 held for Dustin, 25 Open, 23 set aside, 2 declined, 11 not tested). Every one of the 143 codes in the nine reports has a recorded outcome.

**Published:** the chapters page as version 12, private, at https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF, from `work/boards/phase-3/review-4-5/20261116_Guide-Preview-V12.html` (the join build). Version id 1794858048-3280 (D3-2267).

## 2. Next, in order

### A. Confirm the committed state, then the four-width check (DR-284)
Set row `c08` active. V11's three setup steps and the three key tests. A strict build to scratch, matching section 1's figures (the date and time differ). Then the full guide check, `node work/build/scripts/phase-2/guide_check.js <page> ` without `--quick` (1440, 1024, 390 and 360 px), started with `run_in_background`, never with `&`, on a quiet machine; it takes about 60 to 75 minutes. A failure is fixed by its owner before board 3 is built, and the check rerun.

### B. DR-191's second pass (D3-2265)
For each item the rescore left under 4 (`work/handoffs/phase-3/20261116_Rounds-4-5-CD-Rescores.json` and the creative director's "Rescore" section), the owner it names makes the craft or wording fix; the data lead signs it off; the creative director rescores that item alone. An item that needs Dustin's call goes to board 3 flagged.

### C. Board 3, then Gate 3
Board 3 shows, as Gate 2's section 9 and V26 2C set it: round 4's 13 forms; the selection guide and palette specification; the three charts in full; chapter 15 whole; the two trackers with their twelve step names for Dustin's approval (as DR-108's were); the changed approved work listed in the change ledger's C-123 to C-134 ("listed for board 3": S14's source line and two label keys, the masthead and focus room, the "Where to start" links, the token table selector, chapter 18's form script and chooser part, the words inside image stages, the bill's step table, chapters 13 and 18's chips); the V7.1 rows proposed (`routes[].who`); and the register's rows held for Dustin (`work/ledger/20261116_Deferred-Fixes-Register.md`, "Held for Dustin (board 3)" in this review's section and Q-12). Then the Gate 3 report.

## 3. Working notes added this chat

- **The register is a standing duty (DR-282).** Every review, fix pass and board adds its rows before the handoff: each code not fully fixed, each accepted decline, each suggestion set aside, each item held for Dustin, with the file a fix goes into. Owners write "Not fixed" in that form; a clerk agent checks every code against every notes file at the close.
- **A clerk agent for the close.** One agent numbered 139 calls into the decision log, wrote twelve change ledger rows and filled the register from eleven notes files, which saved the main session's context. Give it the main session's own calls in a scratch list.
- **Captures of the 12 MB page are slow.** An element capture takes 1 to 36 seconds (most of it Playwright waiting on a plate in a new part of the page), so a full width set takes hours. Capture only what a reader needs, in priority order, and let readers take their own batches under the load rule.
- **Read `browsers.sh`'s words, not its exit status.** It always exits 0; three owners opened a browser on "WAIT" by testing the status. The helper sits in the scratch folder; a new chat writes its own.
- **`data_round0_build.py` has no argument parser.** Running it with `--help` rewrites the payroll sidecar; it now writes the research lead's release keys back byte for byte.
- **Hide words only where the alt says them all.** Wrapping an image stage's words from the accessibility tree reached 416 stages, and 321 alts lacked a word; hiding those would have taken words from screen reader users. A guide check now fails a hidden stage with an incomplete alt.
- **One writer per file, handed over in words.** The editor wrote second reads directly into finished owners' generators; each hand-over was a message naming the file, and the owner held until told. No collision this chat.
- **Rulings first and facts first** (the data lead's R1 to R7, the research lead's F1 to F13) let six owners start at once.
- **Load.** Up to 14 agents ran at once; the load stayed under 6. Five slips are logged.
- **Context.** This chat ran 25 agents and about 90 resumed runs. Hand off after the second pass and the four-width check if board 3 cannot fit.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

The review of rounds 4 and 5 is done, with its fix pass and the creative director's rescore (DR-277 to DR-284). First, run the full four-width guide check on the fixed page (DR-284), then DR-191's second pass on any item the rescore left under 4, then build board 3 and write the Gate 3 report, as handoff V27 section 2 sets it.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from D3-2122 to the end, with DR-277 to DR-284), the change ledger (to C-134), the open questions, and the Gate 2 report (work/ledger/20261111_Gate-2-Report.md), section 9.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261116_Next-Session-Handoff_V27.md, then section 3 of V5 to V26's handoffs, the review and fix briefs of this round (work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md and 20261116_Rounds-4-5-Fix-Brief.md), the creative director's rescore (20261116_Rounds-4-5-CD-Rescores.json), the board 2 brief and decisions (work/handoffs/phase-3/20261113_Board-2-Brief.md, 20261113_Board-2-Decisions.json) as the model for board 3, and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md).

Data keys are saved on this environment: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64, with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); and every answer I have given from DR-95 on, including DR-225 to DR-284. Size allocations move as content needs; only the page's 16 MB is fixed (DR-271).

Every fix flagged and not made goes into the deferred fixes register before you hand off (DR-282). I will run a final finishing pass from it when the guide is complete.

Phase 3 runs as the proposal sets it: the four-width check and second pass, then board 3, then Gate 3. The guide stays one file.

The bar for everything: a finished product that looks like it was made by the best branding and design firm in the world. Use specialized agents, red team reviews and the creative director's scoring, as the handoffs describe.

How to work with me:
- Ask me the questions a good analyst would ask, post a short plan, and wait for my go before building anything new.
- Make routine calls yourself and log them.
- Show me boards to review at each stage.
- End every reply with a change log: files created, files modified, and where they live.
- Follow the writing rules in CLAUDE.md and chapter 02. No em dashes.
- Never touch source/ or anything I didn't name.
- Move as fast as quality allows, keep agent runs lean since I am on paid credits, and tell me when this chat should hand off to a new one.
```

## 5. Change log of this chat

Created, all under `work/` unless named:
- **Briefs and handoff:** `handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md`, `20261116_Rounds-4-5-Fix-Brief.md` (with Addendum 1), `20261116_Deferred-Fixes-Backfill-Brief.md`, this handoff.
- **Reports:** `handoffs/phase-3/20261116_Review-4-5-Red-Team-Statistics.md`, `-Civic-Education.md`, `-Accessibility.md`, `-Nonpartisan-Brand.md`, `-Craft.md`, `-Production.md`, `20261116_Review-4-5-Reader-Panel-Simulated.md`, `20261116_Review-4-5-Drift-Read.md`, `20261116_CD-Review-Of-Rounds-4-5.md`, `20261116_Rounds-4-5-CD-Scores.json`, `20261116_Rounds-4-5-CD-Rescores.json`; the production test folder `handoffs/phase-3/review-4-5-production-test/`.
- **Fix notes:** `handoffs/phase-3/20261116_Fix-Pass-Data-Lead-Notes.md`, `-Research-Notes.md`, `-Editor-Notes.md`, `-Systems-Designer-Notes.md`, `-Complex-Examples-Notes.md`, `-Tracker-Designer-Notes.md`, `-Engineer-Notes.md`, `-Engineer-2-Notes.md`, `-Component-Engineer-Notes.md`, `-Round-4-Maker-Notes.md`, `-Selection-Guide-Notes.md`, `20261116_Fix-Pass-Engineer-Picture-Words.json`.
- **Register:** `ledger/20261116_Deferred-Fixes-Register.md`; the four backfill parts in `handoffs/phase-3/deferred-fixes-backfill/`.
- **Guide preview:** `boards/phase-3/review-4-5/20261116_Guide-Preview-V12.html`.

Modified:
- `ledger/20261020_Decision-Log.md` (D3-2122 to D3-2265, DR-277 to DR-284); `ledger/20261020_Change-Ledger.md` (C-123 to C-134); `ledger/20261020_Open-Questions.md` (Q-18 moved to Answered).
- Generators and their outputs, each by its owner: chapter 11 (`apply_systems_ch11.py`, `11-icons.json`, `s-11-*`); chapter 14 (`phase3_ch14_complex_build.py`, `phase3_ch14_rules_build.py`, `selection_guide_build.py`, `palette_spec_build.py`, `phase3_ch14_build.py`, `maker_c_round5_derive.py`, the round 4 derive scripts, specs `s14.json`, `s85.json` to `s96.json`, entries `14-001.json` to `14-014.json`, `14-079.json` to `14-084.json`, `14-135.json` to `14-144.json`, the chapter file, log and manifest); chapter 15 (`phase3_ch15_build.py`, `15-systems-graphics.json`, `s-15-*`, its manifest); the kit (`kit.js`, `kit.css`, `checks.js`, `columns-moving-average.js`, the calendar and social card forms, the README); `guide_build.py`, `guide_check.js`; the shell (`guide-shell.css`, `guide-shell.js`), chapter 18's `c-18-choice.css` and `c-18-form` script; `token_table_build.py` and chapter 26's token table; `data_round0_build.py`; the payroll and round 4 sidecars; the workflow sources file and the research ledger.

Published: the chapters page, version 12 (private). Work tracker: row `c07` done, `c08` noted. Not touched: `source/`, `deliverables/`, Atlas V7.
