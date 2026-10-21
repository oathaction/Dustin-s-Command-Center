"""Phase 1 research lead: build the October 21, 2026 addendum to the rights ledger.

Reads work/handoffs/phase-1/20261021_Pics-I-Like-Inventory.json (made by
pics_pdf_inventory.py), combines it with the page classification below
(made by viewing the six contact sheets and twelve pages at full size), and
appends a dated section to work/research/20261020_Rights-Ledger.md.
Refuses to append twice. Nothing in source/ or work/extract/ is written.

Run: python3 -I work/build/scripts/phase-1/build_rights_addendum.py <ROOT>
"""
import json
import os
import sys

root = sys.argv[1]
inv_path = os.path.join(root, "work", "handoffs", "phase-1", "20261021_Pics-I-Like-Inventory.json")
ledger = os.path.join(root, "work", "research", "20261020_Rights-Ledger.md")
MARK = "## Added October 21, 2026: Phase 1 rights review"

inv = json.load(open(inv_path))
pages = {p["page"]: p for p in inv["pages"]}
dup_of = {}
for group in inv["duplicate_page_groups"]:
    first = min(group)
    for g in group:
        if g != first:
            dup_of[g] = first

GEN = "generated mockup"
OAW = "screenshot of Oath & Action atlas work"
OAD = "screenshot of Oath & Action design study"

