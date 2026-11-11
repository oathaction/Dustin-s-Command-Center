# Gate 2 fix pass: the component engineer's notes

Oath & Action Edition 06, Phase 2, Gate 2 fix pass, November 11, 2026. Written by the component engineer, an instance in the `oa-engineer` role scoped to chapter 18's code sets, run as a subagent of the main session under `20261111_Gate-2-Fix-Brief.md` (my row in "Who fixes what"). I edit `work/build/guide/code/c-18-*` (the HTML, CSS, scripts and keys files) and this file.

I read, in order: `CLAUDE.md`, my role file, the Gate 2 brief ("Read first", "Fixed for everyone", "How to look"), the fix brief (my row, "Order and crossings", "Checks"), DT-S2, DT-S3, DT-S7 and DT-S12 in the drift red team's report, the `aria-invalid` note in the accessibility evidence, and the round 1 and round 2 component notes.

Status: **done.** Every item in my row is in the files, and every check below ran on the final files. One crossing waits on the accessibility lead: the form's keys path in their generator (“For the main session”, item 1).

## What I changed, item by item

| Item | Set | Change |
|---|---|---|
| DT-S2 | `c-18-tabs.css` | The tab's focus ring sits inside the tab with its 2 px gap: `outline-offset: calc(-1 * (var(--oa-border-width-focus-ring) + var(--oa-border-focus-offset)))`, −4 px, as `c-18-scroll-region` already draws it. A comment above it cites Rule 18.11 and gives the reason: the tabs stand 4 px apart, so a ring outside would reach the next one. |
| DT-S2 | `c-18-location.css` | The list row's ring the same way, −4 px, with a comment citing Rule 18.11: the rows touch, so a ring outside would cross the next row. The breadcrumb links and Previous and Next keep the outside ring. |
| DT-S2, same fault | `c-18-link.css`, `c-18-search.css` | Two more controls drew the gapless inside ring the drift report did not list: the link list's rows (`.oa-link--item`, added in round 2 from the location's pattern) and the search's Clear button, which fills the end of the search box. Both now take −4 px with the same comment citing Rule 18.11. No c-18 set now draws a ring with no gap (searched: every `outline-offset` in the 24 CSS files is +2 px or −4 px). |
| DT-S3 | `c-18-tracker.html`, `.css` | The check-date notice reads “**Warning:** Checked March 17. The committee may have acted since.”, with “Warning:” in bold as `c-18-messages` sets it; `.oa-tracker-check b` joins the set's bold list. The notice keeps its warning mark and draws no bar, as Rule 11.10's plate draws its notice (see “For the main session”). |
| DT-S7 | `c-18-report-reader.css`, line 219 | The comment gives the current reason: “A page's own states. Loading shows in the view, where the page will appear. An error is a message about the page, so it sits under the view, on the surface, drawn as Rule 18.18 draws every message.” The Prussian clause is gone; no other c-18 file or chapter 18 sentence repeats it. |
| DT-S12 | `c-18-download.html` | The copyable example saves as `download="tokens.css"`, the file its words name (“Download tokens.css, CSS, 95 KB”). In the guide's live stages the build still sends a press to the page's own copy of tokens.css, which saves under the guide's settled dated name; only the code a builder copies changed. |
| AX note, `aria-invalid` | `c-18-form.html`, `.js` | Both fields carry `aria-invalid="false"` in the markup, the script sets it on any checked field that lacks it, and a fixed field goes back to `"false"` where it used to lose the attribute. So the email field says nothing about validity until Send, and says nothing again once fixed, even if the reader then breaks the address before the next Send. The CSS already keys the red bar on `[aria-invalid="true"]` only. The script's head comment says why. |
| Keys | `c-18-form.keys.json` | “Send with mistakes”: after typing “name@”, a new state asks that the email field's `aria-invalid` read `"false"` before Send. “Send right”: after Enter, the email field's `aria-invalid` reads `"false"` where it read absent (`null`). No other keys file names anything I changed (tabs, location, link, search, tracker, report reader and download paths check focus, states and words, none of which moved). |

