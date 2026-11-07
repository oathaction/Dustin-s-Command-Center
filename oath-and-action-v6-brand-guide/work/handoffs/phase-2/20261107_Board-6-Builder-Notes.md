# Board 6 hub builder notes

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the engineer for the creative director and the main session. This file sets the two inputs the Board 6 hub builder reads, so each of you can fill your part exactly. The builder stops with a plain message when a field is missing or wrong, so a failed run tells you what to fix.

## 1. What the builder does

```
python3 -I work/build/scripts/phase-2/board6_hub_build.py --strict
```

The hub is the page Dustin opens first for Board 6. It opens with the creative director's verdict, then gives one band to each of the four sections: Dustin's words, a short summary, the section's lead comparison captured at true size, our recommendation and a link to the full section page. The decisions for Dustin follow, numbered B6-1 on, with the reply box, and a short studio record closes the page.

On every run the builder opens each section page as it stands then, in a 1,440 by 900 window at device scale 2, and captures its lead comparison. Rerun it after the last build of any section page and the hub follows. It runs in about eight seconds.

It reads, from `work/boards/phase-2/board-6/`:

| File | Written by | Holds |
|---|---|---|
| `20261107_Board-6-Content.json` | the creative director | the title and deck, the verdict, one entry for each section, and the decisions |
| `20261107_Board-6-Studio-Record.json` | the main session | what was asked, the process, the checks run, what was not tested and the change log |
| `tracker/`, `pillar-icons/`, `stacked/`, `color-sheets/` | the makers | one finished section page in each folder, found as the folder's one `.html` file, with the check result `dataviz_check.js` wrote beside it |

It writes:

| Output | Where |
|---|---|
| The hub | `work/boards/20261107_Board-6-Explorations.html`, with captures and section pages linked by relative path |
| The captures, PNG, and the facts read from each page | `work/boards/phase-2/board-6/captures/` |
| The publish folder | `/tmp/claude-0/-home-user-Dustin-s-Command-Center/d4b0fb53-ac2c-5992-bcfd-deda558d4457/scratchpad/publish-board-6/` (section 7) |

A helper, `work/build/scripts/phase-2/board6_hub_capture.js`, does the browser work. The builder runs it; nobody runs it by hand.

Options: `--strict` exits 1 on any warning. `--no-capture` reuses the last captures, for layout work only, and the hub then says so. `--board-dir`, `--content`, `--record`, `--out`, `--captures` and `--publish` point at other places, as the sample test did. Errors exit 2.

## 2. What the hub shows, and where each part comes from

| Part | From the content | Read when the builder runs |
|---|---|---|
| Masthead and cover | `title`, `deck`, `ask`, `sample_reply` | the 24 px wordmark master |
| Verdict | `verdict`, `scores`, and each section's `pick` for the four recommendations at a glance | |
| A band for each section | the section's `asked`, `summary`, `note`, `lead`, `recommendation`, `why` and the decisions that name it | the lead comparison, captured from the page; the page's h1; the page's own check result |
| Decisions | `decisions` | the words of each place a decision points at on a section page |
| Studio record | the whole record | the builder adds its own checks |

A section folder with no page yet gets a placeholder band that says the page is still being made, and a warning. So the hub builds while a section is unfinished, and `--strict` fails until all four pages exist.

Each capture sits at its CSS size in a frame on a Newsprint mat. On a window narrower than the capture, the frame scrolls sideways and a line above it says so.

## 3. The content file, for the creative director

Write plain strings. Two marks work inside any text: `**bold**` and `` `code` ``. Write "B6-3" and the hub links it to that decision's card. Straight quotes become curly ones and a hyphen before a figure becomes the true minus sign, so type them plainly. Write `{{illus}}` where the Illustrative label belongs. Every word follows chapter 02's writing section. The builder fails on an em dash anywhere and on a locked line quoted inexactly, and warns on an en dash and on the words W17, W18 and W20 list.

