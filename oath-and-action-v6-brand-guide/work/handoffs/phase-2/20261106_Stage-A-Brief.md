# Brief: stage board A, chapters 01 to 08

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the main session for four makers. Approved by Dustin in DR-69 and DR-88 to DR-91 (`work/ledger/20261020_Decision-Log.md`).

## The goal

Chapters 01 to 08, the Foundations part, as finished guide pages: final copy, real specimens at true size, inside a first draft of the guide shell. A reader should be able to open chapter 05 and set a page correctly with no other document. The bar is the best brand guide any studio has shipped: calm, exact, generous with true-size examples, and every rule earns its place.

| No. | Chapter | Anchor | Instruction line (from the architecture map; the editor may tighten it) |
|---|---|---|---|
| 01 | Purpose | `#purpose` | Learn what Oath & Action does, and how its pillars and nonpartisan rules shape every piece. |
| 02 | Voice | `#voice` | Write the way you'd explain a rule to a neighbor, and quote the brand lines exactly. |
| 03 | Identity | `#identity` | Pick the lockup that fits the surface and size, and give it room on every side. |
| 04 | The Ampersand and the hinge | `#ampersand` | Use the ampersand once per composition to join a commitment to what it produces. |
| 05 | Color | `#color` | Choose a surface first, then the text and graphic colors that pass on it. |
| 06 | Type | `#type` | Set every word at a readable size with the three faces and the type scale. |
| 07 | Layout and spacing | `#layout` | Build each page on the column grid and spacing scale, readable at every width. |
| 08 | The Signal Grid | `#signal-grid` | Keep the lockmark to its fixed places, and put a key beside every Signal Grid that codes content. |

## Who makes what

| Maker | Role file to adopt (`.claude/agents/`) | Owns |
|---|---|---|
| Editor | `oa-editor.md` | 01 Purpose, 02 Voice: copy and specimens. In the fix pass, a copy edit of all eight chapters |
| Identity designer | `oa-design-director.md` | 03 Identity, 04 The Ampersand and the hinge, 08 The Signal Grid, and the Gate 2 proofs panel (DR-89) |
| Systems designer | `oa-design-director.md`, with `oa-ux-accessibility-lead.md`'s checks | 05 Color, 06 Type, 07 Layout and spacing |
| Engineer | `oa-engineer.md` | The guide shell, the template blocks, the build that assembles every chapter into one page, and the shared checks |

## Sources every maker reads

