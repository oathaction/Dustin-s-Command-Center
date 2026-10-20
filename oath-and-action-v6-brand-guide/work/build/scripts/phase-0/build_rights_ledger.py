"""Phase 0: build the first version of the rights ledger.

Read-only on source/ and work/extract/. Reads
  work/boards/screens/references/index.json
  work/handoffs/phase-0/20261020_Rights-Image-Metadata.json   (image_metadata.py)
  work/handoffs/phase-0/20261020_Rights-Font-Name-Tables.json (font_names.py)
and writes work/research/20261020_Rights-Ledger.md.

The per-item classifications below were made by the research lead after
viewing every contact sheet and opening unclear files in full on
October 20, 2026. The script only joins them to paths and metadata and
counts them.

Usage: python3 -I build_rights_ledger.py <ROOT>
"""
import collections
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "work/research/20261020_Rights-Ledger.md"
IDX = json.loads((ROOT / "work/boards/screens/references/index.json").read_text())
META = json.loads((ROOT / "work/handoffs/phase-0/20261020_Rights-Image-Metadata.json").read_text())
FONTS = json.loads((ROOT / "work/handoffs/phase-0/20261020_Rights-Font-Name-Tables.json").read_text())

SP = "stock preview"
TP = "third-party screenshot"
AI = "AI-generated study"
OAS = "screenshot of Oath & Action work"
OA = "Oath & Action original"
FF = "font foundry"
UN = "unknown"
STUDY = "study only"
SHIP = "may ship"
SHIPL = "may ship with license text"
UNK = "unknown"

GI = "Google Images viewer chrome (lens icon)"
GT = "Default filename from saving a Google Images thumbnail"
MED = "Medium image filename pattern (1_ plus 22-character ID)"
WIN = "Windows screenshot filename"
FFX = "Firefox page-screenshot filename with the page title"

