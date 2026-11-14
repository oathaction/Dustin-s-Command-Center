# Round 5 notes: tracker designer, R5-8's number map and Rules 11.10 and 11.11

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Written by the tracker designer (a general-purpose agent briefed as the designer who drew chapter 11's trackers and chapters 11, 12 and 15's systems plates) for `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`, under R5-7, R5-8, DR-274 and DR-275. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Status

01:49 UTC. **R5-8 applied in every file I own, and proved.** The list and map are under "Contracts", posted 01:45 and relayed by the main session. Token source: my three string edits in `work/build/tokens/src/oa-tokens.src.mjs` landed at **01:46 UTC** (lines 139, 398 and 599); the engineer owns the rebuild of `tokens.json`, the token tests and chapter 26's token table (main session, 01:52). Every generator I own reran: each output equals the committed file with the map applied and nothing else, the full chain's second run changed no file (hashes), and no `11.10` or `11.11` is left anywhere in `work/build/`. Next: the two trackers, Rules 11.10 and 11.11, once the research lead's "Facts for owners" item 1 and the editor's words land. For the systems designer: the trackers are not built yet; this line will say when they land.

## Summary

R5-8 first: every match of `11.10` to `11.16` followed by a non-digit across `work/build/`, read by script and in context, then the map applied in one pass. Then the ballot measure and court case trackers as Rules 11.10 and 11.11 in group 2.

## Contracts

### R5-8, the chapter 11 number map (DR-274)

| Old | New | Rule |
|---|---|---|
| (new) | 11.10 | The ballot measure tracker |
| (new) | 11.11 | The court case tracker |
| 11.10 | 11.12 | Say a wait or a later step in words, and keep the count at six. (stays in group 2) |
| 11.11 | 11.13 | Set each utility icon beside its word. (opens group 3) |
| 11.12 | 11.14 | Give each drawing one meaning. |
| 11.13 | 11.15 | Mark a link to another site, and open it in the same tab. |
| 11.14 | 11.16 | Keep topic and atlas symbols out of buttons. |
| 11.15 | 11.17 | Give each error, success and warning its mark and its words. (opens group 4) |
| 11.16 | 11.18 | Give an error the red when it meets the other red jobs. |

Rules 11.1 to 11.9 keep their numbers. Groups keep their numbers: group 2 now runs 11.8 to 11.12, group 3 opens at 11.13 and group 4 at 11.17.

**How to apply it.** Map all seven old numbers in one pass with a function, never one replace after another (a chain would carry 11.12 to 11.14 and then to 11.16). The pattern is `(?<![\d.])11\.1[0-6](?!\d)`, with the anchors `#rule-11-10` to `#rule-11-16` mapped the same way. Read each line first: the scan below already set aside every size and data value. Then rerun the generator and prove it with a second run and an empty `git diff`.

```python
MAP = {'11.10': '11.12', '11.11': '11.13', '11.12': '11.14', '11.13': '11.15', '11.14': '11.16', '11.15': '11.17', '11.16': '11.18'}
re.sub(r'(?<![\d.])11\.1[0-6](?!\d)', lambda m: MAP[m.group()], text)
```

**Specimen IDs follow their rules.** Chapter 11's specimens `s-11-10-correct` to `s-11-16-failure` become `s-11-12-*` to `s-11-18-*`, and the new trackers take `s-11-10-*` and `s-11-11-*`. Nothing outside my two generators and their outputs names them (scanned: the scripts, the checks, the code sets, the keys files and the manifests; the two board builders excepted).

### The scan

