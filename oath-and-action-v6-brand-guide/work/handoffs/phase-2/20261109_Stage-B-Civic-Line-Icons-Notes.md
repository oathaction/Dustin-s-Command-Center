# Stage B, round 1: Civic Line icon designer's notes

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the icon designer for the Civic Line hand (D2-498), in the design director role, run as a subagent of the main session. This file was written early and grew as the work landed.

I read, in order: `.claude/agents/oa-design-director.md`, `CLAUDE.md`, the Master Brief sections 3, 6 and 9 to 12, `20261109_Stage-B-Drawings-Brief.md`, the final stage B brief, the decision log from "Stage B answers" to the end (DR-139 to DR-155 and D2-491 to D2-594 as they stood), section 1 of `20261109_Stage-B-Research-Notes.md`, sections 1.1, 1.4 and 1.5 of `20261109_Stage-B-Accessibility-Audit.md`, the engineer's notes on the two checks, the Civic Line report, the six source drawings and their logs, the four pillar sources, and Rules 01.1, 01.6 and 01.7 as chapter 01 states them.

**Open the plate page:** `work/boards/phase-2/stage-b/drawings/civic-line/20261109_Civic-Line-Drawings-Plates.html`. It shows every option at true size on Newsprint beside its original (or, for the new topics, the two topic drawings it must not be read as), R-46 and R-03 beside the Congress options (DR-152), and the pillar fits beside their masters at 96, 48, 24 and 16 px.

## Where the work stands

Done: 24 options (18 redraws, 6 new topic drawings), 12 pillar fits, both checks, the naming test and the plate page. Ready for the creative director's scores (D2-567).

## What I drew

**The four dome drawings, as three matched sets (D2-503).** Each set draws one Congress sign and reuses it in CL-025, R-13 and R-42; CL-014 takes the same sign without its Congress-only feature.

- **Set A, the building without its dome (within DR-135).** Every kept part keeps its master's own coordinates. The dome, cupola and finial become a flat attic; the columns become walls, windows and, in CL-025, a center door that takes the red from the column. The Congress-only feature is CL-025's two wings, one for each chamber; CL-014 has none, as its original has none. R-13 A and R-42 A keep the book and the ballot box, as DR-135 requires, and so keep their misreadings.
- **Set B, the House chamber from the gallery (DR-146).** Three rows of members' desks curve around the rostrum, each row in five sections with aisles lined up toward the rostrum, and the red sits on the two-tier rostrum. Seen from the gallery the rows bow toward the reader, which keeps the drawing apart from R-03 and R-46, both half rings seen from above. The Congress-only feature is the rostrum's upper tier, where the Speaker sits; CL-014 B's chamber has one tier.
- **Set C, the two chambers.** A House chamber in front and a smaller Senate chamber set behind it, both from the gallery, red on both rostrums: one job, the place each chamber is led from. This is the meaning sheet's second idea. The Congress-only feature is the second chamber; CL-014 C has one. Two chambers also describe 49 of the 50 state legislatures, so the sign separates Congress from a city council or a one-chamber body and leaves "Congress" to the label.
- In R-13 and R-42, sets B and C put the sign on a top tier at three quarters of CL-025's size, with the other parts below. R-13 B and C swap the open book (CL-019 Explain's sign) for an analyst's report whose chart line is red. R-42 B and C swap the ballot box (a public election) for a red card holding a yes and a no, and draw the imports with CL-064's own parcel and a tag.

**CL-059 Credit Allocation.** A keeps the pediment and turns the four columns into one wall holding a round vault door. B drops the pediment: a flat-roofed bank with a large vault door, hub and spokes. C makes the bank its safe, a strongbox on feet with a dial and a handle, and lets the red branches carry the money out, as the meaning sheet asks of a vault drawn alone. The home, factory and red branches stay in all three.

**R-48 Agency Independence.** A keeps the pediment, band, base, brace and official and turns the column bays into a wall with a door and two windows. B replaces the building with a commission of three at one table, the meaning sheet's column-free sign for a multi-member agency. C keeps the commission and moves the official from the lectern to a desk, with an arrow from the desk that stops at the red brace.

**Testify (DR-141, DR-147).** A is DR-147's drawing: a raised, curved dais with three officials above, and the witness below at a table with a red microphone. B sets the same parts on a diagonal, the witness at lower left looking up to the dais at upper right. C leaves the witness out: the dais and the red microphone, so the reader is the witness. There is no gavel, scales, robe, flag or nameplate letter, and there are three officials, as the meaning sheet asks.

