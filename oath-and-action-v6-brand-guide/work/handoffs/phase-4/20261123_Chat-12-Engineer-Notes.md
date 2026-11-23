# Chat 12 engineer notes (E12): the weight options, measured, nothing landed

Engineer, chat 12, November 23, 2026. Brief: `work/handoffs/phase-4/20261123_Chat-12-Review-Brief.md`, section 5, "Engineer (E12)". Register row C11C-W1. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/engineer/` (the project folder copied to `proj/`, the variant pages in `var/`, the scripts in `scripts/`, the proofs in `proof/`). Started 17:12 UTC (`date -u`).

Status: weight options measured and proved (17:57 UTC); the fix pass follows in its own section below.

## How I measured

- **The baseline.** A strict build in my copy of the project folder, under the brief's lock (17:13:22 to 17:13:40 UTC): exit 0, **14,189,507 bytes**, the same as the main session's page except the "Built" time in the colophon (2 bytes differ). Chapter 16 219,338, chapter 20 839,096, chapter 21 1,106,224, as the build reports them.
- **The projection** is `guide_charts.gates()`: the page, plus every unbuilt chapter at its allocation (22 to 25 at 1,572,000, 27 and 28 at 400,000), plus a chapter still being built held at its allocation (15 at 29,899 and 16 at 80,662 today). 16,272,068 bytes, 272,068 past 16 MB. A byte saved in chapter 16 does not lower it until chapter 16 leaves `IN_PROGRESS`, since the hold grows by the same amount.
- **Each option** is a transform of the built page in scratch (`scripts/variants.py`, `xform.py`, `v3c_use.py`, `v3d_entities.py`), so its bytes are what a build step would write. Nothing in the repository changed but this file.
- **A pixel proof** captures every plate the option touches, in the base page and the variant, at 1440 and 390 px, device scale 1, Newsprint, reduced motion, with the shell's sticky parts hidden, and compares them pixel by pixel (`scripts/proof.cjs`, `compare.py`). Where the claim is that the parser builds the same document, the proof is the serialized DOM of both pages with scripts off (`scripts/domeq.cjs`).

## Weight options

Bytes are off the page unless the row says "projection". "Approved" marks a chapter approved at a gate (01 to 15, 17 to 19, 26, the chart kit).

| Option | Bytes saved | Reader loss | Chapters touched | Proof |
|---|---|---|---|---|
| **1a.** Release chapter 15's hold: `IN_PROGRESS` still lists chapters 14 and 15, which Gate 3 approved | 29,899 (projection only) | None | None on the page; `guide_charts.py` | The build report's `held_to_allocation` (15: 29,899) |
| **1b.** Chapters 22 to 25, 27 and 28 re-estimated from measured units (method below) | Mid **+108,043** (2,080,043 against 1,972,000); low −366,717; high +1,871,295 (projection only) | None | None | Arithmetic in `scripts/alloc.py`, table below |
| **1c.** Chapter 16 counted at its built bytes once board 1 approves it | 80,662 (projection only) | None | None | As 1a |
| **2a.** Every 1440 and 1024 px frame of a page that also has a 390 or 360 px frame, replaced by a line naming the export file (25 frames, chapters 20 and 21) | **594,349** | A desktop reader no longer sees the desktop and tablet layouts of the home, article and Act pages, the opener, or the atlas home, Reform R-23, the Register, Loop R18 and the loop index, light or dark. The export opens only where the asset package sits beside the guide; the guide alone cannot show them. A phone reader loses frames it met at about 330 px (C11-1) | 20, 21 | Changes the screen by design; none needed |
| **2b.** Only the 1024 px frames and the 1440 px dark frames replaced (14 frames) | **314,499** | The tablet width of chapter 20's five pages and the dark desktop of every page; light desktop and both phone themes stay | 20, 21 | As 2a |
| **2c.** Only the 1440 px dark frames replaced (9 frames) | **226,777** | The dark desktop; dark stays at 390 px | 20, 21 | As 2a |
| **2d.** A still picture in place of a wide frame | None: heavier | n/a | n/a | Measured from the exports at the 868 px the column shows: A13 1440 light 133,804 (AVIF) to 236,600 (WebP) against 67,805 of markup; A07 86,228 to 134,072 against 17,339. Two to eight times the markup, so not offered |
| **3a.** Plate styles drawn once: each `<style>@scope ([data-specimen="…"])` whose body repeats an earlier one is dropped, and the first carries a scope list of every specimen that uses it | **799,809** (chapter 01 194,847; 02 306,448; 03 49,530; 04 49,898; 08 16,510; 09 27,993; 10 16,970; 12 30,192; 19 13,091; 20 12,859; 21 19,073; 16 10,802; the rest under 10,000) | None | Every chapter but 14 and 15, approved ones included (their output, not their sources) | **764 of 764 identical** with 3b and 3e (382 specimens at 1440 and 390 px), and again inside C1 |
| **3b.** The page's 14 PNGs re-encoded losslessly (oxipng with zopfli) | **40,600** | None | 04, 09, 10, 17 (approved) | Decoded pixels identical, 14 of 14; on screen identical inside the 764 above |
| **3c.** Chapter 20's repeated chart drawings in its frames (S10 on the home page, S86 on the article, the Act page's process diagram, the favicon tab) drawn once as symbols and placed by `<use>` | **59,384** (7 groups, sprite 60,780). The first try took 12 groups (84,220); the tracker marks of the home and Act pages (five groups, `svg.mk`) lose their step fills under `<use>`, so they stay inline | None | 20 | First try: 40 of 48 plate captures identical, the 8 that moved all tracker marks (H.R. 7008's six steps drawn as plain dots). Without those groups: 48 of 48 identical inside C1 |
| **3d.** Text written with `"`, `>` and `'` as themselves where it now carries `&quot;`, `&gt;` and `&#39;` (outside script and style; the parser builds the same text) | **31,816** (chapter 18's code panels 27,879; 26 2,018; 20 480; the rest under 300 each) | None | 18 and 26 mostly (approved); every other chapter by a few bytes | **Same DOM**: both pages serialized with scripts off, 14,193,286 characters each, SHA-256 36b7738ecea54ce4… for both |
| **3e.** The latin-ext font faces left out (Inter, Inter Tight and Lora, 3 faces) | **193,255** | None on today's page: no character on it falls in their ranges, so no reader meets them. A reader typing such a character into a live example, or a later chapter printing an accented name outside Latin-1, would get a fallback font | Shell (every chapter's type) | No glyph on the page comes from them (character scan); on screen identical inside the 764 above |
| **3f.** The two photographs re-encoded losslessly (mozjpeg) | 1,008 | The second file loses its ICC profile, so only the first qualifies | Shell | Decoded pixels identical; not offered |
| **3g.** Comment lines and indentation out of the page's own inline scripts (the chart kit is already minified) | About 26,253 (comments 20,191: shell 11,696, chapter 18 7,846, chapter 26 649; indentation 6,062) | None, if the scripts behave the same | Shell, 18, 26 (approved) | Not built: a script change needs the guide check, not a picture |
| **3i.** The parts of chapters 20 and 21's frames that no reader meets (visually hidden words, `display: none` parts, SVG titles and descriptions inside the inert, hidden frames) left out | 65,323 (20: 24,341; 21: 40,982) | None on screen; a frame stops being the export page's markup word for word | 20, 21 | Measured in Chromium by computed style; not built or proved |
| **3h.** Chapters 14 and 18: other repeated drawings and tables | Under 10,000 each (14: tables 9,356; 18: drawings 7,611, tables 8,469) | Tables would need a script to repeat, a loss with scripts off | 14, 18 (approved) | Measured only; not offered. Chapter 14's plates use its own plate style (4,479) and gain nothing from 3a; its kit is minified |
| **4a.** Chapters 20 and 21's 83 frames carried compressed (raw deflate, base64, one block a chapter) and inflated at load by the chart kit's own synchronous inflater, before the shell's script | **1,182,087** (chapter 20 491,900; 21 690,654; the loader 467) | A sighted reader with scripts off sees each plate's label over an empty stage, since the alt words sit visually hidden; a screen reader still hears them (the stage's `aria-describedby`). To match D3-97 (a chapter 14 chart with scripts off shows its alt words and a line saying the drawing needs scripts), each frame would carry a `<noscript>` line, about 8,300 bytes for the 83. Someone reading the HTML source finds no frame markup there; the exports carry it | 20, 21 | **116 of 116 plates identical** (58 at 1440 and 58 at 390 px, 304 tiles); the two chapters' DOM after load identical at both widths, the carrier blocks aside |
| **4b.** Every plate in every chapter carried compressed, the same way | 6,620,422 | A reader with scripts off loses every plate's words, tables and pictures. Listed for scale; not recommended | All | Not built |
| **4c.** The two token downloads carried compressed and inflated when clicked (tokens.css in the colophon, tokens.json in chapter 26) | **516,992** (125,972 and 391,020) | A reader with scripts off cannot download those two files | 26 (approved), the colophon | Bytes only; download parity not tested |

### Combinations and the projection

Each line is a built variant page in `var/`, measured whole. The projection adds 1,972,000 for the unbuilt chapters and the holds (chapter 16 held at 300,000 until it leaves `IN_PROGRESS`; chapter 15 released where the line says so).

| Combination | Page | Projection | With 1b mid | With 1b high |
|---|---|---|---|---|
| Today | 14,189,507 | 16,272,068 | 16,380,111 | 18,143,363 |
| **C1, keeps everything:** 1a, 3a, 3b, 3c, 3d (`c1-lossless.html`) | 13,257,898 | **15,322,868** | 15,430,911 | 17,194,163 |
| C2: C1 and 3e (`c2-lossless-latinext.html`) | 13,064,643 | 15,129,613 | 15,237,656 | 17,000,908 |
| C3: C2 without 3c, and 4a (`c3b-no-use-plus-zframes.html`) | 11,941,940 | 14,006,910 | 14,114,953 | 15,878,205 |
| 4a alone (holds as today) | 13,007,420 | 15,089,981 | 15,198,024 | 16,961,276 |
| 2a alone (holds as today) | 13,595,158 | 15,677,719 | 15,785,762 | 17,549,014 |

"Keeps everything" means no word, form or picture leaves the page and no pixel moves at 1440 or 390 px (DR-271). C1 brings the projection to 15.32 MB, under the 15.5 MB line, with every unbuilt chapter at today's allocation; it stays under 16 MB unless the unbuilt chapters run past about 2.65 MB together (today 1.97 MB, my mid 2.08 MB). Only C3 stays under 16 MB in my high case, and it costs readers with scripts off chapters 20 and 21's pictures.

Overlaps: 3c and 4a both reach chapter 20's charts, so C3 leaves 3c out (with 3c, 4a saves 1,062,232 more instead of 1,182,087). 2a to 2c shrink to about an eighth of their bytes once 4a is taken (the frames compress to 12.7 percent), since the frames they remove are then compressed. 3a and 4b overlap, since the plate styles sit inside the plates; 3a and 4a do not (no frame carries a `<style>`).

### Option 1b: the allocations from measured units

Units read from the baseline build, as placed:

| Unit | Chat 10 used | Measured now |
|---|---|---|
| A rule's words and frames outside its plates | 6,726 | 7,247 (16), 8,913 (20), 6,775 (21); mean 7,645 |
| A failure plate | 8,039 (artboard) or 11,355 (print) | 3,677 (16), 5,409 (20), 4,732 (21); mean 4,606 |
| A full-length web frame | 21,530 with a figure | 16,063 (article), 30,121 (Act page), 34,166 (home with S10); mean 26,783. Atlas: 32,331 at 390, 33,483 at 1440; the Register 67,805 |
| A new renderer's style, once | not counted | 2,296 (plate) to 49,344 (web-site) and 50,112 (atlas) |
| Detail plates beside the full pages | not counted | Chapter 21 drew 12 (crops of parts), about 17,000 each |

Chapter 21 ran to 169 percent of its allocation for two reasons the table shows: its views were priced at 25,188 a frame and drew 32,000 to 67,800, and its crops and its kit style (74,826 with the sprite) were not priced. Its failure plates came in under (75,716 against 128,624). Each chapter below keeps chat 10's counts from the Gate 3 report's section 9 and changes only the unit prices: low takes the cheapest measured unit, mid the measured mean, high the dearest, with the items a page-like view needs (dark frames, profiles drawn as pages) added.

| Chapter | Allocation | Low | Mid | High | What moves it |
|---|---|---|---|---|---|
| 22 Newsletter and email | 277,000 | 239,440 | 342,780 | 709,463 | The working email at 600 and 375 px and images off priced as three page frames (80,349 mid against 44,512), its renderer's style (15,000 mid), four detail plates; failure plates cheaper. High: the email in both themes and Substack's eight parts as page frames |
| 23 Social and video | 743,000 | 657,828 | 843,592 | 1,377,532 | The 12 profiles "as a reader meets it at desktop and phone" are page frames, 16,063 each mid against an artboard's 8,039; failure plates cheaper (92,120 against 160,780). High: profiles at 26,783 and every post with its feed twin |
| 24 Reports | 338,000 | 233,281 | 282,305 | 572,228 | Failure pages at 4,606 against 11,355. High: the reader's pages at the full print unit and its controls as heavy as the web-site style |
| 25 Print and presentation | 214,000 | 174,734 | 211,366 | 384,072 | Failure plates cheaper; two detail plates. High: print and slide plates half again heavier |
| 27 and 28 (Phase 5) | 200,000 each | 150,000 each | 200,000 each | 400,000 each | No sample. Chapters 19 (173,323) and 17 (394,285) bracket them. Chapter 27's index of exports costs about 209 bytes a row (chapter 20's files table), so 150 exports add about 31,000 |
| **All six** | **1,972,000** | **1,605,283** | **2,080,043** | **3,843,295** | |