Script: `r58_scan.py` in my scratch folder (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/tracker-designer/`), over every text file in `work/build/` but `node_modules`, `__pycache__` and the two board builders (D3-1878), at 01:44 UTC on HEAD `2bcc0232`. 281 matches in 57 files.

**Not rules, left as they are (78 matches in 27 files), each read in context:** coordinates in the Civic Line drawings and their records (`work/build/assets/civic-line/` 26, `civic-line-24-fit/qa/` 10), path data in the identity re-exports and the three chapter 03 specimens that inline them (`assets/identity/reexport/` 12, `s-03-4-correct`, `s-03-l6`, `s-03-lockups` 25), and Missouri's 2022 minimum wage of $11.15 in the two Labor Department tables (`work/build/data/` 6).

**Rules (203 matches in 30 files), by owner.** Each cell gives the count, then each line with its old and new numbers.

| File | Owner | What it is | Lines |
|---|---|---|---|
| `work/build/scripts/phase-2/apply_systems_ch11.py` | Tracker designer | generator | 16: 294: 11.16 to 11.18; 309: 11.16 to 11.18; 469: 11.10 to 11.12; 1147: 11.10 to 11.12; 1159: 11.10 to 11.12; 1411: 11.16 to 11.18; 1608: 11.10 to 11.12; 1615: 11.15 to 11.17; 1628: 11.10 to 11.12; 1650: 11.11 to 11.13, 11.12 to 11.14, 11.13 to 11.15, 11.14 to 11.16; 1651: 11.15 to 11.17, 11.16 to 11.18; 1713: 11.10 to 11.12 |
| `work/build/scripts/phase-2/apply_systems_ch11_ui.py` | Tracker designer | generator | 41: 2: 11.11 to 11.13, 11.16 to 11.18; 104: 11.11 to 11.13; 190: 11.11 to 11.13; 221: 11.11 to 11.13; 249: 11.12 to 11.14; 364: 11.12 to 11.14; 370: 11.12 to 11.14; 389: 11.12 to 11.14; 452: 11.13 to 11.15; 480: 11.13 to 11.15; 498: 11.13 to 11.15; 503: 11.14 to 11.16; 620: 11.14 to 11.16; 643: 11.14 to 11.16; 649: 11.15 to 11.17; 651: 11.15 to 11.17; 722: 11.15 to 11.17; 745: 11.15 to 11.17; 774: 11.16 to 11.18; 847: 11.16 to 11.18; 863: 11.16 to 11.18; 869: 11.11 to 11.13, 11.16 to 11.18; 898: 11.11 to 11.13; 922: 11.11 to 11.13; 947: 11.12 to 11.14; 964: 11.12 to 11.14; 993: 11.13 to 11.15; 1007: 11.13 to 11.15; 1023: 11.14 to 11.16; 1038: 11.14 to 11.16; 1059: 11.15 to 11.17; 1080: 11.15 to 11.17; 1110: 11.16 to 11.18; 1130: 11.16 to 11.18; 1152: 11.11 to 11.13; 1154: 11.12 to 11.14; 1157: 11.15 to 11.17; 1161: 11.11 to 11.13; 1163: 11.15 to 11.17 |
| `work/build/guide/chapters/11-icons.json` | Tracker designer | output of apply_systems_ch11.py | 22: 26: 11.11 to 11.13; 32: 11.15 to 11.17; 287: 11.16 to 11.18; 580: 11.10 to 11.12; 584: 11.15 to 11.17; 601: 11.10 to 11.12; 635: 11.11 to 11.13; 659: 11.11 to 11.13; 705: 11.12 to 11.14; 726: 11.12 to 11.14; 768: 11.13 to 11.15; 789: 11.13 to 11.15; 819: 11.14 to 11.16; 836: 11.14 to 11.16; 869: 11.15 to 11.17; 893: 11.15 to 11.17; 945: 11.16 to 11.18; 968: 11.16 to 11.18; 1030: 11.11 to 11.13; 1036: 11.12 to 11.14; 1042: 11.15 to 11.17; 1081: 11.10 to 11.12 |
| `work/build/guide/specimens/s-11-menu.html` | Tracker designer | output of apply_systems_ch11.py (s_menu) | 7: 1: 11.10 to 11.12, 11.11 to 11.13, 11.12 to 11.14, 11.13 to 11.15, 11.14 to 11.16, 11.15 to 11.17, 11.16 to 11.18 |
| `work/build/scripts/phase-2/stage_a_systems_ch05.py` | Tracker designer | generator (stage_a_systems_build.py probe, capture, final) | 3: 118: 11.15 to 11.17; 492: 11.15 to 11.17; 1127: 11.15 to 11.17 |
| `work/build/guide/chapters/05-color.json` | Tracker designer | output of stage_a_systems_ch05.py | 1: 224: 11.15 to 11.17 |
| `work/build/scripts/phase-2/stage_b_ch12_systems_build.py` | Tracker designer | generator | 5: 102: 11.16 to 11.18; 162: 11.16 to 11.18; 321: 11.16 to 11.18; 477: 11.16 to 11.18; 500: 11.16 to 11.18 |
| `work/build/guide/chapters/12-graphic-devices.json` | Tracker designer | output of stage_b_ch12_systems_build.py | 2: 239: 11.16 to 11.18; 277: 11.16 to 11.18 |
| `work/build/scripts/phase-2/stage_c_ch17_build.py` | Tracker designer | generator | 5: 533: 11.14 to 11.16; 1624: 11.14 to 11.16; 1807: 11.15 to 11.17; 1829: 11.15 to 11.17; 2040: 11.15 to 11.17 |
| `work/build/guide/chapters/17-motion-and-states.json` | Tracker designer | output of stage_c_ch17_build.py | 4: 179: 11.14 to 11.16; 437: 11.15 to 11.17; 479: 11.15 to 11.17; 793: 11.15 to 11.17 |
| `work/build/scripts/phase-2/stage_c_identity_ch17.py` | Tracker designer | generator (a code comment only) | 1: 377: 11.14 to 11.16 |
| `work/build/scripts/phase-2/stage_c_ch19_build.py` | Tracker designer | generator | 10: 212: 11.11 to 11.13; 223: 11.15 to 11.17; 231: 11.11 to 11.13; 241: 11.13 to 11.15; 243: 11.11 to 11.13; 248: 11.11 to 11.13; 257: 11.12 to 11.14; 259: 11.15 to 11.17; 261: 11.15 to 11.17; 266: 11.15 to 11.17 |
| `work/build/guide/specimens/s-19-criteria.html` | Tracker designer | output of stage_c_ch19_build.py | 10: 1: 11.11 to 11.13, 11.15 to 11.17, 11.11 to 11.13, 11.13 to 11.15, 11.11 to 11.13, 11.11 to 11.13, 11.12 to 11.14, 11.15 to 11.17, 11.15 to 11.17, 11.15 to 11.17 |
| `work/build/tokens/src/oa-tokens.src.mjs` | Tracker designer | token_table_build.py's input, through tokens_build.mjs | 3: 139: 11.15 to 11.17; 398: 11.15 to 11.17; 599: 11.16 to 11.18 |
| `work/build/tokens/tokens.json` | Tracker designer | output of tokens_build.mjs | 3: 125: 11.15 to 11.17; 5290: 11.16 to 11.18; 5301: 11.16 to 11.18 |
| `work/build/guide/specimens/s-26-token-table.html` | Tracker designer | output of token_table_build.py | 2: 66: 11.16 to 11.18, 11.16 to 11.18 |
| `work/build/guide/specimens/manifest-systems.json` | Tracker designer | output of apply_systems_ch11.py (s-11-*), stage_a_systems_build.py (s-05-*), stage_b_ch12_systems_build.py (s-12-*) | 18: 51: 11.15 to 11.17; 746: 11.10 to 11.12; 755: 11.10 to 11.12; 764: 11.11 to 11.13; 774: 11.11 to 11.13; 783: 11.12 to 11.14; 787: 11.12 to 11.14; 793: 11.12 to 11.14; 802: 11.13 to 11.15; 812: 11.13 to 11.15; 821: 11.14 to 11.16; 831: 11.14 to 11.16; 840: 11.15 to 11.17; 850: 11.15 to 11.17; 862: 11.16 to 11.18; 871: 11.16 to 11.18; 1149: 11.16 to 11.18; 1160: 11.16 to 11.18 |
| `work/build/scripts/phase-2/guide_build.py` | Engineer | docstring only | 2: 1669: 11.12 to 11.14, 11.15 to 11.17 |
| `work/build/scripts/phase-2/stage_c_ch18_build.py` | Component engineer | generator | 16: 276: 11.11 to 11.13; 286: 11.16 to 11.18; 505: 11.13 to 11.15; 530: 11.13 to 11.15; 892: 11.12 to 11.14; 899: 11.12 to 11.14; 908: 11.12 to 11.14; 941: 11.11 to 11.13; 988: 11.11 to 11.13; 1084: 11.16 to 11.18; 1092: 11.15 to 11.17; 1132: 11.15 to 11.17; 1223: 11.10 to 11.12; 1235: 11.10 to 11.12; 1309: 11.14 to 11.16; 1315: 11.14 to 11.16 |
| `work/build/guide/chapters/18-components.json` | Component engineer | output of stage_c_ch18_build.py | 15: 61: 11.11 to 11.13; 63: 11.16 to 11.18; 391: 11.13 to 11.15; 443: 11.13 to 11.15; 1033: 11.12 to 11.14; 1046: 11.12 to 11.14; 1113: 11.11 to 11.13; 1194: 11.11 to 11.13; 1352: 11.16 to 11.18; 1369: 11.15 to 11.17; 1437: 11.15 to 11.17; 1602: 11.10 to 11.12; 1635: 11.10 to 11.12; 1759: 11.14 to 11.16; 1760: 11.14 to 11.16 |
| `work/build/guide/specimens/manifest-components.json` | Component engineer | output of stage_c_ch18_build.py | 1: 110: 11.12 to 11.14 |
| `work/build/guide/code/c-18-button.css` | Component engineer | code set (comment a reader copies) | 1: 104: 11.16 to 11.18 |
| `work/build/guide/code/c-18-form.css` | Component engineer | code set (comment a reader copies) | 2: 1: 11.15 to 11.17, 11.16 to 11.18 |
| `work/build/guide/code/c-18-form.js` | Component engineer | code set (comment a reader copies) | 2: 1: 11.15 to 11.17; 3: 11.16 to 11.18 |
| `work/build/guide/code/c-18-link.css` | Component engineer | code set (comment a reader copies) | 1: 1: 11.13 to 11.15 |
| `work/build/guide/code/c-18-messages.css` | Component engineer | code set (comment a reader copies) | 1: 1: 11.15 to 11.17 |
| `work/build/guide/code/c-18-tracker.css` | Component engineer | code set (comment a reader copies) | 1: 228: 11.10 to 11.12 |
| `work/build/guide/shell/guide-shell.css` | Component engineer | the shell (comment) | 2: 614: 11.12 to 11.14, 11.15 to 11.17 |
| `work/build/scripts/phase-3/phase3_ch15_build.py` | Systems designer | generator | 3: 2316: 11.14 to 11.16; 2332: 11.14 to 11.16; 3583: 11.14 to 11.16 |
| `work/build/guide/chapters/15-systems-graphics.json` | Systems designer | output of phase3_ch15_build.py | 3: 683: 11.14 to 11.16; 717: 11.14 to 11.16; 1158: 11.14 to 11.16 |

`civic_line_stage_b_drawings.py` and `stage_c_ch18_anatomy_build.py` hold no chapter 11 rule (coordinates only), so neither changes.

**Also by ID (hyphenated, not in the count above):** `s-11-10-*` to `s-11-16-*` in my generators, `11-icons.json` and `manifest-systems.json`; the radio group name `s-11-11-size` in `apply_systems_ch11_ui.py` (becomes `s-11-13-size`); `#rule-11-1x` anchors in `s-11-menu.html` (mine) and `s-19-criteria.html` (mine, from `stage_c_ch19_build.py`'s rule lists).

### Lines for other owners

- **Engineer, `guide_build.py`:** line 1669, the docstring of the status line helper, "Rules 11.12 and 11.15" becomes "Rules 11.14 and 11.17". No output changes.
- **Component engineer, `stage_c_ch18_build.py`:** 16 matches at lines 276 (11.11 to 11.13), 286 (11.16 to 11.18), 505 and 530 (11.13 to 11.15), 892, 899 and 908 (11.12 to 11.14), 941 and 988 (11.11 to 11.13), 1084 (11.16 to 11.18), 1092 and 1132 (11.15 to 11.17), 1223 and 1235 (11.10 to 11.12), 1309 and 1315 (11.14 to 11.16). Its outputs then carry them: `18-components.json` (15) and `manifest-components.json` (1, line 110). `stage_c_ch18_anatomy_build.py`: none.
- **Component engineer, code sets and shell:** `c-18-button.css` line 104 (11.16 to 11.18); `c-18-form.css` line 1 (11.15 to 11.17, 11.16 to 11.18); `c-18-form.js` lines 1 (11.15 to 11.17) and 3 (11.16 to 11.18); `c-18-link.css` line 1 (11.13 to 11.15); `c-18-messages.css` line 1 (11.15 to 11.17); `c-18-tracker.css` line 228 (11.10 to 11.12); `guide-shell.css` line 614 (11.12 to 11.14, 11.15 to 11.17). The code sets' comments are text a reader copies.
- **Systems designer, `phase3_ch15_build.py`:** lines 2316, 2332 and 3583, "Rule 11.14’s plate" becomes "Rule 11.16’s plate" (the loop stepper). Its output `15-systems-graphics.json` lines 683, 717 and 1158 follow.

### Mine, applied in this pass

`apply_systems_ch11.py` and `apply_systems_ch11_ui.py` (and their outputs: `11-icons.json`, `s-11-*`, the `s-11-*` entries of `manifest-systems.json`); `stage_a_systems_ch05.py` (chapter 05, the `s-05-*` entry); `stage_b_ch12_systems_build.py` (chapter 12, the `s-12-*` entries); `stage_c_ch17_build.py` and `stage_c_identity_ch17.py` (chapter 17); `stage_c_ch19_build.py` (`s-19-criteria.html`); and `token_table_build.py`'s input, `work/build/tokens/src/oa-tokens.src.mjs` (three strings: a reason, a comment and the description of the emphasis red's yield), with `tokens.json` rebuilt by `tokens_build.mjs` and `s-26-token-table.html` by `token_table_build.py`. Engineer: I touch only those three strings in the token source, after `tokens_build.mjs --check` passed at 01:44, and rebuild only if the check still passes just before.