## For the main session

1. **The keys file is the accessibility lead's generator's output.** `stage_c_ch18_build.py` writes every `c-18-*.keys.json` from its `KEYS` table, so the next run of that script puts `c-18-form.keys.json` back as it was, and the guide check's walk of “Send right” then fails on `aria-invalid` (it reads `"false"`, the old path wants it absent). The lead's generator needs the same two changes, in `KEYS[17]`:
   ```python
   # "Send with mistakes", the second step
   step(type='name@', focus='input[autocomplete="email"]',
        states=[st('input[autocomplete="email"]', attr='aria-invalid', **{'is': 'false'})]),
   # "Send right", the Enter step's first state
   step('Enter', None, [st('input[autocomplete="email"]', attr='aria-invalid', **{'is': 'false'}),
                        st('.oa-form-send', text='Sending')],
        status_has='Sending', status_el='.oa-form-status'),
   ```
   Imported read-only with these two changes made in memory, the generator emits my keys file byte for byte. Until the lead lands them, `stage_c_ch18_build.py --check` names this one file as differing.
2. **Words the lead may want** (chapter 18 is the lead's): Rule 18.17's builders could say “Give each field <code>aria-invalid="false"</code> until a send finds it wrong, and set it back to "false" once fixed, so a browser's own check of an email address says nothing while the reader types.” Nothing in the chapter is wrong without it.
3. **Chapter 11's live form has the same behavior.** `s-11-15-correct` (systems designer, `apply_systems_ch11_ui.py`, line 692) draws its email field as `type="email"` with no `aria-invalid` until a send, so Chromium reports it invalid while an address with no @ is being typed. The same two-line change fixes it there, if the systems designer wants the two forms to agree.
4. **The warning's bar.** Rule 18.18 says a warning starts “Warning:” beside a 4 px bar in ink, and chapter 11's mark table (`s-11-marks`) draws its warning with that bar. Rule 11.10's plate (`s-11-10-correct`) and this tracker draw the check-date notice with the mark and the words and no bar. I left the tracker matching Rule 11.10's plate, which Rule 18.20 cites. If the studio wants the bar on the check-date notice too, it goes on both at once: the systems designer's plate and my tracker (one border-left and its padding). My recommendation: add the bar to both, so a warning looks the same everywhere.

## For the systems designer (anatomy plates)

`stage_c_ch18_anatomy_build.py` reads my sets' markup and CSS, so a rerun picks up each change by itself. Read from its plate functions:
- **`s-18-09-anatomy` (tabs, `p09`) must follow.** It draws focus on the selected tab, and its rewritten CSS (`.sx-kd[data-ax-focus]`) carries my ring: −4 px after the rerun, where it reads `calc(-1 * var(--x2))` today. This is DT-S2's plate part.
- **`s-18-20-anatomy` (tracker, `p20`) must follow.** It keeps the check-date line, which now starts “Warning:” in bold. Its key's sixth row, “The warning mark and when we last checked”, could name the word too: “The warning mark, “Warning:” and when we last checked”.
- **`s-18-17-anatomy` (form, `p17`)** redraws with no visible change: both fields carry `aria-invalid="false"` in the markup now, and the plate sets `"true"` on the email field it shows in error.
- No change to draw: `s-18-07-anatomy` (location) and `s-18-15-anatomy` (search) draw no focus; `s-18-05-anatomy` (link) draws focus on the skip link only, which keeps its outside ring; `s-18-14-anatomy` (download) and `s-18-21-anatomy` (report reader) take an attribute value and a comment that draw nothing.

## Routine calls

- D2-xxx | Every inside focus ring in chapter 18's code sets takes its 2 px gap, −4 px, including the link list's rows and the search's Clear, which the drift report did not list | DT-S2 names the fault, and builders copy these sets; one look for one behavior, and Rule 17.9's “never 0” holds in every set |
- D2-xxx | Each inside ring's comment cites Rule 18.11 and names why that control cannot take the outside ring | The brief asks for the citation, and a builder who reads the reason knows when the outside ring applies again |
- D2-xxx | The tracker's check-date notice takes “Warning:” in bold and keeps no bar, as Rule 11.10's plate draws its notice | DT-S3 asks for the first word; the bar is a question for both owners at once (“For the main session”, item 4) |
- D2-xxx | The download example saves as `tokens.css`, the name its words give | DT-S12; the guide's own button keeps its settled dated name, and the live stages still hand a press to it |
- D2-xxx | The form's fields carry `aria-invalid="false"` from the start, the script adds it where markup leaves it out, and a fixed field returns to `"false"` | The accessibility evidence's note; a field that loses the attribute hands its state back to the browser's own check, which reports an unfinished address as invalid |
- D2-xxx | The form keys file is edited by hand to match the code, with the generator change written out for the accessibility lead | My row asks me to update the keys paths my changes touch, and the file is that lead's generator's output; the main session routes the generator change |

## Questions for Dustin

None. Every change sits inside the fix brief's calls.

## Tested

All in this container on November 11, 2026, Chromium through Playwright, Python with `-I`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2-fix/components/`.

- **Strict build** of the whole guide into scratch, after the last change: `guide_build.py --strict --out <scratch>/build/guide.html`, exit 0, 0 warnings; 16 chapters, 185 rules, 428 specimens, 9,387,848 bytes; chapter 18 at 1,158,903 bytes of its 1,250,000. A chapter 18 page alone builds with no warning on any code set (its only warnings are other chapters' specimens left unplaced, as a one-chapter page expects).
- **`stage_c_ch18_build.py --check`**: exit 1, naming one file, `c-18-form.keys.json`, my hand edit, which waits on the generator change in “For the main session”, item 1. Before my changes it said “chapter 18: current”. With the two changes made in memory to an imported copy of the generator, it emits my keys file byte for byte.
- **`stage_c_ch18_anatomy_build.py --check`**: exit 0 (it builds in memory and reports sizes; it compares nothing). My own probe (`tools/anatomy_probe.py`) built all 25 plates in memory from my starting sets and from the final sets: three plates change, `s-18-09-anatomy` (the ring), `s-18-20-anatomy` (“Warning:”) and `s-18-17-anatomy` (an attribute that draws nothing). It wrote nothing. Separately, `s-18-23-anatomy` on disk already differs from a fresh build from my starting sets, which is not mine.
- **The generator chain** as the fix brief lists it, from the project folder, with a SHA-256 of every file under `work/build/guide` and `work/build/assets` before and after each step: `apply_systems_ch11.py`, `stage_b_ch10_build.py --no-draw`, `stage_b_ch12_systems_build.py`, `promotion_identity.py specimens`, `guide_editor_build.py`, `stage_b_identity_ch01.py` and `stage_c_ch17_build.py` ran with exit 0. Steps 5 and 6 rewrite the same three chapter 01 plates in turn, as the order intends, and the two folders came out byte for byte as they went in. `stage_c_ch17_build.py` also rewrote its figures file's token version line to “6.0.0-gate2.9”, read from `tokens.json`: the engineer's release, not my change. None of these generators reads a c-18 file. `stage_c_identity_ch17.py` failed as the brief writes it (`ModuleNotFoundError: stage_a_identity_lib`): under `-I` Python leaves the script's folder off the import path, and the module runs inside `stage_a_identity_build.py`, which writes a board, so I did not run that in its place.
- **Key walk.** The guide check's own `keyPaths()` (loaded from `guide_check.js` up to its main block, limited to my eight changed sets) on a chapter 18 page built strict from the final files: 8 sets, 13 paths, 52 walks (both live stages at 1440 and 390 px), 268 steps, no problem. The form's old keys file against the new code fails “Send right” in all four walks (`aria-invalid="false", not null`), which is why the keys path had to change.
- **Copy check** (`tools/copy_check.js`): the eight changed sets, each pasted into a blank page that links `work/build/tokens/tokens.css` and the brand's local font files, from my starting files and from the final files, light and dark, with and without forced colors, at 1440 and 390 px, in 20 states (rest; focus on the selected and the unavailable tab; on the current and another row in the location and link lists; on Clear with text typed; on the ready download; and the form at rest, while typing “name”, after a wrong Send, once fixed, and broken again): 320 captures. No script error, no sideways scroll; axe-core (WCAG 2.0 to 2.2 A and AA and best practice) finds nothing on any final page in either theme or width. The only failed requests are axe re-reading the stylesheet over `file://` after each capture.
- **What changed on screen, pixel by pixel, before against after:** the report reader, download and form draw identically in all 64 of their captures. The four ring sets differ only around the focused control, and the tracker only on its check line. Measured from the pixels at 1440 and 390 px, at 1x and 2x, the ring now sits 2 px in from every edge of the tab, the list row and Clear, 2 px wide, where it sat on the edge before. In the dark theme the selected tab's Newsprint bar and the current row's Newsprint bar sit under the ring's inner edge on one side, as they did before; at 390 px, where the tabs wrap, Votes's ring no longer merges with Summary's bar above it.
- **The form's state as the browser reports it** (Chromium's accessibility tree, through CDP), both themes: before, the email field read invalid while “name” was typed and again once a fixed address was broken; now it reads not invalid in both, and invalid only after a wrong Send.
- **By eye**, contact sheets at 2x, 1440 px, before beside after, light, dark and forced colors: the tabs, the location and link rows, Clear and the tracker's check line; the tracker's card at 390 px in both themes. The rewrap of three comments after the first copy check changed nothing drawn: a second full run matched all 160 final captures pixel for pixel.