# ---------------------------------------------------------------- data-viz
DV = {
    1: (SP, "Filename 1000_F_ (Adobe Stock); visible side watermark 'Adobe Stock | #144421710'; IPTC block", STUDY, "Comp preview, no license held (T-ADOBE). Same 'Big Data' title lockup as 60 and 72 (contributor GarryKillian), so probably the same contributor"),
    2: (SP, "Filename 1000_F_; XMP CreatorTool 'Adobe Stock Platform'; visible watermark 'Adobe Stock | #1668742324'", STUDY, "T-ADOBE. Byte-identical to 3"),
    3: (SP, "Filename 1000_F_; XMP CreatorTool 'Adobe Stock Platform'; visible Adobe Stock watermark", STUDY, "T-ADOBE. Duplicate of 2 (same SHA-256); delete one copy in a later tidy"),
    4: (TP, "Filename names UNDG; partnership and initiative counts with a fan chart; JPEG comment 'LEAD Technologies'", STUDY, "T-TP"),
    5: (TP, "'50 Ways to Visualize Data' with Corporate Finance Institute (CFI) logo; numeric download filename", STUDY, "T-TP"),
    6: (TP, "'Everyone talks about System Thinking', credit 'The Curious Society' and its beehiiv newsletter address", STUDY, "T-TP. Rendering suggests it may be generated; unconfirmed"),
    7: (TP, "Behance module filename (project 19648601 plus hash), same project as 33; XMP CreatorTool Photoshop CS6", STUDY, "T-TP. Arc diagram 'WhatsApp, showing 10 topics'"),
    8: (TP, MED + "; news heatmap 'The coronavirus has destroyed America's job market'", STUDY, "T-TP. Uses a red sequential scale on a white ground"),
    9: (TP, MED + "; 'System in Focus Maps by Leyla Acaroglu' with Unschool, Disrupt Design and Circular Futures logos", STUDY, "T-TP. Same author as 13 and 51"),
    10: (TP, MED + "; 'Information Architecture Concept Map'", STUDY, "T-TP"),
    11: (TP, MED + "; purple finance dashboard UI cards", STUDY, "T-TP"),
    12: (TP, MED + "; 'Understanding Internet Search: Concepts, Systems and Processes, 8 August 1999'", STUDY, "T-TP"),
    13: (TP, MED + "; 'Setting a System Boundary', '@leylaacaroglu | circularfutures.co', 'Adapted from ISO 59020'", STUDY, "T-TP"),
    14: (TP, "CMS upload filename (name, hash, hash); 'Parking Lot Monitoring Dashboard' UI", STUDY, "T-TP"),
    15: (SP, "Filename 360_F_ (Adobe Stock preview size); XMP CreatorTool 'Adobe Stock Platform'", STUDY, "T-ADOBE. KPI dashboard UI"),
    16: (TP, "CMS upload filename; gallery of chart-type thumbnails", STUDY, "T-TP"),
    17: (TP, "Short random image-host filename; UK dot map labelled Glasgow, Edinburgh, Manchester, Liverpool, Bristol, London", STUDY, "T-TP"),
    18: (TP, "32-character hash filename; radial personal chart 'This is my life'", STUDY, "T-TP"),
    19: (TP, "Graphic recording 'Rethink Fashion' with RSA logo", STUDY, "T-TP"),
    20: (TP, "Filename names Giorgia Lupi; 'Nuclear Risk: An Expanding Concern' Doomsday Clock graphic", STUDY, "T-TP"),
    21: (TP, "News scatter of IPO values by year, Facebook, Google and Apple labelled, with a log-scale note", STUDY, "T-TP"),
    22: (TP, "Credit 'David McCandless, InformationIsBeautiful.net' visible", STUDY, "T-TP"),
    23: (TP, "2021 macOS screenshot filename plus WordPress size suffix -1025x630, so a web download of someone else's capture; 'The Air We Breathe'", STUDY, "T-TP"),
    24: (TP, WIN + " dated 2026-10-20; 'Different types of charts & diagrams', credit 'The Unspoken Pitch'", STUDY, "T-TP"),
    25: (TP, WIN + "; " + GI + " and a size badge; video-call name tile 'Nathan Lockwood' over the image", STUDY, "T-TP. Shows a private person's name tile; never reproduce"),
    26: (TP, WIN + "; " + GI + ", badge '992 × 590'; The Economist 'Springtime surge', source Johns Hopkins University CSSE; tile 'Nathan Lockwood'", STUDY, "T-TP. Private person's name tile"),
    27: (TP, WIN + "; " + GI + "; 'Why does my dog...' radial charts; tile 'Nathan Lockwood'", STUDY, "T-TP. Private person's name tile"),
    28: (TP, WIN + "; 'Measuring Impact: One Project at a Time' bubble matrix; video tile 'Francis'", STUDY, "T-TP. Private person's video tile"),
    29: (TP, WIN + "; " + GI + "; Miro 'Content & Data Visualization' marketing illustration", STUDY, "T-TP"),
    30: (TP, WIN + "; " + GI + "; 'Natural Increase in the World' scatter with maker credit line", STUDY, "T-TP. Same chart as 64"),
    31: (TP, WIN + "; " + GI + "; 3D iris-data chart with garbled, misspelled axis labels", STUDY, "T-TP. Visual traits of a generated image; never use as evidence"),
    32: (TP, WIN + "; " + GI + "; nautilus-shell glyph chart", STUDY, "T-TP"),
    33: (TP, "Behance module filename, project 19648601 (same as 7); 'Tone-of-voice and relevance analysis'", STUDY, "T-TP"),
    34: (TP, "WordPress size suffix -768x1024; 'Food & Wine Pairing Method' table with publisher seal", STUDY, "T-TP"),
    35: (TP, "Filename names the subject; 'Source: 2017 Forbes Global 2000' on the image", STUDY, "T-TP"),
    36: (TP, "Filename names BuildSys 2026; conference schedule 'Monday, June 22, Workshops & Tutorials'", STUDY, "T-TP"),
    37: (TP, "Data for Progress logo; dumbbell chart 'Changes in Americans' Social Activity, 1995-2026'", STUDY, "T-TP"),
    38: (TP, "CleanShot (macOS app) filename; XMP UserComment 'Screenshot'; Our World in Data chart 'Vaccines reduced measles cases across US states', 'Licensed under CC-BY by the author Fiona Spooner'", STUDY, "T-OWID. The underlying OWID chart is CC BY per its label; this capture is not the licensed file. If a specimen ever needs it, rebuild from OWID's own download and credit OWID and the data providers (Project Tycho, CDC)"),
    39: (TP, "Filename names Wind River; TYPO3 'csm_' image prefix; 'Intelligent Systems Blueprint', WNDR logo", STUDY, "T-TP"),
    40: (TP, "Filename names AnyChart DataViz Weekly; XMP CreatorTool Photoshop CC 2014", STUDY, "T-TP"),
    41: (UN, "Blog header image; XMP CreatorTool Photoshop 22.0; 3D blue ridgeline with floating, meaningless numerals", STUDY, "T-TP. Visual traits of a generated image"),
    42: (TP, "Filename names the Datylon blog; e-car scatter, 'Datasource: kaggle.com'", STUDY, "T-TP"),
    43: (TP, "DrawHappy infographic, drawhappy.com footer; PNG Software 'Adobe ImageReady'", STUDY, "T-TP"),
    44: (SP, "Filename suffix 'stockcake' (StockCake, a site of AI-generated stock images)", STUDY, "T-STOCKCAKE. StockCake states it releases its images into the public domain; the brief still limits references to study, and V5 Photography lists 'generated imagery' under Avoid"),
    45: (TP, "32-character hash filename; 'Transports System' diagram; EXIF DateTime 2008:03:26", STUDY, "T-TP"),
    46: (UN, "Navy and teal chart-type collage, 4537 × 2268, no credit or watermark", STUDY, "T-TP"),
    47: (UN, "Generic filename; dotted-circle cluster tree on cream, no credit", STUDY, "T-TP"),
    48: (SP, "Visible Alamy watermarks and footer 'Image ID: 2B6DBAG, www.alamy.com'; filename ends with the same ID", STUDY, "T-NOLICENSE"),
    49: (SP, "Filename gettyimages-; visible watermark 'gettyimages Credit: andresr'; IPTC creator andresr, Credit 'Getty Images', licensor URL", STUDY, "T-GETTY"),
    50: (TP, "Filename names The Economist; 'Global surface air-temperature anomalies', source Copernicus ERA5", STUDY, "T-TP. Red-blue diverging scale, which brief section 13 rules out for O&A"),
    51: (TP, GT + "; Leyla Acaroglu system-boundary diagram with Unschool, Disrupt Design and Circular Futures logos", STUDY, "T-TP. Same work as 9"),
    52: (TP, GT + "; 'The 10 Most Populous U.S. Cities Every Decade Since 1790' with publisher logo", STUDY, "T-TP"),
    53: (SP, GT + "; visible credit 'designed by freepik'", STUDY, "T-NOLICENSE"),
    54: (UN, GT + "; 3D ridgeline of waste by type, 1935 onward, no credit", STUDY, "T-TP"),
    55: (TP, GT + "; news interactive 'Track National Unemployment, Job Gains and Job Losses', byline Andrew Van Dam and Renee Lightner", STUDY, "T-TP"),
    56: (TP, GT + "; space-debris object chart", STUDY, "T-TP"),
    57: (TP, GT + "; 'Which firms have the best work-life balance?', source CultureX, publisher roundel", STUDY, "T-TP"),
    58: (TP, GT + "; 3D chart 'No More Fish in the Sea', looks like a video still", STUDY, "T-TP"),
    59: (TP, GT + "; poster 'Where does data visualization come from? The emergence of a discipline'", STUDY, "T-TP"),
    60: (SP, GT + "; visible footer 'dreamstime.com, ID 111948405 © Garrykillian'", STUDY, "T-NOLICENSE. Same contributor as 72"),
    61: (TP, GT + "; 'Marketing strategy map example' template", STUDY, "T-TP"),
    62: (TP, GT + "; Commonland 'Why changing legislation alone won't create systemic change', after Donella Meadows", STUDY, "T-TP"),
    63: (UN, GT + "; spiral of numerals with smeared, meaningless figures, no credit", STUDY, "T-TP. Visual traits of a generated image"),
    64: (TP, GT + "; 'Natural Increase in the World' scatter", STUDY, "T-TP. Same chart as 30"),
    65: (SP, GT + "; visible Alamy watermarks, 'Image ID: 2J8M29N'", STUDY, "T-NOLICENSE"),
    66: (SP, GT + "; visible Shutterstock watermarks, contributor 'BlueMorpho', image ID in footer", STUDY, "T-NOLICENSE"),
    67: (TP, GT + "; 'Gestalt's Principles of Visual Perception'", STUDY, "T-TP"),
    68: (TP, GT + "; dot plot of teacher preparedness with significance marks", STUDY, "T-TP"),
    69: (TP, GT + "; isometric yellow-smartphone feature infographic", STUDY, "T-TP"),
    70: (SP, GT + "; visible footer 'depositphotos, Image ID: 224137128'", STUDY, "T-NOLICENSE"),
    71: (SP, "Filename istockphoto-; IPTC creator bgblue, Credit 'Getty Images', web statement iStock license agreement", STUDY, "T-ISTOCK"),
    72: (SP, "Filename istockphoto-; visible 'iStock Credit: GarryKillian'; IPTC creator GarryKillian", STUDY, "T-ISTOCK"),
    73: (TP, "WordPress size suffix -1024x469; multi-line chart 'A Mixed Recovery'", STUDY, "T-TP"),
    74: (TP, "WordPress-style size suffix; radial chart 'Median Age of Population'", STUDY, "T-TP"),
    75: (UN, "Generic filename; pale-blue dashboard mock with illegible pseudo-text and soft 3D card", STUDY, "T-TP. Visual traits of a generated image"),
    76: (TP, "Filename names Tudor government networks; 'Tudor Networks' correspondence graph with credits line", STUDY, "T-TP"),
    77: (TP, "'System Leadership Capabilities', The Systems Sanctuary logo", STUDY, "T-TP"),
}