## Routine calls

- D3-xxx | Chapter 11's specimen IDs follow their rules: `s-11-10-*` to `s-11-16-*` become `s-11-12-*` to `s-11-18-*`, and the new trackers take `s-11-10-*` and `s-11-11-*` | An ID that names another rule's number would mislead the next builder; nothing outside my two generators names them
- D3-xxx | DR-274's map is applied by one function over every match, with no chained replaces, and each output is proved by mapping its committed text and comparing it whole | A chain would carry 11.12 to 11.14 and on to 11.16; the comparison shows no other byte moved
- D3-xxx | Stage A's first run since token set 6.0.0-gate2.9 prints "29 chart tints" in Rule 05.6's caption, where it printed 27 | The count is read from `oa.color.tint` in tokens.json 6.0.0-gate3.3; the engineer's tints of rounds 1 to 4 added two, and no other figure in chapters 05 to 07 moved (the color shares and every rendered measure came out as before). The main session's snapshot `376f5a52` holds it
- D3-xxx | The 78 matches in Civic Line coordinates, identity path data and Missouri's 2022 minimum wage of $11.15 stay as they are | Each is a size or a data value, read in context

## Requests

### To the engineer
1. R5-8: `guide_build.py` line 1669 (above). Also a heads-up: I edit three strings in `work/build/tokens/src/oa-tokens.src.mjs` for R5-8 (lines 139, 398 and 599) and rebuild `tokens.json` and the token table; nothing else in the token set moves.

