# Creative director recheck after the Phase 1 fixes

oa-creative-director, October 21, 2026. This checks the fix round against `20261021_CD-Review-Of-Phase-1.md`. I changed no board, master, note or ledger, and I did not open `source/`.

## Verdict

Hold the boards for one more short pass. Six of the seven required changes landed in full, and the seventh landed in its wording. The hinge diagram is now one solid, clockwise drawing on three boards, every hinge headline sets the V5 master ampersand, and the red rule appears word for word on every board. Four defects would mislead Dustin, and each one is a small fix:

1. The nonpartisan set lost "Red never marks a party, a side or a person." when NP-04 was replaced by the red rule.
2. The identity board still renders proposals on Prussian in color with a red ampersand or lever, five of them in item 9's visible grid.
3. The composite post sets two different ampersand drawings in one view.
4. The red rule carries two IDs, Rule 01.1 and Rule 05.3, and the map uses Rule 01.1 for a different rule.

After those four, the boards can go to Dustin. The other items below can travel as notes.

## Required changes, status

| # | Change | Status | Evidence |
|---|---|---|---|
| 1 | Item 7 redrawn solid, clockwise, UNDERSTAND and IMPACT below; primer and strategy reuse it | Landed | Identity item 7 shows V5, the withdrawn draft and "V2: solid hairline arcs, clockwise" side by side. Strategy section 1 and systems mark 7 inline the same V2 masters. Neither V2 SVG contains `stroke-dasharray`. At 390 px both boards switch to the compact master, which drops the labels as specified. |
| 2 | Hinge headlines in the V5 master; Act divider ampersand in Charcoal | Landed | All five hinge headline cards set the ampersand as an SVG path in Pillar Red (DOM check, five 18 by 21 px paths). Both Act mocks draw a Charcoal divider ampersand and spend their one red on the ask. |
| 3 | One red rule and treatment D in place of five wordings | Partly landed | The rule is verbatim in Strategy Rule 01.1, the identity decisions, symbol decision 4, systems rule 4 and shell Rule 05.3, and Rule 01.4 states treatment D. Three defects came with it: NP-04's party clause is gone, the rule now has two IDs, and the identity renders still put red on Prussian. |
| 4 | Renumber Voice-Line-And-Headlines section 3 and the strategy notes to the map | Landed | A script match finds all 28 chapter numbers and names in the editor's table identical to the map. The strategy notes cite "01 Purpose", "08 The Signal Grid", "13 Evidence and sourcing" and "16 Photography, illustration and video". |
| 5 | Symbol sections 6 and 7: Option tag, Defect fix on the split only, dotted-arc pattern dropped | Landed | Section 6 opens with OPTION and reads "DEFECT FIX applies to one change only: splitting Contact an official from Campaign money". Section 7's patterns are node rhythm, halftone nodes and rule rhythm, and the board has no dashed stroke. |
| 6 | Recommend Rule NN.n and hold Std-01 | Landed | Mark 3: "Cite guide rules as Rule NN.n, as the architecture map proposes, and hold Std-01." The decisions panel reads "Std-01 held". |
| 7 | The editor's ranked fixes, American spelling, item 8 and 9 thresholds | Landed, one miss | A text scan of the six boards and the revised notes finds no em or en dashes and no British spellings. Items 8 and 9 both give "16 px master from 16 to 23 px; 24 px master from 24 to 47 px; V5 master from 48 px". Decision 6 now carries one recommendation, item 5 reads "0.48 to 0.61", and every story-list headline carries "Illustrative". The miss: `20261021_Research-Summary.md` item 3 still reads "Brief section 13 rules the pairing out." |

Conflicts C1 to C17, where a board shows them:

