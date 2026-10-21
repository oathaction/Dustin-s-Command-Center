# Gate 1 report: research, strategy and direction

Oath & Action Brand Guide, Edition 06. Phase 1, October 21, 2026. Status: stopped at Gate 1, waiting for Dustin's approval.

Open the review board: `work/boards/20261021_Gate-1-Review-Board.html`, also published as a private page at GATE1_URL. It puts each decision beside the drawings it needs. The five detailed boards behind it sit in `work/boards/`:

- `20261021_Strategy-And-Direction-Board.html`
- `20261021_Identity-Refinement-Board.html`
- `20261021_Symbol-Family-Board.html`
- `20261021_Systems-Marks-Board.html`
- `20261021_Navigation-And-Template-Wireframes.html`

## What you are asked to approve

Phase 1 ends with 37 decisions. The studio can recommend most of them. Seven change what the brand looks like or what it says, and those seven are yours alone.

1. **The seven big calls** in section 4. Answer each one.
2. **Six identity changes** in section 5. Each changes identity geometry, so the studio rules ask for your approval by name. Five are repairs or small-size masters. S9 is a new mark, the wordless badge, and it comes with three conditions.
3. **Twenty-two studio recommendations** in section 6, approved as a set. Name any you would change.
4. **The Phase 2 proposal** in section 9.

A reply can be this short: "Big calls: 1 B, 2 yes, 3 V2, 4 adopt and D, 5 A, 6 B and no role, 7 yes. Fixes: approve I1, I2, I3, I7, I8. S9: yes, with its conditions. Set: approved except M2. Phase 2: go."

Section 10 has four new questions only you can answer. Each has a default the studio follows until you do.

## 1. What was done

| Step | Who ran it | Output |
|---|---|---|
| Master Brief V2 issued with the Gate 0 corrections and your decisions DC-01 to DC-10 | Main session | `brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md` |
| Research: civic and design benchmarks, common-ground formats, the font license position, trademark notes, condensed faces, corrections to the brief. Rights review of `pics_i_like.pdf` and the four mockups | Research lead | `work/research/20261021_Research-Ledger.md`; `work/handoffs/phase-1/20261021_Research-Summary.md`; a dated addendum in the rights ledger |
| Strategy: the hinge as the organizing idea, brand architecture, the Act pattern, twenty nonpartisan rules, what to take from your references | Creative director | Strategy board; `20261021_Brand-Strategy.md` |
| Three voice line revisions, the candidate lines, a headline and instruction line for every chapter | Editor | `20261021_Voice-Line-And-Headlines.md` |
| Ten identity refinements, each drawn beside V5 at 16, 24, 48 and 96 px and at display size | Design director | Identity board; `20261021_Identity-Refinement-Notes.md`; SVG proposals in `work/boards/phase-1/identity/` |
| Pillar marks in two directions, four sample topics, the treatments map, craft checks, a composite Act post | Design director | Symbol board; `20261021_Symbol-Family-Notes.md` |
| Systems marks built on Atlas V7's own records, the atlas bases, a 27-item V7.1 issue list | Data visualization and systems lead | Systems board; `20261021_Systems-Marks-Notes.md`; `20261021_Atlas-V7-1-Issue-List.md` |
| Guide architecture of six parts and 28 chapters, navigation at desktop and phone, the chapter template applied to 05 Color | UX and accessibility lead | `work/ledger/20261021_Guide-Architecture-Map.md`; wireframe board; guide shell |
| Token architecture and a draft token file of 157 tokens | Engineer | `work/ledger/20261021_Token-Architecture.md`; `work/build/tokens/20261021_Token-Schema-Draft.json` |
| Review of every word on every board | Editor | `20261021_Editor-Review-Of-Phase-1.md` |
| Rubric review, cross-board conflicts, the red rule | Creative director | `20261021_CD-Review-Of-Phase-1.md` |
| Fix round on all five boards and their notes | Each maker, resumed with the reviews | The boards and notes above |
| Re-check and re-score after the fixes. It found four defects that would have misled you | Creative director | `20261021_CD-Recheck-After-Fixes.md` |
| Final fix pass on those four defects, the red rule's wording and one set of chapter instruction lines | Each maker, resumed; the editor and UX lead for the instruction lines | The boards and notes above |
| Final check of the four defects, and the rubric scores in section 3 | Creative director | `20261021_CD-Final-Check.md` |
| This report | Main session | This file |
| The combined Gate 1 board, built by script from this report | Engineer | `work/boards/20261021_Gate-1-Review-Board.html`; builder `work/build/scripts/phase-1/build_gate1_board.py` |

