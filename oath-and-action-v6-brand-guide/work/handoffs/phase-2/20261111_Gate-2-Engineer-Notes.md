PREVIEW READY work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html 9441768

# Gate 2 engineer notes: the preview build

Oath & Action Edition 06, Phase 2, November 11, 2026. Task 3 of `20261111_Gate-2-Brief.md`. The engineer started from commit 043ad4d8; `guide_build.py --strict` passed as committed.

## Status

- Fonts fetched and checked: six WOFF2 files, 329,896 bytes, with three OFL texts and the manifest, under `work/build/assets/fonts/` (`fonts_fetch.py`).
- The editor's `where-to-start.json` and notes landed before the build work began, so no placeholder was needed on the page.
- Built and strict-clean at 17:12 (`guide_build.py --strict`: 0 warnings, 16 chapters, 185 rules, 424 specimens); the build's self-test passes, 27 of 27 scenarios. Now running the long checks.

## Fonts (D2-1697)

- **Request.** `fonts_fetch.py` asks Google Fonts for the page's own stylesheet, `Inter+Tight:wght@600;700;800`, `Inter:wght@400;500;600;700`, `Lora:ital,wght@1,400;1,500`, with a desktop Chrome 153 user agent, the version of the Chromium the checks run in.
- **What Google serves.** One variable WOFF2 file per family, style and script subset; every weight of a style points at the same file. Lora comes in italic only, as the page asks.
- **Subsets kept: latin and latin-ext.** A script read every character of the frozen page's text, alt text and names against Google's unicode ranges: all 103 distinct characters sit in latin, except five (→, ■, ▲, ▼, ✓) that only Lora's math and symbols subsets cover. A rendered run of the frozen page with Google Fonts loaded only the latin face of each family at 1440 and 390 px, so no Lora-set text uses those five; Inter text draws them from the system's fallback today and still will. latin-ext is kept for names with accents a later chapter may print (Polish, Czech, Turkish, Vietnamese names partly). Left out: cyrillic, cyrillic-ext, greek, greek-ext and vietnamese for both Inters; cyrillic, cyrillic-ext, math, symbols and vietnamese for Lora. Nothing on the page uses them.
- **Files.** Saved byte for byte as served, under dated names (`inter/20261111_Inter-Latin.woff2` and the rest); the manifest gives each file's URL, bytes, SHA-256, unicode range, weights and date. Each family folder holds its `OFL.txt` as published in google/fonts.

| File | Bytes |
|---|---|
| inter/20261111_Inter-Latin.woff2 | 48,256 |
| inter/20261111_Inter-Latin-Ext.woff2 | 85,068 |
| inter-tight/20261111_Inter-Tight-Latin.woff2 | 44,872 |
| inter-tight/20261111_Inter-Tight-Latin-Ext.woff2 | 89,800 |
| lora/20261111_Lora-Italic-Latin.woff2 | 40,772 |
| lora/20261111_Lora-Italic-Latin-Ext.woff2 | 21,128 |
| Six files | 329,896 |

### Rights ledger rows for the main session (`work/research/*_Rights-Ledger.md`)

