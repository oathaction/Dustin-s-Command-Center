# Chat 12b engineer notes (Engineer M): the weight options, measured again, nothing landed

Engineer M, chat 12b, November 24, 2026. Brief: `work/handoffs/phase-4/20261124_Chat-12b-Brief.md`, section 3.7. Register rows C11C-W1 and PR-S7 (chat 12 section). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/engineer-m/` (the project folder copied to `proj/` at 00:02 UTC, the scripts in `scripts/`, the opening page's results in `opening/`). Started 00:01 UTC (`date -u`). Nothing in the repository changes but this file (DR-271).

Status at 00:27 UTC: every option in 3.7 rebuilt as a script and measured on the opening page. Ready for the final page. The pixel proof of C1 and 3d's document identity in Chromium wait for it, as the brief says.

## How I measured

- **The page.** A strict build of my copy of the project folder, under the lock (00:03:42 to 00:03:58 UTC): exit 0, no warnings, no stale plate, **14,395,945 bytes**, 409 rules, 766 specimens, the page of record's size. Its build report gives the projection as 16,476,174 (chapter 15 held 29,899, chapter 16 held 78,330).
- **The weigher.** The scripts import the build's own `weigh()` (`guide_build.py`) and `guide_charts.gates()` from the copy, so every variant is weighed and projected the way a build would. On the opening page they give 14,395,945 bytes and 16,476,174, the build report's figures to the byte.
- **The projection, two ways.** "As the build computes it" is `gates()` with `IN_PROGRESS` as written: every Phase 4 chapter in place counts at no less than its allocation (16 at 300,000, 20 at 757,000, 21 at 655,000) until it leaves the list. "16 held" is chat 12's convention, where only chapter 16 is held and chapters 20 and 21 count at their bytes. The two agree for every option that leaves chapters 20 and 21 over their allocations. They part for 4a and 2a, which take chapter 20 (and with 4a, chapter 21) under its allocation, so the build holds most of their saving back until those chapters leave `IN_PROGRESS`.
- **Each option** is a transform of the built page (`scripts/xforms.py`), so its bytes are what a build step would write. Each combination is one variant page built whole. Option 3i takes its parts from a computed-style measure in Chromium (`scripts/measure_3i.cjs`) and cuts them from the source, each found again by its tag name and index (all 268 found).
- **One command** reruns all of it on a new page: `bash scripts/run.sh <page.html> <label>` (add `--proof` for C1's pixel proof at 1440 and 390 px and 3d's document identity with scripts off). It copies the project folder to `proj-<label>/` for the build's own modules, reads `browsers.sh` before each browser, and writes `<label>/results.json`, `<label>/table.md` and the variant pages in `<label>/var/`.

Scripts, all in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/engineer-m/scripts/`: `run.sh`, `run_all.py`, `xforms.py`, `weigh.py`, `units.py`, `table.py`, `pagelib.py`, `measure_3i.cjs`, `proof.cjs`, `compare.py`, `domeq.cjs`, `domcheck.py`.

## Weight options, on the opening page (14,395,945 bytes)

Bytes are off the page unless the row says "projection". The projection column is the build's own figure for that option alone (today 16,476,174).

