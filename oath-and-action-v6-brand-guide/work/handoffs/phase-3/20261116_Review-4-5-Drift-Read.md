# Review of rounds 4 and 5: drift read

Oath & Action Edition 06, Phase 3, chat 7, November 16, 2026. Reader: drift read (codes DF), adopting `oa-editor.md` for words and `oa-design-director.md` for marks. Brief: `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md`. Started 16:34 UTC; this draft written 16:44 UTC.

Status: in progress. Findings are added as the read goes.

Method: every word was read by script from the built page (`c07/main/guide.html`, 12,107,102 bytes), split into 41,000 located text units (chapter, rule, plate, element), from the chapter JSON files and from the specimen sources. Marks were read from the specimen sources' CSS and markup and from the shared capture set. Scripts and outputs sit in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/review/drift/`.

Which text governs: chapter 02's writing section for words (DR-73); for everything else the chapter Dustin approved first. Chapters 01, 05, 11 (Rules 11.1 to 11.9 and 11.13 to 11.18), 12 and 18 were approved at Gate 2 (G2-01 to G2-04, November 11), with the bill tracker's marks set by DR-108; chapter 13 by DR-237 and DR-242; the chart notes' ink words by DR-262 on board 2.

## 1. Score

Pending.

## 2. Must fix

**DF-1. Rule 15.23's own correct plate calls the law's stages "steps" in two of its five blocks.** Where: `s-15-23-correct`, the records request block and the agency rule block. Rule 15.23 sets the two words apart: "A tracker gives a reader six steps to follow, and the law behind it sets its own stages." The plate then heads the records block "A federal request’s steps in the law, behind the tracker’s six steps" and the rule block "The law’s steps for a federal rule, behind the tracker’s six steps", while its ballot and court blocks say "A citizen initiative’s stages in four states’ constitutions" and "A federal civil case’s stages in Title 28". A reader learning step against stage from this plate is taught both. Governs: Rule 15.23's words, which follow chapter 02's H02 (keep the same term after its first use). Fix: "A federal request’s stages in the law, behind the tracker’s six steps" and "The law’s stages for a federal rule, behind the tracker’s six steps". Owner: the systems designer in `phase3_ch15_build.py`, the editor reading.

**DF-2. A filled, numbered square means "stopped" in chapter 11 and "a stage every bill passes" in Rules 15.22 and 15.23.** Where: `s-15-22-correct` (`.wf .n`, a 22 px square in the subject ink with its number in the surface color) and `s-15-23-correct` (`.wq`, a 20 px square drawn the same way), against Rule 11.2's "Stopped: A filled square 2 px narrower than the circle, in its place; the line ends there" and Rule 11.3's "A bill that stops ends its line on a square", the mark DR-108 approved ("a bill that stops ends its line on a square"). Rule 11.10's plate draws Measure 99013 stopped at step 3 as exactly this mark, a white 3 on a filled square. Rule 15.22's text then uses a square a third time: "End a path that stops on a small square, as a tracker ends a bill that stops (Rule 11.3)", drawn as a 10 px filled square (`.sqm`). So one plate draws "a stage on the main path" and "a path that ends" with the same shape at two sizes, and Rule 15.23 sets those stage squares in one table beside the tracker's step numbers, where a reader of chapter 11 reads a filled square as a stop. Governs: chapter 11, Rules 11.2 and 11.3 (Gate 2; DR-108). Fix: keep the square for a stop alone. Draw 15.22's stage numbers in a shape no tracker uses, such as the 14.96 process diagram's numbered box with an edge in the text's ink (approved on board 2), filled for the spine and outlined for the side paths, or a plain bold number on the line; keep the small filled square for "a path that stops", which then matches Rule 11.3's meaning; carry the same shape into 15.23's stage column. Owner: the systems designer with the design director; shown on board 3 because it changes how Route FS reads.

## 3. Should fix

**DF-3. Rule 14.142's plate names its two drops "in the strongest ink" where every approved chart note says "in the text's ink".** Where: `s-14-s96` (five places: the reading guide, the alt, the named-columns line, the key, the phone note) and `s-14-142-failure`'s alt. Quoted: "the two in the strongest ink are the drops past the margin". The approved notes say, for example, "The 118th Congress, which the title names, is drawn in the text’s ink; the other nine are gray." (S17) and "Social Security, the tile the title names, takes the text’s ink; every other tile is gray" (S47). Governs: the ink words Dustin approved on board 2 (DR-262, "the twelve charts' ink words"), set as one word by D3-914. Fix: "the two in the text’s ink are the drops past the margin", and "Two are drawn in the text’s ink and labeled" in the alt. Owner: the complex examples maker in `phase3_ch14_complex_build.py` and S96's spec, the editor reading.

**DF-4. Rule 15.22's key names its lines "dark" and "lighter", the two words D3-914 retired because they swap on Charcoal and in forced colors.** Where: `s-15-22-correct`, key and alt: "A stage every enacted bill passes, in order, on the dark line", "What can follow the law, on the lighter line", "The stages every enacted bill passes sit on a dark line in filled squares; the other paths and what follows the law are in a lighter ink"; and Rule 15.22's own text, "on one dark line in filled squares, and the paths that leave it in the lighter context ink". On the Charcoal stage the spine draws in Newsprint, the light line. Governs: DR-262 and D3-914 (a named mark "in the text's ink", other marks "gray"). Fix: "on the line in the text’s ink" and "on the gray line", in the key, the alt and the rule. Owner: the systems designer, the editor reading.

**DF-5. Rule 15.24's cards start sentences with figures under ten, beside the same counts in words.** Where: `s-15-24-correct`, the line under each route card (`p.rcn`). Quoted: "7 reform entries name this route; the atlas checked one of them, on October 15, 2026." beside "What it depends on, and its seven entries"; also "6 reform entries", "5 reform entries", "4 reform entries", "3 reform entries", while one card reads "One reform entry names this route". The plate's alt adds "1 entries, 0 checked." Governs: chapter 02's H06 ("In prose, write one to nine as words"). Fix: "Seven reform entries name this route", and so on for six, five, four and three; "1 entry, 0 checked" in the alt. Owner: the systems designer in `phase3_ch15_build.py`.

## 4. The twelve named places

Pending. So far:
- 12. Number map: 155 text citations and 160 links to Rules 11.1 to 11.18 read by script, each checked against its rule's subject; no link's words differ from its target, and no stale "Rule 11.1N" was found in any chapter. Loop titles: no loop drawing in chapters 11, 12, 13, 14, 15, 17 or 18 prints a loop chain label in place of a variable's title; chapter 10 keeps "Executive unilateralism" for CL-026.

## 6. Questions for Dustin

Pending.

## 7. Tested

Pending.

## Not tested

Pending.
