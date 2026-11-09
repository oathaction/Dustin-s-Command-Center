# Brief: stage board B, chapters 09 to 12

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the main session for the makers, the engineer, the accessibility lead and the research lead. Built from `20261107_Stage-B-Scoping-Notes.md` and the draft, `20261108_Stage-B-Brief_DRAFT.md`, which stays as the record. Dustin approved the plan and every recommendation on November 9 (DR-139 to DR-145), after his changes board answers (DR-133 to DR-138). The studio's calls for this stage start at D2-491.

## The goal

Chapters 09 to 12, the rest of the part called Symbols and graphics, as finished guide pages in the same shell as chapters 01 to 08 and 11's trackers: final copy, real specimens at true size, every symbol shown with its word. A designer should be able to open chapter 10, find the symbol for a subject, and set it at a size that reads, with no other document. The bar is unchanged: the best brand guide any studio has shipped, calm and exact, with every rule earning its place.

| No. | Chapter | Anchor | Instruction line |
|---|---|---|---|
| 09 | Pillar icons | `#pillar-icons` (from `pillar-marks`, D2-446) | Mark which pillar a piece serves, always in the order Explain, Track, Connect, Act. |
| 10 | Topic and atlas symbols | `#symbols` | Find the symbol for a subject or an atlas element and set it with its label. |
| 11 | Status and utility icons | `#icons` | Give each record state or interface action a glyph and a word that read without color. |
| 12 | Graphic devices and patterns | `#graphic-devices` | Add dividers, frames, markers and watermarks only where they help someone read. |

## What Dustin has decided for this stage

- **Pillar icons (DR-111, DR-133).** Set A, CL-019 Explain, CL-020 Track, CL-021 Connect and CL-022 Act, each with its word, the current word underlined at every size, red a second sign from 48 px. The studio draws pixel-fit 16 and 24 px versions that keep every feature and red placement, and shows them beside the masters at 16, 24, 48 and 96 px before they enter the guide.
- **Utility icons (DR-134).** About eighteen, drawn on a 24-unit grid, limited to the actions the accessibility audit finds the guide, the atlas and the reports need.
- **Domes and columns (DR-135, D2-464, D2-491).** The domes in CL-025 Congress, CL-014, R-13 and R-42 and the columns in CL-059 and R-48 are redrawn, every other part and its red kept. Rule 01.6 stands whole. The original masters stay in the package as a record.
- **Size floor (DR-136).** Topic and atlas symbols from 48 px; 24 px only for the 41 that read there; none at 16 px. This closes CA-S12's 16 px kicker icon: a kicker's topic icon is 24 px and comes from the 41 (D2-373).
- **Topic set (DR-137, DR-141).** Civic Line's 72 topic drawings are the topic set. Testify and Contact an official are drawn now, for the drawings board.
- **Part openers (DR-138).** No pillar icon on a part opener.
- **Drawings first (DR-139).** A drawings board shows every new or redrawn drawing beside its master or original at true size, for approval by name, before chapters 09 to 11 are built around it.
- **Status marks (DR-140).** Records requests and agency rules, beside the bill tracker, on the tracker's shapes. Court cases and ballot measures wait.
- **End mark (DR-142).** A pixel-fit end mark at 12 and 14 px, shown beside today's end mark.
- **Reader check (DR-143).** The live link is not sent. Board B carries one combined check, sent once to readers who have never seen the brand.
- **Civic Line rights (DR-144).** Dustin made the sheets in his own conversation with ChatGPT, with no one else's work as a source. The traced vector masters are final and approved. The rights ledger records it.
- **Lockmark masters (DR-145).** The 16, 24 and 48 px masters are rebuilt with each node and the lever as one outline, the same pixels at each master's own size, and shown beside today's files at 16, 24, 34, 40 and 48 px.
- **Kickers and red (DR-112, DR-66, DR-67).** A topic icon sits only beside its own word. In a row or a menu, icons go one color and only the current one keeps its red, as signature red. Icons at 16 px are one color with no red.
- **Settled and unchanged.** The Civic Line drawings other than DR-135's six, the atlas visual system (System 1, DR-36), the chart system (DR-52 to DR-61), chapter 14's plan (DR-62, DR-63), DR-64's chart rules, chapter 02's writing rules (DR-73 to DR-83) and every answer from DR-95 on.

## Who makes what

