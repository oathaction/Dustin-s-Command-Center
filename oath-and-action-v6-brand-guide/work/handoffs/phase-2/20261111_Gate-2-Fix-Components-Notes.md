# Gate 2 fix pass: the component engineer's notes

Oath & Action Edition 06, Phase 2, Gate 2 fix pass, November 11, 2026. Written by the component engineer, an instance in the `oa-engineer` role scoped to chapter 18's code sets, run as a subagent of the main session under `20261111_Gate-2-Fix-Brief.md` (my row in "Who fixes what"). I edit `work/build/guide/code/c-18-*` (the HTML, CSS, scripts and keys files) and this file.

I read, in order: `CLAUDE.md`, my role file, the Gate 2 brief ("Read first", "Fixed for everyone", "How to look"), the fix brief (my row, "Order and crossings", "Checks"), DT-S2, DT-S3, DT-S7 and DT-S12 in the drift red team's report, the `aria-invalid` note in the accessibility evidence, and the round 1 and round 2 component notes.

Status: **in progress.** Every item's change is in the files; the checks are running.

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

## Questions for Dustin

## Tested

## Not tested

## Change log