**Contact an official (DR-141, DR-147, DR-155).** A is DR-147's drawing: a person and an official at a desk, joined by one line carrying a red speech mark. B is Dustin's very simple phone, a desk telephone whose red cord runs to an official at a desk; the desk and the official are DR-155's part that names the official. C is the visit: the person stands at the official's desk and one red speech mark rises between them. The official wears no tie (CL-026), and the two never sit level across a table (CL-016).

**The pixel-fit pillar icons (DR-133, D2-496, D2-497).** CL-019 Explain, CL-020 Track, CL-021 Connect and CL-022 Act at 24 px in two fits, A with a 2 px line and B with a 1 px line, and at 16 px in one fit with a 1 px line. Every fit is drawn pixel by pixel, each pixel Charcoal, Pillar Red or empty, keeping every feature and every red placement of its master, with the red as its own shape. The black edition is the one in use under 48 px.

## Every option

Files: each stem below has `src/<stem>.svg` (the source drawing), `svg/<stem>-Red-Black.svg` and `svg/<stem>-Black.svg`, and `png/<stem>-Red-Black.png`, `-Red-Black-2x.png`, `-Black.png` and `-Black-2x.png` (128 and 256 px, clear ground). Redraws are in `work/build/assets/civic-line-redraws/`, new topics in `work/build/assets/civic-line-new-topics/`. Each folder has a manifest with every option's bake figures (`20261109_Stage-B-Drawings-Manifest.json`).

The naming test reads each option at 48 px with no label. The reader is me, an agent standing in for a first-time reader; the creative director repeats it. Verdicts: "names the subject", "names it nearly" (the label settles it), "recognized with the label", and "misleads without the label" (kept by DR-135). Look-alike: the closest drawing on the engineer's check at 24 px; the flag line is 0.913 (99th percentile of master pairs) and the watch line 0.871. "Own" is the option against its original.

