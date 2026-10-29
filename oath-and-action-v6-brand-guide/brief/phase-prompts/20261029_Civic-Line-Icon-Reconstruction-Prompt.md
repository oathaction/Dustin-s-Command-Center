# Civic Line icon reconstruction: Dustin's assignment

Dustin sent this assignment on October 29, 2026, with ten reference sheets. The sheets are saved in `work/research/chat-references/civic-line/`. The text below is his message, word for word. His answers to the studio's questions on the same day follow it, and they govern where they differ from the text.

## Dustin's answers, October 29, 2026

1. "i grant the exception. please trace. i want my logos to look exactly like these, but cleaner, more polished." (Decision DR-02.)
2. "clean them up as needed." (DR-03: one measured line weight across the set; true circles and straight lines where the drawing plainly means them; every feature, count, gap and red placement kept as drawn; each correction logged by ID.)
3. "use these new pillar marks." (DR-04: Explain, Track, Connect and Act from sheet 01 replace the Gate 1 pillar marks.)
4. "use approved edition 06" (DR-05: the contact sheets carry the approved Edition 06 wordmark master, not the wordmark drawn on the reference sheets.)
5. "yes civic line is the winner. please proceed." (DR-01.)

## The assignment, verbatim

Let’s keep it focused just on icons for now. Once we finalize those, we’ll move to the visual design system for the atlas / systems mapping, then your other outstanding questions before proceeding with the rest of the oath and action brand update. Also let me know when it makes sense to start a new chat or clear context to keep this efficient. Prompt:

Your assignment

Reconstruct the attached Oath & Action Civic Line icon collection as a complete, reusable asset set. Reproduce all 122 approved designs in red-black and black, for 244 icon variants. Treat this as restoration and vector tracing of existing artwork. The attached final sheets define the approved appearance.

Spend your effort inspecting the references, measuring shapes, tracing paths, comparing renders and correcting discrepancies. Preserve the silhouettes, proportions, internal gaps, curve shapes, open contour ends, relative component placement, line weights and red accent locations. Complete the full collection.

Use the final five-sheet catalogue described below. Earlier 16-icon or 36-icon explorations, atlas UI screenshots, Y2K studies and duotone concepts belong to different sets. If those are also attached, identify the final catalogue by its headers and row contents.

The written descriptions identify the exact drawing and explain what to inspect. When an approximate description or suggested construction differs from a visible reference detail, the matching reference image controls. Inspect that detail at enlarged scale and reproduce it. Retain the drawing’s actual visual shorthand even when a different metaphor would communicate the subject more literally.

Exact raster identity comes from retaining the original source pixels. A vector reconstruction is a measured match with different rasterisation. Keep these claims separate: preserve original reference crops when tools permit, and describe the SVGs as traced reconstructions unless an actual comparison establishes an exact match. Report measured differences honestly.

Reference manifest and reading order

Identify sheets by the header and icon sequence, even if their uploaded filenames differ.

|Sheet|Header                              |Grid              |Count|First / last icons                            |
|-----|------------------------------------|------------------|----:|----------------------------------------------|
|01   |Participation & Accountability      |6 columns × 4 rows|24   |Voting / Feedback Loop                        |
|02   |Government, Information & Technology|6 columns × 4 rows|24   |Congress / Public Records                     |
|03   |Economy & Public Issues             |6 columns × 4 rows|24   |Wealth Concentration / Reform                 |
|04   |Reforms R-01–R-25                   |5 columns × 5 rows|25   |All-Party Primaries / Child Tax Credit        |
|05   |Reforms R-26–R-50                   |5 columns × 5 rows|25   |Automatic Recession Aid / Popular-Vote Options|

Read rows left to right, starting at the top. The first three sheets use IDs CL-001 through CL-072, assigned below. Retain the actual R-01 through R-50 IDs for the two reform sheets.

Suggested reference filenames, if the attachments have been renamed:

1. 20261029_Oath-And-Action-Civic-Line-01-Participation-Red.png
2. 20261029_Oath-And-Action-Civic-Line-01-Participation-Black.png
3. 20261029_Oath-And-Action-Civic-Line-02-Government-Tech-Red.png
4. 20261029_Oath-And-Action-Civic-Line-02-Government-Tech-Black.png
5. 20261029_Oath-And-Action-Civic-Line-03-Economy-Issues-Red.png
6. 20261029_Oath-And-Action-Civic-Line-03-Economy-Issues-Black.png
7. 20261029_Oath-And-Action-Civic-Line-04-Reforms-01-25-Red.png
8. 20261029_Oath-And-Action-Civic-Line-04-Reforms-01-25-Black.png
9. 20261029_Oath-And-Action-Civic-Line-05-Reforms-26-50-Red.png
10. 20261029_Oath-And-Action-Civic-Line-05-Reforms-26-50-Black.png

Construction rules for the entire collection

Source tracing and scale

Use image inspection and code or vector tools to reconstruct the drawings. Build real SVG path, line, circle, ellipse and polygon geometry. Trace each reference icon individually. A catalogue label alone is insufficient to select a replacement from an icon package.

Make source crops that contain only each pictogram, excluding its caption, reform ID, neighbouring icons and sheet header. Preserve each untouched source crop as a comparison reference when local image tools are available. Record its sheet, row, column and source-pixel crop rectangle.

Use a common square SVG viewBox, preferably 0 0 128 128. This is an export container, not a new design grid that overrides the reference. Transfer the source’s aspect ratio and placement into that space without stretching. Preserve intentional differences between tall, wide and compact symbols. Provide consistent clear space while keeping the original silhouette proportions.

Measure the stroke width from the source. Approximately 3 to 4 units in a 128-unit viewBox is a starting estimate, not an approved measurement. Match the apparent weight, including small interior strokes. Keep round line caps and softly rounded joins where the source shows them. Architectural corners, page corners, parcel edges and diagram nodes retain their particular shapes. Follow the source’s open contours and small breaks.

The catalogue mixes outlines with a few deliberate filled elements: coin tops, selected cells, doors, accent sectors, solid people dots, restriction discs and similar details. Retain each fill exactly where shown. Keep negative-space cutouts open in standalone assets, including the X in R-35 and the person-shaped cutout in Labor Share.

Color editions

Clean vector color tokens:

• Charcoal: #121212.
• Pillar Red: #E63946.
• Catalogue background: Newsprint #DCD9D2.

The assets themselves have transparent backgrounds. Newsprint belongs to the preview/contact-sheet surface. Preserve the source’s background only in untouched raster comparison crops.

For every icon, construct one shared geometry definition. Assign its approved accent paths or fills to a separate color group. The red-black edition uses Charcoal for the main drawing and Pillar Red only on the parts specified in the catalogue. The black edition renders those same accent paths and fills in Charcoal. An element that is red in one edition remains present in the black edition.

Use the black sheet to inspect the complete silhouette and the red sheet to locate the accent mask. Tiny raster differences between the two references can exist. Resolve these by inspecting both at high magnification; retain the clearly intended shape and record any consequential judgement. Keep both exported editions geometrically identical. Avoid independently generating or redrawing the black edition.

Source raster colors can vary slightly through antialiasing or export. The clean SVGs use the specified brand tokens. Retained untouched raster crops preserve the source pixels. Document this distinction in the handoff.

Preserve the approved drawing choices

Keep the actual detail counts visible in the source: heads, seats, windows, coin-stack bands, page rules, chip pins, arrowheads and dots. Count these in the enlarged attachment. The written catalogue calls out their arrangement; the image resolves any ambiguous count.

Symbols that share a topic can still be distinct drawings. Congress and Congressional Capacity differ. Public Investment in Sheet 03 and R-36 differ. Local Reporting and Local-News Funding differ. Registration and Automatic Registration have their own reference cells. Trace these separately.

Retain source-specific visual quirks, including the shield in Paid Leave, the chair within the district-like Safe Seats outline, the open lock in Filibuster Reform, the family composition in Child Tax Credit and the simple robot face in Workplace AI. These are part of this approved set.

Letters, numerals and symbols that form part of the drawing must match: the preference numbers in R-02; the AI lettering in R-40; dollar, percent, exclamation and hashtag marks; the prohibition slashes and rejection X. Captions and reform IDs are separate typography.

Captions and contact sheets

Keep asset SVGs free of captions and wordmarks. Reproduce the five labelled contact-sheet layouts in both color editions separately. Use the exact catalogue names, ordering and reform identifiers. Match the source’s Inter-style labels, title placement, rule, wordmark scale and spacing as closely as the supplied references allow.

