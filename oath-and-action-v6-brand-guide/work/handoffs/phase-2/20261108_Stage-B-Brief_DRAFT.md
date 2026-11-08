# Brief: stage board B, chapters 09 to 12 (draft for Dustin's go)

Oath & Action Edition 06, Phase 2, November 8, 2026. Written by the main session from `20261107_Stage-B-Scoping-Notes.md`, Dustin's changes board answers (DR-133 to DR-138) and the carried items in the eighth handoff. This is a draft. Nothing here is built until Dustin gives his go and answers the open questions at the end. Where an answer would change the plan, the line says so.

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
- **Domes and columns (DR-135, D2-464).** The domes in CL-025 Congress, CL-014, R-13 and R-42 and the columns in CL-059 and R-48 are redrawn, every other part and its red kept. Rule 01.6 stands whole. The original masters stay in the package as a record.
- **Size floor (DR-136).** Topic and atlas symbols from 48 px; 24 px only for the 41 that read there; none at 16 px. This closes CA-S12's 16 px kicker icon: a kicker's topic icon is 24 px and comes from the 41 (D2-373).
- **Topic set (DR-137).** Civic Line's 72 topic drawings are the topic set. Testify and Contact an official are drawn if the Act pieces need them, each under named approval (open question 3).
- **Part openers (DR-138).** No pillar icon on a part opener.
- **Kickers and red (DR-112, DR-66, DR-67).** A topic icon sits only beside its own word. In a row or a menu, icons go one color and only the current one keeps its red, as signature red. Icons at 16 px are one color with no red.
- **Settled and unchanged.** The Civic Line drawings other than DR-135's six, the atlas visual system (System 1, DR-36), the chart system (DR-52 to DR-61), chapter 14's plan (DR-62, DR-63), DR-64's chart rules, chapter 02's writing rules (DR-73 to DR-83) and every answer from DR-95 on.

## Who makes what

| Maker | Role file (`.claude/agents/`) | Owns |
|---|---|---|
| Icon designer | `oa-design-director.md` | Every new drawing in this stage, by one hand: the pixel-fit pillar icons, the six redraws, the utility set, and any drawing open questions 3 and 4 add. Writes new files only, in new folders (`work/build/assets/pillar-pixel-fit/`, `civic-line-redraws/`, `utility-icons/`); the Civic Line masters are read, never edited |
| Identity designer | `oa-design-director.md` | Chapter 09; chapter 12's dividers, watermarks and patterns; the lockmark's pixel masters if open question 7 says so |
| Systems designer | `oa-design-director.md`, checked against `oa-ux-accessibility-lead.md` | Chapter 10; chapter 11's new groups (status marks, utility icons, information and alert marks); chapter 12's systems devices (intervention marker, chart keys, map locators, layer diagram) |
| Editor | `oa-editor.md` | Every word: one meaning sentence per symbol, labels matched to Atlas V7's names and IDs, then the copy edit of all four chapters |
| Engineer | `oa-engineer.md` | Shell for 09, 10 and 12; mark and icon tokens, including the tracker tokens (D2-402); a pixel-fit check and Board 6's shape-likeness script as build checks; the page's weight plan; the tokens.css link (D2-461) |
| Accessibility lead | `oa-ux-accessibility-lead.md` | The audit of interface actions that sets the utility list; accessible names, targets, forced colors and reduced motion for every icon group |
| Research lead | `oa-research-lead.md` | Every CL and R symbol checked against its V7 ID; Loop R4a's 2025 and 2026 redraws counted by party for Rule 01.11's plate; a source for the state hearing claim; Nebraska's one-chamber route; real or labeled state bill numbers; the stages of a records request and of federal rulemaking from official sources; the Civic Line rights line (Q-16) |
| Creative director | `oa-creative-director.md` | Scores last, on the brief's six criteria |

## Order of work

1. **Round 0, in parallel.** The research lead, the accessibility lead's audit, and the engineer's shell and tokens. The audit's list of actions goes to the icon designer as the utility set's scope.
2. **Round 1, drawings.** The icon designer draws, and a short drawings board shows each drawing beside its master at true size (pixel-fit pillar icons at 16, 24, 48 and 96 px; each redraw beside its original; the utility set at 16 and 24 px on Newsprint and Charcoal). The identity designer adds L6 with its wordmark and tagline centered on the strip, since without its dots they sit about 10 px above the middle (the creative director's review of the Q1 to Q4 pass). Dustin approves drawings by name there (gate rule 4, D2-463). Open question 1 asks whether this board comes first.
3. **Round 2, chapters.** Chapter 10's construction and size rules first, since 09 and 11 cite its grid. Then 09 and 11 together, and 12 last. The editor writes alongside each maker.
4. **Round 3, review.** The editor's copy edit. Then red teams on brand and evidence, and on craft and accessibility, with the creative director's review; one fix pass; the creative director's scores and sign-off.
5. **Board B.** Chapters 09 to 12 in the chapters page, a decisions panel, and the reader check (open question 5). The main session builds, checks and publishes.

Then stage board C (chapters 17, 18, 19 and 26), the shell's last pass, the Gate 2 preview build and Gate 2.

## Rules that bind every page

Everything in `20261106_Stage-A-Brief.md` sections "The content contract" and "Rules that bind every page", as amended since: Rule 05.3 as it now reads; text 13 px or more; the type scale for fixed artboards (D2-254); one Illustrative label at the head of a wholly invented piece (DR-97, D2-440); the failure band on a failure plate that could pass for our work (D2-308); no studio codes on reader pages (D2-253); plates 600 px or narrower in a chapter column, with Fit to window never under 13 px (D2-424, D2-442); no em dashes. Encoding glyphs drawn for chapter 10 copy System 1's constants exactly. An error mark, the take-part mark and an intervention marker can each claim red, and only one of them works as a view's red (Rule 05.3); chapter 11 says which one yields.

## Risks the plan answers

- **Page weight.** Inlining 122 symbols strains the 16 MB page limit. The engineer sets a plan before round 2: one sprite per family, referenced by `<use>`, and contact sheets as images.
- **Thin lines.** The Civic Line line renders near 0.5 px at 24 px. The 48 px floor (DR-136) and the pixel-fit pillar icons answer it.
- **Look-alikes.** CL-024 Feedback Loop reads as a refresh sign, and the folder and envelope drawings read as app glyphs. Chapter 11's failure case shows CL-024 used as a refresh button, and the shape-likeness check keeps the utility set apart from the topic set.
- **Missing fifth-edition files.** V5 and V4.2 are not in this checkout (DR-90). The utility set is new (DR-134), so V5's six glyphs are not needed; watermarks are drawn from today's masters at the token opacities 0.08 and 0.10.

## Open questions for Dustin, before the go

1. A drawings board before the chapters are built (recommended), or every drawing on board B with the chapters?
2. Which records beyond bills get status marks: records requests and agency rules (recommended), those two plus court cases and ballot measures, or bills only for now?
3. Should the icon designer draw Testify and Contact an official now, for the drawings board (recommended)?
4. Should stage B also draw a pixel-fit end mark at 12 and 14 px (recommended)?
5. The reader check has no answers yet. Retire its link and send one combined check at board B, to readers who have never seen the brand (recommended), or keep the live check and add a second round?
6. Which tool made the Civic Line sheets, and on what terms (Q-16)?
7. The 16 and 24 px lockmark masters part into stripes when a page scales them, as at L3's 196 px minimum. Should the identity designer rebuild the three pixel masters with each node and the lever as one outline, the same pixels at each master's own size, shown beside today's files at 16, 24, 34, 40 and 48 px on the drawings board (recommended), or keep them as they are?
