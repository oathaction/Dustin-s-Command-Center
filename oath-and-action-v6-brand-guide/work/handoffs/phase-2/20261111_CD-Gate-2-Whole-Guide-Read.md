# Creative director's whole-guide read at Gate 2 (DR-221)

Oath & Action Edition 06, November 11, 2026. Written by the creative director (`oa-creative-director`), a subagent of the main session, under task 1 of `20261111_Gate-2-Brief.md`. The scores, reasons and fixes are also in `20261111_Gate-2-CD-Scores.json`, made from the same data.

The page read: the frozen copy in the scratchpad's `gate-2/review/guide.html`, 8,965,291 bytes, commit 043ad4d8, published as version 7. Sixteen chapters built at three stages: A (01 to 08, November 6 and 7), B (09 to 12, November 8 to 10) and C (17, 18, 19 and 26, November 10 and 11), with the identity proofs.

## Decision or verdict

Sixteen of the 17 items are ready. Chapter 26 is not: it scores 3 on usefulness because its font link and chapter 06's give a builder two different sets of weights to load (M1). The fix is a few lines in two generators and one declaration in the shell, and it adds no font bytes.

The book holds together where a builder works. The shell draws every rule, plate, specification table and cross-reference the same way in all 16 chapters, and the places where a stage A rule and a stage C rule describe the same thing now agree (states, trackers, current marks, the crop of B, red off Prussian). The drift sits where a reader first meets a chapter. Ten chapters open on words and six on a plate of their subject. Failure plates carry three kinds of caption and a do-not-publish bar on some only. Rule titles double in length from chapter 02 to chapter 18. None of these breaks a rule, so they go back as Should fix. I would land S1 and S2 in this fix pass all the same, because they are what makes a reader feel one hand from the first screen of every chapter, the bar Dustin set for this guide.

The addendum scores the preview's new front pages as an eighteenth item. It is not ready: craft and brand fidelity score 3, because the “Where to start” page is three lists of underlined sentences with no mark of the system on it and the colophon ends the book with no signature (A1). The words and the license are right.

## Scores

| Item | Stage | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Must | Should | Ready |
|---|---|---|---|---|---|---|---|---|---|---|
| Chapter 01, Purpose | A | 4 | 4 | 4 | 4 | 5 | 4 | 0 | 3 | yes |
| Chapter 02, Voice | A | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 3 | yes |
| Chapter 03, Identity | A | 4 | 4 | 4 | 5 | 4 | 4 | 0 | 4 | yes |
| Chapter 04, The Ampersand and the hinge | A | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 4 | yes |
| Chapter 05, Color | A | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 4 | yes |
| Chapter 06, Type | A | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 2 | yes |
| Chapter 07, Layout and spacing | A | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 3 | yes |
| Chapter 08, The lockmark | A | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 3 | yes |
| Chapter 09, Pillar icons | B | 4 | 4 | 5 | 4 | 4 | 4 | 0 | 1 | yes |
| Chapter 10, Topic and atlas symbols | B | 4 | 4 | 4 | 5 | 4 | 4 | 0 | 0 | yes |
| Chapter 11, Status and utility icons | B | 4 | 4 | 4 | 5 | 4 | 4 | 0 | 2 | yes |
| Chapter 12, Graphic devices and patterns | B | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 3 | yes |
| Chapter 17, Motion and states | C | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 1 | yes |
| Chapter 18, Components and interaction | C | 4 | 4 | 4 | 5 | 4 | 4 | 0 | 2 | yes |
| Chapter 19, Accessibility | C | 4 | 4 | 4 | 4 | 5 | 4 | 0 | 1 | yes |
| Chapter 26, Tokens and how to choose them | C | 4 | 4 | 4 | 3* | 4 | 4 | 1 | 2 | no |
| Identity proofs | A, revised at B and C | 4 | 4 | 5 | 4 | 4 | 4 | 0 | 1 | yes |
| Gate 2 preview: Where to start, the font license and the colophon | Gate 2 preview | 3* | 4 | 3* | 4 | 4 | 4 | 1 | 4 | no |

An asterisk marks a score under 4.

## Reasons

One sentence per score, in the rubric's order.

**Chapter 01, Purpose** (`#purpose`). Fixes: S1, S2, S9.

- Craft 4: The four pillar pieces sit at true size in one 340 px column each and turn at the hinge divider to one red step, though 11 of the 24 failure plates carry no do-not-publish bar.
- Clarity 4: The instruction line and the two intro paragraphs say what the chapter is for, and the group index sorts 24 rules into six jobs on the first screen.
- Brand fidelity 4: Red discipline holds in every piece, but the first screen is words alone, so with the wordmark covered it reads as Oath & Action only through Newsprint and the type.
- Usefulness 4: Every rule ends in a builders line, while 14 of the 24 rules carry no Specifications block, the template's item 6.
- Evidence honesty 5: Twelve sources, Explain and Track quote real records with dates, and Connect and Act carry Illustrative at their heads.
- Accessibility 4: Every piece reads in gray, the party marks carry names, and the photographs carry captions.

**Chapter 02, Voice** (`#voice`). Fixes: S1, S2, S8.

- Craft 4: Each before and after is set in one consistent pair with struck and bold words, though the two “Terms.” labels draw as a slanted Inter the page never loads, and 22 of 27 failure plates have no bar.
- Clarity 4: Twenty-one rules in five groups, each named for what it teaches, with a worked sentence under every one.
- Brand fidelity 4: The brand lines appear word for word in their own places, and Lora Italic carries only quoted lines.
- Usefulness 4: A writer can apply every rule from its pair alone, and Rule 02.22's house rules give the checklist other chapters cite.
- Evidence honesty 4: Each quoted line names its source, and the invented article carries Illustrative beside it.
- Accessibility 4: Struck and bold words also change in weight and line, so the edit reads without color.