The source sheets use a horizontal OATH & ACTION wordmark at upper left. The words are bold sans serif; the ampersand is a contrasting italic serif and red in the red-black sheets, black in the black sheets. Treat this only as the supplied reference wordmark. Avoid introducing a new logo design.

R-35 must remain labelled “Term Limits · Rejected” in previews, filenames/metadata where appropriate and the inventory. Its presence records a rejected option in the atlas.

Required workflow and deliverables

1. Inspect all ten references and build the 122-row inventory before tracing. Confirm the five sheet counts: 24, 24, 24, 25, 25.
2. Trace each pictogram with its black geometry and accent mask. Work through every row. Check distinctive silhouettes before reusing any primitive.
3. Export the 244 SVGs from those shared definitions. Also render transparent PNGs at 256 and 512 pixels if the tools support them. Keep a source-faithful crop set when image tools are available.
4. Render all ten contact sheets and a searchable visual catalogue. Give the catalogue a color-edition toggle and an ID/name search if an HTML preview can be produced.
5. Compare each traced icon with its source crop at a shared scale. Use an opacity overlay, alternating display and an edge-difference view when tools permit. Correct contour shifts, wrong gaps, incorrect layering, missing detail and misplaced accents. Inspect output at 24, 32, 64, 128 and 256 pixels without changing the approved master geometry.
6. Check exact membership and counts. Each of the 122 IDs needs one red-black SVG and one black SVG. Confirm that the black versions contain no red color tokens and that edition pairs share identical geometry. Validate the SVGs and check for clipped strokes, unwanted background rectangles, broken paths or missing negative spaces.
7. Deliver the complete asset package, inventory, preview and a concise fidelity report. Report unresolved mismatches by ID with the affected feature. Claim only checks that were actually run.

For comparisons, align the traced render with its own source crop using translation and uniform scale. Preserve aspect ratio and use no elastic warping. Inspect at original source scale as well as enlarged scale. Compare the silhouette mask, internal negative spaces, stroke-centre locations and red accent mask separately. When numerical comparison tools are available, report foreground-mask intersection-over-union and edge-distance statistics per icon; retain the actual measurements. Treat approximately one source pixel as a useful initial tracing tolerance, then tighten the fit where the raster edge allows it. A numerical threshold alone does not establish visual identity. Review distinctive corners, intersections, endpoint gaps and the small features called out in each entry.

Verify edition identity programmatically: after replacing the red token with Charcoal, each paired SVG should have the same path coordinates, transforms, clipping geometry and fill/stroke assignments. Preserve deliberate negative-space cuts when converting a red fill to black. Keep metric results and visual inspection status separate in the fidelity report.

Preserve work in files as you proceed. Continue through the full set without pausing for approval of small batches. If a tool limitation prevents an export or comparison, finish the accessible work and state that limitation precisely. Retain a completion ledger so an interrupted run resumes from the remaining IDs.

Filename convention: use the actual creation date as YYYYMMDD, one underscore, Title-Case words separated by hyphens, and lowercase extensions. Example:

20261029_Oath-And-Action-Civic-Line-CL-001-Voting-Red-Black.svg
20261029_Oath-And-Action-Civic-Line-CL-001-Voting-Black.svg
20261029_Oath-And-Action-Civic-Line-R-30-By-Right-Housing-Red-Black.svg

Folders use lowercase kebab-case, such as red-black/, black/, png-256/, png-512/, contact-sheets/, reference-crops/ and qa/. Source-code files can use normal language conventions. Use a dated filename for the inventory, preview and final package. Include an inventory with ID, label, sheet, row, column, variant filenames, accent description, reference crop and verification status.

The complete 122-icon drawing catalogue

“Red” below identifies every colored portion of the approved red-black drawing. The corresponding black edition preserves each listed portion and changes its color to Charcoal. Positions are relative to that icon’s own drawing, with x increasing rightward and y increasing downward.

Sheet 01: Participation & Accountability

CL-001 · Voting · Row 1, column 1

Construction: a wide ballot box with a rectangular front face and a shallow trapezoidal lid. Its front corners are nearly square with rounded stroke joins. A short horizontal slot sits in the lid. A long rectangular ballot rises diagonally up-right from that slot; its long edges lean from lower left to upper right. Preserve the small open separation where the ballot and the right lid contour approach. The box has no lettering or checkmark.

Red: the ballot’s upper short edge and its upper-right/right-facing edge segment. The box, slot and remaining ballot contour stay black. Preserve the angular lid and slanted blank ballot.

CL-002 · Representation · Row 1, column 2

Construction: three frontal, faceless outline people. A larger central circular head sits above a shallow shoulder arc and a prominent tapered lectern. The lectern has a wide flat top, narrows toward its lower part and ends at a short baseline. Smaller people stand left and right with circular heads and open-bottom rounded shoulder shapes. Central head, lectern and side people share a clear vertical symmetry.

Red: only the central head’s circular outline. Keep the centre head hollow. Preserve the lectern’s taper and the side people’s lower height.

CL-003 · Registration · Row 1, column 3

Construction: a horizontal ID card with softly rounded corners. Left half: small outline circular head over an open shoulder/torso outline. Right half: three short horizontal information rules at staggered lengths. The card contour opens or is visually occluded at lower right by a circular verification badge extending outside the card. Put a simple check inside that badge.

Red: the exterior verification circle and its checkmark. The ID portrait, card perimeter and information rules remain black. Maintain the badge’s overlap and the generous blank areas within the ID.

CL-004 · Petition · Row 1, column 4

Construction: an upright document with four horizontal rules and a largely open right side where a writing pen overlaps it. The pen runs diagonally from lower left to upper right, with a long narrow barrel, rounded upper end, parallel inner line/clip detail and a pointed lower nib. Its tip falls near the document’s lower-right interior. Preserve the separate narrow black pen-clip stroke.

Red: the pen’s long outer barrel contour and upper rounded end as shown. Its nib and small clip/detail retain black. The document and text rules are black.

CL-005 · Public Meeting · Row 1, column 5

Construction: a tall central speaker behind a rectangular lectern, with a small circular head above rounded shoulders. A simple outlined circular emblem appears on the lectern front. Two shorter audience members stand in front, one left and one right, each drawn with a hollow head and open-bottom shoulders. The arrangement forms a compact pyramid of people.

Red: the central speaker’s head outline. Keep the lectern emblem black and hollow. Match the audience overlap with the lectern rather than separating everyone into independent columns.

CL-006 · Civic Ties · Row 1, column 6

Construction: three outline people in a triangular arrangement, one high at centre and two lower at left and right. Each has a hollow circular head and an open-bottom shoulder arch. Three separate curved links suggest an enclosing triangle/circle: upper-left arc, upper-right arc and a shallow smile-shaped arc between the lower people. Leave clear gaps between the arcs and the figures.

Red: all three curved connecting arcs. People remain black. The connectors are open arcs, not a continuous circle or arrow loop.

CL-007 · Turnout Equality · Row 2, column 1

Construction: three matching frontal person-and-ballot combinations in a horizontal row. Each hollow circular head sits over a short rounded shoulder arc. In front of each torso is the same rectangular ballot/card, with one short horizontal mark around its upper-middle area. Card top edges align and all three people are equal in height.

Red: the three short horizontal marks, one inside each card. Every card outline and figure contour stays black. Preserve equal proportions across the row.

CL-008 · Political Hostility · Row 2, column 2

Construction: two opposed rounded rectangular speech bubbles, left and right. Their tails descend toward the outer lower corners: the left tail points down-left and the right tail down-right. Their inward-facing contours remain open around a central lightning-bolt stroke. The bolt leans diagonally and separates the bubbles. Preserve the bubbles’ near-mirror arrangement and the negative space around the bolt.

Red: the central lightning bolt only. The speech-bubble outlines are black. Keep both bubbles blank and retain the inward gap.

CL-009 · Safe Seats · Row 2, column 3

Construction: an irregular, approximately square district boundary made of orthogonal stair-step contours. Inside it is a small office/legislative chair: tall rounded-rectangle back, short arm supports, a seat baseline and two short downward supports. The chair occupies the central lower portion of the district shape. Preserve the distinctive stepped perimeter.

Red: the filled lower part of the chair’s back/seat area visible inside its black outline. The district and chair framing remain black. This is the chair-within-a-district drawing shown in the source.

CL-010 · Decisive Primaries · Row 2, column 4

Construction: three small hollow circular inputs vertically aligned at left. Each has a rightward path with rounded orthogonal bends; these paths converge into one narrow central outlet. A single short rightward arrow emerges from that outlet and points toward a larger hollow output circle at right. The top path descends and bottom path ascends into the merger.

