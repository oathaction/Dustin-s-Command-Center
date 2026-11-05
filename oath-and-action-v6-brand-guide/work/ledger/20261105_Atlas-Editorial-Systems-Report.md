# Atlas editorial systems: Board 2 report

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Status: waiting for Dustin's pick. This is a stage review inside Phase 2, not a gate.

Open the board: `work/boards/20261105_Atlas-Editorial-Systems-Board.html`, also published as a private page at https://claude.ai/artifact/WFwciVo4NvugGRfFENninP. The five systems are published as private pages, listed in `work/boards/phase-2/atlas-editorial/board-2/20261105_Published-Pages.json`.

## What you are asked to decide

1. **Which system to finalize.** Recommended: Times Explainer, finished with the layer rule and ground of your Concepts 07 and 09, Night Edition as its dark mode, and Reference Sheets' best parts borrowed in.
2. **The sign mark** (Choice 3): the pointing tag, as recommended on October 28.
3. **"Democratic quality"** prints as "Quality of democracy" on pages, with the code DQ kept in the data.
4. **L23's name** goes to the V7.1 issue list so it reads with its minus sign.
5. **"Household" in two names**: keep both for now.
6. **Your dark atlas's "one documented connection at a time"** becomes "one graded connection at a time" in your copy.
7. **Order of work after the pick**: the finishing pass, then the data visualization system (DR-25), then the open direction review items and Gate 2.

## 1. What was done

| Step | Who ran it | Output |
|---|---|---|
| Your references and answers logged; the editorial brief; the shared dataset joining V7 with the dark atlas's plain layer | Main session | `work/handoffs/phase-2/20261105_Atlas-Editorial-Brief.md`; `work/boards/phase-2/atlas-editorial/shared/` |
| Five systems, six views each | Five specialist makers in parallel | `work/boards/phase-2/atlas-editorial/01` to `05`; notes `work/handoffs/phase-2/20261105_Editorial-0N-Notes.md` |
| Red team | A civic educator, an interface and accessibility lead, an evidence and brand auditor, and a simulated first-time reader panel | `work/handoffs/phase-2/20261105_Red-Team-*.md`, `20261105_Reader-Panel.md` |
| Fix pass against thirteen shared fixes and each system's findings | The five makers | Fix-pass sections in each notes file; `20261105_Editorial-Fix-Pass-Brief.md` |
| Scores, recommendation and six last faults | Creative director | `work/handoffs/phase-2/20261105_CD-Review-Of-Editorial-Systems.md` |
| Last faults fixed; a source correction on one figure | The makers; the main session found the figure | Notes; D2-85, D2-86 |
| Checks re-run after every pass, publishing, Board 2 and this report | Main session | This file; the board |

## 2. Scores

The creative director's scores after the fix pass, 1 to 5, ship threshold 4 on every line.

| System | Craft | Clarity | Brand | Usefulness | Evidence | Accessibility | Beauty | Ships |
|---|---|---|---|---|---|---|---|---|
| 1 Times Explainer | 4 | 5 | 4 | 5 | 4 | 4 | 4 | Yes |
| 2 Economist Register | 4 | 4 | 3 | 5 | 4 | 4 | 4 | Not at review (brand); the fault was fixed after |
| 3 Reference Sheets | 5 | 4 | 4 | 5 | 4 | 4 | 4 | Yes |
| 4 Night Edition | 4 | 4 | 4 | 5 | 3 | 4 | 5 | Not at review (evidence); the fault was fixed after |
| 5 Architecture | 3 | 3 | 4 | 5 | 4 | 4 | 4 | No (craft, clarity) |

The scores were given before the last fixes and were not re-scored after them.

## 3. Verification

**Tested**
- Every page passes the data verifier against V7 (tagged names, signs, grades, delays, loop chains, issues, parts, counts), and its self-test caught all six planted errors on each page.
- Every page passes the rendered check on all six views at 1440, 390 and 360 px: no sideways scroll, no text under 13 px, text contrast, labels inside drawings and apart, the red rule, 0 axe-core violations, a visible focus ring on every stop, and the click from the overview into a close-up and back.
- The evidence auditor checked about 3,300 tagged facts and 25 or more untagged statements per system before the fix pass; the main session checked the 7.65 percent figure against claim CL1467.
- Board 2 passes the rendered check at 1440, 390 and 360 px.

**Not tested**
- Real readers; the reader panel was simulated by one model.
- Screen readers, Safari, Firefox, real phones, 200 percent text zoom and print.
- The creative director did not re-score after the last fixes.

## 4. Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, the Civic Line icons or the identity masters changed.

**Created**
- `work/handoffs/phase-2/`: the editorial brief, the fix-pass brief, five makers' notes, four red team reports, the creative director's review
- `work/boards/phase-2/atlas-editorial/`: the shared dataset, five systems with pages, build scripts, captures and check results, Board 2's content and page links
- `work/boards/20261105_Atlas-Editorial-Systems-Board.html`
- `work/build/scripts/phase-2/atlas_editorial_data.py`, `to_artifact_page.py`, `atlas_board2_build.py`
- `work/research/chat-references/atlas-editorial/`, `work/research/atlas-v7-docs/`
- `work/ledger/20261105_Atlas-Editorial-Systems-Report.md`

**Modified**
- `work/build/scripts/phase-2/atlas_concepts_verify.py` and `atlas_concepts_check.js`
- `work/ledger/20261020_Decision-Log.md` (DR-28 to DR-35, D2-68 to D2-87), `work/ledger/20261020_Source-Manifest.md`, `work/research/20261020_Rights-Ledger.md`