How the agents ran: as in Phase 0, each studio agent ran as a general-purpose subagent briefed to read and adopt its role file in `.claude/agents/`. The main session wrote Brief V2, routed the reviews and fix rounds, ran the checks marked as its own in section 2 and wrote this report.

## 2. Verification

**Tested**

- Each maker rendered its board in Chromium at 1440 and 390 px after the fix round. None scrolls sideways and none sets text under 13 px.
- The systems board passed axe-core 4.10.2 with the WCAG 2.2 AA rules at both widths, with no violations. Its 438 chip cells measure 9.42:1 or better.
- Symbol craft checks: Direction A passes 86 and fails 10, Direction B passes 85 and fails 11. All 161 numeric cells use tabular figures.
- Identity craft checks: silhouette at 16 px, pixel fit of the 16 and 24 px masters, overshoot, one color on all four surfaces, and hinge diagram lines at 3:1 or better.
- Tokens: 157 tokens with 0 failures, and the rule test caught all 11 deliberately broken copies. All 21 contrast values in the brief's palette table match the WCAG formula to two decimals.
- Architecture: a script found a home in the map for every V5 Polished section and h3, and for every V4.2 section.
- The main session's own checks after the fix round. Dotted and dashed lines appear only on the systems board, where V7's evidence code needs them. The red rule appears word for word on the identity, strategy, symbol and systems boards and in the guide shell. The systems board recommends Rule NN.n and holds Std-01. The headline table's chapter numbers match the architecture map.
- The creative director's re-check: every board re-rendered at 1440 and 390 px, the seven required changes traced, and the working reds counted per view (section 3).
- The creative director's final check after the last fix pass. A pixel audit with every panel open finds red touching Prussian only in the identity board's two cells labeled "V5 today", which you need to see beside option D. Path data shows ampersand B, or the narrow B, as the only ampersand in all four composite posts. Text scripts find D1-26's wording verbatim on every board and in the map, the shell, the notes and this report, and the same 28 instruction lines in the map, the shell, the wireframes and the editor's table.
- The combined Gate 1 board, built from this report: no horizontal scroll at 1440 or 390 px in light or dark, every image loads, no text under 13 px, one h1 with no skipped heading levels, axe-core 4.10.2 with the WCAG 2.2 AA rules finds no violations, and no red appears outside the specimens.

**Not tested**

- Readers. No board has been shown to anyone outside the studio. The Act mark at 16 px, the effect marks and the voice line wait on that (Q-13).
- Screen readers, Firefox, Safari, Windows, macOS, high-density screens and print.
- Page reads. This environment still blocks every site except Google Fonts, so research rests on 97 searches of official domains, and every quote is marked as a search snippet until someone reads the page (section 8).
- Trademark searches.
- Ampersand B against commercial serif ampersands. The similarity check covered only the fonts installed here.
- The token format pages themselves, since the fetch failed.

## 3. Rubric scores

Master Brief V2 section 6 sets the ship threshold at 4 on each criterion: Cr craft, Cl clarity, BF brand fidelity, U usefulness, EH evidence honesty, A accessibility. These are the creative director's final scores after the fix rounds (`20261021_CD-Final-Check.md`). Seven rows stay under 4. Each says why it still comes to you.

