# Handoff for the next session: the atlas and systems map visual system

Written October 29, 2026, at the close of the Civic Line icon work. A new session reads `CLAUDE.md` and its start-of-session list first. This note says where things stand and what comes next.

## Where things stand

- **Phase.** Phase 2 is active. Gate 1 was approved on October 28 (G1-01 to G1-11). Gate 2 has not been held.
- **Icons: done and approved.**
  - **The set:** Civic Line, 122 icons, is the icon family (DR-01, DR-07). Its Explain, Track, Connect and Act are the pillar marks (DR-04).
  - **Variants:** four editions, twelve tiles per icon, framing option 3 (DR-08 to DR-10, D2-40 to D2-46).
  - **Records:** `work/ledger/20261029_Civic-Line-Icons-Report.md`. Catalog: https://claude.ai/artifact/XWvZnx86mnKkoVFV9PCcgD.
  - **Package:** `deliverables/20261029_Oath-And-Action-Civic-Line-Icons-SVG.zip` and `-PNG.zip`.
  - **Rebuild:** `python3 -I work/build/scripts/civic-line/export_all.py` rebuilds everything.
- **Overprint and Moving part** are closed (DR-01). Their files stay in `work/boards/phase-2/icons-r2/` for the record.

## What comes next, in Dustin's order (DR-06, DR-11)

1. **The visual system for the atlas and systems maps.**
   - Start from the direction review of October 28: `work/ledger/20261028_Direction-Review-Report.md`, Choice 1 and Choice 3, and its page https://claude.ai/artifact/1nNZZqQDESFYWRcbSnyR8B.
   - The studio's pick is Loop Lines (the transit-map poster on Prussian) joined to the Field Guide (one card per loop, after the R8 card), linked by the locator inset. The recommended sign mark is the pointing tag.
   - None of these is decided yet. Dustin asked for something "very visual, intuitive and beautiful", with the current system as the fallback (G1-11). The scope is a spec and working specimens, not a redesign of the working atlas (G1-08).
   - Sources:
     - the atlas data: `work/extract/atlas-v7-data.json`;
     - the map boards: `work/boards/20261028_Map-Direction-*.html` and `work/boards/phase-2/maps-r2/`;
     - the pipeline: `maps_model.py` and `verify_maps_data.py` in `work/build/scripts/phase-2/`;
     - the creative director's reviews: `work/handoffs/phase-2/20261028_CD-Review-Of-Map-Round-Two.md`.
   - The Civic Line icons now exist and can serve the atlas where an icon belongs on a map or card.
2. **The other open items of the direction review:**
   - P3: the Rule 05.3 sentence on the current icon in a menu;
   - R1 to R14, as a set. Several of them were written for Overprint, so restate the ones that still apply to Civic Line (R10 to R14 in particular);
   - Q-13: the reader check.
3. **The rest of Phase 2 through Gate 2:** identity, color, type, tokens and the component chapters. The identity masters in `work/build/assets/identity/` are waiting for Gate 2.

## Open questions

- Q-11 to Q-14 from Gate 1.
- Q-16: the tool that made the Civic Line sheets.

All are in `work/ledger/20261020_Open-Questions.md`.

## Standing rules worth repeating

- Dustin reviews each stage before changes. Post a short plan with questions, then wait for his go.
- End every reply with a change log.
- Writing rules: plain spoken prose, no em dashes, none of the patterns `CLAUDE.md` lists.
- Never touch `source/` or anything Dustin did not name.
- Commit to `claude/friendly-brahmagupta-tonmfa` and push. The commit attribution lines are in the session's instructions.
