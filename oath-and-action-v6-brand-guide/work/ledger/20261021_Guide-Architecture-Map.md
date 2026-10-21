# Guide architecture map, Edition 06

Proposal for Gate 1. Written October 21, 2026 by the UX and accessibility lead (`oa-ux-accessibility-lead`). The phase prompt pairs this step with the creative director, who has not reviewed it yet; the main session should route it to that review before Gate 1.

Status: proposal. Nothing in V5, the masters or `work/build/` changes because of this file.

The navigation model, the chapter template applied to 05 Color, the interaction model and the check results are on the board `work/boards/20261021_Navigation-And-Template-Wireframes.html`.

Read for this map: Master Brief V2 sections 1 to 3, 7, 8, 10 to 22; the Phase 1 prompt; the Gate 0 report; the decision log (DC-01 to DC-10); the Phase 0 UX audit and its data; the V5 Polished inventory and chapter text in `work/extract/v5-polished/`; all twenty V4.2 sections in `work/extract/v4-2/chapters-text/`; reference slides 24, 27, 45, 47 and 52 in `work/extract/references/pics-i-like/`.

Terms used here. A *part* is a group of chapters. An *anchor* is the name after `#` in a link, which takes a reader to one place on the page. A *landmark* is a page region that screen readers list, such as the banner, a navigation block or the main text. *Front matter* is everything before chapter 01.

## 1. What this map decides

1. The V6 contents: front matter, six parts, 28 numbered chapters and an unnumbered closing (section 2).
2. Each change to the starting map in Master Brief V2 section 7, with its reason (section 3).
3. Numbering, anchors and rule IDs (section 4) and the heading rule (section 5).
4. A home for every unit of every V5 Polished chapter (section 6) and every V4.2 chapter (section 7), with the action taken on it.
5. What the new chapters hold and where their material comes from (section 8), what retires and where its record lives (section 9), and which chapters cross-reference each other (section 10).

Action words in the tables:

| Action | Meaning |
|---|---|
| Keep | Stays in the chapter with the same subject. Its number may change. |
| Move | Goes whole to another chapter. The old chapter keeps a cross-reference where readers would look for it. |
| Merge | Joins a duplicate elsewhere. One home holds it; the other links to it. |
| Split | Divides between chapters, each part named in the row. |
| Rebuild | Keeps its substance and gets a new specimen, values or wording, to fix a defect found at Gate 0. |
| Recover | V4.2 material that V5 dropped, brought back. |
| Retire | Removed from the guide. The row says what replaces it and where the record lives. |

## 2. Proposed contents

Front matter, unnumbered: Cover, Contents, Where to start (three routes in, for a newcomer, a designer and a builder).

The instruction lines are drafts for the editor. Each one sits under its chapter's h2 (section 5).

| No. | Chapter | Part | Instruction line (draft) | Main sources | Built in |
|---|---|---|---|---|---|
| 01 | Purpose | Foundations | Learn what Oath & Action does and how the four pillars lead a reader from a question to a next step. | V5 01; V4.2 01 | Phase 2 |
| 02 | Voice | Foundations | Write copy that sounds like Oath & Action, with the locked lines quoted exactly. | V5 02; V4.2 02, 18 | Phase 2 |
| 03 | Identity | Foundations | Pick the right lockup for the surface and give the wordmark its clear space. | V5 03; V4.2 03, 05 | Phase 2 |
| 04 | The Ampersand and the hinge | Foundations | Use the ampersand to join a promise to an action, once per composition. | V5 04; V4.2 04 | Phase 2 |
| 05 | Color | Foundations | Choose a surface first, then the text and graphic colors that pass on it. | V5 05; V4.2 10, 18 | Phase 2 |
| 06 | Type | Foundations | Set every word at a readable size with the three faces and the type scale. | V5 06; V4.2 11 | Phase 2 |
| 07 | Layout and spacing | Foundations | Build pages on the column grid and spacing scale so the measure stays comfortable at every width. | New; V5 06 craft | Phase 2 |
| 08 | The Signal Grid | Foundations | Place the lockmark in its sanctioned spots, and code content with it only where a key beside it lets a reader decode it. | V5 07 | Phase 2 |
| 09 | Pillar marks | Symbols and graphics | Mark which pillar a piece serves, always in the order Explain, Track, Connect, Act. | V5 08 | Phase 2 |
| 10 | Topic and atlas symbols | Symbols and graphics | Find the symbol for a subject or an atlas element and set it with its label. | V5 09; V4.2 07, 08 | Phase 2 |
| 11 | Status and utility icons | Symbols and graphics | Show a record's state or an interface action with a glyph that never stands in for a topic. | New; V5 09; V4.2 08 | Phase 2 |
| 12 | Graphic devices and patterns | Symbols and graphics | Add dividers, frames, markers and watermarks only where they help someone read. | New; V5 03, 05; V4.2 06, 09 | Phase 2 |
| 13 | Evidence and sourcing | Evidence and media | Say what kind of evidence a claim rests on, and put its source and any illustrative label beside it. | New; V5 11, 15; V4.2 12, 14 | Phase 3 |
| 14 | Data visualization | Evidence and media | Start from the reader's question to choose a chart, then title it with the evidence it shows. | V5 11 | Phase 3 |
| 15 | Systems graphics | Evidence and media | Draw causes, loops and authority from Atlas V7 so a reader can follow one link at a time. | V5 16; V4.2 09 | Phase 3 |
| 16 | Photography, illustration and video | Evidence and media | Show public life as it happens, and label every placeholder and generated image for what it is. | V5 10; V4.2 16 | Phase 4 |
| 17 | Motion and states | Behavior | Keep motion under the reader's control, and give every state a word or a shape as well as a color. | V5 12; V5 07 states | Phase 2 |
| 18 | Components and interaction | Behavior | Build controls that work by keyboard and screen reader, with a status line for every change. | New; V5 07, 09, 14 controls | Phase 2 |
| 19 | Accessibility | Behavior | Check a page against WCAG 2.2 AA before you call it finished. | New; V5 15; V4.2 17 | Phase 2 rules, Phase 5 results |
| 20 | Web | Applications | Assemble the website mastheads, navigation, article pages, trackers and footer from the system. | V5 13; V4.2 12, 13 | Phase 4 |
| 21 | The atlas | Applications | Apply the system to the atlas, its hardest test, with typed IDs and the evidence one step away. | V5 16; Atlas V7; Concepts V2 | Phase 4 |
| 22 | Newsletter and email | Applications | Build an email that reads well with images off and web fonts unavailable. | V5 13; V4.2 05, 13 | Phase 4 |
| 23 | Social and video | Applications | Size posts, covers and video frames to each platform's safe areas, with captions clear of the interface. | V5 13; V4.2 15 | Phase 4 |
| 24 | Reports | Applications | Lay out a report page by page, from the cover to the source notes. | V5 14; V4.2 14 | Phase 4 |
| 25 | Print and presentation | Applications | Produce one-pagers, letterhead, slides, event signs and merchandise at their print sizes. | V5 13, 08 | Phase 4 |
| 26 | Tokens and how to choose them | Production | Pick a token by surface, then role, then state. | New; V5 15 | Phase 2 |
| 27 | Assets and downloads | Production | Download a master with a dated name and see which chapter governs it. | New; V5 15 asset index | Phase 5 |
| 28 | Standards checklist | Production | Run the checklist before anything is called final. | V5 15; V4.2 17, 18 | Phase 5 |
| | Closing | Production | Colophon, edition notes and the way back to the start. | V5 17; V4.2 18, 19 | Phase 5 |