### To the component engineer
1. R5-8: the 16 lines in `stage_c_ch18_build.py` and the 10 in the six code sets and the shell (above).

### To the systems designer
1. R5-8: the three lines in `phase3_ch15_build.py` (above).

## Tested

- **R5-8 scan** (`r58_scan.py`): 281 matches in 57 files at 01:44, classified by hand in context: 78 values, 203 rule citations. After the pass, no `11.10` or `11.11` remains in `work/build/` outside the two board builders.
- **Baseline before any edit:** `apply_systems_ch11.py`, `stage_b_ch12_systems_build.py`, `stage_c_ch17_build.py` rewrote their files unchanged; `stage_c_ch19_build.py --check` current; `tokens_build.mjs --check` and `token_table_build.py --check` current. Stage A (`stage_a_systems_build.py probe`, `stage_a_systems_capture.js`, `final`, scratch `stageA0/`) moved one figure, the tint count (routine calls), and the measurement record's token set line and render date.
- **After the map:** each output equals its committed text with the map applied, compared whole by script (`r58_verify.py`): chapters 05, 11, 12 and 17, `s-11-menu.html`, `s-19-criteria.html`, the ten renamed chapter 11 specimens (old ID against new), and `manifest-systems.json` entry by entry. Stage A's probe pages and probes after the edit are byte for byte those of the baseline, so its capture stands; `final` ran on it (`stageA1/`).
- **Second run:** the full chain (V12 with V15's chapter 17, plus `stage_c_ch19_build.py`; `chain.sh` in scratch) over hashes of every file under `work/build/guide`, `work/build/tokens`, `work/build/assets` and `work/handoffs/phase-2`: no file changed.

## Not tested