**Chapter 03, Identity** (`#identity`). Fixes: S1, S2, S8, S11.

- Craft 4: The eight lockups hold their spacing at 2x and the minimums table is exact, though none of the eight failure plates carries the do-not-publish bar, the chapter where a lifted image does most harm.
- Clarity 4: The intro defines wordmark, lockup and x before any rule uses them.
- Brand fidelity 4: Masters are placed whole, red stays on B, and the four surfaces are measured, yet the first screen shows no mark at all.
- Usefulness 5: Each lockup has its job, screen and print minimums, its replacement below the minimum and its master file.
- Evidence honesty 4: Minimums cite our own measurements with their month, and the partner rule names its approval.
- Accessibility 4: Each mark in the lockup plate carries its name, size and minimum in text beside it.

**Chapter 04, The Ampersand and the hinge** (`#ampersand`). Fixes: S1, S2, S5, S7.

- Craft 4: Hinge headlines at 56, 44 and 26 px take B from the right master, though Rule 04.5's plate stacks the two compact masters at the left and leaves half its frame empty.
- Clarity 4: The intro lists every place the hinge appears before the rules take them one by one.
- Brand fidelity 4: B's red is spent once per composition, the divider and the crop take ink, and the crop's corner is fixed.
- Usefulness 4: Three masters with their pixel ranges, the divider's 12 px clear line and the crop's 25 to 40 percent are all stated.
- Evidence honesty 4: Bases are design judgment or our measurements, and the founder's approval of the badge is named.
- Accessibility 4: The hinge divider is hidden from screen readers in the shell's code, and each plate's point is also in its caption.

**Chapter 05, Color** (`#color`). Fixes: S1, S2, S7, S10.

- Craft 4: The ask on four surfaces is exact, though the keyline on red is drawn with a box shadow here and in 04 and 11, where 01, 02 and chapter 18's code draw a 1 px border.
- Clarity 4: The seven colors and their jobs are named in the first paragraph, though Rule 05.3's body runs about 230 words before its plate.
- Brand fidelity 4: One working red with its order of precedence, red off Prussian, and tints kept off identity marks, all shown; the first screen still shows no color.
- Usefulness 4: Every pair carries its ratio and token, and the palette plate gives values and shares.
- Evidence honesty 4: Ratios are computed on token values by WCAG's formula, and Rule 05.4 points to Rule 17.8 as the reference plate.
- Accessibility 4: Every state has a word or a shape, the focus ring measures 3.37 to 1, and red on Newsprint takes its keyline.

**Chapter 06, Type** (`#type`). Fixes: S1, S2.

- Craft 4: Three faces each in one job, hung quotation marks and tabular figures hold at 2x, and the only text under 13 px sits in the failure plate that teaches the floor.
- Clarity 4: Sizes in rem are explained before the scale, and each rule names one decision.
- Brand fidelity 4: Inter Tight 800 shares the wordmark's voice, which is why the page reads as ours with the logo covered.
- Usefulness 4: The scale, the floor, tracking and measure are exact, but Rule 06.1's builders link names one weight set and Rule 26.5's names another (see M1).
- Evidence honesty 4: Bases separate design judgment from WCAG, and the measure rule labels SC 1.4.8 as advisory.
- Accessibility 4: No text under 13 px on screen, sizes in rem, and a reader's own text size wins.

**Chapter 07, Layout and spacing** (`#layout`). Fixes: S1, S2, S6.

- Craft 4: The spacing bands and heading proximity plates are clean, though Rule 07.2's grid plate sets its labels on the frame's own edge with no inset, in the chapter that teaches the 8 px scale.
- Clarity 4: Grid, spacing and breakpoints are introduced in two short paragraphs, with the 320 px requirement stated up front.
- Brand fidelity 4: The grid stays quiet and Newsprint carries the page, as the system intends.
- Usefulness 4: Eleven spacing steps with tokens, columns, gutters and margins for five widths.
- Evidence honesty 4: Bases cite the fifth edition audit and WCAG where they apply.
- Accessibility 4: Breakpoints in em and the 320 px rule are tested by the guide check.

**Chapter 08, The lockmark** (`#lockmark`). Fixes: S1, S2, S8.

- Craft 4: The four places at true size are exact, though the “4” in Rule 08.3's plate sets in Inter 800, a weight the page never loads, so the browser fakes it.
- Clarity 4: The approved explanatory line opens the chapter and names the four places in one sentence.
- Brand fidelity 4: The lockmark appears whole, fixed and once per view, with the lever as signature red.
- Usefulness 4: Four masters with pixel ranges, the 72 px corner margin and the feed test.
- Evidence honesty 4: Bases name our measurements and the founder's approvals with their months.
- Accessibility 4: Each place is named in text beside its plate, and chapter 19's results report no axe-core violation on the page at four widths.

**Chapter 09, Pillar icons** (`#pillar-icons`). Fixes: S2.

- Craft 4: The rows at 48 and 24 px align on one baseline and the pixel fits sit on whole pixels, though none of its four failure captions opens with “Fails Rule 09.n.” and one has no bar
- Clarity 4: The opener's pillar row says what the chapter is for before a word of the rules.
- Brand fidelity 5: With the wordmark covered the row reads as ours: the Civic Line, the order and one red underline beside a word.
- Usefulness 4: The file for each size, the four places allowed and the row on a phone.
- Evidence honesty 4: Bases name the founder's approval of the pixel fits.
- Accessibility 4: The current pillar is underlined and bold, so it holds without red.