Phase consequences. The Phase 2 prompt lists "Layout and the Signal Grid" as one chapter; this map makes it two (07 and 08). The Phase 4 prompt lists "Web and atlas", "Social", "Video frames" and "Atlas system test"; this map makes them 20, 21 and 23. No prompt names 19 Accessibility, 27 Assets and downloads, 28 Standards checklist or the Closing. The Gate 1 report should place them in the Phase 2 proposal and carry the rest forward.

## 3. Changes to the starting map in Master Brief V2 section 7

| # | Change | Reason |
|---|---|---|
| 1 | "Layout, spacing and the Signal Grid" becomes 07 Layout and spacing and 08 The Signal Grid. | V5's Grid chapter is the largest in the guide (110,055 characters, 63 figures, a composer and a tracker). Tension 4 adds precedence rules, valid combinations and a decoding key. A layout chapter inside it would be hard to find. The V5 name "The Grid" also misleads: the Phase 0 UX audit called it "a layout chapter", and it is the Signal Grid. |
| 2 | Evidence and sourcing moves to the front of its part, ahead of Data visualization. | Data visualization and Systems graphics take their title types, grade words and illustrative labels from it (brief section 15). Read first, it lets their cross-references point back to something the reader has seen. |
| 3 | 19 Accessibility joins the Behavior part. | Brief section 22 sets a verification matrix and V5's Standards chapter holds an accessibility table, but no chapter in the starting map owns either. Keyboard, focus, motion and status rules describe how the guide behaves, so they sit beside Motion and states and Components and interaction. 28 Standards checklist links to it. |
| 4 | "Web and atlas" becomes 20 Web and 21 The atlas. "Atlas system test" folds into 21, and its pass or fail lines go into 28. | The brief calls the atlas the hardest application and the main test of the system. It has its own home, detail and evidence views, typed ID chips and stepped loops, drawn from Concepts 03, 09, 10 and 11. A chapter of its own makes it findable from the contents. A separate "test" chapter would repeat 21's specimens. |
| 5 | "Social" and "Video frames" merge into 23 Social and video. | V5 already keeps the video thumbnail and the vertical cover with social. TikTok covers (DC-07), vertical video and title and end frames share safe areas and caption zones, so one chapter draws each overlay once. Video rules for structure, captions and transcripts stay in 16. |
| 6 | Closing becomes an unnumbered end section with the colophon and edition notes. Front matter adds "Where to start". | V5 left the closing unnumbered. "Where to start" gives a newcomer, a designer and a builder each a route in, the way Atlas V7 and the atlas home pages Dustin saved (slides 24 and 52) start from a question (Gate 0 opportunity 6, brief outcome 1). |
| 7 | Encoding glyphs (polarity signs, link types, delay marks, evidence grades, loop types, closure, intervention markers) are drawn on the symbol grid in 10 and defined and taught in 15. Status marks for tracker and record states live in 11. | A glyph's meaning belongs with the grammar that uses it. Its construction belongs with the other symbol masters, so one set of grids and pixel-fit rules covers all of them. 27 lists every file. |
| 8 | Merchandise, the event kit and letterhead go to 25 Print and presentation. The email signature goes to 22. | V5's In Use chapter holds them, brief section 18 omits merchandise, and `pics_i_like.pdf` shows merchandise Dustin likes. Moving them keeps them in the guide until Dustin decides otherwise. |
| 9 | Chapter names drop V5's slogans. "Topic Icons" becomes "Topic and atlas symbols"; "Systems maps" becomes "Systems graphics"; "In Use" splits across the six application chapters. | Phase 0 found slogan headings and misleading groups (finding 9 and 10). The brief's names say what each chapter covers. |

## 4. Numbering, anchors and rule IDs

**Chapters.** One continuous series, 01 to 28, always two digits. A reader can cite "chapter 14" without naming a part. Front matter and the Closing carry no number.

**Parts.** Named and unnumbered: Foundations, Symbols and graphics, Evidence and media, Behavior, Applications, Production. A second number series would collide with chapter numbers in speech ("part 2" next to "chapter 2").

