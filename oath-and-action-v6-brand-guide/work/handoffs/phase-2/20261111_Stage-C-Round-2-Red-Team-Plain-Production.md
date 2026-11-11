# Red team, stage C round 2: plain language and the production test

Oath & Action Edition 06, Phase 2, stage C, round 2, November 11, 2026. Reviewer: a civic educator who teaches adults, applying `oa-editor.md`'s rules, then a simulated panel of three. Brief: `20261111_Stage-C-Round-2-Brief.md`. Page: the frozen chapters page at commit df0fb08d (`scratchpad/round-2/review/guide.html`).

**The panel is simulated and untested with real people.** One reviewer played a developer, a designer and an auditor in turn, each reading only what the brief allowed. The panel's files sit in `work/handoffs/phase-2/stage-c-round-2/production-test/`.

## 1. Score

**3 of 5.** The prose in chapters 17, 18, 19 and 26 reads plainly aloud and carries none of chapter 02's banned patterns that a script can find, yet a developer who follows the page's own instructions loses dark mode, and the token block offered as a second route drew Rule 18.17's form with no type, spacing or edges.

## 2. Must fix

**M1. The page tells builders to put a surface class where it pins the ground, and dark mode stops working.**
- Where: chapter 26, Rule 26.3's For builders line and Rule 26.6; the For builders blocks that close chapters 17, 18 and 26.
- What is wrong: Rule 26.3 says "Write the role's short name in your CSS and the surface class in your HTML." Each chapter's closing block says "Set a page's ground with a surface class, as in `<body class="oa-surface-newsprint">`". A surface class keeps its own ground in both themes (D2-1191), so the developer's cards, built as told, stayed Newsprint with Charcoal words when the root turned dark, in both the `data-oa-theme="dark"` run and the device run (computed ground `rgb(220, 217, 210)`). Rule 26.6, the rule a builder reads for dark mode, never says to leave the class off. The only place that says it is a comment inside tokens.css: "a product that follows the theme puts no surface class on its body."
- Fix: In Rule 26.6 add: "A surface class keeps its own ground in both themes. In a product that follows the theme, put no surface class on the body or on a block that should follow it; use one only where a block must keep one ground, as Rule 26.4's White and Prussian examples do." Change Rule 26.3's For builders line to "Write the role's short name in your CSS. Add a surface class in your HTML only where a block must keep one ground in both themes." Change the closing blocks' comment to say that with tokens.css linked, the theme sets the page's ground and the body takes no surface class.
- Owner: Engineer (chapter 26 and the shell's closing block).

**M2. The token block each chapter offers "so it also works on its own" is missing most of what its code reads.**
- Where: the For builders sections that close chapters 17, 18 and 26 ("Link it before your own styles, or copy this chapter's block, which holds the 308 custom properties it needs, with the type parts and their clamps").
- What is wrong: Chapter 18's block defines 400 properties but none of `--oa-type-body`, `--oa-type-ui`, `--oa-type-ask`, `--oa-space-050` to `--oa-space-800`, `--oa-border-width-hairline`, `--oa-border-focus-offset`, `--oa-font-weight-*`, `--oa-radius-none` and 23 more that chapter 18's code panels read: 37 in all. Its own comment says "set type with font: var(--oa-type-body)", a property it does not hold. Chapter 26's block misses 15 the chapter's code reads. Rule 18.17's form, pasted with chapter 18's block in place of tokens.css, drew in Times New Roman at 16 px with no field edges, no padding, fields about 18 px tall and a send button under the 44 px target. D2-266 says "the copied block works alone"; it does not. The block also leaves out the themes, so it cannot serve a themed product, which the "or" never says.
- Fix: build each block from every property the chapter's code panels read, with their dependencies, and test it the way the guide check tests code sets; or drop the "or copy this chapter's block" route and the "works on its own" claim and keep tokens.css as the one source. Either way, say beside the block that it holds no themes.
- Owner: Engineer (`guide_build.py`).

## 3. Should fix

**S1. Rule and code disagree on the "Sending" word.** Rule 18.1 says "While a send runs, its word reads 'Sending'", and Rule 18.17's specification says "Sending: the button reads 'Sending' and carries aria-disabled." The `c-18-form` script never changes the word: on the frozen page the live form's button still reads "Remind me" during the send, with "Sending your request." only in the status line (checked by script). Fix: the script swaps the word to "Sending" and back, as the developer had to add. Owner: Component engineer, with the Accessibility lead for Rule 18.17's specification if the words change instead.

**S2. Rule 18.1 names two sets of tokens for one job.** Its TOKENS box lists `--oa-color-action-primary-fill`, `--oa-color-action-ask-fill` and `--oa-color-state-disabled-text`; its CSS reads `--oa-component-button-primary-fill`, `--oa-component-button-ask-fill` and `--oa-component-button-disabled-label`. Chapter 18's closing token table lists the first set and none of the second, nor `--oa-color-state-success-text`, which Rule 18.17's code reads. Rule 26.3 tells builders the component token wins, so the box should name the component tokens the code reads. Owner: Accessibility lead.

**S3. For builders lines that do not match the code.** Rule 18.1's says "with the script stopping its press", but Rule 18.1 prints no script. Rule 18.2's gives `<button type="button" class="oa-chip" aria-pressed="false">`, while the code uses `class="oa-toggle oa-toggle--chip"`. Rule 18.4's Browser support lists "the change event of matchMedia()", which its script never uses. Fix: point 18.1 to Rule 18.17's script or print the three lines; use the code's own class in 18.2; drop the matchMedia line or say why it is there. Owner: Accessibility lead.

**S4. Chapter 18 copies `data-red` and `data-red-job` without a word on what they do.** They appear in Rules 18.1, 18.17 and 18.18's code. Only Rule 05.3's For builders line explains them ("Mark each red element with data-red ... The shared check fails a view with two working jobs"). The same rule leaves "where Rule 05.3 gives the view its working red" unexplained for a builder of chapters 18 and 26. Fix: one sentence in Rule 18.1's For builders: "data-red and data-red-job mark the view's one working red for Rule 05.3's check: an error first, then the one step a reader can take now. Move them as the red moves." Owner: Accessibility lead.

**S5. Chapter 18 covers an action that cannot run yet, and none that can no longer run.** A full event, a closed comment period or a vote already taken leaves the developer guessing whether fields stay ("A field stays open to typing at all times") and what the reason line says. Fix: add to Rule 18.1: "When an action can no longer run, such as a full event, keep the button in place with its reason and the step the reader can take instead, and leave out fields that can no longer send." Owner: Accessibility lead.

**S6. Rule 26.5 leaves the head script out of the page it tells builders to start from.** Its head panel and its "Order in the head" specification give the meta tag, the fonts, tokens.css and your styles. Rules 18.4 and 26.6 put a head script "before the stylesheets". A builder must merge three rules to get one head. Fix: show the head script first in Rule 26.5's panel and specification, marked "for a product that offers the theme switch". Owner: Engineer.

**S7. Rule 26.3's five steps leave gaps a designer falls into.** The emphasis step lists "primary or secondary; essential or subtle; emphasis or context" and nothing for a border, so "strong" and "hairline" have to be found in the table. "Role" names the token's job here and the ARIA role in chapter 18 ("the role 'button'"); "state" is both one of the eight roles and step 4. No state covers a neutral notice, so the designer borrowed `--oa-color-border-strong`, whose job is "Edges of inputs and controls that a reader must find". Fix: add "strong or hairline for a border" to step 3; add "Role here means the token's job, such as text or border, and not the role a screen reader names"; and say where a message with no state goes: words in `--oa-color-text-primary`, its bar in `--oa-color-graphic-essential` at `--oa-border-width-bar`. Owner: Engineer.

**S8. Terms a newcomer meets with no definition.**
- "Accessible name" heads a row in all 24 of chapter 18's specifications and is never defined; chapter 17 defines "accessible description" but not the name. Chapter 18's opening says "A screen reader hears the name, role, state and status line the code hands it" before any of the four is explained.
- "Landmark" (Rules 18.6, 18.7 and 18.15, Rule 11.12's builders line, first in chapter 07) is never defined.
- "APG" stands in 17 basis lines from Rule 18.1 on and is spelled out only in the sources at the chapter's end; "ARIA" the same.
- Chapter 19 never says what levels A and AA mean, or what a success criterion is, though Rule 19.1 builds on both.
- Fix: define each where it first appears, for example "its accessible name, the words a screen reader says for it", "a landmark, a region a screen reader can jump to, such as the navigation", "the ARIA Authoring Practices Guide (APG)", "Level A is the floor; level AA, which most laws ask for, adds criteria such as contrast", "a success criterion, one requirement a page can be tested against". Owners: Accessibility lead for chapters 18 and 19; Editor for chapters 07 and 11.

**S9. One idea, three names, in chapter 18.** It says "status line" (Rules 18.18 to 18.21), "polite live region" (Rule 18.22, "One polite live region says each step") and "live region" (Rule 18.23's builders line and the CSS comment "A status line is a polite live region a script writes"), against H02's "keep the same term after that". Fix: use "status line" throughout and define it once in the chapter's opening. Owner: Accessibility lead.

**S10. Rule 19.7's matrix leaves an auditor unsure what proves a form.** No row names 1.3.5, 2.5.8, 3.3.1, 3.3.2, 3.3.3 or 4.1.3; the only check that hears a form's error is item 9 of Rule 19.9's device script, run before launch. "Automated rules" serves "Many, in part" and asks for "the WCAG 2.2 A and AA tags", though axe-core has no `wcag22a` tag. "Text at 200 percent and 320 px" claims 1.4.12 but its method gives none of the four spacing values and no way to set the text size, and a script that looks for clipping passes a word broken mid-word. "Dark surfaces and long labels" and listening item 3 ("the chapter, then each rule") are written for the guide's own page. Fix: add a row "Forms and messages: send each form empty, then wrong, by keyboard; focus lands on the first field to fix, its description holds the message, and the status line holds the result" for 1.3.5, 3.3.1 to 3.3.3 and 4.1.3; measure targets under Keyboard and focus for 2.5.8; name the axe tags (`wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`); give the spacing values and say how to set text to 200 percent; word the guide-only checks for any page. Owner: Accessibility lead.

**S11. A claim larger than its check.** Rule 26.5's Why says the guide compares each code set's drawing "with the live demo, pixel for pixel". The check tolerates edge differences up to 49 of 255 (D2-1526), and Rule 19.8's results say 20 to 25 of chapter 18's 48 stages drew differently. Fix (W20): "compares what it draws with the live demo, and lists the differences in Rule 19.8's results." Owner: Engineer.

**S12. Instructions a reader cannot act on.**
- Rule 26.2's For builders: "Ask for a token before you add a value of your own" names no one to ask. Its rule paragraph is one 74-word sentence holding all five conditions; the plate's five-row checklist reads better than the sentence.
- Rule 10.9's For builders tells a reader to run `node work/build/scripts/phase-2/icon_likeness_check.js`, a studio file path no builder outside the studio has.
- Rule 03.2's For builders is one paragraph of about 280 words holding six jobs: check the minimum, retire L2, build L4 to L7 with a 14.7-unit shift, place L3 three ways, and keep the old master "as the record". A builder looking for one lockup cannot find it.
- Fix: name who answers a token request; say who runs the likeness test, or ship the script; break 03.2's paragraph into one short line per lockup and drop the record-keeping sentence. Owners: Engineer (26.2), Systems designer (10.9), Identity designer with the Editor (03.2).

**S13. Small edits for the Editor.**
- Rule 11.12's builders line says "let the Escape key clear it", while Rule 18.15 says "Handle Escape in the script, since browsers differ". Make 11.12 say "clear it on Escape in your script, as Rule 18.15 does." Owner: Systems designer.
- Rule 17.9's first sentence buries its object: "thickens the edge of a quiet control, its word in ink inside a 1 px edge, to 2 px". Write "or thickens a quiet control's 1 px edge to 2 px." Owner: Systems designer.
- Rule 17.8's failure caption reads "Fails WCAG 2.2 SC 1.4.1." and Rule 05.4's "Fails 1.4.1.", where every other failure names our rule. Owner: Systems designer.

## 4. Questions for Dustin

None. Every fix above sits inside the approved stage. M2's choice, a complete block or no block, is the engineer's routine call under D2-266.

## 5. The panel

### 5.1 The developer: an event sign-up card (DR-219)

Built from the page's chapters 18 and 26 (words, code panels as printed, token table) and `tokens.css` alone, in three versions. Full log: `production-test/20261111_Developer-Step-Log.md`. The event, two sessions of an Alder County library budget workshop in March 2027, is invented and labeled Illustrative beside each card and in the page's lede.

**What the card does.** Each card gives the date, the place and the seats. The first session is full: its "Save my seat" button stays in the Tab order with `aria-disabled`, a dashed edge and a reason line ("Every seat in this session is taken. The second session, on Thursday, March 18, still has seats."). The second takes a name and an email, sends them empty or wrong with focus on the first field to fix, shows "Sending" while it saves, then writes "You're signed up." with the success mark into a status line and drops the seat count from 8 to 7. Rule 18.4's theme switch sits above the cards and stores its choice.

**Where the guide failed the developer.**
1. Dark mode broke when the developer followed Rule 26.3 and the closing blocks (M1). Only a comment in tokens.css gave the answer.
2. Rule 18.1 and Rule 18.17 promise a "Sending" word the code does not give (S1).
3. Rule 18.1's TOKENS box and CSS name different tokens (S2).
4. Rule 18.1's For builders points to a script it does not print (S3).
5. `data-red` and the ask's working red needed chapter 05, which the developer did not have (S4). Guessed right, by copying Rule 18.17.
6. Nothing covers a full event (S5). The developer guessed: drop the fields, keep the button and its reason.
7. Rule 26.5's head omits the head script (S6).
8. Chapter 18 has no card or label-and-value pattern, so the developer borrowed Rule 26.4's chart rows, whose fixed label column broke words at large text (see below).

**Where the developer failed the guide.**
1. No skip link. Rule 18.5 says "A skip link is the first stop on every page"; the developer never opened Rule 18.5, since the card is not a link. Chapter 19 points 2.4.1 to Rules 18.5 and 18.6, where the auditor found it.
2. Both buttons are named "Save my seat", so a screen reader's list of buttons repeats one name. Rule 18.13's reasoning about ten Copy buttons applies, and the developer missed it.
3. A second press on the open card takes a second seat for the same person. Nothing in the guide asks for this, and nothing stops it.
4. The first facts list used a fixed 5rem label column with `overflow-wrap: anywhere`, which broke "March" and "Alder" mid-word with text at 200 percent on a 390 px phone. Fixed in version 3 with a row that wraps its value under its label.
5. "6 p.m." could split across lines; fixed with a no-break space.

**What the guide made easy.** Copying Rule 18.17's form gave a card with no axe-core violation in any state, a keyboard path that works first time, forced colors that keep every edge and bar, and colors that are all tokens.

### 5.2 The designer: a correction notice on Newsprint and Charcoal

Chapter 26's five steps and token table alone. CSS: `production-test/correction-notice.css`.

- Step 1, surface: Newsprint and Charcoal through the theme. Stuck: whether to add a surface class; found the answer only in tokens.css (M1).
- Step 2, role: text for the words, border for the bar. Stuck: "state" is offered as a role, and a correction is none of the eight states.
- Step 3, emphasis: primary words, secondary date. Stuck: no emphasis listed for a border; found "strong" by searching the table.
- Step 4, state: none fits. Step 5, component: none.
- Chosen: `--oa-color-text-primary`, `--oa-color-text-secondary`, `--oa-color-border-strong` at `--oa-border-width-bar`, with "Correction:" in bold as the first word, as Rule 18.18 sets for "Error:" and "Warning:".
- Measured in Chromium: words Charcoal on Newsprint and Newsprint on Charcoal, 13.29 to 1; date 5.49 and 7.26; bar 13.29 on both; the bar holds in forced colors as CanvasText.

**Compared with chapter 26's rules and the token architecture.** The architecture (`work/ledger/20261021_Token-Architecture.md`, sections 3 and 4) has no notice or correction state. Its nearest paths give the same values by other names: the warning state (primary text, a bar in the text's ink) would add a triangle and the word "Warning", which mislabels a correction; "Graphic, essential" (Charcoal 13.29, Newsprint 13.29) fits a bar a reader needs to see the notice. So the designer's colors match on both grounds, and the name is borrowed: `border.strong` is the architecture's "Border, strong (inputs)". A later change to input edges would move the correction bar with it, the drift Rule 26.1 warns about. S7's fix would have led the designer to `--oa-color-graphic-essential`.

### 5.3 The auditor: the developer's card against chapter 19

Chapter 19's criteria list and Rule 19.7's verification matrix alone, on the third build.

| Matrix check | Could run? | Result | What the chapter left unclear |
|---|---|---|---|
| Every chapter rendered | Yes, as the page at 1440, 1024, 390, 360 and 320 px | No sideways scroll at any width; looked at by the reviewer | Written for "each chapter", so a product page has to translate it |
| Report pages | Does not apply | | |
| Keyboard and focus | Yes, script and eye | Every stop reached in order with a ring; Enter and Space as the specifications say; nothing traps focus | "Each component's keyboard path" lives in chapter 18's specifications; no target measurement for 2.5.8 |
| Reading order and headings | Yes, accessibility tree | h1, then an h2 per card; banner and main landmarks | Listening item 3 expects "the chapter, then each rule" |
| Automated rules | Yes, axe-core 4.10.2 | 0 violations, 0 incomplete in nine states | No `wcag22a` tag exists; "Many, in part" names no criteria |
| Contrast | Yes, script over rendered pairs, states included | Lowest text pair 5.49 (Newsprint) and 7.26 (Charcoal); ask label 4.17 at 19 px bold; success mark 3.37 and 3.95; error bar 2.96 on Newsprint, carried by the mark and "Error:" as the guide sets | Whether the card's decorative edge (3.10 on Charcoal) is held to 3 to 1 |
| Text at 200 percent and 320 px | Yes | Nothing clipped and no sideways scroll; the first build's mid-word breaks would have passed a clip script | How to set 200 percent; whether a broken word fails; no spacing values for 1.4.12 (run anyway with WCAG's four values: nothing lost) |
| Reduced motion | Yes | No animation or transition on the page | |
| Forced colors, light and dark | Yes | Every edge, dashed edge, bar and mark holds | |
| Dark surfaces and long labels | Dark yes; long labels no | Both themes read | "The atlas's longest variable and reform titles" do not apply to an event card |
| Print | Yes, print emulation | Words and order kept | No pass criterion beyond "keeps its words and order" |
| Downloads; diagram and chart equivalents | Do not apply | | |
| Grayscale | Yes, error state | Errors read by mark and word | Named for data and systems specimens only |
| Device script (Rule 19.9) | No: no phones or screen readers here | Item 2 would fail: no skip link | |

From the criteria list the auditor also checked 1.3.5 (autocomplete name and email: met), 2.4.2 (title present), 3.1.1 (`lang="en"`), 3.3.1 and 3.3.3 (by the keyboard script: met), 2.5.8 (targets 44 and 48 px: met, by a script the matrix does not ask for) and 2.4.1, which points to Rule 18.5's skip link: missing. Whether 4.1.3's status line is heard could not be tested without a screen reader. S10 lists what the chapter should add.

## 6. Plain language read

Chapters 17, 18, 19 and 26 read in full from the chapter JSON and the page's text, and the changed parts of chapters 01 to 11 as the brief lists them.

- **Chapter 02's patterns, by script over the four chapters' 1,697 text strings (24,543 words, token names set aside):** em dashes 0; en dashes 0; filler intensifiers 0; corporate verbs 0; hedges 0; corrective-negation shapes 0; studio codes 0; numeric dates 0; one exclamation mark, inside Rule 18.20's failure example ("Updated!"), where it belongs.
- **By hand:** the voice holds across all four chapters, with the actor first and examples drawn from civic life: bills, hearings and sign-ups. Chapter 17's openings define motion, state and the vestibular sense. Chapter 26 teaches its five steps with worked examples a newcomer can follow.
- **Sentence length:** medians of 20 words (17 and 18), 16 (19) and 13 (26). The longest real sentence is Rule 26.2's 74-word list (S12).
- **Terms defined at first use:** token, design token, tier, primitive, semantic token, component token, short name, surface class, theme, forced colors, keyline, working red, typed chip, OKLab, vestibular, accessible description and status line are defined where a reader meets them. Accessible name, landmark, APG, ARIA, level A and AA, and success criterion are not (S8). "Short name" also means a reform's shorter title in chapter 10's specimens, a collision worth watching but not a fault.
- **Changed parts of 01 to 11:** Rules 03.4, 03.6, 05.3's corrective, 05.4 (where forced colors is first defined), 08.1, 09.1, 09.3, 10.4, 10.6 and 11.12's search all read plainly and match their demonstrations. Faults are in Rule 03.2's builders text, Rule 10.9's script path and Rule 11.12's Escape line (S12, S13). Rule 08.2's dark-card feed test is the creative director's to judge (D2-1331).

## 7. Tested

All on November 11, 2026, in Playwright's Chromium, with the files opened from disk.

- The frozen page loaded at 1440 px; the visible text of all 16 chapters extracted by script; chapters 18 and 26 read as a builder, chapters 17 and 19 in full.
- The live Rule 18.17 form on the frozen page sent with good values: its button kept "Remind me" while sending.
- The event card, version 1 and version 3: light; dark by `data-oa-theme="dark"`; dark by the device setting; the stored choice applied on reload.
- Keyboard path by script: Tab order, focus ring color and offset at every stop on both grounds, Enter and Space on the full card's button, empty and wrong sends, focus to the first field to fix, the ask stepping down and back, the "Sending" state, the success line, arrow keys on the theme switch.
- Accessible names, descriptions and states from Chromium's accessibility tree, before and after an empty send.
- axe-core 4.10.2 with `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa` and best practices: nine runs (three themes, each at load, with errors and after a send), 0 violations, 0 incomplete.
- Forced colors, light and dark palettes, at load, with errors, sending and done.
- Widths 1440, 1024, 390, 360 and 320 px, and 640 px at 2x as browser zoom at 200 percent; text at 200 percent (root size doubled) at 1024 and 390 px; WCAG's four text-spacing values at 1024 and 390 px; reduced motion; print emulation; grayscale.
- The fonts: Inter at 400, 600 and 700 and Inter Tight at 800 loaded from Rule 26.5's link (`document.fonts`).
- Every color a token: a script over the CSS found no color literal outside the forced-colors blocks except `transparent`, `fill: none` and `currentColor`; all 50 properties read exist in tokens.css; every color computed on a visible element is one of the ten palette and derived colors.
- Contrast of every rendered pair on the card in both themes, states included, by the WCAG formula.
- The designer's notice, rendered in both themes and both forced-colors palettes, with its colors measured.
- Chapter 18's closing token block in place of tokens.css, with Rule 18.17's code as printed: computed type, padding, borders and heights compared with the tokens.css route.
- Which properties each closing block (17, 18, 26) defines against every `var()` its chapter's code reads, by script over the page's text and its HTML source.
- Each chapter's text searched for any warning that a surface class pins its ground.

## 8. Not tested

- Any real person: the panel is simulated.
- Screen readers, real phones, Safari, Firefox and Windows contrast themes; whether the status line is heard (4.1.3).
- The device script of Rule 19.9.
- The card without network access, where the fonts link cannot load.
- The copy promise for chapter 18's other 23 sets and chapter 26's examples (the craft team's lens).
- Chapter 19's 55 criteria against W3C's words, browser support lines and token figures (the brand and evidence lens).
- Rule 08.2's feed-test method (the creative director's lens).

## 9. Change log

Created:
- `work/handoffs/phase-2/20261111_Stage-C-Round-2-Red-Team-Plain-Production.md` (this report)
- `work/handoffs/phase-2/stage-c-round-2/production-test/event-card.html`
- `work/handoffs/phase-2/stage-c-round-2/production-test/event-card.css`
- `work/handoffs/phase-2/stage-c-round-2/production-test/event-card.js`
- `work/handoffs/phase-2/stage-c-round-2/production-test/20261111_Developer-Step-Log.md`
- `work/handoffs/phase-2/stage-c-round-2/production-test/correction-notice.css`

Modified: none. Scratch files, screenshots and test scripts sit in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2/plain-production/`.
