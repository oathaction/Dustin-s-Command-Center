# Board 2 cartographer notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. The cartographer, a senior news cartographer (general-purpose, as round 3's, D3-1082), under `work/handoffs/phase-3/20261113_Board-2-Brief.md`: A2's drawing, A4's layout check and the board-only pictures. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/cartographer/`. Written as I go; the container can restart.

## Status

- 17:17 UTC. Started 17:07. Read CLAUDE.md, the brief, the decision log from D3-1312 to DR-260 (and D3-1538 to D3-1541), my round 3 notes, the data lead's round 3 D-1 and Q2, the kit README, and the other owners' first notes.
- **A2: drawn, waiting on the editor's words and the data lead's sign-off.** `work/build/guide/specimens/s-14-124-sketch.html` now draws the misleading half in red `#CC0000` and blue `#2C7BB6`, 3,932 bytes (was 3,817; limit 4,096). The better half is byte for byte as signed off. The gray "before" is `work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before.html`. The first `<desc>` carries my draft of the caption (below, "Words for the editor") until the editor's words land; I then set it to match `sketch_alt`'s first sentence exactly.
- A4: waits on the editor's S16 words.
- S12 stacked tile: started 17:17.

## A2: sketch 14.124 in red and blue (DR-255)

**Before.** Today's gray file, copied before any change: `work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before.html`, 3,817 bytes, SHA-256 `2006ce0ceafafd1b95bf6be0e4c86f3a2dc49828d74084d32d337b2198d5dc06`, the same as the committed `s-14-124-sketch.html` (last changed in commit `572ac794`). It is the guide's fragment: two `<svg>` elements in the kit's role classes. It draws only inside a page that loads `tokens.css` and `kit.css` with a surface class, as the guide's stage does; the board builder photographs it that way (see "For the board builder").

**After.** The misleading half's places and key swatches take literal fills, with no `oac-f-*` class:

| Party | Places | Fill | Key words |
|---|---|---|---|
| Party A | 7 small squares | red `#CC0000` | "Party A, red" |
| Party B | 5 large blocks | blue `#2C7BB6` | "Party B, blue" |

Every place and both swatches take a 1 px edge in the context ink (`oac-s-context`), half a pixel inside its outline, as the better half edges every won seat. Data, places, sizes, positions and words other than the key are unchanged; the bar over the half is the guide's own (`plate-dnp`, "Form to avoid / Do not publish"), which `guide_build.py` sets over the first `<svg>` of an avoid pair.

**Why these two inks.** Measured by `scratch/tools/colors.py` against all 39 hex values in `tokens.css` and all 45 in `tokens.json` (the 39 plus its held reds `#AC3339` and `#DA3843` and four composites), by CIEDE2000:

| Ink | Nearest guide values (ΔE 2000) | Pillar Red | Prussian | On Newsprint | On Charcoal | Gray under CSS `grayscale(1)` |
|---|---|---|---|---|---|---|
| `#CC0000` | `#AC3339` 11.9, `#DA3843` 12.0, `#E63946` 13.4 | 13.4 | 44.3 | 4.18 to 1 | 3.18 to 1 | 43 |
| `#2C7BB6` | `#505C7D` 16.5, `#828A9D` 17.1, `#5D636D` 18.0 | 47.9 | 28.3 | 3.23 to 1 | 4.12 to 1 | 110 |

