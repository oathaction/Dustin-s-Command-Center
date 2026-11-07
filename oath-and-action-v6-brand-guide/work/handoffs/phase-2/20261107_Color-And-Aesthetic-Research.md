# Board 6, section 4: color and aesthetic research

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the research lead (`.claude/agents/oa-research-lead.md`) for the color designer, under section 4 of `work/handoffs/phase-2/20261107_Board-6-Brief.md`. Dustin's direction is DR-107: six one-page identity sheets, each with a lead color other than red, on Newsprint (#DCD9D2) with Charcoal (#121212) as the text ink. These are explorations. Pillar Red stays in force until Dustin approves a change by name (gate rule 4), and DR-48, DR-58 and DR-93 hold on every sheet: no party, side or person owns a brand color.

The report has four parts, in the order the brief asks: what studios, newsrooms and civic organizations are doing now; how brands on paper grounds choose an accent; how lead colors read for party in the United States; and eight palette directions with measured contrast. A section on contrast arithmetic comes first, because it decides what any lead color on this ground can and cannot do.

## How to read this report

Every claim carries a grade from H08 in chapter 02's writing section: Documented, Well supported, Plausible, Contested or Hypothesis. A statement about what a brand or forecaster chose is Documented when I opened the brand's or forecaster's own page, package or site. "Opened" means I fetched the page, file or package and read it. "Rendered" means I loaded the live site in a browser (Playwright, 1280 by 900 px) on November 7, 2026 and looked at the screenshot. "CSS" means I counted the colors in a site's stylesheets, which shows what a site uses and says nothing about why. "Snippet" means I read only a search result's summary; I mark each one.

Trend reports (Pantone, WGSN with Coloro, Pinterest, Adobe, Canva) are marketing and forecasting. I list them as creative inputs and never as evidence of what readers think. Anything I conclude from the examples is labeled as a design judgment. Every contrast ratio in this report was computed by script from the WCAG 2.2 formula, and the script reproduces the guide's own published values (2.96, 9.42 and 13.29 to 1), so the numbers match chapter 05.

## Contrast arithmetic for this palette

These are the facts the color designer should hold before choosing any hue. All are Documented by computation.

- Newsprint has a relative luminance of 0.695 and Charcoal 0.006. Charcoal on Newsprint measures 13.29 to 1.
- Because the two grounds are only 13.29 to 1 apart, no color can reach 4.5 to 1 against both. Text-safe on Newsprint needs a relative luminance at or below 0.116; text-safe on Charcoal needs 0.202 or above. The two ranges never meet.
- A color with a relative luminance between 0.118 and 0.198 passes 3 to 1 against both grounds. Below 0.183 it also carries a White label at 4.5 to 1 or better. I call 0.118 to 0.183 "the band". A lead in the band can draw ampersand B on Newsprint with no keyline, draw B on the Charcoal avatar tile that R13 makes the default, fill the ask button with a White label, and mark a chart's emphasis point, all with one hex value.
- Pillar Red sits just outside the band, at 0.202. That is why it measures 2.96 to 1 on Newsprint and needs the Charcoal keyline of Rule 05.5, and why it reaches 4.49 to 1 on Charcoal. Its White label measures 4.17 to 1, which passes only because the guide's ask type (Inter 700, 19 px) counts as large text under WCAG.
- So every possible lead is one of three kinds:
  - An ink lead (relative luminance at or below 0.116) passes 4.5 to 1 on Newsprint and fails on Charcoal. It needs a light partner color for the Charcoal tile. Prussian is one.
  - A band lead (0.118 to 0.183) does every job on both grounds at 3 to 1 or better, and is not text-safe on Newsprint below large-text sizes. Verdigris is one.
  - A fill lead (0.202 and above) carries Charcoal text at 4.5 to 1 or better and fails as a mark on Newsprint. It needs a keyline, a tile or a darker partner on Newsprint. Pillar Red is nearly one; a highlighter yellow or chartreuse is one.
