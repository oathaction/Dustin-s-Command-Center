# Stage C, round 1: the component engineer's notes

Oath & Action Edition 06, Phase 2, stage C, round 1, November 11, 2026. Written by the component engineer, a second instance in the `oa-engineer` role, run as a subagent of the main session under `20261111_Stage-C-Round-1-Brief.md` ("Who works when", item 4) and D2-1268 to D2-1270. I write chapter 18's 24 code sets in `work/build/guide/code/` and nothing else in the repository but this file.

I read, in order: my role file, `CLAUDE.md`, the round 1 brief, the guide engineer's round 0 notes (sections 3 and 4 and "Contracts round 1's makers follow"), the demo set `c-00-save-button.*`, the code set checks in `guide_build.py`, `tokens.css` and `tokens.json`, the accessibility lead's inventory (sections 2, 2.2 and 5), the research notes (sections 2 to 4) and chapter 11's six live specimens. The accessibility lead's chapter 18 notes did not exist when I started; I check for them as I go.

This file is written early and grows as each batch lands. Status: **batches 1 and 2 landed (13 sets); batch 3 in progress.**

## How every set is built

These hold for all 24 sets, on top of the build's contract (round 0 notes, section 4).

- **Self-contained.** Each set's CSS styles everything its HTML holds, so a builder who copies one set gets a working component. Each set's classes start with its own name (`oa-button`, `oa-tabs`, `oa-form`), so two sets on one page never restyle each other. In the guide every set's CSS is global, so this is also what keeps the 24 plates apart.
- **Roles only.** Every color is a short name (`--oa-color-text-primary`, `--oa-color-surface`, `--oa-color-field-ground`, `--oa-color-state-*`, `--oa-component-button-*`), so the light and dark themes and every surface class reach it (F-1). Two short names are `initial` in the dark theme, the Error Band and the ask's keyline; each is read with a fallback (`var(--oa-color-state-error-band, transparent)`), so on Charcoal the error keeps its bar, mark and words with no band (D2-1160).
- **Icons inline.** A builder's page has no sprite, so each set draws its utility icons inline, copied from the 24 px and 16 px masters in `work/build/assets/utility/`, with `aria-hidden="true"`, `focusable="false"` and `currentColor`.
- **States drawn with more than color.** Pressed, checked and current choices take one look (D2-1152): a check glyph before the word, the word in bold, a 2 px edge. Unavailable controls keep focus, carry `aria-disabled="true"`, draw a dashed edge and point to a reason line. Error, warning and selected bars are borders, never shadows (D2-1158). Hover is an underline or a thicker edge, never an inset shadow (G-7).
- **Words for every change.** A change a reader cannot see from the control itself goes to a polite status line in words, with the success or error mark where Rule 11.15 asks for one.
- **Fits.** No label takes `white-space: nowrap`; long words break; a row of two buttons stacks when a label would not fit (F-2). Each set is tested at 320 px and with text at 200 percent in a 360 px window.
- **Forced colors.** Each set has a `forced-colors` block that gives every control a system-color edge, and its states keep their glyph, weight and edge.
- **Scripts.** A plain script finds every copy of its component on the page and sets each up; it reads ids from attributes (`aria-controls`, `aria-describedby`, `for`, `data-oa-theme-for`), never as literals, and writes only inside its own component.

## Batches