```json
{
 "title": "Four explorations, for your pick",
 "deck": "One or two sentences under the title.",
 "ask": ["optional: what Dustin is asked, one line each"],
 "sample_reply": "optional: B6-1 to B6-6: as recommended.",
 "verdict": {
  "headline": "The verdict in one sentence.",
  "text": ["optional: one or two short paragraphs"]
 },
 "scores": [
  {"criterion": "Craft", "score": 4, "line": "optional, all six or none, as on board A"}
 ],
 "sections": {
  "tracker": {
   "summary": ["What the section made, one or two short paragraphs."],
   "pick": "optional: the recommendation in a few words, for the verdict's glance row",
   "recommendation": "The recommendation, one or two sentences, set large.",
   "why": "optional: the reason, a string or a list of paragraphs",
   "note": "optional: a note in your own voice, set in Lora Italic",
   "asked": "optional: Dustin's words, to replace the builder's quote from the brief, or false to leave the quote out",
   "lead": {"selector": "optional CSS selector", "caption": "optional caption", "alt": "optional alt text"},
   "page": "optional: the page's file name, needed only when the folder holds more than one .html"
  },
  "pillar-icons": {},
  "stacked": {},
  "color-sheets": {}
 },
 "decisions": [
  {
   "question": "Which bill tracker do we build?",
   "context": "optional: a sentence or two, or a list of paragraphs",
   "options": [{"text": "Numbered steps in lists, and the timeline on a bill's own page", "short": "numbered steps"}, "The segmented bar"],
   "recommended": "a",
   "recommendation": "optional: the recommendation in your words",
   "why": "The reason for it.",
   "section": "tracker",
   "touches": ["tracker#option-b", "tracker#option-d"],
   "source": "optional: where the question came from, named in words"
  }
 ]
}
```

| Field | Required | Rule |
|---|---|---|
| `title` | no | The hub's h1, set in the title style at up to 110 px. Default "Four explorations, for your pick" |
| `deck` | yes | One or two sentences |
| `ask` | no | Lines for "What you are asked". The default asks Dustin to read the verdict and the four sections, open a full page when he wants every option, and answer B6-1 to the last decision |
| `sample_reply` | no | The short reply shown in the ask box and in the reply box until Dustin marks an answer. Default "B6-1 to B6-n: as recommended." |
| `verdict.headline` | yes | One sentence, set large |
| `verdict.text` | no | A string or a list of paragraphs |
| `scores` | no | When given, exactly six entries in rubric order (Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility), each a whole number from 1 to 5 with a one-line reason, shown as on board A |
| `sections` | yes | Keyed `tracker`, `pillar-icons`, `stacked`, `color-sheets`. Any other key fails. A section whose page exists must have an entry |
| `sections.*.summary` | yes | A string or a list of paragraphs. The first paragraph sets in the intro style |
| `sections.*.recommendation` | when the page exists | One or two sentences, set in the H3 style on a White card |
| `sections.*.pick` | no | A few words for the verdict's row of four recommendations. Without it the row repeats the full recommendation |
| `sections.*.why` | no | The reason, beside the recommendation |
| `sections.*.note` | no | Your note, set in Lora Italic and credited "Creative director" |
| `sections.*.asked` | no | Each band opens with Dustin's words from the brief (section 6 lists them). Give a string to change the quote, or `false` to leave it out. Quote him exactly |
| `sections.*.lead.selector` | no | The element to capture as the lead comparison (section 5). Without it the builder uses the page's `data-board-lead` element, then the section's default |
| `sections.*.lead.caption` | no | The line above the capture. Each default selector has a default caption; when you name your own selector, write a caption too, or the builder warns |
| `sections.*.lead.alt` | no | The capture's alt text. The default names the page, the window width and your caption |
| `sections.*.page` | no | The page's file name inside its folder, needed only when the folder holds two pages |
| `decisions` | yes | At least one. They print in order as B6-1, B6-2 and on. If you write an `id`, it must match its place |
| `decisions[].question` | yes | The question, set as the card's heading |
| `decisions[].options` | yes | Two to eight. A string, or `{"text": ..., "short": ...}`; `short` is what the reply box writes when Dustin picks it. Options print as (a), (b) and on |
| `decisions[].recommended` | yes | The recommended option, as its letter ("b") or its number (2). It carries a Recommended label |
| `decisions[].recommendation` | no | The recommendation in your words. Without it the card repeats the recommended option |
| `decisions[].why` | yes | The reason |
| `decisions[].section` | no | The section the decision belongs to. The card links to that band, and the band lists the decision |
| `decisions[].touches` | no | Places on section pages: "tracker" for the whole page, "tracker#option-b" for an anchor, or `{"section": "tracker", "anchor": "option-b"}`. Each anchor must exist on its page. A decision with neither `section` nor `touches` warns |
| `decisions[].source` | no | A short source line under the card |