| Option | Bytes saved off the page | By chapter (and part) | Projection, as the build computes it | Reader loss | Chapters touched |
|---|---|---|---|---|---|
| **1a.** Release chapter 15's hold: `IN_PROGRESS` still lists chapters 14 and 15, which Gate 3 approved | 0 (29,899 off the projection) | none | 16,446,275 | None | None on the page; `guide_charts.py` |
| **1b.** Chapters 22 to 25, 27 and 28 re-estimated from measured units (table below) | 0 | none | low 16,226,009; mid 16,767,009; high 18,398,103 (against 1,972,000 allocated: low −250,165, mid +290,835, high +1,921,929) | None | None |
| **2a.** Every 1440 and 1024 px frame of a page that also has a 390 or 360 px frame, replaced by a line naming its export file | **641,673** (26 frames) | 21 358,906; 20 282,767 | 15,998,569 (the build holds 164,068 of chapter 20's saving) | A desktop reader no longer sees the desktop and tablet layouts of those pages, light or dark; the export opens only where the asset package sits beside the guide. A phone reader loses frames it met at about 330 px (C11-1) | 20, 21 |
| **2b.** Only the 1024 px frames and the 1440 px dark frames replaced | **326,067** (14 frames) | 20 180,059; 21 146,008 | 16,211,467 | The tablet width of chapter 20's five pages and the dark desktop of every page; light desktop and both phone themes stay | 20, 21 |
| **2c.** Only the 1440 px dark frames replaced | **235,954** (9 frames) | 21 146,008; 20 89,946 | 16,240,220 | The dark desktop; dark stays at 390 px | 20, 21 |
| **3a.** Plate styles drawn once: each `<style>@scope ([data-specimen="…"])` whose body repeats an earlier one is dropped, and the first carries a scope list of every specimen that uses it | **799,531** (452 of 856 blocks dropped; the 499 blocks of the 47 repeated bodies sit in 382 specimens) | 02 306,448; 01 194,847; 04 50,396; 03 48,518; 12 30,615; 09 27,993; 14 more under 21,792 (chapter 05 grows 2,977, since its block carries a long scope list) | 15,687,537 | None | Every chapter but 14 and 15 (their output, not their sources) |
| **3b.** The page's PNGs re-encoded losslessly (oxipng 9.1.1, zopfli deflater) | **40,600** (14 PNGs, 13 distinct; decoded pixels the same, 13 of 13) | 10 38,152; 17 2,000; 09 324; 04 124 | 16,435,574 | None | 04, 09, 10, 17 |
| **3c.** Chapter 20's repeated drawings in its frames (S10 on the home page, S86 on the article, the Act page's process diagram, the favicon tab) drawn once as symbols in the identity sprite and placed by `<use>`; the tracker marks stay inline | **58,999** (7 groups, sprite 60,833) | 20 58,999 | 16,417,175 | None | 20 |
| **3d.** Text and quoted attribute values written with `"`, `>` and `'` as themselves where they carry `&quot;`, `&gt;` and `&#x27;` (outside script, style and comments) | **38,548** (text 37,511; attribute values 1,037) | 18 32,814; 26 2,428; 21 1,022; 20 490; 11 290; 10 192; 16 more under 180 | 16,437,706 | None | 18 and 26 mostly; every chapter by a few bytes |
| **3e.** The latin-ext font faces left out (Inter, Inter Tight and Lora, 3 faces) | **193,255** | fonts 193,255 | 16,282,919 | None on this page: no character anywhere on it falls in their ranges. A reader typing such a character into a live example, or a later chapter printing an accented name outside Latin-1, would get a fallback font | Shell (every chapter's type) |
| **3i.** The parts of chapters 20 and 21's frames that no reader meets (visually hidden words, `display: none` parts, `visibility: hidden` parts, SVG titles and descriptions inside the inert, hidden pictures) left out (PR-S7) | **81,031** (268 parts: visually hidden 48,996, `display: none` 16,917, SVG title or desc 11,148, `visibility: hidden` 3,970) | 21 58,742; 20 22,289 | 16,395,143 | None on screen; a frame stops being its export page's markup word for word | 20, 21 |
| **4a.** Chapters 20 and 21's 90 frames carried compressed (raw deflate, base64, one block a chapter) and inflated at load by the chart kit's own inflater, before the shell's script | **1,280,418** (loader 391) | 21 798,149; 20 482,660 | 15,740,129 (the build holds 544,373 of it: chapter 20 363,961, chapter 21 180,412) | A sighted reader with scripts off sees each plate's label over an empty stage; a screen reader still hears each frame's alt (the stage's `aria-label`). Matching D3-97 would add a line a frame saying the picture needs scripts. Someone reading the HTML source finds no frame markup there | 20, 21 |
| **4c.** The two token downloads carried compressed and written back into their links at load (tokens.css in the colophon, tokens.json in chapter 26) | **516,489** (loader 447) | 26 390,992; the colophon 125,944 | 15,959,685 | A reader with scripts off cannot download those two files | 26, the colophon |

Overlaps, each measured as built:

- 4a after 3c saves 1,189,498 more (alone 1,280,418), since 3c's drawings are then not in the frames it compresses. So C3 leaves 3c out.
- Once 4a is taken, 2a saves 83,598 (alone 641,673), 2b 46,334 (alone 326,067) and 2c 30,112 (alone 235,954): the frames they remove are then compressed.
- 3a and 4a do not overlap (no frame carries a `<style>`).

