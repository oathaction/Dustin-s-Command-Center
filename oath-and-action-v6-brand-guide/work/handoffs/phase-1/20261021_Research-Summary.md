# Research summary, Phase 1

Research lead, October 21, 2026, for the creative director, design director and editor. Full ledger: `work/research/20261021_Research-Ledger.md`. Rights: a dated section at the end of `work/research/20261020_Rights-Ledger.md`.

Method: page fetches still fail (ENOTFOUND today), so I ran 97 searches limited to official domains. No page was read; every [snippet] quote needs a page check before the guide prints it.

## What matters most for strategy and identity

1. **A single mark can carry the brand idea, if the brand teaches it.** The 19th puts an asterisk in its logo to acknowledge the limits of the 19th Amendment, and its strategic plan includes a campaign to re-teach that meaning. GOV.UK's refresh of June 25, 2025 made the dot between GOV and UK the light-blue joint of its wordmark. For DC-05, explain the ampersand's meaning in plain words where a reader first meets it, and give the hinge diagram one consistent job.

2. **Common ground works best as something a reader can try.** The strongest tools ask for a commitment, then show a result. More in Common's Perception Gap Quiz asks you to guess the other side's views, then shows them. The Program for Public Consultation gives the strongest arguments for and against, then shows both parties' majorities side by side. Stanford's America in One Room measures views before and after deliberation. Pew's 2026 typology sorts the public into nine groups and is titled "Beyond Red vs. Blue". The strategy can pick one as the house format for "you & me" pieces.

3. **Red and blue split the field.** AllSides encodes the spectrum in blue, purple and red, with published hex values. The League of Women Voters' 2024 standards require LWV Red and LWV Blue. Braver Angels labels participants Red and Blue in equal numbers and now debates whether the binary helps. Brief section 13 rules the pairing out. Dustin's references break that rule in the Prussian banner (red ampersand on Prussian), the pillar badge rows and the page 14 data sheet. The Gate 1 decision on red and Prussian should show these.

4. **Balance can be written down.** Ballotpedia's neutrality policy covers balanced candidate coverage across major and minor parties, sources trusted across the spectrum, and never excluding a study because of its sponsor. With Braver Angels' equal-representation rule, it gives the editor tested wording for the nonpartisan rule set.

5. **Brand architecture has close models.** CalMatters runs one masthead with named tools (Digital Democracy, the Voter Guide), each with its own method page. Civic News Company runs Chalkbeat, Votebeat and Healthbeat as a family. ProPublica's 2026 redesign bundles each investigation with explainers, methodology notes and tip forms. 
6. **The logo built from font outlines is sound under the OFL.** The OFL-FAQ says artwork made with an OFL font is not subject to the OFL, and its maker remains the author [snippet]. Lora's Reserved Font Name restricts what a modified font file may be called, so it does not reach a logo SVG. A redrawn ampersand used as artwork raises no OFL issue. A font file built around it must stay under the OFL, keep the copyright line and carry a new name.

7. **A drawn ampersand helps the trademark position, and counsel must confirm how far.** The USPTO says filing the words in standard characters gives the broadest protection [snippet]. A special form filing protects the drawing filed, so a drawn ampersand gives Oath & Action a shape that nobody can set from a free font. Copyright adds little, because the Copyright Office generally refuses lettering and typographic ornamentation. Before launch, a trademark attorney should run clearance on OATH & ACTION, the monogram and any standalone ampersand, and advise on filings and contractor terms. Braver Angels had to rename in 2020 after a trademark settlement. I ran no trademark search.

8. **Condensed display faces are a locked-element decision.** Dustin's logo-system boards use a condensed heavy wordmark. Inter 4.0 has no width axis, and Inter Tight is a spacing variant. The ledger documents eleven OFL families, among them Archivo (width 62 to 125), Roboto Flex (width 25 to 151), Barlow Condensed, Oswald, Anton, Big Shoulders (Chicago's municipal face) and Mona Sans. Inter Tight is the locked display face, so any of these needs Dustin's named approval.

9. **The references drift from locked elements and from V7.** Generated boards rename the pillars, swap palettes and repeat an unsourced "12.4M". The atlas mockup on page 24 says "740 sources" where V7 gives 1,099, and the atlas home page on page 52 shows 50 variables and 117 connections where V7 gives 51 and 118. Use the references for direction only.

10. **Corrections to brief section 5.** Sigma 2026's "Invisibles" concerns older adults excluded from Peru's main social protection program by an automated poverty classification. The Urban Institute calculator uses 2016 rules. Bloomberg's "What's Really Warming the World?" is now verified on bloomberg.com. GovTrack has posted "Ending GovTrack's bulk data and API" (title seen only), so no data pipeline should depend on it.

## Rights in brief

`pics_i_like.pdf` has 54 pages, 39 of them unique. 41 are generated mockups (study only), 12 are screenshots of atlas work that Oath & Action owns (Q-03; may be shown with a label and date), and page 14 is a rendered data visualization study whose maker Dustin should confirm. I found no third-party material beyond platform icons inside generated boards. Generated photoreal people (pages 05, 15 and others) must never pass as photographs. The four brand mockups are generated and study only. The "Transparent" hinge file has no alpha channel; its checkerboard is painted in. V6 drops the URW Nimbus faces from Atlas V7 in favor of Inter Tight and Inter (DC-03). Q-02, Q-03, Q-05 and Q-06 are recorded.

## Claims I could not verify

1. Exact wording on any page.
2. Information is Beautiful 2024 edition's presentation: June 2025 at Outlier, or a virtual ceremony in May 2025.
3. ProPublica's redesign date (May 5, 2026, inferred).
4. Cooper Hewitt's full 2026 winner list.
5. Fieldwork Facility's Creative Review win, Ventana's En-ROADS credit, and PolicyEngine's calculator description.
6. GovTrack's bulk data and API change.
7. The Webby 2026 data visualization winner, D&AD 2026 design Yellow Pencils, and two Transform North America results.
8. Malofiej's status on an official domain.
9. Logo colors for nine of the fifteen benchmarks.
10. Code for America's rebrand date and Fast Company listing; Builders' Anthem Awards.
11. Several font details: Bebas Neue's weights, Mona Sans and Sofia Sans weight ranges, some italics, League Gothic's license file.
12. Any trademark fact about OATH & ACTION.
13. The maker of page 14.

## Tested and not tested

Tested: 97 official-domain searches; one failed fetch; PDF metadata, image sizes and page hashes; a WebP provenance scan of the mockups; a pixel comparison of page 24 with design-i-like-19; V7 `meta.counts` from the extracted JSON.

Not tested: page reads, trademark searches, font downloads and the benchmarks' live colors.

## Change log

Created:
- `work/research/20261021_Research-Ledger.md`
- `work/handoffs/phase-1/20261021_Research-Summary.md`
- `work/handoffs/phase-1/20261021_Pics-I-Like-Inventory.json`
- `work/build/scripts/phase-1/pics_pdf_inventory.py`, `mockup_metadata.py`, `build_rights_addendum.py`

Modified:
- `work/research/20261020_Rights-Ledger.md` (section "Added October 21, 2026: Phase 1 rights review" appended)

Nothing in `source/` or `work/extract/` changed.
