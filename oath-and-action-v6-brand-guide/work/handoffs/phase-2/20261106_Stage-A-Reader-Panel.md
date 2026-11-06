# Stage A reader panel: simulated and untested

Oath & Action Edition 06, Phase 2, November 6, 2026. The reader panel lens of the stage A red team, written under `work/handoffs/phase-2/20261106_Stage-A-Red-Team-Brief.md`. Page reviewed: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, built November 6, 2026 at 20:16.

**This whole report is simulated and untested.** No real person used the page. One reviewer played five invented people, each one Illustrative, and used the rendered page the way that person would, one task each. Where a finding says a reader "got stuck" or "misread", it means the simulated reader did, on the page as it renders. These are predictions of where real readers may fail. Test them with real people before relying on them.

## 1. Score

**3 of 5.** All five found the right chapter and learned something they could use; the newcomer came close to finishing from the page alone, and the other four stopped on gaps one fix pass can close.

## The five readers (simulated, Illustrative)

| Reader | Task | Finished? |
|---|---|---|
| 1. Producer at a partner group | Make a US Letter flyer and an event page header for a public-comment workshop the partner co-hosts with Oath & Action, with both names | No. Could sketch the lockup; could not get a file, set it for print or find who approves it |
| 2. Freelance designer | Make a 1200 by 630 link-preview card for a new explainer on who sets property tax rates | Partly. Made a card that looks right, with a kicker that breaks Rule 01.21, specs measured by eye and no master file for the ampersand |
| 3. Volunteer writing the newsletter | Write this week's issue on a county budget hearing: the opening, one statistic with its source, and the ending | Partly. Opening and statistic done; stalled on the ending |
| 4. Developer building the site | Set up the base stylesheet and masthead: fonts, tokens, body type, grid and breakpoints, L3 masthead that drops to L1 on phones | Only by leaving the page for `work/build/tokens/tokens.css`. The page's own Copy blocks produce CSS that fails |
| 5. Reader new to civics, arriving from a search on a phone | Find out what Oath & Action is, whether it takes sides, and how to read one of its tracker cards | Mostly. First two answered well; the tracker half-understood |

### Reader 1, producer at a partner group (Illustrative)

**Path.** Contents, then chapter 03, then the "In this chapter" list to Rule 03.8, "Join a partner with a hairline, and keep our ampersand inside our name." The rule fits the job closely: its failure case is an event flyer for "a workshop on public comment". The producer took the layout from it (L1 at left, a 1 px hairline, 0.6x of space, the partner no taller than our capitals), the print minimum for L1 from Rule 03.4 (1.20 in), clear space from Rule 03.3 and the surfaces from Rule 03.5.

**Stuck.**
- The file. Every Files list is a repository path, such as `work/build/assets/identity/wordmark/20261028_Wordmark-Display-Master.svg`, and each chapter ends "Download buttons for these files arrive with the asset package in Phase 5." The producer has no repository and does not know what Phase 5 is. Nothing on the page says whom to ask.
- Print measures. Rule 03.8's specifications give the hairline as "1 px, as tall as our capitals plus 6 px", in screen pixels, for a printed flyer.
- Approval. The page never says whether a co-branded piece needs Oath & Action's sign-off. The colophon names "Dustin Cathcart, Founder and Editor, who approves every change" and gives no way to reach him.

**Misread.** Rule 03.3 says "Text, rules, image edges and other logos all stay outside" the 1.0x clear space. Rule 03.8 sets the hairline 0.6x from the wordmark. The producer took Rule 03.3 as binding and pushed the hairline out to 1.0x.

**Looked for and did not find.** Which name goes first when the partner is the host. A stacked partnership lockup for a square post. Whether the partner's own colors may appear elsewhere on the flyer (the page shows only the failure where our ampersand turns the partner's blue). What to do about the partner's own ampersand: Rule 01.24 says "a partner's ampersand is written as 'and'", and Rule 03.8 lets "its own logo" sit at right.

### Reader 2, freelance designer (Illustrative)