- `CLAUDE.md`; chapter 02's writing section `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md` (binding on every word, DR-73).
- Master Brief `brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`: section 3 (locked identity, quoted exactly), 6 (quality bar and rubric), 7 (chapter template), 8 (tensions to repair), and your chapters' sections: 9 identity refinement; 10 color, type, layout, tokens; 12 graphic devices (the hinge divider); 15 evidence and illustrative status; 22 accessibility; 23 writing.
- `work/ledger/20261021_Guide-Architecture-Map.md`: sections 2, 4 (anchors and Rule IDs, "Rule 05.2", anchor `#rule-05-2`), 5 (the heading rule), 6 and 7 (every V5 and V4.2 unit that lands in your chapters, with its action), 8 (new chapter 07), 10 (cross-references).
- The decision log from the top; every G1-, D1-, D2- and DR- entry that touches your chapters wins over older text. Key ones: G1-01 to G1-07, D1-26 and D2-01 and DR-66 (Rule 05.3 as it now reads), DR-53 (Newsprint), DR-67 (R9, R10, R11, R13), DR-71 and DR-89 (width and ampersand B decided at Gate 2; chapter 03 shows today's width), DR-73 to DR-83 (chapter 02), DR-91 (products named with no launch dates or status).
- V5's words and measurements: `work/handoffs/phase-0/text-census.json` and the Phase 0 audits in `work/handoffs/phase-0/` (no V5 upload, DR-90). Phase 1 strategy and voice files in `work/handoffs/phase-1/`.
- Gate 1 template wireframes: `work/boards/20261021_Navigation-And-Template-Wireframes.html`.

## The content contract

Template blocks are rendered by the shell, never by a maker, so all eight chapters share one design. Makers write content and specimens.

**One JSON file per chapter**, `work/build/guide/chapters/NN-anchor.json`:

```
{ "number": "05", "anchor": "color", "title": "Color", "part": "Foundations",
  "instruction": "one sentence",
  "intro": ["at most two short paragraphs"],
  "rules": [
    { "id": "05.1", "title": "The rule as one plain sentence.",
      "rule": "the rule stated plainly, one to three sentences",
      "tokens": ["oa.color.text.primary.onNewsprint"],
      "why": { "text": "...", "basis": "Design judgment" or "WCAG 2.2 SC 1.4.3" or a named source },
      "correct": { "specimen": "s-05-1-correct", "caption": "..." },
      "failure": { "specimen": "s-05-1-failure", "caption": "what goes wrong and why it matters" },
      "corrective": { "specimen": "...", "caption": "..." },          (optional, only when it teaches)
      "specs": [ { "label": "...", "value": "...", "token": "..." } ],
      "files": [ "work/build/assets/..." ],
      "related": ["06", "14"],
      "builders": "a short note on picking the right token or asset" } ],
  "extras": [ { "after_rule": "05.3", "specimen": "...", "caption": "..." } ],   (tables, sheets, demos that sit between rules)
  "sources": [ "full source lines for any statistic or quotation" ] }
```

**Specimens**, `work/build/guide/specimens/<id>.html`: one self-contained HTML fragment each, no `<h1>` to `<h6>` (styled text only; heading rule), inline SVG or `<img>` of a committed asset by repository path, colors only through `var(--oa-...)` from `work/build/tokens/tokens.css` (the engineer is finishing it now; until it exists, read names from `work/build/tokens/20261021_Token-Schema-Draft.json` and the naming rule in `work/ledger/20261021_Token-Architecture.md` section 1). Each specimen sets its own true size. A manifest per maker, `work/build/guide/specimens/manifest-<maker>.json`: `{ id: { chapter, rule, width_px, alt, illustrative: true/false, notes } }`. `alt` is the full text alternative a screen reader hears.

**The shell** (engineer): `work/build/scripts/phase-2/guide_build.py` reads every chapter JSON and specimen and writes one page, `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`: cover with the h1 and the tagline as display text, contents, the Foundations part opener, chapters 01 to 08. It renders each rule as the Master Brief section 7 template, with the h3 "Rule 05.2 ..." and its labels ("Why it works", "Correct application", "Failure case", "Specifications", "Related chapters", "For builders"), and sets the hinge divider (hairline broken by ampersand B in the surface's ink, D1-22, D1-26) between each rule and its correct use (Gate 1 proposal item 4). Navigation as the Gate 1 wireframes draw it, with a phone menu. The part's pillar-mark marking waits for board B (DR-88). The engineer publishes the block markup and a preview command in `work/handoffs/phase-2/20261106_Guide-Shell-Notes.md` early, so makers can preview while they work.

## Rules that bind every page

- Rule 05.3 as it now reads: one working red per view; signature red does not count; red never sits on Prussian. Guide specimens, labeled failure cases and palette swatches do not count toward a view's red (D2-102), but carry `data-red` so the check can see them.
- Text 13 px or larger, except a specimen that shows a mark or a minimum size at true size, which is a graphic and says so in its caption.
- Locked lines quoted exactly (Master Brief section 3). Anything invented carries the Illustrative label beside it (H03). Every public policy statistic carries its full source line (H04). Products named with no launch dates or status (DR-91).
- Today's wordmark width and ampersand B as refined in every chapter page. The condensed width appears only in the proofs panel, labeled for Gate 2.
- No em dashes, outside W21's labeled specimen, drawn as a rule one em wide (DR-79).

## The Gate 2 proofs panel (DR-89, identity designer)

The masthead (L3 on the site and in email), the avatar (circle and square, R13's Charcoal default), a social card (1200 by 630), and a letterhead (US Letter, true size on screen and as a print PDF), each at today's width and condensed, with ampersand B. Side by side at actual size, as `CLAUDE.md` gate rule 4 asks. Any invented headline or address on them carries the Illustrative label. Social cards carry no web address yet (DR-55). Build it as its own specimen set, `s-proofs-*`, which the shell renders as an appendix after chapter 08.

## Checks each maker runs before handing back

- Build the page with `guide_build.py` once it exists, and look at your chapters at 1440 and 390 px.
- `node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html --board` (axe-core: `cd work/build && npm install --no-save axe-core@4.10.2`). The engineer extends the check if guide pages need tests it lacks (heading order, anchors, rule IDs, contrast of every text pair) and says so in the shell notes.
- Locked lines found character for character; no em dash outside W21; no bare record code (H11).

## Output from each maker

Notes in `work/handoffs/phase-2/`: `20261106_Stage-A-Editor-Notes.md`, `20261106_Stage-A-Identity-Notes.md`, `20261106_Stage-A-Systems-Notes.md`, and the engineer's shell notes. Each holds what you built, your routine calls as proposed decision lines ("D2-xxx | decision | reason"), open questions for Dustin with a recommendation, a "Tested" list and a "Not tested" list kept apart, and a change log. Never touch `source/`, the ledgers, the Civic Line or identity masters (read and place them only), or any existing board or concept folder. Do not commit or push; the main session does that.

## After the makers

Four red team lenses (brand, evidence and nonpartisanship; accessibility and interface; craft and typography; civic education and plain language) and a simulated reader panel, labeled untested, review the built page side by side. One fix pass takes all their reports. The creative director scores the fixed page and writes stage board A's content, and the main session builds and publishes the board.
