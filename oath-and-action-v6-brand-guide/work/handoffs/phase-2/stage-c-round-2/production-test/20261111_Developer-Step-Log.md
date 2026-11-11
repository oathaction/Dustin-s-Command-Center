# Developer step log: an event sign-up card from chapters 18 and 26

Production test, stage C round 2, November 11, 2026 (DR-219). Simulated and untested with real people: one reviewer played a front-end developer who has never seen the guide before. The developer read only the frozen chapters page (chapters 18 and 26: their words, their code panels as the page prints them, and the token table) and `work/build/tokens/tokens.css`. The developer read no code set file, no maker's note and no other studio file while building.

The task, from the round 2 brief: an event sign-up card in plain HTML, CSS and a short script, with the event's date and place, the seats left, a name and email form, a full state whose button cannot be pressed and says why, and a confirmation message; then dark mode as the guide says. The event is invented and labeled Illustrative beside it.

How the developer read the page: the four chapters' visible text, taken from the rendered page at 1440 px (`innerText` of `#components` and `#tokens`), which holds every code panel as the page shows it. Screens of the live stages were looked at where a word was unclear.

## Steps

### 1. Find where to start (chapter 18's opening, then chapter 26's opening)

- Looked at: chapter 18's lede and rule index; chapter 26's lede and rule index.
- Learned: every code set "reads only tokens.css" and "one copy follows either theme". Chapter 26 says to start a page from tokens.css (Rule 26.5) and to follow light or dark through one attribute (Rule 26.6).
- Stuck: nowhere yet. The two indexes are clear, and each rule's title says what it does.

### 2. Find the parts the card needs in chapter 18's index

- Looked at: the rule index. Picked Rule 18.1 (button, unavailable with its reason), Rule 18.17 (form fields, errors, success line), Rule 18.18 (messages and status lines), Rule 18.4 (theme switch) and Rule 18.19 (loading words, in case the seat count loads).
- Stuck: the index has no "card" and no "event". Chapter 18 has no container component, so the card's own box, heading and fact list are mine to invent.
- Guess 1: the card is a plain block on the page's ground with a hairline edge, since chapter 26 Rule 26.6's illustrative card ("Water rate hearing") shows that look and no rule names a card.

### 3. Read Rule 18.1 for the full state

- Looked at: Rule 18.1's words, its anatomy plate, its HTML and CSS panels, its specification and its For builders line.
- Learned: an unavailable button keeps its place and focus, takes `aria-disabled="true"` and `aria-describedby` pointing at a reason line, and draws a dashed edge.
- Stuck (a): the For builders line says "with the script stopping its press", but Rule 18.1 prints no script. I wrote my own: return early from the submit handler when `aria-disabled` is true. Rule 18.17's script does the same, which I found later.
- Stuck (b): the TOKENS box lists `--oa-color-action-primary-fill`, `--oa-color-action-ask-fill` and `--oa-color-state-disabled-text`, while the CSS panel uses `--oa-component-button-primary-fill`, `--oa-component-button-ask-fill` and `--oa-component-button-disabled-label`. Two names for one job on one rule. I followed the CSS, since chapter 26 Rule 26.3 says a component token wins.
- Stuck (c): Rule 18.1 says the ask "appears only where Rule 05.3 gives the view its working red". Chapter 05 is not in my two chapters. I could not tell whether my sign-up button may be red.
- Guess 2: the sign-up button is the ask (Pillar Red), because Rule 18.17's own sign-up form uses the ask and `data-red-job="take part now"`, and signing up is the one way to take part on this card.
- Guess 3: `data-red="working"` and `data-red-job="..."` do nothing in the CSS or script I copied. I kept them as markers, since the guide's code carries them, without knowing who reads them.

### 4. Read Rule 18.17 for the form

- Looked at: Rule 18.17's words, anatomy plate, failure plate, HTML, CSS and script panels, specification and For builders line.
- Learned: visible labels, `autocomplete`, errors joined by `aria-describedby`, `aria-invalid`, focus to the first field to fix, the ask stepping down while an error holds the red, and a status line with the success mark after a good send.
- Stuck (a): Rule 18.1 says "While a send runs, its word reads 'Sending'", and Rule 18.17's specification says "Sending: the button reads 'Sending'". The script I copied never changes the button's word; it writes "Sending your request." to the status line and leaves the button reading "Remind me". I followed the rule and added two lines that swap the word and put it back.
- Stuck (b): Rule 18.17 says "A field stays open to typing at all times". It is written for a form that cannot send yet. A full event can never send. Nothing in either chapter says whether a full card keeps its fields.
- Guess 4: the full card drops its fields and keeps the button in place with its reason, so nobody types a name and email that cannot go anywhere.
- Stuck (c): the form's title is a `<p>` in the code. My card needs a heading for its event, so I used an `<h2>` with the same type token (`--oa-type-h4`). Guess 5.
- Stuck (d): the code's email check uses one pattern; there is no name check. Guess 6: a name passes when it holds at least one letter or digit after trimming.