| # | Status | Evidence |
|---|---|---|
| C1 | Landed | Solid arcs on the identity, strategy and systems boards; the symbol patterns hold no dotted line |
| C2 | Partly | Every text says White on Prussian (Rule 01.4, systems rule 4, token roles), and the systems primer renders White. The identity renders still show red there |
| C3 | Partly | Verbatim on every board, and the composite counts the Act handle. Decision D1-22 sets the divider ampersand by surface, which the quoted rule omits. Identity item 7 calls the hinge diagram's ampersand "the view's working red"; the composite draws it in Charcoal |
| C4 | Partly | Rule NN.n adopted and the NP rules became Rules 01.1 to 01.20. The red rule is Rule 01.1 on the strategy board and Rule 05.3 on the map, wireframes and shell. The map's own Rule 01.1 is the "People belong in the picture." opener |
| C5 | Landed | Strategy's R9 figure uses the hollow line with the word "Hypothesis" |
| C6 | Landed | The treatments table gives tiles to "Social avatars, app tiles, series chips"; item 9 gives favicons to the ampersand's 16 px master |
| C7 | Landed | Item 3: "the 16 px master of the recommended ampersand, B" |
| C8 | Landed | Strategy section 4: "This table belongs in 02 Voice; the uses sit in 01 and 08." |
| C9 | Landed | Token architecture section 8: "chapter 26, in Production" |
| C10 | Landed | The boards say "hinge diagram"; no board uses "hinge loop", "hinge mark" or "hinge node"; the chips state the 0.06 em token |
| C11 | Landed | Strategy section 7 and the shell cover use Direction A's marks |
| C12 | Landed | Strategy decision 14 |
| C13, C14 | Landed | Systems primer: V2, clockwise, UNDERSTAND and IMPACT, with its arc captions |
| C15 | Partly | The master glyph landed. The board shows "The permit delay & the by-right rule." as "pending the editor's redraft", and the editor's file already offers "The lead pipe rule & your tap water." |
| C16 | Partly | Numbers and names match. 27 of 28 instruction lines differ between the map (and shell) and the editor's table. For 05 the map says "Choose a surface first, then the text and graphic colors that pass on it." and the editor says "Give Pillar Red one job." |
| C17 | Landed as a note | The identity notes and the composite caption state the Phase 2 drawing, and the condensed post shows the mismatch |

## Red rule audit

Method: on every render I found each cluster of Pillar Red pixels, assigned it to its board section, and flagged any cluster within 3 px of Prussian pixels. Then I judged each specimen by eye. Signature red is left out of the counts. A second set of renders at 1440 px opened every collapsed panel.

| Board | Most working reds in one view | Red on Prussian |
|---|---|---|
| Strategy, 1440 and 390 | One per specimen. Each Act mock spends it on the ask, each hinge headline card and the V2 figure on the ampersand, the Rule 01.2 failure case on one bar | None |
| Identity, 1440 and 390 | One per specimen | Yes. By default 24 red clusters touch Prussian at 1440 and 20 at 390, all in items 9 and 10. Item 9's visible grid shows "Proposal, Prussian, color" in red for L1, L2, L5, the compact hinge diagram and the lockmark lever, under the check "Red discipline: Pass". Item 10 still draws options A and C, which its text retires. With panels open, items 1 to 8 add 12 to 30 such clusters each, and their "Proposal, Prussian, color" rows are red. That includes item 7's V2, whose check reads "On Prussian the ampersand follows treatment D" |
| Symbols, 1440 and 390 | One per specimen: the Act handle in Act contexts. The composite spends it on the Act handle beside the signature wordmark | None; Prussian cells are one color |
| Systems, 1440 and 390 | One job per figure. The R10 figure marks Reform R-01's three targets with three red rings | None; the primer's Prussian cell is White |
| Wireframes, 1440 and 390 | No red found | None |
| Guide shell, 1440 and 390 | Two reds share a screen in 05 Color. The error state's red mark and the labeled V5 failure dot sit 444 px apart at 1440 and 540 px apart at 390, and the dot shares the next screen with the Pillar Red swatch | None. The palette table lists Pillar Red on Prussian as "Large and graphics" with no note that red never sits there |

The audit also showed two cases the rule's wording leaves open. A guide page shows labeled failure cases and swatches. A systems figure can mark several targets of one reform.

## Rubric re-scores

Master Brief V2 section 6, ship threshold 4. Rows marked Held kept their scores because their work did not change, or changed only in wording that leaves the score where it was.

