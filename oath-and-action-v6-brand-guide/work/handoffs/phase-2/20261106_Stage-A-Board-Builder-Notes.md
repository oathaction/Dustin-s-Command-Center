# Stage board A builder notes

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the engineer for the creative director and the main session. This file sets the two inputs the board builder reads, so each of you can fill your part exactly. The builder fails with a plain message when a field is missing or wrong, so a failed run tells you what to fix.

## 1. What the builder does

```
python3 -I work/build/scripts/phase-2/stage_a_board_build.py
```

On every run it opens the chapters page, `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, as it stands at that moment, and captures what the board shows. Rerun it after the last build of the chapters page and the board follows. It runs in about 45 seconds.

It reads two files from `work/boards/phase-2/stage-a/board-a/`:

| File | Written by | Holds |
|---|---|---|
| `20261106_Stage-A-Board-Content.json` | the creative director | the title and deck, the verdict, the six rubric scores, a note and two or three views for each chapter, the letter spacing choice, notes on the proofs, what still needs work, risks and the decisions |
| `20261106_Stage-A-Board-Studio-Record.json` | the main session | the chapters page's published address, what was asked, the process, the checks run, what was not tested and the change log |

It writes:

| Output | Where |
|---|---|
| The board | `work/boards/20261106_Stage-A-Foundations-Board.html`, with images linked by relative path |
| Captures, about 11 MB of JPEG, and the facts read from the page | `work/boards/phase-2/stage-a/board-a/captures/` |
| The publish copy, its 51 images and a publish map | `/tmp/claude-0/-home-user-Dustin-s-Command-Center/d4b0fb53-ac2c-5992-bcfd-deda558d4457/scratchpad/publish-board-a/`, with the page, `captures/` and `files.json` |

A helper, `work/build/scripts/phase-2/stage_a_board_capture.js`, does the browser work. The builder runs it; nobody runs it by hand.

Options: `--strict` exits 1 on any warning. `--no-capture` reuses the last captures, for layout work only, and the board then says so. `--content`, `--record`, `--page`, `--out`, `--captures` and `--publish` point at other files, as the sample test below does.

## 2. What the board shows, and where each part comes from

| Section | From the content | Read from the chapters page when the builder runs |
|---|---|---|
| Cover and "What you are asked" | `title`, `deck`, `ask`, `sample_reply` | |
| 01 Verdict | `verdict`, `scores`, each chapter's `scores` | |
| 02 Chapters | each chapter's `note` and `views` | the chapter title, its instruction line, its rule count and every rule title; each view captured at 1,440 and 390 px at device scale 2 and shown at its CSS size |
| 03 Letter spacing | `tracking` | the chapter title and rule title it names, and the letter spacing the page renders |
| 04 Wordmark proofs | `proofs` | the appendix's instruction line and two intro paragraphs, and each proof's title, note, plate label, size line, caption and alt text; each plate captured at true size |
| 05 Still to do | `needs_work`, `risks` | the words of each linked rule |
| 06 Decisions | `decisions` | the title of each rule a decision touches |
| 07 Studio record | | the builder adds its own checks to the record's |

A view at 1,440 px is the chapter column under the masthead, from the page's own anchor jump, with the rail left out: 1,136 by 835 px. A view at 390 px is the whole phone screen under the masthead: 390 by 755 px. Each view's title links to its anchor in the live chapters page. The decisions section ends in a reply box on Prussian, the board's one dark panel. It gathers the answers Dustin marks on each card into lines such as "A1: as recommended (a)." that he can copy into the chat. His marks stay in his own browser.

## 3. The content file, for the creative director

Write plain strings. Two marks work inside any text: `**bold**` and `` `code` ``. Write "Rule 05.3" and the board links it to the live rule; write "A3" and it links to that decision's card. Straight quotes become curly ones and a hyphen before a figure becomes the true minus sign, so type them plainly. Every word follows chapter 02's writing section. The builder fails on an em dash anywhere and on a locked line quoted inexactly, and warns on the words W17, W18 and W20 list.

```json
{
 "title": "Chapters 01 to 08, for your review",
 "deck": "One or two sentences under the title.",
 "ask": ["optional: what Dustin is asked, one line each"],
 "sample_reply": "optional: A1 to A12: as recommended.",
 "verdict": {
  "headline": "The verdict in one sentence.",
  "text": ["optional: one or two short paragraphs"]
 },
 "scores": [
  {"criterion": "Craft", "score": 4, "line": "The reason, in one line."},
  {"criterion": "Clarity", "score": 4, "line": "..."},
  {"criterion": "Brand fidelity", "score": 5, "line": "..."},
  {"criterion": "Usefulness", "score": 4, "line": "..."},
  {"criterion": "Evidence honesty", "score": 4, "line": "..."},
  {"criterion": "Accessibility", "score": 4, "line": "..."}
 ],
 "chapters": {
  "01": {"note": "One to three sentences.", "views": ["opening", "01.2", "01.21"], "scores": [4, 4, 5, 4, 4, 4]},
  "02": {"note": "...", "views": ["opening", "02.10"]},
  "03": {"...": "..."}, "04": {}, "05": {}, "06": {}, "07": {}, "08": {}
 },
 "tracking": {"chapter": "04", "rule": "05.3", "note": "optional"},
 "proofs": {"note": "optional", "notes": {"proofs-avatar": "optional note on one proof"}},
 "needs_work": ["a string", {"where": "06.4", "text": "an item tied to a rule"}],
 "risks": ["a string", {"where": "proofs-letterhead", "text": "a risk tied to a place"}],
 "decisions": [
  {
   "question": "Which wordmark width do we keep?",
   "context": "optional: a sentence or two, or a list of paragraphs",
   "options": [{"text": "Keep today's width", "short": "today's width"}, "Adopt the condensed width"],
   "recommended": "a",
   "recommendation": "optional: the recommendation in your words",
   "why": "The reason for it.",
   "touches": ["proofs-the-marks-at-a-glance", "03.1", "03.6"],
   "source": "optional: where the question came from, such as a decision log entry named in words"
  }
 ]
}
```

| Field | Required | Rule |
|---|---|---|
| `title` | no | The board's h1. Short, since it sets in the title style at up to 110 px. Default "Chapters 01 to 08, for your review" |
| `deck` | yes | One or two sentences |
| `ask` | no | A list of lines for "What you are asked". The default asks Dustin to read the verdict and the views, compare the proofs, and answer A1 to the last decision |
| `sample_reply` | no | The short reply shown in the ask box and in the reply box until Dustin marks an answer. Default "A1 to An: as recommended." |
| `verdict.headline` | yes | One sentence, set large |
| `verdict.text` | no | A string or a list of paragraphs |
| `scores` | yes | Exactly six entries in rubric order, Master Brief section 6: Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility. `score` is a whole number from 1 to 5. `line` is the reason in one line. The board counts how many reach the ship line of 4 and says so |
| `chapters` | yes | One entry each for "01" to "08", no others |
| `chapters.NN.note` | yes | A string or a list of paragraphs, set in Lora Italic and credited "Creative director" |
| `chapters.NN.views` | yes | Two or three views. Each is "opening", a rule ID such as "05.3", or an anchor in that chapter such as "group-02-1" or "color-specs". To name a view yourself, write `{"anchor": "05.3", "label": "your words"}`. A view must sit inside its own chapter |
| `chapters.NN.scores` | no | Six whole numbers from 1 to 5 in rubric order. When any chapter has them, the verdict adds a table by chapter and boxes each score under 4 |
| `tracking.chapter` | no | The chapter whose title shows the section style. Default "04", the longest title |
| `tracking.rule` | no | The rule whose title shows the H3 style. Default "05.3". The tagline always shows the title style |
| `tracking.note` | no | Your note on the change |
| `proofs.note` | no | Your reading of the proofs, under the appendix's own words |
| `proofs.notes` | no | Notes on single proofs, keyed by the proof's anchor (section 5) |
| `needs_work`, `risks` | yes | Lists, which may be empty. An item is a string, or `{"where": ..., "text": ...}` where `where` is a rule ID, a chapter number or an anchor (it prints as a short linked label), or plain words such as "Board B" |
| `decisions` | yes | At least one. They print in order as A1, A2 and on. If you write an `id`, it must match its place |
| `decisions[].question` | yes | The question, set as the card's heading |
| `decisions[].options` | yes | Two to eight. A string, or `{"text": ..., "short": ...}`; `short` is what the reply box writes when Dustin picks it. Options print as (a), (b) and on |
| `decisions[].recommended` | yes | The recommended option, as its letter ("b") or its number (2). It carries a Recommended label |
| `decisions[].recommendation` | no | The recommendation in your words. Without it the card repeats the recommended option |
| `decisions[].why` | yes | The reason |
| `decisions[].touches` | yes | The rules it touches, as rule IDs or anchors. Each must exist on the chapters page. An empty list warns |
| `decisions[].source` | no | A short source line under the card |

The decisions the handoff lists for board A (`work/handoffs/phase-2/20261106_Next-Session-Handoff_V4.md`, section 2D) are the starting set, less those Dustin has already answered (DR-95 to DR-103).

## 4. The studio record, for the main session

```json
{
 "chapters_page": {"url": "", "placeholder": "https://..."},
 "asked": ["What Dustin asked for this board, one line each."],
 "process": [
  {"stage": "Makers", "text": "..."},
  {"stage": "Red team", "text": "..."},
  {"stage": "Fix pass", "text": ["Round one ...", "Round two ..."]},
  {"stage": "Creative director", "text": "..."}
 ],
 "red_team": [{"lens": "Brand, evidence and nonpartisanship", "score": 2, "must_fix": 6, "should_fix": 12}],
 "checks": [
  {"name": "Guide check at four widths", "command": "node work/build/scripts/phase-2/guide_check.js ...", "result": "4 widths, 0 failures, 17 listed exemptions.", "pass": true}
 ],
 "not_tested": ["..."],
 "changelog": {"created": ["work/..."], "modified": ["work/..."]}
}
```

| Field | Required | Rule |
|---|---|---|
| `chapters_page.url` | no | The chapters page's published address. Every view, rule and proof link on the board is this address plus `#anchor` |
| `chapters_page.placeholder` | when `url` is empty | The address links use until the page is published. While it stands in, the board says so under the chapters intro |
| `asked` | yes | At least one line |
| `process` | yes | A list of stages, each with `stage` and `text` (a string or a list of paragraphs). The stage names must include a maker stage, a red team stage, a fix pass stage and a creative director stage; more may follow |
| `red_team` | no | One row per lens, shown as a table under the process |
| `checks` | yes | At least one. `command` and `pass` are optional; `pass` true or false prints "Pass." or "Fail." before the result |
| `not_tested` | yes | At least one line |
| `changelog` | yes | `created` and `modified`, each a list of repository paths (relative to `oath-and-action-v6-brand-guide/`) |