- Newsprint is darker than the paper grounds other brands use. The FT's paper (#FFF1E5) measures 0.898, Semafor's page color (#F8F5D7) 0.902, and White 1.000. The same accent loses about a fifth of its contrast when it moves onto Newsprint: FT teal (#0D7680) drops from 4.84 to 1 on FT paper to 3.80 to 1 on Newsprint, so a peer's accent cannot be copied across without darkening it.
- In grayscale, almost every candidate lead has the same lightness as Stone (#5D636D). Patina, Ballot Violet, Press Cobalt and Evergreen measure between 1.01 and 1.07 to 1 against Stone, and Pillar Red 1.45 to 1. A grayscale proof cannot tell the lead from Stone context, so emphasis needs a label or a shape as well as a color, as Rule 05.4 already requires.

## 1. What leading studios, newsrooms and civic organizations are doing

### Color forecasts for 2025 to 2027 (trend reports, labeled as such)

| Source | What it named | Date | Grade and basis | What it offers this brief |
|---|---|---|---|---|
| Pantone, Color of the Year 2026 | PANTONE 11-4201 Cloud Dancer, a white. NBC News quotes Pantone: "a billowy, balanced white imbued with a feeling of serenity" | Announced December 4, 2025 | Documented for the name (Pantone's page, opened); description from NBC News, opened. Several outlets call it Pantone's first white since the program began in 1999 (snippet; Pantone's page does not say so) | A pale, quiet ground is the forecaster's color of the year. Newsprint already sits in that territory |
| Pantone, Color of the Year 2025 | Mocha Mousse, a warm brown | Named for 2025 | Snippet only | Earthy browns were the year before's pick |
| WGSN and Coloro, Colour of the Year 2026 | Transformative Teal: "A fluid fusion between dependable dark blue and aquatic green, this is the colour for a period of change and redirection" | Post dated September 3, 2024 | Documented, WGSN blog opened. Coloro code 092-37-14 from secondary coverage | Teal as the forecasters' lead color for 2026, tied to ecology and recovery |
| WGSN and Coloro, A/W 26/27 key colours | Transformative Teal, Wax Paper, Fresh Purple, Cocoa Powder, Green Glow | 2024 release | Snippet | A paper-toned neutral and a purple sit beside the teal |
| WGSN and Coloro, Colour of the Year 2027 | Luminous Blue (125-28-38), "both mysterious and eccentric"; S/S 27 key colours Energy Orange, Pop Pink, Meadowland Green and Clay | April 29, 2025 | Documented, WGSN press release opened | Forecasters are moving to a saturated blue and a bright orange for 2027 |
| Pinterest Palette 2026 | Cool Blue, Jade, Plum Noir, Wasabi ("This electric chartreuse..."), Persimmon ("Part orange, part red") | January 14, 2026 | Documented, Pinterest newsroom opened. Method: search and save data plus "expert curation" | Search behavior points to chartreuse, jade, plum and an orange-red |
| Adobe 2026 Creative Trends | All the Feels, Connectioneering, Surreal Silliness, Local Flavor | 2026 report | Listed in the master brief (snippet, October 20). The page returned HTTP 503 today | Human texture and local context |
| Canva, "Imperfect by Design," 2026 | Ten trends including Texture Check, Explorecore and Notes App Chic | December 2025 | Listed in the master brief (snippet, October 20). The page returned HTTP 403 today | Tactile texture and calm layouts, used sparingly |

Plausible reading of the forecasts, as a design judgment: they disagree. Pantone points to quiet and pale; WGSN and Pinterest point to one saturated accent (teal, blue, chartreuse, orange) against calm neutrals. Both readings fit a Newsprint ground with one lead color.

### Newsrooms

| Brand | What it does with color and feel | Grade and basis |
|---|---|---|
| Financial Times | Paper ground #FFF1E5 with three deep accents, claret #990F3D, oxford #0F5499 and teal #0D7680, and slate #262A33 for text. Only colors the system marks with "allow-tones" may be tinted | Documented, from the FT's own Origami package `@financial-times/o-colors` 6.7.1, opened |
| The Guardian | Navy brand #052962 with yellow #FFE500 for its asks to readers; section colors news #C70000, opinion #C74600 (an orange), sport #0077B6, culture #866D50 (a brown), lifestyle #BB3B80. Its neutral 7 is #121212, the same value as our Charcoal | Documented, from the Guardian's own package `@guardian/source` 14.0.0, opened |
| Semafor | Declares a cream page color (#F8F5D7) with near-black #1F1D1A, a serif masthead, dotted rules, and small yellow and rust dots as accents; cobalt #0E29B5 and #243BB5 appear in its CSS | Documented: theme color and CSS opened, home page rendered |
| Newsweek | A September 2025 redesign with the studio 2x4: "a confident red-and-paper palette" and "high-contrast blacks and whites for accessibility" | Documented, Editor and Publisher release of September 25, 2025, opened |
| Grist | A pale chartreuse band (#E6FFA0, its declared theme color) behind warm brown-black type (#3C3830), with a coral donate button | Documented, rendered and CSS |
| Rest of World | Declares an electric blue theme color, rgb(36, 46, 247) | Documented, theme color opened |
| The 19th | Deep indigo page (#1C1542) with white serif headlines and a cyan button; hot pink #F9135C in its CSS | Documented, rendered and CSS |
| Votebeat | Purple wordmark tag (#824F9D), lavender navigation, serif headlines; ochre #AE610C and teal #178287 in its CSS | Documented, rendered and CSS |
| CalMatters | Teals #0A819F and #075E73 with a gold #F4BB32 in its CSS | CSS only; the page served a bot check, so I did not see it |

### Civic and public-interest organizations

| Organization | What it does | Grade and basis |
|---|---|---|
| GOV.UK, brand refresh | From June 25, 2025, the black header became blue, with "a light blue coloured dot up in the middle between GOV and UK". Its palette lists brand blue #1D70B8, teal #158187 and a focus yellow #FFDD00 that always carries #0B0C0C text. The guidance says "Only use this colour to indicate which element is focused on." | Documented: gov.uk "Changes to GOV.UK" and the GOV.UK Design System colour page, opened. Cost and agency (M+C Saatchi, £532,000) are press reports, not checked |
| Government Digital Service brand, April 2025 | "we landed on two main colours: the cyan and the midnight blue" | Documented, GDS design notes blog, April 4, 2025, opened |
| U.S. Web Design System | Grades every color from 0 (white) to 100 (black); a grade gap of 50 or more gives AA contrast, 40 or more gives AA for large text, 70 or more gives AAA. Grade 50 passes against both white and black | Documented, USWDS color overview, opened |
| Democracy Works (TurboVote, Voting Information Project) | A unified identity introduced February 4, 2026, described as "clean, modern, and designed to better communicate our role as essential civic infrastructure". The site shows deep indigo and violet with magenta #D00060 and navy #142348 | Documented: announcement opened; site rendered and CSS. The page names no designer and says nothing about color |
| Vote.org | A 2020 rebrand by Interactivism made the logo work "on both red and blue backgrounds" to communicate a "bipartisan position at a glance". Today the site declares a deep purple theme (#1C0D32) and uses red buttons and a bright blue band | Documented: Interactivism case study opened; site rendered |
| iCivics | Deep purple (#4C0064) with orange (#FF5900) | Documented, rendered and CSS |
| USAFacts | Magenta theme color (#E1197A), dark green, purple, and a mint highlight behind headline words | Documented, rendered and CSS |
| America250, the national semiquincentennial | Chermayeff and Geismar and Haviv drew a red, white and blue ribbon forming "250". Brian Collins, quoted by the YELLO newsletter on January 9, 2024, said the 1976 Bicentennial designers were "not burdened with the divisiveness those colors now represent" | Documented for the quote and designer (YELLO, opened). Design Week's report of the same point is a snippet; its page refused automated access |

### What these examples add up to

These are design judgments drawn from the examples above, each with its grade.

1. A paper ground with one strong accent and near-black type is a current editorial look. Newsweek's 2025 redesign, Semafor's cream page and the FT's paper all do it. Documented for the three; that it is a trend is Plausible from three cases.
2. Teal and blue-green is the forecasters' color for 2026 and a working accent at GOV.UK, the FT, CalMatters and Votebeat. Documented.
3. Purple and deep indigo lead at five of the voting and civic organizations I checked (Vote.org, Democracy Works, iCivics, Votebeat, The 19th). Documented for the five. That purple has become the visual shorthand for "nonpartisan civic" is Plausible, and it means a purple Oath & Action would join a crowded field.
4. A bright fill behind dark type is a common way to use a light color on a pale ground: Grist's chartreuse band, USAFacts' mint highlight, the Guardian's yellow asks, GOV.UK's yellow focus state. Documented.
5. Civic identity designers treat red and blue as loaded. America250 kept them and drew comment for it; Vote.org used both on purpose to signal balance. Documented for the two cases.

## 2. Paper and newsprint palettes

### How brands on a paper ground choose an accent

- They pick deep accents. All three FT accents measure at least 4.84 to 1 on FT paper, and claret and oxford pass 4.5 to 1 even on our darker Newsprint (5.98 and 5.42). Documented by computation from the FT's own values.
- They keep the brightest color as a fill and never as an ink. The Guardian's yellow (#FFE500) measures 1.15 to 1 on FT-like paper and 14.68 to 1 with Charcoal text; GOV.UK's focus yellow always carries near-black text. Documented.
- They let near-black carry the page. Semafor's accents are small dots; Newsweek names "high-contrast blacks and whites for accessibility". Documented.
- A grade system keeps tints honest. USWDS sets contrast by the gap in grade between two colors. The same idea works here: give each lead a tint scale measured against Newsprint and Charcoal, as the token file already does for Stone and Verdigris. Documented for USWDS; the transfer is a design judgment.

### Printing on newsprint

- Newspaper Club, a newsprint printer, says: "Colours won't look as bright and vibrant as they do on screen"; "Simple colours, which use just one or two of the ink colours, work best"; "Colours with a small percentage of one of the inks are more likely to print inconsistently"; "We can't print spot colours"; "Use 100%K (black) for all black text and details"; and "there will be less contrast in print". Its newsprint is "not as bright white as office paper". Documented, traditional printing guide, opened.
- Pantone says the coated and uncoated labels describe the paper, and that on uncoated paper "A normally vibrant palette on coated paper will become more muted". Documented, Pantone support pages (snippet from pantone.com; the help page I tried returned 404).
- Coldset newspaper presses commonly plan for about 26 percent dot gain at the 50 percent dot and a total ink limit around 240 percent, under the SNAP specification and the ISOnewspaper26v4 profile. Snippet, secondary printer and publisher pages; I did not open SNAP or the ISO standard.

What this means for the sheets, as design judgments (Plausible): a lead that prints well on newsprint is built mostly from one or two process inks at strong percentages, sits in or below the band so that dot gain darkens it without losing it, and never relies on a pale tint of itself to carry meaning. A bright fill lead (Highlighter) is the most likely to dull on press. Screen contrast should keep a margin above the minimum because print loses some. Every direction below needs a press proof on the real stock before it is approved for print.

## 3. How lead colors read for party in the United States

### What the record shows

- Red for Republicans and blue for Democrats became fixed in 2000. Before then networks varied: in 1976 NBC showed Ford in blue and Carter in red, and ABC used yellow for Ford. The New York Times and USA Today first ran color maps two days after the 2000 election, both with Bush in red and Gore in blue. NBC standardized to match ABC and CBS that year. Documented, Smithsonian Magazine, by Jodi Enda, October 31, 2012, updated October 21, 2024, opened.
- Rock the Vote's explainer, published June 4, 2026, teaches: "The color blue refers to the Democratic Party, while the color red is associated with the Republican Party"; "Purple states are states that are relatively equal parts Democratic and Republican"; "The Green Party, fittingly, is represented by the color green"; "The color gold or yellow has become the adopted color of the Libertarian Party." It names no party for orange. Documented, opened.
- On Election Day 2010 and 2012, Republicans' and Democrats' color preferences "changed to become more closely aligned with their own party's colors"; on other days Republicans liked "Democratic blue" more than Democrats did. The authors conclude color preferences "are thus far more dynamic and context-dependent than has previously been believed". Documented for the abstract (Schloss and Palmer, Psychonomic Bulletin and Review 21, 1481 to 1488, 2014, opened). As a general claim about readers, Plausible: one study.
- In a 2023 study, a continuous color gradient reduced the polarizing effect of red and blue election maps, and a green and orange pair reduced perceived polarization in one study and not in the other. The authors conclude "the dichotomization of electoral maps (not the particular hues) increases perceived voting polarization". Documented for the paper (Furrer, Schloss, Lupyan, Niedenthal and Wood, Cognitive Research: Principles and Implications 8, 11, 2023, opened). The finding is Plausible: one paper, mixed results on hue. It supports Rule 01.2 as written: any two colors set against each other stage a contest, whatever the hues.
- The party reading of blue is live this week. On November 7, 2026, both Semafor's and Grist's home pages carried headlines calling the November 3 midterms a "blue wave". Documented, rendered.
- In July 2024 the Harris campaign's account changed its banner to "a simple "kamala hq" against a neon-green background", referencing Charli XCX's album "BRAT". Documented, Fortune, by Eva Roytburg, July 24, 2024, opened.
- Wear Orange, run by Everytown for Gun Safety, "originated on June 2, 2015"; orange is "the color hunters wear in the woods to protect themselves and others." Documented, wearorange.org, opened.
- Gold was "the only color used by all US suffrage organizations", and only the National Woman's Party used purple, white and gold together. Documented, National Park Service, last updated March 4, 2024, opened.
- The yellow Gadsden flag dates from 1775 and became a Tea Party protest symbol from 2009. Snippet, secondary (Snopes, 2021, and encyclopedia pages).
- U.S. safety signs use red for DANGER, orange for WARNING and yellow for CAUTION under ANSI Z535. Snippet, secondary trade pages; I did not open the standard.

### Color by color

Each risk rating is a design judgment built on the sources above. DR-48 applies to every row: whatever a color might suggest, the brand never assigns it to a party, a side or a person, and every party takes one neutral ink with its name printed.

| Lead color | How it can read in the United States | Grade | Risk as an Oath & Action lead |
|---|---|---|---|
| Red | The Republican Party, since 2000 | Documented | Excluded by DR-107 for these sheets |
| Bright or saturated blue (cobalt) | The Democratic Party; "blue wave" headlines this week | Documented | High. Closest to the election-map blue, and the reading sharpens around elections, which the brand covers |
| Deep navy (Prussian) | Still blue, so the same party reading is available; navy also sits in the flag and in government identities | Party reading Documented; that navy reads less partisan than bright blue is Plausible, untested with readers | Moderate |
| Purple | A blend of the two parties: swing states, "equal parts Democratic and Republican"; also suffrage heritage | Documented | Low as a party; Moderate as a meaning. It can say "we sit between the parties", and DR-93 defines nonpartisan as one standard of evidence, which is a different claim. Crowded among civic groups |
| Green | The Green Party; environmental causes | Documented | Low to Moderate for deep greens |
| Chartreuse or lime | The 2024 Harris campaign banner | Documented for the event; whether readers still connect it is a Hypothesis | Moderate |
| Teal | No U.S. party reading in the sources I checked; WGSN frames it as ecological | No source found; readers were never asked | Low |
| Orange | No party in Rock the Vote's list; Wear Orange for gun safety; WARNING on safety signs | Documented for Wear Orange; safety use is a snippet | Low as a party; Moderate on any piece about firearms law |
| Yellow or gold | The Libertarian Party; the Gadsden flag; suffrage gold | Documented, Gadsden is secondary | Moderate for bright yellow as a lead; Low for a deep ochre |
| Brown or ochre | No party reading found | No source found; readers were never asked | Low |

## 4. Palette directions for the color designer

### How I built them

- Each direction keeps Newsprint as the ground and Charcoal as the text ink, and adds one lead and two or three supporting colors. Stone, Deep Stone and White stay available in every scheme.
- Seven of the eight leads sit in the band, so one hex value draws B on Newsprint and on the Charcoal tile, fills the ask button under a White label, and marks a chart's emphasis point. Federal Ink keeps today's Prussian, an ink lead, and adds a light partner for Charcoal. Highlighter is a fill lead on purpose, and its limits are stated.
- Where a lead cannot carry text on one ground, a supporting color does: a deep ink for text on Newsprint, or a light partner for Charcoal.
- No lead is red, and no scheme pairs two colors as sides. Every scheme keeps the one neutral party ink of Rule 01.2.
- I rendered every lead as an ampersand, a button and a word on both grounds beside Pillar Red and looked at them. Comments on how a hue looks are design judgments from that render.

### Measured contrast for every color

"Text" means 4.5 to 1 or more, "mark" means 3 to 1 or more (graphics, large text, button edges), "fails" means under 3 to 1. The Charcoal column gives one ratio for both uses: the color drawn on Charcoal, and Charcoal type set on the color.

| Direction | Color | Role | Hex | On Newsprint | On Charcoal, or Charcoal text on it | White label on it | Relative luminance |
|---|---|---|---|---|---|---|---|
| Reference: today | Pillar Red | lead | `#E63946` | 2.96:1 (fails) | 4.49:1 (mark) | 4.17:1 (mark) | 0.202 |
| 1 Patina | Patina | lead | `#1F6E6A` | 4.26:1 (mark) | 3.12:1 (mark) | 6.01:1 (text) | 0.125 |
| 1 Patina | Prussian | support | `#1F2D5A` | 9.42:1 (text) | 1.41:1 (fails) | 13.28:1 (text) | 0.029 |
| 1 Patina | Brass | support | `#8A6A2A` | 3.57:1 (mark) | 3.73:1 (mark) | 5.03:1 (text) | 0.159 |
| 1 Patina | Sea Glass | support | `#7FB8AE` | 1.59:1 (fails) | 8.36:1 (text) | 2.24:1 (fails) | 0.418 |
| 2 Federal Ink | Prussian | lead | `#1F2D5A` | 9.42:1 (text) | 1.41:1 (fails) | 13.28:1 (text) | 0.029 |
| 2 Federal Ink | Civic Yellow | support | `#FFD23F` | 1.02:1 (fails) | 12.97:1 (text) | 1.44:1 (fails) | 0.677 |
| 2 Federal Ink | Sky | support | `#9DB7E0` | 1.45:1 (fails) | 9.17:1 (text) | 2.04:1 (fails) | 0.464 |
| 2 Federal Ink | Verdigris | support | `#4A7C74` | 3.37:1 (mark) | 3.95:1 (mark) | 4.74:1 (text) | 0.171 |
| 3 Signal Orange | Signal Orange | lead | `#C2500E` | 3.35:1 (mark) | 3.97:1 (mark) | 4.72:1 (text) | 0.172 |
| 3 Signal Orange | Ember | support | `#8F3A0A` | 5.36:1 (text) | 2.48:1 (fails) | 7.56:1 (text) | 0.089 |
| 3 Signal Orange | Prussian | support | `#1F2D5A` | 9.42:1 (text) | 1.41:1 (fails) | 13.28:1 (text) | 0.029 |
| 3 Signal Orange | Apricot | support | `#F4B183` | 1.30:1 (fails) | 10.23:1 (text) | 1.83:1 (fails) | 0.523 |
| 4 Archive Ochre | Ochre | lead | `#946616` | 3.57:1 (mark) | 3.72:1 (mark) | 5.03:1 (text) | 0.159 |
| 4 Archive Ochre | Sepia | support | `#5B4630` | 6.30:1 (text) | 2.11:1 (fails) | 8.88:1 (text) | 0.068 |
| 4 Archive Ochre | Parchment | support | `#CDB98A` | 1.37:1 (fails) | 9.73:1 (text) | 1.93:1 (fails) | 0.495 |
| 4 Archive Ochre | Prussian | support | `#1F2D5A` | 9.42:1 (text) | 1.41:1 (fails) | 13.28:1 (text) | 0.029 |
| 5 Highlighter | Highlighter | lead | `#D4F25A` | 1.12:1 (fails) | 14.85:1 (text) | 1.26:1 (fails) | 0.782 |
| 5 Highlighter | Moss | support | `#45611A` | 5.00:1 (text) | 2.66:1 (fails) | 7.05:1 (text) | 0.099 |
| 5 Highlighter | Lilac | support | `#CBBDEB` | 1.24:1 (fails) | 10.72:1 (text) | 1.75:1 (fails) | 0.551 |
| 6 Ballot Violet | Ballot Violet | lead | `#7552B3` | 4.12:1 (mark) | 3.22:1 (mark) | 5.81:1 (text) | 0.131 |
| 6 Ballot Violet | Deep Violet | support | `#4B2E83` | 7.38:1 (text) | 1.80:1 (fails) | 10.41:1 (text) | 0.051 |
| 6 Ballot Violet | Suffrage Gold | support | `#E0B13A` | 1.42:1 (fails) | 9.38:1 (text) | 2.00:1 (fails) | 0.476 |
| 6 Ballot Violet | Lavender | support | `#B39DDB` | 1.70:1 (fails) | 7.82:1 (text) | 2.40:1 (fails) | 0.388 |
| 7 Evergreen | Evergreen | lead | `#33704A` | 4.19:1 (mark) | 3.17:1 (mark) | 5.90:1 (text) | 0.128 |
| 7 Evergreen | Marigold | support | `#E9A93A` | 1.46:1 (fails) | 9.10:1 (text) | 2.06:1 (fails) | 0.460 |
| 7 Evergreen | Clay | support | `#C98B6B` | 2.02:1 (fails) | 6.59:1 (text) | 2.84:1 (fails) | 0.319 |
| 7 Evergreen | Fern | support | `#8FC29A` | 1.44:1 (fails) | 9.23:1 (text) | 2.03:1 (fails) | 0.468 |
| 8 Press Cobalt | Cobalt | lead | `#3B5BDB` | 4.02:1 (mark) | 3.31:1 (mark) | 5.67:1 (text) | 0.135 |
| 8 Press Cobalt | Periwinkle | support | `#9AA8FF` | 1.58:1 (fails) | 8.40:1 (text) | 2.23:1 (fails) | 0.421 |
| 8 Press Cobalt | Apricot | support | `#F4B183` | 1.30:1 (fails) | 10.23:1 (text) | 1.83:1 (fails) | 0.523 |

### Color-vision and grayscale checks

I simulated protanopia, deuteranopia and tritanopia (Machado, Oliveira and Fernandes, 2009, full severity) and measured the CIEDE2000 color difference, where about 1 is the smallest difference a viewer can see in ideal conditions. As a design judgment, I treat a difference under 10 as a risk for small chart marks.

| Lead | Against Stone in grayscale | Difference from Stone: normal, protan, deutan, tritan | Difference from Pillar Red: normal, protan, deutan |
|---|---|---|---|
| Pillar Red (today) | 1.45:1 | 33.6, 19.9, 32.6, 32.9 | not applicable |
| Patina | 1.01:1 | 19.8, 4.7, **0.9**, 16.5 | 54.6, 14.9, 33.3 |
| Federal Ink (Prussian) | 2.20:1 | 21.7, 20.7, 21.8, 19.2 | 45.4, 37.6, 54.7 |
| Signal Orange | 1.28:1 | 32.8, 30.2, 34.0, 28.7 | 17.7, 11.8, **6.9** |
| Archive Ochre | 1.20:1 | 29.8, 30.5, 31.2, 26.4 | 32.6, 12.2, **8.9** |
| Highlighter | 4.80:1 | 53.8, 52.6, 52.3, 40.3 | 68.2, 42.8, 25.9 |
| Ballot Violet | 1.04:1 | 16.6, 18.6, 17.6, 13.8 | 36.1, 40.3, 51.6 |
| Evergreen | 1.02:1 | 24.9, 20.1, 16.9, 15.4 | 60.6, **1.3**, 20.1 |
| Press Cobalt | 1.07:1 | 18.7, 22.0, 21.2, 15.9 | 42.3, 44.7, 58.5 |

What the bold cells mean for the sheets:
- Patina and Stone are the same color to a reader with deuteranopia (0.9) and the same lightness in grayscale. On a Patina sheet the chart context must move off Stone. The Stone tint #A1A2A3 (already in the token file as stone n55) measures 2.35 to 1 against Patina, with a deuteranopia difference of 25.7.
- If the error state stays red when the lead changes, a reader with deuteranopia sees Signal Orange (6.9) and Archive Ochre (8.9) as close to the error red, and a reader with protanopia cannot tell Evergreen from it at all (1.3). Each of those sheets must show the error state with its icon and word (Rule 05.4) or move error off red.

### The eight directions

#### 1. Patina

- Feel: civic. Calm public authority, the green that copper roofs and statues weather to, and a step deeper than today's Verdigris.
- Lead: Patina `#1F6E6A`. Supporting: Prussian `#1F2D5A` (links, a second data series, dark panels), Brass `#8A6A2A` (a small warm accent such as a kicker rule), Sea Glass `#7FB8AE` (Patina's partner for text on Charcoal).
- Jobs for the lead: ampersand B and the lockmark's lever (4.26 to 1 on Newsprint with no keyline, 3.12 to 1 on the Charcoal tile); the ask fill with a White label (6.01 to 1); the chart emphasis point.
- Why, and examples: WGSN's Colour of the Year 2026 is Transformative Teal (trend report). GOV.UK's 2025 refresh keeps teal #158187 as an accent, the FT uses teal #0D7680 on paper, and CalMatters and Votebeat use teal on screen. Documented.
- Watch: Patina differs from Verdigris by 7.2 (CIEDE2000), so the two read as one family. Verdigris ends the diverging scale (DR-54) and draws the focus ring, which would put the identity lead inside a data scale against section 10 of the master brief. The sheet should say how the scale and the focus ring change. Chart context moves to #A1A2A3 (above).
- Party reading: Low. No party claims teal in the sources I checked. Green reads as the Green Party and as ecology; teal leans blue.

#### 2. Federal Ink

- Feel: institutional. The government document, the court opinion, the seal.
- Lead: Prussian `#1F2D5A`, promoted from today's palette. Supporting: Civic Yellow `#FFD23F` (highlight and focus fill, always under Charcoal text), Sky `#9DB7E0` (Prussian's partner on Charcoal), Verdigris `#4A7C74` (a second mark).
- Jobs: B and lever on Newsprint (9.42 to 1); B in Sky on the Charcoal avatar tile (9.17 to 1), because Prussian measures 1.41 to 1 there and R13 makes Charcoal the default tile; the ask fill with a White label (13.28 to 1); highlight and focus in Civic Yellow.
- Why, and examples: GOV.UK pairs brand blue with a yellow focus state that always carries near-black text; the Guardian pairs navy #052962 with yellow #FFE500 for its asks; USWDS sets the pattern for U.S. federal sites. Documented.
- Watch: Prussian already starts the diverging scale (DR-54), the same token conflict as Patina. Today's guide keeps red off Prussian; with Prussian as the lead that rule no longer has work to do on this sheet.
- Party reading: Moderate. Navy is still blue, and blue reads Democratic (Rock the Vote; this week's "blue wave" headlines). That a deep navy reads less partisan than a bright blue is Plausible and untested with readers. Yellow is the Libertarian color in Rock the Vote's list, so it stays a fill and never marks a side.

#### 3. Signal Orange

- Feel: editorial with urgency. The bulletin, the deadline, the step you can take now. The direction keeps the energy red gives the brand today with a different hue.
- Lead: Signal Orange `#C2500E`. Supporting: Ember `#8F3A0A` (orange-brown ink for kickers and links on Newsprint, 5.36 to 1), Prussian `#1F2D5A` (the cool counterweight for dark panels and a second series), Apricot `#F4B183` (a tint fill under Charcoal text).
- Jobs: B and lever on Newsprint with no keyline (3.35 to 1) and on Charcoal (3.97 to 1); the ask fill with a White label (4.72 to 1); the emphasis point.
- Why, and examples: the Guardian's opinion pillar is an orange, #C74600, which differs from Signal Orange by only 2.4 (Documented); Pinterest's 2026 Persimmon and WGSN's S/S 27 Energy Orange point the same way (trend reports); GOV.UK's palette and iCivics carry orange. In the render, every orange that sits in the band drifts toward rust; #C2500E read most clearly orange of the three I tried (design judgment).
- Watch: the Guardian uses this hue to mark opinion. A reader of both could take an orange Act piece as opinion, which matters because DC-01 labels positions separately (Plausible). Orange is WARNING on U.S. safety signs (snippet), so warning states need their own treatment. Deuteranopia brings it close to an error red (6.9).
- Party reading: Low as a party. Moderate on any piece about firearms law, where an orange ask could read as Wear Orange's color.

#### 4. Archive Ochre

- Feel: archival. The record room, the bound volume, brass plaques, iron-gall ink.
- Lead: Ochre `#946616`. Supporting: Sepia `#5B4630` (brown ink for text, 6.30 to 1), Parchment `#CDB98A` (a tint fill under Charcoal text), Prussian `#1F2D5A` (ink blue).
- Jobs: B and lever on Newsprint (3.57 to 1) and Charcoal (3.72 to 1); the ask fill with a White label (5.03 to 1); the emphasis point.
- Why, and examples: earthy browns and clays recur in the forecasts (Pantone 2025 Mocha Mousse, a snippet; WGSN S/S 27 Clay, Documented). The Guardian's culture pillar is a brown in the same band, #866D50. Gold was the color every U.S. suffrage group shared (National Park Service). Documented. My first ochre (#8C6A1F) read olive in the render; #946616 reads warmer (design judgment).
- Watch: deuteranopia brings it close to an error red (8.9). Ochre is three process inks on press, so it is the most likely of the band leads to shift between print runs (Plausible, from Newspaper Club's guidance; not tested on press).
- Party reading: Low to Moderate. Gold and yellow are the Libertarian Party's colors and the Gadsden flag's; a deep ochre sits far darker than either (design judgment).

#### 5. Highlighter

- Feel: modern and digital-native. The newsletter, the social card, the marked-up page.
- Lead: Highlighter `#D4F25A`, used only as a fill. Supporting: Moss `#45611A` (the lead's ink form, for kickers and links on Newsprint, 5.00 to 1), Lilac `#CBBDEB` (a second fill for a second job, such as the selected state).
- Jobs: a band behind Charcoal headline words; the ask fill with a Charcoal label (14.85 to 1); B on the Charcoal tile (14.85 to 1).
- Limits: on Newsprint the lead measures 1.12 to 1 and disappears. B on Newsprint takes Charcoal or Moss, or sits on a Highlighter or Charcoal tile; that is a change to how the wordmark is shown, and the sheet must show it plainly. A chart's emphasis becomes a band behind the labeled value, never a lime mark.
- Why, and examples: Grist's chartreuse band behind brown-black type; USAFacts' mint highlight behind headline words; the Guardian's yellow asks; GOV.UK's yellow focus state; Pinterest's 2026 Wasabi, "electric chartreuse" (trend report). Documented.
- Watch: a pale fill is the color most likely to dull on newsprint, where Newspaper Club warns colors "won't look as bright", and a highlighter that dulls loses its point. Not tested on press.
- Party reading: Moderate. The Harris campaign's July 2024 banner used a neon green; whether readers still connect it is a Hypothesis.

#### 6. Ballot Violet

- Feel: community and civic heritage. The suffrage banner, the polling place, the neighborhood meeting.
- Lead: Ballot Violet `#7552B3`. Supporting: Deep Violet `#4B2E83` (ink for text on Newsprint, 7.38 to 1), Suffrage Gold `#E0B13A` (a fill under Charcoal text), Lavender `#B39DDB` (the partner for text on Charcoal).
- Jobs: B and lever on Newsprint (4.12 to 1) and Charcoal (3.22 to 1); the ask fill with a White label (5.81 to 1); the emphasis point.
- Why, and examples: purple, white and gold were the National Woman's Party's colors (National Park Service). Purple or indigo leads at Vote.org, Democracy Works, iCivics, Votebeat and The 19th. WGSN lists Fresh Purple for A/W 26/27 (snippet) and Pinterest names Plum Noir for 2026. Documented except where marked.
- Watch: five of the civic groups I checked already lead with purple, so this scheme would look like the category (Plausible). In the deuteranopia simulation Ballot Violet differs from Press Cobalt by only 4.6, so do not show both on one board side by side without labels.
- Party reading: Low as a party. Moderate as a meaning: purple is the blend of the two party colors, and it can tell a reader the brand stands between the parties, which is a different claim from DR-93's one standard (design judgment, Plausible).

#### 7. Evergreen (alternate)

- Feel: warm and community. Parks, libraries, the market on a Saturday.
- Lead: Evergreen `#33704A`. Supporting: Marigold `#E9A93A` (a fill under Charcoal text), Clay `#C98B6B` (a warm pink-brown fill, after WGSN's S/S 27 Clay), Fern `#8FC29A` (the partner for text on Charcoal).
- Jobs: B and lever on Newsprint (4.19 to 1) and Charcoal (3.17 to 1); the ask fill with a White label (5.90 to 1); the emphasis point.
- Watch: Evergreen differs from Patina by 13.1, so the two read as near neighbors; a board should show only one of them. A reader with protanopia cannot tell Evergreen from an error red (1.3).
- Party reading: Low to Moderate. Green is the Green Party's color and reads as ecology.

#### 8. Press Cobalt (alternate, highest risk)

- Feel: modern editorial. The color most current in forecasts and in new digital newsrooms.
- Lead: Cobalt `#3B5BDB`. Supporting: Periwinkle `#9AA8FF` (the partner for text on Charcoal), Apricot `#F4B183` (a warm fill under Charcoal text).
- Jobs: B and lever on Newsprint (4.02 to 1) and Charcoal (3.31 to 1); the ask fill with a White label (5.67 to 1); the emphasis point.
- Why, and examples: WGSN's Colour of the Year 2027 is Luminous Blue and Pinterest names Cool Blue for 2026 (trend reports); Rest of World declares an electric blue theme color and Semafor uses cobalt in its CSS. Documented.
- Party reading: High. A bright, saturated blue is the color of the Democratic side on election maps, the reading is in this week's headlines, and Schloss and Palmer found party readings sharpen on Election Day, when Track pieces run. I would show it only if Dustin asks to see the risk.

### Research view on which six to draw

As a design judgment for the color designer, who owns the pick: six distinct hues with the lowest combined risk are Patina (civic), Federal Ink (institutional), Signal Orange (editorial), Archive Ochre (archival), Highlighter (modern) and Ballot Violet (community and civic heritage). Evergreen can replace Patina if Dustin prefers green to teal; the two should not both appear. Press Cobalt stays out unless Dustin wants to see a blue beside the risk. On evidence and arithmetic together, Patina carries the strongest case: it sits in the band, has trend support and peer use, and a low party reading, at the cost of two fixes (chart context off Stone, and the diverging scale and focus ring off Verdigris). The seventh panel shows today's palette with Pillar Red's own measured values from the first row of the table.

### Points for the color designer to settle on the sheets

1. Error state. Today error marks are Pillar Red. If a sheet's lead is not red, say whether error keeps a red as a state color (section 10 separates state color from identity color) and show it with its icon and word.
2. Token conflicts. Patina and Federal Ink overlap the diverging scale's ends (Prussian and Verdigris, DR-54) and the focus ring (Verdigris). Show the change on the sheet.
3. One neutral party ink. Every sheet's chart keeps party marks in Charcoal with names printed (Rule 01.2), and no sheet sets its lead against a supporting color as two sides.
4. Print. A press proof on the real stock before any direction is approved for print; Newspaper Club cannot print spot colors, so each lead needs a process build.

## Sources

All pages were checked on November 7, 2026.

| Source | Publisher and date | URL | How I read it |
|---|---|---|---|
| Pantone Color of the Year 2026, Cloud Dancer | Pantone | https://www.pantone.com/color-of-the-year/2026 | Opened (name only) |
| "Pantone names 2026 Color of the Year" | NBC News, December 4, 2025 | https://www.nbcnews.com/pop-culture/pop-culture-news/pantone-names-2026-color-year-rcna247366 | Opened |
| Pantone 2026 coverage calling it the first white | Manila Bulletin and others, December 4, 2025 | https://mb.com.ph/2025/12/04/pantone-announces-its-2026-color-of-the-year-cloud-dancer | Snippet |
| Colour of the Year 2026, Transformative Teal | WGSN, September 3, 2024 | https://www.wgsn.com/en/blogs/colour-year-2026-transformative-TEAL | Opened |
| Colour of the Year 2027, Luminous Blue, and S/S 27 key colours | WGSN press release, April 29, 2025 | https://www.wgsn.com/en/wgsn/press/press-releases/wgsn-and-coloro-reveal-colour-year-2027-luminous-blue-and-s/s-27-key | Opened |
| A/W 26/27 key colours | Mr Mag and others, 2024 | https://mr-mag.com/wgsn-and-coloro-announce-colour-of-the-year-2026-transformative-teal-and-the-key-colours-for-a-w-26-27 | Snippet |
| "From Cool Blue to Persimmon: Meet the 2026 Pinterest Palette" | Pinterest Newsroom, January 14, 2026 | https://newsroom.pinterest.com/news/from-cool-blue-to-persimmon-meet-the-2026-pinterest-palette/ | Opened |
| Adobe 2026 Creative Trends | Adobe | https://business.adobe.com/resources/creative-trends-report.html | HTTP 503; master brief snippet |
| Canva design trends 2026 | Canva, December 2025 | https://www.canva.com/newsroom/news/design-trends-2026/ | HTTP 403; master brief snippet |
| `@financial-times/o-colors` 6.7.1, palette file | Financial Times Origami, npm | https://registry.npmjs.org/@financial-times/o-colors/-/o-colors-6.7.1.tgz | Opened |
| `@guardian/source` 14.0.0, generated palette | Guardian News and Media, npm | https://registry.npmjs.org/@guardian/source/-/source-14.0.0.tgz | Opened |
| Semafor home page | Semafor, November 7, 2026 | https://www.semafor.com/ | Rendered and CSS |
| "Newsweek unveils historic redesign" | Editor and Publisher, September 25, 2025 | https://www.editorandpublisher.com/stories/newsweek-unveils-historic-redesign,257943 | Opened |
| Grist home page | Grist, November 7, 2026 | https://grist.org/ | Rendered and CSS |
| Rest of World home page | Rest of World | https://restofworld.org/ | Theme color and CSS |
| The 19th home page | The 19th | https://19thnews.org/ | Rendered and CSS |
| Votebeat home page | Votebeat | https://www.votebeat.org/ | Rendered and CSS |
| CalMatters home page | CalMatters | https://calmatters.org/ | CSS only (bot check) |
| USAFacts home page | USAFacts | https://usafacts.org/ | Rendered and CSS |
| Democracy Works, "Introducing Our New Brand Identity" | Democracy Works, February 4, 2026 | https://www.democracy.works/news/introducing-our-new-brand-identity | Opened; site rendered |
| "Vote.org: Rebranding democracy" | Interactivism, 2020 | https://interactivism.com/work/vote-rebranding-democracy/ | Opened; vote.org rendered |
| iCivics home page | iCivics | https://www.icivics.org/ | Rendered and CSS |
| "Changes to GOV.UK" | GOV.UK, June 25, 2025 | https://www.gov.uk/guidance/changes-to-govuk | Opened |
| GOV.UK Design System, Colour | Government Digital Service | https://design-system.service.gov.uk/styles/colour/ | Opened |
| GOV.UK Frontend, brand refresh changes | Government Digital Service | https://frontend.design-system.service.gov.uk/brand-refresh-changes/ | Opened |
| "How we refreshed the Government Digital Service brand" | GDS design notes, April 4, 2025 | https://designnotes.blog.gov.uk/2025/04/04/how-we-refreshed-the-government-digital-service-brand-and-what-were-doing-differently | Opened |
| GOV.UK refresh cost and agency | Design Week and PublicTechnology, June 2025 | https://www.designweek.co.uk/we-need-to-talk-about-the-gov-uk-redesign-again/ | Snippet |
| USWDS color overview | U.S. General Services Administration | https://designsystem.digital.gov/design-tokens/color/overview/ | Opened |
| "America250 got a rebrand and new logo" | YELLO, Hunter Schwarz, January 9, 2024 | https://www.yellopolitics.com/p/america250-got-a-rebrand-and-new | Opened |
| America250 identity by Chermayeff and Geismar and Haviv | Design Week | https://www.designweek.co.uk/chermayeffgeismarhaviv-creates-red-white-and-blue-america250-semiquincentennial-identity/ | Snippet (page refused access) |
| "When Republicans Became 'Red' and Democrats Became 'Blue'" | Smithsonian Magazine, Jodi Enda, October 31, 2012, updated October 21, 2024 | https://www.smithsonianmag.com/history/when-republicans-were-blue-and-democrats-were-red-104176297/ | Opened |
| "Political Colors: An Explainer" | Rock the Vote, June 4, 2026 | https://www.rockthevote.org/explainers/political-colors | Opened |
| Schloss and Palmer, "The politics of color" | Psychonomic Bulletin and Review 21, 1481 to 1488, April 15, 2014 | https://psy311.wichita.edu/wp-content/uploads/2020/07/Schloss_PBR_abstract_2014-1.pdf | Abstract opened; citation checked on Crossref |
| Furrer and others, "Red and blue states: dichotomized maps mislead and reduce perceived voting influence" | Cognitive Research: Principles and Implications 8, 11, 2023 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9908792 | Opened |
| "Kamala Harris is wooing the cynical Gen Z vote" | Fortune, Eva Roytburg, July 24, 2024 | https://fortune.com/2024/07/24/kamala-harris-is-wooing-the-cynical-gen-z-vote-with-coconut-tree-and-brat-memes/ | Opened |
| Wear Orange, About | Everytown for Gun Safety | https://wearorange.org/about/ | Opened |
| "Symbols of the Women's Suffrage Movement" | National Park Service, last updated March 4, 2024 | https://www.nps.gov/articles/symbols-of-the-women-s-suffrage-movement.htm | Opened |
| Gadsden flag history | Snopes, January 8, 2021 | https://www.snopes.com/news/2021/01/08/yellow-gadsden-flag-carries-a-long-and-shifting-history/ | Snippet |
| ANSI Z535.1 safety colors | In Compliance Magazine, July 2023 | https://incompliancemag.com/ansi-z535-1-safety-colors-in-focus/ | Snippet |
| Traditional printing design guide | Newspaper Club | https://www.newspaperclub.com/create/design-guides/traditional-printing | Opened |
| Coated and uncoated | Pantone support | https://support.pantone.com/en/what-does-the-terms-coated-and-uncoated-mean-in-the-pantone-graphics-system | Snippet |
| SNAP, coldset dot gain and ink limits | Printer and publisher specification pages | https://adrates.thestar.com.my/popup_newspaper_requirements.php | Snippet, secondary |
| Machado, Oliveira and Fernandes, color-vision simulation matrices | IEEE Transactions on Visualization and Computer Graphics 15(6), 2009 | Matrices applied from the published values | Used in a script; paper not reopened |

## Claims I could not verify

- That Cloud Dancer is the first white Pantone has named: several outlets say so; Pantone's own page does not.
- Pantone 2025 Mocha Mousse and WGSN's A/W 26/27 key colours (Wax Paper, Fresh Purple, Cocoa Powder, Green Glow): search snippets only.
- Adobe's and Canva's 2026 trend lists: both pages refused or failed today; I rely on the master brief's October 20 snippets.
- Design Week's report that the America250 designers addressed red and blue's party meaning: the page refused automated access, and I did not work around it. The YELLO quote from Brian Collins stands on its own.
- The GOV.UK refresh's cost (£532,000) and agency (M+C Saatchi): press reports only.
- SNAP's dot gain and ink limits for coldset newsprint: secondary pages only; I did not open SNAP or ISO 12647-3.
- ANSI Z535's color meanings: secondary pages; the standard is sold and I did not open it.
- The Gadsden flag's Tea Party history: Snopes and encyclopedia pages, no primary record.
- The Forward Party's colors: two encyclopedia mirrors disagree (one lists indigo, blue and red; a later one lists purple, cyan, orange, navy, blue and red), so I left it out.
- That deep navy reads less partisan than bright blue, that purple reads as "between the parties", and that the 2024 lime green still reads as Democratic: I found no reader study for any of these, so each stays Plausible or a Hypothesis.
- Notus.org now shows a different masthead ("The Washington Sun"); I did not research why and used nothing from it.
- The Marshall Project and Code for America returned HTTP 403, so they are not in the survey.

## Tested

- A WCAG 2.2 contrast script, checked against the guide's published values (Pillar Red 2.96, Prussian 9.42 and Charcoal 13.29 to 1 on Newsprint); every ratio in this report comes from it.
- The band thresholds (0.116, 0.118, 0.183, 0.198 and 0.202 relative luminance), derived from Newsprint's and Charcoal's luminance.
- The FT and Guardian palettes, read from their official npm packages, and their contrast on FT paper, Semafor's cream, White and Newsprint.
- Home pages of Semafor, Grist, USAFacts, Democracy Works, Vote.org, iCivics, Votebeat, The 19th and notus.org, rendered in Playwright at 1280 by 900 px and viewed; CSS color counts for these and for ProPublica, CalMatters, Texas Tribune, Rest of World, Pudding, Center for Civic Design, League of Women Voters, Braver Angels and Ballotpedia.
- Twelve candidate leads rendered beside Pillar Red as an ampersand in Lora Bold, a button with a White label, a dot and a word in Inter Tight 800, on Newsprint and on Charcoal, and viewed.
- Protanopia, deuteranopia and tritanopia simulation (Machado 2009, full severity) with CIEDE2000 differences for each lead against Stone, against Pillar Red and against each other; grayscale contrast of each lead against Stone.

## Not tested

- How any lead prints on newsprint or uncoated stock; no press proof, no CMYK build, no Pantone match.
- How readers read any of these colors for party; no survey or reader panel was run.
- APCA or any contrast method beyond WCAG 2.2.
- Calibrated display rendering; the swatch render used an uncalibrated headless browser.
- The Civic Line icons, the wordmark master and the lockmark in the new colors; that is the color designer's sheet.
- Any color at 16 px or in a small chart; the swatch render showed 64 px ampersands and 15 px button labels only.
- Pages that refused access or served a bot check (Design Week, Adobe, Canva, CalMatters content, The Marshall Project, Code for America).

## Change log

- Created `work/handoffs/phase-2/20261107_Color-And-Aesthetic-Research.md` (this report).
- Working files, kept outside the project in the session scratchpad and not for shipping: the contrast, color-vision and table scripts, the swatch page and its render, and screenshots of third-party sites (study only, never to be shipped, as the master brief's rights rules require).
- Nothing else in the project was edited. Nothing was committed or pushed.