### Combinations and the projection

Each line is a variant page built whole and weighed as the build weighs it. C1 to C3 include 1a.

| Combination | Page | Projection, as the build computes it | Projection, 16 held | Build, 1b mid | Build, 1b high | Room under 16,000,000 (build) |
|---|---|---|---|---|---|---|
| Today | 14,395,945 | 16,476,174 | 16,476,174 | 16,767,009 | 18,398,103 | −476,174 |
| **C1, keeps everything:** 1a, 3a, 3b, 3c, 3d | 13,458,267 | **15,519,541** (holds 16: 89,274) | 15,519,541 | 15,810,376 | 17,441,470 | +480,459 |
| C2: C1 and 3e | 13,265,012 | **15,326,286** (holds 16: 89,274) | 15,326,286 | 15,617,121 | 17,248,215 | +673,714 |
| C3: C2 without 3c, and 4a | 12,044,241 | **14,686,751** (holds 16: 89,274, 20: 378,658, 21: 202,578) | 14,105,515 | 14,977,586 | 16,608,680 | +1,313,249 |
| 4a alone | 13,115,527 | 15,740,129 (holds 15: 29,899, 16: 78,330, 20: 363,961, 21: 180,412) | 15,195,756 | 16,030,964 | 17,662,058 | +259,871 |
| 2a alone | 13,754,272 | 15,998,569 (holds 15: 29,899, 16: 78,330, 20: 164,068) | 15,834,501 | 16,289,404 | 17,920,498 | +1,431 |

What the table says. C1 keeps every word, form and picture and brings the build's projection from 16,476,174 to 15,519,541, 480,459 under 16 MB and 19,541 past the 15.5 MB line. It saves 937,678 bytes off the page (chat 12 measured 931,609 on a page 206,438 bytes lighter). C2 adds the latin-ext faces and reaches 15,326,286. Only C3 stays under 16 MB in the 1b high case (16,608,680 as the build computes it, 16,027,444 with chapters 20 and 21 at their bytes), and it costs readers with scripts off chapters 20 and 21's pictures. With 4a, the build holds 581,236 bytes of C3's saving back until chapters 20 and 21 leave `IN_PROGRESS`, since both then weigh less than their allocations; chat 12's table did not show that hold.

A byte saved in chapter 16 does not lower the projection while chapter 16 is held: C1 takes 10,944 bytes from it and its hold grows by the same.

### Option 1b: units measured on this page, and the chapters re-estimated

