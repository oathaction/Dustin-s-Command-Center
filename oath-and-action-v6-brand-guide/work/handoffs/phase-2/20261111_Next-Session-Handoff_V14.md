# Handoff for the next session: Oath & Action Edition 06 (fourteenth handoff, November 11)

Written November 11, 2026, after drawings board C's promotion and stage C's round 1. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `20261110_Next-Session-Handoff_V13.md`. V5's sections 3 to 5 and section 3 of V8 to V13 still hold, with the additions below. Decision log entries for this chat run from DR-213 to DR-218 and from D2-1260 to D2-1530. The change ledger runs to C-071.

## 1. Where things stand

| Page | Address | Status |
|---|---|---|
| Chapters page (01 to 12, 17, 18, 19, 26, identity proofs) | https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF | Version 6 (1794372751-f710), published privately at this handoff as the preview of DR-215, no decisions asked (D2-1528). Board C republishes it as version 7 |
| Drawings board C | https://claude.ai/artifact/LtEuA2zNh1WUidhd4cAVsH | Answered (DR-207 to DR-211) and promoted (C-066 to C-071) |

**Dustin's answers this chat** (to the plan's three questions, "go with all your recs or defaults"):
- DR-213: chapter 19's device script covers iPhone with VoiceOver, Android with TalkBack, Windows with NVDA and a contrast theme, and Mac with VoiceOver; the Gate 2 report lists each as not tested.
- DR-214: chapter 26 ships tokens.css and tokens.json; a Canva brand kit sheet and a Figma variables file come with Phase 3's asset package only if he asks.
- DR-215: a private preview of the chapters page at this handoff, with no decisions asked.

**Promotion, closed (D2-1333).** CL-075 Housing in the set in use (125 drawings); the 37 fits in `civic-line-v6/fit-24/` with the switch on all 41 (77 switches in the page, `fitSwitch` in the guide check); the 16 px Pause and Filter A, the replaced files in `utility/_archive/`; the print L3 for print and the screen widths the display masters allow, with L3 under 40 px tall keeping the pixel masters (D2-1329, for Dustin to confirm on board C); the 96 px social sign-off; chapters 01, 03, 05, 08, 09, 10 and 11 brought into line, F-1 to F-5 and F-9 fixed. Checked on chapters 01 to 12 alone: chain clean, strict build 0 warnings, token tests pass, guide check at four widths 0 failures.

**Round 1, built.**
- Chapter 17, Motion and states: 12 rules (17.11 disabled and 17.12 empty added), three players on request, the identity designer's hinge and lever (Rule 17.6), the canonical ten-states plate (17.8).
- Chapter 18, Components and interaction: 24 rules in seven groups, 24 code sets (65 files) in `work/build/guide/code/`, 24 keys files, 24 anatomy plates, failure plates; about 1.1 MB against a 1.25 MB ceiling (D2-1468).
- Chapter 19, Accessibility: 9 rules; the 55 criteria in W3C's words (37 met, 5 in part, 8 gaps owed by chapters 02, 16, 20 and 23, 5 not applicable yet); the matrix; dated results; DR-213's device scripts.
- Chapter 26, Tokens and how to choose them: rules 26.1 to 26.8, the token table, the four worked examples as code.
- The engineer's round 1 checks: `keyPath`, the motion check, the token table's parity, with the guide check's page loading fixed for a page past 9 MB.
- The editor read every changed word in 01 to 12 and all four new chapters; every row went to its owner.

**Final checks on commit 10ba650b (D2-1527).** The generator chain changed no file. `guide_build.py --strict`: 0 warnings, 16 chapters, 185 rules, 420 specimens, 9,544,650 bytes. The token tests pass. `guide_check.js` at 1440, 1024, 390 and 360 px: 1,917 same-page links; `fitSwitch` 77 of 77 at 1x, 2x and 3x; `keyPath` 140 walks of 37 paths; `motion` 7 of 7 with the final frame at once under reduced motion; `tokenTable` 500 rows at 6.0.0-gate2.7; one failure, `codeMatch` at 360 px on c-18-tracker in the light theme, one flat-area pixel 1 of 255 apart. The engineer found it was the check's fault (an edge where Pillar Red meets the Charcoal keyline, judged by luminance alone) and fixed the check; its rerun on a fresh build of 10ba650b passes at four widths with 0 failures (D2-1530). The page did not change, so the preview is the checked build.