How far each could move: chapter 23 most (−85,000 to +635,000), then 22 (−38,000 to +432,000); 24 and 25 sit near or under their figures at mid. My recommendation for the board: keep G3-07's allocations in the build until each chapter is placed and measured (the lesson of chapter 21, "measure at first placement"), and show the mid and high totals beside the projection.

## Routine calls

- D4-xxx | Each option is measured as a transform of the strict build's page in scratch, never by changing a generator or the build | Nothing lands (brief section 5); a transform's bytes are what a build step would write
- D4-xxx | A pixel proof captures every plate an option touches in the base page and the variant at 1440 and 390 px, device scale 1, reduced motion, the shell's sticky parts hidden, and compares them pixel by pixel; DOM identity with scripts off where the claim is the parser's document | The brief asks pixel for pixel at 1440 and 390 px; a plate is the unit a reader meets
- D4-xxx | Captures are viewport tiles 900 px tall, scrolled by script and cropped to the plate's box, instead of Playwright's element shot | The element shot waited 45 seconds on plates that never settle (A05's menu plate) and a full-page clip took longer still; tiles take the same pixels at about seven a second
- D4-xxx | No still picture is offered for a wide frame | Measured two to eight times the markup it would replace (option 2d)
- D4-xxx | The photographs stay as they are | mozjpeg's lossless pass saves 1,008 bytes on one and drops the other's ICC profile
- D4-xxx | Subsetting the latin faces is not offered | D2-1697: the studio neither subsets nor renames a font, and Lora's license reserves its name; option 3e only leaves out faces no character on the page reaches
- D4-xxx | Compressed frames inflate with the chart kit's synchronous inflater in a script placed before the shell's, never with `DecompressionStream` | D3-90's reason: an asynchronous inflater lets print outrun it; the shell's scripts then see the frames as built
- D4-xxx | The re-estimate keeps chat 10's counts of what each chapter draws and changes only the unit prices | The counts come from the Gate 3 report's section 9, which Dustin approved; the prices are what chapters 16, 20 and 21 measured

## Done

1. **The baseline**, rebuilt in my copy under the lock: 14,189,507 bytes, exit 0, matching the main session's page but for the colophon's build time.
2. **Every option in the brief, measured**, with more found on the way (3c, 3d, 3e, 3g, 3i, 4c) and three measured to rule them out (2d, 3f, 3h). Each option's bytes come from a variant page built in scratch; the combinations C1 to C3 are built whole, not summed.
3. **Named place 14, bytes a reader never meets.** Yes, four kinds: the plate styles repeated in 381 specimens (788,534 bytes of repeats, 799,809 net of the scope lists); the three latin-ext font faces, which no character on the page reaches (193,255); chapter 20's charts drawn again in each frame of the same page, light and dark (59,384 net that `<use>` can save); and inside chapters 20 and 21's frames, 65,323 bytes a frame never paints, since every frame is an inert picture hidden from the accessibility tree: visually hidden words 41,286, parts set to `display: none` 11,467, SVG titles and descriptions 11,148, hidden by `visibility` 1,422 (chapter 20 24,341, chapter 21 40,982). Those last are the export pages' own markup, kept so a frame is the page as built; leaving them out is option 3i. The two token downloads (516,992) are met only by a reader who downloads them; the photographs, fonts in use and every plate's words are met.
4. **C11-1, the bytes.** Taking the wide frames out (2a) saves 594,349 and costs the desktop reader those pages; a still is two to eight times the markup; compressing the frames (4a) saves twice as much and keeps every frame for a reader with scripts on. The layout call for phones (narrow frames first, a scroll box at true size, or a link) is the design director's and adds or saves no bytes of its own.
5. **One fault for the fix pass:** `guide_charts.IN_PROGRESS` still holds chapters 14 and 15, which Gate 3 approved, so the projection carries 29,899 bytes for chapter 15 that will never be spent (option 1a). Chapter 14 sits over its allocation, so its hold costs nothing today.

## Not fixed

Nothing landed, as the brief asks: every option goes to Phase 4 board 1 (DR-271), and C11C-W1 stays open until Dustin chooses.

- **For Dustin** (each touches approved chapters' output, though no source and, where proved, no pixel): 3a reaches chapters 01 to 13, 17 to 19 and 26; 3b chapters 04, 09, 10 and 17; 3d chapters 18 and 26; 3e the shell, and it reverses the studio's call D2-1825 (keep latin-ext "for accented names a later chapter may print"); 3g the shell, 18 and 26; 4c chapter 26 and the colophon. My recommendation: take C1 (1a, 3a to 3d), which keeps every word, form and picture and moves no pixel; hold 3e until chapters 22 to 25 are written, since a name they print may need those faces; bring 4a to the board as the reserve if the unbuilt chapters come in near my high case.
- **For the fix pass, if the board agrees:** 1a in `guide_charts.py` (chapter 15 out of `IN_PROGRESS`), with its self-test case.
- **Option 2** is a design call on chapters 20 and 21 (C11-1); its bytes are above.
- **Not built:** 4b (a loss to every reader with scripts off), 3g (needs the guide check), 3h (under 10,000 each), 3i (it would part each frame from its export's markup; the board may weigh 65,323 bytes against that).

## Tested

- Strict build of the copied tree under the lock, 17:13:22 to 17:13:40 UTC: exit 0, 14,189,507 bytes; `cmp` against the main session's page: 2 bytes differ, both in the colophon's build time.
- Every byte figure above, read from the variant pages in `var/` and `var/variants.json`.
- PNGs (3b): each of the 14 decoded before and after with Pillow, pixels identical, 14 of 14. Photographs (3f): decoded identical; the ICC loss read from the file's info.
- Latin-ext faces (3e): every character of the page outside `data:` payloads, entities decoded, against the faces' `unicode-range`: none falls in a latin-ext-only range; CSS `content` escapes and script `\u` escapes checked the same way: none.
- Parts no reader meets inside the frames (3i): `scripts/hidden.cjs` in Chromium at 1440 px (17:43 UTC) walked all 83 frames by computed style: 65,323 of 1,359,431 bytes.
- 3c's first try (17:42 UTC): 24 chapter 20 plates at 1440 and 390 px against the base page, 40 of 48 identical; the 8 that moved were the tracker marks (looked at side by side: the six steps lost their numbers and fills). Those five groups now stay inline.
- Stills (2d): four 1440 px exports resized to 868 and 1,736 px wide and encoded as WebP (quality 80) and AVIF (quality 50) with Pillow, base64 lengths read.
- **4a, pixel for pixel:** chapters 20 and 21's 58 plates captured in the base page and the compressed-frames page in Chromium at 1440 and 390 px (17:37 to 17:41 UTC): **116 of 116 identical** (304 viewport tiles, cropped to each plate; every uncropped tile at 1440 px identical too). The `#web` and `#atlas` sections' DOM after load, at both widths: identical once the two carrier blocks are set aside (770,986 and 1,031,805 characters; 43 and 40 frames). The loader can remove each carrier after inflating, so the DOM matches whole.
- **3a, 3b and 3e together, pixel for pixel** (17:43 to 17:51 UTC): the 382 specimens whose style 3a moves, and the one other plate with a PNG, in the base page and `v3b-styles-png-fonts.html` at 1440 and 390 px: **764 of 764 identical** (1,072 tiles).
- **3d, DOM identity** (17:51 UTC): the base page and `v3d-entities.html` loaded with scripts off and serialized: the same 14,193,286 characters, the same SHA-256.
- **C1 whole, pixel for pixel** (17:51 to 17:57 UTC): `c1-lossless.html` (1a's arithmetic aside, every transform C1 holds) against the base page: the 382 specimens, **764 of 764 identical**, and chapter 20's 24 plates, **48 of 48 identical**.

## Not tested

- No variant went through the guide check (the brief forbids running it), and no strict build carries any option: the variants are transforms of a built page, so the build's own weight notes, stale-plate check and self-tests never saw them.
- Pixel proofs at 1024 and 360 px, in Charcoal, at device scale 2, in forced colors, in print and at 200 percent text: not run. The proofs cover 1440 and 390 px on Newsprint only, as the brief asks.
- 4a with scripts off: not captured; the reader loss in its row is read from the markup (the alt paragraph's `vh` class and the stage's `aria-describedby`).
- 4c: the two downloads inflated at click were not built or clicked; download parity (byte-identical files) is untested.
- 3g: not built; a script change needs the guide check and the chapter tests.
- Safari and Firefox: none of the proofs ran there (DR-279). `DecompressionStream` is not used, so 4a depends only on `atob`, `TextDecoder` and the chart kit's inflater, which the guide already needs.
- The re-estimate (1b) is arithmetic on measured units; no chapter 22 to 25, 27 or 28 plate was drawn.

# Fix pass (Engineer W)

Resumed for the fix pass under `work/handoffs/phase-4/20261123_Chat-12-Fix-Brief.md`, section 3.1, at about 17:47 UTC. The weight options' bytes went to the main session by message at 17:47. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/fix/engineer-w/`. Proofs of PR-M1 are run on my 17:12 copy of the project folder with only `app_plates.py` changed (`m1p/guide.html`), so another owner's work in progress cannot move a pixel in them.

## Fix pass: Routine calls

- D4-xxx | PR-M1: every selector of a kit style in the guide's head gets `:where(.oa-app-art *)` on its subject when the build places it (`app_plates.scope_css`), never a rewrite of the kit's files | Zero added specificity, so the cascade inside every frame is as before; the exports and working pages keep their own unscoped files
- D4-xxx | PR-M1: the atlas style's anchor also admits `.wa-sym` and its descendants | Chromium styles a `<use>` copy inside its own shadow tree, where no ancestor outside the symbol is seen (tested: `.ws .r` and `.r:where(.oa-app-art *)` leave a cloned rect unstyled, `.g1 .r` reaches it); every atlas symbol's root is `<g class="… wa-sym">` and no guide element carries the class
- D4-xxx | PR-S8: the root's Dark reaches only a page that names no theme, written `:where(:root[data-oa-theme="dark"]) .ws:not([data-oa-theme])`, so its specificity stays (0,2,0) as the old first selector's was | A frame drawn and labeled light stays light under the guide's dark theme; the working pages, whose root carries the theme, cascade as before
- D4-xxx | CR-13 and CD-S11: the kit holds identifiers, citations, times and addresses in a page's text at render (`hold()` in `web-site.mjs`), never in the words | The editor's words stay plain text; the rule applies to every page the kit draws, the partner's too
- D4-xxx | DD12-Q1: the comment panel stays at specs 11.5's columns (3 to 10, and 2 to 11 from 64em), with its words inside col 8 by the body measure | Specs 11.5 set those columns to hold the Comment screen inside Rule 05.1; cols 3 to 8 put it at 85.8 percent Newsprint. The fact panels' source form waits for the design director (Requests)
- D4-xxx | The frame pruner keeps a one-window page at least the window's height | Once CR-16 moved A06 up 6 px, pruning left its dark phone screen 0.4 px short and the kit's own pixel check stopped the build
- D4-xxx | PR-S2: a content file's `export_date` names its exports' date; `--date` still overrides | A run order then reproduces the studio's exports with no flag to remember
- D4-xxx | PR-S5: the build compares any `kit_inputs` a specimen's manifest entry lists; the generators' half is a request | The generators are the design director's and the editor's files

## Fix pass: Done

- **PR-M1.** `work/build/app-kit/tools/app_plates.py`: `scope_css()` holds every rule of the web-site, share-image, favicon-set and atlas-page styles to the frames' pages (`:where(.oa-app-art *)`; the atlas style `:where(.oa-app-art *,.wa-sym,.wa-sym *)`), @media and @container included, @keyframes left whole; two self-test cases (21 of 21 pass). `guide_check.js`: a new test, `kitReach`, matches every head kit rule against the page and fails one that reaches an element outside every frame's page and the kit's sprites; two plants, the chapter 15 pill drawn `rect.pl.sh` beside a share card frame with the rule unscoped (caught) and scoped (allowed). Proofs, on my copy with only `app_plates.py` changed (`m1p/guide.html`) against the reviewed page: chapters 20 and 21's 58 plates **116 of 116 identical** in light and **116 of 116** with the guide set dark (first try: 10 atlas plates moved, which led to the atlas anchor); chapters 01, 13, 15, 18 and chapter 14's 3-failure, 8-failure and 143 plates: **366 of 372 identical**, the six that moved being exactly `s-14-143-correct`, `s-14-143-failure` and `s-15-15-correct` at both widths, the plates the leak had broken; against version 15's committed page (`work/boards/phase-4/chat-10/20261121_Guide-Preview-V15.html`), each of the six plates shown alone at the top of its page (`iso.cjs`) at 1440 and 390 px, light and dark: the leak's block is gone from all three broken plates. Identical to version 15 in 12 of 24 captures (`s-14-143-failure` at 1440 both themes, `s-14-143-correct` at 390 both themes, `s-15-15-correct` at 390 dark, among them); the other 12 differ by anti-aliasing specks or a 1 px shift (at most 63 levels on `s-15-15-correct` at 1440), and the same kind of difference shows on plates the leak never reached (`s-15-15-failure` at 1440: 12,432 pixels against version 15, 0 between my page and the reviewed one), so it comes from the pages around them or the renderer, not from the kit's styles. I call that proved for the leak and not proved pixel for pixel against version 15. Bytes: the anchors add 27,771 to the page, chapter 20 +9,324 (its kit styles 55,116 to 64,440), chapter 21 +18,447 (the atlas style 50,112 to 68,559).
- **CD-M1 and CR-1.** `web-site.mjs`: `out_link(…, wrap)` holds a flex link's words in one span; the Act page's two source links now read "The rule on the Federal Register" and "The rule as a PDF on govinfo.gov" (each 4 px wider at 1440 and 390 px, measured in Chromium on the working page).
- **CR-13 and CD-S11.** `web-site.mjs` `hold()`: dockets (`FDA-2025-N-2699-0001`), report codes (`G22-CG-ISD`), section citations (`201(ff)(3)(B)`) and a one-letter prefix with its word (`N-acetyl`, `L-cysteine`) stay whole; a time keeps "p.m." on its line; an address breaks only after a slash (`regulations.gov/` `commenton/` `FDA-2025-N-2699-0001`). Seen on A08 at 390 px: "N-acetyl-L-cysteine" no longer splits after "N-", and the comment address breaks after "commenton/". The editor needs no non-breaking hyphen in the words.
- **CR-15, the ask panel, then DD12-Q1.** I first moved A08's comment panel to cols 3 to 8 (18:05 UTC). That broke specs 11.5, which had set it across the wide body columns to hold the Comment screen inside Rule 05.1, and the design director measured the screen at 85.8 percent Newsprint (DD12-Q1). Back at specs 11.5 (cols 3 to 10 from 90em, 2 to 11 from 64em, 18:41 UTC): the panel's words stop at the body measure (33.88rem, 542 px), so they end at 861 px, inside col 8's edge at 931, which keeps CR-15's text edge. Rebuilt A04 to A10 with `--date 20261121` (18:42 to 18:43 UTC, exit 0) and ran `phase4_ch20_build.py` (exit 0): **the Comment screen at 1440 px light is 81.8 percent Newsprint** (1024: 74.3; 390: 68.6; 360: 75.6), no screen of A06, A07 or A08 outside 60 to 85, and Rule 20.9's correct plate prints 81.8.
- **CR-16.** `web-site.mjs`: a kicker's 24 px topic icon takes negative block margins to the label's line height, so the Explainer kicker and its headline sit on the other three columns' lines (A06 at 1440 px, side by side; the article page is 5 to 6 px shorter for the same reason).
- **PR-S8.** `web-site.mjs` `dark()`, as the routine call says. The atlas renderer imports it, so A11 to A20 take it at Engineer A's next build.
- **PR-S1.** `oa-app.mjs`: a plate keeps its `written` while its content is the same; an atlas plate keeps its test's `ran` while its drawing and result are the same, and `atlas-test.json` its `ran` while every plate did; the manifest's entries sort by spec and it keeps its `written` while its list is the same. Proof: chapter 20's run order run twice (18:09 and 18:12 UTC): the 52 files it writes (seven plates, three styles, 41 exports, the manifest) **byte for byte the same** the second time.
- **PR-S2.** Specs `a01` to `a10` carry `"export_date": "20261121"`; `oa-app.mjs` names exports by it unless `--date` is given. Chapter 20's run order with no `--date` (18:09 UTC) wrote no 20261123 file.
- **PR-S3.** `oa-app.mjs`: the default output folder is `$TMPDIR/oa-app-out`; `OA_APP_OUT` and `--out` still name it.
- **PR-M2, the web half.** `web-site.mjs`: a content file may name `words_file`, the generator's entry shape for the page (with `site` or without; without, the studio site's words come from the generator); with none, every word comes from the generator as before. `oa-app.mjs` records the site's words (A07) for such a plate. Header comment lists the keys. Test (18:16 UTC, under the lock, into scratch only): a new article page A22 from a content file in my scratch naming its own words file (A07's entry with another headline) drew its two frames, its working page and two PNGs (dated 20261121 by its `export_date`), with the new headline in its plate; the repository's `git status` showed no A22 file.
- **PR-S5, the build's half.** `guide_build.py`: a specimen whose manifest entry lists `kit_inputs` (path to SHA-256) warns when any file has changed since, naming the generator to rerun. The generators' half is a request.
- **PR-S6.** `guide_check.js`: the page frame test catches a second `.oa-app-art` in one frame; six plants: low-contrast words inside a frame (caught by `contrast`), a glyph-only button inside a frame (allowed) and beside it (caught by `controlNames`), an atlas page's frame typed `atlas-page` (allowed by `specimenHeadings` and `pageFrame`), and a second page in one frame (caught). Not run: the main session runs the guide check and its self-test.
- **PR-S7, measured for board 1.** Inside chapters 20 and 21's 83 frames, 65,323 of 1,359,431 bytes are parts no reader meets: visually hidden words 41,286, `display: none` parts 11,467, SVG titles and descriptions 11,148, `visibility: hidden` 1,422 (chapter 20 24,341; chapter 21 40,982). Weight option 3i above; not landed.
- **Bytes, before and after** (strict build of the repository tree at 18:13 UTC, with other owners' work in it): page 14,189,507 to 14,232,627; chapter 16 219,338 to 220,060; chapter 20 839,096 to 858,352; chapter 21 1,106,224 to 1,128,286; the projection 16,272,068 to 16,314,466.

## Fix pass: Requests

- **Engineer A (`atlas-page.mjs`, specs a11 to a20):** (1) rebuild A11 to A20: my changes to `oa-app.mjs` (a plate input of every plate) and to `web-site.mjs` (`dark()`, PR-S8, which the atlas renderer imports) leave all ten atlas plates stale, and the strict build of 18:13 UTC warns 35 times for that alone; (2) add `"export_date": "20261122"` to specs a11 to a20 (PR-S2), so chapter 21's run order needs no `--date`; (3) CD-S6, the chip with the punctuation after it, is yours: the chip is drawn in `atlas-page.mjs`, not in `site-parts.mjs`; (4) keep `wa-sym` on every symbol's root group (`lib.mjs` writes it; the atlas style's scope depends on it).
- **Design director (CR-15):** name one form for a fact panel's source (inside the panel, as the Count panel's "39,555" has it, or under it on Newsprint, as DD-5 11.1 set for the fact box); I build it.
- **Generators' holders (PR-S5):** `phase4_ch20_build.py` (Rule 20.9's correct plate and `s-20-files`) and `phase4_ch21_build.py` (Rule 21.15's ratio table from `plates/a14.json`, Rule 21.16's report from `plates/atlas-test.json`): write `"kit_inputs": {"<path from the project folder>": "<sha256>"}` into each of those specimens' manifest entries for every kit file read; the build then warns when the kit draws again after the generator.
- **Main session:** (1) run `guide_check.js --self-test`: eight new plants (PR-M1 two, PR-S6 six) and one new test (`kitReach`) have not run; (2) the run orders: chapter 20's needs no `--date` now, and `--out` defaults to `$TMPDIR/oa-app-out`; (3) the register: CD-S8's row (below).
- **Editor:** CD-S11 needs no change in the words; the kit holds "N-acetyl" and the address.

## Fix pass: Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| CD-S6 | CD review | `atlas-page.mjs`, the chip | A parenthesis stranded at 390 px after a chip | A no-wrap span holding the chip and the punctuation after it | The chip is drawn in Engineer A's file, not in `site-parts.mjs` | Passed to Engineer A |
| CD-S8 | CD review | Chapter 16's files | No placeholder template at five ratios, sample WebVTT file, or shot list and rights row as CSV | Make them as kit exports, or name the chapter that holds them | Each needs words (the editor's rows, captions) and a drawing spec (the design director's) before the kit can export it; none fits 20 minutes from here | For the register: chapter 27 (the asset index, Phase 5) holds the files, made when chapter 16's words and the placeholder spec are final |
| CR-15, the ask panel's edge | Craft review | A08, `web-site.mjs` | The panel spans cols 3 to 10, an edge the page's text and chart do not share | Cols 3 to 8 | Specs 11.5 and Rule 05.1: at cols 3 to 8 the Comment screen reads 85.8 percent Newsprint (DD12-Q1). Its words end inside col 8 | Closed by the design director's spec, for the board |
| CR-15, fact panels | Craft review | A07, `web-site.mjs` | The "39,555" panel holds its source inside; the "5" panel sets it under the panel | One form | Waits for the design director's choice | Open, request above |
| PR-S5, the generators | Production review | `phase4_ch20_build.py`, `phase4_ch21_build.py` | Four plates print kit outputs with no stale check | Record `kit_inputs` in their manifest entries | The generators are not my files | Request above; the build's half is done |

## Fix pass: Tested

- `app_plates.py --self-test`: 21 of 21 pass (18:01 UTC).
- `node --check` on `guide_check.js` and `oa-app.mjs`; `guide_build.py` and `guide_charts.py` parse.
- Chromium, the use-element test (17:59 UTC): which selectors reach a cloned symbol's content.
- PR-M1's pixel proofs listed under Done, with `scripts/proof.cjs` and `compare.py` (tiles cropped to each plate, 1440 and 390 px), and the version 15 comparison with `iso.cjs` (each plate alone on its page).
- PR-M2's test page A22, built into scratch (above).
- Chapter 20's run order, three times (18:02 failed on the pruner's check, fixed; 18:09 and 18:12 UTC passed, exit 0); the generator after each (exit 0). The kit's own checks ran inside each build (axe, Tab, reflow, zoom, the pruner's pixel check).
- The exports against the reviewed commit (bc91667e), decoded with Pillow: A04, A05, A09 and A10 unchanged; A06, A07 and A08 changed where the fixes act; side by side for CR-16 (A06 1440 light) and CR-13 (A08 390 light); link widths, the ask panel and the address measured on the working page at 1440 and 390 px.
- PR-S1's rerun: 52 files by SHA-256, identical.
- Strict build of the repository tree (18:13 UTC): exit 1, 35 warnings, every one a stale atlas plate or the atlas self-test (Requests, Engineer A); none in chapter 20.

