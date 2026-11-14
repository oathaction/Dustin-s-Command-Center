# Round 5 engineer notes

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md` (DR-272 to DR-276). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/engineer/` (`scratch/` below). The component engineer owns `work/build/guide/code/`, the shell and chapter 18's generators this round; I write none of those files.

## Status

- 01:40 UTC (clock read): started. Read `CLAUDE.md`, my role file, the round 5 brief, round 4's brief and my round 0 to 4 notes' contracts.
- 01:44 UTC (clock read): writing R5-1 to R5-3 and the kit's needs for complex example 1 under "Contracts" below. Until a section says **SET**, it is not yet a contract.
- 01:50 UTC (clock read): **R5-8 done** for my files (one docstring in `guide_build.py`), and the token rebuild with chapter 26's table after the tracker designer's three strings (under R5-8 below).
- 01:52 UTC (clock read): **Contracts SET: R5-1, R5-2a, R5-2, R5-3's mechanics, S96's kit side.** **LANDED:** the plan file's round 5 rows (group 18, Rules 14.142 to 14.144 with S96 and the reserved S97 and S98, the two extras); `phase3_ch14_build.py` (rounds 1 to 5 by default, group 18's rules with an optional failure plate, a rule's kit plate `s-14-s96`, `PLATE_META` with `wide_px`, `frame_container` and `keys` as the complex examples maker asked, the extras with their meta files, the selection guide's check against the plan); `guide_build.py` (an extra with `contents` takes a line in the local contents; self-test 36 of 36 scenarios, 352 of 352 expectations). The generator now writes Rules 14.142 to 14.144 into `planned_rules` and lists 5 faults, the round 5 files not yet written; `--check` 98 of 98.
- Next: the palette specification's generator (on the data lead's ruling b), the guide check's `selectionGuide` test, S96's kit side (on ruling c).

## Summary

To come.

## Contracts