- Neither value appears in either token file. Each sits 70 or more a channel from Pillar Red (230, 57, 70) and Prussian (31, 45, 90), far past the guide check's 8-a-channel tolerance, so no check reads either as a guide ink.
- The red is a plain, pure red with no pink (CIELAB hue 40 against Pillar Red's 27, and darker); a red as light as Pillar Red came within 5 to 9 of it or of the held reds. The blue is a plain mid blue, far from Prussian's navy.
- Both reach 3 to 1 against both grounds without their edges. The edge keeps the red places apart from the Charcoal ground in grayscale, where the red falls to gray 43 against the ground's 18.
- In grayscale the two parties stay apart (gray 43 and 110 on both grounds), and the key's swatches match their places, so "Party A, red" and "Party B, blue" carry the lesson.

**Looked at** (`scratch/a2-viewer.html`: the strict build's own styles and plate markup from the main session's 15:29 build, before and after, each on Newsprint and Charcoal; photographed at 1x and 2x, in color and in grayscale, `scratch/shots/a2-*.png`): the two inks read as a news map's red and blue on both grounds; every place keeps its edge; at 1x on Charcoal in grayscale the red places read as dark squares with light edges and the blue blocks as mid gray, and the key matches both. One change from the gray version: in grayscale the large blocks (Party B, blue) now read lighter than the small ones (Party A, red), where the gray drawing put Party B in the dark step (D3-1474). A blue darker than this red in grayscale would sit near Prussian, and the land-for-votes harm still shows by area.

## Routine calls

- D3-xxx | Sketch 14.124's misleading half takes red `#CC0000` and blue `#2C7BB6` as literal fills, with a 1 px context edge on every place and swatch | DR-255: a plain news red and blue, measured against every value in both token files (ΔE 2000 at least 11.9 from every guide ink, 3 to 1 or more on both grounds, apart in grayscale)
- D3-xxx | Party A stays red and Party B blue, as the signed-off key named them | The least change; Party B's few large places in blue match no real map's pattern, so the sketch points at no one party (DR-124)
- D3-xxx | The key reads "Party A, red" and "Party B, blue" | The places are now red and blue, so "shown red" no longer fits; the words keep the lesson in grayscale. The editor may reword

## Words for the editor (A2)

- **Caption and first `<desc>` (draft, in the file now):** "A map shaded red for one party and blue for the other, which takes a side at a glance and makes a party that wins a few large places look bigger than its count." This is today's first sentence with "Drawn here in gray: " dropped; it already names both colors. Entry 14.124's `sketch_alt` still opens "Drawn here in gray: ", so `phase3_ch14_build.py` will fault until the two match. Set `sketch_alt` to your words and tell me under "Words for the cartographer"; I set the `<desc>` to your first sentence character for character.
- **The key:** "Party A, red" and "Party B, blue" (were "Party A, shown red", "Party B, shown blue"). Change them if you want other words; each must name its color.

## For the engineer (A3)

- The misleading half is the first `<svg>` of `s-14-124-sketch.html`. Its literal fills are `fill="#CC0000"` (Party A's seven places and swatch) and `fill="#2C7BB6"` (Party B's five places and swatch) on elements with no class. No `style`, no `data-party`, every word 13 px in the kit's classes. If you want an attribute on that `<svg>` for the exemption, name it and I add it (the file has 164 bytes of room).

## For the data lead (sign-off of A2)

- Please sign off at 1x and 2x, on both grounds and in grayscale. My pictures: `scratch/shots/a2-after-{newsprint,charcoal}-{1x,2x}[-grayscale].png`, with the gray "before" as `a2-before-*`.

## For the board builder

- `20261113_S-14-124-Sketch-Gray-Before.html` is the guide's fragment, not a page: it needs `tokens.css`, `kit.css` and a surface class (`oa-surface-newsprint` or `oa-surface-charcoal`) around it, as the guide's plate stage gives it. The "after" is the strict build's own plate, `fig-s-14-124-sketch`, once A6 passes.

## Tested

- `colors.py` (17:16 UTC): the two inks against every hex value in `tokens.css` (39) and `tokens.json` (45), CIEDE2000, contrast on both grounds, gray value; neither value appears in either file.
- `sketch_a2.py` writes the new file from the gray one by script: 3,932 bytes; the better half equal byte for byte; no `style`, no em dash, every font size 13.
- Photographed in Chromium (Playwright) inside the strict build's own styles and plate markup, at 1x and 2x, Newsprint and Charcoal, color and grayscale; gray values read from the pixels: blue 110, red 43, the Charcoal ground 18, the red places' edge 138, the Newsprint ground 217.

## Not tested

- The guide check, the chapter build and the strict build on the new sketch (the engineer's A3 and A6; the guide check is the main session's).
- Forced colors by eye (the kit's CSS keeps a literal fill in forced colors; the words take the system inks).
