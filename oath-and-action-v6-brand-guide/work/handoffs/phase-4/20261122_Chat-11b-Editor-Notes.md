# Chat 11b editor notes

Editor, chat 11b, November 22, 2026. Brief: `work/handoffs/phase-4/20261122_Chat-11b-Brief.md`, section 5.1. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/d65811ca-3324-52ca-92e9-a6b33b098503/scratchpad/c11b/editor/`. Started 15:34:20 UTC (`date -u`).

## Words for the engineer

Written 15:35:29 UTC (`date -u`). Rule 18.6 in `work/build/scripts/phase-2/stage_c_ch18_build.py`, the block under `# ---- 18.6 Masthead and phone menu`. Three fields change for DR-316 (AL11-1). Type each new text in place of the old, keep the file's curly quotes and apostrophes as printed here, and split the Python string lines wherever suits. Comment `# DR-316 (AL11-1)`.

### 1. `rule=`, first paragraph, its second sentence

Old (the string runs across two source lines, joined here):

```
The link to the part the reader is in carries <code>aria-current="page"</code>, bold words and a 2 px underline.
```

New:

```
The link to the part the reader is in carries bold words, a 2 px underline and aria-current: <code>aria-current="page"</code> on that part’s own front page, and <code>aria-current="true"</code>, which a screen reader announces as “current”, on the pages inside it.
```

The sentences before and after it stay as they are.

### 2. `specs=`, the row `L_ST` (printed as “States”), its first sentence

Old:

```
Current part: bold words, a 2 px underline and aria-current.
```

New:

```
Current part: bold words, a 2 px underline and aria-current, “page” on the part’s own front page and “true” on the pages inside it.
```

The rest of the row (“Hover: a 1 px underline. Menu closed or open, …”) stays.

### 3. `specs=`, the row `L_HEAR` (printed as “A screen reader hears”)

Old:

```
The navigation and its name on entry; “current page” on the current part; on Menu, “collapsed” or “expanded”, and once it opens, the dialog’s name.
```

New:

```
The navigation and its name on entry; on the current part, “current page” on its own front page and “current” on the pages inside it; on Menu, “collapsed” or “expanded”, and once it opens, the dialog’s name.
```

### Fields read and left alone

- `rule=`, second paragraph: “Focus moves to the current part’s link” holds for either value, and the code set's script finds the link by `[aria-current]`, which matches both.
- `specs=`, `L_KEY`: “with focus on the current part’s link” holds for either value.
- `anatomy=`: names “the current part’s 2 px underline” and no attribute. `stage_c_ch18_anatomy_build.py`'s masthead key, row 5, reads “Current part” and “Bold, with a 2 px underline”, with no attribute; neither changes.
- `code_caption=`, `code_alt=`, `builders=` and `failure=`: none names `aria-current`.
- Rule 18.7 (Location list) lists the values “page”, “location” and “step” for its own lists. DR-316 names Rule 18.6 only, and Rule 18.7's lists never mark a section that holds the page, so 18.7 stays.

### DR-317 (AL11-2): no words change

Rule 18.6 has no specification row on the open menu's scroll. Its rule text already says “A masthead that sticks to the top of the page sets scroll-padding-top to its own height, so no focused element hides under it”, its basis already cites WCAG 2.2 SC 2.4.11, and its “Browser support” row already lists `scroll-padding` and `sticky`. The dialog's new padding follows the rule's own principle and contradicts none of its words, and DR-317 names the code alone. Type nothing for DR-317.

## Routine calls

