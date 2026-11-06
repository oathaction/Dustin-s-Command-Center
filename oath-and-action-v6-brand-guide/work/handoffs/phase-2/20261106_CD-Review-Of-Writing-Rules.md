# Creative director review: chapter 02 writing rules, Board 5

oa-creative-director, November 6, 2026. Reviewed: `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md` with its notes, `work/boards/phase-2/voice/20261106_Voice-Rules-Content.json` and the draft board `work/boards/20261106_Voice-Writing-Rules-Board.html`, against the brief `20261106_Voice-Writing-Rules-Brief.md`, DR-62 to DR-72 and `work/handoffs/phase-1/20261021_Voice-Line-And-Headlines.md`. Renders and probes sit in my scratchpad and are not committed.

## Decision or verdict

Not ready for Dustin. One fix pass by the editor, then one by the main session on the board, should clear it.

Every before marked real is quoted exactly, the rule texts are plain and teachable, and the terms lines define each pattern in words a newcomer follows. Twelve afters break a rule on the page or change a fact, eight of them badly enough to fix before Dustin sees the board, while the page tells readers every after passes. Thirteen of the 21 befores come from the brand's own design notes and slogans, so the chapter teaches civic writing mostly with captions and board headings. On the board, five sections are empty, the house rules hide their examples on a phone, and no specimen card shows the edit itself.

## Scores

| Criterion | Score | Reason |
|---|---|---|
| Craft | 3 | Twelve afters break a rule or change a fact (section 1), W04 prints the token "[em dash]", the h1 breaks the name after "Oath &", and H01's example uses straight quotes. |
| Clarity | 3 | The deck says what the chapter is for, but the source lines speak studio ("V5 guide", "Atlas V7", "Dark atlas", board names), and afters leave "lever", "hinge" and "Prussian" undefined. |
| Brand fidelity | 3 | Locked lines are exact and the page carries no red; Lora Italic is set on 21 rewrites, two composed examples, a source line, a figure demo and a chart label, and the brand name splits across lines. |
| Usefulness | 4 | Each rule is something a writer can act on today; the checklist covers about half the rules and mixes yes-passes with no-passes. |
| Evidence honesty | 3 | All befores verify, yet the page gives three different counts of Illustrative items, prints "Every after keeps the before's facts" over W10, W14 and W16, and shows real jobs and election figures with no source line. |
| Accessibility | 3 | Contrast holds at 5.49:1 or better and targets reach 44 px, but at 390 px the house rules sit in a 720 px table that clips words, and five headings announce empty sections. |
| Beauty and distinctiveness | 3 | Calm, clean type set in 21 identical cards, specimens no larger than the rule text, no brand device, and a first screen of plain text beside an empty box. |

## Reasons

### 1. Every after against the full list

Passes: W01, W02, W04, W07, W08, W09, W10 (its change of meaning is deliberate, see note 3), W12 and W17. On the board, W04, W08 and W17 lose the Illustrative label beside the after (H03).

| Rule | What breaks | Rule broken |
|---|---|---|
| W03 | "Congress acts first." is a three-word teaser kept for rhythm, as the why line admits ("lets the voice rise and fall"). "Several years" narrows "multi-year". | W11, W12, fact |
| W05 | Narrows "the process" to two places and drops the general instruction. | fact |
| W06 | "the same record, starting from different pages" sets same against different, the pattern this rule removes. | W05, W06 |
| W11 | "the one point where a change moves the whole structure" claims more than the atlas glossary's leverage point. | W21, H08 |
| W13 | The before has no landing sentence. The after closes on an added comparison, a new claim, and sets "OATH and ACTION" in capitals. | W13, fact |
| W14 | A call to act becomes a navigation line, so the meaning changes. | fact |
| W15, W19 | Caption fragments, and W19's "in which" is written register. "Prussian" is never defined. | W01, H02 |
| W16 | "tells you nothing" is stronger than "establishes no claim", and "alone" is gone. | fact, H08 |
| W18 | In V5's reduced-motion paragraph, "simply" and "already" carry meaning (no animation, assembled from the start). The why line calls them filler, and the after leaves "lever" and "hinge" undefined. | W18 misapplied, H02 |
| W19 | "leverage mark" uses leverage as a noun in the leverage-point sense that W19's own terms line exempts, so the before shows no corporate verb. | example shows no fault |
| W20 | "Tell the people who decide what you think" parses as people who decide your thoughts. | W01 |
| W21 | "The page for Loop R10, the safe-seat loop, and the icon card" reads as a list of three; "catches the eye first of the five" is unspoken word order; "ready to show as finished work" is an unlabeled judgment. | W01, W21 |