**Anchors.** Each chapter's anchor is a word: `#color`, `#signal-grid`. A later renumbering then breaks no link.

| No. | Anchor | | No. | Anchor |
|---|---|---|---|---|
| 01 | `#purpose` | | 15 | `#systems-graphics` |
| 02 | `#voice` | | 16 | `#photography` |
| 03 | `#identity` | | 17 | `#motion-and-states` |
| 04 | `#ampersand` | | 18 | `#components` |
| 05 | `#color` | | 19 | `#accessibility` |
| 06 | `#type` | | 20 | `#web` |
| 07 | `#layout` | | 21 | `#atlas` |
| 08 | `#signal-grid` | | 22 | `#newsletter-and-email` |
| 09 | `#pillar-marks` | | 23 | `#social-and-video` |
| 10 | `#symbols` | | 24 | `#reports` |
| 11 | `#icons` | | 25 | `#print` |
| 12 | `#graphic-devices` | | 26 | `#tokens` |
| 13 | `#evidence` | | 27 | `#assets` |
| 14 | `#data-visualization` | | 28 | `#standards` |

Front matter: `#top`, `#contents`, `#start`. Parts: `#part-foundations`, `#part-symbols`, `#part-evidence`, `#part-behavior`, `#part-applications`, `#part-production`. End: `#closing`.

**V5 anchors kept as aliases**, so links written for Edition 05 still land: `#grid` lands on `#signal-grid`, `#topic-icons` on `#symbols`, `#data` on `#data-visualization`, `#motion` on `#motion-and-states`, `#in-use` on `#part-applications`, and `#atlas-system` on `#systems-graphics`. The other V5 anchors (`#purpose`, `#voice`, `#identity`, `#ampersand`, `#color`, `#type`, `#pillar-marks`, `#photography`, `#reports`, `#standards`, `#closing`) keep their names.

**Rule IDs.** A rule is cited as "Rule 05.2": chapter 05, rule 2. Its anchor is `#rule-05-2`. The form cannot collide with Atlas V7 IDs, which start with a letter (variables A1 and B4, links L01 and LE02, loops R1 and B2, reforms R-01, domains D01, drivers X1), with V4.2 symbol codes (01-01, P-01, U-01), or with report folios ("05 / Narrative page"). V6 uses no "R" prefix for its own rules, because V7 already uses R for loops and reforms (tension 7). V5's ten standards R1 to R10 each map to the home rule that carries them (section 6, V5 15), and the checklist in 28 cites those rule IDs.

Atlas IDs themselves always appear in a typed chip ("Variable B4", "Loop B4", "Reform R-01"). The systems marks board owns that design; 15 and 21 apply it.

## 5. The heading rule

| Level | Holds | Example |
|---|---|---|
| h1 | The guide's title, once, on the cover | Oath & Action Brand Guide, Edition 06 |
| h2 | A chapter's number and name, and nothing else | 05 Color |
| Beneath the h2 | The instruction line: one sentence, set as a large paragraph | Choose a surface first, then the text and graphic colors that pass on it. |
| h3 | One per rule, starting with its ID, then three fixed closers | Rule 05.2 Set text only on pairs that pass. / Specifications / Related chapters / For builders |
| Labels | Template blocks inside a rule: "Why it works", "Correct application", "Failure case" | Visible labels on paragraphs and figures |

Notes on the rule:

- Dustin's example "07 The Grid" uses V5's numbering. In V6 the same chapter reads "08 The Signal Grid".
- The tagline "A country that answers to its people." stays the cover's display line, set as text. It stops being the page's h1, so the h1 can name the document (WCAG 2.4.2 Page Titled and 2.4.6 Headings and Labels).
- Part openers carry an h2 that reads "Part Foundations", with "Part" as a small label. A part opener lists its chapters with their instruction lines.
- V5's slogan headings ("Newsprint carries the conversation.") move under the h2 as the instruction line or into a rule, after the editor's pass.
- Why labels, not headings, inside a rule: 28 chapters with several rules each would put hundreds of identical "Why it works" headings into a screen reader's heading list. A rule's h3 already names it.
- Specimens and mockups never use heading elements. Their headlines are styled text. Phase 0 counted 41 mockup headings in the outline.
- Landmarks: one banner, one navigation block for parts and one for chapters (the phone menu holds a single navigation block with both), the main text, and one contentinfo for the colophon. Chapters are sections with headings and no region names, so the landmark list stays short.

Criteria: 1.3.1 Info and Relationships, 2.4.6 Headings and Labels, 2.4.10 Section Headings (AAA, advisory).

## 6. V5 Polished, chapter by chapter

Eighteen sections: the cover, sixteen chapters and the closing. Units are V5's h3 headings, in V5's words, plus unheaded blocks named in brackets.

### V5 00 Cover (`top`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Edition line] "Brand Guide / Edition 05 / October 2026" | Cover | Rebuild | Reads Edition 06 with the issue date |
| [Tagline] "A country that answers to its people." | Cover | Keep | Locked line, exact. Display text; the h1 names the guide |
| [Lines] "Public life belongs to everyone. There should be a way in." and "A people-powered, nonpartisan publication about the rules that shape our lives." | Cover | Keep | Editor reviews |
| [Pillar line] Explain / Track / Connect / Act | Cover | Keep | Locked order |
| [Chapter list in the hero] | Contents | Rebuild | One contents system feeds the contents page, the desktop rail and the phone menu |

### V5 01 Purpose (`purpose`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Opener] "People belong in the picture." and the open-door line | 01 | Keep | Slogan moves under the h2 or into Rule 01.1 |
| [Mission and about text] | 01 | Keep | Mission quoted exactly |
| The hinge. | 01 and 04 | Split | 01 states the idea (DC-05); 04 owns the drawing, the headlines and their rules |
| Four pillars, always in this order. (Explain, Track, Connect, Act, with their products) | 01 | Keep | The product list grows into the brand architecture from the strategy board |
| [Four-dot row note] | 08 | Move | 01 keeps a cross-reference |