| Proposal | Cr | Cl | BF | U | EH | A | Reason for the lowest score |
|---|---|---|---|---|---|---|---|
| Strategy and narrative | 4 | 4 | 4 | 4 | 4 | 4 | The house-format source was read through search results only |
| Act pattern | 3 | 4 | 4 | 4 | 5 | 4 | Under 4: the mocks are board sketches at no true ratio. They go to Dustin as a pattern, and Phase 2 rebuilds them in tokens |
| Voice line, revision B | 4 | 4 | 4 | 4 | 4 | 4 | Echoes the reader promise; untested with readers |
| Identity 1, re-export | 5 | 5 | 5 | 5 | 5 | 4 | Lockup taglines stay small until item 9 |
| Identity 2, hinge gaps 2b | 4 | 4 | 5 | 4 | 5 | 4 | The equal-area model is a design judgment no reader has tested |
| Identity 3, wordmark masters | 4 | 4 | 4 | 5 | 5 | 4 | The larger small-size ampersand reverses a V5 measure |
| Identity 4, ampersand A | 4 | 4 | 5 | 4 | 5 | 4 | Stays a stock glyph |
| Identity 5, ampersand B | 4 | 4 | 4 | 4 | 5 | 4 | First drawing, 0.77 overlap with Lora |
| Identity 6, condensed | 3 | 4 | 3 | 4 | 5 | 4 | Under 4: a squeezed Inter Tight that changes locked proportions. It goes to Dustin as a request for one drawing pass, with today's width in force |
| Identity 7, hinge diagram | 4 | 4 | 4 | 4 | 5 | 4 | The circle and return arc are new to V5, and the masters still carry V5's glyph while B leads |
| Identity 8, lockmark masters | 5 | 4 | 4 | 5 | 5 | 4 | The larger lever reverses a V5 rule |
| Identity 9, minimum sizes | 4 | 4 | 5 | 5 | 5 | 4 | The 13 px tagline floor pushes the L4 to L6 minimums up sharply |
| Identity 10, Prussian D | 4 | 4 | 4 | 4 | 5 | 5 | Gives up the red ampersand of Dustin's Prussian banner |
| Composite Act post | 4 | 4 | 4 | 3 | 5 | 4 | Under 4: a demonstration with no type sizes, tokens or export. It goes to Dustin so he can judge one identity, and Phase 4 builds the template |
| S9 hinge-circle badge | 4 | 4 | 3 | 4 | 4 | 4 | Under 4: Rule 05.3 does not name it yet, and at 24 px it scores 0.608 against the seal. A new mark needs Dustin's named approval |
| Symbols, Direction A | 4 | 4 | 4 | 3 | 5 | 4 | Under 4: no exports, and 16 topics undrawn. Phase 2 draws them if Dustin picks A |
| Symbols, Direction B | 3 | 3 | 3 | 3 | 5 | 3 | Under 4: line masters fail at 16 px. It is shown for comparison and not recommended |
| Systems 1, evidence lines | 4 | 4 | 5 | 4 | 5 | 4 | The record square needs V7.1 |
| Systems 2, grade words | 4 | 4 | 5 | 4 | 5 | 4 | Untested with readers |
| Systems 3, typed chips | 4 | 4 | 4 | 4 | 5 | 4 | Untested with readers, and Rule NN.n waits on T2 |
| Systems 4, effect mark | 4 | 4 | 5 | 4 | 5 | 4 | Untested with readers |
| Systems 5, event mark | 4 | 4 | 4 | 4 | 5 | 4 | Four shapes need a key on every figure |
| Systems 6, authority and delay | 4 | 4 | 4 | 4 | 5 | 4 | Untested with readers |
| Systems 7, hinge primer | 4 | 4 | 4 | 4 | 5 | 4 | Reuses a hinge that still carries V5's glyph; untested with readers |
| Systems 8, atlas bases | 4 | 4 | 4 | 4 | 5 | 4 | The changes exist only as text |
| Architecture and navigation | 4 | 4 | 3 | 5 | 5 | 4 | Under 4: with the wordmark covered, the shell could be any documentation site. It goes to Dustin for its structure, and Phase 2 item 4 marks the parts and sets the hinge divider |
| Token architecture | 4 | 4 | 4 | 4 | 4 | 4 | The DTCG specification pages are still unread |

## 4. The big calls

| # | Call | IDs | Options | Studio recommendation |
|---|---|---|---|---|
| 1 | The ampersand | I4 (L) | V5's Lora glyph; A, V5's glyph tuned, with true small masters; B, a drawn ampersand of Oath & Action's own | B as the direction, A as the fallback |
| 2 | The wordmark's width | I5 (L) | Phase 2 draws a condensed wordmark at 7.5 to 1 for a final choice at Gate 2; keep today's width and stop | Draw it, with today's width in force until Gate 2 |
| 3 | The hinge diagram | I6 (L) | V5's dotted arc; two-way dashed arcs, as in your mockup; V2 with solid arcs running clockwise; V2 without the return arc | V2 with solid arcs, running clockwise, with the five separation rules |
| 4 | Red's job, and the ampersand on Prussian | I10; I9 (L) | Adopt the red rule as Rule 05.3, or keep each board's wording. On Prussian: B, Newsprint; D, White. The rule rules out A, red at display size, and C, red with a keyline | Adopt the red rule, and D |
| 5 | The pillar marks | Y1 | A, geometric solid; B, line with one accent | A |
| 6 | The brand lines | S3; S4 | Voice line: keep V5's, or A, B or C. "From spectators to stewards.": no role, recorded in 01 Purpose; membership and events only; lockups (L) | Revision B, and no role |
| 7 | Position pieces | S6 | Two labeled Act kinds with the fairness kit; positions without the kit. Label: "Our position", "Opinion" or "Position: Support" | Two kinds with the kit, labeled "Our position" |