| Maker | Role file (`.claude/agents/`) | Owns |
|---|---|---|
| Icon designer | `oa-design-director.md` | Every new icon in this stage, by one hand: the pixel-fit pillar icons, the six redraws, the utility set, Testify and Contact an official. Writes new files only, in new folders (`work/build/assets/pillar-pixel-fit/`, `civic-line-redraws/`, `utility-icons/`, and Testify and Contact an official in a folder it names for new topic drawings); the Civic Line masters are read, never edited |
| Identity designer | `oa-design-director.md` | The pixel-fit end mark (DR-142), the lockmark masters' rebuild (DR-145) and L6 centered on its strip, all for the drawings board; then chapter 09, and chapter 12's dividers, watermarks and patterns |
| Systems designer | `oa-design-director.md`, checked against `oa-ux-accessibility-lead.md` | Chapter 10; chapter 11's new groups (status marks for records requests and agency rules, utility icons, information and alert marks); chapter 12's systems devices (intervention marker, chart keys, map locators, layer diagram) |
| Editor | `oa-editor.md` | Every word: one meaning sentence per symbol, labels matched to Atlas V7's names and IDs, the combined reader check's questions (D2-493), then the copy edit of all four chapters |
| Engineer | `oa-engineer.md` | Shell for 09, 10 and 12; mark and icon tokens, including the tracker tokens (D2-402); a pixel-fit check and Board 6's shape-likeness script as build checks; the page's weight plan; the tokens.css link (D2-461); the combined reader check as a new dated page (D2-493) |
| Accessibility lead | `oa-ux-accessibility-lead.md` | The audit of interface actions that sets the utility list; accessible names, targets, forced colors and reduced motion for every icon group |
| Research lead | `oa-research-lead.md` | Every CL and R symbol checked against its V7 ID; Loop R4a's 2025 and 2026 redraws counted by party for Rule 01.11's plate; a source for the state hearing claim; Nebraska's one-chamber route; real or labeled state bill numbers; the stages of a records request and of federal rulemaking from official sources |
| Creative director | `oa-creative-director.md` | Scores the drawings board before it goes to Dustin, then the chapters last, on the brief's six criteria |

## Order of work

1. **Round 0, in parallel.** The research lead, the accessibility lead's audit, and the engineer's shell and tokens. The audit's list of actions goes to the icon designer as the utility set's scope. The research lead writes early and adds as it goes.
2. **Round 1, drawings.** The icon designer and the identity designer draw in parallel. A board builder makes the drawings board:
   - the pixel-fit pillar icons beside the masters at 16, 24, 48 and 96 px
   - each redraw beside its original at 24, 48 and 128 px
   - the utility set at 16 and 24 px on Newsprint and Charcoal, with the shape-likeness check against the topic set
   - Testify and Contact an official beside their nearest topic drawings
   - the pixel-fit end mark at 12 and 14 px beside today's
   - the rebuilt lockmark masters beside today's at 16, 24, 34, 40 and 48 px
   - L6 centered beside L6 as drawn

   Each card says what Dustin approves by name. The creative director scores the board before it goes to him. The main session publishes it and waits for his answers (DR-139).
3. **Round 2, chapters.** Chapter 10's construction and size rules first, since 09 and 11 cite its grid. Then 09 and 11 together, and 12 last. The editor writes alongside each maker.
4. **Round 3, review.**
   - the editor's copy edit
   - red teams on brand and evidence, and on craft and accessibility, with the creative director's review
   - one fix pass
   - the creative director's scores and sign-off
5. **Board B.**
   - chapters 09 to 12 in the chapters page
   - a decisions panel
   - the combined reader check (DR-143)

   The main session builds, checks and publishes.

Then stage board C (chapters 17, 18, 19 and 26), the shell's last pass, the Gate 2 preview build and Gate 2.

## Rules that bind every page

Everything in `20261106_Stage-A-Brief.md` sections "The content contract" and "Rules that bind every page" still binds, as amended since:
- Rule 05.3 as it now reads.
- Text 13 px or more.
- The type scale for fixed artboards (D2-254).
- One Illustrative label at the head of a wholly invented piece (DR-97, D2-440).
- The failure band on a failure plate that could pass for our work (D2-308).
- No studio codes on reader pages (D2-253).
- In a chapter column, plates 600 px or narrower, with Fit to window never under 13 px (D2-424, D2-442); a frame takes 32 px sides where that makes a plate fit (D2-484).
- No em dashes.

Encoding glyphs drawn for chapter 10 copy System 1's constants exactly. An error mark, the take-part mark and an intervention marker can each claim red, and only one of them works as a view's red (Rule 05.3). Chapter 11 says which one yields.

## Risks the plan answers

- **Page weight.** Inlining 122 symbols strains the 16 MB page limit. The engineer sets a plan before round 2: one sprite per family, referenced by `<use>`, and contact sheets as images.
- **Thin lines.** The Civic Line line renders near 0.5 px at 24 px. The 48 px floor (DR-136) and the pixel-fit pillar icons answer it.
- **Look-alikes.** CL-024 Feedback Loop reads as a refresh sign, and the folder and envelope drawings read as app glyphs. Chapter 11's failure case shows CL-024 used as a refresh button, and the shape-likeness check keeps the utility set apart from the topic set.
- **Missing fifth-edition files.** V5 and V4.2 are not in this checkout (DR-90). The utility set is new (DR-134), so V5's six glyphs are not needed. Watermarks are drawn from today's masters at the token opacities 0.08 and 0.10.
- **Fresh containers.** Install the build tools first (ninth handoff, section 3), and commit a snapshot as each agent reports.

## Notes and limits for every agent

Each agent writes its notes to `work/handoffs/phase-2/YYYYMMDD_Stage-B-<Role>-Notes.md` with:
- what it built
- routine calls as "D2-xxx | decision | reason" lines
- questions for Dustin with a recommendation
- Tested and Not tested, kept apart
- a change log

Never touch `source/`, `work/ledger/`, the Civic Line masters, the identity masters (new files beside them only), any existing board, the first reader check, or another owner's files. Do not commit or push. Reply to the main session in 200 words or fewer.