**Path.** The contents show "23 Social and video" as a later stage, so the designer searched the page for "social card" and found Rule 04.2 (a 480 by 252 link card), Rule 08.2 (the lockmark "at the bottom right of social cards, covers and posters, 40 px"), and the appendix's "Social card", 1200 by 630. Chapter 05 gave every hex value and the pairs that pass. Rule 06.1 gave the three faces and the font link. Rules 02.27 and 04.3 taught the hinge headline, and Rule 05.3 said its ampersand takes the view's one working red. That is most of what the job needs, and it was easy to find.

**Stuck.**
- No specifications for the card. The proof gives no margin, headline size, deck size, wordmark height or lockmark size. The designer measured the rendered plate instead (kicker Inter 700 at 20 px, deck Inter 400 at 32 px) and had to scroll the 1200 px card inside a 1080 px frame at 1440 to find the lockmark at its bottom right.
- No ampersand file. Rule 04.3 says "Set B as an inline image, not a font glyph", and the masters are repository paths.

**Misread.**
- The kicker. The designer copied "EXPLAIN" from the proof card. Rule 01.21 says the kicker opens with "one content label: Explainer, Tracker, Analysis, Report, Act · How to take part, or Our position." (Must fix 1.)
- Whose choice. The appendix says "before you choose at Gate 2" and "Today's width stays in force until you choose." The designer read "you" as themselves and wondered whether the condensed wordmark was theirs to use.

### Reader 3, volunteer writing the newsletter (Illustrative)

**Path.** Chapter 02. The brand lines table told the volunteer that the reader promise goes in "the newsletter welcome" and the tagline in "the newsletter's sign-off". The index at the top of the writing section linked straight to the ten questions, which worked well as a checklist. W05 fixed their first line, the way its own before and after does. H04 gave the order of a source line with a worked example, and H05 and H06 settled dates and small numbers. The list of words to leave out in Rule 02.26 caught two words in the draft.

**Stuck.** The ending. Rule 02.24 says "End every piece on the one step a reader is most likely to take, with its date and place and the way to take it." W08 says "Where a sign-off line belongs, use the locked tagline." Rule 02.23's specimen "Newsletter, the sign-off" ends "That's the briefing for November 6." then "A country that answers to its people." with no step. The volunteer could not tell whether the step comes before the sign-off or whether a newsletter skips it, and wondered whether "That's the briefing for November 6." is the summary beat that W07 removes. (Must fix 2.)

**Misread.** Looking for a whole issue to copy, the volunteer opened the email proof in the appendix and took its deck as a model: "Here is who wrote it, what changed since the draft, and how to speak before the vote." That is W05's throat-clearing opener, the same "Here is how" that W05's own example removes.

**Looked for and did not find.** The newsletter's own content label. Rule 01.21 lists six, none for a newsletter issue, and says "A piece that fits none of them needs a ruling before it runs." The volunteer also met "approved on Board 5" and "approved at Gate 1" and did not know what either meant.

### Reader 4, developer building the site (Illustrative)

**Path.** Rule 06.1's For builders note for the font link. Rule 06.2's note: "font: var(--oa-type-body) carries face, weight, size and line height". Rule 05.1's note: "Set a page's ground with its surface class, such as .oa-surface-newsprint." The Copy buttons in the For builders closers of chapters 05, 06 and 07. Rule 07.5 for em breakpoints and Rule 03.6 for the masthead.

**Stuck.**
- The copied CSS fails. Copy in chapter 06 gives a `:root` block in which all 14 type styles are comments, such as `/* --oa-type-body: Inter 400, 1.0625rem/1.6 */`. No block defines a surface class or the part properties the notes name, such as `--oa-type-label-letter-spacing`. A scratch page built from the three copied blocks plus the notes' own declarations rendered every element in Times New Roman at 16 px in black. The same page built on `tokens.css` rendered Inter at 17 px, a 110 px Inter Tight 800 title and Charcoal text, as the guide intends. (Must fix 3.)
- The font link prints `&amp;` for each `&`. Requested exactly as printed, Google Fonts returned Inter alone, with no Inter Tight and no Lora. Pasted inside an HTML link's `href` the browser decodes it and it works; pasted into a CSS `@import`, a build config or an address bar it loads one face of three. (Must fix 4.)
- Rule 06.5's note says "write the minus as `&amp;minus;`". Written that way in a template, the page shows the text "&minus;". (Must fix 4.)