| Card | Opt | DR-135 | What it shows | Stem | Naming test at 48 px | Closest drawing | Own |
|---|---|---|---|---|---|---|---|
| CL-025 | A | Within | Dome, cupola and finial become a flat attic; the columns become walls, windows and a center door, which takes the red | `20261109_CL-025-Congress-Option-A` | A large public building, most likely a city hall or a museum. Recognized with the label | CL-005 Public Meeting, 0.920; 3 flagged pairs | 0.864 |
| CL-025 | B | Outside | The House chamber from the gallery: three rows of seats curving around the rostrum, red on the rostrum | `20261109_CL-025-Congress-Option-B` | A chamber or an auditorium with a stage; a reader who knows the House may say Congress. Recognized with the label | R-31 Childcare Supply, 0.910; 1 flagged pair (with CL-014 A, a new drawing) | 0.757 |
| CL-025 | C | Outside | The two chambers, the House in front and the smaller Senate behind, red on both rostrums | `20261109_CL-025-Congress-Option-C` | Two seating chambers, one larger; with the label, the House and the Senate. Recognized with the label | R-28 Capital-Income Tax, 0.773 | 0.506 |
| CL-014 | A | Within | Spire, cupola and dome become set A's flat attic; the six columns become two walls. Fence and red door kept | `20261109_CL-014-Entrenched-Power-Option-A` | A government building fenced in. Names it nearly | R-31 Childcare Supply, 0.933; 8 flagged pairs | 0.959 |
| CL-014 | B | Outside | Set B's chamber, one-tier rostrum, inside the fence; the red moves from the door to the rostrum | `20261109_CL-014-Entrenched-Power-Option-B` | A chamber or an arena behind a fence. Recognized with the label | R-46 Expand the House, 0.950; 4 flagged pairs | 0.896 |
| CL-014 | C | Outside | One chamber of set C inside the fence; the red moves from the door to the rostrum | `20261109_CL-014-Entrenched-Power-Option-C` | A chamber or an arena behind a fence. Recognized with the label | R-20 Merger Enforcement, 0.940; 3 flagged pairs | 0.907 |
| R-13 | A | Within | Dome arcs and finial go, leaving the drum as a flat attic; drum columns go, lower columns become two windows and a door | `20261109_R-13-Congressional-Capacity-Option-A` | Two people, a building and an open book; the book pulls toward reading or a library. Misleads without the label | CL-035 Residential Sorting, 0.917; 1 flagged pair | 0.966 |
| R-13 | B | Outside | Set B's chamber above two staff and an analyst's report whose chart line is red | `20261109_R-13-Congressional-Capacity-Option-B` | A chamber with two staff and a report: staff working for a legislature. Recognized with the label | CL-047 Data Rights, 0.858 | 0.620 |
| R-13 | C | Outside | Set C's two chambers above two staff and the report | `20261109_R-13-Congressional-Capacity-Option-C` | Two chambers with two staff and a report. Recognized with the label | CL-038 External Shocks, 0.786 | 0.636 |
| R-42 | A | Within | Finial, lantern and dome go, leaving the drum as a flat attic; columns become a band and windows. Ballot box, chart and red kept | `20261109_R-42-Congressional-Tariff-Votes-Option-A` | A building, a ballot box and a crate with an arrow; the ballot box reads as a public election. Misleads without the label | R-06 On-Cycle Elections, 0.929; 1 flagged pair | 0.983 |
| R-42 | B | Outside | Set B's chamber, a red yes-and-no vote card, CL-064's parcel with a tag | `20261109_R-42-Congressional-Tariff-Votes-Option-B` | A chamber, a yes-and-no card and a parcel with a tag: a vote on goods. Recognized with the label | CL-047 Data Rights, 0.908 | 0.488 |
| R-42 | C | Outside | Set C's two chambers, the red vote card, the parcel with a tag | `20261109_R-42-Congressional-Tariff-Votes-Option-C` | Two chambers, a yes-and-no card and a parcel with a tag: a vote on goods. Recognized with the label | CL-012 Election Rules, 0.810 | 0.500 |
| CL-059 | A | Within | The four columns become one wall holding a round vault door; pediment, base, home, factory and red branches kept | `20261109_CL-059-Credit-Allocation-Option-A` | A bank, or a temple, sending money to a home and a factory. Names the subject | CL-040 Platform Power, 0.769 | 0.992 |
| CL-059 | B | Outside | The pediment goes too: a flat-roofed bank with a large vault door, hub and spokes | `20261109_CL-059-Credit-Allocation-Option-B` | A bank vault sending money to a home and a factory. Names the subject | CL-022 Act, 0.762 | 0.975 |
| CL-059 | C | Outside | The bank becomes its safe, a strongbox on feet with a dial and handle; the red branches carry the money out | `20261109_CL-059-Credit-Allocation-Option-C` | A safe paying out to a home and a factory. Names the subject | CL-040 Platform Power, 0.714 | 0.981 |
| R-48 | A | Within | The column bays become one wall with a door and two windows; pediment, band, base, brace and official kept | `20261109_R-48-Agency-Independence-Option-A` | A house or a school and a speaker at a lectern, set apart by a bracket. Recognized with the label | R-41 Grid Cost Allocation, 0.897 | 0.997 |
| R-48 | B | Outside | A commission of three at one table replaces the building; brace and lectern official kept | `20261109_R-48-Agency-Independence-Option-B` | A panel of three and a speaker at a lectern, set apart; some may say a debate. Recognized with the label | CL-035 Residential Sorting, 0.918; 1 flagged pair | 0.848 |
| R-48 | C | Outside | The commission, and the official at a desk whose arrow stops at the red brace | `20261109_R-48-Agency-Independence-Option-C` | A panel of three kept apart from a person at a desk, whose arrow stops at the bracket. Names it nearly | CL-035 Residential Sorting, 0.885 | 0.844 |
| Testify | A | | A raised, curved dais with three officials above the witness at a table with a red microphone | `20261109_Testify-Option-A` | A hearing: a person at a microphone facing a panel. Names the subject | CL-042 AI Concentration, 0.612 | |
| Testify | B | | The witness and red microphone at lower left, facing the raised, curved dais at upper right | `20261109_Testify-Option-B` | A person at a microphone speaking up to a raised panel. Names the subject | CL-062 Assets & Debt, 0.700 | |
| Testify | C | | The raised, curved dais with three officials and the red microphone on the witness table | `20261109_Testify-Option-C` | A panel and a microphone: a hearing, or a panel discussion. Names it nearly | CL-042 AI Concentration, 0.717 | |
| Contact an official | A | | A person and an official at a desk, joined by one line carrying a red speech mark | `20261109_Contact-An-Official-Option-A` | A person sending a message to someone at a desk. Names the subject | R-36 Public Investment, 0.896 | |
| Contact an official | B | | A very simple phone whose red cord runs to an official at a desk | `20261109_Contact-An-Official-Option-B` | A phone line to someone at a desk: calling an office. Names the subject | R-06 On-Cycle Elections, 0.872 | |
| Contact an official | C | | The person at the official's desk, one red speech mark between them | `20261109_Contact-An-Official-Option-C` | A person talking to someone at a desk: a visit, or a help desk. Names it nearly | CL-069 Childcare, 0.864 | |