**Chapter 10, Topic and atlas symbols** (`#symbols`). Fixes: none.

- Craft 4: The library's 125 drawings sit on one grid with words, IDs and typed chips at 2x, with every failure stamped and captioned.
- Clarity 4: The opener shows six drawings with their words and two typed chips, and the groups follow a maker's order.
- Brand fidelity 4: One line weight, round ends and one red accent make the family recognizable without the wordmark.
- Usefulness 5: Sizes, the list of 41, tiles, editions and the likeness test give a maker every decision.
- Evidence honesty 4: Typed chips match Atlas V7 IDs and the likeness test is named as its basis.
- Accessibility 4: Each drawing stands beside its word, so alt text stays empty and nothing is lost.

**Chapter 11, Status and utility icons** (`#icons`). Fixes: S1, S7.

- Craft 4: The six step glyphs and 18 utility icons are drawn at both sizes on a shared grid, and every failure is stamped and led “Fails Rule 11.n.”
- Clarity 4: The group index on the first screen separates trackers, records requests and agency rules, utility icons and messages.
- Brand fidelity 4: The take-part disc carries the one red and yields it to an error by rule.
- Usefulness 5: Six steps, three processes with statute bases, target sizes and a mark for every message.
- Evidence honesty 4: Records requests and agency rules cite 5 U.S.C. 552 and 553, and invented bills carry Illustrative.
- Accessibility 4: Every state is a shape and a word, targets are 44 px, and step numbers read in gray.

**Chapter 12, Graphic devices and patterns** (`#graphic-devices`). Fixes: S1, S2, S8.

- Craft 4: The marker, key, locator and owner frame are drawn with care, though the plates set “raises” in Inter 500 and a “4” in Inter 800, both outside chapter 06's weights, and four failure captions lack the lead.
- Clarity 4: The intro sorts the nine rules into devices that divide a page and devices that explain a system.
- Brand fidelity 4: Rule 12.4 now signs open areas with B or a watermark, and the red target alone carries a reform's red.
- Usefulness 4: Opacity tokens, the crop's measures by rule number and a never list for each device.
- Evidence honesty 4: Bases name the atlas's visual system and the fourth edition where devices come from them.
- Accessibility 4: Rules 12.2 and 12.4 mark the watermark and the crop decorative, and the layer diagram keeps every name flat and readable.

**Chapter 17, Motion and states** (`#motion-and-states`). Fixes: S3.

- Craft 4: The ten states at true size on both grounds agree with Rule 05.4's plate, and the players rest on their masters.
- Clarity 4: The opener shows the ten states, though five of twelve titles run past fifteen words.
- Brand fidelity 4: Red stays off Prussian, the identity players end on their masters, and every state has a shape.
- Usefulness 4: Nine motion tokens, the three behaviors and the states' tokens on both surfaces.
- Evidence honesty 4: Loop R1 carries its grade and the W3C draft its date.
- Accessibility 4: Reduced motion draws the last frame at once, and Play, Pause and Reset are named controls.

**Chapter 18, Components and interaction** (`#components`). Fixes: S3, S10.

- Craft 4: Callouts sit beside their parts, the code sets run live in both themes, and every failure is stamped.
- Clarity 4: Fourteen of 24 titles run past fifteen words, and the intro's second paragraph runs eleven lines before the opener, so the first screen shows no component.
- Brand fidelity 4: The ask stands on its own row, a field on Charcoal stays Charcoal, and red never meets Prussian.
- Usefulness 5: Code to copy in both themes, keys, names, target sizes and status lines for every component.
- Evidence honesty 4: Atlas samples carry their snapshot date, and Loop R1 its grade.
- Accessibility 4: Chapter 19's results report all 37 keyboard paths walked in both themes at 1440 and 390 px, 140 walks in all.

**Chapter 19, Accessibility** (`#accessibility`). Fixes: S3.

- Craft 4: The 33, 8, 9 and 5 count opens the chapter as a plate, and Rule 19.5's chart now has its title, series, years and source.
- Clarity 4: The intro defines WCAG, success criteria and levels before the count.
- Brand fidelity 4: The chapter speaks in the house's plain voice and spends no red it does not need.
- Usefulness 4: Each criterion links the rule that meets it, and the device script is ready for Phase 5.
- Evidence honesty 5: Tested and not tested are kept apart and dated, and the results plate names its own build.
- Accessibility 4: Rule 19.2's alt text plate and Rule 19.5's chart model what they teach, and the results report axe-core with no violation at four widths.

**Chapter 26, Tokens and how to choose them** (`#tokens`). Fixes: M1, S2, S11.

- Craft 4: The five steps plate and the token table, now broken out with its label row, read cleanly at 1440 and 390 px, though none of the seven failure plates carries the bar.
- Clarity 4: The opener's five steps show the chapter's method at once.
- Brand fidelity 4: Token names follow the surface and role, and the worked examples keep red off Prussian.
- Usefulness 3: Rule 26.5's builders link loads Inter Tight 600, 700 and 800 and Inter 400 to 700, where Rule 06.1 tells builders to load Inter Tight 800 and Inter 400, 600 and 700, so a builder meets two answers; the page sets no Inter Tight 600 or 700 anywhere.
- Evidence honesty 4: The token count and version are stated, and the sources carry retrieval dates.
- Accessibility 4: Contrast is printed for every color token on each surface it serves.

**Identity proofs** (`#proofs`). Fixes: S4.

