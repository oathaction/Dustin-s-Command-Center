# Chapter 16 plan: Photography, illustration and video

Creative director, Phase 4, chat 10, November 21, 2026. Written for the design director, who builds the chapter in `work/build/scripts/phase-4/phase4_ch16_build.py`, and for the editor, who then writes every word a reader sees. Brief: `work/handoffs/phase-4/20261121_Chat-10-Brief.md`, sections 3 and 6.

Inputs read: Master Brief sections 1 to 7, 11, 15, 16, 17 and 22; chapter 02's writing rules; the Gate 3 report's sections 9 and 10; G3-01 to G3-09 and DR-300 to DR-304; the V5 photography entries in the Phase 0 census (95 entries, each cut at 50 characters by the census); the architecture map's V5 chapter 10 rows; Gate 1's S10 and Y6 (G1-03); Rules 01.6, 01.8, 02.9, 03.3, 12.3, 12.4, 12.8, 13.8, 17.1, 17.3, 17.4, 19.2 and 19.4; the two photographs' sidecars; the register rows "SA, the photographs" and "Chapter 19's other seven gaps"; the research lead's "Facts for chapter 16" (written 01:36 to 01:41 UTC); the engineer's contract C1 (written 01:40 UTC).

Draft words in this plan show what each field must say. The editor writes the final words under chapter 02's rules once the design director hands them over.

## 1. The chapter's idea

A photograph in Oath & Action is a record a reader can check. It shows people doing public work, in black and white, with a caption that names who, what, where and when and a credit that names who made it. Where we have no photograph yet, a frame says Placeholder in words. A generated picture never stands for a real event. A video answers one question, and its captions, its soundtrack and its transcript give every viewer the same facts.

The chapter teaches on the two public-domain federal photographs chapter 01 already shows, drawn from the one copy the page embeds (P4-5, contract C1), and on labeled placeholder frames. One photograph serves several crops, so the plates stay few and every one of them is real.

## 2. Opener and intro

- **Number, anchor, title, part:** `16`, `photography`, "Photography, illustration and video", `evidence`.
- **Instruction (fixed):** "Show public life as it happens, and label every placeholder and generated image."
- **Opener plate, `s-16-opener`:** the two teaching photographs side by side at 1440 px (stacked on phones), each at 3:2 in black and white, each with its full caption from chapter 01. Lake Isabella: `data-oa-photo="lake-isabella-2014"` cropped in the plate's CSS at `aspect-ratio:3/2; object-position:50% 50%` (the rectangle 24 0 1152 768), up to 576 px wide. Rotunda: `data-oa-photo="rotunda-2005" data-oa-crop="60 0 1080 720"`, up to 540 px wide; this 3:2 rectangle keeps the Architect of the Capitol's corner mark out, which a CSS crop at 3:2 would not, since it keeps the photograph's full height. Alts: chapter 01's two alts. Draft plate caption: "Our two teaching photographs, each in black and white with its full caption: a federal official answers residents at a public meeting in Lake Isabella, California, in 2014, and members of the public file past Rosa Parks in the Capitol Rotunda in 2005. Both are public-domain works of federal agencies."
- **Intro, draft, two paragraphs:**
  1. "This chapter sets how Oath & Action shows public life in pictures: the photographs we choose and make, the frames that hold a photograph's place until we have it, the few drawn and generated pictures we allow, and the videos we publish. A photograph here is a record. It shows people doing public work, and its caption tells a reader who, what, where and when, so they can check it."
  2. "Two public-domain photographs from federal agencies teach every photograph rule, the same two chapter 01 shows. Until we commission photographs of our own, a frame that says Placeholder holds each one's place. A generated picture serves only as a labeled illustration."

## 3. Groups

| Group | Before rule | Title | Line (draft) |
|---|---|---|---|
| 1 | 16.1 | Choosing and framing a photograph | A photograph shows people at public work, in black and white unless its color is part of the record, and its crop and the words around it keep that work in view. |
| 2 | 16.5 | The record behind each photograph | Each photograph runs with a caption a reader can check and alt text for each crop, and its rights and any consent go into our rights ledger before it runs. |
| 3 | 16.8 | Placeholders and made pictures | A frame that says Placeholder holds the place of a photograph we have yet to make, and a generated picture serves only as a labeled illustration. |
| 4 | 16.10 | Video | A video answers one question. A person checks its captions, its soundtrack says what the screen shows, and it plays only when a viewer presses Play. |

## 4. The rules

Thirteen rules and one extra. The brief asked for about 12; Master Brief section 16 names sixteen subjects, and thirteen rules carry them with no rule doing two jobs. Every photograph plate draws from contract C1 as revised at 01:45 UTC and live since 01:51 UTC: an `<img>` with `data-oa-photo` and its own `alt`, cropped either in the plate's CSS (`object-fit:cover`, an `aspect-ratio` and an `object-position`, the way chapter 01 crops) or, for a tight crop, by `data-oa-crop="x y width height"`. The black and white treatment is `filter: grayscale(1)` on the plate's photograph class; under `data-oa-crop` the build's wrapping frame takes the same class. No plate embeds a file. Below, a crop written as a rectangle with a ratio and a focus means the CSS way; a rectangle alone means `data-oa-crop`. Every crop below was checked by eye on the 1,200 px renditions (previews in my scratch folder).

A note on sharpness from C1: a crop looks sharp on a 2x screen while its width in photograph pixels is at least twice the frame's CSS width. Each plate size below keeps to that.

### Group 1. Choosing and framing a photograph

#### 16.1 Photograph public work while it happens.