# page: (class, content as seen, note)
C = {
    1: (GEN, "Brand board: condensed heavy wordmark over 'FROM SPECTATORS TO STEWARDS.', four round pillar badges labelled Understand, Expose, Connect, Act, footer strip with the editorial commitment and X, LinkedIn and email icons, generated photoreal documentary scenes and Capitol columns", "Pillar names differ from the locked Explain, Track, Connect, Act"),
    2: (GEN, "Social and Substack template sheet: 'Democracy has a structure.', a '12.4M' stat card, carousel, quote post, newsletter and article layouts, Capitol photo", "'12.4M' is an unsourced figure"),
    3: (GEN, "Brand board: circular seal logo with 'EST. 2026', named palette swatches, 'INTER TIGHT' type card, 'We explain the rules. We expose the gaps.' statement, Capitol photo, phone, notebook and mug, outline icon set", ""),
    4: (GEN, "Component library: hero 'From spectators to stewards.', pillar explainer row, '12.4M' data card, structure grid, call to action, quote block, footer, hinge diagram, four-step 'How to build'", ""),
    5: (GEN, "Imagery and photo direction: nine generated photoreal civic scenes (voting, registering, town hall, signatures, reading the news, discussing issues, volunteering, organizing, building solutions), overlay and caption system", "Photoreal generated people. Never present as photographs (brief section 16)"),
    6: (GEN, "Applications: email header and footer, social profile, report cover, website banner, notebook and hands", ""),
    7: (GEN, "Logo system: primary condensed wordmark, stacked logo, horizontal lockup, O&A monogram, circle and square ampersand marks in five colors, standalone ampersands, seals, construction and minimum size, application row (cap, app icon, deck cover)", "Repeated on pages 37, 38, 43 and 46"),
    8: (GEN, "Stationery and applications: business cards, letterhead, envelope, 'Democracy has a structure.' poster, Capitol-dome web hero, pillar row, social post", ""),
    9: (GEN, "Brand identity board 'DEMOCRACY HAS A STRUCTURE.': pillar line icons, palette with a bright blue and a coral, typography, logo system, do-not row, in-use examples", "Palette departs from the locked colors"),
    10: (GEN, "Brand identity sheet in Midnight, Persimmon, Teal and Bone: watermarks, avatars, Substack banner, email header, post examples 'Track It. Share It. Change It.'", "Palette departs from the locked colors"),
    11: (GEN, "Variant of page 10 with stacked logo, icon variations, structure mark, seals and usage guidelines", "Palette departs from the locked colors"),
    12: (GEN, "Two hinge diagrams: OATH and ACTION joined through a circled red ampersand with dashed return arrows, 'UNDERSTAND' and 'IMPACT' labels, 'The ampersand is the hinge.'", "Same compositions as the two hinge files in source/brand-mockups/"),
    13: (GEN, "Prussian banner 'From spectators to stewards.' (3,318 x 474 canvas) above a logo system board like page 07", "Banner matches 20261021_Mockup-Banner-Prussian-Stewards.webp in content"),
    14: (OAD, "Data visualization concept studies on one sheet, headed 'All values and records are illustrative.': a budget bar chart, a record line, a dumbbell, a 100-square unit chart, a waterfall, interval estimates, a stage tracker and a responsibility map, each footed 'ILLUSTRATIVE DATA / DESIGN STUDY'", "Rendered page with live-quality text. The first specimen sets Pillar Red, Charcoal and Prussian bars side by side"),
    15: (GEN, "Logo in context, 'PHOTO DIRECTION - REAL ACTION. REAL PEOPLE.' with five generated photoreal scenes, civic action icon set, favicon states, email headers, watermark system, merchandise (clipboard, bottle, tote, notebook)", "Photoreal generated people. Never present as photographs"),
    17: (GEN, "Brand philosophy, values, photography style, social templates such as 'UNDERSTAND THE SYSTEM. CHANGE THE OUTCOME.' and 'TOWN HALLS. REAL QUESTIONS.', print, stationery, infographic", "Photoreal generated people"),
    18: (GEN, "Brand identity board with Newsprint, Charcoal, Pillar Red and Prussian swatches, pillar icons, typography, logo system, do-not row, 'A PUBLIC INFRASTRUCTURE PUBLICATION'", ""),
    19: (GEN, "Logo system, watermarks, social templates, email header and footer, avatars, palette labelled True Black, Pillar Red, Stone, Newsprint, usage guidelines", ""),
    24: (GEN, "Atlas home page mock 'WHO DO THEY ANSWER TO?' with generated editorial illustrations, R8 housing loop card, footer '193 issue records', '50 reforms', '740 sources'", "Same image as design-i-like-19 (mean pixel difference 1.3 of 255 at 64 x 43), which carries an OpenAI C2PA manifest dated 2026-10-15. '740 sources' conflicts with V7 meta.counts sources 1,099"),
    25: (GEN, "New logo concepts: Capitol-dome emblem, 'O|A' monogram, seals, banners, expanded icon set, content and social post templates such as 'Democracy is not a spectator sport.'", ""),
    27: (GEN, "Multi-panel identity overview: logo system, color system with a usage-ratio pie, typography system, spacing system, component library", "Repeated on page 47"),
    35: (GEN, "Three icon study sheets side by side, cropped: '03 / Measured Lines', '02 / Civic Impressions', '08 / Simple Line'", "Canvas sizes 1,024 x 1,536 and 1,086 x 1,448 match the C2PA-signed ChatGPT icon studies. The 02 and 03 titles differ from the names in brief section 2"),
    40: (GEN, "Brand expression board 'FROM SPECTATORS TO STEWARDS.': brand principles (Clarity, Truth, Connection, Action), poster series, social, seals, photography overlay styles, presentation, story card, motion frames", "Photoreal generated people"),
    41: (GEN, "'NEW CONTENT IDEAS & CONCEPTS FOR OATH & ACTION': social carousel, '12.4M' data concept, quote cards, an interactive hinge diagram, event card, cap and t-shirt, report cover, badges, website hero, tote", "Photoreal generated people"),
    44: (GEN, "Crop of the seals and badges row (476 x 152)", "Crop of page 07"),
    45: (GEN, "Identity overview on a 1,672 x 941 canvas: pillar badges, Verdigris promise band, logo system, color system with Verdigris and a usage-ratio pie, type scale, spacing, component library", "Canvas size is unlike the others; visual traits match the generated boards"),
    48: (GEN, "Crop 'EXPLAINER - OUR PILLARS (COMPACT)' (577 x 278)", "Crop of page 04"),
    20: (OAW, "Concepts V2, Concept 09 The Circuit, 'How the whole system is wired.'", "1,184 x 1,167, the same size as design-i-like-14"),
    21: (OAW, "Concepts V2, Concept 10 Who Can Act, 'Who can act, and what it would change.'", "1,201 x 1,367, the same size as design-i-like-15"),
    22: (OAW, "Concepts V2, Concept 11 Register index, 'The whole atlas, line by line.'", "1,200 x 870, the same size as design-i-like-16"),
    23: (OAW, "Concepts V2, Concept 11 Register sheet D02 'Elections and representation'", "1,179 x 1,392, the same size as design-i-like-17"),
    34: (OAW, "Concepts V2, Concept 00 The shared language, 'Every line says what happens next, and how sure we are.'", "1,152 x 720, the same size as design-i-like-07"),
    39: (OAW, "Earlier atlas concept headed 'THE SYSTEMS ATLAS CONCEPT 09': 'HOW ELECTIONS CAN CORRECT POOR PERFORMANCE', loop B4 with D5, C3, C5 and L23, L24, L54", "Footer: 'Private design preview. Evidence labels follow the supplied V4 model.' Built on an earlier model; reconcile every value to V7 before any use"),
    49: (OAW, "Atlas page 'Follow a direct relationship.' in dark mode, header 'THE SYSTEMS ATLAS Edition 10 - October 20, 2026', footer 'Publication snapshot: October 15, 2026'", "An atlas build later than the supplied V7 file. Treat as a dated capture"),
    50: (OAW, "Tall capture (1,920 x 6,041) of Concepts V2: Concept 08 Loop Field Guide and Concept 09 The Circuit 'The system runs in one long loop.'", ""),
    51: (OAW, "Concepts V2, Concept 03 Field Manual, 'Three layers, one machine.'", "1,600 x 1,000; design-i-like-13 is a 1,597 x 998 capture of the same view"),
    52: (OAW, "Atlas home page 'WHO DO THEY ANSWER TO?' with 'Start with something familiar' and 'See how the system fits together'", "Shows 50 variables, 117 numbered connections, 23 feedback loops and 50 reform profiles. V7 meta.counts gives 51 variables and 118 connections. A different build; never cite its counts"),
    53: (OAW, "Atlas loop page 'WHAT KEEPS A PATTERN GOING?' with loop R1", ""),
    54: (OAW, "Five Concept 03 'Civic Circuit' panels: 'Who do they answer to?', 'When the primary decides the seat', 'Can elections correct poor performance?', 'Does my vote change who represents me?', 'Why can housing scarcity sustain itself?'", "Footers name 'Systems Atlas V7 - Model snapshot 15 October 2026'"),
}