- Craft 4: The avatar, social card and letterhead are finished at true size, though the section's title sets at 32 px where every chapter title sets at 80 px, so the book's last pages read as a board bound in.
- Clarity 4: The instruction and intro say what is proved and on which four pieces.
- Brand fidelity 5: With the wordmark covered the social card still reads as ours through the hinge headline, the lockmark and the Newsprint ground.
- Usefulness 4: Each proof prints its sizes, margins and masters, and the letter downloads as a print proof.
- Evidence honesty 4: The letter names its invented parts beside it, and the L2 record names its approval and date.
- Accessibility 4: The site bar scrolls inside its frame with a Fit to window control, and each proof prints its sizes in text beside it.

**Gate 2 preview: Where to start, the font license and the colophon** (`#start, #colophon`). Fixes: A1, A2, A3, A4, A5.

- Craft 3: The start page sets its 21 steps as whole underlined sentences in three 347 px columns, about 64 underlined lines at 1440 px, so the book's front door reads as a list of links; the license texts mix the file's hard line breaks with reflowed paragraphs, two hairlines sit 13 px apart under the last license, and on a phone the cover's edition line breaks “November / 11, 2026”.
- Clarity 4: Three routes named for why a reader came, each step saying what the reader will learn and where it goes, with the one later step in plain words and no link.
- Brand fidelity 3: Locked lines are exact and no red is spent, yet with the wordmark covered the start page carries no mark, symbol or hinge, and the colophon closes the book with no sign-off.
- Usefulness 4: Every step points at the rule that answers it, the builder route starts at the token files, and the colophon names each family's authors, OFL 1.1 and Lora's reserved name, with the full texts.
- Evidence honesty 4: “We built the font files into this page unchanged, so it loads no type from elsewhere” is true: the preview made no network request, and its six @font-face blocks carry the files as data; the Built row gives 17:12 with no time zone.
- Accessibility 4: Each route is an ordered list under its own heading, each link's name is the whole step and its target, and each license sits behind a disclosure that names what opens.

## Drift between stages

Ranked: the three most serious first, then the rest. Each says which way the fix runs.

**D5, Which weights to load** (serious, 1 of 3). Direction: later moves to earlier. Rule 06.1 (stage A) and Rule 26.5 (stage C) give two font links with different weights, and the shell follows 26. Chapter 06 owns the faces and the type tokens use only its weights, so 26 and the shell move to 06. M1.

**D1, The first screen** (serious, 2 of 3). Direction: earlier moves to later. Chapters 09, 10, 17, 19 and 26 open on a plate of their subject. Chapters 01, 02 and 11 open on a group index, and 03 to 08 and 12 on words alone, so the four chapters that hold the identity (03 to 06) show none of it on their first screen. The later form is stronger on the newcomer test and the distinctiveness test. S1.

**D2, The failure plate** (serious, 3 of 3). Direction: earlier moves to later. Three caption leads and a do-not-publish bar on some failures only: every failure in 10, 11, 17, 18 and 19, none on the rule failures of 03, 07 and 26. The bar's words are White on Charcoal in 33 bars across 01, 02, 04, 08, 09, 12, 17 and 26, and Newsprint on Charcoal in 81. Stage C's form, “Fails Rule NN.N.” and the bar in Newsprint, is the one to keep. S2.

**D3, Rule titles**. Direction: later moves to earlier. Titles grow from seven words in 02 and nine in 06 to 16.6 in 18 and 15.6 in 19. Stage A's short imperative is the house form; stage C's two-clause titles carry what belongs in the rule's first sentence. S3.

**D4, The identity proofs**. Direction: proofs move to the chapter form. Built at stage A as a board and revised since, the proofs keep a 32 px title with no number or rail, so the book closes in a different hand from its 16 chapters. S4.

**D6, The keyline on red**. Direction: earlier moves to later. Chapters 04, 05 and 11 draw the Charcoal keyline as a shadow, 01, 02 and chapter 18's code as a border. Chapter 18's border is what a builder copies and what forced colors keeps. S7.

**D7, Weights in plates**. Direction: the plates move to chapter 06. Plates in 08 (stage A) and 12 (stage B) set Inter 800 and Inter 500, outside chapter 06's set, and 02 and 03 fake an Inter italic. S8.

**D8, Who is speaking**. Direction: settle one convention. Chapters 01 to 08 speak as “we” about ten times in a thousand words; 18 almost never does (0.2) and 26 speaks to “you” (10.2) and never says “we”. Each choice fits its chapter, and the book still reads as one voice, so this is a note for the editor's next pass, kept with S10 and S11.

What already reads as one hand, checked across stages:

- The shell draws every rule the same way in all 16 chapters: number, title, rule, tokens, basis, the hinge divider, correct and failure plates with their frame labels, specifications, related chapters and builders.
- One Illustrative chip, the same class and type in every chapter.
- Rule 05.4's ten states (stage A) and Rule 17.8's canonical plate (stage C) draw muted, disabled, hover, focus, selected, warning, error, empty and success the same way, and 05.4 names 17.8 as the reference.
- Chapter 01's tracker piece draws done, now, not yet and never happened exactly as Rule 11.2 does.
- Rule 09.2's underlined current pillar agrees with Rule 17.10's mark for a current place in a masthead.
- The large crop of B takes the surface's ink in Rule 04.8 and Rule 12.4, and red stays off Prussian in 05, 09, 17, 18 and 26.
- Masters and their pixel ranges agree across 03, 04 and 08: the wordmark 16 to 19, 20 to 39 and 40 px up, B and the lockmark 16 to 23, 24 to 47 and 48 px up.

## Distinctiveness test

Six views from six chapters at 1440 px, with the masthead hidden and no wordmark inside the plates in view.