Red: the larger right-hand output circle. Preserve the three black inputs, the three-to-one route geometry and the separate black arrowhead before the output circle.

CL-011 · Electoral Pressure · Row 2, column 5

Construction: on the left, a person with hollow head and rounded shoulders sits behind a narrow desk/lectern. The desk has a horizontal surface and two vertical supports. On the right is a small ballot box with trapezoidal lid and a slanted blank ballot. A horizontal arrow above the space between them points right, from the officeholder toward the ballot box.

Red: that right-pointing arrow. Keep the officeholder, desk, ballot box and ballot black. Preserve the two subjects’ separate baselines and the arrow’s elevated placement.

CL-012 · Election Rules · Row 2, column 6

Construction: upright rounded rectangular page. Two horizontal text rules occupy the upper part. Two adjustment rails occupy the lower part; each has a small hollow circular knob. Upper rail’s knob lies right of centre; lower rail’s knob lies left of centre. Both rails extend visibly past their knobs.

Red: the upper adjustment rail and its circular knob. The page, text rules and lower slider remain black. Preserve the sliders’ opposite knob offsets.

CL-013 · Incumbent Defeat · Row 3, column 1

Construction: a vacant office chair at left, with tall rounded back, wide seat and short armrests. One central stem descends to a horizontal foot with short downward tips. To its right, at seat/back mid-height, is a detached horizontal arrow pointing right. Preserve the open gap between chair and arrow.

Red: the detached right-pointing arrow. Keep the chair entirely black and empty. The source uses a chair rather than an illustrated departing person.

CL-014 · Entrenched Power · Row 3, column 2

Construction: a compact domed legislative building enclosed by an elliptical foreground fence. The central building has a cupola, dome, cornice and vertical façade divisions. The fence has an upper ellipse-like rail, a lower curved rail and repeated narrow vertical pickets; foreground pickets overlap the building’s lower area. A central tall doorway remains visible.

Red: the central doorway outline/fill treatment shown in the source. Dome and fence stay black. Preserve the fence wrapping around the building and count its pickets from the crop.

CL-015 · Political Money · Row 3, column 3

Construction: a large outlined coin with a dollar sign at left. To its right is a ballot box with shallow trapezoid lid and slanted blank ballot. An orthogonal, rounded-corner connector rises from the coin’s right edge, travels across and enters the ballot area. The connector is a plain path without a separate arrowhead.

Red: the dollar sign, the raised connecting path and the ballot’s upper/right accent edge. Retain their particular separate red portions. Coin and box framing remain black.

CL-016 · Lobbying · Row 3, column 4

Construction: two equal-size hollow-headed people face each other across a narrow rectangular table. Each has a rounded shoulder outline and an inward-bending forearm. A small low trapezoidal document/meeting object lies on the table between their hands. The table surface is a long horizontal bar with two downward legs.

Red: the small central object/short trapezoidal stroke on the tabletop. People and table stay black. Keep the paired forearms above the table and the open central space.

CL-017 · Policy Favoritism · Row 3, column 5

Construction: an upright document on the left with three horizontal rules. Three separate short elbow-like routes extend from its right toward three small person busts stacked vertically on the right. Each bust has a circular hollow head and an open-bottom curved shoulder shape. The middle bust and its route form the focal access channel.

Red: the middle person’s head/shoulder strokes and the adjoining highlighted central access stroke as shown. Top and bottom people, page and remaining routes are black. Trace each branch rather than merging them.

CL-018 · Earned Trust · Row 3, column 6

Construction: three hollow-headed people arranged with one taller central person and two shorter side figures. A large circular verification badge overlaps the front of the central lower torso. The circle is black and encloses a simple angled check. Side shoulder arches remain open at their bottoms.

Red: only the checkmark within the central black circle. Keep the three people and circular border black. Preserve the badge’s frontmost layering.

CL-019 · Explain · Row 4, column 1

Construction: a large open book with two curved page blocks, a central vertical spine and a second outer lower cover contour. Its upper page edges bow gently upward toward the outside and meet in a central valley. Three short rays rise above the central valley: one vertical and two diagonal.

Red: the three rays above the book. Book contours remain black. Preserve the hollow page areas, doubled lower edge and the absence of page text.

CL-020 · Track · Row 4, column 2

Construction: an open, rounded S-shaped route starts near upper left, bends right, returns left through the middle and extends right along the lower section. A hollow pointed map pin floats above its upper-left start. A magnifier overlaps the route’s lower-right area, with a black circular lens and a narrow handle descending diagonally right.

Red: the map-pin outline and the magnifier handle. The route and lens circle stay black. Keep the pin hollow and the route free of dotted segments.

CL-021 · Connect · Row 4, column 3

Construction: two equal large hollow circles overlap horizontally, creating a narrow central lens-shaped intersection. Their centres share a baseline. Both loops retain their circular form and neither is a chain-link oblong. The overlap’s two curved boundary segments are the focal geometry.

Red: the inward-facing curved arc of each circle that forms the two sides of the central lens. The outer arcs are black. Preserve the overlap width and the open central negative space.

CL-022 · Act · Row 4, column 4

Construction: an outline hand seen frontally with a long upright index finger touching a round control. The other fingers fold down as small rounded knuckles on the right; a thumb branches diagonally left. A broad open-ended circular ring surrounds the index fingertip. Short rays extend upward-right/right from that ring.

Red: the control ring and its short action rays. The finger and hand contour remain black. Preserve the source’s bent thumb, knuckle count and open wrist.

CL-023 · Evidence · Row 4, column 5

Construction: an upright page with a partial open right edge and four short horizontal information rules. A large magnifier overlaps its lower-right portion. The lens contains a simple checkmark; its handle descends diagonally to lower right. Keep the page visually behind the lens.

Red: the checkmark inside the lens. Page, circular lens and handle remain black. This differs from Watchdogs, whose handle is the red part.

CL-024 · Feedback Loop · Row 4, column 6

Construction: two equal hollow square nodes lie horizontally apart. A broad upper curved arrow runs from above the left node toward the upper-right node; a lower curved arrow returns from below the right toward the lower-left node. Arrowheads terminate near their destination nodes without touching them.

Red: both curved arrows, including their open angled arrowheads. Square nodes remain black. Preserve clockwise circulation and the clear spaces between node corners and arrow ends.

Sheet 02: Government, Information & Technology

CL-025 · Congress · Row 1, column 1

Construction: a symmetrical domed legislative building. From top down: a short finial, small square cupola, rounded dome, two horizontal cornice lines, short upper supports, a central rectangular façade with repeated vertical divisions, low wings and outer vertical supports. The whole drawing is wider than it is tall. Keep the line gaps beneath the wings and the source’s exact column rhythm.

Red: one central vertical façade division/column. All other architectural strokes are black. The red accent is a single upright stroke, not a filled dome or a red group of columns.

CL-026 · Executive Power · Row 1, column 2

Construction: a frontal official behind a desk at left, with hollow circular head and rounded shoulders. A short rectangular paper lies flat on the desktop. A tall upright order/document overlaps the desk’s right side, containing two small horizontal rules and a signature-like zigzag near its bottom. Two legs descend from the broad horizontal desk.

Red: the official’s narrow filled necktie and the signature squiggle on the upright document. Preserve both separate accents. Keep the paper on the desk, the face-free head and the upright document’s overlap.

CL-027 · Court Alignment · Row 1, column 3

Construction: a large balance scale at left, with straight horizontal beam, central vertical stem, two triangular suspension shapes and two shallow curved pans. A short vertical mark rises above the beam’s centre. A small rounded baseline supports the central stem. Behind the right pan is a narrow upright legal document with two horizontal rules and a hollow round seal near its lower part.

Red: the hollow circular seal on the document. All scale components and page rules remain black. Retain the document behind the right side of the scales.

CL-028 · Watchdogs · Row 1, column 4

Construction: an upright record page with a partially open lower-right contour and three or four short horizontal rules. A large magnifier overlaps the page’s lower-right area. Its lens is an empty hollow circle; the handle extends diagonally down-right as a narrow rounded rectangle.

Red: the magnifier handle outline. Keep the lens empty and black. This drawing has no check inside the lens; its silhouette is distinct from Evidence and Watchdog Remedies.

CL-029 · Public Services · Row 1, column 5

Construction: an open service counter with a horizontal top, a rectangular front and a small block at its left end. A staff member appears behind it inside a three-sided rectangular service window. The staff figure has a hollow circular head and a curved shoulder arc. A larger visiting person’s hollow head and open torso stand outside at right.

