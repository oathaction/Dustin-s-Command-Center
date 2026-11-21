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

## Chapter 16 words

Job 2, from 02:22 UTC. The design director handed chapter 16's words over at 02:21 UTC ("Words ready for the editor"); since then I am the only writer of the word fields in `work/build/scripts/phase-4/phase4_ch16_build.py` (`W`, `R['16.1']` to `R['16.13']`, `EXTRA_KINDS`). Marks, crops, sizes and plate structure are as the design director built them: by script, every plate's tags and styles match its 02:20 build, and the one changed attribute is an alt text in `s-16-3-correct`. Chapter 05 stays as built until Dustin answers on G3-06 (c).

### Routine calls

- D4-xxx | The shot list's How column becomes the guide's own direction for each shot, and the plate's caption says so ("with our direction for the shot"); three lines keep our fifth edition's words whole (rows 8, 10 and 11), and the six the census cut, with the kitchen-table line, are written for this guide, so no line passes for a quote of our fifth edition | The main session asked that the studio's completions carry the Illustrative label or give way to real material. A How line is an instruction to a photographer, the rule's own words, which H03's label (invented people, quotes, places and figures a reader could take for real) does not fit; framed as our direction, none is a completed quote, and "Hands, not faces." no longer prints as a corrective negation (W09)
- D4-xxx | Rows 1 and 2 of the shot list describe the two photographs from the pictures themselves: "From behind the line of people" for the Rotunda (the draft's "From the gallery level" is not where it was taken) and "from behind the residents" at Lake Isabella; row 1 now says "the casket of Rosa Parks", as chapter 01's caption does | Checked against both 1,200 px files by eye
- D4-xxx | The video plates' figures (Rules 16.10 to 16.13) carry chart S04's own source line in each correct caption, read from `work/build/chart-kit/specs/s04.json` by the generator (`S04_SOURCE`), and the chapter's source list prints the same line | House rule H04: every public policy statistic carries its source, period and qualification; reading it from the spec keeps the two lines one
- D4-xxx | Rule 16.12's Why names the page and its date: "The W3C’s page “Understanding Success Criterion 1.2.5: Audio Description (Prerecorded)”, retrieved November 21, 2026, notes that …", with the note quoted word for word from the main session's read (research lead's notes, addendum of about 02:00 UTC) | The main session's second point
- D4-xxx | Rule 16.6's failure caption credits "Photograph: Dustin Cathcart, Oath & Action.", Rule 16.5's form for our own photographs, in place of "Photograph: Oath & Action." | The plate then shows one fault, the missing permission, and agrees with Rule 16.5's credit forms; DR-301 makes Dustin the maker at public events. Rule 16.9's failure keeps "Photograph: Oath & Action.", since a photograph's credit on a generated picture is that plate's fault
- D4-xxx | Rule 16.5's credit forms confirmed as the plan drafted them: "Photograph: Dustin Cathcart, Oath & Action." for ours and "Photograph: [name] for Oath & Action." for a photographer we hire | Both follow the form the two federal credits take, the maker and then the organization
- D4-xxx | Rule 16.3's set and Rule 16.7's pair print each photograph's own caption with its credit (chapter 01's, word for word) in place of a sentence about the caption | Rule 16.5 asks every photograph to run with its caption and credit, and the shortened Rotunda caption dropped "the civil rights pioneer"
- D4-xxx | Rule 16.4's headline takes the agency's verb: "At a public meeting in 2014, the Army Corps discussed the dam project’s proposed land purchases with Lake Isabella residents." | The record says Zianno "discusses impacted properties and proposed real estate actions with local residents"; "walked … through" claimed more (H08). Its length stays within three characters of the draft, so the failure plate's measured box still fits it
- D4-xxx | Studio words leave the reader's text: "Master Brief section 16", "Gate 1’s recommendation S10", "Gate 3’s answer P4-3", "Gate 1, Y6", "sidecars" and the bare codes pho-01 to pho-04r. The Basis lines name our founder and editor's approvals by date (October 28, 2026 for black and white and the hand-drawn treatment; November 21, 2026 for generated images and the two video forms), and the rights record names what pho-04 and pho-04r refer to (H11) | No other chapter prints "Master Brief"; house rule H11
- D4-xxx | The hand-drawn spot illustration row keeps "at 96 px and larger, drawn by a person" and drops "in Charcoal on Newsprint" | The approved treatments map (Gate 1, October 28, 2026) gives 96 px and up; I found no approval of the colors, and the row cites that approval
- D4-xxx | A generated picture "appears only with its label" in the intro and the group line, where the draft said it "serves only as a labeled illustration" | Rule 16.9 also allows the setting around our work in a mockup; the summary said less than the rule
- D4-xxx | Rule 16.2 leaves off "every other effect" where the draft said "filters" | The same rule sets <code>filter: grayscale(1)</code>, so "filters off" contradicted it
- D4-xxx | Rule 16.8's padding spec reads "24 px; 16 px in a frame 320 px wide or narrower" | The plates draw the 320 px and 240 px frames at 16 px, so the spec now says what they show
- D4-xxx | Rule 16.13's Controls spec gives 44 px to the Play button and names every control by its words | The plate's two links are text links, not 44 px controls
- D4-xxx | Rule 16.10's name plate spec places it "in the lower third, clear of each platform’s buttons and the captions" | The plan's hand-over to chapter 23 says so; the draft put it inside the caption-safe area the captions use
- D4-xxx | Terms defined at first use: rights ledger (16.6), mockup (16.9), caption file, WebVTT and SubRip (16.11), caption-safe area (16.11), audio description and a described version (16.12); L8 named as "L8, the monogram" (16.10, as Rule 12.3 does) | House rules H02 and H11
- D4-xxx | Placeholder frames and rule-text examples (the jar of brown tap water, the resident at a microphone, the phone on a kitchen table) carry no Illustrative label | Each announces itself as a shot to make or a prompt, and none claims a real event; the label stays on every invented caption, quote and name (Rules 16.5, 16.6, 16.9 failures, and the four video plates)

### Done

`work/build/scripts/phase-4/phase4_ch16_build.py`, its WORDS section rewritten field by field (keys and tuple shapes unchanged), its module docstring and the shot list plate's manifest note made accurate. Run under the lock at 02:34 UTC, it rewrote `work/build/guide/chapters/16-photography.json` (50,016 to 54,238 bytes), `manifest-photography.json` (alts and one note) and eleven plates, in words only:

| Plate | Bytes before | After |
|---|---|---|
| `s-16-1-correct` | 5,339 | 5,437 |
| `s-16-3-correct` | 3,288 | 3,499 |
| `s-16-4-correct` | 2,669 | 2,669 |
| `s-16-4-failure` | 2,852 | 2,852 |
| `s-16-5-correct` | 2,993 | 3,030 |
| `s-16-6-correct` | 4,117 | 4,172 |
| `s-16-6-failure` | 3,365 | 3,382 |
| `s-16-7-correct` | 2,600 | 2,627 |
| `s-16-9-correct` | 3,388 | 3,402 |
| `s-16-10-correct` | 3,964 | 3,933 |
| `s-16-picture-kinds` | 3,474 | 3,490 |

The other seventeen plates are byte for byte as before. All 28 plates as written: 82,739 bytes. Chapter 16 on the strict build: 218,566 bytes against its 300,000 (73 percent), up from 213,681; most of the rise is chart S04's source line in four captions.

### Requests

- For the main session to relay: `s16_7_failure()` in `phase4_ch16_build.py` shows the tight Rotunda crop with no caption, while every other photograph plate prints its caption and credit (Rule 16.5). Add `{cap(W["cap_rotunda"])}` after the alt line, as `s16_7_correct()` does. A layout change, so I have not made it.

### Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| ED10-4 | Editor, chat 10 | Rule 16.7's failure plate, `s16_7_failure()` in `phase4_ch16_build.py` | The photograph runs with no caption or credit, a second fault beside the alt text the plate teaches | The request above | A layout change; the brief keeps plate structure with its builder | Open, requested |

### Tested

- `phase4_ch16_build.py --check` and then the write, under the lock (02:33 and 02:34 UTC): 13 rules, 28 specimens, 82,739 bytes, 18 photograph uses; the chapter check and every specimen check passed (no dash, no straight quote, no listed filler, no literal color, no heading element).
- The strict build to my scratch under the lock (02:34 UTC): exit 0, 0 warnings, 12,238,726 bytes, 382 rules, 707 specimens; chapter 16 at 218,566 of 300,000.
- By script, before against after: every plate keeps its tags and styles, the one changed attribute being an alt in `s-16-3-correct`; the manifest keeps its 28 keys, with only alts and one note changed.
- Word search of the strict build's chapter 16: Rule 16.12's Why prints the page's name, "retrieved November 21, 2026" and the W3C's note word for word, once; the new How lines print; chart S04's source line prints five times (four captions and the sources); "Photograph: Dustin Cathcart, Oath & Action." prints twice (Rule 16.5's spec and Rule 16.6's failure). The old words print 0 times: "residents on the benches", "Here is what its survey found", "The register, the window, the street outside", "Hands, not faces", "From the gallery level", "walked Lake Isabella residents", "Gate 1", "Master Brief", "sidecar", "pho-01", "P4-3". Eleven Illustrative labels in the chapter.
- A script read of all 436 strings in the chapter and its plates (9,530 words): 0 em or en dashes, 0 listed fillers, hedges or corporate verbs, 0 "not … but" or ", not" turns, 0 straight quotes, 0 studio words. I recast the runs it flagged (two sentences in a row on one opener, three sentences of near-equal length) and read every field by hand against chapter 02's rules.
- Facts checked: every figure in the video plates against S04's spec (47.7 percent, down 3.7 points, near 75 percent for 65 and over, the gap from 23 to 27 points, and "answers to a survey, which run higher than counted ballots"); the SPJ quotes and the YouTube quote against the research lead's section D and B; the agency's words for Rule 16.4's headline and 16.5's failure caption against the photograph's sidecar; the two photographs' contents and crops by eye on the 1,200 px files; the 96 px hand-drawn treatment against the Gate 1 board.

### Not tested

- Chapter 16 in a browser at any width: I did not look at how the new words wrap on the plates, including Rule 16.4's headline over the photograph and the longer captions under the video plates.
- The guide check (axe, contrast on pixels, the red test) and the four-width check, which the main session runs.
- Read aloud by a person.