The content file may carry `"sample": true`; the hub then opens with a band that says it was built from sample files.

## 4. The studio record, for the main session

```json
{
 "asked": ["What Dustin asked for this board, one line each."],
 "process": [
  {"stage": "Makers", "text": "Who made each section page, and how."},
  {"stage": "Creative director", "text": ["The review, a string or a list of paragraphs."]}
 ],
 "checks": [
  {"name": "Hub check at three widths", "command": "node work/build/scripts/phase-2/dataviz_check.js work/boards/20261107_Board-6-Explorations.html --board", "result": "PASS, 0 failures at 1,440, 390 and 360 px.", "pass": true}
 ],
 "not_tested": ["..."],
 "changelog": {"created": ["work/..."], "modified": []}
}
```

| Field | Required | Rule |
|---|---|---|
| `asked` | yes | At least one line |
| `process` | no | A list of stages, each with `stage` and `text`. Any stage names; none is required |
| `checks` | yes | At least one. `command` and `pass` are optional; `pass` true or false prints "Pass." or "Fail." before the result |
| `not_tested` | yes | At least one line |
| `changelog` | yes | `created` and `modified`, each a list of repository paths relative to `oath-and-action-v6-brand-guide/` |

The record may carry `"sample": true` as well.

## 5. Section pages, leads and anchors

The builder takes each folder's one `.html` file as its section page. Two pages in one folder stop the build until `sections.*.page` names one.

**The lead comparison.** The builder captures one element of the page, in this order of choice:

1. The selector in `sections.*.lead.selector`. If it matches nothing, the build stops and lists the page's ids.
2. An element the maker marked on the page with the attribute `data-board-lead`.
3. The section's default, below. If the first default is missing and a later one matches, the builder warns.

| Section | Default selector | Default caption | Size today |
|---|---|---|---|
| tracker | `#compare table.mx:not(.mx-c)` | The four options side by side: your four bills as rows, each option drawn at 240 px, the width of a story card. | 1,280 by 1,255 px |
| pillar-icons | `#compare .cmp` | The three sets in the pillar row at 48 px in one color, with each word and icon ID beside its icon. | 1,248 by 525 px |
| stacked | `.lead .cmp-grid` | All six stacks beside today’s L2, every one with capitals 33 px tall. | 1,136 by 384 px |
| color-sheets | `#all-seven .thumbs-w` | All seven at once: the six new sheets and today’s palette, side by side. | 1,280 by 344 px on the page as it stood at 1:39 a.m. UTC |

A lead taller than 1,800 px warns, so a band holds one comparison. A lead wider than 1,312 px, the hub's column at 1,440 px, warns because it would scroll even on a desktop.

**Anchors a decision can name**, as the pages stood on November 7 at 1:39 a.m. UTC. The facts file in the captures folder, `20261107_Board-6-Hub-Capture-Facts.json`, lists every id on every page with the words the hub prints for it.

- tracker: `six-steps`, `compare`, `option-a`, `option-b`, `option-c`, `option-d`, `grid`, `checks`, `answers`
- pillar-icons: `compare`, `rec`, `how`, `set-a`, `set-b`, `set-c`, `naming`, `measure`, and the rows `cmp-a`, `cmp-b`, `cmp-c`
- stacked: `s1` to `s6`, `measures`, `method`
- color-sheets: `all-seven`, `sheet-patina`, `sheet-federal-ink`, `sheet-signal-orange`, `sheet-archive-ochre`, `sheet-highlighter`, `sheet-ballot-violet`, `sheet-today`, `checks`, `answers`

**Each page's own check.** The builder reads the result `dataviz_check.js` wrote beside each page and prints it under the band. It warns when the result is missing, when the page failed, and when the page changed after the check ran.

## 6. Dustin's words the bands quote by default

From the brief, `work/handoffs/phase-2/20261107_Board-6-Brief.md`, exactly as it records them:

- tracker: “a bill tracker should be much simpler, like a line with dots or a 1, 2, 3, 4, 5, 6 step process. That grid system's not clear. I want everything to be clear.”
- pillar-icons: “revisit the civic icons. I'd like to use those and maybe see just a few thoughts on the four icons for the four pillars.”
- stacked: “I don't know that I like that. Can you give me a few more variations of stacked?”
- color-sheets: “I want to see, if red wasn't at the forefront, what other colors would work.”

