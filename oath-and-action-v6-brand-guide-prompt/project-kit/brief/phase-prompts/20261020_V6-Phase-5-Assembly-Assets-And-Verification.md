# Phase 5: Assembly, asset package and verification

Paste everything below the line into Claude Code after I approve Gate 4. Record my Gate 4 decisions under "Gate 4 decisions."

---

This is Phase 5 of the Oath & Action Edition 06 commission. Follow `CLAUDE.md`. Read the ledgers and `work/ledger/YYYYMMDD_Gate-4-Report.md`, then Master Brief sections 20 to 24. Work only within the approved Phase 5 proposal.

Gate 4 decisions: [paste or write "As proposed"]

**Outcome.** The three final deliverables in `deliverables/`, named with the execution date:
1. `YYYYMMDD_Oath-And-Action-Brand-Guide_V6.html`, one self-contained file under 16 MB
2. `oath-and-action-v6-asset-package/`, structured as in Master Brief section 20, with the asset index and the AI builder implementation brief
3. `YYYYMMDD_Oath-And-Action-V6-Change-And-Validation-Report.md`

**Inputs.** Everything in `work/build/`, the ledgers, and the gate reports.

**Skip.** No new design work beyond fixes found in verification. A PDF only if I ask for one.

**Verify.** Run the full matrix in Master Brief section 22 on the final file and package. Show the results in the report, with completed checks and checks the environment could not run as separate lists.

## Steps

1. `oa-engineer`: assemble the single-file guide with embedded fonts, vectors, styles and scripts. Generate the asset package from the same sources. Wire every download to a dated, descriptive filename.
2. `oa-engineer`: run the full verification matrix. Click every download and open every file. Check SVG validity, `<use>` resolution and PNG dimensions by script. Run the token parity test.
3. `oa-ux-accessibility-lead`: final accessibility review on the assembled file, including the manual checks of reading order, focus, keyboard use, reduced motion and diagram alternatives.
4. `oa-editor`: final read of the whole guide, the asset index and the AI builder brief. Confirm the locked lines are exact.
5. `oa-research-lead`: confirm the research and rights ledgers are complete and that nothing shipped lacks a right to ship.
6. `oa-design-director` and `oa-creative-director`: final review of the assembled guide at 1440 and 390 px, chapter by chapter, against the rubric and the definition of done in Master Brief section 24.
7. Fix what the reviews find, then re-run the affected checks.
8. Write the change and validation report:
   - Resolved conflicts and tensions, with locations
   - Identity refinements, with before and after
   - New assets, by class
   - Test results, run and not run
   - Remaining factual, model and rights questions for me
9. Write `work/ledger/YYYYMMDD_Gate-5-Report.md` with the definition-of-done checklist marked. Stop. Wait for my acceptance.

Finish with a change log: files created, files modified and their locations.
