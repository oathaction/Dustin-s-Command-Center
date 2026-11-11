# Gate 2 fix pass: the accessibility lead's notes

Oath & Action Edition 06, Phase 2, November 11, 2026. The accessibility lead's part of `20261111_Gate-2-Fix-Brief.md`: chapter 18's words and chapter 19. Both live in their generators, `work/build/scripts/phase-2/stage_c_ch18_build.py` and `stage_c_ch19_build.py`; no output file was edited by hand.

## Items

- [x] **CD-S1 and CD-S10, chapter 18's opener.** The intro's second paragraph drops from eleven lines to two: "The code reads only tokens.css, the file that holds every color, size and type style as a named value, so one copy follows either theme. How each state looks and moves comes from chapter 17." The definitions it carried (accessible name, role, state, status line, ARIA and the APG) open Rule 18.1's "Why it works", as one paragraph ahead of the button's own reason. At 1440 px the opener plate now starts 747 px down and its first row of controls shows on the first screen; before, the first screen ended inside the intro's second paragraph.
- [x] **CD-S3, titles.** 22 of chapter 18's 24 titles and 8 of chapter 19's 9 are now one clause. Chapter 18's average falls from 16.6 words to 9.4, chapter 19's from 15.6 to 9.9; the longest are 18.3, 18.16 and 19.5 at 13 words, each already one clause, kept as written. No rule number changed. Each dropped clause was checked against its rule's text, and every one is already stated there (most in the first paragraph; 18.1's unavailable button opens its second), so nothing was added twice. No file outside the two generators and their outputs quotes a changed title (searched across `work/build`).
- [x] **CD-S2, captions and bars.** No change needed. All 24 failure captions in chapter 18 and all 9 in chapter 19 already lead with "Fails Rule NN.N." in bold, and all 33 failure plates carry the "Failure case: do not publish" bar with its words in `--oa-color-text-primary-on-charcoal`. Every one draws a piece a reader could lift, so none goes without the bar.
- [x] **DT-S10.** Rule 18.22's second paragraph now cites Rule 17.3 for Play becoming Pause and Rule 11.14 for the pace: "…its icon and its word changing together (Rule 17.3), and it holds each step about 250 ms a word and never under six seconds, with reduced motion too (Rule 11.14)."
- [x] **The form's keys path, from the component engineer's `aria-invalid` change.** `KEYS[17]` in `stage_c_ch18_build.py` takes the two changes in `20261111_Gate-2-Fix-Components-Notes.md`, "For the main session", item 1: in "Send with mistakes", typing "name@" now asks that the email field's `aria-invalid` read `"false"`; in "Send right", the Enter step asks `"false"` where it asked for no attribute. The generator now emits `c-18-form.keys.json` byte for byte as the component engineer wrote it, and `--check` reports "chapter 18: current".
- [x] **Rule 18.17's builders**, item 2 of the same section, in these words: "Give each field <code>aria-invalid="false"</code> from the start, and set it back to <code>"false"</code> once the reader fixes it. A field without the attribute takes the browser’s own check, which calls an email address wrong while the reader is still typing it."
- [x] **D2-1722, the guide's own scroll frames (DT-S1's second remedy).** Rule 18.11's second paragraph ends: "This guide sets its plates and code on a light gray mat, where the focus ring’s color measures 2.98 to 1, under the 3 to 1 a ring needs, so a frame that scrolls on the mat draws the same ring in Charcoal, 11.76 to 1." Both figures are computed in the generator from `tokens.json` (the mat is the shell's `--mat`, `oa.color.tint.stoneN90`), so `palette()` now reads tints as well as palette and derived colors; no other output changed.
- [ ] **DT-S12, "Civic Line" in Rule 19.8's results.** The lower-case "civic line" is in round 2's results file, which the plate prints word for word and which stays as that round's record. It lands with call 12: the new results file writes "Civic Line", and the generator gains a check that stops on the lower-case form.
- [x] **Call 8 (DT-S11) in 18 and 19.** No change needed. Every measured ratio already prints with two decimals and "to 1"; the colon forms in chapter 19 are WCAG's own words, quoted, and "3 to 1" and "4.5 to 1" are thresholds.
- [ ] **Call 12, last.** Waiting for the main session's word that the final guide check has run on the fixed preview.

### Plan for call 12

1. Read the main session's final runs: the guide check at four widths, the sprite check and the token tests on the fixed preview, with their result files and times in UTC.
2. Write `work/handoffs/phase-2/20261111_Gate-2-Ch19-Results.json` in round 2's form (`about`, `date`, `build`, `runs`, `tested`, `not_tested`), naming the preview's file, bytes, SHA-256 and build time, with "Civic Line" in the drawings line. Round 2's file stays as its record.
3. Point `RESULTS` in `stage_c_ch19_build.py` at the new file, add the check against "civic line" in lower case, run it, then the strict build into scratch, and look at Rule 19.8's plate at 1440 and 390 px.

## Second pass

DR-191's short second pass, from the editor's read (`20261111_Gate-2-Editor-Notes.md`, "## Fix pass read", rows 6, 8, 9 and 10). Each fix is in the generators.

