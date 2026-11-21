# Chat 11, design director's notes

Started November 21, 2026, 18:56 UTC. Owner: oa-design-director. Files held this chat: `work/handoffs/phase-4/20261121_Chapter-20-Plan.md`; `work/handoffs/phase-4/20261121_Web-Page-Specs.md`; `work/build/scripts/phase-4/phase4_ch20_build.py` and its outputs (`work/build/guide/chapters/20-web.json`, `work/build/guide/specimens/s-20-*`, `manifest-web.json`). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ac32a0f7-d562-5d93-9aba-0ef59f7ca891/scratchpad/c11/design-director/`.

## Where I am

19:24 UTC. The plan is written (`work/handoffs/phase-4/20261121_Chapter-20-Plan.md`, 19:15 to 19:18 UTC). The page specs are handed over in full (DD-1 at 19:20, DD-2 at 19:24). Next: the generator `phase4_ch20_build.py`, its words and failure plates, while the engineer draws the pages; then the build once the kit's plates exist.

## Contracts

- **DD-1. Masthead, menu and footer, 19:20 UTC.** `work/handoffs/phase-4/20261121_Web-Page-Specs.md`, sections 0 to 4. Section 0: rules for every page (tokens, grid by container query, head, body order, skip link, sections for C5). Section 1: the kit views I ask for (A04 masthead and menu, A05 footer, A06 home, A07 article, A08 Act page, A09 share preview, A10 favicons; ids are proposals). Section 2: the masthead at each width with measured positions (L3 and the seven parts in one 80 px bar from 64em, the switch on a 44 px row beneath at the right edge; L3 and Menu from 48em to 64em; L1 from the 24 px master at 390; L1 from the 16 px master under 24.375em). Section 3: the menu, chapter 18's dialog with the switch at its top. Section 4: the footer, four link groups with Help fourth, and Rule 08.2's lockmark row with the Illustrative address. Chapter 18's masthead, switch and dialog script are read from their files, never copied.
- **DD-2. The page specs, sections 5 to 9, 19:24 UTC.** Same file. Section 5: the home page (four pillar sections under one Charcoal band of head cells, each with its card; the atlas's section with its questions panel and S10). Section 6: the article (the chat 10 sample finished: the 24 px pillar row, the count panel, two body sections, the step and the end mark). Section 7: the Act page (the status panel with Rule 11.6's upright steps and the ask in the first screen, the agency's summary panel, S66, the hinge divider, the steps, the comment panel with the ask again, the rule at a glance). Section 8: the share preview (the proof card with a Charcoal foot band). Section 9: the favicons (C6 as written, B in signature red). Waiting facts are marked R3 and R5 in place.

## Routine calls

- D4-xxx | Chapter 20 has 11 rules in three groups and one extra ("The pages and their files") | The brief asked for about 10; eleven carry the owed criteria (2.4.2, 3.1.1, 3.1.2's markup, 3.2.6) with no rule doing two jobs
- D4-xxx | The home page opens on the 48 px pillar row, its four cells the head of four sections (Explain, Track, Connect, Act), each with one piece under it; the row spreads across the four card columns at 1440 px and breaks two to a line at 1024 px | Rule 09.1 places the 48 px row near the top of a page that introduces the four pillars, and breaks it after Track below about 1,080 px; each cell is its section's one dark panel (Rule 05.1, DR-310)
- D4-xxx | The masthead sets L3 and the seven parts in one 80 px bar from 64em, and the theme switch on a 44 px row beneath at the right edge | Measured: L3, 32 px and the parts take 894 px, which fits the 944 px a 1,024 px window gives; the switch (410 px) fits beside them nowhere under 1,440 px; AL-07 puts the switch after the parts, never above them
- D4-xxx | L1 keeps the 24 px master at 390 px and takes the 16 px master under 24.375em | Rule 03.6 and the approved masthead proof set the 24 px master on a 390 px phone, where it clears Menu by 26 px; at 360 px it would clear it by 4 px (AL-05 asked for the 16 px master at 390 too; told in Requests)
- D4-xxx | The masthead never sticks, and the footer keeps the page's lockmark | Rule 08.2, once in a view: L3's lockmark and the footer's never share a screen on pages this long, and a masthead that scrolls away needs no scroll padding (AL-12)
- D4-xxx | Every part of the masthead stays in its ink, Subscribe included | Rule 05.3: the view's one red goes to the step a reader can take now; AL-16
- D4-xxx | In the dark theme every Charcoal panel keeps its ground and draws a 1 px `--oa-color-border-hairline-on-charcoal` edge (3.10 to 1) | Without it a panel vanishes into the page and the section loses its signal (Rule 05.1's reason)
- D4-xxx | The share preview takes the identity proofs' link-preview card with a Charcoal foot band holding the wordmark and the 96 px sign-off | The proof card, all Newsprint, would measure about 87 percent Newsprint (estimate, to be measured), past Rule 05.1's 85; the chat 10 post's foot band measured 66.3
- D4-xxx | Rule 20.4's passage in another language is the Great Seal's motto, `<i lang="la">E pluribus unum</i>` | Our three pages print no passage in another language, and AL-03 asks for a real phrase, never an invented one; the editor and the accessibility lead may name another
- D4-xxx | The article ends on "Find the districts where you live", pointing to the Census Bureau's "Individual State Descriptions: 2022 Census of Governments" (report G22-CG-ISD, April 30, 2024) | A real step a reader in any state can take (W08); the page was read 19:03 UTC and gives "a separate summary for each state and the District of Columbia"

## Done

## Requests

- **R1, engineer:** a first-screen view, `<width>-<theme>-screen`, the page clipped to one window (900, 768, 844, 780 px), for the opener and Rule 20.5's plate.
- **R2, engineer:** in C5, the footer counts as its own section (`data-oa-section="Footer"`), so the last content section is never charged two dark panels.
- **R3, main session:** three facts no file holds: (a) whether H.R. 7008 had a House committee hearing and (b) a committee vote, for the Track card's steps 2 and 3 (Rule 11.1; the research ledger's P7-019 may hold them); (c) whether docket FDA-2025-N-2699 had an advance notice of proposed rulemaking before November 17, 2026, for step 1 of Rule 11.9 on the Act page and the home card. Until they land, those steps are drawn from no guess.
- **R4, engineer:** each page frame carries only the chart drawing its width shows (the desk drawing from 48em, the phone drawing under it); chat 10's frames carried both.
- **R5, main session:** for Rule 01.22's two sides at the same length, what the proposed rule's preamble reports from those who asked for the change and from any who objected, with page numbers, from govinfo's PDF. Until it lands, the Act page's "What supporters and opponents have said" is left out of the drawing, and Rule 20.8's plate notes it.
- **To the accessibility lead (for agreement, no file):** 390 px keeps L1's 24 px master (Routine call above), and Rule 20.4's passage is the Great Seal's motto.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

## Not tested
