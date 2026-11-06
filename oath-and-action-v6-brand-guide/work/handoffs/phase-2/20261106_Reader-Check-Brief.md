# Brief: the reader check page

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the main session for one maker. Approved by Dustin in DR-68 and DR-84 to DR-87 (`work/ledger/20261020_Decision-Log.md`).

## Why it exists

Every test of the marks, icons, loops and charts so far used agent raters and no people (Q-13). Before Gate 2, five or more people who have never seen the brand take this check on their phones. Dustin sends the link. The studio reads their answers and reports them at Gate 2.

## What the reader is told

Only that this is a short test of a draft design for a civic publication. No pitch, no brand story, no "Oath & Action" in the page chrome. The wordmark appears only where the masthead question tests it.

## Flow, 8 to 10 minutes on a phone

1. **Welcome and consent.** One plain paragraph: what they will do, about how long it takes, that we record their answers and a first name or initials and nothing else, and that they can stop at any time. One field for a first name or initials. A start button.
2. **Loops (DR-84).** Three drawings from the atlas visual system, System 1 (`work/boards/phase-2/atlas-editorial/01-times-explainer/20261105_Editorial-01-Times-Explainer.html`, built by `build_system.py`; captures already in its `captures/` folder): the overview, the R10 loop close-up, and one more loop (R8 if the page draws it, else another reinforcing or balancing loop you pick; say which and why). Each shows for ten seconds, then hides, then the questions appear. For the two loops, the four questions: does the loop come back to where it started; does it feed itself or push back; which step is least certain; where does a reform act. Use answer choices a newcomer can tap (the step and reform choices use the words printed on the drawing). For the overview, one free-text question about what the page is for, and one tap choice of which part they would open first.
3. **Icons (DR-84).** Eight Civic Line icons (`work/build/assets/civic-line/`), one at a time at 48 px, black edition on Newsprint, ten seconds each, then "What do you think this stands for?" in free text. Include the four pillar marks (CL-019 Explain, CL-020 Track, CL-021 Connect, CL-022 Act) and four topic icons spread across the set; record your picks and their intended meanings.
4. **Marks at 16 px (DR-84).** One sheet at true size, ten seconds: the identity's 16 px masters (wordmark, ampersand B, lockmark, hinge-circle badge in `work/build/assets/identity/`) and the four pillar marks at 16 px, one color (R10, DR-67). Per mark, a tap answer: clear, blurry, or cannot tell.
5. **Charts (DR-85).** S02 child poverty (Explainer page, `work/boards/phase-2/data-viz/01-explainer/`), S11 shift arrows and S14 monthly jobs (stretch page, `work/boards/phase-2/data-viz/stretch/`). Use phone-width drawings at twice size for sharpness. Each shows for fifteen seconds (charts need longer than marks; log it as a routine call), then two questions: "What is this chart telling you, in one sentence?" (free text) and "Does it seem to favor a party or side?" (no; yes, the left; yes, the right; not sure).
6. **Writing pairs (DR-86).** Three before and after pairs from chapter 02 (`work/boards/phase-2/voice/20261106_Voice-Rules-Content.json`): pick three short ones with real befores (W02, W05 and W11 are good candidates; check length on a phone). Show each pair as plain sentences with no edit marks, in random order, labeled A and B. "Which is easier to follow?" A, B, or about the same.
7. **Masthead (DR-86).** The L3 horizontal lockup at today's width and condensed (`work/build/assets/identity/lockups/20261028_L3-Horizontal-Master.svg` and `..._Condensed-Master.svg`) set as a site masthead on Newsprint, the two in random order, shown together for ten seconds. "Which reads faster at a glance?" A, B, or about the same, plus an optional "why" field.
8. **End.** Thanks, and what happens next in one sentence.

Every timed exposure has a "Show it again" button after it hides. Count the uses and record them. This keeps the page usable for readers who need more time (WCAG 2.2.1) while the count tells the studio who needed it. Readers can skip any question.

## Recording answers

- The page is published privately by the main session with `capabilities: {db: {rules: [{path: "responses", read: "admin", write: "owner"}, {path: "responses/{self}", read: "view", write: "interact"}]}, user: {}}`. Each reader writes one document, `responses/<their user id>` from `(await claude.use("user")).id()`. Readers cannot see each other's answers; Dustin and the studio can.
- Read the runtime contract before writing code: `/tmp/claude-0/bundled-skills/2.1.319/803843cfd7ccf1d9e023bc34e9ef63fa/artifact-capabilities/0.2.96/claude.d.ts`, `db.d.ts` and `user.d.ts`. `claude.use(name)` resolves the namespace or `null`; never read `window.claude.db`. Write after each step with a merge (`update` or `set` with merge, as the contract allows), so a reader who stops halfway leaves their answers so far. One write at a time per document; a 10 second timeout on the first read or write; no reload loops.
- **When `db` or `user` is `null`** (a reader who is signed out, or who has view-only access), the page still runs every step, keeps answers in memory, and at the end shows them as plain text with a Copy button and one line asking the reader to send it to the person who shared the link. Tell the reader at the start which mode they are in, in one plain sentence.
- Fields: initials, mode (saved or copy), started and finished times, viewport width, the random orders used, and per step the answer, the seconds until answered, and the show-again count. Store an `answer_key` for the loop questions, the icons' intended meanings and the chart findings in a separate JSON file in the folder, never in the page the reader sees.
- No personal data beyond a first name or initials: no email, no location, no free-text prompt that invites it.

## Look

Newsprint ground, Charcoal text, Inter for text and Inter Tight for headings (Google Fonts, as the boards load them), one working red at most per screen (Rule 05.3) and none needed. Large tap targets (44 px or more), one question per screen on phones, a quiet progress line ("Step 3 of 8"). It should feel made by a careful publication, calm and plain. No brand chrome.

## Build and checks

- Folder `work/boards/phase-2/reader-check/`: a build script, the page `20261106_Reader-Check.html` with images in `img/` referenced by relative path (the main session publishes them as supporting files), the answer key `20261106_Reader-Check-Answer-Key.json`, captures.
- Stub `window.claude` locally to test both modes: a fake `use()` that returns a working in-memory db and user, and one that returns `null`. Walk the whole flow with Playwright at 390 and 360 px and at 1440 px in both modes, and save one capture per step at 390 px.
- Run `node work/build/scripts/phase-2/dataviz_check.js <page> --board` (install axe-core first: `cd work/build && npm install --no-save axe-core@4.10.2`) and fix what it flags, or say why a flag does not apply to a form page.
- Writing: the page's own words follow `CLAUDE.md` and chapter 02 (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`): short spoken sentences, no em dashes, no jargon a newcomer would trip on.

## Output

Notes at `work/handoffs/phase-2/20261106_Reader-Check-Notes.md`: what you built, your routine calls as proposed decision lines ("D2-xxx | decision | reason"), the answer key summary, a "Tested" list and a "Not tested" list kept apart, and a change log. Never touch `source/`, the ledgers, or any other board or concept folder. Do not commit or push.