### V5 02 Voice (`voice`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Locked lines table] | 02 | Keep | The voice line sits beside any revision until Dustin approves one (DC-04) |
| Supporting lines. | 02 | Keep | The candidate lines "From spectators to stewards." and "Democracy has a structure." join only if approved at Gate 1. See V4.2 18 below for the history of the first |
| How we sound. | 02 and 13 | Split | "Sourced" moves to 13. "Nonpartisan" grows into the written rule set. "One next step" links to the Act pattern in 13 (DC-01) |
| [We publish the mechanism / Not the mood table] | 02 | Keep | Protected at Gate 0. The "23 states" example needs a source or a label (tension 17) |
| Vocabulary. | 02 | Keep | Series routes move to 08 |
| The hinge headline. | 04 | Merge | Joins V5 04 "Hinge headlines at three scales." 02 keeps the copy rule and links to 04 |

### V5 03 Identity (`identity`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Opener, L1 and construction table] | 03 | Keep | Values follow the Gate 1 identity decisions |
| Clear space. | 03 | Keep | |
| Minimum sizes, at true size. | 03 | Rebuild | One set of minimums with no conflicts (Gate 0 Phase 1 proposal) |
| Eight lockups. | 03 | Keep | Gains the masthead family recovered from V4.2 05 |
| Four surfaces and mono. | 03 | Keep | Red on Prussian goes to Gate 1 |
| Quiet signatures. | 12 | Move | Watermarks are a device with opacity rules |
| The decision behind the service. | 12 | Move | A watermark specimen's mockup heading. Becomes styled text |
| Follow the public record. | 12 | Move | As above |
| Color matrix. | 03, files in 27 | Keep | Each cell gets a download |
| Misuse. | 03 | Keep | Becomes the chapter's failure cases |

### V5 04 The Ampersand (`ampersand`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Master and construction table] | 04 | Rebuild | Starts from the Phase 0 finding that the glyph is unmodified Lora Bold |
| Container marks. | 04 | Keep | Platform avatars are shown in 23 |
| The hinge diagram. | 04 | Keep | |
| Hinge headlines at three scales. | 04 | Merge | With V5 02 "The hinge headline." |
| Editorial crop. | 04 | Keep | |
| Hinge divider. | 04 | Keep | Listed in the device index in 12 |
| Seal and emboss. | 04 | Keep | Print production notes in 25 |
| Partnership lockup. | 03 | Move | Lockups live together. The invented partner name is labeled or replaced (Q-01) |
| Hinge motion. | 17 | Move | Every reader-controlled motion sits in one chapter with the same controls. 04 shows the still frame |
| Misuse. | 04 | Keep | |

### V5 05 Color (`color`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Palette with shares and jobs] | 05 | Keep | |
| ["There are no tints."] | 05 and 26 | Retire | Replaced by bounded tints with tokens and named jobs (tension 3) |
| [Watermark opacities] | 12 | Move | |
| Proportion. | 05 | Keep | Rule 05.1 on the board's wireframe |
| [Red discipline, red against blue, red against green, deltas] | 05 and 14 | Split | Deltas move to 14 |
| [Stone hairline dividers] | 12 | Move | 05 keeps the hairline's color |
| Contrast, measured. | 05 | Rebuild | Text-safe and graphic-safe roles for each color on each surface (tension 9) |
| The keyline rule. | 05 | Keep | |
| Four surfaces. | 05 | Keep | |

### V5 06 Type (`type`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Three faces] | 06 | Keep | |
| The scale. | 06 | Rebuild | 13 px floor and rem units (tension 1; Phase 0 finding 7) |
| Craft. (tabular figures, balanced headings, hanging punctuation, ligatures and figures) | 06 | Keep | Adds the true minus sign |
| [Craft 4, measure] | 06 and 07 | Split | 06 owns characters per line; 07 owns the column widths that deliver it |
| [Craft 5, the 8 px rhythm] | 07 | Move | |
| [CSS settings block] | 06 | Keep | Moves into "For builders" |
| Email is the one exception. | 06, applied in 22 | Keep | |
| [Never substitute list] | 06 | Keep | |

### V5 07 The Grid (`grid`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| Geometry. | 08 | Keep | |
| States. | 08, behavior in 17 | Rebuild | Loading replaced (tension 2). Active and Ready get distinct shapes |
| Positions and sizes. | 08 | Keep | 14 cites the legend position |
| The same geometry, used to code content. (rules A to F) | 08 | Rebuild | Precedence, valid combinations and a key beside each use (tension 4). Rules A to F become Rule 08.n |
| A bill tracker in nine stages. | 08, 15 and 18 | Split | 08 keeps the progress encoding, 15 the workflows for every route (tension 12), 18 the tracker component |
| Six series, six routes. | 08 | Keep | |
| The kicker lockup. | 08 | Merge | Appears twice in V5; one definition in V6 |
| In context. | 08, 14, 20, 22, 23, 24 | Split | 08 keeps one example. The article kicker, tracker card, newsletter header, social corner, chart legend and report kicker move to their applications |
| Composer. | 08 | Rebuild | Demo control with a status line (board, section 6) |
| Misuse. | 08 | Keep | |