- D4-xxx | Rule 18.6 needs no new words for DR-317 | It has no specification row on the open menu's scroll; its rule text already asks a sticky masthead for scroll-padding-top, its basis cites SC 2.4.11 and its "Browser support" row lists `scroll-padding` and `sticky`; DR-317 names the code alone
- D4-xxx | Rule 18.7's list of aria-current values ("page", "location", "step") stays | DR-316 names Rule 18.6 alone, and 18.7's lists never mark a section that holds the page
- D4-xxx | DR-313's 152 px is the figure built: the 16 px master draws a 152 by 16 CSS px box at 16 px tall; its ink spans 152 px at 1x and 151.5 CSS px at 2x, and its path reaches 151.17 of the viewBox's 152 units | The row prints the box width, as Rule 03.4 and the minimum sizes table print "152 px wide" for the same master; no difference to report
- D4-xxx | After the identity chain ran, five files it rewrote beyond chapter 03 went back to their prior bytes: `s-04-1-correct`, `s-09-3-correct`, `s-09-3-failure` and `s-17-hinge-failure` from my copies taken before the run, and `work/boards/phase-2/stage-a/proofs/20261110_Letterhead-Proof.html` from its committed bytes (`git show HEAD:<path> > <path>`, no checkout) | The four specimens' base64 PNGs re-encoded pixel-identical (checked, 0 pixels differ in all 9 images) but 72 to 1,240 bytes larger, and the letterhead proof picked up today's tokens; DR-313 names chapter 03's row alone. The rewritten copies are kept in scratch, `identity-run-side-effects/`
- D4-xxx | DR-318's filter is its own rule, `.ed .ph{filter:grayscale(1)}`, added through `PH_BW` to the three plates' style alone, and `PH` stays as it was | `PH` also styles `s-01-6-failure`, `s-01-7-correct` and `s-01-7-failure`, which hold no photograph; the rule there would add bytes that draw nothing
- D4-xxx | The swatch labels "Newsprint, 60 to 85 percent" in `s-05-palette`, chapter 05's opening figure and `s-05-1-failure`'s alt stay | They give the share across a body of work, which Rule 05.1's second paragraph keeps; DR-312 names the row alone, and Rule 05.1's rule text already carries the long-page exception (DR-310), so the row now agrees with it
- D4-xxx | DR-312's run left `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json` with one change, its capture date | An output `stage_a_systems_build.py` writes (brief section 4); every measured figure held, so chapters 06 and 07 and all 56 systems specimens kept their bytes

## Done

Each time below is a `date -u` value read in the same command.

1. **Words for the engineer**, written 15:35:29 UTC, the section above. Three fields of Rule 18.6 for DR-316; none for DR-317.
2. **DR-312**, Rule 05.1's row "Newsprint in each view": `work/build/scripts/phase-2/stage_a_systems_ch05.py`, comment `# DR-312 (ED11-1)`. Rebuilt through `stage_a_systems_build.py` probe (15:36:30), `stage_a_systems_capture.js` (15:36:34 to 15:36:39, 55 results) and final (15:36:42), each under the lock, into scratch `sys/`.
   - Original: "60 to 85 percent"
   - Revision: "60 to 85 percent; on a long page, screens of running text between the opening screens may hold more"
3. **DR-313**, Rule 03.6's new row after "Site, under 48em": `work/build/scripts/phase-2/stage_a_identity_chapters.py`, comment `# DR-313 (ED11-2)`. Rebuilt with `stage_a_identity_build.py` (15:37:57, under the lock), the script that imports it and writes chapters 03, 04, 08 and 09; then five side-effect files restored (routine calls).
   - Revision: label "Site, under 24.375em", value "L1 from the 16 px master, 152 px wide". No token, since the row names no target size.
4. **DR-314**, Rule 01.22's rule sentence: `work/build/scripts/phase-2/guide_editor_ch01.py`, comment `# DR-314 (DD11-NF1)`.
   - Original: "An Act piece labeled “Act · How to take part” gives one step with its date and place, sets out what supporters and opponents have said at the same length, and takes no side."
   - Revision: "An Act piece labeled “Act · How to take part” gives one step with its date and place, sets out what the record shows from each side, at the length the record holds, and takes no side."
   - Rule 01.22's other fields (its Why, caption, alt, specifications, builders) never say "at the same length"; nothing to report inside the rule. Chapter 13 restates the old wording: "Not fixed", ED11B-1.
5. **DR-318**, the three photograph plates in black and white: `guide_editor_ch01.py`, comment `# DR-318 (C16-CD-01)`. `PH_BW = PH + ".ed .ph{filter:grayscale(1)}"`, used by `s-01-6-correct`, `s-01-8-correct` and `s-01-8-failure`. Before styling, I checked the class: on the built page `class="ph"` sits on these three images alone, and every specimen's style is wrapped in `@scope ([data-specimen="…"])`, so the chapter 14 element `div.fr.ph` and chapter 16's `sx-ph` sit outside its reach. Each plate grew 28 bytes, the rule itself; the page's one copy of each photograph (`<style id="oa-photos">`, 489,462 bytes) is byte-identical before and after.
6. Chapter 01's chain ran as one locked command, `guide_editor_build.py` then `stage_b_identity_ch01.py` (15:41:33 to 15:41:34). The editor build's own checks passed: locked lines exact (tagline 11 uses, mission 6, promise 6, commitment 6), no em dash, no listed filler or corporate word, every Illustrative plate labeled.
7. **Proof**, below under "Tested".

