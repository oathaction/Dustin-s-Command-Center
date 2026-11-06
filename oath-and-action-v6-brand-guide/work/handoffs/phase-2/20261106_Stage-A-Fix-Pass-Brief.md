# Brief: stage A fix pass

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the main session for the four makers and the research lead. One fix pass takes all five stage A reports. Dustin approved every recommendation the studio put to him (DR-95 to DR-103), and the studio's routine calls are D2-248 to D2-258 (`work/ledger/20261020_Decision-Log.md`).

## Read first, in this order

1. `CLAUDE.md` and chapter 02's writing section, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`. It binds every word you write, in the guide and in your notes.
2. The decision log from DR-93 to D2-258. DR-93 defines nonpartisan: one standard of evidence and one way of describing sources, actors and parties, applied to everyone. Findings are reported as the record shows them, even when they fall more on one side. A fairness fix makes two descriptions equal; it never adds, softens or drops a finding to look balanced.
3. `work/handoffs/phase-2/20261106_Stage-A-Brief.md` (the content contract) and your own stage A notes.
4. All five reports, in full. Items are cited below by their own IDs:
   - Brand and evidence, `20261106_Stage-A-Red-Team-Brand-Evidence.md`: M1 to M6, S1 to S12 (cited as BE-M1, BE-S1)
   - Accessibility, `20261106_Stage-A-Red-Team-Accessibility.md`: AX-M1, AX-M2, AX-S1 to AX-S15
   - Craft, `20261106_Stage-A-Red-Team-Craft.md`: C-M1 to C-M7, C-S1 to C-S16
   - Civic education and plain language, `20261106_Stage-A-Red-Team-Civic-Plain.md`: CP-M1 to CP-M9, CP-S1 to CP-S19
   - Reader panel, `20261106_Stage-A-Reader-Panel.md`: must fix 1 to 5 and should fix 1 to 10 (cited as RP-M1, RP-S1)

## Dustin's answers and the studio's rulings, binding on every maker