Red: a short horizontal rule on the counter’s front, slightly right of centre. The people and window stay black. Preserve the counter/window/visitor depth order.

CL-030 · Reform Tests · Row 1, column 6

Construction: two small square test-result panels sit side by side near the top. The left contains one short vertical mark and two information rules; the right contains three ascending vertical bars. A short horizontal connector joins the panels. Curved branches descend from them and merge behind a circular verification badge below the gap.

Red: the left panel’s short vertical mark, the middle bar in the right panel and the check inside the lower badge. Badge circle and connectors remain black.

CL-031 · Local Government · Row 2, column 1

Construction: a compact symmetrical municipal hall. A triangular pediment tops the taller central block; low rectangular wings extend left and right. There are narrow upright window marks in the central block and wings. A horizontal baseline runs under the whole building. The centre has a tall round-topped doorway.

Red: the filled central doorway. All roof, wall, baseline and window strokes stay black. Preserve the central block’s greater height and the small gap under the roof peak.

CL-032 · Local Reporting · Row 2, column 2

Construction: a newspaper represented by a large rounded rectangular front sheet and a rolled/stacked return sheet visible down the left and along the bottom. The front page has several horizontal rules near the top and left. A solid rectangular article/image block occupies its lower-right quadrant.

Red: the lower-right filled article block. Keep page rules black. Trace this paper’s outer return curl and the source’s exact line lengths; avoid replacing it with the differently composed R-32 newspaper-and-coins drawing.

CL-033 · Hostile Content · Row 2, column 3

Construction: a laptop base with a large open screen above. A rounded speech bubble overlaps the screen’s upper-left area and contains a hashtag and exclamation mark. A triangular warning sign occupies the screen’s right side, with a separate vertical exclamation stroke and dot. The laptop base has a shallow centred notch.

Red: the hashtag/exclamation characters in the speech bubble, plus the warning triangle and its exclamation. Laptop and speech-bubble outlines remain black. Preserve the two overlapping message/warning regions.

CL-034 · New Technology · Row 2, column 4

Construction: a hollow lightbulb on the left, with round crown, tapered neck, short base and simple internal filament. From its lower-right region a thin elbow-like circuit wire travels right and upward to a hollow circular terminal. Several short rays sit above and to the upper sides of the bulb.

Red: the bulb’s external rays and the hollow circuit terminal. Bulb contour, filament, screw base and connecting wire stay black. Keep the bulb and terminal as one connected symbol.

CL-035 · Residential Sorting · Row 2, column 5

Construction: two clusters of overlapping pitched-roof homes, separated by a vertical dashed boundary. The left cluster has black roof/wall contours and short upright windows. The right contains taller black homes behind a smaller foreground home. Preserve the reference’s differing house positions and roof heights on the two sides.

Red: the small foreground home’s roof-and-wall outline in the right cluster. Boundary dashes and other homes remain black. Trace the visible house count and overlaps from the crop.

CL-036 · Cross-Border Capital · Row 2, column 6

Construction: one outlined three-dimensional parcel at upper left and a matching parcel at upper right, each with visible top and side edges and a short tape seam. Between and below them sits an outlined coin containing a dollar sign. A detached upper arrow points right across the central gap; a lower arrow points left.

Red: the upper right-pointing arrow and the coin’s dollar sign. Boxes, coin outline and returning lower arrow stay black. Preserve the diagonal parcel edges and vertically separated opposing arrows.

CL-037 · Foreign Interference · Row 3, column 1

Construction: an outlined globe at left, made from an outer circle, vertical curved meridians and horizontal latitude lines. Two outward-bowing signal arcs stand to its right. A small ballot box sits further right with a slanted ballot projecting upward. A triangular warning badge overlaps the box’s front/lower-right area.

Red: the signal arcs, upper accent edges of the slanted ballot, warning triangle and its exclamation. Globe and ballot-box body stay black. Preserve the warning badge in front of the box.

CL-038 · External Shocks · Row 3, column 2

Construction: a winding road-like route formed by two sweeping open curves. The route enters near upper right, sweeps left through the middle and bends back toward lower left. A short centre dash appears within its upper-middle channel. A sharp irregular impact burst interrupts the route on its lower-right side, beside a broken black route end.

Red: the angular impact burst. Road curves, centre dash and broken endpoint stay black. Preserve the source’s jagged burst and broad S-shaped route rather than substituting a generic lightning bolt.

CL-039 · Feed Ranking · Row 3, column 3

Construction: three compact horizontal rounded content cards stacked vertically with equal spacing. Each card contains a small square thumbnail at left and two short rules to the right. A thin vertical ranking rail stands detached on the far right, with a hollow circular knob around the height of the middle card.

Red: the middle card’s thumbnail outline and information rules, plus the circular rail knob. The middle card perimeter remains black. Keep the three cards separate and the right rail visible above and below its knob.

CL-040 · Platform Power · Row 3, column 4

Construction: a large hollow circle at the top contains a small filled central dot. A three-way organisational tree descends from it: branches angle toward left and right while one stem drops centrally. Three smaller outline people align below those branches, with equal head sizes and open-bottom shoulders.

Red: only the filled dot inside the top circle. All branches and people are black. Retain the empty ring around the dot and the hierarchy from one platform to three people.

CL-041 · Workplace AI · Row 3, column 5

Construction: a human worker on the left sits at a desk/laptop, with a hollow round head, shoulder contour and diagonal laptop screen. To the right stands a friendly small robot bust: rounded-square head, side ear tabs, two dark dot eyes, a short curved mouth, narrow neck and simple shoulder arch. Three short activation rays sit above the robot.

Red: those rays above the robot. Both figures and the laptop are black. Preserve the robot face and relative human/robot heights shown in the source.

CL-042 · AI Concentration · Row 3, column 6

Construction: three narrow upright server/document panels line up across the top. Each contains a small stack of horizontal rules. Three connecting paths descend and converge on a larger hollow circle below the middle panel. The outer branches angle inward; the middle branch is vertical. A dollar sign sits inside the lower circle.

Red: the dollar sign within the convergence circle. Keep all panels, rules, connectors and the circle border black. Match the top panels’ equal dimensions and fan-in geometry.

CL-043 · Digital Government · Row 4, column 1

Construction: a small municipal building forms the left/back layer, with triangular roof, central tall wall, low left wing, window marks and doorway. A landscape browser/service panel overlaps it at lower right. The panel has a top bar, small circular controls, horizontal content rules and a small lower-right rectangular interface element.

Red: that small filled rectangular interface element on the service panel. All architecture and browser framing remain black. Preserve the foreground panel obscuring part of the building.

CL-044 · Grid Demand · Row 4, column 2

Construction: three horizontal rounded server trays stack at left. Each tray contains short information/vent rules and a small round indicator near its right end. A large electrical plug stands at right with two upright pins, a rounded U-like body and a short cable descending from its base. A zigzag bolt lies inside the plug.

Red: the three server indicator dots and the bolt inside the plug. Main server outlines, plug and cable remain black. Retain all three separate server trays.

CL-045 · Pricing Algorithms · Row 4, column 3

Construction: two overlapping upright price tags lean or offset slightly, with clipped upper shoulders and small circular holes. The foreground tag contains a dollar sign. A small circuit-tree motif stands separately to the right: one vertical stem, short horizontal elbow/branch and several hollow circular terminals.

Red: the foreground dollar sign and the circuit tree’s upper terminal ring. Tag contours, holes and other circuit nodes remain black. Preserve the asymmetric two-tags-plus-circuit composition.

CL-046 · AI Infrastructure · Row 4, column 4

Construction: three stacked rounded server trays occupy the left. Each has a short information rule and a small indicator at right. On the right is a square microchip, with a small central square and short pins projecting from its edges. The chip and server stack share a similar visual height.

Red: all three small server indicator dots and the chip’s inner square outline. Chip body, pins and server framing remain black. Count pins from the reference rather than using a generic chip.

CL-047 · Data Rights · Row 4, column 5

Construction: an upright page with a partial open right edge and three or four horizontal information rules in its upper/left area. A large key overlaps its lower-right portion. The key has a hollow circular bow, a vertical stem dropping below it and two short teeth pointing right near the stem’s lower end.

Red: the entire key outline/stem/teeth. Page and information rules stay black. The key bow remains hollow and the stem is vertical.

CL-048 · Public Records · Row 4, column 6

Construction: an open rectangular file folder forms the foreground, with a raised shoulder/tab on its left edge and a tall rear edge at right. A single upright rounded document projects above the folder. It contains a longer top rule followed by several shorter black rules. Folder front occludes the document’s lower part.