**L** marks a change to a locked element or identity geometry. V5 stays in force for each one until you approve it by name.

### 1. The ampersand

V5 sets Lora Bold's ampersand, a free font's glyph anyone can type. Option A tunes that glyph and adds true 16 and 24 px masters. Option B is drawn: one self-crossing pen path, with a beak serif and a tail whose foot sits on the baseline. Its silhouette overlaps Lora Bold's at 0.77, so a reader still knows it, and no free font sets it. The research lead found that a trademark filing in special form protects the drawing filed, so a drawn ampersand gives Oath & Action a shape it can protect. A trademark attorney has to say how far that goes (Q-12).

B is a first drawing. Phase 2 would raise its stroke contrast from 1.5 to 1 toward 1.7 to 1, set its crossing on the hinge diagram's center line, refine it at twice size, proof it in print and check it against commercial serif ampersands. A is the fallback if B fails any of those.

### 2. The wordmark's width

Your logo-system references use a condensed heavy wordmark. The design director drew one from Inter Tight 800's own capitals. At 7.5 to 1 it stands 1.26 times taller in the same width, and its A stays open at 16 px. The creative director scores it under threshold. It reads as a squeezed Inter Tight, about 25 percent wider than the references it answers, and close to campaign-sign lettering.

The studio recommends one proper drawing pass in Phase 2, so that you choose between finished drawings at Gate 2. It costs double work, because Phase 2 then draws the main lockups at both widths. If you don't need the extra height, say no and Phase 2 skips it.

### 3. The hinge diagram

Atlas V7 draws a hypothesis as a dotted line and a plausible link as a dashed one. V5's hinge arc is dotted and your mockup's arcs are dashed, so to an atlas reader either one would say the brand is a guess. V2 follows your mockups: the ampersand in a circle, OATH and ACTION on a line with four nodes, two solid hairline arcs running clockwise, and UNDERSTAND and IMPACT beneath. Five rules on the systems board keep it apart from data marks. The identity board also draws V2 without its return arc. Under the red rule's wording in call 4, the hinge diagram is an identity mark of its own, so it never shares a view with the wordmark. A piece that needs the hinge beside the wordmark uses the hinge divider. The V2 masters still draw V5's ampersand, and they take whichever ampersand you choose in call 1. The display master holds 13 px labels from 526 px wide, and the compact master drops the labels and works down to 241 px.

### 4. Red's job, and the ampersand on Prussian

The creative director found red's job written five ways across the boards, and the Act mocks spent two reds in one view. One rule replaces all five. It would be Rule 05.3, in 05 Color:

> The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither does the ampersand inside the hinge diagram, which is an identity mark. The hinge diagram never shares a view with the wordmark and never stands in for the hinge divider. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline's ampersand uses the view's working red. The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. The Act handle is red only when the Act mark is itself the call to act, as on a social tile. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian.

The re-check after the fix round tested this wording on every board and found four cases it left open: the divider's ink on dark surfaces, the hinge diagram's own ampersand, a reform with several targets, and the guide's own failure cases and swatches. The four sentences that settle them are part of the wording above.

On Prussian, V5's red ampersand measures 2.27:1 at 16 px. White measures 8.27:1 there and 13.28:1 at 96 px. The rule's last sentence rules out options A and C, which leaves B and D, and the studio recommends D for identity marks.

If you approve the badge (S9, section 5), the rule's first sentence becomes: "The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither do the ampersands inside the hinge diagram and the hinge-circle badge, which are identity marks."