### 2. Befores marked real, checked by script

`verify_befores.py` searched each named file. All 18 befores marked real, plus W08 (a real draft with invented contents), appear verbatim. W02, W03 and W12 sit in `20261105_Atlas-Editorial-Data.json` under the named fields (pathway "Why is my electric bill going up?", reform R-27, story part "Who holds the money and the market"). W01, W05, W11, W14, W15, W19 and W20 match the V5 text census exactly, and W09 and W10 match its 50-character cut. W16 and W18 exist only in the Phase 0 editor audit, and W07 only in the creative director audit, read from a screenshot; the V5 HTML is not in this checkout. W06 and W13 sit in the Phase 1 editor review, and both boards now carry the fixed wording. W21 sits on the November 5 board. One correction to the editor's notes: the census does record a closing h2, "Put the promise", so W14's source holds.

### 3. The editor's own prose

- "Each asks for sentences you could say aloud to a neighbor." A landing line, and H04 to H10 ask for other things.
- "Nearly every rule below quotes a sentence we published or drafted" and "We wrote the other two ourselves": a hedge and a wrong count. Three items carry the label, and the board says 18 real where the notes say 19.
- "the label every invented place or date carries" disagrees with H03 (person, quote, place or figure).
- "Beside each, we rewrite the same facts" is untrue for W10, W14 and W16.
- H03 "right on the item": an intensifier.
- W01 why "Nobody says ... out loud" and W19 why "'Leverage' is boardroom talk.": sweeping, and they sneer at the founder's own V5 lines.
- W15 "which word is the subject": the stack hides the head noun, which is a different thing.
- Board chrome: "21 rules in 4 groups. 18 of the befores" (H06, figure opening a sentence), "The rules every page already follows" (untrue), "The editor wrote it, the creative director read it against itself" (two clauses joined by a comma alone, W06 and W11).

By script: no em or en dashes in any of the three files, and the locked lines match Master Brief section 3 exactly wherever they appear.

### 4. Narrative, order and coverage

The opening explains duty and compliance ("carry out", "govern") and spends a third of its words on sourcing. It never shows what plain writing does for a reader. The tagline promises a country that answers to its people, and a sentence that names who acts is how writing keeps that promise, so the opening should start there. Here is a direction for the editor, 145 words, with every locked line exact.

> Our tagline is "A country that answers to its people." People can hold an office to account once they know which office decided. So we name who acts, in words you would use at a kitchen table, as in "A regulator or a board approves your rate."
>
> Our reader promise is "We explain how a decision is made and give you a practical way to take part." A reader can take part only in a decision they can follow, which is why our editorial commitment, "Clarity is our duty. Action is our promise.", puts clear writing first.
>
> Dustin Cathcart, our founder and editor, set these rules, and they govern everything Oath & Action publishes. Each rule shows a line from our own work, or one we wrote and labeled Illustrative where we found none, and rewrites it to pass every rule on the page.

Teaching order. The em dash, a mechanical rule, sits between sentence rhythm and negation, and the openings rule (W08) closes its group while the endings rules sit in the next. Regroup into five: 1 Sound like a person talking (W01, W02, W03, W11); 2 Put the point first and stop (W08, W12, W13, W14); 3 Say what is so (W05, W06, W07, W09, W10); 4 Cut the padding (W15 to W21); 5 Marks and numbers (W04 with H05 to H07).

Overlaps: W20 and W21 both cover praise for our own work, so move it to W21; W17 and H08 both cover grade verbs, so cross-refer them. Missing: a scope line saying headings, labels, captions and chart keys may be phrases; and a rule for a nonpartisan publication's hardest word choice, using the neutral name for a contested policy and saying who uses a side's term when it must appear.