### V5 08 Pillar Marks (`pillar-marks`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [The four marks with names and colors] | 09 | Rebuild | Redrawn from one skeleton per pillar (DC-02) |
| How the pillars work together. | 01 | Merge | One set of pillar descriptions, in 01 |
| Construction. | 09 | Rebuild | |
| In a circular badge. | 09 | Keep | |
| In a name lockup. | 09 | Keep | |
| In the website navigation. | 20 | Move | |
| As a section opener. | 09 | Keep | Its mockup heading "Watch the vote." becomes styled text |
| Watch the vote. | 09 | Keep | Section opener specimen |
| In the poster quartet. (Know the rules. / Watch the vote. / Find your hearing. / Make the move.) | 25 | Move | Poster headlines become styled text |

### V5 09 Topic Icons (`topic-icons`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [The twenty subjects] | 10 | Rebuild | Redrawn in the approved symbol grammar |
| Construction. | 10 | Rebuild | |
| Optical sizes. | 10 | Rebuild | Pixel-fit 16 and 24 px masters (Gate 0 tension 22) |
| The distinctness test. | 10 | Keep | Extended to the atlas symbols |
| Four surfaces. | 10 | Keep | |
| In use. | 10, 20, 23, 24 | Split | 10 keeps the Act-context accent rule; the kicker, tracker row, navigation, contents and tile examples move to their applications |
| The library. | 10, files in 27 | Merge | With the V4.2 symbol library |
| Utility glyphs. | 11 | Move | |

### V5 10 Photography (`photography`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Direction] | 16 | Keep | |
| The shot list. | 16 | Keep | Settings from more states (DC-06) |
| Avoid. | 16 | Rebuild | The generated-imagery line follows Gate 0 correction 10 |
| Two treatments. | 16 | Keep | |
| Type never sits on a busy image. | 16 | Keep | |
| Testimonials. | 13 and 23 | Split | Rules move to 13; the quote card to 23. The three invented quotes are labeled or replaced (Q-01) |

### V5 11 Data Visualization (`data`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Opener] "The chart proves the sentence." | 13 and 14 | Retire | Replaced by four title types: finding, association, estimate, illustration (tension 5) |
| [Every chart carries a claim.] | 13 and 14 | Split | 13 defines the title types; 14 shows the title anatomy |
| [Series order.] | 14 | Rebuild | Data palettes kept apart from identity color (brief section 10) |
| [Chart types.] | 14 | Rebuild | Grows into the selection guide |
| [Axes and labels.] | 14 | Rebuild | Labels rise from 12 px to the 13 px floor |
| [Status and deltas.] | 14 | Keep | |
| [The grid as a legend mark.] | 08 | Move | 14 cross-references |
| Four conventions, drawn. | 14 and 18 | Rebuild | The bar chart that contradicts its title retires (record in the change report). The tracker list moves to 18 |

### V5 12 Motion (`motion`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [The lever landing] | 17 | Keep | Reader-controlled |
| [Tracker progress] | 17 and 18 | Split | Motion in 17, the component in 18 |
| The hinge. | 17 | Merge | With V5 04 "Hinge motion." |
| Tokens. | 17, registered in 26 | Keep | |
| Three easings. | 17, registered in 26 | Keep | |
| Reduced motion. | 17, requirement in 19 | Keep | |
| Never. | 17 | Keep | |
| [Link, button and focus transitions] | 17 and 18 | Split | State behavior in 17, component specs in 18 |

### V5 13 In Use (`in-use`)

V5's In Use chapter has no h3 headings. Its units are the application specimens, named by their captions.

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Substack header] | 22 | Move | |
| [Newsletter email] | 22 | Move | |
| [Article page] | 20 | Move | |
| [Home, desktop and mobile] | 20 | Move | |
| [Tracker page] | 20, component in 18 | Move | |
| [Action page, Act / Testify] | 20 | Move | Carries the Act label pattern from 13 (DC-01) |
| [Pillar tiles, hinge headline tiles, quote cards, carousel] | 23 | Move | |
| [Video thumbnail and vertical video cover] | 23 | Move | The grievance line "Who wrote the rule you are angry about?" is rewritten (tension 16) |
| [Avatars and app icon] | 23, masters in 04 | Move | |
| [One-page explainer and event flyer] | 25 | Move | |
| [Presentation: cover, divider, hinge slide, data slide, closing] | 25 | Move | |
| [Event kit: stage banner, name badge, table sign] | 25 | Move | |
| [Merch: tee, cap, tote, sticker sheet] | 25 | Move | See section 3, change 8 |
| [Correspondence: email signature] | 22 | Move | |
| [Correspondence: letterhead] | 25 | Move | |
| [Invented bills, people, places and the single campaign] | 20 to 25 | Rebuild | Labeled beside each item or replaced, and rotated across issues and states (Q-01, DC-06) |

### V5 14 Reports (`reports`)

V5's h3 headings here are the report pages' own headlines. They become styled text inside the page specimens.

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [The twelve pages]: The decision behind the service. / Start with a question. Follow the record. / A useful question has a clear address. / Who do they answer to? / A service schedule shapes someone's day. / Every handoff belongs to someone. / 100 units. Named uses. / Fewer steps. Then check the outcome. / What remains after the bills? / Put the promise to work. / Keep the evidence within reach. / A country that answers to its people. | 24 | Rebuild | Full editorial and visual pass (brief section 19) |
| [Report reader] | 24, component in 18 | Rebuild | Keyboard model on the board, section 6 |
| Anatomy. | 24 | Keep | |
| [PDF/A export note] | 24 and 19 | Split | PDF tagging rules in 19 |