One case is yours to settle. The rule ranks the step a reader can take now above the point the headline names, so on an Act piece the step takes the red and a hinge headline's ampersand cannot. Post 4 of the composite shows the other order, with the headline's ampersand red and the Act handle in Charcoal. Until you choose, the rule stands as written and post 4 is an exception for you to judge. If you want hinge headlines to carry red on Act pieces, say so, and the rule gains a sentence giving the headline's ampersand the red before the step. Data graphics on Prussian keep Newsprint. The cost is that red appears less often than in your mockups, and the Prussian banner loses its red ampersand.

### 5. The pillar marks

Direction A is a geometric solid, drawn from icon study 06 and the filled references you shared. Direction B is a line with one accent, from study 08. Both share one skeleton and one node, the same node that sits in the lockmark and the hinge diagram, with red on the node that acts. B's line masters fail at 16 px. The studio recommends A, with a line companion from 24 px up (Y4). A's Act mark at 16 px reads close to "01" or a D, so Phase 2 tests it beside chapter numbers.

### 6. The brand lines

You made the voice line editable (DC-04). V5's line, in force until you approve a change: "We explain the rules. We expose the gaps. We connect people to action. We act." The editor recommends revision B: "We'll explain the rules and track what happens to them. When a decision is coming, we'll connect you with the people making it, so you can act in time." It splits at the hinge, with the commitment (Explain, Track) first and the action (Connect, Act) after. It drops "expose the gaps", which assumes a wrong to uncover, and hands Act to the reader. Revisions A and C are on the strategy board.

V4.2 lists "From spectators to stewards." as the historical tagline, "Retired from current applications." Your references use it throughout. The editor and creative director recommend no brand-line role. Its turn from one word to the other lands as a slogan, "steward" is rare in everyday speech, and it casts the reader as a spectator. 01 Purpose would record it as the founding line. If you want it in use, its narrowest role is membership and events, never in a lockup and never beside a position piece.

### 7. Position pieces

You allowed Act pieces to take a labeled position (DC-01). The strategy sets two kinds. A process piece gives a step with a date and a place and takes no side. A position piece supports or opposes a named measure and carries the fairness kit:

1. "Our position" comes first, before the headline, and the disclosure repeats above the ask.
2. "The strongest case against" gives the opposing case as its supporters would put it, with sources, at no less than a third of the argument's length.
3. Every claim keeps its evidence grade, and the verb matches the grade.
4. Opponents are described by office or role, never by party as a villain.
5. "What we don't know" names the open questions.
6. Process facts match the neutral tracker word for word.
7. The disclosure names who decided the position, the date and any funder interest, and a public position log lists every position.
8. Positions never appear in the atlas, the trackers or the data.

Each position piece puts the nonpartisan standing at stake, and the kit adds writing and editing time to every one.

## 5. Identity changes to approve by name

Five repairs or small-size masters, and one new mark.

| ID | Fix | What changes | Why |
|---|---|---|---|
| I1 | Re-export the six clipped symbols | The amp, two-line and one-line taglines, URL and stacked symbols get boxes that hold all their ink. Outlines and origins stay | V5 clips their edges (defect fix) |
| I2 | Hinge gaps by equal white area (2b) | The ampersand moves 1.42 units toward ACTION. Both gaps hold 0.205 cap heights of white, and the width holds | Under V5's nearest-ink rule the right gap holds 1.24 times the left's white (defect fix) |
| I3 | Wordmark masters at display, 24 and 16 px | Optical spacing, stems and bars on whole pixels, and the ampersand at full box height at the two small sizes | V5 scales one master down, and its small sizes blur. The larger small ampersand reverses a V5 measure |
| I7 | Lockmark masters at 16 and 24 px | Node centers on whole pixels, with a larger lever. Thresholds: 16 px master to 23 px, 24 px master to 47 px, V5's master from 48 px | At 24 px, V5's lockmark has 5 percent solid ink. The master raises it to 60 percent. The larger lever reverses a V5 measure |
| I8 | One minimum-size rule | No mark draws capitals under 14 px on screen and no tagline sets under 13 px. Each lockup names its replacement below its minimum. Favicons use the ampersand's 16 px master | V5's minimum sizes conflict (defect fix) |
| S9 | A wordless hinge-circle badge, a new mark | Ampersand B in the hinge diagram's ring, with no words, taking the ampersand you choose in call 1. Signature red on Newsprint, White and Charcoal, White on Prussian. Three conditions: Rule 05.3 names it as signature red (the added sentence is under call 4), or it goes Charcoal; it keeps to its jobs, an end mark, a report's back cover and events, and never appears as an avatar or favicon, near a candidate or ballot, or beside the wordmark or the hinge diagram; and Phase 2 redraws its 16 px master from ampersand B's | Your references show seals, and V5 says "Seals imply an authority we do not claim." A badge without words claims none. Against a generated seal it scores 0.584 at 16 px, under the studio's 0.60 similarity limit, and 0.608 at 24 px, over it. No reader has tested it. Drawn on the symbol board, section 12 |