**Misread.**
- The type chips show one value each, such as "--oa-type-title Inter Tight 800, 6.875rem/0.95". The developer set titles at a fixed 110 px. The fluid range, `clamp(3.5rem, 2.2464rem + 5.1429vw, 6.875rem)`, lives only in `tokens.css`.
- Rule 03.6 says the masthead sets L3 "From 768 px wide". The developer wrote a px media query, which Rule 07.5 tells them to write in em.

### Reader 5, reader new to civics (Illustrative)

**Path.** On a phone, from a search, onto the cover: the tagline, the pillars, then "Stage board A draft, November 6, 2026. Chapters 01 to 08 of the Foundations part, with the proofs for Gate 2. 8 of 8 chapters delivered, 99 rules, 234 specimens placed." Nothing on the cover says what Oath & Action is or who the guide is for. The reader opened the contents, then chapter 01, whose first sentence answered the first question: "Oath & Action is a nonpartisan publication and a set of tools for people in every state who live under public rules they rarely get to read." The four pillars with their products and the four sample pieces made the idea concrete; the electric bill explainer was the clearest thing on the page for this reader. "The atlas, the trackers and the data never take a position; positions appear only in labeled Act pieces" answered the second question.

**Stuck.**
- The first five rules of chapter 01 are color rules: "Two sides take Charcoal and Stone, with their names printed", "A diverging scale runs from Prussian through the page color to Verdigris", "On Prussian, identity marks turn White and data marks turn Newsprint." The reader did not know these were color names; chapter 05 explains them. "Locked lines" (the heading "The hinge in the locked lines"), "Loop R4a, the map-drawing loop" and "the atlas's ten domains" are never explained.
- Codes. The part opener ends "arrives with stage board B (DR-88)", and Basis tags read "Rule 05.3 (D2-01, DR-66); G1-05" and "R13 (DR-67)". (Must fix 5.)
- The tracker. In chapter 08, "Stage 4 of 9: Reported out" helped, but "Referred", "Reported out", "Reconciled" and "chamber" are never explained. On the phone the 630 px tracker plate cut off "Testimony is open until March 3", the one line that told the reader what to do, until they scrolled the frame sideways.
- Where am I. The phone header shows the current place in a 49 px slot, so "01 Purpose" reads "01 P..." at 390 px; at 360 px every label reads as a letter and an ellipsis, such as "P...".

**Misread.** Four source lines say "The studio could not open the Senate's own page for the vote." The reader did not know who "the studio" is and took the line to mean the vote count went unchecked.

## 2. Must fix

1. **Kickers contradict Rule 01.21 across the page.** Where: Rule 01.21 sets the kicker as "one content label: Explainer, Tracker, Analysis, Report, Act · How to take part, or Our position. A series name may follow the label." Other specimens show five other patterns. A pillar alone: s-proofs-social-today and s-proofs-social-condensed ("EXPLAIN"), s-04-3-failure and s-04-3-corrective ("ACT"). A pillar and a topic: s-05-1, s-05-3 ("EXPLAIN · LOCAL SCHOOLS"), s-05-2 ("EXPLAIN · LOCAL BUDGETS"), s-05-6-failure ("TRACK · STATE BILLS"), s-06-1 ("EXPLAIN · LOCAL UTILITIES"), s-06-6 ("EXPLAIN · PRIMARIES"), s-07-1 ("TRACK · CITY COUNCIL"). A series and a topic: Rule 08.8, whose text says "then the series and the topic in the label style", and s-08-8-correct ("DISPATCH · PUBLIC MEETINGS"). A seventh label: s-05-5 and s-06-5 ("FINDING"). What goes wrong: the designer copied "EXPLAIN" from the only social card on the page and broke Rule 01.21; a volunteer meets the same choice. Fix: write one kicker grammar in Rule 01.21 (for example: content label, then series, then topic), have Rule 08.8 point to it, and reset every specimen kicker to it. Add "Finding" to Rule 01.21's list if charts keep it, or replace it.