- **Tracking (DR-95).** Title −3 percent, section −2.5 percent, H3 −1 percent, H4 −0.5 percent.
- **Hinge divider (DR-96).** Ampersand B's 24 px master at 24 px, centered on a 1 px line as wide as the text block it divides, with 12 px of clear line on each side of B, in the surface's ink. Shell and specimens alike.
- **Illustrative labels (DR-97).** One label at the head of a piece in which everything is invented. A label beside each item only where real and invented items mix. Use the shell's `<span class="illus">Illustrative</span>` and no other form.
- **H.R. 7008 (DR-98).** "H.R. 7008, the Stop Insider Trading Act". At its first mention in each chapter, state both provisions: it "would bar members of Congress, their spouses and dependent children from buying individual stocks, and would require photo ID to vote in federal elections". The tracker takes the bill's name. The May 2023 survey is a finding about a ban in general and is never tied to this bill's votes.
- **Rule 02.25 (DR-99).** "Our democracy is broken." is answered by a mechanism from the atlas that explains the claim and touches no campaign the editor works on (no ranked-choice voting, no primaries, nothing on Massachusetts Question 3's subject). The 23-states count moves to Rule 01.5's map with a full source line marked secondary and each state's limits.
- **Disclosure (DR-100).** The editor's disclosure leaves every page. A position piece's disclosure names who decided the position, the date, any funder interest, and links to the bios of those who decided it (D2-257).
- **Photographs (DR-101).** Public-domain U.S. government photographs from Wikimedia Commons, logged in the rights ledger. If none clears, Rules 01.6 and 01.8 move to chapter 16 with a link, and no box remains.
- **Partners (DR-102).** A partner's logo stays as drawn; "and" replaces a partner's ampersand only in copy we type. Co-branded pieces go to Dustin or an editor he names before they print or post. The host's name leads. The contact is "the editor", with no address yet.
- **Labels (DR-103, D2-249, D2-250).** Content labels: Explainer, Tracker, Analysis, Report, Guide, Act · How to take part, Our position. A newsletter issue carries none in its header; each story carries its own. A kicker is the content label, then at most one more part after a middle dot: the series name if the piece belongs to a series, otherwise the topic ("Explainer · Local schools"). A pillar name alone is never a kicker. A chart's "Finding" evidence line is the chart system's, sits above the title, and is not a kicker.
- **No codes (D2-253).** No decision code (DR-, D1-, D2-, G1-, T-, R9, R13, I6, I8, S5, S9), "Master Brief", "Phase", "Gate", "Board 5", "stage board", "the studio", "V5", "V4.2" or "Atlas V7" on any reader page, alt text included. Each Basis line gives its reason in words ("Design judgment", "Our measurements, October 2026", "Our locked identity rules", "WCAG 2.2 SC 1.4.3"). Keep codes in manifests and notes. Edition names: "our fifth edition" and "our fourth edition" after one full first use; the atlas is "our systems atlas".
- **Fixed artboards (D2-254).** Pieces up to 600 px wide use each style's phone floor: title 56, section 44, figure 48, H3 26, H4 20, quote 24, intro 19, ask 19, body 17, body small 15, UI 15, caption 14, label 13, data label 13. Pieces 1,200 px wide and up use the desktop ceiling: title 110, section 80, figure 104, H3 32, H4 24, quote 32, intro 22, the rest unchanged. Print pieces use points (D2-205). Any other size needs `check_exempt` "scale" with the reason in `notes`, allowed only on a labeled failure, a historical record or a print piece.
- **Approved chapter 02 text (D2-248).** W03, W07 and W20 keep their approved rewrites. Only H10's qualification changes, as an erratum (D2-256).
- **True size (C-S6).** Every specimen carries the `width_px` of the thing it shows, unless it is page text the shell should flow. A drawing at reduced scale carries `scale` (0.25 prints "One quarter size").

## New interfaces (the engineer builds them; makers write against them now)

| Where | Key | Meaning |
|---|---|---|
| Manifest | `readable: true` | Static table or list. The stage becomes a group named "<plate label>, specimen", its structure reaches assistive technology, and nothing claims interaction (D2-255) |
| Manifest | `interactive: true` | Only for specimens with controls |
| Manifest | `scale: 0.25` | The size line reads "One quarter size" |
| Manifest | `check_exempt` value `"scale"` | Off-scale type, with the reason in `notes` |
| Manifest | `fit_switch: true` | A wide comparison frame gets a "True size / Fit to window" switch, true size by default |
| Chapter JSON | `"groups": [{ "before_rule": "01.1", "number": 1, "title": "...", "line": "one sentence" }]` | The shell prints a rule-group block (hairline, number and title, its line) outside any mat, and a rule index after the intro that lists each group with its rules as links. Rules stay h3 |

Specimens never hold `<nav>`, `<article>`, `<header>`, `<footer>`, `<main>` or `<aside>`; use `div` (AX-S8).

## Round one, in parallel

Fix every item listed for you. Where you decline or change a fix, say why in your notes. Items that touch two owners are listed for both; each does their own part.

### Engineer (`.claude/agents/oa-engineer.md`): shell, build, checks, tokens

- Tokens: DR-95 in `work/build/tokens/src/oa-tokens.src.mjs`, and measure `figure` the same way (touching pairs at its size, by the craft report's method) and loosen it if it fuses; rerun `python3 -I work/build/tests/tokens/run_token_tests.py`. C-M3.
- Build: AX-M2 (unescape once in `img_inline()`), RP-M4 (font link and minus print `&` and `&minus;` once). RP-M3: every For builders Copy block gives working CSS, the part properties with their clamps and the four surface classes as `tokens.css` holds them, headed by a line saying `tokens.css` is the full source, and `tokens.css` offered as a download from the page. RP-S5: type chips show the range ("56 to 110 px") or the clamp.
- Shell: DR-96 hinge (C-M2), C-M4 rule heads, D2-251 appendix (C-M6: no rail from 1440 px, 24 px mat padding, `fit_switch`), D2-255 flags (AX-S2: `aria-hidden` on the hidden alt paragraph, every group named), AX-S1, AX-S3, AX-S4, AX-S6, AX-S7 (RP-S6), AX-S10, AX-S11, AX-S12, AX-S13, AX-S15 (cover pillars), C-S1 grid, C-S2 line weights, C-S3 caption measure and `text-wrap: pretty`, C-S4 tabular figures only on numbers, C-S5 rule foot, C-S6 size line with `scale`, C-S7 phone mat padding 16 px, C-S8 one Illustrative component never stretched, C-S9 contents and part opener read instruction lines from the chapter files, C-S10 and RP-S10 cover (one plain line on what the guide is for, build counts to the colophon, pillars kept whole, 24 px master on phones to match Rule 03.6, rail label), C-S11 and CP-S1 rule-group block and index, C-S16.
- Shell words: CP-S3 ("Coming later" for "later stage"; Files line as D2-252; the part opener without stage board words), BE-M5 and CP-M1 for every string the shell writes, colophon contact per DR-102.
- Checks in `guide_check.js`: fail any accessible name holding `&amp;`; fail a landmark or article element inside a stage; fail specimen type off the D2-254 sizes; fail any D2-253 word or code in reader text and alt text; keep the self-test planting each new fault and catching it.
- Publish the new keys and markup at the top of `20261106_Guide-Shell-Notes.md` first, so makers can preview.

### Editor (`oa-editor.md`): chapters 01 and 02

- BE-M1, BE-M2, BE-M3, BE-S1, BE-S2, BE-S3, BE-S4 (01.2, 01.3, 01.5: a "Failure case: do not publish" band inside each partisan failure stage, and in its alt), BE-S6, BE-S7 (as D2-257), BE-S9 (Rule 01.4's basis).
- AX-S8 (pieces and position cards as `div`), AX-S14 (01.24 and the 02 group alts), `readable` on every static table you own.
- C-M5 (02.22: grades as their own full-width table), C-M7 (sizes), C-S4 (02.22, 02.lines, 01.12), C-S6, C-S8, C-S11 (02's group openers and index become chapter `groups`), C-S15 (rule titles as instructions).
- CP-M2 (a "Words this guide uses" key after chapter 01's intro, "token" defined for the first time), CP-M3, CP-M5, CP-M6 and RP-M2 (one whole newsletter ending), CP-M8 and RP-M1 (Rule 01.21 under D2-250 and DR-103), CP-S1 (chapter 01 in groups), CP-S2, CP-S3, CP-S4, CP-S5, CP-S6, CP-S7, CP-S9, CP-S10, CP-S11, CP-S16, CP-S17 (keep Alder County out of any named state), CP-S18 (D2-256), RP-S1 (01.20's headline), RP-S7, RP-S9.
- DR-102 in Rule 01.24. DR-100: no disclosure anywhere in 01 or 02.
- Hold for round two, writing a placeholder note in your notes only: the research lead's checks on H.R. 7008, Rule 01.5's limits and the Senate vote, the DR-99 line, and the photographs.

### Identity designer (`oa-design-director.md`): chapters 03, 04, 08 and the proofs

- BE-M4 (letterhead PDF labels on both pages, rebuilt), BE-M5, BE-M6 and CP-M4 (04.3 headlines from 02.27's correct list; the Act card "The route plan & your commute."), BE-S8, BE-S9 (Rule 03.5's basis), BE-S11 (condensed minimums to the proofs), BE-S12 and RP-S1 (email deck without "Here is").
- AX-M1 (`readable` on `s-03-minimums`; all eight lockup minimums in Rule 03.2's specifications), AX-S5 (the composer fills its column), AX-S8 (03.6 nav as `div`), AX-S9, AX-S14 (`s-proofs-glance`: all three width pairs in its alt), AX-S15 (composer `aria-describedby`).
- C-M2 (Rule 04.4's specifications say where B sits and what the line spans; plates per DR-96), C-M6 (D2-251: one comparison specimen per pair, avatars and emails side by side, mastheads, social cards and letterheads stacked on a shared left edge, `fit_switch` on the wide ones), C-M7, C-S6, C-S7 (cards and pairs reflow under 568 px; the lockup sheet as two columns at 712 px with L6 on its own row), C-S8, C-S9 (curly quotes through the editor's quote helper), C-S12, C-S13, C-S14, C-S15.
- CP-M1, CP-M9 and RP-S8 (stage names glossed in the legend; 04.4's "reports the bill out" glossed), CP-S2, CP-S3, CP-S14, CP-S17 (rename the letterhead's town so it cannot be joined to Alder County), CP-S19 (a phone-width tracker list beside the true-size plate), and the letterhead's "We are writing to ask" opener.
- RP-S3 with DR-102 (print values in points and x; order; Rule 03.3 says the partnership hairline belongs to the lockup; squares use L8 beside the partner), RP-S4 (a short spec list under the social card; the appendix names Dustin where it says "you choose"), RP-S5 (Rule 03.6 in em: "from 48em, 768 px at the default text size"), RP-M1 (every kicker in your specimens per D2-250).

### Systems designer (`oa-design-director.md` with `oa-ux-accessibility-lead.md`'s checks): chapters 05, 06, 07

- BE-M5, BE-S4 (05.7's failure band), BE-S5 (a hinge divider and 24 px of Newsprint between the Prussian panel and the red ask, or the panel in Charcoal), BE-S10 (one count, or say what each counted).
- AX-S2 (`readable` on your static tables, each with a plate label), AX-S14 (05.7's measured ratios in its alt and specifications).
- C-M2 (the phone pages in 05.1 and 05.3 per DR-96), C-M3 (re-measure Rule 06.4's plates at DR-95's values), C-M7 (the fixed-artboard column in Rule 06.2 as D2-254 sets it), C-S6 (07.2 and 07.3 grids carry `scale`), C-S15.
- CP-M1, CP-S8 ("eyebrows" becomes "kicker"), CP-S9 (breakpoint, em, Dim Newsprint at first use, "diverging pair B" in plain words), CP-S10, CP-S12, CP-S13, CP-S15, D2-248 (06.8 and 07.5 sample text), RP-M1 (kickers per D2-250).

### Research lead (`oa-research-lead.md`): checks and photographs

Write `work/handoffs/phase-2/20261106_Stage-A-Fix-Pass-Research.md`. Congress.gov and senate.gov refused automated reading earlier; try primary alternatives (govinfo.gov, clerk.house.gov, the Senate's roll call XML), respect any refusal, and say what you could and could not open.
1. H.R. 7008: its official title, what its stock section bars, whether it carries the photo ID section, the House roll call and the Senate cloture vote (Vote 253, 53 to 47 in the atlas). Give each claim its grade under H08.
2. The 23-state initiative count with Mississippi's, Illinois's and Florida's limits, checked against the state constitutions or the National Conference of State Legislatures, and the full source line Rule 01.5's map should print.
3. California Proposition 50 and the 2025 Texas map: who drew each, what each aims at, the dates, in one form for both.
4. The number of states whose voters elect utility commissioners.
5. How the National Bureau of Economic Research paper by Anna Stansbury and Lawrence Summers and the Economic Policy Institute describe their authors, so Rule 01.16 can describe both by role and affiliation in one form.
6. DR-99: two or three candidate mechanisms from the atlas export (`work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json`) that explain "Our democracy is broken.", each with its grade and record ID, none touching ranked-choice voting, primaries or Massachusetts Question 3's subject (find and state that subject).
7. Photographs for Rules 01.6 (a documentary photograph of a capitol or other government building as the place where a named public event happened) and 01.8 (people doing public work, officials among them, with who, what, where and when knowable). Wikimedia Commons, public domain as works of the U.S. federal government, with the file page's license read and quoted. No partisan figure as the subject. Download two or three candidates per rule to `work/build/assets/photography/` with a JSON beside each (source URL, author, agency, date, place, license line, and a caption that names who, what, where and when). Append a row for each to `work/research/20261020_Rights-Ledger.md` in its existing form.

## Round two (after round one)

The editor copy edits all eight chapters, starting from the ten cross-chapter issues in its stage A notes, and applies the research lead's findings: the H.R. 7008 grade, Rule 01.5's source line, Rules 01.11, 01.13 and 01.16, the Senate vote line in our own voice, the DR-99 row, and the photographs in Rules 01.6 and 01.8 (cropped and captioned as those rules say). For copy in chapters 03 to 08, the editor changes the string in the owner's chapter JSON or build script (`stage_a_identity_*.py`, `stage_a_systems_*.py`) and reruns that script; generated HTML is never edited by hand.

## Checks before you hand back

- Your own build script, then `python3 -I work/build/scripts/phase-2/guide_build.py`, then `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`. Other makers rebuild the same page while you work; if the build fails in a file you do not own, wait a minute and rebuild. The main session runs the final build.
- Look at your chapters at 1440 and 390 px, at twice size where detail matters.
- npm: `cd work/build && npm install --no-save axe-core@4.10.2 style-dictionary@5.8.0`, both together, never one alone.

## Notes and limits

Add a "Fix pass" section to your stage A notes (the research lead writes its own file): each item ID and what you did, your routine calls as proposed "D2-xxx | decision | reason" lines, questions for Dustin with a recommendation (only where a fix truly needs him), "Tested" and "Not tested" kept apart, and a change log. Never touch `source/`, `work/ledger/`, the Civic Line or identity masters, another maker's files (except the editor's round-two copy edit as described), or any existing board. Do not commit or push.