### 5. Read Rule 18.18 for the confirmation

- Looked at: Rule 18.18's words, HTML and CSS panels, specification and For builders line.
- Learned: a message a script writes goes in a status line that sits empty in the page at load; a success starts with what happened, in bold, beside the Verdigris mark.
- Stuck: nowhere. The For builders line ("Put the status line in the page, empty, when it loads") answered the one question I had.

### 6. Start the page (Rule 26.5)

- Looked at: Rule 26.5's words, its head panel and specification, and its For builders fonts link.
- Learned: the color scheme meta tag, the fonts link, tokens.css, then my own styles, and the body rule `body { margin: 0; font: var(--oa-type-body) }`.
- Stuck: Rule 26.5's head panel shows no head script, while Rules 18.4 and 26.6 put a head script "before the stylesheets". I put the head script first, then the meta tag, the fonts and tokens.css. Guess 7.

### 7. Choose the card's tokens (Rule 26.3, five steps)

- Looked at: Rule 26.3's words, its worked example and failure, its specification and its For builders line; Rule 26.4's four examples; the token table in Rule 26.7, searched for "surface", "field", "success", "error" and "button".
- Learned: surface, role, emphasis, state, then a component token, which wins. "In CSS the first step is a class." The For builders line says "Write the role's short name in your CSS and the surface class in your HTML." The chapter's For builders block says "Set a page's ground with a surface class, as in `<body class="oa-surface-newsprint">`".
- Did: put `class="oa-surface-newsprint"` on each card, since the card sits on Newsprint, and wrote every color in the CSS as a short name.

### 8. Add dark mode (Rules 26.6 and 18.4)

- Looked at: Rule 26.6's words, plates and specification; Rule 18.4's words, HTML, CSS, script and head script panels, specification and For builders lines.
- Learned: with no attribute the page follows the device; `data-oa-theme="dark"` on the root wins; the switch is three radio buttons, Light, Dark and Match my device, and its script stores the choice under `oa-theme`.
- Did: copied Rule 18.4's switch into a header above the cards, without `data-oa-theme-for`, as the HTML comment says to do in a product, and copied its head script into the head.

(Steps 9 onward follow below as the build is tested.)

### 9. First test of dark mode: the cards stayed light

- Did: set `data-oa-theme="dark"` on the root, then, separately, asked for dark through the device setting (Playwright `colorScheme: 'dark'`).
- Saw: the page turned Charcoal, and both cards stayed Newsprint with Charcoal words (computed card ground `rgb(220, 217, 210)` in both dark runs). Screens: version 1 kept in the scratch folder as `event-card-v1.html`.
- Why: step 7 put `.oa-surface-newsprint` on each card, as Rule 26.3's For builders line ("the surface class in your HTML") and the chapter's For builders block ("as in `<body class="oa-surface-newsprint">`") told me to. A surface class pins its own surface in both themes.
- Where I found the answer: not on the page. The theme comment inside tokens.css says "A surface class keeps its own surface in either theme, so a product that follows the theme puts no surface class on its body." On the page, only Rule 26.4's second and fourth examples hint at it ("so the button draws on White in both themes"). Rule 26.6, the rule a builder reads for dark mode, never says to leave the surface class off.
- Had to guess: whether a surface class belongs anywhere on a themed product. Guess 8: put none on a block that should follow the theme, and use a surface class only for a block that must keep one ground, as Rule 26.4's White and Prussian examples do.

### 10. Second build: no surface class

- Did: removed the class from both cards. The cards now read `--oa-color-surface` and the other short names from the root's theme.
- Saw: light on Newsprint, dark on Charcoal, with fields on White and on Prussian, in both the attribute run and the device run.

### 11. Tests the reviewer ran on the second build

Run with Playwright's Chromium and axe-core 4.10.2 from `work/build/node_modules/axe-core`, on the file opened from disk. Results in the report's Tested list.