def sizes(p):
    return "; ".join(f"{i['w']:,} x {i['h']:,}" for i in pages[p]["images"] if "w" in i)


rows = []
counts = {GEN: 0, OAW: 0, OAD: 0}
for n in range(1, inv["page_count"] + 1):
    if n in dup_of:
        base = dup_of[n]
        cls, content, note = C[base]
        content = f"Same page as page {base:02d} (identical render, SHA-256 match)"
        note = ""
    else:
        cls, content, note = C[n]
    counts[cls] += 1
    if cls == GEN:
        use = "study only"
        terms = "T-OPENAI (Q-02). Direction and principles only. Never trace, embed or ship; never as evidence"
    elif cls == OAW:
        use = "may ship with label"
        terms = "T-OA (Q-03). Oath & Action owns it. Show only as a dated record of earlier work, labelled; re-read every value from V7; never as independent evidence"
    else:
        use = "may ship with label"
        terms = "T-OA (Q-03 covers atlas work; Dustin supplied this sheet as his own design study). Its values are illustrative and say so"
    full_note = "; ".join(x for x in (note, terms) if x)
    rows.append(f"| pics-{n:02d} | `source/pics_i_like.pdf` page {n} | {sizes(n)} | {cls} | {content} | {use} | {full_note} |")

unique = inv["unique_pages"]
meta = inv["metadata"]
dups = "; ".join(", ".join(f"{x:02d}" for x in g) for g in inv["duplicate_page_groups"])