# ----------------------------------------------------------- design-i-like
def c2pa(date, study):
    return (f"C2PA manifest signed by OpenAI: action c2pa.created {date}, softwareAgent 'ChatGPT' (gpt-image), "
            f"digitalSourceType trainedAlgorithmicMedia, claim generator 'OpenAI Media Service API'; header 'OATH & ACTION / ICON STUDIES', {study}")


DIL = {
    1: (SP, "Marketplace product preview: 'Y2K 2025 Icon Trends', badges '50 ITEM .AI .EPS .PDF .PNG .SVG'; seller not shown", STUDY, "T-NOLICENSE"),
    2: (AI, c2pa("2026-10-19T15:38:38Z", "07 / Abstract Geometric"), STUDY, "T-OPENAI. Icon study 07. Brief section 2: never trace, copy, embed or ship"),
    3: (SP, "Marketplace product preview 'Blue Ink Doodles, Set of 49 Hand-Drawn Doodle Elements', badges EPS SVG AI PNG", STUDY, "T-NOLICENSE"),
    4: (AI, c2pa("2026-10-19T15:20:26Z", "02 / Flat Geo"), STUDY, "T-OPENAI. Icon study 02"),
    5: (AI, c2pa("2026-10-19T15:21:26Z", "03 / Isometric"), STUDY, "T-OPENAI. Icon study 03"),
    6: (AI, c2pa("2026-10-19T15:24:45Z", "06 / Geometric"), STUDY, "T-OPENAI. Icon study 06"),
    7: (OAS, "'ATLAS CONCEPT 00 / THE SHARED LANGUAGE', 'Every line says what happens next, and how sure we are.', O&A wordmark; name 'Picture17' suggests an export from an Office document", SHIP, "T-OA. Rebuild from Concepts V2 rather than ship this raster. Never present as evidence of V7 values"),
    8: (SP, WIN + "; " + GI + "; visible credit 'designed by vexels'", STUDY, "T-NOLICENSE"),
    9: (TP, WIN + "; blue line icons with coral offset fills; source not shown", STUDY, "T-TP"),
    10: (TP, WIN + "; " + GI + "; Bauhaus shape set; source not shown, probably a stock vector", STUDY, "T-TP"),
    11: (TP, WIN + "; waffle chart '45% of respondents prefer Apple', note 'All data in this chart is fictional and for demonstration purposes only'", STUDY, "T-TP"),
    12: (TP, WIN + "; " + GI + "; grid of about 77 blue logo-style marks; source not shown", STUDY, "T-TP. These read as other organizations' marks. Never trace; check new O&A symbols for resemblance"),
    13: (OAS, WIN + " dated 2026-10-20; Concept 03 Field Manual 'Three layers, one machine.' with O&A wordmark", SHIP, "T-OA. Rebuild from source; never as evidence"),
    14: (OAS, FFX + " 'Atlas Design Concepts V2'; Concept 09 The Circuit 'How the whole system is wired.'", SHIP, "T-OA. Rebuild from source; never as evidence"),
    15: (OAS, FFX + " 'Atlas Design Concepts V2'; Concept 10 Who Can Act 'Who can act, and what it would change.'", SHIP, "T-OA. Rebuild from source; never as evidence"),
    16: (OAS, FFX + " 'Atlas Design Concepts V2'; Concept 11 Register 'The whole atlas, line by line.'", SHIP, "T-OA. Rebuild from source; never as evidence"),
    17: (OAS, FFX + " 'Atlas Design Concepts V2'; Concept 11 Register detail 'Elections and representation'", SHIP, "T-OA. Rebuild from source; never as evidence"),
    18: (TP, "Icon style comparison Line, Duo, Solid, Flat; source not shown", STUDY, "T-TP"),
    19: (AI, "C2PA manifest signed by OpenAI: action c2pa.created 2026-10-15T16:39:14Z, softwareAgent 'ChatGPT' (gpt-image), digitalSourceType trainedAlgorithmicMedia; generated mock of the 'Who Do They Answer To?' home page with generated editorial illustrations", STUDY, "T-OPENAI. Shows '740 sources'; V7 meta.counts gives 1,099 sources. Never use as evidence or as a layout to copy"),
    20: (TP, MED + "; bubble diagram 'tracker mvp, the system, component library, pattern library, design system'", STUDY, "T-TP"),
    21: (TP, MED + "; pill diagram 'Understanding, Alignment, Optimisation'", STUDY, "T-TP"),
    22: (TP, "Webflow-style asset filename (24-character site ID plus random string); UI collage 'Building a design system.'", STUDY, "T-TP"),
    23: (TP, "'Figure 1. Eight base layers of The National Map' (USGS); EXIF Artist 'Sexton, Pamela Ann'", STUDY, "T-USGS. Probably a US federal work with no US copyright; not verified for this figure"),
    24: (TP, WIN + "; " + GI + "; causal loop 'Challenges & Resources to Sofia's Wellbeing' with a portrait illustration", STUDY, "T-TP"),
    25: (TP, WIN + "; " + GI + "; causal loop diagram (Target, Workload, Stress, Productivity) with S/O polarity legend", STUDY, "T-TP"),
    26: (TP, WIN + "; " + GI + ", badge '760 × 418'; widely circulated Afghanistan counterinsurgency dynamics diagram", STUDY, "T-TP"),
    27: (TP, WIN + "; " + GI + "; sketchnote 'Unit 1, Political Systems, Regimes & Governments, AP Comparative Government'", STUDY, "T-TP"),
    28: (TP, WIN + "; map legend and map filter UI panels", STUDY, "T-TP"),
    29: (TP, WIN + "; " + GI + "; 'Quality reporting automation business architecture' with 'ProcessOn' watermark", STUDY, "T-TP"),
    30: (TP, WIN + "; " + GI + ", badge '1,999 × 1,024'; design-system 'Foundations' overview", STUDY, "T-TP"),
    31: (TP, FFX + " 'Organisational Transformation Systems Mapping'; Dutch-language organisation map", STUDY, "T-TP"),
    32: (TP, "UUID 'cover' filename; whiteboard architecture diagram (Node, Express, Prisma, MongoDB)", STUDY, "T-TP"),
    33: (TP, "Filename names Capsifi; JPEG comment 'LEAD Technologies'; operating-model diagram", STUDY, "T-TP"),
    34: (TP, "Charts 'Style guide-based products' and 'Design System-based products'", STUDY, "T-TP"),
    35: (SP, GT + "; 'Digital System Abstract Background' with an 'EPS 10' badge, the layout of a stock vector preview; marketplace not shown", STUDY, "T-NOLICENSE"),
    36: (TP, GT + "; value chain map, 'Source: Participatory Market System Development (PMSD) Roadmap'", STUDY, "T-TP"),
    37: (TP, GT + "; 'Systeemkaart Tapijt Sector' metro-style system map", STUDY, "T-TP"),
    38: (TP, "PNG Description 'Created with Enterprise Architect (Build: 1600)'; layered architecture diagram", STUDY, "T-TP"),
    39: (TP, "Blog CMS filename for 'What are modular blockchains'; green isometric cubes", STUDY, "T-TP. Same illustration style as 42, 46, 49"),
    40: (AI, c2pa("2026-10-19T15:19:54Z", "01 / Y2K"), STUDY, "T-OPENAI. Icon study 01"),
    41: (OAS, "Concept 09 The Circuit 'The system runs in one long loop.' with O&A wordmark; '(1)' duplicate-download suffix", SHIP, "T-OA. Rebuild from source; never as evidence"),
    42: (TP, "Green isometric blockchain cubes on black; no credit", STUDY, "T-TP. Same style as 39"),
    43: (SP, "Filename gettyimages-; visible 'gettyimages Credit: Pikusisi-Studio'; IPTC creator, Credit 'Getty Images'", STUDY, "T-GETTY"),
    44: (SP, "Filename gettyimages-; visible 'gettyimages Credit: fairywong'; IPTC creator, Credit 'Getty Images'", STUDY, "T-GETTY"),
    45: (UN, GT + "; Memphis-style geometric element set laid out like a stock vector preview; no credit or watermark", STUDY, "T-TP. Probably stock; marketplace not identified"),
    46: (TP, GT + "; green isometric cube illustration", STUDY, "T-TP. Same style as 39"),
    47: (SP, "Filename istockphoto-; IPTC creator Astrolounge, Credit 'Getty Images', web statement iStock license agreement", STUDY, "T-ISTOCK"),
    48: (SP, "Filename pattern of a Freepik preview (slug, underscore, two numbers), 740 px wide", STUDY, "T-NOLICENSE. Marketplace inferred from the filename only"),
    49: (TP, "Blog CMS filename for 'What are blockchain sequencers and why do they matter'", STUDY, "T-TP. Same style as 39"),
}