**For round 2's reviewers, noted by the main session:** chapter 26's token table stacks every row at desktop widths (D2-1529); `codeMatch` allows edge differences up to 49 of 255 (D2-1526); the dark-card feed test's 2 by 2 block (D2-1331); the token description release and the error bar rename (D2-1524, D2-1525).

**Approved after the preview (DR-216 to DR-218)**, Dustin: "i approve all recs":
- DR-216: Rule 12.4's hinge arcs retire and the rule is rewritten as the creative director drafted it; the identity designer wires its rewrite into chapter 12 in round 2's fix pass.
- DR-217: L3 under 40 px tall keeps the pixel masters; the 196 px minimum stays at 2.43 cap heights.
- DR-218: token release 6.0.0-gate2.8 cleans the reader-facing descriptions, and the error mark's token becomes `oa.color.state.error.bar` with a one-release alias, both in round 2's fix pass.

Board C still carries any call round 2 raises, and shows chapter 12 with DR-216 in place.

**Carried.** Missouri's certified count, at the Gate 2 preview (D2-1118; the county deadline is November 17). The dark-card feed test's 2 by 2 block count, for the creative director in round 2 (D2-1331). The proofs' card 0.16 px off the pixel grid (D2-1332). Open questions Q-04, Q-11 and Q-12.

## 2. Next, in order

### A. Round 2 (stage C brief, "Order of work" 4)
Freeze one copy of the page. Three red teams as DR-190 set them, with the creative director reading at the same time and scoring chapters 17, 18, 19 and 26 on the six criteria. The production test asks a simulated developer to build a component the guide does not show, from chapters 18 and 26 alone, and to switch it to dark mode. One fix pass, DR-191's short second pass, the editor's read and the creative director's rescore.

### B. Board C
The chapters page republished as version 6, and a short decisions board with the items above and any call round 2 raises.

### C. Gate 2
The preview build of chapters 01 to 12, 17, 18, 19 and 26 as one file, and the Gate 2 report with the Phase 3 proposal, page weight carried as a risk (D2-1214).

## 3. Working notes added this chat

- **Fresh container.** V11's three steps still work.
- **Do not rerun the November 10 promotion scripts** (`civic_line_v6_promote.py` and its kin). They would undo this chat's promotion. `stage_c_icons_promote.py` is the current one.
- **Logging owners' calls.** `work/build/scripts/phase-2/log_routine_calls.py <notes> "<heading>" ["<section>"]` numbers a notes file's "D2-xxx" lines into the log by its section heading. Check for repeated numbers afterwards with the grep in its header.
- **Two engineer instances.** The guide engineer owns `guide_build.py`, `guide_check.js` and the shell; the component engineer owns `work/build/guide/code/`. Every other maker sends build needs through the main session. It worked with no collision.
- **Fixed names ahead.** The round 1 brief fixed chapter 17 and 26's rule numbers and chapter 18's 24 code set names before any maker started, so 18 could cite 17 and 26 while they were written, and the keys files met the code.
- **One manifest per new chapter** (D2-1267), plus `manifest-anatomy.json` for the plates another owner drew.
- **The guide check on a large page.** Past about 9 MB the browser parses beyond `networkidle`'s quiet window; the engineer's fix waits for the page itself. A quick check that times out has not checked anything.
- **Never chain `git checkout --` into a check command while agents write.** This chat did once, to undo the token tests' timestamp; nothing was lost, but it could have discarded an agent's work.
- **Context.** This chat ran ten agents and about twenty resumed runs. Hand off after each board, and before round 2.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from DR-213 on), the change ledger and the open questions.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-2/20261111_Next-Session-Handoff_V14.md, then section 3 of V5 to V13's handoffs as V14 lists them, the stage C brief 20261110_Stage-C-Brief.md, the round 1 brief 20261111_Stage-C-Round-1-Brief.md, and the round 1 notes V14 names.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons, which are final and approved (DR-144), with the redraws and new drawings I approved on the drawings boards (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); the atlas visual system (System 1, DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and Phase 3 build order (DR-62, DR-63); the chart rules of DR-64; chapter 02's writing rules (DR-73 to DR-83); and every answer I have given from DR-95 on.

