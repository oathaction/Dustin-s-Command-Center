# Brief: stage C, round 1, chapters 17, 18, 19 and 26

Oath & Action Edition 06, Phase 2, November 11, 2026. Written by the main session for the makers of round 1. It carries out "Order of work" 3 of `20261110_Stage-C-Brief.md`, which every maker reads first, with its "What each chapter holds", "Who makes what" and "Rules that bind every page". The studio's calls for this round start at D2-1266. Dustin's answers this round: DR-213 (chapter 19's device script), DR-214 (chapter 26's downloads), DR-215 (a private preview at the handoff).

## The goal

Four finished chapters in the guide's shell, at the bar of chapters 01 to 12: a developer opens chapter 18, copies a component, sets it with tokens from chapter 26, and ships it with every state, keyboard path and announcement right, with no other document. Calm, exact, every rule earning its place.

## Read first

`CLAUDE.md`; your role file in `.claude/agents/`; `20261110_Stage-C-Brief.md`; the round 0 notes that feed your chapter: `20261110_Stage-C-Research-Notes.md` (WCAG words, APG patterns, browser support, theme storage), `20261110_Stage-C-Interaction-Inventory.md` (the 24 components, the states matrix, the chapter 19 map, faults F-1 to F-16), `20261110_Stage-C-Engineer-Round-0-Notes.md` (its section "Contracts round 1's makers follow"); `work/ledger/20261021_Token-Architecture.md`; the decision log from D2-1129 on; chapter 02's writing rules, `20261106_Voice-Writing-Rules.md`. Model your chapter file on `work/build/guide/chapters/11-icons.json` (keys `number`, `anchor`, `title`, `part`, `instruction`, `intro`, `groups`, `rules`, `extras`, `related_chapters`, `sources`; each rule `id`, `title`, `rule`, `tokens`, `why`, `correct`, `failure`, `specs`, `related`, `builders`) and write it with a generator script, as every chapter is written.

## Files each chapter owns (D2-1267)

| Chapter | Chapter file | Generator | Specimens and manifest | Code sets |
|---|---|---|---|---|
| 17 Motion and states | `17-motion-and-states.json` | `stage_c_ch17_build.py` | `s-17-*`, `manifest-motion.json` | none, unless a state needs code to copy |
| 18 Components and interaction | `18-components.json` | `stage_c_ch18_build.py` | `s-18-*`, `manifest-components.json`; anatomy plates `s-18-NN-anatomy` in `manifest-anatomy.json` | `work/build/guide/code/c-18-<name>.html`, `.css`, `.js` and `.keys.json` |
| 19 Accessibility | `19-accessibility.json` | `stage_c_ch19_build.py` | `s-19-*`, `manifest-accessibility.json` | none |
| 26 Tokens and how to choose them | `26-tokens.json` | `stage_c_ch26_build.py` | `s-26-*`, `manifest-tokens.json` (with `s-26-token-table` from `token_table_build.py`) | `c-26-<name>` for the worked examples |

The identity designer's chapter 17 specimens (`s-17-hinge-*`, `s-17-lever-*`) go in `manifest-identity.json`, through its own generator.

## Rule numbers fixed ahead

Other chapters cite these before they are written, so they hold. A maker may add rules after the fixed ones.

**Chapter 26** (engineer, words with the editor):
- 26.1 Tiers and names: categories, names and the three tiers.
- 26.2 Add a token only when it meets the five conditions.
- 26.3 Choose a token in five steps: surface, role, emphasis, state, then any component token, which wins.
- 26.4 The four worked examples of the token architecture's section 8, each at actual size beside its failure, as code to copy.
- 26.5 Start a page from tokens.css: link it, then `body { margin: 0; font: var(--oa-type-body) }` (D2-1203); `<meta name="color-scheme" content="light dark">` on a themed product.
- 26.6 Dark mode: how a role resolves under `data-oa-theme`, the storage key `oa-theme`, the head script that applies a stored choice before the first paint, `--oa-color-surface` and `--oa-color-field-ground`, and the roles that stay `initial` on Charcoal.
- 26.7 Every token: `s-26-token-table`, searchable, with a copy button on each name.
- 26.8 The version rule and the downloads: tokens.css and tokens.json (DR-214), with type and size in the words (F-10).