ICON = {
    1: (AI, "Probable. Same 'OATH & ACTION / ICON STUDIES' template, four-pillar layout and 3:4 ratio as the C2PA-signed ChatGPT sheets 01, 02, 03, 06, 07; file stripped of all metadata (PNG holds only IHDR, IDAT, IEND); about half the 1086 × 1448 of the signed sheets", STUDY, "T-OPENAI if confirmed. Dustin to confirm the tool, date and account terms. Brief section 11 uses it as direction only"),
    2: (AI, "Probable. Same template; its twelve subjects and 'Civic life, connected' strip repeat study 07 (C2PA-signed ChatGPT) word for word; WebP holds only VP8X, ICCP and VP8 chunks", STUDY, "T-OPENAI if confirmed. Dustin to confirm the tool and terms"),
    3: (AI, "Probable. Same template and pillar layout as studies 02, 03, 06; PNG holds only IHDR, IDAT, IEND", STUDY, "T-OPENAI if confirmed. Dustin to confirm the tool and terms"),
}


def img_rows(set_key, set_label, table):
    rows = []
    recs = {r["sheet_number"]: r for r in META[set_key]}
    for n, rel in enumerate(IDX[set_key], 1):
        origin, evidence, permitted, notes = table[n]
        r = recs[n]
        assert r["file"] == rel, (r["file"], rel)
        dims = f"{r.get('format')} {r.get('width')} × {r.get('height')}. "
        rows.append((f"{set_key}-{n:02d}", rel, set_label, origin, dims + evidence, permitted, notes))
    return rows