## Fix pass: Not tested

- The guide check and its self-test (the main session runs them): the eight new plants and `kitReach` have not run.
- A strict build with exit 0 on the repository tree: waits for Engineer A's rebuild of A11 to A20.
- Chapter 20's plates in the guide after the fixes, captured at 1440 and 390 px: not yet; the exports were compared instead.
- PR-S8 in the guide's dark theme (the 33 frames that took dark edges): not captured after the change.

## Fix pass, second round (the main session's two items, 18:36 UTC)

- **DD12-Q1, Done:** under "Fix pass: Done", CR-15. The cause was my own CR-15 change: the panel box narrowed from 60.2 to 44.7 percent of the screen's width. New figure 81.8 percent at 1440 px light.
- **CD-S7, Not fixed** (row below). Placement note for the design director (via the main session): when the kit draws it, a plate places the vertical frame as A09 is placed (`<div data-oa-app="A21" data-oa-app-views="1080-light"></div>` in `s-16-11-correct`, and the storyboard frames by their keys in `s-16-10-correct`), with its scale stated in the plate's label; chapter 16's generator prints the caption words.

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| CD-S7 | CD review; the design director's DD12-Q3 | A new kit application (A21, a video-frame renderer), `phase4_ch16_build.py` | Chapter 16's storyboard and vertical frame draw empty boxes where S04 belongs | The kit draws S04 in a 1080 by 1920 vertical frame and 1920 by 1080 storyboard frames, with the caption band and the source line on screen, its words from chapter 16's generator through a `--page-words` hook | More than the 40 minutes the main session allowed: a new renderer type and its export and plate checks, a words hook that chapter 16's generator does not have (the editor holds it this turn), the chart drawn at video size and checked against the 13 px floor at the plate's scale, and the data lead's sign-off. The design director's own estimate is about an hour | Open, for board 1 or the next engineer turn |
- **Strict build after DD12-Q1** (repository tree, 18:44 UTC): exit 1, 34 warnings, every one a stale atlas plate (A11 to A20 wait for Engineer A's rebuild); none in chapters 16 or 20. Page 14,267,413 bytes; chapter 16 220,066; chapter 20 858,353; chapter 21 1,163,065 (Engineer A's and the editor's work in progress included); projection 16,349,246.
