# Round 4 cartographer notes: phone codes and S12's stacked tile

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. The cartographer, a senior news cartographer (general-purpose, as round 3's and board 2's). Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, the cartographer row and its "Cartographer" bullet, under DR-261 and D3-1553. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch (`scratch/` below): `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/cartographer/`. Written as I go; the container can restart.

## Status

- 21:43 UTC (clock read). **Done.** S12 on the stacked tile (DR-261) and S12, S16 and S78 coding all 51 states at the 326 px phone drawing (D3-1553), each on its landed kit change (R4-2, C4-E2, C4-E1). Every check below passes. Waiting only on the data lead's sign-off of the phone codes (D4-2 for S16, D4-3 for S12 and S78). Nothing blocking.
- 21:37 UTC (clock read). **S16 placed on C4-E2** (landed 21:35:40 in `forms/bubble-map.js`, byte-identical to my revised patch): `s16.json` takes `labels.column_phone` and a `notes_internal` line naming the radius check; entry 14.116's builders line names the key. `build s16`, sweep on: PASS, 0 faults; `cartographer_round4_derive.py`: S16 coded 51 of 51 at 326 px and its radius check passes (D4-1 condition 1); the four faults left are S12's and S78's, which wait on C4-E1.
- 21:36 UTC (clock read). Routing from the main session: C4-E2 goes to the component engineer with the revised 1,121-byte patch; C4-E1 (a token value) to the engineer after its card work; no size allocation holds either back (DR-271). S12's before and after captures gathered in `scratch/board3/s12/`.
- 21:02 UTC (clock read). **S12 placed on the landed stacked tile** (`s12.json`: `stage_min` 618, the alt's clause, one `notes_internal` line): `build s12`, sweep on, PASS, 0 faults. **D4-1 ruled (A), the column** (20:57). Waiting on the engineer for C4-E1 (tile gap) and C4-E2 (S16's column, after the tile); then I add `labels.column_phone` to `s16.json`, name the radius check in its `notes_internal`, and run the closing checks. `cartographer_round4_derive.py` written: PASS on the mirror with both changes, FAIL with the six expected faults on the repository until they land.
- 20:56 UTC (clock read). **Phone codes: measured, two kit requests out (C4-E1, C4-E2), one choice for the data lead (D4-1).** No repository file changed yet. S12's stacked tile: ruling (d) signed off at 20:52; I write `s12.json` when the engineer marks the tile LANDED.
- 20:40 UTC. Started.

## Summary

At the guide's 326 px phone drawing (a 390 px window), before this round:

| Spec | Codes drawn at 326 px | Left to the note | Why |
|---|---|---|---|
| S12 (phone tiles) | 48 of 51 | WA, WV, WY | Tiles of 24 px; "WA" and "WV" measure 22.72 px and "WY" 22.53 px at 13 px semibold, past the 22 px a tile holds with 1 px a side |
| S78 (phone tiles) | 48 of 51 | WA, WV, WY | The same tile grid and test |
| S16 (bubbles) | 47 of 51 | DC, DE, ME, NH | The Northeast is boxed in by the drawing's right edge; no clear place within reach |

Now, each change tested first in a scratch mirror of the kit, then landed by its owner and placed by me:

- **S12 and S78: a 2 px tile gap on phones (C4-E1, landed by the engineer in tokens 6.0.0-gate3.3 at 21:38).** Tiles become 25 px at 326 px and every code fits with 1.14 px or more a side: all 51 coded on both maps from 322 to 479 px (today from 328), 0 faults. Under 322 px nothing gets worse (300 px: 43 coded, today 41; 296 px: 41, as today).
- **S16: a column of codes on the ocean for the small northeastern states, on phone drawings narrower than 358 px (C4-E2, ruled (A) by the data lead in D4-1, landed by the component engineer at 21:35).** At 326 px all 51 coded, with fewer leaders crossing a circle (11, today 15) and a shorter longest leader (72 px, today 104). From 358 to 479 px the drawing is identical to today at all 122 widths. Across 300 to 357 px the codes left out fall from 217 to 44 (summed over the 58 widths).
- **S12 at a desk: the stacked tile (DR-261),** placed at 21:01 on the engineer's landed tile with `"stage_min": 618`: in the column from a 1,104 px window, a 618 px frame scrolling 62 px at 1,024, measured in the guide page; signed off by the data lead at 21:03.