def esc(s):
    return str(s).replace("|", "\\|")


def font_evidence(rec):
    n = rec["names"]
    parts = [f"Name table: copyright '{n.get('copyright', '')}'", f"version '{n.get('version', '')}'"]
    parts.append(f"license URL '{n['license_url']}'" if n.get("license_url") else "no license URL (ID 14)")
    parts.append("license description present" if n.get("license_description") else "no license description (ID 13)")
    parts.append(f"vendor {rec.get('vendor_id')}")
    parts.append("fsType 0, installable embedding with no restriction" if rec.get("fsType") == 0 else f"fsType {rec.get('fsType')}, {rec.get('fsType_meaning')}")
    parts.append(f"{rec.get('glyphs'):,} glyphs")
    parts.append(f"SHA-256 {rec['sha256'][:12]}")
    return "; ".join(parts)


def main():
    rows = []
    rows += img_rows("data-viz", "data-viz", DV)
    rows += img_rows("design-i-like", "design-i-like", DIL)
    rows += img_rows("icon-studies", "icon-studies", ICON)

    # fonts embedded in V5 Polished (extracted files)
    for i, rec in enumerate(FONTS["v5_polished_extracted"], 1):
        fam = rec["names"].get("copyright", "")
        lora = "Lora" in fam
        foundry = "Cyreal / The Lora Project Authors" if lora else "The Inter Project Authors (Rasmus Andersson, RSMS)"
        note = ("OFL-1.1 (T-OFL, T-LORA). Copyright string reserves the name 'Lora': ship these files unmodified (match to the release binaries not yet confirmed), or rename any subset. "
                if lora else
                ("OFL-1.1 (T-OFL, T-INTERTIGHT). " if "inter-tight" in fam else "OFL-1.1 (T-OFL, T-INTER). ")
                + "No Reserved Font Name in the copyright string. ")
        note += "Same bytes embedded in V5 and V4.2. V5 Polished shows no OFL text and no copyright notice; the copyright line exists only inside the binary"
        rows.append((f"font-{i:02d}", rec["file"], "font", FF, f"{foundry}. " + font_evidence(rec), SHIPL, note))

    # fonts in other sources (distinct binaries not already listed)
    seen = {r["sha256"] for r in FONTS["v5_polished_extracted"]}
    avs_files = {}
    for f in (ROOT / "work/extract/atlas-visual-system/fonts").glob("*"):
        avs_files[hashlib.sha256(f.read_bytes()).hexdigest()] = str(f.relative_to(ROOT))
    j = len(FONTS["v5_polished_extracted"])
    by_hash = collections.OrderedDict()
    for src, fonts in FONTS["sources"].items():
        for rec in fonts:
            if rec["sha256"] in seen:
                continue
            by_hash.setdefault(rec["sha256"], {"rec": rec, "where": []})
            by_hash[rec["sha256"]]["where"].append((src, rec.get("css_family"), rec.get("css_weight"), rec.get("css_style")))
    for h, item in by_hash.items():
        j += 1
        rec = item["rec"]
        srcs = sorted({w[0] for w in item["where"]})
        css = sorted({f"'{w[1]}' {w[2]} {w[3]}" for w in item["where"]})
        if h in avs_files:
            path = avs_files[h] + " (also nested in the four V5 Polished SVGs)"
        else:
            path = " and ".join(f"source/{s}" for s in srcs) + f" (data URI, CSS {', '.join(css)})"
        n = rec["names"]
        cr = n.get("copyright", "")
        if "URW" in cr:
            foundry = "URW++ Design & Development (base35 set, 2016 build)"
            permitted = UNK
            note = (f"T-URW. Served under the alias {', '.join(css)}, so readers and builders never see the real name. "
                    "fsType 4 asks for preview-and-print embedding only. Artifex distributes the set under AGPL-3.0 with a font exception written for PostScript and PDF; web embedding is not addressed. Not a brand font: replace in V6")
        elif "Lora" in cr:
            foundry = "Cyreal / The Lora Project Authors"
            permitted = UNK
            note = (f"T-OFL, T-LORA. {rec.get('flavor').upper()} subset of {rec.get('glyphs')} glyphs that keeps the Reserved Font Name 'Lora'. "
                    "The OFL FAQ treats a pre-subset as a Modified Version that may not use the RFN. Do not carry into V6; embed the full files from V5 Polished or rename")
        else:
            foundry = "The Inter Project Authors (Rasmus Andersson, RSMS)"
            permitted = SHIPL
            extra = ""
            if any(w[2] == "700" for w in item["where"]) and "ExtraBold" in n.get("full_name", ""):
                extra = " The Concepts files map CSS weight 700 to this ExtraBold file as well as 800."
            note = (f"T-OFL, {'T-INTERTIGHT' if 'tight' in cr.lower() else 'T-INTER'}. {rec.get('flavor').upper()} subset of {rec.get('glyphs')} glyphs; "
                    "subsetting stripped the license URL. No RFN declared, so a subset may keep the name; ship OFL text and the copyright line." + extra)
        rows.append((f"font-{j:02d}", path, "font", FF, f"{foundry}. " + font_evidence(rec), permitted, note))

    # embedded images in V5 Polished
    svgs = sorted((ROOT / "work/extract/v5-polished/images").glob("*.svg"))
    for k, f in enumerate(svgs, 1):
        raw = f.read_text(encoding="utf-8", errors="replace")
        import re
        title = re.search(r"<title[^>]*>([^<]*)", raw).group(1)
        desc = re.search(r"<desc[^>]*>([^<]*)", raw).group(1)
        ev = (f"SVG 1440 wide, no raster content, no generator metadata. Title '{title}'. Desc: '{desc}' "
              "The same file is embedded in the Atlas Visual System. Embeds three WOFF subsets (Inter 400 and 600, Inter Tight 800)")
        rows.append((f"image-{k:02d}", str(f.relative_to(ROOT)), "embedded image", OA, ev, SHIPL,
                     "T-OA plus T-OFL for the nested fonts. Every V7 ID it cites occurs in the V7 JSON; values not reconciled here (dataviz lead). Never present as independent evidence"))

    # counts
    by_set = collections.defaultdict(collections.Counter)
    by_set_use = collections.defaultdict(collections.Counter)
    for row in rows:
        by_set[row[2]][row[3]] += 1
        by_set_use[row[2]][row[5]] += 1
    total_origin = collections.Counter(r[3] for r in rows)
    total_use = collections.Counter(r[5] for r in rows)
    ai_traits = [r[0] for r in rows if "generated image" in r[6] or "may be generated" in r[6]]

    OUT.write_text(render(rows, by_set, by_set_use, total_origin, total_use, ai_traits), encoding="utf-8")
    print("rows", len(rows))
    print("origin", dict(total_origin))
    print("use", dict(total_use))
    for s in by_set:
        print(s, dict(by_set[s]), dict(by_set_use[s]))
    print("third-party items with generated traits:", ai_traits)