| View | Verdict |
|---|---|
| Chapter 01, first screen | Not on its own. Newsprint and Inter Tight 800 carry it, with no red, symbol or hinge in view; any careful civic publisher could have set it. Chapters 02 to 08 and 12 open the same way (S1). |
| Chapter 05, the ask on four surfaces | Reads as Oath & Action: one red ask, the Charcoal keyline on Newsprint, Newsprint on Prussian. |
| Chapter 10, the library | Reads as Oath & Action: the Civic Line's single weight, round ends and typed variable chips. |
| Chapter 11, the six step states | Reads as Oath & Action: the step glyphs and the red take-part disc. |
| Chapter 17, the ten states | Reads as Oath & Action, the weakest of the five: Newsprint, the Charcoal edges and the error's red bar carry it, while the controls themselves are generic. |
| Chapter 12, the reform marker on Loop R10 | Reads as Oath & Action: the atlas's pills, the signed link and the red target. |

Five of six read as Oath & Action without the name. The plates carry the identity everywhere; the first screens of chapters 01 to 08 and 12 lean on Newsprint and Inter Tight alone, which S1 answers.

## Required changes

**Must fix**

- **M1.** Where: Chapter 26, Rule 26.5's builders line, its Fonts row and the code in both its plates; chapter 06, Rule 06.1's builders line; the shell's font declaration. What: Two answers to which weights a product loads. Rule 06.1: “Load all three with one link: …family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&family=Lora:ital,wght@1,400;1,500…”. Rule 26.5: “The fonts link this guide uses: …family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600;700&family=Lora…”. The head code a builder copies from Rule 26.5's plates carries the second link too. The page sets no Inter Tight 600 or 700 anywhere and Inter 500 only in Rule 12.5's plates. In the preview, where the files are embedded, 26.5's sentence also stops being true. Fix: Make Rule 06.1's set the one set (Inter 400, 600 and 700; Inter Tight 800; Lora Italic 400 and 500), since chapter 06 owns the faces and the type tokens use no other weight. Give Rule 26.5's builders line and the code in its two plates the same link, with words such as “A product loads the three faces with this link (Rule 06.10):”, and in the preview's chapter 26 and colophon say the guide carries the files itself. Declare the same weights in the shell. The bytes do not change: Google serves one variable file per family and subset, and the frozen page fetched three. Owner: Engineer (chapter 26, shell, preview), with the Systems designer (chapter 06's generator) and the Editor (words).
- **A1.** Where: The preview's “Where to start” page (#start) and the colophon's close. What: The book's first page after the contents is three lists of underlined sentences with no mark of the system on it, and the book ends on the colophon's table with no signature. Craft and brand fidelity score 3. Fix: Make each step's target line the link (“Rule 01.21 · Purpose”, underlined, with the whole row as its hit area) and set the step's sentence in plain ink, which cuts 64 underlined lines to 21. Set the three route heads on the part opener's Charcoal panel, the dark beat each part opens with, with each route's label and lede there and its seven steps below on Newsprint. Head the newcomer route with the pillar row at 24 px, a place Rule 09.4 allows, since its first step is the pillars. Close the colophon with the footer sign-off Rule 08.2 draws: the lockmark at 24 px beside “A country that answers to its people.” in Newsprint on Charcoal. Nothing here needs a new drawing. Owner: Engineer (the page's build and the shell), with the Identity designer for the pillar row and the sign-off, and the Editor for any changed words.

**Should fix**

- **S1.** Where: Chapters 01 to 08, 11 and 12, and chapter 18's opener. What: Ten chapters open on words alone. At 1440 px Identity shows no lockup, Color no color and Type no type until Rule NN.1's words end. Chapters 09, 10, 17, 19 and 26 open on a plate of their subject; chapter 18's plate sits below an eleven-line paragraph. Fix: One opener form for every chapter: number and title, instruction, at most two short intro paragraphs, then one plate of the subject at true size, then the group index where the chapter has groups. Reuse plates that exist, with no new drawing: 01 the four pillar pieces, 02 the brand lines, 03 the eight lockups, 04 B at display size beside one hinge headline, 05 the seven colors with their shares, 06 the three faces, 07 the five grids, 08 the lockmark in its four places, 11 the six steps, 12 the device index. Move chapter 18's ARIA and APG definitions into Rule 18.1 so its plate reaches the first screen. Owner: Identity designer (03, 04, 08, 12.1 to 12.4), Systems designer (05, 06, 07, 11, 12.5 to 12.9), Editor (01, 02, and chapter 18's intro words with the Accessibility lead), Engineer (the opener slot in the shell).
- **S2.** Where: Failure plates in chapters 01 to 09, 12 and 26. What: Three caption leads: none (01 to 04, 08, 09 and four in 12), “Fails the proportion.” (05 to 07) and “Fails Rule NN.N.” (10, 11, 17, 18, 19, 26). The “Failure case: do not publish” bar is missing from 74 failure plates, all eight of chapter 03's among them, and it prints White on Charcoal in 33 plates where 81 print Newsprint, the text color Charcoal takes. Fix: Lead every failure caption with “Fails Rule NN.N.” in bold. Put the bar on every failure plate that draws a piece a reader could lift (a mark, a card, a page, a chart, a control), chapter 03's first, and set its words in --oa-color-text-primary-on-charcoal. Owner: Each chapter's maker in its generator; Editor for the leads.
- **S3.** Where: Rule titles, chapters 17, 18 and 19 first (44 titles past fifteen words, 14 of them in chapter 18). What: Titles in 02, 03 and 06 average seven to eleven words; chapter 18's average 16.6 and run to 24, so the contents rail and the in-chapter list read as paragraphs. Example: Rule 18.2, “Turn a setting on or off with a toggle button, and mark it on with a check, bold words and a 2 px edge.” Fix: One clause per title, about twelve words at most, with the second clause moved into the rule's first sentence: Rule 18.2 becomes “Turn a setting on or off with a toggle button.” Owner: Accessibility lead (chapter 18's and 19's words), Systems designer (17), Editor.
- **S4.** Where: Identity proofs, the section head. What: The title sets at 32 px with no number and no rail where every chapter sets at 80 px, so the book's last pages read as a board bound in. Fix: Give the proofs the chapter opener form, with “Appendix” in the number's place and the rail listing its five proofs. Owner: Identity designer, with the Engineer for the shell.
- **S5.** Where: Chapter 04, Rule 04.5, s-04-5-correct. What: The two compact masters stack at the left under the display master and leave the right half of the frame empty. Fix: Set the compact masters side by side under the display master, Newsprint and Charcoal, and fit the frame to the three. Owner: Identity designer.
- **S6.** Where: Chapter 07, Rule 07.2, s-07-2-correct. What: The frame wraps the five grids with no inset, so “Wide, 1440 px” and the other labels sit on the frame's left edge. Fix: Give the frame the 24 px inset the other plates use, --oa-space-300. Owner: Systems designer.
- **S7.** Where: Specimens in chapters 04, 05 and 11 (s-04-3-failure, s-05-1-correct, s-05-3-correct, s-11-6-correct and others). What: The Charcoal keyline on red is drawn as a box shadow, which forced colors removes, where 01, 02 and chapter 18's code draw a 1 px border. Fix: Draw the keyline as chapter 18's button does, a 1 px border in --oa-component-button-ask-keyline-on-newsprint. Owner: Systems designer (05, 11), Identity designer (04).
- **S8.** Where: s-02 “Terms.” labels, s-03-1-correct, s-08-3-correct, s-12-signature-correct and -failure, s-12-marker-correct and -failure. What: Off-system weights and faked styles: “Terms.” and the “x” set in an Inter Italic the page never loads, a “4” in Inter 800 in three plates, and “raises” in Inter 500. Fix: Set “Terms.” in Inter 600 roman, the “x” in Inter 400 roman, the “4” in Inter Tight 800 or Inter 700, and “raises” in Inter 600. Owner: Editor (02), Identity designer (03, 08, 12.3), Systems designer (12.5).
- **S9.** Where: Chapter 01, the 14 rules without a Specifications block. What: The template's item 6 is missing from 14 of 24 rules, where every rule from 03 on carries one. Fix: Give each a short Specifications block with what a producer checks: the label, the count, the place, the token where there is one. Owner: Editor.
- **S10.** Where: Rule 05.3's body; chapter 18's intro. What: Rule 05.3's body runs about 230 words before its plate; chapter 18's intro runs eleven lines of definitions before its opener. Fix: Keep Rule 05.3's first three sentences as the rule and move the precedence list and the exceptions into its Specifications; chapter 18 as S1. Owner: Systems designer and Editor (05); Accessibility lead (18).
- **S11.** Where: Basis lines in chapters 26 and 03. What: Chapter 26 writes “; Design judgment” with a capital in four bases where 04, 06, 09, 11, 17 and 18 write it in lower case, and Rule 03.8 cites “Dustin Cathcart’s ruling on partners” where 04 and 08 to 12 write “approved by our founder and editor”. Fix: Lower-case “design judgment” after a semicolon, and write Rule 03.8's basis as the others do, with its month. Owner: Editor, in the generators of 26 (Engineer) and 03 (Identity designer).
- **A2.** Where: The start page's route index (ul.route-index), most visible at 390 px. What: Three links to the routes are drawn as boxed quiet buttons, which chapter 18 keeps for actions (Rule 18.1), and on a phone they wrap two and one. Fix: Draw them as the contents' links or as underlined links in one line of text, as Rule 18.5 sets for a link. Owner: Engineer.
- **A3.** Where: The three license disclosures in the colophon. What: Paragraphs that keep the file's hard line breaks (“This Font Software is licensed under the SIL Open Font License, / Version 1.1…”, “Permission is hereby granted…”) sit beside reflowed ones, and a second hairline sits 13 px under the last disclosure. Fix: Reflow every paragraph, keeping each word, mark and line order of the license as the file has it, and drop the disclosure list's own bottom rule so the row's rule closes it. Owner: Engineer.
- **A4.** Where: The cover's edition line at 390 px. What: “Preview for approval, built November 11, 2026” breaks between “November” and “11”. Fix: Join the month, day and year with no-break spaces, as the editor's notes do for figures and “px”. Owner: Engineer, with the Editor.
- **A5.** Where: The colophon's Built row. What: “November 11, 2026 at 17:12” gives no time zone, where chapter 19's results give theirs in UTC. Fix: Write the time with UTC, as chapter 19 does. Owner: Engineer.

## Risks for Dustin to weigh

- **Chapter 19's results describe another build.** The results plate on the frozen page reports the chapters page built from commit 04a3f3b8 at 8,962,864 bytes. The preview is a 9.44 MB build with the fonts embedded. Before Dustin reads the preview as the record, rerun the results on it or say on the plate which build they describe (Main session, with the Accessibility lead).
- **S1 can cost page weight.** Opener plates should point at plates the chapter already draws, or draw a light version, since repeating the lockups or palette plate repeats its SVG. Page weight is already a Phase 3 to 5 risk (D2-1214).
- **One pass or a third state.** S1 and S2 touch ten generators. Landing them together keeps the book in two states, before and after; landing part of them leaves three.
- **Nothing here asks to change a settled decision.** The hinge divider in every rule is DR-96, the drawings are approved, and M1 keeps the faces and the license as D2-1697 has them.

## Addendum: the Gate 2 preview's front pages

The preview, `work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html` (9,441,768 bytes), scored as the eighteenth item: the “Where to start” page, the font license and the colophon. I looked at the cover, the contents' last screen, the start page and the colophon at 1440 px (1x) and 390 px (2x), opened a license, and read the start page's markup and the routes' words in `where-to-start.json`.

The page made no network request in Chromium, and its six `@font-face` blocks carry Inter (400 to 700), Inter Tight (600 to 800) and Lora Italic (400 to 500) as data, so the colophon's claim holds. The start page is linked from the cover, the contents and the phone menu, as the brief asks.

| Item | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Ready |
|---|---|---|---|---|---|---|---|
| Where to start, the font license and the colophon | 3* | 4 | 3* | 4 | 4 | 4 | no |

The words are good. The routes are the right three, each step says what a reader will learn and points at the rule that answers it, and the license words name the authors and Lora's reserved name in plain sentences. What holds the item under 4 is the drawing: a front door of underlined sentences with nothing of the system on it, and a book that ends without its signature. A1 answers both with parts the guide already draws.

**The main session's question, chapter 06's Google Fonts line.** It is part of M1, and the preview makes it sharper. In the preview Rule 26.5 still says “The fonts link this guide uses:” with the Google link, which is now untrue; the head code in both of Rule 26.5's plates carries the same wider link; Rule 06.1 still gives a different one; and Rule 06.10's builders line (“as the Google Fonts link sets it”) and the Fonts rows of 06.10 and 26.5 (“from Google Fonts”) describe loading from Google. M1's fix covers all of them: one weight set, offered as the link a product uses, with the guide itself carrying the files.

**Chapter 19 in the preview.** Its results plate still describes the chapters page of commit 04a3f3b8 at 8,962,864 bytes (see Risks).

## Rescore

The fixed page, the scratchpad's `gate-2/rescore/guide.html` (9,444,334 bytes, commit 2a11e2e3), read against the fix brief and the six owners' notes. I looked at every chapter's first screen and the proofs at 1440 by 900 and at 390 px, the start page and the licenses at 2x, a sample of the new failure plates and openers by element, and recounted leads, bars, titles, weights, keylines and font lines by script on the page and the chapter files. The identity designer's seven wording fixes (the editor's rows 14 to 20) are read from the working tree and its notes as landed.

**Verdict.** All 18 items are ready, every score 4 or more, with no Must fix. Three Should fix items remain, all the engineer's, and chapter 19's results wait for call 12 as planned.

| Item | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Was under 4 |
|---|---|---|---|---|---|---|---|
| Chapter 01, Purpose | 4 | 4 | 4 | 4 | 5 | 4 |  |
| Chapter 02, Voice | 4 | 4 | 4 | 4 | 4 | 4 |  |
| Chapter 03, Identity | 4 | 5 | 5 | 5 | 4 | 4 |  |
| Chapter 04, The Ampersand and the hinge | 4 | 4 | 4 | 4 | 4 | 4 |  |
| Chapter 05, Color | 4 | 5 | 5 | 4 | 4 | 4 |  |
| Chapter 06, Type | 4 | 5 | 4 | 5 | 4 | 4 |  |
| Chapter 07, Layout and spacing | 4 | 4 | 4 | 4 | 4 | 4 |  |
| Chapter 08, The lockmark | 4 | 4 | 4 | 4 | 4 | 4 |  |
| Chapter 09, Pillar icons | 4 | 4 | 5 | 4 | 4 | 4 |  |
| Chapter 10, Topic and atlas symbols | 4 | 4 | 4 | 5 | 4 | 4 |  |
| Chapter 11, Status and utility icons | 4 | 4 | 4 | 5 | 4 | 4 |  |
| Chapter 12, Graphic devices and patterns | 4 | 4 | 4 | 4 | 4 | 4 |  |
| Chapter 17, Motion and states | 4 | 4 | 4 | 4 | 4 | 4 |  |
| Chapter 18, Components and interaction | 4 | 5 | 4 | 5 | 4 | 4 |  |
| Chapter 19, Accessibility | 4 | 4 | 4 | 4 | 4 | 4 |  |
| Chapter 26, Tokens and how to choose them | 4 | 4 | 4 | 4 | 4 | 4 | Usefulness 3 |
| Identity proofs | 4 | 4 | 5 | 4 | 4 | 4 |  |
| Gate 2 preview: Where to start, the font license and the colophon | 4 | 4 | 4 | 4 | 4 | 4 | Craft 3, Brand fidelity 3 |

**What closed.** M1: one weight set and one link in Rules 06.1, 06.10 and 26.5, in both of 26.5's plates and in the six `@font-face` rules, and Rule 26.5 says the guide carries the files. A1: the route heads on the Charcoal panel with the pillar row, plain step sentences under 20 underlined target lines, and the colophon closing on the lockmark beside the tagline, exact. D1 to D7 closed: one opener form in all 16 chapters and the proofs, every opener reaching the first screen at 1440 by 900; all 184 failure captions leading “Fails Rule NN.N.”, every bar in Newsprint on Charcoal, and the 28 plates without a bar each drawing a method with its reason in its owner's notes; one title past fifteen words, Rule 12.4's; no shadow keyline; no off-system weight.

**Should fix**

- **R1.** Where: “Where to start”, every step's target line (1440 and 390 px). What: The underline runs under the space after “Rule 26.8” and before “Tokens”, so one link reads as two, and “Tokens and how to choose them” leaves “them” alone on a line in the builder route. Fix: Underline the words alone, with the spaces and the dot outside the underlined spans, and join the target's last two words with a no-break space. Owner: Engineer.
- **R2.** Where: “Where to start”, the route index at 390 px. What: The third link wraps with its separator dot at the start of the line: “· Building with code”. Fix: Bind each dot to the link before it with a no-break space, so a line never starts with a dot. Owner: Engineer.
- **R3.** Where: The colophon's sign-off. What: The sign-off's hairline runs to 1376 px at 1440 while the colophon's rows end at 1183, so the book closes on two measures. Fix: End the hairline at the rows' right edge, the colophon's measure. Owner: Engineer.

**Open, by plan.** Chapter 19's results plate still describes commit 04a3f3b8 at 8,962,864 bytes; call 12 reruns it on the fixed preview last, as the fix brief plans (Accessibility lead, after the main session's final guide check).

**Tested.** The fixed page in Chromium: its 21 openers and front pages at 1440 by 900 and 390 px; the start page's steps and an opened license at 2x; seven plates by element (03.4 and 06.4 failures, 07.2, 04.5, and the 01, 04 and 08 openers); by script, every failure caption's lead and every failure specimen's bar in the chapter files, title lengths, the computed style of every bar, every family and weight the page sets, every red fill's keyline, every font link and `@font-face` rule, and chapter 19's results line.

**Not tested.** Keyboard and screen reader on the new front pages and openers; forced colors on the sign-off and the pillar row; every one of the 433 specimens at full size; the identity designer's seven wording fixes on a rebuilt page; the main session's four-width guide check, which runs after.

## Tested and Not tested

**Tested**

- Loaded the frozen page (SHA-256 as the brief gives it, 8,965,291 bytes) in Chromium through Playwright, waiting for load and then the network, as `guide_check.js` does, and mapped all 16 chapter anchors, the proofs and 185 rule anchors.
- Looked at every chapter's first screen and the proofs at 1440 px (1x) and 390 px (1x); the whole page at quarter scale in 209 strips, read as eight sheets for the book's rhythm; one full rule from each chapter at half scale; 28 plates by element at 1440 px and 1x; the lockups, minimums, pillar sizes and token table at 1440 px and 2x; four plates at 390 px and 2x; and eight rules at 390 px.
- Scripted reads of the chapter files: the rule keys each chapter carries, the failure caption leads, the do-not-publish bar in every failure specimen, title lengths, counts of shared names across chapters, voice measures (sentence length; we, you and reader per thousand words), basis lines and every Google Fonts line.
- Scripted reads of the rendered page: the computed style of every Illustrative chip and do-not-publish bar, heading sizes, figure caption type, every text under 13 px (two failure plates only), every red fill in a figure with its ground and how its keyline is drawn, every family and weight the page sets, and the font requests (three WOFF2 files).
- The distinctiveness test on six views with the masthead hidden by CSS.
- Side-by-side reads of Rules 05.4 and 17.8, 09.2 against 17.10 and 18.7, 04.8 against 12.4, and 06.1, 06.10 and 26.5's words.
- The preview: loaded it in Chromium and recorded its requests (none left the file); counted its six `@font-face` blocks and their weight ranges; looked at the cover, the contents' last screen, the start page and the colophon at 1440 px (1x) and 390 px (2x), with the Inter Tight license opened by script; read the start page's markup and the routes' words; found every Google Fonts line left in the preview's words: four links (Rule 06.1's builders line, Rule 26.5's builders line and the head code in both of 26.5's plates) and four mentions.

**Not tested**

- A device dark setting. The guide stays light by decision (D2-1133); I saw chapters 17 and 18's Charcoal and dark-theme stages as plates.
- Keyboard, screen readers, forced colors and reduced motion. My accessibility reasons cite chapter 19's results plate and the rules' own words for those.
- Chapter 17's players in motion.
- Every one of the 424 specimens at full size. I read 28 closely and the rest at quarter and half scale.
- Cross-references, counts and values against `tokens.json`, the Civic Line folder and the WCAG text, which the drift red team checks by script.
- Print.
- On the preview: a keyboard walk and focus order through the start page and the license disclosures, whether every step's link lands where it says (the build stops on a missing id, by the engineer's notes), the license texts against the fetched OFL.txt files character by character, and any chapter page, which the brief says the preview does not change.

## Routine calls

D2-xxx | The identity proofs are scored on the six criteria as a seventeenth item, like a chapter | The brief names them so
D2-xxx | M1 sits on chapter 26, with chapter 06's builders line aligned in the same fix | Rule 26.5 is where the builder route starts, and its weight set is the one wider than the faces chapter 06 owns
D2-xxx | The opener and failure-plate drift (S1, S2) go back as Should fix | Every chapter still states its job in words on its first screen, and every failure plate carries the frame's “Failure case” label
D2-xxx | The distinctiveness test hid the masthead by CSS and used views with no wordmark inside a plate | Covering the wordmark is the test; a plate that draws the wordmark would pass for the page
D2-xxx | The difference in who speaks between chapters (D8) is a note for the editor, with no score lowered | Each chapter's choice suits its job, and the book still reads as one voice
D2-xxx | The preview's start page, font license and colophon are scored together as one eighteenth item | The brief names them as one addendum item
D2-xxx | Chapter 06's Google Fonts line, which the main session raised, is folded into M1 | It is the same fault as Rule 26.5's link: one weight set, offered as the link a product uses
D2-xxx | The rescore reads the identity designer's seven wording fixes from the working tree as landed | The coordinator allowed it, and its notes and the files agree
D2-xxx | Chapter 19's results waiting for call 12 lowers no score | The plate names its own build honestly, and the brief schedules the rerun last