## 7. The publish folder

Every run empties and rewrites `scratchpad/publish-board-6/`. It holds:

- `index.html`: the hub without its document skeleton, as board A's publish copy was. It sets `lang="en"` by script, since the host's skeleton carries no attributes.
- `tracker.html`, `pillar-icons.html`, `stacked.html`, `color-sheets.html`: each section page whole, with a "Back to Board 6" link to `index.html` added as the first child of its `main` and styled from the token colors. The pages in the repository are left as they are.
- `<section>/...`: any local file a section page references (by `src`, `href`, `srcset`, `poster` or CSS `url()`), with the copy's references rewritten to match. A link from one section page to another becomes that page's published name. The four pages on the board today reference no local file, so these folders are empty for now.
- `captures/`: the four lead captures.
- `files.json`: every file to publish other than `index.html`, as published path to source path, the form the Artifact tool's `files` takes.

The hub links to the section pages as `tracker.html` and the rest, and each decision's places as `tracker.html#option-b`.

To publish: call the Artifact tool with `file_path` set to `publish-board-6/index.html` and `files` set from `publish-board-6/files.json`, with the icon "board". If you use the claude-artifacts `publish_files` tool, send `index.html` as `index.html` and every entry of `files.json` with its key as `as`. Read the hub and every page before publishing. The four pages and four captures came to about 3.3 MB in the sample.

## 8. Running it for the real hub

1. Make sure each section page has passed `node work/build/scripts/phase-2/dataviz_check.js <page> --board` since its last build. The color sheets page had no check result beside it when I tested.
2. The creative director writes the content file; the main session writes the record.
3. Run `python3 -I work/build/scripts/phase-2/board6_hub_build.py --strict`.
4. Run `node work/build/scripts/phase-2/dataviz_check.js work/boards/20261107_Board-6-Explorations.html --board`. Both packages are already in `work/build/node_modules`; if axe-core goes missing, install both together: `cd work/build && npm install --no-save axe-core@4.10.2 style-dictionary@5.8.0`. The check writes its result beside the hub and its screenshots to `work/boards/captures/`.
5. Add that check's result to the record's `checks` and rebuild, so the hub reports it.
6. Publish as section 7 says.

## 9. Routine calls, proposed for the decision log

| # | Decision | Reason |
|---|---|---|
| D2-xxx | Lead captures are PNG at device scale 2, clipped on whole CSS pixels, so each image is exactly twice its CSS size | Type and line art stay sharp with no JPEG ringing, and four images come to about 1.2 MB. A capture over 4 MB as PNG falls back to JPEG at quality 90 |
| D2-xxx | A lead comes from the content's selector, then the page's own `data-board-lead` element, then the section's default | The creative director can choose the comparison without editing a page, and a maker can mark it on the page |
| D2-xxx | Each capture sits on a Newsprint mat of up to 24 px inside a Stone hairline, narrowed so a capture that fits the 1,312 px column still fits with its mat at 1,440 px | The capture's own edge rules stay clear of the frame, and nothing scrolls sideways on a desktop |
| D2-xxx | The bands carry the numbers 1 to 4, as the brief and the section pages number the sections; the verdict, decisions and record carry none | A section has one number on the hub and on its page |
| D2-xxx | Each band opens with Dustin's own words from the brief, in Lora Italic | Each band starts from what he asked |
| D2-xxx | The masthead sets the 24 px wordmark master at 221 by 24 px with its ampersand in Pillar Red, marked `data-red="signature"`, as the guide's masthead does; the hub's styles carry no other red | The hub reads as Oath & Action's own page and has no working red |
| D2-xxx | The verdict ends with the four recommendations in one row, each linked to its band | Dustin sees every pick before he scrolls into the sections |
| D2-xxx | Decisions sit on White cards with an answer column, and the reply box is the hub's one Prussian panel, saved in the viewer's browser only | Board A's form (D2-315, D2-316), which Dustin has used |
| D2-xxx | The publish copies of the section pages gain a "Back to Board 6" link as the first child of their `main`; the repository pages stay unchanged | The link lines up with each page's content edge, and the makers' pages stay theirs |
| D2-xxx | A section page's local files publish under `<section>/`, with the copy's references rewritten | Four pages can share a file name without a clash |
| D2-xxx | The hub reads each section page's own check result and warns when it is missing, failed or older than the page | The hub never shows a page that has not passed its check without saying so |
| D2-xxx | A section folder with no page builds a placeholder band and warns | The hub can be laid out early, and `--strict` stops it shipping incomplete |