- Keyboard: Tab goes Theme (the checked radio), the full card's "Save my seat", Name, Email, the open card's "Save my seat", then off the page. Every stop shows the 2 px Verdigris ring at a 2 px gap on Newsprint and the Newsprint ring on Charcoal. Enter and Space on the full card's button do nothing, and focus stays on it. Sending with both fields empty moves focus to Name, which reads "Error: Enter your name..." as its description; sending with a bad email moves focus to Email. The ask steps down to the primary look while an error shows and turns red again once both are fixed. A good send shows "Sending" on the button with `aria-disabled`, then the success line, and the seat count drops from 8 to 7. Arrow keys on the theme switch change the theme at once and store it; a reload keeps it.
- axe-core (WCAG 2.0, 2.1 and 2.2 A and AA, and best practices): 0 violations and 0 incomplete in nine runs: light, dark by attribute and dark by device, each at load, with both errors showing and after a good send.
- Forced colors (`forcedColors: 'active'`): every edge, the dashed unavailable edge, the 4 px error bars and both marks hold; nothing relies on a fill.
- Widths: 390, 360 and 320 px with no sideways scroll; the ask 48 px tall, fields 48 px, theme choices 44 px.
- Text at 200 percent (root font size doubled, since every type token is in rem), at 1024 and 390 px: no sideways scroll and no clipped box. The first run broke words mid-word in the facts list at 390 px ("Marc h", "Alde r"); see step 12.
- Every color a token: a script found no hex, rgb, hsl or named color in the CSS outside the forced-colors blocks, other than `transparent`, `fill: none` and `stroke: currentColor`, which the guide's own code uses. All 50 custom properties the CSS reads exist in tokens.css. Every color Chromium computed on a visible element is one of the ten palette and derived colors.

### 12. Third build: my own faults found by the tests

- The facts list used a fixed `5rem` label column with `overflow-wrap: anywhere`, copied in spirit from Rule 26.4's chart rows and the guide's code sets. With text at 200 percent on a phone it broke words in the middle. Changed to a wrapping row whose value drops under its label when there is no room, with `overflow-wrap: break-word`. This was my fault; the guide offers no label-and-value pattern, so I had borrowed one meant for short chart labels.
- "6 p.m." could split across lines; I joined the number and "p.m." with a no-break space.

### 13. What I could not settle from the page

- Whether a person who has signed up should be stopped from pressing "Save my seat" again. My card lets a second press take a second seat. The guide is silent, and this one is my fault to own.
- Both buttons are named "Save my seat". A screen reader user who lists the buttons hears the same name twice, told apart only by the card around each. Rule 18.1 says nothing about repeated buttons; I left it, and it is mine to fix (for example "Save my seat on March 18").
- What `data-red` and `data-red-job` do. I kept them because the guide's code carries them.

## Every place I looked

Chapter 18: the lede and index; Rules 18.1, 18.2 (to compare the unavailable chip), 18.3 and 18.4 in full; Rules 18.17, 18.18 and 18.19 in full; the chapter's token table, Related chapters and For builders block. Chapter 26: the lede and index; Rules 26.1 to 26.8 in full; the token table, searched for surface, field, success, error, warning, button, disabled and bar; the chapter's token table and For builders block. tokens.css: the header comment, the theme blocks and comments, the Newsprint surface class, and a search for each token the code sets read.

## Every guess

1. The card is a plain block with a hairline edge (no card component exists).
2. The sign-up button is the ask, in Pillar Red.
3. `data-red` and `data-red-job` are markers to keep.
4. The full card drops its fields and keeps the button with its reason.
5. The card's title is an `<h2>` in the form title's type style.
6. A name passes when it holds a letter or digit.
7. The head script goes first in the head, before the meta tag and the stylesheets.
8. A block that should follow the theme carries no surface class (found only in a tokens.css comment).

## Two routes the developer did not take, tested afterward by the reviewer

- **The chapter's own token block in place of tokens.css.** Chapter 18's For builders section offers it as an equal choice ("Link it before your own styles, or copy this chapter's block ... so it also works on its own"). The reviewer pasted that block, as the page prints it, with Rule 18.17's HTML, CSS and script, as the page prints them, into a blank page. The form drew in Times New Roman at 16 px, with no field edges, no padding and fields about 18 px tall, because the block defines none of `--oa-type-body`, `--oa-type-ui`, `--oa-space-*`, `--oa-border-width-hairline`, `--oa-font-weight-*` and 32 more properties the chapter's code reads. Linked to tokens.css, the same files drew correctly.
- **The surface class on the body.** The chapter's For builders block says "Set a page's ground with a surface class, as in `<body class="oa-surface-newsprint">`". Step 9 shows what that does to dark mode on a block; on the body it pins the whole page to Newsprint.

## Files

- `event-card.html`, `event-card.css`, `event-card.js`: the third build, the one tested.
- `correction-notice.css`: the simulated designer's notice, from chapter 26's five steps.
- Version 1, with the surface classes, is kept outside the project at the reviewer's scratch folder as `event-card-v1.html`.