Every option's line runs 2.75 to 3.35 units of 128, inside DR-08's range of 2.68 to 3.35. Every set B and set C composite reaches the cap weight, 3.35.

**The pillar fits.** Files in `work/build/assets/pillar-pixel-fit/`: `svg/<stem>-Red-Black.svg` and `-Black.svg`, `png/<stem>-Red-Black.png`, `-Red-Black-2x.png`, `-Black.png` and `-Black-2x.png`, and `20261109_Pillar-Pixel-Fit-Manifest.json` with each fit's pixel map and pixel counts. Check figures are for the black edition at 1x; every fit also passes at 2x and in its red-black edition.

| Pillar | Fit | Line | Stem | Pixel-fit check | Own master | Closest drawing |
|---|---|---|---|---|---|---|
| CL-019 Explain | 24 px, A | 2 px | `20261109_CL-019-Explain-24px-Fit-A` | Pass: 31 of 31 straight edges on pixel edges, 0% soft, smallest gap 1 px, 4 of 4 counters kept | 0.682 | CL-068 Education, 0.729 |
| CL-019 Explain | 24 px, B | 1 px | `20261109_CL-019-Explain-24px-Fit-B` | Pass: 24 of 24, 0% soft, gap 2 px, 4 of 4 counters | 0.722 | CL-068 Education, 0.766 |
| CL-019 Explain | 16 px, A | 1 px | `20261109_CL-019-Explain-16px-Fit-A` | Pass: 18 of 18, 0% soft, gap 1 px, 4 of 4 counters | 0.669 | CL-068 Education, 0.749 |
| CL-020 Track | 24 px, A | 2 px | `20261109_CL-020-Track-24px-Fit-A` | Pass: 18 of 18, 0% soft, gap 1 px, 2 of 2 counters | 0.596 | R-13 Congressional Capacity, 0.561 |
| CL-020 Track | 24 px, B | 1 px | `20261109_CL-020-Track-24px-Fit-B` | Pass: 15 of 15, 0% soft, gap 2.25 px, 3 of 3 counters | 0.720 | CL-051 Market Power, 0.736 |
| CL-020 Track | 16 px, A | 1 px | `20261109_CL-020-Track-16px-Fit-A` | Pass: 12 of 12, 0% soft, gap 1 px, 2 of 2 counters | 0.665 | CL-051 Market Power, 0.647 |
| CL-021 Connect | 24 px, A | 2 px | `20261109_CL-021-Connect-24px-Fit-A` | Pass: 20 of 20, 0% soft, one connected part, 3 of 3 counters | 0.941 | CL-009 Safe Seats, 0.711 |
| CL-021 Connect | 24 px, B | 1 px | `20261109_CL-021-Connect-24px-Fit-B` | Pass: 20 of 20, 0% soft, one connected part, 3 of 3 counters | 0.993 | CL-019 Explain, 0.776 |
| CL-021 Connect | 16 px, A | 1 px | `20261109_CL-021-Connect-16px-Fit-A` | Pass: 8 of 8, 0% soft, one connected part, 3 of 3 counters | 0.907 | CL-009 Safe Seats, 0.833 |
| CL-022 Act | 24 px, A | 2 px | `20261109_CL-022-Act-24px-Fit-A` | Pass: 29 of 29, 0% soft, gap 1 px, no counters | 0.506 | CL-023 Evidence, 0.491 |
| CL-022 Act | 24 px, B | 1 px | `20261109_CL-022-Act-24px-Fit-B` | Pass: 19 of 19, 0% soft, gap 1 px, no counters | 0.502 | CL-023 Evidence, 0.605 |
| CL-022 Act | 16 px, A | 1 px | `20261109_CL-022-Act-16px-Fit-A` | Pass: 16 of 16, 0% soft, gap 1 px, no counters | 0.311 | R-02 Ranked-Choice Voting, 0.456 |

