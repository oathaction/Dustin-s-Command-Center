# Stage A red team: brand, evidence and nonpartisanship

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the reviewer for this lens, working as `oa-research-lead` with `oa-creative-director`'s brand knowledge, under `work/handoffs/phase-2/20261106_Stage-A-Red-Team-Brief.md`. Page reviewed: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` as built at 20:16 on November 6.

## 1. Score

**2 of 5.** The locked lines, Rule 05.3 and most Illustrative labels are exact, but the guide's main real-world example misdescribes a bill that carried a voter ID requirement, and three nonpartisan rules are taught with examples that tilt or contradict each other.

## 2. Must fix

### M1. H.R. 7008 is called "the stock trading ban", and the bill also carries a voter ID requirement

Where: chapter 01, the Track piece in "One piece from each pillar" (`s-01-pieces`), Rules 01.2, 01.6, 01.10, 01.12, 01.20, 01.21 and 01.24; chapter 02, Rule 02.25 (`s-02-25-correct`) and the chapter sources.

What is wrong. The page says "H.R. 7008 would bar members of Congress from trading individual stocks." The House-passed bill, the Stop Insider Trading Act, bars members, spouses and dependent children from buying individual stocks and requires no sale of stock already held. It also carries a photo ID requirement for federal elections. A House member's own release says so: "The bill, which earned bipartisan support, would also implement voter ID requirements for federal elections" (barrett.house.gov, read November 6, 2026). A Lead Stories fact check rates "Democrats voted against a stock trading ban" as missing context for the same reason. No studio file mentions the voter ID section; the atlas status text omits it too.

