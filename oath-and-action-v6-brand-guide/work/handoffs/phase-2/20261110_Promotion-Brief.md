# Brief: promote the approved drawings into the package

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the main session for the Civic Line hand, the utility hand, the identity designer and the engineer. Dustin approved every card on the drawings board by name (DR-156 to DR-182) and the promotion plan (DR-184 to DR-186, D2-714 to D2-718), all in `work/ledger/20261020_Decision-Log.md`.

## The goal

Each approved drawing becomes a final in one folder per family, so the guide draws it from the engineer's sprite and the later asset package (Master Brief section 20) copies it without asking which file is the right one. The originals and every unpicked option stay where they are, as the record (DR-135, D2-464, D2-718). Nothing here changes a drawing: a final is the approved option's drawing, byte for byte in its paths, with a final's ids, title, description and file name.

## The approved picks

| Card | Final | Approved option file (source) |
|---|---|---|
| CL-025 Congress | Set B | `work/build/assets/civic-line-redraws/svg/20261109_CL-025-Congress-Option-B-*.svg` (DR-156) |
| CL-014 Entrenched Power | Option C | `.../civic-line-redraws/svg/20261109_CL-014-Entrenched-Power-Option-C-*.svg` (DR-156) |
| R-13 Congressional Capacity | Set B | `.../civic-line-redraws/svg/20261109_R-13-Congressional-Capacity-Option-B-*.svg` (DR-156) |
| R-42 Congressional Tariff Votes | Set B | `.../civic-line-redraws/svg/20261109_R-42-Congressional-Tariff-Votes-Option-B-*.svg` (DR-156) |
| CL-059 Credit Allocation | Option B | `.../civic-line-redraws/svg/20261109_CL-059-Credit-Allocation-Option-B-*.svg` (DR-157) |
| R-48 Agency Independence | Option C | `.../civic-line-redraws/svg/20261109_R-48-Agency-Independence-Option-C-*.svg` (DR-158) |
| CL-073 Testify (new, D2-714) | Option A | `work/build/assets/civic-line-new-topics/svg/20261109_Testify-Option-A-*.svg` (DR-159) |
| CL-074 Contact an Official (new, D2-714) | Option A | `.../civic-line-new-topics/svg/20261109_Contact-An-Official-Option-A-*.svg` (DR-160) |
| Pillar icons | 24 px fit B and the 16 px fit (fit A, the only one) on 1x screens; the masters at 24 px on 2x screens | `work/build/assets/pillar-pixel-fit/svg/20261109_CL-0xx-*-24px-Fit-B-*.svg` and `-16px-Fit-A-*.svg` (DR-179) |
| Utility family | Every action bare; Error, Success and Warning in their own shapes | DR-161 |
| Utility icons | A for each, except Reset B and Success B: Close, Menu, Arrow, Chevron, Download, Another Site, Search, Filter, Copy, Play, Pause, Reset (B), Error, Success (B), Selected Check, View Full Size, Sort, Warning | `work/build/assets/utility-icons/svg-24/` and `svg-16/` (DR-162 to DR-178) |
| End mark | Fit B at 14 px for 17 px text and at 12 px for 15 px text | `work/build/assets/identity/ampersand/20261109_Amp-B-1{4,2}px-End-Mark-Fit-B.svg`, with their Prussian White files (DR-180) |
| Lockmark masters | The rebuilt 24 and 48 px files replace today's in use; the 16 px master stays | `work/build/assets/identity/lockmark/20261109_Lockmark-{24,48}px-Master-Outline.svg`, with their Prussian White files (DR-181) |
| L6 | Wordmark and tagline centered on the strip, 9.3 px down at 884 px | `work/boards/phase-2/stage-b/drawings/identity/` and the identity notes, section 3 (DR-182) |

## Folder and naming conventions (every owner follows these)