| Proposal | Round | Cr | Cl | BF | U | EH | A | Reason for the lowest score |
|---|---|---|---|---|---|---|---|---|
| Strategy and narrative* | Re-scored | 4 | 4 | 4 | 3 | 4 | 4 | "Rule 01.1" names two different rules across this board and the map, and NP-04's party clause fell out |
| Act pattern* | Re-scored | 3 | 4 | 4 | 4 | 5 | 4 | Still board sketches at no true ratio; Phase 2 rebuilds them in guide tokens |
| Voice line, revision B | Held | 4 | 4 | 4 | 4 | 4 | 4 | Echoes the reader promise; untested with readers |
| Identity 1, re-export | Held | 5 | 5 | 5 | 5 | 5 | 4 | Lockup taglines stay small until item 9 |
| 2, hinge gaps 2b | Re-scored | 4 | 4 | 4 | 4 | 5 | 4 | Its opened Prussian color cells show the red ampersand |
| 3, wordmark masters | Re-scored | 4 | 4 | 4 | 5 | 5 | 4 | The larger small-size ampersand changes a V5 measure, and its Prussian color cells show red |
| 4, ampersand A | Held | 4 | 4 | 5 | 4 | 5 | 4 | Stays a stock glyph |
| 5, ampersand B | Held | 4 | 4 | 4 | 4 | 5 | 4 | First drawing, 0.77 overlap with Lora |
| 6, condensed | Held | 3 | 4 | 3 | 4 | 5 | 4 | A measured transform that changes locked proportions |
| 7, hinge diagram* | Re-scored | 4 | 4 | 3 | 4 | 4 | 4 | Its Prussian color cells put the red ampersand on Prussian, under a check that claims treatment D |
| 8, lockmark masters | Re-scored | 5 | 4 | 4 | 5 | 4 | 4 | Check 8 now passes the lever's 2.96:1 by citing the red rule, a rule about how many reds a view spends |
| 9, minimum sizes | Re-scored | 4 | 4 | 3 | 5 | 5 | 4 | Its visible grid shows five proposals in red on Prussian under "Red discipline: Pass" |
| 10, Prussian D | Re-scored | 4 | 4 | 4 | 4 | 5 | 5 | Gives up the banner's red ampersand; options A and C stay drawn after the text retires them |
| Composite Act post (new) | Scored | 4 | 4 | 3 | 3 | 4 | 4 | Two ampersand drawings in one post, and no sizes or tokens a producer could reuse |
| Symbols, Direction A | Held | 4 | 4 | 4 | 3 | 5 | 4 | No exports, 16 topics undrawn |
| Symbols, Direction B | Held | 3 | 3 | 3 | 3 | 5 | 3 | Line masters fail at 16 px |
| Systems 1, evidence lines | Held | 4 | 4 | 5 | 4 | 5 | 4 | Record square needs V7.1 |
| 2, grade words | Re-scored | 4 | 4 | 5 | 4 | 5 | 4 | Untested with readers; the two spellings are now one |
| 3, typed chips* | Re-scored | 4 | 4 | 4 | 4 | 5 | 4 | Untested with readers, and Rule NN.n waits on decision T2 |
| 4, effect mark | Held | 4 | 4 | 5 | 4 | 5 | 4 | Untested with readers |
| 5, event mark | Held | 4 | 4 | 4 | 4 | 5 | 4 | Four shapes need a key on every figure |
| 6, authority and delay | Held | 4 | 4 | 4 | 4 | 5 | 4 | Untested with readers |
| 7, hinge primer* | Re-scored | 4 | 4 | 4 | 4 | 5 | 4 | The R10 figure spends red on three rings for one reform, a case the rule's wording leaves open |
| 8, atlas bases | Held | 4 | 4 | 4 | 4 | 5 | 4 | The changes exist only as text |
| Architecture and navigation | Re-scored | 4 | 4 | 3 | 4 | 5 | 4 | With the wordmark covered, only the cover's pillar row reads as Oath & Action |
| Token architecture | Re-scored | 4 | 4 | 4 | 4 | 4 | 4 | DTCG pages still unread, and D1-22's divider ink differs from the red rule's wording |