### Bytes, before and after

| Chapter | JSON file before | after | Section of the built page before | after |
|---|---|---|---|---|
| 01 Purpose | 55,140 | 55,150 (+10) | 674,761 | 674,855 (+94: 3 × 28 for the style, +10 for the words) |
| 03 Identity | 27,011 | 27,118 (+107) | 462,527 | 462,647 (+120, the row's markup) |
| 05 Color | 34,524 | 34,607 (+83) | 241,038 | 241,121 (+83, the added words) |

The whole page went from 13,080,604 to 13,083,858 bytes; my three chapters account for 297 of the 3,254, and the rest is the engineer's work in progress on chapters 18 and 20 and their site styles, which was in the tree when I built, plus the proofs appendix's build time.

## Requests

None. The engineer's notes say the words landed at 15:35:29 UTC and will be typed after the code; at 15:45 UTC they were not yet in `stage_c_ch18_build.py`.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| ED11B-1 | Editor, chat 11b, word search after DR-314 | Rule 13.12, rule text, second paragraph (`work/build/scripts/phase-3/phase3_ch13_build.py`, line 1716; `13-evidence.json`, `rules[11].rule[1]`) | It reads "An Act piece quotes each side at the same length (Rule 01.22)", the wording DR-314 replaced in Rule 01.22; the two rules now disagree where the record holds one side (DR-93) | "An Act piece sets out what the record shows from each side, at the length the record holds (Rule 01.22)" | Chapter 13 is approved at Gate 3 (brief section 2), and DR-314 names Rule 01.22 alone | Open, for Dustin |
| ED11B-2 | Editor, chat 11b, read of Rule 03.6 after DR-313 | Rule 03.6, rule text, first paragraph, and the row "Site, under 48em" (`stage_a_identity_chapters.py`; `03-identity.json`) | The rule text says "Under 48em, it sets L1 from the 24 px master beside the menu button", and the row "Site, under 48em" gives the 24 px master, while the new row gives the 16 px master under 24.375em; a reader who stops at the rule text misses the narrower step | Rule text: "Under 48em, it sets L1 from the 24 px master beside the menu button, and under 24.375em, 390 px, from the 16 px master." Row label: "Site, from 24.375em to 48em" | DR-313 names the new row alone | Open, for Dustin |
| ED11B-3 | Editor, chat 11b, read of Rule 03.6 after DR-313 | Rule 03.6, "Files" (`stage_a_identity_chapters.py`, `files=`) | The new row cites the 16 px master, and the rule's file list names the 24 px master and leaves out `wordmark/20261028_Wordmark-16px-Master.svg` | Add `A + "wordmark/20261028_Wordmark-16px-Master.svg"` after the 24 px master | DR-313 names the new row alone | Open, for Dustin |

## Tested

- **Strict build, before**, under the lock (15:35:56 to 15:36:09 UTC): exit 0, 0 warnings, 13,080,604 bytes, 393 rules, 731 specimens, matching the brief's figure for cb332f40.
- **Strict build, after all four changes**, under the lock (15:41:52 to 15:42:32 UTC): exit 0, 0 warnings, 0 stale, 13,083,858 bytes, 393 rules, 731 specimens. Report: scratch `guide-after-Build-Report.json`.
- **`git diff --stat` for my work**: `stage_a_systems_ch05.py` (+5 −1), `05-color.json` (1 line), the measurements file (its date), `stage_a_identity_chapters.py` (+2), `03-identity.json` (+4), `guide_editor_ch01.py` (+10 −5 over DR-314 and DR-318), `01-purpose.json` (1 line), `s-01-6-correct.html`, `s-01-8-correct.html` and `s-01-8-failure.html` (1 line each). Chapters 02, 04, 06, 07, 08, 09, 12 and proofs, every other specimen and the four manifests these chains write (editor, identity-ch01, identity and systems) kept their bytes. The other modified files in the tree (chapter 18's code, keys and anatomy, `18-components.json`, `stage_c_ch18_build.py`, the two app-kit renderers) are the engineer's.
- **Built-page diff**, before against after, by chapter: 01 has 4 changed places (the three plates' styles and Rule 01.22's sentence), 03 has 1 (the new row), 05 has 1 (the row's value); the rest sit in chapters 18 and 20, the head's site styles (the engineer's) and the proofs appendix's build time.
- **Word search of the after page** (no-break spaces before "px" read as spaces):
  - "60 to 85 percent; on a long page, screens of running text between the opening screens may hold more": 0 before, 1 after, in Rule 05.1's specifications. The bare row value "60 to 85 percent" is gone from that row; the one left is the swatch label in `s-05-palette` (routine calls).
  - "Site, under 24.375em" with "L1 from the 16 px master, 152 px wide": 0 before, 1 after, in Rule 03.6's specifications, after "Site, under 48em".
  - Rule 01.22's new sentence: 0 before, 1 after, in chapter 01. "supporters and opponents have said": 1 before, 0 after anywhere on the page.
  - ".ed .ph{filter:grayscale(1)}": 0 before, 3 after, one in each of the three plates' `@scope` blocks and nowhere else.
- **DR-318 captures**, Chromium at 1x, light theme, viewports 1440 by 900 and 390 by 844, each plate's whole figure, from the before and after builds (uptime load 0.14 and 0.70 when the browser opened). Elements with a grayscale filter inside specimens: 21 before, 24 after, the three added being exactly the three plates' `img.ph`. Pixel comparison against each photograph's footprint, placed at the figure's sub-pixel offset:

  | Plate | Width | Changed pixels outside the photograph | Changed inside / footprint | R, G, B spread inside, before → after |
  |---|---|---|---|---|
  | s-01-6-correct | 1440 | 0 | 213,357 / 216,961 | 133 → 10 |
  | s-01-6-correct | 390 | 0 | 51,283 / 52,038 | 120 → 10 |
  | s-01-8-correct | 1440 | 0 | 235,233 / 241,001 | 185 → 10 |
  | s-01-8-correct | 390 | 0 | 56,705 / 57,918 | 178 → 10 |
  | s-01-8-failure | 1440 | 0 | 235,233 / 241,001 | 185 → 10 |
  | s-01-8-failure | 390 | 0 | 56,703 / 57,918 | 178 → 10 |

  The 10 left is the footprint's edge row, where the photograph blends into Newsprint (220, 217, 210); one pixel in from the edge the spread is 0. A first pass that placed the box at whole pixels counted 353 to 400 changed pixels in column 696 at 1440 px; they lie inside the photograph's rows and turn from photo color to neutral gray, the photograph's own right edge at 696.656 px, and the corrected pass above counts them inside. Captures: scratch `dr318/before-*.png` and `dr318/after-*.png`; contact sheet `dr318/contact-390.png`, which I looked at.
- **The 16 px master's width**, rendered in Chromium at 16 px tall: box 152 by 16 CSS px; ink 152 px at 1x, 151.5 CSS px at 2x; path extent 151.17 of 152 viewBox units.
- **Script check of my words** for em dashes and the listed words: results under "Pattern count".

## Not tested

- Rule 18.6's new words in the built page: the engineer types them, and they were not in `stage_c_ch18_build.py` when I last looked (15:45 UTC).
- What a screen reader says for `aria-current="true"`: the words follow WAI-ARIA 1.2 and the accessibility lead's reading in AL11-1; I ran no screen reader.
- DR-318's plates in Night Edition, a forced-colors theme, at 2x or in print; the captures cover 1x and the light theme only.
- The guide check, which the main session runs at the close.
- Chapter 20's own masthead against the new Rule 03.6 row; chapter 20 belongs to the engineer's run.

## Pattern count

Script check run at 15:47:19 UTC over the seven texts that will print in the guide (Rule 18.6's three replacements, which I wrote, and the DR-312 to DR-314 texts, which are Dustin's, printed word for word) and over this notes file: em dashes 0; genuinely, really, truly, actually 0; leverage, underscore, reflect 0; very, just, simply 0. My own read of the three Rule 18.6 texts against chapter 02's rules found no antithesis, corrective negation, matched pair, setup and payoff, slogan close, hedge or stacked noun phrase. "Bold words, a 2 px underline and aria-current" lists three facts the rule already listed in another order; it is a list of what the link carries, and no rhetorical run. Pattern violations remaining in my words, by type: 0 for each type.

Terms: Rule 18.6 already defines the navigation landmark at first use; Rule 18.7's Why explains aria-current ("lets a screen reader say where the reader is"), and the new words say what the value "true" makes a screen reader say. Rules 18.5 and 18.6 use the term before 18.7 explains it; that order predates this chat and my words leave it as it was. DR-313's "24.375em" follows Rule 03.6's own em switch, which its rule text defines ("768 px at the default text size") and ED11B-2 would extend to 390 px.