Red: the document’s top horizontal information rule. Folder, document perimeter and remaining rules are black. Preserve the clearly visible page rising out of the folder.

Sheet 03: Economy & Public Issues

CL-049 · Wealth Concentration · Row 1, column 1

Construction: three cylindrical coin/asset stacks step upward from left to right. Each has a narrow elliptical top, parallel vertical sides and repeated curved horizontal bands. The left stack is short, the middle taller and the right tallest. Their bases sit along the same lower level while overlapping slightly.

Red: the upper elliptical rim of the tallest right-hand stack. Other rims, sides and bands remain black. Count the bands in each source stack and retain the large differences in height.

CL-050 · Worker Bargaining · Row 1, column 2

Construction: two hollow-headed people face inward over a long narrow table. Their rounded shoulder contours bend into forearms near the tabletop. A horizontal double-headed arrow is suspended between them at shoulder height. The table is a simple black top with two or three visible downward supports as shown.

Red: the complete double-headed arrow between the people. Keep figures and table black. This differs from Lobbying, which highlights a small object on the table rather than an arrow above it.

CL-051 · Market Power · Row 1, column 3

Construction: one tall rectangular building at left dominates two shorter buildings to its right. The tall building has a short rooftop block, six small square windows arranged in two columns and three rows, and a small black doorway. The shorter buildings have sparse black window marks. All sit on one continuous baseline.

Red: the tall building’s six window squares. Remaining architecture and smaller-building windows are black. Preserve the descending rightward skyline and the dominant building’s rectangular shape.

CL-052 · Household Security · Row 1, column 4

Construction: a large simple home fills the left/back of the icon, with pitched roof, chimney where visible, open doorway and square window. An upright financial record overlaps the house’s right side. Its upper area contains a dollar sign and its lower area two short horizontal rules. The paper extends from near roof height to the house’s baseline.

Red: the dollar sign on the financial record. Keep house, record outline and rules black. Preserve the overlap rather than placing the page separately beside the house.

CL-053 · Housing Scarcity · Row 1, column 5

Construction: three house positions in a horizontal row. The left and right homes have solid black pitched-roof/wall outlines and paired narrow windows. The middle position is a missing/ghost house drawn only with separated dash-like roof and wall segments. Leave the central ghost home’s interior empty.

Red: every dashed segment of the middle house outline. Outer houses remain black. Preserve the absence of a solid central building; a red door in a complete centre house would be a different icon.

CL-054 · Home Equity · Row 1, column 6

Construction: a large house at left/back with pitched roof, chimney and a plain rectangular doorway. A financial chart panel overlaps the right side. The chart contains three short ascending vertical bars at its bottom and a jagged rising arrow above them, pointing toward upper right.

Red: the upward-right zigzag arrow. House, chart perimeter and bars remain black. Keep this chart drawing distinct from Household Security’s dollar-sign ledger.

CL-055 · Productivity · Row 2, column 1

Construction: a worker at a laptop behind a low desk occupies the lower left. A large hollow circular head rises above the worker’s rounded shoulders. A prominent clock sits upper right, with two simple perpendicular hands. A short right-pointing arrow crosses the gap from the worker toward the clock.

Red: that rightward arrow and the upper/right accent segment of the clock’s circular rim as shown. Clock hands, person, laptop and desk stay black. Preserve the clock as the icon’s second large shape.

CL-056 · Public Investment · Row 2, column 2

Construction: a suspension bridge stretches across the lower part. It has two upright towers, a level deck, curved suspension cables and short vertical supports. Two short water-wave lines sit below. A compact lightbulb floats above the bridge’s central span, with a short base and small radiating strokes.

Red: the bulb contour and its rays, preserving its small black base where visible. Bridge and water stay black. Keep this version’s bulb centred above the bridge; R-36 has a different three-part layout.

CL-057 · Labor Share · Row 2, column 3

Construction: a large circular pie-like form has a black outline around its left and lower portion. A radial black divider extends from its centre toward the lower right. A separate upper-right quarter-sector sits slightly apart from the rest of the circle. Within that sector is a person silhouette cut out as negative space: circular head and rounded shoulders.

Red: the separate quarter-sector, filled solid. The person within it remains a transparent/negative-space cutout. Preserve the small separation at the circle’s top and right and the source’s wedge shape.

CL-058 · Stock Ownership · Row 2, column 4

Construction: a stock certificate at left is an upright rectangular page with several short rules. A small round seal overlaps its lower-right area, with two tiny ribbon tails below. To the right of the page sit three narrow ascending vertical bars on a shared short baseline. The tallest bar is at far right.

Red: the seal’s hollow circular outline and the tallest rightmost bar’s fill. Certificate, ribbon tails, other bars and baseline stay black. Preserve the certificate-plus-chart composition.

CL-059 · Credit Allocation · Row 2, column 5

Construction: a small classical bank sits upper centre, with triangular pediment, three column-like uprights and horizontal base. A vertical stem descends into a branching allocation route. The left branch turns toward a small home at lower left; the right branch turns toward a sawtooth-roof factory at lower right. Both lower buildings have simple black outlines.

Red: the branching connector below the bank, including its central stem and both elbow branches. Bank, home and factory remain black. Preserve the branch direction from bank to two uses.

CL-060 · Taxes & Benefits · Row 2, column 6

Construction: an upright record page at left, with a partially open right edge and five horizontal rules. At right are two separated horizontal arrows: the upper points right and the lower points left. Their shafts have similar lengths and their open angled arrowheads face opposite directions.

Red: the upper right-pointing arrow. Page, information rules and lower left-pointing arrow stay black. Retain the two arrows outside the page rather than drawing them through the text.

CL-061 · Household Income · Row 3, column 1

Construction: a simple frontal person at left with hollow round head and an open-bottom rounded shoulder/torso outline. A small closed envelope sits at right, with rectangular border and diagonals forming its upper flap. A short arrow between person and envelope points right toward the envelope.

Red: the right-pointing arrow. Person and envelope remain black. Preserve the arrow’s actual source direction even though another income metaphor might reverse it.

CL-062 · Assets & Debt · Row 3, column 2

Construction: two unequal cylindrical asset/coin stacks fill the left, with elliptical top rims and repeated curved bands. An upright debt record stands behind/right, with several information rules. A circular minus badge overlaps its lower-right corner, covering part of the page edge.

Red: the badge’s circular border and short horizontal minus. Stacks, page and rules remain black. Keep the badge round, the minus horizontal and both asset stacks visible.

CL-063 · Essential Costs · Row 3, column 3

Construction: a broad home outline forms the back layer. In front is an open grocery bag, with several projecting groceries including a narrow bottle. A large angled price tag hangs to the lower right, with clipped shoulder, small attachment hole and dollar sign. Preserve how the bag and tag obscure the house’s lower section.

Red: the small upright bottle/cap detail among the groceries and the dollar sign on the tag. House, bag, other groceries and tag outline remain black.

CL-064 · Trade Costs · Row 3, column 4

Construction: an outlined parcel/cube at left, with visible top and right side. A rectangular customs/tariff gate stands in the middle-right: two upright posts, short feet and an overhead horizontal band. Two short slanted barrier/tariff marks cross the gate’s middle area. A detached arrow at far right points right.

Red: the two small slanted barrier marks across the gate. Parcel, gate and outgoing arrow remain black. Preserve their unusual parallelogram-like stroke shapes from the reference.

CL-065 · Climate & Insurance · Row 3, column 5

Construction: a small house sits lower left with pitched roof and doorway. A rounded rain cloud floats above, followed by several diagonal raindrop strokes. An upright insurance document stands at right. A simple umbrella symbol is centred within that document, with domed canopy and a hooked shaft.

Red: the umbrella inside the insurance document. Cloud, rain, home and page stay black. Retain the separation between the weather/home grouping and the insurance page.

CL-066 · Energy & Emissions · Row 3, column 6

Construction: a large two-pin electrical plug stands at upper left, its body a rounded U with an open top joined by the pin base. A thin cable drops and curls right into the lower part of a cloud-like emissions shape. The cloud rises at right with several rounded lobes. One short curved plume line sits within it.

Red: the inner curved plume line. Plug, cable and outer emissions cloud remain black. Preserve the continuous cable-to-cloud composition and avoid adding a bolt.

CL-067 · Healthcare · Row 4, column 1

Construction: a large hollow medical cross with equal rectangular arms and rounded stroke joins. A single electrocardiogram-like pulse runs horizontally across its centre: flat entry, a small rise, sharp higher peak/valley sequence and flat exit. The pulse stays inside or just within the cross’s horizontal arms as shown.