2. **The newsletter ending is unclear.** Where: Rule 02.24, W08 (Rule 02.8), and s-02-23-correct, "Newsletter, the sign-off". What is wrong: Rule 02.24 says "End every piece on the one step a reader is most likely to take"; W08 allows the tagline "where a sign-off line belongs"; the newsletter specimen ends "That's the briefing for November 6. A country that answers to its people." with no step. The volunteer could not finish the issue. Fix: show one whole newsletter ending in s-02-23-correct or beside Rule 02.24, in order: the hinge divider, "What you can do", the dated step and its button, then the tagline as the sign-off. Drop "That's the briefing for November 6." or say why it passes W07.

3. **The For builders Copy blocks give CSS that does not work.** Where: the For builders closer of every chapter (`#purpose-builders` to `#signal-grid-builders`); notes under Rules 05.1 and 06.2. What is wrong: the blocks list flat hex values, comment out every composite type style ("/* --oa-type-h3: Inter Tight 800, 2rem/1.08 */"), and leave out the surface classes and type parts that the notes tell builders to use. Built from the copied blocks and the notes' own declarations, a test page fell back to Times New Roman, 16 px, black. Fix: make the Copy button give working CSS. The simplest is one line at the top of each block, "Import tokens.css; this block lists the values for reference", with `tokens.css` itself offered as a download. Otherwise copy the type parts (`--oa-type-body-font-size: 1.0625rem` and the rest, with the clamp) and the four surface classes as they stand in `tokens.css`.

4. **Two code samples print the wrong characters.** Where: Rule 06.1's For builders (the font link) and Rule 06.5's For builders (the minus); the same double escape names the letterhead's inline wordmark "Oath &amp; Action" inside s-proofs-letterhead-today, the one proof stage set as a group, where that label reaches assistive technology. What is wrong: the build escapes `&` twice. The page shows "`...wght@400;600;700&amp;family=Inter+Tight...`" and "write the minus as `&amp;minus;`". Requested as printed, the font link returns Inter alone; written as printed, the minus shows as text. Fix: escape once in `guide_build.py`, so the page shows `&family=` and `&minus;`, then rebuild and search the built page for `&amp;amp;` (15 SVG labels carry it today; the other 14 sit inside image stages and are not read).

5. **Decision codes and studio words are printed for readers.** House rule H11 reads "Name what an ID refers to the first time it appears, and print no bare code." Where: the part opener, "stage board B (DR-88)"; chapter 03, "(DR-55)" under the eight lockups and "(I8)" under the minimum sizes table; Basis tags in Rule 04.3 "Rule 05.3 (D2-01, DR-66); G1-05", Rule 04.4 "D1-22", Rule 04.5 "I6 (G1-01)", Rule 04.6 "(S9, G1-02)", Rule 04.7 "R13 (DR-67)" and "(R13)" in its text, Rule 05.3 "decisions D2-01 and DR-66", Rule 05.6 "decision D1-04", Rule 05.7 "decisions DR-48, DR-53, DR-54 and DR-58" and "Newsprint (DR-53)" in its specifications, Rule 06.1 "decision DR-47", Rule 06.3 "Master Brief section 8, tension 1; decision T-9", Rule 08.5 "D1-21", Rule 08.7 "R9 (DR-67)" and "(R9)"; chapter 08's sources, "approved at Gate 1 (S5)"; the appendix, "(DR-71)", "(D2-30)", "R13 sets as the default", "(DR-55)". Studio words a reader cannot place: "Phase 5" in eight Files lists, "chapter 25, Phase 4" in Rule 06.2, "approved on Board 5" in chapter 02, "approved at Gate 1" in the brand lines table, "Master Brief section 3" and "section 10" in several Basis tags, and "the studio" in eight places. What goes wrong: the newcomer and the producer stop on each one. Fix: replace each code with what it decided, in words ("Dustin approved Charcoal as the avatar tile in October"), or drop it where the Basis already names the reason. Keep the codes in the decision log and the makers' notes.

