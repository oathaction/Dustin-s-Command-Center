# Round 5 notes: tracker designer, R5-8's number map and Rules 11.10 and 11.11

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Written by the tracker designer (a general-purpose agent briefed as the designer who drew chapter 11's trackers and chapters 11, 12 and 15's systems plates) for `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`, under R5-7, R5-8, DR-274 and DR-275. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Status

03:10 UTC. **The design director's three Shoulds are done (DD-T1 to DD-T3), on the file as the editor's trackers pass left it (02:49).** DD-T1: the bill's step table after Rule 11.1 (`s-11-steps`) now sets each number over its name in a 10rem column and stacks under 30rem, as the two new tables do; it is an approved plate, listed for board 3 below. DD-T2: met by the editor's 02:49 words, which already put 99010's count first ("The polls closed on November 3, and the count is unofficial ..."); no change from me. DD-T3: Rule 11.11's title holds "a denied petition" with no-break spaces, as 14.143's title holds "a variable". Two runs, the second changing nothing; only `11-icons.json` (the title), `s-11-menu.html` (the same title in the phone menu, two no-break spaces) and `s-11-steps.html` moved. Strict build `guide9.html` (03:01): exit 1 on two warnings, both chapter 14's `s-14-s96`, none of chapter 11's; 369 rules; chapter 11 at 500,801 bytes. `s-11-steps` captured at five widths on both grounds (03:08, load 3.92 to 6.32), 10, 0 flagged, read at 1440 and 360 on Newsprint.

**For the accessibility lead:** no tracker's markup changed. Two things you may test: `s-11-steps` now hides its column heads under 30rem of plate width (`thead{display:none}`), as the two new step tables already do, so at a phone's width the table has no column heads in the accessibility tree and each row reads as its step heading then its words; and Rule 11.11's title now carries two no-break spaces, so its text is the same and only its line breaks change.