I kept chat 10's counts (`work/handoffs/phase-4/20261121_Phase-4-Allocations.md`, section 3) and chat 10's prices for parts no built chapter draws yet (an artboard plate 8,039, a smallest-size twin 3,657, a print page 11,355, a chart 11,570, the report reader 69,902 and its assumed controls 10,000, chapter 25's print and slide plates). The rest come from today's chapters 16, 20 and 21. Low takes the cheapest measured unit, mid the measured mean, high the dearest, with the swaps chat 12 named for a page-like view.

| Unit | Measured (chapter: bytes) | Low / mid / high used |
|---|---|---|
| A rule's words and frames outside its plates (and outside the kit styles charged to the chapter) | 16: 7,374; 20: 9,001; 21: 6,931 | 6,726 / 7,769 / 9,001 (low is chat 10's 6,726) |
| A failure plate (each chapter's mean) | 16: 3,695; 20: 5,765; 21: 4,807 | 3,695 / 4,756 / 5,765 |
| A full-length web page frame (each page's mean over its six frames) | home 34,363; article 16,453; Act page 32,143 | 16,453 / 27,653 / 34,363 |
| Atlas page frames, for reference | 390 px 24,717; 1440 px 28,028; the Register 77,608 | not used |
| A renderer's style, once | web-site 65,032; plate 2,296; share-image 2,340; favicon-set 2,011; atlas-page 75,794 | 2,011 / 29,495 / 75,794 |
| A detail plate (chapter 21's plates of crops only) | 11 plates, 9,184 to 44,243 | 9,184 / 21,022 / 44,243 |

| Chapter | Allocation | Low | Mid | High | What moves it |
|---|---|---|---|---|---|
| 22 Newsletter and email | 277,000 | 277,237 | 406,713 | 902,117 | The working email as three page frames (82,959 mid), its renderer's style (29,495 mid), four detail plates (84,088 mid). High: the email in both themes and Substack's eight parts as page frames at the dearest unit |
| 23 Social and video | 743,000 | 694,451 | 912,335 | 1,333,134 | The 12 profiles as page frames (197,436 mid at the article's 16,453), the style and four detail plates; failure plates cheaper. High: profiles at the mean page frame and every post with its feed twin |
| 24 Reports | 338,000 | 256,883 | 307,911 | 515,638 | Failure pages at 4,756 against 11,355. High: the reader's 12 pages at the full print unit and its controls as heavy as the largest renderer style |
| 25 Print and presentation | 214,000 | 193,264 | 235,876 | 343,040 | Two detail plates; failure plates cheaper. High: print and slide plates half again heavier |
| 27 and 28 (Phase 5) | 200,000 each | 150,000 each | 200,000 each | 400,000 each | No sample. Chapters 19 (174,313) and 17 (394,285) bracket them |
| **All six** | **1,972,000** | **1,721,835** | **2,262,835** | **3,893,929** | |

Beside chat 12's: its mid was 2,080,043 and its high 3,843,295. Most of the 182,792 between the two mids is two prices. Chat 12 priced a renderer's style at 15,000 and a detail plate at 10,000 at mid, without naming the measure; today's means are 29,495 and 21,022. At chat 12's two prices my mid would be 2,101,581. My recommendation stays chat 12's: keep G3-07's allocations in the build until each chapter is placed and measured, and show the mid and high totals beside the projection.

The units for chapter 16 change on the final page, once A21's frames are placed (its renderer's style joins the style unit and its frames give a video-frame unit for chapter 23's four shared video frames).

## Routine calls

The main session numbers these.

- D4-xxx (M1) | The projection reported two ways: as `gates()` computes it, which is what the build prints, and with only chapter 16 held, chat 12's convention | With 4a or 2a, chapters 20 and 21 fall under their allocations and the build holds them, which chat 12's table did not show
- D4-xxx (M2) | 3c's favicon group takes the tab frames only (light and dark tab), as chat 12 defined it; the ico and app icon drawings stay inline | Keeps the option as defined; those identity drawings were never in it (with them, 3c saves 61,811)
- D4-xxx (M3) | 3d covers text and quoted attribute values, and `&#x27;`, the spelling today's page uses, beside `&#39;` | The parser reads the same value in both places; the non-browser parse check found the same document
- D4-xxx (M4) | Option 2 picks frames by key: `1440-light`, `1440-dark`, `1024-light` and the openers' `1440-light-screen`, for an application that also has a 390 or 360 px frame; crops stay | Reproduces chat 12's three sets; 2a counts 26 today against chat 12's 25, the new one chapter 21's opener at 1440 px
- D4-xxx (M5) | 1b's mid takes the measured mean for every unit, the renderer's style and the detail plate included | Chat 12 named no measure for its 15,000 and 10,000; the figure at those prices is given beside
- D4-xxx (M6) | 3i built as a variant page as well as measured: each part found by computed style in Chromium, found again in the source by tag name and index, and cut | Source bytes in place of serialized markup; all 268 parts matched
- D4-xxx (M7) | 4a's and 4c's loaders write the document back at load (the frames' pictures, the links' `href`), and remove their carriers | After load the page is the same document as today; 4c writes at load where chat 12 wrote "when clicked", a difference of a few tens of bytes
- D4-xxx (M8) | pyoxipng 9.1.1 (oxipng's bindings, for 3b) and html5lib 1.1 (for a non-browser parse check) installed in my scratch folder only | The container had neither; nothing installed system-wide or in the repository

## Done

- **C11C-W1 (measured again, opening page):** every option in 3.7 rebuilt as a script on a strict build of my copy and measured: 1a, 1b with chapters 16, 20 and 21's units, 2a to 2c, 3a to 3e, 3i, 4a, 4c, and C1, C2 and C3 with each projection against 16,000,000. Table above. Nothing landed.
- **PR-S7 (3i, opening page):** measured by computed style in Chromium and built as a variant: 81,031 bytes (chapter 20 22,289; chapter 21 58,742), against chat 12's 65,323. The frames have grown since.
- **The scripts:** one command reruns all of it on the final page (`run.sh`), with the proofs behind `--proof`.

## Requests

1. `work/build/scripts/phase-2/guide_build.py`, `weigh()` (Engineer W's file this chat, or the main session): the last section ends at `page.find("</main>")`, which today finds a `</main>` inside chapter 20's first web frame (the frames carry their own page's `<main>`; the page has 70). So the proofs appendix, 140,940 bytes, weighs 0 and counts in no part of the weight report. The page's total and the projection are right, since both read the whole page. Fix: `page.rfind("</main>")`, or the `</main>` after the last section.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| C11C-W1 | Register, chat 12 section; this file | The page's weight: `guide_charts.py` (`IN_PROGRESS`, the allocations) and the chapters each option touches | The build projects 16,476,174 bytes, 476,174 past 16 MB | C1 (1a, 3a, 3b, 3c, 3d): 15,519,541 with nothing a reader loses; hold 3e and 4a as chat 12 advised | DR-271: the room for chapters still to come is Dustin's call, and 3a, 3b, 3d, 3e and 4c reach approved chapters' output | Held for Dustin (Phase 4 board 1); the final page's table follows |
| PR-S7 | Register, chat 12 section | The kit's frame step; chapters 20 and 21's frames | 81,031 bytes of the frames are parts no reader meets | Strip them in the frame step and keep them in the exports | Measured only, for board 1 | Held for Dustin (Phase 4 board 1) |
| C1's pixel proof and 3d's document identity | Brief 3.7 | The final page | Not yet run | `bash scripts/run.sh <final page> final --proof` | The brief runs them once, on the final page | Waits for the final page |
| The appendix's weight | Found here | `guide_build.py`, `weigh()` | The proofs appendix weighs 0 in the weight report (Requests, item 1) | `page.rfind("</main>")` | Not my file; I land nothing | Requested |

## Tested

- Strict build of my copy under the lock, 00:03:42 to 00:03:58 UTC: exit 0, no warnings, no stale plate, 14,395,945 bytes, 409 rules, 766 specimens.
- The scripts' weigher against the build report: page bytes and projection the same to the byte (14,395,945 and 16,476,174).
- Every option, combination and overlap built as a whole page in scratch and weighed and projected with the build's own `weigh()` and `gates()` (00:24:19 to 00:26:11 UTC).
- 3b: each of the 13 distinct PNGs decoded before and after (Pillow, RGBA): pixels the same, 13 of 13.
- 3d: the opening page and its 3d variant parsed with html5lib 1.1 (the HTML parsing algorithm, adjacent text nodes read as one): the same document, 257,010 nodes each, SHA-256 50d66644… for both (00:23:37 to 00:23:51 UTC). This is not the Chromium proof the brief asks for on the final page.
- 3e: a character scan of the whole page (markup, scripts and styles, data URIs aside, character references read): no character in the three latin-ext faces' ranges.
- 3i: one Chromium (after `browsers.sh` read "OK to open one", 00:23:07 to 00:23:28 UTC, closed at the end): 268 parts found by computed style in 90 frames, every one found again in the source.
- 3c: seven groups found, no id inside a moved drawing named anywhere outside it.
- `git status`: the only file of mine in the repository is this one.

## Not tested

- C1's pixel proof at 1440 and 390 px (382 plates: every plate 3a or 3c touches) and 3d's document identity in Chromium with scripts off: written (`proof.cjs`, `compare.py`, `domeq.cjs`) and not run; they run once, on the final page.
- 4a's and 4c's loaders were not run in a browser: their bytes are measured, their behaviour is not. 4a's document after load and 4c's downloads are not compared.
- 3c's drawings by `<use>` are not proved on this page; C1's proof covers them on the final page.
- 3i's variant is not proved on screen.
- 2a to 2c's lines naming the export files are placeholder words for measuring, not the editor's, and their links are not tested.
- 1b is arithmetic on measured units: no plate of chapters 22 to 25, 27 or 28 was drawn.
- Whether any script reads a plate's own `<style>` (which 3a would drop for 452 plates) was not checked; the pixel proof will not show it either.