Both files may carry `"sample": true`. The board then opens with a band that says it was built from sample files.

## 5. Anchors you can name

The builder reads every anchor on the chapters page when it runs, and a failed name stops the build with the anchor it could not find. These forms work in `views`, `touches` and `where`:

- A rule: "05.3", "Rule 05.3" or "rule-05-3".
- A chapter: its number, "05", or its anchor: `purpose`, `voice`, `identity`, `ampersand`, `color`, `type`, `layout`, `signal-grid`.
- A proof: `proofs-the-marks-at-a-glance`, `proofs-masthead-on-the-site`, `proofs-masthead-in-email`, `proofs-avatar`, `proofs-social-card`, `proofs-letterhead`, `proofs-minimum-sizes-at-both-widths`, or the appendix as a whole, `proofs`.
- A rule group, such as `group-02-1`; a chapter closer, such as `color-specs`, `color-related` or `color-builders`; a plate, such as `fig-s-05-1-correct`.

The facts file in the captures folder, `20261106_Board-A-Capture-Facts.json`, lists every anchor with the words the board prints for it.

## 6. Running it for the real board

1. The creative director writes the content file; the main session writes the record.
2. Run the final build of the chapters page, then publish it privately and put its address in `chapters_page.url`. Until then, set `placeholder`.
3. Run `python3 -I work/build/scripts/phase-2/stage_a_board_build.py --strict`.
4. Run `node work/build/scripts/phase-2/dataviz_check.js work/boards/20261106_Stage-A-Foundations-Board.html --board`. If `work/build/node_modules` lacks axe-core, install both packages together first: `cd work/build && npm install --no-save axe-core@4.10.2 style-dictionary@5.8.0`.
5. Add that check's result to the record's `checks` and rebuild, so the board reports it.
6. Publish `publish-board-a/20261106_Stage-A-Foundations-Board.html` with `files` set from `publish-board-a/files.json` (51 images, about 11 MB) and the icon "book". Read the page and every image before publishing, as the handoff asks.