### V5 15 Standards (`standards`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| Ten rules that cover most mistakes. | 28 | Rebuild | Each standard links to its home rule and takes that rule's ID (tension 7) |
| Newsprint leads. | 05 | Merge | Rule 05.1 |
| One lever per page. | 08 | Merge | A Signal Grid rule; 05 cites it for red |
| Hairlines, not boxes. | 12 | Merge | Divider rule |
| Specify and show. | 28 | Keep | It describes the chapter template, so it opens 28 |
| Red is punctuation. | 05 | Merge | |
| The grid is a signature. | 08 | Merge | |
| Dimension everything. | 07 | Merge | Applied in every Specifications block |
| Source everything. | 13 | Merge | |
| Pillars in order. | 01 | Merge | Cited from 09 and 20 |
| Number the system. | 28 | Rebuild | Becomes the rule ID scheme in section 4 |
| Specifications. | Every chapter; summary in 28 | Split | Each chapter's Specifications block is the source. 28 carries a summary generated from the token file so it cannot drift |
| Asset index. | 27 | Move | Dated descriptive names (tension 10). Internal IDs stay in SVG `id` attributes |
| Accessibility. | 19 | Move | |
| Before anything is called final. | 28 | Rebuild | Each line cites a rule ID |
| [Colophon] | Closing | Move | |
| [Global note on illustrative content] | 13 | Retire | Replaced by labels beside each item (tension 6) |

### V5 16 Systems maps (`atlas-system`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Opener and the V7 authority note] | 15 | Keep | |
| [Relationship conventions and delays] | 15 | Rebuild | Reconciled to V7: hypotheses dotted, plausible links dashed (Gate 0 correction 4) |
| [Loop R1 example] | 15 | Rebuild | Worked example 1 (brief section 14) |
| [R16 example] | 15 | Rebuild | Discloses a hypothesized return link |
| [Reform R-28 target bracket] | 15 and 12 | Split | The marker's drawing in 12, its meaning in 15 |
| Working rules for the atlas. | 15 and 21 | Split | Grammar in 15, application specs in 21 |
| [Four embedded atlas images] | 15 | Retire | Replaced by live inline SVG in guide tokens (tension 25) |
| [Pointer to the Atlas Visual System] | 21 | Move | |

### V5 17 Closing (`closing`)

| V5 unit | V6 home | Action | Note |
|---|---|---|---|
| [Headline] "Put the promise to work." | Closing | Keep | |
| [Tagline] | Closing | Keep | Exact |
| [Edition line] | Closing | Keep | Joins the colophon |
| [Back to the beginning] | Closing | Rebuild | Becomes "Back to contents" |

## 7. V4.2, chapter by chapter

Twenty sections: the cover, eighteen chapters and the closing. V5 superseded most of V4.2. The rows name what V6 recovers.

| V4.2 section | V6 home | Action | What V6 takes |
|---|---|---|---|
| 00 Cover (`top`): "Brand field guide / HTML refinement" | Cover | Retire | The edition title is V6's own. The two cover lines already live in V5 |
| 01 Point of view (`purpose`) | 01 | Merge | Same substance as V5 01. Nothing further to recover |
| 02 Voice & character (`voice`) | 02 and 13 | Recover | The in-place status labels ("Proposed supporting line.", "Proposed editorial phrasing.") become a labeling pattern in 13 |
| 03 The signature (`identity`) | 03 | Merge | The note that canonical masters were pending is history; the Phase 1 identity work supersedes it. Edition notes keep it |
| 04 Ampersand studies (`ampersands`): freestanding, circular avatar, square avatar, compact signature "O & A", editorial crop "WITH THE PEOPLE", partnership | 04 and 03 | Recover | The avatars match V5's containers. The compact signature goes to the identity board for a ruling beside V5's L8 monogram. The partnership treatment joins 03 |
| 05 Publication furniture (`mastheads`) | 03, 20, 22 | Recover | Masthead lockups in 03 (brief section 7). The issue line ("Issue 001 / Sample edition") in 22. The section masthead with its topic tabs ("Democracy", "The economy", "Everyday life") and the series masthead ("The public record") in 20 and 22 |
| 06 Quiet signatures (`watermarks`) | 12 | Merge | Same two opacities as V5. Its rule for small headers and video corners (an opaque compact signature) stays |
| 07 The symbol language (`symbols`) | 10 | Recover | Four construction principles: "Weight with open space.", "A deliberate cut.", "People have a place.", "Meaning earns the detail." They feed the symbol grammar and its "Why it works" text |
| 08 The complete vocabulary (`library`), 124 symbols | 10, 11, 27 | Recover | The six family names as a starting taxonomy for atlas symbols (Democratic institutions 19, Economic institutions 28, Failures and risks 14, Reforms and solutions 17, Civic actions 15, Evidence and case studies 15). One meaning sentence per symbol, such as "Several inputs meet one accountable seat." The search, family, size and surface controls. The twelve interface glyphs U-01 to U-12 (menu, close, search, next, previous, download, external link, play, pause, filter, expand, collapse) go to 11. The drawings stay study material; Phase 2 redraws |
| 09 Visual explanations (`relationships`) | 15, 12, 08 | Recover | The rule "Give every handoff an owner." and "Each stage names the person or office responsible for the next step." go to 15 as the handoff diagram, with V4.2's instruction to link each handoff to the current official procedure. The frame becomes a mechanism frame in 12. "Explanatory diagrams use their own actors and labels." becomes a Signal Grid misuse in 08 |
| 10 Color (`color`) | 05 and 12 | Merge | "Keep decorative watermark opacity separate from the palette." goes to 12 |
| 11 Typography (`type`) | 06 and 13 | Recover | The caption layer ("Caption and source notes have their own clear reading layer.") |
| 12 Editorial in use (`publications`) | 20, 13, 12 | Recover | The article opening goes to 20. The source slot "[Official procedure, section, date, URL]" and the line "A proposed change describes an intention. A published outcome shows what happened." go to 13. The "Who owns the next step?" callout becomes a device in 12 |
| 13 Headers & endings (`footers`) | 22, 20, 24, 03 | Recover | Newsletter ending with "Keep exploring" pillar links in 22; site footer in 20; report header and back matter in 24; the signature strip stays L6 in 03. Placeholder slots for sender details and unsubscribe go to 22 |
| 14 The report system (`reports`) | 24 and 13 | Recover | V5's pages supersede these. V6 recovers the SAMPLE labels set beside each item and the source slots that V5 dropped (Editor audit section 6) |
| 15 Editorial series (`social`) | 23 | Recover | The series tile structure and the "Sample / Proposed editorial application" label beside each tile. The six tile headlines go to the editor as candidates |
| 16 Motion behavior (`motion`) | 17 and 16 | Recover | The reader-stepped sequence ("Show the next step"), "Each state keeps its label visible.", and the film needs (captions, transcripts, reading holds, still alternatives) |
| 17 Craft & access (`standards`) | 19, 13, 28 | Merge | Reading size, meaningful symbols, color and focus, and calm interaction go to 19. Evidence goes to 13. Brand consistency goes to 28 |
| 18 Specifications & decisions (`specifications`) | 28, 05, 02, Closing | Recover | The tables become the generated summary in 28. The color decisions go to 05. The language table goes to 02, and it records two facts for Gate 1: "The republic is not self-maintaining." as founding history, and "From spectators to stewards." as a historical tagline "Retired from current applications." The candidate-line decision should see that history. "What changed" and "Review and remaining limits" become edition notes in the Closing |
| 19 Closing (`closing`) | Closing | Retire | "Website and newsletter remain on pause." is a dated status note. The headline and tagline already live in V5's closing |