Act's low figures against its master come from two things. The master at 24 and 16 px draws a line under one pixel, a faint grey, and I widened the hand by about a quarter so each knuckle, the thumb and the ring keep a clear pixel. Explain's closest drawing is CL-068 Education, which shares the open book; that pair exists among the masters too.

## The checks' figures

**Look-alike check** (`node work/build/scripts/phase-2/icon_likeness_check.js <folder> --json <file>`), results kept in `work/boards/phase-2/stage-b/drawings/civic-line/checks/`:

- **Redraws:** 18 drawings; exit 1, with 20 flagged pairs and 125 to watch. Fifteen of the flags involve CL-014's three options, two of them against new CL-025 options of other sets. The other five are CL-025 A against CL-005 Public Meeting (0.920) and against CL-014's original (0.918), R-42 A against R-06 On-Cycle Elections (0.929), and R-13 A and R-48 B against CL-035 Residential Sorting (0.917 and 0.918).
- **A baseline**, to read those flags: I ran the six originals through the same check under names without their IDs. The originals already sit near or above the flag line with the same neighbors: CL-014 against R-46 at 0.919 and against CL-025 at 0.922; CL-025 against R-43 Disaster Mitigation at 0.935; R-42 against R-06 at 0.899. CL-014's fence blurs to a wide oval at 24 px, and many drawings blur to the same oval.
- **Which flags matter.** Only CL-014 B against R-46 pairs two chambers (0.950, where the original scores 0.919), so a reader could take "entrenched power" for "expand the House". Every other flagged pair joins drawings of different things, such as a fenced chamber and buildings under a magnifier, or a building and two calendars. CL-025 A against CL-031 Local Government, the clash I watched for in a domeless building with a red door, comes in under the watch line.
- **New topics:** 6 drawings; exit 0, nothing flagged, 5 to watch (the closest, Contact A against R-36 Public Investment, 0.896).
- **Pillar fits:** 12 fits; exit 0, nothing flagged or watched.
- **Across Civic Line and the utility set:** my 36 drawings beside the utility designer's 54 options at 24 px, in one scratch folder. The only pair across the two families above the watch line is Contact A against Utility Arrow C, 0.875; nothing flagged. The phone meets no utility glyph, since the set has none (D2-512).

**Pixel-fit check** (`node work/build/scripts/phase-2/icon_pixel_fit_check.js --size <16|24> --weight <line> --png <scratch> <files>`): 24 of 24 pass, every fit in both editions at its own size and line, at 1x and 2x, with no soft pixel. The redraws and new topics are 48 px drawings (DR-136), and none of the six originals is among the 41 that read at 24 px, so the check does not apply to them.

**My own file checks:** all 72 SVGs parse; each black file is its red-black file with Pillar Red swapped for Charcoal and nothing else changed; no black file holds red; no id repeats in a file; the redraws and new topics sit in a 0 0 128 128 box and draw nothing outside it.

## Routine calls

The main session numbers these when it records them; the numbers below follow the last in the log (D2-594) and are provisional.