Red: the full pulse line. Medical-cross outline stays black. Preserve the source’s exact rhythm of peaks, troughs and flat segments.

CL-068 · Education · Row 4, column 2

Construction: an open book with two curved page blocks, central spine and doubled lower cover contour. A small lightbulb rises out of the book’s central valley. It has a round upper contour, short neck/base and multiple short rays around its upper half. The bulb is much smaller than the book.

Red: the bulb outline and radiating strokes, following the source’s treatment of its tiny base. The book remains black. Distinguish this from Explain, which has rays without an actual bulb.

CL-069 · Childcare · Row 4, column 3

Construction: one large adult figure at left and a smaller child at right, both with hollow circular heads and rounded open-bottom bodies. The adult’s right arm sweeps down and right in a broad embracing curve, meeting the child’s upper body. Their bodies overlap gently rather than standing as isolated generic people.

Red: the adult’s embracing arm stroke. Heads, remaining shoulders and body contours stay black. Preserve the height difference and the low curved meeting point.

CL-070 · Environment · Row 4, column 4

Construction: a large pointed leaf on the left, tilted slightly up-right, with a sweeping inner vein rising from its lower-left stem. A separate large hollow water droplet stands at right, pointed at top and round at bottom. Leaf and droplet have comparable visual height.

Red: the complete water-droplet outline. Leaf contour, stem and inner vein stay black. Retain the open gap between leaf and droplet.

CL-071 · Policy · Row 4, column 5

Construction: an upright page with three horizontal information rules. Near its lower portion, a horizontal adjustment rail begins inside the page and extends out to the right. A hollow circular knob sits on that rail near the page’s right edge. The page contour leaves a small opening around the slider exit.

Red: the circular knob outline. Page, information rules and rail remain black. This has one low slider, distinct from Election Rules’ two-slider page.

CL-072 · Reform · Row 4, column 6

Construction: three routes rise from a close set of stems near the lower centre. The left black route bends outward to the left and ends in a plain rounded line cap. The middle route rises and then bends up-right to an open arrowhead. The right black route bends right to a small hollow circular terminal.

Red: the complete middle redirected route and its arrowhead. Outer routes and right terminal remain black. Preserve the close, parallel lower stems and the three different terminations.

Sheet 04: Reforms R-01–R-25

R-01 · All-Party Primaries · Row 1, column 1

Construction: three small outline person busts stack vertically down the left. Three separate routes extend rightward from them toward one upright rectangular ballot/check card. The middle route is straight; the upper and lower routes curve toward the common destination. All three arrowheads point right. A large check sits centrally inside the right-hand card.

Red: the three routes with their arrowheads and the large check inside the card. People and card border remain black. Preserve the three inputs and the blank area around the check.

R-02 · Ranked-Choice Voting · Row 1, column 2

Construction: a broad rectangular ballot/document, slightly wider than tall. Inside, three small rounded rank cells stack down the left, displaying 1, 2 and 3. Each rank has one long horizontal candidate rule to its right. The top rank cell is filled, while the lower two are outlined. Copy the reference numerals’ compact drawn appearance.

Red: the top rank cell’s filled background; its numeral 1 is a light/negative-space cutout. Lower cell outlines/numerals, candidate rules and page remain black. Preserve the three preferences.

R-03 · Proportional Elections · Row 1, column 3

Construction: a legislative hemicycle made entirely from many small filled circular seat dots. Black dots form two broad curved clusters at left and right. A smaller central upper cluster bridges the two sides, following the same arched seating arrangement. Keep all dot spacing, staggered rows and slight size differences visible in the source.

Red: the central upper cluster of seat dots. All other dots remain black. Count and position the dots from the enlarged crop; avoid replacing this with solid curved chamber bands.

R-04 · Citizen Map Commissions · Row 1, column 4

Construction: an irregular geographic/district outline spans the upper part, using angular steps and short slanted boundary segments. A network of interior district boundaries divides it. Three frontal outline residents overlap its lower edge, with circular hollow heads and simple shoulders. The middle resident sits slightly lower or forward.

Red: the interior district-boundary polylines. Exterior map perimeter and all people remain black. Preserve the particular abstract map shape and boundary network rather than drawing a US outline.

R-05 · Automatic Registration · Row 1, column 5

Construction: a horizontal ID card. Its left side contains a hollow circular head above a small shoulder/torso outline; the right contains staggered short information rules. A circular check badge overlaps and extends beyond the card’s lower-right corner, obscuring part of its border. Trace this reform cell independently from CL-003.

Red: the overlapping badge’s circular outline and check. Card, portrait and rules stay black. Preserve the reform drawing’s own proportions and badge size.

R-06 · On-Cycle Elections · Row 2, column 1

Construction: two equal small calendars sit side by side. Each has a rounded rectangular outer frame, two short binding uprights across its top edge, a horizontal header divider and a compact grid of square dates. A detached horizontal arrow points right in the gap between calendars. The same date positions are highlighted in both.

Red: the matching selected date cells in both calendars and the connecting rightward arrow. Calendar frames and other date cells remain black. Count the source date cells before tracing.

R-07 · Small-Donor Matching · Row 2, column 2

Construction: a short cylindrical coin stack at left and a much taller stack at right. Each uses an elliptical top rim, vertical sides and curved horizontal band lines. A short arrow between them points right from the small stack toward the tall one. Align their lower edges as in the reference.

Red: the rightward arrow and the tallest stack’s upper elliptical rim. Remaining coin outlines are black. Preserve the height contrast and the actual number of stacked bands.

R-08 · Donor Disclosure · Row 2, column 3

Construction: an upright financial disclosure page with a dollar sign near its upper left and information rules to its right and below. A large empty magnifier lens overlaps the page’s lower-right area, with its handle extending diagonally down-right. The lens obscures the page edge.

Red: the magnifier’s narrow handle outline. Dollar sign, page, information rules and lens circle are black. Retain the dollar sign that distinguishes this from the general Watchdogs page.

R-09 · Stock-Trading Ban · Row 2, column 4

Construction: a horizontal stock certificate with an outer rectangular border and a second inset border. The border has small stepped/notched corner details. A jagged black market-price line crosses the interior. A thick diagonal restriction stroke runs from lower left to upper right across the whole certificate and extends slightly outside it.

Red: the broad diagonal restriction stroke. Certificate framing and chart line stay black. Preserve the slash without adding a surrounding prohibition circle.

R-10 · Revolving-Door Limits · Row 2, column 5

Construction: at left, a walking figure passes through a tall rectangular doorway. The figure has a small filled head, angular bent arms and diagonal legs. At right stands an office-like building with a pitched upper contour and rows of small black windows. Between them, a short arrow points right above a filled circular restriction badge with a horizontal knockout bar.

Red: that right-pointing arrow and the restriction disc; the disc’s horizontal bar is negative space. Doorway, person and building remain black.

R-11 · Election Enforcement · Row 3, column 1

Construction: an upright ballot/record at left with several short horizontal rules above a small square check cell. A gavel occupies the right, with its head near upper right and a long handle sloping diagonally down-right. The gavel head has short cap/band details at both ends. There is no separate sound block.

Red: the square check-cell outline/check and the gavel head’s short end-band strokes. Page, text rules, handle and remaining gavel contour stay black.

R-12 · Filibuster Reform · Row 3, column 2

Construction: two blank rounded speech bubbles float side by side above a low debate/chamber rail. The low rail has a long horizontal base and several short vertical divisions. A padlock occupies the gap between the bubbles and rail. Its shackle is visibly open, with one end lifted/free; the body contains a small keyhole.

Red: the open shackle and lock body, with keyhole retained as light/negative space. Bubbles and chamber rail remain black. Preserve the source’s open-lock state.

R-13 · Congressional Capacity · Row 3, column 3

Construction: a small cluster of outline staff members stands at lower left. Behind/centre rises a simplified domed legislative building with façade uprights. An open book occupies the right foreground, partly overlapping the building. Its two page blocks curve toward a central valley and have a doubled lower cover edge.

Red: the lower inner page-edge curve running through the open book. Staff, building and outer book contours remain black. Preserve all three subject groups and their overlapping scale.

R-14 · Automatic Funding · Row 3, column 4

Construction: a broad rounded financial record/card, with a dollar sign at upper left and two short information rules to its right. A long horizontal funding arrow runs along its lower interior and continues out through the open right edge. The arrowhead points right, outside the record.

Red: the full lower funding arrow, including its arrowhead. Record, dollar sign and information rules stay black. Keep the arrow’s continuous relationship to the card’s open right boundary.

