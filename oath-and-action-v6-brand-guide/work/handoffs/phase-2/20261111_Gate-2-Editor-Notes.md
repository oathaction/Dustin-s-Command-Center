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

Status: in progress. The sections below fill in as each item lands.