- **Civic Line set in use:** `work/build/assets/civic-line-v6/` with `black/`, `red-black/`, `newsprint/`, `red-newsprint/` (124 SVGs each), `png-256/` and `png-512/` and `tiles/` in the October layout for the eight changed drawings only, and `20261110_Civic-Line-V6-Inventory.csv` and `.json` (124 rows) (D2-716). An unchanged drawing keeps its October file name and bytes. A changed or new drawing is `20261110_Oath-And-Action-Civic-Line-<ID>-<Slug>-<Edition>.svg`, with the October slug for the six redraws and `Testify` and `Contact-An-Official` for the two new ones. Every SVG keeps `data-id="<ID>"` on its root, which the sprite reads.
- **Pillar icons in use under 48 px:** `work/build/assets/pillar-icons/`, files `20261110_Pillar-Icon-<ID>-<Word>-<24px|16px>-<Black|Red-Black>.svg` with PNG previews at 1x and 2x, root attributes `data-id="<ID>"` and `data-size="24"` or `"16"`, and `20261110_Pillar-Icons-Manifest.json`. The black edition is the one in use under 48 px (D2-497); the red-black edition is kept for the record of DR-133's red placements.
- **Utility icons:** `work/build/assets/utility/` with `svg-24/`, `svg-16/` and `png/`, files `20261110_Utility-<Name>-<24px|16px>.svg` (Name in the existing title case: `Another-Site`, `Selected-Check`, `View-Full-Size`), root attributes `data-icon="U-<name>"`, `data-icon-family="utility"`, `data-size`, no `data-option`, and `20261110_Utility-Icons-Manifest.json` listing each icon's ID, word, uses, turns and mirrors (D2-652, D2-653, D2-556), sizes and approving DR.
- **Sprite symbol ids (engineer):** Civic Line `oa-sym-<id lowercased>` (as today, `oa-sym-cl-025`); pillar fits `oa-sym-<id>-<size>px` (`oa-sym-cl-019-24px`); utility `oa-sym-u-<name>-<size>px` (`oa-sym-u-close-24px`).
- **Identity:** finals that already sit beside the masters keep their names and bytes. A master that embeds a changed drawing (for example an L3 or L6 file that carries the lockmark's paths) gets a new dated file beside it; the old file stays as the record.

## Who does what

1. **Civic Line hand** (`.claude/agents/oa-design-director.md`): the `civic-line-v6/` set, all four editions, previews, tiles and the inventory in use; the pillar icons folder. Newsprint and Red-Newsprint editions of the eight follow the October rule for light editions (DR-09). Tiles follow the October tile pipeline and calibration (DR-10), with the tile minimum sizes measured as for the other 122. Fill each new inventory row's fields as the October rows are filled, with a column saying whether the row is "October master, unchanged" or the DR that approved its final.
2. **Utility hand** (`.claude/agents/oa-design-director.md`): the `utility/` folder and its manifest.
3. **Identity designer** (`.claude/agents/oa-design-director.md`): wire the end mark fits, the rebuilt lockmark masters and L6 centered into every place the guide draws them (chapters 03 and 08, the identity proofs, any L3, L6 or social card specimen), the minimum sizes record (`work/build/assets/identity/20261028_Identity-Minimum-Sizes.json`) and the specimen manifest's notes. Confirm by render that the rebuilt lockmarks draw the same pixels at their own sizes (DR-145).
4. **Engineer** (`.claude/agents/oa-engineer.md`): `guide_build.py`'s sprite reads the three family folders with the symbol ids above, and its self-test covers each family; the masthead's menu glyph becomes Utility Menu A (`U-menu`) from the sprite; then the strict build, `guide_check.js` at 1440, 1024, 390 and 360 px and the token tests once the makers' folders exist. If they do not exist yet when your code is ready, write your notes as far as you can and reply; the main session will resume you when they land.

## Checks every maker runs on its finals

- Byte checks: an unchanged copy hashes the same as its October file; a final's drawing (every `d`, shape and its attributes) matches its approved option file's, with only ids, title, description and file name changed. Write the hashes and the comparison to your notes.
- The engineer's pixel-fit check (`work/build/scripts/phase-2/icon_pixel_fit_check.py`) on every final meant for 16 or 24 px, with `--weight 2` at 24 px and `--weight 1.5` at 16 px for utility icons.
- The engineer's look-alike check (`work/build/scripts/phase-2/icon_likeness_check.js`) on the eight changed Civic Line drawings and the 18 utility icons against the set in use. Report any figure that differs from the drawings board's.
- A look at every final at true size and enlarged, at 1x and 2x.

## Notes and limits

Each owner writes `work/handoffs/phase-2/20261110_Promotion-<Role>-Notes.md` (`Civic-Line`, `Utility`, `Identity`, `Engineer`) with: what it promoted, a table of every final with its source file, the checks' figures, routine calls as "D2-xxx | decision | reason" lines, questions for Dustin with a recommendation, Tested and Not tested kept apart, and a change log of files created and modified with their locations.

Never touch `source/`, `work/ledger/`, `deliverables/`, the October Civic Line folder `work/build/assets/civic-line/`, the makers' option folders, the identity masters (new files beside them only), any board, the first reader check, or another owner's files. Do not commit or push. Write the large scratch outputs (renders, captures) to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/promotion/<role>/`, never into `work/build`. Write your notes early and add to them as you go. Reply to the main session in 200 words or fewer.

The writing rules in `CLAUDE.md` bind every word you write, including notes, titles and descriptions: plain spoken prose, no em dashes.
