# Brief: stage B round 2, chapters 09 to 12

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the main session for the systems designer, the identity designer, the editor and the engineer. It applies round 2 of the final stage B brief (`20261109_Stage-B-Brief.md`) with every answer Dustin has given since: the drawings board (DR-156 to DR-182) and the promotion plan (DR-184 to DR-186, D2-714 to D2-718), all in `work/ledger/20261020_Decision-Log.md`. The final stage B brief's goal, table of chapters, "What Dustin has decided" and "Rules that bind every page" still bind; read them first.

## The goal

Chapters 09 to 12, the rest of the part called Symbols and graphics, as finished guide pages in the same shell as chapters 01 to 08 and 11's trackers. A designer opens chapter 10, finds the symbol for a subject, and sets it at a size that reads, with no other document. The bar is the best brand guide any studio has shipped: calm and exact, every rule earning its place, every specimen finished content at true size.

## Inputs every owner reads

- `CLAUDE.md`, your role file in `.claude/agents/`, the final stage B brief, this brief, and the Master Brief sections your role file names (`brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`; sections 6, 7, 11 and 12 for every maker).
- The content contract and the binding rules in `work/handoffs/phase-2/20261106_Stage-A-Brief.md` ("The content contract", "Rules that bind every page"), and the shell notes `20261106_Guide-Shell-Notes.md`.
- The writing rules: `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md` (chapter 02 governs).
- The round 0 work: `20261109_Stage-B-Research-Notes.md`, `20261109_Stage-B-Accessibility-Audit.md`, `20261109_Stage-B-Engineer-Notes.md`.
- The finals and how to draw them: `20261110_Promotion-Brief.md` and the four `20261110_Promotion-*-Notes.md` files as they land. The engineer's notes give the `<use>` pattern for each family and the 1x and 2x pillar pattern.
- The Atlas V7 model: `work/extract/atlas-v7-data.json` (if it is missing, run `cp work/research/atlas-v7-docs/20261015_Atlas-V7-Model.json work/extract/atlas-v7-data.json` from the project folder). Query it by script with `python3 -I`; never read it whole.
- Chapter 11 as built: `work/build/guide/chapters/11-icons.json`, the `s-11-*` specimens and `work/build/scripts/phase-2/apply_systems_ch11.py`.

## Order of work

1. **Chapter 10 starts first.** Its maker writes the construction and size rules (the grid, the line, caps and joins, the red accent, the capped fit, the size floors and the list of 41 that read at 24 px) to `20261110_Stage-B-Ch10-Construction.md` before anything else, so chapters 09 and 11 cite one text.
2. **Chapters 09 and 11 start** when that file exists.
3. **Chapter 12 starts** when 09 and 11 are drafted.
4. The editor writes alongside each maker from the start, and the engineer builds the reader check page once the editor's questions exist.

Build the guide with `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <your scratch folder>/guide.html` and look at your chapters at 1440 and 390 px as you go.

## Who makes what

| Owner | Role file | Owns this round |
|---|---|---|
| Systems designer | `oa-design-director.md`, checked against `oa-ux-accessibility-lead.md` | Chapter 10; chapter 11's new groups; chapter 12's systems devices; the renumbered state bills and Nebraska's step 5 in chapter 11 (DR-150, DR-151, D2-532) |
| Identity designer | `oa-design-director.md` | Chapter 09; chapter 12's dividers, watermarks and patterns; chapter 01's three pillar specimens (`s-01-pillars`, `s-01-21-correct`, `s-01-21-failure`) moved to the sprite with the pillar fits and `data-icon-family="pillar"`; the renumbered state bill in chapter 08 (`s-08-3-*`) |
| Editor | `oa-editor.md` | Every word of 09 to 12: one meaning sentence per symbol and the labels of DR-185; Rule 01.11's map count (DR-149, research section 3); the combined reader check's questions and its two-line invitation (D2-493, DR-143, DR-148) |
| Engineer | `oa-engineer.md` | The shell for 09, 10 and 12 as the chapters need it; `guide_check.js`'s round 2 checks ("Left for round 2" in the engineer's notes) with `REQUIRE_FAMILY` on; the 16 px utility line token once a 16 px utility icon is on a page; removing the shell's mark bridge rules once `MARK_CSS` reads the tokens; the combined reader check as a new dated page from the first check's tooling (D2-493), leaving `work/boards/phase-2/reader-check/` as it is |

