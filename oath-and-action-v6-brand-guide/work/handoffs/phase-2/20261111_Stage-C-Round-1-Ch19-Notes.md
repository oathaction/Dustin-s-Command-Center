# Stage C, round 1: chapter 19, Accessibility

Oath & Action Edition 06, Phase 2, November 11, 2026. Written by the accessibility lead, in the `oa-ux-accessibility-lead` role, run as a subagent of the main session, under `20261111_Stage-C-Round-1-Brief.md` (chapter 19's row and paragraph) and the main session's task of today. Status: **chapter 19 written and built; its results are dated November 11, 2026.**

I read the round 1 brief's chapter 19 lines, Master Brief section 22, the research lead's section 1 (the 55 criteria in W3C's words), my round 0 map (inventory, section 4), the rule titles of every chapter now in the tree (01 to 12, 17, 18 and 26), DR-213, and the decision log entries the brief names.

## What I built

| Piece | Path | Status |
|---|---|---|
| Generator | `work/build/scripts/phase-2/stage_c_ch19_build.py` (`--check`) | done |
| Chapter | `work/build/guide/chapters/19-accessibility.json` | done: 9 rules in three groups |
| Specimens | `work/build/guide/specimens/s-19-*.html`, 18 files, in `manifest-accessibility.json` | done |
| Results | `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch19-Results.json` | done, dated; Rule 19.8 prints it |

**The rules.** Group 1, the standard: 19.1 Build every page and product to WCAG 2.2 at level AA, and find each criterion here. Group 2, rules this chapter owns, which close the gaps my round 0 map gave chapter 19: 19.2 alt text (1.1.1), 19.3 instructions by their words (1.3.3), 19.4 text as text (1.4.5), 19.5 one tap, click or key (2.1.4, 2.5.1, 2.5.2, 2.5.4, 2.5.7), 19.6 text that grows, spacing that opens and the screen that turns (1.3.4, 1.4.4, 1.4.12, with 07.6 for 1.4.10). Group 3, how to check: 19.7 the verification matrix, 19.8 dated results with Tested and Not tested apart, 19.9 the device script.

**The criteria (`s-19-criteria`, Rule 19.1).** All 55 A and AA criteria, parsed from the research notes by the generator, in W3C's words as the Recommendation prints them (one straight quote in 2.2.1 stays as printed), with level, the six new in 2.2 tagged, and how the guide meets each, with links to the rules the page holds. W3C's informative notes stay out; the sources point to the Understanding pages. 4.1.1 Parsing closes the list as removed. A labeled search field with Clear the search and Escape, and a radio choice (All, Met, Met in part, Gaps, Not used today), narrow the list; a polite status line gives the count and, when nothing matches, the advice in the same line (Rule 18.15). Tested by keyboard at 1440 and 390 px: "focus" leaves 8 of 55, "zzzz" leaves 0 with the advice, Escape and Clear the search restore 55, the arrow keys choose Gaps and leave 8.

**The map, updated from round 0.** Round 0 counted 9 met, 21 in part, 21 gaps and 4 not applicable. With chapters 17, 18, 19 and 26 it now counts **37 met, 5 in part, 8 gaps and 5 not used today**. The gaps, each with the chapter that owes it: 1.2.1, 1.2.2, 1.2.3 and 1.2.5 (chapters 16 and 23, with audio and video); 2.4.2 Page Titled, 3.1.1 Language of Page and 3.2.6 Consistent Help (chapter 20); 3.1.2 Language of Parts (chapters 02 and 20). In part: 1.3.2, 2.3.1, 2.4.5, 2.4.6 and 3.2.1, each with what is met and what chapter 20 or 23 owes. Not used today: 1.2.4, 1.4.2, 3.3.4, 3.3.7 and 3.3.8. The generator refuses a map that cites a rule a present chapter does not hold.

**The matrix (`s-19-matrix`, Rule 19.7).** Master Brief section 22's 14 checks, each with what it shows, its method and the criteria it serves, as a readable list that stacks on a phone.

**The results (`s-19-results`, Rule 19.8).** Printed from the results file, which names the runs behind each line: the full guide check on the build of 03:13 UTC at four widths, my chapter 18 keyboard walk and audit, and the token download test. Nine checks tested, nine not tested with the reason.

**The device script (`s-19-devices`, Rule 19.9, DR-213).** iPhone with VoiceOver, Android with TalkBack, Windows with NVDA and a contrast theme, and Mac with VoiceOver, each in four to six numbered steps written for a person with no training, then "Ten things to listen for: a pass sounds like this", and what to write down. The TalkBack script says plainly that gestures differ between versions and makers. I wrote the steps from what I know of each platform; I could not run any of them here (Not tested).

**Weight.** Chapter 19 weighs 0.204 MB of its 0.3 MB budget; its specimens hold 87 KB, the criteria list most of it.

## For the guide engineer, through the main session

1. **The page scrolls sideways at 200 percent text at 390 and 360 px** (404 and 386 px wide; `textSpacing`, first item "page"), in the full check of the 03:13 UTC build. At the default size no width scrolls. The element is not named in the results; a new chapter (17, 18 or 26) is the likely source.
2. **The check counts the new chapters inconsistently.** On a page that holds 176 rules it counted 155 at 1440 px and 165 at the other widths, and it failed links to `#tokens` and `#part-production` and citations of Rules 18.15 and 18.22 that the page holds (`grep` finds each id once). I did not count these as faults of the page.
3. **The token download test** fails 4 of 16 cases that expect every download button to offer the tokens.css zip; chapter 26's tokens.json download does not.
4. **The new `keyPath` check skips two fields of `oa-keys/1`.** It ran my 24 files on the build with chapter 19 and failed only two paths, each on a field it does not read: `"present": true` with `"attr"` (c-18-download: "has aria-describedby=..., not undefined") and `"above": 0` with `"prop"` (c-18-scroll-region: "scrollLeft is 40, not undefined"). Both sets do what the paths ask; my walker passes them. Both fields are in the format in my chapter 18 notes, because a prefixed id differs by theme and a scroll position has no fixed value.
5. **For the systems designer:** axe-core flags `scrollable-region-focusable` once at 390 px on `.sx-kd.sx-ax-p > .sx-kk`, which sits in one of its specimens.

## For the main session

- **Chapter 18 is over its budget** now that the anatomy plates are landing: 1.13 MB in one build and 1.10 MB in the next, against 1.1 MB.
- **The results are a snapshot.** The results file names its build and runs; when chapters change before the preview, I rerun the checks and rewrite the file, and the generator reprints the plate.

## Routine calls

- D2-xxx | Chapter 19 holds nine rules in three groups: the standard (19.1), five rules that close the gaps the round 0 map gave chapter 19 (19.2 to 19.6), and how to check (19.7 to 19.9) | The brief's four parts, plus the criteria only chapter 19 was owed
- D2-xxx | The 55 criteria are one searchable list with a status choice, in W3C's words, with links to the rules that meet each | A builder looks up one criterion or the open gaps; it must read and search on a phone
- D2-xxx | W3C's informative notes stay out of the list, and the sources point to the Understanding pages | D2-1138 keeps notes apart; they would double the list's weight
- D2-xxx | A criterion's status is Met, Met in part, Gap with the chapter that owes it, or Not used today with the chapter that would add it | Round 0's four kinds, in plain words
- D2-xxx | The map counts 37 met, 5 in part, 8 gaps and 5 not used today | Chapters 17, 18, 19 and 26 now exist
- D2-xxx | A gap stays a gap until a rule states the criterion, even where this guide's own page meets it (2.4.2, 3.1.1) | The rules are what a builder follows; the shell's title and language are not a rule yet
- D2-xxx | The results print from a dated file that names its runs, and the generator shows "pending" when it is missing | D2-469 and D2-805: figures come from a file
- D2-xxx | The results cite only checks whose results hold; the check's miscounts on the new chapters go to its owner | Honesty rule: never describe a result the run did not support
- D2-xxx | The device script uses only basic gestures and keys, and says where they differ by version | A person with no training must be able to follow it, and gestures change between versions
- D2-xxx | The device script asks for ten things to listen for, the same on every device | One list makes four devices' results comparable
- D2-xxx | Numbers under ten in the chapter's prose print as words, through the generator | House rule H06
- D2-xxx | Rule 19.6's pictures show a 360 px screen zoomed to 200 percent as its 180 px layout drawn at twice its sizes, marked twice true size | That is what 200 percent zoom does, and every size divided by two stays on the type scale (D2-254)

## Questions for Dustin

None. DR-213 set the devices; everything else sits inside the round 1 brief.

## Tested

All on November 11, 2026, in Chromium through Playwright, with outside requests blocked.

- `stage_c_ch19_build.py`: writes 9 rules and 18 specimens; its checks pass on every string and alt (no dash, straight quote, banned word, studio code or ", not" turn; W3C's words exempt as quotations); the map covers exactly the 55 criteria and cites only rules that present chapters hold.
- `guide_build.py --strict` with chapter 19: 9,537,586 bytes, 16 chapter files, 185 rules; no warning on chapter 19 (the remaining warnings are other owners' anatomy plates in progress).
- The criteria list by keyboard at 1440 and 390 px (search, Escape, Clear the search, the status choice by arrow keys, the status line's words).
- `guide_check.js` at four widths on the 03:13 UTC build (before chapter 19): the results the chapter prints.
- `guide_check.js --quick` on the build with chapter 19 (1440 and 390 px): chapter 19's plates have no text under 13 px or under contrast, no landmark, no axe-core item and no sideways scroll. Its one finding was mine, the 19.6 pictures' 30 px type off the type scale; I redrew them as the 180 px layout a 360 px screen gives at 200 percent, at exactly twice its sizes and marked twice true size, and the strict build of all 16 chapters then had no warnings, with chapter 19 at 203,879 bytes and chapter 18 at 1,097,358.
- `tokens_download_test.js` on the 03:13 UTC build: 12 of 16 pass.
- Captures at 390 px of the device script, the matrix, the results and three pictures, looked at.

## Not tested

- Any step of the device script: this container has no iPhone, Android phone, NVDA, Mac or Windows contrast theme. The steps follow each maker's menus as I know them, which makers rename between versions.
- Every "Not tested" line in the results file.
- Print, reduced motion on chapter 19 (it has no motion), and grayscale.

## Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, any board, the shell, `guide_build.py`, `guide_check.js` or another owner's files changed. Nothing committed or pushed.

**Created**
- `work/build/scripts/phase-2/stage_c_ch19_build.py`
- `work/build/guide/chapters/19-accessibility.json` (generated)
- `work/build/guide/specimens/s-19-criteria.html`, `s-19-matrix.html`, `s-19-results.html`, `s-19-devices.html`, `s-19-1-failure.html`, `s-19-2-correct.html`, `s-19-2-failure.html`, `s-19-3-correct.html`, `s-19-3-failure.html`, `s-19-4-correct.html`, `s-19-4-failure.html`, `s-19-5-correct.html`, `s-19-5-failure.html`, `s-19-6-correct.html`, `s-19-6-failure.html`, `s-19-7-failure.html`, `s-19-8-failure.html`, `s-19-9-failure.html` (generated)
- `work/build/guide/specimens/manifest-accessibility.json` (generated)
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch19-Results.json`
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch19-Notes.md` (this file)

**Scratch** (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/ch19/`): `full/` (the 03:13 build and its check and download results), `b1/`, `b2/` (builds with chapter 19 and the quick check), `scripts/criteria_test.js`, `shots19.js`, captures in `shots/`.