## 10. Tested

Every item below ran against sample inputs in the scratchpad, `/tmp/claude-0/-home-user-Dustin-s-Command-Center/d4b0fb53-ac2c-5992-bcfd-deda558d4457/scratchpad/board-6-sample/`, with the hubs, captures and publish folders written there too. Nothing from the sample went into the repository.

- Three pages, before the color sheets landed: the build captured the tracker, pillar icons and stacked leads, set a placeholder band for the color sheets and gave two warnings (the missing page, and a decision that names it). `dataviz_check.js --board` on that hub: PASS, 0 failures at 1,440, 390 and 360 px.
- Four pages with the color designer's real page as it first landed (1:34 a.m. UTC on November 7): the default lead `#all-seven .thumbs-w` captured; one warning, since no check result sat beside that page. `dataviz_check.js --board` on that hub: PASS, 0 failures at 1,440, 390 and 360 px, and again with `--mid` at 1,024 and 768 px. Axe-core 4.10.2 found no violations; smallest text 13 px; 40 focus stops at 1,440 px, each with a visible ring; one red mark, the wordmark's ampersand under `data-red="signature"`; no sideways scroll; Inter, Inter Tight and Lora loaded.
- Four pages with a sample color sheets page of my own in a scratch board folder, which references an SVG, a PNG with a query string, a CSS background and a link to the stacked page: `--strict`, 0 warnings. The copy loads `color-sheets/swatches/...` and links to `stacked.html#s1`.
- Each capture is exactly twice its CSS size: tracker 2,560 by 2,510 px for 1,280 by 1,255; pillar icons 2,496 by 1,050 for 1,248 by 525; stacked 2,272 by 768 for 1,136 by 384; color sheets 2,560 by 688 for 1,280 by 344.
- The publish copy wrapped in a document skeleton, in Chromium at 1,440 and 390 px: `lang` is "en"; the four captures load at full resolution; each band's link opens its page; each page's back link, 44 px tall and on the page's content edge, returns to `index.html`; decision links point at `<section>.html#anchor`; no page errors and no failed requests.
- `dataviz_check.js --board` on the published copies of the tracker, pillar icons and stacked pages, back link included: PASS, 0 failures each.
- The reply box: marking (a) on B6-1 and (b) on B6-3, with notes on B6-3 and B6-5, gave three reply lines; Copy put them on the clipboard; a reload restored them; no page errors.
- I looked at the hub with Playwright at 1,440 and 390 px from top to bottom, and fixed what read badly: the capture's edge against its frame, chip words in anchor labels, the wording of links into section pages, the scroll line's place above a tall frame, the back link's arrow and rule, and the spacing of wrapped links on phones.
- Inputs that should fail, each with its message: an em dash in the deck, the tagline quoted without its period, a decision pointing at an anchor a page lacks, a recommended option past the last, a decision numbered out of order, an unknown section key, a lead selector that matches nothing (the message lists the page's ids), a page with no content entry, a record with no checks, a publish folder holding files the builder did not write, two pages in one section folder, a decision pointing at an unknown section and a decision with one option. A flagged word with `--strict` exits 1.

## 11. Not tested

- The real content and record, which do not exist yet, and so the real hub's length and decisions.
- The color sheets page's final build and its check result. Its page changed while I worked, and at 390 px it then ran wider than the screen; its own check will say whether that holds.
- The published hub on claude.ai: whether the host serves the hub at `index.html` so a section page's back link returns to it, whether relative links into section pages work inside the host's frame, and whether Copy reaches the clipboard there. The button falls back to selecting the text.
- A section page that references local files, other than my sample; the four real pages reference none.
- Safari, Firefox, real phones and screen readers.

## 12. Change log

Created:
- `work/build/scripts/phase-2/board6_hub_build.py`
- `work/build/scripts/phase-2/board6_hub_capture.js`
- `work/handoffs/phase-2/20261107_Board-6-Builder-Notes.md` (this file)

Modified: none. The hub, its captures folder and the publish folder are written when the main session runs the builder with the real inputs. Nothing was committed or pushed.