Round 1 of stage C is built. Run round 2, board C and the Gate 2 preview as the fourteenth handoff orders.

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

## 5. Change log of this chat

Created, all under `work/` unless named:
- **Briefs:** `handoffs/phase-2/20261111_Promotion-Stage-C-Brief.md`, `20261111_Stage-C-Round-1-Brief.md`.
- **Notes and reviews:** `20261111_Promotion-C-Icons-Notes.md`, `-Identity-Notes.md` with `20261111_Promotion-C-Identity-Figures.json`, `-Engineer-Notes.md`, `-Systems-Notes.md` with `20261111_Promotion-C-Ch10-Labels-Addendum.json`; `20261111_CD-Review-Of-Rule-12-4.md`; `20261111_Stage-C-Round-1-Ch17-Notes.md`, `-Ch18-Notes.md`, `-Ch19-Notes.md` with `-Ch19-Results.json`, `-Components-Engineer-Notes.md`, `-Anatomy-Notes.md`, `-Identity-Notes.md`, `-Engineer-Notes.md`, `-Editor-Notes.md`; this handoff; `stage-c-identity/20261111_Rule-12-4-Comparison*`.
- **Assets in use:** CL-075 Housing in `build/assets/civic-line-v6/`; `civic-line-v6/fit-24/` (the 37 fits and their manifest); `utility/svg-16/20261111_Utility-Pause-16px.svg` and `-Filter-16px.svg`; `utility/_archive/` (the replaced files, moved).
- **Scripts:** `build/scripts/phase-2/stage_c_icons_promote.py`, `stage_c_ch17_build.py`, `stage_c_ch18_build.py`, `stage_c_ch18_anatomy_build.py`, `stage_c_ch19_build.py`, `stage_c_ch26_build.py`, `stage_c_identity_ch17.py`, `log_routine_calls.py`.
- **Chapters, specimens and code:** `build/guide/chapters/17-motion-and-states.json`, `18-components.json`, `19-accessibility.json`, `26-tokens.json`; specimens `s-17-*`, `s-18-*`, `s-19-*`, `s-26-*`, `s-10-opener`; manifests `manifest-motion.json`, `-components.json`, `-anatomy.json`, `-accessibility.json`, `-tokens.json`; `build/guide/code/c-18-*` (65 files plus 24 keys files) and `c-26-*`.

Modified:
- `ledger/20261020_Decision-Log.md` (DR-213 to DR-215, D2-1260 to D2-1529), `ledger/20261020_Change-Ledger.md` (C-066 to C-077).
- The Civic Line inventory (125 rows), the utility manifest, the identity minimum sizes record.
- Chapters 01, 03, 05, 08, 09, 10 and 11 through their generators (`stage_a_systems_build.py`, `stage_b_ch10_build.py`, `apply_systems_ch11.py`, `apply_systems_ch11_ui.py`, `stage_a_identity_chapters.py`, `stage_a_identity_proofs.py`, `stage_a_identity_lib.py`, `stage_b_identity_ch01.py`, `stage_b_identity_ch09.py`, `stage_b_identity_ch12.py`), with the chapter 10 labels file.
- `guide_build.py`, `guide_check.js`, `sprite_check.js`, `icon_likeness_check.js`, the shell, `token_table_build.py` and the token tests' results.
- The chapters page and its build and check reports in `boards/phase-2/stage-a/`.