Three places turn this into a partisan frame:
- Rule 02.25 rewrites "One party blocked the bill." as "The stock trading ban needed 60 votes to move forward in the Senate, and it got 53." That is the framing the fact check flagged, printed in the guide's lesson on neutral writing. It also breaks H12 (DR-82): the bill's official name is the Stop Insider Trading Act.
- Rule 01.2's source line ends "The survey came three years before the House and Senate votes." That ties a 2023 survey on a ban to votes on a different, combined bill, which most Democrats in the House opposed.
- The rotation log (Rule 01.12 and the editor's notes) records the stock trading ban's backing coalition as "Survey majorities of both parties' voters." For H.R. 7008 that is not the coalition.

Fix:
- Name the bill as "H.R. 7008, the Stop Insider Trading Act" and describe it whole wherever it appears: "would bar members of Congress, their spouses and dependent children from buying individual stocks, and would require photo ID to vote in federal elections."
- Rename the tracker after the bill (for example "Stop Insider Trading Act Tracker") or show both provisions in its deck.
- In Rule 02.25, write the structure row as "H.R. 7008, which paired a limit on members' stock purchases with a voter ID requirement, needed 60 votes to move forward in the Senate and got 53."
- Cut "before the House and Senate votes" from the survey's source line in Rules 01.2 and 01.20. Correct the rotation log row.
- Add the omission to the V7.1 issue list (DC-08). Check S01 in the chapter 14 data (`20261106_Chart-Data.json`, Board 3) for the same framing before it is reused.

### M2. Rule 01.16's correct application gives the two readings unequal descriptions

Where: Rule 01.16, `s-01-16-correct`.

What is wrong. The rule asks for "the same verbs and type" and names who holds each reading. The specimen writes "Economists Anna Stansbury and Lawrence Summers find" beside "The Economic Policy Institute, an advocacy group, finds". One side is credentialed and the other is discounted, in the example that teaches equal treatment. The phrase comes from one atlas field (LE04's qualification); another atlas entry calls the same institute "a labor-oriented research group". The caption, "Each reading runs 24 words, uses the verb 'finds' and names who holds it", counts words and misses the tilt.

Fix: describe both holders the same way. For example: "Economists Anna Stansbury and Lawrence Summers, writing for the National Bureau of Economic Research, find..." and "Economists at the Economic Policy Institute, a labor-oriented research group, find...". Recount both readings. While editing, add "average pay" and "typical pay" to the qualification, since that measure is the largest difference between the two readings.

### M3. Rule 01.2 gives one party the emphasis ink, and chapter 05 and the tokens say one ink for every party

Where: Rule 01.2 (`s-01-2-correct`, its specifications and builders note) against Rule 05.7 and `oa.chart.color.party.mark`.

What is wrong. Rule 01.2 reads "Two sides take Charcoal and Stone". Its specification is "First side: Charcoal ... `--oa-color-data-emphasis-on-newsprint`" and "Second side: Stone ... `--oa-color-data-context-on-newsprint`". With the alphabetical order (D2-186), Democrats always take the emphasis ink and Republicans the context ink, which the token file describes as "Every other data mark". Rule 05.7 says "A party takes the same neutral ink as every other party". The party-mark token's description is "one neutral ink for every party, with the party named on the mark (DR-48, DR-58)". Two chapters teach two answers on the most sensitive color rule in the guide.

Fix: rewrite Rule 01.2 to match DR-48 and DR-58, which postdate its Gate 1 wording and govern under the Stage A brief. Draw every party's mark in `--oa-chart-color-party-mark-on-newsprint` with its name printed on the mark, and drop the emphasis and context tokens from the rule. Where two sides of a debate must be told apart at a glance, use solid and outline in the same ink.

### M4. The letterhead print proof carries no Illustrative label and no width label

Where: proofs appendix, letterhead; `work/boards/phase-2/stage-a/proofs/20261106_Letterhead-Proof.pdf`, linked as a download.

What is wrong. Both PDF pages carry the following with no label of any kind:
- an invented address ("PO Box 214, Alder, MA 01000"),
- an invented clerk ("Jordan Lee, Town Clerk, Town of Alder"),
- a dated records request, signed "Dustin Cathcart, Founder and Editor".

The on-screen plate labels them, but a PDF travels without the page around it. H03 and Master Brief section 15 ask for the label beside each invented item. The Stage A brief also asks that the condensed width appear "labeled for Gate 2", and the PDF does not say which page shows which width.

Fix: print "Illustrative proof. The address, recipient and letter are invented." on each page, outside the letter area. Print "Today's width" on page 1 and "Condensed width, for Gate 2" on page 2. Rebuild the PDF.

### M5. Decision codes print on reader pages in five chapters and the proofs

Where and what. H11 (DR-81) says to print no bare code, and the Stage A brief lists the check. Chapters 01 and 02 are clean. The rest carry:
- 03: "(DR-55)" in the eight-lockup caption; "(I8)" in the minimum-size table caption.
- 04: Basis lines "Rule 05.3 (D2-01, DR-66); G1-05", "Rule 05.3; D1-22", "the five separation rules approved with I6 (G1-01)", "the badge's three conditions (S9, G1-02)", "R13 (DR-67)", and "(R13)" in Rule 04.7's text.
- 05: "decisions D2-01 and DR-66", "decision D1-04", "decisions DR-48, DR-53, DR-54 and DR-58", "Newsprint (DR-53)".
- 06: "decision DR-47"; "decision T-9".
- 08: "D1-21"; "R9 (DR-67)" and "(R9)"; "approved at Gate 1 (S5)".
- Proofs: "(DR-71)", "(D2-30)", "(DR-55)" twice, "R13".

Fix: name each decision in words, for example "approved at Gate 1", "Dustin's ruling on party colors, November 6, 2026" or "the red rule, Rule 05.3". Keep the codes in the manifests and notes.

### M6. Chapter 04 shows as correct a hinge headline that chapter 02 shows as a failure

Where: Rule 04.3, `s-04-3-correct`, against Rule 02.27, `s-02-27-failure`.

What is wrong. Rule 04.3's correct application prints "The hearing & the vote." at 24 px. Rule 02.27's failure prints the same headline and says it "puts an event first". A producer copying from chapter 04 makes the error chapter 02 forbids.

Fix: replace it in 04.3 with a rule-first headline from 02.27's correct set, such as "The filing deadline & the ballot."

## 3. Should fix

**S1. Rule 01.11's two cases name their actors differently** (`s-01-11-correct`). Texas reads "the Republican-led legislature redrew the congressional map, aiming at five more Republican seats". California reads "voters approved Proposition 50, which put in place a congressional map drawn to favor Democrats". The first names the majority that drew the map. The second credits voters and leaves out the Democratic-led legislature that drew the map and put it on the ballot. Fix: "In November 2025, voters approved Proposition 50, a congressional map the Democratic-led legislature drew to add Democratic seats." Also align the rule text ("When majorities of either party use the same mechanism") with its title ("both parties").

**S2. Rule 01.2's title reports a 2023 survey in the present tense.** "Most Republicans and most Democrats favor a ban" and "Percent of registered voters who favor a ban, May 2023". Under H08, documented results take record language. Fix: "In May 2023, most Republicans and most Democrats favored a ban...". Rule 01.20's deck already says "favored".

**S3. The Ballotpedia source line on Rule 01.5's map and Rule 02.25 is incomplete.**
- It does not label Ballotpedia as secondary, as D2-99 did for the same publisher under DR-46.
- It gives no observation date in the line itself.
- It omits the qualification that changes the count's meaning. Illinois allows citizen amendments only on the legislature's own structure and procedure, and Florida allows amendments only.

The research lead should confirm both limits against the state constitutions. Fix: "Source: Ballotpedia, a secondary source, States with initiative or referendum, as of November 6, 2026, 50 states and DC. Retrieved November 6, 2026. Mississippi's process cannot be used after a 2021 state supreme court ruling; Illinois limits citizen amendments to the legislature's structure."

**S4. Failure plates draw the parties in the brand's own Pillar Red and Prussian, with nothing inside the drawing to say so** (`s-01-2-failure`, `s-01-3-failure`, `s-01-5-failure`, `s-05-7-failure`). DR-48 says the two are "never assigned to a party, on any chart or map". The "× Failure case" label sits above the plate, so a cropped screenshot shows an Oath & Action chart with Republicans in Pillar Red and Democrats in Prussian. Fix: set a "Failure case: do not publish" band inside each of these stages, and say the same in each alt text.

**S5. The red ask sits directly under a Prussian panel** in the phone page shown as the correct application of Rules 05.1 and 05.3 (`s-05-1-correct`, `s-05-3-correct`). The "What happens next" panel in Prussian runs straight into the Pillar Red "Sign up to speak" button. The creative director's test asks for a check on every pairing of Pillar Red with Prussian, and builders will copy this view. Fix: put the hinge divider and a 24 px Newsprint gap between them, or set the panel in Charcoal.

**S6. Rule 01.18 says "only the ampersand is red"** and "Only the ampersand takes red, as the view's working red." Under Rule 05.3 and Rule 04.3's corrective, the ampersand takes the headline's ink when an error or a step holds the view's red. Fix: add "unless an error or a step on the same view holds the red, when the ampersand takes the headline's ink (Rule 04.3)."

**S7. The position piece's disclosure leaves out the editor's own roles.** Rule 01.23's specification reads "Disclosure: Who decided the position, the date and any funder interest". D2-80 and D2-106 print the editor's campaign roles wherever a reform he works on is argued. Fix: add "and any role our editor or staff hold in a campaign on the measure".

**S8. Internal names show in reader text.**
- Rule 04.5 says "Atlas V7 draws a hypothesis as a dotted line". The public name is "our systems atlas".
- Plate labels read "V5's ampersand, the Lora Bold glyph" (04.1) and "V5's master scaled to 16 px" (08.1), where the prose says "Edition 05".

Fix: use "our systems atlas" and "Edition 05" throughout.

**S9. Rules 01.4 and 03.5 cite WCAG 2.2 SC 1.4.11 as the basis for keeping red off Prussian, but the flat ratio, 3.19 to 1, passes that criterion's 3 to 1.** The real reasons are the rendered small sizes (2.27 to 1 at 16 px) and the red and blue pairing. Fix: basis "Design judgment, measured against SC 1.4.11 at rendered sizes", with both reasons stated.

**S10. Two counts of Edition 05's text elements disagree.** Rule 06.2 says "none of its 2,383 text elements grew"; Rule 06.3 says "833 of 2,346 rendered text elements under 13 px". Fix: use one count, or say what each counted.

**S11. Chapter 03 prints condensed-width minimums** in the minimum-size table ("condensed 120 px", "condensed 0.95 in" and so on). DR-89 keeps chapter 03 at today's width until Gate 2. Fix: move the condensed figures to the proofs appendix.

**S12. The email masthead proof's first line breaks the guide's own Rule 02.5.** It reads "Here is who wrote it, what changed since the draft, and how to speak before the vote.", the "here is how" opener that Rule 02.5 shows as its failure, in a three-part list. Fix: "The county's finance committee wrote it. Sign up by Monday to speak before Tuesday's vote." with the Illustrative label kept.

## 4. Questions for Dustin

1. **Does the initiative map in Rule 01.5 carry your disclosure?** D2-106 prints it on charts drawn on election-rule data. This map counts the states where citizens can petition a measure onto the ballot, which is the instrument Massachusetts Question 3 uses. *Recommendation:* print the disclosure under the map. Before any page prints it, also confirm the wording's tense, since the November 3, 2026 vote has passed and the text still says your editor "works with the Yes on 3 campaign".
2. **Keep H.R. 7008 as chapter 01's main real example?** *Recommendation:* keep it, described whole as M1 sets out. A bill that pairs two measures teaches Rule 02.25's point about structure better than a single-subject vote, and the survey can stay as a separate finding about a ban in general.

## 5. Tested and not tested

### Tested

- Rendered the page in Chromium with Playwright at 1440 px (at 1x, and at 2x for the maps) and at 390 px (at 2x). Dumped each chapter's rendered text and read chapters 01 to 08 and the proofs appendix in full.
- Looked at captures of these plates:
  - at 1440 px: the pillar pieces; 01.2, 01.3, 01.5 (correct and failure), 01.16, 04.3, 04.7, 05.1 and 05.7;
  - at 390 px: 01.2's failure, 01.11 and 02.25.
- Compared the four locked lines by script against every chapter's rendered text, and read the pillar order.
- Compared Rule 05.3's rendered text by script with D2-01 as amended by DR-66: it matches word for word, with curly apostrophes.
- Scanned every chapter's rendered text for decision codes, internal IDs and "Atlas V7".
- Recomputed the six payroll figures in Rules 05.5 and 06.5 from `20261106_Chart-Data.json`. All match: 3,798.4; 1,640; 1,278; 769; 88; −245.
- Checked Rule 01.5's tile map, 23 solid states plus DC, against the list of initiative states. Checked the failure map's 51 winners against my own record of the 2024 results, which is not FEC's file.
- Checked against the atlas export (`20261105_Atlas-Editorial-Data.json`):
  - the survey's 2,625 voters, dates and 87 and 88 percent;
  - Loop R4a's title;
  - LE04's grade, plausible and contested, and the "advocacy group" wording;
  - the cloture glossary entry;
  - H.R. 7008's status text, which omits the voter ID section.
- Checked that V7 dashes plausible links, in `work/handoffs/phase-0/20261020_Brief-V7-Values-Check.json`.
- Read the party-mark and data emphasis token descriptions in `tokens.json`.
- Read the color variables in the four partisan failure specimens.
- Ran the letterhead PDF through `pdftotext` and rendered both of its pages.
- Read these on the web, November 6, 2026:
  - publicconsultation.org: 86, 87 and 88 percent; 2,625 voters; May 19 to 30, 2023.
  - barrett.house.gov: H.R. 7008 includes a voter ID requirement.
  - crane.house.gov: the bill bars buying.
  - The Lead Stories fact check.
- Read search results only, without opening the pages:
  - census.gov, for 65.3 percent of citizens 18 and over voting in 2024;
  - Ballotpedia News, for Mississippi's May 2021 ruling.

### Not tested

- The House Clerk's Roll Call 280 page returned HTTP 503. senate.gov refused Vote 253 with HTTP 403, and I did not retry. The 53 to 47 count rests on the atlas.
- The bill text of H.R. 7008 on congress.gov. Its scope rests on two House members' releases and a fact check.
- Ballotpedia's "States with initiative or referendum" page returned no content. The 23-state count rests on my reading of the map. Illinois's and Florida's limits are from my own knowledge and need a check against the state constitutions.
- The EPI page and the NBER paper. Both readings rest on the atlas.
- The Texas and California redistricting facts, by search.
- The 1024 and 360 px widths, screen readers, a printed copy of the PDF, and every one of the 234 plates by eye. I read all their text, but looked at only the plates listed above.
- WCAG 2.2 and CSS Color 4 citations were not reopened.

## Change log

Created: `work/handoffs/phase-2/20261106_Stage-A-Red-Team-Brand-Evidence.md` (this file).
Modified: none. Captures and text dumps went to the session scratchpad. Nothing committed or pushed.

Sources read on the web: [PPC survey](https://publicconsultation.org/united-states/stock-trading-by-members-of-congress/), [Barrett release](https://barrett.house.gov/media/press-releases/barrett-helps-pass-congressional-stock-trading-ban-voter-id-requirement), [Crane release](https://crane.house.gov/2026/07/22/rep-crane-backed-bill-restricting-congressional-stock-trading-passes-house/), [Lead Stories fact check](https://leadstories.com/hoax-alert/2026/07/fact-check-democrats-voted-against-stock-trading-ban-bill-but-it-also-included-a-voter-id-provision.html), [Census 2024 voting tables](https://www.census.gov/newsroom/press-releases/2025/2024-presidential-election-voting-registration-tables.html), [Ballotpedia News on Mississippi](https://news.ballotpedia.org/2021/05/15/mississippi-supreme-court-overturns-2020-medical-marijuana-initiative-says-the-states-initiative-process-cant-be-used/).
