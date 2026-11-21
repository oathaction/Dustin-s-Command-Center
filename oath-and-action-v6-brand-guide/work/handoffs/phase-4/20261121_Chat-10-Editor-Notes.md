# Chat 10, editor's notes

Editor (oa-editor), chat 10 of Phase 4, November 21, 2026. Brief: `work/handoffs/phase-4/20261121_Chat-10-Brief.md`, sections 1 to 4 and 8. Job 1 is Gate 3's item 6 (G3-06), the three word changes as `work/ledger/20261120_Gate-3-Report.md` section 10 prints them. Job 2, chapter 16's words, waits for the design director's hand-over.

## For Dustin

Read at 01:40 UTC, before the build, as G3-06 asks. Both of (c)'s sentences are built as approved. These are my concerns and the words I propose in their place; nothing below is made.

**(c), Rule 05.5's new sentence.** Approved: "The atlas’s red target takes none either: the atlas draws it as a red ring and arrowhead, and each plate names its target in words beside the drawing (Rule 15.11)."

1. It contradicts Rule 12.5, the rule that names the atlas’s red target. Rule 12.5 says "On Newsprint a red connection carries a 1 px Charcoal edge", and its specification reads "1 px Charcoal on each side of a red connection, as a 6 px case under the 4 px line". Every atlas plate draws that edge (Rules 15.11, 15.12, 15.16, 15.20 and 14.144; the `.ak-case` stroke, 6 px in ink, in `phase3_ch15_build.py` and `phase3_ch14_complex_build.py`). Board 3's reply 11 took off only the keyline inside a variable's red outline and the arrowhead's edge. So the red connections keep a Charcoal edge, and only a target variable's red outline and the red arrowheads go without one. Read strictly, Rule 05.3 defines a keyline as an edge drawn inside the mark and Rule 12.5's edge sits outside the line, but a reader who sees a Charcoal edge on every red line will read "takes none" as wrong.
2. "A red ring" is a new word for a thing the guide already names. Rules 12.5 and 15.11 call it "the outline of each variable it targets", and the atlas draws a variable as a pill, a rounded box. Chapter 02's house rule H02 asks for the same term after first use.
3. The clause after the colon describes the drawing, and only its second half gives the reason the mark may go without an edge: the words beside the drawing name each target, the accessibility lead's ruling at board 3 (D3-2301). "Names its target" is singular, while a reform has several targets and Rule 15.11 lists each one.
4. Smaller: it repeats the frame of the sentence before it ("The error bar takes none, since …"), which chapter 02's W13 asks writers to recast.

Proposed in its place, two sentences:

> On the atlas’s red target, only the red connections carry a 1 px Charcoal edge on each side (Rule 12.5). Every plate names each target in words beside the drawing (Rule 15.11), so the red outline of a target variable and each red arrowhead go without an edge.

If you keep the approved sentence, the smallest repair is "a red outline and arrowhead" for "a red ring and arrowhead", which fixes point 2 and leaves point 1.

**(c), Rule 05.3's reason.** Approved: "On Newsprint it measures 2.96 to 1, so a working red mark there takes a keyline, a 1 px Charcoal edge drawn inside the mark, apart from the two marks Rule 05.5 names."

1. Read aloud, "apart from the two marks" lands right after "drawn inside the mark", so a listener can hear it as where the edge is drawn before hearing it as the exception.
2. It sends the reader to Rule 05.5 to learn which two marks, where naming them takes a few words (the spirit of H11), and under point 1 above the second "mark" is only part of the atlas’s target.

Proposed in its place, with the ratio still computed from the tokens:

> On Newsprint it measures 2.96 to 1, so a working red mark there takes a keyline, a 1 px Charcoal edge drawn inside the mark. Rule 05.5 lets the error bar, and the red outlines and arrowheads of the atlas’s target, go without one.

(a) and (b) read clean against chapter 02's rules. (b) matches Rule 18.24, which sets a chip's type and code "in the label style on a hairline edge", so a chip's ID is the one data label that takes another style.

## Routine calls

- D4-xxx | (c)'s two sentences are built word for word as approved, with my concerns and proposed words under "For Dustin" | G3-06 approves them as printed; brief section 8 says build them and report the fault
- D4-xxx | Each generator change carries a one-line `# G3-06 (a)`, `(b)` or `(c)` comment beside the words it changed | The next maker can trace each phrase to Gate 3's item 6
- D4-xxx | The measurement record keeps its new render line (Chromium 157.0.8103.78, 01:41:10 UTC) | `stage_a_systems_build.py final` writes it; every rendered figure (55 of 55) matches the committed record, so the render line is all that moved, as in round 5's rebuild
- D4-xxx | `phase3_ch14_build.py` runs right after `phase3_ch14_rules_build.py`, inside the same lock | Chapter 14's file is assembled from the entries; the chat 9 apply pass ran it the same way (A9), and `--check` stays at 99 of 99 for the engineer

## Done

Gate 3's item 6 (G3-06), word for word as the Gate 3 report's section 10 prints it, with the typographer's apostrophes in "text’s" and "chip’s" (U+2019). Built 01:41 UTC.