Chapter 01's three pillar specimens and `s-08-3-*` move to the identity designer for this round (D2-719): they show drawings and marks that chapter 09's owner draws. The editor keeps every word in them.

## Chapter 10, Topic and atlas symbols (`#symbols`)

Instruction line: "Find the symbol for a subject or an atlas element and set it with its label."

- **Classes.** Open with the symbol classes and the job of each, so the reader knows which chapter holds what: pillar icons (09), topic symbols and atlas symbols (10), status marks and utility icons (11), encoding glyphs (shown in 10, taught with the systems grammar in 15). A topic or atlas drawing never stands for an interface action (D2-515).
- **The set in use.** 124 drawings in `work/build/assets/civic-line-v6/`: 74 CL drawings (CL-001 to CL-074, with CL-073 Testify and CL-074 Contact an Official, D2-714; the four pillar icons CL-019 to CL-022 are among them and chapter 09 governs them) and 50 reform drawings (R-01 to R-50). The six redraws are the drawings in use; the originals are a record, never shown on a reader page as a choice. Atlas symbols are keyed to V7's IDs: the 51 variables, drivers X1 to X5 among them, and the 50 reforms. Domains, hubs, layers and routes stay words and typed chips, with no new drawings.
- **Construction.** Civic Line's 128-unit box, one line weight, round caps and joins, one red accent, the capped fit (DR-08), from `work/ledger/20261029_Civic-Line-Icons-Report.md`. V4.2's four construction principles ("Weight with open space.", "A deliberate cut.", "People have a place.", "Meaning earns the detail.") may feed "Why it works" where they hold for Civic Line; say where each came from.
- **Sizes (DR-136, D2-373).** 48 px and up for every topic and atlas symbol; 24 px only for the 41 that read there, listed by ID in the chapter (this is guide check B-3's list); none at 16 px. A kicker's topic icon is 24 px and comes from the 41.
- **Labels (DR-185).** An atlas symbol prints V7's name; a topic symbol its Civic Line word. CL-025 reads "Congress" as a topic and "Congressional capacity" where it stands for D1; R-13 reads "Congress's own experts"; R-36 "Lasting public investment". R-35 keeps "Rejected" with it wherever it appears. The editor's table of labels governs the words.
- **Red (Rule 05.3, DR-66, DR-67, R10, R11).** One red accent per drawing. In a row or a menu the drawings go one color and only the current one keeps its red, as signature red. A standalone drawing's red sits bare on Newsprint as signature red. No red under 48 px.
- **Surfaces and tiles.** The four editions and the six tiles, with Charcoal the default tile for the app icon and avatars (R13).
- **The library.** The whole set shown as contact sheet images by category, drawn from `civic-line-v6/` (D2-591, D2-717), each drawing with its ID, its word and the editor's meaning sentence reachable as text. Keep chapter 10 inside its 1.0 MB budget; a grid of symbols is one Tab stop or links in reading order (G-5).
- **Distinctness.** Side by side checks for related subjects, with the look-alike figures: CL-073 Testify against CL-005 Public Meeting; CL-074 Contact an Official against CL-061 Household Income (research section 2); CL-025 Congress against CL-014; CL-053 Housing Scarcity against CL-054 Home Equity and CL-063 Essential Costs; CL-027 Court Alignment against CL-031 Local Government; CL-048 Public Records against CL-023 Evidence. The Master Brief's Bill and State house have no drawing (DR-137).
- **Encoding glyphs.** Copy System 1's constants exactly (DR-36; `work/ledger/20261105_Atlas-Editorial-Systems-Report.md` and the atlas kit scripts it names). Show them as a class with a pointer to chapter 15.
- **Failure cases** that teach: a symbol at 16 px, a symbol without its word, a red accent in a row where it is not the current item, a drawing used as a button.

## Chapter 09, Pillar icons (`#pillar-icons`)

Instruction line: "Mark which pillar a piece serves, always in the order Explain, Track, Connect, Act."

- Set A, CL-019 to CL-022, each with its word, in that order (DR-111). The current word is underlined at every size; red is a second sign from 48 px.
- Under 48 px: one color (D2-497, R10), drawn from the pixel fits at 24 and 16 px on 1x screens and from the masters at 24 px on 2x screens (DR-179), with the engineer's pattern. Under 48 px a pillar icon sits with its word (R9).
- Where they go: the pillar row, section openers and tiles; never in a kicker (DR-112); no pillar icon on a part opener (DR-138).
- Specimens: pillar rows at 48 and 24 px on Newsprint and Charcoal; the phone column (D2-376); a 128 px Charcoal opener with styled text, such as V5's "Watch the vote."; the rounded tile from 76 px; a failure case with a pillar icon in a kicker.

## Chapter 11, Status and utility icons (`#icons`)

Instruction line: "Give each record state or interface action a glyph and a word that read without color."

- **Trackers stay as Rules 11.1 to 11.7**, with Nebraska's step 5 as DR-108's slash and "Nebraska has one chamber" on every Nebraska card (DR-150), invented state bills renumbered from H.99001 and S.99002 up and labeled Illustrative (DR-151), and Rule 11.7's 44 px (DR-153).
- **Status marks for records requests and agency rules (DR-140)** on the tracker's shapes, from research section 7: six steps each, a step that never happened keeps its number with a slash, end states in words, waits in words (D2-526 to D2-529). Court cases and ballot measures wait.
- **Utility icons (DR-161 to DR-178)**, the 18 finals in `work/build/assets/utility/`, under the audit's rules: a glyph beside a word except the four named exceptions (D2-506); one form, one meaning (D2-507); words for share, zoom, print and information (DR-154); links to other sites in the same tab with hidden words (D2-513); 24 px beside a control's word, 16 px only inline or in a table heading (D2-514); `data-icon` and `data-icon-family` on every use (D2-517).
- **Information and alert marks**: Error, Success and Warning, each with its word. Say which red yields when the error mark, the take-part mark and an intervention marker meet in one view (Rule 05.3).
- **Five live interactive specimens (D2-516)**: a loop stepper, a report reader toolbar, a library filter bar, a phone menu and a form error, built as components so the guide check's name, keyboard, focus and forced colors tests run inside them.
- **Failure case**: CL-024 Feedback Loop used as a refresh button (D2-515).
- The engineer's requests: mark widths in `MARK_CSS` as `var(--oa-component-mark-...)`.

## Chapter 12, Graphic devices and patterns (`#graphic-devices`)

Instruction line: "Add dividers, frames, markers and watermarks only where they help someone read."

- **Identity designer:** dividers (the Stone hairline; the hinge divider, indexed from chapter 04); watermarks drawn from today's masters at the token opacities 0.08 and 0.10, and an opaque compact signature for small headers and video corners; at most two restrained patterns built from approved masters, after icon study 07, each with its failure case (a pattern behind body text).
- **Systems designer:** the intervention marker as System 1's red target; chart keys from the chart system (DR-52 to DR-61); map locators; a layer diagram (the one place an exploded view is allowed); the "Who owns the next step?" frame from V4.2.

## Rules that bind every page

The final stage B brief's list, plus: every symbol shown with its word; drawings from the sprite by `<use>`, never inlined (D2-590); every public policy statistic with its source, period and qualification; invented items labeled Illustrative beside the item; no studio codes on reader pages (D2-253); plates 600 px or narrower in a chapter column; text 13 px or larger except a mark shown at true size, which its caption says.

## Notes and limits

Each owner writes `work/handoffs/phase-2/20261110_Stage-B-Round-2-<Role>-Notes.md` (`Systems`, `Identity`, `Editor`, `Engineer`) early and adds as it goes: what it built, routine calls as "D2-xxx | decision | reason" lines, questions for Dustin with a recommendation, Tested and Not tested kept apart, and a change log.

Never touch `source/`, `work/ledger/`, `deliverables/`, the asset folders' finals or masters, any board, the first reader check, or another owner's files. Specimens and chapter JSON belong to the chapter's owner; the editor sends word changes as a table in its notes or edits words only in files its owner names. Do not commit or push. Scratch outputs go to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/round-2/<role>/`. Reply to the main session in 200 words or fewer.
