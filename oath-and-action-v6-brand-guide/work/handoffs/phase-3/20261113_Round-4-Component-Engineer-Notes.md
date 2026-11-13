# Round 4 component engineer notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the component engineer, a second `oa-engineer` instance under the main session's split of 20:58 UTC (handoff V14: the guide's code sets and shell apart from the chart kit), for `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, contracts R4-5 to R4-7, DR-265 and DR-267. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/component-engineer/` (`scratch/` below).

## Status

- 20:58 UTC: started (clock read 20:58:05).
- 21:04 UTC: the main session gave me every loop word in chapter 18 for DR-267: the code sets, the two KEYS strings in `stage_c_ch18_build.py` (lines 1954, 1970), its lines 1352 and 1631, and `stage_c_ch18_anatomy_build.py` lines 1127 and 1129, as string changes only, with their outputs. **Neither generator is rerun to write until the main session rules on the staleness below.**
- In progress: the five tasks under "Contracts".

## Summary

To come.

## Staleness of chapter 18's generators on HEAD (for the main session's ruling)

Both generators run in a scratch copy of HEAD `17456b9f` (`git archive` of `work/build/scripts`, `work/build/guide` and `work/build/tokens`, with `work/build/assets` and `work/extract` linked read-only), written there and compared with the committed files (21:09 UTC):

- `stage_c_ch18_build.py --check`: "chapter 18: stale work/build/guide/chapters/18-components.json", exit 1. Written in the copy, it changes **one line** of `18-components.json` and nothing else (its 24 failure plates, `manifest-components.json` and its 24 keys files equal the committed ones byte for byte):
  - line 1113, Rule 18.14's rule text: committed "“Download tokens.css, CSS, 95 KB”", the generator would write "“Download tokens.css, CSS, 105 KB”". The generator reads the size from `work/build/tokens/tokens.css` (`TOKENS_KB`, its line 112), which now weighs 105,067 bytes. No other word would change.
- `stage_c_ch18_anatomy_build.py`: written in the copy, its 25 plates and `manifest-anatomy.json` equal the committed ones byte for byte (current).

## Contracts

## Routine calls

## Changed outside chapters 13 to 15

## Requests

## Tested

## Not tested