Each batch is built with `guide_build.py --strict` on a scratch chapter that attaches the sets, then walked in Chromium by my scratch harness (both live stages; 1440, 390 and 320 px; text at 200 percent at 390 and 320 px; text spacing raised at 320 px; forced colors; reduced motion; axe-core on each stage; and a key path per set). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/components/` (`comp_test.js`, `keys.js`, `summ.py`, `build_names.py`, `out/`, `shots/`).

### Batch 1: 18.1 button, 18.2 toggle, 18.3 choice, 18.4 theme switch, 18.5 link, 18.24 ID chip

| Set | Files | Result |
|---|---|---|
| `c-18-button` | html, css | Clean: build strict, no overflow at 320 px or at 200 percent text, axe clean in both stages, forced colors edges, no motion, key path 8 steps in both stages at 1440 and 390 |
| `c-18-toggle` | html, css, js | Clean; key path 11 steps |
| `c-18-choice` | html, css | Clean **only with the build change below** (radio names per stage). With today's build the two stages share one radio group, so the light stage loads with nothing checked |
| `c-18-theme-switch` | html, css, js | As the choice: clean with the change, key path 5 steps (the guide's root stays `light`, the guide's storage is never written) |
| `c-18-link` | html, css | Clean; key path 8 steps (skip link shows and moves focus; the cross-reference moves focus; the outside link's name ends "(another site)") |
| `c-18-id-chip` | html, css | Clean; key path 1 step |

**Hooks for the keys files** (selectors inside a stage; no ids, since the build prefixes them):

- **18.1** `.oa-button-set`; buttons `.oa-button` with `--primary`, `--ask`, `--quiet`, `--icon-start`, `--icon-end`; unavailable `.oa-button[aria-disabled="true"]` described by `[id$="oa-button-why"]`; sending `[aria-describedby$="oa-button-sending"]`, its line `[id$="oa-button-sending"]` (`role="status"`); the yielded ask `.oa-button--ask[data-oa-yield]`. No script. Tab order: Save to your list, Remind me, Read the bill, Start the form over, Next step, Send your comment (unavailable, keeps focus), Sending (unavailable), Remind me (yielded).
- **18.2** `[data-oa-toggle]`; the toggle `.oa-toggle:not(.oa-toggle--chip)` ("Follow this bill", starts not pressed), its line the next `.oa-toggle-status`; chips `.oa-toggle--chip:nth-of-type(1)` to `(4)` (Housing on, Health care, Elections, Transit unavailable), group `[role="group"]`, its line `.oa-toggle-why + .oa-toggle-status`. Words: "You follow this bill. We email you when it moves." / "You no longer follow this bill." / "Showing bills on Health care and Elections." / "No topic is on, so every bill shows." Two status lines in the stage, so a keys path names `status_el`.
- **18.3** `fieldset.oa-choice`; radios `.oa-choice-input[value="summary"]` (checked), `[value="text"]`, `[value="changes"]` (disabled, reason `[id$="oa-choice-why"]`). No script, no status line: the checked state is the words.
- **18.4** `.oa-theme-page` (the target in the guide), `fieldset.oa-theme[data-oa-theme-for]`, radios `.oa-theme-input[value="light"]`, `[value="dark"]`, `[value="device"]` (checked). Each choice sets `data-oa-theme` on `.oa-theme-page` to `light`, `dark` or `device`. No status line (inventory 2.2). Storage `oa-theme` is written only when the switch sets the page's root, so in the guide `{"storage": "oa-theme", "is": null}` holds after every step.
- **18.5** `.oa-link-set`; `.oa-link-skip` (first stop, shown on focus, to `[id$="oa-link-main"]`); in-text `.oa-link-text .oa-link` (the cross-reference to `[id$="oa-link-steps"]`, then the outside link); list `.oa-link--item[aria-current="page"]` (Bills), the second item (Hearings); `.oa-link-muted` ("Votes. Coming later.", text, no stop).
- **18.24** `.oa-chip-set`; text chips `span.oa-chip`; the link chip `a.oa-chip--link` ("Reform R-04") to `[id$="oa-chip-r04"]`, which takes focus.

### Batch 2: 18.8 disclosure, 18.9 tabs, 18.10 table, 18.11 scroll region, 18.12 code block, 18.13 copy, 18.14 download

| Set | Files | Result |
|---|---|---|
| `c-18-disclosure` | html, css, js | Clean; key path 7 steps (details and summary need no script; the button form flips `aria-expanded`) |
| `c-18-tabs` | html, css, js | Clean; key path 9 steps (automatic activation, wrap, Home and End, the unavailable tab takes focus and shows no panel, Tab goes to the panel) |
| `c-18-table` | html, css, js | Clean; key path 7 steps. Cards under 36rem of room. My harness reads the sort buttons' forced colors cue on the button, while the underline sits on its word, so it lists them; the capture shows the underline |
| `c-18-scroll-region` | html, css, js | Clean; a Tab stop, a group role, a name and the hint only while it overflows (at 390 and 320 px, not at 1440); the arrow key scrolls it |
| `c-18-code-block` | html, css, js | Clean; key path 4 steps, the clipboard read back, and a refused copy (the line turns into the error, the text box takes focus with all of it selected) |
| `c-18-copy` | html, css, js | Clean; key path 5 steps, as the code block |
| `c-18-download` | html, css | Clean; key path 2 steps. "Lo where a host asks first" belongs to the guide's own host prompt, so a builder's download shows Hv, Fo and Di only |

**Hooks for the keys files:**

- **18.8** `[data-oa-disclosure]`; `details.oa-disclosure` (the first loads **open**, the second closed), each `> summary.oa-disclosure-summary`; the button form `.oa-disclosure-button` (`aria-expanded="false"`) and its part `.oa-disclosure-button + .oa-disclosure-body` (`hidden`).
- **18.9** `[data-oa-tabs]`; tabs `[role="tab"]:nth-child(1)` to `(4)` (Summary selected, Timeline, Sponsors, Votes unavailable with `aria-disabled` and its reason `[id$="oa-tabs-why"]`); panels `[aria-labelledby$="oa-tabs-t1"]` to `t4`. `End` moves focus to Votes, which takes focus and leaves Summary's panel showing; only the selected tab carries `tabindex="0"`.
- **18.10** `[data-oa-table]`; the first `table.oa-table-grid` **loads sorted by Bill, ascending** (`aria-sort` on `th:nth-child(1)`), so the first Enter there reverses it to descending. Buttons `th:nth-child(1) .oa-table-sort` to `(3)`; Status is not sortable. Line `.oa-table-status`: "Sorted by bill, highest number first.", "Sorted by title, A to Z.", "Sorted by date filed, oldest first." and the reverse of each. The loading, empty and error states sit below in three small tables with `role="status"`, plain text and `role="alert"`.
- **18.11** `[data-oa-scroll]`; the frame is `.oa-scroll-frame` (`tabindex="0"`, `role="group"`, named by its title, only while it overflows); hint `.oa-scroll-hint`.
- **18.12** `[data-oa-code]`; panels `.oa-code-panel`, buttons `.oa-code-copy` ("Copy the HTML", "Copy the CSS"); a panel's `pre.oa-code-pre` takes `tabindex="0"` while it overflows, so at 390 px the Tab after "Copy the HTML" lands on the HTML panel's code. Line `.oa-code-status`: "Copied the HTML, 2 lines, to the clipboard."; refused: "Error: The browser blocked copying. ..." and focus on `textarea.oa-code-fallback`.
- **18.13** `[data-oa-copy]`; buttons `.oa-copy-button` (visible "Copy", name "Copy --oa-color-text-primary" and "Copy #121212, Charcoal"); values `code.oa-copy-value`. Line `.oa-copy-status`: "Copied #121212, Charcoal."; refused: focus on `input.oa-copy-fallback` with the value selected.
- **18.14** `a.oa-download[download]`, then `a.oa-download[aria-disabled="true"]` (no `href`, `tabindex="0"`, reason `[id$="oa-download-why"]`).

## For the guide engineer

1. **Radio names in the live stages (needed by 18.3 and 18.4, and later 18.17 and 18.21).** A radio group is held together by its `name`. The two live stages draw the same markup, so today the light and dark stages' radios form one group across the page: the dark stage's `checked` unchecks the light stage's at load, and a choice in one stage unchecks the other. Please give every `name` attribute of an `input`, `select`, `textarea`, `button`, `fieldset` or `output` in a live stage the stage's prefix, as `code_instance` already does for ids. I test with a scratch wrapper, `build_names.py`, that runs today's `guide_build.py` with exactly this change (one regular expression after `prefix_ids`); with it both sets pass, and `codeMatch` is unaffected since the pasted page holds one copy.
2. **`white-space` reads as a literal color.** `CODE_NAMED` matches "white" in `white-space`, so a set that writes `white-space: nowrap` (Rule 11.13's own builders line asks for it) gets "the CSS sets 1 literal color(s) (white)". I worked around it with `display: inline-block` for the link's last word and the ID, which also never breaks inside, and dropped `white-space` from the visually hidden class. A lookbehind for a hyphen or a property name (`(?<![\w-])white(?![\w-])`) would fix it.
3. **`data-oa-theme-for` is prefixed today only by chance.** `prefix_ids` rewrites `\bfor="..."`, and the `\b` also matches inside `data-oa-theme-for`, so the switch's target reference does follow its id into each stage. Naming `data-oa-theme-for` in `ID_REF_ATTRS` would keep that from breaking if the pattern is ever tightened.
4. **The theme switch's head script** sits at the top of `c-18-theme-switch.js` as a commented block, because the HTML may hold no `script` and the live stage must never run it (it would set the guide's root). If you would rather show it as a fourth panel, "Head script", that the live stage never runs, I would move it to `c-18-theme-switch.head.js`.
5. **AX-S8:** I agree with the accessibility lead's proposal (its notes, "Landmarks in a live stage"): in the live stages only, `code_instance` draws each landmark element (`header`, `nav`, `search`, `footer`, `aside`) as a `div` with `role="group"`, its name and `data-oa-landmark`; the panels and `codeMatch` keep the real elements. My CSS never selects a landmark by its tag, only by its `oa-` class, so both draw alike.

## For the accessibility lead

- **AX-S8, settled from my side:** your proposal (the build swaps landmark elements for named groups in the live stages only) is what my sets are written for. 18.6's masthead is `header` and `nav`, 18.7's breadcrumb and lists are `nav`, 18.15's search is `<search>` around its label, field, Clear and status line, with no named `form`. No set selects a landmark by its tag. Please log the call.
- **Keys hooks:** each batch above lists its selectors and its exact status words. My toggle chips are `.oa-toggle--chip`; `.oa-chip` is the typed ID chip (18.24).
- **Radios and the guide:** 18.3 and 18.4 need the build change "For the guide engineer", item 1, before their keys paths can pass in both stages.
- **Your keys files and my sets.** Thank you for writing them early. Where they differ from what I built, the batch tables above give my hooks. Most differences are names (`.oa-toggle--chip`, `.oa-code-copy`, `.oa-copy-button`, `.oa-scroll-frame`, `a.oa-chip--link`, `.oa-link-vh`) and start states (18.2's first chip loads on, 18.8's first disclosure loads open, 18.10 loads sorted by Bill, 18.9 has a fourth, unavailable tab), chosen so the live stage shows the on, open and sorted looks before anyone presses a key. For the sets still to come I take your class names: `.oa-filters-toggle`, `.oa-filters-clear`, `.oa-form-send`, `.oa-search-clear`, `.oa-stepper-play`, `-reset`, `-prev`, `-next`, `.oa-reader-prev`, `-next`, `.oa-diagram-item`, `.oa-masthead-home`, `.oa-masthead-menu`.
- **18.4, one real difference.** Your theme path checks Light in the light stage and Dark in the dark stage at load, and sets the stage itself (`"el": ""`). My switch follows D2-1147 instead: Match my device is checked first in both stages, and the switch sets `.oa-theme-page`, a sample page inside the stage that its markup carries, named by `data-oa-theme-for`. The stage is outside the markup a builder copies, so the code cannot name it. On the nested sample, Match my device sets `data-oa-theme="device"`, which follows the theme the sample sits in, so each stage stands for a device set to its theme. A path that fits: Tab lands on `input[value="device"]` (checked); ArrowLeft checks Dark and sets `.oa-theme-page` to `dark`; ArrowLeft again checks Light and sets `light`; `:root` stays `light` and `{"storage": "oa-theme", "is": null}` holds throughout. If you would rather the stage itself change, the build would need to give the stage an id the markup can name, which I do not recommend: the copy would then carry a guide-only id.
- **Illustrative:** a set whose content is made up carries a small "Illustrative" tag beside the item it labels (the chip group in 18.2), outside any accessible name.

## Routine calls

- D2-xxx | Each set's classes start with its own name (`oa-button-`, `oa-toggle-`, `oa-choice-`), and each set styles everything it holds | In the guide all 24 sets' CSS is on one page, and a builder copies one set at a time
- D2-xxx | Utility icons are drawn inline from the 24 px and 16 px masters, with `data-icon` and `data-icon-family` | A builder's page has no sprite; the attributes let the shared checks find each icon
- D2-xxx | Every script runs inside its own function and finds each copy of its component | All sets' scripts share one page in the guide, and two copies show in each plate
- D2-xxx | A short name that is `initial` in the dark theme is read with a fallback (the ask's keyline falls back to its fill, the Error Band to transparent) | `var()` of a guaranteed-invalid value would otherwise fall to the property's initial value, a keyline in the label's color
- D2-xxx | Hover rules skip a control with `aria-disabled="true"` | An unavailable control does not answer a pointer
- D2-xxx | A choice's native radio stays in the page, transparent over its face, and the face draws the check, bold word and edge | The radio keeps Tab, the arrow keys and "2 of 3" with no script; the whole face is the target
- D2-xxx | An unavailable radio choice uses the native `disabled`, with its reason in visible words below the row | A radio group's arrow keys skip a disabled choice; `aria-disabled` would let the arrows check it
- D2-xxx | The theme switch's target is `data-oa-theme-for`, an id; absent, the page's root. A named target that is missing sets nothing | The guide's specimen changes only its own stage, and never falls back to the guide's root
- D2-xxx | Only a switch that sets the root stores the choice | Storage holds the page's choice; a nested specimen that stored would recolor the guide's other stage on the next visit
- D2-xxx | On a nested target, Match my device sets `data-oa-theme="device"`, which follows whatever theme the target sits in | tokens.css follows the device only on the root; in the guide, each stage stands for a device set to its theme, and the dark-device check stays clean
- D2-xxx | The theme switch keeps every switch that sets the same element on the same choice | A product may show it in the masthead and again in the phone menu
- D2-xxx | The link to another site keeps only its last word and the mark together, in an inline block | F-3 and D2-1156; the build reads `white-space` as a color today
- D2-xxx | The skip link is the first stop and shows on focus at the top left of its component | WCAG 2.4.1; it moves focus to the main content, which carries `tabindex="-1"`

## Questions for Dustin

None so far.

## Tested

## Not tested

## Change log