### 5. Balance and tone

No before names a person, party or public figure, and every before is Oath & Action's own copy, so nobody outside the house looks foolish. The spread is uneven. Thirteen befores concern the brand's design notes and slogans; eight concern civic life. The three policy befores that carry a lean in public debate (IRS enforcement W03, automatic voter registration W17, concentrated wealth W12) all concern reforms or framings more often argued from the left, in my judgment, and the only party named on the page is "Georgia Republican +2.2". Swap W03 for a reform both parties have backed with the same three short steps, such as Atlas V7 R-19, rules for drug-pricing middlemen (enacted as P.L. 119-75), and show H10 as the stretch page's Georgia row, Democratic +0.2 in 2020 and Republican +2.2 in 2024.

Civic replacements found in committed files: V5's "Written testimony counts. Spoken testimony counts more." (editor audit, section 2) for W06; the dark atlas part "Whether voters can fire them", whose last sentence restates its first, for W13; the stretch test's first S16 title, whose "eligible voters" claimed more than the survey measured (stretch red team ST-S4), for W21.

### 6. The page as design

Rendered with Playwright at 1440 and 390 px, deviceScaleFactor 2. Fonts loaded (Inter 400, 600 and 700, Inter Tight 800, Lora Italic 400). No horizontal page scroll at either width. The page runs 12,733 px tall at 1440 and 21,272 px at 390, where the first rule starts 2,250 px down.

- Hierarchy: specimens set at 18 px against 17 px rule text, so the pair, the part a reader remembers, has no more weight than the instruction. Set specimens at 22 px on desktop and 19 px on phones. Give group breaks a large numeral and the group's rule names; cards drop to a 1 px rule.
- Show the edit. Mark the fault in each before with a Stone strike or dotted underline and the repair in each after with a Charcoal underline, with a 13 px note naming the fault. Join before and after with the hinge divider, the hairline broken by a small Charcoal ampersand, so the brand's own device carries its idea of a promise followed by action, and the page reads as Oath & Action with the wordmark covered.
- Add a rule index after the opening: all rule names on one screen, in their groups, each linked. It replaces the locked-lines panel, which repeats lines the opening already quotes.
- Lora Italic: keep it for quotations, meaning the locked lines and Dustin's own words. Set befores and afters in Inter, as the copy runs in production, with W06's heading in Inter Tight. At the least, take Lora off H04's source line, H07's figures (show them in Inter with tabular figures, the point of that rule) and H10's chart label.
- Cards: drop the "In plain words:" prefix, which produces "In plain words: Plain prose:"; bold the term instead. Put an Illustrative chip beside the after in W04, W08 and W17, and cut the repeated "Illustrative." from their source lines. Draw W04's dash.
- Phone: house rules become stacked cards below 720 px. Shorten the masthead label, which wraps "CHAPTER / 02, VOICE". Collapse the nine-link contents into one scrolling row. Checklist columns read down, 1 to 5 then 6 to 10.
- Finish or remove the empty ask, decisions, process, checks and change-log sections. Keep the name whole in the h1 with `Oath&nbsp;&amp;&nbsp;Action`.

### 7. The editor's notes for Dustin

1. Locked lines exemption: confirm; H01 states it, and W10's card should say so where a reader meets the contradiction.
2. Hinge headlines and W06: confirm, and show "The zoning code & the rent." in W06's terms line with the reason, a rule joined to its result.
3. W10's after: keep voice line B (G1-01). The why line names the dropped "We expose the gaps", and the page's fact claim names W10 as its one deliberate change.
4. Failing V5 lines: retire all four with no role; the locked lines and voice line B cover each job.
5. Twenty-one rules: keep them, since each carries its own worked example; regroup into five and add the index.
6. The em dash: draw it, as an inline SVG rule one em wide labeled "em dash" for screen readers.
7. "May" and "can": confirm; they report a plausible grade, as H08 says.
8. Studio drafts: keep W08, a civic mock; swap W06, W13 and W21, because a public reader cannot check an internal board and civic sentences teach more.
9. H11: add it, in public words: name what an ID refers to the first time, as in "Loop R10, the safe-seat loop".

