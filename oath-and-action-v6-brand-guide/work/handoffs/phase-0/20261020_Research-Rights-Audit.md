# Research Rights Audit, Phase 0

Research lead, October 20, 2026. Full ledger, 157 rows: `work/research/20261020_Rights-Ledger.md`. Nothing in `source/` or `work/extract/` was changed.

I viewed all ten contact sheets and opened 17 unclear files in full. Scripts read every image's metadata and C2PA manifest (the signed record some tools attach to say how an image was made), and the name table of every embedded font.

## Counts

| Origin | Rows | | Permitted use | Rows |
|---|---|---|---|---|
| Stock preview | 22 | | Study only | 122 |
| Third-party screenshot or download | 84 | | May ship | 7 |
| AI-generated study | 9 | | May ship with license text | 22 |
| Screenshot of Oath & Action work | 7 | | Unknown | 6 |
| Oath & Action original (V5 SVGs) | 4 | | | |
| Font foundry | 24 | | | |
| Unknown | 7 | | | |

Six third-party or unknown images show traits of generated images (data-viz 06, 31, 41, 44, 63, 75).

## Never ship

- The 22 stock previews: Adobe Stock 4, iStock 3, Getty Images 3, Alamy 2, Freepik 2, unnamed marketplaces 3, and one each from Shutterstock, Dreamstime, Depositphotos, Vexels and StockCake. Adobe Stock and iStock terms allow watermarked comps for internal layout tests only.
- The 84 third-party images and 7 unknowns. Data-viz 25 to 28 also show video-call name tiles of private people.
- The nine AI-generated images, as artwork or as evidence. The ChatGPT atlas mockup (design-i-like 19) says "740 sources"; V7 `meta.counts` gives 1,099.
- The four Atlas V7 fonts and the two Lora subsets in Concepts V1 and V2, until the font questions below are settled.

Data-viz 38 shows an Our World in Data chart labeled CC BY; a specimen would rebuild it from OWID's own download, with credit.

## Dustin must confirm

1. **Icon studies.** Six images carry signed C2PA manifests naming ChatGPT (gpt-image) as the creating tool, with IPTC source type "trainedAlgorithmicMedia" (created using generative AI): studies 01, 02, 03, 06 and 07, created October 19, 2026 between 15:19 and 15:38 UTC, and the atlas mockup, created October 15. Studies 04, 05 and 08 in `source/icon-studies/` carry no metadata. They share the sheet template, and study 05 repeats study 07's twelve subjects word for word, so I infer the same tool. Please confirm the tool for 04, 05 and 08, your ChatGPT plan, and whether any outside image went into a prompt. OpenAI's terms assign output to the user as far as the law allows, and the US Copyright Office concludes that prompts alone do not make a user the author. Oath & Action could not claim these sheets as its artwork, so final marks stay authored vectors.
2. **Authorship of Concepts V2 and the Atlas Visual System diagrams**, which I treated as Oath & Action work (7 screenshots, 4 SVGs).
3. **The source of data-viz 25 to 28**: a call you attended or a published video.
4. **Stock licenses.** I assumed Oath & Action holds none.

## Font finding

V5 Polished embeds nine complete TTF files: Inter 400, 600, 700 (version 4.001), Inter Tight 400, 600, 800 (version 3.004), and Lora Bold, Italic and Medium Italic (version 3.008). V5 and V4.2 embed identical bytes.

The name tables carry these copyright lines: "Copyright 2016 The Inter Project Authors (https://github.com/rsms/inter)", "Copyright 2022 The Inter Project Authors (https://github.com/rsms/inter-tight)", and "Copyright 2011 The Lora Project Authors (https://github.com/cyrealtype/Lora-Cyrillic), with Reserved Font Name "Lora"." License URLs read https://openfontlicense.org (Inter) and https://scripts.sil.org/OFL (Inter Tight, Lora). No file carries the license text (name ID 13). All set fsType 0, which places no limit on embedding.

Official-domain search results (rsms.me, github.com/rsms/inter, fonts.google.com, github.com/cyrealtype, cyreal.org) put all three families under the SIL Open Font License 1.1. The OFL permits embedding and redistribution, including with commercial products. Each copy must keep the copyright notice and the license, the fonts may not be sold alone, and a modified version may not use a Reserved Font Name. The Inter FAQ adds that "Inter is a trademark of Rasmus Andersson (RSMS)".

What must ship: the OFL 1.1 text with the three copyright lines beside any font file in the asset package, and a font credits and licenses note in the guide.

V5 Polished credits fonts in one Standards row: "Fonts InterTight-800, Inter-400/600/700, LoraItalic-400/500, licensed embedded". It omits Inter Tight 400 and 600 and Lora Bold, names no license and shows no copyright notice. No other license wording appears in the file, and it has no download links.

Elsewhere, Concepts V1 and V2 embed WOFF2 subsets of Lora that keep the reserved name, and the OFL FAQ treats a pre-built subset as a modified version. Atlas V7 embeds four URW++ fonts (Nimbus Sans Regular and Bold, Nimbus Sans Narrow Bold, Nimbus Mono PS) renamed in CSS as "Atlas Display", "Atlas Sans" and "Atlas Mono". They set fsType 4 (preview and print embedding) and carry no license URL. Artifex distributes the set under AGPL-3.0 with a font exception written for PDF and PostScript. They sit outside the brand type system, and V6 should replace them.

## Photography in V5

V5 has no photographs, and no source file embeds a raster image. The Photography chapter shows its ten-frame commissioned shot list as flat CSS panels, Stone for natural color and Charcoal for duotone, each with a caption. Each panel carries `role="img"` and a label that begins "Photograph:", so a screen reader announces a photograph that is absent. The three testimonial cards (Maria T., Derek O., Priya N.) carry no illustrative label. The Avoid list bans "generated imagery", while brief section 16 allows labeled generated conceptual illustration; Phase 1 should settle the rule.

## Phase 1 research tasks

1. Open every page in the ledger's Terms key and quote exact wording.
2. Download the Inter, Inter Tight and Lora releases whose version strings match, compare checksums with the V5 Polished files, and read Inter's own OFL.txt for a Reserved Font Name.
3. Draft the font license bundle and credits note with the engineer.
4. Settle the URW question for Atlas V7 or record the replacement.
5. Record your icon-study answers, with tool, date, prompt and terms, as brief section 16 requires.
6. Compare every new symbol with design-i-like 12 and the stock icon sets before it ships.
7. Define the photography rights record (credit, consent, release, caption).
8. Rights-check the 74 other SVGs in the Atlas Visual System.

## Verified and not verified

Verified: origin and permitted use for every reference image; six C2PA manifests, read as strings without signature validation; name tables and checksums for all 24 font binaries; no raster images in any source.

Not verified: exact license wording (page fetches are blocked, so terms rest on official-domain search snippets); whether the V5 fonts match the release files; the tool behind studies 04, 05 and 08; makers of uncredited images; the URW exception's reach on the web.

## Change log

Created: `work/research/20261020_Rights-Ledger.md`; `work/handoffs/phase-0/20261020_Research-Rights-Audit.md`, `20261020_Rights-Image-Metadata.json`, `20261020_Rights-Font-Name-Tables.json`; scripts in `work/build/scripts/phase-0/` (`image_metadata.py`, `c2pa_strings.py`, `font_names.py`, `svg_fonts.py`, `build_rights_ledger.py`). Modified: none. Installed fonttools and brotli with `pip --user`.