## 7. Routine calls, proposed for the decision log

| # | Decision | Reason |
|---|---|---|
| D2-xxx | A 1,440 px view is the chapter column under the masthead, from the rail's edge to 24 px past the local contents, 1,136 by 835 px; a 390 px view is the whole phone screen under the masthead | At true size the column fits the board's 1,312 px measure with no sideways scroll, and the phone screen keeps the plates' full-width mats |
| D2-xxx | Views are captured after the page's own anchor jump, with the focus ring the shell gives the heading cleared | The capture shows what a reader sees on landing, without a ring no reader would see |
| D2-xxx | Each proof plate is captured as its stage alone, at true size, in a window wide enough for the widest plate, with the page's chrome hidden | The plate is the specimen; the appendix's notes and caption print as live text beside it |
| D2-xxx | Captures are JPEG at quality 80, at device scale 2 | About 11 MB for 51 images, sharp on a 2x screen; a 4 MB chapters page and a 16 MB publish limit leave no room to inline them |
| D2-xxx | The board inlines `tokens.css` and sets every color, size, space and type style from it, with the title, section, H3 and H4 styles at the tracking Dustin approved | The board then looks like the guide and moves with the tokens |
| D2-xxx | The letter spacing pairs set live text in the token styles, old above new, joined by the hinge divider in Charcoal, each pair as wide as its widest line | DR-95 asks for actual size; the divider follows DR-96 and Board 5's before and after |
| D2-xxx | Decisions sit on White cards with an answer column; the reply box is the board's one Prussian panel | One dark panel per section (Rule 05.1); the answers gather in one place Dustin can copy |
| D2-xxx | The reply box saves marks in the viewer's browser only, keyed to the decisions' text | A changed set of decisions never loads stale answers, and no answer leaves Dustin's browser |
| D2-xxx | The publish copy sets `lang="en"` by script and keeps no attribute on its body | The publish skeleton's elements carry no attributes (as D2-243 found) |

