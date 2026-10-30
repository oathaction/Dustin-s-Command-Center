# Atlas concepts, stage 1: the frame and the ideas

Oath & Action Brand Guide, Edition 06. Phase 2, October 30, 2026. Status: waiting for Dustin's three answers. This is a stage review inside Phase 2, not a gate.

Open the board: `work/boards/20261030_Atlas-Concepts-Ideas-Board.html`, also published as a private page at https://claude.ai/artifact/AKEXDb3pA2QKQtbNuU8gHn.

## What you are asked to decide

1. **The six concepts from scratch.** Recommended: the ideation agent's six with Editorial Desk in place of Honeycomb.
2. **The shared frame, as a set.** Recommended: approve.
3. **When the data visualization system starts.** Recommended: right after you pick an atlas direction.

## 1. What was done

| Step | Who ran it | Output |
|---|---|---|
| References saved and logged; decisions DR-12 to DR-22 and D2-47 to D2-62 | Main session | `work/research/chat-references/atlas-concepts/`, `data-viz/`; decision log; rights ledger |
| Concepts brief, variable-to-icon map, shared check and verify scripts | Main session | `work/handoffs/phase-2/20261030_Atlas-Concepts-Brief.md`; `work/build/scripts/phase-2/atlas_concepts_*.{py,js}` |
| Reader, levels and wording rules | Civic education expert (fresh agent with a written brief) | `work/handoffs/phase-2/20261030_Atlas-Civic-Education-Memo.md` |
| Loops as routes, data contract per level, overview options | Data visualization lead | `work/handoffs/phase-2/20261030_Atlas-Dataviz-Memo.md`; loop-route study and geometry in `work/boards/phase-2/atlas-concepts/shared/` |
| Navigation model and shared kit | UX and accessibility lead | `work/handoffs/phase-2/20261030_Atlas-Interaction-Memo.md`; `shared/atlas-kit.js`, `atlas-kit.css`, kit demo |
| Type, line and ground rules | Design director | `work/handoffs/phase-2/20261030_Atlas-Design-Frame-Memo.md`; type and line specimen |
| Ten directions from scratch | A fresh agent that read no earlier board, review or reference (D2-54) | `work/handoffs/phase-2/20261030_Atlas-From-Scratch-Directions.md`; sketches in `work/boards/phase-2/atlas-concepts/ideas/` |
| Data visualization research (DR-22) | Research lead | `work/research/20261030_Data-Viz-System-References.md`; captures in `work/research/data-viz-references/` |
| Recommendation on concept 12, Board 1 and this report | Main session. No creative director reviewed the ten directions before the board | This file; the board |

## 2. Verification

**Tested**
- Shared verifier: caught 6 of 6 planted errors on a test page. Shared rendered check: caught a planted unmarked red and a contrast failure.
- Loop-route study: no pair of thumbnails reaches the 0.60 similarity limit at 256, 310 or 318 px; the closest is R1 and R6 at 0.57.
- Interaction kit: 76 scripted checks pass; axe-core 4.10.2 finds 0 violations in nine states.
- Type and line specimen: no sideways scroll, no text under 13 px, 0 axe-core violations at 1440 and 390 px.
- Board 1: the shared check passes at 1440 and 390 px (no sideways scroll, no text under 13 px, no contrast failures, 0 axe-core violations, focus rings on every stop).
- Two numbers spot-checked against the model by the main session: 22 of 23 loops carry a reform (B5 does not); the glossary line "Improvement or decline can reinforce itself."

**Not tested**
- Readers. No person has seen any sketch, thumbnail or study.
- Screen readers, Firefox, Safari and real phones.
- Any nytimes.com page, by rule (D2-62).
- The raw Atlas V7 file, which is not in this container (DR-20).

## 3. Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, the Civic Line icons or the identity masters changed.

**Created**
- `work/ledger/20261030_Atlas-Concepts-Stage-1-Report.md`
- `work/boards/20261030_Atlas-Concepts-Ideas-Board.html`; `work/boards/phase-2/atlas-concepts/board-1/` (captures, check results)
- `work/handoffs/phase-2/`: the brief, four memos and the ten directions
- `work/boards/phase-2/atlas-concepts/shared/` and `ideas/`
- `work/research/20261030_Data-Viz-System-References.md`, `work/research/data-viz-references/`
- `work/research/chat-references/atlas-concepts/`, `work/research/chat-references/data-viz/`
- `work/build/scripts/phase-2/`: `atlas_concepts_common.py`, `atlas_concepts_check.js`, `atlas_concepts_verify.py`, `atlas_loop_routes.py`, `atlas_kit_demo_build.py`, `atlas_kit_demo_test.js`, `atlas_board1_capture.js`, `atlas_board1_build.py`

**Modified**
- `work/ledger/20261020_Decision-Log.md`: DR-12 to DR-22, D2-47 to D2-62
- `work/research/20261020_Rights-Ledger.md`: October 30 references and research sources