R-15 · Watchdog Remedies · Row 3, column 5

Construction: a large magnifier dominates the left foreground. Its circular lens contains a checkmark and its handle slopes down-left. A ruled upright document stands behind it to the right, with several short information strokes. The lens overlaps and obscures the page’s left portion.

Red: the check inside the lens. Lens border, handle, page and rules remain black. Preserve the down-left handle orientation, distinct from the down-right handle used in several other icons.

R-16 · Court Terms & Ethics · Row 4, column 1

Construction: a wide balance scale across the upper portion, with horizontal beam, central pivot, triangular suspension lines and two curved pans. A small clock hangs or sits beneath the beam’s centre, containing two simple hands. A separate smaller circular check badge occupies the lower-right area.

Red: the central clock’s circular contour/hands and the lower-right verification circle/check. The main scales stay black. Preserve both supplementary circular symbols and their unequal sizes.

R-17 · Civil Service · Row 4, column 2

Construction: a horizontal employee ID card with a small centred top tab. Its left half contains an outline person portrait; its right half has three horizontal rules. To the card’s right, a tall curly-brace-like protection boundary runs from near its top to its bottom. The brace has a central inward/outward elbow.

Red: the full right-hand curly brace. Card, top tab, portrait and information rules remain black. Copy the brace’s exact curvature and separation from the card.

R-18 · Emergency-Power Limits · Row 4, column 3

Construction: a tall order/document with several horizontal rules. A large alarm-clock-like circle overlaps its lower-right area. The clock has a short top nub, small upper side projections where visible and two simple hands. The page’s right/lower edges disappear behind the clock.

Red: the clock’s circular perimeter, hands and small associated clock accents visible in the source. Document and text rules stay black. Preserve the clock’s overlap and scale.

R-19 · Drug-Pricing Rules · Row 4, column 4

Construction: two overlapping oblong medicine capsules tilt up-right. The front capsule has rounded ends and a clear diagonal dividing seam around its middle. Behind/right is a large upright price tag with clipped shoulders, a small black attachment hole and a dollar sign. Keep the capsule shapes hollow.

Red: the front capsule’s short dividing seam and the price tag’s outline/dollar sign. Capsule outer contours and tag hole remain black. Preserve the staggered pair of capsules.

R-20 · Merger Enforcement · Row 4, column 5

Construction: two small company-building clusters sit left and right on short baselines, with taller/shorter rectangular blocks and sparse window marks. A broad upward-bowing connector arches between their upper portions. A magnifier overlaps the right-hand cluster’s lower-right area; its handle points diagonally down-right.

Red: the magnifier’s circular lens outline. Buildings, overhead arch and magnifier handle remain black. Retain the lens empty and count the source building/window divisions.

R-21 · Labor-Law Remedies · Row 5, column 1

Construction: an outline worker in a hard hat stands at left. The hat has a rounded crown, short top detail and horizontal brim; the faceless head and shoulders are visible below. A tall ruled labor document stands behind/right. A large circular verification badge overlaps its lower-right corner.

Red: the verification circle and its check. Worker, hat, page and information rules remain black. Preserve the clear hard-hat silhouette and the document’s back-layer placement.

R-22 · Wage Boards · Row 5, column 2

Construction: three outline people sit/stand around a long straight table. A taller central person is behind, with two shorter participants at left and right. Their arms point inward above the tabletop. A low trapezoidal tabletop/negotiation shape sits at the centre, with a flat short top and slanting side strokes.

Red: the central low trapezoidal tabletop stroke. People, main table surface and legs remain black. Preserve the three-person triangular composition.

R-23 · Indexed Minimum Wage · Row 5, column 3

Construction: a tall wage ledger/document, with a dollar sign at upper left and short rules below/right. Three small ascending bars occupy its lower-right area. A separate curved arrow rises across the interior from lower left toward upper right, ending with an open angled arrowhead above the bars.

Red: the rising curved arrow. Document, dollar sign, information rules and bar chart remain black. Match the arrow’s curve and keep it separate from the black bars.

R-24 · Paid Leave · Row 5, column 4

Construction: a large adult and smaller child form the left foreground, with hollow heads and rounded open-bottom bodies. A calendar stands behind them to the upper right, with binding uprights, header line and date cells. A small shield-shaped benefit badge overlaps the calendar’s lower-right area and contains a dollar sign.

Red: the calendar’s selected date squares and the shield outline/dollar sign. Figures and main calendar framing stay black. Retain the shield because it is present in this exact approved drawing.

R-25 · Child Tax Credit · Row 5, column 5

Construction: a small child-like outline figure stands at left, with hollow round head, a tiny hair/curl detail visible at its upper edge and rounded open torso. A ruled tax record rises behind/right. A large outlined coin with a dollar sign overlaps the record’s lower-right area. Between record and child, a short arrow points left toward the child.

Red: the left-pointing support arrow and the coin’s dollar sign. Child, record, rules and coin border remain black. Follow the source’s small head detail closely.

Sheet 05: Reforms R-26–R-50

R-26 · Automatic Recession Aid · Row 1, column 1

Construction: a home at lower left, with pitched roof, simple walls and narrow interior uprights/door. Unequal coin stacks sit lower right, using elliptical tops and curved bands. A large declining zigzag arrow spans the upper area: it descends, briefly rises and then descends to an open arrowhead toward the upper-right coin area.

Red: the full downward-trending zigzag arrow. Home and coin stacks stay black. Preserve the source’s short upward interruption within the overall downward trend.

R-27 · Tax Enforcement · Row 1, column 2

Construction: an upright tax record with several short horizontal rules at left. A large magnifier overlaps its lower-right portion; its handle runs diagonally down-right. Within the lens is a short gauge-like semicircular arch near the upper half. The rest of the lens remains empty.

Red: only that inner semicircular gauge arc. Magnifier border/handle, page and rules are black. This is not the red-handle Donor Disclosure icon or the check-in-lens Watchdog Remedies icon.

R-28 · Capital-Income Tax · Row 1, column 3

Construction: unequal cylindrical asset stacks occupy the left, one shorter/front and one taller/back, with elliptical rims and repeated curved bands. A tall tax record overlaps behind/right. Its upper area has short information rules; a dollar sign occupies the right-middle/lower area, followed by small rules below as visible.

Red: the dollar sign on the tax record. Stacks, page and other information marks remain black. Preserve the stack-to-page overlap and distinct heights.

R-29 · Baby Bonds · Row 1, column 4

Construction: a small faceless child stands at left, with hollow circular head, short arms and simple legs. A broad outlined piggy bank occupies the right, with rounded back/belly, projecting snout, tiny ear, feet and a short top coin slot. A large hollow coin floats directly above that slot.

Red: the hollow coin outline above the piggy bank. Child and piggy-bank contours remain black. Preserve the pig’s actual profile and the gap between coin and slot.

R-30 · By-Right Housing · Row 1, column 5

Construction: two pitched-roof homes stand at left/centre, one smaller and one larger. The larger central home has a prominent doorway. Behind/right is an upright approval document with short black rules. A large round check badge overlaps the document’s lower-right region, extending outside its perimeter.

Red: the larger home’s filled doorway and the approval badge’s circular border/check. Other architecture, document and rules stay black. Retain the two different house sizes.

R-31 · Childcare Supply · Row 2, column 1

Construction: a small childcare building occupies the left. It has a low wing, taller central block, triangular roof, sparse windows and a large arched doorway. A hollow circular head is positioned above the roof peak as part of the child-centred building motif. A separate larger outline adult stands at right.

Red: the building’s filled arched doorway. All other outlines stay black. Preserve the small head above the roof and the separate right-hand adult.

R-32 · Local-News Funding · Row 2, column 2

Construction: a large newspaper at left with a rounded front sheet, rolled/stacked return contour at its left edge, multiple horizontal information rules and one rectangular image/article block on the lower-right of the front page. A cylindrical coin stack sits separately at lower right, overlapping or closely meeting the paper’s side.

Red: the newspaper’s rectangular article block. Coin stack, newspaper contours and information rules stay black. Preserve the funding stack absent from CL-032.

R-33 · Citizen Assemblies · Row 2, column 3

Construction: five outline people encircle a small oval deliberation table. A taller central person stands behind the table; two mid-level people sit farther left/right, and two lower foreground figures frame the table’s sides. The table has an elliptical top and short vertical legs.

Red: the central upper person’s head circle and shoulder/torso outline. The other four people and table remain black. Match the five-person spacing and the oval table’s overlap.

R-34 · Participatory Budgeting · Row 2, column 4

