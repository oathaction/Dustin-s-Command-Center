# Phase 4 allocations, re-sized from the application kit's measured bytes

Written November 21, 2026 by the engineer, chat 10 (brief section 9, Job 2). The figures below are in `work/build/scripts/phase-3/guide_charts.py` as `PHASE_4_ALLOCATION`, with the Gate 3 report's figures kept beside them as `PHASE_4_GATE_3`. Nothing was cut to fit them, and only the page's 16 MB stops a build (DR-271).

## 1. What the kit measured

The application kit drew the design director's three studio samples (`work/handoffs/phase-4/20261121_Kit-Sample-Specs.md`) from their content files, at build time, into static markup. I placed each sample as a plate in a copy of today's guide (as the only specimen of a fixture chapter 20, 23 or 24), built that copy, and read each plate back as the page places it, frame and label included. I counted the parts that the guide's page already carries (the fonts, `tokens.css`, the chart kit's style and the sprite) once for the page, as the page does, and not again in a plate.

| Sample | Placed, with its frame | What it holds |
|---|---|---|
| Instagram portrait post, 1080 by 1350 px | 11,696 bytes | Its style (2,484), the post at true size in a scaled frame with its safe-area overlay (4,192), the same post at the 390 px a phone's feed shows it (3,657), the safe-area switch and the guide's frame |
| Article page at 1440, 1024, 390 and 360 px, light and dark | 187,145 bytes | Its style once (12,960, with chapter 18's theme switch style), then eight frames of about 21,530 each: the whole page at its width, of which chart S86 (its two drawings, words and table) is 11,570 |
| Report page 3, US Letter with bleed | 11,355 bytes | Its style (4,573), the sheet at 96 px to the inch with its overlay (5,361), the switch and the guide's frame |

The kicker's Civic Line symbol (CL-031) adds nothing: the guide's sprite already holds it. The photographs add nothing to any chapter: the page carries each once (489,462 bytes, its own part).

Two figures from today's page complete the method. A rule's words and frames, outside its plates, weigh 6,726 bytes at the median of chapters 01 to 19 (chapter 14 aside, which carries the chart kit; the mean is 9,994, pulled up by chapter 26's token table). And the ordinary plates in the built chapters nearest Phase 4 in kind run 5,083 to 9,987 bytes at the median (chapters 12, 13, 08, 11, 17 and 18), so the artboard plate measured here, 8,039 bytes without the feed-size twin, sits inside that range.

## 2. The method

Each chapter is the rules the Gate 3 report expects, at 6,726 bytes each for their words and frames, plus every plate it will draw, counted from the Gate 3 report's section 9 tables and priced at the measured unit nearest it:

| Unit | Bytes | From |
|---|---|---|
| An artboard plate (a post, cover, banner, avatar, slide or a failure plate) | 8,039 | The social post as placed, less its feed-size twin |
| A smallest-size twin (an avatar or thumbnail at the size its platform shows it) | 3,657 | The post's feed-size frame |
| A web page at 4 widths in 2 themes | 187,145 | The article, as placed |
| A web frame with a figure / without one | 21,530 / 9,960 | The article's frames; the figure is 11,570 |
| A print page (a report page, explainer, letterhead, poster or sign) | 11,355 | The report page, as placed |
| A page inside the report reader | 5,361 | The report page's frame, the style shared |
| A chart figure | 11,570 | S86 as the article carries it |

Every rule counts one failure plate at the artboard unit (a report rule at the print unit), since most failures show one application with its fault. Each count assumes the larger reading where section 9 leaves room, and avatars and favicons count at the full artboard unit though they draw less, so the figures lean high.

## 3. The seven chapters, re-sized

| Chapter | What it counts | Re-sized | Gate 3 | Change |
|---|---|---|---|---|
| 16 Photography, illustration and video | Built today at 213,681 bytes (the design director's 02:21 build, before the editor's words); held at its allocation so the words have room | 300,000 | 300,000 | 0 |
| 20 Web | 10 rules (67,260); home, article and Act pages, each at 4 widths in 2 themes (561,435); desktop and mobile mastheads in 2 themes (32,156); share preview and favicon set (16,078); 10 failure plates (80,390) | 757,000 | 500,000 | +257,000 |
| 21 The atlas | 16 rules (107,616); home, detail, evidence and loop views, each at 1440 and 390 px in 2 themes with a figure in every frame (403,008); typed ID chips and the system test (16,078); 16 failure plates (128,624) | 655,000 | 460,000 | +195,000 |
| 22 Newsletter and email | 10 rules (67,260); Substack's 8 parts (64,312); one chart in a post (12,570); the working email at 600 and 375 px and with images off (44,512); share preview (8,039); 10 failure plates (80,390) | 277,000 | 300,000 | −23,000 |
| 23 Social and video | 20 rules (134,520); 52 artboards: X 6, Threads 4, Instagram 9, YouTube 5, TikTok 4, LinkedIn 8, each profile as a reader meets it at desktop and phone 12, the shared video frames 4 (418,028); 8 smallest-size twins (29,256); 20 failure plates (160,780) | 743,000 | 660,000 | +83,000 |
| 24 Reports | 13 rules (87,438); the reader with all 12 pages at full size (69,902); 2 charts (23,140); the reader's controls, 10,000, **assumed, not measured**; 13 failure pages (147,615) | 338,000 | 450,000 | −112,000 |
| 25 Print and presentation | 9 rules (60,534); explainer, letterhead, poster and table sign (45,420); slide cover, content and data with its chart (35,687); 9 failure plates (72,351) | 214,000 | 340,000 | −126,000 |
| All seven | | **3,284,000** | 3,010,000 | **+274,000** |

Chapters 20 and 21 grow most, as the Gate 3 report expected: a full web page costs about 21,500 bytes a frame, and they draw many. Chapters 24 and 25 shrink, since a print page as the kit draws it costs less than the chapter-17 rate the Gate 3 method gave them.

## 4. The page against 16 MB

| Part | Bytes |
|---|---|
| Today's page, strict build at 02:24 UTC, chapter 16 in place | 12,233,841 |
| Chapter 16 held to its allocation | 86,319 |
| Chapter 15 held to its allocation | 29,899 |
| Phase 4's six chapters still to build, re-sized | 2,984,000 |
| Phase 5's two chapters (27 and 28) | 400,000 |
| **Projected page** | **15,734,059** |
| Under the 16 MB limit (the reserve) | 265,941 |
| Past the 15.5 MB line | 234,059 |

The build prints the projection past 15.5 MB as a note marked "early warning" and passes a strict build, as the Gate 3 report has it ("the build reports and does not stop on", DR-271); the page itself past 16 MB still stops the build. The line stays at 15.5 MB. Chapter 27's 200,000 bytes must also index every export Phase 4 makes (11 files so far, listed in `work/build/exports/phase-4/20261121_Phase-4-Exports-Manifest.json`).

## 5. What would move these figures

- The web chapters' frames carry the whole page each time. If chapter 20 shows its dark mode at 1440 and 390 px only (as section 9's check table words it) and its light mode at all four widths, each page plate drops from 8 frames to 6, about 43,000 bytes less a page. That is a design choice for chapter 20, not a cut, and these figures do not assume it.
- Plate styles here repeat in every plate. A chapter that shares one plate style, as chapter 15 does, saves 2,500 to 13,000 bytes a plate.
- The report reader's controls (10,000 above) are not measured; chat 15 measures them.
- Each allocation moves as its content needs; only the 16 MB stops a build.

## 6. Where the measures came from

- Plates: `node work/build/app-kit/oa-app.mjs build --all`, then a fixture build of today's guide with the three plates added, read back as placed (scratch: `.../scratchpad/c10/engineer/measurefx/`).
- Rules' words: today's strict build, each chapter's bytes with every plate taken out, divided by its rules.
- Projection: `guide_charts.gates()` on the strict build above.
