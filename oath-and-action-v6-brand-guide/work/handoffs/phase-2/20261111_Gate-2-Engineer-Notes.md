# Gate 2 engineer notes: the preview build

Oath & Action Edition 06, Phase 2, November 11, 2026. Task 3 of `20261111_Gate-2-Brief.md`. The engineer started from commit 043ad4d8; `guide_build.py --strict` passed as committed.

## Status

- Fonts fetched and checked: six WOFF2 files, 329,896 bytes, with three OFL texts and the manifest, under `work/build/assets/fonts/` (`fonts_fetch.py`).
- The editor's `where-to-start.json` and notes landed before the build work began, so no placeholder was needed on the page.
- Now: the build's front page, embedded fonts, license disclosures and edition line; then the checks.

## Fonts (D2-1697)

- **Request.** `fonts_fetch.py` asks Google Fonts for the page's own stylesheet, `Inter+Tight:wght@600;700;800`, `Inter:wght@400;500;600;700`, `Lora:ital,wght@1,400;1,500`, with a desktop Chrome 153 user agent, the version of the Chromium the checks run in.
- **What Google serves.** One variable WOFF2 file per family, style and script subset; every weight of a style points at the same file. Lora comes in italic only, as the page asks.
- **Subsets kept: latin and latin-ext.** A script read every character of the frozen page's text, alt text and names against Google's unicode ranges: all 103 distinct characters sit in latin, except five (→, ■, ▲, ▼, ✓) that only Lora's math and symbols subsets cover. A rendered run of the frozen page with Google Fonts loaded only the latin face of each family at 1440 and 390 px, so no Lora-set text uses those five; Inter text draws them from the system's fallback today and still will. latin-ext is kept for names with accents a later chapter may print (Polish, Czech, Turkish, Vietnamese names partly). Left out: cyrillic, cyrillic-ext, greek, greek-ext and vietnamese for both Inters; cyrillic, cyrillic-ext, math, symbols and vietnamese for Lora. Nothing on the page uses them.
- **Files.** Saved byte for byte as served, under dated names (`inter/20261111_Inter-Latin.woff2` and the rest); the manifest gives each file's URL, bytes, SHA-256, unicode range, weights and date. Each family folder holds its `OFL.txt` as published in google/fonts.

| File | Bytes |
|---|---|
| inter/20261111_Inter-Latin.woff2 | 48,256 |
| inter/20261111_Inter-Latin-Ext.woff2 | 85,068 |
| inter-tight/20261111_Inter-Tight-Latin.woff2 | 44,872 |
| inter-tight/20261111_Inter-Tight-Latin-Ext.woff2 | 89,800 |
| lora/20261111_Lora-Italic-Latin.woff2 | 40,772 |
| lora/20261111_Lora-Italic-Latin-Ext.woff2 | 21,128 |
| Six files | 329,896 |

### Rights ledger rows for the main session (`work/research/*_Rights-Ledger.md`)

| ID | Item | Source | License or terms | May ship |
|---|---|---|---|---|
| T-INTER | Inter, variable WOFF2, latin and latin-ext subsets, weights 400 to 700, unmodified | Google Fonts (fonts.gstatic.com, v20), fetched November 11, 2026; license text from github.com/google/fonts, ofl/inter/OFL.txt | SIL Open Font License 1.1; Copyright 2020 The Inter Project Authors (https://github.com/rsms/inter); no reserved font name | Yes, embedded in the guide and in the asset package's fonts folder, with OFL.txt beside the files |
| T-INTERTIGHT | Inter Tight, variable WOFF2, latin and latin-ext subsets, weights 600 to 800, unmodified | Google Fonts (fonts.gstatic.com, v9), fetched November 11, 2026; license text from ofl/intertight/OFL.txt | SIL Open Font License 1.1; Copyright 2022 The Inter Project Authors (https://github.com/rsms/inter-tight); no reserved font name | Yes, as Inter |
| T-LORA | Lora Italic, variable WOFF2, latin and latin-ext subsets, weights 400 and 500, unmodified | Google Fonts (fonts.gstatic.com, v37), fetched November 11, 2026; license text from ofl/lora/OFL.txt | SIL Open Font License 1.1; Copyright 2011 The Lora Project Authors (https://github.com/cyrealtype/Lora-Cyrillic), with Reserved Font Name "Lora" | Yes, unmodified only under the name Lora; a changed version may not use the name |

## Routine calls

