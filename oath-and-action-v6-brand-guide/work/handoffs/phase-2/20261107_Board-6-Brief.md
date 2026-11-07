# Brief: Board 6, four explorations

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the main session. Dustin's direction is DR-104 to DR-107 and the studio's calls D2-320 to D2-322 (`work/ledger/20261020_Decision-Log.md`). He liked the stage A guide and asked for four things, in his words below. Show options he can pick from, with one recommendation each. Do not question the direction: Newsprint ground, the type faces, the hinge idea and the overall look all stand.

## Read first
- `CLAUDE.md`; chapter 02's writing section `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md` (binding on every word you print).
- The decision log from DR-36 on, especially DR-48 and DR-58 (no party owns a color), DR-67 (R9, R10, R11, R13), DR-93 (one standard), DR-95 to DR-107.
- The guide as it stands: https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF, built locally at `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` (chapters 03, 04, 05, 08 and the proofs matter most). Tokens: `work/build/tokens/tokens.css`. Identity masters: `work/build/assets/identity/`. Civic Line icons: `work/build/assets/civic-line/` (inventory CSV and JSON, catalog HTML, SVGs in red-black, black and newsprint editions).

## The four sections

### 1. The grid keeps one job, and a simpler bill tracker (systems designer)
Dustin: "The grid system, I feel like it's trying to represent and track too many things ... I want to include the grid, and it's good on the mastheads or the headers and footers ... keep it to one use ... a bill tracker should be much simpler, like a line with dots or a 1, 2, 3, 4, 5, 6 step process. That grid system's not clear. I want everything to be clear."
- Show where the lockmark stays (masthead, page header, footer, a sign-off) and list what retires (tracker progress, series routes, pillar corners, coded grids, the grid in the kicker), as a short before and after.
- Propose plain stages. Today's nine (Filed, Referred, Hearing, Out of committee, Passed one chamber, Passed both chambers, Final text agreed, Signed, In effect) may become six a newcomer reads at once; say what each covers and how a skipped or failed stage shows.
- Draw three or four tracker options, for example a line with dots, numbered steps 1 to 6, a segmented bar with the stage word, and a vertical timeline for a bill's own page. Show each in the four-bill list Dustin attached (the invented bills H.4212, S.0876, H.1180 and H.3301, labeled Illustrative once at the head) at 360 px and at 1024 px, on Newsprint and on Charcoal, with "you can take part now" marked by shape and words as well as the view's one working red (Rule 05.3), and a stage that never happened.
- Accessibility: every state named in words; nothing told by color alone; targets and contrast measured.

### 2. Four pillar icons from the Civic Line set (icon designer)
Dustin: "revisit the civic icons. I'd like to use those and maybe see just a few thoughts on the four icons for the four pillars."
- Review all 122 icons. The pillars today are CL-019 Explain, CL-020 Track, CL-021 Connect and CL-022 Act (DR-04). Propose three sets of four, one of which may keep today's set with any refinement in how it is used, and say why each icon fits its pillar and how the four read as a family.
- Show each set at 16, 24, 48 and 128 px (16 px one color, R10), in the pillar row "Explain → Track → Connect → Act" with each word beside its icon (R9), on a section opener, in a kicker, and as a two-color tile on Charcoal (R13). The pillar no longer needs the grid corner.
- A quick naming test of your own: could a newcomer match each icon to its word? Say which pairs risk confusion.

### 3. More stacked lockups (identity designer)
Dustin, of L2 (OATH over ACTION, with ampersand B large at the right, offset): "I don't know that I like that. Can you give me a few more variations of stacked?"
- Draw five or six stacked variations from the approved masters at today's width with ampersand B as refined, for example: B centered between the two words on its own line; B ending the first line ("OATH &" over "ACTION"); B starting the second line; both words flush left with B hung in the left margin; a centered stack; a tight square stack for avatars. Redraw no letter (D2-321).
- Show each beside today's L2 at the same cap height, at 72 px and at a large size, on Newsprint, Charcoal and Prussian (one color White on Prussian), in a square avatar tile and on a poster corner, with its clear space and minimum size measured.

### 4. Six identity sheets in six color schemes (research lead, then the color designer)
Dustin: "six mock-ups, just one page brand identity sheets for Oath & Action, but use six totally different color schemes ... research what's cool in terms of design aesthetic. And take different design approaches and feels, one way could feel more modern, one way more civic, but keep the newsprint concept ... I want to see, if red wasn't at the forefront, what other colors would work."
- The research lead writes `work/handoffs/phase-2/20261107_Color-And-Aesthetic-Research.md`: what leading editorial, civic and news brands and design studios are doing with color and feel in 2025 and 2026, newsprint and paper palettes, how lead colors read for party in the United States (red, blue, purple and others), and six to eight palette directions with sources.
- The color designer then makes six one-page sheets, each a different feel (for example modern, civic, editorial, archival, warm and community, institutional), each with a lead color that is not red. Every sheet keeps Newsprint as the ground and Charcoal as the text ink, and shows the wordmark with ampersand B in the lead color, the palette with hex values and measured contrast, the three faces, the Civic Line icons in the new two-color edition, the lockmark, a sample article card with a hinge headline, a button and its states, and a small chart. Each sheet names its feel, its lead color's jobs and how it could read for party.
- A seventh panel shows today's palette as the reference, at the same size.

## Where work goes
- Section folders: `work/boards/phase-2/board-6/tracker/`, `pillar-icons/`, `stacked/`, `color-sheets/`. Each section is one self-contained HTML page that renders on its own and sets every option at true size, built by a script you write in `work/build/scripts/phase-2/` (`board6_<section>_build.py` or `.js`). Load Inter, Inter Tight and Lora from Google Fonts, as the guide does; inline every SVG; no other outside resource.
- Notes: `work/handoffs/phase-2/20261107_Board-6-<Section>-Notes.md` with what you made, your recommendation and why, your routine calls as "D2-xxx | decision | reason" lines, Tested and Not tested kept apart, and a change log.
- Never touch `source/`, `work/ledger/`, the identity or Civic Line masters (read and place only), the guide's chapters, specimens, shell or tokens, or any existing board. Do not commit or push.

## Checks
- Render your page with Playwright (preinstalled) at 1440 and 390 px and look at every option, at twice size where detail matters.
- `node work/build/scripts/phase-2/dataviz_check.js <your page> --board` (install `cd work/build && npm install --no-save axe-core@4.10.2 style-dictionary@5.8.0`, both together). Text 13 px or larger except a true-size mark; contrast measured; no em dashes.

The bar is the best brand studio in the world: calm, exact and clear, with every option drawn well enough to pick.