- D2-595 | New drawings are authored in Civic Line's source space with the set's 5.5 px line and baked by the family's own parser, emitter and DR-08 capped fit | One hand: the same line, caps, joins, colors and file layout as the 122 masters
- D2-596 | Kept parts of every "Within DR-135" option keep their master's source coordinates | Each kept part can be checked against its original
- D2-597 | In set A, a dome becomes a flat attic and columns become walls, windows or a door | Taking them out alone left free-standing strokes that still read as columns
- D2-598 | Each set's Congress-only feature: set A the two wings, set B the rostrum's upper tier, set C the second chamber; CL-014 drops it | D2-503
- D2-599 | Seat rows split into an odd number of sections, never with a center aisle | A center aisle splits a chamber into two sides, which reads as party (Rule 01.1)
- D2-600 | Set C staggers its two chambers, the Senate behind the House | Side by side the pair ran four times wider than tall and shrank past naming at 48 px
- D2-601 | In R-13 and R-42, sets B and C put the Congress sign on a top tier at three quarters of CL-025's size | In the originals' strip layout its rows closed up; the tier layout also brings the composites to the cap line weight
- D2-602 | R-13 B and C trade the open book for an analyst's report with a red chart line | The book is CL-019 Explain's sign (meaning sheet)
- D2-603 | R-42 B and C trade the ballot box for a red yes-and-no card and draw imports with CL-064's parcel and a tag | A ballot box means a public election, and the set keeps one sign for imports
- D2-604 | CL-059's vault wheel has four diagonal spokes on a hub ring | Spokes in a plus read as a first-aid cross, and three spokes as a fan
- D2-605 | CL-059 A and R-48 A keep the pediment | DR-135 names only the columns in these two; the meaning sheet's caution on pediments goes to Dustin as question 7
- D2-606 | R-48 C drops the brace's dot, and the arrow stops where the dot was | The arrow would otherwise touch it; the bracket and its nub carry the separation
- D2-607 | Testify and Contact an official carry no ID in their file names or files | Neither has one yet, and a made-up code would read as an ID
- D2-608 | The microphone is the common upright microphone: capsule, holder, stem and base | A ball on a stem read as a lollipop
- D2-609 | The phone's red is its cord | Rays over the phone read as an alarm bell, and a red handset is the sign for hanging up
- D2-610 | Contact C draws the visit with the person in it | A speech mark alone over the official read as the official speaking
- D2-611 | The pillar fits are drawn pixel by pixel | Strokes set on the grid left the 16 px curves as grey smudges
- D2-612 | One fit at 16 px, with a 1 px line | A 2 px line at 16 px closes Connect's lens, Track's pin and lens, the book's doubled edge and Act's finger, so no second fit keeps every feature (DR-133)
- D2-613 | The fits fill up to 22 of 24 px, and Act's hand is about a quarter wider than its master's | Each knuckle, the thumb and the ring keep a clear pixel
- D2-614 | In Connect's 2 px fit, pixels where the two rings overlap stay black | The master's black arcs cover both crossings
- D2-615 | The naming test reads each option at 48 px, with me standing in for a first-time reader | The brief's size; the creative director repeats it
- D2-616 | The look-alike flags are read against a baseline of the six originals | A redraw is judged against the drawing it replaces
- D2-617 | The plate page draws each option as an image of its own file at true size | Three inline copies of one SVG would repeat its ids
- D2-618 | Check results sit beside the plate page in `checks/`; the pixel pictures stay in my scratch folder | The engineer asks for the pictures outside `work/build`
- D2-619 | The plate numbers its cards 1 to 8; the board builder sets the board's numbers | The utility set sits between mine on the board

## Questions for Dustin