Instructions for each row under 4 sit in "Remaining issues". The Act pattern, item 6 and both symbol directions stay under threshold for reasons their boards already give, and they go to the gate with those reasons.

## Composite post

Section 11 delivers what section 3 of my review asked for. It shows three posts at 1080 by 1350: the wordmark with ampersand B at today's width, the condensed 7.5 to 1 wordmark with the narrow B, and a covered version. Each carries the V2 hinge diagram, Direction A's marks and the red rule, with the Act handle as the one working red. I rendered the posts at 3x, so each one sits at its true 1080 px width.

With the wordmark covered, the post holds together through the serif ampersand in its ring, the node that the hinge line shares with all four pillar marks, and one red point on Newsprint and Charcoal. Four things work against one identity:

- The post sets two ampersand drawings. The path data confirms it: the wordmark's ampersand has ampersand B's 40 cubic segments, and the hinge diagram's has the V5 sprite's 57 quadratic segments. At true size the two read as different letters.
- The hinge diagram repeats OATH and ACTION, so each post names the brand twice. The covered version had to blank the hinge words too, which shows the diagram acting as a second wordmark.
- The condensed post sets condensed capitals above today's-width hinge letters.
- The lockmark is missing, though it is one of the five retained identity elements and Dustin's references place it at bottom right.

What still reads generic:

- The card itself: an Inter Tight headline over a numbered list on a flat ground, closed by a hairline.
- The tracked "ACT" label beside a large icon, a category badge that many apps use.
- The bottom row of four labeled icons, which reads as an app tab bar.
- The steps, which name no date, place or office as the Act pattern requires, so the post reads as general advice.
- The headline, which leaves out the hinge headline, the system's strongest typographic device.

Instruction: put the hinge divider, a hairline broken by a small Charcoal ampersand B, where the hinge diagram sits now. Draw every ampersand from B, add the lockmark at bottom right, and give step 1 an illustrative date and place. Add one version with a hinge headline whose ampersand is the working red, with the Act handle in Charcoal. Then run the covered test again.

## Gate 1 decision changes

Of the 37 decisions, 27 stand as written. These ten change:

- **S7.** The board now offers "Adopt Rules 01.1 to 01.20" with "the red rule as Rule 01.1". I now recommend that the red rule keep its home as Rule 05.3 in 05 Color, where the map, wireframes and shell already place it. 01 Purpose cites Rule 05.3 and restores "Red never marks a party, a side or a person." as its own rule, in one list with the map's 01 rules.
- **I3.** The recommendation now leads with ampersand B's small masters, with the A versions as the fallback. I agree.
- **I5.** The identity row now says "Condensed 7.5 to 1 as the Phase 2 direction", while strategy decision 13 keeps "Draw it. The current width stays in force until Gate 2". The identity row should take the strategy wording. My recommendation stays.
- **I6.** The options differ by board. Identity lists "V2 with solid arcs, V2 without the return arc, or keep V5"; strategy and systems list V2, two-way dashed arcs and V5's dotted arc. One list of all four should go to Dustin. The recommendation stays V2 with the five separation rules.
- **I9.** It now depends on I10: under the red rule A and C fall away, leaving B and D. D stays recommended.
- **I10.** Add four sentences before Dustin adopts the rule. First: "The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian." (D1-22 already decided this.) Second: "The hinge diagram is an identity mark: its ampersand is signature red, and it never shares a view with the wordmark or stands in for the hinge divider." Third: "In the guide itself, labeled failure cases and palette swatches do not count." Fourth: "One job may take several marks, such as each target of one reform."
- **Y6.** The treatments map dropped the dotted-arc pattern. The recommendation stays.
- **M3.** The options now include Rule NN.n against Std-01, with Std-01 held. I agree.
- **T2.** Architecture decision A7 gains option (c), Std-01 to Std-10. The recommendation stays (a).
- **T5.** The token decisions now run T-1 to T-11. New T-7 asks whether the ask button takes a White label (4.17:1) or a Charcoal label (4.49:1), recommending White at 19 px bold, and T-6 now offers "the red rule with keylines" against "a derived red". I agree with both.