ORIGINS = [SP, TP, AI, OAS, OA, FF, UN]
USES = [STUDY, SHIP, SHIPL, UNK]


def render(rows, by_set, by_set_use, total_origin, total_use, ai_traits):
    out = []
    w = out.append
    w("# Rights Ledger")
    w("")
    w("Oath & Action Brand Guide, Edition 06. Started in Phase 0 by the research lead on October 20, 2026. "
      "Living ledger: Phase 1 extends it, and every later phase adds each new font, photograph, generated image and reference it uses.")
    w("")
    w("Every row was checked on October 20, 2026. Each row's Notes name a terms code; the Terms key below gives the URL, what the terms say and how I checked them. "
      "Rows for reference images are numbered as on the contact sheets in `work/boards/screens/references/` (index.json). "
      "Paths are relative to the project root. Machine-readable evidence: `work/handoffs/phase-0/20261020_Rights-Image-Metadata.json` and "
      "`work/handoffs/phase-0/20261020_Rights-Font-Name-Tables.json`, made by the scripts in `work/build/scripts/phase-0/`.")
    w("")
    w("## Rule that governs every reference")
    w("")
    w("Master Brief section 2: reference images are for principles and mechanisms only. Study them; never trace, copy, embed or ship them. "
      "Final marks are authored vectors. A watermarked stock file is a comp preview, and the agency terms checked here allow comps only for internal layout tests.")
    w("")
    w("## Key")
    w("")
    w("| Likely origin | Meaning |")
    w("|---|---|")
    w("| stock preview | A watermarked or comp file from a stock agency or asset marketplace, identified by filename pattern, watermark or IPTC credit |")
    w("| third-party screenshot | A screenshot or web download of someone else's work |")
    w("| AI-generated study | An image generated for Oath & Action with an image model |")
    w("| screenshot of Oath & Action work | A capture of a supplied Oath & Action file, such as Concepts V2 |")
    w("| Oath & Action original | An asset authored for Oath & Action and embedded in a supplied file |")
    w("| font foundry | A typeface from its foundry or project |")
    w("| unknown | No credit, watermark or metadata names the maker |")
    w("")
    w("| Permitted use | Meaning |")
    w("|---|---|")
    w("| study only | Principles only. Never trace, copy, embed or ship |")
    w("| may ship | Oath & Action may publish it, subject to the note |")
    w("| may ship with license text | May ship if the named license text and notices travel with it |")
    w("| unknown | Do not ship until the open question in the note is answered |")
    w("")
    w("## Terms key")
    w("")
    w("Checked October 20, 2026. This environment blocks page fetches, so each entry rests on WebSearch results from the official domain, on metadata inside the files, or on both. "
      "I did not open any of these pages; Phase 1 opens each and quotes exact wording only after reading it.")
    w("")
    w("| Code | Source and URL | What it says | How checked |")
    w("|---|---|---|---|")
    terms = [
        ("T-ADOBE", "Adobe Stock Product Specific Terms (version dated August 8, 2025). https://www.adobe.com/cc-shared/assets/pdf/legal/servicetou/stock-product-specific-terms-en-us-20250808.pdf",
         "A comp may be used for preview only, for up to 90 days from download, and never in final production", "Official-domain search snippet"),
        ("T-ISTOCK", "iStock Content License Agreement. https://www.istockphoto.com/legal/license-agreement",
         "Watermarked comps are for test or sample layout for 30 days and may not appear in final or publicly available material", "Official-domain search snippet; IPTC web statement in files 71, 72 and design-i-like 47 points here"),
        ("T-GETTY", "Getty Images EULA. https://www.gettyimages.com/eula",
         "Not read. The URL comes from the IPTC web statement inside each gettyimages- file", "File metadata only"),
        ("T-NOLICENSE", "Alamy https://www.alamy.com, Shutterstock https://www.shutterstock.com, Dreamstime https://www.dreamstime.com, Depositphotos https://depositphotos.com, Freepik https://www.freepik.com, Vexels https://www.vexels.com, and unnamed marketplaces",
         "Terms not checked. Each file is a watermarked or credited preview, so no license is held", "Visible watermark or credit"),
        ("T-STOCKCAKE", "StockCake FAQ and Terms. https://stockcake.com/info/faq and https://stockcake.com/info/terms",
         "StockCake says AI generates all its images and that it releases them into the public domain", "Official-domain search snippet"),
        ("T-OPENAI", "OpenAI Terms of Use https://openai.com/policies/row-terms-of-use/ and Services Agreement https://openai.com/policies/services-agreement/; US Copyright Office, Copyright and Artificial Intelligence, Part 2 (January 29, 2025) https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf; IPTC Digital Source Type https://cv.iptc.org/newscodes/digitalsourcetype/",
         "OpenAI assigns Output to the user to the extent the law allows and bars presenting output as human-made. The Copyright Office concludes that prompts alone do not make the user an author. IPTC trainedAlgorithmicMedia means 'Created using Generative AI'", "Official-domain search snippets; C2PA manifests read from the files"),
        ("T-OFL", "SIL Open Font License 1.1 https://openfontlicense.org/open-font-license-official-text/; OFL-FAQ https://openfontlicense.org/ofl-faq/; Webfonts and Reserved Font Names https://openfontlicense.org/webfonts-and-reserved-font-names/",
         "Use, embedding and redistribution are allowed, including bundled with commercial software. Each copy keeps the copyright notice and the license. Fonts may not be sold alone. A Modified Version may not use a Reserved Font Name. The FAQ treats subsetting as modification", "Official-domain search snippets; license URLs in the name tables"),
        ("T-INTER", "Inter project. https://github.com/rsms/inter/ and https://rsms.me/inter/",
         "Inter is free and open source under OFL 1.1. The FAQ says 'Inter is a trademark of Rasmus Andersson (RSMS)'", "Official-domain search snippets; name tables"),
        ("T-INTERTIGHT", "Inter Tight. https://fonts.google.com/specimen/Inter+Tight and https://github.com/googlefonts/inter-gf-tight",
         "OFL 1.1; the Google Fonts repository was archived in February 2024", "Official-domain search snippets; name tables"),
        ("T-LORA", "Lora project. https://github.com/cyrealtype/Lora-Cyrillic, https://www.cyreal.org/license/, https://fonts.google.com/specimen/Lora",
         "OFL 1.1, with Reserved Font Name 'Lora'", "Official-domain search snippets; name tables"),
        ("T-URW", "URW base35 fonts, Artifex. https://github.com/ArtifexSoftware/urw-base35-fonts/blob/master/LICENSE",
         "AGPL-3.0 with a font exception that lets the fonts be embedded in PostScript or PDF files", "Official-domain search snippet; name tables"),
        ("T-OWID", "Our World in Data FAQs. https://ourworldindata.org/faqs",
         "OWID's own visualizations, data and articles are CC BY; third-party data keeps its own license", "Official-domain search snippet"),
        ("T-USGS", "17 U.S.C. section 105. https://www.copyright.gov/title17/92chap1.html#105",
         "Works of the US federal government have no US copyright. Not confirmed for this figure", "Not checked today"),
        ("T-OA", "Oath & Action, Dustin Cathcart, Founder and Editor", "Oath & Action work. Dustin to confirm authorship and that no third-party material is inside", "Supplied files"),
        ("T-TP", "The maker named in Evidence, where visible", "No license held. Copyright stays with the maker", "Visual review and file metadata"),
    ]
    for t in terms:
        w("| " + " | ".join(esc(x) for x in t) + " |")
    w("")
    w("## Counts")
    w("")
    sets = ["data-viz", "design-i-like", "icon-studies", "font", "embedded image"]
    w("| Set | Rows | " + " | ".join(ORIGINS) + " |")
    w("|---|---|" + "---|" * len(ORIGINS))
    for s in sets:
        w(f"| {s} | {sum(by_set[s].values())} | " + " | ".join(str(by_set[s][o]) for o in ORIGINS) + " |")
    w(f"| All | {sum(total_origin.values())} | " + " | ".join(str(total_origin[o]) for o in ORIGINS) + " |")
    w("")
    w("| Set | " + " | ".join(USES) + " |")
    w("|---|" + "---|" * len(USES))
    for s in sets:
        w(f"| {s} | " + " | ".join(str(by_set_use[s][u]) for u in USES) + " |")
    w("| All | " + " | ".join(str(total_use[u]) for u in USES) + " |")
    w("")
    w(f"Third-party or unknown images that show visual traits of a generated image: {', '.join(ai_traits)}.")
    w("")
    w("## Ledger")
    w("")
    for s in sets:
        w(f"### {s}")
        w("")
        w("| # | File | Set | Likely origin | Evidence | Permitted use | Notes |")
        w("|---|---|---|---|---|---|---|")
        for r in rows:
            if r[2] == s:
                w(f"| {r[0]} | `{esc(r[1])}` | {r[2]} | {r[3]} | {esc(r[4])} | {r[5]} | {esc(r[6])} |")
        w("")
    w("## Could not verify")
    w("")
    for line in [
        "No terms page was opened. WebFetch fails here and curl gets a 403 from the proxy. Every license statement in the Terms key rests on official-domain search snippets, so exact wording is unquoted until Phase 1 reads the pages.",
        "Whether the nine V5 Polished font files match the official release binaries byte for byte. I could not download the releases to compare checksums.",
        "Whether Inter's own OFL.txt declares a Reserved Font Name. The name tables declare none, and one third-party fork's README claims one.",
        "Which tool and which account plan made icon studies 04, 05 and 08. Their files carry no metadata. The attribution to ChatGPT is an inference from the shared template and from study 07's identical subject list.",
        "The prompts, dates and account terms behind the six C2PA-signed ChatGPT images. The manifests give the creation time and tool only. I read the manifests as strings and did not validate the signatures.",
        "The owner of every third-party image whose maker is not visible, including all rows marked unknown.",
        "Whether the 'Nathan Lockwood' and 'Francis' tiles in data-viz 25 to 28 come from a call Dustin attended or from a published video.",
        "The license terms for Alamy, Shutterstock, Dreamstime, Depositphotos, Freepik, Vexels and Getty Images previews. None are needed for study use, and none permit shipping a watermarked preview.",
        "Whether the URW font exception covers web embedding in HTML, and whether Atlas V7 needs any license text at all if V6 replaces those fonts.",
        "The authorship of Concepts V2 and of the Atlas Visual System diagrams. I treated them as Oath & Action work because Dustin supplied them as such.",
    ]:
        w(f"- {line}")
    w("")
    return "\n".join(out)


if __name__ == "__main__":
    main()