- **Teaches:** what to photograph and what to leave out. The title is chapter 02's approved rewrite of V5's headline (Rule 02.9's after: "Photograph public work while it happens, such as a hearing or a polling place.").
- **Rule, draft:** "Photograph people while they do public work, such as a resident testifying, a clerk counting ballots or an official answering questions at a public meeting, with officials among them. Choose the frame where the act and the people it serves are both in view. Leave raised fists, megaphones, flag-waving, handshake close-ups, the dome at sunset, protest signs used as a motif, glossy stock and crowds of identical smiling people out of our pictures, because each stands for civic life in general and shows no decision a reader can follow."
- **Why, draft:** "A reader can check a picture of a real meeting on a real day, and a picture of the idea of one gives them nothing to check."
- **Correct plate `s-16-1-correct`: the shot list.** Live text, a commissioning brief at true size, no photograph. Columns: Subject, Where, How, Status. The first two rows are the photographs we have, each with Status "In the guide (Rule 01.6)" and "In the guide (Rule 01.8)". Then V5's ten subjects, kept as the architecture map says (Keep, "Settings from more states", DC-06), each given a level of government and a Census region, each with Status "To commission; a placeholder holds its place (Rule 16.8)". Proposed spread: a planning board meeting in a school cafeteria (town, Northeast); a resident testifying at a microphone in a state house hearing room (state, Midwest); a kitchen table with bills and a laptop at night (household, South); a polling place in a gymnasium (county, West); a small business owner at the counter (city, West); neighbors talking on a front porch (neighborhood, South); a union hall meeting (Midwest); a library bulletin board with meeting notices (town, Northeast); veterans and families at a town hall (a member of Congress's district meeting, South); a volunteer with a clipboard on a sidewalk (city, West). The How column takes V5's lines; the census cuts six of them at 50 characters ("Folding tables, paper agendas, residents on the be…", "From the side, at eye level. The dais stays in fra…", "Wide, from the door. The line, the booths, the ban…", "Mid-task. The register, the window, the street out…", "From the back of the hall. The folding chairs coun…", "Walking toward the camera, mid-conversation with a…"), so the editor completes them, and rewrites "Hands, not faces." under Rule 02.9. The polling place row adds "Ask the election official first; never a marked ballot or a person voting."
- **Failure plate `s-16-1-failure`:** `rotunda-2005`, `data-oa-crop="240 0 720 360"` (2:1), black and white, 480 px wide. The crop keeps the two paintings, the carved panels and the pilasters and no one in the room. Caption: "The Rotunda of the U.S. Capitol, Washington, D.C., October 2005. Photograph: Architect of the Capitol." Draft failure caption: "Fails Rule 16.1. Cropped to its paintings and carved panels, the same photograph shows an empty room, so it stands for government in general and records no public act." Alt: "The upper walls of the Capitol Rotunda: two large framed paintings between carved stone panels and pilasters."
- **Specifications:** Subject: people doing public work, officials among them. Frame: the act and the people it serves both in view. Light: available light, at eye level (V5's "Documentary, available light, eye level."). Staging: none; photograph what happens. Settings: spread across states, regions and levels of government, logged in chapter 01's rotation log (Rules 01.9, 01.10, 01.12). Leave out: the list in the rule.
- **Basis:** Design judgment, from our fifth edition's photography direction and Master Brief section 16.
- **Tokens:** `oa.type.label` (table heads), `oa.type.body.small`, `oa.color.border.hairline`.
- **Related:** Rules 01.6, 01.7, 01.8, 01.9, 01.10, 01.12, 02.9.
- **WCAG:** none of its own.
- **For builders, draft:** "Write the subject and the act you need in the shot list's form before a shoot or a search, then choose the frame where the act is happening."

#### 16.2 Show a photograph in black and white, and keep color only where it is part of the record.

- **Teaches:** the treatment. Gate 1's S10, approved by Dustin (G1-03): "Black and white, with color where color is evidence." V5's two treatments (Natural color as the default, Charcoal duotone for dark beats) become black and white as the default and color as the exception.
- **Rule, draft:** "Show every photograph in black and white, converted from the color original, unless its color is part of what it records, such as the brown of tap water a resident holds up at a hearing. A photograph kept in color says in its caption what the color shows. Change only tone and exposure, evenly across the frame; leave tints, color grades, vignettes and filters off, since each changes how the place looked."
- **Why, draft:** "Black and white keeps a photograph's own reds and blues off our page. The Rotunda photograph in color holds red coats and red, white and blue wreaths; in black and white the view's one working red (Rule 05.3) stays the only red a reader sees, and red never meets blue beside our marks. It also lets photographs from different agencies, cameras and years sit together as one publication."
- **Correct plate `s-16-2-correct`:** two panels. (a) `rotunda-2005`, `data-oa-crop="60 0 1080 720"`, black and white, 540 px wide, chapter 01's caption and alt. (b) A placeholder frame (Rule 16.8's drawing) at 3:2, 260 px wide: "Placeholder. A resident holds up a jar of brown tap water at a city council hearing. Kept in color, since the water's color is the evidence, and the caption says so in words."
- **Failure plate `s-16-2-failure`:** `lake-isabella-2014` at 3:2 (CSS, `object-position:50% 50%`), 540 px wide, with a Prussian duotone: black and white first, then a Prussian layer over the frame in an HTML element with `mix-blend-mode` (C1 allows marks over a photograph in HTML; the design director picks the blend that reads as a duotone). Same caption and alt as chapter 01. Draft failure caption: "Fails Rule 16.2. A Prussian tint dresses the people at the meeting in our color, as if they belonged to our message, and shows a room that never looked that way." No red on this plate, so the failure is the tint alone.
- **Specifications:** Default: black and white, from the color original. On screen: `filter: grayscale(1)` on the photograph and nothing else. For print or an export: a grayscale conversion of the original file, never of the 1,200 px rendition (register row "SA, the photographs"). Color: only where it is part of the record, named in the caption. Adjust: tone, exposure and contrast, evenly across the frame. Never: a tint, a duotone in a brand color, a color grade, a vignette or a filter. On Charcoal: the photograph unchanged; the caption takes Charcoal's text tokens.
- **Basis:** Gate 1 recommendation S10, approved by our founder and editor (G1-03); design judgment for the reasons.
- **Tokens:** `oa.type.caption`, `oa.color.text.primary`; on Charcoal `oa.color.text.primary.onCharcoal`.
- **Related:** Rules 05.3, 01.1, 01.6, 19.1.
- **WCAG:** 1.4.1 Use of Color (A): a photograph kept in color names what its color shows in the caption, so color is never the only carrier.
- **For builders, draft:** "On a page, set `filter: grayscale(1)` on the photograph. For print, convert the original file and compare it with the screen version at the same size."

#### 16.3 Crop to keep the act whole, and change nothing inside the frame.

- **Teaches:** cropping across the five ratios the system uses, and image integrity.
- **Rule, draft:** "Crop a photograph so the person acting, at least one person they serve and the thing they are working on stay in view at every ratio it runs at. One photograph can serve all five ratios below; set each crop by hand and check that the caption still describes what the crop shows. A mark laid on the picture after it was taken, such as an agency's corner logo, comes out in the crop, and its credit goes in the caption. A sign, a map or a badge that was in the room stays, since it is part of what happened. Add, move, remove and retouch nothing inside the frame."
- **Why, draft:** "A crop decides what a reader believes happened. Cut the residents away and an official seems to lecture no one; cut the official and the caption names a man who is no longer there."
- **Correct plate `s-16-3-correct`:** `lake-isabella-2014` four times, black and white, each labeled under its frame with its ratio, its use and its focus:

  | Ratio | Use | Plate CSS | Rectangle | Shown at |
  |---|---|---|---|---|
  | 3:2 | Article and report | `aspect-ratio:3/2; object-position:50% 50%` | 24 0 1152 768 | 360 px |
  | 16:9 | Video poster and thumbnail | `aspect-ratio:16/9; object-position:50% 20%` | 0 19 1200 675 | 360 px |
  | 1:1 | Square post | `aspect-ratio:1/1; object-position:25% 50%` | 108 0 768 768 | 240 px |
  | 4:5 | Portrait post | `aspect-ratio:4/5; object-position:35% 50%` | 205 0 614 768 | 240 px |

  Two rows at 1440 px (the wide pair, then the tall pair), one column on phones. Each keeps the official's face and hand and at least one resident; the 1:1 also keeps both residents and an edge of the map. One shared caption under the set. Each use carries its own alt (Rule 16.7); for the 1:1 and 4:5, "An official explains something to residents, his arm reaching past one of them."
- **Failure plate `s-16-3-failure`:** `lake-isabella-2014`, `data-oa-crop="660 0 540 675"` (4:5), black and white, 240 px wide, with chapter 01's caption, which names Paul Zianno. The crop keeps one resident's back and the map; the official is gone. Draft failure caption: "Fails Rule 16.3. The portrait crop keeps a resident and the map and cuts out the official, so the caption names a man the picture no longer shows." Alt: "A resident, seen from behind, faces a large project map on an easel."
- **Specifications:**
  - Ratios: 3:2, the default for articles, reports and web pages; 16:9, a video's poster frame and thumbnail (YouTube's 1280 x 720, chapter 23); 1:1, a square post (1080 x 1080); 4:5, a portrait post (1080 x 1350); 1.91:1, the share preview (1200 x 630, chapter 20). Platform sizes are the research lead's to confirm in `work/research/20261121_Platform-Specifications.md`.
  - Keep in every crop: the person acting, at least one person they serve, and what they work on where it fits.
  - Remove: a mark laid on after the picture was taken. Keep: signs, maps and badges that were in the room.
  - Smallest shown: 240 px wide (design judgment; below that, faces and hands stop reading).
  - Sharpness: the crop's width in photograph pixels at least twice the frame's width (C1).
  - Print: 300 pixels per inch at the printed size, made from the original file.
  - Crops for builders, both photographs, as rectangles in the photograph's pixels (any of them works as a `data-oa-crop`):

  | Ratio | Lake Isabella | Rotunda |
  |---|---|---|
  | 3:2 | 24 0 1152 768 | 60 0 1080 720 |
  | 16:9 | 0 19 1200 675 | 0 0 1200 675 |
  | 1:1 | 108 0 768 768 | 300 0 720 720 |
  | 4:5 | 205 0 614 768 | 370 0 576 720 |
  | 1.91:1 | 0 21 1200 628 | 0 0 1200 628 |

  Every Rotunda rectangle stops at row 720 or above, so the agency's mark at the lower right stays out.