## 8. New chapters and where their material comes from

| Chapter | Holds | Sources |
|---|---|---|
| 07 Layout and spacing | Spacing scale; column grids at 1440, 1024, 768, 390 and 360 px; section rhythm; measure rules in characters; reflow at 320 px | V5 06 craft; V5 15 accessibility table; brief section 10; the spacing sheet in slides 27 and 45 (principle only) |
| 11 Status and utility icons | Status marks for tracker and record states; utility glyphs for menu, close, search, arrow, download, external link, copy, filter, sort, expand, collapse, play, pause, reset, share, print, info, warning | V5 09 utility glyphs; V4.2 U-01 to U-12; brief section 11 |
| 12 Graphic devices and patterns | Watermarks; dividers; mechanism frames; intervention markers; evidence annotations; document references and source slots; chart keys; map locators; restrained patterns | V5 03, 05, 16; V4.2 06, 09, 12; brief section 12; icon study 07 |
| 13 Evidence and sourcing | The four title types; title verbs matched to V7 grades; the source line format; illustrative labels beside each item; the Act pattern for process and position pieces (DC-01); testimonial and quote rules | Brief section 15; V5 02, 10, 11, 15; V4.2 02, 12, 14 |
| 15 Systems graphics (new as a chapter) | The grammar mapped to V7 fields; the six worked examples; configurable policy workflows; reconciliation results | V5 16; V4.2 09; brief section 14; the Phase 0 reconciliation table |
| 18 Components and interaction | Buttons, links, copy and download controls, the report reader, disclosures, tabs, tables, the tracker, the symbol library, chart and diagram controls, each with every state | V5 07, 09, 14 controls; brief sections 10, 17 and 22; this board's interaction model |
| 19 Accessibility | Requirements with WCAG 2.2 criteria; the verification matrix and its results; what was not tested | V5 15; V4.2 17; brief section 22; Phase 0 UX audit |
| 21 The atlas | Atlas home, detail, evidence view (the Register), loop pages, typed ID chips; how the atlas tests the system | V5 16; Atlas V7; Concepts 03, 09, 10, 11 and 07; slides 24 and 52 (principle only) |
| 26 Tokens and how to choose them | Token categories, names, the rule for adding a token, "How to choose a token" with four worked examples | Brief section 10; the token architecture (`work/ledger/20261021_Token-Architecture.md`, written in parallel by the engineer) |
| 27 Assets and downloads | Every file with its ID, purpose, sizes, surfaces and governing chapter; download buttons; font licenses | V5 15 asset index; brief section 20 |
| 14 Data visualization (expanded) | Selection guide by reader question; at least twenty specimens; data palettes; chart interaction | V5 11; brief section 13 |

## 9. Retired items and where their record lives

Nothing retires without a replacement or a record. Every row here also goes into the V6 change and validation report.

| Retired item | Source | Replaced by | Record |
|---|---|---|---|
| "There are no tints." | V5 05 | Bounded tints with tokens (05, 26) | Change report; tension 3 |
| The pulsing loading state | V5 07, 12 | A still state with visible text (17) | Change report; tension 2 |
| The heading "The chart proves the sentence." | V5 11 | Four title types (13) | Change report; tension 5 |
| The bar chart titled "Closed primaries are the largest group." | V5 11, 13 | A sourced specimen (14) | Change report; Gate 0 finding 1 |
| Four embedded atlas images | V5 16 | Live inline SVG (15) | Change report; tension 25 |
| The global note on illustrative content | V5 15 | Labels beside each item (13) | Change report; tension 6 |
| Testimonials presented as reader quotes | V5 10, 13, 14 | Labeled or replaced quotes (13, 23) | Change report; Q-01 |
| The grievance line "Who wrote the rule you are angry about?" | V5 13 | A rewritten cover line (23) | Change report; tension 16 |
| R-prefixed standards numbering | V5 15 | Rule NN.n (section 4) | Change report; tension 7 |
| Slogan h2 headings | V5, every chapter | Number and name h2, instruction beneath (section 5) | Change report; Phase 0 finding 9 |
| "Brand field guide / HTML refinement" title | V4.2 00 | The Edition 06 title | Edition notes |
| Master-status notes ("Typeset placeholder", masters pending) | V4.2 03, 18 | Phase 1 identity decisions | Edition notes |
| "Website and newsletter remain on pause." | V4.2 19 | Nothing; the note is out of date | Edition notes |
| The 124 V4.2 symbol drawings as shipping art | V4.2 08 | Phase 2 masters; names and meanings recovered | Rights ledger lists them as study material |