## 3. Should fix

1. **Two correct examples break another rule.** s-01-20-correct's hinge headline, "Both parties' voters & the stock trading ban.", fails Rule 02.27's own test ("ask whether its first half is a rule a reader could look up"); its first half names people, and its second half names the rule. s-proofs-email-today and -condensed open their deck with "Here is who wrote it", the pattern W05 removes. Fix: rewrite the 01.20 headline so a rule comes first, or say in Rule 01.20 that a sourced-agreement headline is the one exception to Rule 02.27; rewrite the email deck to give the fact, for example "The county board votes on the budget Tuesday at 7 p.m., and comments close Monday." with its Illustrative label.

2. **No way to get a file.** Every Files list ends "Download buttons for these files arrive with the asset package in Phase 5." This stopped the producer and the designer. The appendix already offers the letterhead proof as a working download from inside the page. Fix: give each listed SVG the same kind of link now, or replace the Phase 5 line with one plain sentence on how a partner or freelancer gets the files today.

3. **The partnership lockup lacks print and edge cases.** Rule 03.8 gives the hairline and spacing in px only, does not say which name leads when the partner hosts, has no stacked version for a square, and sets the hairline at 0.6x, inside the 1.0x clear space that Rule 03.3 says rules stay out of. Fix: add print values (hairline weight in pt, height and spacing in x), a line on order, a note in Rule 03.3 that the partnership hairline belongs to the lockup, and either a stacked version or a line saying square formats use L8 beside the partner.

4. **The social card proof is the only social card, and it has no specifications.** Fix: until chapter 23 exists, add a short spec list under s-proofs-social-today (outer margin, kicker style, headline style and size, deck style, wordmark master and height, lockmark size and inset), and add a line to the appendix that everyone uses today's width until Dustin decides at Gate 2. Name Dustin where the appendix now says "you choose".

5. **Type values and breakpoints read wrong outside `tokens.css`.** The type chips show only the largest size of a fluid style ("6.875rem/0.95"), and Rule 03.6 gives the masthead switch as "768 px" where Rule 07.5 asks for em. Fix: show the clamp, or "56 to 110 px" as the scale table does, on the chips and in the closer; write Rule 03.6 as "from 48em, 768 px at the default text size".

6. **The phone header cannot show where the reader is.** The location label has 49 px at 390 and 27 px at 360, so "04 The Ampersand and the hinge" shows as "04 ..." or less. The menu's "You are in" line works, but only after a tap. Fix: drop "Cover" and the part labels from that slot, and give the chapter number alone, or move the location under the bar.

7. **Chapter 01 uses terms before it explains them.** Color names (Charcoal, Stone, Prussian, Verdigris, Newsprint), "diverging scale", "identity marks" and "data marks" lead chapter 01's rules and are explained in chapter 05; "locked lines", "loop" and "the atlas's ten domains" are never explained. Fix: one sentence in chapter 01's intro naming the seven colors with a link to chapter 05, and a short gloss at first use for the rest, for example "the locked lines, the four brand lines whose wording never changes".

8. **The tracker example leaves a newcomer behind.** s-08-5-correct and s-08-stages use "Referred", "Reported out", "Reconciled" and "chamber" with no gloss, and on a phone the 630 px plate hides the testimony deadline until the reader scrolls sideways. Fix: a few words beside each stage name in s-08-stages (for example "Reported out: the committee voted to send it on"), and a phone-width version of the tracker list beside the true-size plate, since Rule 02.1 says most readers meet Oath & Action on a phone.