text = f"""

{MARK}

Research lead, Phase 1. Checked October 21, 2026. Method: I viewed the six contact sheets `work/boards/screens/references/pics-i-like-01.jpg` to `-06.jpg`, opened twelve rendered pages at full size (05, 13, 14, 15, 23, 24, 35, 39, 45, 49, 52, 53, 54), and ran `work/build/scripts/phase-1/pics_pdf_inventory.py` (PDF metadata, embedded image sizes, page hashes; output `work/handoffs/phase-1/20261021_Pics-I-Like-Inventory.json`) and `work/build/scripts/phase-1/mockup_metadata.py` (WebP chunks and provenance strings). Nothing in `source/` or `work/extract/` changed.

### Dustin's answers recorded (from `work/ledger/20261020_Open-Questions.md`, answered October 21, 2026)

| Question | Answer as recorded | Effect on this ledger |
|---|---|---|
| Q-02: tool, plan and prompts for icon studies 04, 05 and 08 | Made with ChatGPT on the plan Dustin describes as "pro plan 6.1 Sol High effort ($20/m)". No outside images went into the prompts; the prompts described design aesthetics only | Rows icon-studies-01 to -03 change from "probable" to confirmed ChatGPT output under T-OPENAI. Master Brief V2 section 2 extends the same account to the brand mockups and most of `pics_i_like.pdf`. Permitted use stays study only: the US Copyright Office position in T-OPENAI means Oath & Action cannot claim these images as its own authored artwork, so final marks stay authored vectors |
| Q-03: ownership of Concepts V1 and V2, the Atlas Visual System and Atlas V7 | Oath & Action owns all atlas work, including their diagrams | The seven "screenshot of Oath & Action work" rows and the four embedded SVGs are confirmed as T-OA. The atlas screenshots in `pics_i_like.pdf` below inherit this |
| Q-05: stock licenses held | Dustin believes none are held. Assume none | The 22 stock previews stay study only. No stock image may ship |
| Q-06: source of data-viz 25 to 28 | Screenshots of a search Dustin ran, not fully cropped by accident | Rows data-viz-25 to -28 stay third-party screenshots, study only. The visible name tiles of private people mean they never appear on a board shown outside the studio |

### Fonts: Atlas V7's URW faces are replaced (DC-03)

Dustin decided on October 20, 2026 (DC-03) that the atlas converges on the guide's fonts. V6 replaces the four URW++ base35 faces that Atlas V7 embeds under the aliases "Atlas Display", "Atlas Sans" and "Atlas Mono" (rows font-10 to font-13: Nimbus Sans Regular and Bold, Nimbus Sans Narrow Bold, Nimbus Mono PS) with Inter Tight for display and Inter for reading and interface. V6 ships no URW file, so V6 needs no URW license text. The supplied Atlas V7 file stays as it is in `source/`. The open question in "Could not verify" about the URW exception's reach on the web no longer blocks any V6 deliverable; it matters only if the atlas team keeps the V7 build in public use.

| # | File | Set | Likely origin | Evidence | Permitted use | Notes |
|---|---|---|---|---|---|---|
| font-10 to font-13, update | `source/20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html` (four data-URI fonts) | font | font foundry | Rows above; DC-03 in `work/ledger/20261020_Decision-Log.md` | not used in V6 | Replaced in every V6 atlas application by Inter Tight (display) and Inter (reading, interface, data labels). No V6 file embeds or ships them. Any monospaced need in V6 goes to the design director as a separate proposal, because Inter and Inter Tight have no monospaced cut |

### source/pics_i_like.pdf

File facts: {inv['size_bytes']:,} bytes; SHA-256 `{inv['sha256']}` (matches `work/ledger/20261020_Source-Manifest.md`); {inv['page_count']} pages, each built from one to three embedded raster images, with no text layer. Metadata: Author "{meta.get('/Author','')}", Creator "{meta.get('/Creator','')}", Producer "{meta.get('/Producer','')}", created {meta.get('/CreationDate','')}. The PowerPoint export carries no C2PA manifest or IPTC source type, so provenance rests on Dustin's account (Q-02), on canvas sizes, and on one exact image match.

{unique} of the 54 pages are unique. Identical page groups (SHA-256 of the rendered PNG): {dups}.

Classification by page: {counts[GEN]} generated mockups, {counts[OAW]} screenshots of Oath & Action atlas work, {counts[OAD]} screenshot of an Oath & Action design study (page 14), and 0 pages of third-party material. Evidence for the generated class: canvas sizes of 1,536 x 1,024, 1,024 x 1,536, 1,448 x 1,086 and 1,086 x 1,448, the sizes of the C2PA-signed ChatGPT images in this ledger; generated text artifacts; and page 24, which matches design-i-like-19, a C2PA-signed ChatGPT image. Evidence for the atlas class: pixel sizes identical to the dated browser captures design-i-like-07 and -14 to -17, live-quality text, and atlas wordmarks, IDs and footers.

Third-party content inside the generated mockups: X, LinkedIn, Instagram and email icons in footers (pages 01, 10, 11, 15, 19 and duplicates), the U.S. flag, and buildings that resemble the U.S. Capitol. None is a copied photograph that I could identify at the scale reviewed. Platform icons follow each platform's own brand rules when V6 uses them; V6 draws them from the platforms' official asset kits, never from these mockups.

| # | File | Embedded image size (px) | Likely origin | Content as seen | Permitted use | Notes |
|---|---|---|---|---|---|---|
""" + "\n".join(rows) + f"""

### source/brand-mockups/

Dustin's account (Master Brief V2 section 2, Q-02): generated in ChatGPT from his written descriptions, with no outside images in the prompts. Direction only. All four files are lossy WebP (VP8) with an ICC profile and no EXIF, XMP or C2PA chunk; checksums match the source manifest.

| # | File | Set | Likely origin | Evidence | Permitted use | Notes |
|---|---|---|---|---|---|---|
| mockup-01 | `source/brand-mockups/20261021_Mockup-Banner-Prussian-Stewards.webp` | brand-mockups | AI-generated study | WebP 2,000 x 286, VP8X, ICCP and VP8 chunks only. Prussian banner: condensed heavy OATH and ACTION in Newsprint with a red serif ampersand, rule, 'From spectators to stewards.' with 'stewards.' in red, a 3 x 3 node grid with one red and one verdigris node | study only | T-OPENAI (Q-02). Direction for the banner lockup and the candidate line only. Sets the red ampersand on Prussian, an open Gate 1 decision. Never ship; rebuild from authored vectors |
| mockup-02 | `source/brand-mockups/20261021_Mockup-Hinge-Diagram-Newsprint.webp` | brand-mockups | AI-generated study | WebP 1,536 x 1,024, VP8X, ICCP and VP8 only. OATH and ACTION joined by lines with end nodes to a circled red ampersand, dashed curved arrows above and below, labels 'UNDERSTAND' and 'IMPACT', italic 'The ampersand is the hinge.' | study only | T-OPENAI (Q-02). Direction for the hinge diagram. The lower arc has no arrowheads while the upper arc has two, so the drawing does not settle the direction of the cycle |
| mockup-03 | `source/brand-mockups/20261021_Mockup-Hinge-Diagram-Transparent.webp` | brand-mockups | AI-generated study | WebP 1,254 x 1,254, VP8X, ICCP and VP8 only, RGB with no alpha chunk. The hinge diagram in Newsprint-colored strokes over a checkerboard | study only | T-OPENAI (Q-02). The file is not transparent: the checkerboard is painted into the pixels. Never use it as a cut-out asset |
| mockup-04 | `source/brand-mockups/20261021_Mockup-Square-Wordmark-Stewards.webp` | brand-mockups | AI-generated study | WebP 1,254 x 1,254, VP8X, ICCP and VP8 only. Stacked 'OATH & / ACTION' in a wide geometric sans with a red sans ampersand, tracked 'FROM SPECTATORS TO STEWARDS.', a 5 x 5 node grid with one red and one verdigris node, a small hinge diagram, a Prussian footer band 'CIVIC LIFE - INSTITUTIONS - ACCOUNTABILITY - SOLUTIONS' | study only | T-OPENAI (Q-02). Its wordmark face is neither Inter Tight nor condensed, unlike the other references. Direction for a square social or poster format only |

### Counts for this addendum

| Set | Rows | generated mockup or AI-generated study | screenshot of Oath & Action work | font update | study only | may ship with label | not used in V6 |
|---|---|---|---|---|---|---|---|
| pics_i_like.pdf pages | 54 | {counts[GEN]} | {counts[OAW] + counts[OAD]} | 0 | {counts[GEN]} | {counts[OAW] + counts[OAD]} | 0 |
| brand-mockups | 4 | 4 | 0 | 0 | 4 | 0 | 0 |
| fonts | 1 (covers four files) | 0 | 0 | 1 | 0 | 0 | 1 |

### Could not verify (October 21, 2026)

- The tool behind each page of `pics_i_like.pdf` beyond page 24. The PDF strips provenance metadata, so the generated class rests on Dustin's account, canvas sizes and visual traits.
- Which build of the atlas pages 49 and 52 to 54 show. Page 49 names "Edition 10", and page 52's counts differ from V7.
- The prompts behind the generated images. Brief section 16 asks for tool, date, prompt and terms; Dustin gave the tool and plan, and the prompts are not on file.
- The current wording of OpenAI's terms. The T-OPENAI summary rests on official-domain search snippets from October 20, 2026; no page could be opened.
"""

current = open(ledger, encoding="utf-8").read()
if MARK in current:
    sys.exit("Addendum already present; nothing written.")
with open(ledger, "a", encoding="utf-8") as fh:
    fh.write(text)
print("appended", len(text), "characters;", counts)