## 10. Cross-reference plan

Every chapter ends with a "Related chapters" block of two to five links. Each link shows the number and name and a short reason, so the reader knows why to go. Inline references in prose are links too (Phase 0 found none linked).

| No. | Related chapters |
|---|---|
| 01 | 02 (the lines that state the purpose), 04 (the hinge in full), 09 (the pillar marks), 21 (the atlas as the purpose at work) |
| 02 | 01, 04 (hinge headlines), 13 (sourcing and the Act label), 22 (voice in email) |
| 03 | 04, 05 (approved surfaces), 07 (clear space on the grid), 27 (logo files) |
| 04 | 03, 02, 12 (divider index), 17 (hinge motion) |
| 05 | 06 (sizes that count as large text), 08 (lever and content-type colors), 14 (data palettes), 17 (states), 26 (color tokens) |
| 06 | 05, 07 (measure and rhythm), 19 (reading size and zoom), 22 (the email stack) |
| 07 | 06, 08 (sanctioned positions), 20, 25 |
| 08 | 03, 09, 14 (legend mark), 17 (grid states) |
| 09 | 01, 08, 10, 20 (pillar navigation) |
| 10 | 09, 11, 15 (encoding meanings), 27 |
| 11 | 10, 17, 18 |
| 12 | 04, 05 (watermark opacity), 13 (evidence annotations), 15 (intervention markers) |
| 13 | 02, 14, 15, 16 |
| 14 | 13, 05, 08, 18 (chart controls) |
| 15 | 13, 14, 10, 21 |
| 16 | 13, 19 (alt text), 23 |
| 17 | 05, 08, 18, 19 |
| 18 | 17, 19, 24 (the reader), 26 |
| 19 | 05, 06, 17, 18, 28 |
| 20 | 07, 09, 18, 21 |
| 21 | 15, 10, 20, 28 |
| 22 | 02, 03, 06, 23 |
| 23 | 04, 16, 22, 27 |
| 24 | 13, 14, 18, 25 |
| 25 | 03, 07, 24, 27 |
| 26 | 05, 06, 07, 17, 27 |
| 27 | 03, 10, 26, 28 |
| 28 | 13, 19, 26, 27 |

## 11. Accounting check

`work/build/scripts/phase-1/ux_architecture_coverage.py` reads both inventories and the V5 heading list from Phase 0, then searches this file for each one. Results on October 21, 2026:

- V5 Polished sections mapped: 18 of 18.
- V5 h3 headings found in a mapping row: 104 of 104 (V5's line breaks inside headings, such as "Know therules.", are matched with spaces and punctuation removed).
- V4.2 sections mapped: 20 of 20.
- V6 chapters with a contents row and a cross-reference row: 28 of 28.
- Home cells in the V5 tables that cite a chapter number outside 01 to 28: 0.

The script prints any miss. It printed none on the final run.

## 12. Decisions for Gate 1

| # | Decision | Options | Recommendation |
|---|---|---|---|
| A1 | The contents | (a) Six parts, 28 chapters as in section 2. (b) The brief's starting map unchanged. | (a). Every V5 and V4.2 chapter has a home, and the Signal Grid, accessibility and the atlas each get a chapter. |
| A2 | Layout and the Signal Grid | (a) Two chapters, 07 and 08. (b) One chapter, as in the brief. | (a). The encodings need room, and "The Grid" misled even the Phase 0 audit. |
| A3 | Evidence and sourcing position | (a) First in its part. (b) Last, as in the brief. | (a). The chart and systems chapters depend on its title types. |
| A4 | Accessibility | (a) Chapter 19 in Behavior. (b) A chapter in Production. (c) No chapter; rules spread across chapters. | (a). The rules describe behavior, and 28 links to them. |
| A5 | The atlas | (a) 20 Web and 21 The atlas, with the system test inside 21. (b) "Web and atlas" plus "Atlas system test", as in the brief. | (a). The hardest application deserves a findable chapter. |
| A6 | Social and video | (a) One chapter, 23. (b) Separate "Video frames" chapter. | (a). One set of safe-area overlays. |
| A7 | Numbering and IDs | (a) Continuous 01 to 28, word anchors, Rule NN.n, V5 aliases. (b) Numbering within each part. | (a). Short citations that cannot collide with V7 IDs. |
| A8 | Heading rule | (a) h2 "05 Color", instruction beneath, rule h3s, labels for template blocks. (b) h2 plus h3 for every template block. | (a). A clean outline for screen reader users. |
| A9 | Candidate line history | Show Dustin that V4.2 lists "From spectators to stewards." as a retired historical tagline before he rules on it. | Attach the V4.2 record to the strategy board's candidate-line decision. |

## 13. Checked and not checked

**Checked:**
- Every V5 Polished section and h3 heading, and every V4.2 section, against this map, by script (section 11).
- V5 chapter text in full for all eighteen sections, and V4.2 text for all twenty.
- Section sizes from the V5 inventory (the Grid at 110,055 characters and 63 figures).
- Palette contrast values in the brief, recomputed with the WCAG formula; all 24 pairs match to two decimals.

**Not checked:**
- The creative director's review of this map, which the phase prompt calls for.
- Whether the token names used as examples match the engineer's token architecture, written in parallel.
- Reading-level and voice review of the instruction lines; the editor reviews every board's text in step 7.
- The atlas chapter's content against V7; that belongs to the data visualization lead in Phase 3.

## Change log

Created:
- `work/ledger/20261021_Guide-Architecture-Map.md` (this file)
- `work/build/scripts/phase-1/ux_architecture_coverage.py`

Modified: none. `source/`, `work/extract/` and the V5 masters were not touched.