| Spec | Codes at 326 px now | Plate as the guide places it, before and after | Spec file, before and after |
|---|---|---|---|
| S12 | 51 of 51 | 13,153 and 13,206 bytes (+53, `stage_min` and the alt's clause) | 6,281 and 7,264 bytes |
| S16 | 51 of 51 | 10,183 and 10,235 bytes (+52, the column's list) | 5,956 and 6,835 bytes |
| S78 | 51 of 51 | 8,656 and 8,656 bytes | 6,192 and 6,570 bytes (one `notes_internal` line) |

Entry 14.116: 2,088 and 2,209 bytes (its builders line names `labels.column_phone`). Entries 14.115 and 14.117 unchanged: their phone words still hold (14.117's "each code on its square" is now true at 326 px). Kit: `bubble-map.js` +1,121 bytes minified (C4-E2); C4-E1 is a token value.

## Routine calls

- D3-xxx | The phone codes are fixed by the tile grid's gap (S12, S78) and a code column (S16), each in the kit by request; no font size, weight, word or ink changes | Rule 13's type floor is 13 px for tile codes (`type-tile-code-phone`), and D3-1325's 1 px a side stands; the only free variable is room
- D3-xxx | S16's column takes ME, NH, VT, MA, RI, CT, NJ, DE, MD, DC and WV, ordered by their circles from north to south, slots 16 px apart as near each circle's height as the pitch allows | Of four lists tried, this one left the fewest codes out with no leader thrown below Florida (lists without WV threw one at 326 px; adding VA, NC, SC and GA cost crossings and two sweep faults)
- D3-xxx | S12 takes `"stage_min": 618` in place of `"stage": 1024`, and its alt's desk clause reads "each square holds the state’s code over its figure, with an arrow beneath" | DR-261 and ruling (d); the scroll clause stays, since the frame still scrolls below a 618 px column; `phone_note` is not printed and still holds
- D3-xxx | C4-E2 drops `labels.column_under`; the phone artboard's token alone sets the 358 px limit | 274 page bytes less, the same drawing at all 448 phone drawings
- D3-xxx | `cartographer_round4_derive.py` holds this round's checks (codes at 326 and 296 px on S12, S16 and S78; S16's radii, shades and key against the layout without the column), and S12's, S16's and S78's `notes_internal` name it | D4-1 condition 1 asks for a check by script named in `notes_internal`; no layout table is derived this round
- D3-xxx | S16's column applies only under the phone artboard's 358 px | Today's search codes all 51 at 358 px (board 1's phone width, D3-1329, D3-1527), and the column there would drop NC; at 358 px and over nothing changes

## Requests

### To the engineer

- **C4-E1, the phone tile gap (S12, S78; D3-1553).** `--oa-chart-tile-phone-gap` from 2.5 px to 2 px (`work/build/tokens/src/oa-tokens.src.mjs`, `tile.phoneGap: chartDim(2.5, ...)`; diff of the built file in `scratch/requests/C4-E1_tile-phone-gap.diff`). At 326 px `K.parts.tiles` then gives 25 px tiles at a 27 px pitch, every tile edge on a whole pixel, and the widest codes ("WA", "WV", 22.72 px) fit with 1.14 px a side. Tested by patching `P.tiles` in the mirror (`gap = c.phone ? 2 : ...`): S12 and S78 code all 51 at 322, 326, 327, 328, 358, 390 and 479 px, 0 drawing faults at each. S07's phone tiles also grow 1 px (S07 draws no codes on a phone at these widths; 0 faults), so S07 would join board 3's list of changed drawings. If you would rather leave S07, a form-level gap for the two forms that code their tiles (`tile-map-shift-arrows`, `choropleth`'s phone tiles) does the same; no spec key is needed either way. No page bytes either way but a token value.
- **C4-E2, a code column on S16's phone drawing (D3-1553; the data lead ruled (A) at 20:57, D4-1, to land after the tile). Revised 21:34 UTC, smaller.** `forms/bubble-map.js` takes `labels.column_phone` (codes): on a phone drawing narrower than the token `artboard-phone` (358 px), and not in the narrow mode under 300 px, the map fits narrower by the widest listed code plus 10 px, and the listed states whose circles cannot hold their code take a column at the right edge, north to south, slots 16 px apart, each as near its circle's height as the pitch allows (adjacent blocks pooled, so every run matches), each on a hairline leader from its circle's edge to 2 px short of its code; the search places the rest around them and keeps clear of the column's leaders. Circle sizes never change (the radius depends on the token, not on the map's scale). Patch: `scratch/requests/C4-E2_bubble-map-column.diff` (76 lines; the whole form is `C4-E2_bubble-map.js`). **Page cost: the form grows from 10,455 to 11,576 bytes minified (+1,121; my first patch was +1,395, and `labels.column_under` is dropped).** The revised form draws the same SVG as the first at all 448 drawings from 256 to 479 px on both grounds (compared by script; the control against today's kit differs at exactly the 116 drawings from 300 to 357 px). Tested in a mirror: `build` of the S16 I will write (`scratch/draft/s16.json`) with the sweep: PASS, 0 faults, plate 10,235 bytes as the guide places it (+52, the list in the island); `cartographer_round4_derive.py` on the mirror with C4-E1 and C4-E2: PASS, 0 faults. Until it lands I add nothing to `s16.json`, since the kit fails a label key the form does not read.

### To the data lead

- **D4-3, sign-off of S12's and S78's phone codes (C4-E1 landed 21:38).** No spec change draws them: the token sets 25 px tiles at 326 px, and every state's and DC's code sits on its tile with 1.14 px or more each side (before: WA, WV and WY in the note). Each spec gains one `notes_internal` line naming the check. `cartographer_round4_derive.py` on the repository: PASS, 0 faults (S12 and S78 51 of 51 at 326 px; at 296 px 41 of 51, the other ten named in the note, as before). `build s12 s78`, sweep on, both grounds, kit pages 1440, 787, 682, 622, 390, 358, 328 and 288 px: PASS, 0 faults (21:38). Weights unchanged by the gap: S12 13,206, S78 8,656 bytes as the guide places them. Captures: `scratch/after2/kit-out/s12/`, `s78/`; before and after side by side in `scratch/board3/s12/` and `s78/`. Figures, inks, words and the gray steps unchanged. S07's phone tiles also grow 1 px (it draws no codes on a phone), so it joins board 3's list; it is not my spec.
- **D4-2, sign-off of S16 as placed (21:36 UTC), with S12's phone codes to follow on C4-E1.** `s16.json` adds only `labels.column_phone` (ME, NH, VT, MA, RI, CT, NJ, DE, MD, DC, WV) and a `notes_internal` line; entry 14.116's builders line names the key. Your condition 1: `python3 -I work/build/scripts/phase-3/cartographer_round4_derive.py` compares S16 as placed with S16 drawn without `labels.column_phone` at every width from 300 to 357 px: 2,958 circles, each the same radius to 0.01 px, the same shade and the same key words; 122 of 122 drawings from 358 to 479 px the same SVG (the component engineer measured the radii to 0.005 px at all 614 widths). Condition 2: the engineer's next strict build gives the share. `build s16`, sweep on, both grounds at kit pages 1440, 787, 390, 358, 328 and 288 px: PASS, 0 faults, 10,235 bytes as the guide places it. Captures: `scratch/after/kit-out/s16/` (the 326 px drawing is the 358 page), before and after side by side in `scratch/board3/s16/`. Title, measure, notes, source, inks and figures unchanged.
- **D4-1, S16 at 326 px: the column, or the note (D3-1553's "a ruling where a choice is needed").** (A) The column (C4-E2): every state coded at 326 px; 22 leaders, 11 crossing another state's circle (today 14 and 15), longest 72 px (today 104); the eleven column codes sit 41 to 84 px from their circles by design, in latitude order; the South's codes stay the search's, as today (GA's sits under Florida at 326 px, where today MD's does). Unchanged from 358 px up. Costs 1,395 bytes of renderer (1,121 after the revision). (B) The note as today: "Not labeled at this width: DC, DE, ME, NH. The table names every one." Pictures: `scratch/exp/s16-o-map.png` (today, 326 px, 3x), `scratch/exp/s16-w3-map.png` (column, 326 px, 3x), `scratch/exp/s16-col-charcoal-326-map.png` (column on Charcoal, the kit's own export). I recommend (A).

### To the main session

- **S07 on a phone, outside D3-1553:** S07's tiles are now the same 25 px at 326 px that hold every code on S12 and S78, but `tile-map-categorical` draws codes only when a tile holds "WW" with 2 px a side (31 px tiles), so its phone drawing still prints none and says the table names every state. Coding S07's tiles at 326 px as S78's are coded (each where it fits with 1 px a side) would be a small form change for its owner and a board 1 drawing change for the data lead; I have made none.

## S12's stacked tile (DR-261, ruling (d))

**Placed at 21:01 UTC** (the tile LANDED at 20:57), from the draft below, unchanged. Drafted in scratch first: `scratch/draft/s12.json` changes `s12.json` in three places only: `"stage_min": 618` where `"stage": 1024` stood; the alt's desk clause reads "At a desk each square holds the state’s code over its figure, with an arrow beneath as long as the state’s shift ..." (was "holds an arrow as long as the state’s shift ..."), the scroll clause and every other word kept, since the frame still scrolls below a 618 px column; and one `notes_internal` line. `phone_note` stays: the kit does not print it, and its words still hold. Built against a copy of the engineer's mirror kit (20:57 UTC): PASS, 0 faults, sweep on; drawings at 1024, 723, 618, 618 (the 558 px column, framed) and 326 px; 13,206 bytes as the guide places it, about 13,956 with its frame, under 15,000 (ruling (d) gives 14,076 by the page measure). Looked at: 618 px on Newsprint (every tile holds its code, figure and arrow) and the 558 px column's frame (the hint above it; ME, NH and RI past the edge until the reader scrolls).

**In the guide page** (a strict build of my own in a scratch mirror of the repository, 21:15 UTC, exit 0, 11,283,656 bytes; measured in Chromium at each window, both grounds, 0 page errors, `scratch/tools/guide_s12.cjs`):

| Window | Drawing | Frame's box | Shows | Scrolls | Tab stop and hint |
|---|---|---|---|---|---|
| 1,440 | 723 | 722.67 | 723 | 0 | none |
| 1,104 | 618 | 617.98 | 618 | 0 | none |
| 1,103 | 618 | 617.25 | 617 | 1 | none (see below) |
| 1,024 | 618 | 558 | 556 | **62** | yes, with 1 px edges |
| 390 | 326 (phone) | 326 | 326 | 0 | none |

DR-261 holds to the pixel: the stacked tile in the column from a 1,104 px window, a 618 px frame that scrolls 62 px at 1,024. **For the engineer, an observation, not a fault:** where the column falls less than 1 px short of 618 (1,103 px windows), the frame scrolls 1 px with no tab stop or hint, since `stage_stop` needs 1 px of overflow before it calls the frame scrolling. The pixel hidden is the last column's tile edge, inside the cell's 1 px spare; no code, figure or arrow is cut.

## Pixels changed, for board 3

Before captures are the kit's at 20:44 UTC (before any round 4 change); after captures are the kit's at landing. Kit pages give the guide's drawings: page 787 the 723 px drawing (a 1,440 px window), 682 the 618 px drawing (a 1,104 px window), 622 the 618 px frame in a 558 px column (a 1,024 px window), 358 the 326 px phone drawing (a 390 px window).

| Drawing | What changed | Widths whose pixels changed | Before and after (in `scratch/board3/`) |
|---|---|---|---|
| S12, desk (DR-261) | Board 1's 1024 px stage in a sideways frame becomes the stacked tile: each state's code over its figure, the arrow beneath, in the column from 618 px, in a 618 px frame that scrolls 62 px below that | every desk drawing (480 px and wider) | `s12/before-page-787-*.png`, `before-page-682-*.png`, `before-drawing-1024-stage-*.png`; `s12/after-page-787-*.png`, `after-page-682-*.png`, `after-page-622-framed-*.png`, `after-drawing-723-*.png`, `after-drawing-618-*.png` (Newsprint and Charcoal each) |
| S16, phone (D3-1553, D4-1) | A column of codes on the ocean for ME, NH, VT, MA, RI, CT, NJ, DE, MD, DC and WV, the map fitted that much narrower; the search's other codes move with it; circle sizes, shades, key and words unchanged | phone drawings from 300 to 357 px (326 among them); none from 358 px up, none under 300 | `s16/before-*-326-*.png`, `s16/after-*-326-*.png` (Newsprint and Charcoal), `s16/before-map-326-newsprint-3x.png` and `after-map-326-newsprint-3x.png` |
| S12, phone (C4-E1) | Tiles 1 px larger with 0.5 px narrower gaps; WA, WV and WY now carry their codes at 326 px and the "Not labeled" note goes; gray steps, lists and frames unchanged | every phone drawing, 256 to 479 px (448 drawings on both grounds differ from the 2.5 px gap, compared by script); codes gained from 300 to 327 px | `s12/before-phone-page-358-drawing-326-*.png`, `before-phone-drawing-326-newsprint-2x.png`; `s12/after-phone-page-358-drawing-326-*.png` |
| S78, phone (C4-E1) | The same tile change; WA, WV and WY coded at 326 px | every phone drawing, 256 to 479 px; codes gained from 300 to 327 px | `s78/before-phone-page-358-drawing-326-*.png`, `before-phone-drawing-326-newsprint-2x.png`; `s78/after-phone-page-358-drawing-326-*.png` |
| S07, phone (C4-E1, the token) | Tiles 1 px larger with narrower gaps; no codes on a phone, as before | every phone drawing, 256 to 479 px | `s07/before-phone-page-358-drawing-326-*.png` (drawn by the kit with the 2.5 px token restored in a scratch mirror), `s07/after-phone-page-358-drawing-326-*.png` |

Desk drawings of S07, S16 and S78 do not change (the desk tile gap is 6 px; S16's column is phone only).

## Tested

- `node work/build/chart-kit/oa-chart.mjs build s12 s16 s78 --widths 1440,787,682,358 --no-sweep --out scratch/before/kit-out` (20:44 UTC): 3 of 3 PASS, 0 faults; the "before" captures for board 3 (kit pages 358, 682, 787 and 1440 px give the guide's 326, 618 and 723 px drawings and the 1024 px stage). Before copies of the three specs and three entries in `scratch/before/`.
- By the kit's draw (no browser, `scratch/tools/probe_codes.mjs`), codes drawn today at 256, 296, 300, 326, 358 and 390 px on S12, S16 and S78 (table above); code widths by `K.measure` at 13 px.
- In the mirror (`scratch/tools/mirror.sh`: the chart kit copied, tokens, fonts, data and atlas extract linked read-only): the 2 px phone gap on S12, S78 and S07 at nine widths; S16 with longer reach, finer rings, a right margin, and four column lists; `scratch/tools/quality.mjs` over every whole width from 300 to 479 px for today and each column list (codes, leaders, crossings, distance); the column variant's kit `build` with the sweep (above).
- Looked at, 3x, Newsprint: S16 at 326 px today, with three search settings, and with three column lists; the chosen column on Charcoal from the kit's export at 2x.

- After landing, on the repository: `build s12 --widths 1440,787,682,622,390,358,328,288` with the sweep (21:01, PASS, 0 faults); `build s16 --widths 1440,787,390,358,328,288` with the sweep (21:36, PASS, 0 faults); `build s12 s78` at the same eight pages with the sweep after C4-E1 (21:38, PASS, 0 faults each); `build s07 --widths 358 --no-sweep` (PASS); `check s12 s16 s78` with the sweep after the last `notes_internal` lines (21:41, 3 of 3 PASS, 0 faults).
- `python3 -I work/build/scripts/phase-3/cartographer_round4_derive.py` on the repository (21:42): PASS, 0 faults (S12, S16 and S78 51 of 51 at 326 px; their 296 px notes name every code left out; S16 radii, shades and key equal at 58 widths, 2,958 circles; 122 of 122 drawings the same from 358 to 479 px). Earlier the same script on the repository failed with exactly the expected faults while C4-E1 and C4-E2 were unlanded (six, then four), and passed on the mirror with both.
- C4-E2 as landed: `bubble-map.js` byte-identical to my revised patch (`cmp`); the revised and first patches draw the same SVG at 448 of 448 phone drawings; the control (column spec on the old kit) differs at exactly the 116 drawings from 300 to 357 px.
- C4-E1 as landed: the token diff is the gap and its version notes only; S07, S12 and S78 each differ at 448 of 448 phone drawings against a mirror with the 2.5 px token.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py --check --rounds 1,2,3,4` (21:41): 98 of 98 files current, so nothing to write.
- Strict builds of my own in a scratch mirror of the repository (so the kit's `plate-share.json` is not rewritten): 21:15, exit 0, 11,283,656 bytes; 21:41, exit 0, 0 warnings, 11,500,848 bytes, 360 rules, 657 specimens. The repository's `plate-share.json` changes in `git status` are other owners' builds (written 21:14:58 and 21:41:20; mine wrote the mirror's copy).
- S12 in the guide page at 1,440, 1,104, 1,103, 1,024 and 390 px windows (table above).
- Looked at: S12 at 723 px on Charcoal and 618 px on Newsprint (2x), the 558 px column's frame, 296 px on Newsprint and 256 px on Charcoal; S12's phone at 326 px today and with the 2 px gap on both grounds; S78 at 326 px on Charcoal; S07 at 326 px on Newsprint; S16 at 326 px today and with the column (3x, Newsprint), on Charcoal (2x) and in grayscale, and at 296 px on Charcoal.

## Not tested

- The quick guide check (`guide_check.js`): I touched no sketch, and the brief asks it of sketches; not run.
- S12, S16 and S78 at a 1440 px kit page by eye after the changes (their desk drawings at 1024 px; the guide draws S12 at 723 px at a 1,440 px window, which I looked at).
- Forced colors, print, 200 percent text and screen readers beyond the kit's emulated checks; real phones.
- My photographs of S12 inside the guide page: the sticky header crossed the figure and the dark theme did not switch, so I did not use them; the page's measurements stand.

## Files

Modified: `work/build/chart-kit/specs/s12.json` (`stage_min`, the alt's clause, two `notes_internal` lines), `s16.json` (`labels.column_phone`, one `notes_internal` line), `s78.json` (one `notes_internal` line); `work/build/guide/entries/14-116.json` (builders line).
Created: `work/build/scripts/phase-3/cartographer_round4_derive.py` (checks only; writes nothing); this notes file.
Kit changes I asked for and others landed: `forms/bubble-map.js` (C4-E2, the component engineer, from my patch), the tokens' `tile.phoneGap` (C4-E1, the engineer).
Scratch only: `before/`, `after/`, `after2/`, `draft/`, `exp/`, `requests/`, `board3/`, `tools/`, `strict/`, `strict2/` and the mirrors `mirror/` to `mirror4/` and `repo-mirror/`.
