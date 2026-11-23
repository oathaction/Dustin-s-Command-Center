# Chat 12 engineer notes (E12): the weight options, measured, nothing landed

Engineer, chat 12, November 23, 2026. Brief: `work/handoffs/phase-4/20261123_Chat-12-Review-Brief.md`, section 5, "Engineer (E12)". Register row C11C-W1. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/engineer/` (the project folder copied to `proj/`, the variant pages in `var/`, the scripts in `scripts/`, the proofs in `proof/`). Started 17:12 UTC (`date -u`).

Status: measurements done; pixel proofs running (this file is updated when they land).

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
| **3a.** Plate styles drawn once: each `<style>@scope ([data-specimen="…"])` whose body repeats an earlier one is dropped, and the first carries a scope list of every specimen that uses it | **799,809** (chapter 01 194,847; 02 306,448; 03 49,530; 04 49,898; 08 16,510; 09 27,993; 10 16,970; 12 30,192; 19 13,091; 20 12,859; 21 19,073; 16 10,802; the rest under 10,000) | None | Every chapter but 14 and 15, approved ones included (their output, not their sources) | Pending (381 specimens) |
| **3b.** The page's 14 PNGs re-encoded losslessly (oxipng with zopfli) | **40,600** | None | 04, 09, 10, 17 (approved) | Decoded pixels identical, 14 of 14; on screen pending |
| **3c.** Chapter 20's repeated chart drawings in its frames (S10 on the home page, S86 on the article, the Act page's process diagram, the favicon tab) drawn once as symbols and placed by `<use>` | **59,384** (7 groups, sprite 60,780). The first try took 12 groups (84,220); the tracker marks of the home and Act pages (five groups, `svg.mk`) lose their step fills under `<use>`, so they stay inline | None | 20 | First try: 40 of 48 plate captures identical, the 8 that moved all tracker marks (H.R. 7008's six steps drawn as plain dots). Without those groups: proved inside C1 (below) |
| **3d.** Text written with `"`, `>` and `'` as themselves where it now carries `&quot;`, `&gt;` and `&#39;` (outside script and style; the parser builds the same text) | **31,816** (chapter 18's code panels 27,879; 26 2,018; 20 480; the rest under 300 each) | None | 18 and 26 mostly (approved); every other chapter by a few bytes | Pending (DOM identity) |
| **3e.** The latin-ext font faces left out (Inter, Inter Tight and Lora, 3 faces) | **193,255** | None on today's page: no character on it falls in their ranges, so no reader meets them. A reader typing such a character into a live example, or a later chapter printing an accented name outside Latin-1, would get a fallback font | Shell (every chapter's type) | No glyph on the page comes from them (character scan); on screen pending with 3a |
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

## Not tested

- No variant went through the guide check (the brief forbids running it), and no strict build carries any option: the variants are transforms of a built page, so the build's own weight notes, stale-plate check and self-tests never saw them.
- Pixel proofs at 1024 and 360 px, in Charcoal, at device scale 2, in forced colors, in print and at 200 percent text: not run. The proofs cover 1440 and 390 px on Newsprint only, as the brief asks.
- 4a with scripts off: not captured; the reader loss in its row is read from the markup (the alt paragraph's `vh` class and the stage's `aria-describedby`).
- 4c: the two downloads inflated at click were not built or clicked; download parity (byte-identical files) is untested.
- 3g: not built; a script change needs the guide check and the chapter tests.
- Safari and Firefox: none of the proofs ran there (DR-279). `DecompressionStream` is not used, so 4a depends only on `atob`, `TextDecoder` and the chart kit's inflater, which the guide already needs.
- The re-estimate (1b) is arithmetic on measured units; no chapter 22 to 25, 27 or 28 plate was drawn.