1. **Which Congress sign?** Recommendation: **set B**, the House chamber from the gallery. It reads as a chamber at 48 px, it is the view you asked for, and it stays apart from R-03 and R-46 on the look-alike check (CL-025 B's closest drawing is R-31, at 0.910). Set A reads as a city hall, and set C needs the label to say "two chambers". One caution: CL-014 B, the chamber inside the fence, is the closest pair to R-46 Expand the House (0.950). If the creative director confirms a reader could confuse the two, CL-014 takes option A while the other three take set B.
2. **CL-059 Credit Allocation.** Recommendation: **B**, the flat-roofed bank with a vault door. It names a bank with no pediment, which the research lead counts with columns under Rule 01.6. A reads as a bank fastest but keeps the temple front; C draws a safe, which says "stored money" until the branches carry it out.
3. **R-48 Agency Independence.** Recommendation: **C**. The commission says "agency" without a building, and the arrow that stops at the brace shows the protection at work. B keeps the lectern, which reads as a speech; A keeps a pediment over a door, which reads as a house.
4. **Testify.** Recommendation: **A**, your own description, which names the subject. B is the same scene on a diagonal; C asks the reader to be the witness.
5. **Contact an official.** Recommendation: **A**, the line with the red speech mark, since it covers a call, an email, a letter and a visit. If you want the phone, **B** keeps it very simple and names the official with the desk at the cord's end (DR-155).
6. **Pillar fits.** Recommendation: **24 px fit A**, the 2 px line, which matches the utility set's line at 24 px and holds its own beside the word; and the one 16 px fit. Fit B's 1 px line is nearer the masters' light hand and looks thin beside text.
7. **Pediments.** Rule 01.6 names domes, columns and flags; the meaning sheet adds pediments. CL-059 A and R-48 A keep theirs because DR-135 names only the columns. Recommendation: treat a pediment as part of the classical front and keep it out, which points to B or C on those two cards.

## Tested

- All 72 SVG files: parse, color-swap identity between editions, no red in black, unique ids, the 128 box and nothing drawn outside it, line widths inside DR-08's range.
- The engineer's look-alike check on the 18 redraws, the 6 new topics and the 12 fits; a baseline run on the six originals; one run across my drawings and the utility set's 24 px options.
- The engineer's pixel-fit check on all 12 fits in both editions at their own size and line: 24 of 24 pass.
- The naming test, as my reading at 48 px of all 24 options.
- Visual review at each step: every drawing at 2x, at 48 px enlarged by whole pixels, and at 48 and 24 px true size; every exported PNG on one sheet; the fits enlarged and at true size. Drawings redrawn after looking are listed in the change log.
- The plate page in Chromium at 1440 and 390 px: every image loads, and nothing scrolls sideways at 390 px.

## Not tested

- No person has named any of these drawings. The naming test is an agent's reading; the creative director's repeat and the combined reader check (DR-143) come later.
- The pixel-fit check on the redraws and new topics, which are drawn for 48 px and up and not to the pixel grid, as the masters are not.
- Rendering outside Chromium, and opening the files in Illustrator, Figma or other tools.
- The plate page's accessibility (axe, keyboard order); it is a capture source for the board builder, not a page for readers.
- Whether readers take set B's red rostrum, or set C's two red rostrums, for a party (DR-114's question); the combined reader check asks it.
- The fits in a live pillar row beside Inter text at 16 and 24 px.

## Change log

Nothing in `source/`, `work/ledger/`, the Civic Line masters, the identity masters or any existing board changed. Nothing was committed or pushed.

**Created**

- `work/build/scripts/phase-2/civic_line_stage_b_common.py`, `civic_line_stage_b_drawings.py`, `civic_line_stage_b_new_topics.py`, `civic_line_stage_b_build.py`, `civic_line_stage_b_pillar_fit.py`, `civic_line_stage_b_plates.py`
- `work/build/assets/civic-line-redraws/`: `src/` (18 source drawings), `svg/` (36), `png/` (72), `20261109_Stage-B-Drawings-Manifest.json`
- `work/build/assets/civic-line-new-topics/`: `src/` (6), `svg/` (12), `png/` (24), `20261109_Stage-B-Drawings-Manifest.json`
- `work/build/assets/pillar-pixel-fit/`: `svg/` (24), `png/` (48), `20261109_Pillar-Pixel-Fit-Manifest.json`
- `work/boards/phase-2/stage-b/drawings/civic-line/20261109_Civic-Line-Drawings-Plates.html`
- `work/boards/phase-2/stage-b/drawings/civic-line/checks/`: `20261109_Likeness-Redraws.json`, `20261109_Likeness-New-Topics.json`, `20261109_Likeness-Pillar-Fits.json`, `20261109_Likeness-Across-Civic-Line-And-Utility.json`, `20261109_Pixel-Fit-16px-Fit-A.json`, `20261109_Pixel-Fit-24px-Fit-A.json`, `20261109_Pixel-Fit-24px-Fit-B.json`
- `work/handoffs/phase-2/20261109_Stage-B-Civic-Line-Icons-Notes.md` (this file)

**Rebuild:** `python3 -I work/build/scripts/phase-2/civic_line_stage_b_build.py`, then `civic_line_stage_b_pillar_fit.py`, then `civic_line_stage_b_plates.py`.

**Redrawn after looking, before the board**

- CL-014 B and C read as a cage, then a trampoline; the chamber now stands inside the whole fence.
- R-13 and R-42, B and C: the chamber's rows closed up at strip scale; the sign moved to a top tier.
- CL-025 C, R-13 C and R-42 C: the side-by-side chambers shrank past naming at 48 px; the pair is now staggered.
- CL-059 B read as a first-aid cross, then a fan, and C as a film camera; they are now a vault wheel and a safe.
- Testify: the microphone read as a lollipop in all three. Testify B read as a jury box and is now a diagonal.
- Contact B read as an alarm bell, so the red moved to the cord. In Contact C the official seemed to speak, so the person is drawn.
- Pillar fits: grey smudges at 16 px; redrawn pixel by pixel.

**Removed:** files from first drafts that this work itself wrote: the Connect 16 px fit B, and the new topic files named with a made-up code.
