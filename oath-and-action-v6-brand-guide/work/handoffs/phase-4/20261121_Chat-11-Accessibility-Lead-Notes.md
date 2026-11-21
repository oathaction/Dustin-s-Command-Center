# Chat 11, accessibility lead's notes

Started November 21, 2026, 18:56 UTC (read with `date -u`). Owner: oa-ux-accessibility-lead. Work: the chat 11 brief's section 7. Files held: these notes, and `work/build/scripts/phase-2/stage_c_ch19_build.py` for chapter 19's status map only. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ac32a0f7-d562-5d93-9aba-0ef59f7ca891/scratchpad/c11/accessibility-lead/`.

## Where I am

19:05 UTC. Steps 1 and 2 are done: chapter 20's rulings (AL-01 to AL-18) and chapter 21's (AL-21 to AL-24) are below. Step 3 waits: no chapter 20 page export, standalone HTML page or plate exists yet (`work/build/exports/phase-4/` holds only chat 10's samples; the engineer's contracts C4 to C6 are written and not live; the design director's plan is not written). Step 4 waits for chapter 20's rules. Handed back to the main session at 19:05 UTC, to resume when the pages land.

What step 4 will do, checked now: `stage_c_ch19_build.py`'s map still shows 1.2.1, 1.2.2, 1.2.3 and 1.2.5 as gaps (lines 213 to 217), so chapter 16 did not move them. Chapter 16's own "WCAG 2.2" rows give 1.2.2 to Rule 16.11 and 1.2.1, 1.2.3 and 1.2.5 to Rule 16.12; Rule 16.13 adds the card, the transcript link and play on request, and Rule 16.10 the video's form. The plan: 1.2.1 Met by 16.12 and 16.13 (every video's transcript covers what the screen shows; no product publishes audio alone today), 1.2.2 by 16.11 and 16.13, 1.2.3 and 1.2.5 by 16.12 and 16.10, with `GAP_OWNERS` losing those four; then 2.4.2, 3.1.1 and 3.2.6 by chapter 20's rule numbers; 3.1.2 stays a gap owed by chapter 02 (AL-03).

## Rulings

For the design director (plan and page specs), the engineer (renderers and exports) and the editor (words). Each ruling has a code, AL-01 onward, so a plan or spec can cite it.

### The W3C's own words, read November 21, 2026

Read at 18:57 UTC by `curl` into my scratch (`w3c/`), every page HTTP 200, and the text taken from each page's "Success Criterion" section by script. The Quick Reference (https://www.w3.org/WAI/WCAG22/quickref/) prints "Updated 22 Sep 2025." and gives each level below.

**2.4.2 Page Titled, Level A.** Page: "Understanding Success Criterion 2.4.2: Page Titled", https://www.w3.org/WAI/WCAG22/Understanding/page-titled, read November 21, 2026.

> Web pages have titles that describe topic or purpose.

From its Intent: "The intent of this success criterion is to help users find content and orient themselves within it by ensuring that each web page has a descriptive title. Titles identify the current location without requiring users to read or interpret page content." And: "Having the link and the title agree, or be very similar, is good practice and provides continuity between the link 'clicked on' and the web page that the user lands on." Its example of a set of pages: "Specific patterns are pages titled "X Pattern | APG | WAI | W3C"". Technique G88 (https://www.w3.org/WAI/WCAG22/Techniques/general/G88, read the same day) names its first example "A title that lists the most important identifying information first" and says a title should "Make sense when read out of context" and "Be short".

**3.1.1 Language of Page, Level A.** Page: "Understanding Success Criterion 3.1.1: Language of Page", https://www.w3.org/WAI/WCAG22/Understanding/language-of-page, read November 21, 2026.

> The default human language of each web page can be programmatically determined.

From its Intent: "Screen readers can load the correct pronunciation rules. Visual browsers can display characters and scripts correctly."

**3.1.2 Language of Parts, Level AA.** Page: "Understanding Success Criterion 3.1.2: Language of Parts", https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts, read November 21, 2026.

> The human language of each passage or phrase in the content can be programmatically determined except for proper names, technical terms, words of indeterminate language, and words or phrases that have become part of the vernacular of the immediately surrounding text.

From its Intent: "Phrases and passages consist of one or more words. As a result, even an individual word can be subject to the requirements of this criterion, unless it falls under one of the exceptions." And on names: "Accessible names are "flat" strings, and don't contain any structure or information." It names a workaround, "moving the lang language attribute to the element itself, rather than indicating a change of language on a child nodes inside the element", and says such problems "don't fail the requirements of this success criterion" and that auditors "must verify whether or not changes in natural language have been identified correctly in the underlying code or markup."

**3.2.6 Consistent Help, Level A, added in WCAG 2.2.** Page: "Understanding Success Criterion 3.2.6: Consistent Help", https://www.w3.org/WAI/WCAG22/Understanding/consistent-help, read November 21, 2026.

> If a web page contains any of the following help mechanisms, and those mechanisms are repeated on multiple web pages within a set of web pages, they occur in the same order relative to other page content, unless a change is initiated by the user:
>
> Human contact details;
> Human contact mechanism;
> Self-help option;
> A fully automated contact mechanism.
>
> Note 1: Help mechanisms may be provided directly on the page, or may be provided via a direct link to a different page containing the information.
>
> Note 2: For this success criterion, "the same order relative to other page content" can be thought of as how the content is ordered when the page is serialized. The visual position of a help mechanism is likely to be consistent across pages for the same page variation (e.g., CSS break-point). The user can initiate a change, such as changing the page's zoom or orientation, which may trigger a different page variation. This criterion is concerned with relative order across pages displayed in the same page variation (e.g., same zoom level and orientation).

The page prints "break-point" with a hyphen while its errata list says "Harmonizing occurrences of "breakpoint" to be one word"; the Quick Reference prints the same "break-point". I quote it as printed. Its "Help Mechanisms" section: "Human contact details such as a phone number, email address, hours of operation." "Human contact mechanism such as a messaging system, chat client, contact form, social media channel." "Self-help option such as an up-to-date Frequently Asked Questions, How Do I page, Support page." "A fully automated contact mechanism such as a chatbot." From its Intent: "This is distinct from interface-level help, such as contextual help, features like spell checkers, and instructional text in a form." And: "the absence of a help mechanism on certain pages within a set does not constitute a violation."

**Three more the rulings lean on**, from the same day's reads:

- 2.4.1 Bypass Blocks, Level A (https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks): "A mechanism is available to bypass blocks of content that are repeated on multiple web pages."
- 2.4.11 Focus Not Obscured (Minimum), Level AA (https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum): "When a user interface component receives keyboard focus, the component is not entirely hidden due to author-created content."
- 2.5.8 Target Size (Minimum), Level AA (https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum): "The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:" followed by its five exceptions, Spacing, Equivalent, Inline, User Agent Control and Essential. The Inline exception reads: "The target is in a sentence or its size is otherwise constrained by the line-height of non-target text;"

### What chapter 18 already settles, and stays

The website builds on chapter 18's approved components and changes none of them. Rule 18.6: the masthead's parts sit in a named navigation, and "When the parts no longer fit on one line, they move behind a Menu button, its three bars beside the word Menu, which opens them in a native modal dialog." Rule 18.4: the theme switch is three radio buttons under the legend "Theme" (Light, Dark, Match my device), "in the masthead or at the top of the phone menu". Rule 18.5: the skip link is "the first stop on every page", and a link to another site "opens in the same tab; its 16 px mark follows its last word, and the words “(another site)” end its name for screen readers (Rule 11.15)". Rule 18.8: disclosures. Rules 14.2 and 14.13: every chart's eight parts and its table as live text.

### Chapter 20's rulings

**AL-01. Page titles (2.4.2).** Every page's `<title>` puts the page's own words first and the site's name last, joined by a spaced vertical bar, as the W3C's own set does and G88's first example advises: "What a special district does | Oath & Action". The first part is the page's h1 words, or a shorter form of them the editor writes when the h1 runs past about 60 characters, so the tab and the heading agree. The home page is the one exception, since the site is its subject: "Oath & Action | A country that answers to its people." (the locked principal tagline, exact). Atlas pages add the atlas's name between: "[view] | Who Do They Answer To? | Oath & Action" (for chapter 21). Every title is unique on the site. Opening the menu or changing the theme changes no title. Since a guide plate cannot hold a `<title>`, each page's plate shows the title in words above its frames (a drawn tab or a "Page title" line), copied from the page's markup by the renderer, never typed twice; the failure plate can show three tabs that all read "Oath & Action". The separator is not a dash, so the writing rules hold; screen readers at their default punctuation say nothing for it.

**AL-02. Page language (3.1.1).** Every page's root is `<html lang="en">`, as the guide's own root is. Plain "en" leaves the choice of an American or British voice to the reader's settings; the words follow American spelling either way. Each standalone HTML export carries it; a plate inside the guide takes the guide's root.

**AL-03. Language of parts (3.1.2), the markup half.** A passage or phrase in another language takes `lang` on the smallest element that holds exactly that passage, with its BCP 47 code (`lang="es"` for Spanish). When the passage is a link's or a button's whole name, `lang` goes on the link or the button itself, the workaround the Understanding page names, since a name is a flat string. A link to a page in another language also takes `hreflang`. The exceptions stand as the criterion lists them: proper names (Regulations.gov, the Federal Register), technical terms (N-acetyl-L-cysteine, NAC) and words now part of English need no `lang`. Chapter 20's rule shows the markup in a code panel on a real phrase the pages print, chosen by the design director and the editor; none is invented for it. What chapter 02 still owes (not reopened this chat): the writer's half, a rule or specification row in Voice that says when a quoted passage stays in its own language, that it is marked for its `lang` and translated beside it, and that names and terms are exempt. Chapter 19's 3.1.2 row stays a gap, owed by chapter 02, until then.

**AL-04. Help in the same place on every page (3.2.6).** The site's help is a human contact mechanism: one link, the editor's words (for example "Contact us"), to a contact page, or an email link labeled Illustrative beside it as DR-308 labels the address. It sits in the footer, in the same place in the footer's order on every page of the site, the atlas's pages included (one set of pages, DR-307). The masthead's parts stay DR-307's list and gain no help link. The footer is drawn from one source by one renderer, so its order cannot drift between pages; the check compares each page's serialized order of the footer's links. The Act page's own words on how to comment, and the agency's contact line the docket prints, are content and contextual help, which the Understanding page sets apart, and they stay where the page's steps need them. A page may not drop the footer's help link (the criterion allows an absent mechanism; this site keeps one everywhere, since a reader stuck on a rule's comment form needs it most).

**AL-05. The masthead at each width.** The parts are DR-307's seven, in its order: Explain, Track, Connect, Act, Who Do They Answer To?, About, Subscribe. They sit in the bar, after the wordmark's home link, at every width where all seven and the wordmark fit on one line at the masthead's type size; the design director measures that width and writes it in em (chapter 07's rule), and the bar is never used under 48em. Below that width the parts move behind Menu (AL-06). By my estimate the seven words need about 650 px with 24 px gaps, so at 1024 px they fit beside the wordmark and the switch does not; the design director's measure decides. Text zoom moves the layout by em, so a reader at 200 percent on a 1024 px window gets Menu. At 390, 360 and 320 px, the bar holds the 16 px wordmark (152 px) and Menu on one line with no sideways scroll.

**AL-06. The menu under the breakpoint: Rule 18.6's modal dialog.** The brief's "disclosure menu" is answered by Rule 18.6, which chapter 18 approved: Menu opens the parts in a native `<dialog>` with `showModal()`. Its rows open as disclosures (Rule 18.8) only if a part holds a sublist; DR-307's seven need none. In detail, as Rule 18.6 and `c-18-masthead` set:
- Menu is a `<button type="button">` whose name is its visible word, "Menu" (the bars are `aria-hidden`), with `aria-haspopup="dialog"`, `aria-controls` naming the dialog, and `aria-expanded="false"`, set to "true" while the menu is open.
- On open, focus moves to the link for the part the reader is in; on a page with no current part (the home page), to "Close the menu", as chapter 18's script does.
- Tab and Shift+Tab stay inside the dialog; the page behind is inert.
- Escape, "Close the menu" (44 by 44 px) and following a link each close it. On Escape or Close, focus returns to Menu and `aria-expanded` returns to "false". A link that leads to another page simply loads it.
- The dialog is named by its title, "Menu", and holds, top to bottom: the title and Close, the theme switch (AL-08), then the parts in a navigation named as AL-09 sets.
- The dialog scrolls inside itself when the parts and the switch outgrow a short or zoomed screen, and Close stays reachable by Tab.
- New, for the website: if the window widens past the breakpoint while the menu is open (a phone turned sideways, a reader zooming out), the menu closes and focus goes to the current part's link in the bar, or to the home link when no part is current, since Menu is then hidden. Without this, focus would rest on a hidden button (2.4.3, 2.4.7). This goes to the engineer as a request against the site's script, not chapter 18's code set.

**AL-07. Focus order (2.4.3, 1.3.2).** At 1440 and 1024 px: the skip link, the home link, the seven parts in DR-307's order, the theme switch (one Tab stop, at the checked choice), then the page's content, then the footer. At 390 and 360 px: the skip link, the home link, Menu, the content, the footer; inside the open menu, Close, the switch, the parts. The reading order in the markup matches what a reader sees at every width, so the switch sits after the parts on the screen as well: at the bar's right end, or on a row beneath the bar at its right edge when it does not fit beside the parts; never on a row above them.

**AL-08. The theme switch in the website (Rule 18.4, DR-204).** At 1440 and 1024 px it sits in the masthead, outside the navigation landmark (it is a setting, not a place), after the parts. Under the breakpoint it sits at the top of the phone menu, after Close. It is chapter 18's switch read from its files, never copied: a `<fieldset>` with the legend "Theme", three radios in one Tab stop, the arrow keys moving and choosing, the colors changing at once with no motion, focus staying on the choice. Light and Dark set `data-oa-theme` on the root and store `oa-theme`; Match my device removes the key. The head script applies a stored choice before the first paint, and on load the stored choice is the checked radio, so a reader who reloads sees Dark checked and the page dark. Each segment is 44 px tall. If "Match my device" and its two neighbors do not fit in one row at 360 px, the three stack, each still 44 px tall, with no word cut.

**AL-09. Landmarks and their names (1.3.1, 2.4.1).** On the site and in each standalone export: the skip link as the body's first element, then one `<header>` (banner) holding the masthead; the parts in `<nav aria-label="Parts of the site">` (Rule 18.6's name); one `<main id="main" tabindex="-1">`; one `<footer>` (contentinfo) at the top level. The dialog's navigation is named "Parts of the site, in the menu", as chapter 18's code names it. A footer navigation, if the footer holds one, takes a name for what it holds that differs from the masthead's. The article page wraps its story in `<article>` inside `<main>`, and a breadcrumb, if the design shows one, is `<nav aria-label="Breadcrumb">` (Rule 18.7). No `<aside>` sits inside the article; a related list is a section with a heading. The chat 10 sample's "About this sample" strip is guide furniture: it stays out of the site's export or becomes plain text, since a complementary landmark above the banner breaks the outline. Inside the guide, a plate must not add landmarks or headings to the guide's own lists (the guide check's AX-S8 and structure tests). Under the engineer's C4 a frame keeps the page's real landmarks and headings inside `inert` and `aria-hidden="true"` markup, so neither list sees them, and the plate's specification table lists the landmarks the export carries.

**AL-10. Headings (1.3.1, 2.4.6).** One h1 a page. Article: the headline is the h1, its sections h2, and the chart's title the level the chart kit gives it under that h2. Act page: the h1 is the page's question in the editor's words, each step an h2 or an ordered list item under one h2, never a skipped level. Home page: the h1 is a visible heading the design director places, or, if the design shows none, the wordmark's home link sits inside the h1 on the home page alone (`<h1><a href="/" aria-current="page">` with the wordmark's name "Oath & Action"); each pillar's section and the atlas's section take h2. The masthead holds no heading. Footer groups may take h2 headings.

**AL-11. The skip link (2.4.1, Rule 18.5).** The first Tab stop on every page, hidden until it takes focus, then shown at the top left above the masthead (never under a sticky masthead), 44 px tall with the focus ring. It leads to `<main>` and moves focus there. Its words are the editor's and name where it goes, as the chat 10 sample's "Skip to the article" does; one wording for every page type (for example "Skip to the page" or "Skip to the content") keeps 3.2.4.

**AL-12. A sticky masthead (2.4.11, 1.4.10).** If the masthead sticks, the page sets `scroll-padding-top` to its height (Rule 18.6), so no focused link hides under it. It stops sticking on short screens (for example `@media (max-height: 30em)`), where a sticky bar at 200 percent text would cover a third of the window. The open menu covers the page by design; that is content the reader opened (2.4.11's Note 2).

**AL-13. The Act page's link to Regulations.gov (2.4.4, Rules 18.5 and 11.15).** The link opens in the same tab, with no `target="_blank"`. Its words name the action and the place, in the editor's words (for example "Comment on docket FDA-2025-N-2699 at Regulations.gov"); the outside-link mark, the arrow leaving a box, follows the last word at 16 px with `aria-hidden="true"`, held on that word's line; and the hidden words "(another site)" end its name. The full address the docket file gives (https://www.regulations.gov/commenton/FDA-2025-N-2699-0001) prints as text beside or under it, so a reader can copy it or read it on paper. If the link is the page's one way to take part, drawn in red on its own shape (Rule 11.4), it stays a link (it goes somewhere), it is 44 px tall, its words are White on Pillar Red at the ask's type token, `oa.type.ask` (Inter 700, 19 px), since White on Pillar Red measures 4.17 to 1 and passes only as large text (D4-91), and its focus ring must stand off both the red and the Newsprint (I measure it in the walks). Every other outside link on the page (the Federal Register page, govinfo's PDF) follows Rule 11.15 the same way.

**AL-14. The article's chart (1.1.1, 1.3.1, 1.4.1).** S86 keeps the chart kit's anatomy whole inside the article (Rule 14.2's eight parts in order), with its table as live text folded under the source line as "The table and notes" (Rule 14.13), the disclosure's summary at least 44 px tall. The drawing's text alternative is the kit's own description, never a new one written for the article. The article's own sentence around the chart says what the chart shows, so a reader who skips the figure loses no finding. At 390 and 360 px the table reflows or scrolls inside a named group with a Tab stop (Rule 18.11, as D4-92 fixed for chapter 16), with no sideways scroll of the page.

**AL-15. Target sizes at 360 px (2.5.8; the studio's 44 px token).** Every control a thumb uses is at least 44 px tall (`oa.size.target.touch`): the skip link, the home link's box (the 16 px wordmark with padding), Menu, Close the menu (44 by 44), each theme segment, each part's row in the menu, the chart's disclosure, the Act page's outside link, and each footer link set as a list. Links inside a sentence take 2.5.8's Inline exception and keep their line. Nothing on any page is smaller than 24 by 24 px without the Spacing exception's 24 px circle clear of its neighbors. I measure every one in the walks.

**AL-16. Color and state checks I hold the pages to (1.4.3, 1.4.11, 1.4.1).** Text 4.5 to 1, large text 3 to 1, marks and control edges 3 to 1, on each frame's pixels, Charcoal included. The current part keeps Rule 18.6's bold words and 2 px underline, so its color is never the only sign. Subscribe in red would put a second working red in a view on the Act page (Rule 05.3) and needs the ask's type for contrast; I flag it for the design director's plan, without ruling on the look.

**AL-17. For chapter 21: the atlas inside the site (DR-307).** Atlas pages carry the site's masthead, with "Who Do They Answer To?" as the current part, and the atlas's title bar beneath it as a second navigation named for what it holds (for example "Atlas views"), never a second banner. The page title follows AL-01's three-part form. The footer and its help link are the site's (AL-04).

**AL-18. Plates inside the guide (2.1.1, 2.4.1, 4.1.2, 1.1.1). Revised 19:05 UTC to agree with the engineer's contract C4.** Each page plate shows six or more frames, and each frame holds 20 or more links and controls; if every frame took focus, a keyboard reader would press Tab over a hundred times to pass one plate. So every frame in the guide is a picture, as C4 draws it: an SVG with `role="img"` named by the frame's alt, its page markup `inert` and `aria-hidden="true"`, no Tab stop inside. The working pages are the standalone HTML exports, where I walk the skip link, the parts, the menu and the switch; chapter 18's live masthead (Rule 18.6) and switch (Rule 18.4) stay the reader's live trial inside the guide. Each frame's alt is written for its purpose: the page, the width, the theme, the state (menu open or closed) and what the frame shows that the others do not, in a sentence or two, never the page's whole text. The plate's caption or specification table names the export a reader can open to try the page.

### Which criteria each chapter 20 subject meets

For the plan's "WCAG" lines, by subject. The design director maps them to rule numbers.

| Subject | Criteria |
|---|---|
| Page titles | 2.4.2 |
| Page language and parts in another language | 3.1.1; 3.1.2 (markup half) |
| Masthead and parts | 1.3.1, 2.4.1, 2.4.3, 3.2.3, 3.2.4, 4.1.2 |
| Phone menu | 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11, 2.5.3, 2.5.8, 4.1.2 |
| Theme switch | 1.4.3, 1.4.11, 3.2.2, 3.2.3, 4.1.2 |
| Skip link and landmarks | 2.4.1, 1.3.1 |
| Help in the footer | 3.2.6 |
| Article and its chart | 1.1.1, 1.3.1, 1.4.1, 1.4.10, 2.4.6 |
| Act page and its outside link | 2.4.4, 2.5.8, 1.4.3 |
| Every page at four widths and dark | 1.4.3, 1.4.4, 1.4.10, 1.4.11, 1.4.12 |
| Share preview | None on the site itself, since the card shows on other sites; its words also go in `og:image:alt` and `twitter:image:alt`, so a platform that reads them can speak them, and they repeat the page's title |
| Favicons | None by themselves; the page title (2.4.2) names the tab |

## Rulings for chapter 21

For the data visualization lead's plan. Each register row below sits in Atlas V7's own interface, which is not in this repository; chapter 21 draws the atlas's views from the application kit, so each ruling binds the kit's atlas renderers and the plates, and the atlas's own source takes the same fix at its next version.

**AL-21. UX-4, a pressed question shown by weight alone.** A question button that is pressed draws Rule 17.10's one look (D2-1152): the selected check (U-selected-check from the utility set) before the words, the words in bold, and a 2 px edge in the strong border color where an unpressed question keeps 1 px; `aria-pressed="true"`. The check and the edge are shapes, so the state holds in forced colors and in gray print. The plate shows one question pressed beside unpressed ones at 1440 and 390 px, on Newsprint and Charcoal. Criteria: 1.4.1, 4.1.2 (and the guide's own Rule 17.10).

**AL-22. F-8, the stepper's button order.** The atlas's loop stepper runs Rule 18.22's order and names, the same in every product: Play, Reset the loop, Previous step, Next step, each with its utility icon beside its word (D2-1154). On a phone the four sit in a two-by-two grid in that reading order (Play and Reset the loop, then Previous step and Next step). Criteria: 3.2.4; 2.4.3.

**AL-23. F-14, marks on Charcoal.** On Charcoal (Night Edition) a muted mark reads `--oa-color-state-muted-mark-on-charcoal` (Dim Newsprint, 7.26 to 1), never Stone (3.10 to 1), and a muted label `--oa-color-state-muted-text-on-charcoal`; the selected bar reads `--oa-color-state-selected-bar-on-charcoal` (Newsprint), never White. Every color in a dark atlas view comes from a token read from `tokens.css`, never a hex in the renderer, and the plan states each mark's ratio measured on the plate's pixels. Criteria: 1.4.11, 1.4.3.

**AL-24. F-15, the stepper's pace.** Rule 18.22's pace, as chapter 18 times it: Play holds each step about 250 ms a word of everything the status line reads, "Step 2 of 3:" included (D2-1019), and never under 6 seconds (D2-972), with reduced motion too; nothing plays until the reader presses Play; Play becomes Pause and then Play again; Next step, Previous step and Reset the loop stop playback, and no button moves focus. The plan prints each loop's hold per step, counted by script from its status lines, as D3-1755 did. Criteria: 2.2.2, 2.3.3 (the guide's own pace), 4.1.3 for the status line.

## Routine calls

- D4-xxx | The website's phone menu is Rule 18.6's native modal dialog, and the brief's "disclosure menu under 48em" is read as that dialog's Menu button | Rule 18.6 is approved and names the dialog; a disclosure in its place would change approved work (brief section 2)
- D4-xxx | Page titles put the page's words first and "Oath & Action" last, joined by " | "; the home page leads with the site's name | The W3C's own set and Technique G88's first example; no dash, so chapter 02's rules hold
- D4-xxx | `<html lang="en">` on every page, without a region | It matches the guide's root and leaves the reader's voice choice alone
- D4-xxx | The site's one help mechanism is a contact link in the footer, at one place in the footer's order on every page | WCAG 3.2.6; DR-307 fixes the masthead's parts, and one renderer draws the footer for every page
- D4-xxx | If the window widens past the breakpoint with the menu open, the menu closes and focus goes to the current part's link in the bar | Otherwise focus rests on a hidden button (2.4.3, 2.4.7)
- D4-xxx | Every page frame in the guide is a picture named by its alt, as the engineer's C4 draws it, and the standalone exports are the working pages I walk | Six frames of 20 or more stops each would make a keyboard reader press Tab over a hundred times per plate (2.4.1); chapter 18's live masthead and switch stay the trial inside the guide

## Done

- 18:57 UTC: the W3C pages read and quoted above.
- 18:58 to 19:04 UTC: chapter 20's rulings AL-01 to AL-18, and chapter 21's AL-21 to AL-24, written.

## Requests

- Engineer (`work/build/app-kit/renderers/web-page.mjs` and the site's script): (1) for my walks, each page as a standalone HTML file in your exports or scratch, with chapter 18's masthead and theme-switch scripts and the head script loaded, so the menu opens and closes, Escape works and the switch's choice survives a reload; name the paths under "Contracts". (2) AL-06's close-on-widen behavior in the site's menu script. (3) AL-01's title line on each plate, read from the page's own `<title>`. AL-18 now follows your C4; inside a frame the page keeps its real landmarks and headings, hidden from the guide's lists by `inert` and `aria-hidden`, which also answers AL-09's last sentence.
- Design director (plan and specs): AL-01 to AL-17 as written; the bar's em breakpoint measured (AL-05); the switch's place at 1024 px (AL-07); the footer's help link and its place (AL-04).
- Editor (later, chapter 20's words): each page's title, the skip link's one wording, the help link's words, the outside link's words.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| AL11-1 | My reading of Rule 18.6 against WAI-ARIA 1.2's `aria-current` values | Rule 18.6's rule text and `c-18-masthead` | Rule 18.6 gives `aria-current="page"` to "the part the reader is in". On an article inside Explain, the Explain link is not the current page, so a screen reader says "current page" on a link to another page. ARIA's "true" ("current") fits a section that holds the page | Give a part link `aria-current="page"` only on the part's own front page, and `aria-current="true"` on pages inside it, with the same bold words and 2 px underline | Rule 18.6 is approved work (brief section 2); the website follows its words this chat. Minor: the visual cue and the landmark are right either way | Open |

## Tested

- The eleven W3C pages above (the Quick Reference, nine Understanding pages and Technique G88), fetched at 18:57 UTC (G88 between 18:58 and 19:01), HTTP 200 each, quoted from the saved HTML by script.

## Not tested

- Nothing on chapter 20's pages yet: no page, export or plate of chapter 20 exists at 19:04 UTC.