**Board 3, changed approved drawings:** `s-11-steps` (Rule 11.1's extra, "The six steps"), layout only: number over name, a 10rem first column, stacked rows under 30rem. Its words, inks and markup are as approved.

**For the systems designer (Rule 15.23): the trackers have landed, and their step names are final** (the editor kept all twelve):
- **11.10, a state ballot measure (citizen initiative):** 1 Filed, 2 Title and summary, 3 Signatures, 4 Legislature (a slash where the initiative is direct), 5 On the ballot, 6 Vote (current until the count is certified).
- **11.11, a federal civil case:** 1 Filed, 2 Trial court ruling, 3 Appeal, 4 Appeals court ruling, 5 Supreme Court petition (a denied petition ends here on a square), 6 Supreme Court ruling.
Read them from `BALLOT_STEPS` and `COURT_STEPS` in `apply_systems_ch11.py` (each row: name, the editor's words for what happens, the law) or from the plates `s-11-ballot-steps` and `s-11-court-steps`.

R5-8: done and proved (01:49), signed off by the data lead (batch 1, 02:27). Token source edit landed at **01:46 UTC** (three strings in `work/build/tokens/src/oa-tokens.src.mjs`, lines 139, 398 and 599); the engineer owns the rebuild.

## Summary

**R5-8 (DR-274).** Every match of `11.10` to `11.16` across `work/build/` listed by script, read in context (78 sizes and data values set aside, 203 rule citations), mapped by owner under "Contracts" at 01:45, and applied in my files in one pass: chapter 11's two generators, chapter 05 (stage A), 12, 17 and 19's generators, and three strings in the token source. Each output equals its committed text with the map applied and nothing else; the full chain's second run changed no file. Chapter 11's specimens follow their rules' numbers.

**Rules 11.10 and 11.11 (DR-231, DR-275, R5-7).** Two six-step trackers in group 2 on chapter 11's marks: a state ballot measure (a citizen initiative: Filed, Title and summary, Signatures, Legislature, On the ballot, Vote) and a federal civil case (Filed, Trial court ruling, Appeal, Appeals court ruling, Supreme Court petition, Supreme Court ruling). Each has a correct plate of three invented items labeled Illustrative (one current, one decided or certified, one stopped, as ruling (f) asks), a failure plate of the misreading the facts warn of (an election night count printed as approved; a denied petition printed as a Supreme Court ruling), and a step table with what happens at each step and where the law sets it. Step names from the research lead, end words from the editor (02:16), marks under ruling (f). Group 2's title, line and the chapter intro take in the new trackers in the editor's words, and Rule 11.12 (old 11.10) now names a wait for all four trackers in group 2.

**Weight (reported, DR-271).** Rules 11.10 and 11.11 with their four plates and two tables: 59,853 bytes in the page (strict build `guide8.html`, 02:41). The plates with their frames: `s-11-10-correct` 11,829, `s-11-10-failure` 7,006, `s-11-11-correct` 10,888, `s-11-11-failure` 6,028, the tables `s-11-ballot-steps` 6,349 and `s-11-court-steps` 5,356; 47,456 in all. Chapter 11: 436,762 bytes before round 5, 500,217 now, of its 550,000. The page at 12,090,327 bytes, projected 15,117,037, with every owner's work in progress.

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

`apply_systems_ch11.py` and `apply_systems_ch11_ui.py` (and their outputs: `11-icons.json`, `s-11-*`, the `s-11-*` entries of `manifest-systems.json`); `stage_a_systems_ch05.py` (chapter 05, the `s-05-*` entry); `stage_b_ch12_systems_build.py` (chapter 12, the `s-12-*` entries); `stage_c_ch17_build.py` and `stage_c_identity_ch17.py` (chapter 17); `stage_c_ch19_build.py` (`s-19-criteria.html`); and `token_table_build.py`'s input, `work/build/tokens/src/oa-tokens.src.mjs` (three strings: a reason, a comment and the description of the emphasis red's yield), with `tokens.json`, the token tests and `s-26-token-table.html` left to the engineer, who owns `work/build/tokens/` (main session, 01:52). Engineer: I touched only those three strings in the token source (01:46), after `tokens_build.mjs --check` passed at 01:44; the rebuild is yours (main session, 01:52).

## Routine calls

- D3-xxx | Chapter 11's specimen IDs follow their rules: `s-11-10-*` to `s-11-16-*` become `s-11-12-*` to `s-11-18-*`, and the new trackers take `s-11-10-*` and `s-11-11-*` | An ID that names another rule's number would mislead the next builder; nothing outside my two generators names them
- D3-xxx | DR-274's map is applied by one function over every match, with no chained replaces, and each output is proved by mapping its committed text and comparing it whole | A chain would carry 11.12 to 11.14 and on to 11.16; the comparison shows no other byte moved
- D3-xxx | Stage A's first run since token set 6.0.0-gate2.9 prints "29 chart tints" in Rule 05.6's caption, where it printed 27 | The count is read from `oa.color.tint` in tokens.json 6.0.0-gate3.3; the engineer's tints of rounds 1 to 4 added two, and no other figure in chapters 05 to 07 moved (the color shares and every rendered measure came out as before). The main session's snapshot `376f5a52` holds it
- D3-xxx | The 78 matches in Civic Line coordinates, identity path data and Missouri's 2022 minimum wage of $11.15 stay as they are | Each is a size or a data value, read in context

- D3-xxx | Rule 11.10 follows a citizen initiative in six steps: Filed, Title and summary, Signatures, Legislature, On the ballot, Vote; a direct initiative keeps step 4 under a slash | The research lead's frame from four states' constitutions and California's election office; ruling (f): a slash marks a step the law gives the item no room for
- D3-xxx | Rule 11.11 follows a federal civil case in six steps: Filed, Trial court ruling, Appeal, Appeals court ruling, Supreme Court petition, Supreme Court ruling | The research lead's frame from Title 28, the federal rules and the Supreme Court's rules; each court's ruling is its own step, so the end words can say which court spoke last
- D3-xxx | A denied petition ends the case on a square at step 5, with "Petition denied by the Supreme Court" and the date (the editor's words); a case decided at trial and never appealed ends on a square at step 2 | Ruling (f): an item that ends before the last step ends on a square at the last step it reached, and a slash is only for a step the law does not give; this replaces the research lead's suggested slashes
- D3-xxx | A measure stays at step 6, current, until its count is certified, and its words then say Approved by voters or Rejected by voters with the dates of the vote and the certification (the editor's words) | Ruling (f): an unofficial count is no record of a done step; R5-7 asks a certified item to say so in words
- D3-xxx | Each plate's three items: ballot measures 99010 (direct, counted, not certified), 99011 (indirect, approved by voters and certified) and 99013 (did not qualify, a square at step 3); court cases 99014 (argued, waiting on the appeals court), 99015 (reversed and sent back by the Supreme Court, all six filled) and 99016 (review denied, a square at step 5) | Ruling (f) and DR-275: one current, one decided or certified, one stopped per plate; the subjects (park fees, library funding, shoreline setbacks, a bakery's trademark, a ferry contract, highway noise walls) tie to no party, and the outcomes favor no side
- D3-xxx | The failure plates draw the two misreadings the facts warn of: an election night count printed as "Approved by voters" with step 6 filled, and a denied petition printed as "Affirmed by the Supreme Court" with step 6 filled | R5-4's test of a common misreading; one fault each, the rest of each card drawn right
- D3-xxx | A remand prints in the end words ("Reversed and sent back by the Supreme Court on June 2") and a sentence, and the six marks stay filled | Ruling (f): the line never runs backward; the research lead's facts
- D3-xxx | No take-part mark on either new tracker's plates | A court case offers the public no step to take, and on a ballot measure a petition is a way to back one side; the vote's red would need its own ruling, so the plates leave it out
- D3-xxx | Each new tracker gets one readable table after its rule, its six steps with what happens and where the law sets it (`s-11-ballot-steps`, `s-11-court-steps`) | The steps are less familiar than a bill's, which has its own table after Rule 11.1; R4-3 puts reference sets in live text; Rule 15.23 maps these same steps
- D3-xxx | The invented items continue chapter 11's records counter past 99009 and skip 99012 | One counter keeps each number unique in the chapter (D2-848); H.R. 99012 holds 99012
- D3-xxx | Chapter 11's own tracker pieces take the surface color from the stage's role, `--oa-color-surface`, where they took Newsprint by name; chapter 01's card keeps the old call | On a Charcoal stage the done marks lost their numbers; on Newsprint the role resolves to Newsprint, so no pixel moves (proved, "Tested"); opt-in, so `guide_editor_ch01.py`'s output is untouched

- D3-xxx | The editor's words (02:16) applied: the twelve step names kept, each step's words in the step tables, the end words in group 2's frames ("Withdrawn by its sponsors", "Too few valid signatures to qualify", "Approved by voters", "Settled by the parties", "Petition denied by the Supreme Court" and the rest), Rule 11.11's title "Follow a court case through six steps, and end a denied petition at step 5.", and Rule 11.12's text for all four trackers (D3-1879) | The editor owns the words; each fact behind them is the research lead's
- D3-xxx | A measure the Legislature passes keeps steps 5 and 6 under slashes with "Passed by the Legislature on" and its date, in its own spec row; it takes no square | The data lead's sign-off (batch 1): it became law, and the square's key word is Stopped; the words describe the item and claim nothing about a later referendum
- D3-xxx | A higher court's ruling prints the docket's own verb, "Affirmed", explained once in Rule 11.11's text ("which leaves the ruling below in place"), with Reversed, Vacated and Modified | ED5-3 (data lead, batch 1): "Upheld" names no object and can read as a law upheld when a court affirmed its striking down; one constant, `AFFIRMED`, sets it
- D3-xxx | Executive Order 12866 takes its own source line behind Rule 11.12, and the court source line names 28 U.S.C. 1292 for Rule 11.12's injunction | Rule 11.12's new words cite both (the editor's D3-1879); the workflow sources file's dates (the order read November 12, 1292 November 14, 2026)

- D3-xxx | The three source points settled by the research lead (02:30): the court source line as it suggested (1253, 2284 and Neil v. Biggers added); the "Straight to the Supreme Court" row and Rule 11.11's text say an injunction order of a three-judge district court; a tie prints "Affirmed by an equally divided Court, which is a tie vote" | The data lead's batch 1 points; 1253 reaches only that order, and the Court's own words for a tie are its disposition (ruling (f))

- D3-xxx | Each new plate's key lists only the marks its cards use (the court plate drops Never happened) | Rule 11.5's spec: "every mark the list uses"; ruling (f) left the court plate no slash
- D3-xxx | The two step tables take the stage's role inks and set each step's number over its name, stacking number and name over the words under 30rem | On Charcoal the law lines in Newsprint's secondary ink nearly vanished; a long name wrapped under its number at 1440 px; the narrow columns squeezed the words at 360 px
- D3-xxx | "52 percent" holds together on the ballot failure plate | A figure stays with its unit at a line end, as `nb()` keeps "px" with its number

- D3-xxx | The bill's step table (`s-11-steps`) takes the new tables' grammar: number over name, a 10rem first column, stacked under 30rem; its words, inks and markup stay | DD-T1: one step-table grammar in chapter 11; "Governor or President" no longer wraps back under its 6; only this plate moved (hashes)
- D3-xxx | Rule 11.11's title holds "a denied petition" with no-break spaces | DD-T3: the article no longer ends a line at 1440 px; 14.143's title holds "a variable" the same way
- D3-xxx | DD-T2 needs no change from me | The editor's 02:49 words already set 99010's count before the slash's reason

## Requests

### To the editor
1. **Your question on Rule 11.12 (old 11.10): it covers all four trackers** (main session's routine call on ED5-2, and the research lead's facts). Waits inside a step, from the facts: a second round of signatures under a ballot measure's step 4; an order on an injunction and its appeal under a court case's step 2; a rehearing by the full appeals court under step 4. Steps after the end words: a lawsuit after a records request (as now); a case sent back to a lower court ("Reversed and sent back", then a sentence); the Legislature amending or repealing a measure the voters passed. An official status needs no warning mark when it comes from the agency's tracking service, the Federal Register, the court's docket or the state's election office. Its title can stay; its first sentence and "every request still counts to six" need your words for all four. Its plate stays as it is (main session). Write the lines here and I apply them in `apply_systems_ch11.py`.
2. **Words pass on Rules 11.10 and 11.11**, everything in `apply_systems_ch11.py` from `BALLOT_STEPS` to the two rules: each rule's title (15 words or fewer), rule, why, basis, captions, specs and builders; the step names and the "What happens" words of the two step tables (`BALLOT_STEPS`, `COURT_STEPS`) and the tables' labels and captions; the six invented items' titles, status lines and end words (`BALLOTS`, `COURTS`), with the failure plates' words in `s_11_10()` and `s_11_11()`; the four alts; the two new source lines. Built under the research lead's step names and ruling (f); the end words are the facts' own ("Passed", "Certified", "Did not qualify: too few valid signatures", "Review denied by the Supreme Court", "Reversed and sent back"). I applied your group 2 title, line and intro sentence, with "a state ballot measure" and "a federal court case" in the line, as your note asked once the facts said which.

### To the data lead
1. **Ruling (f) as built:** every slash is a step the law gives that item no room for (a direct initiative's step 4; an appeal from three district judges straight to the Supreme Court, steps 3 and 4, in the specs); every item that ends before step 6 ends on a square at the last step reached, a denied petition on step 5 and a measure the Legislature enacts on step 4 among them; the vote step stays current until the count is certified; end words name the court. Each plate holds one current, one decided or certified, one stopped item. Sign-off asked when the editor's pass lands. One point to confirm: a measure the Legislature enacts becomes law on a square, which the key calls Stopped; the words say "Enacted by the Legislature". It appears in the specs only.
2. **Invented numbers (your item on DR-151's practice):** measures 99010, 99011 and 99013 and cases 99014 to 99016 continue chapter 11's records counter past 99009 and skip 99012 (H.R. 99012). Checked: a federal case number carries its year before a hyphen (the research file's own "No. 22-451" for Loper Bright), so a bare five-digit number is no docket number; no state is named, so no measure number can match a state's. Not checked: every state's measure numbering scheme.

### To the research lead
1. Answered at 02:30 and applied at 02:30: your source line for Rule 11.11 word for word with its closing words; 28 U.S.C. 1253 and 2284 behind the "Straight to the Supreme Court" row, whose words now hold to an injunction order of a three-judge district court; the tie as "Affirmed by an equally divided Court, which is a tie vote", from Neil v. Biggers; the basis as you suggested. Nothing open.

### To the engineer
1. R5-8: `guide_build.py` line 1669 (above). Also: my three R5-8 strings in `work/build/tokens/src/oa-tokens.src.mjs` (lines 139, 398 and 599) landed at 01:46 UTC; the rebuild of `tokens.json`, the token tests and chapter 26's token table is yours (main session, 01:52).

### To the component engineer
1. R5-8: the 16 lines in `stage_c_ch18_build.py` and the 10 in the six code sets and the shell (above).

### To the systems designer
1. R5-8: the three lines in `phase3_ch15_build.py` (above).

## Tested

- **R5-8 scan** (`r58_scan.py`): 281 matches in 57 files at 01:44, classified by hand in context: 78 values, 203 rule citations. After the pass, no `11.10` or `11.11` remains in `work/build/` outside the two board builders.
- **Baseline before any edit:** `apply_systems_ch11.py`, `stage_b_ch12_systems_build.py`, `stage_c_ch17_build.py` rewrote their files unchanged; `stage_c_ch19_build.py --check` current; `tokens_build.mjs --check` and `token_table_build.py --check` current. Stage A (`stage_a_systems_build.py probe`, `stage_a_systems_capture.js`, `final`, scratch `stageA0/`) moved one figure, the tint count (routine calls), and the measurement record's token set line and render date.
- **After the map:** each output equals its committed text with the map applied, compared whole by script (`r58_verify.py`): chapters 05, 11, 12 and 17, `s-11-menu.html`, `s-19-criteria.html`, the ten renamed chapter 11 specimens (old ID against new), and `manifest-systems.json` entry by entry. Stage A's probe pages and probes after the edit are byte for byte those of the baseline, so its capture stands; `final` ran on it (`stageA1/`).
- **Second run:** the full chain (V12 with V15's chapter 17, plus `stage_c_ch19_build.py`; `chain.sh` in scratch) over hashes of every file under `work/build/guide`, `work/build/tokens`, `work/build/assets` and `work/handoffs/phase-2`: no file changed.

- **Trackers, generator:** `apply_systems_ch11.py` runs clean (its copy checks on every word, its specimen check: 18 rules, 45 specimens, none missing or unused); a second run changed no file (hashes, 02:21, after the editor's words). The full chain's second run (02:23) changed none of its outputs; the one file that moved between the hashes, `s-14-144-correct.html`, is the complex examples maker's and no generator in the chain writes it.
- **The surface change, proved:** two strict pages built from the same content, one with the 26 changed chapter 11 specimens put back to `--bg:var(--oa-color-surface-newsprint)` (`guide3old.html`, 260 bytes apart), compared at 390 px on Newsprint: all 22 old tracker plates and the opener pixel-identical, and their computed `--bg` the same, #DCD9D2 (`bgproof.js`, 02:16 to 02:19).
- **Strict builds** (`python3 -I work/build/scripts/phase-2/guide_build.py --strict`, to scratch): `guide1.html` (01:56, the first draft): exit 0, 0 warnings, 363 rules. `guide2.html` (02:10): exit 1 on chapter 14's `s-14-s96`, none of chapter 11's. `guide4.html` (02:22, after the editor's words): exit 0, 0 warnings. `guide5.html` (02:31, batch 1 and the source points), `guide6.html` (02:36), `guide7.html` (02:39): each exit 0, 0 warnings. `guide8.html` (02:41, final): exit 0, 0 warnings, 369 rules, 679 specimens, 12,090,327 bytes, projected 15,117,037; chapter 11 at 500,217. The cross-reference check in each proves every same-page link to a chapter 11 rule. Each build's rewrite of the chart kit's `plate-share.json` timestamp was put back (`build.sh`).
- **Captures of the first draft** (`capA/`, from `guide1.html`, 01:57 to 02:06): the six new plates at 1440, 1024, 768, 390 and 360 px, on Newsprint and with the stage set to Charcoal, 60 captures, 0 flagged by `cap.js` (type under 13 px, text outside the stage, SVG text overlapping, sideways scroll). Read by eye, they showed two faults, both fixed: on Charcoal the done marks lost their numbers (the surface change above), and the step tables' narrow layout kept the name at its wide width and never reached three columns inside the guide's 606 px stage (redrawn as two columns, the law under each step's words).
- **The captures, by run, each with the load beside it** (`cap.js`: Chromium, element shots of each figure, the stage set to Newsprint and to Charcoal, measured for type under 13 px, text outside the stage, SVG text overlapping and sideways scroll):
  - `capA/` from `guide1.html`, 01:57 to 02:06, load 3.53 at the start, 4.19 at the end: 60, 0 flagged (the first draft, above).
  - `capC/` from `guide4.html`, 02:23 to 02:35, load 3.98 at the start and 8.28 at the end (other owners' browsers rose during it): 60, 0 flagged. Its measures stand, but its pictures were offset upward by a layout shift after measuring and cut off the foot of tall plates, so it is not the record of how the plates look; the capture method then changed (a tall viewport, the figure measured again after scrolling, the shot clipped from the viewport).
  - `capD/` from `guide6.html`, 02:37 to 02:39, load 3.95 to 4.19: the six new plates at 1440, 1024, 768, 390 and 360 px on both grounds, 60, 0 flagged. Read by eye: every plate at 360 on Newsprint, 11.11's correct plate at 768 on Newsprint and at 360 and 1440 on Charcoal, 11.10's correct plate at 1440 on Charcoal, 11.10's failure at 1024 on Charcoal, 11.11's failure at 390 on Charcoal, the court table at 360. That read found the court key's unused mark and the narrow table's squeezed words (both fixed).
  - `capE/` from `guide7.html`, 02:39 to 02:40, load 3.96 to 4.20: the two tables, 20, 0 flagged. Read by eye at 360 on Charcoal and 1440 on Newsprint: the law lines nearly vanished on Charcoal and a long name wrapped under its number (both fixed).
  - `capF/` from `guide8.html`, 02:42 to 02:43, load 3.99 to 4.96: `s-11-10-failure` and the two tables, 30, 0 flagged. Read by eye: the court table at 1440 on Charcoal, the ballot table at 390 on Newsprint, the failure plate at 360 on Newsprint.
  - The final state, then: `s-11-10-correct`, `s-11-11-correct` and `s-11-11-failure` as in `capD/` (no byte of them changed after `guide6.html`), and `s-11-10-failure` and the two tables as in `capF/`.
- **Words, by script:** no em dash, en dash, U+2011, straight apostrophe or straight quote in any new rule, caption, alt or plate text of chapter 11.
- **Generator, last runs:** after each change from 02:31 to 02:41, two runs of `apply_systems_ch11.py` with hashes of every file under `work/build/guide`, `work/build/tokens`, `work/build/assets` and `work/handoffs/phase-2`: the second run changed no file each time.

## Not tested

- Rule 11.11's title at 1440 px after DD-T3: built and checked in the text (two no-break spaces), not captured, since the load stood at 6.32 after the last capture.
- A screen reader; forced colors; 200 percent text; Safari and Firefox.
- The guide check (`guide_check.js`), quick or full: not run, to keep the browser load down; the strict build's cross-reference check proves every same-page link ("Rule 11.x" and `#rule-11-x`).
- The chapter 11 plates I did not change, on Charcoal: on a Charcoal stage they now keep their numbers (the surface change), but only the six new plates were captured on Charcoal.
- Every state's ballot measure numbering, and every federal court's docket form beyond the year-hyphen form the research file shows (No. 22-451), for the invented numbers.
- The stage A capture after the R5-8 edit: its probe pages and probes were byte for byte the baseline's, so the baseline capture (01:46) was reused for `final`; the capture itself ran once.

## Files

Modified (none created outside these generators' outputs):
- `work/build/scripts/phase-2/apply_systems_ch11.py`: R5-8; Rules 11.10 and 11.11, their four plates and two step tables; group 2, the intro and Rule 11.12's words; three source lines (the ballot measure, the court case, Executive Order 12866); the opt-in surface color. Its outputs: `work/build/guide/chapters/11-icons.json`, `work/build/guide/specimens/s-11-*.html` (new: `s-11-10-correct`, `s-11-10-failure`, `s-11-11-correct`, `s-11-11-failure`, `s-11-ballot-steps`, `s-11-court-steps`; renamed by R5-8: old `s-11-10-*` to `s-11-16-*` now `s-11-12-*` to `s-11-18-*`; 26 others rewritten for the surface color, no pixel moved on Newsprint); `s-11-steps` re-laid for DD-T1 (an approved plate, listed for board 3), the `s-11-*` entries of `work/build/guide/specimens/manifest-systems.json`.
- `work/build/scripts/phase-2/apply_systems_ch11_ui.py`: R5-8 only (41 numbers, 26 IDs).
- R5-8 string edits only: `work/build/scripts/phase-2/stage_a_systems_ch05.py` (with `work/build/guide/chapters/05-color.json`, the `s-05-3-corrective` manifest entry, and `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json`'s token set line, render date and tint count); `stage_b_ch12_systems_build.py` (with `12-graphic-devices.json` and the `s-12-*` manifest entries); `stage_c_ch17_build.py` (with `17-motion-and-states.json`); `stage_c_identity_ch17.py` (a code comment); `stage_c_ch19_build.py` (with `s-19-criteria.html`); `work/build/tokens/src/oa-tokens.src.mjs` (three strings; the rebuild is the engineer's).
- `work/handoffs/phase-3/20261114_Round-5-Tracker-Designer-Notes.md` (this file).

Scratch (not delivered): `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/tracker-designer/`: the scan, map and proof scripts (`r58_*.py`, `bgproof.js`, `cap.js`, `chain.sh`, `hashes.sh`, `build.sh`), strict builds `guide0.html` to `guide6.html` with their reports, captures `capA/` to `capD/`.
