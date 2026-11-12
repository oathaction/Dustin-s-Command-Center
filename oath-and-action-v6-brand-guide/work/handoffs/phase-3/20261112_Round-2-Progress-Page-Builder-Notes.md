# Round 2 progress page builder notes

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. The page builder works as the design director building a review page (`.claude/agents/oa-design-director.md`), under `work/handoffs/phase-3/20261112_Round-2-Progress-Page-Brief.md` (DR-241, DR-246). Paths are relative to `oath-and-action-v6-brand-guide/`.

## Status

- **Scripts and content written; first run in progress.** `work/build/scripts/phase-3/progress_round_2_build.py` and `progress_round_2_render.js` (copied from round 1's and adapted; round 1's files untouched), and `work/boards/phase-3/round-2/progress/20261112_Round-2-Progress-Content.json`.
- Next: run once on the current files without `--reuse`, with `--check`; report to the main session; then wait for its word that the rescore has landed and rerun with `--reuse --check`.

## How to rerun

```
python3 -I work/build/scripts/phase-3/progress_round_2_build.py --reuse --check
```