- **Basis:** Society of Professional Journalists, Code of Ethics, revised October 4, 2026: "Take responsibility for the accuracy of their work before releasing it." and "Never publish fabricated content that could be confused with reality." Design judgment for the ratios.
- **Tokens:** `oa.type.label` (ratio labels), `oa.color.text.secondary`.
- **Related:** Rules 01.6, 01.8; chapters 20 and 23.
- **WCAG:** none of its own.
- **For builders, draft:** "Take a crop from the table, then read the caption against the cropped picture. If a person the caption names has left the frame, choose another crop."

#### 16.4 Set words beside a photograph or on a solid panel, never on the picture itself.

- **Teaches:** words and photographs. V5's "Type never sits on a busy image." (architecture map: Keep), joined to Rules 03.3 and 19.4.
- **Rule, draft:** "Set a headline, a label or a logo beside a photograph, or on a solid Charcoal or Newsprint panel laid over a plain part of it that covers no face, no hand at work and no sign. Words never sit straight on the image, with or without a shadow or a gradient behind them."
- **Why, draft:** "Over a photograph, the ground under each letter changes from one letter to the next, so parts of a headline fade for every reader. A solid panel gives the words one ground and a contrast we can measure, and live text grows, reflows and reads aloud (Rule 19.4)."
- **Correct plate `s-16-4-correct`:** an article opener at true size: a kicker that opens with one content label (Rule 01.21; the design director picks it), a headline set above the photograph as live text in `oa.type.h3`, then `lake-isabella-2014` at 3:2, black and white, 540 px wide, then chapter 01's caption. Draft headline, from the agency's record: "At a public meeting in 2014, the Army Corps walked Lake Isabella residents through the dam project's proposed land purchases."
- **Failure plate `s-16-4-failure`:** the same headline in Newsprint at `oa.type.h3`, set straight on the same photograph across the residents and the map, with a soft text shadow. The design director measures the lowest contrast under the letters on the plate and prints the figure in the caption. Draft failure caption: "Fails Rule 16.4. Set on the picture, the headline crosses dark coats and a pale map, so parts of it fall to [measured] to 1, and it covers the people the meeting was for."
- **Specifications:** Beside the photograph: the default. Panel: solid `oa.color.surface.charcoal` or `oa.color.surface.newsprint`, words in that surface's text tokens (Newsprint on Charcoal measures 13.29 to 1). A panel covers: a plain area, never a face, a hand at work or a sign. Never: words on the image, a text shadow, a gradient scrim. A logo over a photograph: Rule 03.3's panel.
- **Basis:** WCAG 2.2 SC 1.4.3 and SC 1.4.5; our fifth edition's rule.
- **Tokens:** `oa.color.surface.charcoal`, `oa.color.surface.newsprint`, `oa.color.text.primary.onCharcoal`, `oa.type.h3`.
- **Related:** Rules 03.3, 19.4; chapters 20 and 23.
- **WCAG:** 1.4.3 Contrast (Minimum) (AA); 1.4.5 Images of Text (AA).

### Group 2. The record behind each photograph

#### 16.5 Caption who, what, where and when from the record, then credit the maker.

- **Teaches:** the caption's parts, its source, and how far it may go.
- **Rule, draft:** "Write each caption from the record: the agency's own caption, our capture notes or the event's public notice. Name who is shown, what they are doing, where and when, in that order, then give the credit. Give only as much as the record holds: when it knows only the month, the caption gives only the month. Claim no feeling, motive or result that the picture and the record do not show."
- **Why, draft:** "A caption is the part of a photograph a reader can check, and each of its four parts sends them to a record. A guess in any part spends the trust the photograph earned."
- **Correct plate `s-16-5-correct`:** `rotunda-2005` at 3:2 (`data-oa-crop="60 0 1080 720"`), black and white, 240 px wide, beside chapter 01's caption set at true size, with each part underlined and keyed by a small label under it: Who ("Members of the public", "Rosa Parks, the civil rights pioneer"), What ("file past the casket", "as she lies in honor"), Where ("in the Rotunda of the U.S. Capitol, Washington, D.C."), When ("October 2005"), Credit ("Photograph: Architect of the Capitol."). A note under When, from the sidecar: "The record dates the event to October 30 or 31, so the caption gives the month." The underline follows chapter 02's `ins` style; the keys are live text, read in order.
- **Failure plate `s-16-5-failure`:** `lake-isabella-2014` at 3:2, black and white, 540 px wide, chapter 01's alt, with an invented caption and the Illustrative label beside it: "Angry Lake Isabella homeowners confront an Army official over the seizure of their land, March 2014. Photograph: John Prettyman, U.S. Army." Draft failure caption: "Fails Rule 16.5. The caption claims anger and a seizure that neither the picture nor the agency's record shows; the record says he discussed proposed real estate actions with residents."
- **Specifications:**
  - Order: who, what, where, when, then the credit.
  - Who: officials by name and role, from the record; members of the public unnamed unless the record names them and they agreed (Rule 16.6).
  - What: present tense, the act in view.
  - Where: the place, the city or town, and the state written out.
  - When: the date in words (house rule H05), only as exact as the record.
  - Credit: "Photograph: John Prettyman, U.S. Army." when the maker is named; "Photograph: Architect of the Capitol." when the agency is the maker; "Photograph: Dustin Cathcart, Oath & Action." for ours; "Photograph: [name] for Oath & Action." for a photographer we hire. The editor confirms the last two forms.
  - Never: the website that hosts the file, such as Wikimedia Commons, in place of the maker; a guess.
  - Length: one or two sentences.
