# Stage B round 2: systems designer's notes

Oath & Action Edition 06, Phase 2, stage B round 2, November 10, 2026. Written under `20261110_Stage-B-Round-2-Brief.md`. Two agents share this file under the same role file (D2-720): one for chapter 10 and then chapter 12's systems devices, one for chapter 11. Each keeps to its own section.

## Chapter 10

Written by the chapter 10 maker (`oa-design-director`, checked against `oa-ux-accessibility-lead`). This section grows as the work lands.

### Status

- **03:44 UTC: the construction file is done.** `work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md` holds the 128-unit box, the line, caps and joins, the red accent, the capped fit, the four editions and six tiles, the size floors and the list of 41 by ID with how it was decided. Chapters 09 and 11 can start from it. Its section 0 fixes chapter 10's rule numbers (10.1 to 10.10) so other chapters can cite them now.
- Next: the chapter's copy, layout and the contact sheet plan; specimens that draw symbols wait for `civic-line-v6/black/` to hold 124 files and for the engineer's promotion notes.

### What I built

(added as it lands)

### Routine calls

- D2-xxx | The list of 41 for 24 px is the trace review's section 6 list, unchanged, and none of the six redraws, CL-073 or CL-074 joins it | DR-136 approved "the 41"; the eight new finals were shown at 24 px as reference only (D2-673), so adding one is Dustin's call
- D2-xxx | Of the 41, the four pillar icons draw from chapter 09's fits at 24 px, so 37 topic and atlas drawings may be set at 24 px, and a kicker's icon comes from those 37 | DR-179 and DR-112 keep the pillar icons to their own fits and out of kickers
- D2-xxx | Chapter 10's rule numbers are fixed in the construction file before the chapter is written | Chapters 09 and 11 cite them in parallel, and the shell links "Rule 10.n" only when the numbers hold
- D2-xxx | On Prussian a Civic Line drawing is one color in the ink token, with no accent token named | DR-09 sets the Newsprint edition alone on Prussian; the accent token's "White on Prussian" belongs to the identity marks

### Questions for Dustin

(none yet)

### Requests to other owners

- **Identity designer and editor, `s-01-21-correct`.** Rule 01.21's kicker sets CL-055 Productivity at 24 px; CL-055 is not among the 41, so guide check B-3 fails it once the list is on. Recommendation: one of the 37 whose word fits an analysis kicker, such as CL-057 Labor Share or CL-060 Taxes & Benefits, with the kicker's word changed to match.
- **Engineer, tokens.** `oa.component.icon.accent.*`: `minSize` to `{oa.size.icon.large}` and the description to "at 48 px and up", since every Civic Line drawing is one color under 48 px (round 2 brief, D2-373, D2-497). The "White on Prussian" line does not hold for Civic Line drawings (DR-09).
- **Engineer, B-3.** The list of 41 is in the construction file, section 10.

### Tested

- The 41 compared by script with the trace review's section 6: identical, 41 IDs, no repeat.
- The 41 rendered at 24 px on Newsprint at 1x and 2x in Chromium, from the October Black files, and looked at.
- Construction figures read by script from the 122 October red-black files and the eight approved option files.
- Cap counts (92 at the cap, 32 filling to 116 units) computed from the October inventory and the eight finals' line widths.
- Contrast figures from the hex values with the WCAG 2.x formula.

### Not tested

- Anything in `civic-line-v6/`, which did not exist when this section was first written.

### Change log

Created:
- `work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md`
- `work/handoffs/phase-2/20261110_Stage-B-Round-2-Systems-Notes.md` (this file; the chapter 11 maker adds its own section)

Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/round-2/ch10/` (24 px renders of the 41).