Construction: a large upright budget/checklist page stands behind a row of residents. The page has a left column of checkbox squares and black horizontal choice rules to their right. Several hollow-headed outline residents overlap its bottom edge, with different heights. Preserve the source’s actual resident and checkbox counts.

Red: the selected checkbox cells/check marks near the checklist’s upper-left area, including their filled-versus-outlined treatment. Page, information rules and residents remain black. Retain the residents in front of the document.

R-35 · Term Limits · Rejected · Row 2, column 5

Construction: an officeholder at a desk occupies the left, with hollow head, rounded shoulders and short tabletop/legs. A large hollow clock sits behind/right, with two black hands. A filled circular rejection badge overlaps the clock’s lower-right area; its centre contains a thick X knockout.

Red: the rejection disc. The X remains light/negative space, and all other geometry remains black. Preserve the exact caption “Term Limits · Rejected”; the black edition uses a black disc with the same X cutout.

R-36 · Public Investment · Row 3, column 1

Construction: three clearly separated subjects: a tall bulb at left, a small suspension bridge in the middle and an upright funding ledger at right. The bulb has rays, a short base and an inner filament. The bridge has two upright towers and curved suspension cables. The ledger has a dollar sign and a few black information rules.

Red: bulb contour/rays and the ledger’s dollar sign. Preserve any tiny black bulb-base/filament details visible in the reference. Bridge and ledger framing stay black. This differs from CL-056’s bulb-over-bridge layout.

R-37 · Feed Choice · Row 3, column 2

Construction: a rounded browser window at left with three small top-bar dots, a horizontal header divider and several content/selector rules. A horizontal slider near its lower area has a hollow circular knob. At right stands a large upright key with hollow round bow, vertical stem and two short side teeth.

Red: the slider’s circular knob. Browser, content rules, rail and separate key remain black. Keep the large key detached from the browser.

R-38 · Pricing-Data Limits · Row 3, column 3

Construction: two upright price tags face each other left and right. Each has clipped upper shoulders, a black attachment hole and a dollar sign inside. A short dashed horizontal data link crosses the gap between tags. A circular prohibition symbol sits centrally on that link, with a diagonal slash.

Red: both dollar signs and the central prohibition circle/slash. Tag contours, holes and short dashed link strokes stay black. Preserve the circle as an explicit interrupted-link marker.

R-39 · Digital Service Teams · Row 3, column 4

Construction: a landscape monitor/service screen occupies the left. Inside is an outline ID portrait at left and several horizontal interface rules at right. A small stand descends below the screen. Two small outline people stand together outside the screen at right, their shoulders partially overlapping.

Red: the horizontal interface rules to the right of the portrait. Screen, portrait, stand and the two team members remain black. Preserve the portrait-in-screen plus people-outside composition.

R-40 · Worker Voice on AI · Row 3, column 5

Construction: an outline worker bust at left with hollow head and rounded open shoulders. A rounded rectangular speech bubble floats above/right of the worker and contains three horizontal message strokes. A large square microchip occupies the right, with short pins on all sides and the uppercase letters AI centred inside.

Red: the three message strokes and the AI lettering. Person, bubble outline, chip outline and pins remain black. Match the reference’s letter shapes and pin count.

R-41 · Grid Cost Allocation · Row 4, column 1

Construction: a vertical stack of three rounded server trays at left, with small indicators and short rules. A narrow electrical plug with two upright pins and a curling short cable occupies the centre. An upright electricity-cost record stands at right, containing a small top rule and a large dollar sign.

Red: the dollar sign on the right-hand record. Servers, plug, cable and paper remain black. Retain the three-part servers/plug/bill sequence.

R-42 · Congressional Tariff Votes · Row 4, column 2

Construction: a small domed legislative building stands at left. A compact ballot box overlaps the centre foreground, with a shallow lid and a slanted ballot. At right is a small rising bar chart on a common baseline. A detached horizontal arrow above the chart points right.

Red: the ballot’s upper/right accent edge and the right-pointing arrow above the chart. Building, box and chart bars remain black. Preserve the actual chart in the source rather than substituting goods or a shipping box.

R-43 · Disaster Mitigation · Row 4, column 3

Construction: a pitched-roof home stands beneath a rounded storm cloud. Short diagonal rain strokes fall around its roof. Several wavy horizontal flood lines run beneath and across its lower area. The house has a simple doorway/window and a reinforced-looking broad roof segment on one slope.

Red: the broad diagonal roof segment on the house’s right-facing roof slope. House remainder, rain, cloud and flood waves stay black. Preserve the source’s specific reinforced roof orientation.

R-44 · Digital Competition · Row 4, column 4

Construction: two matching small browser windows at left and right. Each has a top header band with small dots and a large magnifier symbol inside its content area. Between the windows, an upper arrow points right and a lower arrow points left. Keep the two arrows detached from the window edges.

Red: both in-window magnifiers and the upper right-pointing arrow. Browser framing and lower left-pointing arrow remain black. Preserve equal window dimensions and the opposing-arrow arrangement.

R-45 · Paper Ballots & Audits · Row 4, column 5

Construction: a stack of three offset paper sheets, with the front upright ballot/record at centre-right. Short information rules sit near the front page’s upper area. A large magnifier overlaps the lower-right portion; its handle slopes down-right and its lens contains a simple checkmark.

Red: the front page’s top information rule and the check inside the lens. Paper contours, other rules, lens border and handle stay black. Preserve the visible offset sheet edges.

R-46 · Expand the House · Row 5, column 1

Construction: a broad semicircular legislative chamber viewed schematically from above. A curved outer boundary contains multiple small outlined seat rectangles that follow its arc. More seats form inner curved rows. A small raised dais/podium stands near the top centre, with a short roof/cap-like detail.

Red: the small group of newly added seats along the chamber’s upper-right outer arc. Other seats, curved framing and dais stay black. Count and position the seat rectangles directly from the enlarged reference.

R-47 · Fusion Voting · Row 5, column 2

Construction: two upright candidate portrait cards stand at left and right. Each contains a hollow head, shoulders and a short lower caption rule. Between and below them is one larger outline person bust. Two short inward-sloping connector strokes approach the central area from the upper-inner sides of the cards.

Red: both cards’ lower caption rules and the right-hand inward-sloping connector. Cards, portraits, central person and left connector stay black. Preserve the shared central-person arrangement.

R-48 · Agency Independence · Row 5, column 3

Construction: a small classical public-agency building at left, with triangular pediment, repeated columns and doubled baseline. An official stands behind a lectern at right, with hollow head and shoulders. Between them is a tall brace-like vertical separation mark with short curved/stepped ends and a middle elbow.

Red: the full separating brace. Agency and official remain black. Preserve the visual separation and the particular brace contour rather than inserting a wall, shield or padlock.

R-49 · Cross-Party Civic Work · Row 5, column 4

Construction: two outline people stand at left and right with hollow heads and rounded shoulders. A small bridge spans between their lower/middle bodies, with a central peaked/arched structural contour and short vertical supports. One broad shallow connecting arc rises over the people and bridge, ending near the outside heads/shoulders.

Red: the overhead connecting arc. People and bridge stay black. Preserve the open gap beneath the arc and the shared bridge between the two figures.

R-50 · Popular-Vote Options · Row 5, column 5

Construction: four small upright ballot/record cards align across the top, each with short black horizontal rules and a small lower mark. A broad collecting brace runs beneath all four. Below it sits a compact outline map of the contiguous United States, with a small check inside.

Red: the collecting brace and the check inside the US outline. Cards, their rules and the map perimeter stay black. Preserve four cards and the specific simplified mainland silhouette.

Final acceptance checklist

• All 122 catalogue entries are present: CL-001–CL-072 and R-01–R-50.
• All five source-sheet orders are preserved.
• Every entry has both a red-black and a black edition.
• Each edition pair shares geometry, transforms, masks, viewBox and clear space.
• Each accent agrees with the corresponding red reference cell.
• Each black version retains every accent shape in Charcoal.
• Symbols and small details match the image: restriction discs, numeral cutouts, clocks, seals, slot gaps, pin counts, dot arrangements and arrow directions.
• Standalone SVGs contain real editable vector geometry and transparent backgrounds.
• Captions, sheet titles and reform IDs stay outside the icon assets.
• R-35 retains its Rejected status.
• Contact sheets, inventory and preview agree on names, IDs and file counts.
• Overlay/edge comparisons are completed where tools allow, with unresolved differences listed accurately.

Deliver the complete package and a brief report of actual verification. Let the source artwork determine the result all the way through the final export.