- **Basis:** SPJ Code of Ethics, revised October 4, 2026: "Take responsibility for the accuracy of their work before releasing it." and "Never plagiarize. Always attribute." Rule 01.8.
- **Tokens:** `oa.type.caption`, `oa.type.label` (keys), `oa.color.graphic.essential` (the underline, as chapter 02's `ins`).
- **Related:** Rules 01.8, 13.6, 13.12, and 02.22 for house rule H05.
- **WCAG:** none of its own. The caption carries the facts the alt text leaves out (Rule 16.7).

#### 16.6 Before a photograph runs, record its rights and any consent it needs.

- **Teaches:** capture at public events for the two makers DR-301 names, consent, children, and the rights record.
- **Rule, draft, two paragraphs:**
  1. "Dustin, on a phone at a public event, and any photographer we hire work to the same rules. Check the host's rules on cameras before the event starts, and photograph from where the public may stand. A public official doing public work may be shown and named by role. A member of the public may appear in a scene and stay unnamed. Ask a person's permission, and write down the answer, before you single them out in a close picture or name them in a caption. Show a person under 18 so they can be recognized only with a parent's or guardian's permission. Stop photographing anyone who asks you to, and leave their picture out."
  2. "Before any photograph runs, give it a row in our rights ledger: who made it, where it came from, the license or permission that covers it, and any consent. Some of this is a matter of state law that differs from state to state, such as recording a conversation's sound or using a person's likeness, and this guide gives no legal advice."
- **Why, draft:** quote SPJ: "Private people have a greater right to control information about themselves than public figures and others who seek power, influence or attention." and "Use heightened sensitivity when dealing with crime victims (especially victims of sex crimes), juveniles, and sources or subjects who are inexperienced or unable to give consent." The editor may add "Recognize that legal access to information differs from the ethical justification for reporting it."
- **Correct plate `s-16-6-correct`:** `lake-isabella-2014` at 3:2, black and white, 540 px wide, with two numbered markers set in HTML over the frame as C1 allows, then a key and the rights record.
  - Marker 1 beside the official, on the plain wall to the right of his head, about 36 percent across and 12 percent down; never on a face. Key: "Named by role. A public official at a public meeting, named in the agency's own caption."
  - Marker 2 on the right resident's back, about 66 percent across and 72 percent down. Key: "Unnamed. Members of the public, seen from behind and named nowhere in the record."
  - Markers: 24 px circles, `oa.color.surface.charcoal` fill, Newsprint numeral, a 1 px Newsprint ring so they read on light and dark parts; hidden from a screen reader, since the key carries their words. The design director checks both positions by eye.
  - The record, as a compact two-column list from the sidecar and the rights ledger: Maker, John Prettyman, U.S. Army. Agency, U.S. Army Corps of Engineers, Sacramento District. Date, March 27, 2014. Place, Lake Isabella, Kern County, California. License, public domain in the United States as a work of the federal government (17 U.S.C. 105), read on the Commons file page November 21, 2026. Consent, none needed: one official at public work, named by his agency; residents unnamed and seen from behind. Rights rows, pho-04 and pho-04r.
- **Failure plate `s-16-6-failure`:** a placeholder frame (Rule 16.8's drawing) at 4:5, 240 px wide: "Placeholder for this failure: a close portrait of a ninth grader speaking at a school board meeting." Its caption, with the Illustrative label beside the name and beside the place: "Maya Brooks, 14, a ninth grader at Alder County High School, asks the school board to keep the late bus, April 2026. Photograph: Oath & Action." Its record line: "Permission from a parent or guardian: none recorded." Draft failure caption: "Fails Rule 16.6. The caption names a 14-year-old and her school, and the record holds no permission from a parent or guardian."
- **Specifications:**
  - Makers: Dustin on a phone at public events; a hired photographer; one set of rules (DR-301).
  - Before the event: the host's rules on cameras, which differ by body.
  - Officials doing public work: shown and named by role.
  - Members of the public in a scene: shown and unnamed.
  - A close picture or a named caption of a private person: their permission, written into the record.
  - Under 18: recognizable only with a parent's or guardian's permission.
  - Asked to stop: stop, and leave the picture out.
  - Polling places: ask the election official first; never a marked ballot or a person voting.
  - Matters of state law: recording a conversation's sound (the Reporters Committee for Freedom of the Press keeps a state-by-state guide), a person's likeness, pictures of minors. No legal advice.
  - The rights ledger row: maker, source, date, place, license or permission, consent, where the caption came from, the file and its original.
- **Basis:** SPJ Code of Ethics, revised October 4, 2026; Reporters Committee for Freedom of the Press, "Reporter's Recording Guide"; DR-301; design judgment for the record's fields.
- **Tokens:** `oa.color.surface.charcoal`, `oa.color.text.primary.onCharcoal`, `oa.type.label`, `oa.type.body.small`.
- **Related:** Rules 01.8, 13.8; the rights ledger (chapter 27 at Phase 5).
- **WCAG:** none of its own; the markers' meaning sits in live text (1.1.1).

#### 16.7 Write alt text for what each crop shows.

- **Teaches:** alt text written for purpose, per use, as contract C1 allows. Rule 19.2 sets alt text for every image; this rule applies it to photographs and their crops.
- **Rule, draft:** "Write alt text for each use of a photograph, for what that crop shows happening, in one or two sentences. Leave the names, the place, the date and the credit to the caption, which a screen reader also reads. When a photograph runs at a new crop, write its alt text again."
- **Why, draft:** "One photograph can run in five crops, and each shows something different. Alt text written for the wide frame describes things a tight crop has cut away."
- **Correct plate `s-16-7-correct`:** `rotunda-2005` twice, black and white, each with its alt printed visibly under the frame in a line headed "Alt text" (the same words sit in the `alt` attribute):
  - Wide, `data-oa-crop="60 0 1080 720"`, 360 px: "Mourners file past a casket ringed by velvet ropes in the Capitol Rotunda, under its paintings and statues." (chapter 01's)
  - Tight, `data-oa-crop="0 77 576 720"` (4:5), 280 px: "Mourners wait in line along velvet ropes in the Capitol Rotunda, beside a wreath and under a large painting." This crop holds the line of mourners, a wreath, a painting and a statue, and no casket.
  - One shared caption under both.
- **Failure plate `s-16-7-failure`:** the tight crop at 280 px, carrying the wide crop's alt, printed visibly as above. Draft failure caption: "Fails Rule 16.7. The tight crop reuses the wide crop's alt text, so a screen reader hears of a casket this crop has cut away."
- **Specifications:** Length: one or two sentences. Says: what is happening and who acts, in plain words. Leaves to the caption: names, place, date, credit. Each use: its own alt for its own crop. Never: a file name, "photo of" or "image of", the caption repeated. A placeholder frame: live text, no alt (Rule 16.8). A generated image: alt text that begins "Generated image" (Rule 16.9).
- **Basis:** WCAG 2.2 SC 1.1.1; Rule 19.2.
- **Tokens:** `oa.type.label` (the "Alt text" head), `oa.type.body.small`.
- **Related:** Rules 19.2, 16.3.
- **WCAG:** 1.1.1 Non-text Content (A).

### Group 3. Placeholders and made pictures

#### 16.8 Hold a commissioned photograph's place with a frame that says Placeholder.

- **Teaches:** the placeholder, settled by Master Brief section 16 ("A placeholder announces itself as a placeholder, never as a photograph.") and P4-3. Term at first use: a placeholder here is a frame that holds a picture's place, apart from the placeholder text in a form field that chapter 18 rules out. The editor settles the wording under house rule H02.
- **Rule, draft:** "Until we commission a photograph, a placeholder holds its place: a frame at the photograph's ratio and size, with the word Placeholder at its top, the shot it waits for in live text and the caption's parts still to write. It imitates no photograph, so it takes no gray fill, texture, silhouette or stock picture. A published piece with no photograph runs without one; placeholders belong in this guide, in templates and in drafts."
- **Why, draft:** "A gray box at a photograph's size reads as a picture still loading, and our fifth edition's panels told a screen reader 'Photograph' for pictures that did not exist. Words in the frame tell every reader what is missing and what will fill it."
- **Correct plate `s-16-8-correct`:** two frames.
  - (a) 3:2 at 540 px on Newsprint. Top left inside: "Placeholder" (`oa.type.label`, text primary), then "Photograph to commission" (`oa.type.label`, text secondary). Middle, in `oa.type.body`: "A resident testifies at a microphone in a state house hearing room, seen from the side at eye level, with the committee's dais in frame." Bottom left: "3:2 · Black and white · Shot list, row 4 (Rule 16.1)". Under the frame, in `oa.type.caption`, text secondary: "Caption to write from the record: who, what, where and when, then the credit."
  - (b) The same frame at 4:5, 240 px, on a Charcoal panel in Charcoal's tokens, to show the frame in a dark mode.
  - The drawing: a 1 px keyline in the surface's strong border (`oa.color.border.strong`; Charcoal on Newsprint, Newsprint on Charcoal), no fill, padding `oa.space.300`, and four corner crop marks outside the frame (1 px, 12 px arms, 6 px off each corner) in the same ink, a printer's sign for where a picture's edges fall. No dashed line, since dashes carry evidence grades in chapters 13 and 15, and no cross through the frame, which a newcomer could read as a failure mark.
  - Markup: a `figure` of live text, the word Placeholder first in reading order, no `role="img"` and no alt.
- **Failure plate `s-16-8-failure`:** our fifth edition's panel, redrawn: a 3:2 box at 540 px filled with Stone, a small Newsprint caption bar inside reading "A polling place in a gymnasium" over a tiny "Natural color / 3:2". It sits in an image stage whose plate alt describes it, so the guide's own reader is never misled: "Failure: a Stone panel at a photograph's size, which our fifth edition announced to screen readers as 'Photograph: A polling place in a gymnasium'." Draft failure caption: "Fails Rule 16.8. Our fifth edition's panel looks like a picture still loading, and a screen reader announced it as a photograph that never existed."
- **Specifications:** Frame: the photograph's ratio and display size; a 1 px keyline in the surface's strong border; no fill; four corner crop marks. Words: "Placeholder", what it waits for, the shot, the ratio and the treatment. Caption: the parts still to write. Markup: live text in a figure; no image role, no alt. Where: the guide, templates and drafts. Never: a published piece. Surfaces: Newsprint, White and Charcoal.
- **Basis:** Master Brief section 16; WCAG 2.2 SC 1.1.1; the Phase 0 rights audit of our fifth edition (`work/handoffs/phase-0/20261020_Research-Rights-Audit.md`, "Photography in V5").
- **Tokens:** `oa.color.border.strong`, `oa.type.label`, `oa.type.body`, `oa.type.caption`, `oa.color.text.secondary`, `oa.space.300`; on Charcoal, the `onCharcoal` text and border tokens.
- **Related:** Rules 16.1, 13.8; chapter 18's form fields, for the word.
- **WCAG:** 1.1.1 Non-text Content (A); 1.3.1 Info and Relationships (A).

#### 16.9 Label a generated image beside it, and never let one stand for a real event.

- **Teaches:** where a generated image may serve and how it is labeled, on the guide and on each platform. Settled: Master Brief section 16, P4-3 (G3-08), and the studio's call for this chat, no generated image.
- **My judgment on P4-3's test:** this rule can show its own label without a generated image. The label is three things, a tab on the picture's corner, a caption line and the start of the alt text, and a placeholder frame shows all three at true size, on a solid tab that reads the same over any picture. Nothing goes to Dustin from this rule.
- **Rule, draft:** "A generated image is a picture an AI tool makes from a written prompt. It may serve only as a labeled conceptual illustration or as the scene around our real work in a mockup. It carries the words 'Generated image' on a solid tab at its top left corner, its caption says what idea it shows and names the tool and the date, and its alt text begins 'Generated image'. It never shows a real person or a real place on a real day, and nothing a reader could take for a photograph of an event. Where a platform has its own label, we turn it on too, and we keep the Content Credentials some tools write into the file. Each one gets a rights row with the tool, the date, the prompt and the tool's terms."
- **Term at first use:** Content Credentials, the C2PA data some tools write into a file; YouTube and TikTok read it to label content, and LinkedIn shows an icon for it (research lead, section C).
- **Why, draft:** quote SPJ: "Never publish fabricated content that could be confused with reality. Clearly label illustrations and reenactments." and "Clearly identify the sources and technology that shape the creation of news."
- **Correct plate `s-16-9-correct`:** a 3:2 placeholder frame at 540 px (Rule 16.8's drawing), headed above the frame "Placeholder · Generated image to make". Inside, at the top left, the "Generated image" tab exactly where it sits on a real one: solid `oa.color.surface.charcoal`, Newsprint words in `oa.type.label`, padding 4 px by 8 px, flush to the corner. In the middle, the written prompt in `oa.type.body.small`: "A phone lying screen up on a kitchen table beside a folded utility bill and a mug, morning light, seen from above. The screen is blank for our page to be placed on. No people, no logos, no words." Under the frame, the caption: "Mockup: where a reader meets our explainer. The page on the screen is ours; the scene is a generated image, [tool], [date]." with the tool and date shown as fields to fill once it is made, and a record line: "Rights row: tool, date, prompt, terms read. File: YYYYMMDD_Generated-Mockup-Kitchen-Table-Phone.png". The plate teaches the mixed case, which Rule 13.8 sets for invented and real items: our real page keeps its own credit, and the generated scene carries its label.
- **Failure plate `s-16-9-failure`:** a 3:2 placeholder frame at 540 px: "Placeholder for this failure: a generated picture of a packed hearing room." No tab. Its caption, with the Illustrative label beside the event: "Residents fill the Alder County hearing room before the rezoning vote, March 3, 2026. Photograph: Oath & Action." Draft failure caption: "Fails Rule 16.9. A generated picture runs with a news caption and a photograph's credit, so a reader believes a hearing looked this way."
- **Specifications:**
  - May serve as: a conceptual illustration; the scene around our real work in a mockup.
  - Label on the picture: "Generated image", on a solid Charcoal tab, top left.
  - Caption: the idea it shows, then "Generated image, [tool], [date]".
  - Alt text: begins "Generated image".
  - Never: a real person, a real place on a real day, evidence, documentary imagery, or the hand-drawn spot illustration's job (the extra below).
  - File name: `YYYYMMDD_Generated-[Subject].png`. Rights row: tool, date, prompt, the tool's terms as read.
  - Content Credentials: keep them in the file.
  - Platform labels, from the research lead's section C, each turned on wherever it exists:

  | Platform | Its label | What we do | Status |
  |---|---|---|---|
  | YouTube | The "AI use" setting in YouTube Studio; viewers see that the content is AI generated or altered | Answer Yes for any generated or altered realistic content | read |
  | TikTok | Its creator label for AI-generated content; required for realistic scenes or people | Turn on the label | rule read; label words from a search result |
  | Instagram, Threads, Facebook | "AI info"; Instagram's "Label as made with AI" when sharing | Turn on the label | newsroom read; Instagram help from a search result |
  | LinkedIn | No label a poster sets; shows the Content Credentials icon when the file carries C2PA data | Keep Content Credentials in the file | read |
  | X | No label a poster sets was found; X may add "Manipulated media" | Our own tab and caption carry the label | search result |

- **Basis:** Master Brief section 16; P4-3 (G3-08); SPJ Code of Ethics, revised October 4, 2026; the platforms' help and policy pages (sources list).
- **Tokens:** `oa.color.surface.charcoal`, `oa.color.text.primary.onCharcoal`, `oa.type.label`, `oa.type.caption`.
- **Related:** Rules 13.1, 13.8, 16.8; chapter 23.
- **WCAG:** 1.1.1 Non-text Content (A): the label reaches a screen reader through the alt text.

#### Extra after 16.9: Where each kind of picture may appear (`s-16-picture-kinds`)

A table, live text, so a builder can choose in one look. Draft rows:

| Kind | Where it may appear | Its label | Never | Rules |
|---|---|---|---|---|
| Documentary photograph | Articles, reports, web pages, social posts, video | Caption: who, what, where, when, then "Photograph: maker" | Tinted, cropped to change what happened, under words | 16.1 to 16.7, 01.6, 01.8 |
| Placeholder | This guide, templates, drafts | "Placeholder" in its frame | A published piece | 16.8 |
| Hand-drawn spot illustration | Article openers, report spreads, event signs; 96 px and larger; drawn by a person in Charcoal on Newsprint (Gate 1, Y6) | "Illustration: maker" | An icon; red and blue together; a Capitol dome or scales; a generated drawing in its place | Gate 1, Y6 |
| Exploded view | The atlas's three layers only | Its names, flat beside each plane | Anything else | 12.8 |
| Generated image | A conceptual illustration; the scene around our work in a mockup | "Generated image" tab, caption with tool and date, alt that begins "Generated image" | Evidence, a real person, a real place on a real day | 16.9 |

Draft caption: "Five kinds of picture, where each may appear, how each is labeled and the rule that sets it." Gate 1's treatments map also noted that study 05, the hand-drawn icon study, was likely generated and cannot ship, so no spot illustration exists yet; a commission fills that row.

### Group 4. Video

The four video rules follow one example video through its parts, built on chart S04 from chapter 14 (reported voting by age, 2020 and 2024, from the Census Bureau's Current Population Survey), so every figure a plate shows is real and sourced. The video itself does not exist yet, so each video plate carries the Illustrative label at its head, and the figures keep S04's source line.

#### 16.10 Make each video answer one question, from its title frame to its step.

- **Teaches:** short-video structure, the two forms DR-301 sets, the name plate, and the rules chapter 23 draws to.
- **Rule, draft:** "Each video answers one question a viewer could ask, such as 'Which age groups reported voting in 2024?' It takes one of two forms, Dustin on camera as host or his voice over charts and atlas views, and it may move between them. The first sentence spoken asks the question or answers it. Every chart on screen carries its source line for as long as it shows. The video ends on a step a viewer can take, then the end frame. The first time Dustin appears, his name plate reads 'Dustin Cathcart, Founder and Editor'. L8 signs the corner (Rule 12.3). Chapter 23 draws the title frame, the end frame, the name plate and each platform's safe areas."
- **Why, draft:** "A viewer scrolling a feed decides fast whether to stay, so the question comes first. A video that answers one question can be captioned, described and summed up in one sentence, which its card needs (Rule 16.13)."
- **Correct plate `s-16-10-correct`:** a storyboard of six 16:9 frames, 200 px wide each, in two rows of three at 1440 px and two columns on phones. Each frame shows its start time above and the words said below. Frames are drawn in type and tokens; no photograph.
  1. 0:00. Title frame, a slot labeled "Drawn in chapter 23", holding the question.
  2. 0:02. A placeholder frame, "Placeholder: Dustin Cathcart on camera", with the name plate "Dustin Cathcart, Founder and Editor" in the lower third. Said: "Which age groups told the Census Bureau they voted in 2024? Here is what its survey found."
  3. 0:08. S04's chart in miniature, or a frame naming it, with its source line in the frame. Said: "Citizens 18 to 24 reported voting at 47.7 percent, down 3.7 points from 2020. Those 65 and over stayed near 75 percent."
  4. 0:30. The gap, marked. Said: "So the gap between the youngest and the oldest grew from 23 points to 27. These are answers to a survey, which run higher than counted ballots."
  5. 0:50. The step, on Newsprint, in the view's working red under Rule 05.3. Said: "Your state's election office can tell you whether you are registered."
  6. 1:00. End frame, a slot labeled "Drawn in chapter 23".
  
  Every figure comes from S04's title, alt and notes; the editor checks each against the spec (`work/build/chart-kit/specs/s04.json`).
- **Failure plate `s-16-10-failure`:** the same strip with other times: 0:00, the lockmark animates to music for eight seconds; 0:08, the host says "Hey everyone, welcome back"; 0:21, the question. Illustrative at its head. Draft failure caption: "Fails Rule 16.10. The question arrives at 0:21, after an animated logo and a greeting, so a viewer who scrolls on never learns what the video answers."
- **Specifications:**
  - Question: one, in a viewer's words.
  - Forms: Dustin on camera as host; his voice over charts and atlas views (DR-301).
  - First sentence: asks or answers the question.
  - Charts: from the chart kit, each with its source line on screen while it shows (house rule H04, Rule 13.6).
  - Name plate: "Dustin Cathcart, Founder and Editor", the first time he appears; chapter 23 places it inside the caption-safe area.
  - Signature: L8, 24 px in from the top and side edges (Rule 12.3).
  - Ending: the step, then the end frame. A process piece names the step and leaves the position to the viewer (Rule 01.22); a position piece shows its label before the ask (Rule 01.23).
  - Title and end frames: chapter 23, at 1920 x 1080 and 1080 x 1920, each with its caption-safe area.
  - Music: under the voice, and silent while a figure is read (design judgment).
- **Basis:** Design judgment; DR-301; DC-01 for the step.
- **Tokens:** `oa.color.surface.charcoal`, `oa.color.surface.newsprint`, `oa.type.label`, `oa.type.caption`.
- **Related:** Rules 12.3, 13.6, 01.22, 01.23; chapter 14's S04; chapter 23.
- **WCAG:** none of its own; it sets up 1.2.2, 1.2.3 and 1.2.5 for the next two rules.

#### 16.11 Caption every video, and have a person check every word.

- **Teaches:** closed and open captions, by platform, from the research lead's section B.
- **Terms at first use, from the W3C (research lead, section A):** captions, "synchronized visual and/or text alternative for both speech and non-speech audio information needed to understand the media content"; closed captions "can be turned on and off with some players"; open captions "cannot be turned off".
- **Rule, draft:** "Every video carries closed captions, made from the final script and checked word for word against the final cut by a person before it posts. Upload a caption file wherever a platform takes one: WebVTT on our own pages, WebVTT or SubRip on YouTube, SubRip on LinkedIn and X. On TikTok and Instagram, where we found no way to upload a file, turn on the app's own captions and correct every word before publishing. Treat any automatic caption as a first draft. Burn captions into the picture only where a platform offers neither, inside chapter 23's caption-safe area, and never on top of closed captions. Put a sound that matters, such as a gavel, in square brackets, and name a speaker who is off screen."
- **Why, draft:** WCAG 2.2 SC 1.2.2 quoted; then "Automatic captions mishear names and numbers, and a misheard number tells a viewer who cannot hear something false." YouTube's own help page says "You should always review automatic captions and edit any parts that haven't been properly transcribed."
- **Correct plate `s-16-11-correct`:** a 9:16 frame at 270 by 480 px. The picture area is a placeholder frame, "Placeholder: Dustin's voice over chart S04". Chapter 23's caption-safe area is outlined in a hairline; the caption sits inside it on two lines on a Charcoal band in Newsprint: "Citizens 18 to 24 reported voting / at 47.7 percent, down 3.7 points." Beside the frame, the matching WebVTT excerpt in a code block:

  ```
  WEBVTT

  00:00:08.000 --> 00:00:11.500
  Citizens 18 to 24 reported voting
  at 47.7 percent, down 3.7 points.
  ```

- **Failure plate `s-16-11-failure`:** the same frame with an unchecked automatic caption: "Citizens 18 to 24 reported voting / at 47.7 percent, down 37 points." The Illustrative label sits beside the misheard line. Draft failure caption: "Fails Rule 16.11. Nobody checked the automatic caption, so a fall of 3.7 points reads as 37."
- **Specifications:**
  - Closed captions: on every video.
  - Files: WebVTT (`.vtt`) on our pages; YouTube takes `.vtt`, `.srt` and others (read); LinkedIn takes `.srt` on desktop (read); X takes `.srt` (its help page seen through a search result).
  - TikTok and Instagram: the app's own captions, corrected word for word; no caption file upload found on either (November 21, 2026; TikTok from a search result, Instagram from a search result).
  - Automatic captions: a first draft only.
  - Burned-in captions: only where a platform offers neither, inside chapter 23's caption-safe area, never doubled.
  - Lines: two at most, about 42 characters each, broken at a phrase (design judgment).
  - Type: Inter 600 in Newsprint on a Charcoal band, 13.29 to 1; chapter 23 sets the size for each frame.
  - Sounds: in square brackets when they carry meaning. Speakers: named when off screen.
  - Checked by: a person, against the final cut, before posting.
  - Live: a live stream needs live captions (SC 1.2.4); none streams today.
- **Basis:** WCAG 2.2 SC 1.2.2; the platforms' help pages (sources list).
- **Tokens:** `oa.color.surface.charcoal`, `oa.color.text.primary.onCharcoal`, `oa.color.border.hairline`, `oa.type.label`.
- **Related:** chapter 23; Rule 19.1.
- **WCAG:** 1.2.2 Captions (Prerecorded) (A); 1.2.4 Captions (Live) (AA) stays "none today"; 1.4.3 for burned-in captions.

#### 16.12 Say aloud what the screen shows, and publish a transcript with every video.

- **Teaches:** audio description built into the script, and the transcript.
- **Terms at first use:** audio description, a spoken account of what the picture shows; the transcript, which the W3C calls an "alternative for time-based media", a "document including correctly sequenced text descriptions of time-based visual and auditory information" (research lead, section A).
- **Rule, draft:** "Write the script so the soundtrack carries every fact the picture shows: read each figure and what it measures, say whose source it is, and name what a gesture points at. A viewer who cannot see the screen then misses nothing. Where the picture shows something there is no time to say, make a described version too. Publish a transcript on the video's page and link it from every post: every word spoken, who speaks, the sounds that matter and what the screen shows that the words leave out, in order, corrected to the final cut. Link each chart in the transcript to its table."
- **Why, draft:** WCAG 2.2 SC 1.2.5 quoted: "Audio description is provided for all prerecorded video content in synchronized media." Then: "A voice that reads each chart aloud describes it as it goes, which serves a viewer who cannot see the screen and one who has the sound on and is looking away." **Marked gap:** the W3C's "Understanding SC 1.2.5" page has words on video whose soundtrack already carries what the picture shows. The research lead has not read it today. Until it is quoted, the Why rests on 1.2.5's own text and the W3C definitions, and the design director leaves a named field `why_understanding_quote` empty for the editor.
- **Correct plate `s-16-12-correct`:** a script excerpt as a two-column table, "On screen" and "Said", then a transcript excerpt.
  - Row 1. On screen: "Chart S04: a dot for 2020 and one for 2024 in each age group; citizens 18 to 24 at the left." Said: "Citizens 18 to 24 reported voting at 47.7 percent in 2024, down 3.7 points from 2020, in the Census Bureau's survey."
  - Row 2. On screen: "The gap between the youngest and oldest groups, marked." Said: "The gap between the youngest and the oldest grew from 23 points to 27."
  - Row 3. On screen: "S04's source line." Said: "These are answers to a Census survey, which run higher than counted ballots."
  - Transcript excerpt: "[0:08] Dustin Cathcart: Citizens 18 to 24 reported voting at 47.7 percent in 2024 … [On screen: a dot chart of reported voting by age group, 2020 and 2024, with its source line.]" and a link, "The chart's table", to S04's table in chapter 14.
- **Failure plate `s-16-12-failure`:** the same two columns. On screen: the same chart. Said: "As you can see, young people dropped off right here." The Illustrative label beside the line. Draft failure caption: "Fails Rule 16.12. The voice points at the chart and reads none of it, so a listener hears that something dropped and never learns by how much or in which survey."
- **Specifications:** Script: every figure, its measure and its source said while it shows; gestures named. Described version: where the picture outruns the voice. Transcript: on the video's page, linked from every post; speakers, sounds that matter and what is shown, in order; corrected to the final cut. Charts: linked to their tables. A clip with sound only: a transcript (SC 1.2.1). A clip with no sound: a transcript or a voice track (SC 1.2.1).
- **Basis:** WCAG 2.2 SC 1.2.1, 1.2.3 and 1.2.5; the W3C's definition of an alternative for time-based media.
- **Tokens:** `oa.type.body.small`, `oa.type.label`, `oa.color.border.hairline`.
- **Related:** chapter 14 (S04 and its table); Rules 18.23, 19.2.
- **WCAG:** 1.2.1 Audio-only and Video-only (Prerecorded) (A); 1.2.3 Audio Description or Media Alternative (Prerecorded) (A); 1.2.5 Audio Description (Prerecorded) (AA).

#### 16.13 Where a video sits, show its poster, summary and transcript, and play it only when a reader presses Play.

- **Teaches:** the embed's fallback and no autoplay, joined into one card.
- **Rule, draft:** "On our pages a video sits in a card: its poster frame, its title as live text, its length, one sentence with what it finds, a Play button, a link to the transcript and a link to watch it on the platform. The platform's player loads only when a reader presses Play, and the video never plays by itself, with sound or without it. If the player cannot load, because a reader is offline, blocks the platform or runs no scripts, the card still gives the finding in its summary and the whole video in its transcript."
- **Why, draft:** "A card that stands on its own serves every reader the player fails, and it keeps the platform's player off the page until a reader asks for it. Sound that starts by itself talks over a screen reader."
- **Correct plate `s-16-13-correct`:** the card at true size, 540 px wide. Poster at 16:9: a Charcoal frame with the question in Newsprint type and L8 at the top right corner, 24 px in (Rule 12.3); it stands in for chapter 23's title frame. Under it: the title "Which age groups reported voting in 2024?" with the Illustrative label beside it, since the video is not made; the length "1:05"; the summary "Citizens 18 to 24 reported voting at 47.7 percent in 2024, down 3.7 points from 2020, in the Census Bureau's survey."; a Play button (chapter 18's secondary button with the utility play icon, 44 px tall); and two links, "Read the transcript" and "Watch on YouTube". In the guide nothing can load, so the card sits in an image stage with its controls drawn and a plate alt that says what it shows; the design director confirms the stage pattern.
- **Failure plate `s-16-13-failure`:** an empty 16:9 Charcoal box with "Video unavailable" in small gray type and nothing else around it. Draft failure caption: "Fails Rule 16.13. The player failed to load and the page offers nothing in its place, so a reader gets no finding, no transcript and no link."
- **Specifications:** Card: poster, title, length, summary, Play, transcript link, platform link. Poster: a frame from the video, usually its title frame (chapter 23), with alt text that gives its words (Rule 19.4). Player: loads only on Play. Playback: never by itself, with or without sound (Rule 17.1). Captions: on at the start where the player allows (design judgment). If the player fails: the card stays whole. Controls: 44 px tall (`oa.size.target.touch`), each named by its words (Rule 19.3). Email: a still and a link, no player (chapter 22).
- **Basis:** Master Brief section 16; WCAG 2.2 SC 1.4.2 and SC 2.2.2; Rules 17.1 and 17.3.
- **Tokens:** `oa.size.target.touch`, `oa.color.surface.charcoal`, `oa.color.text.primary.onCharcoal`, `oa.type.h4`, `oa.type.body.small`, `oa.type.label`.
- **Related:** Rules 17.1, 17.3, 19.3, 19.4; chapters 18, 20, 22 and 23.
- **WCAG:** 1.4.2 Audio Control (A); 2.2.2 Pause, Stop, Hide (A); 2.1.1 Keyboard (A); 4.1.2 Name, Role, Value (A); 1.1.1 for the poster.

## 5. WCAG 2.2 criteria the chapter meets

Criteria text: the research lead's section A, read from the W3C on November 21, 2026.

| Criterion | Level | Rules | Note for chapter 19's map |
|---|---|---|---|
| 1.1.1 Non-text Content | A | 16.7, 16.8, 16.9, 16.13 | Already met through Rule 19.2; chapter 16 adds photographs and crops |
| 1.2.1 Audio-only and Video-only (Prerecorded) | A | 16.12 | Gap today; moves to met, with chapter 23 also owing it |
| 1.2.2 Captions (Prerecorded) | A | 16.11 | Gap today; moves to met, with chapter 23 also owing it |
| 1.2.3 Audio Description or Media Alternative (Prerecorded) | A | 16.12 | Gap today; moves to met, with chapter 23 also owing it |
| 1.2.4 Captions (Live) | AA | 16.11 states it | Stays "none today": nothing streams live |
| 1.2.5 Audio Description (Prerecorded) | AA | 16.12 | Gap today; moves to met, with chapter 23 also owing it |
| 1.3.1 Info and Relationships | A | 16.8 | Already met elsewhere |
| 1.4.1 Use of Color | A | 16.2 | Already met elsewhere |
| 1.4.2 Audio Control | A | 16.13 | Stays "none": no sound plays by itself, and Rule 16.13 now says so for video |
| 1.4.3 Contrast (Minimum) | AA | 16.4, 16.11 | Already met elsewhere |
| 1.4.5 Images of Text | AA | 16.4 | Already met through Rule 19.4 |
| 2.1.1, 2.2.2, 4.1.2 | A | 16.13 | Already met elsewhere |

## 6. Plates and bytes

Allocation 300,000 bytes (Gate 3 report, section 9). Under contract C1 the photographs weigh as a part of the page of their own, outside every chapter, and each use costs only its `<img>` tag, about 150 bytes with its alt. Estimates below come from built chapters: chapter 12's plates average 5,489 bytes, chapter 13's 3,662, and each built rule's own text, frame and links come to about 10,000 bytes (chapter 12: 196,047 bytes for nine rules with 104,292 of plates; chapter 13: 243,178 for thirteen with 117,198 of plates).

| Plate | What it holds | Photograph uses | Estimate, bytes |
|---|---|---|---|
| s-16-opener | Two photographs and captions | 2 | 5,000 |
| s-16-1-correct | Shot list table, 12 rows | 0 | 9,000 |
| s-16-1-failure | Rotunda walls crop | 1 | 4,000 |
| s-16-2-correct | Rotunda in black and white; color-evidence placeholder | 1 | 6,000 |
| s-16-2-failure | Meeting with Prussian tint | 1 | 4,500 |
| s-16-3-correct | Four crops with labels | 4 | 7,000 |
| s-16-3-failure | Crop without the official | 1 | 4,500 |
| s-16-4-correct | Article opener | 1 | 5,000 |
| s-16-4-failure | Headline on the picture | 1 | 5,000 |
| s-16-5-correct | Keyed caption and thumbnail | 1 | 6,000 |
| s-16-5-failure | Invented caption | 1 | 4,500 |
| s-16-6-correct | Markers, key and record | 1 | 8,000 |
| s-16-6-failure | Placeholder, caption, record | 0 | 6,000 |
| s-16-7-correct | Two crops with alt lines | 2 | 6,000 |
| s-16-7-failure | Tight crop, wrong alt | 1 | 4,500 |
| s-16-8-correct | Two placeholder frames | 0 | 6,000 |
| s-16-8-failure | Fifth edition's panel | 0 | 3,500 |
| s-16-9-correct | Generated-image placeholder, tab, prompt | 0 | 6,000 |
| s-16-9-failure | Generated picture passed off as news | 0 | 4,500 |
| s-16-picture-kinds | Five-row table | 0 | 7,000 |
| s-16-10-correct | Six-frame storyboard | 0 | 9,000 |
| s-16-10-failure | Storyboard with a late question | 0 | 6,000 |
| s-16-11-correct | 9:16 frame and caption file | 0 | 7,000 |
| s-16-11-failure | Misheard caption | 0 | 5,000 |
| s-16-12-correct | Script table and transcript | 0 | 7,000 |
| s-16-12-failure | Voice that reads nothing | 0 | 4,000 |
| s-16-13-correct | Video card | 0 | 7,000 |
| s-16-13-failure | Empty player | 0 | 3,500 |
| **Plates** | 28 | 18 uses | **160,500** |
| Rule text, specifications and frames | 13 rules at about 10,000 | | 130,000 |
| Chapter head, groups, related chapters, sources | | | 8,000 |
| **Chapter 16** | | | **about 298,500** |

The estimate sits at the allocation. Nothing is cut to meet it; the page's 16 MB is the one stop (DR-271). The design director reports the built figure.

## 7. Related chapters and sources

**Related chapters, draft reasons:** 01 Purpose (Rules 01.6 and 01.8, the rotation log); 02 Voice (Rule 02.9, house rules H03 to H05); 03 Identity (a logo over a photograph, Rule 03.3); 05 Color (the red rule, Rule 05.3); 12 Graphic devices (L8 in a video's corner, the exploded view); 13 Evidence and sourcing (the Illustrative label, source lines); 14 Data visualization (chart S04 and its table); 17 Motion and states (no autoplay, the player); 18 Components (buttons, the word placeholder in forms); 19 Accessibility (alt text, the WCAG map); 20 Web (the article photograph, share preview, the video card); 22 Newsletter and email (a video as a still and a link); 23 Social and video (crops, title and end frames, caption-safe areas).

**Sources, each with its status from the research lead's notes:**
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", W3C Recommendation, December 12, 2024, success criteria 1.1.1, 1.2.1 to 1.2.5, 1.4.2, 1.4.3, 1.4.5, 2.2.2, and the definitions of captions and alternative for time-based media; read November 21, 2026.
- Society of Professional Journalists, Code of Ethics, revised October 4, 2026; read November 21, 2026. The NPPA's code page drew its text by script and could not be read; no copy from another site is quoted.
- Reporters Committee for Freedom of the Press, "Reporter's Recording Guide"; read November 21, 2026.
- YouTube Help: pages 2734796, 2734698, 6373554 (captions) and 14328491 (disclosing generated content); read.
- LinkedIn Help: a552177 and a1327025 (captions), a6282984 (Content Credentials); read.
- X Help: "Upload caption (.srt) file" and "Manipulated media"; search result.
- TikTok: newsroom, "Auto captions on TikTok" (search result); Community Guidelines, "Edited Media and AI-Generated Content", effective September 24, 2026 (read).
- Meta newsroom, "Our Approach to Labeling AI-Generated Content and Manipulated Media", April 5, 2024, with its July 1 and September 12, 2024 updates (read); Instagram Help on captions and AI labels (search result).
- Wikimedia Commons file pages for the two photographs, license boxes read November 21, 2026; the sidecars in `work/build/assets/photography/`; rights rows pho-01, pho-01r, pho-04, pho-04r.
- U.S. Census Bureau, Current Population Survey Voting and Registration Supplement, through chart S04's source line, for the video example.

## 8. What chapter 16 hands to chapter 23

- Title and end frames at 1920 x 1080 and 1080 x 1920, each with its caption-safe area: the title frame holds the video's one question; the end frame holds the step, then where to read more. Brand strategy puts the tagline, "A country that answers to its people.", on a video's last frame; chapter 23 decides whether it sits on the end frame with the step. A web address joins only once the site is settled (DR-55).
- The name plate, "Dustin Cathcart, Founder and Editor" (DR-301): its place in the lower third, clear of each platform's buttons and of the caption band, and how long it stays.
- The caption band for burned-in captions and the size of Inter 600 for each frame (Rule 16.11), and where closed captions fall on each platform.
- L8 in each frame's corner, 24 px in (Rule 12.3), clear of each platform's buttons.
- The poster frame and thumbnail: a frame from the video, usually the title frame, at 16:9 for YouTube's 1280 x 720 and the platforms' cover sizes.
- The photograph crops for posts (Rule 16.3's table): 1:1, 4:5 and 1.91:1 from either photograph, in black and white, with words beside or on a solid panel (Rule 16.4) and the caption carried in the post's text and the image's alt text (Rule 19.4).
- Each platform's own AI label and where to turn it on (Rule 16.9's table), and the transcript link in every video post (Rule 16.12).
- The checks: captions and a transcript for every video frame set, alt text on every export, and no face inside a platform's button or crop zone (Gate 3 report, section 9).

## 9. What chapter 16 hands to chapter 20

- The article photograph: 3:2 in black and white, the caption under it with the credit (Rules 16.2 and 16.5), each use with its own alt text (Rule 16.7), and the headline beside it or on a solid panel (Rule 16.4). Under 240 px wide, no photograph.
- The share preview at 1200 x 630 from Rule 16.3's 1.91:1 crops, with its words set as Rule 16.4 sets them.
- The video card as a web component (Rule 16.13): the player loads only on Play, the card stays whole when it fails, and the transcript has a page of its own on the site.
- In the dark mode (DR-204): photographs unchanged, captions and placeholder frames in Charcoal's tokens.
- A page with no photograph runs without one; a placeholder never ships (Rule 16.8).

## 10. Open items

- **For Dustin, Phase 4 board 1:** chapter 01's two plates (Rules 01.6 and 01.8) show their photographs in color, and Gate 1's S10 (G1-03) sets black and white as the default. Chapter 16 follows S10, so the guide would show the same photographs two ways. The studio recommends chapter 01's three plates take the same `filter: grayscale(1)`, a CSS change with no new bytes. It changes approved chapter 01 on screen, so it waits for his named answer. Logged under "Not fixed" in my notes.
- **Gap, for the research lead:** the W3C's "Understanding Success Criterion 1.2.5" words on video whose soundtrack already describes what is shown (Rule 16.12's Why).
- **Optional facts:** a published caption standard for line length, if the editor wants a citation in place of "design judgment" (Rule 16.11); the official NPPA text, if it can be reached.
- **Q-04** (whether to commission photographs) stays open; placeholders hold every commissioned photograph's place.