9. **"The studio could not open the Senate's own page for the vote."** It appears in four source lines (s-01-pieces, chapter 01's sources, s-02-25-correct, chapter 02's sources). A public reader does not know the studio and reads the line as an unchecked count. Fix: say what was checked and where, in Oath & Action's own voice, and leave the call on the source itself to the brand and evidence lens.

10. **The cover speaks to the studio.** It gives build counts and "proofs for Gate 2" and no line on what Oath & Action is or who the guide is for; at 390 px the pillars row leaves "Act" alone on its own line. Fix: one plain line under the tagline, such as "The rules for everything Oath & Action publishes, for staff, partners, designers and builders.", move the counts to the colophon, and keep the four pillars on one line or two balanced lines.

## 4. Questions for Dustin

1. **A partner's own ampersand.** Rule 01.24 says "a partner's ampersand is written as 'and'", and Rule 03.8 places "its own logo" in the partnership lockup. A partner whose logo holds an ampersand will ask whether it has to change. Recommendation: the partner's logo artwork stays as the partner draws it; "and" applies only where Oath & Action types the partner's name in its own copy and product names. Say so in both rules.

2. **Who approves a co-branded piece, and whose name leads.** Recommendation: every partnership lockup goes to you, or an editor you name, before it prints or posts; Oath & Action leads on pieces it hosts, the host leads otherwise. Add a contact line to the colophon and to Rule 03.8.

3. **The newsletter's kicker.** Rule 01.21's six labels have none for a newsletter issue. Recommendation: the issue carries no content label in its header, and each item inside carries its own; say so in Rule 01.21 so a volunteer does not wait for a ruling.

## 5. Tested and not tested

### Tested (checks this reviewer ran)

- Rendered the page in Playwright Chromium at 1440 by 900 and 390 by 844, with selected views at twice size, plus 360 px for the phone header and 1920 px for the social card proof, and looked at the screenshots.
- Extracted the rendered text of every section and the heading outline, and read all eight chapters and the appendix in that text, with the screenshots for layout.
- Opened the phone menu at 390 px and followed its "Color" link: the page moved to `#color` with focus on the chapter heading.
- Measured the phone header's location label (its visible width against its full width) in six places at 390 and 360 px.
- Clicked "Copy the custom properties" in chapters 05, 06 and 07 with clipboard access, built a scratch page from the copied CSS and the builder notes' own declarations, and read the computed styles; then built the same page on `work/build/tokens/tokens.css` and read them again.
- Requested the font link exactly as printed and with plain `&` from Google Fonts with curl, and counted the font faces each returned.
- Searched the built page for `&amp;amp;` and listed each place; checked which stages expose their inner labels (role `group`) and which hide them (role `img`).
- Clicked "Tracker progress" in the Signal Grid composer: its status line changed to "Tracker progress: stage 1 of 9, Filed."
- Measured the social card proof's frame at 1440 and 1920 px (the 1200 px card scrolls in both) and the kicker and deck sizes inside it.
- Mapped every kicker in the rendered specimens to its specimen id, and counted code-like IDs in the rendered text.
- Measured each chapter's length in screens (chapter 02: 74 screens at 1440, 93 at 390).
- Read `tokens.json` for the `mediaQuery` fields and `tokens.css` for the four surface classes.

### Not tested

- Any real person. Every reader here is simulated by one reviewer; no producer, designer, volunteer, developer or newcomer used the page.
- Screen readers, keyboard use beyond the one menu link, reduced motion, zoom to 200 percent, and contrast (the accessibility lens covers these).
- Safari, Firefox and real phones; widths of 1024 and 320 px beyond the header measurement.
- Opening any SVG master in a design app, printing a flyer or the letterhead, or opening the letterhead PDF (the link was found, not opened).
- Email clients.
- Whether the cited records and statistics are correct (the brand and evidence lens covers sources).
- `guide_check.js`; the main session ran it.

## Change log

- Created: `work/handoffs/phase-2/20261106_Stage-A-Reader-Panel.md` (this report).
- Modified: none. Scratch scripts and screenshots sit outside the repository, in the session's scratchpad.