- **Row 8, Rule 18.7's title (serious).** Now "Show where the reader is with aria-current and a mark that needs no color.", as the editor wrote it: "a visible mark" allowed a mark in color alone.
- **Row 9, Rule 19.6's title.** Now "Keep every word and control when text grows, spacing opens or the screen turns.", as the editor wrote it.
- **Row 10, Rule 18.1's definitions.** The paragraph on accessible name, role, state, status line, ARIA and the APG moves from "Why it works" into Rule 18.1's rule text as its second paragraph, ahead of the unavailable button; "Why it works" keeps only the button's reason. ARIA is now defined before the rule's own aria-disabled.
- **Row 6, Rule 18.11, so the citations to it hold.** The ring sentence now names the gap, and the editor's sentence follows it: "Its focus ring sits inside the frame with its 2 px gap, where the frame’s edge cannot clip it. A control whose neighbor stands too close for an outside ring, such as a tab or a row in a list, draws the same ring inside its own edge, with the 2 px gap, offset −4 px." The scroll region's own CSS already draws its ring at −4 px, so the frame and the tabs, list rows, link rows and Clear button now match their rule.

Checks: both generators run, then `--check`, "chapter 18: current" and "chapter 19: current", with only `18-components.json` and `19-accessibility.json` changed. `guide_build.py --strict` into scratch: 185 rules, 433 specimens, 9,442,558 bytes, and one warning, outside my files: "Rule 26.7: s-26-token-table is not what tokens.json 6.0.0-gate2.9 makes; run token_table_build.py", the engineer's token release waiting on its table. The four fixes read as written in the built page.

## Routine calls

D2-xxx | Chapter 18's definitions of accessible name, role, state, status line, ARIA and the APG open Rule 18.1's "Why it works" | They explain why a native button works, the rule's own reason; in the rule text they would stand before the rule they serve
D2-xxx | A title's dropped clause is not repeated where its rule's text already states it | Every dropped clause was there already, most in the first paragraph; saying it twice would break W07
D2-xxx | Three titles of 13 words (18.3, 18.16, 19.5) stay as written | Each is one clause, and the brief sets about twelve words, past fifteen as the line
D2-xxx | Rule 18.17's title becomes "Give every field a visible label and its own error message." | One clause holding the rule's two parts; moving focus to the first field to fix stays in its first paragraph
D2-xxx | Rule 19.9's title names "real devices" and leaves the four platforms to its text | The four names made it eighteen words; the rule's first sentence and its script name each platform
D2-xxx | The form's keys path asks for `aria-invalid="false"` before Send and after a fix, as the component engineer's code sets it | The keys file is this generator's output, so the path lives here; otherwise the next run would revert it and fail the form's walk
D2-xxx | Rule 18.17's builders name the browser's own check as the reason for `aria-invalid="false"` | A builder who knows why keeps the attribute when rewriting the form
D2-xxx | Rule 18.11's sentence on the mat computes its two ratios from the tokens | A printed figure that reads the token file cannot drift from it
D2-xxx | DT-S12 lands with call 12, in the new results file | The plate prints its results file word for word, and the page and the file must not disagree (Rule 19.8's builders line); round 2's file stays its record

## Tested

- After D2-1722's sentence: `stage_c_ch18_build.py` run, then `--check`, "chapter 18: current", with only `18-components.json` changed; `guide_build.py --strict` into scratch, exit 0, 0 warnings, 185 rules, 433 specimens, 9,441,111 bytes; the sentence read in the built page.

- After the keys and builders changes: `stage_c_ch18_build.py` run, then `--check`, "chapter 18: current"; `guide_build.py --strict` into scratch, 0 warnings, 16 chapters, 185 rules, 433 specimens, 9,439,392 bytes.

- Both generators run, then `--check`: "chapter 18: current", "chapter 19: current". Only `18-components.json` and `19-accessibility.json` changed; the 24 keys files, the 24 failure plates, chapter 19's 19 specimens and the manifests came out byte for byte the same.
- `guide_build.py --strict` into scratch: 0 warnings, 16 chapters, 185 rules, 424 specimens, 9,429,344 bytes (every owner's work as it stood at the build's time stamp, 17:35).
- Chapter 18's and 19's first screens at 1440 px (1x and 2x) and 390 px, Rule 18.1 and Rule 18.22 at 1440 and 390 px, read on screen and as extracted text.
- Title lengths and caption leads by script over both chapter files; every failure plate in 18 and 19 searched for its bar; every file under `work/build` searched for quotations of the old titles.

## Not tested

- Chapter 19's results on the fixed preview: call 12, after the main session's final guide check.
- The editor's read of the changed strings, which follows every owner.
- The full guide check on this build; the main session runs it once every owner is done.

## Change log

Modified:

- `work/build/scripts/phase-2/stage_c_ch18_build.py`: the intro, Rule 18.1's "Why it works", Rule 18.22's citations, 22 titles, `KEYS[17]`'s two form states, Rule 18.17's builders, Rule 18.11's sentence on the guide's mat (D2-1722) and `palette()` reading tints, the second pass's four fixes
- `work/build/scripts/phase-2/stage_c_ch19_build.py`: 8 titles, Rule 19.6's again in the second pass
- `work/build/guide/chapters/18-components.json` and `work/build/guide/chapters/19-accessibility.json`: regenerated

Created:

- `work/handoffs/phase-2/20261111_Gate-2-Fix-Accessibility-Notes.md` (this file)