## 8. Tested

Every item below ran against a sample pair written into the scratchpad, `/tmp/claude-0/-home-user-Dustin-s-Command-Center/d4b0fb53-ac2c-5992-bcfd-deda558d4457/scratchpad/board-a-sample/`, with the board, captures and publish copy built there too. Nothing from the sample went into the repository.

- A full build with fresh captures and `--strict`: 44 views (22 at each width) and 7 plates captured from the chapters page as built at 10:14 p.m. UTC on November 6, 0 errors, 0 warnings, about 45 seconds.
- `node work/build/scripts/phase-2/dataviz_check.js <sample board> --board`: PASS, 0 failures at 1,440, 390 and 360 px. Axe-core 4.10.2 found no violations; no sideways scroll; smallest text 13 px; no red mark; 40 focus stops, each with a visible ring; Inter, Inter Tight and Lora loaded.
- I looked at the sample board with Playwright at 1,440 and 390 px, section by section, and fixed what read badly: the masthead rule, the view captions, the hinge width, the decision cards' answer column, the checks table on phones and the spacing of second-column headings on phones.
- The reply box in Chromium: marking (a) on A1 and (b) on A3, with notes on A3 and A5, gave three reply lines; Copy put them on the clipboard; a reload restored them; no page errors.
- The publish copy, wrapped in a document skeleton: all 51 images load from `captures/` at 1,440 and 390 px, the page sets `lang="en"`, no page errors.
- Inputs that should fail, each with its message: an em dash in the deck, the tagline quoted without its period, a view on a rule that does not exist, a view from another chapter, a decision touching a rule that does not exist, a recommended option past the last, five scores, one view, a decision numbered out of order, and a record with no fix pass stage.
- The capture's letter spacing on the chapters page at 1,440 px: −3 percent on the tagline, −2.5 percent on chapter titles, −1 percent on rule titles, matching DR-95 and `tokens.css`.

## 9. Not tested

- The real content and record, which do not exist yet, and so the real board's length and decisions.
- The published board on claude.ai: whether its links into the chapters page land on their anchors there, and whether Copy reaches the clipboard inside the published frame. The button falls back to selecting the text.
- Safari, Firefox, real phones and screen readers.
- A rerun against the chapters page after the fix pass's final build; the sample used the build of 10:14 p.m. UTC.

## 10. Change log

Created:
- `work/build/scripts/phase-2/stage_a_board_build.py`
- `work/build/scripts/phase-2/stage_a_board_capture.js`
- `work/handoffs/phase-2/20261106_Stage-A-Board-Builder-Notes.md` (this file)

Modified: none. The board itself, its captures folder and the publish folder are written when the main session runs the builder with the real inputs.
