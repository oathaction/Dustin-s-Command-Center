# Gate 2 editor notes: "Where to start", the font license and the edition line

Editor (`oa-editor`), November 11, 2026, for task 4 of `20261111_Gate-2-Brief.md`. Every word below that goes on the page follows chapter 02's writing rules. These notes may name decisions; the page names none.

## 1. "Where to start"

Written to `work/build/guide/front/where-to-start.json`, in the schema the brief fixes for task 3 (SHA-256 886f0f24…0e9cc599). Instruction line, from the architecture map, section 2: “Pick the route that matches why you’re here.”

| Route | Label | Steps | Later steps |
|---|---|---|---|
| newcomer | New to Oath & Action | 7 | 0 |
| designer | Designing a piece | 7 | 1 |
| builder | Building with code | 7 | 0 |

Where each step points, and why that place answers it:

| Route, step | Target | Why there |
|---|---|---|
| Newcomer 1 | `#purpose` | Chapter 01 opens with what we do, the word list and the four pillars before its rules |
| Newcomer 2 | `#rule-01-21` | Sets the seven content labels that open a kicker |
| Newcomer 3 | `#rule-01-23` | The “Our position” label and the strongest case against |
| Newcomer 4 | `#s-02-22-correct--h08` | House rule H08, the grade table; chapter 01’s word list links “Evidence grade” to this same anchor |
| Newcomer 5 | `#s-02-22-correct--h03` | House rule H03, the Illustrative label; the word list links here too |
| Newcomer 6 | `#rule-11-1` | The tracker’s six numbered steps |
| Newcomer 7 | `#rule-02-24` | One next step, with its date |
| Designer 1 | `#rule-03-2` | Choosing a lockup by width and surface |
| Designer 2 | `#color` | Rules 05.1 and 05.2 together: Newsprint first, then passing text pairs |
| Designer 3 | `#rule-05-3` | One working red per view |
| Designer 4 | `#rule-06-2` | The type scale |
| Designer 5 | `#layout` | Rules 07.1 and 07.2 together: the spacing scale and the column grid |
| Designer 6 | `#proofs` | The identity at true size on four of our pieces |
| Designer 7 | none, `later: true` | Chapters 20 to 25, the application chapters |
| Builder 1 | `#rule-26-8` | The two token files and their version |
| Builder 2 | `#rule-26-5` | Linking tokens.css and the body rule |
| Builder 3 | `#rule-26-3` | The five steps to a token |
| Builder 4 | `#rule-26-6` | Light and dark through one attribute |
| Builder 5 | `#components` | Chapter 18, every control as code to copy |
| Builder 6 | `#rule-17-8` | The ten states, each with words or a shape |
| Builder 7 | `#rule-19-7` | The verification matrix |

Terms the page defines where they first appear: the evidence grade, Illustrative, the lockup (in the word list’s own wording), Newsprint, tokens and WCAG 2.2 at level AA. The page avoids “working red” and “kicker” so it needs no more definitions.

### For the engineer

- **Two anchors sit inside a specimen.** Newcomer steps 4 and 5 point at house rules H08 and H03 inside Rule 02.22’s specimen, not at a `rule-` id. Each occurs once on the frozen page.
- **The later step already says so.** Designer step 7 reads “Chapters 20 to 25, which come later, will show…”, as the brief asks. Mark it the way the contents mark later chapters, and pick a mark that doesn’t print “Coming later” a second time right beside those words, such as a quiet tag or the contents’ later style alone.
- **Characters.** The words carry “&”, typographic quotes and apostrophes, and a no-break space (U+00A0) between each figure and “px”. Escape the HTML and keep the no-break spaces.
- **Anchors.** Use the page’s ids, not the architecture map’s table: chapter 08 is `#lockmark` and chapter 09 is `#pillar-icons` on the page.

## 2. The colophon’s license words

Each family’s copyright line, read from its OFL.txt at `https://raw.githubusercontent.com/google/fonts/main/ofl/{inter,intertight,lora}/OFL.txt` on November 11, 2026:

