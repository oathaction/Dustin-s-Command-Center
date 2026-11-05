# Editorial atlas systems: the fix pass

November 5, 2026. Every maker reads this after the four red team reports. Keep your system's idea; fix what stops it from teaching, working, telling the truth or holding the brand. Do not drift toward the other systems.

## The four reports

Read your own section in each, then the shared sections:

| Report | Your section |
|---|---|
| `work/handoffs/phase-2/20261105_Red-Team-Civic-Education.md` | "System N" under section 1; section 2, "What to borrow" and "Fixes every system needs" |
| `work/handoffs/phase-2/20261105_Red-Team-Interface-Accessibility.md` | "Shared defects" X1 to X6; your numbered section |
| `work/handoffs/phase-2/20261105_Red-Team-Evidence-And-Brand.md` | "Shared findings" S1 to S4; your "0N" section |
| `work/handoffs/phase-2/20261105_Reader-Panel.md` | your version (A Times Explainer, B Economist Register, C Reference Sheets, D Night Edition, E Architecture) |

Fix every Must fix and Should fix in your sections. Take Polish items where they are quick. Borrow an idea from "What to borrow" only where it serves your system's own idea.

## Fixes every system makes

1. **The first screen shows the system.** At 1440 by 900, the first screen of the overview names all eight parts with their plain names and questions and shows the main relationships between them. A reader who sees only that screen for ten seconds can name the parts and say how they connect. On a phone, this holds within the first two screens. The reader panel found this was the biggest miss in every version.
2. **Disclosures wherever a reform is argued** (D2-80). Any reform shown with more than its title carries its disclosure line when the dataset has one. On the R-01 page, one labeled box near the top holds "The Atlas takes no position" first and the disclosure second, set apart from the reform's case, so it reads as a disclosure and never as backing.
3. **Dates on the ballot measures.** Every mention of the November 3, 2026 ballot opens "As of October 15, 2026," and never suggests the vote is still ahead or states a result.
4. **Headlines claim no more than the data.** Fix each overclaim the evidence report names. A loop that closes through a plausible step is described as one that can sustain itself, not one that does.
5. **Steps read in the direction the loop runs**, matching the read-aloud line ("More seats settled in the primary means less risk of losing office"). Use "fewer" for countable things ("fewer incumbents defeated").
6. **Reform effects in words.** "Moderate positive" in words, with no plus or minus glyph or code beside it.
7. **Red discipline.** Sign tags never take red. On the loop and reform pages, red marks only R-01's targets: their line, arrowhead or target box. No working red on the overview, Elections or the catalog unless DR-18's selected item takes it with no reform in view.
8. **The panel never hides what the reader picked.** On desktop, run the panel as a column the layout makes room for. On a phone, scroll the tapped item into the band above the sheet before it opens.
9. **Small phones.** No text under 13 px and no clipped drawing at 360 px and 320 px. Give phone figures `width: 100%` and a viewBox drawn for 320 px. The shared check now audits 360 px (D2-82).
10. **Keyboard.** A skip link that focuses the view's `h1` and keeps the view's hash; a readout line "Arrow keys move between items. Enter opens one." when a drawing takes focus; `#area-a` and the other part keys accepted as aliases, with a visible status line for an unknown hash.
11. **The loop catalog teaches on its own.** Under each loop's title, the first sentence of its summary. R1's card carries its qualification.
12. **An evidence key** wherever evidence textures appear, the overview included.
13. **Palette and wordmark.** No color outside the locked palette and the two approved tints; the name appears only as the wordmark master, never in live type.

## Then

1. Rebuild, render and look at every view at 1440, 390 and 360 px. Make at least one full refinement pass on craft after the fixes.
2. Run both checks until they pass (the rendered check now covers three widths):
   - `python3 -I work/build/scripts/phase-2/atlas_concepts_verify.py <page>`
   - `node work/build/scripts/phase-2/atlas_concepts_check.js <page>`
3. Add a "Fix pass" section to your notes: each finding you were given, what you changed, or why you left it.
4. Reply in under 200 words: what changed most, the check results, and anything you could not fix.

Same limits as before: write only inside your folder and your notes; do not commit.