| ID | Item | Source | License or terms | May ship |
|---|---|---|---|---|
| T-INTER | Inter, variable WOFF2, latin and latin-ext subsets, weights 400 to 700, unmodified | Google Fonts (fonts.gstatic.com, v20), fetched November 11, 2026; license text from github.com/google/fonts, ofl/inter/OFL.txt | SIL Open Font License 1.1; Copyright 2020 The Inter Project Authors (https://github.com/rsms/inter); no reserved font name | Yes, embedded in the guide and in the asset package's fonts folder, with OFL.txt beside the files |
| T-INTERTIGHT | Inter Tight, variable WOFF2, latin and latin-ext subsets, weights 600 to 800, unmodified | Google Fonts (fonts.gstatic.com, v9), fetched November 11, 2026; license text from ofl/intertight/OFL.txt | SIL Open Font License 1.1; Copyright 2022 The Inter Project Authors (https://github.com/rsms/inter-tight); no reserved font name | Yes, as Inter |
| T-LORA | Lora Italic, variable WOFF2, latin and latin-ext subsets, weights 400 and 500, unmodified | Google Fonts (fonts.gstatic.com, v37), fetched November 11, 2026; license text from ofl/lora/OFL.txt | SIL Open Font License 1.1; Copyright 2011 The Lora Project Authors (https://github.com/cyrealtype/Lora-Cyrillic), with Reserved Font Name "Lora" | Yes, unmodified only under the name Lora; a changed version may not use the name |

## The page

**Path and weight.** `work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html`, 9,441,768 bytes, 60.9 percent of the 15.5 MB budget; version 7 was 8,965,291. The difference, 476,477 bytes, is the fonts (443,189 bytes as six base64 data URLs in `<style id="oa-fonts">`, 4.7 percent of the page), the new front page and contents entry, the three license texts in the colophon and the shell's new styles. Headroom under the budget: 6.06 MB.

| Part | Bytes | Budget |
|---|---|---|
| Fonts (new part) | 443,189 | 500,000 |
| Head and shell | 189,118 | 200,000 |
| Sprites | 210,685 | 350,000 |
| Front matter and part openers | 25,495 | 100,000 |
| Appendix | 140,999 | 200,000 |
| Chapters 01 to 26 | unchanged from version 7, byte for byte | as before |

**What changed, and nothing else.** A script cut both pages into their sections: all 16 chapters, the six part openers and the appendix are byte for byte the same as version 7's. The cover changed in its folio and its second link; the contents gained its first entry; "Where to start" is new. Outside the sections: the head (the fonts block in place of the Google Fonts links, the title and description), the rail and menu entries, and the colophon's Edition and Type rows.

**Old path (D2-1702).** `guide_build.py` now writes the preview by default. `20261106_Stage-A-Chapters.html` stays in `work/boards/phase-2/stage-a/` as version 7's record, with its build report and check results, and is never rebuilt. Five scripts name it: `apply_pass_board_build.py`, `stage_a_board_build.py`, `stage_a_identity_q_measure.py`, `stage_c_board_c_build.py` and `stage_c_identity_round0.py`. Each builds or measures an earlier board from version 7 on purpose, so each keeps the old path. No check names it. The guide check's self-test now writes its plant results beside the preview.

## "Where to start" (D2-1698)

Rendered from the editor's `work/build/guide/front/where-to-start.json` (it landed before the build work began, so no placeholder reached the page), between the contents and the Foundations part, with the anchor `#start` and heading `#start-h` of the Gate 1 wireframe.

- **The head** is the contents' head: the title at the section size, the instruction line at the intro size.
- **The routes.** From 90em (1440 px) the three stand side by side on main's columns, their heads sharing one row through CSS subgrid, so the first step of each starts on one line. From 48em to 90em (1024 px) each route is a row: its name and lede on the first three columns, its seven steps on the rest, the way a Rule ID hangs beside its text; the head stays in view (sticky) while its steps scroll past. On phones the routes stack under a line of the three route names as links, which goes away once the three stand side by side.
- **A step** is one link, at least 44 px tall: its sentence, underlined (Rule 18.5), then a caption line the build reads from the assembled page, saying where it leads: "Rule 05.3 · Color", "Chapter 07 · Layout and spacing", "Appendix · Identity proofs". Its number hangs in the contents' 36 px box (CA-N8) on the sentence's first baseline, in Inter Tight in the secondary ink.
- **The later step** (designer 7) is quiet text in the secondary ink, never a link, with no second "later" marker; its words say it comes later.
- **The way back.** Each step carries its own id. Opening one sets the shell's way back, "Return to step 2 of New to Oath & Action, Where to start", and Return puts focus on that step, so a reader walks a route one step at a time. For the two steps that open house rules inside Rule 02.22's specimen, the way back now sits right after that plate, where the next Tab reaches it, in place of the top of chapter 02.
- **Links to it:** the cover ("Where to start", after "Open the contents"), the contents' first entry (its title and instruction line, one column wide), the rail and the phone menu, each after Contents.
- **The build stops** on any break in the brief's schema and on any step href that matches no id on the assembled page, and writes no page. The two specimen anchors (`#s-02-22-correct--h08`, `#s-02-22-correct--h03`) pass, since the check reads every id on the page.

## The license and the edition line (D2-1697, D2-1702)

- The editor's words are placed in `work/build/guide/front/edition.json`, which the build reads: the cover's folio ("Preview for approval, built November 11, 2026"), the colophon's Edition row, the page title and description, the new Type row and the three disclosure titles. The date is the build's own.
- Under the Type row, three disclosures built on details and summary as Rule 18.8 builds one: "The license for Inter Tight", "The license for Inter", "The license for Lora", each a 44 px row with the utility chevron from the sprite, which turns when open (0 ms under reduced motion). Each holds its family's OFL.txt in full: the file's paragraphs as paragraphs, hard line ends joined, each section heading on its own line in semibold, the lines of hyphens as hairlines. `fonts_fetch.py --page` proves the words on the page are the file's words, in order.

## Routine calls
D2-xxx | guide_build.py writes the Gate 2 preview by default; version 7's page stays as its record and is never rebuilt | One 9 MB page per round in the repository; the five scripts that name the old path build earlier boards from version 7 on purpose
D2-xxx | Keep the latin and latin-ext subsets of each family, and leave out cyrillic, greek, vietnamese, math and symbols | Every character on the page sits in latin, and a rendered run loaded only latin faces; latin-ext covers accented names a later chapter may print
D2-xxx | One @font-face per file over the weights Google declares for it (Inter 400 to 700, Inter Tight 600 to 800, Lora italic 400 to 500), in place of Google's one rule per weight | Each variable file goes in once; nineteen elements drawn both ways matched version 7 pixel for pixel
D2-xxx | Store the font files under dated names, with each Google URL, size and SHA-256 in the manifest | The project's file naming; the bytes stay as served, and the manifest ties each file to its source
D2-xxx | Fetch with a desktop Chrome 153 user agent | The version of the Chromium the checks run in; Google serves other files to other agents
D2-xxx | Fixture builds over test chapters keep the Google Fonts link; the guide's own and --demo builds embed | The build's earlier self-test scenarios stay as written; the guide check's self-test plants font faults on a demo that carries its fonts
D2-xxx | The fonts weigh as a part of their own, budget 0.5 MB, out of the head's 0.2 MB | The head's budget was set before the fonts moved in
D2-xxx | The front page takes the Gate 1 wireframe's anchor, #start, and heading id, #start-h | The approved wireframe named them
D2-xxx | Each step is one link, with a line the build writes from the page saying where it leads (Rule NN.n or Chapter NN, then the chapter's name) | A newcomer sees where a step goes before opening it, and learns how the guide numbers its rules
D2-xxx | Routes side by side from 90em, as rows from 48em, stacked on phones under a line of the three route names | Three columns fit only from 1440 px; a phone reader reaches the third route in one press
D2-xxx | The later step takes the secondary ink and no link, with no second "later" marker | Its words already say it comes later (the editor's and the main session's note)
D2-xxx | A step carries its own way back: "Return to step N of <route>, Where to start" | A reader walks a route one step at a time without losing their place
D2-xxx | A target inside a specimen gets its way back right after its plate | The two house-rule steps opened Rule 02.22's plate with the way back at the top of chapter 02, out of the Tab path; chapter 01's word list links gain the same fix
D2-xxx | The license texts open in disclosures on details and summary, the shell's copy of Rule 18.8's code set | Chapter 18's own rule for opening a part in place; no script needed
D2-xxx | The license paragraphs reflow, each heading on its own line, hyphen rules as hairlines | The file's hard line ends broke into ragged pairs at 390 px; the words stay the file's, which fonts_fetch.py checks
D2-xxx | The editor's edition and colophon words live in work/build/guide/front/edition.json | Words go into data files, never the output (the generator trap)
D2-xxx | The guide check's code harness takes the page's own @font-face block | The pasted copy draws with the same files and asks no server, so the pixel match stays fair
D2-xxx | The four-width guide check runs with --no-captures | The accessibility lead's evidence holds the board's screenshots; the captures folder would add about 19 MB to the repository
D2-xxx | Token parity evidence goes to work/boards/phase-2/gate-2/evidence/20261111_Token-Parity-Results.json, written by token_parity_evidence.py | The board builder reads it there, with the page's own copies of both token files checked against them