Round 0 to round 4 contracts stand (C1 to C7, R1-C1 to R1-C7, R2-C1 to R2-C6, R3-2, R3-3, R3-5, R4-2 to R4-5, with each round's changes). Round 5's follow. **SET** means written here for owners to build on; **LANDED** means the code that serves it is in the repository.

### R5-1. The plan file's round 5 rows (SET and LANDED 01:51 UTC)

The plan, `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, gains these rows. Nobody renumbers; an owner who believes an ID should change writes a request with the reason.

**Group 18** in `groups`: `{"group": 18, "title": "Three charts in full", "rules": "14.142 to 14.144", "round": 5}`. The printed title and line are the editor's, in `14-chapter.json`'s `groups` (`"before_rule": "14.142"`), as for every group; the plan's title is a working name.

**Rules 14.142 to 14.144** in `chapter_rules` (they are rules with plates, as 14.1 to 14.14 are, not entries):

| Rule | Owner | Entry file | Correct plate | Failure plate (only where the lesson has a common misreading, R5-4) | Spec | Keys file |
|---|---|---|---|---|---|---|
| 14.142 | complex examples maker | `work/build/guide/entries/14-142.json` | `s-14-s96`: the kit draws `work/build/chart-kit/specs/s96.json`; the generator writes the fragment (R1-C3), never the maker | `s-14-142-failure`: a kit figure through `s-14-142-failure.chart.json` beside `s-14-142-failure.html` (C7), or a static plate | **S96**, form `columns-moving-average`, dataset `fred-payrolls-monthly-change` (S14's frozen file) | none |
| 14.143 | complex examples maker (fragment, drawings); component engineer (the live part's markup contract and the keys file) | `14-143.json` | `s-14-143-correct.html`: Loops B4 and R10 on Rule 18.22's stepper, with its still sequence | `s-14-143-failure.html` | **S97, reserved**: a kit figure inside the plate (`<div data-oa-chart="s-14-s97"></div>`) if the maker draws one; unused otherwise | `s-14-143-correct.keys.json` |
| 14.144 | as 14.143 | `14-144.json` | `s-14-144-correct.html`: R-06, R-30 and R-38 on Rule 15.20's chooser | `s-14-144-failure.html` | **S98, reserved**, as S97 | `s-14-144-correct.keys.json` |

Each row carries `"round": 5`, `"group": 18`, `"failure_required": false` and the subject the brief gives (the maker and the editor set the printed title, the rule's lesson). A reserved spec is checked and logged for Rule 01.9 only when its file exists; it is never a fault when absent.

**The entry file** for each of the three is a rule file in 14-005's shape: `id`, `title`, `rule`, `why`, `related`, `tokens` and `builders` where they apply, `examples` for Rule 01.12's log, and `correct` (and `failure` where drawn) as `{"specimen", "caption", "alt"}` plus any plate key the shell reads (`width_px`, `wide_px`, `readable`, `interactive`, `keys`, `fit_switch`, `breakout`, `height_px`, `surface`, `scale`, `check_exempt`, `frame_container`). For 14.142 the `correct.specimen` is `s-14-s96`, its alt defaults to S96's own `alt`, and its caption is the entry's. A plate that holds a live part sets `"interactive": true` and `"keys": true` (the guide check then walks `<specimen>.keys.json`, R4-5).

**The extras** in a new list, `extras`, read by `phase3_ch14_build.py` (R5-2a below):

| Specimen | Placed | Local contents | Owner and generator | Meta file the generator writes |
|---|---|---|---|---|
| `s-14-selection-guide` | no `after_rule`: between the opener and group 1 | "Choose a chart" | selection guide maker, `work/build/scripts/phase-3/selection_guide_build.py` | `work/build/guide/specimens/s-14-selection-guide.meta.json` |
| `s-14-palette-spec` | after Rule 14.5 | the extra's label (working: "The data palettes, specified"; the editor's word decides) | engineer, `work/build/scripts/phase-3/palette_spec_build.py` | `work/build/guide/specimens/s-14-palette-spec.meta.json` |

**`phase3_ch14_build.py`** defaults to rounds 1 to 5 (as DR-253 and ED4-6 did for rounds 3 and 4), so a run with no flag keeps every round. Until a round 5 file lands, the generator lists it as a fault and keeps its number in `planned_rules` (a citation of it prints unlinked), as before.

### R5-2a. Labeled extras in the local contents (SET and LANDED 01:52 UTC)

- **The chapter file.** `14-data-visualization.json` gains `extras`, written by the generator from the plan's rows: `{"specimen", "label", "caption", "after_rule" (left out for the selection guide), "contents": true}`.
- **Words.** The label and caption come from the editor's `14-chapter.json` `extras` list (`[{"specimen", "label", "caption"}]`) where the editor has written them; else from the meta file's `label` and `caption` (the generator's draft); else the plan's label, and a missing caption is a fault.
- **The meta file** (`<specimen>.meta.json`, beside the fragment, written by that specimen's generator, never by hand): the manifest keys the shell reads (`alt`, required, 15 characters or more; `width_px`, `readable`, `interactive`, `fit_switch`, `breakout`, `keys`, `notes`) and, as a draft, `label` and `caption`. `phase3_ch14_build.py` copies it into chapter 14's manifest, so chapter 14 keeps one manifest.
- **`guide_build.py`.** An extra with `"contents": true` gets a line in the chapter's "In this chapter" list, its label as the words, linked to its figure (`#fig-<specimen>`): the selection guide's line comes before group 1; the palette specification's sits in group 1's list after Rule 14.5. The figure carries `data-oa-contents`. An extra without `contents` prints as today. Opt-in by measure (V25): every chapter 01 to 17 has labeled extras (35 in 11 chapters), and a global change would put 35 new lines in their lists.
- **The shell.** The shell's current-rule marker reads `.rule, .closer`, so the extra's line takes no `aria-current` while a reader is in it; the line is a plain link. Asking the component engineer (Requests) to read `[data-oa-contents]` too.

### R5-2. The selection guide, "Choose a chart" (SET 01:52 UTC; the generator's check LANDED; the guide check's test lands with the maker's first draft)

For the selection guide maker. The data lead's ruling (a) sets the order within a question and how an avoid form shows; the accessibility lead's specification governs names, the skip path and keyboard order; where either differs from this section, theirs governs that point and I change the checks.

1. **Files.** `work/build/scripts/phase-3/selection_guide_build.py` (yours) reads the plan file and `14-chapter.json` (the groups' printed titles) and writes `work/build/guide/specimens/s-14-selection-guide.html` (the fragment) and `s-14-selection-guide.meta.json` (R5-2a). It holds every word; a second run gives an empty `git diff`. A `--check` flag that fails when either file on disk differs is expected, as `token_table_build.py --check` does.
2. **One symbol set, drawn once.** At the top of the fragment, one `<svg class="oac-svg sg-defs" width="0" height="0" aria-hidden="true" focusable="false">` holds `<defs>` with every `<symbol>` and any `<pattern>`. Hide it with a class in the fragment's `<style>` (`position: absolute; width: 0; height: 0; overflow: hidden`), never `display: none`, which drops the patterns a `<use>` reads. **IDs:** a symbol is `s-14-sg-NN`, NN the rule's number after the point (`s-14-sg-15` to `s-14-sg-141`); a pattern or any other id starts `s-14-sg-`. Two forms may share a symbol where their shape is the same; every symbol is used at least once and defined once.
3. **Each picture** is `<svg class="oac-svg sg-pic" viewBox="0 0 W H" width="W" height="H" aria-hidden="true" focusable="false"><use href="#s-14-sg-NN"/></svg>`: no `<title>`, no `<desc>`, no words inside. **Ink** by R1-C1's classes on the shapes inside the symbol (`oac-f-subject`, `oac-f-context`, `oac-f-light-fill`, `oac-f-cat-1` to `oac-f-cat-4`, `oac-f-seq-*`, `oac-f-div-*`, `oac-f-mag-*`, `oac-s-*`, `oac-f-none`, `oac-f-point` for at most one mark a picture); stroke widths as attributes; no `style` attribute, no literal color, no font. **Group 4's hatch:** a shape with `fill="url(#s-14-sg-hatch)"` and **no** `oac-f-*` class (kit.css's `.oac-f-none { fill: none }` beats the attribute and drops the hatch). **Tested in Chromium (01:50 UTC):** classes on shapes inside a `<symbol>` paint through `<use>` with the ground of the stage the `<use>` sits in (subject Charcoal on Newsprint, Newsprint ink on Charcoal, Verdigris on both), the hatch draws in Stone through `<use>` on both grounds from a 0 by 0 defs drawing, and forced colors maps them to system colors (`scratch/symtest/`).
4. **Links.** Each form is one `<a href="#rule-14-NN">` (the entry's own anchor, as the guide builds it), holding its picture and its name in live HTML text: the plan's `form` name, with the tier's word in the link's text (Core, Extended, Reference, Avoid). The link carries `data-tier` (`core`, `extended`, `reference` or `avoid`, the plan's tier's first word, lowercase) and `data-rule="14.NN"`. An avoid form reads as one in words (its link's text holds "avoid") and in its mark (ruling a). One link a form: every one of the plan's 127 `forms` rows once, no other rule, no form twice.
5. **Groups.** The 16 family questions, in the chapter's order (groups 2 to 17), each a list (`<ul role="list">` or `<ol role="list">`) under a line that prints the group's title exactly as `14-chapter.json` prints it, the list's container carrying `data-group="N"`. A form sits under its own family's question only (ruling a); a question's line may itself link to its group (`#data-visualization-g-N` style anchors as the guide prints them) if the accessibility lead asks for it. No heading element anywhere in the fragment (the guide's structure check); no `id` but the symbol set's and those starting `s-14-sg-`.
6. **The stage.** A flowing stage (no `width_px`) at every width the guide gives, 320 px up, with `"interactive": true` in the meta file (it holds 127 links) and `"fit_switch": false`. The fragment's `<style>` is scoped to it by the build; it reads only tokens.
7. **Checks I land** (in two places, so a fault shows at the maker's desk and on the page):
   - `phase3_ch14_build.py` (each run): the fragment parses; every plan form is linked exactly once by `href="#rule-14-NN"`, under the `data-group` of its family; no link to any other target; each link's text holds the plan's form name (curly quotes, spaces and case aside) and its tier's word, and its `data-tier` and `data-rule` match the plan; every `<use>` names a symbol the fragment defines, each symbol defined once and used at least once; every `<svg>` is `aria-hidden="true"`; no `<title>`, `<desc>`, heading, `style` attribute or literal color. Each is a fault, listed by rule number.
   - `guide_check.js` (on the built page, every width it runs, a new test `selectionGuide`): inside `[data-specimen="s-14-selection-guide"]`, each of the plan's 127 rules has exactly one link; every link's target is on the page and is that rule's block (`.rule#rule-14-NN`); each link's accessible name holds the form's name and tier; every `<use>` resolves to a `<symbol>` on the page; every picture is hidden from the accessibility tree; no link or picture runs out of the stage (the guide check's overflow test covers that). Planted faults in the self-test: a form missing, a form twice, a link to a missing anchor, a `<use>` to a missing symbol, a picture left unhidden, a name without its tier.
8. **Weight.** Q5-2 allows about 100 to 150 KB; the build reports the plate's bytes as placed (DR-271), never a stop.

### R5-3. The palette specification (SET for its mechanics 01:52 UTC; its content waits on the data lead's ruling b; the design director reads its layout)

- **Generator:** `work/build/scripts/phase-3/palette_spec_build.py` (mine). `python3 -I .../palette_spec_build.py` writes `work/build/guide/specimens/s-14-palette-spec.html` and `s-14-palette-spec.meta.json`; `--check` exits 1 when either file differs from what `tokens.json` makes now. It reads only `work/build/tokens/tokens.json` (names, values, aliases, descriptions, the release) and its own words, so a token release rewrites the plate and `--check` fails until it is rerun, as chapter 26's token table does.
- **Content** (ruling b decides which): each data palette by job, sequential Verdigris (5 steps), diverging pair B (5 steps), the four group inks (Charcoal, Verdigris, Prussian, Stone always hatched), gray magnitude (4 steps); for each step its token name, its CSS name and its value on each approved ground, with the label ink set on it; contrast of each step against each ground and of its label ink against the step, computed in the script by WCAG 2.2's formula from the token values; a grayscale proof (each step's lightness, so a reader sees the steps stay apart in gray); three color-vision proofs (protanopia, deuteranopia, tritanopia, by a published simulation the script names, Machado, Oliveira and Fernandes 2009 at full severity unless ruling b names another); the grade line's code.
- **Form:** live HTML text (R4-3's rule): tables a reader can search and copy, swatches drawn from `var(--oa-...)` so the page shows what tokens.css holds; the proofs' swatches are drawn as computed values (a simulated color is not a token) inside a figure marked as a proof. No literal color is a token's stand-in.
- **The guide check** compares each swatch's computed color with its token's value on the page (as `tokenTable` does for chapter 26).

### The kit for complex example 1, S96 (SET 01:52 UTC; the kit side LANDS once the data lead's ruling c names the marks)

- **S96 is a new spec,** `work/build/chart-kit/specs/s96.json`, on S14's frozen file `fred-payrolls-monthly-change` (57 months, January 2022 to September 2026, with `status` and the `with_margin` source line variant), form `columns-moving-average`. S14's spec, its file and its entry stay untouched; S14 stays at Rule 14.29's entry and S96 is placed once, at Rule 14.142's correct plate (`s-14-s96`). `where`, `scale`, `labels` and `annotations` are the maker's, under ruling c.
- **What the form gains, opt-in, so S14's drawings stay byte-identical** (proved by snapshot over every S14 drawing before it lands): `labels.point`, a list of months the title names (DR-239's two drops past the margin, October 2025 and February 2026), drawn in the point red with its keyline on Newsprint, one job (`named_fill`, as `ranked-bar` and `line-event-notes` do); and `labels.margin`, `{"value": 122, "key": "words"}`, a band from minus to plus the margin across the plot behind the columns, drawn by `K.parts.band` in the band ink with its edges (the band check), with its own key entry. Ruling c may ask for a different picture of the margin (whiskers on each column, or the band alone on the months past it); I build what it rules.
- **Checks:** `build s96` with the sweep; the source line is the `with_margin` variant; the CSV export is the kit's, checked row for row against the frozen file (DR-254: no page button).

### R5-8. The chapter 11 number map: my part (DONE 01:50 UTC)

- `guide_build.py` line 1669, the status line helper's docstring: "Rules 11.12 and 11.15" now reads "Rules 11.14 and 11.17", applied by the tracker designer's one-function map. No output changes.
- Scanned for `11.10` to `11.16` (not after a digit or point, not before a digit), `s-11-10` to `s-11-16` and `rule-11-10` to `rule-11-16`: `guide_check.js`, `dataviz_check.js`, `guide_charts.py`, `phase3_ch14_build.py`, `data_round0_build.py`, `v7_check.py`, every chart kit file, its forms and tools, `work/build/tests/guide/`: none.
- **Tokens (for the tracker designer):** your three strings in `oa-tokens.src.mjs` landed (the main session's 01:46 snapshot). `tokens_build.mjs --check` then failed as it should; a scratch build differed from `tokens.json` in exactly the three descriptions (11.15 to 11.17 once, 11.16 to 11.18 twice) and `tokens.css` not at all. Rebuilt (01:47): `--check` passes, 545 tokens; parity, rules, the self-test (44 of 44 plants) and the Style Dictionary cross-check pass, and the render test in Chromium passes with 0 failures. Chapter 26's table rerun: `token_table_build.py` changed one line (the point's description, 11.16 to 11.18, twice), `--check` passes. The release stays 6.0.0-gate3.3 (Routine calls).

## Routine calls

- D3-xxx | Rules 14.142 to 14.144 sit in the plan's `chapter_rules` as rules with plates, with `"failure_required": false` | R5-4 makes each a rule with its lesson as its title and a failure plate only where the lesson has a common misreading; DR-240's two plates stay required for 14.1 to 14.14
- D3-xxx | Complex example 1's correct plate is the kit's figure `s-14-s96`, its fragment written by the chapter generator from the plan's spec ID | R1-C3's one placement path: the share and tier gates key on `s-14-sNN`, and S14 keeps its own fragment at Rule 14.29
- D3-xxx | S97 and S98 are reserved in the plan for a kit figure inside Rules 14.143 and 14.144's plates, checked and logged only once a file exists | R5-1 asks for the three rules' spec IDs; examples 2 and 3 run on live components and may hold no kit figure, and a reserved number never moves
- D3-xxx | An extra takes a line in the local contents only with `"contents": true` | Measured reach (V25): 35 labeled extras in chapters 01 to 17 would each gain a line; the brief asks for the two round 5 extras
- D3-xxx | An extra's plate keys come from a meta file its own generator writes (`<specimen>.meta.json`), and its printed label and caption from the editor's `14-chapter.json` where given | Chapter 14 keeps one manifest, written by its generator; generator output holds the words (round 4's generator trap), and the editor owns the chapter's words
- D3-xxx | The selection guide is checked twice: against the plan in the chapter generator, and on the built page in the guide check | A missing or doubled form shows at the maker's desk; a link that lands nowhere shows only on the page
- D3-xxx | The selection guide's symbols are `s-14-sg-NN` by rule number, and a hatched shape carries no fill class | Ids unique on the page (R1-C1's prefix rule); kit.css's `.oac-f-none` beats a `fill` attribute and drops the hatch (tested in Chromium)
- D3-xxx | Token release stays 6.0.0-gate3.3 after R5-8's three description strings | No name, value or CSS line changes (`tokens.css` identical); the descriptions follow the guide's renumbering, as chapter 26's table does
- D3-xxx | `phase3_ch14_build.py` defaults to rounds 1 to 5 | As DR-253 and ED4-6 set rounds 3 and 4: the closing run takes no flag

## Requests

- **Component engineer (shell, low):** `setRule` in `guide-shell.js` reads `.rule, .closer`; please read `[data-oa-contents]` too, so the local contents marks "Choose a chart" and the palette specification's line while a reader is in them. Until then each line is a plain link and the rule before it stays marked.

## Weight

## Tested

## Not tested