**Chapter 17** (systems designer; the identity designer supplies Rule 17.6's specimens and draft words):
- 17.1 Move something only to explain a state or a mechanism.
- 17.2 Time motion with the nine motion tokens as they stand.
- 17.3 Play on request, with Play, Pause, Reset and a still view; nothing moves on load and nothing loops.
- 17.4 Under reduced motion, every duration resolves to 0 ms and the final state shows at once.
- 17.5 The three behaviors, slide, draw and land, refined or kept.
- 17.6 The hinge and the lever: the identity's own motion, landing exactly on the approved masters.
- 17.7 Loading: visible words and a still drawing, never a pulse (D2-200).
- 17.8 The ten states (muted, disabled, hover, focus, loading, selected, warning, error, empty, success), each with words or a shape as well as color, on Newsprint and Charcoal. This plate becomes the canonical one that `s-05-4-correct` points to.
- 17.9 Hover and focus: hover by underline or a thicker border, never an inset shadow (G-7); the 2 px focus ring, with its 2 px gap wherever it surrounds a Newsprint fill on Charcoal (D2-1162).
- 17.10 One look for pressed, checked and current: a check glyph before the word, the word in bold and a 2 px edge (D2-1152).

**Chapter 18** (accessibility lead, with the systems designer's anatomy plates and the engineer's code): Rules 18.1 to 18.24 are the inventory's components 18-01 to 18-24, in that order (D2-1146). Each rule shows the component's anatomy, its live code set in the light and dark themes, and a specifications table: every state, the keyboard path, the accessible name, what a screen reader hears when it changes, the target size and the forced colors drawing. Chapter 11 keeps its plates and links to chapter 18 (the stage C brief's "One component, two homes").

**Chapter 19** (accessibility lead): the lead sets its numbers. It holds the 55 A and AA criteria in W3C's words with the guide rule that meets each, the verification matrix of Master Brief section 22 with each method, the guide's own results so far, dated, with Tested and Not tested apart, and the device script of DR-213.

## Contracts (the engineer's round 0 notes, in force)

- **Code to copy (DR-203):** `"code": {"set": "c-NN-name", "name": "..."}` on a rule; two or three files in `work/build/guide/code/`; roles only, never a token named for one surface; `oa-` classes; plain class selectors; no literal color; no type under 13 px; no `nowrap` on a label and two-button rows that stack (F-2); a plain script that finds every copy of its component and never writes the guide's root or storage; native `dialog` with `showModal()` for anything modal (F-12). The build warns on each breach, so `--strict` fails until it is fixed.
- **Keyboard path:** each chapter 18 set has `c-18-<name>.keys.json` listing the steps (key, element that must then hold focus, states that must then hold, words the status line must then say); the guide check walks it in both live stages.
- **Motion:** a moving specimen marks its stage `data-oa-motion` and its controls `data-oa-play`, `data-oa-pause` and `data-oa-reset`; under reduced motion Play shows the final frame at once.
- **Theme:** `data-oa-theme` = `light`, `dark` or `device`; storage key `oa-theme`; the guide stays light.
- **Status lines:** results in words after the success or error mark (Rule 11.15); the shell's `status_line()`.
- **Opener:** `"opener": "<specimen id>"`, a flowing specimen or one at most 328 px wide, in chapters 09 on.
- **Weight:** chapter 17 at 0.5 MB, 18 at 1.1, 19 at 0.3, 26 at 0.6.
- **Landmarks in a live stage (AX-S8):** the accessibility lead and the engineer settle how the masthead's `nav` and a search landmark show live, and log the call.

## Who works when

1. **Now, beside the promotion:** the systems designer for chapter 17; the creative director on Rule 12.4's arcs.
2. **After the promotion's engineering:** the engineer on chapter 26 and round 1's three checks (keyboard path, reduced motion, token table parity); the editor writes chapter 26's words alongside.
3. **Once the identity designer's promotion items land:** its chapter 17 specimens and words (Rule 17.6).
4. **Chapter 18:** the accessibility lead writes the chapter and the keys files; a component engineer writes the 24 code sets in `work/build/guide/code/` only; the systems designer draws the anatomy plates once chapter 17 is drafted. The guide engineer alone edits `guide_build.py`, `guide_check.js` and the shell; any change another maker needs there goes through the main session.
5. **Chapter 19:** the accessibility lead, after chapter 18.
6. **The editor** reads each chapter as its draft lands and changes words only through the maker's generator data, agreed with the maker through the main session.

## Notes and limits for every agent

Each agent writes `work/handoffs/phase-2/20261111_Stage-C-Round-1-<Role>-Notes.md` with: what it built; routine calls as "D2-xxx | decision | reason" lines in a section headed "## Routine calls"; questions for Dustin with a recommendation; Tested and Not tested, kept apart; a change log. Write notes early and add as you go.

Build with `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <your scratch>/guide.html`, never over the committed chapters page. Use the scratchpad `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/<your role>/` for anything temporary, never `/tmp` itself. Run Python with `-I`.

Never touch `source/`, `work/ledger/`, `deliverables/`, any asset master, any board, or another owner's files. Do not commit or push; the main session commits snapshots. Reply to the main session in 200 words or fewer. Every word follows `CLAUDE.md` and chapter 02's writing rules: plain spoken prose, no em dashes. Label illustrative people, places, bills and figures beside the item, and give every public policy figure its source, period and qualification.