- (a) `work/build/scripts/phase-3/phase3_ch14_rules_build.py`, `rule_14_6`: the fifth paragraph's "takes Charcoal at any size" now reads "takes the text’s ink at any size"; the spec "A named area, or past 5 percent of the drawing" now opens "The text’s ink, with the label (Rule 05.1)". Outputs: `work/build/guide/entries/14-006.json` and, through `phase3_ch14_build.py`, `work/build/guide/chapters/14-data-visualization.json`, each with exactly these two values changed.
- (b) `work/build/scripts/phase-2/stage_a_systems_ch06.py`, Rule 06.3's "Data label" spec: "Inter 600, 13 px, line height 1.3, tabular figures, except a chip’s ID (Rule 18.24)". Output: `work/build/guide/chapters/06-type.json`, that value alone.
- (c) `work/build/scripts/phase-2/stage_a_systems_ch05.py`: Rule 05.5's new sentence after the error bar's, and Rule 05.3's reason ending "apart from the two marks Rule 05.5 names." Rule 05.3's ratio stays computed from the tokens (`{red_n}`, 2.96). Output: `work/build/guide/chapters/05-color.json`, those two values alone. Rule 05.7 keeps its words.
- The stage A rebuild ran in its three steps (probe, capture, final) and also rewrote `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json`, whose render line alone moved: browser version and date. Chapter 07, the 56 specimens and `manifest-systems.json` came out byte for byte as committed.
- Bytes on the strict build: chapter 05, 240,636 to 240,871; chapter 06, 148,041 to 148,076; chapter 14, 2,151,557 to 2,151,573; the page, 12,210,634 to 12,210,920 (+286). No plate changed. These chapters have no Phase 4 allocation.

`git diff --stat` at 01:47 UTC shows these eight files and no others: the three generators, the four outputs named above and the measurement record. My scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/127ebfa4-7663-587b-a8ae-9ad439f7784c/scratchpad/c10/editor/` (stage A probes and capture in `stageA-base/` and `stageA/`, the strict build `guide.html` with its report and log, and `page-diff.txt`).

## Requests

None.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| ED10-1 | Editor, chat 10, reading G3-06 (c) | Rule 05.5's new sentence and Rule 05.3's reason; `stage_a_systems_ch05.py`, output `05-color.json` | The sentence says the atlas’s red target "takes none", while Rule 12.5 gives every red connection a 1 px Charcoal edge on each side and every atlas plate draws it; "a red ring" renames what Rules 12.5 and 15.11 call a variable's outline; 05.3's "apart from the two marks" reads as where the edge sits | The words under "For Dustin" above | G3-06 approves the sentences as printed; the brief says build them and report | Open, for Dustin |
| ED10-2 | Editor, chat 10 | Rule 05.5's specifications; `stage_a_systems_ch05.py`, output `05-color.json` | The specs give the error bar's exception its own row ("4 px Pillar Red with no keyline; …") and give the atlas’s red target none, so the rule's text names two exceptions and its specs one | A row "Atlas red target": "Red connections on a 1 px Charcoal edge each side (Rule 12.5); a target variable’s red outline and its arrowheads with no keyline; the words beside the drawing name each target (Rule 15.11)" | G3-06 names the sentence only; approved work changes only where an approved answer names the change | Open |
| ED10-3 | Editor, chat 10 | Rule 05.3's specification "Keyline on a red mark on Newsprint"; `stage_a_systems_ch05.py`, output `05-color.json` | The spec states the keyline with no exception, while the rule's reason now points to the marks Rule 05.5 lets go without one | Add "except the marks Rule 05.5 names" to its value | Outside G3-06's words | Open |

## Tested

- The three generators parse, and each ran under the lock and exited 0: `stage_a_systems_build.py probe` (before and after the edits), `stage_a_systems_capture.js` (Chromium, load 0.25 at 01:40 UTC, one other owner holding a browser), `stage_a_systems_build.py final` (its house-rule check on every word of chapters 05 to 07 passed), `phase3_ch14_rules_build.py` (its editor's checks passed: no em dash, no listed filler or corporate word, the plan's numbers), then `phase3_ch14_build.py`, 0 faults.
- The probe pages before and after the edits are byte for byte the same (`probes.json`, `measure.html` and both phone pages), so one capture served the rebuild; its 55 results equal the committed record's rendered figures.
- `phase3_ch14_build.py --check`: 99 of 99 current before and after.
- The strict build to my scratch (01:41 UTC): exit 0, 0 warnings, 12,210,920 bytes, 369 rules, 679 specimens.
- Against the main session's 00:43 strict build of the committed tree (`scratchpad/c10/strict/guide.html`), tag by tag: seven differences, the six word changes and the build's time line, nothing else.
- Word search of the strict build's text: each new phrase prints once ("takes the text’s ink at any size"; "The text’s ink, with the label (Rule 05.1)"; "tabular figures, except a chip’s ID (Rule 18.24)"; Rule 05.5's sentence; Rule 05.3's reason), and the old ones print 0 times ("takes Charcoal at any size"; "Charcoal, with the label (Rule 05.1)"; the data label spec with nothing after "tabular figures"). "drawn inside the mark (Rule 05.5)." still prints once, in the palette plate's line on a chart's one red (`palette_spec_build.py`), a different sentence about a chart point, which keeps its keyline (Rule 05.7).
- Rule 05.5's "Rule 15.11" and Rule 05.3's "Rule 05.5" print as links in the built page.
- Script check of the six new strings: no em or en dash, none of the listed fillers, hedges or corporate verbs, curly apostrophes only. In Rule 14.6, the "Charcoal" left after the change names a ground ("on Charcoal") or the keyline's ink.
- Against the chapters: Rule 12.5's text and specs, and the red-target styles in `phase3_ch15_build.py` and `phase3_ch14_complex_build.py`, for (c)'s first concern; Rule 18.24 for (b).

## Not tested

- The changed rules in a browser at any width. I read their words in the built page by script and did not look at their layout.
- The four-width guide check and the quick check with photographs, which the main session runs at the close.
- Read aloud by a person: my read of (c) for the ear is my own.