I3 and S9 carry whichever ampersand you choose in call 1.

## 6. Studio recommendations, approved as a set

| ID | Question | Recommendation |
|---|---|---|
| S1 | Should the hinge, a promise and then the action that keeps it, organize the system? | Yes, as the strategy board writes it |
| S2 | One masterbrand with plain product names, and "Dispatch from the Front" renamed "Dispatch"? | Yes to both. V5's kicker already says "Dispatch", and a front is a war metaphor |
| S5 | What role does "Democracy has a structure." take? | It explains the lockmark in 08 The Signal Grid and on the About page |
| S7 | Adopt the twenty nonpartisan rules? | Adopt them as Rules 01.1 to 01.20 in 01 Purpose, with Rule 01.1 "Red never marks a party, a side or a person." The red rule keeps its home as Rule 05.3 in 05 Color, and 01 cites it |
| S8 | Which house format for "you & me" pieces? | The strongest arguments for and against, then each party's majorities side by side, sourced, as the Program for Public Consultation does |
| S10 | What is the photography default? | Black and white, with color where color is evidence. Labeled placeholders until photography is settled |
| Y2 | Approve the four skeletons and the shared node? | Yes, with the node. Raise Track, and test Act at 16 px |
| Y3 | Where does red go in the pillar marks? | The Act handle only, under the red rule |
| Y4 | Where does the line companion start? | 24 px |
| Y5 | Redraw all twenty topics in Direction A's grammar? | Yes, in Phase 2, with a vote cue on Ballot |
| Y6 | Approve the treatments map, with patterns behind content? | Yes, at 12 percent ink or less, with no lit nodes |
| M1 | Which evidence line code? | V7's code, plus a record square and a hollow line |
| M2 | Which grade words? | V7's words as labels, each with a plain gloss in keys and at first use |
| M3 | How do atlas IDs appear? | A two-part chip with the full type word, and guide rules cited as Rule NN.n |
| M4 | Adopt the effect, event, authority and delay marks? | Adopt all four |
| M5 | Which atlas bases? | Confirm Concepts 03, 09 and 11, revise 10, and add 07 Loop Card with 04's record panel |
| M6 | Release the V7.1 issue list? | Yes, all 27 items, for the atlas editor |
| T1 | Six parts and 28 chapters as mapped? | The architecture map |
| T2 | Chapter numbers, anchors and rule IDs? | Chapters 01 to 28, word anchors, V5 anchors kept as aliases, Rule NN.n |
| T3 | Navigation, template and interaction? | As proposed on the wireframe board |
| T4 | Derived colors? | Mixed in OKLab. Deep Stone at 18 percent (#4E535B, 5.49:1 on Newsprint). Adopt Dim Newsprint and Error Band |
| T5 | The rest of the token architecture? | As proposed, including the red rule with keylines and no derived red (T-6) and the ask button's White label at 19 px bold, 4.17:1 (T-7) |

## 7. Risks

- "From spectators to stewards." with no role cuts against your references, which use it throughout.
- Under the red rule, red appears less often than in your mockups.
- A condensed drawing pass means Phase 2 draws the main lockups twice.
- Each position piece puts the nonpartisan standing at stake.
- Pillar Red on Newsprint measures 2.96:1 at best. It marks and fills, and small text never sets in it. The 1 px Charcoal edge stays wherever red carries meaning. WCAG exempts logotypes.
- Ampersand B is a first drawing. If the refinement pass fails, Phase 2 falls back to A and loses that time.
- Quotes and award details stay unverified until someone reads the pages.
- Braver Angels had to rename in 2020 after a trademark settlement. Oath & Action has no clearance search yet.
- No proposal has been tested with readers.

## 8. Research: findings, corrections and what still needs page access

**What matters most** (full detail in the research summary):

- A mark can carry the brand idea when the brand teaches it. The 19th explains the asterisk in its logo, and GOV.UK's 2025 refresh made the dot between GOV and UK the joint of its wordmark. So 04 should explain the ampersand in plain words where a reader first meets it.
- Common ground works best as something a reader can try. The Program for Public Consultation, More in Common's Perception Gap Quiz, Stanford's America in One Room and Pew's 2026 typology each do it differently. S8 picks one as the house format.
- Balance can be written down. Ballotpedia's neutrality policy and Braver Angels' equal-representation rule give the editor tested wording for the nonpartisan rules.
- Artwork made with an OFL font is not subject to the font's license, so a logo built from Inter Tight and Lora outlines is sound, and so is a drawn ampersand. A font file built around it would have to stay under the OFL with a new name.

**Corrections to Master Brief section 5.** Sigma 2026's "Invisibles" concerns older adults excluded from Peru's main social protection program by an automated poverty classification. The Urban Institute calculator uses 2016 rules. Bloomberg's "What's Really Warming the World?" is now verified on bloomberg.com. GovTrack has posted "Ending GovTrack's bulk data and API" (title seen only), so no data pipeline should depend on it.

**Your references drift from the record.** The atlas mockup on page 24 of `pics_i_like.pdf` says "740 sources" where V7 gives 1,099 unique sources. The atlas home page on page 52 shows 50 variables and 117 connections where V7 gives 51 and 118. Several boards repeat an unsourced "12.4M". The studio uses the references for direction only.

**Erratum.** Two Phase 0 statements were wrong, and change ledger C-004 corrects them. Atlas V7's 1,099 sources are unique sources, and row 40 of the reconciliation table misnamed V7's weakest step for U.S. services. The Gate 0 report stays as issued.

**Thirteen claims are unverified**, listed in the research summary. Most need one page read each.

**Page access.** The environment's network policy still refuses every host except Google Fonts, and page fetches fail with a lookup error. Phase 3 needs it most, because its chart specimens use public data. You change it in the environment's settings: open the cloud environment menu in the session's title bar, choose Edit, then Network access. Pick a broader access level, or add the hosts under Allowed domains with the package managers box left ticked. The steps are at https://code.claude.com/docs/en/cloud-environments#network-access. For Phase 3 the studio would add designtokens.org, openfontlicense.org, uspto.gov, census.gov, bls.gov, fec.gov, congress.gov, data.gov, pewresearch.org and the benchmark sites in the research ledger (Q-11).

## 9. Phase 2 proposal

**Phase 2 produces**

1. Sixteen chapters in `work/build/`, numbered by the architecture map: 01 Purpose, 02 Voice, 03 Identity, 04 The Ampersand and the hinge, 05 Color, 06 Type, 07 Layout and spacing, 08 The Signal Grid, 09 Pillar marks, 10 Topic and atlas symbols, 11 Status and utility icons, 12 Graphic devices and patterns, 17 Motion and states, 18 Components and interaction, the rules of 19 Accessibility, and 26 Tokens and how to choose them.
2. Vector masters in `work/build/assets/` for each approved refinement, at 16, 24 and 48 px where useful: the wordmark, the ampersand, the lockmark, the hinge diagram, the four pillar marks, twenty topic symbols, atlas symbols drawn from V7, status marks, the systems marks as encoding glyphs, utility icons, and graphic devices, V4.2's watermarks among them.
3. `tokens.css` and `tokens.json` generated from one source, with the parity test.
4. The guide shell, with each part marked by its pillar mark and the hinge divider set between each rule and its correct use. The creative director found the current shell could belong to any documentation site.
5. A preview build of these chapters as one HTML file in `work/boards/`.
6. The Gate 2 report, with before and after boards for each approved refinement, the icon craft checks, similarity sheets, contrast output for every token on every surface, the token parity test, and screenshots at 1440 and 390 px with keyboard and reduced-motion checks.

**What your answers set in motion**

- If you approve ampersand B, its refinement pass, print proof and commercial check come first, since every lockup carries the ampersand. If B fails one of them, the studio tells you at once and moves to A.
- If you approve the condensed pass, the C, N and A get redrawn, B gets a narrow 16 px master, and the hinge diagram's OATH and ACTION get a condensed drawing. The main lockups come to Gate 2 at both widths.
- If you approve Direction A, the four marks get one node-to-stem ratio, Track is raised, and the Act mark is tested beside chapter numbers at 16 px before the twenty topics are drawn.
- If you decline any refinement, V5 stays in force for that element and Phase 2 builds its chapter on V5.

**Order.** The first step records your decisions and updates the Phase 2 and Phase 4 prompts to the map's chapter list (D1-11). Identity masters and tokens start together. The pillar marks follow the ampersand and node decisions, then the topics, atlas symbols and icons. Components and the shell run beside them. The editor writes each chapter against the template, the engineer builds the preview, and the creative director scores everything before Gate 2.

**You decide at Gate 2:** the wordmark width, if Phase 2 draws the condensed one; ampersand B as refined; the twenty topic symbols; and the Phase 3 proposal, with the three items already scheduled there: the diverging palette's hue pair, Atlas V7 data in place of illustrative chart specimens, and tracker examples as real bills or as inventions labeled beside the item.

**Phase 2 does not** build data visualization, systems graphics or applications, and it ships no reference or generated image.

## 10. Questions only you can answer

These are added to `work/ledger/20261020_Open-Questions.md`.

| # | Question | Why it matters | Default until you answer |
|---|---|---|---|
| Q-11 | Can the environment's network access be widened before Phase 3? | Research can't read pages, and Phase 3 can't download public data | Search only. Quotes stay marked as snippets, and chart specimens use Atlas V7 data |
| Q-12 | Will a trademark attorney run clearance on OATH & ACTION, the monogram and a standalone ampersand before launch? | The drawn ampersand's value depends on it, and Braver Angels had to rename after a settlement | The guide flags the need. No filing assumed |
| Q-13 | Can you show a one-page sheet of the 16 px marks to five or more people before Gate 2? | The Act mark, the similarity limit and the pixel-fit limit are studio thresholds that no reader has checked | Studio thresholds only, marked untested |
| Q-14 | Who made page 14 of `pics_i_like.pdf`, the rendered data visualization study? | It is the only page whose maker the rights review couldn't trace | Study only |

## 11. Decisions made

The studio's routine decisions D1-01 to D1-27 are in `work/ledger/20261020_Decision-Log.md`. Six of them set working rules for the boards: D1-20 the red rule, D1-21 no dotted or dashed line in any brand graphic, D1-22 the hinge divider's ink, D1-23 the ask button, D1-26 the red rule's amended wording and D1-27 its ID, Rule 05.3. They become guide rules only through your answers to call 4 and the set in section 6.

## 12. Change log

Phase 1 changed no V5 master and no file in `source/` or `work/extract/`. Your two supplied additions went into `source/` as received. Paths are relative to `oath-and-action-v6-brand-guide/`.

**Created**

- `brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`
- `source/pics_i_like.pdf` and `source/brand-mockups/` (four mockups), your supplied files, recorded in the source manifest
- `work/ledger/`: `20261021_Guide-Architecture-Map.md`, `20261021_Token-Architecture.md`, this report
- `work/research/20261021_Research-Ledger.md`
- `work/handoffs/phase-1/`: 16 files, the notes, reviews, issue list and measurement data named in section 1, with `20261021_CD-Recheck-After-Fixes.md`
- `work/boards/`: the five Phase 1 boards, `20261021_Gate-1-Review-Board.html`, `20261021_Board-Conventions.md`, `board-base.css`
- `work/boards/phase-1/`: identity (1,466 files: SVG proposals in eight item folders and rendered cells), symbols (109), strategy (22), navigation (11, the guide shell among them), systems (9), gate-1 (the combined board's template and images)
- `work/build/scripts/phase-1/`: 44 build, render and check scripts, plus the Gate 1 board builder
- `work/build/tokens/20261021_Token-Schema-Draft.json`

**Modified**

- `CLAUDE.md` and all seven files in `.claude/agents/`, to point to Brief V2 and to add the naming rule for living ledgers
- `brief/phase-prompts/20261020_V6-Phase-0-Intake-And-Review.md`, ledger names
- `.gitignore`
- `work/ledger/`: `20261020_Decision-Log.md` (DC-05 to DC-10, D1-01 to D1-27), `20261020_Change-Ledger.md` (C-002 to C-004), `20261020_Open-Questions.md` (Q-01 to Q-10 answered, Q-11 to Q-14 added), `20261020_Source-Manifest.md` (the October 21 additions)
- `work/research/20261020_Rights-Ledger.md`, with the Phase 1 rights addendum appended
