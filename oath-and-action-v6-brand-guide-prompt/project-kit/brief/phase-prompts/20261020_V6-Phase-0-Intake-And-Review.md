# Phase 0: Intake and review

Paste everything below the line into Claude Code, started in the project folder.

---

You are the studio lead for the Oath & Action Brand Guide, Edition 06. Read `CLAUDE.md`, then read `brief/20261020_Oath-And-Action-V6-Master-Brief_V1.md` in full. This is Phase 0. It ends at Gate 0, and you stop there.

**Outcome.** A concise review of the current guide and a work plan for Phases 1 to 5, ready for my approval:
- `work/ledger/YYYYMMDD_Gate-0-Report.md`
- `work/boards/YYYYMMDD_Gate-0-Review-Board.html` (execution date), a single page I can open to see the screenshots, findings and plan
- `work/ledger/` started: `YYYYMMDD_Change-Ledger.md`, `YYYYMMDD_Decision-Log.md`, `YYYYMMDD_Open-Questions.md`
- `work/research/YYYYMMDD_Rights-Ledger.md` started with every supplied reference, font and image

**Inputs.** Everything in `source/`, listed in Master Brief section 2. Confirm each file is present and record its size and checksum. If a file is missing, list it in the gate report and continue with what is present.

**Skip.** No design changes, no new artwork, no V6 build, no outside research beyond what is needed to identify a reference. Do not edit anything in `source/`.

**Verify.** Show me, in the gate report:
- extraction counts that match the sources: V5 Polished chapters (16 plus a closing), sprite symbols, embedded fonts, scripts and downloads; Atlas V7 `meta.counts` against counts computed from its JSON
- a screenshot of every V5 Polished chapter at 1440 px and 390 px, and every report reader page
- the Atlas reconciliation table
- the rubric scores for the current guide

## Steps

1. Set up the folder layout from `CLAUDE.md`. Record a source manifest.
2. `oa-engineer`: write extraction scripts. Split V5 Polished into CSS, scripts, the SVG sprite (one file per symbol, with its ID), fonts, images and one file per chapter. Do the same at a lighter level for the Atlas Visual System, Concepts V2 and V4.2. Extract the Atlas V7 JSON to `work/extract/atlas-v7-data.json`. Unpack the two zips into `work/extract/references/`. Never read a large file whole.
3. `oa-engineer`: render V5 Polished with Playwright at 1440 and 390 px, every chapter and every report page. Make contact sheets for review.
4. Run these audits in parallel, each writing to `work/handoffs/phase-0/`:
   - `oa-creative-director`: brand strategy and art direction audit. What is strong and should be protected, and where the guide falls short of a leading studio's work. Score each chapter on the rubric.
   - `oa-design-director`: identity geometry and symbol audit from the extracted vectors. Optical spacing, small sizes, icon consistency and similarity, graphic devices, layout and typography. Review the eight icon studies and the reference folders for principles, with notes on what to take and what to avoid.
   - `oa-ux-accessibility-lead`: navigation, structure, interaction, states and an initial accessibility scan.
   - `oa-dataviz-systems-lead`: the Data Visualization and Atlas System chapters, the Atlas Visual System and Concepts V2 against Atlas V7. Produce the reconciliation table in Master Brief section 14. Confirm or correct the V7 values quoted in the brief.
   - `oa-editor`: voice, locked lines, terminology, illustrative labels, and every contradiction between a rule and its demonstration.
   - `oa-research-lead`: rights inventory of every reference image, font and embedded image. Identify stock previews, third-party screenshots and generated studies.
5. Check each of the fifteen tensions in Master Brief section 8 against the extracted files. Confirm it, correct it, or add tensions the audits found.
6. Write the review and the plan:
   - Review: one page. What to protect, what to fix, and the biggest opportunities, with evidence from the screenshots.
   - Plan: Phases 1 to 5 with the work, the agents, the order, the risks, and what I will see at each gate.
   - Phase 1 proposal: exactly what Phase 1 will produce, and the decisions I will be asked to make at Gate 1.
   - Open questions, ranked.
7. Write the gate report and the review board. Stop. Wait for my reply.

Finish with a change log: files created, files modified and their locations.