| Family | Copyright line, exact | Reserved name | SHA-256 of the file |
|---|---|---|---|
| Inter | Copyright 2020 The Inter Project Authors (https://github.com/rsms/inter) | None | 5b9321a4…8fd58c57 |
| Inter Tight | Copyright 2022 The Inter Project Authors (https://github.com/rsms/inter-tight) | None | 50240ab0…92cb9d58 |
| Lora | Copyright 2011 The Lora Project Authors (https://github.com/cyrealtype/Lora-Cyrillic), with Reserved Font Name "Lora". | “Lora” | 1d9a9708…a21be716 |

Inter Tight’s authors are The Inter Project Authors, the same as Inter’s. Below line 1 the three files are identical, 93 lines of plain ASCII with no em dash.

**The colophon’s Type row**, replacing today’s line, which ends “load from Google Fonts in this draft” and stops being true in the preview:

> Inter Tight sets display text, and Inter sets reading text and the interface. Lora Italic appears only in quoted lines. The Inter Project Authors made Inter and Inter Tight. Lora comes from The Lora Project Authors, and the authors license all three under the SIL Open Font License 1.1. We built the font files into this page unchanged, so it loads no type from elsewhere. Lora’s license reserves the name “Lora”, so a changed version would need another name. Open a license below to read it in full.

**The three disclosures’ words**, so each names what opens (Rule 18.8): “The license for Inter”, “The license for Inter Tight” and “The license for Lora”.

**Inside each disclosure**, the family’s OFL.txt exactly as fetched, its copyright line first. It is a quoted legal text, so chapter 02 leaves its wording, straight quotes and hyphens alone. Its URLs can stay as text.

## 3. The edition line

The date is the build’s date, taken from the build as the Built row takes it, so a rebuild on another day prints that day. November 11, 2026 below stands for it.

- **Cover**, the second half of the folio, in place of “Draft of November 7, 2026”: Preview for approval, built November 11, 2026
- **Colophon, Edition row**: Oath & Action Brand Guide, Edition 06. Chapters 01 to 12, 17 to 19 and 26, in a preview for approval, built November 11, 2026, with an appendix of identity proofs.
- **If the page title and description change too**: “Oath & Action Brand Guide, Edition 06: preview of chapters 01 to 12, 17 to 19 and 26” and, in the description, “Chapters 01 to 12, 17 to 19 and 26, in a preview for approval.”

“Gate 2” stays off the page. A reader can’t tell what it means, and “preview for approval” says the same thing in plain words. If Dustin wants the gate named, the main session can swap “for approval” for “for Gate 2”.

## 4. Found while working

1. **Two spacings before “px”.** Across the chapter files, 334 figures meet “px” with a plain space and 676 with a no-break space. Chapter 06 uses plain spaces only (71), and chapter 17 mostly no-break spaces (33 to 8). A line can break between “13” and “px” in the chapters that use plain spaces. This is drift for the red team’s list. The fix belongs in the chapter build scripts, owned by each chapter’s maker, with the editor’s sign-off on words.
2. **D2-1698 lists fewer later chapters than the page.** Its reason names chapters 13, 27 and 28 as not yet built. The brief and the contents treat 13 to 16, 20 to 25, 27 and 28 as later. The JSON follows the brief and the contents.
3. **Today’s Type row says the fonts load from Google Fonts.** The preview embeds them, so that row has to change with the build; section 2 gives its words.

## Routine calls

D2-xxx | The newcomer’s grade and Illustrative steps link to house rules H08 and H03 inside Rule 02.22 (`#s-02-22-correct--h08`, `#s-02-22-correct--h03`) | They are the rules that answer those steps, each id occurs once, and chapter 01’s word list already links to them
D2-xxx | Only the designer route carries a later step, chapters 20 to 25 | Built chapters answer every newcomer and builder step; a designer needs to know the application chapters are coming
D2-xxx | The edition line reads “Preview for approval, built” with the build’s date, and leaves out “Gate 2” | Chapter 02 keeps studio codes off the page (H11), and a reader can’t tell what a gate is
D2-xxx | A no-break space joins each figure to “px” in the new page’s words | Chapters 17 to 19 do this, so a size never breaks across a line
D2-xxx | The license disclosures read “The license for Inter”, “The license for Inter Tight” and “The license for Lora” | Rule 18.8 asks a disclosure’s words to name what opens
D2-xxx | The colophon names the authors from each OFL.txt’s copyright line: The Inter Project Authors for Inter and Inter Tight, The Lora Project Authors for Lora | Read from the three files on November 11, 2026
D2-xxx | The instruction line uses the typographic apostrophe, “you’re” | The guide’s prose sets typographic quotes and apostrophes, as the chapter files do

## Tested

- The JSON parses, with exactly the brief’s keys at every level, route ids in the order newcomer, designer, builder, and seven steps in each route.
- All 20 hrefs match an id on the frozen page, and each id occurs there once. The page’s SHA-256 matched the brief’s, 605377d2…8b6154.
- The one later step has a null href and says “later” in its words, and no built step names an unbuilt chapter.
- A script scan of every title, label, lede and step found none of these: em or en dashes, straight quotes, the listed fillers, corporate verbs, hedges, studio codes or decision numbers, exclamation points, “not” or “never”, inflated adjectives, figures under ten in prose, or a plain space before “px”. Pattern violations remaining, by type: 0 for each.
- I read each target rule’s text in `work/build/guide/chapters/*.json` and checked that each step says what its rule does.
- I read the three OFL.txt files: their copyright lines, reserved names, line counts, characters and URLs.
- A full read by hand of the JSON and of the words in sections 2 and 3, for rhythm, parallel runs, rhetorical triplets, setup and payoff, and a slogan at the close.

## Not tested

- How the page draws, its focus order, and the link check in the engineer’s build.
- Whether the 20 hrefs resolve in the preview. The preview changes no chapter, and its build stops on a miss.
- The license words and disclosures on the colophon’s Charcoal ground.
- How the words sound read aloud to real readers.
- Rhetorical triplets and parallel runs, which no script can rule out. I checked those by reading.

## Change log

- Created `work/build/guide/front/where-to-start.json`.
- Created `work/handoffs/phase-2/20261111_Gate-2-Editor-Notes.md` (this file).
- Scratch, outside the project: the writer and checker scripts and the three fetched license texts in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2/editor/`.

## Fix pass

Editor, November 11, 2026, under `20261111_Gate-2-Fix-Brief.md`. Items: CD-S1 for chapter 02, CD-S2 and CD-S3 in chapters 01 and 02, CD-S8 in chapter 02, CD-S9, DT-S12. Every change goes through `guide_editor_ch01.py`, `guide_editor_ch02.py`, `guide_editor_common.py` and the checks in `guide_editor_build.py`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2-fix/editor/`.

Status: done. The generator chain ran in the brief's order, `guide_build.py --strict` gives 0 warnings on a scratch build, and the editor build's own checks now hold every item below.

### CD-S1: chapter 02's opener

- **What.** A new specimen, `s-02-opener`, placed with `"opener": "s-02-opener"`. It sets the four locked lines and the order of the pillars as live text a reader can select (`readable`), under one caption line: “Our four locked lines and the order of the pillars, word for word.” The lines take Lora Italic 400 at the quote style with the opening mark hung 0.388 em (Rule 06.7); the pillars take the intro style at 600, each arrow kept with the pillar after it and hidden from screen readers, as the cover sets them. Each label sits above its line at every width, so the tagline holds one line at 1440 px.
- **No new drawing.** The words are the brand lines table's. The full table, with each line's role, places and the retired record, stays in the body as the reference Rule 02.23 points to.
- **Weight.** 4,001 bytes as placed, frame included. It carries only the five base styles it uses in place of the shared block, which had put it at 8,794.
- **First screen.** At 1440 by 900 px the opener starts at 665 px, so its caption and the tagline reach the first screen. At 390 px it starts at 853 px, under the two intro paragraphs.

### CD-S2: the caption lead and the bar, chapters 01 and 02

- **Lead.** Every failure caption in both chapters, 51 in all, now opens with “Fails Rule NN.N.” in bold, through one helper, `fails_lead`, in `guide_editor_common.py`. On the scratch build all 141 captions in the guide that carry the lead start with it.
- **Two invented tables.** Rules 01.9 and 01.12's failure plates carried no label of their own, so the shell printed its Illustrative chip ahead of the lead. Each now carries the label inside the plate, as its correct plate does: at the head of 01.9's invented tally, and beside 01.12's invented log row. The shell then leaves the caption alone.
- **The bar's colors.** The editor's bar is now Charcoal with its words in `--oa-color-text-primary-on-charcoal`, Newsprint, as stage C draws it. That covers all 27 bars in chapters 01 and 02. The editor's bar style lives only in `guide_editor_common.py`, and no other chapter uses it.
- **New bars.** Nine plates that draw a piece a reader could lift: 01.4 (the Prussian panel), 01.13, 01.14 and 01.17 (lines of copy), 01.15 (a kicker over a headline), 01.16 (the two readings), 01.21 (four kickers over headlines), 01.24 (product names) and 02.26 (a sentence of copy). Each alt now opens “Failure case: do not publish.” Rule 01.21's failure plate passes through the identity designer's `stage_b_identity_ch01.py`, which touches only its drawings and keeps the bar.
- **Plates left without the bar, as plates that draw a method:**
  - 01.9 and 01.10: a draft chapter's tally of examples by domain, state and level. It is a planning count, and no piece prints it.
  - 01.12: a row of the rotation log, an internal record our editors keep.
  - 02.1 to 02.21, the 21 writing rules' fault cards: each takes one sentence apart under the label “The fault”, with the faulty words struck and the rest dimmed, so no crop of it reads as a finished piece.

### CD-S3: rule titles

Chapter 02's titles were already one clause of twelve words or fewer, so none changed. In chapter 01, nine titles changed, and every clause a title dropped already stands in its rule's opening sentences:

| Rule | Was | Now | Where the dropped part lives |
|---|---|---|---|
| 01.7 | Keep party symbols, candidate photos, campaign gear and protest slogans out of brand graphics. (14 words) | Keep symbols that take a side out of brand graphics. | The rule's first sentence lists all four |
| 01.9 | Draw no more than one example in four from one atlas domain, or one in five from one state. (19) | Limit how many examples come from one domain or one state. | The rule now opens on both limits; its unit sentence moved second |
| 01.11 | Show a case from each party that uses a mechanism, and report the counts as the record gives them. (19) | Show each party’s cases and counts as the record gives them. | The title keeps the counts, the reason D2-368 gave for adding them |
| 01.13 | Name the office that decides, and name a party only when party is part of the finding. (17) | Name the office that decides. | The rule's second sentence, unchanged |
| 01.18 | Set both halves of a hinge headline in one color and weight, and give the red to the ampersand. (19) | Set both halves of a hinge headline in one color and weight. | The rule's second sentence |
| 01.19 | Join people through a rule or place they share, and rotate their order. (13) | Join people through a rule or place they share. | The rule's second sentence |
| 01.20 | Name parties, the left or the right in a hinge headline only to report sourced agreement. (16) | Name the sides in a hinge headline only to report agreement. | The rule names left, right and parties and asks for the source in the deck |
| 01.22 | In a process piece, name the step and leave the side to the reader. (14) | Leave the side to the reader in a process piece. | The rule's first sentence gives the one step |
| 01.24 | Name each product for what it does, and keep the ampersand for Oath & Action. (15) | Name each product for what it does. | The rule's second sentence keeps ampersands out of product names |

Kept as they are: 01.2 and 01.6, one clause at 13 words, and 01.23, one verb at 15 words. No other file quotes a changed title; I checked the chapters, the specimens, the scripts and the ledger by script. The editor build now fails a title over fifteen words.

### CD-S8: “Terms.” in chapter 02

Rules 02.1 and 02.2 set “Terms.” in `<strong>` in place of `<em>`, so it draws as roman Inter 700, a weight the page loads, in place of a slanted Inter it never loads. The page computes it as Inter 700, normal style, at 1440 and 390 px. The creative director asked for 600. A rule's text carries only the shell's inline tags, and `<strong>` gives 700, which is in chapter 06's set. If 600 matters, the engineer can give `.rule-text strong` the semibold weight in the shell; that file is the engineer's.

### CD-S9: Specifications for chapter 01

The 14 rules that had none now carry a short block, two to four rows each: 01.7, 01.9 to 01.20 and 01.24. Each row restates the rule's own words as a producer checks them: the label, the count, the place and, for 01.18, the two tokens the rule already names. The editor build now fails a chapter 01 rule with no block.

### DT-S12: “Prussian blue”

The three alts on `s-01-2-failure`, `s-01-3-failure` and `s-01-5-failure` now say “Prussian”. The editor build now fails “Prussian blue” anywhere in chapters 01 and 02.

### For the main session and other owners

- **The identity designer's chapter 01 opener.** `guide_editor_build.py` deletes any `s-01-*` or `s-02-*` specimen file it did not write and rewrites `manifest-editor.json`. A chapter 01 opener written by `stage_b_identity_ch01.py` survives only if that script writes the file and its manifest row on every run, after mine, and keeps the row out of `manifest-editor.json`.
- **`stage_c_identity_ch17.py` fails under `python3 -I`** at `import stage_a_identity_lib`, since `-I` leaves the script's folder off the import path. The rest of the chain ran. Owner: identity designer.
- **Two handoff files the chain rewrote.** `20261110_Stage-B-Round-2-Ch11-Figures.json` and `20261111_Stage-C-Round-1-Ch17-Figures.json` changed one line each, the token version from 6.0.0-gate2.8 to 6.0.0-gate2.9, from the engineer's release.

### Routine calls (fix pass)

D2-xxx | Chapter 02's opener sets the four locked lines and the pillar order as live text, and the full brand lines table stays in the body | A light version of an existing plate, as call 3 prefers, and Rule 02.23 still points at the table with its roles and the retired record
D2-xxx | The opener carries only the base styles it uses | It drops from 8,794 to 4,001 bytes as placed (D2-1214)
D2-xxx | Rules 01.9, 01.10 and 01.12's failure plates and the 21 writing-rule fault cards go without the bar | Each draws a method, a tally, a log row or a sentence taken apart under “The fault”, and no crop of it reads as a piece (call 4)
D2-xxx | Rules 01.9 and 01.12's failure plates carry their Illustrative label inside the plate | The shell then keeps its chip out of the caption, so “Fails Rule NN.N.” leads it, and each label sits beside its invented item as the correct plates do (DR-97)
D2-xxx | Rule 01.11's title keeps the counts: “Show each party’s cases and counts as the record gives them.” | D2-368 added them so the title teaches the uneven case too (DR-93)
D2-xxx | Rule 01.9's rule now opens on its two limits, and its unit sentence follows | Call 5 moves a title's dropped clause into the rule's first sentence
D2-xxx | Chapter 02's titles and chapter 01's 01.2, 01.6 and 01.23 stay as they are | Each is one clause and fifteen words or fewer, under call 5's limit
D2-xxx | “Terms.” takes `<strong>`, Inter 700 | The rule text's inline tags offer no 600, and 700 is in chapter 06's set; the shell can lower it if 600 is wanted
D2-xxx | The editor build fails a failure caption without the lead, a title past fifteen words, a chapter 01 rule without Specifications, “Prussian blue”, a chapter 02 opener without the four locked lines, and an italic “Terms.” | So a later edit to either generator cannot bring one back

### Tested (fix pass)

- The editor build's checks, old and new, pass: locked lines exact with no near miss, no em dash, no studio codes, every specimen placed once, opener included.
- A field-by-field diff of `01-purpose.json` and `02-voice.json` against the last commit shows only the changes listed above.
- The generator chain in the brief's order: every step ran except `stage_c_identity_ch17.py`, which stops at an import (above).
- `guide_build.py --strict` on a scratch build: 0 warnings, 9,361,185 bytes with other owners' work in progress.
- On that build: 141 failure captions with the lead and none without it at the front; chapter 01 has 21 barred failure plates and chapter 02 six; the opener weighs 4,001 bytes as placed.
- Playwright at 1440 and 390 px, 1x and 2x: chapter 02's first screen, the opener, the failure plates of 01.4, 01.13, 01.16, 01.21, 01.24, 02.26 and 02.1, and Rules 01.9, 01.18 and 02.1 with their Specifications. I looked at the captures. No plate frame overflows, the page made no outside requests, and “Terms.” computes as Inter 700, normal style.
- A script scan of every changed string for em and en dashes, fillers, corporate verbs, hedges, studio codes and “Prussian blue”. The only hits are the bar's own “do not publish” and the failing sentence of 02.26, which quotes “leverage” on purpose.

### Not tested (fix pass)

- The full guide check at four widths, which the main session runs on the rebuilt preview.
- The opener in the dark theme; chapter 02's plates draw on Newsprint only.
- A screen reader reading the opener's group and its description.
- The read of every changed string across all owners, which waits until every owner is done.

### Change log (fix pass)

- Modified `work/build/scripts/phase-2/guide_editor_common.py`, `guide_editor_ch01.py`, `guide_editor_ch02.py` and `guide_editor_build.py`.
- Regenerated `work/build/guide/chapters/01-purpose.json`, `02-voice.json`, `work/build/guide/specimens/manifest-editor.json` and the chapter 01 and 02 specimens; created `work/build/guide/specimens/s-02-opener.html`.
- Modified this file.
- Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2-fix/editor/` holds the scratch build, `look.js` and its captures.