## Not tested

- Any screen reader. The invalid state was read from Chromium's accessibility tree, never heard; whether NVDA, JAWS or VoiceOver announce “invalid” from a native email check differs by reader and browser.
- Safari, Firefox, real phones and Windows contrast themes. Forced colors were emulated in Chromium.
- The full guide check at four widths, and the key walk on the whole page; I walked a chapter 18 page. The main session runs the full check once every owner is done.
- The anatomy plates as files: the systems designer reruns them; I built them in memory only.
- `stage_c_identity_ch17.py` on its own (see Tested).
- 1024 and 360 px, and text at 200 percent, for the changed sets.

## Change log

Modified, all in `work/build/guide/code/`:
- `c-18-tabs.css`, `c-18-location.css`, `c-18-link.css`, `c-18-search.css`: the inside focus ring with its 2 px gap and its comment (DT-S2).
- `c-18-tracker.html`, `c-18-tracker.css`: “Warning:” on the check-date notice, in bold (DT-S3).
- `c-18-report-reader.css`: the comment's current reason (DT-S7).
- `c-18-download.html`: `download="tokens.css"` (DT-S12).
- `c-18-form.html`, `c-18-form.js`: `aria-invalid="false"` until a wrong Send, and back to it once fixed.
- `c-18-form.keys.json`: the two states above.

Created: `work/handoffs/phase-2/20261111_Gate-2-Fix-Components-Notes.md` (this file).

Not touched: any generator, chapter, specimen, manifest, `guide_build.py`, `guide_check.js`, the shell, the tokens, `source/`, `work/ledger/`, a board or another owner's file. The generator chain rewrote files as the brief has every owner do, and left `work/build/guide` and `work/build/assets` byte for byte as it found them. Built only into my scratch folder. Nothing committed or pushed.

Scratch, outside the repository: `before/` (the sets at the start of this pass), `tools/` (`anatomy_probe.py`, `keys_walk.js`, `keys_walk_dir.js`, `copy_check.js`, `copy_check_2x.js`, `sheet.py`), `build/` and `ch18/` (the strict builds, their reports and the walk results), `chain/` (hashes and logs of the chain), `copy/`, `copy-final/` and `copy2x/` (captures and results), `sheets/` (contact sheets).