## Required changes

### Must-fix, one pass

Editor:

1. Reconcile the Illustrative count (W04, W08, W17) across opening, deck, board line and notes, and make every claim about afters true.
2. Rewrite or replace the afters for W06, W13, W16, W18, W19, W20 and W21 as section 1 sets out. Suggested: W16 "How much a town sets aside for a service does not, by itself, show how good the service is."; W20 "Before they vote, let the officials who decide know what you think." For W18 and W19, use labeled Illustrative civic befores, such as "The hearing is really the last chance to speak before the council votes." and "The county will leverage federal funds to expand broadband access.", with afters that cut "really" and say "use federal money to bring broadband to more homes".
3. Add the scope line for headings, labels, captions and chart keys, and define Prussian in W15.
4. Fix the prose lines quoted in section 3.
5. Write source lines in public words, defined once ("our brand guide, fifth edition"; "our systems atlas, Who Do They Answer To?"; "an early draft of this guide"), and move provenance detail to the notes.
6. Give the H06, H08 and H10 examples their source lines, as H04 requires.

Main session, on the board:

7. Fill or remove the five empty sections, and fix the board lines quoted in section 3.
8. Keep the brand name whole in the h1; use curly quotes in H01.
9. Add Illustrative chips to the three afters, draw W04's dash and remove "In plain words:".
10. Stack the house rules on phones, and take Lora off H04, H07 and H10.

### Should-fix

1. Regroup into the five teaching groups and add the rule index.
2. Rebalance topics and lean: the three civic swaps and R-19 for W03, and the two-party Georgia row in H10.
3. W03: drop the teaser and keep "multi-year". W05: "Photograph public work while it happens, such as a hearing or a polling place." W11: "a point where a small change has a large effect". W14: teach with an article ending that closes on a dated step.
4. Why lines: say "the rewrite" in place of "the after", and say what reads better aloud, as the brief asks.
5. H08: show S16's first title and its fix, with the five grade words defined in a small table. H09: give the reason (a split at an inauguration invites credit or blame for one administration) and print why the window starts in January 2022.
6. Checklist: phrase every question so yes means pass (Q7 reads "Can any heavy noun give its verb back"); add party names and neutral terms, and dates, numbers and minus signs.
7. Propose H12 on neutral terms for contested policies to Dustin.
8. Design: larger specimens, marked edits, the hinge divider, stronger group breaks, a compact phone header and contents.

## Risks for Dustin to weigh

- His own V5 lines appear as failures (W10, W11, W14, W20). That is honest and persuasive, and the why lines must explain without scorn.
- The editorial commitment fails W10 by form. Unless H01's exemption is stated where readers see W10, critics will quote the guide against itself.
- The scope line decides how strict the rules are for headlines and captions. Without it, every hinge headline and chart label counts as a fault.
- Without a neutral-terms rule, the chapter guards party colors and names but leaves word choice, where partisan framing most often enters, unguarded.

## Tested

- Every before marked real, plus W08, searched by script in the files its source names: 19 of 19 found verbatim (`verify_befores.py`).
- Atlas field paths for W02, W03, W12 and W17 (R-05, graded plausible, "small but positive"), the glossary entry for cloture and the R10 plain name.
- House examples H04 to H08 and H10 found verbatim on the stretch page; H01, H02, H03 and H09 are composed or quoted from elsewhere.
- Em and en dashes in the three files (none); locked lines character for character.
- Each after read against all 31 rules, and the editor's prose scanned by script for negation, hedges, intensifiers and passives, then read.
- Board rendered at 1440 and 390 px at twice size, with probes for fonts, overflow, Lora use, empty sections, card measures, tap targets and contrast.

## Not tested

- V5 quotes against the V5 HTML, which is not in this checkout.
- How the rules sound read aloud to real readers.
- Screen reader output.
- Widths other than 1440 and 390 px.

## Change log

- Created `work/handoffs/phase-2/20261106_CD-Review-Of-Writing-Rules.md` (this file).
- Modified: none. Renders, probes and scripts stay in the session scratchpad, `review-voice/`.