## Remaining issues, ranked

1. **The party clause is gone** (strategy section 6, Brand-Strategy section 6). Dustin would adopt Rules 01.1 to 01.20 believing they are NP-01 to NP-20 renumbered. Restore "Red never marks a party, a side or a person." as its own rule in 01 Purpose.
2. **Red on Prussian in the identity renders** (item 9 by default, items 1 to 8 when opened). Dustin would approve minimum sizes and the hinge diagram from cells that break the rule he adopts two rows below. Re-render every "Proposal, Prussian, color" cell under treatment D, with a White ampersand and lever, or drop that row. Then correct item 7's check 8 and item 9's check 7.
3. **The composite mixes two ampersands and names the brand twice.** Dustin would judge "one identity" from a post that sets B beside the V5 glyph. Follow the instruction under "Composite post".
4. **The red rule has two IDs.** Strategy says Rule 01.1, the map, wireframes and shell say Rule 05.3, and the map's own Rule 01.1 is another rule. Keep Rule 05.3, write 01 Purpose's rules as one numbered list, and have the strategy board cite Rule 05.3.
5. **The quoted rule omits two settled points.** D1-22 sets the divider by surface, and the boards disagree on the hinge diagram's ampersand. Add the four sentences listed under I10.
6. **Two sets of chapter instruction lines** (27 of 28 differ). The editor and the UX lead pick one set, and the map, the shell and the editor's file carry it.
7. **Decision rows disagree across boards** on I5 and I6. Send one wording and one option list for each.
8. **The problem-and-solution hinge pair** still shows "pending the editor's redraft" though the editor has delivered one. Put one finished pair on the board.
9. **Item 8's check 8** reads "Pass, by the red rule". Record it as "Fail on Newsprint, logotype; the lever's size carries its meaning in one color".
10. **The shell's palette table** gives Pillar Red on Prussian as "Large and graphics". Mark that cell "Not used: Rule 05.3".
11. **Minor.** The wireframe board's file list still says "Modified: none" after the fix round, and Research Summary item 3 keeps its unrevised sentence.

## Tested

- Rendered the five boards and the guide shell in Chromium through Playwright at 1440 and 390 px, full page, after forcing lazy images to load. All images loaded, no request failed, and page width matched the viewport at both widths.
- Read the 1440 px renders section by section, and the 390 px renders as strip sheets for the sections named in this file.
- Rendered the boards again at 1440 px with every collapsed panel open. Chromium returns blank pixels past about 90,000 px, so I captured the opened identity board one section at a time.
- Ran a pixel audit of Pillar Red clusters and their contact with Prussian on every render, plus a DOM inventory of red text, fills, strokes and backgrounds.
- Rendered the composite posts at 3x device scale and compared ampersand path data across the wordmark, hinge V2, ampersand B and the V5 sprite.
- Checked both V2 SVGs and every board for `stroke-dasharray`.
- Compared chapter numbers, names and instruction lines between the map and the editor's file by script.
- Scanned the six boards and the revised notes for em and en dashes, British spellings, stale IDs and retired terms.
- Read the git diff of every note, ledger and build script changed since the review commit.
- Confirmed that every clipped identity image sits in a scrolling region (114 at 1440 px, 929 at 390 px).

## Not tested

- Screen readers, keyboard order, forced colors, zoom, print, high-density screens and other browsers.
- Contrast and axe-core results; I relied on the makers' reports.
- Every 390 px sheet by eye. The pixel audit covered the sheets I did not read.
- Red inside the wireframe board's JPEG stills, where compression can move pixels outside the audit's tolerance.
- Readers, for the covered-wordmark test and the composite.

## Change log

Created: `work/handoffs/phase-1/20261021_CD-Recheck-After-Fixes.md`. Modified: none. Renders and audit scripts sit in the session scratchpad at `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/cd-recheck/`.
